---
type: audit
scope: ai-council (deep conformance re-pass, read-only, file-state-verified)
date: 2026-05-23
author: claude-opus-4-7 + rob
status: immutable
supersedes: none
related: docs/audits/2026-05-11-ai-council-scrum-master-review.md, docs/audits/2026-05-23-corp-monorepo-deep-audit.md
---

# ai-council — Deep Conformance Audit (re-pass) vs current `.dev-knowledge` standards

**Date:** 2026-05-23
**Target repo:** `ai-council`
**Target HEAD:** `2a980ab713d2e2278a3fb5604be4bf700856379f` ("docs: merge chunk4 — retire AGENTS.md, CLAUDE.md v2.1 live (ADR-53)", 2026-05-19)
**Auditor:** Claude Code (read-only; ADR-36 contract — zero `ai-council/` files modified)
**Output home:** `.dev-knowledge/docs/audits/` (this file)
**Routing:** scrum-master review pattern — findings route to a dedicated `ai-council` browser-chat session for remediation decisions; this audit identifies, it does not remediate.

**Basis (the standard):** `.dev-knowledge` ADRs and artifacts as they stand on 2026-05-23, specifically:
ADR-51 (architecture doc convention) **+ amendment 2026-05-22** (codemap generator output spec / embedded-Mermaid form);
ADR-34 (file naming); ADR-38 (universal baseline + A3/A4 root-placement; **tier M** mandatory set ≠ corp's tier L); ADR-39 (file lifecycle);
ADR-41 + ADR-47 (BACKLOG mandate + demoted convention); ADR-46 (dated-entries, demoted); ADR-31 (authority model);
ADR-30 (default branch); ADR-33 (VISION); ADR-49 (CHANGELOG/BACKLOG_ARCHIVE retirement); ADR-53 (CLAUDE.md canonical); `templates/ARCHITECTURE-template.md`;
`.dev-knowledge/ARCHITECTURE.md` (post layer-model-Mermaid exemplar); PLAYBOOK §17 Code Quality + §18 Ecosystem Audit + §Codemap workflow.

**Prior baseline (re-pass anchor):** `docs/audits/2026-05-11-ai-council-scrum-master-review.md` (dated 2026-05-11, executed 2026-05-12 — the "2026-05-12 N=1" pass referenced in the routing brief). Ten findings: 1 critical, 6 important, 3 minor.

---

## 1. Why this audit exists (delta since the 2026-05-11 baseline)

ai-council was last reviewed cross-repo on **2026-05-11** (`docs/audits/2026-05-11-ai-council-scrum-master-review.md`) — the **first** empirical scrum-master review (N=1). That pass predates three material movements in the `.dev-knowledge` standard:

- **ADR-51 (2026-05-18) + its amendment (2026-05-22).** ADR-51 made a dedicated root `ARCHITECTURE.md` mandatory at **M and L** scale (Decision 1) and named ai-council in its rollout list. The 2026-05-22 amendment then specified the codemap's canonical form — an auto-generated **embedded Mermaid** block between `<!-- CODEMAP:START -->` / `<!-- CODEMAP:END -->` markers — and **closed** the ADR-51 "codemap generator output spec" open question. At the 2026-05-11 baseline, ARCHITECTURE.md was assessed "optional at M, no action" (per the ADR-38 table). That assessment is now superseded by ADR-51.
- **ADR-53 (2026-05-19) retired `AGENTS.md`.** The baseline's minor finding **M2 recommended *adding* AGENTS.md** (per the then-current ADR-28/ADR-52 and the ADR-31 baseline-violation list). ADR-53 inverts that: AGENTS.md is retired ecosystem-wide and its content merges into CLAUDE.md. The recommendation has flipped 180°.
- **PLAYBOOK §17 (Code Quality) + §18 (Ecosystem Audit) + §Codemap workflow** landed, and the layer-model Mermaid exemplar landed in `.dev-knowledge/ARCHITECTURE.md`. ai-council is now a registered repo in the ecosystem audit infrastructure (`ecosystem/ai-council/state.yaml`), with `vision_md` / `adr38_baseline` / `claude_md` all reported PASS in the 2026-05-23 ecosystem run.

**Consequence:** this re-pass (a) verifies the status of all ten 2026-05-11 findings at HEAD `2a980ab`, (b) surfaces NEW findings against the post-amendment standard, and (c) builds N=3 grounding for codifying the scrum-master review pattern.

**Headline result:** **all ten 2026-05-11 findings are CLOSED** (enumerated in §5). ai-council also created `ARCHITECTURE.md`, removed its local `docs/handoffs/` (centralized to `.dev-knowledge` per ADR-42), and retired `AGENTS.md`/`CHANGELOG.md` — all conformant moves. The residual conformance debt is small and low-severity.

> **Premise corrections (the routing brief stated two facts that file-state contradicts).** (1) The brief said *"ai-council retains CHANGELOG; ADR-49 specific to `.dev-knowledge`."* File-state: ai-council **removed** `CHANGELOG.md` and cites ADR-49 for it (`CLAUDE.md:109`, JOURNAL); and ADR-49's Decision is written ecosystem-wide ("each repository"), not `.dev-knowledge`-only. (2) The brief framed ARCHITECTURE.md as "optional at tier M (per ADR-38 A3/A4) … if absent that's CONFORMS." ADR-51 Decision 1 + `templates/ARCHITECTURE-template.md:20` make it **mandatory at M**. Both are moot for findings here (ai-council *has* ARCHITECTURE.md and *correctly* lacks CHANGELOG), but they expose two upstream `.dev-knowledge` standard inconsistencies — flagged in §7, out of scope to fix in this audit.

---

## 2. Methodology

- **Read-only.** Glob/Grep/Read of the ai-council working tree at HEAD `2a980ab`; `git log`/`git status` only. No execution, no writes. The gitignored `output/`, `council_inbox/`, and cache trees (`.mypy_cache/`, `.ruff_cache/`, `.venv/`) are out of scope.
- **Standard refresh.** Read the ADRs, template, exemplar, and PLAYBOOK sections listed in the Basis above.
- **Citations.** Every finding cites an ai-council `file:line` (or a verified file-state fact) on the evidence side and a specific ADR/template clause on the standard side.
- **Tier discipline.** ai-council is **Scale M** (VISION frontmatter, CLAUDE.md §2; confirmed by the 2026-05-23 ecosystem audit). ADR-38's mandatory file set differs at M vs L — each ADR's tier-conditional clause is applied at M, **not** carried over from the corp-monorepo (tier L) audit.
- **In scope:** the six audit categories below + a dedicated visual subsection. **Out of scope:** internal code-correctness (provider retries, billing-gate logic, MinHash, etc.) — those belong to ai-council's own internal audits, not `.dev-knowledge`-standards conformance. `.dev-knowledge` self-audit and corp-monorepo are out of scope.
- **Re-pass nature tags:** each finding is tagged **STILL OPEN** / **CLOSED since 2026-05-11** / **NEW post-2026-05-22** / **NEW (other)**.
- **Per-finding format:** Severity / Category / Evidence / Standard / Gap / Recommendation / Difficulty. Severity: **CRITICAL** (load-bearing convention violated; blocks work) · **HIGH** (significant drift, visible to all consumers) · **MEDIUM** (real, deferrable) · **LOW** (polish).

---

## 3. Findings by category

### Category A — Architecture & visual conformance (ADR-51 + amendment 2026-05-22)

> Context: ai-council **created** `ARCHITECTURE.md` on 2026-05-19 from the ADR-51 canonical template (JOURNAL 2026-05-19). It is **strongly conformant on form** — YAML frontmatter present (`scale: M` / `last_reviewed: 2026-05-19` / `status: active` / `owner: Rob`, `ARCHITECTURE.md:1-6`), every `##` header carries a `[CORE]`/`[L-opt]` scale-tag, the three CORE sections are correctly named (`Purpose [CORE]`, `Codemap [CORE]`, `Layer Boundaries & Invariants [CORE]`), and the codemap section already contains `<!-- CODEMAP:START -->` / `<!-- CODEMAP:END -->` markers. The ADR-51 Decision 4 *content* minimum (purpose + codemap + layers + invariants) is fully met, with 7 well-formed invariants (`:85-95`). The doc is **4 days old at HEAD**, not stale. Two residual items only:

#### [MEDIUM] [A] Codemap is in transitional text form and carries a now-false "Open item" note — NEW post-2026-05-22

**Evidence:** `ARCHITECTURE.md:21` reads: *"**Open item.** The codemap generator output spec is undecided (ADR-51 open question). This codemap is hand-maintained in the transitional text form until the generator ships."* The CODEMAP-bounded block (`:23-59`) is a plain ```` ``` ```` fenced ASCII module tree — **not** a ```` ```mermaid ```` block.
**Standard:** ADR-51 amendment 2026-05-22 **closed** that exact open question, shipped the generator at `.dev-knowledge/scripts/codemap/cli.py`, and set the canonical form to embedded Mermaid (`templates/ARCHITECTURE-template.md:46-71`). The amendment's §Per-repo adoption clause **permits** a hand-maintained transitional codemap until generator opt-in — so the text form is **not a violation**. But the note's stated justification ("undecided … until the generator ships") is now factually wrong: the spec is decided and the generator exists.
**Gap:** the note misrepresents the current standard state to every reader; the codemap form has not yet been upgraded to Mermaid. Because the markers are already present, generator opt-in is a one-command swap (unlike corp-monorepo, which lacks markers).
**Recommendation:** (1) replace the "Open item" note with a one-liner noting the generator shipped 2026-05-22 and adoption is opt-in; (2) either opt into the generator per PLAYBOOK §Codemap workflow (`generate . --source-root src --write`; note ai-council has no `tach.toml`, so it runs in degraded mode = no layer colors — acceptable, or add `tach.toml` first), **or** hand-convert the ASCII tree to inline Mermaid mirroring the exemplar.
**Difficulty:** low (note) / low–medium (generator opt-in or Mermaid hand-conversion).

#### [LOW] [A] Layer model rendered as prose + table, not inline Mermaid — NEW post-2026-05-22

**Evidence:** `ARCHITECTURE.md:65-83` renders the 4-layer model (`interface → orchestration → core → foundation`) as a prose sentence plus a module-to-layer markdown table. The current `.dev-knowledge/ARCHITECTURE.md:47-64` exemplar renders its layer model as an inline Mermaid `flowchart`.
**Standard:** `templates/ARCHITECTURE-template.md` §Layer Boundaries does **not** mandate Mermaid for the layer model (only for the codemap). Not a violation — a visual-convergence opportunity vs the exemplar.
**Recommendation:** optional — add an inline Mermaid layer flowchart when the codemap is upgraded (single visual pass). See Visual subsection.
**Difficulty:** low.

---

### Category B — Naming compliance (ADR-34)

#### [MEDIUM] [B] Two governance docs prescribe underscore ADR naming "per ADR-34" — the opposite of ADR-34 — and one fresh violation has already resulted — NEW (other)

**Evidence:** `CLAUDE.md:32` (§4 Conventions) reads *"`ADR-NN_topic.md` future ADRs (7 existing kebab-case grandfathered per ADR-29)"*; `docs/decisions/README.md:3` reads *"Future ADRs use **underscore** naming per ADR-34."* The resulting artifact: `docs/decisions/ADR-08_research-degradation-alarm.md` uses an underscore after the number, while `ADR-01-…` through `ADR-07-…` all use the hyphen.
**Standard:** ADR-34 (amended 2026-05-11) is a **universal hyphen mandate** — canonical form `ADR-NN-topic.md` (`ADR-34:44-52, 61`). Both ai-council docs cite ADR-34 as the authority for the **opposite** convention.
**Gap:** the misattribution is self-propagating — it already produced ADR-08's underscore filename (the same failure class as the baseline's I5 "fresh violation"), and will produce more on every future ADR. This is the root-cause finding; the ADR-08 filename is its visible symptom.
**Recommendation:** correct both docs to the hyphen form; rename `ADR-08_research-degradation-alarm.md` → `ADR-08-research-degradation-alarm.md` and update the `docs/decisions/README.md` index link + any cross-references. Consider closing the BACKLOG P2 "CI enforcement of hyphen-only separator" item (`ai-council/BACKLOG.md:49`) in the same pass.
**Difficulty:** low.

