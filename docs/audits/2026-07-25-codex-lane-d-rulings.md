# Codex Review — lane-d-rulings

**Date:** 2026-07-25
**Branch:** `docs/lane-d-rulings`
**HEAD:** `d2882c84`
**Diff range:** `89ae1d1d..d2882c84`
**Codex version:** codex-cli 0.145.0
**Mode:** doc-review

---

## Focus

LANE D rulings arc. Governing-document review. The tool routed this to the prose-only
sub-range because .methodology.yaml (a code extension) would otherwise force the code
profile. ALSO REVIEW, under the SAME PROSE RUBRIC, these two surfaces outside the range
(read them yourself, repo is available read-only):
  git show b4ac7d54 -- BACKLOG.md            # Part 1: 5 new rows [#416]-[#420]
  git show 89ae1d1d -- docs/decisions/ADR-92-deploy-runbook-doctrine.md   # append-only amendment marker
  git show 89ae1d1d -- BACKLOG.md            # Part 2 rulings on #403/#405/#402/#348

Specific things to try to falsify:
- ADR-92 amendment marker: does it EDIT the immutable body anywhere (ADR-94 forbids it;
  only an appended marker is allowed)? Does its factual claim hold -- deploy/tool.py
  make_carriers() returns FIVE carriers and manifest-v1.4.0 declares a sixth with
  implemented:false? Is "no decision changes" honest, or does it silently re-decide?
- Closure faithfulness: [#339] closed on a DISJUNCTIVE Done-when's second branch --
  verify the ADR-29 ratification marker really records threshold 300 / state 241 /
  content unmoved. [#262] and [#295] closed on a hand-authored-by-policy kill-candidate
  -- verify both consumer ARCHITECTURE.md files really state it. [#304] closed --
  verify BOTH its Done-when clauses (working arg form AND arg-form table) are satisfied.
- protocols/REPO_ONBOARDING.md arg-form table: is EVERY row correct against the actual
  argument definition in the named script? Any command in the runbook missing from it?
- Over-claim hunt in BACKLOG rulings: [#403], [#405], [#402], [#348] decomposition,
  [#305] defer reason, [#215] reachability edit. Do the stated reasons hold?
- [#348] decomposition: are the reciprocal refs on [#409]-[#412] complete and
  non-contradictory, or does a stale "#348 subsumes this" claim survive anywhere?
- docs/archive/README.md: is the pointer correction accurate and is anything ELSE in
  that file now stale?
- JOURNAL entry: any claim it makes that the diff does not support (counts, SHAs,
  verification results).
- Dangling refs: any BACKLOG row still pointing at a now-CLOSED id (#262/#295/#339/#304)
  in a way that rots.

---

## Findings
## Critical

(none)

## High

### protocols/REPO_ONBOARDING.md:87 — Required `--run-date` omitted from executable verification command

**What:** Both `enforcement_coverage.py` invocations omit its required `--run-date` option.  
**Why:** The advertised command fails immediately; the adjacent note identifies the requirement but does not supply a runnable form.  
**Fix direction:** Include a concrete `--run-date YYYY-MM-DD` in both commands and the arg-form table’s command syntax.

## Medium

### BACKLOG.md:270 — #348 still owns configuration outside its post-decomposition scope

**What:** W7 still requires `AGENTIC_TESTING.md` as “#348 config material,” although #348 now explicitly owns only grooming; fan-out/configuration moved to #412.  
**Why:** This leaves a live planning dependency assigned to the wrong ticket after the decomposition.  
**Fix direction:** Reassign the W7 reference to its actual owner or file a dedicated task.

## Low

(none)
