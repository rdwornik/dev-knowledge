# Codex Review — lane-scope-guard-2 (full terra record, repair 1)

**Date:** 2026-09-29
**Branch:** `worktree-lane-scope-guard-2`
**Contract:** `LANE-5B5R-2-scope-guard-2.md` (redo of `LANE-5B4-1-scope-guard.md`, from preserved
tip `ca0bca819773b26fc9f250011fb6836ea6d46d73`)
**Codex version:** codex-cli 0.155.0 (`gpt-5.6-terra`); round 7 substituted `agy` (model/effort
default) after Codex hit its usage limit
**Mode:** commit-review, one round per fix commit (RED-first: each finding is closed by the
next commit, not batched)

**Purpose of this file:** the integrator's refusal
(`to-browser/REFUSED-lane-scope-guard-2.md`) found Done-contract item 6 UNMET — no invocation
line, no fixing sha stated, and rounds 1–2 omitted. This file is the complete record: every
round's invocation, every P1 verbatim as the reviewer wrote it, and the commit that fixed it,
across BOTH the N4 lane's two rounds and this lane's own seven.

---

## Round 1 — N4 original lane, reviewing commit `193e9007`

**Invocation:** not separately captured — the N4 original lane's raw Codex transcript was
never written to a retrievable file, only paraphrased in its own session file
(`to-browser/SESSION-lane-scope-guard.md` DONE-ITEM 5, pre-repair section). This is an
inherited gap from a prior lane, not this repair's to manufacture; N4's own repair-1
established the same finding and supplied fresh verbatim evidence instead (round 2, below)
rather than reconstructing round 1's transcript from memory.

**What the session file paraphrases (not verbatim):** two P1s, both "fixed in-session" before
`193e9007` was pushed:
1. `.claude/settings.json`'s hook command needed the `${CLAUDE_PROJECT_DIR:-.}` fallback form.
2. `normalize()`/`decide()` needed to also check the realpath form of a path, to catch a
   junction whose own name sits outside the zone but that points into it.

**Fixing commit:** both folded into `193e9007` itself (the lane's only commit — fixed before
first push, per its own DONE-ITEM 5).

---

## Round 2 — N4 repair-1, fresh review of commit `193e9007`

**Invocation** (`to-browser/SESSION-lane-scope-guard.md` lines 219–223):
```
$ codex exec review -m gpt-5.6-terra --commit 193e9007 --output-last-message <job-tmp>/codex-review-repair1.md < /dev/null
```

**Verbatim result:**
```
The scope guard leaves multiple supported tool routes and common shell constructions outside
its enforcement, allowing excluded-root access despite the new R15 mechanism.

- [P1] Match filesystem-capable MCP tool calls -- .claude/settings.json:83-83
  The new matcher never invokes this guard for `ReadMcpResourceTool`, `LSP`, or `mcp__.*`, even
  though these routes can access filesystem-backed resources. A call through one of those tools
  therefore bypasses the R15 exclusion entirely and can read an excluded employer folder;
  include the applicable filesystem/MCP tool matchers and handle their path-bearing payload
  fields.

- [P1] Do not allow shell syntax that hides path fragments -- scripts/hooks/scope_guard.py:200-206
  Shell commands can access excluded paths while the path is embedded in program syntax or
  constructed by the shell, because `shlex` only examines resulting shell words. For example, a
  PowerShell/Bash call running `python -c "open(r'C:\...\OneDrive - Blue Yonder\f.txt')"` is
  split into fragments and none normalizes to the excluded component, so `decide` allows the
  access. This makes the claimed Bash/PowerShell protection bypassable; either parse/enforce
  supported command forms conservatively or reject shell calls containing unresolved
  path-like expressions.
```

**Disposition:**
- **P1 #1 (MCP/LSP matcher gap) — FIXED**, in commit `ca0bca81` (the matcher broadened to
  `...|Monitor|LSP|ReadMcpResourceTool|mcp__.*`; `candidate_tokens` gained a `_string_leaves`
  fallback).