**No further naming findings.** ADR-01..07 use hyphen ✓; the two docs/ renames flagged at baseline (I4/I5) are done — `docs/council-question-guide.md` and `docs/synthesis-quality-rubric.md` are now hyphen-compliant ✓; the two legacy `_CODE_REVIEW_REPORT.md` files are archived under `docs/audits/archive/legacy/` (baseline I6) ✓; audits use `YYYY-MM-DD-topic.md` ✓; `output/`/`council_inbox/archive/` ISO-timestamp data files are exempt ✓ (and gitignored). The council-CLI emitter's `YYYYMMDD_HHMMSS` underscore is a known, separately-tracked open question (`BACKLOG.md:55`), not re-raised here.

---

### Category C — Sacred files & lifecycle (ADR-38 tier M, ADR-33, ADR-53, ADR-39)

**No binding findings — ai-council conforms to the ADR-38 tier-M baseline as audited.**

- **ADR-38 baseline (M tier):** all tier-M mandatory items present at root — `README.md` ✓, `VISION.md` ✓, `BACKLOG.md` ✓ (created since baseline — closes I1), `src/ai_council/` ✓, `tests/` ✓, `pyproject.toml` ✓ (full `[build-system]`/`[project]`/deps/`[project.scripts]`/`[tool.pytest]`/`[tool.ruff]`/`[tool.mypy]` — exceeds the minimum), `docs/` ✓. `ARCHITECTURE.md` present at root ✓ (optional at M per the ADR-38 table; **mandatory at M** per ADR-51 — either way, satisfied).
- **CHANGELOG.md absent — CONFORMS.** Removed per ADR-49 (`CLAUDE.md:109,128`; ADR-49 Decision "CHANGELOG is removed", ecosystem-wide). The audit-tool `adr38_baseline` check does not test for CHANGELOG (PLAYBOOK §18:2212). The ADR-38 table still *literally* lists CHANGELOG mandatory at M+, but ADR-49 (which did not amend the ADR-38 table) governs current practice — see §7 discrepancy. Not an ai-council gap.
- **ADR-53 (CLAUDE.md canonical):** `CLAUDE.md` is 139 lines (≤200), v2.1 12-section form, dedicated `ARCHITECTURE.md` carries the technical depth (ADR-51 §2 separation). `AGENTS.md` correctly **absent** — retired per ADR-53 chunk 4 (HEAD commit; JOURNAL 2026-05-19). This **inverts and closes** baseline M2. ✓
- **ADR-33 (VISION):** present, frontmatter parseable, content matches the **Lite** structure appropriate to scale M (Mission / Scope / Relationships / Lifecycle; Values + References omitted as Lite permits). Frontmatter `tier: M` matches the `.dev-knowledge` exemplar VISION verbatim — see §7 for the ADR-33-text-vs-practice discrepancy (an ecosystem issue, not ai-council drift). ✓
- **ADR-39 (6-element lifecycle):** ai-council keeps no explicit per-file lifecycle registry. **Not a finding** — ADR-39 is "**Mandate:** `.dev-knowledge`; **Recommendation:** child repos." ai-council is within the recommendation tier.

