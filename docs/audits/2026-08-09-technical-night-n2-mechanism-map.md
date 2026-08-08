# NIGHT LANE N2 — the 2026-08-08 architect defects, mapped to mechanisms

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-09 · **Slug:** night-n2-mechanism-map
- **Batch:** the 2026-08-09 night batch, manifest `docs/audits/2026-08-09-technical-batch-night-manifest.md` (`batch: 0`, open)
- **Runtime:** CLOUD (Anthropic cloud session), branch `claude/manifest-filename-parser-validation-v4n1ew`, base `origin/main` at `319f885d`
- **Mode:** execute — the dispatch contract was the plan. Model opus, effort xhigh.
- **Contract:** the N2 lane contract as pasted, **plus DEFECT 7 added by the architect after the contract was frozen.** Defect 7 is mapped as a peer of the six, in §1.7, and carries the extra analysis the addendum asked for (the "name it through the generator" question, §1.7d).
- **Standing rule honoured:** read-mostly, no merges. This branch is pushed and merged by nobody but the operator.

> **This file's own name was verified against every parser that consumes `docs/audits/`
> before it was written**, because that is the defect this lane is mapping and it would be
> absurd to reproduce it in the report. Evidence:
>
> ```
> candidate: docs/audits/2026-08-09-technical-night-n2-mechanism-map.md
>  ADR-101 Rule A+B (validate_hermetization): PASS
>  MANIFEST_GLOB match (must be False — not a manifest): False
>  gen_audit_index._DATE_RE: True  -> ('2026-08-09', 'technical-night-n2-mechanism-map')
> ```
>
> The middle line is the one that matters and is the one nobody runs: an artifact must be
> checked against the globs it *must not* match as well as the ones it must.

---

## 0. Verdict board

| # | Defect | Existing organ | Verdict | Smallest fix |
|---|---|---|---|---|
| 1 | Batch 3 dispatched with no manifest | none at dispatch (`batch_manifest` reads, never demands) | **BUILD** | dispatch-time refusal, ~30 lines |
| 2 | Frozen contract asserted false repo state | none | **DO NOT BUILD `contract-lint`** — §1.2 | strengthen `/preflight` adoption, 0 lines |
| 3 | 9/10 lane branches off-enum; two rival regexes | `validate_branch_naming.py` (correct, unrun) | **RECONCILE + BUILD** | import, don't restate: ~10 lines |
| 4 | Worktree provisioning hand-written | `/lane-boot` (exists, unused) | folds into #1 | — |
| 5 | Integration hand-written | `/lane-integrate` (exists, unused) | folds into #1 | — |
| 6 | Acceptance froze "exactly N files" + a non-viable literal | none | **DO NOT BUILD** — §1.6 | contract prose rule |
| **7** | **Manifest filename invisible to its own consumer's glob** | `validate_hermetization` Rule B — checks the *tree's* grammar, blind to the *consumer's* | **BUILD — the highest-ratio item in this report** | **Rule C: ~45 lines, §1.7c** |
| 8 | Lane contracts not recoverable from the repo | none; `[#505]` leg 1, missed twice | **BUILD** (cheap leg only) | manifest `contracts:` block |
| 9 | n=5 unattributed HEAD swaps | none | **INSTRUMENT, do not fix** | reflog attribution probe |

**The three I would build first: #7, #3, #1.** Reasoning in §5. Two of my own proposals
(`contract-lint`, the artifact generator) I argue against building, in §1.2 and §1.7d.

---

## 1. The seven defects

Each carries: what happened · measured cost · the organ that should have prevented it · the
proposed mechanism · library-first check · the smallest version that would have caught it.

### 1.1 Batch 3 dispatched with no committed manifest

**What happened.** Batch 3 was dispatched without committing a batch manifest. The ADR-110
declared-integration-arc exemption requires *both* a `worktree-lane-*` `--no-ff` merge *and* a
committed manifest declaring an open batch (`scripts/batch_manifest.py:12-19`). With no
manifest, `open_batches()` returns `[]`, no merge is exempt, and each lane merge lands an
unanchored first-parent spine entry that `audit-health` (`always_run: true`) evaluates
per-commit. The merge queue is mechanically unrunnable.

**Measured cost.** A **2h12m** integrator run that reached the precondition gate and
**STOPPED before merge #1** — "Zero merges, zero teardown, zero row closes"
(`docs/audits/2026-08-08-technical-batch-3-consolidation-report.md:6-7`;
`docs/audits/2026-08-09-technical-batch-night-manifest.md:18-20`). To the integrator's
credit it stopped rather than reaching for `SKIP=audit-health` or `--no-verify` — the cost
was paid honestly and is therefore measurable.

**The organ that should have prevented it.** There is none, and the asymmetry is the whole
finding: `batch_manifest.py` is a **reader**. It answers "is a batch open?" for
`audit.py:3881`, `gen_handoff.py:412` and the exemption. Nothing anywhere **demands** a
manifest before lanes are dispatched. Ch8 requires it in prose; prose is not an organ.
`/lane-boot` boots one lane and never asks whether a batch is open.

**Proposed mechanism — `/batch-open`, and a refusal in `/lane-boot` §1.** Two halves:

1. `scripts/batch_open.py --check` — a read-only predicate reusing `batch_manifest.open_batches()`
   verbatim. Exit 1 with the Ch8 pointer when zero batches are open.
2. `/lane-boot` §1 pre-flight gains it as a **first** step, before `validate_branch_naming`.
   A lane cannot boot into a batch that does not exist.

The stronger form the contract hints at — "makes a lane prompt **unemittable** while no batch
is open" — is not reachable from Layer 2. Prompt emission happens in the browser seat and in
`Invoke-Dispatch.ps1` (win-tooling, cross-repo, already `[#509]`). What *is* reachable is
making the lane refuse to **start**, which costs one lane-boot instead of a 2h12m integrator
run. Take the reachable version; do not wait for the unreachable one.

**Library-first check.** Stdlib wins outright: the predicate already exists in-repo and is
tested (`tests/test_batch_manifest.py`). This is **reuse, not adoption** — the same verdict
`docs/audits/2026-08-08-technical-library-research.md` §4 reached for the `GIT_DIR` scrub.
No candidate library knows what an ADR-110 batch is.

**Smallest version that would have caught it.** Three lines in `/lane-boot` §1:

```bash
uv run --locked python -c "import sys;sys.path.insert(0,'scripts');import batch_manifest as b,pathlib;\
sys.exit(0 if b.open_batches(pathlib.Path('.')) else 1)" || echo "NO OPEN BATCH — commit the manifest first (Ch8)"
```

Ten lanes each print that line; ten lanes each refuse. Cost: minutes, not 2h12m.

### 1.2 A frozen contract asserted a repo state that was false

**What happened.** The batch-3 dispatch contract opened with *"`journal_spine_anchor` is
hard-RED on `ae339ace` … it also RED-blocks `audit-health` at pre-commit and causes 2 of the 4
current suite failures"* (`…batch-3-consolidation-report.md:191-193`). None of it was true at
dispatch time. The shared predicate `journal_anchor.unanchored_on_spine(main, floor)` returns
**`[]`** — zero unanchored entries (report:199-200). `ae339ace` **is** anchored: it introduced
`8f09c12d`, which the 2026-08-08 (e) JOURNAL entry names (report:202-204). The architect
carried a lane's **earlier** report forward as **present** fact.

