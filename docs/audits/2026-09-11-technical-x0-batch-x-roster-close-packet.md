# X-0 close packet — the batch X roster lands as intake 93, and 28 rows are filed

<!-- lane lane-x-000-batch-x-roster-lands, branch worktree-lane-x-000-batch-x-roster-lands ·
     contract LANE-x-000-batch-x-roster-lands.md (frozen), plus four operator instructions
     delivered mid-run · TEXT-ONLY: no scripts/ file was touched and no mechanism was built ·
     cited by docs/intake/2026-09-11-tech-batch-x-roster.md Part 12 -->

## 1 · What this lane did

Landed the batch X roster into the repo as **intake 93**
(`docs/intake/2026-09-11-tech-batch-x-roster.md`), carrying **eleven transport files**
byte-identically, and filed **33 rows** into `tasks/`.

It is TEXT-ONLY by contract. It built none of the mechanisms the roster names, changed no
file under `scripts/`, wrote no JOURNAL entry, and regenerated no organ index.

Every row's ownership edge back to the intake **is live and queryable in FPG-1**, but it is
NOT carried by an `implements:` frontmatter key: the generator deletes that key by design and
X1-1 (`[#692]`) is the row that makes it possible. The contract's leg 2, what happened to it,
and what X1-1 needs to know are §3.4.

## 2 · Row ids minted, and what each is

Thirty-three rows. The first twenty came from the contract's reserved block `693–719`;
the remaining thirteen were allocated by the live mechanism after the operator ruled the
block exhausted — eight at the AMEND-008/009 fold and five more at AMEND-010/011.

### From the frozen roster and AMEND-006 — ids 693–707

```
693  closure detector: proposals = the whole queue, dead surfacing hook, 99-run cap errors
694  telemetry trigger-or-remove: four modules wired or deleted (+ AX9-5 metric clause)
695  intake #70 (AJ second pass) is ACCEPTED with zero rows
696  M03 leg-1a re-run: stdout capture, UNVERIFIED locators, one silent empty write
697  codespace detached lane returns ZERO WORK, silently
698  SEAT-BOOT: render emits a GO per merge where canon grants one per batch  (AW5-1)
699  SEAT-BOOT: three tally grammars, two colliding on a substring
700  SEAT-BOOT: AW5-4 "control surfaces are STATE" reached no enforcing surface
701  review fallback when Codex is on quota — 50 minutes, no admitted fallback  (C5)
702  zero cron:, zero schedule: — the nightly layer [S20] revives has nothing to revive (B7)
703  W-7's owed MED: an empty impacted-test selection must FAIL CLOSED
704  propose_closures writes a new file per run instead of ONE overwritten  (AX1-4, D5)
705  visualization: nothing renders the task flow  (AX6-3)
706  operator packet gains D14, folder-as-domain  (AX6-4)
707  W-4 close residue — organ index one row stale under a declared bypass  (AX6-5)
```

### From AMEND-007 — ids 715–719, assigned by the operator

```
715  PATH row — and FPG-1 is already the registry; what is new is roots-as-config  (AX7-3)
716  worktree.baseRef unset → lanes branch behind local main  (dispatch defect 3)
717  launch line omits -Model → a sonnet contract runs at opus  (dispatch defect 2)
718  generator writes contracts where the verb does not read  (dispatch defect 1)
719  organ-index entries answer to no schema — validate against catalog-model  (AX7-4)
```

### From AMEND-008 and AMEND-009 — ids 722–729, allocated

```
722  interim routing: read-only work → agy, as READER ONLY  (AX8-1)
723  log-review routine, self-healing, as a batch-close lane until conductor E  (AX8-2)
724  the permanently-RED Windows baseline hides every new failure  (AX8-3)
725  xdist frozenset-identity pollution in test_manifest_link_route  (AX8-3, own row)
726  a torn-down worktree's session silently resolves to the PRIMARY checkout  (AX8-5)
727  deny-and-point PreToolUse hook: a raw search over a governed question is refused (AX9-1)
728  organ skills generated from the organ index  (AX9-2)
729  FPG-1 queries exposed as MCP tools, beside Grep  (AX9-3)
```

