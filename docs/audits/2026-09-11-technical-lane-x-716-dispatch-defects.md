# Lane `lane-x-716-dispatch-defects` — end-of-lane packet

**Consumers:** `[#716]`, `[#717]`, `[#718]` — the three rows this lane carries a RED-first
witness and a fix for. Contract of record:
`docs/audits/2026-09-11-technical-batch-x-launch-contracts/LANE-x-716-dispatch-defects.md`
(batch X wave 1, slot 5 per `AX14-1`).

**Date:** 2026-09-11 · **Branch:** `worktree-lane-x-716-dispatch-defects` · **Base:** `0be08b3c`
· **Mode:** execute · **Model/effort:** opus / high, as the contract's routing row declares.

---

## 1. What changed

Four commits, each one defect, each RED-first. Branch `main..HEAD`:

```
acef1832  fix(worktree): [#716] a lane's base equals main HEAD at dispatch, asserted by a test
0040dc60  fix(gen-lane-contract): [#717] render -Model from the routing row, and widen the checker
63e1d8de  fix(gen-lane-contract): [#718] the generator writes where the verb reads -- ONE key
3b2d4455  docs(batch-x): carry AX12-1's clauses into [#716] [#717] [#718], this lane's own rows
```

```
.claude/settings.json               |   4 +
scripts/gen_lane_contract.py        | 156 +-
scripts/worktree_seed.py            | 211 +
tasks/716-*.md                      |   2 +-
tasks/717-*.md                      |   2 +-
tasks/718-*.md                      |   2 +-
tests/test_gen_lane_contract.py     | 359 +-
tests/test_worktree_seed.py         | 181 +
8 files changed, 900 insertions(+), 17 deletions(-)
```

### `[#718]` — the generator writes where the verb reads

`_default_out_dir()` returned `Path.cwd()`; `Dispatch-Lane` takes a bare filename and resolves
it against the prompts root. Two literals, both individually correct about the root they named,
which is why review never caught it — there was no wrong line to find. Batch W wrote six
contracts to `to-cc/` and all six were refused.

The fix is an **identity, not an agreement**: `gen_handoff.transport_root()` already holds the
reader's resolution rule (`CLAUDE_PROMPTS_DIR`, documented `~/Downloads` fallback, `None` when
unresolved), already in the tree and already tested. It is imported **by name**, so the module
has no second literal to drift from.

**The refusal survives the fix**, which the row asks for in as many words. An unresolved prompts
root raises rather than quietly writing to the cwd: six refusals cost six dispatches, six
contracts silently read from a stale location would have cost six lanes running against the
wrong text. `--out-dir` stays an operator override, with its own test — the one key is the
default, not a jail.

Live confirmation the key is the right one: on this machine `transport_root()` resolves to
`H:\My Drive\CLAUDE PROMPT DIR`, the directory this lane's own contract was read from.

### `[#717]` — the launch line is rendered from the `Model` row

`dispatch_command` emitted slug, file and `-Effort`; `Start-DispatchLane`'s `-Model` defaults to
`opus`. Neither half is wrong alone. Together, a contract declaring `sonnet` and dispatched by
its own carried line ran at `opus` — silently, and in the expensive direction.

**The checker widened in the same change**, per Done-contract clause 2. `_DISPATCH_LINE_RE` was
anchored with no `-Model` alternative, so rendering the model without widening it would have
turned every emitted contract RED at `lane-contract-check`. `-Model` is admitted **optional** —
every contract frozen before this carries a line without it — and where present it must **agree**
with the routing row, the same conjunction `-Effort` already gets, plus an enum check.

The contract's explicit step-3 re-check, run against the real corpus rather than a fixture:

```
gen_lane_contract.py check docs/audits/2026-09-11-technical-batch-x-launch-contracts/*.md
  LANE-w-684-pretooluse-guard-root-prime.md  OK
  LANE-x-664-delivery-spine.md               OK
  LANE-x-689-conductor-e.md                  OK
  LANE-x-692-decision-coverage.md            OK
  LANE-x-716-dispatch-defects.md             OK
  LANE-x-734-retire-stage.md                 OK
```

### `[#716]` — a lane's base equals `main` HEAD at dispatch

`worktree.baseRef` unset → `fresh` → `origin/main`. This lane reproduced it: branched at
`78d99d55` while local `main` stood at `0be08b3c`, **seven commits behind**.

The setting's shape was **verified against the shipped Claude Code 2.1.268 binary**, not
inferred from its display name:

```
if(w.worktree?.baseRef!==void 0)I.push("worktree.baseRef")
baseRef:Y(["fresh","head"]).optional().describe("Which ref new worktrees branch ...")
```

