# CLOUD C4 ruling pre-work pack — [#397] scripts/ grouping refresh + [#488] priority-axis research leg

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-19 · **Slug:** c4-ruling-prework
- **Lane:** CLOUD C4 (Anthropic cloud session, branch `claude/c4-ruling-prework`) — read-only + one artifact.
  Frozen contract: `docs/audits/2026-08-19-technical-c4-ruling-prework-contract.md`.
- **Why this exists:** two AWAITING-RULING rows name their own pre-work (N4 grooming items 13–14). This pack
  delivers that pre-work so the architect can rule without a build step. **Nothing here is a ruling.**
  No file moves, no axis implementation, no `BACKLOG.md` / `tasks/` writes.
- **Method:** mechanical enumeration against the live tree at `4541155` + `git ls-files scripts/` (100 tracked
  files), wiring evidence read from `.pre-commit-config.yaml`, `.pre-commit-hooks.yaml`, `.claude/settings.json`,
  `deploy/manifest-v1.4.0.yaml`, `scripts/audit.py`'s delegate imports and `scripts/audit_checks/registry.py`.
  Backlog statistics computed over the 291 `tasks/*.md` frontmatter blocks (183 open).

## 0. Two limits stated before the findings

1. **The clone is SHALLOW** (`.git/shallow` present; oldest reachable commit `781bd4f`, 2026-08-13). The
   2026-07-22 tree state that produced the original map is **not reachable**, so the delta in §1.4 is computed
   against the *named file list inside* `docs/audits/2026-07-22-technical-hygiene-pre-handoff-inventory.md` §2,
   not against a `git ls-tree` of that date. Every "NEW since the map" verdict below therefore means *"not named
   in the §2 grouping text"*, which is the honest claim; it does not distinguish "landed after 2026-07-22" from
   "existed and was omitted from the map". Two files are known to be the second case (§1.4 c).
2. **The brief's "50→66" is one of three defensible counts.** 66 is the top-level `*.py` count. It excludes the
   3 `.ps1` + 1 `.xml` the original map *did* count, and it excludes all 30 files in the four subpackages. The
   refreshed map below uses **100 tracked files** as the denominator and states the other two framings, because
   a structure ruling that reasons about 66 files would be reasoning about two thirds of the tree.

---

# ITEM 1 — [#397] scripts/ grouping map refresh

## 1.1 The row's own taxonomy, read first

`[#397]` (`tasks/397-*.md`, `BACKLOG.md:252`) proposes no new taxonomy of its own — it *cites* the one in the
2026-07-22 inventory §2 and asks the operator to rule adopt/reject on it. That taxonomy has **ten groups**:

```
G1  audit-core / orchestrator                        (1)
G2  standalone pre-commit / commit-msg / pre-push gates (7)
G3  audit ALL_CHECKS delegate modules                (14)
G4  freshness-hook-wired generators                  (4)
G5  manual-CLI generators                            (5)
G6  doc-tooling packages                             (12)
G7  read-only reporters                              (4)
G8  session hooks                                    (5 py + 2 ps1)
G9  Tier-1 loop                                      (2)
G10 scheduler                                        (2)
```

Everything below classifies into exactly these ten, or is flagged as fitting none. No group is invented for
convenience; the two headings that *look* like new groups (§1.3 A and §1.3 D) are flags, not proposals.

**Arithmetic defect in the source map, recorded because a ruling will lean on its counts.** Those ten counts
sum to **58** entries, and the same paragraph opens by calling the tree "~50 files". Deducting the one file
double-listed across G7 and G8 (`fleet_health.py`) gives **57 distinct named files**, plus
`validate_onboarding_rulings.py` named only in the map's own "lowest-impact" sentence = **58**. So the original
map was already a ~58-file map described as a 50-file map. The delta in §1.4 is stated against the named list,
not against the "50".

## 1.2 Refreshed map — all 100 tracked files

Wiring-evidence key: `PC` `.pre-commit-config.yaml` entry · `PH` `.pre-commit-hooks.yaml` (the DISTRIBUTED hook
repo consumers install) · `SS` `.claude/settings.json` hook · `MF` `deploy/manifest-v1.4.0.yaml` declared ·
`AC` imported by `audit.py` / an `audit_checks/` module as a check body · `LIB` imported by another script ·
`CMD` invoked by a `.claude/commands/*.md` or skill · `TEST` reachable only from `tests/`.

