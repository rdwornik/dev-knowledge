# Census — `docs/decisions/` (SWEEP 2026-09-07, lane S-03)

**Consumer:** `[#564]` (lifecycle archival — the pass this census supplies the measurement for) ·
`[#553]` (the ADR index in `docs/decisions/README.md` being ungated and wrong) ·
`[#616]` (flip-condition instrument) · `[#357]` (silent-rule census run 2 over this folder) ·
`[#362]` (the `[#242]` status cluster). Substantive citations are by path throughout:
`tasks/564-lifecycle-archival-implemented-adrs-and-decided-int.md`,
`tasks/616-flip-condition-every-adr-records-what-evidence-w.md`,
`protocols/STANDING_RULINGS.md` H3, `protocols/FUNNEL_LIFECYCLE.md` §3 and §"The ADR bar",
`scripts/validate_adr_status.py`.

**Posture: READ-ONLY.** Nothing in `docs/decisions/` was moved, deleted, edited or renamed by this
lane. Every verdict below is a **PROPOSAL** the operator rules. One file was written — this one.

**Scope measured:** `docs/decisions/` — **90** live `ADR-*.md` (1,004,094 B), **2** archived
(`archive/ADR-40`, `archive/ADR-52`; 15,682 B), and `README.md` (94,094 B). Folder total
1,113,870 B. Distinct ADR numbers 27–117 with **one gap: 44** (a Reserved index row, no file).

**Witness classes used, and one that was unavailable.** (1) Consumers found by `grep` over
`git ls-files`, stratified — see the Inventory legend. (2) The generator/validator that reads the
subject: `scripts/validate_adr_status.py` (run programmatically against this tree; it is the
authority for every Header-status and Index column below), `scripts/audit_checks/check_adr_status_grammar.py`,
`scripts/gen_claude_rosters.py`, `scripts/hooks/block_immutable_edits.py`.
(3) **Last content commit — UNAVAILABLE in this environment.** See `## Honest limits`.

**Gemini fan-out: NONE.** `command -v gemini` returns nothing on this host, so no locator was
produced by it and none was re-opened. **Gemini-read files: 0. Fabricated locators: 0** — a count
of zero over an empty set, which is not the same as a clean fan-out and is not reported as one.
**Copilot Enterprise offload was NOT available and was NOT used** — it is gated on intake `#75`,
unratified at this writing.

## Inventory

**Legend.** `KiB` = on-disk size. `Header status` / `Index` = the two surfaces
`validate_adr_status.py` compares (`header_status_map` vs `index_effective_status`); `—` in
Header status means the number is claimed by two files, so the validator refuses to resolve it
(its honest limit 4). `G` = which of the five measured status grammars the file uses; canonical is
**G1**. `Alt` = carries an `Alternatives`-headed section. `Flip` = carries a `Flip-condition`
section. `live` = consuming files in the LIVE tree (living docs, `protocols/`, `scripts/`,
`tests/`, `ecosystem/` schemas, `.claude/`, `deploy/` modules, `tasks/`) — **excluding** the three
generated enumerators that name every ADR by construction (`ecosystem/conformance.{md,html}`,
`.claude/generated/recent-adrs.md`) and excluding `docs/decisions/README.md`. `adr` = other ADRs
citing it. `rec` = files in the historical record (`docs/audits/`, `docs/handoffs/`, `JOURNAL.md`,
`logs/`, dated `history/`, `protocols/archive/`). **Counts key on the ADR NUMBER**, so the two
duplicate-numbered pairs (51, 70) each show one shared figure — that ambiguity is itself a finding.

**Flags:** `SIF-a` superseded-in-fact, whole mechanism · `SIF-b` superseded-in-fact, one named
half · `IDX` header/index disagreement · `DUP` duplicate ADR number · `SELF` self-amended in file
(no defect) · `TOKENED` supersession already carried in the status token (no defect) ·
`ORPHAN` zero live consumers · `ARCHIVED` already in `archive/` · `NEW` landed this week.