So the key is **nested** under a `worktree` object, `worktree.baseRef` is only how it is *named*
in messages, and the enum is exactly two values. A flat `"worktree.baseRef"` key would have been
ignored in silence — this row's own failure mode one layer on. Both facts are pinned by tests.

Fix: `.claude/settings.json` declares `worktree.baseRef = "head"`, with the reasoning inline.
The predicate lives in `scripts/worktree_seed.py::base_ref_verdict` — the existing
worktree-provisioning organ, not a new one.

---

## 2. The finding this lane did not expect

**A peer's push turned the RED-first witness GREEN with nothing fixed.**

The first witness compared two SHAs: does the base equal `main` HEAD right now? It was honestly
RED at step 0 — `origin/main` seven commits behind. Hours later a concurrent seat pushed `main`,
`origin/main` caught up, and the same test passed **under the same unset configuration**. Run in
that window and taken at face value, it would have certified the defect closed.

A witness that someone else's push can turn green is measuring push timing, not configuration.
So `fresh` now reports `holds=False` **unconditionally**, with a separate `coincidental` flag
when the SHAs happen to agree — the two facts stay separately readable rather than one
swallowing the other.

The reasoning is the row's own, applied to an axis it did not foresee. `[#716]`'s Done-when
already refuses accidental satisfaction — *"so a dispatcher on a non-`main` branch cannot
satisfy it accidentally"* — and a well-timed push is the same accident from the other side. It
is also what makes the row's other requirement satisfiable at all: a witness that must *"FAIL
against today's unset configuration"* cannot be a bare SHA comparison, because an unset
configuration compares equal whenever `main` happens to be pushed.

The verdict names **which** failure mode fired, because the two want opposite repairs: `fresh`
failing means push or change the setting; `head` failing means move the dispatcher and **do not**
change the setting.

---

## 3. Judgment calls — decided per contract default, reported not asked (V-2)

None of these reached the three escalation classes (curated-baseline touch, rule-vs-ruling
conflict, fork with no standing ruling), so each was decided and is recorded here.

**(a) The step-0 sync's retirement surface does not exist as the clause assumes.** The Done-when
says the sync is *"retired from the lane-contract template only in the same change that makes
that test green"*. Grepped for `fetch origin` / `sync before anything else`: the region is
**hand-authored into each frozen contract** and appears in none of `templates/prompt-template.md`
v1.15, `.claude/commands/lane-boot.md`, `protocols/PLAYBOOK.md`, or
`gen_lane_contract.render_contract`. The six contracts carrying it are immutable audits. So
there was no template line to delete, and deleting nothing would have discharged the clause
vacuously.

Decided: make the retirement **mechanical** rather than editorial. `render_contract` now emits
the step-0 region conditioned on the very predicate the row's test asserts — emitted while the
property is unheld, absent once it holds, and back if the setting is ever unset again.
Retirement by mechanism rather than by an editor remembering, and strictly stronger than a
deletion, which retires it once. `render_contract` stays **pure** (the flag is a spec field set
by `cmd_emit` from the live verdict), asserted by its own test.

Live proof, from one `emit` run after the fix:

```
gen-lane-contract: step-0 sync region: retired -- worktree.baseRef='head' resolves the base
    to .dev-knowledge:HEAD (the dispatching checkout), which is at 0be08b3c -- the same
    commit as main HEAD
gen-lane-contract: dispatch with: Dispatch-Lane lane-z-999-smoke LANE-z-999-smoke.md
    -Effort high -Model opus
```

All three defects visible in two lines.

**(b) Settings are read from the checkout being asked; refs from the primary.** Configuration is
a **tracked property of a tree** — the question is whether the tree that lands is configured
right — and reading the primary's copy would make it impossible for a lane to witness its own
fix, since the primary carries the pre-merge value until integration. Ref state is a property of
the machine at the dispatch act, so it comes from the primary. **The honest limit, stated in the
docstring and repeated here:** a lane's `settings.json` is the tree's *claim*; it governs real
dispatches only once merged to `main`.

**(c) `-Model` is optional in the dispatch grammar, and ordered after `-Effort`.** Mandatory
would redden the entire pre-`[#717]` corpus. A reversed-order line is refused rather than guessed
at, which is the posture the rest of the module already takes.

**(d) An existing test reported a changed premise rather than going vacuous.**
`test_a_generated_contract_without_its_command_line_fails` deleted a **hardcoded** dispatch line;
with `-Model` on it the literal stopped matching, so the deletion deleted nothing. Its own *"the
mutation did not bite"* guard caught that. The line is now built from `dispatch_command` itself,
so the next flag cannot rot it — the class is closed rather than today's spelling re-typed.

---

## 4. `AX` clauses — discharged, and one reported to its owner

- **`AX12-1`** — discharged in the lane's **first commit** (`3b2d4455`), the AW-2 / `[#680]`
  pattern: every clause addressed to this lane is written into the row it binds.
