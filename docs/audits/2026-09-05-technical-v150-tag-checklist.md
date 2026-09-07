# v1.5.0 tag checklist — five gates, filled as witnesses land

<!-- scope: meta -->

Consumers: architect inbox item 012-C, which specifies these five gates; `CLAUDE.md` §12's pointer
ledger and inbox item 012-A, which file the gate (2) note below.

> **Status: NOT EXECUTED.** This file is the checklist, not the tag. It is created empty-by-design
> and filled as each witness lands. **The operator declares the tag on this checklist** — no seat
> flips it, and a gate is not satisfied because the work behind it looks done. Nothing here closes
> a row or authorises a release.
>
> **Ownership gap, recorded rather than assumed.** Inbox item 012 names FILINGS-1 for 012-A and the
> integrator for 012-B; **012-C names no owner.** This file exists because 012-A step 3 instructs
> that its ESSENTIALS deferral be filed *in the 012-C checklist*, and the checklist did not exist.
> Creating the container is not claiming the item — gates (1), (3), (4) and (5) are unowned and need
> an operator word.

---

## The five gates

| # | Gate | Witness | State |
|---|---|---|---|
| 1 | ship-gate reports 0 hard-fail and 0 undispositioned at `main` | — | OPEN |
| 2 | `CLAUDE.md` first-read ESSENTIALS line removed in the release commit (`[#628]` closure) | see note below | OPEN — deferral recorded |
| 3 | doc-counts in sync via the commit-gate derivation (R5P L2) | — | OPEN |
| 4 | fleet-readiness §4 runbook merged with `docs/audits/2026-09-05-technical-fleet-readiness.md` §4 (*H0 runbook — corp-monorepo*) on `main` | — | OPEN |
| 5 | the release commit is the ONLY commit touching hub regions and the manifest version together | see note below | OPEN — one nearby act cleared |

## Gate 2 — the ESSENTIALS deferral (filed by inbox item 012-A, 2026-09-05)

**`CLAUDE.md`'s first-read ESSENTIALS line was deliberately NOT touched by 012-A.** It is
fleet-coupled and rides with the v1.5.0 release commit as `[#628]`'s closure; removing it in an
ordinary docs commit would decouple the hub from consumers that still boot from that line.

The distinction worth keeping when this gate is finally closed: `CLAUDE.md` already sends no session
to `protocols/ESSENTIALS.md` (v2.72 de-blessed every citation), so what remains for the release
commit is the **first-read line itself**, not the citations. The file's body also stays —
`status: superseded`, dissolution still owed under `[#628]`.

## Gate 4 — the referent, replaced (ruling D12, sitting of 2026-09-06)

**Gate 4 previously read *"merged with the local amendment"*, and "the local amendment" resolved to
nothing on `main`.** A gate whose witness cannot be opened is not a gate. `DECLARE-SITTING-2026-09-06.md`
D12 rules the fix as a **replacement, not an append**: the phrase gives way to the H0 runbook's actual
path on `main`, `docs/audits/2026-09-05-technical-fleet-readiness.md` §4 (*H0 runbook — corp-monorepo*).

**The gate stays OPEN.** D12 replaced its *referent*, not its *state* — the same ruling keeps `[#628]`
open, and nothing in this lane merges that runbook. What changed is that a reader can now resolve what
gate 4 is waiting for. Filled by lane `lane-u-628-release-commit` (batch U, W2-R), which owns this edit
per D12's "the checklist edit rides lane 3.14's branch".

## Gate 5 — what a non-release commit may touch, and one act that cleared it

Gate 5 forbids a non-release commit from touching **hub regions and the manifest version
together**. It does not forbid touching a hub region alone.

Recorded because it looks like a violation and is not: inbox item 012-A adds a ninth hub region,
`conventions-library-first` (`CLAUDE.md` §4 + `templates/claude-regions/conventions-library-first.md`,
byte-matched). That commit touches a hub region and does **not** touch the manifest version, so
gate 5 is intact. A future seat auditing the range should read the pair, not the region alone.
