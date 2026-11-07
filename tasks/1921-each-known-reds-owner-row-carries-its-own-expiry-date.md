---
id: "[#1921]"
title: "Each known-reds owner row carries its own expiry date, so the registry has no single clock"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1921] [P1][S] **Each known-reds owner row carries its own expiry date, so the registry has no single clock** - On 2026-11-07 every entry of `logs/KNOWN-REDS-REGISTRY.json` (40 members, 41 + 40 per-OS, one hook entry; 12 owner rows plus `[#1866]` and `[#1020]`) expired on the same day, 2026-11-09, because the last extensions re-dated the whole registry to one date (KR-1, RATIFICATION-2026-10-24), and `load_registry` refuses the whole registry once any entry is past its date (`scripts/known_reds.py:276`), so one date stopped every landing at once and the plan of the day believed a single row owned the clock (to-browser/DIGEST-KR-664-ANALYSIS-2026-11-07.md section 4). The warn-ahead half is `[#1445]` (a dated item warns 3 days before its date, naming its owner); this row is the other half named in to-browser/RATIFICATION-2026-11-07.md Amendment 1 D3: the date per owner row. · touches: `scripts/known_reds.py`, `tests/test_known_reds_extend.py` · kill-candidates: none - `[#1445]` owns the warning, not the per-row date · refs `scripts/known_reds.py`, `[#1445]`, `[#1889]`, to-browser/DIGEST-KR-664-ANALYSIS-2026-11-07.md · Done when: RED first - `known_reds.py extend` refuses a re-date that would give entries of two different owner rows the same new expiry unless the ratification row names that date for each of those rows, and a listing (`known_reds.py` subcommand) prints each owner row with its entries' dates and days left; a re-date of one owner row's entries moves no other row's; the lane-branch CI run is green outside known reds · decided-by: operator, to-browser/RATIFICATION-2026-11-07.md Amendment 1 D3 · source: to-browser/DIGEST-KR-664-ANALYSIS-2026-11-07.md section 4
