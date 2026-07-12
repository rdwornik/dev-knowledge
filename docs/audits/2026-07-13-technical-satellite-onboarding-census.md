# Satellite onboarding census — four methodology consumers

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-13
- **Source-session:** `docs/satellite-census` at hub baseline `dc205263`; sibling repos read-only at the SHAs recorded below
- **Status:** complete census; tier assignments and onboarding prompts are DRAFT proposals, not executed
- **Model:** `gpt-5.6-sol`

## Executive so-what

All four satellites were readable and clean at the worktree level. None has the settled Form-A CLAUDE marker topology, `protocols/`, or `.methodology.yaml`; only `corp-sca-time-automation` has a methodology floor, and that floor's SHA is valid but its second SessionStart guard is absent. The proposed rollout profile is **full gate set** for the three repos whose work can mutate corporate systems or publish sensitive artifacts (`corp-ops`, `corp-sca-time-automation`, `demo-prep`) and **floor-only** for the docs-heavy `life-architect`, preserving its explicit ADR-04 light-governance choice (`../life-architect/ARCHITECTURE.md:27-33`; `../life-architect/CLAUDE.md:93-100`). These are onboarding profiles, not a revival of the retired formal repo-tier system.

The dominant change is template synchronization, not local-content replacement: 32 of 36 requested surface rows are `TEMPLATE-SYNC`, two are `DECLARE-LOCAL`, and two are `N-A-for-tier`. Every proposed prompt therefore freezes repo-local substance, materializes the eight hub regions byte-for-byte, runs a deterministic byte-match test, performs a second-reader review before STOP, commits on a repo-local branch, and leaves merge/push to the operator. This follows the two proven consumer arcs: ai-council materialized all eight regions and preserved its local rules (`../ai-council/JOURNAL.md:36-42`); corp-monorepo did the same, including review-before-STOP and local divergence retention (`../corp-monorepo/JOURNAL.md:38-43`).

## Authority and interpretation

The settled ownership manifest defines `MUST`, `SHOULD`, `LOCAL-declared`, and `IGNORE`, plus role-inverse rules (`docs/intake/2026-07-11-tech-ownership-manifest.md:12-16`, `:18-46`). In particular, every consumer MUST carry the seven-doc spine, a Form-A CLAUDE contract, a hash-guarded floor, a tag-pinned pre-commit surface, `.gitignore`/`.gitattributes`, and `.methodology.yaml` (`docs/intake/2026-07-11-tech-ownership-manifest.md:18-30`). The eight hub-owned CLAUDE bodies come from `templates/claude-regions/*.md`, while repo identity, commands, hooks, domain rules, and other project facts remain `owner=repo` (`templates/CLAUDE-md-template.md:21-142`).

Two terms below must not be conflated:

- **Manifest tier** means the settled artifact disposition (`MUST` / `SHOULD` / `LOCAL` / `IGNORE`).
- **Onboarding profile** means this census's proposed enforcement depth: **full gate set** or **floor-only**. It is a rollout choice, not repo metadata.

Proposed profile contents:

- **Full gate set:** methodology floor + sidecar + commit-time and SessionStart guards; hook self-arm; `canonical_freshness`; `validate-backlog`; portable `backlog-id-on-close` and `block-ff-push`; deterministic session-end backpressure; repo-local ruff/invariant gates; `normalize-headers` and audit-casing where their file scopes exist. Codemap/ToC gates remain conditional on a compatible generated surface, never installed merely for parity. The carrier doctrine requires configured → armed → functionally proven, not presence alone (`protocols/PLAYBOOK.md:1637-1661`).
- **Floor-only:** the non-waivable floor, sidecar, commit-time guard, SessionStart presence check, and hook self-arm, plus the repo's existing local quality gates. The larger freshness/closure/backlog mesh is omitted only through a time-boxed `.methodology.yaml` declaration.

## Scope and read-only method

The four sibling repos were inspected read-only. No sibling file, branch, index, environment, cache, or git configuration was changed. Census commands were limited to `git status`, `git log`, `git ls-files`, `git check-ignore`, file reads, hashes, and in-memory comparisons. The sole write authorized by this session is this audit in the hub.

Snapshot metrics count tracked files from `git ls-files`; `code` includes Python, PowerShell, JavaScript/TypeScript, SQL, and shell/batch extensions; `docs` includes Markdown/RST/text. Activity is the number of commits authored in the previous 30 days at census time.

```text
repo|read state|branch / HEAD|tracked|code|docs|30d commits
corp-ops|READABLE; worktree clean|main ahead 4 / d040fcb|59|35|18|8
corp-sca-time-automation|READABLE; worktree clean|feature/tenrox-loader / 3661b3a|75|41|19|6
life-architect|READABLE; worktree clean|main ahead 4 / 7688b76|45|2|37|45
demo-prep|READABLE; worktree clean|main ahead 53 / 51b5a63|864|57|137|159
```

The branch/ahead states are execution preconditions, not defects. An onboarding run must never reset, pull, merge, or push merely to normalize them.

## Tier-assignment proposals

### corp-ops — full gate set

