# Batch U close packet — the 2026-09-06 NIGHT-2 batch

**Consumer:** `[#590]` — the audit-index narrowing this batch exercised nineteen times.
Secondary: `[#528]` (suite once at integration), `[#605]`, `[#621]`.
Substantive citation by path: `docs/audits/2026-09-06-technical-batch-u-manifest.md`.

**Manifest:** `docs/audits/2026-09-06-technical-batch-u-manifest.md` · dispatched `75c84aa4`,
merged `25539b32` · **19 frozen lane contracts, two waves** · seats: dispatcher-N2, integrator-N2,
filings-N2, one session per lane.

---

## 1 · What the batch did

Nineteen contracted lanes landed across two waves, plus one lane added mid-batch by operator
amendment. A second, read-only batch of **fourteen folder censuses** ran beside wave 2 and landed
after it. The batch shipped executable gates rather than intentions: a merge that is **refusable**
without a review token, a lane-branch enum with **one** source, an ADR template whose
`Alternatives considered` is **REQUIRED** with existing ADRs warning rather than failing, a
derived-copies registry that moved drift detection from ship-gate to commit, and a fleet shape
grammar the tree seal reads as **data**.

**The batch's own reporting is the artifact, not its throughput.** Four lanes found their frozen
before-numbers stale and every one reported the true figure. The closing lane refused a clean
number. The integrator retracted its own claims twice. This packet records the misses in the same
detail as the deliveries, because a close packet that only records deliveries is the failure mode
the batch spent the night cataloguing.

---

## 2 · Lane disposition — measured on the spine

Reproduce:
```
git log --first-parent --format='%h|%s' main | grep "Merge branch 'worktree-lane-u-000-"
```

**THE COUNT AND ITS EXCLUSION — both plausible numbers are wrong unlabelled.**
```
that command returns                                                        18
minus worktree-lane-u-000-batch-manifest -- the MANIFEST branch, which matches
LANE_BRANCH_RE and sits on the spine looking exactly like a contracted lane,
but is NOT one of the 19                                                =   17 contracted lanes
plus W2-R (the 18th to merge, closing the batch)                              +1
plus declare-f2-intakes, ADDED MID-BATCH by operator amendment, not one of 19  (excluded)
```
A packet number grepped from the spine reads one too many; an earlier board read one too few.
**Neither is labelled in the tree.** *(integrator-N2 found this; it is the off-by-one that survives
review because both numbers look defensible.)*

### Wave 1 — 9 of 9
```
8444ba36  W1-1 batch-protocol-mechanisms   a merge is refusable without a review token
cdbe5680  W1-2 dispatch-receipt-is-work    hub half; Ch8 harvest verb; DONE means a commit on origin
f57d029d  W1-3 prompts-dir-guard           RECOVERED after a wrongful burial; PreToolUse leg UNARMED
ad9a7d5d  W1-4 branch-enum-parity          ONE source for the lane-branch enum, read by both ADR-85 organs
4b7ec261  W1-5 intake-id-next-free         all-refs allocator; the D8 id-70 move
0b2bc260  W1-6 trace-scorecard-consumer    13 rows, 9 carrying a measured number
5a0e739a  W1-7 batch-p-local               intake #71 P2/P3/P5; a read cache inert at 0.0% hit rate
ae13e1ae  W1-8 closures-local              224 proposals, ZERO rows closed, all three STRONG false-positive
9fed197f  W1-9 handoff-v71-build           v7.1 pack; probe-core as rows; P8's second leg and P11
```
**W1-3 is the one to read twice.** Three surfaces recorded it dead — "footprint already covered by
`f2802939`". One seat opened that SHA: it is `count_traces_today`, **W1-6's** footprint, containing
no prompts-dir guard. W1-3 was **wedged, not covered** — it armed a `PreToolUse` guard in its own
worktree *before* landing the code, and the guard then refused every call that would have undone it.
It landed its own guard, unarmed, under AMEND §A2. **One read falsified three surfaces.**

**W1-9 shipped a regression the batch did not see until the full suite.** See §11.

