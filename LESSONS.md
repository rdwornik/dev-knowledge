# Lessons Learned — Append-Only Log
<!-- scope: hybrid -->

> **Format:** `### YYYY-MM-DD | source | lesson | category | [scope: X] | action taken`
> New entries go at the bottom. Never edit old entries. Never delete.
> Last updated: 2026-04-30

---

> Split trigger (when navigation by topic becomes painful) deferred 2026-04-24. Rationale: ADR-29 [scope: X] inline field provides equivalent filtering without losing chronology. Reopen if filtering by scope proves insufficient.

## Entries

### 2026-04-21 | browser-chat | Browser-as-tutor defaulting violates three-layer architecture | process | caught + corrected mid-session

### 2026-03-25 | corp-monorepo session | "Stop debating, start deploying" — council debates are valuable but can become procrastination | process | Hard rule: max 2 debates before implementation

### 2026-03-26 | corp-monorepo session | HyperAgents: "Last triggered" date on persistent lessons enables data-driven pruning — agents that track frequency improve faster | architecture | Added to gotchas skill format

### 2026-03-26 | corp-monorepo session | Claude synthesizer costs $0.23/debate (46% of total) — switch to Gemini ($0.04) for synthesis | token-optimization | Updated council default synthesizer to gemini

### 2026-03-28 | dev-practice session | Opus output verbosity (7.5:1 output-to-input ratio) is the main token drain, not model choice | token-optimization | Added conciseness instruction to CLAUDE.md

### 2026-03-28 | dev-practice session | /clear between tasks saves 30-40% input tokens — council unanimous #1 optimization | process | Added to session management workflow

### 2026-03-28 | dev-practice session | Claude Code PowerShell tool requires explicit CLAUDE.md instruction "prefer PowerShell" — settings.json alone insufficient | gotcha | Added Shell section to CLAUDE.md

### 2026-03-28 | dev-practice session | Native installer auto-updates, npm is deprecated — migrate before deploying skills | tooling | Migrated to native Claude Code installer

### 2026-03-28 | dev-practice session | Nested _outputs/_outputs/ caused by script writing to wrong relative dir — always verify output paths | architecture | Added to gotchas

### 2026-03-28 | dev-practice session | "Sacrifice formatting to save tokens, never sacrifice content" — for handoffs between tools | prompt-craft | Created /handoff command

### 2026-03-28 | dev-practice session | Don't constrain output by volume ("max 50 lines") — constrain by format ("flat not tables") | prompt-craft | Corrected /handoff prompt

### 2026-03-28 | corp-monorepo retrospective | Never trust "it's done" from AI in a long session — context degradation accelerates after ~4 hours, AI confabulates based on stale mental model | process | Added verification after every major operation as hard rule

### 2026-03-28 | corp-monorepo retrospective | "Commit and move on" is a trap — optimizing for closure over correctness. When the human says "something feels off" — STOP and investigate, don't reassure | process | Handoff written continuously, not at session end

### 2026-03-28 | corp-monorepo retrospective | Any path change is a database migration — editable installs bake absolute paths, ops.db rows have old paths, venvs have baked paths, PowerShell profile on OneDrive | gotcha | Created path_consumers.md checklist concept; added editable-install reinstall to gotchas

### 2026-03-28 | corp-monorepo retrospective | .ecosystem/ needs enforcement, not just convention — conventions in markdown are suggestions, without validation script drift is inevitable | architecture | Added validation rules to corp doctor

### 2026-03-28 | corp-monorepo retrospective | Claude.ai guesses file paths from memory, Claude Code sees actual files — never let Claude.ai generate filesystem commands from stale mental model | process | Prompts for Claude Code are QUESTIONS not COMMANDS; Claude Code discovers state first

### 2026-03-28 | corp-monorepo retrospective | Naming decisions drain disproportionate energy (ADHD perfectionism loop) — set timer: 2 min to propose, 1 min to pick, never reopen | process | 3 options → 30 seconds → pick shortest → move on

### 2026-03-28 | corp-monorepo retrospective | Test after each structural change IMMEDIATELY, not at the end — broken editable installs after Scripts/ → Dev/ migration found 2 hours late because tests ran at the end | gotcha | Added "pytest after each step" to every Claude Code prompt format

### 2026-03-28 | corp-monorepo retrospective | Council decisions need instant ADR capture — 22 debates but ADRs #13-21 were missing for days because the pipeline was manual | process | Designed corp council-archive automation; until scripted, added to session protocol checklist

### 2026-03-28 | corp-monorepo retrospective | Handoff quality determines next session quality — writing handoffs at end of session = lowest energy, most degraded context, highest time pressure | process | Write handoff notes continuously (JOURNAL entries after each task), final handoff is just formatting

