# Lane `lane-v-000-window-rulings` — end-of-lane packet: the window's rulings landed as repo state

**Lane:** `lane-v-000-window-rulings` (batch V) · **branch** `worktree-lane-v-000-window-rulings`
**Contract:** `docs/audits/2026-09-08-technical-batch-v-launch-contracts/LANE-v-000-window-rulings.md`
**Base:** `552997bb` · **Commits:** `887719f5`, `8869eb23`, `0cc5d04e`, plus this packet
**Mode:** plan · **Model:** opus · **Effort:** high · **Terra tally:** none owed — DOCS lane, the
diff reaches no `scripts/` (footprint below proves it)

---

## 1 · What changed

Fourteen files, all inside the contract's declared footprint. Nothing else was touched.

```
BACKLOG.md                                    |   8 +      (generated view)
docs/intake/2026-09-09-tech-recovery-plan.md  | 242 +      (new — intake #89)
docs/intake/README.md                         |   5 +-     (generated Contents block)
docs/intake/manifest.json                     |  19 +-     (generated)
tasks/628-dc2-recut-essentials-...md          |   2 +-     (AMENDED)
tasks/665..672-*.md                           |  88 +      (8 new rows)
tasks/manifest.json                           |  34 +-     (8 nodes inserted after [#664])
```

**No `scripts/`. No `JOURNAL.md`. No index regeneration. No file deleted.** `protocols/ESSENTIALS.md`
is byte-identical to its state at `552997bb`.

### 1.1 · The intake — `docs/intake/2026-09-09-tech-recovery-plan.md`, intake `#89`

Filed from `DECLARE-RECOVERY-2026-09-09.md`, which lived only on the transport. It carries the
DECLARE's substance in the ADR-98 template's sections: the ten-question paste test (§0), the
four-file target (§1), the delete list (§2), the four mechanisms (§3), the A–G sequence with
substrates (§4) and the four standing asks with their true status (§5). The plan-shaped material
is carried under a "The plan as declared" section, marked explicitly as a **record of the source**
rather than a specification the intake invents — the ADR-98 §3 genre line.

**intake-id allocated with the organ**, not by reading the folder: `gen_intake_index.py --next-free`
returned **89**, scanning the working tree plus all eleven local and origin refs (ruling D8). The
listing under-reports by every archived doc and every unmerged branch, and three ids are already
double-allocated, which is why the folder listing was not consulted.

**Both intake generators run**, as the contract requires: `gen_intake_index.py --write` (Contents
block, 78 → 79 docs) and `gen_intake_tree.py --write` (manifest, 79 item nodes, 297 residue lines).

**Status is DRAFT, not ACCEPTED.** The DECLARE carries the operator's stated want and the browser
seat's plan for satisfying it; the operator has not ruled the plan's shape. A lane does not
self-declare an operator verdict, so the ratification is recorded as the first open question rather
than assumed into the frontmatter.

### 1.2 · The six step rows — `[#665]`–`[#670]`, `[E2]`/`[S3]`

| Row | Step | Size | Dependency declared |
|---|---|---|---|
| `[#665]` | A — chapter map of PLAYBOOK + ARCHITECTURE (`agy`, read-only; CC verifies every locator) | P1/M | — |
| `[#666]` | B — the operator's keep/merge/cut sitting; carries the decision, does not make it | P1/S | `#665` |
| `[#667]` | D — the docs rewrite (ARCHITECTURE render · PLAYBOOK by chapter · `DISPATCH.md` split · `CLAUDE.md` generated lists · ESSENTIALS re-point and delete) | P1/L | `#664` |
| `[#668]` | E — the paste test as a scored eval with a stated bar | P2/M | `#667` |
| `[#669]` | F — the conductor state machine | P1/L | `#664` |
| `[#670]` | G — floor v1.5.0 to `corp-monorepo` | P1/M | `#644` |

**Step C was NOT filed** — it is already `[#664]` on `main` (`3b50ea9f`), as the contract states.

Theme and story are **positional** in this repo (`gen_task_tree.py`: "theme/story — POSITIONAL"),
so the eight nodes were inserted into `tasks/manifest.json` immediately after `[#664]`'s node and
the derived frontmatter was **read back** to confirm: all eight carry
`theme: "[E2] Enforced governance"` / `story: "[S3] Turn advisory guards into enforced gates"`.

### 1.3 · The `[#644]` / `[#664]` collision — recorded, as the contract orders

`DECLARE-RECOVERY-2026-09-09` §3.1 and §4 step C name the spine row **`[#644]`**. That id is wrong.
`[#644]` is a different live row — *"The 2026-08-29 deploy freeze has never been ruled, and it
blocks the universalization order's step 4"*, `[E6]`/`[S15]`, P1/S, filed by lane V-4. The DECLARE
predicted an id that V-4's filings consumed in between.

