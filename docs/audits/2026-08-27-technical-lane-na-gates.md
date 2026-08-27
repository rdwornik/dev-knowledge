---
date: 2026-08-27
lane: lane-na-gates
branch: worktree-lane-na-gates
rows: "[#591] [#592] [#595] [#596]"
consumers: "[#591], [#592], [#595], [#596] — the four rows this lane executes; the morning integrator's merge queue"
---

# LANE na-gates — four gate mechanisms on existing rows

**Consumer:** the four rows `[#591]`, `[#592]`, `[#595]`, `[#596]` (each row's done-when is the
contract of record), plus the morning integrator's merge queue. This artifact is the lane's end
packet; it is what the batch close packet reads.

Night run, LOCAL worktree, gates armed, no operator questions. Four rows, all mechanism-shaped,
all RED-first. One commit per row plus one terra-fix commit and one sync-merge.

## 1. What landed

| Row | Commit | Detector | Adapter | Tests |
|---|---|---|---|---|
| `[#591]` substrate validator, layer 2 | `b95edd31` | `scripts/validate_substrate.py` + `ecosystem/substrate-registry.yaml` | `check_substrate_declaration` | 27 |
| `[#592]` dispatch drift organ | `dd76e2b8` | `scripts/dispatch_drift.py` | `check_dispatch_drift` | 22 |
| `[#595]` consumer-at-landing gate | `96da31c8` | `scripts/consumer_at_landing.py` + `ecosystem/audit-consumer-baseline.json` | `check_consumer_at_landing` | 32 |
| `[#596]` family-3 proof layer | `f8ae0f6d` | `scripts/proof_layer.py` + `ecosystem/proof-layer-baseline.json` | `check_proof_layer` | 20 |
| terra fixes (3 HIGH) | `2d531321` | — | — | +8 |
| sync-merge `main` (`066f6ecd`) | `47ea528b` | — | — | — |

`ALL_CHECKS` 46 → 50. Five count pins bumped per commit, `ecosystem/doc-counts.md`
regenerated, four `exempt:` entries added to `ecosystem/doc-code-edge.yaml`.

**All four checks are green on the live tree**, each measured before arming:

```
substrate_declaration  pass  0 contracts landed on/after 2026-08-27 agree; 5 grandfathered
dispatch_drift         pass  tier host: 12 literal commands resolve; /lane-boot names `dispatch`
consumer_at_landing    pass  745 artifacts; unconsumed 524 at baseline; 744 grandfathered
proof_layer            pass  243 guards across 31 modules at baseline; 10 on an enforcement runner
```

## 2. Arm levels, and the evidence behind each

