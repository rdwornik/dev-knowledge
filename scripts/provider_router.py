#!/usr/bin/env python
"""provider_router.py -- `[#691]` step 4: who answers for a role in a repo, and who is refused.

WHAT THIS IS. The reader of the three surfaces `[#691]` step 3 built, and the one place their
rules are applied together:

    ecosystem/provider-registry.yaml  `roles:`     the ORDERED fallback list, per-entry
                                                   admission, the reviewer-not-producer flag
    ecosystem/provider-registry.yaml  `providers:` each provider's licence
    deploy/manifest-v1.5.0.yaml       `providers.allowed`  the per-repo allowlist (AX22-5)

`route()` answers "who answers for this role in this repo, in what order". `explain()` answers
the same question and ALSO reports every candidate it dropped and why -- which is the surface a
report reads, because a list of survivors cannot tell you what was refused.

WHAT THIS IS NOT, and the boundary is load-bearing rather than decorative: **it places no
call.** It resolves and refuses; it does not dispatch. There is no `subprocess`, no HTTP client
and no provider SDK in this module, and `tests/test_provider_router.py` asserts their absence
rather than trusting this paragraph. That is what makes the whole of step 4 executable inside
AX23-2's Half A -- a lane defined by ordering no non-Claude provider can still build, ship and
trip-test the router that will order them, because resolving a route is not taking one.

EXISTS-BEFORE-BUILD (AX9-4), quoted rather than asserted. Before writing this module:
    uv run --locked python scripts/graph_queries.py process-list   -> 161 processes, none
        routing-, ranking-, provider- or tally-shaped
    grep -iE "rout|rank|provider|telemetr" ecosystem/organ-index.md -> two hits, both CHECKERS:
        `provider-registry-agreement` (pre-commit) and `conformance-hub.js`
`scripts/routing_agreement.py` is the nearest neighbour and is deliberately not extended: it
asserts that the in-repo routing table and its L0 derived copy AGREE, which is detection over
two copies of one table. Choosing between candidates is a different act on different data, and
folding it into an agreement checker would give that module two jobs and one name.

=============================================================================================
THE FOUR REFUSALS, AND THEIR SCOPES -- the part to read before changing anything
=============================================================================================

Three of the four are scoped NARROWER than "always", and each scope is a clause rather than a
judgement call:

  off-allowlist         EVERY ROLE.     AX22-5: "the router refuses a provider not on the
                                        repo's list". No role qualifier in the clause.
  not-admitted          IMPLEMENT, PLUS ANY ENTRY THAT ASKS FOR IT. The lane done-contract,
                                        item 1, verbatim: "REFUSES a non-admitted provider IN
                                        THE IMPLEMENT ROLE" -- that is the role-level gate.
                                        AX22-2 then conditions ONE FURTHER ENTRY on admission
                                        without gating its role: "the reviewer is Grok (AFTER
                                        ADMISSION) or Sonnet". A role-level gate cannot express
                                        that pair, so an entry may set `requires_admission` and
                                        this gate honours it. Both legs, because the two clauses
                                        scope differently and collapsing them would break one.
  licence               EVERY ROLE.     `[#691]`'s Done-when gates on "whose licence permits
                                        THE USE" -- using a provider at all is the use, so
                                        this one does not narrow to producing roles.
  reviewer-is-producer  WHERE THE REGISTRY SETS THE FLAG, which today is `review` alone
                                        (AX22-2). Read from data, never special-cased on the
                                        role's name.

THE ADMISSION SCOPE IS THE ONE THAT LOOKS WRONG AND IS NOT. Codex terra is recorded NOT
ADMITTED -- AX22-1's >= 8-of-10 bar has measured no non-Claude provider -- and is still the
routable reviewer, because the admission refusal reaches only `implement`. Widening it would
have Half A silently change the fleet's review routing, which no clause asked for and which
would be a behaviour change smuggled in under a mechanism commit. The two facts are reconciled
by the scope, not in spite of it.

ORDER IS DECLARED UNTIL MEASURED. `route()` returns the registry's declared order. `rerank()`
(step 5) reorders it by measured pass rate per cost over the `genai_spans` tally, and reports
when it had nothing to measure -- because presenting an unmeasured list as a measured one is
the "fixed list wearing a router's name" failure AX21-2 exists to name.

Layer-2 (ADR-28/36): this module reads three files and writes one local, uncommitted telemetry
row through `cost_usage_telemetry`. It drives no state in any child repo.
"""
from __future__ import annotations

import importlib.util
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Collection, Mapping, Optional

import yaml

_REPO_ROOT = Path(__file__).resolve().parent.parent


def _sibling(name: str, module_name: str):
    """Load a sibling script BY PATH.

    Same shape `telemetry_emit.py` uses for `gitenv.py`, and for the same reason: `import x`
    and `from scripts import x` each have a shadow hole, and ordering them only moves it. A
    path load names exactly one file.
    """
    spec = importlib.util.spec_from_file_location(module_name, Path(__file__).resolve().with_name(name))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_registry = _sibling("provider_registry.py", "dev_knowledge_provider_registry")
_telemetry = _sibling("cost_usage_telemetry.py", "cost_usage_telemetry")

#: The deploy manifest carrying `providers.allowed` (AX22-5). Resolved at call time rather than
#: frozen at import, for the R6(c) reason `telemetry_emit.repo_root` states: a module-frozen
#: path answers "where does this file live", every caller wants "which repository is acting".
MANIFEST_RELPATH = "deploy/manifest-v1.5.0.yaml"

#: Env override, so a consumer checkout or a test can point at its own manifest without
#: patching a module global.
MANIFEST_PATH_ENV = "DEV_KNOWLEDGE_PROVIDER_MANIFEST"

#: The role whose candidates are gated on admission. A frozenset of one rather than an `==`,
#: so widening it later is a visible data change with a diff rather than an edited comparison.
ADMISSION_GATED_ROLES: frozenset[str] = frozenset({"implement"})

