# CONTRACT M — [#529] telemetry v1 EMIT (library only) — contract of record

**Provenance.** Frozen contract dispatched to lane M on 2026-08-15, transcribed here verbatim
under I-D3 (the contract a lane executed becomes a committed artifact, so the executed surface is
auditable after the prompt file is gone). Source: `$env:CLAUDE_PROMPTS_DIR\CONTRACT-M-529-telemetry.md`
(resolved live to `C:\Users\1028120\Downloads\CONTRACT-M-529-telemetry.md`).

- Lane: `M` · worktree `lane-m-529-telemetry-emit` · branch `worktree-lane-m-529-telemetry-emit`
- Row: `[#529]` (open, P1/M, theme `[E7]`, serialize-group `environment`)
- Dispatch: `[dk · #529 · telemetry-emit] Read and execute the frozen contract … — step 0 commits the
  contract of record; run /lane-boot from step 3 onward, commit-and-STOP.`
- T_start: `2026-08-15T14:33:27Z`

Everything below the rule is the frozen contract as received. It is not edited here; deviations and
decisions taken under the V-2 budget are reported in the end-of-arc packet, not by amending this file.

---

# CONTRACT M — [#529] telemetry v1 EMIT (library only) · worktree `lane-m-529-telemetry-emit`
**Purpose:** Stage-1 telemetry per the landed memo (`docs/archive/2026-08-14-research-usage-telemetry-design-wf-0e8cd658.md`) and intake #29 Fold A (contract-of-record): events `check_run` / `hook_run` / `blocker_fired`; SQLite WAL (`journal_mode=WAL`, `synchronous=NORMAL`, `busy_timeout=5000`) + structlog emit helper.
**SCOPE NARROWED (review 2a):** EMIT LIBRARY + TESTS ONLY. You do NOT touch `scripts/audit.py` or any dispatcher/hook script — wiring call sites is an explicitly owed phase-3 integrator step. Your library exposes a call surface the wiring step will consume; document it in the module docstring.
**OWNED-FILES manifest:** one new module under `scripts/` (derive the taxonomy-correct hyphen-free Python name from sibling modules and quote the pattern source in the commit body) + its test file under `tests/`.

## Common law (all phase-1 contracts)
| Model | Mode | Effort |
|---|---|---|
| per dispatch line | auto (zero design freedom beyond stated steps) | per dispatch line |
- Repo: .dev-knowledge (primary = operator's checkout; you are in your own worktree/branch).
- Read CLAUDE.md first. Gotchas: PYTHONUTF8=1 on console errors; manifest-first when closing rows; BACKLOG.md is GENERATED (edit tasks/ source + `python scripts/gen_task_tree.py --emit-source`); freshness-gated docs need a genuine full re-read before stamp moves; silent_rule_ratchet — phrase doc additions declaratively, no new must/shall/never tokens.
- Env: `uv sync --locked --group analytics` before anything (17/19 prior lane reds were this miss).
- Git: work ONLY on this lane's branch in this worktree; commit per step with the step name; NEVER merge, NEVER push main, NEVER --no-verify, NEVER SKIP=.
- T_start: first line of your packet records dispatch timestamp.
- Tiered suite law: targeted test files in-lane only; the full suite runs ONCE at batch integration, not here.
- Decision budget: decide per defaults and REPORT in one end-of-arc packet. STOP-and-report only for: (a) curated-baseline touches, (b) rule-vs-ruling conflicts, (c) a fork class with no standing ruling. Never drip questions.
- File discipline: step 0 prints your OWNED-FILES manifest; you modify NOTHING outside it (BACKLOG/manifest/audit-index regens excluded — regen-at-merge surfaces). Zero births of [#id]s. No register/STANDING_RULINGS edits unless your contract names them.
- Packet: ONE .md — T_start · manifest as executed · per-step commit shas · targeted-test evidence · deviations self-reported · final "STOPPED" line.
## What NOT to do (all lanes)
No merges · no pushes to main · no new ids · no new repo folders/paths (homes derive from quoted governance sources only) · no deleting content without an explicit contract step · no full-suite runs · no edits outside the manifest · no answering stop-hooks with new scope.

## UNDERSTAND
Problem: zero telemetry exists (baseline: no test_run duration emitted anywhere). Risk: wrong numbers worse than none. Failure mode: emitting plausible-but-false metrics.

## Steps
1. COMMIT — schema + writer: SQLite WAL store with the three Stage-1 event types, structlog emit helper. Row fields per the memo's Stage-1 spec (read it; row-is-the-spec via [#529]).
2. COMMIT — correctness constraints (N-15, binding): any git-history-derived metric asserts `git rev-parse --is-shallow-repository == false` and REFUSES to emit on shallow; per-organ coverage values it cannot statically resolve emit `unknown`, never `0`; skip counts emit WITH the host capability vector (git/grep/pre-commit/powershell/pandas presence), never bare.
3. COMMIT — tests: WAL concurrency smoke, refuse-on-shallow, unknown-not-zero, capability-vector shape. Targeted run of your test file only.
4. Packet: call-surface doc for the phase-3 wiring step + which memo lines each event maps to. STOPPED.

---

## OWNED-FILES manifest as declared at step 0

| File | Status | Derivation |
|---|---|---|
| `scripts/telemetry_emit.py` | new | `<domain>_<role>` snake_case, matching the sibling modules `fleet_analytics.py`, `enforcement_coverage.py`, `window_metrics.py`, `desired_state_loader.py`, `journal_anchor.py`. Hyphen-free because `pyproject.toml` `[tool.pytest.ini_options] pythonpath = [".", "scripts", "deploy"]` puts `scripts/` on `sys.path` so "a test file imports `audit` / `tool` / `carrier_precommit` **by bare name**" — a bare-name import requires a valid Python identifier. |
| `tests/test_telemetry_emit.py` | new | `tests/test_<module>.py`, the repo-wide pairing (`tests/test_fleet_analytics.py`, `tests/test_preflight_contract.py`, …). |

Regen-at-merge surfaces touched outside the manifest, per the contract's own exclusion:
`docs/audits/README.md` (audit-index regen) and, if the doc-claim counters move,
`scripts/gen_doc_counts.py --write` output.

**Explicitly NOT touched:** `scripts/audit.py`, any hook or dispatcher script, `pyproject.toml`,
`uv.lock`, `BACKLOG.md`/`tasks/529-*.md` row state, `.gitignore`, `CLAUDE.md`, `ARCHITECTURE.md`.
