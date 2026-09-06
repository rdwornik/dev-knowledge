---
intake-id: 76
status: DRAFT
origin: Layer-1 browser seat, INBOX-dev-knowledge-2026-09-06-031, as amended by 032 and RULED by DECLARE-BROWSER-TOPOLOGY-2026-09-06 (032 ACCEPTED; 031 section 1 withdrawn; sections 2-3 stand); filed and then amended by filings-N under that ruling's own "For filings" line. Ratification with 031.
consumed-by:
---

# The browser window's shape, and "no decision without a carrier"

> **Filing note -- section 1 below is a RULING, not a proposal.**
> `DECLARE-BROWSER-TOPOLOGY-2026-09-06` accepted **032**: one chat per window with the model
> switched per act. **031's two-chat table is WITHDRAWN**; its sections 2 and 3 stand. Section 1
> here carries the ruling's text, per that file's own "For filings" instruction. The intake as a
> whole is still **DRAFT** -- the ruling says *"Ratification with 031."*
>
> **`carried-by:` is recorded in the body, deliberately NOT as a frontmatter key.** The ruling
> fills its own `carried-by:` line (`docs/intake/` 031 candidate, `OPERATOR-INTERFACE` section 2,
> #68 floor item six) and directs filings to carry it. It is written into section 2 below instead
> of the frontmatter because **the intake frontmatter schema is a join key** -- an added key REDs
> the tree manifest. The carrier is recorded, not the schema changed.
>
> `intake-id` **76**, allocated per **D8** (next-free across ALL refs) -- checked against the 11
> content-bearing refs in this clone, not `main` alone. Ids **14 and 70 remain live duplicates on
> `main`**, untouched here: both files are landed, so which one moves is an operator call. See
> intake #75 and `QUESTION-filings.md` Q-3.

## 1 - The window's shape (RULED)

**ONE chat per window, with the model switched per act.** The split is by ACT, not by topic:

| Class | Acts | Model |
|---|---|---|
| Ruling | `DECLARE-*`, contract freezes (`BATCH-*`), amendments (`AMEND-*`), GO, plan review, packet reads at a milestone | Fable |
| Routine | pastes and re-pastes, "check" / "what do I paste", `RULING-RELAY` routing, `QUESTION-*` triage, FREEZE, LEDGER refresh, transport hygiene | Opus / Sonnet |

**Why the simpler shape won, in the ruling's own words:** *cost = context LENGTH, not chat count; a
second chat buys nothing the turn budget does not, and adds synchronisation the operator pays for.*
No failure case was shown for one chat, so the two-chat proposal drew no pushback -- it was simply
the more expensive way to get the same property.

### The three sharpenings (conditions of the ruling, not objections to it)

1. **The switch line is fixed text and carries the price.** Whenever an act enters the ruling class
   the browser emits exactly:

   ```
   RULING AHEAD - switch to Fable, type `rule` (est. ~N k tokens: <files it will read>)
   ```

   A ruling emitted on a non-Fable model **without** that line, or a switch line **without** a
   cost, is a form-probe defect.
2. **A ruling turn reads FILES only.** The switch line names them; the turn does not read chat
   history for premises. That is what keeps a Fable turn near its estimate -- and it is the clause
   that makes the estimate meaningful rather than decorative.
3. **Wrap is mechanical, not felt.** LEDGER carries `turns this window: N/40`; at 40, or at the
   sitting's close, the browser emits the wrap line, and the next window boots from bundle +
   LEDGER.

**Scorecard:** turns per browser window; **Fable turns per window, target 10 or fewer**; bytes read
via connector per window.

**Routing rule, unchanged:** when a routine act meets a decision it writes
`to-browser/QUESTION-browser-ops.md` and stops; the ruling act answers with a DECLARE. Neither is
fed CC transcripts (inbox 030).

**Two chats survive only as the WRAP shape** -- when a window grows long, wrap it (handoff-lite:
LEDGER and STATUS are the state) and open a fresh one, rather than running a second chat in
parallel.

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

**Carriers named by `DECLARE-BROWSER-TOPOLOGY-2026-09-06`** (its own `carried-by:` line, recorded
here per its "For filings" instruction): this intake (the 031 candidate), `OPERATOR-INTERFACE`
section 2, and **#68 floor item six**.

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
