---
id: "[#550]"
title: "Intake #14's ruled SIEM requirements outlived the ruling that shelved them, with no record of which half survives"
status: open
priority: P3
size: S
theme: "[E4] Decision management"
story: "[S11] Keep the decision corpus navigable and contradiction-aware"
generates: BACKLOG.md
---

- [#550] [P3][S] **Intake #14's ruled SIEM requirements outlived the ruling that shelved them, with no record of which half survives** — `docs/intake/2026-07-12-siem-requirements-ruled-pack.md` carries `status: ACCEPTED`, `disposition: deferred`, `trigger: "#328 build"`, `consumers: "#328 build (charter requirements)"`, decided by *"the 2026-07-12 A0 seal ruling (the RULED consolidation)"*. **Two facts collide.** (a) [#328] does not exist (verified 2026-08-17), so the named consumer departed. (b) `BACKLOG.md`'s W-wave **CONSIDERED + REJECTED** line already records *"SQL/SIEM now (premature per intake #14 + S8)"* — the *timing* was declined **citing this very document**, while the ruled requirements themselves were never dispositioned. The pack is therefore simultaneously the authority that justified a rejection and an ACCEPTED document with no live carrier, and nothing states which clauses are shelved-but-live versus dead. One clause HAS been dispositioned and the row records it so the work is not redone: W4's **R7** was ruled 2026-07-26 (*"collector + reporters now, SQLite shelved"*) on the strength of this pack's own least-commitment clause (store/viewer class is a Phase-A build decision, *"not settled here"*) — one clause of many. · Done when: each ruled requirement clause in intake #14 is marked shelved-with-its-reason, live-and-carried-by-a-named-row, or dead, and the document's `trigger:` no longer names a departed id · refs docs/intake/2026-07-12-siem-requirements-ruled-pack.md, BACKLOG.md (the W-wave "CONSIDERED + REJECTED" line), #548, #549, #322 · kill-candidates: none — the R7 ruling dispositioned exactly one clause (the store class) and no open row owns the remainder · source: docs/audits/2026-08-17-technical-batch-7a-lane-b-contract.md step 2 (intake sweep), building on docs/audits/2026-08-16-census-nb6-archive-sweep.md §1.3