---

### Category D — BACKLOG conformance (ADR-41 + ADR-47)

#### [LOW] [D] BACKLOG header cites the superseded ADR-41 schema, not the governing ADR-47 — NEW (other)

**Evidence:** `BACKLOG.md:3` reads `<!-- schema: ADR-41 | grooming: per-handoff (~2 min) + quarterly deep (first 2026-07-01) -->`.
**Standard:** ADR-47 (2026-05-16 demotion) is now the governing convention; it relaxed ADR-41's strict schema to "one file, recommended (not enforced) entry shape." (Identical finding to corp-monorepo's Category D — a consistent cross-repo pattern.)
**Gap:** cosmetic — the citation points at the pre-demotion authority; the entries themselves conform.
**Recommendation:** update the header to "ADR-41 schema as relaxed by ADR-47" (or "ADR-47").
**Difficulty:** low.

**Otherwise conforms — and grooming is healthy.** Single `BACKLOG.md`; entry shape `### [P{N}] [open] <title>` + `**What:** / **Why:** / **Added:** / **Status:**` verified across all entries (`:12-104`); Stream-grouped with `## Stream: <name>` H2s (ADR-47 permits); no `BACKLOG_ARCHIVE.md` (ADR-49) ✓. Active grooming evidence: the surviving `tasks/todo.md` item was migrated here (`:39-43`, "was tasks/todo.md" — confirms baseline C1 closure), and the baseline I5 follow-up is tracked as a live P2 (`:49-53`).

