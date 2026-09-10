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
