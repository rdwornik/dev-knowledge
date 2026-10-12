# LANE lane-bw-1001-sessionstart-one — the SessionStart injections are measured and replaced by one bounded injection

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
claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-bw-1001-sessionstart-one "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-bw-1001-sessionstart-one.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-bw-1001-sessionstart-one.md` **from the target repo root** — the hub shim over
`scripts/dispatch.py launch`, which runs the hub's launcher without changing
directory (PLAYBOOK Ch8's dispatch table, the sole literal-command site). From
the hub checkout itself, `uv run --locked python scripts/dispatch.py launch LANE-bw-1001-sessionstart-one.md`
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
and `--worktree lane-bw-1001-sessionstart-one` — the name that produces `worktree-lane-bw-1001-sessionstart-one` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #1001 · lane-bw-1001-sessionstart-one]`.
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
generator writes is one `dispatch.py` accepts. A lane already holding `worktree-lane-bw-1001-sessionstart-one`
is refused earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-bw-1001-sessionstart-one` -> branch `worktree-lane-bw-1001-sessionstart-one` -> contract `LANE-bw-1001-sessionstart-one.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Context

**Batch:** BW (B2-W4 finish), wave C · **Manifest:** `docs/audits/2026-10-12-technical-batch-bw-manifest.md` (its §4 lane rules bind this lane) · **Order:** `to-cc/BATCH-B2-W4-CC-FINISH-2026-10-12.md` F3 + `to-cc/BATCH-B2-W4-COPILOT-2026-10-11.md` Wave C (Done-when verbatim below) · **Ratified by:** R96 (`to-browser/RATIFICATION-2026-10-11.md`; package `to-browser/DIGEST-RATIFICATION-PACKAGE-2026-10-11.md` P1/P2) · **Frozen on:** F1's integration commit (this file rides `land --slug b2-w4-f1`). · **Row:** `[#1001]` owner.

**Order Done-when (verbatim):** C4 `sessionstart-one`: the 9 SessionStart injections are measured and replaced by one bounded injection.

## Why

R96 D9 (package T5.4; `.claude/settings.json:93`, bytes UNVERIFIED in the package). Row `[#1001]`: SessionStart becomes one stdlib reader — N interpreters to 1, p90 under 2 s. `CLAUDE.md` §9 names 8 SessionStart hooks; the order says 9 — count them in the live `settings.json` and state which number is true. **This lane edits `.claude/settings.json`, so it bases on F1's landed shared hook launcher (`lane-bw-1001-hook-launcher`)**: anything it registers goes THROUGH that launcher, never as inline code.

## Done-contract (immutable)

1. MEASURE first, committed as an artifact under an existing home: for each current SessionStart entry, the bytes it injects into context and its wall time (p50/p90 over at least 5 runs on this box). Record the true count.
2. RED-first: a test asserts `.claude/settings.json` registers exactly ONE SessionStart command, launched through the shared launcher, and that its injected output is bounded (a byte cap as a named constant; the measured total and the cap in the commit body).
3. The one entry runs the former readers in ONE interpreter (import, not a subprocess per reader), stdlib only, and keeps every refusal or advisory line a test pins; a reader that is dropped is listed with why — nothing is dropped silently.
4. p90 wall time under 2 s on this box (measured and recorded), or the measured p90 and the reason it is not met.
5. R8 usage test: start one `copilot -p` (or `claude -p`) session at the worktree root and record the size of the injected SessionStart text.
6. Docs and code in English; hyphen-only names; logging rather than print; Click for a CLI where one is warranted; targeted `pytest` green; `ruff` clean.
7. **Close-out:** the review record carries the served model id and session id from Codex's own output and the nonce it returned (R59).

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
