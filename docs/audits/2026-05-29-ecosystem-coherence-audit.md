# Ecosystem Coherence Audit — 2026-05-29 (overnight)

<!-- scope: meta -->

| Field | Value |
|---|---|
| Date | 2026-05-29 (overnight continuation) |
| Trigger | Operator continuation after the handoff v3.4 fix campaign; broader ecosystem sweep |
| Method | Read-only audit across 7 dimensions (skills, hooks, workflows, goals, corp-monorepo, cross-doc, memory/feedback) |
| Auditor | Claude Code (Opus), `.dev-knowledge` |
| Branch | `docs/ecosystem-coherence-audit-2026-05-29` (off the fix-campaign tip) |
| Scratch sources | `docs/audits/scratch/2026-05-29-ecosystem-{skills,hooks,workflows,goals,corp-monorepo-coherence,cross-doc-harmony,memory-feedback}.md` |
| Total findings | **22** — 0 critical, 0 high, 12 medium, 10 low |
| Ecosystem health | **green** — 90 tests pass, audit.py 7/7, ruff clean, corp-monorepo 2554 tests collectable, clean trees |

## 1. Context

Overnight continuation of the 2026-05-29 session. The handoff v3.4 fix campaign
(13/13 findings closed, retry-ready) is on branch
`fix/handoff-v3.4-complete-campaign-2026-05-29` awaiting merge. This audit reads the
*fixed* state as baseline and widens the lens to the whole ecosystem: skills, hooks,
workflows, goals, the corp-monorepo cross-repo boundary, cross-doc harmony, and the
memory/feedback loop. **Diagnose-only** — every finding routes to BACKLOG; fixes are
separate focused sessions. Read-only outside `.dev-knowledge` (ADR-41).

## 2. Audit method

Seven phases, one scratch report + commit each (Phases 1–7), then this consolidation.
Dimensions per phase as specified in the continuation prompt. Cross-checks were
grep- and file-existence-verified; corp-monorepo was inspected read-only (status,
log, CLAUDE.md head, test-collect — never run, never modified).

## 3. Findings table

Severity: **critical** = blocks work / unsafe; **high** = degrades correctness;
**medium** = clear gap, no current blocker; **low** = cleanup / cosmetic / informational.