- **P1 #2 — PARTIALLY FIXED.** The reviewer's own literal reproduction was tested and found to
  already `block` (backslash-splitting already caught it — a `PREMISE-FAILED` on that specific
  example, not a live bug). Adversarial probing found a REAL gap instead: a shell glob wildcard
  (`OneDrive*`) standing in for the root's literal name — **fixed in `ca0bca81`** via
  `excluded_root_hit`'s new `fnmatch` leg. Two further constructions — PowerShell string
  concatenation and a same-line environment-variable `set`+expand — were verified live to still
  `allow` and recorded as an HONEST LIMIT at that point (not yet fixed — closed later, rounds
  1–4 of this lane, below).

**Fixing commit:** `ca0bca81` (both legs of P1 #1; the glob-wildcard leg of P1 #2).

---

## Round 3 (this lane) — reviewing commit `e3de7e24`

`e3de7e24` is this lane's first substantive commit after merging the preserved tip: it adds
cross-OS normalisation and attempts closure of round 2's remaining honest limit (PowerShell
concatenation, same-line `set`/env-var expand).

**Invocation** (reconstructed from the run's own recorded parameters — the wrapping shell
command was not separately logged; the stdout transcript itself is the checkable artifact:
`C:\Users\1028120\.claude\jobs\0edc1f6d\tmp\codex-review-lane2-stdout.log`):
`codex exec review`, model `gpt-5.6-terra`, workdir this worktree, sandbox `workspace-write`,
approval `never`, reasoning effort `low`, session id `01a0eaea-d134-7c52-8bb0-ea8529d0d4b0`,
input `commit e3de7e2`.

**Verbatim result** (`codex-review-lane2.md`):
```
- [P1] Detect single-quoted PowerShell concatenations — scripts/hooks/scope_guard.py:275-280
  PowerShell supports single-quoted literals, so `Get-Item ('OneDrive' + ' - Blue Yonder')`
  bypasses this scan: the regex only recognizes double quotes, while the ordinary token
  scanner sees no path-shaped token. Extend the literal-concatenation handling to PowerShell
  single quotes as well.

- [P1] Preserve Windows case-insensitive environment lookup — scripts/hooks/scope_guard.py:195-201
  On a Linux runner, `os.environ.get(name)` is case-sensitive, unlike Windows environment
  expansion. Thus a PowerShell/cmd path using `%dk_test_root%` (or `$env:dk_test_root`) when
  only `DK_TEST_ROOT` is set remains unexpanded and is allowed, contradicting the stated
  cross-OS Windows-token behavior. Perform a case-insensitive lookup for Windows-style
  variable forms.

- [P1] Parse quoted cmd set assignments — scripts/hooks/scope_guard.py:173-178
  The normal cmd.exe assignment form `set "X=OneDrive - Blue Yonder" & type "...%X%..."` is not
  matched because the regex requires the variable name immediately after `set`. The subsequent
  path token is therefore normalized with an unresolved `%X%` and allowed, leaving the same-line
  expansion bypass open. Accept the optional assignment quotes and exclude them from the
  captured value.
```

**Fixing commit:** `26a14f3e` — all 3 P1s fixed per the commit message (single/double-quote
concatenation both accepted; case-insensitive percent-form fallback added, dollar-form stays
case-sensitive on purpose; quoted `set` assignment form now tried first).

---

## Round 4 (this lane) — reviewing commit `26a14f3e`

**Invocation:** same shape as round 3; session id `01a0eb02-9d0b-77f2-84bf-f7820bfec75f`,
input `commit 26a14f3`
(`C:\Users\1028120\.claude\jobs\0edc1f6d\tmp\codex-review-lane2-round2-stdout.log`).

**Verbatim result** (`codex-review-lane2-round2.md`):
```
- [P1] Avoid matching quoted prose inside PowerShell arguments — scripts/hooks/scope_guard.py:327-327
  A PowerShell command with no path argument, such as `git commit -m "document 'OneDrive' + '
  - Blue Yonder' handling"`, now matches this regex inside the outer message string, produces
  the joined excluded-root candidate, and is blocked. This newly breaks ordinary PowerShell
  commits/documentation while the only workaround disables the guard for the whole session;
  constrain concatenation detection to actual PowerShell expression context rather than
  arbitrary quoted argument contents.
