# State of Play — 2026-05-25-corp-monorepo-session-sync

---

## What was completed this session

- Deep audit committed 2026-05-20 (commit `1d733b1`): reviewed `src/corp/` module structure, identified conformance gaps against .dev-knowledge governance ADRs.
- Conformance gap audit committed (commit `8a24fae`): catalogued all open gaps between corp-monorepo state and ecosystem ADR requirements.
- Hotfix `eee56ca` merged 2026-04-21: fixed 3 P1 OneDrive safety vulnerabilities in `cleanup/disk.py`, `cleanup/executor.py`, and `actions/_helpers.py`; introduced `OneDriveSafetyError` and `PathTraversalError` in `src/corp/cleanup/errors.py`.
- AI Council debate completed 2026-04-22: 4 AI reviewers evaluated 3 options for OneDrive guard centralization; Option C won (centralized `src/corp/safety/onedrive.py` + AST-based CI scanner), 3-of-4 consensus (Grok dissented, preferred inline guards).
- Safety-invariants ADR-27 drafted and merged into corp-monorepo `docs/decisions/ADR-27-safety-invariants.md`: mandates 4-PR implementation plan.

---

## Current state

- HEAD: `32a47f85b07d697be20066c1ec69df3cf92cb1f6`, branch `main`, working tree clean.
- **ADR-27 implementation MISSING (CRITICAL):** Stage 3 verification confirmed `src/corp/safety/` does not exist and `tests/safety/test_no_unguarded_writes.py` does not exist. The ADR exists and is merged; the code it mandates has not been written.
- **Known drift in `renderer.py`:** `project/renderer.py` raises `ValueError` instead of `OneDriveSafetyError` — not patched by hotfix `eee56ca`.
- **Known unfixed caller:** `deck_actions.py:104` has a write-intent call that was not in the hotfix scope.
- **2 GAP findings open:** Phase 2 universalization BACKLOG items are stale; ADR namespace collision between .dev-knowledge ADR-27 and corp-monorepo ADR-27 is unresolved.
- **2 PARTIAL findings open:** ADR-51 codemap freshness (corp-monorepo `ARCHITECTURE.md` codemap may be stale); ADR-34 vault-file underscore convention not disambiguated in corp-monorepo `CLAUDE.md §4`.
- **Tier deprecation P1 open:** `tier:` and `scale:` frontmatter fields present in corp-monorepo files (e.g., `VISION.md` has `tier: standard`, `scale: L`); removal is P1 governance-blocking per ADR-33.
- **Scrum-master ADR P1 open:** Review authority and merge-gate protocol for architectural changes not yet codified as a corp-local ADR.
- `DECISION_27_onedrive_centralization.md`: VERIFIED PRESENT in `docs/decisions/` — confirms AI Council decision record exists.
- ADR-28 and ADR-29: ABSENT from `docs/decisions/` (file list jumps ADR-27 → ADR-30) — expected or never written; not blocking.
- `2026-04-21-p1-verification.md`: ABSENT from git ls-files — recovery question from Stage 2 is unresolved.
- JOURNAL process drift: 7 consecutive turns were omitted in the prior session; Did/Failed/Next 3-line convention not consistently followed.

---

## Decisions locked this session

- **Option C selected (AI Council 2026-04-22):** Centralized `src/corp/safety/onedrive.py` as single source of truth for all OneDrive path guards, plus AST-based CI scanner at `tests/safety/test_no_unguarded_writes.py`. 3-of-4 consensus; Grok dissented.
- **Option B for vault writer narrowing:** Explicit `VaultZone` enum whitelist approach (not the permissive pattern).
- **JOURNAL append-only 3-line Did/Failed/Next convention:** Each JOURNAL entry must have these three lines; omitting any is a process violation.
- **CMR-NN prefix proposal:** corp-monorepo local ADRs will use `CMR-NN` prefix to resolve namespace collision with .dev-knowledge's `ADR-NN` numbering — decision pending implementation in next session.

---

## Deferred items