#: The one licence status that permits routing. Everything else -- `restricted`, `unknown`,
#: `not-applicable` -- refuses, and `unknown` refusing is the whole point of the vocabulary:
#: an unruled licence is not a permission.
PERMITTING_LICENCE = "permitted"

#: [#1833] the pseudo-role under which the registry's `evaluation:` collection is routed.
EVALUATION_ROLE = "evaluate"


class RouterRefusal(RuntimeError):
    """Every refusal this module raises.

    Raised rather than returned as an empty list. A router that hands back `[]` makes its
    refusal indistinguishable from its success at every call site that iterates the result --
    the caller loops zero times and carries on, which is the silent-degradation failure the
    whole admission apparatus exists to prevent.
    """


@dataclass(frozen=True)
class Candidate:
    """One provider the router WOULD route to, in rank order."""

    provider: str
    model: Optional[str]
    position: int
    note: Optional[str] = None
    max_turns_floor: Optional[int] = None
    #: [#1844] S-1: the entry is a SAME-VENDOR rung that runs in a NEW session (no producer transcript or prose).
    isolated_session: bool = False


@dataclass(frozen=True)
class Verdict:
    """One candidate's full disposition — eligible, or refused with the reason and the clause.

    `refusal` is `None` for an eligible candidate and otherwise names the gate that bit:
    `off-allowlist` | `not-admitted` | `licence` | `reviewer-is-producer`. A machine-readable
    token beside a human-readable `reason`, because a report needs to group by the first and a
    reader needs the second.
    """

    provider: str
    model: Optional[str]
    position: int
    refusal: Optional[str]
    reason: str
    max_turns_floor: Optional[int] = None
    isolated_session: bool = False


def manifest_path(path: Optional[Path] = None) -> Path:
    if path is not None:
        return Path(path)
    override = os.environ.get(MANIFEST_PATH_ENV)
    if override:
        return Path(override)
    return _REPO_ROOT / MANIFEST_RELPATH


def allowlist(repo: str, path: Optional[Path] = None) -> list[str]:
    """The providers `repo` may reach — AX22-5's per-repo list, from the deploy manifest.

    An UNLISTED repo falls to `providers.default`, which is `[anthropic]`. The default is the
    restrictive entry on purpose: a repo nobody has ruled on is not a repo that has been
    cleared, and a permissive default would make "not yet considered" indistinguishable from
    "allowed" — the same present-but-unread defect the licence vocabulary's `unknown` prevents
    one level down.
    """
    p = manifest_path(path)
    if not p.exists():
        raise RouterRefusal(
            f"the deploy manifest carrying `providers.allowed` is absent: {p}. AX22-5 makes it "
            f"the allowlist's home, and a missing allowlist refuses every route rather than "
            f"permitting one — a check that cannot compute its ground truth FAILs, it does not "
            f"skip (register ruling Z-G4)"
        )
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    providers = data.get("providers") or {}
    allowed = providers.get("allowed") or {}
    if repo in allowed:
        return list(allowed[repo])
    return list(providers.get("default") or [])


def declared_order(role: str, registry_path: Optional[Path] = None) -> list[dict[str, Any]]:
    """The registry's DECLARED order for `role` — before any gate, before any re-rank.

    Exposed because a report needs to show what was declared alongside what survived; a reader
    given only the survivors cannot see that anything was dropped.
    """
    try:
        return _registry.role_order(role, registry_path)
    except _registry.RegistryError as exc:
        raise RouterRefusal(str(exc)) from exc


def _role_spec(role: str, registry_path: Optional[Path] = None) -> dict[str, Any]:
    # [#1833] `evaluate` is the top-level `evaluation:` collection, not a `roles:` key.
    spec = (_registry.evaluation(registry_path) if role == EVALUATION_ROLE
            else _registry.roles(registry_path).get(role)) or None
    if spec is None:
        raise RouterRefusal(
            f"role `{role}` is not in the registry; known roles: "
            f"{sorted(_registry.roles(registry_path))}"
        )
    return spec


