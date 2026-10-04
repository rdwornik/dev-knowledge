---
id: "[#1375]"
title: "Skills and commands are kept by the problem they solve, and Anthropic's built-ins are reviewed on a routine"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1375] [P2][M] **Skills and commands are kept by the problem they solve, and Anthropic's built-ins are reviewed on a routine** - R77 (operator, 2026-10-04): each skill or command is judged by the problem it solved. Solved elsewhere is retired (`/session-summary`, replaced by the Drive transport); unknown purpose is checked then retired (`aj-scan`); still open is solved properly (`/why`: the need to know what each part does without re-scanning is met by the spine's map command, step 5). Anthropic's built-in commands and skills are reviewed on a routine that a mechanism triggers; `/auto-mode-setup` is a candidate and changes the operator's global config, so it needs his act. · Done when: a table lists every skill and command with the problem it solved and one disposition (retire, check then retire, solve); `/session-summary` is retired with the Drive-transport replacement named; `aj-scan` is either retired or kept with its reason; the spine's map command exists and the `/why` measurement of `[#924]` reaches its bar; a scheduled mechanism writes a dated list of Anthropic's built-in commands and skills and the diff since the last list; the `/auto-mode-setup` decision is recorded as an OPERATOR-ACTION · owner: wave B2 W2: a skills-and-commands lane; the operator takes the global-config act · touches: `.claude/skills/`, `.claude/commands/`, the changelog-review trigger, tests · kill-candidates: `[#1034]` -- the claude.ai-synced skills question is one row of the same table · refs `[#924]`, `[#1034]`, `protocols/STANDING_RULINGS.md` section AR (R77) · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R77 in `to-browser/RATIFICATION-2026-10-04.md R77`
