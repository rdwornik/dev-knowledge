# ADR-92: Methodology-deployment process doctrine (deploy-runbook)

<!-- scope: meta -->

**Status:** Proposed
**Date:** 2026-06-29
**Decision tier:** Doctrine (the deployment *process* that writes the per-repo version record ADR-91 built the read-side for — a deterministic, versioned, verification-gated deploy tool). Records the architect's distilled design across two AI-Council debates; **the operator ratifies by merge** (this ADR is not self-accepted). **Doctrine only — the deploy tool, the carrier manifest, and the carrier implementations are deliberately NOT built here** (separate later steps).
**Deliberation basis:** two 2026-06-29 AI-Council `pick` debates (4-model panel — claude-opus-4-7, deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.3; openai synthesizer; 2 rounds each) decided the process **form** and **scope**, plus the architect's reconciliation of the Council security points against the Layer-2 boundary. The motivating failure: a prior plugin deploy to `ai-council` silently omitted a carrier (a lint/ruff gate), discovered later.
**Related:** ADR-91 (methodology corpus versioning — this doctrine is the *writer* that ADR-91's read-side `ecosystem/deployed-versions.yaml` + `deployed_methodology_version` check await); ADR-54 / ADR-78 / ADR-28 / ADR-69 (the Layer-2 "hub does not write into sibling repos" boundary this process must preserve); ADR-70 / ADR-73 / ADR-78 / ADR-79 (the carrier set a deploy spans — global L0 config, the `tier1-lifecycle` plugin, pinned pre-commit hooks, the per-repo floor); ADR-71 (the pre-commit `repo:/rev:` consume-pin a deploy updates); ADR-88 (file-oriented dependency management — *do-not-build-is-doctrine*; the deferred tool/manifest are declared-not-built edges).
**Decommission:** none.
**Source:** the two Council transcripts (Evidence, below) + the architect's distilled decision and reconciliation.

## Context

Methodology is now versioned (ADR-91: semver + a git-tag release marker; baseline `v1.0.0` tagged). `ecosystem/deployed-versions.yaml` records each repo's deployed methodology version, and the **read-side** is built — the registry slot, the reader audit check `deployed_methodology_version`, and its `fleet_health` surface. The **writer** — the process that *populates* that field at deploy time — is unbuilt. The writer **is** the deployment process. Until it runs, every repo's field stays `null` and the reader reports `n/a` (the expected pre-deploy state).

Two AI-Council debates (form + scope, transcripts in `docs/decisions/transcripts/`) decided how that process is structured, invoked, and scoped. The empirical anchor is a real failure: in a prior plugin deployment to `ai-council`, one carrier (a lint/ruff gate) was **not** applied and was discovered only later — a silent partial deployment. Both Council verdicts converged on the same root-cause framing: *the prior miss was a verification gap, not a process-form gap* — so the fix is per-carrier post-application verification gating the version-record write, in whatever form the process takes.

**Scope note — threat model.** Heavyweight adversarial-agent defenses (the "zero-trust local state / AI agents are supply-chain attackers" framing some panelists pressed) are **out of scope**. The solo operator controls all repos and the AI agents in them are the operator's own Claude Code sessions — collaborators with write access, not attackers. The design is chosen for **determinism and correctness**, not threat-hardening. (Both synthesizers flagged the zero-trust framing as overstated for this scale.)

## Decision

**Build the deployment process as a deterministic, versioned, verification-gated deploy tool, operator-run from the trusted hub context, applying carriers in the consumer and writing the version record in the hub.** Doctrine recorded here; tool/manifest/carriers built later.

1. **Form = a deterministic deploy tool (script), not a pure Claude Code slash command.** Verification must run in a deterministic runtime, not inside an LLM session that could misreport success. Claude Code is shelled out to **only** for the plugin carrier (the one non-scriptable step); its result is **verified deterministically** (e.g. a file check of the consumer's plugin settings), not trusted from the session's self-report. *(Council form debate, Disagreement #2: "deterministic script orchestrator" was the stronger side — an LLM-mediated command is not a reliable substrate for truthful status reporting.)*

2. **The tool is versioned with the methodology.** It ships at the methodology tag, so deploying `vX` uses `vX`'s deploy logic and carrier set. This resolves the chicken-and-egg as carriers evolve: the deploy logic for a release is exactly the logic that release shipped.

3. **Operator-run, two phases — consumer phase (carriers) then hub phase (record).** The precise Layer-2 write boundary is **not** the binary "write-into-sibling XOR emit-for-consumer" this ADR originally posed; the read-only verify (2026-06-29) resolved it to a **three-edge** boundary — **write-yes, commit-no, autonomy-no**:
   - **(i) Autonomy-no.** No autonomous / scheduled / hook-initiated cross-repo writes from the hub; writes are **operator-invoked at a rollout moment** only (ADR-78 Decision 2).
   - **(ii) Write-yes.** An operator-run tool **MAY write carrier bytes directly into the consumer's working tree** — this is the ADR-78-blessed precedent: `generate_floor.py --out-dir <child>` already writes the floor + `.sha256` into the sibling's tree. So `apply(target)` **need not be emit-only**; it may write (or stage) directly.
   - **(iii) Commit-no.** The **commit stays in the consumer's own context** — the tool writes/stages but does **not** commit in the sibling.
   - **Hub phase** — the version record is written in the **hub** context; the consumer **never holds hub-write credentials** (no consumer→hub writes).
   *(This refines, not contradicts, the original intent — "carriers applied and committed in the consumer's own context": the byte-write may be operator-bridged, but the commit stays consumer-context. Evidence: ADR-78 Decision 2 + `scripts/generate_floor.py`. The architect reconciliation is unchanged — the two Council security points and our Layer-2 invariant are different axes: **consumer↛hub** (form debate Disagreement #3) and **hub↛sibling** (ADR-28/54/69/78), both satisfied by this operator-bridged split. The synthesizer's "run the orchestrator from the trusted hub/operator context" lands the same place.)*

4. **The hub version-record is committed on a branch; the operator ratifies by merge** (not auto-commit). *(Council form debate, Disagreement #4: branch-and-merge beat auto-commit — at ~5 repos the cost is trivial and the audit checkpoint is real.)*

5. **Scope = full-reconcile-to-target, single repository per invocation.** Not incremental-by-version-delta (delta needs trustworthy current-version state + migration paths that do not yet exist, and stays untested at this cadence); fleet-batch is deferred (single-repo contains blast radius; a shell loop gives fleet behavior when wanted). *(Council scope debate: Q1 full-reconcile, Q3 single-repo — strong consensus.)*

6. **Per-carrier `detect / apply / verify`, with a `--force` unconditional-re-apply escape hatch.** Not skip-if-present (tolerates drift — the observed failure: plugin present, lint gate missing), not blind overwrite (destructive, and destroys the drift signal). Detect-and-reconcile is the only model that both surfaces drift and converges it; `--force` exists for the critical-security-fix case where detection should not be trusted. *(Council scope debate, Q2: per-carrier detect/reconcile/verify was the stronger side, narrowly — minimal + deterministic detection paired with post-apply verify, plus the `--force` escape hatch from DeepSeek's revised position.)*

7. **A versioned carrier manifest per methodology tag** declares the complete carrier set, order, and per-carrier target state. (The manifest itself is built later — without it, "full reconcile" is underspecified; both synthesizers flagged the missing manifest as a blind spot to close at build.)

8. **Carrier contract:** each carrier implements `detect(target)` / `apply(target)` / `verify(target)`. The current carriers (global L0 config, the `tier1-lifecycle` plugin, pinned pre-commit hooks, the per-repo floor) are implemented **hand-written against a tiny interface — no plugin-loader, no DSL** (avoid over-build; ship the four hard-coded carriers, extract a framework only if carrier count later forces it).

9. **Core principle — per-carrier verification gates the version-record write.** The registry reflects **verified reality, not intent**. Structured per-carrier output (`detected state | action | result | verification`). `--dry-run` prints the plan. The registry is updated **only on full success**; on partial failure it is left unchanged and the per-carrier outcome is reported. `verify()` should not share a code path with `detect()` (orthogonal logic avoids a shared-bug blind spot).

## VERIFY@BUILD — RESOLVED (read-only verify, 2026-06-29; claude CLI v2.1.195)

Both load-bearing mechanics were confirmed against live code before C1 (the carrier-contract design):

- **(a) Plugin-install invocability (Decision 1) — confirmed at the CLI surface.** `claude plugin marketplace add <source> --scope project` and `claude plugin install <plugin>@<marketplace> --scope project` are **non-interactive CLI subcommands** with deterministic flags/exit codes (live `claude plugin … --help`, v2.1.195) — not session-only slash flows. The one interactive surface (`/plugin configure`) is bypassable via `--config <key=value>`. So the plugin carrier's `apply()` **shells out** to `claude plugin install … --scope project`; its `verify()` reads `claude plugin list --json` (or the consumer's `.claude/settings.json` `enabledPlugins` block). The "emit-the-command-for-the-operator" fallback is **not required**.
  - **Caveat (close at C2/C3, not now):** confirmed at the CLI-surface only — a read-only check could not run a real install. Before the plugin carrier is declared done, one real `claude plugin install … --scope project` in a throwaway clone must assert exit 0 + the `enabledPlugins` block written.
  - **Deterministic gotchas to encode:** `marketplace add` must precede `install` on a fresh cache; `install` no-ops ("already installed") on an installed repo — upgrades use `plugin update --scope project`; live activation needs a session restart (irrelevant — the tool needs the carrier *applied + verified*, not activated).
- **(b) Layer-2 write boundary (Decision 3) — resolved.** The original binary framing was wrong; the live boundary is the **three-edge "write-yes, commit-no, autonomy-no"** rule now stated in Decision 3 (evidence: ADR-78 Decision 2 + `scripts/generate_floor.py --out-dir`).

## Deferred (deliberately NOT decided / built here)

- The deploy tool, the carrier manifest, and the carrier implementations (this ADR is doctrine only).
- Fleet-batch; version-delta logic; rollback automation; a drift-detection poller; concurrent-deploy handling.
- Consumer-commit policy — **deferred to C2**; the read-only verify surfaced four options, all keeping the commit in the consumer context and non-autonomous (so all are permitted by the Decision 3 boundary): (1) tool writes, operator commits — the existing `generate_floor.py` precedent; (2) tool writes + stages, operator reviews `git diff --cached` and commits; (3) tool writes + auto-commits in the consumer (boundary-stretching — flagged); (4) emit-only (reintroduces the omission gap). Pick one and enforce it consistently; regardless of choice, the registry advances only after per-carrier verify (Decision 9).

## Rejected alternatives

- **A pure Claude Code slash command as orchestrator.** Rejected — an LLM-mediated flow is not a reliable authoritative state machine, and verification must not depend on the same session that could misreport success. Claude Code is a subprocess for the plugin carrier only.
- **A documented manual runbook / checklist as the primary control.** Rejected — the prior miss *was* a human following a procedure and skipping a step; "more checkboxes" is the control that already failed. (A short recovery runbook is still worth writing as secondary guidance, not as the deploy mechanism.)
- **Consumer-side auto-push to the hub registry (temp-clone or scoped deploy key).** Rejected — placing hub-write capability in an agent-accessible consumer environment is an avoidable blast-radius expansion not needed to solve the deployment problem.
- **Incremental-by-version-delta + fleet-batch.** Rejected for v1 — delta needs trustworthy current-version state and migration semantics that do not yet exist; fleet-batch multiplies blast radius before the single-repo path is proven.
- **Skip-if-present** (tolerates the observed drift) and **unconditional blind overwrite** (destructive; destroys the drift signal; over-leans on unproven universal idempotency). Both rejected as the *default*; overwrite survives only as the `--force` escape hatch.

## Consequences

- The deployment becomes a **deterministic, versioned, verification-gated tool** — the writer that completes ADR-91's record-and-surface loop. Once it runs, `deployed_methodology_version` reflects verified per-repo reality.
- `ai-council` (deploy run #1) is reconciled from its partial-but-live state (plugin present, ruff-gate missing) — the exact partial-deployment case the per-carrier model is designed to detect and repair.
- The registry becomes a **proof of completeness** rather than a declaration of intent; methodology drift ("repo X is two majors behind", "repo Y is missing carrier Z") becomes detectable.
- The remaining work after ratification is the **build**: the carrier manifest, the four hand-written carriers against the `detect/apply/verify` interface, the tool with `--dry-run`/`--force`/structured output, and the per-carrier test matrix (clean / partial / drifted / apply-twice / detect-verify-disagreement).

## Evidence

The two originating AI-Council transcripts (auto-routed here via `target-project`, ADR-43):

- `docs/decisions/transcripts/council-out-20260629_125000-pick-council-deploy-runbook-form.md` — process **form** (Q1 form, Q2 orchestration, Q3 record-commit). Synthesizer verdict: deterministic deploy-tool orchestrator run from the trusted hub context, one logical invocation with two internal phases, hub record on a branch for review/merge; no consumer-held hub write.
- `docs/decisions/transcripts/council-out-20260629_125409-pick-council-deploy-runbook-scope.md` — deploy **scope** (Q1 full-reconcile vs delta, Q2 partial-repo handling, Q3 multi-repo). Synthesizer verdict: single-repo full-reconcile with per-carrier detect/apply/verify and a `--force` re-apply escape hatch.

## Links

- ADR-91 — methodology corpus versioning (this doctrine is the deferred *writer*; the read-side registry + reader + PLAYBOOK Ch6 doctrine landed in that arc).
- ADR-28 / ADR-54 / ADR-69 / ADR-78 — the Layer-2 hub↛sibling write boundary.
- ADR-70 / ADR-73 / ADR-78 / ADR-79 — the carrier set a deploy spans.
- ADR-71 — the pre-commit `repo:/rev:` consume-pin a deploy updates.
- ADR-88 — file-oriented dependency management (*do-not-build-is-doctrine*).
