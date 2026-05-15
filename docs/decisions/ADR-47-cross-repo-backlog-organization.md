# ADR-47 — Cross-repo BACKLOG.md organization

<!-- scope: meta -->

Status: Accepted
Date: 2026-05-15
Stream: C, governance ADR session B+C
Supersedes: aspirational "consistent BACKLOG organization" implied by
            ADR-41 (mandate without schema)
Superseded by: none
Related: ADR-27 (scope tagging — HTML comments authoritative),
         ADR-33 (VISION universalization),
         ADR-37 (session boundary protocol — handoff anchor),
         ADR-38 (universal repo architecture, mandatory files per tier),
         ADR-39 (file lifecycle governance),
         ADR-41 (BACKLOG architecture — file mandate this ADR refines),
         ADR-46 (cross-repo dated-entries format, paired decision),
         transcripts council-out-20260515_185730-research-...md,
                      council-out-20260515_194305-pick-...md

## Context

ADR-41 mandates `BACKLOG.md` at tier M+ for every ecosystem repo but
does not specify organisation. Result: each repo drifted ad-hoc.
Observed drift in `.dev-knowledge` and across the ecosystem:

- `[done]` entries mixed with `[open]` in same sections, no archiving
  policy
- Files growing without pruning rhythm (`.dev-knowledge` BACKLOG.md
  ~350 lines, ~45 entries, ~half are `[done]` inline)
- No consistent ordering within sections — priority / date-added /
  stream varies
- Cross-repo: each repo's BACKLOG is structured differently

BACKLOG is the primary cross-session handoff anchor (ADR-37). Done
items inline cause LLM context dilution ("lost-in-the-middle"
attention degradation): when the agent loads BACKLOG.md at session
start to recover state, coherent done items are plausible-seeming
distractors that mislead attention away from open items.

Council research (transcript `council-out-20260515_185730-...`)
recommended a two-file state architecture (BACKLOG.md +
BACKLOG_ARCHIVE.md), Now/Next/Later sections, scope-tag pattern, and
session-end auto-prune. Council pick (transcript
`council-out-20260515_194305-...`) selected **Option C-2
(Stream-grouped + Two-file state)** under simple-majority rule, with
operational hardening from Round 2 critique (validator at session
start, not end; deterministic script not LLM prompt).

The panel explicitly weighed Lesson #1 (documentation-conflation) via
"asymmetric validation":

> The stream structure and fielded entries have been actively used as
> handoff anchors (validated), whereas inline `[done]` tags have
> merely survived without scrutiny (unvalidated).

## Decision

Adopt **Stream-grouped BACKLOG with a two-file state architecture**
for all ecosystem repos at tier M+ that have a BACKLOG.md per
ADR-41.

### Structure

#### Active file: `BACKLOG.md`

- Contains **only `[open]` and `[superseded]` items.**
- `[done]` items are extracted to `BACKLOG_ARCHIVE.md` (see below).
- Top-level structure: `## Stream A: <name>`, `## Stream B: <name>`,
  ..., `## Cross-stream / Ecosystem`.
- Stream names are **per-repo flexible** (no fixed cross-repo
  vocabulary). `.dev-knowledge` uses repo-named streams
  (A=corp-monorepo, B=ai-council, C=.dev-knowledge governance,
  D=corp-sca-time-automation) plus Cross-stream / Ecosystem.

#### Archive file: `BACKLOG_ARCHIVE.md`

- Append-only. **`[done]` and `[abandoned]` items only.**
- Top-level structure mirrors `BACKLOG.md`: same Stream headings.
- Within each Stream, **reverse-chronological by close date** (newest
  archived item at the top of its stream section, per ADR-46
  prepend-latest mandate).
- Each archived entry preserves its original entry block verbatim
  plus a `**Archived:** YYYY-MM-DD` line.

### Entry format (universal)

```
### [P{N}] [open] <title>
- **What:** <one paragraph>
- **Why:** <one paragraph>
- **Vision ref:** <VISION.md section or ADR-NN reference>
- **Added:** YYYY-MM-DD by <author> (<context>)
- **Status:** open
```

Required fields: `What`, `Why`, `Added`, `Status`.
Recommended fields: `Vision ref` (omit only for purely operational
items with no governance bearing), other context-specific fields
(`Note:`, `Stage 1 inputs:`, etc.) permitted as additional bullets.

When archived, the entry is moved verbatim and the `Status:` line is
updated:

```
### [P{N}] [done] <title>
- **What:** <unchanged>
- ...
- **Status:** done (YYYY-MM-DD — <closure note>)
- **Archived:** YYYY-MM-DD
```

### Priority semantics

P1/P2/P3 retained as the cross-repo priority vocabulary:

- **P1** — active priority. Currently being worked or queued for the
  next session. Generally fewer than 5 per stream.
- **P2** — queued. Not yet picked up; sequenced behind P1 items in
  the same stream.
- **P3** — someday / opportunistic. May never close; revisited at
  quarterly grooming.

