---
id: "[#1420]"
title: "The next rulings-landing run lands R88, the operator's Codespace sign-in rulings of 2026-10-06"
status: closed
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1420] [P2][S] **The next rulings-landing run lands R88, the operator's Codespace sign-in rulings of 2026-10-06** - The operator ruled R88 to the B2-W1 integrator seat (cycle 17) on 2026-10-06: (a) Copilot in the Codespace via the `COPILOT_GITHUB_TOKEN` secret is accepted as the laptop-equivalent sign-in; (b) the retired gemini CLI is removed from the registry's expectations (provider google's `cli` set to null) so C1 stops requiring it; (c) agy is BLOCKED-AUTH in the Codespace, with one OPERATOR-ACTION line and a follow-on W2 lane to find a headless method; (d) no refresh probe that could sign the laptop out is run -- the expiry check is relied on, and a lost laptop sign-in is one OPERATOR-ACTION to re-login. The ruling lives only in the integrator receipt, so no in-repo surface carries it; the same run also owes R80, R81, the ADR-121 C6 acceptance and R82-R86 · Done when: (1) `protocols/STANDING_RULINGS.md` carries R88 (a)-(d) with its verbatim source (the receipt's OPERATOR-RULING R88 line, or the ratification file the seat moves it to); (2) `decision_coverage.py rulings` passes with R88 present · kill-candidates: none -- folded into [#1446] by lane `b2w2-rulings-landing` (batch B2-W2): section AS of `protocols/STANDING_RULINGS.md` lands R88 (a)-(d) with its verbatim source and R87 beside it, both carried by [#1423], and the rulings gate passes with R80-R92 found; the integrator closes this row · refs `protocols/STANDING_RULINGS.md`, `scripts/decision_coverage.py`, `[#1335]`, `[#1379]` · source: B2-W1 integrator receipt `to-browser/SESSION-integrator-b2-w1-2026-10-04.md` (OPERATOR-RULING R88, cycle 17, 08:39Z) · **CLOSED 2026-10-10** — evidence ed8c13875504574bdc1cb2f7be09ad733ea048da · CI run 38004183484 (success) · tests tests/test_standing_rulings_sources.py::test_the_gate_passes_with_section_as_under_a_simulated_b2_w2_close
