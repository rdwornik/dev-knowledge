# Lane W-2' — the prompts guard fails closed, and proves it evaluated

<!-- scope: meta -->

**Lane** `lane-w-684-pretooluse-guard-root` · **Row** `[#684]` · **Batch X, wave 1, slot 6**
(AX15-3) · **Contract** `LANE-w-684-pretooluse-guard-root-prime.md`, frozen 2026-09-11 ·
**Branch** `worktree-lane-w-684-pretooluse-guard-root`, CONTINUED per AX15-3 rather than
re-cut.

This is the W-2' end-of-lane packet. It supersedes nothing:
`2026-09-11-technical-lane-w-684-pretooluse-guard-root.md` is W-2's own artifact and stands
as written. This one records the continuation that **inverted W-2's central design
decision** — which is why the two disagree on the merits, and why the disagreement is
recorded rather than smoothed over.

## 1. The one-sentence change

The guard used to PERMIT whenever it could not run; it now REFUSES, every refusal names its
cause and its fix, and a permit requires positive proof that the guard actually evaluated.

## 2. Commits

| SHA | What |
|---|---|
| `1372dbb2` | step-0 sync — `origin/main` merged into the lane |
| `c743ab50` | AX12-1 — the batch-X clauses written into row `[#684]`'s own body |
| `0c974eb0` | RED — 18 witnesses for the fail-closed inversion |
| `4cbee3ab` | BUILD — fail closed on every inability to evaluate; floor coupling (AX15-2) |
| `62b2e3f0` | RED — 5 witnesses for the three findings of review round 1 |
| `a17e702a` | BUILD — positive proof of evaluation; the coupling binds |
| `d668bb42` | RED+BUILD for rounds 2 and 3; the refusal marker; this packet |
| *(this)* | RED+BUILD for round 4 — script-operand binding, per-hook implication |

Footprint, all six commits: `.claude/settings.json`, `scripts/fleet_health.py`,
`scripts/fleet_parity.py`, `ecosystem/parity-surfaces.yaml`, `ecosystem/doc-counts.md`,
`tasks/684-*.md`, and three test modules. Nothing outside it.

## 3. Done-contract reconciliation

**Clause 1 — fail closed on every inability to evaluate, refusal names cause and fix,
SessionStart preflight.** Met. The matched class is unchanged (the narrowed matcher stays);
`PROMPTS_UNSET` and `PROMPTS_NO_USER_SCOPE` stay PASSING, because AX15-1 enumerates
inability to EVALUATE and a guard that ran with nothing to compare has evaluated — widening
to those would refuse every consumer that never set the variable.

**Clause 2 — two RED-first trip-tests, M7 smoke, fresh Codex review with no unresolved
HIGH.** Met, at the cost of three review rounds; see §4. Per AX15-2 the hook and
`scripts/fleet_health.py` ship as ONE floor component, enforced by a new
`settings_hook_script` probe rather than by two independent rows — two rows would assert
each half separately and make the script mandatory in repos carrying no hook.

**Clause 3 — English, hyphen-only names, logging not print, Click where warranted, pytest
green.** Met. `print` in the guard leg is deliberate and unchanged: a PreToolUse hook's
contract IS its streams, and the marker on stdout plus the refusal on stderr is the
interface, not incidental output.

## 4. What was measured

**The hook command, on nine paths through a real POSIX shell** (`bash.exe`), each measured
BEFORE the string was written into `settings.json`, and the shipped string read from the
probe file so that what ships is byte-identical to what was measured:

```
guard passes, stdout == OK marker      -> 0
guard refuses, stdout == REFUSE marker -> 2  its own message, verbatim, unchanged
BARE exit 2 (shim, no marker)          -> 2  Cause: not the guard's verdict
exit 0, NO marker                      -> 2  Cause names the marker and rc=0
SILENT shadow python                   -> 2  Cause names the marker
DECOY shadow python                    -> 2  stdout merely CONTAINING the marker
no root resolves                       -> 2  Cause names CLAUDE_PROJECT_DIR and cwd
no python on PATH                      -> 2  Cause "no usable 'python' on PATH", rc=127
guard crashes (rc=1)                   -> 2  Cause "crashed ... import or syntax error"
```

Every refusal quotes back the stdout it actually saw, so the reader gets the evidence
rather than a verdict about it.

**The live seat, before arming and again after each change.** The real guard exits 0
printing only the marker; the shipped command run through `bash` from the repo root exits
0. Both `CLAUDE_PROMPTS_DIR` scopes agree here, so the fail-closed leg could not wedge this
seat the way the 2026-09-06 `"*"` matcher did.

