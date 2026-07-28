---
id: "[#294]"
title: "`validate_backlog` deploy-carrier + `--path` de-hardcode"
status: deferred
priority: P3
size: M
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#294] [P3][M] `validate_backlog` deploy-carrier + `--path` de-hardcode (ai-council pilot G1+G2) — the v1.2.0 manifest ships NO `validate_backlog` component (a consumer gets no in-repo story-map validator; ai-council's #281 "green in-repo" is attestable only via the hub validator run against a scratch copy), AND `validate_backlog.py` hardcodes `BACKLOG = …parent.parent / "BACKLOG.md"` with no CLI arg, so it can't be pointed at a consumer by argument. Pair: a consumer-runnable validator needs BOTH a `--path`/`--repo` arg AND a deploy carrier. Kill-candidate (carried from the gap-note): if the story-map is only ever authored/checked hub-side, per-consumer validation may be unnecessary — decide carrier-vs-hub-only before building. · Done when: `validate_backlog.py` takes a `--path`/`--repo` target AND either a carrier ships it to a consumer (validated green in-repo) or hub-only-by-design is recorded with a reason · refs scripts/validate_backlog.py, deploy/manifest-v1.2.0.yaml, #281, #237 · serialize-group: audit-py · DEFER — peg: post-Wave-1 mesh-portability epic
