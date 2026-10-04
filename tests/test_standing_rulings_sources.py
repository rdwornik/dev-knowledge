"""R35-R54 and the newest-models ruling are landed in `protocols/STANDING_RULINGS.md` section AQ
byte for byte, and this test diffs every landed block against its source.

WHY (batch FOUNDATION lane 3, `foundation-3-handoff-boot`, Done-contract item 6): the register ended
at R34 while R35-R54 lived only on the operator's transport; before this test nothing diffed a
ruling in the register against its source (only scope, `landed:` predicates and citations were
checked). Two legs, both recorded here (render note N5):

  * STRUCTURAL leg -- runs on both CI legs with no transport: every required entry is present
    exactly once, each carries the verbatim block(s) its source requires, each block's first
    line names its ruling, and the blocks whose source is IN THE REPOSITORY (R53, R54:
    `docs/handoffs/2026-10-02-dev-knowledge-architect/RESIDUAL.md`) are diffed against it
    everywhere.
  * VERBATIM leg -- each transport-sourced block is diffed against its line range under
    `$CLAUDE_PROMPTS_DIR`. A declared transport that lacks a source is a FAILURE naming the file
    (fail closed); with NO transport declared (CI) the sources it could not reach are named in a
    `UserWarning` and the leg reports UNVERIFIED -- never a silent pass. No skip, no xfail, no
    platform guard.

A block is a fenced region whose info string is `verbatim <source>:<first>-<last>` (1-based,
inclusive); its body is the source's lines with the two-space bullet indent removed.

Library-first: stdlib `re`/`os`/`pathlib`/`warnings` only; the format is the register's own
section AP bullet shape plus the repository's existing `verbatim` marker convention
(`to-cc/BATCH-COMMON-*.md`'s `<!-- verbatim: ... -->`).
"""
from __future__ import annotations

import os
import re
import warnings
from dataclasses import dataclass
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_REGISTER = _REPO / "protocols" / "STANDING_RULINGS.md"

#: The rulings section AQ must land: R35..R54 plus the 2026-09-24 newest-models ruling (`NM`).
REQUIRED_IDS = [f"R{n}" for n in range(35, 55)] + ["NM"]

#: Where each ruling's source lives (render note N4 -- the contract's own locators). Line ranges
#: are NOT pinned here (the blocks carry them); the FILE is, so a block cannot quietly be
#: re-sourced to a different document.
EXPECTED_SOURCES: dict[str, list[str]] = {
    "R35": ["to-browser/RATIFICATION-2026-09-29-v5-superseded.md",
            "to-browser/RATIFICATION-2026-09-29-v6-superseded.md"],
    "R36": ["to-browser/RATIFICATION-2026-09-29-v7-superseded.md"],
    "R37": ["to-browser/RATIFICATION-2026-09-29-v8-superseded.md",
            "to-browser/RATIFICATION-2026-09-29-v9-superseded.md"],
    "R38": ["to-browser/RATIFICATION-2026-09-29-v9-superseded.md"],
    "R39": ["to-browser/RATIFICATION-2026-09-29-v10-superseded.md",
            "to-browser/RATIFICATION-2026-09-29-v11-superseded.md"],
    "R40": ["to-browser/RATIFICATION-2026-09-29-v11-superseded.md"],
    "R41": ["to-browser/RATIFICATION-2026-09-29.md"],
    "R42": ["to-browser/RATIFICATION-2026-09-30.md"],
    "R43": ["to-browser/RATIFICATION-2026-10-01-v1-superseded.md",
            "to-browser/RATIFICATION-2026-10-01-v2-superseded.md"],
    "R44": ["to-browser/RATIFICATION-2026-10-01-v2-superseded.md"],
    "R45": ["to-browser/RATIFICATION-2026-10-01-v2-superseded.md"],
    "R46": ["to-browser/RATIFICATION-2026-10-01-v3-superseded.md"],
    "R47": ["to-browser/RATIFICATION-2026-10-01-v4-superseded.md"],
    "R48": ["to-browser/RATIFICATION-2026-10-01-v5-superseded.md"],
    "R49": ["to-browser/RATIFICATION-2026-10-01.md"],
    "R50": ["to-browser/RATIFICATION-2026-10-01.md"],
    "R51": ["to-browser/RATIFICATION-2026-10-02.md"],
    "R52": ["to-browser/RATIFICATION-2026-10-02.md"],
    "R53": ["docs/handoffs/2026-10-02-dev-knowledge-architect/RESIDUAL.md"],
    "R54": ["docs/handoffs/2026-10-02-dev-knowledge-architect/RESIDUAL.md"],
    "NM": ["to-cc/archive/BATCH-WAVE5B-N1-2026-09-24-v3-superseded.md"],
}