---

### Category E — Cross-repo + governance (ADR-31, ADR-46, ADR-30)

**No findings — ai-council conforms as audited.**

- **ADR-30 (default branch):** HEAD is on `main`; CLAUDE.md §4 declares `feat/`/`fix/`/`docs/`/`chore/` branches off main. ✓
- **ADR-46 (demoted dated-entries):** `JOURNAL.md` uses ISO `### YYYY-MM-DD —` headers, newest-first, with the Did/Result/Changes/Abandoned/Next per-entry shape (ADR-49); the `normalize-headers` hook is wired (`.pre-commit-config.yaml:4-9`, scoped to `LESSONS|JOURNAL`). ✓
- **ADR-31 (authority):** VISION §Relationships and CLAUDE.md §1/§4 explicitly accept `.dev-knowledge` as the binding methodology source (ESSENTIALS/PLAYBOOK reads, cross-ecosystem lessons routed to `.dev-knowledge/LESSONS.md`). ✓
- **ADR numbering namespace:** ai-council's local ADRs are 01–08 — low numbers, **no collision** with `.dev-knowledge`'s 27+ range, and `CLAUDE.md §11` cleanly separates "Local (`docs/decisions/`)" from "Ecosystem (`.dev-knowledge/docs/decisions/`)". This is *better* than corp-monorepo, which had a namespace-prefix finding here. ✓
- **ADR-31 baseline-violation list is satisfied/superseded:** the three 2026-04-27 baseline violations were "ai-council: add AGENTS.md" (now superseded by ADR-53 — correctly absent), "ai-council: trim CLAUDE.md ≤200" (now 139 lines ✓), and a corp-monorepo item (out of scope). ✓

