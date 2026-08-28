"""
The comparison deliverable: does the scipy-only reimplementation correlate
with the original ("manual") src/ pipeline?

Loads bases once, pulls the same-shaped (family, label, p_raw) list from both
src.global_correction.collect_all_pvals (old) and
scipy_analysis.global_correction.collect_all_pvals (new), joins on
(family, label), and reports:
  - Pearson r and Spearman rho across all matched (p_old, p_new) pairs --
    the literal "do the results correlate" number.
  - n exact / near-exact matches, n significance flips (p<.05 disagreement).

Expected pattern (see module docstrings for why): tests that were already
scipy-only in src/ (Kruskal-Wallis, Mann-Whitney, Shapiro, paired-t) should
match EXACTLY. Chi-square/Fisher rows will show small (<0.02) drift because
scipy's own r x c fisher_exact is internally Monte-Carlo-randomized with no
exposed seed -- that noise exists even between two runs of the SAME code, not
just between the two pipelines. McNemar, Stuart-Maxwell, the ordinal trend
test, Wilcoxon's effect size, and Cronbach's alpha are hand-reimplemented
against a different library's implementation in src/, so these are the
genuinely informative comparisons.
"""

import pandas as pd
from scipy.stats import pearsonr, spearmanr

from src.screen import get_bases
from src.global_correction import collect_all_pvals as collect_old
from scipy_analysis.global_correction import collect_all_pvals as collect_new

from .reporting import save_report

FISHER_NOISE_FAMILIES = {"verify.expectation", "verify.verification", "moderators.method_choice"}


def build_comparison(bases):
    old = pd.DataFrame(collect_old(bases), columns=["family", "label", "p_old"])
    new = pd.DataFrame(collect_new(bases), columns=["family", "label", "p_new"])

    merged = old.merge(new, on=["family", "label"], how="outer", indicator=True)
    merged["p_old"] = pd.to_numeric(merged["p_old"], errors="coerce")
    merged["p_new"] = pd.to_numeric(merged["p_new"], errors="coerce")
    merged["p_diff"] = (merged["p_new"] - merged["p_old"]).abs()
    merged["sig_old"] = merged["p_old"] < 0.05
    merged["sig_new"] = merged["p_new"] < 0.05
    merged["sig_flip"] = merged["sig_old"] != merged["sig_new"]
    merged["known_fisher_noise"] = merged["family"].isin(FISHER_NOISE_FAMILIES)
    return merged.sort_values(["family", "label"]).reset_index(drop=True)


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    merged = build_comparison(bases)

    both = merged[merged["_merge"] == "both"].dropna(subset=["p_old", "p_new"])
    unmatched = merged[merged["_merge"] != "both"]

    r, r_p = pearsonr(both["p_old"], both["p_new"])
    rho, rho_p = spearmanr(both["p_old"], both["p_new"])

    exact = both[both["p_diff"] < 1e-9]
    near = both[(both["p_diff"] >= 1e-9) & (both["p_diff"] < 0.02)]
    drifted = both[both["p_diff"] >= 0.02]
    flips = both[both["sig_flip"]]

    lines = [f"=== scipy_analysis vs src (manual) pipeline: {len(both)} tests compared ==="]
    lines.append(f"Pearson  r   = {r:.6f}  (p={r_p:.2e})")
    lines.append(f"Spearman rho = {rho:.6f}  (p={rho_p:.2e})")
    lines.append(f"\nexact match (diff < 1e-9)      : {len(exact)} / {len(both)}")
    lines.append(f"near match  (1e-9 <= diff < .02): {len(near)} / {len(both)}")
    lines.append(f"drifted     (diff >= .02)       : {len(drifted)} / {len(both)}")
    lines.append(f"significance flips (p<.05 disagreement): {len(flips)} / {len(both)}")

    if len(unmatched):
        lines.append(f"\n-- {len(unmatched)} label(s) present in only one pipeline (fix before trusting the totals) --")
        lines.append(unmatched[["family", "label", "_merge"]].to_string(index=False))

    if len(flips):
        lines.append("\n-- significance flips --")
        lines.append(flips[["family", "label", "p_old", "p_new"]].to_string(index=False))
    else:
        lines.append("\n-- no significance flips --")

    if len(drifted):
        lines.append("\n-- drifted rows (diff >= .02) --")
        lines.append(drifted[["family", "label", "p_old", "p_new", "p_diff", "known_fisher_noise"]]
                      .to_string(index=False))

    for line in lines:
        print(line)

    report_path = save_report("compare", lines)
    print(f"\nreport saved -> {report_path}")

    out_path = "scipy_analysis/outputs/tables/compare_pvals.csv"
    merged.to_csv(out_path, index=False)
    print(f"full comparison table saved -> {out_path}")
