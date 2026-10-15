---
id: "[#1577]"
title: "Seat-authored transport files carry `by:`, live in the right folder, and a dispatcher never writes STATE into the repo checkout"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1577] [P2][S] **Seat-authored transport files carry `by:`, live in the right folder, and a dispatcher never writes STATE into the repo checkout** - `SESSION-*`, `LANE-END-*`, DISPATCHER and INTEGRATOR files lack a flush-left `by:` so `transport_lint` fails (to-browser/SESSION-integrator-bu-2026-10-15.md:44-46,69-70,96-97); `to-cc/LANE-ikea-orders-*` are `wrong-folder` with no R59 proof; `INDEX-ARCHIVE.md` is `unknown-kind`; the BU dispatcher wrote `to-browser/STATE-bu-2026-10-15-dispatcher.json` into the primary checkout (to-browser/SESSION-integrator-bu-2026-10-15.md:47); `STATE-BATCH-NV.md` reads `CLOSED 23:52` with no date · Done when: RED first: a test generates each seat file kind and asserts `transport_lint` is clean on it; a second asserts the dispatcher STATE path resolves under the transport dir, never the git toplevel; a third asserts a STATE close line carries a date; fails on 97bcd374 · touches: `scripts/transport.py`, `scripts/transport_lint.py`, seat templates, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1439]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
