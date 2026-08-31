#!/usr/bin/env python
"""canonical_docs.py — the canonical-doc-name registry.

ONE table for the canonical living-document FILENAMES that ten machine constants across the
gate mesh were each hardcoding independently. Cut from
`docs/audits/2026-08-21-fresh-eyes-cloud-r2-universalization.md` §1.5 GO-(b).

**The decision this table was built to hold has now been made, and it is made HERE.** The
module bought ONE place for a canonical-filename decision instead of ten. `[#614]`'s frozen
arc spends that: `VISION.md` is **RETIRED** from the fleet-wide mandatory set, and
`README.md` is the hub's MUST front door.

**ADR-114 is Accepted (2026-08-29, AMENDMENT 1): `VISION.md` is superseded by a recreated
root `README.md`.** The hub's front door moved in `[#614]` lane-b — `README.md` carries the
live-normative content and `VISION.md` is retained, marked superseded, keeping its `## H2`
spine. This module is that arc's registry half.

**Retirement is a SUBTRACTION, and the direction is what makes it fleet-safe.** `VISION`
leaves `CANONICAL_MANDATORY` — and so leaves `ADR38_BASELINE_REQUIRED` and every consumer's
canonical-set check — into `CANONICAL_RETIRED`. Removing a requirement cannot RED a member
that still carries the file, so the subtraction turns none of the nine RED; it turns one
long-standing latent divergence GREEN, because `terminal-setup` is a declared ADR-104 member
that has never had a `VISION.md` (`ecosystem/deployed-versions.yaml` records it:
*"2 commits, no VISION.md, no CLAUDE.md, no deploy record"*).

**The opposite act is the one that would break six members**, which is why it is NOT taken
here: promoting `README` INTO `CANONICAL_MANDATORY` enrols it in `ADR38_BASELINE_REQUIRED`
and in every consumer's canonical-set check, while only two of the eight ADR-104 children
carry a root `README.md` — re-measured 2026-08-31 on the operator's disk: `terminal-setup`
and `win-tooling`, unchanged from the 2026-08-29 measurement. So `README` is promoted into
`CANONICAL_HUB_MANDATORY` instead: MUST at the hub, unchanged for the fleet. The
consumer-side promotion travels by the deploy carrier declared in
`deploy/manifest-v1.4.0.yaml`, repo by repo, in CUT-1's ruled migration order
`hub -> monorepo -> ai-council -> win-tooling`.

**`VISION.md` itself is untouched — byte-identical, still tracked at the root.** It is
retired from a mandatory ROLE, not removed from the tree. That is deliberate and it is
load-bearing: `gen_handoff._vision_extract` still reads its `## Vision` body, and its
`CANONICAL_SPINE` entry still shapes the eight fleet copies that do exist, so both are left
in place below rather than moved with the tier.

The ten machine constants this serves, by the names R2 §1.2 uses:

    check_vision_md · check_adr38_baseline · check_canonical_md_visibility
    check_canonical_structure · canonical_freshness_gate · validate_doc_rot
    validate_doc_structure · validate_hermetization · session_end_backpressure · gen_handoff

**Two of the ten are deploy-carried and import this module SOFTLY.**
`scripts/canonical_freshness_gate.py` and `scripts/session_end_backpressure.py` are
byte-copied into consumer repos as standalone single files by `deploy/carrier_mesh.py`
(`FRESHNESS_GATE_REL`, and the mesh's `session_end_backpressure` component). A hard import
of a hub-local module would break both on the next deploy. They therefore guard the import
and fall back to their own literals, and `tests/test_canonical_docs.py` asserts each
fallback equals the value here — so drift is caught at the hub, where the two files are
authored, rather than at a consumer, where it would be silent.

An eleventh site, `.claude/workflows/conformance-hub.js` (R2 seam S11), is a JavaScript
string list and cannot import Python at all. It is held in agreement by the same test.

Read-only. Constants and derived tuples; no I/O.
"""

from __future__ import annotations