### 2026-03-28 | corp-monorepo retrospective | "One more thing" anti-pattern — cleanup work is fractal, every dirty corner reveals 3 more. Session planned for 2 tasks expanded to 13 | process | Hard rule: 1-2 objectives per session, everything else → backlog. Set context budget: "50% context left = write handoff"

### 2026-03-28 | corp-monorepo retrospective | Don't declare victory before user sees results — sandbox renames, vault rebuilds, extraction outputs need human review step before "done" | process | Added REVIEW CHECKPOINT markers in prompts; "show me 3 examples" before "clean up the rest"

### 2026-03-28 | corp-monorepo retrospective | Git discipline was non-negotiable but got negotiated — session ended with 27 modified, 20 untracked files. Commits batched instead of per-step | gotcha | "git status must show clean between each numbered step" added to prompt format

### 2026-03-28 | corp-monorepo retrospective | Best Claude Code prompts are investigative (UNDERSTAND → PLAN → EXECUTE → VERIFY → COMMIT), not imperative commands | prompt-craft | Updated prompt format: always start with UNDERSTAND, never skip to EXECUTE

### 2026-03-28 | corp-monorepo retrospective | Handoff generator only as good as its sources — update_handoff.py produced 113-line doc missing 80% of state because it read narrow inputs | architecture | Handoff generator must read ALL sources (JOURNAL, decisions/, eval/, git log, test results) + include "Generated from" footer

### 2026-03-29 | dev-practice-os session | verify: lines transform gotchas from "text Claude hopefully reads" into "rules Claude automatically verifies" — machine-checkable enforcement beats documentation | architecture | Added verify: lines to all 41 gotchas (27 auto-verifiable, 14 manual debt)

### 2026-03-29 | dev-practice-os session | core-invariants.md with paths: **/* loads on every file touch, surviving context compaction — compression-proof rules for the 5 most critical safety rules | architecture | Created ~/.claude/rules/core-invariants.md

### 2026-03-29 | dev-practice-os session | Every prompt should include Model/Mode/Effort table — deterministic routing replaces "use judgment" for ADHD-friendly zero-decision workflow | prompt-craft | Added summary table to PLAYBOOK Section 2 with quick-reference examples

### 2026-03-29 | dev-practice-os session | Claude.ai browser role is NOT just "architecture" — it's critical thinking layer that challenges, pushes back, says "no." Rubber-stamping is a failure mode | process | Updated PLAYBOOK Section 7 with explicit critical thinking mandate

### 2026-03-29 | dev-practice-os session | Knowledge domains should stay separate — pre-sales work knowledge (vault) and dev practice methodology (.dev-knowledge/) serve different contexts, mixing them pollutes search and creates cognitive noise | architecture | Kept vault for work knowledge only, dev practice stays in Dev/.dev-knowledge/, Claude Code config stays in ~/.claude/

### 2026-03-29 | self-evolving-article analysis | Self-evolution article's biggest insight: corrections.jsonl + auto-promotion on 2nd occurrence. Most of the article's infrastructure (agents, path-scoped rules) we already had under different names | tooling | Cherry-picked 5 actionable items (verify lines, corrections log, core-invariants, /boot, session scorecard), skipped the rest

### 2026-03-29 | dev-practice-os session | repos with <100 stars and v0.1.0 = too early to adopt, even when they solve real pain — agentfiles (25 stars, 1 day old) and skill-kit (31 stars, 0 releases) failed own criteria | process | Documented in PLAYBOOK Section 9, enforced as evaluation checkpoint

### 2026-03-28 | council-token-optimization | Every routing decision between providers is a "cache miss that flushes the developer's working set" — for ADHD, fewer providers = higher throughput, even if multi-provider is theoretically cheaper | architecture | Stay on single Claude Max, rejected GLM-5.1 dual-backend

### 2026-03-28 | council-token-optimization | Time-shifting heavy work to 08:00-14:00 CET leverages Anthropic off-peak (3-8AM ET) AND ADHD morning hyperfocus window. Afternoon = light work only (review, docs, testing) | process | Calendar blocked, added to ROUTING.md time-shift section

### 2026-03-28 | council-token-optimization | Manual token logging in spreadsheets has "terrible survival rate with ADHD" — automate or use gut-check: "did I hit rate limit today? what was I doing?" | process | No spreadsheet, intuitive daily check only, re-evaluate GLM on April 12 if limits hit >2x/week

### 2026-03-28 | council-token-optimization | The cheapest tokens are the ones you don't send — /clear between tasks (30-40%), front-load specs (15-25% fewer roundtrips), line ranges (10-20%), batch changes (10-15%) | token-optimization | Ranked by impact/effort, implemented as habits not tools

