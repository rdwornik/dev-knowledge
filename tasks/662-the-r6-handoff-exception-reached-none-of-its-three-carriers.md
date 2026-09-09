---
id: "[#662]"
title: "The R6 handoff-exception rule reached none of the three carriers it was written for"
status: open
priority: P2
size: S
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
generates: BACKLOG.md
---

- [#662] [P2][S] **The R6 handoff-exception rule reached none of the three carriers it was written for** — the ruling says the outgoing handoff is the LAST act of a window, starting only after the integrator reports the queue drained with every batch closed and no linked worktrees, and that a batch close packet is a `/handoff` preflight precondition. It names three homes for that text and the file states in its own §5 that none was written, routing the gap to the unowned list. Measured on this tree: a grep for the rule's own verbatim wording across `protocols/HANDOFF_PROCESS.md`, `protocols/OPERATOR-INTERFACE.md` and `.claude/commands/handoff.md` returns nothing — **0 of 3**. The error it comes from cost the operator an hour, late at night · Done when: the rule text is present in all three homes, 0 of 3 becomes 3 of 3, and the wrap-sequence line reads the same in each · refs DECLARE-R6-HANDOFF-EXCEPTION §§2-5, the unowned list on the transport, `[#642]` · source: DECLARE-R6-HANDOFF-EXCEPTION §5, filed by batch V lane V-4
