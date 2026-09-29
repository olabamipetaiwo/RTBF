"""
Pooled (both-scenario) between-method analyses that respect repeated measures.

Why this exists (paper review item N4, 2026-09-23)
--------------------------------------------------
The earlier pooled analyses (scipy_analysis/pooling.py, contingency_table.py,
crowning.py) built one row per "pooled observation" as follows: a respondent
who picked the same method in both scenarios (a stayer) contributed ONE row
whose scores were the average of their two scenario responses; a respondent
who picked different methods (a switcher) contributed one un-averaged row to
each method's group. Three problems, all raised by the reviewer:

  1. Dependence between groups. A switcher sits in two method groups, so the
     groups are not independent samples, which Kruskal-Wallis and Fisher's
     exact test both assume. Deduplicating inside a group does not remove
     that. Holm correction cannot repair it either: it adjusts for how many
     tests were run, not for whether each test's assumptions hold.
  2. Mixed measurement scale. A stayer's averaged 0/0.5/1 indicator (or
     half-step Likert composite) and a switcher's single 0/1 response are
     different kinds of quantity pooled into one column.
  3. Rounding. Fisher/chi-square need integer event counts; summing 0.5s and
     rounding to the nearest integer does not produce the counts the test
     assumes.

Fix: keep every participant-scenario response as its own observation
(176 participants x 2 scenarios = 352 observations, integer 0/1 indicators,
un-averaged scale scores) and test method effects with a Generalized
Estimating Equation (GEE) that clusters on participant. Robust (sandwich)
standard errors give valid inference when observations from the same person
are correlated, including for the switchers who appear under several methods.

Working correlation: INDEPENDENCE (primary), with robust SEs. Method varies
within a person (switchers), so it is a time-varying covariate, and a
non-independence working correlation is only consistent under the "full
covariate conditional mean" assumption (Pepe & Anderson, 1994), which is
implausible here: a participant's method choice in one scenario plausibly
depends on how they rate things in the other. Independence stays consistent
without that assumption, its point estimates equal the observed
scenario-adjusted group means the paper's descriptive tables report, and
the sandwich SEs still account for the within-person dependence. It costs
some efficiency. This was confirmed empirically: an exchangeable-correlation
fit shrank the effort contrasts to about half the raw group differences
(e.g. -0.25 vs -0.45 rating points, single conversation vs clear history),
because with a within-person correlation near 0.8 it leans on the switchers'
within-person contrasts, a different estimand from "how do people who choose
method A rate compared with people who choose method B". The exchangeable
p-value is still reported (`p_exch`) as a sensitivity check, and its
estimated correlation (`rho`) documents how strong the dependence is.

Model (per outcome):  outcome ~ method + scenario, clustered on participant.
  - Binary expectation options: binomial family, logit link (PRIMARY).
    Linear-probability GEE (Gaussian family, identity link) is run as a
    sensitivity check, because logit GEE is not estimable when a method has
    zero (or all) selections of an option, and reported separately.
  - Likert scale composites (protection, effort, benefit loss): Gaussian GEE
    (identity link, so the independence fit is OLS with cluster-robust SEs).
  - `scenario` is a covariate so the omnibus method test is not confounded
    by the scenario-level shift in the outcome. Scenario and presentation
    order are perfectly confounded in this survey (see paper Limitations), so
    the covariate absorbs both.
  - Omnibus test: Wald chi-square on the (k-1) method coefficients.
  - Post-hoc (scales only, and only where the Holm-adjusted omnibus is
    significant, same convention as src/stats.py): all pairwise method
    contrasts, Holm-adjusted within the scale. Reported as adjusted mean
    differences in rating points with 95% CIs.
  - Holm family sizes match the existing convention: 7 expectation options,
    3 scales. An option that cannot be estimated enters its family at p = 1
    (same treatment as verify.py's "skip(0 sel)").

Method inclusion floor: N_FLOOR is applied to DISTINCT PARTICIPANTS per
method, not observations. Counting observations would double-count stayers
and let two very small methods (about 11 respondents each) through, changing
the paper's "four qualifying methods". Distinct participants reproduces the
same four methods the per-scenario analyses use.

Descriptive statistics from this module (percentages, means, medians) are
computed over the same 352 observations, so every pooled number in the paper
comes from one consistent unit of analysis.

For contrast, each result also carries `p_naive`: the same comparison run as
an ordinary chi-square / Kruskal-Wallis over the 352 observations, ignoring
clustering. It is NOT a recommended test; it is reported so the size of the
clustering correction is visible.
"""

import warnings
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.multitest import multipletests
from statsmodels.tools.sm_exceptions import ConvergenceWarning

from src.reporting import save_report
from src.screen import get_bases
from src.stats import SCALES, scale_score
from src.verify import cramers_v

