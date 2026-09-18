---
id: "[#892]"
title: "A seat ordered sonnet ran Opus and nothing refused -- ordered is not ran for an attended seat"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
implements: "DECLARE-BATCH-AC-CLOSE-2026-09-18"
generates: BACKLOG.md
---

- [#892] [P2][S] **A seat ordered sonnet ran Opus and nothing refused -- ordered is not ran for an attended seat** - Batch AC's primary freeze seat was ordered `sonnet` for S1-S5 and ran Opus, which it disclosed itself (`to-browser/HANDBACK-batch-AC-consolidated.md` L-freeze item 1). It was the largest session of the night and it ran against the operator's first constraint. Priced by the existing organ (`lane_cost.py lane --slug ac-night-freeze`): **USD 15.06 on claude-opus-5 over 124 calls, 49 % of batch AC's USD 30.59 across seven sessions.** `[#885]` makes a lane CONTRACT's declared model the model that runs; an attended seat has no contract, so no freeze-time resolution and no verify-at-run leg reaches it. The only record is the seat's own honesty · Done when: a seat's ordered model is recorded where a verifier reads it, and a ran-model that differs from it is refused at the first tool call or surfaced as a named finding in the seat's close packet. RED-first witness: a seat ordered `sonnet` whose transcript carries `claude-opus-5` produces the finding with no human reading the transcript · implements: DECLARE-BATCH-AC-CLOSE-2026-09-18 · refs `to-cc/DECLARE-BATCH-AC-CLOSE-2026-09-18.md` §6 W1, `to-browser/HANDBACK-batch-AC-consolidated.md` (L-freeze), `scripts/lane_cost.py` (`seat`, the per-model reader), `scripts/seat_registry.py`, `[#885]` · kill-candidates: `[#885]` -- if its verify-at-run leg is widened from contracts to seats at intake, this row folds into it