### 2026-03-28 | council-token-optimization | Compaction at 40% (not 50%) is aggressive but correct — long sessions carry too much dead context. Set-and-forget config wins over willpower-dependent habits | token-optimization | Config: CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=40

### 2026-03-29 | dev-practice-os session | Lessons from chats die in browser history if not extracted — need explicit end-of-chat extraction step: "what 2-3 things did I learn?" → append to LESSONS.md | process | Added extraction process to PLAYBOOK and SESSION_SETUP

### 2026-03-29 | axel-bitblaze article | After 2 failed attempts → /clear and rewrite prompt from scratch. Polluted context with wrong approaches actively hurts — fresh context almost always nails it | process | Added as golden rule to PLAYBOOK Appendix C and ESSENTIALS

### 2026-03-29 | axel-bitblaze article | ! prefix runs shell commands directly without Claude processing — !git status, !pytest inject output to context at zero AI token cost | token-optimization | Added to ESSENTIALS and PLAYBOOK Appendix A+C

### 2026-03-29 | axel-bitblaze article | CLAUDE.md instruction adherence drops above 200 lines — confirmed our architecture decision to split rules into ~/.claude/rules/ and skills/gotchas/ instead of one mega CLAUDE.md | architecture | Noted as validation, no action needed (already doing this)

### 2026-03-29 | council-browser-handoff #24 | Browser handoff is a checkpoint, not an autopsy — trigger at ~2 hours while context is fresh, not at 4+ hours when context is degraded. Generate → Copy → Paste, zero archiving step | process | Added to PLAYBOOK Section 8, SESSION_SETUP, ESSENTIALS

### 2026-03-29 | council-browser-handoff #24 | One universal handoff format, zero choices for Rob — Claude auto-adapts sections based on chat content (programming vs business). Two templates = branching decision = ADHD death | architecture | Single template with optional sections, Claude decides

### 2026-03-29 | dev-practice-os session | Council debate format is NOT Claude Code prompt format — debate = YAML frontmatter + question + numbered options + constraints. Prompt = Model/Mode/Effort + UNDERSTAND + Steps. Mixing produces bloated narrative debates | prompt-craft | Corrected browser handoff debate format

### 2026-03-30 | universalization session | Content written during project work gets absorbed wholesale — always abstract into universal methodology before writing to .dev-knowledge/ | architecture | universalization pass completed

### 2026-03-30 | universalization session | Name folders by function not origin — .ecosystem/ was a relic of "ecosystem of packages" mental model, docs/ is universally understood | process | .ecosystem/ eliminated, docs/ standardized in PLAYBOOK

### 2026-03-30 | universalization session | One governance home, zero exceptions — decisions/ at root alongside docs/ breaks "one home per file type" immediately after establishing the rule | architecture | decisions/ moved to docs/decisions/

### 2026-03-30 | universalization session | Skills scoping: ~/.claude/skills/ = universal (loads everywhere), repo/.claude/skills/ = project-specific (auto-discovered). When in doubt, project scope — better to load explicitly than pollute globally | tooling | gotchas split 3 universal + 37 project-specific

### 2026-03-30 | Codex audit session | Audit-first, fix-second is the only safe order — jumping straight to fixes without a read-only audit produces thrash: fixes invalidate each other, new issues appear mid-session, scope creeps | process | Established Audit-Fix-Verify cycle: read-only pass → triage by severity → fix by tier → re-audit

### 2026-03-30 | Codex audit session | Two AI reviewers catch different blind spots — Claude Code misses structural violations it introduced; Codex flags them because it has no authorship bias. Reviewer ≠ builder | architecture | Hard rule: Codex reviews, Claude Code builds. Never reverse the roles.

### 2026-03-30 | Codex audit session | Structural refactors need shims, not big-bang rewrites — renaming a module used in 40 places requires a compatibility shim first, then migrate callers incrementally, then remove shim | process | Added to PLAYBOOK S16; applies to any change with N>5 call sites

### 2026-03-30 | Codex audit session | ARCHITECTURE.md is the highest-value deliverable of any major session — code can be re-derived from git, but the "why" behind structural decisions evaporates in 48 hours | architecture | Any session that touches module boundaries or dependency direction must produce or update an ARCHITECTURE.md

### 2026-03-30 | Codex audit session | Automated audit false-positive rate ~30% — calibrate AGENTS.md severity levels against real violations before treating every flag as critical. Over-flagging → flag fatigue → real issues ignored | process | After first audit run: triage flags manually, demote false-positive patterns to MEDIUM/LOW in AGENTS.md

### 2026-03-30 | dev-practice session | Universal rules that don't apply universally erode compliance — if a Playbook rule says "update per-module READMEs" but the project has no modules, Claude Code learns that Playbook rules are suggestions. Fix: declare project scale (L/M/S) in CLAUDE.md, tag scale-dependent rules in Playbook, leave universal rules untagged. Rules that apply — apply always. Rules that don't apply — are explicitly scoped out, not silently ignored | process | Added Project Scale Tier system to PLAYBOOK.md and ESSENTIALS.md

