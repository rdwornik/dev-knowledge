# BATCH G — CLOSE PACKET

- **Class:** technical · **Date:** 2026-09-04 (filed at the 09-02 identifier the exemption keys on)
- **Arcs:** `[#613]` `[#632]` `[#630]` `[#629]` `[#276]` `[#621]` `[#626]` `[#628]` `[#614]` `[#611]`
- **closed_by:** this file · **Author:** CC (Opus 5, integrator seat)
- **Manifest:** `docs/audits/2026-09-02-technical-batch-g-manifest.md` (filed LATE, and it says so)

> **Flat by design** (`CLAUDE.md` §4 output-formatting) — no pipe tables, so this copies into
> browser chat without the TUI painting border glyphs.
>
> **This packet CLOSES the batch, and closing it KILLS the ADR-110 exemption.** All nine lane
> merges were therefore anchored BEFORE this file landed — verified, not assumed:
> `unanchored on main spine: NONE`, each merge resolving to an introduced SHA named in JOURNAL.

## 0 · THE ONE-LINE RESULT

Nine lanes merged, 99 commits, 32 merges, zero regressions against the base failed-set — and
**exactly ONE backlog row changed status.** The gap between those two numbers is this packet's
real content.

## 1 · THE QUEUE — nine lanes, all merged, all anchored

```
order  lane                                merge      arc              anchored
 1     lane-g-632-parity        (G5)        85827046   [#632]          yes
 2     lane-g-630-lane-contract-predicate   31653206   [#630] [#629]   yes
 3     lane-g-276-deploy-waiver (G2)        e9c6bbad   [#276]          yes
 4     lane-g-621-freshness-absent (G3)     55fecf34   [#621] item 3   yes
 5     lane-g-626-executing-copies (G4)     cfa9a8e3   [#626]          yes
 6     lane-g-628-essentials-debless (G6)   830e6286   [#628]          yes
 7     lane-g-614-hygiene       (G8)        a436545a   [#614]          yes
 8     lane-g-611-bundle-thinning (G7)      e9d39ed9   [#611]          yes
 9     lane-g-621-c7            (G3b)       001bb261   [#621] C7       yes
 +     docs/batch-g-filings     (step B)    f53a007c   filings         yes
```

G0 ran serial on the primary before any lane booted. G3b was cut mid-batch by ruling R-G-G3b.

## 2 · G3b — HOW THE CONSUMER-REPO CASE WAS RESOLVED

**Resolved by classification, not by an exemption.**

**The check.** `scripts/audit.py:1422-1423`, rule `canonical-freshness` ->
`check_canonical_freshness`. The leg holds NO absence logic of its own: its entire body is a call
at `scripts/audit.py:1476` into `scripts/canonical_freshness_gate.py::evaluate` — the same module
the enforcement-mesh carrier byte-copies into each consumer as a pre-commit hook. Hub leg and
consumer gate are ONE code path, which is why a hub-shaped absence rule was able to threaten three
consumer repos at once.

**The condition.** Absence stopped being one case. It is split by whether the corpus REQUIRES the
file:

```
canonical_freshness_gate.py:76-80    PRESENCE_REQUIRED, derived at the hub from
                                     canonical_docs.CANONICAL_MANDATORY; literal
                                     ["ARCHITECTURE.md","CLAUDE.md","CONTRIBUTING.md"] in the
                                     standalone consumer copy; the two pinned equal by
                                     tests/test_canonical_docs.py
canonical_freshness_gate.py:173-176  absent AND presence-required   -> FAIL
canonical_freshness_gate.py:177-178  absent AND presence-optional   -> WARN, worded
                                     "reported, not skipped silently"
canonical_freshness_gate.py:165-167  NONE of the required files present -> return ([], [])
```

The consumer-breaking pair — `docs/handoffs/README.md` and `protocols/ESSENTIALS.md` — is
`CANONICAL_OPTIONAL`, so it warns rather than blocks. Z-G4 is satisfied on its own terms: for an
OPTIONAL document, absent IS the ground truth — a known state, not an unmeasurable one, which is
the condition Z-G4 actually names.

