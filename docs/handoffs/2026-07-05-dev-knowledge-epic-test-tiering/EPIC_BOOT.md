# EPIC HANDOFF — test-tiering · 2026-07-05
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | 2026-07-05-dev-knowledge-epic-test-tiering |
| **Mode** | **epic** — one epic end-to-end, inside a root-provisioned worktree (ADR-97; HANDOFF_PROCESS §14a) |
| **Repo** | .dev-knowledge |
| **Date** | 2026-07-05 |
| **Epic branch** | `epic/test-tiering` (root-provisioned; bundle generated on `docs/2026-07-05-wave2-prep`) |

## Boot (epic lane)

You are an **EPIC-CHAT lane** (HANDOFF_PROCESS §14a; ADR-97). The root architect owns ADR
acceptance, backlog structure, parallelism rulings, and ALL merges to main. On load reply:
"Epic lane test-tiering booted — worktree + boundary acknowledged."

## Worktree + branch

Worktree `epic-test-tiering` (root-provisioned — never self-provisioned) · branch
`epic/test-tiering`. **RELATIVE PATHS ONLY** (the absolute-path-bypasses-worktree lesson is a
hard rule). Commit-per-story; **commit-and-STOP** — no merges to main.

## Epic scope (the BACKLOG slice)
<!-- FILL-IN:scope START — ROOT authors: epic id · stories in order · done-when per story -->
Epic id **[#260]** (BACKLOG · Tooling & evaluation · "Epic 5 — ship-gate test tiering"); executes **#256 + #257**. **Operator priority: tests EFFECTIVE + DYNAMIC.** Stories in order (from #256 + the 2026-07-05 pytest profile — serial 9m42s vs `-n auto` 2m05s, 4.6×):

1. **S1 — `-n auto` in the ship pre-flight** (measured 9m42s→2m05s). Done when: the /ship pre-flight runs parallel and a timed run evidences it.
2. **S2 — diff-shaped selection**: docs-only diff → the ~20–30 live-repo-sensitive tests + `audit.py ship-gate`, budget ≤60s; code diff → parallel run, budget ≤2min. Done when: each diff class MEASURES within its budget (timed runs).
3. **S3 — full serial suite → nightly/on-demand path defined**: no cron build — a documented invocation is enough for now. Done when: the path is documented and invocable.
4. **S4 — #257 venv hygiene**: dependency-isolation decision implemented (venv or documented policy) + pytest-xdist as declared dev dep. Done when: the decision is recorded + implemented and pytest-xdist is reproducibly installable from `pyproject.toml`.
<!-- FILL-IN:scope END -->

## Epic done-contract (ex-ante, immutable to this lane)
<!-- FILL-IN:done-contract START — the hard closure metric for the WHOLE epic -->
**MEASURED ship latency meets budget per diff class** (docs-only ≤60s; code diff ≤2min — evidence: timed runs pasted in the EPIC RETURN), the full-suite path documented, gates green on branch. Closure is claimed on the measurements — never on "config edited" or "committed". No coverage loss unaccounted (#256's clause).
<!-- FILL-IN:done-contract END -->

## FILE-BOUNDARY (hard)
<!-- FILL-IN:boundary START — may-touch / may-NOT-touch; disjoint from every concurrent epic -->
**May touch:** `plugins/tier1-lifecycle/**` (ship pre-flight) · pytest/pyproject config (`pyproject.toml`, `pytest.ini`-class files) · new selection helper under `scripts/` if needed · #257 venv hygiene surfaces · own BACKLOG block ([#260] checkboxes only) · `JOURNAL.md` (append).
**May NOT touch:** test file contents beyond markers (**a broad marker sweep → escalate**) · `scripts/audit.py` · `ecosystem/doc-counts.md` (**FORBIDDEN** — the root regenerates it once at integration).
A needed file outside the boundary → STOP, escalate — don't touch. 3 lanes = the ADR-97 cap ceiling — this lane spawns no sub-work outside its worktree.
<!-- FILL-IN:boundary END -->

## Escalation
<!-- FILL-IN:escalation START — epic-specific triggers beyond the standing set -->
Epic-specific: (1) a marker sweep touching many test files (beyond adding markers to the ~20–30 live-repo-sensitive set) → STOP, return to root with the proposed sweep; (2) a selection scheme that would silently DROP coverage for a diff class (the no-coverage-loss-unaccounted clause) → escalate with the accounting; (3) the venv decision forcing changes to hooks/CI invocations outside `plugins/tier1-lifecycle/**` (e.g. `.pre-commit-config.yaml` interpreter paths) → escalate — that file is not in this boundary. Standing set (always): ADR-worthy fork · boundary-breach need · cross-epic dependency discovered → STOP, return to the root. Everything intra-epic is the lane's own judgment.
<!-- FILL-IN:escalation END -->

## Refusals (standing — not editable by the lane)

No merge to main · no ADRs · no backlog structure (checkboxes inside this epic's own block
only) · no worktree lifecycle ops · no new top-level folders · no content deletion without
operator ask.

## EPIC RETURN (required before any merge)

Close the lane by filling `EPIC_RETURN.md` in this bundle (§14b): commits + branch state ·
contract-vs-outcome per story · self-adjudications · proposed BACKLOG delta ·
merge-readiness. The root reviews the return against this contract → serial `--no-ff` merge →
applies the backlog delta → declares closure → tears down the worktree.

## Probes

Boot on `PROBES.md` (this bundle) — live-state probes scoped to this epic's boundary
(HANDOFF_PROCESS §5 contract: question + source-locator + command, **never the answer**).

> **Operator note.** Paste THIS file + `PROBES.md` into the fresh epic chat. Epic mode
> assembles no `PASTE_THIS.md` — the v5 paste manifest is architect/execution-shaped
> (requires `RESIDUAL.md`); the EPIC_BOOT scope-contract IS the paste.
