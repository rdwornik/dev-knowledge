# Census — the [#664] orphan residue: DELETE / TRIGGER / KEEP, one file for one GO

**Consumers:** `[#664]` · intake #86 · `docs/audits/2026-09-13-census-x-664-spine-armed-measurement.md`
**Delivered as:** `to-browser/DELETE-LIST-2026-09-13.md` (plain copy, this file is the source)

**What this asks for.** One word. Every row below carries exactly one proposal from a closed
set — **DELETE**, **TRIGGER** or **KEEP** — and its evidence. Reply per row, or reply `ALL AS
PROPOSED` and the execution lane runs the list. There is deliberately no defer state: a defer
state is how these thirty-six got here.

**What this does NOT do.** Nothing here is executed. Deletions are the operator's act and run
in a single lane after the GO — this lane's contract says so and `[#734]` sets the shape.

---

## 0 · Read this before the list — two things that will otherwise mislead

**This is NOT `[#734]`'s list, and the two share a number by coincidence.** `[#734]` disposes
of the DOMAIN CENSUS's thirty-five non-live items (24 untriggered + 10 unread + 1
garbage-candidate, out of 248 — `docs/audits/2026-09-11-technical-domain-census.md`, its
`REPO TOTAL` row). This is the thirty-six untriggered **process nodes** FPG-1 holds, plus one
register row whose subject is no longer untriggered. Different populations, and they were the
same size when this lane started — the coincidence is what makes the confusion likely. **Do not
double-count, and do not read a GO on one as a GO on the other.**

**No DELETE row below carries a `safe_remove` verdict, and that is stated rather than
omitted.** The reverse-dep oracle needs a vendored pyright (`npm install`) that is not
provisioned on this box; it returned `oracle-unavailable` for all nine candidates tried. It
would not have been sufficient anyway: ADR-89 declares the oracle static-only, and
`scripts/desired_state_loader.py` is this repo's own witness that a SAFE verdict can be a FALSE
PASS — it was deleted on one, the suite went RED, and it was restored whole. **The execution
lane runs the oracle as its own precondition.** The evidence each row carries here is FPG-1's
inbound-edge set, which is the organ `[#664]` built for exactly this question.

**Method.** Every row's evidence is read from the persisted store via
`scripts/graph_queries.py process-list` and the store's own `in_edges`. An `implements` edge
from a `tasks/` row is a row NAMING the file — it is ownership, never a trigger, and a module
named by eight open rows and fired by nothing is precisely the state this list exists to end.

**Re-measured after a sync, and the movement is shown rather than smoothed.** The companion
measurement artifact records 35 untriggered processes and 36 disposition rows at `5e280b05`.
Mid-lane, `lane-x-730-one-command-closure` merged to `main` and this lane synced: the register
gained a 37th row (`scripts/propose_row_closures.py`, §4.5). **This list is the post-sync
reading**; the measurement artifact is a dated measurement and stands as taken, which is the
same rule the register itself states — *"the census is a dated measurement, not a live
roster."*

```
at 5e280b05   159 processes · 124 triggered · 35 untriggered · 36 disposition rows
post-sync     160 processes · 124 triggered · 36 untriggered · 37 disposition rows
```

**Totals:** 37 rows — 6 DELETE · 2 TRIGGER · 28 KEEP · 1 register-row correction (§1).

---

## 1 · The one row that is not about a file — ESCALATED, not proposed

**`scripts/worktree_seed.py` — DELETE THE REGISTER ROW, not the module.**

It is no longer an orphan. `.pre-commit-config.yaml` triggers `scripts/gen_lane_contract.py`
(the `lane-contract-check` hook) and that module **imports** `worktree_seed`, so it is reachable
over `TRIGGER_KINDS`. Its `ORPHAN_DISPOSITIONS` entry now records a ruling about a condition
that no longer holds, and
`tests/test_graph_spine.py::test_a_disposition_register_entry_cannot_manufacture_its_own_trigger`
is RED because of it.