Every FAIL arm is against a corpus measuring **zero** — the `check_adr_status_grammar`
evidence bar ("both measure 0 on the live corpus, so arming them is free and they cannot RED a
clean tree"). Every WARN arm cites the `funnel_coverage` ruling: arming RED against an
unmeasured corpus turns the gate off on day one.

- `[#591]` — three REFUSE legs at **FAIL**, `substrate-second-local-writer` at **WARN** (the
  row's own word). Post-cutoff corpus measures 0.
- `[#592]` — **FAIL** on an unresolvable command; **WARN** for the shell-less tier. 0 findings
  live.
- `[#595]` — leg 1 (declaration at landing) at **FAIL**, post-cutoff corpus 0; leg 2 (the
  consumption ratchet) at **WARN** against 524 named pre-existing artifacts.
- `[#596]` — **WARN** identity ratchet against 243 named pre-existing guards.

## 3. Real findings on the live tree

**`[#591]` found four genuine refusals in the committed batch-1 launch contracts** — one
`codespaces` near-miss for the ruled `codespace`, and three contracts declaring no substrate at
all. All four are pre-cutoff and grandfathered on this corpus's own ruled precedent
(architect 2026-08-21: *"retro-fitting them would falsify what was actually dispatched"*). They
are reported here rather than laundered into the registry as an alias — `codespaces` is not
ruled vocabulary, and admitting it would make the validator agree with the defect.

**`[#592]` found a live signal on `/lane-boot`** and the refinement it forced is the more useful
result. The first run FAILed on the raw `claude --worktree` form; read at the locator, the match
is the file's own supersession note. A check that refused it would force deleting the
explanation to satisfy the rule the explanation is about. The discriminator is now the ruling's
own — V4 keeps the raw form documented once and *labelled as the fallback* — so a fence FAILs,
an unlabelled prose mention WARNs, and a labelled one is sanctioned.

## 4. Terra review — tally counted from the artifact file

`codex exec` gpt-5.6-terra, high effort, `main..worktree-lane-na-gates`. Artifact:
`docs/audits/2026-08-27-codex-lane-na-gates.md`.

**0 CRITICAL · 4 HIGH · 0 MEDIUM · 0 LOW.** Counted from the artifact, not the wrapper's
summary line. Three HIGH fixed in `2d531321`; the fourth rejected with proof.

| # | Finding | Disposition |
|---|---|---|
| 1 | `consumer_at_landing` — a partially-read governance pool passed as fully resolved | **FIXED** |
| 2 | `consumer_at_landing` — nested artifacts outside both legs | **FIXED**, `DETECTOR_ID` v1→v2 |
| 3 | `proof_layer` — named `skipif` aliases not detected | **FIXED**, a 6× undercount |
| 4 | `journal_anchor` — "removes the batched ancestry lookup" | **REJECTED** — not this diff |

Finding 1 is worth naming plainly: the module written to gate for "a check that cannot compute
its ground truth and reports a non-failing status" contained exactly that defect. Fixed and
regression-tested.

Finding 3 was verified by grep before acting rather than taken on the reviewer's word — the
claim was true and understated. The alias form is the *dominant* form here (18+ modules), and
fixing it moved the measurement from 38 guards / 13 modules to 243 / 31. Fixing it surfaced a
second defect the review did not name: a **compound** condition
(`not _HAS_PRECOMMIT or shutil.which("git") is None`) reported only its first probe, so two
modules that gate a pre-commit enforcement proof on pre-commit's own presence were filed under
`git`. An enforcement runner now wins the tie; self-policing modules 3 → 5.

Finding 4 is a diff-range artifact. `main` advanced under the lane mid-run (`08b0d192` →
`066f6ecd`, a sibling's `[#587]`/`[#588]` perf lane), so `main..HEAD` rendered the sibling's new
work as this branch's removal. `git diff --name-only 08b0d192..HEAD` lists 22 files and
`journal_anchor.py` is not among them; the contract names it Do-NOT-touch and it was not
touched. Cleared by the sync-merge in `47ea528b`.

## 5. Dogfooding results — two defects the lane found in itself

Both were found by running the mechanism against the live tree rather than against fixtures.

1. **Key collision in `proof_layer`.** Keying a guard's identity on its skip *reason* folded six
   distinct `test_audit.py` guards into one identity; a bare `<module>` folded two module-level
   marks into one. The ratchet compares SETS, so a collapsed key makes a real guard invisible
   *and* makes `load_baseline`'s duplicate check reject the baseline recording it.
2. **A heuristic that discriminated nothing.** `self_policing` first inferred intent from how
   often a module mentioned its gated tool; measured live it returned True for **all 38** guards.
   Replaced by a declared roster, which reproduces the sweep's two named exemplars exactly and
   correctly excludes its §9.2 one — the one the sweep calls load-bearing and *correct*.

A third arrived with the sync-merge: five nested launch contracts reported "no resolvable
landing date" because their date sits on the containing directory. Reported-rather-than-assumed
was the right posture; having nothing else to read was the defect. A directory-date fallback now
resolves them.

## 6. Decisions taken per contract defaults (no operator questions, per the brief)

- **Substrate registry home** — `ecosystem/substrate-registry.yaml`. Intake #45's own open
  question names the fork and answers it in the same breath ("alongside `provider-registry.yaml`
  and `tool-versions.yaml`, the established home for declared ecosystem state"); ADR-101 already
  sanctions the directory; and it survives the Layer-3 router landing in win-tooling.
- **YAML over JSON for the registry, JSON for both baselines.** The registry carries doctrine
  projections a human reads; the baselines are machine-generated name lists. JSON also keeps the
  baselines outside `silent_rule_detector`'s `ecosystem/*.yaml` corpus — the measured reason
  `funnel_coverage` chose it. The registry was checked to contain zero normative tokens, so it
  adds nothing to that pool.
- **`exempt:` rather than `coverage_scope:`** for all four checks, each TEMPORARY and bound to
  its row. The rules these legs embody live in immutable ruling records and intakes, not in a
  living doc a `# rule:` marker can point at; and adding a marker to `protocols/PLAYBOOK.md`
  would RED `canonical_freshness` without a genuine end-to-end re-read of a 5,208-line file,
  which is not this lane's to spend.
- **`warn`, never `unavailable`, for every could-not-evaluate path.** `_STATUS_LABEL` renders
  `unavailable` as N/A and `_check_outcome` projects it onto `pass`.

## 7. Pre-existing REDs — reported, not fixed, none of them this lane's

The targeted suite is **green for this lane's diff**. Three failures on the tree are inherited:

- `tests/test_funnel_coverage.py::test_committed_baseline_agrees_with_a_live_measurement` — 44
  artifacts dated 2026-08-23…26. Proof it is foreign: this lane's diff touches **zero**
  `docs/audits/` files; `ecosystem/audit-funnel-baseline.json` is stamped corpus 693 /
  2026-08-23 / sha `52950fa9` against a live corpus of 745, last touched by `065872b8` on
  2026-08-24. Re-measuring it is a curated-baseline touch — an operator decision by that
  module's own docstring, and V-2 escalation class (a).
- `tests/test_audit.py::test_health_ok_with_registered_repo` and `::test_health_stays_ok_with_na_status`
  — both assert `audit.py health` green **on the live repo**, so any foreign FAIL on main's
  spine REDs them from inside any lane.

`audit.py health` is **DEGRADED** on one FAIL, and it is not this lane's:

```
journal_spine_anchor: 066f6ecd (2026-08-27) Merge branch 'worktree-w2a-perf-core'
                      -- the per-commit anchor tax is cut 27.9x [#587] [#588]
```

That is a sibling lane's own merge, landed on main during this run and not yet anchored by its
integrator. A batch lane does not write `JOURNAL.md` (STANDING_RULINGS P-1), so this lane cannot
discharge it. Every commit here therefore carries a declared `SKIP=audit-health` with its
ownership proof written into the commit body — never `--no-verify`, and never a wider SKIP.

**Owed to the integrator:** anchor `066f6ecd` in `JOURNAL.md` at the merge. (`08b0d192`, the gap
at the start of this run, was anchored by the sibling and is now clear.)

## 8. Open items for the integrator

1. **`ALL_CHECKS` union.** Expected and benign per the contract: this lane appends four
   single-line registrations; the sibling tiering lane appends its own. The union resolves to
   whatever count the merged `ALL_CHECKS` holds — the five count pins and `doc-counts.md` need
   one regeneration at integration, not five.
2. **The anchor for `066f6ecd`**, above.
3. **The stale `funnel_coverage` baseline**, above — a curated-baseline touch, deliberately left.
4. **Both new baselines are stamped at this lane's tip.** If integration merges siblings that add
   `docs/audits/` artifacts or `tests/` guards, both ratchets will name them; regenerate with
   `python scripts/consumer_at_landing.py --write-baseline` and
   `python scripts/proof_layer.py --write-baseline` rather than editing either by hand.
5. **`[#592]` costs one `pwsh -NoProfile` spawn (~1 s) per `audit.py health` run.** Stated so it
   is a known line item on a hook that already costs ~200 s, not a surprise.

## 9. Honest limits, collected

Each module states its own; these are the ones that bound what a green verdict means.

- `[#591]` gates the **committed** contract corpus. A contract dispatched from the prompts dir
  and never copied in-tree is checked by nothing, here or elsewhere. Leg 2 is token-based, leg 3
  matches path shapes, and none of them says a contract asks for the *right* work.
- `[#592]` asserts a command **resolves**, not that it behaves; its corpus is Ch8's dispatch-table
  section, which is sound only while the "SOLE literal-command site" ruling holds — and this
  organ does not enforce that ruling. A `host`-tier green is a claim about the machine that ran
  it and no other seat's.
- `[#595]` checks that an artifact **names** a governance surface, not that the surface exists or
  agrees — `[#99999]` passes. Consumption is a substring match, as the diagnostic's was.
- `[#596]` reads `skipif` marks and module-level `pytestmark`; a bare `pytest.skip()` in a test
  body, or a skip reached through a fixture, is **not** detected. A guard on the list is a
  question, not a verdict.

## 10. Footprint

Files added: 4 detectors, 4 adapters, 4 test modules, 1 registry, 2 baselines.
Files edited: `scripts/audit.py` and `scripts/audit_checks/registry.py` (append-only
registrations), `ecosystem/doc-code-edge.yaml`, `ecosystem/doc-counts.md`, and the five
`ALL_CHECKS` count pins. Nothing in the contract's Do-NOT-touch list was opened:
`audit.py` runner internals / `_GATE_MODE`, `journal_anchor`, generators, `templates/handoff`,
`.devcontainer`, and `tasks/` are all untouched.