### 2026-03-30 | dev-practice session | TODO markers belong in code and tasks/todo.md, never in documentation — TODO in code = technical debt marker (valuable, TODO Tree tracks it). TODO in docs = noise — docs are instructions, not task lists. If a doc needs work, add entry to tasks/todo.md with file reference, don't leave TODO in the doc itself. Applies to all project scales | process | Rule established; applies to all repos

### 2026-04-15 | corp-monorepo tach-adoption session | Intent-based module classification fails; use actual import graph — when classifying modules into architectural layers, don't rely on design intent documents. Use tach sync output (AST-parsed imports) as ground truth. corp.project_resolver was classified as orchestration by intent but imported by core modules. corp.query_engine was classified as interface but imported by orchestration. Tach sync revealed the truth in seconds. Applies to Scale L projects. | architecture | Use tach sync as classification ground truth before writing boundary rules

### 2026-04-15 | corp-monorepo tach-adoption session | Baseline violations are documentation, not blockers — when adopting boundary enforcement (Tach, lint rules), document baseline violations and fix in a separate phase. Phase 1 = instrumentation + documentation. Phase 2 = reclassification fixes. This prevents scope creep and keeps each PR focused. CI may fail between phases — this is known and acceptable if Phase 2 follows immediately. | process | Phased adoption: instrument first, fix in dedicated follow-up PR

### 2026-04-15 | corp-monorepo council-session | Council debate quality scales with real data — Council #26 brief improved significantly after feeding it real numbers (0 import violations from grep, pytest timing 166s, .pre-commit-config.yaml contents). Briefs without repo-specific data produce generic recommendations. Always run data-gathering audit before Council debate. | process | Gather concrete repo metrics before writing Council brief

### 2026-04-24 | stream-a-finale | Prerequisite guards prevent cascade failures across multi-prompt streams | gotcha | [scope: meta] | added prereq check pattern to prompt template

### 2026-04-24 | stream-a-finale | ADR prescription can drift from validator reality — H1 insertion point for LESSONS.md file-level tag discovered wrong only during implementation | process | [scope: meta] | amend ADR when reality proves prescription wrong, do not reopen the decision

### 2026-04-24 | stream-a-finale | Sanity-check step after any bulk change catches systematic errors — Prompt 3.5 caught 5 of 20 top-level PLAYBOOK tag mismatches | process | [scope: dev] | added sanity-check pattern to prompt template for bulk tagging operations

### 2026-04-21 | .dev-knowledge audit + Council #27 session | Session wyprodukowała 4 process-level lessons about (a) handoff content granularity — WHAT vs HOW-level detail, (b) browser-chat-as-tutor anti-pattern (proactive session transitions violate PLAYBOOK S8), (c) scope creep flagging — real-time detection zamiast post-hoc, (d) decision fatigue predictability at >3h / >3 decisions. See handoff 2026-04-21-dev-knowledge-architecture-redefinition.md for detail and generative rule candidates. | process / meta | [scope: unknown] | Lessons 1, 2, 4 mają generative rule candidates — promote to PLAYBOOK/HANDOFF_PROCESS.md przy drugim powtórzeniu pattern (per feedback loop rule). Lesson 3 = specific-case observation.

### 2026-04-24 | repo hygiene session (handoff/ → handoff-prompts/ rename) | Renames that create basename collisions with in-scope files expose validator path-handling assumptions. When validator uses basename lookups (rather than full-path), a file with the same name in a skipped directory can spoof in-scope file's HEAD content, corrupting ratio calculations. Fix: validators should match on full path + ensure is_in_scope() guard before substituting staged content. | [unknown] | [scope: dev] | [unknown]

### 2026-04-24 | repo hygiene session (README.md rewrite) | File-level scope tag (placed under H1) causes validator to count all sections as 1 for ratio purposes, shrinking denominator and triggering false regressions when the file's headers are counted separately. Prefer per-section tags (each H2 tagged individually) over file-level tag for repos with ratio-based enforcement. File-level tag remains appropriate for append-only logs (LESSONS.md) where section count is not meaningful. | [unknown] | [scope: dev] | [unknown]

### 2026-04-25 | Gap #1 implementation — validator vs pre-commit hook divergence | validate_scope_tags.py when invoked without arguments (manual sanity check) processed zero files and printed "all files pass" — a vacuous pass. Pre-commit hook correctly passes staged filenames via pass_filenames: true, so it caught missing H3 scope tags that the manual run missed. Both tools apply the same rule (H2 and H3 headings require scope tags, per H2_RE = re.compile(r"^#{2,3}\s+")); the divergence was invocation semantics, not logic. Fix: main() now falls back to scanning all in-scope files when called with no args. Governance tools that share enforcement rules must produce identical results on identical content regardless of invocation mode — "passes here, fails there" is a silent false-negative, not a tolerated difference. | [unknown] | [scope: dev] | main() now falls back to scanning all in-scope files when called with no args.