Two independent lanes have now declined this same one-line edit as a **curated-baseline touch**
(V-2 class (a)): `lane-x-000-trustworthy-suite` (its evidence artifact, finding 1) and this one.
Two lanes declining on the same rule is the rule working. **It needs your word, and it is one
line.**

*A footnote, because the shorter diagnosis is wrong and will be repeated otherwise:*
`.claude/settings.json` also names the path, which is what `why` reports first — but it names it
inside a `"//worktree"` COMMENT key. That edge is spurious (§8.2 of the measurement artifact);
the import edge above is the real one, and it survives whatever happens to the comment.

---

## 2 · DELETE — 6 rows

Each is lane-built, never adopted, and reachable from nothing that runs. Git keeps the history,
which is what makes deletion cheap and reversible rather than destructive.

**`scripts/gen_trend_dashboard.py`** — inbound: 3 `implements` (rows `[#589]` `[#615]`
`[#694]`), 0 executable. `[#694]` names it by name as one of the three telemetry modules still
inventory after Half A, and rules that a module either gains a call site on a real trigger or
is deleted — *"a module left in place with a docstring explaining what it would measure is the
failure state this row exists to end."* Its only recorded call site is a lane contract.
**Owner of the decision: `[#694]`.**

**`scripts/window_metrics.py`** — inbound: 4 `implements` (`[#470]` `[#611]` `[#689]`
`[#694]`), 0 executable. Same `[#694]` population, same ruling. Only call site is
`LANE-r-000-zc-candidates.md:39`.

**`scripts/failed_set.py`** — inbound: 1 `implements` (`[#694]`), 0 executable. Reachable only
from `window_metrics.py:359`, which is itself untriggered — an orphan by inheritance.
**DELETE WITH `window_metrics.py`, never before it**: deleting it first turns a clean removal
into a broken import.

**`scripts/gen_north_star.py`** — inbound: 2 `implements` (`[#383]` `[#624]`) plus **one
`imports` edge from `gen_trend_dashboard.py`**, which is itself a DELETE row above. So its only
code referrer dies with the row above it. **ORDERED: after `gen_trend_dashboard.py`.** Only
recorded call site is `batch-e CUT.md:40`.

**`scripts/nopack_sandbox.py`** — inbound: **NONE, of any kind.** No row names it, no module
imports it, nothing triggers it. Only recorded call site is `LANE-e-5-vision-relocation.md:46`,
an immutable lane contract that has already run.

**`scripts/trace_writer.py`** — inbound: **NONE, of any kind.** Only recorded call site is
`LANE-t-000-trace-scorecard.md:47`, likewise spent.

---

## 3 · TRIGGER — 2 rows

Each names the specific surface that would fire it. An untriggered module is not saved by good
intentions, so a TRIGGER that cannot name its hook is a DELETE wearing a better coat.

**`scripts/archive_row_body.py` — TRIGGER, and `[#664]` already ordered it.** Inbound: 8
`implements` rows and one test. The row this lane serves says in its own words that
*"`archive_row_body` gaining its trigger ride"* is an edge of this arc, **not a separate row**.
Referenced today only by `tests/test_archive_row_body.py` — and a test proves a module works
while scheduling nothing, which is why it is not a trigger. **Naming surface: the pre-commit
stage, beside the row-lifecycle gates.** This is the one row on the list whose disposition is
already written down; it wants execution, not a decision.

**`scripts/logs_retention.py` — TRIGGER.** Inbound: 3 `implements` (`[#626]` `[#655]`
`[#704]`), 0 executable. **`[#655]` is an open row whose entire title is "run_retention has no
production caller"** — the question is filed, and the answer the corpus keeps reaching for is a
caller rather than a removal: `353b5169` moved `propose_closures` output into `logs/YYYY-MM/`
expressly as *"the caller the retention rule never had"*. **Naming surface: the same
`SessionStart`/`Stop` path that writes the logs it would retain.** **Owner: `[#655]`.**

---

