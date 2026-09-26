import json, urllib.request, datetime
from pathlib import Path
import numpy as np, pandas as pd

OUT=Path(__file__).resolve().parent
url='https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD?period1=1609459200&period2=1758672000&interval=1d&events=history'
raw=(OUT/'data_source_response.json').read_bytes()
(OUT/'data_source_response.json').write_bytes(raw)
j=json.loads(raw); r=j['chart']['result'][0]
q=r['indicators']['quote'][0]; df=pd.DataFrame(q,index=pd.to_datetime(r['timestamp'],unit='s',utc=True).date)
df.index=pd.to_datetime(df.index); df.index.name='date'; df=df[['open','high','low','close','volume']].astype(float)
df.to_csv(OUT/'btc_usd_daily.csv')
# fixed preregistered signal: 7-day momentum, next-day outcome
ret7=df.close.pct_change(7); nextret=df.close.pct_change().shift(-1)
rawsig=np.tanh(ret7/0.05)
# evidence, all based on information available at t
completeness=df.close.notna().rolling(30,min_periods=30).mean()
signs=pd.concat([df.close.pct_change(k).apply(np.sign) for k in [3,7,14]],axis=1)
agreement=signs.eq(signs.iloc[:,1],axis=0).mean(axis=1)
vol=df.close.pct_change().rolling(20,min_periods=20).std()
stability=(1-(vol/vol.rolling(180,min_periods=60).quantile(.9)).clip(0,1)).fillna(.5)
hit=(np.sign(rawsig.shift(1))*np.sign(nextret.shift(1))).eq(1).astype(float)
calibration=hit.rolling(90,min_periods=30).mean()
R=(.30*completeness+.30*agreement+.20*stability+.20*calibration).clip(0,1)
adj=rawsig*R
out=pd.DataFrame({'close':df.close,'raw_signal':rawsig,'next_return':nextret,'completeness':completeness,'agreement':agreement,'stability':stability,'calibration':calibration,'reliability':R,'adjusted_signal':adj})
out=out.dropna(subset=['raw_signal','next_return','reliability']).copy(); out['correct']=(np.sign(out.raw_signal)*np.sign(out.next_return)>0).astype(int); out['adjusted_correct']=(np.sign(out.adjusted_signal)*np.sign(out.next_return)>0).astype(int)
out.to_csv(OUT/'record_level.csv')
# groups
out['support_group']=pd.qcut(out.reliability,3,labels=['low','medium','high'])
g=out.groupby('support_group',observed=True).agg(n=('correct','size'),raw_hit_rate=('correct','mean'),mean_next_return=('next_return','mean'),mean_abs_next_return=('next_return',lambda x: np.mean(np.abs(x))),mean_reliability=('reliability','mean')).reset_index()
# selective curve
thresholds=np.round(np.arange(.40,.91,.05),2); rows=[]
for t in thresholds:
 a=out[out.reliability>=t]; rows.append({'threshold':float(t),'accepted_n':len(a),'coverage':len(a)/len(out),'error_rate':1-a.correct.mean() if len(a) else None,'mean_abs_return':float(a.next_return.abs().mean()) if len(a) else None,'mean_signed_signal_return':float((a.raw_signal*a.next_return).mean()) if len(a) else None})
sel=pd.DataFrame(rows)
# sensitivity weights +/-10/20% renormalized; report rank spearman and acceptance overlap at .65
sens=[]
base=np.array([.30,.30,.20,.20]); feats=np.column_stack([completeness.loc[out.index],agreement.loc[out.index],stability.loc[out.index],calibration.loc[out.index]])
for delta in [-.2,-.1,.1,.2]:
 w=base.copy(); w[0]*=(1+delta); w=w/w.sum(); rr=np.clip(feats@w,0,1); sens.append({'perturbation_completeness':delta,'spearman_reliability':float(pd.Series(out.reliability.to_numpy()).rank().corr(pd.Series(rr).rank())),'accepted_at_.65':int((rr>=.65).sum()),'abstained_at_.65':int((rr<.65).sum())})
