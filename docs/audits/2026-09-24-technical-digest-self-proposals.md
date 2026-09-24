> **Landed by** `lane-precut-landing`, verbatim below.
> Source: `to-browser/DIGEST-SELF-PROPOSALS-2026-09-24.md` (a Drive transport path, not retained
> in this repo — verifiable against the bytes landed below by their hash,
> `sha256:d24be9c37eb38e9f8c79a8a3e05bddde9b42f4d3fd121316004f90c04a1f26da`, 15,206 B, computed by
> this lane at landing time).

---

carried-by: `docs/audits/2026-09-24-technical-digest-self-proposals.md` (landed by `lane-precut-landing`, 2026-09-24)
lands-via: the next batch's P1 (path layer + portability check) and P2 (transport adapter) contracts, per DECLARE-OFFBOX-PORTABILITY; no repo change was made
date: 2026-09-24
from: night-readonly (BATCH-NIGHT-READONLY-2026-09-23 Part 2, job a58f3cec, Opus 5.5), read-only on main @ 4667f731

# DIGEST — the harness's proposals for itself: containerization and the transport contract

**Inputs, as read:**
- `to-browser/SESSION-env-globals-2026-09-23.md`: 48 KB, so under the 50 KB Gemini threshold. **The batch named the Drive root; the file lives under `to-browser/`.**
- ADR-121 and its compute record, `git show origin/worktree-lane-adr-state-store:docs/audits/2026-09-23-technical-compute-substrate.md` (branch tip 48c0cdc2).
- `to-cc/DECLARE-OFFBOX-PORTABILITY-2026-09-23.md` and `to-cc/DECLARE-TRANSPORT-SCHEMA-2026-09-23.md`.

Drive paths are excluded, as ordered (already inventoried: 0 hard-coded in code, 119 read sites).

**Tags:**
- VERIFIED: a probe opened the file:line, and the key claims were re-opened by this orchestrator.
- PROBE: opened by the Sonnet probe only.
- UNVERIFIED: nobody opened it.

---

## (a) Containerization — every environment assumption except Drive paths

**Summary:** nothing crashes on Linux; everything degrades.
- The harness's hook layer is the one hard break: two SessionStart hooks invoke the Windows `powershell` binary.
- Everything else either has a POSIX branch already or silently loses coverage.
- Every CI workflow is already `ubuntu-latest`.

### a1. PowerShell-bound (7 sites)

- **`.claude/settings.json` SessionStart: `powershell -ExecutionPolicy Bypass -File …/surface_triage.ps1`, and `powershell -NoProfile … billing_leak_sentinel.ps1`.** VERIFIED (read this session).
  - DECLARE-OFFBOX allows `pwsh`, but these call `powershell`, the 5.1 name, which does not exist on Linux.
  - **Replace:** port both to `uv run --locked python scripts/<name>.py`, the pattern the other 6 SessionStart hooks already use.
  - This also fixes surface_triage's 252/262 timeouts (Digest ORGAN-TRIAGE D2).
- `scripts/setup-fleet-scheduler.ps1:125,131`: `Register-ScheduledTask`. PROBE.
  - **Replace:** a systemd timer/cron line in the devcontainer, or the existing `.github/workflows/conductor.yml` schedule. Operator-run, so low urgency.
- `templates/dispatch-shim.ps1` (`#requires -Version 7`): pwsh 7 runs on Linux, so it is portable once `pwsh` is in the image. PROBE.
  - **Replace:** add `pwsh` to `.devcontainer/Dockerfile`, or retire the shim in favour of `dispatch.py launch`.
- `.claude/settings.json:8,120,132`: the `deny_and_point` matcher string `Bash|PowerShell|Grep`. Unwired today. Harmless. PROBE.
- **Contracts:** every `LANE-*.md` Dispatch line embeds `$env:CLAUDE_PROMPTS_DIR\LANE-….md`, a PowerShell token and a backslash (VERIFIED in LANE-5A-2/5A-3).
  - **Replace:** `gen_lane_contract.py` emits a logical name (`transport:LANE-5A-3-memory-gate.md`), resolved by the adapter (b). DECLARE-OFFBOX item 1 names this token explicitly.

### a2. Vendored or assumed binaries (8 sites)

- **The `dispatch_drift.py:180-186` / `dispatch_conformance.py:190-196` `find_powershell()` + `Get-Command` organ.** It degrades to `TIER_NO_SHELL` without pwsh, so the dispatch-drift verification path goes dark in a container. PROBE.
  - **Replace:** `pwsh` in the image (the organ then works unchanged), plus a CI assertion that the tier is not `NO_SHELL` in the container.