## 4 · KEEP — 28 rows, grouped by the reason, one line each

### 4.1 Settled by a ruling — wiring it would be the defect (4)

- **`scripts/export_backlog_view.py`** — orphan BY DESIGN; `[#563]`'s one-way view layer, and
  `tests/test_export_backlog_view.py::test_no_gate_hook_or_script_reads_the_export` ASSERTS
  nothing reads it. Wiring it REDs that test. This row must never be "fixed".
- **`scripts/desired_state_loader.py`** — KEPT 2026-09-12 on POSITIVE evidence:
  `tests/test_membership_agreement.py` loads it by name through `importlib`. Deleted once on a
  SAFE oracle verdict; the suite went RED; restored whole. It is this list's own cautionary
  witness.
- **`scripts/propose_closures.py`** — a derived-copy SOURCE, not an orphan. The armed process is
  the plugin copy the `Stop` hook fires; `ecosystem/derived-copies.yaml` owns the pair.
- **`scripts/setup-fleet-scheduler.ps1`** — a one-shot INSTALLER. The task it registers is live
  (`fleet-baseline`, State=Ready), so the PROCESS is triggered; an installer is not a recurring
  process and never was.

### 4.2 Unwired BY CONTRACT — a successor adopts it, and wiring it now would assert something that was refused (3)

- **`scripts/provider_router.py`** — `[#691]` Half A is forbidden from ordering any non-Claude
  provider, and routing through the router IS placing a call. Unwired is the contract-required
  state. **Owner: `[#691]` Half B**, which adopts it by routing through it.
- **`scripts/cost_usage_telemetry.py`** — **its disposition text is STALE and the row is a KEEP
  rather than the DELETE that text implies.** `[#694]` records it PARTIALLY DISCHARGED: it is
  *"no longer inventory"* and has a real call site in `provider_router.py`, which FPG-1
  confirms (`in/imports: scripts/provider_router.py`). It is untriggered only because its caller
  is, so it inherits the row above and moves with it.
- **`scripts/offload_admission.py`** — unwired BY DESIGN: its lane REFUSED the only route it
  measured and deliberately did not write `ecosystem/routing-table.yaml`. Wiring it would assert
  an admission that was denied.

### 4.3 Adopted by a command file, which the census does not count as a wiring surface (3)

**These three are the same finding three times, and they are an ASK rather than three rows —
see §5.**

- **`scripts/merge_receipt.py`** — wired at four points of `.claude/commands/lane-integrate.md`.
  A pre-commit trigger is wrong on the merits: a stopwatch has nothing to gate.
- **`scripts/actions_verdict.py`** — wired to the same command. A pre-commit trigger would query
  a GitHub Actions run for a merge SHA that does not exist at commit time.
- **`scripts/review_packet.py`** — wired to the same command. It assembles a review input over a
  merge range against a lane contract, neither of which exists at commit time.

### 4.4 ON-DEMAND-BY-OPERATOR — one of the census's seven acts (16)

Nothing in this repo fires a command or a skill, and none should. Each maps to an act:

- **`scripts/single_flight.py`** · GO — `/lane-boot:71`, `/lane-integrate:132`
- **`scripts/worktree_import_proof.py`** · GO — `/lane-boot:174`
- **`scripts/review_closures.py`** · ratification — `/review-closures`; also a derived-copy source
- **`plugins/tier1-lifecycle/scripts/review_closures.py`** · ratification — the plugin copy
- **`.claude/commands/boot-session.md`** · sitting
- **`.claude/commands/handoff.md`** · seat release
- **`.claude/commands/handoff-verify.md`** · seat release
- **`.claude/commands/lane-boot.md`** · GO
- **`.claude/commands/lane-integrate.md`** · GO
- **`plugins/tier1-lifecycle/commands/review-closures.md`** · ratification
- **`plugins/tier1-lifecycle/commands/ship.md`** · destructive acts
- **`.claude/commands/preflight.md`** — its own frontmatter says *"wired into no gate"*; an
  adoption-first read-only helper is a legitimate shape for a self-declared orphan