### Wave 2 — 9 lanes + 1 amendment lane
```
61728224  W2-U1 shape-spec-finalize      the fleet shape grammar becomes DATA the tree seal reads
c70fd8d0  W2-U2 seal-report-fleet        fleet seal report; headline NEGATIVE, reported as measured
0e68f4e9  W2-U3 carrier-floor-v150       floor v1.5.0 as mechanisms -- 3 of 5 have NO hub payload
b3bae03f  W2-U4 derived-copies-registry  11 copies registered; drift moves ship-gate -> commit
ec0d7912  W2-F1 adr-carrier-split        ADR-117; three review HIGHs RECORDED rather than answered
1ed350af  W2-F2 deploy-tool-override     the --consumer spelling, and the worktree case it serves
0e046af8  W2-F3 plugin-version-record    carrier #2 gets a durable record + a second drift surface
0298b4ed  W2-F4 adr-template-flip        Alternatives REQUIRED; existing ADRs WARN, new ones FAIL
5080e5c9  W2-F5 erratum-aj-second-pass   an erratum that publishes its own corrections
84f8186c  W2-R  release-commit           MERGED BY SHA (db37f3e2); 39 -> 14, and a refused 0/0
baf2c79c  declare-f2-intakes             ADDED MID-BATCH: intakes #78-#85 + ADR-117 provenance
```
**Three merge subjects are worth preserving verbatim**, because each reports a negative result as
the headline rather than burying it: *"a headline that is negative and reported as measured"* (U2),
*"three of five have no hub payload at all"* (U3), and *"three review HIGHs are recorded rather than
answered"* (F1).

---

## 3 · THE FINDING: check the support, not the conclusion

The batch opened on *"a cited SHA is checked, not inherited."* It closed on something narrower and
harder, because the first version did not survive contact with its own seats:

> **Check the SUPPORT, not the conclusion. A conclusion you agree with is where checking stops.**

**Six independent instances, six different artefacts, one mechanism:**
```
1  a cited SHA           f2802939 -- claimed to cover W1-3; it is a different lane's work
2  a cited PROSE claim   DECLARE-F sourced "THE ONE MEASURED OBSTACLE" from a comment in
                         ecosystem/deployed-versions.yaml that [#605] had ALREADY SUPERSEDED
3  two cited ENUM tokens `DRAFT` for an ADR status (no such member); `ACCEPT` where the intake
                         token is `ACCEPTED`
4  a cited CAUSE         "tonight's tasks/ churn" -- restated by THREE seats, none of whom opened
                         the row's own history
5  a cited PREDICATE     "57/88 carry Alternatives considered" -- CURRENT, and still wrong
6  a cited UNIT          the dispatcher's "canonical_freshness is 5 rows" -- it is 5 FILES in
                         2 FINDINGS, and the gate counts FINDINGS
```

**Instance 2 is the sharpest.** The stale contract number was **correctly derived from a stale
source**, so tightening contract *authorship* would not have caught it. And that module's own
docstring **admits at line 16** that it carried a false claim for months — a lane trusting the prose
would have reported **the opposite of the truth**. The remedy in its strongest form is
integrator-N2's: **measure by executing, because the prose in the file may be lying and may even
admit it.**

**Instances 5 and 6 defeat re-measurement, which is why they matter most.** A stale number is caught
by re-measuring — four lanes did exactly that successfully. But W2-F4's `57/88` was *current*: the
corpus writes that section under **three stems** (`Alternatives considered` 45, `Rejected
alternatives` 6, `Alternatives rejected` 3) plus three numbered forms, so the strict predicate
returns **46** and the permissive **58** — **11 apart, with nothing in the figure saying which was
used.** Re-run the same predicate and you reproduce the same wrong answer with fresh confidence.
**Only re-deriving the predicate catches it.** So the standing clause is not "re-measure, never
restate" but **"re-derive the predicate, then re-measure."**

**Instance 6 was committed by the dispatcher in the same brief that warned about instance 5** — and
handed to every lane all night.

