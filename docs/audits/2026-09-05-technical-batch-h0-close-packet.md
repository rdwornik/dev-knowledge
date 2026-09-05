# BATCH H0-PREP — THE CLOSE PACKET

<!-- scope: meta -->

**Class:** technical · **Batch:** H0-PREP · **Dispatched:** 2026-09-05 · **Closed:** 2026-09-06
· **Manifest:** `docs/audits/2026-09-05-technical-batch-h0-manifest.md`

**Consumers:** `docs/audits/2026-09-05-technical-batch-h0-manifest.md` (this packet is the path its
`closed_by:` names, so the manifest cites it by construction) · `[#528]` (§1, §2 L5) · `[#634]`
(§1, §3) · intake `#66` (§1, §2 L4).

> **The audits index is NOT regenerated here, deliberately.** `[#590]` narrowed
> `audit-index-freshness` to fire on `docs/audits/README.md` and `gen_audit_index.py` only, because
> forcing every batch lane to touch the index put that one file in the large majority of this
> repo's manually-resolved merge conflicts. Regenerating it from here is affirmatively the wrong
> act, not a skipped chore. **The regen is OWED to the integrator on the merged result**
> (`gen_audit_index.py --write`, `git add` first — the generator reads tracked files only), and it
> is named here so the debt is visible rather than silent.

**Landing this file at this path IS the close act.** `scripts/batch_manifest.py` resolves an open
batch as four conjuncts — the manifest is TRACKED, `status: open`, `closed_by:` names a shape that
CAN resolve, and that path is ABSENT. This packet is that absent path, so the merge that lands it
flips the fourth conjunct and the batch closes. No edit to the manifest is required or wanted:
flipping `status: open` would mean editing an immutable file to record that it was finished. This
reuses the mechanism the R5P close established rather than inventing a second one.

## 0. Who wrote this, and under what authority — stated because it is unusual

**This packet was written WITHOUT an operator instruction naming it**, by the outgoing handoff seat,
on the joint judgment of that seat and INTEGRATOR-2 that the packet was **owed work** rather than a
formality manufactured to open a gate. The distinction was tested before either of us acted: all
three committing lanes were verified on `main`'s first-parent spine, independently, by both seats.
Had any lane been unmerged, the handoff would have been reported as owed instead of a packet being
written to clear its path.

The trigger was mechanical and worth recording, because it will recur. `gen_handoff.py` refuses to
cut any bundle while a batch is open (`OpenBatchError`, no override flag), so **an unwritten close
packet blocks every handoff in the repository**, not merely its own batch's paperwork. H0-PREP's
work finished; its packet did not exist; the window could not close. The operator may revisit this
— it is recorded here and in the integrator's census so it is read rather than discovered.

**Ownership followed the standing boundary, not the R5P precedent.** Producing an artifact is the
producing seat's; anchoring, index regeneration, review and the merge are the integrator's. The R5P
packet was written by INTEGRATOR-2 because the operator named that specific file, and a precedent
set by an explicit instruction does not generalise into a rule.

---

## 1. Rows closed — the hard metric

**ROWS CLOSED: 0.** Measured, not assumed, and the measurement is the finding.