### 2026-04-25 | Gap #7d v1.0 drift (subagents documented as "deferred/none active" while two existed at ~/.claude/agents/) | Documentation prompts prescribing absence claims must include filesystem verification step — without it, prescription propagates assumptions that may already be false | process | [scope: meta] | counter-pattern: every absence claim in a prompt's UNDERSTAND or Step 1 must have a corresponding ls/find/grep command verifying the absence

### 2026-04-26 | HANDOFF_PROCESS.md v1.0 → v1.1 amendment discovered mid-handoff | Process specifications need full-cycle dogfooding before ratification — gaps only appear when actually running the full cycle | process | [scope: meta] | before merging a process spec, run one full cycle following it literally; whatever felt missing or improvised becomes v1.1 amendment input

### 2026-04-26 | AGENTS.md sycophancy mid-session (browser conceded to Rob's outdated mental model instead of defending post-reconciliation state in PLAYBOOK) | Decision fatigue creates sycophancy — agreeing with user's outdated mental model instead of defending recent implementations | process | [scope: meta] | counter-pattern: when user expresses doubt about a recent decision, verify against current PLAYBOOK before conceding; concession without verification is sycophancy disguised as agreeableness

### 2026-04-26 | Stream C scope discovery — handoff instances vs handoff intelligence conflated | Conflating concepts that share a name but address different concerns creates inferior solutions — two different concerns require two different mental models even if vocabulary overlaps | architecture | [scope: meta] | counter-pattern: when a term feels overloaded, force separation — list concerns explicitly and assign each its own structure

### 2026-04-26 | Stream B → Stream C discovery (19 gaps closed, 14 foundational gaps invisible until post-stream reflection) | Stream completion ≠ scope completion — closing all known gaps still leaves unknown gaps invisible | process | [scope: meta] | counter-pattern: build "what didn't we look for?" check into stream closure ritual before declaring stream done

### 2026-04-26 | Stream B → Stream C handoff attempt produced 1 artifact instead of 3, caught only by Rob's pushback | Handoff process drifts to shortcuts under decision fatigue — 3-artifact checklist blocks "done" status if any artifact missing | process | [scope: meta] | handoff template includes literal 3-artifact checklist at bottom; missing entry blocks done status

### 2026-04-26 | AGENTS.md error originally omitted from error list (selective error reporting masquerading as self-criticism) | Selective error reporting — when listing own errors, check for selection bias; errors-that-make-me-look-bad are omitted as readily as errors-that-make-me-look-reasonable | process | [scope: meta] | counter-pattern: when self-listing errors, force inclusion of most embarrassing error first, before the easy-to-admit ones

### 2026-04-26 | AGENTS.md reconciliation forgotten twice despite being documented in PLAYBOOK lines 58 and 72 | After reconciliation, mental model can revert to pre-refactor state under fatigue — refactored truth lives in PLAYBOOK, mental memory does not always update | process | [scope: meta] | counter-pattern: when in doubt about state of recently-reconciled concept, grep PLAYBOOK before responding

### 2026-04-27 | Stream C session 1 deep cleansing audit | Audit agents can hallucinate specific file metadata (line counts, filenames, content claims) that reads as confirmed evidence. The "1019 lines" detail in N1 finding looked authoritative but was fabricated for a non-existent file. Counter-pattern: any audit finding citing specific file metrics requires ground-truth verification (ls, find, wc -l) before acting on it. | dev | [scope: meta] | Audit N1 marked INVALID, no fix attempted

### 2026-04-27 | Tier 3 Prompt 2 session summary incident | Session summaries can confabulate completed work as pending — model listed R1/R3/N1/E1 as pending despite all four being completed earlier in the same session via prior commits. State claims in session summaries are authoritative-sounding but not auto-verified; git log was visible and still not cross-checked. | process | [scope: meta] | counter-pattern: verify every "pending" and "done" claim via git log + filesystem check before including in session summary; R1/R3/N1/E1 false pending discovered only after Rob's explicit pushback

### 2026-04-27 | JOURNAL.md creation halt — third governance failure in single session (N1 hallucination, false PENDING, JOURNAL spec miss) | Before proposing artifact creation, search governance docs for existing spec with same artifact name — all three failures share root cause of operating on assumed/cached knowledge without verification. Three failures in one session is a pattern, not coincidence. | process | [scope: meta] | counter-pattern: any artifact-creation or governance-amendment prompt must explicitly grep PLAYBOOK + CLAUDE.md + audit docs for existing spec with same name before proposing creation; treat artifact name as search term, not assumption

