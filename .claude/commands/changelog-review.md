---
name: changelog-review
description: Operator-invoked review of tool changelogs since last review (claude-code + codex) — fetch, classify per the audit-trio rubric, write a digest, bump the state file. PUSH trigger only; never implements adoptions.
---

The **PUSH** half of #113: an operator-invoked review of what changed in our tools'
changelogs since the last review. The SessionStart sentinel
(`scripts/changelog_sentinel.py`) only *nudges* ("installed > last reviewed"); this
command does the actual review. **Operator-invoked only — never scheduled, never
automatic** (operator ruling 2026-06-07, supersedes the routine shape).

This is the manual successor to the 2026-06-07 audit trio
(`docs/audits/2026-06-07-platform-max-audit.md` + `-codex-max-audit.md` +
`-methodology-transfer-audit.md`) — that trio is the v0 of this review and the
source of the classification rubric below.

**Contract — read before acting:**
- **Classification happens in THIS session** (the operator is present — this is the
  push flow, not automation). Use judgment, not a script.
- **Capture / flag ONLY. Never implement an adoption.** Anything you classify
  ADOPT / OBSOLETES-WORKAROUND is captured to the digest and flagged for the
  operator + the browser-chat architect. Adoption decisions are theirs (ADR-28
  roles; ESSENTIALS "Architect routing"). The command's job ends at the digest +
  the state bump.
- **No new BACKLOG items, no edits to other organs.** The digest is the artifact;
  the operator routes from it.

## The rubric (from the audit trio)

Classify every changelog entry *after* `last_reviewed_version` into exactly one bucket:

- **ADOPT** — a capability we lack and should queue (incl. UNDERUSED-NATIVE: the
  platform now has it and we hand-built or don't use it). State the value + a
  candidate BACKLOG home; do NOT create the item.
- **OBSOLETES-WORKAROUND** — a new native feature makes one of OUR artifacts
  (a script, hook, shim, convention) redundant. Name our artifact + what retires it.
- **STALE-NAMES** — a rename/removal means our live docs/config reference a
  now-wrong name. Give the concrete `file:line` drift (highest-confidence output).
- **VERIFY** — relevance depends on a live check. Give the **exact command** to run;
  do not guess the outcome.
- **NOISE-count** — irrelevant to our stack (enterprise/Bedrock/Vertex, IDE tweaks,
  telemetry, model-availability churn, sandbox internals N/A on Windows…). **Count
  it, do not itemize.**

## Steps

1. **Read state.** Read `ecosystem/tool-versions.yaml` — per tool grab
   `last_reviewed_version` + `source_url`. Note today's date for the digest name
   and the bump.

2. **Fetch (only here — the sentinel never fetches).**
   - **claude-code:** WebFetch the raw CHANGELOG at the tool's `source_url`
     (`https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md`).
     Keep only version headers **strictly greater** than `last_reviewed_version`.
   - **codex:** `gh release list -R openai/codex -L 30` then `gh release view <tag>
     -R openai/codex` for each **stable** release newer than `last_reviewed_version`
     (skip alphas/pre-releases). If `gh` is unavailable, say so and fall back to
     WebFetch on the releases page; record the limitation in the digest.

3. **Classify.** Put every extracted entry into one rubric bucket. Intersect against
   OUR stack — installed versions, our hooks/scripts/docs, open BACKLOG items. When
   an entry maps to an existing BACKLOG id, name the id (so the operator sees the
   tie-in) — but do not edit it.

4. **Write the digest** to `docs/audits/<today>-changelog-review.md`. Use a flat,
   scannable layout (no wide tables — render-layer rule, CLAUDE §4). Header block:
   tools + version ranges reviewed + counts per bucket. Then one section per bucket
   (NOISE is a single count line + one-clause "what it covers"). End with an
   **operator-routing** line: which ADOPT/OBSOLETES items want an architect decision.

5. **Bump the state file.** Update `ecosystem/tool-versions.yaml`:
   `last_reviewed_version` -> the newest version you actually reviewed per tool
   (claude-code -> latest CHANGELOG header reviewed; codex -> latest stable
   reviewed, which MAY be ahead of installed — that's intended, it keeps the
   sentinel quiet until a still-newer version installs), `reviewed_date` -> today.

6. **Commit (its own commit).** Stage the digest + the state file and commit
   (PowerShell here-string or `git commit -F`, per the channel-discipline LESSON):
   `docs(audits): changelog-review <ranges>` with a body summarising the bucket
   counts + any ADOPT/OBSOLETES flagged for the operator. If this run closes the
   #113 Done-when ("one real post-update run produces a digest and bumps the state
   file"), add `closes [#113]` and remove #113 from BACKLOG in the same commit.

7. **Report** to the operator: per-tool ranges reviewed, the bucket counts, and —
   explicitly — every ADOPT and OBSOLETES-WORKAROUND item, because those are the
   operator's + architect's decision and the whole point of the push.

**Never** implement an adoption, never schedule this, never fetch from the sentinel.
