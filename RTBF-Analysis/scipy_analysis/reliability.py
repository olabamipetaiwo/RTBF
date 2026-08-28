"""
Scipy-only reimplementation of src/reliability.py (step 2: Cronbach's alpha).
Formula and Feldt (1987) confidence interval reimplemented by hand with
pandas .cov() + scipy.stats.f, replacing pingouin.cronbach_alpha (same
formula pingouin uses internally -- see pingouin.reliability.cronbach_alpha).
"""

import numpy as np
import pandas as pd
from scipy.stats import f

from src.screen import get_bases, LIKERT

from .reporting import save_report

SCALES = {".7": ("protection", 5), ".8": ("effort", 4), ".9": ("benefit_loss", 3)}
SCENARIOS = {"less": "Q4", "more": "Q5"}


def scale_items(base, q):
    return [f"{base}{q}_{i}" for i in range(1, SCALES[q][1] + 1)]


def to_numeric(df, items):
    m = df[items].apply(lambda col: col.map(LIKERT))
    unmapped = df[items].where(df[items].notna() & m.isna())
    n_bad = int(unmapped.notna().sum().sum())
    return m, n_bad


def cronbach_alpha(data, ci=0.95):
    n, k = data.shape
    C = data.cov()
    alpha = (k / (k - 1)) * (1 - np.trace(C.values) / C.values.sum())

    a = 1 - ci
    df1 = n - 1
    df2 = df1 * (k - 1)
    lower = 1 - (1 - alpha) * f.isf(a / 2, df1, df2)
    upper = 1 - (1 - alpha) * f.isf(1 - a / 2, df1, df2)
    return alpha, np.round([lower, upper], 3)


def run():
    bases = get_bases(verbose=False)
    rows = []
    for scen, base_q in SCENARIOS.items():
        df = bases[scen]
        for q, (name, k) in SCALES.items():
            items = scale_items(base_q, q)
            num, n_bad = to_numeric(df, items)
            complete = num.dropna()
            alpha, ci = cronbach_alpha(complete)
            rows.append({
                "scenario": scen, "scale": name, "items": k,
                "n_complete": len(complete),
                "alpha": round(alpha, 3),
                "ci95": f"[{ci[0]:.2f}, {ci[1]:.2f}]",
                "unmapped_values": n_bad,
                "verdict": "OK" if alpha >= 0.70 else "REVIEW",
            })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    tbl = run()

    lines = [
        "=== Cronbach's alpha (>=0.70 = acceptable) ===",
        tbl.to_string(index=False),
    ]

    out_path = "scipy_analysis/outputs/tables/scale_reliability.csv"
    tbl.to_csv(out_path, index=False)
    lines.append(f"\nsaved -> {out_path}")

    for line in lines:
        print(line)

    report_path = save_report("reliability", lines)
    print(f"report saved -> {report_path}")
