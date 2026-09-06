"""
audit.py — Ecosystem audit tool per ADR-36.

Reads child repos under Dev/ and writes only to .dev-knowledge paths.
Read-only contract: never touches child repo files (hard constraint, ADR-36).

This module is self-documenting: `python scripts/audit.py --help` and
`python scripts/audit.py <cmd> --help` are the authoritative CLI reference, and
`python scripts/audit.py checks` lists the registered checks straight from the
ALL_CHECKS registry (so the list cannot drift from what actually runs). The
conceptual / authority model — what this tool is, why the cross-repo `run` is
advisory while the self-audit `health` gates commits, and the self-only
enforcement model — lives in ARCHITECTURE.md (§"Validators and enforcement",
§"Authority and governance") and ADR-36. Do not re-narrate that here.

Commands:
    audit run                          # full ecosystem; writes report
    audit repo <name>                  # single repo
    audit registry update              # regenerate ecosystem/index.yaml
    audit health                       # quick TTY status, no file writes
    audit checks                       # list registered checks (from ALL_CHECKS)

Usage:
    python scripts/audit.py run
    python scripts/audit.py run --repo-path ../ai-council
    python scripts/audit.py repo ai-council
    python scripts/audit.py health
"""

from __future__ import annotations

import contextlib
import importlib.util
import inspect
import logging
import os
import re
import stat as _stat
import subprocess
import sys
import tempfile
import time
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Optional

import click
import yaml
from markdown_it import MarkdownIt

# The [#355] git-env scrub, single-sourced in the LEAF module `scripts/gitenv.py` ([#396]).
# Leaf = stdlib-only, ZERO repo imports, so this top-level import carries none of the
# import-path risk the LAZY fleet_parity import exists to avoid. Bound to its historical
# names at the original site below (search `_GIT_LOCATION_ENV_EXTRA`), where the note on
# WHERE the scrub fires — which this arc does not change — still lives.
#
# Loaded BY PATH, never by name. Both name-based spellings have a shadow hole that ends with
# the scrub silently becoming the EMPTY set, and ordering them only moves it -- full argument
# and the two reproductions are in gitenv.py's docstring (terra HIGH x3, 2026-08-08). A path
# load cannot be intercepted by any sys.path entry, and it is affordable only because gitenv
# is a leaf: executing it runs nothing else.
_gitenv_spec = importlib.util.spec_from_file_location(
    "dev_knowledge_gitenv", Path(__file__).resolve().with_name("gitenv.py"))
_gitenv = importlib.util.module_from_spec(_gitenv_spec)
_gitenv_spec.loader.exec_module(_gitenv)

# Resolve repo root (scripts/ sibling) — after imports
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPTS_DIR)

# Hub identity, decided in ONE place. `_REPO_ROOT` is derived live from __file__ so it always
# names THIS checkout; the `path` in ecosystem/<name>/state.yaml is absolute and committed, so
# it names the checkout that registered the repo. When the two disagree — a worktree, a cloud
# clone, a relocated repo — the hub resolved as not-the-hub and every hub-only check skipped
# silently ([#465] legs 2+3: the 2026-07-21 daily fell 16 WARNs → 2, the missing 14 being
# exactly the three hub-only checks). The comparison lives here and nowhere else so a new
# check cannot gate slightly differently; `resolve_repo_path` keeps the inputs honest.
HUB_REPO_NAME = ".dev-knowledge"


def _is_hub(repo_path) -> bool:
    """True when `repo_path` is the hub tree this audit.py belongs to."""
    try:
        return Path(repo_path).resolve() == Path(_REPO_ROOT).resolve()
    except OSError:  # an unresolvable path is never the hub; never wedge a check
        return False

# [#533] the generate_floor dual-import moved to audit_checks/check_floor_integrity.py,
# its only user; _FLOOR_F5 / _floor_sha256 are re-exported from there.

# #90 git↔backlog drift verifier — imported as a module so the check stays a thin
# adapter and tests can monkeypatch `_vgb.reconcile`. Same dual-import shape.
try:
    from scripts import validate_git_backlog as _vgb
except ImportError:
    import validate_git_backlog as _vgb

# #89 prose-vs-state checker — same module-import + thin-adapter shape as _vgb.
try:
    from scripts import validate_doc_claims as _vdc
except ImportError:
    import validate_doc_claims as _vdc

# #153 --no-ff merge guard — same module-import + thin-adapter shape as _vgb/_vdc.
try:
    from scripts import validate_no_ff as _vnf
except ImportError:
    import validate_no_ff as _vnf

# #163 handoff-probe teeth validator — same module-import + thin-adapter shape.
try:
    from scripts import verify_handoff_probes as _vhp
except ImportError:
    import verify_handoff_probes as _vhp

# [#529] Stage-1 telemetry EMIT — same module-import + thin-adapter shape as _vgb/_vdc/_vnf.
# The runner is the only consumer here (see `run_checks`); nothing in this module reads the
# library's `default_db_path()`, deliberately — see `_telemetry_db_path`.
try:
    from scripts import telemetry_emit as _te
except ImportError:
    import telemetry_emit as _te

# FM-5 governance-health — same module-import + thin-adapter shape. The `governance-health`
# subcommand below is the whole of this module's use of it: the derivations, the close-packet
# parsing and the telemetry record all live in the library, so `audit.py` gains a command and
# not a second implementation of anything.
try:
    from scripts import governance_health as _gh
except ImportError:
    import governance_health as _gh

# [#533] the assemble_paste dual-import moved to audit_checks/check_boot_byte_budget.py,
# its only user; _assemble_paste is re-exported from there.

# [#533] the validate_reconciliation dual-import moved to
# audit_checks/check_reconciled_versions.py, its only user; _vr is re-exported from there.

# #140 doc-rot / grooming checker — same module-import + thin-adapter shape.
try:
    from scripts import validate_doc_rot as _vdr
except ImportError:
    import validate_doc_rot as _vdr

# #194 doc→code declared-edge resolver — same module-import + thin-adapter shape.
try:
    from scripts import validate_doc_code_edge as _vdce
except ImportError:
    import validate_doc_code_edge as _vdce

# Prose structural linter (supplement organ #2) — same module-import + thin-adapter shape.
try:
    from scripts import validate_doc_structure as _vds
except ImportError:
    import validate_doc_structure as _vds

# [#533] the safe_remove dual-import moved to audit_checks/check_safe_removal.py,
# its only user; _sr is re-exported from there.

# [#533] the validate_residual_completeness dual-import moved to
# audit_checks/check_residual_completeness.py; _vrc is re-exported from there.

# [#436] silent-rule ratchet detector — the PINNED definition of the metric (regex + file
# filter + detector id). Same module-import + thin-adapter shape; the check is an adapter
# so the detector contract stays independently testable.
try:
    from scripts import silent_rule_detector as _srd
except ImportError:
    import silent_rule_detector as _srd

# M3 audit funnel-coverage detector -- the PINNED definition of the disposition predicate
# (ledger table shape + the ruled closed set + detector id). Same module-import + thin-adapter
# shape as _srd above; the check is an adapter so the detector contract stays independently
# testable (tests/test_funnel_coverage.py).
try:
    from scripts import funnel_coverage as _fc
except ImportError:
    import funnel_coverage as _fc

# FM-2 funnel-LIFECYCLE detector -- the sibling of _fc above and deliberately a separate
# module: _fc asks whether an audit artifact was DISPOSITIONED, this asks whether a governed
# object that reached a TERMINAL state actually left its live home. Same corpus for neither
# leg; same module-import + thin-adapter shape (tests/test_funnel_lifecycle.py).
try:
    from scripts import funnel_lifecycle as _fl
except ImportError:
    import funnel_lifecycle as _fl

# [#433]/C1 derived-tree coherence gate — the `tasks/` emitter, imported so the check can
# invoke its `--check` semantics in-process rather than shelling out. Same shape.
try:
    from scripts import gen_task_tree as _gtt
except ImportError:
    import gen_task_tree as _gtt

# [#383] wave-1 — the docs/intake/ residue-carrier gate (ADR-109 §4's generality proof).
# Same module-import + thin-adapter shape as the `tasks/` gate above.
try:
    from scripts import gen_intake_tree as _gint
except ImportError:
    import gen_intake_tree as _gint

# [#513] propagation-completeness landing-predicate scanner — same module-import + thin-adapter
# shape as the validators above; tests monkeypatch `_vlp.scan`.
try:
    from scripts import validate_landing_predicate as _vlp
except ImportError:
    import validate_landing_predicate as _vlp

# #179 undeclared-edge scan (Fable consult #1 ruling #2, 2026-07-03) — ship-gate WARN leg; same
# module-import + thin-adapter shape; tests monkeypatch `_sue.scan`.
try:
    from scripts import scan_undeclared_edges as _sue
except ImportError:
    import scan_undeclared_edges as _sue

# Canonical-freshness gate (enforcement-mesh, #236) — single-sourced so the SAME logic serves
# this audit leg AND the consumer-local pre-commit gate the mesh carrier deploys. audit-level
# aliases below keep the existing monkeypatch seam (tests set `_git_last_commit_date`).
try:
    from scripts import canonical_freshness_gate as _cfg
except ImportError:
    import canonical_freshness_gate as _cfg

# The canonical-doc-name registry (CLOUD-4 v2). `[#614]` HY-1 reads its `is_living_doc`
# predicate for the derived-freshness leg below. Same dual-mode shape as every sibling import
# here, for the same reason: `python scripts/audit.py` and `python -m scripts.audit` must
# resolve ONE spelling or the module ends up loaded twice under two sys.modules keys.
try:
    from scripts import canonical_docs as _cdocs
except ImportError:
    import canonical_docs as _cdocs

# Generated-artifact staleness leg (ADR-86 as amended 2026-08-23; `[#171]` leg 1 / f7). Exactly
# the relationship this module already has with `_cfg` above: the relation lives in ONE module,
# and the leg below only wraps its verdict in the Finding envelope. Dual-mode import for the
# same reason (`python scripts/audit.py` vs `python -m scripts.audit`).
try:
    from scripts import generated_artifact_freshness as _gaf
except ImportError:
    import generated_artifact_freshness as _gaf

# [#533] The decomposed check package. Every symbol moved out of this module is RE-EXPORTED
# below under its original name, so `audit.Finding`, `audit.check_vision_md`, `audit._strip_jsonc`
# … all still resolve, to the SAME objects. Live consumers of exactly this surface:
# scripts/{boundary_report,enforcement_coverage,fleet_analytics,gen_doc_counts,gen_handoff}.py,
# deploy/release_lint.py, and ~45 files under tests/.
#
# Same dual-import shape as the sibling validators above — `scripts.` first, bare second — so
# BOTH entry paths (`python scripts/audit.py`, `python -m scripts.audit`) resolve ONE spelling
# and the package cannot end up loaded twice under two sys.modules keys. The sibling-validator
# imports the extracted checks need (`generate_floor`, `validate_reconciliation`, `safe_remove`,
# `validate_residual_completeness`, `assemble_paste`) moved INTO those modules and are re-exported
# from there rather than imported again here: same try/except order → same sys.modules entry →
# `aud._sr` and the check's `_sr` are one object, which is what keeps
# `monkeypatch.setattr(aud._sr, ...)` working.
#
# WHY ONLY SOME CHECKS MOVED — the criterion is mechanical, stated in audit_checks/registry.py:
# a check is movable only if nothing in its transitive closure is monkeypatched onto THIS module
# by a test. 25 of 43 are not, `_is_hub`/`_REPO_ROOT` alone accounting for 19.
try:
    from scripts.audit_checks import registry as _registry
except ImportError:
    from audit_checks import registry as _registry

Finding = _registry.Finding
_NA_SUBJECT_ABSENT = _registry._NA_SUBJECT_ABSENT
_NA_NOT_APPLICABLE = _registry._NA_NOT_APPLICABLE
_NA_REASONS = _registry._NA_REASONS
_NA_REASON_RE = _registry._NA_REASON_RE
_na = _registry._na
_na_reason = _registry._na_reason
_BUNDLE_EXCLUDE_DIRS = _registry._BUNDLE_EXCLUDE_DIRS

check_vision_md = _registry.check_vision_md
check_adr38_baseline = _registry.check_adr38_baseline
check_adr_status_grammar = _registry.check_adr_status_grammar
check_claude_md = _registry.check_claude_md
check_dot_prefix_discipline = _registry.check_dot_prefix_discipline
check_canonical_md_visibility = _registry.check_canonical_md_visibility
check_workspace_settings = _registry.check_workspace_settings
check_handoff_bundle_structure = _registry.check_handoff_bundle_structure
check_canonical_structure = _registry.check_canonical_structure
check_handoff_version_stamp = _registry.check_handoff_version_stamp
check_amendment_coherence = _registry.check_amendment_coherence
check_floor_integrity = _registry.check_floor_integrity
check_substrate_declaration = _registry.check_substrate_declaration
check_dispatch_drift = _registry.check_dispatch_drift
check_routing_agreement = _registry.check_routing_agreement
check_consumer_at_landing = _registry.check_consumer_at_landing
check_proof_layer = _registry.check_proof_layer

_CONFIG_SUFFIXES = _registry._CONFIG_SUFFIXES
_DOT_PREFIX_EXCEPTIONS = _registry._DOT_PREFIX_EXCEPTIONS
_CANONICAL_MANDATORY = _registry._CANONICAL_MANDATORY
_CANONICAL_ALL = _registry._CANONICAL_ALL
_WORKSPACE_REQUIRED_SETTINGS = _registry._WORKSPACE_REQUIRED_SETTINGS
_strip_jsonc = _registry._strip_jsonc
_BUNDLE_BUDGETS = _registry._BUNDLE_BUDGETS
_BUNDLE_REQUIRED_FILES = _registry._BUNDLE_REQUIRED_FILES
_BUNDLE_STAMP_RE = _registry._BUNDLE_STAMP_RE
_CANONICAL_SPINE = _registry._CANONICAL_SPINE
_heading_present = _registry._heading_present
_STAMP_RE = _registry._STAMP_RE
_STAMP_FILES = _registry._STAMP_FILES
CoupledSet = _registry.CoupledSet
_COUPLED_VERSION_SETS = _registry._COUPLED_VERSION_SETS
_norm_version = _registry._norm_version
_FLOOR_MD_REF_RE = _registry._FLOOR_MD_REF_RE
_FLOOR_F5 = _registry._FLOOR_F5
_floor_sha256 = _registry._floor_sha256
check_reconciled_versions = _registry.check_reconciled_versions
check_residual_completeness = _registry.check_residual_completeness
check_safe_removal = _registry.check_safe_removal
check_routine_consumers = _registry.check_routine_consumers
check_boot_byte_budget = _registry.check_boot_byte_budget

_vr = _registry._vr
_vrc = _registry._vrc
_sr = _registry._sr
_assemble_paste = _registry._assemble_paste
_ROUTINE_MARKER_RE = _registry._ROUTINE_MARKER_RE
_ROUTINE_FIELD_RE = _registry._ROUTINE_FIELD_RE
_ROUTINE_TASK_RE = _registry._ROUTINE_TASK_RE
_ROUTINE_REQUIRED = _registry._ROUTINE_REQUIRED
_ROUTINE_LOOKALIKE_RE = _registry._ROUTINE_LOOKALIKE_RE
_ROUTINE_ANYFIELD_RE = _registry._ROUTINE_ANYFIELD_RE
_ROUTINE_FENCE_RE = _registry._ROUTINE_FENCE_RE
_ROUTINE_TICK_RUN_RE = _registry._ROUTINE_TICK_RUN_RE
_ROUTINE_INVISIBLE = _registry._ROUTINE_INVISIBLE
_ROUTINE_SENTINELS = _registry._ROUTINE_SENTINELS
_routine_code_spans = _registry._routine_code_spans
_routine_in_code = _registry._routine_in_code
_routine_value_is_named = _registry._routine_value_is_named

# ---------------------------------------------------------------------------
# Per-check gate tiers ([#597]) — the generalization that RETIRES `_GATE_MODE`
# ---------------------------------------------------------------------------
#
# `_GATE_MODE` was a module global that exactly TWO of 46 checks consulted (#89, and the
# ADR-86 freshness leg), so the other 44 spent their full ship-time cost on every commit.
# PERF-RECON B4 named it, and the module already said it about itself — `check_fleet_parity`
# carried "the walk is ~8s and ALL_CHECKS also runs on the per-commit audit-health gate;
# ship-gate-only scoping is a filed follow-up, not this arc". This is that follow-up.
#
# THE TIER IS A PROPERTY OF THE CHECK, not of the runner: declared inline in `ALL_CHECKS`,
# stamped onto the function, read by `run_checks`. That is what lets it travel with the
# deployed methodology corpus — a consumer repo inherits the tiers by taking the checks — where
# a module global could only ever describe one repo's runner.
#
# TWO TIERS, AND THE LADDER IS NESTED: commit ⊂ ship. `audit-health` (the pre-commit gate) runs
# the commit tier; `ship-gate`, `run` and `repo` run EVERYTHING. So no check is deleted from
# any gate here — it is moved to a later one, and ship-gate's finding stream is unchanged byte
# for byte. That is how [#597]'s own bar ("NO check is made faster by being made weaker") is met
# by construction rather than by assertion.
#
# WHY THERE IS NO `push` TIER, which [#597]'s row names alongside commit and integration: there
# is no push-stage ALL_CHECKS runner to put one in. The pre-push organs (`block_ff_push`,
# `block_unanchored_push`) are separate scripts that never call this module, so a third enum
# value would be inert on the day it landed — the exact class
# `detect_unconditionally_inert_checks` exists to refuse. The value lands with its consumer or
# not at all.
TIER_COMMIT = "commit"
TIER_SHIP = "ship"
GATE_TIERS = (TIER_COMMIT, TIER_SHIP)


def _tier(tier: str, check):
    """Stamp `check` with the gate tier it runs at and return it, so `ALL_CHECKS` declares the
    tier INLINE — one required positional argument per registry entry.

    Stamping the function rather than keying a side table on `__name__`: 16 of the 46 checks are
    defined in `scripts/audit_checks/`, and a name-keyed table would silently mis-tier a renamed
    check — the seam-detaches-silently class `audit_checks/registry.py` documents. An unknown
    tier RAISES at import, because a typo that degraded to a default would move a check off the
    commit gate with nobody noticing.
    """
    if tier not in GATE_TIERS:
        raise ValueError(f"unknown gate tier {tier!r} — expected one of {GATE_TIERS}")
    check.gate_tier = tier
    return check


def tier_of(check) -> str:
    """The tier `check` declared, defaulting to `TIER_COMMIT`.

    THE DEFAULT IS THE STRICT DIRECTION: an undeclared check runs EVERYWHERE, so silence costs
    wall time and never coverage. It is not a licence to omit the declaration —
    `tests/test_audit.py::test_every_all_checks_member_declares_a_gate_tier` refuses an
    undeclared `ALL_CHECKS` member, so a check added without a tier REDs the suite instead of
    quietly joining the commit gate. The default exists for the OTHER caller: a test that
    monkeypatches `ALL_CHECKS` down to a bare sentinel must not have to know about tiers.
    """
    declared = getattr(check, "gate_tier", TIER_COMMIT)
    return declared if declared in GATE_TIERS else TIER_COMMIT


def runs_at_tier(check, tier: str | None) -> bool:
    """Does `check` run when the runner is invoked at `tier`? `None` means "run everything".

    A SUBSET TEST, NEVER EQUALITY. The ladder is nested, so `ship` runs the commit tier too;
    written as `tier_of(check) == tier` this would make `ship-gate` skip every commit-tier
    check — the exact inverse of what a ship gate is for, and it would pass a naive test that
    only ever exercised the commit path.

    AN UNKNOWN RUNNER TIER RAISES (terra HIGH, 2026-08-27). This function used to treat any
    string it did not recognise as the commit tier, so `run_checks(tier="shp")` would have
    silently deferred all ten ship-tier checks and reported a GREEN, incomplete gate. That is
    the same fail-loud contract `_tier` enforces on the declaration side, and it was
    inconsistent for the runner side to be permissive about the identical typo.
    """
    if tier is None:
        return True
    if tier not in GATE_TIERS:
        raise ValueError(f"unknown runner tier {tier!r} — expected None or one of {GATE_TIERS}")
    if tier == TIER_SHIP:
        return True
    return tier_of(check) == TIER_COMMIT

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("audit")

# [#529] MEASURED, and this line is the whole fix. `basicConfig` above routes INFO to STDERR,
# and `telemetry_emit._log_event` mirrors every event onto logger "telemetry" at INFO — so a
# wired `audit.py health` would add ONE `telemetry: {...}` stderr line per check, 43 per run, on
# the gate that fires on every commit. The counter-measure sits adjacent to the line that causes
# it because the pair is only readable together.
#
# CALLER-SIDE ON PURPOSE. `telemetry_emit` does not have this defect: a hook that imports it
# configures no handler at all, so `logging.lastResort` (WARNING) already keeps hook stderr
# byte-clean — measured, both directions. Fixing it in the library would touch
# `test_emit_survives_an_unusable_log_side_channel` and
# `test_logger_backend_reports_which_side_channel_is_live` for a defect the library does not
# have. The durable record is the SQLite row either way; this suppresses the side channel, not
# the event. A caller that wants the side channel back sets the level back.
logging.getLogger("telemetry").setLevel(logging.WARNING)

ECOSYSTEM_DIR = Path(_REPO_ROOT) / "ecosystem"
AUDITS_DIR = Path(_REPO_ROOT) / "docs" / "audits"
ECOSYSTEM_INDEX = Path(_REPO_ROOT) / "ecosystem" / "index.yaml"
# #147 ship-gate: the known-WARN disposition register (read-only). Missing/malformed
# -> [] (every WARN then counts undispositioned — stricter, never wedged).
DISPOSITION_REGISTER = Path(_REPO_ROOT) / "ecosystem" / "disposition-register.yaml"
# ADR-91: the durable per-repo deployed-methodology-version registry (COMMITTED, hand/
# deploy-runbook-written; read-only here). Hub-resolved (a module constant, NOT repo_path) --
# it is ONE hub file read for whichever repo is being audited; check_deployed_methodology_version
# looks up the audited repo by its directory name. Missing/malformed -> WARN (never wedges).
DEPLOYED_VERSIONS_REGISTRY = Path(_REPO_ROOT) / "ecosystem" / "deployed-versions.yaml"

# ---------------------------------------------------------------------------
# Universal visual pattern (ADR-59) — constants
# ---------------------------------------------------------------------------
# [#533] _CONFIG_SUFFIXES / _DOT_PREFIX_EXCEPTIONS / _CANONICAL_MANDATORY / _CANONICAL_ALL
# travelled with the checks that exclusively own them — re-exported above.

# Canonical living docs subject to the freshness cadence (check #10; operationalizes
# the ADR-39 "grooming" lifecycle element). PORTABLE: a child repo inherits this list
# unchanged — "CLAUDE.md" resolves to that repo's own project CLAUDE.md. Append-only
# files (JOURNAL/LESSONS) and the per-session BACKLOG are deliberately EXCLUDED: their
# freshness is intrinsic to how they are written, so an edit-since-review signal would
# fire every session by design.
# Single-sourced in scripts/canonical_freshness_gate.py (deployed consumer-local by the mesh
# carrier). Aliased here so audit.py + its importers (enforcement_coverage, tests) keep the name.
# The PORTABLE base (DEFAULT_FRESHNESS_FILES) is what a consumer inherits verbatim via the deployed
# canonical_freshness gate; the HUB-ONLY extras are hub governance docs under protocols/ that do NOT
# exist in a consumer (so they'd be skipped there anyway) and are gated only here, where audit.py
# runs (audit.py is hub-only). Added per the 2026-07-08 fleet-census A-2 ruling — PLAYBOOK is the
# largest ungated canonical doc but is DEFERRED (no last_reviewed frontmatter yet + a genuine
# end-to-end re-read is its own arc; see BACKLOG). SESSION_SETUP + AI_COUNCIL_PROCESS were genuinely
# re-read and stamped in that arc, so they join now.
# DEFINITION_OF_DONE.md joined 2026-08-06 ([#503]): it is hub-only (absent from every deploy
# manifest), carries a `last_reviewed` stamp, and was the gap's own proof — the ADR-85 amendment
# 2026-08-03 rewrote its teeth while its stamp stayed at 2026-06-19 and no edit-keyed signal fired.
_HUB_ONLY_FRESHNESS_FILES = ["protocols/SESSION_SETUP.md", "protocols/AI_COUNCIL_PROCESS.md",
                             "protocols/DEFINITION_OF_DONE.md"]
_FRESHNESS_FILES = _cfg.DEFAULT_FRESHNESS_FILES + _HUB_ONLY_FRESHNESS_FILES
_FRESHNESS_CADENCE_DAYS = _cfg.FRESHNESS_CADENCE_DAYS

# [#533] _WORKSPACE_REQUIRED_SETTINGS + _strip_jsonc travelled with
# check_workspace_settings, their only user — re-exported above.

# ---------------------------------------------------------------------------
# State schema
# ---------------------------------------------------------------------------

@dataclass
class RepoState:
    """A repo's last audit result — the schema of ecosystem/<name>/state.yaml.

    Fields (round-tripped by to_dict/from_dict): `name` (matches the
    ecosystem/<name>/ folder), `path` (absolute path stored at registration),
    `last_audit` (ISO date of the last run, or None if never audited), and
    `findings` — a list of Finding(check_name, status, evidence) where status is
    one of pass | fail | warn | unavailable | n/a. state.yaml is the per-repo source of
    truth; ecosystem/index.yaml is a derived rollup of these (see regenerate_index).
    """
    name: str
    path: str
    last_audit: Optional[str]
    findings: list[Finding] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "last_audit": self.last_audit,
            "findings": [
                {"check_name": f.check_name, "status": f.status, "evidence": f.evidence}
                for f in self.findings
            ],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RepoState":
        findings = [
            Finding(f["check_name"], f["status"], f["evidence"])
            for f in d.get("findings", [])
        ]
        return cls(
            name=d["name"],
            path=d["path"],
            last_audit=d.get("last_audit"),
            findings=findings,
        )


def _state_path(repo_name: str) -> Path:
    return ECOSYSTEM_DIR / repo_name / "state.yaml"


def _history_path(repo_name: str, run_date: date) -> Path:
    return ECOSYSTEM_DIR / repo_name / "history" / f"{run_date.isoformat()}.md"


def load_state(repo_name: str) -> Optional[RepoState]:
    p = _state_path(repo_name)
    if not p.exists():
        return None
    with open(p, encoding="utf-8") as fh:
        d = yaml.safe_load(fh)
    return RepoState.from_dict(d)


def save_state(state: RepoState) -> None:
    p = _state_path(state.name)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        yaml.dump(state.to_dict(), fh, default_flow_style=False, allow_unicode=True)


_HISTORY_ROW_RE = re.compile(r"^\|\s*([a-z0-9_]+)\s*\|")


def _previously_reported_checks(repo_name: str, upto: date) -> set[str]:
    """Check names in the single most recent history READING at or before `upto`.

    Two details are load-bearing (terra HIGH, 2026-08-04):

    * SAME-DAY entries count. An earlier version compared strictly against an EARLIER DATE, so
      a second `run` on the same day compared against yesterday and re-emitted a retirement
      notice the first run had already recorded — writing a false "retired since the previous
      reading" into the durable history on every rerun.
    * Only the LAST table in that file is parsed. A history file accumulates appended readings,
      so unioning all of them would resurrect names retired several readings ago and suppress
      the notice for a check that vanished today.

    Derived from the history files themselves — there is deliberately no retired-check registry
    to maintain (FR-4). Empty when there is no prior reading, so a repo's first ever run
    correctly reports nothing retired rather than everything.
    """
    hist = ECOSYSTEM_DIR / repo_name / "history"
    if not hist.is_dir():
        return set()
    prior = sorted(p for p in hist.glob("*.md") if p.stem <= upto.isoformat())
    if not prior:
        return set()
    text = prior[-1].read_text(encoding="utf-8", errors="replace")
    last_reading = text.rsplit("\n## ", 1)[-1]
    names = {m.group(1) for m in (_HISTORY_ROW_RE.match(ln)
                                  for ln in last_reading.splitlines()) if m}
    # An UNAVAILABLE repo's reading is a single `availability` row, and an aborted append can
    # leave a partial table. Neither is a complete reading, and treating one as complete would
    # announce every check the repo normally runs as "retired" in the next daily -- a false
    # entry written into the durable history (terra HIGH r2, 2026-08-04). None means "cannot
    # compare", which the caller renders as an explicit unavailable notice rather than silence.
    if not names or names == {"availability"}:
        return None
    return names


def append_history(state: RepoState, run_date: date) -> None:
    p = _history_path(state.name, run_date)
    p.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().isoformat(timespec="seconds")
    lines = [f"## {run_date.isoformat()} — {ts}\n\n"]

    # [#465] leg 4 / FR-5: a retired check must be visible TO A READER OF THE DAILIES, not only
    # in a commit message. Without this, a check simply stops appearing and the row's absence is
    # indistinguishable from a run that never reached it -- the same invisibility that let
    # `handoff_tag_canonicity` emit a verdict for two spec generations after its subject died.
    # Best-effort by design: this is a NOTICE, and a notice must never be able to fail the write
    # of the daily it annotates. It is never silent, though -- a comparison that cannot run says so.
    try:
        previous = _previously_reported_checks(state.name, run_date)
        if previous is None:
            lines.append("> **Retirement comparison unavailable** — the previous reading was "
                         "absent, unavailable, or partial, so a missing row below cannot be "
                         "read as a retirement.\n\n")
        else:
            gone = sorted(previous - {f.check_name for f in state.findings})
            if gone:
                lines.append(f"> **Checks retired since the previous reading:** "
                             f"{', '.join(gone)}. No longer in ALL_CHECKS; their absence below "
                             "is deliberate.\n\n")
    except Exception as exc:  # noqa: BLE001 -- notice only; never blocks the daily
        lines.append(f"> **Retirement comparison unavailable** ({exc!r}) — a missing row below "
                     "cannot be read as a retirement.\n\n")

    lines.append("| Check | Status | Evidence |\n|---|---|---|\n")
    for f in state.findings:
        lines.append(f"| {f.check_name} | {f.status} | {f.evidence} |\n")
    lines.append("\n")
    with open(p, "a", encoding="utf-8") as fh:
        fh.writelines(lines)


# Consumer-root resolution ([#605]) — the same precedence, env vars and registry file as
# `deploy/tool.py::resolve_repo_root`, which states it in full above its own resolver.
# The two are deliberately NOT folded: deploy/ and scripts/ are separate import roots, and
# audit.py is the `audit-health` pre-commit gate — it must not pull in tool.py's
# click/rich/carrier graph to answer where a repo is. [#605] was ruled KEPT SEPARATE from
# [#294] for the same reason. Duplicated CONSTANTS with a shared name are what makes the
# two modules agree; a fold, if ever wanted, is a deliberate act with its own reason.
FLEET_ROOT_ENV = "DEV_KNOWLEDGE_FLEET_ROOT"
REPO_ROOT_ENV_PREFIX = "DEV_KNOWLEDGE_REPO_ROOT_"


def repo_root_env_var(repo_name: str) -> str:
    """The env-var name carrying an explicit working-tree path for `repo_name`.

    `ai-council` -> `DEV_KNOWLEDGE_REPO_ROOT_AI_COUNCIL`. Derived from the registry key
    rather than listed, so a newly registered consumer needs no code change.
    """
    slug = re.sub(r"[^A-Za-z0-9]+", "_", repo_name).strip("_").upper()
    return f"{REPO_ROOT_ENV_PREFIX}{slug}"


def resolve_repo_path(
    repo_name: str,
    stored_path: Optional[str],
    *,
    explicit: Optional[str] = None,
    env: Optional[Mapping[str, str]] = None,
) -> Path:
    """The tree to audit for `repo_name` — the seam where the hub finds itself.

    The hub always audits the tree audit.py lives in, never the absolute path committed to
    its state.yaml: that value is machine- and checkout-specific, so from any other tree the
    hub failed to recognise itself and every hub-only check skipped as `n/a` ([#465]).

    For a CONSUMER, resolution is an explicit precedence, sibling-LAST ([#605]):

    1. `explicit` — `audit repo <name> --repo-path <path>`;
    2. `DEV_KNOWLEDGE_REPO_ROOT_<SLUG>` — the substrate-portable override, and the step
       that makes `audit repo <name>` runnable from a checkout with NO sibling tree;
    3. `stored_path` — `path:` from `ecosystem/<repo>/state.yaml`, the fleet's per-repo
       path registry. It is gitignored (machine-specific), so on a fresh checkout it says
       nothing, which is exactly why steps 1-2 exist rather than this one being enough;
    4. the sibling default `<dev>/<repo>`, where `<dev>` is `DEV_KNOWLEDGE_FLEET_ROOT`
       when set and `_REPO_ROOT.parent` otherwise.

    `explicit` is checked before the hub short-circuit because `--repo-path` already
    outranked it at the CLI; `env` and the registry are NOT, so no environment can undo
    the [#465] binding of the hub to its live tree.

    With no override set, a consumer resolves exactly as it did before [#605].
    """
    environ = os.environ if env is None else env
    if explicit:
        return Path(explicit).resolve()
    if repo_name == HUB_REPO_NAME:
        return Path(_REPO_ROOT)
    from_env = environ.get(repo_root_env_var(repo_name), "").strip()
    if from_env:
        return Path(from_env).resolve()
    if stored_path:
        return Path(stored_path)
    fleet_root = environ.get(FLEET_ROOT_ENV, "").strip()
    parent = Path(fleet_root) if fleet_root else Path(_REPO_ROOT).parent
    return parent / repo_name


def discover_repos() -> list[str]:
    """Return repo names registered in ecosystem/ (by state.yaml presence)."""
    if not ECOSYSTEM_DIR.exists():
        return []
    return [
        d.name
        for d in sorted(ECOSYSTEM_DIR.iterdir())
        if d.is_dir() and (d / "state.yaml").exists()
    ]

# ---------------------------------------------------------------------------
# Audit checks
# ---------------------------------------------------------------------------

# [#533] moved to audit_checks/ — re-exported above.


# check_mermaid_theme_directive (check #7, ADR-51 v2) RETIRED by ADR-51 amendment
# 2026-07-05: canonical docs are LLM-first — Mermaid left them, so the theme standard
# is re-scoped to the visualization surface, unenforced by audit. No replacement
# check asserts Mermaid ABSENCE: child repos carry legacy-form codemaps until their
# per-repo migration (root-scheduled), and a presence-ban would red every child.


# [#533] moved to audit_checks/ — re-exported above.


# Single-sourced in canonical_freshness_gate.py; audit-level aliases keep the monkeypatch seam
# (tests set `aud._git_last_commit_date` / `aud._parse_last_reviewed`; check_canonical_freshness
# passes these names into `_cfg.evaluate`, so a monkeypatch at the audit level still applies).
_parse_last_reviewed = _cfg.parse_last_reviewed
_git_last_commit_date = _cfg.git_last_commit_date
# Audit-level alias for the same reason the two above exist: it keeps a monkeypatch seam, so a
# test that rewrites the name on the `audit` module still reaches the leg.
_gaf_git_last_commit_date = _gaf.git_last_commit_date


# ---------------------------------------------------------------------------
# Freshness DERIVED from git, for every living doc (`[#614]` batch-E HY-1)
# ---------------------------------------------------------------------------
#
# WHAT IT REPLACES. `last_reviewed` is a hand-typed date, and a hand-maintained date lies by
# construction — its failure mode is not that it is wrong but that NOTHING binds the assertion
# to the artifact reviewed. The A1/A2 legs above compare that date to `git log -1`, which buys
# two things and misses three:
#
#   it catches   a stamp older than the file's newest commit, on the NINE files someone
#                remembered to enrol in `_FRESHNESS_FILES`;
#   it misses    (a) same-day drift — `%as` is DAY-granular and `evaluate()` fails only when
#                    `reviewed < git_date`, so content committed LATER THE SAME DAY as the
#                    stamp passes. `docs/audits/2026-08-31-census-doc-freshness-derivation.md`
#                    §3 measured 4 of the 9 GATED files carrying unreviewed content the gate
#                    scores fresh — including the CLAUDE.md re-genre that deleted 15,657 bytes,
#                    40% of the file, after the stamp asserting it had been read end-to-end;
#                (b) the whole UNGATED class — 4 living docs stale, 2 to 53 days, watched by
#                    nothing;
#                (c) the 26 living docs carrying NO stamp at all, the largest class, which the
#                    A1/A2 leg turns into one undifferentiated WARN per file and never itemises.
#
# THE DERIVATION IS ADDITIVE, and that is A4's single most important constraint on this leg.
# `last_reviewed := last_commit_date` is NOT a review stamp — it is an mtime, and it would
# report every file permanently fresh, because derivation measures EDITS and a review that
# changes nothing leaves no commit. So the explicit reviewer record stays; what is derived is
# the COMPARISON TARGET — the date of the last commit that actually changed the doc's content.
#
# HONEST LIMITS, stated here rather than discovered later:
#   * It measures edits against a review, never CONTENT against a decision. A doc fully current
#     against git can be badly drifted against a new ADR that never touched its bytes — the
#     same limit `check_canonical_freshness` already states for A2, unchanged by derivation.
#   * `--name-only` reports no paths for a merge commit (git shows no diff for merges by
#     default), so a conflict RESOLUTION that only exists in a merge commit is invisible here.
#     That biases toward under-reporting on merge-resolved edits; it is the one direction this
#     leg is not conservative in, and it is named rather than hidden.
#   * The commit walk follows the CURRENT path. A doc renamed in its history dates from the
#     rename, not from before it — exactly what `git log -1` already did.

SURFACE_FRONTMATTER = "frontmatter"
SURFACE_PROSE = "prose"
SURFACE_NONE = "none"

# The TOUCH predicates, and the enum is STRUCTURAL ONLY — there is deliberately no fourth
# "mechanical regeneration" predicate keyed on the commit SUBJECT. A4's design draft carried
# one and then ruled it out of anything shipped, because under derivation a misclassification
# silently marks a doc FRESH, and a commit subject is author-controlled free text: keying a
# freshness verdict on it hands the author a one-line way to buy the verdict. Structural
# predicates cost more false-STALE, which is the safe direction.
TOUCH_WHITESPACE = "whitespace-only"        # T1 - empty under whitespace-blindness
TOUCH_FRONTMATTER = "frontmatter-only"      # T2 - the re-stamp / version-bump commit
TOUCH_STAMP_LINE = "stamp-line-only"        # T3 - a prose stamp bump outside frontmatter

# The classes A4 §3 separates. The THIRD is what funds this leg: it is the part no gate
# watches. The fifth is not a class A4 names — it is the residue that makes the partition
# total, so every living doc lands in exactly one bucket and none is silently unreported.
CLASS_GATED_STALE = "gated-and-stale"
CLASS_GATED_FRESH = "gated-and-fresh"
CLASS_UNGATED_STALE = "ungated-and-stale"
CLASS_UNGATED_FRESH = "ungated-and-fresh"
CLASS_UNSTAMPED = "ungated-and-unstamped"

# How far back the TOUCH walk goes before it gives up and reports the newest commit instead.
# A cap is needed because the walk is unbounded in principle; 25 is far past the longest TOUCH
# run measured (A4: 16 TOUCH commits on ARCHITECTURE.md across 167, and never consecutive).
# Exhausting it over-reports staleness, which is the safe direction, and says so in the row.
_DERIVED_WALK_CAP = 25

# `> Last updated: 2026-08-01` (PLAYBOOK, ENVIRONMENT) and `**Last updated:** 2026-08-26`
# (CLAUDE.md's footer, OPERATOR-INTERFACE). A4 admitted the prose surface deliberately: THREE
# of the four ungated-stale docs declare only in prose, so without it PLAYBOOK -- this leg's
# own subject -- has no declared value to compare and would misreport as unstamped.
_PROSE_STAMP_RE = re.compile(
    r"^[>\s]*(?:\*\*)?Last updated:?(?:\*\*)?\s*:?\s*(\d{4}-\d{2}-\d{2})",
    re.IGNORECASE | re.MULTILINE)

# T3's line grammar. Deliberately NARROW -- the four keys A4 measured, nothing widened to
# `status:`/`owner:`/`effective:`. A wider grammar excuses more commits as TOUCH, and every
# commit wrongly excused is a doc reported fresh that nobody read.
_STAMP_LINE_RE = re.compile(
    r"^\s*(?:<!--\s*)?(?:>\s*)?(?:[-*]\s+)?(?:\*\*)?"
    r"(?:last_reviewed|reconciled_with|version|last updated)"
    r"(?:\*\*)?\s*:", re.IGNORECASE)

# `@@ -old,oldcount +new,newcount @@` with `--unified=0`; the counts are omitted when 1.
_HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")

# Could this changed line possibly BE a frontmatter line? `---`, or a YAML `key:` mapping.
# A cheap, SOUND pre-filter for T2 -- see `_classify_touch` for why it earns its place.
_YAML_ISH_RE = re.compile(r"^\s*(?:---\s*$|[A-Za-z_][A-Za-z0-9_.-]*\s*:)")

# The two PROSE version spellings: `Version: 6.3.0` (HANDOFF_PROCESS) and the
# `<!-- version: 2.69 - ... -->` sentinel (CLAUDE.md). The frontmatter spellings are read
# through the YAML parse instead of by regex, so a `version:` line inside a fenced code block
# further down the file cannot be mistaken for the doc's own version claim.
_PROSE_VERSION_RES = (
    re.compile(r"^Version:\s*(\S+)\s*$", re.MULTILINE),
    re.compile(r"^<!--\s*version:\s*(\S+)", re.MULTILINE | re.IGNORECASE),
)


class DerivationUnavailable(RuntimeError):
    """The ground truth does not exist here — no git, or not a git repo.

    A LEGITIMATE `n/a`: a non-git consumer has no commit history to derive from, and saying so
    is a true answer. Distinct from `DerivationRefused` below, and the distinction is the whole
    point of having two exceptions."""


class DerivationRefused(RuntimeError):
    """The ground truth EXISTS and is lying — the clone is shallow.

    Rendered `fail`, never `unavailable`, on the Z-G4 rule `check_intake_lifecycle` states:
    `_STATUS_LABEL` renders `unavailable` as "N/A" and `_check_outcome` projects it onto `pass`,
    so an unavailable verdict SHIPS GREEN having measured nothing. A4 witnessed this failure
    live — under a graft at 2026-08-25 its own first pass mis-dated `protocols/ESSENTIALS.md`
    and 14 other files, silently. A date compare degrades quietly on a shallow clone; a
    history-walking derivation must refuse instead."""


@dataclass(frozen=True)
class DocFreshness:
    """One living doc's declared-vs-derived freshness row. The doctrine table's record type."""
    path: str
    declared: Optional[date]
    surface: str
    derived: Optional[date]
    derived_sha: Optional[str]
    touch_skipped: int
    refined: bool
    gated: bool
    version: Optional[str]
    doc_class: str
    stamp_sha: Optional[str] = None      # the commit that SET the current declared stamp
    unreviewed_after_stamp: int = 0      # CONTENT commits ordered after it - the same-day hole

    @property
    def delta_days(self) -> Optional[int]:
        """Derived minus declared, in days. Positive = content is newer than its review."""
        if self.declared is None or self.derived is None:
            return None
        return (self.derived - self.declared).days

    def brief(self) -> str:
        """The short form the GATE lists members with -- path plus the one number that names
        the problem. The full `row()` is the on-demand `audit.py doc-freshness` surface: a
        Finding whose evidence carries 26 full rows renders as one unreadable table cell in
        every daily, and the point of listing the unstamped class is that a reader can SEE
        which docs are in it."""
        if self.declared is None:
            return (f"{self.path} (no stamp; last content "
                    f"{self.derived.isoformat() if self.derived else '-'})")
        if self.unreviewed_after_stamp:
            return (f"{self.path} (declared {self.declared.isoformat()} [{self.surface}] at "
                    f"{(self.stamp_sha or '-')[:9]}; {self.unreviewed_after_stamp} CONTENT "
                    f"commit(s) landed AFTER it on the same date - invisible to the date "
                    f"compare)")
        return (f"{self.path} (declared {self.declared.isoformat()} [{self.surface}] -> derived "
                f"{self.derived.isoformat() if self.derived else '-'}, +{self.delta_days}d)")

    def row(self) -> str:
        """One flat, pipe-free line. Pipe-free is a CONTRACT, not a style choice:
        `Finding.evidence` is markdown-table-safe and every emitter replaces `|` with `/`."""
        delta = self.delta_days
        after = (f"{self.unreviewed_after_stamp} unreviewed after stamp "
                 f"{(self.stamp_sha or '-')[:9]}  ") if self.unreviewed_after_stamp else ""
        return (
            f"{self.path}  version {self.version or '-'}  "
            f"declared {self.declared.isoformat() if self.declared else '-'} ({self.surface})  "
            f"derived {self.derived.isoformat() if self.derived else '-'} "
            f"({(self.derived_sha or '-')[:9]}{'' if self.refined else ', unrefined'}"
            f"{f', {self.touch_skipped} touch skipped' if self.touch_skipped else ''})  "
            f"{'+' if delta and delta > 0 else ''}{'-' if delta is None else delta}d  "
            f"{after}{self.doc_class}"
        ).replace("|", "/")


def parse_declared_freshness(text: str) -> tuple[Optional[date], str]:
    """The date a doc DECLARES it was last reviewed, and which surface declared it.

    Two surfaces exist and they are NOT interchangeable: frontmatter `last_reviewed` is
    machine-readable and gated, a prose `> Last updated:` line is neither. Frontmatter WINS
    where both are present (CLAUDE.md carries both; they agree today and nothing enforces that
    they ever will) — the gated surface is the one the repo has committed to.
    """
    reviewed = _parse_last_reviewed(text)
    if reviewed is not None:
        return reviewed, SURFACE_FRONTMATTER
    m = _PROSE_STAMP_RE.search(text)
    if m:
        try:
            return date.fromisoformat(m.group(1)), SURFACE_PROSE
        except ValueError:
            return None, SURFACE_NONE
    return None, SURFACE_NONE


def _frontmatter_map(text: str) -> dict:
    """A doc's YAML frontmatter as a mapping, or `{}` for anything unparseable.

    Same tolerant contract as `canonical_freshness_gate.parse_last_reviewed`: no frontmatter,
    an unclosed fence, a non-mapping body or a YAML error all mean "nothing declared here",
    never an exception — a malformed header must not wedge a whole audit run.
    """
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return {}
    return fm if isinstance(fm, dict) else {}


def parse_declared_version(text: str) -> Optional[str]:
    """The version a doctrine doc declares, or None.

    A DOC'S OWN VERSION OUTRANKS THE SPEC IT RECONCILES AGAINST, and the order matters for the
    doctrine table: `reconciled_with: handoff-process@6.3.0` says which SPEC generation this doc
    has been re-reasoned against — a real claim the `reconciled_versions` check gates — but it
    is not this doc's version. Reading it first made CLAUDE.md render as `handoff-process@6.3.0`
    when its own version is 2.69. So: own version (frontmatter, then the two prose spellings)
    first, `reconciled_with` only as the fallback for a doc that carries no version of its own.

    A PROSE VERSION IS READ FROM THE HEADER ONLY -- everything above the first `## ` heading.
    A doc's own version is a header fact, and the whole-file search this started as read
    `protocols/PLAYBOOK.md` as version `1.0`: PLAYBOOK carries per-SECTION
    `<!-- version: 1.0 - 2026-04-26 -->` sentinels from line 477 down, and the first of them
    won. The `## H2` boundary is the same structural line `CANONICAL_SPINE` keys on, not a
    magic line count.
    """
    fm = _frontmatter_map(text)
    own = fm.get("version")
    if own is not None:
        return str(own)
    header = re.split(r"^## ", text, maxsplit=1, flags=re.MULTILINE)[0]
    for pattern in _PROSE_VERSION_RES:
        m = pattern.search(header)
        if m:
            return m.group(1)
    reconciled = fm.get("reconciled_with")
    return str(reconciled) if reconciled is not None else None


def _derive_git(repo_path, args: list[str]) -> Optional[str]:
    """One read-only git call under the [#396] location scrub, or None on any failure.

    The scrub is not optional here: an inherited `GIT_DIR` overrides BOTH `cwd=` and `git -C`,
    so without it this leg would date the PARENT repo's files while labelling the answer with
    the target's paths — the [#355] class `gitenv.py` exists to close.
    """
    scrub = _git_location_env()
    env = {k: v for k, v in os.environ.items() if k not in scrub}
    try:
        p = subprocess.run(["git", "-C", str(repo_path), *args], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", env=env)
    except OSError:
        return None
    return p.stdout if p.returncode == 0 else None


def _git_is_shallow(repo_path) -> Optional[bool]:
    """True/False for a resolvable git repo; None when git is absent or this is not a repo."""
    out = _derive_git(repo_path, ["rev-parse", "--is-shallow-repository"])
    return None if out is None else out.strip() == "true"


def _living_doc_paths(repo_path) -> list[str]:
    """Tracked `.md` files this repo's registry classes as living docs, sorted.

    Enumerated from `git ls-files`, filtered by the registry predicate — so the SET is git's
    answer and the MEMBERSHIP RULE is `canonical_docs`'s, and neither is a list typed into a
    doc that goes stale at the next commit.

    FLEET-WIDE, NOT HUB-ONLY, AND THAT IS MEASURED RATHER THAN ASSUMED. The worry with a
    default-INCLUDE predicate is a consumer whose tree is mostly markdown: the leg would then
    enumerate hundreds of files and drown its own finding. Measured 2026-08-31 on the operator's
    disk, tracked `.md` -> living docs: corp-monorepo 202 -> 28, ai-council 149 -> 14,
    win-tooling 28 -> 20, with the batched log at 0.26-0.47 s each. The `docs/` and `tests/`
    exclusions do the work, so no hub-only carve-out is needed and the leg travels with the
    check the way `_FRESHNESS_FILES` already does.
    """
    out = _derive_git(repo_path, ["ls-files", "--", "*.md"])
    if out is None:
        return []
    return sorted(p for p in out.splitlines() if p and _cdocs.is_living_doc(p))


@dataclass(frozen=True)
class _CommitDiff:
    """One commit's `--unified=0 -w` diff of ONE path — everything T1/T3 need, pre-parsed."""
    sha: str
    when: date
    hunks: tuple[tuple[int, int, int, int], ...]     # old_start, old_count, new_start, new_count
    changed: tuple[str, ...]                          # the +/- lines, sign included
    created: bool                                     # a new-file or deleted-file commit


def _parse_unified_zero(body: str) -> tuple[tuple, tuple, bool]:
    """`(hunks, changed_lines, created_or_deleted)` from one path's `--unified=0` diff body."""
    hunks, changed = [], []
    created = "new file mode " in body or "deleted file mode " in body
    for line in body.splitlines():
        m = _HUNK_RE.match(line)
        if m:
            hunks.append((int(m.group(1)), int(m.group(2) or 1),
                          int(m.group(3)), int(m.group(4) or 1)))
        elif line[:1] in "+-" and not line.startswith(("+++", "---")):
            changed.append(line)
    return tuple(hunks), tuple(changed), created


def _classify_touch(hunks, changed, created, blobs) -> Optional[str]:
    """The ONE CONTENT-vs-TOUCH classifier. Done-contract item 2.

    A whitespace, regeneration or index-refresh commit does not invalidate a review; a delta
    computed off `git log -1` alone counts all three as edits and over-reports. All three
    predicates are STRUCTURAL — the commit subject is never read (see the `TOUCH_*` comment
    above for why that is load-bearing rather than incidental).

    ONE classifier, TWO feeds: `_touch_reason` feeds it a single `git show`, `_diff_index` feeds
    it a batched `git log -p`. Both reach the same code, so the cheap path and the exact path
    cannot drift into two different notions of "content".

    `blobs` is a lazy `() -> (new_text, old_text)` — T2 is the only predicate needing them, and
    T2 is reached only when T1 and T3 have both declined, so the blob read stays rare.

    A commit that CREATES or DELETES the file is CONTENT unconditionally: a file's first
    appearance is the largest content change it will ever have, and its frontmatter being the
    only thing inside the diff's line range is an artefact of the file being short, not
    evidence that nobody wrote anything.
    """
    if created:
        return None
    if not hunks and not changed:
        return TOUCH_WHITESPACE           # T1 - empty once whitespace is ignored
    if changed and all(not ln[1:].strip() or _STAMP_LINE_RE.match(ln[1:]) for ln in changed):
        return TOUCH_STAMP_LINE           # T3
    if not hunks:
        return None
    # T2's PRE-FILTER, and it is what keeps the ordinary case free. T2 needs the blob at this
    # commit AND at its parent — two git processes — and it is reached on every genuine prose
    # edit, so the commonest path was paying the most: 7.18 s for one run of this check, ~4 s of
    # it blob reads that were always going to conclude CONTENT. A line inside YAML frontmatter
    # is `---` or a `key:` mapping; a changed line that is neither cannot be inside frontmatter,
    # so T2 is impossible and the blobs are never fetched.
    #
    # SOUND IN THE SAFE DIRECTION, which is the only reason a filter belongs in front of a
    # correctness predicate: it can only ever make T2 decline (-> CONTENT -> a doc reported
    # STALE), never excuse a commit as a TOUCH. The honest cost is a frontmatter change written
    # as a YAML list item or comment, which scores CONTENT — over-reporting staleness, the
    # direction A4 chose for this classifier throughout.
    if not all(_YAML_ISH_RE.match(ln[1:]) or not ln[1:].strip() for ln in changed):
        return None
    # Every changed line at or above the closing `---`, checked against the frontmatter span of
    # the blob AT THIS COMMIT and at its parent, never against today's file (A4's rule: today's
    # frontmatter may be a different length than the one the commit actually edited).
    new_blob, old_blob = blobs()
    if new_blob is None or old_blob is None:
        return None
    new_end, old_end = _frontmatter_end_line(new_blob), _frontmatter_end_line(old_blob)
    if not new_end or not old_end:
        return None
    for old_start, old_count, new_start, new_count in hunks:
        if old_count and old_start + old_count - 1 > old_end:
            return None
        if new_count and new_start + new_count - 1 > new_end:
            return None
    return TOUCH_FRONTMATTER              # T2


def _diff_index(repo_path, paths: list[str]) -> dict[str, list[_CommitDiff]]:
    """Newest-first per-path commit diffs, from ONE batched `git log -p`.

    THE WHOLE WALK IN ONE PROCESS, AND THAT IS WHAT MAKES THIS LEG AFFORDABLE AT COMMIT TIER.
    Measured on this workstation, over the hub's 39 living docs and their 842 commits:

        39 x `git log -1`                              7.63 s   (the Windows subprocess tax)
        1 x `git log --name-only`                      0.33 s
        1 x `git log -p --unified=0 -w`                1.11 s   <- this, 3.4 MB
        per-commit `git show` for classification       ~0.19 s each

    The first build of this leg used the `--name-only` log plus a `git show` per commit examined
    and a `git log -S` per stamped file, and measured **9.43 s** for one
    `check_canonical_freshness` — on the PRE-COMMIT gate. Folding dates, diffs AND the
    stamp-setting commit into this single `-p` pass removes every one of those per-commit
    processes: they all become string work over output already in memory. Same answers, and the
    same lesson `build_edge_index` records about re-tokenizing per rule (14.53 s -> 0.75 s).

    Author date (`%as`), not committer date, matching `git_last_commit_date`: it survives
    rebase / cherry-pick / amend, so a row keys off when content was edited rather than when
    history was rewritten. Merge commits carry no diff under `git log` defaults and so appear
    here for no path — the under-reporting limit named in this section's header comment.

    **GIT APPLIES T1 ITSELF HERE, and that is worth knowing before reading a row.** Under `-w
    --ignore-blank-lines --ignore-space-at-eol` a whitespace-only commit's diff is EMPTY, and
    `git log -p` then emits no `diff --git` header for that path at all — so the commit never
    enters this index. That is correct for every verdict computed from it (a whitespace commit
    is never the CONTENT commit anyone is looking for) and it is free. Two consequences to hold
    onto: `touch_skipped` counts only the TOUCH commits the CLASSIFIER walked past, never the
    ones git filtered out upstream; and `_classify_touch`'s T1 arm is reachable only through
    the single-commit `_touch_reason` feed, which is why the two feeds are pinned as agreeing
    on every commit this index DOES carry rather than on the same commit COUNT.
    """
    if not paths:
        return {}
    out = _derive_git(repo_path, [
        "log", "--format=%x01%H %as", "-p", "-w", "--ignore-blank-lines",
        "--ignore-space-at-eol", "--unified=0", "--", *paths])
    if out is None:
        return {}
    index: dict[str, list[_CommitDiff]] = {p: [] for p in paths}
    for record in out.split("\x01")[1:]:
        head, _, body = record.partition("\n")
        parts = head.split(" ", 1)
        if len(parts) != 2:
            continue
        sha = parts[0]
        try:
            when = date.fromisoformat(parts[1].strip())
        except ValueError:
            continue
        # One record can carry several paths; `diff --git a/P b/P` starts each.
        for chunk in body.split("\ndiff --git "):
            chunk = chunk.removeprefix("diff --git ")
            first, _, rest = chunk.partition("\n")
            m = re.match(r'"?a/(.+?)"? "?b/(.+?)"?$', first.strip())
            if not m:
                continue
            path = m.group(2)
            if path not in index:
                continue
            hunks, changed, created = _parse_unified_zero(rest)
            index[path].append(_CommitDiff(sha, when, hunks, changed, created))
    return index


def _frontmatter_end_line(text: str) -> int:
    """1-based line of the CLOSING `---`, or 0 when the blob has no frontmatter."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return 0
    for i, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            return i
    return 0


def _blob_pair(repo_path, sha: str, path: str):
    """Lazy `() -> (blob_at_sha, blob_at_parent)` for T2. Two git calls, only when reached."""
    def read():
        return (_derive_git(repo_path, ["show", f"{sha}:{path}"]),
                _derive_git(repo_path, ["show", f"{sha}^:{path}"]))
    return read


def _touch_reason(repo_path, sha: str, path: str) -> Optional[str]:
    """Why commit `sha` is a TOUCH of `path` — or None, meaning it is CONTENT.

    The single-commit feed into `_classify_touch`. `derive_doc_freshness` uses the batched
    `_diff_index` feed instead; this one exists for a caller that has one commit in hand and
    is the seam the classifier's tests exercise directly.
    """
    diff = _derive_git(repo_path, [
        "show", sha, "-w", "--ignore-blank-lines", "--ignore-space-at-eol",
        "--unified=0", "--format=", "--", path])
    if diff is None:
        return None                       # cannot classify -> never excuse it as a TOUCH
    hunks, changed, created = _parse_unified_zero(diff)
    return _classify_touch(hunks, changed, created, _blob_pair(repo_path, sha, path))


def _declared_stamp_needle(text: str) -> Optional[str]:
    """The literal stamp LINE a doc declares — the string whose introduction dates its review.

    The LINE, not the date: a bare `2026-08-29` would match any commit that changed how often
    that date appears anywhere in the file, and these docs quote dates constantly.
    """
    reviewed = _parse_last_reviewed(text)
    if reviewed is not None:
        for line in text.splitlines():
            if line.startswith("last_reviewed:"):
                return line
        return None
    m = _PROSE_STAMP_RE.search(text)
    return m.group(0) if m else None


def _stamp_setting_commit(needle: str, diffs: list[_CommitDiff]) -> Optional[str]:
    """The commit that SET the doc's current stamp — its review's identity.

    The newest commit whose diff ADDS the stamp line. That is precisely what `git log -S`
    computes, and it was one subprocess per stamped file (1.83 s for nine) before the batched
    `-p` walk made the same answer free: the added lines are already parsed in `diffs`.
    """
    wanted = "+" + needle.strip()
    for d in diffs:
        if any(ln.strip() == wanted for ln in d.changed):
            return d.sha
    return None


def _unreviewed_after_stamp(repo_path, path: str, setter: str,
                            diffs: list[_CommitDiff]) -> int:
    """How many CONTENT commits landed AFTER the review this doc's stamp claims.

    THE ANCESTRY TEST, and it is the single most valuable thing this leg does. A2 compares
    DATES, and `%as` is day-granular: content committed later the same day as the stamp passes.
    A4 §3 measured 4 of the 9 gated files carrying exactly that — including the CLAUDE.md
    re-genre that deleted 15,657 bytes, 40% of the file, AFTER the stamp asserting it had been
    read end-to-end and confirmed accurate. Commit ORDER is total; calendar dates are not.

    This is A4's recommendation 2 built against the stamps that EXIST. A4's draft proposed
    changing the reviewer record's type from a date to a `reviewed_at: <sha>` — a frontmatter
    schema change across every gated doc. The same question is answerable today by finding the
    commit that set the current date and classifying what came after it: no doc edited, nothing
    to migrate, and the calendar backstop A4's constraint 1 insists on survives untouched.
    """
    order = [i for i, d in enumerate(diffs) if d.sha == setter]
    if not order:
        return 0          # the setter is not in this path's history -> undeterminable, not drift
    return sum(1 for d in diffs[:order[0]]
               if _classify_touch(d.hunks, d.changed, d.created,
                                  _blob_pair(repo_path, d.sha, path)) is None)


def _last_content_commit(repo_path, path: str,
                         diffs: Optional[list[_CommitDiff]] = None):
    """`(sha, date, touch_skipped)` for the newest CONTENT commit touching `path`.

    Walks newest-first and STOPS at the first CONTENT commit. `diffs` is the pre-batched index;
    omitted, it is fetched for this one path.

    Walk-capped at `_DERIVED_WALK_CAP`: the newest commit is then reported with the skip count,
    which OVER-reports staleness rather than under-reporting it.
    """
    if diffs is None:
        diffs = _diff_index(repo_path, [path]).get(path, [])
    skipped = 0
    for d in diffs[:_DERIVED_WALK_CAP]:
        if _classify_touch(d.hunks, d.changed, d.created,
                           _blob_pair(repo_path, d.sha, path)) is None:
            return d.sha, d.when, skipped
        skipped += 1
    if diffs:
        return diffs[0].sha, diffs[0].when, skipped
    return None, None, 0


def derive_doc_freshness(repo_path, *, refine_all: bool = False) -> list[DocFreshness]:
    """Every living doc's freshness, DERIVED from git. Done-contract items 1, 3 and 5.

    Raises `DerivationUnavailable` (no git / not a repo) or `DerivationRefused` (shallow clone).
    Read-only: it computes, it never re-stamps a file. Layer 2 does not execute.

    REFINEMENT IS SPENT WHERE IT CHANGES A VERDICT, and that is a measured decision rather than
    a shortcut. Classifying CONTENT-vs-TOUCH costs one `git show` per commit examined (0.19 s
    here), so refining all 39 living docs costs ~7 s — affordable on demand, not on every
    commit. Refinement can only move a derived date EARLIER, so it can only ever turn a
    stale verdict fresh; a row that is already fresh cannot change. The default therefore
    refines exactly the CANDIDATE-STALE rows, and any row it did not refine says so
    (`unrefined` in `row()`), so a reader is never shown a refined-looking number that is not.
    `refine_all=True` refines everything — what `doctrine_table` and the CLI use.
    """
    shallow = _git_is_shallow(repo_path)
    if shallow is None:
        raise DerivationUnavailable(
            "no git history to derive from (git absent, or this is not a git repo)")
    if shallow:
        raise DerivationRefused(
            "the clone is shallow -- every git-derived date is a floor, not a fact, and a "
            "grafted history silently mis-dates every file older than the graft. "
            "Run `git fetch --unshallow origin` before trusting a freshness verdict here")

    paths = _living_doc_paths(repo_path)
    index = _diff_index(repo_path, paths)
    gated = set(_FRESHNESS_FILES)
    rows: list[DocFreshness] = []
    for path in paths:
        try:
            text = (Path(repo_path) / path).read_text(encoding="utf-8")
        except OSError:
            continue
        declared, surface = parse_declared_freshness(text)
        diffs = index.get(path, [])
        if not diffs:
            continue                      # tracked but never committed under this path
        sha, when = diffs[0].sha, diffs[0].when
        skipped, refined = 0, False
        if refine_all or (declared is not None and declared < when):
            sha, when, skipped = _last_content_commit(repo_path, path, diffs)
            refined = True

        is_gated = path in gated
        stamp_sha, unreviewed = None, 0
        if declared is None:
            doc_class = CLASS_UNSTAMPED
        elif when is not None and declared < when:
            doc_class = CLASS_GATED_STALE if is_gated else CLASS_UNGATED_STALE
        else:
            # FRESH BY DATE -- so this is exactly where the same-day hole lives, and the only
            # class where the ancestry test can change an answer. A row already stale stays
            # stale; a row with no stamp has no review to be "after". Both the stamp-setting
            # commit and the classification of what followed it come out of the batched diff
            # index, so this costs no additional git process in the ordinary case.
            needle = _declared_stamp_needle(text)
            stamp_sha = _stamp_setting_commit(needle, diffs) if needle else None
            if stamp_sha:
                unreviewed = _unreviewed_after_stamp(repo_path, path, stamp_sha, diffs)
            if unreviewed:
                doc_class = CLASS_GATED_STALE if is_gated else CLASS_UNGATED_STALE
            else:
                doc_class = CLASS_GATED_FRESH if is_gated else CLASS_UNGATED_FRESH
        rows.append(DocFreshness(
            path=path, declared=declared, surface=surface, derived=when, derived_sha=sha,
            touch_skipped=skipped, refined=refined, gated=is_gated,
            version=parse_declared_version(text), doc_class=doc_class,
            stamp_sha=stamp_sha, unreviewed_after_stamp=unreviewed))

    rows.sort(key=lambda r: (-(r.delta_days if r.delta_days is not None else -10**6), r.path))
    return rows


def doctrine_table(repo_path) -> str:
    """The living-doc doctrine table: one flat row per doc, live version and live date.

    Done-contract item 4. `protocols/PLAYBOOK.md` is the case that names the problem — its
    version rides `reconciled_with:` and its date is a prose `> Last updated:` line NO GATE
    PARSES, so the table it carries can assert a date git refutes and nothing notices. Rendered
    here it is DERIVED: the declared pair stays visible beside the derived one rather than
    being overwritten, because the two answer different questions and A4's constraint 1 is that
    the reviewer record survives derivation.

    Fully refined (`refine_all=True`): this is the on-demand surface, where the ~7 s the full
    CONTENT walk costs is free. Flat and pipe-free so the operator can paste it into a fenced
    block without the TUI painting borders into it (CLAUDE.md §4 output-formatting).
    """
    rows = derive_doc_freshness(repo_path, refine_all=True)
    return "\n".join(r.row() for r in rows)


def _derived_freshness_findings(repo_path) -> list[Finding]:
    """The derived leg's Findings, appended after `check_canonical_freshness`'s A1/A2 verdict.

    ONE FINDING PER CLASS, not per doc, and that is a deliberate departure from the
    one-finding-per-violation rule the fail-capable checks follow. This leg is an AWARENESS
    organ on the `git_backlog_drift` model: the classes ARE the deliverable (A4 §3's partition),
    a reader wants them named together, and 26 unstamped docs emitted as 26 separate WARNs
    would drown the ship gate's disposition register in rows that share one answer.
    """
    name = "canonical_freshness"
    try:
        rows = derive_doc_freshness(repo_path)
    except DerivationUnavailable as exc:
        return [_na(name, _NA_NOT_APPLICABLE, f"derived leg: {exc}")]
    except DerivationRefused as exc:
        return [Finding(name, "fail", f"derived leg REFUSES (shallow clone): {exc}"
                        .replace("|", "/"))]
    if not rows:
        return [_na(name, _NA_SUBJECT_ABSENT, "derived leg: no living docs tracked here")]

    findings: list[Finding] = []
    # THE UNSTAMPED CLASS IS SCOPE-NARROWED TO THE GATED SET'S OWN DIRECTORIES (R5 window
    # bundle B10, ruled 2026-09-05). It was reporting 27 files that carry no `last_reviewed`
    # and ARE NOT REQUIRED TO -- `.claude/commands/`, `plugins/`, `deploy/` and friends, none
    # of them under any stamping contract. A permanently-amber row with nothing behind it is
    # the "detector teaches that amber is normal" failure, and the ruled fix is to narrow the
    # scope rather than disposition the row forever: a file sharing a directory with a gated
    # file is one the A1/A2 cadence could plausibly extend to, so its absence of a stamp is a
    # freshness question; a file in a directory the cadence has never reached is a SCOPE
    # question, and belongs to whoever widens the contract, not to this report.
    # NOT SILENTLY DROPPED -- the out-of-scope count is still printed, so narrowing the report
    # cannot hide growth. The two STALE classes are untouched: a stale stamp means a contract
    # exists and is being missed, which is a different fact from never having had one.
    _gated_dirs = {p.rsplit("/", 1)[0] if "/" in p else "" for p in _FRESHNESS_FILES}
    for doc_class in (CLASS_GATED_STALE, CLASS_UNGATED_STALE, CLASS_UNSTAMPED):
        members = [r for r in rows if r.doc_class == doc_class]
        out_of_scope = 0
        if doc_class == CLASS_UNSTAMPED:
            adjacent = [r for r in members
                        if (r.path.rsplit("/", 1)[0] if "/" in r.path else "") in _gated_dirs]
            out_of_scope = len(members) - len(adjacent)
            members = adjacent
        if not members:
            continue
        tail = (f" (+{out_of_scope} unstamped outside the gated set's directories, "
                f"out of scope for this report)" if out_of_scope else "")
        findings.append(Finding(name, "warn", (
            f"derived {doc_class}: {len(members)} - " + "; ".join(r.brief() for r in members)
            + tail + " -- full rows: audit.py doc-freshness"
        ).replace("|", "/")))

    fresh = [r for r in rows if r.doc_class in (CLASS_GATED_FRESH, CLASS_UNGATED_FRESH)]
    gated_fresh = [r for r in fresh if r.gated]
    findings.append(Finding(name, "pass", (
        f"derived {CLASS_GATED_FRESH}: {len(gated_fresh)} of {len(rows)} living docs "
        f"({len(fresh)} fresh overall; derived = last CONTENT commit, TOUCH commits "
        f"[{TOUCH_WHITESPACE}, {TOUCH_FRONTMATTER}, {TOUCH_STAMP_LINE}] walked past)"
    ).replace("|", "/")))

    doctrine = [r for r in rows if r.version]
    if doctrine:
        findings.append(Finding(name, "pass", (
            "derived doctrine rows (live version + date): " + "; ".join(r.row() for r in doctrine)
        ).replace("|", "/")))
    return findings


# rule: canonical-freshness
def check_canonical_freshness(repo_path: Path) -> list[Finding]:
    """Canonical living-file freshness cadence (operationalizes ADR-39 grooming).

    For each canonical living doc (_FRESHNESS_FILES) that carries `last_reviewed`:
      - A2 (primary, FAIL): `last_reviewed` predates the file's last git-commit date — the
        file was edited but never re-reviewed, so its review stamp is stale.
      - A1 (backstop, WARN): `last_reviewed` is older than _FRESHNESS_CADENCE_DAYS — a
        loose calendar nudge even when nothing changed.
    Missing `last_reviewed` → WARN (child-repo-safe: lets a repo adopt the convention
    without a hard failure). An absent file is skipped (presence is enforced by #1/#3/#5).

    `last_reviewed` means "re-read end-to-end and confirmed accurate (or the drift filed)"
    on that date — NOT merely "touched". This check enforces edit-hygiene + a calendar
    backstop; it does NOT verify content against external decisions (e.g. a doc whose
    prose has drifted from a new ADR while its file was never edited trips neither signal).

    A2 is deliberately COMMIT-based, not working-tree-based: an uncommitted edit that has
    not yet bumped `last_reviewed` is not flagged until it lands in a commit (working-tree
    state would FAIL during normal mid-edit work, before the reviewer has bumped the stamp).
    So the signal is post-commit / eventually-consistent — it catches the stale stamp at the
    next audit after the edit is committed, which is the intended enforcement point.

    Read-only; degrades gracefully without git (A2 skipped). PORTABLE via _FRESHNESS_FILES.
    Logic single-sourced in scripts/canonical_freshness_gate.py (the same module the mesh carrier
    deploys consumer-local); this leg only wraps its (fails, warns) in the Finding envelope. The
    audit-level `_parse_last_reviewed` / `_git_last_commit_date` are passed in so tests that
    monkeypatch them at the audit level still take effect.

    SINCE `[#614]` HY-1 THIS CHECK HAS A SECOND LEG: `last_reviewed` DERIVED from git, for every
    living doc, not just the nine `_FRESHNESS_FILES`. Its Findings are APPENDED — index 0 stays
    the A1/A2 verdict it has always been, which is what ten call sites in `tests/test_audit.py`
    and the `test_enforcement_coverage` fire-test read.

    WHY A LEG HERE RATHER THAN A NEW `ALL_CHECKS` MEMBER. Two reasons, and the first is the one
    that would still hold with an unlimited write scope: it is the SAME concern this check
    already owns — is a doc's review stamp honest? — computed by a strictly better method over a
    strictly larger set, and splitting one question across two checks makes the pair drift. The
    second is a scope fact, stated rather than disguised: a new registry member breaks six count
    pins (`tests/test_audit.py` x2, `tests/test_doc_code_edge.py` x2,
    `tests/test_writer_integrity.py`, `ecosystem/doc-counts.md`) and needs an
    `ecosystem/doc-code-edge.yaml` row, none of which is inside this lane's frozen three-file
    footprint.

    THE DERIVED LEG IS WARN-CLASS ON ARRIVAL, AND THE PROMOTION CONDITION IS ONE LINE AND
    MEASURABLE. A4 §3 measured 4 of the 9 gated files ALREADY carrying content that landed after
    the stamp claiming they had been read — invisible to A2 because `%as` is day-granular.
    Emitting that as `fail` on arrival would wedge `audit-health`, the PRE-COMMIT gate, on four
    pre-existing docs; that is an operator ratchet decision, not a lane's. So: WARN here, teeth
    at ship time (`cmd_ship_gate` REDs on any undispositioned warn). PROMOTION: when
    `derived {CLASS_GATED_STALE}` measures 0 on `main`, the `Finding(..., "warn", ...)` for
    `CLASS_GATED_STALE` in `_derived_freshness_findings` becomes `"fail"`. Recorded here rather
    than remembered, because a temporary posture nobody wrote down is a permanent one.
    """
    fails, warns = _cfg.evaluate(
        repo_path, _FRESHNESS_FILES,
        parse_fn=_parse_last_reviewed, git_date_fn=_git_last_commit_date)

    if fails:
        evidence = f"{len(fails)} stale (edited since review): " + "; ".join(fails)
        if warns:
            evidence += f" | also {len(warns)} warn: " + "; ".join(warns)
        verdict = Finding("canonical_freshness", "fail", evidence)
    elif warns:
        verdict = Finding("canonical_freshness", "warn", "; ".join(warns))
    else:
        verdict = Finding("canonical_freshness", "pass",
                          f"{len(_FRESHNESS_FILES)} canonical living files fresh "
                          f"(last_reviewed not before last edit; "
                          f"within {_FRESHNESS_CADENCE_DAYS}d)")
    return [verdict, *_derived_freshness_findings(repo_path)]


def check_generated_artifact_freshness(repo_path: Path) -> list[Finding]:
    """Committed-generated staleness -- is a committed generated artifact older than its inputs?

    ADR-86 as AMENDED 2026-08-23 rules that a human or integrator commit satisfies "committed".
    That makes the dashboard's header honest; it does nothing to keep the output CURRENT. An
    honest header on a stale trust surface is still a stale trust surface, so this leg is the
    other half of the same ruling: WARN when the committed artifact has fallen further behind
    its declared inputs than the baseline measured when the leg was armed (dashboard: 4 days, at
    `aeec0fd1`). The baseline is a RATCHET, not an allowance.

    WARN-CLASS BY RULING. `cmd_health` (the pre-commit gate) exits 1 only on a `fail`, while
    `cmd_ship_gate` REDs on any undispositioned `warn` -- so the TEETH are at ship time.

    AND THE WORK IS SKIPPED AT COMMIT TIME, not merely the blocking. A WARN-class check that
    still SPENDS its cost on every commit -- measured at 11 `git log` calls for the dashboard --
    buys nothing there, because `cmd_health` exits 1 only on a `fail`. This leg hand-rolled that
    skip with `_GATE_MODE`; since [#597] it is DECLARED (`_tier(TIER_SHIP, ...)` in ALL_CHECKS)
    and the runner does the skipping, so the leg's body no longer has a commit-time branch at
    all. At commit time the runner emits the honest `n/a` in its place; at ship time it measures.

    ONE Finding PER ARTIFACT so the #147 ship-gate dispositions each independently. Logic
    single-sourced in `scripts/generated_artifact_freshness.py`; this leg only wraps it, passing
    the audit-level git-date alias so a monkeypatch at the audit level still applies.

    THE STATUS MAPPING IS A TABLE LOOKUP, NOT AN `if/else`, and that is deliberate. Written as
    `if stale: warn / else: pass`, this leg reported every verdict added AFTERWARDS as a silent
    `pass`. `STATUS_FOR_VERDICT` lives in the module beside the verdicts it maps, so an unknown
    verdict raises `KeyError` here instead of passing quietly.
    """
    name = "generated_artifact_freshness"
    findings: list[Finding] = []
    for artifact in _gaf.REGISTRY:
        m = _gaf.measure(repo_path, artifact, git_date_fn=_gaf_git_last_commit_date)
        status = _gaf.STATUS_FOR_VERDICT[m.verdict]   # KeyError on an unmapped verdict: loud
        if status == "unavailable" and m.subject_absent:
            findings.append(_na(name, "SUBJECT-ABSENT", m.detail))
            continue
        evidence = m.detail
        if status == "warn":
            evidence = f"{evidence}; regenerate + commit: {artifact.regen_command}"
        findings.append(Finding(name, status, evidence.replace("|", "/")))
    return findings


def _git_registered_worktrees(repo_path: Path) -> Optional[set[str]]:
    """Normcased absolute paths of every git worktree registered for `repo_path`.

    Read-only (`git worktree list --porcelain`). Returns None when git is absent or the
    path is not a git repo, so a non-git consumer degrades gracefully (the orphan check is
    then skipped) — same pattern as `_git_last_commit_date`. Paths are normalized through
    `Path.resolve()` + `os.path.normcase` so the on-disk comparison is robust to git's
    forward-slash output and Windows' case-insensitive filesystem.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "worktree", "list", "--porcelain"],
            capture_output=True, text=True, encoding="utf-8",
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    registered: set[str] = set()
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            raw = line[len("worktree "):].strip()
            try:
                registered.add(os.path.normcase(str(Path(raw).resolve())))
            except OSError:
                registered.add(os.path.normcase(raw))
    return registered


def _git_repo_root_name(repo_path: Path) -> Optional[str]:
    """Directory name of the MAIN worktree (repo root) for `repo_path`.

    A linked worktree's own basename is a throwaway (`.dev-knowledge-<topic>`); the durable
    repo identity is the main worktree's directory name. `git rev-parse --git-common-dir`
    returns the SHARED `.git` gitdir — `<main-root>/.git` — from any worktree of the repo, so
    its parent's name is the repo-root identity regardless of which worktree we audit from.

    Read-only (`git rev-parse`). Returns None when git is absent or the path is not a git repo
    (same graceful-degradation contract as `_git_registered_worktrees`), so a non-git consumer
    falls back to the working-dir basename at the call site.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "rev-parse", "--git-common-dir"],
            capture_output=True, text=True, encoding="utf-8",
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    common = result.stdout.strip()
    if not common:
        return None
    common_path = Path(common)
    if not common_path.is_absolute():
        common_path = Path(repo_path) / common_path
    try:
        common_path = common_path.resolve()
    except OSError:
        pass
    # `--git-common-dir` is the main worktree's `.git` gitdir; its parent is the repo root.
    return common_path.parent.name


def _looks_like_worktree_remnant(path: Path) -> bool:
    """True when `path` shows evidence of being a torn-down worktree leftover rather
    than an independent repo or an unrelated populated folder.

    Either signal suffices:
      - the directory is EMPTY — the canonical orphan (`.dev-knowledge-cadence` was empty
        after git deregistered it but the shell survived); or
      - it carries a `.git` *gitlink file* (not a `.git/` directory) — the marker a git
        worktree leaves behind, so a half-removed/deregistered worktree that still holds
        content is still caught.

    A legitimate same-prefix sibling is therefore NOT flagged: an independent git repo has
    a `.git/` *directory* (not a gitlink file) plus content, and an unrelated populated
    folder has neither signal. This narrows the detector to actual worktree evidence
    (Codex H1, 2026-06-02) without weakening the registration gate.
    """
    try:
        entries = list(path.iterdir())
    except OSError:
        return False
    if not entries:
        return True
    return (path / ".git").is_file()


def check_no_sibling_orphans(repo_path: Path) -> list[Finding]:
    """No orphaned `<repo>-*` sibling directories left behind by a torn-down worktree
    (no-leftovers invariant — ADR-61/ADR-68, PLAYBOOK G5).

    A parallel-session or night-agent worktree is created as a `<repo>-<topic>` sibling
    next to the repo and removed at goal/run end. When `git worktree remove` silently
    no-ops (the directory is process-locked) and the teardown is not re-checked, git
    deregisters the worktree but the empty directory survives on disk as an orphan — the
    `.dev-knowledge-cadence` / `.dev-knowledge-night-adr` failure (cleaned 2026-06-02).

    A sibling is flagged only when BOTH hold:
      - it is NOT a registered git worktree (registration is the primary gate — a `<repo>-*`
        sibling that IS registered is legitimate in-use parallel work, never flagged); AND
      - it shows worktree-remnant evidence (empty, or a `.git` gitlink file) per
        `_looks_like_worktree_remnant` — so a legitimate same-prefix sibling repo or
        populated folder is not mistaken for an orphan (Codex H1).

    A presence-checking audit structurally cannot catch a directory that exists but should
    not (2026-05-17 decommissioning-gap LESSON), so this is an explicit negative assertion —
    the mechanization PLAYBOOK "No leftovers ... invariant" names (referenced by section name,
    not line number, so it does not drift).

    Read-only (`git worktree list`). Degrades gracefully without git (skipped). PORTABLE:
    a child repo inherits it unchanged — `repo_path.name` resolves to that repo's prefix.
    """
    registered = _git_registered_worktrees(repo_path)
    if registered is None:
        return [Finding("no_sibling_orphans", "unavailable",
                        "git unavailable or not a repo - sibling-orphan check skipped")]
    prefix = repo_path.name + "-"
    try:
        siblings = sorted(
            p for p in repo_path.parent.iterdir()
            if p.is_dir() and p.name.startswith(prefix))
    except OSError:
        return [Finding("no_sibling_orphans", "unavailable",
                        "parent directory unreadable - sibling-orphan check skipped")]
    orphans = [
        p.name for p in siblings
        if os.path.normcase(str(p.resolve())) not in registered
        and _looks_like_worktree_remnant(p)]
    if orphans:
        return [Finding("no_sibling_orphans", "fail",
                        f"Unregistered '{prefix}*' sibling dir(s) next to repo - worktree "
                        f"orphan(s) left behind (remove, or re-register if live): {orphans}")]
    return [Finding("no_sibling_orphans", "pass",
                    f"No orphaned '{prefix}*' siblings (each is a registered worktree or a "
                    f"real repo/folder, not a worktree remnant; or none exist)")]


# [#505] batch hygiene. The horizon is the MECHANIZED WEEKLY PRUNE the intake keeps ("hygiene
# organ — WARN on stale worktrees (mechanized weekly prune stays)", intake #26 Track 1 item 4),
# so 7 is that cadence rather than a taste call. Changing it changes what "stale" means; it is
# named here once so the check and its tests cannot drift to two numbers.
_STALE_WORKTREE_HORIZON_DAYS = 7


def _git_commit_epoch(repo_path: Path, rev: Optional[str]) -> Optional[int]:
    """Committer epoch of `rev`, or None when it cannot be read.

    None is a real answer, not an error code: the caller reports an unreadable date as
    INDETERMINATE rather than defaulting it either way. Defaulting to "now" would hide a stale
    worktree; defaulting to 0 would manufacture one out of a git hiccup.

    Read-only (`git show -s`). Same graceful-degradation contract as its neighbours.
    """
    if not rev:
        return None
    proc = _git(repo_path, "show", "-s", "--format=%ct", rev)
    if proc is None or proc.returncode != 0:
        return None
    try:
        return int(proc.stdout.strip().splitlines()[0])
    except (ValueError, IndexError):
        return None


def _git_linked_worktrees(repo_path: Path) -> Optional[list[dict]]:
    """Every LINKED worktree of `repo_path` — the main one is excluded — carrying the two facts
    staleness needs: whether the directory still exists, and when its checked-out tip was
    committed.

    Distinct from `_git_registered_worktrees` above, which answers a different question (is
    THIS path registered?) and returns a flat path set with no per-worktree detail. Kept as a
    separate reader rather than widening that one, because `check_no_sibling_orphans` depends on
    its exact set semantics.

    `git worktree list --porcelain` reports the MAIN worktree first, always — that ordering is
    the porcelain contract, and it is how the primary is dropped without resolving and comparing
    paths. Prunable/locked annotations are deliberately NOT parsed: they arrived in later git
    versions, so on-disk presence is tested directly and the reader stays version-independent.

    NUL-DELIMITED FIRST, newline-delimited as a fallback (terra HIGH, 2026-08-06). Newline
    parsing splits a worktree path that CONTAINS a newline into malformed records, and the
    truncated path then fails its on-disk test — so a pathological-but-legal path would be
    reported stale, which is a false WARN manufactured by the parser. `-z` removes that class.
    It arrived in a later git, hence the fallback: a `-z` that fails re-runs without it rather
    than returning None, because degrading to the old parse beats disabling the check entirely
    on an older git.

    Read-only. Returns None when git is absent or the path is not a git repo, so a non-git
    consumer degrades gracefully (the check is then n/a) — the `_git_registered_worktrees`
    contract.
    """
    def _run(extra: list[str]) -> Optional[subprocess.CompletedProcess]:
        try:
            return subprocess.run(
                ["git", "-C", str(repo_path), "worktree", "list", "--porcelain", *extra],
                capture_output=True, text=True, encoding="utf-8", timeout=15,
            )
        except (OSError, subprocess.SubprocessError):
            return None

    result = _run(["-z"])
    if result is None:
        return None
    if result.returncode == 0:
        # `-z` terminates every attribute with NUL; a record ends at an empty attribute.
        fields = [f for f in result.stdout.split("\0")]
    else:
        result = _run([])       # older git: no `-z`. Degrade, do not disable.
        if result is None or result.returncode != 0:
            return None
        fields = result.stdout.splitlines()
    records: list[dict] = []
    current: dict = {}
    for line in fields:
        if line.startswith("worktree "):
            if current:
                records.append(current)
            current = {"path": line[len("worktree "):], "branch": None, "head": None}
        elif not current:
            continue
        elif line.startswith("branch "):
            current["branch"] = line[len("branch "):].strip().removeprefix("refs/heads/")
        elif line.startswith("HEAD "):
            current["head"] = line[len("HEAD "):].strip()
    if current:
        records.append(current)
    out: list[dict] = []
    for rec in records[1:]:      # [0] is the main worktree
        try:
            on_disk = Path(rec["path"]).is_dir()
        except OSError:
            on_disk = False
        out.append({
            "path": rec["path"],
            "branch": rec["branch"],
            "on_disk": on_disk,
            "last_commit_epoch": _git_commit_epoch(repo_path, rec["head"]),
        })
    return out


def _git_stash_entries(repo_path: Path) -> Optional[list[str]]:
    """Every entry in the repository's stash, one string per entry, newest first.

    WHY THIS IS A SEPARATE READER FROM THE WORKTREE ONE, and why the leg it feeds exists at
    all (batch-1 F4): `refs/stash` lives in the COMMON git directory. It is not among git's
    per-worktree refs, so a stash pushed from inside a linked worktree is a fact about the
    whole repository — readable from the primary, and untouched by `git worktree remove`,
    `git worktree prune`, and the lane-branch delete. Worktree state therefore cannot be used
    to infer it in either direction: a repo with no worktrees at all can be holding one.

    Returns None when the stash could not be read AT ALL — git absent, not a git repo, a
    timeout, or a non-zero exit. The None/`[]` split is load-bearing rather than cosmetic:
    an empty list means "looked, found nothing stashed", so a path that returned `[]`
    without looking would report a clean stash for a directory nothing ever examined. What
    None does NOT tell the caller is WHICH failure occurred — see `_stash_findings`, which
    resolves that against whether the worktree reader succeeded.

    `errors="replace"` is not decoration (terra HIGH, 2026-08-07): a stash subject carries
    an arbitrary commit message, so a repo emitting non-UTF-8 bytes would raise
    `UnicodeDecodeError` out of `subprocess.run` — which is a `ValueError`, NOT caught by the
    handler below — and turn a WARN-tier advisory leg into a crashing audit check.

    Read-only (`git stash list`), and bounded by the same 15s timeout as its sibling.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "stash", "list"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return [ln for ln in result.stdout.splitlines() if ln.strip()]


#: How many stash entries the WARN evidence names before it summarises the rest. The COUNT is
#: the load-bearing number; the sample only helps a reader recognise their own work.
_STASH_SAMPLE = 3


def _stash_findings(repo_path: Path, git_known_good: bool = False) -> list[Finding]:
    """The F4 leg of `check_stale_worktrees` — a stash is the leftover no close-out item sees.

    WARN-tier, like the organ it joins (ADR-110 §3 arms no gate). An empty stash yields an
    explicit pass rather than silence, because a leg that speaks only when unhappy is
    indistinguishable from a leg that never ran.

    `git_known_good` RESOLVES WHAT None MEANS, and it closes a real hole (terra HIGH,
    2026-08-07). `_git_stash_entries` returns None both for "not a git repo" and for "git is
    here but the read failed" (timeout, non-zero exit). When the caller has ALREADY read the
    worktree list successfully, the first reading is impossible — so a None is a genuine
    read failure, and staying silent about it would let the organ report a clean worktree
    verdict while this leg never ran. That is the detector-that-cannot-see-must-not-report-
    clean rule the sibling worktree leg already follows, applied here rather than merely
    asserted in prose. When git is NOT known good the caller has already emitted its own
    n/a, and a second one would say the same thing twice.
    """
    entries = _git_stash_entries(repo_path)
    if entries is None:
        if git_known_good:
            return [Finding("stale_worktrees", "warn",
                            "git stash list could not be read while git itself is working - "
                            "the stash leg did not run, so this result says nothing about "
                            "stashed work outliving its lane")]
        return []
    if not entries:
        return [Finding("stale_worktrees", "pass",
                        "git stash list is empty - no stashed work outliving its lane")]
    sample = "; ".join(e.strip() for e in entries[:_STASH_SAMPLE])
    if len(entries) > _STASH_SAMPLE:
        sample += f"; +{len(entries) - _STASH_SAMPLE} more"
    return [Finding("stale_worktrees", "warn",
                    f"{len(entries)} git stash entry(ies) present: {sample} - the stash lives "
                    f"in the COMMON git dir, so it survives worktree teardown and every "
                    f"refuse-to-finish item; pop or drop it, or say why it stays"
                    .replace("|", "/"))]


def check_stale_worktrees(repo_path: Path, now: Optional[float] = None) -> list[Finding]:
    """[#505] batch hygiene — WARN on a linked worktree no live batch owns (ADR-110 §1 item 4).

    THE GAP THIS COVERS, and why `check_no_sibling_orphans` above does not: that check looks for
    `<repo>-*` sibling dirs git has already DEREGISTERED. The state here is the opposite one — a
    worktree git still registers, sitting in `.claude/worktrees/`, left behind because a batch
    ended without its integrator walking the refuse-to-finish close-out. Unclosed parallel work
    is the operator's stated #1 pain (intake #26); this is the after-the-fact backstop for it.

    STALE means either of two things, and both are measured rather than inferred:
      - the last commit on the worktree's tip predates the weekly prune horizon
        (`_STALE_WORKTREE_HORIZON_DAYS`), strictly — reaching the horizon is still live; or
      - git registers the worktree but its directory is gone from disk, AT ANY AGE. That is a
        half-finished teardown (`git worktree remove` silently no-ops on a locked directory),
        and holding it for a week would hide the exact failure the teardown round-trip exists
        to catch.

    A worktree whose commit date cannot be read is reported as INDETERMINATE — surfaced, never
    silently counted as fresh, and never counted as stale either. A detector that cannot see
    does not report clean, and equally does not invent a finding it did not measure.

    POSTURE — WARN only, by ruling. ADR-110 §3 arms no gate, and the [#505] contract scopes this
    organ to WARN-tier. It informs; it does not become a new way for the commit gate to go red
    on a live batch. `tests/test_stale_worktrees.py` pins that at the source level.

    MID-BATCH IS A PASS, deliberately: during a running batch every lane worktree is registered
    and recently committed. An organ that fired then would alarm through the whole run it exists
    to close, and would be muted by the second batch.

    PORTABLE: a consumer inherits it unchanged — nothing here is hub-keyed. Read-only
    (`git worktree list`, `git show -s`); degrades to n/a without git.

    THE STASH LEG (batch-1 F4, 2026-08-07) is a SECOND finding from the same organ, emitted by
    `_stash_findings` above. It covers the leftover every worktree-shaped measure structurally
    misses: `refs/stash` is common-dir, not per-worktree, so a lane's mid-work stash outlives
    `worktree remove` / `prune` / the branch delete and all four refuse-to-finish items. Its own
    finding rather than a folded verdict, because the empty-worktree state is exactly where it
    matters most — a batch that closed clean by every other measure can still be hiding one.

    Honest limits. It cannot tell a genuinely abandoned lane from a long-running one that is
    simply slow — age is the only signal available without a batch manifest to read. It says
    nothing about UNMERGED lane branches whose worktree was already removed, which is the other
    half of unclosed parallel work and is the integrator checklist's item 1, not this organ's.
    The stash leg reports entries, not ownership: `git stash list` records no worktree of
    origin, so a stash the operator made deliberately on the primary reads identically to a
    lane's abandoned one — which is why the evidence asks for a disposition rather than an
    action. And it fires after the fact: the close-out refusal lives in `/lane-integrate`.
    """
    entries = _git_linked_worktrees(repo_path)
    if entries is None:
        return [_na("stale_worktrees", _NA_NOT_APPLICABLE,
                    "git unavailable or not a repo - stale-worktree check skipped")]
    # git_known_good=True: `_git_linked_worktrees` just succeeded, so this IS a git repo and
    # a None from the stash reader can only be a genuine read failure, never "not a repo".
    stash = _stash_findings(repo_path, git_known_good=True)
    if not entries:
        return [Finding("stale_worktrees", "pass",
                        "no linked worktrees registered (primary only) - nothing to close out"),
                *stash]
    if now is None:
        now = datetime.now(timezone.utc).timestamp()
    horizon_secs = _STALE_WORKTREE_HORIZON_DAYS * 86400
    problems: list[str] = []
    live = 0
    for entry in entries:
        label = entry.get("branch") or Path(str(entry.get("path"))).name
        if not entry.get("on_disk"):
            problems.append(f"{label} [registered but gone from disk - run `git worktree prune`]")
            continue
        epoch = entry.get("last_commit_epoch")
        if epoch is None:
            problems.append(f"{label} [age unknown - last-commit date unreadable]")
            continue
        age_days = (now - epoch) / 86400
        if (now - epoch) > horizon_secs:
            problems.append(f"{label} [last commit {age_days:.0f}d ago]")
        else:
            live += 1
    if problems:
        return [Finding("stale_worktrees", "warn",
                        f"{len(problems)} of {len(entries)} linked worktree(s) look unclosed "
                        f"(horizon {_STALE_WORKTREE_HORIZON_DAYS}d): {'; '.join(problems)} - "
                        f"close them out per the /lane-integrate checklist, or say why they "
                        f"stay".replace("|", "/")), *stash]
    return [Finding("stale_worktrees", "pass",
                    f"{live} linked worktree(s) registered, each committed within the "
                    f"{_STALE_WORKTREE_HORIZON_DAYS}d horizon and present on disk - live batch "
                    f"lanes, not leftovers"), *stash]


# [#533] moved to audit_checks/ — re-exported above.


def check_hooks_armed(repo_path: Path) -> list[Finding]:
    """RF-2 (Fable architecture review 2026-07-04 §4): make the hub apply
    configured->armed->proven to ITSELF. Asserts the three pre-commit-managed git hooks are
    actually installed in this checkout — `.git/hooks/{pre-commit,commit-msg,pre-push}` exist
    AND carry the pre-commit signature — so a configured-but-unarmed window (a fresh clone, or
    a manually deleted hook) fails LOUD instead of silently letting a gate never fire (the
    `.pre-commit-config.yaml` header's own warning; the direct-to-main 533109f that RF-2 cites).

    Hub-only: arming is per-checkout machine state and the hub is the authority (RF-2) — consumer
    arming is measured by the Informant (scripts/enforcement_coverage.py). n/a when the repo
    carries no .pre-commit-config.yaml (nothing to arm) or is not a standard git checkout (no
    resolvable hooks dir). FAIL — not WARN — on a missing/foreign hook: the RF-2 acceptance is
    that deleting `.git/hooks/pre-push` turns `audit.py health` non-green. Fail-soft: any internal
    error -> WARN (never wedge the commit gate). Read-only.

    The self-arm that KEEPS this green is the SessionStart `python -m pre_commit install -t ...`
    hook in .claude/settings.json (added by the same RF-2 arc). Presence/arming infra, not a
    doc->code behavioral rule -> `exempt` in ecosystem/doc-code-edge.yaml.
    """
    if not _is_hub(repo_path):
        return [_na("hooks_armed", "NOT-APPLICABLE",
                        "hub-only — git-hook arming check skipped (not the hub repo)")]
    try:
        if not (Path(repo_path) / ".pre-commit-config.yaml").exists():
            return [_na("hooks_armed", "NOT-APPLICABLE",
                            "no .pre-commit-config.yaml — no managed git hooks to arm")]
        gp = subprocess.run(
            ["git", "rev-parse", "--git-path", "hooks"],
            cwd=repo_path, capture_output=True, text=True, timeout=10,
        )
        if gp.returncode != 0:
            return [_na("hooks_armed", "NOT-APPLICABLE",
                            "not a standard git checkout (no resolvable hooks dir)")]
        hooks_dir = (Path(repo_path) / gp.stdout.strip()).resolve()
        issues: list[str] = []
        for name in ("pre-commit", "commit-msg", "pre-push"):
            hook = hooks_dir / name
            if not hook.exists():
                issues.append(f"{name} absent (run `pre-commit install -t {name}`)")
                continue
            body = hook.read_text(encoding="utf-8", errors="replace")
            if "File generated by pre-commit" not in body:
                issues.append(f"{name} present but not pre-commit-managed (foreign hook)")
            elif f"--hook-type={name}" not in body:
                issues.append(f"{name} wired for the wrong hook-type")
        # [#590] — the same configured-but-unarmed class, one layer down. `.gitattributes`
        # pins `docs/audits/README.md merge=ours`, but `ours` is not a built-in driver: git
        # resolves it through `merge.ours.driver`, and without that key the pin is inert and
        # the index conflicts on every parallel merge exactly as it did before. An inert pin
        # is worse than no pin, because the file says the problem is solved. Reported here
        # rather than as a new check because it is the same question this leg already asks —
        # is this CHECKOUT armed for the gates the repo declares — and the remedy is the same
        # SessionStart organ.
        try:
            from scripts import arm_hooks as _ah
        except ImportError:
            import arm_hooks as _ah
        attrs = Path(repo_path) / ".gitattributes"
        # Gated on the pin being DECLARED: a repo that never asks for `merge=ours` has
        # nothing to arm, so an unset driver there is not a gap. The check is derived from
        # the tree rather than hardcoded, so retiring the pin retires this leg with it.
        pinned = attrs.is_file() and "merge=ours" in attrs.read_text(encoding="utf-8",
                                                                    errors="replace")
        if pinned and not _ah.merge_driver_armed(Path(repo_path)):
            issues.append("merge.ours.driver unset — the .gitattributes `merge=ours` pin on "
                          "docs/audits/README.md is inert ([#590]); run "
                          "`git config --local merge.ours.driver true`")
        if issues:
            return [Finding("hooks_armed", "fail",
                            ("git hooks not armed (RF-2) — SessionStart self-arm should install "
                             "them: " + "; ".join(issues)).replace("|", "/"))]
        return [Finding("hooks_armed", "pass",
                        "pre-commit / commit-msg / pre-push installed and pre-commit-managed"
                        + ("; merge.ours.driver armed for the declared merge=ours pin"
                           if pinned else "; no merge=ours pin declared"))]
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("hooks_armed", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]


# rule: governance-backlog-leave
def check_git_backlog_drift(repo_path: Path) -> list[Finding]:
    """#90 git<->backlog reconciliation (direction (a) STRONG, ADR-65).

    Hub-only: ALL_CHECKS runs per-repo across the fleet, but the `closes [#id]`
    convention + ADR-65 "done items leave" are .dev-knowledge-specific, so on any
    other repo this is a no-op pass. On the hub: a `closes [#id]` commit (full
    history) whose `[#id]` is still present in BACKLOG.md is drift — the closing
    commit fired but the done item never left the file.

    Awareness layer, not a gate: emits WARN on drift (never FAIL → `health` exits 1
    only on FAIL, so this never blocks the audit-health commit gate). Fail-soft on
    any error — a git/parse hiccup must never wedge `audit.py health`. Read-only.
    Detection + formatting live in scripts/validate_git_backlog.py (reused).
    """
    if not _is_hub(repo_path):
        return [_na("git_backlog_drift", "NOT-APPLICABLE",
                        "hub-only — git<->backlog drift check skipped (not the hub repo)")]
    try:
        drift = _vgb.reconcile(Path(repo_path), Path(repo_path) / "BACKLOG.md")
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("git_backlog_drift", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if not drift:
        return [Finding("git_backlog_drift", "pass",
                        "no closed-but-present backlog drift (direction (a) STRONG, full history)")]
    # ONE Finding per drifted id (atomic). A single aggregate WARN would let the #147
    # ship-gate disposition the WHOLE finding on one matched id and wave a DIFFERENT,
    # undispositioned drift through (Codex CRITICAL 2026-06-10): dispositions match a
    # whole Finding, so the disposition unit must equal the concern unit. Per-id findings
    # gate each drift independently. format_findings({id: ...}) reused (no parallel logic).
    return [
        Finding("git_backlog_drift", "warn",
                ("closed-but-present (ADR-65 done-items-leave): "
                 + _vgb.format_findings({cid: drift[cid]})).replace("|", "/"))
        for cid in sorted(drift, key=int)
    ]


# rule: coherence-doc-claims
def check_doc_claims(repo_path: Path) -> list[Finding]:
    """#89 prose-vs-state: a living doc's count/list CLAIMS vs repo ground truth.

    Hub-only: the claim anchors (ARCHITECTURE "N registered checks", "pre-commit gates
    (N)", CLAUDE §9 roster) are .dev-knowledge-specific, so on any other repo this is a
    no-op pass. Catches edited-but-not-reconciled prose that check #10 (last_reviewed
    staleness) and #13 (HANDOFF version stamps) cannot see; cross-file fidelity / rot
    is #140's, not this check's.

    Awareness layer, not a gate: emits WARN on a mismatch, an anchor-not-found, or a
    could-not-compute (never FAIL → never blocks the audit-health commit gate).

    SHIP-TIER SINCE [#597], and that is the second half of retiring `_GATE_MODE`. This check
    used to run at commit in a degraded posture — everything but the expensive claim-3
    (`pytest --collect-only`), suppressed by `run_expensive=not _GATE_MODE`. Declaring the whole
    check ship-tier says the same thing without a global: it cannot block a commit (WARN-only,
    and the live-repo contract is pinned by
    `tests/test_validate_doc_claims.py::test_registered_check_never_fails_on_live_repo`), so its
    teeth are at ship-gate, and claim-3 now always runs where the check runs. The cost this
    trades away is the 78 ms degraded run the commit gate used to pay; the cost it stops paying
    is the branch that made "which claims actually ran?" depend on a module global.

    Fail-soft on any error. Read-only. Logic lives in scripts/validate_doc_claims.py.
    """
    if not _is_hub(repo_path):
        return [_na("doc_claims", "NOT-APPLICABLE",
                        "hub-only — prose-vs-state check skipped (not the hub repo)")]
    try:
        results = _vdc.reconcile(Path(repo_path), len(ALL_CHECKS),
                                 run_expensive=True)
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("doc_claims", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    mismatches = [r for r in results if r.status == "mismatch"]
    missing = [r for r in results if r.status == "anchor-missing"]
    # A fail_closed claim that could not compute its ground truth (STANDING_RULINGS
    # section U). This adapter ALWAYS injects len(ALL_CHECKS), so the only claim that can
    # reach 'not-computed' cannot do so here -- the branch exists so the status can never
    # go SILENT if a future claim is marked fail_closed with a deriver that can return
    # None. Reported ahead of mismatch (not-run outranks drift: a claim that did not run
    # says nothing about drift either way) and still WARN, never FAIL: this check's
    # never-block-the-commit-gate posture is a separate ruling and is not widened here.
    #
    # NOTE the ClaimResult status is 'not-computed', NOT 'unavailable'. `Finding.status`
    # already has an "unavailable" value and it is GREEN -- it renders as N/A and
    # `_check_outcome` projects it onto `pass`. `check_silent_rule_ratchet` records the
    # same trap ("FAIL, not 'unavailable'", terra HIGH 2026-07-27). Reusing that word for
    # a status that must NOT read as green would import exactly the wrong connotation.
    not_computed = [r for r in results if r.status == "not-computed"]
    if not_computed:
        evidence = (f"{len(not_computed)} claim(s) NOT CHECKED (ground truth not computed): "
                    + ", ".join(f"{u.name}@{u.doc}" for u in not_computed)).replace("|", "/")
        return [Finding("doc_claims", "warn", evidence)]
    if mismatches:
        evidence = (f"{len(mismatches)} prose claim(s) drifted from repo state: "
                    + _vdc.format_findings(results)).replace("|", "/")
        return [Finding("doc_claims", "warn", evidence)]
    if missing:
        evidence = ("anchor(s) not found (doc reworded? re-anchor or accept): "
                    + ", ".join(f"{m.name}@{m.doc}" for m in missing)).replace("|", "/")
        return [Finding("doc_claims", "warn", evidence)]
    matched = sum(1 for r in results if r.status == "match")
    return [Finding("doc_claims", "pass",
                    f"{matched} doc self-claim(s) match repo state")]


# rule: coherence-doc-rot
def check_doc_rot(repo_path: Path) -> list[Finding]:
    """#140 doc-rot / grooming checker — the Layer-2 deterministic-trigger for **ADR-88 FC4**
    (history-accretion bloat). Surfaces inline-history accretion so it can't rot silently, and
    (riding this gate) blocks NEW accretion going forward. Load-bearing doctrine: condense
    inline history to git (ADR-65), retire inline changelogs (ADR-49), groom on cadence
    (ADR-41). DETECT-ONLY / condense-preserving — never edits, never removes a rule.

    Hub-only: BACKLOG.md + the hub living docs are .dev-knowledge-specific, so on any other repo
    this is a no-op pass. Five sub-detectors (BACKLOG inline-history accretion as ARM 1, BACKLOG
    row length against a declared ceiling as ARM 2, Section-history accretion, file-bloat vs a
    declared budget, grooming-cadence lapse) — scripts/validate_doc_rot.py.

    Awareness layer, not a gate: emits one WARN PER rot locus (never FAIL -> never blocks the
    audit-health commit gate; one Finding per locus so the #147 ship-gate dispositions each
    independently — same contract as git_backlog_drift / no_ff_merges). Scope boundary: #140's
    cross-file fidelity drift -> coherence-spine (#179/#180/#182, #89 owns one doc's OWN
    self-claims); intra-file duplication -> #190 — both deferred, not built here. Fail-soft on
    any error. Read-only. Logic lives in scripts/validate_doc_rot.py.
    """
    if not _is_hub(repo_path):
        return [_na("doc_rot", "NOT-APPLICABLE",
                        "hub-only — doc-rot / grooming checker skipped (not the hub repo)")]
    try:
        results = _vdr.scan(Path(repo_path))
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("doc_rot", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if not results:
        return [Finding("doc_rot", "pass",
                        "no history-accretion bloat past thresholds "
                        "(backlog / section-history / file-budget / grooming-cadence)")]
    return [
        Finding("doc_rot", "warn",
                f"history-accretion bloat: {_vdr.format_findings([r])}".replace("|", "/"))
        for r in results
    ]


def check_undeclared_edges(repo_path: Path) -> list[Finding]:
    """#179 undeclared-edge scan wired as a ship-gate WARN leg (Fable consult #1 ruling #2,
    2026-07-03). Surfaces docs that reference a registered spec in PROSE but carry no
    `reconciled_with: <spec>@<ver>` declaration (ADR-88 failure class FC2) — the DISCOVERY half
    of the coherence spine that validate_reconciliation's staleness gate (which only sees
    already-declared edges) is blind to.

    Hub-only: the spec registry + the tracked-mutable corpus are .dev-knowledge-specific, so on
    any other repo this is a no-op pass (mirrors check_doc_rot / check_git_backlog_drift).

    Awareness layer: emits one WARN PER candidate (never FAIL -> never blocks the audit-health
    commit gate; one Finding per candidate so the #147 ship-gate dispositions each independently
    — same contract as doc_rot / git_backlog_drift). A discovery reporter, NOT a doc->code
    behavioral rule -> `exempt` in ecosystem/doc-code-edge.yaml (same posture as
    check_enforcement_coverage). Fail-soft: any error -> WARN. Read-only; logic in
    scripts/scan_undeclared_edges.py.

    Tier filter (architect-noted): only Tier<=2 candidates (scan_undeclared_edges._CANDIDATE_TIER_MAX)
    are WARNed. Tier-3 rows are the scan's own explicitly-designated WEAK signals — bare-name prose
    mentions, human-promotable, NOT confirmed content-dependencies — and format_report splits them
    off the same way. Filtering to Tier<=2 mirrors the tool's own candidate definition; it does NOT
    hide a genuine undeclared edge (a Tier-3 bare mention is not yet a confirmed edge). The standalone
    reporter (scripts/scan_undeclared_edges.py) still surfaces the Tier-3 signals for human promotion.
    """
    if not _is_hub(repo_path):
        return [_na("undeclared_edges", "NOT-APPLICABLE",
                        "hub-only — undeclared-edge scan skipped (not the hub repo)")]
    try:
        cands = _sue.scan(Path(repo_path))
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("undeclared_edges", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    candidates = [c for c in cands if c.best_tier <= _sue._CANDIDATE_TIER_MAX]
    if not candidates:
        return [Finding("undeclared_edges", "pass",
                        "no undeclared prose edges (tier<=2) — every registered-spec prose "
                        "reference is declared (reconciled_with) or a tier-3 weak signal")]
    return [
        Finding("undeclared_edges", "warn",
                (f"undeclared prose edge (ADR-88 FC2): {c.dependent_path} -> {c.spec_id} "
                 f"(tier {c.best_tier}) — declare `reconciled_with` or disposition")
                .replace("|", "/"))
        for c in candidates
    ]


# rule: coherence-doc-structure
def check_doc_structure(repo_path: Path) -> list[Finding]:
    """Prose **structural** linter (supplement organ #2) — the Layer-2 deterministic-trigger
    for **ADR-88's prose-shape coherence**: section-numbering integrity, header-scheme
    consistency, ToC accuracy. Surfaces the structural rot the architect provably cannot
    eyeball (proven 2/2 false this session: the PLAYBOOK §18 gap + embedded-template H2s).
    DETECT-ONLY — never edits / renumbers / auto-fixes.

    Hub-only: the living docs scanned are .dev-knowledge-specific, so on any other repo this
    is a no-op pass. Five sub-detectors (numbering integrity, header-scheme consistency, ToC
    accuracy, dangling-allow self-policing, Ch/§ two-part heading-scheme integrity) —
    scripts/validate_doc_structure.py. Documented-intentional cases pass via co-located
    `structure-allow` markers + the fence-aware parser.

    Awareness layer, not a gate: emits one WARN PER structural locus (never FAIL -> never
    blocks the audit-health commit gate; one Finding per locus so the #147 ship-gate
    dispositions each independently — same contract as doc_rot / git_backlog_drift). Distinct
    failure class from #140 (history-accretion bloat) — follows its pattern, no overlap.
    Fail-soft on any error. Read-only. Logic lives in scripts/validate_doc_structure.py.
    """
    if not _is_hub(repo_path):
        return [_na("doc_structure", "NOT-APPLICABLE",
                        "hub-only — prose structural linter skipped (not the hub repo)")]
    try:
        results = _vds.scan(Path(repo_path))
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("doc_structure", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if not results:
        return [Finding("doc_structure", "pass",
                        "no structural rot (numbering / headers / ToC / dangling-allow / heading-scheme)")]
    return [
        Finding("doc_structure", "warn",
                f"structural rot: {_vds.format_findings([r])}".replace("|", "/"))
        for r in results
    ]


# rule: governance-no-ff
def check_no_ff_merges(repo_path: Path) -> list[Finding]:
    """#153 `--no-ff` merge guard (core-invariants rule 5).

    Hub-only: the rule + the sanctioned-automation allowlist are tuned to
    .dev-knowledge's main, so on any other repo this is a no-op pass (a fleet-wide
    expansion is deferred under #153). Surfaces a non-merge commit on main's
    first-parent spine since the enforcement baseline — a direct-to-main commit or a
    fast-forwarded feature commit the `--no-ff` rule forbids — that does NOT carry an
    ADR-80 automation marker (`chore(routine/…)` scope or a `Routine:` trailer).

    Awareness layer, not a gate: emits one WARN per violation (never FAIL → never
    blocks the audit-health commit gate; one Finding per violation so the #147
    ship-gate dispositions them independently — same contract as git_backlog_drift).
    DETECT-AND-SURFACE, not prevent: git fires no commit-hook on a fast-forward, so
    this cannot block the merge itself; it removes the silence (true prevention = a
    pre-push hook, deferred under #153). Fail-soft on any error. Read-only. Detection
    lives in scripts/validate_no_ff.py.
    """
    if not _is_hub(repo_path):
        return [_na("no_ff_merges", "NOT-APPLICABLE",
                        "hub-only — --no-ff guard skipped (not the hub repo)")]
    try:
        violations = _vnf.find_violations(Path(repo_path))
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("no_ff_merges", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if not violations:
        return [Finding("no_ff_merges", "pass",
                        f"no non-merge commits on main since {_vnf.BASELINE_DATE} "
                        "(--no-ff rule, core-invariants #5; one rule, no exemptions — ADR-84)")]
    return [
        Finding("no_ff_merges", "warn",
                ("non-merge commit on main (FF/direct — expected a --no-ff merge): "
                 + _vnf.format_one(v)).replace("|", "/"))
        for v in violations
    ]


def _bundle_target_repo(bundle_dir: Path) -> str | None:
    """The declared cross-repo target from a bundle's HANDOFF_BOOT.md `Target repo` row
    (e.g. `ai-council`), or None when the bundle carries no such row (a self-handoff).

    Cross-repo handoffs (ADR-36/41) name their target in the session-header table row
    "| **Target repo** | **<repo>** ... |" (repo in a backtick span); the target is the
    first backtick span of that row. Read-only; fail-soft (any read/parse issue -> None ->
    treated as a self-handoff)."""
    boot = bundle_dir / "HANDOFF_BOOT.md"
    if not boot.exists():
        return None
    try:
        for line in boot.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("|") and "target repo" in s.lower():
                m = re.search(r"`([^`]+)`", s)
                if m:
                    return m.group(1).strip()
    except OSError:
        return None
    return None


# Repo-location env vars git inherits from a hook/pre-commit parent; GIT_DIR overrides both
# `cwd=` and `-C` ([#355]). The definition was DUPLICATED here rather than imported, because
# audit.py imports fleet_parity LAZILY (inside check_fleet_parity, for dual script/package
# mode) and bundle selection must not acquire a dependency on that import path. [#396]
# resolves that without weakening it: the canonical pair now lives in `scripts/gitenv.py`, a
# LEAF module -- stdlib-only, zero repo imports -- so importing it here adds no import-path
# risk of the kind the lazy-import constraint exists to avoid. Semantics unchanged: derived
# from `git rev-parse --local-env-vars`, scrubbed by NAME, never a `startswith("GIT_")` strip
# (that would also drop GIT_CONFIG_GLOBAL / GIT_AUTHOR_* / GIT_SSH_COMMAND).
#
# WHERE it fires is unchanged and still decided HERE, not in gitenv: applied inside
# _select_active_bundle's runner, check_fleet_audit_replication and _push_routine_branch, and
# deliberately NOT applied to the fleet-automation commit path further down, which sets
# GIT_INDEX_FILE ON PURPOSE via its own explicit env= dict -- routing that through this scrub
# would silently break it.
_GIT_LOCATION_ENV_EXTRA = _gitenv.GIT_LOCATION_ENV_EXTRA
_GIT_LOCATION_ENV_FALLBACK = _gitenv.GIT_LOCATION_ENV_FALLBACK
_git_location_env = _gitenv.git_location_env

# ONE `git log` for ALL candidate bundles, not one per directory. Measured on the live
# tree before the change: 87 candidates -> 87 process spawns / 26.3 s, inside an
# `audit.py health` that wall-clocked 82.8 s -- roughly a third of the gate spent asking
# 87 times a question one pathspec-limited walk answers.
#
# CHUNKED above a stated bound rather than unbounded, because argv is finite: Windows caps
# a command line at 32767 characters, so an unbounded pathspec list turns from a speedup
# into a crash at some corpus size instead of degrading. The budget below is pathspec
# bytes only, leaving the `git -C <absolute repo path> -c core.quotePath=false log ...`
# prefix its own room; at ~51 chars per bundle path it holds ~470 bundles in ONE call,
# against a live corpus needing ~4.4 KB. So the invocation count is O(chunks) -- driven by
# argv length, never by candidate count -- and is 1 for any plausible corpus here.
_BUNDLE_LOG_PATHSPEC_BUDGET = 24_000


def _chunk_pathspecs(paths: list[str]) -> list[list[str]]:
    """Split `paths` into argv-length-bounded chunks. Never splits a single pathspec."""
    budget = _BUNDLE_LOG_PATHSPEC_BUDGET
    chunks: list[list[str]] = []
    chunk: list[str] = []
    used = 0
    for p in paths:
        cost = len(p) + 1                       # +1 for the argv separator
        if chunk and used + cost > budget:
            chunks.append(chunk)
            chunk, used = [], 0
        chunk.append(p)
        used += cost
    if chunk:
        chunks.append(chunk)
    return chunks


def _select_active_bundle(
    repo_path: Path, candidates: list[Path]
) -> tuple[Optional[Path], str, str]:
    """Pick the ACTIVE handoff bundle from `candidates` by GIT ADD DATE, not slug order.

    Returns ``(bundle, kind, detail)`` where kind is one of:
      "sole"      -- exactly one candidate; no git needed
      "fresh"     -- exactly one candidate with no add-commit (untracked OR staged): the
                     bundle being generated right now, so it outranks every tracked one
      "add-date"  -- newest first-add commit among the tracked candidates
      "no-git"    -- not a git repo / unborn HEAD -> lexical-max fallback (legacy heuristic;
                     a bundle is still returned, so the check stays useful)
      "ambiguous" -- >=2 candidates are fresh; `bundle` is None. NEVER silently pick one:
                     a silent pick between two uncommitted bundles is the same "green about
                     the wrong file" class this selector exists to kill.
      "degraded"  -- git present but a probe errored; `bundle` is None -> caller WARNs.

    WHY not lexical (the defect this replaces): "2026-07-20-dev-knowledge-architect-arc5"
    sorts AFTER "2026-07-20-dev-knowledge-architect" because "-arc5" > "", yet arc5 was
    git-added 2026-07-19 and the plain slug 2026-07-20 -- so the gate validated a stale
    bundle and reported green about the wrong file while the active bundle went unchecked.
    mtime is not usable as a tiebreak: a git worktree checkout re-stamps every file.

    Read-only; fail-soft. EVERY git call here runs through the scrubbed env -- an inherited
    GIT_DIR would resolve the guard below to the WRONG toplevel and silently degrade
    selection to the lexical fallback, reintroducing the exact bug ([#355] recursion).
    """
    lexical = max(candidates, key=lambda d: d.name)
    if len(candidates) == 1:
        return candidates[0], "sole", candidates[0].name

    scrub = _git_location_env()
    env = {k: v for k, v in os.environ.items() if k not in scrub}

    def _run(args: list[str]) -> Optional[str]:
        try:
            p = subprocess.run(["git", "-C", str(repo_path), *args], capture_output=True,
                               text=True, encoding="utf-8", errors="replace", env=env)
        except OSError:
            return None
        return p.stdout if p.returncode == 0 else None

    # Guard: an empty `--diff-filter=A` means "never added" ONLY inside a real repo whose
    # root IS repo_path. Without this, a temp dir nested under some ancestor repo reports
    # every bundle as fresh -> a bogus ambiguous FAIL.
    #
    # The three failure shapes below are deliberately NOT collapsed into one lexical
    # fallback. Collapsing them is how the stale-bundle false green returns: a git
    # misconfiguration would silently restore exactly the behaviour this selector replaces.
    # Only a confirmed NON-git tree earns the legacy heuristic; everything else degrades
    # loudly.
    top = _run(["rev-parse", "--show-toplevel"])
    if not top or not top.strip():
        # Not a git repo (or git absent). The legacy lexical heuristic is the honest
        # degradation here -- a non-git consumer still gets its bundle validated.
        return lexical, "no-git", lexical.name
    try:
        same = (os.path.normcase(str(Path(top.strip()).resolve()))
                == os.path.normcase(str(Path(repo_path).resolve())))
    except OSError:
        same = False
    if not same:
        # repo_path is nested inside a DIFFERENT repo, so add-dates would be read from the
        # wrong history. Never fall back silently -- surface it.
        return None, "degraded", (f"git toplevel {top.strip()} is not {repo_path} "
                                  "(nested repo?) — cannot trust add-dates")
    if _run(["rev-parse", "--verify", "HEAD"]) is None:
        # Unborn HEAD in a real repo: nothing is committed, so EVERY candidate is
        # genuinely fresh. Fall into the ambiguity rule rather than picking lexically --
        # otherwise a fresh repo with two bundles silently gets the wrong one.
        return None, "ambiguous", ", ".join(sorted(d.name for d in candidates))

    # ONE `git log` over ALL the candidate pathspecs (chunked only above the argv budget),
    # parsed back into exactly the per-directory add-dates the per-directory form produced.
    #
    # No `-1`: git applies -1 BEFORE --reverse, which would yield the NEWEST commit.
    # %at (author unix seconds) not %aI: an integer cannot misorder across timezone
    # offsets, and author-date survives a rebase that rewrites committer dates.
    # --reverse is oldest-first, so the FIRST commit naming a bundle carries its add-date
    # -- the same value `lines[0]` carried when each directory was walked alone.
    #
    # `--name-only` is what makes attribution possible at all: %at gives the commit's date,
    # the file names say WHICH bundle that commit added. The \x02 sentinel separates the
    # two, so a filename can never be misread as a timestamp.
    #
    # Attribution splits on PATH SEGMENTS, never a string prefix: "2026-07-20-x" is a
    # prefix of "2026-07-20-x-arc5", and crediting arc5's add-commit to the plain slug
    # turns the active bundle into a stale one -- the #372 "green about the wrong file"
    # defect this selector exists to kill, re-entering through the batching door.
    # `core.quotePath=false` keeps a non-ASCII slug from arriving octal-escaped and
    # silently unmatchable, which would misreport a tracked bundle as fresh.
    wanted = {d.name for d in candidates}
    add_dates: dict[str, int] = {}
    for chunk in _chunk_pathspecs([f"docs/handoffs/{d.name}" for d in candidates]):
        out = _run(["-c", "core.quotePath=false", "log", "--diff-filter=A", "--reverse",
                    "--format=%x02%at", "--name-only", "--", *chunk])
        if out is None:
            # The SAME outcome the per-directory form gave a failing `git log`. A batching
            # optimisation must not change a failure mode, and it must never fall back to
            # the lexical heuristic -- that fallback IS the defect this function replaced.
            return None, "degraded", f"batched git log failed for {len(chunk)} bundle path(s)"
        stamp: Optional[int] = None
        for line in out.splitlines():
            if line.startswith("\x02"):
                try:
                    stamp = int(line[1:].strip())
                except ValueError:
                    return None, "degraded", f"unparseable add-date {line[1:].strip()!r}"
                continue
            parts = line.strip().split("/", 3)
            if stamp is None or len(parts) < 4 or parts[:2] != ["docs", "handoffs"]:
                continue
            if parts[2] in wanted:
                add_dates.setdefault(parts[2], stamp)   # oldest wins: --reverse ordering

    fresh: list[Path] = []
    dated: list[tuple[int, str, Path]] = []
    for d in candidates:
        when = add_dates.get(d.name)
        if when is None:
            fresh.append(d)          # untracked, or staged-but-never-committed
        else:
            dated.append((when, d.name, d))

    if len(fresh) > 1:
        return None, "ambiguous", ", ".join(sorted(d.name for d in fresh))
    if len(fresh) == 1:
        return fresh[0], "fresh", fresh[0].name
    if not dated:
        return lexical, "no-git", lexical.name
    dated.sort(key=lambda t: (t[0], t[1]))   # add-date, then slug as a stable tiebreak
    return dated[-1][2], "add-date", dated[-1][1]


# rule: handoff-probes-bind
def check_handoff_probes(repo_path: Path) -> list[Finding]:
    """#163 handoff-probe teeth: every probe in the LATEST v5 PROBES.md bundle binds
    to live state (structural, RESOLVE-ONLY — Critical Rule #4 "Layer 2 never executes",
    zero false positives). Mechanizes the manual v5 probe-gate (HANDOFF_PROCESS §5/§10).

    Bundle-presence-based: validates the ACTIVE docs/handoffs/<slug>/PROBES.md (excluding
    aborted/in-progress/archive); a repo with no such bundle is a no-op pass, so this
    no-ops on the fleet's child repos. Only the ACTIVE handoff is checked — older bundles
    are immutable historical artifacts whose source anchors legitimately drift, so
    re-validating them against current state would mis-flag.

    "Active" is decided by _select_active_bundle: an uncommitted bundle (the one being
    generated now), else the newest by GIT ADD DATE — never slug order, which picked a
    stale "<date>-<slug>-arc5" over the newer "<date>-<slug>" ([#372]). Two uncommitted
    bundles is ambiguous → FAIL, never a silent pick.

    FAIL-class (gating, unlike the WARN-only doc_claims): a malformed row or a missing
    source/command-target FAILs -> Finding "fail" -> the audit-health + ship-gate block
    (a toothless probe cannot ship). A moved anchor / absent tool -> WARN (anchor-missing
    / skipped: degrade loudly, never a synthesized pass). The "Why" column is checked for
    PRESENCE only — rationale quality stays the manual gate. Fail-soft on any error.
    Read-only. Logic lives in scripts/verify_handoff_probes.py.
    """
    handoffs = Path(repo_path) / "docs" / "handoffs"
    if not handoffs.exists():
        return [_na("handoff_probes", "NOT-APPLICABLE",
                        "no docs/handoffs/ — no probe bundle to validate")]
    candidates = sorted(
        (d for d in handoffs.iterdir()
         if d.is_dir() and d.name not in _BUNDLE_EXCLUDE_DIRS
         and (d / "PROBES.md").exists()),
        key=lambda d: d.name,
    )
    if not candidates:
        return [Finding("handoff_probes", "pass",
                        "no v5 PROBES.md bundle to validate")]
    latest, kind, detail = _select_active_bundle(Path(repo_path), candidates)
    if kind == "ambiguous":
        return [Finding("handoff_probes", "fail",
                        f"ambiguous active handoff bundle: {detail} are all uncommitted "
                        "— commit or remove all but one. Refusing to guess which bundle "
                        "the gate validates (a silent pick is a green about the wrong "
                        "file)".replace("|", "/"))]
    if latest is None:
        return [Finding("handoff_probes", "warn",
                        f"bundle selection degraded (read-only, non-blocking): {detail}"
                        .replace("|", "/"))]
    # Cross-repo bundle (ADR-36/41): a handoff whose declared target repo differs from this
    # one. Its probes bind to the TARGET repo's files, so resolve against the target root,
    # not the hub — resolving foreign paths against the hub gives both false FAILs (a target
    # file absent here) AND false PASSes (a basename collision like JOURNAL.md fake-resolves).
    # Fleet onboarding (#221) makes cross-repo the common case, so this keeps the teeth rather
    # than skipping them. A `.claude/` or ambiguous foreign target degrades to WARN (#234).
    target = _bundle_target_repo(latest)
    cross_repo = bool(target) and target != Path(repo_path).name
    verify_root = None
    if cross_repo:
        cand = Path(repo_path).parent / target
        if not cand.is_dir():
            return [Finding("handoff_probes", "warn",
                            f"cross-repo bundle {latest.name}: target repo '{target}' not "
                            "present as a sibling — cannot resolve foreign probe targets "
                            "(read-only, non-gating)")]
        verify_root = cand
    try:
        results = _vhp.verify(latest, repo_root=verify_root, cross_repo=cross_repo)
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("handoff_probes", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if not results:
        # PROBES.md exists (it is why this bundle was selected) but parses to zero probe
        # rows -> a toothless manifest. Not a silent pass: a v5 bundle must ship probes.
        return [Finding("handoff_probes", "fail",
                        f"{latest.name}/PROBES.md present but no parseable probe rows "
                        "(toothless manifest)")]
    # One Finding per non-passing probe so the #147 ship-gate dispositions each
    # independently (same contract as git_backlog_drift / no_ff_merges): an aggregate
    # WARN would let one disposition mask an unrelated degraded probe.
    findings: list[Finding] = []
    for r in results:
        if r.status == "fail":
            findings.append(Finding("handoff_probes", "fail",
                f"{r.probe_id} toothless in {latest.name}: {r.detail}".replace("|", "/")))
        elif r.status in ("anchor-missing", "skipped"):
            findings.append(Finding("handoff_probes", "warn",
                f"{r.probe_id} {r.status} in {latest.name}: {r.detail}".replace("|", "/")))
    if findings:
        return findings
    return [Finding("handoff_probes", "pass",
                    f"{len(results)} probe(s) bind to live state ({latest.name})")]


# The ERA `supplement_folded` binds from — the date the check landed. A bundle cut before it
# is GRANDFATHERED: named in the evidence, never blocking. This is not leniency, it is the
# only honest option. A sealed bundle's PASTE_THIS.md is an immutable artifact (Critical
# Rule #3), and the loss it records already happened — the seat that needed the 2026-08-23
# answers booted on 2026-08-25 without them. Re-assembling that paste now would edit an
# immutable artifact to falsify what was actually delivered, and it would not un-lose
# anything. Recorded as IMMUTABLE-AND-LOST instead, permanently visible in the gate's own
# output. (A disposition-register entry could not carry this even if it were the right
# answer: the register suppresses WARNs, and this check is FAIL-class.)
# The era boundary is applied by `_vhp.bundle_at_or_after` — the SAME predicate the §5 cond. 4
# boundedness rung uses, reused rather than written a second time. A bare string compare against
# the whole directory name looks equivalent and is not: `2026-08-9-foo` compares GREATER than
# `2026-08-26` on its 9th character, so a pre-era bundle would be blocked by a later era's rule,
# while `2026-08-2` would be waved through. Caught by terra pass 1 on this lane's own diff.
_SUPPLEMENT_FOLD_ERA = "2026-08-26"
_SUPPLEMENT_SECTION_MARKER = "=== SUPPLEMENT.md ==="
# The reason-prefix marking "this bundle could not be READ", as distinct from "this bundle is
# unfolded". Degraded coverage is reported, never counted as a pass (HANDOFF_PROCESS §5's own
# words, and the ladder every validator here follows).
_SUPPLEMENT_UNREADABLE = "unreadable"


def _path_state(p: Path) -> str:
    """`'file'` | `'dir'` | `'absent'` | `'unreadable'` for a path.

    `Path.is_file()` / `Path.is_dir()` cannot carry this: BOTH swallow OSError and return False,
    so a path the process may not stat (a Windows share lock, an ACL change) is indistinguishable
    from one that was never created — and `supplement_folded` treats "never created" as a
    legitimate skip. Every stat failure other than genuine absence is surfaced instead.

    Found by terra across three passes on this lane's own diff, one level at a time: the READ of
    a bundle file (pass 2), the STAT of a bundle file (pass 3), then the stat of the bundle
    DIRECTORY and of `docs/handoffs/` itself (pass 4). One helper now covers all four, which is
    why it is a state enum rather than a boolean."""
    try:
        st = os.stat(p)
    except (FileNotFoundError, NotADirectoryError):
        return "absent"
    except OSError:
        return "unreadable"
    if _stat.S_ISREG(st.st_mode):
        return "file"
    return "dir" if _stat.S_ISDIR(st.st_mode) else "absent"


def supplement_fold_violations(repo_path: Path) -> list[tuple[str, str]]:
    """Every bundle whose SUPPLEMENT ANSWERS are filled but whose PASTE_THIS.md never folded
    them. Returns `(bundle_name, reason)` pairs sorted by name; [] when clean.

    R4 of the 2026-08-26 handoff census (b6). The supplement is filled AFTER the paste is
    assembled and no organ re-folded it: 63 bundles carry both a filled ANSWERS region and an
    assembled paste, 62 folded, and the one that did not is the most recent architect handoff
    before the census. Its 87 answer lines — rulings, rejections, off-repo context, the Q7
    register — never reached the next seat, and the failure was silent.

    The fill-state predicate is `assemble_paste._extract_answers`, REUSED rather than
    reimplemented, so "filled" means here exactly what the assembler means by it (the same
    reuse `gen_handoff.detect_fill_state` already makes). Two deliberate non-violations: a
    COLD supplement (an honest record of a duty undischarged, and what the assembler declines
    to fold), and a bundle with no PASTE_THIS.md at all (nothing was assembled, so no fold was
    missed). Read-only; era-blind — the era gate lives in the adapter below, so this predicate
    can be run against the real tree to reproduce the historical RED.

    A bundle file that cannot be READ is reported as its own outcome, its reason prefixed
    `_SUPPLEMENT_UNREADABLE`, rather than dropped: dropping it would let the adapter return a
    clean pass about evidence it never opened. The adapter maps that prefix to a WARN.
    """
    handoffs = Path(repo_path) / "docs" / "handoffs"
    root_state = _path_state(handoffs)
    if root_state == "unreadable":
        return [("docs/handoffs", f"{_SUPPLEMENT_UNREADABLE}: the bundle root could not be "
                                  "stat'ed — no bundle could be examined")]
    if root_state != "dir":
        return []
    try:
        from assemble_paste import _extract_answers  # noqa: PLC0415
    except ImportError:
        from scripts.assemble_paste import _extract_answers  # noqa: PLC0415
    out: list[tuple[str, str]] = []
    try:
        entries = sorted(handoffs.iterdir(), key=lambda d: d.name)
    except OSError as exc:
        return [("docs/handoffs", f"{_SUPPLEMENT_UNREADABLE}: {exc.__class__.__name__} listing "
                                  "the bundle root — no bundle could be examined")]
    for bundle in entries:
        if bundle.name in _BUNDLE_EXCLUDE_DIRS:
            continue
        bundle_state = _path_state(bundle)
        if bundle_state == "unreadable":
            # Same swallow one level up: `Path.is_dir()` returns False for an OSError, so a
            # bundle directory the process may not stat would be omitted and the check could
            # then report a clean pass about evidence it never opened. (terra pass 4.)
            out.append((bundle.name, f"{_SUPPLEMENT_UNREADABLE}: the bundle directory could not "
                                     "be stat'ed — its fold state was never examined"))
            continue
        if bundle_state != "dir":
            continue
        supplement = bundle / "SUPPLEMENT.md"
        paste = bundle / "PASTE_THIS.md"
        states = {_path_state(supplement), _path_state(paste)}
        if "unreadable" in states:
            out.append((bundle.name, f"{_SUPPLEMENT_UNREADABLE}: SUPPLEMENT.md / PASTE_THIS.md "
                                     "could not be stat'ed — fold state could not be determined"))
            continue
        if "absent" in states:
            continue        # nothing was assembled, or no supplement exists — no fold to miss
        try:
            answers = _extract_answers(supplement.read_text(encoding="utf-8"))
            folded = _SUPPLEMENT_SECTION_MARKER in paste.read_text(encoding="utf-8")
        except OSError as exc:
            # DEGRADE LOUDLY. An unreadable bundle file (a Windows share lock, a permission
            # change) is exactly the moment this check could not look — and dropping it from the
            # result set would let the adapter return a clean `pass` about evidence it never
            # read, which is the synthesized-pass class this repo's validators refuse
            # everywhere else. Reported as its own outcome; the adapter maps it to a WARN.
            # Found by terra pass 2 on this lane's own diff.
            out.append((bundle.name, f"{_SUPPLEMENT_UNREADABLE}: {exc.__class__.__name__} "
                                     "reading SUPPLEMENT.md / PASTE_THIS.md — fold state "
                                     "could not be determined"))
            continue
        if answers and not folded:
            out.append((bundle.name,
                        "SUPPLEMENT ANSWERS filled but PASTE_THIS.md carries no "
                        f"{_SUPPLEMENT_SECTION_MARKER} section"))
    return out


def check_supplement_folded(repo_path: Path) -> list[Finding]:
    """R4 (census 2026-08-26 b6): a filled SUPPLEMENT that never reached the paste is a
    silent, irreplaceable loss of the outgoing architect's judgment. FAIL-class (gating,
    like check_handoff_probes): a bundle cut in this era with filled ANSWERS and an unfolded
    paste blocks audit-health and the ship-gate, so the fix happens while the bundle is
    still live rather than being discovered by the seat that needed it.

    ONE Finding PER offending bundle (the #147 disposition contract — an aggregate finding
    would let one match wave through an unrelated bundle).

    Pre-era bundles are grandfathered and NAMED in the pass evidence: see
    `_SUPPLEMENT_FOLD_ERA` for why repairing them is not on the table. A bundle whose files
    could not be read is a WARN, emitted ALONGSIDE whatever else the run found and never
    collapsed into a pass — degraded coverage is reported, never counted as a pass. Read-only.

    HONEST LIMIT: this asserts the paste carries a SUPPLEMENT section, not that the section
    carries the CURRENT answers. A supplement edited after a fold still reads as folded.
    Catching that needs a content comparison the assembler does not record, and the failure
    class measured — a fold that never happened at all — is the one this refuses.
    """
    handoffs = Path(repo_path) / "docs" / "handoffs"
    # `Path.is_dir()` swallows OSError, so an unreadable handoffs root would report NOT-APPLICABLE
    # — "there is nothing here" — when the truth is "this could not be looked at". Degraded
    # coverage stays visible to the ship-gate instead. (terra pass 4.)
    root_state = _path_state(handoffs)
    if root_state == "unreadable":
        return [Finding("supplement_folded", "warn",
                        "docs/handoffs: the bundle root could not be stat'ed — no bundle was "
                        "examined (degraded coverage, read-only)")]
    if root_state != "dir":
        return [_na("supplement_folded", "NOT-APPLICABLE",
                    "no docs/handoffs/ — no bundle whose supplement could be unfolded")]
    try:
        violations = supplement_fold_violations(Path(repo_path))
    except Exception as exc:  # never wedge the gate on an internal error
        return [Finding("supplement_folded", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    in_era = _vhp.bundle_at_or_after
    unreadable = [(b, why) for b, why in violations
                  if why.startswith(_SUPPLEMENT_UNREADABLE)]
    readable = [(b, why) for b, why in violations
                if not why.startswith(_SUPPLEMENT_UNREADABLE)]
    blocking = [(b, why) for b, why in readable if in_era(b, _SUPPLEMENT_FOLD_ERA)]
    grandfathered = [b for b, _ in readable if not in_era(b, _SUPPLEMENT_FOLD_ERA)]
    # Degraded coverage is SURFACED whatever else the run found — reporting a clean pass about
    # evidence that could not be read is the one outcome this check may not produce.
    degraded = [Finding("supplement_folded", "warn",
                        f"{b}: {why} (degraded coverage, read-only)".replace("|", "/"))
                for b, why in unreadable]
    if blocking:
        return degraded + [
            Finding("supplement_folded", "fail",
                    f"{b}: {why} — the outgoing seat's answers never reached the next "
                    "one; re-run scripts/assemble_paste.py on the bundle before it seals"
                    .replace("|", "/"))
            for b, why in blocking]
    if degraded:
        return degraded
    tail = (" — pre-era, immutable-and-lost (recorded, not repaired): "
            + ", ".join(grandfathered)) if grandfathered else ""
    return [Finding("supplement_folded", "pass",
                    f"every filled SUPPLEMENT reached its paste{tail}".replace("|", "/"))]


def check_dispatch_verb_agreement(repo_path: Path) -> list[Finding]:
    """R5: the drift organ `protocols/STANDING_RULINGS.md` §V records as "owed and unbuilt".

    §V ruled `dispatch <contract.md>` the sole operator verb for a LOCAL lane after measuring
    what four rival launch commands cost: `/lane-boot` emitted the form Ch8 itself labels a
    fallback, silently dropping `--model` and `--effort`, and roughly thirty consecutive browser
    seats failed to launch a lane. The ruling landed and nothing asserted it — §V's own words:
    "until it exists these rulings bind the seat and not the tree."

    Asserts the two point-of-use surfaces (`.claude/commands/lane-boot.md`,
    `templates/prompt-template.md`) name the verb Ch8's dispatch table rules, and carry no rival
    literal launch form in a fenced block. The ruled verb is READ from Ch8 at check-time — this
    check holds no copy of it, which is the same discipline it enforces.

    FAIL-class (gating), one Finding per violation per the #147 disposition contract. Read-only.
    Logic lives in scripts/dispatch_surface.py.

    PRESENCE-based, not `_is_hub`-based (the check_handoff_probes precedent): a repo with no
    `protocols/PLAYBOOK.md` carries no dispatch table to agree with, so it is a no-op n/a and
    this no-ops on the fleet's child repos. A repo that HAS the table and cannot read the ruled
    form out of it FAILs — a moved anchor is a finding, never a silent pass.

    HONEST LIMIT, and it is stated in the module too: this is HALF the organ §V describes. The
    other half — every literal command in Ch8 resolving via `Get-Command` on the operator's
    machine — probes an L0 surface in another repo and would require executing, which Layer 2
    does not do. A verb that agrees everywhere and resolves nowhere passes this gate.
    """
    try:
        try:
            from scripts import dispatch_surface as _ds_probe  # noqa: PLC0415
        except ImportError:
            import dispatch_surface as _ds_probe               # noqa: PLC0415
        # `Path.is_file()` swallows OSError, so an UNREADABLE PLAYBOOK would report
        # NOT-APPLICABLE — "there is no dispatch table" — when the truth is that the canonical
        # command source could not be opened. Only genuine absence is n/a; an unreadable one
        # falls through to the predicate, which reports it as a violation. (terra pass 5.)
        if _path_state(Path(repo_path) / _ds_probe.PLAYBOOK_PATH) == "absent":
            return [_na("dispatch_verb_agreement", "NOT-APPLICABLE",
                        "no protocols/PLAYBOOK.md — no dispatch table to agree with")]
    except Exception as exc:  # noqa: BLE001 — a reader that cannot load is a WARN, not a FAIL
        return [Finding("dispatch_verb_agreement", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    try:
        try:
            from scripts import dispatch_surface as _ds  # noqa: PLC0415
        except ImportError:
            import dispatch_surface as _ds               # noqa: PLC0415
        violations = _ds.agreement_findings(Path(repo_path))
    except Exception as exc:  # never wedge the gate on an internal error
        return [Finding("dispatch_verb_agreement", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if violations:
        return [Finding("dispatch_verb_agreement", "fail", v.replace("|", "/"))
                for v in violations]
    return [Finding("dispatch_verb_agreement", "pass",
                    "both point-of-use sites name the verb Ch8's dispatch table rules, and "
                    "neither carries a rival literal launch form")]


# [#533] moved to audit_checks/ — re-exported above.


def _load_declaration_docs(repo_path: Path) -> tuple[str, ...]:
    """Read the doc→code edge declaration-doc include-list (`ecosystem/doc-code-edge.yaml`,
    `declaration_docs:`) — the registry-scoped scan scope for `check_doc_code_edge`. Resolved
    from `repo_path` at call time (NOT a module constant) so the hub guard + tmp-hub tests see
    the right file. Returns repo-relative doc paths (forward slashes), in declared order.

    Fail-soft → () : a missing/malformed file renders the advisory check inert and passes —
    correct while the edge is ADVISORY. NOTE (hard-gate promotion, ADR-89 OQ1 / OQ3): when this
    edge is promoted to a gate, switch to WARN-on-missing/malformed-config so a lost config
    cannot silently disable a live gate. Read-only.
    """
    cfg = Path(repo_path) / "ecosystem" / "doc-code-edge.yaml"
    try:
        data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return ()
    if not isinstance(data, dict):
        return ()
    docs = data.get("declaration_docs")
    if not isinstance(docs, list):  # a non-list scalar must degrade, not raise
        return ()
    return tuple(d for d in docs if isinstance(d, str))


def _load_coverage_scope(repo_path: Path) -> tuple[str, ...]:
    """Read the doc->code coverage-scope rule-ID list (`ecosystem/doc-code-edge.yaml`,
    `coverage_scope:`) -- the in-scope enforced rule-IDs the #194 rollout must drive to 100%
    resolved (tests/test_doc_code_edge.py asserts each resolves, xfail-strict until complete).

    Sibling key to `declaration_docs`; same fail-soft -> () contract (a missing/malformed file
    or non-list value yields an empty scope -- the coverage test's non-empty precondition guards
    against a vacuous pass). Resolved from `repo_path` at call time. Read-only.
    """
    cfg = Path(repo_path) / "ecosystem" / "doc-code-edge.yaml"
    try:
        data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return ()
    if not isinstance(data, dict):
        return ()
    scope = data.get("coverage_scope")
    if not isinstance(scope, list):  # a non-list scalar must degrade, not raise
        return ()
    return tuple(s for s in scope if isinstance(s, str))


def _load_multi_site(repo_path: Path) -> dict[str, int]:
    """Read the doc->code multi-site expected-count map (`ecosystem/doc-code-edge.yaml`,
    `multi_site:`) -- per ADR-90 (resolver-allows-N), a rule legitimately enforced in N code
    organs declares its expected `# rule:` site count here, so the resolver resolves it at
    EXACTLY that count instead of classing it `ambiguous` (the strict 1:1 duplicate-guard).

    Sibling key to `coverage_scope`/`declaration_docs`; same fail-soft -> {} contract (a
    missing/malformed file or non-mapping value degrades every rule to the strict 1:1 guard --
    conservative: it can only NARROW what resolves, never silently widen it). Only `str -> int`
    entries with count >= 2 are kept (a bool is rejected -- `bool` is an `int` subclass).
    Resolved from `repo_path` at call time. Read-only.
    """
    cfg = Path(repo_path) / "ecosystem" / "doc-code-edge.yaml"
    try:
        data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return {}
    if not isinstance(data, dict):
        return {}
    raw = data.get("multi_site")
    if not isinstance(raw, dict):  # a non-mapping scalar must degrade, not raise
        return {}
    return {k: v for k, v in raw.items()
            if isinstance(k, str) and isinstance(v, int) and not isinstance(v, bool) and v >= 2}


def _load_coverage_exempt(repo_path: Path) -> set[str]:
    """Read the doc->code coverage drift-guard exempt-list (`ecosystem/doc-code-edge.yaml`,
    `exempt:`) -- the ALL_CHECKS members that are NOT declared doc->code behavioral rules: the
    structural/presence baseline checks + the two self-referential meta-checks (`doc_code_edge`,
    `doc_code_coverage_drift`). Entries are CHECK NAMES (a Finding `check_name` =
    `fn.__name__` minus the `check_` prefix).

    Sibling key to `coverage_scope`/`multi_site`; same fail-soft -> set() contract (a
    missing/malformed file or non-list value yields an empty set -- and `check_doc_code_coverage_drift`
    treats an empty scope-or-exempt as INERT, so an absent config cannot vacuously pass every
    member). Resolved from `repo_path` at call time. Read-only.
    """
    cfg = Path(repo_path) / "ecosystem" / "doc-code-edge.yaml"
    try:
        data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return set()
    if not isinstance(data, dict):
        return set()
    raw = data.get("exempt")
    if not isinstance(raw, list):  # a non-list scalar must degrade, not raise
        return set()
    return {s for s in raw if isinstance(s, str)}


def check_doc_code_edge(repo_path: Path) -> list[Finding]:
    """#194 doc->code declared-edge integrity (advisory-first, ADR-89 OQ1).

    Discovers every `<!-- rule: ID -->` annotation in the DECLARATION DOCS registered in
    `ecosystem/doc-code-edge.yaml` (`declaration_docs:`) and resolves each to its `# rule: ID`
    code annotation under scripts/ — rule-ID identity + path/AST content resolution, move-safe
    per the e22e883 spike. A `broken_edge` (a side resolves to nothing) or `ambiguous` (a
    duplicated ID) surfaces as a WARN advisory naming the rule-ID + reason; the #194 L1 scan
    (validate_doc_code_edge.scan_structural_integrity) ALSO surfaces a `code_orphan` — a
    `# rule:` annotation declared in no declaration doc (code->nonexistent-rule), the direction
    doc-side resolution structurally cannot see. NEVER FAILs this arc — advisory-first; promotion
    to a gate is data-gated (ADR-89 OQ3).

    Hub-only: the rule-ID edge is a .dev-knowledge governance concept, so on any other repo this
    is a no-op pass. The scan is REGISTRY-SCOPED to the authoritative declaration docs (ADR-89
    OQ1 naming convention) — illustrative `<!-- rule: <domain>-<slug> -->` tokens elsewhere
    (immutable design records, teaching sections, the test fixtures) are out of scope, and
    teaching tokens additionally use the angle-bracket placeholder form (outside the ID charset).
    An empty/absent registry → advisory inactive (fail-soft). Read-only. Discovery + resolution
    live in scripts/validate_doc_code_edge.py.
    """
    if not _is_hub(repo_path):
        return [_na("doc_code_edge", "NOT-APPLICABLE",
                        "hub-only — doc->code edge check skipped (not the hub repo)")]
    code_root = Path(repo_path) / "scripts"
    try:
        include = _load_declaration_docs(repo_path)
        multi = _load_multi_site(repo_path)  # ADR-90: declared multi-site expected counts
        ids = _vdce.iter_doc_rule_ids(Path(repo_path), include)
        # L1 structural integrity (#194): also surface code-side ORPHANS — a `# rule:` whose ID
        # is declared in NO declaration doc (code->nonexistent-rule), the direction the doc-side
        # resolution below structurally cannot see (it iterates doc-declared IDs only).
        # scan_structural_integrity runs the full L1 scan on the live corpus; its doc-side
        # dangling/duplicate findings are already reported below as broken_edge/ambiguous, so here
        # we take ONLY its code_orphan findings (a disjoint id set — no double-report). Advisory:
        # WARN-only, never a gate (hard-gate promotion is data-gated, ADR-89 OQ3).
        orphans = [f for f in _vdce.scan_structural_integrity(
                       Path(repo_path), code_root, include, multi)
                   if f.kind == "code_orphan"]
    except Exception as exc:  # never wedge the audit-health gate
        return [Finding("doc_code_edge", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    # ONE Finding per defect (atomic) — a #147 ship-gate disposition then matches the concern
    # unit, never waving a different undispositioned edge through (the per-id git_backlog_drift
    # rule). resolve_edge / scan_structural_integrity re-scan by content → move-safe (e22e883).
    warns: list[Finding] = [
        Finding("doc_code_edge", "warn",
                (f"{f.rule_id}: code_orphan (code sites={len(f.code_sites)}, "
                 f"no declaration)").replace("|", "/"))
        for f in orphans]
    if not ids:
        # No doc-declared edges — but a code orphan is still a real structural defect to surface.
        return warns or [_na("doc_code_edge", "NOT-APPLICABLE",
                         "no doc rule-IDs in the declaration-doc registry — advisory inactive "
                         "(ecosystem/doc-code-edge.yaml)")]
    resolved = 0
    for rid in sorted(ids):
        result = _vdce.resolve_edge(rid, Path(repo_path), code_root,
                                    include=include, multi_site=multi)
        if result.status == "resolved":
            resolved += 1
        else:
            warns.append(Finding(
                "doc_code_edge", "warn",
                (f"{rid}: {result.status} (doc sites={len(result.doc_sites)}, "
                 f"code sites={len(result.code_sites)})").replace("|", "/")))
    if warns:
        return warns
    return [Finding("doc_code_edge", "pass",
                    # ASCII arrow: this evidence is printed by cmd_health's click.echo, which
                    # crashes on a Windows cp1252 console for chars outside cp1252 (e.g. U+2192).
                    f"{resolved} doc->code edge(s) resolved; none broken/ambiguous/orphaned")]


# [#533] moved to audit_checks/ — re-exported above.


def _markers_for_check(fn) -> set[str]:
    """The rule-ID(s) an ALL_CHECKS member declares: real `# rule:` COMMENT tokens in its own
    source body PLUS the contiguous `#`-comment block immediately above its `def`.

    `inspect.getsourcelines` starts at the `def` line and OMITS the leading annotation, so the
    above-def convention (the marker sits on the line directly above `def`, matching the cohort-1
    annotations) needs the walk-back. Reads real COMMENT tokens only, via
    `validate_doc_code_edge.markers_in_source` -- a marker quoted in a docstring/string is never
    collected. Fail-soft -> set() when the source is unavailable.
    """
    try:
        body_lines, start = inspect.getsourcelines(fn)
    except (OSError, TypeError):
        return set()
    pre: list[str] = []
    try:
        module = sys.modules.get(fn.__module__)
        all_lines = inspect.getsource(module).splitlines(keepends=True)
        i = start - 2  # 0-based index of the line directly above the def
        while i >= 0 and all_lines[i].lstrip().startswith("#"):
            pre.insert(0, all_lines[i])
            i -= 1
    except (OSError, TypeError):
        pre = []
    return _vdce.markers_in_source("".join(pre) + "".join(body_lines))


def _coverage_drift_findings(checks, coverage_scope: set[str],
                             exempt: set[str]) -> list[tuple[str, set[str]]]:
    """The testable core of the #203 drift-guard: return `(check_name, markers)` for every check
    that is NEITHER mapped (>=1 marker, all in `coverage_scope`) NOR exempt. Empty list = full
    coverage. `check_name` = `fn.__name__` minus the `check_` prefix (the Finding identity)."""
    drift: list[tuple[str, set[str]]] = []
    for fn in checks:
        name = fn.__name__.removeprefix("check_")
        markers = _markers_for_check(fn)
        mapped = bool(markers) and markers <= coverage_scope
        if not mapped and name not in exempt:
            drift.append((name, markers))
    return drift


def check_doc_code_coverage_drift(repo_path: Path) -> list[Finding]:
    """#203 doc->code coverage drift-guard. Every ALL_CHECKS member must be EITHER annotated with
    a `coverage_scope` rule-ID marker OR listed in `exempt:` (ecosystem/doc-code-edge.yaml) --
    else FAIL, NAMING the escapee. So a NEW enforced rule landing as an ALL_CHECKS check cannot
    silently escape the curated doc->code `coverage_scope` (the stated drift cost of the FALLBACK
    curated mechanism). FAIL-class (gating, like check_safe_removal); hub-only; read-only.

    SCOPE (honest limit): this guards ONLY the auto-enumerable ALL_CHECKS surface. Enforcement
    organs OUTSIDE ALL_CHECKS -- the seal Stop-hook, the commit-msg / pre-push hooks, the
    standalone pre-commit validators -- are NOT auto-guarded; that heterogeneous remainder stays
    curated (no single auto-enumerable registry across all mechanisms; doc-code-edge.yaml header).
    """
    if not _is_hub(repo_path):
        return [_na("doc_code_coverage_drift", "NOT-APPLICABLE",
                        "hub-only -- coverage drift-guard skipped (not the hub repo)")]
    try:
        scope = set(_load_coverage_scope(repo_path))
        exempt = _load_coverage_exempt(repo_path)
        if not scope or not exempt:
            # An empty scope OR exempt would let members pass vacuously -- treat as inert config.
            return [Finding("doc_code_coverage_drift", "warn",
                            "coverage_scope or exempt empty/absent -- drift-guard inert "
                            "(ecosystem/doc-code-edge.yaml)")]
        drift = _coverage_drift_findings(ALL_CHECKS, scope, exempt)
    except Exception as exc:  # never wedge the gate on an internal error
        return [Finding("doc_code_coverage_drift", "warn",
                        f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if drift:
        return [Finding("doc_code_coverage_drift", "fail",
                        ("ALL_CHECKS member(s) neither coverage_scope-annotated nor exempt: "
                         + "; ".join(f"{n} (markers={sorted(m) or 'none'})" for n, m in drift))
                        .replace("|", "/"))]
    return [Finding("doc_code_coverage_drift", "pass",
                    f"all {len(ALL_CHECKS)} ALL_CHECKS members covered "
                    "(coverage_scope-annotated or exempt); none escape coverage_scope")]


def _fleet_parity_findings(parity_findings, register: dict,
                           fail_verdicts: set, warn_verdicts: set) -> list["Finding"]:
    """Testable core of check_fleet_parity ([#337]): map fleet_parity ParityFinding verdicts
    to gating Findings. ONE Finding PER blocking row (disposition contract, Codex CRITICAL
    2026-06-10) -- a register entry keys on check_name='fleet_parity' + a substring of THIS
    row's evidence, so it suppresses one row, never the whole organ. If no row blocks, ONE
    summary `pass` Finding carrying the full register tally, so stale/advisory counts stay
    VISIBLE without blocking."""
    out: list[Finding] = []
    for f in parity_findings:
        status = ("fail" if f.verdict in fail_verdicts
                  else "warn" if f.verdict in warn_verdicts else None)
        if status:
            ev = f"{f.repo_id} {f.surface_id} {f.verdict}: {f.evidence}"
            out.append(Finding("fleet_parity", status, ev.replace("|", "/")[:300]))
    if not out:
        tally = ", ".join(f"{k} {v}" for k, v in sorted(register.items()) if v)
        out.append(Finding("fleet_parity", "pass",
                           f"fleet at parity -- {tally or 'no findings'} (blocking verdicts: 0)"
                           .replace("|", "/")))
    return out


def check_fleet_parity(repo_path: Path) -> list[Finding]:
    """[#337] fleet-parity gate -- the #328 cross-repo parity walk as a BLOCKING ALL_CHECKS
    member (promoted once [#336] cleared the last standing WARN; the fleet is at a zero-WARN
    steady state). Runs `fleet_parity.walk()` IN-PROCESS (the CLI exit code cannot carry the
    signal -- it is always 0/2) and maps blocking verdicts to Findings. HUB-ONLY: the walk is
    fleet-wide, run from the hub. Manifest-driven (ecosystem/parity-surfaces.yaml), so `exempt:`
    in doc-code-edge.yaml -- like enforcement_coverage / deployed_methodology_version, not a
    doc->code rule. Read-only (Layer-2, ADR-28/36).

    Verdict->status map (operator ruling 2026-07-18): FAIL on refused / must-absent /
    tombstone-violated; WARN (undispositioned -> RED) on warn-undeclared / unavailable /
    tracked-ephemera; stale-declaration + advisory-rewarn stay advisory-but-VISIBLE (surfaced in
    the summary, never RED from a date/corpus advance -- which is why the wall-clock run-date is
    safe). PERF ([#337] rider, 2026-07-18): the walk is ~8s and ALL_CHECKS also runs on the
    per-commit audit-health gate; ship-gate-only scoping was a filed follow-up. **[#597]
    DISCHARGES IT**: this check is declared `_tier(TIER_SHIP, ...)` in ALL_CHECKS and no longer
    runs at the commit gate. Measured at 14,520 ms (4.80% of check time) in the reference run
    `db4aeea2`, which is what the ~8s estimate had grown into.

    AND THE REASON IS NOT ONLY COST — this is the one ship-tier member that CAN emit `fail`, so
    it is the one that needs a risk argument beyond "it cannot block the commit anyway". The
    argument is that the property is CROSS-REPO: parity drift is caused by what happens in the
    other repos of the fleet, and a hub commit cannot create it. Gating each hub commit on the
    state of five other working trees prices every commit at another repo's drift while doing
    nothing to prevent the drift. The arc boundary is where a fleet-wide claim can honestly be
    made, and ship-gate still FAILs on refused / must-absent / tombstone-violated exactly as
    before. What is genuinely given up: a parity regression introduced elsewhere is now noticed
    at ship rather than at the next hub commit — later, and stated rather than smoothed over.
    """
    if not _is_hub(repo_path):
        return [_na("fleet_parity", "NOT-APPLICABLE",
                        "hub-only -- fleet-parity walk skipped (not the hub repo)")]
    try:
        try:
            from scripts import fleet_parity as fp   # package-mode: `python -m scripts.audit`
        except ImportError:
            import fleet_parity as fp                # script-mode: `python scripts/audit.py`
        from datetime import date as _date
        r = fp.walk(_date.today().isoformat())
        register = fp.summarize(r.findings)
        fail_v = {fp.REFUSED, fp.MUST_ABSENT, fp.TOMBSTONE_VIOLATED}
        warn_v = {fp.WARN_UNDECLARED, fp.UNAVAILABLE, fp.TRACKED_EPHEMERA}
    except Exception as exc:  # never wedge the gate on an internal error (mirrors coverage-drift)
        return [Finding("fleet_parity", "warn",
                        f"fleet-parity walk degraded (read-only): {exc!r}".replace("|", "/"))]
    return _fleet_parity_findings(r.findings, register, fail_v, warn_v)


def check_deployed_methodology_version(repo_path: Path) -> list[Finding]:
    """ADR-91 deployed-version reporter: read the hub-committed deployed-versions registry
    and report THIS repo's deployed methodology-corpus version.

    The registry (ecosystem/deployed-versions.yaml) is the durable record-home ADR-91 chose
    over the derived ecosystem/index.yaml (which audit.py::regenerate_index overwrites wholesale
    each run). One hub file, read for whichever repo is being audited: the audited repo is keyed
    by its repo-ROOT directory name (the main worktree's basename, resolved via
    `git rev-parse --git-common-dir`), so an audit run from a linked worktree keys the record by
    the parent repo — not the throwaway `<repo>-<topic>` worktree basename (#265) — and each
    repo's state.yaml carries its OWN deployed-version finding that fleet_health surfaces per repo.

    Status: `n/a` while the field is null (no methodology release deployed yet -- the expected
    pre-deploy state; the deploy-runbook writer is a separate, later piece); `pass` with the
    version once set. A repo missing from the registry, or an unreadable/malformed registry,
    -> WARN (fail-OPEN on its own input error, never a synthesized FAIL). Read-only; a status
    reporter, NOT a doc->code behavioral rule (so `exempt` in ecosystem/doc-code-edge.yaml).
    """
    name = "deployed_methodology_version"
    try:
        data = yaml.safe_load(DEPLOYED_VERSIONS_REGISTRY.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [Finding(name, "warn",
                        f"deployed-versions.yaml unreadable (read-only, non-blocking): {exc!r}"
                        .replace("|", "/"))]
    repos = data.get("repos") if isinstance(data, dict) else None
    if not isinstance(repos, dict):
        return [Finding(name, "warn",
                        "deployed-versions.yaml missing/malformed 'repos:' map (ADR-91)")]
    # Key by the repo-root basename so a linked worktree audits as its parent repo (#265);
    # fall back to the working-dir basename when git is unavailable (non-git consumer).
    repo_key = _git_repo_root_name(repo_path) or Path(repo_path).name
    if repo_key not in repos:
        return [Finding(name, "warn",
                        f"{repo_key} not listed in deployed-versions.yaml (ADR-91)")]
    entry = repos[repo_key]
    version = entry.get("deployed_methodology_version") if isinstance(entry, dict) else entry
    if version is None:
        return [_na(name, "NOT-APPLICABLE",
                        f"{repo_key}: unset -- no methodology release deployed yet "
                        "(deploy-runbook will populate; ADR-91)")]
    return [Finding(name, "pass",
                    f"{repo_key}: deployed methodology corpus v{version}")]


def check_enforcement_coverage(repo_path: Path) -> list[Finding]:
    """Informant Organ leg (Stage-2 enforcement-transfer): a READ-ONLY, non-blocking reporter of
    whether the 5 hub enforcement organs fire locally in the audited consumer.

    STATIC path only here (never clones — this runs on every hub commit via audit-health):
    applicability + locate per organ. `enforcing-local` is provable ONLY by the standalone
    reporter's fire_test (scripts/enforcement_coverage.py), so this leg never claims it — its
    strongest per-organ label is `present-unverified`. Posture (operator-ratified 2026-07-03):
    emits `n/a` — never FAIL/WARN — so it cannot RED the hub's own health/ship gate for this
    known-tracked gap; the gap lives in the digest logs/ENFORCEMENT-COVERAGE.md + the standalone
    reporter. On the hub itself this is `n/a` (the hub is the SOURCE of the organs, not a consumer
    coverage row). A status reporter, NOT a doc->code behavioral rule -> `exempt` in
    ecosystem/doc-code-edge.yaml (ADR-91-sibling posture to check_deployed_methodology_version).
    Fail-soft: any error -> WARN (fail-OPEN on its own input), never wedges a gate.

    Stage-3 (on the record, NOT built here): once a consumer establishes an enforcing-local
    baseline, a regression enforcing-local -> absent should WARN. Deferred backlog item.
    """
    name = "enforcement_coverage"
    if _is_hub(repo_path):
        return [_na(name, "NOT-APPLICABLE",
                        "hub - source of the 5 enforcement organs; per-consumer coverage is "
                        "measured by scripts/enforcement_coverage.py (read-only reporter)")]
    try:
        from scripts import enforcement_coverage as _enfcov
    except ImportError:
        import enforcement_coverage as _enfcov
    try:
        cells = _enfcov.evaluate_static(Path(repo_path))
    except Exception as exc:  # never wedge the audit gate on the reporter's own error
        return [Finding(name, "warn",
                        f"reporter degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    summary = "; ".join(f"{c.organ_id}={c.verdict}" for c in cells)
    return [_na(name, "NOT-APPLICABLE",
                    (f"{Path(repo_path).name}: {summary} "
                     "(static; enforcing-local proven only by scripts/enforcement_coverage.py)")
                    .replace("|", "/"))]


# ---------------------------------------------------------------------------
# @import edge integrity (#249) — a Claude-Code `@import` whose target is missing
# silently drops session-boot content. The coherence spine tracks reconciled_with
# PROSE edges (validate_reconciliation) but NOT the `@path` file-include graph, so a
# broken/renamed @import target dangles with no gate (the @.claude/CLAUDE-FLOOR.md and
# the [#244] @-imports have been unchecked this way). This check resolves the transitive
# @import graph from the root CLAUDE.md (BFS, cycle-safe, matches Claude-Code boot
# semantics) and FAILs on any target that resolves to nothing. STRUCTURAL presence check,
# not a doc->code behavioral rule -> `exempt` in ecosystem/doc-code-edge.yaml.
# ---------------------------------------------------------------------------

# `@` preceded by start-of-line or whitespace (the (?<!\S) guard excludes emails like
# x@gmail.com and plugin@marketplace tokens); target chars = a path.
_IMPORT_RE = re.compile(r"(?<!\S)@([A-Za-z0-9_~./\\-]+)")
_IMPORT_MAX_DEPTH = 5  # Claude Code resolves @imports recursively up to 5 hops


def _blank_preserving_lines(match: "re.Match[str]") -> str:
    """Replace a multi-line match with the same number of newlines (keeps line nos)."""
    return "\n" * match.group(0).count("\n")


_FENCE_MD = MarkdownIt("commonmark")
# Split exactly where markdown_it does (`\r\n | \r | \n`), captured so each line's own
# separator survives reconstruction — same predicate as scripts/toc/generator.py's
# `_EOL_RE`. Terra HIGH (2026-08-13, docs/audits/2026-08-13-codex-w3-landing-predicate.md):
# `text.splitlines(keepends=True)` also breaks on Unicode line separators (\x0b \x0c
# \x1c-\x1e \x85 U+2028 U+2029) that CommonMark does not treat as line boundaries, so a
# fence following one of those desyncs from markdown_it's `.map` indices and leaks live
# text into `check_import_edges`'s `@import` scan — the exact defect class N5-03 exists to
# catch, reintroduced by the fix for it.
_EOL_SPLIT_RE = re.compile(r"(\r\n|\r|\n)")


def _blank_fenced_code_blocks(text: str) -> str:
    """Blank every fenced code block (``` or ~~~, any indent 0-3) line-count-preserving,
    per CommonMark rather than a column-0-anchored regex. [#513] instance N5-03: the prior
    `^```.*?^```` regex only matched an UN-indented fence, so a legal 1-3-space-indented
    fence leaked its contents into `check_import_edges`'s `@import` scan. markdown_it's own
    `.map` line-range is CommonMark-correct (indented and `~~~` fences both close exact,
    proven against markdown_it's own commonmark spec fixtures) and is the same parser this
    repo already ADOPTED for TOC/header extraction (`scripts/toc/generator.py`,
    `scripts/normalize_headers.py`) — reusing it here is the propagation this row exists for,
    not a new instance of the class it detects."""
    parts = _EOL_SPLIT_RE.split(text)
    n_lines = (len(parts) + 1) // 2  # parts alternates line, sep, line, sep, ..., line
    for token in _FENCE_MD.parse(text):
        if token.type != "fence" or not token.map:
            continue
        start, end = token.map
        for i in range(start, min(end, n_lines)):
            parts[i * 2] = ""
    return "".join(parts)


def _strip_code_regions(text: str) -> str:
    """Blank fenced code blocks, HTML comments, and inline code spans so a `@path`
    quoted as an example — or the roster's backtick-neutralized import tokens
    (gen_methodology_roster._neutralize_import) — is not read as a live @import.
    Multi-line regions are blanked line-count-preserving; inline spans are single-line."""
    text = _blank_fenced_code_blocks(text)
    text = re.sub(r"(?s)<!--.*?-->", _blank_preserving_lines, text)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def _looks_like_import_path(target: str) -> bool:
    """A Claude-Code @import target is a FILE PATH — it has a path separator or a
    (alphabetic) file extension. This excludes version tokens like `@5.4` / `@5.5`
    (a `.4` suffix is not an extension) that pepper the section-history prose."""
    if "/" in target or "\\" in target:
        return True
    return bool(re.search(r"\.[A-Za-z]{2,}$", target))


def _import_targets(text: str) -> list[tuple[int, str]]:
    """Return (1-indexed line-no, target) for each live @import in `text`."""
    out: list[tuple[int, str]] = []
    for i, line in enumerate(_strip_code_regions(text).splitlines(), start=1):
        for m in _IMPORT_RE.finditer(line):
            target = m.group(1)
            if _looks_like_import_path(target):
                out.append((i, target))
    return out


def check_import_edges(repo_path: Path) -> list[Finding]:
    """#249 — every Claude-Code `@import` target reachable from the root CLAUDE.md exists.

    BFS the transitive @import graph (cycle-safe, depth <= 5). A target that resolves
    against neither the importing file's directory nor the repo root is a broken edge
    (FAIL — a broken @import silently drops session-boot content; audit-health makes the
    rename-a-generated-fragment failure mode commit-blocking on the hub). Machine-scoped
    (`~`-home) and absolute targets are skipped (counted, never failed). Read-only.
    """
    name = "import_edges"
    repo_root = Path(repo_path)
    root = repo_root / "CLAUDE.md"
    if not root.exists():
        return [_na(name, "NOT-APPLICABLE", "no root CLAUDE.md (presence gated by check_claude_md)")]
    visited: set[Path] = set()
    queue: list[tuple[Path, int]] = [(root, 0)]
    broken: list[str] = []
    edge_count = 0
    file_count = 0
    while queue:
        current, depth = queue.pop(0)
        rc = current.resolve()
        if rc in visited or depth > _IMPORT_MAX_DEPTH:
            continue
        visited.add(rc)
        try:
            text = current.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        file_count += 1
        for lineno, target in _import_targets(text):
            if target.startswith("~") or Path(target).is_absolute():
                continue  # machine-scoped / absolute — count nothing, never fail
            edge_count += 1
            cand_dir = current.parent / target
            cand_root = repo_root / target
            resolved = cand_dir if cand_dir.exists() else (
                cand_root if cand_root.exists() else None)
            rel = (str(current.relative_to(repo_root))
                   if current.is_relative_to(repo_root) else current.name)
            if resolved is None:
                broken.append(f"{rel}:{lineno} -> @{target}".replace("|", "/"))
            elif resolved.suffix == ".md":
                queue.append((resolved, depth + 1))
    if broken:
        return [Finding(name, "fail",
                        "broken CLAUDE.md @import target(s): " + "; ".join(broken))]
    return [Finding(name, "pass",
                    f"{edge_count} @import edge(s) resolve across {file_count} file(s)")]


# [#533] moved to audit_checks/ — re-exported above.


def _index_worktree_divergence(repo_path: Path, *paths: str) -> tuple[str, list[str]]:
    """Do the index and the working tree agree on `paths`? -> ("ok"|"diverged"|"unknown", …)

    Any check that reads the WORKING TREE is only trustworthy while the index agrees with
    it: otherwise a change can be staged and the working copy restored, so the check
    validates the old bytes while the commit records the new ones. Both organs here read
    the working tree, so both consult this first.

    "unknown" (a git probe that could not complete) is NOT "ok" -- treating it as ok was
    itself the fail-open terra found on the sixth pass. Callers block on both non-ok
    states.

    The predicate is simply "does the index differ from the working tree for any monitored
    path", which is what `git diff -- <paths>` answers directly. An earlier version
    INTERSECTED the staged and unstaged path lists (terra HIGH, 7th pass) and so returned
    "ok" when DIFFERENT monitored paths diverged -- staged `BACKLOG.md` alongside a
    regenerated-but-unstaged `tasks/` passed, letting the gate bless a coherent working
    tree while the commit recorded only half of it. Untracked files under the monitored
    paths count too: a newly generated task file is invisible to `git diff`, so omitting
    it would leave the same hole for the add case.
    """
    unstaged = _git(Path(repo_path), "diff", "--name-only", "--", *paths)
    untracked = _git(Path(repo_path), "ls-files", "--others", "--exclude-standard",
                     "--", *paths)
    if unstaged is None or untracked is None \
            or unstaged.returncode != 0 or untracked.returncode != 0:
        return "unknown", []
    divergent = sorted(set(unstaged.stdout.split()) | set(untracked.stdout.split()))
    return ("diverged", divergent) if divergent else ("ok", [])


def _load_silent_rule_baseline(repo_path: Path) -> Optional[dict]:
    """Read ecosystem/silent-rule-baseline.yaml. Returns None when absent/malformed.

    Fail-soft to None rather than raising: an unreadable baseline must surface as an
    INERT gate (a visible WARN), never wedge the whole audit and never pass silently.
    """
    try:
        data = yaml.safe_load(
            (Path(repo_path) / _srd.BASELINE_RELPATH).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None
    return data if isinstance(data, dict) else None


_BASELINE_REFS = ("origin/main", "main")


def _git(repo_path: Path, *args: str) -> Optional[subprocess.CompletedProcess]:
    """Run a git command, or None if git itself could not be invoked."""
    try:
        return subprocess.run(["git", *args], cwd=str(repo_path), capture_output=True,
                              text=True, timeout=15, check=False)
    except (OSError, subprocess.SubprocessError):
        return None


def _target_baseline_state(repo_path: Path) -> tuple[str, Optional[int], Optional[str]]:
    """The baseline on the INTEGRATION TARGET as a PROVEN state, not an inference.

    Returns one of:
      ("valid", n)      a target ref carries a well-formed baseline -- compare against it
      ("absent", None)  a target ref RESOLVES and provably does NOT contain the file --
                        genuine bootstrap, nothing to compare and nothing to launder
      ("invalid", None) a target ref contains the file but it is unreadable/malformed --
                        INDETERMINATE, must block
      ("unresolved", None)  no target ref resolves at all -- UNVERIFIABLE, must block

    Why proven rather than inferred (terra HIGH, 3rd pass 2026-07-27): the previous shape
    asked two separate questions -- "did any ref resolve?" and "did reading a baseline
    succeed?" -- and treated `ref resolved + read failed` as bootstrap. That is fail-open:
    a target baseline that exists but is malformed, or a `git show` that timed out, would
    be read as "no baseline yet" and a raised branch value would pass uncompared. Absence
    is now established positively with `git cat-file -e`, so only real absence bootstraps.

    Reading the target and NOT `HEAD` is itself the earlier fix: once a raise is committed
    HEAD *is* the new value, so a HEAD comparison compares the baseline against itself.
    """
    states = [_ref_baseline_state(repo_path, ref) for ref in _BASELINE_REFS]
    resolved = [(s, v, d) for s, v, d in states if s != "unresolved"]
    if not resolved:
        return "unresolved", None, None
    if any(s == "invalid" for s, _, _ in resolved):
        # ANY resolved-but-unreadable target makes the comparison indeterminate. Falling
        # through to another ref would be the fail-open this shape exists to close.
        return "invalid", None, None
    valid = [(v, d) for s, v, d in resolved if s == "valid" and v is not None]
    if not valid:
        return "absent", None, None        # every resolving ref provably lacks the file
    # Reconcile DETECTORS BEFORE any numeric comparison (terra HIGH, 9th pass). Running
    # min() first could return the ref whose detector happens to match while a second ref
    # sat on a different, non-commensurable scale -- and then merely changing the old
    # detector's numbers would flip the verdict from migration-WARN to PASS.
    detectors = {d for _v, d in valid}
    if len(detectors) > 1:
        return "mixed", None, None
    # STRICTEST of the resolved targets (terra HIGH, 4th pass): returning the first valid
    # ref let a raise hide behind the other one -- with origin/main at 500 and an ahead
    # local main at 400, a branch value of 450 passed against 500 while raising the real
    # local target from 400. min() cannot be gamed by ref ordering or divergence.
    value, detector = min(valid, key=lambda pair: pair[0])
    return "valid", value, detector


def _ref_baseline_state(repo_path: Path, ref: str) -> tuple[str, Optional[int], Optional[str]]:
    """One ref's baseline state: unresolved / absent / valid / invalid.

    Absence is proven with `git ls-tree`, not `git cat-file -e` (terra HIGH, 4th pass).
    `cat-file -e` returns non-zero for an inaccessible or corrupt object and for a failed
    promisor fetch exactly as it does for a missing path, so "non-zero means absent" would
    read an unreadable target as first-introduction and let a raise through uncompared.
    `ls-tree` exits 0 for a resolvable ref and prints NOTHING when the path is genuinely
    absent, which separates "not there" from "could not look".
    """
    rev = _git(repo_path, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
    if rev is None or rev.returncode != 0 or not rev.stdout.strip():
        return "unresolved", None, None
    # Pin the resolved OID and use it for BOTH probes (terra HIGH, 5th pass). Re-reading
    # the mutable ref NAME lets a concurrent fetch move it between the absence check and
    # the content read, so the two could observe different commits -- and a target baseline
    # could be classified absent against one commit while existing in another.
    oid = rev.stdout.strip()
    listing = _git(repo_path, "ls-tree", "--full-tree", "-z", oid,
                   "--", _srd.BASELINE_RELPATH)
    if listing is None or listing.returncode != 0:
        return "invalid", None, None       # the lookup itself failed: indeterminate
    if not listing.stdout.strip():
        return "absent", None, None        # PROVEN absent at this commit
    show = _git(repo_path, "show", f"{oid}:{_srd.BASELINE_RELPATH}")
    if show is None or show.returncode != 0:
        return "invalid", None, None       # it exists but could not be read
    try:
        data = yaml.safe_load(show.stdout)
    except yaml.YAMLError:
        return "invalid", None, None
    if not isinstance(data, dict):
        return "invalid", None, None
    value = data.get("baseline")
    if not isinstance(value, int) or isinstance(value, bool):
        return "invalid", None, None
    detector = data.get("detector_id")
    if not isinstance(detector, str) or not detector:
        # Without the target's detector id the two numbers cannot be shown commensurable,
        # and the module's whole premise is that counts from different detectors are not
        # comparable (terra HIGH, 8th pass). Indeterminate, so block.
        return "invalid", None, None
    return "valid", value, detector


def _ratchet_findings(live: "_srd.Measurement", baseline: Optional[dict],
                      previous: Optional[int] = None,
                      ref_state: str = "absent",
                      previous_detector: Optional[str] = None) -> list[Finding]:
    """Testable core of check_silent_rule_ratchet ([#436]).

    Kept pure (no filesystem, no git) so the four contract cases -- pass-at-baseline,
    fail-above-baseline, ratchet-down accepted, baseline-raise rejected -- are pinned
    without standing up a repo. Emits exactly ONE Finding so a #147 disposition, if one
    is ever written, cannot suppress an unrelated concern bundled alongside.
    """
    name = "silent_rule_ratchet"
    if baseline is None:
        return [Finding(name, "warn",
                        f"no readable {_srd.BASELINE_RELPATH} — ratchet INERT "
                        f"(live count {live.count}); gate is not measuring anything")]
    stamped = baseline.get("detector_id")
    if stamped != live.detector_id:
        return [Finding(name, "fail",
                        (f"detector mismatch: baseline stamped {stamped!r} but live count "
                         f"produced by {live.detector_id!r} — the two are not commensurable; "
                         f"re-measure and re-stamp rather than comparing them")
                        .replace("|", "/"))]
    value = baseline.get("baseline")
    if not isinstance(value, int) or isinstance(value, bool):
        return [Finding(name, "fail",
                        f"malformed baseline value {value!r} — expected an integer")]
    if ref_state == "mixed":
        # The two integration refs carry baselines from DIFFERENT detectors. There is no
        # single scale to compare against, and picking either would be arbitrary — a
        # broken target state needing human resolution, not a routine migration.
        return [Finding(name, "fail",
                        (f"integration refs ({', '.join(_BASELINE_REFS)}) carry baselines "
                         f"from DIFFERENT detectors — no common scale to compare against; "
                         f"reconcile them before the ratchet can verify anything "
                         f"(live {live.count}, committed {value})").replace("|", "/"))]
    if ref_state == "invalid":
        # The target HAS a baseline but it could not be read. Indeterminate, so a raise
        # cannot be ruled out — block rather than bootstrap past it.
        return [Finding(name, "fail",
                        (f"raise-guard INDETERMINATE: the baseline on the integration ref "
                         f"exists but is unreadable or malformed, so a raise cannot be "
                         f"ruled out (live {live.count}, committed {value})")
                        .replace("|", "/"))]
    if ref_state == "unresolved":
        # No integration ref at all (no remote, shallow/detached clone, not a git tree).
        # WARN blocks ship-gate unless explicitly dispositioned; a pass with a note would
        # not, which was the fail-open terra found on re-review.
        return [Finding(name, "warn",
                        (f"raise-guard UNVERIFIABLE: no integration ref (origin/main, "
                         f"main) resolves, so a baseline raise cannot be ruled out "
                         f"(live {live.count}, committed {value})").replace("|", "/"))]
    if previous is None:
        # PROVEN absent on a resolving ref — the file is genuinely new, so there is no
        # prior value to launder. Surfaced in the evidence, never silent.
        guard = " [raise-guard bootstrap: baseline provably absent on the integration ref]"
    elif previous_detector is not None and previous_detector != live.detector_id:
        # A detector revision makes the two numbers non-commensurable, so the ratchet
        # CANNOT verify this transition -- comparing them numerically would let a bump
        # silently rebase the metric (terra HIGH, 8th pass). WARN blocks ship-gate unless
        # dispositioned, which is the explicit migration path: an operator reviews the
        # re-measurement once, deliberately, rather than a version bump waving it through.
        return [Finding(name, "warn",
                        (f"detector MIGRATION {previous_detector} -> {live.detector_id}: "
                         f"the target baseline {previous} and this arc's {value} were "
                         f"measured by different detectors and are not commensurable; the "
                         f"ratchet cannot verify this transition — review the "
                         f"re-measurement explicitly").replace("|", "/"))]
    else:
        rejection = _srd.validate_transition(old=previous, new=value)
        if rejection is not None:
            return [Finding(name, "fail", rejection.replace("|", "/"))]
        guard = ""
    if live.count > value:
        return [Finding(name, "fail",
                        (f"silent-rule pool GREW: live {live.count} > baseline {value} "
                         f"(+{live.count - value}) under detector {live.detector_id} across "
                         f"{live.files} file(s) — drain the additions or record an operator "
                         f"ruling; the baseline does not rise on a commit")
                        .replace("|", "/"))]
    headroom = value - live.count
    drained = (f"; {headroom} below baseline — ratchet-down available" if headroom else "")
    return [Finding(name, "pass",
                    (f"live {live.count} <= baseline {value} under detector "
                     f"{live.detector_id} ({live.files} file(s) in scope){drained}{guard}")
                    .replace("|", "/"))]


def check_silent_rule_ratchet(repo_path: Path) -> list[Finding]:
    """[#436] silent-rule ratchet — gate the GROWTH of the silently-unenforced rule pool.

    Registered in ALL_CHECKS, so it is a ship-gate leg by construction (ship-gate runs
    the full registry and reads Finding.status directly). FAIL-class: the pool growing
    blocks the arc.

    WHAT A GREEN HERE DOES AND DOES NOT MEAN -- read before trusting it. The metric is a
    normative-keyword OCCURRENCE COUNT produced by a pinned detector
    (scripts/silent_rule_detector.py), NOT the census's `N_silent`. It cannot distinguish a
    rule from a mention of one in an example, and it counts keywords rather than rules. Green
    means "the governed corpus did not accrete normative prose since the baseline" -- it
    does NOT mean the 176-rule backlog was drained, and it says nothing about whether any
    individual rule has a mechanism. The drain is separate work ([#356], [#358]-[#361],
    review 2026-08-26).

    Why a proxy at all: the census figure is not reproducible by code (its regex and file
    filter were never recorded), so no check can recompute it. The 2026-07-27 arm-time
    re-measurement stopped the build on exactly that. D4 (architect-proposed,
    operator-adopted) resolves it by pinning a detector and letting it define the metric.

    RATCHET-DOWN ONLY, enforced two ways: `validate_transition` FAILs a raise of the
    committed baseline against its previous committed value, and this check never writes.
    Hub-only (the detector's scope roots are hub surfaces); read-only.
    """
    if not _is_hub(repo_path):
        return [_na("silent_rule_ratchet", "NOT-APPLICABLE",
                        "hub-only — the detector's scope roots are hub governance surfaces")]
    try:
        live = _srd.measure(Path(repo_path))
    except (OSError, UnicodeDecodeError, _srd.DetectorError) as exc:
        # FAIL, not "unavailable" (terra HIGH, 2026-07-27): ship-gate blocks only on `fail`
        # and undispositioned `warn`, so an "unavailable" detector would ship GREEN having
        # measured nothing at all. A decode failure silently zeroed files in the arm-time
        # probe's first run -- an unmeasured corpus must block, not wave the arc through.
        return [Finding("silent_rule_ratchet", "fail",
                        f"detector could not measure the corpus: {exc!r}".replace("|", "/"))]
    # The baseline is read from the WORKING TREE while the detector measures the INDEX, so
    # staging a raised baseline and restoring the working copy would validate the old value
    # while committing the raised one -- defeating ratchet-down-only (terra HIGH, 6th pass).
    # Refuse to answer unless the two agree.
    agreement, divergent = _index_worktree_divergence(Path(repo_path),
                                                      _srd.BASELINE_RELPATH)
    if agreement != "ok":
        detail = (", ".join(divergent) if divergent
                  else "git could not compare index and working tree")
        return [Finding("silent_rule_ratchet", "fail",
                        (f"baseline read is untrustworthy: {detail} — stage or restore "
                         f"{_srd.BASELINE_RELPATH} consistently, then re-run")
                        .replace("|", "/"))]
    ref_state, previous, previous_detector = _target_baseline_state(Path(repo_path))
    return _ratchet_findings(live, _load_silent_rule_baseline(Path(repo_path)),
                             previous, ref_state, previous_detector)


def _task_tree_findings(problems: list[str], present: bool = True) -> list[Finding]:
    """Testable core of check_task_tree_coherence ([#433] C1). Pure: takes the problem list
    `gen_task_tree.find_incoherences` produced and maps it to a Finding.

    Direction flipped by [#439] (ADR-107 step 3): `tasks/` is the SOURCE OF TRUTH and
    `BACKLOG.md` is the generated side, so the remedy named in a failure is
    `--emit-source` (tree -> file), not `--write` (file -> tree, now the import path).
    """
    name = "task_tree_coherence"
    if not present:
        return [_na(name, "NOT-APPLICABLE", "no tasks/ source tree in this repo")]
    if problems:
        shown = "; ".join(problems[:6])
        more = f" (+{len(problems) - 6} more)" if len(problems) > 6 else ""
        return [Finding(name, "fail",
                        (f"BACKLOG.md is STALE vs the tasks/ source of truth — regenerate "
                         f"with `gen_task_tree.py --emit-source`: {shown}{more}").replace("|", "/"))]
    return [Finding(name, "pass",
                    "BACKLOG.md coherent with the tasks/ source of truth "
                    "(structure + frontmatter honesty + full reassembly)")]


def check_task_tree_coherence(repo_path: Path) -> list[Finding]:
    """[#433] C1 — the `tasks/` coherence gate. [#439] — flipped to the post-flip direction.

    Closes a gap ARCHITECTURE Ch5 named against its own "no organ = decoration" rule:
    `gen_task_tree.py --check` existed as a MODE that nothing invoked. No pre-commit hook
    and no audit check called it, so coherence rested entirely on one pytest case — and a
    BACKLOG edit that skipped the suite left the tree stale at commit time. That was not
    hypothetical: at `b4dd3e48` the committed tree had already drifted (two task files
    stale, [#435]/[#436] missing, manifest and reassembly both mismatched).

    ARMING THIS GATE WAS A PRECONDITION OF THE FLIP, not a follow-up to it (ADR-107 §7.2
    condition (ii)): a stale DERIVED tree is merely wrong, whereas a stale SOURCE-OF-TRUTH
    tree is a corrupted record. Since [#439] the pair is inverted — `tasks/` is the source
    and `BACKLOG.md` is generated — so this leg now asks "does the committed BACKLOG.md
    equal what the tree generates, and does every task file's frontmatter still agree with
    its own body?" Both artifacts are still required, and the index/worktree guard still
    covers both paths, because either one going stale is the same corruption.

    Registered in ALL_CHECKS, so it is a ship-gate leg by construction. FAIL-class.

    SCOPE (inherited from `find_incoherences`, restated so a green is not over-read): this
    compares the two artifacts against EACH OTHER. It does NOT detect a consistent rewrite
    of both together — the expectation is derived from the tree being checked. Source
    integrity is a separate leg (clean `git status` plus the manifest's `generated_sha256`
    pinning which output bytes the tree claims to produce). Hub-only; read-only — it never
    regenerates anything, because a gate that silently fixes what it measures cannot fail.
    """
    if not _is_hub(repo_path):
        return [_na("task_tree_coherence", "NOT-APPLICABLE",
                        "hub-only — tasks/ is a hub-owned tree")]
    root = Path(repo_path)
    source, out_dir = root / "BACKLOG.md", root / "tasks"
    # On the hub BOTH artifacts are required, so a missing one is a FAIL, not "n/a"
    # (terra HIGH, 2026-07-27): returning n/a here made the newly-armed leg non-blocking
    # precisely when one of its artifacts had been deleted -- deleting tasks/ would have
    # disarmed the gate that exists to notice tasks/ drifting. `n/a` is reserved for the
    # off-hub guard above, which is the only case where absence is legitimate. Post-flip
    # ([#439]) an absent tasks/ is strictly worse than it was: it is the SOURCE that has
    # gone missing, not a regenerable derivative.
    missing = [n for n, p in (("BACKLOG.md", source), ("tasks/", out_dir)) if not p.exists()]
    if missing:
        return [Finding("task_tree_coherence", "fail",
                        f"required hub artifact(s) absent: {', '.join(missing)} — the "
                        f"coherence gate cannot be satisfied by deleting what it checks")]
    # The coherence read is a WORKING-TREE read, so it is only trustworthy while the index
    # agrees with the working tree for these paths (terra HIGH, 5th pass): otherwise a
    # staged BACKLOG change can be hidden by restoring the working copy before committing,
    # and the gate would bless a coherent old tree while the commit records an incoherent
    # source/tree pair. Refuse to answer rather than answer about the wrong bytes.
    # A probe that could NOT complete is not agreement (terra HIGH, 6th pass): skipping the
    # guard on a git timeout or error reopened the exact hiding path it exists to close.
    agreement, divergent = _index_worktree_divergence(Path(repo_path), "BACKLOG.md", "tasks")
    if agreement != "ok":
        detail = ("index and working tree disagree on " + ", ".join(divergent)
                  if divergent else "git could not compare index and working tree")
        return [Finding("task_tree_coherence", "fail",
                        (f"{detail} — the coherence read cannot be trusted; stage or "
                         f"restore consistently, then re-run").replace("|", "/"))]
    try:
        problems = _gtt.find_incoherences(source, out_dir)
    except (OSError, ValueError, KeyError, UnicodeDecodeError) as exc:
        # FAIL, not warn (terra HIGH re-review, 2026-07-27). A blanket `except Exception ->
        # warn` let malformed artifacts slip past a gate documented as FAIL-class: the
        # commit-time audit-health gate blocks only on `fail`. These are the artifact-read
        # and parse errors the tree can legitimately raise, and an unreadable derived tree
        # is exactly the state this gate exists to refuse. Anything OUTSIDE this set is a
        # programming defect and is deliberately left to propagate rather than be
        # laundered into a passing status.
        return [Finding("task_tree_coherence", "fail",
                        f"derived-tree check could not complete: {exc!r}".replace("|", "/"))]
    return _task_tree_findings(problems)


def check_intake_tree_coherence(repo_path: Path) -> list[Finding]:
    """[#383] wave 1 — the `docs/intake/` residue-carrier gate: ADR-109 §4's generality proof.

    ADR-109 §4 (transcribing ADR-107 §6.2) withholds the fleet desired-state contract's claim
    to GENERALITY until the engine pattern is *shown* on a second governed surface —
    "per-item frontmattered `.md` files with byte-exact identity, a residue manifest, and a
    green regen-and-diff round-trip — demonstrated by a committed round-trip proof, not by
    argument". This leg is the "green regen-and-diff round-trip" half, armed so the proof is
    a standing gate rather than a one-off run: the same "no organ = decoration" rule that
    motivated `check_task_tree_coherence` for surface 1.

    Registered in ALL_CHECKS, so it is a ship-gate leg by construction. FAIL-class.

    HUB-ONLY, and the guard is the REPO IDENTITY, not the presence of `docs/intake/`
    (verification finding, [#383] wave 1). Both corp-monorepo and ai-council DO carry a
    `docs/intake/` while carrying no residue carrier — the carrier is hub machinery that has
    not been distributed — so keying "adopted" off the folder would have reported a FAIL on
    two consumer repos and manufactured a fleet gap that does not exist (the
    enforcement-organs-are-not-homogeneous class). Off-hub is `n/a`.

    On the hub BOTH artifacts are required, so a missing one is a FAIL, not `n/a` — the same
    terra ruling the `tasks/` gate carries: a coherence gate must not be satisfiable by
    deleting what it checks. `n/a` is reserved for the off-hub guard.

    The four legs are NOT re-declared here — `gen_intake_tree.evaluate` is the single
    definition, shared with the `--check` CLI, so the gate and the command can never disagree
    about what coherent means. Read-only: it never regenerates anything, because a gate that
    silently fixes what it measures cannot fail.
    """
    if not _is_hub(repo_path):
        return [_na("intake_tree_coherence", "NOT-APPLICABLE",
                        "hub-only — the docs/intake/ residue carrier is hub-owned")]
    intake_dir = Path(repo_path) / "docs" / "intake"
    # The coherence read is a WORKING-TREE read, so it is only trustworthy while the index
    # agrees with the working tree for these paths (codex-review HIGH, 2026-07-31 — the
    # `tasks/` gate carries this guard and this one did not): otherwise a staged deletion or
    # edit under docs/intake/ can be hidden by restoring the working copy before committing,
    # and the gate would bless a coherent working tree while the commit records an
    # incoherent — or absent — carrier.
    agreement, divergent = _index_worktree_divergence(Path(repo_path), "docs/intake")
    if agreement != "ok":
        detail = ("index and working tree disagree on " + ", ".join(divergent)
                  if divergent else "git could not compare index and working tree")
        return [Finding("intake_tree_coherence", "fail",
                        (f"{detail} — the coherence read cannot be trusted; stage or "
                         f"restore consistently, then re-run").replace("|", "/"))]
    try:
        verdict, reasons = _gint.evaluate(intake_dir)
    except Exception as exc:  # noqa: BLE001 — a gate that cannot complete must not pass
        return [Finding("intake_tree_coherence", "fail",
                        f"intake residue-carrier check could not complete: {exc!r}"
                        .replace("|", "/"))]
    if verdict == _gint.OK:
        return [Finding("intake_tree_coherence", "pass",
                        f"intake residue carrier coherent ({reasons[0]})".replace("|", "/"))]
    return [Finding("intake_tree_coherence", "fail",
                    (f"{'; '.join(reasons)} — run {_gint.REMEDY}").replace("|", "/"))]


# [#533] moved to audit_checks/ — re-exported above.


# --- [#460] replication of the ADR-80 durable record ------------------------
# ADR-80 promises a DURABLE record; `_commit_routine_outputs` writes it to a LOCAL branch.
# Between 2026-07-16 and 2026-08-01 the push that made it durable was absent and 51 commits
# accumulated on one disk unnoticed, because the push's only owner ([#254]) had closed on an
# existence-shaped Done-when ("origin/... exists and tracks") that a single manual push
# satisfied. The push leg (`_push_routine_branch`) fixes the mechanism; this alarm is the
# BACKSTOP, because a push can only shout at the moment it fails while divergence PERSISTS.
#
# Graduated rather than binary: the routine is daily, so one or two commits of lag is a
# transient push failure (network, credentials) and REDding the ship-gate for it would train
# the operator to disposition the organ -- the exact way the 46-day FAIL on the fleet branch
# came to be ignored. Past the threshold it is an outage, and ADR-80's promise is false.
REPLICATION_LAG_FAIL_AFTER = 3


def classify_replication_lag(ahead: int) -> tuple[str, str]:
    """PURE: (status, evidence) for `ahead` unreplicated commits. ASCII-only evidence ([#470])."""
    if ahead <= 0:
        return ("pass", f"{_AUTOMATION_BRANCH} is replicated to origin (0 commits ahead)")
    if ahead <= REPLICATION_LAG_FAIL_AFTER:
        return ("warn", f"{_AUTOMATION_BRANCH} is {ahead} commit(s) ahead of origin -- a "
                        f"recent push likely failed; ADR-80's durable record is behind")
    return ("fail", f"{_AUTOMATION_BRANCH} is {ahead} commit(s) ahead of origin, over the "
                    f"{REPLICATION_LAG_FAIL_AFTER}-commit threshold -- ADR-80 promises a "
                    f"durable record that currently exists on ONE disk ([#460])")


def check_fleet_audit_replication(repo_path: Path) -> list[Finding]:
    """[#460] — is the ADR-80 durable record actually replicated to origin?

    HUB-ONLY by repo identity, not by branch presence: `automation/fleet-audit` is hub
    machinery that was never distributed, so keying off anything else would manufacture a
    fleet gap on consumers that correctly have no such branch (the
    enforcement-organs-are-not-homogeneous class, [#383] wave 1).

    Reads the REMOTE-TRACKING ref, never the network: the check must be runnable offline and
    inside the ship-gate without turning a verification organ into a network dependency. The
    consequence is stated rather than hidden -- it measures lag against the last-known origin,
    so a very stale fetch understates it. It cannot OVERstate it, which is the safe direction
    for an alarm.

    An absent branch or absent tracking ref is `n/a`, not a failure: there is nothing to
    replicate, and a repo that has never run the routine is not in breach of ADR-80.
    """
    if not _is_hub(repo_path):
        return [_na("fleet_audit_replication", "NOT-APPLICABLE",
                        "hub-only -- automation/fleet-audit is hub-owned machinery")]

    scrub = _git_location_env()
    env = {k: v for k, v in os.environ.items() if k not in scrub}

    def _run(args: list[str]) -> Optional[str]:
        try:
            p = subprocess.run(["git", "-C", str(repo_path), *args], capture_output=True,
                               text=True, encoding="utf-8", errors="replace", env=env)
        except OSError:
            return None
        return p.stdout.strip() if p.returncode == 0 else None

    local = _run(["rev-parse", "--verify", "--quiet", f"refs/heads/{_AUTOMATION_BRANCH}"])
    if not local:
        return [_na("fleet_audit_replication", "NOT-APPLICABLE",
                        f"no local {_AUTOMATION_BRANCH} branch -- nothing to replicate")]
    remote_ref = f"refs/remotes/origin/{_AUTOMATION_BRANCH}"
    if not _run(["rev-parse", "--verify", "--quiet", remote_ref]):
        # NOT n/a (codex HIGH, 2026-08-01). A local durable branch with no remote-tracking ref
        # means this clone has no evidence the record was EVER replicated -- the strongest form
        # of the defect, not an absence of one. Returning `n/a` here would disable the backstop
        # in exactly the never-replicated case it exists for, and the first draft's own evidence
        # string said "has never been replicated" while reporting `n/a`.
        return [Finding("fleet_audit_replication", "fail",
                        f"local {_AUTOMATION_BRANCH} exists but there is no {remote_ref} -- no "
                        f"evidence it has EVER been replicated; ADR-80's durable record may "
                        f"exist on ONE disk ([#460]). If this clone simply has not fetched, "
                        f"run git fetch origin and re-check")]

    count = _run(["rev-list", "--count", f"{remote_ref}..refs/heads/{_AUTOMATION_BRANCH}"])
    if count is None or not count.isdigit():
        # FAIL, not "unavailable" (green-by-skip sweep, 2026-08-25). `unavailable` renders
        # as N/A and `_check_outcome` projects it onto `pass`, so this shipped green having
        # measured nothing -- the same trap the no-remote-ref branch above already refused
        # ("Returning `n/a` here would disable the backstop in exactly the never-replicated
        # case it exists for", codex HIGH 2026-08-01), and the one check_silent_rule_ratchet
        # names at terra HIGH 2026-07-27. Both refs are verified before this line, so git
        # works and the repo is intact: rev-list failing here is a real defect, not an
        # inapplicable context.
        return [Finding("fleet_audit_replication", "fail",
                        "git rev-list failed -- replication lag NOT measurable here, so this "
                        "run proves nothing about ADR-80's durable record")]

    status, evidence = classify_replication_lag(int(count))
    return [Finding("fleet_audit_replication", status, evidence.replace("|", "/"))]


# --- [#462] fleet-membership agreement --------------------------------------
# The [#382] census censused `ecosystem/registry.md` ITSELF, so a member absent FROM that
# registry was invisible BY CONSTRUCTION -- `terminal-setup` sat declared in ADR-104 and in
# VISION while present in zero machine surfaces, caught only because three consecutive
# nightly digests re-noticed it by hand. This organ inverts the direction: the DECLARATION is
# the fixed point and the surfaces are diffed against it, so absence is reported rather than
# waited for.
#
# The declaration is a CONSTANT, deliberately. Parsing ADR-104's prose into repo ids is a new
# loadable declaration source -- [#472]'s scope, and its option (c) collides with ADR-109 §2
# ("No new physical contract file is created in v1.") and §9's named rejection. A constant
# needs no new file, no `SourceSurface` value and no loader change.
#
# Its honest cost, named not claimed away: the constant COULD drift from ADR-104:15 silently.
# [#472] CLOSED that (ADR-104 amendment 2026-08-03): the ADR now carries the same nine ids inside
# a machine-locatable `declaration:start/end id=adr104-fleet-members` anchor, and the
# declaration-agreement leg below reads it and REDs `audit-health` on any disagreement. The
# amendment is the SOURCE; this constant is the MIRROR the leg checks -- it stays the census
# input (ADR-109 section 2/9 forbid a new persisted declaration file), so nothing here becomes a
# loader. Edit one without the other and the gate names which side is stale.
ADR104_FLEET_DECLARATION = (
    ".dev-knowledge", "ai-council", "corp-monorepo", "corp-ops",
    "corp-sca-time-automation", "demo-prep", "life-architect", "terminal-setup",
    "win-tooling",
)

# ADR-109 §2: membership resolves TOWARD deployed-versions.yaml -- the durable record.
_MEMBERSHIP_ANCHOR = "deployed-versions"

# [#472] -- the ADR-104 declaration anchor. An HTML-comment PAIR, chosen on evidence: this repo's
# scripts/ parses five HTML-comment grammars for content location and ZERO fence info-strings
# (every fence handler treats a fence as a region to SKIP). `methodology:*` was rejected as
# boundary_report's hub/repo-OWNERSHIP axis, and the UPPERCASE `X:START/END` form as the shape
# three GENERATORS use -- putting that in an immutable ADR would falsely signal a machine may
# rewrite the block. The fence inside the block is render decoration; the comments are the
# contract.
ADR104_PATH = "docs/decisions/ADR-104-fleet-repository-shape.md"
_DECL_ANCHOR_ID = "adr104-fleet-members"
# FULL-LINE markers with a HARD id boundary (terra HIGH, 2026-08-04). `\b` after the id was
# wrong twice over: `-` is a non-word character, so `id=adr104-fleet-members-v2` satisfied a
# word boundary and matched this anchor -- a differently-versioned block would have been read
# as if it were this one. The id must now be followed by whitespace or the comment close, and
# the marker must occupy its own line, so a marker mentioned mid-sentence is not a match either.
_DECL_START_RE = re.compile(
    rf"^[ \t]*<!--[ \t]*declaration:start[ \t]+id={_DECL_ANCHOR_ID}(?=[ \t]|-->)[^>]*-->[ \t]*$",
    re.MULTILINE)
_DECL_END_RE = re.compile(
    rf"^[ \t]*<!--[ \t]*declaration:end[ \t]+id={_DECL_ANCHOR_ID}(?=[ \t]|-->)[ \t]*-->[ \t]*$",
    re.MULTILINE)


class DeclarationError(RuntimeError):
    """The ADR-104 declaration anchor is absent, duplicated, or unterminated."""


def read_adr104_declaration(path) -> list[str]:
    """The repo ids inside ADR-104's `declaration:start/end` anchor, in file order.

    Returns a LIST, not a set: the count is part of the contract, so a duplicated line is a
    detectable defect rather than one silently collapsed away.

    Raises DeclarationError when the anchor is missing, appears more than once, or has no end
    marker. Never degrades to an empty result -- the check's standing rule is that a gate which
    can be satisfied by deleting what it checks is not a gate.
    """
    text = Path(path).read_text(encoding="utf-8")
    # A marker shown as an EXAMPLE inside a code fence is not the declaration (terra HIGH,
    # 2026-08-04): without this, an incidental fenced example could supply the only matched
    # pair and be read as the source while the real anchor was absent. Fence detection is the
    # corpus-proven `toc.generator` helper rather than a second hand-rolled toggle -- the
    # 2026-08-03 arc established that such toggles are wrong in at least four ways.
    # Dual-import, the pattern block_ff_push already uses for validate_no_ff. Script mode
    # (`python scripts/audit.py`) puts scripts/ on sys.path; package mode
    # (`python -m scripts.audit`) puts the repo ROOT there. The bare import happens to resolve
    # in package mode today only because another imported script inserts scripts/ as a SIDE
    # EFFECT -- incidental, not a contract, and terra flagged the fragility (2026-08-04).
    try:  # noqa: PLC0415 -- local: keeps audit's import cheap on the audit-health path
        from toc.generator import _code_line_indices
    except ImportError:
        from scripts.toc.generator import _code_line_indices
    fenced = _code_line_indices(text)

    def _outside_fence(m) -> bool:
        return text.count("\n", 0, m.start()) not in fenced

    starts = [m for m in _DECL_START_RE.finditer(text) if _outside_fence(m)]
    ends = [m for m in _DECL_END_RE.finditer(text) if _outside_fence(m)]
    if not starts:
        raise DeclarationError(
            f"ADR-104 declaration anchor '{_DECL_ANCHOR_ID}' not found in {ADR104_PATH} -- "
            f"the declaration source cannot be satisfied by deleting what it checks ([#472])")
    if len(starts) > 1:
        raise DeclarationError(
            f"ADR-104 declaration anchor '{_DECL_ANCHOR_ID}' appears {len(starts)} times in "
            f"{ADR104_PATH}; exactly one is required ([#472])")
    if not ends:
        raise DeclarationError(
            f"ADR-104 declaration anchor '{_DECL_ANCHOR_ID}' has a start marker with no matching "
            f"end marker ([#472])")
    if len(ends) > 1:
        raise DeclarationError(
            f"ADR-104 declaration anchor '{_DECL_ANCHOR_ID}' has {len(ends)} end markers in "
            f"{ADR104_PATH}; exactly one is required ([#472])")
    if ends[0].start() < starts[0].end():
        raise DeclarationError(
            f"ADR-104 declaration anchor '{_DECL_ANCHOR_ID}' has its end marker before its start "
            f"marker in {ADR104_PATH} ([#472])")
    inner = text[starts[0].end():ends[0].start()]
    # The fence is decoration (without it markdown joins the ids into one paragraph), so fence
    # lines are dropped and every other non-blank line is an id.
    return [ln.strip() for ln in inner.splitlines()
            if ln.strip() and not ln.strip().startswith("```")]

# Surface id -> repo-relative path. Ids reuse the loader's C1 facts vocabulary
# (`desired_state_loader.SRC_*`) so the two organs name the same surfaces the same way.
_MEMBERSHIP_SURFACES = (
    ("registry-md", "ecosystem/registry.md"),
    ("index-yaml", "ecosystem/index.yaml"),
    ("deployed-versions", "ecosystem/deployed-versions.yaml"),
    ("parity-surfaces", "ecosystem/parity-surfaces.yaml"),
    ("onboarding-rulings", "ecosystem/satellite-onboarding-rulings.yaml"),
)


def _read_registry_members(path: Path) -> set[str]:
    """The hand-maintained markdown table -> registered repo ids.

    Twin of `desired_state_loader.parse_registry_md` (same row regex). Duplicated ON PURPOSE
    rather than imported: that module pulls pydantic, and this check runs on the `audit-health`
    pre-commit path where [#343] already flags per-commit cost. The duplication is held honest
    by a test asserting both readers agree on the live file, not by a comment.
    """
    return set(re.findall(r"(?m)^\|\s*`([^`]+)`\s*\|[^|]*\|[^|]*\|[^|]*\|\s*$",
                          path.read_text(encoding="utf-8")))


def _read_surface_members(surface_id: str, path: Path) -> set[str]:
    """Repo ids carried by one repo-keyed surface. Raises on absent/malformed -- the caller
    turns that into a FAIL, because a gate satisfiable by deleting its input is not a gate."""
    if surface_id == "registry-md":
        return _read_registry_members(path)
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if surface_id == "index-yaml":
        return {str(r["name"]) for r in (doc.get("repos") or ()) if r.get("name")}
    key = {"deployed-versions": "repos", "parity-surfaces": "fleet",
           "onboarding-rulings": "rulings"}[surface_id]
    return {str(k) for k in (doc.get(key) or {})}


def classify_membership(declaration: tuple[str, ...],
                        surfaces: dict[str, set[str]]) -> list[tuple[str, str]]:
    """PURE: [(status, evidence)] for a fleet declaration diffed against repo-keyed surfaces.

    Two directions, deliberately asymmetric:

    * A repo a surface carries but the declaration does not -> FAIL, naming repo AND surface.
      Either ADR-104 is stale or the surface is wrong; both need a human, and which surface
      is the first question that human asks.
    * A declared repo missing from the anchor -> reported as DATA at pass. Ruled 2026-08-01,
      on ADR-109 §2 ("the disagreement itself is carried as model data, never a load error")
      and §8 ("Stale derived inputs are surfaced, not fixed"). Not warn: an undispositioned
      WARN REDs the ship-gate, which trains the operator to disposition the organ -- exactly
      how a 46-day FAIL came to be ignored ([#460]).

    ASCII-only, pipe-free evidence ([#470] + the Finding contract).
    """
    declared = set(declaration)
    findings: list[tuple[str, str]] = []
    for surface_id, members in surfaces.items():
        for repo in sorted(members - declared):
            findings.append(("fail",
                             f"{surface_id} carries repo '{repo}', absent from the ADR-104 "
                             f"fleet declaration -- an undeclared member: either the "
                             f"declaration is stale or the surface is wrong ([#462])"))

    resolved = surfaces.get(_MEMBERSHIP_ANCHOR, set())
    where = [f"{repo} [{', '.join(s for s, m in surfaces.items() if repo in m) or 'NO SURFACE'}]"
             for repo in declaration if repo not in resolved]
    coverage = ", ".join(f"{s} {len(m & declared)}/{len(declared)}"
                         for s, m in surfaces.items())
    findings.append(("pass",
                     f"{len(declared)} declared (ADR-104); {len(resolved & declared)} resolved "
                     f"members ({_MEMBERSHIP_ANCHOR}); coverage {coverage}; "
                     f"declared-but-not-deployed: {'; '.join(where) if where else 'none'}"))
    return findings


def _declaration_agreement(repo_path: Path) -> list[Finding]:
    """[#472] — ADR-104's anchored declaration vs `ADR104_FLEET_DECLARATION`.

    Three assertions and nothing more:
      1. the anchor pair exists exactly once (absent / duplicated / unterminated -> FAIL);
      2. the ids agree with the constant as a SET **and** in COUNT, so a duplicated line is
         caught rather than collapsed away;
      3. nothing else -- the block is NEVER fed to `classify_membership`. The amendment is the
         authority the constant is checked against, never the census's membership input, so
         ADR-109 section 2 (`resolve_fleet_members` not widened) stays intact.

    Drift is reported naming BOTH directions separately, because "which side is stale" is the
    first question a human asks.
    """
    try:
        declared = read_adr104_declaration(Path(repo_path) / ADR104_PATH)
    except DeclarationError as exc:
        return [Finding("membership_agreement", "fail", str(exc).replace("|", "/"))]
    except OSError as exc:
        return [Finding("membership_agreement", "fail",
                        f"ADR-104 could not be read at {ADR104_PATH}: {exc!r}".replace("|", "/"))]

    constant = list(ADR104_FLEET_DECLARATION)
    if sorted(declared) == sorted(constant):
        return [Finding("membership_agreement", "pass",
                        f"declaration source: ADR-104 anchor '{_DECL_ANCHOR_ID}', "
                        f"{len(declared)} ids, agrees with audit.ADR104_FLEET_DECLARATION")]

    only_adr = sorted(Counter(declared) - Counter(constant))
    only_const = sorted(Counter(constant) - Counter(declared))
    parts = []
    if only_adr:
        parts.append(f"in the ADR amendment only: {', '.join(only_adr)}")
    if only_const:
        parts.append(f"in the constant only: {', '.join(only_const)}")
    if not parts:  # same members, different counts -- a duplicated line
        parts.append(f"same ids but different counts (ADR {len(declared)} vs constant "
                     f"{len(constant)}); a duplicated line in the ADR amendment only")
    return [Finding("membership_agreement", "fail",
                    "ADR-104 declaration and audit.ADR104_FLEET_DECLARATION disagree: "
                    + "; ".join(parts)
                    + "; the constant and its declaring ADR have drifted -- fix whichever is "
                      "stale, in one commit with the other ([#472])")]


def check_membership_agreement(repo_path: Path, _surface_paths=None) -> list[Finding]:
    """[#462] — the ADR-104 fleet declaration diffed against every repo-keyed machine surface.

    Closes the blind spot that made [#462] invisible for months: a census keyed on one
    registry cannot see a member missing from that registry, so this one is keyed on the
    DECLARATION and reports per-repo per-surface presence.

    HUB-ONLY by repo identity, never by artifact presence: `ecosystem/`'s registries are hub
    machinery that was never distributed, so guarding on "does this repo have registries"
    would report FAIL across the fleet and manufacture a gap that does not exist (the
    enforcement-organs-are-not-homogeneous class, [#383] wave 1).

    Read-only. It never regenerates a surface -- a gate that silently fixes what it measures
    cannot fail. `resolve_fleet_members` is NOT consulted and NOT widened: that resolution is
    a named ADR-109 §2 ruling and belongs to [#472].
    """
    if not _is_hub(repo_path):
        return [_na("membership_agreement", "NOT-APPLICABLE",
                        "hub-only -- the ecosystem/ membership surfaces are hub-owned")]

    # [#472] declaration-agreement leg. Attached HERE -- after the hub guard, before the surfaces
    # loop -- on purpose: the constant is verified before it is handed to classify_membership, and
    # a declaration/constant disagreement is still reported when a later surface read fails.
    # Evaluated HERE (before the surfaces loop) per the ruled attach point, so the constant is
    # verified before classify_membership receives it and the verdict survives an early return.
    # Emitted LAST: output position is cosmetic, and prepending would silently re-index every
    # caller that reads findings[0] as the census verdict.
    decl: list[Finding] = list(_declaration_agreement(Path(repo_path)))

    surfaces: dict[str, set[str]] = {}
    for surface_id, rel in (_surface_paths or _MEMBERSHIP_SURFACES):
        path = Path(repo_path) / rel
        try:
            surfaces[surface_id] = _read_surface_members(surface_id, path)
        except FileNotFoundError:
            return [Finding("membership_agreement", "fail",
                            f"membership surface {rel} is absent -- the census cannot be "
                            f"satisfied by deleting what it checks ([#462])")] + decl
        except Exception as exc:  # noqa: BLE001 -- a gate that cannot complete must not pass
            return [Finding("membership_agreement", "fail",
                            f"membership surface {rel} could not be read: {exc!r}"
                            .replace("|", "/"))] + decl
    # Same rule as `discover_repos()` (a dir carrying state.yaml) but keyed on repo_path.
    # NOT `discover_repos()` itself: it reads the module-global ECOSYSTEM_DIR, so reusing it
    # would make this one surface read a DIFFERENT repo than the other five whenever the two
    # disagree -- caught by test_health_ok_with_registered_repo, which monkeypatches exactly
    # that global. A check that takes repo_path must honour it for every surface it reads.
    #
    # Guarded like the other five (terra HIGH, 2026-08-01): an unguarded `iterdir()` raises
    # on a permission or I/O error and takes down the whole `audit.py health` run -- strictly
    # worse than this check failing, because it denies every OTHER check its verdict too.
    eco = Path(repo_path) / "ecosystem"
    try:
        surfaces["state-dirs"] = ({d.name for d in eco.iterdir()
                                   if d.is_dir() and (d / "state.yaml").exists()}
                                  if eco.is_dir() else set())
    except OSError as exc:
        return [Finding("membership_agreement", "fail",
                        f"membership surface ecosystem/<repo>/ could not be read: {exc!r}"
                        .replace("|", "/"))] + decl

    return [Finding("membership_agreement", status, evidence.replace("|", "/"))
            for status, evidence in classify_membership(ADR104_FLEET_DECLARATION, surfaces)] + decl


# THE ADR-85 MESSAGE TEXT MOVED TO `journal_anchor` (batch U, lane-u-000-branch-enum-parity).
# It lived here, and `block_unanchored_push` -- the organ this check is the BACKSTOP FOR, in its
# own docstring's words -- printed a paraphrase of it instead. Two organs, two wordings, one
# rule: the drift edge AF-1 exists to close. It now sits in the module that already owns the
# predicate as code and that BOTH organs already import, so neither can restate it alone.
#
# Dual-import, the pattern `check_amendment_coherence`/`block_ff_push` already use: script mode
# puts scripts/ on sys.path, package mode puts the repo ROOT there.
try:  # noqa: PLC0415 -- module-level, mirrors the sibling shim below
    from journal_anchor import SPINE_DIAGNOSTIC as _SPINE_DIAGNOSTIC
    from journal_anchor import SPINE_PREDICATE as _SPINE_PREDICATE
except ImportError:  # pragma: no cover -- package mode
    from scripts.journal_anchor import SPINE_DIAGNOSTIC as _SPINE_DIAGNOSTIC
    from scripts.journal_anchor import SPINE_PREDICATE as _SPINE_PREDICATE


# rule: seal-journal-spine-anchor
def check_journal_spine_anchor(repo_path: Path) -> list[Finding]:
    """ADR-85 amendment 2026-08-03 §A8 / FR4 — the audit BACKSTOP for the pre-push hard leg.

    Walks `git log --first-parent main` and asserts every spine entry AT OR ABOVE the ADR's
    dated disposition floor is anchored by a JOURNAL entry. **A gap is a FAIL, not a WARN**,
    and that is load-bearing rather than stylistic: a WARN is dispositionable, and a
    dispositionable backstop cannot be the thing that makes `git push --no-verify` non-silent.
    The escape stays legitimate; it just stops being invisible.

    The anchoring predicate is imported from `journal_anchor` -- the SAME module the pre-push
    organ uses -- so the gate and its backstop cannot drift about what "anchored" means.
    Predicate (§A7): a spine entry is anchored when JOURNAL names >=1 SHA the entry
    INTRODUCED, never the entry's own SHA (a merge cannot name its own hash).

    The floor is READ FROM THE RATIFIED ADR, never hardcoded and never re-derived here
    (FR4). A floor living in a Python literal can be widened in a commit that reads like a
    refactor; widening it in the ADR is a visible governance act. An unreadable/unparseable
    floor is a FAIL, not a pass -- an unknown exemption boundary is not a clean one.

    THE DECLARED-INTEGRATION-ARC EXEMPTION (ADR-110 amendment 2026-08-07, R-1). A lane merge
    is skipped here while a committed batch manifest declares an open batch — because a
    batch's JOURNAL entry names the lane MERGE SHAs and so cannot exist until after them,
    making the per-commit evaluation structurally unsatisfiable mid-queue. Both conditions
    are required (a `worktree-lane-*` `--no-ff` merge AND an open manifest), the exemption
    self-expires when the manifest's declared `closed_by:` packet lands, and it is REPORTED
    IN THE PASS EVIDENCE rather than applied silently — a skipped entry a reader cannot see
    is the thing this gate exists to prevent. `scripts/batch_manifest.py` holds the rule and
    its honest limits; the range-level pre-push organ does NOT import it, which is what keeps
    "nothing ships unanchored" true. It replaces `SKIP=audit-health`, which disabled the
    whole registry twice per batch at width 3 and would five times at width 6.

    HUB-ONLY by repo identity: ADR-85's floor lives in this repo's ADR and consumers carry
    neither it nor this JOURNAL shape, so scanning them would manufacture a fleet gap (the
    enforcement-organs-are-not-homogeneous class). Read-only (Layer-2).
    """
    if not _is_hub(repo_path):
        return [_na("journal_spine_anchor", "NOT-APPLICABLE",
                        "hub-only -- ADR-85's disposition floor and JOURNAL shape are hub-owned")]
    try:
        import batch_manifest as _bm
        import journal_anchor as _ja
        floor = _ja.floor_sha(repo_path)
        journal = _ja.journal_text(repo_path)
        unanchored_all = _ja.unanchored_on_spine(repo_path, "main", floor, journal)
        live = _bm.open_batches(repo_path)
        exempted = _bm.exempt(repo_path, unanchored_all, batches=live)
        gaps = [s for s in unanchored_all if s not in exempted]
        # N2-L5 (#524 leg c): among spine entries that ARE anchored (i.e. NOT in
        # unanchored_all), which are anchored only by MENTION -- no explicit 'Anchors:'
        # record line -- versus by record? Advisory only; never changes the fail/pass verdict
        # this function returns below (STANDING_RULINGS L-10: "a WARN by design").
        mention_warnings: list[str] = []
        for s in _ja.spine_entries(repo_path, f"{floor}..main"):
            if s not in unanchored_all:
                mention_warnings.extend(_ja.mention_not_record_warnings(repo_path, s, journal))
    except Exception as exc:  # noqa: BLE001 -- FR6: an error is never a silent pass
        return [Finding("journal_spine_anchor", "fail",
                        f"backstop could not complete ({exc!r}) -- an unknown anchoring "
                        "state is not a clean one (ADR-85 §A6)".replace("|", "/"))]
    warn_finding: list[Finding] = []
    if mention_warnings:
        shown = "; ".join(mention_warnings[:5])
        more = f" (+{len(mention_warnings) - 5} more)" if len(mention_warnings) > 5 else ""
        warn_finding = [Finding("journal_spine_anchor", "warn",
                                f"{shown}{more}".replace("|", "/"))]
    if gaps:
        named = "; ".join(_ja.describe(repo_path, s) for s in gaps[:5])
        more = f" (+{len(gaps) - 5} more)" if len(gaps) > 5 else ""
        # THE MIXED CASE MUST STILL DISCLOSE THE EXEMPTION (terra HIGH, 2026-08-07). This
        # branch used to return before mentioning `exempted` at all, so a FAIL naming one
        # unanchored merge silently hid the lane merges the exemption had just skipped --
        # directly contradicting the ADR-110 amendment's own "reported, never applied
        # silently" clause, in the one case where a reader is most likely to be counting.
        # THE SUBJECT-STYLE MISS, SAID OUT LOUD ([#614], 2026-08-31). The exemption reads the
        # lane name out of git's DEFAULT `Merge branch '<name>'` subject. An integrator who
        # writes a descriptive subject instead drops that prefix, the parse returns None, and
        # the merge is treated as a non-lane merge -- failing CLOSED, which is safe and is
        # exactly why it goes unnoticed: the cost arrives later as this deadlock, with nothing
        # saying an exemption was expected and missed. It was a documented honest limit in
        # `batch_manifest`'s docstring and still cost the mechanism its first live test, so the
        # limit is now REPORTED at the moment it bites instead of only being written down.
        style = ""
        if live:
            missed = [(s_, _bm.subject_style_miss(repo_path, s_)) for s_ in gaps]
            named_misses = [f"{s_[:9]} names '{n}'" for s_, n in missed if n]
            if named_misses:
                style = ("; SUBJECT-STYLE MISS -- " + "; ".join(named_misses[:3])
                         + " -- the merge subject mentions a lane but does not carry git's "
                           "default \"Merge branch '<name>'\" prefix, so the ADR-110 exemption "
                           "could not recognise it. Re-merge with the default prefix (prose may "
                           "follow it) or anchor these in JOURNAL")
        also = ""
        if exempted:
            also = (f"; SEPARATELY {len(exempted)} lane merge(s) are exempt under the "
                    f"ADR-110 declared-integration-arc rule while batch "
                    f"{', '.join(sorted(b.batch for b in live))} is open ({live[0].path}) "
                    f"and are NOT counted above")
        return [Finding("journal_spine_anchor", "fail",
                        f"{len(gaps)} first-parent spine entry(ies) above the disposition "
                        f"floor {floor[:9]} carry no JOURNAL anchor: {named}{more}{style}{also}"
                        f"{_SPINE_PREDICATE}{_SPINE_DIAGNOSTIC}"
                        .replace("|", "/"))] + warn_finding
    if exempted:
        named = ", ".join(sorted(b.batch for b in live))
        return [Finding("journal_spine_anchor", "pass",
                        f"every first-parent spine entry above the ADR-85 disposition floor "
                        f"{floor[:9]} is JOURNAL-anchored, EXCEPT {len(exempted)} lane "
                        f"merge(s) exempt under the ADR-110 declared-integration-arc rule "
                        f"while batch {named} is open ({live[0].path}) -- the exemption "
                        f"expires when {live[0].closed_by} lands".replace("|", "/"))] + warn_finding
    return [Finding("journal_spine_anchor", "pass",
                    f"every first-parent spine entry above the ADR-85 disposition floor "
                    f"{floor[:9]} is JOURNAL-anchored")] + warn_finding


# N2-E4-02 (#524 leg a): whole-file JOURNAL day-letter check.
_JOURNAL_HEADING_RE = re.compile(r"^### (\d{4}-\d{2}-\d{2}) \(([a-z]+)\)", re.MULTILINE)
# Floor: intake #18 A5 ratification (2026-07-30, docs/audits/2026-07-30-technical-
# intake18-ratification-record.md) -- "PLAYBOOK Ch8 letter-allocation convention: assigned
# at integration, lanes never allocate" is the doctrine this check enforces, so nothing
# dated before its own ratification is in scope. Without a floor, this check REDs forever
# on two immutable pre-doctrine collisions already on main (2026-07-26 duplicate `f`/`g`;
# 2026-05-09 duplicate `night`) that this lane has no standing to rewrite (JOURNAL is
# append-only, and neither entry is this lane's own to move per the 2026-08-11 (m)
# precedent). A Python-literal floor can drift silently, same risk `journal_anchor.floor_sha`
# names for the ADR-85 SHA floor -- but no ratified machine-readable floor marker exists yet
# for this doctrine, and adding one is outside the ~20-line budget this leg was given.
_JOURNAL_DAY_LETTER_FLOOR = "2026-07-30"


def check_journal_day_letters(repo_path: Path) -> list[Finding]:
    """N2-E4-02 (#524 leg a): every `### YYYY-MM-DD (<letter>)` JOURNAL heading on or after
    `_JOURNAL_DAY_LETTER_FLOOR` must carry a unique letter suffix within its date -- day
    letters are assigned once, at integration (intake #18 A5, 2026-07-30; PLAYBOOK Ch8).
    A duplicate is a stale/collided re-letter that integration missed (exactly the
    2026-08-13 `(d)` collision this lane found and fixed by moving its own not-yet-landed
    entry). FAIL, not WARN: a collision misorders history for any reader.

    Hub-only (JOURNAL day-letter doctrine is this repo's own convention). Read-only.
    """
    if not _is_hub(repo_path):
        return [_na("journal_day_letters", "NOT-APPLICABLE",
                        "hub-only -- JOURNAL day-letter doctrine is hub-owned")]
    try:
        text = (Path(repo_path) / "JOURNAL.md").read_text(encoding="utf-8")
    except OSError as exc:
        return [Finding("journal_day_letters", "fail",
                        f"cannot read JOURNAL.md: {exc!r}".replace("|", "/"))]
    by_date: dict[str, list[str]] = {}
    for date_str, letter in _JOURNAL_HEADING_RE.findall(text):
        if date_str < _JOURNAL_DAY_LETTER_FLOOR:
            continue
        by_date.setdefault(date_str, []).append(letter)
    dupes = []
    for date_str, letters in sorted(by_date.items()):
        seen: set[str] = set()
        for letter in letters:
            if letter in seen:
                dupes.append(f"{date_str} ({letter})")
            seen.add(letter)
    if dupes:
        return [Finding("journal_day_letters", "fail",
                        f"duplicate JOURNAL day-letter(s) since {_JOURNAL_DAY_LETTER_FLOOR}: "
                        + ", ".join(dupes))]
    return [Finding("journal_day_letters", "pass",
                    f"JOURNAL day-letter suffixes are unique per day since "
                    f"{_JOURNAL_DAY_LETTER_FLOOR}")]


def check_preflight_backlog_ids(repo_path: Path) -> list[Finding]:
    """[#483] R3 — ADVISORY leg: a BACKLOG `kill-candidates:` VALUE naming a non-open row.

    WARN-TIER BY RULING, never FAIL. R3 defers hard-gating pending measured evidence — zero
    false positives over two consecutive windows, reported at each seal — because the leg's
    predecessor flagged 11/11 correct historical citations on its first production run. A gate
    wired on that behaviour REDs every handoff bundle by construction. Promotion is a separate
    decision that arrives with data; this leg exists to produce that data.

    SCOPE is the assertion-role surface R2 defines in-repo, and it is deliberately narrow. A
    `kill-candidates:` value claims the named row is OPEN — you cannot kill a dead row. Every
    other `[#id]` in a BACKLOG row (`refs`, the reason prose after the em-dash) cites related
    work INCLUDING closed rows by design, and `docs/audits/`, `docs/handoffs/`, JOURNAL and
    LESSONS are citation-role wholesale. Measured on the live corpus, widening this to intake /
    protocols / ADRs would fire ~255 day-one flags, all narration.

    The role predicates are IMPORTED from `preflight_contract`, never restated, so the tool and
    this leg cannot drift into disagreeing about what an assertion is.

    DEPENDENCY THIS LEG RESTS ON, named so removing it cannot silently blind the leg: it reads
    the GENERATED `BACKLOG.md`, which is sound ONLY because currency is asserted mechanically
    elsewhere — `gen_task_tree.py --check` (and the handoff bundle's P0a probe). If that
    currency check is ever dropped, this leg starts measuring a stale view of the backlog and
    will keep reporting clean while doing it.

    HONEST LIMIT (R3's named gap): this verifies id-LIVENESS of assertions, not correctness of
    PLACEMENT. A citation on the wrong line still passes. Hard enforcement must not claim
    otherwise.
    """
    name = "preflight_backlog_ids"
    if not _is_hub(repo_path):
        return [_na(name, _NA_NOT_APPLICABLE,
                    "hub-only — BACKLOG.md kill-candidates assertions are a hub surface")]
    try:
        try:
            from scripts import preflight_contract as _pf
        except ImportError:
            import preflight_contract as _pf

        # [#589] — the ASSERTIONS are read from the canonical full-body text, the OPEN-ID
        # SET from the committed view, and the split is deliberate rather than an oversight.
        # An assertion clause (the grammar `_pf.kill_candidate_value_spans` owns — never
        # restated here, per [#483] AC4) lives in a row BODY, which the one-line projection
        # does not carry: scanning the projection finds zero assertion spans and passes
        # vacuously, which for a leg whose entire purpose is producing zero-false-positive
        # EVIDENCE toward hard-gating ([#483] R3) would be worse than not running at all.
        # Liveness, by contrast, is exactly what the view encodes -- a row is open iff it
        # is a line in it -- and a closed row keeps its `tasks/` file as the id-allocation
        # record (ADR-107 §6.3), so the tree cannot answer that question.
        try:
            from scripts import backlog_source as _bs
        except ImportError:
            import backlog_source as _bs
        backlog = Path(repo_path) / "BACKLOG.md"
        if not backlog.exists():
            return [Finding(name, "warn", "no BACKLOG.md — nothing to scan")]
        open_ids = set(re.findall(r"(?m)^- \[#(\d+)\]",
                                  backlog.read_text(encoding="utf-8", errors="replace")))
        text = _bs.canonical_text(Path(repo_path))
        if text is None:
            return [Finding(name, "warn", "no backlog source — nothing to scan")]
        stale: list[str] = []
        for line in text.splitlines():
            if not _pf._BACKLOG_ROW.match(line):
                continue
            # EVERY delimited kill-candidates value, via the shared span helper — a row may
            # carry more than one field, and stopping at the first hid a real stale assertion
            # behind an earlier benign one (terra HIGH 2026-08-04).
            spans = _pf.kill_candidate_value_spans(line)
            if not spans:
                continue
            row = re.match(r"- \[#(\d+)\]", line).group(1)
            for start, end in spans:
                for cited in re.findall(r"#(\d+)", line[start:end]):
                    if cited not in open_ids:
                        stale.append(f"[#{row}] -> #{cited}")
        if stale:
            named = ", ".join(stale[:5])
            more = f" (+{len(stale) - 5} more)" if len(stale) > 5 else ""
            return [Finding(name, "warn",
                            f"{len(stale)} kill-candidates assertion(s) name a non-open row: "
                            f"{named}{more} — advisory per the [#483] ruling R3"
                            .replace("|", "/"))]
        return [Finding(name, "pass",
                        "every kill-candidates assertion names an open row")]
    except Exception as exc:  # noqa: BLE001 — advisory leg: never wedge a gate on its own input
        return [Finding(name, "warn", f"could not scan: {exc!r}".replace("|", "/"))]


# NO `# rule:` MARKER, deliberately, until [#499]: the rule this leg embodies is not yet
# written in a living doc, so a marker here would point at nothing and register as a
# code_orphan. The leg carries a TEMPORARY exemption in ecosystem/doc-code-edge.yaml that
# expires with [#499], where the PLAYBOOK rule lands and the marker is reinstated.
# [#480] P3 ruling (2026-08-05). Shape (b): ONE canonical machine-parseable header. Measured
# before the grammar was ruled -- across all 108 codex artifacts `Branch` appears 99x, `HEAD`
# 97x, and a tally line ZERO times -- so this codifies what already exists and adds one line.
_REVIEW_RULING_DATE = "2026-08-05"
_REVIEW_CODE_SUFFIXES = (".py", ".ps1")
# NO bare directory-prefix rule (terra HIGH, 2026-08-05, measured): OR-ing `scripts/`,
# `deploy/`, `tests/`, `plugins/` against the suffix rule made 43 tracked non-code files
# code-impact -- `plugins/tier1-lifecycle/commands/ship.md`, `INSTALL.md`,
# `deploy/release-v1.3.x-contract.md`. A docs-only merge touching one would have WARNed, and
# false WARNs corrupt the very zero-false-positive evidence bar [#499] is gated on.
#
# The reviewer's proposed fix -- require suffix AND prefix -- is WRONG HERE and was not taken:
# 3 tracked code files live outside those directories (`ecosystem/schema/desired_state.py`,
# `ecosystem/schema/__init__.py`, `.claude/skills/verify/verify.py`), so it would trade false
# positives for false NEGATIVES on real code. Suffix-anywhere + exact paths has neither.
# Consequence accepted and named: a non-.py/.ps1 behavioral file (a deploy manifest, a carried
# plugin asset) is NOT code-impact today. Widening is a ruling, never a sweep.
# EXACT-PATH members (operator amendment 2026-08-05), deliberately not a `.yaml` sweep: the
# tight rule would miss the two files where THIS window's enforcement defects actually live
# ([#498] and the [#497] fold are both stale/inert carried pre-commit declarations), while a
# sweep would drag in `ecosystem/*.yaml` data files and manufacture WARNs on data-only merges.
# Further path additions arrive BY RULING, never by widening this tuple in passing.
_REVIEW_CODE_EXACT = (".pre-commit-hooks.yaml", ".pre-commit-config.yaml")
_REVIEW_TALLY_RE = re.compile(r"(?m)^\*\*Tally:\*\*[ \t]*(\d+)/(\d+)/(\d+)/(\d+)\b")
# The canonical TITLE is what makes a doc a review artifact -- a Branch/HEAD field alone does
# NOT (terra HIGH, 2026-08-05, measured): 13 tracked non-review audit docs carry a `**Branch:**`
# field, so field-presence alone would let a memo satisfy coverage and make the pass evidence
# overstate that a review happened. Measured discrimination: 0 of those 13 carry this title,
# and the review wrapper emits it on every run.
_REVIEW_TITLE_RE = re.compile(r"(?m)^# Codex Review\b")
# UTC epoch, not a timezone-bearing calendar date (terra HIGH, 2026-08-05). `%cs` renders in
# each commit's OWN timezone, so a merge near midnight could fall either side of the ruling
# date depending on where it was authored. `%ct` is a UTC instant; the cutoff is UTC midnight
# of the ruling date. Deterministic rather than ambient -- an evidence bar cannot rest on a
# boundary that moves with the committer's clock.
_REVIEW_CUTOFF_EPOCH = int(datetime(2026, 8, 5, tzinfo=timezone.utc).timestamp())
_REVIEW_BRANCH_RE = re.compile(r"(?m)^\*\*Branch:\*\*[ \t]*`?([^`\s]+?)`?[ \t]*$")
_REVIEW_HEAD_RE = re.compile(r"(?m)^\*\*HEAD:\*\*[ \t]*`?([0-9a-f]{7,40})`?")
_REVIEW_MERGE_SUBJECT_RE = re.compile(r"^Merge branch '([^']+)'")


def _review_is_code_impact(paths: list[str]) -> bool:
    """True when >=1 changed path is a code surface under the ruled predicate."""
    return any(p in _REVIEW_CODE_EXACT or p.endswith(_REVIEW_CODE_SUFFIXES) for p in paths)


# --- the HANDBACK review token (D-1, 2026-09-06) -----------------------------------------
# PLAYBOOK Ch8 "Batch communication" carries 027's message shapes and states their honest
# limit in its own words: "The shapes are greppable but UNENFORCED -- no organ parses a
# message or refuses a malformed one, so conformance rests on the seat." D-1 then made
# review a LANE act ("an empty/failed invocation is `review=NONE` -- and the integrator
# refuses a `review=NONE` code branch. Zero reviews cannot recur silently"), which is a
# refusal with nothing to run it. This is the parser those two lines were owed.
#
# ONE parser, two readers: `/lane-integrate` reads it per queue item through the `handback`
# CLI verb, and `check_review_artifact_coverage` reads it over persisted artifacts. A
# second grammar for the same line is how a doc and a gate come to disagree about what a
# handback said.
# The line is parsed as TOKENS, never scanned as prose. terra HIGH x3 (2026-09-06), each
# with a working input: a whole-line `\b(code|docs-only)\b` scan accepted
# `HANDBACK <branch> @ <sha> note: docs-only` as a docs-only exemption with no class and no
# review; a first-match `review=` read accepted `... code review=codex HIGH:0 review=NONE`;
# and a `(?m)` + `.search` verdict accepted a whole DOCUMENT because one embedded line in it
# was valid. All three are the same defect -- a fail-closed gate that scans instead of
# parsing is a gate whose input decides its own grammar.
#
# Two regexes, two jobs, one grammar. SCAN finds candidate lines inside a document (markdown
# decoration and quoting allowed); LINE is anchored and parses ONE line. Everything --
# the CLI verb, the coverage leg -- goes through LINE, so a document cannot be verdicted as
# though it were a line.
_REVIEW_HANDBACK_SCAN_RE = re.compile(r"(?m)^[ \t>*\-]*(?P<line>HANDBACK[ \t]+\S[^\r\n]*?)[ \t]*$")
_REVIEW_HANDBACK_LINE_RE = re.compile(
    r"^HANDBACK[ \t]+(?P<branch>\S+)[ \t]+@[ \t]+(?P<sha>\S+)(?P<rest>(?:[ \t]+\S+)*)[ \t]*$")
_REVIEW_HANDBACK_SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")
# The class is POSITIONAL -- the token immediately after the sha, per 027 point 2's own
# shape. Not a search: `docs-only` appearing anywhere in trailing prose must not confer the
# exemption, and `review=code` must not read as a class.
_REVIEW_HANDBACK_CLASSES = ("code", "docs-only")
# `n/a` and `NONE` are VALUES of this token, not separate tokens -- the `/` is why the
# reviewer charset is not `\w`.
_REVIEW_TOKEN_RE = re.compile(r"^review=(?P<reviewer>[A-Za-z0-9_./-]+)$")
_REVIEW_TOKEN_COUNT_RE = re.compile(r"^(HIGH|MED|LOW):(\d+)$")
_REVIEW_HANDBACK_SHAPE = ("`HANDBACK <branch> @ <sha> [code|docs-only] "
                          "review=<reviewer> HIGH:n MED:n LOW:n`")


def _review_handback_parse(line: str) -> dict | None:
    """Strict, anchored, SINGLE-line parse of one 027 HANDBACK line, or None.

    None on a multi-line input by design: the CLI verb and the coverage leg both verdict one
    LINE, and a caller handing a whole document a document-shaped grammar is how a valid
    docs-only line elsewhere in the file comes to authorise an unreviewed code merge. A
    document is scanned by `_REVIEW_HANDBACK_SCAN_RE` into lines first, then each line comes
    back through here.
    """
    if not line or "\n" in line or "\r" in line:
        return None
    m = _REVIEW_HANDBACK_LINE_RE.match(line.strip())
    if m is None:
        return None
    return {"branch": m.group("branch"), "sha": m.group("sha"),
            "tokens": (m.group("rest") or "").split()}


def _review_handback_tally(tokens: list[str]) -> dict[str, int] | None:
    """The severity counts a handback line reports, or None when it reports no review.

    None covers every no-review shape at once -- no `review=` token, `review=NONE` (a failed
    or empty invocation, which C-7 forbids reporting as clean), `review=n/a` (no reviewer was
    OWED: a docs-only exemption, not evidence), and MORE THAN ONE `review=` token (a line
    that contradicts itself asserts nothing). A reviewer naming no count at all is also None:
    `review=codex` alone is a claim that a review happened, and an unfalsifiable claim is
    precisely what [#480] exists to refuse.
    """
    reviewers = [m.group("reviewer") for m in
                 (_REVIEW_TOKEN_RE.match(t) for t in tokens) if m]
    if len(reviewers) != 1 or reviewers[0].lower() in ("none", "n/a", "na"):
        return None
    if any(t.startswith("review=") and not _REVIEW_TOKEN_RE.match(t) for t in tokens):
        return None          # a malformed `review=` token is not a second opinion
    counts = {m.group(1): int(m.group(2)) for m in
              (_REVIEW_TOKEN_COUNT_RE.match(t) for t in tokens) if m}
    return counts or None


def review_handback_verdict(line: str) -> tuple[bool, str]:
    """Does this 027 HANDBACK line authorise a merge? Returns (mergeable, ONE-line message).

    THE GAP (D-1, 2026-09-06, and PLAYBOOK Ch8's own honest limit). Measured on this
    branch's parent: `review=NONE`, `review=codex` and "review token" appeared NOWHERE
    under scripts/ tests/ .claude/ protocols/. The refusal existed as prose in a batch
    contract and in no organ, so an integrator refused a review-free code branch only by
    remembering to -- and the failure D-1 was written to end (a wave where zero lanes ran a
    review, silently) is exactly the failure a remembered rule permits.

    FAILS CLOSED on every unknown. A line that is not a HANDBACK, a `<sha>` that is not a
    sha, and a missing `[code|docs-only]` class each REFUSE rather than defer: an unknown
    branch class must not read as the exempt one. Same posture as `block_ff_push` and
    `block_unanchored_push`, and for the same reason -- a gate that guesses is a gate that
    is silent on the input it was built for.

    THE ONE EXEMPTION, quoted from D-1 rather than inferred: "docs-only branches:
    `review=n/a` allowed". So a docs-only line merges with `review=n/a` or with no token at
    all. `review=NONE` still refuses on ANY class, because `n/a` and `NONE` say different
    things: `n/a` is "no reviewer was owed", `NONE` is "the invocation failed".

    SEPARATE FROM `check_review_artifact_coverage` BY RULING, not by taste. That leg is
    held at WARN-tier by the [#480] P3 ruling pending zero false positives over two
    windows, and `test_leg_is_structurally_incapable_of_failing` pins the absence of a hard
    verdict at the source. This is a hard verdict; it belongs beside that leg, never in it.

    HONEST LIMIT, inherited whole from the leg next door: this verifies a tally was
    REPORTED, not that a review happened, was competent, or that the counts are truthful. A
    lane that types `review=codex HIGH:0` without running anything passes. It converts an
    unfalsifiable claim into a checkable one; it does not make it a true one. What it does
    close is the silent case -- a code branch that says nothing at all.
    """
    parsed = _review_handback_parse(line)
    if parsed is None:
        return False, (f"REFUSE: not a single HANDBACK line -- expected exactly "
                       f"{_REVIEW_HANDBACK_SHAPE}, one line, nothing around it")
    branch, sha, tokens = parsed["branch"], parsed["sha"], parsed["tokens"]
    where = f"{branch} @ {sha}"
    if not _REVIEW_HANDBACK_SHA_RE.match(sha):
        return False, (f"REFUSE {where}: `{sha}` is not a sha (>=7 hex) -- a HANDBACK names "
                       f"the commit it hands back, never a moving ref")
    if not tokens or tokens[0] not in _REVIEW_HANDBACK_CLASSES:
        return False, (f"REFUSE {where}: the token after the sha must be `code` or "
                       f"`docs-only` -- an unknown branch class is not the exempt one")
    cls = tokens[0]
    reviewers = [m.group("reviewer") for m in
                 (_REVIEW_TOKEN_RE.match(t) for t in tokens[1:]) if m]
    malformed = [t for t in tokens[1:]
                 if t.startswith("review=") and not _REVIEW_TOKEN_RE.match(t)]
    if malformed:
        return False, (f"REFUSE {where}: malformed review token `{malformed[0]}` -- "
                       f"expected `review=<reviewer>`")
    if any(r.lower() == "none" for r in reviewers):
        return False, (f"REFUSE {where}: review=NONE -- an empty or failed reviewer "
                       f"invocation is reported as no review, never as clean (C-7)")
    if len(reviewers) > 1:
        return False, (f"REFUSE {where}: {len(reviewers)} `review=` tokens "
                       f"({', '.join(reviewers)}) -- a line that contradicts itself asserts "
                       f"nothing, and the integrator does not choose between them")
    reviewer = reviewers[0] if reviewers else None
    if reviewer is None or reviewer.lower() in ("n/a", "na"):
        if cls == "docs-only":
            return True, f"MERGE {where}: docs-only, review=n/a (no reviewer owed -- D-1)"
        missing = "no `review=` token" if reviewer is None else f"review={reviewer}"
        return False, (f"REFUSE {where}: code branch carries {missing} -- D-1 owes "
                       f"`review=<reviewer> HIGH:n MED:n LOW:n`, and `review=n/a` is a "
                       f"docs-only allowance")
    counts = _review_handback_tally(tokens[1:])
    if counts is None:
        return False, (f"REFUSE {where}: review={reviewer} carries no severity count -- "
                       f"expected `review={reviewer} HIGH:n MED:n LOW:n`")
    tally = " ".join(f"{k}:{counts[k]}" for k in ("HIGH", "MED", "LOW") if k in counts)
    return True, f"MERGE {where}: {cls} review={reviewer} {tally}"


def check_review_artifact_coverage(repo_path: Path) -> list[Finding]:
    """[#480] P3 -- ADVISORY leg: a code-impact merge carrying no linked review artifact.

    THE GAP: the 2026-08-02 W2 report recorded "terra review: zero findings on both arcs"
    while NO artifact existed anywhere. The claim was never refuted -- it was UNFALSIFIABLE,
    and nothing in the repo could tell a real review from a remembered one.

    WARN-TIER BY RULING, never a hard verdict. The P3 ruling is LAYERED: this advisory leg
    now, the hard pre-push leg DEFERRED behind an evidence bar of zero false positives over
    two consecutive windows, reported at each seal. This leg exists to produce that data.
    The property is asserted structurally by the test suite (no status literal for the hard
    verdict appears in this function), because an observational check only proves such a
    path was not REACHED -- which is exactly what a latent one looks like.

    FORWARD-ONLY from the ruling date. Of the 16 window artifacts only 3 carried a machine
    readable tally and 9 matched no recognised shape; those are immutable records, so a leg
    that reached backwards would demand retro-editing precisely what the ruling forbids
    touching. The date filter is the mechanism that makes "never retro-edited" true.

    LINKAGE IS THREE-LEGGED (D-1 added the third), any one satisfying: by BRANCH (the artifact
    names the branch in the merge subject), by an in-range HEAD (the artifact names a commit the
    merge introduced), or by a persisted 027 HANDBACK line, which carries branch, sha AND tally
    in one line and so admits on its own. The third leg reads `review_handback_verdict` rather
    than a grammar of its own, so a line the integrator REFUSES is never a line this leg COUNTS:
    `review=NONE`, `review=n/a` and a countless `review=codex` are no-review shapes in both.
    That is the same anti-drift discipline the spine walk below already applies.
    The HEAD leg covers a review whose branch was renamed; the BRANCH leg covers a review that
    ran BEFORE a rebase, whose recorded SHA the rebase then rewrote out of the range. An
    artifact naming neither is not evidence for this merge -- otherwise one stale file in
    docs/audits/ would silence the whole leg.

    NAMED LIMITS OF THE LINKAGE, all three surfaced by review rather than discovered later:
      * The BRANCH leg reads a `Merge branch '<x>'` subject, which is the only shape
        core-invariant #5 permits on this spine (`block_ff_push` refuses the rest). A SQUASH
        merge carries no such subject AND its pre-squash SHA is not in `introduced()`, so it
        would WARN despite a real review. That is a false positive this leg does not prevent;
        it is bounded to a merge shape the repo's own gate already refuses.
      * BRANCH linkage is name-based, so REUSING a branch name for a later, unreviewed merge
        lets the earlier artifact cover it. Accepted deliberately: the alternative (full-SHA
        only) breaks the pre-rebase case the leg exists to tolerate.
      * HEAD linkage prefix-matches an abbreviation (>=7 hex). A collision would have to land
        inside the merge's OWN introduced set to mislink, which bounds it sharply, but it is
        not impossible.
    Each of these makes the leg MISS or over-credit; none makes it fail closed on real work.
    They are the reason the hard flip ([#499]) is gated on measured false positives rather
    than on this docstring's confidence.

    Reuses `journal_anchor`'s spine walk and `introduced()` rather than restating them, so
    this leg and the ADR-85 organs cannot drift about what a spine entry is or what a merge
    brought in -- the same anti-drift discipline block_ff_push and the backstop already share.

    HUB-ONLY by repo identity: the codex-review convention is a hub practice (108 artifacts
    here, none in a consumer), so scanning consumers would manufacture a fleet gap -- the
    enforcement-organs-are-not-homogeneous class. Read-only (Layer-2).

    HONEST LIMIT: this verifies an artifact EXISTS, is LINKED, and carries a PARSEABLE tally.
    It cannot verify the review happened, was competent, or that the tally is truthful -- a
    fabricated header passes. It converts an unfalsifiable claim into a checkable one; it does
    not make it a true one. The predicate also does not see a code change arriving through a
    path outside the tuples above; widening is a ruling, not a sweep.
    """
    name = "review_artifact_coverage"
    if not _is_hub(repo_path):
        return [_na(name, _NA_NOT_APPLICABLE,
                    "hub-only -- the codex-review artifact convention is a hub practice")]
    try:
        try:
            from scripts import journal_anchor as _ja
        except ImportError:
            import journal_anchor as _ja

        root = Path(repo_path)
        artifacts = []
        audits = root / "docs" / "audits"
        if audits.is_dir():
            for p in sorted(audits.glob("*.md")):
                txt = p.read_text(encoding="utf-8", errors="replace")
                # THIRD SOURCE (D-1): a persisted SESSION/handback artifact. 027 point 6 --
                # "STATE IS FILES ... every claim a message makes is expected to be
                # re-derivable from git and from to-browser/" -- so the line a lane hands
                # the integrator is the same line that survives it. One HANDBACK carries
                # branch, sha AND tally, which is why it admits on its own rather than
                # linking here and landing in `untallied` below. Read through the shared
                # parser, so a line the integrator refuses is a line this leg does not
                # count: `review=NONE`, `review=n/a` and a countless `review=codex` are all
                # no-review shapes here exactly as they are there.
                for hb in _REVIEW_HANDBACK_SCAN_RE.finditer(txt):
                    accepted, _ = review_handback_verdict(hb.group("line"))
                    parsed = _review_handback_parse(hb.group("line"))
                    if not accepted or parsed is None:
                        continue
                    if _review_handback_tally(parsed["tokens"][1:]) is None:
                        continue
                    artifacts.append({
                        "branch": parsed["branch"],
                        "head": parsed["sha"],
                        "tally": True,
                        "file": p.name,
                    })
                branch_m = _REVIEW_BRANCH_RE.search(txt)
                head_m = _REVIEW_HEAD_RE.search(txt)
                if not _REVIEW_TITLE_RE.search(txt) or not (branch_m or head_m):
                    continue          # not a review artifact -- an index, a memo, a report
                artifacts.append({
                    "branch": branch_m.group(1) if branch_m else None,
                    "head": head_m.group(1) if head_m else None,
                    "tally": bool(_REVIEW_TALLY_RE.search(txt)),
                    "file": p.name,
                })

        unlinked: list[str] = []
        untallied: list[str] = []
        scanned = 0
        # BATCHED date lookup -- one git call for the whole spine, not one PER ENTRY. The
        # per-entry form cost 236s on this repo's 1317-entry spine, and this leg runs inside
        # `audit-health`, a PRE-COMMIT gate: it would have added ~4 minutes to every commit in
        # the repo. Measured, not estimated. `spine_entries` still supplies the authoritative
        # entry list (shared --first-parent definition); this map only annotates it with dates.
        spine_dates: dict[str, int] = {}
        for ln in _ja._git(root, "log", "--first-parent", "--format=%H %ct", "main").splitlines():
            sha_part, _, date_part = ln.strip().partition(" ")
            if sha_part and date_part.strip().isdigit():
                spine_dates[sha_part] = int(date_part.strip())
        # BATCHED subject lookup (P2, intake #71) -- a SEPARATE one-shot walk, not folded into
        # the date format above: `test_spine_date_lookup_stays_batched` pins that literal format
        # string structurally as a regression guard, so widening it would fail a test that is
        # correctly guarding against exactly this class of change reappearing as a per-entry
        # spawn. A second O(1) process is free next to the O(spine) `git log -1 --format=%s`
        # per entry it replaces below.
        spine_subjects: dict[str, str] = {}
        for ln in _ja._git(root, "log", "--first-parent", "--format=%H %s", "main").splitlines():
            sha_part, _, subject_part = ln.partition(" ")
            if sha_part:
                spine_subjects[sha_part] = subject_part
        for sha in _ja.spine_entries(root, "main"):
            # Absent from the map is NOT treated as in-scope: a date we could not read is an
            # unknown, and an unknown must not silently become a WARN against a merge that may
            # predate the ruling. The pairing is one walk, so a miss means git disagreed with
            # itself -- surfaced by the outer handler if it matters, never guessed at here.
            if spine_dates.get(sha, 0) < _REVIEW_CUTOFF_EPOCH:
                continue
            # PARENT LOOKUP FROM THE BATCHED MAP (P2, intake #71), not a fresh `rev-list
            # --parents -n 1 sha` per entry: `journal_anchor`'s [#588] parent map already holds
            # every commit's parents from ONE `rev-list --parents --timestamp --all` read (built
            # here, or already warm from `check_journal_spine_anchor` earlier in CHECK_ORDER), and
            # a commit's parents are fixed by its own hash -- the map's answer and a fresh git
            # read of the same sha cannot disagree. Falls back to the original per-sha git call
            # only if the map genuinely cannot answer (unreachable from any ref even after a
            # rebuild), which never happens for a sha `spine_entries` itself just produced from
            # `main`.
            smap = _ja._spine_map_for(root, sha)
            if smap is not None and sha in smap.parents:
                parent_tuple = smap.parents[sha]
                if len(parent_tuple) < 1:
                    continue          # root commit: no first parent to diff against
                first_parent = parent_tuple[0]
            else:
                parents = _ja._git(root, "rev-list", "--parents", "-n", "1", sha).split()
                if len(parents) < 2:
                    continue          # root commit: no first parent to diff against
                first_parent = parents[1]
            changed = [ln.strip() for ln
                       in _ja._git(root, "diff", "--name-only", first_parent, sha).splitlines()
                       if ln.strip()]
            if not _review_is_code_impact(changed):
                continue
            scanned += 1
            subject = spine_subjects.get(sha, "").strip()
            subject_m = _REVIEW_MERGE_SUBJECT_RE.match(subject)
            branch = subject_m.group(1) if subject_m else None
            brought = set(_ja.introduced(root, sha))
            linked = None
            for art in artifacts:
                if branch and art["branch"] == branch:
                    linked = art
                    break
                if art["head"] and any(c.startswith(art["head"]) for c in brought):
                    linked = art
                    break
            if linked is None:
                unlinked.append(f"{sha[:8]} {branch or subject[:40]}")
            elif not linked["tally"]:
                untallied.append(f"{sha[:8]} -> {linked['file']}")

        deferred = ("advisory per the [#480] P3 ruling; the hard pre-push leg is deferred "
                    "pending 0 false positives over two consecutive windows")
        out: list[Finding] = []
        if unlinked:
            named = ", ".join(unlinked[:5])
            more = f" (+{len(unlinked) - 5} more)" if len(unlinked) > 5 else ""
            out.append(Finding(name, "warn",
                               f"{len(unlinked)} code-impact merge(s) since "
                               f"{_REVIEW_RULING_DATE} carry no linked review artifact: "
                               f"{named}{more} -- {deferred}".replace("|", "/")))
        if untallied:
            named = ", ".join(untallied[:5])
            more = f" (+{len(untallied) - 5} more)" if len(untallied) > 5 else ""
            out.append(Finding(name, "warn",
                               f"{len(untallied)} linked artifact(s) carry no parseable "
                               f"**Tally:** line: {named}{more} -- persistence is not "
                               f"machine-auditability; {deferred}".replace("|", "/")))
        if not out:
            out.append(Finding(name, "pass",
                               f"{scanned} code-impact merge(s) since {_REVIEW_RULING_DATE} "
                               f"each carry a linked review artifact with a parseable tally"))
        return out
    except Exception as exc:  # noqa: BLE001 -- advisory leg: never wedge a gate on its own input
        return [Finding(name, "warn", f"could not scan: {exc!r}".replace("|", "/"))]


def check_landing_predicate(repo_path: Path) -> list[Finding]:
    """[#513] propagation completeness — a ruling that changed a mechanism class can land at
    some call sites and not others; nothing previously owned noticing the CLASS (fixing a found
    site repairs the instance, not the pattern). Reads every `landed:` predicate declared in
    `protocols/STANDING_RULINGS.md` (register entries opt in with a fenced ```landed``` block —
    see `scripts/validate_landing_predicate.py`'s module docstring for the shape) and FAILs when
    a declared ruling's sites disagree — landed at >=1 site, not landed at >=1 other.

    Hub-only: the register is .dev-knowledge-specific, so on any other repo this is a no-op pass
    (mirrors check_doc_rot / check_git_backlog_drift). GATING, not awareness (row clause (a)/(b)):
    unlike doc_rot/doc_structure this emits FAIL, not WARN, and one Finding PER ruling so a future
    dispositioned instance clears independently (the #147 ship-gate contract). A mixed ruling is
    still checked against `ecosystem/disposition-register.yaml` here, inside the check itself,
    rather than deferred to ship-gate's WARN-only disposition layer — audit-health (the pre-commit
    gate this arms) is FAIL-only and never runs ship-gate's dispositioning pass, so a check that
    wants a dated exemption to actually suppress a pre-commit block has to consult the register
    itself (row clause (d)). A dispositioned mixed ruling downgrades to `warn` (visible, not
    blocking); an undispositioned one stays `fail`. A `landed:` site naming a file that does not
    exist is reported as its own `warn` (a broken declaration, not a propagation gap) rather than
    silently folded into either boolean. Logic lives in scripts/validate_landing_predicate.py.
    """
    name = "landing_predicate"
    if not _is_hub(repo_path):
        return [_na(name, "NOT-APPLICABLE",
                    "hub-only — landing-predicate scanner skipped (not the hub repo)")]
    try:
        entries = _vlp.scan(Path(repo_path))
    except Exception as exc:  # noqa: BLE001 -- never wedge audit-health on its own input
        return [Finding(name, "warn", f"check degraded (read-only, non-blocking): {exc!r}".replace("|", "/"))]
    if not entries:
        return [Finding(name, "pass", "no landed: predicates declared in STANDING_RULINGS.md")]

    dispositions = _load_dispositions()
    out: list[Finding] = []
    for entry in entries:
        site_desc = "; ".join(
            f"{s.path}={'ERROR' if s.landed is None else s.landed}" for s in entry.sites
        )
        if entry.mixed:
            evidence = (f"[#513] {entry.ruling_id} ({entry.title}) landed at some sites and "
                        f"not others: {site_desc}".replace("|", "/"))
            f = Finding(name, "fail", evidence)
            disp = _match_disposition(f, dispositions)
            if disp is not None:
                out.append(Finding(name, "warn",
                                    f"{evidence} -- dispositioned: {disp.get('reason', '')}".replace("|", "/")))
            else:
                out.append(f)
        elif entry.errors:
            broken = ", ".join(s.path for s in entry.errors)
            out.append(Finding(name, "warn",
                                f"{entry.ruling_id} ({entry.title}) declares a landed: site that "
                                f"could not be read: {broken}".replace("|", "/")))
        else:
            out.append(Finding(name, "pass",
                                f"{entry.ruling_id} ({entry.title}) landed uniformly: {site_desc}".replace("|", "/")))
    return out


def check_funnel_coverage(repo_path: Path) -> list[Finding]:
    """M3 -- ADVISORY leg: an audit artifact in docs/audits/ carrying no disposition record.

    THE GAP, in ADR-111's own words: "No organ checks that an audit's findings are triaged, and
    none is built here." The architect standing ruling of 2026-08-17 then closed the
    artifact-level set -- ACTIONED / FILED / REJECTED / SUPERSEDED, "an undisposed audit is a
    defect, not a document" -- and a ledger applied it to 80 artifacts. Nothing read it.

    WARN-TIER BY RULING, never a hard verdict: arming RED against an unmeasured corpus turns the
    gate off on day one. The property is asserted structurally by the test suite (no hard-verdict
    literal appears in funnel_coverage.ratchet_findings), because an observational check only
    proves such a path was not REACHED -- which is exactly what a latent one looks like.

    ZERO-BASELINE RATCHET, keyed on IDENTITY rather than a count. The committed baseline
    (ecosystem/audit-funnel-baseline.json) names the artifacts uncovered at arm time; the leg
    reports `live - baseline` BY NAME. A count-based ratchet is satisfied by draining one old
    artifact while adding one new undispositioned one -- net zero, debt unchanged, gate silent.

    ONE FINDING PER CONCERN. The #147 register suppresses an ENTIRE Finding on a substring match,
    so a bundled Finding would let one dispositioned artifact wave through every other regression
    beside it.

    HUB-ONLY by repo identity: the disposition-ledger convention is a hub practice. Read-only
    (Layer-2); no git, no writes.

    HONEST LIMIT: this verifies a disposition was RECORDED, not that it is TRUE. A row reading
    `ACTIONED | deadbeef` passes without `deadbeef` being a real commit. It converts an
    unfalsifiable claim into a checkable one; it does not make it a true one.
    """
    name = _fc.CHECK_NAME
    if not _is_hub(repo_path):
        return [_na(name, _NA_NOT_APPLICABLE,
                    "hub-only -- the audit-disposition ledger is a hub practice")]
    try:
        root = Path(repo_path)
        m = _fc.measure(root)
        baseline = _fc.load_baseline(root)
    except Exception as exc:  # noqa: BLE001 -- advisory leg: never wedge a gate on its own input
        return [Finding(name, "warn", f"could not scan: {exc!r}".replace("|", "/"))]
    return [Finding(name, status, evidence.replace("|", "/"))
            for status, evidence in _fc.ratchet_findings(m, baseline)]


def check_funnel_lifecycle(repo_path: Path) -> list[Finding]:
    """FM-2 -- the funnel's EXIT step, gated: did a terminal object actually leave its home?

    THE GAP IS THE REPO'S OWN, and `docs/intake/README.md` section 5 states it verbatim:
    "Terminal docs (CONSUMED | SUPERSEDED | REJECTED) relocate byte-identical to
    `docs/intake/archive/` ... The move is MANUAL for now -- **the status-coupled validator
    that would gate/automate it is wave work, not built.**" This is that validator, widened
    to the two sibling genres that carry the same shape (ADR status -> archive) and to the
    backward direction (a row's provenance still resolving).

    THIN ADAPTER; the logic and every honest limit live in `scripts/funnel_lifecycle.py`.
    Same shape as `check_funnel_coverage` / `check_consumer_at_landing`.

    SHIP-TIER BY DECLARATION, and this is an EXCEPTION to the assignment rule stated at the
    head of `ALL_CHECKS` -- it is FAIL-capable and would ordinarily be `TIER_COMMIT`. The
    precedent is `check_routing_agreement` directly below it, and the reasoning is the same
    shape: a COMMIT-tier FAIL here wedges every commit in every lane on a defect the
    committing session cannot legally repair. Leg a1 FAILs on live main TODAY -- intake #19
    and #26 were ruled CONSUMED by the 2026-08-29 wave-2 GO and still sit at
    `docs/intake/` depth 1 -- and clearing it means RELOCATING a governed document, which is
    an operator/integrator act, not something a check's author may do from inside a lane.
    The verdict stays fail-capable; only the stage moves.

    PROMOTION IS ONE LINE AND ITS CONDITION IS MEASURABLE: when leg a1 measures 0 on `main`
    (i.e. after the relocation lands), `_tier(TIER_SHIP, ...)` becomes `_tier(TIER_COMMIT,
    ...)`. Recorded here rather than remembered, because a temporary tier nobody wrote down
    is a permanent one.

    Z-G4, NOT A SKIP. `LifecycleUnreadable` is rendered `fail`, never `unavailable`:
    `_STATUS_LABEL` renders `unavailable` as "N/A" and `_check_outcome` projects it onto
    `pass`, so an unavailable verdict SHIPS GREEN having measured nothing -- the green-by-skip
    class the 2026-08-25 sweep closed. An unreadable intake, a `{}` frontmatter parse, an
    unusable ADR corpus or a git that cannot date rows are all failed computations of an
    AVAILABLE ground truth, and they block.

    ONE FINDING PER VIOLATION, never a bundle: the `#147` register suppresses an ENTIRE
    Finding on a substring match, so a bundled Finding would let one relocated intake wave
    through every other violation beside it.

    HUB-ONLY BY REPO IDENTITY, not by the presence of `docs/intake/` -- the `[#383]` lesson,
    copied rather than relearned: corp-monorepo and ai-council both CARRY a `docs/intake/`
    while carrying none of the lifecycle doctrine, so keying "adopted" off the folder would
    manufacture a fleet gap that does not exist. Off-hub is `n/a`.

    Read-only (Layer 2): it moves nothing. A gate that silently fixes what it measures cannot
    fail.
    """
    name = _fl.CHECK_NAME
    if not _is_hub(repo_path):
        return [_na(name, _NA_NOT_APPLICABLE,
                    "hub-only -- the intake/ADR lifecycle doctrine is hub-owned")]
    try:
        m = _fl.measure(Path(repo_path))
    except _fl.LifecycleUnreadable as exc:
        return [Finding(name, "fail",
                        f"ground truth uncomputable (Z-G4): {exc}".replace("|", "/"))]
    except Exception as exc:  # noqa: BLE001 -- an internal error BLOCKS; it never passes
        return [Finding(name, "fail",
                        f"lifecycle scan raised, so no verdict from this run is trustworthy: "
                        f"{exc!r}".replace("|", "/"))]
    return [Finding(name, status, evidence.replace("|", "/"))
            for status, evidence in _fl.findings(m)]


# THE REGISTRY DECLARES THE TIER ([#597]). Every entry is `_tier(<tier>, <check>)` — the tier is
# a required positional argument, so an entry cannot be added without stating one, and
# `tests/test_audit.py::test_every_all_checks_member_declares_a_gate_tier` refuses a bare
# callable outright. Order is still the contract (`audit_checks/registry.py::CHECK_ORDER`); the
# wrapper returns the function unchanged, so the list is a list of the same callables it was.
#
# THE ASSIGNMENT RULE, stated once here rather than re-argued per row. A check is `TIER_SHIP`
# only when BOTH hold: (a) it cannot emit `fail`, so it has ZERO gating power at the commit gate
# — `cmd_health` exits 1 on `fail` alone, so a WARN-only check's commit-time verdict is one line
# among a hundred and blocks nothing; and (b) it costs ≥1 s of measured wall time. Everything
# else stays `TIER_COMMIT`, INCLUDING the sub-second WARN-only checks (`doc_rot` 128 ms,
# `no_ff_merges` 410 ms, `preflight_backlog_ids` 102 ms, `enforcement_coverage` 39 ms,
# `deployed_methodology_version` 322 ms): moving them would buy nothing measurable and cost
# their awareness line, and a tier decision with no payoff is not a decision.
#
# TWO ENTRIES ARE EXCEPTIONS TO THAT RULE AND SAY SO. `fleet_parity` is FAIL-capable and ship
# anyway (cross-repo property; the argument is at its docstring, and it discharges the
# follow-up filed there). `doc_claims` and `generated_artifact_freshness` are the two checks
# `_GATE_MODE` hand-rolled a ship-only posture for; the declaration absorbs them, which is what
# generalizing that global MEANS — `doc_claims` at 82 ms would not clear rule (b) on cost.
#
# The `ms` figures are a DATED MEASUREMENT, not a live claim: telemetry run `db4aeea2` (the
# quietest of W2A's post-[#588] runs, `docs/audits/2026-08-26-technical-w2a-perf-core.md` §5),
# 46 checks, 302,693 ms summed across an 8-wide pool. The full 46-row ranking and this lane's
# own confirming run are in `docs/audits/2026-08-27-technical-lane-nb-tiering.md`.
ALL_CHECKS = [
    _tier(TIER_COMMIT, check_vision_md),
    _tier(TIER_COMMIT, check_adr38_baseline),
    _tier(TIER_COMMIT, check_claude_md),
    _tier(TIER_COMMIT, check_dot_prefix_discipline),
    _tier(TIER_COMMIT, check_canonical_md_visibility),
    _tier(TIER_COMMIT, check_workspace_settings),
    # check_mermaid_theme_directive retired 2026-07-05 (ADR-51 amendment — LLM-first)
    _tier(TIER_COMMIT, check_handoff_bundle_structure),
    _tier(TIER_COMMIT, check_canonical_freshness),
    _tier(TIER_SHIP, check_generated_artifact_freshness),   # ADR-86 amd. 2026-08-23 / `[#171]`
                                          # leg 1 — WARN-tier by ruling; RED is a later act with
                                          # its own ruling. SHIP: it hand-rolled this skip with
                                          # `_GATE_MODE`, which is why it measures 0 ms today
    _tier(TIER_COMMIT, check_no_sibling_orphans),
    _tier(TIER_SHIP, check_stale_worktrees),   # [#505] batch hygiene — WARN-tier by ruling
                             # (ADR-110 §1 item 4). SHIP: 2,420 ms, and a live sibling worktree
                             # is a fact about the operator's disk, not about this commit
    _tier(TIER_COMMIT, check_canonical_structure),
    _tier(TIER_COMMIT, check_handoff_version_stamp),
    _tier(TIER_COMMIT, check_amendment_coherence),
    _tier(TIER_COMMIT, check_floor_integrity),
    _tier(TIER_COMMIT, check_hooks_armed),
    _tier(TIER_SHIP, check_git_backlog_drift),   # SHIP: 3,911 ms, WARN-only awareness organ
                             # (#90a — it "exits 0 even on drift", cmd_ship_gate's own words)
    _tier(TIER_SHIP, check_doc_claims),   # SHIP: `_GATE_MODE` consumer #2 — see its docstring
    _tier(TIER_COMMIT, check_no_ff_merges),
    _tier(TIER_COMMIT, check_handoff_probes),
    _tier(TIER_COMMIT, check_supplement_folded),   # R4 (census 2026-08-26 b6) — FAIL-class;
                               # a filled SUPPLEMENT that never reached the paste is a silent
                               # loss of the outgoing seat's judgment. COMMIT by rule (a):
                               # FAIL-capable, so cost never earns it a ship tier
    _tier(TIER_COMMIT, check_dispatch_verb_agreement),   # R5 — the drift organ
                               # STANDING_RULINGS §V records as "owed and unbuilt"; FAIL-class,
                               # tree-side half only. COMMIT by rule (a)
    _tier(TIER_COMMIT, check_reconciled_versions),
    _tier(TIER_COMMIT, check_doc_rot),
    _tier(TIER_SHIP, check_doc_structure),   # SHIP: 4,531 ms; "never FAIL -> never blocks the
                             # audit-health commit gate" is this check's own docstring
    _tier(TIER_SHIP, check_doc_code_edge),   # SHIP: 36,617 ms (12.10%); "NEVER FAILs this arc —
                             # advisory-first; promotion to a gate is data-gated (ADR-89 OQ3)"
    _tier(TIER_COMMIT, check_safe_removal),
    _tier(TIER_COMMIT, check_residual_completeness),
    _tier(TIER_COMMIT, check_deployed_methodology_version),
    _tier(TIER_COMMIT, check_enforcement_coverage),
    _tier(TIER_SHIP, check_undeclared_edges),   # SHIP: 22,530 ms (7.44%); #179 was "wired as a
                             # ship-gate WARN leg" by the 2026-07-03 ruling — the tier now says
                             # what the docstring already claimed
    _tier(TIER_COMMIT, check_doc_code_coverage_drift),
    _tier(TIER_COMMIT, check_import_edges),
    _tier(TIER_SHIP, check_fleet_parity),   # [#337] blocking #328 fleet-parity gate (was
                             # informational). SHIP: 14,520 ms; the FAIL-capable exception, and
                             # the discharge of the follow-up filed in its docstring
    _tier(TIER_COMMIT, check_routine_consumers),   # [#419]/ADR-105 activation gate; scope =
                                                   # marked rows only
    _tier(TIER_COMMIT, check_silent_rule_ratchet),   # [#436] D4 ratchet — gates GROWTH of the
                                                     # silent-rule pool
    _tier(TIER_COMMIT, check_task_tree_coherence),   # [#433] C1 — arms gen_task_tree --check
    _tier(TIER_COMMIT, check_intake_tree_coherence),   # [#383] wave 1 — arms gen_intake_tree
                                                       # --check (ADR-109 §4)
    _tier(TIER_COMMIT, check_boot_byte_budget),   # [#446] A10 item 2 / R4 — the gate half of
                                                  # the split enforcement
    _tier(TIER_COMMIT, check_fleet_audit_replication),   # [#460] — ADR-80's durable record must
                                                         # exist off this disk
    _tier(TIER_COMMIT, check_membership_agreement),   # [#462] — ADR-104's declaration vs every
                                                      # repo-keyed surface
    _tier(TIER_COMMIT, check_journal_spine_anchor),   # ADR-85 amendment 2026-08-03 §A8/FR4 —
                                  # backstop for the pre-push hard leg; makes `--no-verify`
                                  # non-silent. FAIL-capable and stays at commit BY DESIGN
    _tier(TIER_COMMIT, check_journal_day_letters),   # [#524] leg a — day-letter uniqueness
    _tier(TIER_COMMIT, check_preflight_backlog_ids),   # [#483] R3 — ADVISORY (WARN-tier by
                                   # ruling); hard-gating is deferred pending 0 false positives
                                   # over two windows. 102 ms: fails rule (b), stays at commit
    _tier(TIER_SHIP, check_review_artifact_coverage),   # [#480] P3 — ADVISORY (WARN-tier by
                                     # ruling); the hard pre-push leg is deferred behind a
                                     # two-window zero-false-positive evidence bar.
                                     # SHIP: 128,428 ms — 42.43% of all check time, alone
    _tier(TIER_COMMIT, check_landing_predicate),   # [#513] propagation-completeness — GATING
                               # (FAIL-capable), one Finding per declared ruling
    _tier(TIER_COMMIT, check_adr_status_grammar),  # [#242] — ADR Status grammar/enum +
                               # header<->README coherence. enum/single-field FAIL-armed (both
                               # measure 0); grammar(47)/coherence(3)/wrapped(1)/duplicate-id(2)
                               # WARN against the baseline in
                               # docs/audits/2026-08-23-technical-lane-status-grammar.md
    _tier(TIER_SHIP, check_funnel_coverage),     # M3 — ADVISORY (WARN-tier by ruling);
                               # zero-baseline ratchet over docs/audits/ disposition coverage,
                               # keyed on artifact identity. SHIP: 6,219 ms
    _tier(TIER_COMMIT, check_substrate_declaration),  # [#591] substrate validator layer 2 —
                               # REFUSE legs FAIL-armed against a post-2026-08-27 corpus
                               # measuring 0; the second-local-writer leg is WARN by the row's
                               # own words. COMMIT by rule (a): FAIL-capable
    _tier(TIER_SHIP, check_routing_agreement),    # [#613] — L0 routing copy vs the
    #                                             #   in-repo table. SHIP tier: the L0 copy
    #                                             #   is operator-disk and diverges at arm
    #                                             #   time, so a COMMIT-tier FAIL would wedge
    #                                             #   every commit on a file the repo may not
    #                                             #   write. The verdict stays fail/warn.
    _tier(TIER_COMMIT, check_dispatch_drift),      # [#592] — every literal command in
                               # PLAYBOOK Ch8's dispatch table resolves via Get-Command, and
                               # /lane-boot names the ruled verb. COMMIT by rule (a):
                               # FAIL-capable on an unresolvable command
    _tier(TIER_COMMIT, check_consumer_at_landing),  # [#595] — the subtraction mechanism.
                               # Leg 1 (a landing declares its consumer) FAIL-armed against a
                               # post-2026-08-27 corpus measuring 0; leg 2 (the identity-keyed
                               # consumption ratchet) WARN. COMMIT by rule (a): FAIL-capable
    _tier(TIER_COMMIT, check_proof_layer),         # [#596] — family 3 at the PROOF layer: a
                               # proof whose firing is gated on the environment it polices.
                               # WARN-tier identity ratchet, so it PASSES rule (a) — but rule
                               # (b) needs >=1 s of MEASURED cost and no measurement for it
                               # exists. Integration-time default is the strict direction;
                               # ship-tier is a live candidate for [#597]'s author to rule on,
                               # not an integrator's call to make silently
    _tier(TIER_SHIP, check_funnel_lifecycle),      # FM-2 — the funnel's EXIT step. The THIRD
                               # declared exception to the assignment rule above (after
                               # fleet_parity and routing_agreement): FAIL-capable and ship
                               # anyway, because leg a1 FAILs on live main by design and
                               # clearing it means RELOCATING a governed document — an act a
                               # committing lane may not perform. A COMMIT tier would wedge
                               # every commit on a defect the committer cannot legally
                               # repair. Promotion condition, written down rather than
                               # remembered: flip to TIER_COMMIT when leg a1 measures 0 on
                               # main. Full argument at the check's docstring
]


def detect_unconditionally_inert_checks(
    repo_paths: dict[str, Path],
    checks: "Sequence[Callable[[Path], list[Finding]]] | None" = None,
) -> list[Finding]:
    """[#465] leg 4 / FR-2 — WARN for any check that can only ever return SUBJECT-ABSENT.

    THE CLASS, NOT THE INSTANCE. `handoff_tag_canonicity` emitted a verdict every day for two
    spec generations after its subject stopped existing, and nothing noticed: 285 n/a vs 5
    pass across every `ecosystem/*/history/*.md` on `origin/automation/fleet-audit`, and those
    five passes were the leg-1 skip-as-pass defect. Deleting that one check would have repaired
    the instance and left the next one to die exactly as invisibly. This asks the question
    instead.

    SELF-ENUMERATING over `ALL_CHECKS`, never a hand-maintained roster (the leg-2/3 precedent,
    and FR-4: a "known-inert" list would reproduce the registry sprawl ADR-109 dissolves).
    `checks` is a test seam only; `None` late-binds the live registry so a member added
    tomorrow is covered with no edit here.

    INERT means, across every supplied repo: every result is `n/a`, AND at least one of them is
    SUBJECT-ABSENT. A check that is merely NOT-APPLICABLE everywhere is NOT inert — that is the
    FR-7 consumer-safety line, and getting it wrong is exactly the D1 defect the wave-1 producer
    lane shipped (it would have manufactured a fleet gap on corp-monorepo and ai-council).

    POSTURE (FR-3): WARN, never FAIL — it informs, it does not become a new way for the gate to
    go red on doc drift. An unclassified n/a, a check returning nothing, or a check that raises
    is itself a loud WARN: a detector that cannot see must not report clean.

    Read-only (FR-4 / ADR-28, ADR-36): it invokes read-only checks and writes nothing.

    Honest limits — it does NOT catch: a check that wrongly returns `pass`, a check whose
    assertions are vacuous, subject-absence recorded outside the `_na` prefix, or a check that
    is inert only on the repos it was not run against.
    """
    out: list[Finding] = []
    by_check: dict[str, dict[str, list[Finding]]] = {}
    for check in (ALL_CHECKS if checks is None else checks):
        name = getattr(check, "__name__", str(check)).removeprefix("check_")
        for repo_name, repo_path in repo_paths.items():
            try:
                returned = list(check(Path(repo_path)))
            except Exception as exc:  # noqa: BLE001 -- FR-3: surface, never swallow
                out.append(Finding("writer_integrity", "warn",
                                   f"{name}: could not be evaluated for {repo_name}: {exc!r}"
                                   .replace("|", "/")))
                continue
            # Register the check even when it returned NOTHING: the coverage rule below turns
            # the missing repo into a WARN. Skipping it entirely would make a check that
            # reports nothing disappear from the detector's view — silence about a gap, which
            # is the failure mode this leg exists to remove.
            slot = by_check.setdefault(name, {})
            if returned:
                slot[repo_name] = returned
    return out + classify_inert_checks(by_check, sorted(repo_paths))


def classify_inert_checks(by_check: "dict[str, dict[str, list[Finding]]]",
                          repo_names: "Sequence[str]") -> list[Finding]:
    """THE RULE, defined once, over findings that have ALREADY been computed.

    Extracted so the production path costs nothing (terra HIGH r1, 2026-08-04). `cmd_run` has
    just executed every check against every repo; re-running them inside the detector would
    double a whole fleet audit. Both callers share this function, so the daily and the test seam
    cannot drift about what "inert" means -- the single-definition discipline `journal_anchor`
    uses for the ADR-85 predicate.

    COVERAGE IS PART OF THE RULE (terra HIGH r2, 2026-08-04). `by_check` is keyed check -> repo,
    not check -> flat findings, because "inert" is a claim about the WHOLE fleet: concluding it
    from a subset would let one unavailable or half-audited repo retire a check that is alive
    elsewhere. A check missing a result from a repo that WAS evaluated is reported as incomplete
    coverage and explicitly NOT judged -- silence about a gap is the failure mode this whole leg
    exists to remove.

    `repo_names` must be the repos actually evaluated; callers exclude unavailable ones.
    """
    out: list[Finding] = []
    expected = set(repo_names)
    where = ", ".join(sorted(expected))
    for name in sorted(by_check):
        per_repo = by_check[name]
        missing = expected - set(per_repo)
        if missing:
            out.append(Finding("writer_integrity", "warn",
                               f"{name}: no result from {', '.join(sorted(missing))}; coverage is "
                               "incomplete so inertness was NOT judged -- a check that reports "
                               "nothing cannot be read as clean ([#465] leg 4)"))
            continue
        results = [f for fs in per_repo.values() for f in fs]
        if any(f.status != "n/a" for f in results):
            continue  # it can say something other than n/a somewhere -- not inert
        reasons = [_na_reason(f) for f in results]
        if any(r is None for r in reasons):
            out.append(Finding("writer_integrity", "warn",
                               f"{name}: emitted an n/a with no machine-readable reason -- it "
                               "cannot be told apart from a dead check ([#465] leg 4, FR-1)"))
            continue
        if _NA_SUBJECT_ABSENT not in reasons:
            continue  # NOT-APPLICABLE everywhere is a correct skip, not an inert check
        out.append(Finding("writer_integrity", "warn",
                           f"{name}: UNCONDITIONALLY INERT -- every result across [{where}] is "
                           f"n/a and its subject is absent, so the check can never fire. Fix its "
                           f"subject or retire it ([#465] leg 4)"))
    return out


# ---------------------------------------------------------------------------
# The check runner ([#533] leg 2) — serial by default, optionally threaded
# ---------------------------------------------------------------------------

# Ceiling on worker threads. NAMED, not inlined, so the number is configuration a reader can
# find and an operator can argue with rather than a literal buried in a call. The checks are
# I/O-bound (git subprocesses and file reads, measured 2026-08-16), so threads are the right
# primitive and the useful width is set by how many git processes the machine will usefully
# run at once, not by core count. `--workers` overrides it per invocation.
_PARALLEL_MAX_WORKERS = 8


# --- [#529] telemetry wiring: the switch, the destination, and the projection --------------
#
# DEFAULT OFF, and NAMED rather than inlined, for the reason `_PARALLEL_MAX_WORKERS` is named
# one line above: the switch is configuration a reader can find and an operator can argue with,
# not a literal buried in a call. This is also the architect's config-surface ruling for the
# [#529] wiring lane, verbatim — a named module constant plus a click option plus an env switch
# for the contexts with no click layer, and explicitly NOT a new runtime-knobs YAML file (that
# would be an ADR-101 Rule A/C question, i.e. an operator ruling rather than a lane's call).
#
# Flipping this default — turning emission on for the `audit-health` hook — is a SEPARATE
# ruling, exactly as flipping `--parallel` is. The flag exists so emission can be measured and
# opted into.
_TELEMETRY_DEFAULT = False

#: Env switch for contexts that have no click layer. `audit-health` runs as a pre-commit hook
#: and cannot be handed a flag; the three gate organs have no CLI at all. An explicit
#: `--telemetry/--no-telemetry` still WINS over this, so an operator can turn one run off
#: without editing their environment.
TELEMETRY_ENV = "DEV_KNOWLEDGE_TELEMETRY"

#: What counts as "on". Enumerated rather than tested for truthiness: `bool("0")` is True, and a
#: switch that reads `DEV_KNOWLEDGE_TELEMETRY=0` as ON is a switch that looks wired and is not.
_TELEMETRY_ON_VALUES = frozenset({"1", "true", "yes", "on"})


def telemetry_enabled(explicit: bool | None = None) -> bool:
    """Is [#529] emission on? `explicit` (a `--telemetry/--no-telemetry` flag) wins if given."""
    if explicit is not None:
        return explicit
    return os.environ.get(TELEMETRY_ENV, "").strip().lower() in _TELEMETRY_ON_VALUES


def _telemetry_db_path() -> Path:
    """The [#529] store, derived from THIS module's `_REPO_ROOT`, read AT CALL TIME.

    NEVER `telemetry_emit.default_db_path()`, and the reason is a live seam defect rather than a
    style preference. That function reads `telemetry_emit._REPO_ROOT`, an independent
    module-level value that nothing in `tests/` patches; `audit._REPO_ROOT` is one of the 25
    names the suite DOES patch. A runner that leaned on the library default would write into the
    REAL `logs/` on every suite run while every sandbox assertion — including
    `tests/test_ship_gate.py::test_ship_gate_is_readonly`, which compares an `rglob` snapshot of
    the tmp tree — kept passing. That is the seam-detaches-silently failure class
    `audit_checks/registry.py` documents: the check still passes while testing nothing.

    Reading `_REPO_ROOT` per call (not binding it at import) is the same discipline `run_checks`
    applies to `ALL_CHECKS`, and for the same reason.

    `DEV_KNOWLEDGE_TELEMETRY_DB` stays the operator/sandbox override — it is how a hook
    subprocess in a test gets pointed at a tmp store — so it is honoured first. What is NOT
    inherited is the library's *fallback root*.
    """
    override = os.environ.get(_te.DB_PATH_ENV)
    if override:
        return Path(override)
    return Path(_REPO_ROOT) / _te.DEFAULT_DB_RELPATH


def _elapsed_ms(start: float) -> int:
    """Milliseconds since `start`, as an int — `emit_event` refuses a non-int `duration_ms`.

    `perf_counter` and not `time.time()`: this is a duration, and a wall clock that steps
    (NTP, a DST boundary) can make a duration negative.
    """
    return int((time.perf_counter() - start) * 1000)


def _check_outcome(findings: Sequence[Finding]) -> str:
    """Project `Finding.status` (5 values) onto `telemetry_emit.OUTCOMES` (3). Lane L2 STEP 1.

    `fail` -> `block`, because `fail` is the only status that stops a commit at `audit-health`
    or a ship at `ship-gate`. Everything else -> `pass`: a `warn` informs, an `n/a`/`unavailable`
    did not evaluate, and none of them refuses an action. A check that RAISED is neither, and is
    emitted as `error` by the caller — that is what `OUTCOMES`' third value is for.

    The projection is a function with a test rather than an inline expression because
    `emit_event` RAISES `TelemetryError` on an unknown outcome and `safe_emit` deliberately does
    not swallow that class: a drifting mapping would crash the audit, not degrade quietly.
    """
    return "block" if any(f.status == "fail" for f in findings) else "pass"


def _check_context(findings: Sequence[Finding]) -> dict:
    """What the 5-to-3 collapse would otherwise lose, carried so the read side loses nothing.

    `finding_names` is here for a specific join: the event's `name` is the check FUNCTION's
    `__name__` (`check_doc_claims`), because that is the only name a check emitting ZERO findings
    has — and a check that found nothing still ran, which is exactly the memo's
    "fires>0/blocks=0, retire it" question. But `ecosystem/disposition-register.yaml` and the
    ship-gate key on `Finding.check_name` (`doc_claims`), a different string. Carrying both lets
    a reader join a `check_run` row to the register without re-deriving the relationship.
    """
    return {
        "statuses": dict(sorted(Counter(f.status for f in findings).items())),
        "findings": len(findings),
        "finding_names": sorted({f.check_name for f in findings}),
    }


def _parallel_workers(n_checks: int) -> int:
    """Default width for `n_checks` checks: the configured cap, but never wider than the work.

    Floored at 1 because `ThreadPoolExecutor(max_workers=0)` raises -- an empty registry is a
    legitimate call (`tests/test_audit.py` monkeypatches `ALL_CHECKS` down to a single check,
    and a future caller could pass none) and it must not become a crash.
    """
    return max(1, min(_PARALLEL_MAX_WORKERS, n_checks))


@contextlib.contextmanager
def _cached_reads():
    """P3 (intake #71): a read-through file cache for ONE `run_checks` call, keyed on
    path + mtime.

    Patches `Path.read_text` for the DURATION of this context only -- restored in `finally`,
    so nothing outlives the run and no cache persists across processes (criterion 6 of #71:
    library-first, stdlib only, no cross-run state). No check anywhere has to change how it
    reads a file: many checks independently re-read the same canonical docs (measured: 43% of
    `Path.read_text` calls across a full run are re-reads of a path already read), so patching
    the one shared method both checks and helper modules already call covers them all without
    touching each call site.

    Keyed on `(path, mtime_ns, size)`, not path alone: every check here is documented
    read-only (Layer-2, no file writes), so no check should mutate a file mid-run, but the key
    still catches it rather than serving stale content if one ever does. `args`/`kwargs` ride
    along in the key so a caller passing a different encoding is never served another
    caller's decoded text.
    """
    cache: dict[tuple, str] = {}
    orig_read_text = Path.read_text

    def cached_read_text(self, *args, **kwargs):
        try:
            st = self.stat()
        except OSError:
            return orig_read_text(self, *args, **kwargs)
        key = (str(self), st.st_mtime_ns, st.st_size, args, tuple(sorted(kwargs.items())))
        if key in cache:
            return cache[key]
        text = orig_read_text(self, *args, **kwargs)
        cache[key] = text
        return text

    Path.read_text = cached_read_text
    try:
        yield
    finally:
        Path.read_text = orig_read_text


def run_checks(repo_path: Path, checks: Sequence[Callable] | None = None,
               parallel: bool = False, workers: int | None = None,
               telemetry: bool = _TELEMETRY_DEFAULT,
               telemetry_db: str | os.PathLike | None = None,
               tier: str | None = None) -> list[Finding]:
    """Run `checks` against `repo_path` and return their findings IN REGISTRY ORDER.

    ORDER IS THE CONTRACT, not a side effect. `CHECK_ORDER` is the order findings are emitted
    in, so it is part of the byte-identical output the git hooks read; results are therefore
    collected into a per-check slot and flattened in submission order, NEVER appended as work
    completes. A check emitting several findings keeps them contiguous in its own slot.

    SERIAL IS THE DEFAULT and this function changes no caller's behaviour by existing. Every
    runner loop routes through it so the two modes cannot drift into two different definitions
    of "run the checks", but nothing switches to threads unless it is asked to. Flipping the
    `audit-health` hook's default is a separate ruling ([#533] leg 2 contract), not a
    consequence of this code landing.

    `checks=None` reads the module-level `ALL_CHECKS` AT CALL TIME, deliberately: binding it as
    a default argument would freeze the list at import and silently detach the seam
    `tests/test_audit.py` monkeypatches -- a check that keeps passing while testing nothing,
    which is the exact failure class `audit_checks/registry.py` documents.

    THREADS, not processes: the checks are I/O-bound (git subprocesses, file reads), they share
    process-global state a `ProcessPoolExecutor` could not (the `journal_anchor` memos; before
    [#597] also `_GATE_MODE`), and several are closures over module state that would not pickle.

    An exception in a worker PROPAGATES -- `future.result()` re-raises it on this thread. A
    runner that swallowed it would turn a loud failure into a silently short report, which is
    the worst outcome available to an audit.

    TELEMETRY ([#529] leg 1) IS AN OBSERVER AND NOTHING ELSE, default OFF. When `telemetry` is
    true this emits one `check_run` event per check — name, outcome, `duration_ms` — and the
    findings it returns are field-by-field what it returns with emission off, in both modes.
    Three properties are load-bearing enough to be tests rather than comments
    (`tests/test_telemetry_wiring.py`):

      * emission happens AFTER the slot flatten, walking slots in registry order, so emitted
        event order == `CHECK_ORDER` == finding order. Emitting inside a worker would interleave
        by completion order — the same thing the slots exist to prevent for the findings;
      * `duration_ms` is timed INSIDE the worker, around `check(repo_path)`, never around
        `future.result()`. The latter bills every check for its queue wait and reports a
        fabricated number that looks plausible;
      * a store failure NEVER reaches the caller. `safe_emit` swallows `sqlite3.Error`/`OSError`,
        so a locked database cannot turn a green gate into a failed commit. It does NOT swallow
        `TelemetryError` — that class is a wiring defect, and hiding it would ship a gate that
        silently records nothing.

    A check that RAISES emits `outcome="error"` at the point of failure (there is no flatten to
    walk on that path) and then propagates unchanged.

    TIER ([#597]) IS THE ONLY THING THAT DECIDES WHETHER A CHECK RUNS, and `None` — the default —
    runs everything, so no existing caller changes behaviour by this parameter existing. At
    `TIER_COMMIT` a ship-tier check is NOT dropped from the output: its slot carries one `n/a`
    Finding naming the tier it was deferred to, so the report still enumerates all 46 organs and
    the operator can see at the commit gate what the commit gate did not do. Silence would make a
    deferred check indistinguishable from a deleted one — the `handoff_tag_canonicity` failure
    class this module already refuses in `detect_unconditionally_inert_checks`.

    A DEFERRED CHECK EMITS NO TELEMETRY, deliberately. Its `duration_ms` would be ~0, and a run
    of zeros would silently re-rank the very table the tier decisions are read from: the next
    person to profile would conclude the ship-tier checks are free. No row is better than a
    fabricated one.
    """
    active = list(ALL_CHECKS if checks is None else checks)
    # Validated ONCE here, not only per-check: `runs_at_tier` raises on an unknown tier, but a
    # per-check comprehension never reaches it on an EMPTY registry — and an empty registry is a
    # legitimate call (`tests/` monkeypatches `ALL_CHECKS` down to nothing). Without this line a
    # typo'd tier would return a clean, empty, GREEN result. (terra HIGH, 2026-08-27.)
    if tier is not None and tier not in GATE_TIERS:
        raise ValueError(f"unknown runner tier {tier!r} — expected None or one of {GATE_TIERS}")
    runs = [runs_at_tier(c, tier) for c in active]
    db = None
    if telemetry:
        db = Path(telemetry_db) if telemetry_db is not None else _telemetry_db_path()

    durations: list[int | None] = [None] * len(active)

    def _deferred(check) -> list[Finding]:
        name = getattr(check, "__name__", repr(check)).removeprefix("check_")
        return [_na(name, _NA_NOT_APPLICABLE,
                    f"declared {tier_of(check)}-tier -- not run at the {tier} gate "
                    "([#597] per-check tiering; ship-gate and `audit run` run it)")]

    def _run_one(index: int, check: Callable) -> list[Finding]:
        """Run ONE check, recording its own elapsed time. Never swallows, never reorders."""
        start = time.perf_counter()
        try:
            out = list(check(repo_path))
        except BaseException as exc:
            if db is not None:
                _te.safe_emit(_te.emit_check_run, getattr(check, "__name__", repr(check)),
                              "error", _elapsed_ms(start), db_path=db,
                              context={"error": type(exc).__name__})
            raise
        durations[index] = _elapsed_ms(start)
        return out

    with _cached_reads():
        if not parallel:
            slots = [_run_one(i, check) if runs[i] else _deferred(check)
                     for i, check in enumerate(active)]
        else:
            width = workers if workers is not None else _parallel_workers(sum(runs) or 1)
            slots = [_deferred(c) if not runs[i] else [] for i, c in enumerate(active)]
            with ThreadPoolExecutor(max_workers=max(1, width)) as pool:
                futures = {pool.submit(_run_one, i, check): i
                           for i, check in enumerate(active) if runs[i]}
                for future in as_completed(futures):
                    slots[futures[future]] = list(future.result())

    if db is not None:
        for index, (check, slot) in enumerate(zip(active, slots)):
            if not runs[index]:
                continue
            _te.safe_emit(_te.emit_check_run, getattr(check, "__name__", repr(check)),
                          _check_outcome(slot), durations[index], db_path=db,
                          context=_check_context(slot))
    return [f for slot in slots for f in slot]


def audit_repo(repo_name: str, repo_path: Path, run_date: date) -> RepoState:
    """Run all checks on a single repo and return updated state."""
    if not repo_path.exists():
        state = RepoState(
            name=repo_name,
            path=str(repo_path),
            last_audit=run_date.isoformat(),
            findings=[Finding("availability", "unavailable", f"Path not found: {repo_path}")],
        )
        return state

    findings = run_checks(repo_path)
    state = RepoState(
        name=repo_name,
        path=str(repo_path),
        last_audit=run_date.isoformat(),
        findings=findings,
    )
    return state

# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

# "unavailable" = path-absent / couldn't run; "n/a" = ran but not applicable here (a hub
# no-op: no docs/handoffs/, no section 3.1, no floor). Both surface as "N/A" in the report
# table -- distinguished by the evidence text and the separate per-status tallies below.
_STATUS_EMOJI = {"pass": "✓", "fail": "✗", "warn": "!", "unavailable": "?", "n/a": "-"}
_STATUS_LABEL = {"pass": "PASS", "fail": "FAIL", "warn": "WARN", "unavailable": "N/A", "n/a": "N/A"}


def generate_report(states: list[RepoState], run_date: date, repo_root: Path) -> str:
    ts = datetime.now().isoformat(timespec="seconds")
    total_checks = sum(len(s.findings) for s in states)
    passed = sum(1 for s in states for f in s.findings if f.status == "pass")
    failed = sum(1 for s in states for f in s.findings if f.status == "fail")
    warned = sum(1 for s in states for f in s.findings if f.status == "warn")
    unavailable = sum(1 for s in states for f in s.findings if f.status == "unavailable")
    n_a = sum(1 for s in states for f in s.findings if f.status == "n/a")

    lines = [
        "# Ecosystem Audit Report\n",
        "\n",
        "<!-- scope: meta -->\n",
        "\n",
        f"**Date:** {run_date.isoformat()}  \n",
        f"**Generated:** {ts}  \n",
        f"**Repos audited:** {len(states)}  \n",
        f"**Checks:** {total_checks} total — {passed} pass, {failed} fail, {warned} warn, {unavailable} unavailable, {n_a} n/a\n",
        "\n",
        "---\n",
        "\n",
    ]

    for state in states:
        repo_fail = any(f.status == "fail" for f in state.findings)
        repo_unavail = any(f.status == "unavailable" for f in state.findings)
        summary_status = "UNAVAILABLE" if repo_unavail else ("FAIL" if repo_fail else "PASS")
        lines.append(f"## {state.name} — {summary_status}\n\n")
        lines.append(f"**Path:** `{state.path}`  \n")
        lines.append(f"**Last audit:** {state.last_audit}\n\n")
        lines.append("| Check | Status | Evidence |\n")
        lines.append("|---|---|---|\n")
        for f in state.findings:
            label = _STATUS_LABEL.get(f.status, f.status.upper())
            lines.append(f"| `{f.check_name}` | {label} | {f.evidence} |\n")
        history_rel = Path("ecosystem") / state.name / "history"
        lines.append(f"\nHistory: [`{history_rel}/`]({history_rel}/)\n\n")
        lines.append("---\n\n")

    lines.append("## Summary\n\n")
    lines.append(f"- {len(states)} repo(s) audited\n")
    lines.append(f"- {passed}/{total_checks} checks passed\n")
    if failed:
        lines.append(f"- **{failed} failure(s)** — route findings to repo owners\n")
    if warned:
        lines.append(f"- {warned} warning(s)\n")
    if unavailable:
        lines.append(f"- {unavailable} unavailable (path not found)\n")
    if n_a:
        lines.append(f"- {n_a} n/a (check not applicable to that repo)\n")
    lines.append("\n*Report generated by `scripts/audit.py`. Do not edit manually.*\n")

    return "".join(lines)


def write_report(content: str, run_date: date, single_repo: Optional[str] = None) -> Path:
    AUDITS_DIR.mkdir(parents=True, exist_ok=True)
    if single_repo:
        filename = f"{run_date.isoformat()}-{single_repo}-audit.md"
    else:
        filename = f"{run_date.isoformat()}-ecosystem-audit.md"
    out = AUDITS_DIR / filename
    out.write_text(content, encoding="utf-8", newline="\n")
    return out

# ---------------------------------------------------------------------------
# ecosystem-index regeneration
# ---------------------------------------------------------------------------

def regenerate_index(states: list[RepoState]) -> None:
    """Write the derived ecosystem/index.yaml rollup from the given repo states.

    Shape: `{generated: <ISO timestamp>, repos: [<RepoState.to_dict()>, ...]}` — an
    aggregate snapshot of every registered repo's last audit, for a one-file read of
    ecosystem health. Derived and regenerated wholesale by `registry update`; do not
    edit by hand (manual edits are lost on the next run). The per-repo state.yaml
    files are the source of truth — the index is always rebuildable from them.
    """
    index = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "repos": [s.to_dict() for s in states],
    }
    ECOSYSTEM_INDEX.parent.mkdir(parents=True, exist_ok=True)
    with open(ECOSYSTEM_INDEX, "w", encoding="utf-8", newline="\n") as fh:
        yaml.dump(index, fh, default_flow_style=False, allow_unicode=True)

# ---------------------------------------------------------------------------
# ADR-84 (Q9) writer commit — isolate durable outputs to automation/fleet-audit
# ---------------------------------------------------------------------------

_AUTOMATION_BRANCH = "automation/fleet-audit"


def _parse_porcelain(raw: str) -> list:
    """Parse `git status --porcelain` lines into [(xy, path), ...]. Pure.

    `xy` is the two-char status field; `path` is repo-relative. Durable output
    paths never rename, so the simple `XY<space>PATH` split suffices.
    """
    out = []
    for line in raw.splitlines():
        if len(line) < 4:
            continue
        out.append((line[:2], line[3:].strip().strip('"')))
    return out


def _restore_durable_scope(pathspecs: list) -> None:
    """Return the working tree to HEAD within the durable output paths.

    Crash-safe cleanup (called from a `finally`): RE-DERIVES the dirty state in
    the durable scope itself (so it runs correctly however the caller exited —
    a failed pre-commit snapshot, a mid-plumbing crash, or success), then removes
    NEW untracked outputs and restores MODIFIED tracked files from HEAD. Only
    paths git reports dirty IN SCOPE are touched — never arbitrary files.
    Best-effort: a git-status or per-path failure is logged, never raised.
    """
    st = subprocess.run(
        ["git", "-C", _REPO_ROOT, "status", "--porcelain", "--untracked-files=all", "--", *pathspecs],
        capture_output=True, text=True,
    )
    if st.returncode != 0:
        logger.warning("ADR-84 restore: git status failed — durable scope NOT cleaned (%s)",
                       st.stderr.strip())
        return
    changed = _parse_porcelain(st.stdout)
    untracked = [p for (xy, p) in changed if xy == "??"]
    tracked = [p for (xy, p) in changed if xy != "??"]
    for p in untracked:
        fp = Path(_REPO_ROOT) / p
        try:
            if fp.is_file():
                fp.unlink()
        except OSError as exc:
            logger.warning("ADR-84 restore: could not remove %s — %s", p, exc)
    if tracked:
        subprocess.run(
            ["git", "-C", _REPO_ROOT, "checkout", "HEAD", "--", *tracked],
            capture_output=True, text=True,
        )


_PUSH_TIMEOUT_S = 120


def _push_routine_branch(repo_path: Optional[Path] = None) -> tuple[bool, str]:
    """[#460] — replicate `automation/fleet-audit` to origin. Returns (ok, detail).

    PLACEMENT: called by `_commit_routine_outputs` immediately after `update-ref`, so the
    push belongs to the ACT THAT CREATES THE COMMIT rather than to a separate scheduler leg.
    That is the whole lesson of [#460]: the previous push was a separate, manual organ, so it
    could die without the writer noticing, and it did -- for 16 days. One act, one failure
    surface. (The repo's own ratified line: "push is part of the act it verifies".)

    LOUD ON FAILURE, at ERROR: the surrounding writer is deliberately fail-soft, logging
    WARNs for its ordinary skips, so a replication failure logged at WARN would be
    indistinguishable from "nothing to record today" -- silent success theater, which is the
    defect class itself.

    NEVER RAISES: loud must not mean fatal. Breaking the nightly routine to report a failed
    push would trade a replication gap for a total outage. Persistence is carried by
    `check_fleet_audit_replication`, which sees the lag on every subsequent run.

    Non-interactive and bounded: GIT_TERMINAL_PROMPT=0 plus a timeout, because this runs
    unattended under Task Scheduler where a credential prompt would hang the routine forever.
    """
    repo = Path(repo_path) if repo_path is not None else _REPO_ROOT
    scrub = _git_location_env()
    env = {k: v for k, v in os.environ.items() if k not in scrub}
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        p = subprocess.run(
            ["git", "-C", str(repo), "push", "origin",
             f"refs/heads/{_AUTOMATION_BRANCH}:refs/heads/{_AUTOMATION_BRANCH}"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            env=env, timeout=_PUSH_TIMEOUT_S,
        )
    except subprocess.TimeoutExpired:
        detail = f"push timed out after {_PUSH_TIMEOUT_S}s"
        logger.error("ADR-80 REPLICATION FAILED (%s): %s -- the durable record is local-only "
                     "([#460])", _AUTOMATION_BRANCH, detail)
        return (False, detail)
    except OSError as exc:
        detail = f"could not run git push: {exc!r}"
        logger.error("ADR-80 REPLICATION FAILED (%s): %s -- the durable record is local-only "
                     "([#460])", _AUTOMATION_BRANCH, detail)
        return (False, detail)

    if p.returncode != 0:
        detail = (p.stderr or p.stdout or "no output").strip().replace("\n", " ")[:400]
        logger.error("ADR-80 REPLICATION FAILED (%s): %s -- the durable record is local-only "
                     "([#460])", _AUTOMATION_BRANCH, detail)
        return (False, detail)
    return (True, "pushed")


def _commit_routine_outputs(run_date: date) -> bool:
    """Capture this run's durable audit outputs onto the `automation/fleet-audit`
    branch via git plumbing — never to `main` (ADR-84 / Q9 writer isolation).

    `cmd_run` writes the durable outputs (docs/audits/, ecosystem/<name>/history/)
    into the main working tree; this records their current state onto the orphan,
    output-only `automation/fleet-audit` branch using a SEPARATE index
    (`GIT_INDEX_FILE`) + `commit-tree` plumbing, so main's HEAD / index / working
    tree are never touched and no pre-commit hook fires. The working tree is then
    restored so the just-written outputs do not dirty `main` (the baseline has no
    readers — the live copy lives on the branch). The branch is created
    (parent-less root) on first run. `state.yaml` is gitignored, never staged,
    and stays.

    Fail-soft + crash-safe: any git error logs a WARN and returns; the
    working-tree restore always runs in a `finally`. Enumerates concrete history/
    paths (no glob — git on Windows does not expand `*` in a subprocess pathspec).
    Assumes the durable scope is clean going in (the automation invariant).

    Returns True when this run's outputs are ON the branch (freshly committed, or
    already there under an identical tree), else False. [#296]: the caller needs
    this to print an locator that is TRUE — the restore below removes the report
    from the working tree either way, so "where it landed" and "whether it landed"
    are the same question, and a caller that cannot ask it prints a path to nothing.
    """
    repo = _REPO_ROOT
    history_specs = (
        [
            (d / "history").relative_to(repo).as_posix()
            for d in sorted(ECOSYSTEM_DIR.iterdir())
            if d.is_dir()
        ]
        if ECOSYSTEM_DIR.exists()
        else []
    )
    pathspecs = history_specs + [AUDITS_DIR.relative_to(repo).as_posix()]

    tmp_index = None
    try:
        # Snapshot durable-scope changes for the branch commit. The early-returns
        # below are INSIDE the try, so the finally always runs the restore — which
        # re-derives the scope itself, cleaning main even if this status call (after
        # cmd_run wrote outputs) fails.
        status = subprocess.run(
            ["git", "-C", repo, "status", "--porcelain", "--untracked-files=all", "--", *pathspecs],
            capture_output=True, text=True,
        )
        if status.returncode != 0:
            logger.warning("ADR-84 commit: git status failed — %s", status.stderr.strip())
            return False
        changed = _parse_porcelain(status.stdout)
        if not changed:
            return False  # nothing new this run
        # Stage ONLY this run's changed files (not whole dirs): git 2.0+ `git add <dir>`
        # stages deletions, so re-adding dirs against a branch-seeded index would prune
        # prior outputs (which the restore removes from the working tree). Adding the
        # exact changed paths makes the branch ACCUMULATE.
        changed_paths = [p for (_xy, p) in changed]

        fd, tmp_index = tempfile.mkstemp(prefix="q9-fleet-idx-")
        os.close(fd)
        # mkstemp leaves a 0-byte file, which git rejects as a malformed index.
        # Remove it so git writes a fresh, valid index (read-tree on branch-exists,
        # or git add on the orphan first run) at this reserved unique path.
        os.remove(tmp_index)
        env = dict(os.environ, GIT_INDEX_FILE=tmp_index)

        branch_exists = subprocess.run(
            ["git", "-C", repo, "rev-parse", "--verify", "--quiet",
             f"{_AUTOMATION_BRANCH}^{{commit}}"],
            capture_output=True, text=True,
        ).returncode == 0

        # Seed the temp index from the branch tip so the commit accumulates prior
        # outputs (an EMPTY index on first run → an orphan, output-only root).
        if branch_exists:
            rt = subprocess.run(
                ["git", "-C", repo, "read-tree", _AUTOMATION_BRANCH],
                env=env, capture_output=True, text=True,
            )
            if rt.returncode != 0:
                logger.warning("ADR-84 commit: read-tree failed — %s", rt.stderr.strip())
                return False

        add = subprocess.run(
            ["git", "-C", repo, "add", "--", *changed_paths],
            env=env, capture_output=True, text=True,
        )
        if add.returncode != 0:
            logger.warning("ADR-84 commit: git add failed — %s", add.stderr.strip())
            return False

        wt = subprocess.run(
            ["git", "-C", repo, "write-tree"],
            env=env, capture_output=True, text=True,
        )
        if wt.returncode != 0:
            logger.warning("ADR-84 commit: write-tree failed — %s", wt.stderr.strip())
            return False
        tree = wt.stdout.strip()

        parent_args = []
        if branch_exists:
            cur_tree = subprocess.run(
                ["git", "-C", repo, "rev-parse", f"{_AUTOMATION_BRANCH}^{{tree}}"],
                capture_output=True, text=True,
            ).stdout.strip()
            if tree == cur_tree:
                return True  # identical tree — already recorded on the branch
            parent_args = ["-p", _AUTOMATION_BRANCH]

        msg = (
            f"chore(routine/fleet-audit): record {run_date} baseline\n"
            "\n"
            "Routine: fleet-audit"
        )
        ct = subprocess.run(
            ["git", "-C", repo, "commit-tree", tree, *parent_args, "-m", msg],
            capture_output=True, text=True,
        )
        if ct.returncode != 0:
            logger.warning("ADR-84 commit: commit-tree failed — %s", ct.stderr.strip())
            return False
        commit = ct.stdout.strip()

        ur = subprocess.run(
            ["git", "-C", repo, "update-ref", f"refs/heads/{_AUTOMATION_BRANCH}", commit],
            capture_output=True, text=True,
        )
        if ur.returncode != 0:
            logger.warning("ADR-84 commit: update-ref failed — %s", ur.stderr.strip())
            return False
        # [#460]: the commit exists on ONE disk until this runs. Replication is part of the
        # act, not a follow-on chore — the follow-on chore is precisely what died in July.
        _push_routine_branch(repo)
        return True
    except Exception as exc:
        logger.warning("ADR-84 commit: unexpected error — %s", exc)
        return False
    finally:
        _restore_durable_scope(pathspecs)
        if tmp_index and os.path.exists(tmp_index):
            try:
                os.remove(tmp_index)
            except OSError:
                pass


def report_locator(out, recorded: bool) -> str:
    """[#296] The one honest sentence about where a report actually is.

    The write is real, but `_commit_routine_outputs` records the durable scope onto
    `automation/fleet-audit` and then RESTORES the working tree, so by the time the
    command returns the path it just wrote no longer exists there. Printing that bare
    path (the pre-[#296] behaviour) sent every caller to look where the file is not --
    a misleading locator, NOT a lost report: the live copy is the branch copy. A live
    repro on 2026-08-06 refuted the row's original guess of a suppressed write.

    When the branch commit did NOT happen, say so plainly rather than name a branch
    path that has nothing at it -- the fail-soft path logs a WARN and the report is
    genuinely gone.
    """
    rel = str(out)
    root = str(_REPO_ROOT)
    if rel.startswith(root):
        rel = rel[len(root):].lstrip(chr(92) + "/")
    rel = rel.replace(chr(92), "/")
    if recorded:
        return (f"Report: {rel} on branch {_AUTOMATION_BRANCH} "
                f"(read it with: git show {_AUTOMATION_BRANCH}:{rel}) "
                f"-- not in the working tree; the durable scope is restored after the run")
    return (f"Report: NOT recorded -- {rel} was written, then removed by the durable-scope "
            f"restore without reaching {_AUTOMATION_BRANCH} (see the ADR-84 WARN above)")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

@click.group()
def cli() -> None:
    """Ecosystem audit tool — reads child repos, writes only to .dev-knowledge."""


@cli.command("run")
@click.option("--repo-path", "repo_path", default=None,
              help="Bootstrap: path to a repo not yet registered. Creates state.yaml on first use.")
def cmd_run(repo_path: Optional[str]) -> None:
    """Run the full ecosystem audit; write a report to docs/audits/.

    Runs ALL_CHECKS against every registered repo, saves each repo's state.yaml,
    appends to ecosystem/<name>/history/YYYY-MM-DD.md, and writes a dated report.
    Exits 1 if any check fails. Cross-repo findings are advisory — remediation is
    manual in the child repo (no downstream commit gating; ARCHITECTURE.md / ADR-36).

    --repo-path bootstraps a not-yet-registered repo: it creates that repo's
    state.yaml and permanently registers it, then runs. It does NOT refresh the
    derived ecosystem/index.yaml — follow with `registry update` for that. The
    bootstrapped path is the operator's EXPLICIT answer for that repo and outranks
    every other resolution step for this run ([#605]).

    Examples:
        python scripts/audit.py run
        python scripts/audit.py run --repo-path ../corp-monorepo
    """
    run_date = date.today()

    # (name, path) of the repo bootstrapped by --repo-path, else None. Held rather than
    # left to be re-read from state.yaml: since [#605] the env var outranks the stored
    # path, so a set DEV_KNOWLEDGE_REPO_ROOT_<SLUG> would otherwise silently audit a
    # different tree than the one the operator just registered on this command line.
    bootstrapped: Optional[tuple[str, str]] = None

    if repo_path:
        rp = Path(repo_path).resolve()
        repo_name = rp.name
        click.echo(f"Bootstrapping: registering {repo_name} at {rp}")
        # Create/update state.yaml for the new repo, then fall through to full run
        bootstrap_state = RepoState(name=repo_name, path=str(rp),
                                    last_audit=None, findings=[])
        save_state(bootstrap_state)
        bootstrapped = (repo_name, str(rp))

    names = discover_repos()
    if not names:
        click.echo("No repos registered in ecosystem/. Use --repo-path to register one.", err=True)
        sys.exit(0)
    # [#465] leg 4 / FR-2: the inert-check detector must actually RUN in production -- a
    # detector nothing calls is a mechanism that reports nothing, which is the exact class this
    # leg was opened to remove (terra HIGH r1, 2026-08-04).
    #
    # It is fleet-scoped by construction (a check that is n/a here and firing there is alive),
    # so the hub's verdict cannot be written until every repo has been audited. ONLY the hub's
    # persistence is deferred: consumers still save-and-append as they complete, exactly as
    # before, so a later repo raising cannot lose earlier repos' durable progress (terra HIGH
    # r2 -- deferring everything silently changed that failure semantics). The hub is persisted
    # in a `finally`, so it survives that failure too, with whatever coverage was achieved.
    states = []
    hub_state = None
    try:
        for name in names:
            existing = load_state(name)
            stored = existing.path if existing else None
            # The non-bootstrap call stays two-positional deliberately: `resolve_repo_path`
            # is a documented monkeypatch seam (tests/test_writer_integrity.py substitutes a
            # two-argument lambda), so the `explicit=` keyword is passed only on the one
            # branch that has an explicit answer to pass.
            if bootstrapped is not None and name == bootstrapped[0]:
                rp = resolve_repo_path(name, stored, explicit=bootstrapped[1])
            else:
                rp = resolve_repo_path(name, stored)
            state = audit_repo(name, rp, run_date)
            states.append(state)
            if state.name == HUB_REPO_NAME:
                hub_state = state          # held back for the fleet-scoped detector
            else:
                save_state(state)
                append_history(state, run_date)
    finally:
        if hub_state is not None:
            # An unavailable repo contributes no check results; judging inertness against it
            # would let one missing tree retire a check that is alive everywhere else.
            evaluated = [s for s in states
                         if not any(f.check_name == "availability" and f.status == "unavailable"
                                    for f in s.findings)]
            by_check: dict[str, dict[str, list[Finding]]] = {}
            for s in evaluated:
                for f in s.findings:
                    by_check.setdefault(f.check_name, {}).setdefault(s.name, []).append(f)
            # WARNs attach to the HUB only: this is hub-owned machinery, and writing one onto a
            # consumer would manufacture exactly the fleet gap FR-7 forbids.
            hub_state.findings.extend(
                classify_inert_checks(by_check, [s.name for s in evaluated]))
            save_state(hub_state)
            append_history(hub_state, run_date)

    report = generate_report(states, run_date, Path(_REPO_ROOT))
    out = write_report(report, run_date)
    recorded = _commit_routine_outputs(run_date)
    click.echo(report_locator(out, recorded))

    failures = sum(1 for s in states for f in s.findings if f.status == "fail")
    if failures:
        click.echo(f"{failures} check failure(s). See report for details.", err=True)
        sys.exit(1)


@cli.command("repo")
@click.argument("name")
@click.option("--repo-path", "repo_path", default=None,
              help="Consumer working-tree path, overriding every other resolution step. "
                   "Without it: DEV_KNOWLEDGE_REPO_ROOT_<SLUG>, then the stored path in "
                   "ecosystem/<repo>/state.yaml, then the sibling default ([#605]).")
def cmd_repo(name: str, repo_path: Optional[str]) -> None:
    """Audit a single repo by name.

    Same state.yaml / history / report writes as `run`, scoped to one repo. The
    report is written as docs/audits/YYYY-MM-DD-<name>-audit.md and then RECORDED
    ON the `automation/fleet-audit` branch (ADR-84 writer isolation) -- the working
    tree is restored afterwards, so the file is NOT left in your checkout. Read it
    with `git show automation/fleet-audit:docs/audits/...`; the command prints the
    exact invocation. Exits 1 on any failure.

    Where the tree comes from ([#605]): --repo-path, else
    DEV_KNOWLEDGE_REPO_ROOT_<SLUG>, else the stored path in ecosystem/<name>/state.yaml,
    else the sibling default. The env var is the step that makes this command runnable
    from a checkout with no sibling tree — the state file is gitignored, so on a fresh
    clone of the hub alone there is no stored path to fall back to.

    Examples:
        python scripts/audit.py repo ai-council
        python scripts/audit.py repo corp-monorepo --repo-path ../corp-monorepo
        DEV_KNOWLEDGE_REPO_ROOT_AI_COUNCIL=/srv/ai-council python scripts/audit.py repo ai-council
    """
    run_date = date.today()
    existing = load_state(name)

    rp = resolve_repo_path(name, existing.path if existing else None, explicit=repo_path)
    if not repo_path and not existing:
        click.echo(f"No state.yaml for {name}; assuming path {rp}")

    state = audit_repo(name, rp, run_date)
    save_state(state)
    append_history(state, run_date)

    report = generate_report([state], run_date, Path(_REPO_ROOT))
    out = write_report(report, run_date, single_repo=name)
    recorded = _commit_routine_outputs(run_date)
    click.echo(report_locator(out, recorded))

    failures = sum(1 for f in state.findings if f.status == "fail")
    if failures:
        click.echo(f"{failures} check failure(s).", err=True)
        sys.exit(1)


@cli.command("registry")
@click.argument("action", type=click.Choice(["update"]))
def cmd_registry(action: str) -> None:
    """Manage the ecosystem registry. Action: `update`.

    `update` regenerates the derived ecosystem/index.yaml from the current
    ecosystem/<name>/state.yaml files — a pure read-state -> write-index operation:
    it runs no checks, writes no history, and generates no report. Run it after
    registering a repo (e.g. after `run --repo-path`) to keep the rollup current.
    index.yaml is derived; do not edit it by hand (it is overwritten each run).

    Example:
        python scripts/audit.py registry update
    """
    names = discover_repos()
    states = [load_state(n) for n in names if load_state(n) is not None]
    regenerate_index(states)
    click.echo(f"ecosystem/index.yaml regenerated ({len(states)} repos).")


@cli.command("health")
@click.option("--parallel/--no-parallel", "parallel", default=False, show_default=True,
              help="Run the self-audit checks on a thread pool. DEFAULT SERIAL: this flag "
                   "exists so the speedup can be measured and opted into; flipping the "
                   "audit-health hook's default is a separate ruling ([#533] leg 2).")
@click.option("--workers", type=click.IntRange(min=1), default=None,
              help=f"Worker threads when --parallel (default: min({_PARALLEL_MAX_WORKERS}, "
                   "number of checks)). Ignored when serial.")
@click.option("--telemetry/--no-telemetry", "telemetry", default=None,
              help="Emit one [#529] check_run event per check into the SQLite store. "
                   f"DEFAULT OFF (${TELEMETRY_ENV}=1 turns it on where there is no flag to "
                   "pass, e.g. the audit-health pre-commit hook; an explicit flag beats the "
                   "env var). This flag exists so emission can be measured and opted into; "
                   "flipping the audit-health hook's default is a separate ruling.")
def cmd_health(parallel: bool, workers: int | None, telemetry: bool | None) -> None:
    """Quick TTY status: operational deps + .dev-knowledge self-conformance. No file writes.

    Two parts: (1) operational preflight — click/pyyaml importable, ecosystem/ exists,
    >=1 repo registered; (2) self-audit — the full ALL_CHECKS suite against
    .dev-knowledge itself. A self-audit `fail` (or a failed preflight) prints
    "health: DEGRADED" and exits 1; a `warn` prints but exits 0.

    This is the `audit-health` pre-commit gate ([#69]): a FAIL blocks the commit,
    a WARN only informs. Enforcement is self-only — `health` never reaches child repos.

    Example:
        python scripts/audit.py health
    """
    checks: list[tuple[str, bool, str]] = []

    # (a) click importable
    try:
        import click as _c  # noqa: F401
        checks.append(("click importable", True, ""))
    except ImportError as e:
        checks.append(("click importable", False, str(e)))

    # (b) pyyaml importable
    try:
        import yaml as _y  # noqa: F401
        checks.append(("pyyaml importable", True, ""))
    except ImportError as e:
        checks.append(("pyyaml importable", False, str(e)))

    # (c) ecosystem/ directory exists
    eco_exists = ECOSYSTEM_DIR.exists()
    checks.append(("ecosystem/ exists", eco_exists, "" if eco_exists else str(ECOSYSTEM_DIR)))

    # (d) at least one repo registered
    repos = discover_repos()
    checks.append(("repos registered", len(repos) > 0, f"{repos}" if repos else "none"))

    operational_ok = all(ok for _, ok, _ in checks)

    # Self-conformance against .dev-knowledge, AT THE COMMIT TIER ([#597]). This is the only
    # caller that passes a tier: `ship-gate`, `run` and `repo` run every check. There is no
    # try/finally here any more and that absence is the point — the tier is an argument, not a
    # module global to set and restore, so there is no state a raising check could leave behind.
    self_findings = run_checks(Path(_REPO_ROOT), parallel=parallel, workers=workers,
                               telemetry=telemetry_enabled(telemetry), tier=TIER_COMMIT)
    self_fail = any(f.status == "fail" for f in self_findings)

    click.echo("operational:")
    for label, ok, detail in checks:
        marker = "[OK]" if ok else "[!!]"
        suffix = f"  ({detail})" if detail else ""
        click.echo(f"  {marker} {label}{suffix}")

    passed = sum(1 for f in self_findings if f.status == "pass")
    click.echo(f"self-audit (.dev-knowledge) - {passed}/{len(self_findings)} pass:")
    _marker = {"pass": "[OK]", "warn": "[~~]", "fail": "[!!]", "unavailable": "[??]", "n/a": "[--]"}
    for f in self_findings:
        click.echo(f"  {_marker.get(f.status, '[??]')} {f.check_name}: {f.evidence}")

    if operational_ok and not self_fail:
        click.echo("health: OK")
    else:
        click.echo("health: DEGRADED", err=True)
        sys.exit(1)


def _load_dispositions() -> list[dict]:
    """Read the #147 known-WARN disposition register. Fail-soft: a missing or malformed
    register degrades to [] — every WARN then counts as undispositioned (stricter), and
    the gate never wedges. Read-only."""
    try:
        data = yaml.safe_load(Path(DISPOSITION_REGISTER).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return []
    if not isinstance(data, dict):
        return []
    items = data.get("dispositions")
    if not isinstance(items, list):  # HIGH (Codex): a non-list scalar must degrade, not raise
        return []
    return [d for d in items if isinstance(d, dict)]


def _match_disposition(finding: "Finding", dispositions: list[dict]) -> Optional[dict]:
    """Return the register entry that dispositions this WARN finding, or None.

    A match requires `organ == finding.check_name` AND the entry's `match` substring to
    appear in `finding.evidence` — keying on the specific benign signature (e.g. the
    commit sha), NOT a bare id, so a DIFFERENT future drift on the same id re-surfaces.
    """
    for d in dispositions:
        token = d.get("match")
        if d.get("organ") == finding.check_name and token and str(token) in finding.evidence:
            return d
    return None


# [#337] the INFORMATIONAL fleet-parity subprocess surface (`_fleet_parity_surface` /
# `_FLEET_PARITY_SCRIPT`) was RETIRED when fleet_parity became a blocking ALL_CHECKS member
# (`check_fleet_parity` above) -- the gate now reads the in-process walk, not an echoed subprocess.


@cli.command("ship-gate")
def cmd_ship_gate() -> None:
    """Pre-ship verification-organ gate (#147): make "Definition of shipped" point (6)
    enforceable at /ship time. No file writes (read-only, Layer-2).

    Runs the full ALL_CHECKS self-audit against .dev-knowledge and emits ONE ship verdict
    by reading Finding.status DIRECTLY — never exit codes: the awareness organs
    (git_backlog_drift #90a, doc_claims #89, canonical_freshness A1) exit 0 even on drift,
    so a gate keyed on exit codes would be vacuous (F1). Verdict / exit:
      - any Finding.status == "fail"                         -> RED, exit 1
      - any "warn" NOT dispositioned by the register         -> RED, exit 1
      - a "warn" matched by a register entry (organ == check_name AND the entry's `match`
        substring in the evidence) is DISPOSITIONED           -> does not block
      - else                                                 -> GREEN, exit 0
    A register entry that matched NO live WARN is surfaced as `[stale]` (ADR-75 decoration
    rule — awareness, does NOT block); the register may not silently rot.

    Disposition contract: a register entry suppresses a WHOLE Finding (its `match` is a
    substring of the evidence). So an aggregate awareness organ MUST emit one Finding per
    concern, or one matched token would suppress unrelated drift bundled in the same
    finding (Codex CRITICAL 2026-06-10). `git_backlog_drift` emits one Finding per drifted
    id for exactly this reason; any future dispositioned organ must do likewise.

    Seam vs the pre-commit `audit-health` gate (they reuse ALL_CHECKS but do NOT
    double-run vacuously — different moment, different posture):
      - `audit-health` gates each COMMIT: FAIL-only (WARNs pass), and since [#597] it runs
        only the COMMIT TIER (`run_checks(..., tier=TIER_COMMIT)`). A ship-tier check appears
        in its report as an `n/a` naming the deferral, never as a silent omission.
      - `ship-gate` gates the feature ARC at /ship: FAIL **and** new/undispositioned WARN
        block, and it passes NO tier — every check runs, claim-3 included. This is where the
        WARN-only organs the commit tier defers actually have teeth, which is the whole reason
        deferring them costs no enforcement.

    Hub-only organs no-op on child repos; the /ship wiring is hub-guarded. Register:
    ecosystem/disposition-register.yaml (fail-soft if absent — stricter, never wedged).

    Example:
        python scripts/audit.py ship-gate
    """
    findings: list[Finding] = []
    # SHIP-TIME = FULL VERIFICATION. No `tier=` is passed, so every check runs — the [#597]
    # tiering can only ever move work from the commit gate to HERE, never off the gate set, and
    # this line is what makes that true. Passing `tier=TIER_SHIP` would be equivalent
    # (`runs_at_tier` treats it as run-everything) but would read as a filter; the absence of an
    # argument is the honest shape.
    #
    # [#529]: this gate emits NO telemetry, and that is a decision rather than an omission.
    # "No file writes (read-only, Layer-2)" above is the ship-gate's contract, and a gate
    # that quietly gained a side-effect would be a different organ. It therefore does NOT
    # consult `telemetry_enabled()` — the ambient env switch turns the audit-health mesh on
    # without turning this one on, and `tests/test_ship_gate.py::test_ship_gate_is_readonly`
    # asserts exactly that with the switch forced ON.
    findings = run_checks(Path(_REPO_ROOT))

    dispositions = _load_dispositions()
    fails = [f for f in findings if f.status == "fail"]
    undispositioned: list[Finding] = []
    dispositioned: list[tuple[Finding, dict]] = []
    matched_ids: set[str] = set()
    for f in findings:
        if f.status != "warn":
            continue
        entry = _match_disposition(f, dispositions)
        if entry is None:
            undispositioned.append(f)
        else:
            dispositioned.append((f, entry))
            matched_ids.add(str(entry.get("id")))
    stale = [d for d in dispositions if str(d.get("id")) not in matched_ids]

    _marker = {"pass": "[OK]", "warn": "[~~]", "fail": "[!!]", "unavailable": "[??]", "n/a": "[--]"}
    click.echo("ship-gate (#147) — verification organs vs THIS arc:")
    for f in findings:
        click.echo(f"  {_marker.get(f.status, '[??]')} {f.check_name}: {f.evidence}")
    for f, e in dispositioned:
        click.echo(f"  [disp] {f.check_name}: WARN dispositioned by {e.get('id')} "
                   f"(ref {e.get('ref')}) — expected, not blocking")
    for d in stale:
        click.echo(f"  [stale] disposition {d.get('id')} matched no live WARN — "
                   f"review/remove (ADR-75 decoration rule)")

    # [#337] fleet_parity is now a blocking ALL_CHECKS member (check_fleet_parity); its
    # Findings render inline in the loop above and gate via the normal fails/undispositioned
    # path below -- no separate informational echo.
    if fails or undispositioned:
        reasons = []
        if fails:
            reasons.append(f"{len(fails)} hard-fail organ(s)")
        if undispositioned:
            reasons.append(f"{len(undispositioned)} new/undispositioned WARN(s)")
        click.echo(f"ship-gate: RED — not shipped-ready ({'; '.join(reasons)})", err=True)
        sys.exit(1)
    click.echo("ship-gate: GREEN — verification organs green against this arc "
               f"({len(dispositioned)} WARN dispositioned)")


@cli.command("handback")
@click.argument("line")
def cmd_handback(line: str) -> None:
    """Verdict on ONE 027 HANDBACK line — exit 0 merges, exit 1 refuses.

    `/lane-integrate` runs this per queue item BEFORE the merge, which is what makes D-1's
    "the integrator refuses a `review=NONE` code branch" a refusal rather than a reminder.
    It reads a line, not the repo: no git, no network, no state — so it is the same verdict
    from a lane, the primary checkout, or a paste.

    Example:
        python scripts/audit.py handback "HANDBACK worktree-lane-u-000-x @ 1a2b3c4d code review=codex HIGH:0 MED:1 LOW:2"
    """
    ok, msg = review_handback_verdict(line)
    click.echo(msg)
    sys.exit(0 if ok else 1)


@cli.command("checks")
def cmd_checks() -> None:
    """List the registered audit checks (sourced from ALL_CHECKS — the same list
    that `health` and `run` execute).

    Authoritative, drift-proof inventory: the count and numbering come from
    ALL_CHECKS at runtime, so this listing cannot diverge from what actually runs.
    Each line shows the check's name (== its Finding.check_name) and the first line
    of its docstring.

    Example:
        python scripts/audit.py checks
    """
    click.echo(f"{len(ALL_CHECKS)} registered checks (ALL_CHECKS — run by `health` and `run`):")
    for i, check in enumerate(ALL_CHECKS, start=1):
        name = check.__name__.removeprefix("check_")  # == Finding.check_name
        first = (check.__doc__ or "").strip().splitlines()
        summary = first[0].strip() if first else ""
        click.echo(f"  {i:>2}. {name} — {summary}")


@cli.command("doc-freshness")
def cmd_doc_freshness() -> None:
    """Render the living-doc doctrine table -- declared vs DERIVED freshness, per doc.

    `[#614]` HY-1. The on-demand half of the derived-freshness leg: `audit.py health` reports
    the CLASSES (gated-and-stale / ungated-and-stale / unstamped), this prints every row with
    its live version, its declared date and surface, and the date of its last CONTENT commit.

    FULLY REFINED, unlike the gate leg. The gate spends CONTENT-vs-TOUCH classification only
    where it can change a verdict, because a `git show` per commit costs ~0.19 s; here the ~7 s
    a complete walk costs is free, so every row is refined and none is labelled `unrefined`.

    REFUSES ON A SHALLOW CLONE rather than printing floors as facts -- exit 1 with the reason.

    Read-only. It computes freshness; it never re-stamps a file (Layer 2 never executes). A row
    reading stale is resolved by a GENUINE end-to-end re-read and an honest stamp, never by a
    date typed to green the table.

    Example:
        uv run --locked python scripts/audit.py doc-freshness
    """
    try:
        table = doctrine_table(Path(_REPO_ROOT))
    except DerivationRefused as exc:
        raise SystemExit(f"doc-freshness REFUSED: {exc}")
    except DerivationUnavailable as exc:
        raise SystemExit(f"doc-freshness unavailable: {exc}")
    # `console_safe`-style guard for the same reason `governance-health` states: these rows
    # quote arbitrary doc paths and versions, and `click.echo` raises UnicodeEncodeError on a
    # Windows cp1252 console for anything outside cp1252.
    click.echo(table.encode("ascii", "replace").decode("ascii"))


@cli.command("governance-health")
@click.option("--telemetry/--no-telemetry", "telemetry", default=None,
              help="Append one [#529] check_run record for this run into the SQLite store, so "
                   f"the numbers become a time series. DEFAULT OFF (${TELEMETRY_ENV}=1 turns "
                   "it on where there is no flag to pass; an explicit flag beats the env var).")
def cmd_governance_health(telemetry: bool | None) -> None:
    """Render FM-4's FUNNEL HEALTH numbers on demand, plus what each closed row bought.

    Two halves, with different owners, and the split is the point:

      * the four FUNNEL HEALTH fields FM-4 derives are IMPORTED from FM-4's emitter and
        never recomputed here. When that emitter is absent they render `unavailable` with
        the resolution report attached — a true answer, where a locally-computed number
        that happened to look right would silently break the one-truth contract;
      * `rows closed this window` and `value evidence attached` are this command's own,
        exported for FM-4 to import for the same reason.

    The value section quotes close packets VERBATIM with a `file:line` locator for every
    line, and prints `no value evidence` for a row whose packets say nothing. Nothing is
    summarised, so no benefit can be asserted that a reader cannot open and check.

    Read-only. `--telemetry` appends ONE record to the existing `[#529]` store
    (logs/TELEMETRY.db); it creates no second store and writes nothing else.

    Example:
        uv run --locked python scripts/audit.py governance-health
    """
    report = _gh.build_report(Path(_REPO_ROOT))
    # console_safe, not a bare echo: this output quotes arbitrary close-packet prose, and
    # click.echo raises UnicodeEncodeError on a Windows cp1252 console for anything outside
    # cp1252 — the trap the "ASCII arrow" comment on check_doc_code_edge records.
    click.echo(_gh.console_safe(_gh.render(report)))
    if telemetry_enabled(telemetry):
        row_id = _gh.emit(report, db_path=_telemetry_db_path(), repo_path=Path(_REPO_ROOT))
        click.echo(f"telemetry: appended row {row_id} to {_telemetry_db_path()}"
                   if row_id is not None else "telemetry: not appended (store refused)",
                   err=True)


if __name__ == "__main__":
    cli()
