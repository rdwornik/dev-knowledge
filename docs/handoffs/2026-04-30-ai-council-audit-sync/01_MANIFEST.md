# Manifest — ai-council audit-sync

**Handoff ID:** 2026-04-30-ai-council-audit-sync
**Format version:** v3.0 (ADR-42)
**Type:** audit-sync
**Generated:** 2026-05-09 (regenerated from v2.0 using v3.0 format)
**Audit date:** 2026-04-30
**Stage 2:** implicit — audit findings (Faza A2) substituted for browser-2 response

---

## Target repo state

| Field | Value |
|---|---|
| Repo | ai-council |
| Path | C:/Users/1028120/Documents/Dev/ai-council |
| HEAD SHA | `c821157fcfa957bc6612c74667d70c8c9a88ef5c` |
| Branch | `main` |
| Working tree | **MODIFIED** — `config/settings.yaml` has uncommitted changes |

> **Drift note:** `config/settings.yaml` has uncommitted changes in the working
> tree as of regeneration date (2026-05-09). This predates the audit (2026-04-30).
> Browser-2 must NOT commit or modify `config/settings.yaml` during F-01/F-02 work.
> The audit found working tree clean as of post-migration HEAD c821157 — the
> modification may be post-audit local development. Rob is aware.

---

## HEAD verification (browser-2 first action)

Before reading any other file, run in ai-council:
```
git rev-parse HEAD
```

Expected: `c821157fcfa957bc6612c74667d70c8c9a88ef5c`

Mismatch → STOP. Report actual SHA. Do not proceed.

---

## File index

| File | Purpose |
|---|---|
| `00_README.md` | Upload + usage instructions for Rob |
| `00_first-message.md` | Copy-paste first message for browser-2 |
| `01_MANIFEST.md` | This file — entry point, metadata, navigation |
| `01_manifest.json` | Machine-readable metadata + SHA-256 checksums |
| `02_VISION.md` | Full .dev-knowledge VISION — ecosystem context and methodology scope |
| `03_PLAYBOOK.md` | Full .dev-knowledge PLAYBOOK — complete HOW-we-work reference |
| `04_ESSENTIALS.md` | Full .dev-knowledge ESSENTIALS — high-leverage daily cheat sheet |
| `05_GOVERNANCE_ESSENCES.md` | ADR-33 + ADR-35 essences (only ADRs driving F-01, F-02) |
| `06_STATE_OF_PLAY.md` | Current state: migration status, audit findings, locked decisions, deferred |
| `07_ACTION_PLAN.md` | Goals, directives (F-01, F-02), boundaries, success criteria |
| `08_TREE.txt` | ai-council file inventory via `git ls-files` at Stage 3 |
| `09_EXECUTION_EVIDENCE.md` | Return trip template — browser-2 fills post-work |

**Reading order:** 01 → 02 → 03 → 04 → 05 → 06 → 07 → (08 if needed) → 09 at end

---

## Receiver synthesis prompt

After reading files 01-07, provide synthesis before acting:

> "I will execute [goal from 07_ACTION_PLAN.md]. My understanding:
> [paraphrase of audit findings + locked decisions from 06]. I will NOT
> [boundaries from 07]. I will start with [first directive from 07].
> HEAD SHA matches c821157fcfa957bc6612c74667d70c8c9a88ef5c. I acknowledge
> config/settings.yaml is modified and will not touch it."

Only proceed after Rob confirms accuracy.

---

## Operational center

See `07_ACTION_PLAN.md` for directives. See `06_STATE_OF_PLAY.md` for context.
See `05_GOVERNANCE_ESSENCES.md` for ADR-33 and ADR-35 operational rules.
