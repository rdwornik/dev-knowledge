---
id: "[#1333]"
title: "logs/QUOTA-READS.jsonl is tracked and dirty in every primary session; its home is per-user state"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1333] [P2][S] **logs/QUOTA-READS.jsonl is tracked and dirty in every primary session; its home is per-user state** - `scripts/hooks/quota_daily.py` (SessionStart, `.claude/settings.json`) starts a detached `quota_watch.py record`, which appends to the TRACKED `logs/QUOTA-READS.jsonl` (`READS_LEDGER_RELPATH`); so the primary checkout is dirty after every session and every close carries the ledger into a commit. Quota reads are per-user account state, so the R17/R20 home is the `private` kind of `ecosystem/fleet-shape-spec.yaml` `runtime_data_home` (a per-user OS state directory, `platformdirs.user_state_dir`, outside any repo path; precedent `scripts/cost_usage_telemetry.py`). Built by lane foundation-1-honest-green (Done item 6); this row closes when that branch merges, by the integrator · Done when: the ledger lives under the per-user state directory, `logs/QUOTA-READS.jsonl` is untracked (`git rm --cached`; its history stays in git), `quota_watch.py` and `quota_daily.py` read and write the new path, and a test proves a SessionStart in the primary leaves `git status --porcelain` empty · touches: `scripts/quota_watch.py`, `scripts/hooks/quota_daily.py`, `tests/test_quota_watch.py`, `tests/test_quota_daily.py`, `ecosystem/transport-registry.yaml`, `templates/integrator-order-template.md` · kill-candidates: none -- no open row tracks the ledger's home · refs `ecosystem/fleet-shape-spec.yaml`, `scripts/quota_watch.py`, `scripts/hooks/quota_daily.py`, `scripts/cost_usage_telemetry.py` · source: batch FOUNDATION lane foundation-1-honest-green (2026-10-03)
