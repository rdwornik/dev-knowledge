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
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

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


def test_header_tokens_only_picks_markdown_headers():
    toks = vhp.header_tokens("`VISION.md` `## Vision`")
    assert toks == ["## Vision"]


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
    assert findings[0].status == "pass"


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
# WARN (honest-partial), a genuine miss still FAILs, a real target file PASSes. #NNN hardens
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
# [#370] Active-bundle SELECTION: git add-date, never slug order.
# ---------------------------------------------------------------------------


def _git_repo(root: Path):
    """Make `root` a throwaway git repo; returns a runner. (tests/test_fleet_parity.py idiom.)"""
    root.mkdir(parents=True, exist_ok=True)

    def run(args, env=None):
        return subprocess.run(["git", *args], cwd=str(root), capture_output=True,
                              text=True, encoding="utf-8", errors="replace",
                              env=None if env is None else {**os.environ, **env})

    if run(["init", "-q", "-b", "main"]).returncode != 0:
        run(["init", "-q"])
    for cfg in (["core.autocrlf", "false"], ["user.email", "hp@example.com"],
                ["user.name", "Handoff Probe Test"], ["commit.gpgsign", "false"]):
        run(["config", *cfg])
    return run


def _commit_at(run, pathspec: str, when: str, msg: str):
    """Commit `pathspec` with BOTH author and committer dates pinned, so add-date ordering
    under test is deterministic and independent of wall-clock or checkout mtime."""
    run(["add", "--", pathspec])
    run(["commit", "-q", "-m", msg],
        env={"GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when})


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
    _commit_at(run, "docs/handoffs/2026-07-20-x-arc5", "2026-07-19T14:42:52+02:00", "arc5")
    _commit_at(run, ".", "2026-07-20T17:04:33+02:00", "plain + repo files")
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
    """[#370 + #355] The selector is vulnerable to the very defect #355 fixed. Under
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
