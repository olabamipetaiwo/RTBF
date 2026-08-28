# tester

Playwright automation for the RTBF technical audit. See `CLAUDE.md` for
full project context (what this tests, where the injection/erasure/probe
text comes from, contamination-control rules inherited from the experiment
design).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
```

## Status

Scaffolding only. No platform flows written yet -- `flows/` is empty
pending selector work against each live platform.