**Every row that means the spine cites `[#664]`.** `[#667]` and `[#669]` declare `depends-on: #664`.
`[#670]` is the one row that genuinely cites `[#644]`, **as its blocker**, and states in its own
body why the two are not merged: `[#644]` is closed by a ruling reaching a repo surface, `[#670]`
by a deploy running green — they fail differently, so merging them would either close a deploy row
by making a ruling or hold a ruling open pending a deploy.

The collision is also recorded inside intake `#89` itself, so a reader of the plan meets the
correction at the same place as the error.

### 1.4 · The terra-gate row — `[#671]`, FILED

The contract instructed: read `[#649]` first, and if it already covers the absence case, **file
nothing and say so**. `[#649]` was read in full. It does **not** cover it, and the row is filed.

**What `[#649]` owns** (its own Done-when): the seat templates emit the three-part
`HIGH raw=N fixed=N unresolved=N` line; a refusal reads a **one-number** tally as `review=NONE`;
the integrator's per-merge check reads the same predicate the templates write. That is the tally
line's **content, when one exists**.

**What nothing owns**, and what `[#671]` now does: the tally line's **presence at merge tier**.
Measured against the tree rather than assumed:

- `scripts/seat_refusals.py::refuse_tally_reviewer` **does** raise `tally-malformed` when the line
  it is handed does not parse — so the absence of a *line* is seen.
- But it is reachable only through `seat_refusals.py reviewer --contracted <id> <artifact>`, and
  `scripts/gen_seat_boot.py` renders that command into a seat boot **as an instruction line**. A
  grep over the tree finds no `.pre-commit-config.yaml` entry, no `audit_checks` registration and
  no merge step that fires it.
- And a checker that takes an artifact **path** cannot be handed an artifact that was never
  written. Absence of the *artifact* is the case the existing code shape structurally cannot see.
- `DECLARE-BATCH-V-MERGE-2026-09-09` §1 makes the presence check *"the integrator confirms the
  terra tally line exists in that lane's close artifact"* — the integrator's attention, which is
  precisely what a gate exists to replace.

The seam with `[#649]` is written into `[#671]`'s body so neither row absorbs the other: filing one
row for both would let the format half close while a branch carrying no tally at all still merges.
This is the sibling class of `[#648]` (a refusal implemented and inert), which `[#671]` cites.

### 1.5 · `[#628]` — AMENDED, not duplicated

**The operator asked for a row and received an amendment to the row that already owns the act.**
The reason, recorded as the contract requires: `[#628]` is *"DC-2 re-cut — dissolving
`ESSENTIALS.md` is a FLEET-COUPLED release act, not a doc lane"* (open, P1/L, `[E5]`/`[S14]`), and
its body already names the deletion, its consumers, the floor sha regeneration and `release_lint`
C5. A second row would have split one indivisible act across two owners, which is the shape
`[#629]` exists to refuse.

Two changes, both inside `[#628]`:

**(a) The Done-when gained the two named sites, by ANCHOR TEXT.** The DECLARE names them as
`AI_COUNCIL_PROCESS.md:413` and `PLAYBOOK.md:330`. Both files were opened before citing, per the
contract's own rule, and **both line numbers have moved**. The anchors that hold:

- `protocols/AI_COUNCIL_PROCESS.md` § **"Section history"** — the 2026-09-04 re-stamp entry.
- `protocols/PLAYBOOK.md` Ch2 § **"Authority hierarchy"**, item 1.

**Measured consequence, disclosed because it changes what the dissolution owes:** neither site
*routes* a session today. The first **records the repoint as already landed** (*"Both now cite that
section by anchor text, never a line number"*); the second says in so many words that the file
*"routes nobody"*, pending `[#628]`. They are **dangling references the moment the file goes**, not
re-points owed before it — so the amendment has them re-worded or removed **in the same act as the
deletion**, which is a stricter requirement than "re-point first". The DECLARE's characterisation
of them as "the two live routes still outside the landed fix" is corrected on this evidence; the
sites themselves are named exactly as ordered.

**(b) The count is re-measured and printed, and the row stops carrying two contradictory numbers.**
Per the operator's ruling of 2026-09-09 (relayed by the batch V integrator): the disposition is
**DELETE AFTER RE-POINT**, in that order, as one fleet-coupled release act; and the operator's
**52 was REVIEW carry 4's figure and yields to the measurement**. Measured against the tree at
`8869eb23`, each class named so the number is checkable rather than quoted:

```
563   tracked files contain the string ESSENTIALS   (every class)
 81   after dropping immutable + append-only        (docs/audits/, docs/handoffs/,
                                                     JOURNAL.md, LESSONS*.md, logs/,
                                                     anything under archive/)
 38   files / 95 mention lines, after also dropping the record classes
      (docs/decisions/, docs/intake/, tasks/, BACKLOG.md,
       ecosystem/.dev-knowledge/history/)
```

**38 files / 95 mention lines is the operational consumer set the write-scope must cover, and it is
the number that now stands.** The body's `ten` is kept as what it is — the A3 census's count of
*breaking* consumers, a narrower class — not as a rival total.

Two measured corrections to `[#628]`'s own enumeration, **filed rather than fixed** (fixing them is
the dissolution lane's act, not this one's):

