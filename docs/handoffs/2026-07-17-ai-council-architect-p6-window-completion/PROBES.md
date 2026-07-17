# Probe manifest — ai-council P6 window completion: anti-bluff teeth (HANDOFF_PROCESS §5)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and **no answer**. The browser has no file access, so for every probe it must reply **"run `<command>`"** — surfacing the off-bundle dependency instead of bluffing it. **CC** runs each command against **live state at check-time IN THE ai-council checkout**, re-derives ground truth, and records PASS/FAIL. **Any FAIL blocks onboarding.** Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor; a tool absent → *skipped* (degraded coverage visible), never a synthesized pass.
>
> **Anti-bluff (HANDOFF_PROCESS §5 — a probe that bakes its answer is bluffable, rejected).** This manifest **withholds every answer value** by construction: no SHAs, counts, phase-table text, or armed-state are stated. That withholding IS the teeth. The pass criterion is **"answered from the live source at check-time,"** never "matches a remembered value." The validator `scripts/verify_handoff_probes.py` FAILs any probe row that bakes an answer hint.
>
> **Cross-repo note.** This bundle lives in the hub; its probes bind to **ai-council** — run them in the ai-council checkout. The hub-side `verify_handoff_probes.py` structurally confirms each probe binds to a resolvable target + a value-bearing command; the RECEIVER obtains the live values.

## Teeth probes (state fidelity — answers deliberately withheld, §5)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1 | What is the current **short HEAD sha**, which **branch** is checked out, is the tree clean, and how far **ahead of / behind** `origin`? | live git (the ai-council checkout) | the summary holds a generation-time state; the #26 close + session-wrap already moved HEAD past the merges this residual names — a baked sha goes stale | `git rev-parse --short HEAD` then `git status -sb` |
| P2 | How many **themes / stories / tasks** does `validate_backlog` count in this repo's `BACKLOG.md` right now, and does it report `OK` with zero warnings? | ai-council `BACKLOG.md` story-map ∩ `scripts/validate_backlog.py` | the story-map moved this session (wave tasks #16/#25/#26 struck; #33/#34/#35 + new story [S13]/#36–#38 filed) — neither the counts nor the OK/FAIL verdict appears in this bundle | `python scripts/validate_backlog.py` |
| P3 | Are this repo's git hooks **armed** — do `pre-commit`, `commit-msg`, and `pre-push` exist under `.git/hooks/`, and is `core.hooksPath` unset? (SessionStart `pre-commit install` arms all three.) | the ai-council checkout's armed git-hook stubs under `.git/hooks/` | armed-state is a live filesystem fact absent from any summary; a relic `core.hooksPath` or a fresh clone silently disarms every gate (n=2 fleet incident) | `ls .git/hooks/pre-commit .git/hooks/commit-msg .git/hooks/pre-push` then `git config core.hooksPath` |
| P4 | Quote, **substring-exact**, the **P6 row** of the phase → task map in the plan-of-record — the window-completion pair (ADR-11 deviation closure → its task ids) — confirming the ready-slack scope is read from the frozen primary source, not paraphrased from this bundle. | ai-council `docs/intake/2026-07-16-plan-of-record.md` §4 "Phase → task map" table | the frozen phase-table rows are byte-fixed in the plan-of-record; a summary paraphrases the P6 scope and cannot reproduce the exact `P6 \| … \| **#nn**` row text; the bundle states none of it | `grep -n "P6" docs/intake/2026-07-16-plan-of-record.md` → the browser's quote must be a substring of a live `\| P6 \|` row |

## Gate procedure (CC)

1. **P4 first** — the forced phase-table read orients the session: it anchors the window-completion scope (ADR-11 D2 parity → #22/#23) in the frozen primary source before design begins. **Then run the §13(d) operator-context beat NARROWED** (the supplement is FILLED — ask only *"anything changed since it was written?"*). Then P1–P3, each against **live ai-council state now**.
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing / command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary source → CC re-derives the fact → abort if still unmet).
4. Answer values are deliberately absent (§5): the pass criterion is **"answered from the live source,"** never "matches a remembered value." P1's HEAD/branch is designed to move — re-derive it live, do not trust the residual's prose.
