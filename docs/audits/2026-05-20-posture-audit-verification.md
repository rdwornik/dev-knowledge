---
date: 2026-05-20
type: audit
scope: posture-audit-verification
repos: [.dev-knowledge]
verifies: docs/audits/2026-05-19-dev-knowledge-posture-audit.md
adrs: [ADR-28, ADR-35, ADR-38, ADR-42, ADR-51, ADR-53, ADR-54]
status: complete
mode: ground-truth-verification
auditor: Claude Code (Opus 4.7) in-repo
---

# Posture Audit — File-State Verification

**Date:** 2026-05-20
**Verifies:** [`2026-05-19-dev-knowledge-posture-audit.md`](2026-05-19-dev-knowledge-posture-audit.md)
**Mode:** Ground-truth check against actual repo state. Each finding scored **CONFIRMED / PARTIAL / REFUTED / BONUS** with evidence.
**HEAD at verification:** `3ae24c4` (audit-filed commit).

---

## 1. Summary

The audit's **17 findings + 6 tensions** are largely accurate. Verification confirmed all **5 top risks** and surfaced **3 bonus drift items** the witness-based audit could not see (live scripts referencing deleted files; ADR index drift). One numerical correction: LESSONS.md has **135 entries**, not the audit's witnessed "~39."

**Net assessment:** the audit's structural reasoning holds; ground truth is slightly worse than the audit feared in two places (scripts, ADR index) and identical or better in the rest.

---

## 2. Findings Verification

### Area A — ADR-53 / ADR-54 Effort Closure

**A1 — Effort genuinely closed → CONFIRMED.**
- `codex/AGENTS.md` exists; canonical header confirms purpose.
- No root `AGENTS.md` (Glob returned `codex\AGENTS.md` only).
- ADR-54 frontmatter: `Status: Accepted`.
- `ARCHITECTURE.md` §Authority cites ADR-54 globally.

**A2 — Per-repo `AGENTS.md` mechanism unused → CONFIRMED (minor).**
- `codex/AGENTS.md` lines 3–4 state the per-repo overlay model but do not say "currently unused." Low-priority polish item; not worth its own commit.

**A3 — CLAUDE.md v2.1 condensation rationale → PARTIAL.**
- ADR-53 documents the **retirement** rationale (Decisions 1–4 + Rationale section) but not the **v2.1 condensation choices** (last-5 ADR list, scope-tag reduction, per-file-trigger drop). Rationale for those specific condensations lives only in the migration prompts / session memory.
- Severity: LOW. Add as commentary if a future condensation revisits the same trade-off.

### Area B — ARCHITECTURE.md Governance Arc

**B1 — ARCHITECTURE.md freshness is load-bearing with no automated check → CONFIRMED HIGH.**
- ADR-54 Decision 3: Codex reads `ARCHITECTURE.md` for structural context (load-bearing).
- ADR-51 §5: codemap is auto-generated + CI freshness check — both pending.
- `.dev-knowledge/ARCHITECTURE.md` carries `<!-- CODEMAP:START -->` / `<!-- CODEMAP:END -->` markers; codemap **inside is hand-maintained**. Explicit "Open item" callout at line 22–24.
- BACKLOG entry "Codemap generator output specification (ADR-51 open item)" — Stream C, P2, open, added 2026-05-19.

**B2 — Size-tiered policy (S vs M/L) not operationalized → CONFIRMED MEDIUM.**
- ADR-51 Decision 6 specifies graphical for M/L, text-only for S. No tooling exists. `.dev-knowledge` ARCHITECTURE.md §Diagrams notes "no Mermaid diagrams currently" — consistent with the text-only-for-S branch.

### Area C — Sacred Files / Canonical Docs Coherence

**C1 — Sacred-files drift across 9 canonical files → CONFIRMED HIGH + BONUS DRIFT.**
- BACKLOG Cross-stream P1 "Sacred-files maintenance enforcement" lists: **ARCHITECTURE, BACKLOG, CHANGELOG, CLAUDE, CONTRIBUTING, JOURNAL, LESSONS, README, VISION** (9 files).
- **BONUS:** `CHANGELOG.md` is in the canonical list but was **deleted 2026-05-16** per CLAUDE.md §5 ("Do not recreate `CHANGELOG.md` or `BACKLOG_ARCHIVE.md`"). The sacred-files list is itself stale — the very list of files to keep in sync is out of sync with current governance.
- Coherence check still unbuilt; status `open`.

