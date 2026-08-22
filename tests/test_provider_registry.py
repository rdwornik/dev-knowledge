"""Tests for the provider/model registry — `ecosystem/provider-registry.yaml`.

The registry is CLOUD-4 v2's answer to the finding in
`docs/audits/2026-08-21-fresh-eyes-cloud-r2-universalization.md` §3.3: `claude-sonnet-5` is
hardcoded in THREE different file formats — a `.md` frontmatter key, a `.js` object literal
and `.md` prose — "with nothing asserting they agree". These tests are that assertion.

Two classes of test here, and the split is the whole design:

* **Derivation** — `scripts/changelog_sentinel.py` (seam S7) now READS the registry, so the
  test asserts the derived table, not a literal.
* **Agreement** — the sites that cannot read YAML at load time are checked by
  `scripts/check_provider_registry.py`. The `live_repo` tests below run that checker against
  the real tree; the tmp-tree tests prove it has TEETH, by breaking each site in a copy and
  requiring a finding. A checker that only ever passes is indistinguishable from one that
  cannot fail, which is the failure mode this file exists to foreclose.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
import yaml

import changelog_sentinel as cs  # noqa: E402
import check_provider_registry as cpr  # noqa: E402
import provider_registry as preg  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parent.parent

_ARTIFACT_READER = ".claude/agents/artifact-reader.md"
_CONFORMANCE_HUB = ".claude/workflows/conformance-hub.js"
_PLAYBOOK = "protocols/PLAYBOOK.md"
_SETTINGS = ".claude/settings.json"
_TOOL_VERSIONS = "ecosystem/tool-versions.yaml"


# --- shape ---------------------------------------------------------------------------------

def test_registry_has_the_two_declared_collections():
    """The tool-versions.yaml shape mirror: two collections, each id -> field map."""
    data = preg.load_registry()
    assert set(data) == {"providers", "models"}
    assert all(isinstance(v, dict) for v in data["providers"].values())
    assert all(isinstance(v, dict) for v in data["models"].values())


def test_every_model_names_a_declared_provider():
    known = set(preg.providers())
    for mid, fields in preg.models().items():
        assert fields.get("provider") in known, f"{mid} names an undeclared provider"


def test_a_registry_that_is_absent_raises_rather_than_defaulting(tmp_path):
    """A missing registry is loud. A loader that silently returned a default would rebuild
    the exact drift the registry exists to end."""
    with pytest.raises(preg.RegistryError):
        preg.load_registry(tmp_path / "nope.yaml")


def test_a_registry_missing_a_collection_raises(tmp_path):
    p = tmp_path / "r.yaml"
    p.write_text("providers: {}\n", encoding="utf-8")
    with pytest.raises(preg.RegistryError):
        preg.load_registry(p)


# --- S7: derivation, not a literal ---------------------------------------------------------

def test_changelog_sentinel_tools_are_derived_from_the_registry():
    """Seam S7. The sentinel's `_TOOLS` is the registry's `version_commands()`, not a copy."""
    assert cs._TOOLS == preg.version_commands()
    assert cs._TOOLS == {"claude-code": ["claude", "--version"],
                         "codex": ["codex", "--version"]}


def test_version_commands_omits_a_provider_with_no_cli(tmp_path):
    """`cli: null` means no probe; an entry with no probe is not a probe."""
    p = tmp_path / "r.yaml"
    p.write_text(yaml.safe_dump({
        "providers": {
            "with": {"version_command": ["x", "--version"], "changelog_tool_key": "x"},
            "without": {"cli": None, "version_command": None},
        },
        "models": {},
    }), encoding="utf-8")
    assert preg.version_commands(p) == {"x": ["x", "--version"]}


# --- live agreement -----------------------------------------------------------------------

@pytest.mark.live_repo
def test_the_live_tree_agrees_with_the_registry():
    assert cpr.run(_REPO_ROOT) == []


@pytest.mark.live_repo
def test_the_three_formats_that_hardcode_the_subagent_model_all_agree():
    """The headline R2 §3.3 assertion, spelled out rather than left to the checker.

    One model string, three file formats, one registry. If any of the three moves alone this
    test names which one — which is the difference between a registry and a comment.
    """
    want = cpr._sole_role_model(cpr._SUBAGENT_DEFAULT_ROLE)

    frontmatter = cpr._FRONTMATTER_MODEL_RE.search(
        (_REPO_ROOT / _ARTIFACT_READER).read_text(encoding="utf-8"))
    assert frontmatter is not None
    assert frontmatter.group(1) == want, "md-frontmatter pin disagrees"

    js_pins = cpr._JS_MODEL_RE.findall((_REPO_ROOT / _CONFORMANCE_HUB).read_text(encoding="utf-8"))
    assert js_pins, "no js object-literal pin found"
    assert set(js_pins) == {want}, "js object-literal pin disagrees"

    assert f"`{want}`" in (_REPO_ROOT / _PLAYBOOK).read_text(encoding="utf-8"), \
        "md-prose tier-binding sentence disagrees"


@pytest.mark.live_repo
def test_the_durable_tool_versions_record_agrees_on_identity():
    """Seam S8. tool-versions.yaml stays the DURABLE last-reviewed record (ADR-80 §3); the
    registry owns the identity half — which tool keys exist and where their changelogs live."""
    tools = (yaml.safe_load((_REPO_ROOT / _TOOL_VERSIONS).read_text(encoding="utf-8")) or {})["tools"]
    assert set(tools) == set(preg.changelog_source_urls())
    for key, url in preg.changelog_source_urls().items():
        assert tools[key]["source_url"] == url


@pytest.mark.live_repo
def test_the_marketplace_host_path_has_one_home():
    """Seam S26 — a hardcoded absolute host path in committed agent config."""
    settings = json.loads((_REPO_ROOT / _SETTINGS).read_text(encoding="utf-8"))
    anthropic = preg.providers()["anthropic"]
    entry = settings["extraKnownMarketplaces"][anthropic["marketplace_id"]]
    assert entry["source"]["path"] == anthropic["marketplace_source_path"]


@pytest.mark.live_repo
def test_provenance_attributions_resolve_to_registered_models():
    """Seams S29/S30 — the cheap class, checked so a provider cannot enter the corpus without
    entering the vocabulary."""
    assert cpr.check_provenance_pins(_REPO_ROOT) == []
    tokens = preg.attribution_tokens()
    assert tokens["grok-l5"] == "grok L5", "the on-disk form is prose, not the id"


# --- teeth ---------------------------------------------------------------------------------

@pytest.fixture
def tree(tmp_path):
    """A minimal copy of the checked surface, so a break can be made without touching the
    live tree."""
    root = tmp_path / "repo"
    for rel in (_ARTIFACT_READER, _CONFORMANCE_HUB, _PLAYBOOK, _SETTINGS, _TOOL_VERSIONS,
                "pyproject.toml", "ecosystem/satellite-onboarding-rulings.yaml"):
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(_REPO_ROOT / rel, dest)
    return root


def _break(root: Path, rel: str, old: str, new: str) -> None:
    p = root / rel
    text = p.read_text(encoding="utf-8")
    assert old in text, f"fixture precondition: {old!r} absent from {rel}"
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def test_checker_is_clean_on_the_unbroken_copy(tree):
    assert cpr.run(tree) == []


def test_a_drifted_frontmatter_pin_is_caught(tree):
    _break(tree, _ARTIFACT_READER, "model: claude-sonnet-5", "model: claude-haiku-4-5")
    findings = cpr.run(tree)
    assert any(f.startswith("S9 ") for f in findings), findings


def test_a_drifted_js_pin_is_caught(tree):
    _break(tree, _CONFORMANCE_HUB, "model: 'claude-sonnet-5'", "model: 'claude-opus-4-8'")
    findings = cpr.run(tree)
    assert any(f.startswith("S10 ") for f in findings), findings


def test_a_DELETED_js_pin_is_caught(tree):
    """A pin that is REMOVED, not mistyped -- the case a findall-and-compare leg misses.

    Deleting one of the three Stage-1 `model:` pins leaves two that still AGREE with the
    registry, so a checker that only compares the pins it finds returns clean while that
    stage silently falls back to the harness default. Found by gpt-5.6-terra against the
    lane diff, 2026-08-22; the artifact's claim that S10 asserts "all three" was not true
    of the code as built.
    """
    _break(tree, _CONFORMANCE_HUB, ", model: 'claude-sonnet-5' }", " }")
    remaining = cpr._JS_MODEL_RE.findall((tree / _CONFORMANCE_HUB).read_text(encoding='utf-8'))
    assert len(remaining) == cpr._CONFORMANCE_HUB_PIN_COUNT - 1, remaining
    assert all(p == 'claude-sonnet-5' for p in remaining), (
        'fixture precondition: every SURVIVING pin must still agree, '
        'or this test would pass for the old reason')
    findings = cpr.run(tree)
    assert any(f.startswith('S10 ') for f in findings), findings


def test_a_drifted_prose_pin_is_caught(tree):
    _break(tree, _PLAYBOOK, "`claude-sonnet-5`", "`claude-sonnet-4-6`")
    findings = cpr.run(tree)
    assert any(f.startswith("S17 ") for f in findings), findings


def test_a_deleted_prose_binding_is_caught_rather_than_passing_quietly(tree):
    """The seam gate's other failure mode: the sentence goes away entirely. A check anchored on
    a bare backtick would go green here, which is the silence R2 §3.3 named."""
    _break(tree, _PLAYBOOK, "tier is Sonnet 5 (`claude-sonnet-5`)", "tier is the platform default")
    findings = cpr.run(tree)
    assert any(f.startswith("S17 ") and "was not found" in f for f in findings), findings


def test_a_body_level_model_line_is_not_mistaken_for_the_frontmatter_pin(tree):
    """The S9 check reads the `---`-delimited block, not the first `model:` anywhere in the
    file — so prose below the frontmatter cannot satisfy or break the pin."""
    p = tree / _ARTIFACT_READER
    p.write_text(p.read_text(encoding="utf-8") + "\nmodel: claude-haiku-4-5\n", encoding="utf-8")
    assert cpr.run(tree) == []


def test_a_drifted_marketplace_path_is_caught(tree):
    _break(tree, _SETTINGS, "Documents", "Documenten")
    findings = cpr.run(tree)
    assert any(f.startswith("S26 ") for f in findings), findings


def test_a_drifted_changelog_source_url_is_caught(tree):
    _break(tree, _TOOL_VERSIONS, "https://github.com/openai/codex/releases",
           "https://example.invalid/codex")
    findings = cpr.run(tree)
    assert any(f.startswith("S8 ") for f in findings), findings


def test_a_dropped_provenance_attribution_is_caught(tree):
    _break(tree, "pyproject.toml", "grok L5", "an unnamed reviewer")
    findings = cpr.run(tree)
    assert any(f.startswith("S30 ") for f in findings), findings


def test_main_exits_1_on_a_violation_and_0_when_clean(tree, capsys):
    assert cpr.main([str(tree)]) == 0
    _break(tree, _ARTIFACT_READER, "model: claude-sonnet-5", "model: claude-haiku-4-5")
    assert cpr.main([str(tree)]) == 1
    assert "registry is the source of truth" in capsys.readouterr().out


def test_an_internal_error_blocks_rather_than_passing(tmp_path, capsys):
    """Exit 2, not 0 — the house posture. An empty directory is not a clean repo."""
    assert cpr.main([str(tmp_path)]) == 2
    assert "INTERNAL ERROR" in capsys.readouterr().err
