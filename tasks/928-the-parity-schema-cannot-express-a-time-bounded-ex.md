---
id: "[#928]"
title: "The parity schema cannot express a time-bounded expectation -- settings-deny-and-point INVERSE encodes BUILD-MODE rule 8, which expires 2026-11-18, and nothing will flag it"
status: open
priority: P1
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#928] [P1][S] **The parity schema cannot express a time-bounded expectation -- settings-deny-and-point INVERSE encodes BUILD-MODE rule 8, which expires 2026-11-18, and nothing will flag it** - `f610b798` (2026-09-19) inverted `ecosystem/parity-surfaces.yaml` row `settings-deny-and-point` from hub MUST to hub INVERSE, so re-wiring the PreToolUse `deny_and_point` block without a ruling fails `fleet_parity`. The basis is BUILD-MODE rule 8 ("Refusals ONLY at git boundaries"), and BUILD MODE expires 2026-11-18 (`protocols/BUILD-MODE.md`). The expiry lives only in a YAML comment. MEASURED 2026-09-19: the parity schema has NO row-level expiry. `scripts/fleet_parity.py` time-boxes only waiver DECLARATIONS (`.methodology.yaml` `review_date` -> `advisory-rewarn`), and an INVERSE row is non-waivable by loader refusal (a necessary condition is never waivable). The one self-invalidating expectation is ADR-102's `gate_rev_ahead`, which covers pinned revs only. So after 2026-11-18 the row keeps asserting a rule whose basis has lapsed, with no finding, and an invented `expires:` key would be read by nothing. Same shape as `[#927]`: an emergency order marked TEMPORARY on 2026-09-17 has outlived its emergency because nothing expires it. A temporary measure is only safe when its expiry is a mechanism · Done when: a parity row can carry an expiry the checker READS (schema + loader + `fleet_parity.py` verdict), and after that date the row is reported for re-ruling (a named, visible finding -- not silent continuation, not silent removal); `settings-deny-and-point` carries `2026-11-18` in that field; a RED-first test shows an expired row surfaces and an unexpired one does not; decided as a gate change by ruling, not as a quick fix · refs `ecosystem/parity-surfaces.yaml` (`settings-deny-and-point`), `scripts/fleet_parity.py`, `protocols/BUILD-MODE.md`, `f610b798`, `f3eba9b2`, `[#927]`, `[#926]`
