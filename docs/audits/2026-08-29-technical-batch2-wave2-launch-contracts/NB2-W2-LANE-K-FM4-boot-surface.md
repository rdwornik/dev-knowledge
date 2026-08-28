# NB2 · WAVE 2 · LANE K — FM-4: the boot surface — S/M

**Batch:** night-batch-2, wave 2 · **Repo:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`
**Substrate:** local
**Worktree pairing:** slug `lane-k-4-fm-boot-surface` -> branch `worktree-lane-k-4-fm-boot-surface`
**Frozen by the Layer-1 architect, 2026-08-28** (`docs/audits/2026-08-28-technical-fm-wave2-frozen-bundle.md` §FM-4).

## Dispatch

```
claude --bg --model opus --effort high --worktree lane-k-4-fm-boot-surface --permission-mode bypassPermissions "[dev-knowledge . FM-4 . funnel health block] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\NB2-W2-LANE-K-FM4-boot-surface.md"
```

## LANE CONTRACT (verbatim)

> ## FM-4 — the boot surface — S/M — parallel with FM-3
> Write-scope: the handoff assembler module + tests (FIRST ACT: locate it and witness the path —
> do not assume a filename; the N8 validator will check this contract). gen_handoff emits a
> generated FUNNEL HEALTH block in every bundle: intakes consumed-unarchived / ADRs unexecuted /
> orphans both directions / rows closed this window + value evidence attached — numbers only, no
> verdicts, no shas (anti-bluff intact), sourced from the same derivations FM-2 uses (one truth).
> Ex-ante: the next assembled bundle carries the block; a golden test pins its shape.

## FIRST ACT — WITNESS THE PATH

The contract deliberately does not name the assembler's file. **Locate it and record the
`file:line` in your packet before you write anything.** `scripts/gen_handoff.py` is the obvious
candidate and it is probably right — but "probably right" is exactly the premise class that put
three defects into the batch-1 contracts and four into tonight's. Open it, confirm it is the
module that assembles a bundle, and say so with evidence. **Wave-1 lane G shipped a validator
whose predicate (i) checks precisely this kind of claim; your packet is a test case for it.**

## ONE TRUTH — the block is DERIVED, not recomputed

The numbers come from **the same derivations `check_funnel_lifecycle` uses** (FM-2, lane I, merged
or merging tonight). Import them; do not re-implement them. If FM-2 has not merged when you run,
**write against its module path and say the coupling is unproven until it lands** — a second
implementation of "is this intake consumed?" is the exact failure this batch exists to remove.

## ANTI-BLUFF — the block's shape is a constraint, not a preference

**Numbers only. No verdicts. No SHAs.** A bundle that says *"funnel healthy"* has made a claim the
reader cannot check; a bundle that says *"intakes consumed-unarchived: 7"* has handed them one
they can. The five fields, from the contract: intakes consumed-unarchived · ADRs unexecuted ·
orphans, **both directions** · rows closed this window · value evidence attached. "Both
directions" means forward (object -> consumer) **and** backward (open row -> resolving `source:`).

## THE GOLDEN TEST

A golden test pins the block's **shape**, not tonight's numbers — a test asserting `7` breaks the
first time the funnel changes, which is every day. Pin: the field names, their order, the
numbers-only format, and the block's delimiters. Assert the block is present in an assembled
bundle. Then assert it is **regenerated**, not carried: a stale block is worse than none.

## THE HAZARDS IN THIS MODULE, KNOWN

- `gen_handoff` **refuses to cut a bundle while any worktree is live**, and there is no override
  flag. Six or more lane worktrees exist tonight. So **you cannot cut a real bundle to test
  against** — build the test around the assembler's block-emitting function directly, and record
  that end-to-end assembly is `MEASUREMENT-OWED` until the worktrees are gone. Say so; do not
  work around the refusal.
- `gen_handoff`'s own test stub **shadows `audit`**, making `ALL_CHECKS` read `[]`. Use
  `CHECK_ORDER` if you need the roster.
- Bundles are **immutable artifacts** (`docs/handoffs/`) and `check-seal-identity` gates them at
  commit time. Do not commit a test bundle into `docs/handoffs/`; use `tmp_path`.
- `docs/handoffs/README.md` is freshness-gated — do not touch it without a real review.

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
