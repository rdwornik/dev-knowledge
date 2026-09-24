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
- [#602] [P2][M] Land the ruled dispatch verb in the bundle's forms card, and extend the agreement gate to the bundle sites · tasks/602-land-the-ruled-dispatch-verb-in-the-bundle-s-for.md
- [#603] [P3][S] An operator-interface capability file — the facts every seat re-derives about how the operator works · tasks/603-an-operator-interface-capability-file-the-facts.md
- [#619] [P2][M] The FM-2 to FM-4 funnel-health coupling is dead — six fields, zero overlap · tasks/619-the-fm-2-to-fm-4-funnel-health-coupling-is-dead.md
- [#641] [P3][S] Declare a MEMORY.md byte budget, or rule that none is owed · tasks/641-declare-a-memory-md-byte-budget-or-rule-that-none.md

---
- [#662] [P2][S] The R6 handoff-exception rule reached none of the three carriers it was written for · tasks/662-the-r6-handoff-exception-reached-none-of-its-three-carriers.md
- [#663] [P2][M] The v7.1 boot carries no interface block and no floor item 7, and the bundle is over its own ceiling · tasks/663-the-v71-boot-carries-no-interface-block-and-no-floor-item-7.md
- [#887] [P1][S] The handoff preflight scans the whole shared transport, not the handing-off seat's own files -- a concurrent workstream's decision files refuse this seat's cut · tasks/887-the-handoff-preflight-scans-the-whole-shared-tra.md

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
- [#786] [P2][S] Give the PLAYBOOK order-conventions heading a gate · tasks/786-give-the-playbook-order-conventions-heading-a-ga.md
- [#828] [P1][S] 752 · tasks/828-752.md
- [#829] [P1][S] 613 · tasks/829-613.md
- [#830] [P2][M] Witness · tasks/830-witness.md

- [#510] [P2][M] Scope the R-1 exemption to the lanes its manifest enumerates — self-grantable by branch naming today · tasks/510-scope-r1-exemption-to-enumerated-lanes.md
- [#514] [P1][M] Two rival `LANE_BRANCH_RE` constants ship in one repo · tasks/514-two-rival-lane-branch-re-constants-reconcile-them.md
- [#531] [P2][S] Lane-grammar enforcement at PROVISIONING — the enum is checkable but nothing checks it · tasks/531-lane-grammar-enforcement-at-provisioning-the-enu.md
- [#533] [P2][M] Decompose the `audit.py` check monolith into `scripts/audit_checks/` — one module per check plus an ordered registry · tasks/533-decompose-the-audit-py-check-monolith-into-scrip.md
- [#534] [P2][S] `scripts/audit.py:<line>` locators on four open rows died at the `[#533]` decomposition · tasks/534-audit-py-line-locators-on-four-open-rows-died-at-t.md
- [#552] [P2][M] Window-close disposition + archival routine — every new audit gets a disposition, every terminal ADR/intake is archived · tasks/552-window-close-disposition-and-archival-routine.md
- [#579] [P1][L] Code doctrine & FDD — one ADR merging intakes #31 and #34 (packet ARC-A) · tasks/579-code-doctrine-fdd-one-adr-merging-intakes-31-and.md
- [#583] [P2][M] Green-by-skip sweep — a check that cannot obtain ground truth must not report OK (packet ARC-E, C18) · tasks/583-green-by-skip-sweep-a-check-that-cannot-obtain-g.md
- [#595] [P2][M] Consumer-at-landing gate for `docs/audits/` — the subtraction mechanism · tasks/595-consumer-at-landing-gate-for-docs-audits-the-sub.md
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
- [#747] [P1][M] Adoption-by-invocation — a command file confers adoption only while telemetry records real invocations, and it decays at 30 days · tasks/747-adoption-by-invocation-command-file-confers-adoption-only-while-invoked.md
- [#748] [P1][M] A lane whose worktree resolves to the primary checkout via a `core.worktree` redirect has no isolation, and dispatch cannot see it · tasks/748-a-lane-whose-worktree-redirects-to-the-primary-has-no-isolation.md
- [#749] [P1][M] Two lanes may be dispatched for the same row under different slugs, because every duplicate check compares slugs rather than rows · tasks/749-two-lanes-may-be-dispatched-for-the-same-row-under-different-slugs.md
- [#758] [P2][S] `[#675]` target 3.2 has never been satisfiable by the `lane-integrate` walk · tasks/758-675-target-32-has-never-been-satisfiable-by-the-w.md
- [#759] [P2][S] `range_is_anchored` and `unanchored_on_spine` disagree on scope, and the 2026-09-14 instance fix does not close the class · tasks/759-range-is-anchored-and-unanchored-on-spine-disagree.md
- [#761] [P2][S] The edge-class census prices its own false positive as cheap, but paying it is an escalation class, so lanes route around the gate instead · tasks/761-the-edge-class-census-prices-its-own-false-positive.md
- [#762] [P2][S] A worktree teardown races the departing session's Stop hook, which re-creates the tree being removed — and the no-leftovers check cannot see what it leaves · tasks/762-a-worktree-teardown-races-the-departing-sessions-stop-hook.md
- [#763] [P1][S] Re-measure the batch-Z suite baseline freeze at batch close — a cause whose lane merged must have left the set · tasks/763-re-measure-the-batch-z-suite-baseline-freeze-at.md
- [#764] [P1][S] Batch Z implements the night plan of 2026-09-15 — the four transport decisions the engine refused every commit for · tasks/764-batch-z-implements-the-night-plan-of-2026-09-15.md
- [#792] [P1][L] The runtime-resource lifecycle organ: two regimes, two mechanisms, no shared thresholds · tasks/792-runtime-resource-lifecycle-two-regimes-two-mechanisms.md
- [#783] [P2][S] The carried-to-RESOLVED leg of decision-coverage has never once been exercised · tasks/783-the-carried-to-resolved-leg-of-decision-coverage-has-never-been-exercised.md
- [#768] [P1][M] A gate has one refusal channel, so a violation and an environment it could not evaluate are indistinguishable to the committer · tasks/768-a-gate-has-one-refusal-channel-so-a-violation-an.md
- [#772] [P1][M] Every dispatched lane inherits the whole secret store -- there is no introspect-and-exchange step and no row about it · tasks/772-every-dispatched-lane-inherits-the-whole-secret.md
- [#787] [P2][M] A test double for an external tool must CITE the real tool's contract for the behaviour it fakes -- a fixture nobody checked against the tool is a false-success surface · tasks/787-a-test-double-for-an-external-tool-must-cite-the.md
- [#788] [P1][M] The local maximum is not the task-id allocator under concurrency -- a sibling branch's held id is invisible from a worktree and nothing in the repo refuses it · tasks/788-the-local-maximum-is-not-the-task-id-allocator-u.md
- [#789] [P1][M] The seat boot rendered its declared model split into an HTML COMMENT while the launch line was a bare `claude` — batch Z ran 100% Opus under a header claiming otherwise · tasks/789-the-seat-boot-rendered-its-model-split-into-an-html.md
- [#802] [P1][M] The conductor emails on every push because it does not know about the frozen baseline — compare against the set, do not silence the notification · tasks/802-the-conductor-emails-on-every-push-because-it-does.md
- [#803] [P1][M] A substrate request is availability-gated and silently downgraded while reporting success — the dispatcher must verify the substrate it RECEIVED against the one it ORDERED, before briefing the lane · tasks/803-a-substrate-request-is-availability-gated-and-sile.md
- [#804] [P1][M] No committed batch manifest, no dispatch; ids come from the manifest · tasks/804-a-batch-manifest-committed-before-the-first-l.md
- [#805] [P1][M] An integrator finishes a batch unattended on recorded defaults · tasks/805-an-integrator-must-be-able-to-finish-a-batch-u.md
- [#806] [P1][M] The silent-rule ratchet has no recorded ratification path · tasks/806-the-silent-rule-ratchet-has-no-recorded-ratifi.md
- [#808] [P1][M] A hung hook wedges its session with no record; every hook needs a bound that fails OPEN loudly · tasks/808-a-hook-has-no-bounded-execution-time-so-a-hung-guard-wedges-the-session.md
- [#809] [P1][S] The lane branch grammar allows one batch letter and all 26 are spent; widen it, never recycle · tasks/809-the-lane-branch-grammar-has-one-letter-and-all-26-are-used.md
- [#810] [P1][S] The Codespace runner cannot pass a model, so model enforcement is impossible on that substrate · tasks/810-the-codespace-runner-cannot-pass-a-model.md
- [#811] [P1][S] A frozen contract can be re-issued after its pin, and a lane still boots on it -- the freeze is nominal · tasks/811-a-frozen-contract-can-be-re-issued-after-its-pin-and-a-lane-still-boots-on-it.md
- [#812] [P1][M] A figure later falsified inside an immutable artifact has no standing correction path -- the protected file keeps circulating the error · tasks/812-a-falsified-figure-in-an-immutable-artifact-has-no-standing-correction-path.md
- [#827] [P1][S] The memory floor's per-seat constant was miscalibrated in BOTH directions -- ~7x too low at first, so admission passed work the box could not run, then ~4x too high after recalibration, so it refused work it could have run · tasks/827-the-memory-floor-is-derived-from-a-stale-per-seat-constant.md
- [#819] [P1][M] A lane's hub half can merge while its win-tooling half sits unmerged, undetected · tasks/819-a-lanes-hub-half-can-merge-while-its-win-too.md
- [#820] [P2][S] A HANDBACK addressed to a seat that does not exist is an abandoned lane, not a dispatched one · tasks/820-a-handback-addressed-to-a-seat-that-does-not.md
- [#821] [P1][M] `dispatch_drift` validates the repo against one machine's local deployed state, not the repo itself · tasks/821-dispatch-drift-validates-against-one-machines.md
- [#822] [P1][S] A pipe masks the exit code of the command it wraps — a reported success is not evidence of the effect · tasks/822-a-pipe-masks-the-exit-code-of-the-command-it.md
- [#823] [P1][S] The dispatch verb still boots a lane with no committed manifest -- only /lane-boot refuses · tasks/823-the-dispatch-verb-still-boots-a-lane-with-no-committed-manifest.md
- [#824] [P1][M] No launch verb exists for a non-Claude lane, so every lane defaults to the Claude path · tasks/824-no-launch-verb-exists-for-a-non-claude-lane.md
- [#825] [P2][S] single_flight.py misreports a real push race as an internal error (exit 2), not in flight (exit 3) · tasks/825-single-flight-misreports-a-real-push-race-as-an-internal-error.md
- [#826] [P1][S] Id blocks in a batch manifest must be machine-read -- a prose block stopped nothing · tasks/826-id-blocks-must-be-machine-read-not-prose.md
- [#833] [P1][M] A seat is not a registered entity, so a wedged, starved or absent seat is invisible until a human asks · tasks/833-a-seat-is-not-a-registered-entity-so-a-wedged-starved-or-absent-seat-is-invisible.md
- [#834] [P2][S] Enforce one protocols/ rule-bearing heading with a refusal and a trip-test · tasks/834-enforce-one-protocols-heading-with-a-refusal-and-a-trip-test.md
- [#843] [P1][M] A frozen contract's premise clause is carried from a digest, not verified against main at freeze time · tasks/843-contract-freezing-premise-clauses-carry-from-a-stale-digest.md
- [#839] [P1][M] FPG-1 represents a missing target as an explicit dangling edge — the graph stops dropping the defect class it exists to catch · tasks/839-fpg-1-represents-a-missing-target-as-an-explicit.md
- [#883] [P1][M] The commit gate was never priced -- a mechanism ships with a counter of what it caught, and a gate with no catch in its window is removed, not tuned · tasks/883-a-gate-ships-with-a-counter-or-is-removed.md
- [#884] [P1][M] An unbounded research fan-out ran 17+ hours to re-answer a settled question -- a research dispatch states its agent cap, per-agent deadline and token budget before launch, and a step past its deadline is abandoned with what it has · tasks/884-a-research-dispatch-states-its-bounds-before-launch.md
- [#863] [P1][M] Hook processes are created SUSPENDED and never resumed -- a timeout cannot fire on a process that never started · tasks/863-hook-processes-are-created-suspended-and-never-resumed.md
- [#864] [P1][S] The decision-coverage gate is FLAKY -- it failed and then passed on retry with nothing changed · tasks/864-decision-coverage-gate-is-flaky.md
- [#865] [P2][S] The user-level block-onedrive.ps1 PreToolUse guard launches powershell per call and can hang the same way -- it needs a ruling · tasks/865-user-level-block-onedrive-guard-needs-a-hang-ruling.md
- [#886] [P1][M] An emergency change records its temporary debt as DATA with an owner and an expiry -- JOURNAL prose is invisible to a gate, and a MUST surface has no waiver path at all · tasks/886-an-emergency-change-records-its-temporary-debt-a.md
- [#888] [P1][M] The repo has no DEGRADED state -- an emergency that removes a required component can only lie to the gate or stop work · tasks/888-the-repo-has-no-degraded-state-an-emergency-that.md
- [#894] [P2][S] Lane ac-285 wedged after a successful tool call -- an unexplained single-lane wedge, cause unverified · tasks/894-lane-ac-285-wedged-after-a-successful-tool-call-c.md
- [#895] [P2][S] The lane-ceiling worktree leg refuses a conforming plan -- it counts the freezing seat's own worktree as a provisioned lane · tasks/895-the-lane-ceiling-worktree-leg-refuses-a-conformin.md
- [#896] [P1][S] decision_coverage -- the organ refuses correctly and its gate never fires locally (stages:[manual] behind a disabled ruleset) · tasks/896-decision-coverage-the-organ-refuses-and-its-gate-n.md
- [#891] [P1][M] Lane handback contract -- lanes write a ten-field HANDBACK-<lane>.md to the transport as their mandatory final step · tasks/891-lane-handback-contract-lanes-write-a-ten-field-h.md
- [#902] [P1][S] The night-capacity premise was false -- lane concurrency must be gated by free memory measured at dispatch, not by the hour · tasks/902-the-night-capacity-premise-was-false-lane-concur.md
- [#929] [P1][L] The spine is the whole work loop -- map every organ onto stages 1-16 and run the loop's candidate mechanisms live before anything is built · tasks/929-the-spine-is-the-whole-work-loop-map-every-organ-onto-stages-1-16-and-run-the-mechanisms-live.md
- [#930] [P1][M] Wave 3 lane A (lane-loop-declaration) -- the one file declares every moment the loop needs · tasks/930-wave-3-lane-a-lane-loop-declaration-the-one-file.md
- [#931] [P1][M] Wave 3 lane B (lane-launch-adapter) -- one command launches a lane, refuses a collision, never kills a run · tasks/931-wave-3-lane-b-lane-launch-adapter-one-command-la.md
- [#932] [P1][M] Wave 3 lane C (lane-merge-truth) -- the merge gate reads the right lane, and the census counts real callers · tasks/932-wave-3-lane-c-lane-merge-truth-the-merge-gate-re.md
- [#933] [P1][M] Wave 3 lane D (lane-end-hook) -- every finished lane reports itself, once, through a real event · tasks/933-wave-3-lane-d-lane-end-hook-every-finished-lane.md
- [#934] [P1][S] Wave 3 lane E (lane-repo-housekeeping) -- the gate reports only what is real · tasks/934-wave-3-lane-e-lane-repo-housekeeping-the-gate-re.md
- [#935] [P1][M] Wave 3 lane F (lane-connection-test) -- prove the loop is connected, end to end, with receipts · tasks/935-wave-3-lane-f-lane-connection-test-prove-the-loo.md
- [#936] [P2][S] Preflight skips an all-digit short sha -- a merge whose hash is all digits reds the pairing and passes a contract unchecked · tasks/936-preflight-skips-an-all-digit-short-sha-so-a-merge-whose-hash-is-digits-reds-the-pairing.md
- [#937] [P1][M] Wave 4a lane 1 (lane-known-reds) -- one base run per batch, so a merge takes minutes instead of an hour · tasks/937-wave-4a-lane-1-lane-known-reds-one-base-run-per-ba.md
- [#938] [P1][M] Wave 4a lane 2 (lane-merge-gates-truth) -- the merge gate reads the fates the declaration records · tasks/938-wave-4a-lane-2-lane-merge-gates-truth-the-merge-ga.md
- [#939] [P1][M] Wave 4a lane 3 (lane-batch-digest) -- the morning digest names the work, written by the machine · tasks/939-wave-4a-lane-3-lane-batch-digest-the-morning-diges.md
- [#940] [P2][M] Wave 4a lane 4 (lane-connection-hygiene) -- the connection test tells the truth, stably · tasks/940-wave-4a-lane-4-lane-connection-hygiene-the-connect.md
- [#941] [P2][M] Wave 4a lane 5 (lane-landing-decisions) -- this window's decisions leave the transport and enter the repo · tasks/941-wave-4a-lane-5-lane-landing-decisions-this-window.md
- [#942] [P2][M] State as data -- the STATUS surface, the state query, and the four escalation events · tasks/942-state-as-data-the-status-surface-the-state-query.md
- [#943] [P2][M] Contracts generated from rows -- the spine writes the skeleton, the architect writes only Done-when and decision budget · tasks/943-contracts-generated-from-rows-the-spine-writes.md
- [#944] [P3][S] The secrets field -- a contract's Dispatch block can declare a secret without leaking it to the transport · tasks/944-the-secrets-field-a-contracts-dispatch-block.md
- [#945] [P2][S] The guards decision -- the operator's build-mode answer on write guards for the loop · tasks/945-the-guards-decision-the-operators-build-mode.md
- [#946] [P2][M] The tool-trial organ and its first trials -- Caveman skill, RTK, Headroom, import-linter · tasks/946-the-tool-trial-organ-and-its-first-trials-caveman.md
- [#947] [P2][M] LiteLLM behind the stage-13 adapter -- one provider interface, not four bespoke ones · tasks/947-litellm-behind-the-stage-13-adapter-one-provider.md
- [#948] [P2][S] The fair `why` test -- measure the `why` skill without the bias its earlier trial carried · tasks/948-the-fair-why-test-measure-the-why-skill-without.md
- [#949] [P2][S] Unbind verb for the integrator seat -- releasing a batch's integrator binding is currently a no-op path · tasks/949-unbind-verb-for-the-integrator-seat-releasing-a.md
- [#950] [P3][S] Friction ratio -- measure operator touches against merged work, as a trend, not a per-batch count · tasks/950-friction-ratio-measure-operator-touches-against.md
- [#951] [P3][M] Root-cause taxonomy -- classify why a lane stops, instead of re-deriving it by hand each time · tasks/951-root-cause-taxonomy-classify-why-a-lane-stops.md
- [#952] [P3][S] Gemini routing pin -- a pinned model id for the `agy` adversarial/producer role, recorded like the other providers · tasks/952-gemini-routing-pin-a-pinned-model-id-for-the-agy.md
- [#953] [P3][M] Events that file rows -- some escalation events should produce a task row automatically, not just a STATUS entry · tasks/953-events-that-file-rows-some-escalation-events.md
- [#954] [P2][M] Install the loop in a second repo -- prove stages 1-16 are not `.dev-knowledge`-specific · tasks/954-install-the-loop-in-a-second-repo-prove-stages.md
- [#955] [P1][L] Wave 4b -- one merge path, handback as an organ, verification in the lanes (FR1-FR5) · tasks/955-wave-4b-one-merge-path-handback-as-an-organ-verification-in-the-lanes.md
- [#956] [P1][M] Wave 4b lane 0 (lane-hooks-rearm) -- the eight emergency-disabled session hooks come back on evidence · tasks/956-wave-4b-lane-0-lane-hooks-rearm-the-eight-emergency-disabled-session-hooks-come-back-on-evidence.md
- [#957] [P1][M] Wave 4b lane 1 (lane-merge-path) -- one merge path: the moment, in an integration worktree, main only when green · tasks/957-wave-4b-lane-1-lane-merge-path-one-merge-path-the-moment-in-an-integration-worktree-main-only-when-green.md
- [#958] [P1][M] Wave 4b lane 2 (lane-handback-organ) -- a lane hands back through one organ that checks it first · tasks/958-wave-4b-lane-2-lane-handback-organ-a-lane-hands-back-through-one-organ-that-checks-it-first.md
- [#959] [P1][M] Wave 4b lane 3 (lane-gate-verdicts) -- gates speak data, and the connection test reads it · tasks/959-wave-4b-lane-3-lane-gate-verdicts-gates-speak-data-and-the-connection-test-reads-it.md
- [#961] [P1][M] Wave 4b lane 5 (lane-plan-lint) -- the architect's plan is checked by code before it freezes · tasks/961-wave-4b-lane-5-lane-plan-lint-the-architects-plan-is-checked-by-code-before-it-freezes.md
- [#962] [P1][M] Wave 4b lane 6 (lane-fleet-health-split) -- sessions read fleet health; a guarded background producer makes it · tasks/962-wave-4b-lane-6-lane-fleet-health-split-a-guarded-background-producer.md
- [#963] [P1][L] State store ADR -- where the harness holds its operational state, which part is the truth, and where it executes · tasks/963-state-store-adr-where-the-harness-holds-its-operational-state-and-where-it-executes.md
- [#964] [P1][M] One verification stage -- every check runs once at merge, results reused · tasks/964-one-verification-stage-every-check-runs-once-at-merge.md
- [#965] [P1][M] One known-reds registry, read by CI and local, refreshed at the merge moment · tasks/965-one-known-reds-registry-read-by-ci-and-local-refreshed.md
- [#966] [P1][M] CI's full-suite verdict becomes the merge gate; local runs only Windows-only tests · tasks/966-cis-full-suite-verdict-becomes-the-merge-gate-local.md
- [#967] [P1][M] Test selection stops being 93% prose-triggered -- a doc-test tier, not a 58-file union · tasks/967-test-selection-stops-being-93-prose-triggered-a-doc.md
- [#968] [P1][S] `logs/MERGE-RECEIPTS.jsonl` gets an `impacted_tests.RULES` mapping before it reds every gate · tasks/968-logs-merge-receipts-jsonl-gets-an-impacted-tests-rules.md
- [#969] [P2][M] Connection walk gets JSON verdicts and a slow-tier split; the 18m59s bar comes down · tasks/969-connection-walk-gets-json-verdicts-and-a-slow-tier.md
- [#970] [P1][M] Memory admission gate: heavy runs wait for free memory; `-n` is computed, not hand-set · tasks/970-memory-admission-gate-heavy-runs-wait-for-free-memory-n.md
- [#971] [P1][M] Autonomy: pre-authorized ruling table, liveness watchdog, and a deny-and-point guard for root writes · tasks/971-autonomy-pre-authorized-ruling-table-liveness-watchdog.md
- [#972] [P2][S] Session janitor stops every poll and wake-up a lane leaves running at batch close · tasks/972-session-janitor-stops-every-poll-and-wake-up-a-lane.md
- [#973] [P1][S] Handback organ writes `HANDBACK-REFUSED-<lane>.md`, never the integrator's own `REFUSED-<lane>.md` · tasks/973-handback-organ-writes-handback-refused-lane-md-never.md
- [#974] [P1][S] One comparator: the handback organ's self-check and the integrator's call the same function · tasks/974-one-comparator-the-handback-organs-self-check-and-the.md
- [#975] [P1][M] Origin-only sync + purity check: a lane never merges a local, unverified main · tasks/975-origin-only-sync-purity-check-a-lane-never-merges-a.md
- [#976] [P1][M] Merge receipts record the merge sha and timed steps, so batch-close can name the task · tasks/976-merge-receipts-record-the-merge-sha-and-timed-steps-so.md
- [#977] [P2][S] Provider fallback list: a Sonnet outage no longer stalls every lane · tasks/977-provider-fallback-list-a-sonnet-outage-no-longer-stalls.md
- [#978] [P1][M] Transport file-kind registry, enforced by an adapter -- no more invented names or collisions · tasks/978-transport-file-kind-registry-enforced-by-an-adapter-no.md
- [#979] [P2][S] Path layer reads HARNESS_DRIVE_ROOT/HARNESS_PROMPTS_SUBDIR -- no direct env-var reads outside it · tasks/979-path-layer-reads-harness-drive-root-harness-prompts.md
- [#980] [P2][L] Portability: a path layer + Drive API adapter + container CI job removes the Codespace blocker · tasks/980-portability-a-path-layer-drive-api-adapter-container-ci.md
- [#981] [P2][L] Compute: an off-box execution host, so the laptop stops being the harness's substrate · tasks/981-compute-an-off-box-execution-host-so-the-laptop-stops.md
- [#982] [P2][S] Seat bind marks live immediately; occupancy accepts a starting record instead of exit 2 · tasks/982-seat-bind-marks-live-immediately-occupancy-accepts-a.md
- [#983] [P1][M] Decisions and audits land in the repo every wave -- a recurring step, not a one-off catch-up · tasks/983-decisions-and-audits-land-in-the-repo-every-wave-a.md
- [#984] [P1][L] A state store (ADR-121) carries decisions across a handoff instead of losing them to prose · tasks/984-a-state-store-adr-121-carries-decisions-across-a.md
- [#985] [P2][S] Plan lint rejects an audit order that carries no Codex verification step · tasks/985-plan-lint-rejects-an-audit-order-that-carries-no-codex.md
- [#986] [P1][M] Architecture-level changes require ADR + matrix + debate + operator ratification, not a fast browser accept · tasks/986-architecture-level-changes-require-adr-matrix-debate.md
- [#987] [P2][M] Batch close regenerates the ledger from the state store -- it stops going stale for days · tasks/987-batch-close-regenerates-the-ledger-from-the-state-store.md
- [#988] [P1][M] Copilot admission lands in the registry with in-repo evidence -- the router stops blocking a producer that already ran · tasks/988-copilot-admission-lands-in-the-registry-with-in-repo.md
- [#989] [P1][M] Launcher is wired to the existing provider_router -- routing stops living in prose and hard-coded models · tasks/989-launcher-is-wired-to-the-existing-provider-router.md
- [#990] [P2][M] Opus 5.5 rate row + admission A/B for the orchestrate/plan role · tasks/990-opus-5-5-rate-row-admission-a-b-for-the-orchestrate.md
- [#991] [P2][S] `/changelog-review` runs on a weekly conductor schedule instead of an operator-invoked one-off · tasks/991-changelog-review-runs-on-a-weekly-conductor-schedule.md
- [#992] [P2][S] Measure `/skill-doctor` and `/doctor`'s CLAUDE.md-trim proposal; adopt `omitClaudeMd` for bounded roles · tasks/992-measure-skill-doctor-and-doctors-claude-md-trim.md
- [#993] [P1][M] BUILD MODE exit condition 1: the connection walk is clean on main, xfail removed · tasks/993-build-mode-exit-condition-1-the-connection-walk-is.md
- [#994] [P1][L] BUILD MODE exit condition 2: one real backlog row travels row-to-merge through the whole loop · tasks/994-build-mode-exit-condition-2-one-real-backlog-row.md
- [#995] [P1][M] BUILD MODE exit condition: every disabled guard is re-armed with a live pass/fail test · tasks/995-build-mode-exit-condition-every-disabled-guard-is-re.md
- [#996] [P2][M] Every operator request becomes a row the same day it is made -- a boot-time count, target 0 · tasks/996-every-operator-request-becomes-a-row-the-same-day-it-is.md
- [#997] [P2][S] R-09-19-3: ARCHITECTURE.md KEPT ruling gets a STANDING_RULINGS entry, not just a BUILD-LIST line · tasks/997-r-09-19-3-architecture-md-kept-ruling-gets-a-standing.md
- [#998] [P2][S] R-09-19-7: lane count is by need, not a fixed 6-lane ceiling -- lands in STANDING_RULINGS · tasks/998-r-09-19-7-lane-count-is-by-need-not-a-fixed-6-lane.md
- [#999] [P2][S] R-09-19-10: 'the dispatcher dispatches' -- lands once DECLARE-NIGHT-AUTONOMY is in STANDING_RULINGS · tasks/999-r-09-19-10-the-dispatcher-dispatches-lands-once-declare.md
- [#1000] [P1][S] Doctrine 'the backbone is code; prose is intent' lands in STANDING_RULINGS · tasks/1000-doctrine-the-backbone-is-code-prose-is-intent-lands-in.md
- [#1001] [P1][M] SessionStart becomes one stdlib reader -- 8 interpreters to 1, p90 under 2s · tasks/1001-sessionstart-becomes-one-stdlib-reader-8-interpreters.md
- [#1002] [P1][S] Re-arm evidence must be measured in-session, under the real concurrent hook set, over 20+ events · tasks/1002-re-arm-evidence-must-be-measured-in-session-under-the.md
- [#1003] [P1][M] Closure proposals run once per new commit, with a reader, not once per turn · tasks/1003-closure-proposals-run-once-per-new-commit-with-a-reader.md
- [#1004] [P1][M] Commit-gate counter survives worktree teardown; '0 runs' reads UNMEASURED, not REMOVE · tasks/1004-commit-gate-counter-survives-worktree-teardown-0-runs.md
- [#1005] [P1][M] Path protection comes back as `permissions.deny` rules -- no process per PreToolUse call · tasks/1005-path-protection-comes-back-as-permissions-deny-rules-no.md
- [#1006] [P2][S] Boot banner stops printing re-armed hooks as 'DECLARED BROKEN' · tasks/1006-boot-banner-stops-printing-re-armed-hooks-as-declared.md
- [#1007] [P2][M] SessionEnd writes the seat absent record; lane-start gets its trigger · tasks/1007-sessionend-writes-the-seat-absent-record-lane-start.md
- [#1008] [P2][S] Stale-statement sweep: reconcile 6 doc claims against live hook/organ state · tasks/1008-stale-statement-sweep-reconcile-6-doc-claims-against.md
- [#1010] [P1][S] A Stop hook refuses to end a lane session without a machine `HANDBACK <branch> @ <sha> <kind>` line · tasks/1010-a-stop-hook-refuses-to-end-a-lane-session-withou.md
- [#1012] [P1][M] A dispatcher-held producer shell must run as its own session or a detached process, not a bg shell the reaper can kill · tasks/1012-a-dispatcher-held-producer-shell-must-run-as-its.md
- [#1014] [P1][M] A post-merge check runs before push, because a `--no-ff` merge commit bypasses nearly every pre-commit hook · tasks/1014-a-post-merge-check-runs-before-push-because-a-no.md
- [#1015] [P2][S] `scripts/plan_lint.py` silently reads zero ownership from a contract using only an `Owns:` label · tasks/1015-plan-lint-cannot-read-a-contract-that-uses-only-owns.md
### [S4] Extend structural validation to more governance artifacts
So that drift in transcripts, ADRs, and folders is caught cheaply, not by reviewer luck.
- [#139] [P2][L] merged-arc→record verifier · DEFER · tasks/139-merged-arc-record-verifier.md
- [#190] [P3][M] General intra-file duplication detector · DEFER · tasks/190-general-intra-file-duplication-detector.md
- [#210] [P3][S] Convert journal-wrap no-ff WARNs from per-instance disposition to a standing rule · tasks/210-convert-journal-wrap-no-ff-warns-from-per-instan.md
- [#234] [P3][S] Cross-repo probe validator · DEFER · tasks/234-cross-repo-probe-validator.md
- [#277] [P2][M] propose_closures signal repair · tasks/277-propose-closures-signal-repair.md
- [#693] [P1][M] The closure detector proposes the whole queue, its surfacing hook has been dead since the month-bucket move, and the run cap errors -- three defects that together make a closure proposal mean nothing · tasks/693-closure-detector-proposes-the-whole-queue-with-a-dead-surfacing-hook.md
- [#719] [P2][M] `ecosystem/organ-index` entries answer to no schema -- validate them against Backstage `catalog-model`'s Component shape with our own gate · tasks/719-organ-index-entries-answer-to-no-schema-validate-against-catalog-model.md
- [#767] [P2][M] A tool description is gated only where it is generated, and no surface gates its parameters at all · tasks/767-a-tool-description-is-gated-only-where-it-is-gen.md
- [#904] [P3][S] The branch-name validator rejects a recovered/ prefix -- does recovery work get a sanctioned prefix, or ride an author prefix · tasks/904-the-branch-name-validator-rejects-a-recovered-pr.md

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

> **Relocated verbatim 2026-09-16** to `docs/audits/2026-09-16-technical-backlog-view-narration-relocated.md` §1 — the [S8] Backbone epic ledger (stages 0–4, done-stage history) and the 2026-07-07 FLAG on #168/#170 co-sequencing with #239/#240.

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
- [#793] [P1][M] A withdrawn lane's live worktree built a rival organ · tasks/793-a-withdrawn-lane-contract-left-a-live-worktree-bu.md
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

- [#791] [P1][M] Carry intake 101 — the runtime-resource organ — through the decision engine to a ratified ADR · tasks/791-carry-intake-101-the-runtime-resource-organ-throug.md
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
- [#897] [P2][S] ARCHITECTURE.md is 110,357 B live, about seven times its 15 KB target -- and its down-22-percent figure pointed the wrong way across five surfaces · tasks/897-architecture-md-is-110-357-b-live-seven-times-its.md
- [#903] [P2][M] The audit corpus has no retention rule -- what is an audit for after its arc closes, and what retires it · tasks/903-the-audit-corpus-has-no-retention-rule-what-is-a.md
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
- [#766] [P2][M] The session boot payload has a byte budget on one file and none on the whole -- every tool, command and skill description is paid at startup · tasks/766-the-session-boot-payload-has-a-byte-budget-on-on.md
- [#807] [P2][S] The backlog-shrink instrument was aimed at the wrong corpus: `archive_row_body` relocates task-file bodies, the view renders manifest prose · tasks/807-the-backlog-shrink-instrument-was-aimed-at-row-bodies.md
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
- [#588] [P1][S] P-2 — build the spine parent-map in ONE git process · tasks/588-p-2-build-the-spine-parent-map-in-one-git-proces.md
- [#593] [P2][M] Codespaces chain repair, hub half — uv in the image and a prebuild that actually refreshes · tasks/593-codespaces-chain-repair-hub-half-uv-in-the-image.md
- [#594] [P3][M] Layer-3 router — the HUB prerequisites only, not the verb itself · tasks/594-layer-3-router-the-hub-prerequisites-only-not-th.md
- [#598] [P3][S] P-6 — a slow-marker selector so tiered gating has something to select on · tasks/598-p-6-a-slow-marker-selector-so-tiered-gating-has.md
- [#618] [P2][M] The silently-stale codespace clone — detection and refresh-on-entry, not a rebuild · tasks/618-the-silently-stale-codespace-clone-detection-and.md
- [#623] [P2][S] Mechanize the JOURNAL anchor record-line — 719 anchored-by-mention WARNs is a signal-to-noise defect · tasks/623-mechanize-the-journal-anchor-record-line.md
- [#625] [P1][M] The rule-adherence eval corpus — a FRESH corpus, because neither fold target can carry it · tasks/625-the-rule-adherence-eval-corpus-fresh.md
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
- [#906] [P1][M] The primary checkout has no single writer -- two sessions committed on it concurrently during the batch AC close, and nothing refused either · tasks/906-the-primary-checkout-has-no-single-writer-two-ses.md
- [#724] [P1][M] The Windows baseline is permanently RED and its count is not even reliably knowable -- a red baseline hides every new failure behind it · tasks/724-permanently-red-windows-test-baseline-hides-every-new-failure.md
- [#725] [P2][S] `test_manifest_link_route` fails under xdist on a frozenset identity assert -- a test that passes alone and fails in parallel · tasks/725-xdist-frozenset-identity-pollution-in-test-manifest-link-route.md
- [#728] [P2][M] Every organ that answers a question gets a generated skill whose description says WHEN to invoke it -- the description is what the model matches · tasks/728-organ-skills-generated-from-the-organ-index-so-the-model-can-find-them.md
- [#729] [P2][M] FPG-1's queries are shell scripts the model must remember to run -- expose them as MCP tools so they sit in the tool list beside Grep · tasks/729-fpg1-queries-exposed-as-mcp-tools-so-they-sit-beside-grep.md
- [#746] [P1][M] Devcontainer history-sufficiency (B1) and ecosystem-registration (L5) repair, lost with `scripts/cloud_provisioning.py` · tasks/746-devcontainer-history-and-ecosystem-repair-lost-with-cloud-provisioning-py.md
- [#769] [P2][S] An unattended lane has no cancel for a long-running gate -- the only lever is killing the session · tasks/769-an-unattended-lane-has-no-cancel-for-a-long-runn.md
- [#771] [P2][S] `[#729]` carries no protocol-conformance criterion, so a server can satisfy it completely and not be an MCP server · tasks/771-729-carries-no-protocol-conformance-criterion-so.md
- [#800] [P1][S] The routing unit is the SESSION, not the turn — the prompt cache is per model, so per-turn switching loses money · tasks/800-the-routing-unit-is-the-session-not-the-turn-the-p.md
- [#801] [P2][S] Opus is a flat 2.50x Sonnet on every leg — a false 5x figure circulated and a token-shape argument was built on it · tasks/801-opus-is-a-flat-2-50x-sonnet-and-a-false-5x-figure.md
- [#893] [P1][S] Lane cost is computable and nothing computes it at integration -- batch AC's close packet reads cost UNKNOWN · tasks/893-lane-cost-is-computable-and-nothing-computes-it-at.md
- [#907] [P1][S] Spend is not measured by seat kind, so cost work targets the lanes while the money is in the seats · tasks/907-spend-is-not-measured-by-seat-kind-so-cost-work-t.md
- [#908] [P1][M] A token budget written in a prompt caps nothing -- enforce a hard cap where the agent is launched · tasks/908-a-token-budget-written-in-a-prompt-caps-nothing-en.md
- [#909] [P1][M] Read-only analysis burns the Claude budget while free and cheap capacity sits unused -- route it off first · tasks/909-read-only-analysis-burns-the-claude-budget-while-f.md
- [#910] [P1][S] A seat below ~10% context must not begin an integration walk -- retire and boot fresh · tasks/910-a-seat-below-10-percent-context-must-not-begin-an-in.md
- [#911] [P1][S] A gate whose precondition is passing that same gate -- the silent-rule ratchet cannot accept an operator-approved raise until the raise is already pushed · tasks/911-a-gate-whose-precondition-is-passing-that-same-gat.md
- [#912] [P1][M] main is RED on its own -- 45 live-state tests fail independently of every lane merged in night wave 2, with no owner · tasks/912-main-is-red-on-its-own-45-live-state-tests-fail-i.md
- [#913] [P2][S] Duplicate JOURNAL day-letter 2026-09-18 (f) is on main -- audit journal_day_letters FAILs · tasks/913-duplicate-journal-day-letter-2026-09-18-f-is-on-ma.md
- [#914] [P1][M] The transport is unreachable whenever H: is not mounted -- a post-hook must deliver to-browser artifacts regardless of mount, and refuse loudly instead of reporting success after writing to Downloads · tasks/914-the-transport-is-unreachable-whenever-h-is-not-mo.md
- [#915] [P1][M] AM-5's premise is falsified -- a --bg lane launched from inside a session DOES get its own Agent View row, on the host, twice · tasks/915-am-5-s-premise-is-falsified-a-session-launched-bg.md
- [#916] [P1][M] A lane deleted another lane's LIVE worktree -- the harness lock refuses remove, and was defeated by an explicit unlock · tasks/916-a-lane-deleted-another-lane-s-live-worktree-the-lo.md
- [#917] [P2][S] Our own docs are wrong about the worktree lock -- a locked remove is a loud fatal (exit 128), not a silent no-op · tasks/917-our-own-docs-are-wrong-about-the-worktree-lock-rem.md
- [#918] [P2][M] The seat registry is Stop-only -- it learns about a seat when it ends, so it cannot answer "is this seat live" · tasks/918-the-seat-registry-is-stop-only-it-cannot-answer-is.md
- [#919] [P2][M] The token cap is POLLED, not enforced -- a stop-loss, not a limit: witness A overshot 5.5x before the first poll acted · tasks/919-the-token-cap-is-polled-not-enforced-a-stop-loss-n.md
- [#920] [P1][M] PLAYBOOK Ch8 now describes the OLD dispatch surface -- the sole literal-command site yields wrong syntax to every correct citation · tasks/920-playbook-ch8-now-describes-the-old-dispatch-surfac.md
- [#921] [P1][M] Accumulated gate debt is seen only by the handoff cut -- 11 hard-fails and 272 unruled WARNs built up in one day of merging and nothing surfaced them · tasks/921-accumulated-gate-debt-is-seen-only-by-the-handoff-cut.md
- [#922] [P2][S] Spine stage 7 (substrate) is invoked without its required paths argument -- exit 2, and this is where the spine now stops · tasks/922-spine-stage-7-substrate-is-invoked-without-its-requ.md
- [#923] [P2][M] The distiller design rests on the hookmap answer -- UserPromptSubmit CAN inject, but whether a LONG injected description is used is untested · tasks/923-the-distiller-design-rests-on-the-hookmap-answer-u.md
- [#924] [P2][S] Does a fresh session call /why unprompted? Bar >= 3/5 -- the first measurement scored 0/5 with command registration alone · tasks/924-does-a-fresh-session-call-why-unprompted-bar-3-5-t.md
- [#925] [P2][S] The B2 calibration's per-row read-set target (<= ~60 KB including the boot base) has no owning row and no measurement against it · tasks/925-the-b2-calibration-s-per-row-read-set-target-has-n.md
- [#926] [P1][M] A gate that cannot recognise the only correction its own invariants permit -- journal_day_letters and substrate_declaration refuse forever by construction · tasks/926-a-gate-that-cannot-recognise-the-only-correction-i.md
- [#927] [P1][S] User-level disableAllHooks: true has disarmed block-onedrive.ps1 since 2026-09-17 -- the P0 OneDrive zone rests on rules alone, uncommitted and outliving its emergency · tasks/927-user-level-disableallhooks-true-has-disarmed-block.md
- [#928] [P1][S] The parity schema cannot express a time-bounded expectation -- settings-deny-and-point INVERSE encodes BUILD-MODE rule 8, which expires 2026-11-18, and nothing will flag it · tasks/928-the-parity-schema-cannot-express-a-time-bounded-ex.md
- [#898] [P2][S] A contracted cloud read-only leg never dispatched and a local substitute committed what the contract forbade -- a dispatcher shape defect · tasks/898-a-contracted-cloud-read-only-leg-never-dispatched.md
- [#899] [P3][S] gen_audit_index reads HEAD, not the working tree -- every new audit costs a second, index-only commit and --check is falsely green before it · tasks/899-gen-audit-index-reads-head-so-every-new-audit-cos.md
- [#900] [P2][S] AX9-5's own organ miscounts -- from a worktree it reads one session, its totals ignore the window, and a path mention counts as a call · tasks/900-ax9-5-s-own-organ-miscounts-from-a-worktree-and-t.md
- [#889] [P1][M] The next window's acceptance test has no row -- one lane end to end, dispatch to merged, under one hour, nothing wedged, no human decision in the middle · tasks/889-lane-acceptance-test.md
- [#1009] [P1][S] Wave 5a lane 2 (lane-test-selection) -- prose stops pulling in the whole live_repo test set · tasks/1009-wave-5a-lane-2-lane-test-selection-prose-stops-pulling-in-the-whole-live-repo-test-set.md
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
- [#832] [P3][M] Re-run the three-repo comparison against the operator's named repositories · tasks/832-copilot-collections-comparison-rerun.md
- [#885] [P1][M] The model a contract declares is the model that RUNS — resolved at freeze, verified off the transcript, refused on the receipt, with the default by lane kind in the generator · tasks/885-the-model-a-contract-declares-is-the-model-that-r.md

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
- [#892] [P2][S] A seat ordered sonnet ran Opus and nothing refused -- ordered is not ran for an attended seat · tasks/892-a-seat-ordered-sonnet-ran-opus-and-nothing-refus.md
- [#890] [P2][M] Per-task execution-state carrier is one of the five intakes still owed -- Phase 1 must reconcile what [#664], tasks/ frontmatter, manifest.json, FPG-1 and the organ index already hold before anything new is built · tasks/890-per-task-execution-state-carrier.md
- [#901] [P2][S] Does [#790]'s runtime-resource organ increment exist on main today, superseded, or nowhere -- intake [#101] still says runtime resources have no owning organ · tasks/901-does-790-s-runtime-resource-increment-exist-anywh.md
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

> **Relocated verbatim 2026-09-16** to `docs/audits/2026-09-16-technical-backlog-view-narration-relocated.md` §2 — [E8] basis: why the plan lives in the backlog, the accretion discipline for filing wave tasks, and its source bundle.

> **Relocated verbatim 2026-09-16** to `docs/audits/2026-09-16-technical-backlog-view-narration-relocated.md` §3 — [E8] Wave map W1–W7, the ARC-5 plan of record (unchanged since 2026-07-28; its carried work is ticketed under [S21] and [S22] below).

> **Relocated verbatim 2026-09-16** to `docs/audits/2026-09-16-technical-backlog-view-narration-relocated.md` §4 — [E8] Seedless waves: W1 and W4 carry no seed, and seeds 5 and 6 map to W2 and W5 by content.

> **Relocated verbatim 2026-09-16** to `docs/audits/2026-09-16-technical-backlog-view-narration-relocated.md` §5 — [E8] Closure contract (frozen, verbatim) and the clause (b) rulings F1 and D1 — ARC-5 closes only on clauses (a)–(f) as recorded there.

> **Relocated verbatim 2026-09-16** to `docs/audits/2026-09-16-technical-backlog-view-narration-relocated.md` §6 — [E8] Metric definition — the declaration test governing closure clause (b), and its `bf49cbf9` baseline (N_silent 176); read it before acting on #357.

> **Relocated verbatim 2026-09-16** to `docs/audits/2026-09-16-technical-backlog-view-narration-relocated.md` §7 — [E8] DECISIONS dispositioned 2026-07-26 — the R1–R8 / R1b / R12 table and its reconciliation-debt list (#389; W3, W4, W6, W7 wording).

> **BINDING — do NOT relitigate** (relocated verbatim 2026-09-16 to `docs/audits/2026-09-16-technical-backlog-view-narration-relocated.md` §8): the ARC-4 rulings, terra's seven corrections, sol's four mechanism upgrades and every CONSIDERED + REJECTED and DO-NOT-REDO item recorded there stand, and every ARC-5 wave still requires a frozen acceptance contract before delegation, a Codex terra review before merge, RULING-W for any consumer write, replication material over one-off fixes, an educate artifact with file-level before→after, and one merged arc per wave.

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

> **Relocated verbatim 2026-09-16** to `docs/audits/2026-09-16-technical-backlog-view-narration-relocated.md` §9 — [S24] completion notice (#382 and #459 closed; the heading is retained, retire-not-delete).

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
- [#770] [P2][M] Nothing notices an external specification revising under us, and `[#729]` proposes to build on one · tasks/770-nothing-notices-an-external-specification-revisi.md

---

**About this file** — open `.dev-knowledge` work as a story map (ADR-66): Big Picture → Theme → User Story → Task. Stories are human (goal + `So that`); tasks carry `[#id] [P][size] · Done when · refs`. Done tasks **leave** (ADR-65); git is the implementation record (`git log --grep 'closes \[#'`). Child-repo execution items live in `docs/audits/2026-06-01-child-repo-relocation-proposal.md`. Schema: PLAYBOOK §10; machine-checked by `scripts/validate_backlog.py`.

> **Relocated verbatim 2026-09-16** to `docs/audits/2026-09-16-technical-backlog-view-narration-relocated.md` §10 — ai-council audit residuals — a 2026-07-06 pointer to ai-council-owned cleanups, filed in that repo per ADR-41.

**Grooming log:** git history + JOURNAL. Recent: 2026-06-12 (#149 flip) · 2026-06-18 (currency pass) · 2026-06-25 (groom pass, n=2: 84→81) · 2026-07-08 (leg-c full ruling pass, operator-ratified, 124→74: 14 KILL / 27 MERGE / 2 MOVE / 9 CLOSE / 5 RE-SCOPE / 19 DEFER-peg / 2 new filings #289 #290; #110 #128 moved-to: ai-council (Wave-1)) · 2026-07-30 (per-handoff lightweight groom, arc 0731-g0-groom: 6 doc_rot accretion rows condensed — #344 #421 #422 #332 #278 #426, no live obligation dropped; 5 warn-doc-rot dispositions retired; ADR-105 night-batch routine activated on #426). · 2026-09-14 (mechanised groom, lane `lane-y-754-backlog-to-bar`: the `archive_row_body.py` trigger run to EXHAUSTION over the rows above the 1320-char ceiling — 60 rows, 66 clauses, 18,107 source chars relocated byte-identically into `tasks/archive/`, 84 records re-proven on legs A–E; accretion arm 5 → 4, #241 cleared; over-ceiling COUNT unmoved at 148 of 322 and `propose` now returns one row, itself already under the ceiling — the mechanism is exhausted above the line, measured rather than asserted, and the residual is 35.3% structural clauses plus 38.2% undated prose, both outside the predicate by construction). Next quarterly: 2026-10-08.