"""Quick-review feature on top of the per-cell transcript/screenshot
capture in run_cell.py: reads whatever's under
tester/transcripts/<platform>/<cell_id>/{json,screenshots}/ and
markdownifies it into one REPORT.md per platform, so a reviewer can
scroll one document per platform instead of opening dozens of individual
JSON/PNG files. On-demand -- rerun anytime after new cells have been
run; it doesn't regenerate automatically on every inject/erase/recall
call.

Usage:
    python generate_platform_reports.py            # all platforms
    python generate_platform_reports.py claude      # just one
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import config

# Matches run_cell.py's phase-file naming (01_inject, 02_erase,
# 03_recall_same_session, 04_recall_cross_session) so reports render in
# chronological order regardless of directory-listing order.
PHASE_ORDER = ["01_inject", "02_erase", "03_recall_same_session", "04_recall_cross_session"]
PHASE_TITLES = {
    "01_inject": "Inject",
    "02_erase": "Erase",
    "03_recall_same_session": "Recall -- same session",
    "04_recall_cross_session": "Recall -- cross session",
}


# Fields that hold a platform's read_memory_settings() output verbatim
# (run_cell.py's _run_recall_probes()/_verify_file_injection()) -- these
# are full page.inner_text("body")-style dumps (sidebar nav, the
# conversation sitting behind the settings overlay, model/footer chrome)
# with the actual memory panel content appended last in DOM order, not a
# normal chat reply. The raw JSON keeps the full dump for audit purposes;
# only the report rendering trims it.
MEMORY_DUMP_FIELDS = {"r2_reply", "memory_settings_reply", "memory_settings_reply_after_forced"}


def _extract_memory_section(text: str) -> str:
    """Anchors on the last line that's exactly a "Memory" heading and
    keeps only what follows -- confirmed live against Claude's settings
    dialog (2026-08-28): the nav sidebar has "Memory" as a link/heading
    too, but the actual panel heading ("Memory\\nGenerate memory from
    chats...") is always the *last* such line since the dialog is
    appended after the page it's covering. Falls back to the full text
    unchanged if no such line is found, rather than guessing -- a
    different platform's dump (or a genuinely empty memory panel) is
    better shown whole than silently mangled."""
    lines = text.splitlines()
    anchor = None
    for i, line in enumerate(lines):
        if line.strip() == "Memory":
            anchor = i
    if anchor is None:
        return text
    return "\n".join(lines[anchor:]).strip()


def _render_fields(data: dict) -> str:
    """Generic key -> value renderer -- inject/erase/recall JSON shapes
    differ (chat-based vs. field-based injection, FILE-substudy
    verification, recall probes), so this doesn't hardcode field names,
    it just renders whatever's actually in the dict. The exception is
    MEMORY_DUMP_FIELDS, trimmed to just the relevant memory-panel section
    so a reviewer isn't scrolling past sidebar nav to find it."""
    lines = []
    for key, value in data.items():
        lines.append(f"**{key}**")
        if value is None:
            lines.append("*(not applicable)*")
        else:
            text = str(value)
            if key in MEMORY_DUMP_FIELDS:
                text = _extract_memory_section(text)
            # Blockquote every line so multi-paragraph replies render
            # cleanly instead of collapsing into one run-on line.
            quoted = "\n".join(f"> {line}" for line in text.splitlines()) or "> *(empty)*"
            lines.append(quoted)
        lines.append("")
    return "\n".join(lines)


def _render_phase(cell_dir: Path, phase: str) -> str:
    json_path = cell_dir / "json" / f"{phase}.json"
    shots_dir = cell_dir / "screenshots"
    if not json_path.exists():
        return ""

    data = json.loads(json_path.read_text())
    lines = [f"#### {PHASE_TITLES[phase]}", ""]
    lines.append(_render_fields(data))

    # Pick up every screenshot whose filename starts with this phase's
    # prefix -- handles both the single fixed-name case (01_inject.png,
    # 02_erase.png) and recall's variable set (some probes conditional:
    # r1_choice only if the open question needed a follow-up, r2 only if
    # HAS_MEMORY_UI) without assuming which ones exist.
    shots = sorted(shots_dir.glob(f"{phase}*.png")) if shots_dir.exists() else []
    for shot in shots:
        rel = f"screenshots/{shot.name}"
        lines.append(f"![{shot.stem}]({rel})")
        lines.append("")

    return "\n".join(lines)


def _render_cell(cell_dir: Path) -> str:
    cell_id = cell_dir.name
    lines = [f"### {cell_id}", ""]
    any_phase = False
    for phase in PHASE_ORDER:
        rendered = _render_phase(cell_dir, phase)
        if rendered:
            any_phase = True
            lines.append(rendered)
    if not any_phase:
        lines.append("*(no recorded phases yet)*")
        lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def generate_report(platform: str) -> Path | None:
    platform_dir = config.TRANSCRIPTS_DIR / platform
    if not platform_dir.exists():
        return None

    cell_dirs = sorted(d for d in platform_dir.iterdir() if d.is_dir())
    if not cell_dirs:
        return None

    lines = [f"# {platform} -- cell run report", ""]
    lines.append(f"{len(cell_dirs)} cell(s) with recorded evidence.")
    lines.append("")
    for cell_dir in cell_dirs:
        lines.append(_render_cell(cell_dir))

    report_path = platform_dir / "REPORT.md"
    report_path.write_text("\n".join(lines))
    return report_path


def main() -> None:
    platforms = sys.argv[1:] or list(config.PLATFORMS.keys())
    for platform in platforms:
        path = generate_report(platform)
        if path:
            print(f"{platform}: wrote {path}")
        else:
            print(f"{platform}: nothing under {config.TRANSCRIPTS_DIR / platform} yet, skipped")


if __name__ == "__main__":
    main()
