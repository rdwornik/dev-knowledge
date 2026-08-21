# LANE-539 — Ch8 dispatch-system codification (batch 1, lane A)

**Contract:** `LANE-539-ch8-codification.md` (prompts dir) · **Worktree:** `lane-539-ch8-codification`
· **Branch:** `worktree-lane-539-ch8-codification` · **Repo:** `.dev-knowledge` · **Row:** `[#539]`

> **Artifact home — read this first, it is owed to the integrator.** This file sits at the worktree
> root because the contract puts it there and forbids `docs/audits/` for this batch ("the archival
> lane owns that tree this batch; the integrator relocates your artifact per governance"). A
> top-level `ARTIFACT-lane-539.md` is **refused by `validate-hermetization` Rule A** — Tier-1 files
> are a closed class (ADR-101 §1) and this name is in none of it. The refusal is real, was verified
> rather than assumed, and is handled per the "Deviations" section at the end of this file.
> **PROPOSED-PATH for the integrator's relocation:**
> `docs/audits/2026-08-21-technical-ch8-dispatch-codification.md` — Rule-B conformant
> (`<date>-<class>-<slug>`, class token `technical`, lowercase kebab throughout).

---

## Step 1 — UNDERSTAND

### 1.1 The five §Q rulings whose declared home is Ch8

`protocols/STANDING_RULINGS.md` §Q states the binding explicitly, in its own preamble:

> **This register is the application surface; Ch8 is the declared durable home for Q1 and Q3–Q6,
> and `[#539]`'s codification lane carries them there.**

So the five are **Q1, Q3, Q4, Q5, Q6** — enumerated by id, not by inference. Q2 and Q10 are
excluded by the same preamble (their durable home *is* the register; what they are owed is a
one-line Ch8 pointer, dated `2026-09-19` and explicitly declared as owed by neither lane).
Q7/Q8/Q9 are model-admission rulings carried by `[#491]`/`[#562]`/`[#568]`, not by Ch8.

| id | Ruling, as §Q states it | Gap-table id |
|---|---|---|
| **Q1** | *index freshness on lane material* — the integrator is gate-of-record, and a declared single-hook bypass on a lane branch is sanctioned, with the declaration carried in the commit body | G10 |
| **Q3** | *harvest order* — push-before-delete, on every harvest: a merged branch is deleted on `origin` only after the merge is pushed, so no window exists in which integrated work lives solely in a local clone | G9 |
| **Q4** | *cloud lane hygiene* — a cloud lane branches fresh off `origin/main` and leaves foreign dirty files untouched | G14 |
| **Q5** | *receipt gate* — every cloud dispatch carries one: the git source resolves non-empty AND the first assistant text is echoed back. A dispatch without both is not a dispatch that ran | G3 |
| **Q6** | *contract-as-file without exception* — the frozen contract is a committed repo artifact at dispatch time; inline-with-a-dummy-filename is a forbidden dispatch form. This is the unconditional reading of I-D3, and it retires the "repair path, for batch 3" scoping that `protocols/PLAYBOOK.md` :2045–2086 still carries | G13 |

The gap-table column maps each to `docs/audits/2026-08-20-technical-playbook-status.md`, which §Q
itself names as the independent mapping and which "reads each of them as ABSENT from
`protocols/PLAYBOOK.md` today."

### 1.2 The gap, measured rather than inherited

The census claim was **re-measured live on this worktree's tree**, not carried over. A single
`ripgrep` pass over `protocols/PLAYBOOK.md` for the identifying tokens of all five rulings:

```
pattern: push-before-delete|audit-index-freshness|receipt|Receipt|foreign dirty|gate-of-record|CloudV2|origin/main
file:    protocols/PLAYBOOK.md
result:  No matches found
```

**All five read ABSENT — 0 matches, confirming the census at n=1 independently.** Q6 is the one
partial case: its *subject matter* is present (the section "Dispatch prompts and the contract of
record", :2045–2086) but present in exactly the scoped form Q6 retires — "**The repair path, for
batch 3**" — so the ruling itself, the unconditional reading, is absent. That is the shape §Q
describes, verified rather than trusted.

### 1.3 What Ch8 already carries — the reason this is an index, not a restatement

Ch8 (`protocols/PLAYBOOK.md` :1233–2283, 14 subsections) already holds most of the dispatch
system. The contract's Done-item 1 names three things Ch8 "carries"; two of the three are already
there in full, and re-stating them would create the second-copy-free-to-disagree defect Ch8's own
closing subsection was written to prevent:

| Done-item 1 clause | Live status in Ch8 today | This lane's act |
|---|---|---|
| the batch shape (ADR-110: one plan → N file-disjoint lanes → one integrator) | **Present, canonical** — "The batch protocol — ONE plan → N lanes → ONE integrator (ADR-110)", :1792 | **Point at it.** No restatement. |
| lane lifecycle: dispatch → commit-and-STOP → serial integration → teardown | **Present, distributed across five subsections** — dispatch (:2087, :2172), commit-and-STOP (per-lane requirement 4, :1834), serial integration (:1655 "Integrate from the primary"), teardown (:1679 three-command round-trip) | **Index the sequence**; the one genuinely missing step is the harvest leg. |
| …teardown **with Q3 push-before-delete** | **ABSENT.** The three-command round-trip at :1679 is `worktree remove` → `prune` → `branch -d`, and the merge/push ordering that precedes it is stated at :1655 without the *origin*-delete ordering Q3 rules | **Write it.** This is the real gap in the lifecycle. |

The governance pointer the contract names — Ch8 "Handoff prep for the next architect — an index,
not a restatement" (:2240) — is the doctrinal warrant for that column: *"This subsection is the
index and carries no doctrine of its own — every line below is a pointer, deliberately, because a
second copy of a rule is a second thing to keep true."* Applying that rule to this lane's own
output is the whole design.

**What is genuinely new content, therefore, is exactly the five rulings** plus one index that makes
the lane lifecycle readable end-to-end as one sequence, which it currently is not: a seat has to
assemble it from five subsections that never name each other in order.

### 1.4 Constraints discovered before writing (each verified, not assumed)

1. **`silent_rule_ratchet` headroom is 1 token.** `protocols/PLAYBOOK.md` is inside the detector's
   scope root (`protocols/*.md`). Live count **440** against committed baseline **441**
   (`python scripts/silent_rule_detector.py`, detector `silent-rule-v4`, 58 files). The check FAILs
   on an increase and blocks the commit through `audit-health`. **Consequence: the new Ch8 text is
   authored with zero new `must`/`shall`/`never` occurrences** — declarative phrasing, the same
   discipline `STANDING_RULINGS.md`'s own editing note imposes on itself. This is a real
   constraint on wording, and it is why the new text says "a lane deletes on `origin` only after
   the push lands" rather than the imperative form.
2. **`toc-freshness-playbook` is a regen-and-diff gate** on `^protocols/PLAYBOOK\.md$`. Every new
   `###` heading has to land in the `<!-- TOC:START -->` block. Regen:
   `python -m scripts.toc.cli generate protocols/PLAYBOOK.md --write`.
3. **`validate-hermetization` Rule A refuses a new top-level file.** See the banner at the top of
   this artifact; `scripts/validate_hermetization.py:213` is the classifier, and Tier-1 files are a
   closed class per ADR-101 §1:35.
4. **`scripts/` and `tests/` are both sanctioned Tier-1 directories and allowlisted Rule-C homes**
   (`_HOME_PATTERNS`, `scripts/validate_hermetization.py:172,176`), so the generator needs no
   PROPOSED-PATH of its own. Basis quoted in §3 below.

### 1.5 What could break

- **The ratchet.** One stray `never` in 200 lines of new doctrine REDs `audit-health` and blocks
  every commit including the one that would explain it. Mitigated by measuring before and after
  each PLAYBOOK commit rather than at the end.
- **Restatement drift.** Writing the batch shape out again where Ch8 already carries it creates two
  sources for one rule — the exact defect the ADR-110 section and the index subsection both warn
  about. Mitigated by the §1.3 table: pointer, not copy.
- **Q6 vs the live text.** Q6 does not add a rule beside :2045–2086; it *retires that section's
  scoping*. Landing Q6 as a new paragraph while the old "repair path, for batch 3" wording stands
  would leave the corpus stating both readings. Mitigated by amending the live text in place and
  saying so.
- **A generator that encodes rules no document owns.** The audit's own note: "Doctrine first,
  generator second — the reverse order produces a generator that encodes rules no document owns."
  Mitigated by contract step order (Ch8 at step 2, generator at step 3) and honoured literally.

---

## Step 2 — what landed in Ch8

Three edits to `protocols/PLAYBOOK.md`, +156/−7 lines including the regenerated TOC. All five
§Q rulings land; nothing else in the chapter moved.

**A · NEW subsection "The lane lifecycle — five legs, and where each one is ruled"** (before
"Dispatch visibility"). Four legs — dispatch, execute, commit-and-STOP, teardown — are *pointers*
to text already in Ch8. The fifth, **harvest**, had no prior home, and carries the two rulings that
belong to it:

- **Q3 · push-before-delete**, read explicitly against MERGE IS ATOMIC directly above it: this
  fixes the *order* of that operation's three parts and leaves its atomicity alone. Without that
  sentence the two texts read as competing rules about the same three commands.
- **Q1 · the integrator is gate-of-record for index freshness**, with the declared single-hook
  bypass on a lane branch as the sanctioned lane shape. Two reasons are given rather than asserted:
  a generator reads the *tracked* working tree, so a lane regenerating an index in a tree another
  lane is writing emits bytes that depend on in-flight files (`scripts/gen_audit_index.py`'s own
  header records that defect and the 2026-08-12 night-1 lane that hit it); and N lanes regenerating
  one shared index produce N conflicting versions of a single generated file. Scope is stated
  explicitly — one hook, named in the commit body, for index-freshness material — so it does not
  read as a general license against the gate mesh.

**B · NEW subsection "Cloud lanes — the receipt gate and the fresh-branch rule"** (before the
routing matrix): **Q5** (the two-part receipt, checked as a conjunction, with the reason each half
alone is insufficient) and **Q4** (fresh off `origin/main`, foreign dirty files untouched).

**C · AMENDED "Dispatch prompts and the contract of record" for Q6.** The section's lead read
*"The repair path, **for batch 3**…"* — the exact scoping Q6 retires. It now reads
*"Contract-as-file, without exception"*, names inline-with-a-dummy-filename as a forbidden dispatch
form, and states that the rule has no conditional form. The section's two consequences are
untouched; its honest limit was de-scoped as a terra finding (D3 below).

**D · The chapter's own index** ("Handoff prep for the next architect") gains pointers to both new
subsections, so the index stays complete — the property that subsection exists to hold.

**Every rule carries its evidence and its honest limit**, in the chapter's voice. Stated plainly and
worth repeating here: **all five are prose today.** No organ reads a commit body for a bypass
declaration; no organ reads the ordering of a push against a remote-branch delete; the receipt gate
and the hygiene rule are checked by the dispatching seat and by nothing else.

### The wording constraint, because it shaped the text

`protocols/PLAYBOOK.md` sits in the `silent_rule_ratchet` corpus and live headroom was **one
token** (440 measured against baseline 441). The check FAILs on an increase and blocks the commit
through `audit-health`. So the new doctrine is authored with **zero** new `must`/`shall`/`never`
occurrences — declarative phrasing throughout, the same discipline `STANDING_RULINGS.md`'s own
editing note imposes on itself. Measured before and after every PLAYBOOK commit: **440 → 440.**

---

## Step 3 — the generator

`scripts/gen_lane_contract.py` (573 lines) + `tests/test_gen_lane_contract.py` (343 lines, **70
tests**).

### LOCATION, with the governing line quoted

`docs/decisions/ADR-101-hermetization.md` §1, "Sanctioned top-level set (CLOSED, two-tier)":

> **Tier-1 — repo root.** Sanctioned directories: `.claude/ .claude-plugin/ .vscode/ codex/
> config/ deploy/ docs/ ecosystem/ logs/ plugins/ protocols/ scripts/ templates/ tests/`.

`scripts/` and `tests/` are both members, and both are allowlisted Rule-C homes in
`scripts/validate_hermetization.py` `_HOME_PATTERNS` (lines 172, 176). Nine `gen_*.py` siblings
already live in `scripts/` with their nine `test_gen_*.py` counterparts in `tests/` — the live
precedent for this exact class. **Verified rather than inferred:**
`python scripts/validate_hermetization.py scripts/gen_lane_contract.py tests/test_gen_lane_contract.py`
exits 0. **No `PROPOSED-PATH` is owed for the generator** — governance covers the home.

*Recorded honestly:* the contract names "Folder Governance / dev-root schema" as the source. The
only `## Folder governance` heading in the corpus is `protocols/PLAYBOOK.md` §"1. Starting a New
Project" — a fragment of the **child-repo `CLAUDE.md` template**, not the hub's own taxonomy. The
hub's taxonomy is ADR-101 §1, quoted above, and that is what was used.

### What is baked in, each asserted by a test

| Baked-in region | Test |
|---|---|
| `## Dispatch` block, `Dispatch-Lane <slug> <file> -Effort <tier>` | `test_the_dispatch_block_carries_the_dispatch_lane_form` |
| `--permission-mode bypassPermissions`, `--bg`, model default `opus` | `test_the_dispatch_constants_and_the_model_default_are_stated` |
| worktree ⇄ contract-file pairing, prefix applied exactly once | `test_the_pairing_line_is_present_and_self_consistent`, `test_the_worktree_prefix_is_applied_exactly_once` |
| V-2 decision budget, ask-classes (a)/(b)/(c) | `test_the_decision_budget_carries_all_three_ask_classes` |
| Q5 receipt-gate fields, cloud lanes only | `test_a_cloud_lane_carries_both_receipt_fields_and_a_local_lane_carries_neither` |
| emitted file parses | `test_an_emitted_{local,cloud}_contract_parses_with_no_problems`, `test_the_file_written_to_disk_is_the_file_that_parses` |
| invalid effort names rejected | `test_an_effort_outside_the_enum_is_refused` (9 cases), `test_the_cli_refuses_an_off_enum_effort` |

A `check` subcommand parses an existing contract and reports **every** problem rather than the
first. That parser is what the round-trip tests exercise, so emitter and parser cannot drift apart
silently — a test that only read the emitter's constants back out of its own output would pass on a
generator emitting nothing a dispatch can use.

### Step 4 — the library-first line

**Checked before hand-rolling:** `templates/prompt-template.md` v1.14 (the work-lane card — its
`## Dispatch` block and Model/Mode/Effort table are the emitted markdown's shape, copied rather
than reinvented); `scripts/gen_handoff.py` (the closest sibling generator — its Click CLI and
`templates/handoff/` layout set this module's CLI shape and its logging idiom); and
`scripts/validate_branch_naming.py`, **which changed the design**: `validate_lane_worktree_name`
is the repo's existing lane-name grammar, so it is *called* rather than re-implemented, and this
generator cannot disagree with `/lane-boot` about what a lane name is.

---

## Step 5 — terra review

Run as **two separate `codex exec` passes** at `gpt-5.6-terra`, not through `/codex-review`. Two
reasons, both recorded: the wrapper writes its artifact into `docs/audits/`, which this lane is
forbidden; and its path-guard filters a **mixed** code+prose diff down to the code subset and never
doc-reviews the prose — this branch's diff is mixed, so a single `/codex-review` would have left
the entire Ch8 edit unreviewed.

### Severity tally

```
code lane (scripts/ + tests/)   Critical 0   High 4   Medium 0   Low 0
doc lane  (protocols/PLAYBOOK)  Critical 0   High 3   Medium 2   Low 0
TOTAL                           Critical 0   High 7   Medium 2   Low 0
```

**All 9 adjudicated as real. All 9 fixed. Zero dispositioned, zero deferred.**

### Code findings — every one was in `parse_contract`

A check that can be fooled is worse than no check, which is why all four are High.

1. **C1 · a file whose whole body sat inside one code fence passed.** Every heading and every
   ask-class was "present" — as example text. Structure is now read from de-fenced text
   (`strip_fenced_blocks`, line-count preserving); the dispatch line, which legitimately lives
   inside a fence, is still read from the whole file. Regression:
   `test_a_contract_whose_whole_body_is_inside_a_code_fence_is_refused` plus its complement
   `test_a_fenced_dispatch_line_is_still_found`.
2. **C2 · a self-consistent contract on an off-grammar slug passed** — `bad_slug` +
   `LANE-bad_slug.md` + `worktree-bad_slug` all agreed with each other. The parsed slug is now
   validated, at the hyphen-only-kebab bar rather than the strict batch-lane grammar, because a
   non-batch worktree lane's bare purpose slug is a legal name for this chapter.
3. **C3 · a dispatch line with `-Effort` removed passed**, the tier being optional in the grammar.
   The grammar stays tolerant (the template's own `[-Effort …]` brackets mean optional at the
   surface); an absent tier is now **reported**, because a frozen contract states its own routing.
4. **C4 · the `| Model | Mode | Effort |` row was emitted and never read back**, so
   `| gpt | arbitrary | high |` passed unchallenged. The row is now parsed against both enums and
   cross-checked against the dispatch line's tier. *Worth recording:* the first fix used an
   unanchored three-column regex, which matched the **header** row as the body row — caught by the
   new tests, not by review. The regex is now anchored on its own header and separator.

### Doc findings — three were faithfulness defects, the class that matters most here

1. **D1 · High · Q4 was WIDENED.** *"Files the lane did not author **and its contract did not
   name** are left exactly as found"* grants a carve-out the register does not: Q4 says foreign
   dirty files are left untouched, full stop. Restated at Q4's own scope, with one sentence
   explaining why no exception is needed — a file the contract names and the lane then edits is the
   lane's own work, so the two cases do not overlap.
2. **D2 · High · Q5 was given timing and consequence it does not carry** — *"checked at dispatch
   time"* and *"is re-dispatched"*. Q5's own consequence is *"a dispatch without both is not a
   dispatch that ran"*; what follows from that is the dispatching seat's, and the register leaves it
   there. Restated in the register's words. The conjunction rationale is kept and now explicitly
   labelled *reading rather than ruling*.
3. **D3 · High · the section's honest limit still ended "The batch-3 manifest is the first artifact
   that can satisfy it"** — directly contradicting the Q6 amendment three paragraphs above it.
   De-scoped: a rule with no conditional form has no first batch either.
4. **D4 · Medium · the lifecycle index restated the five per-lane requirements** it was meant to
   point at — the exact defect the chapter's closing subsection names. Compressed to a pointer.
5. **D5 · Medium · the substrate paragraph read as a third landed rule** in a section that says
   two, and it is neither Q4 nor Q5. Demoted to a labelled **description of practice**, explicitly
   outside the two rules, naming `docs/audits/2026-08-20-technical-playbook-status.md` G1 as where
   the rule is owed. Kept rather than deleted: a cloud-lane section with no test for which lanes are
   cloud lanes is hard to apply, and an undescribed gap is the harder one to close.

---

## Deviations, open items, and things for the architect

Reported rather than asked, per this lane's zero-question decision budget. Nothing below was
decided silently.

### 1 · DEVIATION — this artifact's own path is refused by `validate-hermetization` Rule A

The contract places this file at the worktree root and forbids `docs/audits/`. A new top-level
`ARTIFACT-lane-539.md` is outside ADR-101 §1's closed Tier-1 file class, so Rule A blocks it. The
step-1 commit therefore carries a **declared single-hook bypass**, `SKIP=validate-hermetization`,
with the basis in the commit body — the shape Q1 sanctions, applied by analogy beyond its
index-freshness scope, which is itself a stretch and is named as one here rather than hidden.

**Owed to the integrator: relocate this file.** PROPOSED-PATH
`docs/audits/2026-08-21-technical-ch8-dispatch-codification.md` — Rule-B conformant. Once it moves,
the refusal class disappears; Rule A is prospective-only on staged ADDs.

### 2 · This lane's own dispatch does not satisfy Q6, the ruling it just landed

`[#539]`'s frozen contract lives at `~/Downloads/LANE-539-ch8-codification.md` and is **not a
committed repo artifact**. Q6 — *"the frozen contract is a committed repo artifact at dispatch
time"* — is exactly what this lane transcribed into Ch8, and this dispatch does not meet it. Stated
because Ch8 now says the rule has no conditional form, and a lane that lands that sentence while
running outside it should say so rather than let the next reader discover it. **No action taken:**
committing the contract would need a `docs/audits/` write this lane is forbidden.

### 3 · This lane's worktree name is off the batch-lane grammar

`lane-539-ch8-codification` omits the lane **letter**, so
`validate_branch_naming.validate_lane_worktree_name` refuses it; the conforming form is
`lane-a-539-ch8-codification` (the contract's own header calls this "batch 1, **lane A**"). Not
repaired — a rename mid-lane costs a teardown and the validator is wired into no gate. Recorded
because the generator now refuses this name by default, and `test_the_batch_lane_grammar_is_
delegated_not_reimplemented` pins that behaviour deliberately.

### 4 · DECLARED DIVERGENCE — the effort enum has two live definitions

| Source | Enum |
|---|---|
| `[#539]`'s contract (Done-item 2) | `{low \| medium \| high \| xhigh \| max}` |
| `protocols/PLAYBOOK.md` Ch8 + `Invoke-Dispatch.ps1` | `{low \| medium \| high \| xhigh}` — **closed**; `max` held out of dispatch routing by the 2026-08-07 architect ruling |

A contract emitted with `-Effort max` is expected to be **refused at the dispatch surface**.
Resolved per contract defaults: the generator implements the **five the contract names**, refuses
anything outside them, and **logs a warning naming the divergence** whenever `max` is selected — so
the conflict surfaces at generation time rather than at the operator's terminal. Choosing between
the two enums is a ruling, and a generator is not where one gets made. **Architect decision owed.**

### 5 · Proposed pre-commit hook — NOT applied (the contract reserves `.pre-commit-config.yaml`)

A `--check` leg with no gate is a validator nobody runs. The natural wiring, offered as a fenced
diff for the integrator:

```yaml
      - id: lane-contract-check
        name: Lane-contract shape gate ([#539]; HUB-ONLY)
        # A committed lane contract (Q6) is checkable at commit time: every mandatory
        # section present, the dispatch line and the routing row agreeing on the tier,
        # and the worktree<->file pairing self-consistent with the `worktree-` prefix
        # applied exactly once. Honest limit: it checks SHAPE, never whether the
        # contract's footprint claims are true.
        entry: uv run --locked python scripts/gen_lane_contract.py check
        language: system
        files: '^docs/audits/.*-lane-contract\.md$'
```

**Two reasons this is a proposal rather than a recommendation.** The `files:` pattern above is a
guess at where committed contracts will land — `docs/audits/*-lane-contract.md` is the observed
2026-08-20 convention, but nothing rules it. And the gate only becomes meaningful once Q6 is
actually practised (item 2 above); wiring it first would produce a hook that matches zero files.

### 6 · Noticed, out of scope, left standing

- `templates/prompt-template.md` v1.14 carries the effort enum as the closed four and shows a
  `claude --bg --model … --effort …` dispatch line, while `[#539]`'s contract shows the
  `Dispatch-Lane` form. Both are live; neither is wrong. If `Dispatch-Lane` becomes the stated
  surface, the card is the point-of-use copy that would follow — not this lane's file.
- Q2 and Q10 are each owed a **one-line Ch8 pointer** (§Q's anti-orphan block, `disposition:
  deferred`, trigger `2026-09-19` **or this lane's landing, whichever comes first**). §Q says the
  pointer "is owed by neither lane and is dated instead of assumed", so it was not written. **This
  lane landing IS the named trigger**, so the deferral is now due: the pointers go beside
  *"Integrate from the primary"* (Q2) and the lane-contract requirements list (Q10), or the
  deferral is re-dated with a reason.

---

## Self-test — the acceptance contract, re-run as a checklist

| Done-contract item | Verdict | Evidence |
|---|---|---|
| 1 · Ch8 carries the five §Q rulings, enumerated from §Q by id | **PASS** | Q1/Q3/Q4/Q5/Q6, §1.1 above; §Q's preamble quoted as the basis |
| 1 · batch shape (ADR-110) | **PASS (by pointer)** | already canonical in Ch8; the index points, deliberately does not restate |
| 1 · lane lifecycle incl. Q3 push-before-delete at teardown | **PASS** | new "lane lifecycle" subsection; harvest is the leg that was missing |
| 2 · `gen_lane_contract` exists and emits a contract | **PASS** | `scripts/gen_lane_contract.py`; `emit` / `check` / `enums` |
| 2 · dispatch-block template baked in, model default opus, permission-mode stated | **PASS** | table above; 3 tests |
| 2 · decision-budget section baked in | **PASS** | `test_the_decision_budget_carries_all_three_ask_classes` |
| 2 · worktree⇄file pairing line baked in | **PASS** | 2 tests, incl. the doubled-prefix regression |
| 2 · receipt-gate fields for cloud lanes | **PASS** | `--cloud`; `test_a_cloud_lane_carries_both_receipt_fields_and_a_local_lane_carries_neither` |
| 2 · tests: emitted file parses / mandatory fields present / invalid effort rejected | **PASS** | 70 tests green |
| 2 · LOCATION derived with the governing line quoted | **PASS** | ADR-101 §1 quoted above; `validate_hermetization` exits 0; no PROPOSED-PATH owed |
| 3 · English · hyphen-only names · logging not print · Click CLI · pytest green | **PASS, one reading stated** | see below |
| 4 · library-first line | **PASS** | Step 4 above |
| 5 · terra review, tally in the artifact, P1/P2 fixed | **PASS** | 9 findings, 9 fixed |
| 6 · pytest green, one end-of-lane artifact, commit, STOP | **QUALIFIED** — see "Suite result" | 3180 passed / 21 failed; **1 of the 21 is this lane's**, and it is the contract-mandated artifact path |

**The one reading, stated rather than assumed.** *"Hyphen-only names"* is applied to the identifiers
the generator **produces** — slugs, branches, emitted filenames — where it is enforced
(`validate_slug` refuses `lane_a_539_x`). The Python module itself is `gen_lane_contract.py` with
underscores, matching all nine `gen_*.py` siblings, because a hyphen in a module name makes it
unimportable and `tests/` imports it directly. *"Logging not print"* is honoured in the module's own
diagnostics (`logger = logging.getLogger("gen-lane-contract")`, mirroring `audit.py`); `click.echo`
is used only for the two commands whose **output is the product** (`emit --stdout`, `enums`), which
is `gen_handoff.py`'s idiom.

---

## Suite result — stated qualified, because it is

```
uv run --locked pytest      3180 passed · 21 failed · 11 skipped · 1 xfailed · 17m25s
```

**The exit code lied and is not the evidence.** The run was piped (`| tail`), so the harness
reported `exit code 0` — the *pipe's* status, not pytest's. The summary line is the reading, and
it says 21 failed. Recorded because a lane that reports a piped exit code as its verdict has
reported nothing.

**Ownership, proven rather than asserted.** This lane's whole footprint is four files
(`git diff main...HEAD --name-only`): `ARTIFACT-lane-539.md`, `protocols/PLAYBOOK.md`,
`scripts/gen_lane_contract.py`, `tests/test_gen_lane_contract.py`. It touched **zero** of the
surfaces the other twenty REDs read — `git diff main...HEAD --name-only -- BACKLOG.md tasks/
.pre-commit-config.yaml scripts/fleet_analytics.py scripts/block_unanchored_push.py
scripts/enforcement_coverage.py ecosystem/` returns **0 files**.

| n | Failure | Mine? | Why |
|---|---|---|---|
| 17 | `tests/test_fleet_analytics.py` — `ModuleNotFoundError: No module named 'pandas'` | **No** | the optional `analytics` extras group is not synced in this lane's fresh venv. `pyproject.toml:47` names the fix: `uv sync --locked --group analytics`. Confirmed directly — `uv run --locked python -c "import pandas"` raises in this tree |
| 1 | `test_audit.py::test_check_fleet_parity_green_on_live_repo` | **YES — this lane's, and the only one** | see below |
| 1 | `test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row` — `'3 declared routine row(s)'` vs 1 | **No** | reads live `BACKLOG.md`; this lane made zero BACKLOG / `tasks/` edits |
| 1 | `test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent` | **No** | probes the live pre-push organ (*"REFUSED an anchored push too … a constant refusal enforces nothing"*); this lane touched no hook, no hook config, and none of the scripts the probe runs |
| 1 | `test_stale_worktrees.py::test_linked_worktrees_reader_excludes_the_primary` | **No** | asserts `audit._REPO_ROOT` is absent from the linked-worktree set; run from *inside* a worktree that is structurally false, since `_REPO_ROOT` **is** a linked worktree. The known lane-worktree RED |

### The one that is mine — and it is the artifact path again, not the work

```
live fleet not green: [".dev-knowledge root-sweep WARN-undeclared:
 top-level entry 'ARTIFACT-lane-539.md' is not in the template for role 'hub'"]
```

`fleet_parity`'s root-sweep flags a top-level entry absent from the hub role template. The failing
assertion's `real` list has **exactly one member**, and its evidence names **exactly this file** —
so the live fleet is otherwise green and this artifact is the sole cause. That is the proof, taken
from the failure's own output rather than from a second run.

**This is the same root cause as the Rule-A refusal in deviation 1 above, surfacing at a second
gate.** A top-level `ARTIFACT-lane-539.md` is not a sanctioned Tier-1 file (ADR-101 §1) and is not
in the hub root template — one defect, two organs. The contract placed the file here and forbade
`docs/audits/`, so the lane wrote it here as instructed rather than silently relocating it.

**It is REPORTED, not dispositioned, and not worked around.** No `SKIP` was applied to the suite,
no test was edited, and the file was not moved into the tree this lane is forbidden. **The
integrator's relocation to `docs/audits/2026-08-21-technical-ch8-dispatch-codification.md` closes
it** — the entry leaves the root, the root-sweep WARN and the Rule-A refusal both disappear
together, and no other change is needed.

**The lane's own tests: 70 passed, 0 failed** (`tests/test_gen_lane_contract.py`), and
`ruff check` is clean on both new files. Nothing this lane authored fails.

## What this lane did NOT do

No merges, no pushes, no other branch touched — commit-and-STOP. No JOURNAL entry (the integrator's
surface, P-1). No `BACKLOG.md` / `tasks/` writes. No `STANDING_RULINGS.md` edits. No
`.pre-commit-config.yaml` edit — the hook above is a proposal. No `docs/audits/` write of any kind,
including the terra artifacts, which were kept as untracked temporaries and deleted. No audits-index
regeneration. No rulings of its own: every divergence above is reported, not decided.