### G1 — audit core / orchestrator — 1 file (unchanged)

```
scripts/audit.py                     PC audit-health · MF · imported by 6 siblings
```

### G2 — standalone gates — 10 files (was 7, +3)

```
scripts/block_commit_on_main.py      PC pre-commit    HUB-ONLY   NEW since the map
scripts/normalize_headers.py         PC pre-commit
scripts/validate_hermetization.py    PC pre-commit    HUB-ONLY
scripts/check_seal_identity.py       PC pre-commit    HUB-ONLY   NEW since the map
scripts/validate_backlog.py          PC pre-commit    (plugin twin, parity-pinned)
scripts/coherence_nudge.py           PC pre-commit    non-blocking
scripts/check_backlog_commit_msg.py  PC commit-msg    MF
scripts/check_backlog_filing.py      PC commit-msg    HUB-ONLY
scripts/block_ff_push.py             PC pre-push      MF
scripts/block_unanchored_push.py     PC pre-push      HUB-ONLY   NEW since the map
```

### G3 — audit ALL_CHECKS delegate modules — 18 files (was 14, +4; 3 more are dual-role, see G5)

Delegates imported by `audit.py` (`:95`–`:187`, `:1818`, `:1901`, `:3073`, `:3222`) or by an `audit_checks/`
module (`check_safe_removal:17`, `check_reconciled_versions:17`, `check_residual_completeness:18`,
`check_boot_byte_budget:19`):

```
scripts/canonical_freshness_gate.py  AC · MF        scripts/validate_doc_claims.py        AC
scripts/validate_no_ff.py            AC · MF        scripts/validate_reconciliation.py    AC
scripts/validate_doc_rot.py          AC             scripts/validate_doc_structure.py     AC
scripts/validate_git_backlog.py      AC             scripts/validate_doc_code_edge.py     AC
scripts/safe_remove.py               AC             scripts/scan_undeclared_edges.py      AC
scripts/verify_handoff_probes.py     AC             scripts/validate_residual_completeness.py AC
scripts/fleet_parity.py              AC             scripts/enforcement_coverage.py       AC · MF
scripts/silent_rule_detector.py      AC   NEW       scripts/validate_landing_predicate.py AC   NEW
scripts/preflight_contract.py        AC · CMD NEW   scripts/journal_anchor.py             AC · LIB NEW
```

### G4 — freshness-hook-wired generators — 5 files (was 4, +1)

```
scripts/gen_methodology_roster.py    PC roster-freshness
scripts/gen_claude_rosters.py        PC claude-rosters-freshness
scripts/gen_audit_index.py           PC audit-index-freshness
scripts/gen_intake_index.py          PC intake-index-freshness
scripts/generate_organ_index.py      PC organ-index-freshness      NEW since the map
```

### G5 — manual-CLI generators — 10 files (was 5, +5)

```
scripts/gen_doc_counts.py            CLI              scripts/generate_floor.py    CLI · MF-adjacent
scripts/gen_handoff.py               CMD /handoff     scripts/assemble_paste.py    CMD · also AC
scripts/seed_runbook.py              CLI (no caller)  scripts/gen_task_tree.py     also AC   NEW
scripts/gen_intake_tree.py           also AC   NEW    scripts/batch_manifest.py    CMD-adjacent NEW
scripts/desired_state_report.py      CLI       NEW    scripts/coherence_enumerator.py  CMD skill NEW
```

### G6 — doc-tooling packages — 13 files (was 12, +1)

```
scripts/codemap/{__init__,ast_walker,check,cli,generator,mermaid_emit,text_emit}.py   7   (map said 6)
scripts/toc/{__init__,check,cli,generator}.py                                        4
scripts/codemap_hook.py   PH   ·   scripts/toc_hook.py   PH                          2
```

