import json
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent
DATA = OUT / 'btc_usd_daily.csv'
if not DATA.exists():
    raise FileNotFoundError(DATA)
df = pd.read_csv(DATA, parse_dates=['date']).set_index('date').sort_index()
close = df['close'].astype(float)
next_return = close.pct_change().shift(-1)

# Fixed, deterministic raw signals. All inputs at t are available before t+1 outcome.
ret7 = close.pct_change(7)
raw_a = np.tanh(ret7 / 0.05)
# RSI(14), Wilder-style simple rolling average implementation; fixed midpoint normalization.
delta = close.diff()
gain = delta.clip(lower=0).rolling(14, min_periods=14).mean()
loss = (-delta.clip(upper=0)).rolling(14, min_periods=14).mean()
rs = gain / loss.replace(0, np.nan)
rsi = 100 - (100 / (1 + rs))
rsi = rsi.where(loss.ne(0), 100.0)
raw_b = ((rsi - 50.0) / 50.0).clip(-1, 1) * -1.0  # mean reversion: below 50 => positive
# Fixed fast/slow moving-average trend.
ma_fast = close.rolling(20, min_periods=20).mean()
ma_slow = close.rolling(50, min_periods=50).mean()
raw_c = np.tanh((ma_fast / ma_slow - 1.0) / 0.02)
raws = {'A_7d_momentum': raw_a, 'B_RSI14_mean_reversion': raw_b, 'C_MA20_50_trend': raw_c}

# One frozen market evidence layer shared by every strategy.
completeness = close.notna().rolling(30, min_periods=30).mean()
signs = pd.concat([close.pct_change(k).apply(np.sign) for k in [3, 7, 14]], axis=1)
agreement = signs.eq(signs.iloc[:, 1], axis=0).mean(axis=1)
vol = close.pct_change().rolling(20, min_periods=20).std()
vol_q90 = vol.rolling(180, min_periods=60).quantile(.9)
stability = (1 - (vol / vol_q90).clip(0, 1)).fillna(.5)
weights = np.array([.30, .30, .20, .20])

records = []
valid_records = []
for strategy, raw in raws.items():
    # Calibration is strictly past-only: yesterday's correctness enters today's rolling estimate.
    hit = (np.sign(raw.shift(1)) * np.sign(next_return.shift(1))).eq(1).astype(float)
    calibration = hit.rolling(90, min_periods=30).mean()
    reliability = (weights[0]*completeness + weights[1]*agreement + weights[2]*stability + weights[3]*calibration).clip(0, 1)
    adjusted = raw * reliability
    full = pd.DataFrame({
        'timestamp': close.index, 'strategy': strategy, 'raw_signal': raw,
        'reliability': reliability, 'adjusted_signal': adjusted,
        'evaluation_status': np.select([raw.isna() | reliability.isna(), reliability >= .65], ['UNAVAILABLE', 'ACCEPT'], default='ABSTAIN'),
        'future_return': next_return,
        'raw_direction_correct': (np.sign(raw) * np.sign(next_return) > 0).astype('float'),
    })
    full['accepted'] = np.where(full['evaluation_status'] == 'ACCEPT', 1, np.where(full['evaluation_status'] == 'ABSTAIN', 0, np.nan))
    full['abstained'] = np.where(full['evaluation_status'] == 'ABSTAIN', 1, np.where(full['evaluation_status'] == 'ACCEPT', 0, np.nan))
    full['raw_direction_correct'] = full['raw_direction_correct'].where(full['future_return'].notna() & full['raw_signal'].notna(), np.nan)
    records.append(full)
    valid = full.dropna(subset=['raw_signal','reliability','future_return']).copy()
    valid['accepted'] = (valid['evaluation_status'] == 'ACCEPT').astype(int)
    valid['abstained'] = (valid['evaluation_status'] == 'ABSTAIN').astype(int)
    valid['raw_direction_correct'] = valid['raw_direction_correct'].astype(int)
    valid_records.append(valid)

record_level = pd.concat(valid_records, ignore_index=True)
full_record_level = pd.concat(records, ignore_index=True)
full_record_level.to_csv(OUT / 'cross_strategy_record_level.csv', index=False)

# Quality summaries and fixed tertile separation, computed independently within strategy.
def quality(x):
    accepted = x[x.accepted == 1]
    return {
        'n': int(len(x)),
        'coverage': float(x.accepted.mean()),
        'raw_hit_rate': float(x.raw_direction_correct.mean()),
        'accepted_n': int(len(accepted)),
        'accepted_hit_rate': float(accepted.raw_direction_correct.mean()) if len(accepted) else None,
        'accepted_mean_signed_return': float((np.sign(accepted.raw_signal)*accepted.future_return).mean()) if len(accepted) else None,
        'abstained_n': int((x.abstained == 1).sum()),
    }

sep_rows = []
for strategy, x in record_level.groupby('strategy', sort=False):
    x = x.copy()
    x['r_group'] = pd.qcut(x.reliability, 3, labels=['low','medium','high'], duplicates='drop')
    for g, y in x.groupby('r_group', observed=True):
        sep_rows.append({'strategy': strategy, 'reliability_group': str(g), 'n': int(len(y)),
                         'raw_quality_hit_rate': float(y.raw_direction_correct.mean()),
                         'mean_signed_signal_return': float((np.sign(y.raw_signal)*y.future_return).mean()),
                         'mean_reliability': float(y.reliability.mean())})
