---
id: "[#1344]"
title: "Two graph-spine lock tests flake on the windows runner"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1344] [P2][S] **Two graph-spine lock tests flake on the windows runner** - DCT D11. `tests/test_graph_spine.py::test_an_expired_lock_is_broken_so_a_dead_builder_never_wedges_the_store` ("the breaker did not take the lock") was red on 21 of 35 windows runs with same-sha disagreement (2e7fa5f2, a38b6faf); `::test_an_overrun_builder_does_not_release_its_SUCCESSORS_lock` failed on 3 of the 6 recent runs read for this row. No commit made either red -- the cause is lock timing on the runner, so the registry attributes them `flaky` (owner `[#664]`, expiry 2026-10-17). Not registered: `tests/test_transport.py::test_concurrent_appends_to_the_same_destination_serialize_without_interleaving` (1 of 6, a PermissionError) and `tests/test_worktree_import_proof.py::test_end_to_end_fail_when_the_package_does_not_resolve` (1 of 6) -- seen once each, so they stay visible as regressions if they recur · Done when: 10 consecutive green windows runs of both lock tests, shown by the run ids, and the two registry entries are removed · touches: `tests/test_graph_spine.py`, `logs/KNOWN-REDS-REGISTRY.json` · kill-candidates: none -- [#664] wires the spine and does not track these two tests · refs `tests/test_graph_spine.py`, `logs/KNOWN-REDS-REGISTRY.json`, [#664], `docs/audits/2026-10-03-codex-foundation-1-honest-green.md` · source: batch FOUNDATION lane foundation-1-honest-green (2026-10-03)
