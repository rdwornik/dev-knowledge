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
| 1 | This plan, the library-first check, and AX12-1's carried clauses written into `[#664]` and `[#727]` | `7e7ff1a4` |
| 2 | RED-first witnesses: the `[#727]` trip-tests (denial **and** pointer), the non-governed-search test, the over-match guard — all failing first | `8408ae68` |
| 3 | Clause 1's live defect: the disposition register stops naming a file that is gone; the three queries re-measured after | `466ad15b` |
| 4 | `scripts/hooks/deny_and_point.py` + the `.claude/settings.json` wiring + AX4-1's floor declaration — witnesses go GREEN | `6eb08d30` + the 16 Terra fixes |
| 5 | Terra pre-merge review (`codex exec review`, read-only) | 17 passes; pass 17 returned nothing |
| 6 | Targeted `pytest` green, this artifact completed, **commit and STOP** | this commit |

---

## Step 2 — RED-first witnesses, failing before any build code (`8408ae68`)

`tests/test_deny_and_point.py` was written and run **RED** before `scripts/hooks/deny_and_point.py`
existed (ADR-108 §B). The file is organised as the predicate is, one section per clause, so a later
reader can see which condition a test is about:

| § | What it pins |
|---|---|
| A | the trip-test the row demands — **both** the denial and the pointer, plus: every organ the pointer names EXISTS on disk, and every command the refusal prints actually runs and answers |
| B | ordinary non-governed searching is **unaffected** — `grep -n "def parse"`, a plain string, a path that names no process |
| C | the over-match guard — the measured single-word hazards (`audit`, `check`, `save`, `ship`, `cli`, `registry`, `gitenv`, `_common`) are in the fixture **on purpose** and must not resolve |
| C2 | cost ordering — the store is **not opened** for a non-search call |
| D | the `Grep` tool surface, the ADR-77 wire protocol, and cp1252-encodability of the refusal text |
| E | the live store — the guard **computes no edges of its own** (ADR-118 §1), and the command string in `.claude/settings.json` is executed rather than argued about |

The §C fixture is the part worth naming: the guard's expensive failure is over-blocking, so the
hazards that would cause it are *fixture data*, not a footnote. `test_the_guard_computes_no_edges_of_its_own`
is the ADR-118 §1 conformance witness — the guard reads the process set FPG-1 holds and derives
nothing.

## Step 3 — clause 1's live defect, cleared (`466ad15b`)

`ORPHAN_DISPOSITIONS` dispositioned `.claude/commands/override.md`, a file `5e17ecd7` deleted in
batch W. The entry is removed and replaced by a comment recording *why* it is gone, so the next
reader does not re-add it:

```
tests/test_graph_spine.py::test_the_disposition_register_names_no_file_that_is_gone
  RED on main  ->  GREEN here
```

A disposition for a file that is gone is the paper suppression `stale_dispositions()` exists to
surface — the census answering from a stale roster. The register is now clean, and the three
queries were re-measured after the edit, not before it.

## Step 4 — the guard, the wiring, and AX4-1's floor (`6eb08d30` and the sixteen fixes after it)

**The organ** — `scripts/hooks/deny_and_point.py`, stdlib only, ~670 lines including the docstring
that carries the design. Its shape is `block_immutable_edits.py`'s (library-first, "stabilized
project" tier): JSON payload on stdin, `{"decision":"block","reason":…}` + exit 2 to deny, exit 0
to allow.

**The wiring** — one `PreToolUse` object appended to `.claude/settings.json`, matcher
`Bash|PowerShell|Grep`, with the command wrapped in an existence test so that a missing
`$CLAUDE_PROJECT_DIR` cannot make `python` exit 2 — which `PreToolUse` reads as **DENY**. That is
`[#684]`'s defect, and the wrapper is this lane refusing to reproduce it while W-2′ fixes the class.

**The posture is fail-OPEN, and deliberately opposite to the ADR-77 guard beside it.** An
unparseable command, a missing payload field, an absent or unreadable store, any internal error —
all ALLOW. Only a positively identified governed search is refused. The row names over-blocking as
the expensive failure in its own text, so the asymmetry is the design, not a shortcut.

**AX4-1's floor** — `ecosystem/parity-surfaces.yaml` gains `settings-deny-and-point`, a
`settings-hook-block` row with `tier: {hub: MUST}`, and `deny_and_point.py` joins the
`.dev-knowledge` owned map of `settings-local-blocks` (a hook command matching no owned token WARNs
otherwise). The tier was **measured before it was narrowed**: `consumer: MUST` produced `MUST-absent`
on `ai-council` and `corp-monorepo`, which is minting an unsatisfiable pin, so the declaration is
hub-only with AX4-1's required one-line reason (ADR-118 §5 ships the graph fleet-wide at W-G4, and
the pointer names graph organs a consumer does not yet have). Re-measured after the narrowing:

```
[fleet-parity] 3 repo(s) walked: 188 at-parity, 19 pass-declared, 1 gate-ahead-declared,
               2 warn-undeclared, 0 must-absent, 0 tombstone-violated, 3 advisory-rewarn,
               1 stale, 0 refused
```

