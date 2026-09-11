# Batch W — close packet

> The end-of-batch half of ADR-110's two-part archive (`docs/audits/2026-09-10-technical-batch-w-manifest.md`
> is the dispatch half, committed before any lane booted). The manifest's `closed_by:` names this
> path, so **writing this file ends the declared-integration-arc exemption** — which is why every
> merge that took that exemption was independently anchored first (§2b).
>
> Seat: integrator, `SEAT-BOOT-integrator.md`. Batch: `2026-09-10-dev-knowledge-architect`.

## 1 · THE MERGE QUEUE — what landed, in order

```
W-8  worktree-lane-w-000-three-decisions-become-rows  cdeffc2e   docs-only
W-1  worktree-lane-w-000-harness-is-process-intake    365ae7d1   conflict: tasks/manifest.json
W-7  worktree-lane-w-278-impacted-test-selection      e4929b09   conflict: tasks/manifest.json
sub  worktree-batch-w-aw53-substrate                  a3374b70   docs-only, NOT a lane
rep  docs/batch-w-anchor-substrate                    e6f11215   anchor repair, 3 commits
W-3  worktree-lane-w-638-proof-layer-skipif           69a0266c   conflict: ecosystem/doc-counts.md
W-4  worktree-lane-w-683-override-manifest-node       0bb1d5ce   merged with NO handback -- see D-e
W-2  worktree-lane-w-684-pretooluse-guard-root        HELD -> CARRIED to batch X -- see section 8
     (branch and worktree PRESERVED at 90c727bd, deliberately not torn down)
W-5  primary-session act, no branch                   10,051 B removed
W-6  MOVED to batch X, [#687] untouched and unclosed
```

Every teardown gated on `git merge-base --is-ancestor <branch> main` exiting 0 BEFORE any `-d`,
and verified in BOTH halves (worktree + branch), per WORKTREE TEARDOWN IS TWO BRANCHES.

## 2 · THE HEADLINE DEFECT — the exemption is keyed to a class the batch left

`a3374b70` merged the AW5-3 substrate change. The ADR-110 declared-integration-arc exemption covers
a batch's **lane** merges while its manifest is `status: open`. **A substrate merge is not a lane**,
so it took no exemption, landed unanchored on main's first-parent spine, and `journal_spine_anchor`
began FAILing `audit-health` — which blocks **every subsequent commit in the repo**.

The gate text is the discriminator and it was precise: it reported ONE unanchored entry and
SEPARATELY exempted three lane merges. The exemption was working exactly as written. The merge
simply was not of the class it covers.

**Three things this cost, recorded so the next batch does not pay them again:**

1. **The integrator's arc had to run JOURNAL-FIRST**, inverting Ch8's substantive-first /
   JOURNAL-last order (batch-1 F1b). That order assumes the spine is clean when the arc opens.
   Here the block already existed, so the substantive commit was refused by the same gate — the
   entry had to land first to unblock it. Ch8 has no clause for this case.
2. **The arc needed THREE commits, not two.** Commit 1 (JOURNAL naming `81a28aad`) clears the
   pre-existing gap; commit 2 (substantive) then lands; commit 3 (JOURNAL naming commit 2) anchors
   the arc's OWN merge — which commit 1 could not do, because commit 2's hash did not exist when
   commit 1 was authored. Anchors discharge APPEND-ONLY, so a second entry is the correct form and
   amending commit 1 would have been a breach.
3. **`SKIP=audit-health` was available and deliberately NOT used.** The ADR-110 amendment
   2026-08-07 retired that bypass for intermediate merges because the manifest was made to carry
   the exemption instead. And the gate was not misfiring — it reported a real unanchored entry.
   Silencing a correct gate to land one's own commit is the direction this repo files defects
   about, not the direction it takes.

**Recommendation for ADR-110:** the exemption clause should be keyed to *"merges made by the
integrator while the batch is open"* rather than to *"lane merges"*, or the manifest should
enumerate the non-lane merges it also covers. As written, any integrator merge that is not a lane —
a substrate change, an amendment, a repair — silently wedges the whole repo.

### 2b · THE SECOND ANCHORING LESSON — an exemption must be DRAINED before it expires

The first lesson (above) is that the exemption does not cover every merge. The second is about its
**end**, and it nearly cost this batch its own close-out.