# screen.RAW_FILE still points at data/raw/..., which does not exist in this
# checkout; the Sept 9 export lives under survey/ (same constant as
# src/effect_cis.py).
SURVEY_XLSX = "survey/RTBF_September+9,+2026_14.25.xlsx"
TABLES_DIR = Path("outputs/tables")
OTHER = "Other (Please specify)"
N_FLOOR = 14
ALPHA = 0.05

SCENARIOS = {"less": ("Q4", "Q4.2", "Q4.4"), "more": ("Q5", "Q5.2", "Q5.4")}
EXP_OPTS = {
    1: "permanently deleted", 2: "made invisible / hidden",
    3: "not referenced in current convo", 4: "not referenced in future convo",
    5: "no longer used for training", 6: "not sure what happens", 7: "other",
}
SCALE_DIRECTION = {"protection": "higher = more protective", "effort": "lower = less effort",
                   "benefit_loss": "lower = less benefit lost"}


def build_observation_frame(paired: pd.DataFrame) -> pd.DataFrame:
    """One row per participant-scenario response with a named method.

    Columns: pid, scenario, method, exp_1..exp_7 (0/1), protection, effort,
    benefit_loss. "Other (Please specify)" is filtered per scenario, same
    convention as stats.between_method, so a respondent who answered
    "Other" in only one scenario still contributes the other.
    """
    rows = []
    for scenario, (base, method_col, exp_prefix) in SCENARIOS.items():
        scores = {s: scale_score(paired, base, q, k) for s, (q, k) in SCALES.items()}
        for pid in paired.index:
            method = paired.at[pid, method_col]
            if pd.isna(method) or method == OTHER:
                continue
            row = {"pid": pid, "scenario": scenario, "method": method}
            row |= {f"exp_{j}": int(pd.notna(paired.at[pid, f"{exp_prefix}_{j}"])) for j in EXP_OPTS}
            row |= {s: scores[s].loc[pid] for s in SCALES}
            rows.append(row)
    return pd.DataFrame(rows).sort_values(["pid", "scenario"]).reset_index(drop=True)


def qualifying_methods(obs: pd.DataFrame, n_floor: int = N_FLOOR) -> list[str]:
    """Methods with at least `n_floor` distinct participants, largest first
    (the first one becomes the regression reference level)."""
    people = obs.groupby("method")["pid"].nunique().sort_values(ascending=False)
    return people[people >= n_floor].index.tolist()


def _model_frame(obs: pd.DataFrame, methods: list[str]) -> pd.DataFrame:
    sub = obs[obs["method"].isin(methods)].copy()
    sub["method"] = pd.Categorical(sub["method"], categories=methods)
    return sub.sort_values(["pid", "scenario"])


def fit_gee(data: pd.DataFrame, outcome: str, family: sm.families.Family, exchangeable: bool = False):
    """GEE clustered on participant with robust SEs.

    Independence working correlation by default (see module docstring);
    `exchangeable=True` fits the sensitivity variant. Returns
    (result, estimated_within_person_correlation, converged); the
    correlation is NaN under independence.
    """
    cov_struct = sm.cov_struct.Exchangeable() if exchangeable else sm.cov_struct.Independence()
    model = smf.gee(f"{outcome} ~ C(method) + C(scenario)", groups="pid", data=data,
                    family=family, cov_struct=cov_struct)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = model.fit()
    converged = not any(issubclass(w.category, ConvergenceWarning) for w in caught)
    rho = float(model.cov_struct.dep_params) if exchangeable else np.nan
    return result, rho, converged


def method_p_exchangeable(data: pd.DataFrame, outcome: str, family: sm.families.Family) -> tuple[float, float]:
    """Sensitivity: (Wald p, within-person correlation) under exchangeable
    working correlation; (NaN, NaN) if the fit is not estimable."""
    try:
        result, rho, _ = fit_gee(data, outcome, family, exchangeable=True)
        return method_wald(result)[2], rho
    except (np.linalg.LinAlgError, ValueError):
        return np.nan, np.nan


def method_wald(result) -> tuple[float, int, float]:
    """Wald chi-square test that all method coefficients are zero."""
    idx = [i for i, name in enumerate(result.params.index) if name.startswith("C(method)")]
    restriction = np.zeros((len(idx), len(result.params)))
    restriction[np.arange(len(idx)), idx] = 1.0
    wald = result.wald_test(restriction, scalar=True, use_f=False)
    return float(wald.statistic), len(idx), float(wald.pvalue)


