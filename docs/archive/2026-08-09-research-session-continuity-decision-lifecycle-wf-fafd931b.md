# Session Continuity and the Decision Lifecycle for an LLM-Agent Fleet: A Decision-Ready Assessment

## TL;DR
- Your architecture is **ahead of common practice on session handoff and enforcement, but behind on retirement**: the industry has no exact analogue to your probe-gated, answer-withheld bundle (genuinely unusual — keep it), yet it has mature, adoptable answers for your birth-rate problem (Kanban WIP limits, RFC/PEP rejection states) and for the "ruled-but-unverified" gap (architecture fitness functions, ADR-to-code traceability, policy-as-code via Conftest — all local-first, no SaaS).
- **Both operator hypotheses are supported** by cross-domain evidence. Plan-should-travel maps directly to I-PASS's "Action List + Situation Awareness/Contingency" and to After-Action Review, where debriefs "improve effectiveness over a control group by approximately 25% (d = .67)" (Tannenbaum & Cerasoli, *Human Factors* 2013). Verification-at-cut-not-boot maps to I-PASS "Synthesis by receiver" read-back and to release-engineering freeze gates: the outgoing party owes the incoming party a *verified* state, and the receiver must re-derive rather than accept.
- **Adopt three mechanisms now:** (1) capped intake with an explicit **Parked/Rejected** home so ideas stop being relitigated; (2) **ADR sunset/review dates** plus a superseded-not-deleted retirement path; (3) an **audit-finding-to-backlog forcing function** and an **ADR-landing predicate** (a fitness function per accepted ADR) wired into your existing audit.py and pre-push hooks. Drop nothing structural; trim only the boot-time pass-table verbosity.

## Key Findings

**1. Session continuity is real but immature; your bundle is unusually rigorous.** The 2025–2026 stack is: instruction files (CLAUDE.md, `.cursor/rules`, AGENTS.md), context compaction (`/compact`, `/clear`), vendor memory (Claude Code auto-memory / Session Memory; Cursor Memories, shipped v1.0 June 2025), session resume/fork (`claude --continue`/`--resume`), committed scratchpads, plan/spec files (spec-kit, Kiro, BMAD, OpenSpec), issue-tracker-as-memory, and handoff docs (HANDOVER.md conventions and community skills). Compaction and resume/fork are **documented vendor features**; handoff bundles are almost entirely **community convention**. No published practice matches your probe-manifest-with-withheld-answers design.

**2. Compaction has documented failure modes that justify distrust of plausible summaries.** "Context rot" (Chroma Research, July 2025, 18 frontier models incl. GPT-4.1, Claude Opus 4, Gemini 2.5) and "lost-in-the-middle" (Liu et al., TACL 2024) are established **research findings**. This is the empirical backbone for your withheld answers: a compacted summary is exactly the artifact that reads confident and is quietly wrong.

**3. Human handoff protocols strongly endorse both your hypotheses.** I-PASS (Starmer et al., *Pediatrics* 2012; *NEJM* 2014) and SBAR (US Navy origin) mandate that the **outgoing** party supply an Action List and contingency plan, and that the **receiver** performs "Synthesis by receiver": summarizes what was heard, asks questions, restates key actions. Aviation/incident-command practice (NASA flight-controller handover logs, ICS Form 201, GitLab SRE on-call handover) uses a written log by the outgoing party plus a face-to-face briefing; the Joint Commission requires record-and-read-back.

**4. Planner/executor separation is a recognized pattern with measured benefits and known failure modes.** Anthropic reported its orchestrator-worker research system beat single-agent Opus 4, but the same sources warn the split *hurts* tightly-coupled work like coding and burns 4–15× tokens. The planner-hallucinating-repo-state failure is precisely what your probe manifest defends against.

**5. The decision lifecycle has mature models with an explicit rejection state your model is missing.** Rust RFCs and Python PEPs both have first-class terminal/parked states. Your model is right that intake may be rejected and that an ADR = decision-taken, but it lacks a durable **home for the rejected idea** and a **Proposed/provisional** state before an ADR is accepted.

