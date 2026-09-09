"""Tests for scripts/verify_handoff_probes.py — #163 handoff-probe teeth validator.

A read-only Layer-2 validator (mirrors #89 validate_doc_claims): structurally prove
every probe in a v5 bundle's PROBES.md *binds to live state* — RESOLVE-ONLY, no
subprocess (operator ruling; Critical Rule #4 "Layer 2 never executes"; zero false
positives). The §10 ladder it mechanizes:
  malformed row / missing source file / missing command target -> FAIL
  named source file present but the `#`-anchor reworded/moved   -> WARN anchor-missing
  command's executable absent from PATH                         -> skipped (degraded)
  well-formed, all named files + anchors resolve, exe present   -> PASS

Scope boundary (do NOT duplicate): the manual probe-gate still owns rationale-quality
judgment (HANDOFF_PROCESS §5); #161 owns any reusable probe-core. This is structure only.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest


import verify_handoff_probes as vhp  # noqa: E402
import audit as aud  # noqa: E402

# --- mini-bundle fixtures (a self-consistent temp repo) ---------------------

_HDR = "| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |"
_SEP = "|---|---|---|---|---|"

# A repo whose live state satisfies the live-grounded probes below.
_FILES = {
    "VISION.md": "# V\n\n## Vision\nWhat .dev-knowledge is.\n",
    "ARCHITECTURE.md": "# A\n\n## Purpose [CORE]\nLayer 2 of the ADR-28 model.\n",
    "scripts/audit.py": "ALL_CHECKS = []\n",
}

# Canonical ladder rows: (id, question, source-locator, why, verification-command).
_PASS_SYMBOL = ("P2", "how many checks are in ALL_CHECKS",
                "`ALL_CHECKS` in `scripts/audit.py`", "the count drifts every commit",
                "`python scripts/audit.py checks`")
_PASS_ANCHOR = ("P1a", "quote the opening line of Vision",
                "`VISION.md` `## Vision`", "a paraphrase is not a substring",
                "`grep -A4 '^## Vision' VISION.md`")
_FAIL_MISSING = ("PX", "answer from a ghost file",
                 "`GHOST.md`", "nothing live binds here",
                 "`grep x GHOST.md`")
_ANCHOR_MOVED = ("PY", "quote a reworded section",
                 "`VISION.md` `## Gone`", "the anchor moved",
                 "`grep x VISION.md`")
_MALFORMED = ("PZ", "missing its command cell",
              "`VISION.md`", "the row is incomplete", "")
# P5 false-FAIL trap: secondary backtick span names `audit.py` (no scripts/ prefix,
# absent at repo root). First-span-only extraction must keep this a PASS.
_P5_TRAP = ("P5", "freshness relation",
            "`ARCHITECTURE.md`", "a relation over commits",
            "`git log -1 --format=%cs -- ARCHITECTURE.md` vs the stamp (or `audit.py health`)")
# Pure live-state probe with a literal `|` inside the command's backtick span.
_PIPE_CELL = ("P3", "current HEAD + tree",
              "`live git`", "the sha moves on any commit",
              "`git log | grep foo`")
# --- #207 / GAP-4 toothless rung fixtures -----------------------------------
# (1) Toothless: source binds no file/anchor, command is trivial (`git rev-parse` just
# confirms git-on-PATH) -> the silent-PASS the validator must now eliminate.
_TOOTHLESS = ("PT", "what is HEAD", "`live git`",
              "the sha moves every commit", "`git rev-parse`")
# (2) Negative controls: the SAME toothless row given a real binding token -> PASS.
_TOOTHLESS_W_ANCHOR = ("PTA", "quote the Vision opener", "`VISION.md` `## Vision`",
                       "a paraphrase is not a substring", "`git rev-parse`")
_TOOTHLESS_W_FILE = ("PTF", "is the file present", "`VISION.md`",
                     "the file may be deleted", "`git rev-parse`")
# AND-reading proof (the live P3 shape): no token, but a VALUE-bearing git command keeps
# teeth via the surfaced live value -> NOT toothless -> PASS.
_NONTRIVIAL_NOTOKEN = ("PNV", "current short HEAD sha + tree", "`live git`",
                       "the sha + sync-state move on any commit",
                       "`git rev-parse --short HEAD` then `git status -sb`")
# Earned-by-value (#207): no token + a FLAGGED-but-vacuous command — an introspection flag
# (`--is-inside-work-tree`) is operand-present yet constant-true in the probe's own context,
# so it surfaces no probe-answering value -> must FAIL (the operand-presence proxy's hole).
_VACUOUS_FLAG = ("PVF", "are we in a work tree", "`live git`",
                 "this is constant-true at probe time", "`git rev-parse --is-inside-work-tree`")
# (3) First command span valid, a LATER span names a broken path -> must be CAUGHT.
_LATER_SPAN_BROKEN = ("PLS", "compare two files", "`VISION.md`",
                      "the second target may have moved",
                      "`grep x VISION.md` then `grep y ghost/MISSING.md`")
# --- §5 / RF-1 anti-bluff rung fixtures -------------------------------------
# The exact RF-1 disease: a Why cell that bakes the answer as an `expected:` hint (the shape
# every historical architect bundle carried, e.g. 2026-06-25). Otherwise a fine live-git
# probe -> the answer-hint rung must FAIL it regardless (bluffable, §5-rejected).
_ANSWER_HINT_WHY = ("P2H", "how many checks are in ALL_CHECKS",
                    "`ALL_CHECKS` in `scripts/audit.py`",
                    "the count drifts every commit — **expected: 23, last `doc_code_edge`**",
                    "`python scripts/audit.py checks`")
# The bare-space form (`expected 23`, no colon) must also FAIL — RF-1's `/expected[ :]/`.
_ANSWER_HINT_SPACE = ("P4H", "which #ids does the drift check flag",
                      "`BACKLOG.md` ∩ live git", "computed at answer-time — expected 77 only",
                      "`python scripts/validate_git_backlog.py`")


def _table(rows, hdr=_HDR, sep=_SEP):
    lines = [hdr, sep]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines)


def _probes_md(rows, *, preamble="# Probe manifest\n<!-- scope: meta -->\n\n> contract prose\n\n## Teeth\n\n"):
    return preamble + _table(rows) + "\n"


def _init_bundle(tmp_path, rows, *, repo_files=None, slug="2026-06-12-b", probes_md=None):
    repo = tmp_path / "repo"
    bundle = repo / "docs" / "handoffs" / slug
    bundle.mkdir(parents=True)
    for rel, content in (_FILES if repo_files is None else repo_files).items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    (bundle / "PROBES.md").write_text(
        _probes_md(rows) if probes_md is None else probes_md, encoding="utf-8")
    return bundle


def _by_id(results):
    return {r.probe_id: r for r in results}


# --- pure core: split_row (the named failure mode) --------------------------

def test_split_row_basic_five_columns():
    cells = vhp.split_row("| P2 | q | `s` | why | `cmd` |")
    assert cells == ["P2", "q", "`s`", "why", "`cmd`"]


def test_split_row_keeps_pipe_inside_backtick_span():
    # THE named failure mode: a literal `|` inside a backtick code span must NOT split
    # the row. `git log | grep foo` is ONE cell, so the row still has 5 columns.
    line = "| P3 | q | `live git` | why | `git log | grep foo` |"
    cells = vhp.split_row(line)
    assert len(cells) == 5
    assert cells[4] == "`git log | grep foo`"
    assert "|" in cells[4]  # the pipe survived inside the command cell


def test_backtick_spans_returns_all_contents():
    assert vhp.backtick_spans("`ALL_CHECKS` in `scripts/audit.py`") == [
        "ALL_CHECKS", "scripts/audit.py"]


def test_first_span_returns_only_the_first():
    # P5-trap fixture: first span is the canonical command; the `audit.py` shorthand is later.
    cmd = "`git log -1 -- ARCHITECTURE.md` vs the stamp (or `audit.py health`)"
    assert vhp.first_span(cmd) == "git log -1 -- ARCHITECTURE.md"


# --- pure core: token extraction --------------------------------------------

def test_file_tokens_extracts_paths_not_args_or_symbols():
    toks = vhp.file_tokens("`python scripts/audit.py checks`")
    assert "scripts/audit.py" in toks
    assert "checks" not in toks and "python" not in toks


def test_file_tokens_ignores_non_path_symbols():
    # ALL_CHECKS / **N collected** are not file paths -> never resolved (precision-over-recall).
    assert vhp.file_tokens("`ALL_CHECKS` `**N collected**` live git") == []


def test_file_tokens_leading_dot_is_additive_only():
    """R7 v1 ([#421] absorbed into [#446]): admitting a leading dot in the FINAL segment must
    ADD the repo-root-dotfile bindings without changing ANY shape that already tokenized.

    The negative control is the point. A bare `\\.?` (no boundary lookbehind) passes the two
    dotfile cases but silently REGRESSES `a.audit.py` -> [] and `deploy/manifest-v1.4.0.yaml`
    -> [], because the optional dot starts the match one character early. This test pins the
    additive property, not just the fix."""
    # ADDED by R7 v1 — repo-root dotfiles now keep their dot.
    assert vhp.file_tokens("`.pre-commit-config.yaml`") == [".pre-commit-config.yaml"]
    assert vhp.file_tokens("`.markdownlint.json`") == [".markdownlint.json"]
    assert vhp.file_tokens("sub/.hidden.yaml") == ["sub/.hidden.yaml"]
    # UNCHANGED — every shape that tokenized before tokenizes identically now.
    for text, want in (
        ("`scripts/audit.py`", ["scripts/audit.py"]),
        ("`python scripts/audit.py checks`", ["scripts/audit.py"]),
        ("`.claude/settings.json`", [".claude/settings.json"]),
        ("`grep x VISION.md` then `grep y sub/OTHER.md`", ["VISION.md", "sub/OTHER.md"]),
        # NARROWED by F4 (codex HIGH, 2026-07-31): both used to yield a MIS-PARSE — `audit.py`
        # extracted from the middle of `a.audit.py`, and the garbage token `0.yaml` that never
        # resolved. The whole-token boundary that closes the prefixed-dotfile hole removes both.
        # Declared here rather than silently dropped: no real binding is lost.
        ("a.audit.py", []),
        ("deploy/manifest-v1.4.0.yaml", []),
        ("`ALL_CHECKS` `**N collected**` live git", []),
        ("`docs/intake/*.md`", []),
    ):
        assert vhp.file_tokens(text) == want, text


def test_file_tokens_reject_prefixed_dotfiles():
    """REGRESSION (codex HIGH, 2026-07-31): the leading-dot lookbehind guarded only the DOT,
    not the start of the whole token. So a dotfile behind an absolute / URL / escaping prefix
    still tokenized, and `_resolve_path`'s unique-basename fallback then bound it to the
    repo-root file — a false PASS where the old regex produced a miss (FAIL, teeth intact).

    `../.methodology.yaml` is the sharp case: an explicit repo ESCAPE that resolved. The
    containment guard in `_within_repo_file` blocks the literal path, but the basename
    fallback walked around it. A repo-relative token cannot start with `/`, `../`, or a
    host segment, so none of these may tokenize at all."""
    repo = Path(vhp._REPO_ROOT)
    # (a) Not a repo-relative path at all — absolute, URL, drive-qualified, backslash escape.
    #     These may not tokenize: there is nothing here a probe could legitimately mean.
    for text in ("/.methodology.yaml", "https://host/.methodology.yaml",
                 "C:/x/.methodology.yaml", "..\\.methodology.yaml"):
        assert vhp.file_tokens(text) == [], f"still tokenizes: {text}"
    # (b) A `..` escape DOES tokenize on purpose — an escaping locator has to be SEEN to be
    #     FAILed; suppressing the token would turn a missing-target FAIL into a silent PASS.
    #     It is refused at RESOLUTION instead, which is the property that actually matters.
    for text in ("../.methodology.yaml", "../scripts/gen_task_tree.py", "../outside.md"):
        toks = vhp.file_tokens(text)
        assert toks, f"escape must stay visible to the FAIL rung: {text}"
        assert [t for t in toks if vhp._resolve_path(repo, t) is not None] == [], \
            f"escape resolved via the basename fallback: {text} -> {toks}"


def test_file_tokens_still_bind_legitimate_dotfiles():
    """The F4 narrowing must not undo R7 v1: a repo-ROOT dotfile and a nested dotfile under a
    normal relative dir still bind (the frozen FR7v1 contract), and every non-dotfile shape is
    untouched."""
    assert vhp.file_tokens("`.pre-commit-config.yaml`") == [".pre-commit-config.yaml"]
    assert vhp.file_tokens("`.markdownlint.json`") == [".markdownlint.json"]
    assert vhp.file_tokens("sub/.hidden.yaml") == ["sub/.hidden.yaml"]
    assert vhp.file_tokens("`.claude/settings.json`") == [".claude/settings.json"]
    assert vhp.file_tokens("`python scripts/audit.py checks`") == ["scripts/audit.py"]
    # An ESCAPE still tokenizes on purpose — it has to be SEEN to be FAILed. It is refused at
    # resolution instead (see _resolve_path / test_resolve_rejects_path_escaping_repo_root).
    assert vhp.file_tokens("../outside.md") == ["../outside.md"]
    assert vhp._resolve_path(Path(vhp._REPO_ROOT), "../outside.md") is None


def test_header_tokens_only_picks_markdown_headers():
    toks = vhp.header_tokens("`VISION.md` `## Vision`")
    assert toks == ["## Vision"]


def test_header_tokens_reject_a_bare_ticket_id():
    """R7 v2: a header ATX-opens (`#`x1-6 + whitespace); `#421` is a ticket id, not an anchor.
    The old `startswith('#')` test gave a row that merely CITED a ticket a spurious
    `anchor-missing` WARN."""
    assert vhp.header_tokens("absorbed into `#421` this window") == []
    assert vhp.header_tokens("`#446` `#12345`") == []
    # Real headers, every ATX depth, still bind.
    assert vhp.header_tokens("`# T` `## Vision` `###### Deep`") == ["# T", "## Vision", "###### Deep"]
    # Not a header: no whitespace after the hashes.
    assert vhp.header_tokens("`##Nospace`") == []


def test_lead_exe_is_first_command_token():
    assert vhp.lead_exe("python scripts/audit.py checks") == "python"
    assert vhp.lead_exe("git log -1") == "git"


def test_command_file_tokens_scans_all_spans_not_just_first():
    # #207/GAP-4: file tokens are pulled from EVERY command span, so a broken path in a
    # secondary span is visible (the first-span-only blind spot is closed).
    toks = vhp._command_file_tokens("`grep x VISION.md` then `grep y sub/OTHER.md`")
    assert toks == ["VISION.md", "sub/OTHER.md"]


def test_is_trivial_command_distinguishes_value_bearing_commands():
    # #207/GAP-4: a bare exe / `exe subcommand` is trivial (asserts only tool presence);
    # any further operand surfaces a specific live value -> NOT trivial.
    assert vhp._is_trivial_command("git rev-parse")        # exe + bare subcommand
    assert vhp._is_trivial_command("pytest")               # bare exe
    assert not vhp._is_trivial_command("git rev-parse --short HEAD")
    assert not vhp._is_trivial_command("git status -sb")
    assert not vhp._is_trivial_command("git log | grep foo")
    # #207 earned-by-value: operand PRESENCE alone is too weak a proxy — a 3-token command
    # whose only operand is a vacuous introspection flag surfaces no state-specific value
    # (`--is-inside-work-tree` is constant-true in the probe's own context) -> still trivial.
    assert vhp._is_trivial_command("git rev-parse --is-inside-work-tree")
    assert vhp._is_trivial_command("git --version")
    # ...but a mix of vacuous + a state-bearing operand is NOT trivial (recall guard).
    assert not vhp._is_trivial_command("git rev-parse --is-inside-work-tree --short HEAD")


# --- pure core: parse_probes (header-name mapping, multi-table) --------------

def test_parse_probes_maps_columns_by_header_name_ignoring_id_col():
    rows = vhp.parse_probes(_probes_md([_PASS_SYMBOL]))
    assert len(rows) == 1
    r = rows[0]
    assert r["id"] == "P2"
    assert "ALL_CHECKS" in r["source"]
    assert r["command"] == "`python scripts/audit.py checks`"
    assert r["question"].startswith("how many")
    assert r["why"]


def test_parse_probes_skips_non_probe_tables():
    other = "| a | b |\n|---|---|\n| 1 | 2 |\n"
    md = other + "\n" + _probes_md([_PASS_SYMBOL])
    rows = vhp.parse_probes(md)
    assert [r["id"] for r in rows] == ["P2"]


def test_parse_probes_reads_multiple_probe_tables():
    md = (_probes_md([_PASS_ANCHOR])
          + "\n## More teeth\n\n" + _table([_PASS_SYMBOL]) + "\n")
    rows = vhp.parse_probes(md)
    assert {r["id"] for r in rows} == {"P1a", "P2"}


# --- verify(): the §10 ladder -----------------------------------------------

def test_verify_pass_on_live_grounded_symbol_probe(tmp_path):
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL])
    by = _by_id(vhp.verify(bundle))
    assert by["P2"].status == "pass"


@pytest.mark.skipif(shutil.which("grep") is None, reason="grep not in PATH")
def test_verify_pass_on_live_grounded_anchor_probe(tmp_path):
    bundle = _init_bundle(tmp_path, [_PASS_ANCHOR])
    by = _by_id(vhp.verify(bundle))
    assert by["P1a"].status == "pass"


def test_verify_fail_on_missing_source_no_live_binding(tmp_path):
    # bluffable / no live binding: the named file does not exist -> FAIL (never pass).
    bundle = _init_bundle(tmp_path, [_FAIL_MISSING])
    by = _by_id(vhp.verify(bundle))
    assert by["PX"].status == "fail"


def test_verify_anchor_missing_does_not_silent_pass(tmp_path):
    # file present, the `#`-anchor reworded away -> WARN anchor-missing (NOT pass, NOT fail).
    bundle = _init_bundle(tmp_path, [_ANCHOR_MOVED])
    by = _by_id(vhp.verify(bundle))
    assert by["PY"].status == "anchor-missing"
    assert by["PY"].status != "pass"


def test_verify_fail_on_malformed_row(tmp_path):
    bundle = _init_bundle(tmp_path, [_MALFORMED])
    by = _by_id(vhp.verify(bundle))
    assert by["PZ"].status == "fail"
    assert "malformed" in by["PZ"].detail.lower()


def test_verify_fail_on_command_cell_without_backtick_span(tmp_path):
    # codex HIGH: a non-empty command cell with NO backtick span -> cmd == "" must NOT
    # fall through to a silent PASS; it ships no runnable command -> malformed FAIL.
    row = ("PNB", "no real command", "`VISION.md`", "why", "run the grep yourself")
    bundle = _init_bundle(tmp_path, [row])
    by = _by_id(vhp.verify(bundle))
    assert by["PNB"].status == "fail"
    assert "malformed" in by["PNB"].detail.lower()


def test_verify_p5_trap_secondary_span_does_not_false_fail(tmp_path):
    # ARCHITECTURE.md exists; the 2nd-span `audit.py health` shorthand carries the real
    # file token `audit.py`, which now (#207/GAP-4, all-span resolution) resolves via the
    # unique-basename fallback to scripts/audit.py -> a resolvable shorthand must not
    # false-FAIL even though all command spans are scanned. P5 stays PASS.
    bundle = _init_bundle(tmp_path, [_P5_TRAP])
    by = _by_id(vhp.verify(bundle))
    assert by["P5"].status == "pass"


def test_verify_pipe_in_backtick_command_parses_and_passes(tmp_path):
    # The pipe inside the command must not break parsing; pure-git probe -> pass (git present).
    bundle = _init_bundle(tmp_path, [_PIPE_CELL])
    by = _by_id(vhp.verify(bundle))
    assert "P3" in by
    assert by["P3"].status == "pass"


# --- #207 / GAP-4: toothless live-git probe must not silent-PASS ------------

def test_verify_fail_on_toothless_live_git_zero_token_probe(tmp_path):
    # FROZEN CONTRACT (1): a `live git` row with NO file/anchor token + a trivial command
    # (`git rev-parse`, which only confirms git-on-PATH) must FAIL -> the silent-PASS the
    # old ladder gave such a probe is eliminated.
    bundle = _init_bundle(tmp_path, [_TOOTHLESS])
    by = _by_id(vhp.verify(bundle))
    assert by["PT"].status == "fail"
    assert by["PT"].status != "pass"
    assert "toothless" in by["PT"].detail.lower()


def test_verify_fail_on_flagged_but_vacuous_live_git_probe(tmp_path):
    # FROZEN CONTRACT, earned-by-value (#207): a `live git` row with NO file/anchor token
    # whose command IS operand-bearing but VACUOUS (`git rev-parse --is-inside-work-tree`,
    # constant-true at probe time) must FAIL — operand presence does not earn teeth. This is
    # the exact hole the operand-presence proxy left open before the discriminator tightened.
    bundle = _init_bundle(tmp_path, [_VACUOUS_FLAG])
    by = _by_id(vhp.verify(bundle))
    assert by["PVF"].status == "fail"
    assert "toothless" in by["PVF"].detail.lower()


def test_verify_toothless_passes_with_anchor_token(tmp_path):
    # FROZEN CONTRACT (2), anchor leg: the SAME trivial command, but now the source binds a
    # real `#`-anchor (resolvable in VISION.md) -> a binding token exists -> PASS.
    bundle = _init_bundle(tmp_path, [_TOOTHLESS_W_ANCHOR])
    by = _by_id(vhp.verify(bundle))
    assert by["PTA"].status == "pass"


def test_verify_toothless_passes_with_file_token(tmp_path):
    # FROZEN CONTRACT (2), file leg: the SAME trivial command, but the source names a real
    # file token (VISION.md) -> a binding token exists -> PASS.
    bundle = _init_bundle(tmp_path, [_TOOTHLESS_W_FILE])
    by = _by_id(vhp.verify(bundle))
    assert by["PTF"].status == "pass"


def test_verify_no_token_but_value_bearing_command_still_passes(tmp_path):
    # AND-reading guard (the live P3 shape): no file/anchor token, but a VALUE-bearing git
    # command surfaces a specific live value -> keeps its teeth -> PASS (NOT toothless).
    # This is why the live bundle's pure-git P3 stays green.
    bundle = _init_bundle(tmp_path, [_NONTRIVIAL_NOTOKEN])
    by = _by_id(vhp.verify(bundle))
    assert by["PNV"].status == "pass"


def test_verify_later_command_span_broken_path_is_caught(tmp_path):
    # FROZEN CONTRACT (3): the FIRST command span resolves (grep x VISION.md), but a LATER
    # span names a broken path (ghost/MISSING.md) -> CAUGHT as missing source/target, never
    # silent-passed on the strength of the first span alone.
    bundle = _init_bundle(tmp_path, [_LATER_SPAN_BROKEN])
    by = _by_id(vhp.verify(bundle))
    assert by["PLS"].status == "fail"
    assert "ghost/MISSING.md" in by["PLS"].detail


# --- §5 / RF-1: the anti-bluff answer-hint rung -----------------------------

def test_verify_fail_on_answer_hint_in_why_cell(tmp_path):
    # RF-1: a row that prints its answer as `expected: <value>` is bluffable -> FAIL, even
    # though the probe is otherwise well-formed and live-grounded. This is the exact
    # regression the historical bundles (2026-06-25 etc.) shipped in the Why column.
    by = _by_id(vhp.verify(_init_bundle(tmp_path, [_ANSWER_HINT_WHY])))
    assert by["P2H"].status == "fail"
    assert "answer-hint" in by["P2H"].detail.lower()


def test_verify_fail_on_answer_hint_bare_space_form(tmp_path):
    # RF-1's `/expected[ :]/` also catches the colon-less `expected 77` form.
    by = _by_id(vhp.verify(_init_bundle(tmp_path, [_ANSWER_HINT_SPACE])))
    assert by["P4H"].status == "fail"
    assert "answer-hint" in by["P4H"].detail.lower()


def test_verify_clean_row_without_answer_hint_still_passes(tmp_path):
    # Negative control: the rung must not fire on an honest probe (no `expected:` in any
    # cell) — _PASS_SYMBOL binds live and carries no answer value -> PASS.
    by = _by_id(vhp.verify(_init_bundle(tmp_path, [_PASS_SYMBOL])))
    assert by["P2"].status == "pass"


def test_anti_bluff_rung_ignores_expected_in_preamble_prose(tmp_path):
    # The rung is ROW-scoped: `expected:` in the PREAMBLE (the manifest's own anti-bluff
    # note) is not a table row, so parse_probes never yields it and _classify never sees it.
    # This is the live 2026-07-04-bundle property (its only `expected:` is preamble prose).
    preamble = ("# Probe manifest\n<!-- scope: meta -->\n\n"
                "> RF-1: recent bundles printed answers as `expected: <value>` hints — "
                "withheld here by construction.\n\n## Teeth\n\n")
    md = _probes_md([_PASS_SYMBOL], preamble=preamble)
    by = _by_id(vhp.verify(_init_bundle(tmp_path, [_PASS_SYMBOL], probes_md=md)))
    assert by["P2"].status == "pass"


def test_check_fail_class_gates_on_answer_hint_probe(tmp_path):
    # The rung reaches the DEPLOYED gate with NO audit.py edit: status 'fail' -> the adapter
    # (check_handoff_probes) maps it to a FAIL-class Finding that blocks audit-health + ship.
    repo = _repo_with_bundle(tmp_path, [_ANSWER_HINT_WHY])
    findings = aud.check_handoff_probes(repo)
    assert findings[0].status == "fail"
    assert "answer-hint" in findings[0].evidence.lower()
    assert "|" not in findings[0].evidence


def test_verify_skipped_when_executable_absent(tmp_path, monkeypatch):
    # tool absent -> skipped (degraded coverage visible), NEVER a synthesized pass.
    monkeypatch.setattr(vhp, "_exe_available", lambda name: False)
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL])
    by = _by_id(vhp.verify(bundle))
    assert by["P2"].status == "skipped"
    assert by["P2"].status != "pass"


def test_format_findings_lists_only_fails_no_pipe(tmp_path):
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL, _FAIL_MISSING])
    out = vhp.format_findings(vhp.verify(bundle))
    assert "PX" in out
    assert "P2" not in out      # a passing probe is not listed
    assert "|" not in out


# --- unique-basename fallback resolution (#163 integration hardening) --------
# A probe may name a source by bare basename for a file that lives in a subdir
# (real case: P8's `HANDOFF_PROCESS.md` for `protocols/HANDOFF_PROCESS.md`). The
# fallback resolves it IFF exactly one NON-excluded file carries that basename;
# zero or >1 still FAIL (teeth preserved); excluded-dir duplicates never count.

@pytest.mark.skipif(shutil.which("grep") is None, reason="grep not in PATH")
def test_resolve_unique_basename_without_dir_prefix_passes(tmp_path):
    # source names a bare basename whose only live copy sits in a subdir -> resolves.
    row = ("P8", "where does the boilerplate live",
           "`HANDOFF_PROCESS.md` section 13", "the collapse dropped the README",
           "`grep README protocols/HANDOFF_PROCESS.md`")
    files = {"protocols/HANDOFF_PROCESS.md": "# H\n\nno per-bundle README\n"}
    bundle = _init_bundle(tmp_path, [row], repo_files=files)
    by = _by_id(vhp.verify(bundle))
    assert by["P8"].status == "pass"


def test_resolve_ambiguous_basename_two_live_copies_fails(tmp_path):
    # the same basename in two non-excluded dirs -> ambiguous -> unresolved -> FAIL.
    row = ("PA", "names an ambiguous basename", "`DUP.md` here",
           "two live copies must not silently resolve", "`grep x a/DUP.md`")
    files = {"a/DUP.md": "x\n", "b/DUP.md": "x\n"}
    bundle = _init_bundle(tmp_path, [row], repo_files=files)
    by = _by_id(vhp.verify(bundle))
    assert by["PA"].status == "fail"
    assert "DUP.md" in by["PA"].detail


def test_resolve_zero_basename_match_fails(tmp_path):
    # a bare basename that exists nowhere -> a real miss -> FAIL (no synthesized pass).
    row = ("PB", "names a ghost basename", "`NOWHERE.md` here",
           "nothing live binds here", "`grep x VISION.md`")
    files = {"VISION.md": "v\n"}
    bundle = _init_bundle(tmp_path, [row], repo_files=files)
    by = _by_id(vhp.verify(bundle))
    assert by["PB"].status == "fail"
    assert "NOWHERE.md" in by["PB"].detail


@pytest.mark.skipif(shutil.which("grep") is None, reason="grep not in PATH")
def test_resolve_basename_ignores_excluded_dir_duplicates(tmp_path):
    # a live copy + duplicates under excluded dirs (archive*/, .claude/worktrees/…)
    # -> still exactly ONE non-excluded match -> resolves (no false-ambiguity FAIL).
    row = ("PC", "names a basename with archived/worktree twins", "`SPEC.md` section",
           "an excluded-dir copy must not create ambiguity", "`grep x sub/SPEC.md`")
    files = {
        "sub/SPEC.md": "live\n",
        "archive/old/SPEC.md": "stale\n",
        ".claude/worktrees/w/sub/SPEC.md": "worktree dup\n",
    }
    bundle = _init_bundle(tmp_path, [row], repo_files=files)
    by = _by_id(vhp.verify(bundle))
    assert by["PC"].status == "pass"


def test_resolve_rejects_path_escaping_repo_root(tmp_path):
    # a token that escapes repo_root (`../outside.md`) must NOT bind, even though the
    # file exists on disk -- containment keeps the validator's teeth (codex HIGH).
    (tmp_path / "outside.md").write_text("ghost\n", encoding="utf-8")  # sibling of repo/
    row = ("PD", "names a path escaping the repo", "`../outside.md` here",
           "an out-of-repo file must not satisfy a probe", "`grep x VISION.md`")
    files = {"VISION.md": "v\n"}
    bundle = _init_bundle(tmp_path, [row], repo_files=files)
    by = _by_id(vhp.verify(bundle))
    assert by["PD"].status == "fail"
    assert "outside.md" in by["PD"].detail


def test_resolve_rejects_direct_path_under_excluded_dir(tmp_path):
    # a full direct path under an excluded tree (.claude/worktrees) must not bind --
    # exclusions apply to the literal path, not just the fallback (codex HIGH).
    row = ("PE", "names a worktree-duplicate path directly",
           "`.claude/worktrees/w/SPEC.md` here", "a duplicate copy must not satisfy a probe",
           "`grep x VISION.md`")
    files = {"VISION.md": "v\n", ".claude/worktrees/w/SPEC.md": "dup\n"}
    bundle = _init_bundle(tmp_path, [row], repo_files=files)
    by = _by_id(vhp.verify(bundle))
    assert by["PE"].status == "fail"


# --- deployed audit check: check_handoff_probes -----------------------------

def _repo_with_bundle(tmp_path, rows, **kw):
    return _init_bundle(tmp_path, rows, **kw).parents[2]


def test_check_passes_when_no_probe_bundle(tmp_path):
    findings = aud.check_handoff_probes(tmp_path)
    assert len(findings) == 1
    assert findings[0].check_name == "handoff_probes"
    assert findings[0].status == "n/a"  # [#465] leg 1


def test_check_fail_class_gates_on_a_failing_probe(tmp_path):
    repo = _repo_with_bundle(tmp_path, [_FAIL_MISSING])
    findings = aud.check_handoff_probes(repo)
    assert findings[0].status == "fail"        # FAIL-class -> blocks /ship
    assert "|" not in findings[0].evidence


def test_check_fail_class_gates_on_a_toothless_probe(tmp_path):
    # #207/GAP-4: a toothless live-git probe is a FAIL-class Finding (blocks audit-health +
    # ship-gate), not a silent pass — the validator's teeth reach the deployed gate.
    repo = _repo_with_bundle(tmp_path, [_TOOTHLESS])
    findings = aud.check_handoff_probes(repo)
    assert findings[0].status == "fail"
    assert "toothless" in findings[0].evidence.lower()
    assert "|" not in findings[0].evidence


def test_check_warns_on_anchor_missing(tmp_path):
    repo = _repo_with_bundle(tmp_path, [_ANCHOR_MOVED])
    findings = aud.check_handoff_probes(repo)
    assert findings[0].status == "warn"
    assert "anchor" in findings[0].evidence.lower()


@pytest.mark.skipif(shutil.which("grep") is None, reason="grep not in PATH")
def test_check_passes_when_all_probes_bind(tmp_path):
    repo = _repo_with_bundle(tmp_path, [_PASS_SYMBOL, _PASS_ANCHOR])
    assert aud.check_handoff_probes(repo)[0].status == "pass"


def test_check_validates_latest_bundle_only(tmp_path):
    # An OLDER broken bundle must be ignored; only the LATEST (lexically max slug) is validated.
    repo = tmp_path / "repo"
    _init_bundle(tmp_path, [_FAIL_MISSING], slug="2026-06-01-old")
    # second bundle (latest) is clean
    bundle2 = repo / "docs" / "handoffs" / "2026-06-12-new"
    bundle2.mkdir(parents=True)
    (bundle2 / "PROBES.md").write_text(_probes_md([_PASS_SYMBOL]), encoding="utf-8")
    findings = aud.check_handoff_probes(repo)
    assert findings[0].status == "pass"        # older broken bundle ignored


def test_check_fails_on_empty_probe_manifest(tmp_path):
    # codex HIGH: a PROBES.md present but with NO parseable probe rows is a toothless
    # manifest -> FAIL (not a silent pass). The bundle was selected *because* it has a
    # PROBES.md, so empty results mean the manifest itself is the defect.
    bundle = _init_bundle(tmp_path, [], probes_md="# Probe manifest\n\njust prose, no table.\n")
    findings = aud.check_handoff_probes(bundle.parents[2])
    assert findings[0].status == "fail"
    assert "toothless" in findings[0].evidence.lower() or "no parseable" in findings[0].evidence.lower()


def test_check_emits_one_finding_per_degraded_probe(tmp_path):
    # codex HIGH: degraded probes must be ONE Finding each (per-probe ship-gate
    # disposition), not a single collapsed WARN that one disposition could mask.
    a1 = ("PA1", "q", "`VISION.md` `## Gone1`", "why", "`grep x VISION.md`")
    a2 = ("PA2", "q", "`VISION.md` `## Gone2`", "why", "`grep x VISION.md`")
    repo = _repo_with_bundle(tmp_path, [a1, a2])
    findings = aud.check_handoff_probes(repo)
    assert len(findings) == 2
    assert all(f.status == "warn" for f in findings)
    assert any("PA1" in f.evidence for f in findings)
    assert any("PA2" in f.evidence for f in findings)


def test_check_failsoft_on_error(tmp_path, monkeypatch):
    repo = _repo_with_bundle(tmp_path, [_PASS_SYMBOL])

    def _boom(*a, **k):
        raise RuntimeError("parser exploded")

    monkeypatch.setattr(aud._vhp, "verify", _boom)
    findings = aud.check_handoff_probes(repo)
    assert findings[0].status == "warn"
    assert "exploded" in findings[0].evidence or "degraded" in findings[0].evidence


def test_check_is_registered_in_all_checks():
    assert aud.check_handoff_probes in aud.ALL_CHECKS
    names = [c.__name__.removeprefix("check_") for c in aud.ALL_CHECKS]
    assert "handoff_probes" in names


@pytest.mark.live_repo
def test_registered_check_never_fails_on_live_repo():
    # Production contract: the live hub's latest bundle must resolve (pass/warn), never FAIL.
    findings = aud.check_handoff_probes(Path(aud._REPO_ROOT))
    assert findings[0].status in {"pass", "warn"}


# --- cross-repo bundle resolution (ADR-36/41 — probes bind to a TARGET repo) -
# A handoff bundle lives in the hub but its probes may bind to a DIFFERENT (target) repo
# (fleet onboarding, #221). check_handoff_probes reads the bundle's `Target repo` row and
# resolves against the target root; a foreign `.claude/` or ambiguous basename degrades to
# WARN (honest-partial), a genuine miss still FAILs, a real target file PASSes. #234 hardens
# the `.claude/` case to full FAIL teeth.

def _crossrepo_bundle(tmp_path, rows, target="tgt", slug="2026-07-02-x"):
    """A hub bundle whose HANDOFF_BOOT.md declares a cross-repo target + the sibling target
    repo on disk. Returns (hub_root, bundle_dir, target_root)."""
    hub = tmp_path / "hub"
    bundle = hub / "docs" / "handoffs" / slug
    bundle.mkdir(parents=True)
    (bundle / "PROBES.md").write_text(_probes_md(rows), encoding="utf-8")
    (bundle / "HANDOFF_BOOT.md").write_text(
        "# boot\n\n| Field | Value |\n|---|---|\n"
        f"| **Target repo** | **`{target}`** (cross-repo, ADR-36/41) |\n", encoding="utf-8")
    tgt = tmp_path / target
    tgt.mkdir()
    return hub, bundle, tgt


def test_resolve_status_classifies_tokens(tmp_path):
    repo = tmp_path / "t"
    (repo / "docs" / "sub").mkdir(parents=True)
    (repo / ".claude").mkdir()
    (repo / "VISION.md").write_text("v\n", encoding="utf-8")
    (repo / "docs" / "A.md").write_text("a\n", encoding="utf-8")
    (repo / "docs" / "sub" / "A.md").write_text("a2\n", encoding="utf-8")   # 2nd copy
    (repo / ".claude" / "guard.py").write_text("x\n", encoding="utf-8")
    assert vhp._resolve_status(repo, "VISION.md") == "resolved"       # unique basename
    assert vhp._resolve_status(repo, ".claude/guard.py") == "excluded"  # excluded-dir path
    assert vhp._resolve_status(repo, "A.md") == "ambiguous"           # two live copies
    assert vhp._resolve_status(repo, "GHOST.md") == "missing"         # a genuine miss


def test_bundle_target_repo_parses_row(tmp_path):
    _, bundle, _ = _crossrepo_bundle(tmp_path, [_PASS_SYMBOL], target="ai-council")
    assert aud._bundle_target_repo(bundle) == "ai-council"


def test_bundle_target_repo_none_when_no_boot_or_row(tmp_path):
    # a self-handoff bundle (no HANDOFF_BOOT.md) -> None -> treated as same-repo.
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL])
    assert aud._bundle_target_repo(bundle) is None


def test_verify_cross_repo_excluded_target_is_warn_not_fail(tmp_path):
    # a foreign `.claude/` target -> WARN (skipped), never a fake-FAIL nor a fake-PASS.
    row = ("P5", "is the floor armed", "`.claude/guard.py` here",
           "armed is a runtime property", "`python .claude/guard.py`")
    _, bundle, tgt = _crossrepo_bundle(tmp_path, [row])
    (tgt / ".claude").mkdir()
    (tgt / ".claude" / "guard.py").write_text("x\n", encoding="utf-8")
    by = _by_id(vhp.verify(bundle, repo_root=tgt, cross_repo=True))
    assert by["P5"].status == "skipped"
    assert "excluded" in by["P5"].detail


def test_verify_cross_repo_ambiguous_target_is_warn(tmp_path):
    row = ("PAM", "reads an ambiguous basename", "`DUP.md` here",
           "two copies in the target", "`grep x a/DUP.md`")
    _, bundle, tgt = _crossrepo_bundle(tmp_path, [row])
    (tgt / "a").mkdir()
    (tgt / "b").mkdir()
    (tgt / "a" / "DUP.md").write_text("x\n", encoding="utf-8")
    (tgt / "b" / "DUP.md").write_text("x\n", encoding="utf-8")
    by = _by_id(vhp.verify(bundle, repo_root=tgt, cross_repo=True))
    assert by["PAM"].status == "skipped"
    assert "ambiguous" in by["PAM"].detail


def test_verify_cross_repo_missing_target_still_fails(tmp_path):
    # a genuine miss in the foreign repo KEEPS full FAIL teeth (not softened to WARN).
    row = ("PM", "reads a ghost", "`ghost/GONE.md` here",
           "nothing binds", "`grep x ghost/GONE.md`")
    _, bundle, tgt = _crossrepo_bundle(tmp_path, [row])
    by = _by_id(vhp.verify(bundle, repo_root=tgt, cross_repo=True))
    assert by["PM"].status == "fail"
    assert "GONE.md" in by["PM"].detail


@pytest.mark.skipif(shutil.which("grep") is None, reason="grep not in PATH")
def test_verify_cross_repo_resolved_target_passes(tmp_path):
    # a real file in the TARGET repo resolves against the target root -> PASS (teeth kept).
    row = ("PR", "reads a real target file", "`ONLY_IN_TARGET.md` here",
           "the file is in the target repo", "`grep x ONLY_IN_TARGET.md`")
    _, bundle, tgt = _crossrepo_bundle(tmp_path, [row])
    (tgt / "ONLY_IN_TARGET.md").write_text("t\n", encoding="utf-8")
    by = _by_id(vhp.verify(bundle, repo_root=tgt, cross_repo=True))
    assert by["PR"].status == "pass"


def test_check_cross_repo_resolves_against_target_no_false_fail(tmp_path):
    # the probe binds to a file present ONLY in the target repo; check_handoff_probes must
    # resolve against the target (via the Target-repo row) -> no false FAIL.
    row = ("PR", "reads a target file", "`ONLY_IN_TARGET.md` here",
           "lives only in the target repo", "`grep x ONLY_IN_TARGET.md`")
    hub, _, tgt = _crossrepo_bundle(tmp_path, [row])
    (tgt / "ONLY_IN_TARGET.md").write_text("t\n", encoding="utf-8")
    findings = aud.check_handoff_probes(hub)
    assert all(f.status in {"pass", "warn"} for f in findings)  # never FAIL cross-repo-resolved


def test_check_cross_repo_target_absent_is_warn_not_fail(tmp_path):
    # target repo not present as a sibling -> a single non-gating WARN, never FAIL.
    hub = tmp_path / "hub"
    bundle = hub / "docs" / "handoffs" / "2026-07-02-x"
    bundle.mkdir(parents=True)
    (bundle / "PROBES.md").write_text(_probes_md([_PASS_SYMBOL]), encoding="utf-8")
    (bundle / "HANDOFF_BOOT.md").write_text(
        "| **Target repo** | **`nope-not-here`** |\n", encoding="utf-8")
    findings = aud.check_handoff_probes(hub)
    assert len(findings) == 1
    assert findings[0].status == "warn"
    assert "not present" in findings[0].evidence


def test_check_self_handoff_target_row_not_treated_cross_repo(tmp_path):
    # a 'Target repo' equal to this repo's own name is a self-handoff -> resolve same-repo.
    hub = tmp_path / "hub"
    bundle = hub / "docs" / "handoffs" / "2026-07-02-x"
    bundle.mkdir(parents=True)
    (hub / "scripts").mkdir()
    (hub / "scripts" / "audit.py").write_text("ALL_CHECKS = []\n", encoding="utf-8")
    (bundle / "PROBES.md").write_text(_probes_md([_PASS_SYMBOL]), encoding="utf-8")
    (bundle / "HANDOFF_BOOT.md").write_text(
        "| **Target repo** | **`hub`** |\n", encoding="utf-8")  # == repo dir name
    findings = aud.check_handoff_probes(hub)
    assert findings[0].status == "pass"  # resolved against the hub itself, not cross-repo


# ---------------------------------------------------------------------------
# [#372] Active-bundle SELECTION: git add-date, never slug order.
# ---------------------------------------------------------------------------


def _git_repo(root: Path):
    """Make `root` a throwaway git repo; returns a runner. (tests/test_fleet_parity.py idiom.)"""
    root.mkdir(parents=True, exist_ok=True)

    def run(args, env=None, check=True):
        p = subprocess.run(["git", *args], cwd=str(root), capture_output=True,
                           text=True, encoding="utf-8", errors="replace",
                           env=None if env is None else {**os.environ, **env})
        # A silently-failing fixture is worse than no fixture: if the SECOND commit fails,
        # its bundle stays uncommitted and then wins as "fresh" -- so the selection tests
        # would pass for entirely the wrong reason.
        if check:
            assert p.returncode == 0, f"git {' '.join(args)} failed: {p.stderr.strip()}"
        return p

    if run(["init", "-q", "-b", "main"], check=False).returncode != 0:
        run(["init", "-q"])
    for cfg in (["core.autocrlf", "false"], ["user.email", "hp@example.com"],
                ["user.name", "Handoff Probe Test"], ["commit.gpgsign", "false"]):
        run(["config", *cfg])
    return run


def _commit_at(run, pathspec: str, when: str, msg: str):
    """Commit `pathspec` with BOTH author and committer dates pinned, so add-date ordering
    under test is deterministic and independent of wall-clock or checkout mtime. Every
    invocation is return-code checked (see _git_repo.run)."""
    run(["add", "--", pathspec])
    run(["commit", "-q", "-m", msg],
        env={"GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when})
    # Prove the commit actually landed AND carries the pinned date -- the add-date ordering
    # under test is meaningless if either silently drifted.
    got = run(["log", "-1", "--format=%at", "--", pathspec]).stdout.strip()
    assert got, f"no commit recorded for {pathspec}"
    return int(got)


_needs_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not in PATH")


def _arc5_shaped(tmp_path):
    """The live defect's exact shape: '<date>-x-arc5' sorts AFTER '<date>-x' (because
    '-arc5' > ''), yet arc5 was added EARLIER. arc5 carries a FAILING probe, the plain
    slug a passing one, so the selected bundle is legible from the verdict alone."""
    _init_bundle(tmp_path, [_FAIL_MISSING], slug="2026-07-20-x-arc5")
    repo = tmp_path / "repo"
    plain = repo / "docs" / "handoffs" / "2026-07-20-x"
    plain.mkdir(parents=True)
    (plain / "PROBES.md").write_text(_probes_md([_PASS_SYMBOL]), encoding="utf-8")
    run = _git_repo(repo)
    t_arc5 = _commit_at(run, "docs/handoffs/2026-07-20-x-arc5",
                        "2026-07-19T14:42:52+02:00", "arc5")
    t_plain = _commit_at(run, ".", "2026-07-20T17:04:33+02:00", "plain + repo files")
    # The premise of every test built on this fixture: arc5 is LEXICALLY LAST but
    # CHRONOLOGICALLY FIRST. If either half stops holding, the tests below are vacuous.
    assert t_arc5 < t_plain, "fixture premise broken: arc5 must be the OLDER add"
    assert max("2026-07-20-x-arc5", "2026-07-20-x") == "2026-07-20-x-arc5"
    return repo


@_needs_git
def test_check_selects_bundle_by_git_add_date_not_slug_order(tmp_path):
    """Lexical-max validated the STALE arc5 bundle and reported about the wrong file,
    while the actually-active bundle went unchecked. mtime cannot substitute: a worktree
    checkout re-stamps every file."""
    findings = aud.check_handoff_probes(_arc5_shaped(tmp_path))
    assert findings[0].status == "pass"
    assert "2026-07-20-x" in findings[0].evidence
    assert "arc5" not in findings[0].evidence


@_needs_git
def test_check_prefers_the_uncommitted_bundle_over_every_tracked_one(tmp_path):
    """A freshly generated bundle has no add-commit (untracked, or `git add`ed by the very
    pre-commit run validating it). It IS the active handoff, so it outranks every committed
    bundle. Deliberately lexically SMALLEST and FAILING, so slug order cannot fake the pass."""
    _init_bundle(tmp_path, [_PASS_SYMBOL], slug="2026-07-25-zzz-committed")
    repo = tmp_path / "repo"
    run = _git_repo(repo)
    _commit_at(run, ".", "2026-07-25T09:00:00+02:00", "committed bundle")

    live = repo / "docs" / "handoffs" / "2026-07-01-aaa-live"
    live.mkdir(parents=True)
    (live / "PROBES.md").write_text(_probes_md([_FAIL_MISSING]), encoding="utf-8")

    findings = aud.check_handoff_probes(repo)
    assert findings[0].status == "fail"
    assert "2026-07-01-aaa-live" in findings[0].evidence


@_needs_git
def test_check_fails_loudly_when_two_bundles_are_uncommitted(tmp_path):
    """Operator tie-break ruling: two uncommitted candidates is AMBIGUOUS -> FAIL, never a
    silent pick. A silent pick between two uncommitted bundles is the same 'green about the
    wrong file' class this selector exists to kill."""
    _init_bundle(tmp_path, [_PASS_SYMBOL], slug="2026-07-20-a")
    repo = tmp_path / "repo"
    run = _git_repo(repo)
    # Seed HEAD without committing any bundle: the unborn-HEAD guard would otherwise
    # fall back to lexical and this case would never be reached.
    _commit_at(run, "VISION.md", "2026-07-20T09:00:00+02:00", "seed HEAD only")

    second = repo / "docs" / "handoffs" / "2026-07-20-b"
    second.mkdir(parents=True)
    (second / "PROBES.md").write_text(_probes_md([_PASS_SYMBOL]), encoding="utf-8")

    findings = aud.check_handoff_probes(repo)
    assert len(findings) == 1
    assert findings[0].status == "fail"
    assert "ambiguous" in findings[0].evidence.lower()
    assert "2026-07-20-a" in findings[0].evidence
    assert "2026-07-20-b" in findings[0].evidence
    assert "|" not in findings[0].evidence


@_needs_git
def test_check_selects_correctly_under_inherited_git_dir(tmp_path, monkeypatch):
    """[#372 + #355] The selector is vulnerable to the very defect #355 fixed. Under
    pre-commit, GIT_DIR is exported for the WHOLE hook run. If the guard's
    `rev-parse --show-toplevel` does not go through the scrubbed env, it resolves to the
    FOREIGN repo's toplevel, the normcase-vs-repo_path guard fails, and selection silently
    degrades to the no-git lexical fallback -- re-picking arc5. Green in every clean-env
    test above, broken in the only environment that actually matters.

    Every git call inside _select_active_bundle (BOTH guard rev-parse calls and the
    log --diff-filter=A) must be scrubbed; any one of them bypassing it re-opens this.
    """
    repo = _arc5_shaped(tmp_path)                        # built BEFORE the monkeypatch
    foreign = tmp_path / "foreign"
    _git_repo(foreign)
    (foreign / "seed.md").write_text("s\n", encoding="utf-8")
    _commit_at(_git_repo(foreign), ".", "2026-07-01T00:00:00+02:00", "foreign seed")

    monkeypatch.setenv("GIT_DIR", str(foreign / ".git"))
    monkeypatch.setenv("GIT_INDEX_FILE", str(foreign / ".git" / "index"))

    findings = aud.check_handoff_probes(repo)
    assert findings[0].status == "pass"
    assert "2026-07-20-x" in findings[0].evidence
    assert "arc5" not in findings[0].evidence


@_needs_git
def test_every_selector_git_call_receives_the_scrubbed_env(tmp_path, monkeypatch):
    """Codex review [HIGH]: asserting only the final SELECTION lets a regression slip
    through -- e.g. `rev-parse --verify HEAD` bypassing the scrubbed runner while the other
    two calls stay scrubbed would still produce the right answer here, yet violate the
    stated "every git call is scrubbed" invariant. So instrument the runner and assert the
    env of EACH invocation, not just the outcome."""
    repo = _arc5_shaped(tmp_path)
    monkeypatch.setenv("GIT_DIR", str(tmp_path / "nowhere" / ".git"))
    monkeypatch.setenv("GIT_INDEX_FILE", str(tmp_path / "nowhere" / "index"))
    monkeypatch.setenv("GIT_CONFIG_PARAMETERS", "'core.bare=true'")
    # Deliberate non-scrubs: these MUST survive into every call.
    monkeypatch.setenv("GIT_AUTHOR_NAME", "Keep Me")
    monkeypatch.setenv("GIT_SSH_COMMAND", "ssh -o Keep=1")

    seen: list[tuple[list[str], dict]] = []
    real = aud.subprocess.run

    def spy(cmd, *a, **kw):
        if isinstance(cmd, (list, tuple)) and cmd and cmd[0] == "git":
            seen.append((list(cmd), dict(kw.get("env") or {})))
        return real(cmd, *a, **kw)

    monkeypatch.setattr(aud.subprocess, "run", spy)
    aud.check_handoff_probes(repo)

    selector_calls = [(c, e) for c, e in seen if "-C" in c]
    assert len(selector_calls) >= 3, f"expected the guard + log calls, saw {selector_calls}"
    for cmd, env in selector_calls:
        assert env, f"no explicit env passed to {cmd} — it would inherit os.environ"
        for leaked in ("GIT_DIR", "GIT_INDEX_FILE", "GIT_CONFIG_PARAMETERS"):
            assert leaked not in env, f"{leaked} leaked into {cmd}"
        assert env.get("GIT_AUTHOR_NAME") == "Keep Me", f"identity stripped from {cmd}"
        assert env.get("GIT_SSH_COMMAND") == "ssh -o Keep=1", f"transport stripped from {cmd}"


@_needs_git
def test_check_refuses_rather_than_guessing_on_an_unborn_head(tmp_path):
    """Codex review [HIGH]: an unborn HEAD used to collapse into the lexical fallback,
    so a fresh repo holding two uncommitted bundles silently got the lexically-max one --
    bypassing the ambiguity refusal in exactly the situation it exists for."""
    _init_bundle(tmp_path, [_PASS_SYMBOL], slug="2026-07-20-a")
    repo = tmp_path / "repo"
    _git_repo(repo)                      # real repo, nothing committed at all
    second = repo / "docs" / "handoffs" / "2026-07-20-b"
    second.mkdir(parents=True)
    (second / "PROBES.md").write_text(_probes_md([_PASS_SYMBOL]), encoding="utf-8")

    findings = aud.check_handoff_probes(repo)
    assert findings[0].status == "fail"
    assert "ambiguous" in findings[0].evidence.lower()
    assert "2026-07-20-a" in findings[0].evidence
    assert "2026-07-20-b" in findings[0].evidence


@_needs_git
def test_check_degrades_loudly_when_repo_is_nested_in_another_repo(tmp_path):
    """Codex review [HIGH]: a git-toplevel mismatch used to fall back to lexical silently,
    which is precisely how the stale-bundle false green would return under a
    misconfiguration. It must surface as a WARN instead."""
    outer = tmp_path / "outer"
    _git_repo(outer)
    (outer / "seed.md").write_text("s\n", encoding="utf-8")
    _commit_at(_git_repo(outer), ".", "2026-07-01T00:00:00+02:00", "outer seed")

    # A bundle-bearing dir NESTED inside `outer`, with no repo of its own.
    inner = outer / "nested"
    for slug, rows in (("2026-07-20-a", [_PASS_SYMBOL]), ("2026-07-20-b", [_PASS_SYMBOL])):
        d = inner / "docs" / "handoffs" / slug
        d.mkdir(parents=True)
        (d / "PROBES.md").write_text(_probes_md(rows), encoding="utf-8")

    findings = aud.check_handoff_probes(inner)
    assert findings[0].status == "warn"
    assert "degraded" in findings[0].evidence.lower()
    assert "|" not in findings[0].evidence


# --- R6 CLI mapping ([#446]) ------------------------------------------------------
# The two load-bearing cases (the hard error, and both flags accepted) are pinned by the
# frozen contract. These cover the surrounding contract: main() RETURNS codes and never
# escapes as SystemExit, and the pre-R6 invocations keep working byte-for-byte.

def _empty_bundle(tmp_path):
    """A bundle whose PROBES.md carries no rows — the no-op fixture the ARGUMENT-PARSING tests
    below use, so that what they measure is argparse and nothing else.

    The directory name is PRE-ERA on purpose ([#643], 2026-09-08). A zero-row `PROBES.md` is
    now a FAIL for an in-era bundle (`_unreadable_manifest`; AMEND-643-001 §2), and
    `bundle_at_or_after` treats an UNPARSEABLE name as in-era, fail-closed — so the previous
    bare `b` would make every caller here return 1 and turn tests about flag spelling into
    tests about the new verdict. A pre-era name keeps `verify()` returning [] exactly as it
    did, which is the no-op these tests were written against."""
    bundle = tmp_path / "2026-06-12-b"
    bundle.mkdir()
    (bundle / "PROBES.md").write_text("no rows here\n", encoding="utf-8")
    return bundle


def test_main_never_raises_systemexit_on_a_usage_error(tmp_path):
    """argparse's default is to EXIT on a usage error. main() catches that and returns the
    code instead, so the callable stays testable and a usage mistake can never kill a caller
    mid-run. Every one of these is a RETURN, not a raise."""
    assert vhp.main([]) == 2                                    # missing positional
    assert vhp.main(["--cross-repo"]) == 2                      # missing positional + no root
    assert vhp.main([str(_empty_bundle(tmp_path)), "--nonsuch"]) == 2   # unknown option
    assert vhp.main([str(tmp_path / "b"), "--repo-root"]) == 2   # flag missing its value


def test_main_default_invocation_is_unchanged(tmp_path):
    """The pre-R6 call shape — bundle dir alone — resolves against the bundle's own repo and
    returns 0. R6 codifies the existing semantics; it must not change this path."""
    assert vhp.main([str(_empty_bundle(tmp_path))]) == 0


def test_main_repo_root_accepts_the_equals_form(tmp_path):
    """`--repo-root=PATH` and `--repo-root PATH` are the same flag (argparse gives this for
    free — pinned so a hand-rolled reparse can't silently drop it)."""
    bundle = _empty_bundle(tmp_path)
    assert vhp.main([str(bundle), f"--repo-root={tmp_path}"]) == 0
    assert vhp.main([str(bundle), "--repo-root", str(tmp_path)]) == 0


def test_main_cross_repo_without_repo_root_names_the_reason(tmp_path, capsys):
    """R6's hard error must SAY why — a silent inference is the original false-FAIL class."""
    assert vhp.main([str(_empty_bundle(tmp_path)), "--cross-repo"]) == 2
    err = capsys.readouterr().err
    assert "--repo-root" in err and "infer" in err.lower()


# --- suffix-family resolution ([#473] half A) --------------------------------
#
# A multi-handoff day produces `<slug>`, `<slug>-2`, `<slug>-3` siblings — NORMAL operation,
# not an error. The operator names the BASE slug from muscle memory; the gate must reach the
# ACTIVE member anyway. Before this arc the base slug verified the STALE sibling and reported
# a confident verdict about the wrong bundle ("green about the wrong file", the #372 class,
# recurring here through a different door).


def _suffix_family_repo(tmp_path):
    """`2026-08-01-x` (added FIRST, carries a FAILING probe) + `2026-08-01-x-2` (added
    SECOND, carries a PASSING probe). Verdict alone therefore names which was verified."""
    _init_bundle(tmp_path, [_FAIL_MISSING], slug="2026-08-01-x")
    repo = tmp_path / "repo"
    sib = repo / "docs" / "handoffs" / "2026-08-01-x-2"
    sib.mkdir(parents=True)
    (sib / "PROBES.md").write_text(_probes_md([_PASS_SYMBOL]), encoding="utf-8")
    run = _git_repo(repo)
    _commit_at(run, "docs/handoffs/2026-08-01-x", "2026-07-31T17:54:31+02:00", "base")
    _commit_at(run, ".", "2026-08-01T21:20:17+02:00", "the -2 sibling + repo files")
    return repo


@_needs_git
def test_requesting_the_base_slug_resolves_to_the_active_suffixed_sibling(tmp_path):
    """THE ACCEPTANCE TEST. The operator's verbatim prompt names the BASE slug; the gate runs
    against `-2` and returns ITS verdict, with zero failures attributable to the resolution."""
    repo = _suffix_family_repo(tmp_path)
    requested = repo / "docs" / "handoffs" / "2026-08-01-x"

    active, note = vhp.resolve_active_bundle(requested)

    assert active.name == "2026-08-01-x-2", f"resolved to {active.name}, not the active sibling"
    assert note and "active-bundle rule" in note
    results = vhp.verify(active)
    assert [r.status for r in results] == ["pass"], "the -2 bundle's own PASSING probe must run"


@_needs_git
def test_main_on_the_base_slug_prints_one_resolution_line_and_gates_on_the_active(tmp_path, capsys):
    """End-to-end through the CLI the /handoff-verify command path uses: exactly ONE
    informational line, in the specified shape, and the exit code is the ACTIVE bundle's."""
    repo = _suffix_family_repo(tmp_path)
    rc = vhp.main([str(repo / "docs" / "handoffs" / "2026-08-01-x")])
    out = capsys.readouterr().out

    assert rc == 0, "the active (-2) bundle passes; the stale base would have returned 1"
    line = [ln for ln in out.splitlines() if "active-bundle rule" in ln]
    assert len(line) == 1, f"expected exactly one resolution line, got {line}"
    assert line[0].strip() == (
        "resolved '2026-08-01-x' -> '2026-08-01-x-2' (active-bundle rule)")


@_needs_git
def test_exact_flag_verifies_the_requested_bundle_and_reports_supersession(tmp_path, capsys):
    """`--exact` is deliberate archaeology on a superseded bundle: no resolution, and the
    supersession is REPORTED (silence would read as 'this is the active one')."""
    repo = _suffix_family_repo(tmp_path)
    rc = vhp.main([str(repo / "docs" / "handoffs" / "2026-08-01-x"), "--exact"])
    out = capsys.readouterr().out

    assert rc == 1, "the requested (stale) bundle carries the FAILING probe"
    assert "active-bundle rule" not in out, "--exact must not resolve"
    assert "superseded" in out.lower() and "2026-08-01-x-2" in out


@_needs_git
def test_requesting_the_active_sibling_directly_is_a_no_op(tmp_path, capsys):
    """Naming `-2` explicitly already IS the active bundle — no resolution line, no churn."""
    repo = _suffix_family_repo(tmp_path)
    assert vhp.main([str(repo / "docs" / "handoffs" / "2026-08-01-x-2")]) == 0
    assert "active-bundle rule" not in capsys.readouterr().out


def test_single_member_family_needs_no_git_and_is_unchanged(tmp_path):
    """A lone bundle (the overwhelmingly common case) resolves to itself without a git call."""
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL], slug="2026-06-12-b")
    active, note = vhp.resolve_active_bundle(bundle)
    assert active == bundle and note is None


