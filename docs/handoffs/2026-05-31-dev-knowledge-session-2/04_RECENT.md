# 04 · What just happened

A narrative of recent work on `.dev-knowledge`, written so a chat with zero prior
context can pick up the thread. Prose, not a log dump.

## The arc

This handoff closes a **6-day marathon (May 26–31)** inside a longer
**universalization** project — making repository structure, way-of-working, and
process **portable** across the operator's ecosystem (`.dev-knowledge` as canonical
source → `corp-monorepo`, `ai-council`, future repos). Each wave shipped one
portability vector.

**Foundation (May 26–29).** Three ADRs: **ADR-59** (dot-prefix visual config
pattern), **ADR-60** (docs taxonomy — immutable source vs regenerable extract),
**ADR-61** (git-worktree for parallel CC sessions). Mermaid process diagrams added to
ARCHITECTURE with audit check #7 enforcing dark-theme rendering; branch graveyard
cleaned (~73 stale branches). *(Parallel: AI Council CLI v1.0 shipped in `ai-council`
— a different repo, recorded but out-of-scope here per ADR-41.)*

**HANDOFF_PROCESS v4 saga (May 29–30).** v3.4 was aborted under audit (Path C
deprecation, not patch-forward); a 22-finding ecosystem audit forced a ground-up
redesign. **v4** = 8 files, 2-phase (interview → bundle), sage→apprentice frame,
four-tag epistemic discipline. Iterated v4.1 → **v4.2 (Amendment A**, canonical
four-tag) → **v4.3** (comprehensive close: tests 90→103, audit 7/7→9/9) → **v4.3.1**
(caveat patch). Promoted **beta → stable** on the judgment-augmented criterion (use
count AND reviewer verdict, reviewer overrides count). 11 LESSONS appended (May 30).

**ADR sweep (May 30–31).** **ADR-62** (v4 ratification) + **ADR-63** (scrum-master
authority codification) via **Path A** (post-hoc records of already-validated
outcomes — Council would be ceremony). Fresh-eyes review returned MERGE WITH PATCHES;
sharpest finding: **ADR-62 *relaxes* the same ML-2 guard ADR-63 *gates*** — opposite
cures, reconciling principle deferred to BACKLOG P3. Two patch rounds (986d350,
5d02db6 after a Codex /review HIGH-severity catch). Merged `a637f5f`.