- `scripts/canonical_docs.py` carries **two constants** (`ESSENTIALS`, `ESSENTIALS_PATH`) and
  **four** set memberships — `CANONICAL_OPTIONAL` plus three path tuples — not the five the row
  claims.
- `tests/fixtures/repo-with-structural-checks/protocols/ESSENTIALS.md` is a **293-byte fixture
  stub**, not a consumer. A sweep by filename would take it, so the write-scope must say
  explicitly whether it goes.

**Nothing was deleted.** The removal is step D (`[#667]`) and a release act carrying the floor sha
and `release_lint` C5. This lane recorded the ruled disposition and the measured count; it did not
execute either.

### 1.6 · `[#672]` — the additional row, on the integrator's relayed ruling

Filed under `[E2]`/`[S3]` with the rest. **Every claim was re-verified against the tree before
filing**, per the contract's locator rule, and all of them hold:

- `scripts/gen_lane_contract.py::check` builds `contracts` from the paths in argv and hands that
  dict to `_check_manifest_contract_agreement`, whose comparison
  (`batch_manifest.freeze_manifest_contract_agreement`) is documented and implemented as **"SET
  EQUALITY BOTH WAYS"**. A commit adding contracts to an already-frozen batch is therefore a strict
  subset and always refuses, reporting the manifest's other rows as *"named by no matching
  contract"*. Reverting the manifest instead flips the refusal to *"named by no manifest row"*.
- `.pre-commit-config.yaml`'s `lane-contract-check` block carries `always_run: true` and
  **omits `pass_filenames`** (defaulting TRUE), while `check`'s own docstring states the hook runs
  `always_run: true` **+** `pass_filenames: false`. Half the declared pair is absent.
- `pass_filenames: false` is not the fix: with zero paths the predicate logs
  *"0 contract(s) given — 0 checked"* and the gate passes vacuously — the same defect one layer
  down.

The row is written so **the class is the point**: P11's shape, a check that cannot check its own
case. It cites `[#652]` (a gate that passes when its precondition is absent) as the sibling and
`[#630]` as the row that built the predicate — closed by its landing, not re-opened by this defect.

---

## 2 · The two contract amendments received mid-lane

Recorded here so the change of instruction is auditable, as the integrator asked.

**Amendment 1 (ESSENTIALS).** Received after step 1's reading and before step 4. The operator has
ruled the disposition **DELETE after re-point**; the count is **whatever the re-measurement gives**;
the 52 was REVIEW carry 4's figure and **yields**; `[#628]` still owns it and is **amended, not
duplicated**; and this lane still does **not** delete the file. Effect on the work: the amendment
was written as a **ruled disposition with its sequence**, not as an open question, and the two
numbers were resolved **by measurement rather than by adjudication**. The one place the earlier
framing survived — intake `#89`'s Open questions — was edited in the same lane to record the ruling
instead of the disagreement.

**Amendment 2 (one additional row).** `[#672]`, above. Filed under `[E2]`/`[S3]` with the six step
rows and the terra-gate row, from the measured facts supplied and independently re-verified.

Unchanged and honoured: step C is `[#664]`; six step rows A/B/D/E/F/G; no DECLARE edited; no
`scripts/` touched; commit-and-STOP; the `[#589]` byte bar **held**, neither cleared nor
re-baselined.

---

## 3 · Verification

**Organs.**

```
gen_intake_index.py --next-free   -> 89 (working tree + all refs, D8)
gen_intake_index.py --write       -> wrote docs/intake/README.md      (78 -> 79)
gen_intake_tree.py  --write       -> wrote docs/intake/manifest.json  (79 item nodes)
gen_task_tree.py --emit-source    -> regenerated BACKLOG.md (260 tasks), re-pinned sha
gen_task_tree.py --check          -> check ok
validate_backlog.py               -> OK (9 themes, 26 stories, 260 tasks, 2 warnings)
```

Both `validate_backlog` warnings are pre-existing and untouched by this lane: an empty `[S24]`
story, and `[#426]`'s past `review_date=2026-08-26`.

**Targeted tests** (the full suite runs once at integration, `[#528]`) — nine files covering every
organ this diff moves:

