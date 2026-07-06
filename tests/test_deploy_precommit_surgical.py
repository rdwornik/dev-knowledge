"""#225 — the precommit carrier's comment-preserving surgical edit.

Done-when: deploying into a commented consumer config changes ONLY the
methodology-owned hook block and leaves surrounding comments/indentation
byte-identical. Covers both legs (apply + prune), idempotency, the
parse-equal post-condition's fallback teeth (a shape the splice engine
can't express still converges via the full re-dump), and CRLF fidelity.

All tests drive the real PrecommitCarrier.apply/prune/verify end-to-end
against crafted commented configs in tmp_path — no mocks on the code path
under test (the one monkeypatch test sabotages the splice to PROVE the
fallback, not to fake success).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "deploy"))

import carrier_precommit as cp  # noqa: E402

_HUB_REPO = "https://github.com/rdwornik/dev-knowledge"


def _hub_target(rev: str = "v9.9.9") -> dict:
    return {
        "config_path": ".pre-commit-config.yaml",
        "required_repos": [],
        "hub_hooks": {
            "rev": rev,
            "marker_hook_ids": ["toc-freshness", "codemap-freshness"],
            "repo": _HUB_REPO,
            "hooks": [{"id": "toc-freshness"}, {"id": "codemap-freshness"}],
        },
    }


def _local_hook_target() -> dict:
    return {
        "config_path": ".pre-commit-config.yaml",
        "required_repos": [],
        "required_local_hooks": [
            {
                "id": "floor-hash-verify",
                "name": "Verify CLAUDE-FLOOR.md matches its sha256 sidecar",
                "entry": "python .claude/check_floor_hash.py",
                "language": "system",
                "pass_filenames": False,
            }
        ],
    }


_COMMENTED_CONFIG = """\
# Consumer header comment -- must survive every deploy
# (second header line, indented oddly on purpose)
repos:
  # note attached to the hub entry below
  - repo: ../.dev-knowledge   # consumer-local clone path
    rev: v1.0.0  # deployed pin -- trailing comment must survive a rev bump
    hooks:
      - id: toc-freshness
  # the consumer's own hooks follow
  - repo: local
    hooks:
      - id: consumers-own
        name: Consumer's own hook   # keep me verbatim
        entry: echo hi
        language: system

# trailing top-level comment
default_language_version:
  python: python3
"""


def _write(tmp_path: Path, text: str, newline: str | None = None) -> Path:
    path = tmp_path / ".pre-commit-config.yaml"
    if newline:
        path.write_bytes(text.replace("\n", newline).encode("utf-8"))
    else:
        path.write_bytes(text.encode("utf-8"))
    return path


def _read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


# ---------------------------------------------------------------------------
# apply leg
# ---------------------------------------------------------------------------


def test_rev_bump_changes_exactly_the_rev_token(tmp_path):
    path = _write(tmp_path, _COMMENTED_CONFIG)
    carrier = cp.PrecommitCarrier(tmp_path)
    target = _hub_target("v9.9.9")
    # the hub entry is identified path-independently (marker hook-id intersection)
    result = carrier.apply(target)
    assert result.changed
    assert _read(path) == _COMMENTED_CONFIG.replace("rev: v1.0.0", "rev: v9.9.9")
    assert carrier.verify(target).ok


def test_append_missing_required_hook_preserves_every_original_line(tmp_path):
    path = _write(tmp_path, _COMMENTED_CONFIG)
    carrier = cp.PrecommitCarrier(tmp_path)
    # required_repos DO append missing hooks (hub_hooks by design only rev-pins
    # an existing entry) — target the config's exact-URL entry with an extra hook.
    target = {
        "config_path": ".pre-commit-config.yaml",
        "required_repos": [
            {
                "repo": "../.dev-knowledge",
                "rev": "v1.0.0",
                "hooks": [{"id": "toc-freshness"}, {"id": "codemap-freshness"}],
            }
        ],
    }
    result = carrier.apply(target)
    assert result.changed
    new_text = _read(path)
    orig_lines = _COMMENTED_CONFIG.splitlines()
    new_lines = new_text.splitlines()
    # every original line survives verbatim, in order (pure insertion)
    it = iter(new_lines)
    assert all(any(line == cand for cand in it) for line in orig_lines), (
        "an original line was altered or dropped"
    )
    assert "- id: codemap-freshness" in new_text
    assert carrier.verify(target).ok


def test_absent_hub_entry_appends_without_touching_existing_bytes(tmp_path):
    config = """\
# header comment
repos:
  - repo: local
    hooks:
      - id: consumers-own
        entry: echo hi
        language: system
