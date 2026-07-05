# Codex Review — slice-b-fix-batch

**Date:** 2026-07-05
**Branch:** `feat/lived-sandbox-slice-b`
**HEAD:** `2337fd6`
**Diff range:** `c1647f1..HEAD`
**Codex version:** codex-cli 0.141.0
**Mode:** diff-review

---

## Focus

- lived_sandbox #253 fix-batch + Step-7 + C4 closure epic
- observe.py hook-stdout channel scoping (Bash-only tool_results, attachment hook_* payloads, result-event/narration exclusion) — any remaining false-FIRED/false-SILENT channel?
- arc.py GATE-0 outer_only_markers filter (honest-vacuous negative control on self-clone) — soundness
- arc.py seeding (ecosystem state, tier1 plugin into isolated config, consumer-shape baseline commit) + scoped permission allowlist (never bypassPermissions)
- oracle.py signature_breadth_problems guard
- spawn.py utf-8 decode + isolated-config permissions seeding
- fixtures are REAL frozen transcripts (scrub-verified) — flag any secret/PII residue you spot

---

## Findings
## CRITICAL

(none)

## HIGH

## HIGH deploy/lived_sandbox/arc.py:86 — outer marker filter is too broad

**What:** `outer_only_markers()` treats any marker text under `scripts/`, `.claude/`, or `plugins/` as self-emittable; `[closures]` is filtered because it appears in `review_closures.py`, but that marker is emitted by the global surfacing path, not the arc’s project hook path.  
**Why:** A real outer L0 `[closures]` leak can be hidden while provenance still passes, producing a false GATE-0 pass.  
**Fix direction:** Derive self-emittable markers from active hook/command wiring or a clean self-baseline run; keep `[closures]` as a live negative control unless the arc can actually emit it.

## HIGH deploy/lived_sandbox/arc.py:344 — baseline commit failure is ignored

**What:** `run_arc()` runs the baseline `git add`/`git commit` but does not check either return code or assert a clean worktree before spawning the child.  
**Why:** If the baseline commit fails, the child runs against dirty harness setup and the observer may measure setup failure rather than lived-workflow behavior.  
**Fix direction:** Check both git calls, then assert `git status --porcelain` is clean; only tolerate “nothing to commit” when the tree is already clean.

## MEDIUM

(none)

## LOW

(none)
