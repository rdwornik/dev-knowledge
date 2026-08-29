# [#614] lane-b — end-of-lane packet

**Lane:** `lane-b-614-vision-to-readme` · branch `worktree-lane-b-614-vision-to-readme` · batch D · local, commit-and-STOP.
**Contract of record:** `docs/audits/2026-08-29-technical-batchd-launch-contracts/LANE-b-614-vision-to-readme.md`,
sha256 `a17261a0d217727c1779d0cbfffd8cf99c703927a77fe4b30e533180a1b61ca8` — verified byte-identical to the
dispatched copy before any work started.
**Authority:** ADR-114, Accepted 2026-08-29 (AMENDMENT 1). **Row:** `[#614]`.

**Commits, in contract-step order:**

```
7f118161  step 1  enumerate every gate-coupled VISION.md consumer BEFORE any edit
c20d9239  step 2  recreate the root README.md and supersede VISION.md at the hub
d759d872  step 3  run the re-pointed P1a probe; prove P1b byte-identical
<this>    step 4  the three ADR-114 decommission rows + this packet
```

---

## 1. Done-contract, item by item

| # | Item | Discharge |
|---|---|---|
| 1 | enumeration is the FIRST artifact, before any edit | `docs/audits/2026-08-29-technical-614-consumer-enumeration.md`, committed at `7f118161`; the tree was untouched until it landed |
| 2 | P1a re-pointed **and EXECUTED**, output in the packet | `templates/handoff/v5/PROBES.md.tmpl:81`; run at `d759d872`, output verbatim in §2 below and in `docs/audits/2026-08-29-verification-614-p1a-probe-evidence.md` |
| 3 | `ARCHITECTURE.md` Ch1 Layer-2 line survives VERBATIM | **byte-identical, hashed** against pre-lane main `902b621b` — §2 |
| 4 | nine members' `canonical-doc-vision` parity row resolved in ONE act | one edit to that row in `ecosystem/parity-surfaces.yaml`; tier and probe path unchanged, `reason` re-authored — §3 D-2. A **separate** `root-readme-md` row was also added, forced by the root-sweep — §3 D-2b |
| 5 | ZERO immutable / append-only files edited | verified as a class — §5 |
| 6 | ADR-114's three decommission surfaces each become a backlog row | `[#620]`, `[#621]`, `[#622]` — §4 |
| 4' | English, hyphen-only names, logging not print, `pytest` green | no new script or CLI was written; suite evidence in §6 |

## 2. P1a EXECUTED (done-contract item 2) and P1b byte-identity (item 3)

```
$ grep -A4 '^## Vision' README.md
## Vision

`.dev-knowledge` is a universal LLM-driven development guide and
methodology framework. Its **doctrine is host-independent**: the
conventions it defines, and the hub-local validators, generators and gates
$ echo $?
0
```

**P1a: PASS.** The probe resolves against the new `README.md`, exits 0, and returns a section whose
opening sentence is substring-matchable — which is all P1a asks. Run, not diff-read.

```
$ git show 902b621b:ARCHITECTURE.md > /tmp/arch_main.md
$ sed -n '/^## Purpose \[CORE\]/,+6p' /tmp/arch_main.md | sha256sum
ce3c688e7a5b4f0bf94d8643f4c4033b22249f1d26b2e749cf4d45dec558ad7c  -
$ sed -n '/^## Purpose \[CORE\]/,+6p' ARCHITECTURE.md | sha256sum
ce3c688e7a5b4f0bf94d8643f4c4033b22249f1d26b2e749cf4d45dec558ad7c  -
$ sed -n '/^## Purpose \[CORE\]/,/^## Codemap/p' /tmp/arch_main.md | sha256sum
7e702f5d09936795e9834ee81a1ebce86d22158640ae351c0013439cb078f78f  -
$ sed -n '/^## Purpose \[CORE\]/,/^## Codemap/p' ARCHITECTURE.md | sha256sum
7e702f5d09936795e9834ee81a1ebce86d22158640ae351c0013439cb078f78f  -
```

**P1b: BYTE-IDENTICAL**, on the probe's own six-line window **and** on the whole `## Purpose [CORE]`
chapter to the next H2 — the wider hash deliberately, because matching only the lines the probe
reads would leave the rest of the guarded chapter unproven.

## 3. The decisions this lane took under contract defaults — reported, not asked

The V-2 budget escalates on (a) curated-baseline touches, (b) rule-vs-ruling conflicts, (c) fork
classes with no standing ruling. **Nothing here is one of those.** Each is a measurement plus the
contract's own words.