`0bb1d5ce` (W-4's merge) is a LANE merge, so it is exempt — and **underneath that exemption it was
`anchored: False`**. The exemption dies the instant this packet lands, because the manifest's
`closed_by:` names this path and `docs/audits/` is immutable (which is exactly what makes the
expiry real rather than a mutable flag anyone could flip). **Landing the packet first would
therefore have un-exempted an unanchored merge and blocked the very commit that closes the batch** —
the same wedge as §2, arriving from the opposite direction and at the worst possible moment.

The fix is an ordering, and it is not in Ch8: **write the anchors for every exempt merge BEFORE
landing the artifact that ends the exemption.** Done here by `1ad278ad`, whose JOURNAL entry names
`5e17ecd7` from `0bb1d5ce`'s introduced set; `0bb1d5ce` then reads `anchored: True` on its own
merit, and the packet lands against a spine that needs no exemption at all.

**Generalised:** an exemption with a real expiry is a debt, not a discharge. ADR-110 says when the
exemption ends but never says the integrator must settle what it was covering first — so the
checklist should carry a sixth item: *every merge that took the exemption is independently
anchored before the packet is written.*

## 3 · FOUR RECORDED DEVIATIONS (also at manifest `61e8a138`)

**D-a · The AW5-2 Codex review was EXTENDED to W-3, and that extension is not written.**
AW5-2 authorized the integrator to run the terra review itself **for W-2**. W-3 handed back at
`74990bf3` as a **code** branch carrying no `review=` token, which D-1 refuses. Two paths existed:
HOLD W-3 (blocking batch X's W-6, sequenced off W-3's merge), or run the review under AW5-2's
shape. The integrator took the second. **It SATISFIES D-1 rather than waiving it** — but the
authorization names a different lane. **Carried here for ratification; not precedent until ratified.**

**D-b · W-3's HIGH:1 was recorded unmodified and verified not to land against its diff.**
`audit.py handback` returns MERGE at exit 0 on `review=gpt-5.6-terra HIGH:1 MED:0 LOW:0` —
D-1's mechanized bar is that a review *ran and is named*; severity triage is the integrator's act.
No tally was adjusted to clear a gate. The finding, attributed to `scripts/proof_layer.py:481`:

1. **Mechanism real, locus elsewhere.** `_match_disposition` (`scripts/audit.py:6595`) is
   `str(token) in finding.evidence` — substring, never equality. A pre-existing `#147` register
   property that W-3's own docstring names.
2. **W-3 strictly NARROWS the aperture.** Pre-change evidence (`module + scope + tool + count`)
   rendered **byte-identically** for two function-level guards in one module, so one disposition
   masked *every* guard in that file — the whole-Finding masking the register's contract forbids.
   Keying on `guard.key` reduces that to prefix-collision alone.
3. **Unreachable live.** 0 substring collisions among the 243 baseline guard keys; 0 register
   entries with `organ: proof_layer`.

Filed as a **batch-X row against `audit.py:6595`**, not as a hold on W-3.

**D-c · An EIGHTH instance of this batch's recurring shape** — *a pin that does not cover the
thing that can change*. D-b's residual is a match token carrying no boundary anchors, so it pins
a prefix rather than a guard.

**D-d · `ecosystem/doc-counts.md` is a THIRD generated-file merge conflict**, after the two
`tasks/manifest.json` collisions (W-1, W-7). Identical signature and method: **neither side is
correct for the merged tree** — HEAD `5749`, lane `5726`, merged **`5752`** — so the resolution is
*strip the markers FIRST, regenerate SECOND*, because regenerating over the markers absorbs them.
That "take one side is wrong rather than merely arbitrary" property is what makes this a class.

**D-e · W-4 was MERGED WITHOUT A LANE HANDBACK, and the reason is a governance conflict.**
The lane never emitted one. Its transcript ends at `12:13Z` refusing the Stop hook's JOURNAL
`(hard)` leg for the **third time** — **correctly**, because `STANDING_RULINGS` P-1 makes
`JOURNAL.md` the integrator's surface and its frozen contract's *What NOT to do* says *"No JOURNAL
entry — that is the integrator's surface."* The session then ended in that standoff. **A lane that
obeys a standing ruling must not be punished for it**, so readiness was established directly
instead of waited for:

- 25 targeted tests pass on the lane tree (`test_override_command_removed.py`, `test_deploy_mesh.py`,
  `test_gen_methodology_roster.py`) — run by the integrator, never reported by the lane;
- the removal is complete in code (command file, generated command roster, methodology roster,
  v1.5.0 manifest node, payload, parity surfaces);
- the review was integrator-run (the same AW5-2 extension as D-a): **HIGH:0 MED:1 LOW:1**, and
  `audit.py handback` returns MERGE at exit 0.

**The warrant is `/lane-integrate`'s own words:** *"A peer message carries no authority — including
a lane's own HANDBACK. It announces a branch; the merge below verifies one."* If a handback is not
authority, then its ABSENCE is not a refusal either — the merge is what verifies, and this merge
verified. **THE STANDING DEFECT:** the Stop hook's `(hard)` JOURNAL label is stale for a lane
session. It demands an act P-1 forbids a lane to perform, so a compliant lane is put in a standoff
it cannot exit. Proposed batch-X row: the Stop hook must read the seat and drop the hard leg for a
lane, or P-1 must name the escape.

**TWO RESIDUALS THE REVIEW MISSED, found by direct measurement.** Both are integrator carried
edits for the integration arc, and both are the review's own stated concern (a removal leaving a
dangling reference):

