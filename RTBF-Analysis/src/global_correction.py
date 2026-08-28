"""
Step 10: one global multiple-comparison correction across every PRIMARY/omnibus
hypothesis test run anywhere in this analysis (stats.py, verify.py, mcnemar.py,
willingness.py, calibration_stats.py, moderators.py).

Each script already Holm-corrects WITHIN its own family (e.g. the 3 scales in
stats.py steps 3-4, the 7 methods in mcnemar.py). This script asks a stricter
question: if every one of these ~100 tests is treated as ONE family — as they
arguably are, since they're all run on the same n~177 dataset in service of
the same overall project — which results still hold?

Only primary/omnibus tests are included. Post-hoc pairwise tests (Dunn's,
etc.) are conditional follow-ups on an already-significant omnibus test, not
independent primary hypotheses — including them here would double-count the
same underlying comparison and isn't standard practice.

Correction: both Holm (family-wise error rate) and Benjamini-Hochberg FDR are
reported. Holm is what every individual script uses; BH-FDR is the more
common choice for a large, mostly-exploratory battery like this one, since
Holm's FWER control gets extremely conservative once n~100 tests are pooled.
"""

import pandas as pd
from statsmodels.stats.multitest import multipletests
from src.screen import get_bases
from src.reporting import save_report

from src.stats import (
    between_method, between_scenario_likert, between_scenario_binary,
    method_switching, SCEN as STATS_SCEN,
)
from src.willingness import scenario_shift, willingness_by_method
from src.verify import test_family, EXP_OPTS, VER_OPTS, SCEN as VERIFY_SCEN
from src.mcnemar import per_method_shift
from src.calibration import SCEN as CALIB_SCEN
from src.calibration_stats import confidence_trend, used_vs_ideal_mcnemar
from src.moderators import (
    continuous_outcomes, test_moderator_continuous, test_moderator_method, MODERATORS,
)


def collect_all_pvals(bases):
    paired = bases["paired"]
    all_pvals = []   # [(family, label, p_raw)]

    _throwaway = []
    all_pvals += [("stats.between_method", lbl, p) for lbl, p in between_method(bases, _throwaway)]
    all_pvals += [("stats.between_scenario_likert", lbl, p) for lbl, p in between_scenario_likert(paired, _throwaway)]
    all_pvals += [("stats.between_scenario_binary", lbl, p) for lbl, p in between_scenario_binary(paired, _throwaway)]
    all_pvals += [("stats.method_switching", lbl, p) for lbl, p in method_switching(paired, _throwaway)]

    _, p1 = scenario_shift(paired)
    all_pvals += [("willingness.scenario_shift", lbl, p) for lbl, p in p1]
    _, p2 = willingness_by_method(bases)
    all_pvals += [("willingness.by_method", lbl, p) for lbl, p in p2]

    for scen, (mcol, qexp, qver) in VERIFY_SCEN.items():
        df = bases[scen]
        exp_out = test_family(df, mcol, qexp, EXP_OPTS)
        for _, row in exp_out.iterrows():
            all_pvals.append(("verify.expectation", f"[{scen}] {row['option']}", row["p_raw"]))
        ver_out = test_family(df, mcol, qver, VER_OPTS)
        for _, row in ver_out.iterrows():
            all_pvals.append(("verify.verification", f"[{scen}] {row['option']}", row["p_raw"]))

    mc_out = per_method_shift(paired)
    for _, row in mc_out.iterrows():
        all_pvals.append(("mcnemar.per_method_shift", row["method"], row["p_raw"]))

    for scen, (conf_col, verify_prefix, used_col, ideal_prefix) in CALIB_SCEN.items():
        df = bases[scen]
        _, res = confidence_trend(df, conf_col, verify_prefix)
        all_pvals.append(("calibration.confidence_trend", f"[{scen}]", res.pvalue))
        cal_out = used_vs_ideal_mcnemar(df, used_col, ideal_prefix)
        for _, row in cal_out.iterrows():
            all_pvals.append(("calibration.used_vs_ideal", f"[{scen}] {row['method']}", row["p_raw"]))

    for scen in STATS_SCEN:
        _, method_col = STATS_SCEN[scen]
        df = bases[scen]
        outcomes = continuous_outcomes(df, scen)
        for mod_name, (group_col, exclude_val) in MODERATORS.items():
            mod_out, kept, dropped = test_moderator_continuous(df, group_col, exclude_val, outcomes)
            for _, row in mod_out.iterrows():
                all_pvals.append(("moderators.continuous", f"[{scen}] {mod_name}->{row['outcome']}", row["p_raw"]))
            test, p, v, kept_g, kept_m = test_moderator_method(df, group_col, exclude_val, method_col)
            all_pvals.append(("moderators.method_choice", f"[{scen}] {mod_name}->method", p))

    return all_pvals


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    all_pvals = collect_all_pvals(bases)

    df = pd.DataFrame(all_pvals, columns=["family", "label", "p_raw"]).dropna(subset=["p_raw"])
    df["p_raw"] = df["p_raw"].astype(float)

    df["p_holm_global"] = multipletests(df["p_raw"], method="holm")[1]
    df["p_fdr_global"] = multipletests(df["p_raw"], method="fdr_bh")[1]
    df["sig_raw"] = df["p_raw"] < 0.05
    df["sig_holm_global"] = df["p_holm_global"] < 0.05
    df["sig_fdr_global"] = df["p_fdr_global"] < 0.05
    df = df.sort_values("p_raw").reset_index(drop=True)

    lines = [f"=== Global correction across {len(df)} primary/omnibus tests ==="]
    lines.append(f"raw p<.05        : {int(df['sig_raw'].sum())} / {len(df)}")
    lines.append(f"Holm-global p<.05: {int(df['sig_holm_global'].sum())} / {len(df)}")
    lines.append(f"BH-FDR q<.05     : {int(df['sig_fdr_global'].sum())} / {len(df)}")

    lines.append("\n-- tests significant at raw p<.05 (sorted by p_raw) --")
    sig_raw = df[df["sig_raw"]][["family", "label", "p_raw", "p_holm_global", "p_fdr_global",
                                  "sig_holm_global", "sig_fdr_global"]]
    lines.append(sig_raw.to_string(index=False))

    lines.append("\n-- of those, still significant under BH-FDR global correction --")
    survivors = df[df["sig_fdr_global"]][["family", "label", "p_raw", "p_fdr_global"]]
    lines.append(survivors.to_string(index=False) if len(survivors) else "(none)")

    lines.append("\n-- of those, still significant under Holm global correction (strictest) --")
    holm_survivors = df[df["sig_holm_global"]][["family", "label", "p_raw", "p_holm_global"]]
    lines.append(holm_survivors.to_string(index=False) if len(holm_survivors) else "(none)")

    for line in lines:
        print(line)

    report_path = save_report("global_correction", lines)
    print(f"\nreport saved -> {report_path}")

    full_path = "outputs/tables/global_correction_all_tests.csv"
    df.to_csv(full_path, index=False)
    print(f"full table saved -> {full_path}")