### 2026-04-27 | Stream C session 1 final consolidation | Codex review applies to code repos only — doc-only repos (.dev-knowledge — governance markdown, no application code) skip /review even for foundational changes (multi-file governance amendments, new file creation). Triggering /review based on "scope size" or "governance importance" alone is wrong when no executable code is involved. | process | [scope: meta] | decision rule: /review required only when commit modifies executable code, scripts affecting runtime, or config altering behavior; pure markdown/governance/doc edits skip Codex

### 2026-04-28 | session | Never use dates as deadlines in recommendations | meta | scope: meta | rule
Claude must NOT introduce dates as deadlines for tasks unless Rob
explicitly states a deadline. Past pattern: AI introduces "expires
May 5" framing → creates false urgency → distorts prioritization.
Time-sensitive items get flagged WITHOUT date framing — describe
the constraint, not the calendar.

### 2026-04-28 | session | Don't create new files when existing structures cover the gap | meta | scope: meta | rule
Before creating a new markdown file, check: does JOURNAL, HANDOFF,
ADR, or existing protocol cover this? If yes — use existing
structure. Creating new files is breach of CLAUDE.md "Do not create
new markdown files without checking README.md growth triggers."
Default: extend existing, don't proliferate.

### 2026-04-28 | session | Distinguish "session close" from "stream done" | meta | scope: meta | rule
Closing a session ≠ closing a stream. After merging session
deliverables, Claude must verify against original stream plan
before declaring stream complete. Pattern-match to "git log clean"
is not sufficient evidence of stream completion.

### 2026-04-28 | session | Pattern-matching on conversation length is not measurement | llm | scope: llm | rule
Trigger for context-quality flag is >40 messages WITH measurable
degradation, not message count alone. Pre-emptive "wrap chat"
suggestions at message 12 = anxiety pattern, not discipline.
Measure actual quality (factual errors, lost context, drift),
not proxy metrics.

### 2026-04-28 | session | Claude Code prompts always English, no exceptions | meta | scope: meta | rule
Personal preferences explicit: "code, commits, professional docs
in English." Claude Code prompts ARE professional docs. Polish in
prompts = breach. Conversational chat with Rob can be Polish;
artifacts and prompts must be English.

### 2026-04-28 | session | Distinguish triggers from limits | meta | scope: meta | rule
Triggers (subjective signals like "hard to navigate") are not the
same as limits (hard caps like "100 entries"). LESSONS.md has a
trigger ("navigation pain"), not a limit. Pattern-matching trigger
as limit = breach intent. Verify language in governance docs:
trigger language ("when X becomes painful") not cap language
("when X exceeds N").

### 2026-04-30 | session-stream-c-debt | Strażnik metodologii musi sam stosować metodologię — JOURNAL/LESSONS skipped through 5 ADR cycles, surfaced only via user pushback | meta | scope: hybrid | action: formal Claude Code prompt template includes JOURNAL update + lessons promotion as mandatory final steps

### 2026-04-30 | adr-37-debate | Confidence level (high/medium/low) without enforcement mechanism = decoration. Markdown cannot force compliance — enforcement belongs in template (first-message.md), not in data field | architecture | scope: dev | action: rejected confidence levels in ADR-37; pattern applies to all future field proposals — verify mechanism before adding metadata

### 2026-04-30 | adr-38-debate | Scrum vocabulary for solo LLM workflow = cargo cult (9 of 12 elements <40% fidelity per Council debate). Structural insight (centralized queue, two-phase boundary) is separable from vocabulary import. Plain English captures value without ceremony tax | meta | scope: hybrid | action: when import suggested, evaluate structural value vs vocabulary tax separately

### 2026-04-30 | session-pacing | "Defer requires justification" applies to Claude's own recommendations, not just to user requests. Pattern still drift-prone — required user pushback to enforce | meta | scope: hybrid | action: self-check "why not now?" before any "later" / "next session" recommendation; concrete reason required or do it now

### 2026-04-30 | adr-37-design | Augment > supersede for widely-adopted artifacts. ADR-37 added top-level overlay over ADR-32 9-section structure instead of replacing — preserved existing handoffs, minimum migration friction, ADR-29 grandfathering pattern applied | architecture | scope: hybrid | action: prefer overlay/augmentation pattern when amending established structures with active usage

