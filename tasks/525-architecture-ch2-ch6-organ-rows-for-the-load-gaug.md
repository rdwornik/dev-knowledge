---
id: "[#525]"
title: "ARCHITECTURE.md Ch2/Ch6 organ rows for the load-gauge digest section — owed since W2, integrator-collected"
status: closed
priority: P2
size: S
theme: "[E5] Canonical-file integrity"
story: "[S13] Keep canonical files accurate"
serialize-group: architecture
generates: BACKLOG.md
---

- [#525] [P2][S] **ARCHITECTURE.md Ch2/Ch6 organ rows for the load-gauge digest section — owed since W2, integrator-collected** — `[#270]`'s operator-load gauge (`fleet_health.py`'s `[load]` block + `logs/OPERATOR-LOAD.csv`) closed 2026-08-11 (`7e4d503e`) with `ARCHITECTURE.md` explicitly out of scope for the landing lane: batch-4 §4.2 step 6 states *"`ARCHITECTURE.md` is OUT OF SCOPE for this lane under §5.2's recommendation — the owed Ch2/Ch6 row is collected by the integrator"* (`docs/audits/2026-08-10-technical-batch-4-execution-plan-draft.md:300-301`), and the debt is recorded twice in `JOURNAL.md` (W2 close: *"Still owed from W2: the `ARCHITECTURE.md` Ch2/Ch6 organ row for the load-gauge digest section"*, :546; W1 register-hygiene entry: *"`ARCHITECTURE.md` Ch2/Ch6 row for the new digest section, owed per §4.2 step 6"*, :1074) and again on the frozen roadmap (*"Ch2/Ch6 organ rows owed"*, `docs/audits/2026-08-12-technical-roadmap-north-star-frozen.md:30`). No integrator lane has yet landed either row; live-checked 2026-08-13: neither the Ch2 organ table nor the Ch6 verification-mesh table names the `[load]` block or `OPERATOR-LOAD.csv`. · Done when: Ch2's organ table (`ARCHITECTURE.md` §"Organ map") carries a row for the `[load]` digest section / `OPERATOR-LOAD.csv` writer with a live locator, AND Ch6's verification-mesh table (§"Verification mesh and decision flow") reflects the load-gauge as a nightly/funnel-layer signal, each claim declarative and locator-backed, `silent_rule_ratchet` unmoved (<= 441) · refs `scripts/fleet_health.py`, `logs/OPERATOR-LOAD.csv`, `ARCHITECTURE.md` Ch2/Ch6, `[#270]`, `docs/audits/2026-08-10-technical-batch-4-execution-plan-draft.md:300-301`, `docs/audits/2026-08-12-technical-roadmap-north-star-frozen.md:30` · kill-candidates: none — no open row owns the Ch2/Ch6 organ-table entries for the load-gauge digest section · serialize-group: architecture
