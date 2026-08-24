# L7 — Dispatch codification (M10): PLAYBOOK Ch8 + `gen_lane_contract` emits the command

| Field | Value |
|---|---|
| **Lane** | L7 `dispatch-codification` · branch `worktree-dispatch-codification` |
| **Contract** | `LANE-L7-dispatch-codification.md` (operator-side, `$env:CLAUDE_PROMPTS_DIR`) |
| **Scope** | `protocols/PLAYBOOK.md` Ch8 (exclusive) · `scripts/gen_lane_contract.py` · its tests |
| **Shape** | local background lane, commit-and-STOP |
| **Base** | `aeec0fd1` |

---

## 1. Ground truth — Ch8 and `gen_lane_contract` as they stand

Recorded before any edit, so every delta below is attributable.

### 1.1 What Ch8 already says about dispatch

Ch8 spans `protocols/PLAYBOOK.md` lines 1236–2512 and carries **fifteen** `###` subsections. Four
are dispatch-bearing, which is why "codify the cheat-sheet" is *not* a green-field write:

- **"Dispatch prompts and the contract of record — two locations, one of them in the tree."**
  The prompts-dir rule (`~/Downloads` by default, `CLAUDE_PROMPTS_DIR` override) and the Q6
  contract-as-file ruling. States that a dispatch line cites `<PROMPTS_DIR>\<file>` **rather than
  a hard-coded absolute path**, so the line stays portable and one operator's directory layout
  stays out of an artifact other people read.
- **"The dispatch surface is `dispatch <file>` — the contract file is the source ([#509] v2)."**
  Claims in its opening sentence that *"the operator's whole dispatch surface is one typed line:
  `dispatch <contract.md>`"*, implemented by `win-tooling`
  `scripts/dispatch/Invoke-Dispatch.ps1` (merged `d743937`). Carries the batch-6 doubled-prefix
  incident, the `## Dispatch`-block contract mode, the table fallback, the closed effort enum and
  the execution gate.
- **"Cloud lanes — the receipt gate and the fresh-branch rule."** Q5 receipt gate, Q4
  fresh-off-`origin/main` hygiene, and the `claude/<slug>` branch prefix. Explicitly records
  **which-substrate as OWED, not ruled** — *"a section about cloud lanes is hard to apply without
  a test for which lanes are one, and this chapter carries none today."*
- **"Model + effort are stated at dispatch — the routing matrix."** The opus/sonnet/haiku table,
  the 2026-08-07 context-load amendment, `max` held out of *routing*, and the three dispatch
  constants.

**What Ch8 does NOT carry today — the gap M10 names:**

1. **No local-vs-cloud boundary a seat can apply.** The cloud-lane section says so in its own
   words and files the gap as G1 of `docs/audits/2026-08-20-technical-playbook-status.md`. The
   operator's cheat-sheet resolves it (does the work need his disk, or is everything on
   `origin/main`?) and that resolution is nowhere in the chapter.
2. **No enumeration of the three command shapes.** `Dispatch-Lane` and `Dispatch-CloudV2` appear
   **nowhere in `protocols/`** — verified by grep across the whole repo: every hit is in
   `scripts/gen_lane_contract.py`, its tests, `tasks/539-*`, two handoff bundles and six
   `docs/audits/` files. Zero doctrine hits.
3. **A stale headline claim.** *"The operator's whole dispatch surface is one typed line:
   `dispatch <contract.md>`"* is true of one shape of three. `Invoke-Dispatch.ps1` dispatches a
   **local** contract; it is not the cloud transport and not the interactive form. A seat reading
   that sentence while holding a cloud brief has no next move.
4. **No integration-is-always-local-and-interactive rule.** Ch8's parallel-session section rules
   that integration happens from the primary checkout on operator GO; it never states the
   consequence for *dispatch* — that integration cannot be a background lane at all, because a
   background lane can neither merge to main nor ask a question.

**Stale Ch8 claims handed over by LANE-L5:** *none received.* At the time of this write L5 had not
landed — `git worktree list` shows six sibling lanes all still at the batch base `aeec0fd1` with
no lane commits, and `docs/audits/` carries no L5 artifact. Recorded as **not-received**, not as
none-existing.

**One claim IS inherited, from the predecessor lane.** `docs/audits/2026-08-21-technical-ch8-
dispatch-codification.md` (batch-1 lane A, `[#539]` — the lane that wrote the Q1/Q3–Q6 rulings
into Ch8 and built this generator) closes with an open item aimed squarely here:

> `templates/prompt-template.md` v1.14 carries the effort enum as the closed four and shows a
> `claude --bg --model … --effort …` dispatch line, while `[#539]`'s contract shows the
> `Dispatch-Lane` form. Both are live; neither is wrong. **If `Dispatch-Lane` becomes the stated
> surface, the card is the point-of-use copy that would follow** — not this lane's file.

This lane **does** make `Dispatch-Lane` the stated surface. The card is therefore now owed an
update, and it is outside this lane's write scope (`protocols/` Ch8 + the generator). Carried as
residual R1 in §6.

### 1.2 What the generator already emits — and the defect in it

`scripts/gen_lane_contract.py` (576 lines, Click-based, `emit` / `check` / `enums`).
`render_contract` is pure: same `LaneSpec` in, byte-identical markdown out. Emitted sections:
`Dispatch`, `Worktree pairing`, `[Receipt gate]`, `Done-contract`, `Decision budget`, `Steps`,
`What NOT to do`.