# --- the names themselves ---------------------------------------------------------------
# UPPERCASE.md, the ADR-101 §1 closed class. Referenced by symbol from here on.
VISION = "VISION.md"
ARCHITECTURE = "ARCHITECTURE.md"
CLAUDE = "CLAUDE.md"
BACKLOG = "BACKLOG.md"
CONTRIBUTING = "CONTRIBUTING.md"
JOURNAL = "JOURNAL.md"
LESSONS = "LESSONS.md"

# Canonical names that are NOT members of the mandatory root set but travel with them in one
# or more of the constants below (optional-at-root, or protocols-resident). README LEFT this
# tuple in [#614] lane-a: it is now MUST at the hub via CANONICAL_HUB_MANDATORY, and still
# NOT in CANONICAL_MANDATORY -- see the module docstring for why the direction matters.
ENVIRONMENT = "ENVIRONMENT.md"
ESSENTIALS = "ESSENTIALS.md"
PLAYBOOK = "PLAYBOOK.md"
TOKEN_LOG = "TOKEN-LOG.md"
README = "README.md"

# Repo-relative paths for the two protocols-resident docs that the freshness / structure
# sets address by path rather than by bare name.
ESSENTIALS_PATH = "protocols/ESSENTIALS.md"
PLAYBOOK_PATH = "protocols/PLAYBOOK.md"
HANDOFF_PROCESS_PATH = "protocols/HANDOFF_PROCESS.md"
AI_COUNCIL_PROCESS_PATH = "protocols/AI_COUNCIL_PROCESS.md"
HANDOFFS_README_PATH = "docs/handoffs/README.md"


# --- the derived sets the ten constants consume -------------------------------------------
# ADR-38 A6 (2026-06-02) made this the SEVEN-file canonical set, mandatory for every repo.
# ADR-114 (Accepted 2026-08-29, AMENDMENT 1), executed by [#614] lane-a, retires VISION from
# it -- SIX now. Membership here is fleet-wide and is read by ADR38_BASELINE_REQUIRED,
# check_canonical_md_visibility and validate_hermetization.SANCTIONED_TIER1_FILES, so a name
# added here is a name every one of the nine ADR-104 members must carry.
CANONICAL_MANDATORY: tuple[str, ...] = (
    ARCHITECTURE, CLAUDE, BACKLOG, CONTRIBUTING, JOURNAL, LESSONS,
)

# RETIRED from the mandatory set, still tracked in the tree and still name-checked. A retired
# name is NOT a deleted one: it keeps its casing check, keeps its CANONICAL_SPINE entry, and
# keeps whatever generator reads it -- it simply stops being a presence REQUIREMENT. This is
# the tier VISION.md moved into; it is deliberately a tuple so a second retirement appends
# rather than rewrites.
CANONICAL_RETIRED: tuple[str, ...] = (VISION,)

# MUST at the HUB only. The seam that lets a canonical promotion land at the hub without
# enrolling the eight children in it -- README.md's case, and the reason ADR-114's fleet-wide
# filename migration can be sequenced (option (C)) rather than taken in one commit. NOTHING
# fleet-wide reads this tuple; that is the point.
CANONICAL_HUB_MANDATORY: tuple[str, ...] = CANONICAL_MANDATORY + (README,)

# Canonical names whose CASING is checked when present (mandatory + retired + hub-mandatory +
# optional + .dev-knowledge-only). Presence is required only for CANONICAL_MANDATORY. VISION
# and README both remain members: retirement and hub-scoping change the presence TIER, never
# the name-check.
CANONICAL_OPTIONAL: tuple[str, ...] = (ENVIRONMENT, ESSENTIALS, PLAYBOOK, TOKEN_LOG)
CANONICAL_ALL: tuple[str, ...] = (
    CANONICAL_MANDATORY + CANONICAL_RETIRED + (README,) + CANONICAL_OPTIONAL
)

# The ADR-38 governance baseline set: the mandatory seven minus CLAUDE.md, which
# check_claude_md owns and check_adr38_baseline deliberately does not duplicate.
ADR38_BASELINE_REQUIRED: tuple[str, ...] = tuple(n for n in CANONICAL_MANDATORY if n != CLAUDE)