### 2026-04-30 | self-audit-architecture-debt | Prescriptive writing without verification is a recurring methodology failure mode | methodology | scope: meta | action: ALWAYS verify content claims against actual files before writing prescriptive registry/calibration/manifest entries
Three instances surfaced in single session 2026-04-30: (1) ADR-39 ARCHITECTURE.md registry entry described "Tach 4-layer taxonomy" but actual file uses 3-layer ecosystem model (different concept entirely); (2) ADR-40 calibration table contained estimates that did not reproduce when algorithm was actually computed (pure fabrication); (3) ai-council module count "estimate ~8" in ADR-40 calibration was 4x off (actual 2 per strict ADR-38 definition). Pattern: writing what content "should be" without checking what content "actually is." Mitigation: registry/calibration/manifest entries MUST be verified against ground truth before ratification. ADR ratification checkpoint should include "registry/table contents verified against actual files."

### 2026-04-30 | adr-37-canonical | Top-level summary = authoritative operational state; detailed sections beneath = reference evidence. "Detailed Context" naming (not "Archival") — workshop floor, not museum. Solves dual-maintenance drift via explicit canonicality rule | architecture | scope: hybrid | action: when overlaying summary over detail, define canonicality explicitly in ADR

### 2026-05-09 | handoff-format-v3 | Three-stage handoff flow with full ecosystem invariants beats ad-hoc curation | methodology | scope: meta | action: ALWAYS include FULL VISION + PLAYBOOK + ESSENTIALS in handoff bundles; ADR essences only when directly driving actions; never duplicate target repo's own artifacts

First v2.0 handoff (2026-04-30 ai-council audit-sync) failed on 6 dimensions: missing ecosystem context (VISION/PLAYBOOK/ESSENTIALS absent), attention dilution from 7 full ADR copies, nested 3-level folder structure broke drag-drop ergonomics, no standardized question pipeline, no return-trip evidence file, single-actor generation without project-level architect intelligence. Council research (2026-05-09) and Rob's strategic directive ("więcej teraz, optymalizować później") converged on three-stage flow: Claude Code generates question prompt → Browser-2 architect provides project intelligence → Claude Code reconciles + generates flat 11-file folder. Full VISION + PLAYBOOK + ESSENTIALS as invariants preserve methodology and conversational consistency across sessions (SECI externalization). Only ADR essences (2-4 sentences per ADR) for ADRs driving specific actions; full ADRs remain in source repos for drill-down. Mitigation: ADR-42 ratified the architecture; v2.0 handoff regenerated as first v3.0 instance.

### 2026-05-09 (afternoon) | handoff-shortcut-failure | NEVER define a process stage as "implicit" or "skippable" without empirical evidence that the stage adds no value | methodology | scope: meta | action: if a stage is defined in a protocol, it must be exercised at least once before any shortcut is considered; "implicit" without test = untested assumption

ADR-42 v3.0 (morning) included clause: "For audit handoffs, Stage 2 is implicit — Claude Code proceeds Stage 1→3 directly using audit report as Stage 2 substitute." This was unjustified — assumed audit findings substitute for browser-2 tacit knowledge without test. Rob caught this: the flow must be exercised, not theorized. Result: shortcut removed, ai-council handoff folder deleted (12 files), HANDOFF_PROCESS rewritten to v3.1, Stage 1 regenerated for proper 3-stage test. Pattern: instance of "prescriptive choice without verification" (see 2026-04-30 self-audit entry). Generalization: any future "X is optional/implicit/skippable for type Y" claim requires either (a) empirical test showing skip produces same outcome as full execution, or (b) Rob's explicit acknowledgment of the assumption with documented rationale.

### 2026-05-09 (later afternoon) | handoff-semantic-misunderstanding | When designing context-transfer protocols, always specify source/destination state (fresh vs dying vs persistent) explicitly — steps without grounded semantics are mechanism without meaning | methodology | scope: meta | action: before writing process steps for any handoff/transfer protocol, diagram the state of each actor (fresh? dying? persistent?) and verify the step directs content to the actor whose state makes the step valuable

ADR-42 v3.1 implementation (9 commits earlier today) instructed Stage 2 architect to "open a new claude.ai chat" — wrong semantics that inverted handoff purpose. Reality: Stage 2 source is the EXISTING browser chat being wrapped up due to context exhaustion. Its tacit knowledge (priorities, mental model, in-flight decisions, recent concerns) is what's being preserved before the context dies. A new chat has no context to add — Stage 2 collapses to audit findings restatement (the rejected shortcut, in different form). Three actors total: Claude Code (orchestrator), OLD chat (Stage 2 source — dying), NEW chat (Stage 3 receiver — fresh). Mitigation: ADR-42 second amendment specifies 3-actor flow; HANDOFF_PROCESS Stage 2 section rewritten; templates corrected; stage1-question.md regenerated. Root cause differs from earlier prescriptive-without-verification pattern: this was not failure to check assumptions against files — it was failure to ground protocol semantics in the actors' context state. Generalization: when designing transfer protocols, always ask "what makes this actor valuable at this stage?" If Stage 2 source is a fresh chat — it has no value. If Stage 2 source is an existing chat with accumulated context — it's irreplaceable.

