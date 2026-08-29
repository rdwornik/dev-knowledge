# NB2 · WAVE 2 · LANE L — FM-5 hand-back packet

**Batch:** night-batch-2, wave 2 · **Lane:** L (FM-5, "the value half, scoped honest", S)
**Branch:** `worktree-lane-l-5-fm-governance-health` · **Base:** `77096131` (main at dispatch)
**Contract:** `docs/audits/2026-08-28-technical-fm-wave2-frozen-bundle.md` §FM-5, dispatched via
`NB2-W2-LANE-L-FM5-governance-health.md`
**Substrate:** local · **Consumer:** the wave-2 integrator (merge queue) and lane K (FM-4), which
imports this lane's two exported derivations.

---

## 0 · THE EX-ANTE, VERBATIM, THEN THE MEASURED RESULT

> *"Ex-ante: the command runs on merged main and its numbers equal FM-4's block byte-for-byte for
> the shared fields."*

**Measured: NOT-MET, and unmeasurable in-lane — by construction, not by omission.**

The Ex-ante binds *merged main*, and its other party had not merged: lane K (FM-4) was provisioned
at the same moment as this lane (`git branch` shows `worktree-lane-k-4-fm-boot-surface` created 9
minutes before this lane's first act) and has landed no emitter in this tree. The contract
anticipated exactly this and ruled the response:

> *"If lane K has not merged when you run, write against its path, say the coupling is unproven,
> and **still ship the equality test** — RED until K lands is an honest RED, and it is the proof
> the Ex-ante asks for."*

So the Ex-ante ships as an executable test that measures it the moment K lands, with **no edit**:

```
tests/test_governance_health.py::test_shared_fields_equal_fm4_block_byte_for_byte  FAILED
  FM-4's FUNNEL HEALTH emitter is not resolvable, so the byte-for-byte equality cannot be
  measured. Resolution report: no callable in gen_handoff matches
  /funnel.*health|health.*funnel/ — either FM-4 (lane K) has not landed its emitter in this
  tree, or it landed under a name this resolver's rule does not match. gen_handoff's public
  callables: BoundaryHygieneError, BundleCollisionError, BundleIdentityError, GenResult,
  OpenBatchError, Path, assert_batch_boundary, assert_boundary_hygiene, collect_hints,
  collect_state, dataclass, detect_fill_state, dispatch_form, generate, journal_draft, main,
  reflow_framing, standing_vs_new, verify_seal_identity
```

**The coupling is UNPROVEN and is declared so.** The message names both possible causes rather
than the flattering one, and prints `gen_handoff`'s public roster so the integrator settles which
it is by reading, not by trusting this packet.

**One integrator decision this creates, stated plainly:** this lane knowingly adds **one RED to
the suite** until K merges. It is contract-mandated (quoted above) and it is the ONLY RED this
lane owns.

---

## 1 · PER DONE-ITEM — MET / NOT-MET / PARTIAL, each with a witness

The contract's write-scope: *"audit.py runner reuse (a `governance-health` command) +
close-packet parsing + tests. Renders FM-4's numbers on demand + a per-closed-row 'what it bought'
line sourced from close packets; A1: emits into the telemetry store so trends exist. Telemetry
intake #50 stays its own arc — do NOT absorb it."*

### (1) Runner reuse — a `governance-health` command on the existing runner — **MET**

`audit.py` is a `click` group (`@click.group()` at `scripts/audit.py`, `def cli()`), and its
subcommands are `@cli.command("run"|"repo"|"registry"|"health"|"ship-gate"|"checks")`.
`governance-health` is registered in exactly that shape.

**Witness:** `tests/test_governance_health.py::test_subcommand_is_registered_on_the_existing_runner`
asserts `"governance-health" in aud.cli.commands` **and** that `{run, repo, health, checks}` are
still present — reuse, not a rewrite. `test_no_second_argument_parser_was_added` asserts the
library source contains no `argparse`, no `ArgumentParser`, no `click.group`, no `@click.command`.

**Count-pin note, as the contract asked for:** registering a *command* touches **no**
`ALL_CHECKS`-adjacent pin. `audit.py health` reports `doc_code_coverage_drift: all 53 ALL_CHECKS
members covered` after the change — the roster is unmoved, because this lane added a CLI verb and
not a check. No oracle line-offset test fired either; the whole targeted `tests/test_audit.py`
(243 cases) was run to establish that, not assumed.

### (2) Renders FM-4's numbers on demand — **PARTIAL, and the partiality is the design**

The command renders the block on demand. What it renders for FM-4's four fields is
`unavailable` **with a resolution report**, because FM-4's emitter does not exist in this tree.
That is the contract's own instruction ("say the coupling is unproven"), and the alternative —
computing the numbers here so the output looks complete — is the precise failure the batch exists
to remove.

**The negative is enforced structurally, not by inspecting output.**
`test_no_fm4_owned_field_is_derivable_from_this_module` scans the module's namespace for any
callable whose name contains `intake` / `adr` / `orphan` / `unarchived` / `unexecuted` and fails
if one exists. Reading the rendered text would pass just as happily the day someone adds
`_count_unarchived_intakes()` and wires it in.

**Live output (`uv run --locked python scripts/audit.py governance-health`, 2026-08-29):**

```
governance-health
  FM-4 emitter: unavailable - no callable in gen_handoff matches /funnel.*health|health.*funnel/ ...
  window base: 50943b6bfc434dec77a65e110d7f1a7d96939593
  close packets read: 5

FUNNEL HEALTH
  intakes consumed-unarchived: unavailable
  ADRs unexecuted: unavailable
  orphans forward: unavailable
  orphans backward: unavailable
  rows closed this window: 2
  value evidence attached: 1
```

### (3) Close-packet parsing + a per-closed-row "what it bought" line — **MET**

**The shapes were witnessed, not trusted.** The contract listed two candidate globs and said to
verify them. On disk (`docs/audits/`) the live close packets are:
`2026-08-14-technical-batch-4-true-close-packet.md`,
`2026-08-26-verification-batch-1-close-packet.md`,
`2026-08-27-verification-batch-w2-close-packet.md`,
`2026-08-28-technical-batch1-end-of-batch-packet.md`,
`2026-08-29-verification-night-mission-close-packet.md` — **5**, matching both globs. A per-lane
`*-nb2-<letter>-packet.md` is deliberately excluded: it is one lane's hand-back, not the batch's
account of what the batch bought. `test_close_packet_discovery_is_pattern_bound` pins that
boundary.

**Evidence is QUOTED, never synthesised** — the packet's own line, verbatim, with a
`docs/audits/<file>:<line>` locator. The module has no sentence-writing path at all: it can quote
or it can say `no value evidence`.

**Live value section, and it is the honest one after the terra fix:**

```
VALUE - what each closed row bought (verbatim from close packets; never invented)
  [#577] (line cites 2 rows or more; attribution unverified) - .../2026-08-28-...-end-of-batch-packet.md:17 - ### L1 - [#577]+[#584] root AGENTS.md + the section-10 lockstep - **MET**
  [#577] - .../2026-08-29-verification-night-mission-close-packet.md:146 - | **F** (N7) | `[#577]` | `b4ab25ab` | **3/3 MET**; `[#577]` discharged **5 of 5 clauses** | ...
  [#577] - .../2026-08-29-verification-night-mission-close-packet.md:318 - although batch-1 landed their work and lane F discharged `[#577]`'s done-when **5 of 5 clauses**
  [#577] (line cites 2 rows or more; attribution unverified) - .../2026-08-29-verification-night-mission-close-packet.md:463 - 7. **`[#577]` and `[#584]` are closure candidates** - ...
  [#584] - no value evidence of its own; shown below, attribution unverified
  [#584] (line cites 2 rows or more; attribution unverified) - .../2026-08-28-...-end-of-batch-packet.md:17 - ...
  [#584] (line cites 2 rows or more; attribution unverified) - .../2026-08-29-verification-night-mission-close-packet.md:463 - ...
  coverage: 1/2 rows carry sole value evidence, 1 do not
```

### (4) The coverage fraction the contract asks for — **MET**

*"Report the coverage fraction: how many closed rows in the window carry value evidence and how
many do not."* → **1 of 2 rows carry sole value evidence; 1 does not.** `[#584]`'s only packet
lines also name `[#577]`, and the verdict on those lines belongs to `[#577]`.

The command reports this itself (`coverage: 1/2 …`), so the number is regenerable rather than a
figure typed into a document.

### (5) A1 — emits into the telemetry store so trends exist — **MET, end-to-end witnessed**

**The store, located and named as the contract required.** The contract suggested `logs/*.jsonl`
and told me to confirm rather than assume. **Confirmed and corrected:** this repo's telemetry
store is **`logs/TELEMETRY.db`** — one append-only SQLite table in WAL mode, owned by
`scripts/telemetry_emit.py`, specified by `docs/archive/2026-08-14-research-usage-telemetry-design-wf-0e8cd658.md`
Stage 1 and the `[#529]` row. `logs/PARITY-EVENTS.jsonl` is a real event stream but it is
`fleet_parity`'s own gitignored rotation-capped log, not the telemetry store; the design memo is
explicit ("Start with SQLite in WAL mode as the event store, **not raw JSONL**"). Naming the
`.jsonl` file as "the store" would have created the second store A1 forbids.

**Live emission, read back from the store:**

```
1 2026-08-29T09:27:08.877780+00:00 check_run governance_health pass 1365 run b89f98b5
{
  "close_packets": 5,
  "fm4_source": "unavailable",
  "git_derived": true,
  "shared": { "ADRs unexecuted": "unavailable", "intakes consumed-unarchived": "unavailable",
              "orphans backward": "unavailable", "orphans forward": "unavailable",
              "rows closed this window": "2", "value evidence attached": "2" },
  "value_coverage": { "attached": 2, "considered": 2 },
  "window_base": "50943b6bfc434dec77a65e110d7f1a7d96939593"
}
```

*(That capture predates the terra P1 fix, which is why it reads `attached: 2`; the live command
now records `1`. The record's SHAPE is what this witnesses, and the numbers it carries are the
command's own at emit time.)*

**No second store, and it is asserted rather than promised.** `test_emit_writes_no_second_store`
snapshots the tmp tree after an emit and fails on any file outside `{TELEMETRY.db, -wal, -shm}`.
`test_emitted_context_carries_every_shared_field` fails if any shared field is missing from the
record — a trend that has to re-derive its own values is not a trend. Event type is the existing
`check_run`; **no fourth event type was added.** Emission follows `audit.telemetry_enabled()` —
the existing switch, default OFF — so no gate's behaviour changed.

**Owed-step note:** `telemetry_emit.py`'s docstring records that wiring its CALL SURFACE is an
explicitly owed phase-3 step. `audit.py` became its first call site at `[#529]` leg 1; this
command is a second one on the same documented surface. Nothing new was built to carry it.

### (6) Scope fence — intake #50 not absorbed — **MET**

Read: `docs/intake/2026-08-26-tech-cost-and-delivery-telemetry.md` (intake-id 50, status READY).
That arc is a **weekly cost-and-delivery pipeline**: provider billing APIs + `ccusage` local token
usage + Codespaces core-hours + git delivery, joined in DuckDB/SQLite, rendered as Markdown,
**committed to a repo**, run on a **cron**, and explicitly *"the first CONSUMER arc (O4 parity),
not a hub arc"*, with the 2026-08-26 billing-leak replay as its acceptance test.

**The boundary, named as the contract asked:** this lane builds no provider API call, no cost
figure, no cron, no committed report, and touches no consumer repo. It is a hub CLI that renders
numbers another lane derives and appends one local gitignored row to a store that already exists.
The fence is the *pipeline*; nothing here approaches it. Stated permanently in the module
docstring ("WHAT THIS IS NOT"), not just in this packet.

### (7) RED-first — **MET, three separate witnesses**

1. **The module's own birth.** Every case in `tests/test_governance_health.py` was written and run
   BEFORE `scripts/governance_health.py` existed:
   `ModuleNotFoundError: No module named 'governance_health'` — *1 error during collection*, 0
   tests. That is the honest RED for a module that is not there.
2. **The discriminator went red on purpose and stayed green for the right reason.**
   `test_a_bare_mention_is_not_value_evidence` exists because without it the predicate could be
   `id in line` and every other case would still pass while coverage reported 100% forever.
3. **A real defect, red before the fix.** `test_a_quoted_arrow_delta_would_crash_a_cp1252_console_unencoded`
   asserts the raw packet line is *unencodable* in cp1252 before asserting `console_safe` fixes
   it — so the test fails if the defect it guards ever stops being real.

Plus two REDs that were **discovered**, not designed, and are recorded in §4.

---

## 2 · COMMIT SHAs, IN ORDER

| # | SHA | What |
|---|---|---|
| 1 | `11f7bfc4` | `feat(audit): governance-health — FM-4's numbers on demand + what each closed row bought` |
| 2 | `ae8757ce` | `fix(audit): terra pre-merge corrections — attribution, git-derivation, resolver` |
| 3 | *(this commit)* | this packet — `docs(audits): FM-5 lane-L hand-back packet` |

**Files:** `scripts/governance_health.py` (new), `scripts/audit.py` (+1 subcommand, +1 import
shim), `tests/test_governance_health.py` (new), this packet. **No** `protocols/`, **no**
`templates/`, **no** `tasks/`, **no** generated surface, **no** JOURNAL entry.

---

## 3 · TERRA TALLY (pre-merge, `codex exec` over this lane's own diff)

```
TALLY: critical=0 high=5 medium=0 low=0
```

Run with `codex exec` (not `/codex-review` — a mixed doc/code diff kills that lane), codex-cli
0.145.0, scoped in the prompt to the staged diff. **Four accepted and fixed, one rejected.**

| # | Finding | Disposition |
|---|---|---|
| P1 | Status tokens misclassified as value evidence — a multi-row line attributed to every id on it; negations (`not closed`) matched | **ACCEPTED, FIXED.** Evidence now carries `shared`; a multi-row line is shown and MARKED but excluded from the coverage numerator, which counts SOLE evidence only. Negation guard added. **Measured effect on the live tree: coverage 2/2 → 1/2**, `[#584]` correctly reads "no value evidence of its own". Tests: `test_a_line_citing_two_rows_is_shared_and_does_not_count`, `test_a_negated_verdict_is_not_value_evidence` |
| P2 | The `git_derived` closure count mixed git history with working-tree reads; renames scored as new closures | **ACCEPTED, FIXED.** Both sides now read git blobs (`base:` / `HEAD:`); diff is `--name-status -M` so a rename compares against its own earlier blob; row id from frontmatter. Test: `test_rows_closed_ignores_the_working_tree_and_survives_a_rename` (real-git fixture, asserts both properties) |
| P3 | The FM-4 resolver could bind a module-private helper, crashed on a wrong callable, and hid the import error | **ACCEPTED, FIXED.** `_`-private names excluded; a failing call demoted to a resolution report instead of a traceback; the import exception preserved so "missing" and "broken" no longer read alike |
| P4 | The equality test compared only the INTERSECTION of field names; the docstring's "both render from the same function" overclaimed | **ACCEPTED IN PART, FIXED.** The test now requires the full `FM4_OWNED_FIELDS` set present in FM-4's block and compares every field. The docstring is corrected to what the Ex-ante actually binds — the NUMBERS, parsed by one shared function; a browser-visible bundle and a CLI report are not required to be one surface |
| P5 | "The staged test suite contains an intentional unconditional failure" | **REJECTED — contract-mandated.** *"still ship the equality test — RED until K lands is an honest RED, and it is the proof the Ex-ante asks for."* Recorded, not relitigated |

---

## 4 · TWO DEFECTS FOUND AND FIXED IN-LANE (neither was in the contract)

**(a) Package-mode import — RED first, in a sibling test.** The first cut imported
`gen_task_tree` by bare name. Under package mode (`from scripts import audit` — repo ROOT on
`sys.path`, not `scripts/`) that raises `ImportError`, which `audit.py`'s own dual shim then
mis-read as *"governance_health is absent"*, and the module failed to import entirely:

```
tests/test_audit.py::test_check_fleet_parity_package_mode_import  FAILED
  ModuleNotFoundError: No module named 'governance_health'
```

Fixed with dual shims matching `audit.py`'s own `_te` / `_vgb` / `_vdc` pattern, in **three**
places (the top-level import, `_handoff()`, and `emit()`'s `telemetry_emit` import — the second
would otherwise have degraded silently to "FM-4 has not landed" in package mode). A direct
regression test was added rather than leaving the property to a `fleet_parity` test to notice.

**(b) A live cp1252 console crash, latent in the lane's core function.** This command quotes
arbitrary close-packet prose and `click.echo` raises `UnicodeEncodeError` on a Windows cp1252
console for anything outside cp1252 — the trap `check_doc_code_edge` already carries an "ASCII
arrow" comment about. It is **live, not hypothetical**:
`docs/audits/2026-08-26-verification-batch-1-close-packet.md` contains U+2192, and `_DELTA_RE`
matches `77 → 60`, so the very lines this command exists to quote are the likeliest carriers.
`console_safe()` escapes (`→`) rather than dropping — an escape a reader can decode
preserves evidence; silently deleting a character out of a line advertised as verbatim would be
the worst available outcome.

---

## 5 · CANDIDATE FILINGS (reported, never filed)

1. **Name FM-4's emitter path by ruling, so the coupling stops being a name-shaped guess.**
   FM-4's contract deliberately does not name its emitting function, so FM-5 resolves by
   capability (a public callable whose name carries both "funnel" and "health") and REFUSES on
   ambiguity. Terra P3 is right that this is weaker than an explicit export. **One line from the
   integrator or the architect** — the dotted path FM-4 actually landed — replaces the regex with
   a hard binding. *Owner: integrator/architect, at K's merge.*

2. **`rows closed this window` has no ruled owner, and this lane took it by elimination.**
   FM-2's four FAIL classes do not produce it; FM-4's contract does not derive it; FM-4's block
   carries it. It is implemented here and exported for FM-4 to import (`FM5_OWNED_FIELDS`). If
   the architect places it elsewhere, moving it is a one-line change to two tuples and the
   equality test measures the result unchanged. *Owner: architect.* Same note applies to
   `value evidence attached`, which is FM-4's fifth field and can only be computed by
   close-packet parsing — i.e. inside FM-5's write-scope. **If lane K implements either
   independently, the batch has two truths for one number and the integrator must reconcile at
   merge.**

3. **The window boundary is resolved twice.** `gen_handoff._window` states this repo's window
   definition and returns *(previous bundle slug, changed paths)* — not the boundary sha. This
   module re-runs that function's one documented git command to get the sha
   (`governance_health.window_base_sha`, which says so in its docstring). One CALL is duplicated;
   no second DEFINITION exists. A sha-returning window resolver in `gen_handoff` would remove
   even that. *Owner: FM-4 / a later consolidation.*

4. **The value-evidence predicate is a heuristic over prose and both its error directions are
   now measured.** A false negative is live and identifiable: the night-mission close packet's
   line 22 (`| **W1-5** | … **not 9,161 B** … | **MET, with the ex-ante's own number corrected** |`)
   IS value evidence and is scored as none, because the negation guard sees `not` within its
   window of `MET`. The bias is deliberate — an under-count is recoverable, a fabricated benefit
   is not — but a **structured close-packet field** (terra's own fix direction) would remove the
   guesswork entirely on both sides. *Owner: a close-packet schema arc, not this lane.*

5. **`governance-health` is wired into no gate**, by design and consistent with `checks`: it is
   an on-demand read surface, not an organ. Whether the funnel numbers should ever BLOCK is FM-2's
   question, not this command's. *Owner: architect.*

---

## 6 · BUDGET DECISIONS

**Ratchet — measured twice, as instructed, and NOT assumed from the dispatch figure:**

| When | Detector | Files | Count |
|---|---|---|---|
| Before the first commit | `silent-rule-v5` | 61 | **443** |
| Before the last commit | `silent-rule-v5` | 61 | **443** |

**Delta 0.** `protocols/` and `templates/` diffs are empty (`git diff --cached --stat --
protocols/ templates/` returns nothing), which is what this lane's contract requires. The
`audit.py health` gate confirms it independently: `silent_rule_ratchet: live 443 <= baseline 443
under detector silent-rule-v5 (61 file(s) in scope)`. No authorization was requested and none was
spent.

**Other budget calls:**

- **No `tasks/` write, no row closure, no generated-surface regeneration.** None was forced by a
  gate, so §"THE FOUR THINGS" item 4's escape hatch was never used and there is no such commit to
  name.
- **Scope held at S.** The terra fixes were taken because they are correctness defects in the
  lane's own deliverable, caught by the reviewer the contract mandates — not scope growth. The
  fix directions terra proposed that WOULD have grown scope (a structured close-packet schema; a
  canonical shared renderer across two lanes) are filed as candidates instead.
- **No JOURNAL entry.** Per §"THE FOUR THINGS" item 1 — the integrator writes one anchor for the
  whole queue. The Stop hook's demand is declined explicitly on that ground (ADR-85 amendment
  2026-08-03 §A5 made it advisory in full; the hard leg is `block-unanchored-push`, and a lane
  does not push).
- **No self-merge, and none suggested.** This branch enters the frozen queue.

---

## 7 · GATE STATE

| Gate | Result |
|---|---|
| `uv run --locked python scripts/audit.py health` | **OK** (`health: OK`) — including `silent_rule_ratchet` at baseline and `doc_code_coverage_drift: all 53 ALL_CHECKS members covered` |
| `uv run --locked ruff check` (lane files) | **All checks passed** |
| `tests/test_governance_health.py` | **23 passed, 1 failed** — the failure is the Ex-ante RED of §0, and is the only RED this lane owns |
| `tests/test_audit.py` (243 cases) | **all passed** after the package-mode fix (1 RED before it — §4a) |
| `tests/test_telemetry_wiring.py`, `tests/test_ship_gate.py`, `tests/test_audit_parallel.py` | **all passed** |
| `tests/test_audit.py::test_check_fleet_parity_package_mode_import` | **passed** (re-verified after the terra round) |

**Inherited REDs, not run and not claimed:** the full suite is the integrator's single run. The
contract names two known non-lane REDs (the anchor-gate probe test, RED on main since 2026-08-22;
`test_stale_worktrees`, structurally RED in a lane worktree). Neither was touched by this lane and
neither is asserted here — this lane ran **targeted** tests only, per the contract.

---

## 8 · DEVIATIONS, WITH OWNERS

| # | Deviation | Owner |
|---|---|---|
| 1 | **The Ex-ante ships RED.** Contract-mandated; it becomes a live measurement at K's merge with no edit. If K's emitter lands under a name the capability regex does not match, this test stays RED and its message says so explicitly rather than blaming K — resolve with candidate filing #1. | Integrator, at K's merge |
| 2 | **`rows closed this window` and `value evidence attached` are implemented here** rather than imported from FM-4, because neither FM-2 nor FM-4 derives them. Exported for FM-4 to import. If K implemented either independently, reconcile at merge. | Architect / integrator |
| 3 | **The telemetry store named in this lane's contract prompt (`logs/*.jsonl`) is not the store.** The contract said to confirm rather than assume; confirmed as `logs/TELEMETRY.db` (`[#529]`, SQLite/WAL), with `PARITY-EVENTS.jsonl` identified as `fleet_parity`'s own log. Emitting into the `.jsonl` would have created the second store A1 forbids. | Recorded here; no act owed |
| 4 | **One duplicated git CALL** for the window base sha (candidate filing #3), because `gen_handoff._window` returns a slug and paths, not the sha. No second window DEFINITION exists. | FM-4 / later consolidation |
| 5 | **`console_safe` transliterates at the CLI boundary**, so a quoted line containing a non-cp1252 character prints as `→` rather than the glyph. The stored/parsed text is untouched and the locator is always present, so "verbatim" remains checkable at the source. | Recorded; accepted |

---

## 9 · STOP

Lane L is **commit-and-STOP**. Branch `worktree-lane-l-5-fm-governance-health` is handed to the
frozen merge queue at the SHAs in §2. No merge, no push, no JOURNAL entry, no row closure, no
generated-surface regeneration.

The one thing the integrator must decide about this lane: **the Ex-ante RED**, per §0 and
candidate filing #1.