# The living docs carrying a `last_reviewed` stamp (the A1/A2 freshness cadence).
FRESHNESS_FILES: tuple[str, ...] = (
    VISION, ARCHITECTURE, CLAUDE, CONTRIBUTING, HANDOFFS_README_PATH, ESSENTIALS_PATH,
)

# The living docs scanned for Section-history / changelog accretion.
SECTION_HISTORY_DOCS: tuple[str, ...] = (
    CLAUDE, ARCHITECTURE, VISION, CONTRIBUTING,
    PLAYBOOK_PATH, HANDOFF_PROCESS_PATH, AI_COUNCIL_PROCESS_PATH, ESSENTIALS_PATH,
)

# The living docs scanned for structural shape (mirrors SECTION_HISTORY_DOCS, different order
# on disk historically; the membership is what the gate reads).
STRUCTURE_DOCS: tuple[str, ...] = (
    CLAUDE, ARCHITECTURE, VISION, CONTRIBUTING,
    PLAYBOOK_PATH, ESSENTIALS_PATH, HANDOFF_PROCESS_PATH, AI_COUNCIL_PROCESS_PATH,
)

# The four root living docs the session-end backpressure hook treats as canonical.
BACKPRESSURE_CANON: tuple[str, ...] = (VISION, ARCHITECTURE, CLAUDE, CONTRIBUTING)

# The living-doc scan list the conformance-hub V2 verifier reads (R2 seam S11). Held here so
# the JS literal has a Python-side counterpart to be checked against.
CONFORMANCE_V2_SCAN: tuple[str, ...] = (
    VISION, ARCHITECTURE, CLAUDE, CONTRIBUTING, ESSENTIALS_PATH,
)

# The `## H2` spine each canonical file carries (ADR-38 A6). Keyed by the names above so a
# filename decision moves the key with the value.
#
# **`README` is deliberately ABSENT from this table, and its absence is MEASURED, not an
# oversight.** README.md already carries all five of VISION's H2s, so adding the key would
# assert something already true at the hub -- but `release_lint` C7 mirrors this dict into
# EVERY released manifest's `doc_shapes` block and lints the live constants against v1.1.0
# and v1.2.0 as well as the current release. Adding a key here therefore REDs C7 against
# manifests that are released artifacts, and the sanctioned answer to that is a manifest
# VERSION BUMP, not a retro-edit of a shipped spec. So the spine re-point rides ADR-114
# option (C)'s sequenced migration together with the version bump it requires; the TIER
# decision above is independent of it and lands here alone.
#
# VISION keeps its entry: it is retired from the mandatory set, not from the tree, and the
# eight fleet copies that do exist are still shape-checked by it.
CANONICAL_SPINE: dict[str, list[str]] = {
    VISION: ["## Vision", "## Scope", "## Values", "## Lifecycle", "## References"],
    ARCHITECTURE: ["## Purpose", "## Codemap", "## Layer Boundaries & Invariants",
                   "## Key conventions", "## Authority and governance",
                   "## Validators and enforcement"],
    CLAUDE: ["## 1. First read", "## 5. Critical rules", "## 6. Session start protocol"],
    BACKLOG: ["## Big picture"],
    CONTRIBUTING: ["## Branch naming", "## Commit style", "## Handoff process"],
    JOURNAL: ["# Journal"],
    LESSONS: ["# Lessons Learned"],
}

# The heading `gen_handoff._vision_extract` pulls the boot bundle's vision text out of, and
# the degrade string it emits when the heading is absent. R2 §1.4 R2 prices this one: the
# generator does NOT crash on a miss, it stamps the placeholder into an artifact that is
# immutable the moment it is committed — so the two live here together, and a filename
# decision cannot move one without seeing the other.
VISION_EXTRACT_HEADING = "## Vision"
VISION_EXTRACT_MISSING = (
    f"({VISION} `{VISION_EXTRACT_HEADING}` section not found — fix {VISION} before using this boot)"
)
