---
id: "[#912]"
title: "main is RED on its own -- 45 live-state tests fail independently of every lane merged in night wave 2, with no owner"
status: open
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
implements: "night wave 2 integrator ruling 2026-09-19"
generates: BACKLOG.md
---

- [#912] [P1][M] **main is RED on its own -- 45 live-state tests fail independently of every lane merged in night wave 2, with no owner** - During night-wave-2 integration pass #2 (2026-09-19), every lane's impacted-test failures were re-run on the lane's base commit. The same live-state tests fail on `14d273fb` (L3's base) and on `233294c0` (main after L5): 45 on each re-run set. They are pre-existing, and none is attributable to L3, L4 or L5. The families: `tests/test_prompts_guard_hook_wiring.py` (17), handoff probes (`test_gen_handoff` dogfood/epic/suffixed bundles, `test_handoff_modes`), audit health (`test_audit::test_health_ok_with_registered_repo`, `test_health_stays_ok_with_na_status`, `test_check_fleet_parity_green_on_live_repo`), conductor wiring (`test_conductor::test_the_session_start_hook_is_wired_in_settings_json`), the graph-spine commit tier (`test_graph_spine_commit_tier`, 4), canonical-docs derived legs, live-corpus baselines (`test_proof_layer`, `test_consumer_at_landing`), and corpus/header tests (`test_normalize_headers`, `test_toc`, `test_validate_doc_rot`). **This is the number that matters more than any lane.** While main is red, "green impacted tests" at merge can only mean "no new red", which a paired baseline run has to prove every time · Done when: `uv run --locked pytest -n 6` over those 45 node ids is green on main, or each remaining failure has a named owner row and a disposition; and the integrator's merge check is plain "impacted set green" again, with no paired-baseline subtraction · implements: night wave 2 integrator ruling 2026-09-19 · refs `C:\Users\1028120\Downloads\to-browser\INTEGRATOR-wave2-pass2-2026-09-19.md`, JOURNAL 2026-09-19 (z)/(ac), `tests/test_prompts_guard_hook_wiring.py`, `tests/test_graph_spine_commit_tier.py`, `tests/test_gen_handoff.py`
