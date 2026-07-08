"""Hermetic tests for scripts/seed_runbook.py — the hub-side handoff-runbook seeder (#164 leg b).

Fully self-contained: a synthetic canonical source + a synthetic target repo under tmp_path.
The live hub tree is never written (the don't-touch guardrail — and no consumer is touched).
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import seed_runbook as sr  # noqa: E402

# A minimal stand-in for the canonical hub runbook: leading frontmatter (hub review metadata) +
# the H1 repo-name token + generic body.
_SOURCE = (
    "---\n"
    "last_reviewed: 2026-07-07\n"
    "reconciled_with: handoff-process@5.7\n"
    "---\n"
    "<!-- scope: meta -->\n"
    "# Handoffs — operator runbook (`.dev-knowledge`)\n"
    "\n"
    "Generic body — the run loop, the roles, the rationale. Same across repos.\n"
)


def _write_source(tmp_path):
    src = tmp_path / "source" / "docs" / "handoffs" / "README.md"
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text(_SOURCE, encoding="utf-8")
    return src


def _read_target(target_root):
    return (target_root / "docs" / "handoffs" / "README.md").read_text(encoding="utf-8")


def test_seeds_absent_target_with_repo_name_and_no_frontmatter(tmp_path):
    src = _write_source(tmp_path)
    target = tmp_path / "ai-council"
    res = sr.seed_runbook(target, source_readme=src)
    assert res.status == "seeded" and res.wrote
    body = _read_target(target)
    assert "# Handoffs — operator runbook (`ai-council`)" in body   # H1 repo-name swapped
    assert "Generic body" in body                                   # body carried verbatim
    assert not body.startswith("---")                               # source frontmatter dropped
    assert "{{" not in body and "last_reviewed" not in body


def test_second_seed_is_idempotent_current_no_write(tmp_path):
    src = _write_source(tmp_path)
    target = tmp_path / "corp-monorepo"
    first = sr.seed_runbook(target, source_readme=src)
    assert first.status == "seeded"
    before = _read_target(target)
    second = sr.seed_runbook(target, source_readme=src)
    assert second.status == "current" and second.wrote is False
    assert _read_target(target) == before                           # byte-identical, no churn


def test_drifted_body_is_updated_preserving_target_frontmatter(tmp_path):
    src = _write_source(tmp_path)
    target = tmp_path / "dev-knowledge-child"
    sr.seed_runbook(target, source_readme=src)
    # Simulate a repo that added its OWN frontmatter and whose body drifted.
    tgt_file = target / "docs" / "handoffs" / "README.md"
    tgt_file.write_text("---\nlocal: keep-me\n---\n# Handoffs — operator runbook (`x`)\nSTALE\n",
                        encoding="utf-8")
    res = sr.seed_runbook(target, source_readme=src, repo_name="dev-knowledge-child")
    assert res.status == "updated" and res.wrote
    out = _read_target(target)
    assert out.startswith("---\nlocal: keep-me\n---\n")             # target frontmatter PRESERVED
    assert "# Handoffs — operator runbook (`dev-knowledge-child`)" in out
    assert "STALE" not in out                                       # drifted body replaced


def test_check_is_a_dry_run_that_never_writes(tmp_path):
    src = _write_source(tmp_path)
    target = tmp_path / "fresh-repo"
    res = sr.seed_runbook(target, source_readme=src, write=False)
    assert res.status == "seeded" and res.wrote is False
    assert not (target / "docs" / "handoffs" / "README.md").exists()  # nothing written


def test_hub_self_seed_is_current_against_live_source(tmp_path):
    # Dogfood: generalizing the LIVE hub runbook with the hub's own name reproduces the hub body
    # exactly (the source IS the hub runbook) — so a hub self-seed classifies 'current', proving
    # the source<->live equivalence and that the seeder never churns the canonical file.
    live = sr._SOURCE_README
    body = sr.generalize_body(live.read_text(encoding="utf-8"), ".dev-knowledge")
    _, live_body = sr._split_frontmatter(live.read_text(encoding="utf-8"))
    assert body == live_body                                        # title token unchanged for the hub
    assert body.count("# Handoffs — operator runbook (`.dev-knowledge`)") == 1