**C2 — ESSENTIALS lags recent ADRs → CONFIRMED MEDIUM.**
- Grep `ESSENTIALS.md` for `ADR-(3[5-9]|4[0-9]|5[0-4])` returns **only ADR-53** (line 87) in topical content; ADR-45 mentioned twice in source-citation footnotes. ADRs **35, 36, 37, 38, 39, 40, 41, 42, 46, 47, 48, 49, 50, 51, 52, 54** absent from any direct reference.
- BACKLOG entry covers 35–41 but is out of date — the actual gap is 35–54.

### Area D — Audit and Tooling Self-Compliance

**D1 — ADR-38 auditor fails its own checks → CONFIRMED HIGH.**
- No `src/` directory (Glob for `src/**/*.py` returned no files).
- No root `pyproject.toml` (only `tests/fixtures/repo-with-structural-checks/pyproject.toml`).
- BACKLOG entry "ADR-38 self-compliance gap — src/ + pyproject.toml" exists, Stream C P2 open.

**D2 — check_backlog_organization regex false-positive → CONFIRMED LOW.**
- BACKLOG entry "Audit tool: check_backlog_organization code-span-aware done-token regex" exists, Stream C P2 open.

**D3 — Hard-coded reference lists in live scripts are drift surfaces → CONFIRMED + BONUS.**
- **`scripts/backlog_extract.py`:** docstring line 2, function lines 22 + 64 reference `BACKLOG_ARCHIVE.md` — a file that CLAUDE.md §5 says is deleted and must not be recreated. The script's purpose ("Extract [done]/[abandoned] entries from BACKLOG.md to BACKLOG_ARCHIVE.md") **contradicts current governance**. The script either does nothing useful or would create a deleted file.
- **`scripts/migrate_links.py`:** `SKIP_NAMES = {'CHANGELOG.md', 'JOURNAL.md', 'LESSONS.md', 'TOKEN-LOG.md'}` — `CHANGELOG.md` is deleted; the skip-set protects a phantom file.
- The audit guessed "drift surfaces"; ground truth is **two live scripts already drifted** against deletions made 2026-05-16.

### Area E — Lessons / Knowledge Retrieval

**E1 — Lessons corpus browse-only → CONFIRMED + correction.**
- LESSONS.md has **135 `### YYYY-MM-DD` entries**, not the audit's ~39. Corpus is materially larger and the retrieval gap is correspondingly worse.
- No `lessons-index.json` exists (Glob returned no files).
- BACKLOG entry "Lessons activation P1 implementation" exists, Stream C P2 open.

**E2 — Council decisions retrievability → CONFIRMED.**
- BACKLOG Cross-stream P1 "Council decisions management consolidation" — sub-items "contradiction detection" and "ownership model" remain open. First-step inventory (decisions/README.md) was closed 2026-05-11.

### Area F — Contradiction Detection

**F1 — Council decisions contradiction detection unbuilt → CONFIRMED HIGH.**
- Same BACKLOG entry as E2; contradiction-detection sub-item still open.

### Area G — Universalization Patterns

**G1 — Skills universalization open → CONFIRMED MEDIUM.**
- BACKLOG Cross-stream P2 "Skills universalization across repos" exists, open.

**G2 — Hooks audit open → CONFIRMED MEDIUM.**
- BACKLOG Cross-stream P2 "Hooks audit + consolidation" exists, open.

**G3 — Phase 2 rollout half-done → CONFIRMED.**
- BACKLOG Cross-stream P2 "Phase 2 universalization rollout": ai-council substantially complete; corp-monorepo not yet started.

### Area H — Process Lessons

**H1–H4 → not file-verifiable; these are session-process observations. No file-state check applies.**

### Area I — ADR Hygiene