It **already emits a command line** — the surprise of step 1, and it sharpens the deliverable. In
`render_contract`, unconditionally:

~~~
## Dispatch

```
Dispatch-Lane {slug} {fname} -Effort {effort}
```
~~~

**The defect is the one the contract's failure-mode paragraph predicts, with the polarity
reversed.** `spec.cloud` is honoured in exactly one place — it adds the `## Receipt gate` section
— and **nowhere else**. So, before this lane:

- `gen_lane_contract emit --cloud` produced a contract whose command line was **`Dispatch-Lane`**,
  the *local* helper. **A cloud lane handed a local command** — authoritative-looking and wrong.
- That contract's pairing line declared branch **`worktree-<slug>`**, while Ch8's own cloud-lane
  section rules a cloud lane onto **`claude/<slug>`**.
- There was **no interactive shape at all**. `MODE_ENUM` (`execute | plan-then-auto | plan`) is a
  *lane mode*, not a substrate; nothing in the generator's model could express "this is an
  interactive seat act."

`parse_contract` mirrored the blind spot: `_DISPATCH_LINE_RE` matched `Dispatch-Lane` and nothing
else, so a contract carrying the **correct** cloud command would have been refused by the live
`lane-contract-check` pre-commit hook as *"no dispatch line found"*. The gate enforced the wrong
shape onto two cases of three.

**Consequence for the closure contract.** Item 2 is not "add a missing emission" — it is "make the
existing emission *shape-selective*, and make the checker able to verify the selection". The test
the contract demands (*a generated contract with no command line fails*) is necessary but not
sufficient on its own: it would have passed on 2026-08-22 against a generator that emitted the
wrong command for two shapes out of three. **Item 3 is the load-bearing one.**

### 1.3 Cheat-sheet verified against the live helpers

The contract calls the operator's cheat-sheet authoritative. It was still checked against source,
because a command line that does not exist is precisely the failure this lane exists to close.
`win-tooling/config/dispatch-helpers/DispatchHelpers.psm1` (1211 lines) is the stated source of
truth; `scripts/dispatch-helpers/Apply-DispatchHelpers.ps1` deploys it SHA-256-compared and
auto-loading.

| Cheat-sheet claim | Source | Verdict |
|---|---|---|
| `Dispatch-Lane <slug> <FILE.md> [-Effort]` | alias L1196 → `Start-DispatchLane` L47; `Slug`/`File`/`Extra` positional 0/1/2 | **confirmed** |
| optional 3rd positional = extra instruction | `[Parameter(Position = 2)][string]$Extra` | **confirmed** |
| `-Effort ∈ {low,medium,high,xhigh,max}` | `$effortMap`, plus `l`/`m`/`med`/`h`/`x` shorthands | **confirmed** (shorthands are an undocumented bonus) |
| model defaults `opus`; `bypassPermissions` default | `$Model = 'opus'`, `$PermissionMode = 'bypassPermissions'` | **confirmed** |
| creates `worktree-<slug>`, refuses if that branch exists | guard 1, "SKIP-IF-BRANCH-EXISTS" | **confirmed** |
| `Dispatch-CloudV2 <FILE.md> -Title '<slug>'` | alias L1198 → `Start-DispatchCloudV2` L871; `File` positional 0, `Title` named | **confirmed** |
| whole file is the brief, JSON body | `New-CloudSessionBody`; docstring *"puts the brief in a JSON body"* | **confirmed** |
| binds Revision `main` | `[string]$Revision = 'main'` | **confirmed** |
| G1 created / G2 bound / G3 receipt; empty `sources` = hard fail | docstring: G1+G2 **HARD**, G3 **SOFT ON TIMEOUT** | **confirmed** |

Two facts the cheat-sheet omits and a seat should have, both folded into the Ch8 codification:
`Start-DispatchLane` polls up to `-WaitSeconds 120` for the branch and reports a **timeout as a
WARNING, not an error** (the lane may still be coming up — it refuses to claim a failure it has
not established); and `Dispatch-CloudBrief` is a **superseded** third alias that prints its own
supersession notice on every call.

### 1.4 Library-first verdict (required by the contract)

**Verdict: no external library. The library-first move is internal, and it was taken.**

The mechanization half is string emission from a generator that already exists. There is no
external candidate for "emit a line into a template" that would not become a second templating
idiom beside `render_contract`'s `parts: list[str]` accumulation — the contract names exactly that
hazard, and it is the real risk here.

Reused rather than rebuilt, itemised:

- **`render_contract`'s `parts.append` idiom** — the command emission is one more branch inside
  the same function. No template engine, no `str.format` layer, no second renderer.
- **`_DISPATCH_LINE_RE`'s regex-per-shape idiom** — the two new shapes get sibling patterns
  compiled beside it, read by the same `parse_contract`, rather than a parser rewrite.
- **`validate_branch_naming.validate_lane_worktree_name`** — still called, still not
  re-implemented; the module docstring's existing library-first claim stays true.
- **`LaneContractError` and the `validate_*` refusal posture** — the new shape enum refuses
  through the same class with the same *name the enum, never round to a neighbour* message shape.
- **`click.Choice`** — shape selection is a CLI enum the same way model/mode/effort already are.

The one thing deliberately **not** reused: `MODE_ENUM`. It was the tempting hook — already a
declared enum on the spec — and it is the wrong one. Mode is *how a lane thinks*; shape is *where
it runs*. Overloading it would have made `plan` imply a substrate.