def explain(
    role: str,
    repo: str,
    *,
    produced_by: Optional[str] = None,
    registry_path: Optional[Path] = None,
    manifest: Optional[Path] = None,
    admitted_models: Collection[str] = frozenset(),
    case_approved: bool = False,
) -> list[Verdict]:
    """Every declared candidate for `role` in `repo`, each with its disposition.

    The reporting surface. `route()` is this function filtered to the eligible ones — written
    that way round deliberately, so the refusal reasons a report shows and the refusals the
    router actually applies are the SAME computation and cannot drift into disagreement.

    Gates are applied in a fixed order and the FIRST one to bite is reported, which makes each
    verdict single-valued. Where a provider is blocked twice over — copilot-enterprise is both
    unadmitted and unlicensed — only the first is named here; `explain` on a role where the
    other gate does not apply is how the second becomes visible. That is a real limit of a
    one-reason report and is stated rather than papered over.
    """
    spec = _role_spec(role, registry_path)
    allowed = set(allowlist(repo, manifest))
    licences = _registry.licences(registry_path)
    gated = role in ADMISSION_GATED_ROLES
    excludes_producer = bool(spec.get("excludes_producer"))

    verdicts: list[Verdict] = []
    for position, entry in enumerate(declared_order(role, registry_path)):
        provider = str(entry["provider"])
        model = entry.get("model")
        common = dict(provider=provider, model=model, position=position,
                      max_turns_floor=entry.get("max_turns_floor"),
                      isolated_session=bool(entry.get("isolated_session")))

        if provider not in allowed:
            verdicts.append(Verdict(
                **common, refusal="off-allowlist",
                reason=(
                    f"repo `{repo}` does not allow provider `{provider}` (AX22-5: the deploy "
                    f"manifest carries providers.allowed per consumer, and the router refuses "
                    f"a provider not on the repo's list). Allowed here: {sorted(allowed)}"
                )))
            continue

        licence = licences.get(provider, "unknown")
        if licence != PERMITTING_LICENCE:
            verdicts.append(Verdict(
                **common, refusal="licence",
                reason=(
                    f"provider `{provider}` has licence status `{licence}` ([#691] leg c: only "
                    f"a provider whose licence permits the use is routable). `unknown` refuses "
                    f"rather than defers — an unruled licence is not a permission, and ruling "
                    f"one is a functional question for the operator (ADR-108 §A)"
                )))
            continue

        # `admitted_models` ([#1833] D1): model ids that already have a served shadow-admission record, so an
        # entry that `requires_admission` is routable on that record before the registry row is flipped.
        served_admitted = model is not None and model in admitted_models
        if (gated or entry.get("requires_admission")) and not (
                _registry.is_admitted(entry) or served_admitted):
            verdicts.append(Verdict(
                **common, refusal="not-admitted",
                reason=(
                    f"provider `{provider}` is NOT ADMITTED for role `{role}` (AX22-1: "
                    f"admission is >= 8 of 10 tasks green on first review). This lifts by "
                    f"MEASUREMENT, not by editing the registry — the bounded trial tasks are "
                    f"Half B's (AX23-2). The refusal is scoped to the implement role by the "
                    f"lane done-contract; other roles are not gated on admission"
                )))
            continue

        if entry.get("per_case_only") and not case_approved:
            verdicts.append(Verdict(
                **common, refusal="per-case-only",
                reason=(
                    f"provider `{provider}` is routable for an operator-approved case only "
                    f"(R-5: a metered provider is never a standing route; Grok is OFF unless the "
                    f"operator approves a case). Pass `case_approved=True` for an approved case"
                )))
            continue

        if (excludes_producer and produced_by is not None and provider == produced_by
                and not entry.get("isolated_session")):
            verdicts.append(Verdict(
                **common, refusal="reviewer-is-producer",
                reason=(
                    f"provider `{provider}` produced the artifact under review (AX22-2: "
                    f"reviewer != producer, always). The registry sets excludes_producer on "
                    f"this role; the next eligible candidate in the declared order answers "
                    f"instead. A same-vendor entry is admitted ONLY when it carries "
                    f"`isolated_session: true` (operator S-1, [#1844])"
                )))
            continue

        verdicts.append(Verdict(**common, refusal=None, reason="eligible"))
    return verdicts


def route(
    role: str,
    repo: str,
    *,
    produced_by: Optional[str] = None,
    registry_path: Optional[Path] = None,
    manifest: Optional[Path] = None,
    strict: bool = True,
    admitted_models: Collection[str] = frozenset(),
    case_approved: bool = False,
) -> list[Candidate]:
    """The eligible candidates for `role` in `repo`, in declared rank order.

    `strict=True` (the default) RAISES when every candidate is ineligible, carrying each one's
    individual reason — so a caller learns why the chain was exhausted, not merely that it was.
    `strict=False` returns the survivors and is for reporting surfaces that need the list
    without the raise; it never widens eligibility, an ineligible candidate is dropped either
    way.

    `produced_by` is the provider that produced the artifact under review. Supplied on a review
    route and ignored on every role whose registry entry does not set `excludes_producer` —
    read from data rather than special-cased on the role's name, so AX22-2 reaching a second
    role later is a registry edit rather than a code change.
    """
    verdicts = explain(role, repo, produced_by=produced_by,
                       registry_path=registry_path, manifest=manifest,
                       admitted_models=admitted_models, case_approved=case_approved)
    eligible = [
        Candidate(provider=v.provider, model=v.model, position=v.position,
                  max_turns_floor=v.max_turns_floor, isolated_session=v.isolated_session)
        for v in verdicts if v.refusal is None
    ]
    if eligible or not strict:
        return eligible
    detail = "; ".join(f"{v.provider}: {v.reason}" for v in verdicts) or "no candidates declared"
    raise RouterRefusal(
        f"role `{role}` has no eligible provider in repo `{repo}` — every declared candidate "
        f"was refused. {detail}"
    )


def record_routing_call(
    *,
    role: str,
    provider: str,
    model: Optional[str] = None,
    outcome: str = "unknown",
    cost_usd: Optional[float] = None,
    input_tokens: Optional[int] = None,
    output_tokens: Optional[int] = None,
    duration_ms: Optional[int] = None,
    reviewed_by: Optional[str] = None,
    repo: Optional[str] = None,
    lane_id: Optional[str] = None,
    batch_id: Optional[str] = None,
    registry_path: Optional[Path] = None,
    manifest: Optional[Path] = None,
    db_path: Optional[Path] = None,
) -> int | None:
    """Record one routed call in the tally the re-rank reads — AX21-2's write half.

    THIS IS THE CALL SITE `[#694]` ASKED FOR. That row's verdict on
    `scripts/cost_usage_telemetry.py` was INVENTORY, on the operator's definition that "a
    capability with no trigger is not harness". This is its trigger: every call the router
    resolves lands in `genai_spans` carrying the role, the work-product outcome and the
    reviewer, which is exactly the tuple `rerank()` needs. Without it the re-rank would rank
    over a permanently empty table while presenting a declared order as a measured one.

    WHEN `repo` IS GIVEN THE ROUTE IS RE-CHECKED AND AN INELIGIBLE ONE IS REFUSED. That check
    is not belt-and-braces; it closes the one path by which an unadmitted provider could earn a
    position without ever being admitted. The re-rank treats this table as evidence, so a call
    the router would have refused must not be able to launder itself into the measurement that
    later promotes the provider that made it. `repo` is optional only so a replay or an import
    of already-audited history can write rows without re-resolving a repo it has no opinion on.
    """
    if repo is not None:
        eligible = {
            c.provider for c in route(role, repo, registry_path=registry_path,
                                      manifest=manifest, strict=False)
        }
        if provider not in eligible:
            reasons = {v.provider: v.reason for v in
                       explain(role, repo, registry_path=registry_path, manifest=manifest)}
            raise RouterRefusal(
                f"refusing to record a `{role}` call to `{provider}` in repo `{repo}`: the "
                f"router would not have routed it. {reasons.get(provider, 'not a declared candidate')}. "
                f"The tally is the re-rank's evidence, so a call the router refuses cannot be "
                f"written into it"
            )
    return _telemetry.emit_genai_span(
        system=provider,
        request_model=model or provider,
        response_model=model,
        role=role,
        outcome=outcome,
        reviewed_by=reviewed_by,
        cost_estimated_usd=cost_usd,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        duration_ms=duration_ms,
        lane_id=lane_id,
        batch_id=batch_id,
        db_path=db_path,
    )


