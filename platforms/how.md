# Analysis approach

How each platform file (`chatgpt.md`, `claude.md`, ...) moves from the outcome data to its pattern, reasons, findings and survey comparison. The data-collection method (injection, erasure, recall, scoring) is in the paper's Methods; this file covers only the analysis built on its outputs. Apply the same four steps to every platform.

## 1. Pattern (descriptive)

- Tabulate outcomes (recall success, recall failed, can't tell) by study and erasure method, from `RTBF-Analysis/outputs/tables/audit_outcomes.csv`.
- Add the cuts that show how an outcome arises: which probe retrieved the token, the same conversation against a new one, and the acknowledgment at erasure.
- A pattern is stated with its proportion and base (for example, 108 of 131). Words such as "most" never appear without the number. A single cell is never a pattern.

## 2. Reasons (inference to the best explanation)

- List the candidate explanations for the pattern, including the mundane ones.
- Test each against evidence that distinguishes it from the others, and record the verdict in the platform's rival-explanations table using one of: **supported**, **ruled out by design** (the study design excludes it), **ruled out** (direct evidence excludes it), **no detectable effect** (a null result; never written as "ruled out"), **weakly against**, or **open**.
- Always test these rivals:

| Rival explanation | Evidence that tests it |
|---|---|
| Prompt wording | Outcomes by the human-coded prompt features (`src/outcome_by_prompt_features.py`) |
| Account configuration | The platform's default settings, checked on a new account |
| Contamination between cells | Dedicated accounts, unique tokens, the sibling rule |
| Procedural fault | Run logs and transcripts; deviations re-run or disclosed |

- A mechanism that cannot be observed through the interface is stated as a hypothesis, not as a finding.

## 3. Findings (criteria)

A claim is a finding only if:

1. it follows from the outcome rule, not from interpretation;
2. it holds across cells, with its base stated;
3. it survives the rival explanations in step 2;
4. every input it rests on is either deterministic (a documented rule) or human-coded with reported reliability.

Single cells serve only as illustrations. An illustrative case must show the majority pattern, and the text states how common that pattern is. A count that fails criterion 4 (for example, one produced by a pattern search that no coder has checked) stays in Evidence, marked as not used, until it is human-coded.

## 4. Survey comparison (at the level of the method)

The survey did not ask about specific platforms, so the comparison is method against method. Each survey item is mapped to one audit measure:

| Survey item | Audit measure |
|---|---|
| What participants expect to happen | Recall outcome |
| How they would verify | Same conversation against new conversation |
| Protection and effort ratings | Recall outcome of the same method |
| Have seen deleted information come back | Recall success rate |

The comparison is descriptive. The two samples differ in kind (participants against cells), so no statistical test is run across them. Survey figures are quoted only from their saved script.

## Writing each platform file

| Question | What a good answer does | What to avoid |
|---|---|---|
| Pattern | One sentence that states the behaviour, then the single number that shows it | Listing every count and probe |
| Reasons | One mechanism that explains all the observations, illustrated by one case | Several separate guesses |
| Findings | Two or three claims a reader could repeat, each one sentence | Restating the pattern as a list |
| Survey | Follow what a user would experience and mark where expectation and outcome diverge | Matching percentages to percentages |

- Paper register throughout; no cell IDs; operational detail (control names, probes, timing) belongs in Evidence.
- Each platform file stays concise (Summary, Pattern, Why, Findings, Implications) and ends with a link to its evidence file, `evidence/<platform>.md`: every number with the script it comes from, the rival-explanations table, and counts not used in the findings.