### From AMEND-010 and AMEND-011 — ids 730–734

```
730  evidenced bulk closure: the close packet lists what the batch's merges witnessed  (AX10-1)
731  backlog shrinks by mechanism: relocation trigger + enforced closure budget  (AX10-2, +AX10-3 floor clause)
732  ratification #7: committing lanes run LOCAL overnight only  (AX11-1)
733  ratification #5: SEAT-BOOT renders land on the transport, no path typed  (AX11-2)
734  cleanup is an act: the census's 35 non-live items each get DELETE/TRIGGER/KEEP  (AX11-3)
```

**`708–714` are unused holes** inside the reserved block. They were never filed into, and
gaps in the id sequence are normal here rather than a defect to tidy.

## 3 · Five declared deviations

### 3.1 · The intake id is 93, not the 92 the Done-contract froze

The contract's basis for `92` was *"91 is the highest present"*. That premise was true at
dispatch and false by the time the lane ran: batch W's W-1 landed
`docs/intake/2026-09-10-tech-harness-is-process.md` carrying `intake-id: 92` into `main`
**during this lane's own step-0 sync**.

The contract supplies the rule for exactly this case in step 0 — when a merge from `main`
moves the id frontier, *"start your block above whatever you find and say so"* — stated for
task ids, and its merit applies unchanged to the intake id: a ruling binds its merits, not
its quoted integer. Filing a second `92` would have minted a knowing duplicate, and
duplicate intake ids are **unenforced** here, so nothing downstream would have caught it.

`93` was verified free across `docs/intake/`, `docs/intake/archive/`, the manifest, and all
unmerged lane branches. The contract-frozen **filename** was unchanged and did not collide.

### 3.2 · One declared single-hook bypass: `SKIP=audit-health`

Used on the AMEND-006 commit (`f2a2ff1a`). The sole FAIL was `journal_spine_anchor`, and it
was another seat's gap: `a3374b70` — the integrator's `worktree-batch-w-aw53-substrate`
merge — landed on `main` **between this lane's two commits** carrying no JOURNAL anchor. Its
introduced set is `81a28aad`, `9144b095`, `077f1472`, `232b9d62`, every one an integrator
batch-W manifest commit and none of them this lane's.

**Discriminated before bypassing**, using the check's own diagnostic rather than assumption:

```
first run, from a lagging tree   anchored-in-tree False   anchored-at-main False
after syncing to CURRENT main    anchored-in-tree False   anchored-at-main False
```

A both-False reading from a lagging tree proves nothing, which is why the tree was synced
first; both-False *after* the sync reaches current `main` is the real-gap answer rather than
the tree-lag one. The documented remedy for the lag class — sync and re-read — was applied
and did not clear it.

The remaining remedy is a JOURNAL anchor, which this lane is **forbidden** to write
(STANDING_RULINGS P-1; the contract names this contradiction as already filed). Scope was
one hook by id — **not** `--no-verify`. Every other gate ran and passed, including the three
graph gates, `intake-index-freshness` and both commit-msg gates. No push path was touched;
`block-unanchored-push` still fails closed on `main`.

**The bypass was used ONCE and was not renewed, which is the part that matters.** The same
check FAILED again at this lane's final commit, this time naming two spine entries —
`a3374b70` and the newer `e6f11215`. The diagnostic was re-run before reaching for anything,
and the answer had changed: **both read `anchored at main: True`**. The integrator had closed
`a3374b70`'s gap in the interim (`e6f11215` is literally *"anchor the substrate merge"*), so
what was a real gap at the first commit was **tree lag** at the second — the same two symbols,
a different diagnosis, which is exactly why the check ships a discriminator instead of a
verdict. The documented remedy for lag is to sync the tree, and it worked: after
`git merge main` both read `anchored in this tree: True` and the gate passed unaided.

One practical note for the next lane, because it cost a detour here: `git merge` refused the
sync with *"your local changes would be overwritten"*, listing all 28 staged row files — none
of which `main` contains. The refusal is about a **dirty index**, not a real collision; git
declines to merge while `index != HEAD` and reports every such path. `git reset` (mixed,
working tree untouched) cleared it and the merge ran clean. The trap is that the message
reads like a content conflict and invites a bypass, when nothing was in conflict at all.