- **`.claude/commands/save.md`** — a convenience wrapper, not one of the seven acts
- **`.claude/commands/changelog-review.md`** — a PUSH trigger only. A `SessionStart` sentinel
  NUDGES it, and a nudge is not a trigger — a distinction the census draws deliberately
- **`.claude/skills/verify/SKILL.md`** — no event fires a skill. `[#664]`'s anti-pattern list
  rules the repair: **a skill's mandate becomes a HOOK, never a graph row**
- **`.claude/skills/check-against-spec/SKILL.md`** — same class; the mandate lives in prose, and
  prose is carried by a seat's diligence

### 4.5 Operator-transport report generators — their wiring question IS §5's, and is answered there (2)

Both write a file the operator reads out of `to-browser/` and are run from the CLI on demand.
Neither is lane-built-and-abandoned, and neither has a hook that could sensibly fire it: a
report generator's trigger IS an operator invocation. **If §5 rules that a command file is a
wiring surface, both of these resolve without a further decision** — which is why they are
grouped rather than proposed individually.

- **`scripts/gen_ledger.py`** — inbound: **NONE, of any kind**, which reads like a DELETE and is
  not. `LEDGER-<repo>.md` is a **declared transport artifact** in
  `protocols/OPERATOR-INTERFACE.md`'s v2.1 filename table (*"the operator's read surface,
  overwritten each batch and wrap"*). The artifact is ruled; only its producer is unwired, and
  deleting the producer of a declared surface leaves the surface to be hand-maintained — the
  defect this whole row-family exists to end.
- **`scripts/propose_row_closures.py`** — **arrived tonight**, dispositioned by its own lane
  (`lane-x-730-one-command-closure`) in the same act that wrote it. It writes
  `to-browser/CLOSURE-LIST-<date>.md`. Its lane deliberately left the wiring decision open as a
  `[#664]`-scope question; this is that question, and it is §5.

---

## 5 · The ONE structural ask, which is worth more than any single row above

**Should `.claude/commands/*.md` count as a `[#664]` wiring surface?**

Today the census reads five surfaces — `.pre-commit-config.yaml`, `.claude/settings.json`, the
plugin `hooks.json`, the scheduled task, the CI workflows — and a command file is none of them.
So **every operator-invoked organ in this repo reads as an orphan by construction, whatever its
real adoption**. That is not a property of any module; it is a gap in the census's input list,
and it is why §4.3, §4.4 and §4.5 together are **21 of these 37 rows** — a clear majority of
the list.

- **YES** — the register loses roughly 21 rows at once, the three `[#675]` modules stop reading
  as unadopted, the two report generators in §4.5 resolve with no further decision, and
  "untriggered" starts meaning *nothing invokes this*, which is what the word should mean.
- **NO** — the register keeps a standing 21-row tail that every future reader must be told to
  discount, it grows by one every time a lane writes an operator-invoked organ (it grew by one
  during this lane), and the orphan census keeps answering a question nobody asked.

**One word here disposes of more of this list than every row above it combined.** It is a
ruling, not a lane's call, which is why it is asked rather than taken.

---

## 6 · What happens on your GO

1. Approved **DELETE** rows execute in ONE lane, in the order §2 states (`window_metrics` before
   `failed_set`; `gen_trend_dashboard` before `gen_north_star`), with `safe_remove.py` run as
   that lane's precondition after `npm install` provisions the oracle — and with a paired
   baseline/tip suite run, because a SAFE verdict is necessary and not sufficient.
2. Approved **TRIGGER** rows get their named hook, RED-first, one row per commit.
3. **KEEP** rows stay and their disposition text is corrected where §4.2 says it is stale
   (`cost_usage_telemetry.py`).
4. §1's register row and §5's ruling are yours; both are one line of work once ruled.

---

**Produced by:** lane `lane-x-664-spine-armed`, batch X wave 3 slot 5, 2026-09-13.
**Nothing in this file has been executed.**
