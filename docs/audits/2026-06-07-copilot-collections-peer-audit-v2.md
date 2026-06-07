<!-- scope: meta -->
# Peer-methodology audit v2 — TSH `copilot-collections` vs `.dev-knowledge` (ADR-80 stack)

> **Anchored on the 2026-05-31 record** (`docs/audits/2026-05-31-methodology-canonical-audit.md`) — this is a two-sided DIFF, not a fresh audit. The 05-31 self-image is the diff anchor only; the rubric is **current ADR-80-era doctrine** (ADR-74/76/78/79/80).
> **Source:** `github.com/TheSoftwareHouse/copilot-collections` @ shallow-clone 2026-06-07.
> **Source LICENSE:** **MIT, © 2026 The Software House.** Any future *verbatim* adaptation of their markdown into this repo must retain the MIT notice + copyright attribution. This audit quotes for analysis (fair use); nothing is copied verbatim.
> **Date:** 2026-06-07 · **Type:** analysis + single audit-record commit · **Read-through:** all TSH content + the anchor's long sections were ingested via `artifact-reader` (context-budget discipline).

---

## Translation layer (carriers mapped before judging content)

Their toolchain is GitHub Copilot / VS Code; ours is Claude Code. Every finding is read through this map; Copilot-mechanic-bound patterns are **DIVERGENT-BY-DESIGN**, not gaps.

