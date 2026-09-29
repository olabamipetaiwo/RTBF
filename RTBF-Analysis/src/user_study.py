"""
Analyses for Section 4 (User Study) that follow the structure set by Yao Li.

Covers the parts of that structure with no earlier module:
  * sample profile (data typically shared / tried to delete, literacy, concern)
  * 4.1 past use of each method, how users learned of the options, ideal
    methods per scenario and whether they differ between scenarios
  * 4.2.1 measurement model (exploratory factor analysis of the 12 items)
  * 4.2.2-4.2.4 per-method means pooled and per scenario, and the within-method
    scenario contrast (protection, benefit loss, effort)
  * protection regression on demographics, AI literacy and privacy concern
  * 4.2.5 noticed-referencing question and post-deletion feedback questions

Everything runs on the paired base (n=177), the base used for the rest of the
survey results. Method-selection, willingness and expectation/verification
tests that already exist (src/stats.py, src/willingness.py, src/pooled_gee.py,
src/verify.py) are not repeated here.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.multivariate.factor import Factor
from statsmodels.stats.multitest import multipletests

from src.reporting import save_report
from src.screen import LIKERT, get_bases

RAW = "survey/RTBF_September+9,+2026_14.25.xlsx"

METHODS = {
    1: "Ask chatbot to forget",
    2: "Delete single conversation",
    3: "Clear all conversation history",
    4: "Delete specific memory or fact",
    5: "Clear all saved memories",
    6: "Delete account",
    7: "Privacy dashboard",
    8: "File a request",
}
QUALIFYING = [
    "Delete this single conversation.",
    "Clear all conversation history.",
    "Delete a specific saved memory or fact.",
    "Type a message asking the AI Chatbot to forget it.",
]
SHORT = {
    "Delete this single conversation.": "Single conversation",
    "Clear all conversation history.": "Clear all history",
    "Delete a specific saved memory or fact.": "Specific memory",
    "Type a message asking the AI Chatbot to forget it.": "Ask to forget",
}
SCALES = {"protection": (7, 5), "effort": (8, 4), "benefit_loss": (9, 3)}
SCEN = {"less": ("Q4", "Q4.2"), "more": ("Q5", "Q5.2")}

EDU_ORDER = [
    "Some high school or less", "High school diploma or GED",
    "Some college, but no degree", "Associates or technical degree",
    "Bachelor’s degree",
    "Graduate or professional degree (MA, MS, MBA, PhD, JD, MD, DDS etc.)",
]
AGE_ORDER = ["18-24 years old", "25-34 years old", "35-44 years old",
             "45-54 years old", "55-64 years old", "65+ years old"]
LITERACY_ITEMS = [f"Q9.6_{i}" for i in range(1, 11)]
CONCERN_ITEMS = [f"Q9.4_{i}" for i in range(1, 5)]


def pct(k: int, n: int) -> str:
    return f"{k}/{n} ({100 * k / n:.1f}%)"


def multi_select_freq(df: pd.DataFrame, prefix: str, labels: dict[int, str]) -> list[str]:
    """Counts for a select-all question whose columns are <prefix>_<k>."""
    n = len(df)
    out = []
    for k, label in labels.items():
        col = f"{prefix}_{k}"
        if col in df:
            out.append(f"  {label:<45} {pct(int(df[col].notna().sum()), n)}")
    return out


def likert_num(s: pd.Series) -> pd.Series:
    """1-5 numeric from either the agreement wording or the '5 - ...' wording."""
    def one(v: object) -> float:
        if pd.isna(v):
            return np.nan
        t = str(v).strip()
        if t[:1].isdigit():
            return float(t[0])
        return float(LIKERT.get(t, np.nan))
    return s.map(one)


def scale_scores(df: pd.DataFrame, scen: str) -> pd.DataFrame:
    base, method_col = SCEN[scen]
    out = pd.DataFrame(index=df.index)
    out["method"] = df[method_col]
    for name, (q, k) in SCALES.items():
        items = [f"{base}.{q}_{i}" for i in range(1, k + 1)]
        out[name] = df[items].apply(lambda c: c.map(LIKERT)).mean(axis=1)
    return out


# --------------------------------------------------------------------------
# Sample profile
# --------------------------------------------------------------------------
def sample_profile(p: pd.DataFrame) -> list[str]:
    n = len(p)
    lines = ["=== SAMPLE PROFILE (n=%d) ===" % n]
    shared = {1: "General (no personal info)", 2: "Preferences/opinions",
              3: "Work/professional", 4: "Health/medical", 5: "Financial",
              6: "Location", 7: "Sensitive personal experiences",
              8: "Demographics", 9: "Contact information", 10: "Media"}
    lines.append("Types of information typically shared (select all):")
    lines += multi_select_freq(p, "Q6.2", shared)
    lines.append("Types of data tried to delete (select all):")
    lines += multi_select_freq(p, "Q6.4", {**shared, 12: "Have not attempted"})
    lines.append("Platforms attempted to delete from (select all):")
    lines += multi_select_freq(p, "Q6.3", {1: "Claude", 2: "ChatGPT", 3: "Gemini",
                                           4: "Copilot", 5: "Perplexity", 6: "DeepSeek"})
    lit = p[LITERACY_ITEMS].apply(likert_num).mean(axis=1)
    con = p[CONCERN_ITEMS].apply(likert_num).mean(axis=1)
    lines.append(f"AI literacy (10 items, 1-5): M={lit.mean():.2f} SD={lit.std():.2f}")
    lines.append(f"Privacy concern (4 items, 1-5): M={con.mean():.2f} SD={con.std():.2f}")
    return lines


# --------------------------------------------------------------------------
# 4.1
# --------------------------------------------------------------------------
def past_use(p: pd.DataFrame) -> list[str]:
    n = len(p)
    lines = ["\n=== 4.1 PAST USE OF EACH METHOD (Q3.2, select all; n=%d) ===" % n]
    lines += multi_select_freq(p, "Q3.2", {**METHODS, 9: "Other"})
    lines.append("\nHow did you find out the deletion options existed? (Q6.7)")
    for v, k in p["Q6.7"].value_counts().items():
        lines.append(f"  {v:<55} {pct(int(k), n)}")
    return lines


def ideal_methods(p: pd.DataFrame) -> list[str]:
    """Ideal-method selection (Q4.13/Q5.13, select all) per scenario and the
    paired exact McNemar test per method, Holm across the eight methods."""
    n = len(p)
    lines = ["\n=== 4.1 IDEAL METHODS BY SCENARIO (select all; n=%d) ===" % n]
    rows, pvals = [], []
    for k, label in METHODS.items():
        a = p[f"Q4.13_{k}"].notna().to_numpy()
        b = p[f"Q5.13_{k}"].notna().to_numpy()
        only_b, only_a = int((~a & b).sum()), int((a & ~b).sum())
        res = stats.binomtest(only_b, only_a + only_b, 0.5) if only_a + only_b else None
        p_raw = float(res.pvalue) if res else 1.0
        rows.append((label, int(a.sum()), int(b.sum()), only_a, only_b))
        pvals.append(p_raw)
    p_holm = multipletests(pvals, method="holm")[1]
    lines.append(f"{'method':<34}{'less':>12}{'more':>12}  drop add   p     p_Holm")
    for (label, ka, kb, da, ad), pr, ph in zip(rows, pvals, p_holm):
        lines.append(f"{label:<34}{pct(ka, n):>12}{pct(kb, n):>12}  {da:>3} {ad:>3}  {pr:.3f}  {ph:.3f}")
    return lines


# --------------------------------------------------------------------------
# 4.2.1 measurement model
# --------------------------------------------------------------------------
def item_matrix(df: pd.DataFrame, scen: str) -> pd.DataFrame:
    base = SCEN[scen][0]
    cols = [f"{base}.{q}_{i}" for name, (q, k) in SCALES.items() for i in range(1, k + 1)]
    m = df[cols].apply(lambda c: c.map(LIKERT))
    m.columns = [f"{name[:4]}{i}" for name, (q, k) in SCALES.items() for i in range(1, k + 1)]
    return m


def kmo_bartlett(x: pd.DataFrame) -> tuple[float, float, float]:
    r = np.corrcoef(x.to_numpy().T)
    inv = np.linalg.inv(r)
    d = np.sqrt(np.outer(np.diag(inv), np.diag(inv)))
    partial = -inv / d
    np.fill_diagonal(partial, 0)
    rr = r - np.eye(len(r))
    kmo = (rr ** 2).sum() / ((rr ** 2).sum() + (partial ** 2).sum())
    n, k = x.shape
    chi2 = -(n - 1 - (2 * k + 5) / 6) * np.log(np.linalg.det(r))
    p = stats.chi2.sf(chi2, k * (k - 1) / 2)
    return float(kmo), float(chi2), float(p)


def parallel_analysis(x: pd.DataFrame, iters: int = 500, seed: int = 20260924) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n, k = x.shape
    obs = np.sort(np.linalg.eigvalsh(np.corrcoef(x.to_numpy().T)))[::-1]
    sims = np.empty((iters, k))
    for i in range(iters):
        sims[i] = np.sort(np.linalg.eigvalsh(np.corrcoef(rng.standard_normal((n, k)).T)))[::-1]
    return obs, np.percentile(sims, 95, axis=0)


def factor_model(p: pd.DataFrame) -> list[str]:
    frames = [item_matrix(p, s).dropna() for s in SCEN]
    pooled = pd.concat(frames, ignore_index=True)
    lines = ["\n=== 4.2.1 MEASUREMENT MODEL (EFA, principal axis, oblimin) ===",
             f"observations: {len(pooled)} participant-scenario rows, 12 items"]
    kmo, chi2, pb = kmo_bartlett(pooled)
    lines.append(f"KMO={kmo:.3f}  Bartlett chi2(66)={chi2:.1f}  p={pb:.3g}")
    obs, crit = parallel_analysis(pooled)
    lines.append("eigenvalues (observed / 95th pct parallel): " +
                 ", ".join(f"{o:.2f}/{c:.2f}" for o, c in zip(obs[:5], crit[:5])))
    lines.append(f"factors retained by parallel analysis: {int((obs > crit).sum())}")
    for label, data in [("POOLED", pooled)] + [(f"{s.upper()} scenario", f) for s, f in zip(SCEN, frames)]:
        res = Factor(data, n_factor=3, method="pa").fit()
        res.rotate("oblimin")
        load = pd.DataFrame(res.loadings, index=data.columns,
                            columns=["F1", "F2", "F3"]).round(2)
        # order each factor by the scale that loads highest on it
        lines.append(f"\n{label} loadings (oblimin):")
        lines.append(load.to_string())
        if label == "POOLED":
            lines.append(f"variance explained by the three factors: {1 - float(np.mean(res.uniqueness)):.3f}")
    return lines


# --------------------------------------------------------------------------
# 4.2.2-4.2.4 per-method means, scenario contrast
# --------------------------------------------------------------------------
def per_method_scales(p: pd.DataFrame) -> list[str]:
    lines = ["\n=== 4.2.2-4.2.4 PER-METHOD MEANS (four qualifying methods) ==="]
    parts = []
    for s in SCEN:
        d = scale_scores(p, s)
        d["scenario"] = s
        d["pid"] = p["PROLIFIC_PID"].to_numpy()
        parts.append(d)
    obs = pd.concat(parts, ignore_index=True)
    obs = obs[obs["method"].isin(QUALIFYING)]
    lines.append(f"pooled observations: {len(obs)}")
    for scale in SCALES:
        lines.append(f"\n-- {scale} --")
        lines.append(f"{'method':<22}{'pooled M(SD)':>16}{'less M(n)':>14}{'more M(n)':>14}   between-scenario contrast")
        # Between-scenario contrast per method: everyone who chose the method in
        # the less-sensitive scenario vs everyone who chose it in the more-
        # sensitive one (Mann-Whitney U). Some participants are in both groups,
        # which the test ignores; all four methods can be tested this way.
        rows, pvals = [], []
        for m in QUALIFYING:
            g = obs[obs.method == m]
            gl, gm = g[g.scenario == "less"][scale], g[g.scenario == "more"][scale]
            res = stats.mannwhitneyu(gm, gl, alternative="two-sided")
            rows.append((m, g[scale], gl, gm))
            pvals.append(float(res.pvalue))
        adj = multipletests(pvals, method="holm")[1]
        for (m, gp, gl, gm), pr, ph in zip(rows, pvals, adj):
            lines.append(f"{SHORT[m]:<22}{gp.mean():>8.2f}({gp.std():.2f}){gl.mean():>9.2f}({len(gl)}){gm.mean():>9.2f}({len(gm)})   "
                         f"Mann-Whitney p={pr:.3f}, p_Holm={ph:.3f}")
    return lines


# --------------------------------------------------------------------------
# protection regression
# --------------------------------------------------------------------------
def protection_regression(p: pd.DataFrame) -> list[str]:
    lines = ["\n=== PROTECTION ~ demographics, AI literacy, privacy concern "
             "(OLS, participant-clustered SE, both scenarios pooled) ==="]
    person = pd.DataFrame({
        "pid": p["PROLIFIC_PID"],
        "age": p["Q2.1"].map({v: i for i, v in enumerate(AGE_ORDER)}),
        "edu": p["Q10.1"].map({v: i for i, v in enumerate(EDU_ORDER)}),
        "woman": (p["Q10.2"] == "Woman").astype(float),
        "literacy": p[LITERACY_ITEMS].apply(likert_num).mean(axis=1),
        "concern": p[CONCERN_ITEMS].apply(likert_num).mean(axis=1),
    })
    parts = []
    for i, s in enumerate(SCEN):
        d = person.copy()
        d["scenario_more"] = float(i)
        for name in SCALES:
            d[name] = scale_scores(p, s)[name].to_numpy()
        parts.append(d)
    obs = pd.concat(parts, ignore_index=True).dropna()
    lines.append(f"observations: {len(obs)} ({obs.pid.nunique()} participants)")
    for name in SCALES:
        fit = smf.ols(f"{name} ~ scenario_more + age + edu + woman + literacy + concern",
                      data=obs).fit(cov_type="cluster", cov_kwds={"groups": obs["pid"]})
        lines.append(f"\n-- {name}: R2={fit.rsquared:.3f} --")
        tab = pd.DataFrame({"b": fit.params, "SE": fit.bse, "p": fit.pvalues}).round(3)
        lines.append(tab.to_string())
    return lines


# --------------------------------------------------------------------------
# 4.2.5 additions
# --------------------------------------------------------------------------
def referencing_and_feedback(p: pd.DataFrame) -> list[str]:
    n = len(p)
    lines = ["\n=== 4.2.5 NOTICED REFERENCING AND POST-DELETION FEEDBACK (n=%d) ===" % n]
    lines.append("Noticed the chatbot referencing information believed deleted (Q6.8):")
    for v, k in p["Q6.8"].value_counts().items():
        lines.append(f"  {v:<45} {pct(int(k), n)}")
    lines.append("Confirmation currently received (Q7.1, select all):")
    lines += multi_select_freq(p, "Q7.1", {1: "Clear message confirming deletion",
                                            2: "Brief or vague acknowledgement",
                                            3: "No feedback at all",
                                            4: "Have not attempted to delete", 5: "Other"})
    lines.append("Feedback that should be provided (Q7.2, select all):")
    lines += multi_select_freq(p, "Q7.2", {1: "Popup confirmation", 2: "Inline natural-language confirmation",
                                            3: "Email confirmation", 4: "Timestamp/estimate of completion",
                                            5: "Breakdown of what was deleted and may be retained",
                                            6: "No feedback necessary", 7: "Other"})
    return lines


def verification_by_method(p: pd.DataFrame) -> list[str]:
    """Pooled verification-option rates per qualifying method (participant-
    scenario observations), the counterpart of the expectation table."""
    labels = {1: "Asked same conv.", 2: "Asked new conv.", 3: "Checked settings",
              4: "Checked interface", 5: "Privacy portal", 6: "Did not know how",
              7: "Did not want to"}
    parts = []
    for s, (base, mcol) in SCEN.items():
        q = "Q4.5" if s == "less" else "Q5.5"
        d = pd.DataFrame({"method": p[mcol]})
        for k in labels:
            d[k] = p[f"{q}_{k}"].notna().astype(float)
        parts.append(d)
    obs = pd.concat(parts, ignore_index=True)
    obs = obs[obs["method"].isin(QUALIFYING)]
    lines = ["\n=== 4.2.5 VERIFICATION BY METHOD (pooled observations, % selecting) ===",
             f"{'method (obs)':<26}" + "".join(f"{l[:12]:>14}" for l in labels.values())]
    for m in QUALIFYING:
        g = obs[obs.method == m]
        lines.append(f"{SHORT[m] + ' (' + str(len(g)) + ')':<26}" +
                     "".join(f"{100 * g[k].mean():>14.1f}" for k in labels))
    lines.append(f"{'All (' + str(len(obs)) + ')':<26}" +
                 "".join(f"{100 * obs[k].mean():>14.1f}" for k in labels))
    return lines


def main() -> None:
    p = get_bases(RAW, verbose=False)["paired"]
    lines: list[str] = []
    for step in (sample_profile, past_use, ideal_methods, factor_model,
                 per_method_scales, protection_regression,
                 referencing_and_feedback, verification_by_method):
        lines += step(p)
    print("\n".join(lines))
    print("saved ->", save_report("user_study", lines))


if __name__ == "__main__":
    main()
