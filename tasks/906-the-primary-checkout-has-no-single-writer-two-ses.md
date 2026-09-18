---
id: "[#906]"
title: "The primary checkout has no single writer -- two sessions committed on it concurrently during the batch AC close, and nothing refused either"
status: open
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
implements: "operator decision 3, 2026-09-18 (batch AC close)"
generates: BACKLOG.md
---

- [#906] [P1][M] **The primary checkout has no single writer -- two sessions committed on it concurrently during the batch AC close, and nothing refused either** - on 2026-09-18 the integrator seat (bound `integrator AC` in the seat registry) was walking the batch AC merge queue on the primary checkout when a second session merged `worktree-handback-contract-row` there as `bb710468`, between the integrator's M5 (`939e49ed`) and M6 (`ab5f6245`). Both sessions allocated JOURNAL letter (f), so `main` carries two `2026-09-18 (f)` entries; the integrator's (g) "Next" line then listed [#891] as still waiting although it had landed; and the integrator merged M6 onto a tree that had moved under it without noticing. AGENTS.md states "one checkout = one committing session" and PLAYBOOK Ch8 says JOURNAL letters are allocated at integration by the primary's single writer -- both are PROSE, and the operator ruled 2026-09-18 that this is "a mechanism, not an etiquette request". The seat registry already knows who the bound integrator is ([#833]); nothing consults it before a commit on the primary. Adjacent, not duplicate: [#739] (the Stop hook reads the tree but not its authorship), [#748] (a lane whose worktree redirects to the primary) · Done when: while a batch manifest is `status: open` and an integrator seat is bound to that batch, a commit or merge on the PRIMARY checkout by any session other than that integrator is refused mechanically, the refusal names the holding seat, and the mechanism carries a counter (refusals fired, over what window) per the standing rule that a gate without one is removed at its next review. Outside an open batch the primary behaves as today. Witness: two sessions, one bound integrator; the unbound one's commit on the primary is refused, the integrator's is not · implements: operator decision 3, 2026-09-18 (batch AC close) · refs `docs/audits/2026-09-17-technical-batch-ac-close-packet.md`, JOURNAL 2026-09-18 (f)/(f)/(g) and the correction entry, `scripts/seat_registry.py`, `[#833]`, `[#739]`, `[#748]` · kill-candidates: none -- no open row makes the primary a single-writer resource; [#739] and [#748] are adjacent, not the same