**D-1 · `VISION.md` is NOT deleted, and the enumeration is what proves that is right.**
`[#614]`'s row names four acts including *"archive `VISION.md`"*; the **frozen contract's Steps name
only the first three**, its done-contract names no archival, and its write-scope lists `VISION.md`
as an editable file. Deleting it breaks, in one commit and all outside this lane's write-scope:
`check_vision_md`, `check_adr38_baseline`, `check_canonical_structure` (the five-H2 spine, mirrored
in five live deploy manifests), `canonical_freshness` + audit #10, `validate_doc_rot`,
`validate_doc_structure`, `session_end_backpressure`, `consumer_at_landing`, `nopack_sandbox`,
`gen_handoff._vision_extract`, `conformance-hub.js`, the ×9 parity MUST row, and **91 `tests/`
occurrences — `tests/**` being lane-a's frozen write-scope in this same batch.** So `VISION.md` is
retained, marked superseded, keeping frontmatter and spine, with its normative bodies **migrated
out** to pointers rather than duplicated.

**D-2 · the parity probe path does NOT move.** Measured on the operator's disk 2026-08-29:

```
consumer root README.md:  terminal-setup YES · win-tooling YES
                          ai-council no · corp-monorepo no · corp-ops no
                          corp-sca-time-automation no · demo-prep no · life-architect no
                          -> 2 of 8
```

`canonical-doc-vision` is `{hub: MUST, consumer: MUST}` — the tier the done-contract restates, i.e.
the tier that does **not** move. A probe flip would turn **six of eight** consumers RED in one
commit, and the contract itself says *"a partial resolution breaks parity fleet-wide"*. The ONE act
that resolves all nine is re-authoring the row so it is **true after the supersession**: `VISION.md`
is still tracked in all nine, the hub's front door is `README.md`, and the filename migration is
ADR-114 option (C)'s sequenced program (`[#621]`). The `&own-prov` YAML anchor is defined on this
row and referenced by six siblings, so provenance was deliberately **not** appended — doing so
would have silently attributed ADR-114 to `canonical-doc-architecture` and five others.

**D-2b · a second parity row WAS needed, and the enumeration got its shape wrong — corrected here
rather than smoothed.** The enumeration artifact (§2.4) declined to add a `canonical-doc-readme`
row and said so. That reasoning stands for a `canonical-doc-*` row. What the tree actually required
is a different family: `fleet_parity`'s **root-sweep** WARNs on *any* undeclared top-level entry, so
the new `README.md` immediately produced

```
.dev-knowledge root-sweep WARN-undeclared: top-level entry 'README.md'
is not in the template for role 'hub'
```

and `tests/test_audit.py::test_check_fleet_parity_green_on_live_repo` went RED. **Found by running
the suite, not by reading the census** — and it is exactly the class the census could not have
found, because it is a consequence of *adding a root file*, not of *referencing `VISION.md`*. The
fix is `root-readme-md`, `{hub: MUST, consumer: LOCAL}`, `value: conditional`, placed beside and
modelled on the landed **`root-agents-md`** row that `[#577]` added for the same reason under
ADR-115. `consumer: LOCAL` is the measured tier (2 of 8), not a preference, and it is a
**forward-only add — no member goes RED**. `canonical-doc-vision` itself is still untouched in
tier and probe path, so D-2 above stands as written.

**D-3 · `README.md` enters `SANCTIONED_TIER1_FILES` as a LITERAL, not via `CANONICAL_MANDATORY`.**
ADR-114's `Amends` line requires the enum to gain it (and that enum is also the gate that would
otherwise BLOCK the add — Rule A refuses an unsanctioned top-level file). The literal shape follows
the landed **ADR-115 `AGENTS.md` precedent** one line above it, for the opposite reason: `AGENTS.md`
is Tier-1 but not canonical; `README.md` is canonical in substance at the hub but promoting it into
`CANONICAL_MANDATORY` would enrol it in `ADR38_BASELINE_REQUIRED` and every consumer's canonical-set
check while six of eight children carry no README. That promotion is `[#622]`.

**D-4 · not one `canonical_docs.py` constant moved.** Only the module docstring — which asserted
*"Whether `VISION.md` is ever renamed is an open operator decision"*, false since 2026-08-29.

**D-5 · `check_adr38_baseline`'s BEHAVIOUR is unchanged.** Only its docstring (decommission (c)).
`README.md`'s absence still does not fail the check, because the check runs fleet-wide.

## 4. The three rows (done-contract item 6 · ADR-114 header `:10`)

Each surface is **decommissioned in this lane**; each row carries the residual this lane genuinely
cannot finish, not born-closed ceremony.

- **`[#620]` (a)** — `CLAUDE.md` §5 rule 5's *"do not recreate it"*, retired here. The clause is
  **repo-owned**: it sits between the `critical-rules-records` end-marker and the
  `critical-rules-consistency` start-marker, so **no lockstep `templates/claude-regions/` act was
  owed and none was taken**. Residual: the eight children still inherit ADR-38 A5's deprecation.