**Measured cost.** Bounded and small: the lane that received it re-derived live state and the
false premise was corrected in-flight. The cost is a re-derivation round-trip per lane
receiving a stale claim, times N lanes — real but not the 2h12m class. **I record it as the
cheapest of the six**, which matters for the ranking.

**The organ that should have prevented it.** `/preflight` exists and is exactly this tool —
"Verify every repo locator a contract or prompt cites — file:line, headings, SHAs, [#id]
liveness — BEFORE acting on it. Read-only, adoption-first, **wired into no gate**"
(`.claude/generated/commands-repo.md`). Same shape as defects 3/4/5: **the organ existed and
was not invoked.**

**Proposed mechanism — and I argue against the contract's own candidate.** The contract
proposes "contracts must cite live state with a timestamp/SHA, and a `contract-lint` that
fails any state claim lacking one." **Do not build `contract-lint`.** Three reasons:

1. **It cannot tell a state claim from prose.** "`journal_spine_anchor` is hard-RED on
   `ae339ace`" is a state claim; "the gate can go RED here" is not. Distinguishing them is NLP
   over free text, and a linter that guesses will either miss the real ones or cry wolf on
   every sentence containing a SHA. This repo has a named precedent for refusing exactly this:
   `_REVIEW_TITLE_RE`'s docstring records that field-presence alone was measured to be a bad
   discriminator (13 tracked non-review docs carry `**Branch:**`), so a canonical *title* was
   required instead (`scripts/audit.py:4001-4005`).
2. **A SHA-stamped claim is still a false claim.** The batch-3 contract *named a SHA*
   (`ae339ace`). Stamping is not verification. A linter enforcing stamps would have passed
   this contract unchanged.
3. **The dispatch contract is not a repo artifact** (see §1.8 / defect 8). Linting a file that
   lives in `~/Downloads` and is never committed requires solving the artifact problem first.

**What to build instead — nothing new.** Make `/preflight` a **named step in the contract
template**, not an available command. `templates/prompt-template.md` gains a mandatory
opening beat: *"Run `/preflight` against every state claim in §Premises before acting. Report
each as CONFIRMED / REFUTED with the live command output."* That converts a stale premise from
an invisible inheritance into a visible REFUTED row in the lane's first output — which is
exactly what happened here by luck, made routine by construction. Zero code.

**Library-first check.** Nothing to check: the recommendation is to build nothing.

**Smallest version that would have caught it.** One line in the contract template. The lane
would have printed `REFUTED — unanchored_on_spine() == []` in its first minute.

### 1.3 Nine of ten hub lane branches violated the ratified enum — and two rival regexes ship in one repo

**What happened.** `validate_branch_naming.LANE_BRANCH_RE` requires
`^worktree-lane-[a-z]-\d+-<slug>$` (`scripts/validate_branch_naming.py:85`). Of batch 3's ten
lanes, **only `lane-c-393-rot` passes**. Nine fail: `lane-290-floor-teeth`,
`lane-e-gitenv-scrub`, `lane-intakes-28-29`, `lane-280-315-carriers`, `lane-506-groom-sheet`,
`lane-archival-audit`, `lane-502-pythonpath-measure`, `lane-seeded-defect-substrate`,
`lane-wave-closures` (`…consolidation-report.md:246-249`). **Every satellite lane the same day
conformed**, because a validator was invoked there — so this is a hub-side dispatch-discipline
gap, not a broken validator (report:250-251).

**F4, the sharper half.** Two definitions of "a lane branch" ship in the same repo:

| site | regex | admits |
|---|---|---|
| `scripts/validate_branch_naming.py:85` | `^worktree-lane-[a-z]-\d+-<slug>$` | **strict** — letter, id, slug |
| `scripts/batch_manifest.py:91` | `^worktree-lane-[a-z0-9]+(?:-[a-z0-9]+)*$` | **loose** — any kebab tail |

All ten batch-3 branches match the loose one; nine fail the strict one. `journal_anchor.py`'s
own docstring states the standard being broken: *"A second definition is a drift edge, not a
convenience."*

**The trap the contract correctly flags.** Tightening `batch_manifest.LANE_BRANCH_RE` naively
to match the strict one **would have made nine of ten merges non-exempt** — turning a naming
lint into a merge-queue outage. The loose regex is currently load-bearing *because* the enum
is unenforced.

**Proposed reconciliation, both regexes named.** Sequenced, and the order is the whole point:

1. **First, enforce at provisioning** (below). Nothing is tightened yet.
2. **Then, after one batch provisions clean**, delete `batch_manifest.LANE_BRANCH_RE` and
   import `validate_branch_naming.LANE_BRANCH_RE` — one definition, the strict one.
3. `batch_manifest`'s containment property is preserved: `validate_branch_naming` is a
   stdlib-only leaf, so the import adds no edge reaching the pre-push organ. **This must be
   asserted, not assumed** — `tests/test_batch_manifest.py` already asserts non-import of the
   pre-push organ on the AST; extend that assertion rather than adding a comment.

Step 2 before step 1 is the outage. Step 1 before step 2 costs one batch of latency and
nothing else.

**Enforcement at provisioning.** The gap is precisely that `/lane-boot` §1 *asks* the operator
to run the validator "and that is the whole enforcement" (report:250). The fix is that a lane
branch cannot be *committed to* while off-enum: a **pre-commit** leg (not pre-push — pre-push
is too late, the worktree already exists and the work is already done) that classifies
`git branch --show-current` and BLOCKs on `KIND_UNKNOWN` when the name starts `worktree-lane-`.
Scoped to that prefix so it touches no other branch class.

**Library-first check.** The classifier exists, is typed (`Classification`), enumerates kinds,
and is tested (`tests/test_validate_branch_naming.py`). **Reuse.** No library models this
repo's lane grammar; hand-rolled already won this argument when the validator was written.

**Smallest version that would have caught it.** `/lane-boot` §1 already prints the command.
Making it a **hook** rather than an instruction is ~15 lines against an existing classifier.
Nine of ten lanes would have refused to boot and been renamed in seconds.

### 1.4 Worktree provisioning was hand-written instead of `/lane-boot`

**What happened.** Provisioning was hand-written. The command exists, carries the enum check
(§1), the seed plan (§3) and the contract freeze (§4). Hand-writing it skipped all three —
which *is* defect 3's proximate cause, and is why I fold this into #1 rather than propose a
separate organ.

**The live premise correction.** The contract asserted that `worktree_seed --plan` prints only
the SEED half. `.claude/commands/lane-boot.md:52-59` states the opposite in the file the
architect would have read: *"It prints two things, because provisioning has two halves and
only the first used to be written down (`[#429]`)"* — untracked files to copy **and** the
per-checkout environment. The lane corrected this live. This is defect 2's shape again (a
carried-forward stale premise) and it is *self-correcting by invocation*: running the tool
prints the truth. **A stale premise about a tool is cured by running the tool** — which is the
one-line argument for every mechanism in this report.

