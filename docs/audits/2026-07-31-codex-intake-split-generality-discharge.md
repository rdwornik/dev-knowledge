# Codex Review — intake-split-generality-discharge

**Date:** 2026-07-31
**Branch:** `feat/intake-split-generality-discharge`
**HEAD:** `0807fbda`
**Diff range:** `main..feat/intake-split-generality-discharge`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review

---

## Focus

- The residue-carrier round-trip: is byte-exactness actually guaranteed, or only usually? Look for any input where parse_readme -> reassemble could diverge.
- The hub-only guard on check_intake_tree_coherence: can it still manufacture a consumer FAIL?
- gen_intake_index.render_row extraction: is output byte-identical to the previous inline form?
- ASCII-only output discipline on the drift path (README.md contains U+2192; Windows stdout is cp1252).
- Whether the gate can be satisfied by deleting what it checks.

---

## Findings
Four High findings.

## Critical

(none)

## High

### HIGH — [scripts/gen_intake_tree.py:157](C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/gen_intake_tree.py:157) — Empty residue-only manifests pass

**What:** Marker presence, ordering, uniqueness, and item coverage are not validated; deleting the marker block or every item row and regenerating produces a valid all-residue manifest that passes the round-trip.

**Why:** The gate can report success without exercising the per-item split it exists to prove.

**Fix direction:** Require exactly one ordered marker pair and a non-empty, duplicate-free item-node set matching `collect_intakes()` one-for-one.

### HIGH — [scripts/audit.py:3000](C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:3000) — Staged changes can bypass the gate

**What:** Unlike `check_task_tree_coherence`, this check reads only the working tree and never verifies index/worktree agreement.

**Why:** A staged deletion or modification under `docs/intake/` can be hidden by restoring the coherent working-tree version; the pre-commit check passes, but the commit records an incoherent or deleted carrier.

**Fix direction:** Fail on `_index_worktree_divergence` across the complete `docs/intake/` path before calling `evaluate()`.

### HIGH — [scripts/gen_intake_tree.py:170](C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/gen_intake_tree.py:170) — Parse-time losslessness check is tautological

**What:** Item nodes are checked by looking their original text back up in the input, rather than by calling `Model.reassemble()`; a stale title or trailing row suffix therefore lets `parse_readme()` return a model whose reassembly differs from its input.

**Why:** The advertised byte-exact parser contract is false, and `--write` can successfully emit a carrier that immediately fails its own round-trip check.

**Fix direction:** Validate the model against actual item-derived reassembly and refuse manifest generation when it differs from the source.

### HIGH — [scripts/gen_intake_tree.py:140](C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/gen_intake_tree.py:140) — Status-only changes remain green

**What:** `_rows_by_filename()` discards the collected status, while status headings and ordering are stored as unchanged residue; changing only an intake document’s `status:` therefore affects neither reassembly nor the expected manifest.

**Why:** `--check` stays green despite a stale README grouping, contradicting the manifest’s claim that projected status changes turn the check red.

**Fix direction:** Re-derive and validate grouping from statuses, or store/hash projected status values in the manifest, with a status-change regression test.

## Medium

(none)

## Low

(none)
