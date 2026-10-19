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

#: SECTION AS (batch B2-W2, lane 6 `b2w2-rulings-landing`, row [#1446]): R80..R92, landed beside AR
#: in the same shape. R81.3 is a sub-ruling with its own heading and lands inside R81's entry.
REQUIRED_IDS_AS = [f"R{n}" for n in range(80, 93)]

_T5 = "to-browser/RATIFICATION-2026-10-05.md"
_T6 = "to-browser/RATIFICATION-2026-10-06.md"
_T8 = "to-browser/RATIFICATION-2026-10-08.md"
_T9 = "to-browser/RATIFICATION-2026-10-09.md"
#: The FILE of each source, as for AQ and AR; the live files are rewritten in place, so a range is
#: valid for the version each entry names (the 10-05 file is v5, the 10-08 file is v2).
EXPECTED_SOURCES_AS: dict[str, list[str]] = {
    **{f"R{n}": [_T5] for n in range(80, 87)},
    **{f"R{n}": [_T6] for n in (87, 88, 89)},
    **{f"R{n}": [_T8] for n in (90, 91)},
    "R92": [_T9],
}
FIRST_LINE_TOKEN_AS = {f"R{n}": f"## R{n} " for n in range(80, 93)}

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


def test_the_bundles_landed_row_reads_through_r136_with_every_id_present():
    """Item 1: `handoff_state.row_landed` (W1-9's row) is read, not changed. On this tree it says
    `through R147` (sections AV and AW, batch E1 lane `e1-rows`, extend section AU's R115;
    section AX, batch E2.0 lane `e2-rulings`, lands R137-R147), and every id from R1 to R147
    is bulleted except R103, which was never ruled (section AU). The test name keeps `r136`
    so the integrator's node id stays the same across the pin move."""
    import sys as _sys
    scripts = str(_REPO / "scripts")
    if scripts not in _sys.path:
        _sys.path.insert(0, scripts)
    import handoff_state as hs
    row = hs.row_landed(_REPO)
    assert row.value.startswith("through R147 "), row.value
    ids = {int(n) for n in hs._LANDED_RE.findall(_REGISTER.read_text(encoding="utf-8"))}
    want = set(range(1, 148)) - {103}
    assert want <= ids, sorted(want - ids)
    assert 103 not in ids


# ======================================================================================
# SECTION AS -- R80..R92 (batch B2-W2, lane 6 `b2w2-rulings-landing`, row [#1446])
# ======================================================================================
#
# Same two legs as AQ and AR, plus the gate they exist for: `decision_coverage.py rulings` read
# with a simulated B2-W2 close. RED-first at origin/main 03d21ff8: that tree's register stops at
# R79, so the gate refuses R80..R86 the moment a second batch has closed after 2026-10-05, and
# every test below that reads section AS fails there.

@pytest.fixture(scope="module")
def entries_as():
    return parse_entries(_REGISTER.read_text(encoding="utf-8"), "AS")


def test_section_as_lands_every_ruling_r80_to_r92_exactly_once(entries_as):
    missing = [i for i in REQUIRED_IDS_AS if i not in entries_as]
    dup = [i for i, v in entries_as.items() if len(v) > 1]
    extra = [i for i in entries_as if i not in REQUIRED_IDS_AS]
    assert not missing, f"section AS of protocols/STANDING_RULINGS.md lacks: {missing}"
    assert not dup, f"entries landed more than once: {dup}"
    assert not extra, f"section AS carries entries outside R80-R92: {extra}"


def test_every_as_entry_carries_the_verbatim_blocks_its_sources_require(entries_as):
    problems = []
    for rid in REQUIRED_IDS_AS:
        if rid not in entries_as:
            continue
        blocks = entries_as[rid][0][1]
        got = [b.path for b in blocks]
        if sorted(set(got)) != sorted(set(EXPECTED_SOURCES_AS[rid])):
            problems.append(f"{rid}: block sources {sorted(set(got))} != {EXPECTED_SOURCES_AS[rid]}")
        for b in blocks:
            if not b.body.strip():
                problems.append(f"{rid}: an empty verbatim block for {b.path}:{b.first}-{b.last}")
    assert entries_as, "section AS is absent -- R80-R92 are not landed"
    assert not problems, "\n".join(problems)


def test_each_as_primary_block_starts_at_its_own_ruling(entries_as):
    problems = []
    for rid in REQUIRED_IDS_AS:
        if rid not in entries_as or not entries_as[rid][0][1]:
            continue
        first = entries_as[rid][0][1][0].body.split("\n")[0]
        if FIRST_LINE_TOKEN_AS[rid] not in first:
            problems.append(f"{rid}: first line {first[:80]!r} lacks {FIRST_LINE_TOKEN_AS[rid]!r}")
    assert entries_as and not problems, "\n".join(problems) or "section AS is absent"


