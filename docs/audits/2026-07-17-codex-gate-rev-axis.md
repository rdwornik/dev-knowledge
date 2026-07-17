# Codex Review — gate-rev-axis

**Date:** 2026-07-17
**Branch:** `feat/336-gate-rev-axis`
**HEAD:** `96b651a8`
**Diff range:** `main..feat/336-gate-rev-axis`
**Codex version:** codex-cli 0.144.5
**Mode:** diff-review

---

## Focus

- ADR-102 gate_rev_ahead axis in scripts/fleet_parity.py: is the MUST_OK refinement truly non-waivable (never routes through _pass_or_declare / .methodology.yaml)?
- Ancestry direction: is 'corpus C is ancestor of gate G' the correct 'strictly ahead' predicate? Any way a behind/equal/unrelated gate slips through _gate_ahead_ok?
- Can a gate_rev_ahead declaration conjure presence, suppress a missing hook id, or clear an absent MUST surface?
- The waivable:true-on-MUST loader refusal + the STALE self-invalidation path.

---

> **Note:** the `codex-review.ps1` wrapper's read-only sandbox had no writable temp dir, so Codex's session-start `pytest --collect-only` self-check failed and it paused for confirmation instead of reviewing. The review below was produced by re-running `codex exec --sandbox read-only` directly with the diff and an explicit static-review instruction (same Codex `gpt-5.6-terra` lane). Both findings were **fixed before merge** (commit follows this audit); see resolution notes.

## Findings

### HIGH — `scripts/fleet_parity.py` — Tag-name inequality does not prove strict ancestry
**What:** Strictness was inferred from `hit["rev"] != source_tag`, but two differently-named tags can resolve to the same commit; `merge-base --is-ancestor C G` is then true (reflexive) and would incorrectly bless `GATE_AHEAD_DECLARED`.
**Why:** An equal gate can slip through under an alias tag, violating the strictly-ahead contract; the tests covered identical names and behind-ancestry but not distinct tags on the same commit.
**Fix direction:** Compare peeled commit IDs, or require `C` ancestor-of `G` **and** `G` not ancestor-of `C`, with an equal-commit alias regression test.
**RESOLUTION (fixed):** `collect_facts` now computes `gate_strictly_ahead = (C anc-of G) and not (G anc-of C)` — the second `merge-base` leg defeats the reflexive alias case; `_gate_ahead_ok` reads `gate_strictly_ahead`. Regression test `test_gate_ahead_alias_tag_same_commit_still_warns` (two tags on one commit → WARN).

### HIGH — `scripts/fleet_parity.py` — Declaration grammar is not enforced
**What:** `_gate_ahead_ok` accepted any non-empty provenance list (incl. `[{}]`/`[null]`); a truthy non-mapping `gate_rev_ahead` could raise on `.get()` in `collect_facts` (crash instead of a clean refusal).
**Why:** A malformed declaration could bless a MUST mismatch without the mandatory provenance, or crash the checker; tests exercised only well-formed declarations.
**Fix direction:** Validate `gate_rev_ahead` fully in `load_manifest` — mapping shape, fleet repo keys, entry mapping, non-blank reason, gate_tag, and every provenance item `{kind, repo, ref}` — with malformed-shape refusal tests.
**RESOLUTION (fixed):** `load_manifest` now refuses a malformed `gate_rev_ahead` (row skipped, never reaches `collect_facts`); `collect_facts` also hardened with an `isinstance(..., dict)` guard. Regression test `test_gate_rev_ahead_malformed_declaration_is_loader_refusal` (5 malformed shapes → REFUSED, good row survives).

### HIGH (round 2 re-review) — `scripts/fleet_parity.py` — Provenance validation permitted malformed evidence
**What:** After the round-1 fix, provenance fields were still checked for truthiness only, so whitespace-only or non-string `kind`/`repo`/`ref` values passed and could bless `GATE_AHEAD_DECLARED` without meaningful, auditable provenance.
**Why:** The declaration grammar (which #316 will adopt) was not fully enforced.
**Fix direction:** Require non-blank strings for every provenance field (and gate_tag); add null/non-list/non-dict/blank/non-string cases.
**RESOLUTION (fixed):** Added `_nonblank(v)` (non-blank string predicate); `load_manifest` now requires non-blank-string `gate_tag`, `reason`, and every provenance `{kind, repo, ref}` field. Malformed-refusal test extended to 9 shapes (non-list provenance, whitespace field, non-string field, non-string gate_tag). Round-2 also confirmed: HIGH #1 resolved (reverse-ancestry defeats same-commit aliases), HIGH #2 crash path closed, `_gate_ahead_ok` remains non-waivable (never consults the allowlist; failed conjuncts fall to the MUST error path). `gate_rev_ahead: null` is treated as absent (standard YAML semantics — intentional, not a defect).

## Verdict

Three HIGH findings (2 round-1 + 1 round-2) all fixed pre-merge and re-reviewed. No Critical/Medium/Low findings survive. The MUST_OK refinement is confirmed non-waivable (never routes through `_pass_or_declare`/`.methodology.yaml`); the strict-ahead predicate, loader grammar refusal, and STALE self-invalidation paths are sound.