def test_suffix_family_groups_base_and_numeric_siblings_only(tmp_path):
    """The family is `<base>` + `<base>-<n>`. A DIFFERENT slug that merely shares a prefix
    (`-arc5`, a longer date-slug) is NOT a family member — over-grouping would resolve an
    unrelated bundle, which is the same wrong-file failure wearing the opposite sign."""
    _init_bundle(tmp_path, [_PASS_SYMBOL], slug="2026-08-01-x")
    root = tmp_path / "repo" / "docs" / "handoffs"
    for name in ("2026-08-01-x-2", "2026-08-01-x-10", "2026-08-01-x-arc5", "2026-08-01-y"):
        (root / name).mkdir(parents=True)
    fam = {d.name for d in vhp.sibling_family(root / "2026-08-01-x")}
    assert fam == {"2026-08-01-x", "2026-08-01-x-2", "2026-08-01-x-10"}


# --- locator identity ([#473] half B') ---------------------------------------
#
# Already-SEALED bundles carry the generator defect and are immutable, so the verifier has to
# absorb it: when verifying bundle X, a `docs/handoffs/<other>/…` locator is interpreted
# relative to X's OWN directory. The -2 verify run proved the blast radius — 7 self-references
# to the un-suffixed sibling — and passed only because both bundles coincidentally shared the
# checked values. Binding is not identity.

