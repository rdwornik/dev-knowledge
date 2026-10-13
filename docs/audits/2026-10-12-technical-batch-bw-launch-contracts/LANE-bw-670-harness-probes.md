# LANE lane-bw-670-harness-probes — ADR-123 step 0 probe receipts for N=1 corp-monorepo, read-only in the consumer

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
claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-bw-670-harness-probes "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-bw-670-harness-probes.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-bw-670-harness-probes.md` **from the target repo root** — the hub shim over
`scripts/dispatch.py launch`, which runs the hub's launcher without changing
directory (PLAYBOOK Ch8's dispatch table, the sole literal-command site). From
the hub checkout itself, `uv run --locked python scripts/dispatch.py launch LANE-bw-670-harness-probes.md`
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
and `--worktree lane-bw-670-harness-probes` — the name that produces `worktree-lane-bw-670-harness-probes` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #670 · lane-bw-670-harness-probes]`.
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
generator writes is one `dispatch.py` accepts. A lane already holding `worktree-lane-bw-670-harness-probes`
is refused earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-bw-670-harness-probes` -> branch `worktree-lane-bw-670-harness-probes` -> contract `LANE-bw-670-harness-probes.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Context

**Batch:** BW (B2-W4 finish), wave D · **Manifest:** `docs/audits/2026-10-12-technical-batch-bw-manifest.md` (its §4 lane rules bind this lane) · **Order:** `to-cc/BATCH-B2-W4-CC-FINISH-2026-10-12.md` F3/F4 + `to-cc/AMEND-BATCH-B2-W4-CC-FINISH-R99-2026-10-12.md` + `to-cc/BATCH-B2-W4-COPILOT-2026-10-11.md` Wave D (Done-when verbatim below) + `to-cc/BATCH-BW-NIGHT-2026-10-13.md` · **Frozen on:** Wave C's integration commit (this file rides `land --slug b2-w4-c`). · **Row:** `[#670]` nearest; read-only in `corp-monorepo`.

**Order Done-when (verbatim):** D6 `harness-probes`: the ADR-123 step 0 receipts for N=1 `corp-monorepo`; read-only in the consumer.

## Why

ADR-123 §Migration step 0 (Probes before build): P-1 a Claude Code plugin materialised from package data loads in a fresh codespace (`CLAUDE_CODE_PLUGIN_SEED_DIR` or project `.claude/`), witnessed by one hook firing; P-2 `uv add "dk-harness @ git+https://...#subdirectory=packages/harness"` resolves under the pinned uv 0.11.19 in a fresh codespace; P-3 a lane runs with the hub unreachable after `postCreateCommand`. Exit: three receipts; any failure routes to §Flip-condition. Layer 2 never executes in a child repo: this lane writes NOTHING in `corp-monorepo` (read-only) — receipts live in the hub.

## Done-contract (immutable)

1. Three receipts (P-1, P-2, P-3) under the hub's existing receipts/audits home, each with command, exit code, evidence (log excerpt, codespace name, timestamp) and verdict PASS/FAIL — or `NOT_RUN` with the exact blocker.
2. A codespace credential or billing block is `INPUT_REQUIRED` with the exact `operator_action` (e.g. `gh auth refresh -s codespace`), never worked around; the codespace (if created) is stopped and deleted by the lane before handback, and its deletion recorded (no leftovers).
3. `git -C <corp-monorepo> status` before/after shows no change made by this lane.
4. A FAIL routes to ADR-123 §Flip-condition: the LANE REPORT names which.
5. Docs and code in English; hyphen-only names; logging rather than print; Click for a CLI where one is warranted; targeted `pytest` green; `ruff` clean.
6. **Close-out:** the review record carries the served model id and session id from Codex's own output and the nonce it returned (R59).

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
