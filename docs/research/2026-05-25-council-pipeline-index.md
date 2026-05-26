---
type: research-index
scope: AI Council pipeline + .dev-knowledge docs/ taxonomy
date: 2026-05-25
status: index (entry point for the audit chain)
---

# AI Council Pipeline + docs/ Taxonomy — Audit Chain Index 2026-05-25

Entry point for the three-document audit of the AI Council pipeline lifecycle and the
`.dev-knowledge/docs/` folder taxonomy. Read in order; each builds on the prior.

## The chain

| # | Document | Layer | What it does |
|---|----------|-------|--------------|
| 1 | [`2026-05-25-council-pipeline-discovery.md`](2026-05-25-council-pipeline-discovery.md) | Description | Read-only inventory of both repos; Q1–Q9 mechanism; Stage 0–7 lifecycle table; all claims file-cited |
| 2 | [`2026-05-25-council-pipeline-audit.md`](2026-05-25-council-pipeline-audit.md) | Analysis | Findings A–G with severity (High ×4, Medium ×7, Low ×6); root-cause clustering |
| 3 | [`2026-05-25-council-pipeline-proposal.md`](2026-05-25-council-pipeline-proposal.md) | Prescription | Options A/B/C; recommends **B (truth-up first)**; phased plan; open questions |

## The chain in one paragraph

Discovery mapped the pipeline end-to-end (question draft in `research/` → manual copy to
`ai-council/council_inbox/` → `council --inbox` → transcript auto-routed to
`.dev-knowledge/docs/decisions/transcripts/` via ADR-43 → ADR in `docs/decisions/`) and inventoried every
`docs/` subfolder. The audit found two root problems behind four High findings: (1) **staleness** — ADR-43
shipped automatic transcript routing, but PLAYBOOK (×2 blocks), `decisions/README`, and a BACKLOG P2 item
still describe routing as "pending/manual"; and (2) **taxonomy** — `docs/research/` conflates research
*outputs* with Council-question *inputs*, so a file's folder no longer tells you what it is. The proposal
recommends **Option B**: correct the docs first (zero-risk truth-up), then separate question-staging from
research outputs and add one holistic lifecycle runbook — proportional to a low-volume solo pipeline, and
the smallest option that leaves no High finding open.

## Live corroboration (recorded during the audit)

While this audit was being written, the operator's in-flight `council --inbox` run completed its first
question and `ai-council/routing.py` **auto-deposited** a routed transcript
(`docs/decisions/transcripts/council-out-20260526_142806-pick-…-Q1-…md`) into `.dev-knowledge` — real-time
empirical confirmation of audit finding **E1** (routing is implemented, not "pending/manual"). These routed
transcripts are the operator's deferred handoff-debate outputs; they were **left untracked and not committed**
by this audit (out of scope; handoff topic deferred). See the session report / proposal open question 6.

## Operator next actions

1. Review the proposal; choose Option A / B / C / other.
2. Answer the proposal's open questions (esp. staging location, Q1).
3. Handle the newly-routed handoff transcript(s) separately (commit + ADR, or discard) — not part of this branch.
4. If changes are wanted, run each phase as its own prompt/branch (this audit applied nothing).

## Scope boundaries (what this chain did NOT do)

No files moved, no folders created/deleted, no methodology or ADR changed, **zero writes to ai-council**.
Out of scope by operator instruction: handoff process, workspace aliases, proposal implementation. The only
changes on this branch are these four `docs/research/` documents.
