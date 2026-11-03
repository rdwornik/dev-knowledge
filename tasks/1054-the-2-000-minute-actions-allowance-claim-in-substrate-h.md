---
id: "[#1054]"
title: "the 2,000-minute Actions-allowance claim in substrate-heartbeat.yml is the Free-tier figure, uncorrected for GitHub Pro's 3,000"
status: closed
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1054] [P3][S] **the 2,000-minute Actions-allowance claim in substrate-heartbeat.yml is the Free-tier figure, uncorrected for GitHub Pro's 3,000** - `.github/workflows/substrate-heartbeat.yml:180` states "2000-minute included allowance is a PRIVATE-repository entitlement" as a live fact; this account is GitHub Pro (RATIFICATION-2026-09-25 R5: "the personal account `rdwornik` (GitHub Pro)"), whose included Actions minutes are 3,000, not 2,000 -- the file names the Free-tier number without the Pro correction. Commit `6e9b7a4f` (2026-09-15) is the origin of the framing being corrected. Historical `docs/audits/`/`JOURNAL.md`/`LESSONS.md` occurrences of "2,000" are immutable narrative, not corrected by this row. · Done when: `git grep -n "2,000\|2000-minute\|2,000-minute"` over living (non-immutable) files returns no claim stating 2,000 as this account's Actions allowance without noting the Pro correction to 3,000 · refs `.github/workflows/substrate-heartbeat.yml:180`, commit `6e9b7a4f`, `to-browser/RATIFICATION-2026-09-25.md` R5 · kill-candidates: none -- no open row corrects this claim · **CLOSED 2026-11-03** — evidence 432d0d1a295a4c7a544439c5ad02fac6332b5462
sweep-close: legacy-sweep · witnesses checked=K1,K2,K3 absent=K1,K2,K3 · filed 2026-09-25 before 2026-10-01; no KEEP witness (K1 protected, K2 alive in code, K3 agreed LINE P1/P2) holds
