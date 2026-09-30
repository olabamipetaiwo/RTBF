Injection and erasure
- Injection is complete: all 828 NL-forget cells (138 prompts × 6 platforms) are in.
- run_tracking.json has 906 cells: 876 erased and 30 still injected.

- The 30 injected cells are 5 prompts (I0056, I0064, I0088, I0249, I0280) × 6 platforms. I believe these are the generic "Group 2" prompts you decided to hold, so they are intentionally not run.


Copilot
- Fix the old UI flow to accoutn for the new ons

Recall
- The FOUND-reply spot check is parked until those results exist.
- N3 -  A live check that platforms echo their own probe replies into memory. Only DeepSeek and Free-tier Perplexity can't carry an echo, and the risk on the other four is plausible but untested.
- Why the echo check matters. It tests whether the "not independent" caution is a real effect.
- If platforms don't save their own probe replies, the cross-session visit is independent evidence even when visit 1 leaked. The label throws away good data, and you could report cross-session as a second measurement.
- If they do, the label is needed. You could then say how often echoing happens, which answers a reviewer asking "how do you know this isn't an echo?"

As it stands, the paper can only say a reply "may be saved."

The check isn't urgent. The labelling runs automatically and doesn't depend on the answer, so the 2026-10-01 recall isn't blocked. It only decides how the results are interpreted, so it can wait until after the first recalls.

----

The injection and erasure phases are almost finished. 

### Where things stand
- Tracking: 906 cells are tracked. 874 are erased and 30 are still injected.

### Not erased yet (32 cells)
- 30 NL-forget cells: These are the 5 generic prompts, held back by your decision.

### Open decisions and cleanup
1. 197 incomplete NL-forget replies: OCR read 601 replies as whole, and 197 are cut off or missing their start, mostly Perplexity (85) and DeepSeek (73). I recommend reloading each platform's own conversation for a full-page screenshot and scraped text, which is about 200 page loads. Perplexity, DeepSeek, ChatGPT and Claude come first, since Copilot and Gemini are logged out. The alternative is to code only the 601 whole replies and report 197 as unreadable. That would drop any redirect cases like "go to Settings".
2. Three battery cells without erase evidence: GE-I1-E3 and GE-I2-E3 were erased by hand at myactivity.google.com on 2026-09-13 (Google blocks automation), and GE-I1-E5 was marked erased on end state only (lower confidence).
3. Response-type coding: Only 4 of 13 Gemini replies are checked. You and Jihwan still need to finish those and code the response types across all platforms.

### CoPilot Blockers

Copilot sending is blocked. Copilot moved to copilot.com, which shows "Verify you are human" and doesn't clear even after a manual tick. Recall sends messages, so it hits the same wall. That affects 12 battery cells on 10-08 and 120 NL-forget cells on 10-19. The options are manual recall, extending the stealth measure already disclosed for two other platforms, or reporting Copilot as blocked by the platform. That call is yours.


Code in tester/flows/copilot.py still on the old UI
- The new-site work is done. That covers new_conversation, sending and uploading, the login check and _send_nl_forget.
- These methods still need re-mapping on copilot.com:
  - _open_view_memory and read_memory_settings
  - the sidebar row finders
  - _delete_conversation_history
  - _delete_all_memory
  - _delete_via_facts_editor
  - _delete_via_privacy_dashboard
  - _erase_maximal

What I need from you
- A throwaway chat URL that you make by hand, so I can test deletion without touching real study chats.
- Fresh cookie and localStorage exports for the main account and ui_migration_i1, taken from a copilot.com tab.
- A decision on Copilot recall.

Recall is blocked
- Sending hits "Verify you are human," which a manual tick didn't clear.
- That affects 12 battery cells due 2026-10-08 and 120 NL-forget cells due 2026-10-19.
- Your options are manual recall, extending the stealth measure already disclosed for two other platforms, or reporting Copilot as blocked by the platform.


Summary -  Re-map read_memory_settings() and _open_view_memory() in flows/copilot.py to copilot.com, and decide how to get past the "Verify you are human" check so recall can send messages (manual, extended stealth, or report Copilot as blocked) before the 2026-10-08 battery recall.



 