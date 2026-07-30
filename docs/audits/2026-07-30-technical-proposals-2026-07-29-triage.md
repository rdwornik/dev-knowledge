---
class: technical
date: 2026-07-30
slug: proposals-2026-07-29-triage
Status: "UNVERIFIED-UNTIL-LOCAL — INPUT, NOT AUTHORITY"
producer: claude-code-night-batch
lane: claude/night-2026-07-30-boot-prep
anchor_sha: c8490c1d
consumer: incoming 2026-07-31 dev-knowledge architect boot
consumption_path: "branch -> local re-verification -> architect reads at boot"
scope: "read-only classification of logs/PROPOSALS-2026-07-29.md WEAK rows; propose_closures.py NOT run, nothing closed"
---

> **Status: UNVERIFIED-UNTIL-LOCAL. INPUT, NOT AUTHORITY.** Cloud night-batch lane: no merge, no
> canon edit, no closure, no ruling. `scripts/propose_closures.py` was **not** run and no BACKLOG
> row was touched. Classification only — every disposition here is a proposal for the architect.

# W4 proposals triage -- logs/PROPOSALS-2026-07-29.md WEAK section

UNVERIFIED-UNTIL-LOCAL

input_file: logs/PROPOSALS-2026-07-29.md
input_file_last_commit_sha: 69d49b93 (frontmatter head_commit; file itself untouched since, per `git log -1 --format=%h -- logs/PROPOSALS-2026-07-29.md`)
repo_branch: claude/night-2026-07-30-boot-prep
proposals_total_parsed: 132
proposals_expected_by_brief: 133

## Count discrepancy (133 vs 132)

The file contains exactly 132 top-level `- [ ] **#NNN**` WEAK entries (verified twice: 
`grep -c '^- \[ \] \*\*#'` and a manual walk of every header line). There is no 133rd entry.
The only place a 133rd id-like token appears is inside proposal #139's own body, which parenthetically
aliases itself as "a.k.a. **#90b**" -- that is prose inside #139, not a separate bulleted proposal, and
it does not increment the count. I did not find a `count:` field in the frontmatter or any other place
in the file asserting 133. Reporting the real number: 132 parsed, 132 accounted for below.

## Method actually used

1. Extracted every proposal id + one-line subject (132/132).
2. Cross-checked every id against the live `BACKLOG.md` -- result: **all 132 ids are still present and
   open in BACKLOG.md** (`grep '\[#N\]' BACKLOG.md` hit for every single one).
