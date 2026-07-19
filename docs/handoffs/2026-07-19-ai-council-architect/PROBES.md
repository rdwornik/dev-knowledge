# Probe manifest — ai-council architect: orientation first, then teeth (HANDOFF_PROCESS §5 + §13c)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and **no
> answer**. The browser has no file access, so for every probe it must reply **"run `<command>`"** —
> surfacing the off-bundle dependency instead of bluffing it. **CC** runs each command against **live
> state at check-time**, re-derives ground truth, and records PASS/FAIL. **Any FAIL blocks
> onboarding.** Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor (never a synthesized
> pass); git/tooling absent → reported *skipped* (degraded coverage visible), never counted as pass.
>
> **Anti-bluff (HANDOFF_PROCESS §5 — a probe that bakes its answer is bluffable, rejected).** This
> manifest **withholds every answer value** by construction: no counts, SHAs, dates, verdicts, task-line
> text, or orienting lines are stated. That withholding IS the teeth. The pass criterion is **"answered
> from the live source at check-time,"** never "matches a remembered number."
>
> **CROSS-REPO — run these in the ai-council checkout (load-bearing).** This bundle is *hosted* in the
> hub (`.dev-knowledge`, ADR-36/41 read-only-on-target) but its **subject is `ai-council`**. Every command
> below runs in the **ai-council** working copy. The probes are re-bound to ai-council's own surfaces
> (`scripts/validate_backlog.py`, `scripts/check.ps1`, its `BACKLOG.md` / `VISION.md` / `ARCHITECTURE.md`);
> the hub's `audit.py ship-gate` / `ALL_CHECKS` / `doc-counts` / disposition-register probes are
> **deliberately absent** — ai-council carries no such surfaces, so a hub-bound probe would FAIL
> `anchor-missing` by construction rather than testing anything.
>
> **Branch note.** This bundle was cut on hub branch `docs/ai-council-architect-handoff`. That names only
> where the *artifact* lives — **re-derive ai-council's HEAD / tree / branch / ahead-behind live (P2); do
> not trust this line.**
>
> > **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

## P1 — Orientation (the architect's **first move**, before any mechanism — §13c)

A plain-language "what is this project" is **summary-bluffable** and so fails §5's own bar; a copy of
VISION into the handoff is barred (§2/§3). So orientation is a **forced exact-line read**: the line
enters the session **only** by CC reading the **live** primary source, and the quote must match as a
**substring** (never a paraphrase). The browser has no files → it replies **"run `<command>`"**; CC
reads live and substring-checks. The grep is a **tool** that confirms the frame — **the backlog
navigates** (§13c), not this read.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1a | Quote, **substring-exact**, the **opening sentence** of ai-council `VISION.md` `## Vision` — *what ai-council is*. | ai-council `VISION.md` `## Vision` | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of ai-council `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *what the system does*. | ai-council `ARCHITECTURE.md` `## Purpose [CORE]` | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read live
by CC, substring-matched. **Then, before design, the operator-context beat fires (§13d):** the browser
asks the operator for **off-repo** context.
This bundle's supplement is **generated EMPTY**, so the beat fires **FULL** — *"what off-repo context: intent, priorities, findings not in the repo, changed decisions?"* — not a narrowed "anything changed since?". (If the operator runs `supplement filled`, its ANSWERS fold in and the beat narrows.)

## Teeth probes (state fidelity — same contract; **answers deliberately withheld, §5**)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | What is ai-council's current **short HEAD sha**, is the working tree clean, which **branch** is checked out, and how far **ahead of / behind** `origin` is it? | live git (the **ai-council** checkout) | the summary holds a generation-time state; this window closed with merges still landing, so a baked sha is stale on arrival | `git rev-parse --short HEAD` then `git status -sb` |
| P3 | How many **themes / stories / tasks** does `validate_backlog` count in ai-council's `BACKLOG.md` right now, and does it report `OK` with zero warnings? | ai-council `BACKLOG.md` story-map ∩ `scripts/validate_backlog.py` | the story-map moved hard this window (#33 struck, #44 closed, #69–#72 filed, #68 re-prioritized) — neither the counts nor the OK/FAIL verdict appears in this bundle | `python scripts/validate_backlog.py` |
| P4 | Quote, **substring-exact**, the two **P2 silent-failure task lines — #69 and #71** — including their bracketed priority/size tags, confirming the ready slack is read from the live story-map and not paraphrased from this bundle. | ai-council `BACKLOG.md` story-map (#69, #71) | both lines were authored *after* the compaction window and are byte-fixed in the live file; a summary paraphrases the pair and cannot reproduce the exact `- [#69] …` / `- [#71] …` text; this bundle states none of it | `grep -nE '^- \[#(69\|71)\]' BACKLOG.md` → the browser's quote must be a substring of a live matched line |
| P5 | Are ai-council's git hooks **armed** — do `pre-commit`, `commit-msg`, and `pre-push` exist under `.git/hooks/`, and is `core.hooksPath` unset? | the ai-council checkout's armed git-hook stubs under `.git/hooks/` | armed-state is a live filesystem fact absent from any summary; a relic `core.hooksPath` or a fresh clone silently disarms every gate (n=2 fleet incident) | `ls .git/hooks/pre-commit .git/hooks/commit-msg .git/hooks/pre-push` then `git config core.hooksPath` |
| P6 | Does the repo gate pass **right now** — what does `check.ps1` **exit**, how many tests pass, and does `mypy src/` report clean? | ai-council `scripts/check.ps1` (pytest + mypy + ruff) | the pass-count and the mypy verdict are live build facts that drift on any merge; the `types-PyYAML` declaration landed *this* window, so the green claim is exactly what must be re-derived rather than trusted — the residual states neither value | `pwsh -File scripts/check.ps1` (or `py -m pytest -q` then `py -m mypy src/`) → read the exit code + the counts |
| P7 | **BACKLOG grooming (operator ruling 2026-07-17).** For **every OPEN item** in ai-council's `BACKLOG.md`, is each still **live** (actively in-progress), **dead** (superseded / obsoleted / already-shipped — a grooming close per ADR-65), or **awaiting-ruling** (blocked on an operator / Council decision)? The successor grooms the **whole open set** at boot — no open `#id` passes unreconciled. | ai-council `BACKLOG.md` ∩ `scripts/validate_backlog.py` ∩ live git | the live / dead / awaiting-ruling status of each open item is an at-boot judgment over current git ∩ `BACKLOG.md`; a summary holds a stale snapshot and cannot tell a still-live item from one already shipped or superseded | `python scripts/validate_backlog.py` then `git log --first-parent --oneline main` to cross-check each open `#id` against its closing merge |

## Gate procedure (CC)

1. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then P4**, which anchors this window's ready slack (#69/#71) in the live
   story-map. **Then the operator-context beat (§13d), FULL** (the supplement is generated empty).
   Then P2, P3, P5, P6, P7 — each against **live ai-council state now**.
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
4. Probes P2–P7 are *designed to move* between generation and check-time — that is the point. **Answer
   values are deliberately absent (§5)**: the pass criterion is **"answered from the live source,"**
   never "matches a remembered number." P6 is the headline gate (exit code + test count + mypy verdict);
   P7 grooms the whole open BACKLOG at boot. First re-derive which branch is live (P2), then re-derive
   every load-bearing fact from the live primary source.