---

### Category F — Documentation quality (aspirational-vs-actual pattern)

> This category targets governance/user-facing docs that state a fact the file-state does not realize. All three items are in `README.md` and are low-severity polish; none are load-bearing.

#### [LOW] [F] README test count is stale — re-drifted since the baseline fix — NEW (other)

**Evidence:** `README.md:234` reads "**362 unit tests** covering all modules." File-state: `grep -rc 'def test_' tests/` sums to **405** test functions across 21 test files; JOURNAL 2026-05-19 records "**407** unit tests pass unchanged." Baseline finding I3 was fixed (354 → 362) on 2026-05-12, but the suite has since grown ~45 tests without a README re-bump. `CLAUDE.md` no longer states an absolute count (good).
**Standard:** documentation accuracy; the public entry point should not understate the suite by ~12%.
**Gap:** the same metric that I3 fixed has re-drifted — evidence that a pinned absolute count is a recurring staleness magnet.
**Recommendation:** bump to the current `pytest --collect-only -q` count, or drop the absolute number ("see `pytest --collect-only`").
**Difficulty:** low.

#### [LOW] [F] README contradicts itself on the default synthesizer — NEW (other)

**Evidence:** `README.md:152` (All options table) lists `--synthesizer NAME` default **`claude`**; `README.md:175` (Models section) states *"The default synthesizer is **Gemini**."* `ARCHITECTURE.md:129` ("default `gemini`"), `VISION.md:21`, and ADR-01 all say Gemini.
**Standard:** documentation accuracy / internal consistency.
**Gap:** the options-table default (`claude`) contradicts the rest of the repo's docs and ADR-01; one of the two README lines is wrong (the table).
**Recommendation:** correct the options-table default to `gemini` (verify against `runner.py:pick_synthesizer()`). While here, fix the §Transcript-Routing pointer `README.md:288` ("See `CLAUDE.md` for full architecture details") to point at `ARCHITECTURE.md` — architecture depth moved there per ADR-51/ADR-53.
**Difficulty:** low.

#### [LOW] [F] README "Related repos" lists obsolete repo names — NEW (other) / OPEN QUESTION

**Evidence:** `README.md:294-298` lists "corp-by-os — orchestrator / corp-os-meta — shared schemas / corp-knowledge-extractor — extraction engine / corp-rfp-agent — RFP automation." None of these match the current ecosystem repos named throughout the standard (`corp-monorepo`, `corp-ops`, `corp-sca-time-automation`, `.dev-knowledge`).
**Standard:** documentation accuracy.
**Gap:** these read as pre-consolidation product names (before the corp-monorepo merge). They may be intentional product-line labels, but they do not reconcile with the ecosystem inventory.
**Recommendation:** reconcile against the actual ecosystem repos or remove the section. (Architect: confirm whether these are intentional — see §7.)
**Difficulty:** low.

---

## 4. Visual aspect — diagrams & embedded-Mermaid upgrade plan

