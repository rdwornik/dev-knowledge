# ADR-41 — Cross-Session Backlog Architecture (BACKLOG.md)

<!-- scope: meta -->

Status: Accepted
Date: 2026-04-30
Related: ADR-29 (grandfathering pattern), ADR-32 (HANDOFF_PROCESS v2.0),
         ADR-33 (universalization), ADR-37 (session boundary protocol),
         ADR-38 (universal repo architecture, mandatory files per tier),
         ADR-39 (file lifecycle governance, 6-element pattern),
         ADR-40 (scale tier evaluation, M+ mandate trigger),
         transcripts council-out-20260430-134721-*,
         council-out-20260430-150751-research_*

## Context

Pending items historically scattered across handoff "Pending" sections
(per ADR-32 §4), JOURNAL entries, TODO comments in code, and open
questions in chat history. No central backlog → strategic drift,
O(n) discovery latency, lost cross-stream visibility.

Council research debate (council-out-20260430-150751-*) validated
centralized backlog file approach:
- "Lost in the middle" attention degradation hurts LLMs reading
  hybrid files (README/JOURNAL with embedded backlog)
- O(1) lookup vs O(n) handoff scan
- At ecosystem scale (4+ streams, 20-40 items) dedicated file pays
  back maintenance cost
- LLM Wiki pattern (Karpathy) validates plain Markdown as native
  database for AI agents

Council Scrum framework debate (council-out-20260430-134721-*) rejected
Scrum vocabulary as cargo cult for solo LLM workflow (9 of 12 elements
<40% fidelity) but extracted structural insight: centralized queue.
"Backlog" used as plain English noun, not Scrum term.

Rob's insight on tier applicability: M and L tiers mandate BACKLOG.md
(proactive — easier to maintain from start than retrofit). S tier
uses handoff §4 (existing pattern sufficient at small scale).

## Prior Art

Inspired by Scrum's product backlog concept — strategic queue separated
from tactical sprint planning. ADR-41 adopts the *structural insight*
(centralized queue with priority and stream context) without importing
Scrum vocabulary, ceremonies, or roles. Mental model lives here for
historical reference; daily templates use plain English ("backlog item",
"pending", "priority") not Scrum terms ("user story", "sprint backlog",
"product owner").

## Decision

### Storage

Single canonical file: `.dev-knowledge/BACKLOG.md` (for .dev-knowledge
ecosystem-level backlog).

For child repos at M+ tier: each repo MAY have own `BACKLOG.md` per
this schema. Recommended for tier L repos with 10+ active items
(reduces .dev-knowledge BACKLOG bloat). Tier M repos typically
contribute to .dev-knowledge BACKLOG via Stream sections.

Strict curation — actionable items only. Speculative or distant ideas
route to VISION.md per Council anti-pattern: "write-only graveyard."

### Tier mandate (per ADR-40)

| Tier | BACKLOG.md status |
|---|---|
| **S** | Optional. Pending items live in handoff §4 per ADR-32 (status quo). |
| **M** | MANDATORY. Repo's own BACKLOG.md OR contribute to .dev-knowledge BACKLOG.md "## Stream {name}" section. |
| **L** | MANDATORY. Repo's own BACKLOG.md (avoids .dev-knowledge BACKLOG bloat at L scale). |

Trigger for new repo crossing S→M threshold: BACKLOG.md initialization
required within 2 sessions per ADR-40 transition procedure.

### Schema (rigid template, mutation-resistant)

Items use lightweight format optimized for solo dev + LLM consumption:

```
## Stream {name}

### [P{1-3}] [Status] Item title
- **What:** brief description
- **Why:** rationale / triggering context
- **Vision ref:** (optional) link to VISION.md section if strategic
- **Added:** YYYY-MM-DD by {browser-1 or audit-tool or rob}
- **Status:** open | in-progress | blocked | done
```

Where:
- `P1` = critical / blocking other work
- `P2` = important / next 1-3 sessions
- `P3` = wishlist / when capacity allows

Anti-pattern: do NOT mutate this template structure during edits.
LLMs left to themselves drift in formatting; rigid template + audit
checks prevent mutation creep.

### Stream sections (multi-stream visibility)

In .dev-knowledge BACKLOG.md, items organized by stream:
- `## Stream A: corp-monorepo`
- `## Stream B: ai-council`
- `## Stream C: .dev-knowledge`
- `## Stream D: corp-sca-time-automation`
- (additional streams added as ecosystem grows)

Plus optional cross-stream section:
- `## Cross-stream / Ecosystem`
  (items affecting multiple repos)

### Grooming cadence (default specified)

**Per-handoff (lightweight, mandatory)**:
- Browser 1 reviews backlog at session end
- Marks stale items (no progress in 3+ sessions) for review
- Prunes obvious dead items (completed, no longer relevant)
- Adds new items surfaced this session
- Time budget: ~2 minutes