| # | File | KiB | Header status | Index | G | Alt | Flip | live | adr | rec | Flag |
|---|---|--:|---|---|---|---|---|--:|--:|--:|---|
| 27 | `ADR-27-scope-tagging` | 7.2 | Accepted | Accepted | G2 | — | — | 5 | 7 | 76 | SIF-b |
| 28 | `ADR-28-three-layer-architecture` | 2.0 | Accepted | Accepted | G2 | — | — | 83 | 26 | 198 |  |
| 29 | `ADR-29-lessons-grandfathering` | 18.2 | Accepted | Accepted | G2 | Y | — | 14 | 9 | 134 |  |
| 30 | `ADR-30-default-branch-main` | 2.7 | Accepted | Accepted | G2 | Y | — | 5 | 1 | 47 |  |
| 31 | `ADR-31-authority-model` | 5.4 | Accepted | Accepted | G2 | Y | — | 6 | 5 | 52 |  |
| 32 | `ADR-32-handoff-format` | 9.2 | Accepted | Accepted | G2 | Y | — | 3 | 7 | 51 | SIF-a |
| 33 | `ADR-33-vision-universalization` | 6.6 | Accepted | Accepted | G2 | — | — | 4 | 10 | 122 | SIF-a |
| 34 | `ADR-34-file-naming-convention` | 7.6 | Accepted | Accepted | G3 | — | — | 5 | 9 | 97 |  |
| 35 | `ADR-35-lessons-base-activation` | 6.0 | Accepted | Accepted | G3 | — | — | 5 | 3 | 51 |  |
| 36 | `ADR-36-audit-tool-architecture` | 15.1 | Accepted | Accepted | G3 | — | — | 20 | 18 | 194 |  |
| 37 | `ADR-37-session-boundary-protocol` | 6.3 | Accepted | Accepted | G3 | — | — | 2 | 5 | 49 |  |
| 38 | `ADR-38-universal-repo-architecture` | 18.3 | Accepted | Accepted | G3 | — | — | 27 | 12 | 249 | SIF-b |
| 39 | `ADR-39-file-lifecycle-governance` | 22.2 | Accepted | Accepted | G3 | — | — | 9 | 16 | 88 |  |
| 40 | `archive/ADR-40-scale-tier-evaluation` | 12.3 | — | Deprecated | G3 | — | — | 5 | 5 | 84 | ARCHIVED |
| 41 | `ADR-41-cross-session-backlog-architecture` | 16.8 | Accepted | Accepted | G3 | — | — | 33 | 14 | 198 |  |
| 42 | `ADR-42-handoff-format-v3` | 21.0 | Accepted | Accepted | G3 | — | — | 5 | 10 | 131 | SIF-a |
| 43 | `ADR-43_cross_project_transcript_routing` | 7.9 | Accepted | Accepted | G3 | Y | — | 7 | 6 | 66 | SIF-b |
| 45 | `ADR-45-handoff-architecture-v4` | 22.4 | Explored, not adopted | Superseded | G3 | — | — | 5 | 3 | 65 | IDX |
| 46 | `ADR-46-cross-repo-dated-entries-format` | 2.8 | Partially superseded | Accepted | G3 | — | — | 3 | 4 | 68 | IDX |
| 47 | `ADR-47-cross-repo-backlog-organization` | 3.2 | Partially superseded | Accepted | G3 | — | — | 2 | 8 | 56 | IDX |
| 48 | `ADR-48-trim-documentation-governance` | 1.9 | Accepted | Accepted | G1 | — | — | 3 | 4 | 28 |  |
| 49 | `ADR-49-consolidate-past-recording-files` | 2.0 | Accepted | Accepted | G1 | — | — | 16 | 6 | 80 |  |
| 50 | `ADR-50-machine-document-encoding` | 2.0 | Accepted | Accepted | G1 | — | — | 1 | 0 | 10 |  |
| 51 | `ADR-51-amendment-2026-07-05-llm-first-canonical-docs` | 5.7 | — | Accepted | G1 | — | — | 31 | 6 | 106 | DUP |
| 51 | `ADR-51-architecture-doc-convention` | 21.2 | — | Accepted | G1 | Y | — | 31 | 6 | 106 | DUP |
| 52 | `archive/ADR-52-agents-md-convention` | 3.0 | Superseded | Superseded | G1 | Y | — | 6 | 2 | 30 | ARCHIVED |
| 53 | `ADR-53-claude-md-single-instruction-file` | 4.4 | Partially superseded | Partially superseded | G1 | Y | — | 18 | 5 | 104 | TOKENED |
| 54 | `ADR-54-codex-reviewer-global-standard` | 4.9 | Accepted | Accepted | G1 | Y | — | 9 | 2 | 55 |  |
| 55 | `ADR-55-applied-task-internalization-gate` | 6.7 | Accepted | Accepted | G1 | Y | — | 2 | 6 | 22 |  |
| 56 | `ADR-56-prompt-generation-card` | 6.0 | Accepted | Accepted | G1 | Y | — | 3 | 3 | 18 |  |
| 57 | `ADR-57-two-layer-bundle-contract` | 5.6 | Accepted | Accepted | G1 | Y | — | 2 | 2 | 19 |  |
| 58 | `ADR-58-structured-claims-verification` | 6.4 | Accepted | Accepted | G1 | Y | — | 2 | 3 | 18 |  |
| 59 | `ADR-59-universal-visual-repository-pattern` | 17.3 | Accepted | Accepted | G1 | Y | — | 16 | 3 | 134 |  |
| 60 | `ADR-60-docs-folder-taxonomy` | 13.8 | Accepted | Accepted | G1 | — | — | 10 | 8 | 79 | SELF |
| 61 | `ADR-61-git-worktree-parallel-sessions` | 4.4 | Accepted | Accepted | G4 | — | — | 16 | 3 | 55 | SIF-a |
| 62 | `ADR-62-v4-handoff-process-ratification` | 14.4 | Accepted | Accepted | G1 | Y | — | 3 | 3 | 26 | SIF-a |
| 63 | `ADR-63-scrum-master-review-authority` | 11.6 | Accepted | Accepted | G1 | Y | — | 2 | 1 | 18 |  |
| 64 | `ADR-64-backlog-architecture` | 4.9 | Accepted | Accepted | G2 | — | — | 4 | 4 | 15 |  |
| 65 | `ADR-65-backlog-done-item-disposition` | 3.8 | Accepted | Accepted | G2 | Y | — | 35 | 12 | 151 |  |
| 66 | `ADR-66-backlog-story-map-hierarchy` | 8.7 | Accepted | Accepted | G2 | Y | — | 22 | 8 | 65 |  |
| 67 | `ADR-67-ai-council-process-operationalization` | 5.4 | Accepted | Accepted | G2 | Y | — | 5 | 3 | 15 |  |
| 68 | `ADR-68-night-agent` | 9.8 | Accepted | Accepted | G2 | Y | — | 9 | 5 | 17 |  |
| 69 | `ADR-69-cross-repo-audit-reach-model` | 4.4 | Accepted | Accepted | G2 | Y | — | 3 | 5 | 5 |  |
| 70 | `ADR-70-amendment-2026-07-07-fable-xl-tier` | 5.2 | — | Accepted | G1 | Y | — | 36 | 12 | 86 | DUP |
| 70 | `ADR-70-three-tier-process-automation` | 9.2 | — | Accepted | G2 | Y | — | 36 | 12 | 86 | DUP |
| 71 | `ADR-71-doc-tooling-hook-source-repo` | 10.5 | Accepted | Accepted | G2 | Y | — | 10 | 5 | 22 |  |
| 72 | `ADR-72-cloud-routine-hub-independence` | 9.1 | Accepted | Accepted | G2 | Y | — | 8 | 4 | 25 |  |
| 73 | `ADR-73-per-repo-orchestration-distribution` | 1.6 | Accepted | Accepted | G1 | Y | — | 2 | 6 | 14 |  |
| 74 | `ADR-74-automation-doctrine-consolidation` | 6.2 | Accepted | Accepted | G1 | Y | — | 6 | 4 | 25 |  |
| 75 | `ADR-75-exclusion-zone-register` | 2.0 | Accepted | Accepted | G1 | Y | — | 14 | 4 | 56 |  |
| 76 | `ADR-76-local-fleet-baseline-host` | 5.7 | Accepted | Accepted | G1 | Y | — | 9 | 2 | 25 |  |
| 77 | `ADR-77-immutable-paths-zone-class` | 5.0 | Accepted | Accepted | G1 | Y | — | 11 | 3 | 44 |  |
| 78 | `ADR-78-child-methodology-floor` | 5.9 | Accepted | Accepted | G1 | Y | — | 24 | 4 | 37 |  |
| 79 | `ADR-79-browser-carrier-bundle-only` | 4.3 | Accepted | Accepted | G1 | Y | — | 2 | 3 | 10 | SIF-b |
| 80 | `ADR-80-two-tier-automation-adoption` | 7.5 | Accepted | Accepted | G1 | Y | — | 29 | 7 | 73 |  |
| 81 | `ADR-81-feature-lifecycle-definition-of-done` | 7.5 | Accepted | Accepted | G1 | Y | — | 26 | 5 | 122 |  |
| 82 | `ADR-82-handoff-process-v5-model-c` | 18.3 | Accepted | Accepted | G1 | Y | — | 11 | 7 | 75 |  |
| 83 | `ADR-83-protocols-archive-convention` | 5.4 | Accepted | Accepted | G1 | Y | — | 3 | 0 | 44 |  |
| 84 | `ADR-84-automation-writer-isolation` | 5.1 | Accepted | Accepted | G2 | — | — | 17 | 1 | 60 |  |
| 85 | `ADR-85-session-lifecycle-enforcement` | 29.1 | Accepted | Accepted | G2 | Y | — | 75 | 8 | 264 | SIF-b |
| 86 | `ADR-86-conformance-dashboard-location` | 10.4 | Accepted | Accepted | G2 | Y | — | 12 | 2 | 38 |  |
| 87 | `ADR-87-equilibrium-contract` | 8.9 | Accepted | Accepted | G2 | Y | — | 11 | 11 | 155 |  |
| 88 | `ADR-88-file-oriented-dependency-management` | 14.8 | Accepted | Accepted | G2 | — | — | 23 | 8 | 98 |  |
| 89 | `ADR-89-computed-code-dependency-edges` | 27.1 | Accepted | Accepted | G2 | — | — | 19 | 3 | 60 |  |
| 90 | `ADR-90-resolver-allows-n-multi-site` | 8.3 | Accepted | Accepted | G2 | Y | — | 7 | 1 | 12 |  |
| 91 | `ADR-91-methodology-corpus-versioning` | 9.1 | Accepted | Accepted | G2 | Y | — | 20 | 8 | 44 |  |
| 92 | `ADR-92-deploy-runbook-doctrine` | 18.3 | Accepted | Accepted | G2 | Y | — | 25 | 4 | 36 |  |
| 93 | `ADR-93-floor-provisioning-model-a` | 11.8 | Accepted | Accepted | G2 | Y | — | 19 | 2 | 34 |  |
| 94 | `ADR-94-adr-status-line-mutable-on-ratification` | 4.9 | Accepted | Accepted | G1 | Y | — | 15 | 20 | 82 |  |
| 95 | `ADR-95-ai-council-query-lane-split` | 3.7 | Accepted | Accepted | G1 | Y | — | 0 | 1 | 14 | ORPHAN |
| 96 | `ADR-96-deploy-remove-leg` | 10.5 | Accepted | Accepted | G1 | Y | — | 10 | 0 | 20 |  |
| 97 | `ADR-97-tree-orchestration` | 9.2 | Accepted | Accepted | G1 | Y | — | 13 | 3 | 32 |  |
| 98 | `ADR-98-intake-pipeline` | 11.9 | Accepted | Accepted | G1 | Y | — | 39 | 11 | 125 |  |
| 99 | `ADR-99-epic-naming-convention` | 4.3 | Accepted | Accepted | G1 | Y | — | 8 | 1 | 15 |  |
| 100 | `ADR-100-audit-retention-index-rule` | 7.3 | Accepted | Accepted | G1 | Y | — | 12 | 5 | 86 |  |
| 101 | `ADR-101-hermetization` | 52.2 | Accepted | Accepted | G1 | Y | — | 48 | 8 | 363 |  |
| 102 | `ADR-102-parity-gate-rev-axis` | 8.2 | Accepted | Accepted | G2 | — | — | 10 | 4 | 44 |  |
| 103 | `ADR-103-parity-ownership-axis` | 8.5 | Accepted | Accepted | G2 | — | — | 4 | 1 | 20 |  |
| 104 | `ADR-104-fleet-repository-shape` | 22.2 | Accepted | Accepted | G1 | Y | — | 30 | 3 | 90 |  |
| 105 | `ADR-105-routine-consumer-declaration` | 8.6 | Accepted | Accepted | G2 | — | — | 21 | 4 | 81 |  |
| 106 | `ADR-106-environment-isolation-uv` | 7.9 | Accepted | Accepted | G2 | — | — | 28 | 4 | 117 |  |
| 107 | `ADR-107-backlog-restructure-engine-schema-viewer` | 36.3 | Accepted | Accepted | G2 | Y | — | 41 | 3 | 103 |  |
| 108 | `ADR-108-decision-routing-and-engineering-standards` | 8.4 | Accepted | Accepted | G2 | — | — | 20 | 5 | 82 |  |
| 109 | `ADR-109-fleet-desired-state-contract-v1` | 26.4 | Accepted | Accepted | G2 | Y | — | 25 | 2 | 83 |  |
| 110 | `ADR-110-parallel-execution-batch-protocol` | 22.1 | Accepted | Accepted | G2 | Y | — | 41 | 1 | 225 |  |
| 111 | `ADR-111-finding-triage-pipeline` | 14.4 | Accepted | Accepted | G1 | — | — | 19 | 3 | 140 |  |
| 112 | `ADR-112-two-tier-adoption-bar` | 9.3 | Accepted | Accepted | G1 | Y | — | 7 | 1 | 71 |  |
| 113 | `ADR-113-l0-l5-maturity-ladder-ratification` | 6.4 | Accepted | Accepted | G1 | — | — | 3 | 1 | 15 |  |
| 114 | `ADR-114-readme-recreation-legality` | 17.5 | Accepted | Accepted | G1 | Y | — | 27 | 1 | 65 |  |
| 115 | `ADR-115-agents-md-portable-instruction-layer` | 29.2 | Accepted | Accepted | G1 | Y | — | 19 | 2 | 48 |  |
| 116 | `ADR-116-fuzzy-band-acceptance-shape` | 18.5 | Proposed | Proposed | G1 | Y | — | 8 | 1 | 20 |  |
| 117 | `ADR-117-carrier-split-by-divergence` | 20.4 | Proposed | Proposed | G1 | Y | Y | 1 | 0 | 4 | NEW |

