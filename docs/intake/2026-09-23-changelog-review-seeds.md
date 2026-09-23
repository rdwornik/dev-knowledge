---
intake-id: 105
status: SEED
origin: "changelog-review, 2026-09-23 (claude-code 2.1.205-2.1.281; ADR-98 §7 SEED-feed)"
consumed-by:
---

# SEED — changelog-review findings (claude-code 2.1.205–2.1.281)

Pre-intake candidates from the 2026-09-23 changelog review (`docs/audits/2026-09-23-changelog-review.md`). A feed proposes; it never decomposes and never mutates the backlog. Each row is a candidate for a future functional/technical pass, not a commitment. Only ADOPT / OBSOLETES-WORKAROUND findings land here; NOISE / VERIFY / STALE-NAMES stay digest-only.

## S1 — `/skill-doctor` (ADOPT)

Claude Code 2.1.261 adds `/skill-doctor`: shows which loaded skills go unused and what they cost in context, "so you can prune them." This hub carries a large, growing `.claude/skills/` roster plus a hub-generated methodology roster deployed to consumers. **Candidate value:** a free, native signal on skill bloat/dead weight, directly relevant to this repo's byte-budget doctrine. **Candidate home:** run opportunistically at a session boundary; if it surfaces unused skills, file a row against the skill in question. No architect decision needed to try it — only to act on what it finds.

## S2 — `/doctor` CLAUDE.md-trim proposal (ADOPT / UNDERUSED-NATIVE)

Claude Code 2.1.206 adds a `/doctor` check that "proposes trimming checked-in CLAUDE.md files by cutting content Claude could derive from the codebase." This hub's `CLAUDE.md` is gated at `≤24,576 B` (`tests/test_claude_md_byte_cap.py`, ADR-53) and its own conventions section already forbids restating counts/rosters in prose — this native check automates a review this repo already does by hand at every `CLAUDE.md` edit. **Candidate value:** an independent, vendor-side second opinion on the same byte-budget problem this repo's tooling polices. **Candidate home:** run against `CLAUDE.md` before the next edit that touches it; if it proposes cuts, weigh them against ADR-53's ≤200-line / ≤24.4KB budget note.

## S3 — `omitClaudeMd` agent frontmatter (ADOPT)

Claude Code adds `omitClaudeMd` to agent frontmatter and `--agents` JSON (2.1.271-range): a subagent can run without loading user/project/local CLAUDE.md files (managed policy files still load). This hub's `CLAUDE.md` is intentionally large — it is governance doctrine for a Claude Code session working *on this repo*, not for every bounded task a subagent or external producer might run. **Candidate value:** a read-only research subagent, or the bounded external producer pattern the Copilot-offload line is trying to stand up (`docs/intake/2026-09-06-tech-copilot-offload-role-and-account-map.md`), does not need this repo's full governance doctrine loaded to do narrow, well-scoped work — cutting that load is a real token-cost win on every such spawn. **Candidate home:** fold into the Copilot-offload / bounded-producer intake line, or a new row on the dispatch/lane-contract surface (`scripts/provider_router.py`, `ecosystem/provider-registry.yaml`) where a producer's contract could declare `omitClaudeMd: true` for size-S bounded work.
