# Lane `w-638-proof-layer-skipif` — end-of-lane record: the guard key in the evidence, the four rulings, and the re-stamp that is not owed

Consumers: `[#638]`

> Batch W, lane W-3. Contract:
> `docs/audits/2026-09-10-technical-batch-w-launch-contracts/LANE-w-638-proof-layer-skipif.md`.
> Branch `worktree-lane-w-638-proof-layer-skipif`, base `3acca581`, commits `e89e8312`
> and `16c4b5be`. Every number below was measured in this worktree at the commit it is
> attributed to; none is transcribed from the contract, from the `[#638]` row, or from
> lane C-1's report.

---

## 0 · Substrate — the lane ran LOCAL, and the receipt gate is moot

The contract froze this lane CODESPACE and was dispatched as one on 2026-09-10. That run
produced no work: no `worktree-lane-w-638-proof-layer-skipif` branch existed locally or on
origin, and the container was shut down. **AMEND-BATCH-W-005 AW5-3** re-cut the substrate to
LOCAL under PLAYBOOK Ch8 Layer-1 Q1 — a gate-dependent result is not cloud — and the lane ran
on the operator's Windows primary in the worktree above.

Three consequences, recorded because each supersedes a frozen section:

1. The `## Dispatch` block's `Shape: codespace` and its `Dispatch-Codespace` line are
   superseded. There was no container and no ssh transport.
2. The `## Receipt gate` section has no subject. **No `receipt.json` was written** — one at
   the repo root blocks a commit here — and none was pulled back.
3. AW-4's receipt half ("the receipt is a RED list, never a verdict") likewise has no
   subject. **Its other half is untouched and was honoured:** this artifact reports
   measurements, not an acceptance verdict, and FR-8
   (`docs/intake/2026-09-09-tech-window-close-rulings.md:83`) leaves the verdict to the
   integrator's re-derivation on the primary. §4 is written as the RED list AW-4 asks for.

Everything else the contract froze — model, mode, the V-2 budget, the footprint, the frozen
intent and the Done-when — was unchanged and binding. The branch prefix is unchanged too: a
codespace lane and a local lane both commit on `worktree-<slug>`.

## 1 · The premise, re-measured rather than inherited

The contract's anti-pattern section names the population `[#638]` was filed against: *"243
guards, 247 live, 0 dropped"*, stamped at `2d531321`. Re-measured on this lane's base
`3acca581` before any edit:

```
live 247 / baseline 243 / new 4 / drained 0
```

The four NEW keys, verbatim from the scanner:

```
test_review_artifact_coverage.py::test_an_unrelated_handback_does_not_launder_a_merge
test_review_artifact_coverage.py::test_handback_artifact_supplies_both_linkage_and_tally
test_review_artifact_coverage.py::test_handback_artifact_with_review_none_is_not_coverage
test_review_artifact_coverage.py::test_handback_artifact_without_a_review_token_is_not_coverage
```

The premise holds exactly. Nothing was refuted, so no Q10 PAUSE was owed.

## 2 · Done-when (a) — the evidence carries the guard KEY (`e89e8312`)

**The defect was one layer in from where it looks.** `check_proof_layer` already emits one
Finding per guard, precisely so the `#147` register can disposition them one at a time — its
docstring says so. But the register matches on a **substring of the evidence**
(`audit.py::_match_disposition`), and every field the evidence line carried — module, scope,
tool, gated-test count — is shared by two function-level guards in one module. The four
findings were therefore **one distinct string, rendered four times**. One Finding per guard
buys nothing when the four Findings are indistinguishable.

**RED first (ADR-108 §B).** Three witnesses were added to `tests/test_proof_layer.py` and run
before any change to `scripts/proof_layer.py`. All three failed, each naming the real defect:

```
test_two_guards_in_one_module_do_not_render_byte_identically  FAILED  assert 1 == 2
test_each_finding_carries_the_guard_key_the_baseline_lists    FAILED  assert 0 == 1
test_a_module_level_guard_carries_its_module_scoped_key       FAILED  key not in evidence
```

