# WINDOW SEAL — 2026-08-20 → 2026-08-23

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-23 · **Slug:** window-seal
- **Window:** opened at `main` `4acce74f` (2026-08-20, 214 open rows), sealed at the merge this
  record rides
- **Governing rule:** `protocols/PLAYBOOK.md` Ch8 wave close (D0–D5) + the R2 ledger arithmetic
- **Scope note:** this record does **not** touch `ARCHITECTURE.md`, `CLAUDE.md` or `VISION.md`.
  Those three are the exclusive property of the `lane-docs-governance` worktree lane, dispatched
  in parallel with this close and running as this was written.

---

## 1. The final ledger line — `validate_backlog` against R2, across the whole window

R2's denominator, as ruled: **the open-row count `validate_backlog` returns on `main`** — the live
instrument, not a census view.

```
window baseline (main @ 4acce74f, 2026-08-20)                214 open rows
closures in the window   11
  #126  #397  #488  #507  #529  #530  #539  #562  #563  #565  #566
births in the window      9
  #570  #571  #572  #573  #574  #575  #576  #577  #578
ledger                   214 - 11 + 9                       = 212
validate_backlog on main (measured, not derived)              212 open rows
                                                              AGREES
banked_D at the wave close   11 - 8 = 3 headroom, 1 spent ([#578]), 2 remaining
```

**Three of the eleven closures were born and closed inside the same window** (`#563`, `#565`,
`#566`), which is why the closure list is longer than a naive diff of the two row sets. Stating it
because a reader reconciling the numbers by subtraction alone would come up short by three and
conclude the ledger was wrong.

**The R2 rule held at every filing.** Births were charged against demonstrated close capacity, and
the cap bound twice: the 2026-08-22 filing queue stopped at exactly five with `f6`–`f8` named as a
queue rather than dropped, and this close spent 1 of 3 rather than filing every classified line.

---

## 2. A4 — the release note: what the operator gained this window

**Written as what a *user of this repo* now SEES that they did not before**, per the A4 convention
the lane contracts carry.

> **Model acceptance stopped being guesswork.** There is now a no-pack sandbox that can prove a
> candidate cannot read its own answer key — 11 probe vectors, a verified postcondition, and a
> teardown that deletes only what it provisioned — and the first A/B run under it measured **240
> commands with zero contamination**. Two candidates were scored against three gates on evidence
> and **both were REFUSED**, with the verdict recorded verbatim in one place instead of scattered
> across rows.
>
> **Telemetry events are now correlated.** Every `check_run` / `hook_run` / `blocker_fired` row
> carries a `run_id`, so events from concurrent gate runs in parallel worktrees can be told apart
> in one shared store instead of guessed at by timestamp. The single-flight dispatch guard **no
> longer deletes another run's live lock** — release requires the per-claim token and is a
> compare-and-swap. Telemetry emission got **~49× cheaper** on its logging side-channel
> (480.60 µs → 9.79 µs).
>
> **Direct-to-`main` is now refused at commit time, not only at push time** (`block-commit-on-main`),
> and a provider/model pin that gets *deleted* no longer passes the agreement gate silently.
>
> **The tree is legible again.** `origin` carries `main` and one protected automation branch — down
> from eighteen — and every retirement was content-verified before the delete rather than after.

### The three operator demands, scored

