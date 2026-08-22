---
id: "[#565]"
title: "`run_id` in telemetry emit — sequenced before the read-path build lane"
status: open
priority: P1
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: environment
generates: BACKLOG.md
---

- [#565] [P1][S] **`run_id` in telemetry emit — sequenced before the read-path build lane** — Ruled 2026-08-20: **this lands BEFORE the read-path build lane**, and the sequencing is the whole content of the ruling. `[#529]` shipped the emit library with the three stage-1 events (`check_run`, `hook_run`, `blocker_fired`) and **zero call sites**; a `run_id` correlating every event emitted by one gate run is cheap to add while the emit surface has no consumers, and expensive afterwards — a read path built against an uncorrelated event stream either re-derives the grouping from timestamps or gets rebuilt. Without it, `check_run` rows from two concurrent gate runs in two worktrees interleave in one WAL store with nothing to separate them, which is exactly the shape this repo already runs (parallel lanes, one shared hooks dir). Scope is the field and its plumbing only — **no consumer, no query, no dashboard**; those are the read-path lane's. · Done when: every stage-1 event carries a `run_id` stable across one gate invocation and distinct across concurrent ones, the schema change lands in the emit library with a test asserting two interleaved runs separate cleanly, and the read-path row is filed AFTER this one rather than beside it · refs #529, #528, docs/audits/2026-08-15-technical-batch-phase1-packet.md, intake #29 Fold A · kill-candidates: none — `[#529]` owns emission and stays open on four legs; this is a schema precondition on the same library and neither subsumes the other · serialize-group: environment · PRE-RULED 2026-08-20, principle level; lane derives details within these: (a) library-first — stdlib logging unless a MEASURED gap on this repo demands structlog, recorded either way; (b) the WAL store path is .gitignore'd (entry ships as a fenced diff, integrator applies); (c) repo root resolved at call time via `git rev-parse --show-toplevel` — safe under linked worktrees, never a hardcoded `_REPO_ROOT`; (d) the [#530] races close test-first: release compares-and-swaps on run_id, never on branch tip, and resolve-once is separated from rev-parse.
