---
id: "[#1918]"
title: "The handoff Plan row admits a plan whose name says superseded before its date"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1918] [P2][S] **The handoff Plan row admits a plan whose name says superseded before its date** - `scripts/handoff_state.py::row_plan` reads "the newest non-superseded `to-cc/PLAN-*.md`" through `_live_transport_docs`, whose filter `_SUPERSEDED_RE = re.compile(r"-v\d+-superseded\.md$")` (`scripts/handoff_state.py:285`) drops only the `-vN-superseded.md` shape; a name such as `PLAN-NEXT-r3-draft2-superseded-2026-10-31.md`, which says superseded before its date token, passes as live, and the 2026-11-05 bundle's Plan row named it as the newest non-superseded master plan (to-browser/DIGEST-ONBOARDING-ANSWERS-TA48-2026-11-07.md section B item 3). Candidate (b) of to-browser/RATIFICATION-2026-11-07.md item 5; no open row held it (phase A, to-browser/DIGEST-KR-664-ANALYSIS-2026-11-07.md section 6). · touches: `scripts/handoff_state.py`, `tests/test_handoff_state.py` · kill-candidates: none - no open row owns the Plan row's superseded filter · refs `scripts/handoff_state.py`, to-browser/DIGEST-KR-664-ANALYSIS-2026-11-07.md · Done when: RED first - a transport fixture holding `PLAN-X-superseded-2026-10-31.md` (a master by its head) and an older live master makes `row_plan` name the older live master, and a `-v2-superseded` sibling stays excluded as today; then the filter treats `superseded` as a whole name segment wherever it stands; the lane-branch CI run is green outside known reds · decided-by: operator, to-browser/RATIFICATION-2026-11-07.md item 5 and Amendment 1 D1 · source: to-browser/DIGEST-KR-664-ANALYSIS-2026-11-07.md section 6 (b)