- **The `winreg` user-env read of `CLAUDE_PROMPTS_DIR` in `dispatch.py:206-211`, `fleet_health.py:1832-1840` and `transport_report.py:116-118`.** Each is guarded by `os.name != "nt"` and returns None on Linux, so the "authority drive" override becomes inert rather than failing. PROBE.
  - **Replace:** the one path layer (DECLARE-OFFBOX item 1) — YAML + env, with `winreg` as a Windows-only fallback inside it.
- **`codex` is not installed in the devcontainer** (ADR-121 compute record §3: "No Codex install step exists — only a `node` assertion"). Every Codex review leg fails in a container.
  - **Replace:** an `npm i -g @openai/codex` step pinned in `.devcontainer/Dockerfile`, beside the `claude-code` feature.
- `agy` and `copilot`: no install leg anywhere. UNVERIFIED beyond a name grep. **Replace:** declare them in `ecosystem/provider-registry.yaml` with an `install:` field, and assert them in the container self-test.
- Already portable, cited as the pattern to copy:
  - `provider_bench.py:424-430` `_npm_shim()` (`.cmd` only on nt);
  - `resource_lifecycle.py:243-289,344` (a `ps -eo` POSIX branch plus `ctypes.windll` behind `_IS_WINDOWS`).
- `surface_triage.ps1:30-31`: a `ProgramFiles\GitHub CLI\gh.exe` fallback. Moot once it is ported (a1).
- `uv ==0.11.19` (`pyproject.toml:25`): portable. The image must install that exact Linux build (the Dockerfile already pins uv; VERIFIED in the ADR-121 record §3).

### a3. Temp and home paths (4 sites)

- `scripts/gen_seat_boot.py:96-101`: the generated paste embeds a `$env:USERPROFILE\Downloads` fallback. **Replace:** emit the logical transport name.
- `scripts/no_leftovers.py:443`: `--jobs-dir` defaults to `~/.claude/jobs`. UNVERIFIED whether it resolves through `Path.home()`. **Replace:** the path layer's `jobs_root`.
- `ecosystem/index.yaml`, `ecosystem/registry.md`, `ecosystem/provider-registry.yaml`, `.claude/settings.json:126`: literal `C:\Users\1028120\…` values. They are data, and the probe found no runtime dereference (UNVERIFIED). **Replace:** paths relative to a `DEV_ROOT` the path layer resolves.
- `tests/test_connection_loop.py:445`: `C:\Program Files\Git\bin\bash.exe` is tried first, then `shutil.which`. It degrades correctly. **Replace:** `shutil.which` first.

### a4. Windows-only tests (about 7 files; none crash, all silently skip)

- `tests/test_dispatch_py.py:151`: a drive-root test, genuinely Windows-only. **Keep**, marked `windows_only`.
- `tests/test_dispatch_launch.py:466`, `tests/test_dispatch_shim.py:19-21`: skip unless pwsh AND nt. **Replace:** drop the `nt` leg once `pwsh` is in the image, so the shim is covered on Linux too.
- `tests/test_proof_layer.py:102-105`: a skip keyed on `C:\Program Files\PowerShell\7\pwsh.exe`. **Replace:** `shutil.which("pwsh")` only.
- `tests/test_fleet_health.py:2302-2332`: 5 `importorskip("winreg")` tests. **Replace:** test the path layer's env/YAML resolution on every OS; keep `winreg` as one Windows-only fallback test.
- `tests/test_spine_moments.py:101,122`: `CREATE_NEW_PROCESS_GROUP` on win32. UNVERIFIED whether the POSIX branch runs.
- **Gate proposal:** a CI job in the devcontainer that reports the SKIP count by reason. A skip that rises is the regression signal (DECLARE-OFFBOX C2).

### a5. Other

- `deploy/carrier_floor.py:310-322` casefolds tool names unconditionally. That risks a false match on a case-sensitive filesystem. **Replace:** casefold only when `os.name == "nt"`.

### a6. Ranked by blast radius, as proposed lanes

