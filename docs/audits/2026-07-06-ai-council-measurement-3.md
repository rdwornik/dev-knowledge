# ai-council consumer measurement #3 — FULL-COVERAGE (Wave-3 STEP-3 closure evidence)

**Date:** 2026-07-06 · **Lane:** Wave-3 priority-#1, STEP 3 (re-measure after root-ruled instrument hardening)
**Instrument:** `observe-arc --consumer` on hub `main` @ `80fbaa9` (G1+G3+G2+G4 batch `8b9fe3e` + G7 `80fbaa9`) · oracle = hub manifest v1.2.0
**Consumer:** `C:\Users\1028120\Documents\Dev\ai-council` @ `5c81e71` (unchanged all day — **zero ai-council commits, zero deploy-pipeline changes**; the consumer was measured, never modified)
**Child:** claude-sonnet-5, claude-code 2.1.200, headless, isolated config

> Immutable audit record. Companion to `2026-07-05-ai-council-measurement-2.md` (the STOP-1 before-run) and `2026-07-06-codex-consumer-instrument-hardening.md` (the batch review, 0 CRIT / 4 HIGH fixed pre-merge).

## Final result (fresh clone, canonical CLI)

- **GATE-0 isolation PROVEN** (`provenance=True outer-absent=True exit-ok=True controls=[fleet],[changelog],[closures]`)
- **COVERAGE: 4-of-6 FIRED + 2 armed-but-skipped; tombstones ok — VERDICT: FULL-COVERAGE, exit 0**

| Component (stage) | Verdict | Verbatim evidence (hook stdout) |
|---|---|---|
| propose-closures-stop-hook (stop) | **FIRED** | `propose_closures: 0 strong, 0 weak over 400 commit(s) -> PROPOSALS-2026-07-06.md (weak suppressed: cold start)` |
| floor-sessionstart-guard (session-start) | **FIRED** | `pre-commit installed at .git\hooks\pre-commit` |
| session-end-backpressure (stop) | **FIRED — BLOCKING** | `Session-end gate BLOCKED (deterministic; ADR-85) — repair before stopping:` |
| canonical-freshness (pre-commit) | **FIRED** | `canonical_freshness last_reviewed gate (A2 FAIL blocks the commit).......Passed` |
| hub-toc-hooks (pre-commit) | ARMED-BUT-SKIPPED | `TOC freshness (markdown doc vs its own headers)......(no files to check)Skipped` |
| floor-hash-verify-hook (pre-commit) | ARMED-BUT-SKIPPED | `Verify CLAUDE-FLOOR.md matches its sha256 sidecar....(no files to check)Skipped` |
| ruff-gate tombstone | CORRECTLY-ABSENT (non-vacuous: pre-commit genuinely ran) | — |

Observed-not-gated: `review-closures-command` **OBSERVED** (the ≥1 command act happened), `override-command` OBSERVED (consistent with the child clearing the blocked Stop via the deployed `/override` escape hatch — plausible, not verified from the discarded transcript), `tier1-lifecycle-plugin` OBSERVED (settings declaration, exact-JSON probe), `methodology-floor` OBSERVED; `codex-agents-config` NOT-OBSERVED (machine-level, honestly unprobeable from a clone), `ship-command` NOT-OBSERVED (the arc never ships — correct).

**Enforcement highlights:** the ai-council-deployed `session_end_backpressure` gate **actually blocked** the child's stop (the strongest witnessable form of enforcing), `canonical_freshness` executed on the arc commit, and the tier1 Stop hook produced real proposals output over the consumer's own 400-commit history. The two ARMED-BUT-SKIPPED hooks are wired and consulted; their file scopes (`COUNCIL_QUESTION_GUIDE.md`, `CLAUDE-FLOOR.md`) are simply not touched by the arc's single-file commit — follow-up [#267] covers witnessing them FIRED via a scope-exercising arc extension.

## Before / after (the priority-#1 delta)