_SELF_LOCATOR = ("P0c", "does this bundle's Purpose name a live authority",
                 "this bundle's `docs/handoffs/2026-08-01-x/HANDOFF_BOOT.md` `## Destination`",
                 "the Purpose is hand-authored per bundle",
                 "`sed -n 'p' docs/handoffs/2026-08-01-x/HANDOFF_BOOT.md`")


def _mislabelled_bundle(tmp_path):
    """`-2` whose PROBES.md self-references the UN-SUFFIXED sibling — the sealed live defect.

    Both bundles carry a HANDOFF_BOOT.md, exactly as the real pair does, and THAT is why a
    status check alone cannot discriminate: the sibling's file exists, so the mis-pointed
    locator binds — to the wrong bundle — and still reports `pass`. Resolving is not
    resolving-to-the-right-thing, which is the whole "binding is not identity" point.

    So the fixture keys on CONTENT: the `## Destination` anchor exists ONLY in the `-2` copy.
    No rebase -> the row resolves the base copy and the anchor is missing (anchor-missing);
    rebase -> it resolves `-2` and the anchor is found (pass). The verdict now names which
    file was actually read."""
    repo = tmp_path / "repo"
    for rel, content in _FILES.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    base = repo / "docs" / "handoffs" / "2026-08-01-x"
    base.mkdir(parents=True)
    (base / "HANDOFF_BOOT.md").write_text(
        "| **Slug** | `2026-08-01-x` |\n\n## Purpose\nthe SIBLING's boot header\n",
        encoding="utf-8")
    sib = repo / "docs" / "handoffs" / "2026-08-01-x-2"
    sib.mkdir(parents=True)
    (sib / "PROBES.md").write_text(_probes_md([_SELF_LOCATOR]), encoding="utf-8")
    (sib / "HANDOFF_BOOT.md").write_text(
        "| **Slug** | `2026-08-01-x` |\n\n## Destination\nbranch `main`\n", encoding="utf-8")
    return sib


