# Night-3 research — the 1431 s integration suite, CLI-scriptable dispatch/harvest, and the pre-commit hook stack

> **EXTERNAL EVIDENCE — advisory until ratified, never doctrine by virtue of existing.**
> **STATUS: DRAFT.** This document decides nothing, adopts nothing, and births no BACKLOG row.
> No config file, dependency, hook or protocol was edited by the lane that produced it.

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-15 · **Slug:** night3-research
- **Lane:** `claude/night3-research-perf-m2a3lp` (Anthropic cloud session, Linux container), night3-D research lane
- **Base:** `main` @ `65dc318` (the merged phase-1 tree) · working tree clean before and after
- **Model:** Opus 5 · web search permitted · **no adoption, no config edits — evidence only**
- **Answers three bounded questions.** Each carries: recommended approach · current version ·
  Windows/uv compatibility · minimal integration sketch · do-not-adopt alternatives with the
  one-line reason.

---

## 0. Method, and the honest limits of it

**Library-first ladder applied as stated:** stdlib > established dependency > stabilized project >
industry pattern. All three answers land on the **top rung** — Q1 needs no new library at all,
Q3's fix is one `functools` decorator, and Q2's sketches are `subprocess` + `json` + `argparse`.
Where that looks too easy, §1–§3 give the measured reason.

**What is first-party here.** Every number below was measured in this container, on this tree,
tonight. Three full suite runs (485 s, 957 s, and a third with a proposed patch), a 10-commit
gated-commit sample run twice, a `cProfile` of the dominant hook, a byte-diff of that hook's
output before and after a proposed fix, and six live `claude` CLI probes. **The CLI section was
written from `claude --help` and from running the commands** — not from recollection, and §2.1
records two places where the help text and the live binary disagree.

**Five limits, stated up front because each bounds a claim:**

1. **This lane runs on Linux; the integrator ran on Windows.** That difference turns out to be
   the *answer* to Q1 rather than a caveat to it (§1.3), but it means no number here is a
   substitute for the host figure — it is the controlled comparison against it.
2. **This container's failure set is not the integrator's.** They saw 1 failure; this container
   sees 28, from absent fleet siblings and a PowerShell-only hook set (§1.5). The A-vs-B
   comparison is still sound because **both runs carry the identical failure set** — only the
   absolute is non-transferable.
3. **The Q3 fix was measured by runtime monkey-patch, never by editing the tree.** `journal_anchor.py`
   is byte-unchanged. That proves the saving and the output-identity; it does not prove the patch
   survives review as source.
4. **The clone arrived shallow and this lane unshallowed it** (§3.4). That is the one deliberate
   state change made to the container, it is disclosed rather than implied, and it *raised* the
   measured hook cost 4.5× rather than flattering it.
