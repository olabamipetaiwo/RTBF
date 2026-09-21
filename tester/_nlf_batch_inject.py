"""One-off batch driver: injects every NL-forget cell for one platform,
skipping any already-injected (tracked) cell. Catches exceptions per-cell
so one failure doesn't abort the whole run -- logs progress to
_nlf_batch_<platform>.log instead.

Batches attempts (success OR failure both count -- a failed send still hit
the send-button, so it likely still counts against whatever's rate-limiting
us) in groups of BATCH_SIZE, sleeping COOLDOWN_SECONDS between batches --
added 2026-09-11 after ChatGPT's failure rate went from ~2% (1/44) to
~50%+ right around attempt 44-50, a clean rate-limit/soft-throttle
signature, not random flakiness (confirmed: 37/38 failures were the exact
same "Locator.click: Timeout 10000ms exceeded" on the send-button).
Failed cells are NOT marked injected (inject_cell only calls
tracking.mark_injected on success), so they're automatically retried in a
later batch/run without any special-casing here.

Usage: python _nlf_batch_inject.py <platform> [batch_size] [cooldown_seconds]
"""
import sys
import time
import traceback

import openpyxl

import config
import tracking
import run_cell as rc

platform = sys.argv[1]
BATCH_SIZE = int(sys.argv[2]) if len(sys.argv) > 2 else 40
COOLDOWN_SECONDS = int(sys.argv[3]) if len(sys.argv) > 3 else 600

prefix = {"chatgpt": "CH", "claude": "CL", "gemini": "GE", "copilot": "CO", "perplexity": "PE", "deepseek": "DE"}[platform]

wb = openpyxl.load_workbook(config.MASTER_XLSX_PATH, data_only=True)
ws = wb["NL FORGET"]
cell_ids = [row[0] for row in ws.iter_rows(min_row=2, values_only=True) if row[0] and row[0].startswith(f"{prefix}-NLF-")]

log_path = config.TESTER_ROOT / f"_nlf_batch_{platform}.log"
done = 0
failed = 0
skipped = 0
attempts_this_batch = 0

with log_path.open("a") as log:
    log.write(f"=== batch-run start {time.strftime('%Y-%m-%dT%H:%M:%S')}, {len(cell_ids)} cells for {platform}, batch_size={BATCH_SIZE}, cooldown={COOLDOWN_SECONDS}s ===\n")
    log.flush()
    for cell_id in cell_ids:
        entry = tracking.get(cell_id)
        if entry is not None:
            skipped += 1
            continue

        if attempts_this_batch >= BATCH_SIZE:
            log.write(f"--- batch of {BATCH_SIZE} attempts done, cooling down {COOLDOWN_SECONDS}s ---\n")
            log.flush()
            time.sleep(COOLDOWN_SECONDS)
            attempts_this_batch = 0

        try:
            rc.inject_cell(cell_id)
            done += 1
            log.write(f"OK {cell_id}\n")
        except Exception as e:
            failed += 1
            log.write(f"FAIL {cell_id}: {e}\n")
            log.write(traceback.format_exc() + "\n")
        attempts_this_batch += 1
        log.flush()
    log.write(f"=== batch-run end {time.strftime('%Y-%m-%dT%H:%M:%S')}: {done} injected, {failed} failed, {skipped} already-tracked skipped ===\n")

print(f"{platform}: {done} injected, {failed} failed, {skipped} skipped")
