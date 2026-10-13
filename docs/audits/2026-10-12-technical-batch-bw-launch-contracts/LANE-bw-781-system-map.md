# LANE lane-bw-781-system-map — a generated drill-down system map (JSON and static HTML, no LLM) with a /map command and a recorded map sha

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
claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-bw-781-system-map "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-bw-781-system-map.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-bw-781-system-map.md` **from the target repo root** — the hub shim over
`scripts/dispatch.py launch`, which runs the hub's launcher without changing
directory (PLAYBOOK Ch8's dispatch table, the sole literal-command site). From
the hub checkout itself, `uv run --locked python scripts/dispatch.py launch LANE-bw-781-system-map.md`
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
and `--worktree lane-bw-781-system-map` — the name that produces `worktree-lane-bw-781-system-map` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #781 · lane-bw-781-system-map]`.
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
generator writes is one `dispatch.py` accepts. A lane already holding `worktree-lane-bw-781-system-map`
is refused earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-bw-781-system-map` -> branch `worktree-lane-bw-781-system-map` -> contract `LANE-bw-781-system-map.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Context

**Batch:** BW (B2-W4 finish), wave C · **Manifest:** `docs/audits/2026-10-12-technical-batch-bw-manifest.md` (its §4 lane rules bind this lane) · **Order:** `to-cc/BATCH-B2-W4-CC-FINISH-2026-10-12.md` F3 + `to-cc/BATCH-B2-W4-COPILOT-2026-10-11.md` Wave C (Done-when verbatim below) · **Ratified by:** R96 (`to-browser/RATIFICATION-2026-10-11.md`; package `to-browser/DIGEST-RATIFICATION-PACKAGE-2026-10-11.md` P1/P2) · **Frozen on:** F1's integration commit (this file rides `land --slug b2-w4-f1`). · **Row:** `[#781]` nearest.

**Order Done-when (verbatim):** C6 `system-map`: `uv add grimp` (D15); a map JSON is built from `file_purpose_graph` and `grimp`; the HTML is regenerated with no LLM; a `/map` command; a map sha and diff are recorded.

## Why

Proposal §9 C (adopted by R96 D4; D15 allows `grimp` for this lane only, and the lock change rides this lane). C4-style views: process (ADR -> backlog -> task -> distiller -> lane -> checkers -> land -> rollup -> handoff) and module (system -> stage -> script -> file leaf: purpose, consumers, imports, tests, last commit, used yes/no). Inputs: `scripts/file_purpose_graph.py`, `grimp.build_graph()`, `ecosystem/harness.yaml`, `ecosystem/provider-registry.yaml`, the `.claude/commands|skills|agents` listings. Row `[#781]`: one management map rendered from the organ index, trigger-less organs rendered DEAD — reuse `scripts/generate_organ_index.py` and `ecosystem/organ-index.md`, not a parallel census.

## Done-contract (immutable)

1. `uv add grimp` with an exact pin (ADR-106); the `uv.lock` change is in this lane's diff and nowhere else. No other new dependency.
2. A generator builds ONE map JSON from the inputs above (deterministic: same tree, byte-identical JSON) and renders ONE static HTML page (inline JS for expand/collapse, no CDN, no LLM). Tests: determinism; a file `file_purpose_graph` cannot explain is rendered as such; a trigger-less organ is rendered DEAD.
3. A `/map` command under `.claude/commands/` regenerates JSON and HTML and prints the path and the map sha (sha256 of the JSON); the previous sha and a diff summary (added/removed nodes) are recorded in a committed place the handoff generator (lane D2) can read.
4. Whether the HTML is committed follows the repo's generated-artifact rules (`.gitignore`, hermetization) — state which; the JSON's sha is always recorded.
5. R8 usage test: `copilot -p` runs the generator command and reports the sha.
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