> Rob's explicit emphasis. Unlike corp-monorepo (a mature C4/Mermaid set), ai-council is a CLI tool with **no diagram artifacts at all** — there is no `docs/diagrams/` directory, and `ARCHITECTURE.md` has no `## Diagrams [M/L]` section. This subsection states that explicitly and gives the inline-Mermaid recommendations.

**Existing diagram inventory:** **none.** No `.mermaid`/`.svg` files; no `docs/diagrams/`.

**In-document visual artifacts (all currently text):**

| Artifact | Location | Current form | Disposition under post-2026-05-22 convention |
|---|---|---|---|
| Codemap | `ARCHITECTURE.md:23-59` (between CODEMAP markers) | plain ASCII module tree | **UPGRADE → embedded Mermaid** — either generator opt-in (`generate . --source-root src --write`) or hand-authored inline Mermaid. Markers already present → one-command swap. (Finding A1.) |
| Layer model | `ARCHITECTURE.md:65-83` | prose + markdown table | **OPTIONAL inline Mermaid** flowchart mirroring `.dev-knowledge/ARCHITECTURE.md:47-64`. Template does not mandate Mermaid here. (Finding A2.) |
| Data Flow | `ARCHITECTURE.md:99-121` | ASCII numbered pipeline | ASCII permitted (template §Data Flow shows ASCII). Optional Mermaid `flowchart` if the architect wants visual parity; not required. |

**`## Diagrams [M/L]` section:** absent. The template lists Diagrams as `[M/L]` but "add or omit as the repo needs," and the `.dev-knowledge` exemplar keeps a one-line Diagrams section that simply states "no Mermaid diagrams currently." For ecosystem convergence ai-council *could* add the same one-liner, but for a CLI tool with no system-context/pipeline diagrams this is genuinely optional — **not** a finding.

**Should ai-council have ARCHITECTURE.md + inline Mermaid at tier M? — already resolved.** Yes, and it does: ARCHITECTURE.md exists and is ADR-51-template-conformant. The only visual work outstanding is the codemap Mermaid upgrade (A1) and the optional layer-model Mermaid (A2).

**Visual upgrade plan, in order:**
1. Refresh the `ARCHITECTURE.md:21` "Open item" note (generator shipped 2026-05-22; opt-in).
2. Upgrade the codemap to embedded Mermaid — generator opt-in (PLAYBOOK §Codemap checklist: add `codemap-freshness` hook with `--source-root src` → `generate --write` → commit) **or** hand-author inline Mermaid between the existing markers.
3. (Optional) convert the layer model to inline Mermaid in the same pass.

**Diagram tally:** **0** existing diagram files; **0** stay-separate; **1** in-document artifact recommended for inline-Mermaid upgrade (codemap), **+1** optional net-new inline Mermaid (layer model), **+1** optional (data-flow). No SVG pipeline needed (VS Code 1.121 + GitHub render Mermaid natively, per the amendment).

---

## 5. Summary

**Active findings by severity:** **0 CRITICAL · 0 HIGH · 2 MEDIUM · 5 LOW** (7 total). Several CONFORMS/INFO results stated inline (all of C and E, most of B and D).

| Category | MEDIUM | LOW | Notes |
|---|---|---|---|
| A — Architecture & visual | 1 (A: codemap transitional + stale note) | 1 (A: layer model not Mermaid) | ARCHITECTURE.md otherwise strongly conformant (form + content) |
| B — Naming | 1 (B: underscore ADR misguidance → ADR-08 violation) | — | I4/I5/I6 all closed; otherwise conforms |
| C — Sacred files & lifecycle | — | — | conforms (ADR-38 M baseline; ADR-53; CHANGELOG removal per ADR-49) |
| D — BACKLOG | — | 1 (D: header cites ADR-41 not ADR-47) | otherwise conforms; healthy grooming |
| E — Cross-repo governance | — | — | conforms (cleaner ADR namespace than corp) |
| F — Documentation quality | — | 3 (F: test count, synthesizer default, related repos) | all README polish |
| Visual subsection | (folds into A) | | 0 diagrams; 1 codemap upgrade + 2 optional |

**Top 3 highest-impact active items:**
1. **Underscore-ADR misguidance (MEDIUM, B).** Two governance docs instruct the wrong (`ADR-NN_topic.md`) convention while citing ADR-34, which mandates the opposite; it has already produced `ADR-08_…`. Self-propagating, so fix the *guidance* (CLAUDE.md §4 + ADR README) plus rename ADR-08.
2. **Codemap transitional form + stale "Open item" note (MEDIUM, A1).** The note cites an ADR-51 open question that the 2026-05-22 amendment closed; the codemap form should move to Mermaid (markers already present — trivial swap).
3. **README documentation drift (LOW ×3, F).** Stale test count (362 vs ~405), self-contradictory synthesizer default, and obsolete "Related repos" list — all in the public entry point.

