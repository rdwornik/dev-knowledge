# Probe manifest — architect mode, cross-repo (target: ai-council): orientation first, then teeth (v5.3 §5 + §13c)

<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and **no
> answer**. The browser has no file access, so for every probe it must reply **"run `<command>`"** —
> surfacing the off-bundle dependency instead of bluffing it. **CC** runs each command against **live
> state at check-time**, re-derives ground truth, and records PASS/FAIL. **Any FAIL blocks
> onboarding.** Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor (never a synthesized
> pass); git/tooling absent → reported *skipped* (degraded coverage visible), never counted as pass.
>
> **Cross-repo (ADR-36/41).** The target is **ai-council**, which has **no** `audit.py` / `ship-gate`.
> These probes are **ai-council-native** — bound to its git, its pytest, its JOURNAL, its floor-guard,
> its ADR index. **Run every command from the ai-council checkout**
> (`cd C:\Users\1028120\Documents\Dev\ai-council`), not the hub.
>
> The answers — the orienting lines, the test count, the HEAD sha, the two JOURNAL/git dates, the
> guard exit code, the branch presence, the ADR counts — are deliberately **absent from this whole
> bundle**. That is what gives the probes teeth. Do not infer them; run the command. The "expected at
> generation" hints on the teeth probes are a **drift reference** so CC can detect movement between
> generation and check-time — the pass criterion is **"answered from the live source,"** never
> "matches the remembered number."
>
> **Filled supplement.** `SUPPLEMENT.md` was **FILLED** by the operator from the outgoing ai-council
> architect chat — its ANSWERS are folded into `PASTE_THIS.md` (the research-mode-authoring priority +
> the two operational flags), so the §13(d) operator-context beat **NARROWS** to *"anything changed
> since the supplement was written?"* — **not** a FULL re-ask.

## P1 — Orientation (the architect's **first move**, before any mechanism — v5.3 §13c)

A plain-language "what is ai-council" is **summary-bluffable** and so fails §5's own bar; a copy of
VISION into the handoff is barred (§2/§3). So orientation is a **forced exact-line read**: the line
enters the session **only** by CC reading the **live** primary source, and the quote must match as a
**substring** (never a paraphrase). The browser has no files → it replies **"run `<command>`"**; CC
reads live and substring-checks. The grep is a **tool** that confirms the frame — **the backlog
navigates** (v5.3 §13c), not this read.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1a | Quote, **substring-exact**, the **opening sentence** of `ai-council/VISION.md` `## Vision` — *what ai-council is*. | `VISION.md` `## Vision` (near line 14) | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of `ai-council/ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *the multi-model debate/research CLI + its role as the ecosystem's ADR-producing mechanism*. | `ARCHITECTURE.md` `## Purpose [CORE]` (near line 14) | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+3p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read live
by CC, substring-matched. **Then, before design, the operator-context beat fires (v5.3 §13d):** the
browser asks the operator for **off-repo** context. The supplement is **FILLED** (its ANSWERS are in
the paste — the research-mode-authoring priority + operational flags), so the beat **NARROWS** to
*"anything changed since the supplement was written?"* — **not** a FULL re-ask.

## Teeth probes (state fidelity — same contract; run in the ai-council checkout)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many tests does ai-council's suite collect **right now**? | live pytest ∩ `tests/` | the count drifts on any test change; a summary rounds/omits it — **expected at generation: 413 collected** | `python -m pytest --collect-only -q \| tail -1` |
| P3 | What is ai-council's current **short HEAD sha**, is the working tree clean, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time sha + sync-state — **at generation: HEAD `2675394`, tree clean, `main` in sync with `origin/main`; re-derive, don't trust this line** | `git rev-parse --short HEAD` then `git status -sb` |
| P4 | What is the **date of `JOURNAL.md`'s newest entry**, what is the **date of the newest first-parent merge on `main`**, and **do they match**? | `JOURNAL.md` ∩ live git | **THIS is the §1 headline drift:** at generation the JOURNAL's newest entry is `2026-06-03` but the newest first-parent merge is `2026-07-01` → **they DIVERGE (~4 weeks unjournaled)**. The live answer is the only ground truth; the dates are absent from the bundle | `grep -m1 '^### 2026' JOURNAL.md` (newest entry header) vs `git log --first-parent -1 --format=%cs` |
| P5 | Is the **methodology floor ARMED and INTACT** — does the hash-guard exit 0, and is `CLAUDE-FLOOR.md` `@`-included in `CLAUDE.md`? | `.claude/check_floor_hash.py` ∩ `CLAUDE.md` | "armed" is a runtime property (guard exit code) a summary cannot assert — **expected: guard exits 0; `@.claude/CLAUDE-FLOOR.md` on `CLAUDE.md` line 7** | `python .claude/check_floor_hash.py; echo "exit=$?"` then `grep -n 'CLAUDE-FLOOR' CLAUDE.md` |
| P6 | Is the **`feat/floor-arming` branch** still present (merged into `main` but not deleted)? | live git | branch-state is live and drifts the moment the operator runs `git branch -d` — **expected: present at generation (a cleanup straggler)** | `git branch --merged main \| grep floor-arming` (empty output = deleted since generation) |
| P7 | How many `ADR-NN-*.md` files are in `docs/decisions/`, and how many ADR rows does the index `docs/decisions/README.md` table list — **do they match**? | `docs/decisions/` listing ∩ `README.md` | a summary may "remember" a stale count; the live listing + index are the only ground truth — **expected: 8 files (ADR-01…08) but the index lists only ADR-01…07 → ADR-08 MISSING from the index** (minor drift #1) | `ls docs/decisions/ADR-*.md \| wc -l` vs the ADR rows in `docs/decisions/README.md` |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d)** — **NARROWED** to *"anything changed
   since the supplement was written?"* (the supplement is FILLED, ANSWERS folded into the paste), not a
   FULL re-ask, before design. Then run P2–P7, each against **live ai-council state now** (not
   generation-time), **from the ai-council checkout**.
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
4. Probes P2–P7 are *expected to move* between generation and check-time — that is the design. **P4 is
   the headline: expected to DIVERGE (JOURNAL `2026-06-03` vs git `2026-07-01`)** — but the pass
   criterion is **"answered from the live source,"** never "matches the dates the summary remembered."
   **P2** is expected to read **413**. **P5** pins the floor as **ARMED** (guard exit 0). **P6/P7**
   pin the two standing cleanup drifts (straggler branch; ADR-08 not in the index) — expected present
   at generation, and their disappearance is the *correct* live answer if the operator has since fixed them.