def test_bundle_internal_locator_is_rebased_onto_the_verified_bundle(tmp_path):
    """The locator names the sibling, whose HANDOFF_BOOT.md lacks the anchor. Without the
    rebase the row reads the WRONG file and degrades to anchor-missing; with it, the row
    reads the bundle actually under verification and binds."""
    results = vhp.verify(_mislabelled_bundle(tmp_path))
    assert [r.status for r in results] == ["pass"], [r.detail for r in results]


def test_rebased_locator_reports_the_identity_defect(tmp_path):
    """The rebase makes verification CORRECT; the report makes the defect VISIBLE. Silently
    rebasing would hide a real generator bug behind a clean green."""
    results = vhp.verify(_mislabelled_bundle(tmp_path))
    assert results[0].locator_rebased, "identity mismatch must be recorded on the result"
    assert "2026-08-01-x" in results[0].locator_rebased


def test_main_surfaces_the_locator_identity_defect(tmp_path, capsys):
    """The operator-facing CLI says it out loud, and it stays ADVISORY (exit 0)."""
    assert vhp.main([str(_mislabelled_bundle(tmp_path)), "--exact"]) == 0
    out = capsys.readouterr().out.lower()
    assert "identity" in out and "2026-08-01-x" in out


def test_locator_naming_the_verified_bundle_is_never_flagged(tmp_path):
    """Negative control: a correctly-self-referencing bundle produces no identity note."""
    repo = tmp_path / "repo"
    for rel, content in _FILES.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    b = repo / "docs" / "handoffs" / "2026-08-01-x"
    b.mkdir(parents=True)
    (b / "PROBES.md").write_text(_probes_md([_SELF_LOCATOR]), encoding="utf-8")
    (b / "HANDOFF_BOOT.md").write_text(
        "| **Slug** | `2026-08-01-x` |\n\n## Destination\nbranch `main`\n", encoding="utf-8")
    results = vhp.verify(b)
    assert [r.status for r in results] == ["pass"]
    assert not results[0].locator_rebased


