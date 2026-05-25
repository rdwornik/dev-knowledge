# ADR-45 — Handoff Architecture v4: Invariant/Session Separation + Defense-in-Depth Enforcement

<!-- scope: meta -->

Status: Explored, not adopted; ADR-42 v3.2 remains canonical authority for handoff architecture
Date: 2026-05-13
Supersedes: ~~ADR-42 (Handoff Format v3, amended through v3.2)~~ — claim WITHDRAWN 2026-05-25 (see Amendment at end); ADR-45 was explored, not adopted; ADR-42 v3.2 remains canonical authority
Related: ADR-29 (LESSONS.md grandfathering / append-only format),
         ADR-34 (file naming convention),
         ADR-37 (session boundary protocol — preserved as overlay),
         ADR-40 (scale tier evaluation — provides the per-project tier
                 marker used in MANIFEST.md),
         ADR-41 (cross-session backlog architecture — BACKLOG remains the
                 canonical pending queue),
         transcripts council-out-20260513_102702-research-question-*,
         council-out-20260513_111424-pick-council-handoff-architecture-pick,
         audit docs/audits/2026-05-12-handoff-process-audit.md

## Context

**Note 2026-05-13 night:** v1 of this ADR over-concluded toward bundle
replacement (12 → 2 files + drop full invariants). Side-by-side reading
against ADR-42 v3.2 + 2026-05-12 audit revealed conflicts with audit's
"what works, preserve" findings — full invariants prevent norm drift per
SECI rationale, 11-file bundle empirically catches real architect
fabrications (2026-05-09 ai-council Grok timeout-vs-model-string case).
Minimum-viable refinement implemented instead (HANDOFF_PROCESS v3.3 —
template language fixes per audit, mandatory articulation gate in
00_first-message). Sequential loading, question battery, and ADR-45 v2
full rewrite remain deferred — implement only if minimum doesn't address
empirical drift in next handoff cycle.

ADR-42 v3.2 is the current handoff authority. It prescribes a three-stage
relay (Claude Code generates a question prompt; the OLD browser chat
answers from lived knowledge; Claude Code reconciles and emits the
bundle), an optional Stage 2.5 Q&A loop, and an 11-file flat folder
delivered to the NEW browser chat. The bundle includes full copies of
VISION, PLAYBOOK, and ESSENTIALS as invariants, plus a five-section
SBAR/I-PASS-shaped response template (OBJECTIVE / REALITY / RATIONALE /
DIRECTIVES / BOUNDARIES) carried into `06_STATE_OF_PLAY.md` and
`07_ACTION_PLAN.md`. SHA-256 manifest checksums plus a HEAD-pin guard
the bundle against drift.

The 2026-05-12 audit (`docs/audits/2026-05-12-handoff-process-audit.md`)
read the protocol, the templates, the slash command, and four real
handoff artifacts end-to-end. It surfaced three problems that are
structural, not template polish:

- The 11-file bundle is dense with decoder-required language (priority
  codes plus finding codes plus ADR numbers compressed into single
  bullets; long undifferentiated DO-NOT lists; SBAR section names with
  no plain-language gloss). A reader without the protocol in head sees
  status flags rather than prose.
- Roughly 60% of bundle size is full verbatim copies of invariants
  (VISION + PLAYBOOK + ESSENTIALS) that do not change between handoffs
  but ride along every time. This bloats the upload and dilutes the
  per-handoff signal.
- The five-section vocabulary leaves a register on downstream artifacts.
  Once OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES are the
  Stage 2 input shape, the generated `06_STATE_OF_PLAY` and
  `07_ACTION_PLAN` inherit form-like enumeration where prose would carry
  the meaning more directly.