**Quarterly (deep, scheduled)**:
- Rob reviews full backlog
- Archives DONE items to `BACKLOG-archive/YYYY-Q{N}.md`
- Re-prioritizes P1/P2/P3 based on current ecosystem state
- Removes items that no longer align with VISION
- Time budget: ~30 minutes per quarter
- First quarterly review: 2026-07-01

Default cadence specified to prevent write-only graveyard — Council
flagged this risk explicitly.

### Integration with ADR-37 handoffs (Split-Brain elimination)

Per Council research finding: handoffs and BACKLOG must NOT duplicate
pending state.

**BACKLOG = single source of truth for ALL pending items.**

Handoff integration:
- Handoff §4 "Pending — next session candidates" (per ADR-32 v2.0)
  → DEPRECATED. Replaced with "Pending items: see BACKLOG.md" pointer.
- Handoff Future State (per ADR-37) = THIS session's tactical plan,
  i.e. which BACKLOG items this session targets. NOT a duplicate queue.

Browser 1 (departing) at handoff generation:
1. Reads BACKLOG.md for current state
2. Updates BACKLOG.md with items surfaced this session
3. Marks completed items DONE
4. Future State references BACKLOG items by stream + title (pointers,
   not duplication)
5. May copy-paste critical P1 items into Future State if browser 2
   needs them inline (Council Risk #2 mitigation — light duplication
   acceptable at P1 only)

Browser 2 (incoming) at session start:
1. Reads handoff Current State + Future State (per ADR-37)
2. Reads BACKLOG.md for full pending context
3. Validates Future State items against BACKLOG.md (drift check
   per ADR-37)
4. Acts on prioritized items

Eliminates split-brain risk: no duplication between handoff and BACKLOG.

### Enforcement (Rob's pushback 1)

Backlog review instruction lives in `first-message.md` template
(consistent with ADR-37 validation enforcement pattern):

