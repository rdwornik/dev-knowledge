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
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

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
    spec = _registry.roles(registry_path).get(role)
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
        common = dict(provider=provider, model=model, position=position)

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

        if (gated or entry.get("requires_admission")) and not _registry.is_admitted(entry):
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

        if excludes_producer and produced_by is not None and provider == produced_by:
            verdicts.append(Verdict(
                **common, refusal="reviewer-is-producer",
                reason=(
                    f"provider `{provider}` produced the artifact under review (AX22-2: "
                    f"reviewer != producer, always). The registry sets excludes_producer on "
                    f"this role; the next eligible candidate in the declared order answers "
                    f"instead"
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
                       registry_path=registry_path, manifest=manifest)
    eligible = [
        Candidate(provider=v.provider, model=v.model, position=v.position)
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


__all__ = [
    "ADMISSION_GATED_ROLES",
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