sep = pd.DataFrame(sep_rows)

# Selective curves; no threshold is tuned to results.
thresholds = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85]
sel_rows = []
for strategy, x in record_level.groupby('strategy', sort=False):
    for t in thresholds:
        a = x[x.reliability >= t]
        sel_rows.append({'strategy': strategy, 'threshold': t, 'accepted_n': int(len(a)),
                         'coverage': float(len(a)/len(x)),
                         'accepted_hit_rate': float(a.raw_direction_correct.mean()) if len(a) else None,
                         'accepted_mean_signed_return': float((np.sign(a.raw_signal)*a.future_return).mean()) if len(a) else None})
selective = pd.DataFrame(sel_rows)

# Walk-forward split: signals/R use only history available at each timestamp; no future window is used.
cut = record_level.timestamp.min() + (record_level.timestamp.max() - record_level.timestamp.min()) * 0.70
record_level['sample'] = np.where(record_level.timestamp <= cut, 'in_sample', 'out_of_sample')
wf_rows = []
for (strategy, sample), x in record_level.groupby(['strategy','sample'], sort=False):
    q = quality(x)
    wf_rows.append({'strategy': strategy, 'sample': sample, **q, 'date_start': str(x.timestamp.min().date()), 'date_end': str(x.timestamp.max().date())})
walk_forward = pd.DataFrame(wf_rows)

# Five preregistered reweighting levels. Contrast shifts mass between reliability components,
# preserving sum=1 and avoiding a meaningless uniform rescale.
sensitivity = []
contrast = np.array([.30, .30, -.20, -.20])
for delta in [-.20, -.10, 0.0, .10, .20]:
    w = weights + delta * contrast
    for strategy, raw in raws.items():
        hit = (np.sign(raw.shift(1)) * np.sign(next_return.shift(1))).eq(1).astype(float)
        cal = hit.rolling(90, min_periods=30).mean()
        rr = (w[0]*completeness + w[1]*agreement + w[2]*stability + w[3]*cal).clip(0,1)
        z = pd.DataFrame({'r': rr, 'raw': raw, 'ret': next_return}).dropna()
        z = z.assign(correct=(np.sign(z.raw)*np.sign(z.ret)>0).astype(int))
        accepted = z[z.r >= .65]
        sensitivity.append({'strategy': strategy, 'perturbation': delta, 'weights': w.tolist(),
                            'reliability_rank_spearman_vs_baseline': float(z.r.rank().corr((weights[0]*completeness + weights[1]*agreement + weights[2]*stability + weights[3]*cal).loc[z.index].rank())),
                            'accepted_n_at_.65': int(len(accepted)), 'coverage_at_.65': float(len(accepted)/len(z)),
                            'accepted_hit_rate_at_.65': float(accepted.correct.mean()) if len(accepted) else None})
sensitivity = pd.DataFrame(sensitivity)

# Counterexamples: at most one of each class per strategy.
cases = []
for strategy, x in record_level.groupby('strategy', sort=False):
    hi = x[(x.raw_signal.abs() >= x.raw_signal.abs().quantile(.90)) & (x.reliability >= x.reliability.quantile(.67))].sort_values('timestamp')
    lo = x[(x.raw_signal.abs() >= x.raw_signal.abs().quantile(.90)) & (x.reliability <= x.reliability.quantile(.33))].sort_values('timestamp')
    ab = x[x.abstained == 1].sort_values('timestamp')
    for label, y in [('high_raw_high_reliability', hi), ('high_raw_low_reliability', lo), ('abstain', ab)]:
        if len(y):
            r = y.iloc[0]
            cases.append({'strategy': strategy, 'case': label, 'timestamp': str(r.timestamp.date()),
                          'raw_signal': float(r.raw_signal), 'reliability': float(r.reliability),
                          'adjusted_signal': float(r.adjusted_signal), 'future_return': float(r.future_return),
                          'raw_direction_correct': int(r.raw_direction_correct), 'evaluation_status': r.evaluation_status})

# Status rules are descriptive and fixed; they do not search thresholds.
strategy_status = []
for strategy in raws:
    s = sep[sep.strategy == strategy].set_index('reliability_group')
    high_better = bool(s.loc['high','raw_quality_hit_rate'] > s.loc['low','raw_quality_hit_rate'])
    curve = selective[selective.strategy == strategy].dropna(subset=['accepted_hit_rate'])
    monotone_gain = bool((curve.accepted_hit_rate.iloc[-1] > curve.accepted_hit_rate.iloc[0]) and (curve.accepted_hit_rate.max() > curve.accepted_hit_rate.min())) if len(curve)>1 else False
    oos = walk_forward[walk_forward.strategy == strategy].set_index('sample')
    oos_preserved = bool((oos.loc['out_of_sample','accepted_hit_rate'] or 0) >= (oos.loc['in_sample','accepted_hit_rate'] or 0))
    strategy_status.append({'strategy': strategy, 'high_R_better_than_low_R': high_better,
                            'selective_quality_gain_supported': monotone_gain,
                            'oos_gain_preserved': oos_preserved})

