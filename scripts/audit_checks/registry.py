"""The ordered check registry for the decomposed `audit.py` ([#533]).

`CHECK_ORDER` is the canonical order of `audit.ALL_CHECKS` — **order is load-bearing**: it is
the order findings are emitted in, and therefore part of the byte-identical output contract the
git hooks depend on. `EXTRACTED_CHECKS` is the subset that now lives in its own module, listed
in CHECK_ORDER-relative order; the rest are still defined in the `audit.py` facade and are
marked `# facade` below.

WHY THE SPLIT IS WHERE IT IS — the criterion is mechanical, not editorial. A check can be moved
only if nothing in its transitive dependency closure is monkeypatched onto the `audit` module by
a test. `tests/` patches these names on `audit`:

    ALL_CHECKS  AUDITS_DIR  DEPLOYED_VERSIONS_REGISTRY  DISPOSITION_REGISTER  ECOSYSTEM_DIR
    _GATE_MODE  _REPO_ROOT  _git  _git_last_commit_date  _git_linked_worktrees
    _git_registered_worktrees  _git_repo_root_name  _git_stash_entries
    _index_worktree_divergence  _is_hub  _ref_baseline_state

A check that read any of them through its own module namespace would keep reading the ORIGINAL
value while the test rewrote `audit`'s — the seam detaches SILENTLY, which is worse than a
failure, because the check would still pass while testing nothing. `_is_hub` (itself a reader of
`_REPO_ROOT`) alone accounts for 19 of the 25 held-back checks. `tests/test_audit.py` is
read-only to [#533], so re-pointing those seams is not this change's to make.

`check_handoff_probes` is held back for a second, independent reason: it reaches `_gitenv`,
which `audit.py` loads BY PATH via `Path(__file__).resolve().with_name("gitenv.py")`. That
expression is position-dependent — from inside this package it would resolve to
`scripts/audit_checks/gitenv.py`, which does not exist — so relocating it is not a pure move.

HONEST LIMIT: nothing currently asserts that `CHECK_ORDER` still agrees with
`audit.ALL_CHECKS`. The guard belongs in `tests/`, which this change may not touch, so the
agreement is maintained by hand until that test is written. Stated rather than papered over.

This package is a PEP 420 namespace package (**no `__init__.py`**, deliberately), matching
`scripts/` itself, which has none either. `scripts/codemap/` and `scripts/toc/` DO carry
`__init__.py` and are therefore exactly the two entries in the generated ARCHITECTURE.md
codemap; adding a third would change that generated block, and ARCHITECTURE.md is outside this
change's owned files.
"""

from __future__ import annotations

from ._common import (
    _BUNDLE_EXCLUDE_DIRS,
    _NA_NOT_APPLICABLE,
    _NA_REASON_RE,
    _NA_REASONS,
    _NA_SUBJECT_ABSENT,
    _na,
    _na_reason,
    Finding,
)
from .check_adr38_baseline import check_adr38_baseline
from .check_adr_status_grammar import check_adr_status_grammar
from .check_amendment_coherence import (
    _COUPLED_VERSION_SETS,
    _norm_version,
    check_amendment_coherence,
    CoupledSet,
)
from .check_boot_byte_budget import _assemble_paste, check_boot_byte_budget
from .check_canonical_md_visibility import (
    _CANONICAL_ALL,
    _CANONICAL_MANDATORY,
    check_canonical_md_visibility,
)
from .check_canonical_structure import (
    _CANONICAL_SPINE,
    _heading_present,
    check_canonical_structure,
)
from .check_claude_md import check_claude_md
from .check_consumer_at_landing import check_consumer_at_landing
from .check_dispatch_drift import check_dispatch_drift
from .check_dot_prefix_discipline import (
    _CONFIG_SUFFIXES,
    _DOT_PREFIX_EXCEPTIONS,
    check_dot_prefix_discipline,
)
from .check_floor_integrity import (
    _FLOOR_F5,
    _FLOOR_MD_REF_RE,
    _floor_sha256,
    check_floor_integrity,
)
from .check_handoff_bundle_structure import (
    _BUNDLE_BUDGETS,
    _BUNDLE_REQUIRED_FILES,
    _BUNDLE_STAMP_RE,
    check_handoff_bundle_structure,
)
from .check_handoff_version_stamp import (
    _STAMP_FILES,
    _STAMP_RE,
    check_handoff_version_stamp,
)
from .check_proof_layer import check_proof_layer
from .check_reconciled_versions import _vr, check_reconciled_versions
from .check_residual_completeness import _vrc, check_residual_completeness
from .check_routine_consumers import (
    _ROUTINE_ANYFIELD_RE,
    _ROUTINE_FENCE_RE,
    _ROUTINE_FIELD_RE,
    _ROUTINE_INVISIBLE,
    _ROUTINE_LOOKALIKE_RE,
    _ROUTINE_MARKER_RE,
    _ROUTINE_REQUIRED,
    _ROUTINE_SENTINELS,
    _ROUTINE_TASK_RE,
    _ROUTINE_TICK_RUN_RE,
    _routine_code_spans,
    _routine_in_code,
    _routine_value_is_named,
    check_routine_consumers,
)
from .check_safe_removal import _sr, check_safe_removal
from .check_substrate_declaration import check_substrate_declaration
from .check_vision_md import check_vision_md
from .check_workspace_settings import (
    _strip_jsonc,
    _WORKSPACE_REQUIRED_SETTINGS,
    check_workspace_settings,
)