Two AI Council debates on 2026-05-13 examined the problem from
different angles and converged. The research debate
(`council-out-20260513_102702-research-question-how-do-llm-agent-ecosystems-with-isolated.md`)
asked how 2026 LLM-agent ecosystems with isolated repos and shared
governance documents actually handle invariant-vs-session separation
in practice; it surfaced empirical adherence numbers from real
deployments — implicit memory plus CLAUDE.md alone yields roughly 40%
convention adherence; SBAR-shaped templates yield around 85% adherence
but with about 60% bundle bloat; hybrid layered architectures
(canonical-source + machine validators + minimal session payload)
hit 96–99% adherence at a fraction of the size. The pick debate
(`council-out-20260513_111424-pick-council-handoff-architecture-pick.md`)
forced a concrete five-question architectural choice across three
panel models, with the synthesizer landing on a single composite.

The single strongest argument across both debates: the browser
architect cannot dereference filesystem pointers. Whatever the handoff
sends has to be self-contained at the browser side, because a "see
@.dev-knowledge/PLAYBOOK.md" pointer is unreadable in claude.ai.
Anything the architect needs to read has to either be uploaded
explicitly at session start or be inlined into the handoff payload —
there is no third option. This is the constraint that ruled out
several otherwise-attractive purely-pointer-based designs.

The convergence direction across both debates is the same shape:

- Move discipline enforcement out of the prompt and into the harness
  (an "institutional AI" reframe — the rules live where they can be
  mechanically checked, not where the model is asked to remember them).
- Separate invariants (governance documents that change rarely) from
  session state (the per-handoff payload that changes every time).
  Keep invariants canonical in one place and let them reach consumers
  through stable mechanisms; keep session state thin.
- Make the handoff payload small enough to be read end-to-end without a
  decoder, and self-contained enough that the browser architect needs
  no resolved pointers to act on it.

## Decision

### Foundational principle 1 — Invariants and session state are different things and live in different places

Invariants are the documents that govern *how* this ecosystem works:
PLAYBOOK, ESSENTIALS, AGENTS, the scale-tier definitions from ADR-40,
the file naming convention from ADR-34, and any other document whose
content is the same across two consecutive handoffs.

Invariants live canonically in `.dev-knowledge`. They reach the
executor (Claude Code in any repo) via Claude Code's `@path` import
mechanism in `CLAUDE.md` or `AGENTS.md`, with a sync-script CI verifier
running in parallel as a guardrail in case the import mechanism breaks
or drifts. They reach the browser-chat architect either through
operator-mediated upload at session start (paste / drag-drop a small
fixed bundle) or through claude.ai Project Instructions configured
once per project.

Session state is the per-handoff payload: what was just done, what the
current pinned state is, what the next session should do, and which
hard constraints apply. This is the only thing the handoff carries —
no governance copies, no methodology recap, no full ADR text.

### Foundational principle 2 — Discipline enforcement lives in the harness, not in the prompt

Every behavior the handoff currently asks the model to remember
(update JOURNAL, update CHANGELOG, groom BACKLOG, capture lessons,
verify HEAD-SHA before acting) becomes a mechanical check that the
harness runs. The model can still forget; the harness will not let
the session close in a forgotten state.

The architecture is defense-in-depth — three independent enforcement
points, all calling the same shared validator script so the rules live
in one place:

- A git pre-commit hook (installed via `core.hooksPath` from
  `.dev-knowledge`) refuses commits that leave session bookkeeping
  stale.
- A Claude Code PreToolUse hook (exit code 2) refuses Write/Edit
  operations that bypass conventions (for example, writing source
  without a JOURNAL entry staged for that session).
- The `/save` slash command runs the same validator before emitting
  any handoff and refuses to produce a bundle whose checksums or
  required files are missing.

All three call one shared validator at `.dev-knowledge/scripts/validator.py`.
The validator is the source of truth for which mechanical checks must
pass; the three hooks are thin shims that invoke it.

### Per-question commitments from the Council pick debate

These are the concrete answers the pick debate locked in. They
implement the two foundational principles above.

**Q1 (where do conventions live):** `.dev-knowledge` is the canonical
home. Each child repo's `CLAUDE.md`/`AGENTS.md` references the
canonical files via Claude Code `@path` imports rather than copying
content. A sync-script CI verifier runs in parallel as a guardrail —
if `@path` imports break or drift in a future Claude Code version, the
sync script can be promoted from guardrail to primary mechanism without
changing other answers.

