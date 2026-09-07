# APPENDIX — census lane S-06 · `tasks/` · per-file verdict table

> Appendix to `docs/audits/2026-09-07-technical-census-tasks.md`, split out of it under that
> contract's 40 KB rule and committed with it. Read the census for the witnesses behind these
> verdicts, for the counts, and for the honest limits that bound them. Every verdict here is a
> **PROPOSAL** the operator rules; this lane changed nothing.

**Consumer:** `[#506]` (whole-set grooming arc, the row that consumes a per-row sheet like this one) · `[#440]` · `[#580]` — see the census.

## Non-row files

| File | Bytes | Verdict | Witness |
|---|---|---|---|
| `tasks/README.md` | 6,576 | KEEP | generator `scripts/gen_task_tree.py`; 46 `scripts/`+`tests/` modules reference `tasks/` |
| `tasks/manifest.json` | 68,365 | KEEP | generator `scripts/gen_task_tree.py`; gate `audit.py::task_tree_coherence` |
| `tasks/archive/README.md` | 6,471 | KEEP | generator `scripts/archive_row_body.py`; `tests/test_archive_row_body.py` |

## `tasks/archive/` records (24)

| Record | Bytes | Row | Verdict | Witness |
|---|---|---|---|---|
| `112.md` | 3,596 | `[#112]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `130.md` | 3,832 | `[#130]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `139.md` | 2,221 | `[#139]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `145.md` | 2,940 | `[#145]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `146.md` | 3,236 | `[#146]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `169.md` | 2,297 | `[#169]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `171.md` | 3,678 | `[#171]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `188.md` | 2,096 | `[#188]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `218.md` | 2,058 | `[#218]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `267.md` | 2,772 | `[#267]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `277.md` | 3,396 | `[#277]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `294.md` | 2,187 | `[#294]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `298.md` | 1,844 | `[#298]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `301.md` | 2,081 | `[#301]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `308.md` | 2,045 | `[#308]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `325.md` | 2,340 | `[#325]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `420.md` | 2,012 | `[#420]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `491.md` | 3,643 | `[#491]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `492.md` | 3,245 | `[#492]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `533.md` | 1,981 | `[#533]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `535.md` | 1,881 | `[#535]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `541.md` | 2,366 | `[#541]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `555.md` | 1,974 | `[#555]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |
| `561.md` | 1,922 | `[#561]` live, in queue | KEEP | pointer present in the row exactly once; `archive_row_body.py verify` legs B/E |

## Row files — live in the queue (224)

Verdict **KEEP** for every row below: each is referenced by a `tasks/manifest.json` node, renders into `BACKLOG.md`, and is read as source by `scripts/backlog_source.py::canonical_text`. That is the witness; the `Note` column carries only what this lane established beyond it.

| id | file | status | P | size | theme | Verdict | Note |
|---|---|---|---|---|---|---|---|
| `[#4]` | `4-build-lessons-index-json-sessionstart-retrieval.md` | deferred | P2 | M | [E3] | KEEP |  |
| `[#19]` | `19-complete-the-adr-39-register.md` | deferred | P3 | M | [E4] | KEEP |  |
| `[#23]` | `23-validate-adr-frontmatter-relation-fields.md` | deferred | P3 | S | [E4] | KEEP |  |
| `[#43]` | `43-decide.md` | deferred | P3 | L | [E6] | KEEP |  |
| `[#82]` | `82-define-per-repository-agentic-review-profiles.md` | deferred | P3 | M | [E6] | KEEP | dangling citation `#221` |
| `[#102]` | `102-machine-readable-repo-index-for-agent-consumptio.md` | deferred | P2 | M | [E7] | KEEP |  |
| `[#112]` | `112-adr-amend-helper-adr-immutable-zone-extension.md` | open | P2 | M | [E2] | KEEP | narrowed Done-when lives only in `tasks/archive/112.md` |
| `[#116]` | `116-hooks-hygiene.md` | deferred | P3 | S | [E2] | KEEP |  |
| `[#117]` | `117-evaluate-prompt-agent-based-hooks.md` | deferred | P3 | S | [E2] | KEEP |  |
| `[#123]` | `123-routine-observability-convention-value-review.md` | deferred | P2 | S | [E7] | KEEP |  |
| `[#130]` | `130-memory-hygiene-review.md` | open | P3 | S | [E3] | KEEP | narrowed Done-when lives only in `tasks/archive/130.md` |
| `[#139]` | `139-merged-arc-record-verifier.md` | deferred | P2 | L | [E2] | KEEP |  |
| `[#144]` | `144-feature-dod-end-to-end-user-flow-test.md` | deferred | P3 | M | [E3] | KEEP |  |
| `[#145]` | `145-codification-completeness-pass.md` | open | P3 | M | [E3] | KEEP | scope halved in `tasks/archive/145.md`; criterion text unchanged |
| `[#146]` | `146-de-hardcode-first-doctrine-sweep.md` | open | P3 | S | [E2] | KEEP | narrowed Done-when lives only in `tasks/archive/146.md` |
| `[#153]` | `153-enforcement-completeness-pass.md` | deferred | P2 | M | [E2] | KEEP |  |
| `[#166]` | `166-doctrine-enforcement-coherence-check.md` | deferred | P3 | M | [E2] | KEEP |  |
| `[#169]` | `169-ungated-doc-staleness-detection.md` | deferred | P3 | M | [E2] | KEEP | DEFER peg redirected to `[#171]`'s archive-only remainder |
| `[#170]` | `170-design-land-the-traceability-spine-adr.md` | open | P3 | M | [E2] | KEEP |  |
| `[#171]` | `171-build-the-conformance-dashboard-at-ecosystem-con.md` | open | P3 | M | [E2] | KEEP | row-body Done-when WITNESSED on main; operative criterion is archive-only |
| `[#181]` | `181-coherence-v2-nudge-response.md` | deferred | P2 | S | [E2] | KEEP |  |
| `[#185]` | `185-gap-2-deterministic-gotcha-injection-guard.md` | open | P2 | M | [E2] | KEEP |  |
| `[#188]` | `188-deny-rule-hook-completeness-audit.md` | deferred | P3 | M | [E2] | KEEP |  |
| `[#189]` | `189-execute-in-claude.md` | deferred | P3 | S | [E2] | KEEP |  |
| `[#190]` | `190-general-intra-file-duplication-detector.md` | deferred | P3 | M | [E2] | KEEP |  |
| `[#210]` | `210-convert-journal-wrap-no-ff-warns-from-per-instan.md` | open | P3 | S | [E2] | KEEP |  |
| `[#218]` | `218-safe-removal-gate-m2-m3-boundary.md` | deferred | P1 | M | [E2] | KEEP |  |
| `[#220]` | `220-modify-semantic-drift-axis.md` | deferred | P2 | M | [E2] | KEEP |  |
| `[#227]` | `227-relocate-agent-framework-md-out-of-protocols.md` | deferred | P3 | S | [E5] | KEEP |  |
| `[#231]` | `231-consumer-hub-feedback-report.md` | deferred | P3 | M | [E6] | KEEP |  |
| `[#234]` | `234-cross-repo-probe-validator.md` | deferred | P3 | S | [E2] | KEEP |  |
| `[#240]` | `240-follow-up.md` | deferred | P3 | S | [E2] | KEEP |  |
| `[#241]` | `241-undeclared-edge-groom.md` | open | P2 | S | [E2] | KEEP |  |
| `[#242]` | `242-adr-status-flip-coherence-check.md` | open | P2 | M | [E2] | KEEP |  |
| `[#244]` | `244-essence-spec-lifecycle-epic.md` | deferred | P2 | L | [E6] | KEEP | dangling citation `#221`, `#246`, `#248`, `#249`, `#250` |
| `[#245]` | `245-add-path-status-awareness.md` | deferred | P2 | M | [E6] | KEEP |  |
| `[#267]` | `267-scope-exercising-arc-extension.md` | open | P2 | S | [E2] | KEEP | row asserts leg 2 verified on disk 2026-08-28; leg 1 unmet; dangling citation `#221` |
| `[#269]` | `269-audit-index-count-tiered-shape-freshness-hook.md` | deferred | P3 | S | [E5] | KEEP |  |
| `[#271]` | `271-nightly-proposal-loop.md` | open | P3 | L | [E7] | KEEP |  |
| `[#273]` | `273-changelog-review-staleness-escalation.md` | deferred | P3 | S | [E7] | KEEP |  |
| `[#274]` | `274-dogfood-signal-prior-in-the-changelog-review-ado.md` | open | P3 | S | [E7] | KEEP | Done-when leg 1 witnessed on main; leg 2 (a citing digest) not |
| `[#277]` | `277-propose-closures-signal-repair.md` | open | P2 | M | [E2] | KEEP | narrowed Done-when lives only in `tasks/archive/277.md` |
| `[#278]` | `278-test-suite-hygiene-epic.md` | deferred | P2 | M | [E7] | KEEP |  |
| `[#285]` | `285-extend-hub-freshness-gating-to-playbook.md` | deferred | P3 | S | [E5] | KEEP |  |
| `[#288]` | `288-model-identity-guard-for-unattended-runs.md` | deferred | P3 | S | [E7] | KEEP |  |
| `[#289]` | `289-hub-own-the-onedrive-blue-yonder-guard.md` | deferred | P2 | M | [E2] | KEEP |  |
| `[#293]` | `293-consumer-runbook-fan-out.md` | open | P3 | S | [E1] | KEEP |  |
| `[#294]` | `294-validate-backlog-deploy-carrier-path-de-hardcode.md` | deferred | P3 | M | [E2] | KEEP |  |
| `[#297]` | `297-lightweight-dry-observe-arc-coverage-mode.md` | deferred | P3 | S | [E2] | KEEP |  |
| `[#298]` | `298-handoff-generator-polish.md` | open | P3 | S | [E1] | KEEP |  |
| `[#300]` | `300-hermetization-residual-d-ii.md` | deferred | P1 | M | [E5] | KEEP |  |
| `[#301]` | `301-session-plan-artifact-class.md` | deferred | P2 | M | [E1] | KEEP |  |
| `[#303]` | `303-make-seed-runbook-py-child-class-aware.md` | deferred | P2 | S | [E2] | KEEP |  |
| `[#305]` | `305-add-a-verify-only-already-onboarded-re-run-mode.md` | deferred | P3 | S | [E2] | KEEP |  |
| `[#308]` | `308-decide-the-verify-skill-s-canonical-home.md` | deferred | P3 | S | [E2] | KEEP |  |
| `[#310]` | `310-define-the-cold-bundle-annotation-surface-annota.md` | deferred | P3 | S | [E2] | KEEP |  |
| `[#317]` | `317-default-parallel-test-invocation-slow-tier-marke.md` | deferred | P2 | M | [E7] | KEEP |  |
| `[#322]` | `322-fleet-dashboard.md` | deferred | P2 | M | [E7] | KEEP |  |
| `[#324]` | `324-phase-6-axis-2-carrier.md` | deferred | P3 | M | [E2] | KEEP |  |
| `[#325]` | `325-carry-save-to-consumers-via-a-manifest-command-a.md` | deferred | P3 | S | [E2] | KEEP | dangling citation `#236` |
| `[#327]` | `327-protocols-as-interface-genre-ruling.md` | deferred | P2 | M | [E6] | KEEP |  |
| `[#329]` | `329-vs-code-ownership-visualization.md` | deferred | P3 | S | [E6] | KEEP |  |
| `[#331]` | `331-consumer-backlog-schema-adoption-ruling.md` | deferred | P2 | S | [E6] | KEEP |  |
| `[#332]` | `332-fleet-dependency-version-parity.md` | deferred | P2 | M | [E6] | KEEP |  |
| `[#334]` | `334-fleet-wide-ruff-hook-id-migration-ruff-ruff-chec.md` | open | P3 | S | [E6] | KEEP |  |
| `[#340]` | `340-ship-pre-flight-validator-honors-the-consumer-re.md` | open | P2 | S | [E7] | KEEP |  |
| `[#341]` | `341-codex-producer-lane-activation-mechanism.md` | open | P2 | S | [E7] | KEEP |  |
| `[#342]` | `342-fleet-parity-gate-ahead-max-fidelity-hardening.md` | open | P3 | S | [E6] | KEEP |  |
| `[#343]` | `343-fleet-parity-ship-gate-only-scoping.md` | open | P3 | S | [E6] | KEEP | dangling citation `#337` |
| `[#345]` | `345-externalize-the-adr-101-frozensets-machine-reada.md` | open | P2 | M | [E2] | KEEP |  |
| `[#347]` | `347-formalize-the-engineering-loop-harness-end-to-en.md` | open | P2 | M | [E7] | KEEP |  |
| `[#351]` | `351-fleet-python-upgrade-ticket.md` | open | P3 | M | [E6] | KEEP |  |
| `[#354]` | `354-w6-seed-1-recurrence-half.md` | open | P2 | M | [E8] | KEEP |  |
| `[#357]` | `357-silent-rule-census-run-2.md` | open | P2 | M | [E8] | KEEP |  |
| `[#359]` | `359-phantom-enforcement-protocols-handoff-process-md.md` | open | P1 | M | [E8] | KEEP |  |
| `[#361]` | `361-adr-immutability-s-real-coverage-is-declared-onl.md` | open | P3 | S | [E8] | KEEP |  |
| `[#362]` | `362-242-carries-a-substantive-guard-loss-not-status.md` | open | P2 | M | [E8] | KEEP |  |
| `[#365]` | `365-promote-residual-completeness-from-exempt-to-cov.md` | open | P3 | S | [E8] | KEEP |  |
| `[#369]` | `369-wire-boundary-headers-py-check-into-pre-commit.md` | open | P3 | S | [E8] | KEEP |  |
| `[#371]` | `371-consumer-editor-config-write-through-declared-at.md` | open | P2 | S | [E8] | KEEP |  |
| `[#383]` | `383-execution-waves-per-surface.md` | open | P2 | L | [E9] | KEEP |  |
| `[#385]` | `385-l4-tech-currency-lane.md` | open | P3 | M | [E9] | KEEP |  |
| `[#387]` | `387-rewrite-the-buy-vs-build-intake-before-anything.md` | open | P2 | S | [E7] | KEEP |  |
| `[#388]` | `388-the-10-20-repo-fleet-scale-target-is-fabricated.md` | open | P3 | S | [E5] | KEEP |  |
| `[#389]` | `389-prompt-lint-gate-the-five-architect-fields-befor.md` | open | P2 | S | [E2] | KEEP |  |
| `[#390]` | `390-resolve-the-adr-87-effort-ownership-contradictio.md` | open | P2 | S | [E1] | KEEP |  |
| `[#392]` | `392-fleet-analytics-rename-alias-loses-history-on-pa.md` | open | P3 | S | [E9] | KEEP |  |
| `[#393]` | `393-corp-sca-rot-review-confirm-live-or-retire-3-can.md` | open | P3 | S | [E9] | KEEP | Done-when names an artifact absent from the tree: `config/category_mapping.yaml`, `config/excluded.yaml`, `requirements.txt` |
| `[#400]` | `400-ownership-model-the-hub-mandated-structure-repo.md` | open | P3 | S | [E8] | KEEP |  |
| `[#401]` | `401-ai-council-routing-still-armed-at-the-deleted-hu.md` | open | P2 | S | [E2] | KEEP |  |
| `[#402]` | `402-intake-naming-clause-deploy-the-yyyy-mm-dd-class.md` | open | P3 | S | [E8] | KEEP | dangling citation `#398` |
| `[#403]` | `403-extend-doc-claims-to-architecture-s-machine-deri.md` | open | P3 | S | [E7] | KEEP | dangling citation `#321` |
| `[#404]` | `404-gen-handoff-execution-mode-supplement-leak-mode.md` | open | P2 | S | [E1] | KEEP |  |
| `[#405]` | `405-session-end-leftover-check-nothing-verifies-no-l.md` | open | P2 | S | [E2] | KEEP |  |
| `[#413]` | `413-colors-semantics-visually-distinguish-global-hub.md` | open | P2 | S | [E8] | KEEP |  |
| `[#414]` | `414-self-acting-on-main-incident-family-a-session-ch.md` | open | P2 | S | [E2] | KEEP |  |
| `[#418]` | `418-automation-fleet-audit-records-0-10-baselines-a.md` | open | P2 | S | [E2] | KEEP |  |
| `[#419]` | `419-we-run-routines-whose-output-nobody-consumes.md` | open | P2 | M | [E7] | KEEP |  |
| `[#420]` | `420-does-a-top-level-docs-archive-still-make-sense.md` | open | P3 | S | [E5] | KEEP |  |
| `[#422]` | `422-reflow-framing-s-cold-filled-flip-is-partial-by.md` | open | P2 | S | [E1] | KEEP |  |
| `[#426]` | `426-declare-consumer-consumption-path-for-every-live.md` | open | P2 | M | [E7] | KEEP |  |
| `[#427]` | `427-region-templates-carry-a-repo-position-dependent.md` | open | P3 | S | [E8] | KEEP |  |
| `[#428]` | `428-nightly-triage-reports-a-dead-producer-to-every.md` | open | P2 | S | [E7] | KEEP | dangling citation `#434` |
| `[#430]` | `430-consumer-template-rejects-root-conftest-py-fleet.md` | open | P2 | M | [E6] | KEEP |  |
| `[#431]` | `431-codex-review-silently-drops-the-doc-lane-on-any.md` | open | P2 | S | [E7] | KEEP |  |
| `[#438]` | `438-codify-gate-class-posture-terra-design-review-be.md` | open | P3 | S | [E3] | KEEP | dangling citation `#436` |
| `[#440]` | `440-make-the-tasks-id-ledger-tamper-evident-a-delete.md` | open | P2 | S | [E7] | KEEP |  |
| `[#442]` | `442-plugin-command-cache-staleness-cached-command-te.md` | open | P2 | M | [E2] | KEEP |  |
| `[#445]` | `445-codex-review-wrapper-path-guard-reports-success-h.md` | open | P2 | S | [E7] | KEEP |  |
| `[#447]` | `447-ratchet-raise-local-hook-bootstrap-deadlock.md` | open | P3 | S | [E1] | KEEP |  |
| `[#448]` | `448-a11-staged-diff-guard-cover-every-candidate-bun.md` | open | P2 | S | [E8] | KEEP |  |
| `[#451]` | `451-ca-layer-edge-check-ai-council-precedent.md` | open | P2 | M | [E2] | KEEP |  |
| `[#454]` | `454-closure-ids-negation-defect-negated-mention-reads.md` | open | P2 | S | [E2] | KEEP |  |
| `[#457]` | `457-inherited-live-repo-test-failures.md` | open | P2 | S | [E2] | KEEP |  |
| `[#470]` | `470-audit-py-checks-crashes-on-a-cp1252-console.md` | open | P3 | S | [E7] | KEEP |  |
| `[#477]` | `477-deployed-version-check-keys-registry-by-basename.md` | open | P2 | S | [E2] | KEEP |  |
| `[#478]` | `478-changelog-sentinel-drops-pep-440-suffixes.md` | open | P2 | S | [E2] | KEEP |  |
| `[#485]` | `485-lf-enforcing-write-helper-replaces-a-gotcha.md` | open | P3 | S | [E2] | KEEP |  |
| `[#487]` | `487-closure-proposal-consumption-arc-139-parked-prop.md` | open | P2 | L | [E7] | KEEP |  |
| `[#491]` | `491-gemini-scanning-lane-ruling-r-g-plus-an-acceptan.md` | deferred | P3 | S | [E7] | KEEP |  |
| `[#492]` | `492-grok-review-lane-acceptance-gated-2026-08-07-mea.md` | deferred | P3 | S | [E7] | KEEP |  |
| `[#493]` | `493-b-2-investigation-the-scheduled-fleet-baseline-t.md` | open | P2 | S | [E7] | KEEP |  |
| `[#495]` | `495-tech-currency-cadence-give-385-a-recurring-lane.md` | deferred | P3 | S | [E9] | KEEP |  |
| `[#496]` | `496-organ-to-component-attributes-the-pre-push-organ.md` | open | P3 | S | [E2] | KEEP |  |
| `[#497]` | `497-carrier-mesh-py-75-still-claims-the-informant-lo.md` | open | P3 | S | [E2] | KEEP |  |
| `[#499]` | `499-promote-the-review-artifact-coverage-leg-from-ad.md` | deferred | P3 | M | [E2] | KEEP |  |
| `[#500]` | `500-the-stop-hook-s-backlog-advisory-reads-a-correct.md` | open | P3 | S | [E2] | KEEP |  |
| `[#506]` | `506-whole-set-p10-grooming-arc-full-open-set.md` | open | P2 | M | [E5] | KEEP |  |
| `[#509]` | `509-invoke-dispatch-resolves-claude-prompts-dir.md` | open | P3 | S | [E7] | KEEP |  |
| `[#510]` | `510-scope-r1-exemption-to-enumerated-lanes.md` | open | P2 | M | [E2] | KEEP |  |
| `[#511]` | `511-handoff-cut-cost-is-session-authoring.md` | open | P2 | M | [E1] | KEEP |  |
| `[#514]` | `514-two-rival-lane-branch-re-constants-reconcile-them.md` | open | P1 | M | [E2] | KEEP |  |
| `[#518]` | `518-audit-py-git-runs-unscrubbed-and-undecoded-at-one.md` | open | P2 | S | [E2] | KEEP |  |
| `[#519]` | `519-the-close-path-is-two-edits-and-nothing-makes-a.md` | open | P1 | M | [E2] | KEEP |  |
| `[#520]` | `520-no-sanctioned-way-to-retire-a-committed-bundle-w.md` | open | P2 | S | [E2] | KEEP |  |
| `[#522]` | `522-re-cut-bundle-carries-predecessor-payloads.md` | open | P2 | M | [E2] | KEEP |  |
| `[#523]` | `523-executive-index-render-leg-on-generated-backlog.md` | open | P2 | M | [E7] | KEEP |  |
| `[#526]` | `526-root-hygiene-audit-which-root-files-must-be-root.md` | open | P3 | S | [E5] | KEEP |  |
| `[#528]` | `528-lane-latency-full-suite-multiplied-across-a-batch.md` | open | P1 | M | [E7] | KEEP |  |
| `[#531]` | `531-lane-grammar-enforcement-at-provisioning-the-enu.md` | open | P2 | S | [E2] | KEEP |  |
| `[#533]` | `533-decompose-the-audit-py-check-monolith-into-scrip.md` | open | P2 | M | [E2] | KEEP |  |
| `[#534]` | `534-audit-py-line-locators-on-four-open-rows-died-at-t.md` | open | P2 | S | [E2] | KEEP |  |
| `[#535]` | `535-audit-py-has-two-module-identities-in-one-process.md` | open | P2 | S | [E7] | KEEP |  |
| `[#538]` | `538-the-nb4-c-playbook-gap-arc-twelve-paste-ready-acts.md` | open | P2 | M | [E3] | KEEP |  |
| `[#540]` | `540-harvest-batch-py-read-the-board-then-fetch-packets.md` | open | P3 | S | [E7] | KEEP | Done-when names an artifact absent from the tree: `scripts/harvest_batch.py` |
| `[#541]` | `541-scale-out-substrate-decision-unowned-after-two-rep.md` | open | P3 | S | [E7] | KEEP |  |
| `[#542]` | `542-architecture-md-still-claims-four-doc-rot-sub-dete.md` | open | P3 | S | [E5] | KEEP |  |
| `[#546]` | `546-adr-60-docs-taxonomy-no-longer-describes-the-tree.md` | open | P3 | S | [E4] | KEEP |  |
| `[#547]` | `547-split-brain-prevention-has-no-referent-under-v6.md` | open | P3 | S | [E1] | KEEP |  |
| `[#548]` | `548-intake-12-settled-ownership-manifest-has-no-carrier.md` | open | P2 | S | [E4] | KEEP | dangling citation `#328` |
| `[#549]` | `549-fleet-hygiene-plan-of-record-has-no-carrier.md` | deferred | P2 | S | [E4] | KEEP | dangling citation `#328` |
| `[#550]` | `550-intake-14-ruled-siem-requirements-half-dispositioned.md` | open | P3 | S | [E4] | KEEP | dangling citation `#328` |
| `[#551]` | `551-audit-artifacts-carry-no-status-field.md` | open | P2 | S | [E5] | KEEP |  |
| `[#552]` | `552-window-close-disposition-and-archival-routine.md` | open | P2 | M | [E2] | KEEP | dangling citation `#398` |
| `[#553]` | `553-adr-census-in-decisions-readme-is-ungated-and-wrong.md` | open | P3 | S | [E5] | KEEP |  |
| `[#554]` | `554-devcontainer-provisioning-script-nb4-g-stage-1.md` | open | P2 | M | [E7] | KEEP |  |
| `[#555]` | `555-closing-campaign-batch-1-kill-candidates-instrum.md` | open | P1 | M | [E7] | KEEP |  |
| `[#559]` | `559-kernel-lab-check-tiering-dev-knowledge-kernel-as.md` | open | P2 | L | [E6] | KEEP |  |
| `[#560]` | `560-review-artifact-coverage-reads-only-the-first-br.md` | open | P2 | S | [E2] | KEEP |  |
| `[#561]` | `561-re-base-the-compute-plan-onto-the-hetzner-cx-sha.md` | open | P2 | S | [E7] | KEEP |  |
| `[#564]` | `564-lifecycle-archival-implemented-adrs-and-decided-int.md` | open | P2 | M | [E4] | KEEP |  |
| `[#567]` | `567-cx53-daily-driver-substrate-lane-the-every-prompt-r.md` | open | P2 | M | [E7] | KEEP |  |
| `[#568]` | `568-provider-config-as-code-dev-knowledge-as-source-of-.md` | open | P2 | M | [E7] | KEEP |  |
| `[#570]` | `570-consume-the-tech-adoption-ledger-w-wave.md` | open | P2 | L | [E7] | KEEP |  |
| `[#571]` | `571-define-architecture-described-surface.md` | open | P2 | M | [E5] | KEEP |  |
| `[#572]` | `572-intake-funnel-completion-carrier.md` | open | P2 | M | [E4] | KEEP |  |
| `[#573]` | `573-lychee-zero-baseline-md-link-gate.md` | open | P3 | S | [E2] | KEEP | Done-when names an artifact absent from the tree: `lychee.toml` |
| `[#574]` | `574-batch-manifest-emitted-by-gen-lane-contract.md` | open | P2 | M | [E7] | KEEP | `[#777]` in the body is a deliberate synthetic example, not a citation |
| `[#575]` | `575-telemetry-store-performance-and-silent-drops.md` | open | P2 | M | [E7] | KEEP |  |
| `[#576]` | `576-telemetry-read-path-lane.md` | open | P2 | M | [E7] | KEEP |  |
| `[#578]` | `578-the-earned-mitigated-rerun-one-slot-role-reminder.md` | open | P3 | S | [E7] | KEEP |  |
| `[#579]` | `579-code-doctrine-fdd-one-adr-merging-intakes-31-and.md` | open | P1 | L | [E2] | KEEP |  |
| `[#580]` | `580-state-as-data-atomic-id-allocation-and-tasks-as.md` | open | P1 | M | [E7] | KEEP |  |
| `[#581]` | `581-backlog-vitals-three-flow-instruments-a-committe.md` | open | P1 | L | [E7] | KEEP |  |
| `[#582]` | `582-substrate-router-one-gated-enum-a-capability-key.md` | open | P1 | L | [E7] | KEEP |  |
| `[#583]` | `583-green-by-skip-sweep-a-check-that-cannot-obtain-g.md` | open | P2 | M | [E2] | KEEP |  |
| `[#585]` | `585-suite-red-test-anchor-gate-probe-distinguishes-i.md` | open | P2 | S | [E5] | KEEP |  |
| `[#586]` | `586-suite-red-test-no-gate-hook-or-script-reads-the.md` | open | P3 | S | [E7] | KEEP |  |
| `[#587]` | `587-p-1-invert-the-journal-anchor-check-to-a-single.md` | open | P1 | M | [E7] | KEEP |  |
| `[#588]` | `588-p-2-build-the-spine-parent-map-in-one-git-proces.md` | open | P1 | S | [E7] | KEEP |  |
| `[#589]` | `589-one-line-per-row-the-backlog-view-projection-wit.md` | open | P1 | M | [E5] | KEEP | Done-when byte predicate (<70,000 B) FALSE on main today (70,668 B) |
| `[#590]` | `590-the-audits-index-is-regenerated-on-read-never-me.md` | open | P2 | S | [E5] | KEEP | 3 of 4 Done-when legs witnessed on main; 4th is an observation window |
| `[#591]` | `591-substrate-validator-layer-2-refuse-a-contract-wh.md` | open | P2 | M | [E2] | KEEP |  |
| `[#592]` | `592-dispatch-drift-organ-every-literal-command-in-ch.md` | open | P2 | S | [E2] | KEEP |  |
| `[#593]` | `593-codespaces-chain-repair-hub-half-uv-in-the-image.md` | open | P2 | M | [E7] | KEEP |  |
| `[#594]` | `594-layer-3-router-the-hub-prerequisites-only-not-th.md` | open | P3 | M | [E7] | KEEP |  |
| `[#595]` | `595-consumer-at-landing-gate-for-docs-audits-the-sub.md` | open | P2 | M | [E2] | KEEP |  |
| `[#596]` | `596-family-3-at-the-proof-layer-the-class-583-names.md` | open | P3 | S | [E2] | KEEP |  |
| `[#597]` | `597-p-4-a-declared-tier-per-check-and-p-3-s-telemetr.md` | open | P2 | M | [E7] | KEEP |  |
| `[#598]` | `598-p-6-a-slow-marker-selector-so-tiered-gating-has.md` | open | P3 | S | [E7] | KEEP |  |
| `[#599]` | `599-generated-standing-vs-new-drift-block-in-the-han.md` | open | P2 | M | [E1] | KEEP |  |
| `[#600]` | `600-delete-p10-from-the-shipped-probe-manifest-and-g.md` | open | P2 | S | [E1] | KEEP |  |
| `[#601]` | `601-supplement-folded-audit-check-a-filled-supplemen.md` | open | P2 | S | [E2] | KEEP |  |
| `[#602]` | `602-land-the-ruled-dispatch-verb-in-the-bundle-s-for.md` | open | P2 | M | [E1] | KEEP |  |
| `[#603]` | `603-an-operator-interface-capability-file-the-facts.md` | open | P3 | S | [E1] | KEEP |  |
| `[#604]` | `604-admit-win-tooling-and-terminal-setup-to-the-depl.md` | open | P2 | S | [E6] | KEEP |  |
| `[#605]` | `605-de-hardcode-consumer-root-resolution-in-deploy-t.md` | open | P2 | M | [E2] | KEEP |  |
| `[#606]` | `606-the-win-tooling-first-slice-instantiation-arc-ru.md` | open | P2 | L | [E6] | KEEP |  |
| `[#607]` | `607-playbook-census-discharge-the-mechanical-half-of.md` | open | P2 | S | [E5] | KEEP |  |
| `[#608]` | `608-tiling-aware-journal-read-the-rotation-seam-befo.md` | open | P1 | S | [E7] | KEEP |  |
| `[#609]` | `609-free-ruff-ratchet-the-zero-cost-python-standard.md` | open | P2 | S | [E6] | KEEP |  |
| `[#610]` | `610-the-night-batch-protocol-named-with-its-two-verb.md` | open | P2 | M | [E7] | KEEP |  |
| `[#611]` | `611-handoff-process-v7-the-minimal-bundle-package.md` | open | P2 | M | [E1] | KEEP |  |
| `[#612]` | `612-doc-rot-row-body-archival.md` | open | P2 | M | [E5] | KEEP |  |
| `[#613]` | `613-in-repo-routing-table-agreement-check.md` | open | P2 | M | [E2] | KEEP |  |
| `[#615]` | `615-model-attribution-signature-trailer-on-every.md` | open | P2 | M | [E2] | KEEP |  |
| `[#616]` | `616-flip-condition-every-adr-records-what-evidence-w.md` | open | P2 | S | [E4] | KEEP |  |
| `[#617]` | `617-file-distillation-the-output-half-and-the-only-w.md` | open | P2 | M | [E5] | KEEP |  |
| `[#618]` | `618-the-silently-stale-codespace-clone-detection-and.md` | open | P2 | M | [E7] | KEEP |  |
| `[#619]` | `619-the-fm-2-to-fm-4-funnel-health-coupling-is-dead.md` | open | P2 | M | [E1] | KEEP |  |
| `[#620]` | `620-retire-the-root-readme-prohibition-across-the-fl.md` | open | P2 | M | [E5] | KEEP |  |
| `[#621]` | `621-adr-114-option-c-the-nine-repo-vision-md-to-read.md` | open | P2 | L | [E5] | KEEP |  |
| `[#622]` | `622-promote-readme-md-into-the-adr-38-canonical-mand.md` | open | P3 | M | [E5] | KEEP |  |
| `[#623]` | `623-mechanize-the-journal-anchor-record-line.md` | open | P2 | S | [E7] | KEEP |  |
| `[#624]` | `624-nothing-watches-a-blockers-status.md` | open | P2 | M | [E2] | KEEP |  |
| `[#625]` | `625-the-rule-adherence-eval-corpus-fresh.md` | open | P1 | M | [E7] | KEEP | Done-when names an artifact absent from the tree: `/.claude/rules/core-invariants.md` |
| `[#626]` | `626-logs-retention-exempts-the-prefixes-that-accumulate.md` | open | P2 | M | [E7] | KEEP |  |
| `[#627]` | `627-agy-route-is-inert-no-row-authorizes-analysis-admission.md` | open | P2 | M | [E7] | KEEP | Done-when names an artifact absent from the tree: `ROUTING.md` |
| `[#628]` | `628-dc2-recut-essentials-dissolution-is-a-release-act.md` | open | P1 | L | [E5] | KEEP |  |
| `[#629]` | `629-a-contract-amendment-cannot-subtract-an-act.md` | open | P1 | M | [E2] | KEEP |  |
| `[#631]` | `631-a-freeze-cannot-bind-a-rule-that-postdates-it.md` | open | P1 | M | [E2] | KEEP |  |
| `[#632]` | `632-codespace-is-admitted-for-transport-and-unstable-for-inference.md` | open | P1 | L | [E7] | KEEP | Done-when names an artifact absent from the tree: `tests/test_dispatch_helpers_codespace.py` |
| `[#633]` | `633-boot-session-gains-history-delta-and-equilibrium-map.md` | open | P2 | M | [E1] | KEEP |  |
| `[#634]` | `634-dispatch-run-accepts-github-token-as-the-anthropic-check.md` | open | P1 | S | [E7] | KEEP |  |

## Row files — retired allocation records, out of the queue (140)

Verdict **KEEP** for every row below, and the verdict is not discretionary: ADR-107 §6.3 rules **retire, never delete** — the file *is* the allocation record that keeps its id from being re-issued, `gen_task_tree.py --prune` is refused, and `scripts/gen_task_tree.py` reports an unreferenced file carrying the `generates: BACKLOG.md` marker as a legitimate retired record. All 140 carry that marker and a terminal `status:`.

| id | file | status | Verdict | Note |
|---|---|---|---|---|
| `[#35]` | `35-fix-the-self-owned-low-severity-cleanups.md` | closed | KEEP |  |
| `[#41]` | `41-split-architecture-processes-into-process-md-if.md` | closed | KEEP |  |
| `[#71]` | `71-reconcile-environment-md-s-claude-directory-tree.md` | closed | KEEP |  |
| `[#99]` | `99-fleet-health-digest-names-the-failing-check-per.md` | closed | KEEP |  |
| `[#122]` | `122-retire-the-path-shim.md` | closed | KEEP |  |
| `[#126]` | `126-backpressure-loop-pattern-evaluation.md` | retired | KEEP |  |
| `[#127]` | `127-verify-skill-failure-output-contract.md` | closed | KEEP |  |
| `[#132]` | `132-organ-index-generator.md` | closed | KEEP |  |
| `[#162]` | `162-vocab-decision.md` | closed | KEEP |  |
| `[#213]` | `213-playbook-rule-history-condensation.md` | closed | KEEP |  |
| `[#215]` | `215-onboard-verify-methodology-in-a-new-repo.md` | closed | KEEP |  |
| `[#239]` | `239-follow-up.md` | closed | KEEP |  |
| `[#263]` | `263-protocols-edge-map-reconciliation-residuals.md` | closed | KEEP |  |
| `[#266]` | `266-codify-the-test-scoped-grant-language-lesson.md` | closed | KEEP |  |
| `[#270]` | `270-operator-load-gauge.md` | closed | KEEP |  |
| `[#276]` | `276-d2-per-consumer-waiver-honoring.md` | closed | KEEP |  |
| `[#280]` | `280-propagate-the-intake-area-to-greenfield-consumer.md` | closed | KEEP |  |
| `[#281]` | `281-re-peg-the-ai-council-adr-66-story-map-convergen.md` | closed | KEEP |  |
| `[#282]` | `282-fleet-gitattributes-eol-normalization-parity.md` | closed | KEEP |  |
| `[#283]` | `283-corp-monorepo-hybrid-classifier-json-1-08mb-dupl.md` | closed | KEEP |  |
| `[#290]` | `290-floor-carrier-verify-teeth-self-heal.md` | closed | KEEP |  |
| `[#296]` | `296-audit-py-repo-name-repo-path-doesn-t-persist-its.md` | closed | KEEP |  |
| `[#315]` | `315-install-md-uniform-fleet-wide-hub-owned-deploy-c.md` | closed | KEEP |  |
| `[#320]` | `320-fleet-backup-posture.md` | closed | KEEP |  |
| `[#323]` | `323-design-question.md` | closed | KEEP |  |
| `[#335]` | `335-exempt-templates-from-the-reconciled-versions-ch.md` | closed | KEEP |  |
| `[#338]` | `338-codex-review-drift-consolidation.md` | closed | KEEP |  |
| `[#344]` | `344-session-close-gate-for-handoff-generation-consum.md` | closed | KEEP |  |
| `[#346]` | `346-persist-the-two-tier-new-path-executor-rule-into.md` | closed | KEEP |  |
| `[#348]` | `348-backlog-grooming-as-a-standing-routine-not-ad-ho.md` | closed | KEEP |  |
| `[#349]` | `349-mechanize-session-discipline-inheritance.md` | closed | KEEP |  |
| `[#350]` | `350-handoff-process-refinements.md` | closed | KEEP |  |
| `[#352]` | `352-versioned-vscode-region-decoration.md` | closed | KEEP |  |
| `[#353]` | `353-session-boot-contract-hardening.md` | closed | KEEP |  |
| `[#356]` | `356-ruling-w-and-the-merge-delegation-composite-are.md` | closed | KEEP |  |
| `[#358]` | `358-ecosystem-parity-surfaces-yaml-misdescribes-its.md` | closed | KEEP | dangling citation `#337` |
| `[#360]` | `360-protocols-definition-of-done-md-106-109-expired.md` | closed | KEEP |  |
| `[#363]` | `363-codex-review-routed-a-code-shaped-diff-through-t.md` | closed | KEEP | dangling citation `#333` |
| `[#364]` | `364-doc-rot-s-length-cap-blocks-353-from-doing-its-j.md` | retired | KEEP |  |
| `[#366]` | `366-residual-completeness-scans-the-working-tree-not.md` | closed | KEEP |  |
| `[#367]` | `367-handoff-process-held-at-version-5-7-while-gainin.md` | closed | KEEP |  |
| `[#370]` | `370-is-the-owner-hub-owner-repo-ownership-model-two.md` | closed | KEEP |  |
| `[#382]` | `382-desired-state-data-model-intake-adr.md` | closed | KEEP | dangling citation `#381` |
| `[#386]` | `386-codify-the-proven-delivery-loop-into-playbook-ow.md` | closed | KEEP |  |
| `[#391]` | `391-wire-fleet-analytics-into-a-nightly-lane-or-narr.md` | closed | KEEP | dangling citation `#384` |
| `[#394]` | `394-analytics-coverage-gap-corp-monorepo-no-edit-rec.md` | closed | KEEP |  |
| `[#396]` | `396-extract-scripts-gitenv-py-the-git-env-scrub-is-i.md` | closed | KEEP |  |
| `[#397]` | `397-scripts-target-structure-rule-on-the-mapped-grou.md` | closed | KEEP |  |
| `[#399]` | `399-templates-handoff-v5-readme-md-tmpl-phantom-sour.md` | closed | KEEP |  |
| `[#406]` | `406-commit-time-doc-rot-surfacing-an-over-threshold.md` | closed | KEEP |  |
| `[#407]` | `407-universal-fleet-python-style-functional-vs-oop-s.md` | closed | KEEP |  |
| `[#408]` | `408-auto-coupled-doc-updates-closing-a-backlog-item.md` | closed | KEEP |  |
| `[#409]` | `409-standing-night-batch-code-review-formalize-as-ro.md` | closed | KEEP |  |
| `[#410]` | `410-standing-night-batch-architecture-review-formali.md` | closed | KEEP |  |
| `[#411]` | `411-standing-night-batch-creative-session-and-the-re.md` | closed | KEEP |  |
| `[#412]` | `412-subagent-workflow-routing-configured-fan-out-onl.md` | closed | KEEP |  |
| `[#415]` | `415-tests-must-bind-fixtures-not-live-mutable-repo-c.md` | closed | KEEP |  |
| `[#416]` | `416-ai-council-architecture-md-codemap-drift-at-l23.md` | closed | KEEP | dangling citation `#262`, `#295` |
| `[#417]` | `417-check-dirty-tree-runs-with-no-pathspec-so-the-st.md` | closed | KEEP | dangling citation `#355` |
| `[#421]` | `421-verify-handoff-probes-cannot-bind-a-repo-root-do.md` | closed | KEEP |  |
| `[#423]` | `423-the-integration-sequence-runs-on-prose-every-tim.md` | closed | KEEP |  |
| `[#424]` | `424-backlog-depends-on-gates-are-inert-depid-re-requ.md` | closed | KEEP |  |
| `[#425]` | `425-the-suite-is-green-on-a-format-the-file-does-not.md` | closed | KEEP |  |
| `[#429]` | `429-worktree-provisioning-is-not-portable-across-the.md` | closed | KEEP |  |
| `[#432]` | `432-adopt-uv-as-the-environment-dependency-toolchain.md` | closed | KEEP |  |
| `[#433]` | `433-backlog-restructure-build-thin-engine-backlog-md.md` | closed | KEEP |  |
| `[#435]` | `435-steward-intake-18-handoff-process-v6-to-a-ratifi.md` | closed | KEEP |  |
| `[#437]` | `437-closes-re-quoting-defect-backtick-strip-before-t.md` | closed | KEEP |  |
| `[#439]` | `439-adr-107-strangler-step-3-the-source-of-truth-fli.md` | closed | KEEP |  |
| `[#441]` | `441-way-of-working-the-default-is-one-strong-self-co.md` | closed | KEEP |  |
| `[#443]` | `443-planning-artifacts-outside-the-three-enforced-cl.md` | closed | KEEP |  |
| `[#444]` | `444-release-tier1-lifecycle-0-1-11-ship-the-437-quot.md` | closed | KEEP |  |
| `[#446]` | `446-section-b-b-one-round-trip-boot-build-the-v6-ca.md` | closed | KEEP |  |
| `[#449]` | `449-assembled-paste-byte-budget.md` | closed | KEEP |  |
| `[#450]` | `450-per-section-intake-ratification.md` | closed | KEEP |  |
| `[#452]` | `452-433-382-dependency-is-prose-only.md` | retired | KEEP |  |
| `[#453]` | `453-cloud-night-run-runbook-container-gaps.md` | closed | KEEP |  |
| `[#455]` | `455-registry-md-derived-field-drift-checker.md` | closed | KEEP |  |
| `[#456]` | `456-ruling-blocked-cohort-sweep-adr-108-re-route.md` | closed | KEEP |  |
| `[#458]` | `458-playbook-note-gates-never-race-commits.md` | closed | KEEP |  |
| `[#459]` | `459-architecture-prose-desired-state-organs.md` | closed | KEEP |  |
| `[#460]` | `460-history-dailies-write-only-no-consumer.md` | closed | KEEP | dangling citation `#254` |
| `[#461]` | `461-mechanize-window-report-metrics.md` | closed | KEEP |  |
| `[#462]` | `462-terminal-setup-absent-from-every-machine-member.md` | closed | KEEP |  |
| `[#463]` | `463-win-tooling-onboarding-debt-unchanged-since-admi.md` | closed | KEEP |  |
| `[#464]` | `464-corp-consumer-governance-drift-live-weeks-unacti.md` | closed | KEEP |  |
| `[#465]` | `465-fleet-audit-writer-integrity-skip-as-pass-overwr.md` | closed | KEEP |  |
| `[#466]` | `466-intake-flip-candidate-post-discharge.md` | closed | KEEP |  |
| `[#467]` | `467-paste-budget-repomix-rejected-on-measurement.md` | closed | KEEP |  |
| `[#468]` | `468-why-not-a-frontmatter-library-the-measured-ratio.md` | closed | KEEP |  |
| `[#469]` | `469-codex-review-code-lane-runs-an-unpinned-model.md` | closed | KEEP |  |
| `[#471]` | `471-generators-inherit-platform-newline-translation.md` | closed | KEEP |  |
| `[#472]` | `472-membership-census-diffs-declaration-vs-surfaces.md` | closed | KEEP |  |
| `[#473]` | `473-handoff-suffix-sibling-resolution.md` | closed | KEEP | dangling citation `#372` |
| `[#474]` | `474-gen-task-tree-write-import-recovery-footgun.md` | closed | KEEP |  |
| `[#475]` | `475-seal-identity-as-a-pre-commit-gate-on-bundles.md` | closed | KEEP |  |
| `[#476]` | `476-backpressure-flags-lane-owned-fleet-audit-dailies.md` | closed | KEEP |  |
| `[#479]` | `479-session-end-backpressure-swallows-internal-errors.md` | superseded | KEEP |  |
| `[#480]` | `480-code-impact-merge-without-review-artifact.md` | closed | KEEP |  |
| `[#481]` | `481-enforcement-coverage-organ-id-names-a-retired-organ.md` | closed | KEEP |  |
| `[#482]` | `482-boundary-glob-engine-repair-true-glob.md` | closed | KEEP |  |
| `[#483]` | `483-preflight-contract-enforcement-question.md` | closed | KEEP |  |
| `[#484]` | `484-adr106-system-python-divergence-deferral.md` | closed | KEEP |  |
| `[#486]` | `486-desired-state-report-py-dies-on-a-cp1252-console.md` | closed | KEEP |  |
| `[#488]` | `488-priority-axis-the-backlog-has-no-ranking-functio.md` | closed | KEEP |  |
| `[#489]` | `489-safe-remove-m2-m3-as-the-l3-real-deletion-lifecy.md` | retired | KEEP |  |
| `[#490]` | `490-parity-manifest-9-9-fleet-green-currently-measur.md` | closed | KEEP |  |
| `[#494]` | `494-ladder-ratification-l0-l5-promote-vs-leave-is-un.md` | closed | KEEP |  |
| `[#498]` | `498-carried-block-ff-push-is-non-executable-the-ff-g.md` | closed | KEEP |  |
| `[#501]` | `501-server-side-report-only-recorder-github-actions.md` | closed | KEEP | dangling citation `#255` |
| `[#502]` | `502-mutmut-mutation-testing-evaluation-ci-hosted.md` | closed | KEEP |  |
| `[#503]` | `503-doc-currency-eight-sites-the-world-moved-past.md` | closed | KEEP |  |
| `[#504]` | `504-block-ff-push-docstring-contradicts-fail-closed.md` | closed | KEEP |  |
| `[#505]` | `505-batch-protocol-encoding-parallel-execution-wow.md` | closed | KEEP |  |
| `[#507]` | `507-report-only-wall-fourth-leg-precommit-run-all-files.md` | closed | KEEP |  |
| `[#508]` | `508-lane-prefix-enum-cardinality-coupling.md` | closed | KEEP |  |
| `[#512]` | `512-open-batch-refusal-doesnt-scrub-git-dir.md` | closed | KEEP | dangling citation `#355` |
| `[#513]` | `513-propagation-completeness-a-ruled-adoption-that-la.md` | closed | KEEP |  |
| `[#521]` | `521-syspath-substrate-shape-b-rollout-owner.md` | closed | KEEP |  |
| `[#524]` | `524-four-ruled-check-extensions.md` | closed | KEEP |  |
| `[#525]` | `525-architecture-ch2-ch6-organ-rows-for-the-load-gaug.md` | closed | KEEP |  |
| `[#527]` | `527-anti-direct-to-main-mechanism.md` | closed | KEEP |  |
| `[#529]` | `529-telemetry-v1-emit-stage-1-events-from-the-gate-m.md` | closed | KEEP |  |
| `[#530]` | `530-single-flight-dispatch-guard-one-contract-execut.md` | closed | KEEP |  |
| `[#532]` | `532-doc-rot-backlog-accretion-conflates-three-defect.md` | closed | KEEP |  |
| `[#536]` | `536-the-arm-2-row-length-pile-has-no-owner-and-the-con.md` | closed | KEEP |  |
| `[#537]` | `537-disposition-token-is-a-done-when-branch-nothing-de.md` | closed | KEEP |  |
| `[#539]` | `539-gen-lane-contract-py-assembly-not-generation-with.md` | closed | KEEP |  |
| `[#556]` | `556-505-is-closed-but-present-the-adr-65-done-items.md` | closed | KEEP |  |
| `[#557]` | `557-three-stale-dispositions-match-no-live-warn-the.md` | closed | KEEP |  |
| `[#558]` | `558-vision-md-still-describes-scripts-as-read-only-v.md` | closed | KEEP |  |
| `[#562]` | `562-grok-4-6-guarded-rerun-a-no-pack-sandbox-before-th.md` | closed | KEEP |  |
| `[#563]` | `563-backlog-md-as-a-read-only-view-layer-the-one-way-ex.md` | closed | KEEP |  |
| `[#565]` | `565-run-id-in-telemetry-emit-before-the-read-path-lane.md` | closed | KEEP |  |
| `[#566]` | `566-constraint-contention-tiebreak-implement-the-accept.md` | closed | KEEP |  |
| `[#569]` | `569-grouped-hygiene-two-standing-suite-reds-and-the-19-.md` | closed | KEEP |  |
| `[#577]` | `577-adopt-agents-md-as-the-portable-instruction-layer.md` | closed | KEEP |  |
| `[#584]` | `584-claude-md-10-in-lockstep-with-its-form-a-templat.md` | closed | KEEP |  |
| `[#614]` | `614-vision-superseded-by-a-recreated-root-readme.md` | closed | KEEP |  |
| `[#630]` | `630-manifest-lane-enum-must-equal-contract-slug-at-freeze.md` | closed | KEEP |  |

## Files NOT on main, reported for the record (2)

| id | file | State | Witness |
|---|---|---|---|
| `[#635]` | `tasks/635-sessionstart-refuses-a-non-integrator-session-on-the-primary.md` | dropped on recorded operator consent | `JOURNAL.md` 2026-09-05 (p); present in exactly one reachable tree, `1cefc303` |
| `[#636]` | `tasks/636-window-metrics-gains-a-ten-line-scorecard.md` | dropped on recorded operator consent | same |