```

**Fixing commit:** `75998e42` — concatenation scan scoped to the PowerShell tool only, and
nested-quote characters are neutralized before the scan, so a `+` quoted as prose inside a
Bash commit message is never a candidate. New regression test covers exactly this shape
(`test_a_word_that_merely_mentions_the_zone_name_in_prose_is_not_a_path`'s sibling).

---

## Round 5 (this lane) — reviewing commit `75998e42`

**Invocation:** session id `01a0eb12-f3b6-7282-97b9-e34f3cbfa6ae`, input `commit 75998e4`
(`C:\Users\1028120\.claude\jobs\0edc1f6d\tmp\codex-review-lane2-round3-stdout.log`).

**Verbatim result** (`codex-review-lane2-round3.md`):
```
- [P1] Handle PowerShell backtick-escaped delimiters — scripts/hooks/scope_guard.py:348-353
  A valid prior PowerShell string with an escaped double quote leaves `state` incorrectly
  open, so subsequent top-level single-quoted concatenations are neutralized and never
  scanned. For example, `Write-Output "x`""; Remove-Item ('OneDrive' + ' - Blue Yonder')`
  bypasses the guard and can target the protected directory. Account for PowerShell backtick
  escapes while tracking quote state.
```

**Fixing commit:** `0317c7fe` — backtick-escape consumption added to
`_neutralize_nested_quote_chars`.

---

## Round 6 (this lane) — reviewing commit `0317c7fe`

**Invocation:** session id `01a0eb1e-1bc4-79e1-b60e-746f48a0116d`, input `commit 0317c7f`
(`C:\Users\1028120\.claude\jobs\0edc1f6d\tmp\codex-review-lane2-round4-stdout.log`).

**Verbatim result** (`codex-review-lane2-round4.md`):
```
- [P1] Handle backticks only in expandable strings — scripts/hooks/scope_guard.py:361-365
  In PowerShell single-quoted strings, backtick is literal rather than an escape. Thus
  `Write-Output 'x`'; Remove-Item ("OneDrive" + " - Blue Yonder")` leaves the scanner in
  single-quote state because it skips the real closing apostrophe, neutralizes the subsequent
  double-quoted concatenation, and allows a command targeting the protected directory. Restrict
  backtick escaping to double-quoted state (or implement PowerShell quote semantics).
```

**Fixing commit:** `ffd2b478` — backtick condition gained `and state != "'"`, so a literal
backtick inside a single-quoted string no longer eats the closing quote.

---

## Round 7 (this lane) — reviewing commit `ffd2b478`

**Invocation:** session id `01a0eb29-4630-7671-be80-9a3841299d54`, input `commit ffd2b47`
(`C:\Users\1028120\.claude\jobs\0edc1f6d\tmp\codex-review-lane2-round5-stdout.log`).

**Verbatim result** (`codex-review-lane2-round5.md`):
```
The changed escape handling correctly preserves PowerShell single-quoted literal semantics
while retaining handling for expandable and unquoted contexts. The added regression test
covers the relevant bypass scenario.
```
**No P1 findings.**

**Fixing commit:** none needed — clean pass.

---

## Round 8 (this lane) — reviewing commit `27d7859d`

`27d7859d` added an exemption for bare-wildcard glob path components, to fix a false positive
on `templates/**` this lane's own tests surfaced.

**Invocation:** session id `01a0eb3c-5db4-79e1-ba74-a308832e2883`, input `commit 27d7859`
(`C:\Users\1028120\.claude\jobs\0edc1f6d\tmp\codex-review-lane2-round6-stdout.log`).

**Verbatim result** (`codex-review-lane2-round6.md`):
```
- [P1] Preserve blocking for globs that can expand into excluded roots — scripts/hooks/scope_guard.py:523-524
  When a shell command uses a bare wildcard at the excluded root's parent, such as
  `Get-ChildItem 'C:\Users\x\*\secret.txt'`, the `*` can expand to `OneDrive - Blue Yonder`;
  this new predicate skips it and allows access to the protected zone. Distinguish generic
  globs relative to an unrelated directory from wildcard components whose resolved parent can
  contain an excluded root, rather than exempting all pure-wildcard components.
```

**Fixing commit:** `f9a94353` — the exemption is reverted outright (no filesystem-aware way to
tell the two cases apart without resolving the glob live), accepting the `templates/**`-style
false positive as a documented cost; wedge escape is the way through.