---

## 2. What landed

### 2.1 PLAYBOOK Ch8 — the codification half (`959b80a1`)

One new subsection, **"Dispatching a session — the boundary, the three shapes, and the standing
rules"**, placed at the head of Ch8's dispatch cluster so a seat meets it before the sections that
rule on a dispatch's *conditions*. It carries:

- **The boundary** — LOCAL if the work needs the operator's disk (provider keys and vendor CLIs,
  unpushed branches, files in the prompts dir); CLOUD if every input is on `origin/main`;
  **integration always LOCAL *and* INTERACTIVE**, because a background lane can neither merge to
  `main` nor ask a question, so an integrator dispatched `--bg` is a contradiction in terms.
- **The three shapes with their literal commands** — `Dispatch-Lane <slug> <FILE.md> -Effort high`
  (plus the optional third positional as the amendment channel), `Dispatch-CloudV2 <FILE.md>
  -Title '<slug>'`, and `claude` plus its `Read <PROMPTS_DIR>\<FILE>.md and execute it exactly.`
  first message — each with the facts a seat would otherwise have to read the PowerShell module
  for: the effort enum, the branch-exists refusal, the 120 s branch wait whose **timeout is a
  WARNING rather than an error**, cwd-binding, one-file-one-lane, Revision `main`, and G1/G2 hard
  vs G3 soft-on-timeout.
- **The five standing operator-interface rules** — prompts dir not Desktop; `.md` upload because
  inline paste arrives empty; no session ships without its command; artifacts to `docs/audits/`;
  teardown sequenced after a STOP.

**Two neighbouring Ch8 claims were reconciled rather than left to contradict the new one.** This
is the half a "just add a section" reading would have skipped, and it is where the drift lives:

| Site | Was | Now |
|---|---|---|
| "The dispatch surface is `dispatch <file>`" | *"the operator's **whole** dispatch surface is one typed line"* | scoped by a dated amendment to **shape 1 of 3**; the rest of the section stands unchanged |
| "Cloud lanes" — *"Which substrate — RECORDED AS OWED, not ruled here"* | recorded the routing test as absent, filed as **G1** of `docs/audits/2026-08-20-technical-playbook-status.md` | marked **ANSWERED**, pointing at the boundary above; the gate-mesh heuristic is kept as the refinement it always was, and G1 is stated as discharged **by the boundary subsection, not by that paragraph** |

Two further census rows are discharged in passing, and are named rather than left to be
rediscovered: **G6** (`Dispatch-Lane`'s name, its one-block shape and skip-if-branch-exists — the
row explicitly asks for an amendment here) and **G7** (short effort forms). G7 is landed with a
**correction to the row's own premise**: it reads *"`--effort` takes full names only; short forms
are silently ignored"*, and that is true of the **raw CLI** but false of the helper, whose
`$effortMap` maps `l`/`m`/`med`/`h`/`x`. Ch8 now states both halves, because the helper's docstring
says it maps them *precisely because* `claude --effort m` does not.

**The Ch11 collision the census warned about is handled.** `docs/audits/2026-08-20-technical-
playbook-status.md` closes its gap table with one authoring constraint — PLAYBOOK's cloud
vocabulary is already taken by Ch11's **scheduled Routines**, and a G1/G2 write that does not name
the distinction silently merges two populations. The boundary's CLOUD bullet opens by naming it: a
*dispatched cloud lane* is not a *scheduled cloud Routine*, and they share a word and nothing else.

### 2.2 `gen_lane_contract` — the mechanization half (`df9ce8a8` tests, `74cfa2f0` code)

Full rationale is in the two commit bodies. In short: `SHAPE_ENUM = (local, cloud, interactive)`
becomes the substrate the contract declares; `dispatch_command()` is the **single source** for the
literal line, read by the emitter, by the `emit` log line and — through `_COMMAND_RES` — by the
parser, so the three cannot drift into emitting a form the checker rejects; every contract carries
a `**Shape:**` line so the command can be checked against *something*; `branch_name(slug, shape)`
derives `worktree-` / `claude/` / none; and `parse_contract` refuses a contract with no command,
with two commands, with an off-enum shape, or with a command that disagrees with its own declared
shape.

---

## 3. Emitted-command evidence — all three shapes, actual output

Not a description. This is the terminal output of `.l7_proof.py`, which emits one contract per
shape into a scratch directory and then runs **the same entry point the `lane-contract-check`
pre-commit hook runs** (`gen_lane_contract.py check <path>`) over each — so the round trip is
proven through the live gate rather than through an import. It also asserts the WRONG shape
against each file, because a checker that accepts everything proves nothing.

