---
id: "[#947]"
title: "LiteLLM behind the stage-13 adapter -- one provider interface, not four bespoke ones"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#947] [P2][M] **LiteLLM behind the stage-13 adapter -- one provider interface, not four bespoke ones** - filed by LANE-W4-5 (landing-decisions) per `to-cc/DECLARE-WAVE4A-2026-09-22.md` "Deferred to wave 4b". Value: ADR-120's stage-13 adapter needs one result shape (output, cost, cap kind, model requested/served, stop reason, tokens) across dispatch, the Claude Agent SDK and `codex exec`; LiteLLM is the library-first candidate for that unification and was deferred until the adapter's own shape landed (ADR-120 D7 step 5). · Done when: LiteLLM is trialed behind the ADR-120 adapter interface for at least Claude and Codex, and a MEASURED adopt/reject verdict is recorded -- an adapter never claims what a provider does not report (ADR-120 "Adapter contract"). · refs `to-cc/DECLARE-WAVE4A-2026-09-22.md`, `docs/decisions/ADR-120-the-spine-is-the-whole-loop.md` (D7 step 5, "Adapter contract") · kill-candidates: none -- no open row trials LiteLLM
