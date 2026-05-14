# Handoff Stage 2 Response: ai-council (session-sync)

<!-- scope: meta -->

**Header**

| Field | Value |
|---|---|
| Repo | ai-council |
| Type | session-sync |
| Slug | `2026-05-14-ai-council-session-sync` |
| Timestamp | 2026-05-14 |

<!--
ROB — INSTRUCTIONS FOR FILLING THIS FILE:

1. Open the EXISTING (OLD) browser chat for ai-council.
2. Paste the block from stage1-question.md (from PASTE_BOUNDARY to end) as a message.
3. The old chat will respond with the 5-section architect answer.
4. Copy that response.
5. Replace EVERYTHING below the ═══ marker line with the copied response.
6. Save this file.
7. Return to Claude Code at .dev-knowledge and say: "complete handoff for ai-council"

Option B: In Claude Code, say "save this response as stage 2 for 2026-05-14-ai-council-session-sync"
and Claude Code will write the response for you.
-->

═══ REPLACE EVERYTHING BELOW THIS LINE ═══

### 1. OBJECTIVE

This section assumes zero prior session knowledge.

ai-council has two clusters of pending work. The highest-value pending item is operational: score the current default synthesizer (Gemini) against the synthesis quality rubric on approximately 15 recent debate transcripts in `output/` to determine whether a synthesizer refresh is empirically justified. This unblocks codification of a cost-optimization principle (synthesizer selection prefers lowest-cost model meeting the quality rubric; higher-cost tiers reserved for cases where lower tiers fail) into ADR-01. The principle is currently captured in `LESSONS.md` but not yet in any ADR.

The governance cluster contains lower-value but lower-risk items, all aligned with `BACKLOG.md` at repo root: AGENTS.md addition (cross-tool LLM agent governance file per PLAYBOOK), hyphen-only filename compliance spot-check (substantially complete per recent work), ARCHITECTURE.md addition (optional at Scale M — the CLAUDE.md Architecture section provides equivalent coverage unless scale escalates), and a state-confirmation pass on `docs/HANDOFF.md` (already removed; see REALITY).

Goal recommendation: operational work first (synthesis scoring → ADR-01 amendment) because it closes a gap in governance documentation that affects future decision-making. The scoring exercise is manual and operator-driven, so if operator engagement is not immediately available, the governance cluster items are quick wins that can fill the session.

### 2. REALITY

This section assumes zero prior session knowledge.

**Working state:** HEAD `0f06955`, branch `main`, working tree clean. Approximately 74 commits ahead of `origin/main` (architect inference based on running count during recent development; verify via `git rev-list --count origin/main..main`). Test count: 362 (architect inference; verify via `pytest --collect-only -q`).

**Recent significant work (traceable in git log preceding HEAD `0f06955`):**

1. Created `VISION.md` at Scale M tier; configured `DEV_KNOWLEDGE_PATH` reference in `CLAUDE.md` per ADR-35 (ecosystem lessons discovery).
2. Shipped cross-project transcript routing feature: `target-project` frontmatter field plus `--target-project` Click flag on the CLI; introduced `dev_root` and `target_projects` list schema in `config/settings.yaml`; added `TargetResolver` in `src/ai_council/routing.py` with fail-loud behavior on unknown target names at parse time.
3. ADR-43 schema refactor: changed `target_projects` from `dict[name, full_path]` to `dev_root: str + target_projects: list[str]` with paths computed.
4. Post-routing cleanup: flipped `secondary_output_enabled` default to `false`; the code path is retained for explicit opt-in.
5. Docs hygiene sweep: deleted `docs/HANDOFF.md` flat file (handoffs are .dev-knowledge domain per ADR-42); consolidated `docs/archive/` content into `docs/audits/`.
6. ADR governance sweep across ADR-01 through ADR-07: status date corrections, factual drift fixes (e.g., ADR-02 default panel 3-model → 5-model), ADR-06 Qwen trial deferred with reopen trigger documented, ADR-07 superseded by ADR-43.
7. Council debate on synthesizer/panel refresh produced unanimous Option B (synthesizer-only refresh, panel composition unchanged, gated on smoke test); transcript routed to `.dev-knowledge/docs/decisions/transcripts/` via the new routing feature.
8. ADR-34 universal hyphen mandate: CLI emitter changed from `council_out_*` to `council-out-*`; downstream patterns and tests updated; cross-repo cycle closed on merge.
9. Combined merge added per-synthesis observability metrics (latency, transcript size, output tokens, error class), created `docs/synthesis-quality-rubric.md` as a 5-point operator-applicable checklist, closed out ADR-06 Qwen trial, and performed Gemini synthesizer version diagnostic.
10. Scrum-master review (.dev-knowledge produced unilateral audit of ai-council, single round trip): nine of ten findings implemented. Notable: retired `tasks/todo.md` (severely stale); created `BACKLOG.md` per ADR-41; updated README architecture section + test count; fixed multiple ADR-34 filename violations (including one fresh violation introduced earlier in the same development period — `SYNTHESIS-QUALITY-RUBRIC.md` renamed to lowercase `synthesis-quality-rubric.md`); archived legacy `_CODE_REVIEW_REPORT.md` audits to `docs/audits/archive/legacy/`.
11. Scrum-master review addendum: moved `tasks/lessons.md` to root `LESSONS.md`; retired `tasks/` folder entirely; renamed `docs/handoffs/_archive/` to `docs/handoffs/archive/`.
12. Most recent commit (`9de640e`): captured a P3 BACKLOG item for an ADR-34 edge case in `council-out-*` filename timestamps (architect inference: the timestamp segment `YYYYMMDD_HHMMSS` retains an underscore between date and time, which is a strict ADR-34 violation if separator rule applies inside the timestamp; deferred to P3 because impact is low and changing format affects sort order and parsing assumptions).

