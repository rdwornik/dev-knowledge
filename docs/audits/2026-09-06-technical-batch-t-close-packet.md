---
last_reviewed: 2026-09-06
status: active
owner: Rob
---

# Batch T close packet — 2026-09-06 NIGHT

> **This file CLOSES batch T.** `docs/audits/2026-09-06-technical-batch-t-manifest.md` names it as
> its `closed_by:`, and `batch_manifest.open_batches` probes `git cat-file -e HEAD:<closed_by>` — so
> the batch is open exactly while this path is absent and closed the moment it is committed. Landing
> it ends the ADR-110 declared-integration-arc exemption for every lane. It was therefore merged
> LAST, deliberately, after every other arc.
>
> Written by `dispatcher-T` per §1 Close of `BATCH-2026-09-06-NIGHT-CONTRACTS.md`, as amended by
> `AMEND-BATCH-T-001`. Companion surfaces, none of them restated here: the dispatch-time record and
> AMENDMENT 1 in the manifest above; `to-browser\STATUS-DISPATCHER.md` for the step-0 evidence board
> and my post-launch corrections; `to-browser\RATIFICATION-2026-09-06.md` (filings-N) for the dawn
> list; the integrator's own census for merge-by-merge detail.

## 1 · Per-lane before → after

Fifteen lanes after A3 widened the batch by one. **Seven merged, one landed by ruling with no commit,
one codespace lane handed back and is HELD, one codespace lane produced nothing at all, three cloud
lanes and one local lane were unmerged at close, one was HELD at the dispatch gate and never
launched.**

```
LANE  SLUG                          SUBSTRATE   OUTCOME AT CLOSE          MERGE
3.1   lane-t-000-v2-logs            local       MERGED                    b8f94008  7 files  +327 -27
3.2   (42-v3-ecosystem)             local       HELD -- NEVER LAUNCHED    --
3.3   lane-t-000-v4-archive-report  cloud       unmerged at close         --
3.4   lane-t-000-v5-closures        cloud       BLOCKED -- awaiting human --
3.5   lane-t-000-aj-research        cloud       unmerged at close         --
3.6   lane-t-000-nc1-clear          local       HANDBACK, hard-fail 2->0  c4fdc4e6
3.7   lane-t-000-shape-seal         local       MERGED, FINAL, both halves 6e385c67  1 file   +288
                                                                          815e13c0  3 files  +335 -7
3.8   lane-t-000-batch-p-audit-speed CODESPACE  attempt 2 HANDBACK, HELD  22f06b21 (not merged; #71)
3.9   lane-t-000-trace-scorecard    CODESPACE   DEAD -- never produced    --
3.10  lane-t-000-reds-spine         local       MERGED                    d76c8e09  4 files  +209 -13
3.11  lane-t-000-playbook           local       MERGED (freshness half)   aaa1e96a  2 files  +59 -13
3.12  lane-t-000-readme             local       MERGED                    f6d166d7  1 file   +57 -10
3.13  lane-t-000-browser-floor      local       DONE at NO-COMMIT         -- (by ruling)
3.14  lane-t-628-v1-release         WAVE 2      see §6
3.15  lane-t-000-freshness-unstamped local      MERGED                    0d2db2f7  7 files  +80 -29
```

Batch scaffolding, for completeness: `c004ac8c` landed the manifest AT DISPATCH before any lane
(14 files, +3058); `30f0b0a3` drained the spine wedge; `fa18d06a` / `736b5fe7` / `df4f7b61` /
`25b8bd10` and `92b7aaa9` are the integrator's anchor arcs; AMENDMENT 1 is `89a2fa04`, merged as
`3dbff773`. Main stood at `92b7aaa9` when this section was written.

**Integration cost, from the integrator's own record.** Every lane merge ran 9-28s against a
5-minute docs bar, and **every one logged NO REVIEW** — no lane reported a terra tally, and per C-7
an empty invocation is NO REVIEW, never clean. That is an honest limit on this batch's assurance, not
a pass: seven lanes merged without a review artifact, and the packet should not be read as though
they carried one.

**Substantive before → after, one line each, for the lanes that changed the tree:**