def test_r81_3_lands_inside_r81s_entry_as_its_second_block(entries_as):
    """R81.3 has its own heading in the 2026-10-05 file and is a sub-ruling of R81: it is not a
    register id of its own, so its text is R81's second block."""
    blocks = (entries_as.get("R81") or [("", [])])[0][1]
    assert [b.body.split("\n")[0][:11] for b in blocks] == ["## R81 — mu", "## R81.3 — "]
    assert "R81.3" not in entries_as


def test_as_blocks_match_their_sources_where_the_transport_is_reachable(entries_as):
    transport = _transport_root()
    mismatched, unreachable = [], []
    for rid in REQUIRED_IDS_AS:
        for b in (entries_as.get(rid) or [("", [])])[0][1]:
            verdict, detail = diff_block(b, transport)
            if verdict == "mismatch":
                mismatched.append(f"{rid}: {detail}")
            elif verdict == "unreachable":
                unreachable.append(f"{rid}: {b.path} ({detail})")
    assert entries_as, "section AS is absent -- nothing to diff"
    assert not mismatched, "landed text differs from its source:\n" + "\n".join(mismatched)
    if transport is not None:
        assert not unreachable, "a declared transport lacks sources:\n" + "\n".join(unreachable)
    elif unreachable:
        warnings.warn(
            f"UNVERIFIED: {len(unreachable)} transport-sourced block(s) of section AS not diffed "
            f"-- no transport declared. Unreachable: " + "; ".join(unreachable), UserWarning,
            stacklevel=1)


# --- the gate section AS exists for ----------------------------------------------------------

_AS_FILE_DATES = {_T5: "2026-10-05", _T6: "2026-10-06", _T8: "2026-10-08", _T9: "2026-10-09"}


def _decision_coverage():
    import sys as _sys
    scripts = str(_REPO / "scripts")
    if scripts not in _sys.path:
        _sys.path.insert(0, scripts)
    import decision_coverage as dc
    return dc


def _as_transport(tmp_path: Path, *, b2_w2_closed: bool) -> Path:
    """A transport holding the four RATIFICATION files of R80..R92 (headings only, dated as the
    live files are) and the batch clock as it stands: B2-W1 CLOSED 2026-10-06, and B2-W2 CLOSED
    when asked -- the simulated close."""
    folder = tmp_path / "t" / "to-browser"
    folder.mkdir(parents=True)
    for path, day in _AS_FILE_DATES.items():
        ids = [r for r in REQUIRED_IDS_AS if EXPECTED_SOURCES_AS[r] == [path]]
        head = f"carried-by: OPEN\nkind: RATIFICATION\ndate: {day}\n\n# RATIFICATION - {day}\n\n"
        body = "\n\n".join(f"## {r} — a ruling" for r in ids)
        (folder / Path(path).name).write_text(head + body + "\n", encoding="utf-8", newline="\n")
    (folder / "STATE-BATCH-B2-W1.md").write_text("CLOSED 2026-10-06T15:51Z\n", encoding="utf-8")
    if b2_w2_closed:
        (folder / "STATE-BATCH-B2-W2.md").write_text("CLOSED 2026-10-09T23:59Z\n", encoding="utf-8")
    return tmp_path / "t"


def _repo_without_section_as(tmp_path: Path) -> Path:
    """A copy of the register without section AS -- the tree at 03d21ff8 -- and the task rows."""
    import shutil
    root = tmp_path / "repo"
    (root / "protocols").mkdir(parents=True)
    text = _REGISTER.read_text(encoding="utf-8")
    start, end = text.index("## AS. "), text.index("## Editing note")
    (root / "protocols" / "STANDING_RULINGS.md").write_text(
        text[:start] + text[end:], encoding="utf-8", newline="\n")
    shutil.copytree(_REPO / "tasks", root / "tasks")
    return root


def test_the_gate_refuses_r80_to_r86_without_section_as_once_b2_w2_reads_closed(tmp_path):
    """The RED-first witness (Done-contract item 3), kept as a test: the register as it stood at
    03d21ff8 refuses exactly R80..R86 under a simulated B2-W2 close, and the same tree is clean
    before that close -- so the clock, not a quirk of the fixture, arms the refusal."""
    dc = _decision_coverage()
    bare = _repo_without_section_as(tmp_path)
    closed = dc.rulings_report(bare, transport=_as_transport(tmp_path / "a", b2_w2_closed=True))
    assert closed.unlanded is not dc.UNMEASURED
    assert sorted(f.subject for f in closed.unlanded) == [f"R{n}" for n in range(80, 87)]
    assert not closed.passed
    open_ = dc.rulings_report(bare, transport=_as_transport(tmp_path / "b", b2_w2_closed=False))
    assert open_.unlanded == []


