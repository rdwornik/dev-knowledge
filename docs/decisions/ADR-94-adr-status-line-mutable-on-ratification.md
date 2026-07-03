# ADR-94: ADR status line mutable on ratification (decision content frozen)

- **Status:** Accepted
- **Date:** 2026-07-03
- **Decision tier:** Architecture (Path A — direct operator ruling, Fable consult #1; operator-signed on the exact CLAUDE.md §5 item 3 before/after; no Council transcript, like ADR-87/90/92)
- **Related:** ADR-88 / ADR-89 (Pattern A — frozen `Proposed` header + in-file amendment marker), ADR-92 (Pattern B — Status line edited in place on ratification), #112 (the ADR immutable-zone amend helper — sibling), #242 (the status-flip coherence check this doctrine will be enforced by), CLAUDE.md §5 item 3 + §"File lifecycle" (the rule this narrows)
- **Source:** Fable consult #1, 2026-07-03 (architect-ratified; operator-signed). Consult chat expired; this records the accepted-and-signed ruling.
- **Decommission:** none

## Context

The repo's immutability convention (CLAUDE.md §5 item 3, §"File lifecycle") read as a blanket "ADRs, transcripts, handoffs, audits are immutable — never edit in place." But ratification — flipping an ADR's status from `Proposed` to `Accepted` — is a legitimate metadata change, and the repo had drifted into **two divergent patterns** for it, with no machine check reconciling them:

- **Pattern A (ADR-88/89):** the `**Status:**` header is left FROZEN at `Proposed`; the flip is recorded only in an appended `## Amendment — Accepted (operator ratification)` marker ("frozen header above unchanged per the immutability convention"). A reader scanning headers alone misreads the status.
- **Pattern B (ADR-92):** the `**Status:**` header is edited in place → `Accepted (ratified by merge …)`.

Both are recorded as legitimate ratifications, and no audit leg reconciles a frozen `Proposed` header against the README-index / CLAUDE effective "Accepted" status (the gap the 2026-06-21 JOURNAL ratify entry records). The blanket rule, read literally, made Pattern B a violation — while Pattern A's frozen headers are the actual readability hazard.

## Decision

The immutability rule is narrowed to distinguish **decision content** from the **status line**:

- An ADR's **status line is metadata, not decision content**, and MAY be edited in place on ratification (e.g. `Proposed → Accepted`).
- An ADR's **decision content remains frozen** — changed only by superseding with a new file or by an appended in-file amendment marker, never edited in place.
- **Transcripts, handoffs, and audits remain fully immutable** — this exception is **ADR-specific and covers the status line only**.

This standardizes the **go-forward** ratification mechanic on **Pattern B** (edit the Status line in place). It is recorded in CLAUDE.md §5 item 3 as the operator-signed text:

> 3. **ADRs, transcripts, handoffs, and audits are immutable** — supersede with a new file or an in-file amendment marker; never edit in place. **ADR ratification exception (ADR-94):** an ADR's *status line* MAY be edited in place on ratification (e.g. Proposed → Accepted) — the status line is metadata, not decision content. This exception is ADR-specific and covers the status line only; ADR decision content, and transcripts / handoffs / audits in full, remain immutable.

## Consequences

- **Easier:** a `Proposed → Accepted` flip no longer needs a frozen-header + marker dance; the header tells the truth. One consistent go-forward mechanic (Pattern B) replaces the A/B divergence.
- **Scope discipline:** the exception is narrow by construction — status line only, ADRs only. Editing an ADR's Decision/Context, or any part of a transcript / handoff / audit, is still forbidden in place (append or supersede). The added specificity is deliberate: a broad "immutable in decision content" phrasing was rejected as diluting transcript/handoff/audit immutability.
- **Retro-normalization deferred:** ADR-88/89 keep their frozen `Proposed` headers + markers for now — editing already-ratified history is a separate operator-gated task, out of scope here. This ADR governs go-forward.
- **Enforcement is filed, not built:** no machine check yet reconciles header status against README-index effective status, nor enforces Pattern B go-forward. That coherence check is tracked as **#242** (sibling of the #112 amend-helper), per ADR-81 (d) — a named deferral, not a silent gap.

## Alternatives considered

- **Keep the blanket rule (status quo).** Rejected: it made Pattern B a nominal violation while leaving Pattern A's frozen-header readability hazard un-addressed, and left the A/B divergence unreconciled.
- **Standardize on Pattern A (frozen header + marker) instead.** Rejected: the frozen `Proposed` header actively misleads a header-only reader, and it needs a companion coherence check to be safe; Pattern B makes the header self-truthful.
- **Broaden the exception to "decision content immutable" across all artifact types.** Rejected (operator correction): it over-generalized and diluted transcript / handoff / audit immutability. The exception is deliberately ADR-status-line-only.
