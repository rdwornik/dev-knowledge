# LANE-g-621-c7 — the freshness registry is changeable without lying about shipped manifests

**Date:** 2026-09-03 · **Class:** technical · **Arc:** `[#621]` · **Lane:** `lane-g-621-c7`
· **Branch:** `worktree-lane-g-621-c7` · **Seat:** CC (Sonnet 5)

## 1 · What this is

The revised contract superseding `lane-g-621-freshness-absent`'s escalation
(`docs/audits/2026-09-02-technical-lane-g-621-freshness-absent.md`), which parked two items
after reproducing real conflicts: removing `VISION` from the live freshness registry REDs
released, tagged manifests (`release_lint` C7 compares every linted manifest's `doc_shapes`
against LIVE constants, unconditionally), and flipping absence-handling from skip to FAIL
REDs four tests built on minimal fixtures. This lane's Done-contract named the actual defect
— C7's unconditional live-comparison — as the thing to fix, which unblocks both parked items.
All four Done-contract items landed; nothing escalated.

## 2 · Closure 1 — C7 binds a manifest to the constants AS OF ITS OWN VERSION

**Option taken (CC default, contract explicitly deferred this to CC's judgment):** bind C7's
live-constant mirror to the CURRENT manifest only, where "current" is **structural** — the
highest-versioned `deploy/manifest-v*.yaml` FILE present in `repo_root` (`_current_manifest_version`
in `deploy/release_lint.py`), not tag-probed. A manifest superseded by a newer one on disk
PASSes C7 without comparison. "Or a versioned snapshot if one exists" was the contract's other
named option; no such per-release snapshot mechanism exists in this codebase, so "current only"
is the plain default rather than inventing a new snapshot format for this lane.

**Why structural rather than tag-probed:** `lint()`'s `tag_probe` is caller-injected, and the
existing test suite's injected probe always reports "resolved" regardless of a manifest's real
release status (`test_missing_tag_is_warn_not_fail` needs the OPPOSITE — an UNRESOLVED tag — to
stay a WARN, not a FAIL, so tag resolution already carries a different meaning). Reusing it to
mean "released" would make C7's teeth inert under every test that also needs C2 green. A
manifest file's presence has no such double duty.

**Verified against the real repo:** v1.1.0/v1.2.0 (superseded by `deploy/manifest-v1.5.0.yaml`)
now PASS C7 trivially; v1.5.0 (current) still gets the full mirror and is green
(`test_current_manifest_still_engages_the_live_c7_mirror`). Mutation-detection coverage is
unchanged: the injected-mismatch tests run inside an isolated tmp root carrying only ONE
manifest file, where that file is trivially "current," so the teeth still fire.

## 3 · Closure 2 — VISION leaves the freshness registry, in both places

Removed from `scripts/canonical_docs.py FRESHNESS_FILES` (six-tuple → five) and
`scripts/canonical_freshness_gate.py:49`'s `DEFAULT_FRESHNESS_FILES` fallback literal; the
equality test between them (`test_freshness_gate_consumer_fallback_equals_the_registry`) STAYS
and passes. `deploy/manifest-v1.5.0.yaml`'s `VISION.md.freshness_gated` flipped `true → false`.
VISION keeps every OTHER registry membership (`CANONICAL_RETIRED`, `CANONICAL_SPINE`, casing
checks) — only the freshness-review requirement is removed.

**No special-casing VISION in any check's logic** (the anti-pattern the contract named): only
registry membership and the one draft manifest that declares it moved. Everything else is
mechanical fallout: `tests/test_release_lint.py`'s `make_root()` now syncs each `doc_shapes`
entry's `freshness_gated` flag to the LIVE registry generically (by filename lookup, not by
naming VISION) before writing its tmp-root fixture — that fixture represents "the current
manifest," which must track live truth as the registry evolves, unlike a real released manifest
frozen at its own version. Two tests retargeted from VISION.md (no longer gated) to a file that
still is: the "freshness-gated-set-drift" mutation test → CLAUDE.md;
`test_enforcement_coverage.py::test_freshness_fire_stales_a_quoted_last_reviewed` → ARCHITECTURE.md
(the new first entry in `DEFAULT_FRESHNESS_FILES`).

## 4 · Closure 3 — an absent registry member FAILs, never skips (Z-G4)

`canonical_freshness_gate.evaluate()`'s `if not fpath.exists(): continue` (silent skip) is now
`fails.append(...); continue`. lane-g-621-freshness-absent's Attempt A tried exactly this flip
and reverted it because it REDs four tests built on minimal fixtures that didn't declare every
registered file present. Per this contract: fix the fixtures, not the FAIL.

Repaired, all mechanical (no logic weakened):

- `test_evaluate_absent_file_fails` (direct unit test, no fixture) — assertion inverted from the
  RED-tests commit.
- `test_gate_exits_0_when_fresh` — now writes+commits every `DEFAULT_FRESHNESS_FILES` member
  fresh, not just the one file under test; `_doc()` creates parent dirs for path-shaped members.