`corp-ops` is small-to-medium by footprint but code-heavy (35 code files versus 18 text docs) and operationally high-consequence: its Python and PowerShell surfaces perform OneDrive/SharePoint CRUD, backups, sync, and scheduled health checks (`../corp-ops/ARCHITECTURE.md:14-19`, `:66-70`). Its invariants include explicit confirmation for destructive work and a hard prohibition on writes into Blue Yonder OneDrive paths (`../corp-ops/ARCHITECTURE.md:113-134`). That risk profile outweighs its modest activity and test count. Proposal: full methodology gate set, while every auth, path, PowerShell, and OneDrive safety rule remains repo-local and untouched.

### corp-sca-time-automation — full gate set

This is a medium, code-heavy automation repo (41 code files, 19 docs, 19 tracked test-path files) whose pipeline ends in a reviewed upload to SharePoint/Upland PSA (`../corp-sca-time-automation/ARCHITECTURE.md:14-18`, `:117-129`). It already has a valid floor hash and commit-time floor guard, so onboarding completes a proven partial carrier rather than starting cold; however, the live checkout is on `feature/tenrox-loader`, and the current Tenrox work includes a browser-post write path and credential escalation (`../corp-sca-time-automation/BACKLOG.md:40-46`). Proposal: full gate set, but only after that feature branch is dispositioned and the repo is back on a clean operator-approved baseline.

### life-architect — floor-only

`life-architect` is highly active because it is new, but structurally docs-heavy: 37 text docs, two code files, one tracked test path, and a placeholder Python package. Its architecture explicitly describes the repo as a governed content/persistence layer with no meaningful code graph (`../life-architect/ARCHITECTURE.md:27-42`). ADR-04 deliberately keeps governance light and defers the enforcement mesh (`../life-architect/CLAUDE.md:93-100`; `../life-architect/CONTRIBUTING.md:53-65`). Proposal: floor-only, retaining the current baseline hygiene/ruff hooks as LOCAL. This supplies the always-loaded methodology and floor integrity without silently overruling a settled local ADR.

### demo-prep — full gate set

`demo-prep` is artifact/docs-heavy rather than a conventional package, but it is the largest and most active satellite by far (864 tracked files; 159 commits in 30 days) and includes 57 code files supporting deck production. Its core boundaries prevent tracked Office binaries, secrets, customer deliverables, and unsafe remote publication (`../demo-prep/ARCHITECTURE.md:20-29`, `:39-45`). It already has repo-local ruff and pre-push invariant gates (`../demo-prep/.pre-commit-config.yaml:20-40`). Proposal: full gate set layered around those local gates. The onboarding must not touch deck binaries, output trees, frozen generators, brand/knowledge payload, or the immutable local handoff bundle.

## Gap table — corp-ops

```text
surface|current state|disposition|evidence / note
CLAUDE.md + regions|12-section prose exists; 0 methodology markers; no floor import; obsolete live /boot roster|TEMPLATE-SYNC|../corp-ops/CLAUDE.md:12-20, :66-77
floor + sha + guard|floor, sidecar, checker, and both guards absent; whole .claude dir is ignored|TEMPLATE-SYNC|../corp-ops/.gitignore:40-41; tracked .claude roster is only the three local rules + settings
CONTRIBUTING / LESSONS / JOURNAL shells|all three exist but preambles/contracts predate the canonical shells|TEMPLATE-SYNC|../corp-ops/CONTRIBUTING.md:11-36; ../corp-ops/LESSONS.md:1-9; ../corp-ops/JOURNAL.md:1-9
BACKLOG schema|story-map substance exists, but theme/story lack [E<n>]/[S<n>] ids and no validator is wired|TEMPLATE-SYNC|../corp-ops/BACKLOG.md:3-19; ../corp-ops/CLAUDE.md:75-77
.gitignore + .gitattributes|local ignores are useful, but bare .claude/ blocks track-by-default; .gitattributes absent|TEMPLATE-SYNC|../corp-ops/.gitignore:1-47
pre-commit gates per profile|no pre-commit config; lint/tests manual|TEMPLATE-SYNC|../corp-ops/CONTRIBUTING.md:34-45; ../corp-ops/ARCHITECTURE.md:273-278
protocols/|absent|TEMPLATE-SYNC|manifest SHOULD interface shell; preserve hub-centralized handoff pointer at ../corp-ops/CONTRIBUTING.md:53-57
.methodology.yaml|absent|TEMPLATE-SYNC|consumer MUST; seed the register and declare only evidenced local surfaces
.env hygiene|repo .env absent and ignored; secrets explicitly external|N-A-for-tier|../corp-ops/.gitignore:25-32; ../corp-ops/CLAUDE.md:51-56
```

### Preserve untouched — corp-ops

- OneDrive/SharePoint safety and the sanctioned read-only `sync-mywork.ps1` exception (`../corp-ops/CLAUDE.md:49-56`; `../corp-ops/ARCHITECTURE.md:113-134`).
- The three auth models, `config/paths.yaml` authority, package/module map, CLI catalog, PowerShell/browser manual surfaces, and their ASCII-only convention (`../corp-ops/CLAUDE.md:30-47`; `../corp-ops/ARCHITECTURE.md:139-155`, `:195-249`).
- Repo-local `.claude/rules/{code-standards,python-env,testing}.md`, named in `../corp-ops/CLAUDE.md:70-73`.
- Secret, state, data, and log ignore payloads; template sync may alter only the generic `.claude` tracking block and add the canonical EOL baseline (`../corp-ops/.gitignore:28-47`).
- Existing `docs/{audits,decisions,archive}` and the explicit no-local-ADR/hub-handoff policy (`../corp-ops/CONTRIBUTING.md:47-57`).

