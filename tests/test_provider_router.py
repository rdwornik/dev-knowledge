"""RED-first trip-tests for `scripts/provider_router.py` — `[#691]` step 4.

THE TWO REFUSALS THE DONE-CONTRACT NAMES, quoted so the scoping is not re-derived later:

    "The router REFUSES a provider not on the repo's list and REFUSES a non-admitted
     provider in the implement role — a RED-first trip-test for each refusal."

Read the scoping exactly. The allowlist refusal is universal; the ADMISSION refusal is
scoped to ONE role. That asymmetry is not an oversight and the tests below pin it in both
directions, because it is the clause that lets Codex terra stay the fleet's routable reviewer
while being recorded NOT ADMITTED — a pair of facts that reads like a contradiction until the
scoping is what resolves it.

TRIP-TESTED AGAINST REAL ROWS, NOT FIXTURES. The lane contract requires `agy`, Grok 4.6,
Copilot Enterprise and Codex terra to be LISTED in the registry as NOT ADMITTED entries
precisely so these refusals bite on shipped data. Where a test below could have used a
hand-built fixture it uses the live registry instead; the fixtures that do appear are for the
cases the live file deliberately does not contain (an admitted-but-off-allowlist provider, for
instance, which the shipped data has no example of and should not).

NO CALL IS PLACED BY ANY TEST HERE. The router resolves and refuses; it does not dispatch.
That is what makes the whole of step 4 executable inside Half A's Claude-only boundary.
"""
from __future__ import annotations

import copy
import importlib.util
import sqlite3
import sys
from pathlib import Path

import pytest
import yaml

_ROOT = Path(__file__).resolve().parent.parent