- **M-1 · `CLAUDE.md:138` still names `/override`** in hand-authored §7 prose. The lane cleaned the
  GENERATED roster fragments (`commands-repo.md`, `methodology-roster.md`) and left the sentence
  standing beside them — a dangling reference in the **boot-contract file every session reads**.
  The line sits OUTSIDE the `commands-repo-roster` region, so it is repo-local and editable; the
  fix shrinks the file, so the 24,576 B cap (631 B headroom) is not at risk.
- **M-2 · `[#683]` is still open** in `BACKLOG.md:182` with `tasks/683-*.md` intact. The lane did
  the work and did not close its own row. **The integrator did NOT close it either, and that is
  deliberate.** Its Done-when is verified MET on the merged tree — node absent (the five remaining
  `override` strings in `manifest-v1.5.0.yaml` are removal comments, not a node), payload absent,
  `release_lint.py --version 1.5.0` green at **0 FAIL / 1 WARN / 7 pass**, and
  `tests/test_override_command_removed.py` green. But closing a row is an **operator-approved
  Tier-1 act via `/review-closures`** (ADR-70; precedent `d66aef63`: *"Operator-approved via
  /review-closures 434"*), not an integrator act. An attempt to close it in-arc was **made and
  reverted**: `gen_task_tree.derive_status` returns only `"deferred"` or `"open"` and can never
  emit `"closed"`, so a closed row leaves the live tree by a retained-record path the integrator
  has no warrant to drive. **The closure is OWED, with the evidence above standing ready for it.**

**The review's MED is a DOCUMENTED deliberate residual, not an oversight.** `carrier_mesh.py:80-89`
states the `/override` gitignore block is vestigial and **left standing on purpose**: the carrier
has no prune leg to retract it from consumers that already carry it, because this release cannot
ship `status: removed` tombstones (`release_lint` C6 — unlocked in P2 on operator decision D3).
Retracting it is filed as its own act rather than smuggled into the removal lane. The reviewer
flagged what the comment itself declares. Carried as a row; not a blocker.

## 4 · A NINTH INSTANCE, FOUND INSIDE W-7's OWN GATE

W-7's `impacted-tests-guard` originally carried a `files:` regex scoped to `scripts/*.py` together
with `pass_filenames`. A reviewer HIGH on 2026-09-11 showed a commit could add an uncovered
`scripts/new_tool.py` **and narrow that regex in the same act** — pre-commit evaluates the STAGED
config, so the hook was skipped and **the gate was disarmed by the change it exists to inspect**.
It now runs `always_run: true`, reading the staged set itself via
`git diff --cached --diff-filter=ACMRT`, pinned by
`tests/test_impacted_tests.py::test_the_guard_cannot_be_disarmed_by_its_own_wiring`.

Same shape as D-c. **Nine instances in one batch is not a coincidence; it is a class the fleet
has no standing check for.** Proposed batch-X row: a lint that flags any gate whose activation
predicate is itself editable by the commits it gates.

## 5 · THREE WITNESSED FACTS (operator-requested, 2026-09-11)

**(1) W-5 — the three SUPERSEDED hook copies: DELETED.** Witnessed as absence on the primary.

```
REMAINS  C:\Users\1028120\.claude\hooks\block-onedrive.ps1      9,016 B  (live guard, armed)
REMAINS  C:\Users\1028120\.claude\hooks\surface-closures.ps1    1,434 B  (untouched)
SUPERSEDED files anywhere under C:\Users\1028120\.claude\ :     ZERO
REMOVED  block-onedrive.SUPERSEDED-...-allowlist-v1             3,322 B
REMOVED  block-onedrive.SUPERSEDED-...-emptygrant-v2            5,432 B
REMOVED  block-onedrive.SUPERSEDED.ps1                          1,297 B
                                                         total 10,051 B
```

**Honest limit:** the integrator witnesses the POST-STATE. The byte figures are the dispatcher's
before/after measurement; they reconcile exactly, and the live guard reads 9,016 B on both sides,
but the deletion EVENT was not observed by this seat. `[#690]` is the in-repo record — the files
live in no git tree, so `main` can never witness their absence directly.

**(2) W-7 clause (b) — BUILT, and witnessed running.**

- Gate: `impacted-tests-guard`, `.pre-commit-config.yaml:450`;
  entry `uv run --locked python scripts/impacted_tests.py guard`; exit 1 on a zero-selection script.
- Trip-test: `tests/test_impacted_tests.py::test_the_refusal_trips_on_a_script_with_no_covering_test`,
  which asserts the refusal NAMES the test to write — it requires the witness to equal
  `tests/test_lonely_organ.py`, on the rationale *"a refusal that only says 'no tests' does half
  the job."*
- **Witnessed, not cited:** run at integration — **5 passed in 42.17s**.
- Scope measured, not assumed: 136/140 `scripts/**.py` select at least one test; the 4 that do not
  are grandfathered in `impacted_tests.ZERO_COVER_GRANDFATHERED`, a set that may shrink and must
  never grow. `deploy/` and `plugins/` are deliberately out of scope — unmeasured ground.

**(3) `DIGEST-2026-09-11-floor-and-cost.md` — ABSENT from the transport.**
Transport resolved from `CLAUDE_PROMPTS_DIR` = `H:\My Drive\CLAUDE PROMPT DIR`. Not at root. A full
recursive sweep found 24 `DIGEST-*.md`; the only 2026-09-11 member is
`to-browser\DIGEST-2026-09-11-research-folder-as-domain.md` (3,593 B). No floor-and-cost digest exists.

## 6 · CARRIED FROM THE BATCH — findings owed to the record

- **AW5-4 · MACHINE-READ CONTROL SURFACES ARE STATE.** Ruled verbatim: *"A line a reader consumes
  first-match (`Tally:`, read at `seat_refusals.py:558`) is updated in place; the prior value is
  preserved verbatim in the file's history section. Amendment-only discipline governs narrative
  records, not control surfaces. The integrator's W-7 ruling stands."* **This is the resolution of
  the amendment-vs-control-surface conflict below, and the two must be read together.**
- **The GO-granularity RENDER DEFECT.** `SEAT-BOOT-integrator.md` §3 heading reads *"one operator
  GO per merge"*; `.claude/commands/lane-integrate.md` §0 reads *"One operator GO authorizes the
  whole batch integration."* Resolved by AW5-1 in favour of `/lane-integrate`. The seat boot is
  GENERATED from PLAYBOOK Ch8 by `gen_seat_boot.py`, so the defect is in the generator's source
  region and is not hand-editable at the seat.
- **THE THREE-GRAMMAR TALLY COLLISION.** Three different `Tally:` grammars are live:
  `seat_refusals._TALLY_RE` (`Tally: review=... findings=N fixed=N`), the D-1 handback shape
  (`review=<id> HIGH:n MED:n LOW:n`), and `audit.py:4720` `_REVIEW_TALLY_RE` (the bolded
  four-number form). Because `seat_refusals.py:558` selects the FIRST line containing the substring
  `Tally:`, and the bolded form CONTAINS that substring, a compliant artifact can draw a false
  `tally-malformed` refusal.
- **`gen_lane_contract.py` REVIEW-CLAUSE REGRESSION.** The generator contains no `review` token at
  all; "REVIEW IS A LANE ACT" greps 0 in batch V's and batch W's generated contracts and is present
  in batch U's hand-authored ones. **This is the generator regression explaining both code-lane
  holds** — W-2 and W-3 each handed back without a `review=` token.
- **THE AMENDMENT-VS-CONTROL-SURFACE CONFLICT — two live rules pointing opposite ways.**
  Critical rule 3 makes audits immutable: supersede with a new file or an in-file amendment marker,
  **never edit in place**. But a `Tally:` line is read FIRST-MATCH by `seat_refusals.py:558`, so an
  amendment marker leaves the SUPERSEDED value as the one the machine reads — obeying the
  immutability rule actively breaks the gate. The two rules cannot both be satisfied on the same
  line. **AW5-4 resolves it by class:** amendment-only discipline governs NARRATIVE records;
  a machine-read control surface is STATE and is updated in place, with the prior value preserved
  verbatim in the file's history section. **The general lesson is the one worth carrying:** a rule
  written for prose silently mis-governs any line a program parses, and this repo has three such
  `Tally:` grammars (above) that no single rule currently covers.
- **MERGE ORDER DEVIATED FROM AW5-5, within the latitude AW5-5 itself grants.** Ruled order was
  W-8 -> W-1 -> W-7 -> W-2 (if AW5-2 passes) -> W-4 -> W-3 *"as they hand back."* Actual:
  W-8 -> W-1 -> W-7 -> substrate -> anchor repair -> **W-3 -> W-4**, with W-2 last and still open.
  W-2 moved to the tail because AW5-2 did not pass (HELD, fix lane dispatched under AW6-2); W-3
  preceded W-4 because it completed first; and the substrate merge plus its anchor repair were
  not in the ruled sequence at all. The *"as they hand back"* clause covers the swap; the two
  unsequenced merges are recorded here because nothing in AW5-5 anticipated them.
- **FR-8's UNSATISFIABLE CLAUSE.** FR-8 requires re-deriving the measurement on the primary
  BEFORE merge; for a lane whose Done-when is the ABSENCE of findings this is literally
  unsatisfiable, because `proof_layer._main` prints the census line only when `findings` is empty.
  Discharged for W-3 by the integrator's own measurement: **243 guards, all at baseline, 10
  self-policing** — which agrees with the lane.
- **THE `tasks/manifest.json` `generated_sha256` CONFLICT PATTERN** (W-1, W-7) plus the
  `doc-counts.md` third instance — see D-d.
- **THE AW5-3 SUBSTRATE OOM COST.** Three OOMs killed full suites at `-n auto` (16), `-n 6` and
  `-n 3`. Per-lane full suites were abandoned on the protocol's own terms: ADR-110 checklist item 2
  requires the full suite run ONCE on the merged result, and PLAYBOOK Ch5 rules targeted in-lane
  plus one full suite at integration ([#528]). **Stated as a reporting gap rather than substituted
  silently** — per-lane suite deltas are NOT in this packet, by design and with cause.
- **THE HUSK DISPOSITION.** `.claude/worktrees/batch-w-aw53-substrate` could not be removed
  ("being used by another process"). Verified to hold nothing unmerged (only `__pycache__/*.pyc`
  absent from main) and its branch passed the ancestor proof. Batch V precedent: record the
  disposition, do not kill holding sessions.
- **CHECKLIST ITEM 3 MUST BE SCOPED.** `git worktree list == primary only` is UNSATISFIABLE:
  three batch-X lanes are live and LOCKED (`lane-x-000-batch-x-roster-lands`,
  `lane-x-000-domain-census`, `lane-x-000-window-rules-land`). The item is discharged **scoped to
  batch W's lanes**, which is a recorded narrowing of a checklist item, not a pass.
- **THE OWED W-7 MED** — to be filed with a non-colliding id per AW4-2.

## 8 · W-2 — HELD, DISPOSITIONED **CARRIED TO BATCH X** (AW7-1's "otherwise" branch)

**The Done-when addendum AW7-1 asks for, recorded verbatim:**

```
HANDBACK worktree-lane-w-684-pretooluse-guard-root @ deeb1b8e code review=gpt-5.6-terra HIGH:0 MED:0 LOW:0
Tally: review=lane reviewer=gpt-5.6-terra findings=5 fixed=5
**Tally:** 0/5/0/0        (RAISED across four terra passes; all five resolved)
carried-forward branch:   worktree-lane-w-684-pretooluse-guard-root @ 90c727bd
reviewed sha:             deeb1b8e   (terminator-1 gate holds: deeb1b8e..90c727bd is exactly
                                      one markdown file, +332 lines -- the artifact itself)
```

**Why HELD and not merged, when the D-1 gate says MERGE.** `audit.py handback` returns MERGE at
exit 0 on that line — but **that gate reads a TALLY, not an ACCEPTANCE**. AW5-2's bar for W-2 is
conjunctive: *"merge only with no unresolved HIGH **and** the M7 smoke evidence present, else
HELD."* The first conjunct is met. The second is not, by the lane's own declaration.

**The lane's own verdict table, verbatim:**

| Closure leg (contract, verbatim) | State |
|---|---|
| non-Claude reader under the guard REFUSED -> passes, one witnessed smoke | MECHANISM CLOSED, WITNESS PARTIAL |
| **M7 smoke run by the lane before its commit, output witnessed (A7-6)** | **UNMET — BLOCKED, external** |
| RED-first test absent -> present, and RED with the fallback removed | CLOSED |
| matcher `"*"` -> the named tool classes | CLOSED |

**The frozen contract admits exactly ONE witness, and there is no second branch.** Done-when,
verbatim from `[#684]`: *"one non-Claude CLI smoke **passes** under the guard, a RED-first test
fails when the fallback is removed."* A7-6: *"the smoke is a **commit precondition owned by the
lane**, not something the integrator re-derives and not something acceptance review takes on
trust … **A commit with no witnessed smoke output is the lane failing its own acceptance**."* The
lane's §A3 characterises this as *"Done-when 4's second branch"*; **the frozen text has no second
branch**, and a frozen leg outranks a later reading of it.

**THIS IS A BLAMELESS FAILURE AND THE LANE'S WORK IS GOOD.** Five HIGH raised across four terra
passes and all five resolved; matcher narrowed; the hook now resolves its own repo root. The
diligence was real: the lane re-probed FIRST as the contract orders, recorded the vendor refusal
verbatim and timestamped (`2026-09-11 13:36:42 +02:00`), and **converted `agy` from "unprobed,
unlikely" to MEASURED-no**, so the honour-set is now fully measured rather than partly assumed.

**THE COST OF CARRYING, STATED PLAINLY.** `main` keeps the `"*"` PreToolUse matcher. That is not
cosmetic: `.claude/settings.json`'s own wiring comment says of that form — *"while the two
CLAUDE_PROMPTS_DIR scopes disagree it refuses EVERY tool call with no in-session escape (measured
2026-09-06)."* The fix that removes this hazard is the thing being carried.

**AND CARRYING DOES NOT SOLVE IT.** The block is a vendor quota on `cursor-agent` — the only CLI
measured to honour `.claude/settings.json`. `codex`, `copilot` and `agy` are all measured
**vacuous instruments**, and `gemini` is client-ineligible. **Batch X meets the identical wall.**
The A7-6 leg is therefore **unsatisfiable with the instruments available**, structurally the same
defect as FR-8's unsatisfiable clause recorded above: an acceptance leg naming a witness nothing
can produce. **Carrying it forward unamended reproduces the block rather than resolving it.**

**ESCALATION — this needs an operator act, not another lane.** Three paths, and only the operator
can choose: (a) supply an instrument (restore `cursor-agent` quota); (b) amend A7-6 to accept a
recorded external block as closure — the reading the lane already took; or (c) accept the lane
without the leg, on the recorded ground that every instrument that exists has been measured.
**Teardown was deliberately NOT performed:** branch and worktree are preserved at `90c727bd`, so
reversing this disposition is a merge, not a re-run.

## 7 · THE REFUSE-TO-FINISH CHECKLIST

```
1  every lane branch merged-or-abandoned   MET (scoped)  6 merged; W-2 CARRIED -- a RECORDED
                                                         disposition, which the item admits.
                                                         Branch PRESERVED at 90c727bd on purpose.
2  full suite run once on merged result    see below
3  git worktree list == primary only       SCOPED       batch W's lanes are gone except W-2's,
                                                         preserved by the carry. Three batch-X
                                                         trees are live and LOCKED, so the literal
                                                         form is unsatisfiable -- a recorded
                                                         NARROWING, not a pass.
4  manifest/packet archived, both halves   MET          manifest at dispatch; this file at close.
4b audits index regenerated once           MET          once, on the final merged result.
5  git stash list empty                    MET          empty.
5b handback tokens recorded                MET          W-8/W-1/W-7/W-3/W-4 recorded; W-2's tally
                                                         recorded as the Done-when addendum in S8.
6  refs/locks/* FREE                       MET          empty.
6b (PROPOSED) every exempt merge anchored  MET          drained by 1ad278ad -- see section 2b.
                                                         Proposed as a standing sixth item.
```

**Item 2 is reported honestly rather than claimed.** The full suite on the final merged tree is the
one item this packet cannot assert from a clean run: three OOMs killed full suites earlier in this
batch at `-n auto` (16), `-n 6` and `-n 3`, and three batch-X lanes are running concurrently on the
same box. What DID run on the merged result is recorded per lane above — W-3's organ green
(`proof_layer` 243/243 at baseline), W-4's 25 targeted tests, W-7's 5 clause-(b) trip-tests, and
`audit.py health` reporting **OK with 0 hard-fails** on the final tree. That is not a substitute for
the item and is not offered as one. **The item stands OPEN pending a full suite on a quiet box**,
which is a recorded gap, not a discharged one.

## 9 · EVIDENCED CLOSURES — ONE OPERATOR WORD CLOSES ALL FOUR (AX10-1, first application)

Per **AX10-1**, every row whose Done-when this batch's merges **witnessed** is listed with its id,
its Done-when **verbatim**, the merged SHA, and the test or gate that proves it. **A row with no
witness is not listed** — which is why `[#684]` is absent (see below), and why this table is an
evidence list rather than a wish list.

**`[#683]` — the v1.5.0 floor ships `/override`, a command that discharges no gate**
- *Done when:* **"node absent, payload absent, `release_lint.py` green, one test fails if either returns"**
- *Merged:* `0bb1d5ce` (W-4)
- *Witness:* node gone from `deploy/manifest-v1.5.0.yaml` (its 5 remaining `override` strings are
  removal comments); `.claude/commands/override.md` absent; `release_lint.py --version 1.5.0` =
  **0 FAIL / 1 WARN / 7 pass**; `tests/test_override_command_removed.py` **1 passed** — and it
  asserts node and payload are ONE act (*"restore both or neither"*).

**`[#638]` — four new proof-layer guards are undispositionable**
- *Done when:* **"(a) `ratchet_findings` carries the guard KEY in its evidence so a disposition can
  be per-guard, and (b) the four guards are ruled on their merits … and
  `ecosystem/proof-layer-baseline.json` is re-stamped"**
- *Merged:* `69a0266c` (W-3)
- *Witness:* `Guard key:` now present in `ratchet_findings`' evidence string
  (`scripts/proof_layer.py`); baseline carries **243 guards**; `audit.py health` reports
  **[OK] proof_layer: 243 … all at the committed baseline, 10 gated on an enforcement runner**.
  The integrator re-derived this independently (FR-8) and got the same 243.

**`[#278]` — test-suite hygiene epic (impacted-test selection leg)**
- *Done when:* **"…the theatricality review ships as a `docs/audits/` artifact and impacted-test
  selection is live in the verify cadence with a test"**
- *Merged:* `e4929b09` (W-7)
- *Witness:* three artifacts shipped (`2026-09-11-technical-w278-close-packet.md`,
  `-selector-leg-measurement.md`, `-ship-gate-baseline.md`); `scripts/impacted_tests.py` wired as
  the live `impacted-tests-guard` pre-commit gate; **5 clause-(b) trip-tests pass in 42.17s**,
  including one asserting the refusal NAMES the test to write.

**`[#688]` — DECLARE-HARNESS-IS-PROCESS is cited by three audits and answers to no tracked file**
- *Done when:* **"`docs/intake/2026-09-10-tech-harness-is-process.md` exists on main"**
- *Merged:* `365ae7d1` (W-1), landed by `d8af8a55`
- *Witness:* the file **exists on main**. This is the one row whose Done-when is a pure existence
  predicate, so the witness is the predicate itself.

**NOT LISTED — `[#684]`**, whose Done-when is *"one non-Claude CLI smoke passes under the guard, a
RED-first test fails when the fallback is removed."* The RED-first half holds; **the smoke half has
no witness**, which is the whole basis of the W-2 carry in §8. AX10-1 says a row with no witness is
not listed, so it is not listed — listing it would be the exact substitution this clause exists to
prevent.

> **OPERATOR: ONE WORD closes `[#683]`, `[#638]`, `[#278]` and `[#688]`.** The integrator did not
> close them unilaterally: `gen_task_tree.derive_status` can only ever emit `"deferred"` or
> `"open"`, and closure runs through `/review-closures` as an operator-approved Tier-1 act
> (ADR-70; precedent `d66aef63`). An in-arc attempt was made and **reverted** on discovering that.

## 10 · NET ROWS, REPORTED HONESTLY (AX11-4)

**This window files more rows than it closes, and the overdraft is stated rather than netted away.**

```
FILED in the window (task files added since 2026-09-10):   14
   [#679] [#680] [#681] [#682] [#683] [#684] [#685] [#686]
   [#687] [#688] [#689] [#690] [#691] [#692]
CLOSED in the window:                                       0
NET:                                                      +14      <- the overdraft
OPEN rows on main at close:                               228

If the operator speaks the ONE word in section 9:          -4
NET AFTER evidenced closures:                             +10
```

**The overdraft is real even after the offset.** Four evidenced closures do not cover fourteen
filings, and this packet does not present them as if they did. Two structural contributors are
worth naming, because both are visible in this batch's own record: the recurring-defect class of
§3-D-c and §4 produced **nine** findings that each want a row, and §6's carried findings add more.
**A batch that discovers faster than it closes is not failing — but it is accruing**, and AX11-4
exists so that accrual is a number in a packet rather than a drift nobody measured.

## 11 · AX11-1 — THE WORKING-HOURS BREACH, RECORDED

**AX11-1 amends AX3-1: committing lanes run LOCAL overnight only; during working hours a committing
lane waits for the night (or for conductor E.)** Today's daytime local lanes **and the integrator's
own suites** breached ratification #7. Recorded here, not repeated: the batch W integrator ran
targeted suites and four terra review passes during working hours, and the batch's three OOMs
(§6) are the cost of that contention showing up as measurement. **No further merges run during
working hours after the current queue.**

---

## 12 · AMENDED AFTER CLOSE — 2026-09-11, W-2's disposition completed and the closure word applied

> **In-file amendment marker, per critical rule 3** (*"supersede with a new file **or an in-file
> amendment marker**; never edit in place"*) — the same form batch W's manifest used for its own
> post-dispatch amendments. **Nothing above is edited.** Sections 8 and 10 are SUPERSEDED in the
> two respects named below and are kept, marked, not swapped out: §8 held W-2 on the M7 leg before
> a fresh review existed, and §10's `+14` was correct when measured and is now stale.

### 12.1 · W-2 — the fresh review ran, and it found the ORIGINAL defect still live

AW6-2 bars a merge except *"on a fresh Codex review with no unresolved HIGH."* The integrator ran
it. **Tally, quoted as AX15-4 requires:**

```
HANDBACK worktree-lane-w-684-pretooluse-guard-root @ 90c727bd code review=gpt-5.6-terra HIGH:2 MED:0 LOW:0
  HIGH .claude/settings.json — guard fails open when it cannot execute
  HIGH tests/test_prompts_guard_hook_wiring.py — tests enforce the insecure fail-open behaviour
```

**Verified against the code, not taken on trust:**

```
g="${CLAUDE_PROJECT_DIR:-.}/scripts/fleet_health.py"
[ -f "$g" ] || g="./scripts/fleet_health.py"
[ -f "$g" ] || exit 0            <- script missing          -> PERMIT
python "$g" --prompts-guard; rc=$?
[ "$rc" = 2 ] && exit 2
exit 0                            <- crash / no interpreter -> PERMIT
```

Only `rc == 2` refuses. **This is the integrator's ORIGINAL W-2 HIGH, unchanged** — a fail-safe
that fails open.

**It was deliberate, and the provenance resolves verbatim.** `REVIEW.md:85` — *"Missing: a guard
that resolves its own path, and that **fails open** when its interpreter cannot start."*
`REVIEW.md:102` — *"intent — the prompts-guard resolves its own path and **fails open on
interpreter failure**."* The measured alternative is MA-1 itself: matcher `"*"` turned an
interpreter failure into *"refusal of every tool call with no in-session escape."* The lane
adjudicated the objection across four passes (§A2.6, *"Pass 3 — MA-1 again"*), narrowed the
fail-open, and fixed a real bug where it skipped a guard sitting in cwd.

**So the two reviews disagreed on a ruled design, and the integrator refused to settle it by
fiat** — merging would land a guard that permits when it cannot decide; refusing would override
the verbatim intent of the finding that created the lane. Routed to the operator under ADR-108 §A.

**THE RULING — AX15-1** (`to-cc/AMEND-BATCH-X-ROSTER-015.md`): *"the PreToolUse prompts-guard
**FAILS CLOSED** for the matched class … whenever it cannot evaluate: script missing, interpreter
missing, crash, any rc other than 0 … a guard that permits when it cannot run is declared
enforcement without enforcement."* MA-1's fail-open intent is **superseded**. The HIGH:2 stands.

**DISPOSITION: W-2 is CARRIED to batch X as lane W-2′** (AX15-3), continuing **on its own branch**
`worktree-lane-w-684-pretooluse-guard-root` @ `90c727bd`. Its **worktree is torn down; the branch
is PRESERVED** — the work continues on it rather than restarting. W-2′'s Done-when adds RED-first
trip-tests for both failure modes, the M7 smoke still passing, and a fresh review with no
unresolved HIGH. On merge it unblocks AX8-1 and X1-4 routing.

**What §8 got right and what it missed.** §8 held W-2 on the M7 leg and called that leg
unsatisfiable with available instruments — still true, and AX15-3 keeps it in W-2′'s Done-when. But
§8 was written before a fresh review existed, so it recorded the M7 leg as the *only* thing holding
W-2. **It was not.** The guard's fail-open posture was the larger of the two, and it took a fresh
review to surface it.

### 12.2 · THE OPERATOR'S CLOSURE WORD — applied to four rows

`to-browser/RATIFICATION-2026-09-11.md`: *"Close the batch W tasks whose work is on `main` — YES.
`[#683]` `[#638]` `[#278]` `[#688]`, and `[#684]` once merged, under `[#730]`."*

That is the ONE WORD §9 asked for. **Applied to all four**, each carrying `[#730]`'s evidence shape
(row id · Done-when verbatim · merged SHA · the gate that proves it) in its own row body:

```
[#683]  0bb1d5ce (W-4)  release_lint 1.5.0 = 0 FAIL/1 WARN/7 pass; test_override_command_removed
[#638]  69a0266c (W-3)  proof_layer [OK] 243/243 at baseline; FR-8 re-derived independently
[#278]  e4929b09 (W-7)  3 artifacts shipped; impacted-tests-guard live; 5 trip-tests pass
[#688]  365ae7d1 (W-1)  the intake file exists on main -- a pure existence predicate
```

**`[#684]` is NOT closed** — the word covers it *"once merged"*, and it is carried, not merged.

**The mechanism, recorded because it is not discoverable from the generator's help.** A row closes
by three coupled edits, not one: the `· CLOSED <date> — <evidence>` marker in the **row body**,
`status: closed` in the frontmatter, **and removal of its node from `tasks/manifest.json`**. The
third is load-bearing and non-obvious: `gen_task_tree.plan_frontmatter_refresh` re-renders
frontmatter **only for files the manifest lists**, and `derive_status` can return only `"deferred"`
or `"open"` — never `"closed"`. So a hand-set `status: closed` on a still-listed row is silently
reverted at the next regeneration. The invariant that makes this legible: **closed ⟺ absent from
the manifest** — measured across the tree at 135 closed rows, all absent, zero closed rows present.
An earlier in-arc attempt that edited only the frontmatter was reverted by the generator and
withdrawn; this is the recorded reason.

### 12.3 · NET-ROW OVERDRAFT — §10's figure is SUPERSEDED (AX11-4)

```
FILED   in the window (task files added since 2026-09-10)          49
        14 batch W  +  33 X-0 (#693-707, #715-719, #722-734)  +  2 X-R (#720, #721)
CLOSED  in the window (this act)                                    4
NET                                                               +45
open rows on main after this act                                  259
closed rows on main after this act                                139
```

**§10 reported `14 filed, 0 closed, +14`.** That was correct when measured — before X-0 and X-R
landed — and §10 itself warned the figure would be read as the window total once more rows
arrived. **It is superseded by the +45 above.** The four closures are the first ever applied under
AX10-1/`[#730]`, so the mechanism now has a precedent as well as a row.

**The overdraft is real and is not netted away.** Four evidenced closures do not cover forty-nine
filings. The batch discovered faster than it closed — nine instances of *a pin that does not cover
the thing that can change*, three unguarded edges of the ADR-110 exemption, and a fail-open guard
that survived four review passes. **That is accrual, not failure — but it is accrual, and AX11-4
exists so it is a number in a packet rather than a drift nobody measured.**