**Work in progress not reflected in commit log:** none witnessed.

**CLI state:** routing.py and emitter changes complete and merged; observability metrics emitted per synthesis run; test suite passing at HEAD. No partial features.

**docs/HANDOFF.md state:** already deleted in recent docs hygiene sweep. The `.dev-knowledge` BACKLOG items relevant to ai-council reference this file as if it still exists — that referenced state is stale relative to ai-council's actual state. Per ADR-41 each repo manages its own BACKLOG; this is awareness, not an action item for ai-council to fix in .dev-knowledge.

**External dependencies:** `.dev-knowledge` repository hosts methodology artifacts (PLAYBOOK, ADR-NN essences, templates including `templates/AGENTS-md-template.md`). Cross-repo writes from ai-council to .dev-knowledge are forbidden per ADR-36 read-only contract. Operator hand-carries any cross-repo artifacts.

**Unclosed thread that genuinely could not close:** cost-optimization principle for synthesizer selection (the principle that synthesizer choice prefers lowest-cost model meeting quality rubric; higher-cost tiers reserved as escalation only) is captured in `LESSONS.md` but is not codified in any ADR. The Council debate that informed this principle recommended a high-cost synthesizer candidate (Claude Opus 4.7) without cost-benefit framing; operator caught the gap. Codification is intended via ADR-01 amendment gated on synthesis scoring data. This is awareness for the receiving session: the principle exists in lessons but is not yet governance.

**Constraints that apply to next session work:**

- Cross-repo handshake convention: well-formed cross-repo requests close in one round trip; multi-turn exchanges signal badly framed request rather than legitimate protocol depth. This supersedes a 4-turn protocol that was tried earlier and found over-engineered.
- Cost-optimization principle (above): governs synthesizer/model selection decisions.
- ADR-34 universal hyphen mandate: lowercase + hyphens in any new filenames (ADR prefix grandfathered).
- ADR-36 read-only contract: ai-council does not write to .dev-knowledge files; operator hand-carries cross-repo artifacts.
- No push to `origin` without explicit operator authorization.
- Fast-forward merges only.
- Codex `/review` required on formal-prompt-scale PRs (three or more files per PLAYBOOK section 15).

### 3. RATIONALE

This section assumes zero prior session knowledge.

**ADR-34 timestamp-underscore P3 capture (most recent commit `9de640e`):** (architect inference — the rationale is not directly witnessed; verify against commit message and BACKLOG entry) the capture likely reflects discovery that `council-out-YYYYMMDD_HHMMSS-topic.md` filenames retain an underscore between date and time segments, which is a strict ADR-34 hyphen-mandate violation if the rule applies inside the timestamp portion. P3 priority suggests low impact assessment — most likely because changing timestamp format would break existing sort-order assumptions and any external parsers/globs. The reasoning behind deferral rather than immediate fix is that ADR-34 was originally aimed at word separators in slug portions, and timestamps are arguably a different category (numeric, structured). The proper resolution requires either an ADR-34 amendment clarifying scope or an explicit exception for ISO-style timestamps. Either path is non-urgent.

**Synthesizer refresh — Option B over Options A and C (Council debate):** the panel reached unanimous Option B (refresh synthesizer only; leave panel composition unchanged), gated on smoke-test data. Reasoning: Option A (no change) ignored evidence that the model landscape had shifted since defaults were set. Option C (refresh both panel and synthesizer) introduced too many variables for clean attribution of quality changes. Option B minimizes blast radius while testing the highest-leverage variable. The smoke-test gate prevents flipping defaults on Council recommendation alone — empirical evidence is required.

