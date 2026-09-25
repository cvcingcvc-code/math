"""Reliability statistics for the annotation gate.

Implements Krippendorff's alpha (nominal / ordinal / interval) and Cohen's kappa
(nominal / quadratic weighted) without external dependencies, so the reproduction
package stays runnable offline.

Krippendorff alpha is computed from coincidence matrices:
    o_ck = sum_u pairs_u(c,k) / (m_u - 1)
    D_o  = sum_ck o_ck * delta2_ck
    D_e  = sum_ck n_c * n_k * delta2_ck / (N - 1)
    alpha = 1 - D_o / D_e

delta2:
    nominal : 0 if c == k else 1
    interval: (v_c - v_k)^2
    ordinal : ( sum_{g=lo..hi} n_g - (n_c + n_k) / 2 )^2

Run `python src/reliability.py` for hand-verified self-tests.
"""
from __future__ import annotations

import numpy as np

MISSING = {"", "nan", "none", "na", "n/a"}


def _clean(values, missing=MISSING):
    return [v for v in values if str(v).strip().lower() not in missing]


def _coincidence(units, order):
    """Coincidence matrix o_ck and marginals n_c over pairable units."""
    idx = {v: i for i, v in enumerate(order)}
    K = len(order)
    o = np.zeros((K, K), dtype=float)
    for u in units:
        vals = [idx[v] for v in u]
        m = len(vals)
        if m < 2:
            continue
        cnt = np.zeros(K, dtype=float)
        for c in vals:
            cnt[c] += 1
        for c in range(K):
            if cnt[c] == 0:
                continue
            for k in range(K):
                pairs = cnt[c] * (cnt[c] - 1) if c == k else cnt[c] * cnt[k]
                if pairs:
                    o[c, k] += pairs / (m - 1)
    n = o.sum(axis=1)
    return o, n


def _delta2(kind, order, n):
    K = len(order)
    d = np.zeros((K, K), dtype=float)
    if kind == "nominal":
        for c in range(K):
            for k in range(K):
                d[c, k] = 0.0 if c == k else 1.0
    elif kind == "interval":
        v = np.asarray(order, dtype=float)
        for c in range(K):
            for k in range(K):
                d[c, k] = (v[c] - v[k]) ** 2
    elif kind == "ordinal":
        for c in range(K):
            for k in range(K):
                lo, hi = min(c, k), max(c, k)
                d[c, k] = (n[lo:hi + 1].sum() - (n[c] + n[k]) / 2.0) ** 2
    else:
        raise ValueError(f"unknown metric: {kind}")
    return d


def krippendorff_alpha(units, level="nominal", order=None):
    """units: iterable of per-unit value lists (coders x unit orientation free)."""
    cleaned = [_clean(u) for u in units]
    cleaned = [u for u in cleaned if len(u) >= 2]
    if not cleaned:
        return float("nan")
    if order is None:
        seen = []
        for u in cleaned:
            for v in u:
                if v not in seen:
                    seen.append(v)
        order = sorted(seen)
    order = list(order)
    o, n = _coincidence(cleaned, order)
    N = n.sum()
    if N <= 1:
        return float("nan")
    d = _delta2(level, order, n)
    D_o = float((o * d).sum())
    D_e = float((np.outer(n, n) * d).sum() / (N - 1))
    if D_e == 0:
        return 1.0 if D_o == 0 else float("nan")
    return 1.0 - D_o / D_e


def cohen_kappa(a, b, labels=None):
    a, b = list(a), list(b)
    keep = [(x, y) for x, y in zip(a, b)
            if str(x).strip().lower() not in MISSING and str(y).strip().lower() not in MISSING]
    if not keep:
        return float("nan")
    a = [x for x, _ in keep]
    b = [y for _, y in keep]
    labels = labels or sorted(set(a) | set(b))
    idx = {v: i for i, v in enumerate(labels)}
    K = len(labels)
    cm = np.zeros((K, K), dtype=float)
    for x, y in zip(a, b):
        cm[idx[x], idx[y]] += 1
    n = cm.sum()
    po = np.trace(cm) / n
    pe = float((cm.sum(axis=0) * cm.sum(axis=1)).sum()) / (n * n)
    return 1.0 - (1.0 - po) / (1.0 - pe) if pe != 1 else float("nan")