The last line is the narrow one. It is NONE, not "any missing": a repo carrying `ARCHITECTURE.md`
and `CLAUDE.md` but no `CONTRIBUTING.md` has a genuine gap and still FAILs.

**Measured 2026-09-04, run rather than reasoned about:**

```
empty tree                       -> ([], [])
ARCHITECTURE.md only             -> 2 FAIL (CLAUDE, CONTRIBUTING) + 2 WARN (the optional pair)
3 required + 2 optional absent   -> 0 FAIL, 2 WARN, consumer gate exit 0   <- the consumer shape
```

**Does any absent-file case now report "skip" rather than FAIL?**

As a STATUS: **no.** `audit.py` has exactly two skip statuses — `unavailable` (could not run) and
`n/a` (ran, not applicable), semantics at `scripts/audit.py:5327-5331`. This check emits NEITHER
for absence, in any case, hub or consumer.

As an OUTCOME: **yes, once**, and it is named here rather than presented as a clean sweep. The
no-corpus guard returns `([], [])`, which the leg renders at `scripts/audit.py:1489` as status
`pass` with evidence *"8 canonical living files fresh"* — a green sentence counting
`len(_FRESHNESS_FILES)`, i.e. files REGISTERED, in a tree carrying none of them. Scope: only a tree
with none of the three required files (a `tmp_path`, a foreign tree, a fixture built for another
check). No live repo — hub or consumer — reaches it.

**Provenance, so the packet takes no credit it is not owed.** That false-pass WORDING is
INHERITED, not introduced. Pre-G3b (`001bb261^1`) the loop read
`continue  # presence enforced elsewhere — don't double-report`, so EVERY absent file was silently
skipped and an empty tree produced the identical string. G3b did not fix that sentence; it shrank
the set of trees that reach it from "any tree with an absent registered file" to "a tree with none
of the required three".