```
=== local ===
emit rc=0
  LOG gen-lane-contract: wrote ...\LANE-a-777-widget.md
  LOG gen-lane-contract: dispatch with: Dispatch-Lane lane-a-777-widget LANE-a-777-widget.md -Effort high
  EMITTED COMMAND LINE(S):
    Dispatch-Lane lane-a-777-widget LANE-a-777-widget.md -Effort high
  check --expect-shape local: rc=0
    gen-lane-contract: ...\LANE-a-777-widget.md: OK - 6 sections, shape local, slug lane-a-777-widget, branch worktree-lane-a-777-widget, command 'Dispatch-Lane lane-a-777-widget LANE-a-777-widget.md -Effort high'
  check --expect-shape cloud: rc=1 -> REFUSED (correct)
=== cloud ===
emit rc=0
  LOG gen-lane-contract: wrote ...\LANE-b-778-audit.md
  LOG gen-lane-contract: dispatch with: Dispatch-CloudV2 LANE-b-778-audit.md -Title 'lane-b-778-audit'
  EMITTED COMMAND LINE(S):
    Dispatch-CloudV2 LANE-b-778-audit.md -Title 'lane-b-778-audit'
  check --expect-shape cloud: rc=0
    gen-lane-contract: ...\LANE-b-778-audit.md: OK - 7 sections, shape cloud, slug lane-b-778-audit, branch claude/lane-b-778-audit, command "Dispatch-CloudV2 LANE-b-778-audit.md -Title 'lane-b-778-audit'"
  check --expect-shape local: rc=1 -> REFUSED (correct)
=== interactive ===
emit rc=0
  LOG gen-lane-contract: wrote ...\LANE-c-779-integrate.md
  LOG gen-lane-contract: dispatch with: start `claude`, then send: Read <PROMPTS_DIR>\LANE-c-779-integrate.md and execute it exactly.
  EMITTED COMMAND LINE(S):
    claude
    Read <PROMPTS_DIR>\LANE-c-779-integrate.md and execute it exactly.
  check --expect-shape interactive: rc=0
    gen-lane-contract: ...\LANE-c-779-integrate.md: OK - 6 sections, shape interactive, slug lane-c-779-integrate, branch (none - interactive), command 'Read <PROMPTS_DIR>\\LANE-c-779-integrate.md and execute it exactly.'
  check --expect-shape cloud: rc=1 -> REFUSED (correct)
scratch removed: True
```

**Read the three `EMITTED COMMAND LINE(S)` blocks against each other — that is the whole
deliverable.** Before this lane all three read `Dispatch-Lane …`, because `spec.cloud` never
reached the emission. The `branch` field in the three `check` lines is the same story in the
pairing: `worktree-lane-a-777-widget` · `claude/lane-b-778-audit` · `(none — interactive)`, where
all three previously read `worktree-<slug>`.

**Two honest limits of this evidence, stated rather than left to be assumed away:**

1. `--expect-shape` is a **flag a caller passes**, and the `lane-contract-check` hook passes no
   flags — at commit time nothing outside a file says what shape it was *meant* to be. The
   protection the hook actually gets is the **internal** one: declared `**Shape:**` vs emitted
   command, which is checked with no flag at all and is what the mutation pass below exercises.
2. The scratch contracts were emitted to a temp directory and removed (`scratch removed: True`).
   Nothing named `LANE-*.md` was left in the tree, so this lane adds no file to the hook's glob.

---

## 4. terra review — tally in the body, as the contract requires

**Reviewer:** terra, run directly on the diff rather than through the review skill. The skill
writes into `docs/audits/`, which this lane also writes; the contract names that trap explicitly
("that trap has fired here before"), so the direct route was taken.

### 4.1 Tally

```
Critical: 0
High:     0
Medium:   2  (both fixed in-lane, before this commit — see 4.3)
Low:      1  (fixed in-lane)
Info:     2  (recorded, not actioned — see 4.4)
```

**Zero Critical / zero High.** The three Medium/Low findings were found by the mutation pass and
by the file's own test suite while the work was in flight, and each was fixed rather than
dispositioned.

### 4.2 Mutation evidence — 8 mutants, 8 killed

The claim "there is a test asserting exactly that" is only worth what a mutation pass says it is.
`.l7_mutate.py` applies each mutation to `scripts/gen_lane_contract.py`, runs the suite, restores
the file and asserts the restore was byte-identical:

```
[KILLED] M1 dispatch_command always emits the LOCAL form (the pre-lane defect)   7 failed, 98 passed
[KILLED] M2 the declared **Shape:** line is not emitted                         14 failed, 91 passed
[KILLED] M3 branch_name ignores the shape (always worktree-)                     2 failed, 103 passed
[KILLED] M4 the missing-command-line refusal is dropped                          1 failed, 104 passed
[KILLED] M5 the shape/command disagreement refusal is dropped                    2 failed, 103 passed
[KILLED] M6 the interactive first message loses its `claude` start line          1 failed, 104 passed
[KILLED] M7 the emit log line hard-codes the local command                       1 failed, 104 passed
[KILLED] M8 the receipt gate is emitted for every shape                          9 failed, 96 passed
source restored byte-identical
```

**M1 is the contract's own stated failure mode, reproduced and killed** — it reverts the generator
to emitting `Dispatch-Lane` for every shape, which is exactly what it did on 2026-08-22. **M4 is
the contract's Done-item 2**, and it kills exactly one test, which is the right number: the
missing-command-line refusal has one dedicated regression rather than being incidentally covered.

Note `mutmut` was **not** used and could not be: `[tool.mutmut]` in `pyproject.toml` records that
it requires `fork()` and is CI-only, so a Windows host cannot run it. This is a hand-authored
mutation pass, which is the same shape the 2026-08-22 `check_s10` deletion test used.

### 4.3 Findings fixed in-lane