## Proposals

Grouped by verdict. Every row carries a witness; where one could not be established the file is
marked `UNDETERMINED` and the gap is named rather than filled.

### KEEP — 92 of 92

**Every file in `docs/decisions/` stays where it is, and this is a measured verdict rather than a
default.** The repo's own archival bar is `protocols/STANDING_RULINGS.md` **H3**: *a terminal-status
ADR moves to `docs/decisions/archive/` when its inbound reference count is zero.* Applied to this
tree:

- **Terminal statuses (`Superseded`, `Deprecated`) on LIVE ADRs: zero.** The only two terminal
  tokens in the corpus are `archive/ADR-52` (`Superseded`) and `archive/ADR-40` (`Deprecated`), and
  both are already archived. Witness: `validate_adr_status.py` status tally over both zones —
  `Accepted` 84, `Partially superseded` 3, `Proposed` 2, `Explored, not adopted` 1, `Deprecated` 1,
  `Superseded` 1, unparseable 1.
- **Zero-inbound: one candidate, and it fails the other half of the test.** `ADR-95` is the only
  file with **zero** live consumers, but its status is `Accepted`, not terminal, so H3 does not
  reach it.

**Consequence, stated plainly: H3's predicate is satisfied by no live ADR, so the archival half of
`[#564]` has nothing to move in this folder.** That row's complaint — "2 archived against 86 live"
— re-measures here as **2 against 90**, and the ratio is not evidence of un-run archival. It is
evidence that **no ADR has been given a terminal token**, which is a different repair and one
`[#564]`'s own scope line explicitly excludes (*"no ADR is superseded ... by this row"*). The
operator decision this census actually surfaces is therefore **not where files live, but whether
the twelve `SIF` files below should be tokened** — and only after that would `[#564]`'s pass have
input.