- **Phase 2 universalization rollout:** Applying ADR-38 amendment A5 structural requirements (VISION/ARCHITECTURE/BACKLOG at root) across all child repos beyond corp-monorepo. Deferred; do not start in same session as tier-deprecation or scrum-master ADR work.
- **Hyphen migration (ADR-38 subitems 1 and 3):** Renaming any remaining underscore-named files in corp-monorepo to kebab-case. Deferred pending ADR-34 disambiguation.
- **Handoff folder format adoption:** Evaluating whether other active repos need ADR-42 v3.0 format handoffs. Deferred.
- **Root hygiene application:** Removing or relocating stale root-level files in corp-monorepo. Deferred.
- **`renderer.py` drift and `deck_actions.py:104` caller fix:** Deferred to ADR-27 implementation session (directive #1 must first confirm scope).

---

## Rationale (architect judgment)

- **Audit-fix-verify-merge cycle works:** The two-AI-reviewer pattern (Codex `/review` empirically caught a symlink bypass and a test-layer ambiguity bug in prior sessions) demonstrates that architectural changes to safety-critical code must go through review before merge. This is not optional overhead — it has caught real bugs.
- **AI Council with real data produces real decisions:** The 2026-04-22 Council debate used actual code paths, not abstractions. Option C won because the reviewers could trace the inline guard sites and evaluate migration cost concretely.
- **READ FIRST checklist defect is the root cause of prompt drift:** When Claude Code sessions do not load `CLAUDE.md`, `ARCHITECTURE.md`, and the relevant ADR before making changes, the session accumulates invisible assumptions that contradict governance constraints. The Stage 3 verification requirement and the `00_first-message.md` articulation gate are both mitigations for this defect.
- **Directive #1 must precede all P1 BACKLOG work:** ADR-27 implementation status is unknown until verified. Proceeding with tier-deprecation or namespace-collision fixes without confirming whether safety infrastructure is present inverts the priority stack — safety invariants are P0, governance conformance is P1.

---

## Stage 3 verification summary

Verification performed against `git ls-files` snapshot (`08_TREE.txt`) and spot-reads of key files.

| Claim from Stage 2 | Status | Notes |
|---|---|---|
| Hotfix `eee56ca` merged 2026-04-21 (3 P1 OneDrive vulns fixed) | VERIFIED | `git log` shows commit |
| `OneDriveSafetyError` / `PathTraversalError` in `src/corp/cleanup/errors.py` | VERIFIED | File present in `08_TREE.txt` |
| `DECISION_27_onedrive_centralization.md` present in `docs/decisions/` | VERIFIED | File confirmed in `08_TREE.txt` |
| `corp-monorepo/docs/decisions/ADR-27-safety-invariants.md` present | VERIFIED | File confirmed in `08_TREE.txt` |
| `src/corp/safety/onedrive.py` present (ADR-27 implementation) | **MISSING — CRITICAL** | Not in `08_TREE.txt`; `src/corp/safety/` dir absent |
| `tests/safety/test_no_unguarded_writes.py` present | **MISSING — CRITICAL** | Not in `08_TREE.txt` |
| `renderer.py` raises `ValueError` (not `OneDriveSafetyError`) | VERIFIED | Consistent with Stage 2 drift report |
| AI Council debate 2026-04-22 (Option C selected) | VERIFIED via `DECISION_27_onedrive_centralization.md` | |
| ADR-28 in `docs/decisions/` | ABSENT | Not in `08_TREE.txt`; list jumps ADR-27 → ADR-30 |
| ADR-29 in `docs/decisions/` | ABSENT | Same |
| `2026-04-21-p1-verification.md` | ABSENT | Not in `08_TREE.txt` |
| `tier: standard` / `scale: L` in `VISION.md` frontmatter | VERIFIED | Confirmed by direct read |
| JOURNAL omitted 7 consecutive turns | UNVERIFIABLE | External conversation record |
| `deck_actions.py:104` write-intent caller | UNVERIFIED | File present; line not spot-read |

**Summary:** 2 CRITICAL gaps (ADR-27 implementation absent). 2 items absent but not P1-blocking (ADR-28/29). 1 item unresolved (p1-verification.md). All session-claimed completed work verified via git history or file presence.
