# Architect strategic supplement — 2026-07-06-dev-knowledge-architect

Repo: dev-knowledge · Mode: architect · Date: 2026-07-06

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the
   repo.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

# SUPPLEMENT ANSWERS (enriched) — outgoing architect wrap · 2026-07-06
# Paste into the outgoing bundle's ANSWERS region (replaces the earlier compressed draft).

## Q1 — Strategic intent (way-of-working level)
The session closed the ecosystem's central claim: enforcement-in-effect is now a MEASURABLE property with a runbook (measure → attribute → complete → re-measure), proven end-to-end on ai-council (1/6 → FULL-COVERAGE, ZERO consumer-side changes — every gap was instrument-side). The next session's way-of-working goal is two-part:
(A) CONSOLIDATION WAVE from the operator's audit list: universalize epic-naming across repos (hub ADR-66 story-map vs ai-council "Epic A/B/C" — one convention or none); child-repo Mermaid migration (#262); References sections in CLAUDE/CONTRIBUTING → generability phase 2; ENVIRONMENT.md retire-or-own (stale ~06-03); audit proliferation → an audit-index/retention rule; transfer Epic-5 test tiering to consumers (ai-council check.ps1 got nothing — tiering is methodology, ship it via the deploy pipeline).
(B) DESIGN THE INTAKE PROCESS the operator sketched: functional architect (gathers requirements, writes intake) → technical architect (owns backlog + ADRs, cuts §14 epic handoffs) → epic browser-chats (one epic each, to completion). Lands in PLAYBOOK as methodology; ai-council wired for genuinely contested forks. This is the operator's explicit ask and UNDESIGNED.
Only after A+B: P6 fleet roll — its WAIT condition (sandbox as acceptance instrument) expired this session; its own gates #225/#249/#250 stand. Phase-2 rot-report equally UNLOCKED (defer-until-after-sandbox expired) — it is the designed answer to the operator's dead-code/redundancy concern; build it rather than hand-sweeping.

## Q2 — Tensions weighed (where landed, why)
- Measure-first vs assume-gaps (Wave 3): measure-first; vindicated — the assumed "mesh completion 1/6→6/6" was a phantom; consumer was healthy, instrument was blind.
- Authorization channel (G3): prompt self-legitimization vs owned-config; CONFIG won — a deployed floor CORRECTLY refuses prompt-asserted authority (witnessed: the child refused the arc as injection citing ai-council's own floor). User-config is the principal's channel; ex-ante standing consent satisfies "ask before destructive" without weakening the floor.
- Armed vs fired (#267): armed-as-enforcing REJECTED as doctrine; file-scoped hooks correctly skipping out-of-scope diffs is correct behavior, not silence. #267 = refinement (in-scope arc edit + scope-conditional engages:), not a closure gate.
- Epic ceremony vs serial: worktree-per-EPIC (not per-story), 2–3-lane cap, root-only merges, file-boundaries adjudicated at spawn — held through two waves incl. self-application (Epic 2 refused BACKLOG-structure edits citing the ADR it was integrating).
- Plan-mode vs execution (operator finding, CONCEDED): plan-first was used at genuine forks (Slice B plan — surfaced two forks; consumer seam) but Waves 2–3 defaulted to EXECUTION and §14a carries no MODE field. Real drift from PLAYBOOK. CORRECTIVE (do early, small): §14a template gains a mandatory Mode row; L-sized epic stories default plan-first; every architect prompt re-declares MODE.
- Autonomy boundary (overnight): execute pre-authorized contracts YES / design decisions NO — held; Block A DEGRADED honestly on a real GATE-0 confound rather than improvising past it; zero safety-envelope violations unattended.

## Q3 — Considered + rejected (do not relitigate)
Hand-copied mesh transfer (deploy pipeline only) · armed-as-enforcing · splitting the 90s E2E test (budget "~2min" met per #256's own framing) · LLM-gating semantic properties · sibling-dir worktrees · AI Council for CLAUDE.md quality (architect review + generability epic was right) · prompt-prose authorization for sandbox children · Task-Scheduler auto-resume harness (FAILED in practice: never fired the resume; clean-tree gate + untested wake path; manual git-boot re-paste is the reliable resume — treat re-automation as a fresh design, not a retry).

## Q4 — Open questions (unresolved / deferred)
- Intake process shape (Q1-B) — undesigned; needs PLAYBOOK section + intake template; how the audit corpus feeds it (operator flags audit proliferation; consider audit-index + retention).
- Epic-naming universalization (fleet-wide convention pick).
- Test-tiering transfer to consumers (hub-only today).
- ENVIRONMENT.md purpose · child Mermaid #262 · References generability · #267 · #254/#255 · #261 (generator slug) · #263–#266 · content-echo doctrine follow-through.
- Vault V1–V5/OM1–4 sign-off: corp-monorepo audit merged (32b4e20) — OPERATOR ratification in a corp-OS session; pointer only, do NOT pull into hub scope.
- Plan-mode corrective (Q2) — first small move.

## Q5 — Decomposition rationale (do not redo)
Dependency-gated waves: instrument before consumers (sandbox = the acceptance instrument), measure before complete (killed a phantom workstream), §14 rails before the 3-lane wave that ran on them, merge order 5→3→4 (ship speedup first; Epic-4's stale loci fixed against post-Epic-3 text). Sealed: C4 closure + fixtures · G3 config-channel trust seam · ADR-51 amendment + check-#7 retirement · ADR-97 · Epic-5 tiering rulings · the operator-approved ESSENTIALS deletion list · priority-#1 closure declaration (8e1dd57).

## Q6 — Off-repo context + the honest ledgers
EVIDENCE SPINE: main a523fca → fb11266 (~25 --no-ff merges, all pushed); suite 1216 → 1323 tests; closed #251/#252/#253a–d/#256–#260; filed #254/#255/#261–#267; ADR-97 new, ADR-51 amended, HANDOFF_PROCESS 5.3→5.4→5.5; ESSENTIALS 448→174 lines; /ship docs-only 9m42s→~34s, code ~2min; ai-council 1/6→FULL-COVERAGE with IDENTICAL consumer HEAD before/after.
INCIDENTS THE INSTRUMENT CAUGHT (methodology wins, on record): ai-council's relic core.hooksPath had EVERY git hook silently bypassed since the repo move (found+repaired mid-mission); the ruff tombstone prune-proof was false-green ("already absent" while ruff ran); the content-echo channel class (repo files quoting signatures leak into tool_result echoes); a deployed floor refusing prompt-asserted authority; the child declining git commit --no-verify at a failing gate under a narrowed allowlist.
ARCHITECT DEFECT LEDGER (the outgoing session's own error rate — trust the mechanism, not the architect): four contract-authoring defects (item-1 RF-1 mislabel; nonexistent docs/adr/ path; S2 bump-vs-boundary contradiction; E4-1 missing tests path) — ALL caught downstream by lane escalation or the fidelity check; plan-mode drift (conceded above); the overnight relaunch harness failure; one mid-session thread-sprawl episode (fixed by hermetization + a STOP rule: nothing new opens until the current wave closes — keep the rule).
OPERATIONAL: API credits funded (negative balance found 07-05; sandbox children bill API credits, NOT the Max subscription — by design of the isolation seam). CC update pending 2.1.177→2.1.200 (native; all claude.exe must exit first; one 14h --dangerously-skip-permissions terminal from the overnight window flagged for conscious close). Overnight-harness scheduled task unregister pending (needs elevation). No LLM-budget ceiling.