| Demand | Verdict | The evidence, not the impression |
|---|---|---|
| **Felt speed** | **MET, partially, and the remainder is filed** | The measured win is real and specific: 49× on the logging side-channel, run_id correlation landed, the single-flight ABA race closed test-first. It is **not** a whole-loop speed-up: the tel lane measured the store leg at **16.4 ms/event, 98.5% of an emit**, with **silent drops at 8 concurrent writers** — filed as `[#575]`, not smoothed. The read path the operator would actually *feel* is `[#576]`, sequenced deliberately behind run_id and not yet built |
| **Archival EXECUTED** | **NOT MET — and the answer is a finding, not a failure** | `git mv` operations: **0**. The lane executed the measurement that decides what is archivable and the repo returned *nothing, yet*: ADRs 86 live / 2 archived with no implemented-and-superseded set to move, and ADR-100 §1 forbids physically moving audit files at all. `[#564]` stays open carrying that result. The honest scoring is that the demand was answered rather than delivered — the operator asked for a move and got a proof that there is nothing lawful to move |
| **Library-first for the management loop** | **MET as research; adoption deliberately not taken** | Four scaling surfaces surveyed with live trials, and the lane corrected the brief's own premise (Track 1's conflation) and its own count (`deploy/` has six carriers, not four) rather than answering the question as asked. Two carrier rows were approved verbatim by the architect (`[#570]`, `[#571]`). **The honest limit is in the artifact's §0 and is repeated here because it bounds every number: no Python candidate was trialled under our pinned `uv` (0.11.19 vs the container's 0.8.17), and nothing was trialled on Windows** — which matters, because this repo is Windows-developed |

**One demand outside the three, and it is not this record's to score:** *"playbook, architecture,
wszystko zaktualizowane"* — the governance-drift discharge — is the `lane-docs-governance` lane,
dispatched in parallel and still running. See §4.

---

## 3. The next-window queue — verbatim, and each with its handle

Named rather than dropped. A queue entry here is an obligation with an owner or an explicit
"operator-held"; nothing in this list is silently carried.

| Handle | What it is | Where it lives now |
|---|---|---|
| **f6** | The claim-token transport through `/lane-boot` — `single_flight claim` now prints a token the dispatch path does not carry | Unfiled by design (2026-08-22 (c) banked out); no row |
| **f7-dash** | The dashboard stage-2 carrier | Unfiled by design; no row |
| **f8-harness** | The `anchor_gate_probe` investigation — RED on `main` since 2026-08-22, rooted in a `tmp_path` fixture, diagnosed only as far as *"points at the fixture"*, which is not a diagnosis | Unfiled; the RED is live and inherited by every suite run |
| **Q2-mechanism** | *One integrator at a time enforced by mechanism (a lock or a branch guard), not by convention* — Ch8 says so in its own text and then says the rule is prose until the item lands | `protocols/STANDING_RULINGS.md` Q2 + PLAYBOOK Ch8's closing paragraph |
| **#331 / #153 / #541 crossover** | Consumer BACKLOG schema adoption (`#331`), enforcement-completeness (`#153`), and the unowned scale-out substrate decision (`#541`) — three open rows whose overlap nobody has priced | All three live rows |
| **incumbent-promptability** | Whether the incumbent's own refusal failure is promptable — same items plus the reminder, Anthropic path, when billing allows. Blocked on billing, not on judgement | `[#578]`, second clause |
| **mitigated-rerun slot** | The ONE rerun the 2026-08-23 verdict earned, role-reminder preamble baked into every item. Not an admission | `[#578]`, first clause; triage intake 41 first |
| **#34 still operator-held** | Intake #34 remains a DRAFT the operator holds; no lane owns it and none should take it | `docs/intake/`, DRAFT |

---

## 4. State at the seal, for whoever boots next

```
main                      sealed at this merge; origin/main == main
branches (origin)         main + automation/fleet-audit (protected) -- nothing else
worktrees                 lane-docs-governance, LIVE (owns ARCHITECTURE/CLAUDE/VISION)
open rows                 212, validate_backlog OK (1 pre-existing WARN: story [S24] has no tasks)
known RED                 tests/... anchor_gate_probe, inherited since 2026-08-22, tmp_path fixture
known leftover            an EMPTY .claude/worktrees/lane-562-local directory, git-deregistered,
                          held open by the lane's own idle claude process (pid 36348); it
                          disappears when that window closes
intakes                   41 filed today (guard refusal surface); #34-#37 remain DRAFT
```

**What this record deliberately does not do.** It does not merge the handoff bundle — the operator
gates that. It does not touch the three governance files. And it does not score the
docs-governance lane, which was still running when this was written: scoring a lane from outside
while it works is how a close invents a result.
