"""
Step 2: Scale reliability (Cronbach's alpha) for each multi-item scale,
per scenario. Go/no-go on averaging items into a scale score.

Scales (each internally single-direction, so no reverse-coding needed):
  .7 protection (5 items, high = more protection)
  .8 effort     (4 items, high = more effort/burden)
  .9 benefit-loss(3 items, high = more loss)

Likert values are TEXT; mapped to 1-5. Note raw-data typo "Stongly Disagree"
is handled explicitly so no items silently drop to NaN.
"""

import pandas as pd
import pingouin as pg
from src.screen import get_bases, LIKERT
from src.reporting import save_report

SCALES = {".7": ("protection", 5), ".8": ("effort", 4), ".9": ("benefit_loss", 3)}
SCENARIOS = {"less": "Q4", "more": "Q5"}


def scale_items(base, q):
    return [f"{base}{q}_{i}" for i in range(1, SCALES[q][1] + 1)]


def to_numeric(df, items):
    m = df[items].apply(lambda col: col.map(LIKERT))
    unmapped = df[items].where(df[items].notna() & m.isna())
    n_bad = int(unmapped.notna().sum().sum())
    return m, n_bad


def run():
    bases = get_bases(verbose=False)
    rows = []
    for scen, base_q in SCENARIOS.items():
        df = bases[scen]
        for q, (name, k) in SCALES.items():
            items = scale_items(base_q, q)
            num, n_bad = to_numeric(df, items)
            complete = num.dropna()
            alpha, ci = pg.cronbach_alpha(data=complete)
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

    out_path = "outputs/tables/scale_reliability.csv"
    tbl.to_csv(out_path, index=False)
    lines.append(f"\nsaved -> {out_path}")

    for line in lines:
        print(line)

    report_path = save_report("reliability", lines)
    print(f"report saved -> {report_path}")