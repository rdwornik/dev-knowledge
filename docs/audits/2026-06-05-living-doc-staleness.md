<!-- scope: meta -->
# Living-Doc Staleness Map — 2026-06-05

**Date:** 2026-06-05
**Author:** Claude Code (Opus 4.8), operator Rob
**Backlog:** the doc-debt conversion of the Phase-D codification arc (#84 + the
ARCHITECTURE / CONTRIBUTING / CLAUDE.md items added this session)
**Nature:** **Immutable audit record** (per CLAUDE.md §5 / ADR-39 — audits are
immutable once merged; supersede with a new dated file, never edit in place).

## Provenance

Copied faithfully from the `docs/handoffs/2026-06-05-dev-knowledge-session`
handoff bundle — specifically **Workstream 1 ("living-doc staleness map")** of
the Phase-1 interview (`_handoff-interview.md`), which was folded into `05_NOW.md`
and removed at Phase-2 consolidation, so the full table survives only in git
history. This is the **FINAL CORRECTED** version: the `ARCHITECTURE.md` row was
operator-verified by grep against the live file and rewritten in commit
**`19c2b72`** ("docs(handoff): correct staleness-map ARCHITECTURE row
(operator-verified)") — the earlier "cloud-night + nightly Action ARE already
present" parenthetical was false (confused with CONTRIBUTING's C4 section).

This map is the **acceptance oracle** for the doc-debt BACKLOG items: a row
"flips to **CURRENT**" when its Phase-D codification lands. The map itself is the
record of the *starting* state (2026-06-05) and does not change as rows flip —
flips are tracked by the items' closures in git.

## Workstream 1 — living-doc staleness map (the rewrite targets)

| File | Verdict | Phase-D codification targets |
|---|---|---|
| `ARCHITECTURE.md` | **STALE** (operator-verified by grep against the live file) | **Fully missing** — the GitHub remote/push reality, the cloud-night pipeline + nightly Routine, the spec-orchestration doctrine, the in-repo conformance-hub workflow, the GitHub Action / nightly-triage outcome loop, t-shirt model routing, machinery retirements (C3), and the adoption process. **PLUS** the ADR-68 night-agent section is **misleading**: it describes a mechanism that was never registered (C3 finding) and is superseded in reality by the cloud Routine → needs a **supersession note**. (The earlier "cloud-night + nightly Action ARE already present" parenthetical was **false** — likely confused with CONTRIBUTING's C4 section.) |
| `CLAUDE.md` | **STALE-by-deferral** | silent on cloud/nightly/spec-orch/routing; ≤200-line per-repo instruction defers to ARCHITECTURE — fix = add pointers once ARCHITECTURE gains the sections |
| `VISION.md` | **CURRENT** | strategic layer; operational detail appropriately deferred (optional: name model-routing efficiency as an emphasis) |
| `CONTRIBUTING.md` | **PARTIAL** | nightly Action + cloud-night documented; MISSING the spec-orchestration fallback rationale (why the `.js` workflow exists / when it runs) |
| `protocols/PLAYBOOK.md` | **STALE** | verify+complete Appendix B Model-Routing Table (suspected stub); add GitHub-Actions/cloud standards; add machinery-retirement patterns; expand §6 adoption with kill-criteria + tool-vs-platform rubric |
| `protocols/ESSENTIALS.md` | **CURRENT** | daily cheat sheet; correctly defers detail to PLAYBOOK/ARCHITECTURE |

## Phase-D agenda (the codification topics)

*(Copied verbatim from the same bundle block — the codification doctrine the
rewrites must land.)*

- **Adoption process** — rubric = tool-vs-platform / pain-owned-vs-imagined / subscription-economy fit + pilot discipline with **pre-registered kill criteria** + 3 case studies (Dynamic Workflows **ADOPT**, graphify **REJECT**, GitHub Action **ADOPT**).
- **T-shirt model-routing doctrine** — S=Haiku, M=Sonnet, L/judgment=Opus; unpinned fan-out = bug; unpinned default inherits the **main session model** (Opus 4.8). Verified functional on **both** the Agent-tool and workflow-engine paths after removing the `CLAUDE_CODE_SUBAGENT_MODEL=haiku` override (the C3 root-cause).
- **Deterministic prose-vs-state checker** — BACKLOG **[#89]** (counts / version stamps / enumerated lists = three evidence loci).
- **V4 verifier candidate** — BACKLOG **[#90]** (git↔backlog two-direction reconciliation — the inverse of V3; this sweep ran it manually as the reference spec).
- **Cloud-readiness** — shallow clones; environment guards in hooks; spec-orchestration as the canonical cloud execution path with a nightly native re-probe; cloud-session closeout = check stranded `claude/*` branches.
- **Maintenance cadences** — quarterly machinery review; plans prune.
