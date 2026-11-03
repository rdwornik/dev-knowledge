---
id: "[#979]"
title: "Path layer reads HARNESS_DRIVE_ROOT/HARNESS_PROMPTS_SUBDIR -- no direct env-var reads outside it"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#979] [P2][S] **Path layer reads HARNESS_DRIVE_ROOT/HARNESS_PROMPTS_SUBDIR -- no direct env-var reads outside it** - D20: `HARNESS_DRIVE_ROOT` and `HARNESS_PROMPTS_SUBDIR` are already set as globals (ENV review, `to-cc/PLAN-WAVE5-2026-09-23.md` §2 item 4), but the remaining half of the mechanism -- a path layer that is the SOLE reader of those variables, with every one of the 119 read sites going through it -- is not built · Done when: a path-layer module is the only code that reads `HARNESS_DRIVE_ROOT`/`HARNESS_PROMPTS_SUBDIR`; every other read site (119 measured at 09-23) calls the module instead of `os.environ` directly; a grep-based test asserts 0 direct reads outside the module · implements: ADR-120 · refs `to-cc/PLAN-WAVE5-2026-09-23.md`, `docs/audits/2026-09-23-technical-window-defects.md` · kill-candidates: none -- no open row centralizes the 119 read sites behind one module
