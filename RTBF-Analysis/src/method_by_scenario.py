"""
Method x scenario interaction for the three scales (protection, effort, benefit loss).

Question (Yao Li, 2026-10-07 table): does the shift from the less sensitive
scenario (LS) to the more sensitive one (MS) differ across the four most chosen
data deletion methods? The paper's between-method GEE (src/pooled_gee.py) uses
scenario as a covariate, so it assumes the LS to MS shift is the same for every
method. This script tests that assumption and reports each method's own shift.

Data and unit of analysis: identical to src/pooled_gee.py (one row per
participant-scenario response, four methods with at least 14 distinct
participants, clustered on participant).

Tests (per scale):
  1. Gaussian GEE, outcome ~ method * scenario, clustered on participant,
     independence working correlation with robust SEs (same primary setup as
     pooled_gee). Joint Wald chi-square on the method:scenario terms (df = 3).
     Holm across the 3 scales (the same family as the between-method test).
  2. Within-method scenario difference (MS minus LS) from contrasts in that
     model, Holm across the 4 methods, separately for each scale (three
     families of four).
Robustness (per scale):
  3. Exchangeable working correlation, joint Wald on the interaction.
  4. Aligned rank transform (Wobbrock et al., 2011) for the interaction: align
     the outcome for the interaction effect, rank it, and refit the same GEE on
     the ranks. ARTool is an R package, so the alignment is implemented here;
     it uses the participant-clustered GEE in place of the mixed model ARTool
     fits, so read it as a nonparametric check, not as ARTool output.

No confidence intervals are reported (supervisor decision, 2026-10-07); the
standard error of each difference is shown instead.
"""

import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.multitest import multipletests
from statsmodels.tools.sm_exceptions import ConvergenceWarning

from src.pooled_gee import (
    N_FLOOR, SURVEY_XLSX, TABLES_DIR, _model_frame, build_observation_frame,
    method_wald, qualifying_methods,
)
from src.reporting import save_report
from src.screen import get_bases
from src.stats import SCALES

ALPHA = 0.05
FORMULA = "{y} ~ C(method) * C(scenario)"


def fit_interaction(data: pd.DataFrame, outcome: str, exchangeable: bool = False):
    """GEE with the method x scenario interaction; returns (result, converged)."""
    cov_struct = sm.cov_struct.Exchangeable() if exchangeable else sm.cov_struct.Independence()
    model = smf.gee(FORMULA.format(y=outcome), groups="pid", data=data,
                    family=sm.families.Gaussian(), cov_struct=cov_struct)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = model.fit()
    return result, not any(issubclass(w.category, ConvergenceWarning) for w in caught)


def interaction_wald(result) -> tuple[float, int, float]:
    """Joint Wald chi-square on every method:scenario coefficient."""
    names = list(result.params.index)
    idx = [i for i, n in enumerate(names) if ":" in n]
    restriction = np.zeros((len(idx), len(names)))
    restriction[np.arange(len(idx)), idx] = 1.0
    wald = result.wald_test(restriction, scalar=True, use_f=False)
    return float(wald.statistic), len(idx), float(wald.pvalue)


def aligned_ranks(data: pd.DataFrame, outcome: str) -> pd.Series:
    """Aligned rank transform of `outcome` for the method x scenario interaction.

    aligned = residual (outcome - cell mean) + interaction effect
              (cell mean - method mean - scenario mean + grand mean); then ranked.
    """
    y = data[outcome]
    cell = data.groupby(["method", "scenario"], observed=True)[outcome].transform("mean")
    row = data.groupby("method", observed=True)[outcome].transform("mean")
    col = data.groupby("scenario", observed=True)[outcome].transform("mean")
    aligned = (y - cell) + (cell - row - col + y.mean())
    return aligned.rank()


def scenario_shift_by_method(result, methods: list[str]) -> pd.DataFrame:
    """MS minus LS within each method, from contrasts in the interaction model."""
    names = list(result.params.index)
    rows = []
    for method in methods:
        contrast = np.zeros(len(names))
        contrast[names.index("C(scenario)[T.more]")] = 1.0
        key = f"C(method)[T.{method}]:C(scenario)[T.more]"
        if key in names:                      # reference method has no interaction term
            contrast[names.index(key)] = 1.0
        test = result.t_test(contrast.reshape(1, -1))
        rows.append({"method": method, "diff_MS_minus_LS": float(np.ravel(test.effect)[0]),
                     "se": float(np.ravel(test.sd)[0]), "p_raw": float(np.ravel(test.pvalue)[0])})
    out = pd.DataFrame(rows)
    out["p_holm"] = multipletests(out["p_raw"], method="holm")[1]
    out["sig"] = np.where(out["p_holm"] < ALPHA, "*", "")
    return out