# =============================================================================================
# [#1833] / [#1844] -- ROUTING UNDER QUOTA (operator S-1, replacing A-3), BUDGETS, BULK, ACCOUNTS
# =============================================================================================
#
# PURE FUNCTIONS OVER READINGS. Nothing here reads a rollout, a statusline or a billing API: the readers are
# `scripts/quota_watch.py`, and they hand this module plain readings. A Codex reading is any object with the
# attributes below (read with getattr-default-None, so a reader may grow fields without breaking the router);
# `None` always means "not read", never zero, and an unread Codex is NOT out (R-4: a launch with no current
# reading goes ahead and the receipt records `quota: unread`).
#
#     status                   "ok" | "unknown"
#     primary_used_percent     the 5-hour window, 0..100
#     primary_resets_at        epoch seconds
#     secondary_used_percent   the weekly window
#     secondary_resets_at      epoch seconds
#     secondary_window_minutes defaults to 10080
#     usage_limit_at           epoch seconds of the newest usage-limit error record
#     usage_limit_resets_at    epoch seconds that record said the limit lifts, when it said so

#: R-1 window leg: Codex is OUT at or above this primary used-percent while its reset is still in the future.
CODEX_OUT_PERCENT = 95.0
#: R-1 pacing leg: weekly usage leading the elapsed fraction of the week by this many points moves review 1 only.
CODEX_PACING_LEAD_POINTS = 10.0
#: Operator S-1: the longest any stage waits for a reset. A usable next rung is ALWAYS taken at once; WAIT exists
#: only when no rung is usable and the reset is this close.
WAIT_BOUND_SECONDS = 1200.0
#: What the caller records in the receipt when an isolated same-vendor session runs (S-1).
ISOLATED_SESSION_MARKER = "ISOLATED-SESSION-SAME-VENDOR"
#: Roles that never route to an anthropic provider, whatever the registry says (S-1 item 7: evaluation keeps
#: "never Claude"; the isolated-Claude rung is written for review and judge only).
NEVER_CLAUDE_ROLES: frozenset[str] = frozenset({EVALUATION_ROLE})
#: R-3: more than this many units in one dispatch call is bulk work.
BULK_UNIT_THRESHOLD = 20
BULK_KINDS: frozenset[str] = frozenset({"aj-extraction"})
#: R-5.
COPILOT_PROVIDER = "copilot-enterprise"
ACTION_ROUTE = "ROUTE"
ACTION_WAIT = "WAIT"
ACTION_REFUSED = "REFUSED-NO-ROUTE"


def _num(obj: Any, name: str) -> Optional[float]:
    value = getattr(obj, name, None)
    return None if value is None else float(value)


def _codex_ok(codex: Any) -> bool:
    return codex is not None and getattr(codex, "status", "ok") != "unknown"


def codex_window_out(codex: Any, now: float) -> bool:
    """R-1 window leg: is Codex OUT right now?

    OUT while the newest rollout's primary window reads 95 % or more with its `resets_at` still in the future, OR
    a usage-limit record is newer than that `resets_at` (the limit was hit in a window the rollout does not
    describe) and the record's own reset, when it named one, has not passed. A rollout older than its own
    `resets_at` counts as reset, and `None` / an unknown reading is never out.
    """
    if not _codex_ok(codex):
        return False
    used, resets = _num(codex, "primary_used_percent"), _num(codex, "primary_resets_at")
    if used is not None and used >= CODEX_OUT_PERCENT and resets is not None and resets > now:
        return True
    limit_at, limit_resets = _num(codex, "usage_limit_at"), _num(codex, "usage_limit_resets_at")
    if limit_at is not None and (resets is None or limit_at > resets):
        return limit_resets is None or limit_resets > now
    return False


def codex_pacing_ahead(codex: Any, now: float) -> bool:
    """R-1 pacing leg: does weekly usage lead the elapsed share of the week by 10 points or more?"""
    if not _codex_ok(codex):
        return False
    used, resets = _num(codex, "secondary_used_percent"), _num(codex, "secondary_resets_at")
    if used is None or resets is None:
        return False
    window = _num(codex, "secondary_window_minutes") or 10080.0
    elapsed = min(100.0, max(0.0, (1 - (resets - now) / (window * 60)) * 100))
    return used - elapsed >= CODEX_PACING_LEAD_POINTS - 1e-9


def _codex_reset(codex: Any, now: float) -> Optional[float]:
    """When the window leg lifts, for the WAIT arithmetic: the primary reset, else the usage-limit record's own."""
    resets = _num(codex, "primary_resets_at")
    used = _num(codex, "primary_used_percent")
    if used is not None and used >= CODEX_OUT_PERCENT and resets is not None and resets > now:
        return resets
    return _num(codex, "usage_limit_resets_at")


@dataclass(frozen=True)
class ProviderState:
    """One provider's usability right now, as a reader reported it. A provider with no state is usable."""

    usable: bool = True
    reason: Optional[str] = None
    resets_at: Optional[float] = None


@dataclass(frozen=True)
class RouteDecision:
    """The answer of `route_under_quota`: take a rung now, wait a bounded time, or refuse with the facts.

    `rungs` is every usable candidate in order (so the evaluation PAIR is visible), `candidate` is `rungs[0]` for a
    ROUTE, `reasons` maps `provider/model` to why each skipped rung was skipped, `resets_at` is the soonest known
    reset among the unusable rungs, and `trigger` names the fallback rule that skipped Codex.
    """

    action: str
    role: str
    candidate: Optional[Candidate] = None
    rungs: tuple[Candidate, ...] = ()
    resets_at: Optional[float] = None
    reasons: dict[str, str] = field(default_factory=dict)
    trigger: Optional[str] = None
    marker: Optional[str] = None


