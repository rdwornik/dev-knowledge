# Codex Review — lane-scope-guard-3

**Date:** 2026-09-29
**Branch:** `worktree-lane-scope-guard-3`
**HEAD:** `a40f873a`
**Diff range:** `main..worktree-lane-scope-guard-3`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** TBD/TBD/TBD/TBD <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Consumer: this review is for LANE-5B5-1-lane-scope-guard-3.md (H:\My Drive\CLAUDE PROMPT DIR\LANE-5B5-1-lane-scope-guard-3.md), batch WAVE5B-N5.
Diff: scripts/hooks/scope_guard.py and tests/test_scope_guard.py only.
Change: excluded_root_hit's bare-wildcard-matches-any-root leg (a path component made entirely
of glob metacharacters, e.g. a bare star or double-star, used to fnmatch against every root
name regardless of position) is narrowed to fire only when the wildcard sits exactly two path
components below a conventional OS user-home parent ('users' or 'home', case-insensitive) --
the only place the real excluded root can ever be a direct child. This closes four witnessed
false positives (a grep -oE regex with escaped literal asterisks, a glob under
~/.claude/projects/, that same token quoted in a PowerShell here-string, and the pre-existing
'git diff -- templates/star-star' accepted-false-positive test, now flipped to allow) while
keeping the real bypass refused -- see
test_a_bare_wildcard_standing_in_for_the_root_at_its_own_parent_is_refused in
tests/test_scope_guard.py for its exact shape.
Please check specifically: (1) whether the home-boundary heuristic (checking parts[i-2] against
{'users','home'}) can itself be bypassed by a constructed path, (2) whether the fix could
under-block a real bypass shaped differently than the existing test, (3) general code quality
of the new _bare_wildcard_hit helper and its docstring accuracy.

---

## Findings
## Critical

### scripts/hooks/scope_guard.py:555 — `**` can bypass the home-boundary check

**What:** `**` is treated like a single-component wildcard, so `shopt -s globstar; cat /home/**/secret.txt` is allowed.  
**Why:** Bash globstar can expand this through `/home/<user>/OneDrive - Blue Yonder/secret.txt`; the `**` component is immediately below `home`, not two components below it.  
**Fix direction:** Handle recursive `**` separately, blocking it when its expansion can traverse a `home`/`Users` profile boundary into a direct-child excluded root; add a Bash-globstar regression test.

### scripts/hooks/scope_guard.py:556 — heuristic under-blocks roots mounted outside `Users`/`home`

**What:** Bare wildcards are now allowed outside `Users/<user>` or `/home/<user>`, e.g. `Get-ChildItem 'D:\*\secret.txt'`.  
**Why:** `excluded-roots.yaml` defines bare root names as matching wherever mounted; if the excluded folder is `D:\OneDrive - Blue Yonder`, this command reaches it but the guard permits it. The docstring’s “only ever” claim is therefore not supported by the registry contract.  
**Fix direction:** Preserve the mount-location invariant in configuration or resolve wildcard candidates against configured root locations rather than assuming a single home-directory topology.

## High

(none)

## Medium

(none)

## Low

(none)

---

## AMENDMENT (2026-09-29, in-file marker per CLAUDE.md §5 rule 3 -- audits are immutable,
## the tally line above is left as generated rather than edited in place)

**Tally: 2/0/0/0.** Both Critical findings were addressed in a follow-up commit
(`2fc067b2`, `fix(scope-guard): close two Codex terra Critical findings on the
home-boundary heuristic`):
- Critical #1 (`**` bypasses the home-boundary check): `_bare_wildcard_hit` now anchors a
  recursive `**` one component back from a `users`/`home` marker instead of two, since `**`
  ranges over zero-or-more levels below its own anchor. Regression test:
  `test_a_recursive_globstar_directly_under_a_home_parent_is_refused`.
- Critical #2 (heuristic under-blocks roots mounted outside `Users`/`home`): a bare
  wildcard within the first two path components (no home marker needed at all) is now also
  treated as a hit, matching `excluded-roots.yaml`'s own "matches wherever mounted"
  contract. Regression test: `test_a_bare_wildcard_directly_under_a_drive_root_is_refused`.

Both fixes verified: the full suite (61 tests) green, the four witnessed false positives
this lane exists to fix still allow, and the pre-existing real-bypass test still blocks.