## Gap table — corp-sca-time-automation

```text
surface|current state|disposition|evidence / note
CLAUDE.md + regions|0 methodology markers; floor import exists; §9 falsely says the floor hook was removed although the hook is live|TEMPLATE-SYNC|../corp-sca-time-automation/CLAUDE.md:12-21, :75-77; ../corp-sca-time-automation/.pre-commit-config.yaml:1-10
floor + sha + guard|floor/sidecar/checker tracked; LF-normalized SHA matches 4d268f...; commit guard live; SessionStart presence/self-arm guard absent|TEMPLATE-SYNC|../corp-sca-time-automation/CLAUDE.md:12-14; ../corp-sca-time-automation/.claude/settings.json:1-14
CONTRIBUTING / LESSONS / JOURNAL shells|all exist but use older local preambles; CONTRIBUTING also incorrectly says no pre-commit config|TEMPLATE-SYNC|../corp-sca-time-automation/CONTRIBUTING.md:11-35; ../corp-sca-time-automation/LESSONS.md:1-9; ../corp-sca-time-automation/JOURNAL.md:1-8
BACKLOG schema|story map exists; themes/stories lack E/S ids; no validate-backlog gate|TEMPLATE-SYNC|../corp-sca-time-automation/BACKLOG.md:3-28, :40-46
.gitignore + .gitattributes|local data/.env ignores useful; bare .claude/ conflicts with track-by-default; .gitattributes absent|TEMPLATE-SYNC|../corp-sca-time-automation/.gitignore:25-43
pre-commit gates per profile|only floor-hash-verify is configured; full profile incomplete|TEMPLATE-SYNC|../corp-sca-time-automation/.pre-commit-config.yaml:1-10
protocols/|absent|TEMPLATE-SYNC|manifest SHOULD interface shell; existing operator guide remains docs-local
.methodology.yaml|absent|TEMPLATE-SYNC|consumer MUST; record requirements.txt/no-pyproject and any gate exceptions only after operator ruling
.env hygiene|root .env exists, is untracked+ignored, and contains IDs plus a short-lived token; never copy/display values|DECLARE-LOCAL|../corp-sca-time-automation/.env:1-7; ../corp-sca-time-automation/.gitignore:25-26; ../corp-sca-time-automation/CONTRIBUTING.md:44-54
```

### Preserve untouched — corp-sca-time-automation

- Pipeline order, human Excel-review gate, idempotent upload, config expansion, and AI fallback invariants (`../corp-sca-time-automation/ARCHITECTURE.md:57-70`, `:117-142`).
- The current Tenrox feature work: payload builder, console uploader, audit evidence, operator guide, config mapping, and BACKLOG #8/#9 (`../corp-sca-time-automation/docs/tenrox-console-uploader.md:1-41`; `../corp-sca-time-automation/BACKLOG.md:40-46`).
- The ignored `.env` file and every value in it; onboarding may document keys but must never print, stage, copy, rewrite, or hash secret values (`../corp-sca-time-automation/.env:1-7`).
- The explicit `requirements.txt` dependency model and current no-`pyproject.toml` choice until the manifest conflict is operator-ruled (`../corp-sca-time-automation/ARCHITECTURE.md:144-146`).
- Repo-local `.claude/rules/{code-standards,python-env,testing}.md`, named in `../corp-sca-time-automation/CLAUDE.md:70-73`.

## Gap table — life-architect

```text
surface|current state|disposition|evidence / note
CLAUDE.md + regions|current 12-section local contract; 0 methodology markers; no floor import; local ADR-04 rules are substantive|TEMPLATE-SYNC|../life-architect/CLAUDE.md:15-25, :49-65, :93-100
floor + sha + guard|floor, sidecar, checker, settings guard, and import absent|TEMPLATE-SYNC|../life-architect/CLAUDE.md:15-25; tracked .claude surface is heartbeat only at :75-82
CONTRIBUTING / LESSONS / JOURNAL shells|LESSONS is close to canon; CONTRIBUTING/JOURNAL are local variants; preserve all existing entries byte-untouched|TEMPLATE-SYNC|../life-architect/CONTRIBUTING.md:11-34; ../life-architect/LESSONS.md:1-13; ../life-architect/JOURNAL.md:1-17
BACKLOG schema|story map exists but lacks E/S ids and retains completed items/inline history; no validator by ADR-04|TEMPLATE-SYNC|../life-architect/BACKLOG.md:3-25, :27-38, :42-58; ../life-architect/ARCHITECTURE.md:102-109
.gitignore + .gitattributes|track-by-default .claude policy is good; .env is not ignored; EOL file is close but not the current fleet baseline|TEMPLATE-SYNC|../life-architect/.gitignore:1-17; ../life-architect/.gitattributes:1-11
pre-commit gates per profile|baseline hygiene + ruff are intentional; full mesh explicitly deferred|DECLARE-LOCAL|../life-architect/.pre-commit-config.yaml:1-18; ../life-architect/CONTRIBUTING.md:53-65
protocols/|absent|TEMPLATE-SYNC|manifest SHOULD interface shell; keep hub pointers, never copy PLAYBOOK/ESSENTIALS
.methodology.yaml|absent|TEMPLATE-SYNC|consumer MUST; encode floor-only/ADR-04 omissions with reason + review date
.env hygiene|no repo .env and no ignore rule; secrets doctrine uses external .secrets/.env|TEMPLATE-SYNC|../life-architect/.gitignore:1-17; ../life-architect/JOURNAL.md:17-23
```

