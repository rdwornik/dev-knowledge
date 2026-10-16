---
id: "[#1575]"
title: "CLAUDE.md section 9, the hook_watchdog fate date and canonical_freshness tell the truth about the guards"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1575] [P2][S] **CLAUDE.md section 9, the hook_watchdog fate date and canonical_freshness tell the truth about the guards** - `harness.yaml` fate `hook_watchdog.py manual_until 2026-10-14` is expired and wrong; CLAUDE.md section 9 'guards off since 2026-09-17' and 'armed 12' are stale (config has more armed); `canonical_freshness: CLAUDE.md last_reviewed 2026-10-05 predates last edit` (`docs/audits/2026-10-14-technical-phase0.md:25-27`; to-browser/SESSION-integrator-bu-2026-10-15.md:135; `docs/audits/2026-10-15-technical-verified-harness-map.md:46`) · Done when: RED first: a test derives the armed-hook count from `.pre-commit-config.yaml` and asserts CLAUDE.md section 9 states it, no expired `manual_until` remains in `ecosystem/harness.yaml`, and `canonical_freshness` passes on CLAUDE.md; fails on 97bcd374 · touches: `CLAUDE.md`, `ecosystem/harness.yaml`, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1445]`, `[#1563]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
