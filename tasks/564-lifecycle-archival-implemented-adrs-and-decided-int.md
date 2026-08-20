---
id: "[#564]"
title: "Lifecycle archival — a pass over implemented ADRs and decided intakes, plus a check so archival cannot silently lag"
status: open
priority: P2
size: M
theme: "[E4] Decision management"
story: "[S11] Keep the decision corpus navigable and contradiction-aware"
generates: BACKLOG.md
---

- [#564] [P2][M] **Lifecycle archival — a pass over implemented ADRs and decided intakes, plus a check so archival cannot silently lag** — Operator complaint, 2026-08-20, and it re-measures exactly: **`docs/decisions/archive/` holds 2 files** (`ADR-40`, `ADR-52`) against **86 live ADRs, 83 of them `Accepted`**, and **`docs/intake/` holds 34 files with 16 `ACCEPTED` and zero archived** — there is no intake archive at all. Archival is not undefined here, it is simply unrun: `protocols/STANDING_RULINGS.md` **H3** already rules that *an ADR archives at zero inbound references*, which is a mechanical predicate over the live tree. **The row is deliberately two halves and the second is the point:** (a) a one-time pass archiving what qualifies under the existing convention, and (b) a check that surfaces the lag — because a pass without a check is a one-off, and the backlog of un-archived terminal records simply re-accumulates, which is how it reached 2-of-86 without anyone deciding it should. Scope is archival only: **no ADR is superseded, no intake status is flipped, and no decision content is re-opened** by this row. · Done when: every ADR meeting H3's zero-inbound-reference predicate is in `docs/decisions/archive/`, every intake in a terminal decided state is archived per the ADR-98 spine's convention, and an `audit.py` check reports a terminal-state record that has sat un-archived past a stated threshold — with a test that seeds one and sees it surface · refs protocols/STANDING_RULINGS.md H3, docs/intake/README.md, docs/decisions/README.md, ADR-98, ADR-100, ADR-60, #553 · kill-candidates: none — `[#553]` owns the ADR census IN `decisions/README.md` being ungated and wrong, which is the index; this row owns the ARCHIVE, and a correct index over an unarchived corpus is still the state complained about
