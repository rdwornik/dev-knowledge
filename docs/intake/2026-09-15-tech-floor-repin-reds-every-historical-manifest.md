---
intake-id: 100
status: DRAFT
origin: batch-z integrator seat (CC, Opus 5), 2026-09-15 — surfaced by the SUITE-BASELINE-FREEZE judging rule refusing lane z-0's merge with five release-lint failures
consumed-by:
---

# When the floor template changes, every historical manifest goes red, and nobody has ruled whether it should

## Problem / motivation

Lane z-0 changed `templates/child-methodology-floor.md.tmpl` and moved its sidecar
`4d268f32..` → `e8c62d24..`, re-pinning `anchors.floor_sha256` in `deploy/manifest-v1.5.0.yaml`
to match. `deploy/release_lint.py --version v1.5.0` reports **0 FAIL**, which is what the lane
measured and reported honestly.

**Every other tagged manifest now fails.** `v1.1.0`, `v1.2.0`, `v1.3.0`, `v1.3.1` and `v1.4.0`
still pin `4d268f32..`, and check **C5-floor-pin** compares each of them against the **live**
sidecar:

```
release-lint FAIL C5-floor-pin: spec pin 4d268f329a7e.. != sidecar e8c62d24a019..
```

Five tests that were green at the freeze are now red: `test_live_hub_state_is_green`,
`test_live_v120_state_is_green`, `test_cli_green_exit_0`, `test_unmutated_copy_is_green`,
`test_missing_tag_is_warn_not_fail`.

**The lint is internally inconsistent about what a historical manifest is.** In the same run,
against the same file, check **C7** says:

```
release-lint ok  C7-doc-shapes: v1.2.0 is not the current manifest (v1.5.0) — released/historical,
                 not compared to live constants
```

So C7 already knows a released manifest describes what that version shipped and must not be held
to today's constants. **C5 does not.** One check treats the file as history and the next treats it
as a live claim.

**There is no precedent, and that is the actual problem.** `deploy/manifest-v1.5.0.yaml`'s own
header says this is *"THE FLOOR TEMPLATE CHANGED, and `anchors.floor_sha256` moves with it — **the
first time**"*. The floor template has never changed before, so the repo has never had to answer
this, and the first answer given will be the precedent.

## Scenarios (+1 view)

**As the integrator, judging a merge.** Lane z-0's merge measured 8 failures outside the frozen
51. Three were the index debts the lane declared and I paid. **Five are these**, and they are not
a debt anybody declared — the lane measured `v1.5.0`, found it green, and reported that truthfully.
Nothing instructed it to measure the other six manifests.

**As whoever fixes this.** Two resolutions, and they disagree about what a tagged manifest *is*:

- **Re-pin all historical manifests to the live sidecar.** Cheap, greens the suite immediately —
  and asserts that `v1.2.0` shipped a floor it did not ship. It makes the manifests a mirror of
  today rather than a record of a release.
- **Make C5 version-aware, exactly as C7 already is.** A released manifest's floor pin is compared
  to what that version shipped, not to the live sidecar. Costlier, needs RED-first witnesses, and
  is the reading the lint's own C7 already commits to.

**As a consumer repo.** Whether a consumer pinned to an older methodology version should receive
the new floor is the substance underneath both options, and it is not answered anywhere.

## Functional requirements

- **Must:** the two checks in one lint agree about whether a non-current manifest is history or a
  live claim. Today C5 and C7 answer differently about the same file in the same run.
- **Must:** a floor-template change has a **defined, mechanical consequence** for every tagged
  manifest, rather than greening whichever manifest the changing lane happened to measure.
- **Should:** whatever the ruling, a lane that changes the floor template is told at commit time
  which manifests it has just invalidated — the cost should not surface two merges later as five
  red tests attributed to the wrong cause.

## Acceptance criteria (ex-ante)

1. `deploy/release_lint.py --version <V>` for **every** `deploy/manifest-*.yaml` reports 0 FAIL on
   a clean tree, with C5 and C7 giving the same answer about whether `<V>` is historical.
2. A RED-first witness exists: mutating the floor template without discharging the ruled
   consequence FAILS, naming the manifests affected.
3. The five named tests are green, and green **because the question was answered**, not because a
   pin was copied to silence them.

## Non-goals

- Not a change to lane z-0's floor content. The floor change itself is wanted; only its blast
  radius across tagged manifests is unruled.
- **Not a decision made by the integrator.** Recorded here precisely because choosing between the
  two resolutions decides what a tagged manifest means, which is an architect's question under
  ADR-108 §A and not an integration act.

## Impact sketch (4+1 lite)

- **Logical:** what a tagged manifest asserts — a historical record, or a live mirror.
- **Process:** every future floor-template change; the release-lint gate.
- **Development:** `deploy/release_lint.py` C5, or six manifest files.
- **Physical:** untouched.

## Open questions

- Does a consumer pinned to an older methodology version receive the new floor? The answer settles
  the resolution rather than the other way round. **Architect question — recorded, not answered.**
- Are there other anchors (`plugin_version`) with the same latent split, currently invisible only
  because they have not moved?
- Is `test_missing_tag_is_warn_not_fail` failing for this cause or for its own? It is grouped here
  because it went red in the same run and shares the fixture, which is an association and **not**
  an established cause.

## Status

DRAFT — CANDIDATE under the ADR-111 funnel. **Blocking a clean batch-Z close:** five failures sit
outside `logs/SUITE-BASELINE-FREEZE.md`'s frozen 51 and are therefore a regression that refuses
lane z-0's merge under the operator's own rule. They are **not** absorbed into the frozen set, and
the merge is recorded as not-yet-clean rather than waved through. Claimed by `[#765]`, the open row
that owns lane z-0's deliverable.