**6. Retirement practices exist and are contested — which is itself the finding.** ADR practice (Nygard, MADR, Log4brains) is explicit: ADRs are immutable; you supersede/deprecate, never delete. Backlog "bankruptcy" and stale-bots are real, used, and genuinely disputed. Kanban WIP limits and Little's Law give the rigorous version of your birth-rate insight: bounding intake, not raising throughput, is the lever.

**7. The "ruled-but-unverified" gap has a named industry answer.** Architecture fitness functions (ArchUnit, dependency-cruiser, import-linter, go-arch-lint) + policy-as-code (OPA/Conftest, local, single binary, no server) + ADR-to-code traceability operationalize a decision. The published rule: every non-retired ADR should map to at least one fitness function.

## Details

### Q1 — Session continuity: what the industry actually does (2025–2026)

**Documented vendor features.** Claude Code: `/compact` (summarize-and-continue), `/clear` (fresh context), `--continue`/`--resume` persistence, CLAUDE.md re-injected from disk after compaction, and auto-memory. "Session Memory" (background-written summaries enabling instant compaction) exists from ~v2.0.64 (late 2025); visible "Recalled/Wrote memories" messages appeared around v2.1.30–2.1.31 (early Feb 2026); it is gated behind the `tengu_session_memory` Statsig flag and requires Anthropic's native API (not Bedrock/Vertex/Foundry). Anthropic's docs are explicit that memory files are "context, not enforced configuration" — "To block an action regardless of what Claude decides, use a PreToolUse hook instead." **That sentence is your "instructions are requests, mechanisms are guarantees" philosophy, stated by the vendor.** Cursor Memories shipped v1.0 (June 2025), per-project, background-model-proposed and user-approved. Spec-driven tools (GitHub Spec Kit, AWS Kiro with Requirements/Design/Tasks + EARS notation + agent hooks, BMAD-METHOD's versioned PRD/architecture/story artifacts, OpenSpec's delta specs) make the durable artifact the spec, which "persists across sessions and team members."

