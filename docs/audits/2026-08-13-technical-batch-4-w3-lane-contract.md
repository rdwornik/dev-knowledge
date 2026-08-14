# W3 — `[#513]` landing-predicate organ (+ E4-05 drive-by)

## Dispatch
| Field | Value |
|---|---|
| Model | Opus plan → Sonnet implement (`opusplan`) |
| Mode | auto (accept edits); plan-mode NOT invoked — the committed contract is the plan |
| Effort | high |
| Worktree | **`worktree-lane-c-513-landing-predicate`** (grammar per `[#514]`; letter c per the E5a skeleton) |
| Label | `w3-513-landing-predicate` |
| Bucket | finish-line |

## Repo + Purpose
`.dev-knowledge`. Purpose: build the `[#513]` landing-predicate organ — the mechanism that answers "did this ruling actually land?" from the tree — exactly to the row's amended Done-when, plus the ruled E4-05 drive-by pair. This lane is a **batch-4 carried lane**: contract committed before dispatch (I-D3, step-0 self-serve) and manifest row flipped by amendment marker.

## Contract base — DO NOT RE-DERIVE
The committed **night-2 E5a skeleton is this contract's base**: row-is-the-spec; `[#513]`'s amended Done-when (4 testable clauses) quoted **verbatim** as the acceptance section; 7 steps as drafted; expected-REDs stated as a **class with revert-proof duty** (W2-reds law), never a list. Where this file and the skeleton differ, the skeleton's technical content wins and this file's scope additions below apply on top.

## Scope additions (ruled at the picker / ARC2)
1. **E4-05 drive-by, both halves** (route (i), I-D8 precedent): (a) repair the PLAYBOOK Ch8 dispatch-alias paragraph (L19) — wording **declarative**, names the PATH command, ratchet ≤ 441 verified after; (b) port the `git ls-files` filter into `gen_audit_index.py:57` (W5 wrote and tested this exact fix — port, not design) with the test: real git repo, **untracked** `docs/audits/*.md`, `--check` stays exit 0.
2. **L19's paragraph is this organ's first natural test case** — after (a), the organ run over the repaired site must report it landed; include that as a test.
3. **Registration boundary (from the ARC2b step-7 verdict):** if the verdict printed `DISJOINT`, the organ lives in its own module and **`scripts/audit.py` registration is OWED TO THE INTEGRATOR** — record the owed registration in the lane packet, do not touch audit.py. If the verdict printed `OVERLAP`, this lane runs before CODEX-524 and registers normally.
4. **G-6 pinned:** any recorded-reason surface this organ writes to is `STANDING_RULINGS` — not re-litigated in-lane.

## Lane discipline (law, restated thin)
`uv run --locked` on every test · V-2 decision budget stated back in one line at boot · JOURNAL entry ON the lane branch before stopping · **commit-and-STOP, stash empty, NEVER self-merge** · questions batched in the lane packet, never dripped · no `CLAUDE.md` edit (the §9 row is integrator-owed, W5 precedent) · no `ARCHITECTURE.md` edit · no `SKIP=` · no births.

## Review
**Code-impact lane → terra review PRE-MERGE, mandatory.** Review artifact persisted with the severity tally in-body; the integrator merges only against that artifact.

## Done-when (frozen)
(1) The four amended `[#513]` Done-when clauses pass, each with its named test; (2) E4-05 (a)+(b) landed with their tests, ratchet ≤ 441; (3) L19-site landing verified by the organ itself; (4) registration either landed (OVERLAP path) or recorded integrator-owed (DISJOINT path); (5) terra artifact present with tally; (6) lane packet: shas · test counts · decision-budget report · owed-to-integrator list.
