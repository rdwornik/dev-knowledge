# Fable Architectural Review — `.dev-knowledge` methodology system

<!-- scope: meta -->

> **Type:** point-in-time review (ADR-60 `docs/audits/` zone). Immutable once landed — supersede with a new file, do not edit in place.
> **Date:** 2026-07-04 · **Reviewed HEAD:** `b65c760` (post-P1 essence-spec merge; read in worktree `fable-arch-review`) · **Reviewer:** Claude Fable 5 (`claude-fable-5`, max effort), read-only session — ANALYSIS ONLY per the operator mandate (no code, no branch beyond this artifact's landing).
> **Lens:** the operator's own thesis method (Bass/Clements/Kazman tradition, 4+1 views, QA→scenario→tactic→tradeoff vocabulary) applied in the **evaluation** direction (ATAM-style), per the mandate. The thesis's two conclusions (continuous "what is our goal?" re-evaluation; machine-legible documentation makes inevitable change manageable) are used as evaluation criteria; the sociotechnical equilibrium is evaluated as a first-class QA the thesis's pre-LLM framework could not name.
> **Grounding:** every claim below is grounded in a live read at this HEAD: ARCHITECTURE.md, PLAYBOOK.md (full chapter read), ESSENTIALS.md, CLAUDE.md, VISION.md, `scripts/audit.py` (registry + a live `health` run), `scripts/enforcement_coverage.py`, `deploy/*` (tool, manifest v1.1.0, release_lint, carriers), `scripts/session_end_backpressure.py`, `.pre-commit-config.yaml`, `.claude/settings.json` (hub + `~/.claude` + ai-council), ADR-81/85/87/92/93/94/95 (+ index), DEFINITION_OF_DONE.md, HANDOFF_BOOT.md, HANDOFF_PROCESS.md (map), BACKLOG.md (full), JOURNAL.md (recent arcs), LESSONS.md (targeted), `~/.claude/skills/gotchas/gotchas.md`, `ecosystem/disposition-register.yaml`, `ecosystem/deployed-versions.yaml`, the 2026-07-02 self-audit, the 2026-07-03 handoff bundle + SUPPLEMENT, and the operator's thesis (`main.md`, incl. the author-method chapter and Wnioski).

---

## 0. Verdict in one paragraph

Architecturally sound, exceptional in self-honesty, and further along the "held by mechanism, not memory" road than any comparable system I can name — but it is currently **stronger at detecting drift than at preventing it**, applies its configured→armed→proven standard **more rigorously to consumers than to itself**, and its highest-severity safety zone (OneDrive P0) has a **known-open write vector that the map claims is closed**. The system's founding insight (presence ≠ enforcement) is correct and proven; the review's core message is that this insight has three more rings to travel outward: from organs to **ARMING** (the hub's own hooks), from organs to the **WHOLE WORKFLOW** (skills/commands/gotchas — the operator's sandbox question, answered §6), and from the executor to the **DECISION CHANNEL** (consult records nearly evaporating with expired chats). Nothing here says stop; several things say re-order.

---

## 1. The system in 4+1 views (concise)

**Scenario view (+1)** — the view that binds the others; the load-bearing scenarios:

- S1 modifiability: "a lesson lands at 02:00 → becomes enforceable convention without human memory carrying it" (Lessons→ADR→Convention→Enforcement→Dissemination loop).
- S2 deployability: "operator deploys corpus vX to a consumer; record lands only if every carrier verifies; a poisoned floor fails loud on next clone."
- S3 integrity: "an agent (or human) attempts a forbidden write / un-journaled stop / FF-merge → a deterministic organ blocks it, or a WARN surfaces it at ship-gate."
- S4 testability: "for any mechanism, a test can force it to fire and observe the block."
- S5 equilibrium: "a 4-hour-degraded session hands off; the next session reconstructs intent from repo artifacts alone, without the operator re-explaining."

**Logical view:** three actors (L1 browser-architect / operator-as-consent-gate / L3 CC executor) around L2 (this repo: passive prescription + read-only validation). Corpus object classes: living / append-only / immutable (ADR-39 lifecycle). Coherence held across 4 declared/computed edge types (code↔code, code↔doc, doc↔doc, undeclared). Two lifelines (Workflow, Coherence) — plus, per this review's ruling on the self-audit's §7.7 fork: **dissemination is a third lifeline, not a leak.** Evidence: PLAYBOOK §20 is unmapped in the lifelines chapter-map; VISION names "Disseminator" as a co-equal role; ARCHITECTURE Ch6 names Dissemination a frontier stage; ADR-91/92/93 + the Informant form a coherent subsystem with its own invariants (write-yes/commit-no/autonomy-no). Name it Lifeline 3 and re-home §19/§20 + the deploy ADRs under it. Two-lifelines was true until ~June; the system outgrew its own frame and the frame should follow.

**Process view:** five concentric loops, each with named gates —

- turn/session: SessionStart surfacing → work → Stop (propose_closures + ADR-85 seal).
- commit: pre-commit (10 gates; audit-health FAIL-blocks) → commit-msg → pre-push.
- arc: branch → ex-ante frozen acceptance contract → ship-gate → `--no-ff` merge → closure loop (`/review-closures`, human-gated).
- nightly: cloud Routine (spec-orchestrated, read-only+skeptic) → Action diff-guard → digest diverted to `automation/*` → morning funnel; local `fleet_health` (deterministic).
- release: essence-spec manifest → release_lint (manual) → deploy assess→execute→ratify → Informant fire-verdicts.

**Development view:** markdown governance corpus + read-only Python validators (`scripts/`, `deploy/`), 28 registered checks, 1101 collected tests, ruff-gated, plugin distributed via directory marketplace, native worktrees for parallel sessions, no CI on the governance path (deliberate: corp-ops has no remote, so local-carrier + central-detection is the fleet model — this single physical fact shapes the whole enforcement-transfer design).

**Physical view:** one Windows 11 machine is the entire "fleet" substrate (hub + 4 sibling consumer repos + `~/.claude` L0 + Task Scheduler), plus GitHub private remotes and ephemeral cloud-Routine Linux clones (hub-independent by design, ADR-72). Single-machine, single-operator: availability and security postures are calibrated to that, correctly — but it makes ARMING per-machine state (see RF-2) and the operator the sole scheduler.

---

## 2. The thesis lens — the operator's own method, applied backward

**Method mapping:** the thesis's 5 steps (general scenarios → tactics per QA → tactic questionnaires → pattern tradeoff analysis → whole-system decision) are applied here in the ATAM/evaluation direction: §3 states scenarios (stimulus → response → response-measure, per the thesis's 6-part scenario anatomy), identifies the system's ACTUAL tactics, weighs tradeoffs, verdicts. The thesis's questionnaire instrument (its human-consultation core) maps onto what this system built instead: council debates, Fable consults, and the handoff probe manifest — machine-era questionnaires. One vocabulary shift, made deliberately: the thesis's "integralność" means component-integration ability; this review uses the operator's evaluation-frame meaning (enforcement-holds), which is the right QA for a governance system.

