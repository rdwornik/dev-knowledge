"""RED-first witnesses for `[#691]`'s role collection — the registry half of the router.

`[#691]`'s frozen Done-when names one test explicitly: *"RED-first test: listing a
non-admitted provider fails."* That sentence needs reading carefully, because taken at face
value it contradicts this lane's own contract, which REQUIRES `agy`, Grok 4.6, Copilot
Enterprise and Codex terra to be listed as NOT ADMITTED entries so the router's refusals can
be trip-tested against real rows.

The two reconcile on a distinction the tests below encode as the central one:

    LISTED is not ELIGIBLE.

A provider may be listed under any admission state, any licence, any allowlist membership —
that is what makes it addressable and trip-testable. What FAILS is any attempt to make a
non-admitted provider ROUTABLE: `admitted` is the only verdict that does that, and the schema
refuses to grant it without provenance, without a permitting licence, or against a model row
that records the same role refused.

So "listing a non-admitted provider fails" is enforced as "ADMITTING one fails", which is the
reading that leaves the clause with teeth instead of leaving it in conflict with the lane it
governs.

THE THREE LEGS `[#691]` NAMES, each with its own section below:
  (a) ORDER      — `test_order_*`
  (b) ADMISSION  — `test_admission_*`  (the Done-when's named RED-first test)
  (c) LICENCE    — `test_licence_*`    (the leg the row measured as absent entirely)
"""
from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from ecosystem.schema.provider_registry import (  # noqa: E402
    ROLE_NAMES,
    ProviderRegistry,
)

_REGISTRY_PATH = _ROOT / "ecosystem" / "provider-registry.yaml"
_ROUTING_TABLE_PATH = _ROOT / "ecosystem" / "routing-table.yaml"
_MANIFEST_PATH = _ROOT / "deploy" / "manifest-v1.5.0.yaml"


@pytest.fixture(scope="module")
def live() -> dict:
    return yaml.safe_load(_REGISTRY_PATH.read_text(encoding="utf-8"))


def _mutated(live: dict, mutate) -> dict:
    """A deep copy of the live registry with one thing changed — so every refusal below is
    demonstrated against the REAL file rather than against a minimal fixture that might not
    resemble it."""
    data = copy.deepcopy(live)
    mutate(data)
    return data


def _refuses(data: dict) -> str:
    with pytest.raises(Exception) as exc:
        ProviderRegistry.model_validate(data)
    return str(exc.value)


# --- the vocabulary has two homes and one checker ------------------------------------------