def route_under_quota(
    role: str,
    repo: str,
    *,
    now: float,
    codex: Any = None,
    states: Optional[Mapping[str, ProviderState]] = None,
    produced_by: Optional[str] = None,
    admitted_models: Collection[str] = frozenset(),
    case_approved: bool = False,
    registry_path: Optional[Path] = None,
    manifest: Optional[Path] = None,
) -> RouteDecision:
    """Operator S-1 on [#1833]'s R-1 legs: who answers for `review`, `judge` or `evaluate` NOW.

    Walks the role's eligible entries in declared order (every existing gate still applies: allowlist, licence,
    admission, per-case, producer exclusion) and returns the FIRST USABLE rung at once, whatever any reset time is.
    Codex is skipped while its window leg holds (any role) or, for `review` alone, while its pacing leg holds.
    A provider whose `ProviderState` is unusable is skipped. Only when NO rung is usable does time matter: a known
    reset 20 minutes away or less is a bounded WAIT, anything else is REFUSED-NO-ROUTE carrying the role, the
    soonest reset and each skipped rung's reason -- never an unbounded wait.
    """
    states = states or {}
    verdicts = explain(role, repo, produced_by=produced_by, registry_path=registry_path, manifest=manifest,
                       admitted_models=admitted_models, case_approved=case_approved)
    window_out = codex_window_out(codex, now)
    pacing = role == "review" and codex_pacing_ahead(codex, now)
    codex_reset = _codex_reset(codex, now) if window_out else None

    reasons: dict[str, str] = {}
    resets: list[float] = []
    rungs: list[Candidate] = []
    trigger: Optional[str] = None
    for v in verdicts:
        key = f"{v.provider}/{v.model or 'default'}"
        if v.refusal is not None:
            reasons[key] = f"{v.refusal}: {v.reason}"
            continue
        if role in NEVER_CLAUDE_ROLES and v.provider == "anthropic":
            reasons[key] = f"role `{role}` never routes to Claude (operator S-1 item 7)"
            continue
        if v.provider == "openai" and window_out:
            trigger = trigger or "codex_quota.window"
            reasons[key] = "Codex is out: primary window at 95% or more, or a newer usage-limit record (R-1 window leg)"
            if codex_reset is not None:
                resets.append(codex_reset)
            continue
        if v.provider == "openai" and pacing:
            trigger = trigger or "codex_quota.pacing"
            reasons[key] = "Codex weekly usage leads the elapsed week by 10 points or more (R-1 pacing leg: review 1 only)"
            continue
        state = states.get(v.provider)
        if state is not None and not state.usable:
            reasons[key] = state.reason or f"provider `{v.provider}` is unusable right now"
            if state.resets_at is not None and state.resets_at > now:
                resets.append(state.resets_at)
            continue
        rungs.append(Candidate(provider=v.provider, model=v.model, position=v.position,
                               max_turns_floor=v.max_turns_floor, isolated_session=v.isolated_session))
    soonest = min(resets) if resets else None
    if rungs:
        chosen = rungs[0]
        marker = (ISOLATED_SESSION_MARKER
                  if chosen.isolated_session and produced_by is not None and chosen.provider == produced_by
                  else None)
        return RouteDecision(ACTION_ROUTE, role, chosen, tuple(rungs), soonest, reasons, trigger, marker)
    if soonest is not None and soonest - now <= WAIT_BOUND_SECONDS:
        return RouteDecision(ACTION_WAIT, role, None, (), soonest, reasons, trigger, None)
    return RouteDecision(ACTION_REFUSED, role, None, (), soonest, reasons, trigger, None)


# --- budgets (R-5) --------------------------------------------------------------------------

@dataclass(frozen=True)
class BudgetVerdict:
    allowed: bool
    reason: str


def _billing(provider: str, registry_path: Optional[Path]) -> dict[str, Any]:
    return (_registry.providers(registry_path).get(provider) or {}).get("billing") or {}


def check_budget(
    provider: str,
    *,
    requested_usd: float = 0.0,
    spent_today_usd: float = 0.0,
    case_cap_usd: Optional[float] = None,
    mtd_credits: Optional[float] = None,
    requested_credits: float = 0.0,
    approved: bool = False,
    registry_path: Optional[Path] = None,
) -> BudgetVerdict:
    """R-5: may this provider take a call of this size today? Read from the registry's `billing:` block.

    * `metered` (xai): the day's budget is the approved case's cap, else `default_usd` (0). A cap above
      `per_case_cap_usd` is refused. A budget of 0 refuses EVERY call. Refused when today's spend plus the request
      would pass the budget.
    * `copilot-enterprise`: refused when month-to-date plus the request would pass
      `refuse_noncritical_when_mtd_above` (25,000 credits) without operator `approved`; an unread month-to-date is
      allowed and SAYS so ("unread"), because R-4 sends a launch ahead on no reading.
    * a flat subscription is allowed.
    """
    billing = _billing(provider, registry_path)
    klass = billing.get("class")
    budget = billing.get("daily_budget") or {}
    if klass == "metered":
        default = float(budget.get("default_usd") or 0.0)
        per_case = budget.get("per_case_cap_usd")
        if case_cap_usd is not None and per_case is not None and case_cap_usd > float(per_case):
            return BudgetVerdict(False, f"case cap ${case_cap_usd:g} exceeds the per-case ceiling ${float(per_case):g} for `{provider}`")
        day = float(case_cap_usd) if case_cap_usd is not None else default
        if day <= 0:
            return BudgetVerdict(False, f"`{provider}` is metered with a ${day:g} daily budget: every call is refused until the operator approves a case")
        if spent_today_usd + requested_usd > day + 1e-12:
            return BudgetVerdict(False, f"`{provider}` call of ${requested_usd:g} on ${spent_today_usd:g} spent today passes the ${day:g} daily budget")
        return BudgetVerdict(True, f"within the ${day:g} daily budget for `{provider}`")
    if klass == "subscription-employer" and budget.get("refuse_noncritical_when_mtd_above") is not None:
        ceiling = float(budget["refuse_noncritical_when_mtd_above"])
        if mtd_credits is None:
            return BudgetVerdict(True, f"`{provider}` month-to-date credits unread: the launch goes ahead (R-4)")
        if mtd_credits + requested_credits > ceiling and not approved:
            return BudgetVerdict(False, f"`{provider}` month-to-date {mtd_credits:g} + {requested_credits:g} credits passes {ceiling:g}: overage needs operator approval")
        return BudgetVerdict(True, f"`{provider}` month-to-date {mtd_credits:g} credits within {ceiling:g}")
    return BudgetVerdict(True, f"`{provider}` is a flat subscription: no per-call budget")