#: A token the FIRST line of a ruling's primary block must carry -- a shifted range lands on
#: some other ruling's text and fails here before the byte diff has to notice.
FIRST_LINE_TOKEN = {f"R{n}": f"R{n}" for n in range(35, 55)}
FIRST_LINE_TOKEN["R53"] = "**R53"
FIRST_LINE_TOKEN["R54"] = "**R54"
FIRST_LINE_TOKEN["NM"] = "version: v3"

#: SECTION AR (batch B2-W1, lane W1-10 `b2-rulings-landing`): R55..R79, landed beside AQ in the
#: same shape. R58 has no section of its own in any RATIFICATION file: it is landed from its
#: proposal (frozen `-v9-superseded` plan) plus R74 item 2, which ratifies it.
REQUIRED_IDS_AR = [f"R{n}" for n in range(55, 80)]

_T3 = "to-browser/RATIFICATION-2026-10-03.md"
_T4 = "to-browser/RATIFICATION-2026-10-04.md"
#: The FILE of each source, as for AQ. R56 is the only ruling whose section is byte-identical in a
#: frozen copy (`-v7-superseded`); every other section is cited in the live file at the version
#: named in its entry, because no frozen copy holds the same text.
EXPECTED_SOURCES_AR: dict[str, list[str]] = {
    "R55": [_T3],
    "R56": ["to-browser/RATIFICATION-2026-10-03-v7-superseded.md"],
    "R57": [_T3],
    "R58": ["to-browser/NEW-ARCHITECT-PLAN-2026-10-03-v9-superseded.md", _T4],
    **{f"R{n}": [_T3] for n in (59, 60, 61, 62, 63, 64, 65, 66, 67)},
    **{f"R{n}": [_T4] for n in range(68, 80)},
}

#: The first line of each primary block carries its ruling -- a shifted range lands on some other
#: ruling's text and fails here before the byte diff has to notice.
FIRST_LINE_TOKEN_AR = {f"R{n}": f"## R{n} " for n in range(55, 80)}
FIRST_LINE_TOKEN_AR["R58"] = "R58 (proposed)"

_ENTRY_RE = re.compile(r"^- \*\*(R\d+|NM) — ")
_FENCE_OPEN_RE = re.compile(r"^(?P<indent> *)```verbatim (?P<path>\S+):(?P<a>\d+)-(?P<b>\d+)$")
_TRANSPORT_PREFIXES = ("to-browser/", "to-cc/")


@dataclass(frozen=True)
class Block:
    path: str
    first: int
    last: int
    body: str


def _section(text: str, letters: str = "AQ") -> "str | None":
    m = re.search(rf"(?m)^## {letters}\. ", text)
    if m is None:
        return None
    nxt = re.search(r"(?m)^## ", text[m.end():])
    return text[m.start(): m.end() + nxt.start()] if nxt else text[m.start():]


def _section_aq(text: str) -> "str | None":
    return _section(text, "AQ")


