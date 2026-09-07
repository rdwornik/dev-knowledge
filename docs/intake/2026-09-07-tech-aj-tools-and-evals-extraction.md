---
intake-id: 88
status: DRAFT
origin: browser architect seat, 2026-09-07 — `to-cc/AMEND-SWEEP-001.md` lane S-15; the still-open half of architect-inbox item 022-A, whose tool-by-tool table was never produced
consumed-by:
---

# The AJ corpus was mined at CLAIM level and never at TOOL level — the have/use/where table 022-A asked for does not exist

## Problem / motivation

**Honest premise, stated first because it is the whole reason this intake exists:** the AJ
catalogue (§2a, rows A-01…A-12) covered the 13 transcripts, 2 ebooks and 12 decks **at claim level
through prior arcs' locators**. The lane itself **never opened the 48 files** — a cloud session
cannot reach the operator's disk. The catalogue is therefore a second-hand read, and it is honest
about being one.

What 022-A asked for and is **still missing** is a different artifact: a **tool-by-tool /
eval-by-eval table** with *have / use / where*. Named inline across the corpus so far, never
tabulated:

- **Phoenix** — trace inspection
- **LiteLLM** — gateway / model routing
- **SlopCodeBench** — long-term modifiability
- **Opik** — `.opik-tracing-enabled`
- **LLM-judge + mechanical verifier pairs**
- *"measure token optimisation on your own usage"*
- **cost per command as an architecture signal**

Each is a name we have written down and never answered. Without the table, "did we already adopt
this?" is re-litigated every time one of these names comes up — which is exactly the cost the
catalogue was supposed to end.

## Scenarios (+1 view)

- As the operator, I ask "do we use Phoenix?" and read one row: named at *locator*, we have / do not
  have it, used at *these sites* or nowhere, and its token-cost relevance. No re-read of the corpus.
- As a lane, Gemini reads the 48 files and lists every tool / eval / service / practice named per
  file, **retrieval only, one locator per item**. CC then re-opens **every** locator; items whose
  locator does not resolve are counted as fabrications, not quietly dropped.
- As the token-bottleneck lane (S-14), I cross-check my mechanism list against what the course
  proposed — two independent derivations of the same question, disagreements listed rather than
  reconciled.
- As the operator, the lane runs **locally** and the corpus is **read, never committed** — the
  audit carries paraphrase plus locator only.

## Functional requirements

- **Must:**
  - Inputs: `C:\Users\1028120\Documents\Priv\Architekt Jutra` (48 files; the `.md` transcripts are
    canonical). **Read, never committed.** Paraphrase + locator only in the output.
  - Method: Gemini reads and lists every tool / eval / service / practice named per file
    (**retrieval only**, locator per item) → **CC re-opens every locator** → fabrications counted.
  - Columns: item · locator · **have** · **use** · **where** (answered by live hub reads, not by
    recall) · **token-cost relevance** — does it reduce our token spend, and how would we measure it.
  - Output `docs/audits/<date>-technical-aj-tools-evals-table.md`, plus candidates routed to the
    token lane.
  - **LOCAL substrate**, first local slot **after wave 2** — deferred at filing because local
    memory was critical at 838 MB, and because cloud cannot read the operator's disk at all.
- **Should:** cross-check against S-14's mechanism list, so an item the course proposed and we
  already do is visibly closed rather than re-proposed.
- **Could:** a standing refresh when the corpus grows — out of scope until the first table exists.

## Acceptance criteria (ex-ante)

1. Every one of the 48 files appears in the table's provenance list, **including files that yielded
   nothing** — an empty read is evidence, and an absent row is indistinguishable from an unread file.
2. Every row carries a locator that **CC re-opened**; the fabrication count is stated as a number,
   including when it is 0.
3. The seven items named above each have a `have / use / where` verdict, each answered by a live
   hub read cited in the row — recall is not an answer.
4. `gemini` unavailable is reported as **`fan-out: NONE`**, never as clean — the SWEEP rule applies
   unchanged.
5. No file from the corpus is committed; the diff contains the audit and nothing from `Priv`.
6. Disagreements with S-14's mechanism list are **listed**, not reconciled — two derivations talked
   into agreement are one derivation.

## Non-goals

- **Not an adoption.** The table says have / use / where; adopting anything is a separate intake and
  a separate ruling (ADR-112 Tier L, where a fit-assessment precedes adoption).
- **Not a re-read of §4.** Its closure counts were witnessed by the lane (45 rows, 31 two-sided, 22
  empty searches, 0 fabrications measured; no fan-out ran).
- **Not a claim-level re-derivation.** The catalogue's claim layer stands; this is the tool layer
  beneath it.
- **Not cloud-runnable.** Recorded so no later reader re-dispatches it and gets an empty read.

## Impact sketch (4+1 lite)

- **Logical:** one audit table; no organ, no schema, no gate.
- **Process:** Gemini-reads → CC-verifies → operator rules; the SWEEP's `fan-out` honesty rule binds.
- **Development:** none in-tree beyond the audit artifact and the candidates it routes.
- **Physical:** LOCAL only; the corpus lives on the operator's disk and is read in place.

## Open questions

1. Does the token-cost column need S-14's instrumentation to land first, or can it be qualitative
   at this pass and re-derived once cost per lane is a number (intake #83)?
2. What is the retention rule for the table when the corpus changes — regenerate, or amend?
3. Is `have` answered per repo or fleet-wide? A tool present in `win-tooling` and absent in the hub
   is not one answer.

## Status

DRAFT — filed 2026-09-07 by filings-N3 from `AMEND-SWEEP-001` S-15. Scheduled for the first LOCAL
slot after wave 2; not runnable on cloud. Awaiting technical-architect triage and ratification. No
carrier row (ADR-111 §2).
