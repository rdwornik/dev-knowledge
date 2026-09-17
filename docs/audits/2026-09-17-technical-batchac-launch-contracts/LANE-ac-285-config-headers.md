# LANE lane-ac-285-config-headers — Remove the gitignored settings.local.json merge allow and stamp PLAYBOOK and ENVIRONMENT behind a genuine end-to-end re-read

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

## Organs and rows

**`organs:`** -- the organ(s) this lane MUST use. Before writing ANY query or ordering ANY scan, NAME THE ORGAN THAT ALREADY ANSWERS IT. New code ONLY for what no organ answers, and FILE THE GAP AS A ROW when that happens. **A lane that could have used an organ and did not MUST say so in its handback.**

- `ecosystem/organ-index.md` -- gate coverage: which gate reaches which file
- `gen_task_tree` over `tasks/` -- the BACKLOG row index for `[#285]` and any existing header row
- `canonical_docs.py::FRESHNESS_FILES` + `audit.py::_HUB_ONLY_FRESHNESS_FILES` -- the stamped set is COMPUTED, never restated

**`rows:`** -- the open row(s) this lane's subject already belongs to, resolved against the live index at freeze. A lane whose subject already has a row is RE-SCOPED to that row rather than duplicating it.

- `[#285]` PRIMARY -- extend hub freshness gating to PLAYBOOK; **status DEFER**, and its scope was already WIDENED 2026-09-05 to cover `protocols/ENVIRONMENT.md` alongside `protocols/PLAYBOOK.md` -- exactly this lane's two files, so this lane RE-SCOPES to it and files no rival row
- `[#863]` -- owns the hook/settings surface this lane's P4 half touches

**Library ladder** for anything genuinely new: stdlib > established dependency > proven project > industry pattern; hand-roll only on a MEASURED divergence, recorded so it is not relitigated.

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

**Kind:** `code` — changes executable code — `scripts/`, `tests/`, hooks, schema, generators.

The kind is DECLARED, not inferred, and it is what the routing default keys on
(`[#885]` clause 2). A text-only, deletion or read-only-digest lane never starts on
Opus; a review lane is not dispatched from a lane contract at all, because
`ecosystem/routing-table.yaml` is the authority for which CLI runs that role; a code lane
plans on Opus and implements on Sonnet **as two sessions with a file between them**,
never as one session changing tier mid-flight. The prompt cache is keyed PER MODEL,
so a mid-session switch re-writes the whole context: at this repo's measured mean of
232,875 tokens per call, one switch costs USD 1.46 into Opus or USD 0.58 into Sonnet
against USD 0.0812 saved per turn moved — about 25 consecutive cheap turns to repay
one round trip. Anything shaped like plan-then-execute is TWO SESSIONS.

```
claude --bg --model sonnet --effort high --permission-mode bypassPermissions --worktree lane-ac-285-config-headers "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-ac-285-config-headers.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-ac-285-config-headers.md` **from the target repo root** — the ruled verb for a local
lane (PLAYBOOK Ch8's dispatch table, the sole literal-command site). The verb
reads this `## Dispatch` block and runs it **verbatim**, substituting exactly
one literal — `$env:CLAUDE_PROMPTS_DIR` — which is how a frozen contract
names its own location without hard-coding an absolute path. That spelling is
load-bearing: it is the only token the reader replaces, and any other
placeholder is passed through untouched into a real session's prompt.
The repo root still matters: the worktree
is created relative to the current repo, so dispatching from the wrong one
lands the lane in it.

The line carries every dispatch constant rather than defaulting it:
`--permission-mode bypassPermissions` (a `--bg` lane has nobody to answer a
permission prompt, so a default would stall it silently), `--bg`,
and `--worktree lane-ac-285-config-headers` — the name that produces `worktree-lane-ac-285-config-headers` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #285 · lane-ac-285-config-headers]`.
**The model is ON the line, not defaulted** (`[#717]`): it is rendered from the
routing table above, so this lane dispatches at `sonnet` whatever any
surface default (`opus`, the `.dev-knowledge` default per the Ch8
routing matrix) happens to be. A line that omitted it would silently re-decide
the most expensive constant on it. Effort is a closed enum:
{low | medium | high | xhigh | max}; a value outside it is refused with the enum named,
rather than guessed.

**The `claude` head token is required, not stylistic** (`[#675]` clause 1 /
AX25-2). The verb refuses any other program — *"this script never runs an
arbitrary command from a contract file"* — so a contract's `## Dispatch` block
is not a place to name a helper. Until 2026-09-12 this generator emitted the
deprecated `Dispatch-Lane` alias here and **every contract it produced was
refused by the verb meant to launch it**. That alias still resolves as the
manual fallback and adds a skip-if-`worktree-lane-ac-285-config-headers`-exists guard the verb path does
not have; that guard's job is done earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-ac-285-config-headers` -> branch `worktree-lane-ac-285-config-headers` -> contract `LANE-ac-285-config-headers.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. The `Bash(git merge *)` allow is REMOVED from the gitignored `.claude/settings.local.json`. An untracked file overriding a tracked one is a real defect and this is P4's buildable half.
2. The **REFUSAL half** of P4 moves to a `deny` rule or a `PreToolUse` exit 2, **or** is scoped to the INTEGRATOR surface. `allow` and `ask` are **INERT under `bypassPermissions`**, which every lane uses, so they may NOT be used to express a refusal (§3 Class A).
3. Whether ab-834's `protocols/` heading gate actually **REACHES** `protocols/PLAYBOOK.md` and the environment file is ESTABLISHED and STATED. If the gate does not reach them, the handback SAYS SO -- a header added by hand under a gate that ignores the file WILL ROT AGAIN.
4. **`[#285]`'s standing prohibition binds this lane and outranks the convenience of a green gate: a bare stamp to green a gate is FORBIDDEN.** A `last_updated` / `last_reviewed` stamp lands ONLY behind a genuine end-to-end re-read, evidenced by per-section notes in the stamping commit. **If the re-read is not done, the stamp is NOT applied and the lane reports the gap** -- that is a passing outcome, not a failure.
5. Docs and code in English; hyphen-only names; logging rather than print; `pytest` green.

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. Read `[#285]` in full and the two files' current header state; establish the gate's actual reach. **COMMIT**
2. Remove the `settings.local.json` allow; move or scope the refusal half. **COMMIT**
3. Apply headers ONLY behind a genuine re-read with per-section notes, or report the gap. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