**Overall posture:** ai-council is **very strongly conformant** to current `.dev-knowledge` standards. The structural baseline is clean across sacred files (C), cross-repo governance (E), and BACKLOG (D); ARCHITECTURE.md exists and is template-conformant on both form and content (A). The residual debt is one self-propagating naming-guidance bug (B), one transitional-codemap upgrade (A1), and three README polish items (F) — none load-bearing, none CRITICAL or HIGH. **Rough conformance estimate: ~90%** against current standards — meaningfully ahead of corp-monorepo's ~80% (whose debt was concentrated in a pre-ADR-51, 7-week-stale ARCHITECTURE.md that ai-council does not have).

### Changes since the 2026-05-11 baseline — all ten findings CLOSED

| # (baseline) | Severity | Finding | Closure evidence at HEAD `2a980ab` |
|---|---|---|---|
| C1 | Critical | `tasks/todo.md` severely stale (255 vs 362 tests) | **CLOSED** — `tasks/` folder removed entirely; surviving item migrated to `BACKLOG.md:39-43` ("was tasks/todo.md") |
| I1 | Important | `BACKLOG.md` missing (ADR-41 M+ mandate) | **CLOSED** — `BACKLOG.md` present at root, ADR-47-conformant, 8 streams |
| I2 | Important | README architecture = pre-ADR-38 flat `src/` | **CLOSED** — `README.md:181-213` shows `src/ai_council/` namespace |
| I3 | Important | README test count stale (354) | **CLOSED** at 362 (but re-drifted to ~405 → new LOW F-finding) |
| I4 | Important | `docs/COUNCIL_QUESTION_GUIDE.md` non-compliant | **CLOSED** — renamed `docs/council-question-guide.md` |
| I5 | Important | `docs/SYNTHESIS-QUALITY-RUBRIC.md` (fresh viol.) | **CLOSED** — renamed `docs/synthesis-quality-rubric.md` |
| I6 | Important | 2 legacy `_CODE_REVIEW_REPORT.md` to archive | **CLOSED** — moved to `docs/audits/archive/legacy/` |
| M1 | Minor | VISION `last_reviewed` not bumped | **CLOSED** — now `2026-05-12` |
| M2 | Minor | AGENTS.md absent (recommend *adding*) | **INVERTED & CLOSED** — ADR-53 retired AGENTS.md; correctly absent |
| M3 | Minor | `tasks/lessons.md` stale | **CLOSED/superseded** — `tasks/` removed; `LESSONS.md` at root |

Additional conformant changes since baseline (not prior findings): `ARCHITECTURE.md` created (ADR-51); `docs/handoffs/` removed and centralized to `.dev-knowledge` (ADR-42); `CHANGELOG.md` removed (ADR-49).

---

## 6. Recommended remediation sequence (for the dedicated ai-council session)

| Step | Work | Findings closed | Depends on |
|---|---|---|---|
| 1 | **Naming-guidance fix.** Correct `CLAUDE.md:32` and `docs/decisions/README.md:3` to the hyphen form; rename `ADR-08_research-degradation-alarm.md` → `ADR-08-research-degradation-alarm.md`; update the README index link + cross-refs. Optionally close `BACKLOG.md:49` (CI hyphen-enforcement) in the same pass. | B (+ ADR-08 symptom) | — |
| 2 | **ARCHITECTURE.md codemap pass.** Refresh the `:21` "Open item" note; upgrade the codemap to embedded Mermaid (generator opt-in per PLAYBOOK §Codemap checklist, or hand-authored inline Mermaid); optionally add the inline-Mermaid layer model. One PR. | A1, A2, Visual steps 1-3 | — (markers already present) |
| 3 | **README polish batch** (one PR): test count → current (or drop the number); synthesizer-default table fix + `:288` pointer → ARCHITECTURE.md; reconcile/remove "Related repos". | F (×3) | — |
| 4 | **BACKLOG header** one-liner: ADR-41 → "ADR-41 as relaxed by ADR-47". | D | — |

