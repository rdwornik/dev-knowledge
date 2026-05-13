# AI Council Debate: ## Question: Which architectural changes should replace ADR-42 v3.2 handoff proc

**Date:** 2026-05-13 11:14:24
**Panel:** claude-opus-4-7, deepseek-v4-pro, grok-4.3
**Synthesizer:** openai (non-participant)
**Rounds:** 2
**Duration:** 580.8s
**Panel Mode:** full (3-model panel)
**Debate Mode:** pick
**Source:** C:\Users\1028120\Downloads\council-handoff-architecture-pick.md
**Cost:** ~$0.3592 (68,374 tokens)

---

## Round 1: Initial Responses

### Claude (claude-opus-4-7)

## Position
Adopt a **C/C/C/D/A** composite: central `.dev-knowledge` reference with per-repo `@path` imports (Q1-C), a 2-file manifest+NEXT handoff (Q2-C), executor-as-custodian via Claude Code's existing tooling (Q3-C), defense-in-depth mechanical enforcement at git + PreToolUse + `/save` (Q4-D), and a parallel pilot on `.dev-knowledge` before fleet rollout (Q5-A).

## Alternatives Considered
- **Workspace Repository Pattern (Q1-A) + MCP custodian (Q3-B)**: Rejected. Restructuring 5 repos into a workspace is high-blast-radius for a solo dev, and a hand-rolled MCP server becomes a second system to babysit at 2am. The operability cost dwarfs the flexibility benefit when one human owns everything.
- **Token-compressed JSON payload (Q2-B) + big-bang migration (Q5-D)**: Rejected. JSON/YAML handoffs are unreadable when the architect hallucinates and you need to diff what changed; the 2am test fails. Big-bang cutover violates the stated "verify each step" constraint and offers no rollback.

## Decision Criteria
1. **2am legibility**: Can solo-dev, six months from now, read the handoff and recover state without tooling?
2. **Mechanical enforcement over discipline**: Every required behavior must have a deterministic gate (Lesson A is explicit).
3. **Minimize net-new infrastructure**: Each new daemon/server is a future outage. Prefer existing Claude Code primitives and git.
4. **Preserve drift detection**: HEAD-pin + SHA-256 manifest is non-negotiable and must survive any restructure.
5. **Reversibility**: Each migration step must be revertable with a single `git revert` or directory rename.

## Assumptions
- Claude Code's `@path` import syntax in CLAUDE.md is stable enough to depend on for 12+ months (if it breaks, fall back to a sync script — Q1-B — without changing other answers).
- `~/.claude/projects/` session storage and PreToolUse hooks remain supported in current form.
- The 5 repos sit on one developer machine (or are checked out together), so a sibling `.dev-knowledge` directory is reachable by relative path.
- Handoff frequency is on the order of daily, not hourly — so a 2-file manual paste is tolerable.

## Recommendation

**Now:**
- Create `.dev-knowledge/` as a sixth repo containing canonical `AGENTS.md`, `CLAUDE.md` fragments, ADR index, and handoff templates. Version it like any other repo.
- In each of the 5 existing repos, replace inline convention text in `CLAUDE.md` with `@../.dev-knowledge/agents.md` (or equivalent) imports. Keep repo-specific overrides local.
- Define the handoff as exactly two files:
  - `MANIFEST.md` — HEAD SHAs per repo, SHA-256 over the bundle, object pointers (paths + line ranges) into `.dev-knowledge` and source repos, model/tool versions.
  - `NEXT.md` — ~50 lines plain prose: *Built / Current State / Next Action / Hard Constraints*. No SBAR vocabulary, no rationale section.
- Implement enforcement triple:
  - **Git pre-commit hook** (in `.dev-knowledge`, installed via `core.hooksPath`): blocks commit if JOURNAL/CHANGELOG not touched in session window.
  - **Claude Code PreToolUse hook**: exit-code-2 on writes that bypass conventions (e.g., editing source without a JOURNAL entry staged).
  - **`/save` slash command**: runs a deterministic validator script; refuses to emit handoff if MANIFEST checksums fail or required files are stale.
- Pilot all of the above on `.dev-knowledge` itself for 2 weeks. It is its own first customer.

**Don't do now:**
- Don't build a local MCP server for conventions. Defer until you have a second tool (beyond Claude Code) that needs them.
- Don't restructure into a workspace monorepo.
- Don't adopt Mem0/Zep/Letta. The executor + git is sufficient custody.
- Don't migrate the other 4 repos until the pilot survives 2 weeks with zero fabrication incidents and ≥95% convention adherence.

**Defer:**
- MCP server (Q3-B) as a *future* read path if/when a non-Claude-Code tool enters the ecosystem.
- External memory service as an *optional* archival mirror, not primary.
- Retiring `MANIFEST.md`/`NEXT.md` plaintext in favor of structured payloads — only after 3 months of stable use proves the schema.

## Rationale
- **`.dev-knowledge` + `@path` imports** gives one canonical source (the primary goal) without the structural rework of a workspace pattern. If imports break, a 20-line sync script (Q1-B) is a drop-in fallback — the migration cost is bounded.
- **2-file handoff** is the smallest unit that keeps machine-checkable metadata (`MANIFEST.md`) separate from human-readable intent (`NEXT.md`). The 11→2 reduction roughly matches the empirical "object-reference sparse context = 98% at ~800 tokens" result while staying skimmable at 2am; JSON would hit similar token counts but fail the legibility test.
- **Executor-as-custodian** uses infrastructure that already exists and is maintained by Anthropic. Building an MCP server adds ~200 LOC of custodial code that *you* will debug during incidents. Solo-dev attention budget is the binding constraint.
- **Defense-in-depth enforcement** is justified here specifically because each layer catches a different failure mode: git hook catches "forgot to update JOURNAL," PreToolUse catches "LLM tried to skip," `/save` catches "session ending in bad state." A single layer historically yielded 85%; the empirical 96-99% target requires stacking. The cost of three hooks for one developer is one afternoon of setup.
- **Pilot on `.dev-knowledge` first** means the meta-repo eats its own dogfood. If the conventions can't govern their own repo cleanly, they won't govern the other 4. This is the cheapest possible validation.

## Trade-offs
- **Manual paste per handoff** remains (Q3-C implies operator copies manifest into new browser session). ~30 seconds/handoff vs. zero with MCP — accepted to avoid MCP maintenance.
- **`@path` import coupling** to Claude Code's specific behavior. If Anthropic changes semantics, ~5 repos need a coordinated patch.
- **No vendor memory service** means losing potential cross-device continuity. Acceptable for single-machine solo dev.
- **Three enforcement layers** mean three places to update when conventions evolve. Mitigated by centralizing validator logic in `.dev-knowledge/scripts/` and having all three hooks call it.

## Risks
- **`@path` import semantics change or silently fail** (likelihood: medium; impact: high — invisible convention drift). Mitigation: weekly CI job in `.dev-knowledge` that diffs resolved imports against canonical text; alert on mismatch.
- **PreToolUse hook becomes annoying and gets disabled** (likelihood: medium; impact: high — returns to 40% adherence). Mitigation: log every block with reason; review weekly; tune thresholds rather than disable.
- **Pilot succeeds but multi-repo rollout exposes path-resolution bugs** (likelihood: medium; impact: medium). Mitigation: migrate one repo at a time, 1-week soak each.
- **HEAD-pin + checksum logic gets bypassed during the migration window** (likelihood: low; impact: critical — fabrication slips through). Mitigation: port the existing checksum code *first*, before removing the 11-file bundle; both run in parallel for the pilot's 2 weeks.
- **Solo dev gets sick / context-switches for a month**: the 2-file format and centralized `.dev-knowledge` are specifically chosen so re-onboarding requires reading ~2 files, not 11.

