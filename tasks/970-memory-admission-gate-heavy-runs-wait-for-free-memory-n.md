---
id: "[#970]"
title: "Memory admission gate: heavy runs wait for free memory; `-n` is computed, not hand-set"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#970] [P1][M] **Memory admission gate: heavy runs wait for free memory; `-n` is computed, not hand-set** - D7: `resource_lifecycle.py` reads no free-memory figure before a dispatch; `-n` has been hand-set to 2 (sometimes 4) all window, `-n auto` OOM-killed 5 full-suite attempts on 09-07/08, and the box saw 8+ reaper kills plus 2 lanes lost to OOM this window (`docs/audits/2026-09-23-technical-verify-time.md` §Memory, confirmed `docs/audits/2026-09-23-technical-audit-crosscheck.md` C12) · Done when: a memory gate (psutil + filelock, inside the organs the harness already runs) blocks a heavy pytest/gates invocation until free memory clears a threshold, and derives `-n` from free memory rather than a hand-set constant; a witness run under a synthetic low-memory condition waits rather than OOM-killing · implements: ADR-120 · refs `scripts/resource_lifecycle.py`, `pyproject.toml`, `docs/audits/2026-09-23-technical-verify-time.md` · kill-candidates: none -- no open row derives -n from measured free memory; LANE-5A-3 (lane-memory-gate) is this window's own build of this mechanism, tracked on its own contract rather than this backlog row