def test_the_gate_passes_with_section_as_under_a_simulated_b2_w2_close(tmp_path):
    """Done-contract item 2: `decision_coverage.py rulings` reports 0 unlanded with B2-W2 CLOSED,
    all thirteen rulings read, and every landed entry carried (the carried leg is not weakened)."""
    dc = _decision_coverage()
    report = dc.rulings_report(_REPO, transport=_as_transport(tmp_path, b2_w2_closed=True))
    assert report.unlanded is not dc.UNMEASURED
    assert report.rulings_read == len(REQUIRED_IDS_AS)
    assert report.unlanded == [], [f.subject for f in report.unlanded]
    assert report.uncarried == [], [f.subject for f in report.uncarried]
    assert report.passed


def test_the_gate_passes_on_the_live_ratification_files_under_a_simulated_b2_w2_close(tmp_path):
    """The same close, read against the operator's real RATIFICATION files wherever the transport
    is reachable; with none declared the leg is named UNVERIFIED, never passed in silence."""
    import shutil
    transport = _transport_root()
    if transport is None or not (transport / "to-browser").is_dir():
        warnings.warn("UNVERIFIED: the simulated B2-W2 close was not read against the live "
                      "RATIFICATION files -- no transport declared.", UserWarning, stacklevel=1)
        return
    dc = _decision_coverage()
    sim = tmp_path / "t" / "to-browser"
    sim.mkdir(parents=True)
    for prefix in ("RATIFICATION-", "STATE-BATCH-"):
        for src in (transport / "to-browser").glob(f"{prefix}*.md"):
            shutil.copy2(src, sim / src.name)
    (sim / "STATE-BATCH-B2-W2.md").write_text("CLOSED 2026-10-09T23:59Z\n", encoding="utf-8")
    report = dc.rulings_report(_REPO, transport=tmp_path / "t")
    assert report.unlanded is not dc.UNMEASURED, report.unmeasured_reason
    ours = {f"R{n}" for n in range(80, 93)}
    refused = [f.subject for f in report.unlanded if f.subject in ours]
    assert not refused, f"R80-R92 still unlanded under a simulated B2-W2 close: {refused}"
    assert not [f.subject for f in report.uncarried if f.subject in ours]


# ======================================================================================
# SECTION AT -- R93..R99 (batch BW, wave D, lane `bw-1378-rulings-landing`, row [#1378] nearest)
# ======================================================================================
#
# Same two legs as AQ, AR and AS, plus the gate they exist for. RED-first on main d8619ab0: that
# tree's register stops at R92, so the gate refuses R93..R95 once batch BW reads CLOSED, the live
# `decision_coverage.py rulings` names all seven as pending, and every test below that reads
# section AT fails there.

REQUIRED_IDS_AT = [f"R{n}" for n in range(93, 100)]

_T10 = "to-browser/RATIFICATION-2026-10-10.md"
_T11 = "to-browser/RATIFICATION-2026-10-11.md"
_T12 = "to-browser/RATIFICATION-2026-10-12.md"
#: The FILE of each source. The 10-10 file is v3 and the 10-12 file is v2 (each rewritten in
#: place); `RATIFICATION-2026-10-12-v1-superseded.md` is not a source.
EXPECTED_SOURCES_AT: dict[str, list[str]] = {
    **{f"R{n}": [_T10] for n in (93, 94, 95)},
    "R96": [_T11],
    **{f"R{n}": [_T12] for n in (97, 98, 99)},
}
FIRST_LINE_TOKEN_AT = {f"R{n}": f"## R{n} " for n in range(93, 100)}
_AT_FILE_DATES = {_T10: "2026-10-10", _T11: "2026-10-11", _T12: "2026-10-12"}


@pytest.fixture(scope="module")
def entries_at():
    return parse_entries(_REGISTER.read_text(encoding="utf-8"), "AT")


def test_section_at_lands_every_ruling_r93_to_r99_exactly_once(entries_at):
    missing = [i for i in REQUIRED_IDS_AT if i not in entries_at]
    dup = [i for i, v in entries_at.items() if len(v) > 1]
    extra = [i for i in entries_at if i not in REQUIRED_IDS_AT]
    assert not missing, f"section AT of protocols/STANDING_RULINGS.md lacks: {missing}"
    assert not dup, f"entries landed more than once: {dup}"
    assert not extra, f"section AT carries entries outside R93-R99: {extra}"