### 3.1 · Mutual checking did not catch it
```
1  dispatcher : "the batch created the third RED tonight by filing rows"      FALSE (cause)
2  integrator : corrects the cause -- CORRECT -- supported by
                "dadda5fc touches ZERO files under tasks/"                    FALSE (support)
3  dispatcher : accepts, verifies the CONCLUSION, substitutes
                "those commits are not on main"                              FALSE (support)
4  integrator : corrects that too, and explains BOTH probes
```
**Both headline conclusions were right. Both supporting clauses were false.** At every step the
receiving seat checked the conclusion and neither re-derived the support — **because the conclusion
was right, which is when a reader's guard is lowest.** Two careful seats, each checking the other,
and a false statement still reached this packet twice. **Both retractions are left visible on the
boards rather than deleted; the deleted version teaches nothing.**

### 3.2 · A seat can verify its own innocence and still pass on a false cause
Three seats stated the "tasks/ churn" theory. Each checked whether **its own diff** touched `tasks/`
— a question about **itself**. None asked what the **cited ids currently resolve to** — the question
about the **claim**. Both are diligence; only the second could falsify the theory.

---

## 4 · Five instruments that lied, in one night

Every one produced a **plausible number** and none announced itself.
```
1  git show --stat        ELIDES long paths -> a path-grep counted 0 of 9 real rows
2  git log --since=DATE   evaluated in the LOCAL timezone -> a commit dated 2026-09-06 05:05 +0200
                          is EXCLUDED by --since=2026-09-06.  "No commits" offered as proof of absence
3  WARN-line counting     consumer_at_landing warns on CITATION, not state: 42 lines printed,
                          19 dispositioned, 23 undispositioned. A closure counting lines chases 42
4  substring probe over a changed-file set -> 0 hits across a 109-file diff; MISSED
                          templates/handoff/v5/ and verify_handoff_probes.py, and nearly filed the
                          batch's OWN regression as inherited
5  git diff main <branch> WRONG BASE -> reported 39 non-audit files per census lane (main's own
                          batch-U content, seen in reverse). Diffing the MERGE BASE gives 1-2.
                          A contract violation that was never there
```
**Instruments 1, 2, 4 and 5 return an empty or zero result** — the single easiest output to mistake
for evidence, because nothing about it looks like a failure. **An absence claim needs a probe whose
failure mode is not silence.** Instrument 3 is the same disease inverted: a number that looks
measured because a command produced it.

Each was caught the same way — **by a second, differently-shaped probe**, never by staring harder at
the first.
---

## 5 · One mechanism, three vantages — and the anchor rule revised three times

`journal_spine_anchor` reads the spine from the **shared `main` ref** and the JOURNAL from the
**committing tree**. Every observable face appeared:
```
1  a LANE reading a stale local main                  lag -- `git merge origin/main` clears it
2  a SEAT reading an UNPUSHED local merge as fact     the anchor exists where nobody can fetch it
3  the DISPATCHER reading a stale CACHED origin/main  told a blocked lane it was still blocked
                                                      AFTER the push had landed
```
For (3), **every row of the table was individually correct and the conclusion was false.** The
discriminator is **`git ls-remote`** — ask the remote, not the cache.

**The rule was revised twice by lanes, each time strictly better:**
```
v1  dispatcher   both legs False = REAL GAP -> STOP and escalate
v2  W2-U3        both False -> REPORT AND KEEP RETRYING, never stop
                 (indistinguishable from a lane's vantage; retrying is right under both causes,
                  stopping is wrong under one)
v3  W2-U4        both False -> SYNC AND RETRY IN A LOOP. Never stop, never BARE-retry.
                 `fetch + merge origin/main + push` as ONE loop -- a bare push retry NEVER FETCHES,
                 so the integrator's anchor never reaches your tree and the range never goes clean
```
W2-U4 established v3 over **four separate refusals on foreign merges**. **v2 was right about not
stopping and silent about the mechanism**, so a lane obeying it literally could spin indefinitely
while looking patient. **The rule reached its correct form only because each lane reported what it
actually did rather than confirming the pin it was handed.**

---

## 6 · Clauses that cannot be satisfied as written