**The fix.** `ratchet_findings` now names `Guard.key` — `module::target`, the ratchet's own
identity, not a second handle invented at the reporting surface. The consequence is the one
the row asked for: a disposition author and `ecosystem/proof-layer-baseline.json` quote the
**same** token, so a register entry that stops matching has stopped matching the guard it was
written for. Module-scope guards are keyed through the same grammar (`<module:tool>`), so
neither scope is dispositionable only by luck.

Measured on the live tree, before and after:

```
before   4 findings, 1 distinct evidence string
after    4 findings, 4 distinct evidence strings, each naming its own test
```

`ecosystem/doc-counts.md` was regenerated in the same commit — `5723 -> 5726 collected`,
exactly the three witnesses. That claim is a commit-tier block, not a ship-tier WARN, so it
could not be deferred to the integrator.

## 3 · Done-when (b) — the four guards, ruled on their merits (`16c4b5be`)

**The question the contract poses is live, not rhetorical**, and `scripts/proof_layer.py`
poses it about itself: *"a guard on `git`, `grep` or `pwsh` may still be self-policing in a
module whose subject IS that tool"*, and *"a guard on this list is a QUESTION, not a
verdict"*. `tests/test_review_artifact_coverage.py`'s subject **is** git-derived data, so the
four had to be answered rather than counted.

**Ruled: ROUTE OUT — all four, on two grounds.**

**Ground 1 — git is this fixture's scaffolding, not these four properties' subject.** What
each of the four pins is the **token grammar of a persisted handback**: whether a missing
token, `review=NONE`, or an unrelated artifact counts as coverage. `git` stands up a repo
with a merge in it so the grammar has somewhere to be read from; it is not what is measured.
That is the merits difference from the sweep's §9.2 exemplar, which `proof_layer` calls
load-bearing and CORRECT — there the property genuinely cannot exist without the tool. Here
it can, and the tool's absence decides only whether the proof **runs**. Three of the four are
refusal properties: they pin that the leg still WARNs. A refusal proof that can go quiet on
the machine where the refusal would matter is the family-3 defect stated exactly.

**Ground 2 — in this repo a machine without `git` is a broken machine, not a supported one.**
`.dev-knowledge` is a git-governance hub: every gate is a git hook, `audit.py` shells out to
git, and the checkout these tests run from cannot be obtained without it. The only live
effect the mark can have here is to convert that breakage into a silent green — the outcome
`[#596]` exists to refuse. Unmarked, the four raise `FileNotFoundError: git` from `_run`:
loud, named and attributable, rather than a dot in a summary nobody reads line by line.

Guard by guard, each ruled, each on the same two grounds:

- `test_handback_artifact_supplies_both_linkage_and_tally` — **ROUTE OUT.** Pins that a
  persisted handback is first-class coverage. The property is the artifact's grammar.
- `test_handback_artifact_without_a_review_token_is_not_coverage` — **ROUTE OUT.** A refusal
  property; the one most damaged by a silent skip.
- `test_handback_artifact_with_review_none_is_not_coverage` — **ROUTE OUT.** Refusal
  property; `review=NONE` is a token, not a git fact.
- `test_an_unrelated_handback_does_not_launder_a_merge` — **ROUTE OUT.** Refusal property;
  laundering is the failure mode `[#480]` was filed against.

**The thirteen older guards in the same file keep the mark, and that is a ruling too.**
Symmetry is not a merit. They are the pre-existing population `ratchet_findings` records as
the reason its tier is WARN, they sit outside this lane's declared footprint, and ruling them
is a separate act with its own evidence. The ratchet drains as designed — its own docstring's
*"a NEW guard surfaces by name even while an old one drains"*. The asymmetry is recorded **in
the test file, above the tests it governs**, so the next reader does not "restore" the mark
for tidiness.

**What was not done, deliberately.** No `#147` register entry was written: any token narrow
enough to be true of one of these four was true of all four **and** of the next guard added to
that file, which is the whole-Finding masking the register's own contract forbids and the
entry lane C-1 refused to write. No guard was deleted to move a count — the four proofs still
run, and they run unconditionally now.

## 4 · Done-when (b), second half — the prepared re-stamp, with the measured count PRINTED

The Done-when offers two terminations: *"`ecosystem/proof-layer-baseline.json` is re-stamped,
**or** the properties are routed out from behind the guard"*. §3 took the second. The Closure
leg's matching right-hand side is *"the properties routed out and the baseline unchanged"*.

