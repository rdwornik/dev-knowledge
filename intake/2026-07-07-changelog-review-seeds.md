---
intake-id: 5
status: SEED
origin: "changelog-review, 2026-07-07 (claude-code 2.1.202; ADR-98 §7 SEED-feed)"
consumed-by:
---

# SEED — changelog-review findings (claude-code 2.1.202)

Pre-intake candidates from the 2026-07-07 changelog review (`docs/audits/2026-07-07-changelog-review.md`). A feed proposes; it never decomposes and never mutates the backlog. Each row is a candidate for a future functional/technical pass, not a commitment. Only ADOPT / OBSOLETES-WORKAROUND findings land here; NOISE / VERIFY / STALE-NAMES stay digest-only.

## S1 — Dynamic-workflow-size `/config` setting (ADOPT / UNDERUSED-NATIVE)

Claude Code 2.1.202 adds a `/config` control for how large Claude makes dynamic workflows (small / medium / large agent counts — advisory, not an enforced cap). We orchestrate multi-agent work through the Workflow tool but set no default size, so fan-out breadth is ad hoc per invocation. **Candidate value:** a fleet-default lever on workflow agent-count, relevant to token discipline and operator load. **Candidate home:** #155 (loops architecture) or a PLAYBOOK workflow-doctrine note; ties to #270 (operator-load gauge). The architect rules whether to set a default and where to record it.