The manifest's lane table cites two ids, and the natural reading — that a merged lane closed the row
it names — **is wrong in both cases, for two different reasons**:

    [#528]  OPEN.  tasks/528-lane-latency-full-suite-multiplied-across-a-batch.md carries
                   `status: open`. L5's own end-of-lane artifact says so in its own words:
                   "this lane is one narrow leg of that broader lane-latency task, not a
                   closure of it". The lane referenced the row; it never claimed to close it.

    [#66]   NOT A BACKLOG ROW AT ALL. There is no `tasks/66-*`. `#66` is an INTAKE id —
                   docs/intake/2026-09-01-tech-observable-harness.md, "The OBSERVABLE HARNESS".
                   The manifest cites it in `[#id]` bracket notation, which is this corpus's
                   notation for a backlog row.

    [#634]  OPEN.  tasks/634-dispatch-run-accepts-github-token-as-the-anthropic-check.md
                   carries `status: open`. Re-scoped, not closed — see §3.

**`[#66]` is a THIRD instance of a citation class this window has now hit three times.** A bare
number resolved into the wrong namespace: `E-NN` defect-register ids read against `#NN` intake ids
(recorded in the seat-notes audit), `NC1–NC6` resolving into both the v1.5.0 tag gate and the AJ
lane contract's non-negotiables, and now an intake id wearing a backlog row's brackets. These are
**not** the same defect as the `#70` allocation race filed as CANDIDATE R5P-C2 — that one needs an
allocator that cannot hand out an id twice; this one needs **qualified citations**. R5P's ERRATUM 2
drew that distinction explicitly and it holds here. Filed below as a CANDIDATE, not repaired: the
manifest is immutable, and re-notating a live citation handle is not this packet's act.

**Net backlog delta: 0** (224 open rows before and after; method named in §5).

---

## 2. Per-lane witnesses — read off the branches, not off the receipts

Every lane carried **Done-clause 0** from the operator's ruling: *a lane is done when its branch
carries a commit*, because a receipt reports transport only. All three are verified here by
first-parent spine membership and by their own landed diffs.

### L5 · `lane-h0-suite-speed` — merged `c710ece0`, lane commit `ed2d34d9`, refs `[#528]`

**The contract's named lever was already closed, and the real defect was somewhere else.** pytest's
collection phase never paid for live worktrees at any count tried — `4917 tests collected` at 0, 2
and 5 live worktrees, ~1.4–1.9 s throughout — because pytest's default `norecursedirs` includes
`.*`, which prunes `.claude` before the walker reaches `.claude/worktrees`. The `pyproject.toml`
lever the contract named in its Done-clause 2 was closed by an undocumented default.

The cost lived in two `live_repo` tests that walk the tree themselves: `test_toc.py` and
`test_normalize_headers.py` each build a corpus via `Path.rglob("*.md")` and applied their
`_SKIP_PARTS` filter **after** the walk. `Path.rglob` consults neither `.gitignore` nor
`norecursedirs`, and a live worktree is a full checkout of this repo, so every worktree's duplicate
corpus was read and parsed on top of the primary's.

    state                       corpus files      normalize_text over it
    0 worktrees (repo alone)          2,420       —
    5 live worktrees, pre-fix        14,510       78.57 s   (12,090 duplicates)
    5 live worktrees, post-fix        2,420       12.96 s

Serial run of the two real tests at 5 live worktrees, pre-fix: **killed twice after exceeding a
120 s bound, never observed to complete.** Post-fix, same two tests at 5 worktrees: `2 passed in
51.39 s`; at 2 worktrees (the operator's declared floor): `2 passed in 51.49 s` — a 0.2 % delta,
**because after the fix corpus size no longer depends on worktree count at all**. The witness holds
by construction rather than by luck, which is the stronger form.

Landed: 2 test modules changed, 1 artifact
(`docs/audits/2026-09-05-verification-lane-h0-suite-speed.md`).

### L4 · `lane-h0-trace` — merged `62ec945c`, lane commits `413b9592`, `f2802939`, `0d318c1f`, board `#66`

Every dispatch now leaves a readable trace under `logs/prompts/`, reusing `receipt.json`'s own
fields rather than inventing a format. New `scripts/trace_writer.py` (`render_trace()` /
`write_trace()` plus a Click CLI) writes one file per dispatch carrying the five contracted parts:
the contract as sent, the skeleton run, the receipt, the outcome, and model/effort — concatenation
only, no computed metric. `logs/prompts/` joins the DISPATCH ARTIFACTS ignore block, never
committed. `scripts/fleet_health.py` gains `count_traces_today()` and prints `[traces] N today`,
fail-soft. Tests: `test_trace_writer.py` (9) plus 4 cases in `test_fleet_health.py`. 389 insertions
across 6 files.

**The lane's honest limit, restated here rather than left in its own artifact.** Done-contract item 1
asked for one seeded dispatch witnessed with all five parts present. That witnessing is via hermetic
`tmp_path` fixtures, **not a live capture of the lane's own dispatch** — and that is structural, not
a shortcut: `dispatch-run.sh` writes `receipt.json` only after the `claude -p` process it launched
exits, so no action from inside a session can produce a genuine receipt for its own run. A live
end-to-end trace needs a later dispatch, or a change to `dispatch-run.sh` itself — both outside the
lane's declared footprint. **So `logs/prompts/` has a writer and a counter, and has not yet been
witnessed end-to-end on a real dispatch.** Anyone citing the TRACE layer as delivered should cite it
at that resolution.

### L3 · `lane-h0-readme` — merged `b3326083`, lane commit `24eac392`, no row id

`README.md` becomes the front door: 189 lines of governance prose relocated to
`docs/archive/governance.md` (+210), with `docs/archive/VISION.md` re-pointed. Nothing deleted —
relocation only, consistent with ADR-114's recreation of `README.md` as a sanctioned Tier-1 file.

**L3 left NO end-of-lane artifact.** It is the only one of the three that did not, so its outcome is
recorded here from its diff rather than quoted from a lane packet. Done-clause 0 is satisfied — the
branch carried a commit — but the batch's evidence for L3 is this paragraph and the diff behind it,
which is weaker than the other two lanes' and is said so rather than smoothed.

---

## 3. L2 — retired before dispatch, and whether that retirement still holds

The manifest's own title calls L2 *"the admission gate that was already fixed"*, and records
`lane-h0-admission-gate` (`[#634]`, P1) as **retired by operator ruling before any machine was
provisioned**, on two established facts: the target `dispatch-run.sh` is cross-repo (generated per
run by `win-tooling`, absent from this repo's history), and the defect was already fixed by
`win-tooling@d6cbd92`, which split `adm_tok_anthropic` from `adm_tok_github` four days before the
row was filed.

**The question the integrator raised, answered here rather than left silent.** `main` still carries
`[#634]` as an OPEN P1 whose title asserts the fail-open gate. Is that a contradiction? **No, and
the reason is on the record:** `[#634]` was **re-scoped, not closed** (branch `docs/rescope-634`).
Its residual is two things the `win-tooling` fix does not cover — (a) a probe that can SEE the
`CLAUDE_CODE_MESSAGING_SOCKET` path, and (b) Done-clause 0 itself, that a dispatched lane's
correctness gate is a commit on its own branch and never the receipt. Both survive the token-split
fix, because the evidence for them is that in `lane-632-longrun-a-w95qprj5wq4cg67g`
`CLAUDE_CODE_OAUTH_TOKEN` was unset and `claude auth status` reported `loggedIn: false` while the
session ran 338 events authenticated over the socket — **both local probes false-negative**.

So L2's retirement holds: the contracted closure (*"only `GITHUB_TOKEN` set → REFUSED naming the
variable"*) was deliberately not built because it would be fail-CLOSED on a path measured working.
**What the open row's TITLE claims is narrower than what the row now IS**, and a reader who resolves
only the title will misread it. That is a citation defect in the row, not a live fail-open gate —
recorded, not repaired, because editing a row's title is not this packet's act.

---

## 4. What this batch actually delivered, at the right resolution

- **A measured, structural fix to suite cost under live worktrees** (L5) — the strongest result
  here, because it removes the dependency rather than reducing a constant.
- **A trace writer and its counter** (L4) — built and tested, **not yet witnessed on a live
  dispatch**.
- **`README.md` as the front door** (L3) — relocation complete, evidence thin.
- **A retirement that was correct on evidence** (L2) — and which the batch's manifest calls its own
  main finding.

**Three lanes were instructed to run in parallel; two did.** The account caps concurrent codespaces
at 2, so L3's create was refused `HTTP 400: You have too many codespaces running` and it queued into
the first free slot. Nothing was provisioned or billed for it while queued. The manifest recorded
this at dispatch; it is repeated here because "three lanes in parallel" appears in the instruction
and is not what physically happened.

---

## 5. SCORECARD — every number marked for how it was obtained

`organ-computed` names the command. `hand-counted` names the method and is a tally of recorded
events, not a metric. **A hand count wearing an organ's label is the drift class this section exists
to prevent, and the R5P packet paid for it in review — six carried findings, most of them here.**

Measured at `8f5bcda2` (`main`, this packet unmerged and therefore not counted in any corpus figure
below), from the PRIMARY checkout with zero linked worktrees.

    rows closed                        0    hand-counted    per-id status read from tasks/*.md; §1
    net backlog delta                  0    hand-counted    grep -c '^- \[#' BACKLOG.md, 224 -> 224
    lanes dispatched                   4    hand-counted    manifest lane table
    lanes retired before dispatch      1    hand-counted    L2, manifest §"L2 WAS RETIRED"
    committing lanes merged            3    hand-counted    first-parent spine membership, verified
                                                            independently by both seats
    audit.py health                   OK    organ-computed  uv run --locked python scripts/audit.py health
    hard-fail [!!]                     0    organ-computed  same run
    WARN [~~]                         40    organ-computed  same run
    OK [OK]                           45    organ-computed  same run
    n/a [--]                          16    organ-computed  same run

**`audit.py health` wall-clock is deliberately ABSENT from this scorecard.** The command prints no
timing, so any figure would be the author's stopwatch. R5P's packet carried one labelled
`organ-computed`, which was its single provenance mislabel; the correct fix is not a better label
but not claiming a number the packet does not need.

**THE FULL SUITE WAS NOT RE-MEASURED FOR THIS PACKET, and no aggregate is claimed.** The last
measured aggregate is R5P's `21 failed · 4967 passed · 3 skipped · 1 xfailed` in 1310.50 s, taken at
`3a2391fb` — **before** several subsequent merges including this batch's own AJ lane. Quoting it as
this batch's state would repeat R5P's ERRATUM 1 exactly: a measurement basis stated as later than it
was. Re-running a 22-minute suite to decorate a docs-only close is not proportionate, so the honest
record is that the aggregate is unknown at `8f5bcda2` and this packet does not assert one.

---

## 6. Health at close — attributed, not totalled

`health: OK`, **0 hard-fail**. The 40 WARNs are not this batch's and are not summed into a verdict:

- **22 are `consumer_at_landing`**, the largest group, and they are a MECHANISM fact rather than
  incomplete work. `consumer_at_landing` asks whether a *governance POOL* file cites an artifact,
  and `docs/audits/` is not in `POOL_DIRS`. **Three of those 22 are this batch's own artifacts** —
  the manifest, L4's close and L5's verification. **This packet cites all three by path, and that
  will NOT clear their WARN**, because a citation from `docs/audits/` is invisible to the check by
  construction. Predicting otherwise would be the error; the ruling that check needs is already
  before the operator.
- **8 are `canonical_freshness`** (1 gated-and-stale — `CLAUDE.md`; 4 ungated-and-stale; 8
  unstamped, the groups overlapping), untouched by this batch.
- **7 are `doc_rot` history-accretion**, five of them named BACKLOG rows plus row-length and a
  grooming cadence 38 d against a 21 d cadence. Calendar-driven and pre-existing.
- **1 is `journal_spine_anchor`** — *"anchored by mention, not by record"* for `3a2391f`. This is
  the WARN leg, **not** the hard-fail leg; it does not block.
- **1 is `adr_status_grammar`**, at its declared baseline.

**One prediction, flagged for the integrator to VERIFY at merge rather than trusted here.** The
suite's `test_batch_manifest` was failing on H0-PREP's name at the R5P close. Landing this packet
closes H0-PREP, so that test *may* clear — but this packet does not claim it. Verify on the merged
result; if it clears, the R5P attribution was right, and if it does not, the cause was never the
open batch.

---

## 7. CANDIDATES carried forward — Z-C shape, no rows born here (ADR-111)

**H0-C1 · An unwritten close packet silently blocks every handoff in the repository.**
`gen_handoff.assert_batch_boundary` refuses over any open batch, with no override flag, so a batch
whose lanes all merged but whose packet nobody wrote holds the entire window-close hostage — and the
refusal names the batch, not the missing act, so the reader must already know the mechanism to
diagnose it. Evidence: this packet's own §0. **Owes intake. Not a row.**

**H0-C2 · A handoff cut cannot be taken from a worktree, so "never the primary" is unsatisfiable
for it.** `assert_boundary_hygiene` refuses over ANY linked worktree, so provisioning an isolation
worktree blocks the gate the cut needs. A standing brief instructing a seat to work in its own
worktree and never the primary is therefore self-blocking for this one act. Witnessed 2026-09-06.
**Owes intake. Not a row.**

**H0-C3 · An intake id was cited in backlog-row notation** (`[#66]`, §1). Distinct from the `#70`
allocation race (R5P-C2): that one needs an allocator, this one needs qualified citations — number
**and** path. **Owes intake. Not a row.**

**H0-C4 · `[#634]`'s title asserts a defect narrower than the row's re-scoped content** (§3). A
reader resolving the title alone misreads a live P1. **Owes intake. Not a row.**

---

## 8. What this packet does NOT claim

- **It does not claim H0 was executed.** H0-PREP is the *preparation* batch. The corp-monorepo H0
  runbook (`docs/audits/2026-09-05-technical-fleet-readiness.md` §4) has not been run, and architect
  inbox item 023 amends it further by adding a seal-report step the merged runbook does not contain.
- **It does not claim `[#528]`, `[#66]` or `[#634]` advanced to closure.** Rows closed is 0 (§1).
- **It does not claim a suite aggregate** at this HEAD (§5).
- **It does not claim `logs/prompts/` is witnessed end-to-end** (§2, L4).
- **It does not claim the `consumer_at_landing` WARNs on its own artifacts will clear** (§6).
- **It does not rule on the v1.5.0 tag.** Three live enumerations of that gate disagree, and the
  operator declares it on the checklist, not a seat.
- **It does not rule whether closing this batch without an operator instruction was correct.** It
  records that it happened, who decided, and on what evidence (§0).
