# Santhanam, Dang, Shan, Neamtiu. Scraping Sticky Leftovers: App User Information Left on Servers After Account Deletion

IEEE Symposium on Security and Privacy (S&P) 2022, pp. 2145-2160, DOI 10.1109/SP46214.2022.9833720 (venue, pages and DOI from Crossref today). File: `2_audits/santhanam-sp22-sticky-leftovers.pdf`. **This PDF is the authors' preprint** (PDF created August 2021, no venue header, 13 pages), not the S&P version. Numbers below come from the preprint; check each against the published paper before quoting. Read the abstract, introduction, problem definition, the pilot study, the inference approach (Section 6.1), the retention-period and statistics results, limitations and related work. I did not read the static-analysis and NLP pipeline in detail, nor the cleaner's engineering.

## Question
Can users delete app accounts, and after deletion does the app's server still keep the data ("leftover account information", LAI)? Do apps keep their own retention promises (Abstract)?

## Method
- 1,435 popular Google Play apps and 771 websites; 938 require sign-up, 260 use third-party sign-in, leaving 678 "own sign-in" apps for the study (Section 1).
- Pilot study of 188 apps: sign up, explore, delete the account, uninstall, reinstall and try to sign up again with the same information (Section 1, Table 1).
- Four tools (Section 1): LeftoverAccountAnalyzer, AccountDeletionAnalyzer, LeftoverAccountCleaner and RetentionPeriodAnalyzer.
- Inference of what stays on the server (Sections 6 and 6.1): because the server database cannot be seen, the tools intercept the app's account-manipulation API calls (create, delete account, create field, delete field) at runtime and compute the fields still retained as fields added minus fields deleted. If re-registration with the old email returns "already exists", the account is still there (Figure 6 shows the "no LAI", "all fields left" and "some fields left" cases).

## Findings
- 64.45% of apps offer no way to delete an account; 35.55% do (Abstract, Introduction). Pilot (135 apps): 57.04% had no deletion function, 34.81% left LAI after uninstalling, and 2.96% kept LAI after account deletion (Table 1).
- Main study: 254 apps (37.46% of 678) leave LAI after uninstallation and 17 apps (2.5%) after account deletion, including government IDs or banking details (Section 1, Table 7).
- Only 5% of apps state a retention period (30 minutes to 5 years; median 30 days; mean 117.85 days). Three apps with over 50 million installs keep data months after the stated period; eBay is the shown example (Table 9, Figure 1d).
- The cleaner removed leftover accounts for 214 of 245 uninstalled apps (87.34%). Analyzer accuracy: F-measure above 88% (Abstract); retention-period analyzer 91.9%.

## Limits the authors state
It cannot remove LAI from the backend database controlled by developers; the account analyzer is not fully automated when CAPTCHAs are used; the NLP only handles English; invisible buttons are not detected (Section 10).

## How it differs from ours
- It infers server-side state from code and API traffic of an app the researchers control on their own device. We cannot inspect an agent's back end, so our check is behavioural.
- The idea "reinstall and re-register to see whether the old account persists" is a behavioural probe like ours, and the paper's own rule ("already exists") only shows persistence, never absence.

## Use in our paper
- Cite for the finding that deletion can leave data on servers even when the app says it will erase (2.5% after deletion in the main study), and for apps that break their own stated retention period. Use the 17-of-678 base, not 2.5% of 1,435.
- Careful: confirm figures in the S&P version because this is the preprint.
