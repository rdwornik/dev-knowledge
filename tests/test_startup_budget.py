"""The start-up context budget, rows [#1616] [#1617] [#1618] (BATCH-TOKEN-CUTS-2026-10-16).

DIGEST-NIGHT-CLOSEOUT-2026-10-15 §5 measured that this repo injects ~25 k tokens into every turn
of every session. The fast tests below pin the BYTE sizes of the three always-loaded surfaces
under their targets; the live test re-runs the same measurement command and is skipped unless
`DEV_KNOWLEDGE_LIVE_TOKENS=1` (it needs auth and costs a few cents).

HONEST LIMIT: bytes are a proxy. The live test is the witness; the fast tests keep the cut cut.
"""
from __future__ import annotations

import json
import os
import shutil
import statistics
import subprocess
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent

#: CLAUDE.md plus every file it @-imports -- the real session payload (the byte-cap module's
#: docstring names the expanded payload as the unbuilt gate; this is it).
CLAUDE_MD_CAP = 21 * 1024
CLAUDE_MD_EXPANDED_CAP = 31 * 1024
#: The SessionStart hook's injected stdout (was 8,192).
SESSION_START_CAP = 2560
#: The always-loaded rule file (was 5,694).
GIT_DISCIPLINE_CAP = 2560
#: The live witness: median start-up tokens must drop by at least this much vs the baseline.
BASELINE_TOKENS = 55_987
REQUIRED_DROP = 6_000


def _size(p: Path) -> int:
    return p.stat().st_size


def _imports(doc: Path) -> list[Path]:
    out = []
    for line in doc.read_text(encoding="utf-8").splitlines():
        if line.startswith("@") and " " not in line:
            out.append(_REPO_ROOT / line[1:])
    return out


def test_claude_md_is_under_the_start_up_target() -> None:
    assert _size(_REPO_ROOT / "CLAUDE.md") <= CLAUDE_MD_CAP


def test_claude_md_with_its_imports_is_under_the_expanded_target() -> None:
    claude = _REPO_ROOT / "CLAUDE.md"
    total = _size(claude) + sum(_size(p) for p in _imports(claude))
    assert total <= CLAUDE_MD_EXPANDED_CAP, total


def test_session_start_output_cap_is_the_small_one() -> None:
    from scripts.hooks import session_start as ss
    assert ss.OUTPUT_CAP_BYTES <= SESSION_START_CAP


def test_session_start_writes_its_full_text_to_a_file_the_notice_names() -> None:
    from scripts.hooks import session_start as ss
    assert ss.FULL_TEXT_FILE.name
    assert ss.FULL_TEXT_FILE.name in " ".join(ss.compose(["[x] " + "y" * 100] * 200))


def test_git_discipline_rule_is_under_target_and_keeps_its_verify_lines() -> None:
    p = _REPO_ROOT / ".claude" / "rules" / "git-discipline.md"
    assert _size(p) <= GIT_DISCIPLINE_CAP
    assert p.read_text(encoding="utf-8").count("- verify:") >= 3


_RELOCATED_ANCHORS = (
    # git-discipline.md, one distinctive phrase per relocated block
    "alive is a defect, not a pending decision", "`automation/*` is EXPLICITLY PROTECTED",
    "The two protected globs have opposite lifecycles", "Both places, or the merge is unfinished",
    "The ancestor proof is the safety check", "WORKTREE TEARDOWN IS TWO BRANCHES, NOT ONE",
    "| carrier branch | tip | closes when | expires |", "docs: update PLAYBOOK S5 council debate format",
    # CLAUDE.md section 9, section 4 and the header
    "## 9. Hooks active", "A roster, not a manual", "disableAllHooks", "ADR-108",
    "**TDD", "**Spec-driven development", "**Freshness cadence:**", "**File lifecycle:**",
    "**Scope tags:**",
)


def test_relocated_detail_has_its_home() -> None:
    home = _REPO_ROOT / ".claude" / "BOOT-REFERENCE.md"
    assert home.is_file()
    text = home.read_text(encoding="utf-8")
    missing = [a for a in _RELOCATED_ANCHORS if a not in text]
    assert not missing, missing


def _fake_reader(lines):
    from scripts.hooks import session_start as ss

    def entry():
        for line in lines:
            print(line)
    return ss.Reader("fake", "scripts/x.py", entry)


def test_main_writes_the_uncapped_text_while_stdout_stays_capped(tmp_path, monkeypatch, capsys) -> None:
    from scripts.hooks import session_start as ss
    full = tmp_path / "SESSION-START-FULL.txt"
    lines = [f"[bulk] line {i} " + "x" * 100 for i in range(200)]
    monkeypatch.setattr(ss, "FULL_TEXT_FILE", full)
    monkeypatch.setattr(ss, "READERS", (_fake_reader(lines),))
    monkeypatch.setattr(ss, "read_payload", lambda *_a, **_k: "")
    assert ss.main([]) == 0
    out = capsys.readouterr().out
    assert len(out.encode("utf-8")) <= ss.OUTPUT_CAP_BYTES
    assert full.read_text(encoding="utf-8").splitlines() == lines


def test_a_failed_save_is_named_not_advertised(tmp_path, monkeypatch, capsys) -> None:
    from scripts.hooks import session_start as ss
    # the target's parent is a FILE, so mkdir/write raise OSError
    blocker = tmp_path / "blocker"
    blocker.write_text("x", encoding="utf-8")
    monkeypatch.setattr(ss, "FULL_TEXT_FILE", blocker / "SESSION-START-FULL.txt")
    monkeypatch.setattr(ss, "READERS", (_fake_reader([f"[bulk] {i} " + "x" * 100 for i in range(200)]),))
    monkeypatch.setattr(ss, "read_payload", lambda *_a, **_k: "")
    assert ss.main([]) == 0
    out = capsys.readouterr().out
    assert "full text not saved" in out
    assert "full text: logs/" not in out


@pytest.mark.skipif(os.environ.get("DEV_KNOWLEDGE_LIVE_TOKENS") != "1" or not shutil.which("claude"),
                    reason="live: needs DEV_KNOWLEDGE_LIVE_TOKENS=1 and an authenticated claude CLI")
def test_live_startup_tokens_dropped_by_the_required_margin() -> None:
    totals = []
    for _ in range(3):
        r = subprocess.run(["claude", "-p", "Reply with OK.", "--output-format", "json",
                            "--model", "claude-sonnet-5-5"], cwd=_REPO_ROOT, capture_output=True,
                           text=True, stdin=subprocess.DEVNULL, timeout=180)
        u = json.loads(r.stdout)["usage"]
        totals.append(u["input_tokens"] + u["cache_creation_input_tokens"] + u["cache_read_input_tokens"])
    assert statistics.median(totals) <= BASELINE_TOKENS - REQUIRED_DROP, totals
