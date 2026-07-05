# Consumer onboarding runbook — measure → complete → re-measure

<!-- scope: llm -->

> The repeatable process for proving the hub methodology ENFORCING (not merely present)
> on a consumer repo, distilled from the first real onboarding (ai-council, 2026-07-05/06:
> `docs/audits/2026-07-05-ai-council-measurement-2.md` + `2026-07-06-ai-council-measurement-3.md`).
> Secondary guidance per ADR-92 — the deploy TOOL remains the deploy mechanism; this runbook
> governs the measurement loop around it. Proposed home: `templates/` (root may rename).

## Preconditions

- Hub checkout clean at the methodology version under test; `deploy/manifest-v<X>.yaml`
  carries `engages:` triples (the oracle).
- Funded `ANTHROPIC_API_KEY` reachable (env, or `DEV_SECRETS_ENV` pointing at the .env).
- Consumer repo locally present, committed state = what you intend to measure (the harness
  clones committed state only; it NEVER mutates the real consumer).
- `claude` CLI on PATH. Sonnet child is the default (never Opus-by-inheritance).

## Step 1 — MEASURE (as-is baseline)

```
PYTHONPATH=deploy python -m lived_sandbox.cli observe-arc --consumer <repo-path>
```

- Record: GATE-0 verdict, per-component FIRED / ARMED-BUT-SKIPPED / EXPECTED-BUT-SILENT /
  tombstone state, coverage n-of-6, verbatim evidence lines, exit code (0 full / 1 gate
  failed / 2 fail-by-coverage).
- **GATE-0 FAILED → STOP.** The measurement is untrusted; never diagnose coverage numbers
  off a facade.
- Ambiguous silences? Re-run once (retry ×2 cap). If attribution still needs the child's
  transcript (the CLI tears it down), replicate `run_consumer_arc` verbatim through the
  harness primitives with evidence retention — same semantics, transcript kept.
- Write the measurement audit to `docs/audits/YYYY-MM-DD-<consumer>-measurement-N.md`,
  commit via branch + `--no-ff` merge. **STOP: report coverage + gap list to the
  architect/root. Do not start completion — the root rules the scope.**

## Step 2 — ATTRIBUTE, then COMPLETE (only root-approved gaps)

Attribute every silence to exactly one class before fixing anything:

- **Consumer mesh gap** (component genuinely absent/inert in the consumer) → close **via
  the deploy pipeline only** (carriers, deployed-versions record, version stamps) — never
  a hand-copy; commits land in the consumer through its own gates.
- **Instrument gap** (the harness cannot see or reach what exists) → hub-side fix in
  `deploy/lived_sandbox/**` + tests, feature branch, normal gates. Trust-seam changes
  take a heterogeneous review (Codex), CRIT/HIGH fixed pre-merge.
- **Honest limit** (fires but unobservable — silent-success class) → record it; don't
  force it.

Attribution patterns witnessed at n=1 (check these FIRST on a new consumer):

1. **Refusal wall**: a floor-carrying child treats prompt-asserted authority as injection
   (and it is right to). Authorization must ride the OWNED-CONFIG channel — the harness
   seeds the sanction as the isolated profile's user-level CLAUDE.md + the scoped
   permission allowlist (`arc_isolated_config`); the prompt only references it.
2. **Untrusted-workspace wall**: the sandbox clone's own `settings.local.json` allows are
   IGNORED (`hasTrustDialogAccepted` absent). Only user-level seeded rules count headless.
3. **User-level state the isolated config can't reach**: plugins live in outer `~/.claude`
   on a real machine — seed from the hub checkout, GATED on the consumer's own
   `enabledPlugins` declaration (never manufacture presence).
4. **Layout-dependent consumer config**: a relative-path pre-commit source
   (`repo: ../<hub>`) resolves on the operator machine, not beside a temp-dir clone —
   the harness mirrors it at the same relative position (`mirror_relative_precommit_sources`);
   also file the fragility back to the consumer (any CI/second checkout hits it too).
5. **Name-echo ≠ execution**: pre-commit prints hook NAMEs even when Skipped — the
   observer's ARMED-BUT-SKIPPED / VACUOUS verdicts exist for exactly this; never read a
   skip line as FIRED, never read tombstone absence on a commit-less run as conformance.

## Step 3 — RE-MEASURE (fresh clone) + closure evidence

- Re-run Step 1's command on the final instrument/consumer state. The before/after
  coverage delta + two recorded runs are the closure evidence.
- Record: measurement audit N+1 (immutable), BACKLOG file/close per the closure loop,
  JOURNAL entries (hub always; consumer only if the consumer actually changed).
- **STOP: final report** — both coverage tables, deploy records (or "zero deploy changes
  needed" — a valid and important outcome), evidence SHAs. The root declares closure.

## Invariants (hold at every step)

- Measurement is the deliverable: FAIL-by-coverage on a partial mesh is a CORRECT verdict,
  never forced green. Exit 2 is a result, not an error.
- The real consumer repo is never mutated by measurement; sandbox teardown leaves no
  residue (blast-radius-guarded temp roots only).
- Harness-seeded state is disclosed in the report; what is MEASURED is firing.
- No gate weakening anywhere — the allowlist stays scoped to the arc's exact operations
  (no `--no-verify` path), and a child declining to bypass a failing gate is the
  methodology WORKING, to be recorded as such.
