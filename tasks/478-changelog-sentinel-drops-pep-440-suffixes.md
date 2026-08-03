---
id: "[#478]"
title: "`changelog_sentinel` drops PEP 440 suffixes — a prerelease as the reviewed value silences the sentinel permanently"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
generates: BACKLOG.md
---

- [#478] [P2][S] **`changelog_sentinel` drops PEP 440 suffixes — a prerelease as the reviewed value silences the sentinel permanently** — `scripts/changelog_sentinel.py:45-52` parses with `(\d+(?:\.\d+)+)`, discarding every suffix, so `2.0.15rc1` becomes `(2,0,15)`. Measured live by the 2026-08-03 L-E lane: `is_newer('2.0.15' over reviewed '2.0.15rc1')` gives **False** where PEP 440 gives **True**; `2.0.14.post1` vs `2.0.14` likewise. If `/changelog-review` ever records a prerelease as the reviewed version, the GA release that follows compares EQUAL and the sentinel goes quiet for that tool forever — silently, since the failure mode is absence of output. Fix adds no dependency: `packaging.version.Version` is declared at `pyproject.toml:37` and already swapped into `fleet_parity` at `a7e42a30`. · Done when: suffixed versions compare per PEP 440, with a test covering prerelease-then-GA and `.post` · refs scripts/changelog_sentinel.py, pyproject.toml, a7e42a30 · kill-candidates: none — the `a7e42a30` swap covered fleet_parity only; no row owns the sentinel's comparator