**Today (May 31) — handoff skill saga, the immediate context.** (1) *Morning:* first
production use of v4-stable — a cold-start bundle at
`docs/handoffs/2026-05-31-dev-knowledge-session/` (merged `6a228eb`). (2) *Auto-scope
partial fix:* a 3-case decision tree added to the skill (merged `bd909ff`) — it
**proved incomplete the moment a 4th invocation state (slug collision + new work)
appeared**, which is exactly the cluster-as-diagnosis failure the LESSONS warn about.
(3) *Revert:* operator demanded REVERT + comprehensive redesign rather than another
incremental patch (`0c98611`). (4) *Comprehensive 5-case matrix:* the skill now
resolves **every** invocation state deterministically from git state — no scope
question, ever (`8e4b5ea`, skill 135→201 lines, merged `f7de267`). **This very
handoff is that matrix's first production validation:** invoking it hit **Case 4**
(clean tree + commits since last handoff + today's slug exists) and auto-selected the
counter-suffix slug `-session-2` with no question. It worked.

## Four-tag discipline (canonical)

The sage tagged every claim using this discipline (canonical per HANDOFF_PROCESS
v4.3 Amendment A; supersedes the earlier three-tag body in spec §3.1):

- **witnessed** — sage just verified this OR saw it happen recently AND has no
  reason to think it changed since
- **recall** — sage remembers from earlier in the session; **state may have
  changed** — verify via CC inline if the claim is load-bearing
- **inferred** — reasoning from evidence (not direct knowledge)
- **unknown** — sage doesn't know — flagged explicitly

When you encounter `recall` or `unknown` on a load-bearing claim in this file,
verify via CC before acting on it. This is the "handoff is back-and-forth" rule.

## What the sender chat said (interview)

The sender framed the whole arc as **universalization** — not side-work but the
strategic domain (`WC2`, recall). Every artifact above served portability of one
vector. The today-saga the sender tagged **witnessed** (it happened in front of
them); the older waves and ecosystem-wide counts (ADR totals, LESSONS counts,
ai-council 310 tests) they tagged **inferred** — record-derived, and the ai-council
ones are cross-repo. The sender's strongest forward signal: **memory management is
the foundation under everything** (`WC6`) — three-domain separation (Obsidian =
pre-sales, `.dev-knowledge` = methodology, `~/.claude/` = runtime); violate it and
every downstream process degrades. Two explicit Phase-2 asks were honored in this
bundle: inspect the `ecosystem/` folder and name its gap (→ `03_PROJECT`), and
describe the AI Council operational flow (→ `02_METHODOLOGY`).

## Load-bearing facts (cross-checked vs repo at Phase 2)

| Claim from sender | Repo fact | Phase-2 verdict | Verification command |
|---|---|---|---|
| HEAD `f7de267`, tree clean | HEAD now `a21e355` (Phase-1 commit advanced it); tree clean | ⚠️ benign drift — expected | `git rev-parse --short HEAD` |
| Skill 135 → 201 lines | 201 lines | ✅ matches | `wc -l .claude/commands/handoff.md` |
| Comprehensive matrix Case 4 fired → slug `-2` | witnessed this session; slug `-session-2` | ✅ matches | (matrix run at Phase 1) |
| Commits 9cf7707/bd909ff/0c98611/8e4b5ea | all present in history | ✅ matches | `git log --oneline` |
| "63 ADRs" | **36 ADR files**, highest number ADR-63 | ⚠️ drift — number ≠ count | `ls docs/decisions/ADR-*.md \| wc -l` |
| LESSONS "50 entries" | not verifiable via header probe (pipe-delimited format) | ❔ unverified — treat `inferred` | `grep -c '^### ' LESSONS.md` (inconclusive) |
| Tests 103 / audit 9/9 | 103 passed / health OK | ✅ matches | `pytest -q && python scripts/audit.py health` |
| `ecosystem/` folder is open-design registry | exists, no dot; index.yaml stale 2026-05-23 | ✅ matches | `ls ecosystem/` |

## Decisions & reasoning to carry forward

- **D1 — Path A vs Council:** Path A for *empirically-validated, post-hoc* decisions;
  Council for *forward-looking* decisions with real optionality. (inferred)
- **D3 — Four-tag, adding `unknown` as first-class** made "I don't know" an honest
  answer, not an embarrassment — foundational to honest sage→apprentice transmission.
- **D6 — Counter-suffix for Case 4 slug collision** chosen for *determinism*;
  topic-based (judgment-heavy) and timestamp (non-semantic) rejected. (witnessed)
- **D7 — Comprehensive over incremental:** after the partial fix failed on Case 4,
  the operator forced a full revert + 5-case redesign rather than a third patch.
  **This is the arc's central lesson** — partial fixes that miss edge cases ARE the
  disease. (witnessed)
- **D9 — The operating discipline is itself the deliverable:** architect-in-browser +
  executor-in-CC, sage→apprentice handoff, operator-as-scrum-master, fresh-eyes
  triangulation (operator runs it, not the architect), honest no-op over fabricated
  commit. These are scattered across ADRs/LESSONS but cohere as one operating mode.
- *Harder than expected:* curse-of-knowledge recursion (caught at ~7 meta-levels —
  expect the 8th). *Easier:* CC executes a comprehensive matrix cleanly once it's
  *designed* — the hard part was the architect overcoming the partial-fix reflex.