**I1 — ADR relationship map / index → CONFIRMED + BONUS DRIFT.**
- `docs/decisions/README.md` carries an "ADR Index" table that **stops at ADR-43, jumps to ADR-44 (Reserved), then to ADR-51–53**. Missing from the index: **ADR-45, 46, 47, 48, 49, 50, 54**.
- ARCHITECTURE.md's "Governing ADRs" section lists 27–53 (no 54). The index doc and ARCHITECTURE.md both lag.
- No supersession-graph artifact exists.

**I2 — ADR-42 amendment open → CONFIRMED LOW.**
- BACKLOG entry "ADR-42 amendment — clarify single vs multi-artifact handoff format" exists, P3 open.

### Area J — Stream Taxonomy

**J1 — Cross-stream exceeds 33% kill criterion → CONFIRMED.**
- BACKLOG entry confirms 40% reading, deferred to 2026-07-01 quarterly grooming. (Audit said "exceeds 33%"; actual is 40%.)

### Tensions T1–T6

Not file-verifiable; these are principle-pair reasoning artifacts. Verification N/A.

---

## 3. Bonus Drift (Not in Audit)

Verification surfaced three items beyond the audit's witnessed findings:

**X1 — `scripts/backlog_extract.py` references deleted `BACKLOG_ARCHIVE.md`.**
- Severity: MEDIUM. Script is callable; behavior contradicts CLAUDE.md §5.
- Disposition: either retire the script (deletion was governance choice) or amend its target. Confirm before action — script may have a residual valid use unknown to verifier.

**X2 — `scripts/migrate_links.py` SKIP_NAMES includes deleted `CHANGELOG.md`.**
- Severity: LOW. Cosmetic; the skip-set protects a file that won't exist.
- Disposition: remove `CHANGELOG.md` from SKIP_NAMES on next touch.

**X3 — `docs/decisions/README.md` ADR Index missing ADRs 45–50 and 54.**
- Severity: MEDIUM. Index is the discoverability surface — missing 7 ADRs makes navigation incorrect. ARCHITECTURE.md "Governing ADRs" section also missing ADR-54.
- Disposition: extend the index table; could be a small commit independent of B1's broader index work (I1).

**X4 — BACKLOG's sacred-files list (Cross-stream P1) names `CHANGELOG.md`.**
- Already covered under C1 above as bonus drift to that finding. Listed here for completeness.

---

## 4. Corrections to Audit Numbers

| Audit claim | Witnessed | Verified | Correction |
|---|---|---|---|
| LESSONS entries | "~39" | 135 | Audit undercounted by ~3.5x; retrieval gap is materially worse |
| Cross-stream % | "exceeds 33%" | 40% | Minor — direction correct, magnitude unstated |
| ADR count | "22+" | 27 ADRs in `docs/decisions/` (numbered 27–54 with gaps at 44) | Direction correct; 27 — gap of 5 from contiguous numbering reflects supersession + reserved slots |

---

## 5. What the Audit Could Not See (Now Known)

- **Live-script drift** from governance deletions (X1, X2).
- **Index doc drift** in `docs/decisions/README.md` (X3).
- **Self-referential drift** in BACKLOG's sacred-files list (C1 bonus).
- **Actual LESSONS volume** (135, not ~39).

The pattern across all four: **the witness-based audit could anticipate structural drift but not specific instances of it**. File-state verification adds the instances; the structural framing remains correct.

---

## 6. Verification's Own Limits

- Did not run `audit.py` to gather machine-readable findings (read-only repo inspection sufficed for the audit's questions).
- Did not enumerate all ADRs' frontmatter for `supersedes:` / `related:` fields needed for an ADR graph (I1 implementation work).
- Did not test whether `backlog_extract.py` runs successfully today against the current `BACKLOG.md` (X1 disposition decision should include this test).
- Did not verify `~/.codex/AGENTS.md` matches `codex/AGENTS.md` byte-for-byte (cross-filesystem; outside this repo's boundary).

---

## 7. Forward Pointer

Triage of these findings into BACKLOG follows in the next commit. Tier-1 scope assessment lives there too.

---

*End of verification.*