def weighted_kappa(a, b, weights="quadratic", order=None):
    """Cohen's weighted kappa with linear/quadratic weights on an ordered scale."""
    a, b = list(a), list(b)
    keep = [(x, y) for x, y in zip(a, b)
            if str(x).strip().lower() not in MISSING and str(y).strip().lower() not in MISSING]
    if not keep:
        return float("nan")
    a = [x for x, _ in keep]
    b = [y for _, y in keep]
    order = list(order or sorted(set(a) | set(b)))
    idx = {v: i for i, v in enumerate(order)}
    K = len(order)
    cm = np.zeros((K, K), dtype=float)
    for x, y in zip(a, b):
        cm[idx[x], idx[y]] += 1
    n = cm.sum()
    i = np.arange(K)[:, None]
    j = np.arange(K)[None, :]
    d = (i - j) ** 2 if weights == "quadratic" else np.abs(i - j)
    d = d / (d.max() if d.max() else 1)
    exp = np.outer(cm.sum(axis=1), cm.sum(axis=0)) / n
    D_o = float((cm * d).sum())
    D_e = float((exp * d).sum())
    return 1.0 - D_o / D_e if D_e != 0 else float("nan")


def agreement_rate(a, b):
    a, b = list(a), list(b)
    keep = [(x, y) for x, y in zip(a, b)
            if str(x).strip().lower() not in MISSING and str(y).strip().lower() not in MISSING]
    if not keep:
        return float("nan")
    return sum(1 for x, y in keep if x == y) / len(keep)


def bootstrap_ci(values_a, values_b, cluster=None, level="nominal", order=None,
                 n_boot=2000, seed=20260925, alpha=0.05):
    """Bootstrap CI for Krippendorff alpha. Cluster-resample units when given.

    Manual V0.1 / validation plan require resampling by student where students
    contribute multiple records, so the student is the resampling unit.
    """
    rng = np.random.default_rng(seed)
    pairs = list(zip(values_a, values_b))
    n = len(pairs)
    if n == 0:
        return (float("nan"), float("nan"))
    groups: dict[str, list[int]] = {}
    keys = list(cluster) if cluster is not None else [str(i) for i in range(n)]
    for i, k in enumerate(keys):
        groups.setdefault(k, []).append(i)
    gkeys = list(groups)
    stats = []
    for _ in range(n_boot):
        picked = rng.choice(len(gkeys), size=len(gkeys), replace=True)
        idx = [i for p in picked for i in groups[gkeys[p]]]
        ua = [values_a[i] for i in idx]
        ub = [values_b[i] for i in idx]
        s = krippendorff_alpha(list(zip(ua, ub)), level=level, order=order)
        if not np.isnan(s):
            stats.append(s)
    if not stats:
        return (float("nan"), float("nan"))
    lo, hi = np.percentile(stats, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return (float(lo), float(hi))


# --------------------------------------------------------------------------
# self-tests: values below are hand-computed, not taken from any library.
# --------------------------------------------------------------------------
def _selftest() -> int:
    fails = 0
    def close(name, got, want, tol=1e-4):
        nonlocal fails
        ok = abs(got - want) < tol
        if not ok:
            fails += 1
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: got={got:.6f} want={want:.6f}")

    # hand-computed case: 4 units x 2 coders -> (1,2),(2,3),(3,3) style scale 1..3
    units = [(1, 2), (2, 3), (3, 3)]
    close("nominal alpha", krippendorff_alpha(units, "nominal"), 0.090909)
    close("ordinal alpha", krippendorff_alpha(units, "ordinal"), 0.527778)
    close("interval alpha", krippendorff_alpha(units, "interval"), 0.5)
    close("perfect agreement -> 1", krippendorff_alpha([(1, 1), (2, 2), (3, 3)], "nominal"), 1.0)

    # hand-computed nominal case with a 2-category scale
    u2 = [("A", "A"), ("A", "B"), ("B", "B"), ("B", "B")]
    close("nominal alpha (A/B)", krippendorff_alpha(u2, "nominal"), 0.533333)

    # ordinal >= nominal when only adjacent categories disagree
    assert krippendorff_alpha(units, "ordinal") > krippendorff_alpha(units, "nominal")
    print("[PASS] ordinal > nominal for adjacent disagreements")

    # cross-check Cohen's kappa against its closed form
    close("cohen kappa (A/B)", cohen_kappa([x for x, _ in u2], [y for _, y in u2]), 0.5)
    close("agreement rate (A/B)", agreement_rate([x for x, _ in u2], [y for _, y in u2]), 0.75)

    # missing values must be dropped, not counted as a category
    close("missing dropped", krippendorff_alpha([(1, 1), (2, 2), ("", 2)], "nominal"), 1.0)

    print(f"\nself-test failures: {fails}")
    return fails


if __name__ == "__main__":
    raise SystemExit(1 if _selftest() else 0)