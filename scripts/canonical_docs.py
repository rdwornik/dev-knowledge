#!/usr/bin/env python
"""canonical_docs.py — the canonical-doc-name registry.

ONE table for the canonical living-document FILENAMES that ten machine constants across the
gate mesh were each hardcoding independently. Cut from
`docs/audits/2026-08-21-fresh-eyes-cloud-r2-universalization.md` §1.5 GO-(b).

**This is plumbing, not a rename.** Every value here is unchanged — `VISION.md` is still
`VISION.md`. What changes is that a future decision about a canonical filename has ONE place
to be made instead of ten, and that the ten sites are now provably reading the same string.
Whether `VISION.md` is ever renamed is an open operator decision (R2 §1.5 records it as
NO-GO as briefed); this module is worth its keep either way, which is exactly why R2
recommended landing it "whether or not the rename ever happens".

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

# Canonical names that are NOT root living docs but travel with them in one or more of the
# constants below (optional-at-root, or protocols-resident).
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
# ADR-38 A6 (2026-06-02): the seven-file canonical set, mandatory for every repo.
CANONICAL_MANDATORY: tuple[str, ...] = (
    VISION, ARCHITECTURE, CLAUDE, BACKLOG, CONTRIBUTING, JOURNAL, LESSONS,
)

# Canonical names whose CASING is checked when present (mandatory + optional +
# .dev-knowledge-only). Presence is required only for CANONICAL_MANDATORY.
CANONICAL_OPTIONAL: tuple[str, ...] = (ENVIRONMENT, ESSENTIALS, PLAYBOOK, TOKEN_LOG, README)
CANONICAL_ALL: tuple[str, ...] = CANONICAL_MANDATORY + CANONICAL_OPTIONAL

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