**The fleet, before and after the coupling was tightened.** Identical:
`190 at-parity, 0 MUST-absent, 0 refused` across all surfaces, 3 repos walked. A tightened
probe can only ADD findings, so an unchanged tally is the evidence that it binds the hub's
own hook rather than merely passing it.

**Codex, three rounds**, `gpt-5.6-terra`, each against the live diff:

| Round | Verdict | Disposition |
|---|---|---|
| 1 (at `4cbee3ab`) | HIGH:2 MED:1 | all three FIXED (`62b2e3f0` + `a17e702a`) |
| 2 (at `a17e702a`) | HIGH:2 MED:0 | both FIXED (`d668bb42`) |
| 3 (at `a17e702a`) | HIGH:3 MED:0 | two FIXED (`d668bb42`); one DISPOSITIONED, below |
| 4 (at `d668bb42`) | HIGH:2 MED:0 | both FIXED; the disposition ACCEPTED by the reviewer |
| 5 (at `25ea70ab`) | HIGH:1 MED:0 | FIXED — a variable's LAST assignment before the call |

**Round 4 closed the disposition explicitly.** Asked to attack the argument rather than
restate the finding, the reviewer answered: *"The exact-marker shim argument holds: without
a portable trust anchor outside PATH/repo control, it is not a distinct defect from
controlling the real interpreter's answer. Do not re-report it."* So the one unfixed
finding is resolved on the record by the reviewer, not merely asserted by the lane.

Its two NEW findings were both real and both fixed: `python -c '<program>'` naming the path
in its source was read as invoking the guard (the script is the interpreter's EFFECTIVE
script operand — the first non-option word — and `-c`/`-m` mean there is none), and
`hook_bound` used `any`, so one compliant hook masked a second token-bearing hook pointed
at another guard (it is `all` now: the implication is per carried hook, because each
refuses tool calls on its own). A `uv run --locked python <script>` witness was added at
the same time, because every other hook command in this repo runs under `uv run` and a
binder that only understood a bare `python` would call the repo's own doctrine a defect.

**Round 5** found one more, and it is the one that best justifies open item 3: `assigned`
recorded a variable if ANY assignment mentioned the path, so
`g=".../fleet_health.py"; g="/opt/other_guard.py"; python "$g"` certified a hook running
the other guard. Asked explicitly whether this was real drift or a constructed decoy, the
reviewer judged it *"a plausible deployment-drift shape"* — correctly: this repo's own hook
already assigns `g` TWICE (the resolve and the cwd fallback), so a third assignment
re-pointing it is the shape the mistake actually takes. Assignments are now replayed in
order and a variable is worth what it holds AT the invocation.

Eleven of the twelve findings were FIXED, none waved away. Several were arguably outside the
guard's threat model — anyone who can place a shim on `PATH` can also edit `settings.json`
— but each fix was cheap, and "declared enforcement without enforcement" is the precise
thing this row exists to end, so arguing the threat model would have answered a different
question than the one AX15-1 asked.

**The one DISPOSITIONED finding, and why it is not a judgment call.** Round 3 asks that a
`python` shim printing exactly `PROMPTS-GUARD-EVALUATED-OK` and exiting 0 be prevented from
permitting, "using a mechanism a substituted interpreter cannot forge". No such mechanism
exists here. The hook's only channel to the guard is an interpreter that `PATH` selects, so
any bytes the real guard can emit a substitute can emit too; a challenge-response needs a
secret the verifier does not hand to the prover, and the hook hands the prover everything —
the substitute can read `fleet_health.py` and `settings.json` itself. Pinning an absolute
interpreter path would defeat it and also defeat every consumer, whose own `python` is the
one that must run. The finding is also moot at its own premise: whoever controls that
`python` controls the guard's answer outright, and the guard exists to catch a STALE
DIRECTORY — a configuration mistake — not a local adversary.

What exists instead is DETECTION, and it was already there: the SessionStart preflight
prints the ABSOLUTE path of the interpreter it resolved *through the hook's own PATH*
(`hook_path` strips the venv `uv run` prepends, so it measures what PreToolUse will see).
A shadowed `python` is therefore visible at boot, by name. That is the honest answer —
detect and report, not prevent — and it is recorded in `.claude/settings.json`'s comment so
the next reader does not re-litigate it.

**The two findings that were REFUSED on the merits**, both from earlier rounds and both
recorded in code rather than only here: `EnterWorktree` / `ExitWorktree` were proposed for
the matcher and declined, because they are the break-glass family — gating the DESTINATION
of the `ToolSearch` escape route defeats the route as surely as gating the route itself.

