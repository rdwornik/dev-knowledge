---
id: "[#907]"
title: "Spend is not measured by seat kind, so cost work targets the lanes while the money is in the seats"
status: open
priority: P1
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
implements: "DECLARE-BATCH-AC-NOT-CLOSED-2026-09-18"
generates: BACKLOG.md
---

- [#907] [P1][S] **Spend is not measured by seat kind, so cost work targets the lanes while the money is in the seats** - re-derived by the integrator on 2026-09-18 with `scripts/lane_cost.py lane --slug <slug> --batch AC`: batch AC's seven lane sessions cost **USD 30.59** in total (claude-opus-5 15.06, the freeze seat alone; claude-sonnet-5 15.53, the six lanes; rates as_of 2026-06-24). `to-cc/DECLARE-BATCH-AC-NOT-CLOSED-2026-09-18.md` §2 sets that against roughly USD 8,721 for the week (the architect's figure, not re-derived here): the cost is NOT in the lanes but in the large seat sessions, and the primary session was ORDERED sonnet for S1-S5 and RAN opus ([#892]). The declare therefore WITHDRAWS the earlier claim that the non-Claude launch path "is the only item that moves 99.47 %" -- the lever it names is seat model discipline, which is a hypothesis until spend is measured by seat kind. The organ half exists: `lane_cost.py seat --session <id> --since --until` prices an attended seat by session id and window (`a-seat-cost-is-keyed-by-session-id-and-a-window-never-a-directory`), and `lane` prices a lane; nothing groups the result by SEAT KIND · Done when: one committed table gives spend per seat kind -- architect, primary, dispatcher, integrator, lane -- per model, over one named window, each figure with its instrument and session ids; any seat kind that cannot be priced from this box is named with the reason (the browser architect seat leaves no local Claude Code transcript) rather than estimated; and the table states what share of the window's total the lanes are. No cost-reduction work is planned before this lands · implements: DECLARE-BATCH-AC-NOT-CLOSED-2026-09-18 · refs `docs/audits/2026-09-17-technical-batch-ac-close-packet.md` §5, `scripts/lane_cost.py` (`seat`, `lane`, `report`), `[#893]` (receipts at integration), `[#892]` (ordered != ran), `[#833]` (the seat registry holds each seat's role) · kill-candidates: none -- [#893] makes the integrator record lane receipts; this asks for the seat-kind breakdown, which no row measures