**Correction to a plausible-looking orphan verdict.** `codemap_hook.py` / `toc_hook.py` have **zero** callers in
`.pre-commit-config.yaml` — the hub's own entries call `python -m scripts.codemap.cli` / `scripts.toc.cli`
directly. They are nevertheless **live**: they are the four `entry:` lines of `.pre-commit-hooks.yaml`
(`:26 :35 :44 :52`), the distributed hook repo a consumer installs by `repo:`/`rev:`. Renaming or moving either
one is a **remote-consumer-visible** break that no hub-local test or caller-count would surface. The original
map's caller-impact column does not carry this surface at all.

### G7 — read-only reporters — 7 files (was 4, +3: `window_metrics`, `probe_child_backlogs`, and
`validate_onboarding_rulings` — the last a *placement*, named by the old map but in no group)

```
scripts/boundary_report.py     scripts/boundary_headers.py  MF     scripts/fleet_analytics.py
scripts/fleet_health.py  (also G8)                                 scripts/probe_child_backlogs.py  TEST-only
scripts/window_metrics.py            NEW                           scripts/validate_onboarding_rulings.py  TEST-only, advisory
```

### G8 — session hooks — 7 files (unchanged: 5 py + 2 ps1)

```
scripts/session_end_backpressure.py  SS Stop · MF        scripts/hooks/block_immutable_edits.py  SS PreToolUse
scripts/fleet_health.py              SS SessionStart     scripts/changelog_sentinel.py           SS SessionStart
scripts/arm_hooks.py                 SS SessionStart     scripts/surface_triage.ps1              SS SessionStart
scripts/billing_leak_sentinel.ps1    SS SessionStart
```

### G9 — Tier-1 loop — 2 files (unchanged)

```
scripts/propose_closures.py   MF (plugin twin)     scripts/review_closures.py   MF (plugin twin)
```

### G10 — scheduler — 2 files (unchanged)

```
scripts/setup-fleet-scheduler.ps1        scripts/fleet-baseline.task.xml
```

## 1.3 Files that fit NO group in the row's taxonomy — 26 of 100

This is the flag list the brief asked for. It is a quarter of the tree, and it is the part a ruling has to
dispose of, because a ten-group structure that leaves 26 files homeless is not yet a structure.

**A. The `scripts/audit_checks/` package — 18 files. The single largest miss.**

```
scripts/audit_checks/_common.py        scripts/audit_checks/registry.py
scripts/audit_checks/check_adr38_baseline.py           check_amendment_coherence.py
check_boot_byte_budget.py              check_canonical_md_visibility.py
check_canonical_structure.py           check_claude_md.py
check_dot_prefix_discipline.py         check_floor_integrity.py
check_handoff_bundle_structure.py      check_handoff_version_stamp.py
check_reconciled_versions.py           check_residual_completeness.py
check_routine_consumers.py             check_safe_removal.py
check_vision_md.py                     check_workspace_settings.py
```

These are 16 extracted checks plus `_common.py` and the ordered `registry.py`, landed by `[#533]` on 2026-08-16
(`7731d9d5`+`f84b4d81`). They are neither G1 (they are not the orchestrator) nor G3 (a G3 member is a
*standalone script* the orchestrator imports; these are *interior* modules of the orchestrator, admitted as a
home by operator ruling `STANDING_RULINGS` K-2 only after ADR-101 Rule C **refused** the directory). The row's
taxonomy predates them by three and a half weeks. **`[#533]` is not finished** — 27 of 43 checks remain in the
facade with a batch-7 follow-on leg ruled — so this group is still growing while `[#397]` waits. Both rows carry
`serialize-group: audit-py`.

**B. Shared libraries — 6 files.** Imported by other organs; not themselves a gate, generator, reporter or hook,
so no group fits:

```
scripts/gitenv.py              path-loaded by audit.py:63, fleet_parity.py:95, batch_manifest.py:97
                               (deliberately by path, NOT by import — see its own :41-49 docstring)
scripts/reverse_dep_oracle.py  imported by validate_doc_code_edge.py, safe_remove.py
scripts/desired_state_loader.py imported by desired_state_report.py, audit.py
scripts/validate_branch_naming.py imported by batch_manifest.py, worktree_seed.py; CMD /lane-boot
scripts/single_flight.py       [#530] dispatch guard; zero non-test callers
scripts/telemetry_emit.py      [#529] Stage-1 emit library; its own docstring states "Library only; no call sites"
```