Within KEEP, four sub-groups carry something the operator should see.

**(a) Superseded-in-fact — whole mechanism replaced, status still `Accepted` (5 files).**

| ADR | The mechanism it decided | What replaced it | Witness |
|---|---|---|---|
| 32 | handoff format v2: 9-section content, folder-format convention, `AGENTS.md` as canonical cross-tool governance | `HANDOFF_PROCESS` v7 for the format; ADR-52 → ADR-53 → ADR-115 for the instruction layer | `protocols/HANDOFF_PROCESS.md:7,17-18`; `docs/decisions/archive/ADR-52-agents-md-convention.md` |
| 33 | `VISION.md` mandated across ecosystem repos, with frontmatter and an enforcement leg | ADR-114 / `[#614]` retired `VISION.md` as a canonical MUST; the file now lives at `docs/archive/VISION.md` and the check that asserted its presence is registry-driven and returns n/a | `scripts/audit_checks/check_vision_md.py` docstring (`canonical_docs.CANONICAL_RETIRED`); `docs/archive/VISION.md` exists, root `VISION.md` does not; `protocols/HANDOFF_PROCESS.md:661` |
| 42 | handoff format v3.0 (three-stage flow, ~11-file flat folder) | `HANDOFF_PROCESS` v7 | `protocols/HANDOFF_PROCESS.md:7,17`; `protocols/archive/HANDOFF_PROCESS_v3.4.md` |
| 61 | worktree setup / cleanup / naming procedure | the native-worktree convention (`#107`); **the ADR marks its own procedure subsections `❌ SUPERSEDED` in-file at lines 40, 48, 64 and 71 while its status line still reads `Accepted`** | `docs/decisions/ADR-61-git-worktree-parallel-sessions.md:40,48,64,71`; `protocols/PLAYBOOK.md:1919` |
| 62 | post-hoc ratification of `HANDOFF_PROCESS` v4 | v7, which names v4.4 as the version it supersedes | `protocols/HANDOFF_PROCESS.md:17` (`Supersedes: HANDOFF_PROCESS v4.4`) |

