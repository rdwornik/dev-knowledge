---
name: decide
description: Run a structural decision through the system, not through one seat -- research, subagent fan-out, a matrix, a pre-mortem, two independent evaluators, an ADR draft -- and gate every step with scripts/decide_checks.py rather than trusting the prose.
---

# /decide — a structural decision, produced and checked

```
/decide <question>
```

## Why

R14 (`RATIFICATION-2026-09-25`) says CC decides through the system: research, several
subagents, multi-model review, a Proposed ADR, the operator's ratification — "what CC does not
know, it researches — it does not defer." The CI/OS-verification decision is the proof this is
worth doing as a command rather than a one-off prompt: two independent evaluators caught the
producer scoring end-states instead of first-implementable stages, two factual errors, and a
contract-breaking option nobody had flagged — and the producer's own matrix arithmetic was wrong
in **12 of 15 totals** until a script recomputed them
(`PROPOSAL-ADR-CI-VERIFICATION-2026-09-26-seat-71020de7.md` §"Step 5"). The companion run found
the same shape of gap from the other side: three of four failed evaluator spot-checks were
subagent errors the producer had passed on unverified
(`PROPOSAL-ADR-REMOTE-LANE-OBSERVABILITY-2026-09-26.md` §"Step 5"). Free-text review did not
catch either class. A deterministic check, run before synthesis and before the operator ever
reads the proposal, does.

## The flow

1. **Brief** — state the question and its known constraints; nothing more (questions only, no
   pre-committed answer).
2. **Research fan-out** — several subagents in parallel, one per sub-question; Gemini (`agy`)
   for any basis document over ~50 KB. Every subagent's brief carries the exclusion list
   (Check 7) — R15's frame, enforced by mechanism, not by asking nicely.
3. **Evidence + matrix + pre-mortem** — the producer assembles the evidence file: the decision
   matrix (weights + scored options, the markup below), a self-evaluation of what could be
   wrong before anyone else reads it, and a `## Subagent claims` section naming every subagent
   finding the matrix or pre-mortem actually relies on (Check 8).
4. **Two independent evaluators** — from model families other than the producer's own (Check
   4: `excludes_producer`). Each writes findings as `- id: <ID> -- <objection>` lines.
5. **Response table** — one row per finding id, every response cell starting `**Accepted**` or
   `**Rejected**` (Check 5).
6. **ADR draft** — `## Quality attributes` (ADR-124 D5), `## Flip-condition`, `## Alternatives
   considered`, all present and filled (Check 6).
7. **Gate, then hand to the operator** — `scripts/decide_checks.py` on every artifact above;
   any defect is fixed or the artifact is not ready. Ratification is the operator's, never this
   command's.

## The markup contract `scripts/decide_checks.py` reads

**Matrix** (the evidence file):
```
Weights: fidelity=25 portability=20 throughput=20 cost=10 modifiability=10 observability=15
| Option | fidelity | portability | throughput | cost | modifiability | observability | Σ |
|---|---|---|---|---|---|---|---|
| A1 today | 3 | 1 | 1 | 2 | 3 | 1 | 1.80 |
| A7 armed | 4[^1] | 4[^2] | 4 | 4 | 3 | 4 | 3.90 |

[^1]: measured -- run 36234959090, jobs/70677588/tmp/vtop-suite.log:561
[^2]: measured -- docs.github.com/actions/reference/runners, read 2026-09-26
```
Column names must be the weight names, exactly, case-insensitive; weights must sum to 100; a
cell scored 4 or 5 without a `[^n]` footnote whose body contains "measured" is flagged — it was
supposed to cap at 3.

**Subagent claims** (the evidence file, one section):
```
## Subagent claims

- the comparator only checks node ids {probe: scripts/known_reds.py:200}
- the config still says "private on the Free tier" {probe: grep -c 'private on the Free' report-only-wall.yml}
- no org exists {probe: git check-ignore some/path}
- cannot be recovered from the transcript {unverified}
```
Every bullet ends in `{probe: <path:line | grep -c '<pattern>' <path> | git check-ignore <path>>}`
(run and checked) or `{unverified}` (recorded, not silently dropped).

**Evaluator record** (each `EVAL-*.md`, top fields):
```
served-model: gpt-5.6-sol
attestation-source: codex exec header
producer-model: claude-opus-5-5

- id: C1 -- <objection>
```

**Response table** (one row per finding id across every evaluator file):
```
| id | objection (short) | response |
|---|---|---|
| C1 | <short form> | **Accepted** -- <what changed> |
```

**ADR draft** — `## Quality attributes` carries **Quality attribute(s)**, a six-part
**Scenario** with a **Response measure**, and **Decision evidence**; `## Flip-condition` and
`## Alternatives considered` are both present and non-empty (reuses
`validate_adr_status.section_state` for the latter two — the same shape `validate_adr_status.py`
already enforces for every landed ADR).

## Running the gate

```bash
uv run --locked python scripts/decide_checks.py paths <evidence-file> [<adr-draft> ...]
uv run --locked python scripts/decide_checks.py matrix <evidence-file>
uv run --locked python scripts/decide_checks.py evaluators <eval-file> ... --producer-model <id>
uv run --locked python scripts/decide_checks.py response-coverage <eval-file> ... --response-file <file>
uv run --locked python scripts/decide_checks.py adr-sections <adr-draft>
uv run --locked python scripts/decide_checks.py subagent-exclusions <brief-file> ...
uv run --locked python scripts/decide_checks.py subagent-claims <evidence-file>
```
Each subcommand is one of the eight checks (checks 2 and 3 share the `matrix` subcommand — one
parse, two defect classes). Exit `0` clean, `1` at least one defect (named), `2` internal error
— an error is never a silent pass (the `preflight_contract` posture, reused).

## Honest limits (recorded, not patched around)

- **`.claude/skills/preflight/SKILL.md`, cited by this lane's own contract as the reuse target
  for path resolution, does not exist in this tree.** Check `paths` instead reuses the real,
  already-shipped mechanism: `scripts/preflight_contract.py::verify`, the same one `/preflight`
  wraps. That module predates this lane; it is not a `lane-scope-guard` artefact.
- **`ecosystem/excluded-roots.yaml`, cited "as merged by `lane-scope-guard`", does not exist
  either — `lane-scope-guard` FAILED terminally (`to-browser/SESSION-integrator-wave5b-n4
  -2026-09-26.md`, STATE line 2026-09-27T12:45) and was never re-admitted itself, unlike the
  four lanes downstream of it.** `decide_checks.load_excluded_roots` falls back to the one root
  this batch's own proposal names by hand ("OneDrive - Blue Yonder") and reads the real file
  transparently once it lands — `ROWS-OWED`, not a block on this command.
- The matrix and subagent-claims markup contracts above are this module's own design, built to
  the two source proposals' Step-5 specifications — they do not retrofit the historical
  free-prose proposals that motivated them, which predate this mechanism.
- This command does not call any model itself; it names the shape of the run and gates its
  artifacts. A future lane may wire the fan-out/evaluator calls themselves — out of this
  contract's `Files you own`.