def _load():
    spec = importlib.util.spec_from_file_location(
        "provider_router", _ROOT / "scripts" / "provider_router.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["provider_router"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def router():
    return _load()


@pytest.fixture(scope="module")
def live_registry() -> dict:
    return yaml.safe_load(
        (_ROOT / "ecosystem" / "provider-registry.yaml").read_text(encoding="utf-8")
    )


# --- REFUSAL 1: a provider not on the repo's allowlist (AX22-5, every role) ------------------


def test_refusal_1_an_off_allowlist_provider_is_refused(router):
    """AX22-5: *"the router refuses a provider not on the repo's list (RED-first)."*

    Asserted through `explain` rather than `route`, because the survivors alone cannot show
    WHICH gate bit. `xai` is refused in BOTH repos and for DIFFERENT reasons — off-allowlist in
    the work repository, not-admitted on the hub — and that difference is the whole content of
    this refusal. Comparing survivor lists would have shown "absent in both" and proved nothing
    about the allowlist at all.
    """
    hub = {v.provider: v.refusal for v in router.explain("implement", repo=".dev-knowledge")}
    work = {v.provider: v.refusal for v in router.explain("implement", repo="corp-monorepo")}
    assert work["xai"] == "off-allowlist"
    assert hub["xai"] == "not-admitted", "on the hub xai is allowed; it fails a different gate"


def test_refusal_1_names_the_repo_and_the_provider(router):
    """A refusal that does not say WHICH repo refused WHICH provider sends the reader to the
    source. Both appear, plus the clause id."""
    verdicts = router.explain("implement", repo="corp-monorepo")
    off = [v for v in verdicts if v.refusal == "off-allowlist"]
    assert off, "corp-monorepo excludes two providers; at least one must show on implement"
    message = off[0].reason
    assert "corp-monorepo" in message
    assert off[0].provider in message
    assert "AX22-5" in message


def test_refusal_1_an_unlisted_repo_falls_to_the_restrictive_default(router):
    """An unknown repo is one nobody has ruled on. It gets `default:` (anthropic only), so a
    repo that was never considered cannot silently reach a paid third-party provider."""
    got = [c.provider for c in router.route("implement", repo="some-repo-nobody-declared",
                                            strict=False)]
    assert got == ["anthropic"]


def test_refusal_1_applies_to_every_role_not_just_implement(router):
    """The allowlist refusal is UNIVERSAL — contrast refusal 2, which is scoped to one role.
    `read` is the check: its declared order leads with `antigravity`, which corp-monorepo does
    not allow."""
    order = [e["provider"] for e in router.declared_order("read")]
    assert order[0] == "antigravity"
    got = [c.provider for c in router.route("read", repo="corp-monorepo", strict=False)]
    assert "antigravity" not in got


# --- REFUSAL 2: a non-admitted provider in the IMPLEMENT role --------------------------------


def test_refusal_2_a_non_admitted_producer_is_refused_on_implement(router):
    """The done-contract's second named refusal, trip-tested against the one real NOT ADMITTED
    row the registry now ships on this role: xai. (copilot-enterprise was ADMITTED here
    2026-09-23 by operator ruling O-3 — see `test_copilot_enterprise_is_now_admitted_on_implement`
    below — so it is no longer this test's example.)"""
    got = [c.provider for c in router.route("implement", repo=".dev-knowledge")]
    assert got == ["anthropic", "copilot-enterprise"], (
        "Sonnet stays first (AX22-1's >= 8-of-10 bar is unmet), and copilot-enterprise now "
        "follows it: admitted and licensed, still declared second because admission-by-ruling "
        "is not the measurement that would move its position (AX21-2's re-rank is)"
    )


def test_refusal_2_names_the_clause_and_the_measurement_that_would_lift_it(router):
    """A refusal is more useful when it says what would change it. AX22-1's >= 8-of-10 bar is
    the measurement, and it is Half B's — so the message names both the clause and the fact
    that the lift is a measurement rather than an edit."""
    verdicts = router.explain("implement", repo=".dev-knowledge")
    blocked = [v for v in verdicts if v.refusal == "not-admitted"]
    # `xai` alone. copilot-enterprise no longer appears here at all (admitted 2026-09-23) —
    # contrast the pre-2026-09-23 state, where its absence from this set was the documented
    # one-reason-per-verdict limit (blocked twice over, licence gate ran first). Now it clears
    # every gate on this role and shows up in `route()`'s survivors instead.
    assert {v.provider for v in blocked} == {"xai"}
    assert "AX22-1" in blocked[0].reason
    assert "Half B" in blocked[0].reason, "a refusal should say what would lift it"


def test_copilot_enterprise_is_now_admitted_on_implement(router):
    """`[691]`'s Half A / Half B boundary drew copilot-enterprise as NOT ADMITTED on every role.
    2026-09-23 (operator ruling O-3, `RATIFICATION-2026-09-23-copilot.md`) admitted it on
    `implement` specifically, on IN-REPO evidence (`JOURNAL.md`:962/:1113, merge `88dc48f4`, the
    ab-828/ab-832 receipts committed at
    `docs/audits/2026-09-23-technical-copilot-admission-evidence.md`) — not the AX22-1
    >= 8-of-10 measurement Half B still owns. This is the router admitting Copilot for implement,
    trip-tested against the live row rather than a fixture."""
    verdicts = {v.provider: v for v in router.explain("implement", repo=".dev-knowledge")}
    assert verdicts["copilot-enterprise"].refusal is None, (
        f"expected copilot-enterprise eligible on implement, got: {verdicts['copilot-enterprise']}"
    )
    got = [c.provider for c in router.route("implement", repo=".dev-knowledge")]
    assert "copilot-enterprise" in got
    assert got.index("copilot-enterprise") == 1, (
        "admission did not move its declared position — Sonnet stays first until AX22-1's "
        "measurement, per AX21-2, moves it"
    )


def test_the_licence_fix_also_opens_copilot_on_read_though_its_admission_there_is_untouched(
        router):
    """A side effect of the LICENCE ruling, made explicit rather than left implicit (codex terra
    review, `docs/audits/2026-09-24-codex-lane-provider-registry.md`, High).

    `providers.copilot-enterprise.licence` is a PROVIDER-level fact — fixing it repo-wide (O-3)
    clears the licence gate on every role Copilot appears in, not just `implement`. On `read`,
    that is enough on its own: the role is not admission-gated (`ADMISSION_GATED_ROLES` is
    `{"implement"}` only) and this entry sets no `requires_admission`, so once the licence gate
    clears, nothing else stands between Copilot and eligibility — even though its `read`-role
    `admission:` is untouched at `unevaluated` (`test_admission_copilot_enterprise_is_admitted_
    on_implement_not_elsewhere`, tests/test_provider_roles.py). This is the DESIGNED shape of
    `read` (its own registry description: "a not-yet-admitted reader is still a coherent idea …
    CC verifies"), not an oversight — asserted here so it is a checked property instead of an
    untested consequence of the licence edit above.
    """
    verdicts = {v.provider: v for v in router.explain("read", repo=".dev-knowledge")}
    assert verdicts["copilot-enterprise"].refusal is None, (
        f"expected copilot-enterprise eligible on read once its licence is permitted, got: "
        f"{verdicts['copilot-enterprise']}"
    )
    got = [c.provider for c in router.route("read", repo=".dev-knowledge")]
    assert got == ["antigravity", "copilot-enterprise", "anthropic"], (
        "read's declared order is unchanged; copilot-enterprise now clears every gate on it "
        "and shows up as a survivor in its declared position, same as antigravity (also "
        "unadmitted-but-licensed on this role)"
    )


def test_refusal_2_does_NOT_apply_to_review(router):
    """THE SCOPING, asserted in the direction that is easy to get wrong.

    Codex terra is recorded NOT ADMITTED (AX22-1 has measured no non-Claude provider) and is
    STILL the routable reviewer, because the done-contract scopes the admission refusal to the
    implement role alone. Were this leg to over-reach, Half A would silently change the fleet's
    review routing — a behaviour change no clause asked for.
    """
    got = [c.provider for c in router.route("review", repo=".dev-knowledge")]
    assert got[0] == "openai"


def test_refusal_2_does_NOT_apply_to_read_or_verify(router):
    """Same scoping, on the other two roles carrying unadmitted entries."""
    got = [c.provider for c in router.route("read", repo=".dev-knowledge")]
    assert got[0] == "antigravity", "read is not gated on admission; only implement is"


# --- REFUSAL 3: the licence (`[#691]` leg c) -------------------------------------------------


def test_refusal_3_a_provider_without_a_permitting_licence_is_refused(router, live_registry,
                                                                       tmp_path):
    """A RULED, non-`permitted` licence refuses just as an unruled one does — `restricted` is
    "permitted for some uses and not others", not "forbidden", and the router still refuses it
    because only `permitted` routes.

    Pre-2026-09-23 this was trip-tested against copilot-enterprise's live `read`-role row, which
    was blocked TWICE OVER (unadmitted AND unlicensed). Operator ruling O-3 (`RATIFICATION-2026-
    09-23-copilot.md`) ruled the licence `permitted` repo-wide (see `ecosystem/provider-
    registry.yaml`'s `providers.copilot-enterprise.licence` and
    `docs/audits/2026-09-23-technical-copilot-admission-evidence.md`), so the live registry no
    longer contains a REAL row with a ruled, non-permitting licence — every provider it lists is
    now `permitted` or `not-applicable` (google, deepseek — retired/absent, not routed on any
    role). A fixture is therefore the honest lever here, same shape as the unruled-licence test
    below, but for the RULED half of the vocabulary.
    """
    data = copy.deepcopy(live_registry)
    data["providers"]["xai"]["licence"] = {
        "status": "restricted",
        "reason": "fixture: a ruled, non-permitting licence.",
        "decided_by": "test",
        "decided_on": "2026-09-23",
    }
    path = tmp_path / "reg.yaml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    verdicts = {v.provider: v for v in
                router.explain("implement", repo=".dev-knowledge", registry_path=path)}
    assert verdicts["xai"].refusal == "licence"
    assert "restricted" in verdicts["xai"].reason