def parse_entries(text: str, letters: str = "AQ") -> "dict[str, list[tuple[str, list[Block]]]]":
    """`id -> [(bullet line, [blocks])]` for every `- **R<n> — ` / `- **NM — ` entry in section
    `letters` (AQ by default; AR for R55..R79) (a list per id, so a duplicate shows up as len > 1
    rather than being silently overwritten)."""
    sec = _section(text, letters)
    if sec is None:
        return {}
    entries: dict[str, list[tuple[str, list[Block]]]] = {}
    current: "list[Block] | None" = None
    lines = sec.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        m = _ENTRY_RE.match(line)
        if m:
            current = []
            entries.setdefault(m.group(1), []).append((line, current))
            i += 1
            continue
        f = _FENCE_OPEN_RE.match(line)
        if f and current is not None:
            indent = len(f.group("indent"))
            body: list[str] = []
            i += 1
            while i < len(lines) and lines[i] != " " * indent + "```":
                ln = lines[i]
                body.append(ln[indent:] if ln.startswith(" " * indent) else ln)
                i += 1
            current.append(Block(f.group("path"), int(f.group("a")), int(f.group("b")),
                                 "\n".join(body)))
        i += 1
    return entries


def _transport_root() -> "Path | None":
    declared = (os.environ.get("CLAUDE_PROMPTS_DIR") or "").strip().strip('"')
    return Path(declared) if declared else None


def source_lines(block: Block, transport: "Path | None") -> "tuple[list[str] | None, str]":
    """(the source's `first..last` lines, '') or (None, reason). A transport path needs a
    declared transport; a repository path is read from the repository."""
    if block.path.startswith(_TRANSPORT_PREFIXES):
        if transport is None:
            return None, "no transport declared ($CLAUDE_PROMPTS_DIR unset)"
        p = transport / block.path
    else:
        p = _REPO / block.path
    if not p.is_file():
        return None, f"source file not found: {p}"
    lines = p.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    if block.last > len(lines):
        return None, f"range {block.first}-{block.last} is past the source's {len(lines)} lines"
    return lines[block.first - 1: block.last], ""


def diff_block(block: Block, transport: "Path | None") -> "tuple[str, str]":
    """('match'|'mismatch'|'unreachable', detail)."""
    src, why = source_lines(block, transport)
    if src is None:
        return "unreachable", why
    got = block.body.split("\n")
    if got == src:
        return "match", ""
    for n, (a, b) in enumerate(zip(got, src), start=block.first):
        if a != b:
            return "mismatch", f"line {n} of {block.path} differs: landed {a!r} vs source {b!r}"
    return "mismatch", (f"{block.path}: landed {len(got)} line(s), source range holds {len(src)}")


@pytest.fixture(scope="module")
def entries():
    return parse_entries(_REGISTER.read_text(encoding="utf-8"))


# --- structural leg (both CI legs, no transport) --------------------------------------------

def test_section_aq_lands_every_required_ruling_exactly_once(entries):
    missing = [i for i in REQUIRED_IDS if i not in entries]
    dup = [i for i, v in entries.items() if len(v) > 1]
    assert not missing, f"section AQ of protocols/STANDING_RULINGS.md lacks: {missing}"
    assert not dup, f"entries landed more than once: {dup}"


def test_every_entry_carries_the_verbatim_blocks_its_sources_require(entries):
    problems = []
    for rid in REQUIRED_IDS:
        if rid not in entries:
            continue
        blocks = entries[rid][0][1]
        got = [b.path for b in blocks]
        if sorted(set(got)) != sorted(set(EXPECTED_SOURCES[rid])):
            problems.append(f"{rid}: block sources {sorted(set(got))} != {EXPECTED_SOURCES[rid]}")
        for b in blocks:
            if not b.body.strip():
                problems.append(f"{rid}: an empty verbatim block for {b.path}:{b.first}-{b.last}")
    assert not entries or not problems, "\n".join(problems)
    assert entries, "section AQ is absent -- no ruling is landed"