1. **Path layer + portability check** (DECLARE-OFFBOX P1). It absorbs winreg, jobs-dir, USERPROFILE, contract tokens and the `ecosystem/` literals. The check is an audit leg that fails on `[A-Z]:\\`, `$env:` and `powershell ` in scripts, hooks and templates.
2. **Port the two `.ps1` SessionStart hooks to Python.** Small and file-disjoint, and it fixes the 96% timeout.
3. **The devcontainer gains `pwsh` and `codex`.** It restores dispatch-drift and Codex review in the container.
4. **A container CI job with a skip-count report.**
5. The Task Scheduler → cron/Actions schedule.

---

## (b) The transport contract — logical names, writers, readers

**Rules that bind this map:**
- DECLARE-TRANSPORT-SCHEMA's registry: kinds, folders and writers, "enforced by code, not by this table".
- ADR-121 D9: *"transport input is **untrusted** and is admitted into `harness-state` only by the integrator after validation"*. That is the ADR-121 file on `origin/worktree-lane-adr-state-store`, Decision D9; ADR-121 is Proposed, and migration step 1 is unbuilt.

**Admitted?** below means that code validates more than the file name before the content drives a verdict.

### b1. Kind by kind: writer, reader, admission, reconciliation

- **DECLARE / AMEND / BATCH** (to-cc, browser-written)
  - Readers: `gen_handoff.py:1272,1324-1340`, `seat_refusals.py:705-718`, `decision_coverage.py:157`.
  - Admitted: **no.** A prefix match plus one `carried-by:` header regex; the body is trusted.
  - vs DECLARE: **DIFFERS.** One undifferentiated `CARRIAGE_PREFIXES` bucket. BATCH has no dispatcher/lane parser of its own, so it is read as prose.
- **RATIFICATION**
  - Reader: `gen_handoff.py:904-911`, which checks `to-browser/RATIFICATION-{today}.md`. VERIFIED.
  - vs DECLARE: **DIFFERS twice.**
    - The folder: the DECLARE says `to-cc`, and real files are in `to-cc` (`RATIFICATION-2026-09-23-copilot.md`).
    - The name: the DECLARE says `<date>-<topic>`, and code expects no topic.
    - So the preflight row false-FAILs against current practice.
  - Admitted: presence only.
- **ANSWER**
  - Reader: `gen_handoff.py:1063-1066`, a name match on the seat.
  - Admitted: presence only.
  - vs DECLARE: AGREES on the name family.
- **INTEGRATOR order:** 0 code hits (VERIFIED). **MISSING-FROM-CODE.** Read as prose by the integrator seat.
- **LANE contract**
  - Writer: `gen_lane_contract.py:1701-1791`, writing to the transport root. Readers: the lane (prose) and `plan_lint.py`.
  - Admitted: **no.** A lane executes the prose. `plan_lint` is the only shape reader, and it refuses every live WAVE5A contract (Digest MEASUREMENTS §3).
  - vs DECLARE: AGREES on name/folder. The DECLARE's "later the spine" writer is not yet real.
- **SESSION seat receipt**
  - Writers: `handback.py:326-340` (appends HANDBACK + STATE lines), `dodo.py:111`. Reader: `lane_end_guard.py` (the last HANDBACK-shaped line only).
  - vs DECLARE: **DIFFERS.**
    - The name: the DECLARE says `SESSION-<slug>-<batch>.md`, while code and the WAVE5A rule 6 use `SESSION-<slug>.md`.
    - **Lane STATE lines:** the DECLARE puts them "inside the integrator receipt, integrator only". The code writes them inside the LANE's own SESSION file, from the handback organ, and `StateLine` (`handback_schema.py:152-168`) has **0 readers**, while the DECLARE names the dispatcher as the reader.
  - Admitted: no.
- **LANE-END**
  - Writer: `transport_report.py:82`, through an atomic `os.replace`. Reader: `lane_digest.py:264-283`, via `parse_report`.
  - Admitted: **structured parse only.** No writer identity, so a hand-written file reads the same.
  - vs DECLARE: AGREES (the lane-end organ writes it, the digest organ reads it).
- **STATE-BATCH:** 0 code hits (VERIFIED). **MISSING-FROM-CODE.** WAVE5A's dispatcher closes on it, by hand.
- **QUESTION**
  - Reader: `gen_handoff.py:1035-1063`, a glob plus a header regex.
  - Admitted: no.
  - vs DECLARE: AGREES on name. The DECLARE's `-<batch>` suffix is not required by the glob.
- **REFUSED (repair order)**
  - The DECLARE says **integrator only.** Code: **`handback.py:392` writes `REFUSED-{lane}.md` from the handback organ** (VERIFIED).
  - **DIFFERS.** This is the collision the DECLARE was filed for, and it is still live.
