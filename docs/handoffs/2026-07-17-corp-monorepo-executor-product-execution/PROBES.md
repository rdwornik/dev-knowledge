# Probe manifest — corp-monorepo executor: anti-bluff teeth (HANDOFF_PROCESS §5)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and **no answer**. The browser has no file access, so for every probe it must reply **"run `<command>`"** — surfacing the off-bundle dependency instead of bluffing it. **CC** runs each command against **live state at check-time IN THE corp-monorepo checkout**, re-derives ground truth, and records PASS/FAIL. **Any FAIL blocks onboarding.** Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor; a tool absent → *skipped* (degraded coverage visible), never a synthesized pass.
>
> **Anti-bluff (HANDOFF_PROCESS §5 — a probe that bakes its answer is bluffable, rejected).** This manifest **withholds every answer value** by construction: no SHAs, counts, quote text, or armed-state are stated. That withholding IS the teeth. The pass criterion is **"answered from the live source at check-time,"** never "matches a remembered value." The validator `scripts/verify_handoff_probes.py` FAILs any probe row that bakes an answer hint.
>
> **Cross-repo note (ADR-36/41).** This bundle lives in the hub; its probes bind to **corp-monorepo** (the session-header `Target repo` row) — run them in the corp checkout. The hub-side `verify_handoff_probes.py` resolves each probe's source/command target against the corp sibling root and structurally confirms it binds to a resolvable target + a value-bearing command; the RECEIVER obtains the live values.

## Teeth probes (state fidelity — answers deliberately withheld, §5)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1 | What is the current **short HEAD sha**, which **branch** is checked out, is the tree clean, and how far **ahead of / behind** `origin`? | live git (the corp-monorepo checkout) | the summary holds a generation-time state; a fresh arc merges move HEAD, so any baked sha is already stale | `git rev-parse --short HEAD` then `git status -sb` |
| P2 | How many **themes / stories / tasks** does `validate_backlog` count in this repo's `BACKLOG.md` right now, and does it report `OK`? | corp `BACKLOG.md` story-map ∩ `scripts/validate_backlog.py` | the story-map counts drift on any BACKLOG edit as tasks close; neither the counts nor the OK/FAIL verdict appears in this bundle | `python scripts/validate_backlog.py BACKLOG.md` |
| P3 | Are this repo's git hooks **armed** — do `pre-commit`, `commit-msg`, and `pre-push` exist under `.git/hooks/`? (SessionStart `pre-commit install` arms all three.) | the corp checkout's armed git-hook stubs under `.git/hooks/` | armed-state is a live filesystem fact absent from any summary; a relic `core.hooksPath` or a fresh clone silently disarms every gate (n=2 fleet incident) | `ls .git/hooks/pre-commit .git/hooks/commit-msg .git/hooks/pre-push` |
| P4 | Quote, **substring-exact**, the **NOT-list** line inside §3 of the execution charter — the three infrastructure tiers ruled out at solo-operator scale — confirming the integration-protocol ruling is materialized, not paraphrased. | corp `docs/audits/2026-07-17-execution-charter.md` §3 (Protocol ruling) | the NOT-list wording is byte-fixed in the charter; a summary paraphrases it and cannot reproduce the substring | `grep -n -A2 "NOT-list" docs/audits/2026-07-17-execution-charter.md` → the quote must be a substring of the live line |

## Gate procedure (CC)

1. **P4 first** — the forced charter-§3 read orients the session (confirms the integration-protocol ruling — R2/R6/T6/N2 + the NOT-list — is materialized before any arc opens). **Then run the §13(d) operator-context beat FULL** (the supplement is empty — nothing to narrow against). Then P1–P3, each against **live corp state now**.
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing / command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary source → CC re-derives the fact → abort if still unmet).
4. Answer values are deliberately absent (§5): the pass criterion is **"answered from the live source,"** never "matches a remembered value." P1's HEAD/branch is designed to move as arcs merge — re-derive it live, do not trust the residual's prose.
