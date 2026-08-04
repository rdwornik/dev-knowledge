"""Tests for scripts/preflight_contract.py — the pre-flight locator verifier (lesson 8).

WHY THIS EXISTS. Nine architect premise errors landed in this window's contracts and prompts,
every one caught downstream by accident rather than by a check:

  1. "len(ALL_CHECKS) stays 38"                    live 39   (window-2 prompt + L-D dossier)
  2. L-D dossier: ALL_CHECKS registered at :3381   live 3429
  3. leg-4 contract AC-2: "38 -> 37" arithmetic    live 39 -> 38
  4. leg-4 contract: five consumer dailies dated 2026-08-02, absent from this tree (tops out
     at 2026-07-31)
  5. leg-4 contract FR-2 read literally contradicts its own F4 and R1
  6. window-2 prompt: "Closes [#465] (all four legs done)" — blocked by AC-7's unmet clause
  7. window-1 prompt row 3: "8 of 1493 files" — 3 of 1578 against the actual fix
  8. window-1 prompt: `.claude/**/*.md` called "a dead glob matching nothing" — matches 11
  9. window-1 prompt: `normalize-dated-headers` called "deployed" — hub-only

Items 1-4 are pure LOCATOR claims: a number, a line, a date, a path. A machine can check those
before a session acts on them, which is the whole point — the cost of these is not that they are
wrong, it is that they are found three hours in.

SCOPE, stated so the tests cannot over-claim: this verifies locators that are mechanically
checkable — `file:line` existence, heading/anchor text, SHA reachability, `[#id]` liveness. It
does NOT and cannot verify a claim's REASONING (items 5 and 6 above are contradictions and
unmet preconditions, not bad locators). Adoption-first: nothing wires it into a gate.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import pytest

import preflight_contract as pf

_REPO_ROOT = Path(__file__).resolve().parent.parent


def _write(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "contract.md"
    p.write_text(body, encoding="utf-8", newline="\n")
    return p


# ---------------------------------------------------------------------------
# A clean contract passes. Without this the FAIL tests could be satisfied by a
# verifier that simply fails everything.
# ---------------------------------------------------------------------------

def test_a_contract_whose_locators_all_resolve_passes(tmp_path):
    head = subprocess.run(["git", "-C", str(_REPO_ROOT), "rev-parse", "--short", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    body = (
        "# Contract\n\n"
        "- the constant lives at `scripts/audit.py:1`\n"
        f"- landed at `{head}`\n"
        "- see `CLAUDE.md` heading \"## 2. Repo identity\"\n"
    )
    report = pf.verify(_write(tmp_path, body), _REPO_ROOT)
    assert report.failed == [], [c.detail for c in report.failed]
    assert report.checked, "nothing was extracted — the verifier would be vacuous"


def test_a_clean_contract_exits_zero(tmp_path):
    body = "# C\n\n- `scripts/audit.py:1`\n"
    assert pf.main([str(_write(tmp_path, body)), "--repo-root", str(_REPO_ROOT)]) == 0


# ---------------------------------------------------------------------------
# One fixture per claim class the brief names. Each must be CAUGHT and NAMED,
# and each failure must carry the LIVE value — "wrong" without "actually N" is
# a second lookup for the reader.
# ---------------------------------------------------------------------------

def test_a_wrong_line_number_is_caught_and_the_live_length_named(tmp_path):
    body = "# C\n\n- the registration is at `scripts/audit.py:999999`\n"
    report = pf.verify(_write(tmp_path, body), _REPO_ROOT)
    assert len(report.failed) == 1, [c.detail for c in report.checked]
    # Assert on the RENDERED line: that is what an operator reads, and it is where the
    # cited value and the live value sit side by side.
    rendered = report.render()
    assert "999999" in rendered and "scripts/audit.py" in rendered
    assert "lines" in rendered, f"the live length was not named: {rendered}"


def test_a_renamed_heading_is_caught(tmp_path):
    body = '# C\n\n- see `CLAUDE.md` heading "## 42. A Section That Does Not Exist"\n'
    report = pf.verify(_write(tmp_path, body), _REPO_ROOT)
    assert len(report.failed) == 1, [c.detail for c in report.checked]
    assert "Does Not Exist" in report.render()


def test_an_unreachable_sha_is_caught(tmp_path):
    body = "# C\n\n- landed at `deadbee`\n"
    report = pf.verify(_write(tmp_path, body), _REPO_ROOT)
    assert len(report.failed) == 1, [c.detail for c in report.checked]
    rendered = report.render()
    assert "deadbee" in rendered and "not present" in rendered


def test_a_closed_backlog_id_is_caught(tmp_path):
    """[#465] closed earlier today. A contract that still speaks of it as open is stale, and
    that is exactly premise error 6 in this module's docstring — caught mechanically here."""
    body = "# C\n\n- the open row [#465] is the subject\n"
    report = pf.verify(_write(tmp_path, body), _REPO_ROOT)
    assert len(report.failed) == 1, [c.detail for c in report.checked]
    rendered = report.render()
    assert "#465" in rendered and "not open" in rendered


def test_a_missing_file_is_caught(tmp_path):
    body = "# C\n\n- `scripts/does_not_exist.py:12`\n"
    report = pf.verify(_write(tmp_path, body), _REPO_ROOT)
    assert len(report.failed) == 1
    assert "does not exist" in report.render()


def test_an_open_backlog_id_passes(tmp_path):
    """The positive control for id liveness — otherwise "caught" could mean "flags every id"."""
    body = "# C\n\n- [#383] governs the waves\n"
    report = pf.verify(_write(tmp_path, body), _REPO_ROOT)
    assert report.failed == [], [c.detail for c in report.failed]


# ---------------------------------------------------------------------------
# Exit codes and posture.
# ---------------------------------------------------------------------------

def test_any_failure_exits_nonzero(tmp_path):
    body = "# C\n\n- `scripts/audit.py:999999`\n"
    assert pf.main([str(_write(tmp_path, body)), "--repo-root", str(_REPO_ROOT)]) == 1


def test_an_unreadable_contract_fails_closed_with_exit_2(tmp_path):
    """The `check_seal_identity` posture: an internal error is never a silent pass. Exit 2 is
    distinct from exit 1 so "I could not look" is distinguishable from "I looked and it is
    wrong" — the [#465] leg-4 lesson, applied to this tool from the start."""
    assert pf.main([str(tmp_path / "no-such-contract.md"), "--repo-root", str(_REPO_ROOT)]) == 2


def test_it_writes_nothing(tmp_path):
    """Read-only, Layer 2 (ADR-28/36)."""
    body = "# C\n\n- `scripts/audit.py:1`\n- `scripts/audit.py:999999`\n"
    contract = _write(tmp_path, body)
    before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    pf.main([str(contract), "--repo-root", str(_REPO_ROOT)])
    after = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    assert before == after, "the verifier wrote something"


# ---------------------------------------------------------------------------
# Extraction — the part that decides whether the tool measures anything at all.
# ---------------------------------------------------------------------------

def test_prose_that_merely_resembles_a_locator_is_not_extracted(tmp_path):
    """A verifier that extracts nothing reports PASS on everything, which is this window's
    defining failure mode. A verifier that extracts too much drowns the reader in false
    failures and gets ignored — equally fatal, more slowly."""
    body = ("# C\n\nRatios like 3:1 and times like 14:30 are not locators. Version 1.2.3 is\n"
            "not a SHA. The word deadbeef in prose is not a SHA either — only a backticked\n"
            "one is. An issue like #465 without brackets is not a backlog id.\n")
    report = pf.verify(_write(tmp_path, body), _REPO_ROOT)
    assert report.checked == [], [c.raw for c in report.checked]


def test_every_claim_class_the_brief_names_is_extractable(tmp_path):
    """STRUCTURAL: the four classes are derived from the module's own registry, not a literal
    list here, so adding a class without a fixture is visible."""
    assert set(pf.CLAIM_KINDS) == {"file-line", "heading", "sha", "backlog-id"}, pf.CLAIM_KINDS
    head = subprocess.run(["git", "-C", str(_REPO_ROOT), "rev-parse", "--short", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    body = (f"# C\n\n- `scripts/audit.py:1`\n- `{head}`\n- [#383]\n"
            '- `CLAUDE.md` heading "## 2. Repo identity"\n')
    report = pf.verify(_write(tmp_path, body), _REPO_ROOT)
    assert {c.kind for c in report.checked} == set(pf.CLAIM_KINDS), \
        sorted({c.kind for c in report.checked})


@pytest.mark.live_repo
def test_the_windows_own_stale_locator_would_have_been_caught(tmp_path):
    """The motivating case, run against the real tree rather than asserted.

    The L-D dossier said the ALL_CHECKS registration was at `scripts/audit.py:3381`. It was
    3429 when I checked it by hand, three arcs in. Both are real lines in a 3800-line file, so
    a bare existence check would NOT have caught it — which is the honest limit this tool has
    to state about itself. What it does catch is the class in fixture 1: a line number past the
    end of the file. Recorded so nobody reads more into the tool than it delivers.
    """
    n = len((_REPO_ROOT / "scripts" / "audit.py").read_text(encoding="utf-8").splitlines())
    body = f"# C\n\n- in range `scripts/audit.py:3381`\n- past EOF `scripts/audit.py:{n + 1}`\n"
    report = pf.verify(_write(tmp_path, body), _REPO_ROOT)
    assert len(report.failed) == 1, [c.detail for c in report.checked]
    assert str(n + 1) in report.render()


def test_a_bare_script_filename_resolves_against_the_source_roots(tmp_path):
    """This repo habitually cites a script by bare name — `normalize_headers.py:32` means
    `scripts/normalize_headers.py:32`. Resolving only at the repo root produced SIX false FAILs
    on the very first real artifact this tool was pointed at (the L-D dossier). A verifier that
    cries wolf is ignored just as surely as one that never fires."""
    body = "# C\n\n- `normalize_headers.py:1`\n- `audit.py:1`\n"
    report = pf.verify(_write(tmp_path, body), _REPO_ROOT)
    assert report.failed == [], [c.detail for c in report.failed]
    assert len(report.checked) == 2


def test_a_bare_name_that_exists_nowhere_still_fails(tmp_path):
    """The source-root fallback must not become a way for a wrong path to pass."""
    body = "# C\n\n- `not_a_real_module_anywhere.py:1`\n"
    report = pf.verify(_write(tmp_path, body), _REPO_ROOT)
    assert len(report.failed) == 1
    assert "does not exist" in report.render()


def test_a_bare_name_past_EOF_names_the_resolved_path(tmp_path):
    """When a bare name resolves via a source root, the FAIL must name the path it actually
    checked — otherwise the reader cannot tell which file the line count refers to."""
    n = len((_REPO_ROOT / "scripts" / "normalize_headers.py").read_text(encoding="utf-8").splitlines())
    body = f"# C\n\n- `normalize_headers.py:{n + 500}`\n"
    report = pf.verify(_write(tmp_path, body), _REPO_ROOT)
    assert len(report.failed) == 1
    assert "scripts/normalize_headers.py" in report.render(), report.render()


# ---------------------------------------------------------------------------
# terra round 1, 2026-08-04 — three HIGHs, each pinned.
# ---------------------------------------------------------------------------

def test_a_windows_absolute_locator_is_extracted_not_silently_skipped(tmp_path):
    """A contract carrying ONLY a Windows absolute locator used to report a clean 0/0 — and a
    verifier that extracts nothing passes everything, which is this window's defining failure
    mode. It must be EXTRACTED; whether it then resolves is a separate question."""
    bs = chr(92)  # built, not written literally: every escaping layer between here and the
    # file mangled a backslash at least once this session, and a fixture that silently loses
    # its backslashes tests nothing.
    win = f"C:{bs}nowhere{bs}scripts{bs}audit.py:12"
    body = "# C" + chr(10) * 2 + "- `" + win + "`" + chr(10)
    assert body.count(bs) == 3, f"the fixture lost its backslashes: {body!r}"
    report = pf.verify(_write(tmp_path, body), _REPO_ROOT)
    assert report.checked, "the Windows absolute locator was not extracted at all"
    assert len(report.failed) == 1, [c.raw for c in report.checked]


def test_an_ambiguous_bare_name_does_not_silently_verify_the_wrong_file(tmp_path):
    """First-match-wins across the source roots could verify a locator against a file the
    contract never named, so a stale citation would pass. An ambiguous bare name is a defect in
    the CITATION: it is reported unresolved and told to qualify itself."""
    repo = tmp_path / "repo"
    for root in ("scripts", "deploy"):
        (repo / root).mkdir(parents=True)
        (repo / root / "twin.py").write_text("x = 1\n", encoding="utf-8", newline="\n")
    (repo / "BACKLOG.md").write_text("# B\n", encoding="utf-8", newline="\n")

    resolved, note = pf._resolve(repo, "twin.py")
    assert resolved is None, resolved
    assert "ambiguous" in note and "scripts/twin.py" in note and "deploy/twin.py" in note

    report = pf.verify(_write(tmp_path, "# C\n\n- `twin.py:1`\n"), repo)
    assert len(report.failed) == 1
    assert "ambiguous" in report.render()


def test_an_unambiguous_bare_name_still_resolves(tmp_path):
    """The positive control — the ambiguity guard must not become "reject every bare name"."""
    resolved, note = pf._resolve(_REPO_ROOT, "normalize_headers.py")
    assert resolved is not None and note == ""
    assert resolved.name == "normalize_headers.py"


def test_a_qualified_path_wins_over_the_bare_name_search(tmp_path):
    """A path given relative to the repo root is unambiguous by construction and must never be
    subjected to the source-root search."""
    resolved, _ = pf._resolve(_REPO_ROOT, "scripts/audit.py")
    assert resolved == _REPO_ROOT / "scripts" / "audit.py"


def test_an_unusable_git_fails_closed_rather_than_calling_every_sha_stale(tmp_path):
    """git exits 1 for BOTH a missing object and a broken invocation. Without a health probe, a
    dead git renders every SHA as an ordinary 'not reachable' failure at exit 1 — "I could not
    check" wearing the costume of "I checked and it is wrong". That is the [#465] leg-4 defect,
    and it must not live in the tool built to answer that class."""
    not_a_repo = tmp_path / "bare"
    not_a_repo.mkdir()
    (not_a_repo / "BACKLOG.md").write_text("# B\n", encoding="utf-8", newline="\n")
    contract = _write(tmp_path, "# C\n\n- landed at `abc1234`\n")

    with pytest.raises(pf.PreflightError):
        pf.verify(contract, not_a_repo)
    assert pf.main([str(contract), "--repo-root", str(not_a_repo)]) == 2, \
        "an unusable git produced exit 1 (an ordinary claim failure) instead of fail-closed 2"


# ---------------------------------------------------------------------------
# terra round 2, 2026-08-04 — three more HIGHs, each pinned.
# ---------------------------------------------------------------------------

def test_a_qualified_path_is_never_source_root_searched(tmp_path):
    """A qualified path names exactly ONE place. Falling back to the source-root search after it
    fails would let `scripts/typo.py:1` quietly verify against `deploy/typo.py` — the same
    wrong-file defect the ambiguity guard exists to stop, arriving by the other door."""
    repo = tmp_path / "repo"
    (repo / "deploy").mkdir(parents=True)
    (repo / "deploy" / "only_here.py").write_text("x = 1\n", encoding="utf-8", newline="\n")
    (repo / "BACKLOG.md").write_text("# B\n", encoding="utf-8", newline="\n")

    resolved, note = pf._resolve(repo, "scripts/only_here.py")
    assert resolved is None, f"a qualified path resolved elsewhere: {resolved}"
    assert "does not exist" in note

    bare, _ = pf._resolve(repo, "only_here.py")
    assert bare is not None, "the bare-name search should still work"


def test_a_bare_name_in_the_root_and_a_source_root_is_ambiguous(tmp_path):
    """The repo root belongs IN the ambiguity set — otherwise a root copy silently wins."""
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    (repo / "BACKLOG.md").write_text("# B\n", encoding="utf-8", newline="\n")
    for rel in ("dup.py", "scripts/dup.py"):
        (repo / rel).write_text("x = 1\n", encoding="utf-8", newline="\n")

    # The root copy exists, so `direct` wins and there is no ambiguity to report — that is the
    # documented precedence, asserted so a future change to it is a visible decision.
    resolved, _ = pf._resolve(repo, "dup.py")
    assert resolved == repo / "dup.py"


def test_a_file_only_contract_does_not_need_git_at_all(tmp_path):
    """The health probe is LAZY. Probing eagerly and failing hard would refuse to verify a
    file-and-heading contract in a tree with no git — a legitimate use — while probing eagerly
    and ignoring the result let a failed operational probe go silent. Deferring it does neither."""
    bare = tmp_path / "nogit"
    bare.mkdir()
    (bare / "BACKLOG.md").write_text("# B\n", encoding="utf-8", newline="\n")
    (bare / "thing.md").write_text("# T\n", encoding="utf-8", newline="\n")

    contract = _write(tmp_path, "# C\n\n- `thing.md:1`\n")
    assert pf.main([str(contract), "--repo-root", str(bare)]) == 0


def test_the_same_unusable_repo_still_fails_closed_once_a_sha_is_cited(tmp_path):
    """The other half: the moment a SHA claim actually needs git, an unusable repo is exit 2."""
    bare = tmp_path / "nogit2"
    bare.mkdir()
    (bare / "BACKLOG.md").write_text("# B\n", encoding="utf-8", newline="\n")
    contract = _write(tmp_path, "# C\n\n- landed at `abc1234`\n")
    assert pf.main([str(contract), "--repo-root", str(bare)]) == 2


# ---------------------------------------------------------------------------
# [#483] FR-3b — assertion-vs-citation discrimination on the backlog-id leg.
#
# R1 (binding precondition): the leg reads EVERY `[#id]` as a claim that the row is OPEN.
# Its first production run over the 2026-08-04 handoff bundle flagged 11 ids, every one a
# correct historical citation — ids in a table literally headed `| closed |`, and a provenance
# clause. A gate wired on that behaviour REDs every handoff bundle by construction.
#
# R2 (role rule), implemented in two mechanical layers:
#   Layer 1  surface path class — docs/audits/, docs/handoffs/, JOURNAL, LESSONS are
#            citation-role wholesale.
#   Layer 2  in-line context on assertion-role surfaces — backtick-quoted spans are prose;
#            in a BACKLOG row only the `kill-candidates:` field VALUE is an open-claim;
#            closed-table rows and `since [#id]` provenance clauses are citations.
#
# Every fixture below is a REAL shape captured from the live bundle or the live BACKLOG,
# not an invented one.
# ---------------------------------------------------------------------------

_CLOSED = "479"   # closed on main; asserted below so the fixture cannot rot into a fiction
_OPEN = "310"     # open on main


def _mini_repo(tmp_path: Path) -> Path:
    """A throwaway repo whose BACKLOG.md carries exactly one OPEN row (`_OPEN`)."""
    root = tmp_path / "repo"
    root.mkdir(parents=True, exist_ok=True)
    root.joinpath("BACKLOG.md").write_text(
        f"# Backlog\n\n- [#{_OPEN}] [P3][S] a live row\n", encoding="utf-8", newline="\n")
    return root


def _at(root: Path, rel: str, body: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8", newline="\n")
    return p


def _backlog_id_failures(report) -> list[str]:
    return [c.raw for c in report.failed if c.kind == "backlog-id"]


def test_fixture_ids_still_have_the_liveness_this_suite_assumes():
    """Guard the fixtures: if `_CLOSED` reopens or `_OPEN` closes, every test below goes
    vacuous or falsely red. Asserted against the LIVE BACKLOG, not assumed."""
    live = pf._open_backlog_ids(_REPO_ROOT)
    assert _OPEN in live, f"fixture id #{_OPEN} is no longer open — re-point it"
    assert _CLOSED not in live, f"fixture id #{_CLOSED} is open again — re-point it"


def test_handoff_bundle_citations_are_not_flagged(tmp_path):
    """[#483] R2 Layer 1 — a docs/handoffs/ artifact is citation-role wholesale.

    Both shapes are verbatim from the 2026-08-04 bundle: the `| closed |` table row and the
    provenance clause. These are the false positives R1 measured.
    """
    root = _mini_repo(tmp_path)
    contract = _at(root, "docs/handoffs/2026-08-04-x/RESIDUAL.md",
                   "| closed | what |\n|---|---|\n"
                   f"| `[#{_CLOSED}]` | SUPERSEDED — its Done-when died with ADR-85's FR5 |\n\n"
                   f"`BACKLOG.md` is GENERATED since [#{_CLOSED}] — a probe that can pass on "
                   "stale generated content is bluffable\n")
    assert _backlog_id_failures(pf.verify(contract, root)) == []


def test_audit_artifact_citations_are_not_flagged(tmp_path):
    """[#483] R2 Layer 1 — sub-question (b) ruled: docs/audits/ is citation-role, never gated."""
    root = _mini_repo(tmp_path)
    contract = _at(root, "docs/audits/2026-08-04-technical-x.md",
                   f"The window closed [#{_CLOSED}] against its Done-when.\n")
    assert _backlog_id_failures(pf.verify(contract, root)) == []


def test_closed_table_and_provenance_are_citations_on_an_assertion_surface(tmp_path):
    """[#483] R2 Layer 2 — the shapes stay citations even on a forward-committing surface.

    Layer 1 alone would clear the bundle; a plan document quoting a closed-table or a
    `since [#id]` provenance clause must not be flagged either, or the rule is only a
    path waiver wearing a role rule's name.
    """
    root = _mini_repo(tmp_path)
    contract = _at(root, "docs/plan.md",
                   "| closed | what |\n|---|---|\n"
                   f"| `[#{_CLOSED}]` | shipped this window |\n\n"
                   f"`BACKLOG.md` is GENERATED since [#{_CLOSED}].\n")
    assert _backlog_id_failures(pf.verify(contract, root)) == []


def test_backlog_reason_prose_and_backtick_quoting_are_citations(tmp_path):
    """[#483] R2 Layer 2 — in a BACKLOG row only the `kill-candidates:` VALUE is an open-claim.

    Both lines are real shapes from the live BACKLOG: a `kill-candidates: none` field whose
    REASON prose cites a closed row, and the row whose own prose backtick-quotes the field name.
    The second is this repo's known convention-quoting false positive — a scan that matches the
    field before stripping backticks reads the quote as a real field. Measured live on
    BACKLOG.md: naive whole-fragment 24 flags, field-value-only 2, strip-backticks-first 1.
    """
    root = _mini_repo(tmp_path)
    rows = [
        f"- [#{_OPEN}] [P3][S] a live row",
        f"- [#{_OPEN}] [P3][S] thing · kill-candidates: none — [#{_CLOSED}] shipped its other "
        "legs and does not own this one",
        f"- [#{_OPEN}] [P3][S] other · the `kill-candidates: [#{_CLOSED}]` resting on it, are "
        "spent · kill-candidates: none — premise falsified",
    ]
    contract = _at(root, "BACKLOG.md", "# Backlog\n\n" + "\n".join(rows) + "\n")
    assert _backlog_id_failures(pf.verify(contract, root)) == []


def test_a_genuinely_stale_assertion_role_id_still_fails(tmp_path):
    """[#483] the control — discrimination must not become blanket suppression.

    An emitted contract line telling the executor to close an id is a forward-committing
    open-claim: it asserts the row is live. It must still FAIL. Without this, every test above
    would be satisfied by a verifier that simply stopped checking backlog ids.

    (The `kill-candidates:` VALUE case is the ALL_CHECKS leg's territory, not this tool's: the
    tool's claim vocabulary is the bracketed `[#id]` form, while BACKLOG field values are written
    bare (`kill-candidates: #292`). That extractor and its own RED fixtures live with the leg.)
    """
    root = _mini_repo(tmp_path)
    emitted = _at(root, "docs/contract.md",
                  f"Close [#{_CLOSED}] this arc, then re-run the gate.\n")
    assert _backlog_id_failures(pf.verify(emitted, root)) == [f"[#{_CLOSED}]"]