def pairwise_contrasts(result, methods: list[str]) -> pd.DataFrame:
    """All pairwise method contrasts (a - b) from a fitted GEE, Holm-adjusted."""
    names = list(result.params.index)

    def column(method: str) -> int | None:
        key = f"C(method)[T.{method}]"
        return names.index(key) if key in names else None   # None = reference level

    rows = []
    for a, b in combinations(methods, 2):
        contrast = np.zeros(len(names))
        if (i := column(a)) is not None:
            contrast[i] += 1.0
        if (j := column(b)) is not None:
            contrast[j] -= 1.0
        test = result.t_test(contrast.reshape(1, -1))
        low, high = np.ravel(test.conf_int())[:2]
        rows.append({"a": a, "b": b, "diff": float(np.ravel(test.effect)[0]),
                     "ci_low": float(low), "ci_high": float(high),
                     "p_raw": float(np.ravel(test.pvalue)[0])})
    out = pd.DataFrame(rows)
    out["p_holm"] = multipletests(out["p_raw"], method="holm")[1]
    return out


def _holm_with_unestimable(p_raw: pd.Series) -> np.ndarray:
    """Holm over the whole family; inestimable (NaN) options count as p = 1."""
    return multipletests(p_raw.fillna(1.0).to_numpy(), method="holm")[1]


def expectation_family(obs: pd.DataFrame, methods: list[str]) -> pd.DataFrame:
    """Method effect on each of the 7 expectation options (select-all items)."""
    data = _model_frame(obs, methods)
    rows = []
    for j, label in EXP_OPTS.items():
        col = f"exp_{j}"
        per = data.groupby("method", observed=True)[col].agg(["sum", "count"]).reindex(methods)
        table = np.column_stack([per["sum"], per["count"] - per["sum"]]).astype(int)
        n_sel = int(per["sum"].sum())
        zero_cell = bool((per["sum"] == 0).any() or (per["sum"] == per["count"]).any())

        row = {"option": label, "n_selected": n_sel, "chi2": np.nan, "df": np.nan,
               "p_raw": np.nan, "p_exch": np.nan, "p_lpm": np.nan, "p_naive": np.nan,
               "cramers_v": np.nan, "rho": np.nan, "note": ""}
        if n_sel == 0:
            row["note"] = "never selected"
        else:
            row["p_naive"] = stats.chi2_contingency(table, correction=False)[1]
            row["cramers_v"] = round(float(cramers_v(table)), 3)
            # rho is the within-person correlation of the 0/1 indicator, from
            # the exchangeable linear-probability fit (estimable even when the
            # logit is not).
            try:
                lpm, _, _ = fit_gee(data, col, sm.families.Gaussian())
                row["p_lpm"] = method_wald(lpm)[2]
            except (np.linalg.LinAlgError, ValueError):
                pass
            _, row["rho"] = method_p_exchangeable(data, col, sm.families.Gaussian())
            if zero_cell:
                row["note"] = "logit not estimable (a method has 0 or all selections)"
            else:
                res, _, converged = fit_gee(data, col, sm.families.Binomial())
                row["chi2"], row["df"], row["p_raw"] = method_wald(res)
                row["p_exch"], _ = method_p_exchangeable(data, col, sm.families.Binomial())
                row["note"] = "" if converged else "GEE did not converge"
        rows.append(row)
    out = pd.DataFrame(rows)
    out["p_holm"] = _holm_with_unestimable(out["p_raw"])
    out["sig"] = np.where(out["p_holm"] < ALPHA, "*", "")
    return out


def scale_family(obs: pd.DataFrame, methods: list[str]) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    """Method effect on each Likert composite, plus pairwise contrasts where
    the Holm-adjusted omnibus test is significant."""
    data = _model_frame(obs, methods)
    rows, fits = [], {}
    for scale in SCALES:
        res, _, converged = fit_gee(data, scale, sm.families.Gaussian())
        chi2, df, p = method_wald(res)
        p_exch, rho = method_p_exchangeable(data, scale, sm.families.Gaussian())
        groups = [g[scale].to_numpy() for _, g in data.groupby("method", observed=True)]
        rows.append({"scale": scale, "chi2": chi2, "df": df, "p_raw": p, "p_exch": p_exch,
                     "p_naive": stats.kruskal(*groups)[1], "rho": rho,
                     "note": "" if converged else "GEE did not converge"})
        fits[scale] = res
    out = pd.DataFrame(rows)
    out["p_holm"] = multipletests(out["p_raw"], method="holm")[1]
    out["sig"] = np.where(out["p_holm"] < ALPHA, "*", "")
    posthoc = {row.scale: pairwise_contrasts(fits[row.scale], methods)
               for row in out.itertuples() if row.p_holm < ALPHA}
    return out, posthoc


