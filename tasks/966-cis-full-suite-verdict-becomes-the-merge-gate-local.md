---
id: "[#966]"
title: "CI's full-suite verdict becomes the merge gate; local runs only Windows-only tests"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#966] [P1][M] **CI's full-suite verdict becomes the merge gate; local runs only Windows-only tests** - D3: CI already runs the whole 7,343-test suite in about 8 minutes (`-n 4`, ubuntu) but stays report-only, while the local merge spends 30-59 minutes comparing a 59-118-file subset -- CI says failure and local says CLEAN on every sampled merge (`docs/audits/2026-09-23-technical-verify-time.md` §CI facts and parity, `docs/audits/2026-09-23-technical-audit-crosscheck.md` C7/C8) · Done when: after `logs/SUITE-BASELINE-FREEZE.md` is refreshed and `deploy/conductor-required-checks.ruleset.json` enforcement is no longer `disabled`, the integrator gates a merge on the CI verdict for that SHA, and the local `compare` step runs only tests that are platform-specific (Windows-only); the crosscheck's ordering caveat (fix selection first, per D4) is honored before this is armed · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-window-defects.md`, `docs/audits/2026-09-23-technical-verify-time.md`, `docs/audits/2026-09-23-technical-audit-crosscheck.md`, `deploy/conductor-required-checks.ruleset.json`, `logs/SUITE-BASELINE-FREEZE.md` · kill-candidates: none -- no open row makes CI's verdict the gate; depends on the freeze refresh named in the same audit
