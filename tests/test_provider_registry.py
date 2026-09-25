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
import re
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

def test_registry_has_the_three_declared_collections_and_the_rate_card():
    """The tool-versions.yaml shape mirror: THREE collections plus ONE card.

    WAS `== {"providers", "models"}` until `[#691]` (2026-09-12). The row that changed it is
    explicit that the third collection is not a rename of anything: *"today's `roles:` is a per-
    MODEL list ... a role entry is a third thing, not a field rename."* `providers:` and
    `models:` are unchanged and still answer their own questions; `roles:` answers "who answers
    for this role, in what order".

    `rate_card:` ARRIVED WITH `[#751]` (2026-09-14) AND IS DELIBERATELY NOT A FOURTH COLLECTION.
    Every collection here is an `id -> field map`; the card is ONE mapping of units, provenance
    and multipliers for the whole file. Per-model prices live on the model rows, where a price
    belongs, so adding a model cannot leave its price in a second place to be forgotten — which
    is why the collection assertions below still name three and the card is asserted apart from
    them rather than folded in.

    The equality is kept rather than relaxed to a superset — an exact set is what makes a new
    top-level key arriving unannounced a RED instead of silently inert data, which is the same
    posture `extra="forbid"` takes one level down. This test REDdened on `rate_card`'s arrival
    exactly as designed; updating it is the announcement.
    """
    data = preg.load_registry()
    assert set(data) == {"providers", "models", "roles", "rate_card"}
    assert all(isinstance(v, dict) for v in data["providers"].values())
    assert all(isinstance(v, dict) for v in data["models"].values())
    assert all(isinstance(v, dict) for v in data["roles"].values())
    assert isinstance(data["rate_card"], dict)


def test_a_price_is_never_a_bare_number_without_its_card(tmp_path):
    """`[#751]`: currency, unit and the date a price was true on live on the card, so a model
    row carrying `rates:` while the file carries no `rate_card:` is refused at load.

    The witness strips the card from a copy of the LIVE registry rather than from a fixture, so
    it also fails if the real file ever stops pricing anything at all — which is the condition
    under which this invariant would quietly become vacuous.
    """
    import copy

    import yaml

    data = copy.deepcopy(preg.load_registry())
    assert any(m.get("rates") for m in data["models"].values()), (
        "no model in the live registry declares `rates:` — this invariant has nothing to guard")
    del data["rate_card"]
    broken = tmp_path / "no-card.yaml"
    broken.write_text(yaml.safe_dump(data), encoding="utf-8", newline="\n")
    with pytest.raises(preg.RegistryError) as exc:
        preg.load_registry(broken)
    assert "rate_card" in str(exc.value)


def test_every_declared_rate_resolves_with_its_units_and_its_date():
    """Every priced model in the LIVE registry resolves to a complete, positive rate.

    The point is the ABSENT-vs-ZERO boundary this lane's whole design rests on: a model in
    `priced_models()` must produce four positive numbers with a currency and an `as_of`, and a
    model outside that set must REFUSE by name. Neither may silently return zero.
    """
    priced = preg.priced_models()
    assert priced, "the live registry prices nothing — every cost report is vacuous"
    for model in priced:
        rate = preg.resolve_rate(model)
        assert rate.currency and rate.as_of
        assert min(rate.input, rate.output, rate.cache_write, rate.cache_read) > 0
    for model in set(preg.model_ids()) - set(priced):
        with pytest.raises(preg.RateUnavailable) as exc:
            preg.resolve_rate(model)
        assert model in str(exc.value)


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
    assert preg.version_commands() == cs._TOOLS
    assert cs._TOOLS == {"claude-code": ["claude", "--version"],
                         "codex": ["codex", "--version"]}


