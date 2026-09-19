---
id: "[#917]"
title: "Our own docs are wrong about the worktree lock -- a locked remove is a loud fatal (exit 128), not a silent no-op"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
implements: "DECLARE-SPINE-AND-B3-2026-09-19"
generates: BACKLOG.md
---

- [#917] [P2][S] **Our own docs are wrong about the worktree lock -- a locked remove is a loud fatal (exit 128), not a silent no-op** - `.claude/commands/lane-integrate.md:320` and `scripts/audit.py:1906` both state that `git worktree remove` "silently no-ops" on a locked directory. Measured on git 2.55.0.windows.5 (throwaway repo, 2026-09-19): `git worktree remove ../wt` -> `fatal: cannot remove a locked working tree, lock reason: claude session x (pid 1)`, exit 128; `remove -f` -> the same fatal, exit 128; only `remove -f -f`, `unlock` or a filesystem delete gets past it. Reproduced again in the wave-3 close: `git worktree remove .claude/worktrees/wave3-dispatch-split` failed loudly while a resumed witness process held the directory. Two places reason from a false premise about the one guard that works (`[#916]`) -- a reader who believes the no-op story treats a refused teardown as done · Done when: both sites state the measured behaviour (fatal, exit 128, lock reason printed; bypassed only by `unlock`, `-f -f` or a filesystem delete), and a test pins the refusal against a real locked worktree so the claim cannot drift again · implements: DECLARE-SPINE-AND-B3-2026-09-19 · refs filed by the wave-3 close operator order 2026-09-19, `.claude/commands/lane-integrate.md:320`, `scripts/audit.py:1906`, SCAN-live-worktree-teardown-am5-contracts-2026-09-19.md section 1b, `[#916]`