def cell_table(data: pd.DataFrame, scale: str) -> pd.DataFrame:
    """Mean per method in LS, MS and Pooled with response and participant counts."""
    rows = []
    for method, g in data.groupby("method", observed=True):
        ls, ms = g[g["scenario"] == "less"], g[g["scenario"] == "more"]
        rows.append({"method": method, "Pooled": g[scale].mean(), "LS": ls[scale].mean(),
                     "MS": ms[scale].mean(), "MS-LS": ms[scale].mean() - ls[scale].mean(),
                     "n_LS": len(ls), "n_MS": len(ms), "people": g["pid"].nunique()})
    return pd.DataFrame(rows)


def _fmt(df: pd.DataFrame) -> str:
    return df.round(4).to_string(index=False)


def main() -> None:
    bases = get_bases(path=SURVEY_XLSX, verbose=False)
    obs = build_observation_frame(bases["paired"])
    methods = qualifying_methods(obs)
    data = _model_frame(obs, methods)

    lines = [
        "=== Method x scenario interaction on protection, effort and benefit loss ===",
        f"{len(data)} responses from {data['pid'].nunique()} participants; methods with >= {N_FLOOR} "
        "distinct participants: " + "; ".join(f"{m} ({data[data['method'] == m]['pid'].nunique()})" for m in methods),
        "Model: scale ~ method * scenario, Gaussian GEE clustered on participant, independence working "
        "correlation, robust SEs. Joint Wald chi-square on the 3 interaction terms, Holm across the 3 scales.",
        "Reference levels: first method listed above, scenario = less sensitive (LS).",
    ]

    # Reproduction check: the paper's between-method test (method + scenario, no interaction).
    lines += ["", "-" * 70, "CHECK: paper's between-method test (no interaction) reproduces", "-" * 70]
    for scale in SCALES:
        base = smf.gee(f"{scale} ~ C(method) + C(scenario)", groups="pid", data=data,
                       family=sm.families.Gaussian(), cov_struct=sm.cov_struct.Independence()).fit()
        chi2, df, p = method_wald(base)
        lines.append(f"{scale}: method Wald chi2({df}) = {chi2:.2f}, p = {p:.4f}")

    summary = []
    for scale in SCALES:
        res, converged = fit_interaction(data, scale)
        chi2, df, p = interaction_wald(res)
        exch, exch_ok = fit_interaction(data, scale, exchangeable=True)
        try:
            chi2_e, _, p_e = interaction_wald(exch)
        except (np.linalg.LinAlgError, ValueError):
            chi2_e, p_e = np.nan, np.nan
        art = data.assign(**{f"{scale}_art": aligned_ranks(data, scale)})
        art_res, art_ok = fit_interaction(art, f"{scale}_art")
        chi2_a, _, p_a = interaction_wald(art_res)
        summary.append({"scale": scale, "chi2": chi2, "df": df, "p_raw": p,
                        "p_exch": p_e, "p_art": p_a,
                        "note": "" if converged and exch_ok and art_ok else "a GEE did not converge"})

        shift = scenario_shift_by_method(res, methods)
        lines += ["", "=" * 70, f"{scale.upper()}", "=" * 70,
                  "Means by method (LS, MS, Pooled) and responses per cell:", _fmt(cell_table(data, scale)),
                  "", "MS minus LS within each method (GEE contrasts from the interaction model, "
                  "Holm across the 4 methods):", _fmt(shift)]
        shift.assign(scale=scale).to_csv(TABLES_DIR / f"method_by_scenario_shift_{scale}.csv", index=False)

    tests = pd.DataFrame(summary)
    tests["p_holm"] = multipletests(tests["p_raw"], method="holm")[1]
    tests["sig"] = np.where(tests["p_holm"] < ALPHA, "*", "")
    lines += ["", "=" * 70, "INTERACTION TESTS (joint Wald, df = 3), Holm across the 3 scales", "=" * 70, _fmt(tests),
              "", "p_exch = exchangeable working correlation; p_art = aligned rank transform "
              "(GEE on ranks). Both are robustness checks and are not Holm-adjusted."]

    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    tests.to_csv(TABLES_DIR / "method_by_scenario_tests.csv", index=False)
    lines += ["", f"saved -> {TABLES_DIR}/method_by_scenario_*.csv"]
    print("\n".join(lines))
    print(f"\nreport saved -> {save_report('method_by_scenario', lines)}")


if __name__ == "__main__":
    main()
