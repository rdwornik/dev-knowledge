# Census — `[#664]` corpus-structure edge computations, RE-MEASURED under the five-kind class (lane `ab-664-spine-witnessed`, step 1)

**Consumers:** `[#664]` · ADR-118 · `docs/audits/2026-09-16-technical-lane-ab-664-spine-witnessed.md` (this lane's end-of-lane artifact)

**What this is.** Step 1 of the frozen contract: *"Re-measure the corpus-structure edge computations under
§A.1's five-kind class (citation, generation, template, test, script call-site); do NOT inherit the
withdrawn '12'."* It does not inherit the 18 either. Every module the ratchet's own shape predicate
matches was re-read and verdicted, not only the rows already in `EDGE_COMPUTATIONS`.

**What this is NOT.** It does not change the register. A verdict that differs from a register row is
recorded here as a PROPOSED re-verdict. Editing `EDGE_COMPUTATIONS` without a code migration behind the
edit is a curated-register touch, which is V-2 class (a). Two earlier lanes declined the identical
class of edit on `ORPHAN_DISPOSITIONS` for that reason, and this lane follows them.

---

## 1 · Method

```
base         f8ca1d40 (main; origin/main identical at measurement time)
population   scripts/**/*.py matching graph_queries.is_edge_computation_shape  -> 65 of 149 modules
             by module: 17 registered private (18 rows -- audit.py holds two) + 3 reconciled
             + 5 not-an-edge + 40 unverdicted
class        citation · generation · template · test · script call-site  (DECLARE-REVIEWS §A.1)
excluded     state gates (one file or one tree/commit state: grammar, schema, existence alone,
             declared-copy parity, git history, the staged set) · non-corpus data (machine,
             vendor output, operator transport) · a hand-DECLARED relation read back from a register
instrument   six parallel read-only classifier passes, one rubric (function + line evidence per
             module, FPG-1 coverage named by edge kind and loader); one pass was stopped by the
             operator and one was stopped by this seat after the box ran a sibling pass for 12.9 h,
             so those 22 modules were verdicted in-seat on a narrower read -- stated, not hidden
FPG-1        2868 nodes · 21392 edges · 15 kinds, rebuilt at f8ca1d40
```

## 2 · The number

```
PRIVATE SITES (lean private, borderlines counted IN)      17   in 16 modules (audit.py carries two)
  citation                                               14
  script call-site                                        3
  generation / template / test                            0 / 0 / 0
RECONCILED MODULES (the graph consumes them)               4   (3 registered + decision_coverage;
                                                               consumer_at_landing INCOMPLETE)
NOT-AN-EDGE MODULES (borderlines counted IN)              44
FPG-1 itself                                               1
                                                          --
shape-matching modules                                    65
```

**17, not 18, and not the same 17.** Eight registered private rows are measured out of the class: four
clearly, four on a lean. One registered row that stays private has the wrong kind. Seven sites the
register never saw are in the class.

**`template`, `test` and `generation` are all 0.** The register's one `test` row (`proof_layer.py`) and its
one `template` row (`gen_handoff.py`) are both measured out. `generation` was 0 before and stays 0. An
empty kind is evidence: it means the five-kind class has three members nothing in this repo computes
privately. A table that drops empty rows can't tell "none" from "not looked at".

## 3 · The seventeen, with the blocker each carries into a migration

`D` = the refusal IS a dangling target, which FPG-1 drops by construction (`PurposeGraph.add_edge`:
*"a dangling or self edge is dropped, never invented"*) · `T` = the relation is over a different tree
or ref than the working tree FPG-1 builds from · `C` = runs in a consumer repo, which has no FPG-1
before ADR-118 W-G4 · `G` = sub-file granularity (line, symbol) a file graph does not hold · `-` = no
structural blocker.

```
module                                              kind         blocker   size  register today
scripts/batch_manifest.py::manifest_links           citation     -         S     private
scripts/validate_reconciliation.py                  citation     -         S     private
scripts/scan_undeclared_edges.py                    citation     G (tier3) M     private
scripts/funnel_coverage.py                          citation     D         M     private
scripts/funnel_lifecycle.py (leg c)                 citation     D         M     private
scripts/verify_handoff_probes.py                    citation     D T       L     private
scripts/preflight_contract.py                       citation     D T       L     private
scripts/audit.py::check_import_edges                citation     D C       M     private, KIND WRONG
scripts/audit.py::check_preflight_backlog_ids       citation     D         S-M   UNREGISTERED
scripts/audit_checks/check_floor_integrity.py       citation     D C       M     UNREGISTERED
scripts/governance_health.py                        citation     G         S     UNREGISTERED
scripts/propose_closures.py (WEAK leg)              citation     C D       M     UNREGISTERED
scripts/gen_dashboard.py (intake mentions)          citation     -         S     UNREGISTERED, borderline
scripts/codemap/ast_walker.py                       call-site    C         M     private
scripts/reverse_dep_oracle.py                       call-site    T G       L     private
scripts/safe_remove.py::_bare_stem_literal_hits     call-site    -  (*)    M     UNREGISTERED
scripts/fleet_analytics.py::inbound_reference_counts citation    T         M     UNREGISTERED, borderline
```

(*) `safe_remove`'s bare-stem leg has no structural blocker. It does have a precision one: it is recall-heavy on
purpose (a hit only downgrades SAFE to REVIEW), and putting that grammar into FPG-1's `imports` would
mint false edges the orphan census would then trust.

**Blocker-free and S-sized: two.** `batch_manifest::manifest_links` and `validate_reconciliation`. Both are
parsers of a relation FPG-1 does not load yet. Each reconciles the way the three registered `reconciled`
rows already did: FPG-1 imports the parser as an input rather than re-deriving it (ADR-118 §1, *"a new
edge kind is added to FPG-1, never to a script"*).

**Carrying `D`: eight of seventeen.** For these organs the missing target IS the finding: a probe naming a
file that is gone, a `@include` that resolves to nothing, a kill-candidate id that closed. FPG-1's
design invariant is that it does not invent a node for a target that does not exist. So "read FPG-1
instead" presumes a representation of UNRESOLVED targets the graph deliberately refuses. That is a
ruling about FPG-1's semantics. It is not a migration step.

## 4 · Proposed re-verdicts — recorded, NOT applied (V-2 class (a))

```
register row                           today                   measured            reason (one line)
scripts/validate_doc_rot.py            private citation        not-an-edge         date tokens are blanked, no target resolved; every arm a one-file property
scripts/dispatch_drift.py              private call-site       not-an-edge         targets are host PowerShell commands (machine), leg 2 single-file state
scripts/proof_layer.py                 private test            not-an-edge         extracts skipif-probed TOOLS (environment), never test -> script
scripts/gen_handoff.py                 private template        not-an-edge         template -> bundle is the generator's own hard-coded authoring; other legs off-tree transport on `main`
scripts/audit.py::check_import_edges   private call-site       private citation    a CLAUDE.md `@include` is file-names-file; the "overlap with imports" note is false
scripts/audit.py::check_doc_claims     private citation        not-an-edge (lean)  3 of 4 claims are counts; the 4th is hook-id set parity, and a hook id is not a corpus file
scripts/enforcement_coverage.py        private call-site       not-an-edge (lean)  reads CONSUMER repos' wiring and proves firing by execution; hub leg is n/a
scripts/generate_organ_index.py        private call-site       not-an-edge (lean)  an existence inventory; one leg names a script by unresolved basename
scripts/archive_row_body.py            private citation        not-an-edge (lean)  WRITES the row<->record relation; verify is byte parity; FPG-1 `archives` already holds live pairs
scripts/consumer_at_landing.py         reconciled              reconciled, INCOMPLETE  FPG-1 input 3 omits its manifest-link route (batch_manifest)
scripts/decision_coverage.py           (unverdicted)           reconciled          reads FPG-1 input 8 via store.in_edges; shape came from date regexes
scripts/file_purpose_graph.py          (unverdicted)           the graph           it is FPG-1; counting it as unverdicted inflates the exemption
+ 32 unverdicted modules measured not-an-edge (section 5), and the 7 unregistered private sites of section 3
```

## 5 · The not-an-edge population, one line each

```
assemble_paste                      writes PASTE_THIS from a fixed manifest (borderline generation, program-authored)
audit_checks/check_amendment_coherence   declared coupled-surface version agreement
audit_checks/check_handoff_version_stamp declared file list, value agreement
audit_checks/check_substrate_declaration adapter; naming-grammar date; delegates to validate_substrate
check_derived_copies                declared derived-copies.yaml + byte parity + staged set (FPG-1 could ingest the register: growth, not migration)
check_provider_registry             registry value agreement at hard-coded sites
coherence_enumerator                intra-document line sites; the pair relation is validate_reconciliation's
dispatch_conformance                writer vs an external verb's dry-run output
dispatch_surface                    value agreement at declared sites + enum checks
export_backlog_view                 renders task files to a view; resolves nothing
fleet_health                        state files, dates, proposal log vs open ids (machine log)
fleet_parity                        consumer repos' wiring (other trees) against a declared manifest
gen_claude_rosters                  inventory of command frontmatter and ADR headers
gen_lane_contract                   contract shape rendering
gen_methodology_roster              declared manifest read back
gen_seat_boot                       template fill from PLAYBOOK Ch8 tokens, program-authored (borderline template)
gen_task_tree                       the generator of the view; declared clauses FPG-1 already loads
generate_floor                      template render + F5 blacklist
journal_anchor                      JOURNAL -> commit SHA is git history
normalize_headers                   one file's heading format
review_closures                     machine-written PROPOSALS register + state
routing_agreement                   declared-copy parity with L0 + transcripts (machine)
seat_refusals                       footprints in off-tree contracts; declared intent (borderline)
session_end_backpressure            four state gates
toc/generator                       self-loop inside PLAYBOOK.md (borderline generation)
validate_adr_status                 status grammar + index/header parity
validate_backlog                    declared-clause existence (borderline; FPG-1 loads both clauses; ab-828/ab-589 footprint)
validate_doc_claims                 see check_doc_claims
validate_doc_structure              intra-file numbering and TOC anchors
validate_landing_predicate          hand-declared `landed:` sites read back
validate_residual_completeness      unfilled regions + staged set
validate_substrate                  contract text shape, declared write-scope
+ the five already verdicted not-an-edge (graph_queries, provider_bench, quality_requirements,
  substrate_provenance, validate_hermetization) and the seven modules section 4 measures out
  (check_doc_claims is a leg of audit.py, which stays private through check_import_edges)
```

## 6 · What the measurement says about the Done-when — stated here, acted on in the artifact

The Done-when asks for these computations *"driven to 0 with every organ holding one reading FPG-1
instead"*. Measured:

- **2 of 17** can reach FPG-1 with no ruling. They carry no blocker and are S-sized.
- **8 of 17** refuse on an unresolved target, which FPG-1 refuses to represent.
- **4 of 17** run in consumer repos, which have no FPG-1 before W-G4.
- **4 of 17** relate a tree or ref other than the working tree FPG-1 builds.
- **3 of 17** need sub-file granularity.

(The four blocker kinds overlap, so the counts do not sum to 17.) This is the shape ADR-118's
flip-condition 1 names: *"closing the gap requires an edge kind whose semantics are organ-specific rather
than corpus-general"*. The measurement is recorded here. Whether it trips the flip-condition is a
ruling, and it is not this census's to make.