**(b) Superseded-in-fact in ONE named half — the rest of the decision stands (5 files).**

| ADR | The half that is gone | The half that stands | Witness |
|---|---|---|---|
| 27 | scope-tag **enforcement** | scope tags as an informal convention | `protocols/PLAYBOOK.md:4183` ("scope-tag enforcement withdrawn per ADR-48"); `CLAUDE.md` §4 ("informal, not enforced") |
| 38 | amendment **A5**'s deprecation of the root `README.md` | the rest of the universal repo baseline, cited by 27 live files | `docs/decisions/ADR-114-readme-recreation-legality.md:7` (`Supersedes (if accepted): ADR-38 amendment A5`) with `:171` recording that the conditional lapsed when the operator ruled it Accepted 2026-08-29; `protocols/ENVIRONMENT.md:194,228` |
| 43 | the **routed-mirror** clause — landing zones retired, hub archive deleted at `b4435fad` | transcripts canonical-only in `ai-council/output/`; the ADR carries the retirement as an in-file amendment | `protocols/AI_COUNCIL_PROCESS.md:17,173,313,394`; `protocols/PLAYBOOK.md:1245` |
| 79 | the consolidated `BUNDLE.md` delivery it mandated — **no `BUNDLE.md` exists in the tree** | "Projects deferred", which is still live doctrine | `ARCHITECTURE.md:898,1196` ("ADR-79's consolidated-`BUNDLE.md` delivery was superseded by ADR-82") |
| 85 | §4's **local override token path** | the rest of session-lifecycle enforcement — the two fail-closed pre-push hooks, 75 live consumers | `protocols/DEFINITION_OF_DONE.md:155` ("Override — **RETIRED** (ADR-85 amendment 2026-08-03, §A2)") |