### Preserve untouched — life-architect

- All `seed/` source/extract content, U-item IDs, Polish verbatim text, provenance links, and the Downloads no-touch rule (`../life-architect/ARCHITECTURE.md:44-60`, `:86-98`; `../life-architect/CLAUDE.md:54-63`).
- The no-corporate-content and private-repo boundaries (`../life-architect/CLAUDE.md:49-63`).
- `dimensions/`, root `intake/`, local ADR-01..07, `OPEN-QUESTIONS.md`, and every existing knowledge/lived-content file.
- The repo-local `/heartbeat` command and its Sunday ritual contract (`../life-architect/CLAUDE.md:75-82`; `../life-architect/JOURNAL.md:29-32`).
- ADR-04's light-governance posture and the existing baseline hook set; onboarding adds only floor integrity unless the operator explicitly expands the profile (`../life-architect/CONTRIBUTING.md:53-65`).

## Gap table — demo-prep

```text
surface|current state|disposition|evidence / note
CLAUDE.md + regions|local 12-section contract; 0 methodology markers; no floor import; several critical domain rules|TEMPLATE-SYNC|../demo-prep/CLAUDE.md:13-22, :34-59
floor + sha + guard|floor, sidecar, checker, settings guard, and import absent|TEMPLATE-SYNC|../demo-prep/CLAUDE.md:13-22, :68-84
CONTRIBUTING / LESSONS / JOURNAL shells|minimal local variants; no canonical CONTRIBUTING sections; preserve all append-only entries|TEMPLATE-SYNC|../demo-prep/CONTRIBUTING.md:1-23; ../demo-prep/LESSONS.md:1-7; ../demo-prep/JOURNAL.md:1-8
BACKLOG schema|large story-like file but no E/S ids; done items remain; several task-band shapes are noncanonical|TEMPLATE-SYNC|../demo-prep/BACKLOG.md:67-89, :127-145
.gitignore + .gitattributes|rich local binary/secret/output policy must remain; .gitattributes absent|TEMPLATE-SYNC|../demo-prep/.gitignore:1-67
pre-commit gates per profile|local ruff pre-commit + repo-invariants pre-push exist; methodology mesh deferred|TEMPLATE-SYNC|../demo-prep/.pre-commit-config.yaml:20-40; ../demo-prep/CLAUDE.md:82-84
protocols/|absent|TEMPLATE-SYNC|manifest SHOULD interface shell; do not turn local pipeline docs into methodology protocols
.methodology.yaml|absent|TEMPLATE-SYNC|consumer MUST; declare deck/artifact gates and local audit naming as LOCAL
.env hygiene|repo .env absent and ignored; repo forbids secrets entirely|N-A-for-tier|../demo-prep/.gitignore:36-41; ../demo-prep/CLAUDE.md:50-55
```

### Preserve untouched — demo-prep

- All deck binaries, `output/`, `examples/`, preview/render trees, brand assets/specs, knowledge corpus, templates, and migrated artifacts (`../demo-prep/ARCHITECTURE.md:20-29`; `../demo-prep/CLAUDE.md:34-59`).
- The complete project-specific `.gitignore` payload, including binary, confidential-source, output, secret, and scratch protections (`../demo-prep/.gitignore:1-67`).
- The repo-local ruff and `repo-invariants` hooks; full-profile gates are additive and must not weaken their pre-commit/pre-push stages (`../demo-prep/.pre-commit-config.yaml:20-40`).
- Local ADR-001/002, audit naming/rulings, `SOURCES.md`, pipeline process docs, frozen generators, and every append-only LESSONS/JOURNAL entry (`../demo-prep/CLAUDE.md:93-100`; `../demo-prep/JOURNAL.md:5-19`).
- `docs/handoffs/2026-07-08-v2-closeout/**` is immutable and must not be edited or deleted. It conflicts with the settled consumer inverse rule and needs a separate relocation ruling, not an onboarding guess (`docs/intake/2026-07-11-tech-ownership-manifest.md:29-32`; `../demo-prep/docs/handoffs/2026-07-08-v2-closeout/HANDOFF_BOOT.md:1`).

## Manifest completeness outside the requested nine surfaces

These are blockers/plan-gate questions, not hidden assumptions and not included in the 36-row disposition count:

- `corp-ops` has a root `INSTALL.md`, but it is not byte-equal to the hub's current canonical plugin install document; `docs/intake/` is absent.
- `corp-sca-time-automation` lacks root `INSTALL.md` and `docs/intake/`; its explicit `requirements.txt`/no-`pyproject.toml` architecture conflicts with the manifest's Tier-1 `pyproject.toml` row (`../corp-sca-time-automation/ARCHITECTURE.md:144-146`).
- `life-architect` lacks root `INSTALL.md` and the manifest's `docs/{audits,intake,archive}` shape; it intentionally uses root `intake/`. No canonical migration source was identified, so the onboarding prompt must surface a structured operator choice rather than move content.
- `demo-prep` lacks root `INSTALL.md` and carries the inverse-rule `docs/handoffs/` violation described above.

## DRAFT onboarding prompt — corp-ops

```text
| Parameter | Value |
| Model | CC pick (Opus-class judgment expected) |
| Mode | plan |
| Effort | high |

TITLE: Onboard corp-ops to the settled fleet template, full-gate profile
REPO: C:\Users\1028120\Documents\Dev\corp-ops
PURPOSE: Bring the nine censused methodology surfaces to canonical form while preserving every operational and OneDrive safety invariant.

READ FIRST:
- C:\Users\1028120\Documents\Dev\corp-ops\CLAUDE.md and ARCHITECTURE.md.
- C:\Users\1028120\Documents\Dev\.dev-knowledge\docs\intake\2026-07-11-tech-ownership-manifest.md.
- C:\Users\1028120\Documents\Dev\.dev-knowledge\templates\CLAUDE-md-template.md, templates\claude-regions\*.md, and the CONTRIBUTING/LESSONS/JOURNAL templates.
- The hub JOURNAL entry for the proven corp/ai consumer shape (2026-07-13 content-parity baseline).

NON-NEGOTIABLE SCOPE:
- Profile = FULL GATE SET.
- Preserve untouched: src/, tools/, scripts/, config/, tests/, assets/, data/, all OneDrive/auth/path rules, .claude/rules/*, and existing docs payload.
- Never execute operational scripts or touch any OneDrive path.
- Never merge, push, reset, pull, or rewrite unrelated history.

PRE-FLIGHT:
1. Read-only: git status, branch, log -5, tracked-tree census, pytest --collect-only. If the tree is dirty or not on the operator-approved main baseline, STOP and report; do not repair it.
2. PLAN ONLY. Produce an addressable plan mapping every census row to exact files, exact canonical source, preserved local text, and the final hook id/stage roster. Surface the drifted INSTALL.md and missing docs/intake shape as typed operator choices. Do not edit before ExitPlanMode approval.

AFTER PLAN APPROVAL:
3. Create branch chore/methodology-onboarding.
4. Materialize the 15-region CLAUDE topology: exactly 8 owner=hub bodies byte-verbatim from templates/claude-regions and 7 owner=repo regions around all corp-ops content. Add the floor import/boundary note. Do not paraphrase hub bodies.
5. Provision the floor, sidecar, checker, SessionStart presence+self-arm pair, and commit-time floor-hash hook from hub-canonical sources. Normalize .gitignore to track .claude by default while retaining every local secret/data/log rule.
6. Adopt canonical CONTRIBUTING/LESSONS/JOURNAL shells. Existing LESSONS/JOURNAL entries are immutable: preamble-only changes, zero entry-body changes.
7. Migrate BACKLOG headings to E/S ids without changing task ids or work substance; wire validate-backlog. Add protocols/ interface shell and .methodology.yaml. Adopt the fleet .gitattributes baseline, including CRLF checkout for *.ps1.
8. Build the full profile: floor-hash, canonical_freshness, validate-backlog, backlog-id-on-close, block-ff-push, session-end backpressure, ruff, normalize-headers, and audit-casing where applicable. Codemap/ToC hooks are N/A unless a compatible generated surface is proven. Preserve local gates/rules as LOCAL.

CLOSURE CONTRACT — ALL REQUIRED BEFORE STOP:
9. BYTE-MATCH TEST (PowerShell, run from repo root):
   $hub='C:\Users\1028120\Documents\Dev\.dev-knowledge\templates\claude-regions'
   $raw=[IO.File]::ReadAllText('CLAUDE.md').Replace("`r`n","`n")
   $ids=@('antipatterns-universal','conventions-commit-branch','conventions-output-formatting','critical-rules-consistency','critical-rules-no-leftovers','critical-rules-records','first-read','session-start-protocol')
   $found=[regex]::Matches($raw,'(?m)^<!-- methodology:start id=[^ ]+ owner=hub -->$')
   if($found.Count -ne 8){throw "owner=hub region count $($found.Count), expected 8"}
   foreach($id in $ids){$e=[regex]::Escape($id);$m=[regex]::Match($raw,"(?ms)^<!-- methodology:start id=$e owner=hub -->\n(?<body>.*?)^<!-- methodology:end id=$e -->");if(!$m.Success){throw "missing $id"};$want=[IO.File]::ReadAllText((Join-Path $hub ($id+'.md'))).Replace("`r`n","`n");if($m.Groups['body'].Value -cne $want){throw "drift $id"}}
   'BYTE-MATCH PASS: 8/8'
