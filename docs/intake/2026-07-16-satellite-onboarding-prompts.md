---
intake-id: 15
status: READY-TO-FIRE
origin: satellite tier-rulings arc, 2026-07-16 — operator rulings recorded in ecosystem/satellite-onboarding-rulings.yaml; prompts derived from the 2026-07-13 satellite onboarding census (immutable audit), with life-architect regenerated floor-only -> FULL per the operator override
note: onboarding EXECUTION contracts (not a decomposition intake); parked in docs/intake for the operator-chosen status + join-key traceability. READY-TO-FIRE is a descriptive status (OTHER group), consistent with existing custom-status intake docs (RULED, settled, plan-of-record-active).
---

# Satellite onboarding prompts — ready to fire (four consumers)

> **What this is.** The four operator-fired onboarding execution prompts, each internally
> consistent with its **ruled** onboarding profile (`ecosystem/satellite-onboarding-rulings.yaml`:
> all four **full gate set**). Three are forwarded **verbatim** from the DRAFT census
> (`docs/audits/2026-07-13-technical-satellite-onboarding-census.md`, lines 163–320); the
> **life-architect** prompt is **regenerated** from the census's floor-only draft to the
> full gate set, per the operator override (census proposed floor-only citing ADR-04; the
> operator's standing statement overrules to full).
>
> **These are NOT fired from this session.** They are parked here for status + index
> traceability. Each begins in plan mode, makes uncertainty a typed plan-gate choice,
> byte-tests the eight hub regions, reviews before STOP, and ends committed-but-unmerged.
> The census rollout-order recommendation (lines 322–329) stands: corp-ops → corp-sca
> (after `feature/tenrox-loader` is dispositioned) → life-architect → demo-prep.

---

## corp-ops — full gate set (forwarded verbatim from census lines 163–211)

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

---

## corp-sca-time-automation — full gate set (forwarded verbatim from census lines 213–248)

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

---

## life-architect — full gate set (REGENERATED from the census floor-only draft, per operator override)

> **Regeneration note.** The census (lines 250–284) authored this prompt for **floor-only**
> (title line 258; scope line 265 explicitly forbids canonical_freshness / session-end
> backpressure / validate-backlog / block-ff-push / audit-casing / codemap / ToC). The
> operator ruled **FULL** (`ecosystem/satellite-onboarding-rulings.yaml`, life-architect
> override). This prompt is regenerated to the full gate set, **preserving the census's
> protect-untouched list verbatim** (seed/**, dimensions/**, intake/**, docs/decisions/**,
> OPEN-QUESTIONS.md, /heartbeat, lived/Polish content, U-ids, existing LESSONS/JOURNAL
> entries) and adding a **mandatory plan-gate choice** for reconciling ADR-04 (whose
> light-governance posture the full mesh deliberately supersedes).

```text
| Parameter | Value |
| Model | CC pick (Opus-class judgment expected) |
| Mode | plan |
| Effort | high |

TITLE: Onboard life-architect to the settled fleet template, FULL-gate profile
REPO: C:\Users\1028120\Documents\Dev\life-architect
PURPOSE: Bring the nine censused methodology surfaces to canonical form AND install the full enforcement mesh, while preserving all personal/lived content and every seed/provenance edge.

OPERATOR OVERRIDE (binding — do not soften): the 2026-07-13 census proposed FLOOR-ONLY for this repo (docs-heavy; ADR-04 keeps governance light and defers the mesh). The operator's standing ruling OVERRIDES that to FULL GATE SET (ecosystem/satellite-onboarding-rulings.yaml, life-architect). Installing the full mesh deliberately supersedes ADR-04's light-governance deferral — this is intentional, not drift, and may not be softened back to floor-only.

READ FIRST: repo CLAUDE.md + ARCHITECTURE.md + ADR-04; hub ownership manifest; canonical templates (CLAUDE-md-template, claude-regions/*, CONTRIBUTING/LESSONS/JOURNAL); the proven 2026-07-13 consumer JOURNAL entry.

NON-NEGOTIABLE SCOPE:
- Profile = FULL GATE SET. Install: methodology floor + sidecar + commit-time floor-hash guard + SessionStart presence+self-arm pair; canonical_freshness; validate-backlog; backlog-id-on-close; block-ff-push; deterministic session-end backpressure; repo-local ruff/invariant gates (kept LOCAL); normalize-headers and audit-casing where their file scopes exist. Codemap/ToC gates remain N/A unless a compatible generated surface is proven.
- ADR-04 RECONCILIATION IS A PLAN-GATE CHOICE: installing the mesh contradicts ADR-04's light-governance posture. Surface a TYPED operator choice — (A) amend ADR-04 to record the operator's full-gate override, or (B) add a superseding local ADR — and do not silently leave ADR-04 contradicting the installed mesh. The choice is HOW to record the override, never WHETHER to onboard full.
- Preserve untouched: seed/**, dimensions/**, intake/**, docs/decisions/**, OPEN-QUESTIONS.md, the /heartbeat command and its Sunday ritual, every lived-content/Polish passage, every U-id/provenance edge, and all existing LESSONS/JOURNAL entries.
- Never read/write Downloads, corporate data, secrets, health source data outside tracked text, or remote privacy settings.

PLAN GATE:
1. Read-only pre-flight (git status/branch/log-5/tracked-tree census/pytest --collect-only). If dirty or off the operator-approved main baseline, STOP and report; do not repair. Produce an addressable plan mapping every census row to exact files, canonical source, preserved local text, and the final hook id/stage roster for the FULL profile. Declare the existing local hygiene/ruff hooks as LOCAL divergences in .methodology.yaml — the census floor-only mesh OMISSIONS do NOT apply (the mesh is installed, not omitted). Present typed choices for (a) the ADR-04 reconciliation above, (b) completed BACKLOG items and inline history, (c) root intake versus manifest docs/intake, and (d) missing INSTALL/docs genres. No edits before ExitPlanMode approval.

AFTER APPROVAL:
2. Branch chore/methodology-onboarding. Materialize the 15-region CLAUDE topology: exactly 8 owner=hub bodies byte-verbatim from templates/claude-regions and 7 owner=repo regions around all life-architect content (privacy, seed, ADR-04-only, heartbeat, language, and lived-closure rules stay owner=repo). Add the floor import/boundary note. Do not paraphrase hub bodies.
3. Provision the floor, sidecar, checker, CLAUDE import, SessionStart presence+self-arm pair, and commit-time floor-hash hook from hub-canonical sources. Preserve the existing hygiene/ruff hooks exactly and declare them LOCAL.
4. Adopt canonical CONTRIBUTING/LESSONS/JOURNAL shells; zero changes below the existing entry boundaries. Add E/S BACKLOG ids mechanically; do not remove/close/rewrite a task unless the approved plan selected that exact disposition. Wire validate-backlog.
5. Add protocols/ interface shell, .methodology.yaml, canonical .gitattributes baseline, and .env ignore. Keep PLAYBOOK/ESSENTIALS as hub pointers only.
6. Build the FULL profile around the preserved local gates: floor-hash, canonical_freshness, validate-backlog, backlog-id-on-close, block-ff-push, session-end backpressure, ruff (LOCAL), normalize-headers, and audit-casing where applicable. Codemap/ToC N/A unless a compatible generated surface is proven.

CLOSURE CONTRACT — ALL REQUIRED BEFORE STOP:
7. BYTE-MATCH TEST:
   $hub='C:\Users\1028120\Documents\Dev\.dev-knowledge\templates\claude-regions';$raw=[IO.File]::ReadAllText('CLAUDE.md').Replace("`r`n","`n");$ids=@('antipatterns-universal','conventions-commit-branch','conventions-output-formatting','critical-rules-consistency','critical-rules-no-leftovers','critical-rules-records','first-read','session-start-protocol');if(([regex]::Matches($raw,'(?m)^<!-- methodology:start id=[^ ]+ owner=hub -->$')).Count -ne 8){throw 'owner=hub count'};foreach($id in $ids){$e=[regex]::Escape($id);$m=[regex]::Match($raw,"(?ms)^<!-- methodology:start id=$e owner=hub -->\n(?<body>.*?)^<!-- methodology:end id=$e -->");$w=[IO.File]::ReadAllText((Join-Path $hub ($id+'.md'))).Replace("`r`n","`n");if(!$m.Success -or $m.Groups['body'].Value -cne $w){throw "drift $id"}};'BYTE-MATCH PASS: 8/8'
8. Run pytest, ruff, validate-backlog, all hook stages (commit-msg + pre-push explicit), and a floor poison/block/restore trip-test. If the recorded process-spawn hang recurs, STOP and report; do not use --no-verify unless the operator separately invokes the repo's already-recorded managed exception. Verify seed/** has zero diff and no leftovers.
9. REVIEW-BEFORE-STOP: run `codex exec -m gpt-5.6-sol --sandbox read-only "Review git diff main...HEAD for privacy or corporate-scope leaks, seed mutation, local-content loss, byte fidelity, hook-stage mistakes, and whether the ADR-04 reconciliation choice was honored (not silently skipped). Cite path:line; report CRITICAL/HIGH only."`. Fix every actionable CRITICAL/HIGH and rerun 7-8. Review may not be deferred to the operator.
10. Add the canonical JOURNAL entry naming at least one work SHA, commit all approved changes, and leave git status clean. Report commits, tests, byte-match, trip-test, review verdict, and the recorded ADR-04 reconciliation. COMMIT-AND-STOP: do not merge or push.
```

---

## demo-prep — full gate set (forwarded verbatim from census lines 286–320)

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
