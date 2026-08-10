---
id: "[#419]"
title: "We run routines whose output nobody consumes"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#419] [P2][M] **We run routines whose output nobody consumes** — the nightly conformance routine emits a digest nightly and nobody reads it. **1st instance:** six `claude/conformance-*` branches (07-21…-26) sat unread; their one High finding was fixed on main (`037d9f08`) by a session that never opened the branch that found it; the ADR-92 half went unfixed as a result. **2nd instance, IDENTICAL WIDTH:** six digests (08-03…08-09; 08-06 no branch) unmerged while main's stream stops at 08-02 — the manual absorb merge last ran `24882f8c`; ADR-105 §1 named it in advance; evidence `docs/audits/2026-08-10-verification-ruled-dispositions-and-digest-gap.md` §2. Operator's framing: how routine output reaches a decision, NOT branch cleanup (touch no branch). Rule + gate landed 07-26 (ADR-105); coverage pegged to [#426]. STAYS OPEN. · Done when: every standing routine has a named consumer and a consumption path, and unconsumed output is surfaced rather than silently accumulating · refs #270, #271, #348, #409, #410, #411, ADR-80, the five conformance branches · kill-candidates: none — #270 gauges operator LOAD, not whether output is ever read · serialize-group: settings-json