### 3.3 · The BACKLOG view byte bar is breached — and it was already breached on `main`

`tests/test_gen_task_tree.py::test_the_live_view_is_under_the_589_done_when_byte_bar`
asserts `BACKLOG.md < 72,000 B`. After this lane's 33 rows the live view is **89,633 B**.
**That test was already RED before this lane touched anything:** `BACKLOG.md` at `main` and
at this branch's base is **81,743 B** — 9,743 B over the bar, on a file this lane did not
write. This lane's 33 rows add **7,890 B** and deepen an existing breach; they do not create
one. The arithmetic is the whole proof, since the assertion reads only the file's length, and
it closes exactly: 81,743 + 7,890 = 89,633. (The base moved from 81,266 during this lane, as
X-R and X-C landed on `main` — the breach predates all three of us.)

**The growth-proof half of the mechanism HELD, which is the part worth reporting.** The
per-row ceiling `_VIEW_ROW_BYTE_CEILING = 400` is enforced on every commit; this lane's
largest projected row is **301 B** and all 28 are under it. So is the per-commit total gate
`_VIEW_BYTE_CEILING = 100,000`, which the generator's docstring says sits deliberately above
the 72,000 bar *"so ordinary queue growth can never wedge a commit"* — 89,633 is under it,
and the commit is therefore not wedged **by design**, not by luck.

**This lane did not fix it, and could not.** The bar's own docstring names the two lawful
answers — groom, or re-baseline deliberately on the architect's ruling — and records that
the last re-baseline (70,000 → 72,000, 2026-09-01) was taken only after a grooming pass
found nothing to close, because *"closing a row to buy bytes is closing undone work."*
Grooming rows and re-baselining an architect-ruled constant are both outside a TEXT-ONLY
roster lane's footprint. **Owed to the operator/architect**, and noted beside `[#589]`,
which owns the bar.

Note what this is an instance of: a point-in-time assertion that has been failing on `main`
for long enough that filing a legitimate row now looks like it broke something. That is
`[#724]`'s subject exactly — a red baseline makes a new arrival indistinguishable from the
noise — observed inside the same lane that filed `[#724]`.

### 3.4 · The `implements:` frontmatter key is NOT on the rows — the generator deletes it, and X1-1 is the row that makes it possible

The Done-contract's leg 2 asked for every NEW row to carry *"frontmatter `implements:`
pointing at the intake."* All 28 rows were filed with exactly that key. **The repo's own
generator then removed it**, silently, at the first `gen_task_tree.py --emit-source` — its
log line for the act is the unremarkable *"refreshed derived frontmatter in 28 task file(s)"*.

This is not a bug to route around. `emit_task_file_text` is the **closed oracle for
frontmatter honesty** (`[#439]`): its key set is fixed at `id, title, status, priority?,
size?, theme?, story?, serialize-group?, depends-on?, generates`, every one of them a pure
function of the row's own body, and `--check` asserts that re-rendering a file from its body
reproduces it **byte-for-byte**. There is no `implements` deriver, so the key is not merely
unsupported — it is structurally excluded. Had it survived, `gen_task_tree --check` would
fail on all 28 rows. A hand-written key there is the exact thing the oracle exists to
prevent: *"a hand-edited `status:` sitting in a source-of-truth file meaning nothing."*

