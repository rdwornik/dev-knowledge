# NB2 · WAVE 2 · LANE J — FM-3: the visible shrinkage (execution) — M

**Batch:** night-batch-2, wave 2 · **Repo:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`
**Substrate:** local
**Worktree pairing:** slug `lane-j-3-fm-visible-shrinkage` -> branch `worktree-lane-j-3-fm-visible-shrinkage`
**Frozen by the Layer-1 architect, 2026-08-28** (`docs/audits/2026-08-28-technical-fm-wave2-frozen-bundle.md` §FM-3).
**Runs AFTER FM-2 merges — you execute under the new gate, not beside it.**

## Dispatch

```
claude --bg --model opus --effort high --worktree lane-j-3-fm-visible-shrinkage --permission-mode bypassPermissions "[dev-knowledge . FM-3 . visible shrinkage] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\NB2-W2-LANE-J-FM3-shrinkage.md"
```

## LANE CONTRACT (verbatim)

> ## FM-3 — the visible shrinkage (execution) — M — runs AFTER FM-2 merges
> Write-scope: docs/intake/, docs/decisions/, the ruled archive destinations, tasks/ row-body
> pointers via N4's landed mechanism. **STALENESS GUARD (self-review fix): FM-C's census is a
> snapshot of the origin clone at dispatch time, and wave-1 merges land AFTER it. Before relocating
> ANY item, re-verify its classification against the LIVE merged tree (consumers still terminal, no
> new consumer born tonight); an item failing re-verification is SKIPPED and reported, never
> relocated on the census's word alone.** Then execute the worklist under the NEW gate: archive
> every re-verified consumed intake and superseded ADR per FM-1's rules — byte-identical relocation
> on the ADR-29 precedent, md5 per object, ZERO deletion, ZERO content edits. Ex-ante: docs/intake
> and docs/decisions counts DROP — exact before/after in the packet; check_funnel_lifecycle GREEN
> on main afterwards; every relocation md5-proven; skipped items listed with reasons.

## THE STALENESS GUARD IS THE FIRST THING YOU BUILD, NOT A DISCLAIMER

FM-C censused a clone of `origin/main` taken at **2026-08-29 ~00:2x**, before any wave-1 lane
merged. Between then and you: seven lanes landed, one of which (lane D / N4) rewrote `tasks/` row
bodies wholesale. **Every classification in that census is a hypothesis about a tree that no
longer exists.**

So: write the re-verification as a **function**, run it over every candidate, and let it gate the
relocation. Per item it re-asks, on the live merged tree: are all consumers still terminal? has a
new consumer appeared tonight? does the object still exist at the path the census names? **An item
that fails any leg is SKIPPED and listed with the reason.** A skipped item is a success of this
guard, not a failure of the lane — the packet says so.

## MEASURED BEFORE-NUMBERS (dispatch-time, on the operator's disk — your own re-count wins)

`docs/intake/*.md` = **56** · `docs/decisions/*.md` (top level) = **89**. Re-count on the live
merged tree as your first act and report both pairs. The Ex-ante the morning packet reports
against is: **both counts DROP, exact before/after named.**

## RELOCATION DISCIPLINE — byte-identity is provable or it did not happen

- **The precedent is ADR-29's chronological-archival exception**: a contiguous older block MAY
  relocate **byte-identical**. Read it before you design the move.
- **md5 per object, before and after, recorded in the archive record itself.** `Path.write_text`
  launders LF->CRLF on Windows and a `read_text` round-trip cannot detect it — use
  `read_bytes`/`write_bytes` for anything you claim is byte-identical.
- **ZERO deletion. ZERO content edits.** Not one character, not a heading, not a status line.
- Use `git mv` where the destination is a path move, so history follows.
- **Row-body pointers go through lane D's landed mechanism** (`tasks/archive/`, merged in wave 1).
  Read that mechanism and use it; do not build a second one. Scripted `tasks/` edits write **LF**.
- `docs/decisions/` and `docs/intake/` both have **generated indices** with freshness gates
  (`gen_intake_index.py --check` is a pre-commit hook; `docs/decisions/README.md` and
  `.claude/generated/recent-adrs.md` have their own). Moving files will fire them. Regenerate what
  your own commit needs to be legal, in its own commit, and name it in the packet — the
  integrator's single regeneration pass covers the rest.
- **An ADR's status line is the ONE in-place-editable thing about an ADR (ADR-94), and you are not
  editing it.** Archiving is a move, not a status change. If an object needs a status change to be
  archivable, it is not archivable yet — SKIP and report.

## THE ORDER

1. Re-count, live. 2. Build and run the re-verification. 3. Relocate the survivors, md5-proven.
4. Re-run `check_funnel_lifecycle` (FM-2's, merged before you) and show it **GREEN on main
afterwards** — that is an Ex-ante item, and if it is not green, say exactly which class still
FAILs. 5. Re-count, live. 6. Packet.

## WHAT THIS LANE DOES NOT DO

No deletions of any kind. No `codex/AGENTS.md` (root `AGENTS.md`'s precedence section documents it
by name — FM-C classifies it PROTECTED). No root `README.md` recreation as a side effect (deleted
2026-05-23; ADR-114 is PARKED, not decided). No `protocols/` writes. No new check code.

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

## LATE ADDENDUM — FM-C's answer, added at wave-2 dispatch. READ IT BEFORE YOU PLAN.

**The census came back and its headline is: the archival step is not what is broken.**
Measured on the clone at `fcc9485`, 951 objects, 100 % classified, UNCLASSIFIED = 0:

```
directory                              total  PROTECTED  CONSUMED-BY  CONS-&-ARCHIVABLE  ORPHAN
docs/audits/ (top level)                 773        773            0                  0       0
docs/audits/<launch-contract subdirs>     20         20            0                  0       0
docs/decisions/ (88 ADRs + README)        89         89            0                  0       0
docs/decisions/archive/                    2          2            0                  0       0
docs/intake/ (55 live + README + json)    57          2           44                  0      11
docs/intake/archive/                       8          8            0                  0       0
TOTAL                                    951        895           45                  0      11
```

**CONSUMED-AND-ARCHIVABLE = 0, corpus-wide.** Three retention authorities do it:
**ADR-100 §1** — *"Every accepted audit is kept, unbounded; audit files are never physically moved,
rolled up, or compacted"* — protects all 793 audit objects. **CLAUDE.md §5 rule 3** (ADR
immutability) protects all 88 ADRs. And the intake archival predicate,
`docs/intake/README.md:228-231` — *"Terminal docs (CONSUMED | SUPERSEDED | REJECTED) relocate
byte-identical to `docs/intake/archive/`"* — has **zero backlog**: live statuses are
ACCEPTED 19 · READY 19 · SEED 10 · DRAFT 7, **no terminal doc sits at depth 1**, and all 8 files
already in `archive/` are terminal. Zero mis-filings in either direction.

**So the honest consequence, stated plainly: this lane's Ex-ante — "docs/intake and
docs/decisions counts DROP" — is NOT MECHANICALLY ACHIEVABLE tonight, and you must not
manufacture a relocation to satisfy it.** The three intake candidates FM-C found
(**#19** SEED, consumed by ADR-82, only row [#446] CLOSED — the strongest; **#26** and **#28**,
both ACCEPTED, consumed by ADR-110 / ADR-112) each need a **status flip to a terminal value**, and
`README.md:228-231` says ACCEPTED is *deliberately* not terminal because *"a standing decision
stays live"*. **A status flip is an operator/architect act. It is not yours and it is not
mechanical.** FM-C also *rejected* a fourth candidate (**#42**, DRAFT) after opening the file:
ADR-115 answered some of its questions, not the document.

### WHAT THIS LANE THEREFORE DOES

1. **Re-verify FM-C's zero on the LIVE MERGED tree** — the staleness guard above, run over the
   whole predicate rather than over a worklist. Wave-1 lanes landed after the census; recompute
   the per-directory × class table and the four status counts yourself, and report **your** numbers
   beside FM-C's. If a terminal doc HAS appeared at depth 1, relocate it byte-identically,
   md5-proven — that is the worklist, however short.
2. **Execute the other shrinkage axis, which IS mechanical and IS yours:** `tasks/` row-body
   pointers through the mechanism wave-1 lane D landed at `tasks/archive/`. Lane D's exclusive
   `tasks/` ownership ended when it STOPped; your contract's write-scope names row-body pointers
   explicitly. Report `validate_doc_rot` before and after — the dispatch-time figure was **77**
   loci and lane D moved it; measure, do not assume.
3. **Produce the RULING REQUEST as a deliverable**, in the packet, in the operator's own terms:
   the three intake docs, what each is consumed by, which row closed it, what flipping its status
   would cost, and the one line the operator would have to say. That is what "decision-ready"
   means here.
4. **Re-run `check_funnel_lifecycle`** (lane I's, merged before you) and report its verdict. If it
   is GREEN because there is genuinely nothing to reap, say that — a gate that is green on an
   empty set is only worth something when the emptiness has been proven, and §1 is that proof.

**Report the Ex-ante verbatim and then the measured result against it.** "NOT MET, and here is the
retention authority that makes it unmeetable without a ruling" is a correct outcome. A relocation
that violates ADR-100 or ADR-94 to make a number move is not.

---

## NOTE ON ONE CITED ID — `[#446]` is CLOSED, and that is the point being made

The freeze predicates flag `[#446]` in the addendum above as *"resolves to a CLOSED row … a
contract cannot dispatch work against it"*. Correct on the form, and the citation is deliberate:
`[#446]` is named as **evidence that intake #19's only born row has reached a terminal state**,
which is precisely what makes #19 the strongest archival candidate. **No work is dispatched
against it.** Do not open it, do not reopen it, do not close anything.

Reported as a candidate filing against `[#591]`: predicate (iii) cannot distinguish an id cited as
a **dispatch target** from an id cited as **terminal-state evidence**, and an archival contract is
made almost entirely of the second kind.
