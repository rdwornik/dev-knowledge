# Lane contract — dependency-graph organ (rustworkx) + reusable-workflows re-test

**Dispatch stamp.** This file is the frozen brief as dispatched, committed as the lane's FIRST
commit before any work. Verbatim; no edits, no annotations.

**Lane:** cloud, docs-only · **Base:** `origin/main` @ `70aa5f2` · **Branch:**
`claude/technical-graph-and-workflows`
**Output of record:** `docs/audits/2026-08-21-technical-graph-and-workflows.md`
**Input of record:** `docs/audits/2026-08-21-technical-library-first-research.md`

---

```
# CLOUD LANE — DEPENDENCY-GRAPH ORGAN (rustworkx) + REUSABLE-WORKFLOWS RE-TEST

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — research + spec; docs-only | high |

Cloud lane, docs-only. FIRST COMMIT = dispatch-stamp (this prompt as
`docs/audits/2026-08-21-technical-graph-and-workflows-lane-contract.md`). Fresh branch off
origin/main. No index regeneration, no JOURNAL, no row edits, no rulings, no dependency added.

INPUT OF RECORD: `docs/audits/2026-08-21-technical-library-first-research.md` (read Track 1 §1.2
and Track 2 §2.4 first — this lane extends them, never re-derives them).

## TRACK A — the dependency-graph organ, now that a consumer EXISTS
ARCHITECT RULING carried into this lane: the operator has named the consumer — **dependency
management**. Under ADR-105 that clears activation for the query classes that genuinely need a
graph. Library choice is RULED: **rustworkx**, on the report's own measurement (7.1 MB, no
scipy, pagerank built in, released 2026-07-30) — networkx is not reconsidered.

1. **Enumerate the 18 nontrivial SCCs your predecessor measured.** For each: the member nodes,
   the edge that closes the cycle, and a one-line read — REAL problem (a doctrine loop, a
   mutual dependency that should be a hierarchy) vs BENIGN (cross-references between peer
   canon). This is the evidence that decides whether the organ is worth building at all —
   report it honestly even if most are benign.
2. **Spec the organ** (spec only, no build): CLI shape, where the edge extraction lives (reuse
   the report's extractor logic — cite it, don't reinvent), which queries are SQL (reachability,
   orphans, degree) and which are rustworkx (SCC/cycles, impact-of-move, centrality), the output
   contract, and where it plugs in (`audit.py` check vs standalone command vs dashboard section).
   State the LOC estimate and the failure modes.
3. **The gate question:** should cycle detection be a FAIL leg, a WARN leg, or a report-only
   command? Recommend with the reason; the architect rules.
4. Name the row/intake shape this needs, and whether it supersedes or complements `[#534]`.

## TRACK B — reusable workflows, re-tested under the CORRECTED premise
The previous rejection rested partly on a premise the architect has since corrected: private
caller repos CAN call workflows from private repos when the called repo's Actions → Access
policy allows it; no public repo is needed; the "outside collaborator" warning is inert here
(personal account, zero orgs, zero outside collaborators — verify this with `gh` rather than
assuming). The rejection's OTHER two grounds stand and are NOT reopened: file distribution
(floor/mesh must exist in the clone) and offline operation.

1. **Scope the survivor**: reusable workflows as a carrier for FLEET-WIDE CI GATES ONLY — the
   checks that run in Actions on a consumer's push, defined once in the hub, referenced by tag.
   Which of our gates could run there, and which cannot (need local files, need the hub tree,
   need Windows)?
2. **Cost, measured not assumed**: each reusable-workflow call starts its own job/runner. Given
   30% of the 2,000 monthly Actions minutes are already consumed, model the minute cost at
   realistic push frequency across the fleet. If the cost exceeds the benefit, say so.
3. **The setup, concretely**: exact settings path + `gh api` equivalent to flip the access
   policy, the `uses: owner/repo/.github/workflows/x.yml@vTAG` form, and how versioning
   interacts with our deployed-versions record.
4. Compare against the incumbent for this same job: our existing pre-commit remote hook repo
   (ADR-71, already adopted, tags v1.0.0–v1.3.1). Does the workflow layer add anything the hook
   layer does not already give us? Honest answer, including "no".

## OUTPUT
ONE artifact `docs/audits/2026-08-21-technical-graph-and-workflows.md`: Track A (SCC table,
organ spec, gate recommendation, row shape) then Track B (survivor scope, minute cost, setup,
verdict vs the hook layer). Commit, push, STOP packet: the SCC real/benign split in one line,
the organ's LOC estimate, and Track B's verdict in one line.
NOT: no build, no dependency added, no rulings, no row edits, nothing outside the artifact.
```