def test_every_at_entry_carries_the_verbatim_blocks_its_sources_require(entries_at):
    problems = []
    for rid in REQUIRED_IDS_AT:
        if rid not in entries_at:
            continue
        blocks = entries_at[rid][0][1]
        got = [b.path for b in blocks]
        if sorted(set(got)) != sorted(set(EXPECTED_SOURCES_AT[rid])):
            problems.append(f"{rid}: block sources {sorted(set(got))} != {EXPECTED_SOURCES_AT[rid]}")
        for b in blocks:
            if not b.body.strip():
                problems.append(f"{rid}: an empty verbatim block for {b.path}:{b.first}-{b.last}")
    assert entries_at, "section AT is absent -- R93-R99 are not landed"
    assert not problems, "\n".join(problems)


def test_each_at_primary_block_starts_at_its_own_ruling(entries_at):
    problems = []
    for rid in REQUIRED_IDS_AT:
        if rid not in entries_at or not entries_at[rid][0][1]:
            continue
        first = entries_at[rid][0][1][0].body.split("\n")[0]
        if FIRST_LINE_TOKEN_AT[rid] not in first:
            problems.append(f"{rid}: first line {first[:80]!r} lacks {FIRST_LINE_TOKEN_AT[rid]!r}")
    assert entries_at and not problems, "\n".join(problems) or "section AT is absent"


def test_at_blocks_match_their_sources_where_the_transport_is_reachable(entries_at):
    transport = _transport_root()
    mismatched, unreachable = [], []
    for rid in REQUIRED_IDS_AT:
        for b in (entries_at.get(rid) or [("", [])])[0][1]:
            verdict, detail = diff_block(b, transport)
            if verdict == "mismatch":
                mismatched.append(f"{rid}: {detail}")
            elif verdict == "unreachable":
                unreachable.append(f"{rid}: {b.path} ({detail})")
    assert entries_at, "section AT is absent -- nothing to diff"
    assert not mismatched, "landed text differs from its source:\n" + "\n".join(mismatched)
    if transport is not None:
        assert not unreachable, "a declared transport lacks sources:\n" + "\n".join(unreachable)
    elif unreachable:
        warnings.warn(
            f"UNVERIFIED: {len(unreachable)} transport-sourced block(s) of section AT not diffed "
            f"-- no transport declared. Unreachable: " + "; ".join(unreachable), UserWarning,
            stacklevel=1)


def test_every_at_entry_is_carried_by_a_row_or_a_written_disposition():
    """Done-contract item 1's carriage leg, read through the gate's own parser: each of R93..R99
    has a `Carried by:` line the gate accepts (a carrying row, or `no implementation required —
    <why> (owner: <who>)`)."""
    dc = _decision_coverage()
    entries = {e.number: e for e in dc.parse_register(_REGISTER.read_text(encoding="utf-8"))}
    missing = [n for n in range(93, 100) if n not in entries]
    assert not missing, f"not landed: {missing}"
    refused = {f.subject: f.evidence for f in dc.uncarried_rulings(_REPO)
               if f.subject in set(REQUIRED_IDS_AT)}
    assert refused == {}, refused


def _at_transport(tmp_path: Path, *, bw_closed: bool) -> Path:
    """A transport holding the three RATIFICATION files of R93..R99 (headings only, dated as the
    live files are) and the batch clock: B2-W3 CLOSED 2026-10-11, and BW CLOSED when asked."""
    folder = tmp_path / "t" / "to-browser"
    folder.mkdir(parents=True)
    for path, day in _AT_FILE_DATES.items():
        ids = [r for r in REQUIRED_IDS_AT if EXPECTED_SOURCES_AT[r] == [path]]
        head = f"carried-by: OPEN\nkind: RATIFICATION\ndate: {day}\n\n# RATIFICATION - {day}\n\n"
        body = "\n\n".join(f"## {r} — a ruling" for r in ids)
        (folder / Path(path).name).write_text(head + body + "\n", encoding="utf-8", newline="\n")
    (folder / "STATE-BATCH-B2-W3.md").write_text("CLOSED 2026-10-11T12:00Z\n", encoding="utf-8")
    if bw_closed:
        (folder / "STATE-BATCH-BW.md").write_text("CLOSED 2026-10-14T23:59Z\n", encoding="utf-8")
    return tmp_path / "t"


def _repo_without_section_at(tmp_path: Path) -> Path:
    """A copy of the register without section AT -- the tree at d8619ab0 -- and the task rows."""
    import shutil
    root = tmp_path / "repo"
    (root / "protocols").mkdir(parents=True)
    text = _REGISTER.read_text(encoding="utf-8")
    if "## AT. " in text:
        start, end = text.index("## AT. "), text.index("## Editing note")
        text = text[:start] + text[end:]
    (root / "protocols" / "STANDING_RULINGS.md").write_text(text, encoding="utf-8", newline="\n")
    shutil.copytree(_REPO / "tasks", root / "tasks")
    return root