# The canonical order of `audit.ALL_CHECKS`, by function name. 46 entries; the count is pinned
# in ARCHITECTURE.md, .claude/commands/{handoff-verify,preflight}.md, deploy/release_lint.py and
# the test suite, so it does not move without those moving too. The inline notes are carried
# over from the ALL_CHECKS literal they came from.
CHECK_ORDER: tuple[str, ...] = (
    "check_vision_md",
    "check_adr38_baseline",
    "check_claude_md",
    "check_dot_prefix_discipline",
    "check_canonical_md_visibility",
    "check_workspace_settings",
    # check_mermaid_theme_directive retired 2026-07-05 (ADR-51 amendment — LLM-first)
    "check_handoff_bundle_structure",
    "check_canonical_freshness",          # facade — _git_last_commit_date seam
    "check_generated_artifact_freshness",  # facade — _gaf_git_last_commit_date seam
    "check_no_sibling_orphans",           # facade — _git_registered_worktrees seam
    "check_stale_worktrees",              # facade — _git_linked_worktrees/_git_stash_entries seams
    "check_canonical_structure",
    "check_handoff_version_stamp",
    "check_amendment_coherence",
    "check_floor_integrity",
    "check_hooks_armed",                  # facade — _is_hub/_REPO_ROOT seam
    "check_git_backlog_drift",            # facade — _is_hub/_REPO_ROOT seam
    "check_doc_claims",                   # facade — ALL_CHECKS/_GATE_MODE/_is_hub seams
    "check_no_ff_merges",                 # facade — _is_hub/_REPO_ROOT seam
    "check_handoff_probes",               # facade — _gitenv path-load
    "check_supplement_folded",            # facade — R4 (handoff census 2026-08-26 b6)
    "check_dispatch_verb_agreement",      # facade — R5 (STANDING_RULINGS §V's owed organ)
    "check_reconciled_versions",
    "check_doc_rot",                      # facade — _is_hub/_REPO_ROOT seam
    "check_doc_structure",                # facade — _is_hub/_REPO_ROOT seam
    "check_doc_code_edge",                # facade — _is_hub/_REPO_ROOT seam
    "check_safe_removal",
    "check_residual_completeness",
    "check_deployed_methodology_version",  # facade — DEPLOYED_VERSIONS_REGISTRY seam
    "check_enforcement_coverage",         # facade — _is_hub/_REPO_ROOT seam
    "check_undeclared_edges",             # facade — _is_hub/_REPO_ROOT seam
    "check_doc_code_coverage_drift",      # facade — ALL_CHECKS/_is_hub seams
    "check_import_edges",                 # facade — STANDING_RULINGS N-1 site
    "check_fleet_parity",                 # facade — _is_hub/_REPO_ROOT seam
    "check_routine_consumers",
    "check_silent_rule_ratchet",          # facade — _ref_baseline_state/_git/_is_hub seams
    "check_task_tree_coherence",          # facade — _index_worktree_divergence/_is_hub seams
    "check_intake_tree_coherence",        # facade — _index_worktree_divergence/_is_hub seams
    "check_boot_byte_budget",
    "check_fleet_audit_replication",      # facade — _is_hub/_REPO_ROOT seam
    "check_membership_agreement",         # facade — _is_hub/_REPO_ROOT seam
    "check_journal_spine_anchor",         # facade — _is_hub/_REPO_ROOT seam
    "check_journal_day_letters",          # facade — _is_hub/_REPO_ROOT seam
    "check_preflight_backlog_ids",        # facade — _is_hub/_REPO_ROOT seam
    "check_review_artifact_coverage",     # facade — _is_hub/_REPO_ROOT seam
    "check_landing_predicate",            # facade — DISPOSITION_REGISTER/_is_hub seams
    "check_adr_status_grammar",           # [#242] ADR status grammar/enum + README coherence
    "check_funnel_coverage",              # facade — _is_hub seam; detector in funnel_coverage.py
    "check_substrate_declaration",        # [#591] substrate validator layer 2 — thin adapter
    "check_dispatch_drift",               # [#592] Ch8 literal commands vs the machine
    "check_consumer_at_landing",          # [#595] docs/audits consumer declaration + ratchet
    "check_proof_layer",                  # [#596] family-3 environment-conditional guards
)

