<!-- scope: meta -->
# Wave-A Post-Ship Witness Validation
**Date:** 2026-06-07
**Pattern:** ADR-85 (post-ship witness record)
**Wave merge:** `1e5ae0b` (manual) — wave A: writer wiring + carriers

---

## W1 — audit.py routine commit isolation (#125)

**Spec:** Create untracked scratch file → run `python scripts/audit.py run` → verify:
(a) new commit exists, (b) `git show --stat HEAD` contains ONLY `ecosystem/*/history/` + `docs/audits/` paths,
(c) `git log -1 --format=%B` carries `Routine: fleet-audit` trailer, (d) scratch file still untracked,
(e) tree otherwise clean. Remove scratch.

**Result:** PASSED (prior session — see session transcript `a595d680-3440-4620-9e45-74580e4f9e9b`)

All five sub-checks confirmed. Fixes landed in that session:
- Windows git glob pathspec bug in `_commit_routine_outputs` → concrete path enumeration
- Pre-commit auto-format causing routine commit failure → one-shot re-stage + retry

---

## W2 — backlog-id-on-close hook enforcement (#114)

**Spec:** In a temp dir outside the repo — git init, minimal BACKLOG.md with one task,
`.pre-commit-config.yaml` consuming hub's `backlog-id-on-close` at current rev.
Commit removing task WITHOUT `[#id]` → MUST block. Then with `[#id]` → MUST pass.

**Result:** PASSED (this session — 2026-06-07)

**Root cause of prior failure:** `pass_filenames: false` in `.pre-commit-hooks.yaml` caused
pre-commit to wipe `filenames = ()` before subprocess invocation. For `commit-msg` stage,
`filenames = (commit_msg_filename,)` initially, but `pass_filenames: false` overrides it to
`()`. Script received no `sys.argv[1]` and returned 0 unconditionally.

**Fix applied:** Removed `pass_filenames: false` from `backlog-id-on-close` hook definition.
Note: attempted `language: python` but reverted — causes `pip install .` on hub which fails
(multiple top-level packages, no py package setup). `language: script` with shebang-based
Python detection is correct and now works with `pass_filenames` restored to default (true).

**Fix commits:** `7e004d2` (drop pass_filenames:false + language:python) → merged `42b84f3`
then `6bc8105` (revert language:python → language:script) → merged `67c3d28`

**Block test output:**
```
Require [#id] in commit message when a BACKLOG task is closed.......................Failed
- hook id: backlog-id-on-close
- exit code: 1

commit-msg: BACKLOG task(s) #99 removed but not referenced in the message.
  Add [#<id>] or 'closes [#<id>]' for each (ADR-65/66 forward-only index).
```

**Pass test output:**
```
Require [#id] in commit message when a BACKLOG task is closed.......................Passed
[master 2befcaa] chore: close witness task closes [#99]
```

---

## W3 — /ship pre-flight refusal on main (#115)

**Spec:** State whether `1e5ae0b` merge was performed by /ship or manually. Then invoke
/ship on main → paste pre-flight refusal (proves plugin-sourced command executes).

**Merge provenance:** `1e5ae0b` was performed **manually** — not by /ship.

**Result:** PASSED (this session — 2026-06-07)

**Pre-flight refusal output:**
```
Pre-flight FAILED: /ship must run on a feature branch, not main.
```
(`git rev-parse --abbrev-ref HEAD` returned `main`; /ship halted at check 1 as specified)

---

## Summary

All three wave-A witnesses passed. Wave-A closures stand:
- #125 (audit.py routine commit isolation)
- #114 (backlog-id-on-close hook enforcement)
- #115 (/ship command integration)

Incidental fix: #114 investigation discovered and corrected the `pass_filenames: false` bug
in the `backlog-id-on-close` hook definition — the hook was silently passing all commits
that removed BACKLOG tasks (a latent gate bypass). Fixed and verified gate-closed.