**M-1 (Medium) — a pre-existing test silently stopped testing.**
`test_a_doubled_prefix_in_the_pairing_line_is_reported` mutated the substring
``branch `worktree-lane-a-539-ch8-codification` `` with `count=1`. The new dispatch prose *also*
names the branch and sits **above** the pairing line, so the replace hit the prose instead: the
pairing line was never mangled, `parse_contract` correctly reported no problems, and the assertion
failed. The failure was loud here by luck — had the prose been added *below* the pairing line the
test would have kept passing while checking nothing. Fixed by anchoring the mutation on the whole
pairing line plus a guard assertion that fails if that line moves. **This is the more valuable
finding of the two**, because the class (an unanchored `replace` in a mutation test) is live in
several other tests in this file.

**M-2 (Medium) — CRLF laundering through the mutation harness.** `.l7_mutate.py` restored the
source with `Path.write_text`, which applies platform newline translation on Windows: the restore
assertion passed (`read_text` translates back) while all 892 line endings on disk had become CRLF.
Caught by `git add`'s own warning, not by any gate. Normalized back to LF before staging, and the
committed blob was verified LF.

**L-1 (Low) — `SyntaxWarning: invalid escape sequence '\<'`.** The new module docstring contains
the literal interactive command `Read <PROMPTS_DIR>\<file> …`; in a non-raw docstring `\<` is an
invalid escape. Python currently warns and will eventually error. Fixed by escaping to `\\<file>`
rather than by making the whole docstring raw, which would have silently changed every other
escape in it.

### 4.4 Findings recorded, not actioned

**I-1 (Info) — `## Worktree pairing` is now a slightly wrong heading for one shape.** An
interactive contract has no worktree, and its body says so in its first words. The heading is kept
because `MANDATORY_SECTIONS` is the checkable surface the hook reads, and renaming it for one
shape would either fork the mandatory-section list by shape or rename it for all three. Neither is
worth a heading. Recorded so it is a known compromise rather than an oversight.

**I-2 (Info) — `contract_filename` still emits `LANE-<stem>.md` for a cloud brief.** Live cloud
briefs in this repo are named `CLOUD-C1-….md`. Keeping `LANE-` is deliberate: it is what the
`lane-contract-check` hook's glob (`(^|/)LANE-[^/]*\.md$`) matches, so a cloud contract emitted
under a `CLOUD-` name would leave the gate's coverage entirely. Changing the glob is not in this
lane's footprint.

---

## 5. Suite

Measured against the A2 baseline in section 7 below, with every additional RED attributed.

---

## 6. Residuals, and the one operator decision this lane owes

### R0 — OPERATOR RULING OWED: raise `ecosystem/silent-rule-baseline.yaml` 441 → 445

**This is a decision-budget class (a) item — a curated-baseline touch — and this lane does not
take it.** The baseline file's own header rules that raising is an operator act and that *"there
is no code path that raises it"*, which is why this is queued with attribution rather than done.

**The measurement, not an estimate.** `check_silent_rule_ratchet` FAILed the first attempt at the
Ch8 commit. Counting `\b(?:must|shall|never)\b` case-insensitively, exactly as the detector does:

| Blob | Occurrences |
|---|---|
| `aeec0fd1:protocols/PLAYBOOK.md` (the merge base) | **210** |
| this branch's `protocols/PLAYBOOK.md` | **214** |
| live corpus total (`silent_rule_detector.py`, 59 files) | **445** |
| committed baseline (`detector_id: silent-rule-v4`) | **441** |

**main sits EXACTLY at the baseline with zero headroom**, so *any* codification of normative
doctrine into a `protocols/` file trips this gate by construction. That is a property of the
current baseline, not of this lane.

**Six occurrences were added on the first pass; two were drained and four were kept, and the split
is the part worth reviewing.** The two drained were **descriptive, not normative** — "the other
sections rule on what a dispatch *must* satisfy … and *never* state what the operator types" is a
sentence *about* rules, and the detector's own docstring admits it "cannot distinguish a rule from
a mention of one in an example". Removing a false positive improves the measurement.

The four kept are the standing rules this lane was dispatched to codify, line by line:

| # | Line, as it stands in Ch8 | Why it is not drained |
|---|---|---|
| 1 | "the **whole file is the brief** … so **one file = one lane, never a multi-lane bundle**" | the bundle-mode defect is the named G2 hard-fail condition |
| 2 | "Every prompt file reaches the operator via the prompts dir (`~\Downloads`), **never** the Desktop" | a standing operator-interface rule, verbatim from the cheat-sheet |
| 3 | "**Lane artifacts land in `docs/audits/`, never the repo root**" | `validate-hermetization` Rule A refuses the alternative |
| 4 | "**Teardown is sequenced *after* a session STOPs**, **never** alongside a ruling that keeps it alive" | a standing operator-interface rule, verbatim from the cheat-sheet |

Swapping "never" for "not" in these four would lower the metric **without removing a rule** — the
exact inverse of the v1→v2 occurrence-counting correction the detector contract records, and a
form of gaming this repo has already ruled against once. They are left intact and the raise is
put to the operator instead.

**Precedent, in the baseline's own provenance block:** RAISE 428 → 441, operator-ruled 2026-07-30
for the intake-#18 ratification arc, with line-by-line attribution in
`docs/audits/2026-07-30-technical-intake18-ratification-record.md`, and the note that *"until that
arc merges, the branch-side check reads raise-rejected vs origin/main — expected, self-healing at
merge."* This lane is in that same window.

#### R0a — RULING R8: APPROVED on the merits. The raise is SHIPPED HERE, not applied.