3. Because BACKLOG.md is a GENERATED file (ADR-107 strangler; "Source of truth: tasks/"), I went
   one level deeper and read the `status:` frontmatter field directly in `tasks/<id>-*.md` for a spot
   sample (#244, #282) -- both `status: open`, confirming BACKLOG.md is not merely stale.
4. Extracted the `Done when:` clause for all 132 tasks from BACKLOG.md (the actual closure contract).
5. For every proposal, tallied which file(s) its evidence commits touch and how many evidence lines
   it carries. The dominant pattern: proposals citing `protocols/PLAYBOOK.md`, `scripts/audit.py`,
   `ecosystem/disposition-register.yaml`, `docs/decisions/README.md`, `docs/audits/README.md`,
   `deploy/manifest-v*.yaml` carry 30-100+ evidence lines apiece, almost none of which relate to the
   proposal's own specific scope -- they are commits closing OTHER tickets that happened to touch a
   large shared canonical file. This is the exact near-zero-precision signature #277 itself names.
6. Ran targeted verification against live code/config for the ~12 proposals whose Done-when looked
   most checkable (a narrow file, a specific function, a specific regex, a specific config line):
   - #334 (ruff id migration): `.pre-commit-config.yaml` still has `id: ruff`, not `ruff-check` -> open
   - #396 (extract scripts/gitenv.py): file does not exist -> open
   - #369 (wire boundary_headers.py --check into pre-commit): no such hook in `.pre-commit-config.yaml` -> open
   - #218 (safe_remove.py M2/M3): no M2/M3 code found in scripts/safe_remove.py -> open
   - #294 (validate_backlog.py --path arg): no such CLI arg exists -> open
   - #421 (dotfile tokenizer fix): `_FILE_RE` in scripts/verify_handoff_probes.py:54 is unchanged, still
     excludes a leading dot on the final path segment -> open, bug still live
   - #424 (bare depends-on id parsing): `_DEPID_RE = re.compile(r"#(\d+)")` in validate_backlog.py
     still requires the `#` -> open, defect still live
   - #317 (parallel-by-default pytest): pyproject.toml addopts do not default to `-n auto` -> open
7. Went one further step on the single most promising-looking candidate in the whole file, #213
   (PLAYBOOK condensation), whose evidence includes a commit literally titled "Group F -- rule-
   inventory diff + pointer-integrity finalize [#213]" with commit body "Closure artifact for the
   SEAL-1a condensation arc" (`ef2c32dea`, 2026-06-26). Checked the actual outcome: that commit trimmed
   PLAYBOOK.md from 3410 to 3386 lines (-24) and was explicitly "NOT merged" pending operator review.
   The task's Done-when target was "honest landing ~2600-2950" lines; PLAYBOOK.md is **3950 lines
   today** (grew, did not shrink). #213 is genuinely open -- the SEAL-1a arc was a small, real, but
   partial pass that did not discharge the ticket. This is the report's cautionary case: the best-
   looking evidence in the whole corpus still does not survive a direct check.

## Summary counts

```
plausibly-closable: 0
noise:              124
needs-ruling:       8
cannot-classify:    0
total:              132
```

Headline finding: **zero of the 132 WEAK proposals are plausibly-closable.** Every single one of the
132 ids is confirmed `status: open` in its own `tasks/<id>-*.md` file (the ADR-107 source of truth),
and for every proposal whose Done-when named a checkable code artifact, the artifact does not exist
or the described behavior is unchanged. This matches proposal #277's own diagnosis in this same file
(2026-07-07 run: 49 proposed, 0 valid) almost exactly -- the WEAK heuristic fires on file-churn, and
the files it keys on (PLAYBOOK.md, audit.py, disposition-register.yaml, decisions/README.md,
audits/README.md, deploy manifests) are edited on nearly every arc by construction.

## Bucket 1: plausibly-closable (0 items)

None. No proposal in this WEAK batch survived a direct evidence check. See method step 7 (#213) for
the closest near-miss, which still failed verification.

## Bucket 2: needs-ruling (8 items)

These are cases where the task's Done-when is satisfied purely by an **operator/architect decision**
(no code or test involved), and I could not confirm from git history/file evidence whether that
decision has already been made and simply never reflected back onto the task. Flat-out calling these
"noise" would overclaim; they are open tasks whose true state depends on operator memory I cannot audit.

```
proposal | backlog_id | subject | ruling_question
#162 | #162 | [P2][M] Vocab decision (architect-session): disambiguate "architect" as the Layer-1 **actor** (ARCHITECTURE.md | Has the architect vs handoff-mode 'architect' vocabulary collision been formally disambiguated anywhere (ADR or ruling) since this was filed? No ADR/ruling evidence found in the proposal's own evidence list.
#283 | #283 | [P3][S] corp-monorepo `hybrid_classifier.json` 1.08MB duplication — byte-identical file in `models/` + `src/co | Was the corp-monorepo hybrid_classifier.json de-dup decision made in a corp-monorepo product session (out of hub scope, per the task's own text)? Hub git history cannot answer this -- needs an operator check of the corp-monorepo repo/session record.
#308 | #308 | [P3][S] Decide the `verify` skill's canonical home (#9 self-flagged open question), pegged to P6 — the hub `.c | Has the .claude/skills/verify canonical-home question (hub-local vs floor/plugin-distributed) been decided since its P6 peg (#221) closed with no successor? The task is now an orphaned peg -- does it need a new peg, or was it quietly settled?
#320 | #320 | [P2][S] Fleet backup posture — three repos hold unpushed work on one disk: corp-ops `main` 4 ahead of `origin/ | Have corp-ops / corp-sca-time-automation / demo-prep pushed their outstanding local commits to origin/main, or was accept-local recorded? This is live state in three OTHER repos the hub cannot see from here -- needs operator confirmation, not a hub-side code check.
#323 | #323 | [P3][S] Design question: add `codemap-generate`/`toc-generate` to the carried `hub_hooks` install list? — a de | Was the codemap-generate/toc-generate hub_hooks carry decision (#319 follow-on) made and simply not looped back to this ticket?
#331 | #331 | [P2][S] Consumer BACKLOG schema adoption ruling — rule whether ai-council + corp-monorepo adopt the hub E-pref | Has an operator ruling on ai-council/corp-monorepo BACKLOG-schema adoption (adopt-at-P6 vs accept-durable, per consumer) been recorded since 2026-07-11? No ADR/JOURNAL evidence of this specific ruling turned up in the proposal's evidence list.
#420 | #420 | [P3][S] **Does a TOP-LEVEL `docs/archive/` still make sense?** — operator-raised structural question, filing o | Has the top-level docs/archive/ fate (kept-with-restated-charter vs dissolved into per-area homes) been ruled? Explicitly still an open operator-raised structural question per the task text; no resolution evidence found.
#443 | #443 | [P3][S] **Planning artifacts outside the three enforced classes carry no rent rule** — "meta serves object" (N | Do handoff bundles / session plans / audit docs need a stated rent/binding rule, or are they to be recorded as deliberately un-ruled? The task text already treats this as unresolved (there is no open-ended third option) -- genuinely awaiting an architect call, not evidence.
```

## Bucket 3: noise (124 items)

The decisive evidence for every row here is the same and was checked directly, not inferred: each id is
confirmed `status: open` in its own `tasks/<id>-*.md` (the ADR-107 source of truth) with an unmet
Done-when, and the ~12 spot-checked against live code/config (method step 6) all came back unimplemented.
The `reason` column adds supplementary context -- which file(s) the WEAK heuristic's evidence keyed on.
For most rows (PLAYBOOK.md, audit.py, disposition-register.yaml, docs/decisions/README.md,
docs/audits/README.md, deploy manifests dominating with 30-100+ hits) this is the classic [#277]
near-zero-precision file-churn signature: a large canonical file edited by many unrelated arcs. A smaller
set of rows key on a narrower, more topically-relevant file (e.g. #430 on scripts/fleet_parity.py x14,
#440 on scripts/gen_task_tree.py x17) -- for those the evidence is more plausibly *related* work, but the
status:open + unmet-Done-when check still rules out closure; I did not individually re-verify each such
narrow-file row's specific Done-when clause against code beyond the ~12 sampled in step 6, so treat the
"related-but-unclosed" framing there as somewhat less exhaustively checked than the churn rows.

```
proposal | backlog_id | subject | reason (dominant evidence files; see note above on churn vs narrow-file rows)
#43 | #43 | [P3][L] Decide + (if yes) author a one-step new-repo scaffold (ADR + templates/new-repo-skeleton/, no scripts) | n=3 evidence lines, dominated by: docs/intake/2026-07-08-func-new-project-bootstrap.md(x3)
#132 | #132 | [P2][M] Organ-index generator — `scripts/generate_organ_index.py` (read-only, codemap/toc pattern — Layer-2-sa | n=1 evidence lines, dominated by: docs/audits/2026-06-07-copilot-collections-peer-audit-v2.md(x1)
#139 | #139 | [P2][L] merged-arc→record verifier (a.k.a. **#90b** — direction (b), deferred from #90 which shipped direction | n=4 evidence lines, dominated by: scripts/validate_git_backlog.py(x4)
#169 | #169 | [P3][M] Ungated-doc staleness detection (ADR-85 R2) — surface ARCHITECTURE/VISION/LESSONS/CONTRIBUTING stalene | n=6 evidence lines, dominated by: scripts/fleet_health.py(x3), docs/decisions/ADR-85-session-lifecycle-enforcement.md(x3)
#170 | #170 | [P3][M] Design + land the traceability-spine ADR (issue-ID↔commit anchor) that #168 depends on — the airtight, | n=3 evidence lines, dominated by: docs/decisions/ADR-85-session-lifecycle-enforcement.md(x3)
#171 | #171 | [P3][M] Build the conformance dashboard at `ecosystem/conformance.md` (ADR-86 / ADR-85 R2) — a read-only valid | n=1 evidence lines, dominated by: docs/decisions/ADR-86-conformance-dashboard-location.md(x1)
#181 | #181 | [P2][S] Coherence v2 nudge-response — decide escape-hatch vs deferred-hash vs promote-nudge-to-gate for the fo | n=2 evidence lines, dominated by: docs/handoffs/2026-06-17-dev-knowledge-architect-2/SUPPLEMENT.md(x2)
#210 | #210 | [P3][S] Convert journal-wrap no-ff WARNs from per-instance disposition to a standing rule — 3 instances of one | n=28 evidence lines, dominated by: ecosystem/disposition-register.yaml(x25), scripts/validate_no_ff.py(x3)
#213 | #213 | [P2][L] PLAYBOOK rule/history condensation — separate rule from rationale/history across protocols/PLAYBOOK.md | n=105 evidence lines, dominated by: protocols/PLAYBOOK.md(x105)
#215 | #215 | [P2][M] Onboard + verify methodology in a new repo — a consolidated runbook to deploy the methodology into a f | n=2 evidence lines, dominated by: protocols/REPO_ONBOARDING.md(x2)
#218 | #218 | [P3][M] Safe-removal gate M2+M3 boundary (the deferred phases of #195) — extend the code→code (M1) safe-remova | n=3 evidence lines, dominated by: scripts/safe_remove.py(x2), docs/audits/2026-06-20-removal-closure-spike-findings.md(x1)
#231 | #231 | [P3][M] Consumer → hub feedback report — when a consumer session detects a methodology gap, ambiguity, or brok | n=124 evidence lines, dominated by: protocols/PLAYBOOK.md(x105), protocols/ESSENTIALS.md(x19)
#234 | #234 | [P3][S] Cross-repo probe validator — give `.claude/` target paths full FAIL teeth — the #163 handoff-probe val | n=81 evidence lines, dominated by: scripts/audit.py(x69), scripts/verify_handoff_probes.py(x12)
#239 | #239 | [P3][M] Follow-up — extend the Informant Organ Tier-2 beyond the 4 deploy manifest carriers to skills / comman | n=13 evidence lines, dominated by: scripts/enforcement_coverage.py(x7), deploy/manifest-v1.0.0.yaml(x6)
#240 | #240 | [P3][S] Follow-up — Stage-3 audit-leg regression teeth: `check_enforcement_coverage` emits WARN on an `enforci | n=76 evidence lines, dominated by: scripts/audit.py(x69), scripts/enforcement_coverage.py(x7)
#241 | #241 | [P2][S] Undeclared-edge groom — adjudicate the 6 tier-1 candidates the newly-wired `undeclared_edges` ship-gat | n=96 evidence lines, dominated by: scripts/audit.py(x69), ecosystem/disposition-register.yaml(x25), scripts/scan_undeclared_edges.py(x2)
#242 | #242 | [P2][M] ADR status-flip coherence check — the ratified go-forward status-flip pattern (ADR-94, Accepted 2026-0 | n=52 evidence lines, dominated by: docs/decisions/README.md(x52)
#244 | #244 | [P2][L] Essence-spec lifecycle epic — P1 SHIPPED (feat/essence-spec-p1: manifest-v1.1.0 grew `anchors:`/`compo | n=8 evidence lines, dominated by: deploy/manifest-v1.1.0.yaml(x4), deploy/release_lint.py(x4)
#245 | #245 | [P2][M] Add-path status-awareness — the deploy add-path (`deploy/tool.py` execute + each carrier `apply`) is b | n=13 evidence lines, dominated by: deploy/tool.py(x11), deploy/contract.py(x2)
#263 | #263 | [P3][S] Protocols/edge-map reconciliation residuals (ADR-51 amendment) — groom the residuals Epic-4's EPIC_RET | n=125 evidence lines, dominated by: protocols/PLAYBOOK.md(x105), ecosystem/doc-code-edge.yaml(x15), protocols/AI_COUNCIL_PROCESS.md(x5)
#266 | #266 | [P3][S] Codify the test-scoped-grant language lesson (E4-1 precedent) — Wave-2 ratified (2026-07-05): a NARROW | n=26 evidence lines, dominated by: tests/test_doc_code_edge.py(x26)
#267 | #267 | [P2][S] Scope-exercising arc extension (REFINEMENT, root-ratified 2026-07-06 — not a closure gate; armed-as-en | n=24 evidence lines, dominated by: deploy/lived_sandbox/arc.py(x12), deploy/manifest-v1.2.0.yaml(x11), docs/audits/2026-07-06-ai-council-measurement-3.md(x1)
#269 | #269 | [P3][S] Audit-index count-tiered shape + freshness hook (ADR-100 Q2) — apply the ADR-100 count-tiered shape to | n=96 evidence lines, dominated by: docs/audits/README.md(x94), docs/audits/2026-07-08-fleet-consistency-census.md(x1), scripts/gen_audit_index.py(x1)
#270 | #270 | [P1][M] Operator-load gauge — the gating FIRST element of any Tier-2 nightly layer (standing operator ruling;  | n=5 evidence lines, dominated by: scripts/fleet_health.py(x3), docs/audits/2026-07-05-draft-tier2-nightly-layer.md(x1), docs/audits/2026-07-04-fable-architecture-review.md(x1)
#271 | #271 | [P3][L] Nightly proposal loop — revive the Tier-2 draft ONLY under intake brief #1 §6 constraints (carried ex- | n=2 evidence lines, dominated by: docs/intake/archive/2026-07-06-functional-architect-nightly-loop.md(x1), docs/audits/2026-07-05-draft-tier2-nightly-layer.md(x1)
#273 | #273 | [P3][S] Changelog-review staleness escalation (intake doc #2 R3) — the SessionStart sentinel nudges, but a mon | n=8 evidence lines, dominated by: ecosystem/tool-versions.yaml(x4), scripts/fleet_health.py(x3), docs/intake/archive/2026-07-06-platform-feature-scan.md(x1)
#274 | #274 | [P3][S] Dogfood-signal prior in the /changelog-review ADOPT rubric (intake doc #2 R4) — features Anthropic shi | n=4 evidence lines, dominated by: .claude/commands/changelog-review.md(x3), docs/intake/archive/2026-07-06-platform-feature-scan.md(x1)
#276 | #276 | [P2][M] D2 per-consumer waiver-honoring — a `.methodology.yaml` divergence-allowlist the deploy tool actually  | n=16 evidence lines, dominated by: deploy/tool.py(x11), deploy/carrier_precommit.py(x5)
#277 | #277 | [P2][M] propose_closures signal repair — the 2026-07-07 /review-closures run proposed 49 items, 0 valid (a 49: | n=7 evidence lines, dominated by: scripts/propose_closures.py(x4), plugins/tier1-lifecycle/scripts/propose_closures.py(x3)
#278 | #278 | [P2][M] Test-suite hygiene epic (consumes intake-id 3) — theatricality review of the pytest corpus (find tests | n=71 evidence lines, dominated by: scripts/audit.py(x69), docs/intake/archive/2026-07-07-test-suite-hygiene.md(x1), docs/audits/2026-07-08-fleet-consistency-census.md(x1)
#280 | #280 | [P3][S] Propagate the intake area to greenfield consumers via the deploy manifest — `docs/intake/` + `template | n=43 evidence lines, dominated by: docs/intake/README.md(x24), deploy/manifest-v1.2.0.yaml(x11), templates/intake-template.md(x4)
#281 | #281 | [P2][S] Re-peg the ai-council ADR-66 story-map convergence (ADR-99 clause A) — orphaned by #221's close on the | n=12 evidence lines, dominated by: deploy/manifest-v1.2.0.yaml(x11), docs/audits/2026-07-08-fleet-consistency-census.md(x1)
#282 | #282 | [P3][S] Fleet `.gitattributes` EOL-normalization parity — 4 consumers lack `.gitattributes` (ai-council, corp- | n=1 evidence lines, dominated by: docs/audits/2026-07-08-fleet-consistency-census.md(x1)
#285 | #285 | [P3][S] Extend hub freshness gating to PLAYBOOK — SESSION_SETUP + AI_COUNCIL_PROCESS joined `_FRESHNESS_FILES` | n=176 evidence lines, dominated by: protocols/PLAYBOOK.md(x105), scripts/audit.py(x69), docs/audits/2026-07-08-fleet-consistency-census.md(x1)
#290 | #290 | [P3][S] Floor-carrier verify-teeth + self-heal (residual of #275b) — the v1.3.x arm-command fix landed the 3-s | n=10 evidence lines, dominated by: deploy/release-v1.3.x-contract.md(x4), deploy/carrier_floor.py(x4), scripts/arm_hooks.py(x2)
#293 | #293 | [P3][S] Consumer runbook fan-out — seed each consumer repo's `docs/handoffs/README.md` from the hub canonical  | n=17 evidence lines, dominated by: docs/handoffs/README.md(x15), scripts/seed_runbook.py(x2)
#294 | #294 | [P3][M] `validate_backlog` deploy-carrier + `--path` de-hardcode (ai-council pilot G1+G2) — the v1.2.0 manifes | n=19 evidence lines, dominated by: deploy/manifest-v1.2.0.yaml(x11), scripts/validate_backlog.py(x8)
#296 | #296 | [P3][S] `audit.py repo <name> --repo-path` doesn't persist its report (ai-council pilot G6) — `python scripts/ | n=69 evidence lines, dominated by: scripts/audit.py(x69)
#297 | #297 | [P3][S] Lightweight/dry `observe-arc` coverage mode (ai-council pilot G7) — `lived_sandbox.cli observe-arc` re | n=7 evidence lines, dominated by: scripts/enforcement_coverage.py(x7)
#298 | #298 | [P3][S] Handoff-generator polish — three ruled enhancements (2026-07-08): (a) EPIC_BOOT auto-pulls the relevan | n=6 evidence lines, dominated by: scripts/gen_handoff.py(x6)
#300 | #300 | [P1][M] Hermetization residual d.ii — mode-boot home (incident-recovery arc; TRIMMED 2026-07-18 to the single  | n=34 evidence lines, dominated by: protocols/HANDOFF_PROCESS.md(x32), protocols/REPO_ONBOARDING.md(x2)
#301 | #301 | [P2][M] Session-plan artifact class — architect-mode bundles gain a bundle-resident PLAN.md, completing the mo | n=6 evidence lines, dominated by: scripts/gen_handoff.py(x6)
#303 | #303 | [P2][S] Make seed_runbook.py child-class-aware (ADR-36 no-local-handoffs) — the leg-b seeder (scripts/seed_run | n=3 evidence lines, dominated by: scripts/seed_runbook.py(x2), docs/audits/2026-07-08-census-amendment-docs-handoffs-ruling.md(x1)
#305 | #305 | [P3][S] Add a verify-only / already-onboarded re-run mode to the onboarding runbook — the runbook's only path  | n=13 evidence lines, dominated by: deploy/tool.py(x11), protocols/REPO_ONBOARDING.md(x2)
#310 | #310 | [P3][S] Define the cold-bundle annotation surface + annotate the 2026-07-05 architect bundle as-cold — no sanc | n=15 evidence lines, dominated by: docs/handoffs/README.md(x15)
#315 | #315 | [P3][S] `INSTALL.md` uniform fleet-wide, hub-owned, deploy-carried (operator ruling; fleet-boundary-matrix Sur | n=3 evidence lines, dominated by: plugins/tier1-lifecycle/INSTALL.md(x1), deploy/manifest-v1.3.1.yaml(x1), docs/audits/2026-07-11-technical-fleet-boundary-matrix.md(x1)
#317 | #317 | [P2][M] Default-parallel test invocation + slow-tier markers — close the inner-loop serial tax left by #256/#2 | n=1 evidence lines, dominated by: .claude/skills/verify/verify.py(x1)
#322 | #322 | [P2][M] Fleet dashboard — a human-facing fleet-observability surface, three legs: (a) DATA SOURCES (existing,  | n=6 evidence lines, dominated by: scripts/fleet_health.py(x3), docs/intake/2026-07-08-func-dashboards-local-html.md(x2), scripts/boundary_report.py(x1)
#324 | #324 | [P3][M] Phase-6 axis-2 carrier — codify the night-batch → morning-prompt loop as a standing routine (charter;  | n=1 evidence lines, dominated by: docs/audits/2026-07-12-technical-night-codex-review.md(x1)
#325 | #325 | [P3][S] Carry `/save` to consumers via a manifest command-artifact carrier — the hub `/save` command (stage-al | n=3 evidence lines, dominated by: .claude/commands/override.md(x2), deploy/manifest-v1.3.1.yaml(x1)
#327 | #327 | [P2][M] Protocols-as-interface genre ruling (fleet-parity register acceptance) — unify the three current meani | n=5 evidence lines, dominated by: protocols/README.md(x3), docs/audits/2026-07-11-technical-fleet-parity-register.md(x2)
#329 | #329 | [P3][S] VS Code ownership visualization — folder icons/colors GENERATED from the #328 fleet_parity manifest (d | n=9 evidence lines, dominated by: ecosystem/parity-surfaces.yaml(x7), docs/audits/2026-07-11-technical-fleet-parity-register.md(x2)
#334 | #334 | [P3][S] Fleet-wide ruff hook id migration `ruff` → `ruff-check` (upstream `ruff-pre-commit` deprecation; flagg | n=1 evidence lines, dominated by: docs/audits/2026-07-12-codex-ruff-hub-pin.md(x1)
#335 | #335 | [P3][S] Exempt `templates/` from the `reconciled_versions` check — a template file's `reconciled_with` intenti | n=97 evidence lines, dominated by: scripts/audit.py(x69), ecosystem/disposition-register.yaml(x25), templates/CONTRIBUTING-md-template.md(x3)
#340 | #340 | [P2][S] /ship pre-flight validator honors the consumer repo's canonical test gate — the tier1-lifecycle ship c | n=7 evidence lines, dominated by: plugins/tier1-lifecycle/commands/ship.md(x7)
#342 | #342 | [P3][S] fleet_parity gate-ahead max-fidelity hardening (deferred from #336/ADR-102, operator-ruled) — three ne | n=16 evidence lines, dominated by: scripts/fleet_parity.py(x14), docs/decisions/ADR-102-parity-gate-rev-axis.md(x2)
#343 | #343 | [P3][S] fleet_parity ship-gate-only scoping (RIDER 2 perf follow-up, operator-ruled 2026-07-18) — the [#337] p | n=83 evidence lines, dominated by: scripts/audit.py(x69), scripts/fleet_parity.py(x14)
#344 | #344 | [P2][M] Session-close gate for handoff generation + consumer hub-write guard (NEEDS-RULING; ai-council 2026-07 | n=14 evidence lines, dominated by: scripts/assemble_paste.py(x8), scripts/session_end_backpressure.py(x6)
#345 | #345 | [P2][M] Externalize the ADR-101 frozensets → machine-readable path-pattern registry + generalize `validate_her | n=5 evidence lines, dominated by: scripts/validate_hermetization.py(x5)
#349 | #349 | [P2][M] Mechanize session-discipline inheritance — the test-then-close gate travels via mechanism, not operato | n=11 evidence lines, dominated by: scripts/session_end_backpressure.py(x6), protocols/DEFINITION_OF_DONE.md(x5)
#350 | #350 | [P3][S] Handoff-process refinements (operator priority-program item 5 — explicitly LAST, 2026-07-18) — general | n=38 evidence lines, dominated by: protocols/HANDOFF_PROCESS.md(x32), scripts/gen_handoff.py(x6)
#351 | #351 | [P3][M] Fleet-Python-upgrade ticket ("always newest Python" — RULING-PY, 2026-07-18) — RULING-PY set the ruff  | n=1 evidence lines, dominated by: deploy/manifest-v1.3.1.yaml(x1)
#352 | #352 | [P3][S] Versioned `.vscode` region decoration (RULING-S human-facing half) — editor-side background decoration | n=5 evidence lines, dominated by: docs/audits/2026-07-11-technical-fleet-boundary-marker-design.md(x5)
#353 | #353 | [P2][M] Session-boot contract hardening — refuse a mid-session externally-authored order lacking a worktree/cl | n=6 evidence lines, dominated by: scripts/session_end_backpressure.py(x6)
#354 | #354 | [P2][M] W6 seed-1 **recurrence half** — build the staged-diff CO-CHANGE checker with explicit ADR-36/41/101 →  | n=5 evidence lines, dominated by: scripts/coherence_nudge.py(x3), docs/audits/2026-07-19-codex-cycle-close-terra-review.md(x1), docs/audits/2026-07-19-technical-night-consolidated-cycl...
#356 | #356 | [P2][M] **RULING-W and the merge-delegation composite are LEGIBLE but have neither a mechanism nor a declarati | n=1 evidence lines, dominated by: docs/audits/2026-07-19-technical-night-s4-handoff-playbook-currency.md(x1)
#357 | #357 | [P2][M] **Silent-rule census run 2** — sweep `docs/decisions/` under the [E8] declaration test, completing the | n=69 evidence lines, dominated by: scripts/audit.py(x69)
#358 | #358 | [P2][S] **`ecosystem/parity-surfaces.yaml` misdescribes its own enforcement posture at HEAD** — header `:6` an | n=90 evidence lines, dominated by: scripts/audit.py(x69), scripts/fleet_parity.py(x14), ecosystem/parity-surfaces.yaml(x7)
#359 | #359 | [P1][M] **PHANTOM ENFORCEMENT — `protocols/HANDOFF_PROCESS.md:517-518` claims a mechanism that does not exist. | n=33 evidence lines, dominated by: protocols/HANDOFF_PROCESS.md(x32), scripts/boundary_report.py(x1)
#360 | #360 | [P3][S] **`protocols/DEFINITION_OF_DONE.md:106-109` expired in place** — the `## Scope-freeze` clause froze th | n=5 evidence lines, dominated by: protocols/DEFINITION_OF_DONE.md(x5)
#361 | #361 | [P3][S] **ADR-immutability's real coverage is declared only in code, never in the protocol** — `protocols/AI_C | n=7 evidence lines, dominated by: protocols/AI_COUNCIL_PROCESS.md(x5), templates/claude-regions/critical-rules-records.md(x2)
#363 | #363 | [P2][S] **`codex-review` routed a CODE-shaped diff through the `gpt-5.6-sol` lane, not terra** — live observat | n=1 evidence lines, dominated by: docs/audits/2026-07-19-codex-residual-completeness-gate.md(x1)
#364 | #364 | [P3][S] **`doc_rot`'s length cap blocks [#353] from doing its job** — [#353] exists to accumulate "n=N recover | n=4 evidence lines, dominated by: scripts/validate_doc_rot.py(x4)
#365 | #365 | [P3][S] **Promote `residual_completeness` from `exempt:` to `coverage_scope`** — the doc-side rule now EXISTS. | n=47 evidence lines, dominated by: protocols/HANDOFF_PROCESS.md(x32), ecosystem/doc-code-edge.yaml(x15)
#366 | #366 | [P2][S] **`residual_completeness` scans the WORKING TREE, not the staged blob** — codex HIGH 2026-07-19, verif | n=35 evidence lines, dominated by: protocols/HANDOFF_PROCESS.md(x32), scripts/validate_residual_completeness.py(x2), docs/audits/2026-07-19-codex-residual-rule-declaration.md(x1)
#367 | #367 | [P2][S] **HANDOFF_PROCESS held at `Version: 5.7` while gaining an additive normative rule** — codex HIGH 2026- | n=33 evidence lines, dominated by: protocols/HANDOFF_PROCESS.md(x32), docs/audits/2026-07-19-codex-residual-rule-declaration.md(x1)
#369 | #369 | [P3][S] **Wire `boundary_headers.py --check` into pre-commit** — the generated-not-hand-maintained property of | n=97 evidence lines, dominated by: ecosystem/doc-counts.md(x94), scripts/boundary_headers.py(x3)
#370 | #370 | [P3][S] **Is the `owner=hub` / `owner=repo` ownership model two-state-complete?** — **RULED 2026-07-28 (operat | n=3 evidence lines, dominated by: deploy/manifest-v1.4.0.yaml(x3)
#371 | #371 | [P2][S] **Consumer editor-config write-through — declared at v1.4.0, never built, never ticketed** — `deploy/m | n=9 evidence lines, dominated by: .vscode/settings.json(x5), deploy/manifest-v1.4.0.yaml(x3), docs/audits/2026-07-20-technical-352-boundary-render-diagnostic.md(x1)
#382 | #382 | [P1][M] **Desired-state data model: intake → ADR** — build the intake #16 §2 architecture (the Terraform **mod | n=55 evidence lines, dominated by: docs/decisions/README.md(x52), docs/intake/2026-07-21-func-fleet-north-star.md(x3)
#383 | #383 | [P2][L] **Execution waves per surface** — once the schema exists, converge each L0/L2 surface (caches, the `.c | n=3 evidence lines, dominated by: docs/intake/2026-07-21-func-fleet-north-star.md(x3)
#385 | #385 | [P3][M] **L4 tech-currency lane** — nightly research on new Python tech/versions → version-bump proposals writ | n=3 evidence lines, dominated by: docs/intake/2026-07-21-func-fleet-north-star.md(x3)
#387 | #387 | [P2][S] **Rewrite the buy-vs-build intake BEFORE anything ingests it** — intake **#2** (the platform buy-vs-bu | n=4 evidence lines, dominated by: docs/intake/2026-07-21-func-fleet-north-star.md(x3), docs/intake/archive/2026-07-06-platform-feature-scan.md(x1)
#388 | #388 | [P3][S] **The "10–20 repo" fleet-scale target is FABRICATED — correct it to the live 5–8+ wherever it is resta | n=1 evidence lines, dominated by: docs/audits/2026-07-21-technical-night-vision-audit.md(x1)
#389 | #389 | [P2][S] **Prompt-lint — gate the five architect fields before a lane runs** — the ADR-87 contract (architect e | n=1 evidence lines, dominated by: docs/audits/2026-07-19-technical-night-s7-prompt-authoring-quality.md(x1)
#390 | #390 | [P2][S] **Resolve the ADR-87 effort-ownership contradiction, then true up the prompt template** — ADR-87 Decis | n=4 evidence lines, dominated by: templates/prompt-template.md(x4)
#391 | #391 | [P3][S] **Wire fleet_analytics into a nightly lane, or narrow #384 to a manual reporter** — #384 claims "runs  | n=3 evidence lines, dominated by: scripts/fleet_analytics.py(x2), docs/audits/2026-07-22-verification-night-batch-integration-386-384.md(x1)
#392 | #392 | [P3][S] **fleet_analytics rename-alias loses history on path-reuse** — `scripts/fleet_analytics.py:326`'s glob | n=3 evidence lines, dominated by: scripts/fleet_analytics.py(x2), docs/audits/2026-07-22-verification-night-batch-integration-386-384.md(x1)
#393 | #393 | [P3][S] **corp-sca rot review — confirm-live-or-retire 3 candidates** — the first fleet_analytics run flagged  | n=1 evidence lines, dominated by: docs/audits/2026-07-22-verification-night-batch-integration-386-384.md(x1)
#394 | #394 | [P3][S] **Analytics coverage gap — corp-monorepo no-edit-record blind spot** — the run found 311/812 files (38 | n=1 evidence lines, dominated by: docs/audits/2026-07-22-verification-night-batch-integration-386-384.md(x1)
#396 | #396 | [P3][S] **Extract `scripts/gitenv.py` — the GIT_* env-scrub is in 3 places** — the subprocess-git env scrub (t | n=86 evidence lines, dominated by: scripts/audit.py(x69), scripts/fleet_parity.py(x14), scripts/fleet_analytics.py(x2)
#397 | #397 | [P3][M] **scripts/ target structure — rule on the mapped grouping, then (maybe) move** — the 2026-07-22 hygien | n=1 evidence lines, dominated by: docs/audits/2026-07-22-technical-hygiene-pre-handoff-inventory.md(x1)
#399 | #399 | [P2][S] **`templates/handoff/v5/README.md.tmpl` — phantom source claim (the [#359] class)** — `protocols/HANDO | n=50 evidence lines, dominated by: protocols/HANDOFF_PROCESS.md(x32), docs/handoffs/README.md(x15), scripts/seed_runbook.py(x2)
#400 | #400 | [P3][S] **Ownership-model: the hub-mandated-STRUCTURE / repo-owned-CONTENT cell (rosters) — same ruling family | n=2 evidence lines, dominated by: docs/audits/2026-07-22-technical-night-batch-deep-audit.md(x2)
#402 | #402 | [P3][S] **Intake naming clause — DEPLOY the `YYYY-MM-DD-<class>-<slug>` half of the enum ruling** — the naming | n=25 evidence lines, dominated by: docs/intake/README.md(x24), docs/audits/2026-07-23-technical-status-enum-reconcile.md(x1)
#404 | #404 | [P2][S] **gen_handoff execution-mode SUPPLEMENT leak (mode-blind framing + P8 row)** — `_tokens()` picks `SUPP | n=38 evidence lines, dominated by: protocols/HANDOFF_PROCESS.md(x32), scripts/gen_handoff.py(x6)
#405 | #405 | [P2][S] **Session-end leftover check — nothing verifies "no leftovers"** — cleanup failed 3x the 2026-07 arc ( | n=6 evidence lines, dominated by: scripts/session_end_backpressure.py(x6)
#406 | #406 | [P3][S] **Commit-time doc_rot surfacing — an over-threshold BACKLOG task commits clean, reds only the NEXT shi | n=72 evidence lines, dominated by: scripts/audit.py(x69), scripts/coherence_nudge.py(x3)
#408 | #408 | [P2][M] **Auto-coupled doc updates — closing a backlog item must mechanically PULL its ARCHITECTURE + JOURNAL  | n=69 evidence lines, dominated by: scripts/audit.py(x69)
#413 | #413 | [P2][S] **Colors semantics — visually distinguish global/hub-managed vs per-repo content in governed markdown  | n=3 evidence lines, dominated by: deploy/manifest-v1.4.0.yaml(x3)
#414 | #414 | [P2][S] **Self-acting-on-main incident family — a session changed `main` with no operator GO and no anchored a | n=6 evidence lines, dominated by: scripts/session_end_backpressure.py(x6)
#415 | #415 | [P2][S] **Tests must bind fixtures, not live mutable repo content (heuristic-behaviour tests)** — `test_live_b | n=14 evidence lines, dominated by: scripts/validate_backlog.py(x8), tests/test_validate_backlog.py(x6)
#416 | #416 | [P3][S] **ai-council `ARCHITECTURE.md` codemap drift at L23/L109** — carved out of [#262]'s Done-when BEFORE t | n=1 evidence lines, dominated by: docs/audits/2026-07-08-fleet-consistency-census.md(x1)
#417 | #417 | [P3][S] **`check_dirty_tree` runs with no pathspec, so the Stop gate fires every session on non-work** —... | n=75 evidence lines, dominated by: scripts/audit.py(x69), scripts/session_end_backpressure.py(x6)
#418 | #418 | [P2][S] **`automation/fleet-audit` records 0–10 baselines a day, not one** — the writer branch carries up to 1 | n=75 evidence lines, dominated by: scripts/audit.py(x69), .claude/settings.json(x3), scripts/fleet_health.py(x3)
#419 | #419 | [P2][M] **We run routines whose output nobody consumes** — the nightly conformance routine emits a digest ever | n=11 evidence lines, dominated by: deploy/tool.py(x11)
#421 | #421 | [P2][S] **`verify_handoff_probes` cannot bind a repo-root dotfile — the tokenizer drops the leading dot** (sur | n=116 evidence lines, dominated by: scripts/audit.py(x69), protocols/HANDOFF_PROCESS.md(x32), scripts/verify_handoff_probes.py(x12)
#422 | #422 | [P2][S] **`reflow_framing`'s cold→FILLED flip is partial by design, and nothing detects the self-contradiction | n=46 evidence lines, dominated by: protocols/HANDOFF_PROCESS.md(x32), scripts/assemble_paste.py(x8), scripts/gen_handoff.py(x6)
#423 | #423 | [P2][M] **The integration sequence runs on prose every time, never mechanized** — landing an arc takes eight s | n=7 evidence lines, dominated by: plugins/tier1-lifecycle/commands/ship.md(x7)
#424 | #424 | [P2][S] **Backlog `depends-on` gates are INERT — `_DEPID_RE` requires a `#`, the [E9] chain is written bare**  | n=14 evidence lines, dominated by: scripts/validate_backlog.py(x8), tests/test_validate_backlog.py(x6)
#425 | #425 | [P2][S] **The suite is green on a format the file does not use** — every `depends-on` fixture in `tests/test_v | n=8 evidence lines, dominated by: tests/test_validate_backlog.py(x6), tests/test_validate_backlog_twin_parity.py(x2)
#426 | #426 | [P2][M] **Declare `consumer` + `consumption_path` for every LIVE routine** — ADR-105's activation gate governs | n=5 evidence lines, dominated by: .claude/settings.json(x3), scripts/surface_triage.ps1(x2)
#427 | #427 | [P3][S] **Region templates carry a repo-POSITION-DEPENDENT path** (ai-council, 2026-07-26):... | n=8 evidence lines, dominated by: logs/TOKEN-LOG.md(x6), templates/claude-regions/critical-rules-records.md(x2)
#428 | #428 | [P2][S] **`nightly-triage` reports a dead producer to every session start** — the producer has been dead since | n=2 evidence lines, dominated by: scripts/surface_triage.ps1(x2)
#430 | #430 | [P2][M] **Consumer template rejects root `conftest.py`; `fleet_parity`'s verdict depends on state outside its  | n=14 evidence lines, dominated by: scripts/fleet_parity.py(x14)
#431 | #431 | [P2][S] **`codex-review` silently drops the doc lane on any mixed diff** — any code-allowlist file routes the  | n=105 evidence lines, dominated by: protocols/PLAYBOOK.md(x105)
#432 | #432 | [P1][M] **Adopt `uv` as the environment/dependency toolchain — `.dev-knowledge` ONLY this window** — operator  | n=52 evidence lines, dominated by: docs/decisions/README.md(x52)
#433 | #433 | [P1][M] **BACKLOG restructure — build-thin ENGINE + Backlog.md VIEWER** — the three-way bake-off is **SUPERSED | n=52 evidence lines, dominated by: docs/decisions/README.md(x52)
#438 | #438 | [P3][S] **Codify gate-class posture: terra design review BEFORE build for refusal-gate arcs** — a gate whose j | n=106 evidence lines, dominated by: protocols/PLAYBOOK.md(x105), docs/audits/2026-07-27-codex-436-ratchet-final.md(x1)
#440 | #440 | [P2][S] **Make the `tasks/` id ledger tamper-evident — a deleted retired record is undetectable** (terra 5th p | n=17 evidence lines, dominated by: scripts/gen_task_tree.py(x17)
#442 | #442 | [P2][M] **Plugin command-cache staleness — cached command text can silently outlive a workflow change** — witn | n=4 evidence lines, dominated by: plugins/tier1-lifecycle/commands/review-closures.md(x4)
#445 | #445 | [P2][S] **`codex-review` wrapper path-guard reports SUCCESS having reviewed nothing** — third instance of the  | n=1 evidence lines, dominated by: docs/audits/2026-07-29-codex-postflip-fix-batch-review.md(x1)
#446 | #446 | [P2][L] **§B(b) one-round-trip boot build — the v6 carrier arc** — intake #19 §B(b) ADOPTED at intake #18 rati | n=8 evidence lines, dominated by: .claude/commands/handoff.md(x8)
#447 | #447 | [P3][S] **Self-referential gate family — the committing act cannot satisfy the gate's own precondition** — (1) | n=8 evidence lines, dominated by: scripts/session_end_backpressure.py(x6), scripts/arm_hooks.py(x2)
```

## Top candidates for the architect (closable)

**None.** Zero of the 132 proposals produced verifiable closure evidence. This itself is the most
useful output of this triage: the WEAK bucket in its current form is not finding real closures, it is
reproducing #277's own diagnosis at n=132 instead of n=49. If anything is worth architect attention it
is not a closure candidate but two structural notes surfaced along the way:

1. **#213 (PLAYBOOK condensation)** has real, partial, dated evidence of past work (the SEAL-1a arc,
   commit `ef2c32dea`, 2026-06-26) but PLAYBOOK.md has since grown to 3950 lines against a ~2600-2950
   target -- worth a fresh scoping pass rather than closure.
2. **#402 / #382** show explicit RULED / DISCHARGED language in their own task text pointing at
   real upstream progress (intake naming enum ruled 2026-07-25; the #381 precondition discharged via
   ADR-104) but each task's own stated Done-when still requires unbuilt work -- both correctly remain
   open, not closable.

## Cannot classify

None. All 132 parsed proposals were placed in exactly one bucket. Nothing resisted classification --
the uniformly-open BACKLOG/tasks status combined with per-id Done-when text was sufficient signal in
every case except the 8 pure-ruling items above, which went to needs-ruling rather than a forced guess.
