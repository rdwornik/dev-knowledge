# Ecosystem Memory / Feedback / Lessons Coherence — scratch (2026-05-29)

<!-- scope: meta -->

Overnight ecosystem-coherence audit, Phase 7. Read-only: LESSONS.md (144 entries),
TOKEN-LOG.md, gotchas, recent ADR amendments. Richest phase — the feedback loop has
a real enforcement gap. No writes to LESSONS (append-only, out of scope); findings →
BACKLOG.

## Findings

| ID | Sev | Dim | Evidence | Description | Fix scope | Owner |
|---|---|---|---|---|---|---|
| ML-2 | medium | A | `HANDOFF_PROCESS.md:737,745-746,844`; audit `2026-05-29-handoff-v3.4-process-audit.md` §7 | **Feedback flow breaks at enforcement.** LESSON #9 (`LESSONS.md:73`, universal-without-cross-case-verification, 2026-05-14) produced a guard: "mandatory cross-case trace before any future template amendment." But the guard is **advisory prose** in the spec — there is no mechanism that forces it. The v3.4 "Phase C" amendment skipped the trace (amended Stage 3 template, left Stage 1 template + skill stale) and **reproduced LESSON #9's exact failure** — the 2026-05-29 abort. The lesson→guard→enforcement chain is broken at the last link. | Convert the cross-case-trace guard into an enforced step (handoff-amendment checklist gate, or a `/save`-time reminder when templates change). Layer-2 caveat: reminder/checklist, not orchestration. | self |
| ML-3 | medium | D | `LESSONS.md` (grep 2026-05-29/abort/v3.4 → none); JOURNAL + `docs/audits/2026-05-29-*` | **Memory loop gap.** The 2026-05-29 abort is captured in JOURNAL, the process audit, and the fix-campaign verification — but **not promoted to LESSONS.md**. It is an N+2 recurrence of LESSON #9 plus two new lessons: (a) version-straggler sweeps must include CLAUDE.md §7 + the skill, not just the spec; (b) multi-surface amendments (spec + 2 templates + skill + ≥5 ADRs) need a cross-surface completeness checklist. The system witnessed its own repeat-failure but hasn't written the lesson. | Append a LESSONS entry for the abort + fix campaign (future session — append-only, not this read-only audit). | self |
| ML-1 | low | B | `LESSONS.md:1` ("Append-Only Log"); file ordering (2026-05-25 at top → 2026-03-25 at bottom); `JOURNAL.md` intro + global memory note ("LESSONS … oldest-top per ADR-29") | LESSONS.md is maintained **newest-top (prepend)**, but it is described as "**oldest-top** per ADR-29" in the JOURNAL intro and the global memory note. ("Append-only" on line 1 is fine if read as *additive-only/immutable*, which is compatible with prepend — the contradiction is specifically the "oldest-top" descriptor vs the newest-top file.) | Verify against ADR-29 and fix whichever is wrong (the descriptor or the file ordering). | self |
| ML-4 | low | B | `CLAUDE.md:§4,§5` ("Append-only: `LESSONS.md`, `TOKEN-LOG.md`"); `TOKEN-LOG.md` absent | CLAUDE.md §4 (file lifecycle) and §5 (critical rules) name **`TOKEN-LOG.md` as an append-only canonical living file**, but the file **does not exist**. Token logging was deliberately dropped (LESSON 2026-03-28: "Manual token logging … terrible survival rate with ADHD — automate or use gut-check"). The doc still treats the abandoned artifact as canonical. | Remove TOKEN-LOG.md from CLAUDE.md §4/§5 (or recreate it if logging resumes). | self |

## Dimension C — gotcha freshness (spot-check)

`~/.claude/skills/gotchas/gotchas.md` entries carry `Last triggered` dates spanning
2026-03-25 … 2026-05-23 — live, no obviously-dead entry. Their `verify:` lines target
**code repos** (e.g. "Grep `subprocess.run` in `src/` → all use `encoding=utf-8`"),
which `.dev-knowledge` (a docs repo, no `src/`) can't exercise — expected, since the
gotchas are the *universal* skill applied across the ecosystem. No stale gotcha found;
the verify lines are appropriately code-repo-scoped.

## What works (no finding)

- The `verify`-line gotcha format (with `Last triggered` dates) is sound and enables
  the data-driven pruning the 2026-03-26 LESSON called for.
- LESSONS capture is genuinely active (144 entries; multiple per heavy session) —
  the *capture* habit is healthy; the gap is in (a) enforcing the guards lessons
  produce (ML-2) and (b) closing the loop on the latest failure (ML-3).

## Notes

- ML-2 is the single most important ecosystem finding of the night: it explains *why*
  the v3.4 abort happened (a known lesson's guard was never enforced) and predicts it
  will recur on the next multi-surface amendment unless the guard becomes a gate.
- ML-2 + ML-3 + the existing P1 "Codify scrum-master review authority pattern" form a
  cluster: independent review (scrum-master) is currently the *only* working backstop
  for un-enforced guards — which is exactly what caught the v3.4 abort.