# --- §5 cond. 4: the bounded-deterministic rung (R3, census 2026-08-26) -----
#
# HANDOFF_PROCESS §5 condition 4 (ratified at intake #18) rejects a probe "whose honest
# answer requires unbounded judgment over an open set" and names P10 as its origin. P10
# then shipped in 35 bundles anyway, surviving the v6 cut that ratified the condition
# rejecting it. These fixtures are P10's own two quantifiers, in shape.

# The exact P10 disease: a question cell quantifying over EVERY OPEN item of a live,
# arbitrarily-large set. Otherwise a well-formed, live-grounded probe -> the rung must FAIL
# it regardless (it is an arc, not a probe).
_UNBOUNDED_QUESTION = ("P10", "for **every OPEN item** in the backlog, is each still live",
                       "`VISION.md` in live git", "an at-boot judgment over the open set",
                       "`python scripts/audit.py checks`")
# P10's second quantifier — "the successor grooms the whole open set at boot".
_UNBOUNDED_WHOLE_SET = ("P11", "the successor grooms the **whole open set** at boot",
                        "`VISION.md` in live git", "a stale snapshot cannot answer it",
                        "`python scripts/audit.py checks`")
# The Why cell carries it instead — the rung is column-blind, like the answer-hint rung.
_UNBOUNDED_WHY = ("P12", "which ids are drifted", "`VISION.md` in live git",
                  "each open item must be classified live / dead / awaiting-ruling",
                  "`python scripts/audit.py checks`")
