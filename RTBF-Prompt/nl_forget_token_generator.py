"""Generates 270 NEW token/anchor(referent) pairs for the professor's
NL-forget-prompt phrasing factorial sub-study (Location x Extent x Form x
Tone x Verb design -- see Compare/First Pass/formal_comparison.md and
PROJECT_STATUS.md's "Progress 2026-08-26" section for the prior, now
superseded, 1-3-fixed-prompt decision).

Explicitly separate from the existing 88-cell battery's token/anchor pool
-- nothing here reads-to-modify or overwrites `token.md`,
`data/token_assignment.csv`, or `data/RTBF Experiments.xlsx`. Both new
pools are required to be disjoint from the existing assignment because the
new sub-study's cells are expected to run on the SAME reused accounts as
the existing battery (accounts-may-be-reused policy, PROJECT_STATUS.md
2026-08-26) -- a collision with an already-injected referent or token
would make that cell's R3 indirect-recall probe ambiguous between the old
cell and the new one, and could read as contaminating a cell that's
already run. Generating disjoint pools up front is what avoids that,
independent of however the platform/cell-ID scoping questions get
resolved later.

TOKENS: continues the exact same seeded draw as token_generator.py (same
EFF wordlist, same noun filter, same category exclusion, same denylist,
same SEED) past its existing N_TOKENS=250 cutoff (88 assigned + 162
reserve), taking indices [250:520) as the new 270. This is a deterministic
continuation of one unbroken sampling-without-replacement stream --
collision with the existing 250 is impossible by construction, not just
unlikely. token_generator.py is imported for its pure word-pool/filtering
functions only; it is never modified and none of its write functions are
called.

REFERENTS: 270 new naturalistic, non-sensitive conversational referent
phrases in the same register as token_generator.py's REFERENTS list
(ordinary things a person might casually mention in chat -- hobbies,
pets, home projects, collections, etc.), built from curated noun banks
disjoint in content from the existing 100-entry list, combined with a
small set of natural carrier templates, deduplicated against the existing
list (exact match) and against themselves, then deterministically sampled
down to 270 (same SEED-based reproducibility principle as the token
draw).

Output (new files only):
- `nl_forget_tokens.md` (human-readable, this directory)
- `data/nl_forget_token_assignment.csv` (machine-readable)

This script only generates the 270 (referent, token) pairs as a flat,
unassigned pool. It deliberately does NOT assign them to specific cell
IDs, platforms, or factorial conditions (Location/Extent/Form/Tone/Verb
combinations / the actual erasure-request text) -- those depend on open
scoping questions (full 270 vs. a fractioned subset, which platform(s),
additive vs. replacing the 13 existing blocked MASTER cells, see
[[project_nl_forget_prompt_substudy_planned]] memory) that are not yet
resolved.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

from token_generator import (
    REFERENTS as EXISTING_REFERENTS,
    N_TOKENS as EXISTING_N_TOKENS,
    SEED as EXISTING_TOKEN_SEED,
    WORDLIST_PATH,
    build_token_pool,
    filter_denylist,
    filter_excluded_categories,
    filter_to_nouns,
    load_wordlist,
    token,
)

REPO_ROOT = Path(__file__).parent
OUT_MD_PATH = REPO_ROOT / "nl_forget_tokens.md"
OUT_CSV_PATH = REPO_ROOT / "data" / "nl_forget_token_assignment.csv"

N_NEW_PAIRS = 270
REFERENT_SEED = 20260907  # date this sub-study's pool was generated

# ---------------------------------------------------------------------------
# TOKENS -- continue the existing seeded draw past its current cutoff.
# ---------------------------------------------------------------------------


def build_new_tokens() -> list[tuple[str, ...]]:
    raw_words = load_wordlist(WORDLIST_PATH)
    nouns = filter_to_nouns(raw_words)
    categorized = filter_excluded_categories(nouns)
    words = filter_denylist(categorized)

    extended_n = EXISTING_N_TOKENS + N_NEW_PAIRS  # 250 + 270 = 520
    full_pool = build_token_pool(words, EXISTING_TOKEN_SEED, extended_n)

    # Sanity check: the first EXISTING_N_TOKENS entries must be byte-for-byte
    # identical to what token_generator.py itself produces, proving this
    # draw is a pure continuation, not a re-derivation that could collide.
    original_pool = build_token_pool(words, EXISTING_TOKEN_SEED, EXISTING_N_TOKENS)
    assert full_pool[:EXISTING_N_TOKENS] == original_pool, (
        "extended draw diverged from the original pool's prefix -- "
        "this would risk colliding with an already-assigned token"
    )

    new_tokens = full_pool[EXISTING_N_TOKENS:]
    assert len(new_tokens) == N_NEW_PAIRS
    assert len(set(new_tokens) & set(original_pool)) == 0
    return new_tokens


# ---------------------------------------------------------------------------
# REFERENTS -- new curated noun banks, disjoint in content from the
# existing REFERENTS list, combined with natural carrier templates.
# ---------------------------------------------------------------------------

# Concrete objects/possessions -- pairs naturally with "a new X" / "my X" /
# "our X" style templates.
OBJECT_NOUNS = [
    "espresso machine", "cast iron skillet", "record player", "film camera",
    "pottery wheel", "sewing machine", "leather wallet I made", "hiking backpack",
    "climbing harness", "kayak paddle", "longboard", "unicycle", "ukulele",
    "harmonica", "banjo", "violin I'm learning", "digital piano", "drum kit",
    "telescope", "weather station", "ham radio", "mechanical keyboard",
    "retro game console", "synthesizer", "raspberry pi cluster", "3D pen",
    "embroidery hoop", "loom", "letterpress kit", "calligraphy pen set",
    "watercolor palette", "airbrush kit", "woodburning tool", "chisel set",
    "welding rig", "lathe", "drone", "action camera", "binoculars",
    "field journal", "compass I inherited", "pocket knife I restored",
    "fountain pen collection", "typewriter", "rotary phone", "gramophone",
    "antique clock", "grandfather clock", "wind chime I built",
    "birdhouse kit", "beehive frame", "chicken coop feeder", "rain gauge",
    "sundial", "hammock chair", "porch swing", "fire pit grate",
    "smoker box", "pizza stone", "waffle iron", "ice cream maker",
    "bread machine", "stand mixer", "pasta roller", "mandoline",
    "mortar and pestle", "tea set", "coffee grinder", "cold brew tower",
    "kombucha SCOBY", "fermentation crock", "cheese press", "canning rack",
    "spice grinder", "knife roll", "cutting board I made",
    "surfboard", "wetsuit", "fishing rod", "tackle box", "canoe paddle",
    "camping stove", "tent I'm patching", "sleeping bag", "trekking poles",
    "snowshoes", "cross-country skis", "ice skates", "roller skates",
    "skateboard deck", "bike helmet", "cycling jersey", "bike lock",
    "car stereo", "dashcam", "toolbox", "workbench", "pegboard",
    "sawhorse", "shop vac", "air compressor", "drill press",
]

# Ongoing activities/projects -- pairs naturally with "a X I'm working on" /
# "a X I started" / "our X" / "a X project" style templates.
PROJECT_NOUNS = [
    "kitchen backsplash", "bathroom retile", "closet remodel", "attic cleanout",
    "basement conversion", "garage reorganization", "garden shed build",
    "greenhouse kit", "chicken coop", "rain barrel system", "compost setup",
    "raised bed layout", "pergola build", "deck resurfacing", "fence repair",
    "mailbox rebuild", "porch railing", "gutter cleanout", "driveway resurfacing",
    "solar panel install", "home battery setup", "smart thermostat install",
    "security camera setup", "home network rewiring", "server rack build",
    "podcast setup", "streaming setup", "video editing workflow",
    "photography portfolio", "short film", "stop-motion animation",
    "comic strip", "graphic novel", "screenplay", "short story collection",
    "poetry chapbook", "family cookbook", "recipe blog", "sourdough log",
    "spice inventory", "wine cellar organization", "beer cellar rotation",
    "cocktail menu", "meal-prep rotation", "grocery budget tracker",
    "family tree research", "genealogy scrapbook", "photo restoration project",
    "home movie digitization", "vinyl digitization project",
    "language learning streak", "handwriting practice log", "sign language course",
    "sourdough starter", "kimchi batch", "hot sauce ferment", "pickle crock",
    "jam canning run", "maple syrup tap", "beekeeping log", "worm bin",
    "aquaponics setup", "hydroponic tower", "bonsai training",
    "orchid propagation", "succulent propagation", "seed-starting tray",
    "wildflower patch", "pollinator garden", "rain garden", "xeriscape yard",
    "trellis build", "arbor build", "fire pit patio", "outdoor kitchen",
    "treehouse build", "playhouse build", "sandbox build", "swing set assembly",
    "half-pipe build", "climbing wall install", "home gym buildout",
    "yoga studio setup", "meditation corner", "reading nook build",
    "library cataloging project", "board game night rotation",
    "trivia night prep", "escape room build", "puzzle swap",
    "geocaching route", "letterboxing hunt", "birding life list",
    "star chart project", "astrophotography setup", "weather logging habit",
]

# KNOWN BUG, found 2026-09-11 (not fixed here -- the 270-pool is already
# generated/live and shouldn't be reshuffled; patched by hand instead in
# data/nl_forget_token_assignment.csv + nl_forget_tokens.md for the 3
# affected rows, pool_index 40/104/237): some OBJECT_NOUNS entries already
# carry their own relative clause ("pocket knife I restored", "cutting
# board I made", "violin I'm learning"), and the last two templates below
# append a SECOND clause on top, producing a double-clause referent like
# "a pocket knife I restored I picked up secondhand". If this pool is ever
# regenerated or extended past 270, fix by either stripping OBJECT_NOUNS
# entries that already contain "I " before combining with these two
# templates, or building a separate noun sub-list for them.
CARRIER_TEMPLATES_OBJECT = [
    "a new {n}",
    "my {n}",
    "our {n}",
    "{article} {n} I just got",
    "{article} {n} I picked up secondhand",
]

CARRIER_TEMPLATES_PROJECT = [
    "{article} {n} I'm working on",
    "{article} {n} I started",
    "our {n}",
    "{article} {n} I've been planning",
    "{article} {n} project",
]

_VOWEL_SOUND_START = ("a", "e", "i", "o", "u")


def _article(n: str) -> str:
    return "an" if n[0].lower() in _VOWEL_SOUND_START else "a"


def build_new_referents() -> list[str]:
    existing = set(EXISTING_REFERENTS)
    candidates: list[str] = []

    for n in OBJECT_NOUNS:
        for tmpl in CARRIER_TEMPLATES_OBJECT:
            candidates.append(tmpl.format(n=n, article=_article(n)))
    for n in PROJECT_NOUNS:
        for tmpl in CARRIER_TEMPLATES_PROJECT:
            candidates.append(tmpl.format(n=n, article=_article(n)))

    # Drop anything that collides with the existing 100-entry list (exact
    # match) and any accidental duplicate produced by the templating itself.
    seen: set[str] = set()
    deduped: list[str] = []
    for c in candidates:
        if c in existing or c in seen:
            continue
        seen.add(c)
        deduped.append(c)

    if len(deduped) < N_NEW_PAIRS:
        raise RuntimeError(
            f"only {len(deduped)} candidate referents after dedup, need {N_NEW_PAIRS} "
            "-- expand OBJECT_NOUNS/PROJECT_NOUNS"
        )

    rng = random.Random(REFERENT_SEED)
    rng.shuffle(deduped)
    return deduped[:N_NEW_PAIRS]


# ---------------------------------------------------------------------------


def main() -> None:
    new_tokens = build_new_tokens()
    new_referents = build_new_referents()

    assert len(new_tokens) == len(new_referents) == N_NEW_PAIRS

    rows = []
    for i in range(N_NEW_PAIRS):
        tok_str = token(new_tokens[i])
        rows.append(
            {
                "pool_index": i + 1,
                "referent": new_referents[i],
                "token": tok_str,
                "token_length": len(new_tokens[i]),
            }
        )

    with OUT_CSV_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["pool_index", "referent", "token", "token_length"])
        writer.writeheader()
        writer.writerows(rows)

    lines = []
    lines.append("# NL-Forget Factorial Sub-Study -- New Token/Anchor Pool (270)")
    lines.append("")
    lines.append(
        "Generated by `nl_forget_token_generator.py`. 270 new (referent, "
        "token) pairs, entirely disjoint from the existing 88-cell "
        "battery's pool (`token.md` / `data/token_assignment.csv` / "
        "`data/RTBF Experiments.xlsx` -- none of those files were read "
        "for writing or modified by this script). Tokens continue the "
        "same seeded draw as `token_generator.py` past its existing "
        f"cutoff ({EXISTING_N_TOKENS}), so collision with an "
        "already-assigned or already-reserved token is impossible by "
        "construction. Referents are newly authored (own noun banks, "
        "disjoint in content from the existing REFERENTS list), "
        "deduplicated against the existing list, and deterministically "
        "sampled (seed documented in the script)."
    )
    lines.append("")
    lines.append(
        "**Not yet assigned** to specific cell IDs, platforms, or "
        "factorial conditions (Location/Extent/Form/Tone/Verb "
        "combinations) -- this is a flat, unassigned pool of 270 pairs, "
        "ready to be drawn from once the open scoping questions (full 270 "
        "vs. a fractioned subset, which platform(s), additive vs. "
        "replacing the 13 existing blocked MASTER cells, account-sharing "
        "policy) are resolved."
    )
    lines.append("")
    lines.append("| # | Referent | Token | Token length |")
    lines.append("|---|---|---|---|")
    for r in rows:
        lines.append(f"| {r['pool_index']} | {r['referent']} | {r['token']} | {r['token_length']} |")

    OUT_MD_PATH.write_text("\n".join(lines) + "\n")

    print(f"Wrote {len(rows)} new (referent, token) pairs")
    print(f"  -> {OUT_MD_PATH}")
    print(f"  -> {OUT_CSV_PATH}")
    print("\nFirst 8:")
    for r in rows[:8]:
        print(f"  {r['referent']!r} -> {r['token']!r}")


if __name__ == "__main__":
    main()
