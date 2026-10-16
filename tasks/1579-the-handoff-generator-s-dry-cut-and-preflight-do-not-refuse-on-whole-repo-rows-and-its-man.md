---
id: "[#1579]"
title: "The handoff generator's dry cut and preflight do not refuse on whole-repo rows, and its manual-until reader matches"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1579] [P1][M] **The handoff generator's dry cut and preflight do not refuse on whole-repo rows, and its manual-until reader matches** - `gen_handoff --dry-cut` refuses on `ship_gate` though its help says it skips cut gates; `--preflight-only` exits 1 on 148 OPEN decision files plus 2 QUESTION files without `disposition:`; `handoff_state.py:697 _MANUAL_UNTIL_RE` is `^`-anchored and matches 0 lines so `verify_handoff_probes.py:1575` always reads 'none'; the 10-14 bundle has unfilled FILL-INs (`docs/audits/2026-10-15-technical-verified-harness-map.md:59`; `docs/audits/2026-10-14-technical-phase0.md:30,77`; `docs/audits/2026-10-14-technical-handoff-gaps.md` Q3). Per R129 (ADR-129) the cut is gated by handoff-relevant checks only · Done when: RED first: (1) a dry-cut test with a red `ship_gate` row exits 0 and names the row; (2) a preflight test over a fixture of OPEN decisions reports them as non-gating rows; (3) `_MANUAL_UNTIL_RE` matches a fixture line `manual_until: 2026-10-19`; fails on 97bcd374 · touches: `scripts/gen_handoff.py`, `scripts/handoff_state.py`, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1456]`, `[#1386]`, `[#1445]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
