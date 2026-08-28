"""
Task 1 -- discriminant-validity check between the three Likert scales
(protection, effort, benefit_loss) via pairwise Spearman correlation.
Spearman (not Pearson) because the scales are non-normal (per the existing
Shapiro results in stats.between_scenario_likert). |rho| >= 0.8 on a pair
means the two scales are too tightly coupled to call them distinguishable
constructs; the threshold is applied to |rho| rather than rho because
protection and benefit_loss could plausibly correlate negatively (more
protection felt <-> less loss felt) -- the threshold is about strength of
association in either direction, not sign.

Two scopes, 3 pairs each = 9 correlations total:
  A. within scenario (less, more) -- bases["less"] (n=177) and
     bases["more"] (n=178) used directly and independently, matching how
     src.stats.between_method (steps 1-2) already treats each scenario's
     base as its own independent sample rather than the paired base.
  B. pooled (both scenarios combined) -- bases["paired"] (n=177). Each
     respondent's less- and more-scenario score is averaged per scale
     BEFORE correlating, reusing task 2's already-established solution
     ("average each respondent's own less/more scores first, so each
     person contributes exactly one observation") -- there is no
     method-grouping dimension in this pooled scope, so task 2's refined
     per-method-conditional averaging doesn't apply; a flat average is
     correct here.

A local Holm correction is applied across all 9 raw p-values as a single
family for this module's own report (p_holm column) -- same "one family"
convention as src.stats.between_scenario_likert's "Holm x3" across its 3
scale comparisons. Per the task spec ("each one gets checked against 0.8
independently"), the |rho|<0.8 DISTINCT/COUPLED verdict is NOT itself
multiple-comparison corrected -- it's a straightforward per-row threshold
check, reported only in this module's own output. Only the raw (uncorrected)
spearmanr p-value feeds the global registry via discriminant_validity(),
matching every other scipy_analysis module's collect_all_pvals contract
(they all return raw p, never locally-corrected p).
"""

import itertools
import pandas as pd
from scipy import stats

from src.screen import get_bases
from src.stats import scale_score, SCALES

from .reporting import save_report
from .correction import holm

PAIRS = list(itertools.combinations(SCALES.keys(), 2))
THRESHOLD = 0.8


def _scale_scores(df, base):
    """{'protection': Series, 'effort': Series, 'benefit_loss': Series}, indexed like df."""
    return {scale: scale_score(df, base, q, k) for scale, (q, k) in SCALES.items()}


def _spearman_row(label, s1, s2):
    d = pd.concat([s1, s2], axis=1).dropna()
    rho, p = stats.spearmanr(d.iloc[:, 0], d.iloc[:, 1])
    return {"label": label, "rho": rho, "n": len(d), "p_raw": p}


def _within_scenario_rows(bases):
    rows = []
    for scen, base in (("less", "Q4"), ("more", "Q5")):
        scores = _scale_scores(bases[scen], base)
        for s1, s2 in PAIRS:
            rows.append(_spearman_row(f"[{scen}] {s1}~{s2}", scores[s1], scores[s2]))
    return rows


def _pooled_rows(bases):
    paired = bases["paired"]
    less_scores = _scale_scores(paired, "Q4")
    more_scores = _scale_scores(paired, "Q5")
    pooled = {
        scale: pd.concat([less_scores[scale], more_scores[scale]], axis=1).mean(axis=1)
        for scale in SCALES
    }
    return [_spearman_row(f"[pooled] {s1}~{s2}", pooled[s1], pooled[s2]) for s1, s2 in PAIRS]


def discriminant_validity(bases, lines=None):
    """3 pairs x [less, more, pooled] = 9 pairwise Spearman correlations.

    Returns [(label, p_raw)] for the global p-value registry -- raw p only,
    matching stats.between_method(bases, lines) / stats.method_switching(...)
    etc. If `lines` is given, a full report table (rho, n, p_raw, p_holm,
    verdict) is appended to it in place.
    """
    rows = _within_scenario_rows(bases) + _pooled_rows(bases)

    padj = holm([r["p_raw"] for r in rows])
    for r, pa in zip(rows, padj):
        r["p_holm"] = pa
        r["verdict"] = "DISTINCT" if abs(r["rho"]) < THRESHOLD else "COUPLED"

    if lines is not None:
        lines.append("\n" + "=" * 70)
        lines.append("TASK 1  DISCRIMINANT VALIDITY (Spearman, |rho|>=0.8 = coupled, Holm x9)")
        lines.append("=" * 70)
        lines.append(f"\n{'label':28} {'rho':>7} {'n':>5} {'p_raw':>8} {'p_holm':>8}  verdict")
        for r in rows:
            lines.append(f"{r['label']:28} {r['rho']:7.3f} {r['n']:5d} "
                          f"{r['p_raw']:8.4f} {r['p_holm']:8.4f}  {r['verdict']}")

    return [(r["label"], r["p_raw"]) for r in rows]


if __name__ == "__main__":
    bases = get_bases(verbose=False)
    lines = []
    discriminant_validity(bases, lines)

    for line in lines:
        print(line)

    report_path = save_report("correlations", lines)
    print(f"\nreport saved -> {report_path}")
