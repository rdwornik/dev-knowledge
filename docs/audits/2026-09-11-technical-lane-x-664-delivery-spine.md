# LANE x-664 delivery-spine — end-of-lane artifact

**Consumers:** `[#664]` · `[#727]` · intake #93 · ADR-118

**Lane:** `lane-x-664-delivery-spine` · branch `worktree-lane-x-664-delivery-spine` · slot X1-5
of `docs/audits/2026-09-11-technical-batch-x-manifest.md` · mode `plan` · decision budget V-2 ·
terra pre-merge · **merges LAST in batch X**.

**Base:** step-0 sync ran before anything else and is not optional while `[#716]` is open.
`git fetch origin` then `git merge origin/main` landed `0be08b3c` (*"Merge branch
'docs/batch-x-anchor-manifest' — anchor e688669c, the batch X manifest merge"*); `git merge main`
reported *Already up to date*. The base is `origin/main` at `0be08b3c`, not the tree the worktree
was cut from.

---

## Step 1 — locators resolved, the premise re-measured, and the plan

### 1.1 Every locator the contract cites, resolved before it was trusted

The repo rule is that *a `file:line`, heading, SHA, branch or `[#id]` you have not opened is a
claim, not evidence*. Resolved here, and **two of them came back different from the contract**:

| Locator | Resolved | Note |
|---|---|---|
| `LANE-x-664-delivery-spine.md` (frozen, prompts-dir root) vs the in-tree carriage at `docs/audits/2026-09-11-technical-batch-x-launch-contracts/` | **byte-identical** (diff after CRLF strip) | the transport-copy-goes-stale class did not bite here |
| `[#664]` | OPEN, `tasks/664-wire-fpg-1-as-the-delivery-spine-three-commit-tier.md` | Done-when carried verbatim in the contract matches the row |
| `[#727]` | OPEN, `tasks/727-deny-and-point-hook-a-raw-search-over-a-governed-question-is-refused.md` | ditto |
| `scripts/graph_queries.py why` (AX9-1's pointer) | **DOES NOT EXIST** | `graph_queries.py` exposes `orphan-census`, `task-coverage`, `process-list` only |
| `file_purpose_graph.py why` | **EXISTS** — `scripts/file_purpose_graph.py:1543` | `why` is on FPG-1's own CLI, not on the query CLI |
| `scripts/impacted_tests.py` | EXISTS — Click CLI, `select` + `guard` | the impacted-test selector AX9-1 names |
| `ecosystem/organ-index.md` | EXISTS, generated | the third pointer target |
| ADR-118 §5 | resolved | *"migrate the twelve organs **one per lane**, each proving its edge set is a subset of FPG-1 (diff = 0)"* |

**AX9-1's pointer locator is half-wrong and is corrected rather than copied.** A refusal whose
exception text names an organ that does not exist trains the model to distrust the pointer, which
is the exact failure the row exists to end. The hook points at `file_purpose_graph.py why` for
"what is this file / where does X live", at `graph_queries.py process-list` for "who triggers it /
is there already an organ for Z", and at `impacted_tests.py select` for "which tests cover Y".
The clause's *intent* is carried; its `graph_queries.py why` spelling is not.

### 1.2 The premise, re-measured: clause 1 is DISCHARGED on `main` before this lane starts

The contract's Done-contract clause 1 restates `[#664]`'s spine bar. **Lane `v-664` already landed
it** — `da4d1ec9`, `dd161577`, `26c9e729`, `cc9b5555`, `e7bcb630`, `d2cfe7c2`, `bedae758`, with its
own artifact at `docs/audits/2026-09-09-technical-lane-v-664-delivery-spine.md`. Measured on THIS
tree rather than read off that artifact:

```
graph_store.py stats     2560 nodes · 19469 edges · 15 edge kinds, read back from
                         .git/worktrees/lane-x-664-delivery-spine/fpg-graph/FPG.db
graph_queries orphan-census   OK   (exit 0)  + one NOTE, see below
graph_queries task-coverage   OK   (exit 0)
graph_queries process-list    OK   (exit 0)  158 processes, 119 triggered, 39 not
.pre-commit-config.yaml       graph-rebuild + the three query hooks, rebuild FIRST
tests/test_graph_spine.py     35 tests; a trip-test per query (orphan 235/243/251/260,
                              task-coverage 272..371, process-list 372..406)
```

So: the three queries refuse at commit tier **with a trip-test each**; the graph is built on every
commit and persisted in stdlib sqlite; `orphan_census` reaches 0; `task_coverage` reports 0 FAIL on
the merged tree. The 32-vs-20 cardinality gap is recorded at
`2026-09-09-technical-lane-v-664-delivery-spine.md` §1.4/§2.4, and the dead "12 → 0" bar was
re-measured under §A.1's five-kind class at §2.5 — **N-before 18, N-after 18, migrated 0**, with
every remaining site named and owned.

**This is not a refuted premise and does not PAUSE the lane.** Batch X scheduled this lane
knowingly after V: AX3-7 puts *"spine `[#664]`"* in X1 and *"`[#664]` step D + organ map"* in X3,
so the row is deliberately split across waves and stays OPEN. What the lane inherits is a
discharged clause 1 with **one live defect inside it**, plus an unbuilt clause 2.

**The live defect — clause 1's own test is RED on `main`.**
`tests/test_graph_spine.py::test_the_disposition_register_names_no_file_that_is_gone` fails:
`ORPHAN_DISPOSITIONS` in `scripts/graph_queries.py:293` dispositions `.claude/commands/override.md`,
which `5e17ecd7` (*"feat([#683]): remove /override — node, payload and the carrier leg, in one
act"*, batch W) deleted. The census prints it as a NOTE and still exits 0. **This is squarely
clause-1 work in this lane's footprint** — a disposition register that names a file that is gone is
the orphan census answering from a stale roster, which is the class the census exists to catch. A
peer lane created it; this lane owns the organ, so this lane clears it.

### 1.3 "Migrate each organ" — resolved IN CONTRACT, not escalated

The **Steps** skeleton (step 3) says *"migrate each organ to READ the graph instead of parsing its
own edges."* The **Done-contract (immutable)** does not: clause 1 names the refusals, the census,
`task_coverage`, the re-measure and the cardinality gap, and stops. The frozen Done-contract
outranks the Steps skeleton, and two independent authorities point the same way:

- **ADR-118 §5** rules the migration *"one per lane, each proving its edge set is a subset of FPG-1
  (diff = 0) before the old computation is retired"*, and its Alternatives section rejects the big
  bang by name. A lane migrating eighteen sites is the rejected alternative.
- **Lane v-664 §2.5** already recorded the owner: *"a W-G3 migration lane, one per organ, each
  naming its own proof"*, and noted that **every one of the 18 sites lives in a file this lane may
  not edit** — the same footprint bound applies here (`[#664]` touches *"the graph organs and
  `.pre-commit-config.yaml`"*, manifest §2).

Decided per contract defaults and **reported rather than asked** — this is not one of V-2's three
escalation classes. No organ migration happens in this lane; the eighteen sites keep the owner lane
v-664 assigned them.

### 1.4 AX9-4 — exists-before-build, discharged for `[#727]`

AX9-4 requires a contract that CREATES an organ to quote a `process-list` / organ-index result
showing no existing organ answers the need. Run, not asserted:

```
$ graph_queries.py process-list | grep -icE "search|grep|deny"
0
$ grep -rilE "raw search|deny.and.point|governed question" scripts/ ecosystem/ .claude/
(no output)
```

`process-list` enumerates 158 processes and **none** answers "refuse a raw search over a governed
question". The two existing `PreToolUse` guards are adjacent and do not substitute: the ADR-77
`block_immutable_edits.py` guard matches `Edit|MultiEdit|Write|NotebookEdit` and protects a
*write* zone; `fleet_health.py --prompts-guard` refuses on prompts-dir scope disagreement. Neither
inspects a *search*. The need is unanswered; the build is admitted.

### 1.5 AX9-1's precondition — discharged LIVE, on this version, in this session

AX9-1 asks CC to verify *on this version* that a `PreToolUse` deny on `Bash` actually blocks, since
a known upstream issue reported the opposite. Probed with a command that is harmless if the guard
does **not** fire — an `echo` of the operator's P0 exclusion-zone literal into `/dev/null`, no read
and no write into the zone — shaped to trip the `block-onedrive` v3 redirection rule. The Bash call
was refused before it ran and the refusal reached the model as exception text:

> `BLOCKED: zone command contains forbidden token '>' (only provably read-only, redirection-free
> enumeration is permitted on the exclusion zone).`

**A `PreToolUse` deny on `Bash` blocks on this version**, so AX9-1's reserve fallback — moving the
rule to `UserPromptSubmit` / skill hooks — is not required, and the design starts from a verified
mechanism rather than an assumed one.

*(Recorded as a working note for anyone editing this file: the same guard scans **command text**,
so a heredoc writing this section's evidence is itself refused. That is why this artifact is
authored through the Write tool, which scans the destination path and not the bytes.)*

### 1.6 The `[#727]` design — what makes the deny NARROW

The row names the failure mode in its own text: *"over-broad matching here wedges every session,
which is a known and expensive failure mode for a match-all `PreToolUse` rule."* The whole design
problem is the discriminator, so it is stated as a predicate before a line is written.

**A raw search is DENIED only when all four hold:**

1. **The tool is in scope** — `Bash` (and `PowerShell`) or the `Grep` tool.
2. **A search tool is the head of a command segment** — `grep` / `rg` / `ripgrep` / `find` /
   `Select-String` / `sls`, tokenized with stdlib `shlex` and split on `| && || ;`, so a *mention*
   of the word grep in an argument or a commit message is not a match.
3. **The search pattern RESOLVES to a process the graph already holds** — the pattern, after
   stripping regex noise, names an existing `scripts/*.py` path or bare module stem, a hook id in
   `.pre-commit-config.yaml`, a `.claude/commands/*.md` command, or a skill. Asking where
   `gen_task_tree` lives, or who triggers it, is a governed question; `grep -n "def parse"` is not,
   and cannot become one, because `parse` resolves to no process node.
4. **No declared escape is present** — a trailing `# raw-needed: <reason>` on the command line
   allows it through, recorded in the hook's own log line.

Clause 3 is what makes "ordinary non-governed searching provably unaffected" a **property of the
predicate rather than a promise**: a plain string search is undeniable unless the string *is* a real
process, and the test suite pins exactly that. Clause 4 exists because a refusal with no lawful way
through is how a `PreToolUse` rule wedges a session — the repo's own doctrine is that a bypass is
one named thing, declared, not a `--no-verify` reflex.

**The pointer is the row, not the denial.** The exception text names the organ *and the exact
invocation*, chosen from the resolved question:

| Governed question (AX9-1's enumeration) | Organ the refusal names |
|---|---|
| what is this file · where does X live | `uv run --locked python scripts/file_purpose_graph.py why <path>` |
| who triggers it · is there already an organ for Z | `uv run --locked python scripts/graph_queries.py process-list` |
| which tests cover Y | `uv run --locked python scripts/impacted_tests.py select` |

### 1.7 Library-first check (mandatory — every plan names it)

*stdlib > established dependency > stabilized project > industry pattern; hand-roll only on a
MEASURED divergence.*

| Need | Answer | Tier |
|---|---|---|
| `PreToolUse` JSON-stdin / exit-2 wire adapter | **reuse `scripts/hooks/block_immutable_edits.py`'s shape** — same payload read, same `{"decision":"block","reason":…}` + exit 2, same asymmetric fail posture | **stabilized project** |
| shell command tokenization | **stdlib `shlex`** — no hand-rolled splitter, no new dep | stdlib |
| does this token name a real process? | **query FPG-1 via the persisted store** the spine already builds; the hook computes NO edges of its own | stabilized project (and ADR-118 §1 requires it) |
| structured hook output | stdlib `json` | stdlib |

**Nothing new is added to `pyproject.toml`.** The one judgment call is clause 3's resolver: it would
be a hand-rolled scan if written from scratch, and is not, because FPG-1 already holds the process
node set — which is the point of the spine and the reason `[#727]` was folded into this lane rather
than dispatched beside it.

### 1.8 Footprint, floor, and what this lane will NOT do

**Footprint** (manifest §2: *"`[#727]` touches `.claude/settings.json` plus a new hook and test;
`[#664]` touches the graph organs and `.pre-commit-config.yaml`"*):

```
scripts/hooks/deny_and_point.py            NEW    the [#727] guard
tests/test_deny_and_point.py               NEW    RED-first trip-tests
.claude/settings.json                      EDIT   one PreToolUse object
ecosystem/parity-surfaces.yaml             EDIT   AX4-1's named floor carrier
scripts/graph_queries.py                   EDIT   clause-1 disposition-register rot
tasks/664-*.md, tasks/727-*.md             EDIT   AX12-1 carried clauses (first commit)
BACKLOG.md                                 GEN    from tasks/, never hand-edited
docs/audits/2026-09-11-technical-lane-x-664-delivery-spine.md   NEW  this file
```

**AX4-1 — floor declaration.** `[#727]`'s Done-when declares the component **floor: MUST**.
`ecosystem/parity-surfaces.yaml` is the carrier AX4-1 names and `fleet_parity` is the check. The
edit is narrow, and the reason it is safe is stated where it is made: the hub's own hook command is
added to `settings-local-blocks`' owned map for `.dev-knowledge` (a new hook command matching no
owned token WARNs otherwise), and the MUST declaration is made in a form that does not mint an
unsatisfiable consumer pin — a registry admission that REDs a live repo pin is a recorded scar, not
a clever move, and is re-measured with `fleet_parity` before the commit stands.

**NOT done here, each with its owner:**

- **No organ migration** (§1.3) — W-G3, one per lane, ADR-118 §5.
- **No `ARCHITECTURE.md` Ch2 render.** The renderer exists and the `dangling_reference` refusal is
  armed; the prose rewrite is **step D**, which AX3-7 puts in **X3**. Pinned out of this lane.
- **No `ORPHAN_DISPOSITIONS` relocation to `ecosystem/disposition-register.yaml`** (lane v-664 open
  item 2) — a mechanical move, but not this lane's row, and it would put a second `ecosystem/` edit
  beside the floor declaration for no acceptance-contract gain.
- **No merge, no push to `main`, no JOURNAL entry, no index regeneration** — contract §"What NOT to
  do"; the integrator is gate-of-record.

### 1.9 Known collisions and inherited REDs, named before they are hit

1. **`.claude/settings.json` collides with W-2′ (`[#684]`), running in parallel.** The manifest
   proves `[#727]` file-disjoint from `[#664]` but says nothing about W-2′, whose row edits
   *"`.claude/settings.json:21`"* — the `--prompts-guard` command and its matcher — while this lane
   appends a new `PreToolUse` object to the same array. **This lane merges LAST**, so the conflict
   lands on this lane's merge and is the integrator's to resolve. Mitigation taken here: the edit is
   one self-contained array element, appended after the existing two, touching no line W-2′ owns.
2. **BACKLOG.md is RED on `main` against `[#589]`'s byte bar** — 88,956 B live against the 72,000 B
   assertion in `tests/test_gen_task_tree.py`. Pre-existing and not this lane's to clear (raising
   the constant is the act `[#589]` exists to forbid). Row **body** edits are free: the view is a
   one-line projection, so AX12-1's carried clauses cost the view nothing.
3. **`test_the_disposition_register_names_no_file_that_is_gone` is RED on `main`** — §1.2. Unlike
   the two above, this one **is** this lane's, and clause 1 is not honestly discharged while it
   stands.

### 1.10 The plan, as steps

| # | Act | Commit |
|---|---|---|
| 1 | This plan, the library-first check, and AX12-1's carried clauses written into `[#664]` and `[#727]` | this commit |
| 2 | RED-first witnesses: the `[#727]` trip-tests (denial **and** pointer), the non-governed-search test, the over-match guard — all failing first | |
| 3 | Clause 1's live defect: the disposition register stops naming a file that is gone; the three queries re-measured after | |
| 4 | `scripts/hooks/deny_and_point.py` + the `.claude/settings.json` wiring + AX4-1's floor declaration — witnesses go GREEN | |
| 5 | Terra pre-merge review (`codex exec review`, read-only) | |
| 6 | Targeted `pytest` green, this artifact completed, **commit and STOP** | |