**Measured at `16c4b5be`, printed rather than asserted:**

```
scanner:   243 environment-conditional guard(s), all at baseline; 10 self-policing
live       243
baseline   243   (measured_at 2026-08-27, measured_at_sha 2d531321, detector proof-layer/v1)
new        0     []
drained    0     []
```

**`ecosystem/proof-layer-baseline.json` is UNCHANGED by this lane** — not one byte. The four
keys that were over the line are gone from the live population because the guards they named
are gone, so the baseline's 243 keys are exactly the live 243. **No re-stamp is owed, and
none was taken.** The V-2 escalation class (a) *curated-baseline touches* was therefore never
entered, which is the second reason route-out was preferred over accepting the four: the
re-stamp branch would have required an escalation this lane could not make.

**AW-4 is satisfied on its surviving half.** The lane took no acceptance verdict from its own
reading. The three numbers above are a measurement; the integrator re-derives them on the
primary before merge, per FR-8. If that re-derivation disagrees with the block above, the
integrator's number governs and this lane's is the one to discard.

The command that reproduces it:

```
uv run --locked python scripts/proof_layer.py
```

## 5 · Closure ledger

| Closure leg (frozen) | Left-hand side | Right-hand side, at `16c4b5be` |
|---|---|---|
| `ratchet_findings` evidence carries the guard KEY | no | **yes** — `Guard.key`, three RED-first witnesses |
| the four guards | undispositionable | **ruled on their merits, each ruling recorded** — §3, and in the test file |
| baseline | stamped at `2d531321` | **routed out, baseline unchanged**; measured count printed in §4 |

Anti-patterns, each checked rather than asserted: no `#147` entry matching the module (none
written at all); no guard deleted to move a count (four proofs still run, now
unconditionally); no re-stamp against an unagreed population (no re-stamp).

## 6 · Decision budget — 2 forks, 2 spent, 0 escalations

- **Fork 1 — the guard-key evidence format.** Decided: carry `Guard.key` itself, as a labelled
  `Guard key: …` clause inside the existing sentence. Rejected: a new reporting-surface handle,
  which would have let the register and the baseline drift apart; and replacing the leading
  module name with the key, which reads wrongly for module scope and loses nothing by staying.
- **Fork 2 — route out vs re-stamp.** Decided: route out, on the two grounds in §3. The merits
  are genuinely balanced on Ground 1 alone; Ground 2 is repo-specific and decides it. Route-out
  also leaves the curated baseline untouched, so the decision stayed inside the budget instead
  of becoming escalation class (a).
- **No third fork**, so no commit-and-STOP was triggered by the budget. The lane stops at the
  end of its Steps, as contracted.

## 7 · Residual — what the integrator owes

1. **Re-derive §4 on the primary** before merge (FR-8). The expected reading is
   `live 243 / baseline 243 / new 0 / drained 0`.
2. **Regenerate `docs/audits/README.md`** once on the merged result
   (`gen_audit_index.py --write`, `git add` first). This lane deliberately left the index
   stale — `audit-index-freshness` was narrowed by `[#590]` and regenerating in-lane is the
   wrong act, not a missed chore. This artifact is the file that makes it owed.
3. **Re-run `gen_doc_counts.py --write` on the merged tree.** `5726` is true of this branch;
   a sibling W lane that adds or removes tests moves it.
4. **The JOURNAL entry is the integrator's surface** (`STANDING_RULINGS` P-1); this lane wrote
   none.
5. **Batch X's W-6 unblocks on this lane's merge, not on a prediction** — A7-1's condition is
   *`skipped_gates`' writer is W-3's output*. Read it off `main`'s first-parent spine. This
   lane did not widen scope toward W-6's `tasks/` frontmatter keys, and nothing here writes
   one.

## 8 · One honest limit

Routing four guards out does not make `tests/test_review_artifact_coverage.py` unskippable —
thirteen guards in that file still carry `requires_git`, and the module-wide property "this
file's proofs run wherever the suite runs" is **not** established by this lane. What is
established is that those thirteen are now individually dispositionable, which is what
`[#638]` asked for and the precondition for ruling them at all. They remain pre-existing debt,
visible by name in `ecosystem/proof-layer-baseline.json`, and the ratchet reports any
fourteenth by its own key on the day it appears.