def enforce_budget(provider: str, **kwargs: Any) -> BudgetVerdict:
    """`check_budget`, raising `RouterRefusal` when the call is not allowed."""
    verdict = check_budget(provider, **kwargs)
    if not verdict.allowed:
        raise RouterRefusal(verdict.reason)
    return verdict


# --- bulk work (R-3) ------------------------------------------------------------------------

@dataclass(frozen=True)
class BulkDecision:
    action: str
    provider: str
    model: Optional[str] = None
    resets_at: Optional[float] = None


def bulk_route(*, kind: str, batch_units: int, agy: ProviderState = ProviderState()) -> BulkDecision:
    """R-3: bulk work (an AJ extraction, or more than 20 units in one dispatch call) waits for its own provider's
    reset and NEVER falls back into the anthropic pool. A single read with agy out may fall back to Haiku."""
    bulk = kind in BULK_KINDS or batch_units > BULK_UNIT_THRESHOLD
    if agy.usable:
        return BulkDecision(ACTION_ROUTE, "antigravity", None, None)
    if bulk:
        return BulkDecision(ACTION_WAIT, "antigravity", None, agy.resets_at)
    return BulkDecision(ACTION_ROUTE, "anthropic", _registry.anthropic_role_model("read"), None)


# --- accounts (D4) --------------------------------------------------------------------------

def select_account(
    accounts: Optional[list[Mapping[str, Any]]],
    seat: str,
    *,
    quota_for: Optional[Callable[[Mapping[str, Any]], Optional[tuple[Optional[float], Optional[float]]]]] = None,
) -> Optional[Mapping[str, Any]]:
    """D4: the first ACTIVE account that serves `seat` and has headroom, else None.

    An inactive account is never returned, however much headroom it has: drafted accounts are inert until a ruling
    activates them. `quota_for(account)` returns `(five_hour_pct, seven_day_pct)`; either may be None (unread, so
    not a reason to skip, R-4), and so may the whole return.
    """
    for account in accounts or ():
        if not account.get("active"):
            continue
        seats = list(account.get("seats") or ())
        if seat not in seats and "*" not in seats:
            continue
        reading = quota_for(account) if quota_for is not None else None
        if reading is not None and any(v is not None and v >= CODEX_OUT_PERCENT for v in reading):
            continue
        return account
    return None


# =============================================================================================
# STEP 5 -- the re-rank (AX21-2) and the admission report
# =============================================================================================
#
# THE FAILURE THIS SECTION IS WRITTEN AGAINST, from the lane contract: *"a router re-ranked on
# nothing measured is a fixed list wearing a router's name."* A re-rank that quietly hands back
# the declared order when it has no data looks IDENTICAL to one that measured and confirmed it,
# and the difference between those two is the whole of AX21-2. So every result below carries
# `measured` and `basis`: a caller can always tell a measured order from a declared one without
# going to the tally itself.
#
# THE METRIC is AX21-2's own words -- "measured pass rate per cost":
#
#     score = pass_rate / mean_cost_per_call        pass_rate = passed / judged
#
# and each term has a decision behind it:
#
#   `judged` EXCLUDES `unknown`. An unjudged call is not evidence of a pass. Leaving it in the
#   denominator understates a provider; dropping it from the record entirely would let a
#   half-measured provider read as a fully-measured one. It is excluded from the rate and
#   reported in the count.
#
#   A MINIMUM SAMPLE, defaulting to AX22-1's ten. A provider that passed its only call has a
#   measured rate of 1.0, and promoting on that is ranking on noise while calling it
#   measurement. Below the floor the declared position stands and the reason is reported.
#
#   NO RECORDED COST MEANS NO SCORE, not a sentinel. A subscription-metered provider records no
#   per-call cost, so pass-rate-per-cost is not computable for it. Infinity would make it
#   unbeatable and zero would make it last; both are fabrications. It is reported unscored and
#   keeps its declared position, which is the only answer the data supports.

#: AX22-1's measurement window -- "the first ten tasks per provider are the measurement".
#: Reused here as the re-rank's floor rather than a second number invented for the purpose.
DEFAULT_MIN_SAMPLE = 10


@dataclass(frozen=True)
class ProviderStats:
    """One provider's measured record for one role, read from the `genai_spans` tally."""

    provider: str
    calls: int
    judged: int
    passed: int
    failed: int
    unknown: int
    cost_usd: float

    @property
    def pass_rate(self) -> Optional[float]:
        """`passed / judged`, or `None` when nothing has been judged.

        `None` rather than `0.0`: a provider nobody has judged has NO measured rate, and a zero
        would read as "measured, and it failed everything" -- the same
        unresolved-is-not-a-measured-zero distinction `telemetry_emit` draws on coverage.
        """
        return (self.passed / self.judged) if self.judged else None

    @property
    def mean_cost(self) -> Optional[float]:
        return (self.cost_usd / self.calls) if self.calls and self.cost_usd else None

    @property
    def score(self) -> Optional[float]:
        """Pass rate per cost — `None` when either term is unmeasured. See the section note."""
        rate, cost = self.pass_rate, self.mean_cost
        if rate is None or cost is None:
            return None
        return rate / cost


