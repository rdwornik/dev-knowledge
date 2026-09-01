---
id: "[#615]"
title: "MODEL ATTRIBUTION — a model+version signature trailer on every model-authored commit"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#615] [P2][M] **MODEL ATTRIBUTION — a model+version signature trailer on every model-authored commit** — **the enabling row for a telemetry series that is underivable today.** DB-1 enumerated the live history stores and reported **per-model change quality as ABSENT, in the legend, with the reason**: nothing records which model authored a commit, so the series cannot be computed and was **not proxied**. This row makes it derivable — a model+version trailer, **hook-enforced at commit-msg** like the `[#id]` and `kill-candidates:` gates already are, consumed by the telemetry store. **Two design questions the arc rules rather than assumes:** what counts as *model-authored* (a session flag, or the absence of a human co-author), and what a **missing** trailer does (BLOCK like `backlog-id-on-close`, or WARN like `coherence-nudge`) — the posture decides whether the series is complete or indicative, and **a partial series is worse than an absent one because it looks whole.** **Fence:** intake #50 stays its own arc; this row produces the *signal*, not the store. · Done when: a commit-msg hook asserts the trailer and its posture is ruled; the shape is single-sourced; the store consumes it; DB-1's per-model panel renders data instead of `ABSENT` · refs docs/intake/2026-08-26-tech-cost-and-delivery-telemetry.md, docs/audits/2026-08-29-technical-nb2-n-packet.md, `docs/audits/2026-09-01-census-atlas-r1-def-usage-ledger.md` (**the measurement that makes this row's premise a fact**: 31 lanes across batches D—F, credits recorded ZERO, and attribution named UNDERIVABLE rather than missing — *"nothing in a commit says which model authored it"*; it also records that all 31 ran on one model, so the routing series the trailer would enable currently has no variance to show), `docs/audits/2026-09-01-technical-atlas-r1-layer-graph.md` (the `tests/` and `ecosystem/` layers the governed graph still owes) · source: intake #50