# A bundle cut ON the era date (the day P10 left the shipped manifest) and one cut before it.
_ERA_SLUG = "2026-08-26-b"
_PRE_ERA_SLUG = "2026-08-25-b"


def test_verify_fail_on_unbounded_open_set_question(tmp_path):
    # §5 cond. 4: unbounded judgment over an open set is an arc, not a probe -> FAIL.
    by = _by_id(vhp.verify(_init_bundle(tmp_path, [_UNBOUNDED_QUESTION], slug=_ERA_SLUG)))
    assert by["P10"].status == "fail"
    assert "unbounded" in by["P10"].detail.lower()


def test_verify_fail_on_whole_open_set_form(tmp_path):
    # The second P10 quantifier ("the whole open set") must FAIL on its own.
    by = _by_id(vhp.verify(_init_bundle(tmp_path, [_UNBOUNDED_WHOLE_SET], slug=_ERA_SLUG)))
    assert by["P11"].status == "fail"
    assert "unbounded" in by["P11"].detail.lower()


def test_verify_fail_on_unbounded_in_why_cell(tmp_path):
    # Column-blind, exactly like the answer-hint rung: the Why cell is scanned too.
    by = _by_id(vhp.verify(_init_bundle(tmp_path, [_UNBOUNDED_WHY], slug=_ERA_SLUG)))
    assert by["P12"].status == "fail"
    assert "unbounded" in by["P12"].detail.lower()


def test_bounded_row_naming_backlog_still_passes(tmp_path):
    # Negative control, and the one that matters: P4/P9 ask BACKLOG questions whose answer
    # is whatever a validator prints — bounded and mechanical. The rung must not fire.
    bounded = ("P4", "which backlog ids does the drift check flag right now",
               "`VISION.md` in live git", "the drifted set is computed at answer-time",
               "`python scripts/audit.py checks`")
    by = _by_id(vhp.verify(_init_bundle(tmp_path, [bounded], slug=_ERA_SLUG)))
    assert by["P4"].status == "pass"


def test_boundedness_rung_ignores_open_set_prose_in_preamble(tmp_path):
    # ROW-scoped: a preamble that DESCRIBES the condition — as this template's own contract
    # prose now does — is never a table row and is never classified.
    preamble = ("# Probe manifest\n<!-- scope: meta -->\n\n"
                "> §5 cond. 4: a probe asking a seat to groom every open item — the whole "
                "open set — is an arc, not a probe, and is rejected here.\n\n## Teeth\n\n")
    md = _probes_md([_PASS_SYMBOL], preamble=preamble)
    by = _by_id(vhp.verify(_init_bundle(tmp_path, [_PASS_SYMBOL],
                                        slug=_ERA_SLUG, probes_md=md)))
    assert by["P2"].status == "pass"


def test_pre_era_bundle_is_judged_by_its_own_era(tmp_path):
    # THE era clause, and the reason it is a date and not merely row-scoping: the 35
    # P10-bearing bundles are immutable committed artifacts, and the newest of them is what
    # check_handoff_probes reads on every commit. A rung that REDs an unfixable artifact is
    # condemning the past for the present's rule.
    by = _by_id(vhp.verify(_init_bundle(tmp_path, [_UNBOUNDED_QUESTION], slug=_PRE_ERA_SLUG)))
    assert by["P10"].status == "pass"


def test_era_boundary_parses_the_date_rather_than_comparing_the_whole_name():
    """A bare string compare against the DIR NAME looks equivalent to a date compare and is not
    — `2026-08-9-x` compares GREATER than `2026-08-26` on its 9th character, so a pre-era bundle
    would be judged by a later era's rule, and `2026-08-2` would be waved through. Both
    directions pinned; found by terra on this lane's own diff."""
    era = "2026-08-26"
    assert vhp.bundle_at_or_after("2026-08-26-x", era) is True      # ON the boundary
    assert vhp.bundle_at_or_after("2026-09-01-x", era) is True
    assert vhp.bundle_at_or_after("2026-08-25-x", era) is False
    # malformed, both signs — neither may be ordered by raw string comparison
    assert vhp.bundle_at_or_after("2026-08-9-x", era) is True       # not a strict ISO prefix
    assert vhp.bundle_at_or_after("2026-08-2", era) is True         # short: not a date at all
    assert vhp.bundle_at_or_after("scratch", era) is True           # fail-closed
    # right SHAPE, not a real calendar day — it would otherwise compare as pre-era and exempt a
    # malformed CURRENT bundle, which inverts the fail-closed rule (terra pass 5)
    assert vhp.bundle_at_or_after("2026-02-31-manual", era) is True
    assert vhp.bundle_at_or_after("2026-13-01-manual", era) is True


def test_undated_bundle_dir_is_judged_by_the_current_rule(tmp_path):
    # Fail-CLOSED on an unparseable name: a non-dated directory is not a historical bundle,
    # so it does not inherit an exemption by being unreadable.
    by = _by_id(vhp.verify(_init_bundle(tmp_path, [_UNBOUNDED_QUESTION], slug="scratch-bundle")))
    assert by["P10"].status == "fail"


def test_check_fail_class_gates_on_unbounded_probe(tmp_path):
    # The rung reaches the DEPLOYED gate with no audit.py edit: 'fail' -> the adapter maps it
    # to a FAIL-class Finding that blocks audit-health + ship (same path as answer-hint).
    repo = _repo_with_bundle(tmp_path, [_UNBOUNDED_QUESTION], slug=_ERA_SLUG)
    findings = aud.check_handoff_probes(repo)
    assert findings[0].status == "fail"
    assert "unbounded" in findings[0].evidence.lower()
    assert "|" not in findings[0].evidence


def test_live_probe_template_carries_no_unbounded_row():
    # The template IS the shipped manifest, so P10's removal is asserted against the live
    # file: a re-introduction fails the suite rather than 35 more bundles.
    tmpl_path = (Path(__file__).resolve().parents[1]
                 / "templates" / "handoff" / "v5" / "PROBES.md.tmpl")
    rows = vhp.parse_probes(tmpl_path.read_text(encoding="utf-8"))
    assert rows, "the template must still parse as a probe manifest"
    offenders = [r["id"] for r in rows
                 if any(vhp._UNBOUNDED_SCOPE_RE.search(r[c]) for c in vhp._LOAD_BEARING)]
    assert offenders == [], f"unbounded probe row(s) in the shipped template: {offenders}"


# ---------------------------------------------------------------------------
# [batch R5P, lane-r-000] ONE `git log` for ALL bundles, not one per directory.
#
# _select_active_bundle spawned one `git log --diff-filter=A` PER candidate: 87 spawns
# / 26.3 s on the live tree, ~32% of `audit.py health`'s 82.8 s. Batching that into a
# single `--name-only` walk is only safe if selection is provably UNCHANGED, so the
# oracle below is a FROZEN copy of the per-directory method and every test in this
# section asserts the production selector agrees with it.
#
# NO `@_needs_git` IN THIS SECTION, deliberately. `scripts/proof_layer.py` ratchets the
# population of environment-conditional guards against a committed baseline, and its
# whole point applies here: a proof that can be SKIPPED on the machine where git is the
# thing under test is not a mechanism. Without git these tests error loudly instead of
# reporting a green they did not earn. Do not "restore" the decorator for symmetry with
# the older tests above.
# ---------------------------------------------------------------------------


def _perdir_select(repo_path, candidates):
    """FROZEN per-directory oracle: one `git log` per candidate, the pre-batching method.

    Deliberately a COPY, not an import. An oracle that imports the implementation it is
    meant to check agrees with it by construction and proves nothing; this copy keeps a
    second, independent statement of the same rule so a batching regression has something
    to disagree with. Detail STRINGS are intentionally not reproduced verbatim (the
    batched form names a chunk, not a directory) - the contract is (bundle, kind).
    """
    lexical = max(candidates, key=lambda d: d.name)
    if len(candidates) == 1:
        return candidates[0], "sole", candidates[0].name

    scrub = aud._git_location_env()
    env = {k: v for k, v in os.environ.items() if k not in scrub}

    def _run(args):
        try:
            p = subprocess.run(["git", "-C", str(repo_path), *args], capture_output=True,
                               text=True, encoding="utf-8", errors="replace", env=env)
        except OSError:
            return None
        return p.stdout if p.returncode == 0 else None

    top = _run(["rev-parse", "--show-toplevel"])
    if not top or not top.strip():
        return lexical, "no-git", lexical.name
    try:
        same = (os.path.normcase(str(Path(top.strip()).resolve()))
                == os.path.normcase(str(Path(repo_path).resolve())))
    except OSError:
        same = False
    if not same:
        return None, "degraded", f"git toplevel {top.strip()} is not {repo_path}"
    if _run(["rev-parse", "--verify", "HEAD"]) is None:
        return None, "ambiguous", ", ".join(sorted(d.name for d in candidates))

    fresh, dated = [], []
    for d in candidates:
        out = _run(["log", "--diff-filter=A", "--reverse", "--format=%at",
                    "--", f"docs/handoffs/{d.name}"])
        if out is None:
            return None, "degraded", f"git log failed for {d.name}"
        lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
        if not lines:
            fresh.append(d)
            continue
        try:
            dated.append((int(lines[0]), d.name, d))
        except ValueError:
            return None, "degraded", f"unparseable add-date for {d.name}"

    if len(fresh) > 1:
        return None, "ambiguous", ", ".join(sorted(d.name for d in fresh))
    if len(fresh) == 1:
        return fresh[0], "fresh", fresh[0].name
    if not dated:
        return lexical, "no-git", lexical.name
    dated.sort(key=lambda t: (t[0], t[1]))
    return dated[-1][2], "add-date", dated[-1][1]


def _spy_git(monkeypatch):
    """Record every `git` argv audit.py spawns. Returns the (mutating) list."""
    seen = []
    real = aud.subprocess.run

    def spy(cmd, *a, **kw):
        if isinstance(cmd, (list, tuple)) and cmd and cmd[0] == "git":
            seen.append(list(cmd))
        return real(cmd, *a, **kw)

    monkeypatch.setattr(aud.subprocess, "run", spy)
    return seen


def _log_calls(seen):
    return [c for c in seen if "log" in c]


def _make_bundle(repo, slug):
    b = repo / "docs" / "handoffs" / slug
    b.mkdir(parents=True, exist_ok=True)
    (b / "PROBES.md").write_text(_probes_md([_PASS_SYMBOL]), encoding="utf-8")
    return b


def _seed_bundles(tmp_path, tracked, *, untracked=(), staged=(), name="repo"):
    """Repo with one bundle per `tracked` (slug, iso-date), committed AT that date.

    `untracked` bundles exist on disk only; `staged` bundles are `git add`ed but never
    committed - both are "fresh" to the selector, and the distinction is exactly what
    the fresh/ambiguous pins below exercise.
    """
    repo = tmp_path / name
    (repo / "docs" / "handoffs").mkdir(parents=True)
    (repo / "VISION.md").write_text("# V\n", encoding="utf-8")
    run = _git_repo(repo)
    _commit_at(run, "VISION.md", "2026-01-01T00:00:00+00:00", "seed HEAD")
    for slug, when in tracked:
        _make_bundle(repo, slug)
        _commit_at(run, f"docs/handoffs/{slug}", when, slug)
    for slug in untracked:
        _make_bundle(repo, slug)
    for slug in staged:
        _make_bundle(repo, slug)
        run(["add", "--", f"docs/handoffs/{slug}"])
    return repo


def _candidates(repo):
    handoffs = repo / "docs" / "handoffs"
    return sorted((d for d in handoffs.iterdir() if d.is_dir()), key=lambda d: d.name)


def _dated(n, *, start_day=1):
    """`n` tracked bundles whose add-date order is the REVERSE of their slug order, so a
    lexical fallback and an add-date selection can never accidentally agree."""
    return [(f"2026-07-{start_day + i:02d}-slug-{n - i:02d}",
             f"2026-07-{start_day + i:02d}T09:00:00+00:00") for i in range(n)]


# --- done-contract 1: ONE invocation, proven by spawn count ----------------


def test_selector_issues_one_git_log_regardless_of_candidate_count(tmp_path, monkeypatch):
    """The lane's whole point. 12 candidates must cost ONE `git log`, not 12 - asserted on
    the observed spawn argv list, never on a claim in a docstring."""
    repo = _seed_bundles(tmp_path, _dated(12))
    cands = _candidates(repo)
    assert len(cands) == 12, "fixture premise: 12 candidates"

    seen = _spy_git(monkeypatch)
    bundle, kind, _ = aud._select_active_bundle(repo, cands)

    assert kind == "add-date"
    assert bundle is not None and bundle.name == "2026-07-12-slug-01"
    logs = _log_calls(seen)
    assert len(logs) == 1, f"expected ONE git log for 12 candidates, saw {len(logs)}: {logs}"


def test_git_log_count_does_not_grow_with_candidate_count(tmp_path, monkeypatch):
    """O(1), not merely 'fewer': 4 candidates and 16 candidates cost the SAME number of
    invocations. A per-directory implementation passes neither arm."""
    counts = []
    for n in (4, 16):
        repo = _seed_bundles(tmp_path, _dated(n), name=f"repo{n}")
        seen = _spy_git(monkeypatch)
        aud._select_active_bundle(repo, _candidates(repo))
        counts.append(len(_log_calls(seen)))
    assert counts[0] == counts[1] == 1, f"invocation count scaled with candidates: {counts}"


# --- done-contract 2: both methods agree, on seeded shapes AND the live tree ---


def _shape_add_date(tmp_path):
    return _seed_bundles(tmp_path, _dated(6))


def _shape_fresh_untracked(tmp_path):
    return _seed_bundles(tmp_path, _dated(5), untracked=["2026-06-01-aaa-live"])