- `test_freshness_absent_file_fails` (test_audit.py, was `..._skipped`) — assertion inverted.
- `test_freshness_real_git_committed_stale_fails` / `test_freshness_real_git_equal_date_passes`
  — retargeted VISION.md → CLAUDE.md (VISION left the registry in closure 2) and now seed+commit
  every `_FRESHNESS_FILES` member fresh via a new `_write_and_commit_all_fresh()` helper before
  staling/re-stamping the one file under test.
- `test_freshness_a2_edited_since_review_fails` / `test_freshness_a2_dominates_a1` — retargeted
  VISION.md → ARCHITECTURE.md / CLAUDE.md.
- `tests/fixtures/repo-with-structural-checks/` — the shared synthetic-repo fixture behind
  `test_audit_run_passes_structural_checks_on_synthetic_repo` was missing 5 of the 8 live
  `_FRESHNESS_FILES` members (`docs/handoffs/README.md`,
  `protocols/{ESSENTIALS,SESSION_SETUP,AI_COUNCIL_PROCESS,DEFINITION_OF_DONE}.md`) and relied on
  the old skip-on-absence behavior. Added all 5, each with a fresh (2099-01-01) `last_reviewed`
  stamp; `tests/fixtures/README.md` updated.

## 5 · Closure 4 — verification

`tests/test_release_lint.py` green with `git diff --stat b91b82cf..HEAD -- deploy/manifest-v1.0.0.yaml
deploy/manifest-v1.1.0.yaml deploy/manifest-v1.2.0.yaml deploy/manifest-v1.3.0.yaml
deploy/manifest-v1.3.1.yaml deploy/manifest-v1.4.0.yaml` **exactly empty** — every released manifest
byte-identical across the whole lane. That empty diff is the proof: the lint was re-shaped, not
the history rewritten.

Full targeted run (`test_canonical_docs`, `test_canonical_freshness_gate`, `test_release_lint`,
`test_audit`, `test_enforcement_coverage`, `test_gen_intake_index`, `test_lived_sandbox_observer`):
first pass **478 passed, 1 skipped, 2 failed**
(`test_check_fleet_parity_green_on_live_repo`, `test_anchor_gate_probe_distinguishes_installed_from_absent`
— both pre-existing, already in the committed base failed-set
`docs/audits/2026-09-02-verification-base-failed-set-1e064921.json`). A re-run minutes later
(after this artifact was added) showed **4 failed**: those same two, plus
`test_health_ok_with_registered_repo` and `test_health_stays_ok_with_na_status` — both invoke
`aud.cmd_health` against the live repo via `CliRunner`, and both fail on the identical single
cause (verified with `--tb=long`): `[!!] journal_spine_anchor: 1 first-parent spine entry(ies)
above the disposition floor 24882f8cc carry no JOURNAL anchor: b62b8cd6` — see §6, same
concurrent, pre-existing, out-of-scope defect, newly visible because `main` moved mid-session.
Not caused by this diff: no canonical_freshness/VISION-related finding appears in either
failure's full report. `ruff check` clean on every touched file.

## 6 · Deviation disclosed (Q10) — `SKIP=audit-health` on two commits

Mid-lane, `main` (verified == `origin/main`) advanced to `b62b8cd6` ("correct-g7-claim"), merged
concurrently by a peer session, whose `journal_spine_anchor` finding is FAIL — pre-existing,
already pushed, unrelated to this diff. The commit-time `audit-health` gate scans the whole
`main` first-parent spine regardless of which branch is being committed to, so every commit in
every worktree wedges on it until it's fixed. Fixing it means writing `JOURNAL.md`, which this
lane's frozen contract explicitly reserves for the integrator ("No JOURNAL entry — that is the
integrator's surface"). Both `fix(canonical-docs)` and `fix(canonical-freshness-gate)` commits
therefore carry `SKIP=audit-health`, declared in each commit body per the repo's own sanctioned
single-hook-bypass convention (AGENTS.md "Gates" section) — the disclosure discharges the
reporting duty; it does not authorize anything beyond this one named hook on these two commits.

The same wedge also surfaces as two test-suite failures (§5) that were NOT present in an earlier
run of the identical targeted set minutes before — `test_health_ok_with_registered_repo` and
`test_health_stays_ok_with_na_status`, both invoking `audit.py health` against the live repo.
Confirmed by full traceback: the only FAIL-tier line in either report is `journal_spine_anchor`
naming `b62b8cd6`; nothing related to this lane's diff. **Integrator: `journal_spine_anchor`
needs a fix on `main` independent of this lane — until then, `audit.py health` and the
`audit-health` pre-commit hook FAIL for every worktree in this repo, not just this one.**

## 7 · C4 generalization check (contract's sibling-anchor question)

