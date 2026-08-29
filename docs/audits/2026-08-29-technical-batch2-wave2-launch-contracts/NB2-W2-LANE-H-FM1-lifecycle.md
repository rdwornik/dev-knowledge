# NB2 · WAVE 2 · LANE H — FM-1: the lifecycle written ONCE (doctrine) — M

**Batch:** night-batch-2, wave 2 · **Repo:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`
**Substrate:** local
**Worktree pairing:** slug `lane-h-1-fm-lifecycle-doctrine` -> branch `worktree-lane-h-1-fm-lifecycle-doctrine`
**Frozen by the Layer-1 architect, 2026-08-28** (`docs/audits/2026-08-28-technical-fm-wave2-frozen-bundle.md` §FM-1).

## Dispatch

```
claude --bg --model opus --effort high --worktree lane-h-1-fm-lifecycle-doctrine --permission-mode bypassPermissions "[dev-knowledge . FM-1 . funnel lifecycle doctrine] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\NB2-W2-LANE-H-FM1-lifecycle.md"
```

## LANE CONTRACT (verbatim)

> ## FM-1 — the lifecycle written ONCE (doctrine) — M
> Write-scope: PLAYBOOK section if post-N3 ratchet headroom allows; else the ONE justified new
> protocols/ file, operator-authorized by the mandate (measure headroom FIRST — witness the count).
> Collision note: starts only after N3 merges (wave-1 step 4). Content: the state machine —
> states, allowed transitions, terminal conditions, who archives what and when, the session's two
> standing jobs — citing ADR-98/111/100/70 as the sources unified, superseding nothing silently;
> the N-days READY threshold ruled here (FM-2 reads it). A1: this machine is the TEMPLATE for all
> governed objects, stated as such. Ex-ante: two seats could run one funnel pass from this text
> alone and produce identical transitions.

## MEASURE HEADROOM FIRST — this is done-item zero and it is a REFUSAL POINT

```
uv run --locked python scripts/silent_rule_detector.py
```

Wave-1 dispatch measured **443 / 61 files**, live == baseline, **zero headroom**. Wave-1 lane C
held the batch's only ratchet authorization and may have moved it — **read the live number, do
not assume 443.** Then decide, and say which you took and why:

- **Headroom exists** -> a named section in `protocols/PLAYBOOK.md`. Regenerate the TOC in your own
  lane (`toc-freshness-playbook` gates your own commit).
- **No headroom** -> the ONE justified new `protocols/` file, which the operator's mandate
  authorizes. A new `protocols/*.md` is itself in ratchet scope, so a token-free authoring is the
  outcome that costs nothing — batch-1's lane L1 landed a whole §10 correction that way and spent
  **zero** of an identical grant. Also check `validate_hermetization` before committing: a new
  top-level file class is refused, and `protocols/` is an existing home, so this should pass —
  verify rather than assume.

## THE STATE MACHINE — the operator's own words, made mechanical

`audit -> intake | ADR` · `intake -> reject/archive | ADR` · `ADR -> backlog rows` ·
`rows -> executed` · **consumed sources -> ARCHIVED at terminal state.** And the session's **two
standing jobs**: *funnel coherence* (everything consumed, numbered, archived at terminal state)
and *value audit* (what shipped, what it bought, measured).

Write it as a machine, not an essay: **states** (each with the frontmatter/status token that
carries it in the tree), **allowed transitions** (each with who may perform it and what evidence
it requires), **terminal conditions**, **who archives what and when**. The test in the Ex-ante is
literal — *two seats could run one funnel pass from this text alone and produce identical
transitions* — so every judgement call the text leaves open is a defect in it.

**The N-days READY threshold is RULED HERE**, as a number, because FM-2 reads it and a check
cannot read a maybe. Pick it, justify it in one line, and state that FM-2 binds to it.

## THE FOUR SOURCES YOU UNIFY — resolve each before citing it

`docs/decisions/ADR-98-*.md` (the requirements spine / intake), `ADR-111-*.md` (the four-outcome
finding funnel), `ADR-100-*.md` and `ADR-70-*.md` (Tier-1 closure). **Supersede nothing silently:**
where your text restates one of them, say so and cite; where it goes further, say that too. If you
find a genuine conflict between two of them, that is a **rule-vs-ruling fork** — report it as a
candidate filing and write the text to the reading you can defend, naming the fork.

## A1 — say it out loud

The contract's own words: *this machine is the TEMPLATE for all governed objects, stated as such.*
So the section says, in its own text, that the state+dated-transition shape generalizes beyond the
funnel. That sentence is a done-item, not decoration.

## WHAT THIS LANE DOES NOT DO

No check code (FM-2's), no relocation (FM-3's), no `tasks/` writes, and **no edit to Ch8's
dispatch table**. `protocols/HANDOFF_PROCESS.md` belongs to no wave-2 lane.

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