def test_without_section_at_the_gate_names_r93_to_r99_pending_then_refuses_after_a_bw_close(
        tmp_path):
    """The RED-first witness (Done-contract item 2), kept as a test: the register as it stood at
    d8619ab0 names all seven pending inside the grace period, and refuses R93..R95 (two closed
    batches after 2026-10-10) once BW reads CLOSED -- so the clock arms the refusal."""
    dc = _decision_coverage()
    bare = _repo_without_section_at(tmp_path)
    open_ = dc.rulings_report(bare, transport=_at_transport(tmp_path / "a", bw_closed=False))
    assert open_.unlanded == []
    assert list(open_.pending) == REQUIRED_IDS_AT
    assert "pending within grace: 7" in open_.render()
    closed = dc.rulings_report(bare, transport=_at_transport(tmp_path / "b", bw_closed=True))
    assert sorted(f.subject for f in closed.unlanded) == ["R93", "R94", "R95"]
    assert not closed.passed


def test_the_gate_reports_r93_to_r99_landed_and_carried_under_a_simulated_bw_close(tmp_path):
    """Done-contract item 2: `decision_coverage.py rulings` reports 0 unlanded and 0 pending for
    R93..R99 with BW CLOSED, all seven read, and every landed entry carried."""
    dc = _decision_coverage()
    report = dc.rulings_report(_REPO, transport=_at_transport(tmp_path, bw_closed=True))
    assert report.unlanded is not dc.UNMEASURED
    assert report.rulings_read == len(REQUIRED_IDS_AT)
    assert report.unlanded == [], [f.subject for f in report.unlanded]
    assert list(report.pending) == []
    assert report.uncarried == [], [f.subject for f in report.uncarried]
    assert report.passed


def test_the_live_ratification_files_leave_nothing_of_r93_to_r99_pending():
    """The same reading against the operator's real RATIFICATION files wherever the transport is
    reachable; with none declared the leg is named UNVERIFIED, never passed in silence."""
    transport = _transport_root()
    if transport is None or not (transport / "to-browser").is_dir():
        warnings.warn("UNVERIFIED: R93-R99 were not read against the live RATIFICATION files -- "
                      "no transport declared.", UserWarning, stacklevel=1)
        return
    dc = _decision_coverage()
    report = dc.rulings_report(_REPO, transport=transport)
    assert report.unlanded is not dc.UNMEASURED, report.unmeasured_reason
    ours = set(REQUIRED_IDS_AT)
    assert not [f.subject for f in report.unlanded if f.subject in ours]
    assert not [r for r in report.pending if r in ours], report.pending
    assert not [f.subject for f in report.uncarried if f.subject in ours]

# --- R96: ADR-123 and ADR-124 Accepted, the status line only (ADR-94) ------------------------

_ADRS_R96 = {123: "ADR-123-the-harness-ships-as-one-versioned-artefact-pinned-in-each-consumer.md",
             124: "ADR-124-one-code-standard-enforced-by-tools-adopted-one-at-a-time.md"}


@pytest.mark.parametrize("number", sorted(_ADRS_R96))
def test_r96_accepts_adr_123_and_124_on_the_status_line_and_the_index_agrees(number):
    """Done-contract item 3: the status line reads Accepted and cites R96; the README index row
    agrees (the header<->index coherence leg of `validate_adr_status`), and the decision register
    no longer says the ADR awaits ratification."""
    adr = (_REPO / "docs" / "decisions" / _ADRS_R96[number]).read_text(encoding="utf-8")
    status = next(ln for ln in adr.splitlines() if ln.startswith("- **Status:**"))
    assert status.startswith("- **Status:** Accepted"), status
    assert "R96" in status, status
    index = (_REPO / "docs" / "decisions" / "README.md").read_text(encoding="utf-8")
    row = next(ln for ln in index.splitlines() if ln.startswith(f"| ADR-{number} |"))
    assert "| **Accepted" in row and "**Proposed.**" not in row, row[:120]
    dc = _decision_coverage()
    disp = dc.DECISION_DISPOSITIONS.get(f"adr:{number}")
    assert disp is None or disp.reason != dc._AWAITING_RATIFICATION


# ======================================================================================
# SECTION AU -- R100..R102, R104..R115 (batch BU, lane `lane-bu-1450-boot-v2`, row [#1538])
# ======================================================================================
#
# Same legs as AT. RED-first on main a4fde7bf: that tree's register stops at R99, so every test
# below that reads section AU fails there, and the simulation shows the gate refusing all fifteen
# once two batches have closed. R103 is not a ruling (no entry may carry it).