**Measured cost.** Not separately measurable; it is the delivery vehicle for defect 3's nine
off-enum branches and for the seeding gaps.

**Proposed mechanism.** None new. Defect 3's provisioning-time refusal makes the hand-written
path fail where the command path passes, which is the only durable way to make a command
non-optional without a Layer-2 violation. **Prefer extending an existing organ** — the
Discipline section's rule — and here the extension is defect 3's.

**Library-first check.** N/A (no new mechanism).

**Smallest version.** Same as §1.3.

### 1.5 Integration was hand-written instead of `/lane-integrate`

**What happened.** Same class, at the other end. `/lane-integrate` carries the five-item
refuse-to-finish checklist mechanically (`…batch-3-manifest.md:155-159`): every lane branch
merged-or-abandoned · full suite once on the merged result · `git worktree list` == primary
only · manifest **and** packet archived · `git stash list` empty. Hand-written integration
executes the merges and skips the checklist.

**Measured cost.** Batch 3's integrator **stopped** at the precondition gate, so the checklist
was never reached — the cost here is masked by defect 1 and is not independently measurable
this batch. I decline to invent a figure. Batch 2's packet is the better evidence that the
checklist matters.

**The organ that should have prevented it.** `/lane-integrate` exists. Nothing requires it.

**Proposed mechanism — the one genuinely new leg worth considering here.** Item 4 of the
checklist ("manifest **and** packet archived") is *already mechanical and already free*: the
manifest names `closed_by:`, and the batch is open until that path is committed. So a batch
that ends without a packet is **already** detectable — `open_batches()` returns it forever.
The missing organ is not a checker, it is a **surfacer**: `audit.py` already prints
"batch N is open" (`audit.py:3881,3888`), but nothing escalates on **staleness**. Add: an
open batch whose manifest is older than the newest commit by more than one day WARNs. That
converts "the batch never formally closed" from invisible to a daily nag, using state that
already exists.

**Library-first check.** Reuse of `open_batches()` + git timestamps. Stdlib. No adoption.

**Smallest version that would have caught it.** ~12 lines added to the existing
`audit.py` open-batch reporting. It does not force `/lane-integrate`; it makes skipping its
item 4 visible.

### 1.6 Acceptance criteria froze "exactly N files" and a structurally non-viable literal

**What happened.** Two sub-defects with one root.

*(a) "exactly N files."* Hooks mandate regenerated companions: `audit-index-freshness`
(`docs/audits/README.md`), `intake-index-freshness` (`docs/intake/README.md`),
`gen_intake_tree.py` (`docs/intake/manifest.json`), `gen_doc_counts` (`ecosystem/doc-counts.md`),
`claude-rosters-freshness`, `roster-freshness`. A lane adding one audit file **cannot** produce
exactly one file — the gate blocks the commit until the index is regenerated. An acceptance
criterion of "exactly N files" is unsatisfiable by construction and puts the lane in a bind
between its contract and its gate.

*(b) `pythonpath = ["."]`.* The contract froze this literal. Measured:
**67 of 99 test files fail to collect** under it, because `scripts/` and `deploy/` are not
packages and tests import bare module names. Any viable adoption is
`[".", "scripts", "deploy"]` (`docs/audits/2026-08-08-technical-502-pythonpath-measurement.md:201-204`,
arm table :103-105). *"The `["."]` figure is the measurement of a spelling, not of the shape."*

**Measured cost.** Sub-defect (b) is the expensive one and it is fully measured — a full
three-arm measurement lane (baseline 789.04s, arm 1 427.36s, arm 2 615.27s) that ended in
"three shapes costed, **no pick**" (library-research §5:369). Note this cost was **not wasted**
— the lane produced a real measurement. The defect is that it measured a spelling the
architect had already frozen as the answer.

**The organ that should have prevented it.** None. And I will say plainly: **there should not
be one.** A contract freezing a wrong literal is a *reasoning* error, and the class of tool
that catches it is a tool that runs the experiment — which is what the lane is for.

**Proposed mechanism — a contract-prose rule, not code.**

1. **Acceptance criteria name a property, never a file count.** "The audit index regenerates
   clean" not "exactly 1 file." A count is a claim about the *gate set*, which the architect
   does not hold in memory (that is the whole premise of this lane) and which the hooks change
   underneath any frozen number.
2. **A frozen literal is a hypothesis, and the contract says so.** `pythonpath = ["."]` should
   have read *"candidate spelling `["."]` — the lane may report a different viable spelling;
   measuring the shape is the deliverable, adopting the literal is not."*

Both belong in `templates/prompt-template.md`, beside §1.2's `/preflight` beat.

**Library-first check.** N/A — recommendation is prose, no code. Explicitly: I considered and
reject a "companion-file predictor" that computes the regenerated set from
`.pre-commit-config.yaml` and injects the true N into contracts. It is real code (~80 lines,
parsing hook config), it serves one prose sentence, and it institutionalises the file-count
habit this section argues against.

**Smallest version that would have caught it.** Sub-defect (a): one template sentence.
Sub-defect (b): the word "candidate" instead of a frozen `=`.

---

### 1.7 DEFECT 7 — a manifest filename invisible to the parser that consumes it

*Added by the architect after the contract was frozen; mapped here as a peer of the six, with
the extra analysis the addendum asked for.*

#### 1.7a What happened, verified

The dispatch contract specified `…-technical-night-batch-manifest.md`. That name is
**invisible** to `batch_manifest.MANIFEST_GLOB = "docs/audits/*-batch-*-manifest.md"`
(`scripts/batch_manifest.py:87`), matched with `PurePosixPath.match`. Re-verified in this
lane, independently of the executing session's claim:

```
pattern:       *-batch-*-manifest.md
fnmatch regex: (?s:(?>.*?\-batch\-).*\-manifest\.md)\Z

  INVISIBLE  2026-08-09-technical-night-batch-manifest.md   <- the architect's spelling
  MATCH      2026-08-09-technical-batch-night-manifest.md   <- what shipped
  MATCH      2026-08-08-technical-batch-3-manifest.md
  MATCH      2026-08-07-technical-batch-2-manifest.md
  INVISIBLE  2026-08-09-technical-batch-manifest.md         <- the degenerate name also fails
```

The mechanism: after the only `-batch-` the remainder is `manifest.md`, and the pattern still
requires `*-manifest.md` — a literal hyphen that is no longer available. Nothing remains
between `batch-` and `-manifest.md` to satisfy the second wildcard.

**The consequence had it shipped.** `_committed_manifests()` filters on this pattern
(`batch_manifest.py:178-180`), so `open_batches()` returns `[]`, no ADR-110 exemption exists,
and the night batch would have **reproduced batch 3's 2h12m failure while looking like its
repair.** The executing session verified both spellings before writing and swapped two tokens
— the smallest edit that makes the parser see the file
(`docs/audits/2026-08-09-technical-batch-night-manifest.md:44-58`).

**Measured cost this time: ~zero.** The defect was caught at authoring time by a session that
chose to check. That is precisely why it belongs in this report: **the cost was zero because
of individual diligence, not because of a mechanism.** The counterfactual is batch 3's 2h12m,
and it recurs the first night nobody checks.

