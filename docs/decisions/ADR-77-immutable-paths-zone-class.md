<!-- scope: meta -->

# ADR-77 — Immutable-paths zone class (transcripts)

- **Status:** Accepted — 2026-06-06
- **Amends:** ADR-75 (exclusion-zone register — adds a second zone class)
- **Related:** ADR-74; ADR-68 (the in-place ADR-amendment precedent); CLAUDE.md §5; BACKLOG #105, #112, #23
- **Decommission:** none
- **Source:** Operator GO 2026-06-06 (implementation wave; research-validated — deterministic constraints belong on the executing path, not in aspirational prose). Scope ruled by the operator after the UNDERSTAND-valve surfaced a sanctioned in-place flow on ADRs.

## Context

ADR-75 established an exclusion-zone register with a single member (the `OneDrive - Blue Yonder` P0 zone) and the rule that **new zones are added by amending ADR-75**, each backed by a fail-closed enforcing organ. This ADR adds the second zone class: **immutable decision-record paths** — files that are *evidence*, where history that can be silently edited is not evidence.

The implementation valve found that the obvious framing ("block in-place edits of all ADRs and transcripts", BACKLOG #105) collides with a **sanctioned, in-use flow**:

- **ADRs are amended in place today.** CLAUDE.md §5 rule #3 itself sanctions "supersede with a new file **or in-file marker**"; ADR-68 carries a formal in-place `## Amendment 2026-06-01` section (commit `69efa9a`, explicitly "the append-only ADR rule"). A hard guard over `docs/decisions/*.md` would block a legitimate convention.
- **Transcripts have a clean record.** All 37 transcript files under `docs/decisions/transcripts/**` are single-commit — never edited in place. The zone is conflict-free.
- **Handoffs and audits are deliberately NOT in scope.** Handoff bundles are append-amendable by design (HANDOFF_PROCESS v4 — e.g. the `04_RECENT.md` append flow and the v4.3 "Amendment A" precedent); audits use a dated-addenda convention. Both have sanctioned in-place flows and stay outside the zone.

## Decision

**1 — Transcripts immutable zone (enforced now).** A new register entry, backed by a fail-closed PreToolUse organ:

| Field | Value |
|---|---|
| Path pattern | any path containing `docs/decisions/transcripts/` (incl. the `archive/` subfolder) |
| Rationale | Council debate records are evidence; an editable record is not a record. Supersede a transcript by adding a new dated file, never by rewriting one. |
| Enforcing organ | project PreToolUse hook `scripts/hooks/block_immutable_edits.py` (matches Edit / MultiEdit / Write / NotebookEdit) |

Semantics: an in-place edit of an **existing** transcript is denied (Edit/MultiEdit/NotebookEdit always; Write only when the target already exists); **creating a new** transcript is allowed (it is the lifecycle). The organ fails **open outside** the zone (a guard malfunction must never block normal work) and **closed inside** it once a zone path is positively identified.

**2 — ADR zone: ruled direction, not yet enforced (Option A, queued).** ADRs will join the immutable zone via a **script-enforced amend path**: a helper (`scripts/hooks/adr_amend.py`, BACKLOG #112) becomes the **only** sanctioned writer of an Amendment/status line on an existing ADR, and the guard denies every *other* in-place ADR edit. The canonical Amendment format is derived from ADR-68's formal Amendment + the HANDOFF v4.3 "Amendment A" precedent. Existing in-place annotations (ADR-68, etc.) are **grandfathered**.

**3 — Option B rejected (for now).** The alternative — a hard ADR zone with the doctrine that supersession/refutation is recorded **only** in a new ADR + JOURNAL — was rejected on **discoverability** grounds: until BACKLOG #23 (the navigable supersedes/related/amends graph) exists, forcing every amendment into a separate new file scatters a decision's history across unconnected files with no index. Revisit Option B once #23 ships and supersession is followable without reading every ADR.

## Consequences

- Decision-record integrity becomes a debuggable invariant on the executing path, not a convention in prose — the same posture ADR-75 set for the P0 zone.
- The register now has the extension shape ADR-75 promised: zone class #2 added by amending, backed by a real organ ("no organ = decoration").
- BACKLOG #105 is **partially** delivered (transcripts portion); handoffs/audits are removed from its scope; its ADR portion is re-routed to #112 (Option A). #105 stays open.
- A future CLAUDE.md §5 cleanup is owed: the self-contradictory "supersede with a new file **or in-file marker**; never edit in place" resolves to "append-only via the `adr_amend` helper" once #112 lands (tracked in #112, includes the freshness re-read + restamp).

## Alternatives considered

- **Whole-`docs/decisions/*` zone now (the #105 framing):** rejected — blocks the sanctioned in-place ADR-amendment flow. Scope shrinks to transcripts rather than silently exempting ADRs.
- **Option B (hard ADR zone + new-file-only doctrine):** rejected until #23 (discoverability), per Decision 3.
- **Including handoffs / audits:** rejected — both have sanctioned append/dated-addenda flows; guarding them would block legitimate work.
