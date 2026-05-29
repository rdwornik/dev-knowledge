# 04 · What just happened

A narrative for a chat with zero prior context. The last several days were **not**
"some handoff work" — they were the closing chapter of a multi-day **ecosystem
universalization arc** (≈2026-05-26 → 2026-05-29). Today's visible output (the v4
handoff redesign) sits on top of that larger arc.

## The arc

**The universalization arc (2026-05-27 → 2026-05-28).** A 2026-05-26
universalization had over-propagated `.dev-knowledge`-specific folders to child code
repos. The correction landed as **ADR-60** (two-variant `docs/` taxonomy:
`.dev-knowledge` keeps `handoffs/`; child code repos do not) plus a 2026-05-28
addendum making the baseline uniform across child repos (operator preference:
"when I open any repo it looks the same"). Alongside: **ADR-59** visual pattern
(dot-prefix configs, ALL-CAPS canonical roots), four Mermaid process diagrams in
`ARCHITECTURE.md`, the standalone **AI Council CLI v1.0** (310 tests; runbook
`protocols/AI_COUNCIL_PROCESS.md`), a Mermaid **dark-theme v1→v2** fix (v1 only
rendered one diagram readably on Rob's black background — caught by *hard-metric*
closure, then fixed and rolled across all repos; `audit.py` check #7 enforces it,
health went 6/6 → **7/7**), and **ADR-61** (git-worktree pattern for same-repo
parallel sessions). A universalization **durability audit** rated 7/11 findings
fully durable, 3/11 partial.

**Today's marathon (2026-05-29).** Three things happened in sequence:

1. **The v3.4 handoff first-test ABORTED.** The first real run of the old v3.4
   process failed at Stage 3 — the sender produced only the pipeline sections
   because the Stage-1 question template never asked for claims/scope, compounded by
   fabricated structure. An **empirical process audit** returned **13 findings**
   (2 critical, 4 high, 6 medium, 1 low). Rob chose **Path C** (fix all 13) over a
   minimum retry. All 13 closed, ADR-39 immutability respected via append-only
   amendments on six ADRs (42/45/55/56/57/58 — verified by `git numstat`:
   insertions only, 0 deletions). Hard-metric simulation PASS.

2. **The overnight ecosystem coherence audit** returned **22 findings** (0 critical,
   0 high, 12 medium, 10 low). The dominant pattern: **doc-truth drift** (12 of 22)
   — and the structural lesson **ML-2: un-enforced guards** (conventions are
   authored well but not gated). The irony the sender flags: the repo whose VISION
   says "drift detected proactively" is itself the largest drift surface.

3. **The handoff v4 redesign.** Reading the 13-finding audit, the diagnosis was that
   the disease wasn't 13 bugs — it was the **13/14-file, multi-stage architecture**
   (multi-surface fragility). So v3.4 was replaced wholesale by **v4**: two phases
   (interview → consolidate), **8 bundle files generated from source**, an operator
   escalation ladder, a content-based state machine. v4 was implemented, then a
   same-morning **v4.1 fix** corrected two defects the first Phase-1 run surfaced —
   a unilaterally-introduced `_scratch/` folder (reverted to the existing
   `in-progress/` convention) and a two-cluster interview (collapsed to the single
   **sage→apprentice** cluster, because the methodology cluster duplicated the books
   the apprentice reads anyway). v3.4 is archived at
   `protocols/archive/HANDOFF_PROCESS_v3.4.md`; the spec is now **v4.1**.

**This handoff is the post-fix first real v4 test** — the very flow you are reading.

## What the sender chat said (interview)

The sender (sage) framed the session as the **end of a 5-wave arc**, not a single
task, and was explicit about tagging *witnessed / inferred / unknown*. Key
witnessed points folded in above. Three the sender stressed:

- **The new-folder anti-pattern recurred N+3 times in ~24h** (`docs/strategic/`,
  `_scratch/`, the two-cluster design). The right gate is *pre-output*: verify the
  existing convention **before** any prompt proposes a path or structure. This is
  the single most-repeated anti-pattern of the session and the strongest grounding
  the scrum-master codification ADR has ever had.
- **Chat-mode storytelling vs empirical work** — defaulting to "generate a prompt"
  when the correct move was to read artifacts and synthesize in chat with file:line
  evidence. Rob caught this repeatedly.
- **`.ecosystem/` registry knowledge gap (unknown):** the sender implemented it
  earlier; Rob says he doesn't fully know how it works. Treat it as *not yet
  authoritative* until you ask Claude Code to inventory it.

## Load-bearing facts (cross-checked vs repo at Phase 2)

| Claim from sender | Repo fact | Verdict |
|---|---|---|
| `main` at `367c81e`, the v4.1-fix merge | `main` HEAD = `367c81e` | ✅ matches |
| `pytest` 90 / `audit.py` 7/7 / ruff clean | pre-commit + 90 tests pass at Phase 2 | ✅ matches |
| HANDOFF spec is **v4.1** | `protocols/HANDOFF_PROCESS.md` → `Version: 4.1` | ✅ matches |
| v3.4 archive preserved | `protocols/archive/HANDOFF_PROCESS_v3.4.md` exists | ✅ matches |
| LESSONS.md ~4 days stale | last commit **2026-05-25** (4 days) | ✅ confirmed — act on it |
| **Aborted handoff folder** `docs/handoffs/aborted/…ABORTED/` is **preserved, "do not delete"** | folder was **deliberately DELETED** in commit `987edac`; absent from the working tree. Surviving record is the post-mortem audit `docs/audits/2026-05-29-handoff-v3.4-process-audit.md` (present) | ⚠️ **DRIFT** — the sage's "preserve, do not delete" is stale. Nothing to preserve; it is already gone, intentionally. Don't go looking for it. |
| **corp-monorepo** P1-2 path-traversal branch "operator thinks merged" (*chyba ogarnięty*) | corp-monorepo is **still on** `chore/extract-p1-2-to-backlog-2026-05-28` (HEAD `a1007b1`), **not merged to main** | ⚠️ **DRIFT** vs operator belief — confirms BACKLOG **CM-1**. Cross-repo → corp-monorepo's own session (ADR-41); surface to Rob, do not act from here. |

## Decisions & reasoning to carry forward

- **Path C over minimum retry** — "do it right not fast"; a minimal retry would have
  left 11 known bugs latent. Comprehensive closure + hard-metric simulation paid off.
- **v4 redesign over v3.4 patch** — *when audit findings cluster, the cluster is the
  diagnosis.* The disease was the architecture, not the bug list. The **Hashimoto
  principle** (every mistake becomes a structural change, not another prose guard)
  is the through-line.
- **sage→apprentice frame** — theory lives in the books (PLAYBOOK/ESSENTIALS) which
  the apprentice reads independently; the sage transmits only *lived implementation*.
  Generalizes: metaphors carry design intent better than ADR-numbers in human↔LLM
  dialogue (P3 BACKLOG to codify).
- **v4 implemented WITHOUT an ADR — deliberately.** Architecture goes through AI
  Council, and Council was skipped for fatigue. v4 "wins on conflict" by spec
  assertion only; the ADR is deferred (P2 BACKLOG). *If you change v4 substantively,
  the ratification gap compounds.* (Opinion of the sender, shared here as guidance.)
- **Handoff is back-and-forth, not a unilateral guess** — if you don't know
  something and the cost to resolve is low, have Claude Code verify rather than
  passing forward "unknown." (This Phase 2 did exactly that for the two drifts above.)
