# Architectural Decision Records — `.dev-knowledge`

<!-- scope: meta -->

Architecture decisions for `.dev-knowledge` in Michael Nygard ADR format. The `transcripts/`
subfolder holds AI Council debate outputs that informed them.

## ADR Index

<!-- scope: meta -->

| ADR | Date | Title |
|-----|------|-------|
| ADR-27 | 2026-04-21 | Scope tagging — single-repo `dev\|llm\|hybrid\|runtime\|meta` vocabulary, hybrid ≤25% ceiling, pre-commit enforcement |
| ADR-28 | 2026-04-21 | Three-layer architecture — browser chat → .dev-knowledge → projects; descriptive ADR documenting existing practice |
| ADR-29 | 2026-04-21 | LESSONS.md grandfathering — existing entries untouched; new entries include inline `[scope: X]` tag |
| ADR-30 | 2026-04-26 | Default git branch `main` — universal rule for all Rob's repos |
| ADR-31 | 2026-04-27 | Authority model — prescriptive with conformance audit (Option 1B); .dev-knowledge prescriptions are binding |
| ADR-32 | 2026-04-27 | Handoff format and browser/agent role split — folder-format handoffs, strict role boundary |
| ADR-33 | 2026-04-28 | VISION.md universalization — mandatory at ≥1 dependent; Standard/Lite tiers per scale |
| ADR-34 | 2026-04-29 | File naming convention — per-file-type table; codifies existing de-facto patterns cross-repo |
| ADR-35 | 2026-04-29 | Lessons base activation — lessons-index.json + SessionStart retrieval + CLI querying |
| ADR-36 | 2026-04-30 | Audit tool architecture — .dev-knowledge as ecosystem auditor; 4-phase implementation plan |
| ADR-37 | 2026-04-30 | Session boundary protocol — two-phase handoff (Current State + Future State) |
| ADR-38 | 2026-04-30 | Universal repo architecture baseline — mandatory files per tier S/M/L; foundation for ADR-39/40/41 |
| ADR-39 | 2026-04-30 | File lifecycle governance — 6-element pattern per file (purpose/trigger/owner/grooming/boundaries/enforcement) |
| ADR-40 | 2026-04-30 | Scale tier evaluation algorithm — logarithmic Maintainability Index pattern; 3 signals (module count, test count, TCR) |
| ADR-41 | 2026-04-30 | Cross-session backlog architecture — BACKLOG.md mandate at M+ tier; no Scrum vocabulary |
| ADR-42 | 2026-05-09 | Handoff format v3 — three-stage generation flow; v3.2 = flat per-session folder, Q&A iteration loop |
| ADR-43 | 2026-05-11 | Cross-project transcript routing — per-invocation, opt-in, config-driven; `target-project:` frontmatter + `--target-project` flag; `TargetResolver` in ai-council CLI |
| ADR-44 | — | Reserved — scrum-master review propagation authority codification; held pending N=2 empirical instance (corp-monorepo scrum-master review). See PLAYBOOK § 17. |

## Transcript naming convention

<!-- scope: meta -->

### Canonical (since 2026-04-30 revert commit `4a00560`)

`council-out-YYYYMMDD-HHMMSS-{slug}.md` — timestamped, CLI-emitted from AI Council. 12 files
currently in `transcripts/`.

### Legacy (pre-canonical)

`DECISION_NN_{slug}.md` — 3 files (`DECISION_27`, `DECISION_28`, `DECISION_29`) are pre-CLI
historical artifacts from the manual archival era. **Relocated to `transcripts/archive/legacy/` (2026-05-12). Not renamed retroactively.**

> **Important:** legacy `DECISION_NN` numbering does NOT align with ADR-NN numbering.
> `DECISION_28_authority_model` informed ADR-31 (not ADR-28); `DECISION_29_handoff_synergy`
> informed ADR-32 (not ADR-29).

## ADR↔transcript traceability

<!-- scope: meta -->

| ADR | Originating transcript(s) |
|-----|---------------------------|
| ADR-27 | `transcripts/archive/legacy/DECISION_27_llm_practice_ecosystem.md` — verified: Council #27 brief about single-repo vs split; decided Option A (scope tagging) |
| ADR-28 | *(no transcript — conversational decision documenting existing practice)* |
| ADR-29 | *(no transcript — derivative of ADR-27, same session)* |
| ADR-30 | *(no Council transcript — decided via Codex audit `docs/audits/2026-04-26-codex-adr-30-default-branch-main.md`)* |
| ADR-31 | `transcripts/archive/legacy/DECISION_28_authority_model.md` — verified: per ADR-31 "Debate transcript" reference |
| ADR-32 | `transcripts/archive/legacy/DECISION_29_handoff_synergy.md` — verified: per ADR-32 "Debate transcript" reference |
| ADR-33 | `council-out-20260428-125133-format-and-structure-of-visionmd-for-dev.md` (research) + `council-out-20260428-162415-pick-council-prompt-adr33-vision-universalization.md` (decision) |
| ADR-34 | `council-out-20260429-190922-pick-council-adr34-file-naming-convention.md` |
| ADR-35 | `council-out-20260429-210057-pick-council-adr35-lessons-base-activation.md` |
| ADR-36 | `council-out-20260430-123043-pick-council-adr36-audit-tool-architecture.md` + `council-out-20260430-125039-research-question-what-prior-art-exists-for-cross-repo-audi.md` (research) |
| ADR-37 | `council-out-20260430-132308-pick-council-adr37-two-phase-handoff.md` |
| ADR-38 | `council-out-20260430-134721-pick-council-adr38-scrum-framework.md` — verified: "adr38" in filename; content is scrum-as-framework debate that produced universal repo architecture ADR; "scrum_framework" slug reflects original question framing |
| ADR-39 | *(no obvious transcript — may be conversational)* |
| ADR-40 | `council-out-20260430-154818-research-question-how-should-an-llm-driven-multi-repo-ecosy.md` — per ADR-40 Related field |
| ADR-41 | `council-out-20260430-134721-pick-council-adr38-scrum-framework.md` (also cited in ADR-41 Related field as structural context) + `council-out-20260430-150751-research-question-for-a-solo-developer-with-multiple-active.md` (research) |
| ADR-42 | `council-out-20260509-143831-research-brief-for-ai-council-architect-browser-session-con.md` + `council-out-20260509-144836-research-question-how-should-an-llm-driven-solo-developer-a.md` |

## Pending Council decisions

<!-- scope: meta -->

No `pending-council-questions.md` exists yet — pending questions are currently tracked in
`BACKLOG.md` under "Council debate territory" annotations. Future convention: create
`docs/decisions/pending-council-questions.md` when the queue warrants a dedicated file.

## Council output reality note

<!-- scope: meta -->

AI Council CLI currently emits to `ai-council/output/` only. Transcripts here are **manual
archival copies** — this is the current process for all 14 `council-out-*` files. Cross-project
routing as a CLI feature is pending (see BACKLOG Cross-stream P1 "AI Council cross-project
transcript routing"). Until the feature lands: canonical filename is preserved; source of truth
remains `ai-council/output/`. Full operational detail in PLAYBOOK Section 5 "Council Debate
Archival Protocol".

## Related

<!-- scope: meta -->

- `docs/research/` — research-mode Council debate outputs and external research reports
- `docs/audits/` — point-in-time audit outputs (per-repo state analysis)