```
uv run --locked pytest -q tests/test_gen_intake_index.py tests/test_gen_intake_tree.py \
  tests/test_gen_task_tree.py tests/test_task_tree_gate.py tests/test_validate_backlog.py \
  tests/test_validate_backlog_twin_parity.py tests/test_validate_doc_claims.py \
  tests/test_validate_doc_rot.py tests/test_validate_hermetization.py

380 passed, 2 failed in 43.84s
```

**Both failures are INHERITED. Neither is caused by this lane, and both are proven so rather than
asserted.**

**RED 1 — `test_the_live_view_is_under_the_589_done_when_byte_bar`.** Known and named in the
contract. `BACKLOG.md` was already **75,539 B** against `[#589]`'s **72,000 B** bar before this lane
started; it is **76,970 B** after, **+1,431 B**, over the bar by **4,970 B**. The growth is small
because `BACKLOG.md` is a **VIEW** — eight new rows contribute one projected line each, and the
bodies live in `tasks/`. **Not cleared and not re-baselined**, per the contract and the operator's
standing ruling: grooming is a closure act, and raising a bar to fit new rows is the act the row
exists to forbid. The decision is the operator's and the architect's.

**RED 2 — `test_validate_doc_rot.py::test_citation_regex_strips_only_real_dated_artifact_identifiers`**,
false-stripping `'2026-09-08-architect-2.md'`. **This lane did not introduce it.** The token is
produced by `[#643]`'s row body — which cites
`to-browser/HANDOFF-VERIFY-2026-09-08-architect-2.md` — and running the scanner's own
`_TASK_RE` / `_ARTIFACT_DATE_RE` pair over **`tasks/643-…md` as it stands at the base commit
`552997bb`** yields exactly `['2026-09-08-architect-2.md', '2026-09-08-dev-knowledge-architect']`.
The second is a real bundle directory and passes; the first is the failure, and it predates this
lane's first commit. This lane's own rows contribute **no** false-stripped token: the finding list
has exactly one entry and it traces to `[#643]`.

**Integrator note:** `[#643]` is being worked by the live sibling lane
`worktree-lane-v-643-enforcement-debt`. Whether the fix belongs to that lane's diff, to the regex,
or to neither is not this lane's call — it is flagged, not decided.

**Footprint.** `git diff --stat 552997bb..HEAD` reaches `BACKLOG.md`, `docs/intake/` (3 files) and
`tasks/` (10 files) and nothing else. **No `scripts/`**, so the DOCS-lane clause holds and no terra
tally is owed. Every pinned-out surface is untouched: `protocols/ESSENTIALS.md`,
`docs/audits/README.md`, `ecosystem/organ-index.md`, `ecosystem/doc-counts.md`, `JOURNAL.md`, and
every landed row other than the one amendment done-clause 4 ordered.

---

## 4 · Proposed diffs (for the integrator)

Nothing beyond what is committed. Three commits plus this packet, in order:

| SHA | What |
|---|---|
| `887719f5` | intake `#89` + both intake generators |
| `8869eb23` | eight rows `[#665]`–`[#672]` + `gen_task_tree --emit-source` |
| `0cc5d04e` | `[#628]` amended — ruled disposition, measured count, two sites by anchor |

**Owed at integration, not here:** the JOURNAL entry (P-1, the integrator's surface); the
regeneration of `docs/audits/README.md`, `ecosystem/organ-index.md` and `ecosystem/doc-counts.md`
once on the merged result (`[#590]`, Q1); and the full suite.

---

## 5 · Open items

1. **The `[#589]` byte bar is over by 4,970 B and rising.** Held deliberately. It needs an operator
   and architect decision — groom, re-cut the view, or move the bar with a reason — and this lane
   is not the place for any of the three.
2. **The doc-rot citation RED belongs to somebody.** `[#643]`'s row text or
   `validate_doc_rot._ARTIFACT_DATE_RE`. Flagged above; the live `[#643]` lane is the obvious
   candidate but the routing is the integrator's.
3. **Intake `#89` is DRAFT and its plan is unratified.** Its steps are filed as rows, which is the
   right order — a row is filed before a lane is dispatched against it — but `[#666]` (the
   operator's sitting) and the plan's own ratification are the same class of unmade decision, and
   the plan should not be treated as authority until it is ruled.
4. **`[#665]`'s substrate carries three measured hazards** the lane will meet: `agy` logs a
   workspace model the run ignores, an unknown model id is silently substituted rather than
   refused, and `--print` mode soft-denies tools. The row names the first two; the third is
   recorded here.
5. **The DECLARE's "two live routes" characterisation is corrected on evidence.** Neither site
   routes a session today. The correction is in `[#628]` and in §1.5 above; whether the DECLARE
   itself is amended is the browser seat's act, not this lane's — the transport is read-only here.

---

**STOPped after this commit.** No merge, no push to `main`, no JOURNAL entry, no index
regeneration. Integration is the integrator's act, from the primary checkout.
