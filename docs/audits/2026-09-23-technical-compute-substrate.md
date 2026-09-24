# Compute substrate — where the harness should execute and where it should test (Part B)

<!-- scope: meta -->

- **Date:** 2026-09-23
- **Lane:** `lane-adr-state-store` (branch `worktree-lane-adr-state-store`)
- **Order:** `to-cc/BATCH-ADR-STATE-STORE-2026-09-23.md` Part B ("cost is not a constraint now;
  performance is")
- **Provenance:** ADR-120 (stage 13 RUN needs a substrate; `DECLARE-OFFBOX-PORTABILITY-2026-09-23`
  makes portability its precondition)
- **Consumers:** [#963], ADR-121
- **Method:** repo/transport history — Sonnet sub-agent; vendor facts — Haiku web lookups; prices and
  plan limits re-verified by Codex `gpt-6-sol` with live web search (debate record, "Independent
  check", C16–C23). Nothing was provisioned or bought.

## 1. Answer first

- **Execution host: one persistent Linux VM you control** (16–32 dedicated vCPU, 64–128 GB RAM),
  reached over SSH / VS Code Remote-SSH, running the repo's **own devcontainer image** via
  `devcontainer up`. It is the only candidate that is simultaneously persistent (no idle stop, no
  re-provision on restart), large enough for 6+ lanes plus a suite, and always on for night batches.
- **Test host: GitHub Actions larger runners** (16- or 32-core Linux) for the full-suite merge
  verdict — ephemeral, clean, already wired (`conductor.yml` runs 7,343 tests in ~8 min on a
  standard runner). **Blocked on a verdict nobody can read**: CI is 20/20 red against a 6-day-stale
  frozen baseline, so its first step is ADR-121's step 1 (baseline identity), not more cores.
- **Codespaces is not the execution host**, despite being proven fastest per core: the account is
  capped at 4 cores, a codespace stops on inactivity (a risk for unattended nights, untested), and the previous
  attempt stalled on re-provisioning, not on speed.

## 2. Why the laptop cannot carry it (measured)

- 27.7 GB RAM, 3–6 GB free; `-n` hand-set to 2 because `-n auto` OOM-killed five full-suite runs
  (`pyproject.toml:266-288`); repeated reaper and OOM kills on 09-22/23; operator cap ≤ 2 heavy
  sessions and a 3 GB launch floor (`to-browser/DIGEST-VERIFY-TIME-2026-09-23.md`, "Memory").
- A local merge's `compare` leg costs 30–59 min at `-n 2`; the same full suite takes ~8 min on a
  4-vCPU CI runner (same digest).
- Same commit, same suite (2026-08-20): **local Windows 715 s · Codespaces 2-core 281 s · 4-core
  147 s**; `ruff check .` 14.7× faster; suite scaling 95.7 % through 4 cores
  (`docs/audits/2026-08-20-technical-codespaces-audit.md` §0).
- Git process spawn on this box: ~1.3 s per process under load (state-store research record §5).
- The memory-seat admission ceiling (26 seats at 413 MB/seat) refused a 28-seat burst
  (`ecosystem/quality-requirements.yaml:440-448`).

## 3. The earlier Codespace attempt — what it cost and why it stalled

**Cost recorded:** GitHub Free plan (120 core-h / 15 GB-month free); **1.57 core-hours used in
August (1.3 %)**, never billed; $0.090 per core-hour flat at every size; ruling: stay in the free
tier, never buy overage (`docs/audits/2026-08-20-technical-codespaces-audit.md` §0 and "RULING").
`logs/CODESPACE-RECEIPTS.jsonl` holds one entry — an 11.97-minute probe. Money was never the cost;
**lost lanes were.**

**Why it stalled** (chronological, all from the repo):

1. 2026-08-20 — the machine menu **stops at 4 cores** (account-level, proven across 15 repos and 5
   regions); `hostRequirements` can only subtract. The audit's counterweight: "`devcontainer up` on a
   host we control has still never been executed".
2. 2026-08-25 — Claude Code was not installed in the image; the first dispatch failed copying the
   contract in (~0.4 core-hours for 11 min).
3. 2026-09-01/05 — transport bugs in `Start-DispatchCodespace` (PowerShell profile / scp path
   parsing), fixed.
4. Recurring — `receipt.json` at the repo root blocked in-container commits
   (`dot_prefix_discipline`).
5. 2026-09-09 — a *restarted* codespace came back without `uv` and with a stale `.venv`, producing a
   false "126 failed vs 28 baseline".
6. **2026-09-14/15 — fatal:** `provision.sh` fast-forwarded its own tree, then executed a stale copy
   of itself that called the retired `scripts/cloud_provisioning.py`; a fresh `gh codespace create`
   came up with **no `claude`, `node`, `npm`, `uv` or `gh`**; "The CODESPACE substrate is DEAD";
   **eight of the fifteen planned lanes were routed to it**, the batch ordered at sixteen landed six
   (`JOURNAL.md:2432-2442, 2504-2517`).

Repaired since: `.devcontainer/Dockerfile` (from `mcr.microsoft.com/devcontainers/python:1-3.12-bookworm`)
bakes uv at the exact pin `0.11.19`; `provision.sh` asserts `claude`/`node` and fails loud; the
self-refresh moved to `updateContentCommand` (`.devcontainer/Dockerfile:30,81`,
`devcontainer.json:147,229-231`). **No Codex install step exists** — only a `node` assertion.

**Lesson:** every stall was an *environment-reproducibility* failure, not a speed or cost failure.
Any host that re-provisions itself on restart inherits this class; a persistent host built once from
the same image does not.

## 4. Comparison

Prices are list prices found 2026-09-23; "verified" = re-checked by `gpt-6-sol` with live web
search. Cost is recorded, not weighed (the order).

| | Codespaces (larger types) | Persistent cloud VM (SSH / Remote-SSH + devcontainer) | Actions larger runners | Serverless sandboxes (Modal, Daytona) |
|---|---|---|---|---|
| **cores / memory** | 2–32 cores; 16-core = 64 GB (verified); **this account: 4-core ceiling** until the plan changes | any: e.g. Azure D16s_v5 16 vCPU / 64 GiB; D32s_v5 32/128; Hetzner dedicated CCX up to 48+ vCPU | 4–64 cores Linux; 16-core, 32-core common | per-sandbox CPU/memory limits (Modal per-core-second; Daytona per-vCPU-second) |
| **start time** | ~60 s cold with prebuild, 110 s measured create (85 s container build); resume < 10 s | boot once; afterwards always on | per job: runner pickup + checkout + `uv sync` (~1–2 min) | sub-second to ~100 ms claimed (Daytona 27–90 ms; vendor/blog figures, not verified) |
| **persistence** | stops after an inactivity timeout (default 30 min, max 240) — whether a running background agent counts as activity is **untested here**; stopped codespaces keep disk | full — disk, `~/.claude`, worktrees, caches, running batches | none (ephemeral per job) | volumes/snapshots; lifetime limits per sandbox |
| **Claude Code / Codex** | `claude-code` devcontainer feature (present); Codex **not installed** — needs `npm i -g @openai/codex` | same image via `devcontainer up`; `claude` with `CLAUDE_CODE_OAUTH_TOKEN` (`claude setup-token`); `codex login --device-auth` once, persists | `anthropics/claude-code-action` / `claude -p`; `codex exec` with API key | install per image; headless only |
| **transport** | Drive API adapter (`google-api-python-client`, service account or OAuth refresh token) — not built | same adapter, **or rclone mount** (rclone Drive backend) — a persistent host can mount | adapter reads; tests should not need the transport | adapter |
| **secrets** | Codespaces secrets (`CLAUDE_CODE_OAUTH_TOKEN` declared today) | files / env on the VM, or a secret manager; SSH keys | repo/org Actions secrets | vendor secret store |
| **portability work first** (DECLARE-OFFBOX P1–P3) | path layer, transport adapter, Codex install leg | path layer, transport adapter, Codex install leg | none for the suite (already runs on ubuntu); **baseline refresh** | path layer, adapter, image |
| **set-up effort** | low (exists), but plan change for > 4 cores | medium: one VM, Docker, devcontainer CLI, SSH, secrets | low (workflow exists); plan must be Team/Enterprise for larger runners (verified) | high: new API surface, no git-worktree-native model |
| **recorded / list cost** | $0.090/core-h flat (account, Aug); 16-core $1.44/h (verified) | Azure D16s_v5 Linux ≈ $0.768/h East US (verified, compute only) | 16-core $0.042/min, 32-core $0.082/min Linux x64 (verified) | Modal ≈ $0.14/core-h; Daytona ≈ $0.05/vCPU-h (unverified) |
| **fit** | proven fast; wrong for unattended nights and > 4 cores today | **execution host** | **test host** | not now: agent sessions need long-lived worktrees and git state |

Unverified and not used for the recommendation: the Hetzner price rise reported by one lookup, and
the Daytona/E2B blog-sourced figures.

## 5. Recommendation

### Execution host — a persistent Linux VM running the repo's devcontainer

- **Size:** start at 16 dedicated vCPU / 64 GB (e.g. Azure D16s_v5 or an equivalent dedicated
  instance); the admission organ's own arithmetic (413 MB/seat, 3 GB reserve) puts ~140 seats' worth
  of headroom in 64 GB — memory stops being the governor, and the lane ceiling (ADR-110) becomes the
  only one. Move to 32/128 when a measured batch saturates CPU.
- **Why this and not Codespaces:** persistence removes the whole re-provision failure class (§3);
  no inactivity stop to reason about for night batches; no 4-core account ceiling; `rclone` can mount Drive on a host we
  own, so the transport adapter can be phased in rather than being a blocker.
- **First measurable step:** provision one VM, run `devcontainer up` with the repo's
  `.devcontainer/` (the step the 2026-08-20 ruling put first and that has never been executed), then
  (a) the full suite at `-n 16` and (b) one fixture lane end to end reading its contract and writing
  its handback through the adapter (DECLARE-OFFBOX P4 / goal C1). **Exit:** suite wall time recorded
  and < 4 min; the lane merges; local workstation memory use for that lane ≈ 0.

### Test host — Actions larger runners for the merge verdict

- **Why:** the suite already runs green-or-red on ubuntu in ~8 min on 4 vCPU; a 16-/32-core runner
  should cut that several-fold (estimate, not measured — the 95.7 % scaling was measured only to 4
  cores). Ephemeral runners give a clean, reproducible verdict per SHA — exactly the "verdict with
  baseline identity" ADR-121 needs.
- **Precondition, not optional:** CI's verdict is unreadable today (20/20 red vs a 6-day-stale
  freeze). Larger runners on an unreadable verdict buy nothing.
- **First measurable step:** refresh the known-reds baseline as ADR-121 step 1 (baseline events with
  an ID that CI and local both stamp), then run `conductor.yml`'s pytest job on a 16-core larger
  runner at `-n 16`. **Exit:** full suite < 4 min wall; CI and local agree on the merge SHA's verdict
  under the same baseline ID; the plan change (Team) is recorded.

### What the portability work must deliver first (from `DECLARE-OFFBOX-PORTABILITY`)

1. **One path layer** — `CLAUDE_PROMPTS_DIR` is referenced in 25 files under `scripts/ .claude/
   templates/`, there is no shared path module, 4 files carry hard-coded `C:\Users` paths and 12 carry
   `$env:` tokens (Sonnet census; the "18+ independent resolvers" count was not confirmed by the
   independent check — the reference count is).
2. **The transport adapter** (Drive API; rclone as the persistent-host alternative).
3. **A Codex install leg** in `provision.sh` / the Dockerfile (absent today).
4. **The portability gate** (DECLARE P4 item 4) so none of the above regresses.

## 6. Where the evidence stops

- No VM was provisioned and no larger runner was run; > 4-core scaling is extrapolated.
- Vendor start-time claims for sandboxes are from vendor/blog pages.
- Whether Codespaces idle-timeout treats a running `claude` background process as activity was not
  tested here; the recommendation does not depend on it (persistence and the 4-core cap suffice).