#### 1.7b The organ that should have prevented it — and the exact shape of the gap

**`validate_hermetization.py` Rule B is the right organ, standing in the right place, checking
the wrong grammar.** It is a pre-commit hook, prospective-only on staged ADDs, that BLOCKs an
off-grammar `docs/audits/*.md` name (`scripts/validate_hermetization.py:153-196`). It fires at
**authoring time**, which is exactly what the addendum asks for.

Run against both spellings:

```
docs/audits/2026-08-09-technical-night-batch-manifest.md -> PASSES Rule A+B
docs/audits/2026-08-09-technical-batch-night-manifest.md -> PASSES Rule A+B
```

**Both pass.** Rule B validates `<YYYY-MM-DD>-<class>[-<slug>]` — date shape, closed 11-class
enum, R4 casing, well-formed slug. Both names carry class `technical` and a lowercase-kebab
slug. Rule B is *correct*; it enforces **ADR-101's tree grammar**. It has no knowledge of, and
no edge to, the **consumer grammar** that decides whether the file is functionally a manifest.

**The gap named precisely: the repo validates that a filename is well-formed for the tree, and
never that it is well-formed for its reader.** Two grammars govern one name; one is gated and
one is not.

And the third instance shows the same gap at field level: `_valid_closer()` shape-checks
`closed_by` rigorously (`batch_manifest.py:133-147`) while `batch` is read raw at line 228
(`fm.get("batch", "?")`) — the field whose well-formedness the suite pins.

#### 1.7c The three instances are one defect class

| # | artifact | authored from | consumed by | outcome |
|---|---|---|---|---|
| A | `…-night-batch-manifest.md` | prose intent | `MANIFEST_GLOB` (`batch_manifest.py:87`) | would have granted **no** exemption |
| B | `# Codex review …` (lowercase) | prose intent | `_REVIEW_TITLE_RE = ^# Codex Review\b` (`audit.py:4005`) | review ran, satisfied **no** gate |
| C | `batch: 2026-08-08-batch-3` | the batch's human name | `b.batch.isdigit()` (`tests/test_batch_manifest.py`) | working exemption, **RED** suite |

**The invariant they share, and it is the dangerous part:** in all three the artifact *reads
correctly to a human* and is *wrong to the machine*, and in B and C **the mechanism still
appeared to work.** The batch-3 manifest's own amendment states it exactly: *"the malformed
field granted a working exemption while failing the repo's own well-formedness pin. A defect
that leaves the mechanism functional is the kind that survives a batch and is inherited by the
next one"* (`…batch-3-manifest.md:179-182`). Instance B is worse — a review that ran, reached a
verdict, and satisfied no coverage leg (`docs/audits/2026-08-09-codex-batch-3-integrator-arc.md:17-21`).

**The recovery cost is asymmetric and this is what makes the class expensive.**
`docs/audits/` is immutable (CLAUDE.md §5 rule 3), so a wrong name or field is not a one-line
fix:

- Instance B was repaired by **superseding with a new file** — the sanctioned option worked
  because the broken file, failing the title regex, is inert rather than competing.
- Instance C **could not** be superseded: two manifests would both match `MANIFEST_GLOB`, both
  be open, and the test iterates *all* live open manifests. Nor could an in-file amendment
  marker help — `_frontmatter()` parses only the first `---` block, so a body correction is
  read by humans and ignored by the machine. It was repaired by **editing an immutable file
  in place**, recorded as a deliberate deviation from rule 3
  (`…batch-3-manifest.md:184-196`).

So the class does not merely cost a defect; **it costs either a superseding artifact or a
knowing violation of the repo's immutability rule.** An authoring-time refusal is worth
disproportionately more here than in a tree where a rename is free.

#### 1.7d Does "name it through the generator, never by hand" subsume all three?

**No — and the evidence against it is in the repo, twice over.**

**First, the generator does not exist.** Retrieval across `scripts/gen_*.py` returns: *no
generator writes any new file under `docs/audits/`.* `gen_audit_index.py` writes
`docs/audits/README.md` (the index) and reads everything else; `gen_task_tree.py` writes
`tasks/`; `gen_handoff.py` writes `docs/handoffs/`. So "name it through the generator" is not
an adoption of an existing path — it is **a new script, a new command, a new template set, and
a new freshness surface**, proposed to prevent a class whose measured cost so far is one
avoided error.

**Second, and decisively: a template that already existed did not prevent instance B.**
`protocols/PLAYBOOK.md:3476` carries the literal line:

```
# Codex Review — {topic}
```

The template was correct, present, and canonical. The artifact was authored from prose intent
anyway, in lowercase, and was invisible to `audit.py:4005`. **This is a measured negative
result for the generator-as-prevention hypothesis, in this repo, on one of the three instances
the hypothesis claims to subsume.** A generator prevents nothing it is not routed through, and
nothing can route a hand-authored markdown file through a generator except a refusal — at
which point the refusal is doing the work.

**Third, it subsumes the instances unevenly even in principle.** A generator emitting the path
fully subsumes A. It subsumes B only for artifacts it emits (the codex wrapper's output, not a
hand-written supersede). It subsumes C only if `--batch 3` is typed correctly, which is the
same human keystroke that produced `2026-08-08-batch-3`.

**The correct decomposition.** These are two separable mechanisms with very different value:

- **The refusal is the enforcing half.** It catches hand-authoring, which is how all three
  defects actually arrived, and it is an extension of an organ that already runs.
- **The generator is the ergonomic half.** It makes the right name easy. It catches nothing.

**Build the refusal. Do not build the generator** — or rather, do not build it *for this
reason*. If a batch-artifact generator is later justified by ergonomics (see §3, where a
`/batch-open` step is proposed on independent grounds and could reasonably emit the manifest),
it should be justified by the operator keystrokes it saves, never by defect prevention it
cannot deliver.

#### 1.7e The proposed mechanism — Rule C, consumer-glob round-trip

**Extend `validate_hermetization.py` with a Rule C that runs the *live consumer predicate*,
imported from the consuming module rather than restated.**

```python
# scripts/validate_hermetization.py  — Rule C (sketch)
#
# Rule B answers "is this name well-formed for the TREE?" (ADR-101).
# Rule C answers "is this name well-formed for its READER?" — the grammar that
# decides whether the machine can see the file at all.
#
# The predicates are IMPORTED, never restated. A restated glob is a second
# definition, and journal_anchor.py already ruled on that: "A second definition
# is a drift edge, not a convenience."

_CONSUMER_CONTRACTS = (
    # (human intent marker, consumer predicate, what the consumer is)
    ("manifest", _matches_manifest_glob, "batch_manifest.MANIFEST_GLOB"),
)

def rule_c_violation(path: str) -> Optional[str]:
    """An added docs/audits/*.md whose name ANNOUNCES an artifact class its
    consumer cannot enumerate. Silent on names announcing no class."""
    fname = _posix_parts(path)[-1]
    for marker, predicate, consumer in _CONSUMER_CONTRACTS:
        if marker in fname and not predicate(fname):
            return (f"consumer: '{fname}' contains '{marker}' but does not match "
                    f"{consumer}. The file would be INVISIBLE to the organ that "
                    f"reads it — it would declare nothing while looking correct. "
                    f"Rename, or state in the commit body why this is not one.")
    return None
```