## Signals to Revisit
- A second LLM tool (Cursor, Aider, etc.) enters the workflow → reconsider MCP server (Q3-B) as primary.
- `@path` import behavior changes in a Claude Code release → fall back to Q1-B sync script.
- Convention adherence drops below 90% in any 2-week window post-migration → add a fourth enforcement layer or tighten existing ones.
- Handoff frequency exceeds ~10/day → reconsider operator-paste model in favor of automated custody.
- A real fabrication incident slips past HEAD-pin + SHA-256 → escalate manifest scope (add per-file checksums, not just bundle-level).
- Team grows beyond solo → re-evaluate everything; this design is explicitly optimized against the solo-dev constraint.

*Latency: 42.73s | Tokens: 6071*

### Deepseek (deepseek-v4-pro)

## Position
Replace ADR-42 with a manifest+pointer handoff (2-file MANIFEST+NEXT), executor-as-custodian via Claude Code, PreToolUse hook enforcement in the executor, conventions propagated from a single canonical source via git sync, and pilot on `.dev-knowledge` first. This cuts handoff bloat to <800 tokens, hard-enforces >95% convention adherence, and eliminates operator memory dependency.

## Alternatives Considered
- **MCP-based state or convention serving (Q3-B, Q1-D)**: Rejected because the browser-chat architect has no filesystem/network access to reach a local MCP server, and standalone MCP infrastructure mandates sustained maintenance—violating the solo-dev attention budget.
- **Keep 11-file bundle but radically slimmer (Q2-D) plus git pre-commit hooks only (Q4-A)**: Rejected because eleven files still impose bloat above the 10% target even when slimmed, and commit-time hooks can be bypassed by never calling commit; the empirical failure mode of implicit approach (40% adherence) demands harness-level blocking, not peripheral hooks.

## Decision Criteria
1. **Cross-repo convention fidelity** — one authoritative source, all repos identical, no per-repo drift.
2. **Handoff token efficiency** — ≤1000 tokens empirically (target 98% adherence at ~800 tokens), bloat ratio <10%.
3. **Mechanical enforcement** — deterministic block on non-compliance that does not rely on prompt memory; failure mode from implicit 40% eliminated.
4. **Operator attention budget** — no sustained daily manual discipline, minimal cognitive load, operator can verify each step.
5. **Migration safety** — pilotable, reversible, operator-verifiable increments; no big-bang.

## Assumptions
- The browser-chat architect cannot directly call local MCP servers; all interaction is via operator-pasted text.
- Claude Code executor can reliably execute PreToolUse hooks that inspect repo state (JOURNAL timestamps, checksums) before mutating files or committing.
- A sync script for conventions can be triggered automatically (e.g., via Makefile or pre-commit) with negligible maintenance overhead.
- The `.dev-knowledge` pilot will yield at least 5 complete handoff sessions within 1-2 weeks to validate adherence and token counts.

## Recommendation
### What to do now
1. Establish a **single canonical source** for all universal conventions (AGENTS.md, CLAUDE.md, JOURNAL templates, etc.) in a dedicated directory (e.g., `ai-council/.dev-conventions`). Write a git-propagation script that copies these files into each of the 5 repos and verifies SHA-256 parity.
2. Define the **2-file handoff payload**:
   - `MANIFEST.md` – Contains SHA-256 checksums of referenced knowledge objects (specific sections in `.dev-knowledge`), HEAD-pin, and drift-detection data.
   - `NEXT.md` – Condensed prose (max 50 lines) in dense-bullet format: built state, immediate next actions, hard constraints. No rationale, no SBAR narrative.
3. Implement a **Claude Code PreToolUse hook** that intercepts any file-write or `git commit` call and blocks with exit code 2 if the session’s JOURNAL entry is absent or outdated. Include a bypass command with operator confirmation and audit log.
4. **Pilot** on the `.dev-knowledge` repo: use the new handoff format and enforcement for all its handoff sessions. Measure adherence and payload size after each.

### What not to do now
- Do **not** deploy MCP server for conventions or state; do **not** introduce external memory services as primary custodian.
- Do **not** retain the 11-file structure in any form (even slimmed). Commit fully to the 2-file format.
- Do **not** roll out to other repos before pilot validation reaches ≥98% adherence and ≤800 tokens average payload.

### What to defer until later
- Migration of `ai-council`, `corp-monorepo`, `corp-ops`, and `corp-sca-time-automation` repos. Only after pilot achieves the success criteria over 5 consecutive handoffs, migrate one repo at a time with operator sign-off.

## Rationale
- The 2-file manifest+pointer format projects ~800 tokens per handoff (based on prior empirical object-reference sparse context achieving 98% adherence), a **93% reduction** from the current 12 000-token bundle and well under the 10% bloat target.
- Executor-as-custodian eliminates reliance on operator memory: state lives in Claude Code’s auto-memory and project files; the operator pastes only a pointer-manifest between sessions. This avoids the implicit-operator-memory failure mode.
- PreToolUse hard-block directly addresses the 40% adherence problem. Prior council validation proved that moving discipline into the executor harness raises adherence to 96–99%; a hook that rejects non-compliant tool calls forces deterministic compliance.
- Git-based convention propagation gives one authoritative source without changing the repo topology, and the same PreToolUse hook can verify repo conventions match canonical checksums—mechanically preventing drift.
- Piloting on `.dev-knowledge` limits the blast radius. If the hook is too strict or the payload format causes confusion, only one repo’s workflow is disrupted while tuning proceeds.

## Trade-offs
- We give up handoff narrative and deep rationale in the payload; dense bullets require the operator to occasionally consult referenced knowledge objects for nuance. This is acceptable because the payload is a state-transfer mechanism, not a tutorial.
- PreToolUse enforcement may occasionally block legitimate rapid iterations (e.g., quick fix without a JOURNAL update). Mitigation: an explicit bypass command with audit logging, but this adds a manual backdoor—operator discipline must hold.
- Git sync adds a small operational step: after updating canonical conventions, run the sync script. This is automatable (Make target, pre-commit hook in the source-of-truth repo) and failure is caught by the enforcement hook.

## Risks
- **PreToolUse hook false positives** — frequent blocking disrupts flow. Likelihood: medium initially. Mitigation: thorough pilot tuning, allow operator to skip with an audit trail, and refine the check to only trigger after a threshold of modified files.
- **Sync script neglect** — canonical conventions are updated but sync is forgotten, causing cross-repo drift. Likelihood: medium. Mitigation: the same PreToolUse hook can verify repo AGENTS.md against a canonical checksum and block commits if mismatched; this mechanically enforces sync.
- **Browser architect misinterprets pointers** and fetches wrong objects. Likelihood: low if pointers are precise (file+line range). Mitigation: MANIFEST includes a one-line description per pointer for human verification.

