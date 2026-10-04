---
id: "[#1350]"
title: "The transport append lock reads a Windows delete-pending file as an error, and one test flakes on it"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1350] [P2][S] **The transport append lock reads a Windows delete-pending file as an error, and one test flakes on it** - `scripts/transport.py` `_DestinationLock.__enter__` (`:193`) retries only on `FileExistsError`; on Windows an `os.open(O_CREAT|O_EXCL)` that meets a lock file another thread is deleting raises `PermissionError`, which escapes `append()`. `tests/test_transport.py::test_concurrent_appends_to_the_same_destination_serialize_without_interleaving` fails on it: 63 of 300 runs of the real test body in a local Windows loop (all `PermissionError` at `transport.py:193`), and with that one change made in-process (`PermissionError` read as contention) 0 of 300. On CI it was red on 1 of 6 recent windows runs; a later read of 5 main push runs showed 0 of 5. Quarantined `flaky` on windows-latest in the known-reds registry (owner B2, expiry 2026-10-19) · Done when: `_DestinationLock.__enter__` treats a Windows delete-pending `PermissionError` as contention, retried inside the same deadline, with a RED-first test that fails on the shipped lock; 10 consecutive green windows runs of the test, shown by the run ids; the registry entry removed · touches: `scripts/transport.py`, `tests/test_transport.py`, `logs/KNOWN-REDS-REGISTRY.json` · kill-candidates: none -- [#1344] is the graph-spine lock tests, a different lock in a different script · refs `scripts/transport.py`, `tests/test_transport.py`, `logs/KNOWN-REDS-REGISTRY.json`, [#1344] · source: batch FOUNDATION lane foundation-8-test-isolation (2026-10-04)