**Two design points that carry the whole safety argument:**

1. **The trigger is the human-intent token in the name** (`manifest`), not a guess. A file
   whose author typed "manifest" into the name is asserting it *is* one. If the consumer that
   owns that word cannot see it, that is a contradiction the tree can detect with certainty
   and no NLP — the discrimination problem §1.2 refused to solve for prose does not arise
   here, because the name is a closed, short, machine-readable string.
2. **The predicate is imported, not copied.** `validate_hermetization` gains an import edge to
   `batch_manifest`'s *constant only*. That constant is a module-level string with no git and
   no side effects. The containment property `tests/test_batch_manifest.py` asserts (no import
   path from `batch_manifest` to the pre-push organ) is unaffected because the edge points the
   other way — but it must be **asserted in the test**, not argued in a comment.

**Honest limits, stated rather than discovered later.**

- **It catches announced classes only.** A manifest named `2026-08-09-technical-night-plan.md`
  contains no marker, trips nothing, and is invisible to `MANIFEST_GLOB`. Rule C makes a
  *contradiction* refusable; it cannot make an *omission* refusable, because a file that
  claims nothing cannot be checked against a claim. This is a real gap and I am not going to
  paper over it — it is the price of not guessing.
- **It is one registry entry at first.** Instance B (the heading) is not a filename and does
  not fit Rule C; see below. Instance C (the field) is a frontmatter value and also does not.
  Rule C fixes the *filename* leg only, which is the leg DEFECT 7 is.
- **`_CONSUMER_CONTRACTS` is a growth surface.** A registry with one row is a list; with ten
  it is a config file nobody maintains. Cap it by ruling: a row enters only when a real defect
  of this class has been recorded, exactly as `LANE_PREFIXES` grows only by recorded ruling.

**The other two legs, which are cheaper still and should ride along:**

- **Instance C (field).** `batch_manifest.open_batches()` currently accepts any `batch:` value.
  Add a shape check to `_frontmatter` consumption — mirroring `_valid_closer`'s existing
  discipline — but **keep the current failure direction**: a malformed `batch:` should make the
  manifest open **nothing** (consistent with `_valid_closer`), which converts C from "working
  exemption, RED suite" into "loud refusal at the gate". This is ~6 lines and removes the
  scenario where the artifact is broken and the mechanism looks fine. **Ruling needed** — see
  §6, R2 — because it changes the exemption's failure surface.
- **Instance B (heading).** The codex-review wrapper already emits the canonical title; the
  gap is hand-authored supersedes. A pre-commit leg: an added `docs/audits/*-codex-*.md`
  (class token `codex`, so it announces itself in the name — the same trigger discipline as
  Rule C) whose body does not match `audit._REVIEW_TITLE_RE` BLOCKs. ~15 lines, imported regex,
  same registry.

#### 1.7f Library-first check

Applied strictly, in the order the Discipline section fixes.

| tier | candidate | verdict |
|---|---|---|
| **stdlib** | `fnmatch` / `pathlib.PurePosixPath.match` | **WINS.** The predicate already exists as a constant. Rule C needs an *import edge*, not a dependency — zero new code beyond the glue. |
| established dep | **`pydantic` ≥2** (already declared, ADR-109 `ecosystem/schema/`) | **The right tool for instance C's field leg, in the wrong place.** A `BatchManifestFrontmatter(batch: int, status: Literal["open","closed"], closed_by: str)` model refuses `2026-08-08-batch-3` at parse time and is strictly better than a hand-rolled `isdigit()`. **But it must not enter `batch_manifest.py`**: that module's docstring explicitly refuses a dependency in a gate path (*"taking a yaml dependency into a gate path to read three strings buys nothing"*), and it is reached from `audit-health` at every commit. Pydantic belongs in the **authoring-time** validator, never in the runtime exemption reader. Given that split, the shape check the reader needs is 6 lines and the model is a second definition of the same schema — **so: no.** Revisit only if the frontmatter grows past ~5 fields. |
| established dep | `jsonschema`, `python-frontmatter`, `PyYAML` for the frontmatter | **NO.** New distribution (`jsonschema`, `python-frontmatter`) or a dep the module deliberately avoids (`PyYAML`), to parse three scalars. Same verdict `…library-research.md` §4 reached for dulwich/pygit2/GitPython: *"a new distribution to fix a problem a 25-line helper already fixes."* |
| stabilized project | `validate_hermetization` + `validate_branch_naming` + `journal_anchor` | **WINS as the pattern.** All three already implement "one predicate, one definition, shared by the gate and the backstop" — `block_ff_push` delegates to `validate_no_ff.find_violations`; `check_seal_identity` runs `gen_handoff.verify_seal_identity` *"reused, not reimplemented"*. Rule C is the **fourth instance of a shape this repo has already ratified three times.** That is the strongest argument in this report: it is not a new idea, it is an unapplied one. |
| industry pattern | **consumer-driven contract testing** (Pact and successors) | **Names the class correctly; do not adopt the tooling.** The pattern — *the consumer publishes its acceptance predicate; the producer's CI verifies against it* — is precisely this defect. Pact is HTTP/message-broker machinery for cross-service versioning; here producer and consumer are two files in one repo and "publishing the predicate" is `import`. Adopt the idea, name it in the docstring, take none of the tooling. |
| hand-rolled | Rule C's ~45 lines | **Wins by default**, and the one-line reason is: no library knows what an ADR-110 batch manifest is, and the predicate being enforced is a repo constant that already exists. |

**Also considered and rejected:** a `pre-commit` `check-added-large-files`-style off-the-shelf
filename hook (`check-case-conflict`, `name-tests-test`). They enforce *generic* conventions;
this defect is that a *repo-specific consumer* cannot see a repo-specific artifact. No generic
hook can hold that predicate.

#### 1.7g Smallest version that would have caught it

Not Rule C — **six lines, added to `/lane-boot`'s dispatch-side sibling or run by hand:**

```bash
uv run --locked python -c "
import sys;sys.path.insert(0,'scripts')
from pathlib import PurePosixPath as P; import batch_manifest as b
n=sys.argv[1]; print(('MATCH ' if P(n).match(b.MANIFEST_GLOB.split('/')[-1]) else 'INVISIBLE'), n)
" 2026-08-09-technical-night-batch-manifest.md
```

That is exactly what the executing session ran, by choice. Rule C's contribution is making it
**unskippable** rather than **available** — which, on the evidence of defects 2/3/4/5 (four
organs that existed and were not invoked), is the entire difference between a tool and a
mechanism in this repo.

---

## 2. Handoff & onboarding gap analysis (contract item 7)

### 2.1 What the incoming seat needed on 2026-08-08 and did not have

