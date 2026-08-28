# NB2 · WAVE 2 · LANE M — FPG-1: the file-purpose graph, first slice (A3) — M

**Batch:** night-batch-2, wave 2 · **Repo:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`
**Substrate:** local
**Worktree pairing:** slug `lane-m-1-fpg-file-purpose-graph` -> branch `worktree-lane-m-1-fpg-file-purpose-graph`
**Frozen by the Layer-1 architect, 2026-08-28** (`docs/audits/2026-08-28-technical-fm-wave2-frozen-bundle.md` §FPG-1).

## Dispatch

```
claude --bg --model opus --effort high --worktree lane-m-1-fpg-file-purpose-graph --permission-mode bypassPermissions "[dev-knowledge . FPG-1 . file purpose graph] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\NB2-W2-LANE-M-FPG1-file-purpose-graph.md"
```

## LANE CONTRACT (verbatim)

> ## FPG-1 — the file-purpose graph, first slice (A3) — M
> Write-scope: new query module + tests; reads doc-code-edge.yaml, the audits index, [#595]
> citations, tasks/ depends-on, the deploy manifest — unified into ONE queryable graph. This IS
> the named consumer ruling R-A reserved: **rustworkx** (per R-A: "if a consumer is ever named,
> the library is rustworkx, not networkx"). **DEPENDENCY DISCIPLINE (self-review fix): adding
> rustworkx is a dependency change and is never incidental (ADR-106) — its authorization is the
> operator's A3 mandate verbatim ("a real graph library, not more hand-rolled traversal"); declare
> it through the ruled dependency path, cite the mandate in the commit.** FIRST ACT: verify the two
> facts R-A left open. Half one is now externally witnessed: rustworkx publishes prebuilt PyPI
> wheels for 32/64-bit Windows and its CI covers Python 3.10–3.14 incl. Windows (rustworkx.org
> install docs + project CI matrix, checked 2026-08-28 by the architect) — re-confirm locally.
> Half two stays MEASUREMENT-OWED-LOCAL: installability under the pinned uv 0.11.19. On failure,
> fall back to R-A's measured sqlite/stdlib edges with a swap-ready seam, and record the measured
> divergence (library-first discipline both directions). Deliverable: `why <path>` answering
> purpose + consumers + edges for governed surfaces, FAILING on unknown files (a file nothing
> explains is a defect, not a mystery). Phase: new-files-first; FM-2 gains the predicate in a
> later batch, not tonight.
> Ex-ante: `why` answers correctly on 3 named governed files (witnessed transcripts) and FAILs
> on a planted unknown.

## THE DEPENDENCY ACT — do it the ruled way or not at all

ADR-106: the environment is **declared** by `pyproject.toml` + `uv.lock` + `.python-version`, and
`uv` itself is pinned exactly (`==0.11.19`). A dependency change is therefore:
`pyproject.toml` -> `uv lock` -> `uv sync --locked`, committed together, **with the operator's A3
mandate quoted in the commit body** as the authorization. Never `uv add` into a drifted lock,
never a bare `pip install`, and **never bump `uv` itself** — a uv bump is its own gated change.

**The measured half is yours to measure.** Run the install under the pinned uv in your own
worktree and report the result either way. If it fails, take R-A's fallback — sqlite/stdlib edges
behind a **swap-ready seam** — and record the measured divergence. Library-first discipline runs
in both directions: you may not hand-roll because the library is inconvenient, and you may not
adopt because it is fashionable. The evidence decides, and the evidence goes in the packet.

## THE FIVE INPUTS — resolve every one before you build the graph

`ecosystem/doc-code-edge.yaml` · the generated `docs/audits/README.md` index · the `[#595]`
consumer-at-landing citations · `tasks/**` `depends-on` edges (the SOURCE OF TRUTH is `tasks/`,
**not** `BACKLOG.md`, a generated one-line view) · `deploy/manifest-v*.yaml`. Open each, record its
real path and shape in the packet, and say what edge type it contributes. **A known trap in the
`tasks/` half:** `_parse_deps` reads only the FIRST clause (`search()`, not `finditer()`), so
multi-target dependency edges are expressed in ONE comma-separated clause — if you read deps with
that helper you inherit its limit, and if you write your own you may see edges the rest of the
repo does not. Say which you did.

## `why <path>` — the deliverable, and its refusal is half the value

Three answers per governed path: **purpose** (what this file is for), **consumers** (what reads
it), **edges** (what it reads / is coupled to). And on an unknown file it **FAILs** — *a file
nothing explains is a defect, not a mystery.* Build the refusal first and test it with a planted
unknown; that is the RED-first witness for this lane.

Ex-ante is literal: **3 named governed files, witnessed transcripts** — paste the actual command
output into the packet, not a description of it. Pick three of genuinely different kinds (a
generated surface, a hand-authored canonical doc, a script) so the answer shape is proven, not the
happy path.

## PHASE FENCE

**New-files-first.** You are not making `check_funnel_lifecycle` consume the predicate — that is a
later batch, and the contract says so. Do not wire `why` into any gate tonight; ship the module
and the CLI, and report the wiring as a candidate filing.

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