- **"`git stash list` must be empty at STOP".** `refs/stash` lives in the **common git dir**. The
  clause reads per-lane and measures **repository-wide**: with N lanes it is unsatisfiable for
  whoever stops last-but-one, and **the literal way to satisfy it is to drop a peer's live WIP.**
  W2-F1 saw an entry that was not its own, did not touch it, and named its owner — the correct
  behaviour, and not what the clause asks for. The measurement is also **time-varying**, so the
  clause is only meaningful at CLOSE.
- **"`PACKET-MERGED wave-1`"** — unsatisfiable while one lane was believed dead. Resolved as *every
  lane that will hand back*; wants ratification.
- **Teardown "no leftovers"** would have been satisfiable at any moment by forcing removal of four
  **live** worktrees. It was not forced. **Both hygiene clauses share a shape: literal satisfaction
  causes data loss.**

**"No leftovers" was satisfied honestly.** All four locked worktrees cleared **on retry, once their
sessions exited**, including a husk whose busy-resource error was a node-grandchild transient rather
than a live seat. **No forced removal at any point.** 13 of 15 origin lane refs deleted, each
verified `merge-base --is-ancestor ... main` **first**; 2 kept deliberately. **A removal that had to
wait for a session to exit is a different fact from one that worked first time. Both are acceptable;
only the first is honest.**

---

## 7 · The integrator mechanic verdicts a SHA and merges a BRANCH

```
audit.py handback     verdicts a SHA
lane-integrate §2     prescribes  git merge --no-ff worktree-lane-<slug>   <- a BRANCH NAME
```
A lane branch ref lives in the **common git dir**, so a lane that commits after handing back
**advances the ref under the integrator silently**. Measured across one arc's four merges: three
matched; **U4 did not** (`origin 8f817c3d` vs local `dafcfeff`) — precisely the lane whose local ref
had moved ahead of origin, **invisible to every check the checklist runs.** **Fix is one word: merge
the SHA you verdicted.**

**The reasoning for accepting that overrun matters more than the outcome.** `dafcfeff` was 3 files
and cosmetic, and the targeted run returned **50 passed** where `8f817c3d` gives 49 — **so the tests
witnessed the tree actually merged.** A real check, not a rationalisation. But it held **only
because the extra commit happened to be trivial**: had it been substantive, **nothing in the process
would have caught it**, and the batch would have shipped an unreviewed change under a review tally
that never saw it. **A near miss whose safety came from luck is a finding, not a pass.**

The checklist was **not patched mid-queue**, on the principle that **the seat executing a checklist
is not the seat that should silently rewrite it while executing it.** It is carried as its own arc.

**The defect was applied to the batch's own last merge within the hour:** W2-R was merged **by SHA**
(`db37f3e2`) after checking claimed == local == origin, and W2-R committed nothing after handback
and stated the full 40 characters.

---

## 8 · A machine-read surface makes formatting semantic