def test_version_commands_omits_a_provider_with_no_cli(tmp_path):
    """`cli: null` means no probe; an entry with no probe is not a probe.

    The fixture gained `display_name`, an explicit `cli:` and the `changelog_source_url`
    half of the S8 pair when LANE L1 declared the schema (2026-08-23). The assertion is
    untouched — what changed is that the old fixture was not a LEGAL registry: it carried a
    `version_command` with no `cli`, and a `changelog_tool_key` with no source url. Both are
    now refused by `ecosystem/schema/provider_registry.py`, so this edit is the schema
    demonstrating itself rather than the test being relaxed to fit.
    """
    p = tmp_path / "r.yaml"
    p.write_text(yaml.safe_dump({
        "providers": {
            "with": {
                "display_name": "With", "cli": "x", "version_command": ["x", "--version"],
                "changelog_tool_key": "x",
                "changelog_source_url": "https://example.invalid/x",
            },
            "without": {"display_name": "Without", "cli": None, "version_command": None},
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
                "pyproject.toml", "ecosystem/satellite-onboarding-rulings.yaml",
                # S31's roster site, and every artifact a live `role_admission` verdict
                # cites — both joined the copied surface with LANE L1 (2026-08-23). The
                # evidence set is DERIVED from the registry rather than typed, so a new
                # verdict cannot silently leave this fixture behind.
                "protocols/AI_COUNCIL_PROCESS.md",
                *sorted({str(r["evidence"]) for r in preg.role_admissions().values()
                         if r.get("evidence")})):
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


# --- S31: the council roster reads the rows LANE L1 added ----------------------------------

@pytest.mark.live_repo
def test_every_council_provider_resolves_to_a_registry_entry():
    """The live assertion, and the one the lane exists to make true.

    Before 2026-08-23 the roster named five providers and the registry declared three; this
    passing is the measurement that `gemini` and `deepseek` now resolve.
    """
    assert cpr.check_s31_council_panel(_REPO_ROOT) == []
    aliases = preg.council_aliases()
    assert aliases == {"claude": "anthropic", "gemini": "google", "openai": "openai",
                       "deepseek": "deepseek", "grok": "xai"}


def test_a_council_provider_absent_from_the_registry_is_caught(tree):
    """roster -> registry: the direction that was FAILING before this lane ran."""
    _break(tree, "protocols/AI_COUNCIL_PROCESS.md",
           "`claude,gemini,openai,deepseek,grok`", "`claude,gemini,openai,deepseek,grok,mistral`")
    findings = cpr.run(tree)
    assert any(f.startswith("S31 ") and "mistral" in f for f in findings), findings


def test_a_registry_alias_the_roster_no_longer_names_is_caught(tree):
    """registry -> roster: a stale registry claim, whose fix is `council_alias: null`."""
    _break(tree, "protocols/AI_COUNCIL_PROCESS.md",
           "`claude,gemini,openai,deepseek,grok`", "`claude,openai,grok`")
    findings = cpr.run(tree)
    assert any(f.startswith("S31 ") and "deepseek" in f for f in findings), findings
    assert any(f.startswith("S31 ") and "gemini" in f for f in findings), findings


def test_a_reworded_roster_row_fails_loud_rather_than_passing_quietly(tree):
    """The anchored-regex posture: a seam that cannot find its site says so."""
    _break(tree, "protocols/AI_COUNCIL_PROCESS.md", "| `models`", "| `panel-members`")
    findings = cpr.run(tree)
    assert any("roster row" in f and f.startswith("S31 ") for f in findings), findings


# --- role_admission evidence resolves -------------------------------------------------------

@pytest.mark.live_repo
def test_every_recorded_admission_verdict_cites_an_artifact_that_exists():
    assert cpr.check_role_admission_evidence(_REPO_ROOT) == []
    admissions = preg.role_admissions()
    assert admissions, "precondition: the registry carries at least one verdict to check"


def test_a_decoy_roster_row_is_reported_rather_than_silently_preferred(tree):
    """terra HIGH, 2026-08-23: `search()` takes match #1, so a decoy row above the real one
    would be validated while the live roster drifts. Two matches is now ambiguity, reported."""
    p = tree / "protocols/AI_COUNCIL_PROCESS.md"
    text = p.read_text(encoding="utf-8")
    decoy = "| `models`         | `claude,gemini,openai,deepseek,grok`     | decoy |\n"
    p.write_text(decoy + text.replace("`claude,gemini,openai,deepseek,grok`",
                                      "`claude,gemini,openai,deepseek,mistral`", 1),
                 encoding="utf-8")
    findings = cpr.run(tree)
    assert any(f.startswith("S31 ") and "ambiguous" in f for f in findings), findings


def test_an_empty_roster_token_is_reported_rather_than_dropped(tree):
    _break(tree, "protocols/AI_COUNCIL_PROCESS.md",
           "`claude,gemini,openai,deepseek,grok`", "`claude,,gemini,openai,deepseek,grok`")
    findings = cpr.run(tree)
    assert any(f.startswith("S31 ") and "empty token" in f for f in findings), findings


def test_a_duplicated_roster_token_is_reported(tree):
    _break(tree, "protocols/AI_COUNCIL_PROCESS.md",
           "`claude,gemini,openai,deepseek,grok`", "`claude,gemini,openai,deepseek,grok,grok`")
    findings = cpr.run(tree)
    assert any(f.startswith("S31 ") and "more than once" in f for f in findings), findings


def test_a_roster_row_inside_a_fenced_block_is_not_the_live_roster(tree):
    """terra HIGH round 2, 2026-08-23: a fenced EXAMPLE row would otherwise be read as
    authoritative while the real row drifted. Uses the N-1 CommonMark fence instrument."""
    p = tree / "protocols/AI_COUNCIL_PROCESS.md"
    text = p.read_text(encoding="utf-8")
    fenced = ("```\n| `models`         | `claude,gemini,openai,deepseek,grok`     | ex |\n```\n")
    p.write_text(fenced + text.replace("`claude,gemini,openai,deepseek,grok`",
                                       "`claude,gemini,openai,deepseek,mistral`", 1),
                 encoding="utf-8")
    findings = cpr.run(tree)
    # The fenced row is ignored, so the LIVE row is the one read — and it names `mistral`.
    assert any(f.startswith("S31 ") and "mistral" in f for f in findings), findings
    assert not any("ambiguous" in f for f in findings), findings


def test_a_vertical_tab_cannot_desync_the_fence_mask(tree):
    """terra MEDIUM round 3, 2026-08-23 — and the same defect class terra raised as HIGH
    against `audit.py` on 2026-08-13. `str.splitlines()` breaks on \\x0b, which CommonMark
    does not treat as a line boundary, so every index after it shifts and a fenced roster row
    escapes the mask. Splitting with the generator's own `_EOL_RE` is what keeps them aligned."""
    p = tree / "protocols/AI_COUNCIL_PROCESS.md"
    drifted = p.read_text(encoding="utf-8").replace(
        "`claude,gemini,openai,deepseek,grok`", "`claude,gemini,openai,deepseek,mistral`", 1)
    # The trigger is specific and was verified before being asserted: TWO \x0b before an
    # UNTERMINATED trailing fence. A terminated fence is NOT a reproducer — the off-by-two
    # still lands inside a 3-line masked span, so the leak does not surface.
    poison = ("\n\x0b\x0b\n```\n"
              "| `models`         | `claude,gemini,openai,deepseek,grok`     | ex |\n")
    p.write_text(drifted + poison, encoding="utf-8")
    findings = cpr.run(tree)
    # Aligned: the fenced row stays masked, so the LIVE (drifted) row is the one S31 reads.
    # Desynced: the fenced row leaks, S31 sees TWO rows and reports ambiguity instead.
    assert any(f.startswith("S31 ") and "mistral" in f for f in findings), findings
    assert not any("ambiguous" in f for f in findings), findings


def test_the_agreement_hook_fires_on_its_own_implementation(tree):
    """terra HIGH round 3, 2026-08-23: a gate whose `files:` pattern excludes its own source
    can be disarmed by a commit that touches nothing else. Asserted against the committed
    pattern rather than against prose."""
    cfg = yaml.safe_load((_REPO_ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    hooks = [h for repo in cfg["repos"] for h in repo.get("hooks", [])
             if h.get("id") == "provider-registry-agreement"]
    assert len(hooks) == 1, hooks
    pattern = re.compile(hooks[0]["files"])
    for rel in ("scripts/check_provider_registry.py", "scripts/provider_registry.py",
                "ecosystem/schema/provider_registry.py",
                # terra round 4: the selector itself, and the fence instrument S31 imports.
                # Narrowing the selector, or neutering `_code_line_indices`, each disarms the
                # gate in a commit the gate would otherwise never see.
                ".pre-commit-config.yaml", "scripts/toc/generator.py",
                "ecosystem/provider-registry.yaml", "protocols/AI_COUNCIL_PROCESS.md"):
        assert pattern.search(rel), f"hook would not fire on {rel}"
    # ...and it stays a selector, not a catch-all.
    for rel in ("README.md", "scripts/audit.py", "docs/audits/x.md", "tests/test_audit.py"):
        assert not pattern.search(rel), f"hook over-matches {rel}"
    # terra CRITICAL round 5: the pattern DOCUMENTS the coupled surface; `always_run` is what
    # guarantees the hook runs, because a commit narrowing this selector is evaluated against
    # the narrowed selector and would otherwise skip the gate that should have refused it.
    assert hooks[0].get("always_run") is True, hooks[0]
    assert hooks[0].get("pass_filenames") is False, hooks[0]


@pytest.mark.parametrize("target", [".", "docs", "docs/audits"])
def test_evidence_naming_a_directory_is_caught(tree, monkeypatch, target):
    """terra HIGH round 2, 2026-08-23: a directory resolves in-tree and `.exists()`, while
    citing no measurement at all. The registry is read from THIS repo by contract, so the
    record is injected at the accessor rather than by writing a second registry file."""
    (tree / "docs" / "audits").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(cpr._preg, "role_admissions", lambda *a, **k: {
        ("m", "fan-out"): {"verdict": "refused", "decided_by": "architect",
                           "decided_on": "2026-08-23", "evidence": target},
    })
    findings = cpr.check_role_admission_evidence(tree)
    assert any("is not a file" in f for f in findings), findings


def test_a_verdict_citing_a_missing_artifact_is_caught(tree):
    for rel in {str(r["evidence"]) for r in preg.role_admissions().values() if r.get("evidence")}:
        (tree / rel).unlink()
    findings = cpr.run(tree)
    assert any(f.startswith("role_admission ") for f in findings), findings
