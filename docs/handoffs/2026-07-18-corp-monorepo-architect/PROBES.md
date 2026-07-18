# Probe manifest — corp-monorepo architect (2026-07-18): anti-bluff teeth (HANDOFF_PROCESS §5)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and **no answer**. The browser has no file access, so for every probe it must reply **"run `<command>`"** — surfacing the off-bundle dependency instead of bluffing it. **CC** runs each command against **live state at check-time IN THE corp-monorepo checkout**, re-derives ground truth, and records PASS/FAIL. **Any FAIL blocks onboarding.** Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor; a tool absent → *skipped* (degraded coverage visible), never a synthesized pass.
>
> **Anti-bluff (HANDOFF_PROCESS §5 — a probe that bakes its answer is bluffable, rejected).** This manifest **withholds every answer value** by construction: no SHAs, counts, region text, or armed-state are stated. That withholding IS the teeth. The pass criterion is **"answered from the live source at check-time,"** never "matches a remembered value." The validator `scripts/verify_handoff_probes.py` FAILs any probe row that bakes an answer hint.
>
> **Cross-repo note.** This bundle lives in the hub `.dev-knowledge`; its probes bind to **corp-monorepo** — run them in the corp checkout (`../corp-monorepo` from the hub, or the corp working directory). The hub-side `verify_handoff_probes.py` structurally confirms each probe binds to a resolvable target + a value-bearing command; the RECEIVER obtains the live values.

## Teeth probes (state fidelity — answers deliberately withheld, §5)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1 | What is the current **short HEAD sha**, which **branch** is checked out, is the tree clean, and how far **ahead of / behind** `origin`? | live git (the corp-monorepo checkout) | the summary holds a generation-time state; corp closed a product window (Arc-B/Arc-C-W1/E5-design merges + a closing sweep) and the next arc will move HEAD, so any baked sha is already stale | `git rev-parse --short HEAD` then `git status -sb` |
| P2 | How many **themes / stories / tasks** does `validate_backlog` count in this repo's `BACKLOG.md` right now, and does it report `OK`? | corp `BACKLOG.md` product story-map (E1–E7, R10 sequence) ∩ `scripts/validate_backlog.py` | the story-map counts drift on any BACKLOG edit (the closing sweep folded audit note-refs onto #17/#28/#34/#45); neither the counts nor the OK/FAIL verdict appears in this bundle | `python scripts/validate_backlog.py BACKLOG.md` |
| P3 | Are this repo's git hooks **armed** — do `pre-commit`, `commit-msg`, and `pre-push` exist under `.git/hooks/`? (SessionStart `pre-commit install` arms all three.) | the corp checkout's armed git-hook stubs under `.git/hooks/` | armed-state is a live filesystem fact absent from any summary; a relic `core.hooksPath` or a fresh clone silently disarms every gate (n=2 fleet incident) | `ls .git/hooks/pre-commit .git/hooks/commit-msg .git/hooks/pre-push` |
| P4 | Quote, **substring-exact**, the first content line inside the `owner=hub` region `conventions-commit-branch` of this repo's `CLAUDE.md` — confirming the hub methodology is materialized **verbatim**, not paraphrased. | corp `CLAUDE.md` region `<!-- methodology:start id=conventions-commit-branch owner=hub -->` | the owner=hub region text is byte-fixed from the hub template (`templates/claude-regions/`); a summary paraphrases it and cannot reproduce the substring | `grep -n -A4 "methodology:start id=conventions-commit-branch" CLAUDE.md` → the quote must be a substring of the live region |

## Gate procedure (CC)

1. **P4 first** — the forced CLAUDE-region read orients the session (confirms the hub methodology layer is materialized verbatim; corp is A0-closed) before product planning resumes. **Then run the §13(d) operator-context beat FULL** (the supplement is empty — nothing to narrow against). Then P1–P3, each against **live corp state now**.
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing / command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary source → CC re-derives the fact → abort if still unmet).
4. Answer values are deliberately absent (§5): the pass criterion is **"answered from the live source,"** never "matches a remembered value." P1's HEAD/branch is designed to move (the next product arc) — re-derive it live, do not trust the residual's prose.