For (a) and (b) alike the **file** stays: ADRs are immutable, H3 holds an ADR in place on any
inbound reference, and all ten carry live inbound. What is proposed is a **status-token decision**,
which is the operator's under ADR-94 (the status line is the one in-place-editable field) — not a
move, and not this lane's to take.

**(c) Header/index disagreement — 3 files, and in every case the INDEX is the stale side.**

`validate_adr_status.py`'s coherence leg fires three times, all WARN:

- `ADR-45` — header `Explored, not adopted`, index `Superseded`. The index is wrong: the
  supersession claim was **withdrawn** at `c5e6d9f4`, and `protocols/FUNNEL_LIFECYCLE.md:95-99`
  records the withdrawal as a token correction rather than a state change.
- `ADR-46`, `ADR-47` — header `Partially superseded`, index `Accepted`. `docs/decisions/README.md`
  §"Status enum" itself names these two as `Partially superseded` in its 2026-08-12 measurement,
  so the index table disagrees with the index's own prose.

Proposal: the fix belongs to `[#553]` (the index), not to the ADR bodies. Three index rows.

**(d) Duplicate ADR numbers — 2 pairs, 4 files.** `ADR-51` and `ADR-70` are each claimed by a
base file and an `-amendment-` file. The validator reports the collision rather than resolving it
(its honest limit 4) and, as a consequence, **refuses to emit a header status for either number** —
which is why four rows in the Inventory show `—`. It also means the consumer counts for 51 and 70
cannot be split between the two files by any mechanical means available here. Proposal: this is a
naming-grammar question for the operator; renaming an immutable ADR is not proposable by a census.

**(e) Orphan — 1 file.** `ADR-95` (ai-council query lane-split) has **zero** live consumers: no
protocol, no script, no test, no living doc, no `tasks/` row. Its 14 record-stratum mentions are
JOURNAL entries, four handoff bundles and four audits. The JOURNAL entry that lands it says why —
*"recorded the ai-council query lane-split as ADR-95 (record-only; **no `/council` wiring built**)"*
(`JOURNAL.md:27172`). Proposal: the operator rules whether a ratified decision whose mechanism was
never built should carry a terminal token; if it does, it becomes the **first** live ADR to satisfy
H3's zero-inbound predicate, and `[#564]`'s pass gains its first genuine subject.

### RELOCATE — 0

No file is in the wrong home. `docs/decisions/` is the ruled home for ADRs and `archive/` for
terminal ones; there is no third home in the `#73` grammar for this class, and both archived files
carry terminal tokens. The two `-amendment-` files are the only relocation-shaped question in the
folder and they fail it: an amendment to an immutable ADR is decision content, and moving it
would break locators that immutable files cannot re-point.

### ARCHIVE — 0

Measured against H3, above: zero live ADRs carry a terminal status, so zero are eligible. Recorded
for the next reader: `protocols/FUNNEL_LIFECYCLE.md` §"The ADR bar" measures that **neither** of
the two already-archived files satisfied H3 at the moment it was archived (`ADR-52` carried 13
inbound, `ADR-40` carried two living-doc inbound). This census does **not** propose reversing
either move — reversal costs more locators than it repairs — but it confirms that measurement
stands and that the 2026-07-22 commit must not be cited as a worked instance of H3.

### RETIRE — 0

Not proposable for this class. ADRs are immutable by `CLAUDE.md` §5 rule 3 and guarded at tool time
by `scripts/hooks/block_immutable_edits.py` (ADR-77, fail-closed `PreToolUse`). A census cannot
propose deleting a ratified decision.

### UNDETERMINED — 0 files, 1 question

Every one of the 92 files has at least one witness, so no file-level verdict is unwitnessed. One
**question** is undetermined and is named rather than guessed: see limit 3 in `## Honest limits`.

### The three questions this lane was asked