### 2026-05-09 (late afternoon) | handoff-audience-confusion | Mixed audiences in a single message file contaminate downstream when copy-pasted blindly — use explicit visual delimiters to separate audience-specific blocks | methodology | scope: meta | action: any artifact with multiple readers needs explicit per-audience boundaries (visual delimiter > prose hint); the operator copies only their target's block

ADR-42 v3.1 stage1-question.md had mixed audiences: Rob's operational instructions (open old chat, save response, say "complete handoff") were intermingled with architect-facing question content. Plus receiver synthesis prompt — meant for NEW chat (Stage 3 receiver validating its understanding before acting) — was placed inside Stage 1 question prompt where the OLD chat (Stage 2 responder) would see it confusingly. When Rob copy-pastes the file into the old chat without careful reading, both Rob's operational steps and the Stage 3 synthesis instructions contaminate the architect message. Mitigation: HANDOFF_QUESTION_TEMPLATE refactored with explicit Section A (Rob) / PASTE_BOUNDARY (thick `═` lines) / Section B (architect) structure; synthesis prompt moved to HANDOFF_FOLDER_TEMPLATE for 00_first-message.md generation (correct audience: NEW chat). stage1-question.md regenerated. HANDOFF_PROCESS Stage 1 gen spec updated to remove "Receiver synthesis prompt at end" bullet. Pattern: Claude Code wrote a multi-audience file without reasoning about who reads which part. Generalization: before writing any file that multiple parties consume differently, list the readers and their responsibilities first, then structure file sections accordingly.

### 2026-05-09 (late afternoon) | handoff-friction-precreate | Pre-create downstream files at upstream stage to eliminate operator friction — upstream stages should create the input files downstream stages need | methodology | scope: meta | action: when workflow has multi-step file dependencies, upstream stage pre-creates downstream stage's input file as a template; operator fills content, never creates files

ADR-42 v3.1 Stage 1 generated stage1-question.md but required Rob to manually create stage2-response.md when returning from old chat. Friction: operator opens editor, creates new file, types markdown headings, pastes content. Solution: Stage 1 pre-creates stage2-response.md as placeholder template with 5 expected headings, `[old chat answer]` placeholder text, `═══ REPLACE EVERYTHING BELOW THIS LINE ═══` marker, and instructions header comment for Rob. Rob's only action on return: open existing file, replace placeholder block. Plus: Section B end of stage1-question.md now includes explicit "Format requirements (CRITICAL)" block mandating pure markdown response (no preamble, no code fence wrapper, exact heading format) — LLMs default to "helpful" wrapping that breaks Stage 3 parsing. Pattern: 10th instance today of friction surfacing only when operator runs the actual flow. Generalization: any "file X depends on file Y" workflow should have X pre-created at Y's generation. The pre-created file IS the contract — it shows the shape the downstream expects.

### 2026-05-09 (evening) | stage2-context-completeness | Stage 2 quality bounded by context provided to old chat — role, bundle awareness, epistemic standard, and format requirements must be at TOP of Section B, not buried at end | category: methodology | scope: meta | action: When asking an LLM to answer structured questions for downstream parsing, provide ROLE definition, OUT-OF-SCOPE markers, EPISTEMIC standard, and FORMAT requirements at the very beginning of the prompt — before any content the LLM will be tempted to respond to

First Stage 2 response for ai-council audit-sync was weak: (1) plain-text headings instead of markdown — format requirements were buried at end of long prompt, missed by old chat; (2) fabricated specifics — commit messages, version numbers, agent IDs, config change reasoning — old chat confabulated "lived knowledge" where it had none; (3) duplicated ecosystem-level info — VISION.md schema, ADR-33 mandate details — old chat doesn't know these but mimicked from audit context in the prompt.

Root cause: stage1-question.md didn't tell old chat (a) its ROLE — project-level architect not ecosystem oracle; (b) what's in HANDOFF BUNDLE — so old chat doesn't repeat ecosystem info already covered; (c) EPISTEMIC standard — witnessed vs inferred vs unknown classification; (d) FORMAT requirements at top, not end.

Mitigation: HANDOFF_QUESTION_TEMPLATE Section B restructured with role/bundle/epistemic/format at top before current state, audit context, and questions. Inline epistemic notes added per question. Stage 1 procedure documents this Section B order requirement with rationale.

Pattern: LLM-to-LLM prompts (one LLM asking another to produce structured output) require explicit framing before any content. By the time the responding LLM has read the content, it has mentally committed to a response style. Generalization: any LLM-to-LLM handoff via prompt needs role/scope/epistemic/format framing at the top. Burial = ignored.