def _shape_fresh_staged(tmp_path):
    return _seed_bundles(tmp_path, _dated(5), staged=["2026-06-01-aaa-staged"])


def _shape_ambiguous(tmp_path):
    return _seed_bundles(tmp_path, _dated(5),
                         untracked=["2026-06-01-aaa-live", "2026-06-02-bbb-live"])


def _shape_ambiguous_mixed(tmp_path):
    return _seed_bundles(tmp_path, _dated(4), untracked=["2026-06-01-aaa-live"],
                         staged=["2026-06-02-bbb-staged"])


def _shape_sole(tmp_path):
    return _seed_bundles(tmp_path, _dated(1))


def _shape_unborn_head(tmp_path):
    repo = tmp_path / "repo"
    (repo / "docs" / "handoffs").mkdir(parents=True)
    _git_repo(repo)
    _make_bundle(repo, "2026-07-01-a")
    _make_bundle(repo, "2026-07-02-b")
    return repo


def _shape_no_git(tmp_path):
    repo = tmp_path / "repo"
    (repo / "docs" / "handoffs").mkdir(parents=True)
    _make_bundle(repo, "2026-07-01-a")
    _make_bundle(repo, "2026-07-02-b")
    return repo


def _shape_nested_repo(tmp_path):
    """repo_path sits INSIDE a different repo - add-dates would be read from the wrong
    history, so both methods must degrade rather than answer."""
    outer = tmp_path / "outer"
    outer.mkdir(parents=True)
    run = _git_repo(outer)
    (outer / "seed.md").write_text("s\n", encoding="utf-8")
    _commit_at(run, "seed.md", "2026-01-01T00:00:00+00:00", "outer seed")
    inner = outer / "inner"
    (inner / "docs" / "handoffs").mkdir(parents=True)
    _make_bundle(inner, "2026-07-01-a")
    _make_bundle(inner, "2026-07-02-b")
    return inner


def _shape_prefix_siblings(tmp_path):
    """The #372 shape, sharpened for BATCHING: '<slug>-arc5' files live under a path that
    STARTS WITH '<slug>'. A batched matcher that attributes by bare string prefix instead
    of a path-segment boundary silently credits arc5's add-commit to '<slug>' - which
    would turn the untracked '<slug>' from `fresh` into `add-date`."""
    repo = _seed_bundles(tmp_path, [("2026-07-20-x-arc5", "2026-07-19T14:42:52+00:00"),
                                    ("2026-07-18-other", "2026-07-18T09:00:00+00:00")],
                         untracked=["2026-07-20-x"])
    assert max("2026-07-20-x-arc5", "2026-07-20-x") == "2026-07-20-x-arc5"
    return repo


_SHAPES = {
    "add-date": (_shape_add_date, "add-date"),
    "fresh-untracked": (_shape_fresh_untracked, "fresh"),
    "fresh-staged": (_shape_fresh_staged, "fresh"),
    "ambiguous-two-untracked": (_shape_ambiguous, "ambiguous"),
    "ambiguous-untracked-plus-staged": (_shape_ambiguous_mixed, "ambiguous"),
    "sole": (_shape_sole, "sole"),
    "unborn-head": (_shape_unborn_head, "ambiguous"),
    "no-git": (_shape_no_git, "no-git"),
    "nested-repo": (_shape_nested_repo, "degraded"),
    "prefix-siblings": (_shape_prefix_siblings, "fresh"),
}


@pytest.mark.parametrize("shape", sorted(_SHAPES))
def test_batched_and_per_directory_selection_agree(tmp_path, shape):
    """Done-contract 2, seeded arm: for EVERY kind the selector can return, the batched
    production selector and the frozen per-directory oracle return the same bundle and
    the same kind. `expected_kind` is pinned separately so a shape that silently stops
    exercising its kind (both methods agreeing on the WRONG thing) still fails."""
    build, expected_kind = _SHAPES[shape]
    repo = build(tmp_path)
    cands = _candidates(repo)

    got_bundle, got_kind, _ = aud._select_active_bundle(repo, cands)
    ref_bundle, ref_kind, _ = _perdir_select(repo, cands)

    assert got_kind == ref_kind, f"{shape}: kind {got_kind!r} != per-dir {ref_kind!r}"
    assert got_kind == expected_kind, f"{shape}: no longer exercises {expected_kind!r}"
    assert (got_bundle.name if got_bundle else None) == (
        ref_bundle.name if ref_bundle else None), f"{shape}: bundle disagrees"


@pytest.mark.live_repo
@pytest.mark.slow
def test_batched_and_per_directory_selection_agree_on_the_live_tree():
    """Done-contract 2, LIVE arm. The seeded shapes are synthetic linear histories; the
    live tree has merges, renames and ~87 bundles, which is where a batched pathspec walk
    can diverge from 87 single-pathspec walks (history simplification is computed over
    the UNION of the pathspecs, not over each one alone). Slow by construction: the
    oracle arm IS the 87-spawn cost this lane removed."""
    repo = Path(aud.__file__).resolve().parents[1]
    handoffs = repo / "docs" / "handoffs"
    if not (repo / ".git").exists() or not handoffs.is_dir():
        pytest.skip("not a live checkout with docs/handoffs/")
    cands = sorted((d for d in handoffs.iterdir()
                    if d.is_dir() and d.name not in aud._BUNDLE_EXCLUDE_DIRS
                    and (d / "PROBES.md").exists()), key=lambda d: d.name)
    if len(cands) < 2:
        pytest.skip("fewer than 2 live bundles - nothing to compare")

    got_bundle, got_kind, _ = aud._select_active_bundle(repo, cands)
    ref_bundle, ref_kind, _ = _perdir_select(repo, cands)

    assert got_kind == ref_kind, f"live kind {got_kind!r} != per-dir {ref_kind!r}"
    assert (got_bundle.name if got_bundle else None) == (
        ref_bundle.name if ref_bundle else None), "live bundle selection disagrees"


# --- done-contract 3: fresh / ambiguous semantics survive verbatim ----------


def test_fresh_bundle_still_outranks_every_tracked_one_under_batching(tmp_path, monkeypatch):
    """The uncommitted bundle is the one being generated right now, so it wins over every
    tracked bundle no matter how new. Lexically SMALLEST here, so slug order cannot fake
    the answer - and asserted together with the ONE-invocation count, because a batched
    walk that silently fell back to per-directory would pass this alone."""
    repo = _seed_bundles(tmp_path, _dated(8), untracked=["2026-01-02-aaa-live"])
    seen = _spy_git(monkeypatch)
    bundle, kind, detail = aud._select_active_bundle(repo, _candidates(repo))
    assert (kind, bundle.name) == ("fresh", "2026-01-02-aaa-live")
    assert detail == "2026-01-02-aaa-live"
    assert len(_log_calls(seen)) == 1


def test_staged_but_never_committed_bundle_is_still_fresh_under_batching(tmp_path):
    """`git add`ed by the very pre-commit run validating it - staged is NOT committed, so
    it has no add-date and is still the active bundle."""
    repo = _seed_bundles(tmp_path, _dated(6), staged=["2026-01-02-aaa-staged"])
    bundle, kind, _ = aud._select_active_bundle(repo, _candidates(repo))
    assert (kind, bundle.name) == ("fresh", "2026-01-02-aaa-staged")


def test_two_fresh_bundles_still_refuse_to_pick_under_batching(tmp_path):
    """The refusal this selector exists for: two uncommitted candidates -> bundle is None
    and kind is 'ambiguous'. A batched `git log` must not quietly reintroduce a silent
    pick - so assert the None, the kind, AND that BOTH names reach the detail."""
    repo = _seed_bundles(tmp_path, _dated(6),
                         untracked=["2026-01-02-aaa-live", "2026-01-03-bbb-live"])
    bundle, kind, detail = aud._select_active_bundle(repo, _candidates(repo))
    assert bundle is None
    assert kind == "ambiguous"
    assert "2026-01-02-aaa-live" in detail and "2026-01-03-bbb-live" in detail
    for tracked in ("slug-01", "slug-06"):
        assert tracked not in detail, "only the FRESH candidates belong in the ambiguity"


def test_prefix_sibling_slugs_are_not_cross_attributed(tmp_path):
    """'<slug>' and '<slug>-arc5' share a string prefix but not a path segment. If the
    batched attribution credits arc5's add-commit to the untracked '<slug>', the fresh
    bundle silently becomes a dated one and the gate validates the stale sibling -
    #372's exact failure, reintroduced through the batching door."""
    repo = _shape_prefix_siblings(tmp_path)
    bundle, kind, _ = aud._select_active_bundle(repo, _candidates(repo))
    assert (kind, bundle.name) == ("fresh", "2026-07-20-x")


def test_batched_log_failure_degrades_and_never_guesses(tmp_path, monkeypatch):
    """Frozen default 'fall back, do not crash': a failing `git log` takes the SAME outcome
    the per-directory method gives it today - degraded, bundle None, caller WARNs. Never a
    lexical guess, which is the stale-bundle false green this selector replaced."""
    repo = _seed_bundles(tmp_path, _dated(5))
    real = aud.subprocess.run

    def flaky(cmd, *a, **kw):
        if isinstance(cmd, (list, tuple)) and "log" in cmd:
            return subprocess.CompletedProcess(list(cmd), 128, "", "fatal: bad revision")
        return real(cmd, *a, **kw)

    monkeypatch.setattr(aud.subprocess, "run", flaky)
    bundle, kind, detail = aud._select_active_bundle(repo, _candidates(repo))
    assert bundle is None
    assert kind == "degraded"
    assert detail


def test_every_batched_selector_git_call_still_receives_the_scrubbed_env(tmp_path, monkeypatch):
    """The env scrub is a FROZEN default, not an incidental detail: an inherited GIT_DIR
    resolves the guard to the WRONG toplevel and degrades selection to the lexical
    fallback ([#355] recursion). Batching changes WHICH calls exist, so re-assert the
    invariant over the calls that now exist - including the batched log."""
    repo = _seed_bundles(tmp_path, _dated(6))
    monkeypatch.setenv("GIT_DIR", str(tmp_path / "nowhere" / ".git"))
    monkeypatch.setenv("GIT_INDEX_FILE", str(tmp_path / "nowhere" / "index"))
    monkeypatch.setenv("GIT_AUTHOR_NAME", "Keep Me")

    seen = []
    real = aud.subprocess.run

    def spy(cmd, *a, **kw):
        if isinstance(cmd, (list, tuple)) and cmd and cmd[0] == "git":
            seen.append((list(cmd), dict(kw.get("env") or {})))
        return real(cmd, *a, **kw)

    monkeypatch.setattr(aud.subprocess, "run", spy)
    bundle, kind, _ = aud._select_active_bundle(repo, _candidates(repo))
    assert kind == "add-date", "the scrub failed and selection degraded"
    assert bundle is not None

    log_calls = [(c, e) for c, e in seen if "log" in c]
    assert len(log_calls) == 1
    for cmd, env in seen:
        assert env, f"no explicit env passed to {cmd} - it would inherit os.environ"
        assert "GIT_DIR" not in env and "GIT_INDEX_FILE" not in env
        assert env.get("GIT_AUTHOR_NAME") == "Keep Me"


# --- frozen default: chunk above a stated bound, still O(chunks) ------------


def test_pathspec_chunking_is_bounded_by_argv_budget_not_candidate_count(tmp_path, monkeypatch):
    """Windows caps a command line at 32767 chars, so an unbounded pathspec list is a
    crash waiting for a big enough corpus. Chunking keeps it O(chunks): with the budget
    forced down to a few pathspecs' worth, 9 candidates cost far fewer than 9 calls - and
    the SELECTION is identical to the unchunked one."""
    repo = _seed_bundles(tmp_path, _dated(9))
    cands = _candidates(repo)

    unchunked = aud._select_active_bundle(repo, cands)

    monkeypatch.setattr(aud, "_BUNDLE_LOG_PATHSPEC_BUDGET", 80)
    seen = _spy_git(monkeypatch)
    chunked = aud._select_active_bundle(repo, cands)
    calls = len(_log_calls(seen))

    assert 1 < calls < len(cands), f"expected chunked-but-bounded, saw {calls} for 9 dirs"
    assert (chunked[0].name, chunked[1]) == (unchunked[0].name, unchunked[1])


def test_default_argv_budget_leaves_the_live_corpus_in_one_chunk():
    """The stated bound, pinned. The live tree's ~87 bundles are ~4 KB of pathspec; the
    budget must be comfortably above that (so 'ONE invocation' is the real behaviour here)
    and comfortably below Windows' 32767-char command-line cap (so it is a real guard)."""
    assert 8_000 <= aud._BUNDLE_LOG_PATHSPEC_BUDGET <= 30_000
    worst = len("docs/handoffs/2026-09-01-dev-knowledge-architect-v7") + 1
    assert aud._BUNDLE_LOG_PATHSPEC_BUDGET // worst >= 150, "budget too tight for the corpus"


# --- v7.1: the required-row rung (P11 decision carriage) --------------------
#
# HANDOFF_PROCESS §5's evidence-block contract has always said "a missing required row is not
# a pass". Until v7.1 that was prose with no organ: a bundle could silently ship without P11
# and the structural gate saw nothing to classify. These pin the rung and its era gate.

_P11_ROW = ("P11", "does a flush-left carried-by: appear in each decision file head",
            "`protocols/HANDOFF_PROCESS.md` `## 5. The teeth-y forced primary-source read (#148 a)`",
            "the window's decision files are written after this bundle is cut",
            "`grep -l -E '^carried-by:' \"$env:CLAUDE_PROMPTS_DIR/to-cc/\"DECLARE-*`")


def test_v71_bundle_without_p11_fails_the_required_row_rung(tmp_path):
    """A bundle cut in the v7.1 era that ships no P11 row FAILs — the row is required."""
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL], slug="2026-09-07-dev-knowledge-architect")
    by = _by_id(vhp.verify(bundle))
    assert "P11" in by, "no P11 result synthesized for an in-era bundle missing the row"
    assert by["P11"].status == "fail"
    assert "required" in by["P11"].detail