| ID | Sev | Dim | Evidence (file:line) | Description | Fix scope | Owner |
|---|---|---|---|---|---|---|
| ML-2 | medium | memory/A | `HANDOFF_PROCESS.md:737,745-746,844`; abort audit §7 | LESSON #9's cross-case-trace guard is advisory prose, not enforced → v3.4 reproduced #9's failure (the abort). Feedback loop breaks at enforcement. | Convert guard to a checklist/gate on template amendments | self |
| ML-3 | medium | memory/D | `LESSONS.md` (no 2026-05-29 entry) | The abort (N+2 of #9 + new straggler/multi-surface lessons) is in JOURNAL+audit but not promoted to LESSONS. | Append a LESSONS entry (future session) | self |
| SK-1 | medium | skills/B | `CLAUDE.md:§7` vs `~/.claude/commands/` | §7 lists user-level `/save` (absent at user level); omits `/codex-review`, `/evolve` (present). | Update CLAUDE.md §7 to match disk | self |
| SK-2 | medium | skills/B | `CLAUDE.md:§8` vs `~/.claude/skills/` | §8 calls boot/session-summary/handoff/save "skills" (they're commands); omits the real `verify` skill. | Rewrite CLAUDE.md §8 (skills = gotchas + verify) | self |
| SK-3 | medium | skills/C | `~/.claude/commands/boot.md:7-19`; global Self-Evolution Protocol | boot + protocol read `sessions.jsonl`/`violations.jsonl`/`corrections.jsonl`/`observations.jsonl` — none exist (only `learned-rules.md`, `evolution-log.md`). Evolution machinery vacuous (degrades gracefully). | Create the logs OR repoint to `evolution-log.md` | ~/.claude |
| HK-1 | medium | hooks/B-D | `CLAUDE.md:§9,§4` vs `.pre-commit-config.yaml` | ruff documented as a pre-commit hook; it is NOT in the config (only normalize-dated-headers + codemap-freshness). corp-monorepo *does* enforce ruff. | Add the ruff hook OR correct the doc | self |
| HK-2 | medium | hooks/C | `~/.claude/settings.json` SessionStart+Stop | Evolution hooks count/echo from non-existent `.jsonl` logs (= SK-3 root). Scorecard sink absent. | Create logs OR repoint hooks | ~/.claude |
| HK-3 | medium | hooks/C | `~/.claude/settings.json` Stop hook | A Stop hook exists but does no functional session-close automation (no clean-tree/audit check). 4 concrete use cases listed in scratch. | Design 1-2 session-close automations (read-only) | self/~/.claude |
| WF-1 | medium | workflows/A-B | `ARCHITECTURE.md` §Governing ADRs | Omits ADR-59 (grounds audit.py checks #4–#6) and ADR-61, both binding (CLAUDE.md §11 lists them). | Add ADR-59 + ADR-61; cross-link 59→audit checks | self |
| WF-2 | medium | workflows/C | `ARCHITECTURE.md` §Validators | (a) repeats false ruff-pre-commit claim; (b) lists `scripts/backlog_extract.py` (does not exist); (c) omits the real codemap-freshness hook. | Correct the validators list | self |
| CD-1 | medium | cross-doc/A-D | `CLAUDE.md:94` | `/handoff` described as "ADR-42 v3.3.3"; spec/skill/ARCHITECTURE are v3.4. Same straggler class as the abort; outside fix-campaign scope. | One-line edit v3.3.3→v3.4 | self |
| CM-1 | medium | corp-mono/C-D | corp-monorepo HEAD `chore/extract-p1-2-to-backlog-2026-05-28`, tip `a1007b1` | P1-2 path-traversal extraction landed but sits on an unmerged branch; HEAD not on main. | Merge branch → main; resolve pre-delete gate | corp-monorepo |
| SK-4 | low | skills/C | `~/.claude/skills/verify/cross-repo-boundaries.ps1:1-30` | Hard-codes corp-monorepo package layout ("last validated 2026-03-28"); silently passes if layout drifted (missing-path → no errors). | Re-validate vs current layout; add missing-root guard | ~/.claude + corp-monorepo |
| SK-5 | low | skills/D | (inferential) | Gap: no SessionStop functional automation (overlaps HK-3). | See HK-3 | self |
| HK-4 | low | hooks/A-D | per-repo pre-commit configs | corp-ops + corp-sca-time-automation have NO pre-commit; ai-council only normalize-headers; hook-id naming drift (`normalize-dated-headers` vs `normalize-headers`). | Define a pre-commit floor + align id names | corp-ops, corp-sca, ai-council |
| WF-3 | low | workflows/C | `ARCHITECTURE.md` §Handoff diagram s2c/s2d,s1b | Diagram attributes scope/claims to "Operator" (per ADR-57/58 they're the architect's); "SBAR/I-PASS" label unused elsewhere. Cosmetic. | Tweak diagram labels | self |
| GO-1 | low | goals/C-D | `VISION.md:39-42` | Emphasis #1 asserts "adoption pace tracked as a health signal" — no instrument tracks it. Aspiration vs mechanism. | Build a light signal OR soften wording | self |
| GO-2 | low | goals/D | `VISION.md:6` frontmatter | `last_reviewed: 2026-05-24` predates ADR-59/60/61 + v3.4 arc. No review trigger fired (not overdue). Informational. | Optional VISION review at next boundary | self |
| CD-2 | low | cross-doc/B | `CLAUDE.md:148` vs `:144` | Footer "Last updated: 2026-05-24" contradicts §12 history "v2.3 (2026-05-28)". | Bump footer (fold with CD-1) | self |
| ML-1 | low | memory/B | `LESSONS.md:1`; file ordering; JOURNAL intro | LESSONS is newest-top (prepend) but described "oldest-top per ADR-29". Descriptor vs file mismatch. | Verify vs ADR-29; fix the wrong one | self |
| ML-4 | low | memory/B | `CLAUDE.md:§4,§5`; `TOKEN-LOG.md` absent | TOKEN-LOG.md named as append-only canonical but doesn't exist (logging dropped per 2026-03-28 LESSON). | Remove from §4/§5 (or recreate) | self |
| CM-2 | low | corp-mono/A | corp-monorepo `CLAUDE.md:§1` step 4 | Still references the flat `docs/handoffs/*.md` (pre-ADR-42). Confirms existing BACKLOG P3 flat-handoff item. | Migrate at next handoff event | corp-monorepo |

## 4. Cross-finding interactions

- **SK-3 ≡ HK-2** — one root cause: the evolution `.jsonl` logs (sessions/corrections/
  violations/observations) were never created; both boot.md (SK-3) and the lifecycle
  hooks (HK-2) read from them. Fix once.
- **HK-1 ≡ WF-2(a)** — the "ruff is a pre-commit hook" claim is false and appears in
  *two* docs (CLAUDE.md §9/§4 and ARCHITECTURE.md §Validators). Fix both together.
- **SK-1 + SK-2 + CD-1 + CD-2 + WF-1 + WF-2 + ML-1 + ML-4** — one meta-class:
  **CLAUDE.md / ARCHITECTURE describe their own tooling/versions/files inaccurately.**
  A single "doc-truth sweep" closes all eight.
- **ML-2 → (the entire fix campaign)** — the un-enforced cross-case-trace guard is the
  *root cause* of the v3.4 abort that the fix campaign just remediated. ML-3 (promote
  the abort to a LESSON) closes that loop; ML-2 (make the guard a gate) prevents the
  next recurrence.
- **ML-2 + ML-3 + P1 "scrum-master codification"** — independent review is currently
  the only working backstop for un-enforced guards; codifying it is the structural fix.
- **SK-4 depends on Phase 5** — the verify script's assumed corp-monorepo layout should
  be checked against the repo's actual `packages/` structure.

## 5. Recommended fix sequence

Each is a single-purpose session (no big-bang). Effort = model + level.

1. **Merge the two overnight branches** *(operator, now).* Fix campaign first, then
   this audit branch. Commands in the morning briefing §4.
2. **Doc-truth sweep** *(Sonnet, medium).* Closes SK-1, SK-2, CD-1, CD-2, WF-1, WF-2,
   ML-1, ML-4, HK-1(doc side) — all CLAUDE.md/ARCHITECTURE accuracy one-liners +
   small list fixes. Highest finding-count-per-effort. Verify vs ADR-29 for ML-1.
3. **Feedback-loop enforcement** *(Opus, medium).* ML-2 (cross-case-trace guard → gate)
   + ML-3 (promote abort to LESSON) + the existing P1 scrum-master codification.
   Judgment-heavy; the structural win of the night.
4. **Evolution-log + hooks** *(Sonnet/Opus, medium).* SK-3/HK-2 (create or repoint the
   `.jsonl` logs), HK-3/SK-5 (one read-only SessionStop automation). Runtime config.
5. **ruff-enforcement decision** *(Sonnet, low).* Decide add-the-hook vs doc-only;
   foldable into #2.
6. **corp-monorepo merge + hygiene** *(operator / corp-monorepo session).* CM-1 (merge
   the P1-2 branch), CM-2 (flat-handoff migration at next handoff). Owner repo.
7. **Cross-repo hook baseline** *(per-repo, low).* HK-4 — corp-ops/corp-sca/ai-council
   pre-commit floor. Owner repos.
8. **VISION touch** *(Sonnet, low, optional).* GO-1 (adoption signal), GO-2 (review).

## 6. What was NOT audited (gaps)

- **CKE (corp-knowledge-extractor) and corp-by-os internals** — only referenced via the
  verify script (SK-4); not inspected.
- **corp-ops / corp-sca-time-automation** — only pre-commit presence checked (none); no
  deeper coherence read.
- **ai-council internals** — only pre-commit + cross-references from `.dev-knowledge`;
  the live `src/ai_council/*.py` modules were not traced.
- **The evolution `.jsonl` content** — they don't exist (SK-3); nothing to read.
- **ADR-29 actual text** — ML-1's "oldest-top" claim is asserted against the JOURNAL
  intro + global note, not verified against ADR-29 itself (low confidence on which is wrong).
- **Token / size budget** — the original v3.4 audit's deferred ADR-57 "bundle may remain
  heavy" risk was not measured here either.
- **The 5 Council transcripts** — immutable; not re-read.

## 7. Meta-observations

- **Dominant pattern: documentation-truth drift.** 12 of 22 findings (and 8 in one
  meta-class) are "the doc claims X; reality is Y" — stale version strings, a
  non-existent script and a non-existent log file listed as canonical, a ruff hook
  documented-but-absent, a skill/command inventory out of sync with disk. None breaks
  anything; all erode trust in the governance docs that are the repo's whole product.
  The repo whose VISION is "methodology consistency / drift detected proactively" is
  itself the locus of the drift.
- **Second pattern: un-enforced guards.** ML-2 is the structural lesson — the ecosystem
  is good at *writing* guards (LESSONS, ADR mitigations, conventions) and poor at
  *enforcing* them. The v3.4 abort is the proof: a guard existed, wasn't a gate, and the
  failure recurred. Independent (scrum-master) review is currently the only backstop —
  which is exactly why codifying it (open P1) matters.
- **Health is sound.** Zero critical/high; tests/audits/trees all green across repos.
  This is a coherence-and-truth audit, not a breakage audit. The system works; its
  self-description has lagged its own velocity.

## 8. Retry-readiness inheritance

Per the fix-campaign verification report
(`docs/audits/2026-05-29-handoff-v3.4-fix-campaign-verification.md` §6): the handoff
process is **RETRY-READY**. All 13 audit findings closed; the hard-metric simulation
(§4 of that report) confirmed a fresh Stage 1 generation now requests
`next_session_scope` + `11_CLAIMS.md` (with schema) + gate-probe review inside the
architect-facing paste block. Nothing in this ecosystem audit changes that verdict.
Note CD-1 (CLAUDE.md §7 still says "/handoff … v3.3.3") is a *documentation* straggler,
not a process defect — it does not block the retry, but it is the same straggler class
and should be swept in fix-session #2.