**Cost-optimization correction to the Council recommendation:** the Council recommended Claude Opus 4.7 as synthesizer candidate. The recommendation contained a cost-blind spot: Opus tier is approximately 5-10× more expensive than Gemini per synthesis run, and the Council deliberation did not include cost-benefit framing. The operator caught this gap. The corrected approach (test current default first, escalate in cost order only if quality fails) is the cost-optimization principle now sitting in `LESSONS.md` awaiting ADR-01 codification.

**Cross-repo handshake protocol simplification (4-turn → 1-round-trip):** an earlier cycle codified a 4-turn protocol (proposal → approval → closure note → delivery report) for cross-repo amendments. Empirical experience across two cycles showed this was over-engineered for S-scale changes (a few files, mechanical updates). The sharper principle that emerged: well-formed cross-repo requests close in one round trip; needing more than one round signals the request was badly framed, not that the protocol needs more depth. Two cycles closed cleanly under the new principle (cross-repo cycle 2 for ADR-34 hyphen, scrum-master review cycle for the audit response). No Turn 4 delivery reports were produced; git log plus CHANGELOG entries serve as audit trail.

**Scrum-master review pattern (N=1 empirical instance for the ai-council audit):** the `.dev-knowledge` strażnik produced a unilateral audit of ai-council (single direction, no bilateral handshake). The architect implemented findings where there was agreement and would have opened a new conversation for any disagreement. The pattern worked on N=1. Codification into a formal ADR awaits N=2 (a second audit instance, ideally on a different repo) to confirm the pattern is stable.

**BACKLOG structure adoption:** the repo now has `BACKLOG.md` at root per ADR-41 (Scale M mandate). Items follow priority tagging (P1/P2/P3) and stream-aligned organization. This supersedes ad-hoc tracking in `tasks/todo.md` (retired). The migration was clean — surviving todo items were migrated before retirement; no content was lost.

**Combined-merge approach for the Phase-1 + ADR-34 work:** two independent workstreams (per-synthesis observability + ADR-34 hyphen mandate) were combined into a single Claude Code prompt rather than split. Reasoning: operator was explicit about ceremony fatigue at the time, and the workstreams are mechanically independent at file level (different functions, different files). The combined merge produced eight commits cleanly across both concerns; Codex `/review` passed clean. The trade-off accepted: audit-trail granularity (combined session vs separate sessions) for ceremony cost. Worth preserving in future similar decisions.

**AGENTS.md content/scope (deferred):** the scrum-master audit flagged AGENTS.md absent. No specific scope or content decisions were made in subsequent discussion. The `.dev-knowledge` framing was "low urgency; include in future maintenance cycle." Architect inference: the `.dev-knowledge` template at `templates/AGENTS-md-template.md` is the intended scaffold; specifics will be filled by whichever session takes up the work, marking Unknown sections rather than fabricating governance rules.

**Three manifestations of a single failure pattern (worth carrying forward):** during recent extended work, the same boundary-blur pattern surfaced three times in mirror-image forms: defending local repo config as "by-design" when convention divergence was flagged (rejected by operator); accepting a similar local-config defense from another source without questioning it (rejected); and generating a cross-boundary directive in an earlier handoff that asked ai-council architect to reconcile another repo's BACKLOG (caught by operator and the receiving chat). All three are captured in `LESSONS.md`. The structural fix is now codified as the Universal Self-Containment Rule in the handoff process documentation. Default response when convention divergence is flagged: "evaluate against ecosystem baseline," not "intentional per local config."

### 4. DIRECTIVES

This section assumes zero prior session knowledge.

Each directive: action verb + target + verification step.

1. **Score current default synthesizer against synthesis quality rubric.** Operator-driven manual scoring exercise. Select approximately 15 representative recent debate transcripts from `output/`. Apply the 5-point checklist in `docs/synthesis-quality-rubric.md` (position representation, no hallucinated consensus, scannability, faithfulness, verbosity proportionality) to each transcript's synthesis section. Aggregate per-criterion pass rate. Verify: scoring artifact produced (markdown table format suggested); aggregate decision documented (≥80% pass per criterion → no synthesizer refresh recommended; <80% → escalation testing required in cost order).

2. **Codify cost-optimization principle in ADR-01 (gated on Directive 1).** Formal Claude Code prompt for ADR-01 amendment. Amendment text: synthesizer selection prefers lowest-cost model meeting synthesis quality rubric; higher-cost tiers (Sonnet → GPT → Opus, in cost order) are reserved for cases where lower tiers demonstrably fail the rubric. If Directive 1 indicates current default fails rubric, run escalation testing first and include the chosen tier in the amendment. Verify: ADR-01 amended in `docs/decisions/`; principle text searchable; BACKLOG entry for cost-optimization codification closed; CHANGELOG entry recorded.

