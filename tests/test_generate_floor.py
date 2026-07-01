"""Tests for scripts/generate_floor.py — ceiling refusal, hash stability, content fidelity,
F5 self-containment, and emit behavior (ADR-78 O2)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import pytest
from click.testing import CliRunner

import generate_floor as gf


# ---------------------------------------------------------------------------
# The shipped template
# ---------------------------------------------------------------------------

def test_shipped_template_is_valid_under_ceiling():
    floor = gf.render_floor()
    assert gf.validate(floor) == []
    assert gf.estimate_tokens(floor) <= gf.FLOOR_TOKEN_CEILING


def test_shipped_template_is_f5_clean_and_urlless():
    floor = gf.render_floor()
    assert gf.f5_hits(floor) == []
    assert gf.url_hits(floor) == []


def test_shipped_template_whitelist_content_present():
    """Content-set fidelity: each ADR-75 methodology_surface whitelist element surfaces."""
    floor = gf.render_floor()
    assert "Model" in floor and "Effort" in floor          # prompt-header
    assert "STOP after UNDERSTAND" in floor                 # valve discipline
    assert "after each numbered step" in floor              # cadence
    assert "--no-ff" in floor and "/ship" in floor          # ship rule
    assert "/clear" in floor                                # context budget
    assert "Re-anchor rule" in floor                        # re-anchor mechanic
    assert "gotchas skill" in floor                         # safety pointer
    assert ".dev-knowledge" in floor                        # labeled escape-hatch (ADR-78 D1)


# ---------------------------------------------------------------------------
# Hash stability / determinism
# ---------------------------------------------------------------------------

def test_hash_is_deterministic():
    floor = gf.render_floor()
    assert gf.floor_sha256(floor) == gf.floor_sha256(floor)


def test_hash_is_crlf_invariant():
    """autocrlf-proof: CRLF and LF variants of the same content hash identically."""
    lf = "# Floor\n\nLine one.\nLine two.\n"
    crlf = lf.replace("\n", "\r\n")
    assert gf.floor_sha256(lf) == gf.floor_sha256(crlf)


def test_render_floor_ends_with_single_newline():
    assert gf.render_floor().endswith("\n")


# ---------------------------------------------------------------------------
# Ceiling refusal
# ---------------------------------------------------------------------------

def _write_template(tmp_path: Path, body: str) -> Path:
    t = tmp_path / "floor.md.tmpl"
    t.write_text(body, encoding="utf-8")
    return t


def test_ceiling_refusal_validate(tmp_path: Path):
    big = "# Floor\n\n" + ("word " * 2000)  # ~10k chars -> ~2860 tokens
    floor = gf.render_floor(_write_template(tmp_path, big))
    issues = gf.validate(floor)
    assert any("token ceiling exceeded" in i for i in issues)


def test_ceiling_refusal_generate_exits_1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(gf, "HUB_CANONICAL_SHA", tmp_path / "hub.sha256")
    big = "# Floor\n\n" + ("word " * 2000)
    tpl = _write_template(tmp_path, big)
    result = CliRunner().invoke(gf.cli, ["generate", "--template", str(tpl)])
    assert result.exit_code == 1
    assert "REFUSED" in result.output
    assert not (tmp_path / "hub.sha256").exists()  # refused before any write


# ---------------------------------------------------------------------------
# F5 self-containment + zero-URL
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("leak", [
    "See [#121] in the hub backlog.",
    "Read LESSONS.md for context.",
    "Prepend to JOURNAL.md at wrap.",
    "Per ADR-78 the floor is generated.",
    "Check docs/handoffs/ for the bundle.",
])
def test_f5_leak_detected(tmp_path: Path, leak: str):
    floor = gf.render_floor(_write_template(tmp_path, f"# Floor\n\n{leak}\n"))
    assert gf.f5_hits(floor)
    assert any("F5 self-containment" in i for i in gf.validate(floor))


def test_url_policy_detected(tmp_path: Path):
    floor = gf.render_floor(_write_template(tmp_path, "# Floor\n\nSee https://example.com\n"))
    assert gf.url_hits(floor)
    assert any("zero-URL" in i for i in gf.validate(floor))


# ---------------------------------------------------------------------------
# Emit behavior
# ---------------------------------------------------------------------------

def test_generate_out_dir_writes_floor_and_matching_sidecar(tmp_path: Path, monkeypatch):
    hub_sha = tmp_path / "hub.sha256"
    monkeypatch.setattr(gf, "HUB_CANONICAL_SHA", hub_sha)
    child = tmp_path / "child"
    child.mkdir()
    result = CliRunner().invoke(gf.cli, ["generate", "--out-dir", str(child)])
    assert result.exit_code == 0

    # Floor + sidecar land under the child's .claude/, NOT the repo root.
    claude_dir = child / gf.CHILD_CLAUDE_DIRNAME
    floor_file = claude_dir / gf.FLOOR_FILENAME
    sidecar = claude_dir / gf.SIDECAR_FILENAME
    assert floor_file.exists() and sidecar.exists()
    assert not (child / gf.FLOOR_FILENAME).exists()  # not at root
    # The install note (with the @-include + pre-commit install steps) is printed.
    assert "@.claude/CLAUDE-FLOOR.md" in result.output
    assert "pre-commit install" in result.output

    expected = gf.floor_sha256(floor_file.read_text(encoding="utf-8"))
    assert expected in sidecar.read_text(encoding="utf-8")
    # Hub canonical reference matches the emitted sidecar (currency anchor parity).
    assert expected in hub_sha.read_text(encoding="utf-8")


def test_generate_no_out_dir_only_refreshes_hub_ref(tmp_path: Path, monkeypatch):
    hub_sha = tmp_path / "hub.sha256"
    monkeypatch.setattr(gf, "HUB_CANONICAL_SHA", hub_sha)
    result = CliRunner().invoke(gf.cli, ["generate"])
    assert result.exit_code == 0
    assert hub_sha.exists()
    assert gf.floor_sha256(gf.render_floor()) in hub_sha.read_text(encoding="utf-8")


def test_generate_refuses_bad_out_dir(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(gf, "HUB_CANONICAL_SHA", tmp_path / "hub.sha256")
    missing = tmp_path / "does-not-exist"
    result = CliRunner().invoke(gf.cli, ["generate", "--out-dir", str(missing)])
    assert result.exit_code == 1
    assert "not a directory" in result.output


def test_check_exits_0_on_shipped_template():
    result = CliRunner().invoke(gf.cli, ["check"])
    assert result.exit_code == 0
    assert "floor valid" in result.output


# ---------------------------------------------------------------------------
# Install note — must be paste-ready (the surprise-free contract, 2026-06-08)
# ---------------------------------------------------------------------------

def _extract_check_floor_hash_script() -> str:
    """Pull the embedded check_floor_hash.py block out of the install note and dedent it.

    The script is indented 7 spaces under step 2; collect from the shebang until the
    first non-indented, non-blank line (step 3's heading)."""
    lines = gf.INSTALL_NOTE.splitlines()
    start = next(i for i, ln in enumerate(lines) if "#!/usr/bin/env python3" in ln)
    out: list[str] = []
    for ln in lines[start:]:
        if ln.strip() == "":
            out.append("")
        elif ln.startswith("       "):  # 7-space indent
            out.append(ln[7:])
        else:
            break
    return "\n".join(out)


def test_install_note_has_no_leaked_escaped_quote():
    """A raw-string docstring escape (\\") would leak verbatim and break a paste."""
    assert '\\"' not in gf.INSTALL_NOTE


def test_install_note_is_pure_ascii():
    """ASCII-only so it survives a Windows cp1252 console (the embedded hook's
    print() strings must not UnicodeEncodeError when it reports drift)."""
    gf.INSTALL_NOTE.encode("ascii")  # raises UnicodeEncodeError on any non-ASCII char


def test_emitted_check_floor_hash_script_is_valid_python():
    """The check_floor_hash.py the note hands a child must compile as-is (paste-ready)."""
    script = _extract_check_floor_hash_script()
    assert "def main()" in script and "sys.exit(main())" in script
    compile(script, "check_floor_hash.py", "exec")  # raises SyntaxError if malformed


def test_guard_script_is_single_sourced_byte_identical():
    """The carrier-written guard (CHECK_FLOOR_HASH_SCRIPT) and the INSTALL_NOTE-embedded
    guard MUST be byte-identical — one source, so the automated arm and the paste-ready
    manual runbook can never disagree (the drift this whole feature exists to kill)."""
    assert gf.CHECK_FLOOR_HASH_SCRIPT == gf.extract_check_floor_hash_script()
    # both the module extractor and this file's local extractor agree
    assert gf.CHECK_FLOOR_HASH_SCRIPT == _extract_check_floor_hash_script()


def test_guard_script_require_present_fails_loud_on_absent_floor(tmp_path: Path):
    """--require-present: an absent floor exits 1 with a named reason (session-start leg);
    without the flag an absent floor is permissive (exit 0, commit-time leg)."""
    import subprocess as _sp
    script = tmp_path / "check_floor_hash.py"
    script.write_text(gf.CHECK_FLOOR_HASH_SCRIPT, encoding="utf-8", newline="\n")
    (tmp_path / ".claude").mkdir()  # floor deliberately absent
    loud = _sp.run([sys.executable, str(script), "--require-present"], cwd=tmp_path,
                   capture_output=True, text=True)
    assert loud.returncode == 1 and "floor absent" in loud.stderr
    permissive = _sp.run([sys.executable, str(script)], cwd=tmp_path,
                         capture_output=True, text=True)
    assert permissive.returncode == 0  # no flag -> nothing to verify


def _extract_precommit_yaml_block() -> str:
    """Pull the .pre-commit-config.yaml block out of step 3 of the install note and
    dedent it (7-space indent, like the script block).

    Collect from the `repos:` line until the first non-indented, non-blank line
    (step 4's heading)."""
    lines = gf.INSTALL_NOTE.splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.strip() == "repos:")
    out: list[str] = []
    for ln in lines[start:]:
        if ln.strip() == "":
            out.append("")
        elif ln.startswith("       "):  # 7-space indent
            out.append(ln[7:])
        else:
            break
    return "\n".join(out).strip("\n")