5. **Scratch hygiene (core-invariant #9):** two scratch branches, one probe file, and one
   dispatched background agent were created and **removal was verified** — `git status` clean,
   `HEAD` and tree SHA identical before and after, `background agents left: 0` (§4).

---

## 1. Q1 — why the integration suite took 1431 s

### 1.1 The premise is false, and that is the finding

The question asks whether the integrator's one full run used xdist, and if not, to name the
invocation that would. **It did use xdist.** There is no missing flag to add.

`pyproject.toml:140` sets, in `[tool.pytest.ini_options]`:

```
addopts = "-n auto"
```

adopted 2026-08-06 on a measured 5.2× (the comment block at `:131-137` carries the evidence).
The integrator's invocation — `uv run --locked pytest -q`, prescribed by
`.claude/commands/lane-integrate.md:37,59` — therefore **inherits `-n auto`**. That is not an
inference from the config; it is visible in this lane's own run of the identical command:

```
=== RUN A: the integrator's exact invocation (inherits addopts -n auto) ===
bringing up nodes...
```

`bringing up nodes...` is xdist's worker-pool banner. The bare command is parallel.

**Consequence for the row:** `[#528]` leg 1's Done-when — *"gate-run call sites use `-n auto
--dist worksteal` (or a recorded reason one does not)"* — is **already half-satisfied everywhere
by inheritance**. What lane N's leg 1 actually added at `.claude/skills/verify/verify.py:24` is
the *other* two flags, and its own source comment says so in as many words: *"`-n auto` is already
the `addopts` default … so repeating it changes nothing today."*

### 1.2 The three runs

All on `main` @ `65dc318`, 2960 tests collected, this container (4 vCPU, 15 GB), Python 3.12.10,
pytest-xdist 3.8.0, uv 0.11.19.

| run | invocation | wall | outcome |
|---|---|---|---|
| **A** | `uv run --locked pytest -q` (= `-n auto`, 4 workers) | **485.55 s** | 28 failed · 2924 passed · 7 skipped · 1 xfailed |
| **B** | `uv run --locked pytest -q -n 0` (forced serial) | **956.68 s** | 28 failed · 2924 passed · 7 skipped · 1 xfailed |

**Ratio 1.97×, and the failure sets are identical term for term** — so the parallel path is not
buying speed by skipping or destabilizing anything. This reproduces night-2's 1.48× on a bigger
tree rather than contradicting it; the gap between 1.97× and the 5.2× of 2026-08-06 is explained
entirely by §1.4.

### 1.3 Where the 1431 s actually went — a host penalty, not a serial run

Line the four known measurements up on one axis. Every one of them is `-n auto`:

| tree | machine | tests | wall | source |
|---|---|---|---|---|
| pre-batch | cloud container | ~2897 | 473.02 s | night-2 latency audit `8387ff2a` §2 |
| pre-batch | **operator host** | 2897 | **918.90 s** | `JOURNAL.md` 2026-08-15 (a), `:215` |
| merged | cloud container | 2960 | **485.55 s** | **run A, this lane** |
| merged | **operator host** | 2960 | **1431.73 s** | phase-1 packet §2 |

Two facts fall straight out:

1. **The batch cost +12.53 s in the container and +512.83 s on the host.** Same 63 new tests, same
   invocation — a **41× difference in the increment**. The added tests are the three new files
   (`test_single_flight.py`, `test_block_commit_on_main.py`, `test_telemetry_emit.py`, 1143 lines,
   33 of the tests spawning real `git` subprocesses against real temporary repos). Subprocess spawn
   is the single most expensive primitive on Windows and one of the cheapest on Linux. The batch
   did not add slow tests; it added *Windows*-slow tests.
2. **Host ÷ container, identical tree and invocation, is 2.95×** (1431.73 / 485.55) — up from 1.94×
   on the pre-batch tree. The penalty is not constant; it grew with the batch, exactly as (1) predicts.

**So the 1431 s decomposes as: ~486 s of work, multiplied by a ~2.95× host factor.** Not a serial run.

### 1.4 The floor no invocation can cross

Run A's slowest durations:

```
269.73s  tests/test_safe_remove.py::test_real_oracle_blocks_real_cross_module_removal
 65.63s  tests/test_reverse_dep_oracle.py::test_finding_headline_resolves_with_provenance
 65.63s  tests/test_reverse_dep_oracle.py::test_main_finding_json_exit_zero
 48.82s  tests/test_writer_integrity.py::test_live_registry_has_no_unconditionally_inert_check_left
 47.70s  tests/test_audit.py::test_health_stays_ok_with_na_status
 47.41s  tests/test_audit.py::test_health_degraded_no_ecosystem
 46.19s  tests/test_audit.py::test_health_ok_with_registered_repo
 46.10s  tests/test_hub_identity.py::test_no_hub_only_check_skips_when_the_stored_path_is_stale
 42.14s  tests/test_membership_agreement.py::test_declaration_leg_works_under_package_mode_invocation
```

**One test is 269.73 s — 55.6 % of the entire parallel wall.** Night-2 measured the same test at
268.74 s, so it is stable, not noise. xdist distributes whole tests, so **269.73 s is a hard floor**:
adding workers, changing schedulers, or buying more cores cannot go below it. That single test is
why the measured speedup is 1.97× and not 5.2× — the suite has an Amdahl ceiling of
485.55 / 269.73 ≈ 1.8× further improvement, and only if everything else became free.

**The second tier is the interesting one.** Six of the next eight entries (48.82, 47.70, 47.41,
46.19, 46.10, 42.14 — ~278 s of test time) are tests that invoke `audit.cmd_health` in-process via
`CliRunner`. That is the *same* function §3 profiles, and the same 25 s of avoidable work is
being paid **once per test**. Whether removing it also shortens the *suite* is a separate question
from whether it removes work — §3.5 measures both, and the two answers differ.

### 1.5 Why this container shows 28 failures and the host showed 1

Recorded so the run is auditable rather than quietly discounted. The container lacks
`/home/user/ai-council` and `/home/user/corp-monorepo`, so `audit.py health` reports
`[!!] repos registered  (none)` and every test asserting a healthy fleet surface fails. The
`SessionStart` hooks are PowerShell (`powershell: not found`, witnessed in §2.1's probe). None of
this is repo state, and none of it differs between runs A and B — which is the property that makes
the A/B ratio usable.

### 1.6 Recommendation, with the reason a change could be wrong

**Recommendation: change nothing about the invocation, and do not chase the 1431 s.** It is a
correct measurement of a Windows host running an already-parallel suite. The two levers that
*would* pay, in order of value:

1. **The 269.73 s test** — the only change that moves the floor. Out of scope tonight; it needs its
   own row, and it is a correctness-sensitive test (a real language-server oracle), so it is not a
   candidate for casual speed work.
2. **`--dist worksteal --max-worker-restart=0`** on the integration call site.
   `.claude/skills/verify/verify.py:24` already carries them after lane N's leg 1;
   **`.claude/commands/lane-integrate.md:37,59` still reads bare `uv run --locked pytest -q`**, so
   the one run that most needs a rebalancing scheduler is the one that does not ask for it. Night-2
   attributed ~204 s of a 473 s parallel wall to two heavy files landing on one worker.

**The recorded reason `--max-worker-restart=0` must not be adopted casually:** xdist's default
restart budget is `numprocesses × 4`, and setting it to 0 converts a crashed worker from a silent
replacement into a hard suite failure. That is *correct for a gate* and is precisely why lane N
took it — but it changes failure semantics, so it belongs in the same act that updates the
integrator's runbook, not as a drive-by.

**Do not adopt:** `-p no:xdist` to force serial (unloads the `-n` option `addopts` supplies →
`unrecognized arguments: -n`, exit 4 before collection; `pyproject.toml:83-91` already records this
costing a whole mutation pilot). `--dist loadfile`/`loadgroup` here (they *reduce* spread; the
problem is one oversized test, not cross-test coupling). Raising `-n` above `auto` (the floor test
is single-threaded; extra workers add memory pressure against real git repos for no wall gain).

---

## 2. Q2 — dispatch/harvest automation for the Cloud Agents SDK loop

### 2.1 What the installed CLI actually does — probed, not assumed

Installed: **`claude` 2.1.233**. Everything below was executed in this container tonight.
**Two of these contradict what a reasonable reading of `--help` would predict**, which is exactly
why the question asked for the real surface.

| capability | verified command | result |
|---|---|---|
| dispatch background | `claude --bg --model haiku "<prompt>"` | **exit 0**; prints `backgrounded · d58afcea` |
| **`--bg` REFUSES `--session-id`** | `claude --bg --session-id <uuid> …` | `warning: --bg manages the session id; ignoring --session-id` — **the dispatcher cannot choose the id** |
| board listing | `claude agents --json` | JSON array, exit 0, **no TTY required** |
| completed sessions | `claude agents --json --all` | same, includes finished background rows |
| **completion signal** | (background row) | `"status": "idle", "state": "done"` |
| **`logs` is not parseable** | `claude logs d58afcea` | exit 0 but emits a **raw ANSI/TUI screen replay** (`[?1049h`, cursor moves, spinner frames) |
| undocumented subcommands | `claude attach\|logs\|stop <id>` | all real; **none appears in `--help`'s `Commands:` list** |
| structured print | `claude -p --output-format json` | single JSON object; **exit 1** when `is_error` |
| structured schema | `--json-schema '<schema>'` | validates the printed result |
| budget cap | `--max-budget-usd` | **`--print` only** — *not* available to `--bg` |

A background row, verbatim:

```json
{ "pid": 11151, "id": "d58afcea", "cwd": "/home/user/dev-knowledge",
  "kind": "background", "startedAt": 1786832495380,
  "sessionId": "d58afcea-0027-4874-a88c-c0ff9f4e3daf",
  "name": "probe night cli-shape", "status": "idle", "state": "done" }
```

and the `-p --output-format json` envelope carries `is_error`, `subtype`, `session_id`,
`total_cost_usd`, `usage`, `modelUsage`, `permission_denials`, `errors`.

**Three design consequences, each forced by a probe rather than chosen:**

1. **Correlation must be by short id captured at dispatch, not by a pre-chosen UUID.** `--bg`
   overrides `--session-id`. The dispatcher parses `backgrounded · <id>` from stdout and persists it.
2. **Harvest must read the repo, not the transcript.** `claude logs` is a terminal replay; parsing
   it would be scraping ANSI frames. The repo already solves this — `STANDING_RULINGS` **I-D3**
   commits the contract before dispatch and each lane commits its packet — so **packet fetch is a
   `git` operation with no CLI in the path at all.**
3. **The board is pollable and machine-readable.** `state == "done"` is the completion predicate;
   `claude agents --json --all` is the poll. No webhook or callback exists — polling is the
   only mechanism, and that is a property to design around, not a gap to route around.

**One live observation that sits against recorded doctrine, reported rather than resolved.**
`PLAYBOOK` Ch8 (AM-5, operator-ratified 2026-08-11) records that a session spawned from inside
another session *"does not surface as its own Agent View row"*. This lane's `--bg` probe was
dispatched from inside a session and **did** surface as a `kind: "background"` row. This is a
Linux container on CLI 2.1.233, not the operator's host, and one observation is not a refutation —
but the doctrine rests on a property that did not hold here, and that is worth a deliberate
re-witness before anything is built on either reading. **It changes nothing in the sketches below**,
which keep the operator-at-a-terminal shape regardless (§2.2).

### 2.2 What is scriptable today, and what is not

**Scriptable now:** dispatch (`claude --bg`, exit code + id on stdout) · board watch
(`claude agents --json --all`, `state == "done"`) · packet fetch (pure `git fetch` + read a
committed path) · harvest verdict (`claude -p --output-format json --json-schema`, exit 0/1).

**Not scriptable today, stated plainly:** no completion callback (poll only) · no per-agent budget
cap on `--bg` (`--max-budget-usd` is `--print`-only) · no machine-readable per-session transcript
(`logs` is ANSI) · no exit status for the *work* in `agents --json` — `state: "done"` says the
session ended, **not that it succeeded**. The success predicate must come from the repo: did the
lane commit its packet, and does the tree pass its gates.

**The AM-5 shape is preserved by construction.** Both scripts are **operator-run from a terminal**.
A Python process is not a Claude session, so the agents it spawns are top-level dispatches — the
same object the operator would have typed by hand, with the same Agent View visibility. Neither
script may be invoked from inside a lane session.

### 2.3 `dispatch_batch.py` — PROPOSAL (single-flight woven in at dispatch)

Stdlib only (`argparse`, `json`, `pathlib`, `re`, `subprocess`, `shutil`). Windows-safe: no
`shell=True`, list-form argv, `shutil.which("claude")` resolves `claude.cmd`, `pathlib` throughout.

```python
#!/usr/bin/env python
"""PROPOSAL — operator-run from a terminal. Never invoke from inside a lane session (AM-5)."""
import argparse, json, re, shutil, subprocess, sys
from pathlib import Path

CLAUDE = shutil.which("claude") or sys.exit("claude not on PATH")
BACKGROUNDED = re.compile(r"backgrounded\s*[·|]\s*(\w+)")   # `backgrounded · d58afcea`

def claim(contract_id: str, repo: Path) -> int:
    """[#530] single-flight. 0 claimed · 3 already in flight · 2 internal error (fail closed)."""
    return subprocess.run(
        [sys.executable, "scripts/single_flight.py", "claim", contract_id],
        cwd=repo).returncode

def dispatch(lane: dict, repo: Path) -> dict:
    contract_id = lane["contract_id"]
    rc = claim(contract_id, repo)
    if rc == 3:
        return {**lane, "dispatched": False, "reason": "already in flight (single-flight refused)"}
    if rc != 0:
        # 2 = internal error. Fail CLOSED: an unknown lock state is not a free one.
        return {**lane, "dispatched": False, "reason": f"single_flight claim error rc={rc}"}

    # The board label opens the prompt (PLAYBOOK Ch8) -- it becomes the Agent View row `name`.
    prompt = f"[{lane['repo']} · {lane['id']} · {lane['verb']}] Execute the frozen contract at {lane['contract_path']}"
    argv = [CLAUDE, "--bg", "--worktree", lane["worktree"],
            "--model", lane["model"], "--effort", lane["effort"],
            "--permission-mode", lane.get("permission_mode", "acceptEdits"), prompt]
    r = subprocess.run(argv, cwd=repo, capture_output=True, text=True)
    m = BACKGROUNDED.search(r.stdout)
    if r.returncode != 0 or not m:
        # The claim is now held by a lane that never started -- release it or it wedges the id.
        subprocess.run([sys.executable, "scripts/single_flight.py", "release", contract_id], cwd=repo)
        return {**lane, "dispatched": False, "reason": f"dispatch failed rc={r.returncode}: {r.stdout.strip()}"}
    return {**lane, "dispatched": True, "agent_id": m.group(1)}   # NOT --session-id: --bg overrides it

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("manifest", type=Path, help="the COMMITTED batch manifest (I-D3)")
    p.add_argument("--repo", type=Path, default=Path("."))
    p.add_argument("--ledger", type=Path, default=Path("logs/DISPATCH-LEDGER.jsonl"))
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()

    lanes = json.loads(a.manifest.read_text(encoding="utf-8"))["lanes"]
    if a.dry_run:
        print(json.dumps(lanes, indent=2)); return 0
    rows = [dispatch(l, a.repo) for l in lanes]
    with a.ledger.open("a", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row) + "\n")
    for row in rows:                                     # the operator reads this, not the ledger
        print(f"{'OK ' if row['dispatched'] else 'SKIP'} {row['id']:<8} "
              f"{row.get('agent_id', row.get('reason'))}")
    return 0 if all(r["dispatched"] for r in rows) else 1
main() if __name__ == "__main__" else None
```

**Why the single-flight call sits exactly there.** `[#530]`'s guard arbitrates on `origin`, so it
is the one check that works across worktrees *and* across machines — the collision witnessed
2026-08-14 was cross-machine. Placing `claim` **before** the spawn is what makes it a guard;
placing it after would make it a log. The `release`-on-failed-spawn path is the non-obvious half:
a claim held by a lane that never started wedges that contract id until someone releases it by hand.

### 2.4 `harvest_batch.py` — PROPOSAL (board watch → packet fetch → harvest prompt)

```python
#!/usr/bin/env python
"""PROPOSAL — poll the board, then harvest from the REPO (never from `claude logs`: it is ANSI)."""
import argparse, json, subprocess, sys, time
from pathlib import Path

def board(cwd: Path) -> list[dict]:
    r = subprocess.run(["claude", "agents", "--json", "--all", "--cwd", str(cwd)],
                       capture_output=True, text=True)
    return json.loads(r.stdout) if r.returncode == 0 else []

def wait(agent_ids: set[str], cwd: Path, poll: int, timeout: int) -> dict[str, str]:
    """`state == 'done'` means the SESSION ended -- not that the work succeeded (§2.2)."""
    deadline, seen = time.monotonic() + timeout, {}
    while time.monotonic() < deadline:
        for row in board(cwd):
            if row.get("id") in agent_ids and row.get("state") == "done":
                seen[row["id"]] = row.get("status", "unknown")
        if agent_ids <= seen.keys():
            return seen
        time.sleep(poll)
    return seen                                   # partial: caller reports the stragglers

def packet(lane: dict, repo: Path) -> tuple[bool, str]:
    """The REAL success predicate: did the lane commit its packet on its branch?"""
    subprocess.run(["git", "fetch", "origin", lane["branch"]], cwd=repo, capture_output=True)
    r = subprocess.run(["git", "show", f"origin/{lane['branch']}:{lane['packet_path']}"],
                       cwd=repo, capture_output=True, text=True)
    return r.returncode == 0, r.stdout

def harvest(packets: dict[str, str], repo: Path) -> dict:
    schema = json.dumps({"type": "object", "required": ["lane_verdicts"], "properties": {
        "lane_verdicts": {"type": "array", "items": {"type": "object",
            "required": ["lane", "outcome", "evidence"], "properties": {
                "lane": {"type": "string"},
                "outcome": {"enum": ["clean", "deviation", "blocked"]},
                "evidence": {"type": "string"}}}}}})
    prompt = ("Read each lane packet below. For each, return outcome + the ONE line of evidence "
              "that justifies it. Do not infer beyond the packet text.\n\n" +
              "\n\n".join(f"=== {k} ===\n{v}" for k, v in packets.items()))
    r = subprocess.run(["claude", "-p", "--output-format", "json", "--json-schema", schema, prompt],
                       cwd=repo, capture_output=True, text=True)
    env = json.loads(r.stdout)                    # exit 1 iff is_error (§2.1)
    return {"ok": r.returncode == 0 and not env.get("is_error"),
            "cost_usd": env.get("total_cost_usd"), "result": env.get("result")}

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("ledger", type=Path); p.add_argument("--repo", type=Path, default=Path("."))
    p.add_argument("--poll", type=int, default=30); p.add_argument("--timeout", type=int, default=7200)
    a = p.parse_args()
    lanes = [json.loads(l) for l in a.ledger.read_text().splitlines() if l.strip()]
    lanes = [l for l in lanes if l.get("dispatched")]
    done = wait({l["agent_id"] for l in lanes}, a.repo, a.poll, a.timeout)

    packets, missing = {}, []
    for l in lanes:
        ok, text = packet(l, a.repo)
        (packets.__setitem__(l["id"], text) if ok else missing.append(l["id"]))
    for l in lanes:
        if l["agent_id"] not in done:
            print(f"STRAGGLER {l['id']} -- session never reported done", file=sys.stderr)
    for m in missing:
        print(f"NO PACKET  {m} -- session ended without committing its packet", file=sys.stderr)
    print(json.dumps(harvest(packets, a.repo), indent=2))
    return 0 if packets and not missing and len(done) == len(lanes) else 1
main() if __name__ == "__main__" else None
```

**Note what the exit code keys on:** every lane reported `done` **and** every lane's packet exists.
A session that ends without a packet is the failure mode the board cannot see, and it is reported
by name rather than folded into a pass.

### 2.5 Recommendation

**Recommendation: build `harvest_batch.py` first, and treat `dispatch_batch.py` as optional.**
Harvest is where tonight's manual cycle actually costs — board watching is polling a JSON array a
human is currently reading by eye, and packet fetch is `git show` a human is currently doing by
hand. Both are fully determined, both are stdlib, and neither needs a doctrine change. Dispatch
is *already* one short command per lane and is governed by AM-5; automating it buys less and
touches a ratified operator boundary.

**Version/fit:** `claude` 2.1.233 · Python 3.12 stdlib only · **Windows-safe as sketched**
(`shutil.which`, list-form argv, no `shell=True`, `pathlib`) · no `uv` dependency change — both
scripts run under the existing locked environment.

**Do not adopt:** parsing `claude logs` (ANSI screen replay — §2.1) · pre-allocating `--session-id`
for correlation (`--bg` overrides it) · a job queue such as Celery/RQ (a broker and a daemon to
watch ≤10 processes the CLI already tracks) · `--max-budget-usd` as a lane guard (`--print`-only) ·
inferring lane success from `state: "done"` (it reports session end, not outcome).

---

## 3. Q3 — pre-commit hook runtime cost

### 3.1 The 10-commit sample

Hooks armed via `pre-commit install` (pre-commit 4.6.1; all three stages per
`default_install_hook_types`). Ten real gated commits on a scratch branch, one small file staged
each time:

```
commit  1  42.60s     commit  6  45.36s
commit  2  42.32s     commit  7  42.68s
commit  3  42.15s     commit  8  42.86s
commit  4  42.89s     commit  9  42.69s
commit  5  42.96s     commit 10  42.82s
```

**Median 42.75 s per commit.** Spread is 3.2 s across ten samples — this is a stable cost, not noise.

### 3.2 The slowest hook, isolated

A second 10-commit sample with `SKIP=audit-health` — commits that **succeed**, so this figure
includes the `commit-msg` stage that a blocked commit never reaches:

```
0.65 0.63 0.63 0.62 0.62 0.63 0.64 0.62 0.63 0.63   -> 0.63 s
```

Per-hook, N=5, direct invocation:

```
block_commit_on_main        0.05 0.05 0.05 0.05 0.05
validate_hermetization      0.05 0.05 0.05 0.05 0.06
check_backlog_commit_msg    0.05 0.04 0.04 0.04 0.04
check_backlog_filing        0.05 0.04 0.04 0.04 0.04
audit.py health            42.08 42.30 42.46 42.20 42.46
gen_audit_index --check     0.12 0.13 0.12
generate_organ_index --check 0.16 0.14 0.14
gen_claude_rosters --check  0.07 0.06 0.07
gen_intake_index --check    0.09 0.09 0.09
gen_methodology_roster --check 0.11 0.10 0.10
```

**`audit-health` is 42.2 s of a 42.75 s commit — 98.5 % of the entire per-commit cost.**
Everything else in the stack, all thirteen other hooks combined including both `commit-msg`
hooks, costs **0.63 s**. There is no second candidate.

**A live doc-claim defect, surfaced by the measurement.** `.pre-commit-config.yaml` documents this
hook as *"~1.4 s"*, and `CLAUDE.md` §9 repeats the roster row without a figure. The measured cost
is **30× the documented one**. Recorded here as evidence; no file was edited by this lane.

*(An earlier identical sample measured 9.6 s per commit — before §3.4's unshallow. Reported in
§3.4 rather than buried, because the difference is itself a finding.)*

### 3.3 The root cause, and the cheapest 2× win

`cProfile` over `audit.cmd_health` (51.53 s under the profiler; proportions are what carry):

```
   1    31.170  scripts/audit.py:3859(check_journal_spine_anchor)
 159    30.009  scripts/journal_anchor.py:219(mention_not_record_warnings)
 737    24.994  scripts/journal_anchor.py:214(_entries)
 794    24.520  {method 'split' of 're.Pattern' objects}      <-- 47% of the whole run
```

The mechanism, at `scripts/journal_anchor.py:219-236`:

```python
def mention_not_record_warnings(repo, sha, journal):
    for c in introduced(repo, sha):          # once per introduced commit
        for entry in _entries(journal):      # <-- re-splits the WHOLE journal, every iteration
```

`_entries` (`:214`) runs `re.split(r"(?=^### )", journal, MULTILINE)` over **`JOURNAL.md`, which is
2,594,581 bytes**. It is loop-invariant — `journal` never changes inside the loop — yet it is
recomputed 737 times across 159 calls. **794 splits × ~31 ms = 24.5 s of pure repeated work.**

**The fix is one stdlib line** — top rung of the ladder, no dependency, no Windows surface:

```python
@functools.lru_cache(maxsize=1)     # `journal` is a str: hashable, and one entry is all that is used
def _entries(journal: str) -> list[str]:
    return [p for p in _ENTRY_SPLIT_RE.split(journal) if p.strip()]
```

*(Hoisting the call out of the loop is the equivalent local fix and needs no decorator; it cuts
737 splits to 159. The cache cuts them to **1**, which is why it is the one measured below.)*

**Measured, by runtime monkey-patch, with the tree byte-unchanged:**

| | wall | findings |
|---|---|---|
| baseline | **42.68 s** | 86 lines |
| `lru_cache` on `_entries` | **17.14 s** | 86 lines |

**2.49× on the hook; 42.75 s → ~17.8 s per commit, a 2.4× win on the whole gated-commit cost.**
And the output is **byte-identical** — a `diff` of the two full finding sets is empty but for the
wall-time line the harness itself printed. Faster *and* the same verdict; three repeats gave
17.15 / 17.45 / 17.45 s.

The second-largest contributor, for whoever takes this further, is `check_doc_code_edge` at 9.77 s
(tokenize-bound, 5.49 M `_generate_tokens_from_c_tokenizer` calls). It is a real target but it is
not a one-liner, and it is not needed to clear 2×.

### 3.4 Two environment findings that block a cloud lane outright

Neither is repo state; both cost this lane real time and both will hit the next cloud session.

1. **The container's clone arrived SHALLOW** (283 commits, `.git/shallow` present). The ADR-85
   disposition floor `24882f8cc` is below the cutoff, so `journal_spine_anchor` raised
   `AnchorError: ... not a valid object name`, `audit.py health` went `DEGRADED`, `audit-health`
   exited 1, and **every commit in the container was refused** — the first 10-commit sample is
   ten `rc=1` rows for exactly this reason. `git fetch --unshallow` (5102 commits) fixed it.
   **A fresh cloud lane cannot commit until it unshallows.**
2. **`audit.py health` still FAILs afterwards, on `[!!] repos registered (none)`** — the fleet
   siblings `ai-council` and `corp-monorepo` do not exist in the container. This is the only
   remaining FAIL, and it means a cloud lane's commits are gated by the *absence of other repos*.

**And the cost of the fix is the finding's twin:** unshallowing took the stack from **9.6 s to
42.8 s per commit**, because the git-walking checks then had 5102 commits to walk instead of 283.
`audit.py health`'s cost scales with history depth — which is the same reason §3.3's saving will
keep growing as `JOURNAL.md` does.

### 3.5 The cross-question payoff

§1.4 showed six of the suite's slowest tests invoke `cmd_health` in-process, so the same one-line
change was measured against the **full suite** — run C, `-n auto`, same tree, same container, the
patch applied through a `-p` plugin so the tree stayed byte-unchanged.

**The hypothesis was that the suite would get faster. It did not, and the honest result is the
more useful one.**

| | run A (baseline) | run C (memoized) |
|---|---|---|
| **wall** | **485.55 s** | **521.60 s** *(+7.4 %)* |
| outcome | 28 failed · 2924 passed · 7 skipped · 1 xfailed | **identical** |

Per-test, the fix did exactly what §3.3 predicted:

```
test_health_stays_ok_with_na_status                47.70s -> 23.10s   -24.60
test_live_registry_has_no_unconditionally_inert…   48.82s -> 23.01s   -25.81
test_health_degraded_no_ecosystem                  47.41s -> 22.24s   -25.17
test_health_ok_with_registered_repo                46.19s -> 22.21s   -23.98
test_no_hub_only_check_skips_when_the_stored_path… 46.10s -> 22.07s   -24.03
test_real_oracle_blocks_real_cross_module_removal 269.73s -> 269.71s   (floor, untouched)
```

**123.59 s of test time removed — and the wall went up 36 s.** Both are true, and the reconciliation
is §1.4's floor. One test is 269.7 s of a ~486 s wall, so the wall is set by *how the remaining work
packs around that test on four workers*, not by how much of it there is. xdist's default `load`
scheduler assigns work up front; removing 124 s from tests that were already sharing a worker with
slack changes the packing without shortening the critical path, and the run-to-run variance of that
packing is larger than the saving. This is the same mechanism night-2 measured when it attributed
~204 s of a 473 s wall to two heavy files landing on one worker.

**So the correct claim is narrow: the fix removes real work and halves five tests; it does not
reliably shorten the suite while one test owns 55 % of the wall.** Both runs are N=1, and N=1 is
not a distribution — the +7.4 % is inside the variance this scheduler produces, and nothing here
should be read as the patch making the suite slower.

**This is independent evidence for §1.6's second lever.** A suite whose wall does not respond to
removing a quarter of its non-floor work is packing-bound, which is precisely the condition
`--dist worksteal` exists to fix.

### 3.6 Recommendation

**Recommendation: memoize `journal_anchor._entries` with `functools.lru_cache(maxsize=1)`.**
One stdlib line, no dependency, no Windows surface, 2.49× on the hook, 2.4× on the per-commit
cost, output byte-identical. **Justify it on the commit gate, not on the suite** — §3.5 measured
123.59 s of test time removed with no wall-clock gain, so a claim that it speeds up CI would not
survive. It needs a row and a test (assert `_entries.cache_info().misses == 1` across a multi-commit
range) — this lane files neither, per its own contract.

**Do not adopt:** dropping `uv run --locked` from the hook entries (measured: 34 ms vs 17 ms
direct — 17 ms × 14 hooks ≈ 0.24 s, i.e. **0.6 %** of the cost; it would trade the locked
environment for nothing) · moving `audit-health` to `pre-push` (it would stop gating the commit it
exists to gate, and §3.4 shows the pre-push organs are the ones with real teeth) · caching health
results across commits (the tree changes between commits; a stale pass is worse than a slow one) ·
`--no-verify` as routine practice (`journal_spine_anchor`'s backstop makes it a **FAIL**, by design).

---

## 4. Scratch hygiene — core-invariant #9

Everything this lane created, and the verification that it is gone:

```
scratch/night3-hook-timing     branch   created -> deleted   ("scratch branch gone: YES")
scratch/night3-hook-timing-2   branch   created -> deleted
tests/fixtures/night3-hook-timing-probe.txt   created -> removed ("probe file gone: YES")
background agent d58afcea      dispatched -> `claude stop`   ("background agents left: 0")
```

`HEAD` and tree SHA before and after both samples: `65dc3183…` / `cf87f2a6…` — **identical**
(`sha identical: YES`, `tree identical: YES`). `git status --porcelain` empty.

**One deliberate, disclosed state change remains:** the clone is now **unshallowed** and the
git hooks are **armed** (`pre-commit install`). Neither is tracked state, both are what a working
clone is supposed to look like — the repo's own `arm_hooks.py` performs the second at every
`SessionStart` — and §3.4 is the reason the first was necessary. Nothing else was left behind.

## 5. What would close the remaining gaps

- **Q1:** one `-n auto` run of the merged tree **on the operator's Windows host** with
  `--durations=25`, to confirm the 2.95× is spread across subprocess-heavy tests rather than
  concentrated in one Windows-pathological case. This lane cannot run it.
- **Q2:** re-witness the AM-5 nesting property on the host (§2.1) — this container contradicted it.
- **Q3:** the `lru_cache` measured here was a monkey-patch; the source change still needs a test
  proving one split per range, and a second reading on whether `maxsize=1` is right when `_entries`
  is ever called with two different journals in one process.
- **Q3/Q1 jointly:** §3.5's wall-clock comparison is N=1 against N=1. Three runs each of baseline
  and memoized — and a pair with `--dist worksteal` — would separate "the fix does not help the
  wall" from "the `load` scheduler's variance is larger than the fix", which is the difference
  between the two readings that comparison currently admits.

---

**One recommendation per question.**

1. **Q1 — change nothing about the invocation: the integrator's run already used xdist** (`addopts = "-n auto"`, confirmed live by `bringing up nodes...`), and the 1431 s is a ~2.95× Windows-host penalty over this container's 485.55 s on the identical tree, floored by one 269.73 s test; if one thing is changed, give `.claude/commands/lane-integrate.md` the `--dist worksteal --max-worker-restart=0` flags lane N already put in `verify.py`.
2. **Q2 — build `harvest_batch.py` first** (board watch via `claude agents --json --all` on `state == "done"`, then packet fetch by `git show` — never by parsing `claude logs`, which is ANSI screen replay), and keep dispatch operator-run with the `[#530]` `claim` gating the spawn and releasing on a failed spawn.
3. **Q3 — memoize `journal_anchor._entries` with `functools.lru_cache(maxsize=1)`**: one stdlib line takes `audit-health` from 42.68 s to 17.14 s with byte-identical findings, and that hook is 98.5 % of a 42.75 s gated commit — justified on the commit gate alone, since the same fix removed 123.59 s of test time without shortening the suite's wall (§3.5).