def test_refusal_3_an_unruled_licence_is_refused_not_assumed(router, live_registry, tmp_path):
    """Absence of a licence block resolves to `unknown`, and `unknown` refuses. The field's
    absence cannot grant what its presence was added to withhold.

    Demonstrated on `xai` rather than on `anthropic`, and the reason is itself a check on the
    schema: anthropic's licence CANNOT be deleted, because the schema refuses to validate a
    registry holding an `admitted` entry under a non-permitting licence. The fixture that would
    have been convenient here is one the data model makes unrepresentable — which is the
    invariant doing its job one level down.
    """
    data = copy.deepcopy(live_registry)
    del data["providers"]["xai"]["licence"]
    path = tmp_path / "reg.yaml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    verdicts = {v.provider: v for v in
                router.explain("implement", repo=".dev-knowledge", registry_path=path)}
    assert verdicts["xai"].refusal == "licence"
    assert "unknown" in verdicts["xai"].reason


# --- REFUSAL 4: AX22-2, reviewer is not the producer -----------------------------------------


def test_refusal_4_the_producing_provider_is_excluded_from_reviewing_its_own_work(router):
    """AX22-2 verbatim: *"Codex terra reviews unless Codex produced; then the reviewer is Grok
    (after admission) or Sonnet."* Grok is not admitted, so today the exclusion resolves to
    Sonnet — and that the chain lands there rather than failing is the property worth pinning."""
    normal = [c.provider for c in router.route("review", repo=".dev-knowledge")]
    assert normal[0] == "openai"
    excluded = [c.provider for c in
                router.route("review", repo=".dev-knowledge", produced_by="openai")]
    assert "openai" not in excluded
    assert excluded[0] == "anthropic", "AX22-2's chain lands on Sonnet while Grok is unadmitted"


