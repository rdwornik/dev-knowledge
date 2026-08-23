# WAVE CLOSE — the funnel table over the 562-local guarded A/B run

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-23 · **Slug:** wave-close-funnel
- **Wave:** the single-lane `lane-562-local` dispatch (leg 3 of `[#562]`), closed inside the
  2026-08-20 window seal
- **Source artifact:** `docs/audits/2026-08-23-technical-lane-562-local-admission.md`
- **Governing rule:** `protocols/PLAYBOOK.md` Ch8 *"The wave close — every dispatched wave ends
  D0–D5, and the funnel table is mandatory"*; classifications are ADR-111 §1's four outcomes plus
  the executed case
- **Status:** D0–D5 complete. Two lines executed, two filed, five rejected with reasons, two
  covered. No line is a fork, so no PAUSE was taken.

---

## 0. Why this table exists at all for a one-lane wave

Ch8's rule is not scoped by wave size: *"A wave whose artifacts carry findings and whose close
carries no table is unfinished."* This wave dispatched one lane, and that lane reported **four
instrument defects it was contractually forbidden to fix** — the exact shape the rule exists for.
A defect reported and then left in an artifact nobody triages is the leak Ch8 was written after.

---

## 1. D0–D3, recorded before the table

**D0 — enumerate, don't trust.** `git fetch --prune`; the lane's branch `worktree-lane-562-local`
resolved locally at `8c725668`, one commit. Nothing was inferred from absence.

**D1 — read before merging.** The artifact was read end to end before the merge, including §7.4's
surfaced indeterminacy and §10's four defects. **No unfixed Critical or High**: the lane shipped no
code, and the two Criticals of the previous arc were closed on the guard lane before this run began.
The environment caveat is declared in the artifact itself (§11: the pre-commit stack was armed and
run over both staged files ahead of the commit, reported as a measurement rather than an
expectation).

**D2 — merge queue.** One lane, one `--no-ff` merge (`3832f2b4`), JOURNAL anchor 2026-08-23 (b)
naming `8c725668`. Generated-file conflict: none — the index regen the lane carried applied clean.
Teardown followed the merge of the content, push-before-delete, and is recorded in §5 below.

**D3 — closure sweep, and the banked number, computed before anything is filed.**

```
window baseline (main @ 4acce74f, 2026-08-20)            214 open rows
closed in the window   11   #126 #397 #488 #507 #529 #530 #539 #562 #563 #565 #566
born in the window      8   #570 #571 #572 #573 #574 #575 #576 #577
banked_D  = 11 closures - 8 births                       =  3 births of headroom
spent by this table                                       1  ([#578])
remaining after this table                                2
open rows after this table (validate_backlog on main)   212
```

The arithmetic is R2's denominator as ruled: the open-row count `validate_backlog` returns on
`main`, not a census view. `[#562]`'s own closure is inside the 11, which is what funds the one
birth below.

---

## 2. THE FUNNEL TABLE — the four reported defects

Each line cites the clause it answers to. **MECHANICAL lines are listed first**, per Ch8.

### F1 · Defect 1 — `exec` delivers mojibake for non-ASCII on Windows — **MECHANICAL**

**Clause: ADR-111 §1(b) DISCHARGED — the fix is judgment-free, so the integrator executes it in
session.** And a discharge is only a discharge with a locator that resolves:

- **Locator:** `scripts/nopack_sandbox.py`, three `subprocess.run` sites;
  `tests/test_nopack_sandbox.py`, two new tests. Commit `8c9fe372`.
- **What was wrong:** `text=True` with no `encoding=` decodes with
  `locale.getpreferredencoding()`, which is cp1252 on the operator host. The sandbox tree was
  byte-correct; the guard delivered three mangled characters where the file held one em dash.
- **Why it is not cosmetic, and why it was the sharpest of the four:** `C1-X1` scores em dashes
  **verbatim** and instructs the lane not to correct anything. Both lanes passed that item anyway —
  by silently correcting a corrupted source. That is luck pointing the same way as the answer key,
  and on a different item it would not have.
- **Scope of the fix, stated because it is wider than the reported instance:** all three decode
  sites are pinned, not only the one the lane hit. Fixing one instance of a decode bug and leaving
  two siblings is how it comes back. `errors="replace"` was added to the two sites lacking it, so
  pinning UTF-8 cannot introduce a new raise path on undecodable bytes; ASCII behaviour is unchanged
  everywhere.
- **Evidence it works:** `pytest tests/test_nopack_sandbox.py` gives **113 passed** (was 111),
  `ruff` clean. **Mutation-checked** — reverting the exec-site pin fails both new tests, one at the
  em dash and one naming the offending line by number.

### F2 · Defect 2 — `pwd` refused as `argv0-not-allowed` — **INTAKE**

**Clause: ADR-111 §1(c) CANDIDATE, and §2 — a finding may not become a backlog row directly.**
Filed as **intake 41**, `docs/intake/2026-08-23-tech-nopack-guard-refusal-surface.md`.

Not MECHANICAL: widening a security guard's allowlist is a threat-model judgement, not a typo, even
for a harmless read-only builtin. Not REJECT either: 1 genuine over-refusal in 20 ordinary fan-out
commands is a real measurement, and nobody has enumerated whether `pwd` is a one-off or a class.
Carried with F3 because they are one question seen from two sides.

### F3 · Defect 3 — the shell-construct rule is not lane-neutral and reached a scored item — **INTAKE**