**Thesis conclusion 1 — continuous "jaki jest nasz cel, co chcemy osiągnąć?"** (the re-evaluation question that saves time). VERDICT: **structurally embodied, with one named drift mode.** Embodied: every BACKLOG task carries "Done when"; ADR-81's 2026-06-24 amendment makes the acceptance contract EX-ANTE and frozen; closure is declared on the hard metric by doctrine (PLAYBOOK Ch12.1); the educate→close gate forces a so-what artifact. This is the thesis's question turned into gates — better operationalized than the thesis itself managed. The drift mode: when the gate becomes the goal. The proven instance is the 2026-07-01 forced-false ARCHITECTURE re-stamp (gate satisfied, goal — a genuine re-read — missed), which the system itself caught and answered with #222. The pattern to watch: every deterministic proxy for a semantic goal will eventually be satisfied without the goal; the system needs (and mostly has) a standing genuineness audit per proxy. Keep asking the thesis's question OF THE GATES themselves.

**Thesis conclusion 2 — change is inevitable; machine-legible documentation makes it manageable.** VERDICT: **delivered on detection, half-delivered on removal.** The essence-spec (P1, #244) is literally this conclusion operationalized: the methodology now has a component-granular, machine-readable self-model (components with verify classes fire/hash/wired; anchors closing the 5-way version smear R6; doc_shapes lint-guarded against their authoritative constants). The coherence spine + doc_rot/doc_structure/doc_claims detect rot mechanically. But the add-only surfaces still accrete (gotchas ~91KB with no retirement, #130; the `docs/handoffs/` corpus unbounded, #212; PLAYBOOK 3,457 lines, #213; two dead v4-era checks still in ALL_CHECKS) — the PRUNE half (P2) is exactly the thesis's promise not yet kept. The plan is right (pathology split: audit trail stays append-only, live surface gets pruned, tombstone is an append); execute it.

**Where the system EXTENDS the thesis:** the thesis is pre-LLM-agent; it has no QA for a standing human-architect ↔ AI-executor ↔ methodology-hub equilibrium. This system's genuinely novel contribution is treating that equilibrium as an ENGINEERED property: the ADR-87 division of labor (empirically derived, by-class), the role-stability self-check in HANDOFF_BOOT (role-drift named as "the recurring, witnessed failure"), the un-bluffable orientation probes, the consent-gate economics ("ratification bandwidth is the scarce resource"). §5 evaluates it as a first-class QA. Also extended: the thesis's "confrontation with a differently-thinking third party was the turning point" (the Stankiewicz interview) is institutionalized here as multi-provider council debate, cross-vendor Codex review, and Mythos-tier consults — heterogeneous-second-reader as standing doctrine, not a lucky interview.

---

## 3. Quality-attribute assessment (scenario → tactics → tradeoffs → verdict)

### 3.1 Modifiability — the reason the system exists

**Scenario:** a friction/lesson at any hour → generalized rule → enforceable convention → distributed, without any human carrying it in memory; AND any piece can later be changed/retired without archaeology.

**Tactics present:** the methodology engine loop (Lessons→ADR→Convention→Enforcement→Dissemination); amend-vs-reopen protocol; ADR-94 status-line rule (kills the frozen-header dance); narrow-first / do-not-build-is-doctrine (ADR-88 P5); evidence gates (n=2 before codifying a routine; data-gated promotions); the sealing test ("does this mechanism have its consumer?" — allowed to answer NO, e.g. the declined import-cycle gate); semver'd corpus + per-release manifest; source→gate→agent precedence (drift-proofing by construction: derive > gate > review).

**Tradeoffs:** the price of evolvability-with-receipts is corpus mass — PLAYBOOK 3,457 lines, 228 LESSONS, ~69 ADRs, 100 open tasks — and a growing meta-surface (dispositions, registers, coverage annotations) that itself needs grooming. The system knows (#213, #212, #130, doc_rot) and has chosen detection-then-gated-prune. Correct choice; the debt is real until P2 lands.

**Verdict: ACHIEVED** — the strongest QA. Watch item: priority signal in BACKLOG is flat (effectively everything P2/P3; no P1 tier in live use), so "what to change first" rides in handoff residuals and the operator's head — a small held-by-memory leak inside the modifiability machinery itself.

### 3.2 Deployability — transfer / sync / prune across repos

**Scenario:** deploy corpus vX to consumer C; every carrier verifies or nothing is recorded; drift after deploy fails loud; a component retired at the hub disappears at C, verified absent.

**Tactics present:** ADR-91 tag-anchored semver; ADR-92 deterministic verify-gated tool (write-yes/commit-no/autonomy-no — a principled answer to the Layer-2 boundary); ADR-93 two-leg hash-guard + SessionStart self-arm at consumers; the #230 functional conformance harness; the Informant's honest verdict vocabulary (enforcing-local / absent / hub-scoped / present-unverified — refusing to manufacture fake gaps); essence-spec P1 (golden-diff behavior-preservation; release_lint reconciling 5 version anchors); byte-faithful git transport (the Windows CRLF/cp1252 class closed with tests).

**Tradeoffs and open risk:** n=1 (ai-council only; #221 pending). release_lint is MANUAL — wired into neither ALL_CHECKS nor deploy preflight (honest, but that is a configured-not-armed window in the release path itself; the SUPPLEMENT defers preflight wiring — fine, but do it before v1.2.0, because P2 is the first behavior-CHANGING release and that is exactly when an anchor-inconsistent release hurts). The Model-A guard is single-point-of-failure by ADR-93's own admission, with a greenfield-settings hole closed only for ai-council by test. Per-consumer divergence (gitignore shapes) is a discovered class with a forward rule but no mechanization. The mesh-deploy defect arc (`git add -A` vs gitignore swallowing; `verify()` checking presence-not-committability, fixed `5f8be71`) shows the carrier verify contract needed its own hard lesson — good recovery, and exactly why #230-style functional acceptance must gate every carrier, not just floor.

**Verdict: ACHIEVED AT n=1, AT-RISK FOR FLEET** until: release_lint wired to preflight, #221 runs with #230-class acceptance per repo, and the greenfield-settings precondition is generalized (ruling on self-audit §7.2: option (a)-as-precondition + the cheap second leg from RF-2 below; do NOT block fleet on a full second guard).

On self-audit §7.6 (currency model): rule per-carrier — floor = drift-catch (present model, correct); precommit = consumer-pull (already true); orchestration copies = #95 detection at fleet_health; REJECT scheduled active-push (it breaches autonomy-no for marginal gain). #231 consumer→hub feedback is the right complement, not a precondition.

### 3.3 Integrity — does enforcement actually HOLD ("presence ≠ enforcement")

**Scenario set:** (a) agent edits a transcript → blocked; (b) session with commits tries to stop un-journaled → blocked until compliant; (c) direct-to-main/FF push → refused; (d) canonical doc edited without re-review → commit blocked; (e) forbidden OneDrive write → blocked; (f) drift too semantic to gate → surfaced and dispositioned, never silently suppressed.

**Tactics present:** fail-closed PreToolUse guards (block_immutable_edits: fail-closed in-zone, fail-open out-of-zone — right shape); the ADR-85 Stop-gate (the most carefully engineered Stop hook I have seen: fire-once vs structural-floor against the block-cap bypass; HEAD-bound logged `/override`; compliance-terminates-not-cap); ship-gate reading `Finding.status` with a disposition register that surfaces its own stale entries (ADR-75 decoration rule — the register cannot rot silently; genuinely good design); block-ff-push sharing ONE FF-signature with the detector so gate and WARN cannot disagree; the zone register's "no organ = decoration" rule.

**Where it does NOT hold — the grill:**

1. **The P0 zone's Edit/Write vector is OPEN and the map claims otherwise.** Global PreToolUse matcher is `Bash|PowerShell` only (live read of `~/.claude/settings.json`); ARCHITECTURE Ch2 row says "every Bash/Edit/Write tool call". Known as #191 — filed at P2 while the operator's daily driver is Accept-Edits mode. The single highest-severity gap in the system, and a map-integrity failure on the same row (RF-1).
2. **Arming is per-machine manual state and the hub does not self-arm.** The pre-commit config's own header warns the pre-push gate "never fires" until a one-time manual install; commit `533109f` landed direct-to-main on 2026-06-26 — SIX DAYS after the prevent organ shipped — and was ratified as the THIRD instance of its class (#210). Meanwhile consumers get a SessionStart `pre_commit install` self-arm via the mesh/floor carriers, but the hub's own SessionStart has no self-arm step. The consumer is better armed than the authority (RF-2).
3. **The "un-gameable" Stop-gate is un-gameable in CONTENT but evadeable in STATE:** every check (including the hard leg) short-circuits on a dirty tree, so not-committing (or leaving any file dirty) silences the seal; and the platform block-cap ultimately force-ends a turn after N blocks, so persistence CAN beat policy at the platform layer (witnessed "9 consecutive times — overriding"). Both are known internally; neither caveat appears in DEFINITION_OF_DONE.md, which still says "un-gameable" unqualified (RF-3).
4. **WARN-tier awareness organs bind only at ship-gate; drift ratified per-instance accumulates in the register** (3× journal-wrap before #210 was filed). The structural tension is real: ADR-85 demands a JOURNAL wrap citing the merge SHA, which only exists AFTER the merge — so the wrap's natural home is a direct-to-main commit, which core-invariant #5 forbids. Two organs' happy paths collide; the register absorbed the collision as paperwork. Decide #210's shape (recommended: the path-scoped exemption — a JOURNAL.md-only direct commit passes, anything else WARNs — it preserves #5 for substance and ends the ratification treadmill).
5. **`--no-verify` remains a sanctioned-but-unlogged bypass:** the operator's own `bda4fff` in ai-council carried a stamp that "must have used --no-verify" (JOURNAL, execution-truthfulness flag). The gates' threat model is accidental-drift, not adversary — correct — but bypass events are currently invisible; they should at least be countable (the override token is logged; `--no-verify` is not).

**Verdict: AT-RISK** — not because the mechanisms are weak (where armed, they demonstrably bite: enforcing-local ×2 fire-proven; the deployed freshness gate is right now blocking ai-council's next commit on a REAL staleness — the organ dogfooding itself) but because the arming layer and the P0 edge are behind the system's own standard. The fix list is short and cheap (§8 roadmap items 1–3).

### 3.4 Testability — is conformance demonstrable; does a gate provably fire

**Scenario:** for any enforcement mechanism, a test forces the trigger and observes the block; for any release, behavior-preservation is provable; for the workflow itself, "deployed" is demonstrated by observed engagement, not presence.

**Tactics present — genuinely state-of-the-art at the organ level:** leg-e (ADR-81e, demonstrated-firing as the sufficient condition); the Informant fire_test as sole truth-maker with static-locate demoted to pre-filter; hub-scoped verdicts DEMONSTRATED not source-read (`_demonstrate_hub_scoped` — running the organ off-hub and observing the guard, a beautiful application of the standard to its own seam); the circular-testing guard + "what one-line change would make this go red?" teeth-check; ex-ante frozen contracts (xfail-strict #194 exemplar); golden-diff for the essence conversion; 1101 tests; fixture-from-producer rule (LESSONS 2026-06-05).

**Where it does NOT hold — the operator's own observation, confirmed:** leg-e stops at enforcement organs. Skills, commands, gotchas, and the composed workflow are accepted on presence + a prose "smoke test" step (PLAYBOOK Ch14 validation — manual, unenforced). Live consequence found this session: `python scripts/audit.py checks` — the command three canonical docs cite as THE live registry — crashes with UnicodeEncodeError on a default cp1252 console (check #23's summary carries `→`). The exact gotcha exists (gotchas.md, "Last triggered 2026-06-22", fixed for `cmd_health`'s evidence strings) and did not propagate to `cmd_checks` in the SAME FILE. A gotcha is prose; nothing mechanizes it; presence-of-the-lesson ≠ enforcement-of-the-lesson. One transcript-level lived run of "show me the registry" on PowerShell would have caught it the day it shipped — which is precisely the sandbox argument (§6).

**Verdict: ACHIEVED at the validator/organ level (best-in-class); AT-RISK at the workflow level** — the gap is real, bounded, and closable (§6).

### 3.5 Secondary QAs (brief)

- **Availability: ACHIEVED for the context.** Fail-soft on every awareness path, fail-open-on-own-error for the Stop-gate (the deadlock guard), catch-up posture for missed runs, no wake-from-sleep. Single-machine SPOF is accepted and consistent with the threat model (git remotes are the backup).
- **Performance: ACHIEVED with one watch item.** audit-health ~1.4s/commit is fine; the real performance axis here is TOKEN/CONTEXT economics, and the system is unusually literate about it (context-budget read-scoping rule, ≤1,500-token floor, thin boot, marker-first consumption, render-layer fencing). Watch: PLAYBOOK's mass makes "read only the section you need" load-bearing; the TOC + chapter-map carry that, but #213 condensation protects it long-term.
- **Security/safety invariants:** keys discipline holds (secrets in `~/.secrets`, none in repo); hub-no-autonomous-cross-repo-write holds structurally (write-yes/commit-no reviewed at two ratify points; nothing schedules a cross-repo writer); OneDrive P0 — see RF-1 (the one real hole); plus `temp/` holding ~700MB personal/client scratch (passport scans, client pptx) inside the methodology working tree (#229, gitignored but a Three-Homes violation and a privacy exposure on any directory-level share/backup) — operator-gated, should actually happen.

---

## 4. Prioritized red-flag list (each with live evidence)

**RF-1 [safety, P0]** OneDrive guard does not cover Edit/Write, and the organ map claims it does. Evidence: `~/.claude/settings.json` PreToolUse matcher = `Bash|PowerShell`; ARCHITECTURE Ch2 row "every Bash/Edit/Write tool call ... fail-closed (P0)"; #191 filed P2 (from the #188 audit) — under-prioritized given the operator's data-loss history and Accept-Edits as daily driver. Fix is a small PreToolUse guard on Edit|Write|NotebookEdit `file_path` + correcting the map row; prove it with a fire_test-style seeded block (leg-e applies — it IS an enforcement organ).

**RF-2 [integrity]** The hub does not apply configured→armed→proven to itself. Evidence: `.pre-commit-config.yaml`'s own header ("changing this list does NOT install the pre-push hook... Without it the gate never fires"); direct-to-main `533109f` on 2026-06-26, six days after block-ff-push shipped, ratified as instance #3; consumers get SessionStart self-arm (`python -m pre_commit install`) via carriers while the hub's SessionStart has none; ai-council `bda4fff` evidently used `--no-verify` and no organ counts bypasses. The Informant measures consumer arming; NOTHING measures hub arming. Cheapest fix in the whole review: add the self-arm step to the hub's SessionStart + an audit check asserting `.git/hooks/{pre-commit,commit-msg,pre-push}` exist and are pre-commit-managed (deterministic, read-only, seconds).

**RF-3 [integrity, honesty-of-claims]** The Stop-gate's "un-gameable" is overstated in its canon. Dirty tree silences ALL legs including the hard one (`session_end_backpressure.check_journal_sha_anchor`: `if not _is_clean(): return None`); the CC block-cap force-ends a turn after N consecutive blocks (platform-side auto-override, witnessed and documented in the ADR-85 amendment). Both are reasonable engineering tradeoffs; neither is stated in DEFINITION_OF_DONE.md, which a fresh session reads as absolute. State the honest limits where the rule lives (the system's own "state honest enforcement limits" memory demands exactly this).

**RF-4 [integrity/modifiability]** Structural organ-collision resolved by paperwork: ADR-85's wrap-commit vs core-invariant #5 (3 ratified violations, #210 open). Also the register's per-instance pattern: a recurring same-class disposition should FORCE a rule decision at n=2 — #210 was derived by hand at n=3; make recurrence-detection a register-groom rule so the next collision surfaces itself.

**RF-5 [testability]** Leg-e does not reach the lived workflow. Evidence: the `cmd_checks` cp1252 crash (live, this session) vs the 2026-06-22 gotcha; `/handoff` v5 generator still #164 while bundles are produced by following the spec manually; PLAYBOOK Ch14 "smoke test" is prose. This is the operator's sandbox question — real, and the answer is a bounded harness, not a blanket rule (§6).

**RF-6 [decision-channel]** The heavy-decision organ drifted from its doctrine, and the record channel nearly leaked. Doctrine routes architecture/contested → Council (5-provider, blind vote); practice since mid-June routes → single-Mythos consults (ADR-87/90/92/94/95 all "Path A ... no Council transcript"), and ADR-94/95 both open with "Consult chat expired; this records the ... ruling" — two binding decisions reconstructed after their source context evaporated. The consult lane is legitimate (heterogeneity via Codex remains; council for genuinely contested forks) but it is UNWRITTEN: the complexity router doesn't name it, and there is no "record the ruling as ADR before the consult window closes" rule. Also: Council operationalization (#70, #96, #110 sycophancy-isolation audit) sits open while the organ it hardens is increasingly bypassed — decide whether Council is the standing organ or the escalation tier, and right-size the open work to that.

**RF-7 [modifiability]** Model-routing doctrine is smeared across un-reconciled L0/hub surfaces: `~/.claude/ROUTING.md` says "SONNET (default Claude Code session)" and global CLAUDE.md says "Tier 1 (Sonnet) ≤5 files"; PLAYBOOK §2/ESSENTIALS say "default Opus 4.8 — the floor; model is CC's pick". The manifest already knows ROUTING.md is uncovered ("candidate for future L0-payload coverage") — but the CONTENT contradiction is unfiled. A fresh session reading L0 first genuinely gets the opposite default.

**RF-8 [rot, low]** The check registry itself accretes: `handoff_bundle_structure` + `handoff_tag_canonicity` are v4-era checks running on every commit ("historical v4 surface"; tag_canonicity permanently reports section-not-found). Dead weight is small; the signal is that ALL_CHECKS has no retirement discipline — fold into P5 hub-self-prune. Same family: 6 undeclared-edge WARNs live-dispositioned pending #241; fine, but groom on schedule.

**RF-9 [ops hygiene, low]** Worktree-context degradation: in this worktree, `deployed_methodology_version` reports "fable-arch-review not listed" and `no_sibling_orphans` keys on the worktree name — audit checks silently change meaning off the primary checkout (the seed-state class already in memory). Cheap fix: checks that key on repo-dir-name should resolve the primary root (git-common-dir) first.

---

## 5. Harmony / equilibrium — the sociotechnical QA (the frontier)

Claim first: this system MAINTAINS its equilibrium, and does so by engineering rather than by hope — but the equilibrium is asymmetrically mechanized: strongest at the CC/repo boundary, prose-only at the browser boundary, and unmeasured at the operator.

### 5.1 Where entropy leaks, and what resists it (source → counter-tactic → residual)

- **Context degradation (long sessions):** countered by handoff v5 (CC-owned residual + thin boot + PROBES with FAIL-class teeth via `verify_handoff_probes` + supplement fill→fold). The 2026-07-03 bundle shows the whole chain WORKING: empty-supplement cold disposition defined, operator filled it, answers folded, probes re-bound, and the load-bearing "why" (#244 = lifecycle epic; P2 next; consult #2 MOOT) survived a chat boundary intact. Residual: the mid-course handoff cost is real but this is the correct tactic — degradation is a law, not a bug; the system's answer (externalize early, probe on re-entry) is the right one. STRONG.
- **Role-drift (architect defers to CC's framing):** named as "the recurring, witnessed failure" and countered by the HANDOFF_BOOT role-stability self-check + the plan-review output contract (exactly-one-of-three) + the orientation probe that cannot be bluffed from a summary. Honest limit: these are PROSE at the browser layer — no mechanism CAN run there; the mechanized halves (probes, verification split, "CC verifies state fidelity") are correctly placed on the CC side. Residual: the contract "recurs as a failure when softened to conversation" (BOOT's own words) — this stays a watched, re-taught surface. ADEQUATE, inherently un-mechanizable.
- **Held-by-memory decisions:** countered by ADR-per-ruling + JOURNAL SHA-seal + the supplement. Residual: the consult-expiry near-miss (RF-6) — the newest decision channel (Mythos consults) ran ahead of the record discipline. One-line rule fixes it.
- **Rot (add-only surfaces):** countered by doc_rot/doc_structure/doc_claims + condensation precedents (CLAUDE §12, ADR-49/65) + the essence-spec; residual: prune unbuilt (P2), gotchas/handoffs/checks unpruned. The operator's continuous-conformance vision (Opus decomposes → Sonnet binary per-file rot-verdicts → surface) is the right shape for the SEMANTIC tail of rot: it matches the two-tier doctrine (judgment reads, human ratifies), the t-shirt pins, and the funnel. Two design notes: (a) make the observers' verdict BINARY with a mandatory evidence_command (the conformance-hub.js finding schema already solved this — reuse it), else nightly LLM opinions become funnel noise; (b) gate it behind the existing n=2 adoption rule and a findings-acted-on metric — a nightly that surfaces nothing actionable in 2 weeks gets demoted to weekly, per the routine-value review (#123).
- **Version/state smear:** countered by release_lint (5 anchors → source_tag), deployed-versions.yaml, amendment_coherence, de-hardcode-first (#146). Residual: lint manual (wire at P2); ROUTING/PLAYBOOK model-default contradiction (RF-7).
- **Consumer-surface divergence:** countered by hash-guarded floor + Informant + fleet digest. Residual: #95 between-rollout template drift (filed), rosters declarative-only until P3.
- **Premature closure (easy-metric):** countered by hard-metric doctrine + ex-ante frozen contracts + ship-gate + educate-on-value; the floor saga → ADR-93 → #230 arc shows the system LEARNING this class end-to-end. Residual: the forced-false stamp shows proxy-gaming pressure persists; #222 landed the right fix pattern (decouple volatile claims from semantic stamps).
- **Operator saturation — THE UNMEASURED LEAK:** the funnel is the equilibrium's keystone (nothing binds unattended), yet nothing accounts for its load. Standing obligations now include: morning triage, `/review-closures`, weekly review, monthly Codex audit, quarterly grooming, changelog nudges, supplement fills, disposition rulings, D1–D3 decision queue, ratify-only digests (#130/#134...). Each is individually justified; the SUM is invisible. When the funnel saturates, ratification degrades to rubber-stamping — which re-opens every gate that assumes a genuine human check, silently. This is the one entropy source with NO counter-tactic. Cheapest gauge: a fleet_health line counting open ratification items + a per-routine findings-acted-on tally (#123 built out), reviewed at the weekly. If override-rate >10% means "tune the rules", define the analogous threshold for funnel backlog.

### 5.2 Degraded-and-restored, judged

The three incidents the mandate names are all REAL and all now have tactics: long-session degradation → handoff v5 (mechanized, probed); consumer-surface rot caught by eye → doc_claims/doc_rot + (pending) roster generation P3 + continuous-conformance; enforcement through unarmed windows → ADR-93/#230/#236 closed it for CONSUMERS — the remaining unarmed windows are the HUB'S OWN (RF-2) and the release path (release_lint). So: not one-offs — each was a symptom of a missing tactic, and in two of three cases the tactic has since been built. The equilibrium's real test is that pattern repeating: incident → named class → mechanism → leg-e proof. It is repeating. That is what "maintains, not drifts" looks like in evidence.

### 5.3 Equilibrium verdict

**ACHIEVED-AND-FRAGILE.** Achieved because the loop's transition gates exist, fire, and are taught at boot; fragile because (a) the operator-funnel has no load gauge, (b) the browser-side contract is prose by nature, and (c) the newest channels (consults; the about-to-multiply fleet) each need the record/arming discipline extended to them BEFORE volume arrives. The thesis's framework had no name for this QA; this system is the evidence it needs one.

---

## 6. The lived-workflow sandbox — dedicated evaluation

**Q1 — Is deployed-not-agent-tested a real testability red flag?** YES (RF-5), with a precise boundary. Leg-e's current scope (enforcement mechanisms) is right as a HARD gate; the gap is that non-enforcement organs (skills, commands, gotchas, the composed lifecycle) have NO observed-engagement standard at all — their "validation" is a prose checklist. But do NOT generalize leg-e as a uniform hard rule: engagement of a skill/gotcha is a probabilistic model behavior, not a deterministic gate — a fail-closed gate on LLM behavior is the false-positive death-spiral the check-against-spec scope note already refuses. Generalize the STANDARD (observed-in-a-real-run before "done"), split the VERDICT CLASS: deterministic organs/commands → provable, gateable; model-mediated engagement (skills/gotchas) → observed-and-reported, never gated. This is exactly the Informant's fire/hash/wired typing extended with one more class ("engaged" — evidence-graded, non-blocking).

**Q2 — The proposed CLI (headless session-in-session driving a test feature through the full lifecycle, with a state-observer logging triggers):** SOUND AS AN EPISODIC HARNESS, and the corpus already contains 80% of its parts. floor_conformance proved clone+inject+assert; the Informant proved fire-verdicts + honest vocabulary; conformance-hub proved schema-bound findings with mandatory evidence_command; #106 (Auto Mode) and ADR-68's worktree hygiene cover the run mechanics. The harmony test it must pass: the INNER agent never closes its own verify loop — LESSONS 2026-06-04 (verify by state, never narration, proven twice) makes self-certification inadmissible. Design consequence: the observer is the OUTER, deterministic layer (transcript + git state + hook stdout parsing), the inner session is just the stimulus generator, and the report lands in the operator funnel like every other judgment output. Done that way it STRENGTHENS the equilibrium (it converts "deployed-not-tested" entropy into funnel signal); done as an agent grading itself it would inject exactly the narration-trust failure the methodology exists to kill.

**Q3 — The three forks, resolved:**

- **SPAWN:** `claude -p` headless inside a THROWAWAY CLONE of a synthetic (or cloned real) consumer — the fire_test/floor_conformance precedent — not a worktree (shared `.git`, shared stash, gitignored-state seeding class, audit checks that mis-key off dir names: RF-9), not a container (adds a platform the operator does not run; Windows-native fidelity is the point — half the gotchas are Windows-specific). Environment is part of the spec (LESSONS 2026-06-05): scrub/pin the env explicitly — the `$CLAUDE_PROJECT_DIR` trap is already precedent (#237 chose git-toplevel-first for exactly this), and the settings surface must be isolated (a temp `CLAUDE_CONFIG_DIR` or explicit `--settings`) or the child inherits the outer machine's L0 hooks and the observer measures the workstation, not the deployment. Budget: session model Sonnet (mechanical lifecycle-driving), observer deterministic, triage-only LLM — per the t-shirt doctrine; never Opus-by-inheritance.
- **SCOPE:** v1 = deterministic surface only — hooks fire (SessionStart/Stop/PreToolUse/pre-commit/commit-msg/pre-push through a real branch→edit→commit→wrap arc) + commands expand and act (`/override`, `/review-closures` against a seeded proposal, `/ship` refusal cases). v2 = skill/gotcha ENGAGEMENT as observed-and-reported (transcript shows the SKILL.md read / the gotcha consult on a seeded trigger) with a rate, not a gate. Full-workflow (browser-in-the-loop) stays out — the browser layer cannot be spawned headlessly and its contract is prose by design (§5).
- **ORACLE — the decisive fork, and P1 already built the answer: THE ESSENCE-SPEC IS THE ORACLE.** Manifest components already declare kind, artifacts, wiring, and a verify class; extend each with an `engages:` expectation (trigger scenario → expected observable: hook stdout JSON / exit code / transcript event / command output marker). Expectations-from-spec is what turns the observer log from noise into signal: every trigger event is diffed against the component table — fired-as-expected / fired-unexpected / EXPECTED-BUT-SILENT (the class nothing else can see). No spec entry, no assertion — which also makes coverage growth an explicit spec edit (reviewable), not scenario sprawl.

**Q4 — Placement vs the Informant, and worth:** it is the INTEGRATION-LEVEL COMPLEMENT — fire_test proves one organ in isolation (unit); the sandbox proves the composed lifecycle end-to-end on one machine-fidelity run (integration). Do not make it a nightly: it is EPISODIC by the two-tier doctrine — run it at release/deploy moments (the P2 prune acceptance NEEDS exactly this harness: "removed AND verified absent AND nothing-else-broke" is an end-to-end property), after CC platform upgrades (the re-probe rule), and at consumer onboarding (#221's per-repo acceptance alongside #230). Cost check: a Sonnet-driven scripted lifecycle run is minutes and cents; the build cost is the oracle table — which P1 already 80%-built. Worth it, sequenced WITH #244 P2 (its first paying customer), filed as its own BACKLOG item with an ex-ante contract per ADR-81 discipline. It is not over-engineering PROVIDED the three refusals hold: no nightly cadence, no LLM-judged gating, no container. (Also fold RF-2's hub-arming check into its preconditions — a sandbox on an unarmed hub would measure a facade.)

---

## 7. What is missing / what not to add

**Missing (each tied to a QA / entropy source):**

1. Edit/Write `file_path` guard for the P0 zone + map correction (RF-1; safety).
2. Hub self-arming + an armed-state audit check (RF-2; integrity — closes the configured-not-armed class at its last unguarded ring).
3. Honest-limits paragraph in DEFINITION_OF_DONE (RF-3; integrity-of-claims).
4. #139 merged-arc→record verifier BEFORE fleet rollout (self-audit §7.8; the untracked-deploy-build proved the class; fleet volume multiplies it).
5. ASCII-output regression test over CLI-printed strings + the `cmd_checks` fix (RF-5's concrete instance; mechanizes the #1 gotcha — gotcha-to-gate promotion).
6. The sandbox harness, scoped per §6 (testability; leg-e's outward ring).
7. Register-recurrence rule: ≥2 same-class dispositions force a rule decision (RF-4).
8. Consult-lane codification: one PLAYBOOK router line + "ADR lands before the consult window closes" (RF-6; decision-channel record discipline).
9. Operator-load gauge: fleet_health counts open ratification items; weekly review reads it (the §5 unmeasured leak).
10. ROUTING.md ↔ PLAYBOOK model-default reconciliation (RF-7).
11. release_lint wired into deploy preflight at the P2/v1.2.0 boundary (deployability).
12. PLAYBOOK freshness posture decided explicitly: either add `last_reviewed` or record why the constitution is exempt (it is currently the only load-bearing living doc outside the gate, silently).

**What NOT to add (over-engineering to refuse):**

- No LLM-judged hard gates on semantic properties (reviewedness, engagement, prose drift) — the advisory-by-design stance on the open-world half (self-audit §7.4) is correct and permanent; keep judgment read-only + funneled.
- No transclusion engine while detection suffices (#180 stays gated on DEC-04; the drift-surface it would remove is small vs the machinery it adds).
- No second conformance organ; no per-component semver (both rightly rejected already).
- No scheduled active-push deployer (breaches autonomy-no; drift-catch + consumer-pull per carrier is the model).
- No container layer for the sandbox; no nightly cadence for it.
- No new per-session hard gates during the ADR-85 scope-freeze — the Stop-gate's false-positive budget is the equilibrium's most precious asset; spend it on data.

---

## 8. Overall verdict + roadmap

**Verdict: ARCHITECTURALLY SOUND** — a coherent, evidence-driven, self-correcting design whose failure classes are named, mechanized, and (unusually) honestly bounded. The system passes its own thesis-derived tests where it has finished building, and its open gaps are almost all ALREADY FILED — the review's contribution is mostly re-ordering: safety edge first, self-arming second, record-discipline for the new channels third, then the prune epic with the sandbox as its instrument. Grade by QA: modifiability ACHIEVED · deployability ACHIEVED@n=1/AT-RISK-fleet · integrity AT-RISK (arming + P0 edge) · testability ACHIEVED-organs/AT-RISK-workflow · equilibrium ACHIEVED-AND-FRAGILE (unmeasured funnel).

**Roadmap (sequenced; each with a demonstrable acceptance criterion):**

1. **P0 edge (RF-1):** Edit/Write/NotebookEdit `file_path` OneDrive guard + ARCHITECTURE row fix. Accept: seeded Edit to an excluded path is blocked fail-closed in a test; normal-path edit passes; map row matches live matcher.
2. **Hub arming mesh (RF-2):** SessionStart self-arm (pre-commit install, all 3 hook types) + audit check `hooks_armed`. Accept: on a fresh clone the first session arms all three; deleting `.git/hooks/pre-push` turns the next health run non-green.
3. **Truth-in-canon (RF-3 + RF-7):** DEFINITION_OF_DONE honest-limits note; ROUTING.md reconciled to the Opus-floor/CC's-pick doctrine. Accept: a fresh session reading only L0 states the correct default; DoD names the dirty-tree and block-cap bounds.
4. **cp1252 fix + ASCII-output test (RF-5).** Accept: `audit.py checks` runs clean on a cp1252 console; the test goes red if any CLI-printed string gains a non-cp1252 glyph.
5. **#139 merged-arc verifier + register-recurrence rule + #210 shape decision (RF-4).** Accept: a seeded merged arc with no item/closure/no-item-class is flagged; a 2nd same-class disposition emits a "promote to rule" finding; a JOURNAL-only direct commit passes while a code-touching one still WARNs (or wraps move behind `--no-ff`).
6. **Consult-lane codification (RF-6).** Accept: the complexity router names the consult tier; the next consult's ruling exists as an ADR before its chat expires (n=1 witnessed).
7. **#244 P2 PRUNE + sandbox v1 (§6), release_lint→preflight, then #221 fleet with per-repo #230-class acceptance.** Accept: a tombstoned component is removed from ai-council and VERIFIED ABSENT by the harness; release_lint failure blocks `--execute`; each fleet repo's deploy closes on its own green acceptance run.
8. **Grooming wave (RF-8 + thesis-conclusion-2 debt):** retire/sunset the two v4 checks, #130 gotchas hygiene n=1, #212 handoff-retention ruling, #213 PLAYBOOK condensation, #229 `temp/` clearance. Accept: each surface has either a prune commit or a recorded keep-with-reason.
9. **Operator-load gauge (§5).** Accept: fleet_health prints the open-ratification count; two weekly reviews consume it; a threshold analogous to the 10% override rule is recorded.

---

*End of review. Read-only analysis session; this artifact is the session's only repo write (operator-directed landing in `docs/audits/`). Implementation is a separate, later effort.*