**Operator ruling, 2026-08-23 (R8).** The raise 441 -> 445 stands on the attribution above.
The order is explicit and is followed to the letter: **ship the raise, do not apply it.**
`ecosystem/silent-rule-baseline.yaml` is **not written by this lane** — it still reads
`baseline: 441` at this branch's tip, verified with `git status --porcelain` after the diff
below was generated.

**Why it is shipped rather than applied, in the operator's own reasoning: 445 is
N-dependent.** It was measured against **this branch alone**. `protocols/` is inside the
detector's scope roots and sibling lanes of this batch sweep it, so the live number moves
again as each one merges. **A value pinned before the last merge is pinned to a pre-merge
measurement.** This is the same class as the `ALL_CHECKS` count pins under binding amendment
A6, and it gets the same handling: **the integrator counts once, at the end, and sets it.**

**The change, as a diff ready to apply.** Generated mechanically — the proposed content was
written to a scratch path and diffed against the real file with `git diff --no-index`, so the
hunk header is git's own rather than hand-counted, and it was proven with
`git apply --check` (dry run, nothing written):

```diff
diff --git a/ecosystem/silent-rule-baseline.yaml b/ecosystem/silent-rule-baseline.yaml
index 606592c0..2143c434 100644
--- a/ecosystem/silent-rule-baseline.yaml
+++ b/ecosystem/silent-rule-baseline.yaml
@@ -18,20 +18,28 @@
 # commensurable; the check refuses to compare them rather than silently reporting drift.
 
 detector_id: silent-rule-v4
-baseline: 441
-measured_at: 2026-07-30
-measured_at_sha: 3cd4417a
-measured_files: 56
+baseline: 445
+measured_at: 2026-08-23
+measured_at_sha: <INTEGRATOR-SETS-THIS>
+measured_files: 59
 
 provenance: |
-  RAISE 428 -> 441, operator-RULED 2026-07-30 (the intake #18 ratification arc, [#435]):
-  the ruled-verbatim adopted texts (A4 checklist, A2/A9/A6/A10 staged paragraphs, U3
-  statement, A3 template extract) add exactly +14 normative-token occurrences over the
-  pre-arc live 427; line-by-line attribution + the ruling's four conditions:
-  docs/audits/2026-07-30-technical-intake18-ratification-record.md ("Silent-rule ratchet"
-  section). Until that arc merges, the branch-side check reads raise-rejected vs
-  origin/main (428) -- expected, self-healing at merge.
-  Prior baseline: 428 @ 2026-07-27 (sha 527958fbf89311610bd3be65fbfcb77df1f5fe29).
+  RAISE 441 -> 445, operator-RULED 2026-08-23 (RULING R8; M10 dispatch codification,
+  lane L7). The Ch8 subsection "Dispatching a session -- the boundary, the three shapes,
+  and the standing rules" adds exactly +4 normative-token occurrences over the pre-lane
+  live 441: protocols/PLAYBOOK.md blob 210 -> 214, every other file in scope unchanged.
+  Six were added; TWO were drained as descriptive false positives (sentences ABOUT rules,
+  which the detector cannot tell from rules), and the FOUR kept are the standing
+  operator-interface rules the lane was dispatched to write. They are enumerated with
+  their lines in
+  docs/audits/2026-08-23-technical-lane-dispatch-codification.md section R0.
+  N-DEPENDENT -- READ BEFORE PINNING. 445 was measured against lane L7's branch ALONE.
+  protocols/ is inside the detector's scope roots and sibling lanes of the same batch
+  sweep it, so the live number moves again as each one merges. The INTEGRATOR re-measures
+  after the LAST merge (`python scripts/silent_rule_detector.py`) and sets baseline,
+  measured_at_sha and measured_files from that run. Same handling as the ALL_CHECKS count
+  pins: a value pinned before the last merge is pinned to a pre-merge measurement.
+  Prior baseline: 441 @ 2026-07-30 (sha 3cd4417a).
   Baseline semantics: detector-measured at arm time. Architect-proposed 2026-07-27,
   operator-adopted (D4), subject to revision after live testing. Historical ruling
   reference: 176 @ 2026-07-26; floor >= 179 per
```

**`git apply --check` on this diff: CLEAN.** The scratch file was removed; the real baseline
file was read and never written.

**What the integrator MUST re-derive after the LAST merge of this batch, not before:**

| Field | In the diff | Why it moves |
|---|---|---|
| `baseline` | `445` | L7's branch alone. Re-run `python scripts/silent_rule_detector.py` after the final merge. |
| `measured_files` | `59` | 56 at the 2026-07-30 baseline, 59 on this branch; sibling lanes may add or archive in-scope files. |
| `measured_at_sha` | `<INTEGRATOR-SETS-THIS>` | Deliberately a placeholder, not the stale `3cd4417a`. Leaving the July sha beside `445` would claim the new number was measured at the old commit. **Inert to the gate** — `check_silent_rule_ratchet` reads only `detector_id` and `baseline` — so it cannot cause a silent wrong pass, and it is unmissable on sight. |

**My arithmetic, so the integrator can show its own against it.** Both numbers are reproducible
from the tree:

```
git show aeec0fd1:protocols/PLAYBOOK.md | grep -oiE '\b(must|shall|never)\b' | wc -l   -> 210
git show HEAD:protocols/PLAYBOOK.md     | grep -oiE '\b(must|shall|never)\b' | wc -l   -> 214
python scripts/silent_rule_detector.py                       -> detector silent-rule-v4, 59 files, 445
```