REQUIRED_IDS_AU = ["R100", "R101", "R102"] + [f"R{n}" for n in range(104, 116)]

_U13 = "to-browser/RATIFICATION-2026-10-13.md"
_U14V3 = "to-browser/RATIFICATION-2026-10-14-v3-superseded.md"
_U14V4 = "to-browser/RATIFICATION-2026-10-14-v4-superseded.md"
_U14V5 = "to-browser/RATIFICATION-2026-10-14-v5-superseded.md"
_U14V6 = "to-browser/RATIFICATION-2026-10-14-v6-superseded.md"
_U14V7 = "to-browser/RATIFICATION-2026-10-14-v7-superseded.md"
#: v7 names v3-v6 as the source of record for what it calls "unchanged"; v7 is itself superseded
#: by v8/v9 since, which carry R113-R115 "unchanged (v7)". R102-R115 live only in superseded
#: files, so `decision_coverage.ratification_files` -- which skips `-superseded` -- never sees
#: them: that is why the simulation below presents them as live files.
EXPECTED_SOURCES_AU: dict[str, list[str]] = {
    "R100": [_U13], "R101": [_U13],
    **{r: [_U14V3] for r in ("R102", "R104", "R105", "R106")},
    "R107": [_U14V4], "R108": [_U14V4],
    "R109": [_U14V5], "R110": [_U14V5],
    "R112": [_U14V6],
    **{r: [_U14V7] for r in ("R111", "R113", "R114", "R115")},
}
FIRST_LINE_TOKEN_AU = {r: (f"## {r} (amended) " if r == "R111" else f"## {r} ")
                       for r in REQUIRED_IDS_AU}

#: sha256 of section AT as it stands at a4fde7bf (LF-normalised). Section AT is append-only and is
#: never edited.
_SECTION_AT_SHA256 = "13c385641911bf5ee08d776b1a1d0320dc3c3eabf10aad22a6e9d38e29f4ab63"


@pytest.fixture(scope="module")
def entries_au():
    return parse_entries(_REGISTER.read_text(encoding="utf-8"), "AU")


def _prose_outside_fences(section: "str | None") -> str:
    out, fenced = [], False
    for ln in (section or "").split("\n"):
        if ln.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            out.append(ln)
    return "\n".join(out)


def _register_text() -> str:
    return _REGISTER.read_text(encoding="utf-8").replace("\r\n", "\n")


def test_section_au_lands_every_id_of_r100_to_r115_exactly_once_and_no_r103(entries_au):
    missing = [i for i in REQUIRED_IDS_AU if i not in entries_au]
    dup = [i for i, v in entries_au.items() if len(v) > 1]
    extra = [i for i in entries_au if i not in REQUIRED_IDS_AU]
    assert not missing, f"section AU of protocols/STANDING_RULINGS.md lacks: {missing}"
    assert not dup, f"entries landed more than once: {dup}"
    assert not extra, f"section AU carries entries outside its ids (R103 is no ruling): {extra}"


def test_every_au_entry_carries_the_verbatim_blocks_its_sources_require(entries_au):
    problems = []
    for rid in REQUIRED_IDS_AU:
        if rid not in entries_au:
            continue
        blocks = entries_au[rid][0][1]
        got = [b.path for b in blocks]
        if sorted(set(got)) != sorted(set(EXPECTED_SOURCES_AU[rid])):
            problems.append(f"{rid}: block sources {sorted(set(got))} != {EXPECTED_SOURCES_AU[rid]}")
        for b in blocks:
            if not b.body.strip():
                problems.append(f"{rid}: an empty verbatim block for {b.path}:{b.first}-{b.last}")
    assert entries_au, "section AU is absent -- R100-R115 are not landed"
    assert not problems, "\n".join(problems)


def test_each_au_primary_block_starts_at_its_own_ruling(entries_au):
    problems = []
    for rid in REQUIRED_IDS_AU:
        if rid not in entries_au or not entries_au[rid][0][1]:
            continue
        first = entries_au[rid][0][1][0].body.split("\n")[0]
        if FIRST_LINE_TOKEN_AU[rid] not in first:
            problems.append(f"{rid}: first line {first[:80]!r} lacks {FIRST_LINE_TOKEN_AU[rid]!r}")
    assert entries_au and not problems, "\n".join(problems) or "section AU is absent"


