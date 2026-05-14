# State of Play — ai-council (session-sync, 2026-05-14)

<!-- scope: meta -->

Current state and architect judgment for the ai-council session ending 2026-05-14.
Derived from Stage 2 architect response (REALITY + RATIONALE sections).

---

## Current state

- HEAD: `0f069554b894802504aa4e5ce140b1d481ae9ec8`
- Branch: `main`
- Working tree: clean
- Test count: approximately 362 (architect inference — verify via `pytest --collect-only -q`)
- Commits ahead of `origin/main`: approximately 74 (architect inference — verify via `git rev-list --count origin/main..main`)

---

## What was completed this session

The following work was witnessed by the architect in the current session, traceable
in git log preceding HEAD `0f06955`:

1. **VISION.md created at Scale M tier** — configured `DEV_KNOWLEDGE_PATH` reference in `CLAUDE.md` per ADR-35 [ecosystem lessons discovery].

2. **Cross-project transcript routing shipped** — `target-project` frontmatter field and `--target-project` Click flag on the CLI; `dev_root` and `target_projects` list schema in `config/settings.yaml`; `TargetResolver` in `src/ai_council/routing.py` with fail-loud behavior on unknown target names at parse time.

3. **ADR-43 schema refactor** — changed `target_projects` from `dict[name, full_path]` to `dev_root: str + target_projects: list[str]` with paths computed from prefix.

4. **Post-routing cleanup** — `secondary_output_enabled` default flipped to `false`; code path retained for explicit opt-in.

5. **Docs hygiene sweep** — deleted `docs/HANDOFF.md` flat file (handoffs are .dev-knowledge domain per ADR-42 [handoff format v3]); consolidated `docs/archive/` content into `docs/audits/`.

6. **ADR governance sweep (ADR-01 through ADR-07)** — status date corrections, factual drift fixes (e.g., ADR-02 default panel 3-model → 5-model), ADR-06 Qwen trial deferred with reopen trigger documented, ADR-07 superseded by ADR-43.

7. **Synthesizer/panel refresh Council debate** — unanimous Option B (synthesizer-only refresh, panel unchanged, gated on smoke test); transcript routed to `.dev-knowledge` via the new routing feature.

8. **ADR-34 [file naming convention] universal hyphen mandate applied** — CLI emitter changed from `council_out_*` to `council-out-*`; downstream patterns and tests updated; cross-repo cycle closed on merge.

9. **Combined merge: per-synthesis observability + ADR-34 hyphen + ADR-06 closure** — observability metrics added (latency, transcript size, output tokens, error class); `docs/synthesis-quality-rubric.md` created (5-point operator-applicable checklist); Gemini synthesizer version diagnostic performed.

10. **Scrum-master review (N=1)** — nine of ten findings implemented: retired `tasks/todo.md`; created `BACKLOG.md` per ADR-41 [cross-session backlog]; updated README; fixed ADR-34 filename violations including `SYNTHESIS-QUALITY-RUBRIC.md` → `synthesis-quality-rubric.md`; archived legacy `_CODE_REVIEW_REPORT.md` to `docs/audits/archive/legacy/`.

11. **Scrum-master review addendum** — moved `tasks/lessons.md` to root `LESSONS.md`; retired `tasks/` folder; renamed `docs/handoffs/_archive/` to `docs/handoffs/archive/`.

12. **Most recent commit (`9de640e`)** — captured a P3 [low-priority] BACKLOG item for ADR-34 edge case: `council-out-YYYYMMDD_HHMMSS-topic.md` filenames retain an underscore between date and time in the timestamp, which is a strict ADR-34 violation. Deferred to P3 because changing timestamp format would break sort-order assumptions and parsing (architect inference on rationale; verify against commit message and BACKLOG entry).

**Work in progress:** none witnessed.

**docs/HANDOFF.md state:** deleted in docs hygiene sweep (Step 5 above). The
`.dev-knowledge` BACKLOG references to this file reflect stale state; the file is
absent in the current repo. This is awareness only — each repo manages its own
BACKLOG per ADR-41.

---

## Decisions locked this session

**Synthesizer refresh gated on scoring data.** The Council debate produced
unanimous Option B (refresh synthesizer only; panel unchanged). Option A (no
change) ignored evidence of model landscape shift. Option C (panel + synthesizer
refresh) introduced too many variables. The gate: smoke-test/scoring data required
before any default flip. Council recommendation contained a cost-blind spot
(Opus 4.7 recommended without cost-benefit framing); the operator caught the gap.
The corrected approach — test current default first, escalate in cost order only
if quality fails — is captured in `LESSONS.md` as the cost-optimization principle.
Codification into ADR-01 amendment is gated on scoring data from this session.

