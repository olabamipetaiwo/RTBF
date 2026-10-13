"""
Confirmatory factor analysis for the 12 protection / effort / benefit-loss
items. The three-factor structure comes from prior literature, so CFA (not
EFA) is the right validation step.

Reports for each slice (LS, MS, Pooled):
  - model fit: chi-square, df, p, CFI, TLI, RMSEA, SRMR
  - standardised factor loadings (all should be > .6)
  - AVE per factor (> .5 acceptable, > .6 good)
  - Cronbach's alpha per factor (should be > .8)

Uses semopy (ML estimation) + pingouin (Cronbach's alpha) + scipy.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pingouin as pg
import semopy

from src.reporting import save_report
from src.screen import get_bases
from src.user_study import item_matrix, SCEN

MODEL_SPEC = """
protection =~ prot1 + prot2 + prot3 + prot4 + prot5
effort     =~ effo1 + effo2 + effo3 + effo4
benefit    =~ bene1 + bene2 + bene3
"""

FACTOR_ITEMS = {
    "protection": ["prot1", "prot2", "prot3", "prot4", "prot5"],
    "effort": ["effo1", "effo2", "effo3", "effo4"],
    "benefit_loss": ["bene1", "bene2", "bene3"],
}


def _cov_to_corr(c: np.ndarray) -> np.ndarray:
    d = np.sqrt(np.diag(c))
    return c / np.outer(d, d)


def compute_srmr(mod: semopy.Model, data: pd.DataFrame) -> float:
    sigma = mod.calc_sigma()[0]
    obs_order = list(mod.vars["observed"])
    s_full = data[obs_order].cov().values
    r_obs = _cov_to_corr(s_full)
    r_imp = _cov_to_corr(sigma)
    p = s_full.shape[0]
    tril = np.tril_indices(p, k=0)
    srmr = np.sqrt(np.sum((r_obs[tril] - r_imp[tril]) ** 2) * 2 / (p * (p + 1)))
    return float(srmr)


def fit_cfa(data: pd.DataFrame) -> tuple[semopy.Model, dict]:
    mod = semopy.Model(MODEL_SPEC)
    mod.fit(data)
    stats = semopy.calc_stats(mod)
    fit = {k: float(stats[k].iloc[0]) for k in stats.columns}
    fit["SRMR"] = compute_srmr(mod, data)
    return mod, fit


def standardised_loadings(mod: semopy.Model) -> pd.DataFrame:
    insp = mod.inspect(std_est=True)
    loadings = insp[insp["op"] == "~"].copy()
    loadings = loadings[["rval", "lval", "Estimate", "Est. Std", "p-value"]]
    loadings.columns = ["factor", "item", "unstd", "std_loading", "p"]
    return loadings.reset_index(drop=True)


def compute_ave(loadings: pd.DataFrame) -> dict[str, float]:
    ave = {}
    for factor in loadings["factor"].unique():
        lam = loadings.loc[loadings["factor"] == factor, "std_loading"].to_numpy()
        ave[factor] = float(np.mean(lam ** 2))
    return ave


def cronbach_per_factor(data: pd.DataFrame) -> dict[str, float]:
    alphas = {}
    for name, items in FACTOR_ITEMS.items():
        alpha, _ = pg.cronbach_alpha(data=data[items])
        alphas[name] = round(float(alpha), 3)
    return alphas


def run_one_slice(data: pd.DataFrame, label: str) -> list[str]:
    lines = [f"\n--- {label} (n={len(data)}) ---"]

    mod, fit = fit_cfa(data)

    lines.append("Model fit:")
    for k in ["chi2", "dof", "chi2 p-value", "CFI", "TLI", "RMSEA", "SRMR"]:
        if k in fit:
            lines.append(f"  {k}: {fit[k]:.4f}")

    loadings = standardised_loadings(mod)
    lines.append("\nStandardised factor loadings:")
    for _, row in loadings.iterrows():
        flag = " ***" if row["std_loading"] < 0.6 else ""
        lines.append(f"  {row['factor']:<12} <- {row['item']:<8}  {row['std_loading']:.3f}{flag}")

    min_loading = loadings["std_loading"].min()
    lines.append(f"  min loading: {min_loading:.3f} {'(BELOW .6)' if min_loading < 0.6 else '(all above .6)'}")

    ave = compute_ave(loadings)
    lines.append("\nAVE per factor:")
    for f, v in ave.items():
        verdict = "good" if v >= 0.6 else ("acceptable" if v >= 0.5 else "BELOW .5")
        lines.append(f"  {f:<12}  {v:.3f}  ({verdict})")

    alphas = cronbach_per_factor(data)
    lines.append("\nCronbach's alpha:")
    for f, a in alphas.items():
        verdict = "good" if a >= 0.8 else "BELOW .8"
        lines.append(f"  {f:<12}  {a:.3f}  ({verdict})")

    return lines


def run():
    bases = get_bases(verbose=False)
    p = bases["paired"]

    ls_data = item_matrix(p, "less").dropna()
    ms_data = item_matrix(p, "more").dropna()
    pooled = pd.concat([ls_data, ms_data], ignore_index=True)

    lines = ["=== CONFIRMATORY FACTOR ANALYSIS (3-factor, ML estimation) ==="]

    for data, label in [(pooled, "Pooled"), (ls_data, "LS"), (ms_data, "MS")]:
        lines += run_one_slice(data, label)

    return lines


if __name__ == "__main__":
    lines = run()
    for line in lines:
        print(line)
    report_path = save_report("cfa", lines)
    print(f"\nreport saved -> {report_path}")
