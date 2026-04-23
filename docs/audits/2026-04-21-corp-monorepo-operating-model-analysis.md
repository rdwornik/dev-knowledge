# corp-monorepo Scale L Operating Model — Analysis

**Date:** 2026-04-21 (started); 2026-04-23 written
**Subject repo:** `C:\Users\1028120\Documents\Dev\corp-monorepo`
**Branch at time of analysis:** `docs/adr-27-safety-invariants` (clean tree)
**Analyst:** Claude Code (Opus 4.7, xhigh effort)
**Purpose:** Reverse-engineer the Scale L operating model from the only Scale L repo in the ecosystem. Raw material for later synthesis (Council debate, PLAYBOOK update). Not a design document. Not a fix list.
**Constraints:** Read-only on corp-monorepo. Cite files. Do not synthesize universal patterns. Do not resolve conflicts — surface them.

---

## Section 1 — Executive Summary

The corp-monorepo Scale L operating model is a **six-layer governance stack** running on top of a unified `src/corp/` Python monorepo: (1) `CLAUDE.md` as the Claude Code contract, (2) `AGENTS.md` as the Codex review contract, (3) `CONTRIBUTING.md` as the human-and-AI workflow contract, (4) `docs/ARCHITECTURE.md` as the structural mirror, (5) `.claude/skills/gotchas/gotchas.md` as the empirical pattern memory, (6) `docs/decisions/ADR-NN-*.md` as the durable decision record (with `transcripts/` for raw debates). It is reinforced by mechanical enforcement (Tach pre-commit + CI from ADR-26, planned AST safety scanner from ADR-27), an AI Council debate ritual (4-model panel + non-participant synthesizer, 2 rounds, ~$0.50, ~250s), and a Codex code-review loop with explicit review modes.

**What is strong, with evidence.** ADR cadence (27 ADRs in ~2 months: ADR-01..ADR-21 distilled retroactively per `JOURNAL.md:147`, then ADR-22..27 produced per-decision); structured Council transcripts with cost/token attribution (`docs/decisions/transcripts/DECISION_24...md:1-13`); an explicit two-mode Codex review (diff vs. full audit, `AGENTS.md:77-83`); a Tach 4-layer enforcement model that is both documented and CI-blocking (`tach.toml`, `.pre-commit-config.yaml:11-18`, `.github/workflows/tach.yml` per `JOURNAL.md:19`); an append-only `JOURNAL.md` with a stable "Did / Failed / Next" shape; and a re-review-after-amendment Codex pattern that surfaces same-class bugs across non-flagged sites (`docs/audits/2026-04-21-codex-hotfix-review.md:122-131`).