def test_au_blocks_match_their_sources_where_the_transport_is_reachable(entries_au):
    transport = _transport_root()
    mismatched, unreachable = [], []
    for rid in REQUIRED_IDS_AU:
        for b in (entries_au.get(rid) or [("", [])])[0][1]:
            verdict, detail = diff_block(b, transport)
            if verdict == "mismatch":
                mismatched.append(f"{rid}: {detail}")
            elif verdict == "unreachable":
                unreachable.append(f"{rid}: {b.path} ({detail})")
    assert entries_au, "section AU is absent -- nothing to diff"
    assert not mismatched, "landed text differs from its source:\n" + "\n".join(mismatched)
    if transport is not None:
        assert not unreachable, "a declared transport lacks sources:\n" + "\n".join(unreachable)
    elif unreachable:
        warnings.warn(
            f"UNVERIFIED: {len(unreachable)} transport-sourced block(s) of section AU not diffed "
            f"-- no transport declared. Unreachable: " + "; ".join(unreachable), UserWarning,
            stacklevel=1)


def test_every_au_entry_is_carried_by_a_row_or_a_written_disposition():
    """The carriage leg, read through the gate's own parser: each AU id is in the parsed register
    and has a `Carried by:` line the gate accepts."""
    dc = _decision_coverage()
    entries = {e.number for e in dc.parse_register(_REGISTER.read_text(encoding="utf-8"))}
    missing = [r for r in REQUIRED_IDS_AU if int(r[1:]) not in entries]
    assert not missing, f"not landed: {missing}"
    refused = {f.subject: f.evidence for f in dc.uncarried_rulings(_REPO)
               if f.subject in set(REQUIRED_IDS_AU)}
    assert refused == {}, refused


def _carried_line(rid: str) -> str:
    """The first `**Carried by:**` line after the entry's bullet, outside fences ('' if none)."""
    bullet = re.compile(r"- \*\*" + rid + r"\b")
    end = re.compile(r"- \*\*R\d+\b|#{2,3} ")
    fenced, inside = False, False
    for ln in _register_text().split("\n"):
        if ln.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if bullet.match(ln):
            inside = True
            continue
        if inside and end.match(ln):
            return ""
        if inside and ln.strip().startswith("**Carried by:**"):
            return ln
    return ""


@pytest.mark.parametrize("rid", ["R111", "R113"])
def test_r111_and_r113_carry_the_build_1_challenge_disposition(rid):
    line = _carried_line(rid)
    assert line, f"{rid} has no `**Carried by:**` line"
    for token in ("CHALLENGE", "INPUT_REQUIRED", "DIGEST-BUILD1-READY"):
        assert token in line, f"{rid}'s Carried-by line lacks {token!r}: {line[:160]!r}"


def test_r103_is_recorded_as_no_ruling_and_has_no_entry():
    text = _register_text()
    prose = _prose_outside_fences(_section(text, "AU"))
    m = re.search(r"R103", prose)
    assert m, "section AU does not mention R103 (it must record that there is no such ruling)"
    assert "no such ruling" in prose[m.end(): m.end() + 200], prose[m.start(): m.start() + 240]
    assert not [ln for ln in text.split("\n") if ln.startswith("- **R103")]


def test_section_au_states_that_section_ats_no_r100_sentence_is_superseded():
    prose = _prose_outside_fences(_section(_register_text(), "AU"))
    m = re.search(r"There is no R100", prose)
    assert m, "section AU does not quote section AT's `There is no R100` sentence"
    assert "superseded" in prose[m.end(): m.end() + 300]


def test_section_at_is_byte_identical_to_its_landed_text():
    """A GUARD, not a RED test: it passes on the base by construction. Section AT is append-only
    and is never edited; section AU supersedes its sentence by a note of its own."""
    import hashlib
    at = _section(_register_text(), "AT")
    assert at is not None
    assert hashlib.sha256(at.encode("utf-8")).hexdigest() == _SECTION_AT_SHA256


# --- the gate section AU exists for ----------------------------------------------------------

_AU_LIVE_FILES = {
    "RATIFICATION-2026-10-13.md": ("2026-10-13", ["R100", "R101"]),
    "RATIFICATION-2026-10-14.md": ("2026-10-14", ["R102"] + [f"R{n}" for n in range(104, 111)]
                                   + ["R112"]),
    "RATIFICATION-2026-10-15.md": ("2026-10-15", ["R111", "R113", "R114", "R115"]),
}


def _au_transport(tmp_path: Path, *, closed: bool) -> Path:
    """A transport presenting R100..R115 as three LIVE RATIFICATION files (the real v3-v7 files
    are `-superseded`, which the gate skips) and a batch clock: BU CLOSED 2026-10-16 and, when
    asked, BV CLOSED 2026-10-17 -- two closed batches after every file's day, past the grace."""
    folder = tmp_path / "t" / "to-browser"
    folder.mkdir(parents=True)
    for name, (day, ids) in _AU_LIVE_FILES.items():
        head = f"carried-by: OPEN\nkind: RATIFICATION\ndate: {day}\n\n# RATIFICATION - {day}\n\n"
        body = "\n\n".join(f"## {r} — a ruling" for r in ids)
        (folder / name).write_text(head + body + "\n", encoding="utf-8", newline="\n")
    (folder / "STATE-BATCH-BU.md").write_text("CLOSED 2026-10-16T12:00Z\n", encoding="utf-8")
    if closed:
        (folder / "STATE-BATCH-BV.md").write_text("CLOSED 2026-10-17T12:00Z\n", encoding="utf-8")
    return tmp_path / "t"


