# 05 · What to do now

## Immediate objective

There is **no forced next task** — the v4 redesign closed cleanly. The sender offers
three candidates and explicitly says to **weigh them with Rob against his energy**,
not auto-select. The strongest-argued first move is **(a) convene AI Council to
ratify v4 → ADR**: v4 is live but un-ratified and "wins on conflict" by spec
assertion alone; ratifying it closes a clear governance gap at the lowest blast
radius. Scope = architecture/governance (Council + ADR distillation).

**But before any architecture session**, one piece of low-scope, high-value
hygiene is overdue and Rob flagged it directly: **update `LESSONS.md`** (4 days
stale; today's anti-patterns — folder-creation N+3, chat-mode storytelling,
methodology-duplication, multi-surface fragility — belong there). This is
Sonnet/medium and prevents the exact recurrence ML-2 predicts.

## Top priorities (from BACKLOG — see `BACKLOG.md` for full queue)

**P1 (self):**
- **Codify scrum-master review authority pattern** — N=3 grounding reached
  (unblocked); today's N+3 anti-pattern evidence is the richest yet. Architecture
  territory → also a Council candidate.
- **Sacred-files maintenance enforcement** — canonical files drift; needs a
  mechanism (staleness hook / session-end check).
- **Council decisions management consolidation** — index + contradiction detection +
  ownership model as ADR count passes 60.

**Cross-repo P1 (own-repo sessions, not here — ADR-41):** apply tier-deprecation to
corp-monorepo and to ai-council (remove `tier:`/`scale:` frontmatter).

**P2, high-leverage:**
- **AI Council → ADR formalizing HANDOFF_PROCESS v4** (the governance gate above).
- **Ecosystem feedback-loop enforcement (ML-2)** — convert advisory guards into
  gates; promote the v3.4 abort into LESSONS. The sender calls this the highest-value
  non-doc finding and ties it to Rob's explicit ask for an **agent/enforcement layer
  so he stops repeating structural reminders**.
- **Doc-truth sweep (8 findings)** — CLAUDE.md / ARCHITECTURE describe their own
  tooling/versions inaccurately. One Sonnet pass. *Sequencing tension:* the morning
  briefing put this at #2; the harness re-analysis argues **enforcement-first** (a
  sweep without gates just lets the next 8 drifts recur). Both framings are valid —
  decide with Rob.

**P3 (relevant):** `audit.py` check #8 (v4 bundle structure validator) · codify
metaphor-based communication in PLAYBOOK/ESSENTIALS.

## In-progress branches & repo state

- **`docs/handoff-2026-05-29`** ← you are here; carries this bundle + the Phase-1
  interview. Merge to `main` after the bundle is approved.
- Several **unmerged local branches** from the arc exist (e.g.
  `docs/ecosystem-coherence-audit-2026-05-29`, `docs/handoff-2026-05-29-session-sync`
  [the abort post-mortem], `feature/handoff-v4-redesign-2026-05-29`,
  `fix/handoff-v4-sage-interview-and-folder-2026-05-29`). Most are already folded
  into `main` via merge commits; check `git branch --merged main` before deleting any.
- **Branch:** `docs/handoff-2026-05-29` · **HEAD (main tip):** `367c81e`
- **Working tree at generation:** clean (interview committed; bundle being added)

## Boundaries

- **Do not** edit any ADR / transcript / handoff / audit in place — append only
  (ADR-39). Do not edit old `LESSONS.md` / `TOKEN-LOG.md` entries.
- **Do not** add orchestration to `scripts/` (Layer-2 invariant).
- **Do not** act on corp-monorepo (or any child repo) from here — surface, route,
  don't write (ADR-41).
- **Do not** recreate root `README.md`, `CHANGELOG.md`, or `BACKLOG_ARCHIVE.md`.
- **Do not** treat `.ecosystem/` as authoritative until you've inventoried it with CC.
- **Do not** go looking for the "aborted handoff folder" — it was intentionally
  deleted; the post-mortem audit is the record (see `04_RECENT` cross-check).
- **Do not** push marathon/big-bang scope on day one — single-purpose, defer with
  justification.