## 5. Proposed diffs the lane did NOT make

**The `version:` bump in `ecosystem/parity-surfaces.yaml`.** Adding the coupling row is a
spec edit that `coherence-nudge` correctly flags. The bump is NOT made here: it REDs
`check_reconciled_versions` for dependents outside this lane's write scope, and
`audit-health` is a pre-commit gate — so the bump would block this lane's own commit and
the repair would touch files it may not write. Filed as one candidate for the integrator:
*bump `version:`, then re-stamp the dependents the bump REDs.*

**The manifest entry that would make the hook block REACH a consumer.** AX4-1 names the
owner in the same breath as the duty: *"Owner: `decision_coverage` lane (X1-1) gains this
clause; the parity registry is the carrier."* Which repos the hook block reaches is that
carrier act and it is X1-1's row. This lane lands the CHECK and declares `floor: MUST` on
`[#684]`; it adds nothing to `deploy/manifest-v1.5.0.yaml`. The coupling is correct in
either order, which is the property that lets the two land independently.

**`ecosystem/organ-index.md` was NOT regenerated**, and the bypass is declared in every
commit body that needed it. The staleness is INHERITED FROM MAIN — `origin/main`'s copy
carries the retired `/override` row and the 65-vs-64 count that follows, on a repo where
`origin/main` no longer tracks `.claude/commands/override.md`. Regenerating here would
absorb main's drift into a lane commit; the integrator is gate-of-record.

`ecosystem/doc-counts.md` got the OPPOSITE treatment — regenerated, not bypassed — because
that staleness is PRODUCED BY THIS LANE (it adds tests). The two generated files are
treated differently on purpose, and the reason is which tree produced the drift.

## 6. Open items

1. **The `version:` bump and its dependent re-stamps** — §5, for the integrator.
2. **The X1-1 carrier act** — §5. Until it lands, the coupling row is armed but the hook
   block reaches only the hub.
3. **`hook_invokes_script` is a heuristic, not a shell parse**, and says so in its own
   docstring. A parity walk reads strings and must not execute what it reads (ADR-28/36).
   It cannot resolve a variable assigned from another variable, a path built by
   substitution, or one supplied by the environment — each of which reports a compliant
   hook as a SPLIT, which is the safe direction to be wrong in: a finding gets read, a
   silent pass does not. A `sh -c "..."` wrapper would still defeat it.
   **FIVE review rounds each found another shape it mis-read** (`; : path`; `echo python
   path`; `python -c '...path...'`; `any` over sibling hooks; a reassigned variable). That
   convergence is itself the finding, and it is the strongest recommendation this packet
   makes: a string heuristic over arbitrary shell has no natural stopping point, and each
   round's fix was correct without making the next round less likely. **Proposed to the
   integrator:** constrain what a prompts-guard hook command may LOOK like — a declared
   shape parity can check exactly — instead of continuing to teach a parser to read shell.
   The lane did not do this, because it would change the deployed hook's contract for every
   consumer, which is a carrier decision and not this row's to take.
4. **The M7 smoke's CLI leg remains externally blocked.** The shell-level property is
   measured green both ways (good tree → 0, broken tree → 2 with the teaching message).
   The CLI leg is not re-run: `cursor-agent` is usage-limited, and `codex` v0.153.4 is the
   same binary W-2 measured as NOT honouring `.claude/settings.json` — re-running it would
   be vacuous rather than confirmatory. Recorded as a limit, not as a pass.
5. **Exactness on stdout is deliberately brittle in one direction.** Any future `print` on
   the guard's pass path refuses every matched tool call. `test_prompts_guard_passing_says_
   so_on_stdout_and_stays_silent_on_stderr` pins the contract, so the break surfaces at
   commit time rather than at tool-call time — but a reader adding output there should know
   the cost before they do.

## 7. What a later reader should not re-derive

The fail-open argument was careful and it LOST on a different axis than it was made on. It
reasoned — correctly on its own terms — that a guard which bricks every tool call because
its interpreter is missing is worse than the stale directory it guards, and MA-1 was
exactly that failure. AX15-1 answers: *"a guard that permits when it cannot run is declared
enforcement without enforcement."* Both halves of the losing argument are kept in full in
`scripts/fleet_health.py`'s wiring block and in the wiring test's module docstring,
because a reader who cannot see the argument will make it again.

What PAYS for the inversion, and may not be removed without re-opening the ruling: the
matcher stays narrowed so the break-glass family is ungated; every refusal names cause and
fix; and the SessionStart preflight checks interpreter + script once at boot, so a per-call
refusal is the exception rather than the first news.
