---
id: "[#965]"
title: "One known-reds registry, read by CI and local, refreshed at the merge moment"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#965] [P1][M] **One known-reds registry, read by CI and local, refreshed at the merge moment** - D2: two known-reds registries disagree -- CI's 87-test baseline is 6 days stale and always red, so nobody reads its verdict, while the local per-batch registry is the one integrators actually trust (`docs/audits/2026-09-23-technical-verify-time.md` §CI facts and parity) · Done when: one known-reds registry is read by both CI (`conductor.yml`) and the local `test_pairing.py`/`gates.py` path, refreshed at the merge moment rather than by hand; a parity check on the same SHA shows CI and local agreeing on the reds · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-window-defects.md`, `docs/audits/2026-09-23-technical-verify-time.md`, `logs/SUITE-BASELINE-FREEZE.md`, `.github/workflows/conductor.yml` · kill-candidates: none -- no open row unifies the two registries