**Data point 1 — the retrieval payload was a pointer, and the pointer cost a round trip.**
The bundle's `HANDOFF_BOOT.md:9` states the seat's purpose as *"Start from the candidate pool
and the carried-decision list in `docs/audits/2026-08-08-technical-successor-prep.md` (§3 and
§5), which are **retrieval, not a plan** — the cut is this session's."* `RESIDUAL.md:137-140`
repeats it verbatim: *"Sheets, not decisions… They are retrieval — this seat cuts them."*

The bundle is right that the *cut* is the seat's work. It is wrong about what that implies for
transport. **A pointer to retrieval forces a round trip before the seat's actual job can
begin**, and the browser seat has no file access — so the round trip is an operator ferry.
`PASTE_THIS.md` is 51,589 bytes; the candidate pool and carried-decision list are the two
things the seat is being asked to *act on first* and are the two things not in it.

This is a **misapplication of a correct rule.** HANDOFF_PROCESS §2 says the residual carries
*"Pointers (paths) — where the next session reads, not copies of what's there"* and that
re-transmission is *"the v4 disease"*. But §2's target is **methodology and task-state** —
stable surfaces the repo already encodes and that drift when copied. A **candidate pool cut
for this specific session** is neither: it is session-scoped, generated once, consumed once,
and cannot drift because nothing else reads it. Pointering it buys no drift-protection and
costs a ferry.

**Data point 2 — the operator stated the probe ceremony gave him little.** Taken at face value
and reconciled against what the ceremony *is*: v6 already collapsed it from one round trip per
probe to **one** `/handoff-verify` run emitting exactly one evidence block
(`HANDOFF_PROCESS.md:165-207`). So the operator's complaint is not about transport — v6 fixed
that — it is about **yield**. The evidence block's required rows are the five manifest probes,
both orientation reads, inherited claims, P0a/P0b/P0c and P3. Of those, **P3 is the only row
with a mechanical counterpart that can genuinely FAIL** in the ordinary case (it compares the
declared branch against `git branch --show-current`). The bundle's own `HANDOFF_BOOT.md:16-19`
concedes the point about its neighbours: worktree, write-scope and MODE-basis *"stay prose and
deliberately carry no probe leg — a leg with no mechanical counterpart cannot fail honestly,
and one that cannot fail honestly discredits the whole block."*

**The gap, named:** the bundle applies "cannot fail honestly → carry no probe" correctly to
the Destination rows and **not** to the probe manifest itself. A ceremony composed largely of
rows that pass by construction reads as ceremony — which is the operator's report, and it is
accurate.

**Data point 3 (mine, from this batch).** The BOOT DRILL was added at v6.2.0 and its own text
concedes: *"This is prose discipline, not a mechanism: no probe binds it and no gate reads it,
so a seat that skips the drill produces a bundle indistinguishable from one that ran it"*
(`HANDOFF_PROCESS.md:130-133`). On 2026-08-08 the seat emitted ten dispatch lines; nine
carried off-enum lane names (§1.3). **The drill either did not run or ran without the enum
check.** Either way the drill as specified would not have caught it: it asks the operator to
*look* at one sample line, and an off-enum lane name is not visible to a look — it is visible
to `validate_branch_naming.py`.

### 2.2 Proposed bundle content spec

A four-way split, replacing the current three-way (resident / pointer / probed):

| tier | rule | contents |
|---|---|---|
| **RESIDENT** | session-scoped, generated once, consumed once, cannot drift | the candidate pool · the carried-decision list · live target rows for every `[#id]` the purpose names · the open-batch state |
| **POINTER** | stable repo surface that would drift if copied | methodology, PLAYBOOK chapters, ADRs, BACKLOG task state, runbooks |
| **PROBED** | a claim with a mechanical counterpart that can FAIL | P3 branch · HEAD/tree-clean · inherited claims naming a SHA · **open-batch predicate** (new) |
| **DRILLED** | a claim the seat must *execute* to inherit, not read | **the dispatch line, run through `validate_branch_naming.py`** (new) |

The last row is the substantive change and it is DEFECT 7's lesson applied to onboarding:
**a seat inherits conventions by running the validator, not by reading the convention.**

### 2.3 Amendment text

**Amendment 1 — `protocols/HANDOFF_PROCESS.md` §2, "What CC emits — the residual".**

Current text (lines 48-56) says the residual is pointers and does not re-transmit state the
repo encodes. **Append after item 3:**

> **4. Session-scoped retrieval — RESIDENT, not pointered.** The §2 pointer rule protects
> against *drift*, and drift is a property of surfaces with more than one reader. A sheet cut
> for this session alone — a candidate pool, a carried-decision list, the live rows for every
> `[#id]` the purpose names — has exactly one reader and cannot drift, so pointering it buys
> nothing and costs a round trip the browser seat cannot make on its own. **Test: if the
> artifact would be stale in a week, pointer it; if it would be meaningless in a week, carry
> it.** Methodology and BACKLOG task-state remain pointers (§3, §6) — this clause narrows
> neither.

**Amendment 2 — `protocols/HANDOFF_PROCESS.md` §5, evidence-block contract.**

Current text (lines 199-207) requires rows for the five manifest probes, both orientation
reads, inherited claims, P0a/P0b/P0c and P3. **Append:**

> **A required row must be able to FAIL.** The Destination block's own rule — *"a leg with no
> mechanical counterpart cannot fail honestly, and one that cannot fail honestly discredits
> the whole block"* — governs the probe manifest too. A row that passes by construction is
> removed, not retained for completeness; a manifest of rows that cannot fail reads as
> ceremony and is discounted wholesale, taking the rows that *can* fail down with it.
> **Each seal reports the count of rows that have ever FAILed**; a row with zero failures
> across three consecutive seals is a removal candidate, surfaced at the next cut.

**Amendment 3 — `protocols/HANDOFF_PROCESS.md` §4, the BOOT DRILL (lines 108-133).**

The drill currently asks the operator to *read* one sample dispatch line and concedes it binds
to nothing. **Replace the "Honest limit" paragraph with:**

> *What binds it.* The sample line's **lane name is checked, not looked at**: the seat runs
> `validate_branch_naming.py --lane <name>` on the line it emits and reports the classification
> alongside it. That converts the drill's one checkable component from a judgment into a
> verdict, and it is the component that failed on 2026-08-08 — nine of ten dispatched lanes
> carried names the validator refuses. The rest of the line (board label, tier, tree) remains
> an operator look, and that half is still prose discipline: no gate reads it. Stated so this
> is not read as fully enforced.

---

## 3. The lane-contract-as-artifact gap (contract item 8)

**The record.** `[#505]` leg 1 has now been missed by two consecutive batches. Batch 2's
packet already named the fix — *"lane contracts must be committed artifacts, referenced by the
manifest… That is one change away"* — and **batch 3 did not take it**; worse, batch 3 removed
the manifest as well, *"so a fresh seat inheriting batch 3 finds **neither** the contracts
**nor** the plan in the tree"* (`…consolidation-report.md:240-244, 322-330`). Every batch-3
contract lived in `~/Downloads`, and `$env:CLAUDE_PROMPTS_DIR` did not expand at dispatch — the
integrator's own contract path arrived as a literal `\ARC-batch3-consolidation-integrate.md`.