**Cross-repo handshake protocol: one round trip.** An earlier 4-turn protocol
(proposal → approval → closure note → delivery report) was retired as
over-engineered for S-scale changes. The operative principle: well-formed
cross-repo requests close in one round trip; needing more rounds signals a
badly-framed request. Two cycles closed cleanly under this principle.

**Scrum-master review pattern (N=1).** The `.dev-knowledge` strażnik [guardian]
produced a unilateral audit of ai-council; architect implemented nine of ten
findings. The pattern worked at N=1. Codification into a formal ADR awaits N=2
(second instance, ideally on a different repo).

**Combined-merge approach validated.** Two independent workstreams (observability
+ ADR-34 hyphen) were combined in a single Claude Code prompt; Codex `/review`
passed clean. Trade-off: audit-trail granularity vs ceremony cost. Worth repeating
for similar future cases.

**Boundary-blur failure pattern codified.** Three manifestations of the same
pattern surfaced during this session: defending local repo config as "by-design"
when convention divergence was flagged; accepting a similar defense from another
source; generating a cross-boundary directive in an earlier handoff. All three
captured in `LESSONS.md`. The structural fix is the Universal Self-Containment
Rule in HANDOFF_PROCESS. Default response when convention divergence is flagged:
"evaluate against ecosystem baseline," not "intentional per local config."

---

## Rationale (architect judgment)

- **Synthesizer scoring before ADR-01 amendment:** empirical data required before
  governance codification. The Council recommendation had a cost-blind spot; the
  principle correction exists in `LESSONS.md` but is not ADR until data confirms it.

- **AGENTS.md low urgency:** the `.dev-knowledge` framing was "low urgency; include
  in future maintenance cycle." The `templates/AGENTS-md-template.md` is the intended
  scaffold. Mark Unknown sections explicitly; do not fabricate governance rules.

- **ARCHITECTURE.md optional at Scale M:** the `CLAUDE.md` Architecture section
  provides equivalent coverage. Only warranted if scale escalates to L.

- **Push to `origin` backup risk:** approximately 74 commits ahead (architect
  inference). Risk grows with each session. No functional blocker.

---

## Deferred items (BACKLOG references)

The following items remain open in `.dev-knowledge/BACKLOG.md`. See that file for
full details; not duplicated here.

- **[P2][open] Stream B — ai-council needs AGENTS.md** (cross-tool LLM governance)
- **[P2][open] Cross-stream — Phase 2 universalization rollout** (ai-council remaining: AGENTS.md P3, ARCHITECTURE.md optional)
- **[P2][open] Cross-stream — Handoff folder format adoption** (A4 decision needed)
- **[P3][open] Cross-stream — docs/HANDOFF.md flat file deprecation** (tied to A4)
- **[P2][open] Cross-stream — ai-council hyphen migration + ADR-38 compliance**
- **[P3][open] Cross-stream — A5: retire UPPERCASE TYPE tag in legacy archive filenames** (opportunistic)
- **[P3][open] Cross-stream — ADR-34 timestamp-underscore in council-out emitter**

---

## Stage 3 verification summary

Architect provided witnessed claims that were checked against repo state:

- **Verified (8):**
  - `docs/HANDOFF.md` deleted — absent from `git ls-files` ✓
  - `docs/synthesis-quality-rubric.md` present — in `git ls-files` ✓
  - `src/ai_council/routing.py` present — in `git ls-files` ✓
  - `BACKLOG.md` at root — in `git ls-files` ✓
  - `LESSONS.md` at root — in `git ls-files` ✓
  - `tasks/` folder absent — not in `git ls-files` ✓
  - `docs/handoffs/archive/` (not `_archive/`) — archive files present ✓
  - `docs/decisions/ADR-06-cost-optimization.md` present — in `git ls-files` ✓

- **Unverifiable from repo (6):** Council debate content and outcome (conversation history); cost-optimization correction sequence (conversation history); 4-turn → 1-round-trip simplification decision (conversation history); scrum-master review pattern N=1 implementation details (conversation history); boundary-blur failure pattern instances (conversation history); combined-merge decision rationale (conversation history).

- **Architect-flagged inferences (4):** test count ~362; commits ahead of origin/main ~74; ADR-34 timestamp P3 deferral rationale; AGENTS.md scope/content decisions. All preserved with "(architect inference)" markers.

- **Architect-flagged unknowns (0):** none.