10. Run validate-backlog, the real repo test/lint commands, pre-commit --all-files, and explicit commit-msg/pre-push stage checks. Trip-test floor-hash once (must block a staged one-byte floor change), then restore only that probe and verify no leftovers.
11. REVIEW-BEFORE-STOP: run `codex exec -m gpt-5.6-sol --sandbox read-only "Review git diff main...HEAD for disposition-faithfulness, hub-only leaks, OneDrive safety regressions, hook-stage mistakes, and local-content loss. Cite path:line; report CRITICAL/HIGH only."`. Fix every actionable finding; rerun steps 9-10. Review may not be deferred to the operator.
12. Add the canonical JOURNAL entry naming at least one work SHA, commit all approved changes, and leave git status clean. Report commits, tests, byte-match, trip-test, review verdict, and remaining plan-gate decisions. COMMIT-AND-STOP: do not merge or push.
```

## DRAFT onboarding prompt — corp-sca-time-automation

```text
| Parameter | Value |
| Model | CC pick (Opus-class judgment expected) |
| Mode | plan |
| Effort | high |

TITLE: Complete corp-sca-time-automation onboarding, full-gate profile
REPO: C:\Users\1028120\Documents\Dev\corp-sca-time-automation
PURPOSE: Complete the partial floor carrier and synchronize governance surfaces without touching Tenrox work, upload logic, or secret values.

READ FIRST: repo CLAUDE.md + ARCHITECTURE.md; hub ownership manifest; hub CLAUDE/CONTRIBUTING/LESSONS/JOURNAL templates; the 2026-07-13 proven consumer JOURNAL entry.

NON-NEGOTIABLE SCOPE:
- Profile = FULL GATE SET.
- Current census is on feature/tenrox-loader. If that branch is still active, STOP at pre-flight; onboarding starts only from an operator-approved clean main baseline.
- Preserve untouched: src/, scripts/, config/, tests/, data/, Tenrox audits/guide/uploader/mapping, requirements.txt, all pipeline rules, and every .env value. Never print or copy .env values.
- No Upland, SharePoint, Graph, browser, or upload command may run.

PLAN GATE:
1. Read-only status/log/tree/test discovery. Produce an addressable plan for the nine surfaces, the stale CLAUDE §9 claim, the existing valid floor, exact hook roster/stages, and local preserve list. Surface the no-pyproject manifest conflict and missing INSTALL/docs-intake as structured operator choices. No edits before approval.

AFTER APPROVAL:
2. Create chore/methodology-onboarding. Materialize 8 exact hub regions + 7 repo regions; retain the existing floor import and every local pipeline/Tenrox rule.
3. Keep the valid floor/sidecar/checker bytes; add the missing SessionStart --require-present + pre_commit install pair. Reconcile CLAUDE §9 and CONTRIBUTING to live state.
4. Adopt canonical governance shells without changing any existing LESSONS/JOURNAL entry. Add E/S BACKLOG ids without changing task ids or substance. Add protocols/ and .methodology.yaml; declare the ignored local .env without its values.
5. Normalize .gitignore/.gitattributes and install the full profile around the existing floor hook: canonical_freshness, validate-backlog, backlog-id-on-close, block-ff-push, session-end backpressure, repo-local ruff, normalize-headers, audit-casing. Codemap/ToC N/A unless proven compatible.

CLOSURE CONTRACT:
6. BYTE-MATCH TEST:
   $hub='C:\Users\1028120\Documents\Dev\.dev-knowledge\templates\claude-regions';$raw=[IO.File]::ReadAllText('CLAUDE.md').Replace("`r`n","`n");$ids=@('antipatterns-universal','conventions-commit-branch','conventions-output-formatting','critical-rules-consistency','critical-rules-no-leftovers','critical-rules-records','first-read','session-start-protocol');if(([regex]::Matches($raw,'(?m)^<!-- methodology:start id=[^ ]+ owner=hub -->$')).Count -ne 8){throw 'owner=hub count'};foreach($id in $ids){$e=[regex]::Escape($id);$m=[regex]::Match($raw,"(?ms)^<!-- methodology:start id=$e owner=hub -->\n(?<body>.*?)^<!-- methodology:end id=$e -->");$w=[IO.File]::ReadAllText((Join-Path $hub ($id+'.md'))).Replace("`r`n","`n");if(!$m.Success -or $m.Groups['body'].Value -cne $w){throw "drift $id"}};'BYTE-MATCH PASS: 8/8'
7. Run pytest, ruff, validate-backlog, all hook stages, and a floor poison/block/restore trip-test. Verify .env remains ignored, untracked, byte-unchanged, and absent from every diff/output. Verify no leftovers.
8. REVIEW-BEFORE-STOP: run `codex exec -m gpt-5.6-sol --sandbox read-only "Review git diff main...HEAD for template fidelity, secret leakage, upload/Tenrox drift, hook-stage mistakes, and local-content loss. Cite path:line; report CRITICAL/HIGH only."`. Fix actionable findings and rerun 6-7.
9. Add a canonical JOURNAL entry with work SHA(s), commit, verify clean. Report evidence. COMMIT-AND-STOP; no merge/push.
```

## DRAFT onboarding prompt — life-architect

```text
| Parameter | Value |
| Model | CC pick (Opus-class judgment expected) |
| Mode | plan |
| Effort | high |

TITLE: Onboard life-architect to the settled fleet template, floor-only profile
REPO: C:\Users\1028120\Documents\Dev\life-architect
PURPOSE: Add the always-loaded methodology floor and canonical document shells while preserving ADR-04 light governance and all personal/lived content.

