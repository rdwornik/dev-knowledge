# Lane ab-833 — the seat as a registered entity

**Lane:** `lane-ab-833-seat-registry` · **Branch:** `worktree-lane-ab-833-seat-registry` ·
**Batch:** AB (`docs/audits/2026-09-16-technical-batch-ab-manifest.md`, amended by
`docs/audits/2026-09-16-technical-batch-ab-manifest-amendment-1.md`) · **Date:** 2026-09-16 (run 2026-09-17)

Consumers: [#833]

## 1 · Premise — what already computes seat liveness, measured before anything was built

**Contract identity.** `sha256` of the frozen contract read at boot
(`$CLAUDE_PROMPTS_DIR\LANE-ab-833-seat-registry.md`):
`978954e42252847ab3f4cd20244f55e8d2a4aefa5c387d1e196b333d2df03481`. That matches the pin in batch AB
manifest amendment 1's lane table, so this is the contract that was dispatched.

**Base, and it MOVED under a live seat.** The worktree was provisioned at `f8ca1d40`. At 11:17:25 +0200 a
duplicate session (see §1.4) ran `git merge --ff-only main` in this checkout, moving it to `645ec4db`
(ab-802's merge: `scripts/conductor.py`, `scripts/graph_queries.py`, `tests/test_conductor.py`,
`.github/workflows/conductor.yml`, `JOURNAL.md`, `ecosystem/doc-counts.md`, `docs/audits/README.md`, one new
audit) — between this seat's write of the row file and its manifest edit. None of the three step-1 files
were touched by it. The first step-1 commit was then refused by `audit-health` / `journal_spine_anchor` on
`33246c0a` (main's emergency hook-disable merge); the split diagnostic read `mine: [33246c0a…]`,
`main: []` — lane lag, not a gap — and a second `--ff-only main` (zero lane commits, no overlap with the
staged files) cleared it. Step 1 landed as `b7697c89` with **no hook bypassed**. That commit's pre-commit
run took **more than 600 s** on this box.

### 1.1 · The organs Done 5 names, and what each actually holds

| Organ | What it computes | Does it hold a seat's liveness? |
|---|---|---|
| `scripts/seat_refusals.py` | Seven `SeatRefusal` raisers (`REFUSALS`), a per-role audience (`SEAT_REFUSALS`: dispatcher / integrator / filings / handoff / lane), `carried-by` for decision files, `_live_worktrees` from `git worktree list` | **No.** Stateless: it refuses a seat's *acts* and never records a seat. `_live_worktrees` reads worktrees, and a worktree is not a seat — a husk and a live owner are indistinguishable there. |
| `scripts/resource_lifecycle.py` | `process_table()`, `count_seats()` (62 `claude` processes = 31 seats by an RSS split), `pid_is_alive(pid)` (query-only handle on Windows — never `os.kill`), `sample()` → `~/.claude/resource-samples.jsonl`, `session-start` hook leg | **No.** It counts processes *named* `claude` and knows neither their session id, their role, nor their batch. It does hold the one reusable liveness primitive: `pid_is_alive`. |
| `scripts/preflight_contract.py` | Locator resolution, `[#id]` liveness, `check_open_batch` (a committed manifest opens a batch) | **No — and this REFUTES a cited premise.** `[#648]`'s body says this module "computes both locator resolution and dispatcher liveness", and the contract's Done 5 names "`preflight_contract.py`'s dispatcher-liveness computation (`[#648]`)". Grepped in full: its only "liveness" is **row** liveness (`_open_backlog_ids`, line 311) and "Liveness is not identity" (line 864). There is no dispatcher-liveness computation to reuse. Recorded, not paused on: it does not refute this lane's premise (the absence of a seat registry) — it strengthens it. |
| `scripts/lane_cost.py` | `seat_session_transcripts(session_id)` — store-wide by transcript STEM; `seat_cost`, `seat-close` writes a SEAT row to `logs/LANE-COSTS.jsonl`; `seat_cost_gap` surfaces a batch with lane rows and no seat row in `[cost]` | **No.** It is the only organ that keys an attended seat by **session id** — the right key — but it prices a sitting after the fact, in committed repo state. Reused: its session-id-as-key doctrine and its transcript lookup. |
| `claude agents` / the session store | Agent View; transcripts under `~/.claude/projects/<dir>/<session>.jsonl`, appended by the RUNTIME on every turn | **Self-report: not evidence.** `[#803]` records `claude agents --json` reporting a session "busy" after its PID was dead. The TRANSCRIPT, however, is written by the harness, not by the model's prose, so its last-write time is an event timestamp. |
| heartbeat receipt ledger (`scripts/substrate_heartbeat.py`) | One receipt per substrate at `~/.claude/substrate-heartbeat.json`, schema `dev-knowledge-substrate-heartbeat/1`; `predispatch` refuses an off-machine dispatch on a stale receipt | **No** — a *substrate* is proven live, not a seat. Reused: its shape (machine-local receipt, outside the tree, schema-tagged, turned into a refusal at dispatch). |
| `scripts/lane_boot.py` | `/lane-boot`'s STEP-0 refusals (lane-name grammar, open batch committed on main) | **No** — but it is the one hub organ a lane runs BEFORE work, i.e. the dispatch-time seam. |
| `scripts/conductor.py` (re-read at `645ec4db`) | Component table lists `dispatcher-seat` and `integrator-seat` as "a SEAT (a role, not a file)", file `None` | **No** — it names the seats and has nowhere to read them from. |

**The `dispatch` verb calls no hub script.** `~/.dev-terminals/bin/dispatch.ps1` (win-tooling) contains no
`.py` / `uv run` reference; `lane_boot.py`'s own docstring already records the same limit for `[#804]`. A
refusal authored in this hub can therefore reach a seat only through something that seat runs.

**Hooks already wired** (`.claude/settings.json` at `33246c0a`): `SessionStart` → `fleet_health.py`,
`resource_lifecycle.py session-start`, and six others; `Stop` → `session_end_backpressure.py` (already parses
the hook's stdin JSON, `_read_hook_input`); `PreToolUse` → the prompts guard and the ADR-77 guard. The batch
manifest sequences **ab-808 <-> ab-833 on `.claude/settings.json`** and ab-808 has not merged, so this lane
adds no hook registration; the event writers ride hook legs that already fire.

**The runtime exposes the session id.** Measured in this seat's own shell: `CLAUDE_CODE_SESSION_ID` and
`CLAUDE_PID` are set by Claude Code. A seat can therefore bind its role against the id the runtime gave it,
rather than an id it types.

### 1.2 · Which organ becomes the registry, and why a new store is needed

**Verdict: a new append-only store, `~/.claude/seat-registry.jsonl`, written by a new module
`scripts/seat_registry.py`; the refusals join `seat_refusals.py`'s roster; the SessionStart surface is a
`fleet_health.py` digest line.** The measured reason for a new store, in one line: **no existing store
carries (session id, role, batch, event timestamp) together** — the census has no session id, the cost ledger
is committed after-the-fact money, the heartbeat receipt is per substrate, and `preflight_contract` holds no
liveness at all.

Where it lives, and why not `logs/`: the same three reasons `resource_lifecycle.SAMPLE_LEDGER_PATH` records —
a hook writes it on every session so it must never dirty the tree it reports on; the fact is about THIS
machine's processes; and an in-repo `.jsonl` under `logs/` is the route `[#785]` shows retention and
hermetization disagreeing over.

What is reused rather than rebuilt: `SeatRefusal` and the roster/CLI shape (`seat_refusals.py`);
`pid_is_alive` (`resource_lifecycle.py`); session-id keying and store-wide transcript lookup
(`lane_cost.seat_session_transcripts`); the lane-name grammar (`validate_branch_naming.validate_lane_worktree_name`,
so the registry compiles no regex of its own and does not take the `graph_queries.is_edge_computation_shape`);
the Stop hook's stdin parse (`session_end_backpressure._read_hook_input`); the fail-soft digest-line shape
(`fleet_health.cost_health_line`).

### 1.3 · The design this measurement admits

- **The field.** `state ∈ {live, wedged, absent, starved}`. An event row's `state` is set by the WRITER from
  the event kind (`SessionStart`/`Stop` → `live`, `SessionEnd` → `absent`); no API accepts a caller-supplied
  `state`, and the reader discards any row whose `state` disagrees with its event. `bind` (role + batch for
  a primary-checkout seat) carries no `state` at all.
- **Aging is read-time, over event timestamps only:** the last event is the newer of the registry's last hook
  row and the session transcript's last runtime write. Older than the threshold → `starved` if the last hook
  event was a `Stop` with nothing written since (a seat waiting for input nobody sends), otherwise `wedged`
  (a seat that went silent mid-turn). A dead `pid` or a removed lane worktree → `absent`.
- **The refusals** (dispatch time, never a commit-tier gate): `no-live-integrator` (a lane boots into a batch
  whose integrator seat is not `live`) and — accepted into scope by operator ruling 2026-09-17 — `lane-owned`
  (a second session boots onto a lane that already has a `live` owner). Wired into `lane_boot.py preflight`
  and exposed as `seat_refusals.py` verbs for the dispatcher's step 0.

### 1.4 · The witness — this lane, 2026-09-17

Nothing in the repository recorded that this lane already had an owner. This seat (`52a3764d`) was launched
at 10:47 onto a contract whose previous attempt had wedged for 12 h 43 min at SessionStart hook 9/10 (a hook
process created suspended). At 11:12 a **second** session (`506ef5c0`) was dispatched onto the same contract,
with a prompt telling it the predecessor "never started". Nothing refused the launch: no registry held
"lane ab-833 has a live seat", the worktree-exists guard cannot tell a live owner from an abandoned husk, and
`claude agents` — which listed this seat as busy — is consulted by nobody at dispatch. The duplicate found the
owner only by accident, from `git status` showing staged files written after its first clean read, then
rebuilt ownership by hand from a Win32 process scan and this seat's transcript. Before noticing, it had
already written once into this checkout (the fast-forward above), mid-step-1. **Cost:** one base shift under
a live seat, ~25 min of a duplicate Opus seat. **Near-miss:** two committing sessions on one index. Every value
the field needs was available — owner session id, role `lane`, batch `AB`, last event this seat's 11:19:36
tool call — and none of it was written anywhere a dispatcher reads. That is `[#833]` demonstrated on itself.

## 2 · What changed

| Commit | Step | What |
|---|---|---|
| `b7697c89` | 1 | `[#833]` filed: row file, manifest node under [E2]/[S3], `gen_task_tree.py --emit-source`. Four symptom rows cited as OVERLAPS, each with its uncovered leg named |
| `3a088ab7` | 2 | §1 of this artifact (the premise) |
| `eb3c9ced` | — | `git merge main` (sync): cleared `journal_spine_anchor` lane lag on `aacce0f8`; one conflict, `tasks/manifest.json`'s `generated_sha256` pin, resolved by re-pinning (`--emit-source`, `--check ok`) |
| `58ad21d2` | 3 | RED-first witnesses (§3) |
| `1b0fa936` | 4 | `scripts/seat_registry.py` — the registry |
| `f09e77fd` | 4 | `seat_refusals.py` (`no-live-integrator`, `lane-owned`), `gen_seat_boot.py` lines, `lane_boot.py` refusals 4-5, `tests/test_lane_boot.py` fixture registry |
| `c103665c` | 4 | event writers: `resource_lifecycle.py session-start` (SessionStart), `session_end_backpressure.py` (Stop) |
| `1b2db48a` | 5 | `fleet_health.py` `[seats]` line |

**Footprint:** `scripts/seat_registry.py` (new), `scripts/seat_refusals.py`, `scripts/lane_boot.py`, `scripts/gen_seat_boot.py`,
`scripts/resource_lifecycle.py`, `scripts/session_end_backpressure.py`, `scripts/fleet_health.py`, `tests/test_seat_registry.py` (new),
`tests/test_seat_refusals.py`, `tests/test_lane_boot.py`, `tasks/833-*.md`, `tasks/manifest.json`, `BACKLOG.md`, this file. **Not touched:**
`.claude/settings.json` (sequenced behind ab-808, unmerged), `JOURNAL.md`, any generated index.

## 3 · RED-first, then green

**RED, recorded run on `58ad21d2`'s tree before any build code** (`-n 0`, targeted files only):
`12 failed, 92 passed, 1 error` — every new witness in `tests/test_seat_refusals.py` (8, plus the widened whole-roster assertion) and
`tests/test_lane_boot.py` (3) failed on `ModuleNotFoundError: seat_registry` / `no attribute 'seat_preflight'` / the roster tuple; all
23 of `tests/test_seat_registry.py` failed at collection on `No module named 'seat_registry'`; the 92 pre-existing tests stayed green.
The RED commit also landed (`58ad21d2`) — possible here because the row already named the test paths, and because by then main's
`6e9f0bb8` had moved the graph gates off the local commit tier.

**Green, targeted** (never the full suite on this workstation):

| Run | Files | Result |
|---|---|---|
| after `f09e77fd` | `test_seat_registry`, `test_seat_refusals`, `test_lane_boot`, `test_gen_seat_boot`, `test_seat_split`, `test_seat_ch8` | 194 passed |
| after `c103665c` | `test_seat_registry`, `test_resource_lifecycle`, `test_session_end_backpressure` | 96 passed |
| step 5 | `test_seat_registry`, `test_fleet_health` | 225 passed |
| adjacent | `test_prompts_guard_hook_wiring`, `test_fleet_parity`, `test_lane_cost`, `test_seat_cost` | no failure in the last three; **every** failure is in `test_prompts_guard_hook_wiring.py` ("expected exactly one prompts-guard hook, found 0") — **attributed to main, not this lane:** main's `33246c0a` (emergency disable of all PreToolUse hooks) removed that hook block from `.claude/settings.json`, and this lane's diff does not touch `settings.json` (`git diff --name-only main...HEAD -- .claude/settings.json` is empty) |

`ruff check` clean on every touched file before each commit — run by hand, because since `6e9f0bb8` ruff is a conductor job, not a
local hook. After every run `~/.claude/seat-registry.jsonl` did **not** exist: no test wrote the real registry.

**The two properties the contract names, and the test that pins each:**
- *a model-authored write is refused* — `test_a_model_authored_state_write_is_refused` (write-time, leaves no file),
  `test_a_hand_appended_row_whose_state_disagrees_with_its_event_is_discarded` (read-time, the half that makes the first one real),
  `test_no_verb_accepts_a_state`, `test_the_session_start_leg_refuses_a_payload_that_asserts_its_own_state`.
- *refusal cannot pass by refusing everything* — each trip-test has a passing path: `test_a_live_integrator_for_the_batch_admits_the_lane`,
  `test_the_owner_itself_is_not_refused_by_its_own_seat`, `test_a_relaunch_over_a_wedged_owner_is_admitted`,
  `test_an_owner_of_a_different_lane_does_not_refuse`, `test_lane_boot_admits_a_lane_with_a_live_integrator_and_no_other_owner`, and the
  pre-existing `test_lane_boot_admits_a_batch_whose_manifest_is_committed_on_main` (now with a fixture registry).

## 4 · Done-contract, item by item

| Done | Discharged by |
|---|---|
| 1 row filed, symptom rows cited | `b7697c89`. `[#648]` `[#805]` `[#808]` `[#682]` each OVERLAPS with the uncovered leg named; none superseded (none has its Done-when fully covered), none closed |
| 2 one registry, one field, event-written, model write refused | `seat_registry.py`: `SCHEMA`, `ROLES`, `STATES`, `EVENT_STATE`; `record_event` refuses `model-authored-state` / `not-an-event`; `_valid` discards forged rows; `bind` has no state |
| 3 no-live-integrator refusal, RED + passing path | `seat_refusals.refuse_no_live_integrator`, wired in `lane_boot.py preflight` (refusal 5) and three seat boots. **Widened by operator ruling 2026-09-17:** `refuse_lane_owned` (refusal 4) |
| 4 self-surfacing at SessionStart, threshold with provenance | `fleet_health.py` `[seats]` line → `seat_registry.seat_health_line`; `WEDGED_AFTER_MIN`, `STARVED_AFTER_MIN`, `SURFACE_LOOKBACK_HOURS` each in `THRESHOLD_PROVENANCE` |
| 5 library-first, named | §1.2 — a new store, with the one-line measured reason; what was reused is listed there |
| 6 nothing rests on allow/ask | both refusals are exit 1 from a command the seat runs; the write refusal is code. No permission rule was added or relied on |
| 7 targeted pytest green, no new commit-tier gate | §3; no `.pre-commit-config.yaml` change |

## 5 · Measurements taken on the way

- **Commit-gate wall time on this box, 2026-09-17:** step 1 and step 2 commits each spent **more than 600 s** in pre-commit (step 2
  observed at `decision_coverage.py check` alone for ~490 s). After main's `6e9f0bb8` stripped the local gate, the step 3-5 commits
  took seconds.
- **Hung hook processes, observed live at ~12:40 +0200** in a `Win32_Process` scan while waiting on a commit: four
  `fleet_health.py --prompts-guard` (PreToolUse) processes aged **~7,800 s (2 h 10 min)**, one `session_end_backpressure.py` (Stop) at
  **4,759 s**, one `conductor.py session-start` at **4,045 s** — all from other sessions. Not killed (not this lane's). This is `[#808]`'s
  class in the field, and it is also this row's: none of those sessions was visible as wedged to anyone.
- **Base shifts under a live seat: three.** `f8ca1d40 → 645ec4db` (the duplicate session's fast-forward, §1.4), `645ec4db → 33246c0a`
  (`--ff-only` to clear lane lag), `3a088ab7 → eb3c9ced` (sync merge to clear lane lag on `aacce0f8`). Each spine-anchor block was
  diagnosed with the split predicate (`mine` vs `main` JOURNAL), never a grep; each read `main: []`; no hook was bypassed for it.
- **Edge-computation ratchet (operator warning, 2026-09-17): did not apply, and no workaround was taken.** Checked with
  `graph_queries.is_edge_computation_shape` directly, since that gate now runs in the conductor: `seat_registry.py` → `False` (no `re`
  call, no `ast`); `seat_refusals`, `fleet_health`, `session_end_backpressure`, `gen_seat_boot` → `True` at base `33246c0a` and `True`
  after — no module changed shape; `lane_boot`, `resource_lifecycle` → `False` both. No `EDGE_COMPUTATIONS` entry was needed, so the
  dict ab-802 grew is untouched here.

## 6 · Honest limits and open items

- **The dispatch verb still calls no hub script.** `lane-owned` and `no-live-integrator` reach a seat only through `/lane-boot`
  (`lane_boot.py preflight`) or a rendered seat boot. A seat that types `dispatch` and nothing else is not refused — the exact path the
  2026-09-17 duplicate took. → To file (1).
- **A forged EVENT is not refused.** A process piping a well-formed hook payload into `record_event` writes an event; the refusal stops a
  seat asserting a state, not forging the event that implies one.
- **No heartbeat between SessionStart and Stop** other than the harness-written transcript's mtime, which moves when a tool call
  returns. One call longer than `WEDGED_AFTER_MIN`, or a seat supervising a background agent that long, reads wedged. `UserPromptSubmit`
  and `SessionEnd` are in `EVENT_STATE` but nothing registers them yet. → To file (2).
- **The integrator must bind.** Until an integrator runs `seat_registry.py bind --role integrator --batch <B>` from its own session,
  `no-live-integrator` refuses every lane of that batch — by design, and the refusal names the command, but the `/lane-integrate`
  command file does not carry it yet. → To file (3).
- **A `browser` seat has no event surface**; it can be bound and reads `absent`.
- **`STARVED_AFTER_MIN` is chosen, not derived**, and says so. The registry is never compacted.
- **Correction to §1.2 (premise, as committed at `3a088ab7`):** it lists `lane_cost.seat_session_transcripts`'s store-wide transcript
  lookup as reused. The build does **not** use it: every hook payload already carries `transcript_path`, so the registry records the
  path at the event and reads one file's mtime, where the store-wide walk would grow with history on every SessionStart. What is
  kept from `lane_cost` is the doctrine only — a seat is keyed by session id, never by directory.
- **Refuted premise carried forward:** `[#648]`'s body says `preflight_contract.py` computes dispatcher liveness; it does not (§1.1).

## To file

Ids for these come from this lane's block (851-854, batch AB manifest amendment 1 §3) via `id_allocator.py allocate` at filing time; none
was allocated by this lane.

1. **The `dispatch` verb runs the seat refusals before it launches** (win-tooling `scripts/dispatch/Invoke-Dispatch.ps1`): call
   `lane_boot.py preflight --lane <worktree name>` (which now carries `lane-owned` and `no-live-integrator`) as its first act, and refuse
   on exit 1. Out of this hub's footprint. Witness: the 2026-09-17 duplicate dispatch onto lane ab-833 (§1.4).
2. **Register the missing seat events once ab-808 merges** (`.claude/settings.json`): `UserPromptSubmit` (so a starved seat reads live
   the moment it is fed, not at its next Stop) and `SessionEnd` (so `absent` is an event, not only a dead pid). Both already map in
   `seat_registry.EVENT_STATE`; each hook must carry the bound ab-808 establishes.
3. **`/lane-integrate` binds its seat**: `.claude/commands/lane-integrate.md` gains `seat_registry.py bind --role integrator --batch <B>`
   followed by `seat_refusals.py no-live-integrator --batch <B>` as its opening lines, so the integrator's receiving state is written at
   boot rather than discovered by the first refused lane.
4. **Correct `[#648]`'s claim** that `preflight_contract.py` computes dispatcher liveness (it computes row liveness only), and narrow its
   dispatcher-liveness half against `[#833]`'s refusals.
5. **Derive `STARVED_AFTER_MIN`** from the registry's own Stop → next-event gaps once it holds a week of history, and rewrite its provenance.