**Q2 (what does the handoff payload look like):** Two files only.

- `MANIFEST.md` — the machine layer of the handoff. HEAD SHA per repo
  involved, SHA-256 over the bundle, model and tool version pins, and
  the scale-tier marker (per ADR-40) for the target project so the
  architect knows which tier's obligations apply.
- `NEXT.md` — the human layer of the handoff. Around 50 lines of
  plain prose in four labelled blocks: *Built* (what shipped this
  session), *Current State* (where the repo actually is now, with the
  pinned HEAD), *Next Action* (the single next thing to do), *Hard
  Constraints* (the small handful of DO-NOTs that are critical for
  the next step). No SBAR vocabulary; no RATIONALE section; the
  reader gets the state in plain English without a decoder.

**Q3 (who custodies session state across browser chats):** The
executor — Claude Code — is the state custodian. Claude Code already
maintains per-project session storage in `~/.claude/projects/` and an
auto-memory layer; the handoff design leans on that rather than
inventing a new MCP server. The operator's job is to paste the minimal
two-file payload into the new browser session so the architect sees
the same state Claude Code sees.

**Q4 (how is discipline enforced):** Defense-in-depth as described in
foundational principle 2 — git pre-commit hook plus Claude Code
PreToolUse hook plus `/save` slash command, all calling one shared
validator script. Three failure-independent gates. Any one of them is
enough to catch a missed bookkeeping step.

**Q5 (how do we migrate):** Pilot first, fleet second. A throwaway
repo gets a bootstrap dry-run to shake out the validator and templates.
Then `.dev-knowledge` itself runs the new architecture for two weeks
as the pilot. A gate check at the end of the pilot decides whether to
roll out: target is at least 95% convention adherence in the validator,
average handoff size at or below 1500 tokens, and zero missed-checksum
incidents in the last five consecutive sessions. If the gate passes,
the architecture rolls out to the rest of the ecosystem one repo at
a time with a one-week soak per repo: ai-council, then corp-monorepo,
then corp-ops, then corp-sca-time-automation. If the gate fails,
ADR-42 v3.2 remains the baseline and the design re-enters debate.

### Browser-chat architect compliance path

The browser architect (claude.ai) is the only consumer that cannot
read the filesystem. Compliance for the architect comes from three
places:

- The operator uploads `ESSENTIALS.md` at session start, or persists
  it via claude.ai Project Instructions so it loads automatically per
  project.
- `MANIFEST.md` carries the scale-tier marker (per ADR-40) and the
  HEAD SHA so the architect's directives are framed in the right
  tier-specific obligations and pinned to a known repo state.
- The architect generates prompts; those prompts hit Claude Code,
  which is governed by the harness — so any architect output that
  violates conventions gets caught at execution time even if the
  architect itself drifted.

The architect is responsible for following the uploaded conventions.
Enforcement is operator review at the architect-output stage plus the
Claude Code harness at the execution stage. There is no architect-side
hook to install.

### What ADR-45 preserves from ADR-42

The structural decisions ADR-42 got right are kept verbatim:

- The three-stage relay structure plus Stage 4 receiver synthesis.
  Stage 1 captures session state, Stage 2 extracts tacit knowledge
  from the OLD chat, Stage 3 reconciles against the repo and emits
  the payload, Stage 4 is the NEW chat reading the payload before
  acting. The roles are unchanged; only what flows between them
  changes.
- HEAD-pin plus SHA-256 manifest checksums. The 2026-05-09 ai-council
  case has a worked example of this catching a real fabrication
  (architect described a Grok timeout change that the actual diff
  showed was a model-string change). Drift detection is non-negotiable
  and survives the restructure unchanged.
- Stage 3's verification of architect claims against the repo, with
  results made visible (verified vs failed vs unverifiable vs
  inference-flagged). The witnessed/inference/unknown contract with
  the architect is the input to this verification step and is also
  preserved.
- Per-handoff archival. Every handoff still produces an artifact under
  `docs/handoffs/{date}-{slug}/`; the difference is what the artifact
  contains.

