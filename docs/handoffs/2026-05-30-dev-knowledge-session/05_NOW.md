# 05 · What to do now

## Immediate objective

**Run the fresh-eyes review of THIS bundle, then make the promotion decision — in
that order.** This bundle is the v4.3 first real test. Give it (plus the existing
meta-reviewer prompt) to an independent LLM chat with zero project context. **If the
review returns <2 critical findings → promote v4 `beta → stable`** (a single commit
flipping the stamp in `.claude/commands/handoff.md` + `templates/handoff/README.md.tmpl`).
**If ≥2 critical → open a v4.4 cycle** and re-evaluate whether v4 is the right
architecture. Scope: docs/process. **Do not begin downstream work assuming v4 is
stable before the review runs — that is exactly the easy-metric premature-closure
failure mode v4.3 exists to prevent.**

## Top priorities (from BACKLOG)

Gated on this cycle first, then (operator-weighed, not forced-ranked):

- **[P1] Sacred-files maintenance enforcement** — canonical files drift out of date
  at session boundaries; needs an enforcement mechanism (pre-commit staleness hook /
  session-end check). Pairs with the agent-framework signal.
- **[P1] Council decisions management consolidation** — remaining sub-items:
  contradiction-detection mechanism + decision-evolution ownership model (both
  Council territory).
- **[P1] Agent-framework / enforcement layer** — operator's strongest structural
  signal, anchored as `protocols/AGENT_FRAMEWORK.md` v0.1 stub; full build is
  separate Council-scope work. Checks #8/#9 landed one enforcement layer.
- **[P1] Scrum-master review-authority codification** — this 24h is the strongest
  grounding base it has ever had (N+3 operator catches of anti-patterns).
- **Hygiene gate (do first regardless):** **LESSONS.md update** — last touched
  2026-05-25; this arc surfaced an unusually rich pattern set (new-folder-without-
  checking ×3, curse-of-knowledge, triangulation, generated-vs-hand-authored). ~30
  min, Sonnet/medium. Closes ML-2's first surface symptom.

See `BACKLOG.md` for the full queue (don't duplicate it here).

## In-progress branches & repo state

- **`docs/handoff-2026-05-30`** (this branch) — the Phase 1 interview + this Phase 2
  bundle. Merge to `main` after review like the prior handoff branches.
- **`main`** at `5a5ab83` — v4.3 merged, baseline green (103 tests / 9-9 / ruff).
- **Cross-repo (ADR-41, surface only):** corp-monorepo `chore/extract-p1-2-to-backlog-2026-05-28`
  at `a1007b1` — unmerged. Do NOT act on it from `.dev-knowledge`; flag to Rob.
- Several stale local feature branches from the arc exist (`feat/handoff-v4*`, `fix/handoff-v*`)
  — candidates for cleanup once v4.3 is settled; ask before deleting.

- **Branch:** `docs/handoff-2026-05-30`  ·  **HEAD:** `b17711d`
- **Working tree at generation:** clean (interview answers folded into this bundle,
  in-progress folder removed)

## Boundaries

- **Do NOT promote to stable before the fresh-eyes review runs** (premature closure).
- **Do NOT touch the v4.1 / v4.2 historical bundles** — preserved evidence.
- **Do NOT recreate the aborted-handoff folder** (deleted intentionally in `987edac`).
- **Do NOT convene Council for the stable promotion** — operator's explicit call;
  promotion is quality-gated, not Council-gated. Council is for the separate
  architectural ratification ADR.
- **Do NOT act on the corp-monorepo branch from here** (ADR-41).
- **Do NOT introduce any new folder/naming/convention** without checking the existing
  one first — the period's single most-repeated anti-pattern (3× in 24h).
- **Inventory `ecosystem/` before treating it authoritative** — operator stated he
  doesn't know how it works; verify with CC (`ls ecosystem/`) first.

## How to choose

If multiple first-moves present themselves, **propose your choice with rationale to
Rob** — don't ask him to forced-rank. The fresh-eyes review is the unambiguous first
move here; everything else waits on its verdict.