def test_install_note_precommit_covers_create_if_absent():
    """G3 precondition fix: step 3 must work for a child with NO .pre-commit-config.yaml.
    The prose must cover both the create-from-scratch and append-to-existing paths."""
    note = gf.INSTALL_NOTE.lower()
    assert "no .pre-commit-config.yaml" in note          # create-if-absent path
    assert "already exists" in note                       # append-to-existing path
    assert "append" in note


def test_install_note_precommit_block_is_full_standalone_config():
    """The emitted yaml must be a COMPLETE config (top-level `repos:`), not a bare
    `- repo: local` fragment — a from-scratch child pastes it verbatim into a new file."""
    block = _extract_precommit_yaml_block()
    assert block.startswith("repos:")
    assert "- repo: local" in block
    assert "id: floor-hash-verify" in block


def test_install_note_precommit_block_parses_as_valid_precommit_config():
    """Real structural proof the from-scratch block is valid: it parses to a config with
    a local repo carrying the floor-hash-verify hook wired to the child-side script."""
    yaml = pytest.importorskip("yaml")
    cfg = yaml.safe_load(_extract_precommit_yaml_block())
    assert isinstance(cfg, dict) and "repos" in cfg
    repo = cfg["repos"][0]
    assert repo["repo"] == "local"
    hook = repo["hooks"][0]
    assert hook["id"] == "floor-hash-verify"
    assert hook["entry"] == "python .claude/check_floor_hash.py"
    assert hook["language"] == "system"
    assert hook["pass_filenames"] is False