**What is weak, with evidence.** `CLAUDE.md` is structurally and numerically stale ("Council Decisions: 24", "CLIs (2,404 tests)") while the live repo has 27 ADRs and ~2,515 tests (`CHANGELOG.md:17`). `docs/HANDOFF.md` was last regenerated 2026-03-29 (`docs/HANDOFF.md:2`) and now coexists with a new `docs/handoffs/YYYY-MM-DD-handoff.md` per-session pattern (`docs/handoffs/2026-04-15-handoff.md`), with no document declaring which is canonical. `docs/decisions/README.md` ends mid-section at line 38 listing only ADR-01..ADR-21. `docs/ARCHITECTURE.md:423-426` references `docs/audits/2026-04-21-p1-verification.md`, which **does not exist** on disk. `docs/diagrams/conventions.yaml` still labels `layer_3` as "Composition" while the canonical Tach taxonomy uses `interface`. Several Council decisions (#25 diagrams, #26 Tach) have **no transcript file** in `docs/decisions/transcripts/`; ADR-27's transcript is filed under `docs/decisions/ADR-27-council-onedrive-centralization.md` (different folder, different naming convention).

**Documented vs. practiced.** What is documented: branch naming, conventional commits, ADR template (≤20 lines per `docs/decisions/README.md:35`), Codex severity levels, Tach layer rules, Session Protocol (4 steps in `CLAUDE.md:73-77`), Prompt Decision Rule (`CLAUDE.md:90-94`). What is **practiced but not documented**: the multi-PR ADR rollout pattern (PR-1 foundation / PR-2 migration / PR-3 CI in `ADR-27...:88-95`; mirrored in ADR-26's Phase 1 / Phase 2 / Step 12 sequence in `JOURNAL.md:8-21`), `hotfix/*` branch convention (used 2026-04-21 but absent from `CONTRIBUTING.md:5-11`), the `verify:` line on every gotcha and learned-rule (in `CLAUDE.md:65-71` and pervasively in `gotchas.md`, but no doc explains the convention), the Codex re-review-after-amendment cycle (`docs/audits/2026-04-21-codex-hotfix-review.md:92`), and the unique location/naming for the ADR-27 transcript.

---

## Section 2 — File Inventory with Roles

| Path | Role | Update author | Cadence | Mode | Update trigger |
|------|------|---------------|---------|------|----------------|
| `CLAUDE.md` | Claude Code session contract; architecture rules; learned rules; session protocol | Human (mostly) | Sporadic | Living | New invariant; promoted learned rule |
| `AGENTS.md` | Codex CLI review contract; severity ladder; review modes | Human | Sporadic | Living | New review category; calibration after audit |
| `CONTRIBUTING.md` | Human + AI workflow; Tach culture rules; pre-commit setup | Human | After major-tool adoption | Living | New tool integrated |
| `README.md` | Repo entry point; module/test table | Human | Sporadic | Living | Module count change |
| `docs/ARCHITECTURE.md` | Structural mirror; module map; data flow; invariants; "OneDrive safety guards" table | Human | After structural change | Living | Module add/move; new invariant; ADR landing |
| `docs/HANDOFF.md` (25KB) | Master session paste-into-new-chat document; live stats; pipeline diagram; open decisions | `scripts/update_handoff.py` (table rows only) + manual | "End of every major session" per `CLAUDE.md:85-88`; actual: 2026-03-29 last regen | Living | Per-session; script call |
| `docs/handoffs/2026-04-15-handoff.md` | Dated handoff snapshot for a multi-day session | Human | Per-session (new pattern, n=1) | Frozen-on-write | End of multi-day session |
| `JOURNAL.md` (237 lines) | Append-only session log, "Did / Failed / Next" | Claude Code per session | Per session, "3 lines per session" per `JOURNAL.md:3` (actual: paragraphs) | Append-only | End of every session |
| `CHANGELOG.md` | Versioned change record (semver-style for [1.0.0]); recent entries are date-headed not version-headed | Human at session end | After significant merges | Append-only at top | Major merge or ADR landing |
| `docs/decisions/README.md` | ADR table-of-contents | Human | After every ADR | Living (currently truncated) | New ADR |
| `docs/decisions/ADR-NN-*.md` | Distilled decision record (≤20 lines target) | Human after Council | One per Council decision | Frozen | Council debate concludes |
| `docs/decisions/transcripts/DECISION_NN_*.md` | Raw 4-model debate output | AI Council tool | One per Council debate (gaps: #25, #26 missing) | Frozen | Council run completes |
| `docs/decisions/ADR-27-council-onedrive-centralization.md` | Raw Council transcript for ADR-27 (filed differently from older transcripts) | AI Council tool | One-off | Frozen | This Council run |
| `docs/audits/YYYY-MM-DD-*.md` | Codex audit results; Tach baseline; verification reports | Codex output + human | Per audit/review | Frozen-on-write | Codex run; pre-merge verification |
| `.claude/skills/gotchas/SKILL.md` | One-line skill dispatcher (frontmatter only) | Human | Once | Frozen | Initial skill creation |
| `.claude/skills/gotchas/gotchas.md` | Empirical pattern memory; per-entry Gotcha/Trigger/Symptom/Fix/verify/Last triggered | Human + Claude | Per discovered pattern; "Last triggered" updates | Append + edit | New pattern; pattern re-triggered |
| `tach.toml` | Authoritative module-to-layer assignments + explicit `depends_on` | Developer running `tach sync --add` | Per new cross-module import | Living | Code change introduces new dependency |
| `pyproject.toml` | Single package definition; CLI entry points; ruff config | Human | Per dependency change | Living | Add/remove dep; new CLI |
| `.pre-commit-config.yaml` | ruff + tach hooks | Human | Rare | Living | New mechanical check |
| `docs/diagrams/conventions.yaml` | Diagram style guide; "read by Claude Code, not by scripts" (line 1) | Human | Rare | Living | Style policy change |
| `docs/diagrams/*.mermaid` (3 only) | Source of truth for the 3 diagrams (system-context, container-module, magistrala-pipeline) | Human | After structural change | Living | Module map change |
| `docs/diagrams/*.svg` | Generated outputs (open directly in VS Code) | `scripts/render-diagrams.ps1` | After mermaid change | Generated | mermaid change |
| `scripts/update_handoff.py` (140 LOC) | Updates 4 table rows in `docs/HANDOFF.md`: timestamp, eval scores, vault note count, test count from JOURNAL | Manual invocation | "End of each session" (intent) | Tool | Manual |
| `scripts/dev-check.ps1` | Pre-merge quality gate referenced in `CLAUDE.md:76` and `CONTRIBUTING.md:46` | (script) | Pre-merge | Tool | Manual |
| `scripts/run-all-tests.ps1` | All-tests runner (`CLAUDE.md:42`) | (script) | Pre-merge | Tool | Manual |

Notes on the inventory:
- `docs/decisions/transcripts/` shows files DECISION_01..DECISION_24 (25 files including `DECISION_03_..._SUPERSEDED.md` and `DECISION_04_..._SUPERSEDED.md`). No DECISION_25 or DECISION_26 file exists. The Council #27 transcript was filed at `docs/decisions/ADR-27-council-onedrive-centralization.md` rather than `docs/decisions/transcripts/DECISION_27_*.md` — this is a one-off naming exception, not a deprecation.
- `docs/audits/` contains 3 files. ARCHITECTURE.md cites `2026-04-21-p1-verification.md`, which is **not present**.
- `docs/handoffs/` contains 1 file (`2026-04-15-handoff.md`); the folder pattern is new.

---

## Section 3 — Governance Layer Analysis

### CLAUDE.md (95 lines) — Claude Code contract

**What it defines.** Architecture overview ("unified src/corp/ layout"), 5 non-negotiable architecture rules (`CLAUDE.md:8-13`), source layout, CLI table, dev workflow (branch + commit naming), key config paths, an inline list of 24 Council decisions with #14 and #23 highlighted (`CLAUDE.md:54-56`), safety rules including the OneDrive exclusion (`CLAUDE.md:58-61`), 4 project-specific learned rules with `verify:` lines (`CLAUDE.md:63-71`), a 4-step Session Protocol (`CLAUDE.md:73-77`), the HANDOFF.md ritual (`CLAUDE.md:79-88`), and a Prompt Decision Rule (`CLAUDE.md:90-94`).

**What is stale or contradicted by current state.**
- Line 29: "CLIs (2,404 tests)" — `CHANGELOG.md:17` states Apr-21 hotfix landed at "2507 -> 2515 green" (current count ≈ 2,515).
- Line 54: "Council Decisions: 24" — `CHANGELOG.md:3-7` records ADR-27 drafted; `git log` shows ADR-26 and ADR-27 commits between this CLAUDE.md count and now (delta of +2 minimum, +3 if pre-Tach decisions are included). `docs/HANDOFF.md` (also stale) lists 24 in a different table.
- Line 47: "Naming convention: `config/naming_config.yaml` (19 type codes, 15 client aliases)". `JOURNAL.md:36` records that the canonical file moved to `schema/` with a shim left in `ingest/` ("`naming_config.py` moved from `ingest/` to `schema/` ..."). The stated path is the YAML, not the .py, but both module residency and YAML location are absent context.
- Line 43: "Check `~/.claude/skills/gotchas/`" — points to global skill location, while a project-local `.claude/skills/gotchas/SKILL.md` + `gotchas.md` also exist (the project file's line 4-5 declares it was "moved from ~/.claude/skills/gotchas/gotchas.md (global → project scope)"). CLAUDE.md still points to global.
- No mention of: AGENTS.md, CONTRIBUTING.md, tach.toml, ADR-25, ADR-26, ADR-27, the `docs/audits/` directory, the `docs/handoffs/` folder, or `docs/diagrams/conventions.yaml`. Prompt Decision Rule does not mention `docs/decisions/transcripts/` at all.

### AGENTS.md (131 lines) — Codex review contract

**What it defines.** Role ("read-only code reviewer"; explicit MUST/MUST-NOT lists at `AGENTS.md:8-18`), repo architecture context (5 CLI entry points, module structure, "Dependency Rule (ENFORCED BY TACH)" at `AGENTS.md:43-54`), 7 key invariants (`AGENTS.md:55-63`), database table inventory (8 + 6 + 3 tables), config sources, two review modes (diff default vs explicit "full audit", `AGENTS.md:77-83`), and a 4-tier severity ladder (Critical 6 / High 5 / Medium 7 / Low 3) with one-line definitions per tier and an explicit "Codex skips this check" for Tach-enforced import direction (`AGENTS.md:89`).

**Severity calibration.** "CRITICAL = blocks merge. Runtime bugs, data loss risk, security issues, architectural invariant violations" (`AGENTS.md:88`). "HIGH = issues that change runtime behavior or silently degrade data. Convention violations belong in MEDIUM or LOW" (`AGENTS.md:97`). The 2026-04-15 handoff records this as "severity calibrated after first audit" (`docs/handoffs/2026-04-15-handoff.md:28`); the recalibration is invisible in AGENTS.md itself (no changelog inside the file). The 2026-03-30 codex full audit (`docs/audits/2026-03-30-codex-full-audit.md`) emitted 4 CRITICAL + 4 HIGH + 1 MEDIUM, of which several CRITICALs were arguably architectural-invariant (e.g., `synthesize.py:257` extractor writing artifacts → ADR-27 Decision 2 amendment) — calibration in practice happens via decision-by-decision negotiation, not by re-editing AGENTS.md.

**Output format.** Strict template at `AGENTS.md:118-128` (`## [SEVERITY] file:line — description` then `**What:** ... **Why:** ... **Fix direction:** ...`). The hotfix review (`docs/audits/2026-04-21-codex-hotfix-review.md:34-67`) follows this format precisely.

### Skill invocation

CLAUDE.md does not explicitly say "invoke the gotchas skill" or "read SKILL.md"; it says "Check `~/.claude/skills/gotchas/`" (`CLAUDE.md:43`) and lists 4 specific learned rules inline. The project-local `.claude/skills/gotchas/SKILL.md` is one-line frontmatter only:
```
---
name: corp-gotchas
description: Project-specific gotchas for corp-monorepo ecosystem...
---
```
The actual content lives in the sibling `gotchas.md`. Whether the skill is invoked by Claude on session start, by user `/skill` invocation, or only by file reads, is not declared in CLAUDE.md.

### Gaps identified at the governance layer

- **No cross-link map.** CLAUDE.md, AGENTS.md, CONTRIBUTING.md, ARCHITECTURE.md each describe parts of the same architecture (especially layers and invariants) without referencing each other systematically. AGENTS.md does not mention CLAUDE.md; CLAUDE.md does not mention AGENTS.md or CONTRIBUTING.md; CONTRIBUTING.md mentions AGENTS.md once (`CONTRIBUTING.md:121`) and ARCHITECTURE.md once (`CONTRIBUTING.md:118`).
- **Two definitions of layers.** AGENTS.md lists layer assignments inline (`AGENTS.md:46-51`); ARCHITECTURE.md lists them again (`docs/ARCHITECTURE.md:174-191`); `tach.toml` is the canonical source. None of the three docs declares which is the source of truth — `JOURNAL.md:9` retroactively asserts "Single source of truth: tach.toml" but this is in JOURNAL, not in any contract file.
- **Invariants count differs.** AGENTS.md lists 7 invariants (`AGENTS.md:55-63`); ARCHITECTURE.md lists 7 invariants (`docs/ARCHITECTURE.md:393-399`) but with different ordering and numbering and an inline ADR-27 narrowing footnote on #1; CLAUDE.md lists 5 architecture rules (`CLAUDE.md:8-13`) plus 3 safety rules (`CLAUDE.md:58-61`). None claims canonicality.
- **Self-Evolution Protocol is in the user's global CLAUDE.md** (referenced in the system context of this audit) **but not in the repo CLAUDE.md.** The repo's "Learned Rules" section assumes the protocol exists but does not quote it.

---

## Section 4 — Session Lifecycle (as-practiced)

Reverse-engineered from `JOURNAL.md` entries 2026-03-25 through 2026-04-15 and the post-2026-04-15 git log.

### Start-of-session

Per `CLAUDE.md:73-77`: "Read last 5 entries from JOURNAL.md before starting work." Per `docs/HANDOFF.md:445-451`: also "Check `~/.claude/skills/gotchas/gotchas.md` before modifying any package". Practiced state: JOURNAL recent entries are paragraph-length not 3-line; reading 5 entries means reading roughly 50-100 lines of dense narrative.

### Branch + commit pattern

Per `CONTRIBUTING.md:5-25`: feature branches `feat/`, `fix/`, `refactor/`, `chore/`, `docs/`; conventional commits `type: imperative`. Practiced as documented (recent log shows `feat(...)`, `fix(...)`, `docs(...)`, `test(...)`, `ci(...)` consistently). One observed deviation: `hotfix/onedrive-safety-p1` branch (merged 2026-04-21, commit `eee56ca`) — the `hotfix/*` prefix is **not** in the documented set.

### Within-session iteration

The Tach-adoption sequence in `JOURNAL.md:18-21` (most-cited example with rich detail) shows: "Bootstrapped tach.toml ... Ran tach sync — found 6 baseline violations ... documented in docs/audits/2026-04-15-tach-baseline-violations.md. Wired tach check into pre-commit ... created .github/workflows/tach.yml ... Added CONTRIBUTING.md with tach sync cultural rules. Replaced AGENTS.md import-direction check with Tach reference. Created ADR-26. **2495 tests passing, 0 failed.** 8 commits, merged to main." — i.e. one session can produce 8 commits across code + config + 2 governance files + 1 ADR + 1 audit doc + a Phase-2 follow-up.

The 2026-04-21 OneDrive hotfix sequence in git log (commits `21e062e`..`eee56ca`) shows another pattern: failing-tests-first (`test(safety): failing regression tests for P1-1, P1-2, P1-3`), three P1 fix commits, audit doc commit (`181a39c docs(audit): codex review output for hotfix branch`), then 4 amendment commits ("resolve paths before OneDrive check"), then a re-review audit append (`47011fd docs(audit): codex re-review after amendment`), then merge.

### Pre-merge

Per `CONTRIBUTING.md:37-47`: `pytest -x --tb=short && pre-commit run --all-files && tach check` — or `./scripts/dev-check.ps1`.

### End-of-session

Per `CLAUDE.md:73-77`: "Append session summary to JOURNAL.md before ending."  Per `CLAUDE.md:85-88` and `HANDOFF.md:451`: "Run `python scripts/update_handoff.py` to refresh this file." JOURNAL is reliably appended (37+ entries through Apr-15). HANDOFF.md regeneration is **not** reliably executed — last update timestamp embedded in `docs/HANDOFF.md:2` is `2026-03-29T01:13:07Z` despite multiple sessions since.

### What goes where (boundary identified from practice)

- **JOURNAL.md** = per-session narrative ("Did / Failed / Next" — the "Failed" line is consistently filled even when "-" or "Nothing")
- **CHANGELOG.md** = significant landings (consolidation v1.0.0, hotfix landing, ADR drafting)
- **ADR-NN-*.md** = decisions taken (ADR-26 explicitly created during the same session as Tach implementation, before the related work landed — see `JOURNAL.md:21`)
- **docs/audits/** = Codex outputs and verification reports referenced in commits and ADRs
- **gotchas.md** = patterns repeatable across sessions (with Last triggered date for staleness signal)
- **LESSONS** in `.dev-knowledge` (out of scope here) vs. JOURNAL in repo: not explicitly delineated in any corp-monorepo file. Project-scoped gotchas live in `.claude/skills/gotchas/gotchas.md`; cross-project lessons live elsewhere.

---

## Section 5 — Architectural Change Workflow (as-practiced, ADR-26 trace)

ADR-26 (Tach adoption) is the most recent and best-documented full-cycle architectural change. Reconstructed timeline:

| When | What | Evidence |
|------|------|----------|
| Pre-2026-04-15 | Codex routine diff review found 3 upward dependency violations in `ingest/router.py:18,653,743` | `ADR-26-tach-adoption.md:22-26` |
| 2026-04-15 (early) | Council #26 debate runs; ADR-26 drafted | Implied by `ADR-26...:5` ("Debate: Council #26"), but **no transcript file** exists in `docs/decisions/transcripts/` |
| 2026-04-15 | Phase 1 implementation: `tach.toml` bootstrap (34 modules, 4 layers) → `tach sync` finds 6 baseline violations → docs/audits/2026-04-15-tach-baseline-violations.md created with status "DEFERRED — document only" → pre-commit hook → `.github/workflows/tach.yml` → CONTRIBUTING.md added → AGENTS.md import-direction check replaced with Tach reference → ADR-26 committed | git log commits `8c05eb7..684eacc`; `JOURNAL.md:18-21` |
| 2026-04-15 (same day) | Phase 2: `corp.project_resolver` orchestration→core, `corp.query_engine` interface→orchestration, baseline violations marked RESOLVED in audit doc, ADR-26 amended with "Phase 2 Resolution" section | git log commits `2e9e511..f120c11`; `ADR-26...:120-136`; `docs/audits/2026-04-15-tach-baseline-violations.md:3-5` |
| 2026-04-15 (same day) | Step 12: 4-layer taxonomy reconciled across AGENTS.md, ARCHITECTURE.md, 5 per-module READMEs | git log `05ffcba`, `803540c`, `5ea65b3` (the latter two are duplicate-subject commits — see Section 10) |
| 2026-04-15 | JOURNAL entries (3 separate entries for the same day, one per phase): `JOURNAL.md:8-21` |
| 2026-04-17 | "Verified handoff 2026-04-15" added at `docs/handoffs/2026-04-15-handoff.md` (introduces the new dated-handoff pattern; see Section 6) | git log commit `ca5d454`; file ctime |
| 2026-04-15..present | **CHANGELOG.md not updated for ADR-26.** Current CHANGELOG entries are `2026-04-22` (ADR-27 drafting), `2026-04-21` (hotfix), `[1.0.0] 2026-03-28` (consolidation). No mention of ADR-26 or Tach. | `CHANGELOG.md` |
| 2026-04-15..present | **docs/HANDOFF.md not updated for ADR-26.** Live stats still show "Council decisions \| 24 \| 2026-03-29" and "ADRs \| 24 \| 2026-03-29" (`docs/HANDOFF.md:23-24`). | |
| 2026-04-15..present | **CLAUDE.md not updated for ADR-26.** Still says "Council Decisions: 24" (`CLAUDE.md:54`) and lacks any reference to Tach, CONTRIBUTING.md, or `tach.toml`. | |
| 2026-04-15..present | **docs/decisions/README.md not updated** for ADR-22..27 (table ends at ADR-21, `README.md:29`). | |

Workflow interpretation: code/CI/audit/ADR/per-module-doc updates land in the same session; the higher-aggregation living docs (CLAUDE, HANDOFF, decisions/README, CHANGELOG) lag without an explicit re-aggregation step.

---

## Section 6 — Handoff Convention Analysis

### Source 1: `docs/HANDOFF.md` (~25KB, 457 lines)

- Self-described purpose at line 5: "Paste this file into new Claude.ai chats for context. This is the ONLY document a new chat needs."
- Updated by `python scripts/update_handoff.py` per the instruction at line 9. The script (140 LOC) updates four table rows only: timestamp, eval scores, vault note count from `index.db`, test count by regex on JOURNAL ("first match = most recent entry", `update_handoff.py:57`). It does **not** touch the prose body, the Council Decisions list, the ADR count, the gotchas count, the Open Decisions list, or any of the architectural narrative.
- Last regenerated: `2026-03-29T01:13:07Z` (`docs/HANDOFF.md:2`).
- Per `CLAUDE.md:81-88`, this file is invoked at the start of new chats and updated at the end of every major session.

### Source 2: `docs/handoffs/2026-04-15-handoff.md` (148 lines)

- Self-describes as "Project Scale: L (multi-package monorepo, 2495+ tests, ARCHITECTURE.md, per-module READMEs, AGENTS.md)" at line 5.
- Adopts a Scale-aware structure: OBJECTIVE → STATUS → COMPLETED → PENDING → KEY DECISIONS → CONTEXT.
- Created 2026-04-17, frozen on write. No regeneration script.
- Covers the 2026-03-30..2026-04-15 multi-day session (i.e., overlaps with the period that `docs/HANDOFF.md` should also cover).
- Not regenerated, not appended to. There is one file in this folder.

### The conflict, presented from both sides

**View A — `docs/HANDOFF.md` is the source of truth.** Evidence: explicit instruction in `CLAUDE.md:79-88` and in `docs/HANDOFF.md:5`; tooling (`scripts/update_handoff.py`) exists and is documented; the file is comprehensive (live stats, full pipeline diagram, all Council decisions, all open decisions, infrastructure inventory, CLI command list — 457 lines of context).

**View B — `docs/handoffs/YYYY-MM-DD-handoff.md` is the new pattern.** Evidence: Scale-aware framing in line 5; created after a multi-day session that produced significant architectural change (ADR-25, ADR-26, Codex integration); the master HANDOFF.md was not updated for any of that work; the new file is concise (148 lines) and decision-focused; the verb in its commit message is "verified" (commit `ca5d454`: "docs: add verified handoff 2026-04-15").

The repo contains **no document declaring which is canonical**. `CLAUDE.md` continues to point only at HANDOFF.md. No JOURNAL entry mentions the new folder or the change in pattern. `update_handoff.py` continues to write to `docs/HANDOFF.md` only.

---

## Section 7 — Tooling Adoption Patterns

Reconstructed for four major tools/conventions adopted in 2026-03 / 2026-04.

### Codex CLI as code reviewer

**How it entered.** No JOURNAL entry I sampled records the introduction event itself. `AGENTS.md` exists in the root and is dated by content (e.g., references to current architecture). The first Codex audit landed at `docs/audits/2026-03-30-codex-full-audit.md` (5006 bytes); follow-up fixes in `JOURNAL.md:29-31`.

**How it was anchored.** `AGENTS.md` (131 lines, defines role + invariants + severity ladder + output format). `CONTRIBUTING.md:121` mentions it once. `CLAUDE.md` does not mention it. The `/review` command is mentioned in the user-invocable skills list at session start (`/review` and `/security-review`), separately defined per the user's claude environment, not in the repo.

**Reopening triggers in evidence.** The Codex re-review-after-amendment cycle (`docs/audits/2026-04-21-codex-hotfix-review.md:92-141`) documents a re-run after fixes; severity calibration was implicitly revised based on first-audit experience (per `docs/handoffs/2026-04-15-handoff.md:28`).

### Tach (import boundary enforcement)

**How it entered.** Per `ADR-26-tach-adoption.md:22-26`: triggered by Codex finding 3 upward import violations in a single module during a routine diff review. Then a Council #26 debate (transcript file missing).

**How it was anchored.** New file `tach.toml` (179 lines, 27 [[modules]] entries — `JOURNAL.md` and `docs/handoffs/2026-04-15-handoff.md:111` claim "32 modules in tach.toml"; actual count differs). New CI workflow `.github/workflows/tach.yml`. Updated `.pre-commit-config.yaml` with local hook (`.pre-commit-config.yaml:11-18`). New `CONTRIBUTING.md` (122 lines, 60% of which is Tach-related). Modified `AGENTS.md` to delegate the import-direction check ("Codex skips this check", `AGENTS.md:89`). New ADR-26 (137 lines).

**Reopening triggers in evidence.** Phase 2 needed within hours when CI surfaced 6 baseline violations (`ADR-26...:120-136`). Step 12 was deferred to a separate PR for documentation reconciliation — explicitly so the code change and the doc change could be reviewed independently. The whole "Phase 1 / Phase 2 / Step 12" sequence is itself an emergent multi-PR pattern (see Section 9).

### `gotchas` skill

**How it entered.** Per `gotchas.md:4-5`: "moved from `~/.claude/skills/gotchas/gotchas.md` (global → project scope)". This is the only documentation of the move event. No JOURNAL entry.

**How it was anchored.** `.claude/skills/gotchas/SKILL.md` (5-line frontmatter only). `.claude/skills/gotchas/gotchas.md` (294 lines, organized by subsystem, every entry has `Trigger / Symptom / Fix / verify / Last triggered`). Format declared at `gotchas.md:6`: "Use negative constraints ('Do NOT...') over positive descriptions where possible". Cross-references in `CLAUDE.md:43` (still pointing at global path) and `docs/HANDOFF.md:213,447`.

**Reopening triggers in evidence.** Per the per-entry `Last triggered:` line. Per the global Self-Evolution Protocol (referenced in user's global CLAUDE.md). Inflated count drift: HANDOFF.md says "Gotchas \| 37 \| 2026-03-28" (`docs/HANDOFF.md:25`); the file currently has ~30 entries (counting `**Gotcha:**` headers) — but `[MERGED]` and `[PROMOTED]` markers indicate consolidation, so the count delta is consistent with curation.

### Diagrams (ADR-25)

**How it entered.** Council #25 (no transcript file in `docs/decisions/transcripts/`); ADR-25 (24 lines).

**How it was anchored.** `docs/diagrams/conventions.yaml` (31 lines; explicitly "read by Claude Code, not by scripts" at line 1 — i.e., it is a normative spec for the LLM, not a render config). Three `.mermaid` files. Three `.svg` files. `scripts/render-diagrams.ps1` (referenced in `JOURNAL.md:24`, has a known Join-Path bug per `docs/handoffs/2026-04-15-handoff.md:88`). Pointers in `docs/ARCHITECTURE.md:8` ("→ System context diagram: ...") and lines 205, 342.

**Reopening triggers in evidence.** "Diagrams v1 functional but visually weak (monochrome, low detail on dark theme)" (`docs/handoffs/2026-04-15-handoff.md:58`). "Diagram v2 — add colors (classDef), rewrite container-module with real dependencies, improve dark theme readability" (`docs/handoffs/2026-04-15-handoff.md:87`). Hard limit: max 3 diagrams (`ADR-25...:23`).

### Common shape across all four adoptions

`brief / incident / Codex finding` → `Council debate (4-model panel + Claude synthesizer)` → `ADR-NN-*.md` (≤20-line distillation, exception: ADR-26 at 137 lines, ADR-27 at 184 lines) → `tach.toml` / `pre-commit` / `CI workflow` (mechanical anchors) → `CONTRIBUTING.md` / `AGENTS.md` updates → JOURNAL entry. CHANGELOG, CLAUDE.md, HANDOFF.md updates lag inconsistently.

---

## Section 8 — Staleness & Drift

### Numerical drift (specific evidence)

| Where | Stated | Likely actual | Source |
|-------|--------|---------------|--------|
| `CLAUDE.md:29` | "CLIs (2,404 tests)" | ~2,515 | `CHANGELOG.md:17` ("2507 -> 2515 green") |
| `CLAUDE.md:54` | "Council Decisions: 24" | 27 (ADR-27 just drafted; ADR-26 in flight) | `git log` and `docs/decisions/ADR-2*.md` glob |
| `docs/HANDOFF.md:17` | "Tests passing \| 2,412 \| 2026-03-29" | ~2,515 | same |
| `docs/HANDOFF.md:23` | "Council decisions \| 24 \| 2026-03-29" | 27 | same |
| `docs/HANDOFF.md:24` | "ADRs \| 24" | 27 | same (ADR-25, 26, 27 all post-date) |
| `docs/HANDOFF.md:25` | "Gotchas \| 37 \| 2026-03-28" | ~30 (curation; 2 added 2026-04-21) | `gotchas.md` per-entry headers |
| `docs/HANDOFF.md:393` | "decisions/ADR-NN-*.md   22 ADR summaries" | 27, and the path is wrong (it's `docs/decisions/`, not `decisions/`) | both wrong |
| `README.md:18` | "**Total** \| \| **2,412** \| \|" | ~2,515 | same |
| `docs/handoffs/2026-04-15-handoff.md:111` | "32 modules in tach.toml" | 27 [[modules]] entries | `tach.toml` count |
| `docs/handoffs/2026-04-15-handoff.md:63-64` | "32 modules ... ADR-26 doc references 34 from Phase 1 bootstrap; 2 removed during sync" | self-acknowledged drift | already noted in same file |

### Reference drift (citations to non-existent or wrong-location files)

- `docs/ARCHITECTURE.md:423-426`: cites `docs/audits/2026-04-21-p1-verification.md` — **file does not exist**.
- `docs/HANDOFF.md:393`: "decisions/ADR-NN-*.md" — wrong directory; ADRs live in `docs/decisions/`.
- `docs/HANDOFF.md:194-195`: "Full transcripts: `.ecosystem/council_transcripts/DECISION_NN_*.md`" and "ADR summaries: `decisions/ADR-NN-*.md` (ADR-01 through ADR-23)" — `JOURNAL.md:223` records that `.ecosystem/` was eliminated 2026-03-30 ("Eliminated `.ecosystem/`. Moved: ... `archive/` (32 files) → `docs/archive/`, `council_transcripts/` (25 files) → `docs/decisions/transcripts/`"). HANDOFF.md still cites the old paths.
- `docs/decisions/README.md:29`: table ends at ADR-21; ADR-22..27 missing from the index.
- `docs/HANDOFF.md:312-320`: "Gemini Models (updated 2026-03-28)" lists `gemini-2.0-flash-lite` and `gemini-2.0-pro-preview`. `gotchas.md:68` records "all removed as of 2026-03-12. Verified RESOLVED 2026-03-30: 0 matches in src/. Current models in use: gemini-3-flash-preview, gemini-3.1-flash-lite, gemini-3.1-flash, gemini-3.1-pro-preview".
- `docs/diagrams/conventions.yaml:18-23`: declares colors for `layer_0..layer_3` with labels "Foundation / Core services / Orchestration / **Composition**" — but the canonical Tach taxonomy (per `tach.toml:23-28` and `docs/ARCHITECTURE.md:171`) has the four layers named **interface / orchestration / core / foundation**. "Composition" is an old / different name; "interface" is current.

### Pre-consolidation language still present

`docs/HANDOFF.md` extensively uses "corp-by-os", "CKE", "CPE", "COM" as separate package nouns (e.g., lines 65-95 in the pipeline section). The 2026-03-29 consolidation moved all six packages into `src/corp/`. The HANDOFF still narrates the system as a 6-package layout in places.

### Process rituals stated vs. observed

- "Update HANDOFF.md at the end of every major session" (`CLAUDE.md:85-88`). Observed: last regen 2026-03-29; multiple major sessions since.
- "3 lines per session" in JOURNAL (`JOURNAL.md:3`). Observed: recent entries are paragraphs (e.g., `JOURNAL.md:9` is a 130-word paragraph for "Did").
- gotcha "Last triggered" updates per protocol. Observed: most entries still say `2026-03-25` (initial seeding date), suggesting the field is not being updated when a gotcha re-fires.

---

## Section 9 — Gaps & Open Questions

### Documented but not practiced (or practiced inconsistently)

- **HANDOFF.md regeneration cadence.** Documented every major session; observed once in last 25+ days.
- **3-line JOURNAL format.** Documented at top of file; not enforced.
- **gotcha "Last triggered" update on re-fire.** Documented in user's global CLAUDE.md self-evolution protocol; rarely updated.
- **`./scripts/dev-check.ps1` before merging.** Documented in `CLAUDE.md:76` and `CONTRIBUTING.md:46`. Hard to verify from artifacts; inferred-but-unobserved.

### Practiced but not documented (or documented elsewhere only)

- **`hotfix/*` branch naming convention.** Used 2026-04-21 but absent from `CONTRIBUTING.md:5-11`.
- **Multi-PR ADR rollout pattern.** ADR-26 → Phase 1 + Phase 2 + Step 12. ADR-27 → PR-1 (foundation) + PR-2 (migration) + PR-3 (CI) + PR-4 (vault writer). The pattern is implicit in both ADRs but never declared as a project convention.
- **Codex re-review-after-amendment loop.** Used 2026-04-21 (`docs/audits/2026-04-21-codex-hotfix-review.md:92`) — strong pattern, no doc.
- **`verify:` line on every learned rule and gotcha.** Used pervasively; semantics ("Grep / Glob / manual") are not defined in any contract file.
- **Failing-tests-first commit pattern for safety fixes.** Commit `21e062e` "test(safety): failing regression tests for P1-1, P1-2, P1-3" landed *before* the fixes. Not declared as a convention.
- **One-off transcript filing for ADR-27.** ADR-27 transcript at `docs/decisions/ADR-27-council-onedrive-centralization.md`, breaking the `docs/decisions/transcripts/DECISION_NN_*.md` pattern. No note explaining the deviation.
- **Acknowledged-limitations section as part of an ADR.** ADR-27 explicitly lists "Acknowledged limitations" (`ADR-27...:79-86`). ADR-26 has "Deferred" (`ADR-26...:114-118`). Older ADRs do not. Pattern is emerging but not codified.

### Open questions that are actionable, not philosophical

1. **Source-of-truth declaration for handoff.** Is `docs/HANDOFF.md` (living, scripted) deprecated by `docs/handoffs/YYYY-MM-DD-handoff.md` (frozen, manual), kept in parallel, or is the new folder for one-off Scale-aware events only? Decision needed before the next major session — current state means a new chat is told to read a 25-day-stale doc.
2. **Single source of truth for layer + invariants definitions.** Which file is canonical when CLAUDE.md, AGENTS.md, ARCHITECTURE.md, and `tach.toml` give different versions? Especially: does AGENTS.md need to keep its inline layer table now that Tach enforces it?
3. **CLAUDE.md update protocol.** Currently has hard-coded counts ("24 ADRs", "2,404 tests") that go stale within days. Either the counts move to a script-updated section, or they are removed from CLAUDE.md and live only in HANDOFF.md. Not both.
4. **`docs/decisions/README.md` truncation.** Index ends at ADR-21. Either auto-generate, or commit to manual maintenance with a process gate.
5. **Transcript naming convention for new ADRs.** Council debates that produce ADR-NN should produce `docs/decisions/transcripts/DECISION_NN_*.md` per existing convention, OR `docs/decisions/ADR-NN-council-*.md` per ADR-27's precedent. Pick one.
6. **AST safety scanner pre-commit hook.** ADR-27 specifies a pytest test (`tests/safety/test_no_unguarded_writes.py`). Should it also be a pre-commit hook the way Tach is, or only CI? Not specified in ADR-27 design section.
7. **Adding a second AI agent contract.** AGENTS.md is currently Codex-specific (`AGENTS.md:1-2`: "This file is read automatically by Codex CLI (OpenAI). Codex is a read-only code reviewer in this repo"). When a future agent (Gemini-as-reviewer, a Chinese-model agent, a deep-research subagent) joins, does it get its own `<NAME>.md`, a section in AGENTS.md, or a different file? The current pattern is "one file per agent role", which scales linearly.
8. **Subagent registration.** Claude Code subagents have a definitions folder (`.claude/agents/` typically). The repo has `.claude/skills/gotchas/` but no subagents directory observed. If subagents start being used, the directory + naming convention + invariants per subagent need a place to live.
9. **Council panel reproducibility.** ADR-26 cites Council #26 with no panelist list in the ADR; ADR-23 lists "deepseek-reasoner, gemini-3.1-pro-preview, grok-4.20-beta, gpt-5.4" with synthesizer = claude; ADR-27 uses "claude-opus-4-7, gemini-3.1-pro-preview, grok-4.20, gpt-5.4" + synthesizer = claude-sonnet. Pinning policy is implicit, evolving, and not recorded.
10. **Self-evolution corrections location.** Repo CLAUDE.md mentions "Learned Rules (project-specific, graduated from corrections)" without saying *where* the corrections.jsonl lives or how promotion to CLAUDE.md is triggered. The user's global CLAUDE.md describes the protocol; the repo's does not.

---

## Section 10 — Raw Observations

Surfaced during the read but not naturally fitting Sections 1-9.

- **Two commits with identical subject lines.** `5ea65b3 docs(ARCHITECTURE): replace 7-layer model with 4-layer Tach taxonomy` and `803540c docs(ARCHITECTURE): replace 7-layer model with 4-layer Tach taxonomy` (both visible in `git log`). Either merge artifact or accidental double-commit. Worth a `git show` in any future cleanup.
- **`ollama>=0.4.0` is a required dependency** in `pyproject.toml:20` — not under `[project.optional-dependencies]`. No ADR for local-LLM adoption is on disk; HANDOFF mentions "Local AI — Ollama exploration" as #8 in Open Decisions (`docs/HANDOFF.md:428`).
- **CHANGELOG mixes formats.** Recent entries (Apr-22, Apr-21) use `### YYYY-MM-DD` date headers; the older block uses `## [1.0.0] - 2026-03-28` semver header (`CHANGELOG.md:1-43`). No narrative about which is current.
- **`docs/decisions/README.md` is mid-file truncated** — ends at line 38 ("How to add a new ADR" section, step 5). The table only goes to ADR-21. There is no closing `---` or page-end marker.
- **`AGENTS.md` lists `extraction/` twice in adjacent sections**: once in module structure (`AGENTS.md:30`) and once in foundation layer assignments (`AGENTS.md:51`). Not contradictory, but redundant.
- **The ADR-27 council file uses `claude-opus-4-7`**, which matches the model running this analysis (per the system context). Worth noting only because it indicates the Council panel is being kept on the latest Claude version as it ships.
- **`gotchas.md:1` says "Last updated: 2026-03-30"** but the two new entries about the 2026-04-21 hotfix are present (`gotchas.md:200-211`). The header date is now ~3 weeks behind the file's actual content.
- **Pre-commit does not enforce ADR-27's planned AST scanner.** `.pre-commit-config.yaml` currently has only ruff and tach. ADR-27 specifies pytest-based enforcement (`ADR-27...:56-63`); when PR-3 lands, pre-commit will likely need an addition.
- **`tach.toml` declares `path = "corp.project_resolver"` under the "ORCHESTRATION" comment block (`tach.toml:116-132`)** but with `layer = "core"`. This is the Phase-2 reclassification, but the comment was not moved with the entry. A reader scanning by comment header will mis-classify.
- **`tach.toml` declares `path = "corp.query_engine"` under the "INTERFACE" comment block (`tach.toml:157-162`)** but with `layer = "orchestration"`. Same comment-vs-content mismatch as above.
- **`update_handoff.py:11` docstring says "Update MASTER_HANDOFF.md"** — old name; the file was renamed to `docs/HANDOFF.md` per `JOURNAL.md:223` and `CHANGELOG.md:23`. The script targets the right path but its own docstring is outdated.
- **`docs/HANDOFF.md:451`** asserts gotcha count "(41 gotchas)" inline, while the live-stats table at `docs/HANDOFF.md:25` says 37. Two different numbers in the same file.
- **CONTRIBUTING.md is the only file with a one-liner pre-merge command** (`pytest -x --tb=short && pre-commit run --all-files && tach check`, `CONTRIBUTING.md:38-42`). CLAUDE.md and HANDOFF.md only point to `dev-check.ps1` without saying what it runs.
- **`docs/ARCHITECTURE.md:5`** is dated `Last updated: 2026-03-30` but the file was edited 2026-04-22 to add the ADR-27 cross-reference (commit `1b6c293`). Header date not updated.
- **Two ADR-27 files exist**: `docs/decisions/ADR-27-safety-invariants.md` (the actual ADR, 184 lines) and `docs/decisions/ADR-27-council-onedrive-centralization.md` (the Council transcript, 1019 lines). They sort adjacently in any glob; a reader doing `Read ADR-27-*.md` would need to know which is which.
- **`AGENTS.md:43` "ENFORCED BY TACH"** — Tach was adopted 2026-04-15 per ADR-26. AGENTS.md absorbed the change in the Step-12 reconciliation. This is the only contract file that explicitly delegates a check to mechanical enforcement; CLAUDE.md does not delegate any of its rules to a tool.

---

## Provenance

Files read in full: `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `README.md`, `.claude/skills/gotchas/SKILL.md`, `.claude/skills/gotchas/gotchas.md`, `docs/decisions/README.md`, `docs/ARCHITECTURE.md`, `docs/HANDOFF.md`, `JOURNAL.md`, `CHANGELOG.md`, `docs/decisions/ADR-25-diagram-strategy.md`, `docs/decisions/ADR-26-tach-adoption.md`, `docs/decisions/ADR-23-monorepo-internal-architecture.md`, `docs/decisions/ADR-27-safety-invariants.md`, `docs/audits/2026-03-30-codex-full-audit.md`, `docs/audits/2026-04-15-tach-baseline-violations.md`, `docs/audits/2026-04-21-codex-hotfix-review.md`, `docs/handoffs/2026-04-15-handoff.md`, `docs/diagrams/conventions.yaml`, `scripts/update_handoff.py`, `tach.toml`, `pyproject.toml`, `.pre-commit-config.yaml`.

Files sampled: `docs/decisions/transcripts/DECISION_23_monorepo_internal_architecture.md` (first 120 lines of 1053), `docs/decisions/transcripts/DECISION_24_mywork_knowledge_architecture.md` (first 100 lines of 1238), `docs/decisions/ADR-27-council-onedrive-centralization.md` (first 100 lines of 1019).

Files looked-up by directory listing only: `docs/decisions/transcripts/` (24 files, all DECISION_01..24 + 2 SUPERSEDED), `docs/decisions/ADR-2*.md` glob, `docs/audits/`, `docs/handoffs/`.

Git log range examined: HEAD..40 commits back (covers 2026-04-15..2026-04-22 in detail, plus references to earlier work).

No file in `corp-monorepo` was modified during this analysis. Output committed only to `.dev-knowledge`.