# The extracted subset, in CHECK_ORDER-relative order.
EXTRACTED_CHECKS = (
    check_vision_md,
    check_adr38_baseline,
    check_claude_md,
    check_dot_prefix_discipline,
    check_canonical_md_visibility,
    check_workspace_settings,
    check_handoff_bundle_structure,
    check_canonical_structure,
    check_handoff_version_stamp,
    check_amendment_coherence,
    check_floor_integrity,
    check_reconciled_versions,
    check_safe_removal,
    check_residual_completeness,
    check_routine_consumers,
    check_boot_byte_budget,
    check_adr_status_grammar,
    check_substrate_declaration,
    check_dispatch_drift,
    check_consumer_at_landing,
    check_proof_layer,
)

# The flat surface `audit.py` re-exports. Names beyond the check functions appear here because a
# live consumer reads them off the `audit` module: `tests/test_audit.py` uses `aud._strip_jsonc`,
# `aud._CANONICAL_MANDATORY` and `aud.CoupledSet`, `scripts/boundary_report.py` uses
# `audit._CANONICAL_SPINE` and `audit._na`. Re-exporting keeps those reads working AND keeps them
# pointing at the same objects, which is the whole facade-compatibility contract.
__all__ = [
    "CHECK_ORDER",
    "CoupledSet",
    "EXTRACTED_CHECKS",
    "Finding",
    "_BUNDLE_BUDGETS",
    "_BUNDLE_EXCLUDE_DIRS",
    "_BUNDLE_REQUIRED_FILES",
    "_BUNDLE_STAMP_RE",
    "_CANONICAL_ALL",
    "_CANONICAL_MANDATORY",
    "_CANONICAL_SPINE",
    "_CONFIG_SUFFIXES",
    "_COUPLED_VERSION_SETS",
    "_DOT_PREFIX_EXCEPTIONS",
    "_FLOOR_F5",
    "_FLOOR_MD_REF_RE",
    "_NA_NOT_APPLICABLE",
    "_NA_REASONS",
    "_NA_REASON_RE",
    "_NA_SUBJECT_ABSENT",
    "_ROUTINE_ANYFIELD_RE",
    "_ROUTINE_FENCE_RE",
    "_ROUTINE_FIELD_RE",
    "_ROUTINE_INVISIBLE",
    "_ROUTINE_LOOKALIKE_RE",
    "_ROUTINE_MARKER_RE",
    "_ROUTINE_REQUIRED",
    "_ROUTINE_SENTINELS",
    "_ROUTINE_TASK_RE",
    "_ROUTINE_TICK_RUN_RE",
    "_STAMP_FILES",
    "_STAMP_RE",
    "_WORKSPACE_REQUIRED_SETTINGS",
    "_assemble_paste",
    "_floor_sha256",
    "_heading_present",
    "_na",
    "_na_reason",
    "_norm_version",
    "_routine_code_spans",
    "_routine_in_code",
    "_routine_value_is_named",
    "_sr",
    "_strip_jsonc",
    "_vr",
    "_vrc",
    "check_adr38_baseline",
    "check_adr_status_grammar",
    "check_amendment_coherence",
    "check_boot_byte_budget",
    "check_canonical_md_visibility",
    "check_canonical_structure",
    "check_claude_md",
    "check_consumer_at_landing",
    "check_dispatch_drift",
    "check_dot_prefix_discipline",
    "check_floor_integrity",
    "check_handoff_bundle_structure",
    "check_handoff_version_stamp",
    "check_proof_layer",
    "check_reconciled_versions",
    "check_residual_completeness",
    "check_routine_consumers",
    "check_safe_removal",
    "check_substrate_declaration",
    "check_vision_md",
    "check_workspace_settings",
]