### What ADR-45 removes from ADR-42

The structural decisions ADR-42 got wrong are dropped:

- The 11-file bundle format. Replaced by the two-file MANIFEST + NEXT
  payload.
- Full verbatim copies of VISION, PLAYBOOK, and ESSENTIALS in every
  bundle. Invariants reach consumers through `@path` imports plus the
  sync-script verifier (executor) and through operator-side upload or
  Project Instructions (architect).
- The SBAR/I-PASS five-section vocabulary at output level (OBJECTIVE /
  REALITY / RATIONALE / DIRECTIVES / BOUNDARIES). Replaced by the
  four plain-prose blocks in NEXT.md (Built / Current State / Next
  Action / Hard Constraints).
- The unbounded BOUNDARIES section. Replaced by a small fixed
  Hard Constraints block that lists only the DO-NOTs critical for the
  next step, not the full pile.
- The RATIONALE section. The reasoning behind a decision belongs in
  ADRs (architectural), JOURNAL (session-tactical), or LESSONS
  (methodology corrections), not in every handoff. Repeating it per
  handoff duplicates content and adds bloat without adding signal.

## Consequences

### Positive

- Roughly 87% reduction in handoff payload size (the audit-grounded
  estimate is from about 12,000 tokens per ADR-42 v3.2 bundle to
  about 800–1500 tokens per ADR-45 MANIFEST + NEXT pair).
- Convention adherence target of 96–99% (Council research empirical
  range for hybrid layered architectures), versus ~85% under ADR-42.
- Mechanical convention enforcement through three independent gates;
  the model is no longer the only thing remembering to update JOURNAL.
- Cross-repo consistency physically guaranteed by the canonical-source
  plus `@path` import architecture, rather than maintained by hand
  across five repos.
- The bundle is readable end-to-end without a protocol decoder. Status
  codes, finding codes, and SBAR labels are out; plain prose is in.

### Negative

- Migration cost. The new architecture needs a shared validator script,
  three enforcement hooks, a sync-script for `@path` fallback, and the
  two-file payload templates. Estimate is one to two weeks of
  engineering before the pilot can start.
- Three enforcement layers means three places to update when the rule
  set changes. Mitigated by keeping all rules in the shared validator;
  the hooks themselves are thin shims.
- The `@path` import mechanism is a Claude Code feature; if its
  semantics change in a future version, the executor-side invariant
  delivery breaks. Mitigated by the sync-script guardrail running in
  parallel — if the import path fails, sync-script is promoted to
  primary without other architectural changes.

### Fallback modes

- If `@path` imports break or drift, the sync-script becomes the
  primary mechanism for invariant delivery to executor repos. No
  other answer changes.
- If the Claude Code PreToolUse hook becomes unreliable, the
  enforcement triple drops to a duo (pre-commit plus `/save`); pre-commit
  is the strongest single gate because it sits at the irreversibility
  boundary.
- If a particular handoff's payload genuinely cannot fit in 1500
  tokens, the priority rules in the NEXT.md template trim from the
  bottom (Hard Constraints first by criticality, then Next Action
  scope, then Current State detail; Built is always first to compress
  if needed).
- If the pilot fails its gate check, ADR-42 v3.2 remains the baseline
  and ADR-45 returns to debate. The rollback is a documentation
  revert plus removing the new hooks; no data is destroyed because
  invariants stayed canonical in `.dev-knowledge` throughout.

## Success metrics (tracked during pilot)

- Average handoff payload size (tokens) per transfer.
- Convention adherence rate (per-session JOURNAL, CHANGELOG, BACKLOG,
  LESSONS completion measured by the validator).
- False-block rate (hook errors that turned out not to be actual
  violations). High false-block rate signals the validator needs
  tuning, not that the architecture is wrong.
- Extra clarification requests per handoff (NEW chat asking the
  operator to relay questions back). High rate signals NEXT.md is
  insufficient and the template needs more block structure.
- Checksum and drift incident count. Must remain at zero — any
  non-zero count is a regression on what ADR-42 already gave us.

