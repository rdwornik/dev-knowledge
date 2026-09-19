---
id: "[#922]"
title: "Spine stage 7 (substrate) is invoked without its required paths argument -- exit 2, and this is where the spine now stops"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#922] [P2][S] **Spine stage 7 (substrate) is invoked without its required paths argument -- exit 2, and this is where the spine now stops** - `ecosystem/harness.yaml` stage 7 declares `command: [uv, run, --locked, python, scripts/validate_substrate.py, --rules]`, but `validate_substrate.py`'s argparse requires positional `paths [paths ...]`, so the stage exits 2 (`validate_substrate.py: error: the following arguments are required: paths` / `TaskFailed - taskid:stage:07-substrate`). Measured by the wave-3 spine-fixups lane on the `WIRE` / `dispatch` subject after stage 6 was wired: `docs/audits/2026-09-19-technical-wave3-spine-fixups.md` "Acceptance 1". Stages 1-6 now pass, so stage 7 is the spine's first stop. The stage has no notion of WHICH artifact's substrate it validates -- the subject's lane contract is the obvious operand, but that is a design choice this row makes, not a fact already in the tree · Done when: stage 7 runs `validate_substrate.py` against a named operand derived from the spine's (kind, subject) -- or is declared `command: null` with a reason, as stage 11 is -- and a RED-first test in `tests/test_dodo.py` shows the real spine on the `dispatch` subject gets past stage 7 (or stops at it with a named, non-argparse refusal) · refs `ecosystem/harness.yaml` (stage 7), `scripts/validate_substrate.py`, `scripts/dodo.py`, `docs/audits/2026-09-19-technical-wave3-spine-fixups.md`