**Why discipline has failed twice, and will fail a third time.** The contract is authored in
the browser seat, which has no file access, and dispatched through a Windows wrapper in another
repo. Every step of its life is outside the tree. There is no moment in the current flow where
committing it is the path of least resistance — and a step that is never the easy path is not
maintained by discipline, it is maintained by luck.

**The mechanism — make the manifest's existing openness predicate carry the contracts.**

The manifest is already the artifact that must exist at dispatch (§1.1), is already committed,
is already immutable, and is already read by a live predicate. Extend its frontmatter:

```yaml
---
batch: 4
status: open
closed_by: docs/audits/2026-08-XX-technical-batch-4-packet.md
contracts: docs/batch/2026-08-XX-batch-4/     # NEW — the directory holding every lane contract
---
```

and add to `batch_manifest.open_batches()` the same discipline `_valid_closer` already
applies: **a manifest whose `contracts:` path is absent from the committed tree opens
nothing.** That is the entire enforcement, and it works because it inverts the incentive — the
batch cannot obtain its exemption until the contracts are in the tree. Nobody has to remember;
the merge queue does not run otherwise.

**Two problems it creates, both real.**

1. **`docs/batch/` is not a sanctioned Tier-1 or Tier-2 path.** `validate_hermetization`
   Rule A blocks a new `docs/<genre>/` (`SANCTIONED_GENRES` = archive, audits, decisions,
   handoffs, intake). So this needs either an ADR-101 amendment or the contracts nest under
   `docs/audits/` with a class token. **The latter is wrong** — a contract is not an audit —
   and I recommend the amendment. **Ruling needed, §6 R3.**
2. **`docs/audits/` immutability vs. a mid-batch contract correction.** An operator correction
   to a live lane cannot edit a committed contract. That is correct behaviour, not a bug: the
   correction is a new artifact, and `/lane-boot` §4 already rules that the frozen contract is
   *"this lane's authoritative surface"* and later content is not load-bearing. Note it; do
   not solve it.

**Library-first check.** Reuse of `_valid_closer`'s exact pattern and `_git`'s
`cat-file -e` probe — both already written, both already tested. Stdlib. **This is the
cheapest real leg in the report: ~10 lines against existing helpers**, and it is the one
`[#505]` obligation that two batches have proven discipline will not deliver.

**Scope honesty.** This delivers `[#505]` leg 1 only (contracts recoverable from the tree). It
does not deliver "a fresh seat runs a full batch from repo artifacts alone" — that needs the
per-lane *decisions* too, which is a larger row. Do not let leg 1's landing be read as the
row closing.

---

## 4. The n=5 unattributed HEAD swaps (contract item 9)

**Evidence, and its limit.** The batch-3 consolidation report lists this among items *"Carried
from the contract, unmodified… relayed as the contract stated them and carry no independent
check from this arc"* (`…consolidation-report.md:255-265`). **The n=5 figure is not
independently verified anywhere in the tree, and this lane does not verify it either** —
verification requires the operator's local reflog, which is gitignored and therefore does not
exist in a cloud clone. **Marked UNAVAILABLE** per the runtime rule.

**What the tree does hold** — two prior instances, fully documented, which make the pattern
real even if n is not:

- `JOURNAL.md:7104-7110` (2026-07-21): a concurrent HEAD swap put commit `94426dc0` directly on
  main's first-parent spine — a **core-invariant #5 violation**. The reflog is explicit:
  `checkout: moving from main to chore/reserve-id-range-373-380`, then back to `main` — *"a
  checkout **this session did not run**"*. Between those points the session ran only Edit,
  `validate_backlog.py`, `git diff --stat`, `git add`, `git commit` — **none of which moves
  HEAD.** The `ai-council-handoff` session was live throughout. Recorded as *"the second time
  this arc that a concurrent session's HEAD swap has cost real work."*
- `JOURNAL.md:6117`: *"mid-arc HEAD swap to main at 14:43:25 (repaired, zero loss)"*.

**Root-cause candidates, ranked by what the evidence supports.**

1. **A concurrent Claude Code session sharing the primary checkout — strongest.** The 07-21
   entry names a live sibling session and rules out every command the affected session ran.
   Multiple sessions in one working tree share one HEAD; a `git checkout` in either moves it
   for both. This explains the timing, the direction (back to `main`), and the orphaned branch.
2. **The agent runtime's own branch handling.** Worktree entry/exit and branch provisioning
   both check out. A tool that checks out and returns without restoring produces exactly this
   signature.
3. **Editor/tooling git integration** (VS Code branch indicator, a GUI client). Plausible,
   weaker: these usually check out on explicit click.
4. **A background script.** No evidence; Layer 2 forbids orchestration scripts here.

**What would identify it — one cheap instrument.** The reflog *already records the answer* and
nothing reads it. A `SessionStart` probe that records `git rev-parse HEAD` + the reflog head,
and a `Stop`/pre-commit probe that compares: an unexplained delta between them, with the
intervening reflog lines and their timestamps, attributes the swap to a window. Correlating
that window against session start times names the culprit in one or two occurrences.

**What would make it harmless — and this is the better investment.** Root-causing costs
instrumentation plus a wait for recurrence. **Making it harmless is already 90% done and free:**