P0 reserved for emergencies (e.g., security or correctness blocker
in production). Use sparingly.

### Status tags

`[open]`, `[done]`, `[superseded]`, `[abandoned]`. `[superseded]`
items may remain in `BACKLOG.md` (active file) until quarterly
grooming, since they carry context about why the item was replaced.
`[abandoned]` items move to archive immediately on next session-start
cleanup.

### Pruning rhythm

- **Session start** (validator gate, per operational hardening):
  fail-fast if `[done]` items exist in `BACKLOG.md`. Operator runs the
  extraction script to clear before starting new work.
- **Per-handoff lightweight grooming:** review whether any items
  should be reprioritized; close any obviously-stale `[done]` items.
- **Quarterly deep grooming:** move `[superseded]` items to archive;
  reassess P3 items.

### Scope vocabulary

This ADR does **not** mandate inline scope tags within entries (the
research's `<!-- SCOPE_SCHEMA: -->` pattern is **not adopted**).
Stream sections already carry the scope-of-work signal; an additional
tag layer adds ceremony without payoff at current scale.

Per-repo decision: a repo MAY add `<!-- SCOPE_SCHEMA: -->` declaration
if it operates in a more swarm-of-agents mode and benefits from
deterministic routing. Not required.

### Kill criteria (when to revisit this ADR)

This ADR triggers automatic review and likely migration to a
Now/Next/Later or hybrid scheme (C-3 or C-4) if **any** of the
following hold for any repo's `BACKLOG.md`:

- Active file exceeds **300 lines**.
- Any single stream section exceeds **15 open items**.
- `Cross-stream / Ecosystem` section exceeds **33%** of total open
  items.

Audit tool (Session E) MUST emit a WARN finding on each trigger; ADR
review is operator-initiated.

### Enforcement (Session E scope)

Deterministic Python validator at session start (or pre-commit) MUST:

1. **Fatal:** the literal token `[done]` appears in `BACKLOG.md`
   outside of fenced code blocks and HTML comments.
2. **Fatal:** `BACKLOG_ARCHIVE.md` is missing when `BACKLOG.md` is
   present.
3. **Fatal:** any entry heading does not match the required `### [P{N}]
   [open|superseded] <title>` regex.
4. **Fatal:** any entry block lacks the required fields
   (`What`, `Why`, `Added`, `Status`).
5. **Warn:** kill-criteria triggers (300 lines / 15-per-stream / 33%
   Cross-stream).
6. **Warn:** `[done]` items in `BACKLOG.md` at session start —
   indicates Session D extraction failed and must be re-run manually.

### Extraction script (Session D scope)

A deterministic Python script (target < 50 LOC) MUST handle done-item
extraction. **No LLM prompt is permitted for this operation** — the
panel's operational hardening explicitly rejected reliance on LLM
agents for end-of-session housekeeping.

Script behavior:
1. Read `BACKLOG.md` line-by-line.
2. Detect entry blocks matching `### [P{N}] [done] <title>`.
3. Capture the entry block (heading + indented bullets) until next
   `### ` or `## ` heading or EOF.
4. Append captured block to `BACKLOG_ARCHIVE.md` under the matching
   Stream heading (creating the heading if absent), preserving
   reverse-chronological order by archived date.
5. Add `**Archived:** YYYY-MM-DD` to the moved block.
6. Rewrite `BACKLOG.md` with the entry block removed.

Restore recipe (for reviving an archived item): operator copies the
entry block from `BACKLOG_ARCHIVE.md`, flips `[done]` → `[open]`,
removes `**Archived:**` line, prepends to the matching Stream
section in `BACKLOG.md`.

## Rationale

Pick transcript synthesis:

> C-2 is the most rational architectural choice for a single-operator
> + LLM environment. It delivers an immediate 25-30% reduction in
> active token context by stripping out completed work, without
> requiring an irreversible, high-cost rewrite of existing multi-repo
> metadata.

Specific drivers:

- **Asymmetric validation** (Claude's Round 2 framing). Stream
  taxonomy and fielded entries have been validated by use as handoff
  anchors. Inline `[done]` tags have merely survived without
  scrutiny. C-2 keeps what works and fixes what doesn't.
- **Two-file state solves the actual observed defect** —
  `.dev-knowledge` BACKLOG's roughly half-done entries push open items
  below the LLM's attention zone at session start. Two-file split
  fixes this immediately.
- **Validator at session start, not end** (DeepSeek's operational
  maxim: "We never place a blocking error path on a non-critical-path
  maintenance operation"). Fail-fast at session boundary; don't
  introduce a latency bomb at session end.
- **Deterministic extraction script, not LLM prompt** — explicit
  rejection of LLM reliability for housekeeping (Grok's Round 1
  position was the panel's weakest argument). Script is < 50 LOC and
  testable.
- **No scope-tag inline ceremony.** Per-entry `[scope]` tags add
  ceremony without payoff at current ecosystem scale; the Stream
  section already carries the routing signal.
- **Kill criteria codified.** ADR is not "stream taxonomy forever" —
  it triggers automatic review when growth invalidates the choice.

## Alternatives considered

### Option C-1 — Stream-grouped, inline `[done]` (existing convention)

Single file with `[done]` items mixed with `[open]` items in same
sections, quarterly archival only.

**Why not chosen:** Does not fix the observed scannability defect —
this is the current state that produced the drift. Done items inline
continue to dilute LLM attention at session start.

### Option C-3 — Now/Next/Later + Two-file state (research's strong recommendation)

Replace streams with `## Now` / `## Next` / `## Later` sections;
scope-tag-only routing.

**Why not chosen:** Burns the validated cross-repo Stream coordination
signal without concrete evidence that stream-based routing is
currently failing. The Now/Next/Later pattern is optimized for
sprint-style execution; `.dev-knowledge` BACKLOG is long-horizon
governance work where items sit for weeks. ADR-47 codifies kill
criteria that automatically trigger reconsideration if growth
invalidates the C-2 choice.

### Option C-4 — Hybrid: Now/Next/Later within Streams

Two-level hierarchy (Stream H2 → N/N/L H3 → checkbox items).

**Why not chosen:** Adds temporal hierarchy with no evidence of
demand. Migration cost is high; benefit is theoretical until kill
criteria fire. Reserved as the natural next step **if** C-2's kill
criteria trigger.

## Consequences

### Positive

- BACKLOG.md becomes high-signal active state — `[open]` items are
  the only things competing for LLM attention at session start.
- 25-30% immediate reduction in active token context across
  ecosystem BACKLOGs.
- Stream coordination signal preserved for multi-repo planning.
- Extraction script is testable, deterministic, and ~50 LOC.
- Validator runs at session start — operator catches drift before
  losing context to it.

### Negative

- Initial migration must extract ~half of `.dev-knowledge` BACKLOG
  entries to archive (Session D scope).
- Restoring an archived item requires manual operator action (not
  automatable safely).
- Audit-trail querying across `BACKLOG_ARCHIVE.md` is not designed
  here — future tooling concern.
- Append-only archive file may grow indefinitely until a separate
  archive-rotation policy is defined.

### Follow-ups

- **Session D** (cleanup pass): one-time, zero-touch-for-open-items
  extraction of all `[done]` entries to a new `BACKLOG_ARCHIVE.md`
  per repo. Preserves stream headings in archive. Updates ADR-41 to
  reference ADR-47.
- **Session E** (audit tool extension):
  - Implement `check_backlog_organization` per the enforcement
    section. Fatal-error checks 1-4; warn checks 5-6.
  - Implement extraction script (`scripts/backlog_archive.py` or
    similar) per the extraction-script section.
  - Wire validator into session-start hook or pre-commit.
- **ADR-41 amendment** — add a reference to ADR-47 in ADR-41 §
  Storage; ADR-41 stands as the "file mandate" decision, ADR-47 is
  the "file schema" decision.
- **Document executable restore recipe** in PLAYBOOK or
  HANDOFF_PROCESS so future sessions can revive archived items
  without re-deriving the procedure.

## References

- Council research transcript: `docs/decisions/transcripts/council-out-20260515_185730-research-research-brief-cross-repo-backlog-organization-res.md`
- Council pick transcript: `docs/decisions/transcripts/council-out-20260515_194305-pick-council-pick-cross-repo-backlog-organization-decis.md`
- ADR-27 (scope tagging architecture)
- ADR-37 (session boundary protocol — BACKLOG as handoff anchor)
- ADR-38 (universal repo architecture)
- ADR-39 (file lifecycle governance)
- ADR-41 (BACKLOG architecture — file mandate refined here)
- ADR-46 (cross-repo dated-entries format — paired decision)
- "Lost in the Middle" — Liu et al., transformer attention curve

## Synthesis notes (operator-visible)

Where the pick transcript was ambiguous and this ADR made a judgment
call:

1. **Scope tag ceremony.** Synthesizer kept `<!-- SCOPE_SCHEMA: -->`
   in the Recommended Decision (carried over from research). This
   ADR explicitly **does not adopt** inline scope tags or
   SCOPE_SCHEMA. Justification: streams already carry the
   routing signal; per-entry tags add ceremony without payoff at
   `.dev-knowledge` scale.
2. **Cross-stream-canary blind spot.** Synthesizer flagged that the
   "Cross-stream" section being >30% of entries would invalidate the
   stream taxonomy. This ADR encodes that as a 33% kill criterion.
3. **Restore mechanism.** Synthesizer Action Item #4 said "document
   an explicit command or copy-paste recipe." This ADR specifies the
   manual recipe (operator copy-paste, flip status, prepend) but
   defers automated restore to Session D/E judgment.
4. **Write-only ceremony blind spot.** Synthesizer questioned whether
   the verbose entry schema (What/Why/Vision ref) is read by LLM
   agents at all. This ADR preserves the schema (it is read; HANDOFF
   processes cite Vision ref) but flags the question for revisit at
   the first kill-criterion review.