def expectation_pct_table(obs: pd.DataFrame, min_people: int = N_FLOOR) -> pd.DataFrame:
    """Observation-level % of each method's responses selecting each option."""
    rows = []
    for method, g in obs.groupby("method"):
        people = g["pid"].nunique()
        row = {"method": method, "n_obs": len(g), "n_people": people,
               "flag": "" if people >= min_people else f"<{min_people} people"}
        row |= {label: round(100 * g[f"exp_{j}"].mean(), 1) for j, label in EXP_OPTS.items()}
        rows.append(row)
    return pd.DataFrame(rows).sort_values("n_people", ascending=False).reset_index(drop=True)


def scale_desc_table(obs: pd.DataFrame, min_people: int = N_FLOOR) -> pd.DataFrame:
    """Observation-level mean / median / SD of each scale, per method."""
    rows = []
    for method, g in obs.groupby("method"):
        people = g["pid"].nunique()
        row = {"method": method, "n_obs": len(g), "n_people": people,
               "flag": "" if people >= min_people else f"<{min_people} people"}
        for s in SCALES:
            row |= {f"{s}_mean": round(g[s].mean(), 2), f"{s}_median": round(g[s].median(), 2),
                    f"{s}_sd": round(g[s].std(), 2)}
        rows.append(row)
    return pd.DataFrame(rows).sort_values("n_people", ascending=False).reset_index(drop=True)


def _fmt(df: pd.DataFrame) -> str:
    return df.round(4).to_string(index=False)


def main() -> None:
    bases = get_bases(path=SURVEY_XLSX, verbose=False)
    obs = build_observation_frame(bases["paired"])
    methods = qualifying_methods(obs)
    people = obs["pid"].nunique()

    lines = [
        "=== Pooled between-method tests: participant-clustered GEE ===",
        f"{len(obs)} participant-scenario observations from {people} participants "
        f"(paired base n={len(bases['paired'])}; 'Other' filtered per scenario).",
        f"Qualifying methods (>= {N_FLOOR} distinct participants): "
        + "; ".join(f"{m} (ref)" if i == 0 else m for i, m in enumerate(methods)),
        "Model: outcome ~ method + scenario, clustered on participant, independence "
        "working correlation with robust SEs (primary; see module docstring). Wald "
        "chi-square on the method coefficients.",
        "p_exch = sensitivity check under an exchangeable working correlation; "
        "p_lpm = sensitivity check with a linear-probability (Gaussian) GEE; "
        "rho = within-person correlation of the outcome (exchangeable fit).",
        "p_naive = same comparison ignoring clustering (chi-square / Kruskal-Wallis on "
        "the observations); shown only to expose the size of the correction.",
    ]

    exp_pct = expectation_pct_table(obs)
    lines += ["", "-" * 70, "DESCRIPTIVE: % of each method's observations selecting each expectation", "-" * 70,
              exp_pct.to_string(index=False)]
    scale_desc = scale_desc_table(obs)
    lines += ["", "-" * 70, "DESCRIPTIVE: scale scores per method (observation level)", "-" * 70,
              scale_desc.to_string(index=False)]

    exp_tests = expectation_family(obs, methods)
    lines += ["", "=" * 70,
              f"EXPECTATIONS by method, logit GEE, Holm across {len(EXP_OPTS)} options "
              "(inestimable options enter the family at p=1)", "=" * 70, _fmt(exp_tests)]

    scale_tests, posthoc = scale_family(obs, methods)
    lines += ["", "=" * 70, "SCALES by method, Gaussian GEE, Holm across 3 scales", "=" * 70, _fmt(scale_tests)]
    for scale, contrasts in posthoc.items():
        lines += ["", f"Pairwise contrasts for {scale} ({SCALE_DIRECTION[scale]}); diff = a minus b, "
                      "adjusted for scenario, Holm within the 6 pairs:", _fmt(contrasts)]
    if not posthoc:
        lines += ["", "No scale had a Holm-significant omnibus test, so no pairwise contrasts were run."]

    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    exp_pct.to_csv(TABLES_DIR / "pooled_obs_expectation_pct.csv", index=False)
    scale_desc.to_csv(TABLES_DIR / "pooled_obs_scale_desc.csv", index=False)
    exp_tests.to_csv(TABLES_DIR / "pooled_gee_expectations.csv", index=False)
    scale_tests.to_csv(TABLES_DIR / "pooled_gee_scales.csv", index=False)
    for scale, contrasts in posthoc.items():
        contrasts.to_csv(TABLES_DIR / f"pooled_gee_posthoc_{scale}.csv", index=False)
    lines += ["", f"saved -> {TABLES_DIR}/pooled_obs_*.csv, pooled_gee_*.csv"]

    print("\n".join(lines))
    print(f"\nreport saved -> {save_report('pooled_gee', lines)}")


if __name__ == "__main__":
    main()
