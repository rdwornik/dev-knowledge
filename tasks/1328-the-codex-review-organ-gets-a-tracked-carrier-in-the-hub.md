---
id: "[#1328]"
title: "The Codex-review organ gets a tracked carrier in the hub"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1328] [P1][M] **The Codex-review organ gets a tracked carrier in the hub** - operator ruling 2026-09-30 on R42.2 (`to-browser/RATIFICATION-2026-09-30.md` v2): the Codex-review organ is L0-only and untracked (`~/.claude/bin/codex-review.ps1`, `~/.claude/commands/codex-review.md`), so `[#1329]`'s "the organ writes the consumer line itself" has no repo home to build in. Its source moves under the hub, tested, and `~/.claude/` becomes an installed copy; `~/.claude/` is never edited directly. · Done when: RED-first, a test pins that the hub-tracked source of `codex-review.ps1` and `codex-review.md` is byte-identical to what the carrier installs; the carrier is declared in the current `deploy/manifest-v*.yaml` `carriers:` block with a `source_path`, `deploy/release_lint.py` passes, and a deploy run reproduces the two `~/.claude/` files from the hub source · depends on: current `deploy/manifest-v*.yaml` (`carriers:`, the `global-config` `source_path` precedent for `deploy/global-instructions-codex.md`), `deploy/release_lint.py`, the deploy tool's carrier executor, `tests/test_deploy_globalconfig.py` (the precedent test), a new carrier test, `scripts/deploy` pre-commit carrier hooks (`tests/test_carrier_landed_check.py`) · kill-candidates: none -- no open row tracked the organ's missing carrier before this entry