All four steps are prerequisite-free and can run in any order / parallel. Step 2's generator opt-in is a per-repo operator decision (both the transitional text form and the Mermaid form satisfy ADR-51).

---

## 7. Open questions & discrepancies (state unclear, or upstream standard inconsistencies)

**Upstream `.dev-knowledge` standard inconsistencies surfaced by this re-pass (out of scope to fix here — flagged for a `.dev-knowledge` session):**

1. **ADR-38 still mandates CHANGELOG at M+, but ADR-49 removed it ecosystem-wide.** ADR-49 (2026-05-17) Decision: "CHANGELOG is removed" (worded for "each repository"); it amends ADR-46/ADR-47 but **not** the ADR-38 mandatory-files table (`ADR-38:98` still lists CHANGELOG mandatory at M+). The audit tool's `adr38_baseline` check does not test CHANGELOG. ai-council (and corp-monorepo) correctly have no CHANGELOG. **The gap is in ADR-38's un-amended table**, not in either child repo. Recommend amending ADR-38 to strike the CHANGELOG row. (This also corrects the routing-brief premise "ai-council retains CHANGELOG.")
2. **ARCHITECTURE.md is "mandatory at M" (ADR-51 Decision 1 + `templates/ARCHITECTURE-template.md:20`) yet "optional at M" (ADR-38 table + audit-tool WARN, PLAYBOOK §18:2212).** A three-way inconsistency. Moot for ai-council (it has one), but it should be reconciled so the standard speaks with one voice.
3. **ADR-33 says VISION frontmatter `tier:` ∈ {standard, lite}, but both the `.dev-knowledge` exemplar VISION and ai-council use `tier: M`** (the scale letter), alongside a separate `scale: M`. The audit-tool `vision_md` check only tests key *presence*, so the value-space drift is invisible to automation. ai-council **matches the exemplar**, so this is an ADR-33-text-vs-universal-practice discrepancy, **not** ai-council drift. Recommend either amending ADR-33 to match practice (drop the standard/lite value-space, or fold it into `scale`) or correcting both VISION files.

**ai-council state genuinely unclear from file inspection:**

4. **Exact unit-test count.** `def test_` sums to 405; JOURNAL records 407; README says 362. The authoritative collected count needs `pytest --collect-only -q` (not run — read-only audit, env-dependent). Regardless, 362 is stale (F-finding).
5. **`docs/decisions/transcripts/` is empty (0 files).** The 2026-05-11 baseline counted ~14 there. Curated transcripts now route to `.dev-knowledge/docs/decisions/transcripts/` (ADR-43); ai-council's local dir may be vestigial. Whether the empty directory should remain (and whether anything was lost vs deliberately re-routed) is unclear from file-state — architect to confirm. Not a conformance finding.
6. **README "Related repos" (corp-by-os / corp-os-meta / corp-knowledge-extractor / corp-rfp-agent).** Intentional product-line names, or obsolete pre-consolidation names? Drives whether F's "Related repos" item is a fix or a no-op.

---

## 8. Cross-references

- **`.dev-knowledge` standards:** ADR-51 (+ amendment 2026-05-22) · ADR-34 · ADR-38 (tier M; A3/A4) · ADR-39 · ADR-41 · ADR-47 · ADR-46 · ADR-31 · ADR-30 · ADR-33 · ADR-49 · ADR-53 · `templates/ARCHITECTURE-template.md` · `.dev-knowledge/ARCHITECTURE.md` (exemplar) · PLAYBOOK §17 / §18 / §Codemap workflow.
- **Prior baseline compared:** `docs/audits/2026-05-11-ai-council-scrum-master-review.md` (N=1 scrum-master review — all 10 findings closed at HEAD `2a980ab`).
- **Structure template:** `docs/audits/2026-05-23-corp-monorepo-deep-audit.md` (Prompt 8 / N=2). This report mirrors its section structure; findings differ in content (ai-council is tier M, has ARCHITECTURE.md, cleaner posture).
- **Routing:** scrum-master review pattern (BACKLOG Cross-stream "Apply scrum-master review pattern to other child repos" / "Codify scrum-master review authority"). **Builds N=3 grounding** for codification (ai-council 2026-05-11 N=1 · corp-monorepo 2026-05-23 N=2 · ai-council re-pass 2026-05-23 N=3).

---

**Contract preserved:** zero `ai-council/` files modified. Read-only per ADR-36.