- Audit handoffs `first-message.md`: STRONG ("MUST review BACKLOG.md
  before acting")
- Session handoffs `first-message.md`: MEDIUM ("SHOULD review
  BACKLOG.md before acting")

Implementation deferred to ADR-32 / ADR-37 template update session —
`HANDOFF_PROCESS.md` + `HANDOFF_TEMPLATE.md` + `first-message.md`
templates updated together to reflect ADR-37/ADR-41 integration.

Markdown alone cannot force compliance; template-level enforcement
is the practical boundary.

### VISION.md cross-link (Rob's pushback 4)

Items MAY include `Vision ref:` pointer to specific VISION.md section
for strategic items. NOT mandatory.

Use cases for Vision ref:
- Strategic backlog items aligned with ecosystem direction
- Cross-stream items affecting multiple repos
- Items that need clear "why" beyond immediate context

Tactical items (single session, single repo, well-scoped) typically
do NOT need Vision ref — would be ceremony.

### Anti-pattern protections (Council research findings)

- **Write-only graveyard**: strict curation, ruthless quarterly
  grooming, default cadence enforced via per-handoff template
- **Split-brain**: BACKLOG = single source of truth for pending;
  handoffs reference it, never duplicate queue
- **Mutation drift**: rigid template-driven structure, system-level
  instructions forbid layout mutation during edits

### Universalization (per ADR-33 pattern)

- **Mandate**: .dev-knowledge maintains canonical BACKLOG.md
- **Mandate**: child repos at M+ tier (per ADR-40) maintain BACKLOG.md
  OR contribute to .dev-knowledge BACKLOG.md Stream sections
- **Recommendation**: tier S repos use handoff §4 status quo until
  S→M transition triggers BACKLOG mandate
- **Cross-repo audit (Phase 3)**: auditor verifies BACKLOG.md presence
  per tier compliance, format compliance, grooming activity

### Lifecycle entry (per ADR-39)

#### BACKLOG.md

| Element | Value |
|---|---|
| Purpose | Canonical cross-session pending items per stream. Strategic queue. NOT chronological log (JOURNAL), NOT decision rationale (ADRs), NOT current session plan (handoff Future State). |
| Update trigger | Mutable. Per-handoff lightweight grooming (~2 min) + quarterly deep grooming (~30 min). Items added/edited/marked done as work progresses. |
| Owner | Browser session (per-handoff updates) + Rob (quarterly grooming) |
| Grooming | Per-handoff lightweight + quarterly deep. First quarterly: 2026-07-01. |
| Boundaries | Canonical for cross-session pending state. Handoff Future State references BACKLOG items (pointers, not duplication). Split-brain prevention: BACKLOG wins as source of truth. |
| Enforcement | first-message.md template (STRONG for audit, MEDIUM for session handoffs). Audit tool (per ADR-36) verifies presence + format compliance per tier. |

This entry to be added to ADR-39 registry on next ADR-39 amendment
(grouped with other deferred amendments to minimize ADR amendment churn).

## Consequences

### Positive
- Single discovery point: O(1) lookup vs O(n) handoff scan
- Strategic visibility across streams in one file
- ADR-37 Future State + BACKLOG.md = complete tactical+strategic picture
- Cargo-culting Scrum vocabulary avoided — plain English keeps cognitive
  tax at zero
- Default grooming cadence prevents write-only graveyard
- Stream sections respect actual multi-repo workflow
- VISION.md cross-link optional — strategic items get clear "why",
  tactical items stay lean
- Tier-aware mandate (per ADR-40) — proactive at M, prevents L retrofit
- Lifecycle compliance per ADR-39 — explicit ownership, trigger,
  grooming, boundaries, enforcement

### Negative
- Yet another file to maintain (mitigated by mandatory per-handoff
  grooming = ~2 min)
- Browser 1 cognitive load: must update BACKLOG.md at session end
- Risk of duplication between Future State (handoff) and BACKLOG.md
  (mitigated by REFERENCES not full duplication; light copy-paste
  acceptable for critical P1)
- Stream organization adds slight friction (which stream does this
  belong to?) for cross-cutting items (mitigated by Cross-stream
  section)
- Tier transition (S→M) requires BACKLOG.md initialization within
  2 sessions (manageable per ADR-40 transition timeline)

### Follow-ups
- Initial BACKLOG.md seed: Stream C items currently scattered across
  recent handoffs (this session, Step 2 below)
- HANDOFF_PROCESS.md + HANDOFF_TEMPLATE.md + first-message.md updates
  reflecting BACKLOG.md integration (separate session)
- ADR-32 §4 deprecation note (separate session): "Pending — next session
  candidates" deprecated in favor of BACKLOG.md reference
- Audit tool (ADR-36) integration: findings as backlog items per gap
  severity (P3 implementation)
- Backlog tooling CLI if needed (post-evidence, not P1)
- Quarterly grooming: first review at 2026-07-01
- ADR-39 amendment: add BACKLOG.md lifecycle entry to registry (grouped
  with other deferred amendments)

## References

- transcript council-out-20260430-134721-pick-council-adr38-scrum-framework.md
- transcript council-out-20260430-150751-research-question-for-a-solo-developer-with-multiple-active.md
- ADR-29 (lessons format and grandfathering)
- ADR-32 (HANDOFF_PROCESS v2.0)
- ADR-33 (VISION.md universalization)
- ADR-37 (Session Boundary Protocol — Future State integration)
- ADR-38 (universal repo architecture, mandatory files per tier)
- ADR-39 (file lifecycle governance)
- ADR-40 (scale tier evaluation, M+ mandate)

## Amendments

### 2026-06-02 — Supersession cross-reference + ecosystem backlog-form binding (closes BACKLOG #20)

- **Source:** Operator decision 2026-06-02 (ecosystem-unification effort). Closes
  BACKLOG #20 ("add a dated amendment to ADR-41 cross-referencing ADR-47/64/65").
- **Decision tier:** Path A — a housekeeping cross-reference plus the record of an
  operator-settled binding; no Council convene.

**The backlog-architecture supersession chain.** ADR-41 is the original spec; five
later decisions have replaced its model. This amendment records the chain so a reader
of ADR-41 is not misled by its superseded original text:

| Element of ADR-41 (original) | Now governed by |
|---|---|
| Tier mandate (S/M/L → BACKLOG.md) | Tiers deprecated (ADR-38 A5; ADR-40 deprecation). BACKLOG.md is MANDATORY for every repo (ADR-38 A5 + A6). |
| `## Stream {name}` sections | Retired as headers (ADR-64 Decision 2); repo affiliation is theme/text, not a stream section. |
| Rigid `### [P{1-3}] [Status] Item title` schema | Replaced by the story-map task line `- [#id] [P][size] … · Done when: … · refs` (ADR-64 schema restore + ADR-66 hierarchy). |
| Quarterly archive to `BACKLOG-archive/YYYY-Q{N}.md` | Retired — done items LEAVE; git is the record (ADR-47; ADR-64 Decision 1; ADR-65). No archive file (CLAUDE.md §5). |
| "plain-English noun, NOT Scrum vocabulary … not 'user story', 'sprint backlog', 'product owner'" | **Reversed for structure** by ADR-66, which adopts the Theme → User Story → Task story-map (Scrum + Patton). The anti-cargo-cult intent survives as **proportional depth** (ADR-38 A6) — hierarchy only where item volume justifies it. |
| Per-handoff + quarterly grooming cadence | Retained in spirit; the grooming log lives in the BACKLOG.md footer (ADR-66). |

**Ecosystem binding (ADR-38 A6, 2026-06-02).** The canonical backlog form — the ADR-66
story-map with proportional depth — binds all in-scope repos (`.dev-knowledge` + the four
child repos), because it feeds the git changelog (`git log --grep 'closes \[#'`) and must
be uniform. The file *mandate* (ADR-41) and the file *form* (ADR-64/65/66) are now both
universal; see ADR-38 A6 Delta 3.

**What still stands from ADR-41.** The core insight — a single canonical cross-session
`BACKLOG.md` as the source of truth for pending items, split-brain-free from handoffs — is
unchanged and is the foundation the later ADRs refine.