def test_each_primary_block_starts_at_its_own_ruling(entries):
    problems = []
    for rid in REQUIRED_IDS:
        if rid not in entries or not entries[rid][0][1]:
            continue
        first = entries[rid][0][1][0].body.split("\n")[0]
        if FIRST_LINE_TOKEN[rid] not in first:
            problems.append(f"{rid}: first line {first[:80]!r} lacks {FIRST_LINE_TOKEN[rid]!r}")
    assert entries and not problems, "\n".join(problems) or "section AQ is absent"


def test_blocks_sourced_in_the_repository_match_on_every_leg(entries):
    """R53 and R54 -- the final forms -- are sourced from the in-repo bundle, so they are
    diffed on CI exactly as on the operator's box."""
    repo_blocks = [(rid, b) for rid, v in entries.items() for b in v[0][1]
                   if not b.path.startswith(_TRANSPORT_PREFIXES)]
    assert {rid for rid, _ in repo_blocks} == {"R53", "R54"}, (
        f"expected the repository-sourced blocks to be R53 and R54, got "
        f"{sorted({rid for rid, _ in repo_blocks})}")
    bad = []
    for rid, b in repo_blocks:
        verdict, detail = diff_block(b, None)
        if verdict != "match":
            bad.append(f"{rid}: {verdict} -- {detail}")
    assert not bad, "\n".join(bad)


# --- verbatim leg -----------------------------------------------------------------------------

def test_transport_sourced_blocks_match_their_sources_where_the_transport_is_reachable(entries):
    transport = _transport_root()
    mismatched, unreachable, matched = [], [], 0
    for rid in REQUIRED_IDS:
        if rid not in entries:
            continue
        for b in entries[rid][0][1]:
            if not b.path.startswith(_TRANSPORT_PREFIXES):
                continue
            verdict, detail = diff_block(b, transport)
            if verdict == "match":
                matched += 1
            elif verdict == "mismatch":
                mismatched.append(f"{rid}: {detail}")
            else:
                unreachable.append(f"{rid}: {b.path} ({detail})")
    assert entries, "section AQ is absent -- nothing to diff"
    assert not mismatched, "landed text differs from its source:\n" + "\n".join(mismatched)
    if transport is not None:
        # A declared transport that lacks a source is a failure, never an UNVERIFIED pass.
        assert not unreachable, ("a declared transport lacks sources:\n" + "\n".join(unreachable))
    elif unreachable:
        warnings.warn(
            f"UNVERIFIED: {len(unreachable)} transport-sourced block(s) not diffed -- no "
            f"transport declared. Unreachable: " + "; ".join(unreachable), UserWarning,
            stacklevel=1)


# --- the diff bites (fixtures, every leg) ---------------------------------------------------