**Why the existing guard does not catch it.** `tests/test_skip_is_not_pass.py:44` matches
pass-findings whose EVIDENCE is skip-worded (`_SKIP_EVIDENCE_RE`: "skipped", "unreadable", "git
unavailable", …). This evidence is affirmatively worded, so it passes. The guard catches an honest
skip mislabelled `pass`; it does not catch a confident false sentence. That is a gap in the guard,
not in G3b.

**RESIDUAL, one line, not fixed in this batch.** `scripts/audit.py:1432` still reads *"An absent
file is skipped (presence is enforced by #1/#3/#5)."* That is now FALSE for a required file — the
docstring documents the pre-G3b behaviour of the code directly beneath it. Coupled to candidate (j).

**The load-bearing sentence.** Absence stopped being one case. Every earlier attempt failed because
it answered "is the file there?" — one question with one verdict, which either broke the fleet
(unconditional FAIL) or forgave the hub (unconditional skip). The split asks "does THIS corpus
require it?" first, and only then "is it there?"

## 3 · ROWS CLOSED — the hard metric

**Measured, `status:` frontmatter in `tasks/*.md`, batch start (`1e064921`) -> HEAD:**

```
open    172 -> 171
closed  132 -> 133
rows whose status actually changed:  1   ([#614])
```

**ONE row closed.** Not nine. That is the honest counter, and it is not a failure of the batch —
flipping a row is `/review-closures`, an operator act (ADR-70 Tier-1). The packet's job is to
witness the clause so the operator can declare. Below, per row: the clause, the witness, the
verdict.

```
[#614]  CLOSED ALREADY — the only status flip. VISION superseded by a recreated root README.
        Witness: a436545a (G8). Counter currently stands here.

[#630]  CLAUSE  freeze gate REFUSES unless manifest lane-slug set == contract-slug set, BOTH
                ways; refusal names both sides; a test freezes a renumbered slug and asserts it.
        WITNESS tests/test_gen_lane_contract.py --
                test_check_refuses_the_measured_batch_e_slug_renumbering
                test_check_refuses_a_manifest_naming_a_contract_no_manifest_row_declares
                test_the_precommit_hook_runs_on_every_commit_AND_still_receives_its_contracts
                test_check_runs_with_zero_paths_instead_of_erroring
        VERDICT MET. One honest qualifier: the predicate lives in gen_lane_contract.py invoked by
                the lane-contract-check hook, not in validate_substrate.py. Set equality both
                ways, the named-both-sides refusal and the renumbering test are all present.
                >>> ELIGIBLE FOR THE OPERATOR'S DECLARATION.

[#276]  CLAUSE  a consumer-declared divergence causes BOTH the prune sweep to SKIP it AND the
                add/converge leg to NOT re-append it, on a previously-deployed consumer, with tests.
        WITNESS tests/test_enforcement_coverage.py + tests/test_carrier_precommit.py --
                test_waived_components_honors_a_valid_unexpired_date      (honouring)
                test_prune_refuses_on_an_expired_waiver                   (prune leg)
                test_add_leg_re_adds_the_hook_on_an_expired_waiver        (add leg)
                test_waived_components_refuses_entry_with_no_date
                test_waived_components_refuses_entry_with_unparseable_date
                test_waived_components_refuses_expired_entry
                test_a_malformed_date_is_not_absent_it_is_a_REFUSAL
        VERDICT MET, and it fails CLOSED on both date fields (expiry AND review_date), which the
                clause did not demand and G2 added anyway.
                >>> ELIGIBLE FOR THE OPERATOR'S DECLARATION.

[#629]  CLAUSE  validate_substrate.py carries a SEVENTH predicate refusing a contract whose
                amendment negates an act present in its own body; refusal names the reissue path;
                gen_lane_contract grows the reissue verb; predicate armed at FREEZE with the
                per-leg grandfather; one RED-first test dispatches the real DC-3 shape.
        WITNESS none.
        VERDICT NOT MET, and the evidence is categorical: `git diff --name-only 1e064921 HEAD --
                scripts/validate_substrate.py` is EMPTY. The file was never touched anywhere in
                the batch. G1 built #630's predicate (two surfaces disagreeing), not #629's (a
                contract contradicting itself). They rode one lane and are two defects; the row
                said so, and the lane closed one of them.
                >>> STAYS OPEN.
```
```
[#621]  CLAUSE  a sequencing plan across the ADR-104 members exists before the first commit, and
                ADR-114's second (spine) decision is made in the same ruling.
        WITNESS G3b (001bb261): release_lint C7 re-shaped to bind a manifest to the constants AS
                OF ITS OWN VERSION; VISION out of FRESHNESS_FILES and out of the consumer
                fallback literal; released manifests v1.1.0/v1.2.0/v1.3.0/v1.3.1/v1.4.0 show a
                ZERO-LINE diff. The retro-edit was REFUSED by ruling, and the refusal held.
        VERDICT NOT MET as written. The clause is about a NINE-REPO filename migration; batch G
                did the hub's step one and the lint re-shape that unblocks it. Real progress
                against a clause it does not satisfy.
                >>> STAYS OPEN.

[#626]  CLAUSE  ls logs/ after retention: no dated PROPOSALS-* / DETECTOR-ERROR-* flat (step A).
        WITNESS step A, run 2026-09-04: 3 flat before, 3 flat after. Retention REFUSED.
        VERDICT NOT MET, and step A is what found out. Reading was fixed (the deployed plugin
                copies now glob **/PROPOSALS-*.md recursively -- propose_closures.py:329,:371,
                review_closures.py:235). WRITING was not: propose_closures.py:413 and :482 still
                write flat, and retention is wired into no hook. Two further facts the step
                surfaced: it buckets by MONTH (logs/YYYY-MM/), not into the logs/proposals/ +
                logs/detector-errors/ pair the clause assumes; and it is now WEDGED -- see §7.
                >>> STAYS OPEN.

[#628]  CLAUSE  pointers zero; STAYS OPEN until v1.5.0 (a release act by construction).
        WITNESS re-measured 2026-09-04: pointers are NOT zero. TWO live routes remain --
                protocols/AI_COUNCIL_PROCESS.md:413 and protocols/PLAYBOOK.md:330, both outside
                the owning lane's write-scope, unchanged since the 2026-09-02 measurement.
        VERDICT NOT MET on the pointer leg, and STAYS OPEN by design regardless.
                >>> STAYS OPEN.

[#611]  CLAUSE  gen_handoff measurement printed on a real cut: bytes <= 20,000 + the derived ratio.
        WITNESS mechanism LANDED in full -- assemble_paste.py:198 derives the window-specific
                definition, :359-361 computes and PRINTS "window-specific {ws}/{content}", :352
                prints the byte count on the END OF PASTE line, :46 leaves ONE ceiling
                (PASTE_BYTE_CEILING = 20_000) with both rivals retired (_SIZE_WARN_BYTES = 48_000
                and paste_budget = 65_000 survive only as comments recording their retirement).
                BARS MISSED, from the lane's own doc, verbatim:
                  BAR 1  size            <= 20,000 B   ACTUAL 29,776 B   MISS by 9,776 B (+49%)
                  BAR 2  window-specific >= 70%        ACTUAL 32%        MISS by 38 points
                The lane improved the filled cut 32,264 B -> 29,776 B and reported both misses
                itself.
        VERDICT NOT MET. The measurement is printed; the value is not under the ceiling.
                >>> STAYS OPEN.

[#632]  CLAUSE  STAYS OPEN: G5 nodeids re-filed as portability candidates; substrate note in §V.
        WITNESS the dated V-addendum in protocols/STANDING_RULINGS.md carries the per-substrate
                base failed-set doctrine and cites the parity doc
                docs/audits/2026-09-02-verification-parity-b5753f52.md (4e279c1c, merged
                85827046). G5's flip is deliberately NOT closed -- classification first.
        VERDICT the instruction is DISCHARGED; the row STAYS OPEN as instructed.
                >>> STAYS OPEN, correctly.
```

**The counter, if the operator declares on this evidence: `[#614]` + `[#630]` + `[#276]` = 3.**
The other five cannot move on what batch G produced, and each says why in one line above.
"Do not leave the counter at `[#614]`" was right — and it moves to three, not to nine.

## 4 · SMALLER

```
measure                                    before        after      delta
tasks/** rows (files)                      389           389        0  -- closing retires, never deletes
tasks/ status: open                        172           171        -1
docs/intake/*.md                           59            58         -1
byte budgets claiming to be THE budget     3             1          -2  (48_000 and 65_000 retired)
logs/ top-level entries (working tree)     101           18         -83 (89 dated files bucketed by month)
logs/ flat dated files                     89            3          -86 -- and the 3 are the defect, see §7
PASTE_THIS.md filled cut (bytes)           32,264        29,776     -2,488 (-7.7%); ceiling is 20,000
CLAUDE.md bytes                            24,432        24,432     0  -- untouched, cap 24,576
```

`docs/audits/*.md` went 866 -> 875 (+9): the batch's own evidence, which is the one number that
SHOULD go up.

## 5 · VISIBLE — what can now be seen that could not

```
OPERATOR ASKS register rows                5 -> 15, one live store, live-parser verified
absence in the freshness gate              silently skipped -> FAIL (required) / WARN (optional)
window-specific ratio                      undefined -> derived, implemented, PRINTED on every cut
the substrate decision                     asserted -> MEASURED (parity doc + container-set JSON)
base failed-set                            ad hoc -> a committed artifact, 13 nodeids, per substrate
routing carrier vs L0 region               diverged -> agreeing 4/4
the deploy waiver's time-box               shape-only -> policed by BOTH readers, fails closed
```

## 6 · UNBLOCKED

```
question                                        answer   evidence
lane-contract gate reachable on a real commit?  YES      always_run: true; the pass_filenames: false
                                                         that made the predicate unreachable removed
manifest<->contract slug drift detectable?      YES      set equality both ways + renumbering test
a valid consumer waiver honoured on both legs?  YES      prune skips, add does not re-append
a malformed waiver date?                        REFUSED  fails closed, not open
consumer repos blocked by the freshness gate?   NO       measured on the 3 live consumers: 0 FAIL
released manifests protected from retro-edit?   YES      C7 binds a manifest to its OWN version;
                                                         5 released manifests show a zero-line diff
```

## 7 · #528 — THE CONTENTION DATAPOINT

Delta A2 was computed once per merge, serially, on `main`, comparing nodeid SETS (never counts —
`addopts = "-n auto"` makes a count meaningless). Wall-clock, in queue order:

```
baseline (0 lane worktrees)   897 s
merge 1  2675 s      merge 4  2004 s      merge 7  1832 s
merge 2  2543 s      merge 5  1981 s      merge 8  1924 s
merge 3  2585 s      merge 6  1982 s      merge 9  2159 s
```

**The driver is live worktree COUNT, not the diff under test.** ~2,600 s at nine worktrees, falling
to ~2,000 s after two were removed, against an 897 s baseline — a **2.2x–3.0x tax** paid on every
merge. Nine serial full-suite runs cost roughly **5.4 hours of wall-clock**, and the batch's own
parallelism is what bought it: the lanes that make the batch fast are the same lanes that make each
verification slow.

An earlier reading of this series was WRONG and is corrected here rather than quietly dropped: the
diagnostic runs I added were blamed for a 3x inflation. Re-measured, runs 2675/2543/2585 s put the
diagnostic cost at ~4%. The worktree count was always the driver.

**The filings merge's own delta A2 (the tenth run): 2,023 s, 13 failing, and it caught something.**
Set comparison against the base: **2 fixed, 2 REGRESSIONS** — and the failing COUNT was 13 both
times, which is exactly why R-G-A2 compares nodeid SETS. A count-based check would have reported
"no change" and shipped the regression.

```
fixed:      tests/test_reverse_dep_oracle.py::test_finding_headline_resolves_with_provenance
fixed:      tests/test_reverse_dep_oracle.py::test_main_finding_json_exit_zero
REGRESSION: tests/test_gen_audit_index.py::test_live_index_is_fresh
REGRESSION: tests/test_gen_audit_index.py::test_live_index_excludes_nothing_because_every_audit_is_tracked
```

Diagnosed, not bounced: G3b's lane added `docs/audits/2026-09-03-technical-lane-g-621-c7.md` and
the generated index still declared 873 documents against a live 874. A lane must NOT regenerate
that index — it races every sibling lane — so leaving it stale in-lane was correct, and
regenerating it is the INTEGRATOR's act, gate-of-record for generated surfaces. Both nodeids are
discharged by the regeneration that lands with this packet, which also absorbs the packet's own
+1. Same class as G7's terra P1 (`ecosystem/doc-counts.md`), same resolution.


## 8 · THE TWO SOFT-GATE ARTEFACTS

```
1  docs/audits/2026-09-02-verification-base-failed-set-1e064921.json
   13 nodeids, source `run-report`. The lastfailed cache was a day stale and reported 45; the
   --from-report path reads the run's own FAILED/ERROR lines instead. Ratified as R-G0-3.
   Its ANSI-stripping regex is built by construction (chr(27)) because a coloured FAILED line kept
   a leading ESC and matched nothing -- a silent dropper of real failures, inside the organ built
   to stop silent forgiveness.

2  docs/audits/2026-09-02-verification-parity-b5753f52.md  (+ the container-set JSON)
   The measured codespace-vs-local diff that FLIPPED the substrate verdict. It is the witness the
   `Codespace used` operator ask now cites, and the doc the V-addendum points at.
```

## 9 · DEVIATIONS AND CORRECTIONS, INCLUDING MINE

```
1  G7's MERGE SUBJECT IS FALSE. `e9d39ed9` reads "a real cut under 20,000 B". The cut measured
   29,776 B. The lane reported both misses honestly in its own doc; I collapsed "mechanism landed"
   into "bars met" when writing the merge subject and when reporting it to the operator. Corrected
   in JOURNAL (e); the commit message is immutable and stands wrong in history, which is why it is
   restated here.

2  THE RETENTION ORGAN IS WEDGED, and step A is what found it. `PROPOSALS-<date>.md` is a
   day-granular name for a per-RUN artifact. logs/PROPOSALS-2026-09-02.md and
   logs/2026-09/PROPOSALS-2026-09-02.md are both 208,062 bytes, differ in content, and record
   head_commit 040dec74 / window 4763 vs 55fecf34 / window 4754 -- two real runs eleven minutes
   apart during integration. Flat, the second silently overwrites the first. Once one copy is
   archived, apply_moves correctly REFUSES to overwrite it and aborts the whole plan, so 09-03 and
   09-04 queue behind a collision that will never clear itself. The guard is right; the naming
   grammar guarantees the collision it guards against. Filed as candidate (k). NOTHING DELETED --
   which copy survives is the operator's call.

3  BRANCH-NAME DEVIATION. The note names the filings lane `lane-g-filings`;
   `validate_branch_naming.py --lane lane-g-filings` exits 1 (LANE_BRANCH_RE wants
   worktree-lane-<letter>-<id>-<slug>, and this arc closes no row so it has no numeric id). It ran
   as `docs/batch-g-filings`, an author-chosen enum prefix. Same precedent the manifest already
   set for `g5-632-parity` and `lane-g-621b-c7`: the gate is the authority over the prompt's
   shorthand.

4  STEP A's PREMISE DID NOT HOLD, harmlessly. It specifies "moved via git mv, byte-identical
   (never deleted)". Every dated logs artifact is untracked and gitignored -- `git ls-files`
   returns 0 across all four month buckets -- so that describes a tracked-file hazard that does not
   exist here. Reported rather than silently satisfied.

5  THE ASKS REGISTER IS PERMANENTLY 0 RED, and that is a property of the predicate. RED needs
   re-asked >= 2 with no visible-fix AND no named blocker; all 15 rows carry one, and
   fleet_health.ask_is_red concedes it "does not adjudicate blocker QUALITY, only presence". The
   digest line the operator reads each session cannot distinguish "nothing is stuck" from
   "everything named a reason".

6  THE #629/#630 PAIR RODE ONE LANE AND ONLY ONE CLOSED. Both rows warned about this in their own
   text ("deliberately a separate row because it is a different gate at a different moment"). The
   lane was contracted around the manifest<->contract comparison and delivered exactly that.
```

## 10 · TERRA

Eight completed reviews across the queue, **10 x P1**. Every one traced to the CONTRACT or to
INTEGRATION, not to lane execution — including the batch's most consequential catch: G3b's closure
text, implemented exactly as written, would have blocked **every commit in all three consumer
repos**. The lane obeyed; the text never said WHICH files must exist.

That pattern is the batch's clearest signal about where defects are actually born.

## 11 · THE ARCHITECT'S PROPOSED H ORDER — for the operator's ruling

The architect proposes, and this packet does not decide: **(g) the Gemini/agy whole-corpus
doctrine-coherence audit first**, because it is retrieval-only and its output re-prices everything
after it; **then H0 with the monorepo attended**; **then the TRACE layer**, which is the declared
precondition for the prompt-distiller and dashboard asks both (a trace has nowhere to land until
`logs/prompts/` exists); **then the derived-copies registry** (candidate (c)), which this batch
earned the evidence for by hitting three separate copy-drift classes with three unrelated organs;
**then the rest**. Candidates (a) README front door, (g) corpus audit and (j) per-consumer freshness
registry are each flagged **H0 PRECONDITION** — (j) newly so, because until a consumer can declare
its own freshness set, every registry change stays a fleet-wide blast-radius decision made at the
hub, which is the exact shape that produced the defect G3b spent a lane repairing.

No new lanes are proposed here.

## 12 · WHAT THIS PACKET CLOSES

This file is the `closed_by:` target named in
`docs/audits/2026-09-02-technical-batch-g-manifest.md`. Landing it makes that path PRESENT, which
resolves the batch as no-longer-open and **retires the ADR-110 declared-integration-arc exemption**.
All nine lane merges plus the filings merge were anchored before this file landed — verified as
`unanchored on main spine: NONE`, not assumed.

**Still owed, and named rather than left implicit:** the `worktree-lane-g-*` teardown — six live
worktrees and eight branches at the time of writing. Teardown is two branches, not one, and the
ancestor proof (`git merge-base --is-ancestor`) gates each deletion.
