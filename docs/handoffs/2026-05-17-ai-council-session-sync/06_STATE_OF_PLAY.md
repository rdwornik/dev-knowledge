# State of Play — ai-council

<!-- scope: meta -->

## Current HEAD

- **Repo:** `ai-council` — `C:\Users\1028120\Documents\Dev\ai-council`
- **HEAD SHA:** `1bcc6abae464d1455a8cec7fd0eb7cd512e43fd8`
- **Branch:** `main`
- **Working tree:** clean

**Verify before acting:** run `git rev-parse HEAD` in the ai-council repo and confirm it matches the SHA above. If it differs, stop and report the drift — do not proceed until the discrepancy is understood.

---

## What was completed in the most recent session

The most recent documented session (`f2dc586 merge: docs-simplification-rollout into main`) adopted simplified documentation conventions:

- **CHANGELOG.md removed** per ADR-49 — git history + JOURNAL `Changes:` line replaces it
- **BACKLOG_ARCHIVE.md removed** per ADR-49 — done items leave BACKLOG; trace is git
- **Simplified doc conventions adopted** per ADR-48 and ADR-49 — scope-tag enforcement withdrawn, four past-recording files reduced to two (JOURNAL + LESSONS)
- **Deterministic header-normalizer pre-commit hook added** (`scripts/normalize_headers.py`) — cosmetic consistency now handled by normalizer, not audit
- **ADR-48 and ADR-49 ratified** — governance-admission rule for new checks, CHANGELOG/BACKLOG_ARCHIVE removal

The session closed with `1bcc6ab` removing orphaned `docs/handoffs/` from the repo (handoffs are now centralized in `.dev-knowledge` per ADR-42).

*Note: The previous architect chat did not directly witness the docs-simplification session; the above is reconstructed from git log. Verify against the commits if precision matters.*

---

## What the architect witnessed directly

The previous session's architect chat witnessed the identification of a **recurring research-mode question-formulation failure**: when a Council debate question is intended for `research` mode (output = survey of what the field knows), question authors consistently structure it like a `pick`/`judge`/`ideas` decision question instead. The result is shallow opinion where an evidence survey was needed.

**Root cause:** `docs/council-question-guide.md` gives `research` mode only a single table row — no recognition test and no formulation rules. The guide is not giving authors enough to know when and how to write a research-mode question.

**A corrective section was drafted** during the architect chat. It covers three parts: (a) a recognition test — research mode is identified by the output wanted (survey of what the field/industry/literature knows) versus a decision for the asker's specific situation; (b) formulation rules — the headline asks what the field knows rather than what the asker should do, options are evidence-testable candidate approaches (name real systems where possible), source-corpus constraints (recency windows, excluding marketing material) are valid; (c) the breadth-over-depth trap — research questions with more than three sub-questions dilute evidence depth and should be split or explicitly instructed to prioritize the best-evidenced positions.

The operator (Rob) may be able to provide this drafted section directly; if so, use it. If not, it can be reconstructed from the three-part specification above.

---

## Verified absent files (Stage 3 verification)

- **`AGENTS.md`** — NOT present in repo (confirmed via `git ls-files` at HEAD `1bcc6ab`). Must be created.
- **`docs/HANDOFF.md`** — NOT present in repo (confirmed via `git ls-files`). The architect marked its status as "Unknown"; Stage 3 confirms it does not exist. No deprecation action needed.

---

## Governance-compliance gaps

| Gap | Severity | Source |
|---|---|---|
| `AGENTS.md` absent | Active compliance gap (P2) | Council #28 — cross-tool governance mandates AGENTS.md at root |
| `research`-mode question formulation | Active quality problem | Witnessed by architect; recurring pattern across debates |
| LESSONS.md scope-tag backfill | Advisory only (P3) | ADR-46 demoted; tags are informal metadata, not enforced |
| ADR-38 Scale M compliance verification | P2 — verify before declaring clean | May be already compliant; Stage 3 has not verified all required files |

---

## Technical debt and in-flight items

- **Header-normalizer pre-commit hook** was added in the docs-simplification session. It has not been verified clean against current repo state — `pre-commit run --all-files` should be run before other work to establish a clean baseline.
- **ADR-38 Scale M file set** should be confirmed: `README.md`, `VISION.md`, `BACKLOG.md` required; `LESSONS.md` present; `CHANGELOG.md` correctly absent per ADR-49.
- **No in-flight Council debates** were reported as pending capture in an ADR by the architect.

---

## What the architect did NOT witness

The architect's knowledge predates the docs-simplification session by at least one full session. The following are unknown from architect perspective and should be verified against the repo:

- Exact scope decisions within docs-simplification (which items were included vs. deferred and why)
- Any decisions about AGENTS.md timing made during docs-simplification
- Whether LESSONS.md scope-tag backfill was discussed and deliberately deferred
- Exact state of JOURNAL.md, BACKLOG.md at HEAD