| TSH carrier (Copilot/VS Code) | Our carrier (Claude Code) |
|---|---|
| repo `copilot-instructions.md` + scoped `*.instructions.md` (`applyTo`) | `CLAUDE.md` (auto-read) + child-methodology-floor (ADR-78) |
| `.prompt.md` files (`/tsh-*`) | `.claude/commands/` + `templates/prompt-template.md` |
| `.agent.md` chat-mode agents | `.claude/agents/` + built-in workflow subagent types |
| `SKILL.md` skills (`.github/skills/`) | `~/.claude/skills/` + repo `.claude/` skills |
| review prompts / plan-reviewer / ui-reviewer | Codex second-reader + per-repo agentic-review profiles (#82) |
| CHANGELOG + per-asset version watermark | git history + JOURNAL `Changes:` + ADR/section-history + `last_reviewed` |
| collections versioning / clone-once distribution | hub + `tier1-lifecycle` plugin + pre-commit source-repo (ADR-71) + cloud Routine (ADR-72) |

---

## 1. DIFF LEDGER — OUR SIDE (the five-week scorecard) **[HEADLINE]**

Status TODAY of every anchor §3 finding (C1–C12) and §4.1 plan item (1–12), measured against the external 05-31 yardstick.

### §3 findings

| Finding (severity) | Status today | Evidence |
|---|---|---|
| **C1** 🔴 PLAYBOOK §10 forbidden archive action | **IMPLEMENTED-SINCE** | `PLAYBOOK.md` §10 now "done items **leave**; **no archive file**"; CLAUDE §5 rule #8 forbids recreating `BACKLOG_ARCHIVE.md`. Closed by **ADR-65**. |
| **C2** 🟡 BACKLOG status-vocab drift | **IMPLEMENTED-SINCE** | **ADR-66** story-map schema; `scripts/validate_backlog.py` wired as `validate-backlog` pre-commit hook (hard-fails `status:done`/`[x]`). |
| **C3** 🟡 documented-vs-actual drift cluster | **IMPLEMENTED-SINCE** (mechanized + ongoing) | `audit.py` 13 checks incl. `canonical_freshness`/`canonical_structure`/`handoff_version_stamp`; `conformance-hub` workflow + nightly Routine + GH Action digests. Residual deterministic prose-vs-state checker = **#89/#90**. |
| **C4** 🟡 no canonical-file cadence | **IMPLEMENTED-SINCE** | `audit.py check_canonical_freshness` (FAIL if `last_reviewed` predates git-edit; WARN >30d) via `audit-health` gate. |
| **C5** 🟡 evolution machinery vacuous | **OBSOLETED-BY** | Machinery **retired** Phase-C3 (2026-06-05); `/evolve` `/boot` archived; BACKLOG **#12 withdrawn**. The loop was removed, not backfilled. |
| **C6** 🟡 ruff documented-not-enforced | **IMPLEMENTED-SINCE** | `ruff` gate in `.pre-commit-config.yaml` (pinned ≥0.15.5, `language: system`). **#13 closed.** |
| **C7** 🟡 hooks analysed-not-built | **IMPLEMENTED-SINCE** (partial residual) | 8 pre-commit hooks + SessionStart hooks + PreToolUse immutability guard + Tier-1 Stop→`propose_closures.py` (plugin, ADR-70). Residual = **#8** (session-end clean-tree + lessons-retrieval), **#98** (PROPOSALS persistence). |
| **C8** 🟢 frontmatter inconsistency | **IMPLEMENTED-SINCE** | CLAUDE/ARCHITECTURE/CONTRIBUTING/VISION all carry `last_reviewed`+`status`+`owner`. Cosmetic residual: VISION `owner: rob` casing (**#35**). |
| **C9** 🟢 ARCHITECTURE split candidate | **STILL-OPEN** (trigger not met) | **544 lines** (grew, not split); auto-TOC + `toc-freshness` hook present (ADR-71). Split deliberately deferred = **#41**. |
| **C10** 🟢 no skill/command naming convention | **STILL-OPEN** | PLAYBOOK §7 has file-path conventions but no name-FORM rule. Tracked = **#67**. |
| **C11** 🟢 no skill-authoring template | **STILL-OPEN (untracked)** | `templates/` has ADR/ARCHITECTURE/CLAUDE/handoff/prompt/workspace scaffolds — **no SKILL scaffold**. No discrete backlog id (only tangential **#9**). |
| **C12** 🟢 orchestrator/worker not a how-to | **PARTIAL** | Orchestration content exists (PLAYBOOK §7d Subagents, §12, Dynamic-Workflow tier) + live `conformance-hub.js` worker-fanout exemplar. Consolidated §7 how-to still owed = **#67**. |

### §4.1 plan items

| Item | Status | Evidence |
|---|---|---|
| 1 BACKLOG arch decision (Council) | **IMPLEMENTED-SINCE** | ADR-64/65/66; Council transcript `council-out-20260601_103339-…backlog-architecture…`. |
| 2 reconcile PLAYBOOK §10 | **IMPLEMENTED-SINCE** | = C1. |
| 3 BACKLOG migration | **IMPLEMENTED-SINCE** | `2026-06-01-backlog-migration-inventory.md`; merges `db352ee` + `31938a4`; BACKLOG now a story-map. |
| 4 sacred-files cadence | **IMPLEMENTED-SINCE** | = C4. |
| 5 doc-truth sweep + ruff claim | **IMPLEMENTED-SINCE** | = C3/C6. |
| 6 ruff enforcement | **IMPLEMENTED-SINCE** | = C6. |
| 7 evolution logs | **OBSOLETED-BY** | = C5 (#12 withdrawn). |
| 8 SessionStop automation | **IMPLEMENTED-SINCE** (partial) | Tier-1 Stop hook via plugin (ADR-70). Residual = #8/#98. |
| 9 PLAYBOOK §7 polish | **STILL-OPEN** | = C10+C12 (#67). |
| 10 skill template/scaffold | **STILL-OPEN** | = C11 (untracked). |
| 11 ARCHITECTURE split | **STILL-OPEN** | = C9 (#41). |
| 12 frontmatter consistency | **IMPLEMENTED-SINCE** | = C8 (#35 cosmetic). |

### Scorecard
**12 findings → 7 IMPLEMENTED-SINCE (C1,C2,C3,C4,C6,C7,C8) · 1 OBSOLETED (C5) · 1 PARTIAL (C12) · 3 STILL-OPEN (C9,C10,C11).** Every **Critical (1) and Important (6)** finding is closed or obsoleted. **All residual items are Nice-to-have**, and all but one are tracked (**#41**, **#67**); the lone untracked residual is **C11 — the skill-authoring scaffold**. Five weeks moved the entire Critical/Important tier to done.

---

## 2. DIFF LEDGER — THEIR SIDE (post-05-31 delta + anchor Partial/Absent refresh)

### Their post-05-31 delta = ONE changelog entry (2026-06-01)
A Business-Analyst orchestration rework. **Pattern (Jira plumbing stripped):**
- **`/tsh-explore-materials` (new)** — an *Explore Mode* for ambiguous inputs: produces a `workshop-context-summary.md` with a **readiness verdict** *before* committing to extraction; creates no backlog items until the operator says go.
- **`tsh-business-analyst` reworked into an orchestrator** delegating to 5 internal workers (transcript-clean, context-synthesis, extraction, quality-review, formatting). Workers run **isolated** ("no conversation history, no knowledge of previous worker outputs"), return **in-memory only**; the orchestrator owns all file-writes + mutations + every human gate.
- **`/tsh-analyze-materials` gates** — Gate 0 (intent-brief approval) → Gate 1 (extraction) → auto quality-review → Gate 1.5 (accept/reject each suggestion) → Gate 2 (push approval) → **post-push read-back verification** → project-baseline refresh.
- (The 2026-05-17 entry — Claude→GPT-5.4 model swap — pre-dates the anchor; DIVERGENT-BY-DESIGN, not delta.)

### Anchor §2 matrix — refresh verdicts (Partial/Absent rows only; per the do-not-re-derive rule)

| Anchor row (05-31 verdict) | Refresh today |
|---|---|
| Orchestrator → isolated workers (**Partial**) | **We advanced**: ADR-70 Tier-3 Workflows + the live `conformance-hub.js` (isolated verifiers → adversarial skeptic → digest). Their side is now a *mature, documented* pattern across 3 orchestrators; our consolidated how-to still owed (#67/C12). |
| Frontmatter for progressive load (**Partial**) | Their `tsh-creating-skills` formalizes a 3-tier budget (discovery ~100 tok / activation <5000 / resources) + 500-line body cap. Ours carry name+description but no explicit token-budget discipline. Low-leverage enrichment. |
| Severity-tiered + scannable reporting (**Partial**) | **We advanced**: `conformance-hub` findings schema carries severity + required `evidence_command` + skeptic gate. Their `tsh-ui-verifying` severity table is clean but we now match the intent. |
| Gerund naming (**Absent**) | Unchanged — their *skills* are gerunds (`{verb-ing}-{object}`), *agents* are role-nouns (mixed). We have not adopted; relates to C10/#67. |
| Skill template + examples (**Absent**) | **Still absent on our side** — this is C11 and the one live TRANSLATE-ADOPT (below). Their `tsh-creating-skills` ships `skill.template.md` + `examples/` + `references/`. |
| Namespace prefix `tsh-` (**Absent — §4.3 against**) | Unchanged; still solves a multi-team collision we don't have. Stays recommended-against. |
| `applyTo` glob scoping (**Absent — §4.3 against**) | Unchanged; still only 1 `applyTo` file in their repo; no Claude Code equivalent. Stays against. |
| XML structure tags (**Absent — §4.3 against**) | Unchanged; pervasive in their agents + an explicit "XML-for-bounded / markdown-for-sequences" rule in `tsh-creating-skills`. Markdown headers still suffice at our scale. Stays against. |

---

## 3.5 USAGE-MODEL RECONSTRUCTION — how a TSH engineer drives a feature, and how it binds back

**The flow.** Clone the repo *once* to a fixed path; point three VS Code User-Settings keys at its `.github/{prompts,agents,skills}` — nothing is copied into the target project ("plug-and-play, configure once"). From then on, any workspace can fire `/tsh-*`. For a feature: `/tsh-implement <JIRA_ID>` routes to the **Engineering-Manager orchestrator**, which runs **research** (Context-Engineer → `*.research.md`) → **plan** (Architect → `*.plan.md` with a *Technical Context* section) → **plan-review** (Plan-Reviewer → binary APPROVED/REVISIONS, ≤3 iterations) → **implement** (Software-Engineer, after a `vscode/askQuestions` human gate) → **UI-verify** (Figma-vs-Playwright, ≤5 iterations) → **code-review** (`/tsh-review`). Each phase boundary is a human confirmation gate.

**Their answer to the reference-back problem (the core question).** Three layers, and it is *architectural*, not a single file:
1. **`tsh-technical-context-discovering`** — an **agent-mandatory** skill: every implementation agent MUST read the project's `copilot-instructions.md` + scoped `*.instructions.md` *before writing code*, and "never introduce new patterns unless specified in the plan." This re-anchors **every action**, not just session-start.
2. **`*.plan.md` Technical Context section** — discovered conventions are persisted into the plan; downstream agents read it instead of re-discovering (and skip re-discovery if present). Session-scoped binding artifact.
3. **Delegation structure removes the choice** — the EM hard-codes which subagent-prompt each phase uses; the engineer fires one prompt and cannot skip research/plan/review. "Forgetting to consult the methodology" is engineered out by giving the human no skip path.
Cross-session continuity: BA track keeps a durable `task-baseline.md`; dev track relies on `specifications/<task>/{research,plan}.md` persisting on disk.

**Map onto OUR lifecycle** (handoff → formal prompt → STOP-valve → steps → verify → Codex → /ship → funnel) and **ADR-78 floor+pointer:**

| TSH binding layer | Our equivalent | Stronger side |
|---|---|---|
| Always-on project instructions | `CLAUDE.md` auto-read + ADR-78 child floor | Even |
| Agent-mandatory context-discovery *before each action* | Session-start contract (CLAUDE §6 read ESSENTIALS/PLAYBOOK) | **THEIRS** — re-anchors per-action; ours reads once at session-start, so mid-session drift is possible |
| `*.plan.md` Technical Context persistence | Handoff bundle + UNDERSTAND phase + JOURNAL | Even |
| "Remove the choice" orchestration | Operator-authored formal prompt + STOP-valve | Even (locus differs: their EM agent vs our prompt+operator) |
| — (none) | **Mechanical commit-time enforcement** (pre-commit gates, audit-health, validate-backlog, immutability guard) | **OURS** — their binding is *all* instruction-level; ours has a hook backstop that blocks the commit |
| — (none) | **`git closes [#id]` capture backbone + JOURNAL/LESSONS append-only ledger** | **OURS** — durable cross-session institutional memory the dev track lacks |

**Where their binding is stronger (the lesson for #121 + the repo-onboarding runbook):** TSH re-asserts the floor *mid-session, per implementation action*, via a mandatory skill — our floor is asserted at session-start and then trusted. Our hook layer catches violations *at commit*, which covers much of the same drift, but the gap between "floor read at start" and "floor re-checked before each change" is real. **#121 (child methodology floor) should consider a "re-read the floor before structural work" mechanic**, not only a session-start pointer. **Where ours is stronger:** mechanical enforcement + a decision/closure ledger they have no analog for.

---

## 3.6 ROSTER COMPARISON + curated shortlist (≤7; doctrine guard: leverage, not headcount)

### Roles (not filenames): theirs vs ours

| Role class | TSH | `.dev-knowledge` |
|---|---|---|
| Orchestrators | EM, BA, copilot-orchestrator (hub-and-spoke, isolated workers, human gates) | `conformance-hub.js` workflow; Dynamic-Workflow tier (ADR-70) — autonomous, adversarial-vote, no human mid-gate |
| Implementation agents | software-engineer, devops, e2e, frontend/backend/k8s/terraform… | — (implementation lives in child code repos, not this governance hub) |
| Review/quality | plan-reviewer, code-reviewer, ui-reviewer (binary verdicts, persisted artifacts) | Codex second-reader; conformance-hub skeptic; per-repo review profiles (#82) |
| Meta-authoring | creating-skills/agents/prompts/instructions + copilot-artifact-creator/reviewer/engineer | `templates/` (ADR/CLAUDE/ARCHITECTURE/prompt/handoff) — **no skill scaffold** |
| Analysis/context | context-engineer, codebase-analysing, technical-context-discovering | artifact-reader agent; Explore/general-purpose subagents; CLAUDE §6 protocol |
| Lifecycle commands | /tsh-implement, /tsh-review, /tsh-create-custom-* | /handoff, /save, /ship, /review-closures, /session-summary, /codex-review, /changelog-review |

### Curated shortlist (7 candidates; survival decided in Step 5)

| # | Role to translate | Their asset | Our target organ class | Solo trigger freq |
|---|---|---|---|---|
| S1 | **Skill-authoring scaffold** | `tsh-creating-skills` (template+examples+references) | `templates/SKILL-scaffold.md` + short authoring note | LOW-MED (per new skill) |
| S2 | **Explore-mode readiness pass** | `tsh-explore-materials` | enrichment to `prompt-template.md` UNDERSTAND/STOP valve (#111) | MED (ambiguous handoff/prompt) |
| S3 | Mid-session floor re-anchor | `tsh-technical-context-discovering` | ADR-78 floor mechanic input → **#121** | HIGH (every structural session) |
| S4 | Adversarial plan-gate | `tsh-plan-reviewer` (binary verdict, ≤3 iter, persisted) | pre-impl review step | MED (speculative) |
| S5 | Severity-tiered report template | `tsh-ui-verifying` table | verify/conformance findings schema | HIGH |
| S6 | Agent/prompt authoring guides | `tsh-creating-agents`/`-prompts` | PLAYBOOK §7 note → **#67** | LOW |
| S7 | Runtime LLM-prompt skill | `tsh-engineering-prompts` | reference doc | LOW |

---

## 3. NET-NEW FINDINGS — buckets (post-translation)

### TRANSLATE-ADOPT (concrete target; dup-checked vs anchor matrix + BACKLOG #102–#128)
- **[T1] Skill-authoring scaffold** (= S1, anchor C11). `templates/` has every other canonical scaffold but no SKILL template. **Not on the backlog** (only tangential #9) — genuinely new. Target: `templates/SKILL-scaffold.md` (+ optional `examples/`), mirroring how `templates/prompt-template.md` already anchors prompt authoring. *Capture is a separate post-review step (not done here).*
- **[T2] Explore-mode readiness pass** (= S2). Their pattern: for ambiguous inputs, emit a *readiness verdict artifact* and create nothing until the operator approves. This is a richer cousin of our STOP-after-UNDERSTAND valve — the increment is "produce a named readiness artifact + go/no-go recommendation." Folds into prompt-format enrichment (**#111**) rather than a new organ.

### ALREADY-COVERED (name our organ; enrichment only if theirs is materially stronger)
- Spec-driven creation, progressive disclosure, gate-based review, repo constitution — all anchor-P, still covered.
- **Binding mechanism** → CLAUDE.md auto-load + ADR-78 floor + **mechanical hook enforcement** (which they lack). Enrichment: their per-action re-anchor (→ #121, see 3.5).
- **Severity-tiered reporting** (= S5) → `conformance-hub` findings schema already carries severity + `evidence_command` + skeptic. Their table is clean; marginal.
- **Orchestrator/isolated-workers** → ADR-70 Tier-3 + conformance-hub.js exemplar; how-to consolidation owed (#67/C12).
- **Agent/prompt authoring guidance** (= S6) → already tracked by **#67**.

### DIVERGENT-BY-DESIGN (does not transfer to a solo multi-repo Claude-Code operator)
- **Multi-model per-agent pinning** (GPT-5.4 / Gemini 3.1 / Claude Sonnet) + the 05-17 cost-driven model swap — we are Claude-Code-bound, single-model.
- **Jira/Atlassian/Figma MCP-heavy BA workshop→backlog flow** — team/enterprise discovery ceremony; a solo operator runs no client workshops.
- **21-agent / 32-skill library** — a team library serving many engineers across many client repos. Our small-roster doctrine binds (#97 rider; field datapoint: 17-agent zoo abandoned). See meta-comparison for why their many-worker design is safe *for them* and unsafe *for us*.
- **`handoffs:` UI phase-buttons + `vscode/askQuestions` gates** — Copilot/VS Code mechanics.
- **Namespace prefix `tsh-`, `applyTo` glob scoping, XML structure tags** — §4.3 binding; no material change (see compliance statement).

### VERIFY (exact command)
- Claim: our `conformance-hub.js` already realizes their orchestrator+reviewer pattern (isolated workers → adversarial skeptic → synthesis). **Verify:** `Read C:/Users/1028120/Documents/Dev/.dev-knowledge/.claude/workflows/conformance-hub.js` and confirm the fan-out→skeptic→digest stages. (High confidence from the skill descriptor; not line-verified in this pass.)

### NOISE (count only)
- ~20 domain-implementation skills (frontend, backend, forms, a11y, hooks, sql, e2e, k8s, terraform, observability, ci-cd, secrets, multi-cloud, cloud-cost, frontend-optimization, frontend-review) — irrelevant to a methodology-governance hub whose implementation lives in child code repos. **Count: ~20. No action.**

---

## 4. META-COMPARISON — governing an AI methodology (NET-NEW; the anchor skipped this)

| Dimension | TSH (production software house) | `.dev-knowledge` (solo, multi-repo) |
|---|---|---|
| Versioning | Keep-a-Changelog `CHANGELOG.md` (dated) + per-asset watermark `<!-- …:prompt:tsh-implement:v1 -->` | git history + JOURNAL `Changes:` + ADR + per-file section-history + `last_reviewed` |
| Distribution | clone-once + VS Code User-Settings paths; Docusaurus website (Vercel); MIT public | hub + `tier1-lifecycle` plugin + pre-commit source-repo (ADR-71) + cloud Routine (ADR-72); private |
| Change review | meta-skills + copilot-artifact-**reviewer** agent (dogfoods own methodology) | AI Council debate → ADR; Codex second-reader; conformance-hub; Discovery→Review funnel |
| Decision provenance | CHANGELOG says *what* changed | **ADRs (immutable, numbered, superseded-not-edited) + Council transcripts** say *what + why* |
| Enforcement | instruction-level (agents are *told* to comply) | **mechanical** — pre-commit gates / audit-health / validate-backlog / immutability guard block the commit |
| Closure/continuity | `specifications/` files + BA `task-baseline.md` | **`git closes [#id]` capture backbone** + append-only JOURNAL/LESSONS |
| Adoption path | installation + getting-started docs, plug-and-play | CLAUDE §6 session-start protocol; #121 child floor; repo-onboarding runbook (pending) |

**What they do that would strengthen us:** (a) a public **getting-started/onboarding structure** — low value solo, but a clean shape for the pending repo-onboarding runbook; (b) **dogfooding meta-authoring** — exactly the C11/T1 skill-scaffold gap. **What we have that they lack:** mechanical enforcement, a why-ledger (ADRs + Council), an automated closure loop, append-only institutional memory, and repo-self-auditing.

**The crux contrast (rider) — their gated-worker design vs our blind-vote isolation + small-roster doctrine.** TSH runs orchestrator → *many* isolated specialized workers with a **human gate at every phase boundary** (Gate 0/1/1.5/2; plan-review APPROVE; UI-verify PASS). The human gates are what make a *large* roster safe: each added agent adds a human-reviewed stage, not unreviewed risk — and a team has the reviewer bandwidth to staff those gates. **We run the opposite trade:** workflow subagents fan out and **adversarially verify each other** (independent skeptics, majority-refute kills a finding), synthesized by a digest, with the operator reviewing only the *final* output — because a solo operator cannot be the human gate at every phase without becoming the bottleneck. So we substitute machine-checks-machine for human-gates, and we keep the roster **small** to bound the verification surface. Both are coherent — they answer *different* constraints (team + many clients vs solo + multi-repo). **The failure mode to avoid:** importing their many-worker roster *without* their gates (and without a team to staff them) reproduces the abandoned 17-agent zoo. Headcount parity is an anti-goal; leverage is the only admission test.

---

## 5. SELF-SKEPTIC PASS — kills

Killed 3 of the 7 shortlist candidates + 0 spurious TRANSLATE-ADOPT:
- **KILL S4 (plan-reviewer adoption)** — speculative trigger for a solo operator: we don't author a per-task `plan.md`, and the browser-architect already critiques approach pre-execution. Adds team-ceremony (a dedicated review agent + persisted artifact) without a matching solo workflow. Trigger frequency speculative → killed per Step-5 rule.
- **KILL S5 (severity-tiered report template adoption)** — ALREADY-COVERED: `conformance-hub` findings schema carries severity + `evidence_command` + skeptic. Adopting their table would duplicate an existing organ.
- **KILL S7 (runtime LLM-prompt skill)** — out of scope for a methodology-governance hub; runtime prompt-engineering belongs to child repos (e.g. `ai-council`), not Layer 2. DIVERGENT.
- **S6 (authoring guides)** — not killed but **already tracked** by #67; not new work.
- **S3 (mid-session floor re-anchor)** — survives as a **#121 input/pattern**, not a standalone organ.

**Survivors as genuinely-new TRANSLATE-ADOPT:** **T1 skill-authoring scaffold** (strong; untracked; rider-flagged) and **T2 explore-mode readiness pass** (enrichment to #111). Net new agents recommended: **zero** — the small-roster doctrine holds; the one new organ is a *template*, not a worker.

---

## Anchor §4.3 compliance statement

This audit did **not** re-propose any §4.3 recommended-against pattern. Confirmed **no material change** since 2026-05-31 that would alter the calculus: the `tsh-` **namespace prefix** is still pervasive and still solves a multi-team collision we don't have; **`applyTo` glob scoping** still has no Claude Code mechanism (their repo carries a single `applyTo` instructions file); **XML structure tags** are still Copilot-parse-reliability hygiene that markdown headers cover at our scale. One nuance noted (their `tsh-creating-skills` "XML-for-bounded-content / markdown-for-sequences" rule) — recorded for completeness, but it does **not** change our calculus and is not proposed. §4.3 honored.

---

## Provenance
- Anchor: `docs/audits/2026-05-31-methodology-canonical-audit.md` (216 lines; 13 matrix rows 5P/3Partial/5A; 12 findings; 12 plan items; §4.3 binding registry).
- TSH source: `github.com/TheSoftwareHouse/copilot-collections`, shallow clone 2026-06-07, MIT © 2026 The Software House. Inventory: `.github/` {21 agents, 32 skill-dirs, 13 prompts, 12 internal-prompts, 1 instructions} + `website/docs/` prose. Post-anchor delta: one CHANGELOG entry (2026-06-01, BA orchestrator rework). Temp clone deleted post-audit.
- Method: 5 `artifact-reader`/evidence subagents (TSH agents, skills, prompts, usage-model; our-side current state). All TSH content + anchor long-sections read out-of-thread per context-budget discipline.