`journal_anchor.py` is a seventh of this shape but is already placed in G3 (it is both the shared anchoring
predicate for `block_ff_push`/`block_unanchored_push` **and** an `audit.py` check delegate — a dual role the
taxonomy has no way to express).

**C. Lane / batch-protocol tools — 2 files** (plus `batch_manifest.py`, `preflight_contract.py` and
`coherence_enumerator.py`, each parked in G5/G3 for want of a better slot). Invoked by a slash command or a
skill, wired to no hook and to no `ALL_CHECKS` entry:

```
scripts/worktree_seed.py           CMD /lane-boot
scripts/worktree_import_proof.py   CMD /lane-boot
```

**D. `scripts/coherence_enumerator.py`** — invoked by the `check-against-spec` skill, imports
`validate_reconciliation`. Parked in G5 above; it is a *site enumerator*, not a generator, and not in the map.

**Two of the six libraries have no consumer at all today** (`single_flight.py`, `telemetry_emit.py`) — by their
own declared design, staged ahead of a consumer. They are **not** orphans and must not be read as dead code in a
structure ruling; they are the one category where "zero callers" is the intended state.

## 1.4 Delta vs the original map

**a. Count.** Named in the 2026-07-22 §2 list: **58 distinct files** (prose said "~50"). Tracked today: **100**.
Top-level `*.py` today: **66** (the brief's figure). Growth on the like-for-like named-file basis: **+42 files,
+72%**, of which **18 (43% of the growth) is the single `audit_checks/` package**.

**b. New files by group** (reconciled against `git ls-files scripts/` — the ten groups hold **74 distinct**
files and the flag list holds **26**; 74 + 26 = 100, with `fleet_health.py` the one file counted in two groups
and `assemble_paste` / `gen_task_tree` / `gen_intake_tree` dual-role across G3 and G5):

```
G2  +3   block_commit_on_main · block_unanchored_push · check_seal_identity
G3  +4   silent_rule_detector · validate_landing_predicate · preflight_contract · journal_anchor
G4  +1   generate_organ_index
G5  +5   gen_task_tree · gen_intake_tree · batch_manifest · desired_state_report · coherence_enumerator
G6  +1   codemap/ went 6 -> 7; the shallow clone cannot say whether text_emit.py or mermaid_emit.py is the add
G7  +2   window_metrics · probe_child_backlogs   (+1 placement: validate_onboarding_rulings)
G1 G8 G9 G10  +0   membership byte-for-byte unchanged
no group  +26   audit_checks/ 18 · shared libraries 6 · lane tools 2   (of these, gitenv.py is a map
                omission rather than an addition — see (c))
```

Arithmetic: 57 distinct files in the old groups + 16 grouped additions + 1 placement = 74 grouped today;
74 + 26 flagged = 100; 100 - 58 named in 2026-07-22 = **+42**, of which 41 are genuinely new files and 1
(`gitenv.py`) existed unmapped.

**c. Two files are map omissions, not additions.** `gitenv.py` is named in the 2026-07-22 §1 text ("`#396` owns
only the gitenv slice") but appears in **no** §2 group; `validate_onboarding_rulings.py` appears only in §2's
"lowest-impact" sentence, likewise in no group. The taxonomy was incomplete on the day it was written.

**d. Groups that did NOT move.** G1, G8, G9, G10 are byte-for-byte the same membership. The four groups the
original map called out as the *deploy-contract ripple risk* also did not grow: every one of the three new G2
gates and the one new G4 generator is **HUB-ONLY** by its own `.pre-commit-config.yaml` comment, and
`deploy/manifest-v1.4.0.yaml` still declares the same scripts/ set (`canonical_freshness_gate`,
`session_end_backpressure`, `block_ff_push`+`validate_no_ff`, `check_backlog_commit_msg`, `boundary_headers`,
`enforcement_coverage`, `audit`, the two Tier-1 twins, and `codemap_hook`/`toc_hook` via `.pre-commit-hooks.yaml`).
**The move-impact surface the row worried about is unchanged in size** even though the tree grew 72%.

**e. The highest-move-impact file is now higher, and its risk changed shape.** `audit.py` was "~8 caller
sites". Verified live today: **5 sibling modules across 7 import sites** — `boundary_report.py:47`,
`fleet_analytics.py:111`, `gen_doc_counts.py:35`/`:38`, `gen_handoff.py:495`, `enforcement_coverage.py:566`/
`:695`/`:753` — plus the `audit-health` pre-commit entry, the `deploy/manifest-v1.4.0.yaml` declaration, and
`tests/test_audit.py`. (`fleet_health.py` inserts `scripts/` on `sys.path` at `:351` but does **not** import
`audit`; the original map's caller list should not be read as including it.) The material change is not the
count but the **kind**: `audit.py:63-64` path-loads `gitenv.py` via `Path(__file__).resolve().with_name(...)`,
and `scripts/audit_checks/registry.py`'s own docstring records that this expression is *position-dependent* and
is why `check_handoff_probes` could not be extracted. Moving `audit.py` now breaks a path expression, which no
import-graph tool reports.

**f. The row's "flat may be the right answer" is now a weaker default than it was.** Not a recommendation —
the observation is only that the two facts the row rested on have both moved: 50→100 files, and one
sub-package already exists in the tree (`audit_checks/`), admitted by an operator ruling that had to override
ADR-101 Rule C to let it in. Whatever is ruled, `scripts/` is no longer flat.

**ITEM 1 STATUS: CLEAR.** No moves executed, no proposals beyond the row's own frame.

---

# ITEM 2 — [#488] priority-axis research leg

## 2.1 What the row asks and what the tree actually carries

`[#488]` (`BACKLOG.md:276`) names three candidates: **WSJF/RICE-class scoring**, **graph-centrality ranking over
the depends-on / blocks edges the task tree already carries**, under a **library-first bar** and a **Fibonacci
binding for any estimated field**. Output is ruling input; build only after the ruling.

Measured over the 291 `tasks/*.md` frontmatter blocks (183 open):

```
priority          P1 6 · P2 97 · P3 80                      (hand-set; 97 rows tie at P2)
size              S 116 · M 61 · L 6                        (3-value enum, NOT Fibonacci)
theme             9 themes; E2 62 · E7 49 · E8 17 · rest 55
serialize-group   present on 116 of 183; 11 groups; audit-py 42 · architecture 16 · settings-json 14
depends-on        present on 3 open rows: [#112] [#385] [#389]
blocks            present on 0 rows — the field does not exist
id                monotonic allocation, open range 23..561 — a free age proxy, no new field
prose [#id] refs  dense and untyped (top in-degree: #348 ×18, #242 ×16, #328 ×14, #270 ×13)
```

**The row's own premise for candidate 3 does not hold.** "The depends-on / blocks edges the task tree already
carries" is **3 edges on 183 nodes**, and `blocks:` is absent entirely. `[#424]` independently records that the
`depends-on` gates are inert. Any centrality measure over that graph assigns an identical score to 180 of 183
rows. This is the single most decision-relevant fact in Item 2 and it is stated first for that reason.

## 2.2 The row's named candidates

**WSJF (SAFe).** Cost of Delay ÷ job size, where CoD = user-business value + time criticality +
risk-reduction/opportunity-enablement, each a Fibonacci estimate. **Inputs it needs:** four estimated fields per
row that do not exist — three CoD components plus a Fibonacci-scaled size (today's `S/M/L` is a 3-value enum
and would have to be re-scaled, which is exactly the "false precision through the back door" the row's Fibonacci
clause is guarding against). **Maintenance cost:** highest of any option here — 183 open rows × 4 fields = 732
estimates, all of them stale the moment context moves, and re-estimation is a recurring operator obligation with
no mechanical backstop. A generator can *compute* WSJF but cannot *populate* it. **Mechanically derivable:** no,
for any component.

**RICE (Intercom).** Reach × Impact × Confidence ÷ Effort. **Inputs:** Reach is the load-bearing term and it is
near-meaningless in a single-operator hub — "how many users in a period" collapses to 1, or has to be redefined
as *sessions or child repos affected*, which is a redefinition, not an adoption, and the library-first bar cuts
against a bespoke variant. Impact and Confidence are estimates; Effort could proxy off `size`. **Maintenance:**
lower than WSJF (3 fields, one proxied) but the same recurring-estimate shape. **Mechanically derivable:**
Effort only.

**Graph centrality over depends-on / blocks.** **Inputs:** a dependency edge set. **The tree has 3 edges and no
`blocks` field.** To make this axis mean anything, someone must first populate dependencies across ~183 rows —
which is itself a larger and more error-prone job than any of the scoring axes, and `[#424]` shows the last
attempt at this field went inert. **Maintenance:** the edge set has to be maintained on every filing and every
close, forever, or the ranking silently rots — the failure mode is a *confident wrong order*, worse than no
order. **Mechanically derivable:** the algorithm yes (stdlib or `networkx`, library-first is satisfiable); the
**edges no**. A cheap salvage exists: run centrality over the *untyped prose `[#id]` mentions* the tree already
carries densely. That is derivable today, and it is a different measurement — attention, not dependency.

## 2.3 Three added from established practice

**P-enum + age (Kanban / simple staleness ordering).** The minimal axis: keep the hand-set `[P1..P3]` as the
primary key and break its ties by age. **Inputs:** none new. Task ids are allocated monotonically (open range
23..561) and `gen_task_tree` already owns the ledger, so **id is a free age proxy** — no `created:` field, no
backfill, and it is tamper-evident because the id ledger already refuses re-issue. **Maintenance:** zero
recurring cost; the only ongoing obligation is the one the operator already has (setting P). **Mechanically
derivable: fully.** What it buys is modest and precisely scoped: it does not rank *across* P tiers any better
than today, it only dissolves the 97-way P2 tie and the 80-way P3 tie into a deterministic order. What it cannot
do is tell the operator that a P3 is actually urgent.

**Constraint-contention / unblocking count (Theory of Constraints, critical-chain).** Rank by how many other
rows a completion frees for parallel work. **Inputs:** none new — `serialize-group` is present on 116 of 183
open rows and exists *precisely because* a shared file serializes lanes; `[#533]`'s own filing text records the
batch-6 pre-dispatch matrix **refusing to dispatch two lanes** over exactly this. Score = (group size − 1) for a
row that dissolves or shrinks its group, 0 for an ungrouped row. **Maintenance:** low, and it is *already being
paid* — the field is set at filing time for lane-dispatch reasons and would rot only if lane dispatch itself
rotted, which the batch protocol would surface immediately. **Mechanically derivable: fully, today**, from
frontmatter the generator already parses. Honest limit: it ranks *throughput*, not *value* — a row can unblock
forty others and still matter less than one that unblocks none, so it is a strong secondary key and a poor sole
one.

**SQALE-style debt-interest ratio (SQALE method, ISO/IEC 25010 lineage).** Rank by (recurring cost of NOT
fixing) ÷ (one-off remediation cost) — the axis built for exactly this repo's population, where most rows are
governance/tooling debt rather than features. **Inputs:** a structured per-row incident signal. The tree carries
a rich *unstructured* one — `[#486]` records "both wave runs had to be forced under `PYTHONUTF8=1`", `[#533]`
records a refused dispatch — but as prose, so an `incidents:` field (count + date, no estimate) would have to be
added and filled on each recurrence. **Maintenance:** medium, and unusually honest: it is append-only and
evidential rather than estimated, so it does not decay the way a WSJF estimate does; the cost is remembering to
append. **Mechanically derivable:** the ratio yes once `incidents:` exists and `size` proxies remediation cost;
the incident signal no. This is the only axis of the six under which `[#486]` can plausibly outrank `[#533]`.

## 2.4 Worked example — how each axis orders [#533] against [#486] on this week's tree

Measured inputs, both rows open at `4541155`:

```
[#533]  P2 · M · theme E2 · serialize-group audit-py (42 members) · id 533 · open rows citing it: 2 (#534,#535)
        subject: decompose the audit.py check monolith; 16/43 extracted, batch-7 follow-on leg ruled
[#486]  P3 · S · theme E7 · serialize-group none      · id 486 · open rows citing it: 0
        subject: U+21C4 in desired_state_report.py crashes a cp1252 console; workaround PYTHONUTF8=1 exists
```

| axis | derivable mechanically? | maintenance cost | how it orders #533 vs #486 this week |
|---|---|---|---|
| **Status quo — hand-set [P1..P3]** | n/a (the field is the input) | zero recurring, but no ordering *within* a tier | **#533 > #486** (P2 > P3). Both sit inside a tie block — 97 rows at P2, 80 at P3 — so the pair is ordered only because they happen to land in different tiers. Two P2s are not ordered at all. |
| **WSJF** | **No** — 3 CoD components + a Fibonacci size, none exist (732 new estimates across 183 rows) | **Highest**; recurring re-estimation, no mechanical backstop | **#533 > #486**, but by judgement, not derivation. #533's CoD is high on time-criticality (it is a measured throughput constraint on batch dispatch) over size M; #486's CoD is low (a crash with a live workaround) over size S, and the small denominator lifts it into mid-pack rather than the floor. Change one estimate and the order changes. |
| **RICE** | **Effort only** (proxied off `size`); Reach is meaningless at n=1 operator without a bespoke redefinition | High; 3 estimated fields | **#533 > #486**, narrower than WSJF. #533 reaches every hub session running `audit.py` plus every batch dispatch; #486 reaches only runs on a cp1252 console — but #486's S effort against #533's M closes much of the gap. |
| **Graph centrality over `depends-on`/`blocks`** | Algorithm yes (library-first satisfiable); **edges NO** — 3 edges on 183 nodes, `blocks` absent | Very high — the edge set must be maintained on every filing and close, or the ranking rots into confident-wrong | **NEITHER — both score 0 and are indistinguishable**, along with 180 of the 183 open rows. This axis cannot separate the pair today. *(Salvage variant, over untyped prose `[#id]` mentions, which IS derivable now: #533 in-degree 2, #486 in-degree 0 → **#533 > #486**.)* |
| **P-enum + age (id proxy)** | **Fully** — no new field; id is a monotonic, ledger-backed age proxy | **Zero recurring** | **#533 > #486** on the P key, unchanged from status quo. Its actual contribution is inside the tiers: #486 lands at ~decile 8 of the open id range, i.e. near the *bottom* of the P3 staleness queue, and #533 near the bottom of P2. It orders the tie blocks; it does not re-order this pair. |
| **Constraint-contention / unblocking count** | **Fully, today** — `serialize-group` on 116/183 rows, already generator-parsed | **Low, and already paid** — set at filing time for lane dispatch | **#533 ≫ #486, by the widest margin of any axis: 41 vs 0.** `audit-py` is the largest serialize-group in the tree (42 members) and #533 is the row that dissolves it. #486 carries no group and scores 0. This is also the only axis that would have predicted the batch-6 refusal *before* it happened. |
| **SQALE debt-interest ratio** | Ratio yes once an `incidents:` field exists; **the incident signal no** | Medium, but append-only/evidential — does not decay like an estimate | **The one axis that can invert the pair.** #533: interest = a refused dispatch per batch, remediation = M and partially spent → very high ratio. #486: interest = one forced env var per run on one console, remediation = a single ASCII character swap → the ratio is high *per unit of remediation* and could rank #486 first. Which way it lands depends entirely on how `incidents:` counts a cheap-but-constant tax. |

## 2.5 LEAN

**LEAN:** the only axis that needs no new field, is fully derivable by the existing generator today, and
separates these two rows 41-to-0 is **constraint-contention over `serialize-group`** — layered as a tiebreak
*under* the hand-set `[P1..P3]` rather than replacing it, with `P-enum + age` as the zero-cost floor beneath
both; WSJF and RICE each demand 3–4 recurring estimates across 183 rows for an ordering they produce by
judgement anyway, and the row's own graph-centrality candidate is inert on today's 3-edge population and should
be reframed as a *prose-mention* attention measure or dropped before it is costed.

**ITEM 2 STATUS: CLEAR.** No axis implemented, no ranking ratified, no `BACKLOG.md` / `tasks/` write.
