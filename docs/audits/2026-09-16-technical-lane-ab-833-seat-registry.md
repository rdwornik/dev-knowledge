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