**0 must-absent**, and no `deny-and-point` row fires — the surface is at parity on the hub.

## Step 5 — Terra pre-merge: seventeen passes, and the loop terminated by its own rule

The contract's stopping rule is *stop when a pass returns nothing*. It took seventeen. Every finding
was triaged into ACCEPTED (fixed RED-first, one commit each) or REJECTED (with the reason recorded
and, in both cases, a test pinning the rule so the rejection is machine-checked rather than argued).

| # | Finding | Verdict | Commit |
|---|---|---|---|
| 1 | every operand was collected, so the PATH you search *in* was read as the governed question | ACCEPTED | `157864ae` |
| 2 | two P1s, both on the POINTER: `impacted_tests.py select` with no `--changed` answers off the staged diff; a bare `process-list` prints no rows | ACCEPTED | `18d75e0c` |
| 3 | only `argv[0]` was tested against the search-head set, so `uv run … rg` and `xargs grep` escaped | ACCEPTED | `ee796d2c` |
| 4 | PowerShell attaches a parameter value with a colon — `-Pattern:gen_task_tree` | ACCEPTED | `57c224b5` |
| 5 | splitting the raw string on `\|` tore quoted alternations in half; and an alternation BRANCH is itself a candidate | ACCEPTED | `09066487` |
| 6 | the escape marker was matched inside quoted text; a heredoc body was read as commands; a newline ends a command | ACCEPTED | `b49c4050` |
| 7 | a wrapper's own value-taking options hid the command it wrapped | ACCEPTED | `fd35eb93` |
| 8 | (a) an attached `-ePATTERN` is still a pattern — **ACCEPTED**; (b) "the POSIX hook command cannot run on Windows" — **REJECTED on live evidence** | split | `78309897` |
| 9 | `strip_heredocs` recognised only identifier-shaped delimiters, so `<<'END-MSG'` left its body in the stream — an over-block | ACCEPTED | `01a28d1a` |
| 10 | `\b` word boundaries and `\.` escaped literals defeated resolution | ACCEPTED | `c32e35b2` |
| 11 | re-assertion of 8(b) | **REJECTED** — and converted into a test that EXECUTES the command string from `.claude/settings.json` through bash, so the claim is now machine-checked | `b52b139c` |
| 12 | backslash path spellings did not resolve — **half right**: `./scripts/…` already resolved, only the backslash forms failed | ACCEPTED (narrowed) | `edd8b4f3` |
| 13 | the escape was evaluated over the whole command, so a declaration covered LATER lines | ACCEPTED | `2aaa7ed7` |
| 14 | …and earlier commands on its OWN line | ACCEPTED | `05119d8c` |
| 15 | "a declaration trailing an EMPTY segment is void, so `rg X; # raw-needed: r` should deny" | **REJECTED on design** — all five forms were mapped and it grants no extra power; over-blocking a good-faith declaration is the failure this row names. The rule is pinned by a test instead | `ad1010fe` |
| 16 | POSIX `shlex` ate unquoted backslashes on the **`PowerShell`** surface — a hole on one of the guard's own configured tools | ACCEPTED | `ad2f8435` |
| 17 | *nothing* — "No blocking regressions were identified in the diff." | **STOP** | — |

**14 findings accepted and fixed; 2 rejected.** Both rejections carry a test rather than a
paragraph, which is the point: a rejected finding that leaves no witness is an argument, and the
next review re-opens it (pass 11 is the proof — it re-asserted pass 8(b) verbatim).

**Three of the seventeen were the same escape clause in a row** (6, 13, 14), each one notch tighter.
That is recorded rather than smoothed over: a *declared* bypass is only as good as the precision of
what it declares, and getting that precision right took three findings plus one rejected fourth.

## Step 6 — final state

### 6.1 What changed

```
scripts/hooks/deny_and_point.py     NEW   +672   the [#727] guard
tests/test_deny_and_point.py        NEW   +753   116 tests
.claude/settings.json               EDIT  +12/-0 one PreToolUse object + the wiring comment
ecosystem/parity-surfaces.yaml      EDIT  +30/-0 AX4-1's floor declaration
scripts/graph_queries.py            EDIT  +13/-4 the stale disposition, removed
tasks/664-*.md, tasks/727-*.md      EDIT  2 rows AX12-1's carried clauses
docs/audits/2026-09-11-...-lane-x-664-delivery-spine.md  NEW  this file
```

Every path is inside the footprint the manifest declares. `BACKLOG.md` is not in the diff and that
is correct, not an omission: the view is a one-line projection of each row, so a row **body** edit
changes no byte of it — and a lane does not regenerate a gate-of-record surface.

### 6.2 The Done-contract, clause by clause

**Clause 1 — the spine.** DISCHARGED, re-measured on this tree rather than read off lane v-664's
artifact:

```
store          2563 nodes · 19500 edges · 15 edge kinds, persisted in stdlib sqlite under
               the RESOLVED git dir (per-worktree), rebuilt by the graph-rebuild pre-commit hook
orphan-census  OK   (exit 0)   -- 0 against its STATED node class
task-coverage  OK   (exit 0)   -- 0 FAIL
process-list   OK   159 processes, 120 triggered, 39 not
trip-tests     tests/test_graph_spine.py -- one per query, 35 tests
```

The 32-vs-20 cardinality gap is **recorded, not rounded** (§1.2, and lane v-664 §1.4/§2.4). The
blanket "12 → 0" bar is dead and was re-measured under §A.1's five-kind class: **N-before 18,
N-after 18, migrated 0**, every remaining site named and owned by W-G3.

The new guard is itself a **triggered** process — `process-list` counts 159/120 where it counted
158/119 before, so wiring the organ did not create an orphan. That is the spine checking this
lane's own work.

**Clause 2 — `[#727]` rides in this lane.** DISCHARGED:

- a `PreToolUse` **deny-and-point** hook whose exception text NAMES the organ to run — four
  pointers, each parameterised on the resolved path, each verified to exist and to answer;
- a **RED-first trip-test asserting BOTH** the denial and the pointer (§A), written and failing
  before the guard existed;
- ordinary non-governed searching **provably** unaffected — §B and §C, and the proof is a property
  of the predicate (clause 3 of §1.6): a plain string is undeniable unless the string *is* a
  process;
- **floor: MUST**, declared in `ecosystem/parity-surfaces.yaml`, `fleet_parity` re-measured green.

The known failure mode the row names — over-broad matching wedging every session — is guarded by
§C's measured hazard fixture and by the fail-OPEN posture, and the escape (`# raw-needed: <reason>`)
means a refusal always has a lawful way through.

**Clause 3 — house rules.** English throughout; hyphen-only names; the guard logs nothing to stdout
except the refusal JSON the wire protocol requires (no `print` diagnostics); no Click CLI, because
this organ has no CLI — it is a hook with a stdin protocol, and adding one would be inventory;
`pytest` green.

```
tests/test_deny_and_point.py + tests/test_graph_spine.py   151 passed
ruff check                                                 All checks passed!
```

### 6.3 Open items — the integrator's, named rather than left to be discovered

1. **`.claude/settings.json` will conflict with W-2′ (`[#684]`).** W-2′ edits line 21 (the
   `--prompts-guard` command); this lane appends a third array element after the existing two and
   extends the `//` comment. **This lane merges LAST in batch X**, so the conflict lands here by
   design. The resolution is additive — keep W-2′'s line 21 and this lane's new object.
2. **The `$CLAUDE_PROJECT_DIR` wrapper shape is a question, not a defect.** This lane wraps its own
   command in `[ -f "$G" ]` so an unset variable cannot make `python` exit 2 (= DENY). If W-2′ lands
   a general fix for that class, the wrapper becomes belt-and-braces rather than wrong. Whether to
   simplify it afterwards is the integrator's call; it is recorded here so the choice is visible.
3. **Two declared bypasses ride in every commit of this lane**, per-hook attributed in each body,
   never `--no-verify`:
   - `doc-counts-pytest-freshness` — the lane adds 116 tests, so the `pytest_collected` claim moves
     on every commit. On this tree: **file 5752 / actual 5868**. Restate it **once**, at
     integration.
   - `organ-index-freshness` — the committed index is **already stale on `main`**: it still lists
     `/override`, whose file `5e17ecd7` deleted in batch W. A lane must not regenerate the index
     (integrator is gate-of-record), and this lane adds one more organ to it.
4. **Inherited RED, not this lane's:** `BACKLOG.md` is 88,956 B against `[#589]`'s 72,000 B
   assertion in `tests/test_gen_task_tree.py`. Pre-existing on `main`; raising the constant is the
   act `[#589]` exists to forbid.
5. **`[#664]` stays OPEN and that is conforming.** AX3-7 puts step D (the `ARCHITECTURE.md` Ch2
   render) and the organ map in **X3**, and ADR-118 §5 puts the eighteen edge-computation
   migrations in W-G3, one organ per lane. Both are named in the row itself (§1.3, §1.8).
6. **`[#727]` is complete against its Done-when** — every clause above is discharged with a witness.
   Closing it is the operator's word, not this lane's.

### 6.4 Working notes worth keeping

- **A `PreToolUse` hook judges the WHOLE command line.** Bundling a positive and a negative probe
  into one `&&` chain got the whole call denied by the second half. Probes go one per call.
- **The guard denied its own commit.** A `git commit -F -` heredoc whose message quoted a search
  command was read as a search, because the heredoc BODY was still in the command stream. That is
  pass 6/9's lineage, and it is the strongest argument for the fail-OPEN posture: a guard that can
  block the commit that fixes it is one bad predicate away from wedging a session.
- **A newline ends a command**; `shlex` treats it as ordinary whitespace. Lines are lexed one at a
  time for that reason.
- **The `block-onedrive` guard scans command TEXT, not file content.** Writing this artifact through
  a heredoc is refused where writing it through the Write tool is not — the destination path is what
  that guard reads.
