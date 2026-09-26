# Codex Review — lane-boot-contract

**Date:** 2026-09-25
**Branch:** `worktree-lane-boot-contract`
**HEAD:** `0722fa37`
**Diff range:** `main..worktree-lane-boot-contract`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 1/5/0/0 <!-- Critical/High/Medium/Low. All six were fixed in eb7ab636; this tally counts what the review found, not what remains open. -->

**Consumer:** lane contract `LANE-5B2-12-boot-contract.md` (batch WAVE5B-N2 row 12; plan `PLAN-HARNESS-CONSOLIDATE-DEPLOY-2026-09-25` phase P1) — its Done-contract item 4 requires this record.

**Disposition:** all 6 findings fixed in commit `eb7ab636`, each pinned by a regression test: the CRITICAL dry-cut target (refused inside any git work tree that does not ignore it — `test_dry_cut_refuses_a_target_inside_another_git_work_tree`); self-locator traversal (`test_a_self_locator_cannot_traverse_out_of_its_bundle`); exact pointer sets and the exact launcher line (`test_a_plausible_but_wrong_existing_pointer_fails`); stray DATA-block content (`test_an_unchecked_line_inside_the_data_block_fails`); boot-cost provenance — a measured value now names its instrument ("operator tally … not machine-witnessed") and binds its dispatch by sha256 (`test_a_measured_boot_cost_without_its_provenance_fails`). On that last one the count itself stays the operator's by design: the browser seat keeps no transcript the repo can read (HANDOFF_PROCESS §5), and the C4 research names the operator's tally as the honest instrument for turns; what is machine-witnessed is the dispatch.

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Consumer: lane contract LANE-5B2-12-boot-contract.md (batch WAVE5B-N2 row 12, plan PLAN-HARNESS-CONSOLIDATE-DEPLOY-2026-09-25 phase P1).
Changes: scripts/gen_handoff.py (boot header emitted as a probe-checked DATA block + a byte-budgeted PROSE block; HANDOFF_RECEIPT.json with paste bytes and a boot_cost field; --dry-cut/--boot-turns/--boot-dispatch flags); scripts/verify_handoff_probes.py (BOOT_DATA_RULES: one rule per data row, BD-*/BP-budget results, era-gated 2026-09-25, self-locators bind to the bundle under verification); templates/handoff/v5/HANDOFF_BOOT.md.tmpl; tests.
Please check: can any rule PASS a wrong fact (false clean)? does the self-locator change let a probe row bind to the wrong file? does --dry-cut open a way to commit an unchecked bundle? is boot_cost ever a guessed value? are existing CLI flags/exit codes and older (pre-era) bundles unaffected?

---

## Findings
## Critical

## scripts/gen_handoff.py:2570 — `--dry-cut` can write a committable unchecked bundle

**What:** It only rejects paths inside the current `repo_root`; a sibling worktree’s `docs/handoffs/` is outside that root and is a valid Git-tracked handoff destination.  
**Why:** The command skips all cut-boundary gates, yet its output can be committed as a normal bundle from that other worktree.  
**Fix direction:** Refuse any dry-cut target inside any Git worktree/repository, and require a non-repository temporary target.

## High

## scripts/verify_handoff_probes.py:1068 — Self-locator permits traversal outside the verified bundle

**What:** `_self_locator_file()` joins the unvalidated `rest` portion directly onto `bundle_dir`; e.g. `docs/handoffs/<slug>/../other/PROBES.md` resolves to a sibling file.  
**Why:** A probe/data row can PASS while binding to the wrong bundle (or, on Windows, potentially an absolute path), defeating the self-locator guarantee.  
**Fix direction:** Resolve the candidate and require it to remain beneath the resolved bundle directory before accepting it.

## scripts/verify_handoff_probes.py:1085 — Pointer rows PASS arbitrary existing files

**What:** Generic `_rule_pointer()` checks only that a backticked path exists; `Routing`, `Rules`, `Runbook`, `Harness`, and `Seat orders` can name unrelated existing files and pass. `Role` inherits this weakness at line 1159.  
**Why:** The header can contain a plausible but wrong canonical pointer while every BD result is clean.  
**Fix direction:** Give each named row an exact expected path/set of paths, including the ordered seat-template list, and reject substitutions.

## scripts/verify_handoff_probes.py:1177 — Launch rule does not validate the claimed command

**What:** Any command containing one existing script path, `--help`, and a source-text-matched verb passes; the interpreter/runner and other arguments are unchecked.  
**Why:** A non-runnable or wrong launch command can be emitted as verified data.  
**Fix direction:** Parse and require the sanctioned command form (including `uv run --locked python`, script, verb, and terminal `--help`).

## scripts/gen_handoff.py:2088 — `boot_cost` labels an unverifiable CLI value as measured

**What:** Any positive `--boot-turns` paired with any existing `to-cc/*.md` path becomes `"measured"`; neither the count’s provenance nor whether that order was the first correct dispatch is established.  
**Why:** A guessed value is recorded and later accepted as a measurement, contrary to the receipt’s stated honesty contract.  
**Fix direction:** Keep the value unmeasured unless a durable tally artifact binds the count to the relevant dispatch and superseded bundle; verify that artifact in the receipt rule.

## scripts/verify_handoff_probes.py:1029 — Unrecognised content in the DATA block is silently ignored

**What:** The parser ignores every non-bold-key line in the DATA block, including unbolded table rows and prose.  
**Why:** An unchecked fact can be inserted into a block promised to contain only probe-checked data while all BD probes still pass.  
**Fix direction:** Reject nonblank DATA-block content except the exact table header/separator and valid bold-key rows.

## Medium

(none)

## Low

(none)