## Signals to Revisit
- If pilot adherence remains below 95% after rule tuning, consider layering a `/save` validator (Q4-C) as a second defense, or combining with pre-commit hooks.
- If handoff payload exceeds 1200 tokens consistently, switch to a structured JSON format (Q2-B) with a human-readable header to squeeze further.
- If sync script maintenance exceeds 10 min/month or cross-repo drift incidents occur more than once, adopt the workspace repository pattern (Q1-A) to eliminate propagation entirely.
- If the AGENTS.md standard matures with stable `@import` support and all tools reliably resolve paths, switch to per-repo imports from a central `.dev-knowledge` reference (Q1-C) to reduce scripting.

*Latency: 237.28s | Tokens: 9042*

### Grok (grok-4.3)

## Position
Adopt workspace-root conventions (Q1-A), 3-file manifest handoff (Q2-A), executor-as-custodian with pointer paste (Q3-C), and multi-layer mechanical enforcement (Q4-D), migrating via parallel pilot on one repo (Q5-A).

## Alternatives Considered
- D MCP server for conventions + B compressed JSON payload: rejected because it adds ongoing server maintenance and reduces human skimmability without measurable adherence gain beyond the 98% already achieved by manifest+pointers at 800 tokens.
- A operator thin-paste only + C variant-by-stakes: rejected because it reintroduces manual discipline per session, violating the explicit constraint against sustained attention load.

## Decision Criteria
- Universal conventions must exist in one canonical location reachable by all five repos.
- Handoff must stay under ~1,000 tokens while preserving HEAD-pin + SHA-256 checksums.
- Updates to JOURNAL/CHANGELOG/BACKLOG/LESSONS must be mechanically blocked, not prompted.
- No new persistent infrastructure that the solo operator must maintain daily.
- Migration must permit verification of each step before full commitment.

## Assumptions
- Workspace directory restructuring is acceptable because the developer controls all five repos and no external contributors exist.
- Claude Code tooling already exposes reliable PreToolUse hooks and `~/.claude/projects/` memory that can hold the thin manifest without additional setup.
- The operator will run one pilot repo for at least ten sessions before expanding.

## Recommendation
Move all seven governance files (CLAUDE.md through ADRs) to a workspace-root directory that each repo references via git worktree or symlink. Replace the 11-file bundle with `MANIFEST.md` (pointers + SHA-256), `SUMMARY.md` (<500 lines), and `DIRECTIVES.md`. Configure Claude Code to act as custodian: at session end it writes the manifest locally; the operator pastes only the manifest path into the next browser session. Combine git pre-commit, PreToolUse exit-2, and `/save` validator to block non-compliant exits. Run the new format first on `.dev-knowledge` only until 10 consecutive handoffs show 96%+ adherence and zero missed updates, then migrate the remaining four repos one at a time.

## Rationale
- Workspace root eliminates the 85% adherence ceiling observed when conventions lived inside each repo.
- Three-file manifest with object pointers matches the empirical 800-token / 98% adherence result while keeping the SHA-256 checksum that previously caught fabrication.
- Executor custody removes the per-handoff manual paste that previously produced 40% adherence under implicit memory alone.
- Defense-in-depth enforcement (git + hook + slash command) directly addresses the mechanical requirement; any single layer alone has shown leakage in prior runs.
- Parallel pilot on one repo bounds risk to at most 10 wasted sessions before rollback.

## Trade-offs
- One-time workspace symlink or worktree setup (estimated 2-3 hours) traded for permanent elimination of sync scripts and per-repo drift.
- Slightly higher initial Claude Code configuration cost traded for zero daily operator discipline thereafter.

## Risks
- Symlink breakage across OS updates (likelihood low, impact medium): mitigate by documenting the exact `git worktree add` commands and keeping a one-line restore script in the workspace root.
- Claude Code hook version drift disabling PreToolUse (likelihood medium, impact high): pin the hook version in the repo and test after every Claude update during the pilot phase.

## Signals to Revisit
- Any session where JOURNAL/CHANGELOG updates are missed despite the three-layer block, or measured handoff token count exceeds 1,200.

*Latency: 21.45s | Tokens: 3108*

## Round 2: Critique

### Claude (claude-opus-4-7)

# Round 2 Assessment

## Proposal A (Workspace-A / 3-file / Executor / Defense-in-depth / Pilot)

**Steelman:** If the solo dev has full control of all five repos, no external contributors, and is willing to pay a one-time 2-3 hour restructure cost, then collapsing everything under a workspace root with worktrees gives the cleanest possible "one canonical location" — no sync scripts, no import-resolution semantics to babysit, no drift physically possible. The 3-file split (MANIFEST/SUMMARY/DIRECTIVES) preserves the distinction between machine-checkable data, human context, and forward intent. Defense-in-depth is the only known way to hit 96-99% adherence empirically. This is right if Claude Code's `~/.claude/projects/` storage is a reliable enough custodian to trust without a fallback.

**Assessment:** Partially agree. Q2-A (3 files) and Q1-A (workspace) are both heavier than needed. The third file (SUMMARY at <500 lines) is exactly the kind of artifact that grows into the old 11-file bloat over 6 months — there's no mechanical pressure keeping it small.

**Strongest point:** "Any single layer alone has shown leakage." Defense-in-depth at Q4 is correctly justified by failure-mode analysis, not by belt-and-suspenders reflex.

**Weakest assumption:** That `git worktree`/symlink restructure is a one-time cost. In practice, worktree setups break in subtle ways across OS updates, IDE configurations, and CI runners. The "one-line restore script" mitigation handwaves the actual on-call experience: at 2am the symlink is dangling and you don't remember whether `.dev-knowledge` is the source or the target.

**Hidden assumptions:**
1. That a `SUMMARY.md` capped at "<500 lines" will stay disciplined without a mechanical enforcer — but no hook in Q4 actually measures SUMMARY length. This is the same failure mode that produced the 11-file bloat.
2. That workspace restructuring is reversible. It isn't really — once five repos depend on relative paths into a workspace root, "rollback" means re-vendoring conventions back into each.

**Overlooked risks:**
- IDE/tool path resolution when repos are worktrees vs. independent clones (Cursor, VS Code workspace files, language servers).
- The SUMMARY.md drift risk — no checksum, no length gate, no enforcement.
- What happens to the workspace when one repo needs to be cloned standalone (e.g., on a new machine, for a one-off audit).

---

## Proposal B (`.dev-knowledge` + @path / 2-file / Executor / Defense-in-depth / Pilot)

**Steelman:** Solo-dev attention is the binding constraint, not architectural elegance. Every piece of net-new infrastructure is a future 2am outage. Use what already exists: git, Claude Code's built-in custody, `@path` imports. Keep the handoff to the smallest unit that's still human-legible at 2am (2 files, not 1 JSON blob, not 3). Have a named fallback for every dependency (`@path` breaks → sync script). Pilot the meta-repo on itself. This is right if `@path` import semantics are stable for 12+ months and if 2-file handoffs are skimmable enough for cold re-onboarding.

**Assessment:** Agree with the Position. This proposal is the only one that takes the 2am test seriously throughout — not just as a slogan but as a design constraint applied to each individual choice. The named-fallback discipline (`@path` fails → Q1-B sync script; no other answers change) is exactly the kind of bounded-blast-radius thinking long-term operability requires.

**Strongest point:** "JSON would hit similar token counts but fail the legibility test." This is the right reason to reject Q2-B and it generalizes: token efficiency is not the objective function; recoverability under degraded conditions is.

