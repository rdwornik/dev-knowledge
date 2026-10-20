---
id: "[#1713]"
title: "G-REDAGE: wire ci_red_age into the batch-close digest, or retire it with its flag (R149)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1713] [P2][S] **G-REDAGE: wire ci_red_age into the batch-close digest, or retire it with its flag (R149)** - `scripts/lane_digest.py:486` passes `--ci-red-json` but the `ci_red_age` step runs before `digest` and its fate expired 2026-10-19; it now carries `manual_until: 2026-11-09` · owner: CI-signal lane · target batch: E2 · Done when: (1) RED first: a seeded red run makes `doit -f scripts/dodo.py moment:batch-close` print no OPERATOR-ACTION line; (2) the producer step feeds `--ci-red-json`; (3) real-use witness: that command prints the OPERATOR-ACTION line of `scripts/lane_digest.py:161`; stated fallback, not a re-date: if not witnessed by E2 close, retire `ci_red_age.py` and the flag together · touches: `scripts/ci_red_age.py`, `scripts/lane_digest.py`, `ecosystem/harness.yaml` · kill-candidates: none -- no open row covers it · decided-by: R149 (operator, 2026-10-19) · refs `ecosystem/harness.yaml` · source: G-REDAGE in `to-browser/DIGEST-E1-FATES-2026-10-19.md`