def test_refusal_4_applies_only_where_the_registry_sets_the_flag(router):
    """The exclusion is data, not a hardcoded special case for one role name. A `produced_by`
    on a role whose `excludes_producer` is false changes nothing — `implement` doesn't set
    `excludes_producer`, so naming anthropic as producer here drops no candidate; the survivor
    list is unchanged from a call with no `produced_by` at all."""
    with_producer = [c.provider for c in
                     router.route("implement", repo=".dev-knowledge", produced_by="anthropic")]
    without_producer = [c.provider for c in router.route("implement", repo=".dev-knowledge")]
    assert with_producer == without_producer == ["anthropic", "copilot-enterprise"]


def test_refusal_4_reports_its_clause(router):
    verdicts = router.explain("review", repo=".dev-knowledge", produced_by="openai")
    blocked = [v for v in verdicts if v.refusal == "reviewer-is-producer"]
    assert blocked and "AX22-2" in blocked[0].reason


# --- the router refuses to return nothing silently -------------------------------------------


@pytest.fixture
def empty_allowlist_manifest(tmp_path) -> Path:
    """A manifest allowing nothing — the cleanest way to exhaust a role.

    Exhausting it through the REGISTRY is not available: the schema refuses a registry whose
    admitted entries sit under a non-permitting licence, so "make every provider unlicensed"
    is unrepresentable by construction. The allowlist has no such invariant — a repo genuinely
    may be allowed nothing — so that is the honest lever.
    """
    path = tmp_path / "manifest.yaml"
    path.write_text(yaml.safe_dump({"providers": {"allowed": {}, "default": []}}),
                    encoding="utf-8")
    return path


def test_an_exhausted_role_raises_rather_than_returning_an_empty_list(router,
                                                                     empty_allowlist_manifest):
    """A router that returns `[]` makes its refusal indistinguishable from its success at every
    call site that iterates the result — the caller loops zero times and carries on. Every
    candidate being ineligible is a REFUSAL and is raised as one, carrying each candidate's
    individual reason so the caller learns why the chain was exhausted, not merely that it was.
    """
    with pytest.raises(router.RouterRefusal) as exc:
        router.route("verify", repo=".dev-knowledge", manifest=empty_allowlist_manifest)
    message = str(exc.value)
    assert "verify" in message
    assert "anthropic" in message, "the raise carries each candidate's own reason"
    assert "AX22-5" in message


def test_strict_false_returns_the_survivors_instead_of_raising(router,
                                                               empty_allowlist_manifest):
    """`strict=False` is for REPORTING surfaces, which need the survivors without the raise.
    It never widens eligibility — an ineligible candidate is dropped either way."""
    assert router.route("verify", repo=".dev-knowledge",
                        manifest=empty_allowlist_manifest, strict=False) == []


def test_a_missing_manifest_refuses_every_route_rather_than_permitting_one(router, tmp_path):
    """Register ruling Z-G4: *"a check that cannot compute its ground truth FAILs, it does not
    skip."* An absent allowlist is the case where failing open would be most tempting and most
    wrong — the allowlist is the only gate that varies per repo, so losing it silently means
    every repo is routed as though it were the hub."""
    with pytest.raises(router.RouterRefusal) as exc:
        router.route("verify", repo=".dev-knowledge", manifest=tmp_path / "absent.yaml")
    assert "AX22-5" in str(exc.value)


def test_an_unknown_role_is_refused_by_name(router):
    with pytest.raises(router.RouterRefusal) as exc:
        router.route("summarise", repo=".dev-knowledge")
    assert "summarise" in str(exc.value)


# --- the router is the call site that makes the telemetry module harness, not inventory ------