- **`[#621]` (b)** — the `ARCHITECTURE.md:366` echo. **That locator does not exist**
  (`grep -n "recreate" ARCHITECTURE.md` → no match), confirming C5 §5 D-4: item (b) was discharged
  by attrition before the ADR was ruled. Corrected in its place: the stale deletion fact at `:478`
  and the stale **PARKED** verdict in the Governing-ADRs list. Residual: the nine-repo migration.
- **`[#622]` (c)** — the *"README.md is optional (deprecated from the baseline)"* docstring, retired
  here. Residual: `README.md`'s membership promotion, blocked on six README-less children and three
  test pins.

Filed at `max(id in tasks/) + 1` = **620/621/622**, the synthetic `[#777]` excluded per standing
precedent. Inserted immediately after `[#614]`'s manifest node so they inherit its
`[E5] Canonical-file integrity` / `[S14]` block; `gen_task_tree.py --check` is **ok**; none of the
three trips `doc_rot`'s 1320-char row ceiling.

## 5. Scope discipline — what was NOT touched

**ZERO immutable or append-only files edited**, verified as a class: no edit lands in
`docs/decisions/`, `docs/handoffs/` (all 117 bundles still name `VISION.md`, correct for artifacts
sealed before the ruling), `docs/archive/`, `docs/intake/`, `JOURNAL.md`, `LESSONS.md`,
`logs/TOKEN-LOG.md`. The only `docs/audits/` writes are three **adds** (this lane's own artifacts).

**No merge, no push, no other lane's branch. No JOURNAL entry** — the integrator's surface
(`STANDING_RULINGS` P-1). **No index regeneration, and none was needed:** `[#590]` narrowed
`audit-index-freshness` so a new `docs/audits/*.md` no longer forces the index, and no other
regen-and-diff gate fired. **`BACKLOG.md` was regenerated** — that is not an index regeneration but
the mandatory `tasks/` → `BACKLOG.md` emit that `check_task_tree_coherence` gates.

**Not touched, named so the absence is not read as an oversight:** `scripts/gen_handoff.py` and the
rest of `tests/**` (**lane-a**), `.claude/generated/**` (**lane-c**), `codex/**` (**lane-d**),
`docs/intake/**` + `docs/decisions/**` (**lane-f**). **Lane-c is unblocked:** `CLAUDE.md` §5 rule 5
is edited and committed, which is the dependency its contract names.

### Three declared footprint extensions — disclosed, never silent

The done-contract is **immutable**; the write-scope is a **frozen ex-ante enumeration**, and
done-contract item 1 exists precisely because that enumeration could not be complete before the
census pass. Where an immutable item mandates an act on a file the write-scope omits, the act was
taken, narrowly, and declared. **Batch-D collision risk was measured for each** against every other
lane's Write-scope block.

| Extension | Mandated by | Why nowhere else | Collision |
|---|---|---|---|
| `templates/handoff/v5/PROBES.md.tmpl` — the P1a row only | done-contract item 2 | the rendered bundle copy is immutable (item 5); this is the only mutable authoring site | **none** — no batch-D lane declares `templates/**` |
| `tasks/**` + `BACKLOG.md` — three rows | done-contract item 6 | a backlog row has no other home, and the emit is gate-mandatory | **none** — no batch-D lane declares `tasks/` |
| `tests/test_canonical_docs.py` — one assertion + its docstring | forced by D-3 | the test pins `SANCTIONED_TIER1_FILES`' `.md` members; its **own docstring** says the `AGENTS.md` divergence is *"written as an explicit exception so that a second one cannot slip in unnamed"* — ADR-114 is that naming | `tests/**` is lane-a's scope, but lane-a's contract names `tests/test_governance_health.py` and its subject (FM-2/FM-4 funnel coupling) does not reach this file |

The third was found **after** the enumeration artifact landed, which is why it is not in that
artifact's §5. Recorded here rather than left for the integrator to discover in a diff.

### One gate-forced edit outside the stated sub-scope

The contract scopes `CLAUDE.md` to *"§5 rule 5 ONLY"*. `CLAUDE.md` and `ARCHITECTURE.md`
`last_reviewed` were also bumped `2026-08-28 → 2026-08-29`: `canonical_freshness` **A2 FAILs when a
stamp predates the file's last commit**, and `audit-health` is a pre-commit gate, so the bump is not
optional. **Both files were re-read end-to-end from disk before the stamp moved** —
`ARCHITECTURE.md` carries the stamp-semantics entry and its three honest limits, per its own
convention. `CLAUDE.md` got **no §12 Section-history entry**, deliberately: the contract's *"§5 rule
5 ONLY"* is the narrower instruction, and lane-c holds that file's byte budget next.

**Also corrected, found by that end-to-end re-read and unrelated to this lane's own acts:**
`ARCHITECTURE.md`'s **ADR-115** bullet still named `[#577]` as the *open owner* of a CLAUDE.md §10
anti-pattern that `[#577]` had already discharged (CLAUDE.md §12 v2.68). One line.

## 6. Evidence

**Targeted suite** — `uv run --locked pytest` over the modules covering this lane's diff
(`canonical_docs`, `validate_hermetization`, `fleet_parity`, `doc_rot`, `doc_structure`,
`doc_claims`, `gen_task_tree`, `task_tree_gate`, `backlog_source`, `ship_gate`, `audit`, …):

```
BASELINE, taken BEFORE any edit, 28 modules   1274 passed ·  3 failed · 3 skipped
FINAL,    35 modules (7 added for the tasks/  1502 passed ·  4 failed · 3 skipped
          and backlog surfaces this lane
          later touched)
```

**Zero new failures.** All four are pre-existing on `main` and none is in this lane's footprint:

| Failure | Why it is not this lane's |
|---|---|
| `test_enforcement_coverage::test_anchor_gate_probe_distinguishes_installed_from_absent` | in the 28-module BASELINE, red before any edit |
| `test_validate_doc_rot::test_live_corpus_has_no_accretion_arm_findings_only_length_findings` | in the BASELINE; and none of `[#620]`–`[#622]` adds a `doc_rot` finding (each is under the 1320-char ceiling) |
| `test_preflight_freeze_predicates::test_vi_batch1_reproduces_the_wrong_id_citation` | in the BASELINE, red before any edit |
| `test_export_backlog_view::test_no_gate_hook_or_script_reads_the_export` | **not in the baseline set** — the module was added for the final run. Its offenders are `ecosystem/conformance.html` and `ecosystem/conformance.md`, both **unmodified by this lane** (`git diff 902b621b -- ecosystem/conformance.{md,html}` is empty; last touched at `83023bbc`). Stated precisely: this is inference from an untouched-file diff, **not** a re-measurement on bare `main` |

**Two tests went RED mid-lane and were FIXED, not absorbed** — both are the mechanism working:

- `test_canonical_docs::test_validate_hermetization_seals_exactly_the_registry_living_docs` — the
  named-exception pin (§5). Its own docstring demands the naming; ADR-114 supplied it.
- `test_audit::test_check_fleet_parity_green_on_live_repo` — the root-sweep WARN (§3 D-2b), fixed by
  the `root-readme-md` row rather than by relaxing the assertion.

`test_task_tree_gate::test_registered_and_green_on_live_repo` also read RED in one intermediate run
and is **not** a finding: `check_task_tree_coherence` refuses while the index and working tree
disagree, which they did while the three new `tasks/` files sat untracked. Green once staged.
Recorded because a reader comparing run logs would otherwise count it.

**`audit.py health`: OK** at each commit (the pre-commit `audit-health` gate passed on all four).
**`gen_task_tree.py --check`: ok.** **`ruff`: passed.**

## 7. For the integrator

- Merge order: **lane-b before lane-c** (lane-c's contract says *"BLOCKED BY lane-b"*). Nothing
  else in batch D touches this lane's files.
- **No hook bypass was used anywhere in this lane** — no `SKIP=`, no `--no-verify`. There is nothing
  to re-arm.
- The `consumer_at_landing` WARN on this lane's three artifacts clears once `[#620]`–`[#622]` are on
  `main`: each row cites the enumeration artifact by path, which is what that check reads.
- `docs/audits/README.md` is **deliberately left stale** for these three adds — `[#590]` narrowed the
  hook, and regenerating it is the integrator's single act at the merge.

## 8. Reproduce

```bash
git log --oneline 902b621b..HEAD
sha256sum docs/audits/2026-08-29-technical-batchd-launch-contracts/LANE-b-614-vision-to-readme.md
grep -A4 '^## Vision' README.md
git show 902b621b:ARCHITECTURE.md > /tmp/a.md
sed -n '/^## Purpose \[CORE\]/,/^## Codemap/p' /tmp/a.md | sha256sum
sed -n '/^## Purpose \[CORE\]/,/^## Codemap/p' ARCHITECTURE.md | sha256sum
grep -nE "canonical-doc-vision|root-readme-md" -A 24 ecosystem/parity-surfaces.yaml
sed -n '99p' CLAUDE.md ; grep -n "recreate" ARCHITECTURE.md
uv run --locked python scripts/gen_task_tree.py --check
uv run --locked python scripts/audit.py health | tail -1
```

**Consumer:** `[#614]`, ADR-114 (AMENDMENT 1), `[#620]`, `[#621]`, `[#622]`,
`docs/audits/2026-08-29-technical-614-consumer-enumeration.md`,
`docs/audits/2026-08-29-verification-614-p1a-probe-evidence.md`.