"""
    path = _write(tmp_path, config)
    carrier = cp.PrecommitCarrier(tmp_path)
    target = _hub_target("v2.0.0")
    assert carrier.apply(target).changed
    new_text = _read(path)
    # the config ends with the repos block, so the new entry is a pure APPEND:
    # every original byte is an untouched prefix
    assert new_text.startswith(config)
    assert _HUB_REPO in new_text[len(config):]
    assert carrier.verify(target).ok


def test_local_hook_lands_in_commented_local_block(tmp_path):
    path = _write(tmp_path, _COMMENTED_CONFIG)
    carrier = cp.PrecommitCarrier(tmp_path)
    target = _local_hook_target()
    assert carrier.apply(target).changed
    new_text = _read(path)
    for must_survive in (
        "# Consumer header comment -- must survive every deploy",
        "name: Consumer's own hook   # keep me verbatim",
        "# trailing top-level comment",
        "rev: v1.0.0  # deployed pin -- trailing comment must survive a rev bump",
    ):
        assert must_survive in new_text
    assert carrier.verify(target).ok
    # the consumer's own local hook is still there alongside the deployed one
    parsed = yaml.safe_load(new_text)
    local = next(e for e in parsed["repos"] if e.get("repo") == "local")
    ids = [h["id"] for h in local["hooks"]]
    assert ids == ["consumers-own", "floor-hash-verify"]


def test_apply_is_idempotent_on_bytes(tmp_path):
    path = _write(tmp_path, _COMMENTED_CONFIG)
    carrier = cp.PrecommitCarrier(tmp_path)
    target = _hub_target("v9.9.9")
    assert carrier.apply(target).changed
    after_first = path.read_bytes()
    second = carrier.apply(target)
    assert not second.changed
    assert path.read_bytes() == after_first


def test_crlf_config_keeps_crlf_on_untouched_lines(tmp_path):
    path = _write(tmp_path, _COMMENTED_CONFIG, newline="\r\n")
    carrier = cp.PrecommitCarrier(tmp_path)
    target = _hub_target("v9.9.9")
    assert carrier.apply(target).changed
    data = path.read_bytes()
    assert b"# Consumer header comment -- must survive every deploy\r\n" in data
    assert b"rev: v9.9.9  # deployed pin -- trailing comment must survive a rev bump\r\n" in data
    assert carrier.verify(target).ok


# ---------------------------------------------------------------------------
# fallback teeth — the splice refusing must never block convergence
# ---------------------------------------------------------------------------


def test_flow_style_config_falls_back_and_still_converges(tmp_path):
    config = (
        'repos: [{repo: "../.dev-knowledge", rev: v1.0.0, '
        'hooks: [{id: toc-freshness}]}]\n'
    )
    _write(tmp_path, config)
    carrier = cp.PrecommitCarrier(tmp_path)
    target = _hub_target("v9.9.9")
    assert carrier.apply(target).changed
    assert carrier.verify(target).ok  # semantics converge even though comments-preservation is moot


def test_sabotaged_splice_falls_back_and_still_converges(tmp_path, monkeypatch):
    _write(tmp_path, _COMMENTED_CONFIG)
    monkeypatch.setattr(cp, "_surgical_edit", lambda text, ops: None)
    carrier = cp.PrecommitCarrier(tmp_path)
    target = _hub_target("v9.9.9")
    assert carrier.apply(target).changed
    assert carrier.verify(target).ok


# ---------------------------------------------------------------------------
# prune leg
# ---------------------------------------------------------------------------

_RUFF_URL = "https://github.com/astral-sh/ruff-pre-commit"

_PRUNE_CONFIG = """\
# header: consumer prose above everything
repos:
  # comment immediately above the ruff entry -- LEFT IN PLACE on prune (ruling)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.5
    hooks:
      - id: ruff
        name: Ruff lint gate (Tier-1, pinned rev; blocks on violations)
        args: []
  # comment above the consumer's own entry -- must survive the prune
  - repo: local
    hooks:
      - id: consumers-own
        entry: echo hi   # inline note
        language: system

# trailing comment
"""


def _ruff_component() -> dict:
    return {
        "id": "ruff-gate",
        "prune": {
            "match": {"repo": _RUFF_URL},
            "expected": {
                "rev": "v0.15.5",
                "hooks": [
                    {
                        "id": "ruff",
                        "name": "Ruff lint gate (Tier-1, pinned rev; blocks on violations)",
                        "args": [],
                    }
                ],
            },
        },
    }


def test_prune_removes_only_the_matched_entry_lines(tmp_path):
    path = _write(tmp_path, _PRUNE_CONFIG)
    carrier = cp.PrecommitCarrier(tmp_path)
    result = carrier.prune(_ruff_component())
    assert result.pruned
    new_text = _read(path)
    for must_survive in (
        "# header: consumer prose above everything",
        "# comment immediately above the ruff entry -- LEFT IN PLACE on prune (ruling)",
        "# comment above the consumer's own entry -- must survive the prune",
        "entry: echo hi   # inline note",
        "# trailing comment",
    ):
        assert must_survive in new_text
    assert _RUFF_URL not in new_text
    assert carrier.verify_pruned(_ruff_component()).ok


def test_prune_twice_is_a_byte_noop(tmp_path):
    path = _write(tmp_path, _PRUNE_CONFIG)
    carrier = cp.PrecommitCarrier(tmp_path)
    assert carrier.prune(_ruff_component()).pruned
    after_first = path.read_bytes()
    second = carrier.prune(_ruff_component())
    assert not second.pruned
    assert path.read_bytes() == after_first


def test_prune_of_modified_entry_still_refuses_and_writes_nothing(tmp_path):
    edited = _PRUNE_CONFIG.replace("rev: v0.15.5", "rev: v0.16.0")
    path = _write(tmp_path, edited)
    before = path.read_bytes()
    carrier = cp.PrecommitCarrier(tmp_path)
    result = carrier.prune(_ruff_component())
    assert not result.pruned
    assert result.refused
    assert path.read_bytes() == before