def test_install_note_carries_gitignore_negation_block():
    """Step 5 must hand the child a .gitignore block that re-includes all three tracked
    files when .claude/ is ignored -- otherwise the floor needs a fragile `git add -f` (#138)."""
    note = gf.INSTALL_NOTE
    for line in (
        "!.claude/CLAUDE-FLOOR.md",
        "!.claude/CLAUDE-FLOOR.md.sha256",
        "!.claude/check_floor_hash.py",
    ):
        assert line in note


def test_install_note_negation_uses_contents_form_not_bare_dir():
    """Load-bearing correctness (verified empirically, #138): negations only re-include a file
    when the exclusion is the CONTENTS-form `.claude/*`. A bare `.claude/` DIRECTORY
    exclusion silently defeats the negations (git won't re-include under an excluded dir),
    so the block git would actually honor must pair `.claude/*` with the negations."""
    stripped = [ln.strip() for ln in gf.INSTALL_NOTE.splitlines()]
    expected = [
        ".claude/*",
        "!.claude/CLAUDE-FLOOR.md",
        "!.claude/CLAUDE-FLOOR.md.sha256",
        "!.claude/check_floor_hash.py",
    ]
    # the contents-form line must sit immediately above the three negations as a contiguous block
    assert any(
        stripped[i:i + len(expected)] == expected for i in range(len(stripped))
    ), "contents-form `.claude/*` + 3 negations must appear as a contiguous .gitignore block"
