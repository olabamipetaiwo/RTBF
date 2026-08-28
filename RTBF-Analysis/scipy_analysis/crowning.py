"""
Statistically identify the most protective / least-effort / lowest-
benefit-loss deletion method. Kruskal-Wallis (n>=14 floor) per scale -> if
significant, Dunn's post-hoc + Holm (dunn_test, already Holm-corrected
internally) -> crowning synthesis per tasks.md's rule: a method is CROWNED
only if it (1) has the best point estimate (mean, matching src.methods.py's
convention) AND (2) significantly beats EVERY other kept method in the
post-hoc. Partial wins are reported honestly, never forced into a single
winner. ns omnibus -> "no method is statistically distinguishable."

Two scopes:
  (a) pooled -- scipy_analysis.pooling.pooled_method_scores(bases) (task 2's
      dedup logic, n=239). NEW omnibus tests -- these 3 feed the global
      p-value registry.
  (b) per-scenario -- less, more. DUPLICATES stats.between_method's KW+Dunn
      computation (deterministic, must match stats.md exactly) because
      between_method doesn't expose the full pairwise matrix or point
      estimates externally. NOT re-registered globally -- already present
      under "stats.between_method".
"""

from scipy import stats as spstats

from src.screen import get_bases
from src.stats import SCALES, scale_score, SCEN, N_FLOOR, eps2, rank_biserial_indep

from .reporting import save_report
from .dunn import dunn_test
from .pooling import pooled_method_scores

DIRECTION = {"protection": "high", "effort": "low", "benefit_loss": "low"}
LABEL = {"protection": "most protective", "effort": "least effort", "benefit_loss": "lowest benefit loss"}


def crown_scale(long_df, method_col, scale_col, direction, n_floor=N_FLOOR):
    counts = long_df[method_col].value_counts()
    kept = counts[counts >= n_floor].index.tolist()
    sub = long_df[long_df[method_col].isin(kept)][[method_col, scale_col]].dropna()
    groups = {m: sub.loc[sub[method_col] == m, scale_col].values for m in kept}
    H, p_omni = spstats.kruskal(*groups.values())
    means = {m: float(sub.loc[sub[method_col] == m, scale_col].mean()) for m in kept}
    medians = {m: float(sub.loc[sub[method_col] == m, scale_col].median()) for m in kept}
    best = max(means, key=means.get) if direction == "high" else min(means, key=means.get)

    result = {"kept": kept, "n_kept": len(kept), "H": H, "p_omnibus": p_omni,
              "eps2": eps2(H, len(sub), len(kept)), "means": means,
              "medians": medians, "best": best}

    if p_omni >= 0.05:
        result["beats"], result["not_distinguishable"], result["verdict"] = [], [], "ns"
        return result

    dunn = dunn_test(sub, val_col=scale_col, group_col=method_col)
    others = [m for m in kept if m != best]
    beats, nd = [], []
    for m in others:
        p_holm = dunn.loc[best, m]
        r = rank_biserial_indep(groups[best], groups[m])
        (beats if p_holm < 0.05 else nd).append((m, p_holm, r))
    result.update(dunn=dunn, beats=beats, not_distinguishable=nd,
                   verdict="CROWNED" if not nd else "PARTIAL")
    return result


def _scored(df, base, scale):
    q, k = SCALES[scale]
    out = df.copy()
    out["_s"] = scale_score(df, base, q, k)
    return out


def _report_scale(lines, scope, scale, direction, r):
    arrow = "higher=better" if direction == "high" else "lower=better"
    lines.append(f"\n[{scope} | {scale}] ({arrow})  KW H={r['H']:.2f} p={r['p_omnibus']:.4f} "
                  f"eps2={r['eps2']}  n_methods={r['n_kept']}")
    ordered = sorted(r["means"].items(), key=lambda kv: kv[1], reverse=(direction == "high"))
    lines.append("    means: " + ", ".join(f"{m[:20]}={v:.3f}" for m, v in ordered))
    if r["verdict"] == "ns":
        lines.append("    -> ns: no method is statistically distinguishable from the others")
        return
    best_short = r["best"][:30]
    if r["verdict"] == "CROWNED":
        lines.append(f"    -> CROWNED: '{best_short}' is significantly {LABEL[scale]}, "
                      f"beating all {len(r['beats'])} other kept methods")
    else:
        lines.append(f"    -> PARTIAL: '{best_short}' has the best point estimate but "
                      f"doesn't beat everyone -- not a clean winner")
    for m, p, rr in r["beats"]:
        lines.append(f"       * significantly beats {m[:30]:30} p_holm={p:.4f} r={rr}")
    for m, p, rr in r["not_distinguishable"]:
        lines.append(f"       * NOT distinguishable from {m[:30]:30} p_holm={p:.4f} r={rr}")


def pooled_crowning(bases, lines=None):
    """Scope (a). Returns [(label, p_omnibus)] -- feeds the global registry (NEW tests)."""
    pooled = pooled_method_scores(bases)
    if lines is not None:
        lines.append("\n" + "=" * 70)
        lines.append("SCOPE A -- POOLED (both scenarios, task 2 dedup)")
        lines.append("=" * 70)
    out = []
    for scale, direction in DIRECTION.items():
        r = crown_scale(pooled, "method", scale, direction)
        out.append((f"[pooled] {scale}", r["p_omnibus"]))
        if lines is not None:
            _report_scale(lines, "pooled", scale, direction, r)
    return out


def per_scenario_crowning(bases, lines=None):
    """Scope (b). Report-only -- NOT registered globally (already present under
    stats.between_method)."""
    for scen, (base, mcol) in SCEN.items():
        df = bases[scen]
        df = df[df[mcol] != "Other (Please specify)"]
        if lines is not None:
            lines.append("\n" + "=" * 70)
            lines.append(f"SCOPE B -- {scen.upper()} SCENARIO "
                          "(recomputed for crowning synthesis; omnibus p already in stats.md, not re-registered)")
            lines.append("=" * 70)
        for scale, direction in DIRECTION.items():
            scored = _scored(df, base, scale)
            r = crown_scale(scored, mcol, "_s", direction)
            if lines is not None:
                _report_scale(lines, scen, scale, direction, r)


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    lines = []
    pooled_crowning(bases, lines)
    per_scenario_crowning(bases, lines)

    for line in lines:
        print(line)

    report_path = save_report("crowning", lines)
    print(f"\nreport saved -> {report_path}")
