# Probe manifest — epic mode: boundary-scoped teeth (HANDOFF_PROCESS §5 + §14a)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and
> **no answer** (HANDOFF_PROCESS §5). The epic chat has no file access — for every probe it
> replies **"run `<command>`"**; CC runs each command against **live state at check-time**,
> re-derives ground truth, and records PASS/FAIL. **Any FAIL blocks the lane boot.** Degrade
> loudly (§10): a moved anchor → WARN `anchor-missing`, re-anchor; tooling absent → reported
> *skipped* (degraded coverage visible), never counted as pass.
>
> **Branch note.** This bundle was generated on branch `docs/2026-07-05-wave2-prep`; the lane works
> `epic/llm-first-docs`. This line names only *which* branch to compare against — **re-derive the
> live branch / HEAD / tree (E1); do not trust this line.**

## Teeth probes (boundary-scoped — answers deliberately withheld, §5)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| E1 | What is the current **short HEAD sha**, which **branch** is checked out (it must be the epic branch), and is the working tree **clean**? | live git | the generation-time state moves with every story commit; a summary holds a stale sha | `git rev-parse --short HEAD` then `git branch --show-current` then `git status -sb` |
| E2 | Quote, **substring-exact**, the opening sentence of the `protocols/HANDOFF_PROCESS.md` §14 body — the governing contract for this lane. | `protocols/HANDOFF_PROCESS.md` §14 | a paraphrase of the lane contract is not a substring; the live spec is the only ground truth | `grep -A8 '^## 14\.' protocols/HANDOFF_PROCESS.md` → the quote must be a substring of the live section |
| E3 | Which paths does the epic branch touch **right now**, and is **every** path inside the FILE-BOUNDARY declared in `docs/handoffs/2026-07-05-dev-knowledge-epic-llm-first-docs/EPIC_BOOT.md`? | live git ∩ `docs/handoffs/2026-07-05-dev-knowledge-epic-llm-first-docs/EPIC_BOOT.md` | the touched-path set grows with every commit; the boundary verdict is computable only from the live diff | `git diff --name-only main...HEAD` compared against the EPIC_BOOT FILE-BOUNDARY section |
| E4 | Does `audit.py ship-gate` come back **GREEN or RED** on this branch right now, and **how many WARNs are dispositioned**? | live git ∩ `scripts/audit.py` | computed at answer-time over live git; any commit can re-RED it; the values are absent from this bundle | `python scripts/audit.py ship-gate` (read the final verdict + the disposition count) |
| E5 | Which files does this **epic bundle** carry, and is `EPIC_RETURN.md` still the unfilled skeleton or already filled by the lane? | `docs/handoffs/2026-07-05-dev-knowledge-epic-llm-first-docs/` listing | the fill-state flips when the lane closes; a summary holds a stale bundle shape | `ls docs/handoffs/2026-07-05-dev-knowledge-epic-llm-first-docs/` then `grep -c '^## ' docs/handoffs/2026-07-05-dev-knowledge-epic-llm-first-docs/EPIC_RETURN.md` (skeleton section count vs filled content) |

## Gate procedure (CC)

1. Run E1–E5 against **live state now**; record **PASS** (live ground truth obtained and
   consistent) or **FAIL** (anchor missing / command errored / receiver answered from memory
   or this bundle) for each.
2. **Any FAIL → do not boot the lane**; route through the §10 escalation ladder (re-read the
   named primary source → CC re-derives the fact → abort if still unmet).
3. **E3 is continuous, not once**: re-run it at every story commit and again at EPIC RETURN
   (the §14b merge-readiness checklist) — the boundary is audited for the life of the lane.