3. **Add AGENTS.md at repo root.** Reference `.dev-knowledge/templates/AGENTS-md-template.md` as scaffold. Operator delivers template content as artifact if not directly accessible from ai-council session. Cover: cross-tool LLM agent governance (Codex, Cursor, Aider), project context, do-not lists for AI agents. Mark sections "Unknown — operator confirms" where specifics are unclear; do not fabricate governance rules. Verify: file present at root; references `CLAUDE.md`; covers required cross-tool surfaces.

4. **Spot-check ADR-38 Scale M compliance.** Run `git ls-files | grep -E '^(BACKLOG|LESSONS|VISION|README|CHANGELOG|JOURNAL)\.md$'`. Confirm all six files present at root. ARCHITECTURE.md absence is expected at Scale M (optional; CLAUDE.md Architecture section serves equivalent purpose). Verify: command output matches expectation; document any drift.

5. **Spot-check hyphen-only filename compliance.** Run `git ls-files | grep -E '_[A-Z]+'` filtered to `docs/` and `src/`. Flag any UPPERCASE-with-underscore patterns. Exempt categories: ADR-prefixed files (grandfathered), historical transcripts (preserved pre-decision), `council_inbox/archive/` ISO timestamp data files. Verify: no unexpected matches in scope-applicable directories; document any drift for follow-up.

6. **Push to `origin` (operator timing decision).** Approximately 74 commits ahead at handoff (architect inference; verify via `git rev-list --count origin/main..main`). Backup risk grows with each session. Verify: `git push origin main`; ahead count drops to zero.

### 5. BOUNDARIES

This section assumes zero prior session knowledge.

**Do NOT:**

- Force a synthesizer model flip based on Council debate alone — empirical scoring data via Directive 1 is required. Council recommendation contained a cost-blind spot which the cost-optimization principle (see RATIONALE) addresses.
- Codify any cross-repo handshake protocol requiring more than one round trip — the operative principle is that well-formed cross-repo requests close in one round trip; multi-turn signals badly framed request.
- Defend "local config" or "by-design per CLAUDE.md" as justification when a convention divergence is flagged by audit, operator, or cross-repo reviewer — default response must be "evaluate against ecosystem baseline."
- Modify `routing.py`, CLI configuration loading, or cross-repo routing logic — that work shipped recently and is stable; next session is governance plus cost-optimization codification.
- Implement a cross-repo audit tool from ai-council — that is a `.dev-knowledge` concern.
- Make changes to `.dev-knowledge` files from within an ai-council session — ADR-36 read-only contract forbids it. Operator hand-carries cross-repo artifacts if needed.
- Start corp-monorepo Phase 2 work from this session — that is a separate visit after ai-council gaps are closed.
- Generate reconciliation reports about other repos' BACKLOG or tracking-file state. Do NOT treat staleness observations about another repo's tracking as an action item for this session — per ADR-41, each repo manages its own BACKLOG; cross-repo work flows via operator-carried routing artifacts.
- Codify the scrum-master review authority pattern into a formal ADR yet — empirical grounding is N=1; await N=2 (second instance, ideally on a different repo) before codification.
- Recreate `docs/HANDOFF.md` — already deleted in prior work; handoffs live in `docs/handoffs/` per ADR-42.
- Fabricate AGENTS.md governance rules if specifics are unclear — mark Unknown sections; operator confirms.
- Add timeline qualifiers to recommendations or directives ("this week," "next session," "end of day," "heavy-work window").
- Pre-emptively flag context degradation based on message count alone rather than measurable quality issues.
- Skip Codex `/review` on PRs touching three or more files (PLAYBOOK section 15).
- Use UPPERCASE letters in new filenames — ADR-34 mandates lowercase plus hyphens (ADR prefix grandfathered). One fresh violation occurred recently and was caught and renamed; the convention is empirically easy to slip on.
- Combine ADR amendment work with feature shipping in the same Claude Code prompt without clear section separation — governance changes deserve their own commits for audit-trail clarity.
- Push to `origin` without explicit operator authorization.

**Fallback contingencies:**

- If Directive 1 scoring is inconclusive (pass rate near 80% threshold, or quality scores ambiguous across criteria): expand sample size (30 transcripts instead of 15) before escalating to higher-cost tier testing.
- If Codex `/review` surfaces a blocker requiring `.dev-knowledge` input mid-implementation: opens a new cross-repo conversation (one round trip principle applies); not a continuation of routine PR completion.
- If new feature work surfaces ADR drift mid-PR: invoke ADR audit step inline; architect judgment call on whether to update affected ADRs in the same PR or capture as BACKLOG follow-up.
- If operator declares scope creep mid-session: stop, summarize completed work, propose handoff or scope contraction. Do not deepen ceremony as response to scope concerns.
- If AGENTS.md template at `.dev-knowledge/templates/AGENTS-md-template.md` is inaccessible to ai-council session: operator hand-carries template content as artifact; do not fabricate substitute structure.
