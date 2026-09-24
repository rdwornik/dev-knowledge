> **Landed by** `lane-precut-landing`, verbatim below.
> Source: `to-cc/AMEND-PLAN-WAVE5-2026-09-24.md` (a Drive transport path, not retained in this
> repo — verifiable against the bytes landed below by their hash,
> `sha256:5309302c2dfdd5c39616df73414ba7e98e70f112db6a1ea2b7072918f54b1d6e`, 5,754 B, computed
> by this lane at landing time).

---

carried-by: `docs/audits/2026-09-24-technical-amend-plan-wave5.md` (landed by `lane-precut-landing`, 2026-09-24)
lands-via: the next landing commits it beside PLAN-WAVE5 under docs/audits/; the handoff boot points to both
date: 2026-09-24
amends: to-cc/PLAN-WAVE5-2026-09-23.md (§2, §4, §5, §6, §7), after the three night read-only digests (ORGAN-TRIAGE, SELF-PROPOSALS, MEASUREMENTS) and the WAVE5A close
from: 2026-09-19-dev-knowledge-architect (Layer-1 browser seat, SEQ 1)

# AMEND — plan wave 5 after the night of 2026-09-23/24

## §2 — a correction to the diagnosis

"Built but never called" was mostly the instrument. Of 97 organs the census called unobserved or
unreachable, **74 are wired** through surfaces the census cannot see (import chains, git hooks,
consumer-side hooks, session hooks, the devcontainer, harness moments); 3 await a wiring; 18 are
deliberately manual with a date; **2 are retire candidates, and both collide with a standing
ruling.** The real defect is that the harness has no trustworthy measure of what runs.

## §4 — decisions owed, added

10. `export_backlog_view.py`: retiring it reverses ruling [#563] (view layer). Does the operator
    still use the external Backlog.md board? No → retire; yes → keep.
11. `offload_admission.py`: is the offload role (intake #75) dead or deferred? Dead → retire;
    deferred → keep-manual, dated.
12. **Opus 5.5 for orchestrate/plan:** the A/B shows equal cost (within 3.5 %), equal structure, and
    88 % vs 52 % checkable Done-items. Architect's recommendation: admit, by explicit model id.
13. **Skills:** switch off the 8 claude.ai-synced Anthropic skills (account setting); rule the fate
    of the 4 never-invoked project skills (`preflight`, `spine`, `why`, `conformance-hub`).
14. Run `/doctor` interactively once, approving its read-only prompts (5 checks were blocked headless).

## §5 — handoff, added

- Until the transport registry lands, **code is the authority over the transport DECLARE:** the
  operator's acts of the day are written where `gen_handoff` looks, `to-browser/RATIFICATION-<today>.md`.
- `HANDOFF_PROCESS` is bumped to 7.2.0 at the cut.
- Known deviation, recorded: rename-to-superseded remains the practice until the adapter provides
  versions with a `supersedes:` header.

## §6 — wave 5b, made concrete

2. **Launcher to router** is row [#691] Half B; D32 cites it instead of a new row. Registry: explicit
   model ids for every role; an Opus 5.5 rate row; **cache-write multiplier corrected to 2×** (the CLI
   bills 1-hour cache writes at 2× input; the registry says 1.25×, so cost telemetry undercounts by
   about 27 %).
3. **Hooks:** port the two PowerShell SessionStart hooks to `uv run --locked python` — one change
   fixes the 96 % timeouts and the container's only hard break; `lane_end_guard` through `uv run`;
   the fleet-health start hook still times out 41 % after the 4B split, so the target design must
   measure it in real sessions, not in isolation.
4. **Path layer and transport adapter, as the harness proposed:**
   - `ecosystem/transport-registry.yaml` — the DECLARE's table as data, with the missing kinds
     `GO-`, `LEDGER-`, `PLAN-`, and `-v<n>` + `supersedes:`; each row names writers, readers and an
     admission mode (none / shape / integrator);
   - `scripts/transport.py` — read / write / list by kind, two backends, refusing a writer not in
     the registry (the handback organ then cannot write `REFUSED-`);
   - `transport.admit()` — the four readers whose raw read becomes a durable fact switch first:
     lane digest, handoff preflight rows, decision carriers, the GO reader. ADR-121's event log
     consumes `admit()` output later, so this does not wait on the ADR.
   - **Ruling:** lane STATE lines live in the integrator receipt; the unread `StateLine` write in the
     handback organ is proposed for removal, with the operator's GO.
   - The portability check fails on `[A-Z]:\`, `$env:` and `powershell ` in scripts, hooks and
     templates; `gen_lane_contract` emits logical transport names; the `C:\Users\...` literals in
     `ecosystem/` become paths relative to a resolved dev root.
5. **Organs:** fix the instrument (count through import chains, hooks and moments); the six wirings
   — `handback` → lane-end, `lane_boot` → pre-launch, `plan_lint` → pre-launch, `block_commit_on_main`
   → the default pre-commit stage (core invariant #5 is inert today; test the integrator path first),
   the two ported hooks; fix the two stale `fates:` lines in `harness.yaml` (D1); **wire the existing
   `deny_and_point.py` instead of building a guard**; the two retirements only with GO.
10. **Tooling:** one contract grammar, the plan lint's, emitted by the generator and used by hand-written
    contracts; the lint reads `serialize-group:`; investigate the `codex-review` skill's 67.6 M tokens
    in 7 days; the 1 k tokens loaded twice from `CLAUDE.md` and `AGENTS.md` (a parity row); trim
    `MEMORY.md`.
11. **Night autonomy, from the night's findings:** a session janitor at batch close (finished
    sessions held about 7 × 400 MB); a Stop hook that refuses to end a lane without a machine
    HANDBACK line; a Copilot producer that runs as its own session, never as a dispatcher shell;
    Monitor children reaped on Windows; a post-merge check before push (a `--no-ff` merge commit
    bypasses pre-commit); `merge_receipt` records timed steps.

## §7 — wave 5c, added

- The devcontainer gains `pwsh`, `codex`, `agy` and `copilot`, each declared with an `install:` field
  in the provider registry and asserted by the container self-test.
- A container CI job reports the skip count by reason; a rising count is the regression signal.
- The Windows Task Scheduler routine moves to cron in the container or to the Actions schedule.