- **3.1 v2-logs** — `logs/` retention had a mechanism and **no caller**; after, the mechanism is
  wired and the dead path is gone.
- **3.7 shape-seal** — the seal report landed first (report half), then the intake DRAFT superseded
  it after I released the serialization. Its `intake-id: 73` was derived by scanning every
  `docs/intake/` blob reachable from ANY ref (269 blobs, 72 ids, max 72, no gaps) rather than by
  listing the folder — **the method matters more than the id**, and §4 explains why.
- **3.10 reds-spine** — a suite RED fixed **in the test, without weakening the check**. The
  distinction is the deliverable.
- **3.11 playbook** — freshness half merged; its `[ratification-pending]` half is HELD.
- **3.12 readme** — the root `README.md` front door (ADR-114's sanctioned Tier-1 file).
- **3.13 browser-floor** — produced `BROWSER-SEAT-FLOOR-DRAFT-2026-09-06.md`, its `.sha256`, the PIN
  file and the seat skills zip, **all in `to-browser\` and none in the repo**, because intake #68
  names no in-repo location for it. That absence is QUESTION item 2 and is the reason the lane
  correctly created no repo path.
- **3.6 nc1-clear** — handed back at `c4fdc4e6`. **hard-fail 2 → 0 · undispositioned 52 → 3 ·
  stale 4 → 0 · PENDING 7.** `routing_agreement` is CLEARED ("agree: 4 role(s)") — the L0 copy read
  `adversarial | sol` against a table rebound to `codex` at `5be038ff`. Both A2 acts executed:
  `protocols/OPERATOR-INTERFACE.md` genuinely re-read (no change needed) and then stamped.
  `~/.claude/ROUTING.md` is re-rendered and left UNSTAGED — separate repo, correctly outside §3.6's
  footprint, and **OWED to the operator**. This is the lane the wave-2 gate turned on.
- **3.15 freshness-unstamped** — the AMEND-created lane. **`unstamped 8 → 1`**, and the remaining 1
  is `protocols/HANDOFF_BOOT.md`, excluded BY RULING and named: its sha256 is the ROLE PIN every
  browser seat carries, so stamping it breaks every booted seat until the operator re-uploads.
  Measured at `a39edb2d`:
  `3b6d5691294e149844e16a2965d27ff49d2e95e3a69d138f6f77a33ecdef5858`.

### The two codespace lanes

**3.9 trace-scorecard is DEAD and produced nothing.** 45 turns of real work, cut off mid-sentence
waiting on a background test, never committed, no branch on origin or locally. **I then stopped its
codespace at 04:33 to free the cap-2 slot for 3.8's re-dispatch** — the cap was 2, both slots were
held by failed lanes, and I judged one re-dispatch worth more than two dead ones. My call, recorded
as mine.

**3.8 batch-p-audit-speed LANDED on attempt 2, and it is the best technical result of the night.**
`HANDBACK worktree-lane-t-000-batch-p-audit-speed @ 22f06b21 [code] [ratification-pending]` — 114
turns, 36 minutes, HELD on intake #71 (DRAFT) and therefore going to dawn with its id rather than to
main.

```
git spawns   1310 -> 645    (-51%)
file reads  13854 -> 4170   (-70%)
health tier  spawns 79 -> 79 (the fixed check is ship-only), reads 4534 -> 4028
```

**The root cause was not what intake #71 guessed.** Not Python-level duplicate git calls —
`check_review_artifact_coverage` in `scripts/audit.py` spawned THREE git processes per spine entry in
a loop, on a `TIER_SHIP`-only check, which is exactly why it never appeared in `health` and only ever
cost ship-gate. ~90 lines in `scripts/audit.py` alone. **Criterion 3 held: `health` and `ship-gate`
output diffed BYTE-FOR-BYTE IDENTICAL before and after**, RED against RED, verified twice. Full suite
in its own substrate: 4959 passed both sides, the same 39 pre-existing worktree-environment failures
before and after, confirmed by a `git stash` A/B rather than assumed. Zero new dependencies.

**Attempt 2 vindicates the diagnosis of attempt 1.** Attempt 1 refused on locators it said did not
resolve — one of which I verified DOES exist on `origin/main` — and returned a clean receipt over
zero work. Attempt 2, given a pre-resolved locator table and an explicit
`git cat-file -e origin/main:<path>` re-check, executed the same contract and landed. **The defect
was the contract's locator handling, not the lane.**

## 2 · Deviations

**Mine, and the expensive one is first.**

1. **The manifest branch wedged the whole repo (~04:00).** I named the batch-manifest worktree
   `worktree-batch-t-manifest`, which carries no `lane-<letter>-<id>-` segment and so does not match
   `validate_branch_naming.LANE_BRANCH_RE`. The ADR-110 exemption keys on that regex — so **the one
   merge that OPENS a batch received no exemption**, and its unanchored merge blocked every commit
   in every tree until the integrator drained it at `30f0b0a3`. **Measured cost, from the
   integrator's record: twelve lanes wedged at once**, because `journal_spine_anchor` runs at the
   `always_run` commit gate and so blocked the FIRST commit on every branch simultaneously. Re-cut as
   `worktree-lane-t-000-manifest-amend` for the amendment. The integrator records `c004ac8c` as
   theirs to have merged; the branch NAME that cost the exemption was mine, and both halves belong in
   the record.
2. **My step-0 ship-gate breakdown was wrong, and it is why this batch needed an amendment at all.**
   I captured 62 lines of a 148-line output, grepped the truncated tail, and reported three organs
   summing to **24** against a headline of **36** I had recorded correctly in the same block. The
   lines I never saw included `canonical_freshness`'s eight ungated-and-unstamped files, owned by no
   lane at any wave — which made wave-1 ship-gate GREEN **unreachable by construction** while 3.14's
   launch was gated on that GREEN and 3.14 was itself the lane that re-stamps `CLAUDE.md`. Circular.
   The integrator found it; the architect confirmed it as "the contract's own error"; A1 and A3 are
   the fix. **Had I read my own output in full at step 0, no amendment would have been needed.**
   A truncated capture is a claim, not evidence — the repo's own rule, applied to my own instrument.

   **Related count correction, measured by lane 3.6 and accepted:** `consumer_at_landing` live was
   **21, not 22**. I pinned 22 and `AMEND-BATCH-T-001` §A5 restated it, so the architect and I were
   wrong together. The discriminating reason is 3.6's:
   `2026-09-01-technical-article-harness-substrate-brief.md` is already dispositioned by
   `warn-consumer-article-harness-substrate-brief`, so it never entered the UNDISPOSITIONED set —
   **a count of a set is not a count of its superset.** No act turned on it either way.

   **And one finding cleared itself through this packet's own sibling:** §3.6's `funnel_coverage`
   target (`research-aj-second-pass`) self-resolved because the batch-T MANIFEST names it, so
   `manifest_links` resolves it `explicit`. The dispatch artifact discharged a finding as a side
   effect of naming its own inputs.
3. **I misread the ADR-85 anchor predicate twice in ten minutes**, both times by grepping JOURNAL for
   a MERGE's own hash, which returns nothing by construction. The predicate anchors on a SHA the
   merge INTRODUCED. Compounding it, `check_journal_spine_anchor` reads the SPINE from `main` and the
   JOURNAL TEXT from the WORKING TREE, so a lagging tree reports gaps that do not exist. I escalated
   a non-existent treadmill to the integrator on the strength of it. The fix both times was
   `git merge origin/main`. Recorded because it is the fourth misreading of this predicate in one
   batch, including once by the integrator — a predicate misread that often is a documentation
   defect, not four independent lapses.
4. **Batch width 12 → 15 against the 4-6 ceiling** in STANDING_RULINGS §U(b). Recorded pre-launch on
   the operator's explicit GO for a "12-14-lane night batch"; A3 then widened it by one more.

**Not mine, recorded as batch facts.**

5. **Both codespace lanes failed on their FIRST attempt, and neither failure was visible in its
   receipt.** 3.8 attempt 1 returned `Ok:True`, `RemoteExitCode:0`, `is_error:false`, `status:DONE`
   and **did zero work**, refusing on locators it said did not resolve — including one I then
   verified DOES exist on `origin/main`. 3.9 did 45 turns of real work, was cut off mid-sentence
   waiting on a background test, and **committed nothing**, losing all of it.

   **The re-dispatch fixed 3.8 and 3.9 was never re-dispatched.** Attempt 2 got a pre-resolved
   "locators you cannot resolve here" table plus a `git cat-file -e origin/main:<path>` re-check, and
   landed at `22f06b21` after 114 turns. 3.9's fix — inverting the order to **COMMIT BEFORE YOU RUN
   THE SUITE** — was written but never dispatched, because I stopped its codespace to free the cap-2
   slot for 3.8. **So the substrate produced one recovered lane and one dead one, and the difference
   between them was a slot, not a capability.** See §4.0 and §4.5 for the general findings.
6. **The integrator changed merge order mid-batch and was right to.** Cloud lanes merge LAST, each
   merged+anchored+pushed as one unbroken act, because `claude/lane-t-000-*` branches are UNEXEMPT
   under `LANE_BRANCH_RE` and merging one early would re-wedge exactly the seats still working.

## 3 · HOLD queue

The authoritative queue is **`to-browser\RATIFICATION-2026-09-06.md` §8 and §8b** (filings-N). Not
restated here — a second copy of a HOLD queue is a drift generator. What belongs to me:

- **3.2 was HELD AT THE DISPATCH GATE and never launched** — the only lane in the batch that did not
  run at all. Two independent evidence-backed blocks from intake #42's own amendment text: a C-6
  Done-when mismatch and a C-8 block. It is filings-N's §8b, "a VISIBLE ask that did not run", and
  its dawn item is QUESTION item 1.
- **3.8 hands back `[ratification-pending]`** per A4; the integrator HOLDs it. Any text reading "3.8
  merges LAST regardless" is void where it conflicts with DECLARE-GO's authorization boundary.
- **3.11's `[ratification-pending]` half** (its 027 commit) is held; its freshness half merged at
  `aaa1e96a`.
- **filings-N's intake #72** is held as a single-commit branch at `7c5432ea`.

Four items are held under DECLARE-GO's authorization boundary and go to dawn **with their intake id,
not to main**: 3.8 (#71), 3.13 (#68), 3.11's 027 commit, and filings' intake #72.
- **3.13 is DONE at NO-COMMIT** and is not a HOLD — nothing is waiting to merge, because by ruling
  nothing was created in the repo.

## 4 · What this batch found — the dawn items that are mine

**RULE THIS FIRST.** Nominated by filings-N, who has seen every row, and carried here verbatim at
their word:

> RULE ROW 27 FIRST: ratify or reverse NC1's 18 out-of-scope dispositions. It is the only item on
> the list that is cheap to reverse tonight and expensive to reverse later, it gates wave 2's launch
> condition and therefore the v1.5.0 tag, and unlike the tag itself it can be ruled from evidence
> already in hand rather than waiting on a measurement.

The clock on it is real and is created by THIS FILE: NC1's 18 entries are individually reversible
while the batch is open — delete them and the WARNs return — but once this close packet lands the
`closed_by:` exemption self-expires and the dispositions stop being a live choice and become the
recorded state. And if the ruling is REVERSE, A1's launch condition must be re-issued, because those
WARNs cannot clear tonight by any act available to a lane. **Reversing after this packet is a
materially larger job than reversing before it.** The lane also flagged its own discomfort rather
than burying it — that the work "sits close to my named anti-pattern, Dispositioning to reach GREEN"
— and asked to be checked. A seat that asks to be checked should be checked first.

The ratification list of record is **`to-browser\RATIFICATION-2026-09-06.md`**, filings-N's, 30 rows
in number order with its own defects section (§9). These are the items this batch produced that are
mine to file rather than theirs, and they are additions to that list, not a replacement for it.
**All of them are already folded into that file** — filings-N carries §4.1 as row 31, §4.3 as row 32
(indexed "RULE 32 BEFORE 31", because whether the hook's comment or its body is intended decides
whether 31 is a bug or a scope), §4.7 as row 33, §4.5 in defect D-12, §4.6 as row 29, and the
allocator ruling as a new box on D-1. The `docs/dashboard/` genre admission is row 20. Cited, not
duplicated.

0. **THE ROOT FINDING — `027`'s message protocol assumes a substrate that TWO OF TONIGHT'S FOUR
   REMOTE LANES DID NOT HAVE.** Promoted to the head of this list at the integrator's argument, which
   is better than my original ordering: I had filed the two symptoms and left the cause underneath
   them.

   A codespace lane cannot see this apparatus at all. Lane 3.8's own account: `ListAgents` shows it
   no dispatcher and no integrator, so it "treated the lane file as real work to execute, not as an
   authority chain to obey literally", and it wrote no QUESTION file because **it has no such channel
   — its packet WAS the channel**. A cloud lane has the mirror-image gap: it can receive a message
   and cannot send one, so **a handback has no transport** and the integrator can never receive one.

   **Every downstream symptom of the night follows from this one gap:** attempt 1's refusal that
   reached nobody and surfaced only as a green receipt over empty work; the QUESTION files two remote
   lanes could not file; and both cloud lanes merging on a recorded weaker basis
   ("merged on dispatcher's read of a lane that cannot hand back") because no handback was
   physically possible. Neither the lanes nor the integrator erred. **The protocol is written for
   local sessions and is silently partial on two of the four substrates this batch dispatched to.**

1. **`[#630]` and the post-freeze amendment path are not composed.** An amended-in lane's contract
   can NEVER reach the tree. `[#630]` compares the manifest's roster against contracts **in the
   CHANGESET**; a batch's other contracts landed at freeze and are unchanged, so `git add` cannot
   re-stage them — there is no diff. Contract alone refuses; contract-plus-amendment refuses; only
   the manifest alone passes, because the predicate skips at 0 contracts given. **Both refusing
   orderings were attempted**, so this is measured. The predicate is scoped "at freeze" by its own
   docstring and does exactly what it was built for; adding a lane after freeze is simply outside it.
2. **The sharper form of the same gap:** lane 3.15's WORK merged at `0d2db2f7` while its contract
   never landed, and `[#630]` cannot see that either. **Batch T ends with 13 contracts for 14
   executed lanes.** A lane whose work merges without its contract is invisible to a predicate that
   compares only against the changeset. Contract of record for 3.15 is
   `<PROMPTS_DIR>/to-cc/LANE-t-000-freshness-unstamped.md`, sha256
   `2d628f6d14a02986b860c65625193db872c9c588b526633d304da35ec8e0023a`.
3. **`.pre-commit-config.yaml` `lane-contract-check` disagrees with itself**, and settling it decides
   whether items 1-2 are a bug or a scope. Its comment asserts "`always_run: true` +
   `pass_filenames: false` (lane-g-630, [#630])"; the hook body sets `always_run: true` and a
   `files:` glob and **does not set `pass_filenames: false`**. The comment describes an every-commit
   repo-wide gate; the configuration implements a staged-files gate. The behaviour above is the
   configuration's.
4. **`intake-id` is double-allocated FOUR times — 14, 42, 70 and 72 — so this is an ALLOCATOR
   defect, not an index defect.** I filed 70; lane 3.7 independently measured 14 and 42 by scanning
   every `docs/intake/` blob reachable from ANY ref (269 blobs, 72 ids, max 72, no gaps). **A folder
   listing cannot see ids allocated on unmerged branches, which is precisely how these collisions
   happen** — the scan-every-ref derivation is the fix and should become the allocator.

   **#72 formed TONIGHT, under observation, which turns this from inferred to demonstrated.**
   filings-N's 027 intake (`7c5432ea`) and lane 3.6's candidate-(c) intake (`dadda5fc`) both print
   `intake-id: 72`. **Neither lane erred:** 3.6 computed next-free from `main`, where 72 *was* free,
   because filings' file sat on an unmerged branch. Next free is **74**, not 73 — lane 3.7 took 73.

   **It could not actually collide on main tonight, and the reason is uncomfortable.** filings'
   branch is a single commit, that commit is the `[ratification-pending]` 027 intake, so the whole
   branch is held and only 3.6's #72 can land. **The collision was defused by an unrelated
   authorization boundary, not by any mechanism designed to prevent it** — nothing stopped the two
   generators rendering "#72" twice except a hold that exists for another reason entirely. After both
   branches merge, they will.

   Consequence for dawn: **colliding intakes must be cited BY PATH, never by id**, or the row cannot
   be executed as written. This bites the `docs/dashboard/` genre row directly, which cites **#42** —
   and there are two #42s; the one meant is the 2026-08-23 generated-artifact-currency lineage, not
   the `AGENTS.md`-vs-ADR-53 one.
5. **A codespace receipt proves TRANSPORT, not WORK.** The shape
   (`transport-ok-and-remote-exit-code-read-separately`,
   `is-error-false-not-subtype-success`) returned clean over an empty result on BOTH codespace lanes
   tonight, once after a refusal on locators that do resolve. A receipt that cannot distinguish "did
   the work" from "connected successfully" is measuring the wrong thing.
6. **A portable measurement is a COUNT, not a DURATION**, and this one nearly inverted a verdict.
   Intake #71's 664s/75s baseline was taken on a slow Windows process-spawn substrate. On the Linux
   devcontainer, ship-gate was already ~28s against a 200s target **before lane 3.8 changed
   anything**. **A lane that measured wall-clock would have reported a large success, honestly, and
   been wrong** — it would have "proved" a win that was really a Windows-vs-Linux spawn-cost
   difference. It measured git spawns and file reads instead and got a result that survives the
   substrate.

   **Read this together with §4.5 — they are one lesson stated twice: the instrument decides what you
   are allowed to conclude, and BOTH of tonight's instrument failures were invisible from inside the
   thing they were measuring.** A receipt cannot see that no work happened; a stopwatch cannot see
   that it is timing the substrate rather than the change.
7. **The branch enum has a second, invisible half** (the integrator's generalisation, and the
   sharpest structural finding of the night). The ADR-110 exemption keys on `LANE_BRANCH_RE`, which
   was deliberately narrowed from `worktree-lane-*`. So `claude/*` cloud lanes, `docs/*` integration
   branches and dispatcher/manifest branches are ALL unexempt — my 04:00 wedge was one instance of a
   class, not a one-off. **Any future prefix admitted to the branch enum without a matching
   `LANE_BRANCH_RE` update joins that class silently.** The enum is meant to be the checkable
   surface; today it checks only half of what it names.
8. **Manifest lane-slug linking cannot reach a `LANE-<slug>.md` contract copy** (lane 3.6's Q2).
   Those names carry no `<date>-<class>-` prefix, so `artifact_tail` refuses them — and this hits
   **every batch that freezes contract copies**, not only T. Rule it TOGETHER with §4.1-4.2: two
   independent surfaces cannot see the same directory correctly, and fixing one alone leaves it
   half-visible.
9. **A frozen launch condition can be invalidated by the batch's own progress** (see §6). Wave 2's
   condition enumerated two tolerated FILES; two later merges landed two new findings in other
   organs, and the condition failed with no lane at fault. A launch condition should name a CLASS of
   acceptable residual, not a file list.
10. **`protocols/HANDOFF_BOOT.md` must be stamped together with a browser PIN re-issue**, or every
   booted seat breaks. It is the deliberate `8 → 1` residue of lane 3.15.

## 5 · QUESTION files owed to dawn

Four filed by me before any launch, all in `to-browser\QUESTION-dispatcher-T.md`, all answered by
`AMEND-BATCH-T-001` leg B and carried into filings-N's list:

```
1  lane 3.2 -- admit docs/dashboard/ as an ADR-101 genre, or re-scope the lane to the
   class-currency rule its Done-when actually describes?   (blocks the one lane that never ran)
2  lane 3.13 -- intake #68 names NO location for BROWSER-SEAT-FLOOR.md
3  intake-id 70 allocated twice  (now known to be three collisions -- see 4.4)
4  lane 3.14 discharges [#628] only PARTIALLY, by the contract's own scoping
```

Lanes filed their own alongside these: `QUESTION-lane-t-000-{freshness-unstamped, nc1-clear,
playbook, readme, reds-spine, shape-seal}.md` and `QUESTION-filings.md`. **No lane raised a budget
ESCALATE**, and every one of these is a lane that stopped and asked instead of deciding for the
operator. On bypasses the accurate statement is **one spent and withdrawn** by lane 3.6, disclosed
unprompted — see §9; an earlier revision of this section claimed none was spent and that was wrong.

## 6 · Wave 2, and what did not happen

**Lane 3.14's launch condition was RE-ISSUED by A1** and supersedes the `ship-gate GREEN` condition
frozen at dispatch. It launches on `PACKET-MERGED wave-1 @ <sha>` **AND** hard-fail = 0 **AND** every
surviving undispositioned WARN being a `canonical_freshness` line naming only `CLAUDE.md` (which 3.14
re-stamps in the same act) and/or `protocols/HANDOFF_BOOT.md`. **Anything else surviving and 3.14 is
not launched, with the blocking organ recorded BY NAME AND FILE** — so that dawn does not misread a
RED as NC1 having failed.

**DISPOSITION: LANE 3.14 WAS NOT LAUNCHED.** Two of the three surviving undispositioned WARNs are
not `canonical_freshness` lines, so A1's condition fails on its literal reading — which is the
reading A1 asks for. Recorded by organ and file, as A1 requires:

```
NOT LAUNCHED -- 3.14 lane-t-628-v1-release (wave 2)
BLOCKING, by organ and file:
  undeclared_edges   docs/intake/2026-09-05-tech-shape-spec-tree-seal-to-consumers.md   (lane 3.7's intake)
  funnel_coverage    2026-09-06-technical-seal-report-corp-monorepo.md                  (the H0 seal arc)
TOLERATED BY A1, not blocking:
  canonical_freshness  gated-and-stale: CLAUDE.md   (3.14's own act -- it re-stamps it)
```

**Neither blocker is wave 1 falling short, and this is the part dawn must not misread.** Both arrived
in lane 3.6's THIRD sync — *after* its contract froze. They are **two later merges landing two new
findings**, each one line of work for its owner. A1 exists precisely so that a RED at this point is
not read as NC1 having failed; NC1 took hard-fail 2 → 0 and undispositioned 52 → 3.

**This is itself a dawn item: a frozen launch condition can be invalidated by the batch's own
progress.** A condition frozen against a moment, evaluated after N further merges, measures a
different tree than the one it was written for — and no lane has done anything wrong when it fails.
The fix is not a bigger tolerance list; it is that a launch condition needs to name a *class* of
acceptable residual rather than an enumerated file list.

**3.14 was not launched on a partial condition to make the batch look complete.** A recorded
non-launch is a result.

## 7 · State at close

Measured, not expected. Ship-gate run in git-bash at `89a2fa04` — **before lane 3.6 (nc1-clear)
landed**, so this is the shape going into wave 1's gate, not the wave-1 result. The integrator's
decomposed `PACKET-MERGED wave-1` line is the authority on the final reading.

```
ship-gate: RED -- not shipped-ready (1 hard-fail organ(s); 52 new/undispositioned WARN(s))
canonical_freshness  derived ungated-and-unstamped:  1  protocols/HANDOFF_BOOT.md
canonical_freshness  derived gated-and-stale:        1  CLAUDE.md
canonical_freshness  derived ungated-and-stale:      1  protocols/OPERATOR-INTERFACE.md
STALE dispositions:  4  -- the four the operator consented to remove
```

**Lane 3.15's deliverable is visible in that reading: `ungated-and-unstamped` is 1, down from the 8
that made wave-1 GREEN unreachable, and the remaining 1 is the ROLE-PIN file excluded by ruling.**

Against A1's re-issued launch condition, which tolerates only `CLAUDE.md` and/or
`protocols/HANDOFF_BOOT.md`: two of the three surviving freshness rows are tolerated by name. The
third, `protocols/OPERATOR-INTERFACE.md`, **is precisely the file A2 added to lane 3.6's contract**,
so nc1-clear landing is expected to clear it — and NC1's own commit `dadda5fc` reports
`undispositioned 52 -> 3`, which is the same 52 this run measured. **If it clears as expected, the
surviving WARNs are exactly the two A1 tolerates and 3.14 launches; if it does not, the blocking
organ is recorded BY NAME AND FILE and 3.14 is NOT launched.** A recorded non-launch is a result, not
a failure, and no partial condition is rounded toward launchable.

See `to-browser\SESSION-dispatcher.md` for the session-level record and
`to-browser\STATUS-DISPATCHER.md` for the step-0 evidence board.

## 8 · Residuals — named, because an honest leftover beats a false clean tree

**The lane worktrees are still on disk and their sessions are still alive.** This is a KNOWN and
RECORDED leftover, not an oversight, and it is the one thing in this batch that no session could
close:

- `ExitWorktree` only operates on a worktree entered by the CALLING session. The local lanes were
  launched with `.claude/worktrees/<name>` as cwd and never entered it, so `ExitWorktree` is a no-op
  for them.
- `git worktree remove` refuses a tree a live session holds, and a merged husk still holding cwd is
  what FAILs the orphan gate.
- **No session can terminate a peer session.** The lanes are independent background sessions, not
  tasks any session holds a handle on.

So teardown is an **OPERATOR act against the job list**, and the correct wording is **"session alive,
cwd held"** — not "worktree not removed", which invites a retry of `remove` and the false conclusion
that the tool is broken. **IDLE IS NOT DEAD:** a lane showing idle has finished its turn, not exited.

**FOUR CODESPACES EXIST AND NONE IS DELETED — they bill for storage until they are.** Stopped is
not deleted; retention is 24h, after which they auto-delete.

```
lane-t-000-batch-p-audit-speed-g5rvj4w6qvxcjw7      Shutdown
lane-t-000-trace-scorecard-7r5j6v45grvcxvg7         Shutdown
lane-t-000-trace-scorecard-b-rr65q4vwrp72544w       Shutdown   <-- see the hazard below
lane-t-000-batch-p-audit-speed-b-6r5xq9756jwf4j46   Available
```

**HAZARD — read before deleting or letting retention expire `lane-t-000-trace-scorecard-b`.** Lane
3.9's 45 turns of work were never committed and never pushed, so **the only place that work can still
exist is inside that codespace's disk**. Deleting it destroys the only copy. I did not delete any of
them: deletion is destructive and it is the operator's call, and this one must be INSPECTED before it
is deleted or allowed to expire. The 24h retention clock means this is not indefinite.

Also residual: **13 contracts for 14 executed lanes** (§4.1-4.2), and **`protocols/HANDOFF_BOOT.md`
unstamped by ruling** (§4.8).

## 9 · What went right, since a close packet that only lists defects mis-describes the night

Seven lanes merged clean. No lane raised a budget ESCALATE.

**CORRECTION, and it retracts a claim I made four times tonight.** I wrote "no lane spent a
`--no-verify`" in this packet, in `STATUS-DISPATCHER.md`, in `SESSION-dispatcher.md` and to the
integrator. **That is false.** Lane 3.6 spent ONE bypass, on the spine phantom, against an addendum
that told it not to. It then reset the commit out of history and re-committed identical content
through the full gate, so **no bypassed commit is on the pushed branch** — but the act happened. The
honest sentence is "one bypass was spent and withdrawn", not "none was spent".

**The lane disclosed it unprompted when nothing would have surfaced it**, and gave me the accurate
version of my own claim. That is the behaviour the batch should want; the defect it points at is the
phantom, which cost four seats in one night (the integrator, this dispatcher three times, and 3.6) —
a predicate misread that often is a documentation defect, not four lapses. Every
lane that hit an ambiguity stopped and filed a QUESTION rather than deciding for the operator — 3.13
declined to invent a repo location it had not been given, and 3.7 asked to be released from a
serialization rather than unilaterally breaking it. The integrator refused a paraphrase from me and
was right to, and later corrected my anchor misreading with the diagnostic rather than the verdict.
**The two findings most likely to outlive this batch — the branch-enum's invisible half and the
receipt that proves transport rather than work — were both found by seats noticing that a green
signal did not match what they could see.**
