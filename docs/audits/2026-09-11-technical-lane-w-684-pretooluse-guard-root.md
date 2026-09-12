# Lane W-2 — `[#684]`: the `PreToolUse` guard resolves its own repo root, and its matcher narrows

**Consumers:** `[#684]` (the row this lane closes) · batch W merge queue · `intake #91`

**Lane:** `lane-w-684-pretooluse-guard-root` · branch `worktree-lane-w-684-pretooluse-guard-root`
**Contract:** `LANE-w-684-pretooluse-guard-root.md`, frozen from `BATCH-2026-09-10-W-CONTRACTS.md`
**Substrate:** LOCAL, cut at Q2 (the Done-when needs a non-Claude CLI authenticated on the
operator's disk). **Mode:** plan. **Decision budget:** V-2, 2 forks.

---

## 1. Verdict, stated first

| Closure leg (contract, verbatim) | State |
|---|---|
| non-Claude reader under the guard **REFUSED → passes, one witnessed smoke** | **MECHANISM CLOSED, WITNESS PARTIAL** — see §4 |
| M7 smoke **run by the lane before its commit, output witnessed** (A7-6) | **UNMET — BLOCKED, external** — see §4 |
| RED-first test **absent → present, and RED with the fallback removed** | **CLOSED** — §2 |
| matcher **`"*"` → the named tool classes** | **CLOSED** — §3 |

The fix is landed, ARMED, and proven by every instrument that exists on this machine except
the one the A7-6 clause names. That one is refused by its own vendor, not by our guard. This
artifact says so plainly rather than substituting a passing instrument for the named one.

---

## 2. What was broken, and what the fix is

`.claude/settings.json` ran

```
python "$CLAUDE_PROJECT_DIR/scripts/fleet_health.py" --prompts-guard
```

`CLAUDE_PROJECT_DIR` is set by Claude Code and by nothing else. Any other reader that honours
the hook file expands it empty, the path resolves to garbage, the interpreter exits non-zero —
and **a `PreToolUse` hook that exits non-zero REFUSES**. Not a degraded read, a total one, and
it presents as the reader being broken rather than as our harness refusing it
(`docs/audits/2026-09-10-technical-night-aj-m03/REVIEW.md`:83, pointer :105, mechanism
`MATRIX.md` §4 MA-1).

It now runs

```
g="${CLAUDE_PROJECT_DIR:-.}/scripts/fleet_health.py"; [ -f "$g" ] || exit 0; python "$g" --prompts-guard
```

**Fork 1 of the budget — where the repo-root fallback is computed: in the COMMAND STRING, not
in the module.** The module already computes `_REPO_ROOT` from `__file__`; that was never the
gap. A garbage path means `fleet_health.py` never loads at all, so no in-module fallback can be
reached. Two POSIX legs:

- `${CLAUDE_PROJECT_DIR:-.}` — prefer the variable, fall back to cwd.
- `[ -f "$g" ] || exit 0` — a guard that cannot be **loaded** passes instead of refusing. This is
  the fail-open posture `prompts_guard()` already documents for its own internal errors, extended
  to the one failure it could not reach. The review states the intent in those words: *"the
  prompts-guard resolves its own path and fails open on interpreter failure"* (REVIEW.md:102).

**Both halves of that shape were measured before being written, not assumed** — in a throwaway
child `claude -p` session, because a `"*"` `PreToolUse` matcher can wedge a live one with no
escape:

```
hook shell : C:\Program Files\Git\bin\bash.exe   -> ${VAR:-default} expands
hook cwd   : the project directory               -> the "." fallback resolves
```

**Nothing the guard guards is weakened.** Where the script resolves it runs with full force and
a scope mismatch still exits 2 — asserted against the live tree by
`test_hook_command_still_runs_the_real_guard_from_the_repo_root`. The ADR-77
transcript-immutability leg beside it is untouched and still fail-closed.

### RED-first (ADR-108 §B)

`tests/test_prompts_guard_hook_wiring.py`, committed RED before any fix (`fe90dc25`):

```
5 failed, 3 passed in 8.91s
rc=2  python.exe: can't open file 'C:\Program Files\Git\scripts\fleet_health.py'
```

That rc=2 **is** the refusal, reproduced in this repo rather than quoted from the audit. The
three path-resolution tests are hermetic — they reach an exit-7 stand-in script in a `tmp_path`
tree, so they assert path resolution alone and cannot be moved by this machine's live
`CLAUDE_PROMPTS_DIR` scopes. Delete the fallback and
`test_hook_command_resolves_the_script_without_claude_project_dir` fails. Final state: **8
passed**.

The file carries **no `skipif`** — an earlier draft guarded on `shutil.which("bash")` and tripped
`proof_layer` ("a proof that can be skipped on the machine that breaks the property is not a
mechanism"). A machine with no POSIX shell is a machine where this hook cannot run at all, so
absence now FAILS with the reason named.

---

## 3. The matcher

```
"*"  ->  "Read|Write|Edit|MultiEdit|NotebookEdit|Glob|Grep|Bash|PowerShell"
```

**Fork 2 of the budget — which classes the narrowed matcher names: the filesystem-touching
ones**, which are exactly the classes a stale `CLAUDE_PROMPTS_DIR` makes lie. The L0
`block-onedrive.ps1` guard, the row directly above this one in `ecosystem/organ-index.md`,
already carries `Bash|PowerShell|Edit|Write|NotebookEdit|Read` — the same shape, chosen
independently for the same kind of guard. This is the house pattern, not a new one.

**The refusal is not narrowed.** A mismatch still stops the seat at its first file-touching
call, which is the first thing any session does. What the narrowing buys is the **break-glass**:
`"*"` gated `ToolSearch` too, and `ToolSearch` is the only route to the deferred `ExitWorktree`
/ `SendMessage` tools — which is why the 2026-09-06 wedge could not be undone from inside the
session and recovery took an external shell. A guard that refuses must leave a way to reach the
thing that would unrefuse it.

**Tested before landing, as the contract orders, and in a throwaway session.** Both directions,
so the negative is observed rather than merely absent:

```
narrowed matcher    (Read|Write|Edit|...|Bash|PowerShell)  fired on: Read, Bash
break-glass matcher (ToolSearch|Agent|Task|WebFetch|...)   fired on: <none>
```

A named matcher matches by tool name and does not match-all.

**It landed ARMED, not wired-later.** The guard is live in the lane session under the narrowed
matcher, and every commit after `fa4cf7ae` was authored through it. The recorded memory of this
class is a guard landed unarmed and armed as a separate act that never came.

---

## 4. The A7-6 / M7 smoke — UNMET, and why

The clause: *"one non-Claude CLI call not refused by the guard, proven by the lane before it
commits."* It is **not satisfied**, and the reason is external to the fix.

**The smoke is only non-vacuous against a reader that HONOURS `.claude/settings.json`.** A reader
that ignores the file cannot be refused by the hook, so its passing proves nothing. The lane
measured the honour-set across every non-Claude CLI installed on this machine, by running each
one in a throwaway tree carrying the **old broken hook verbatim** — honour it and you are
refused; ignore it and you read the marker file:

| CLI | Result in the broken-hook tree | Honours the hook file? | Usable as the M7 instrument |
|---|---|---|---|
| `cursor-agent` 2026.09.08 | never reached a tool call — `ActionRequiredError: You've hit your usage limit` | **yes** (recorded by the night mission) | **yes, but vendor-refused today** |
| `codex` v0.153.4 | read `hello.txt`, returned `MARKER-VALUE-8461` | **no** | no — vacuous |
| `copilot` | read `hello.txt`, returned `MARKER-VALUE-8461` | **no** | no — vacuous |
| `gemini` | `IneligibleTierError` — client no longer supported | unknown | no — cannot run |
| `agy` | not probed (same vendor as `gemini`) | unlikely | no |

So the honour-set on this machine is `{cursor-agent}`, and cursor-agent is **authenticated but
usage-limited**: `--list-models` returns the full roster, `--version` returns cleanly, and only
the agent run is refused. This is the same wall the night mission hit on its own attempt 3
(`REVIEW.md`:458), so the row's Done-when was already standing on an instrument that had run out.

**The audit's claim about codex is now verified rather than trusted.** *"`codex` escaped only
because it does not read `.claude/settings.json`. That is luck, and luck does not survive a
deploy."* Measured here, in-lane. `copilot` escapes for the same reason.

### What IS witnessed, labelled as the substitute it is

The hook command executed in a POSIX shell with `CLAUDE_PROJECT_DIR` undefined, cwd = the repo
root — which is precisely what a honouring reader's harness does with it:

```
== CLAUDE_PROJECT_DIR: [<undefined>]

-- OLD shape (what main carried until fa4cf7ae) --
python.exe: can't open file 'C:\Program Files\Git\scripts\fleet_health.py'
   exit=2   <- non-zero from a PreToolUse hook IS the refusal

-- NEW shape --
   exit=0
```

`REFUSED → passes`, the contract's closure transition, on the exact command string the reader
runs. What it does **not** carry is the one thing A7-6 asks for: a real reader making a real tool
call through it. Do not read this table as that.

### The exact re-run, for whoever has quota

```
cd <the tree carrying this fix>
unset CLAUDE_PROJECT_DIR
cursor-agent -p --mode ask --trust "Read ecosystem/doc-counts.md and reply with ONLY the number of collected tests it claims."
```

Pass = it answers with the number. Fail = every tool call refused, which is MA-1 unfixed. The
`--trust` flag is required non-interactively and is not part of the guard.

---

## 5. Residual, named rather than taken — OUT OF FOOTPRINT

The sibling ADR-77 hook in the same `PreToolUse` array still runs

```
python "$CLAUDE_PROJECT_DIR/scripts/hooks/block_immutable_edits.py"
```

and carries the **identical** unresolved-variable defect. It bites a narrower population — its
matcher is `Edit|MultiEdit|Write|NotebookEdit`, so a read-only non-Claude review leg (the ordered
use case, and the one the night mission measured: Read, Shell, Glob, Grep, Task) never reaches
it. The same one-line `${CLAUDE_PROJECT_DIR:-.}` + `[ -f ]` treatment closes it.

`[#684]` says *"two edits, both narrow"* and this lane's contract forbids edits outside its
footprint, so this is **reported for filing, not taken**. It is a candidate row, not a lane act.

---

## 6. Gate state, honestly

**Pre-existing RED, not attributable to this diff:**
`tests/test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent`
— reproducible in isolation (63 s), and deductively not this lane's: the fixture is hermetic in
`tmp_path`, its script closure is `block_unanchored_push` + `block_ff_push` + `journal_anchor`,
and this lane's diff touches none of them. Adjacent targeted run: **268 passed, 1 failed**.

**Declared single-hook bypass, on all four commits: `SKIP=audit-health`.** The sole `[!!]` is
`journal_spine_anchor` on `2040653c` — **main's own tip**, not this diff.
`worktree-batch-w-anchor` carried ONE commit (`2781094a`), so its `--no-ff` merge introduces
`{2040653c, 2781094a}` and the JOURNAL entry inside `2781094a` cannot name its own hash:
structurally unanchorable, and it blocks every commit in the repo until an integrator **appends**
a discharging entry. Discriminator, run from a tree `git ls-remote` confirms is exactly at
`origin/main`:

```
introduced:            2040653c..., 2781094a...
anchored in this tree: False
anchored at main:      False
```

A lane does not journal (`STANDING_RULINGS` P-1), so the fix is not this lane's to make. No
`--no-verify` anywhere: one named hook, declared in every commit body.

**Regenerated in-lane, because both gates BLOCK and both deltas are consequences of this lane's
own footprint** — not the integrator's Q1 index regen:
`ecosystem/doc-counts.md` (5723 → 5731, exactly this file's 8 tests) and
`ecosystem/organ-index.md` (one row, the matcher itself, still `ARMED`).

---

## 7. Commits

| SHA | Step |
|---|---|
| `fe90dc25` | RED-first witness — the wiring test, 5 failed / 3 passed |
| `fa4cf7ae` | the hook resolves its own repo root — 3 legs RED → GREEN |
| `7101448d` | the matcher narrows off `"*"` — 2 legs RED → GREEN, 8 passed |

**No leftovers:** every probe tree lives under the job tmp dir, never in the repo;
`git status --untracked-files=all` on the worktree is clean.

---

## AMENDMENT — 2026-09-11, the fix round (AW6-2, `FIX-BATCH-W-002-guard-root.md`)

> **In-file amendment marker (critical rule 3).** This artifact is immutable and **nothing
> above this line is edited**. Everything below records the fix lane AW6-2 dispatched into
> this same worktree, on this same branch, resuming the lane rather than opening a new one.

### A0. The premise AW6-2 states, corrected — and it was corrected in-contract

AW6-2 asks this lane to *"resolve the unresolved HIGH"* from *"the integrator's W-2 review
tally"*. **There was no such tally and no such HIGH**: no review of this branch had ever been
run. The integrator recorded exactly that — `W-2 ... @ 8634f5f6 code EXIT 1 HELD review=NONE`,
refused because *"code branch carries no `review=` token"*, with §9 finding *"no reviewer tally
of any kind"* and §10 *"I did not run the reviews myself. D-1 makes review a LANE act."*

The operator's dispatch of 2026-09-11 chose §10's second way out: **re-dispatch the lane to
review its own branch.** So this round did not resolve someone else's findings — it produced
the review that never existed. The correction was already made in the fix contract, so it
consumed no fork and triggered no PAUSE.

### A1. The review — four passes, all of them fresh

Tally: review=lane reviewer=gpt-5.6-terra findings=5 fixed=5

**Tally:** 0/5/0/0

`review=lane` because D-1 makes review a lane act and this lane performed it; the reviewer that
actually ran is the contracted one. **The model is verified, not trusted:** `-c
model=gpt-5.6-terra` was passed, and each session's own `turn_context` was then read back from
`~/.codex/sessions/2026/09/11/` — `model=gpt-5.6-terra effort=high` on all four. That check
exists because the recorded scar in this repo is terra silently executing as sol ([#469]).

| Pass | Tree reviewed | Raised | Outcome |
|---|---|---|---|
| 1 | `8634f5f6` | 3 HIGH | all three resolved — A2 |
| 2 | `537f23eb` | 1 HIGH | resolved — A2.5 |
| 3 | `6c31cf52` | 1 HIGH | resolved — A2.6 |
| 4 | `deeb1b8e` | **0 — clean in every band** | nothing owed |

Passes 2-4 were not asked for. They were run because **recording a tally changes the tree that
was tallied**: a tally naming only pass 1 would describe a tree three commits stale. Pass 4
exists so the tally describes the tip being handed back.

`codex exec` invocation: `--sandbox read-only -c model=gpt-5.6-terra -c
model_reasoning_effort=high --output-last-message <file> -`, prompt on stdin.

> **The contract's codex trap is precise but easy to misread, and it cost nothing to resolve
> live.** `codex exec` at 0.153.4 **does** accept `-s/--sandbox` (`read-only`,
> `workspace-write`, `danger-full-access`). It is the `codex exec review` SUBCOMMAND that has
> no such flag. The wrapper's free-form path is therefore correct as written.

### A2. Pass 1 — the three HIGH, each resolved on the merits

#### HIGH-1 · `.claude/settings.json` · a missing guard script silently bypasses the check

*"`[ -f "$g" ] || exit 0` approves the tool call whenever `CLAUDE_PROJECT_DIR` is non-empty but
wrong, or the guard file is absent/moved."*

**PARTLY A REAL DEFECT, and the real half was fixed** (`a6c81952`). `${VAR:-.}` defaults only on
unset-or-empty, so a variable set to the WRONG root skipped the cwd fallback entirely and fell
through to fail-open — **passing without consulting a guard that was sitting in cwd all along.**
Measured, not reasoned:

```
wrong non-empty CLAUDE_PROJECT_DIR, guard present in cwd
  OLD rc=0   <- silent bypass, guard never consulted
  NEW rc=7   <- guard reached
```

The command now makes a SECOND `[ -f ]` attempt at cwd before giving up.

**The other half is NOT a defect and is kept.** Total absence of the script failing open is the
module's ruled posture — `prompts_guard()`'s own docstring reserves refusal for *"a mismatch it
positively established"* — and it grants no capability an attacker lacks: anyone who can move
the script or set the environment can also edit the settings file that declares the hook. Fail-
open is now reserved for the case where NO root resolves, which is how the posture was always
argued.

#### HIGH-2 · `.claude/settings.json` · the matcher excludes filesystem-capable routes

**SPLIT — four names adopted, two refused** (`ea3f1b9d`).

ADOPTED: `Monitor|LSP|ReadMcpResourceTool|mcp__.*`. The reviewer is right that an `mcp__*`
filesystem tool reaches a wrongly-resolved directory without passing the guard. `LSP` and
`ReadMcpResourceTool` are **not in this client's roster** — a matcher branch naming a tool that
does not exist is inert, so over-listing costs nothing and under-listing is a gap. They are
carried for consumers and labelled unverified rather than claimed as present.

REFUSED, argued rather than dismissed: `EnterWorktree` / `ExitWorktree`. They are the break-
glass family, and gating them recreates the terminal wedge `[#684]` exists to prevent.

**The review sharpened this rather than weakening it.** The break-glass is a ROUTE *and* a
DESTINATION: `ToolSearch` is only the way to REACH the deferred session-control tools, so gating
what it reaches defeats the escape as surely as gating the route. `_MUST_NOT_MATCH` had pinned
`ToolSearch` alone; it now pins `ExitWorktree` and `SendMessage` beside it — and `EnterWorktree`
after pass 2. `Agent` is not a gap by the reviewer's own concession: configured hooks run for a
subagent's own tool calls.

#### HIGH-3 · `tests/...` · the "real guard" test accepted ambient results

**ACCEPTED IN FULL** (`c147f17d`). `rc in (0, 2)` passed whether this machine's two scopes agreed
or not, so it could not distinguish "ran and passed" from "ran and refused" — nor catch a command
converting one into the other, which is the one regression the fail-open leg makes possible.

The live-tree test now asserts EQUIVALENCE with a direct guard invocation through the same shell
and interpreter. The load-bearing half is a NEW hermetic test: a stand-in exiting 2 in a
`tmp_path` tree pins refusal-propagation on any platform, removing the registry half of the real
verdict from the question entirely.

### A2.4 A HIGH this lane raised itself — the suite was silently PATH-dependent

Not a Codex finding. Found while verifying HIGH-3, and a real defect in this lane's own test
file (`537f23eb`). `_SH = shutil.which("bash")` is not enough on Windows:

```
session A   which -> C:/Program Files/Git/bin/bash.exe     12 passed
session B   which -> .../WindowsApps/bash.EXE               8 failed, 4 passed
```

Session B's PATH put `WindowsApps` first, so `which` returned the **WSL app-execution-alias
stub**. With no distro installed that stub exits 1 and writes its message to **stdout**, leaving
stderr EMPTY — so every shell-backed test failed with `rc=1 stderr=''` and nothing pointed at the
cause. The worse case is the silent one: a WSL bash WITH a distro runs fine and returns plausible
codes while asserting the hook's behaviour under a shell that cannot see this repo's Windows
paths at all.

Candidates are now validated by RUNNING them (`[ -f "<settings.json>" ]`, which a shell that
cannot see Windows paths fails). No `skipif` was added — absence still FAILS with the reason
named, per `proof_layer`.

### A2.5 Pass 2 — a decision no test could fail

`_MUST_NOT_MATCH` pinned `ExitWorktree` and `SendMessage` but not `EnterWorktree`, though the
comment beside it rules BOTH worktree tools out. A later edit could have gated `EnterWorktree`,
re-blocking part of the documented recovery path, with every test still green. **Accepted in
full** (`6c31cf52`).

### A2.6 Pass 3 — MA-1 again, by a different missing piece

The sole HIGH of pass 3, and the most serious finding of the whole round: **the two `[ -f ]` legs
guard the SCRIPT's existence and said nothing about the INTERPRETER's.** A reader with no usable
`python` got a non-zero exit from the hook and therefore TOTAL REFUSAL of every matching tool
call — the exact failure this row exists to close, and a direct contradiction of the intent the
night-mission audit states in its own words: *"fails open on interpreter failure"*
(`REVIEW.md`:102). The shipped fix honoured the first half of that sentence and not the second.

```
...; python "$g" --prompts-guard; rc=$?; [ "$rc" = 2 ] && exit 2; exit 0
```

`prompts_guard()` returns 0 or 2 and NOTHING else, so mapping "exactly 2" to refusal and every
other status to pass loses no refusal the guard can express. Measured with an absolute-path
shell, because a first attempt using `env PATH="" bash` measured nothing — `env` could not find
`bash` either, and returned 127 of its own:

```
no interpreter (PATH="")   BEFORE rc=127 (refuses everything)   AFTER rc=0
guard refuses              BEFORE rc=2                          AFTER rc=2
```

The refusal is untouched at full force; only failures to RUN the guard changed. Landed
`deeb1b8e`, with two hermetic RED-first witnesses (no interpreter; guard crashes on import).

The "reached" signal changed with it — it was an exit of 7, which the new mapping folds to 0. It
is now a **marker on stdout**, which is better evidence anyway: it says WHICH file ran, not merely
that something did. The fail-open test now also asserts the marker is ABSENT, so its pass cannot
come from a stand-in that executed anyway.

### A2.7 Pass 4 — clean

Verbatim: *"Diff is clean. No remaining findings."* — `(none)` in all four bands, with each of
the four targeted questions answered in the affirmative (status mapping loses no refusal; `rc=$?`
captures the right command; refusal stderr still reaches the model; nothing newly lets a real
scope mismatch through).

### A3. The A7-6 / M7 smoke — RE-MEASURED TODAY, still externally blocked

Done-when 4's second branch. The clause is **not** weakened and **not** faked.

**Probed FIRST, before any other work, as the contract orders.** `cursor-agent` is still
installed at `2026.09.08-6caf4ff`, still authenticated — `--list-models` returns the full roster
— and the agent run is still refused, verbatim, at **2026-09-11 13:36:42 +02:00**, from the
fixed tree with `CLAUDE_PROJECT_DIR` undefined:

```
ActionRequiredError: You've hit your usage limit Get Cursor Pro for more Agent usage, unlimited Tab, and more.
```

A vendor quota is not a defect in the guard. The honour-set is unchanged at `{cursor-agent}`, and
**one cell of W-2's table that was an ASSUMPTION is now a measurement**:

| CLI | Honours `.claude/settings.json`? | Basis |
|---|---|---|
| `cursor-agent` | yes | night mission; still the only instrument, still quota-refused |
| `codex` | no | W-2, measured 2026-09-11 |
| `copilot` | no | W-2, measured 2026-09-11 |
| `gemini` | n/a | client ineligible |
| `agy` 1.1.28 | **no — MEASURED, was "unprobed, unlikely"** | this round, below |

`agy` was run in a throwaway tree carrying the **old broken hook verbatim** (matcher `"*"`, bare
`$CLAUDE_PROJECT_DIR`), whose refusal was confirmed first (`exit=2`, `can't open file`). It read
the marker file straight through:

```
2026-09-11 13:39:49 +02:00   agy --dangerously-skip-permissions '--print=Read the file hello.txt ...'
MARKER-VALUE-8461
exit 0
```

So `agy` is a **vacuous instrument, not a passing one** — same class as `codex` and `copilot`.
Its flag order is a trap worth recording: `agy -p --dangerously-skip-permissions "<prompt>"`
takes the FLAG as the prompt and silently ignores the real one; the prompt must be attached
(`--print=...`).

**Net: Done-when 4 closes on its second branch — re-measured today, still externally blocked,
with the refusal recorded verbatim.** The measurement also shrank the gap: the honour-set is now
fully measured rather than partly assumed.

### A4. Gate state and test evidence

**`SKIP=audit-health` declared on every commit of this round, as in the first** — and this round
went back and CHECKED what that skip was hiding, which the first did not:

```
audit.py health -> DEGRADED (rc=0; the [~~] rows are WARN, not FAIL)
sole [!!]       -> journal_spine_anchor, now FOUR first-parent spine entries
                   (e6f11215, a3374b70, 3acca581, 2040653c) -- main has advanced
                   since W-2 recorded ONE. All four are main's own merges.
grep of every health finding for this lane's touched files -> NO MATCH
```

A lane does not journal (`STANDING_RULINGS` P-1), so none of it is this diff's to fix. No
`--no-verify` anywhere; one named hook, declared in every commit body.

**Targeted tests — the lane's actual obligation** (`CLAUDE.md`: *"In a lane run the targeted
tests for that lane's diff; the full suite runs once, at integration"*, `[#528]`). Every test file
in `tests/` mentioning `settings.json`, `prompts_guard`, `fleet_health`, `organ_index` or
`doc_counts` — 30 files:

```
1501 passed, 12 failed in 465s
```

**None of the 12 is in this lane's footprint**, and the two surfaces this diff owns are green:
`test_prompts_guard_hook_wiring.py` **14 passed** (run in BOTH shells that disagreed before the
`_resolve_posix_shell` fix) and `test_fleet_health.py` **179 passed** — the guard's own verdict
function, untouched by any of this. The 12 are `test_audit` health ×2 (main's anchor gap, above),
`test_gen_audit_index` ×2, `test_canonical_docs` ×2 (PLAYBOOK re-stamp), `test_gen_handoff` ×4,
`test_enforcement_coverage` ×1 (the one W-2 already recorded) and `test_v6_frozen_contract` ×1.

The `test_gen_audit_index` pair is **proven** pre-existing rather than argued: `git show
8634f5f6:docs/audits/README.md` does not list this artifact, so W-2's own commit added it without
indexing it. [#590] deliberately narrowed `audit-index-freshness` to
`(^docs/audits/README\.md$|^scripts/gen_audit_index\.py$)` precisely so a lane does NOT have to
touch the shared index — it put that file in 6 of the last 7 conflicted merges. **So this lane
does not regenerate it**, and the ship-tier `generated_artifact_freshness` leg is where it is
caught, by design.

**The full suite was ALSO run, and it is NOT green — stated plainly:**

```
51 failed, 5676 passed, 10 skipped in 2281s (0:38:01)
```

**An honest limit on that number, because the listing is truncated.** The run was piped through
`tail`, so only 24 of the 51 `FAILED` lines were captured. Neither of this lane's two test
surfaces appears among those 24, and every failing FILE among them is one this diff does not
touch (`test_fleet_analytics` ×10, all `ModuleNotFoundError: No module named 'pandas'`;
`test_normalize_headers` ×4 and `test_toc`, all *"corpus implausibly small (0) — glob is wrong"*;
`test_proof_layer`, whose finding `audit.py health` independently identifies as
`test_review_artifact_coverage.py`, not this file). **The remaining 27 were not enumerated and no
claim is made about them** — a truncated listing is not evidence of absence. The box was also
carrying a SECOND concurrent pytest run from another seat throughout.

The full suite at integration is the authority on that population; this lane reports what it
measured and does not launder it.

`ecosystem/doc-counts.md` and `ecosystem/organ-index.md` were regenerated in-lane: both deltas
are consequences of this lane's own footprint (its test count, and the matcher IS that organ row).

### A5. Residual — still OUT OF FOOTPRINT, and now worse than §5 recorded

The sibling ADR-77 hook in the same `PreToolUse` array still runs

```
python "$CLAUDE_PROJECT_DIR/scripts/hooks/block_immutable_edits.py"
```

§5 named its unresolved-variable defect. Pass 3 shows it carries the **second** defect too: no
interpreter guard. Both one-line treatments from this round close it. Still reported for filing,
not taken — `[#684]` says *"two edits, both narrow"* and the contract forbids edits outside the
footprint.

**Accepted residual, named rather than hidden:** `_resolve_posix_shell` retains a `shutil.which`
fallback, so some environment dependence remains. Pass 3 noted this in prose and did NOT rate it
in any severity band. It is bounded deliberately — every candidate, including the fallback, is
validated by execution before use.

### A6. Commits of this round

| SHA | Step |
|---|---|
| `a6c81952` | HIGH-1 — a wrong `CLAUDE_PROJECT_DIR` no longer skips a resolvable guard |
| `ea3f1b9d` | HIGH-2 — the matcher covers the MCP and secondary filesystem routes |
| `c147f17d` | HIGH-3 — the wiring test binds to the guard's verdict, not to a set |
| `537f23eb` | lane-raised — the POSIX shell is resolved by RUNNING it, not by `which()` |
| `6c31cf52` | pass 2 — `EnterWorktree` pinned in the break-glass roster |
| `deeb1b8e` | pass 3 — only the guard's own refusal code refuses |

**No leftovers:** every probe tree and review artifact of this round lives under the job tmp dir,
never in the repo.

### A7. Handback

HANDBACK worktree-lane-w-684-pretooluse-guard-root @ deeb1b8e code review=gpt-5.6-terra HIGH:0 MED:0 LOW:0

**`HIGH:0` is UNRESOLVED-at-tip, not raised.** Five HIGH were raised across four passes and all
five are resolved; `**Tally:** 0/5/0/0` above is what was RAISED. The two numbers describe
different things on purpose.

**The one gap in Done-when 3, stated outright rather than papered over.** The HANDBACK names
`deeb1b8e`, which is the tip pass 4 reviewed and found clean. The commit the integrator actually
merges is the one carrying THIS amendment, sitting on top of it — a fixpoint no artifact can
satisfy, since recording a tally changes the tree the tally describes. What bounds it: **that
commit is docs-only.** It touches this file and nothing else — no code, no test, no config, no
generated surface — so every file pass 4 examined is byte-identical between `deeb1b8e` and the
tip. The `by-HEAD` linkage leg admits it: `deeb1b8e` is a commit the merge introduces.

**No merge, no push.** AW6-2 makes the merge conditional on this review, and the merge is the
integrator's act from the primary checkout.