**Clause: ADR-111 §1(c) CANDIDATE.** Same intake 41; this is its load-bearing half.

29 of the run's 38 refusals were `A/shell-construct`, split **22 to 7** between the two candidate
lanes — a roughly 3x handicap that depends on a candidate's shell habits rather than on its
competence. It reached `C1-R5`: two attempts to DERIVE the count were refused for chaining, the lane
then eyeballed and returned 86 against a ground truth of 87. **The fabrication is still the
candidate's** — a single `ls | wc -l` was available and the other lane used exactly that — but the
2026-08-23 verdict needed an attribution amendment to say which half belonged to whom, and **the
operator's own framing of this line is the requirement: the item set should not depend on it.**
Whether that is fixed in the item set or in the guard is exactly the fork the intake records rather
than resolves.

### F4 · Defect 4 — the guard is detectable from inside — **REJECT**

**Clause: ADR-111 §1(d), with the reason recorded where the finding lives** (artifact §10 defect 4,
and here).

**Reason:** unavoidable by construction. A guard that refuses a command is information the moment it
refuses one; the only instrument that is undetectable is one that never intervenes. The cloud
artifact **declared this limit before the run** (§3.5) and this run is the live witness — a declared
limit behaving as declared, not a new defect. The refusal message names neither artifact nor canary,
and **no answer-key content leaked**: the property that actually matters held. Not relitigated.

---

## 3. The verdict's own residuals — two successors, one carrier row

These are not lane findings, so §2's finding-to-intake path does not govern them: they are an
architect ruling's explicit acts, and register **P-2** requires a ruling to end at a live carrier
row or a dated deferral.

### F5 · The ONE earned mitigated rerun slot — **FILED, `[#578]`** (the birth this table spends)

The `C1-N3` control passed on both candidates where `C1-N1` failed on both, single variable the role
reminder. R3's promptable-failure clause therefore earns exactly one rerun with the preamble baked
into every item. **Not an admission and not a standing licence** — admission stays REFUSED until
that rerun clears the floor. Charged against `banked_D`: 1 of 3.

### F6 · The OWED incumbent refusal-promptability measurement — **COVERED, `[#578]` second clause**

**Clause: ADR-111 §1(a) OWNED, and the cite resolves to a row that is live as of this table** —
checked, not assumed, which is the trap Ch8's check 1 names. It rides `[#578]` rather than a row of
its own because it is the same run: the incumbent's `C1-N3` on the Anthropic path, when billing
allows. Until it exists, no ruling touching the fan-out pin should be made from this evidence.

---

## 4. Section 9's limitations — classified rather than left as prose

| Line | Limitation | Class | Clause and reason |
|---|---|---|---|
| L1 | The incumbent was not re-run; `P_i`/`Phi_i`/`R_i` carried from an unguarded head at tier high | **COVERED** | §1(a) OWNED — `[#578]`, live |
| L2 | Effort tier moved high to medium, so the 13/14 to 10/14 drop has two variables | **REJECT** | §1(d) — medium is canonical per Q8, so THIS run is the correct instrument; the caveat is recorded and there is nothing to fix. The artifact nowhere attributes the drop to de-contamination alone |
| L3 | n=1 per lane; the variance leg did not run | **REJECT** | §1(d) — an admission gate is a floor, and the floor was failed **identically on both refusal items on both lanes**. Variance moves a marginal score, not a 0/2 |
| L4 | The 30-round cap bound two items, both scored FAIL | **REJECT** | §1(d) — the cap was fixed before the run and applied to both lanes; adjusting it after seeing the outcome is what the pack forbids |
| L5 | A guard syntax rule interacted with a scored trap item | **INTAKE** | §1(c) — the same line as F3; recorded once, not double-counted |
| L6 | Scope exclusions unchanged (no recall outside the 14, no cost claim, no long-context, no multi-site retrieval at scale) | **REJECT** | §1(d) — declared scope of the pack, unchanged by this run |
| §7.4 | `C1-N2` indeterminacy: is an exhausted run a refusal? | **INTAKE** | §1(c) — routed to intake 41 as an open question. Not load-bearing this run (G2 fails independently under either reading), but the next run has no reason to be that lucky |

---

## 5. D5 execution — what actually moved

```
MERGED     worktree-lane-562-local (8c725668) -> main at 3832f2b4, pushed
CLOSED     [#562] REFUSED via the tier1-lifecycle gate; row count 212 -> 211, verified
LANDED     the admission verdict, verbatim, as an APPENDED section 5 of
           docs/audits/2026-08-22-technical-annotation-and-rulings-ledger.md
ANNOTATED  [#491] -- evidence only; the row did NOT move and its DEFERRAL is untouched
EXECUTED   F1, the decode fix + 2 tests, mutation-checked (8c9fe372)
FILED      intake 41 (F2 + F3 + L5 + the section 7.4 question)
FILED      [#578] (F5 + F6), 1 birth against 3 banked
REJECTED   F4, L2, L3, L4, L6 -- each with its reason recorded here
RETIRED    17 remote branches, content-verified; origin is now main + automation/fleet-audit
```

**Honest limit of this table.** It classifies what the lane REPORTED. A defect the lane did not
notice is not in it, and the run's n=1 shape (L3) means the instrument has been exercised hard
exactly once on this platform. The two sibling decode sites F1 pinned were found by reading the
module, not by the run — which is a small argument that §10's list is a floor rather than a ceiling.
