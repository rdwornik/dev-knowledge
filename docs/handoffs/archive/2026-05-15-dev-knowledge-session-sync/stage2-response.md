# Stage 2 Response: .dev-knowledge (session-sync, 2026-05-15)

Instructions for Rob:
1. Paste the PASTE_BOUNDARY block from stage1-question.md into the OLD chat.
2. Copy the old chat's full response.
3. Replace everything below the marker line with the response.
4. Save this file.
5. In Claude Code: "complete handoff for .dev-knowledge"

═══ REPLACE EVERYTHING BELOW THIS LINE ═══

### 1. OBJECTIVE

This section assumes zero prior session knowledge.

The primary objective for this session is Audit Tool P1 MVP implementation per ADR-36 [audit tool architecture]. Two prerequisites have landed in the lineage culminating at HEAD `a00985b`: PLAYBOOK additions for ADRs 36/37/40/41 merged at commit `72f486e` (operationally documenting the audit tool workflow before its implementation begins); v3.3.2 handoff template fix completed (parameterized `HANDOFF_FOLDER_TEMPLATE.md` for cross-repo bundles, `HANDOFF_PROCESS.md` bumped to v3.3.2, ai-council bundle regenerated with target VISION as primary `02_VISION.md` source). With both prerequisites cleared, audit tool implementation is the natural next P1 — Stream C `BACKLOG.md` had two P1 items, the first now `[done]`.

**P1 MVP deliverable spec.** A Click CLI in `scripts/audit.py` (matching the existing `scripts/validate_scope_tags.py` pattern for Python tooling in this repo) with subcommands `audit run`, `audit health`, `audit list-repos`. An ecosystem state schema persisted as `ecosystem/{repo}/state.yaml` (current snapshot) plus `ecosystem/{repo}/history/YYYY-MM-DD.md` (append-only history). Three pure-Python deterministic checks: (a) VISION.md presence + frontmatter parseable per ADR-33 [vision universalization]; (b) ADR-38 [universal repo architecture] baseline — the six mandatory root files (BACKLOG/LESSONS/VISION/README/CHANGELOG/JOURNAL) present at repo root; (c) ADR-31 [authority model] minimum — CLAUDE.md presence and parseable. Single markdown report output to `docs/audits/YYYY-MM-DD-ecosystem-audit.md`. Self-audit capability (`.dev-knowledge` auditing itself, dogfooding by construction).

**Success criteria.** Self-audit of `.dev-knowledge` produces a coherent markdown report; cross-repo audit of at least one child repo (recommend `ai-council` since its v3.3.2-regenerated bundle proves cross-repo template parameterization works) produces a coherent markdown report; all tests pass via `pytest -x --tb=short`. (architect inference): if both runs surface findings rather than producing clean reports, those findings should be cycled back into `BACKLOG.md` as P1/P2/P3 items — the audit tool's first audit is itself a feature, not a flaw.