**Weakest assumption:** That Claude Code's `@path` import semantics are stable for 12+ months. Anthropic has shipped breaking changes to Claude Code's configuration surface multiple times. If `@path` silently changes resolution behavior (e.g., changes precedence between local and imported CLAUDE.md), conventions drift invisibly across all five repos at once. The weekly CI diff mitigation is good but assumes the dev notices the alert.

**Hidden assumptions:**
1. That `core.hooksPath` pointed at `.dev-knowledge` works cleanly when `.dev-knowledge` is itself one of the repos being governed — i.e., the hooks repo can run hooks against itself during the pilot. This bootstrapping path is not exercised.
2. That "centralize validator logic in `.dev-knowledge/scripts/`" composes cleanly with three different invocation contexts (git, Claude Code hook, slash command). Each has different env vars, cwd, and exit-code semantics.

**Overlooked risks:**
- The `@path` resolution depends on where Claude Code is invoked from. If the operator launches Claude Code in a subdirectory, relative `@../.dev-knowledge/...` may not resolve. Not addressed.
- No story for what happens when `.dev-knowledge` itself needs a handoff — the pilot uses the meta-repo as its first customer, but the format that governs it is the one being tested. Circular bootstrap is acknowledged ("eats its own dogfood") but not de-risked.

---

## Proposal C (Git-sync / 2-file / Executor / PreToolUse only / Pilot)

**Steelman:** The 11-file bundle even slimmed is still bloat; commit to 2 files. The 40% implicit-memory adherence problem is fundamentally a harness problem, so put enforcement at the harness layer (PreToolUse) where it can actually block before damage. Git sync is unglamorous but it's a 20-line script with zero ongoing maintenance, and the same hook that enforces conventions can verify sync. This is right if a single enforcement layer (PreToolUse) is sufficient at 96-99% adherence and if the bypass command doesn't get habitually used.

**Assessment:** Disagree with the Position, specifically with Q4-B (single-layer PreToolUse) and with the explicit operator-bypass command. The Round 1 framing was clear: empirical data shows single layers leak. Choosing Q4-B over Q4-D for "simplicity" reintroduces the failure mode this whole exercise is designed to eliminate. Worse, an audit-logged operator bypass is exactly the affordance that, under deadline pressure, becomes the default path.

**Strongest point:** "Commit-time hooks can be bypassed by never calling commit." This is correct and underappreciated — git pre-commit alone is not sufficient because the LLM doesn't have to commit. PreToolUse blocks the *write*, which is the earlier and harder gate.

**Weakest assumption:** That a single PreToolUse layer reaches 96-99%. The Round 1 evidence showed hybrid layered memory at 96-99%, not single-hook enforcement. Proposal C conflates the two. If adherence sits at, say, 88% with PreToolUse alone, the dev is back to manual discipline for the remaining 12% — which is exactly the failure mode the constraint prohibits.

**Hidden assumptions:**
1. That PreToolUse hooks can reliably inspect "session JOURNAL entry timestamps" — this requires the hook to know what "this session" means, which is non-trivial state for a stateless hook to derive.
2. That the operator-bypass with audit log will be reviewed. Audit logs that nobody reads are theater.

**Overlooked risks:**
- Bypass-command drift: once added, it becomes the path of least resistance for any false positive. No mechanism prevents this.
- PreToolUse hook behavior changes across Claude Code releases — same risk as B's `@path` assumption, but C has no named fallback.
- Sync script "neglect" is mitigated by the same PreToolUse hook verifying checksums — but this creates a circular dependency: the hook that enforces sync is itself synced by the script. If sync breaks, the hook's reference checksum is stale.

---

# Revised Recommendation

**I align with Proposal B (C/C/C/D/A composite), with two amendments.**

What moved me: Proposal B is the only one that consistently applies the 2am-legibility test as a design constraint rather than as decorative language, and the only one that pairs every dependency with a named, bounded-cost fallback (`@path` → sync script; MCP deferred; vendor memory deferred). Proposal A's workspace restructure trades a recurring small cost (sync) for a one-time large cost with a long tail of subtle path-resolution failures — that trade looks attractive on a whiteboard and ugly on-call. Proposal C's choice of single-layer enforcement plus an operator bypass directly recreates the 40% adherence failure mode the constraints explicitly forbid.

