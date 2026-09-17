# Lane ab-694 — a refuted premise corrected in place, the GO-file half of `[#685]`, and AX9-5's metric

**Lane:** `lane-ab-694-cost-telemetry` · **Branch:** `worktree-lane-ab-694-cost-telemetry` ·
**Batch:** AB (`docs/audits/2026-09-16-technical-batch-ab-manifest.md`, amendment 1) ·
**Date:** 2026-09-16

Consumers: [#694] [#685] [#843]

## 1 · Premise — refuted, and the operator's ruling on what happens next

**Contract identity.** `sha256` of the frozen contract at
`H:\My Drive\CLAUDE PROMPT DIR\LANE-ab-694-cost-telemetry.md`:
`08ffb7150c969a390ef8d6c02b31b9b097e22f78f6d32a33272307db3ed1e294`. Matches the pin in
`docs/audits/2026-09-16-technical-batch-ab-manifest-amendment-1.md` line 38 exactly.

**The contract's premise — LEDGER F6's "four modules unwired" — is REFUTED.** Checked against
`main`, not carried from the roster digest: `scripts/gen_trend_dashboard.py`,
`scripts/window_metrics.py` and `scripts/failed_set.py` were already DELETED by
`lane-x-664-spine-armed` (`c9ea3b07`, `3a380fd8`, both ancestors of `main` — confirmed by
`git merge-base --is-ancestor`), flagged stale by
`docs/audits/2026-09-13-census-x-664-delete-list.md` section 4.2 three days before this
contract froze, and never acted on. `scripts/cost_usage_telemetry.py`, the fourth, was already
WIRED (imported by `scripts/provider_router.py`, per `lane-x-691-routing-half-a`) rather than
inventory. Per the contract's own Decision Budget Q10 ("a lane that discovers a refuted premise
PAUSEs with the fact"), this paused rather than proceeding on the stale text.

**Operator ruling (2026-09-16), reduced scope, four deliverables:**

1. CORRECT [#694]'s stale row text in place, citing the x-664 census as source — not archive it
   away a second time, which the operator named as the same failure mode as leaving it
   undocumented (the census already flagged it once, on 2026-09-13, and nothing acted on it).
2. `[#685]`: dispatch refuses without a GO artifact, RED-first — the batch-manifest-line half
   only; the `RATIFICATION-<date>.md` transport fallback is explicitly out of scope.
3. AX9-5's metric — raw-search calls vs organ calls per session, organs uncalled in 30 days —
   emitted from the surviving telemetry.
4. File a new row, from this lane's reserved id block (843-846), against the contract-freezing
   mechanism itself: three lanes this window (`[#667]`/y-755, `[#810]`/ab-810, this lane's
   `[#694]`) found their contract's premise refuted, and all three premises came from digests
   the architect wrote without re-verifying current state at freeze time.

Explicitly ruled NOT a fork: a fork is an undefined rule in this protocol, and this is a stale
premise with two well-specified remainders — escalating would cost a round trip for a ruling
the operator gave in one line.

## 2 · Deliverable 1 — the premise corrected in place (`c0565024`)

`tasks/694-*.md`'s stale sentence (*"the other three ... are untouched and remain X2-6's"*) is
replaced in place with the true disposition (deleted at `c9ea3b07`/`3a380fd8`, citing the x-664
census as source). Row body: 5787 bytes, under the `row-archive-proof` LEG D ratchet ceiling of
5806 bytes (event 1, 2026-09-14) by 19 bytes — computed with `gen_task_tree.extract_body()`
before writing, not by trial and error against the gate.

**Kept inline, not relocated**, and that choice is the point: a correction relocated via
`archive_row_body.py relocate` would move the true text into `tasks/archive/694.md` and leave
the LIVE row showing the original false sentence — functionally the same failure the operator
named (documenting a lie a second time). This trips `row-archive-proof` LEG C to UNPROVEN for
`tasks/archive/694.md` (non-blocking, per the tool's own docstring: expected when a row is
edited in place after its last relocation rather than through the tool) — accepted rather than
resolved by relocating, because resolving it would undo the correction.

## 3 · Deliverable 2 — `[#685]`'s GO-file refusal, RED-first (`31aa12cb`)

`scripts/lane_boot.py` gains a fourth `/lane-boot` preflight refusal,
`check_go_artifact(repo, lane, batches, main_ref)`: for each open batch, it reads the manifest
plus every committed `<manifest-stem>-amendment-N.md` (numeric-sorted, later wins) and refuses
unless some row names the lane and that row does not read HELD. Five new RED-first tests in
`tests/test_lane_boot.py` (12/12 pass). No new artifact format invented — it reads the exact
live shape already in use: the batch-manifest amendment's per-lane State column.

**Honest limit, stated rather than solved:** the `RATIFICATION-<date>.md` transport fallback
`protocols/OPERATOR-INTERFACE.md` section 1 also names is NOT built. `[#685]`'s Done-when has
two carriers; this lane discharges the batch-manifest-line half and records the transport half
as open, in the row body (relocated to `tasks/archive/685.md` Event 2 via
`archive_row_body.py relocate --id 685`, since it is additive new-work narration, not a
correction — the class distinction Deliverable 1 draws above).

## 4 · Deliverable 3 — AX9-5's metric (`7d70c595`)

**Not added to `cost_usage_telemetry.py`.** That module's own docstring states it "owns no read
surface, matching `telemetry_emit.py`'s own Stage-3 deferral" and separately argues against
folding a different-axis metric into an existing table — reasoning that applies symmetrically
against forcing THIS metric in, since it is a different axis again (tool-call classification,
not model-call spans).

**New module `scripts/organ_usage_metric.py`.** A retrospective reader over Claude Code's own
session transcripts — `lane_cost.py`'s own "reader, not instrument" posture, applied to a
different question. Classifies each `tool_use` block as `raw_search` (a `Grep` call, or a
`Bash`/`PowerShell` command headed by a search tool) or `organ_call` (a shell command naming a
known organ path), reusing `deny_and_point.SEARCH_HEADS`/`load_processes()` so "organ" and
"search" mean the same thing on both surfaces. `organ_usage_report()` tallies per session and
computes organs uncalled in the window; a minimal `report` CLI subcommand is the operator's
call site. 13 RED-first tests in `tests/test_organ_usage_metric.py`, all green.

**Disposition, not a SessionStart wire, and that is a deliberate reading of an existing
anti-pattern rather than an oversight.** `fleet_health.py`'s `cost_health_line` reads ONE
precomputed ledger file rather than scanning the session store, specifically because
SessionStart pays for the digest on every boot and a transcript walk would make that cost grow
with history rather than with the batch. `organ_usage_report()` IS a transcript walk — the only
way this metric can exist at all, since nothing in this repo persists a raw-search-vs-organ-call
event — so wiring it to SessionStart would reintroduce exactly that anti-pattern on the
widest-audience hook in the repo. `graph_queries.ORPHAN_DISPOSITIONS` records it instead as an
on-demand operator report, owned by `[#709]` (the log-review routine AX9-5 names as its
regression-flagging consumer) or a future digest command.

## 5 · Deliverable 4 — the systemic finding, filed (`4cf49681`)

`[#843]` (drawn from this lane's reserved block 843-846). Files the row against
`gen_lane_contract.py`'s freeze step: a contract clause asserting a file's or module's state is
a claim about `main`, checkable the moment before the freeze, not a claim about the digest that
produced it. Cites all three refuted-premise instances this window: `[#667]` (lane y-755,
`docs/audits/2026-09-14-technical-lane-y-755-docs-cut-finish.md` section 2), `[#810]`
(lane-ab-810-substrate-repair — cited as the operator's own characterization, "two-sided
drift", since that lane has not merged and its own end-of-lane artifact was not yet available to
read against), and `[#694]` (this lane). `tasks/manifest.json` gained a node at the section
holding this window's other freshly-filed rows (accepted 823/824/825/826/827), immediately
before the `### [S4]` heading — `gen_task_tree --emit-source`/`--check` both clean afterward.

## 6 · Verdict, and what the integrator owes

**Targeted suite** (per `scripts/impacted_tests.py select` over every changed `scripts/*.py`):
23 modules, 1175 collected, **12 failed, 1163 passed**. All 12 attributed against a detached
baseline worktree at this lane's own merge-base with `origin/main` (`f8ca1d40`), then removed and
verified gone:

- **10 fail identically** on baseline and tip, none touching this diff: `test_deny_and_point`
  ×2 (`.claude/settings.json` does not wire `deny_and_point` into `PreToolUse` — a pre-existing
  gap this lane's footprint excludes), `test_canonical_docs` ×2 and `test_gen_handoff` ×5
  (PLAYBOOK/handoff staleness drift), `test_v6_frozen_contract` ×1 (`--cross-repo` unbuilt).
- **1 flips from SKIP to FAIL for an environmental reason, not a content one:**
  `test_deny_and_point::test_the_WIRED_COMMAND_ITSELF_denies_and_allows_as_configured` skips
  when the FPG-1 store is absent (a fresh baseline worktree never rebuilds it) and runs once the
  store exists (this worktree's own `graph-rebuild` pre-commit hook built it over several
  commits) — and then hits the SAME pre-existing "not wired into `.claude/settings.json`"
  condition the two rows above already show. Not a new class of failure.
- **1 is this lane's own, and by design:** `test_archive_row_body::test_every_committed_record_still_proves_out`
  fails on both (`proven == len(record_files)` never holds, pre-existing), but the proven count
  drops from 85 to 84 — [#694]'s in-place correction is an edit after `tasks/archive/694.md`'s
  last relocation, so LEG C reports it UNPROVEN, which is §2's accepted consequence, not a
  surprise found here.

The full suite was not run, per the contract's explicit targeted-only constraint.

**Rows.**

- `[#694]`: the modules leg of Done-when is MET (three deleted, the fourth wired, corrected in
  the row itself) and AX9-5's metric clause is MET (`organ_usage_metric.py`, on-demand). Left
  `open` — the GO-file leg of Done-when belongs to `[#685]`, not this row, per the row's own
  text ("the roster pairs them in one lane and they are two rows"), and the row is the
  architect's/operator's to close, not this lane's under its reduced-scope ruling.
- `[#685]`: the batch-manifest-line half of Done-when is MET, witnessed (5 RED-first tests).
  Left `open` — the `RATIFICATION-<date>.md` transport half is not built, named in the row body
  rather than left to be noticed.
- `[#843]`: filed `open`, against the contract-freezing mechanism itself. Nothing in this
  lane's footprint builds its Done-when — that is a `gen_lane_contract.py` change, outside a
  cost-telemetry lane's declared scope, and is recorded as the next lane's to pick up.

**Decisions taken under the Decision Budget, none escalated:**

1. The refuted premise was corrected, not merely re-documented — the operator's explicit
   instruction, and the one place this lane deviated from the frozen contract's literal steps
   (which assumed the premise held).
2. AX9-5's metric landed in a new sibling module rather than in `cost_usage_telemetry.py`,
   on that module's own stated read-surface boundary — a judgment call under the library-first/
   no-scope-creep rule, not escalated because the reasoning is symmetric with reasoning the
   target module already states about itself.
3. The new metric was NOT wired to `SessionStart`, on the same cost reasoning
   `fleet_health.cost_health_line` already states about itself — recorded as a disposition
   rather than a TODO.
4. `[#810]`'s citation in `[#843]` is attributed to the operator's own characterization rather
   than to a landed audit, because that lane has not merged at the time of this writing. Named
   rather than left unstated.

**No merges, no pushes, no JOURNAL entry, no index regeneration beyond what filing/correcting a
row requires** (`gen_doc_counts.py --write` for the pytest-count gate, `gen_task_tree.py
--emit-source` for the new row) — per the contract's explicit prohibitions. `git stash list`
empty; working tree verified clean before this audit's own commit.