**Why this objective is correctly ordered, not premature.** Audit Tool P1 has been deferred at least twice in the BACKLOG (Stream C P1 since 2026-04-30 per the BACKLOG entry context). The methodology work has now caught up: PLAYBOOK documents the workflow; v3.3.2 unblocks cross-repo bundles; LESSONS captured during the lineage explicitly motivate the tool (LESSON #1 documentation-conflation, LESSON #2 propose-then-verify — the audit tool's purpose is exactly to verify operational state rather than ratify artifacts). Further deferral would itself be the failure pattern the lessons warn against.

### 2. REALITY

This section assumes zero prior session knowledge.

**Methodology work landed in the recent lineage** (witnessed in commit messages preceding HEAD `a00985b`):

- Commit `72f486e` merged PLAYBOOK additions for ADRs 36/37/40/41: new Section 10 "BACKLOG Grooming Workflow" (ADR-41), Section 8 amended in place for ADR-37 [session boundary protocol] two-phase Current/Future State protocol, "Project Scale Tiers" extended with ADR-40 [scale tier evaluation] tier-transition procedures, new Section 18 "Ecosystem Audit Tool Workflow" for ADR-36. Renumbered existing sections 10-17 to 11-19 with cross-references updated across PLAYBOOK, ESSENTIALS, ADR-28, and one audit document. Scope-tag hybrid ratio stayed at 14% post-merge.
- Commit `cd33e85` merged 8 architect-self-observation LESSONS entries (documentation-conflation, propose-then-verify, over-conclusion-on-open-questions, internalization-vs-delivery, role-grounding-via-vision, iterative-file-load-pacing, tree-archive-value-distinct-from-regenerability, over-agreement-as-defensive-sycophancy).
- Commit `7c4faaa` merged a 9th LESSON (universal-without-cross-case-verification) plus the BACKLOG Stream C P1 entry for v3.3.2 template fix — both captures from the same lineage that surfaced template bugs in the initial ai-council cross-repo bundle attempt.
- Commit `14f0467` merged a same-day correction: the 9 LESSONS entries rewrote to canonical 6-field schema (drop the non-schema `— source: X; evidence: Y` trailer that broke format consistency with existing entries) and relocated from file tail to top of the dated-entries section. LESSONS.md header line 5 was updated from "go at the bottom" to "go at the top of the Entries section" to match the new convention. ADR-29 [LESSONS grandfathering] same-day override was authorized for the rewrite; formal "prepend at top" ordering convention amendment captured as Stream C P2 BACKLOG entry (deferred to its own dedicated session).
- (architect inference): the v3.3.2 template fix at HEAD `a00985b` parameterized articulation gate item #1 with `{repo}` substitution, made `02_VISION.md` source target-specific (target repo's VISION primary), introduced conditional `02b_ECOSYSTEM_VISION.md` (generated only when target ≠ `.dev-knowledge`), bumped `HANDOFF_PROCESS.md` v3.3.1 → v3.3.2, and regenerated the ai-council bundle with 12 checksummed files plus `01_manifest.json`. **Unknown — verify against repo:** exact set of files modified in the v3.3.2 commit, whether cross-case trace verification step was executed, whether the historical bugged ai-council bundle was preserved or overwritten.

**Work in progress not in commit log.** None witnessed at the time of writing.

**Open decisions bearing on audit tool design.**

- ADR-29 amendment for "prepend at top" LESSONS ordering remains [open] as Stream C P2 — not blocking audit tool, but worth being aware of since the audit tool may want to check LESSONS append discipline in a future phase.
- Sacred-files maintenance enforcement (Stream C P2) is conceptually adjacent: the audit tool *defines* the checks (file presence, frontmatter parseable), while sacred-files enforcement would *enforce* them long-term via hooks or periodic runs. (architect inference): P1 should define the checks; sacred-files enforcement remains separate P2 work and is not blocking.
- ESSENTIALS.md cheat-sheet additions for ADRs 35-41 are queued as P2 (currently at 226 lines per the ecosystem state context, pruning likely needed to satisfy under-1-page constraint). Not blocking audit tool P1.

**Relevant constraints witnessed in the methodology.**

- `scripts/validate_scope_tags.py` is the existing Python tooling pattern: single-file CLI in `scripts/`, tests in `tests/`, runs in pre-commit. The audit tool should follow this pattern unless explicit reason to diverge.
- The PLAYBOOK Section 18 (Ecosystem Audit Tool Workflow, added in commit `72f486e`) is the operational authority for the workflow. P1 implementation must match what that section describes, or the section must be amended in the same commit (preferable: implementation matches PLAYBOOK; PLAYBOOK is the spec).
- Pre-commit + `pytest -x --tb=short` + `ruff check --fix` + `git status` discipline is mandatory after each step. The audit tool's own tests must pass; existing pre-existing test failure (`test_ratio_pass_when_stable_above_ceiling`) remains pre-existing and acceptable but should not propagate to new tests.

**Architectural concerns about starting audit tool P1 now.**

(architect inference): None blocking. The PLAYBOOK section exists; the workflow is documented; the prerequisite v3.3.2 work has cleared the cross-repo path. The risk is scope creep — P1 must stay scoped to the three baseline checks specified, deferring richer checks (scope-tag drift, gotcha staleness, cross-reference integrity, LESSONS append discipline) to P2+ and LLM-augmented narrative to P4.

### 3. RATIONALE

This section assumes zero prior session knowledge.

**Architecture decision: P1 should be pure Python, not hybrid Python + LLM.** ADR-36 specifies a hybrid architecture: deterministic checks in Python, narrative/gap reporting in LLM-augmented Python. For P1 MVP, recommend deferring all LLM involvement to P4 (the explicitly-LLM-augmented phase per ADR-36). P1's three checks are binary or near-binary: file present/absent, frontmatter parseable yes/no, root-files-set complete or not. LLM-in-the-loop adds latency, cost, non-determinism, and provider dependency without commensurate value for binary verification. Save LLM for the storytelling phase where it earns its complexity (P4: gap detection across repos, anomaly identification, narrative explanation of findings). This narrows the P1 scope cleanly and matches the principle that emerged in the recent lineage's LESSONS — verify operational state cleanly, narrate later.

**CLI entry point location: `scripts/audit.py`.** (architect inference, based on `scripts/validate_scope_tags.py` precedent visible in the repo's existing tooling pattern.) Single-file CLI in `scripts/` matches the existing convention for Python developer tooling in `.dev-knowledge`. If the implementation grows beyond ~300-400 lines, factor out into `scripts/audit_lib/` with `scripts/audit.py` as thin CLI entry — but for P1 with only three checks, a single file should suffice. **Do not create a `src/audit/` package** — `.dev-knowledge` is currently a methodology repo, not a code package, and creating a `src/` would imply broader package structure that ADR-38 [universal repo architecture] does not mandate for `.dev-knowledge`'s tier (M). (architect inference): if scale escalates and a `src/` becomes warranted later, migration is a separate concern.

**P1 check scope — what is definitely in, what is deferred.**

IN (P1):

- VISION.md presence + frontmatter parseable per ADR-33: detects repos where VISION is missing entirely (audit-blocking gap) or where frontmatter has malformed YAML (architectural concern). High-signal, low-implementation-cost.
- ADR-38 universal repo architecture baseline — six mandatory root files: `BACKLOG.md`, `LESSONS.md`, `VISION.md`, `README.md`, `CHANGELOG.md`, `JOURNAL.md`. Single file-existence check, returns gap list of any missing. Highest-signal for cross-repo compliance.
- ADR-31 CLAUDE.md presence + basic parse: detects repos lacking CLAUDE.md governance authority (deep architectural gap).

DEFERRED to P2:

- Scope-tag drift across files (`validate_scope_tags.py` already covers this — audit tool can reference its findings rather than duplicate).
- Gotcha staleness (whether captured gotchas still apply).
- Cross-reference integrity (whether links between files resolve).
- LESSONS append-only invariant (whether file has retroactive edits).
- ADR-NN-prefix file naming compliance (catches mis-named ADR files).

DEFERRED to P4 (LLM phase):

- Narrative gap reports.
- Topic-clustering of findings across repos.
- Anomaly detection ("this repo's frontmatter pattern differs from siblings; possible drift").
- Suggested remediations.

**P1/P2 ordering: do not block P1 on sacred-files maintenance enforcement.** Sacred-files maintenance enforcement (the P2 item for staleness detection on 9 canonical files) is complementary, not prerequisite. P1 defines the checks; sacred-files enforcement would later automate periodic runs of those checks with staleness signaling. Implementing them in series (P1 first, then sacred-files P2) is correct ordering; conflating them in a single P1 session risks scope explosion.

**Cross-repo audit of `ai-council` serves dual purpose.** Beyond the deliverable spec (demonstrate cross-repo capability per success criteria), running audit on `ai-council` empirically validates the v3.3.2 template fix that landed in this same lineage. The `ai-council` bundle at `docs/handoffs/2026-05-14-ai-council-session-sync/` was regenerated from v3.3.2 template; that bundle's `02_VISION.md` should now contain ai-council's own VISION (not `.dev-knowledge` VISION). If audit tool finds the regenerated bundle non-compliant with VISION expectations, v3.3.2 fix itself was incomplete and needs follow-up amendment. Treat this as bonus signal during cross-repo audit interpretation: clean audit on regenerated `ai-council` bundle confirms v3.3.2 worked end-to-end; gaps may indicate v3.3.2 follow-up needed.

**Why scope discipline matters here in particular — failure modes from recent LESSONS firing in implementation-shaped work.** The lineage's LESSONS captured during recent sessions explicitly warn against scope expansion under empirical-evidence pressure. Audit Tool P1 will surface findings on first run; the temptation will be strong to "just also add a check for X" or "build the LLM narrative now since we're already here." Resist. P1 is three checks, ecosystem state file, markdown report, tests. That is the contract. Watch specifically for:

- **LESSON #1 (documentation conflation):** PLAYBOOK Section 18 documents the audit tool workflow. Documented workflow ≠ implemented tool. Implementation completion = test pass + self-audit run + cross-repo audit run, NOT merge of scaffold. Do not mark BACKLOG P1 `[done]` until end-to-end runs produce coherent markdown reports.
- **LESSON #2 (propose-then-verify):** Do not assume the tool works after initial scaffold. Run `audit health` first; run `audit list-repos`; inspect output manually; only then claim a directive is verified. The verification step in each directive is mandatory; tests-pass alone is insufficient signal.
- **LESSON #3 (over-conclusion on open questions):** First audit findings on `.dev-knowledge` self-audit may surface gaps. These are open questions, not established failures. Surface to operator before treating as bugs. Audit tool's job in P1 is to detect, not to judge severity or remediate.
- **LESSON #9 (universal-without-cross-case-verification):** Do NOT test only on `.dev-knowledge` self-audit. Cross-repo audit on `ai-council` is mandatory before declaring P1 complete. The 2026-05-14 v3.3.1 amendment was declared "universal" without cross-case test; cross-repo bug surfaced on first cross-repo use. Same pattern risk applies here.
- **Boundary blur on "while we're here" check additions:** First audit run will surface findings. Strong temptation to "just also add a check for X" or "improve the report format." Resist. P1 = three checks documented in DIRECTIVES. Additional checks defer to P2.

### 4. DIRECTIVES

This section assumes zero prior session knowledge.

0. **Pre-flight state verification (plan-mode checkpoint).** Before any scaffolding work, read state from repo to ground implementation in ground truth:
   - `git log --oneline -20`
   - `JOURNAL.md` (last 100 lines)
   - `BACKLOG.md` (full file — verify Stream C P1 audit-tool entry status)
   - `LESSONS.md` (last 80 lines — including #9 and any post-2026-05-14 entries)
   - `protocols/PLAYBOOK.md` Section 18 (Ecosystem Audit Tool Workflow — this is the operational spec the implementation must match)
   - `docs/decisions/ADR-36-audit-tool-architecture.md` (the architectural authority)
   - `docs/decisions/ADR-38-universal-repo-architecture.md` (canonical mandatory-files list for check #2 — verify Stage 2 REALITY section's 6-file list against this; adjust check #2 spec if discrepancy)

   Present state summary + revised implementation plan to operator. Plan mode → operator confirms → switch to auto-accept execution mode for remaining directives.

   Verification: state summary presented, operator confirms with explicit "proceed" or returns corrections. If corrections, adjust plan and re-present before proceeding to DIRECTIVE 1.

1. **Scaffold the Click CLI in `scripts/audit.py`** with subcommands `audit run` (executes all configured checks across all registered repos), `audit health` (sanity-check that the audit tool itself is configured correctly — Python version, dependencies, write paths), `audit list-repos` (enumerates repos discoverable in the ecosystem state directory). Verification: `python scripts/audit.py health` exits 0; `--help` text is coherent and matches PLAYBOOK Section 18 description.

2. **Define the ecosystem state schema** — `ecosystem/{repo}/state.yaml` for current snapshot (fields: repo name, repo path, last-audit timestamp, last-audit findings list with `check_name`, `status`, `evidence` per finding); `ecosystem/{repo}/history/YYYY-MM-DD.md` for append-only audit history (one markdown file per audit run). Implement with dataclasses (per repo dev standards: dataclasses over dicts) or `pydantic` if existing in `config/requirements-dev.txt` (check before adding; if not present, dataclasses suffice). Verification: roundtrip test — load state.yaml, mutate findings list, write back, reload — produces identical structure.

3. **Implement check #1: VISION.md presence + frontmatter parseable per ADR-33.** Check: target repo has `VISION.md` at root; YAML frontmatter is present, valid YAML, and contains minimum keys (architect inference — likely `version`, `tier`, `owner`, `last_reviewed`, `scale`, `status`; verify the actual ADR-33 minimum spec before implementing). Verification: check passes on `.dev-knowledge` self-audit; passes on `ai-council` (which has VISION at root per its tree at commit `0f069554`); detects missing/malformed VISION in a fixture.

4. **Implement check #2: ADR-38 universal repo architecture baseline.** Check: target repo has all six mandatory files at root — `BACKLOG.md`, `LESSONS.md`, `VISION.md`, `README.md`, `CHANGELOG.md`, `JOURNAL.md`. Returns gap list of any missing. `ARCHITECTURE.md` is conditionally optional at Scale M per ADR-38 — exclude from mandatory list, mention separately if absent. Verification: check passes on `.dev-knowledge` self-audit; passes on `ai-council`; detects missing files in fixture.

5. **Implement check #3: ADR-31 CLAUDE.md presence + basic parse.** Check: target repo has `CLAUDE.md` at root; file is non-empty and contains at least the conventional section headers (architect inference — verify expected sections against ADR-31 baseline). Verification: passes on `.dev-knowledge` self-audit; passes on `ai-council`; fails on fixture without CLAUDE.md.

6. **Implement markdown report output to `docs/audits/YYYY-MM-DD-ecosystem-audit.md`** containing per-repo findings table (repo, check name, status, evidence), aggregate summary (n repos, n checks, n passes, n fails), and links to per-repo `history/YYYY-MM-DD.md` files. Verification: report file generated; renders cleanly as markdown; passes scope-tag validator with `<!-- scope: meta -->` at top.

7. **Write tests in `tests/test_audit.py`** covering: schema roundtrip; each check on known-good fixture (synthetic repo dir with correct structure) and known-bad fixture (synthetic repo dir with intentional gaps); report generation with mocked check results; `audit health` subcommand exit code. Verification: `pytest -x --tb=short tests/test_audit.py` passes; coverage of new modules acceptable per existing repo conventions.

8. **Run self-audit:** `python scripts/audit.py run --repo .dev-knowledge`. Verification: report generated at `docs/audits/YYYY-MM-DD-ecosystem-audit.md`; findings either match expected clean state OR surface real issues (acceptable outcome — surfaced issues become new BACKLOG items).

9. **Run cross-repo audit:** `python scripts/audit.py run --repo ai-council`. Verification: report generated; findings either show ai-council compliance OR surface real gaps (acceptable; gaps become ai-council BACKLOG items, captured via operator-carried routing artifact per ADR-36's read-only contract — `.dev-knowledge` does NOT write to ai-council).

10. **Update BACKLOG:** mark Stream C "Audit tool P1 implementation" `[done]`; add any surfaced findings as new BACKLOG items (in the correct repo's BACKLOG — `.dev-knowledge` findings stay here; ai-council findings get captured for operator hand-carry to ai-council). Verification: BACKLOG diff shows P1 item flipped to `[done]`.

11. **Update BACKLOG, CHANGELOG, JOURNAL with multi-commit feature branch.** Use feature branch `feat/audit-tool-p1-mvp` off main. Commit cadence: one commit per concern (suggested boundaries: `scaffold + schema`; `check #1 VISION+frontmatter`; `check #2 ADR-38 baseline`; `check #3 CLAUDE.md`; `markdown report generation`; `tests`; `self-audit run results`; `cross-repo audit run results`; `BACKLOG/CHANGELOG/JOURNAL`). After all commits clean and validators green, merge `--no-ff` to main as single merge commit after operator approval.

    Verification: pre-commit clean across all commits; scope-tag validator clean; tests pass on every commit; hybrid ratio stays under ceiling. Single `--no-ff` merge commit visible in main log.

### 5. BOUNDARIES

This section assumes zero prior session knowledge.

- **Do NOT write to child repos.** ADR-36 read-only contract is absolute. Any code path that writes to a path outside `.dev-knowledge/` (other than reading from child repos for audit purposes) is an architectural violation. The audit tool reads child repos, writes only to `.dev-knowledge/ecosystem/{repo}/` and `.dev-knowledge/docs/audits/`. Findings on child repos that need remediation are surfaced in the report; operator hand-carries them to the relevant child repo's BACKLOG via routing artifact.

- **Do NOT add new Python dependencies without operator confirmation.** Check `config/requirements-dev.txt` first; the audit tool should be implementable with stdlib + whatever is already present (likely `pyyaml`, `click`, `rich` for output, `pytest`). If `pydantic` or similar is desired and not present, surface as a decision request rather than `pip install`-ing.

- **Do NOT implement P2 (handoff folder generator) in the P1 session.** P2 is the next phase per ADR-36's roadmap. Scope boundary: P1 = audit run + state + report. P2 = handoff folder generation per non-compliant repo (one folder per repo with structured findings to hand to that repo's next session). Conflating phases destroys the value of phasing.

- **Do NOT use the LLM for deterministic checks in P1.** All three P1 checks are pure Python: file existence, YAML parse, section presence. LLM augmentation is P4 scope per ADR-36 phasing. If the temptation arises ("but the LLM could write better evidence descriptions"), defer.

- **Do NOT skip tests.** Follow the `scripts/validate_scope_tags.py` + `tests/test_validate_scope_tags.py` pattern. Tests covering schema roundtrip, each check on known-good and known-bad fixtures, and report generation are non-negotiable. Pre-commit must pass clean before commit.

- **Do NOT expand check scope beyond the three specified.** Scope-tag drift, gotcha staleness, cross-reference integrity, LESSONS append-only invariant, ADR-NN file naming compliance — all interesting, all deferred to P2. P1 ships when three checks plus schema plus report plus tests are clean.

- **Do NOT couple audit tool P1 with sacred-files maintenance enforcement.** Sacred-files enforcement (the separate P2 item) is complementary, runs the audit's checks periodically with staleness signaling. Implement P1 first; sacred-files later as its own session. They are not the same scope.

- **Do NOT regenerate or modify the historical handoff bundles** (the bundle at `docs/handoffs/2026-05-14-ai-council-session-sync/` or any other handoff folder). Audit tool reads them as part of its repository inventory but never modifies them. They are append-only historical artifacts.

- **Do NOT push to remote without explicit operator approval.** Local commits only until operator authorizes `git push`.

- **Do NOT skip the self-audit step.** Running the audit tool against `.dev-knowledge` itself is mandatory dogfooding. If the audit tool cannot audit the repo it lives in, the audit tool has a structural defect.

- **Do NOT defend ad-hoc structural choices when convention divergence is flagged.** Default response when something feels off: "evaluate against ecosystem baseline (PLAYBOOK Section 18, ADR-36, existing `scripts/validate_scope_tags.py` pattern)" — not "intentional per local design."

- **Verify ADR-38 mandatory files list against actual ADR file** before implementing check #2. The architect-inferred 6-file list in REALITY section (`BACKLOG/LESSONS/VISION/README/CHANGELOG/JOURNAL`) may differ from canonical ADR-38 spec. Read `docs/decisions/ADR-38-universal-repo-architecture.md` first; if list differs, adjust check #2 spec to match the ADR. Surface discrepancy in CHANGELOG if found.

- **LESSONS entries (if any surfaced during implementation) must follow canonical 6-field schema** per commit `14f0467` correction: `### YYYY-MM-DD | source | lesson | category | [scope: X] | action taken`. No body trailer. Prepend at top of dated-entries section, not append at tail. ADR-29 amendment for "prepend at top" is pending separate session (Stream C P2 BACKLOG) but the schema convention applies now.

- **Self-audit recursive findings on `.dev-knowledge`** are design questions, not bugs. If audit tool finds `.dev-knowledge` non-compliant with rules the audit tool itself defines, surface to operator as potential design question. May require Council debate routing if architectural. Do NOT auto-fix `.dev-knowledge` based on self-audit output without operator review.
