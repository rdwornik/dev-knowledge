# LANE lane-bw-912-known-reds-expiry — known-reds entries expiring 2026-10-16/17 are fixed, removed on evidence, or listed

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

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
claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-bw-912-known-reds-expiry "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-bw-912-known-reds-expiry.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-bw-912-known-reds-expiry.md` **from the target repo root** — the hub shim over
`scripts/dispatch.py launch`, which runs the hub's launcher without changing
directory (PLAYBOOK Ch8's dispatch table, the sole literal-command site). From
the hub checkout itself, `uv run --locked python scripts/dispatch.py launch LANE-bw-912-known-reds-expiry.md`
is the same act typed in full. The launcher reads this `## Dispatch`
block for its fields — model, effort, worktree, permission mode — and builds the
session's own argv; it never runs the block. The `$env:CLAUDE_PROMPTS_DIR`
token is how a frozen contract names its own location without hard-coding an
absolute path. The repo root still matters: the worktree
is created relative to the current repo, so dispatching from the wrong one
lands the lane in it.

The line carries every dispatch constant rather than defaulting it:
`--permission-mode bypassPermissions` (a `--bg` lane has nobody to answer a
permission prompt, so a default would stall it silently), `--bg`,
and `--worktree lane-bw-912-known-reds-expiry` — the name that produces `worktree-lane-bw-912-known-reds-expiry` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #912 · lane-bw-912-known-reds-expiry]`.
**The model is ON the line, not defaulted** (`[#717]`): it is rendered from the
routing table above, so this lane dispatches at `opus` whatever any
surface default (`opus`, the `.dev-knowledge` default per the Ch8
routing matrix) happens to be. A line that omitted it would silently re-decide
the most expensive constant on it. Effort is a closed enum:
{low | medium | high | xhigh | max}; a value outside it is refused with the enum named,
rather than guessed.

**The `claude` head token is required, not stylistic** (`[#675]` clause 1 /
AX25-2). The launcher admits a `claude`, `codex` or `copilot` head and refuses
any other program, so a contract's `## Dispatch` block is not a place to name a
helper. Until 2026-09-12 this generator emitted a different head here and
**every contract it produced was refused by the reader meant to launch it**;
`tests/test_dispatch_conformance.py` is the standing witness that the fence this
generator writes is one `dispatch.py` accepts. A lane already holding `worktree-lane-bw-912-known-reds-expiry`
is refused earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-bw-912-known-reds-expiry` -> branch `worktree-lane-bw-912-known-reds-expiry` -> contract `LANE-bw-912-known-reds-expiry.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Context

**Batch:** BW (B2-W4 finish), wave F1 · **Manifest:** `docs/audits/2026-10-12-technical-batch-bw-manifest.md`
(its §4 lane rules bind this lane) · **Rows:** `[#912]` `[#664]` `[#1340]` `[#1341]` `[#1343]`
`[#1344]` owners · **Order:** F0.4.

## Why

`logs/KNOWN-REDS-REGISTRY.json` carries 40 entries for `[#912]` expiring 2026-10-16 (20 node ids,
`members` + `members_by_os.windows-latest`) and 26 expiring 2026-10-17 (`[#664]` 15, `[#1340]`,
`[#1341]`, `[#1343]` 3 each, `[#1344]` 2). From an expired date `land` refuses every merge
(`scripts/known_reds.py:264`, the "EXPIRED … fix it, or re-date it by a recorded ruling" problem).
There is **no R98** in `to-browser/RATIFICATION-2026-10-12.md`: **re-dating is FORBIDDEN** in this lane.

## Done-contract (immutable)


1. **Fix at cause** every entry you can: the test goes green on its OS for a real reason (code or
   test repair, RED-first where the fix is in code), and its registry entry is removed in the same
   commit.
2. **Remove on evidence** an entry whose red no longer reproduces: cite the witness run — main's
   CI run 38249609543 (sha `c1b65e6d`, windows and ubuntu `known_reds.py compare` output lists
   which members are `known`, i.e. still red) plus a local run on this Windows box. An entry not
   listed `known` in that run for its OS AND green locally is removable; say which for each.
3. Every remaining expiring entry is listed in the LANE REPORT with the reason it is not fixed,
   and the lane state is `INPUT_REQUIRED` with `operator_action: "rule R98: re-date or fix <list>"`
   if any remain. Nothing is re-dated.
4. `tests/test_known_reds.py` green; `uv run --locked python scripts/known_reds.py --help` lists
   any validation verb — run it on the edited registry and record exit 0.
5. Close-out: the review record carries the served model id and session id from Codex's own output.

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

1. Boot: confirm the worktree path and branch, seed check (manifest §4 rule 1). **COMMIT** nothing yet.
2. Work the Done-contract above in order, RED-first where code changes (§4 rules 2-3). **COMMIT** per step.
3. Review with Codex until APPROVE (§4 rule 6); usage test where it applies (§4 rule 7). **COMMIT** fixes.
4. Push the lane branch only, write the LANE REPORT (§4 rules 4, 9), hand back (§4 rule 8), **then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
