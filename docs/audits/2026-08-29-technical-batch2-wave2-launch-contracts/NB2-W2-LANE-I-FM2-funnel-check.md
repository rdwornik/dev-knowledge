# NB2 · WAVE 2 · LANE I — FM-2: check_funnel_lifecycle, the reaper's teeth — M

**Batch:** night-batch-2, wave 2 · **Repo:** `C:\Users\1028120\Documents\Dev\.dev-knowledge`
**Substrate:** local
**Worktree pairing:** slug `lane-i-2-fm-funnel-lifecycle-check` -> branch `worktree-lane-i-2-fm-funnel-lifecycle-check`
**Frozen by the Layer-1 architect, 2026-08-28** (`docs/audits/2026-08-28-technical-fm-wave2-frozen-bundle.md` §FM-2).

## Dispatch

```
claude --bg --model opus --effort high --worktree lane-i-2-fm-funnel-lifecycle-check --permission-mode bypassPermissions "[dev-knowledge . FM-2 . funnel lifecycle check] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\NB2-W2-LANE-I-FM2-funnel-check.md"
```

## LANE CONTRACT (verbatim)

> ## FM-2 — check_funnel_lifecycle, the reaper's teeth — M
> Write-scope: new check module + registration (audit.py) + tests. Collision note: after N6
> merges. Extends existing organs (funnel_coverage, intake_tree_coherence, [#595]) — never a
> rival. FAIL-class: (a) intake ACCEPTED, all rows terminal, not archived -> FAIL; (b) ADR
> superseded/rejected, not archived -> FAIL; (c) post-cutoff row whose source does not resolve ->
> FAIL; (d) intake READY beyond FM-1's N days, no ruling -> WARN. Z-G4 holds: cannot-compute ->
> FAIL, never skip. Ex-ante: RED-first against live main reproducing FM-C's findings (that is the
> proof of teeth), plus a seeded-violation test that FAILs then passes.

## READ FM-1's N-DAYS THRESHOLD FROM THE TREE, NEVER FROM MEMORY

FM-1 (lane H) rules the READY threshold as a number and lands it in `protocols/`. It merges before
you. **Find it, quote it, and cite the file:line in your packet.** If it is absent — lane H
stopped, or landed a different shape — leg (d) is **NOT-MET with the reason**, and the other three
legs still ship. Do not invent a threshold; a check whose constant nobody ruled is the drift this
whole batch exists to stop.

## REGISTRATION — the expensive half, and it is not the code

`audit.py`'s registry is coupled at more sites than the module. Before you register:

- **`ALL_CHECKS` count pins live in SIX places.** Find them all (`grep` the number, then grep for
  `len(ALL_CHECKS)` and the oracle test) and move them together. There is a test that pins the
  count and a test that pins a line offset in `audit.py`; both move with you.
- `gen_handoff`'s test stub **shadows** `audit`, making `ALL_CHECKS` read `[]` — use `CHECK_ORDER`
  when a test needs the roster.
- `audit-health` is a **pre-commit hook**. Your new check runs on every commit in every lane from
  the moment you register it, including your own next commit. If it FAILs on live main — and
  **the Ex-ante says it must** — you have just wedged your own lane. Plan for that: land the check
  **not registered** (or registered at a tier the commit gate does not run) in one commit, prove
  the RED with a direct invocation, and register at the gate in a second commit only if the tree
  is clean by then. **State which you did.** `[#597]` per-check tiering is the existing mechanism
  for "not run at the commit gate" — read how `routing_agreement` declares its ship-tier and reuse
  that seam rather than inventing one.

## RED-FIRST, TWICE — and the two REDs mean different things

1. **Against live main, reproducing FM-C's findings.** That is the proof of teeth: the census
   found real unarchived consumed intakes and superseded ADRs, and your check must see the same
   ones. Show the overlap explicitly — *"FM-C listed N objects in class X; the check FAILs on M of
   them; the N−M difference is <reason>"*. Two instruments, one reality.
2. **A seeded-violation test that FAILs then passes.** Synthetic, hermetic, in `tmp_path`.

FM-C's census artifact will be in `docs/audits/` by the time you run. Find it; it is the input.

## Z-G4 IS NOT OPTIONAL

`protocols/STANDING_RULINGS.md` **Z-G4: a check that cannot compute its ground truth FAILS — it
does not skip.** An unreadable intake, an unparseable frontmatter, a `source:` you cannot resolve
because the resolver itself broke: **FAIL**, with the reason in the evidence string. Exit codes
follow the sibling gates: 0 clean, 1 violation, 2 internal error, and an internal error BLOCKS.

## EXTEND, NEVER RIVAL

`funnel_coverage`, `intake_tree_coherence` and the `[#595]` consumer-at-landing check already read
much of this ground. Open all three first and say, in the packet, **what each already does and
what your check adds**. Reuse their resolvers rather than writing a second one — two answers to
"is this intake consumed?" is the failure mode, not the fix. Row ids and statuses come from
`tasks/`, the source of truth; `BACKLOG.md` is a generated one-line VIEW and reading it returns an
empty set.

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

## LATE ADDENDUM — a contract-premise defect FM-C found, added at wave-2 dispatch, not repaired

**FM-2's FAIL-leg (c) is written against a field that does not exist.** The contract says
*"post-cutoff row whose `source:` does not resolve -> FAIL"*. FM-C's census measured the live
`tasks/` schema and found **zero of 344 rows carry a `source:` field**. The frontmatter schema is
`id · title · status · priority · size · theme · story · generates`.

```
$ grep -l '^source:' tasks/*.md | wc -l          -> 0
$ awk '/^---$/{n++;next} n==1{print $1}' tasks/*.md | sort -u
generates:  id:  priority:  size:  status:  story:  theme:  title:
```

**FM-C's substitute, which it verified is complete:** every row body carries a `· refs …`
provenance clause, and **153 of 153 OPEN rows carry one**. FM-C executed the whole backward
direction against `refs` on that basis.

**Take the same substitute, and say so.** Leg (c) reads `· refs …` — the de-facto `source:` — not
a `source:` frontmatter key. Re-derive the 153/153 figure yourself on the live merged tree before
relying on it (wave-1 lane D rewrote row bodies wholesale, so the clause may have moved). If the
substitute does not hold on the merged tree, leg (c) is **NOT-MET with the measurement**, and the
other three legs still ship.

**Do not "fix" this by adding a `source:` field to 344 rows.** That is a schema change to the
backlog source of truth, it is outside your write-scope, and lane D is the batch's `tasks/` writer.
Report it as a candidate filing: *"either the funnel doctrine names `refs` as the provenance
clause, or `tasks/` grows a `source:` field — one act, ruled once."*

---

## STATE OF THE TREE WHEN YOU BOOT — 2026-08-29, after the wave-2 GO's carried acts

Four things moved on `main` between FM-C's census and your boot. **Re-measure; do not reuse the
census's numbers.**

1. **Two intakes are now terminal.** #19 (SEED → CONSUMED) and #26 (ACCEPTED → CONSUMED) by
   operator status ruling. **#28 is HELD** per ADR-112. So your FAIL-leg (a) — *"intake ACCEPTED,
   all rows terminal, not archived"* — has live subjects for the first time. Lane J relocates them
   in this same wave; depending on merge order you may see them at depth 1 or already in
   `docs/intake/archive/`. **Your check must be right either way**, which is a good thing to prove
   with a test.
2. **The intake index was repaired.** Six live intakes (ids 56–61) had a `consumers:` scalar
   opening with a backtick — illegal as a YAML scalar opener — so `gen_intake_index._parse_frontmatter`
   returned `{}` and those docs lost id and status. Live statuses now read **SEED 10 · DRAFT 7 ·
   READY 19 · ACCEPTED 19**. **If your check parses intake frontmatter, do not reimplement that
   parser** — reuse the generator's, and treat a `{}` parse as a **FAIL** under Z-G4 rather than as
   a doc with no status. That is exactly the "cannot compute its ground truth" case.
3. **`[#577]` and `[#584]` are closed.** `BACKLOG.md` is **206** rows; `validate_doc_rot` is at
   **59**.
4. **Both audit baselines were regenerated** under operator approval —
   `ecosystem/audit-consumer-baseline.json` and `ecosystem/audit-funnel-baseline.json`. If your
   check reads either, read the committed one, and do **not** rewrite them: a baseline write is an
   acceptance act and it is not in your write-scope.

**The freshness-vs-correctness gap is a candidate filing, not your work.** `intake-index-freshness`
is regen-and-diff, so it reproduced the wrong index byte-for-byte and stayed green through all six
broken docs. Do not try to fix that inside `check_funnel_lifecycle`; report it.
