# LANE CS — Codespaces transport enablement: ACT 1 (Claude Code in image) + ACT 2 (credential path)

| Field | Value |
|---|---|
| Model | opus |
| Effort | high |

**Repo:** `.dev-knowledge` · **Launch:** ruled verb (`dispatch LANE-CS-codespace-transport.md`) —
dispatcher creates the worktree and branch; use whatever branch it creates · **Substrate: LOCAL
worktree** (gates armed). READ THIS TWICE: `dispatch` is LOCAL-ONLY and does not route; the word
"Codespace" in this filename names the SUBJECT of the work (the `.devcontainer/` image), not the
substrate. Nothing in this lane runs on Codespaces; the smoke run happens post-integration via
`Dispatch-Codespace` from the operator's machine. Commit-and-**STOP**.

**Purpose.** `Dispatch-Codespace` is built and proven end-to-end; the container answered in its
own words: `{"error":"claude is not installed in this devcontainer"}` (runner guard, exit 91).
Two blockers remain, both in-repo. Closing them makes the substrate table's Q4 default real.
Authority: BRIEF-TO-ARCHITECT-DISPATCH.md §3 (operator + outgoing seat, BINDING, 2026-08-25).

## Read first
`.devcontainer/` in full (`devcontainer.json`, `Dockerfile`, `provision.sh`, `provisioning.yaml`)
· the `[#554]` history on `devcontainer.json:53-70` (the `containerEnv` block was DELIBERATELY
removed; that removal was correct and stays) · BRIEF-TO-ARCHITECT-DISPATCH.md §2.5 + §3 (landed
in `docs/audits/` by a sibling lane; if not yet merged, read it from
`C:\Users\1028120\Downloads\BRIEF-TO-ARCHITECT-DISPATCH.md`).

## UNDERSTAND
- **Problem:** the Codespaces substrate has a proven transport and a destination, but the image
  lacks the runtime (ACT 1) and the container has no credential path (ACT 2).
- **Scope:** `.devcontainer/` only. Two commits. Nothing else.
- **Risks:** (a) inventing the install command — forbidden, derive from the current official doc
  and QUOTE the doc line in the commit message; (b) resurrecting the removed `containerEnv` —
  forbidden; (c) introducing `ANTHROPIC_API_KEY` anywhere in the image or config — forbidden
  (precedence would silently flip billing off-subscription).
- **Failure mode:** touching any file outside `.devcontainer/`.

## Steps

**1. ACT 1 — install Claude Code in the devcontainer image.**
Derive the CURRENT documented Linux install path from code.claude.com (fetch it live), add it as
one devcontainer feature or one `RUN` line in `.devcontainer/Dockerfile` — whichever the official
doc recommends for devcontainers. Quote the doc line verbatim in the commit message. Pin what is
pinnable (version/checksum where the doc offers one). Validate: image config lints clean;
`devcontainer.json` references stay coherent. **COMMIT.**

**2. ACT 2 — credential path via the documented user-secret mechanism.**
Expose the ALREADY-CREATED user-level Codespaces secret `CLAUDE_CODE_OAUTH_TOKEN` to the
container using the mechanism GitHub's own docs prescribe for Codespaces user secrets (derive it
live; quote the doc line in the commit). Do NOT re-add the removed `containerEnv` block; do NOT
reference `ANTHROPIC_API_KEY`. The exposure/rotation register note is landed by a sibling lane in
the standing register — reference it by name in the commit message (deviation from "same commit"
per operator-approved single-writer-per-file). **COMMIT.**

**Final.** Lane report per `/save`: what was pinned, the two quoted doc lines, and the statement
that smoke 5 (the DONE-WHEN: `Dispatch-Codespace` returning `Ok=True` AND `RemoteExitCode=0`
with an in-container audit-check-count receipt) executes POST-INTEGRATION from the operator's
machine — this lane only makes it possible. **STOP.**

## Decision budget
Ask ONLY about: curated-baseline touches · rule-vs-ruling conflicts · unruled forks. Doc-derived
install/secret mechanics are yours to decide and record. ONE end-of-lane packet.

## What NOT to do
- Do NOT touch anything outside `.devcontainer/`. No scripts/, docs/, protocols/, tasks/.
- Do NOT invent install or secret syntax — every mechanism line derives from a fetched official
  doc, quoted in the commit.
- Do NOT resurrect `containerEnv` ([#554]); do NOT introduce `ANTHROPIC_API_KEY` in any form.
- Do NOT run the smoke yourself; do NOT merge. Commit-and-STOP.
- **Sibling-hook clause:** end-of-session hooks may attribute concurrent sessions' commits to
  this lane — decline with the stated reason.