def test_pre_v71_bundle_without_p11_is_judged_by_its_own_era(tmp_path):
    """Bundles cut before the era are immutable artifacts — the rung must not condemn them."""
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL], slug="2026-06-12-b")
    by = _by_id(vhp.verify(bundle))
    assert "P11" not in by


def test_v71_bundle_carrying_p11_is_not_given_a_synthetic_fail(tmp_path):
    """The rung fires on ABSENCE only; a present P11 row is classified like any other."""
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL, _P11_ROW],
                          slug="2026-09-07-dev-knowledge-architect")
    results = vhp.verify(bundle)
    p11 = [r for r in results if r.probe_id == "P11"]
    assert len(p11) == 1, "the rung synthesized a duplicate row alongside the real one"
    assert "required" not in p11[0].detail


def test_required_row_rung_accepts_emphasised_and_backticked_ids(tmp_path):
    """`**P11**` / `` `P11` `` / `p11` are the SAME row typeset differently — all count."""
    for i, typeset in enumerate(("**P11**", "`P11`", "p11", " P11 ")):
        row = (typeset,) + _P11_ROW[1:]
        bundle = _init_bundle(tmp_path / f"case{i}", [_PASS_SYMBOL, row],
                              slug="2026-09-07-dev-knowledge-architect")
        assert "P11" not in {r.probe_id for r in vhp.verify(bundle)
                             if "required" in r.detail}, f"{typeset} was read as absent"


def test_required_row_rung_does_not_fold_a_different_id_onto_p11(tmp_path):
    """`P-11` is not `P11`. A blanket punctuation strip folds them together and PASSes the
    exact omission the rung exists to catch (terra HIGH, 2026-09-07)."""
    row = ("P-11",) + _P11_ROW[1:]
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL, row],
                          slug="2026-09-07-dev-knowledge-architect")
    by = _by_id(vhp.verify(bundle))
    assert "P11" in by and by["P11"].status == "fail"


def test_required_row_rung_is_era_gated_by_the_shared_predicate(tmp_path):
    """The era gate reuses bundle_at_or_after — one predicate, not a second date compare."""
    assert vhp.bundle_at_or_after("2026-09-07-x", vhp._V71_ERA)
    assert not vhp.bundle_at_or_after("2026-09-06-dev-knowledge-architect", vhp._V71_ERA)


# --- the zero-row bypass, CLOSED ([#643] leg b, AMEND-643-001 §2) -----------
#
# WHAT THIS REVERSES, on the record rather than silently. Until 2026-09-08 the rung was
# NARROWED to a bundle that actually HAS probe rows, and the narrowing was pinned by a test
# whose reasoning was: a `PROBES.md` parsing to zero rows is a non-probe artifact, the same
# class `verify()` returns [] for when there is no `PROBES.md` at all, so firing there would
# manufacture a P11 FAIL for every such directory.
#
# THAT ARGUMENT CONFLATED TWO DIFFERENT ABSENCES, and the module's own docstring already said
# so ("THE HOLE IS WIDER THAN 'someone ships an empty table' … recorded here rather than
# papered over, because the next author of that seal needs to know this door is open"). NO
# `PROBES.md` is a non-v5 bundle — genuinely nothing to classify. A `PROBES.md` that EXISTS
# and parses to zero rows is a v5-lineage bundle whose probe manifest could not be read: a
# reworded column header, a missing separator, a table mangled by a template edit. Such a
# bundle bypasses not just this rung but EVERY present-row rung in this file, while `main()`
# prints the reassuring "no probes found". A validator that reports a clean run over a
# manifest it could not read is the toothless door P11 exists to catch, one along.
#
# Ruled: `to-cc/AMEND-643-001.md` §2 ("Zero rows = FAIL, not pass"), 2026-09-08. Era-gated by
# the SAME `bundle_at_or_after` predicate as the rest, for the same reason: bundles cut before
# v7.1 are immutable and cannot grow a manifest.

def test_a_present_probes_file_that_parses_to_zero_rows_FAILS(tmp_path):
    """The bypass, closed. An in-era bundle whose PROBES.md cannot be read as a probe table is
    BROKEN, and a gate must not report a clean run over rows that never parsed."""
    bundle = tmp_path / "2026-09-07-dev-knowledge-architect"
    bundle.mkdir()
    (bundle / "PROBES.md").write_text("no rows here\n", encoding="utf-8")
    results = vhp.verify(bundle)
    assert [r.status for r in results] == ["fail"]
    assert "no probe rows" in results[0].detail


def test_no_probes_file_at_all_is_still_a_non_v5_bundle_and_returns_empty(tmp_path):
    """The distinction the reversal turns on, pinned so the two absences stay apart: an ABSENT
    manifest is a non-v5 bundle with nothing to classify; an UNREADABLE one is a defect."""
    bundle = tmp_path / "2026-09-07-dev-knowledge-architect"
    bundle.mkdir()
    assert vhp.verify(bundle) == []


def test_the_zero_row_refusal_is_era_gated_like_every_other_rung(tmp_path):
    """A pre-v7.1 bundle is an immutable sealed artifact; condemning it for a rule written
    after it was sealed is the one thing 'judged by their own era' forbids."""
    bundle = tmp_path / "2026-06-12-b"
    bundle.mkdir()
    (bundle / "PROBES.md").write_text("no rows here\n", encoding="utf-8")
    assert vhp.verify(bundle) == []


# --- [#643] P11 leg 2 at ACCEPTANCE time -------------------------------------
# Terra pass 2, and it is the hole the pass-1 repair opened. Leg 2 refuses at the POST-FILL
# assemble, and the cold in-cut pass defers (it has no filled residual to judge). Between the
# two sits a real gap: the cold pass writes PASTE_THIS.md, so an operator who never re-runs the
# assembler can commit a bundle whose residual names none of its `carried-by: OPEN` files --
# the exact shortfall leg 2 exists to prevent, reached by simply not running the second step.
#
# `/handoff-verify` is where a bundle is ACCEPTED (HANDOFF_PROCESS §5), so it is where the
# question "did the residual actually discharge its debt" has to be answerable. This closes the
# loop to three stages with no silent path: the cut DEFERS, the post-fill assemble REFUSES, and
# acceptance FAILS. Each names the files owed.

_CARRIAGE_ERA_SLUG = "2026-09-09-carriage"


@pytest.fixture
def as_hub(monkeypatch):
    """Treat the test's temp repo as the hub for the carriage rung.

    The rung is HUB-ONLY by repo identity because the transport is a MACHINE-level surface.
    Without this fixture these tests would be skipped by their own scoping; WITH it they
    exercise the rung against a temp transport rather than the operator's real one, which is
    the whole point -- a suite result must not depend on what is sitting in the live
    CLAUDE_PROMPTS_DIR today.
    """
    import gen_handoff as gh
    monkeypatch.setattr(gh, "_is_hub", lambda _root: True)


def _transport_with_open(tmp_path, name="BATCH-2026-09-07-CLOSE-CONTRACTS.md"):
    transport = tmp_path / "transport"
    (transport / "to-cc").mkdir(parents=True)
    (transport / "to-cc" / name).write_text(
        f"# {name}\ncarried-by: OPEN -- in flight\n", encoding="utf-8")
    return transport, name


def test_a_residual_naming_none_of_its_open_carriers_fails_verification(tmp_path, monkeypatch, as_hub):
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL], slug=_CARRIAGE_ERA_SLUG)
    (bundle / "RESIDUAL.md").write_text("# Residual\n\nNothing carried.\n", encoding="utf-8")
    transport, name = _transport_with_open(tmp_path)
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(transport))

    results = _by_id(vhp.verify(bundle))
    row = results.get(vhp._CARRIAGE_FINDING_ID)
    assert row is not None and row.status == "fail", results
    assert name in row.detail


def test_a_residual_that_names_them_verifies_clean(tmp_path, monkeypatch, as_hub):
    """The negative control. Without it the row above proves only that the rung can fire, never
    that a correctly-carried window can be accepted -- which is the deadlock every gate in this
    family was ruled against."""
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL], slug=_CARRIAGE_ERA_SLUG)
    transport, name = _transport_with_open(tmp_path)
    (bundle / "RESIDUAL.md").write_text(
        f"# Residual\n\nCarried OPEN: `to-cc/{name}` -- owned by [#643].\n", encoding="utf-8")
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(transport))

    assert vhp._CARRIAGE_FINDING_ID not in _by_id(vhp.verify(bundle))


def test_a_pre_era_bundle_is_not_retro_judged(tmp_path, monkeypatch, as_hub):
    """THE SCOPING, as a test rather than a comment. `verify` runs over historical bundles, and
    the transport it would judge them against is TODAY's -- every past bundle would be re-judged
    on files that did not exist when it was cut. The era gate is the same predicate
    `_missing_required_rows` and `audit.check_supplement_folded` already share; a third one
    written by hand is how two era gates disagree."""
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL], slug="2026-06-12-b")
    (bundle / "RESIDUAL.md").write_text("# Residual\n\nNothing carried.\n", encoding="utf-8")
    transport, _name = _transport_with_open(tmp_path)
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(transport))

    assert vhp._CARRIAGE_FINDING_ID not in _by_id(vhp.verify(bundle))


def test_an_unmeasurable_transport_is_not_a_silent_pass(tmp_path, monkeypatch, as_hub):
    """An unknown boundary is not a clean one (DEFECT E-29, the reason leg 2's own transport
    arm refuses rather than assembles). Here the honest verdict is `skipped` -- this validator
    is resolve-only and reports degradation rather than manufacturing either verdict -- but it
    must not vanish, because a rung that disappears when it cannot measure reads as a pass."""
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL], slug=_CARRIAGE_ERA_SLUG)
    (bundle / "RESIDUAL.md").write_text("# Residual\n\nNothing carried.\n", encoding="utf-8")
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(tmp_path / "does-not-exist"))
    monkeypatch.setenv("USERPROFILE", str(tmp_path / "no-home"))
    monkeypatch.setenv("HOME", str(tmp_path / "no-home"))

    row = _by_id(vhp.verify(bundle)).get(vhp._CARRIAGE_FINDING_ID)
    assert row is not None and row.status == "skipped", row


def test_a_non_hub_repo_is_never_judged_against_this_machines_transport(tmp_path, monkeypatch):
    """THE GUARD THAT KEEPS THE SUITE DETERMINISTIC, and it is here because the first cut of
    this rung failed exactly this way.

    The transport is a MACHINE-level surface (`CLAUDE_PROMPTS_DIR`). Without the hub-identity
    scope, ANY bundle handed to `verify()` -- including one a unit test synthesizes in a temp
    directory -- was judged against whatever decision files happened to be sitting in the
    operator's real transport. That was witnessed, not imagined: a dogfood probe count moved
    from 15 to 16 because the operator's live transport carried unnamed OPEN carriers, so the
    suite's answer depended on a directory outside the repo. Note the slug below is in-era
    (`bundle_at_or_after` is fail-closed on an unparseable date, so `0000-00-00-x` counts as
    IN-era) -- the era gate does NOT cover this case, which is why the scope has to.

    No `as_hub` fixture here: this test asserts the REAL predicate, so stubbing it would
    remove its subject.
    """
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL], slug="0000-00-00-x")
    (bundle / "RESIDUAL.md").write_text("# Residual\n\nNothing carried.\n", encoding="utf-8")
    transport, _name = _transport_with_open(tmp_path)
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(transport))

    assert vhp._CARRIAGE_FINDING_ID not in _by_id(vhp.verify(bundle))


def _commit_bundle(repo_root):
    ident = ["-c", "user.name=t", "-c", "user.email=t@t"]
    subprocess.run(["git", "init", "-b", "main"], cwd=repo_root, check=True, capture_output=True)
    subprocess.run(["git", *ident, "add", "-A"], cwd=repo_root, check=True, capture_output=True)
    subprocess.run(["git", *ident, "commit", "-m", "cut"], cwd=repo_root, check=True,
                   capture_output=True)


def test_an_already_committed_bundle_is_no_longer_judged(tmp_path, monkeypatch, as_hub):
    """THE WEDGE THIS GATE MUST NOT BECOME, and the repo has a ruling on exactly this shape.

    `check_handoff_probes` runs at the COMMIT tier, so an unbounded rung re-judges the active
    bundle on EVERY later commit. The transport keeps growing; a decision file added after the
    cut can never appear in that bundle's residual, because a committed bundle is IMMUTABLE.
    The result would be every subsequent commit in the repo failing on a defect the committer
    is not permitted to repair -- which is verbatim the argument `audit.py` already records for
    keeping `check_funnel_lifecycle` at SHIP rather than COMMIT tier.

    The bound is the same repairability criterion leg 2 rests on throughout: judge while the
    bundle can still be fixed. Once it is in HEAD it cannot, so the rung goes silent rather
    than shouting at someone who cannot act. It keeps full teeth where they are actionable --
    the cut, `/handoff-verify`, and the commit that first lands the bundle -- which is strictly
    more than the historical failure had, where two bundles shipped and the defect surfaced
    only after they were committed and merged.
    """
    bundle = _init_bundle(tmp_path, [_PASS_SYMBOL], slug=_CARRIAGE_ERA_SLUG)
    (bundle / "RESIDUAL.md").write_text("# Residual\n\nNothing carried.\n", encoding="utf-8")
    transport, name = _transport_with_open(tmp_path)
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(transport))

    # Uncommitted: still repairable, so it is judged -- the control for the assertion below.
    before = _by_id(vhp.verify(bundle))
    assert before[vhp._CARRIAGE_FINDING_ID].status == "fail"
    assert name in before[vhp._CARRIAGE_FINDING_ID].detail

    _commit_bundle(tmp_path / "repo")
    assert vhp._CARRIAGE_FINDING_ID not in _by_id(vhp.verify(bundle))
