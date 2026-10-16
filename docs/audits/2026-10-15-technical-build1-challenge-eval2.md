# Archive copy of transport file DIGEST-BUILD1-CHALLENGE-EVAL2-2026-10-15.md

> Provenance: verbatim copy of `to-browser/DIGEST-BUILD1-CHALLENGE-EVAL2-2026-10-15.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15 A). Source sha256[:16] dbbb4e0e327a1389. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-15
by: build1-prep (Claude Code claude-opus-5-5; contract to-cc/BATCH-BUILD1-PREP-2026-10-15 + AMEND v5 step 0)
summary: verbatim evaluator record 2 of 2 for the BUILD-1 step-0 CHALLENGE; ids re-keyed G-I<item>-<k> (decide_checks' id grammar stops at a dot), text unedited.
served-model: grok-4.20-0309-non-reasoning
attestation-source: grok -p --output-format json modelUsage key
producer-model: claude-opus-5-5
run: grok -p <challenge-prompt.md> --max-turns 30 --output-format json --deny Write --deny Edit; 2026-10-15T09:35:17Z-09:35:51Z; 4 turns; $0.0919; exit 0

# EVAL 2 - BUILD-1 CHALLENGE (Grok)

### I1
- id: G-I1-1 -- Linux-first CI with nightly Windows is worse than current conductor.yml (already Linux-primary with path-filtered Windows via known_reds + ci_verdict; cancel-in-progress already present at conductor.yml:88-89) | evidence: .github/workflows/conductor.yml:84-92 (concurrency + cancel-in-progress:true),:626-654 (terra job still present but report-only, never required) | severity: HIGH
- id: G-I1-2 -- Removing terra job is redundant; it is already non-blocking/report-only with explicit gap comment and no entry in conductor-required-checks.ruleset.json | evidence: .github/workflows/conductor.yml:629-652 | severity: MEDIUM
SUGGESTED: DISAGREE current OS-agnostic conductor + measured nightly already satisfies operator words without new BUILD-2 row.

### I2
- id: G-I2-1 -- Duplicate ruff pre-commit entry claim false; only one ruff hook (stages:[manual], managed rev v0.15.5 pinned to pyproject.toml) | evidence: .pre-commit-config.yaml:815-830 | severity: HIGH
- id: G-I2-2 -- "plugin copy of validate_backlog.py" redundant; plugins/tier1-lifecycle/scripts/ has no such copy, core is scripts/validate_backlog.py (used by pre-commit hook at .pre-commit-config.yaml:336) | evidence: .pre-commit-config.yaml:336, scripts/validate_backlog.py:1 | severity: HIGH
- id: G-I2-3 -- provider_bench census entries (aider/llm/amp) already handled by existing provider_registry.yaml + check_provider_registry.py; dropping them is duplicate of L2 work | evidence: ecosystem/provider-registry.yaml, scripts/provider_bench.py:1, scripts/check_provider_registry.py | severity: MEDIUM
- id: G-I2-4 -- CI terra job already dead/non-blocking (see I1) | evidence: .github/workflows/conductor.yml:629-652 | severity: LOW
SUGGESTED: DISAGREE List A items mostly already cleaned or wired; List B/C belong in existing transport/janitor mechanisms (scripts/batch_janitor.py, scripts/transport_lint.py).

### I3
- id: G-I3-1 -- agy 1.3.5 headless + --dangerously-skip-permissions already measured and routed (F1/F2 contradict proposal's "permission bypass as bulk reader"); F2 shows --add-dir suffices without full bypass | evidence: scripts/provider_bench.py:263-280 (agy invocation), ecosystem/routing-table.yaml, F1 quote in query | severity: HIGH
- id: G-I3-2 -- Proposal ignores existing read_gate.py + interim-routing (722) that already prefers Copilot for reads until proven | evidence: scripts/read_gate.py:1, ecosystem/routing-table.yaml | severity: HIGH
SUGGESTED: DISAGREE Existing routing + --add-dir (F2) is safer and already proven; full bypass violates R59 mitigations cited in R113.

### I4
- id: G-I4-1 -- Distiller as "front stage" with bounded point tasks is redundant with existing learning_distiller.py + gen_lane_contract.py + conductor.py phases (already maps reuse, skills, constraints, boosted prompt) | evidence: scripts/learning_distiller.py:1, scripts/gen_lane_contract.py:1, scripts/conductor.py:12-15 (phases table), scripts/dispatch.py:553-596 (vendor dispatch) | severity: HIGH
- id: G-I4-2 -- "Completion = payload file, never process exit" already implemented (handback.json, harvest on payload, psutil tree-kill in conductor) | evidence: scripts/handback.py:1, scripts/conductor.py (heartbeat/tree-kill), tests/test_conductor.py | severity: HIGH
SUGGESTED: DISAGREE learning_distiller.py + existing point-task contract in L1 already do this; new "CC-owned contract" duplicates conductor E / ADR-130.

### I5
- id: G-I5-1 -- Sequence after BUILD-2 (Architekt Jutra trials then consumer) is already in STANDING_RULINGS.md and ecosystem/aj-scan-state.yaml + aj_scan.py; R115 restates existing R115 carrier | evidence: protocols/STANDING_RULINGS.md:4868 (R115 carriage note), scripts/aj_scan.py:1, ecosystem/aj-scan-state.yaml | severity: HIGH
- id: G-I5-2 -- F3 confirms R100 exists (RATIFICATION-2026-10-13.md:42) and contradictions in STANDING_RULINGS.md:6307 ("no R100") + missing R103 heading | evidence: protocols/STANDING_RULINGS.md:6307, protocols/RATIFICATION-2026-10-13.md (absent, per grep) | severity: MEDIUM
SUGGESTED: DISAGREE Already carried by L5 boot v2 + rulings landing; no new row needed.

### I6
- id: G-I6-1 -- Runner choice (e = conductor + doit + python-statemachine for [#669] + pydantic) is worse than existing: conductor.py + dodo.py (doit 0.37.0 already in uv.lock + scripts/dodo.py:65-74 worktrees) + python-statemachine already scored highest in DESIGN matrix | evidence: scripts/conductor.py:1, scripts/dodo.py:1, uv.lock:353 (doit), protocols/STANDING_RULINGS.md (matrix at DESIGN §3) | severity: HIGH
- id: G-I6-2 -- pydantic already used in handback_schema.py + lane-report.schema; adding for [#669] duplicates existing PhaseReceipt pattern | evidence: scripts/handback_schema.py:1 | severity: MEDIUM
SUGGESTED: AGREE but matrix already recommends (e); no change required.

### I7
- id: G-I7-1 -- BUILD-1 lane split (6 lanes after AMEND v5) contradicts existing L1-L6 in AMEND v5 itself and BACKLOG.md tasks/689 + tasks/1450 | evidence: to-cc/BATCH-BUILD1-PREP-2026-10-15.md (per query), BACKLOG.md:97 (#689), protocols/STANDING_RULINGS.md (L5 boot v2) | severity: HIGH
- id: G-I7-2 -- Steel thread [#1430] moved to BUILD-2 already recorded; L6 transport is new but duplicates existing transport.py + transport_lint.py + batch_janitor.py | evidence: scripts/transport.py:1, scripts/transport_lint.py:1, scripts/batch_janitor.py:1, BACKLOG.md:135 (#764 transport) | severity: HIGH
SUGGESTED: DISAGREE Lane table and L6 already exist in AMEND v5; transport work is in existing scripts/.

### I8
- id: G-I8-1 -- AMEND L1 additions (DistillReceipt, NEW-JUSTIFIED gate, CHALLENGE sub-stage, ChallengeReceipt, point-task contract) duplicate existing DistillReceipt in learning_distiller.py output, NEW-JUSTIFIED already in anti-dupe (stage_prior_art.py), CHALLENGE in decide_checks.py + stage_library_first.py | evidence: scripts/learning_distiller.py, scripts/stage_prior_art.py, scripts/decide_checks.py:1, scripts/gen_lane_contract.py | severity: HIGH
SUGGESTED: DISAGREE Already implemented in L1 distiller + decide_checks.py (R76/R41 method cited in AMEND v5 Step 0).

### I9
- id: G-I9-1 -- AMEND L2 additions (agy bypass route read = agy -> Copilot) contradicts F1/F2 (no --yolo, --add-dir suffices, existing routing prefers Copilot) and R113 mitigations | evidence: ecosystem/routing-table.yaml, scripts/provider_router.py, F1/F2 in query | severity: HIGH
SUGGESTED: DISAGREE Route already Copilot-first per registry; bypass route violates measured headless behavior.

### I10
- id: G-I10-1 -- AMEND L3 additions (CI concurrency + terra removal + list A + filing BUILD-2 Linux-first) redundant with existing concurrency in conductor.yml:87-89, terra already non-blocking, List A mostly already addressed (see I2), Linux-first already in R111 text | evidence: .github/workflows/conductor.yml:87-89, .pre-commit-config.yaml:815-830 | severity: HIGH
SUGGESTED: DISAGREE CI changes already landed; filing belongs in existing transport.

### I11
- id: G-I11-1 -- AMEND L4 additions (OPERATOR-ACTION agy sign-in, 10-min wait, GAP on timeout, fake-agy RED test) duplicate existing R110 (Codespace sign-in by link) + codespace_regime.py + codespace_state.py | evidence: scripts/codespace_regime.py:1, ecosystem/routing-table.yaml (L4), R110 in RATIFICATION | severity: HIGH
SUGGESTED: DISAGREE Already in L4 Codespace fix + R110.

### I12
- id: G-I12-1 -- AMEND L5 additions (what boot v2 teaches + R100-R115 into STANDING_RULINGS) duplicate existing boot v2 task [#1450], HANDOFF_BOOT.md, and rulings landing in L5 | evidence: tasks/1450-handoff-boot-teaching.md, scripts/lane_boot.py, protocols/STANDING_RULINGS.md:6290-6310 (R100 note), BACKLOG.md | severity: HIGH
SUGGESTED: DISAGREE Exactly L5 scope; F3 contradictions already noted in STANDING_RULINGS.

### I13
- id: G-I13-1 -- AMEND L6 (transport: janitor --apply, index by trigger, architect inbox query, machine-set status handshakes, by: lint, transport_report --help fix) redundant with existing batch_janitor.py, transport.py (query/index), transport_lint.py (by: lint), transport_report.py | evidence: scripts/batch_janitor.py:1, scripts/transport.py:1, scripts/transport_lint.py:1, scripts/transport_report.py:1, ecosystem/index.yaml | severity: HIGH
- id: G-I13-2 -- janitor --apply already partially in batch_janitor.py; index by trigger already in transport triggers | evidence: scripts/batch_janitor.py:85-288, scripts/transport_lint.py | severity: MEDIUM
SUGGESTED: DISAGREE All mechanisms exist in scripts/transport*.py + janitor; L6 duplicates current transport work (R71/D8).

DONE.