def _repo_without_section_au(tmp_path: Path) -> Path:
    """A copy of the register without section AU -- the tree at a4fde7bf -- and the task rows."""
    import shutil
    root = tmp_path / "repo"
    (root / "protocols").mkdir(parents=True)
    text = _REGISTER.read_text(encoding="utf-8")
    if "## AU. " in text:
        start = text.index("## AU. ")
        nxt = re.search(r"(?m)^## ", text[start + 6:])
        text = text[:start] + text[start + 6 + nxt.start():]
    (root / "protocols" / "STANDING_RULINGS.md").write_text(text, encoding="utf-8", newline="\n")
    shutil.copytree(_REPO / "tasks", root / "tasks")
    return root


def _by_number(ids):
    return sorted(ids, key=lambda r: int(r[1:]))


def test_without_section_au_the_gate_refuses_all_fifteen_once_two_batches_have_closed(tmp_path):
    """RED witness, kept as a test: the register at a4fde7bf names all fifteen pending inside the
    grace period (one closed batch) and refuses all fifteen after a second -- the clock arms it."""
    dc = _decision_coverage()
    bare = _repo_without_section_au(tmp_path)
    closed = dc.rulings_report(bare, transport=_au_transport(tmp_path / "a", closed=True))
    assert closed.unlanded is not dc.UNMEASURED, closed.unmeasured_reason
    assert _by_number(f.subject for f in closed.unlanded) == _by_number(REQUIRED_IDS_AU)
    assert not closed.passed
    open_ = dc.rulings_report(bare, transport=_au_transport(tmp_path / "b", closed=False))
    assert open_.unlanded == []
    assert _by_number(open_.pending) == _by_number(REQUIRED_IDS_AU)


def test_with_section_au_the_gate_reads_fifteen_rulings_landed_and_carried(tmp_path):
    dc = _decision_coverage()
    report = dc.rulings_report(_REPO, transport=_au_transport(tmp_path, closed=True))
    assert report.unlanded is not dc.UNMEASURED, report.unmeasured_reason
    assert report.rulings_read == len(REQUIRED_IDS_AU)
    assert report.unlanded == [], [f.subject for f in report.unlanded]
    assert list(report.pending) == []
    assert not [f.subject for f in report.uncarried if f.subject in set(REQUIRED_IDS_AU)]


def test_the_live_ratification_files_leave_nothing_of_r100_to_r115_open(tmp_path):
    """Read against a tmp copy of the operator's real RATIFICATION and STATE-BATCH files. A
    STATE-BATCH file that makes the clock unreadable is left out of the copy (and named in a
    warning). With no transport declared the leg is named UNVERIFIED, never passed in silence."""
    import shutil
    transport = _transport_root()
    if transport is None or not (transport / "to-browser").is_dir():
        warnings.warn("UNVERIFIED: R100-R115 were not read against the live RATIFICATION files "
                      "-- no transport declared.", UserWarning, stacklevel=1)
        return
    dc = _decision_coverage()
    sim = tmp_path / "t" / "to-browser"
    sim.mkdir(parents=True)
    for src in (transport / "to-browser").glob("RATIFICATION-*.md"):
        shutil.copy2(src, sim / src.name)
    skipped = []
    for src in sorted((transport / "to-browser").glob("STATE-BATCH-*.md")):
        probe = tmp_path / "probe" / "to-browser"
        shutil.rmtree(tmp_path / "probe", ignore_errors=True)
        probe.mkdir(parents=True)
        shutil.copy2(src, probe / src.name)
        try:
            dc.closed_batch_dates(tmp_path / "probe")
        except Exception:
            skipped.append(src.name)
            continue
        shutil.copy2(src, sim / src.name)
    if skipped:
        warnings.warn(f"skipped unreadable STATE-BATCH file(s): {skipped}", UserWarning,
                      stacklevel=1)
    report = dc.rulings_report(_REPO, transport=tmp_path / "t")
    assert report.unlanded is not dc.UNMEASURED, report.unmeasured_reason
    ours = set(REQUIRED_IDS_AU)
    assert not [f.subject for f in report.unlanded if f.subject in ours]
    assert not [r for r in report.pending if r in ours], report.pending
    assert not [f.subject for f in report.uncarried if f.subject in ours]
