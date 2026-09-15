# .dev-knowledge BACKLOG
<!-- [#589] GENERATED VIEW — one line per row. NOT an import source: `gen_task_tree.py --write` refuses this file. -->
<!-- Do not edit directly; the line above is this file's machine identity. Each row shows
     id · [P][size] · title · DEFER-if-deferred · a pointer to its tasks/ file. The FULL
     body — Done-when, refs, kill-candidates, routine fields — lives in that file, which is
     the source of truth (ADR-107 §7.2, [#439]); theme and story are the enclosing headings.
     Regenerate: uv run --locked python scripts/gen_task_tree.py --emit-source -->

## Big picture

`.dev-knowledge` is the ecosystem's methodology brain: it absorbs lessons from every repo, universalizes them into enforced conventions, and audits the ecosystem against them — the LLM-development "scrum master" for all `Dev/` projects (VISION: Knowledge Guardian · Methodology Author · Auditor · Disseminator). The backlog advances that mission across eight mission themes plus one time-boxed execution arc.

**Themes (backbone) — epic ids:** [E1] Handoff continuity · [E2] Enforced governance · [E3] Lessons feedback loop · [E4] Decision management · [E5] Canonical-file integrity · [E6] Cross-repo universalization · [E7] Tooling & evaluation · [E8] ARC-5 execution (time-boxed arc, not a permanent mission theme) · [E9] Fleet Desired-State System (North Star)

---

## [E1] Handoff continuity
> As a session inheriting this repo, I want to pick up with full state and lose nothing.

### [S1] Match the handoff payload to the work mode
So that an architecture session inherits the big picture + vision while an execution session inherits lean task-state — one process, two payloads.
- [#511] [P2][M] The 30-minute handoff cut is ~99.8% session authoring, not machinery · tasks/511-handoff-cut-cost-is-session-authoring.md
- [#611] [P2][M] HANDOFF_PROCESS v7: the minimal-bundle package · tasks/611-handoff-process-v7-the-minimal-bundle-package.md
- [#720] [P3][S] The browser role file carries no pointer to the standing-rulings register, so a booting seat never learns a ruling landed after its ROLE PIN · tasks/720-handoff-boot-carries-no-pointer-to-the-standing-rulings-register.md
- [#633] [P2][M] /boot-session gains HISTORY DELTA and EQUILIBRIUM MAP — two GENERATED sections · tasks/633-boot-session-gains-history-delta-and-equilibrium-map.md
- [#733] [P1][S] Ratification #5: the operator never types a path and the browser never composes a boot line -- the SEAT-BOOT renders go to the transport · tasks/733-seat-boot-renders-land-on-the-transport-so-the-operator-never-types-a-path.md

### [S2] Finish the v5 handoff machinery deferred at the #149 flip
So that the canonical v5 handoff is fully implemented (generator) and mechanically verified (teeth), not just specified.
- [#293] [P3][S] Consumer runbook fan-out · tasks/293-consumer-runbook-fan-out.md
- [#298] [P3][S] Handoff-generator polish · tasks/298-handoff-generator-polish.md
- [#301] [P2][M] Session-plan artifact class · DEFER · tasks/301-session-plan-artifact-class.md
- [#390] [P2][S] Resolve the ADR-87 effort-ownership contradiction, then true up the prompt template · tasks/390-resolve-the-adr-87-effort-ownership-contradictio.md
- [#404] [P2][S] gen_handoff execution-mode SUPPLEMENT leak (mode-blind framing + P8 row) · tasks/404-gen-handoff-execution-mode-supplement-leak-mode.md
- [#447] [P3][S] Self-referential gate family — the committing act cannot satisfy the gate's own precondition · tasks/447-ratchet-raise-local-hook-bootstrap-deadlock.md
- [#422] [P2][S] `reflow_framing`'s cold→FILLED flip is partial by design, and nothing detects the self-contradiction it leaves · tasks/422-reflow-framing-s-cold-filled-flip-is-partial-by.md
- [#547] [P3][S] Split-brain prevention is instructed against a handoff section shape v6 does not produce · tasks/547-split-brain-prevention-has-no-referent-under-v6.md
- [#599] [P2][M] Generated standing-vs-NEW drift block in the handoff residual · tasks/599-generated-standing-vs-new-drift-block-in-the-han.md
- [#600] [P2][S] Delete P10 from the shipped probe manifest and gate the boundedness condition · tasks/600-delete-p10-from-the-shipped-probe-manifest-and-g.md
- [#602] [P2][M] Land the ruled dispatch verb in the bundle's forms card, and extend the agreement gate to the bundle sites · tasks/602-land-the-ruled-dispatch-verb-in-the-bundle-s-for.md
- [#643] [P1][M] The handoff preflight reports P11 carriage after the cut instead of refusing it, and two consecutive bundles shipped the same defect · tasks/643-preflight-reports-p11-carriage-instead-of-refusing.md
- [#603] [P3][S] An operator-interface capability file — the facts every seat re-derives about how the operator works · tasks/603-an-operator-interface-capability-file-the-facts.md
- [#619] [P2][M] The FM-2 to FM-4 funnel-health coupling is dead — six fields, zero overlap · tasks/619-the-fm-2-to-fm-4-funnel-health-coupling-is-dead.md
- [#641] [P3][S] Declare a MEMORY.md byte budget, or rule that none is owed · tasks/641-declare-a-memory-md-byte-budget-or-rule-that-none.md

---
- [#662] [P2][S] The R6 handoff-exception rule reached none of the three carriers it was written for · tasks/662-the-r6-handoff-exception-reached-none-of-its-three-carriers.md
- [#663] [P2][M] The v7.1 boot carries no interface block and no floor item 7, and the bundle is over its own ceiling · tasks/663-the-v71-boot-carries-no-interface-block-and-no-floor-item-7.md

## [E2] Enforced governance
> As the operator, I want load-bearing conventions enforced by tools, not memory, so they can't silently drift.

### [S3] Turn advisory guards into enforced gates
So that a convention can't be skipped under load (the failure mode behind real aborts).
- [#146] [P3][S] De-hardcode-first doctrine + sweep · tasks/146-de-hardcode-first-doctrine-sweep.md
- [#112] [P2][M] adr_amend helper + ADR immutable-zone extension · tasks/112-adr-amend-helper-adr-immutable-zone-extension.md
- [#242] [P2][M] ADR status-flip coherence check · tasks/242-adr-status-flip-coherence-check.md
- [#153] [P2][M] Enforcement-completeness pass · DEFER · tasks/153-enforcement-completeness-pass.md
- [#345] [P2][M] Externalize the ADR-101 frozensets → machine-readable path-pattern registry + generalize `validate_hermetization.py` · tasks/345-externalize-the-adr-101-frozensets-machine-reada.md
- [#185] [P2][M] GAP-2 deterministic gotcha-injection guard · tasks/185-gap-2-deterministic-gotcha-injection-guard.md
- [#188] [P3][M] Deny-rule + hook completeness audit · DEFER · tasks/188-deny-rule-hook-completeness-audit.md
- [#485] [P3][S] A shared LF-enforcing write helper — the mechanism that replaces the CRLF gotcha · tasks/485-lf-enforcing-write-helper-replaces-a-gotcha.md
- [#518] [P2][S] `scripts/audit.py::_git` — one call site, two REPRODUCED defects, filed as one row because they are one fix. · tasks/518-audit-py-git-runs-unscrubbed-and-undecoded-at-one.md
- [#389] [P2][S] Prompt-lint — gate the five architect fields before a lane runs · tasks/389-prompt-lint-gate-the-five-architect-fields-befor.md
- [#401] [P2][S] ai-council routing still ARMED at the deleted hub landing zone · tasks/401-ai-council-routing-still-armed-at-the-deleted-hu.md
- [#451] [P2][M] CA layer-edge check — port the ai-council layer-edge review as the missing Layer-2 organ · tasks/451-ca-layer-edge-check-ai-council-precedent.md
- [#499] [P3][M] Promote the review-artifact coverage leg to a hard pre-push gate · DEFER · tasks/499-promote-the-review-artifact-coverage-leg-from-ad.md
- [#560] [P2][S] `review_artifact_coverage` reads only the FIRST branch/HEAD triple per file, and one title literal, so a real review can be invisible to it · tasks/560-review-artifact-coverage-reads-only-the-first-br.md
- [#573] [P3][S] lychee as a zero-baseline markdown-link gate on the actionable corpus · tasks/573-lychee-zero-baseline-md-link-gate.md

- [#510] [P2][M] Scope the R-1 exemption to the lanes its manifest enumerates — self-grantable by branch naming today · tasks/510-scope-r1-exemption-to-enumerated-lanes.md
- [#514] [P1][M] Two rival `LANE_BRANCH_RE` constants ship in one repo · tasks/514-two-rival-lane-branch-re-constants-reconcile-them.md
- [#531] [P2][S] Lane-grammar enforcement at PROVISIONING — the enum is checkable but nothing checks it · tasks/531-lane-grammar-enforcement-at-provisioning-the-enu.md
- [#533] [P2][M] Decompose the `audit.py` check monolith into `scripts/audit_checks/` — one module per check plus an ordered registry · tasks/533-decompose-the-audit-py-check-monolith-into-scrip.md
- [#534] [P2][S] `scripts/audit.py:<line>` locators on four open rows died at the `[#533]` decomposition · tasks/534-audit-py-line-locators-on-four-open-rows-died-at-t.md
- [#552] [P2][M] Window-close disposition + archival routine — every new audit gets a disposition, every terminal ADR/intake is archived · tasks/552-window-close-disposition-and-archival-routine.md
- [#579] [P1][L] Code doctrine & FDD — one ADR merging intakes #31 and #34 (packet ARC-A) · tasks/579-code-doctrine-fdd-one-adr-merging-intakes-31-and.md
- [#583] [P2][M] Green-by-skip sweep — a check that cannot obtain ground truth must not report OK (packet ARC-E, C18) · tasks/583-green-by-skip-sweep-a-check-that-cannot-obtain-g.md
- [#591] [P2][M] Substrate validator, layer 2 — REFUSE a contract whose substrate contradicts its own content · tasks/591-substrate-validator-layer-2-refuse-a-contract-wh.md
- [#592] [P2][S] Dispatch drift organ — every literal command in Ch8 must resolve on the machine · tasks/592-dispatch-drift-organ-every-literal-command-in-ch.md
- [#595] [P2][M] Consumer-at-landing gate for `docs/audits/` — the subtraction mechanism · tasks/595-consumer-at-landing-gate-for-docs-audits-the-sub.md
- [#596] [P3][S] Family-3 at the PROOF layer — the class `[#583]` names but does not prove · tasks/596-family-3-at-the-proof-layer-the-class-583-names.md
- [#601] [P2][S] `supplement_folded` audit check — a filled supplement that never reached the paste · tasks/601-supplement-folded-audit-check-a-filled-supplemen.md
- [#613] [P2][M] In-repo routing table + L0 agreement check · tasks/613-in-repo-routing-table-agreement-check.md
- [#615] [P2][M] MODEL ATTRIBUTION — a model+version signature trailer on every model-authored commit · tasks/615-model-attribution-signature-trailer-on-every.md
- [#624] [P2][M] Nothing watches a BLOCKER's status — a fold target went deferred and no organ noticed · tasks/624-nothing-watches-a-blockers-status.md
- [#629] [P1][M] An amendment cannot SUBTRACT an act — split rulings REISSUE (predicate 7) · tasks/629-a-contract-amendment-cannot-subtract-an-act.md
- [#631] [P1][M] A freeze cannot bind a rule that post-dates it — and nothing re-validates a frozen batch when the rules change · tasks/631-a-freeze-cannot-bind-a-rule-that-postdates-it.md
- [#639] [P3][S] Retire the verification organs that fire but never block - by measurement, not by feel · tasks/639-retire-the-verification-organs-that-fire-but-never-.md
- [#648] [P2][M] Two of R-6's six under-mechanised rules are still prose: locator staleness and dispatcher liveness gate nothing · tasks/648-locator-staleness-and-dispatcher-liveness-gate-nothing.md
- [#649] [P2][S] The reviewer tally carries one HIGH number where the ruling requires three · tasks/649-reviewer-tally-carries-one-number-where-three-are-owed.md
- [#651] [P2][S] The two ADR-85 organs each hold their own copy of the branch enum · tasks/651-two-adr-85-organs-each-hold-their-own-branch-enum.md
- [#652] [P2][S] A gate that passes when its precondition is ABSENT is the empty-rows shape, and the receipt check has it · tasks/652-a-gate-that-passes-when-its-precondition-is-absent.md
- [#664] [P1][L] Wire FPG-1 as the delivery spine — three commit-tier queries, and organs become views · tasks/664-wire-fpg-1-as-the-delivery-spine-three-commit-tier.md
- [#665] [P1][M] Step A — the chapter map of PLAYBOOK and ARCHITECTURE, without which step B's sitting cannot happen · tasks/665-step-a-the-chapter-map-of-playbook-and-architect.md
- [#666] [P1][S] Step B — the operator rules keep, merge or cut per chapter: one sitting, one file · tasks/666-step-b-the-operator-rules-keep-merge-or-cut-per.md
- [#667] [P1][L] Step D — the docs rewrite: ARCHITECTURE rendered, PLAYBOOK by chapter, DISPATCH split out, ESSENTIALS gone · tasks/667-step-d-the-docs-rewrite-architecture-rendered-pl.md
- [#668] [P2][M] Step E — the paste test becomes a scored eval, or the whole recovery plan is graded by vibe · tasks/668-step-e-the-paste-test-becomes-a-scored-eval-or-t.md
- [#669] [P1][L] Step F — the conductor: the delivery loop's transitions become a state machine over rows · tasks/669-step-f-the-conductor-the-delivery-loop-s-transit.md
- [#670] [P1][M] Step G — floor v1.5.0 reaches corp-monorepo, and the only thing stopping it is an unmade decision · tasks/670-step-g-floor-v1-5-0-reaches-corp-monorepo-and-th.md
- [#671] [P2][S] A lane branch carrying NO reviewer tally at all is refused by nothing at merge tier · tasks/671-a-lane-branch-carrying-no-reviewer-tally-at-all.md
- [#672] [P2][M] `lane-contract-check` cannot express an incremental contract addition, and its docstring disagrees with its YAML · tasks/672-lane-contract-check-cannot-express-an-incrementa.md
- [#676] [P2][M] No check verifies that each provider CLI's non-interactive invocation shape still works, so a mis-invoked tool is indistinguishable from a dead one · tasks/676-no-check-verifies-a-provider-cli-s-non-interactive.md
- [#677] [P2][M] The `gpt-6-astra` XL-class rule is doctrine at L0 with no gate, and exactly ONE codex call site pins a model · tasks/677-the-gpt-6-astra-xl-class-rule-is-doctrine-at-l0.md
- [#678] [P2][M] The memory index is rolled by a seat's judgment, not by a rule, and the directory it lives in has no undo · tasks/678-the-memory-index-is-rolled-by-a-seat-s-judgment.md
- [#679] [P2][S] An architect ruling that answers a `QUESTION-*.md` does not write the `disposition:` back onto the file that asked, so the ruling is given and not landed · tasks/679-an-architect-ruling-that-answers-a-question-file.md
- [#680] [P2][S] The handoff generator emits six bundle files from templates that name no owning row, so `[#664]` clause 2 refuses the commit of every architect cut · tasks/680-the-handoff-generator-emits-files-no-open-row-can.md
- [#681] [P2][S] `protocols/OPERATOR-INTERFACE.md` documents a paste sentinel and a model-switch line the live organs no longer emit, so the file is present, cited, and wrong on both · tasks/681-operator-interface-documents-a-form-the-live-organs-no-longer-emit.md
- [#682] [P2][S] Nothing tells the operator which session a paste belongs to, so a correct paste delivered to the wrong seat is indistinguishable from a correct act · tasks/682-nothing-tells-the-operator-which-session-a-paste-belongs-to.md
- [#685] [P2][M] The operator GO leaves no artifact, so the authorization a lane runs under cannot be read back from the tree · tasks/685-the-operator-go-leaves-no-artifact.md
- [#686] [P2][M] Three handoff-gate predicates measure the wrong property — carrier existence, file bytes, and an over-globbed population · tasks/686-three-gate-predicates-measure-the-wrong-property.md
- [#687] [P2][M] A task carries no execution position, and the row that would compute one from the spine is not required to · tasks/687-a-task-carries-no-execution-position-and-the-spine-does-not-yet-supply-one.md
- [#689] [P1][L] Conductor E is decided and unbuilt — GitHub Actions as the runner, state stays in tasks/, required checks as gates · tasks/689-conductor-e-is-decided-and-unbuilt.md
- [#691] [P2][M] Provider routing is an unordered role set with no admission gate and no licence field — a role needs an ORDERED fallback list only admitted providers may enter · tasks/691-provider-routing-is-an-unordered-role-set-with-no-admission-gate.md
- [#721] [P2][S] `decision_coverage` does not count STANDING_RULINGS entries, so a ruling with no mechanism row is the one decision class the query cannot see · tasks/721-decision-coverage-counts-standing-rulings-entries-as-decisions.md
- [#735] [P1][M] Floor declaration is mandatory — a new organ, hook, gate, doc or command carrying no `floor: MUST | hub-only` is refused at commit · tasks/735-floor-declaration-is-mandatory-a-new-component-without-one-is-refused.md
- [#698] [P2][S] The SEAT-BOOT-integrator render emits a GO line per merge where the canon it implements grants ONE GO for the batch · tasks/698-seat-boot-integrator-render-emits-a-go-per-merge-where-canon-grants-one-per-batch.md
- [#699] [P2][S] Three tally grammars coexist and two collide on a substring, so which one a first-match reader resolves is decided by ordering rather than by meaning · tasks/699-three-tally-grammars-coexist-and-two-collide-on-a-substring.md
- [#715] [P1][L] Path management has no single declaration -- three governed-path mismatches in one day, and the registry the operator is describing already exists as FPG-1 · tasks/715-path-management-has-no-single-declaration-and-fpg1-is-already-the-registry.md
- [#726] [P1][S] A session whose worktree was torn down silently resolves to the PRIMARY checkout, so its next write lands on the integrator's branch · tasks/726-torn-down-worktree-session-silently-resolves-to-the-primary-checkout.md
- [#742] [P1][S] `actions_verdict` reports PASS when the job details cannot be read, so an unreadable run is indistinguishable from a clean one · tasks/742-actions-verdict-reports-pass-when-job-details-cannot-be-read.md
- [#743] [P1][S] The step-0 collision extractor requires a slash, so two lanes may both declare a root-level file and pass · tasks/743-collision-extractor-is-blind-to-root-level-files.md
- [#744] [P1][S] `median_report` filters receipts by kind but never by completeness, so the under-30 target can be met on incomplete receipts · tasks/744-median-report-counts-incomplete-receipts.md
- [#747] [P1][M] Adoption-by-invocation — a command file confers adoption only while telemetry records real invocations, and it decays at 30 days · tasks/747-adoption-by-invocation-command-file-confers-adoption-only-while-invoked.md
- [#748] [P1][M] A lane whose worktree resolves to the primary checkout via a `core.worktree` redirect has no isolation, and dispatch cannot see it · tasks/748-a-lane-whose-worktree-redirects-to-the-primary-has-no-isolation.md
- [#749] [P1][M] Two lanes may be dispatched for the same row under different slugs, because every duplicate check compares slugs rather than rows · tasks/749-two-lanes-may-be-dispatched-for-the-same-row-under-different-slugs.md
- [#750] [P1][M] A merge can land with no receipt, the completeness predicate flattens a verdict state machine into a boolean, and `wall_seconds` records serial time rather than the arc span · tasks/750-a-merge-can-land-with-no-receipt-the-completenes.md
- [#752] [P1][M] A contract's declared model and mode reach no flag the background launcher honours, and nothing reads what a lane actually ran · tasks/752-a-contracts-declared-model-and-mode-reach-no-fla.md
- [#758] [P2][S] `[#675]` target 3.2 has never been satisfiable by the `lane-integrate` walk · tasks/758-675-target-32-has-never-been-satisfiable-by-the-w.md
- [#759] [P2][S] `range_is_anchored` and `unanchored_on_spine` disagree on scope, and the 2026-09-14 instance fix does not close the class · tasks/759-range-is-anchored-and-unanchored-on-spine-disagree.md
- [#761] [P2][S] The edge-class census prices its own false positive as cheap, but paying it is an escalation class, so lanes route around the gate instead · tasks/761-the-edge-class-census-prices-its-own-false-positive.md
- [#762] [P2][S] A worktree teardown races the departing session's Stop hook, which re-creates the tree being removed — and the no-leftovers check cannot see what it leaves · tasks/762-a-worktree-teardown-races-the-departing-sessions-stop-hook.md
- [#763] [P1][S] Re-measure the batch-Z suite baseline freeze at batch close — a cause whose lane merged must have left the set · tasks/763-re-measure-the-batch-z-suite-baseline-freeze-at.md
- [#764] [P1][S] Batch Z implements the night plan of 2026-09-15 — the four transport decisions the engine refused every commit for · tasks/764-batch-z-implements-the-night-plan-of-2026-09-15.md
- [#782] [P1][M] The quality-requirements register: non-functional requirements as a registered, enforced, rendered artifact · tasks/782-the-quality-requirements-register-non-functional-requirements-as-a-registered-enforced-artifact.md
- [#783] [P2][S] The carried-to-RESOLVED leg of decision-coverage has never once been exercised · tasks/783-the-carried-to-resolved-leg-of-decision-coverage-has-never-been-exercised.md
### [S4] Extend structural validation to more governance artifacts
So that drift in transcripts, ADRs, and folders is caught cheaply, not by reviewer luck.
- [#139] [P2][L] merged-arc→record verifier · DEFER · tasks/139-merged-arc-record-verifier.md
- [#190] [P3][M] General intra-file duplication detector · DEFER · tasks/190-general-intra-file-duplication-detector.md
- [#210] [P3][S] Convert journal-wrap no-ff WARNs from per-instance disposition to a standing rule · tasks/210-convert-journal-wrap-no-ff-warns-from-per-instan.md
- [#234] [P3][S] Cross-repo probe validator · DEFER · tasks/234-cross-repo-probe-validator.md
- [#277] [P2][M] propose_closures signal repair · tasks/277-propose-closures-signal-repair.md
- [#693] [P1][M] The closure detector proposes the whole queue, its surfacing hook has been dead since the month-bucket move, and the run cap errors -- three defects that together make a closure proposal mean nothing · tasks/693-closure-detector-proposes-the-whole-queue-with-a-dead-surfacing-hook.md
- [#719] [P2][M] `ecosystem/organ-index` entries answer to no schema -- validate them against Backstage `catalog-model`'s Component shape with our own gate · tasks/719-organ-index-entries-answer-to-no-schema-validate-against-catalog-model.md

### [S5] Catch spec/dependent drift mechanically, not by memory
So that "spec bumped, dependent partially updated, caught only because a human remembered" stops being the failure mode — machine-checkable coherence between a dependent doc and its spec.
- [#169] [P3][M] Ungated-doc staleness detection · DEFER · tasks/169-ungated-doc-staleness-detection.md
- [#171] [P3][M] Build the conformance dashboard at `ecosystem/conformance.md` · tasks/171-build-the-conformance-dashboard-at-ecosystem-con.md
- [#166] [P3][M] doctrine_enforcement_coherence check · DEFER · tasks/166-doctrine-enforcement-coherence-check.md
- [#181] [P2][S] Coherence v2 nudge-response · DEFER · tasks/181-coherence-v2-nudge-response.md
- [#220] [P2][M] MODIFY / semantic-drift axis · DEFER · tasks/220-modify-semantic-drift-axis.md
- [#241] [P2][S] Undeclared-edge groom · tasks/241-undeclared-edge-groom.md
- [#457] [P2][S] Two live-repo tests fail on main against green gates — test-vs-organ mismatch · tasks/457-inherited-live-repo-test-failures.md
- [#477] [P2][S] `deployed_methodology_version` keys the registry by repo-root BASENAME — a clone named `dev-knowledge` cannot find `.dev-knowledge` · tasks/477-deployed-version-check-keys-registry-by-basename.md
- [#478] [P2][S] `changelog_sentinel` drops PEP 440 suffixes — a prerelease as the reviewed value silences the sentinel permanently · tasks/478-changelog-sentinel-drops-pep-440-suffixes.md
- [#653] [P2][S] The fleet-shape spec changed what a consumer owes and its `spec_version` did not move · tasks/653-fleet-shape-spec-version-unbumped-after-a-consumer-change.md
- [#654] [P2][M] The 037 render-pass ruling has no intake file, so `reconciled_with` stays hand-typed · tasks/654-the-037-render-pass-ruling-has-no-intake-and-no-carrier.md

### [S6] Know what depends on code before removing it (ADR-89 computed edges)
So that a symbol deletion can't silently break a dependent — the code analog of catching doc/spec drift.
- [#218] [P1][M] Safe-removal gate M2+M3 boundary · DEFER · tasks/218-safe-removal-gate-m2-m3-boundary.md
- [#659] [P2][S] The `orphan_census` intake names two triggers and one of them does not exist · tasks/659-orphan-census-names-a-trigger-that-does-not-exist.md
- [#674] [P2][M] `[#563]`'s no-reader test checks a NAME to prove a RELATIONSHIP; it must assert the absence of a `reads` edge · tasks/674-563-s-no-reader-test-checks-a-name-to-prove-a-rela.md
- [#675] [P2][M] Manifest tooling reads a heterogeneous node list with a bare `.get` default, so every node of the other shape reads as the default · tasks/675-manifest-tooling-reads-a-heterogeneous-node-list.md

### [S7] Wire up the lifecycle hooks the workflow relies on
So that session-start/close automation actually runs instead of being wired-but-vacuous.
- [#116] [P3][S] Hooks hygiene · DEFER · tasks/116-hooks-hygiene.md
- [#117] [P3][S] Evaluate prompt/agent-based hooks · DEFER · tasks/117-evaluate-prompt-agent-based-hooks.md
- [#170] [P3][M] Design + land the traceability-spine ADR · tasks/170-design-land-the-traceability-spine-adr.md
- [#189] [P3][S] Execute in ~/.claude · DEFER · tasks/189-execute-in-claude.md
- [#310] [P3][S] Define the cold-bundle annotation surface + annotate the 07-05 bundle as-cold · DEFER · tasks/310-define-the-cold-bundle-annotation-surface-annota.md
- [#520] [P2][S] No sanctioned way to retire a committed bundle whose seal is wrong · tasks/520-no-sanctioned-way-to-retire-a-committed-bundle-w.md
- [#405] [P2][S] Session-end leftover check — nothing verifies "no leftovers" · tasks/405-session-end-leftover-check-nothing-verifies-no-l.md
- [#418] [P2][S] `automation/fleet-audit` records 0–10 baselines a day, not one · tasks/418-automation-fleet-audit-records-0-10-baselines-a.md
- [#414] [P2][S] Self-acting-on-main incident family — a session changed `main` with no operator GO and no anchored action (n=2 this week) · tasks/414-self-acting-on-main-incident-family-a-session-ch.md
- [#442] [P2][M] Plugin command-cache staleness — cached command text can silently outlive a workflow change · tasks/442-plugin-command-cache-staleness-cached-command-te.md
- [#454] [P2][S] `closure_ids` negation defect — the parser reads a negated closure mention as a closure · tasks/454-closure-ids-negation-defect-negated-mention-reads.md
- [#500] [P3][S] The Stop hook's BACKLOG advisory reads a correctly-closed task as "nothing closed" · tasks/500-the-stop-hook-s-backlog-advisory-reads-a-correct.md
- [#519] [P1][M] The close path is two edits, and nothing makes a half-done close visible · tasks/519-the-close-path-is-two-edits-and-nothing-makes-a.md
- [#522] [P2][M] A re-cut handoff sibling carries its predecessor's payloads — the thinner-refill hole · tasks/522-re-cut-bundle-carries-predecessor-payloads.md
- [#730] [P1][M] Work lands on main and its row stays open, because nobody hands the operator closures in bulk -- the close packet lists what the merges witnessed · tasks/730-evidenced-bulk-closure-at-every-batch-close-one-operator-word.md

### [S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)
So that "held by mechanism, not memory" is true for every consumer, not only the hub — the deploy subsystem (ADR-91/92) carries the PRESENCE of the methodology to consumers but NOT its ENFORCEMENT: five hub organs (session_end_backpressure, canonical_freshness, doc_claims, git_backlog_drift, the coherence spine) are hub-only, so the founding standard is TRUE for the hub and FALSE for every consumer (proof: ai-council shipped 3 epics with JOURNAL ~1mo stale, unblocked). This epic closes that gap, stage-ordered.

Backbone (dependency-ordered; done stages recorded here as the epic ledger — ADR-65: git is the implementation record, so the DONE stages are narrative, not live task lines):
- Stage 0 — stabilize live (ship-gate GREEN + clean tree). [DONE]
- Stage 1 — fleet blast-radius map (5 organs x 4 consumers classified from live config). [DONE]
- Stage 2 [#235] — Informant Organ: the read-only enforcement-coverage reporter that measures enforcement-in-effect (whether the gate FIRES, not presence — proven by the present-inert->absent / blocking->enforcing-local fixture pair; first live run reproduces the differentiated fleet map, 0 enforcing-local; no organ modified). [DONE 2026-07-03, feat/informant-organ, commits 99401d7/03a3280/07a061a — closed against #235]
- Stage 3 [#236 + sub-item #237] — the mesh carrier (the enforcement-transfer mechanism). Stage 4 [#238] — record + formalize. Follow-ups: Tier-2 breadth #239, audit-leg regression teeth #240. Sequenced-after (off the critical path): fleet rollout n=2+ (#221), each repo gated on the Informant's enforcing-local — only after Stage 3 is proven on n=1.
- FLAG RESOLVED (architect, 2026-07-07): the arc-tracking / record-integrity fold is adjudicated — #168/#170 **co-sequence with #239/#240** (they harden the same `session_end_backpressure` organ the enforcement-transfer epic ports consumer-local in #237); #243 co-sequences there too (its #168-hard vs Fable-WARN conflict resolves at that mesh-consult). #139 **stays separate** (hub record-integrity, tangential — not folded).

- [#240] [P3][S] Follow-up · DEFER · tasks/240-follow-up.md
- [#267] [P2][S] Scope-exercising arc extension · tasks/267-scope-exercising-arc-extension.md
- [#289] [P2][M] Hub-own the OneDrive-Blue-Yonder guard · DEFER · tasks/289-hub-own-the-onedrive-blue-yonder-guard.md
- [#294] [P3][M] `validate_backlog` deploy-carrier + `--path` de-hardcode · DEFER · tasks/294-validate-backlog-deploy-carrier-path-de-hardcode.md
- [#297] [P3][S] Lightweight/dry `observe-arc` coverage mode · DEFER · tasks/297-lightweight-dry-observe-arc-coverage-mode.md
- [#303] [P2][S] Make seed_runbook.py child-class-aware · DEFER · tasks/303-make-seed-runbook-py-child-class-aware.md
- [#305] [P3][S] Add a verify-only / already-onboarded re-run mode to the onboarding runbook · DEFER · tasks/305-add-a-verify-only-already-onboarded-re-run-mode.md
- [#308] [P3][S] Decide the `verify` skill's canonical home · DEFER · tasks/308-decide-the-verify-skill-s-canonical-home.md
- [#324] [P3][M] Phase-6 axis-2 carrier · DEFER · tasks/324-phase-6-axis-2-carrier.md
- [#325] [P3][S] Carry `/save` to consumers via a manifest command-artifact carrier · DEFER · tasks/325-carry-save-to-consumers-via-a-manifest-command-a.md
- [#497] [P3][S] Two stale claims on carrier/hook declarations · tasks/497-carrier-mesh-py-75-still-claims-the-informant-lo.md
- [#496] [P3][S] `_ORGAN_TO_COMPONENT` attributes the pre-push organ to a component that does not carry it — the Tier-3 DRIFT rows it produces are misfiled · tasks/496-organ-to-component-attributes-the-pre-push-organ.md
- [#605] [P2][M] De-hardcode consumer-root resolution in `deploy/tool.py` and `scripts/audit.py` · tasks/605-de-hardcode-consumer-root-resolution-in-deploy-t.md
---
- [#656] [P2][S] The v1.5.0 carrier's `floor-seal-report` drift probe matches a literal the command no longer has · tasks/656-v150-floor-seal-report-drift-probe-matches-a-dead-literal.md
- [#741] [P1][M] Lane launching is methodology, so the hub owns it — a floor component shipped to every consumer, OS-independent, with machine-local values staying in win-tooling · tasks/741-lane-launching-is-methodology-so-the-hub-owns-it-as-a-floor-component.md

## [E3] Lessons feedback loop
> As the methodology author, I want lessons to flow back into enforced rules, not sit in an archive.

### [S9] Make lessons an active feedback loop, not a passive archive
So that captured lessons reach runtime rules and stay enforceable.
- [#4] [P2][M] Build lessons-index.json + SessionStart retrieval + CLI query · DEFER · tasks/4-build-lessons-index-json-sessionstart-retrieval.md
- [#130] [P3][S] Memory-hygiene review · tasks/130-memory-hygiene-review.md

### [S10] Codify recurring patterns into the methodology
So that observed failure-modes become written guidance instead of recurring.
- [#144] [P3][M] Feature DoD = end-to-end / user-flow test · DEFER · tasks/144-feature-dod-end-to-end-user-flow-test.md
- [#145] [P3][M] Codification-completeness pass · tasks/145-codification-completeness-pass.md
- [#438] [P3][S] Codify gate-class posture: terra design review BEFORE build for refusal-gate arcs · tasks/438-codify-gate-class-posture-terra-design-review-be.md

---

- [#538] [P2][M] The NB4-C PLAYBOOK gap arc — twelve paste-ready acts, none landed · tasks/538-the-nb4-c-playbook-gap-arc-twelve-paste-ready-acts.md
## [E4] Decision management
> As a reader of 65+ ADRs, I want decisions navigable and free of silent contradiction.

### [S11] Keep the decision corpus navigable and contradiction-aware
So that growth past 65 ADRs doesn't bury or quietly contradict prior decisions.
- [#23] [P3][S] Validate ADR frontmatter relation-fields · DEFER · tasks/23-validate-adr-frontmatter-relation-fields.md
- [#546] [P3][S] ADR-60's `docs/` taxonomy no longer describes the tree it governs · tasks/546-adr-60-docs-taxonomy-no-longer-describes-the-tree.md
- [#548] [P2][S] Intake #12's SETTLED ownership manifest is parked on a departed id, and three live rows depend on it by name · tasks/548-intake-12-settled-ownership-manifest-has-no-carrier.md
- [#549] [P2][S] The operator-approved Fleet-Hygiene plan-of-record (intake #13 v4) has no carrier · DEFER · tasks/549-fleet-hygiene-plan-of-record-has-no-carrier.md
- [#550] [P3][S] Intake #14's ruled SIEM requirements outlived the ruling that shelved them, with no record of which half survives · tasks/550-intake-14-ruled-siem-requirements-half-dispositioned.md
- [#564] [P2][M] Lifecycle archival — a pass over implemented ADRs and decided intakes, plus a check so archival cannot silently lag · tasks/564-lifecycle-archival-implemented-adrs-and-decided-int.md
- [#572] [P2][M] Intake-funnel completion — #34 flip, #35–#37 transitions post-R7, funnel hygiene · tasks/572-intake-funnel-completion-carrier.md
- [#616] [P2][S] FLIP-CONDITION — every ADR records what evidence would reverse it · tasks/616-flip-condition-every-adr-records-what-evidence-w.md
- [#637] [P2][M] Nineteen landed audit artifacts carry PROPOSALS that no governance surface has ruled · tasks/637-nineteen-landed-audit-artifacts-carry-proposals-tha.md
- [#640] [P1][S] The FPG-1 scope narrowing is recorded nowhere, and two landed surfaces still carry the superseded version · tasks/640-the-fpg-1-scope-narrowing-is-recorded-nowhere-and-t.md
- [#642] [P1][S] The eleven carried questions from batches T and U have no owning row, so their debt is silent · tasks/642-eleven-carried-questions-have-no-owning-row.md
- [#695] [P2][M] Intake #70 (AJ second pass) is ACCEPTED with zero rows -- its operator practices were extracted and never became work · tasks/695-intake-70-aj-second-pass-is-accepted-with-zero-rows.md
- [#700] [P2][S] AW5-4 ruled that machine-read control surfaces are STATE rather than narrative, and the ruling reached the close packet and none of the surfaces that state amendment discipline · tasks/700-aw54-control-surfaces-are-state-ruling-reached-no-enforcing-surface.md

### [S12] Close the small ADR cross-reference + registry amendments
So that the ADR web is internally consistent.
- [#19] [P3][M] Complete the ADR-39 register · DEFER · tasks/19-complete-the-adr-39-register.md

---
- [#650] [P2][S] ADR-117 sits at `Proposed` while a gate already enforces it · tasks/650-adr-117-is-proposed-while-a-gate-enforces-it.md

## [E5] Canonical-file integrity
> As any agent reading this repo, I want the canonical files accurate and current.

### [S13] Keep canonical files accurate
So that stale ground truth stops silently misleading sessions (the repo's own VISION is "drift detected proactively").
- [#285] [P3][S] Extend hub freshness gating to PLAYBOOK · DEFER · tasks/285-extend-hub-freshness-gating-to-playbook.md
- [#300] [P1][M] Hermetization residual d.ii · DEFER · tasks/300-hermetization-residual-d-ii.md
- [#388] [P3][S] The "10–20 repo" fleet-scale target is FABRICATED — correct it to the live 5–8+ wherever it is restated · tasks/388-the-10-20-repo-fleet-scale-target-is-fabricated.md
- [#526] [P3][S] Root-hygiene audit — which root files MUST be root, which are movable · tasks/526-root-hygiene-audit-which-root-files-must-be-root.md

- [#571] [P2][M] Define "architecture-described surface" + the architecture-freshness check (intake #33 A1) · tasks/571-define-architecture-described-surface.md
- [#542] [P3][S] `ARCHITECTURE.md` still claims four `doc_rot` sub-detectors; there are five · tasks/542-architecture-md-still-claims-four-doc-rot-sub-dete.md
- [#585] [P2][S] Suite RED — `test_anchor_gate_probe_distinguishes_installed_from_absent` does not discriminate: repair it, retire it, or fix the organ · tasks/585-suite-red-test-anchor-gate-probe-distinguishes-i.md
- [#707] [P1][S] W-4 closed under a declared organ-index bypass with four repairs owed -- the committed index is one row stale against its own generator · tasks/707-w4-close-residue-organ-index-one-row-stale-under-a-declared-bypass.md
### [S14] Keep the day-to-day docs right-sized and current
So that the cheat-sheet and architecture stay scannable as conventions accrue.
- [#269] [P3][S] Audit-index count-tiered shape + freshness hook · DEFER · tasks/269-audit-index-count-tiered-shape-freshness-hook.md
- [#420] [P3][S] Does a TOP-LEVEL `docs/archive/` still make sense? · tasks/420-does-a-top-level-docs-archive-still-make-sense.md
- [#227] [P3][S] Relocate AGENT_FRAMEWORK.md out of protocols/ · DEFER · tasks/227-relocate-agent-framework-md-out-of-protocols.md

- [#506] [P2][M] Whole-set P10 grooming arc — the open set is unreconciled · tasks/506-whole-set-p10-grooming-arc-full-open-set.md
- [#551] [P2][S] Audit artifacts carry no `status:`, so a consumed audit is indistinguishable from a live one · tasks/551-audit-artifacts-carry-no-status-field.md
- [#553] [P3][S] `docs/decisions/README.md`'s ADR census is hand-maintained, ungated, and currently wrong in two places · tasks/553-adr-census-in-decisions-readme-is-ungated-and-wrong.md
- [#620] [P2][M] Retire the root-README prohibition across the fleet, not only at the hub · tasks/620-retire-the-root-readme-prohibition-across-the-fl.md
- [#621] [P2][L] ADR-114 option (C): the nine-repo VISION.md to README.md filename migration · tasks/621-adr-114-option-c-the-nine-repo-vision-md-to-read.md
- [#622] [P3][M] Promote README.md into the ADR-38 canonical mandatory set · tasks/622-promote-readme-md-into-the-adr-38-canonical-mand.md
---

- [#589] [P1][M] One line per row — the BACKLOG view projection, with a size assertion that cannot be silently undone · tasks/589-one-line-per-row-the-backlog-view-projection-wit.md
- [#590] [P2][S] The audits index is regenerated on read, never merge-resolved · tasks/590-the-audits-index-is-regenerated-on-read-never-me.md
- [#607] [P2][S] PLAYBOOK census discharge — the mechanical half of the 19 findings · tasks/607-playbook-census-discharge-the-mechanical-half-of.md
- [#617] [P2][M] FILE DISTILLATION — the output half, and the only worsening series · tasks/617-file-distillation-the-output-half-and-the-only-w.md
- [#612] [P2][M] Doc-rot row-body archival mechanism · tasks/612-doc-rot-row-body-archival.md
- [#628] [P1][L] DC-2 re-cut — dissolving `ESSENTIALS.md` is a FLEET-COUPLED release act, not a doc lane · tasks/628-dc2-recut-essentials-dissolution-is-a-release-act.md
- [#755] [P1][M] Finish the docs cut — `ARCHITECTURE.md` to ≤ 15 KB behind the X3 render, and the four ESSENTIALS residues the dissolution could not reach · tasks/755-finish-the-docs-cut-architecture-to-15-kb-and-t.md
- [#757] [P1][S] Reconcile the ratified anchor topology with B2, P-1 and the `DEFINITION_OF_DONE` wording · tasks/757-reconcile-the-ratified-anchor-topology-with-b2-p1.md
- [#760] [P1][L] X3 — `ARCHITECTURE.md` to <= 15 KB behind the step-D render, starting from the measured eleven chapters · tasks/760-x3-architecture-to-15-kb-behind-the-step-d-render.md
- [#647] [P3][M] The harness's own carrying cost is unmeasured, and lane contracts are pasted rather than referenced · tasks/647-harness-carrying-cost-unmeasured-contracts-pasted.md
- [#731] [P1][M] The backlog only grows -- narration is relocated by hand and nothing stops a batch filing more rows than it closes · tasks/731-backlog-shrinks-by-mechanism-relocation-trigger-and-an-enforced-closure-budget.md
- [#754] [P2][S] The two backlog row ceilings measure different corpora, and the source-side one has decayed back into the percentile its own amendment abolished · tasks/754-the-two-backlog-row-ceilings-measure-different-corpora.md
- [#781] [P2][M] One management map rendered from the organ index, with trigger-less organs rendered DEAD · tasks/781-one-management-map-rendered-from-the-organ-index-with-trigger-less-organs-rendered-dead.md
## [E6] Cross-repo universalization
> As the disseminator, I want every child repo to converge on the universal baseline.

### [S15] Converge every child repo on the universal baseline
So that "open any repo, same layout/governance" actually holds.
- [#82] [P3][M] Define per-repository agentic-review profiles · DEFER · tasks/82-define-per-repository-agentic-review-profiles.md
- [#231] [P3][M] Consumer → hub feedback report · DEFER · tasks/231-consumer-hub-feedback-report.md
- [#327] [P2][M] Protocols-as-interface genre ruling · DEFER · tasks/327-protocols-as-interface-genre-ruling.md
- [#329] [P3][S] VS Code ownership visualization · DEFER · tasks/329-vs-code-ownership-visualization.md
- [#331] [P2][S] Consumer BACKLOG schema adoption ruling · DEFER · tasks/331-consumer-backlog-schema-adoption-ruling.md
- [#332] [P2][M] Fleet dependency-version parity · DEFER · tasks/332-fleet-dependency-version-parity.md
- [#334] [P3][S] Fleet-wide ruff hook id migration `ruff` → `ruff-check` · tasks/334-fleet-wide-ruff-hook-id-migration-ruff-ruff-chec.md
- [#609] [P2][S] Free ruff ratchet — the zero-cost half of the Python standard · tasks/609-free-ruff-ratchet-the-zero-cost-python-standard.md
- [#343] [P3][S] fleet_parity ship-gate-only scoping · tasks/343-fleet-parity-ship-gate-only-scoping.md
- [#342] [P3][S] fleet_parity gate-ahead max-fidelity hardening · tasks/342-fleet-parity-gate-ahead-max-fidelity-hardening.md
- [#351] [P3][M] Fleet-Python-upgrade ticket · tasks/351-fleet-python-upgrade-ticket.md
- [#559] [P2][L] Kernel/lab check tiering + `dev-knowledge-kernel` as an installable package · tasks/559-kernel-lab-check-tiering-dev-knowledge-kernel-as.md
- [#430] [P2][M] Consumer template rejects root `conftest.py`; `fleet_parity`'s verdict depends on state outside its subject · tasks/430-consumer-template-rejects-root-conftest-py-fleet.md
- [#604] [P2][S] Admit win-tooling and terminal-setup to the deploy registry and rule their onboarding profiles · tasks/604-admit-win-tooling-and-terminal-setup-to-the-depl.md
- [#606] [P2][L] The win-tooling first-slice instantiation arc, run in the RULING-W shape · tasks/606-the-win-tooling-first-slice-instantiation-arc-ru.md
- [#644] [P1][S] The 2026-08-29 deploy freeze has never been ruled, and it blocks the universalization order's step 4 · tasks/644-the-2026-08-29-deploy-freeze-has-never-been-ruled.md

### [S16] Manage the methodology as a living thing (essence lifecycle: transfer · sync · PRUNE)
So that the consumer-facing live surface reflects CURRENT state — hub-deprecated elements get REMOVED from consumers, not accumulated (the append-only-live-surface bug; distinct from the append-only-BY-DESIGN audit trail).
- [#244] [P2][L] Essence-spec lifecycle epic · DEFER · tasks/244-essence-spec-lifecycle-epic.md
- [#245] [P2][M] Add-path status-awareness · DEFER · tasks/245-add-path-status-awareness.md
- [#690] [P2][S] The three SUPERSEDED `block-onedrive` hook copies under `~/.claude/hooks/` — removed, and the removal recorded in-repo · tasks/690-three-superseded-l0-hook-copies-removed-batch-w-w5.md
- [#734] [P1][M] Cleanup is an act, not a note -- the census's 35 non-live items each get DELETE, TRIGGER or KEEP, as one file for one operator GO · tasks/734-cleanup-is-an-act-35-non-live-census-items-get-a-proposal-each.md
- [#736] [P2][M] Component lifecycle is not data, so nothing can deprecate an organ — an item untriggered and unread for 30 days stays `production` forever · tasks/736-component-lifecycle-as-data-and-automatic-deprecation.md
- [#745] [P1][M] The domain census's 16 UNKNOWN items are resolved to a live/non-live verdict by a second pass rather than carried forward · tasks/745-the-sixteen-unknown-census-items-are-resolved-by-a-second-pass.md

### [S17] Make new-repo scaffolding correct-by-default
So that a new repo inherits the full baseline in one step, not by re-derivation.
- [#43] [P3][L] Decide + · DEFER · tasks/43-decide.md

---
- [#645] [P2][S] `INSTALL.md`'s repo-root path is retired to `docs/`, not allow-listed into the seal · tasks/645-install-md-root-path-retired-to-docs-not-allowlisted.md

## [E7] Tooling & evaluation
> As the operator, I want low-friction tooling and timely tech adoption.

### [S18] Cut session friction with better tooling
So that cognitive overhead per session drops.
- [#102] [P2][M] Machine-readable repo index for agent consumption · DEFER · tasks/102-machine-readable-repo-index-for-agent-consumptio.md
- [#273] [P3][S] Changelog-review staleness escalation · DEFER · tasks/273-changelog-review-staleness-escalation.md
- [#274] [P3][S] Dogfood-signal prior in the /changelog-review ADOPT rubric · tasks/274-dogfood-signal-prior-in-the-changelog-review-ado.md
- [#317] [P2][M] Default-parallel test invocation · DEFER · tasks/317-default-parallel-test-invocation-slow-tier-marke.md
- [#322] [P2][M] Fleet dashboard · DEFER · tasks/322-fleet-dashboard.md
- [#340] [P2][S] /ship pre-flight validator honors the consumer repo's canonical test gate · tasks/340-ship-pre-flight-validator-honors-the-consumer-re.md
- [#341] [P2][S] Codex producer-lane activation mechanism · tasks/341-codex-producer-lane-activation-mechanism.md
- [#431] [P2][S] `codex-review` silently drops the doc lane on any mixed diff · tasks/431-codex-review-silently-drops-the-doc-lane-on-any.md
- [#445] [P2][S] `codex-review` wrapper path-guard reports SUCCESS having reviewed nothing · tasks/445-codex-review-wrapper-path-guard-reports-success-h.md
- [#470] [P3][S] `audit.py checks` crashes mid-listing on a cp1252 console — one U+2192 glyph · tasks/470-audit-py-checks-crashes-on-a-cp1252-console.md
- [#403] [P3][S] Extend `doc_claims` to ARCHITECTURE's machine-derivable claims · tasks/403-extend-doc-claims-to-architecture-s-machine-deri.md
- [#487] [P2][L] Closure-proposal consumption arc — repair the pipeline first · tasks/487-closure-proposal-consumption-arc-139-parked-prop.md
- [#509] [P3][S] `Invoke-Dispatch.ps1` resolves `CLAUDE_PROMPTS_DIR` · tasks/509-invoke-dispatch-resolves-claude-prompts-dir.md
- [#528] [P1][M] Lane-latency — the full suite multiplied by per-lane + per-merge runs is the real batch cost · tasks/528-lane-latency-full-suite-multiplied-across-a-batch.md
- [#576] [P2][M] Telemetry read path — the lane `[#565]` was sequenced before · tasks/576-telemetry-read-path-lane.md
- [#575] [P2][M] Telemetry store: 98.5% of an emit, and silent drops under concurrent writers · tasks/575-telemetry-store-performance-and-silent-drops.md
- [#574] [P2][M] gen_lane_contract emits the batch manifest — Q6's own failure class, recurring · tasks/574-batch-manifest-emitted-by-gen-lane-contract.md

- [#540] [P3][S] `harvest_batch.py` — read the board, then fetch packets by `git show`, never by log-scraping · tasks/540-harvest-batch-py-read-the-board-then-fetch-packets.md
- [#554] [P2][M] Devcontainer + provisioning script (NB4-G stage 1) · tasks/554-devcontainer-provisioning-script-nb4-g-stage-1.md
- [#568] [P2][M] Provider config as code — `.dev-knowledge` as source of truth, machine-global dirs as junctions · tasks/568-provider-config-as-code-dev-knowledge-as-source-of-.md
- [#581] [P1][L] Backlog vitals — three flow instruments, a committed digest, and what-is-unblocked-now (packet ARC-C) · tasks/581-backlog-vitals-three-flow-instruments-a-committe.md
- [#582] [P1][L] Substrate router — one gated enum, a capability-keyed table, and the generator that reads it (packet ARC-D) · tasks/582-substrate-router-one-gated-enum-a-capability-key.md
- [#586] [P3][S] Suite RED — `test_no_gate_hook_or_script_reads_the_export` has no `ecosystem/` naming-vs-reading carve-out (packet ARC-G, C04) · tasks/586-suite-red-test-no-gate-hook-or-script-reads-the.md
- [#587] [P1][M] P-1 — invert the journal-anchor check to a single pass · tasks/587-p-1-invert-the-journal-anchor-check-to-a-single.md
- [#588] [P1][S] P-2 — build the spine parent-map in ONE git process · tasks/588-p-2-build-the-spine-parent-map-in-one-git-proces.md
- [#608] [P1][S] Tiling-aware journal read — the rotation seam, before any split · tasks/608-tiling-aware-journal-read-the-rotation-seam-befo.md
- [#593] [P2][M] Codespaces chain repair, hub half — uv in the image and a prebuild that actually refreshes · tasks/593-codespaces-chain-repair-hub-half-uv-in-the-image.md
- [#594] [P3][M] Layer-3 router — the HUB prerequisites only, not the verb itself · tasks/594-layer-3-router-the-hub-prerequisites-only-not-th.md
- [#597] [P2][M] P-4 — a declared tier per check, and P-3's telemetry window FIRST · tasks/597-p-4-a-declared-tier-per-check-and-p-3-s-telemetr.md
- [#598] [P3][S] P-6 — a slow-marker selector so tiered gating has something to select on · tasks/598-p-6-a-slow-marker-selector-so-tiered-gating-has.md
- [#618] [P2][M] The silently-stale codespace clone — detection and refresh-on-entry, not a rebuild · tasks/618-the-silently-stale-codespace-clone-detection-and.md
- [#623] [P2][S] Mechanize the JOURNAL anchor record-line — 719 anchored-by-mention WARNs is a signal-to-noise defect · tasks/623-mechanize-the-journal-anchor-record-line.md
- [#625] [P1][M] The rule-adherence eval corpus — a FRESH corpus, because neither fold target can carry it · tasks/625-the-rule-adherence-eval-corpus-fresh.md
- [#626] [P2][M] `logs/` does not thin — the retention rule exempts the two prefixes that actually accumulate · tasks/626-logs-retention-exempts-the-prefixes-that-accumulate.md
- [#632] [P1][L] Codespace is ADMITTED for transport and UNSTABLE for inference — the six-layer plan, the runner hardening, and the two defects they depend on · tasks/632-codespace-is-admitted-for-transport-and-unstable-for-inference.md
- [#634] [P1][S] dispatch-run.sh accepts GITHUB_TOKEN as its Anthropic-token check — a fail-open admission gate on a paid substrate · tasks/634-dispatch-run-accepts-github-token-as-the-anthropic-check.md
- [#646] [P3][S] The ceremony ratio was measured once, by hand, and nothing computes it · tasks/646-substantive-commit-share-is-measured-once-by-hand.md
- [#658] [P2][M] Fourteen operator points on the critical path, nine of them mechanisable, and nothing counts them · tasks/658-fourteen-operator-points-nine-mechanisable-nothing-counts.md
- [#694] [P1][M] Four telemetry modules are inventory rather than harness -- each gets a trigger or is deleted, and the roster allows no third state · tasks/694-four-telemetry-modules-are-inventory-each-gets-a-trigger-or-is-deleted.md
- [#697] [P1][M] A detached codespace lane returns ZERO WORK and returns it quietly -- two nights of it, and nothing decides whether the substrate is repaired or retired · tasks/697-codespace-detached-lane-returns-zero-work-and-nothing-decides-repair-or-retire.md
- [#703] [P1][S] Impacted-test selection can read an empty selection as "nothing impacted" -- the one reading that turns a selector into a silent skip · tasks/703-impacted-test-selection-empty-selection-must-fail-closed.md
- [#704] [P2][S] `propose_closures` writes a new proposals file every run, so four sessions of asking produced 154 swept files where one current file was wanted · tasks/704-propose-closures-writes-a-new-file-every-run-instead-of-one-overwritten.md
- [#705] [P2][M] Nothing renders the task flow, so "how is the batch going" is answered by reading rows · tasks/705-no-chart-renders-task-flow-so-how-is-the-batch-going-is-answered-by-reading-rows.md
- [#737] [P2][S] A SEAT-BOOT render cannot express the seat's own model, so the operator's re-tiering ruling has nowhere to live but prose the next seat never reads · tasks/737-a-seat-boot-render-cannot-express-the-seat-s-own-model.md
- [#738] [P2][S] `lane-ceiling --check-worktrees` refuses on worktree PRESENCE, so a wave-2 batch is refused by a prior wave's lane awaiting merge and the only offered remedy destroys it · tasks/738-lane-ceiling-refuses-on-worktree-presence-with-no-merged-discrimination.md
- [#739] [P2][S] `session_end_backpressure` reads the working tree but not its authorship, so it orders a seat to commit or stash a CONCURRENT seat's in-flight work · tasks/739-session-end-backpressure-orders-a-commit-of-another-seats-in-flight-work.md
- [#740] [P1][S] The generator emits a `Dispatch-Lane` fence and the ruled verb admits only a `claude` fence, so `dispatch -DryRun` refuses every conforming generated contract — a SYMPTOM of the two-owner launch path (AX25-1) · tasks/740-generated-contract-carries-a-fence-the-ruled-verb-refuses.md
- [#724] [P1][M] The Windows baseline is permanently RED and its count is not even reliably knowable -- a red baseline hides every new failure behind it · tasks/724-permanently-red-windows-test-baseline-hides-every-new-failure.md
- [#725] [P2][S] `test_manifest_link_route` fails under xdist on a frozenset identity assert -- a test that passes alone and fails in parallel · tasks/725-xdist-frozenset-identity-pollution-in-test-manifest-link-route.md
- [#728] [P2][M] Every organ that answers a question gets a generated skill whose description says WHEN to invoke it -- the description is what the model matches · tasks/728-organ-skills-generated-from-the-organ-index-so-the-model-can-find-them.md
- [#729] [P2][M] FPG-1's queries are shell scripts the model must remember to run -- expose them as MCP tools so they sit in the tool list beside Grep · tasks/729-fpg1-queries-exposed-as-mcp-tools-so-they-sit-beside-grep.md
- [#746] [P1][M] Devcontainer history-sufficiency (B1) and ecosystem-registration (L5) repair, lost with `scripts/cloud_provisioning.py` · tasks/746-devcontainer-history-and-ecosystem-repair-lost-with-cloud-provisioning-py.md
- [#751] [P2][M] Cost in money — the transcripts' token figures become tokens and USD per lane and per model, priced from the registry's own rate card · tasks/751-cost-in-money-tokens-and-usd-per-lane-and-per-model.md
### [S19] Decide the undecided artifact/tool models
So that cadence-less artifacts and unevaluated tools don't rot or get adopted blind.

- [#123] [P2][S] Routine observability convention + value review · DEFER · tasks/123-routine-observability-convention-value-review.md
- [#347] [P2][M] Formalize the engineering loop/harness end-to-end + sanctioned safe-deletion pattern · tasks/347-formalize-the-engineering-loop-harness-end-to-en.md
- [#387] [P2][S] Rewrite the buy-vs-build intake BEFORE anything ingests it · tasks/387-rewrite-the-buy-vs-build-intake-before-anything.md
- [#440] [P2][S] Make the `tasks/` id ledger tamper-evident — a deleted retired record is undetectable · tasks/440-make-the-tasks-id-ledger-tamper-evident-a-delete.md
- [#523] [P2][M] Executive-index render leg on the generated `BACKLOG.md` · tasks/523-executive-index-render-leg-on-generated-backlog.md
- [#492] [P3][S] Grok review-lane acceptance — gated ≥ 2026-08-07, measured against terra on the same diffs · DEFER · tasks/492-grok-review-lane-acceptance-gated-2026-08-07-mea.md
- [#491] [P3][S] Gemini scanning lane — ruling R-G plus an acceptance contract · DEFER · tasks/491-gemini-scanning-lane-ruling-r-g-plus-an-acceptan.md
- [#578] [P3][S] The earned mitigated rerun — one slot, role-reminder preamble baked in · tasks/578-the-earned-mitigated-rerun-one-slot-role-reminder.md
- [#753] [P2][M] The supervised non-Claude producer trial — ten bounded tasks, stdout-only producers, admission recorded in the registry · tasks/753-the-supervised-non-claude-producer-trial.md
- [#772] [P2][M] Ten unattended outcomes price every non-Claude provider CLI on this box, and the metering unit is named where USD-per-token is the wrong instrument · tasks/772-ten-unattended-outcomes-price-every-non-claude-p.md

- [#570] [P2][L] Consume intake #27's W-wave rows — the deferred half of the tech-adoption ledger · tasks/570-consume-the-tech-adoption-ledger-w-wave.md
- [#535] [P2][S] `audit.py` has two module identities in one process, and a test's monkeypatch is invisible to one of them · tasks/535-audit-py-has-two-module-identities-in-one-process.md
- [#541] [P3][S] Scale-out substrate decision — unowned after two reports and a priced option set · tasks/541-scale-out-substrate-decision-unowned-after-two-rep.md
- [#561] [P2][S] Re-base the compute plan onto the Hetzner CX shared line · tasks/561-re-base-the-compute-plan-onto-the-hetzner-cx-sha.md
- [#567] [P2][M] CX53 daily-driver substrate lane — the every-prompt requirement, carried under `[#561]` · tasks/567-cx53-daily-driver-substrate-lane-the-every-prompt-r.md
- [#580] [P1][M] State-as-data: atomic id allocation, and `tasks/` as the SOLE source (packet ARC-B) · tasks/580-state-as-data-atomic-id-allocation-and-tasks-as.md
- [#627] [P2][M] The agy route is INERT — no row authorizes its analysis-role admission, so the token policy promises what nothing gates · tasks/627-agy-route-is-inert-no-row-authorizes-analysis-admission.md
- [#660] [P3][M] S-15 — the AJ tools-and-evals table is the one deliverable of that arc still owed · tasks/660-s-15-the-aj-tools-and-evals-table-was-never-produced.md
- [#661] [P3][M] SDA-1 is a complete benchmark design that has never been run · tasks/661-sda-1-is-a-complete-benchmark-design-that-never-ran.md
- [#696] [P2][M] M03 leg 1a ran to captured stdout with UNVERIFIED locators and one silent empty write, so the practices it produced rest on evidence nobody can re-open · tasks/696-m03-leg-1a-re-run-stdout-capture-unverified-locators-silent-empty-write.md
- [#701] [P2][S] A Codex quota hit stalls review for 50 minutes and no fallback provider is authorized, so the reviewer role is a single point of failure · tasks/701-codex-quota-hit-stalls-review-with-no-authorized-fallback-provider.md
- [#706] [P2][S] The operator packet gains D14, folder-as-domain -- and it cannot be decided before the domain census returns · tasks/706-operator-packet-gains-d14-folder-as-domain-decided-after-the-census.md
- [#722] [P1][S] Interim routing: read-only digests, censuses and scans default to agy as a READER ONLY, with conclusions and verdicts staying on Claude · tasks/722-interim-routing-read-only-work-defaults-to-agy-as-reader-only.md
- [#780] [P3][M] Three-repo comparison: a gap matrix, adopt-candidates, and an explicit will-NOT-adopt list · tasks/780-three-repo-comparison-gaps-adopt-candidates-and-an-explicit-will-not-adopt-list.md
### [S20] Revive the nightly layer, load-gauge first (rent-rule discipline)
So that unattended routines run only with a named consumer, a survival metric, and a bounded operator load — never as rot generators (the fleet-audit lesson; sequencing per the standing operator ruling: the load-gauge lands before anything else in the Tier-2 nightly layer).
- [#271] [P3][L] Nightly proposal loop · tasks/271-nightly-proposal-loop.md
- [#610] [P2][M] The night-batch protocol, named — with its two missing verbs · tasks/610-the-night-batch-protocol-named-with-its-two-verb.md
- [#288] [P3][S] Model-identity guard for unattended runs · DEFER · tasks/288-model-identity-guard-for-unattended-runs.md
- [#419] [P2][M] We run routines whose output nobody consumes · tasks/419-we-run-routines-whose-output-nobody-consumes.md
- [#426] [P2][M] Declare `consumer` + `consumption_path` for every LIVE routine · tasks/426-declare-consumer-consumption-path-for-every-live.md
- [#428] [P2][S] `nightly-triage` reports a dead producer to every session start · tasks/428-nightly-triage-reports-a-dead-producer-to-every.md
- [#493] [P2][S] B-2 investigation — the scheduled fleet-baseline task has been silent 10+ days · tasks/493-b-2-investigation-the-scheduled-fleet-baseline-t.md

---

- [#555] [P1][M] Closing campaign batch 1 + kill-candidates instrument · tasks/555-closing-campaign-batch-1-kill-candidates-instrum.md
- [#655] [P2][S] `run_retention()` has no production caller, and the ruled one is `fleet_health`'s daily run · tasks/655-run-retention-has-no-production-caller.md
- [#657] [P1][S] Orphan #33 — something outside the repo writes into it on a schedule the registry does not know · tasks/657-orphan-33-an-unregistered-writer-edits-the-repo-nightly.md
- [#673] [P2][S] Six batch-V suite REDs are unattributed, and only a same-substrate run on the pre-batch commit can attribute them · tasks/673-six-batch-v-suite-reds-are-unattributed-and-only-a.md
- [#702] [P1][M] The repo declares zero `cron:` and zero `schedule:`, so the nightly layer `[S20]` exists to revive has nothing to revive · tasks/702-zero-cron-zero-schedule-the-nightly-layer-has-nothing-to-revive.md
- [#723] [P1][M] Nothing reads the logs, so a model that silently stops delivering costs a whole night before anyone notices -- a log-review routine that files its own anomalies · tasks/723-log-review-routine-self-healing-runs-as-a-batch-close-lane-until-conductor-e.md
- [#732] [P1][S] Ratification #7: a committing lane runs LOCAL overnight only, and during working hours it waits for the night or for conductor E · tasks/732-committing-lanes-run-local-overnight-only-ratification-7-honoured.md
## [E8] ARC-5 execution
> As the operator, I want ARC-5's wave map, closure contract, and unruled decisions to live somewhere that can EVOLVE as waves land — not frozen inside an immutable handoff bundle.

**Why this form (basis).** The plan of record needs a home that changes as waves land. An **ADR is the wrong form** — ADRs are immutable (CLAUDE.md §5 rule 3); only the status line is editable (ADR-94), so a wave map could never be updated in place. `BACKLOG.md` is **living / update-in-place** (§4 File lifecycle) and is already the repo's declared spec surface ("the BACKLOG is the spec; items are tickets"). The live schema is a story map — verified **7 themes / 20 stories / 116 tasks** at filing (ADR-66; `scripts/validate_backlog.py`). So the plan lands as a **theme + stories** here, not an ADR and not a new path. `[E8]` is marked a time-boxed arc, not a permanent mission theme, so it retires when ARC-5 closes.

**Accretion discipline.** The seven waves are recorded as the **wave map below**, not as seven pre-filed stories with placeholder tasks. Each wave's build tasks are filed **when that wave opens**, so this filing adds three carried tickets rather than a speculative +10 — which is what closure criterion (d) below requires.

**Source.** `docs/handoffs/2026-07-20-dev-knowledge-architect-arc5/` (SUPPLEMENT ANSWERS, operator-authored 2026-07-19) ∩ `docs/audits/2026-07-19-technical-night-consolidated-cycle-close.md` §3 (the nine seeds, terra-corrected). Strategic intent, verbatim: **"AUDITS ARE OVER. ARC 5 IS EXECUTION."** Meta-finding the arc closes: *"decision recorded ≠ decision enforced ≠ decision legible."*

#### Wave map W1–W7 (ordered by operator pain-priority, not dependency elegance)

**W1 — VISIBLE BOUNDARY** (the "colors"; the operator's most-repeated ask). Build #329/#352: versioned `.vscode` background decoration (grey/navy, dark theme) of `owner=hub` / `owner=repo` regions, deployed fleet-wide as carrier material; plus a sweep completing RULING-S reader-visible universal-vs-repo section headers in every governed file across all three repos. **Done when:** the operator opens any governed file in any repo and SEES which lines are methodology and which are repo-personal. **Deadline:** must land before the P4a `.vscode` ruling shelf-life **2026-08-13**. **SEEDLESS** — see the seedless note below.

**W2 — STRUCTURE EQUALIZATION LEG 2** (the `assets/` folder, mypy, "why do folders differ"). Disposes `ai-council/assets/ruff-pre-commit.yaml` per **R1**; mypy/cache posture per **R1b**; `hub-toc-hooks` resolution (S5 §4.2 — recommended path (b): hub manifest re-scope v1.3.2 matching the hub's own retirement, then prune ai-council + retire corp's waiver); #331 ratification + `parity-surfaces.yaml` consumer-tier rows for the BACKLOG story-map schema + gate; reconcile the corp-vs-ai `validate_backlog.py` fork; corp `deployed-versions.yaml` currency (evidence for #276). **This wave carries consolidated-report seed 5** (consumer parity-surface reconciliation, S5) — mapped by CONTENT, not by label. **[#355] routes here.** **Done when:** each named divergence is either equalized or recorded as a declared, time-boxed divergence; every consumer write goes via RULING-W worktree/branch → report; changes land as manifest/template carrier material (replication-first, not one-off fixes).

**W3 — LIFECYCLE MECHANISMS** (intake→ADR→backlog→close→DELETE — "the process problem"). Carries **seeds 2, 3, 4** + the #269 build. Seed 2: `validate_intake.py` HARD pre-commit gate — closed status enum (+ ratified tech-extension per **R4**), unique `intake-id` (fixes the live id:14 triple collision), required `consumed-by` on CONSUMED, machine-readable `Intake:` provenance on ADRs + citation enforcement (ADR-102/103 backfill or recorded non-intake-origin). **[#398] update (2026-07-23):** the enum is DEPLOYED (README §5 + `gen_intake_index._STATUS_ORDER` + template), the id:14 triple is dissolved, and the R4 tech-extension allowlist is DEAD (rejected by the 2026-07-19 ruling, SUPPLEMENT.md:68-70); the validator's current spec is `docs/audits/2026-07-23-technical-status-enum-reconcile.md` §4 (supersedes night-batch P2c). Seed 3: build #242 (ADR header↔README status reconciliation; ADR-88/89 frozen-Proposed case). Seed 4: `gen_grooming_worksheet.py` + an `audit.py` grooming-cadence/net-delta WARN (witnessed accretion 74→116 in 11 days, ≈3.8/day) + extend `safe_remove.py` M2/M3 as #347's sanctioned REAL-DELETION mechanism per **R3**. Plus #269 (count-tiered audit index, ADR-100). **Done when:** a seeded off-enum status, a duplicate `intake-id`, and an uncited ADR are each flagged with tests; #242 and #269 are built; the grooming worksheet + accretion WARN are live; `safe_remove.py` M2/M3 is the sanctioned deletion path.

**W4 — ARCHIVE LEGIBILITY** (the operator's archiving ask). **R2** decides the shape. Facts already true: file NAMES encode genre+date by convention (`ADR-NN-slug`, date-class-slug audits, date-genre-slug intakes); the ruled convention is stay-in-place (join keys, ADR-101 seal) with status on index surfaces. **Done when:** R2 is ruled AND its build has landed — either (a) the index/status surfaces (seeds 2/3 + #269 + the handoff-README micro-era clause) OR (b) a physical `archive/` with a genre-preserving naming rule via ADR amendment. **NOT both by default; no silent relitigating.** **SEEDLESS** — see the seedless note below.

**W5 — SESSION/WRITE GUARDS** (worktree pain; #353/#344/#349). **This wave carries consolidated-report seed 6** (session-boot + consumer-write guards, S6) — mapped by CONTENT, not by label. Per **R5**, ONE unifying organ: a HEAD-bound operator-authorization token (naming worktree + branch + allowed paths) checked by a `PreToolUse` guard, satisfying #344 Ask-2 (consumer hub-write guard), #353 (boot contract), and the S7 prompt-attestation at once. Plus S6's boot-snapshot `SessionStart` hook, the `.claude/.session-lock` HEAD-movement advisory, #349's close-discipline boot echo, and a signed integration-return token for self-merge detection. **Justification:** six recovered-not-prevented incidents, the sixth carrying a clean reflog trace (a concurrent session swapped HEAD in the primary tree mid-command during handoff generation; no guard fired). **Done when:** the organ REFUSES a witnessed unauthorized write (n≥1 witnessed refusal, not merely installed) — the incident class moves from recovered to prevented.

**W6 — CANON INOCULATION + PROMPT EQUILIBRIUM** (PLAYBOOK/handoff currency). Carries **seeds 1 and 7**. May run FIRST, in parallel, as a doc lane — file-disjoint from W1/W2. Seed 1: transcribe the four un-inoculated rulings (RULING-W · two-tier · worktree side-effect rule · consumer merge-delegation composite) into PLAYBOOK (operational) + ESSENTIALS (one-liner), grep-verified against the ADR amendments; **plus** the staged-diff CO-CHANGE checker (**[#354]**). Seed 7: the 7-item inbound prompt-spec as a PLAYBOOK §2 amendment + a handoff-time self-check probe (**R6** decides hard-probe vs soft). Plus handoff-README micro-era documentation (stage1/stage2 archive class). **Done when:** the four rulings carry PLAYBOOK + ESSENTIALS text grep-verified against their ADR amendments AND the co-change checker flags an ADR-36/41/101 amendment lacking a companion PLAYBOOK/ESSENTIALS edit. *Legibility half already landed at merge `8c913a6a`; the enforcement half is [#354].*

**W7 — TESTING + FLEET STATE** (last, per dependency). Carries **seeds 8 and 9**. Seed 9: dynamic-test evidence gate (code-impact tier in `ship.md` or a versioned `test-harness.yaml`), **WARN-first then FAIL after two demonstrated runs**, depends-on #270; `protocols/AGENTIC_TESTING.md` as #412 config material (re-owned 2026-07-25 — #348 was decomposed to grooming-only; the configured-workflow layer this seed feeds now lives in #412). Seed 8: a scheduled `fleet_collect` PULL collector with watermarks ("silence ≠ absence") subsuming the two reporters; SQL/SIEM stays SHELVED until a witnessed join-pain (**R7** confirms this as the standing answer, matching the intake #14 ruling). **Done when:** the evidence gate is live WARN-first with its FAIL-after-two-runs rule recorded, `AGENTIC_TESTING.md` exists as #348 config, and the collector runs on a watermarked schedule.

#### Seedless waves (do not read the seed list as the wave list)

**W1 and W4 are the SEEDLESS waves** — neither is backed by a seed from the nine-seed consolidated report:

- **W1** is justified by **operator priority and the 2026-08-13 `.vscode` ruling shelf-life — NOT by audit evidence.** It is first because it is the most visible, deliberately (the operator's frustration is itself context: visible results per wave).
- **W4** owns no seed of its own; it **discharges W3's seeds 2/3** (index/status surfaces) if R2 lands on shape (a). If R2 lands on shape (b), W4 acquires its own build via ADR amendment.
- **Seeds 5 and 6 map to W2 and W5 by CONTENT, not by label** — they are named explicitly in those waves' text above. A reader matching seed numbers to wave numbers will drop them in execution; that is why they are named rather than numbered.

#### Closure contract (frozen — reproduced verbatim)

```
ARC 5 is CLOSED when and only when: (a) the ledger exists as a mechanism, four-state, over
MUST-shaped governed rules — not ADRs; (b) the silently-unenforced count strictly decreases and
everything still unenforced has moved to declared-unenforced with an owner and a review date;
(c) each shipped wave carries a frozen done-contract, a Codex review before merge, an educate
artifact with file-level before→after, and a BACKLOG structural-marker change; (d) backlog
accretion is net ≤ 0 excluding tickets minted by ARC-5's own waves, every open item adjudicated at
least once, and the accretion rate measured and reported; (e) enforcement is witnessed, not
installed — for every guard or gate shipped, a run exists in which it fired or refused; (f) the
operator confirms, per wave, in his own words, that the named pain is gone.
NOT closure: waves merged, ship-gate green, tests passing, items marked done.
```

> **Clause (b) — RULED F1 (operator, 2026-07-27; discharges the R12 fork below).** Clause (b) will be amended to **ratchet + bounded drain**: gate the GROWTH of silent rules (the ratchet — built by [#436], row-independent) *and* drain a bounded slice, rather than dispositioning all 176. The **drain row selection (scope) is still pending** the operator's pick; the drain matrix is **slice × mechanism × owner × review date**. The frozen text above is deliberately UNCHANGED — this records the ruling; the amendment lands with the row selection.

> **Clause (b) — AMENDED (operator ruling D1, 2026-07-28; lands the F1 row selection above).** The frozen contract text stays verbatim — this blockquote is the amendment of record. Clause (b) is discharged by **ratchet + bounded drain**: the ratchet ([#436], BUILT — merge `6195d932`) gates the GROWTH of silent rules, and the **drain slice is [#356] + [#358]–[#361]** (the two still-silent seed-1 rules + the four census escalations; [#362]'s 49 dropped #242 guards are NOT in the slice). **Architect prepares / operator ratifies.** **Review date 2026-08-26.** Matrix unchanged: slice × mechanism × owner × review date. **Recorded, never executed** — this selects the slice; no drain is performed by this entry.
>
> **Operator intent (2026-07-28):** the FULL silent-rule pool (428 @ detector `silent-rule-v4`) is to be dispositioned over time — drained, mechanized, or DELIBERATELY RETIRED as no-longer-valid; staged, wholesale classes post-flip. **Nothing expires by being forgotten.**
>
> **Drain-owed now:** `PLAYBOOK.md:1270`, `REPO_ONBOARDING.md:92`, `REPO_ONBOARDING.md:199` + the 43-line delta per `docs/audits/2026-07-27-census-silent-rule-ratchet-arm-measurement.md`, review **2026-08-26**. **Baseline semantics:** architect-proposed 2026-07-27, operator-adopted (D4), test-and-iterate.

#### Metric definition — the declaration test (operative; governs closure clause (b))

Closure clause (b) turns on the four-state ledger, so the boundary between `silent` and
`declared-unenforced` is load-bearing. Operator-ruled 2026-07-19, recorded verbatim:

```
A MUST-shaped rule counts as declared-unenforced only if the non-mechanisation clause is BOTH
on-surface -- at the rule's own file:line or its canonical PLAYBOOK/ESSENTIALS span, because
`silent` means a reader OF THE RULE cannot tell it is unenforced -- AND bound to an OPEN ticket
naming the remaining work, per ADR-81(d). Neither condition suffices alone. Without the second,
N_silent is gameable by writing 'this isn't enforced' next to every rule.
```

**Baseline — first measurement under that definition, pinned to `bf49cbf9`.** Denominator **320**
MUST-shaped rules · **N_silent 176 (55%)** · **N_enforced 130** · **N_declared 14**. Scope was
`protocols/` + `templates/` + `ecosystem/*.yaml`; `docs/decisions/` is deferred to a second sweep
([#357]), so **176 is a floor, not a total**. N_enforced is deliberately **conservative** — ~55
partial-mechanism rules (one leg gated, the rest not) are folded into `enforced`, and splitting
them strictly would raise N_silent. Controls held: the ADR-template intake-id cite rule and the
merge-delegation composite both measured `silent`; the worktree side-effect rule measured
`declared-unenforced`, having been converted out of `silent` by `8c913a6a` — the canon inoculation
working as designed, not a model failure. **Evidence** — the 176-item itemisation, the declared list, the near-misses, and the pending-#242 per-ADR table are archived at `docs/audits/2026-07-19-census-silent-rule-ledger.md`.

#### DECISIONS — dispositioned 2026-07-26 (the "ALL UNRULED" claim was true at filing, false since)

Every decision below was **UNRULED as of its filing** (2026-07-19). The recommendations are the outgoing architect's, carried verbatim in substance; **a recommendation is not a ruling.**

> **Disposition sweep 2026-07-26 (intake #17 §5 micro-window).** Each row was re-verified against LIVE state, not against the filing. The table had survived at least one operator ruling by three days.
>
> **Delegation authority for the four RULED rows** — and it is a delegation, not a recommendation promoting itself: the operator's 2026-07-26 micro-window execution order (intake #17 §5) instructed that rows verified still-LIVE be recorded as *"RULED per attached recommendation — operator-delegated 2026-07-26"*. That standing instruction is the ruling record for R1b/R3/R5/R6; the per-row cells carry the LIVE-premise verification that qualified each row for it. R8 was excluded by the same order (his own pick) and R12 has no recommendation to delegate to.
>
> Outcome (final, after two review passes): **1 DEAD-OBE** (R1 — the folder it decides about no longer exists), **3 ALREADY-RULED** (R1b, R2, R4), **4 RULED by operator-delegated adoption** (R3, R5, R6, R7), **1 still open for the operator** (R8 — PARKED, his own pick; **R12 discharged 2026-07-27 by the clause-(b) ruling F1 above**, so the sweep's "2 still open" no longer holds). **All three already-ruled rows went AGAINST their recommendation** — R1b rejected (Pyrefly universal, not a divergence), R2 chose (b) over (a), R4 rejected outright. That is the sweep's most useful finding: where this table had a prior ruling, the recommendation lost 3 times out of 3, so an unverified recommendation is a poor predictor of the operator's call. A ruling here is **recorded, never executed** — each adopted row still needs its build.
>
> **Reconciliation debt this sweep creates — the FULL list, enumerated after sol's adversarial pass found the first version incomplete.** Dependent rows still carry the pre-sweep status and were deliberately NOT reworded (out of this window's two-row edit scope): **`[#389]`** reads "R6 … **UNRULED**; rule R6 first" and gates its own Done-when on it · **W3 seed 2** says "+ ratified tech-extension per **R4**" (already self-superseded later in the same paragraph by the `[#398]` update) · **W4** says "**R2** decides the shape" though R2 is ruled · **W6 seed 7** says "**R6** decides hard-probe vs soft" · **W7 seed 9** says "**R7** confirms". Reconcile each when its wave opens; none is a silent contradiction now that all five are named.

| Ref | Decision | Status (verified 2026-07-26) | Recommendation as filed (NOT a ruling) |
|---|---|---|---|
| **R1** | `assets/` disposition: (a) DISSOLVE — relocate `ruff-pre-commit.yaml` to the canonical config location, delete the folder (RULING-W leg + safe-deletion path); or (b) UNIVERSALIZE `assets/` as a fleet deployment convention | **DEAD-OBE** — the folder is gone. `ai-council/assets/` was dissolved by `6d78851e` (2026-07-21) "dissolve vestigial assets/ and repair its two live references"; `git ls-files assets/` is empty and no `ruff` path remains tracked. Option (a) was executed without the ruling. | **(a)** — one file, no fleet role; (b) would mint a new mandatory folder fleet-wide for no carrier need |
| **R1b** | mypy posture: declare ai-council's mypy a sanctioned divergence vs roll out fleet-wide | **ALREADY-RULED — REJECTED, against its recommendation.** Caught on sol's adversarial pass: a **BINDING** operator ruling already exists and the delegated adoption first recorded here was withdrawn as a relitigation. `docs/handoffs/2026-07-20-dev-knowledge-architect/SUPPLEMENT.md:113` heads the block "BINDING — do not relitigate" and `:119` reads "Pyrefly is universal across the fleet — **NOT** a sanctioned mypy divergence"; `PASTE_THIS.md:528` records "mypy as a sanctioned divergence → **REJECTED by the operator**. Python stack, tooling universal → Pyrefly". The ruling is UNIVERSALIZE, not diverge. (Method note: the first pass searched JOURNAL/LESSONS/docs-decisions and missed it — `docs/handoffs/` carries binding rulings too.) | **Declare sanctioned divergence** |
| **R2** | Archive shape: (a) INDEX-ARCHIVE — status/count-tiered index surfaces, files stay, names already carry genre; or (b) PHYSICAL `archive/` folders with a genre-preserving rename rule via ADR-98/100/101 amendments | **ALREADY-RULED 2026-07-22 — and the ruling went to (b), NOT the recommended (a).** "**Archive-inside-each-folder** (operator ruling 2026-07-22)" in `ARCHITECTURE.md` Ch5 (quote the heading, not a line range — this window's own edits shifted it from :563 to :595); six physical `archive/` dirs exist on disk; applied at `JOURNAL.md:548-550`. The recommendation was not followed — recorded so the divergence is not re-litigated as an open pick. | **(a)** — zero join-key breakage, builds already seeded |
| **R3** | #347 safe-deletion = `safe_remove.py` M2/M3 extension as THE sanctioned mechanism | **RULED per attached recommendation — operator-delegated 2026-07-26.** Premise verified LIVE: `safe_remove.py` exists but is **M1 only** (no M2/M3 in the file), `[#218]` carries M2/M3 and is DEFER, `[#347]` is open and unruled. Recorded, not executed. | **YES** |
| **R4** | Intake enum: ratify the 6 off-canon statuses as a documented tech-genre extension vs reclassify the docs | **ALREADY-RULED 2026-07-19 — REJECTED, against its recommendation** (reclassified from DEAD-OBE on terra review: a decision that was decided is not one overtaken by events). The 2026-07-19 ruling (`SUPPLEMENT.md:68-70`) rejected ratifying the six off-canon statuses outright; W3's `[#398]` update records "the R4 tech-extension allowlist is DEAD", and the ruled enum SEED→DRAFT→READY→{ACCEPTED\|CONSUMED\|SUPERSEDED\|REJECTED} is deployed in `gen_intake_index._STATUS_ORDER`. | **Ratify-with-documentation** — they are functioning plan-of-record artifacts |
| **R5** | Unifying HEAD-bound authorization token as ONE organ for #344/#353/attestation, vs three separate builds | **RULED per attached recommendation — operator-delegated 2026-07-26.** Premise verified LIVE: `[#344]` and `[#353]` are both open, the unified organ is unbuilt, and the only HEAD-bound token in code is `/override`'s `logs/.session-override-token` — a different organ. Recorded, not executed. | **ONE organ** |
| **R6** | Prompt-spec: hard handoff probe vs soft self-check | **RULED per attached recommendation — operator-delegated 2026-07-26.** Premise verified LIVE, against a first-pass misread: `verify_handoff_probes.py` is the **#163 PROBES.md-teeth** validator, NOT the prompt-spec probe R6 decides. No prompt-spec probe exists (`scripts/` has no `prompt_spec`; PLAYBOOK carries no §2 prompt-spec amendment) and W6 seed 7 still reads "**R6** decides hard-probe vs soft". Recorded, not executed. | **Hard probe on the bundle side** — the off-repo prompt itself can't be gated; attestation covers the paste |
| **R7** | Fleet-state: confirm "collector + reporters now, SQLite shelved" as standing | **RULED per attached recommendation — operator-delegated 2026-07-26.** Corrected on sol's adversarial pass: this was first recorded ALREADY-RULED, but the cited authority says the opposite — `docs/intake/2026-07-12-siem-requirements-ruled-pack.md:61` explicitly retains least commitment, "store/viewer class (SQLite vs DuckDB) … are Phase A build decisions, **not settled here**", and FR-18 lives only in the ARCHIVED provenance draft, not the ruled pack. So the shelving genuinely was open and is ruled here by delegation. Live state already matches: reporters on disk, zero `.db`/`.sqlite` anywhere. | **Confirm** |
| **R8** | (carried, corp-side) #38 channel pick: 1 primary-direct / 2 worktree / 3 epic-dev | **UNRULED — stays that way.** The operator's own pick; four exhaustive searches across BACKLOG/JOURNAL/docs found no ruling. Explicitly NOT delegated. | *(none recorded — operator's pick)* |
| **R12** | Closure clause (b) is **not achievable in one arc** at N_silent 176 — "everything still unenforced has moved to declared-unenforced" would require dispositioning 176 rules. Two options: **(i) NARROW** the arc target to a bounded load-bearing slice — the 4 census escalations ([#358]–[#361]) + the 2 still-silent seed-1 rules (RULING-W, merge-delegation, [#356]) + the 49 dropped #242 guards ([#362]); or **(ii) GATE THE GROWTH** of silent rules rather than drain the pool. | **LIVE, and NOT delegable — needs the operator.** Premise verified current: `[#242]`, `[#356]`, `[#358]`–`[#362]` are all still open, N_silent 176 still stands (`BACKLOG:316`, census ledger `:111`), evidence artifact present. But **no recommendation is attached**, so there is nothing to rule by delegation — narrow-vs-gate is a genuine operator choice. | *(none attached — a recommendation is not a ruling)* |

> **Numbering note (2026-07-19):** the census-derived decision above is filed as **R12**, not R9 — the discrepancy below records that R9/R10/R11 never existed in the ARC-5 bundle, and minting R9 now would resurrect a ref the record says does not exist.

> **Discrepancy recorded — the ruling set is R1–R8 (+R1b), nine picks; there is no R9, R10, or R11.** The lane prompt for this filing specified "R1–R11". An exhaustive search of the ARC-5 bundle (`SUPPLEMENT.md`, `PASTE_THIS.md`), all fourteen `docs/audits/2026-07-19-*` night-audit artifacts, and `JOURNAL.md` found exactly the eight R-labels above plus the R1b sub-ruling. The only `R9`/`R10`/`R11` strings in the repo belong to a **different, unrelated R-namespace** (`docs/audits/2026-06-07-methodology-transfer-audit.md`). Three rulings were **NOT invented to reach eleven** — per the filing instruction "do not invent rulings". If the operator holds R9–R11 off-repo, they are missing from every repo source and must be supplied.

#### BINDING (travels verbatim; do NOT relitigate)

The ARC-4 rulings (RULING-W/S/PY/CF; two-tier "compliance IS authorization" in force now); the terra ×7 corrections as applied; sol's 4 mechanism upgrades as accepted strengthenings; **satellite wave FROZEN** until Wave-1 lessons are extracted; luna's floor-misreport corrected (consumers DO carry the floor, hash-matched — Haiku fan-out is indicative, not authoritative); E1 scope honesty (only two organs were fire-proved this run).

**CONSIDERED + REJECTED:** SQL/SIEM now (premature per intake #14 + S8); a `coherence-nudge` extension for co-change (terra: not implementable — see [#354]); blanket new-path blocking (the two-tier rule supersedes); physical file moves for archival as the default (R2 decides; convention says stay-in-place); more audits (operator: enough).

**DO-NOT-REDO:** the nine seeds' adjudication (terra-corrected kill-candidates stand); the 8-domain gap derivation (sol-triangulated); the ARC-4 equalization values (py311 / 120 / >=0.15.5 / minversion 9.0 — at-parity, verified); the grooming closes #306/#307/#328.

**Per-wave standing requirements** (from the closure contract, applied to every wave): a frozen acceptance contract before delegation · Codex terra review pre-merge · RULING-W for any consumer write · replication material over one-off fixes · an educate artifact with file-level before→after · one wave = one merged arc.

### [S21] Discharge the ARC-5 carried items that no wave has yet absorbed
So that the three items carried out of the night-audit cycle stop living only in narrative — each becomes a ticket with a done-when, rather than being rediscovered a wave later.
- [#354] [P2][M] W6 seed-1 recurrence half · tasks/354-w6-seed-1-recurrence-half.md


### [S22] Discharge the silent-rule census findings
So that the four-state ledger's first measurement produces tickets rather than a report nobody acts on — each finding gets a done-when, and the two findings the four-state model cannot express are named as such.
- [#357] [P2][M] Silent-rule census run 2 · tasks/357-silent-rule-census-run-2.md
- [#359] [P1][M] PHANTOM ENFORCEMENT — `protocols/HANDOFF_PROCESS.md` §14a FILE-BOUNDARY claims a mechanism that does not exist. · tasks/359-phantom-enforcement-protocols-handoff-process-md.md
- [#402] [P3][S] Intake naming clause — DEPLOY the `YYYY-MM-DD-<class>-<slug>` half of the enum ruling · tasks/402-intake-naming-clause-deploy-the-yyyy-mm-dd-class.md
- [#361] [P3][S] ADR-immutability's real coverage is declared only in code, never in the protocol · tasks/361-adr-immutability-s-real-coverage-is-declared-onl.md
- [#362] [P2][M] #242 carries a SUBSTANTIVE guard loss, not status hygiene · tasks/362-242-carries-a-substantive-guard-loss-not-status.md

- [#365] [P3][S] Promote `residual_completeness` from `exempt:` to `coverage_scope` · tasks/365-promote-residual-completeness-from-exempt-to-cov.md


- [#369] [P3][S] Wire `boundary_headers.py --check` into pre-commit · tasks/369-wire-boundary-headers-py-check-into-pre-commit.md
- [#371] [P2][S] Consumer editor-config write-through — declared at v1.4.0, never built, never ticketed · tasks/371-consumer-editor-config-write-through-declared-at.md
- [#400] [P3][S] Ownership-model: the hub-mandated-STRUCTURE / repo-owned-CONTENT cell (rosters) — same ruling family as [#370] · tasks/400-ownership-model-the-hub-mandated-structure-repo.md
- [#413] [P2][S] Colors semantics — visually distinguish global/hub-managed vs per-repo content in governed markdown (declared ai-council interim) · tasks/413-colors-semantics-visually-distinguish-global-hub.md
- [#427] [P3][S] Region templates carry a repo-POSITION-DEPENDENT path · tasks/427-region-templates-carry-a-repo-position-dependent.md
- [#448] [P2][S] A11 staged-diff guard — cover EVERY candidate bundle, not just the active one · tasks/448-a11-staged-diff-guard-cover-every-candidate-bun.md

---

## [E9] Fleet Desired-State System (North Star)
> As the operator, I want the fleet's desired state declared once as versioned data and mechanically reconciled, so that "done" stops being anyone's word and becomes a report I can read in two minutes.

**Source.** `docs/intake/2026-07-21-func-fleet-north-star.md` (intake **#16**, DRAFT) — the Layer-1 architect's consolidation of the operator's dictated vision (2026-07-20/21), the Fable vision audit, the 2026-07-21 read-only polyrepo recon, the `assets/` delivery session, and three months of session lessons. The stories below map intake §6's sequenced plan; each link unblocks the next, so the gating is expressed as `depends-on`, not as preference.

**The brake is DISCHARGED.** Intake §6's standing constraint — *no new fleet machinery before [#381] rules* — was met when **ADR-104** was accepted and merged at **`92fabb51`**, closing [#381]. S24–S27 remain sequenced: [#383] is gated on [#382], and [#385] on [#383]. **Those gates are recorded in prose and are NOT mechanically enforced** — `validate_backlog`'s `_DEPID_RE` requires a `#` and the [E9] chain's clauses are written bare, so they do not fire; see [#424].

### [S24] Declare desired state once, as data, instead of as N registries — **COMPLETED 2026-08-01**
So that every check derives from one schema — a check without a schema row is the registry-sprawl anti-pattern that produced "green that means nothing".

**COMPLETED 2026-08-01.** All tasks closed: [#382] (`0acc3328`, merged `f7abe228`) and [#459] (`bf373b13`, merged `31c80714`). The heading is RETAINED, not deleted — retire-not-delete at story level: a completed story keeps its place in the map so the [E9] sequence stays readable and its id is never re-issued, exactly as a retired task keeps its allocation record (ADR-107 §6.3). FIRST empty story on main — this marker is the precedent.

### [S25] Converge surfaces in waves, with a mechanical done-signal
So that a wave closes on a report rather than on a claim — the operator stops verifying convergence by hand.
- [#383] [P2][L] Execution waves per surface · tasks/383-execution-waves-per-surface.md

### [S26] Mine our own history before predicting anything
So that "the repo learns us" starts as a cheap descriptive lane on real data, not as an ML platform bought ahead of the evidence.
- [#392] [P3][S] fleet_analytics rename-alias loses history on path-reuse · tasks/392-fleet-analytics-rename-alias-loses-history-on-pa.md
- [#393] [P3][S] corp-sca rot review — confirm-live-or-retire 3 candidates · tasks/393-corp-sca-rot-review-confirm-live-or-retire-3-can.md

### [S27] Make tech-currency a distributed rule, not a one-off
So that a version bump researched once reaches every repo through the deploy channel instead of dying in a session.
- [#385] [P3][M] L4 tech-currency lane · tasks/385-l4-tech-currency-lane.md
- [#495] [P3][S] Tech-currency cadence — give [#385] a recurring lane instead of a one-off · DEFER · tasks/495-tech-currency-cadence-give-385-a-recurring-lane.md

---

**About this file** — open `.dev-knowledge` work as a story map (ADR-66): Big Picture → Theme → User Story → Task. Stories are human (goal + `So that`); tasks carry `[#id] [P][size] · Done when · refs`. Done tasks **leave** (ADR-65); git is the implementation record (`git log --grep 'closes \[#'`). Child-repo execution items live in `docs/audits/2026-06-01-child-repo-relocation-proposal.md`. Schema: PLAYBOOK §10; machine-checked by `scripts/validate_backlog.py`.

**ai-council audit residuals (pointer, not filed here)** — the ai-council audit surfaced ai-council-owned cleanups (stale force-added `settings.local.json` pointing at dead paths; an empty `worktrees/fix/` dir; codemap/backlog-hook universalization gaps). Added 2026-07-06 (Wave-3, root adjudication 5): the relative-path pre-commit source (`repo: ../.dev-knowledge`) makes ai-council's toc-freshness gates layout-dependent — ANY out-of-layout checkout (CI, second clone, another machine) silently loses them (witnessed: the sandbox clone; measurement-3 audit) — decide pin-by-URL+rev vs documented layout constraint. Per ADR-41 routing these are filed in a dedicated ai-council session, not duplicated in the hub backlog.

**Grooming log:** git history is the record (`git log --grep 'groom'` + per-session JOURNAL). Recent: 2026-06-12 (#149 flip) · 2026-06-18 (currency pass) · 2026-06-25 (groom pass, n=2: 84→81) · 2026-07-08 (leg-c full ruling pass, operator-ratified, 124→74: 14 KILL / 27 MERGE / 2 MOVE / 9 CLOSE / 5 RE-SCOPE / 19 DEFER-peg / 2 new filings #289 #290; #110 #128 moved-to: ai-council (Wave-1)) · 2026-07-30 (per-handoff lightweight groom, arc 0731-g0-groom: 6 doc_rot accretion rows condensed — #344 #421 #422 #332 #278 #426, no live obligation dropped; 5 warn-doc-rot dispositions retired; ADR-105 night-batch routine activated on #426). · 2026-09-14 (mechanised groom, lane `lane-y-754-backlog-to-bar`: the `archive_row_body.py` trigger run to EXHAUSTION over the rows above the 1320-char ceiling — 60 rows, 66 clauses, 18,107 source chars relocated byte-identically into `tasks/archive/`, 84 records re-proven on legs A–E; accretion arm 5 → 4, #241 cleared; over-ceiling COUNT unmoved at 148 of 322 and `propose` now returns one row, itself already under the ceiling — the mechanism is exhausted above the line, measured rather than asserted, and the residual is 35.3% structural clauses plus 38.2% undated prose, both outside the predicate by construction). Next quarterly: 2026-10-08.