def test_routing_a_call_records_it_in_the_tally(router, tmp_path, monkeypatch):
    """`[#694]`'s verdict on `cost_usage_telemetry.py` was INVENTORY — "a capability with no
    trigger is not harness". This is its trigger.

    `record_routing_call` is the seam AX21-2 needs: every call the router resolves is written
    to the same `genai_spans` store the re-rank reads, carrying the role, the outcome and the
    reviewer. Without a call site the re-rank would be ranking over a permanently empty table
    and reporting a declared order as a measured one.
    """
    db = tmp_path / "GENAI-TELEMETRY.db"
    router.record_routing_call(
        role="implement",
        provider="anthropic",
        model="claude-sonnet-5",
        outcome="passed",
        cost_usd=0.0142,
        input_tokens=1200,
        output_tokens=340,
        reviewed_by="gpt-5.6-terra",
        db_path=db,
    )
    with sqlite3.connect(str(db)) as conn:
        rows = conn.execute(
            "SELECT gen_ai_system, request_model, attributes_json FROM genai_spans"
        ).fetchall()
    assert len(rows) == 1
    system, model, attrs = rows[0]
    assert system == "anthropic" and model == "claude-sonnet-5"
    assert '"devknowledge.role": "implement"' in attrs
    assert '"devknowledge.outcome": "passed"' in attrs


def test_recording_a_call_for_an_ineligible_provider_is_refused(router, tmp_path):
    """The tally records what the router ROUTED. Letting it record a provider the router would
    have refused would let an off-contract call launder itself into the measurement that the
    re-rank then treats as evidence — the one path by which an unadmitted provider could earn
    a position without ever being admitted."""
    db = tmp_path / "GENAI-TELEMETRY.db"
    with pytest.raises(router.RouterRefusal):
        router.record_routing_call(
            role="implement",
            provider="xai",
            model="grok-4.6",
            outcome="passed",
            repo=".dev-knowledge",
            db_path=db,
        )


# --- Half A's own boundary, asserted rather than trusted -------------------------------------


def test_the_router_places_no_call():
    """AX23-2's boundary as a property of the code: this module resolves and refuses, it does
    not dispatch. Nothing here shells out, opens a socket, or imports a provider SDK — so the
    whole of step 4 is executable inside Half A's Claude-only scope, and Half B inherits a
    router it does not have to re-verify.

    PARSED, NOT GREPPED, and the first draft of this test is why. A substring scan went RED on
    the module's own docstring, which uses the word `subprocess` to say there is none — the
    check was matching prose ABOUT the property while claiming to measure the property. Walking
    the AST's import nodes measures what is actually imported, which is the difference between
    a name appearing in a file and a module being wired to it.
    """
    import ast

    tree = ast.parse((_ROOT / "scripts" / "provider_router.py").read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])

    dispatching = {"subprocess", "requests", "httpx", "urllib", "socket", "http", "anthropic", "openai"}
    assert not (imported & dispatching), (
        f"the router imports {sorted(imported & dispatching)}; it is a resolver, not a dispatcher"
    )


# --- alias drift, made visible (2026-09-23, S1 of POSTWAVE-CHAIN-2026-09-22) -------------------


#: The CLI-resolved marketing aliases a `--model` flag can name at dispatch time. Claude Code
#: 2.1.280 repointed `opus` from `claude-opus-4-8` to `claude-opus-5-5` with no registry edit —
#: the whole point of an alias is that its target can move underneath it. A registry entry that
#: named one of these instead of a versioned id would silently repoint the next time the CLI's
#: alias table changed, with nothing here to notice.
_BARE_CLI_ALIASES = {"opus", "sonnet", "haiku", "opusplan"}


def test_every_role_entry_pins_a_versioned_model_id_not_a_bare_alias(live_registry):
    """Alias drift, guarded rather than merely noted. `ecosystem/provider-registry.yaml` carries
    a dated comment (above `roles:`) recording that the bare `opus` alias now resolves to
    `claude-opus-5-5` rather than to `claude-opus-4-8`, the id `orchestrate`/`plan` still pin —
    a fact nothing in a lane contract's `--model opus` dispatch line would otherwise surface.

    This test is the enforcement half: every role-order entry that names a model at all names
    the VERSIONED id, never the bare alias a CLI resolves at dispatch time. It passes today by
    construction — every live entry already pins a real id — and it exists so a future hand-edit
    that swaps one back to a bare alias fails loudly instead of drifting silently the way the
    CLI's own alias table just did.
    """
    for role, spec in live_registry.get("roles", {}).items():
        for i, entry in enumerate(spec.get("order") or []):
            model = entry.get("model")
            if model is None:
                continue
            assert model not in _BARE_CLI_ALIASES, (
                f"role `{role}` order[{i}] pins the bare alias `{model}` — name the versioned "
                f"model id it resolves to today; the CLI's alias->id mapping can move (2.1.280 "
                f"repointed `opus` from claude-opus-4-8 to claude-opus-5-5) with no edit here"
            )
            assert model in live_registry["models"], (
                f"role `{role}` order[{i}] pins `{model}`, which is not a declared model id"
            )