**Community conventions.** CLAUDE.md + HANDOVER.md pairs; committed sequential HANDOFF.md files; the aihero `/handoff` skill; softaworks session-handoff (a subagent inspects git status, diffs, and tests, then writes HANDOVER.md); danielrosehill Agent-Handover; the Claude-Handover plugin (handover file `git rm`'d but not committed — "ephemeral infrastructure, not project documentation"). A community SessionStart hook surfaces the latest handoff "as context, not instructions — suggested actions must be verified against current state before executing" — the community's version of your non-bluffable rule, but as a warning rather than a mechanism.

**Is your probe-gated, answer-withheld bundle unusual? Yes — genuinely.** Nothing found publishes a design where the incoming architect is deliberately denied the answers and must have the executor re-derive load-bearing facts live. The community consistently gestures at the problem ("watch for confident claims the session never actually verified: 'X isn't built', 'Y is done'") but stops at a warning. You have converted the warning into a mechanism. **(Report synthesis: this is your single most defensible novelty; preserve it and document it as a named pattern.)**

### Q2 — Handoff quality and verification; hypothesis (2)

**Making a summary non-bluffable (research finding).** SelfCheckGPT samples multiple responses and flags low-consistency spans as likely hallucinated; NLI-based and QA-based (Q-S-E) consistency checks detect entity/quantity/causal distortions; the 2026 survey "Summarization is Not Dead Yet" lists faithfulness verification as still-open. The robust techniques reduce to **re-derivation and cross-checking against source**, not trusting a single pass — exactly your withheld-probe logic.

**Verification-at-freeze vs verification-at-consume (hypothesis 2): SUPPORTED across three literatures.**
- *Aviation/medical handoff:* I-PASS puts "Synthesis by receiver" at the moment of transfer. AHRQ's TeamSTEPPS I-PASS tool defines it verbatim: "**Synthesis by Receiver — Receiver summarizes what was heard; Asks questions; Restates key actions/to-do items.**" The read-back happens at cut/transfer, and the Joint Commission mandates record-and-read-back before acting.
- *Release engineering:* freeze-time gates (CI green at the tag/freeze) are the norm; the consumer receives a signed, verified artifact plus exceptions, not a re-run of every test.
- *Incident command:* ICS Form 201 is "a written record of the incident as of the time prepared," produced by the outgoing commander at transfer.

**What the outgoing party owes the incoming party:** an explicit action list, a contingency/"what might happen" plan, current state as-of-freeze, and pending items — and the incoming party owes a read-back. This is a near-exact spec for your residual (why + drift flags) + supplement (outgoing author) + probe (forces receiver read-back). **From the evidence: run the probe/verification at CUT, have the executor re-derive and record pass/fail into the frozen bundle, and hand the incoming architect only the exceptions plus the read-back obligation.** Your hypothesis is the safety-critical-industry default.

### Q3 — Plan-and-outcome continuity; hypothesis (1)

**Plan-should-travel (hypothesis 1): SUPPORTED.**
- *After-Action Review / debrief (direct evidence):* Tannenbaum & Cerasoli, *Human Factors* 2013 (vol. 55(1), pp. 231–245; PMID 23516804), a meta-analysis of 46 samples (N = 2,136): "Findings from 46 samples (N = 2,136) indicate that on average, debriefs improve effectiveness over a control group by approximately 25% (d = .67)… Organizations can improve individual and team performance by approximately 20% to 25% by using properly conducted debriefs." The AAR mechanism is definitionally planned-vs-actual: it "begins with a clear comparison of intended versus actual results achieved." Keiser & Arthur (*J. Applied Psychology* 2020) corroborate that AARs improve task performance.
- *Pre-mortem (planning-side counterpart):* Klein, *HBR* Sept 2007, citing Mitchell, Russo & Pennington (1989, *J. Behavioral Decision Making* 2(1):25–38): "prospective hindsight—imagining that an event has already occurred—increases the ability to correctly identify reasons for future outcomes by 30%." (Caveat: prospective, the conceptual opposite of carrying a realized outcome forward; cite as complementary, not direct support.)
- *Agent-specific practice:* spec-driven development keeps the spec as the durable artifact agents "execute against, verify against, and report against."

**Minimum viable form of "planned / landed / remains + why":** the I-PASS Action List + Patient Summary ("events leading up to… hospital course… ongoing assessment… contingency plan") is the field-tested minimal shape. Mapped to your fleet: (a) the previous session's plan; (b) a diff of what landed vs. what did not (from git state, re-derived by the executor at cut); (c) remaining items with a one-line "why" each; (d) drift flags. This is your residual, made to carry the plan explicitly. **Adopt hypothesis 1.**

### Q4 — Browser↔executor division of labour

**What the reasoning-with-web model does better:** breadth-first research, library/dependency selection (open-web comparison), planning/decomposition, trade-off judgment, prompt/contract authoring, and review — all "what/why" work. Anthropic's own guidance: multi-agent/orchestrator patterns excel at "breadth-heavy research" and are "less effective for tightly interdependent tasks such as coding." **What the repo-resident executor does better:** anything requiring ground truth — running tools, reading actual files, tests, commits, and re-deriving state.

**Does separation measurably help?** Yes for breadth/long-horizon, with two headline data points to cite precisely: Anthropic's "How we built our multi-agent research system" reports an Opus 4 lead + Sonnet 4 subagents setup "outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval," that on the BrowseComp benchmark "token usage by itself explains 80% of performance variance" (rising to ~95% with tool-call count and model choice), and that "multi-agent systems use about 15× more tokens than chats." Prasad et al.'s ADaPT (NAACL 2024 Findings, arXiv:2311.05772) reports "success rates up to 28.3% higher in ALFWorld, 27% in WebShop, and 33% in TextCraft" over ReAct/Plan-and-Execute baselines. But the same sources warn the split *hurts* tightly-coupled work and burns 4–15× tokens. **Failure modes:** plan drift, over-planning, subagents duplicating work absent explicit boundaries (Anthropic's example: one subagent researched the wrong time period while others duplicated it, fixed with explicit objectives/boundaries), and — most relevant to you — **the planner hallucinating repo state.**

**What should minimally live in the architect's head:** the decision and its rationale, the frozen contract/invariants, the plan and its acceptance criteria, and the trade-off record. Everything that is a *fact about the repo* should be delegated to the executor and re-derived, never remembered. **(Report synthesis: your Layer-1's "no filesystem access" is not a limitation to work around; it is the enforcement mechanism that prevents the planner-hallucinates-repo-state failure. Keep it.)**

### Q5 — The decision lifecycle end-to-end

**RFC/PEP as the reference model.**
- *PEP states* (PEP 1): Draft → (Deferred | Rejected | Withdrawn | Accepted/Provisional → Final | Superseded). "Withdrawn" = the author concluded it's a bad idea or a competitor is better; "Rejected" is recorded with a linked resolution post; "Provisional" = accepted-but-reversible.
- *Rust RFC:* a Final Comment Period (10 days, publicized in "This Week in Rust") precedes accept/close/postpone; "postponed" is a closed-but-re-openable parking state; low-quality or previously-rejected proposals are closed fast.
- *Where "rejected" is recorded and kept from relitigation:* in the numbered, permanent archive with a resolution link — the record *is* the anti-relitigation mechanism (you point at it when the idea returns). "Proposals for previously-rejected features… may be quickly rejected" (Rust RFC book): the recorded rejection is reused as a decision. (Practitioner consensus, not a controlled study.)

**Mapping to your model — right and missing.**
- Right: "intake = idea that may be rejected"; "ADR = decision to implement taken"; "backlog = execution / if-yes-no tree"; "rejection must have a home."
- **Missing state 1 — a Proposed/Provisional ADR:** between intake-accepted and ADR-final there is a review window (PEP Provisional, Rust FCP). Your ADRs jump straight to immutable-accepted; add a short Proposed status so "testing shows it wrong" has a graceful path that isn't a separate amendment act.
- **Missing state 2 — a durable Rejected/Parked intake home:** PEP Rejected/Withdrawn/Deferred and Rust "postponed." Your ~150 un-adjudicated closure proposals and 15/33 expired "deferred-until-X" pegs are the exact symptom of not having enforced terminal states with owners and dates.

### Q6 — Retirement, archiving, deletion (the hardest part)

**ADRs (community convention + tool docs).** Immutable; "Only its status can change. Thanks to this, your documentation is never out-of-date" (Log4brains/MADR). You supersede (new ADR references old; old set to "Superseded by ADR-XXXX") or deprecate; you don't delete. This *validates* your immutable-by-policy stance — the ADR set growing is correct; the missing piece is a **review/expiry** to move stale ones to deprecated. pyadr (Python) manages the proposal/accept/reject/supersede lifecycle programmatically.

**Sunset clauses / periodic review (cross-domain).** Law and contracts use fixed-term or trigger-based expiry to force "periodic reassessment" and prevent "accumulation of obsolete" rules. Directly portable: add `review_date` (and optionally `expires`) front-matter to each ADR; an ADR past its review date without reaffirmation flips to "needs review," surfaced by audit.py. (A real ADR README in the wild — ATLAS-GATE-MCP — already models `review_date` front-matter.)

**Backlog hygiene at scale (contested).**
- *Backlog/bug bankruptcy* — used and defended: Mountain Goat Software ("declare Backlog bankruptcy," archive all, resurrect on request); a ProductPlan PM deleted ~600 items with "no repercussions" and the lesson "if an idea has high enough value… it will come back." Critics: bugs get buried in Closed, duplicates refile, triage is lost (Bicheng Cao: bankruptcy "throws all bugs back into the cabinet"). Consensus: bankruptcy relieves cognitive load but does not fix birth rate.
- *Stale-bots* — widely deployed (probot/stale defaults: 60 days to stale, 7 to close; actions/stale) and widely criticized (nostalebots.xyz: "glorified footgun"; a GitHub community discussion petitions to ban auto-close; the well-known case of a stale-bot closing the very issue asking it not to). The defensible middle: **label-only, never auto-close** — "There is value… in stale bots that only label and never close."
- *WIP limits / Little's Law (research-grounded):* WIP = throughput × cycle time; bounding WIP (arrival rate λ vs service rate μ) prevents queue blow-up. This is the rigorous statement of your birth-rate finding: with ~161 open rows, ~73% born in the last 30 days, and throughput roughly fixed, **the only lever you fully control is intake.** Kanban prescribes an explicit intake cap and pulling new work only when capacity opens.

**Thresholds practitioners use to call an item dead:** stale-bot defaults cluster at 60 days inactive → stale, +7 → close; sunset reviews commonly start 60–90 days before expiry. **(Report synthesis: for your fleet, tie "dead" to birth-cohort aging — an intake proposal un-adjudicated for N days auto-moves to Parked with a required one-line reason, not silent deletion.)**

### Q7 — The "ruled-but-unverified" gap

**Named pattern: architecture fitness functions + ADR-to-code traceability.** Fitness functions are "automated tests that verify your codebase adheres to architectural decisions," run in CI to "fail the build when architectural rules are violated." Tools: ArchUnit (Java, gold standard), dependency-cruiser (JS), NetArchTest (.NET), go-arch-lint (Go), and — for Python/polyglot — **import-linter** and custom AST tests. The operational rule (DEV/platformtoolsmith, 2025–2026): map "an ADR → a fitness function"; "every ADR that isn't explicitly deprecated or superseded should map to at least one fitness function," filter inclusively (check proposed too), and run against every PR diff.

**Policy-as-code, local-first, no server.** **Conftest** is "a small open-source CLI from the same [OPA] project… ships as a single binary that drops into a CI pipeline," evaluates Rego against JSON/YAML/config, and "runs completely locally… doesn't make network requests." This satisfies your no-SaaS/no-server constraint exactly: OPA-the-server is *not* required; Conftest is the right tool. Wiring: pre-commit (fast local) → CI gate (a `deny` fails the build) → optional pre-apply.

**How this fills your gap.** A "decision-landing predicate" is a fitness function per accepted ADR asserting the ruling is actually present in code. Your audit.py's ~41 checks are already home-grown fitness functions; the missing organ is the **binding from each accepted ADR to at least one such check**, so a half-landed ruling fails audit. **(Report synthesis: this is the highest-value adoption — it directly kills the ruled-but-unverified defect class.)**

### Q8 — Synthesis for this fleet

**Keep (already ahead of common practice):** probe-gated answer-withheld bundle; boundary invariants refusing a cut on open batch/dirty worktree; Layer-1 no-filesystem enforcement; immutable ADRs; count ratchets; mechanisms-over-instructions philosophy (Anthropic's own docs concede instructions aren't guarantees — hooks are).

**Adopt (with plug-in point):**
1. **Plan-carrying residual** (hypothesis 1) → residual gains a "planned vs. landed vs. remains+why" section, populated by the executor re-deriving git state at CUT. Plug-in: bundle-cut step + audit.py check that the section is non-empty.
2. **Verification-at-cut, exceptions-only boot** (hypothesis 2) → probe answers computed at freeze, stored in the bundle; incoming architect receives only failures + a read-back obligation. Plug-in: pre-push hook at cut; boot loader filters to exceptions.
3. **Intake WIP cap + Parked state** → hard cap on open intake; new intake beyond the cap forces adjudication of an old one. Plug-in: audit.py ratchet on open-intake count; a `parked/` location with a required reason.
4. **ADR review/sunset dates + Proposed state** → `review_date` front-matter; overdue → "needs review"; add a Proposed→Accepted transition. Plug-in: audit.py date check; optional pyadr for lifecycle.
5. **Audit-finding-to-backlog forcing function** → every audit finding must emit either a backlog row id or an explicit "no-action + reason." Plug-in: audit.py fails if a finding has neither. Kills "audits for audits' sake."
6. **ADR-landing predicates (fitness functions)** → each accepted ADR maps to ≥1 check (import-linter / Conftest / pytest). Plug-in: an audit.py registry mapping ADR→check; an unmapped accepted ADR is a failing check.

**Drop (ceremony not earning its keep):** the boot-time table of passes (replace with exceptions-only, per hypothesis 2); any manual "audit report" that does not emit backlog rows (fold into the forcing function). Do **not** adopt SaaS stale-bots or backlog bankruptcy as a first resort — both are contested and neither fixes birth rate; use label-only aging + a WIP cap instead.

**Local-first / library-first flags:**
- Policy-as-code: use **Conftest** (single binary, local) — do **not** stand up OPA-the-server. ✔ no SaaS.
- ADR lifecycle: **pyadr** (Python) or plain markdown + front-matter before reaching for **Log4brains** (Node/Next.js dependency — a heavier bring-in for a static site you may not need). Hand-rolling status transitions is justified only if pyadr's divergence is measured first.
- Fitness functions: **import-linter** (Python, pip) plus your existing audit.py cover this; no new service.
- Stale handling: GitHub `actions/stale` in **label-only** mode if you already use Actions; otherwise a local audit.py aging check — no bot server.

### Source classification (as requested)
- **Documented vendor feature:** Claude Code `/compact`, `/clear`, `--continue`/`--resume`, auto-memory, Session Memory, PreToolUse hooks; Cursor Memories v1.0; Kiro/Spec Kit/BMAD/OpenSpec artifacts; AHRQ I-PASS tool wording; probot/stale & actions/stale defaults; Conftest local execution.
- **Community convention:** HANDOVER.md/HANDOFF.md patterns, aihero/softaworks/danielrosehill handoff skills, ADR-to-fitness-function mapping, backlog bankruptcy, "label-only" stale handling, Cursor Memory-Bank repos.
- **Research finding:** context rot (Chroma 2025), lost-in-the-middle (Liu et al., TACL 2024), SelfCheckGPT/NLI faithfulness, planner/executor gains (Anthropic internal eval; ADaPT NAACL 2024), debrief meta-analysis (Tannenbaum & Cerasoli 2013), I-PASS outcomes (NEJM 2014), pre-mortem/prospective hindsight (Klein 2007; Mitchell/Russo/Pennington 1989), Little's Law/WIP.
- **Report synthesis (my own):** the probe bundle as a named novelty; "no-filesystem as enforcement, not limitation"; ADR-landing predicate as the missing organ; birth-cohort aging → Parked; the proposed state machine below.

## Recommendations

**Stage 1 (this week, S) — stop the bleeding on birth rate.**
- Set a hard WIP cap on open intake and open backlog cohorts; encode it as an audit.py ratchet (must-never-exceed baseline — you already have the ratchet machinery). *Threshold to change course:* if net backlog does not trend down over 3–4 cut cycles, tighten the cap; do not add throughput.
- Add a `parked/` home with a required one-line reason and a pointer back to the audit/intake it came from. Migrate the ~150 un-adjudicated closure proposals here in one pass — a *targeted* bankruptcy that archives rather than deletes, so items can resurface.

**Stage 2 (this month, M) — close the ruled-but-unverified gap; force findings to land.**
- Build the ADR→check registry: every accepted ADR names ≥1 fitness function (import-linter rule, Conftest policy, or pytest). An accepted ADR with no mapped check fails audit.py. Start with 3–5 load-bearing ADRs, then expand.
- Make audit findings emit either a backlog row id or an explicit dispositioned "no-action + reason"; audit.py fails otherwise. *Threshold:* if findings-without-rows recur, promote the check from warn to hard-fail at pre-push.

**Stage 3 (this quarter, M/L) — make the handoff carry plan+outcome and verify at cut.**
- Move probe execution to CUT; store pass/fail in the frozen bundle; boot delivers exceptions + a mandatory executor read-back (Synthesis-by-receiver). This is the I-PASS-validated shape.
- Add the "planned vs. landed vs. remains+why" section to the residual, auto-populated from git at cut.
- Add `review_date` front-matter to ADRs and a Proposed status; overdue ADRs surface as "needs review." *Threshold:* if the ADR set keeps growing with zero deprecations after two review cycles, your review cadence is too slow — shorten it.

**Benchmarks that would change the plan:** if net backlog falls consistently under the WIP cap and expired "deferred-until-X" pegs drop to near-zero, relax intake friction. If ADR-landing predicates catch zero half-landed rulings over a quarter, the gap was smaller than believed and you can reduce check density. If read-back-at-boot measurably slows sessions without catching bluffs, revert to a lighter exceptions summary.

## Proposed State Machines (report synthesis)

**Intake (idea that may be rejected):**
`Proposed` → `Under-Review` → { `Accepted→ADR` | `Rejected` (terminal, reasoned, archived) | `Parked/Deferred(until X or N-days)` (re-openable) }
- Every non-`Accepted` terminal requires a one-line reason and an owner; `Parked` requires a trigger or expiry date. Relitigation is answered by pointing at the recorded `Rejected`/`Parked` record.

**ADR (decision to implement, immutable):**
`Proposed` → `Accepted` → { `Deprecated` | `Superseded-by(ADR-N)` }, with `review_date` front-matter; overdue → `Needs-Review` (surfaced by audit.py, not a new status class). No deletion, ever. Each `Accepted`/`Proposed` ADR must map to ≥1 fitness function (landing predicate).

**Backlog row (execution of an accepted ADR — an if-yes/no tree):**
`Ready` → `In-Progress` (subject to WIP limit) → { `Done` (landing predicate green) | `Blocked(reason)` | `Parked(reason)` | `Dropped(reason, archived)` }
- A row cannot enter `Done` until its ADR's landing predicate passes (this is where ruled-but-unverified is caught). Intake into `Ready` is capped; exceeding the cap forces adjudication of an existing row.

## Caveats
- **Contested practices, presented as such:** backlog/bug bankruptcy (relief vs. buried duplicates) and stale-bots (deployed vs. "footgun") are genuinely disputed; the report recommends the label-only / archive-not-delete middle path rather than endorsing either pole. Planner/executor separation helps for breadth but is documented to *hurt* tightly-coupled work like coding — do not over-generalize the 90.2% figure.
- **Source quality:** the 90.2% and 15× figures are Anthropic's own internal-eval reporting (vendor source, not independent replication). Spec-driven "first-pass success" multipliers are early-adopter reports, not controlled studies. Context-rot and lost-in-the-middle are peer-reviewed/replicated; treat those as solid.
- **Hypothesis status:** both operator hypotheses are **supported by analogy** to safety-critical human-handoff and debrief literature and to release engineering; neither has been tested in a controlled study *on LLM-agent fleets specifically*, so the support is strong-but-indirect (RESEARCH FINDING by analogy, not direct measurement on this class of system).
- **Vendor volatility:** Claude Code Session Memory is behind a Statsig flag with a gradual rollout and a native-API requirement; availability may differ on your plan. Cursor Memories behavior is disputed by some users vs. its own docs. Verify current behavior against release notes before depending on either as a mechanism.
- **Numbers cited precisely:** the *NEJM* 2014 I-PASS study (10,740 admissions) found "the medical-error rate decreased by 23%… (24.5 vs. 18.8 per 100 admissions, P<0.001), and the rate of preventable adverse events decreased by 30% (4.7 vs. 3.3 events per 100 admissions, P<0.001)," with "significant error reductions at six of nine sites." The "30%" refers specifically to preventable adverse events; overall errors fell 23%; the effect was not uniform across sites.