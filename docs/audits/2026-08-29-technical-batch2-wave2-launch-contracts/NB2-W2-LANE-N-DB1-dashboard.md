# NB2 · WAVE 2 · LANE N — DB-1: the dashboard successor (A2) — M

**Batch:** night-batch-2, wave 2 · **Repo:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`
**Substrate:** local
**Worktree pairing:** slug `lane-n-1-db-dashboard-successor` -> branch `worktree-lane-n-1-db-dashboard-successor`
**Frozen by the Layer-1 architect, 2026-08-28** (`docs/audits/2026-08-28-technical-fm-wave2-frozen-bundle.md` §DB-1).
**Runs after FM-4 (lane K).**

## Dispatch

```
claude --bg --model opus --effort high --worktree lane-n-1-db-dashboard-successor --permission-mode bypassPermissions "[dev-knowledge . DB-1 . dashboard successor] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\NB2-W2-LANE-N-DB1-dashboard.md"
```

## LANE CONTRACT (verbatim)

> ## DB-1 — the dashboard successor (A2) — M — after FM-4
> Write-scope: new render module + tests; INPUT = telemetry/history data only. The conformance
> HTML dashboard is censused by FM-C like any artifact (zero consumers -> orphan -> FM-3 archives
> it). Replacement: ONE analyst-grade surface rendering TRENDS — open rows, banked ledger,
> commit-gate wall-time, doc-rot findings, funnel orphans, paste bytes, suite time — as charts
> over window history, regenerated, never hand-written. Library-first: pick an established
> charting library by measured fit; record divergence if anything is hand-rolled. Ex-ante
> (operator's acceptance verbatim): DIRECTION visible in one glance; zero colored-table markdown;
> regenerable from the store with one command.

## INPUT IS THE STORE. FULL STOP.

*"INPUT = telemetry/history data only."* You render what the repo already records. You do not
compute a metric, scrape a doc, or hand-enter a number. **First act: enumerate the actual history
sources on disk and record their paths** — `logs/*.jsonl` event streams, `ecosystem/*/history/`
baselines, `logs/TOKEN-LOG.md`, whatever else exists. For each of the seven series the contract
names (open rows · banked ledger · commit-gate wall-time · doc-rot findings · funnel orphans ·
paste bytes · suite time), say **which store carries it and how far back**. A series with no store
is rendered as **absent**, named in the legend, not silently dropped and not back-filled by hand.
That enumeration is a done-item on its own; a chart of invented history is worse than no chart.

## THE OPERATOR'S ACCEPTANCE IS THE SPEC — three literal tests

1. **DIRECTION visible in one glance.** Not values — *direction*. Every series shows whether it is
   getting better or worse over the window. Design for that first and let everything else follow.
2. **Zero colored-table markdown.** The thing being replaced is a table pretending to be a
   dashboard. If your output contains a colour-coded markdown table, you have rebuilt it.
3. **Regenerable from the store with ONE command.** Write that command down; it is the deliverable
   as much as the module is. Nothing hand-written, ever, and a regeneration must be idempotent.

## LIBRARY-FIRST, MEASURED — and mind the dependency rule

Pick an established charting library **by measured fit**, and if you hand-roll anything, record the
divergence and why. But the dependency is a **gated act** (ADR-106): `pyproject.toml` -> `uv lock`
-> `uv sync --locked`, committed together, authorization cited. Note the cheap answer that may
well win on measured fit and costs no dependency at all: **this repo renders mermaid natively in
its visualization surface, and inline SVG needs no library.** If a stdlib/SVG render meets all
three acceptance tests, that IS the library-first answer — say so with the measurement, do not add
a dependency to look thorough. Whatever you choose, name the alternatives you rejected.

## THE PREDECESSOR — do not delete it, and do not preserve it either

The conformance HTML dashboard is **FM-C's to classify and FM-3's to archive**. You neither delete
it nor keep it alive. What you owe it is a **consumer statement**: if anything reads it, your
successor must serve that reader or the archival is not safe. Check, and say what you found.

## HAZARDS

- `gen_dashboard`-class generators in this repo need `PYTHONUTF8=1` or they emit **silent
  mojibake and exit 0**. If you write a generator that emits non-ASCII, set it and **verify the
  output bytes after regenerating** rather than trusting exit 0.
- The console here is cp1252: the bar is cp1252-encodable, not ASCII-only.
- Your output file's home must survive `validate_hermetization` Rule C. `ecosystem/` and
  `docs/audits/` are existing homes; a new top-level anything is refused.
- If your renderer's output is a **generated** file, it needs a freshness/regen story before it can
  be committed — say which gate you added or why none is owed tonight.

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

---

## OPERATOR ADDENDUM — 2026-08-29: the telemetry scope extension. Two more series, and a fence.

Ruled after this contract was frozen and carried here rather than left to the packet.

**FIRST ACT, before you design anything: LOCATE the operator's telemetry artifact.** It is
**intake #50** plus the **L5 cost-research** artifact. Open both, record their real paths and what
each actually holds, and say in your packet what the store's shape is. The contract above tells you
to enumerate history sources; #50 and the L5 research are named inputs to that enumeration, not
optional reading. **If either does not resolve, say `MEASUREMENT-OWED` and name what you searched**
— do not substitute a store you found instead.

**Two series are added to the seven this contract already names:**

- **Backlog-consumption velocity** — rows closed per window, against rows born per window. The
  banked-ledger series is already in your list; this is its rate, and the operator's standing
  frame is *"closures fund births"*, so the pair is the whole point. Derive it from `tasks/`
  terminal-status transitions, **not** from `BACKLOG.md` (a generated one-line VIEW).
- **Per-model change quality trends** — quality of change, over time, **by authoring model**. Note
  honestly that this series is **not derivable today**: nothing in the tree records which model
  authored a commit. Render it as **absent, in the legend, with the reason** — exactly as this
  contract already requires for any series with no store. Do not proxy it with something else.

**The enabling row is a candidate filing, not your work: MODEL ATTRIBUTION** — every model-authored
commit carries a **model + version signature trailer**, hook-enforced, and the telemetry store
consumes it. That is what would make the second series real. **Report it as a candidate; do not
build it, do not add a hook.**

**The fence is unchanged and now doubly binding:** *telemetry intake #50 stays its own arc — do NOT
absorb it.* You are reading #50 to find the store, not to implement it. If your diff starts adding
collection, you have crossed the fence.