| Run (instrument state) | GATE-0 | Coverage | Child behavior |
|---|---|---|---|
| 2026-07-05 Block B (pre-#253 instrument) | PROVEN | nominal 1-of-6, real ~0 (narration leak) | refused ×2 / permission-stalled |
| STEP-1 ×2 (fixed observer, pre-hardening) | PROVEN | 1-of-6 honest | refused as injection, zero tool calls |
| STEP-3 pre-G7 ×2 (G1–G4 batch) | PROVEN | 3-of-6 | worked; refused to bypass the broken gate (asked) |
| **STEP-3 final (G1–G4 + G7)** | **PROVEN** | **FULL-COVERAGE (4 FIRED + 2 armed-skipped), exit 0** | completed the arc through the armed gates |

Every gap between 1-of-6 and FULL-COVERAGE was **instrument-side** (G1 permission seam, G3 authorization channel, G2 plugin reachability, G4 verdict fidelity, G7 sandbox environment fidelity). **ai-council's deployed mesh needed zero changes** — the measure-first ruling is vindicated: the consumer was healthy; only the measurement could not see it.

## Run ledger (this lane, 5 live runs total)

1. STEP-1 run 1 (CLI) + run 2 (verbatim retention driver): 1-of-6, exit 2 — refusal wall, evidence in measurement-2 audit.
2. STEP-3 run 1 (CLI) + run 2 (retention driver): 3-of-6, exit 2 — G7 witnessed: ai-council pins `repo: ../.dev-knowledge` (relative path) in `.pre-commit-config.yaml`; unresolvable beside a temp-dir clone, pre-commit errors before any hook. Child (verbatim): *"the failure is an environment artifact — `../.dev-knowledge` isn't a valid repo in this sandboxed clone"* — and it **declined to self-authorize `--no-verify`**, its `stash`/`cat` remediations were correctly permission-walled (`permission_denials` recorded). The Codex-narrowed allowlist held under live fire.
3. STEP-3 final (CLI, fresh clone): FULL-COVERAGE, exit 0 (above).

## Honest limits & findings (standing)

- **ARMED-BUT-SKIPPED ≠ FIRED**: proven wired + consulted; not proven to execute/block on a matching file. [#267] filed.
- **Harness-mirrored state, disclosed**: plugin presence seeded from the hub checkout (G2, gated on the consumer's own `enabledPlugins` declaration), hub pre-commit source mirrored beside the clone (G7). Both mirror what exists on the operator machine; what is measured is the firing.
- **G5 resolved by the real arc**: `session-end-backpressure` is not silent-success on ai-council — it FIRED blocking. The silent-success honest-limit class no longer applies to this component here.
- **ai-council-owned finding (ADR-41 pointer, filed in its dedicated session, not here):** the relative-path pre-commit source (`repo: ../.dev-knowledge`) makes ai-council's gates layout-dependent — any checkout outside `Dev/` (CI, second clone, another machine) silently loses the toc-freshness gates the same way the sandbox did. Worth an ai-council-side decision (pin by URL+rev, or document the layout constraint).
- **G7's mirror runs pre-spawn and unconditionally** for any relative `repo:` path in the consumer's config; a future consumer with a HUGE relative dependency pays a clone. Acceptable at n=1 fleet scale; revisit at rollout (#221 territory).

## Closure claim (for root — STOP-POINT 2)

The ex-ante objective: *"a consumer measurement with the FIXED instrument shows every deployed-mesh component ENFORCING on ai-council (FIRED under the real arc), or every gap is named, closed VIA THE DEPLOY PIPELINE, and a re-measure confirms it."*

Measured state: 4 of 6 FIRED under the real arc; the remaining 2 are armed + consulted with their non-firing fully explained by file scope (named, tracked [#267]); tombstone conformance proven; zero consumer gaps required the deploy pipeline. Two recorded runs before/after + coverage figures: this audit + measurement-2. The repeatable onboarding process: `templates/consumer-onboarding-runbook.md` (proposed home — root names the final one). **Root declares closure or names what's short.**