**The roster itself says so, which is what makes this decidable in-contract rather than a
fork.** Intake 93's X1 table gives X1-1's NEW clause as: *"frontmatter key `implements:
[ADR-n | intake-n | DECLARE-…]`, validated, FPG-1 edge decision→task"* — i.e. the key is
**X1-1's deliverable**, owned by `[#692]` (`decision_coverage`), and the contract asked this
lane to write a field whose mechanism a later lane is scheduled to build. Leg 2's *merit* is
a traversable ownership edge; its *spelling* was a key that does not exist yet. A ruling
binds its merits, not its quoted spelling — the same principle applied to the intake id.

**The merit is satisfied, and proven rather than asserted.** FPG-1 builds `implements` from
two legs, and leg 1 — *"the row names the file"* — scans the whole row file for a relative
path and finds one in every row body, since each opens by citing
`docs/intake/2026-09-11-tech-batch-x-roster.md`. Built against the committed tree:

```
new rows with an edge: [730, 731, 732, 733, 734]
all 33 lane rows present: True | lane rows: 33
```

All 33 of this lane's rows are there (re-run after the AMEND-010/011 fold). (The other 15 are leg 2 — the intake's byte scan
finding `[#id]` tokens inside the carried roster text, which is the reverse claim and not
this lane's doing.) So the edge the contract wanted **exists and is queryable today**; only
the key does not.

**Owed to X1-1 / `[#692]`, and this is the useful part of the finding:** when the
`implements:` key is built, it needs a deriver inside `emit_task_file_text`'s key set or the
generator will keep deleting it from every row that carries one — including rows filed by
lanes that were told to write it. Either add the deriver, or police the body-path edge FPG-1
already computes. What cannot work is a contract instructing lanes to hand-write a key the
generator is designed to strip, because that failure is **silent**: the lane complies, the
regen removes it, and nothing reports the loss.

### 3.5 · This lane breached ratification #7 while filing the row that states it

`[#732]` carries AX11-1: **a committing lane runs LOCAL and OVERNIGHT ONLY; during working
hours it waits for the night or for conductor E.** This lane is a committing local lane that
ran through 2026-09-11 daytime. It is one of the lanes the amendment means when it says
*"Today's daytime local lanes and integrator suites breached #7; recorded, not repeated."*

Recorded rather than argued, for three reasons that are worth separating:

1. **The amendment scopes its own exemption to today** and asks for a record, not a halt.
2. **The instruction to fold AMEND-010/011 postdates the ratification**, and an operator
   instruction to do work now is the operator's call on when it runs.
3. **The breach is not costless, and this window measured the cost.** `[#724]` exists
   because no valid RED-baseline count could be taken from a worktree while sibling lanes
   saturated the box. That is the same concurrency ratification #7 forbids, and it is why
   `[#732]` is filed as a real constraint rather than as hygiene.

A lane that files a rule and quietly exempts itself from it has filed nothing. The record
is the row, and this is the row's first citation.

## 4 · The judgment calls the contract left to this lane

### 4.1 · SEAT-BOOT is THREE rows, not one

The contract asked for the count and for the reasoning. The three touch different organs,
need different Done-whens, and one is not a fix at all:

- **698** — a GENERATOR emitting a GO per merge against `/lane-integrate` §0's canon.
- **699** — a first-match READER resolving between three tally grammars, two sharing a substring.
- **700** — AW5-4, a RULING that must reach the surface stating amendment discipline.

No single Done-when discharges all three. Folding them would have hidden two behind one.

### 4.2 · AX6-2 is not seven task rows

AX6-2 says the management map "gains rows" for seven folder-domains. AX5-2 defines that map
as **one page rendered from `ecosystem/organ-index.md`, never hand-maintained** — so its
"rows" are table rows in a generated artifact. It is a clause extending the management-map
row, and **that row lives in the uncarried AMEND-005**. Zero task rows filed; recorded in the
intake. Filing seven would have duplicated lane X-C's census and pre-empted D14 (`706`).

### 4.3 · AX8-3 is two rows

Its own text directs it: *"Plus the xdist frozenset-identity pollution
(`test_manifest_link_route`) as its own row."* A parallel-only failure and a permanent
failure warrant different verdicts — merging them would let an intermittent test be
dispositioned as a known-red constant.

### 4.4 · Why 724 carries no number — the measurement the lane could not validly take

The operator asked this lane to measure the RED baseline rather than copy AMEND-008's `26`,
noting it moves between 26 and 28 by commit. **The lane attempted it and is reporting a
finding instead of a number, because from this position no valid number exists.**

The lane first ran the suite serially (`-n 0`) and abandoned that: `addopts = -n auto` means
the Windows baseline IS the parallel one, and `-n 0` cannot see `[#725]`'s xdist-only failure
at all. It then ran the suite at its default parallel invocation — and that result is
disqualified on two independent grounds, **both recorded the same day, in
`docs/audits/2026-09-11-technical-w278-ship-gate-baseline.md`, by the lane that measured it**:

1. **Worktree inflation.** That audit's own closing note: *"the pass/fail COUNTS above are
   worktree-inflated. The wall-times are the transferable half; the pass/fail counts are
   not."* This lane runs from `.claude/worktrees/lane-x-000-batch-x-roster-lands`.
2. **Sibling load.** Same audit: *"measured while a sibling run saturates sixteen workers
   measures the sibling."* Three sibling lanes were live on this box throughout — the domain
   census, the guard-root lane and the seat-boot integrator — with ~106 python processes
   resident. The lane declined to kill them to free the box: their work is not this lane's to
   destroy, and a number bought that way would still fail ground 1.

A count taken under both conditions is not the Windows baseline; it is an artifact of where
and when it was taken. Writing it into the row would have satisfied the instruction's letter
and defeated its purpose.

**What 724 carries instead**, so the row starts from evidence rather than from nothing:

- the nearest *validly measured* number — the W-7 ship-gate baseline's full suite at
  `2040653c`: **33 failed · 5682 passed · 8 skipped** in 1446.49 s — carried **with** its own
  worktree caveat attached rather than laundered;
- the observation that 33 against the operator's 26–28 differs by roughly the size of the
  worktree-artifact set, which is itself a finding rather than noise;
- and an **acceptance clause**, not a placeholder: the count must be established from the
  **PRIMARY CHECKOUT on an otherwise quiet box**, that is the row's first act, and the
  closing re-measurement is taken the same way. The measurement conditions became part of the
  Done-when precisely because the number could not be.

That a routine repo fact — how many tests are red — is this hard to establish is not
incidental to `[#724]`. It is the same defect the row is about, seen from the other side.

## 5 · Folds — run before filing, and three changed the rows

Fold-first was applied to every candidate. The three genuine near-misses are named **in the
row bodies** rather than silently ignored, because an unstated near-miss rots twice:

- **693 vs `[#277]`** — `[#277]` owns SIGNAL QUALITY and its Done-when is a STRONG:WEAK
  ratio. It reaches defect 1 only; a ratio cannot express a dead surfacing hook or a run-cap
  error. Filed, overlap named.
- **699 vs `[#649]`** — `[#649]` owns the tally's CONTENT (one number vs three). Adopting one
  canonical line does not retire two legacy grammars already in the corpus.
- **704 vs `[#626]`** — genuine **tension**, not overlap: `[#626]`'s Done-when presumes a
  DATED SERIES to bucket, and 704 deletes the series. `[#626]` already names the collision
  from its own side. Filed with an explicit *"reconcile in writing"* clause.

**715 was scoped by a fold**: APR-1's FPG-1-completion legs ARE `[#664]`'s clauses
(step D, clauses 1–3), so 715's Done-when deliberately EXCLUDES them and covers only
roots-as-config, the literal-path lint and APR-4's folded candidates. Restating them would
have duplicated a live row.

## 6 · Not filed, each for a stated reason

- **Ledger A6** (CLAUDE.md §7–§9 generated) sits in the roster's §4 prose but **not** in the
  contract's frozen NEW enumeration, which is exhaustive by its own terms. LEDGER A6 reads
  SAID / "No row", so this is a real gap — **reported, not filed**, because the enumeration
  exists precisely to stop this lane over-filing on judgment. **Owed to the operator.**
- **A8** doc congruence — AX1-5 folds it into X2-4 as a clause.
- **X1-1/2/4/5/6 `NEW:` clauses** — additions to rows that already exist.
- **`[#616]` and `[#242]`** — AX7-1 ABSORBS them. Existing ids, not renumbered, not edited,
  not closed; the absorption is recorded in the intake.
- **Everything §5 refuses or defers**, plus the PowerShell dispatch retirement (AX1-6, batch Y).
- **AX6-1** — lane X-C is already dispatched with a named output artifact.
- **AX9-4 and AX8-4** — clauses on rows that do not exist here (both point at AX4-1 in the
  uncarried AMEND-004).
- **The fourth dispatch defect** — the `claude` `.cmd` shim truncating the third positional,
  measured and recorded in the batch W manifest today. AX7-3 lists three. Not filed on the
  lane's own initiative; flagged as the operator's call.

## 7 · Done-when provenance, marked per row

Roster §2 and §3 carry a Done-when column and those rows carry it **verbatim** (693, 694).
The §4 list carries none, so those Done-whens are **AUTHORED** by this lane and each says so
in its own body. 703 carries AX1-3's precondition sentence; 704 extends AX1-4's; 707 carries
AX6-5's four acts with one ordering constraint made explicit; 717 and 718 carry AX7-3's
clauses.

## 8 · Facts this lane verified rather than carried

- **`worktree.baseRef`** — AX7-3 asked CC to verify the setting name. It is correct, and it
  is **unset** in both `.claude/settings.json` and the operator's user settings. Values are
  `fresh` (default → `origin/<default-branch>`) and `head` (current local HEAD). One
  precision written into `716`: `head` is the DISPATCHING SESSION's HEAD, not literally
  `main` HEAD — they coincide only when the dispatcher sits on `main`, so the row asserts the
  property rather than the setting value.
- **A `PreToolUse` deny on `Bash` DOES block on this version** — AX9-1's stated precondition,
  discharged affirmatively. Evidence is this filing session: its Bash calls were denied
  several times by the worktree-isolation `PreToolUse` guard, each refusal reaching the model
  and stopping the call. The `UserPromptSubmit` fallback AX9-1 held in reserve is not needed.
- **The domain-census counts in AX11-3 are VERIFIED, not carried on the amendment's word.**
  X-C landed `docs/audits/2026-09-11-technical-domain-census.md` on `main` (`cd25a094`)
  while `[#734]` was being written, so the input became resolvable mid-filing. Its own
  **REPO TOTAL** row reads **248 | 197 | 24 | 10 | 1 | 16** — AX11-3's figures exactly.
  **And the way to read it is part of the finding:** this lane first tallied the verdict
  column across the tables and got 234, not 248, and briefly took that for a discrepancy
  between the amendment and the artifact. The tally was the faulty instrument — several
  rows stand for COMPRESSED STREAMS (the `history/*.md` row alone covers ~90 dated files
  across six streams), so a per-row scan undercounts by construction. The census states
  its own total precisely so nobody has to count; the warning is written into `[#734]`
  rather than left here, because the next seat to act on those numbers will be reading the
  row, not this packet.
- **One locator corrected**: AX6-3 names `dashboard/conformance.html`. No `dashboard/`
  directory exists; the file is **`ecosystem/conformance.html`**, and `705` carries the
  corrected path.
- **One relay inaccuracy corrected**: `QUESTION-path-registry-2026-09-11.md` carries **no**
  `carried-by:` line, unlike the other eight. It routes here through AX7-3 and its own "lands
  as an intake via X-0's row" sentence. Carried on that basis, recorded.

## 9 · Owed to the integrator, and owed to the operator

**Integrator:**

1. **`BACKLOG.md` will need re-generating after the second merge.** This lane and
   `lane-x-000-window-rules-land` both touch `tasks/manifest.json` and both regenerate
   `BACKLOG.md`. This lane's regeneration is correct for its own base and **is not expected
   to survive the second merge untouched** — re-run `gen_task_tree.py --emit-source` on the
   merged tree. This is the contract's own named coupling, not a defect.
2. **`a3374b70` still owes a JOURNAL anchor** (see §3.2). Unaffected by the declared bypass.
3. **`[#707]` is the integrator's own residue row** — regenerate the organ index (64 → 63),
   fix `CLAUDE.md:138`, re-derive the ship-gate WARN delta **against the regenerated index**,
   and supersede the `ORPHAN_DISPOSITIONS` `/override` line per AW6-1.

4. **AX11-4 is owed to the BATCH W close packet, which is the integrator's artifact.** It
   directs that packet to report the window's net-row overdraft alongside AX10-1's evidenced
   closures. No row was filed here for it; the enforcement half of the same idea is
   `[#731]`'s overdraft clause. **This lane is the overdraft's largest single contributor:
   33 rows filed, none closed.**
5. **AX10-1's first application is already specified by live evidence**, which makes it
   cheap to run: `[#683]` at `0bb1d5ce`, `[#638]` at `69a0266c`, `[#278]` at `e4929b09`,
   `[#688]` at `365ae7d1` — four rows whose work is on `main`'s first-parent spine and whose
   `status:` is still `open`. `[#684]` is unmerged, so under `[#730]`'s own no-witness rule
   it is excluded until its lane lands.

**Operator:**

6. **AMEND-003, -004 and -005 are still NOT carried.** All three declare
   `carried-by: docs/intake/2026-09-11-tech-batch-x-roster.md` — this intake — and no
   instruction has ever named them, where -006, -007, -008 and -009 each were. They leave
   **live dangling references inside what IS carried**, named precisely in the intake's
   Part 11: AX6-2 and AX9-4 → AX4-1/AX5-2; AX6-3 → AX5-1; AX8-2 → AX3-4; AX8-4 → AX4-1;
   AX7-2 supersedes an ordering AX3-3 set; AX7-3 supersedes AX5-3's conditional filing.
   Landing them is one more instruction. This lane did not infer it.
7. **Ledger A6 has no row and no refusal** (see §6).
8. **The fourth dispatch defect** is unfiled by design (see §6).
9. **THREE amendments now point at the same absent row.** AX8-4, AX9-4 and now AX10-3 all
   attach to the floor declaration AX4-1, which lives in the uncarried AMEND-004. The cost
   of not carrying that file is no longer one dangling clause but a pattern, and it is the
   strongest argument yet for landing 003–005. AX10-3's text rides inside `[#731]` so it is
   at least reachable.

## 10 · Verification

- Carriage proven mechanically, not asserted: all **eleven** carried blocks re-extracted from
  the committed file and compared byte-for-byte against their transport sources — **27,933 B
  carried of 64,113 B total**. Each block is exactly 60 B shorter than its source — the
  excluded `carried-by:` line and its newline — except `QUESTION-path-registry`, which has no
  such line and is 1 B shorter for its trailing newline. AMEND-010 (1,446 → 1,386 B) and
  AMEND-011 (1,739 → 1,679 B) both hold the 60 B pattern exactly. All sources are LF, so no
  normalisation was applied. Their sha256s were taken independently with `Get-FileHash`
  before assembly and match what the assembler recorded.
- Every line this lane added sits inside a marked `LANE-ADDED` block **beside** carried text.
  Nothing in Parts 1–11 was edited to produce the supersession map. The lane-added parts were
  renumbered to 12/13/14 when Parts 10 and 11 arrived; no carried text moved.
- `gen_task_tree.py --check` **ok** — frontmatter honesty holds across all 315 rows, which is
  also the proof that a hand-written `implements:` key would have failed it (§3.4).
- All **33** of this lane's rows carry a live FPG-1 `implements` edge into intake 93,
  re-verified after the AMEND-010/011 fold.
- **Targeted suite for this lane's diff** (`[#528]`: a lane runs targeted, the full suite
  runs once at integration) — `test_backlog_source`, `test_gen_task_tree`,
  `test_task_tree_gate`, `test_validate_backlog`, `test_gen_intake_index`,
  `test_gen_intake_tree`, `test_validate_hermetization`, `test_check_backlog_filing`:
  **288 passed, 2 failed**, both understood and neither a defect in what this lane wrote:
  - `test_gen_task_tree::test_the_live_view_is_under_the_589_done_when_byte_bar` — the
    pre-existing breach, §3.3.
  - `test_task_tree_gate::test_registered_and_green_on_live_repo` — `task_tree_coherence`
    returns *"index and working tree disagree ... the coherence read cannot be trusted"*,
    naming this lane's own 28 uncommitted rows. It is the check refusing a half-staged tree,
    which is what it is for; it resolves at the commit that stages them together.
- **The RED baseline count itself could not be validly measured from here** — §4.4. The full
  suite was not run at this lane: `[#528]` puts it at integration, and this box could not
  have produced a trustworthy number anyway.