@dataclass(frozen=True)
class RerankResult:
    """A role's order, plus whether measurement produced it.

    `measured` is the field that stops a declared order masquerading as a confirmed one, and
    `basis` is the sentence a report prints so a human gets the same distinction the caller does.
    """

    role: str
    order: list[str]
    measured: bool
    basis: str
    stats: dict[str, ProviderStats]


@dataclass(frozen=True)
class AdmissionRow:
    """One provider's RECORDED admission state — what the registry says, not a measurement."""

    provider: str
    admitted_in: list[str]
    not_admitted_in: list[str]
    licence: str
    measured: bool
    basis: str


def measure(role: str, db_path: Optional[Path] = None) -> dict[str, ProviderStats]:
    """Per-provider stats for `role`, from the `genai_spans` tally.

    Reads the store `cost_usage_telemetry` writes and `record_routing_call` feeds. An absent
    store is an EMPTY measurement, not an error: before Half B runs there is legitimately
    nothing to measure, and that is a state the caller handles rather than a failure.
    """
    import json
    import sqlite3

    path = Path(db_path) if db_path is not None else _telemetry.default_db_path()
    if not Path(path).exists():
        return {}

    acc: dict[str, dict[str, Any]] = {}
    with sqlite3.connect(str(path)) as conn:
        try:
            rows = conn.execute(
                "SELECT gen_ai_system, attributes_json FROM genai_spans").fetchall()
        except sqlite3.DatabaseError:
            return {}
    for system, attrs_json in rows:
        attrs = json.loads(attrs_json)
        if attrs.get("devknowledge.role") != role:
            continue
        bucket = acc.setdefault(
            system, {"calls": 0, "passed": 0, "failed": 0, "unknown": 0, "cost": 0.0})
        bucket["calls"] += 1
        outcome = attrs.get("devknowledge.outcome")
        if outcome in ("passed", "failed", "unknown"):
            bucket[outcome] += 1
        bucket["cost"] += float(attrs.get("devknowledge.cost.estimated_usd") or 0.0)

    return {
        provider: ProviderStats(
            provider=provider,
            calls=b["calls"],
            judged=b["passed"] + b["failed"],
            passed=b["passed"],
            failed=b["failed"],
            unknown=b["unknown"],
            cost_usd=b["cost"],
        )
        for provider, b in acc.items()
    }


def rank_by_score(stats: dict[str, ProviderStats],
                  min_sample: int = DEFAULT_MIN_SAMPLE) -> list[str]:
    """Providers with a computable score and a sufficient sample, best first.

    Providers that are unscored or under-sampled are ABSENT from this list rather than pushed
    to the end — `rerank()` reinserts them at their declared positions, because "no measurement"
    is not the same claim as "measured worst" and the ordering must not conflate them.
    """
    scored = [s for s in stats.values() if s.score is not None and s.judged >= min_sample]
    return [s.provider for s in sorted(scored, key=lambda s: s.score, reverse=True)]


def rerank(
    role: str,
    repo: str,
    *,
    db_path: Optional[Path] = None,
    registry_path: Optional[Path] = None,
    manifest: Optional[Path] = None,
    min_sample: int = DEFAULT_MIN_SAMPLE,
) -> RerankResult:
    """Re-rank `role`'s eligible candidates by measured pass rate per cost — AX21-2.

    Returns the DECLARED order, unchanged and with `measured=False`, whenever measurement
    cannot support a reorder: a non-re-rankable role, an empty tally, or every provider under
    the sample floor. In each case `basis` says which, because the three are different facts
    and a caller that cannot tell them apart is back to a fixed list wearing a router's name.
    """
    spec = _role_spec(role, registry_path)
    declared = [c.provider for c in route(role, repo, registry_path=registry_path,
                                          manifest=manifest, strict=False)]
    stats = measure(role, db_path)

    if not spec.get("rerankable", True):
        return RerankResult(
            role=role, order=declared, measured=False, stats=stats,
            basis=("role is not rerankable (AX21-1: orchestration never routes to a cheaper "
                   "tier -- the one line of the role table not subject to re-ranking). The "
                   "declared order stands regardless of what the tally says"))

    relevant = {p: s for p, s in stats.items() if p in declared}
    if not any(s.calls for s in relevant.values()):
        return RerankResult(
            role=role, order=declared, measured=False, stats=stats,
            basis=("no measured calls for this role in the tally -- the declared order stands, "
                   "and it is DECLARED rather than confirmed. Half A places no calls "
                   "(AX23-2), so an empty tally is this arc's expected state"))

    ranked = rank_by_score(relevant, min_sample)
    if not ranked:
        judged = {p: s.judged for p, s in relevant.items() if s.calls}
        return RerankResult(
            role=role, order=declared, measured=False, stats=stats,
            basis=(f"every provider is below the minimum sample of {min_sample} (AX22-1's "
                   f"measurement window) or has no recorded cost to score against; judged "
                   f"counts: {judged}. Promoting on this would be ranking on noise while "
                   f"calling it measurement"))

    # Reinsert the unscored providers at their DECLARED positions rather than appending them.
    # Appending would encode "unmeasured is worse than measured-badly", which the data does not
    # say; holding position encodes "we learned nothing about this one", which it does.
    order: list[str] = []
    ranked_iter = iter(ranked)
    ranked_set = set(ranked)
    for provider in declared:
        order.append(next(ranked_iter) if provider in ranked_set else provider)

    return RerankResult(
        role=role, order=order, measured=True, stats=stats,
        basis=(f"re-ranked {len(ranked)} of {len(declared)} candidate(s) by measured pass rate "
               f"per cost over {sum(s.judged for s in relevant.values())} judged call(s); "
               f"providers with no score or fewer than {min_sample} judged calls held their "
               f"declared position"))


