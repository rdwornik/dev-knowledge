---
id: "[#431]"
title: "`codex-review` silently drops the doc lane on any mixed diff"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: codex-review
source: BACKLOG.md
derived: true
---

- [#431] [P2][S] **`codex-review` silently drops the doc lane on any mixed diff** — any code-allowlist file routes the diff to the CODE profile, filtered to the code subset; that diff's prose files are **not** doc-reviewed and nothing says so at run time. The allowlist includes `.yaml/.yml/.toml/.json/.ini`, so a one-line config change strips doc review from an all-prose diff. Designed-and-documented at `protocols/PLAYBOOK.md:3439`, implemented at `~/.claude/bin/codex-review.ps1:103-115` — a doctrine defect, not a code bug. **Second defect, same wrapper:** the severity counter printed 0/0/0/0 for a review carrying 1 High / 3 Medium / 1 Low (witnessed 2026-07-26) — never trust the counter, read the BODY. **Global-infra:** the wrapper is `~/.claude/`, so both fixes need an operator ruling (core-invariant #6). Assigned by intake #17 §5. · Done when: a mixed diff gets both profiles or emits a loud skipped-prose warning naming the unreviewed files, AND the counter agrees with the body, with tests · refs #333, #338, #363, ADR-54, intake #17 §5 · kill-candidates: none — #363 is lane-SELECTION within a reviewed diff; this is prose unreviewed entirely · serialize-group: codex-review
