# 05 · What to do now

## Immediate objective

First, **finish this v4.2 re-test cleanly**: this bundle is Phase 2 output; once Rob
merges `fix/handoff-v4.2-refinements-and-rerun-2026-05-29`, the re-test is complete
and tomorrow's apprentice starts from a v4.2 bundle. After the merge, the natural
first work item is the **LESSONS.md update** (see below) — a hygiene gate before any
architecture session.

## Top priorities (from BACKLOG)

- **[P1] Codify scrum-master review authority** — N=3+ grounding reached; this
  session added the strongest evidence yet (operator catching anti-patterns 3× in
  24h). Codification is itself an architecture decision → Council.
- **[P1] Council decisions consolidation** — index + contradiction detection +
  ownership model for decision evolution. ADR corpus is 60+; navigability degrades.
- **[P1] Sacred-files maintenance enforcement** — canonical files drift stale; part
  of the enforcement-layer trio (with audit.py check #8 + an eval-suite minimum) that
  treats the ML-2 root cause.
- **[P2] AI Council → ADR ratifying v4 + v4.2** (single decision). Closes the
  unilateral-implementation governance gap.
- **[P3] audit.py check #8** — v4 handoff structure validator (8 files, line budgets,
  no shipped markers, no stale in-progress interview). Read-only, no orchestration.

## Sequencing note (from the sage)

The morning briefing put a doc-truth sweep first (symptom-first, fast win); the
harness-positioning analysis argued enforcement-layer first (cause-first). Both have
merit. **LESSONS.md update is universally first** regardless — today's anti-patterns
(new-folder-without-approval ×3, chat-mode storytelling vs empirical work, sage
tagging discipline) belong there before they recur.

## In-progress branches & repo state

- **Branch:** `fix/handoff-v4.2-refinements-and-rerun-2026-05-29` · **HEAD:** `3ae2b6b`
- **Working tree at generation:** clean · baseline green (90 tests / audit 7/7 / ruff)
- **Unmerged:** this branch (awaiting Rob's merge after the re-test).
- **Cross-repo (ADR-41 — surface only, do NOT act):** corp-monorepo
  `chore/extract-p1-2-to-backlog-2026-05-28` @ `a1007b1` is still unmerged.

## Boundaries

- **Do NOT** touch the v4.1 first-run bundle (`docs/handoffs/2026-05-29-dev-knowledge-session/`)
  or `protocols/archive/HANDOFF_PROCESS_v3.4.md` — historical evidence.
- **Do NOT** write the v4/v4.2 ADR yourself — that is Council's call.
- **Do NOT** introduce any new folder/naming/convention without verifying the
  existing one first.
- **Do NOT** proceed past your first concrete work item without updating LESSONS.md.
- Single-purpose session; respect operator energy; no aggressive bundling.

## How to choose

If more than one first-move looks viable, **propose your choice with rationale to
Rob** — don't ask him to forced-rank. Operator energy is finite; your job is reasoned
pre-selection. Rob confirms or redirects.