The contract asked whether this lane's C7 re-shape generalizes to `release_lint` **C4**
(`anchors.plugin_version` pinned to the LIVE `plugin.json` across six manifests, five released
— the identical shape, hit by G4). **It does generalize, mechanically**: C4 could bind to
`_current_manifest_version()` exactly as C7 now does, and the same "released manifest is frozen,
not compared to live" argument applies verbatim. **Not extended here** — write-scope for this
lane is `deploy/release_lint.py` + the two registry files + the one manifest + matching tests,
and C4 is explicitly named out-of-scope by the contract ("report, do not fix"). This is the
architect's call.

## 8 · Diff summary

```
deploy/release_lint.py                                              (C7 re-shape)
scripts/canonical_docs.py                                            (VISION out of FRESHNESS_FILES)
scripts/canonical_freshness_gate.py                                  (fallback sync + absence FAILs)
deploy/manifest-v1.5.0.yaml                                          (VISION.md freshness_gated: false)
tests/test_release_lint.py                                           (RED tests + fixture sync + retargeted mutation)
tests/test_canonical_docs.py                                         (RED test: VISION out of both places)
tests/test_canonical_freshness_gate.py                                (RED test + fixture repair)
tests/test_audit.py                                                   (absence-FAIL fixture repairs, VISION retargeting)
tests/test_enforcement_coverage.py                                    (VISION -> ARCHITECTURE retargeting)
tests/fixtures/repo-with-structural-checks/{docs,protocols}/*.md      (5 new files, fixture repair)
tests/fixtures/README.md                                              (doc update)
```

Four commits on `worktree-lane-g-621-c7`, all RED-first: `test(release-lint)` (RED),
`fix(release-lint)` (closure 1), `fix(canonical-docs)` (closure 2), `fix(canonical-freshness-gate)`
(closure 3). No merges, no pushes to `main`, no index regeneration, no JOURNAL entry — per contract.

## Terra pre-merge review (integrator, 2026-09-03)

Reviewer `codex exec review --base main`, concurrency 1. **Wall-clock 108 s.**

**Severity tally: HIGH/P1 = 1 · MED = 0 · LOW = 0. CONFIRMED with the blast radius MEASURED, and
fixed before merge.**

| # | Sev | Finding | Disposition |
|---|---|---|---|
| 1 | P1 | Closure 3's unconditional absence-FAIL would block **every commit in every consumer repo**: this gate is byte-copied into consumers as a pre-commit hook, and the registry names two documents no consumer carries | **FIXED** — presence-required vs presence-optional split |

**The blast radius was measured, not argued.** The enforcement-mesh carrier byte-copies
`scripts/canonical_freshness_gate.py` into each consumer as a pre-commit hook
(`entry: python scripts/canonical_freshness_gate.py`), and `DEFAULT_FRESHNESS_FILES` registers
`protocols/ESSENTIALS.md` and `docs/handoffs/README.md`. Checked against the three live consumers
on 2026-09-03:

```
corp-monorepo   protocols/ESSENTIALS.md ABSENT   docs/handoffs/README.md ABSENT
ai-council      protocols/ESSENTIALS.md ABSENT   docs/handoffs/README.md ABSENT
win-tooling     protocols/ESSENTIALS.md ABSENT   docs/handoffs/README.md ABSENT
```

Three repos, every commit, permanently — from a lane whose closure text reads "never weaken the
FAIL". The lane obeyed that text exactly; the text did not say which files must exist.

**THE FIX IS NOT A WEAKENING, AND THE REPO ALREADY HELD THE ANSWER.** `canonical_docs` puts
`ESSENTIALS` in `CANONICAL_OPTIONAL` and states *"Presence is required only for
CANONICAL_MANDATORY"*. Z-G4 targets a check that **cannot compute its ground truth**; for an
optional document, *absent* IS the ground truth — a known, correct state. So:

```
presence-REQUIRED (absent -> FAIL)      ARCHITECTURE.md, CLAUDE.md, CONTRIBUTING.md
presence-OPTIONAL (absent -> REPORTED)  docs/handoffs/README.md, protocols/ESSENTIALS.md
```

Derived from the registry at the hub, literal in the consumer copy, the two pinned equal by
`tests/test_canonical_docs.py`. **The absence is still REPORTED** — Z-G4's real target is
silence, not non-fatality.

**Proven both ways on the measured consumer shape:** three required files present and both
optional absent → `FAILS: none`, commits unblocked, two warns emitted; remove `CLAUDE.md` →
`FAILS: ['CLAUDE.md: absent …']`, Z-G4 still bites.

**One of the lane's own tests was narrowed, and it matters why.**
`test_evaluate_absent_file_fails` asserted against a synthetic `DOES_NOT_EXIST.md` — a name in no
corpus at all, so it exercised the branch that now belongs to presence-OPTIONAL entries and would
have gone **green against the wrong half of the split**. It now asserts on `CLAUDE.md`, where
Z-G4 actually bites, with the optional half pinned by its own test.

`tests/test_canonical_freshness_gate.py` + `test_canonical_docs.py` + `test_release_lint.py`:
**101 passed.**