**Amendment 1 (addressing B's weakest assumption):** Do not depend on `@path` semantics as the *only* propagation mechanism even during the pilot. Run the sync-script fallback (Q1-B) in parallel from day one as a verifier, not a propagator — a CI job in `.dev-knowledge` that resolves each repo's imports and diffs them against the canonical text. This makes the `@path` failure mode loud instead of silent, which is the actual operability concern. Cost: one cron job. This is cheaper than discovering invisible drift three months in.

**Amendment 2 (addressing B's circular-bootstrap hidden assumption):** Before piloting on `.dev-knowledge`, run a one-session dry-run where the handoff format governs a throwaway sixth repo with no real content. This separates "does the format work" from "does the format work when it's governing its own home." The pilot on `.dev-knowledge` proper then validates the harder case, but you've already de-risked the format mechanics. Cost: one afternoon.

**What I did not adopt from A or C:**
- A's three-file split: the third file (SUMMARY) has no mechanical length enforcement and will bloat. Two files is the right Schelling point.
- A's workspace restructure: the operability cost (worktree fragility, IDE/CI path assumptions, irreversibility) exceeds the sync-script cost it eliminates.
- C's single-layer enforcement: contradicts the empirical evidence that single layers leak.
- C's operator-bypass command: any explicit bypass becomes the default under pressure. If a PreToolUse block is wrong often enough to need a bypass, the rule is wrong and should be fixed, not bypassed.

**The on-call test at 2am:** With B+amendments, the dev opens two files (MANIFEST.md, NEXT.md), sees HEAD SHAs and a 50-line prose status, and can reconstruct state without running any tooling. If `@path` is broken, the CI diff alert already told them which repo drifted. If the PreToolUse hook is blocking incorrectly, they can read the block reason in the log and fix the rule — not paper over it with a bypass. That is the architecture I can hand to a stranger in three years.

*Latency: 50.80s | Tokens: 13656*

### Deepseek (deepseek-v4-pro)

### Proposal A
**Steelman**
Workspace-root conventions (Q1-A) give a single, canonical physical location, eliminating all sync scripts and import fragility. The 3-file manifest (MANIFEST, SUMMARY, DIRECTIVES) achieves ~800 tokens by splitting machine-verifiable metadata, dense human-status bullets, and immediate action items. Executor custody (Q3-C) with operator pasting only a pointer‑manifest removes sustained manual state‑keeping. Defense-in-depth (Q4‑D) layers git pre-commit, PreToolUse exit-2, and a `/save` validator—each catches a different non‑compliance mode, matching the empirical 96‑99% adherence. Rolling out via a single‑repo pilot (Q5‑A) bounds risk. If the workspace restructure is clean and the SUMMARY stays disciplined, this permanently solves cross‑repo drift without ongoing maintenance.

**Assessment**: Partially agree.  
The workspace pattern is the most robust for convention fidelity, but the restructuring cost and the handoff token risk keep it from being clearly superior.  
**Strongest point**: The one‑time restructure permanently eliminates propagation drift—no scripts, no imports, no per‑repo copies.  
**Weakest assumption**: That `SUMMARY.md` <500 lines reliably stays under the ~1 000‑token target. A 500‑line file of dense bullets can easily exceed 4 000 tokens (8–10 tokens/line). If the operator ever relaxes the discipline, bloat returns to SBAR‑bundle levels.  
**Hidden assumptions**:  
- Symlink/worktree will be fully transparent to all git operations, hooks, and any future tooling; there is no plan for testing this across OS updates or filesystem‑specific edge cases.  
- The browser‑chained architect can function from a manifest of **pointers** despite having no filesystem access. If the operator must manually resolve those pointers during a session, the per‑handoff attention load jumps back to unacceptable levels.  
**Overlooked risks**:  
- The workspace root becomes a single corruption/delete point for all five repos’ conventions.  
- If the architect cannot dereference pointers, the operator will paste the referenced content on‑demand, violating the “no sustained daily manual discipline” constraint.

---

### Proposal B
**Steelman**
A central `.dev-knowledge` repo with per‑repo `@path` imports (Q1‑C) avoids restructuring while guaranteeing a single canonical source. The 2‑file handoff (Q2‑C) splits machine‑checkable metadata (`MANIFEST.md`) from a ~50‑line human‑readable intent (`NEXT.md`), hitting the ~800‑token empirical sweet spot. Executor custody (Q3‑C) re‑uses existing Claude Code infrastructure. Defense‑in‑depth (Q4‑D) stacks three enforcement layers exactly as the earlier hybrid‑layered experiment that reached 96‑99% adherence. The pilot on `.dev-knowledge` first (Q5‑A) is cheap, reversible, and dogfoods the convention system itself. Fallbacks are explicit (sync script if imports break), and no new daemons are added.

**Assessment**: Partially agree.  
This is the closest to an incrementally safe, low‑ops‑overhead solution, but the `@path` import stability and the adequacy of a 50‑line self‑contained summary are the two make‑or‑break points.  
**Strongest point**: It minimises net‑new infrastructure—every moving part is either git or existing Claude Code primitives, keeping the solo dev’s attention budget intact.  
**Weakest assumption**: That Claude Code’s `@path` import semantics will remain stable and not silently degrade. If an update causes imports to resolve differently *without* a hard error, convention drift could go unnoticed for weeks despite the weekly CI diff, because the CI diff itself might be fooled by partial resolution.  
**Hidden assumptions**:  
- All five repos sit on a single filesystem with consistent relative‑path resolution to `.dev-knowledge/`; any network mount, container, or WSL layer could break `@../.dev-knowledge/…`.  
- That 50 lines of plain prose can carry the full state the architect needs to resume. The empirical 98%‑at‑800‑tokens result used *object‑reference sparse context* where the LLM could fetch objects—here the browser architect receives only the 50‑line text and no ability to fetch. If `NEXT.md` is too terse, the operator will have to manually supply missing context during the session.  
**Overlooked risks**:  
- The `MANIFEST.md` contains “object pointers” – if those pointers are not materialised in the pasted payload, the architect cannot resolve them. The proposal does not spell out that the executor must pre‑render all needed context into the payload; it assumes the operator will look up pointers, which is an open manual step per query.  
- A failing CI diff job could be overlooked (solo dev attention budget), letting silent import drift compound.

---

### Proposal C
**Steelman**
A git‑propagation sync script (Q1‑B) gives one canonical source without restructuring or import dependencies. The 2‑file handoff cuts bloat to <800 tokens. Executor custody via Claude Code (Q3‑C) removes op memory load. A single PreToolUse exit‑2 hook (Q4‑B) deterministically blocks all tool‑mediated writes that violate conventions—no multi‑layer complexity. The empirical case that “moving discipline into the executor harness raises adherence to 96‑99%” is cited directly. Pilot on `.dev-knowledge` first. This is the simplest possible harness‑side enforcement, with no extra hooks to tune.

**Assessment**: Disagree.  
The single‑layer enforcement is the critical weakness. The 96‑99% hybrid‑layered result came from *stacked* mechanisms (prompt + harness + checks), not a lone PreToolUse hook. A single hook with a manual bypass backdoor will degrade under time pressure, exactly as Lesson A warns.  
**Strongest point**: Maximum simplicity—fewest new moving parts, one hook to write, one sync script to maintain.  
**Weakest assumption**: That PreToolUse alone can sustain 96‑99% adherence without a second barrier. The prior data shows that any single mechanism (prompt alone, bundle alone) tops out around 85%; the leap to 96+% required layering.  
**Hidden assumptions**:  
- The bypass command will be used only in genuine emergencies; in practice, a busy solo dev will use it whenever the hook feels obtrusive, and the audit log will not be reviewed regularly.  
- That the sync script will be triggered reliably. Automating it via a make target or pre‑commit in the conventions source repo only covers the case when the source is explicitly committed; edits to canonical conventions without a commit still produce drift until the next enforcement check.  
**Overlooked risks**:  
- The PreToolUse hook can be disabled with a config toggle or a Claude Code update; there is no secondary mechanism to catch the resulting compliance collapse.  
- No `/save` validator means a session can end with a corrupted handoff payload (bad checksums, missing files) and the operator will discover it only when the next architect session stalls—this is a time‑bomb under the solo‑dev attention budget.

---

### Revised Recommendation
*(This is my original position, informed by analysing all three proposals, not an arbitration between them.)*

**Composite**: **Q1‑C primary with automated fallback, Q2‑C with a token‑capped self‑contained payload, Q3‑C, Q4‑D, Q5‑A.**

**Rationale**:
- **Convention location (Q1‑C + B fallback)**: Place all canonical governance files in a separate `.dev-knowledge` repo. Each tool repo’s `CLAUDE.md` imports them via `@../.dev-knowledge/…` syntax. This avoids restructuring, keeps one canonical source, and survives a single‑repo checkout failure. To guard against `@path` instability, implement an **automated sync script** (Q1‑B style) that runs on every `git push` / hook, copying the canonical files into each repo and verifying SHA‑256. The sync script is the mechanical backup; the `@import` is the normal fast path. This gives exactly the same guarantees as Proposal B without betting solely on Anthropic’s import stability.
- **Handoff payload (Q2‑C with hard token ceiling)**: The executor generates exactly two files:
  - `MANIFEST.md` — SHA‑256 over the bundle, HEAD pins per repo, tool versions, and a **fully materialised dense context block** (not pointers) that includes the current JOURNAL summaries, top‑N BACKLOG items, and any active LESSONS.  
  - `NEXT.md` — ≤1 200 tokens of plain prose: *What was built / Current state / Immediate next actions / Hard constraints*.  
  Both files together must fit in **≤1 500 tokens** total (measured via the Claude tokeniser). No SBAR narrative, no rationale, no file‑by‑file copies. The materialised block inside `MANIFEST.md` eliminates the pointer‑resolution problem for the stateless browser architect; the operator pastes the whole payload once per handoff, and the architect can resume without further fetches.
- **State custodian (Q3‑C)**: The executor writes the payload to a known location; the operator copies it into the new browser session. This uses only existing Claude Code memory primitives and costs ~30 seconds per handoff. MCP‑based custody is deferred until a second tool requires it, keeping the solo‑dev attention budget intact.
- **Mechanical enforcement (Q4‑D, defense‑in‑depth)**: Stack three layers exactly as in the empirical hybrid‑layered success:
  1. **Git pre‑commit hook** installed in each repo blocks commits if JOURNAL/CHANGELOG haven’t been modified in the session window.  
  2. **Claude Code PreToolUse hook (exit‑2)** blocks any tool call that writes to a file without a corresponding JOURNAL entry staged, or that alters conventions without a checksum match.  
  3. **`/save` slash command** runs a deterministic validator that refuses to emit the handoff if manifest checksums fail or required files are stale.  
  This stacking is non‑negotiable because each layer catches a distinct failure mode; a single hook with a bypass backdoor will regress to ≤85% within weeks.
- **Migration (Q5‑A)**: Pilot the full stack on `.dev-knowledge` only. After **10 consecutive handoffs** achieve ≥96% end‑of‑session compliance and ≤1 500 measured tokens, migrate the other four repos one at a time with a 1‑week soak each. Every step is revertible with a single `git revert`.

**Why I am not adopting Proposal B as‑is**  
It underestimates the “pointers are useless to a browser architect” problem and over‑trusts `@path` import stability. My version hardens both: the payload becomes self‑contained with a materialised context block, and the sync‑script backup eliminates the single point of failure in import resolution.

**Why I am not adopting Proposal A**  
The workspace restructure burns 2‑3 hours on a scenario that can be solved with a 20‑line sync script and an import line. The risk of symlink breakage and the ambiguity of the SUMMARY line limit (500 vs. token‑measured) introduce more unknowns than they remove.

**Why I am not adopting Proposal C**  
Single‑layer enforcement contradicts the empirical evidence that got us from 40% to 96%. Stacking is not over‑engineering; it is the mechanism that works.

**Token estimate validation**  
- 1 500‑token handoff budget: derived from the earlier 800‑token object‑reference result, adding a 700‑token buffer for the materialised context block needed to make it self‑contained. At 20 tokens/dense line, this is ~75 lines of content—sufficient to capture multi‑repo state while staying ~90% below the current 12 000 tokens.

**Signals to revisit**  
- If `@path` imports trigger the fallback sync script more than once per quarter, migrate to Q1‑A (workspace root).  
- If handoff token counts rise above 2 000 for three consecutive sessions, switch to a machine‑readable JSON payload with a human‑readable header.  
- If PreToolUse bypasses occur more than once per fortnight without audit review, add a fourth layer (e.g., a cron job that nags).  
- If a second LLM enters the workflow, build the MCP server for conventions as primary with the sync script as fallback.

*Latency: 276.92s | Tokens: 14423*

### Grok (grok-4.3)

**Proposal A**

**Steelman first:** If the five repositories already share a single physical machine and the developer is willing to accept a one-time topology change, placing all seven governance files at a true workspace root eliminates every source of sync drift permanently. The three-file manifest plus triple enforcement then becomes the minimal sufficient handoff that still preserves checksums and blocks non-compliance at the tool level, achieving the empirical 98 % adherence target with zero daily operator discipline after the initial setup.

**Your assessment:** Partially agree. The workspace-root choice is the cleanest solution to the canonical-source requirement, but the proposal underestimates the blast radius of even a solo-dev restructure when symlinks or worktrees interact with future tooling or OS updates.

**Strongest point:** Defense-in-depth enforcement (git + PreToolUse + /save) is the only combination shown to move adherence from the 40–85 % range into the 96–99 % band.

**Weakest assumption:** That a 2–3 hour symlink/worktree setup will remain stable indefinitely. If the Claude Code project-root detection or git worktree semantics shift, every subsequent handoff silently references the wrong files.

**Hidden assumptions:** (1) The operator will actually notice and repair a broken symlink before the next handoff; (2) the single pilot repo will surface topology problems that would only appear after the other four repos are migrated.

**Overlooked risks:** Symlink or worktree breakage across a Claude or git version bump that produces silent convention drift undetectable by the SHA-256 manifest (because the manifest itself lives in the now-broken location).

**Proposal B**

**Steelman first:** If `@path` imports remain stable for the next 12 months and the developer values 2 a.m. legibility over further token reduction, a sibling `.dev-knowledge` repository plus two-file manifest gives one canonical source without touching repo topology. The triple mechanical enforcement still delivers the required adherence while every migration step remains a single `git revert`.

**Your assessment:** Agree. B is the only proposal that explicitly treats the stability of its chosen import mechanism as provisional and names the exact fallback (Q1-B sync script) if the assumption fails.

**Strongest point:** The explicit “2 a.m. legibility” decision criterion and the corresponding rejection of pure JSON payloads; this is the only proposal that treats future solo-dev context recovery as a first-class requirement.

**Weakest assumption:** That the PreToolUse hook plus `/save` validator will be tuned once and then left alone. Any tightening after the pilot will require coordinated changes across three separate enforcement surfaces.

**Hidden assumptions:** (1) The developer will actually review the weekly CI diff job that detects import drift; (2) handoff frequency will remain low enough that a 30-second manual paste stays tolerable.

**Overlooked risks:** Coordinated failure where an Anthropic release simultaneously alters `@path` semantics and PreToolUse hook behavior, forcing an emergency switch to the sync-script fallback under time pressure.

**Proposal C**

**Steelman first:** If the only acceptable enforcement surface is inside the executor harness itself, then a git-sync script plus a single PreToolUse hard block plus the two-file payload is the smallest possible mechanical system that still meets the adherence and token targets without introducing new daemons.

**Your assessment:** Disagree. C under-specifies how the git-sync script itself is kept in sync and relies on a single enforcement layer (PreToolUse) during the critical pilot phase, which historically leaks.

**Strongest point:** The explicit 93 % token reduction claim tied to the prior empirical 800-token result.

**Weakest assumption:** That a lone PreToolUse hook will be sufficient to force JOURNAL updates on every relevant file change. The proposal itself cites the 40 % implicit-memory failure mode yet offers only one deterministic gate.

**Hidden assumptions:** (1) The sync script will be run after every canonical change because the enforcement hook will catch drift; (2) the operator will treat the bypass command as an exceptional audit event rather than a routine workaround.

**Overlooked risks:** Rapid-iteration sessions where the developer repeatedly uses the bypass, gradually training the habit of disabling the only enforcement layer and returning to the original 40 % adherence regime.

**Revised recommendation**

Adopt Proposal B’s core (`.dev-knowledge` + `@path` + 2-file `MANIFEST.md`/`NEXT.md` + triple enforcement + pilot on `.dev-knowledge` first). The decisive evidence is B’s explicit fallback path and its refusal to treat any new infrastructure (workspace restructure or MCP server) as free. All three proposals correctly converge on executor custody and mechanical blocking; B is the only one that also treats its own import mechanism as fallible and therefore does not create an unstated long-term dependency on Claude Code’s `@path` behavior remaining unchanged. No other proposal’s risk section addresses coordinated Claude release breakage across import and hook surfaces.

*Latency: 24.70s | Tokens: 7398*

## Synthesis (by openai, non-participant)

## Consensus

Strong, evidence-based consensus emerged on four points:

1. **Replace the 11-file ADR-42 bundle with a thin manifest-based handoff**
   - Most participants converged on **2 files** (`MANIFEST.md` + `NEXT.md`), with one proposing 3 files.
   - This was driven by the stated empirical evidence, not mere repetition:
     - current bundle = ~12,000 tokens / ~60% bloat
     - sparse object-reference handoff = ~800 tokens / ~98% adherence
     - hybrid layered approach = 96–99% adherence, <10% bloat
   - The shared conclusion was that **full-file copies must be eliminated** and **HEAD-pin + SHA-256 drift detection must remain**.

2. **State custody should stay with the executor, not a new external system**
   - Broad agreement favored **Q3-C: executor-as-custodian via existing Claude Code tooling**, with operator pasting only a thin payload into the next browser session.
   - This was supported by the constraints:
     - browser architect is stateless and has no filesystem access
     - solo-dev attention budget is limited
     - closed vendor memory cannot be the primary dependency
   - MCP and external memory were consistently treated as optional future additions, not primary architecture.

3. **Convention compliance must be mechanically enforced in the executor/harness, not via prompts**
   - Strong consensus rejected implicit/prompt-only discipline due to explicit failure evidence: **40% adherence is unacceptable**.
   - Most participants endorsed **defense-in-depth**, especially:
     - PreToolUse hook
     - `/save` validator
     - often pre-commit hooks as a third layer
   - This was grounded in prior empirical research that moving enforcement into the harness materially improved adherence.

4. **Migration should be piloted incrementally, not big-bang**
   - Strong consensus supported **Q5-A pilot-first rollout**, usually on `.dev-knowledge` or equivalent first.
   - This aligns directly with the stated requirement that the operator must verify each step before commitment.

There was also broad agreement that:
- **MCP is not justified now** as a primary solution for this solo-dev setup.
- **Vendor memory services should not be the sole memory dependency**.
- **Human legibility matters**, especially for 2am recovery/debugging.

## Unresolved Disagreements

### 1. Where universal conventions should physically live

#### Options debated
- **Q1-A** Workspace root / workspace repo pattern
- **Q1-B** Canonical repo + git propagation/sync
- **Q1-C** Central `.dev-knowledge` + per-repo imports
- **Q1-D** MCP-served conventions

#### The crux
Whether the bigger risk is:
- **structural complexity and path/tooling fragility** from workspace restructuring, or
- **import/sync fragility** from keeping repos separate.

#### Stronger side
**Q1-C with Q1-B fallback** had the stronger argument.

#### Why
The best argument was not “imports are perfect,” but:
- central canonical source is required,
- restructuring 5 repos imposes significant blast radius,
- solo-dev attention budget makes ongoing topology/debug fragility expensive,
- and **sync-script fallback** bounds the downside if imports break.

The workspace argument’s main strength was conceptual cleanliness: one canonical physical location, no sync drift. But it relied on weaker assumptions:
- that worktrees/symlinks/pathing are a one-time cost,
- that IDEs/tooling/CI/project-root behavior won’t become a recurring issue,
- that rollback is easy.

Those assumptions were challenged persuasively and never really answered.

#### Judgment
Choose **central `.dev-knowledge` as canonical source**, but **do not rely solely on imports**. Treat imports as convenience, not the only correctness mechanism. Add automated sync/verification as fallback or guardrail.

---

### 2. Whether the handoff should be 2 files or 3 files

#### Options debated
- **Q2-C** `MANIFEST.md` + `NEXT.md`
- **Q2-A** `MANIFEST.md` + `SUMMARY.md` + `DIRECTIVES.md`
- structured JSON was mostly rejected

#### The crux
Whether a third summary file improves clarity enough to justify the risk of gradual bloat.

#### Stronger side
**2-file handoff** had the stronger argument.

#### Why
The strongest reasoning was:
- a third file has no natural hard boundary and is likely to regrow into the old bundle shape,
- 2 files cleanly separate:
  - machine-checkable state (`MANIFEST.md`)
  - human-readable next-state transfer (`NEXT.md`)
- this is the smallest format that still passes the “2am legibility” test.

The 3-file proposal was weaker because its proposed `SUMMARY.md` cap (“<500 lines”) is not a meaningful anti-bloat control. Several participants correctly noted that this is exactly how document creep reappears.

#### Important caveat
A key critique was valid: **pure pointers are insufficient if the browser architect cannot dereference them**. So the winning 2-file design should not be “manifest with opaque pointers only.” It must be **self-contained enough for a stateless browser handoff**.

#### Judgment
Adopt **2 files**, but ensure the payload includes **materialized dense context summaries**, not just unresolved pointers.

---

### 3. Whether one enforcement layer is enough or defense-in-depth is required

#### Options debated
- **Q4-B** PreToolUse hard block only
- **Q4-D** multi-layer enforcement

#### The crux
Does a single deterministic executor hook suffice, or do the failure modes require layered gates?

#### Stronger side
**Q4-D defense-in-depth** clearly had the stronger argument.

#### Why
This was the most one-sided unresolved issue:
- the evidence cited in the prompt supports **hybrid/layered enforcement**
- the single-layer proposal effectively inferred too much from evidence that did not specifically validate “PreToolUse alone”
- several critiques correctly pointed out that:
  - pre-commit alone is too late / bypassable
  - PreToolUse alone can be disabled, tuned badly, or bypassed in practice
  - `/save` catches session-end corruption the others do not

The strongest version of the layered argument was that **each layer catches a distinct failure mode**:
- PreToolUse: blocks bad writes before damage
- pre-commit: blocks bad commits
- `/save`: blocks bad handoff/session exit

#### Judgment
Use **all three**.

---

## Argument Quality Assessment

### Best-reasoned proposals
The strongest overall reasoning came from the arguments that supported:

- **central canonical knowledge repo**
- **2-file handoff**
- **executor custody**
- **layered enforcement**
- **pilot-first migration**

The best proposals were strong because they:
- directly used the empirical evidence provided,
- respected the solo-dev constraints,
- considered operability under degraded conditions,
- and included fallback paths for their own assumptions.

The strongest arguments consistently emphasized:
- **2am recoverability**
- **bounded blast radius**
- **moving discipline out of prompts and into harness/tooling**
- **not adding infrastructure unless there is a demonstrated need**

### Weaker reasoning
The weaker proposals tended to:
- overestimate the stability of pathing/workspaces/imports without specifying robust verification,
- conflate “hybrid layered success” with “single hook is enough,”
- or assume browser architect pointer dereferencing that the constraints do not support.

### Single strongest argument in the debate
**The strongest argument was that the browser architect cannot dereference filesystem pointers, so a thin handoff must be self-contained enough to resume work without additional manual lookup.**

Why this mattered:
- It cut through superficial agreement on “manifest + pointers.”
- It exposed a gap between the empirical sparse-context result and this actual architecture, where the architect has no FS access.
- It changed the best solution from “just pointers” to “manifest + materialized dense summary.”

That was the most important corrective insight.

### Single weakest argument in the debate
**The weakest argument was that workspace restructuring is basically a one-time 2–3 hour setup cost that permanently solves drift.**

Why weak:
- it understated long-tail maintenance and tooling fragility,
- ignored IDE/project-root/worktree/symlink edge cases,
- and offered little evidence beyond assertion.

It was a neat architectural story, but not well-supported for this real solo-dev context.

## Blind Spots

The debate missed or underexplored several important issues:

1. **How exactly “session window” is determined for JOURNAL/CHANGELOG enforcement**
   - Multiple proposals assumed hooks can tell whether required files were updated “for this session.”
   - Nobody specified the deterministic source of truth for session boundaries.
   - This is critical; vague session detection will cause false positives/negatives.

2. **How the browser architect receives enough context without token creep**
   - Several proposals said “pointers,” but the browser cannot dereference them.
   - The debate identified this problem, but did not fully specify a concrete payload schema that balances:
     - self-contained context
     - token ceiling
     - human legibility
     - checksum integrity

3. **How slash commands, hooks, and git hooks share one validator implementation**
   - Many proposals said “centralize validator logic,” but no one detailed:
     - interface contract
     - invocation semantics
     - cwd/env normalization
     - failure behavior
   - This matters because duplicated logic across 3 surfaces is a drift risk.

4. **What happens on a new machine or cross-device setup**
   - The architecture seems implicitly single-machine.
   - That may be fine, but it should be made explicit and tested.

5. **No concrete success metrics beyond adherence and token count**
   - Good metrics were discussed, but nobody proposed a minimal dashboard/logging scheme.
   - For a pilot, you need explicit measurement:
     - token count
     - handoff recovery success
     - false-block rate
     - missed-update incidents
     - drift-detection incidents

6. **Bootstrap problem for `.dev-knowledge` governing itself**
   - Mentioned, but not resolved.
   - A throwaway repo or dry-run should be part of the plan before dogfooding on the meta-repo itself.

## Recommended Decision

Adopt this composite:

- **Q1:** Central **`.dev-knowledge` canonical repo** for universal conventions, with **per-repo import/reference as convenience**, but backed by **automated sync/verification fallback**
- **Q2:** **2-file handoff**
  - `MANIFEST.md`
  - `NEXT.md`
- **Q3:** **Executor-as-custodian** using existing Claude Code facilities; operator pastes the generated thin payload into the next browser architect session
- **Q4:** **Defense-in-depth enforcement**
  - PreToolUse hard block
  - git pre-commit hook
  - deterministic `/save` validator
- **Q5:** **Pilot-first migration**, starting with a dry-run repo, then `.dev-knowledge`, then one repo at a time

### Rationale
This best fits the actual evidence and constraints:

1. **Preserves the empirically validated direction**
   - discipline moves into harness/tooling
   - handoff becomes manifest + summary, not file bundle
   - drift detection remains intact

2. **Minimizes new operational burden**
   - no new MCP server required now
   - no external memory service dependency
   - no large workspace restructuring

3. **Avoids over-trusting a single mechanism**
   - imports may break
   - one hook may leak
   - pointers alone may be unusable
   - therefore the right architecture is layered and bounded, not elegant-but-brittle

4. **Matches the real browser/executor split**
   - executor can access local state and validate
   - browser architect cannot
   - therefore the executor must emit a **self-contained, legible handoff payload**, not just references

### Precise form of the handoff
The debate supports a refinement beyond the listed options:

#### `MANIFEST.md`
Include:
- HEAD pin per repo
- SHA-256 checksums
- tool/model/version metadata
- list of referenced objects/paths for auditability
- **materialized compact state extracts** for anything the browser architect actually needs and cannot fetch:
  - active task(s)
  - top backlog items relevant to next step
  - current constraints
  - current repo/revision map
  - recent lessons if active
  - affected files/components

#### `NEXT.md`
Keep to ~50 dense lines or equivalent token cap:
- Built
- Current state
- Immediate next actions
- Hard constraints
- Open risks/blockers

This preserves 2am legibility while avoiding unresolved pointers.

### Strongest objections and why they were outweighed

#### Objection: Workspace root is cleaner and eliminates drift physically
True, but cleanliness was outweighed by:
- higher restructure blast radius
- more path/tooling fragility
- weaker reversibility
- mismatch with the solo-dev “don’t create new maintenance classes” constraint

#### Objection: Imports may break silently
Also true. That is why the decision is **not import-only**. The answer is:
- central canonical repo
- imports where useful
- automated verification/sync fallback
- checksum-based drift checks

#### Objection: 2 files may omit needed nuance
Valid, but the 3-file answer had no convincing anti-bloat control. The correct response is not “add a third file”; it is “make the 2 files slightly more self-contained and mechanically token-capped.”

## Risks

1. **Import/reference mechanism drift**
   - Risk: `@path` or equivalent behavior changes silently.
   - Mitigation:
     - automated parity check against canonical source
     - sync-script fallback ready from day one
     - alert on mismatch, not just weekly passive check if possible

2. **False positives from enforcement hooks**
   - Risk: developer disables hooks out of frustration.
   - Mitigation:
     - one shared validator implementation
     - pilot tuning period
     - measure false-block rate
     - prefer narrowing rules over introducing casual bypasses

3. **Payload regrows over time**
   - Risk: `NEXT.md` becomes narrative bloat.
   - Mitigation:
     - hard token cap
     - deterministic `/save` validation
     - fixed section schema
     - reject over-limit handoffs

4. **Self-contained handoff still lacks enough context**
   - Risk: browser architect asks for manual follow-up context, reintroducing operator burden.
   - Mitigation:
     - explicitly include compact materialized extracts for non-dereferenceable context
     - measure “additional operator clarification requests per handoff” during pilot

5. **Bootstrap/circularity in `.dev-knowledge` pilot**
   - Risk: testing the governing repo on itself masks setup issues.
   - Mitigation:
     - first run one throwaway dry-run repo/session before `.dev-knowledge`

6. **Hook/version drift in Claude Code**
   - Risk: PreToolUse or slash command semantics change.
   - Mitigation:
     - keep validator logic external and versioned
     - add smoke test after Claude Code updates
     - ensure git hook still provides partial protection

## Action Items

1. **Create canonical repo**
   - Stand up `.dev-knowledge` as the single source of universal conventions:
     - `AGENTS.md`
     - templates
     - validator scripts
     - handoff schema
     - ADR index

2. **Define the new handoff schema**
   - Finalize:
     - `MANIFEST.md` fields
     - `NEXT.md` sections
     - token caps
     - checksum requirements
   - Explicitly require **materialized compact context**, not pointers alone.

3. **Build one shared validator**
   - Implement a single deterministic validator script/library used by:
     - PreToolUse hook
     - pre-commit hook
     - `/save` command
   - Normalize cwd/env handling.

4. **Define session-boundary semantics**
   - Decide exactly how “this session updated JOURNAL/CHANGELOG/BACKLOG/LESSONS” is detected.
   - Make it mechanical and auditable.

5. **Implement enforcement layers**
   - PreToolUse: block non-compliant writes
   - pre-commit: block non-compliant commits
   - `/save`: block invalid handoff emission or session-end

6. **Add canonical parity verification**
   - Implement automated check that each repo’s effective conventions match `.dev-knowledge`
   - If using imports, verify resolved content
   - If imports fail, enable sync-script fallback

7. **Run bootstrap dry-run**
   - Test the whole flow in a throwaway repo/session first to de-risk self-governance issues.

8. **Pilot on `.dev-knowledge`**
   - Use the new process exclusively there for a fixed pilot window.
   - Track:
     - handoff token count
     - convention adherence
     - false-block rate
     - extra clarification requests
     - checksum/drift incidents

9. **Set explicit rollout gates**
   - Example:
     - ≥95–98% compliance
     - ≤1,500 token total handoff budget
     - zero missed checksum/drift detections
     - acceptable false-positive rate
   - Only then migrate one repo at a time.

10. **Document fallback modes**
   - If imports break → switch to sync mode
   - If PreToolUse breaks → rely temporarily on pre-commit + `/save`
   - If payload exceeds cap → trim materialized context according to explicit priority rules

Overall: the debate was sufficiently conclusive to recommend a direction. The winning architecture is **central canonical knowledge + 2-file self-contained handoff + executor custody + layered mechanical enforcement + pilot-first rollout**, with the key correction that the handoff must be **self-contained for a stateless browser architect**, not just pointer-based.