## Migration plan

The plan deliberately does not include implementation specifics
(validator-script structure, exact hook syntax, MANIFEST schema field
list). Those belong in follow-up implementation prompts so they can be
debated on their own merits.

1. Implement the shared validator script at
   `.dev-knowledge/scripts/validator.py`. This is the foundation; the
   hooks are thin around it.
2. Define the MANIFEST.md and NEXT.md schemas; ship templates under
   `.dev-knowledge/templates/`.
3. Define the session-boundary semantics — what mechanically counts
   as "JOURNAL was updated this session" so the validator can decide.
4. Implement the three enforcement hooks (git pre-commit, Claude Code
   PreToolUse, `/save` slash command) calling the shared validator.
5. Implement the sync-script for `@path` fallback so the guardrail is
   in place from day one.
6. Bootstrap dry-run on a throwaway repo to shake out the templates
   and the validator before any production repo is exposed.
7. Pilot on `.dev-knowledge` for two weeks under the new architecture.
8. Gate check at end of pilot: ≥95% adherence, ≤1500 token average
   handoff, zero missed-checksum incidents over five consecutive
   sessions.
9. Rollout: ai-council → corp-monorepo → corp-ops →
   corp-sca-time-automation, one at a time, with a one-week soak per
   repo before moving to the next.

## References

- ADR-29 — LESSONS.md format and grandfathering
- ADR-34 — file naming convention
- ADR-37 — session boundary protocol (Current State / Future State
  framing preserved as the conceptual overlay; the new payload's
  Current State and Next Action blocks are how that framing manifests
  under v4)
- ADR-40 — scale tier evaluation algorithm (provides the per-project
  tier marker that MANIFEST.md carries)
- ADR-41 — cross-session backlog architecture (BACKLOG.md remains the
  canonical pending queue; NEXT.md does not duplicate it)
- ADR-42 — handoff format v3 (ADR-45 was never accepted; supersession claim
  withdrawn 2026-05-25 — ADR-42 v3.2 remains canonical, see Amendment at end)
- `docs/audits/2026-05-12-handoff-process-audit.md` — empirical audit
  of ADR-42 v3.2 in practice
- `docs/decisions/transcripts/council-out-20260513_102702-research-question-how-do-llm-agent-ecosystems-with-isolated.md`
  — Council research debate on invariant/session separation patterns
  in 2026 LLM-agent ecosystems
- `docs/decisions/transcripts/council-out-20260513_111424-pick-council-handoff-architecture-pick.md`
  — Council pick debate selecting the five architectural commitments
  (Q1 through Q5) above

## Amendment 2026-05-25 — Supersession claim formally withdrawn (resolves audit M-2)

**Trigger.** 2026-05-20 handoff-process audit, finding M-2
(`docs/audits/2026-05-20-handoff-process.md` §7). A reader scanning ADR headers
sees `Supersedes: ADR-42` and infers ADR-45 is canonical, while the Status line
(clarified earlier in commit `abb76a7`) says the opposite. That header inversion
is the documented read-order trap.

**Decision.** The `Supersedes: ADR-42` claim in the header — and the matching
"superseded by this ADR once accepted" note in References — is formally
**withdrawn**. ADR-45 supersedes nothing. It stands as a frozen design
exploration ("v4": invariant/session separation + defense-in-depth enforcement)
that was explored on 2026-05-13 and **not adopted**. The same-night
minimum-viable refinement (HANDOFF_PROCESS v3.3, since advanced to v3.3.3) was
implemented instead, preserving the 11-file bundle and full invariants per the
2026-05-12 audit's "what works, preserve" findings (see the Context note
2026-05-13 night).

**Authority.** `docs/decisions/ADR-42-handoff-format-v3.md` (v3, amended through
v3.2) plus `protocols/HANDOFF_PROCESS.md` (v3.3.3) remain the canonical handoff
architecture. This amendment changes no decision content; it reconciles the
header metadata with the already-clarified Status line so the ADR index no
longer mis-signals supersession.