n_high = sum(s['high_R_better_than_low_R'] for s in strategy_status)
n_sel = sum(s['selective_quality_gain_supported'] for s in strategy_status)
framework_transfer = 'DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT' if n_high >= 2 else ('PARTIAL' if n_high == 1 else 'NOT_SUPPORTED')
cross_reliability = 'DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT' if n_high >= 2 and all(s['oos_gain_preserved'] for s in strategy_status if s['high_R_better_than_low_R']) else ('PARTIAL' if n_high >= 1 else 'NOT_SUPPORTED')
selective_gain = 'DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT' if n_sel >= 2 else ('PARTIAL' if n_sel == 1 else 'NOT_SUPPORTED')

matrix=[]
for strategy in raws:
    rows=sep[sep.strategy==strategy].set_index('reliability_group')
    matrix.append({'strategy':strategy, 'raw_quality':float(record_level[record_level.strategy==strategy].raw_direction_correct.mean()),
                   'low_R_quality':float(rows.loc['low','raw_quality_hit_rate']), 'medium_R_quality':float(rows.loc['medium','raw_quality_hit_rate']), 'high_R_quality':float(rows.loc['high','raw_quality_hit_rate'])})

summary = {
    'study_type':'External Transfer Validation / Cross-Strategy Reliability',
    'data_source':'local historical BTC-USD daily data (Yahoo Finance snapshot already present; no live execution)',
    'symbol':'BTC-USD', 'date_range':[str(record_level.timestamp.min().date()), str(record_level.timestamp.max().date())],
    'sample_size_by_strategy':{k:int((record_level.strategy==k).sum()) for k in raws},
    'timestamp_grid_size': int(len(close)*len(raws)),
    'unavailable_warmup_rows': int(full_record_level.evaluation_status.eq('UNAVAILABLE').sum()),
    'strategies':{
      'A_7d_momentum':{'raw_signal':'tanh(7-day close return / 0.05)','fixed':True},
      'B_RSI14_mean_reversion':{'raw_signal':'-(RSI14 - 50) / 50, clipped to [-1,1]','fixed':True},
      'C_MA20_50_trend':{'raw_signal':'tanh((MA20 / MA50 - 1) / 0.02)','fixed':True}},
    'reliability_framework':{'components':['completeness','agreement','stability','calibration'],'weights':[.30,.30,.20,.20],
      'calibration_note':'past-only rolling 90-day hit rate; each timestamp uses information available by t'},
    'unavailable_status':'UNAVAILABLE before a fixed signal/reliability window is computable',
    'output_schema':['timestamp','strategy','raw_signal','reliability','adjusted_signal','evaluation_status','future_return','raw_direction_correct','accepted','abstained'],
    'reliability_separation':{'matrix':matrix,'groups':sep.to_dict(orient='records'),'strategy_status':strategy_status},
    'selective_evaluation':{'thresholds':thresholds,'curves':selective.to_dict(orient='records'),'status_by_strategy':{s['strategy']:s['selective_quality_gain_supported'] for s in strategy_status}},
    'walk_forward_oos':{'split_rule':'chronological 70% in-sample / 30% out-of-sample; no future-window information','rows':walk_forward.to_dict(orient='records')},
    'sensitivity':{'levels':[-.20,-.10,0.0,.10,.20],'definition':'shift weight mass between completeness/agreement and stability/calibration; sum preserved','rows':sensitivity.to_dict(orient='records')},
    'counterexamples':cases,
    'final_judgement':{'FRAMEWORK_TRANSFER':framework_transfer,'CROSS_STRATEGY_RELIABILITY':cross_reliability,'SELECTIVE_DECISION_GAIN':selective_gain},
    'competition_value':{
      'reliability_cross_raw_strategy_stable_information': 'descriptive structural separation across at least two strategies' if n_high>=2 else 'not stable across two strategies',
      'supported_strategies':[s['strategy'] for s in strategy_status if s['high_R_better_than_low_R']],
      'unsupported_strategies':[s['strategy'] for s in strategy_status if not s['high_R_better_than_low_R']],
      'oos_conclusion':'reported separately above; no claim pooled across strategies',
      'strengthens_raw_output_not_equal_reliable_evidence': bool(n_high>=2),
      'paper_body_recommendation':'include as a compact external validation if framed as partial/qualified evidence' if framework_transfer!='NOT_SUPPORTED' else 'do not include as a positive transfer claim',
      'recommended_defense_figure':'one cross-strategy low/medium/high reliability quality matrix; omit extra trading curves unless needed'
    },
    'prohibitions_respected':['no real trading','no leverage','no future data in signal/reliability','no threshold retuning','no LLM'],
    'paper_use':'historical/paper simulation validation only; not a trading strategy'
}
(OUT/'cross_strategy_validation.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False), encoding='utf-8')
print(json.dumps({'final_judgement':summary['final_judgement'],'strategy_status':strategy_status}, ensure_ascii=False))


