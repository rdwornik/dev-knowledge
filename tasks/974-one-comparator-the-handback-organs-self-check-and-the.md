---
id: "[#974]"
title: "One comparator: the handback organ's self-check and the integrator's call the same function"
status: open
priority: P1
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#974] [P1][S] **One comparator: the handback organ's self-check and the integrator's call the same function** - D11: the handback organ's self-check disagreed with the integrator's own check twice this window (false negatives), because each is a separate implementation of what should be one comparison · Done when: the handback organ and the integrator both call one shared comparator function (not two independently-written checks); a regression test asserts both call sites produce identical verdicts on the same input · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-window-defects.md`, `docs/audits/2026-09-22-technical-lane-handback-organ-sol-adversary.md` · kill-candidates: none -- no open row unifies the two comparator implementations; LANE-5A-4 (lane-handback-fixes) is this window's own build of this mechanism
