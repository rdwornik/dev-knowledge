---
id: "[#1012]"
title: "A dispatcher-held producer shell must run as its own session or a detached process, not a bg shell the reaper can kill"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#1012] [P1][M] **A dispatcher-held producer shell must run as its own session or a detached process, not a bg shell the reaper can kill** - WAVE5A finding: the Copilot primary for `lane-graph-stage-edge` (`run-lane-copilot.ps1`, launched as a background shell of the dispatcher) was killed by Claude Code's low-memory reaper ~4 min in, mid-read, 0 commits, Copilot credits partly spent with no output; the script refuses a re-run once its branch exists, so the dispatcher fell back to a Sonnet SUBSTITUTION (`to-browser/SESSION-dispatcher-wave5a-2026-09-23.md`, 07:23-07:24Z) · Done when: a producer a dispatcher would otherwise hold as its own background shell instead runs as a detached process or its own session (the pattern `[#962]`'s fleet-health producer already specifies: own clean checkout, process tree ends with it), so the reaper's kill scope never includes it; a witness run under the same memory-pressure condition leaves the producer alive · implements: ADR-120 · refs `docs/audits/2026-09-24-technical-digest-wave5a.md` (§4 Reaps, this lane's general landed provenance), `to-browser/SESSION-dispatcher-wave5a-2026-09-23.md` (07:23-07:24Z entries -- the Copilot-reap incident itself; a Drive transport document, not retained in this repo), `to-cc/run-lane-copilot.ps1`, `[#962]` (the detached-producer pattern this row generalizes to a non-Claude producer), `[#808]` (the general hook-timeout-bound row; this row is about a dispatcher-held shell, not a hook) · kill-candidates: none -- no open row bounds a dispatcher-held producer shell against the reaper