def admission_report(registry_path: Optional[Path] = None) -> list[AdmissionRow]:
    """Each provider's RECORDED admission state and licence — the contract's step 5, part two.

    *"Report each provider's recorded admission state ... and reporting it is not the same act
    as measuring it."* This reads the registry's recorded verdicts. It runs no trial task and
    contacts no provider, which is why `measured` is False on every row and why the basis says
    so: a report that did not say it could be mistaken for a measurement result.

    Licence rides alongside admission because the two gates are independent, and a report
    showing only one invites the wrong conclusion — copilot-enterprise is blocked on both, and
    an admission measurement would not clear its licence.
    """
    all_roles = _registry.roles(registry_path)
    licences = _registry.licences(registry_path)
    admitted: dict[str, list[str]] = {}
    not_admitted: dict[str, list[str]] = {}
    for role, spec in all_roles.items():
        for entry in spec.get("order") or []:
            provider = str(entry["provider"])
            bucket = admitted if _registry.is_admitted(entry) else not_admitted
            bucket.setdefault(provider, []).append(role)
            (not_admitted if bucket is admitted else admitted).setdefault(provider, [])

    return [
        AdmissionRow(
            provider=provider,
            admitted_in=sorted(admitted.get(provider, [])),
            not_admitted_in=sorted(not_admitted.get(provider, [])),
            licence=licences.get(provider, "unknown"),
            measured=False,
            basis=("recorded state, read from the registry. NOT a measurement: AX22-1's bar "
                   "(>= 8 of 10 tasks green on first review) is Half B's act, and reporting a "
                   "state is not the same act as measuring it"),
        )
        for provider in sorted(set(admitted) | set(not_admitted))
    ]


# --- CLI (done-contract item 4: "Click for a CLI where one is warranted") --------------------
#
# WARRANTED because step 5 asks for a REPORT, and a report needs a surface an operator can
# reach. Deliberately READ-ONLY: `report`, `route` and `rerank` print what the files and the
# tally say. There is no subcommand that admits a provider, edits the registry, or places a
# call -- admission is a measurement Half B performs, and a CLI flag that could grant it would
# be the "declared, not earned" failure AX21-2 names, one keystroke away.

try:
    import click
except ImportError:  # pragma: no cover - click is a declared dependency
    click = None


if click is not None:

    @click.group()
    def cli() -> None:
        """Read-only provider routing: who answers a role here, who is refused, and why."""

    @cli.command(name="report")
    @click.option("--registry", type=click.Path(path_type=Path), default=None)
    def _report(registry: Optional[Path]) -> None:
        """Each provider's RECORDED admission state and licence."""
        click.echo("Recorded admission state -- NOT a measurement (AX22-1's bar is Half B's).")
        click.echo("")
        for row in admission_report(registry):
            state = f"admitted in {row.admitted_in}" if row.admitted_in else "NOT ADMITTED"
            click.echo(f"  {row.provider:<22} {state:<34} licence: {row.licence}")

    @cli.command(name="route")
    @click.argument("role")
    @click.option("--repo", default=".dev-knowledge", show_default=True)
    @click.option("--produced-by", default=None)
    def _route(role: str, repo: str, produced_by: Optional[str]) -> None:
        """Who answers ROLE in --repo (provider, model, turns floor), and every candidate refused, with its reason."""
        for verdict in explain(role, repo, produced_by=produced_by):
            mark = "OK " if verdict.refusal is None else f"{verdict.refusal}:"
            model = verdict.model or "-"
            floor = (f"--max-turns >= {verdict.max_turns_floor} "
                     if verdict.max_turns_floor else "")
            click.echo(
                f"  [{verdict.position}] {verdict.provider:<22} {model:<22} "
                f"{floor}{mark} {verdict.reason}"
            )

    @cli.command(name="rerank")
    @click.argument("role")
    @click.option("--repo", default=".dev-knowledge", show_default=True)
    @click.option("--min-sample", default=DEFAULT_MIN_SAMPLE, show_default=True)
    def _rerank(role: str, repo: str, min_sample: int) -> None:
        """Re-rank ROLE by measured pass rate per cost, saying whether it measured anything."""
        result = rerank(role, repo, min_sample=min_sample)
        click.echo(f"  order   : {result.order}")
        click.echo(f"  measured: {result.measured}")
        click.echo(f"  basis   : {result.basis}")

else:  # pragma: no cover
    cli = None


__all__ = [
    "ADMISSION_GATED_ROLES",
    "AdmissionRow",
    "DEFAULT_MIN_SAMPLE",
    "ProviderStats",
    "RerankResult",
    "admission_report",
    "cli",
    "measure",
    "rank_by_score",
    "rerank",
    "main",
    "Candidate",
    "MANIFEST_PATH_ENV",
    "MANIFEST_RELPATH",
    "PERMITTING_LICENCE",
    "RouterRefusal",
    "Verdict",
    "allowlist",
    "declared_order",
    "explain",
    "manifest_path",
    "record_routing_call",
    "route",
]


def main() -> int:
    """CLI entrypoint. Read-only by construction — see the CLI section note."""
    if cli is None:  # pragma: no cover - click is a declared dependency
        raise RuntimeError(
            "click is not importable, so the CLI cannot run. It is a declared dependency "
            "(pyproject.toml); rebuild with `uv sync --locked`. The library half of this "
            "module does not need it and is unaffected."
        )
    # A refusal is a verdict, not a crash: one line on stderr and a non-zero exit, so
    # `route <unknown-role>` names the valid roles instead of printing a traceback.
    try:
        cli.main(standalone_mode=False)
    except RouterRefusal as exc:
        click.echo(f"refused: {' '.join(str(exc).split())}", err=True)
        return 2
    except click.exceptions.Abort:
        click.echo("aborted", err=True)
        return 1
    except click.ClickException as exc:
        exc.show()
        return exc.exit_code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