- **`AX9-4`** (exists-before-build) — **discharged by reuse, not by a quote excusing a build.**
  This lane creates no organ, script, hook or doc. `graph_queries.py process-list --render` was
  run live and returned `scripts/gen_lane_contract.py` (triggered by `.pre-commit-config.yaml`),
  `scripts/gen_handoff.py` (triggered by `scripts/assemble_paste.py`) and
  `scripts/worktree_seed.py` (no trigger; ON-DEMAND-BY-OPERATOR, invoked by `/lane-boot`).
  All three fixes land inside one of them.
- **`AX7-5`** — satisfied by construction once `[#717]` lands; stays in force until the row is
  closed, which is the operator's act.
- **`AX4-1`** (floor declaration) — **REPORTED, NOT FILED, and the owner is `X1-1`.** Measured:
  **zero** `tasks/*.md` rows carry a `floor:` key, and `ecosystem/parity-surfaces.yaml` carries
  no lane-contract or dispatch surface. AX4-1 names the `decision_coverage` lane (X1-1) as owner
  and the parity registry as carrier. Adding an unvalidated frontmatter key ahead of its carrier
  would put these rows outside the ADR-66 schema `validate-backlog` gates. **This lane declares
  its floor in prose: `floor: MUST`** — all three defects sit in the deployed methodology
  corpus's own generator, and every consumer that dispatches a lane inherits them. Per the
  contract, a clause naming a row this lane did not file is reported rather than acted on in
  someone else's registry.

---

## 5. Open items for the integrator

1. **`ecosystem/doc-counts.md` — owed regeneration.** This lane adds tests, so the
   `pytest_collected` claim moves (measured at the first bypass: file 5752 / actual 5756, and
   further since). `SKIP=doc-counts-pytest-freshness` was declared in each affected commit body.
   The file is a **generated index**, and this contract reserves index regeneration to the
   integrator (Q1). One named hook per commit, never `--no-verify`.
2. **`ecosystem/organ-index.md` — owed regeneration, and the drift is NOT this lane's.**
   `generate_organ_index.py --check` reports exactly one delta: `65 → 64 organs`, removing
   ``| `/override` | command | ... | RETIRED |``. `/override` was deleted by `5e17ecd7`
   (*"feat([#683]): remove /override"*); the file is gone from disk and the generated index on
   `main` still carries its row (`git show main:ecosystem/organ-index.md | grep -c override` →
   `1`). This lane merely made the file-filtered hook **fire**, by staging
   `.claude/settings.json`. Regenerating here would pull an unrelated `/override` removal into
   this lane's diff — the coupling "no index regeneration" exists to prevent. Run
   `generate_organ_index.py --write` at the merge; it closes `[#683]`-era drift.
3. **`docs/audits/README.md` — deliberately left stale.** `audit-index-freshness` does **not**
   fire for a new `docs/audits/*.md` ( `[#590]` narrowed its `files:` on 2026-08-26, after the
   index turned up in six of the last seven conflicted merges). Leaving it is the correct act,
   not a missed chore — named here so the owed regen is not invisible. `gen_audit_index.py
   --write` at the merge, `git add` first.
4. **`.claude/settings.json` takes effect at the merge, not before** — the primary's copy is
   what a real dispatch reads.
5. **Five pre-existing REDs in `tests/test_gen_handoff.py`**, reported rather than absorbed:
   `test_dogfood_no_probe_row_carries_an_answer_value` and
   `test_dogfood_generated_bundle_has_no_failing_probe` (both `assert 15 == 13`),
   `test_epic_bundle_has_no_failing_probe` (`assert 6 == 5`),
   `test_suffixed_bundle_probes_resolve_against_their_own_directory`,
   `test_funnel_health_renders_no_unavailable_against_the_live_repo`. Probe-roster / live-state
   drift. **Not this lane, proven rather than argued:** this branch's whole delta from `main` is
   eight files, and `tests/test_gen_handoff.py` references none of them — no reference to
   `tasks/` and none to `gen_lane_contract`, grepped.
6. **Three rows stay OPEN.** `[#716]`, `[#717]` and `[#718]` each have their Done-when satisfied
   and a witness that bites, but closure is the operator's act, not a lane's.

---

## 6. Verification

- `tests/test_gen_lane_contract.py` + `tests/test_worktree_seed.py`: **184 passed** (`-n 0`).
- `ruff check scripts/ tests/`: **All checks passed.**
- Each fix is preceded by its RED, quoted verbatim in the commit that fixes it — three witnesses,
  one per defect, each failing against the code it was written for.
- Full-suite cadence is the integrator's (`CLAUDE.md` §4, `[#528]`: a lane runs the targeted
  tests for its diff; the full suite runs once, at integration). Item 5 above is what a full run
  from this tree carries in.