- `block-ff-push` **already refuses** the push a HEAD swap produces (a non-merge commit on
  main's first-parent spine), and has failed CLOSED since the 2026-08-03 amendment. The 07-21
  violation *"was not pushed; `block-ff-push` would refuse it."* **The damage is already
  contained at the boundary that matters.**
- The residual harm is local: a commit landing on the wrong branch, needing a repair the 07-21
  entry declined to perform because it would hard-reset a tree another live session was using.

So the remaining exposure is **not "a bad commit escapes"** — it is **"repair is unsafe while a
sibling session is live."** The mechanism that addresses *that* is not HEAD-swap detection, it
is **not sharing the primary checkout**: every parallel session gets a worktree. The repo has
already ratified this (`worktree-<name>` lanes, `/lane-boot`, `.worktreeinclude`,
`worktree_seed.py`) — and 2026-08-08 is a batch where nine of ten lanes were provisioned
*by hand instead of through it* (§1.3/§1.4).

**Verdict: do not build a HEAD-swap organ.** Build the §1.3 provisioning refusal, which
removes the shared-checkout precondition. Add the reflog probe **only** as cheap instrumentation
to confirm the diagnosis — ~20 lines, `git reflog --date=iso`, stdlib — and expect it to become
redundant.

---

## 5. Ranking — prevented cost ÷ build size (contract item 10)

Prevented cost is **measured 2026-08-08 cost**, not projected. Build size is honest
line-count against existing organs.

| rank | mechanism | prevented cost (measured) | build | ratio |
|---|---|---|---|---|
| **1** | **Rule C — consumer-glob refusal (§1.7e)** | 2h12m *counterfactual*, plus 2 immutable-artifact repairs actually paid (one supersede, one deliberate rule-3 deviation) | ~45 lines + tests, extends a live hook | **highest** |
| **2** | **Lane-branch enum at provisioning (§1.3)** | 9 of 10 branches off-enum; two rival regexes; the F4 drift edge | ~15 lines against a tested classifier | **very high** |
| **3** | **Dispatch-time open-batch refusal (§1.1)** | **2h12m, actually paid** | ~30 lines, reuses `open_batches()` | **very high** |
| 4 | `contracts:` in the manifest (§3) | `[#505]` leg 1 missed twice; a fresh seat finds no plan and no contracts | ~10 lines + an ADR-101 amendment | high, but gated on a ruling |
| 5 | Stale-open-batch WARN (§1.5) | not independently measurable this batch | ~12 lines in existing reporting | moderate |
| 6 | `/preflight` as a template beat (§1.2) | one false premise, corrected in-flight | 1 sentence | high ratio, low absolute |
| 7 | Contract-prose rules — no file counts, literals are hypotheses (§1.6) | one measurement lane spent on a frozen spelling | 2 sentences | high ratio, low absolute |
| 8 | Handoff amendments 1–3 (§2.3) | 1 boot round trip; a discounted probe ceremony | 3 prose amendments | moderate |
| 9 | Reflog attribution probe (§4) | unverified (n=5 UNAVAILABLE) | ~20 lines | **low — build last or never** |

### The three I would build first

**#7 (Rule C), #3 (lane-enum at provisioning), #1 (open-batch refusal).**

They are the same mechanism three times — *the authoring step runs the predicate the consumer
will apply* — and they are the three places where an organ either exists and is unrun, or is
one import away from existing. Together they are under 100 lines, add zero dependencies, and
each converts a documented 2026-08-08 failure into a refusal at the moment the cost is
seconds instead of hours.

### Blunt: which of my own proposals are not worth building

- **`contract-lint` (§1.2) — do not build.** It cannot discriminate state claims from prose
  without NLP, and the contract that motivated it *already carried a SHA*, so the stamping rule
  it would enforce would have passed the very artifact it exists to catch. This repo already
  measured and rejected the analogous "field presence implies artifact class" heuristic at
  `audit.py:4001-4005`. One template sentence does more.
- **The artifact generator / "name it through the generator" (§1.7d) — do not build for this
  reason.** No generator writes to `docs/audits/` today, so it is a new script + command +
  template + freshness surface; and the repo contains a **measured negative result** —
  `PLAYBOOK.md:3476` already holds the correct `# Codex Review — {topic}` template, and
  instance B was hand-authored around it anyway. A generator prevents only what is routed
  through it.
- **The "companion-file predictor" (§1.6) — do not build.** ~80 lines parsing hook config to
  serve one prose sentence, and it would institutionalise the file-count habit the sentence
  exists to kill.
- **A HEAD-swap detection organ (§4) — do not build.** `block-ff-push` already contains the
  consequence at the push boundary and fails closed. The precondition (a shared primary
  checkout) is removed by mechanism #2, which is being built anyway.
- **`pydantic` for the manifest frontmatter (§1.7f) — not yet.** Right library, wrong place:
  it must not enter a gate path, and outside that path it duplicates a 6-line check. Revisit
  above ~5 fields.

**One caution on the top three, stated against my own recommendation.** Rule C's
`_CONSUMER_CONTRACTS` is a registry, and this repo's own record is that registries grow past
their maintainers (`AUDIT_CLASS_ENUM` is closed by ADR for exactly this reason). If Rule C
ships, it ships with the same closure discipline: **a row enters only by recorded ruling,
after a real defect.** A Rule C with six speculative rows is worse than no Rule C.

---

## 6. Needs a ruling

**R1 — Rule C's scope, and whether an *omission* is refusable.** Rule C as designed catches a
name that *announces* a class its consumer cannot parse (`…night-batch-manifest.md`). It does
**not** catch a manifest named `…-night-plan.md`, which announces nothing. Closing that gap
requires the inverse rule — *a batch's manifest must be named through a fixed template* —
which is the generator proposal §1.7d argues against. **Ruling: accept the announced-class-only
scope with the omission gap documented, or mandate a template name for manifests specifically
(narrow, and defensible for this one artifact class even though it fails as a general rule)?**

**R2 — the `batch:` field's failure direction.** Making `batch:` shape-checked in
`open_batches()` means a malformed value opens **no batch**, consistent with `_valid_closer`.
That is the safe direction for the exemption and the *unsafe* direction for
`gen_handoff`'s open-batch refusal (a handoff cut mid-batch would see nothing to refuse) —
the exact asymmetry `batch_manifest._git`'s docstring records for `[#512]`. **Ruling: accept
that asymmetry (as the repo already does for every other None-path), or is the `batch:` field
better left reporting-only and pinned by the test alone, as today?**

**R3 — `docs/batch/` and ADR-101.** §3's `contracts:` block needs a home. `docs/batch/` is not
in `SANCTIONED_GENRES`, so it needs an ADR-101 amendment; nesting contracts under
`docs/audits/` avoids the amendment but misclassifies a contract as an audit. **Ruling: amend
ADR-101 to sanction `docs/batch/`, or accept the misclassification, or a third home?**

**R4 — is a lane contract immutable?** If contracts become committed artifacts under
`docs/audits/` they inherit CLAUDE.md §5 rule 3 immutability. Under `docs/batch/` they do not,
unless ruled. `/lane-boot` §4 already treats a contract as frozen at the lane's boundary.
**Ruling: are committed lane contracts immutable artifacts, or living files a mid-batch
correction may amend?**

**R5 — the probe-manifest pruning rule.** §2.3 amendment 2 proposes removing probe rows that
have never FAILed across three seals. That deliberately shrinks the ceremony the operator
reports as low-yield, and it equally shrinks the evidence surface. **Ruling: adopt the
three-seal pruning rule, or keep every row and accept the yield complaint?**

**R6 — n=5 is unverified.** The figure is relayed from the dispatch contract with no
independent check anywhere in the tree, and the reflog needed to verify it is gitignored
(UNAVAILABLE from a cloud clone). **Ruling: verify n locally before any work is scoped against
it — or accept §4's recommendation that the number does not matter, because the fix is the
provisioning refusal that is being built anyway.**

**R7 — sequencing on the two `LANE_BRANCH_RE`s.** §1.3 insists provisioning-enforcement lands
*before* the loose regex is tightened, because tightening first makes nine of ten historical
lane shapes non-exempt. **Ruling: confirm the two-step sequence, and confirm that
`batch_manifest` importing `validate_branch_naming` is acceptable given the containment
property `tests/test_batch_manifest.py` asserts** (the edge points away from the pre-push
organ, but the assertion must be extended, not assumed).

---

## 7. What this lane did not do

- **Built nothing.** No edits to commands, hooks, templates, protocols, `tasks/` or
  `BACKLOG.md`. No rows birthed, no paths created beyond this report.
- **Merged nothing.** Branch pushed, integration is the operator's.
- **Did not verify n=5** — UNAVAILABLE from a cloud clone (§4, R6).
- **Did not verify defect 5's cost independently** — masked by defect 1's stop; no figure
  invented (§1.5).
- **Regenerated `docs/audits/README.md`**, which is not an exception to "one report": the
  `audit-index-freshness` hook blocks any commit adding a `docs/audits/*.md` without it. That
  is defect 6(a)'s lesson arriving in this lane's own commit — a contract saying "one file"
  would have been unsatisfiable here too.