*(integrator-N2's formulation — the most transferable thing the night produced.)*
```
audit.py    check_doc_code_edge tokenizes a LINE-INITIAL "# rule:" as a MARKER.
            a comment wrapped so prose landed as "# rule: the drift edge AF-1 exists to close."
            => a marker declaring rule id `the` => code_orphan: the => RED since b429d9f4
            THE SENTENCE WAS CORRECT ENGLISH AND CORRECT ABOUT THE CODE. Only its LINE BREAK
            was wrong. Fix = reflow (428ab05a). No code, no behaviour, no marker changed.

ADR-117     gen_claude_rosters.py scrapes the ADR STATUS LINE VERBATIM. an inline HTML comment on
            that line landed WHOLE in .claude/generated/recent-adrs.md -- @-imported into CLAUDE.md,
            i.e. BOOT-TIME CONTEXT FOR EVERY SESSION. Byte cap passed, --check exit 0.
            NO GATE OBJECTED.
```
**Both are invisible to a reviewer reading for meaning**, because in both the meaning was fine. The
failing property — where the line broke, which line the text sat on — is one **nobody reviews a
comment for**. Both were silent: one RED stood in **nobody's lane footprint** so no lane owned it;
the other failed nothing at all.

**A defect that trips no gate and belongs to no owner has no natural discoverer.** The remedy applied
is cheap and right: **an inline note at the wrap point**, addressed to the next author who would
reflow it for readability. Generalised: **any line whose formatting is load-bearing should say so on
itself.**

**Corollary, violated by three seats at once:** the comment is at `audit.py:4419`, **not 4271**. Two
lane reports and the fix all carried a locator **wrong by 148 lines**. The fix landed correctly
because the integrator ran `sed -n '4265,4278p'`, **saw an unrelated docstring, stopped, and
re-located by grepping** — it **abandoned the locator the moment it did not resolve to what it
expected.** That noticing is the recoverable skill; **cite by anchor text, not by line number.**

---

## 9 · Organs that warn on CITATION rather than state

- **`consumer_at_landing`: a dispositioned WARN still PRINTS.** Measured at close: **42 WARN lines,
  19 dispositioned, 23 undispositioned.** A closure counting lines chases 42 to an unreachable zero.
  Read the `new/undispositioned` verdict line.
- **A grep for a RETRACTED figure hits the branch that retracts it.** `9.1x` appears exactly once in
  W2-F5's diff — in the retraction that kills it. Counting occurrences would have **held the lane
  that fixed the problem.** Retractions must say the number out loud.

**Where an organ reports citation rather than state, counting is the wrong instrument and reading is
the only one.**

---

## 10 · W2-R: the closing lane refused a clean number

**39 → 14, with a stated remainder.** Measured at `59b82aff` with
`PYTHONUTF8=1 uv run --locked python scripts/audit.py ship-gate`, 199 lines captured whole, exit 1,
verdict line read as `39 new/undispositioned WARN(s)`. The decomposition **sums exactly**:
`consumer_at_landing 23 · funnel_coverage 5 · proof_layer 4 · canonical_freshness 2 ·
adr_status_grammar 1 · doc_claims 1 · doc_code_edge 1 · generated_artifact_freshness 1 ·
undeclared_edges 1`.

Predicate **re-derived from `cmd_ship_gate` source**, not from any report:
```
undispositioned = Finding.status == "warn" AND _match_disposition returns None
                  (entry.organ == check_name AND entry.match is a SUBSTRING of the evidence)
stale           = register ids that matched no live WARN
```

**Four things it did that the batch should be judged by:**
1. **Both stated targets found stale** — its contract's `3/3` and the dispatcher's `31/7`.
2. **Declared its own measurement pair NOT CLEAN**, because `main` moved between halves.
3. **Credited one gain to a peer** — `doc_code_edge` 1→0 came from the integrator's reflow, not from
   itself. **A lane quietly absorbing a peer's fix into its own totals would have been invisible;
   no gate could catch it.**
4. **Refused to re-stamp three `last_reviewed` files it had not re-read end-to-end.** The stamp's
   entire meaning is that someone re-read the document. **Stamping to make a number fall is a false
   claim in the most literal sense this repo defines.** The integrator states it would have refused
   the cleaner figure too.

**39 → 14 with a stated remainder is a better close than 0/0 would have been.**

---

## 11 · The full suite ran, and it caught a regression THIS BATCH SHIPPED

```
21 failed, 5333 passed, 3 skipped in 2182.66s (36:22)
-n 4 --dist worksteal --max-worker-restart=0    DEVIATION from the prescribed -n auto, on the record
   reason: 2.41 GB free against 16 logical CPUs; 16 workers is exactly what OOM-killed three
   earlier attempts tonight
0 orphaned workers after the run
```

**FIVE OF THE 21 ARE OURS.** W1-9 `handoff-v71-build` (`5cb41d6b`) rewrote
`templates/handoff/v5/PROBES.md.tmpl` (110 lines), `HANDOFF_BOOT.md.tmpl`, `RESIDUAL.md.tmpl` and
`verify_handoff_probes.py`. **It updated the one test file it owned and left two sibling suites
pinning the old shape.**
```
tests/test_gen_handoff.py:74,89     assert len(...) == 13    live 15
tests/test_gen_handoff.py:266,283   assert len(...) ==  5    live  6
+ test_suffixed_bundle_probes_resolve_against_their_own_directory
+ test_handoff_modes.py::test_boot_carries_both_postures
```
**15 IS THE TRUTH, NOT TODAY'S OUTPUT.** The template defines exactly 15 probe rows
(`P0a P0b P0c P1a P1b P2 P3 P4 P5 P6 P7 P8a P8b P9 P11`): P8 split into P8a/P8b (+1) and P11 landed
(+1) = **+2 over 13** — the commit subject verbatim.

**Two opposite diseases were live in the same suite run:**
```
test_gen_handoff   the ARTIFACT deliberately grew   -> the PIN is stale   -> UPDATE the pin
test_vi_batch1     the EXPECTATION was right, the CORPUS moved -> do NOT update the pin
```
**Getting that backwards in either direction is the wrong repair.**

**Not patched, on a ruling rather than timidity.** Two are clean literal bumps; **three are not** —
one asserts a list of probe *outcomes*, one asserts `'navigation gate'` in a boot doc the v7.1 pack
rewrote. That is real repair inside another lane's footprint at the end of a batch the operator has
ruled STOPS. **It is the strongest candidate for the next batch's first arc.**

**THE LANE'S MISS IS STRUCTURAL AND BOTH HALVES ARE REQUIRED.** A lane runs **targeted** tests by
design, so it **cannot** see a sibling suite pinning its own artifact. That is precisely why [#528]
puts the full suite once at integration. **Success of the cadence, miss by the lane** — neither
statement alone is honest.

### 11.1 · Attribution at the confidence actually held
```
 5  OURS          the handoff-v71 sibling suites
 2  INHERITED     test_the_class_enum... (selection-triggered, NOT parallelism, `-n 0` does NOT
                  dodge it, NOT a dual import; blame PLAUSIBLE for W2-U1 but NOT WITNESSED --
                  nobody ran that selection at df88f767)
                  test_vi_batch1...      (NINE DAYS RED; [#577]/[#584] resolve to CLOSED rows,
                  status set in 11c2322e on 2026-08-29, an ancestor of batch U's OWN wave-1 base)
 4  ONE FACT, TWO SURFACES -- consumer_at_landing, proof_layer, funnel_coverage, canonical_docs are
                  "committed baseline vs live measurement" tests. W2-R could not close them and
                  neither can a test
10  UNATTRIBUTED  reported as such rather than presumed inherited
```

### 11.2 · The substrate claim is narrowed
An earlier finding reported the full-suite number as **unavailable from this substrate** — four
attempts, three OOM kills. **It was available once the box was quiet.** W2-R's lane, the gate
processes and pytest together measured **under 220 MB**; what exhausted the machine was
**accumulated finished sessions plus the operator's own desktop applications**. That is a
**lifecycle** problem, not a substrate one, and far cheaper to fix than "integration needs a
different machine."

---

## 12 · The SWEEP — 14 read-only censuses, and a missing manifest

Fourteen folder censuses ran **beside** wave 2 and landed after it: thirteen on cloud, **S-13 local
by declared deviation** (a cloud session is bound to the hub repo alone and cannot see sibling repo
roots at any path, so on cloud its one job was impossible). All verdicts are **PROPOSALS**; nothing
was moved, deleted, edited or renamed. The execution batch is a later act, by operator ruling.

**A coupling scan ran before launch:** all eight live wave-2 branches diffed against main, **zero
census-path collisions**, zero pre-existing census files.

**THE SWEEP HAS NO COMMITTED MANIFEST, AND THAT IS THE DISPATCHER'S DEFECT.** Fourteen lanes were
dispatched against a batch whose manifest never landed; the censuses declare `closed_by:` a file
that does not exist. **This packet already carries the rule that forbids it** — batch U's own wave-1
lanes booted before their manifest reached main, and the durable fix recorded at the time was
**manifest and contracts must land in ONE commit**. The dispatcher recorded that rule and then
dispatched an entire batch with no manifest at all, having run the coupling scan and treated it as
sufficient.

**RULING — deliberately the conservative one: merged as ORDINARY DOCS ARCS, anchored in one group,
no ADR-110 exemption claimed, and the missing manifest was NOT written.**
- A manifest committed **at dispatch** is evidence; one committed **after fourteen lanes have
  landed** is decoration that retro-licenses finished work, and would make `batch_manifest` report
  an open batch that was never opened.
- **Creating a manifest is opening a batch**, which the operator has ruled stops.
- **The censuses never needed the exemption.** Read-only, docs-only, single-file arcs; group
  anchoring costs anchor commits and nothing else. **The exemption spares a long queue from anchor
  churn; it does not make merges legal.**

**The dangling `closed_by:` lines are left pointing at nothing on purpose**, cause recorded — because
**a dangling reference that someone later "fixes" by writing the missing manifest is exactly how a
fabricated artifact enters the record.**

**A cloud/Gemini conflict, unresolved and structural:** the SWEEP was designated *the first Gemini
workload* **and** pinned to cloud to burn quota before reset. `gemini` is a **local** CLI, so the
thirteen cloud censuses had no reader. **S-13, the one local lane, is the entire evidence base for
that question** — it reports `fan-out: PARTIAL`, names the binary and version `0.56.0`, and refuses
to simplify the CLI's state to "clean" or "absent". **Cloud quota and the Gemini fan-out are
mutually exclusive as currently built.**

**S-13 also disagrees with W2-U2 on the record rather than reconciling** — `demo-prep/output/` is
`UNDETERMINED` where U2's seal says WAIVE, argued on merits it calls orthogonal. **Two independent
derivations that agree are evidence; two talked into agreeing are one derivation.**

---

## 13 · Dispatcher defects, in full

1. **Ended a turn on a peer wait**, and wave 2 did not launch (AMEND §A1). A dispatcher's wait is
   now a **sleeping poll until the condition is witnessed**.
2. **Asserted a discharge from a SHA never opened** (`f2802939`) — and recorded it as
   self-criticism, which made it look verified.
3. **Told the integrator "consumer repos read-only, do not merge win-tooling."** A later, more
   specific operator ruling authorised it; the NO was withdrawn on reading the ruling itself.
4. **Relayed a wrong mechanism for a real RED** — "xdist dual-import, passes at `-n 0`". Measured:
   **selection-triggered, `-n 0` does NOT dodge it, no dual import.** W2-R would have walked into it
   expecting serial to dodge it.
5. **Read a stale cached `origin/main` as fact** and told a blocked lane it was still blocked after
   the push had landed.
6. **Contracts cite `STATUS-DISPATCHER-N2.md` section 5**, which the ≤5 KB rule rolled to archive.
   **Two lanes hit it.** A contract cannot cite a rolling, size-capped board.
7. **A unit error handed to every lane** — `canonical_freshness` "5 rows" where the gate counts
   **findings** (5 files in 2 findings). Written in the same brief that warned about exactly this.
8. **Dispatched 14 lanes with no committed manifest** (§12).
9. **Stopped a lane before it handed back.** Reaping sessions for memory, the dispatcher selected on
   `state == done` — *a session's claim about itself* — and terminated S-13, which had never sent a
   HANDBACK. **Its only reporting channel was destroyed by the seat waiting for the report.** The
   merge then proceeded on **verified artifact evidence** (session absent; local == origin ==
   `2d791e0a`; exactly one file against the **merge base**; id-shaped consumer token; verdict
   counts) with the limit stated: **the artifact is complete and well-formed; the lane's own verdict
   on its completeness does not exist.**

---

## 14 · Open for the operator

1. **win-tooling W1-2 is HELD.** The 11:27 ruling's condition (2) requires **HIGH = 0**; the
   artifact reads **1 Critical + 7 High**, one **NOT FIXED / ESCALATED** (the `gh auth status`
   admission gate, which the lane declined to change because its frozen contract names it).
   **Does condition (2) mean raw or unresolved HIGH?**
2. **`gpt-5-codex` is unusable on this account** ("not supported when using Codex with a ChatGPT
   account"); default is `gpt-5.6-sol`. **Two independent lanes**, neither worked around it. **Every
   `review=codex` tally in this batch was earned on a different model than the contracts assume.**
   Related: `codex exec` **hangs ~20 minutes reading stdin** without `< /dev/null`; one lane's first
   invocation produced nothing and it **did not report the empty run as clean**.
3. **Cloud quota and the Gemini fan-out are mutually exclusive as built** (§12).
4. **S-13 ran LOCAL against a contract saying CLOUD** — declared deviation; on cloud it could not
   have read one consumer root.
5. **The five handoff-v71 sibling failures** need their own arc; three are real repair inside
   another lane's footprint (§11).
6. **The `ecosystem/deployed-versions.yaml` `win-tooling:` prose comment** that [#605] superseded is
   still present. **The next planner reopens a closed row from it.** Deliberately not fixed as an
   opportunistic edit.
7. **`git stash list` and teardown clauses are unsatisfiable as written** (§6) — both require data
   loss to satisfy literally.
8. **`lane-integrate` verdicts a SHA and merges a branch** (§7) — carried as its own arc.
9. **`test_vi_batch1` freezes against row LIFECYCLE, not corpus growth** — pinning "the shape of the
   failure" must mean shape across **open→closed transitions**. **Editing the expected list to match
   today's output re-freezes against a tree that moves at the next closure.**
10. **INSTALL.md is refused at consumer roots** by `rule_a_violation`, while `README.md` and
    `AGENTS.md` pass by dated ADR-101 amendments. Because W2-U1 made the allowlist **data**, the
    remedy is now **a one-line add to `ecosystem/fleet-shape-spec.yaml` `root_allowlist.files`** — an
    operator act, but a cheap one. **The fix got cheaper because an earlier lane in this same batch
    turned a hard-coded rule into data.**
11. **16-vs-19 lane count** in the manifest header · **the DAY window has no manifest on main** ·
    **`docs/intake-031-two-chats` HOLD at `949b8961`** (**not** the stale `b6b7cb08` still cited in
    NIGHT-2 §2) · **MEMORY.md compaction** declined again, no drop list ruled.

---

## 15 · Honest limits

- **The suite verdict is real and not clean.** 21 failed. **10 are UNATTRIBUTED and are not claimed
  as inherited.** The `-n 4` deviation from the prescribed `-n auto` is recorded, not hidden.
- **`test_the_class_enum` attribution to W2-U1 is PLAUSIBLE, NOT WITNESSED.** Nobody ran that
  selection at `df88f767`. "Not caused by this merge" was witnessed; "caused by that one" was not.
- **Several numbers in this packet are CARRIED, not VERIFIED**, and are labelled where they appear.
  The integrator explicitly did not verify W2-R's 39/8/0, noting only that the decomposition sums to
  the verdict — **a consistency check, not a measurement.**
- **S-13's completeness is inferred from its artifact, not reported by the lane** (§13.9).
- **Criterion E is NO.** Interruptions were not zero, a lane died, a lane was killed by its own
  dispatcher, and the batch shipped five test failures.

---

## 16 · Owed before any next session

> **daemon restart + PreToolUse arming owed before any next session**

Recorded verbatim at the operator's instruction. **It is a precondition on the next session, not a
task for a lane.** W1-3's guard code is on `main` and the guard is **deliberately UNARMED** under
AMEND §A2 — because W1-3 armed a `PreToolUse` guard in its own worktree *before* landing the code,
and the guard then refused every call that would have undone it. **A `PreToolUse` hook takes effect
for sessions started after it**, so arming it mid-session repeats exactly that failure.

**BATCH U STOPS HERE.** No new batch is opened by any seat in this session. The next batch — W-G1
graph + `orphan_census` first — is contracted by the **browser**, after the daemon restart.

**The temptation this close creates, named so it is refused:** fourteen censuses have just produced a
large body of RETIRE / RELOCATE / ARCHIVE **proposals**, and the pull at the end of a productive
night is to start executing them while context is warm. They were commissioned **read-only**
precisely so that measuring and moving never happen in the same breath. **A seat that begins the
cleanup because the census is fresh has destroyed the evidence the census exists to provide.**