---

## Round 9 (this lane) — SUBSTITUTION (`agy`, not Codex), reviewing commit `f9a94353`

Codex (`gpt-5.6-terra`) hit its usage limit mid-review on `f9a94353` ("You've hit your usage
limit ... try again at 8:57 AM"). Per ruling (e), `agy` (model/effort default) substituted.

**Invocation prompt** (`C:\Users\1028120\.claude\jobs\0edc1f6d\tmp\agy-review-prompt-round7.txt`,
full text — the diff review request, embedding `f9a94353`'s complete diff, asking four
confirmations and any P1s):
```
You are doing a security/correctness code review, standing in for Codex
(which is out of usage credits) as a SUBSTITUTION for this review round.

Review the following git commit diff. It is a defensive fix in a
PreToolUse scope-guard hook (scripts/hooks/scope_guard.py) in an
authorized personal governance repository. The commit reverts a prior
exemption for bare shell-glob wildcard path components (a lone *, **, or
? with no literal characters) in excluded_root_hit's fnmatch leg, because
a prior review found that exemption reopens a real bypass: a bare
wildcard standing in for the excluded root's own parent directory would
still expand onto the excluded zone at shell-execution time. The revert
restores unconditional fnmatch matching for any path component containing
a glob character, accepting a known false positive on unrelated generic
glob arguments (e.g. a git pathspec like templates/**) in exchange for
closing the real bypass, documenting an environment-variable wedge escape
as the way through for a legitimate bare-glob command. Two tests were
rewritten to assert the component is now blocked rather than allowed.

Confirm: (1) the revert is correctly implemented -- no leftover exemption
logic remains, and the docstring accurately describes current behavior;
(2) no new bypass is introduced by this diff; (3) the trade-off reasoning
is sound given the guard's own stated fail-closed doctrine
(_cannot_evaluate: "permitting what it cannot check is enforcement
without enforcement"); (4) test coverage for this change is adequate.
List any P1 (must-fix) findings explicitly, or state there are none.

--- BEGIN DIFF --- (f9a94353's full diff, elided here — see the prompt file for the complete
text, or `git show f9a94353`)
```

**Raw agy response:** not persisted to a file this session (same class of gap as round 1 — the
invocation and disposition below are recorded from the session's own record, not
reconstructed). Disposition as recorded in `to-browser/SESSION-lane-scope-guard-2.md`: all four
confirmations affirmed — revert correctly implemented, no leftover exemption logic, no new
bypass, trade-off reasoning sound, test coverage adequate. **No P1 findings.**

**Fixing commit:** none needed — clean pass; `f9a94353` stands as pushed.

---

## Summary table

| # | Reviewer | Commit reviewed | P1 count | Fixing commit |
|---|---|---|---|---|
| 1 | Codex terra (N4 original, prose-only, unrecoverable verbatim) | `193e9007` | 2 (paraphrased) | `193e9007` (same commit) |
| 2 | Codex terra (N4 repair-1) | `193e9007` | 2 | `ca0bca81` |
| 3 | Codex terra (this lane) | `e3de7e24` | 3 | `26a14f3e` |
| 4 | Codex terra (this lane) | `26a14f3e` | 1 | `75998e42` |
| 5 | Codex terra (this lane) | `75998e42` | 1 | `0317c7fe` |
| 6 | Codex terra (this lane) | `0317c7fe` | 1 | `ffd2b478` |
| 7 | Codex terra (this lane) | `ffd2b478` | 0 (clean) | — |
| 8 | Codex terra (this lane) | `27d7859d` | 1 | `f9a94353` |
| 9 | `agy` SUBSTITUTION (this lane) | `f9a94353` | 0 (clean) | — |

**Tally:** 0/11/0/0 <!-- Critical/High/Medium/Low. This repo's Codex "P1" (must-fix) findings
map to this file's High tier per ruling (e); 9 review rounds across rounds 1-9, 11 total P1s
(round 1: 2, round 2: 2, round 3: 3, round 4: 1, round 5: 1, round 6: 1, round 8: 1 -- round
1's 2 were fixed pre-push in the same commit, each other round's fixed in the next commit
named beside it), rounds 7 and 9 clean. -->