def test_the_role_vocabulary_agrees_with_the_telemetry_emitters_copy():
    """`ROLE_NAMES` and `cost_usage_telemetry.ROLES` must be equal.

    The duplication is unavoidable and is justified where each copy lives: the emitter is a
    leaf module with a deliberately thin import surface and must not pull in pydantic to
    validate one string, while this schema is models-only (Layer-2) and must not import a
    script. This repo's standing answer to a value with two unavoidable homes is a CHECKER,
    not an import — the same mechanism `check_provider_registry` already is for the frontmatter
    and JS-literal seams. This test is that checker.
    """
    spec = importlib.util.spec_from_file_location(
        "cost_usage_telemetry", _ROOT / "scripts" / "cost_usage_telemetry.py"
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["cost_usage_telemetry"] = mod
    spec.loader.exec_module(mod)
    assert mod.ROLES == ROLE_NAMES


def test_the_live_registry_validates_and_carries_all_six_roles(live):
    registry = ProviderRegistry.model_validate(live)
    assert set(registry.roles) == ROLE_NAMES


def test_an_invented_role_name_is_refused(live):
    message = _refuses(_mutated(live, lambda d: d["roles"].update({"summarise": d["roles"]["verify"]})))
    assert "summarise" in message


# --- leg (a): ORDER -------------------------------------------------------------------------


def test_order_is_a_list_not_a_set_so_position_is_meaningful(live):
    """The defect `[#691]` was filed against, stated as a property.

    The row: *"today's `roles:` is a set, and a set cannot express a fallback chain."* The
    per-model `roles:` membership list still exists and still answers its own question; what
    this asserts is that the NEW collection answers the other one — who is first, and who
    answers when the first is ineligible.
    """
    registry = ProviderRegistry.model_validate(live)
    implement = [e.provider for e in registry.roles["implement"].order]
    assert implement[0] == "anthropic", "AX22-1: implement order until admission is Sonnet first"
    assert len(implement) > 1, "a fallback chain needs somewhere to fall back to"


def test_order_refuses_an_empty_list(live):
    def mutate(d):
        d["roles"]["verify"]["order"] = []

    assert "empty" in _refuses(_mutated(live, mutate))


def test_order_refuses_a_provider_holding_two_positions(live):
    """A fallback list is a RANKING. A provider at two positions has no defined rank once the
    re-rank reorders it, so the ambiguity is refused at load rather than resolved arbitrarily
    at route time."""
    def mutate(d):
        d["roles"]["implement"]["order"].append({"provider": "anthropic"})

    assert "twice" in _refuses(_mutated(live, mutate))


def test_order_refuses_an_undeclared_provider(live):
    def mutate(d):
        d["roles"]["implement"]["order"].append({"provider": "mistral"})

    assert "mistral" in _refuses(_mutated(live, mutate))


def test_order_refuses_a_model_pin_that_crosses_providers(live):
    """A pin whose model belongs to a different vendor makes the allowlist check and the
    admission check disagree about which vendor is being routed to — one keys on `provider`,
    the other resolves through the model row."""
    def mutate(d):
        d["roles"]["implement"]["order"][0]["model"] = "gpt-5.6-terra"

    message = _refuses(_mutated(live, mutate))
    assert "openai" in message and "anthropic" in message


# --- leg (b): ADMISSION — the Done-when's named RED-first test -------------------------------


def test_admission_every_non_claude_entry_is_recorded_not_admitted(live):
    """THE HALF A / HALF B BOUNDARY, asserted as a property of the shipped file.

    AX23-2 splits this arc: Half A builds the mechanism with no non-Claude provider ordered
    through AX22-1's >= 8-of-10 MEASUREMENT; Half B is where that measurement happens. This
    test is what makes that split checkable rather than merely stated — if a later edit
    quietly admits one of these ON THE STRENGTH OF A DECLARED (unmeasured) ranking, this goes
    RED, and the admission would be exactly what AX21-2 and AX22-1 forbid.

    `copilot-enterprise` is the DOCUMENTED EXCEPTION, added 2026-09-23 (`lane-provider-
    registry`, operator ruling O-3): its `implement` admission is NOT an AX22-1 measurement —
    it is an operator ruling on IN-REPO evidence of prior real production
    (`docs/audits/2026-09-23-technical-copilot-admission-evidence.md`) — but it is still an
    ADMITTED verdict in the `roles:` collection, so this test's set must carry it or the
    property it asserts (which providers hold an admitted verdict anywhere) would be false.
    Reporting an admission state is not the same act as measuring one, on either provider.
    """
    registry = ProviderRegistry.model_validate(live)
    admitted_providers = {
        entry.provider
        for role in registry.roles.values()
        for entry in role.order
        if entry.admission is not None and entry.admission.verdict == "admitted"
    }
    assert admitted_providers == {"anthropic", "copilot-enterprise"}


def test_admission_the_four_trip_test_targets_are_all_present_and_not_admitted(live):
    """The lane contract requires exactly these to be LISTED so the router's refusals have real
    rows to bite on. Presence and non-admission are asserted together, because either alone is
    the wrong state: absent, and the refusal is untestable; admitted, and Half A has silently
    done Half B's job.

    `copilot-enterprise` moved out of this set 2026-09-23 (operator ruling O-3) — it is now
    ADMITTED on `implement` (see the test above), so it no longer belongs among the NOT ADMITTED
    trip-test targets. It is asserted separately, right below, on its remaining role (`read`),
    where it is still NOT ADMITTED and still trip-tests the router's refusal there.
    """
    registry = ProviderRegistry.model_validate(live)
    listed: dict[str, bool] = {}
    for role in registry.roles.values():
        for entry in role.order:
            admitted = entry.admission is not None and entry.admission.verdict == "admitted"
            listed[entry.provider] = listed.get(entry.provider, False) or admitted
    for provider in ("antigravity", "xai", "openai"):
        assert provider in listed, f"{provider} must be LISTED for the router refusal to be trip-testable"
        assert listed[provider] is False, f"{provider} is NOT ADMITTED in Half A"


def test_admission_copilot_enterprise_is_admitted_on_implement_not_elsewhere(live):
    """The 2026-09-23 exception, pinned precisely: `copilot-enterprise` is ADMITTED on
    `implement` (operator ruling O-3) and remains NOT ADMITTED on every other role it appears
    in (`read`) — the ruling is scoped to the role the in-repo evidence actually demonstrates
    (two production lanes), not a blanket admission across the registry."""
    registry = ProviderRegistry.model_validate(live)
    by_role: dict[str, bool] = {}
    for role_name, role in registry.roles.items():
        for entry in role.order:
            if entry.provider != "copilot-enterprise":
                continue
            by_role[role_name] = entry.admission is not None and entry.admission.verdict == "admitted"
    assert by_role.get("implement") is True
    assert by_role.get("read") is False


def test_admission_refuses_a_verdict_with_no_provenance(live):
    """A bare `admitted:` is an assertion. Reuses `RoleAdmission`'s existing rule rather than
    restating it — which is the point of having reused the model."""
    def mutate(d):
        d["roles"]["implement"]["order"][1]["admission"] = {"verdict": "admitted"}

    assert "provenance" in _refuses(_mutated(live, mutate))


def test_admission_refuses_admitting_a_model_its_own_row_records_refused(live):
    """One fact must not have two answers depending on which collection the reader opened.

    grok-4.6's model row records a REFUSED `fan-out` verdict. Admitting `fan-out` for it in the
    role collection would make `models:` and `roles:` contradict each other, and a consumer
    would get whichever answer its accessor happened to reach for.
    """
    def mutate(d):
        d["providers"]["xai"]["licence"] = {
            "status": "permitted", "reason": "test", "decided_by": "t", "decided_on": "2026-09-12",
        }
        d["roles"]["read"] = {
            "description": "fixture",
            "order": [{
                "provider": "xai",
                "model": "grok-4.6",
                "admission": {
                    "verdict": "admitted", "decided_by": "t", "decided_on": "2026-09-12",
                    "evidence": "docs/audits/x.md",
                },
            }],
        }
        d["models"]["grok-4.6"]["role_admission"]["read"] = d["models"]["grok-4.6"]["role_admission"]["fan-out"]

    message = _refuses(_mutated(live, mutate))
    assert "refused" in message


def test_admission_absent_block_means_not_admitted_not_unknown(live):
    """Silence is never permission. An entry with no `admission:` at all is NOT ADMITTED, and
    the loader's predicate must agree with the schema's default rather than treating a missing
    block as an open question the router might resolve optimistically."""
    spec = importlib.util.spec_from_file_location(
        "provider_registry_mod", _ROOT / "scripts" / "provider_registry.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.is_admitted({}) is False
    assert mod.is_admitted({"admission": {"verdict": "unevaluated"}}) is False
    assert mod.is_admitted({"admission": {"verdict": "refused"}}) is False
    assert mod.is_admitted({"admission": {"verdict": "admitted"}}) is True


# --- leg (c): LICENCE — the leg the row measured as absent entirely --------------------------


def test_licence_every_provider_now_carries_one(live):
    """`[#691]` leg (c): *"the registry has no licence or terms field at all (grepped: zero hits
    for licence/license/terms)."* It does now, on every provider row."""
    registry = ProviderRegistry.model_validate(live)
    for pid in registry.providers:
        assert registry.providers[pid].licence is not None, f"{pid} carries no licence block"


def test_licence_an_absent_block_reads_as_unknown_never_permitted(live):
    """The default must be the conservative one: the field's absence must not grant what its
    presence was added to withhold."""
    def mutate(d):
        del d["providers"]["xai"]["licence"]

    registry = ProviderRegistry.model_validate(_mutated(live, mutate))
    assert registry.licence_of("xai") == "unknown"


def test_licence_the_employer_metered_seat_was_ruled_2026_09_23(live):
    """The one genuinely OPEN licence on this surface, and the row that made the field worth
    adding. copilot-enterprise is metered to the BY-Product-Development enterprise org seat;
    whether that may be spent on this repository was a FUNCTIONAL question and therefore the
    operator's under ADR-108 §A. `lane-x-691-routing-half-a` recorded the state and stopped —
    `unknown` was a first-class verdict there, neither a soft refusal nor a soft permission.

    RULED 2026-09-23 (operator O-3, `RATIFICATION-2026-09-23-copilot.md`; in-repo evidence at
    `docs/audits/2026-09-23-technical-copilot-admission-evidence.md`): `permitted`, repo-wide —
    a licence ruling is a property of the PROVIDER, not of one role, so it is not scoped to
    `implement` even though the evidence that prompted it is an `implement`-role admission.
    """
    registry = ProviderRegistry.model_validate(live)
    assert registry.licence_of("copilot-enterprise") == "permitted"


def test_licence_refuses_admitting_a_provider_whose_licence_does_not_permit(live):
    """THE LEG (c) REFUSAL. `[#691]`'s Done-when: only providers *"whose licence permits the
    use"* may be routable. Enforced on ADMISSION rather than on LISTING — see this module's
    docstring for why that is the reading with teeth.

    Fixture-based since 2026-09-23: `order[1]` on `implement` (copilot-enterprise) carries a
    `permitted` licence now (operator ruling O-3), so admitting it no longer trips this refusal
    on its own — the mutation below gives `xai` (already `order[2]`) a non-permitting licence
    instead, restricted rather than unknown, to also cover the RULED (not just the unruled) half
    of the vocabulary."""
    def mutate(d):
        d["providers"]["xai"]["licence"] = {
            "status": "restricted", "reason": "fixture", "decided_by": "t",
            "decided_on": "2026-09-23",
        }
        d["roles"]["implement"]["order"][2]["admission"] = {
            "verdict": "admitted", "decided_by": "t", "decided_on": "2026-09-12",
            "evidence": "docs/audits/x.md",
        }

    message = _refuses(_mutated(live, mutate))
    assert "licence" in message and "restricted" in message


def test_licence_refuses_a_decided_status_with_no_decider(live):
    """Symmetric with `RoleAdmission`: a ruling without a decider and a date is an assertion.
    `unknown` is exempt, because demanding a decider for "nobody decided" would make the honest
    state unexpressible and push every unruled provider into a fabricated `permitted`."""
    def mutate(d):
        d["providers"]["xai"]["licence"] = {"status": "permitted", "reason": "because"}

    assert "decided_by" in _refuses(_mutated(live, mutate))


def test_licence_unknown_needs_no_decider_but_still_needs_a_reason(live):
    """The exemption is scoped to provenance, not to the reason. An `unknown` with no stated
    open question teaches the next reader nothing and is the drift the field exists to end."""
    def mutate(d):
        d["providers"]["xai"]["licence"] = {"status": "unknown", "reason": "the open question"}

    ProviderRegistry.model_validate(_mutated(live, mutate))  # valid

    def mutate_bad(d):
        d["providers"]["xai"]["licence"] = {"status": "unknown"}

    assert "reason" in _refuses(_mutated(live, mutate_bad))


# --- AX22-2: the exclusion is ENCODED in the registry ---------------------------------------


def test_the_review_role_encodes_the_reviewer_is_not_the_producer_exclusion(live):
    """AX22-2 verbatim: *"The registry encodes the exclusion; the tally records both roles."*
    This is the registry half. The router enforces it before dispatch
    (`test_provider_router.py`) and the tally catches it after the fact
    (`test_routing_telemetry.py`) — three legs, because a rule with one leg is a convention."""
    registry = ProviderRegistry.model_validate(live)
    assert registry.roles["review"].excludes_producer is True
    others = {r: s.excludes_producer for r, s in registry.roles.items() if r != "review"}
    assert not any(others.values()), f"the exclusion belongs to review alone, got {others}"


def test_the_review_fallback_order_is_ax22_2s_own(live):
    """AX22-2: *"Codex terra reviews unless Codex produced; then the reviewer is Grok (after
    admission) or Sonnet."* Encoded in that order, with Grok NOT admitted — so today the
    exclusion resolves to Sonnet, which is the only live fallback."""
    registry = ProviderRegistry.model_validate(live)
    assert [e.provider for e in registry.roles["review"].order] == ["openai", "xai", "anthropic"]


# --- AX21-1's one non-re-rankable line -------------------------------------------------------


def test_orchestrate_and_plan_are_pinned_against_the_re_rank(live):
    """This lane's contract: *"orchestration never routes to a cheaper tier, which is the one
    line of the role table that is not subject to re-ranking."*

    A cheap model scoring well on pass-rate-per-cost must not be promoted into the seat that
    decides what the expensive ones do — the promotion would be the metric's artefact, not its
    finding. Asserted on exactly two roles, so a later edit cannot quietly pin a third and
    disable the re-rank by attrition.
    """
    registry = ProviderRegistry.model_validate(live)
    pinned = {r for r, s in registry.roles.items() if not s.rerankable}
    assert pinned == {"orchestrate", "plan"}


# --- the two role-keyed surfaces must not drift ---------------------------------------------


def test_declared_routing_table_links_agree_with_routing_table_yaml(live):
    """`ecosystem/routing-table.yaml` is the AUTHORITY for role -> CLI (register ruling Z-G3
    amendment A2). This collection is a RANKING, not a rival authority — and the thing that
    keeps it from becoming one is this check.

    Where a role declares `routing_table_role:`, the CLI that table names must be reachable
    through one of this role's listed providers. A `null` link asserts nothing, which is the
    honest state where no correspondence exists: writing a lossy mapping to fill the field
    would manufacture exactly the drift the link exists to detect.
    """
    registry = ProviderRegistry.model_validate(live)
    table = yaml.safe_load(_ROUTING_TABLE_PATH.read_text(encoding="utf-8"))["roles"]
    clis = {pid: p.cli for pid, p in registry.providers.items()}

    linked = {r: s.routing_table_role for r, s in registry.roles.items() if s.routing_table_role}
    assert linked, "at least one link must be declared or this check is vacuous"

    for role, table_role in linked.items():
        assert table_role in table, f"role `{role}` links to absent routing-table role `{table_role}`"
        table_cli = table[table_role].get("cli")
        expected = {table_cli} if isinstance(table_cli, str) else set(table_cli or ())
        reachable = {clis.get(e.provider) for e in registry.roles[role].order}
        # `claude-code` is the routing table's name for the Claude runtime; the registry's
        # `anthropic` row names the CLI `claude`. One vendor, two spellings of its entry point.
        reachable |= {"claude-code"} if "claude" in reachable else set()
        assert expected & reachable, (
            f"role `{role}` links to routing-table role `{table_role}` (cli {sorted(expected)}) "
            f"but none of its providers reach that CLI (reachable: {sorted(c for c in reachable if c)})"
        )


# --- AX22-5: the per-repo allowlist in the deploy manifest ----------------------------------


@pytest.fixture(scope="module")
def manifest() -> dict:
    return yaml.safe_load(_MANIFEST_PATH.read_text(encoding="utf-8"))


def test_the_manifest_carries_providers_allowed_per_consumer(manifest):
    """AX22-5 verbatim: *"The deploy manifest carries `providers.allowed` per consumer."*"""
    assert "providers" in manifest
    assert "allowed" in manifest["providers"]
    assert manifest["providers"]["allowed"], "an empty allowlist map refuses every route"


def test_the_allowlist_keys_are_exactly_the_declared_fleet(manifest):
    """Keyed by the ADR-104 fleet ids `ecosystem/parity-surfaces.yaml` declares, so the two
    roster surfaces cannot silently disagree about who is in the fleet — the failure mode where
    a repo onboards on one surface and inherits `default:` on the other without anyone seeing
    it."""
    fleet = set(yaml.safe_load(
        (_ROOT / "ecosystem" / "parity-surfaces.yaml").read_text(encoding="utf-8"))["fleet"])
    assert set(manifest["providers"]["allowed"]) == fleet


def test_every_allowlisted_provider_is_a_registered_provider(manifest, live):
    """An allowlist naming a provider the registry does not declare would refuse silently: the
    router would never match it, and the list would read as permission while granting none."""
    known = set(live["providers"])
    for repo, allowed in manifest["providers"]["allowed"].items():
        unknown = set(allowed) - known
        assert not unknown, f"{repo} allows unregistered provider(s) {sorted(unknown)}"
    assert not set(manifest["providers"]["default"]) - known


def test_the_default_is_the_most_restrictive_entry(manifest):
    """An unlisted repo is one nobody has ruled on. A permissive default would make "not yet
    considered" indistinguishable from "cleared", which is the same present-but-unread defect
    the licence field's `unknown` exists to prevent."""
    default = set(manifest["providers"]["default"])
    assert default == {"anthropic"}
    for repo, allowed in manifest["providers"]["allowed"].items():
        assert default <= set(allowed), f"{repo} allows less than the default, which cannot be right"


def test_a_work_repository_excludes_the_paid_third_party_route(manifest):
    """AX22-5's own carve-out: *"work repositories may exclude paid third-party APIs."*
    `corp-monorepo` excludes `xai` (pay-per-call on the operator's PERSONAL credential) and
    `copilot-enterprise` (metered to the employer org seat). The two exclusions point in
    opposite directions and both are deliberate. `copilot-enterprise`'s licence was RULED
    `permitted` for THIS repo 2026-09-23 (operator O-3) — that ruling is about spending the
    BY-Product-Development seat on `.dev-knowledge`'s own work, and does not itself extend to
    `corp-monorepo`; the manifest's per-repo allowlist, not the registry's per-provider licence,
    is what would have to change to admit it there, and nothing has ruled that yet."""
    allowed = set(manifest["providers"]["allowed"]["corp-monorepo"])
    assert "xai" not in allowed
    assert "copilot-enterprise" not in allowed
