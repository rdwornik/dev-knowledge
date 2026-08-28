# NB2 · LANE G packet — pre-freeze contract predicates ([#591] extension, architect lane N8)

**Consumer:** `docs/audits/2026-08-28-technical-batch-2-manifest.md` (this packet is that
manifest's lane-G return; the integrator consumes it in the merge queue).
**Branch:** `worktree-lane-g-591-preflight-predicates` · **Substrate:** local worktree
**Contract:** `docs/audits/2026-08-28-technical-batch2-launch-contracts/NB2-LANE-G-591-preflight-predicates.md`
**Status:** committed and STOPped. No self-merge, no JOURNAL entry, no `tasks/` write, no
generated-surface regeneration.

---

## 0. THE HOME DECISION — asked for explicitly, answered before code was written

The contract named three candidates and required the choice be stated with a reason.

**Chosen: predicates (i)–(iv) extend `scripts/preflight_contract.py`; defect (v) is fixed in
`scripts/validate_substrate.py`.** Two existing organs extended, no rival created.

Why not put (i)–(iv) in `validate_substrate.py`, the module `[#591]` names: that module answers
exactly one question — *does a contract's declared SUBSTRATE agree with its content*, against
`ecosystem/substrate-registry.yaml`. **None of the four predicates is a substrate question.**
Putting them there would have produced two organs sharing a filename.

Why `preflight_contract.py` is the honest sibling — and the contract pre-authorised this
reading ("if the honest home turns out to be `preflight_contract.py`, that is a ruled-sibling
reading the contract's own parenthetical permits"):

| | evidence |
|---|---|
| its charter is the predicates' charter | module docstring: *"verify the repo locators a contract or prompt cites, before acting"* |
| leg (iii) is already half-built there | `CLAIM_KINDS` carries `backlog-id`; the `[#483]` assertion-vs-citation role rule is already implemented |
| legs (i)/(ii) reduce to its primitive | "does this claim carry a locator that resolves" |
| the posture already matches | 0 clean / 1 violation / 2 internal-error-BLOCKS, and *"adoption first: wired into NO gate"* |

Defect (v) is not a choice: `_SHAPE_RE` lives in `validate_substrate.py` and nowhere else.

---

## 1. PER-DONE-ITEM VERDICT

Every witness below is a command that was run, or a `file:line`. Re-run witness:

```
uv run --locked python scripts/preflight_contract.py \
  docs/audits/2026-08-28-technical-batch1-launch-contracts/BATCH1-LANE-CONTRACTS-2026-08-28.md \
  --predicates-only
uv run --locked pytest tests/test_preflight_freeze_predicates.py tests/test_preflight_contract.py tests/test_validate_substrate.py
```

### (i) every referenced off-repo input EXISTS at freeze — **MET**

Two legs, because one is not enough and the reason matters.

- **Path leg** — `preflight_contract.py::check_off_repo_inputs`, `_OFF_REPO_PATH_RE`. Six
  operator-disk shapes (Windows drive, `~/`, `%USERPROFILE%`, `$env:CLAUDE_PROMPTS_DIR`,
  `$CLAUDE_PROMPTS_DIR`, `<PROMPTS_DIR>`). Existence is checked on the freezing machine; a MISS
  is a REFUSAL naming the path. An **unset** variable is a refusal, not a skip.
  Failing/passing pair: `test_i_off_repo_path_that_does_not_exist_is_refused` /
  `test_i_off_repo_path_that_exists_passes`; plus `test_i_unset_prompts_dir_is_a_refusal_not_a_skip`.
- **Input-clause leg** — and this one is the reason (i) actually reproduces the real defect.
  **The path leg alone would have caught NOTHING in batch-1's contract**: I measured it, that
  file contains zero operator-disk path shapes. Finding C-G is `**Basis:** the SDA-1 adversarial
  artifact` — an input with *no path at all*, which is precisely why no path-existence check can
  see it. So a `Basis:`/`Input:`/`Reads:`/`Fixture:`/`Depends on:` clause carrying **no locator
  of any kind** is itself the refusal. `**Depends on:** nothing` is a complete answer and passes
  (`test_i_depends_on_nothing_is_an_answer_not_a_miss`).

### (ii) every "verified"/"measured" claim carries a witness — **MET**

`check_witnessed_claims`. Trigger set is the contract's own: `verif*` / `measur*`. A witness is
a **command or a locator in the same sentence** — a `file:line`, a backticked command line, a
`.py`/`.ps1`/`.sh` script, a `--flag`, or a lowercase dotted callable.

**The precision/recall trade, as required.** Recall is capped at one axis on purpose — the
trigger words — and precision is bought three ways, each paying for a *measured* false positive
on the batch-1 corpus, not a hypothetical one:

1. **fenced blocks and blockquotes are dropped.** The design note's own warning: the bundles
   quote their own lanes, so without this a defect reported once is re-reported by every bundle
   that ever quoted it (`test_ii_quoted_prose_does_not_fire`).
2. **the trigger must sit outside a backtick span.** `` `verify:` `` names a convention; it does
   not assert one was run.
3. **the unit is a SENTENCE, not a line.** This corpus hard-wraps at ~90 chars. A line-unit
   detector reports batch-1 L1 item 1 as unwitnessed, and the only thing wrong with it is where
   the newline fell — a false positive manufactured by typography
   (`test_ii_a_witness_that_hard_wrapped_still_counts`).

**A deliberate non-decision, stated rather than hidden:** no attempt is made to separate a
past-tense claim ("verified, not assumed") from a future obligation ("verify no leftovers").
Both want the same thing, and the repo's forward rule is unconditional — *"the word 'verified'
in a contract must name the command that verified it"* (LESSONS.md 2026-08-28). An obligation
that names its command is a better obligation. Measured on batch-1 this costs nothing: every
obligation that fires is one a reader would agree should name a command.

**The sharpest sub-decision**, because it is the one that could have been got wrong: a witness
is what *established* a claim, never what the claim is *about*. `` `CLAUDE.md` `` is a subject;
`` `validate_doc_rot.scan_file_budget` `` is a witness. Collapsing them lets every claim cite
itself and pass — the detector would then be inert while rendering green
(`test_ii_a_named_callable_is_a_witness_but_a_bare_doc_name_is_not`).

### (iii) every cited `[#id]` / ADR / register id resolves live — **MET, with the honest limit named**

`check_cited_ids` + `load_task_rows`. `[#id]` resolves against **`tasks/`** (345 files, 208 open
rows), never `BACKLOG.md`. ADR ids resolve against `docs/decisions/ADR-*.md`; register ids
against `protocols/STANDING_RULINGS.md` headings. An absent `tasks/` **raises** (exit 2), it does
not report clean — `test_iii_absent_tasks_dir_raises_rather_than_reporting_clean`.

**THE LIMIT, stated first because it bounds the whole leg: `[#587]` cited for `[#608]`'s seam is
a LIVE, OPEN row. No liveness check catches it, and no strengthening of one ever will.** Same
theme, same story, same serialize-group, same file; only the title separates them. So the leg
does what LESSONS.md's forward rule asks — *"a contract citing an id must quote that row's title
beside it"* — in the two mechanical forms available:

- every resolved id's **title is echoed into the evidence line**, on passes as well as failures,
  so a freezer reads it beside their own prose;
- a citation whose **adjacent description shares no content word with the row title** is flagged.

That second leg is the one that reproduces the defect, and it is deliberately gated narrow —
see §3's false-positive log.

### (iv) declared do-not-touch set vs detector scope roots — **MET**

`check_do_not_touch` + `ratchet_scope_roots`, which **reads `silent_rule_detector._SCOPE_RULES`
and never restates it** — asserted by `test_iv_scope_roots_are_read_from_the_detector_not_restated`.
That is the design note's instruction and also the defect's own moral: batch-1's RATCHET preamble
*restated* the roots as `protocols/*.md` + `templates/*`, dropped the third, and reasoned from the
incomplete enum to a claim it labelled "verified".

Two sub-legs: a sentence claiming a scope root sits *outside* scope; and a contract whose own
`**Write-scope:**` lands inside a scope root while it claims the ratchet untouched. Fires only in
a ratchet context — `test_iv_does_not_fire_outside_a_ratchet_context` guards the narrowness.

### (v) the C-F `**Shape:**` mis-parse fixed, regression test included — **MET**

RED first, then fixed. RED evidence, before the change:

```
FAILED test_prose_shape_line_is_not_a_substrate_declaration      - assert 'one' is None
FAILED test_prose_shape_no_longer_masks_the_real_substrate_line  - assert 'one' == 'local'
FAILED test_prose_shape_does_not_fabricate_an_off_enum_refusal   - assert [Refusal(...)] == []
FAILED test_shape_declaration_requires_BOTH_backticks            - assert 'local' is None
4 failed, 28 passed
```

**The fix is a tighter grammar, and it is not a new one.** `_SHAPE_RE` now requires the
backticks that **layer 1 has always required** — `gen_lane_contract._SHAPE_LINE_RE` at
`scripts/gen_lane_contract.py:170` reads ``^\*\*Shape:\*\*\s+`(?P<shape>[a-z]+)` ``. The two
organs now agree on what counts as a declaration instead of disagreeing, which is what let a
hand-authored contract trip a gate on a word it had no way to know was reserved. The substrate
check was **not** weakened: `test_shape_declaration_requires_BOTH_backticks` guards the drift
direction back toward `` `? ``.

**The masking was the expensive half, and the fix removes it:** batch-1's contract now resolves
to `local` — its real substrate, which its own line 179 states as `**Real substrate: LOCAL**` —
where before `'one'` won the precedence race and that line was never read at all.

### (vi) batch-1's frozen contract reproduces the known defects — **MET**

`uv run --locked python scripts/preflight_contract.py <batch-1 contract> --predicates-only`
→ **exit 1**, `17/28 freeze-time predicate(s) resolved; 11 FAILED`.

| the recorded defect | reproduced as | evidence |
|---|---|---|
| C-G — off-repo artifact assumed on disk | `off-repo-input` ×1 | `**Basis:** the SDA-1 adversarial artifact` — "NO locator" |
| premise error 1 — "verified" for a ratchet scope root | `unwitnessed-claim` (line 142) | *"Ratchet untouched (ecosystem/ + code are outside its scope roots — verified, not assumed)"* |
| premise error 1's mechanism | `do-not-touch-scope` ×3 | claims `ecosystem/` outside scope; **and independently** L5's own write-scope `ecosystem/routing-table.yaml`, the exact file LESSONS records as scanned-not-exempt |
| premise error 2 — `[#587]` for `[#608]` | `cited-id` ×1 | resolves to `'P-1 — invert the journal-anchor check to a single pass'`, no shared content word with *"tiling seam surfaces"* |
| premise error 3 / C-F — `**Shape:**` → `'one'` | fixed in (v) | 4 RED tests, now green |

**The precision claim, which is the part worth checking:** across 13,213 B and every `[#id]` in
the file, **exactly one** id fires — the known-wrong one. Asserted by
`test_vi_batch1_reproduces_the_wrong_id_citation` (`assert fails == ["[#587]"]`).

Guarded in both directions: `test_vi_a_clean_contract_exits_0` proves this is not a
fail-everything (without it, every assertion above is satisfied by a predicate set that refuses
all input), and `test_vi_an_internal_error_exits_2_and_blocks` proves 2 stays distinct from 1.

---

## 2. THE FIFTH ACCEPTANCE CASE — asked for, and the answer is **NO**

The contract asked whether predicate (ii) flags lane F's restatement of the AGENTS.md byte
payload. **It does not, and the reason is structural rather than fixable by tuning.**

**First, the contract's premise is CONFIRMED** — verified, with the command:

```
$ wc -c -l AGENTS.md              →  107 lines   5539 bytes
$ git cat-file -p 43c18e9f:AGENTS.md | wc -c -l  →  107 lines   5539 bytes
```

So `CLAUDE.md` §2.68's **"103 lines, 5,270 B"** was false when written, and has been false since
`AGENTS.md`'s only content commit. The dispatch note is right.

**Why (ii) misses it:** predicate (ii) keys on the *word*. The false figure is asserted in a
sentence that uses no trigger word — *"A root `AGENTS.md` lands per ADR-115 §3.2's ruled shape:
103 lines (bound ≤120), 5,270 B, combined global+root payload 9,161 B = 28.0 % of the 32 KiB
cap"*. Nothing marks it as a claim that was checked. Predicate (ii) *does* fire on §2.68's
neighbouring `**Measured, not asserted:**` sentence — but that one is about the ratchet delta
(443 → 443), not the byte payload, so **counting it as a catch would be a false success report.**

**This is predicate (ii)'s honest recall ceiling: a bare number asserted without a
witness-claiming word is invisible to a word-triggered detector.** Filed as candidate C4 below.

---

## 3. FALSE POSITIVES FOUND AND KILLED — measured, not asserted

The first acceptance run returned **16 FAILs**; four were wrong. Each was fixed and each fix
carries a test, because an unrecorded tuning is indistinguishable from weakening the check.

| # | false positive | cause | fix | test |
|---|---|---|---|---|
| 1–2 | `register ADR-85` ×2 | `[A-Z]{1,2}-?[A-Z]?` eats `ADR-`, so every ADR was also looked up as a ruling | negative lookahead; ADRs keep their own leg | `test_iii_an_adr_is_not_looked_up_as_a_register_id` |
| 3 | `register W2` | `per W2/D5` is a **session-plan** id. `per`/`under` precede lane letters and plan steps as readily as rulings | dropped `per`/`under` from the marker set | `test_iii_a_session_plan_id_is_not_read_as_a_register_id` |
| 4–5 | `[#592]` ×2 | `[#592]-shaped` is a bare pointer — it describes nothing, so it cannot describe anything *wrongly* | gate on an adjacent-window description floor | `test_iii_a_bare_pointer_is_not_a_description_and_does_not_fire` |

Fixing #4 by narrowing the window then produced **two new** false positives (`[#584]`, `[#613]`),
where the agreeing word sat one comma past the window's edge. Resolved by splitting the two
spans — **narrow GATE (is there a description?), generous TEST (does anything in the sentence
corroborate it?)**. Final state: 11 FAILs, **zero known false positives**.

**Recall cost of fix #3, stated because it is real:** a bare `per Z-G3` — a genuine register
citation, and the spelling batch-1 actually uses — is **not** checked. Precision was chosen
deliberately: this organ is opt-in and ungated, so it has to be worth running, and a false
refusal on a lane letter is what gets a detector switched off.

---

## 3a. TERRA REVIEW — tally in body, and what was done about it

`codex exec --model gpt-5.6-terra` over the staged diff (not `/codex-review` — a mixed
doc/code diff kills that lane).

**Severity tally: CRITICAL 0 · HIGH 8 · MEDIUM 0 · LOW 0.**

**Six accepted and fixed; one accepted-and-improved-differently; one built, measured, and
reverted with the measurement recorded.** Every fix carries a test.

| # | terra HIGH | disposition |
|---|---|---|
| 1 | `_SHAPE_RE` unanchored — an *example* of the field masks the real declaration | **FIXED.** Anchored to line start with `re.M`, matching layer 1's anchoring as well as its grammar. `test_shape_declaration_is_anchored_to_line_start` |
| 2 | off-repo regex ignores POSIX-absolute and UNC paths — they pass silently | **FIXED.** UNC added; POSIX added **restricted to real filesystem roots**, because a bare leading `/` matches `/preflight`, `/lane-boot`, `/handoff` — this corpus's slash-commands. Both directions tested |
| 3 | any backticked prose counts as an input locator | **FIXED.** A locator must look like a path (slash or extension). Otherwise `` `SDA-1 artifact` `` discharges C-G by adding punctuation |
| 4 | witness accepts arbitrary multi-word backticks — *"verified in `the artifact`"* passes | **FIXED, and the most material of the eight.** A command must begin with a runnable verb, or carry a path/script/flag. The old rule handed every author a two-word escape and rendered green while checking nothing |
| 5 | id-identity only reads words *after* the id | **BUILT, MEASURED, REVERTED — see below** |
| 6 | bare `per Z-Q9` unparsed, contradicting "every cited register id resolves" | **FIXED BETTER than terra proposed.** `per`/`under` readmitted, gated on section letters **read from the live register**: `Z` is a live section so `per Z-Q9` is now caught; `W` is not, so `per W2/D5` stays alone. Recall recovered without the false positive |
| 7 | ratchet-context regex misses "silent rule detector" | **FIXED** (`silent[_ -]rule`) |
| 8 | directory matching is case-sensitive and ignores suffix/depth rules | **FIXED, and it was the most substantive.** The write-scope leg now calls `silent_rule_detector._in_scope` itself, so `ecosystem/README.md` is correctly **not** in scope (only `*.yaml` is) and nested `templates/**.md` correctly **is**. Root-name matching is casefolded, because the detector folds |

**On #5 — the one I did not take, with the evidence.** Terra is right in principle: a
description sitting *before* the id is not gated, so `the tiling seam at [#587]` would pass.
I built the both-sides variant and ran it against the live corpus: **it reintroduced a false
positive.** Batch-1's *"the agreement check's code home per the `[#592]` pattern"* is an
**analogy citation** — the preceding prose describes the lane's own work, not the row, so
nothing in it can be expected to share the row's title. Text *after* an id is usually an
appositive naming the row; text *before* it is usually the sentence's own subject. **This
organ is advisory and ungated, so a measured false positive costs more than a hypothetical
false negative.** The gap stays, named in the code, rather than being closed at the price of
trust.

One terra round was run, not the ~12 a new-code terra loop typically needs. **This is a
recorded deviation, owner = integrator**: further rounds would likely find more, and the
findings above show the first round was productive rather than cosmetic.

---

## 4. SELF-APPLICATION — this lane's own frozen contract

Run against `NB2-LANE-G-591-preflight-predicates.md`: **5 FAILED, 12/17 resolved**, all
`unwitnessed-claim`. Including, fairly, line 126 — *"The dispatch-time measurement is count:
443, files: 61, detector silent-rule-v5"* — a measurement I did re-run and the contract did not
name the command for. The predicate is right about its own commissioning document.

One borderline: line 34 fires on the **section heading** `## RESOLVED LOCATORS (verified at
dispatch …)`. A heading asserting "verified" is a claim, so the fire is defensible, but headings
may deserve their own rule. Reported, not silently tuned away — candidate C5.

---

## 5. GATE STATE

| gate | result |
|---|---|
| targeted tests | **116 passed** (`test_preflight_freeze_predicates.py` 46 new · `test_preflight_contract.py` · `test_validate_substrate.py` +6) |
| `ruff check` (4 changed files) | **All checks passed!** |
| `audit.py health` | **`health: OK`**, exit 0 (run twice — before and after the terra round) |
| ratchet, pre-first-commit | count **443**, files **61**, `silent-rule-v5` |
| ratchet, pre-last-commit | count **443**, files **61**, `silent-rule-v5` — **delta 0** |
| full suite | **not run** — targeted only per `[#528]`; runs once at integration |

**Inherited, not mine** — 10 `consumer_at_landing` WARNs naming the batch-2 lane-contract files
(`NB2-CLOUD-*`, `NB2-LANE-*`). Evidence they pre-date this lane:
`git log --oneline -1 -- docs/audits/2026-08-28-technical-batch2-launch-contracts/` →
**`e23e001d`**, the batch-2 dispatch commit. `health` is `OK` regardless — these are WARNs.

---

## 6. CANDIDATE FILINGS — reported, never filed (lane D is the batch's `tasks/` writer)

- **C1 · Arm the predicates as a gate.** The contract instructed shipping the organ + CLI and
  reporting the arming as a candidate. A pre-commit or freeze-time hook over lane contracts has
  its own roster and doc consequences (`ARCHITECTURE.md` Ch2, `CLAUDE.md` §9) — both outside this
  lane's write-scope. Suggest the `check_preflight_backlog_ids` precedent: **WARN-tier first,
  hard-gate after two windows at zero false positives.**
- **C2 · A premise note on this lane's own contract (a fifth instance of the class).** The
  contract justifies resolving `[#id]` against `tasks/` because `BACKLOG.md` *"is a one-line
  generated VIEW and would let the check pass on an empty set"*. **Measured: `BACKLOG.md` carries
  208 `- [#id]` rows** (`grep -c -E "^- \[#[0-9]+\]" BACKLOG.md`), so the check would not pass on
  an empty set. **The instruction is right; the stated reason is not.** The real reason is
  better: `tasks/` separates *never allocated* from *closed*, which `BACKLOG.md` conflates into
  one negative — and that separation is exactly what leg (iii) needs.
- **C3 · `CLAUDE.md` §2.68 carries a false measurement.** "103 lines, 5,270 B" against a live
  **107 lines / 5,539 B**, false since `43c18e9f`. `CLAUDE.md` is outside this lane's
  write-scope; handed to the integrator as a correction candidate. Note it is inside the
  ratchet's `protocols/`-adjacent zero-headroom regime only if the edit touches a hub region —
  measure before editing.
- **C4 · Predicate (ii)'s recall ceiling** (§2): a numeric claim asserted with no
  witness-claiming word is invisible. A sibling predicate over *bare numbers adjacent to a
  file/byte/line noun* would reach it, at an unmeasured false-positive cost. Worth a decision,
  not worth guessing tonight.
- **C5 · Should a section heading be a claim site?** (§4, line 34.)
- **C6 · `preflight_contract` now has two id-resolution sources** — `_open_backlog_ids`
  (BACKLOG.md, for the existing `backlog-id` locator leg) and `load_task_rows` (`tasks/`, for the
  new leg). Both are correct *for their own question* and the docstrings say which is which, but
  a future reader will ask. Candidate: converge, or record the split as intentional.

---

## 7. DECISIONS TAKEN UNDER THE BUDGET

Standing rulings applied silently. Nothing hit the four ask-conditions (curated baseline /
rule-vs-ruling / no-ruling fork / out-of-scope path), so **no operator question was needed**.
Decided per contract defaults:

1. **Home split** (§0) — taken under the contract's own parenthetical permission.
2. **No `tests/fixtures/` copy of the batch-1 contract.** The contract offered it "if the test
   needs a stable input". It does not: the file is an **immutable audit artifact**, so it cannot
   drift, and a second copy would be a second thing to keep true. The test reads it from the tree
   and **FAILS rather than skips** if it is absent (Z-G4) — `batch1_claims` fixture.
3. **`--freeze` / `--predicates-only` are opt-in flags; `verify()` is untouched.** Existing
   callers and all pre-existing tests keep their behaviour; the new legs are additive.
4. **`Report` gained a `label` field** so the locator legs and the predicates do not both claim
   to be counting "locator claims" in one run.
5. **stdout/stderr re-encoded to UTF-8 in `main`.** The predicates quote contract prose, which
   carries `≠`, em dashes and arrows; on the cp1252 console that was an `UnicodeEncodeError` at
   print time — i.e. the tool crashed on exactly the contracts it exists for, and a crash is
   indistinguishable from an internal error. Fixed in the tool rather than by demanding
   `PYTHONUTF8=1` at every call site.
6. **`docs/audits/README.md` deliberately left stale.** This packet is a new `docs/audits/` file;
   clause 4 reserves generated-surface regeneration for the integrator, and `[#590]` narrowed the
   index hook so a batch lane must not regenerate it.

---

## 8. DEVIATIONS, each with an owner

| deviation | owner | why |
|---|---|---|
| **No `JOURNAL.md` entry**, and the session-end Stop hook is **declined explicitly** | lane G | Contract clause 1: a batch lane never journals; the integrator writes one anchor for the whole queue. The hook is **advisory in full** since the ADR-85 amendment 2026-08-03 §A5; the hard leg is `block-unanchored-push` at pre-push, and **a lane does not push**. Declined with the reason, not silently ignored. |
| **No self-merge and no merge command named** | lane G | Clause 2. The queue order is frozen; naming a merge invites it out of order. |
| **No `tasks/` write, no row closure** | lane G | Clause 3. Six candidates in §6 for lane D / the integrator. |
| **Full suite not run** | integration | `[#528]` — targeted per lane, full suite once on the merged result. |
| **`ecosystem/doc-counts.md` not regenerated** despite a new test file | integrator | Shared clause A5. `audit.py health` is `OK` as-is, so nothing is wedged. |

---

## 9. COMMITS ON THIS BRANCH, in order

1. **`8e452b3d`** — `feat(preflight): four freeze-time contract predicates + the C-F Shape
   mis-parse fix [#591]`. The whole organ: `scripts/preflight_contract.py`,
   `scripts/validate_substrate.py`, `tests/test_preflight_freeze_predicates.py` (new),
   `tests/test_validate_substrate.py`. 4 files, +1283 / −7. All pre-commit gates passed, none
   skipped under protest.
2. **this packet** — `docs/audits/2026-08-28-technical-nb2-g-packet.md`, its own commit.

**No generated-surface commit was needed.** Clause 4 anticipated one being forced by a gate;
none was. `docs/audits/README.md` is deliberately left stale for the integrator ([#590]
narrowed the index hook precisely so a batch lane does not regenerate it), and
`audit.py health` is `OK` with it stale.

**STOPped.** Branch is `worktree-lane-g-591-preflight-predicates`, ready for the integrator's
frozen queue.
