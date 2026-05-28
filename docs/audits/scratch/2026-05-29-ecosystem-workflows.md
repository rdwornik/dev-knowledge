# Ecosystem Workflows Audit — scratch (2026-05-29)

<!-- scope: meta -->

Overnight ecosystem-coherence audit, Phase 3. Read-only trace of the documented
workflows (handoff v3.4, AI Council, dev workflow, codemap, audit.py) against
their implementations + against each other. Baseline = the fixed v3.4 handoff state.

## Inventory (Dimension A)

| Workflow | Process doc | Visual | Implementation | State |
|---|---|---|---|---|
| Handoff v3.4 | `protocols/HANDOFF_PROCESS.md` v3.4 | ARCHITECTURE.md §"Handoff process v3.4" | templates + `.claude/commands/handoff.md` (rewritten this session) | current |
| AI Council | `protocols/AI_COUNCIL_PROCESS.md` v1.0 | ARCHITECTURE.md C3 | `ai-council/src/ai_council/*.py` | current |
| Dev workflow | `PLAYBOOK.md` (complexity routing) | ARCHITECTURE.md §"Development workflow" | n/a (methodology) | current |
| Codemap | inline in `scripts/codemap/` | ARCHITECTURE.md §Codemap | `scripts/codemap/{cli,check,generator,…}.py` + pre-commit hook | current |
| Self-audit | n/a | n/a | `scripts/audit.py` (7 checks) | current |

audit.py self-checks (7/7): vision_md, adr38_baseline, claude_md, dot_prefix_discipline,
canonical_md_visibility, workspace_settings, mermaid_theme_directive.

## Findings

| ID | Sev | Dim | Evidence (file:line) | Description | Fix scope | Owner |
|---|---|---|---|---|---|---|
| WF-1 | medium | A/B | `ARCHITECTURE.md` §"Governing ADRs" (lists ADR-27…58, 60) | The governing-ADR list **omits ADR-59 and ADR-61**, both of which exist and are binding (CLAUDE.md §11 lists 57–61). ADR-59 (universal visual repository pattern) is especially load-bearing: it grounds **audit.py checks #4–#6** (dot_prefix_discipline, canonical_md_visibility, workspace_settings). A reader of ARCHITECTURE's governance section can't trace those checks to their ADR. | Add ADR-59 + ADR-61 to ARCHITECTURE governing-ADRs; cross-link ADR-59 → audit.py checks #4–#6. | self |
| WF-2 | medium | C | `ARCHITECTURE.md` §"Validators and enforcement" | Three drifts in one block: (a) "**Pre-commit:** ruff (`ruff check --fix`) + normalize_headers.py" — ruff is NOT in `.pre-commit-config.yaml` (same false claim as HK-1); (b) lists `scripts/backlog_extract.py` as a validator — **the file does not exist** (`scripts/` has only audit.py, migrate_links.py, normalize_headers.py + codemap/); (c) **omits** the real `codemap-freshness` pre-commit hook. | Correct the validators list: drop/restore backlog_extract.py, fix ruff claim, add codemap-freshness hook. | self |
| WF-3 | low | C | `ARCHITECTURE.md` §"Handoff process v3.4" s2c/s2d, s1b | Minor attribution imprecision: the diagram puts "Operator declares next_session_scope" + "Operator produces 11_CLAIMS.md" in the Stage-2 OLD-chat subgraph, but per ADR-57/58 those are the **architect/OLD-chat's** outputs (operator facilitates). Also s1b labels the 5 sections "5 SBAR/I-PASS questions" — a medical-handoff analogy not used in the spec (sections are OBJECTIVE/REALITY/RATIONALE/DIRECTIVES/BOUNDARIES). Cosmetic. | Tweak diagram labels (architect vs operator; drop SBAR/I-PASS or define it). | self |

## What works (no finding)

- **audit.py has NO handoff-structure validator** — the original audit's §6 worry
  ("does audit.py assume the old 11/12-file count?") is moot: it never validates
  handoff bundles, so the v3.4 count change introduced zero validator drift.
- **AI_COUNCIL_PROCESS.md v1.0** is internally coherent and correctly cross-references
  ARCHITECTURE C3, ADR-43 (routing), ADR-60 (taxonomy), PLAYBOOK, and the live
  `ai-council` code modules. Stage names (0–6) are consistent doc↔diagram.
- **Dimension D (post-v3.4 coherence):** ARCHITECTURE's v3.4 handoff diagram already
  reflects the *fixed* structure — 13-file bundle, 10_GATE_PROBE, 11_CLAIMS,
  next_session_scope, ancestor check, thinness pre-flight, structured ratification.
  The fix campaign did not introduce diagram drift; spec ↔ skill ↔ diagram agree.
- **codemap-freshness** pre-commit hook validates ARCHITECTURE's inline codemap vs a
  fresh generation — real, runs green.

## Notes

- WF-2(a) and HK-1 are the same fact (ruff claimed-but-unenforced) surfacing in two
  docs (ARCHITECTURE + CLAUDE.md) — fix both in one pass.
- No workflow-vs-workflow contradiction found (stage names, validators, conventions
  consistent across handoff ↔ AI Council ↔ codemap).
