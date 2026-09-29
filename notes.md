# Open items (2026-09-23)

## 1. Tasks

Fix code to accomodate copilot UI changes

1. **Copilot sending is blocked.** copilot.com shows "Verify you are human" and a manual tick does not clear it. Recall sends messages, so it hits the same wall: 12 battery cells on 10-08, 120 NL-forget cells on 10-19. Options: manual recall, extend the disclosed stealth measure, or report it as blocked by the platform.
2. **Copilot old-UI code.** R2 and the Copilot delete methods in `flows/copilot.py` are still written for the old interface. Needed before erasing `CO-I1-E4` and `CO-I1-E6` (throwaway chat URL and two fresh copilot.com exports).
--------

1. 197 incomplete NL-forget replies (needs your decision)
- OCR read 601 as whole. The other 197 are cut off or missing their start, mostly Perplexity (85) and DeepSeek (73).
- I recommend re-loading each platform's own conversation and capturing a full-page screenshot plus the text scraped from the page. That is about 200 page loads, not 800.
- Do it on Perplexity, DeepSeek, ChatGPT and Claude first. Copilot and Gemini are logged out and Copilot is also Cloudflare-blocked, so they wait for fresh exports.
- The alternative is to code Acknowledgment only on the 601 whole replies and report the 197 as unreadable. That drops the redirect cases ("go to Settings"), and a cut-off reply could be hiding one of those.
- I'd fix the erase step so it scrolls and captures the full reply, and leave the --force OCR re-run for the end. This is already the "deviation from agreed design" rule.

2. Three battery cells with no erase evidence
- GE-I1-E3 and GE-I2-E3: Google blocks automation, so the user erased them by hand at myactivity.google.com on 2026-09-13. No screenshots on file.
- GE-I1-E5: the tracked delete timed out 3 times and it was marked erased on end state only (lower confidence).
- GE-I1-E4, GE-I2-E2 and CH-I3-E4 are valid nulls, already recorded in their xlsx Notes. They need no erase evidence.
- No live runs are needed. Inject evidence already exists for all of them.

3. 70 thin battery erase JSONs (no fix needed)
- Those erasures were UI-only, so the screenshot is the evidence. One sentence in Methods says so.
- The 13 NL-forget battery cells lack replies, so I'd OCR them with the existing extract_erase_replies.py. Gemini may need the same live re-capture as gap 1.

4. Gemini replies and response-type coding (needs Taiwo/Jihwan)
- Only 4 of 13 Gemini replies are checked. Finish those and code the response types across all platforms.

----


## 2. Cells not yet erased (32)

- 30 NL-forget cells: the 5 generic prompts, held back by decision.
- `CO-I1-E4`, `CO-I1-E6` (Copilot; see 1.1 and 1.2; `CO-I1-E6` also had the Temporary-mode problem).