- **HANDBACK-REFUSED (self-refusal):** 0 code hits (VERIFIED). **MISSING-FROM-CODE.** The handback organ emits the bare `REFUSED-` name for both meanings.
- **DIGEST**
  - `lane_digest.py:357` writes to stdout only; a seat pastes it.
  - vs DECLARE: **DIFFERS.** The DECLARE says a "batch-close organ" writes it.
  - Readers: browser/operator (AGREES).
- **GO-<batch>**
  - Reader: `go_reader.py:88-113`, presence only by stated design ("presence, not authority").
  - **MISSING-FROM-DECLARE.** It is coded and load-bearing (harness `merge` moment), yet absent from the registry table.
- **LEDGER-<repo>**
  - Writers: `gen_ledger.py:71-75`, `gen_handoff.py:891`. Reader: `gen_handoff.py:906-919`, a `refreshed` token.
  - **MISSING-FROM-DECLARE.**
- **Not in the DECLARE, observed on the transport tonight:** `PLAN-*`, `LEDGER-*-vN-superseded`, `DIGEST-*-APPENDIX`, `-v1-superseded` renames.
  - The DECLARE's own self-critique names `PLAN-` and rename-to-superseded as strays.
  - The rename is still the practice (e.g. `BATCH-WAVE5A-2026-09-23-v1-superseded.md`), against lifecycle rule 3 ("no rename-to-superseded").

### b2. The enforcement the DECLARE requires (item 4): none exists

- **No transport adapter.** Every writer builds `Path(transport)/"to-x"/f"…"` itself.
- No batch-close stray lint.
- No registry file. The table lives only in the DECLARE.

### b3. ADR-121 D9 (untrusted until admitted): where the code disagrees

- **Every reader above consumes transport content with no admission step.** They are not violations of a live gate, because none exists yet. They are the population that migration step 1 must route.
- The four whose raw read becomes a durable fact, and so come first:
  1. `lane_digest.reports_root_lanes` (digest verdicts);
  2. `gen_handoff` preflight rows (RATIFICATION/QUESTION/DECLARE → PASS/FAIL);
  3. `seat_refusals` carried-by (discharge);
  4. `go_reader.read_go` (the merge moment).
- **Where admission goes:** one choke point, the integrator's fold boundary. The registry is the admission check: kind by name + folder + header + writer. The content becomes an event on `harness-state`, and downstream reads the projection (ADR-121 D8), never the file.

### b4. Proposal: one contract, three artifacts, file-disjoint

1. **`ecosystem/transport-registry.yaml`.** The DECLARE table as data, plus the missing kinds `GO-`, `LEDGER-` and `PLAN-` (or PLAN banned), plus `-v<n>` with a `supersedes:` header.
   - Each row: `kind`, `pattern`, `folder`, `writers` (organ ids), `readers`, `admission: none|shape|integrator`.
2. **`scripts/transport.py`, the adapter** (DECLARE-OFFBOX P2 = DECLARE-TRANSPORT item 4, one module).
   - `read/write/list(kind, **fields)`, with the two backends: the local mount and the Drive API.
   - It refuses a write whose caller organ is not in `writers`. That is what makes `handback.py:392` physically unable to write `REFUSED-`: it gets `HANDBACK-REFUSED-`.
3. **The admission leg:** `transport.admit(kind, path)`. It returns a validated, typed record or a refusal receipt. The four readers in b3 switch to it first. ADR-121's event log consumes `admit()` output when it lands, so this does not wait on ADR-121.
- **Measures:** these are the DECLARE's own T1-T4, read from adapter receipts.
- **One conflict to rule:** where lane STATE lives (b1, SESSION). The DECLARE says the integrator receipt; the code says the lane's own SESSION file, which nothing reads. **Recommendation:** follow the DECLARE, and delete the unread `StateLine` write.

## Routing record (what served)

- orchestrate + reconciliation re-checks: claude-opus-5-5 (this session).
- probes: 2 × Sonnet sub-agents (`model: sonnet`). (a) 24 tool calls, about 113k tokens; (b) 29 tool calls, about 134k tokens.
- lookups: none needed as separate Haiku calls. The probes did their own greps. **Recorded as a deviation from the routing table, not a substitution:** no Haiku agent was launched.
- Gemini/agy: not used. No input exceeded 50 KB.

DONE 2026-09-24 00:35