READ FIRST: repo CLAUDE.md + ARCHITECTURE.md + ADR-04; hub ownership manifest; canonical templates; proven 2026-07-13 consumer JOURNAL entry.

NON-NEGOTIABLE SCOPE:
- Profile = FLOOR-ONLY. Do not add canonical_freshness, session-end backpressure, validate-backlog, block-ff-push, audit-casing, codemap, or ToC gates unless the operator explicitly expands the profile at the plan gate.
- Preserve untouched: seed/**, dimensions/**, intake/**, docs/decisions/**, OPEN-QUESTIONS.md, heartbeat command, every lived-content/Polish passage, every U-id/provenance edge, and all existing LESSONS/JOURNAL entries.
- Never read/write Downloads, corporate data, secrets, health source data outside tracked text, or remote privacy settings.

PLAN GATE:
1. Read-only pre-flight. If dirty/off the approved baseline, STOP. Produce an addressable plan for all nine surfaces. Explicitly map ADR-04 omissions into .methodology.yaml with reasons + review date. Present typed choices for (a) completed BACKLOG items and inline history, (b) root intake versus manifest docs/intake, and (c) missing INSTALL/docs genres. No edits before approval.

AFTER APPROVAL:
2. Branch chore/methodology-onboarding. Materialize 8 exact hub regions + 7 repo regions; all privacy, seed, D04-only, heartbeat, language, and lived-closure rules remain owner=repo.
3. Add floor, sidecar, checker, CLAUDE import, SessionStart presence+self-arm pair, and commit-time floor hash. Preserve existing hygiene/ruff hooks exactly and declare them LOCAL.
4. Adopt canonical CONTRIBUTING/LESSONS/JOURNAL shells; zero changes below the existing entry boundaries. Add E/S BACKLOG ids mechanically; do not remove/close/rewrite a task unless the approved plan selected that exact disposition.
5. Add protocols/ interface shell, .methodology.yaml, canonical .gitattributes baseline, and .env ignore. Keep PLAYBOOK/ESSENTIALS as hub pointers only.

CLOSURE CONTRACT:
6. BYTE-MATCH TEST:
   $hub='C:\Users\1028120\Documents\Dev\.dev-knowledge\templates\claude-regions';$raw=[IO.File]::ReadAllText('CLAUDE.md').Replace("`r`n","`n");$ids=@('antipatterns-universal','conventions-commit-branch','conventions-output-formatting','critical-rules-consistency','critical-rules-no-leftovers','critical-rules-records','first-read','session-start-protocol');if(([regex]::Matches($raw,'(?m)^<!-- methodology:start id=[^ ]+ owner=hub -->$')).Count -ne 8){throw 'owner=hub count'};foreach($id in $ids){$e=[regex]::Escape($id);$m=[regex]::Match($raw,"(?ms)^<!-- methodology:start id=$e owner=hub -->\n(?<body>.*?)^<!-- methodology:end id=$e -->");$w=[IO.File]::ReadAllText((Join-Path $hub ($id+'.md'))).Replace("`r`n","`n");if(!$m.Success -or $m.Groups['body'].Value -cne $w){throw "drift $id"}};'BYTE-MATCH PASS: 8/8'
7. Run the existing seven baseline hooks + ruff, pytest, and a floor poison/block/restore trip-test. If the recorded process-spawn hang recurs, STOP and report; do not use --no-verify unless the operator separately invokes the repo's already-recorded managed exception. Verify seed/** has zero diff and no leftovers.
8. REVIEW-BEFORE-STOP: run `codex exec -m gpt-5.6-sol --sandbox read-only "Review git diff main...HEAD for privacy or corporate-scope leaks, seed mutation, ADR-04 overreach, local-content loss, and byte fidelity. Cite path:line; report CRITICAL/HIGH only."`. Fix actionable findings and rerun 6-7.
9. Add canonical JOURNAL entry with work SHA(s), commit, verify clean. COMMIT-AND-STOP; no merge/push.
```

## DRAFT onboarding prompt — demo-prep

```text
| Parameter | Value |
| Model | CC pick (Opus-class judgment expected) |
| Mode | plan |
| Effort | high |

TITLE: Onboard demo-prep to the settled fleet template, full-gate profile
REPO: C:\Users\1028120\Documents\Dev\demo-prep
PURPOSE: Add the full methodology mesh around the existing deck safety gates without touching any deck, artifact payload, or immutable record.

READ FIRST: repo CLAUDE.md + ARCHITECTURE.md + ADR-001/002; hub ownership manifest and canonical templates; proven 2026-07-13 consumer JOURNAL entry.

NON-NEGOTIABLE SCOPE:
- Profile = FULL GATE SET.
- Preserve untouched: brand/**, templates/** payloads, knowledge/**, pipeline/** payloads, generators/**, examples/**, output/**, SOURCES.md, every binary/render, and all existing audit/decision/handoff/LESSONS/JOURNAL bodies.
- Never touch MyWork, Warsaw archive, OneDrive, PowerPoint, LibreOffice, COM, source decks, or remotes. Do not run deck generators.
- Existing ruff and repo-invariants stages stay functional and may not be weakened.

PLAN GATE:
1. Read-only pre-flight. Produce an exact nine-surface plan plus the settled-manifest extras. The local docs/handoffs bundle is an inverse-rule conflict: present a structured choice — (A) separately relocate/hash-verify it into the hub under an operator-approved immutable-record plan, or (B) hold onboarding with the ERROR open. Never delete, edit, or locally waive it. Present all other unresolved choices similarly. No edits before approval.

AFTER APPROVAL:
2. Create chore/methodology-onboarding. Materialize 8 exact hub regions + 7 repo regions, preserving all brand, grounding, binary, output, no-push, and immutable-generator rules as owner=repo.
3. Add floor/sidecar/checker/import, SessionStart presence+self-arm, commit floor guard, canonical shells, E/S BACKLOG headings, protocols/ interface shell, .methodology.yaml, and canonical EOL baseline. Preserve the entire local .gitignore payload; only add generic tracking/EOL rules.
4. Add the full profile around the existing gates: canonical_freshness, validate-backlog, backlog-id-on-close, block-ff-push, session-end backpressure, normalize-headers, audit-casing, floor-hash. Keep ruff at pre-commit and repo-invariants at pre-push. Codemap/ToC N/A unless a compatible generated surface is proven.

CLOSURE CONTRACT:
5. BYTE-MATCH TEST:
   $hub='C:\Users\1028120\Documents\Dev\.dev-knowledge\templates\claude-regions';$raw=[IO.File]::ReadAllText('CLAUDE.md').Replace("`r`n","`n");$ids=@('antipatterns-universal','conventions-commit-branch','conventions-output-formatting','critical-rules-consistency','critical-rules-no-leftovers','critical-rules-records','first-read','session-start-protocol');if(([regex]::Matches($raw,'(?m)^<!-- methodology:start id=[^ ]+ owner=hub -->$')).Count -ne 8){throw 'owner=hub count'};foreach($id in $ids){$e=[regex]::Escape($id);$m=[regex]::Match($raw,"(?ms)^<!-- methodology:start id=$e owner=hub -->\n(?<body>.*?)^<!-- methodology:end id=$e -->");$w=[IO.File]::ReadAllText((Join-Path $hub ($id+'.md'))).Replace("`r`n","`n");if(!$m.Success -or $m.Groups['body'].Value -cne $w){throw "drift $id"}};'BYTE-MATCH PASS: 8/8'
6. Run pytest including repo-invariants, ruff, validate-backlog, every hook stage, and floor poison/block/restore. Prove git ls-files still contains no pptx/potx/docx and examples tracks only sanctioned README files. Verify all preserved payload paths have zero diff and no leftovers.
7. REVIEW-BEFORE-STOP: run `codex exec -m gpt-5.6-sol --sandbox read-only "Review git diff main...HEAD for binary or secret boundary regression, immutable-record edits, brand or pipeline payload loss, hook-stage mistakes, and hub-only leaks. Cite path:line; report CRITICAL/HIGH only."`. Fix actionable findings and rerun 5-6.
8. Add canonical JOURNAL entry with work SHA(s), commit, verify clean. Report explicit disposition of the handoff inverse-rule conflict. COMMIT-AND-STOP; no merge/push.
```

## Rollout order recommendation

Criterion: **smallest onboarding blast radius first**, scored qualitatively by (1) tracked-tree size, (2) amount of local content that must be protected, (3) carrier/gate starting state, (4) active-branch divergence, and (5) consequence of a false gate or accidental payload edit.

1. **corp-ops** — smallest stable content surface and only one backlog task; full-gate bootstrap is broad but isolated to governance/config, with runtime paths explicitly frozen.
2. **corp-sca-time-automation** — small tree and partial floor already proven, but wait until `feature/tenrox-loader` is dispositioned and return to an approved main baseline; secrets and upload surfaces stay untouched.
3. **life-architect** — floor-only keeps the mechanical change small, but privacy, immutable seed content, completed-item backlog history, and the recorded process-spawn hang raise execution/review risk.
4. **demo-prep** — last: by far the largest/most active tree, high immutable/artifact density, existing local gate stages, and an unresolved `docs/handoffs/` inverse-rule conflict.

## Count summary

```text
repos requested: 4
repos readable: 4
repos unreadable: 0
proposed full-gate profiles: 3
proposed floor-only profiles: 1
requested gap rows: 36 (9 x 4)
TEMPLATE-SYNC: 32
DECLARE-LOCAL: 2 (corp-sca .env; life-architect local hook profile)
N-A-for-tier: 2 (corp-ops .env; demo-prep .env)
CLAUDE contracts with Form-A markers: 0/4
expected hub regions present and byte-matched: 0/32
floors present: 1/4
valid floor SHA pairs: 1/4
complete two-leg floor guards: 0/4
protocols/ present: 0/4
.methodology.yaml present: 0/4
canonical .gitattributes baseline present: 0/4
BACKLOG E/S schema present: 0/4
pre-commit config present: 3/4
full-profile gate set complete: 0/3
.env hygiene already sufficient for proposed profile: 3/4
```

## Read-only close

No satellite changes were made. The prompts above are DRAFT execution contracts only. Each begins in plan mode, makes uncertainty addressable, mechanically tests the hub-region bytes, runs review before STOP, and ends committed-but-unmerged.