All three re-run clean at this branch's tip. **447** was the *first* reading, before the two
descriptive false positives were drained; **445** is the figure after that drain and is what the
branch carries now — so the pre-drain number is recorded here as history and is deliberately not
the one in the command block, which has to reproduce. The `+4` in the gate's own FAIL message
(`live 445 > baseline 441 (+4)`) is the independent confirmation of the same arithmetic.

**Operator's finding, recorded because it is a ruling on conduct and not just on a number:**
the `never` -> `not` swap was available and was declined, because it lowers the metric without
removing a rule — the inverse of the detector's own v1->v2 occurrence-counting correction.
R8 rules that declining it was correct at the exact point where gaming was available.

**Until that ruling lands, every commit on this branch carries a declared
`SKIP=audit-health` with the reason in its body** (PLAYBOOK Ch8 Q1 — a lane declares its
single-hook bypass in the commit body). No `--no-verify` was used anywhere in this lane, and no
other hook was skipped: the bypass is one hook, on a lane branch, for one named and measured
cause. **The integrator cannot merge this branch to `main` without the ruling** — main would then
sit above its own baseline and every subsequent commit in the repo would red.

### R1 — `templates/prompt-template.md` is now owed an update, and its predecessor said so

The v1.14 card still shows the hand-composed form
`claude --bg --model opus --effort high --permission-mode bypassPermissions "[…] Read and execute
the frozen contract at $env:CLAUDE_PROMPTS_DIR\<FILE>.md"`. The predecessor lane
(`docs/audits/2026-08-21-technical-ch8-dispatch-codification.md`, open items) named the trigger
precisely: *"If `Dispatch-Lane` becomes the stated surface, the card is the point-of-use copy that
would follow — not this lane's file."* **This lane is that trigger.** It is outside this lane's
footprint (Ch8 + the generator), so it is filed rather than swept — and note that
`templates/**` is **inside** the silent-rule detector's scope roots, so whoever takes it inherits
R0's arithmetic.

### R2 — carrier row specification (A3: `banked = 0`, so a spec, not a file)

No file was written to `tasks/`. The row this work would carry, for the architect to queue:

```
id:        <next free>
title:     Dispatch codification — Ch8 states the three shapes; gen_lane_contract emits them
theme:     Methodology / session boundaries
size:      S
status:    done-pending-ruling
evidence:  959b80a1 (Ch8) · df9ce8a8 (tests) · 74cfa2f0 (generator)
blocked-by: the R0 operator ruling on ecosystem/silent-rule-baseline.yaml 441 -> 445
notes:     closes G1/G6/G7 of docs/audits/2026-08-20-technical-playbook-status.md;
           G7 lands with a correction to that row's own premise (short effort forms ARE
           mapped by the helper, and are ignored only by the raw CLI).
```

### R3 — `--expect-shape` is reachable but unwired

The `check` command grew `--expect-shape`, and the `lane-contract-check` hook does not pass it —
correctly, since at commit time nothing outside a contract states its intended shape. It is there
for a caller that *does* know: a batch manifest that declares each lane's substrate could assert
it per row. No such caller exists today, and none was invented here.

### R4 — decided per contract defaults, reported rather than asked

- **`--cloud/--local` was replaced by `--shape`, not kept beside it.** Two flags meaning the same
  thing is the second-source-free-to-disagree class this generator exists to remove. Verified by
  grep that the only caller was this module's own test file.
- **`**Shape:**` is a mandatory field**, so a contract that does not declare its shape is refused.
  Verified safe first: `git ls-files` matches **zero** files against the hook's `LANE-*.md` glob,
  so nothing committed is affected, and every contract emitted from now on carries it.
- **The interactive shape cites `<PROMPTS_DIR>`, not a literal `C:\Users\…\Downloads`**, following
  Ch8's existing rule that a dispatch line stays portable and keeps one operator's directory
  layout out of an artifact other people read. The operator's cheat-sheet showed the absolute
  path; the ruled form won, and the emitted prose says plainly that he resolves the token by eye
  because a chat message is not a shell.

---

## 7. Suite — measured against the A2 baseline, and NOT reported green

`uv run --locked --group analytics python -m pytest`, unpiped, 36m34s wall on a workstation
carrying six concurrent lanes.

```
A2 baseline (contract):   1 failed, 3567 passed,  4 skipped, 1 xfailed  = 3573
this branch:              6 failed, 3592 passed,  9 skipped, 1 xfailed  = 3608
delta:                   +5 failed,   +25 passed, +5 skipped            =  +35
```

**"Suite green" would be false, and so would "suite matches baseline".** Both are stated
plainly rather than rounded, and every one of the five additional REDs is named and attributed
below.

### 7.1 The +35 test delta is this lane's own tests, proven rather than asserted

`tests/test_gen_lane_contract.py` is the only test file this lane touched. Collected at the merge
base and at HEAD:

```
git show aeec0fd1:tests/test_gen_lane_contract.py -> 70 tests collected
HEAD tests/test_gen_lane_contract.py             -> 105 tests collected
```

**105 − 70 = 35 = 3608 − 3573.** The arithmetic closes exactly, so no other test moved.

### 7.2 All six REDs, attributed

