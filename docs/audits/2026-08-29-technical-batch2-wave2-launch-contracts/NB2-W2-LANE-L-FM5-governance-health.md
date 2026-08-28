# NB2 · WAVE 2 · LANE L — FM-5: the value half, scoped honest — S

**Batch:** night-batch-2, wave 2 · **Repo:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`
**Substrate:** local
**Worktree pairing:** slug `lane-l-5-fm-governance-health` -> branch `worktree-lane-l-5-fm-governance-health`
**Frozen by the Layer-1 architect, 2026-08-28** (`docs/audits/2026-08-28-technical-fm-wave2-frozen-bundle.md` §FM-5).

## Dispatch

```
claude --bg --model opus --effort high --worktree lane-l-5-fm-governance-health --permission-mode bypassPermissions "[dev-knowledge . FM-5 . governance-health command] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\NB2-W2-LANE-L-FM5-governance-health.md"
```

## LANE CONTRACT (verbatim)

> ## FM-5 — the value half, scoped honest — S — parallel with FM-3
> Write-scope: audit.py runner reuse (a `governance-health` command) + close-packet parsing +
> tests. Renders FM-4's numbers on demand + a per-closed-row "what it bought" line sourced from
> close packets; A1: emits into the telemetry store so trends exist. Telemetry intake #50 stays
> its own arc — do NOT absorb it. Ex-ante: the command runs on merged main and its numbers equal
> FM-4's block byte-for-byte for the shared fields.

## THE EX-ANTE IS A BYTE-FOR-BYTE EQUALITY — design for it

*"its numbers equal FM-4's block byte-for-byte for the shared fields."* That is achievable exactly
one way: **both render from the same function**. Do not compute anything yourself. Import FM-4's
emitter (lane K, merging tonight) or the FM-2 derivations underneath it, and render. If lane K has
not merged when you run, write against its path, say the coupling is unproven, and **still ship the
equality test** — RED until K lands is an honest RED, and it is the proof the Ex-ante asks for.

## "WHAT IT BOUGHT" — sourced from close packets, never invented

A per-closed-row line, **sourced from close packets**. Find the close packets on disk
(`docs/audits/*close-packet*.md`, `*end-of-batch-packet*.md` — verify the real shapes rather than
trusting this list), parse what they actually say a row bought, and attach it. A row whose packet
says nothing renders as **"no value evidence"** — a true and useful answer; inventing a benefit is
the failure mode. Report the coverage fraction: how many closed rows in the window carry value
evidence and how many do not.

## A1 — the telemetry store already exists; find it, do not build one

*"emits into the telemetry store so trends exist"*, and the appendix is explicit: **append-only
records, derived views, NO second store.** Locate the existing store (`logs/*.jsonl` is where this
repo puts event streams — `PARITY-EVENTS.jsonl` is a live instance; confirm rather than assume),
record its path in your packet, and append in its shape. `logs/` artifact naming is ruled:
UPPERCASE-KEBAB stem, and the extension is a format claim (`.jsonl` for an event stream,
`.log` for a line-append stream, `.md` for a human digest).

## SCOPE FENCE, STATED BY THE CONTRACT ITSELF

**Telemetry intake #50 stays its own arc — do NOT absorb it.** If the work starts to look like
building a telemetry system, you have crossed the fence. You are adding a *command* that renders
existing numbers and appends its own run to an existing store. Read intake #50 so you can name the
boundary in your packet.

## RUNNER REUSE

`audit.py` already has a subcommand runner (`audit.py health`, `audit.py checks`,
`audit repo <name>`). **Reuse it** — a `governance-health` subcommand in the shape the existing
ones take. Do not add a new entry point, a new CLI framework or a second argument parser. If
registering a subcommand touches an `ALL_CHECKS`-adjacent count pin, note it: those pins live in
six places and move together, and there is an oracle test pinning a line offset in `audit.py`.

---

## BOOT (mechanical — before touching a file)

`dispatch` put you in your own worktree. `/lane-boot` steps 1–2 are done (name validated,
single-flight claimed, worktree provisioned). Run 3–7:

```
Get-Location                                              # confirm the worktree
uv run --locked python scripts/worktree_seed.py --plan .  # prints the seed plan; RUN it
uv sync --locked
```

Without `ecosystem/*/state.yaml` seeded from the primary, `audit-health` reports
`repos registered (none)` -> `health: DEGRADED` and **every commit is blocked**. Every test
invocation is `uv run --locked pytest …`; a bare `pytest` inherits the primary's `VIRTUAL_ENV`
and reports green about the primary's source (STANDING_RULINGS D4).

## BINDING CLAUSES ON EVERY LANE OF THIS BATCH (operator appendix, verbatim)

> **A1** state is first-class — every governed object carries explicit state + dated transitions;
> all health numbers are TIME-SERIES on the existing telemetry-store pattern (append-only
> records, derived views; NO second store). **A5** trust contract — every claim carries a
> witness; the packet reports the ex-ante numbers verbatim. Terra pre-merge on every mutating
> lane, tally-in-body. RED-first everywhere: a gate that never fired is not proven.
> Library-first named per lane. Alias standing: "Gemini" (operator speech) = **agy**; the
> retired Gemini-CLI registry entry stays retired.

**RED-first is not a style note.** Where your deliverable is a check, a gate or a query, the
failing witness comes FIRST and is shown in the packet: the test that FAILS before your change
and passes after, or the seeded violation the new check REFUSES. A green test that never went red
proves the assertion runs, not that it discriminates.

**A1 in practice.** If you emit health numbers, they go into the **existing** telemetry store as
append-only records with derived views. Do not create a second store. Find the store before you
design against it, and name its path in your packet.

## RATCHET

`protocols/` + `templates/` deltas are **0** for every wave-2 lane except where your own contract
says otherwise. Measure with `uv run --locked python scripts/silent_rule_detector.py` before your
first commit and before your last, and report both. The wave-1 dispatch measurement was
**443 / 61 files, detector silent-rule-v5, zero headroom**; wave-1 lane C held the batch's only
authorization and may have moved it — so **measure, do not assume 443**.

## THE FOUR THINGS THIS LANE DOES NOT DO

1. **No JOURNAL.md entry.** The integrator writes one anchor for the whole queue after every lane
   STOPs. The Stop hook will demand one naming your SHAs — **decline it explicitly, with the
   reason** (ADR-85 amendment 2026-08-03 §A5 made that hook advisory in full; the hard leg is
   `block-unanchored-push`, and a lane does not push).
2. **No self-merge and no suggesting one.** Commit-and-STOP; your branch enters a frozen queue.
   A hand-back packet ends at `branch + SHAs + gate state + findings`.
3. **No row closures, no `tasks/` writes** unless your own contract grants them. Findings are
   **REPORTED as candidate filings**, never filed.
4. **No generated-surface regeneration** (`BACKLOG.md`, `docs/audits/README.md`,
   `ecosystem/doc-counts.md`, `ecosystem/organ-index.md`, `.claude/generated/*`) — the integrator
   does it ONCE on the merged result. If a gate forces one to keep your own commit legal, do it in
   its own commit and **name that commit in your packet**.

## TESTS

Targeted only — the files covering your own diff. The full suite runs once, at integration
(~9–13 min). Known REDs that are **not yours**: the anchor-gate probe test has been RED on main
since 2026-08-22, and a lane worktree structurally REDs `test_stale_worktrees`. Prove a RED is
inherited (`git merge-base --is-ancestor`) rather than asserting it.

## REVIEWER

Terra pre-merge, **tally-in-body**: run `codex exec` over your own diff (NOT `/codex-review` — a
mixed doc/code diff kills that lane) and put the tally in your packet. An unreachable reviewer is
one recorded line with the error, not a lane failure.

## YOUR PACKET

`docs/audits/2026-08-29-technical-nb2-<lane-letter>-packet.md` — never the repo root. In order:
(1) per-done-item **MET / NOT-MET / PARTIAL** with a witness each; (2) commit SHAs in order;
(3) terra tally; (4) candidate filings; (5) budget decisions; (6) deviations with owners.
**Report your contract's own Ex-ante line verbatim, then the measured result against it.**

Then **STOP**.