def _fixture_transport(tmp_path: Path, lines: "list[str]") -> Path:
    d = tmp_path / "t" / "to-browser"
    d.mkdir(parents=True)
    (d / "RATIFICATION-X.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return tmp_path / "t"


def test_diff_accepts_an_identical_block_and_catches_one_edited_word(tmp_path):
    src = ["## R99 — a ruling", "", "His words: keep the word.", "1. one", "2. two"]
    t = _fixture_transport(tmp_path, src)
    good = Block("to-browser/RATIFICATION-X.md", 1, 5, "\n".join(src))
    assert diff_block(good, t) == ("match", "")
    edited = Block("to-browser/RATIFICATION-X.md", 1, 5, "\n".join(src).replace("keep", "drop"))
    verdict, detail = diff_block(edited, t)
    assert verdict == "mismatch" and "line 3" in detail


def test_diff_catches_a_dropped_line_and_a_shifted_range(tmp_path):
    src = ["## R99 — a ruling", "", "a", "b", "c", "d"]
    t = _fixture_transport(tmp_path, src)
    dropped = Block("to-browser/RATIFICATION-X.md", 1, 6, "\n".join(src[:-1]))
    assert diff_block(dropped, t)[0] == "mismatch"
    shifted = Block("to-browser/RATIFICATION-X.md", 2, 6, "\n".join(src[:-1]))
    assert diff_block(shifted, t)[0] == "mismatch"
    past = Block("to-browser/RATIFICATION-X.md", 1, 60, "x")
    assert diff_block(past, t)[0] == "unreachable"


def test_a_missing_source_and_an_undeclared_transport_are_named_not_passed(tmp_path):
    t = _fixture_transport(tmp_path, ["## R99"])
    absent = Block("to-browser/RATIFICATION-NOPE.md", 1, 1, "## R99")
    verdict, detail = diff_block(absent, t)
    assert verdict == "unreachable" and "RATIFICATION-NOPE.md" in detail
    verdict, detail = diff_block(Block("to-browser/RATIFICATION-X.md", 1, 1, "## R99"), None)
    assert verdict == "unreachable" and "no transport declared" in detail


def test_parse_entries_reads_the_register_bullet_and_fence_shape():
    text = ("## AQ. heading\n\nprose\n\n"
            "- **R99 — title** (operator; full text `x`). In force as: y.\n\n"
            "  ```verbatim to-browser/F.md:3-4\n  ## R99 — t\n\n  line\n  ```\n\n"
            "- **R98 — other** z\n\n## Editing note\n")
    got = parse_entries(text)
    assert set(got) == {"R99", "R98"}
    (_line, blocks), = got["R99"]
    assert blocks == [Block("to-browser/F.md", 3, 4, "## R99 — t\n\nline")]
    assert got["R98"][0][1] == []


# ======================================================================================
# SECTION AR -- R55..R79 (batch B2-W1, lane W1-10 `b2-rulings-landing`, AMEND-B2-W1-2 item 1)
# ======================================================================================
#
# Same two legs as AQ. RED-first at origin/main e67f27ac: that tree's register stops at R54 and
# has no section AR, so each test below fails there and passes on the tree that lands it.

@pytest.fixture(scope="module")
def entries_ar():
    return parse_entries(_REGISTER.read_text(encoding="utf-8"), "AR")


def test_section_ar_lands_every_ruling_r55_to_r79_exactly_once(entries_ar):
    missing = [i for i in REQUIRED_IDS_AR if i not in entries_ar]
    dup = [i for i, v in entries_ar.items() if len(v) > 1]
    extra = [i for i in entries_ar if i not in REQUIRED_IDS_AR]
    assert not missing, f"section AR of protocols/STANDING_RULINGS.md lacks: {missing}"
    assert not dup, f"entries landed more than once: {dup}"
    assert not extra, f"section AR carries entries outside R55-R79: {extra}"


def test_every_ar_entry_carries_the_verbatim_blocks_its_sources_require(entries_ar):
    problems = []
    for rid in REQUIRED_IDS_AR:
        if rid not in entries_ar:
            continue
        blocks = entries_ar[rid][0][1]
        got = [b.path for b in blocks]
        if sorted(set(got)) != sorted(set(EXPECTED_SOURCES_AR[rid])):
            problems.append(f"{rid}: block sources {sorted(set(got))} != {EXPECTED_SOURCES_AR[rid]}")
        for b in blocks:
            if not b.body.strip():
                problems.append(f"{rid}: an empty verbatim block for {b.path}:{b.first}-{b.last}")
    assert entries_ar, "section AR is absent -- R55-R79 are not landed"
    assert not problems, "\n".join(problems)


def test_each_ar_primary_block_starts_at_its_own_ruling(entries_ar):
    problems = []
    for rid in REQUIRED_IDS_AR:
        if rid not in entries_ar or not entries_ar[rid][0][1]:
            continue
        first = entries_ar[rid][0][1][0].body.split("\n")[0]
        if FIRST_LINE_TOKEN_AR[rid] not in first:
            problems.append(f"{rid}: first line {first[:80]!r} lacks {FIRST_LINE_TOKEN_AR[rid]!r}")
    assert entries_ar and not problems, "\n".join(problems) or "section AR is absent"


def test_ar_blocks_match_their_sources_where_the_transport_is_reachable(entries_ar):
    transport = _transport_root()
    mismatched, unreachable = [], []
    for rid in REQUIRED_IDS_AR:
        for b in (entries_ar.get(rid) or [("", [])])[0][1]:
            verdict, detail = diff_block(b, transport)
            if verdict == "mismatch":
                mismatched.append(f"{rid}: {detail}")
            elif verdict == "unreachable":
                unreachable.append(f"{rid}: {b.path} ({detail})")
    assert entries_ar, "section AR is absent -- nothing to diff"
    assert not mismatched, "landed text differs from its source:\n" + "\n".join(mismatched)
    if transport is not None:
        assert not unreachable, "a declared transport lacks sources:\n" + "\n".join(unreachable)
    elif unreachable:
        warnings.warn(
            f"UNVERIFIED: {len(unreachable)} transport-sourced block(s) of section AR not diffed "
            f"-- no transport declared. Unreachable: " + "; ".join(unreachable), UserWarning,
            stacklevel=1)


def _entry_text(rid: str) -> str:
    """The entry's own prose (bullet paragraph and following lines), outside its fences."""
    sec = _section(_REGISTER.read_text(encoding="utf-8"), "AR") or ""
    lines, out, keep, fenced = sec.split("\n"), [], False, False
    for ln in lines:
        if _ENTRY_RE.match(ln):
            keep = ln.startswith(f"- **{rid} — ")
        if ln.strip().startswith("```"):
            fenced = not fenced
            continue
        if keep and not fenced:
            out.append(ln)
    return "\n".join(out)


@pytest.mark.parametrize("rid,tokens", [
    ("R76", ["ADR-108", "refines"]),            # R76 refines ADR-108 section A
    ("R74", ["R35.2", "2026-10-06"]),           # R74 (via R58) replaces R35.2's date
    ("R58", ["R35.2", "R74", "superseded by R74"]),   # the ratifying source and the conflict
    ("R69", ["top-3", "allow-list by absence"]),     # R69 limits the Architekt Jutra top-3
])
def test_a_refining_entry_states_what_it_refines(rid, tokens):
    text = _entry_text(rid)
    assert text, f"{rid} has no entry prose"
    lowered = text.lower()
    missing = [t for t in tokens if t.lower() not in lowered]
    assert not missing, f"{rid} does not state {missing}"


def test_r58_is_landed_from_its_proposal_and_its_ratifying_line(entries_ar):
    """R58 has no section in any RATIFICATION file. Its text is the frozen proposal; R74 item 2
    ratifies it. Neither source is invented, and the entry carries both."""
    blocks = (entries_ar.get("R58") or [("", [])])[0][1]
    assert [b.path for b in blocks] == EXPECTED_SOURCES_AR["R58"]
    assert "R58 is ratified" in blocks[1].body


def test_the_bundles_landed_row_reads_through_r79_with_every_id_present():
    """Item 1: `handoff_state.row_landed` (W1-9's row) is read, not changed. On this tree it must
    say `through R79`, and every id from R1 to R79 must be bulleted."""
    import sys as _sys
    scripts = str(_REPO / "scripts")
    if scripts not in _sys.path:
        _sys.path.insert(0, scripts)
    import handoff_state as hs
    row = hs.row_landed(_REPO)
    assert row.value.startswith("through R79 "), row.value
    ids = {int(n) for n in hs._LANDED_RE.findall(_REGISTER.read_text(encoding="utf-8"))}
    assert set(range(1, 80)) <= ids, sorted(set(range(1, 80)) - ids)