| # | Test | Attribution |
|---|---|---|
| 1 | `test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent` | **The A2 baseline failure.** Pre-existing on `main` since 2026-08-22; the contract names it by name. |
| 2 | `test_silent_rule_ratchet.py::test_committed_baseline_matches_live_measurement` | **MINE — R0.** `live 445 exceeds committed baseline 441`. |
| 3 | `test_silent_rule_ratchet.py::test_check_registered_and_green_on_live_repo` | **MINE — R0**, same cause: `assert 'fail' == 'pass'`. |
| 4 | `test_audit.py::test_health_ok_with_registered_repo` | **MINE — R0**, same cause. `audit.py health` exits 1; the blocking finding in its own captured output is `[!!] silent_rule_ratchet: silent-rule pool GREW: live 445 > baseline 441 (+4)`, and it is the only `[!!]` present. |
| 5 | `test_audit.py::test_health_stays_ok_with_na_status` | **MINE — R0**, same cause, same captured finding. |
| 6 | `test_stale_worktrees.py::test_linked_worktrees_reader_excludes_the_primary` | **ENVIRONMENTAL — running the suite from inside a worktree.** Not this lane's diff. |

**Four of the five additional REDs are ONE cause.** #2–#5 are the silent-rule ratchet reporting
`+4` — the same measurement §R0 documents, reached through four different assertions. They go
green the moment the operator rules the raise 441 → 445, with no code change. This is the
mechanical consequence of the lane being told to codify normative doctrine into a `protocols/`
file while `main` sits exactly at its own baseline.

**#6 is environmental and provable from its own assertion message.** The test asserts
`aud._REPO_ROOT` is not among `_git_linked_worktrees(...)`; run from a worktree, `_REPO_ROOT`
**is** a linked worktree, so it fails by construction. Its message names the neighbours it found —
`dashboard-commit-path`, `rulings-landing`, `status-grammar` — which are sibling lanes of this
batch, not anything this lane created. The `+5 skipped` has the same origin: worktree-guarded
tests skip when the suite is not run from the primary checkout. **The integrator should re-run
this test from the primary checkout before treating it as a finding** — this lane cannot, because
it is commit-and-STOP inside the worktree that causes it.

**Net, after attribution:** this lane introduces **zero** REDs of its own logic. Four are one
queued operator ruling, one is the declared baseline failure, one is the measurement environment.
`tests/test_gen_lane_contract.py` is 105/105 green in isolation, and 8/8 mutants die against it.

---

## 8. Operator rulings received after the lane's first STOP (2026-08-23)

Recorded here because they change what a later reader should believe about sections 5–7, and
because two of them correct **the contract and the baseline**, not this lane's work.

### R8 — the baseline raise: APPROVED on the merits, SHIPPED not applied

Full treatment at §R0a above, including the ready-to-apply fenced diff. In one line: the raise
441 → 445 is approved, `ecosystem/silent-rule-baseline.yaml` is **not written by this lane**, and
the integrator re-measures after the last merge because **445 is N-dependent** — sibling lanes are
sweeping `protocols/`, which is inside the detector's scope roots.

### R9 — the JOURNAL entry: P-1 governs, and the contract's Final step 3 was wrong

**The conflict flagged in the JOURNAL entry's opening block is resolved by the operator against
the contract.** `protocols/STANDING_RULINGS.md` P-1 — *a batch lane never journals; the integrator
does* — governs. The frozen contract's Final step 3 (*"`JOURNAL.md` entry on this branch"*) was an
authoring error.

**Nothing is deleted.** `JOURNAL.md` is append-only (CLAUDE.md §5 rule 2), so the entry **stays as
written**, conflict flag and all, and the **integrator appends one correction note**. That is the
whole remedy; this lane takes no action on it.

Worth recording as the reason the flag was written rather than the flag being noise: the entry
opened by naming the P-1 conflict instead of silently obeying the contract, and the operator's
ruling says that flag is what surfaced the error. **A lane that had quietly complied would have
buried it** — the entry would have looked correct and P-1 would have been breached without a
trace. This is the Q10 posture applied to an instruction rather than a premise: comply, disclose,
let the ruling come back.

### R10 — the suite report accepted in full, and the A2 baseline itself corrected

The operator accepts §7 as written and **corrects the contract's own A2 baseline**: it was
measured in the **primary tree** and was therefore wrong for worktree lanes.

```
A2 as written in the contract:   1 failed  (primary-tree measurement)
A2 as corrected by R10:          2 failed  (correct for a lane running from a linked worktree)
```

`test_stale_worktrees.py::test_linked_worktrees_reader_excludes_the_primary` **fails by
construction** from inside a linked worktree — independently reproduced by **LANE-L6**, which
detached to bare `main` inside its own worktree and saw the same thing. So it was never a finding
against any lane's diff; it was a property of where the suite runs.

**Restated against the corrected baseline, this lane's numbers close even more cleanly:**

| | corrected A2 | this branch | delta |
|---|---|---|---|
| failed | 2 | 6 | **+4 — all one cause (the R8 ratchet), zero from this lane's logic** |
| passed | 3567 | 3592 | +25 |
| skipped | 4 | 9 | +5 (worktree-guarded tests) |
| total | 3573 | 3608 | **+35 = 105 − 70, this lane's own tests** |

The operator additionally names the `105 − 70 = 35 = 3608 − 3573` collection proof as the
standard expected from every lane. It is cheap to reproduce and is recorded at §7.1 with the two
commands that produce it.

**Net after R10:** the five "additional REDs" of §7 are more precisely **four**, and all four are
the single queued ratchet cause that goes green when R8's diff is applied by the integrator.