**1. ADRs superseded-in-fact (mechanism replaced): 10** — five whole (`ADR-32, 33, 42, 61, 62`),
five in one named half (`ADR-27, 38, 43, 79, 85`). All ten still read `Accepted`. Two further files
already carry the fact in their token and are **not** counted: `ADR-53` (`Partially superseded`,
by ADR-115) and `archive/ADR-52` (`Superseded`, by ADR-53). Two more self-amend in file with the
supersession scoped inside the ADR (`ADR-60`'s 2026-05-27 amendment heading literally reads
*"supersedes original folder list above"*; `ADR-43`'s amendment block) — `ADR-60` is recorded as
`SELF` and not counted as a defect; `ADR-43` is counted in (b) because its retirement was ruled
outside the file and its whole subject is the retired mechanism.

**2. ADRs cited by nothing: 1** — `ADR-95`, zero live consumers, evidenced above. Under a stricter
reading ("nothing but the enumerators that name every ADR by construction") the answer is still 1.
A near-miss set of **11** is thinly cited at ≤2 live consumers and is where the next orphan will
come from: `ADR-37, 46, 47, 50, 55, 57, 58, 63, 73, 79, 117` — of which `ADR-50` (1 consumer:
`ARCHITECTURE.md`) and `ADR-117` (1 consumer: a comment in `tests/test_validate_adr_status.py`)
are the thinnest. `ADR-117` landed 2026-09-06 and its thinness is age, not rot.

**3. ADRs without Alternatives / without Flip-condition — COUNT ONLY (W2-F4 owns the fix):**

- **without an `Alternatives`-headed section: 32 of 92** (60 carry one). The template
  (`templates/ADR-template.md`) already carries `## Alternatives considered` and says *"Always
  filled"*, so all 32 are pre-template or template-divergent files. Full list is the `Alt = —`
  rows in the Inventory.
- **without a `Flip-condition` section: 91 of 92.** Exactly one carries it — `ADR-117`, which is
  `[#616]`'s first and only live instance. The **template carries no `Flip-condition` section at
  all**, which is `[#616]`'s first Done-when clause and is open.

**No fix is proposed for either count, and none was applied.** `[#616]` is open and W2-F4 is live
in the tree beside this lane.

## Counts before → proposed after

Read-only census: **every "after" equals its "before" for file placement.** What changes, if the
operator rules the proposals, is metadata this lane did not touch.

```
FILE PLACEMENT (this lane proposes no move)
live ADR files in docs/decisions/          90  ->  90
files in docs/decisions/archive/            2  ->   2
README.md                                   1  ->   1
folder bytes                        1,113,870  ->  1,113,870

VERDICTS ASSIGNED (92 files)
KEEP                                       92
RELOCATE                                    0
ARCHIVE                                     0
RETIRE                                      0
UNDETERMINED                                0

WHAT THE OPERATOR IS ASKED TO RULE (no lane may take these)
status tokens still reading `Accepted` on a replaced mechanism   10  ->  operator's call
index rows disagreeing with the ADR header (owned by [#553])      3  ->   0 if ruled
duplicate ADR numbers (51, 70)                                    2  ->  operator's call
ratified-but-never-built ADRs with no terminal token (ADR-95)     1  ->  operator's call

MEASUREMENTS THAT RE-PRICE AN OPEN ROW
[#564] "2 archived against 86 live"      re-measures  2 against 90
[#564] ADRs eligible under H3 today                            0
[#616] ADRs carrying a Flip-condition                     1 of 92
[#616] template carries a Flip-condition section              no
ADRs with no Alternatives section                        32 of 92
canonical status grammar G1                    44 of 93 fields
validator defect tally  grammar 49 WARN / coherence 3 WARN / duplicate-id 2 WARN
                        wrapped-value 1 WARN / enum 1 FAIL / single-field 1 FAIL
```

The two FAIL-armed defects both land on **one already-archived file**,
`archive/ADR-40-scale-tier-evaluation.md`: it carries **two** status fields (lines 5 and 10) and
the first reads `DEPRECATED 2026-05-23.`, which is not a member of the declared enum — the enum
spells it `Deprecated`. This is pre-existing and it is in `archive/`, which the `TIER_COMMIT` hook
scans only via `--include-archive`; it is reported here, not repaired here.

## Honest limits

These are the things this census could **not** establish. The section is the point.

**1. The "last content commit" witness class was unavailable — for 91 of 92 files.** This clone is
**shallow** (`.git/shallow` present, 17 graft points, 278 commits reachable, oldest 2026-09-01).
At a graft boundary git truncates the parents of the boundary commit, so `git log --no-merges -1 --
<file>` does **not** filter it: it reports the boundary merge `428656f` (2026-09-05) as a root
commit with a full diff. That value was returned for **91 of 92** ADR files and is an artefact of
the clone, not a fact about the corpus. Only `ADR-117` has a genuine in-window content commit
(`591267e`, 2026-09-07). **Consequence: no verdict in this census rests on file age or last-touch,
and no staleness claim is made from git history.** Every verdict rests on consumers-by-grep or on
the generator/validator that reads the file. A re-run on a full clone would add that third witness
class and could sharpen sub-group (e) in particular.

**2. The frozen authority file was not read.** The contract names
`to-cc\BATCH-2026-09-07-SWEEP-CONTRACTS.md` (5422 B) as the authority that wins over the working
copy, and instructs the lane to read it. **It is not present in this checkout and not anywhere on
this host** (`find` over the tree returns nothing; there is no `to-cc/` directory). This lane
executed the working copy alone. If the frozen contract differs from it, this census was produced
against the wrong rules and nothing here detected that.

**3. "Superseded-in-fact" is a judgment, and its boundary is undetermined.** Ten files are reported
because a live, non-record surface says in terms that the mechanism was replaced, retired or
deleted. What this lane could **not** establish is the complement: whether any of the remaining
80 files decide a mechanism that has quietly stopped existing **without any living doc saying so**.
Establishing that means reading 80 Decision sections against the current tree — a different and
much larger job than a census, and one whose absence would be invisible in a census that claimed to
have done it. The 10 is a **floor**, not a total. `[#357]` (silent-rule census run 2 over exactly
this folder) is the open row that owns the mechanical half of that sweep.

**4. Consumer counts are substring matches on `ADR-\d+`, and they over-count.** A file that names
an ADR only to say it is retired counts as a citer — the same limit
`scripts/consumer_at_landing.py` declares for itself. So `ADR-79`'s two live consumers are both
files recording that half of it is superseded, and `ADR-95`'s zero is therefore a **stronger**
result than the non-zero figures around it: over-counting cannot manufacture a zero. The stratum
boundary (live vs record) is this lane's construction, not a repo-declared one; it excludes three
generated enumerators by name and treats `ecosystem/*/history/` and `protocols/archive/` as record.
A reader who draws that boundary differently gets different `live` figures and the same zero.

**5. Duplicate-numbered files cannot be told apart by any mechanical means here.** For `ADR-51` and
`ADR-70` the consumer counts, the index status and the header status are all keyed on the number,
so the four rows involved carry shared or absent values. Which file "is" ADR-51 is not a question
this census can answer, and `validate_adr_status.py` explicitly declines it too.

**6. The declared environment could not be rebuilt, so the validator was run out-of-env.**
`uv run --locked` refuses on this host: `pyproject.toml` pins `required-version = "==0.11.19"` and
the host carries `uv 0.8.17`. Bumping `uv` is its own gated change (ADR-106) and is not a
docs-only lane's act, so it was **not** done. `validate_adr_status.py` was instead imported and
driven with the system interpreter behind a two-function `click` stub; its parsing, enum, grammar,
coherence and duplicate-id logic ran **unmodified** against this tree, and the surface line it
produced is quoted above. What did **not** run: the CLI's own exit-code contract, the pre-commit
hook wrapper, and the pinned dependency set. A re-run under `uv 0.11.19` is the confirming act.

**7. No test suite was run, by contract.** The lane brief forbids the full suite (a known RED on
main, `test_manifest_link_route.py::test_the_class_enum_is_the_hermetization_module_s_own_object`,
triggered by test selection and not this lane's). No targeted subset was run either: this lane's
diff is one new markdown file under `docs/audits/` and touches no module any test covers.

**8. `docs/audits/README.md` was deliberately NOT regenerated.** `[#590]` narrowed
`audit-index-freshness`; the integrator regenerates the index once after the last of the 13 census
lanes merges. This file will therefore be absent from that index until then, and that absence is
expected rather than a defect.

**9. No fan-out happened at all.** `gemini` is not on PATH; Copilot Enterprise offload is gated on
unratified intake `#75`. Both the Gemini-read-file count (0) and the fabrication count (0) are
counts over an empty set. Nothing was cross-read, so nothing here has a second reader — every
locator in this file was opened by this lane and by nobody else.

**10. The commit gates did not run on this commit, and could not.** `.git/hooks/` in this clone
carries no `pre-commit`, `commit-msg` or `pre-push` hook, and arming them (`pre-commit install`)
is impossible for the same reason as limit 6 — every hook `entry:` in `.pre-commit-config.yaml`
invokes `uv run --locked`, which refuses on this host's `uv 0.8.17` against the `==0.11.19` pin.
So `consumer_at_landing`, `audit-title-gate`, `validate-hermetization` and `audit-health` were
**not** exercised by this landing. Two of them were checked by hand instead and both pass:
`consumer_at_landing._CITATION_RES` matches three classes in this file (a backlog row, an ADR, the
standing-rulings register) against the one it requires, and `validate_hermetization.AUDIT_CLASS_ENUM`
contains `technical`, this file's class token. `audit-title-gate` is satisfied by construction —
the file opens with a `# ` heading. **`audit-health` was not run in any form.** The integrator's
merge is where these actually fire.
