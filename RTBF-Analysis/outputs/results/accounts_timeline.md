# accounts_timeline

_Run at 2026-11-10T00:13:39_

```text
Base: 865 test cases with a recall outcome (outputs/tables/audit_outcomes_provisional.csv).

Accounts per agent (one account = one agent + one email):
  chatgpt: 7 accounts, 151 cases
  claude: 8 accounts, 148 cases
  copilot: 6 accounts, 145 cases
  deepseek: 3 accounts, 137 cases
  gemini: 8 accounts, 145 cases
  perplexity: 2 accounts, 139 cases
  total: 34 accounts

Cases per account, by role:
  chatgpt | account-wide deletion shared with another case: 2 account(s), cases per account [2, 2]
  chatgpt | full deletion procedure: 3 account(s), cases per account [1, 1, 1]
  chatgpt | main (shared by unrelated cases): 1 account(s), cases per account [11]
  chatgpt | typed-request study: 1 account(s), cases per account [133]
  claude | account-wide deletion shared with another case: 2 account(s), cases per account [1, 1]
  claude | account-wide deletion that would reach pending recalls: 1 account(s), cases per account [1]
  claude | full deletion procedure: 3 account(s), cases per account [1, 1, 1]
  claude | main (shared by unrelated cases): 1 account(s), cases per account [9]
  claude | typed-request study: 1 account(s), cases per account [133]
  copilot | account-wide deletion shared with another case: 1 account(s), cases per account [1]
  copilot | account-wide deletion that would reach pending recalls: 1 account(s), cases per account [2]
  copilot | main (shared by unrelated cases): 1 account(s), cases per account [7]
  copilot | moved after the Copilot interface migration: 2 account(s), cases per account [1, 1]
  copilot | typed-request study: 1 account(s), cases per account [133]
  deepseek | full deletion procedure: 1 account(s), cases per account [1]
  deepseek | main (shared by unrelated cases): 1 account(s), cases per account [3]
  deepseek | typed-request study: 1 account(s), cases per account [133]
  gemini | account-wide deletion shared with another case: 1 account(s), cases per account [1]
  gemini | account-wide deletion that would reach pending recalls: 1 account(s), cases per account [2]
  gemini | full deletion procedure: 2 account(s), cases per account [1, 1]
  gemini | main (shared by unrelated cases): 1 account(s), cases per account [4]
  gemini | moved off an unstable account: 2 account(s), cases per account [2, 1]
  gemini | typed-request study: 1 account(s), cases per account [133]
  perplexity | main (shared by unrelated cases): 1 account(s), cases per account [6]
  perplexity | typed-request study: 1 account(s), cases per account [133]

Windows (UTC dates):
  injected_at: 2026-08-28 to 2026-09-13 (865 of 865 cases have a timestamp)
  erased_at: 2026-08-31 to 2026-09-29 (865 of 865 cases have a timestamp)
  recalled_at: 2026-10-12 to 2026-11-05 (816 of 865 cases have a timestamp)
  MASTER: injected 2026-08-28 to 2026-09-11; recalled 2026-10-12 to 2026-10-26
  NL FORGET: injected 2026-09-12 to 2026-09-13; recalled 2026-10-18 to 2026-11-05

Intervals (the paper claims deletion >= 48 h after injection and recall >= 30 days after deletion):
  injection -> deletion: min 48.7 h, median 130.5 h, cases under 48 h: 0 (missing 0)
  deletion -> recall: min 30.2 days, median 30.9 days, cases under 30 days: 0 (missing 49)
  cases without a recall timestamp: 49 ({'copilot': 39, 'gemini': 10}; placeholder-filled: 49)
```
