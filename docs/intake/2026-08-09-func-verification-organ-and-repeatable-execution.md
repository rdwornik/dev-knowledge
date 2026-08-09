---
intake-id: 30
status: DRAFT
origin: "Layer-1 architect (predecessor seat), 2026-08-09 — consolidating the challenge answer `CHALLENGE-ANSWER-2026-08-09`, the operator directives of 2026-08-08/09, and the predecessor review; authored off-repo and filed verbatim by the ARC-3 hygiene close-out"
note: "BODY FILED VERBATIM — zero edits, zero births. The body's own header bullet still reads `intake-id: 30 (PROPOSED — verify next-free before filing)`; that check is now DISCHARGED and the id is 30, held in reserve for this document since intake #32 recorded 30/31 as RESERVED rather than free. The bullet is left unedited because the archival value of a verbatim filing outranks tidying a resolved parenthetical."
---

# The verification gap, repeatable execution, and the cost of parallelism

- **intake-id:** 30 (PROPOSED — verify next-free before filing)
- **Class:** functional · **Date:** 2026-08-09 · **Status:** DRAFT — triage at the batch-4 planning GO together with #28 and #29, ONE ratification batch
- **Author:** Layer-1 architect (predecessor seat), consolidating the 2026-08-09 challenge answer, the operator's directives of 2026-08-08/09, and the predecessor's own review
- **Provenance:** challenge answer `CHALLENGE-ANSWER-2026-08-09` (counts 🟢26/🟡6/🟠15/🔴8); operator observations 2026-08-09 (session length, cloud repeatability, development telemetry, Pylance workspace indexing); predecessor commentary as marked

## §A — Proposed ruling 1: an organ for HALF-LANDED RULINGS (the challenge's central diagnosis)

**Evidence (from the answer, six independent instances found by five lanes that never spoke to each other):** `markdown_it` ruled ADOPT, landed at 1 of 3 sites; `yaml.safe_load` ruled ADOPT, unimplemented six days on; two `LANE_BRANCH_RE` constants with different grammars disagreeing on 8 of 11 real merged branches; the intake area's two generator-carriers with one hooked; an ADR-archival bar existing only in a commit body; ADR-100's ruled-but-unbuilt index split. **The repo is excellent at ruling and has no organ that notices a ruling only half-landed.**

**Proposal:** every ruling that names an adoption or a mechanism carries a machine-checkable *landing predicate* (the file/symbol/site count that proves it landed), and a periodic organ verifies the set. Shape to be chosen at ratification against the library-first bar: a check in `audit.py` reading the rulings register · or the register gaining a `landed:` field validated by an existing validator. **Predecessor commentary:** this is the highest-value item in the whole answer — it is the meta-defect behind X-1, X-2 and X-8 alike, and it is the only proposal here that makes future rulings self-policing rather than adding another rule to remember.

## §B — Proposed ruling 2: REPEATABLE CLOUD EXECUTION (operator: "chmura musi być powtarzalna")

**Evidence:** the ADR-106 `uv` pin cannot be satisfied in a cloud container, so every `uv run --locked` hook entry refuses — no SessionStart digest, no self-arming, no Stop backpressure; witnessed independently three times in one night. Four lanes met the same condition and chose **four different answers** (replaced the binary · refused on ADR-106 grounds · committed with declared `--no-verify` · built a venv alongside). No ruling covers what a cloud lane may do to its own toolchain — that, not the cloud itself, is what makes night batches unrepeatable.

**Proposal, two legs, both required:** (1) a pin strategy that a fresh container can satisfy (`mise` or equivalent — ledger item 36, now evidence-backed rather than speculative); (2) a **cloud-lane contract clause**: the single sanctioned response to an unsatisfiable toolchain, the mandatory `--unshallow` before any history claim, declared-bypass form, read-mostly scope, zero merges to main, and re-gating locally at integration. **Operator's routing intent, recorded:** read-mostly lanes (audits, research, recon, evidence sheets) run in the cloud; gated mutations run locally — this is also the mitigation for §C.

## §C — Proposed ruling 3: PARALLELISM EXTERNALITIES on the operator's machine

**Evidence:** at ~10 worktrees the operator's editor reported an excessive source-file count (each worktree is a full checkout by design, so indexers see N copies), with a real correctness risk — an import resolving into a worktree copy instead of the primary. Handled same-day at the user-settings level (analysis excludes for `.claude/worktrees/`, venvs, mutants, caches; `openFilesOnly`). **The class is broader than one editor:** indexing, workspace search, `git status` latency, and disk footprint all scale with batch width, and none of them is measured or budgeted today.

**Proposal:** (1) name the class in the batch protocol — batch width has an operator-machine cost, and cloud routing (§B) is its release valve; (2) decide the durable form of the editor-hygiene config: **user-level** (fixes every repo at once, zero repo surface — the operator's machine is already covered) versus **per-repo via the doc-carrier** (fleet-universal, but requires a Folder Governance clause for the path before anything is authored — zero invented paths). Predecessor recommendation: keep user-level as the working fix, and ratify the carrier version only if the fleet gains other editor-shared settings, so a folder is not created for one file (the same objection the operator raised against `codex/` and `config/`).

## §D — Amendment pointer: DEVELOPMENT TELEMETRY (extends intake #29 S3a, no new intake)

The operator's stated purpose: *compare models and know whether development actually got faster.* #29 S3a currently scopes per-arc instrumentation; extend it to a **persisted per-day / per-window record**: rows opened and closed, test runs and failures, arc wall-clock per phase, model + effort used, tokens. Note the substrate already exists — the runtime records per-subagent side-files, timestamps, per-message model and token usage in the session transcript (verified against a live transcript), so this is extraction, not new plumbing. Acceptance: two consecutive windows of data before any optimization is designed (the [#511] discipline — the 30-minute handoff was 0.25% machinery).

## §E — Sequencing note (proposal, non-binding, for the batch-4 cut)

1. §B pin + cloud-lane clause — unblocks the whole night channel and relieves the operator's machine.
2. `[#505]` leg 1: contracts become committed repo artefacts (~10 lines) — precondition for anything that lints a contract.
3. Rule C refusal leg (intake #29's distiller shape) — ends the "knew the rule, nothing checked" family.
4. Seeded-defect corpus — the entry gate for Gemini `[#491]`, Grok `[#492]`, and the free-tier Copilot channel (CLI is available on the free plan but consumes a capped monthly premium-request allowance, so it is a probe-scale lane, not a workhorse — bake-off yes, standing fan-out no).
5. §D telemetry · 6. canonical `AGENTS.md` registered in `_SPEC_REGISTRY` (+ `templates/prompt-template.md`, same class, missing today) · 7. `pythonpath` Shape B rollout → mutmut · 8. gap-week evals (check-jsonschema, testmon, lychee) · 9. one-command onboarding by extending the doc-carrier manifest · 10. `[#493]` absence-of-run detection.

## Births

ZERO at filing (capacity law). Candidate rows at batch-4 planning, against demonstrated close capacity: §A landing-predicate organ · §B pin + cloud clause · §C editor-hygiene decision (may be a one-line disposition rather than a row) · §D telemetry extraction.

## Acceptance criterion

§A/§B/§C ratified or amended at the batch-4 GO; §D folded into #29 as an amendment; §E consulted at the cut and departed from only with a stated reason.
