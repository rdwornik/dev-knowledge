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
CLAUDE_MD_CAP = 17 * 1024
CLAUDE_MD_EXPANDED_CAP = 23 * 1024
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


def test_relocated_detail_has_its_home() -> None:
    home = _REPO_ROOT / ".claude" / "BOOT-REFERENCE.md"
    assert home.is_file()
    text = home.read_text(encoding="utf-8")
    for needle in ("Hooks active", "MERGE IS ATOMIC", "WORKTREE TEARDOWN IS TWO BRANCHES"):
        assert needle in text, needle


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
