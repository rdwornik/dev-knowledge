---
id: "[#939]"
title: "The secrets field -- a contract's Dispatch block can declare a secret without leaking it to the transport"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#939] [P3][S] **The secrets field -- a contract's Dispatch block can declare a secret without leaking it to the transport** - filed by LANE-W4-5 (landing-decisions) per `to-cc/DECLARE-WAVE4A-2026-09-22.md` "Deferred to wave 4b", named there without elaboration. Value: a stage-13 adapter that calls a model on behalf of a lane will eventually need a credential path that is not a plaintext contract field on a Google-Drive transport read by every seat. · Done when: the field's shape, storage and read path are decided (spec before build, ADR-108 §B) and recorded before any code declares it; the pickup lane scopes what "secrets field" names, since this row's own DECLARE source does not. · refs `to-cc/DECLARE-WAVE4A-2026-09-22.md` · kill-candidates: none -- no open row names a contract secrets field
