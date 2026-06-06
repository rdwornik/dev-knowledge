<!-- scope: meta -->

# ADR-75 — Exclusion-zone register

- **Status:** Accepted — 2026-06-06
- **Related:** ADR-74; global CLAUDE.md §P0
- **Decommission:** none
- **Source:** Operator ratification, browser session 2026-06-06 (doctrine pass, gap G4).

## Context

The "OneDrive - Blue Yonder" P0 exclusion zone is enforced by a global PreToolUse hook (`block-onedrive.ps1`) and stated in global CLAUDE.md §P0, but no ADR records the decision. If the rule needs to evolve (additional zones), there is nothing to amend.

## Decision

A formal **exclusion-zone register** exists as governance doctrine. Each zone is defined by:

- **Path pattern** — the substring or glob that identifies the zone
- **Rationale** — why automation must not write or delete into this path
- **Enforcing organ** — a fail-closed PreToolUse hook (or equivalent) on the executing path

**Founding member:**

| Field | Value |
|---|---|
| Path pattern | any path containing `OneDrive - Blue Yonder` |
| Rationale | live corporate data; a write or delete is unrecoverable (past cleanup scripts deleted Rob's personal files alongside SharePoint copies) |
| Enforcing organ | global PreToolUse hook `block-onedrive.ps1` (covers Bash + PowerShell tools) |

**Governance rule:** new zones are added by amending ADR-75. A register entry with no enforcing organ on the executing path is decoration — every zone must be backed by a fail-closed organ before the entry is considered active.

## Consequences

- The P0 rule becomes citable and extensible; `block-onedrive.ps1` and CLAUDE.md §P0 are now implementations of a recorded decision rather than floating conventions.
- Future zones (e.g. a secrets directory, a production config path) have a clear amendment target.
- The "no organ = decoration" rule prevents the register from accumulating paper zones with no enforcement.

## Alternatives considered

Per-zone ADRs — rejected; a register with a single amendment target is simpler and keeps all exclusion policy findable in one place.
