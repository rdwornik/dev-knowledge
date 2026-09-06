---
intake-id: 76
status: DRAFT
origin: Layer-1 browser seat, INBOX-dev-knowledge-2026-09-06-031 ("browser proposes, operator ratifies"; depends 029, 030) AS AMENDED BY INBOX-dev-knowledge-2026-09-06-032, which replaced 031's two-chat shape with one chat and a per-act model switch; filed by filings-N under 031's own owner-role line
consumed-by:
---

# The browser window's shape, and "no decision without a carrier"

> **Filing note -- this intake records 031 AS AMENDED, not 031 as written.** Item 032 landed while
> this file was being drafted and before it was committed. It keeps most of 031 and **replaces its
> headline proposal**: not two parallel chats, but ONE chat per window with the model switched per
> act. Filing 031 verbatim would have filed a superseded shape, so the amendment is folded in and
> the divergence is shown in section 1 rather than smoothed away.
>
> `intake-id` **76**, allocated per **D8** (next-free across ALL refs) -- checked against the 11
> content-bearing refs in this clone, not `main` alone. Ids **14 and 70 remain live duplicates on
> `main`**, untouched here: both files are landed, so which one moves is an operator call. See
> intake #75 and `QUESTION-filings.md` Q-3.

## 1 - The window's shape

**The split is by ACT, not by topic** (031, kept by 032):

| Class | Acts | Model |
|---|---|---|
| Ruling | `DECLARE-*`, contract freezes (`BATCH-*`), amendments (`AMEND-*`), GO, plan review (select / paste / approve), packet reads at a milestone, one deliberate read of a decisive document | Fable |
| Routine | pastes and re-pastes, "check" / "what do I paste", `RULING-RELAY` routing, `QUESTION-*` triage, FREEZE, LEDGER refresh from STATUS files, transport hygiene | Opus / Sonnet |

**031 proposed two parallel chats. 032 replaced that with ONE chat per window**, because
claude.ai switches the model inside a single conversation:

- default model Opus for routine acts;
- when an act enters the ruling class, the chat emits a fixed line -- *"this is a ruling — switch
  to Fable and type `rule`"* -- the operator switches, one expensive turn happens, the operator
  switches back;
- same context, same project memory, **nothing to synchronize**.

**Two chats survive only as the WRAP shape:** when a window grows long, wrap it (handoff-lite --
LEDGER and STATUS are the state) and open a fresh one, rather than running a second chat in
parallel.

> **The reasoning 032 supplies, and it is the part worth keeping:** *context LENGTH is the cost,
> not the number of chats.* A Fable turn is billed the whole context whichever chat it sits in, so
> a second chat buys nothing and costs the operator a synchronization problem. That is why the turn
> budget (about 40 turns, or one sitting) is unchanged by the amendment.

**Routing rule, unchanged from 031:** when the routine seat meets a decision it writes
`to-browser/QUESTION-browser-ops.md` and stops; the ruling act answers with a DECLARE. Neither is
fed CC transcripts (inbox 030).

**Enforcement proposed for the switch itself:** a form-probe predicate -- a ruling emitted without
the switch line, on a non-Fable model, is a defect -- and the bundle's supplement records which
turns ran on which model. Scorecard: **Fable turns per window, target 10 or fewer**.

## 2 - No decision without a carrier

Extends rule 1 of inbox 029 (*a browser decision exists only as a file*) with the mechanism. Kept
in full by 032:

1. Every `DECLARE-*` / `AMEND-*` / `BATCH-*` file carries a **`carried-by:`** line naming the repo
   home that will hold it -- an intake path, an ADR, a JOURNAL entry, a PLAYBOOK section, a
   `STANDING_RULINGS` row. Filings fills it at wrap; **empty means the file is not yet a decision
   of record**.
2. `/handoff-verify` gains probe **P11 - decision carriage**: every `DECLARE-*` / `AMEND-*` /
   `BATCH-*` written during the window has a `carried-by:` that resolves on `main`, or is named in
   the bundle's residual as OPEN. A missing carrier FAILS the probe, and **the window cannot close
   with a homeless decision**.
3. The browser floor (#68) lists **six** irreducible items: role/loop, where truth is, equilibrium
   contract, operator rights, session topology, and **decisions are files with a carrier**.
4. LESSONS line: *"A browser sentence is a proposal; a file with a carrier is a decision."*

## 3 - Token rules that become mechanism (from inbox 030)

- `STATUS-*` at or under 5 KB with a "now" section on top -- checked by a transport-grammar check
  at `/handoff-verify` P8 (size plus first heading), rather than by prose.
- The browser reads LEDGER / STATUS / QUESTION / `DIGEST-*` only; RATIFICATION files and lane
  packets are read by CC and delivered as `DIGEST-<date>.md` (a new entry in the 017 grammar table).
- Scorecard lines: turns per browser window, and bytes read via connector per window.

## 4 - What this seat did NOT do, and why

**Nothing in sections 1-3 was applied.** 031 names the operator as ratifier, and three of its
clauses would otherwise have been implemented by the filing seat on its own authority:

- **`carried-by:` was NOT retro-filled** onto the window's `DECLARE-*` / `AMEND-*` / `BATCH-*`
  files. The clause says filings fills it at wrap -- but the clause is unratified, and back-filling
  would make the mechanism look adopted, which is the one thing a DRAFT should not do.
- **No two-chat table was added to `OPERATOR-INTERFACE.md` §2**, and after 032 that is doubly
  right: the table 031's done-when asked for describes a shape the next item replaced. What §2
  already carries is the one-line version from inbox **030**, which was gate-free and therefore
  live.
- **P11, the six-item floor and the form-probe predicate are other seats' carriers** (the handoff
  build behind #68), recorded here so the ratifying reader sees the whole shape.

> **The distinction being protected.** Inbox 030 arrived `gate: none` and was carried into
> `OPERATOR-INTERFACE` §2 the same hour. 031 arrived saying the operator ratifies, and was filed
> and left alone -- and within the hour 032 amended its headline clause. Same seat, same window,
> opposite handling, and the second case is why: **had 031 been applied on arrival, the amendment
> would have had to undo landed work instead of editing a draft.**

**Done-when (031's own, unchanged by 032):** intake ratified; `carried-by:` present on every
DECLARE / AMEND / BATCH of the 2026-09-06 window; P11 exists and passes on the next handoff; the
#68 floor lists six items; `OPERATOR-INTERFACE` §2 carries the window-shape table.