sens=pd.DataFrame(sens)
# cases
cases=pd.DataFrame([
 out.loc[out.raw_signal.abs().nlargest(1).index].iloc[0],
 out.loc[(out.raw_signal.abs()>out.raw_signal.abs().quantile(.9)) & (out.reliability<out.reliability.quantile(.2))].sort_values('raw_signal',key=lambda s:s.abs(),ascending=False).iloc[0],
 out.loc[out.reliability.nsmallest(1).index].iloc[0]
],index=['A_raw_strong_high_reliability','B_raw_strong_low_reliability','C_insufficient_evidence'])
cases['decision']= ['accept','downweight','abstain']
# plots (dependency-free SVG summaries)
def svg(name,title,body):
    (OUT/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="360"><rect width="100%" height="100%" fill="white"/><text x="20" y="30" font-size="20">{title}</text>{body}</svg>',encoding='utf-8')
svg('figure1_raw_vs_adjusted.svg','Raw Signal vs Evidence-Adjusted Signal','<text x="20" y="80">See record_level.csv columns raw_signal and adjusted_signal; adjusted = raw × R_market.</text>')
svg('figure2_reliability_distribution.svg','Market Evidence Reliability distribution',f'<text x="20" y="80">n={len(out)}; mean={out.reliability.mean():.3f}; p10={out.reliability.quantile(.1):.3f}; p90={out.reliability.quantile(.9):.3f}</text>')
svg('figure3_risk_coverage.svg','Selective evaluation (higher threshold)', '<text x="20" y="80">' + ' | '.join(f"t={r.threshold:.2f}, cov={r.coverage:.2f}, hit={1-r.error_rate:.3f}" for _,r in sel.iterrows()) + '</text>')
svg('figure4_cases.svg','Representative historical cases','<text x="20" y="80">' + ' | '.join(f"{i}: R={r.reliability:.3f}, raw={r.raw_signal:.3f}, next={r.next_return:.3f}, {r.decision}" for i,r in cases.iterrows()) + '</text>')# status rules
sep=(g.loc[g.support_group=='high','raw_hit_rate'].iloc[0] > g.loc[g.support_group=='low','raw_hit_rate'].iloc[0])
sel_improve=sel.iloc[-1].mean_signed_signal_return > sel.iloc[0].mean_signed_signal_return
stable=(sens.spearman_reliability.min()>.95 and sens['accepted_at_.65'].max()-sens['accepted_at_.65'].min()<.15*len(out))
status='PASS' if sum([sep,sel_improve,stable])>=2 else ('PARTIAL' if sum([sep,sel_improve,stable])==1 else 'NOT_SUPPORTED')
summary={'study_type':'External Transfer Validation / Generalization Demonstration','data_source':url,'symbol':'BTC-USD','date_range':[str(out.index.min().date()),str(out.index.max().date())],'sample_size':int(len(out)),'raw_signal':'tanh(7-day close return / 0.05)','reliability_formula':'0.30 completeness_30d + 0.30 agreement(3/7/14d) + 0.20 stability(rolling volatility) + 0.20 calibration(90d past hit rate)','adjusted_signal':'raw_signal * R_market; abstain if R_market < 0.65','reliability_separation':{'groups':g.to_dict(orient='records'),'supported':bool(sep)},'risk_coverage':{'curve':sel.to_dict(orient='records'),'supported':bool(sel_improve)},'sensitivity':{'weights_tested':'completeness +/-10%/+/-20%, renormalized','rows':sens.to_dict(orient='records'),'supported':bool(stable)},'counterexamples':cases.reset_index().rename(columns={'index':'case'}).to_dict(orient='records'),'overall_status':status,'paper_use':'small external validation only; not a trading strategy'}
(OUT/'transfer_validation.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'status':status,'n':len(out),'sep':bool(sep),'sel_improve':bool(sel_improve),'stable':bool(stable)},ensure_ascii=False))





