# Fleet boundary matrix — methodology-vs-project divergence across dev-knowledge / ai-council / corp-monorepo

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-11
- **Source-session:** CC (Opus 4.8), branch `docs/audit-fleet-boundary-matrix`, HEAD `380f018`. Read-only fan-out: 2 `Explore` subagents (ai-council, corp-monorepo) + hub self-sweep; synthesis + commit serial in the main thread (per the acceptance contract, item 6).
- **Status:** PROPOSAL-ONLY — a divergence matrix + per-row dispositions for operator ruling. No mechanism is built in this session (item 7).
- **Model:** claude-opus-4-8 (main-thread synthesis) + Sonnet `Explore` subagents (read-only scans).

> **Filename note (ADR-101).** The frozen contract fixed this file's name as `2026-07-11-fleet-boundary-matrix.md`. Under the ADR-101 §2 grammar `<date>-<class>-<slug>` the `<class>` token must come from the closed 11-class enum; `fleet` is not in it, so a strict reading wants `2026-07-11-technical-fleet-boundary-matrix.md` (class `technical`, slug `fleet-boundary-matrix`). The name is honored as the contract froze it; the ADR-101 refusal-gate (#306) is unbuilt, so nothing enforces it, and an existing file is grandfathered either way. Flagged for the architect as a candidate rename (§Candidate mechanisms).

---

## Executive so-what

The charter (2026-07-11 architect `SUPPLEMENT.md` Q1): **universalization + hermetization is P1** — dev-knowledge is the source of truth over what is *methodology-generic* vs *project-specific*; produce an evidence-based boundary **per surface**, then route it into mechanisms, never prose. The operator's framing correction is on record and governs this document: **Wave-1 n=2 proved the *enforcement* layer is in effect; it never proved *structural uniformity*.** That gap is this audit's subject.

This report **does not** emit an aggregate verdict, and treats **"all onboarded = all OK" as a banned claim shape** (contract item 5). Each surface below carries its own independent disposition; there is deliberately no fleet-level roll-up.

The load-bearing findings, stated as surface dispositions (detail + evidence per row below):

- The **CLAUDE.md 12-section skeleton is de-facto methodology** carried by all three repos, yet the only *explicitly marked* methodology block is the floor `@import` — the section-level methodology/project boundary is **unmarked and hand-maintained per repo** (Surface 2 → **DEFECT**). This is the structural-uniformity gap the charter names, and the seed for the fleet CLAUDE.md diff-routine (§Candidate mechanisms).
- The hub's **commit-msg + pre-push enforcement does not transfer**: both consumers install all three git-hook stages but leave commit-msg/pre-push **armed-but-empty** (Surface 3 → **DEFECT**; already filed #302/#309, and independently witnessed by the corp QA scorecard).
- The **`.claude/` contents boundary is under-specified**: the command set diverges (hub 4 vs consumers 1), skills are half-universalized (#308), workflows/rules diverge (Surface 9 → **DEFECT**).
- Several surfaces are genuinely uniform and correctly hub-owned (root file set, top-level baseline, `.code-workspace` template, cache-gitignore policy → **METHODOLOGY-GENERIC**), and several are legitimately per-project (CI/CD choice, `tach.toml`, provider `.env`, corp `tests/` nesting → **PROJECT-SPECIFIC** / flag-only).

---

## Method, scope, and inputs

**Surfaces audited (11)**, one matrix row each, per contract item 1: root files · CLAUDE.md section inventory · hook inventories (pre-commit/commit-msg/pre-push) · top-level folder sets · `protocols/` (presence + genre) · `.code-workspace` · cache-folder policy · `INSTALL.md` · `.claude/` contents (worktrees/workflows/skills/commands incl. `/codex-review` vs `/code-review`) · CI/CD currency · `tests/` layout (corp = **flag-only**).

**Columns:** `dev-knowledge` (hub — the methodology source), `ai-council`, `corp-monorepo`. Every cell is a **witnessed read** with a path/config cite. Fan-out was read-only (`Explore` agents cannot Edit/Write); synthesis and this commit are serial in the main thread.

**Builds on (cited, not re-derived — contract item 4):**
- **ADR-101** (`docs/decisions/ADR-101-hermetization.md`, Accepted 2026-07-11) — the sanctioned top-level set (§1), the `<date>-<class>-<slug>` grammar + closed 11-class enum (§2 + R3), the all-lowercase-kebab casing rule (R4), and the required header block (R5); this file dogfoods R5.
- **audit-template** (`templates/audit-template.md`) — the author-facing skeleton used here.
- **Naming census + gotchas universalization** — `docs/audits/2026-07-11-census-consolidated-morning-brief.md`. **Phase 4 (naming census, L166–185):** hub `docs/audits/` is 100% lowercase-kebab (L176); **ai-council is the cleanest child** — its `docs/audits/README.md` documents + enforces the hub `YYYY-MM-DD-<topic>` rule and quarantines pre-ADR-34 UPPERCASE to `archive/legacy/` (L182); **corp-monorepo is least-disciplined** — no README/convention, an UPPERCASE-underscore enum (`_AUDIT_`/`_BRIEF_`/`_EVIDENCE_`) **actively growing** 2026-07-07/08 (L183) — the divergence ADR-101 R4 fixes. **Phase 5 (gotchas universalization, L244–246):** the universal gotchas store is user-level `~/.claude/skills/gotchas/` (hub carries none); corp carries a project `gotchas` skill, **ai-council carries none** (no `.claude/skills/` dir; L245) — the half-adoption re-witnessed at Surface 9; `verify` self-flags its home open (#9).
- **QA n=2 scorecard + corp root-hygiene audit** — `corp-monorepo/docs/audits/2026-07-11-qa-lived-onboarding-and-root-hygiene.md` (root inventory 24 entries all-KEEP; Phase-1 QA lived arc: every organ fired, P1 findings = 0, two absences flagged = no commit-msg conventional gate, no pre-push `block_ff_push`). Sibling: ai-council `docs/audits/2026-07-09-qa-lived-exercise.md`.

**Not covered:** deep analysis of corp `tests/` (flag-only per contract); code-level dependency mapping (out of scope per SUPPLEMENT A3d); any mutation of ai-council/corp (read-only). UNVERIFIED residue is flagged inline where present.

---

## The divergence matrix (at a glance)

```
SURFACE                     | dev-knowledge (hub)        | ai-council                  | corp-monorepo               | DISPOSITION
----------------------------+----------------------------+-----------------------------+-----------------------------+-------------------
1 root files                | 7 UPPERCASE + 3 manifests  | + INSTALL.md, .env          | + .methodology.yaml,        | METHODOLOGY-GENERIC
                            | + 7 dotfiles; no INSTALL   | (no .ruff.toml/.pch.yaml)   | tach.toml (no INSTALL.md)   | (core set uniform)
2 CLAUDE.md section split   | monolithic authoring;      | floor @import + same §1-12; | floor @import + same §1-12; | DEFECT
                            | IS the methodology         | boundary unmarked           | boundary unmarked           | (boundary unmarked)
3 hook inventories          | 11 pre-commit +2 msg +1    | pre-commit only; msg/push   | pre-commit only; msg/push   | DEFECT
                            | push; all 3 stages full    | ARMED-BUT-EMPTY             | ARMED-BUT-EMPTY             | (#302/#309 parity)
4 top-level folders         | 14 sanctioned (+deploy/    | baseline + src/assets/      | baseline + src/data/eval/   | METHODOLOGY-GENERIC
                            | ecosystem/plugins/tmpl)    | council_inbox/output        | models/.github              | (baseline uniform)
5 protocols/ (genre)        | PRESENT: methodology       | PRESENT: Council DOMAIN     | ABSENT                      | DEFER
                            | (ESSENTIALS/PLAYBOOK/…)    | (invocation/rubric)         | (hub-homed via ../)         | (genre collision, Qb)
6 .code-workspace           | .dev-knowledge.cw (ref)    | .ai-council.cw (ADR-59)     | .corp.cw ("copied verbatim")| METHODOLOGY-GENERIC
7 cache-folder policy       | .pytest+.ruff; 3 ignored   | +.mypy (mypy); 3 ignored    | +.hypothesis; 3 ignored     | METHODOLOGY-GENERIC
                            |                            |                             |                             | (policy uniform)
8 INSTALL.md                | ABSENT                     | PRESENT (tier1 plugin)      | ABSENT                      | DEFER (Qf)
9 .claude/ contents         | 4 cmds/2 skills/agents/    | 1 cmd (override)/0 skills/  | 1 cmd (override)/gotchas/   | DEFECT
                            | wf/rules/generated         | rules(3)                    | wf/worktree                 | (under-specified)
10 CI/CD currency           | none (pre-commit+cloud)    | none (local-only)           | .github: newest 2026-06-06  | PROJECT-SPECIFIC
11 tests/ layout            | flat (~60 test_*.py)       | flat (~20 test_*.py)        | NESTED (~18 subdirs) FLAG   | DEFER (Qi, flag-only)
```

Legend for disposition: **METHODOLOGY-GENERIC** (uniform + hub-owned, correct) · **PROJECT-SPECIFIC** (legitimately per-repo) · **DEFECT** (drift-prone / gap to close) · **DEFER(reason)** (a ruling the operator must make before mechanizing).

---

## Per-surface detail (witnessed evidence per cell)

### Surface 1 — root files → METHODOLOGY-GENERIC (core set)
- **hub:** `ARCHITECTURE/BACKLOG/CLAUDE/CONTRIBUTING/JOURNAL/LESSONS/VISION.md` (7 UPPERCASE living docs) + `package.json`/`package-lock.json`/`pyproject.toml` + dotfiles `.dev-knowledge.code-workspace`, `.gitattributes`, `.gitignore`, `.pre-commit-config.yaml`, `.pre-commit-hooks.yaml`, `.ruff.toml`, `.worktreeinclude`. No `INSTALL.md`/`README`. _(hub sweep, `ls -ap`.)_
- **ai-council:** same 7 UPPERCASE + `pyproject.toml` + `.ai-council.code-workspace`/`.gitattributes`/`.gitignore`/`.pre-commit-config.yaml`; **plus** `INSTALL.md` (→ Surface 8) and `.env` (provider keys, PROJECT); **no** `.ruff.toml`/`.pre-commit-hooks.yaml`/`.worktreeinclude`. _(Explore scan, root listing.)_
- **corp:** same 7 UPPERCASE + `pyproject.toml` + `.corp-monorepo.code-workspace`/`.gitattributes`/`.gitignore`/`.pre-commit-config.yaml`/`.ruff.toml`; **plus** `.methodology.yaml` (hub Informant contract — METHODOLOGY, deploy-carried; operator-ratified KEEP-ROOT per SUPPLEMENT A3a) and `tach.toml` (monorepo package boundaries, PROJECT). _(Explore scan, root listing.)_
- **Boundary:** the **7 UPPERCASE living docs + `CLAUDE.md`/`CONTRIBUTING.md`/`VISION.md` + `pyproject.toml` + `.{repo}.code-workspace` + `.gitignore`/`.gitattributes`/`.pre-commit-config.yaml`** are the **methodology-generic universal root set** (uniform across all three). Per-repo deltas are individually dispositioned: `.env`/`tach.toml` = PROJECT-SPECIFIC; `.methodology.yaml` = METHODOLOGY-GENERIC (deploy artifact, present only where deployed); `INSTALL.md` → Surface 8 (DEFER).

### Surface 2 — CLAUDE.md section inventory (methodology-block vs project-block) → DEFECT
- **All three carry the identical 12-section skeleton** verbatim: §1 First read · §2 Repo identity · §3 Architecture · §4 Conventions · §5 Critical rules · §6 Session start protocol · §7 Slash commands · §8 Skills active · §9 Hooks active · §10 Anti-patterns · §11 Recent ADRs · §12 Section history. _(hub: `grep '^#' CLAUDE.md`; ai-council + corp: Explore heading enumeration.)_
- **hub:** monolithic — **no floor `@import`** (it is the source); the whole file is methodology-authoring. `@imports`: `commands-repo.md`, `methodology-roster.md`, `recent-adrs.md` (generated fragments).
- **ai-council:** `@.claude/CLAUDE-FLOOR.md` (line 7). Methodology-derived sections: §1/§6/§7/§8/§9 (session protocol, plugin commands, floor hooks, ecosystem ADRs). Project sections: §2/§3/§4/§5/§10/§11/§12 (debate-CLI identity, provider keys, google-genai anti-patterns, local ADR-01..08). `last_reviewed: 2026-07-06`.
- **corp:** `@.claude/CLAUDE-FLOOR.md` (line 7). Same methodology/project interleave; §4 is *mixed* (project naming + a hub `.methodology.yaml` bullet), §11 namespaces corp-local + ecosystem ADRs. `last_reviewed: 2026-07-10`, `version: 2.5`.
- **The gap (charter headline):** the 12-section skeleton is **de-facto methodology** — ~identical fleet-wide — yet the **only explicitly-marked, hub-owned methodology block is the floor `@import`**. Which sections are methodology vs project is **implicit and hand-maintained per repo**, so there is no machine-checkable "methodology block" to diff fleet-wide. This is the *structural-uniformity* gap the charter distinguishes from *enforcement* (which the QA n=2 scorecard proved fires). **Disposition DEFECT** — drives the fleet CLAUDE.md diff-routine (§Candidate mechanisms) and open-Q (a).

### Surface 3 — hook inventories (pre-commit / commit-msg / pre-push) → DEFECT
- **hub (all three stages armed AND populated):** pre-commit — `normalize-dated-headers`, `codemap-freshness`, `toc-freshness`, `toc-freshness-playbook`, `roster-freshness`, `claude-rosters-freshness`, `audit-index-freshness`, `validate-backlog`, `audit-health`, `ruff`, `coherence-nudge` (11); commit-msg — `backlog-id-on-close`, `backlog-filing-backpressure` (2); pre-push — `block-ff-push` (1). `default_install_hook_types: [pre-commit, commit-msg, pre-push]`. _(`.pre-commit-config.yaml`.)_ Several are **HUB-ONLY by construction** (`roster-freshness`, `claude-rosters-freshness`, `audit-index-freshness`, `coherence-nudge`) — correctly absent from consumers, **not a gap** (per the "enforcement organs not homogeneous" doctrine).
- **ai-council:** local `normalize-headers`, `floor-hash-verify`, `canonical_freshness` + hub-sourced (`github.com/rdwornik/dev-knowledge@v1.2.0`) `toc-freshness`, `toc-generate`, `backlog-id-on-close`. `default_install_hook_types: [pre-commit, commit-msg, pre-push]` **but no hook declares a commit-msg/pre-push stage → those stages are ARMED-BUT-EMPTY.**
- **corp:** `ruff@v0.15.8`, `tach-check`, `normalize-headers`, `floor-hash-verify`, `canonical_freshness` + hub `toc-freshness` (`toc-generate` manual). Same three stages installed, **commit-msg + pre-push ARMED-BUT-EMPTY** — independently witnessed by the corp QA scorecard ("no commit-msg conventional-commit gate; no pre-push `block_ff_push`", `2026-07-11-qa-lived-onboarding-and-root-hygiene.md`).
- **Boundary:** the hub's commit-discipline gates (`backlog-id-on-close`, `backlog-filing-backpressure`, `block-ff-push`) are **methodology-generic but do not transfer** to consumers. **Disposition DEFECT** — the enforcement-transfer parity gap, already filed **#302** (pre-push `block-ff-push` carrier) + **#309** (commit-msg carrier); this audit adds the *witnessed inventory* the filings predicted.

### Surface 4 — top-level folder sets → METHODOLOGY-GENERIC (baseline uniform)
- **hub (tracked):** `.claude .claude-plugin .vscode codex config deploy docs ecosystem logs plugins protocols scripts templates tests` (14, exactly ADR-101 §1's sanctioned Tier-1 set). Gitignored: `node_modules temp .pytest_cache .ruff_cache`. _(Note: `temp/` + `node_modules/` are gitignored, so not tracked members of the sealed set — but they exist on disk; a minor hygiene flag, not a seal breach.)_
- **ai-council:** baseline `.claude config docs logs scripts tests` + PROJECT `src assets council_inbox output`; gitignored `.mypy_cache .pytest_cache .ruff_cache .venv ai_council.egg-info`. **No** `deploy/ecosystem/plugins/templates/codex` (hub-source-only).
- **corp:** baseline `.claude config docs logs scripts tests` + PROJECT `src data eval models output` + `.github` (CI); gitignored `.hypothesis .pytest_cache .ruff_cache .venv`.
- **Boundary:** `.claude/ config/ docs/ logs/ scripts/ tests/` = **methodology-generic baseline** (uniform). `deploy/ ecosystem/ plugins/ templates/ codex/ .claude-plugin/` = methodology **source-side, correctly hub-only**. `src/ data/ eval/ models/ assets/ council_inbox/ output/` = PROJECT-SPECIFIC. Disposition METHODOLOGY-GENERIC for the baseline; project + source-side dirs are correct-by-design.

### Surface 5 — protocols/ (presence + genre) → DEFER (genre collision — open-Q b)
- **hub:** PRESENT, **methodology genre** — `ESSENTIALS.md`, `PLAYBOOK.md`, `HANDOFF_PROCESS.md`, `HANDOFF_BOOT.md`, `AI_COUNCIL_PROCESS.md`, `SESSION_SETUP.md`, `DEFINITION_OF_DONE.md`, `ENVIRONMENT.md`, `AGENT_FRAMEWORK.md` (+ `archive/`). _(`ls protocols/`.)_
- **ai-council:** PRESENT, **project/domain genre** — `COUNCIL_INVOCATION_CONTRACT.md`, `COUNCIL_QUESTION_GUIDE.md`, `SYNTHESIS_QUALITY_RUBRIC.md` (Council domain, *not* methodology; the methodology protocols are read via `../.dev-knowledge/protocols/`).
- **corp:** **ABSENT** — `protocols/` does not exist; CLAUDE.md §1 points at `../.dev-knowledge/protocols/{ESSENTIALS,PLAYBOOK}.md`. (Operator wants per-package interface/protocol docs in corp — SUPPLEMENT Q4b — but none exist today.)
- **Boundary is UNRESOLVED:** the same folder name `protocols/` holds **methodology** in the hub, **project domain** in ai-council, and is **absent** in corp. **Disposition DEFER(reason)** — decide whether `protocols/` is a methodology-mandated genre (and if so, disambiguate the name from ai-council's domain use) before any mechanism. Open-Q (b). **[AMENDED 2026-07-11 → RULED: `protocols/` IS a methodology-mandated genre fleet-wide, with the universal boundary applied inside it (methodology = hub-pointer, project docs = local + marked). Tracked #314 — see Amendment.]**

### Surface 6 — .code-workspace → METHODOLOGY-GENERIC
- All three carry a dot-prefixed `.{repo}.code-workspace` with a shared pattern: `.venv` interpreter, pytest enabled, **Ruff as sole `[python]` formatter + formatOnSave + fixAll/organizeImports**, the **ADR-59 explorer sort** (`upper`/reverse), errorLens, todo-tree, gitlens. corp's is annotated **"copied verbatim from corrected `.dev-knowledge.code-workspace`"**. _(Explore scans + hub `.dev-knowledge.code-workspace`.)_
- Project deltas are sanctioned: folder name; pytest args (ai-council `-m "not integration and not envcheck"`, corp `-x --tb=short`); rulers (ai-council `[88,120]` vs corp `[120]`); corp adds `launch`/`tasks` + more extensions + `unwantedRecommendations`. **Disposition METHODOLOGY-GENERIC** — a shared ADR-59 visual + tool template with project-local deltas; open-Q (g).

### Surface 7 — cache-folder policy → METHODOLOGY-GENERIC (policy uniform)
- All three `.gitignore` the standard three caches (`.ruff_cache/`, `.pytest_cache/`, `.mypy_cache/`). _(hub `.gitignore` L4–6; ai-council L7–9; corp L6–8, all quoted by the scans.)_
- **Cache *presence* reflects PROJECT toolchain, not a policy divergence:** hub `.pytest_cache`+`.ruff_cache`; ai-council additionally `.mypy_cache` (runs **mypy**); corp additionally `.hypothesis` (runs **Hypothesis**). **Disposition METHODOLOGY-GENERIC** for the gitignore policy; the toolchain deltas (mypy vs hypothesis vs neither) are a **PROJECT-SPECIFIC programming-style signal** (open-Q g) — worth noting but not a boundary defect.

### Surface 8 — INSTALL.md → DEFER (open-Q f)
- **ai-council:** PRESENT — install/setup guide for the **`tier1-lifecycle` plugin** (the ADR-70 propose-closures Stop hook, `/review-closures`, the portable ruff gate). **Methodology-plugin content**, not a project bootstrap README. _(Explore: `INSTALL.md`, 2629 bytes.)_
- **hub:** ABSENT at root (the plugin's own `plugins/tier1-lifecycle/INSTALL.md` exists, but no root INSTALL.md).
- **corp:** ABSENT.
- **Boundary:** the content is **methodology-generic** (plugin install), but placement is **non-uniform** — only the repo that co-authored the plugin carries a root copy. **Disposition DEFER(reason)** — decide standardize-fleet-wide (a deploy-carried INSTALL for onboarded repos) vs accept ai-council-local. Open-Q (f). **[AMENDED 2026-07-11 → RULED: `INSTALL.md` uniform fleet-wide, hub-owned, deploy-carried. Tracked #315 — see Amendment.]**

### Surface 9 — .claude/ contents → DEFECT (under-specified boundary)
- **commands/:** hub = `changelog-review`, `handoff`, `override`, `save` (4); **ai-council = `override` only; corp = `override` only.** So `/handoff` + `/save` (methodology-generic session commands) **do not reach consumers**. `/codex-review` is **user-level** (`~/.claude/commands/`, all repos) — absent repo-level everywhere; `/code-review` is a **built-in skill**, not a repo command anywhere. So the "codex-review vs code-review documentation" coverage is: neither is a repo-level command in any repo; both are documented only in the hub CLAUDE.md §7 pointer.
- **skills/:** hub = `check-against-spec`, `verify` (+ user-level `gotchas`); **corp = `gotchas/` (SKILL.md + gotchas.md) in-repo**; **ai-council = none (no `.claude/skills/` dir at all; it has `.claude/rules/` instead — census brief L245)**. Gotchas universalization is therefore **half-adopted** — filed **#308** (and Phase 5 of the naming/gotchas census, L244–246).
- **workflows/:** hub `conformance-hub.js`; corp `conformance-corp.js`; ai-council none. **rules/:** hub `git-discipline`; ai-council `code-standards`/`python-env`/`testing`; corp none. **worktrees/:** hub present; corp present (**`cm-deep-vault/` — a live worktree**); ai-council absent. **agents/:** hub `artifact-reader` only. Common to all: `override.md`, `CLAUDE-FLOOR.md`(+`.sha256`), `check_floor_hash.py`, `settings.json`.
- **Boundary:** `.claude/` is **the least-specified surface** — command set, skills, workflows, and rules each diverge, with only the floor + `override` + settings common. **Disposition DEFECT** — the `.claude/` methodology surface needs an explicit hub-owned spec (which of commands/skills/workflows/rules are methodology-carried vs project-local). Open-Q (e); ties to #308 (skill home) and the ORGAN-INDEX generator #132.

### Surface 10 — CI/CD currency → PROJECT-SPECIFIC
- **hub:** **no `.github/`** — quality gating is pre-commit + local `audit.py` + the cloud nightly Routine (spec-orchestration via `.claude/workflows/conformance-hub.js`).
- **ai-council:** **no `.github/`** — local-only gating (`.pre-commit-config.yaml` + `scripts/check.ps1`).
- **corp:** **`.github/workflows/` present** — `nightly-conformance-triage.yml` (newest, git last-commit **2026-06-06**) + `tach.yml` (**2026-04-15**).
- **Boundary:** GitHub-Actions CI is **not methodology-mandated** — two of three repos have none by design. **Disposition PROJECT-SPECIFIC.** Currency **FLAG (routed to corp, ADR-41):** corp's newest workflow is ~5 weeks old and `tach.yml` ~3 months old as of 2026-07-11 — a corp-side currency concern, not a fleet boundary defect. Open-Q (h).

### Surface 11 — tests/ layout → DEFER (flag-only, open-Q i)
- **hub:** flat — ~60 `test_*.py` at `tests/` root + `fixtures/` + `conftest`. _(63 entries.)_
- **ai-council:** flat — ~20 `test_*.py` + `conftest.py` + `__init__.py`, single-level.
- **corp (FLAG-ONLY per contract):** **nested** — ~18 top-level subdirs (`extractor/ integration/ safety/ schema/ opportunity/ project/ rfp/ …`) + ~20 root `test_*.py` + `conftest`. No deeper analysis performed.
- **Boundary:** hub + ai-council share a **flat layout** (loosely methodology-consistent); corp's **nested layout** reflects monorepo scale. **Disposition DEFER(reason)** — corp `tests/` layout is a dedicated-session concern (flag-only per contract); no fleet ruling here. Open-Q (i).

---

## Open-questions mapping (SUPPLEMENT Q4 (a)–(j) → rows / DEFER)

Contract item 3 — each maps to ≥1 row or an explicit DEFER line:
- **(a)** where the methodology/project boundary runs, per surface → the **whole matrix**; headline row **Surface 2** (CLAUDE.md split).
- **(b)** `protocols/` as a methodology-mandated genre → **Surface 5** (DEFER).
- **(c)** ToC deprecation (carrier impact) + Mermaid successor → **DEFER(reason):** the ARCHITECTURE ToC is enforced by the deployed `toc-freshness` carrier (hub `@v1.2.0`, present in both consumers, Surface 3), so removing it is a **methodology-component deprecation**, not a doc edit; and Mermaid removal (SUPPLEMENT A2e) must land a **successor first** (coupled to #262, currently BLOCKED — corp is mapless without it). Not mechanized here; routed to the architect. _(Not one of the 11 surfaces; recorded as a closing DEFER.)_
- **(d)** the missing consolidation MECHANISM (fleet CLAUDE.md diff-routine) → **§Candidate mechanisms** (proposal C1).
- **(e)** `.claude/` full review → **Surface 9** (DEFECT).
- **(f)** `INSTALL.md` uniformity → **Surface 8** (DEFER).
- **(g)** `.code-workspace` + cache policy → **Surfaces 6 + 7** (METHODOLOGY-GENERIC; toolchain deltas noted PROJECT-SPECIFIC).
- **(h)** CI/CD currency → **Surface 10** (PROJECT-SPECIFIC + corp currency flag).
- **(i)** corp `tests/` layout → **Surface 11** (DEFER, flag-only).
- **(j)** web-research leg (better architecture/dependency-visualization libraries than the home-grown codemap set) → **DEFER(reason):** a research spike, not a boundary surface; recorded as candidate research C4 (sky-is-the-limit budget, SUPPLEMENT A6). Routed to the architect; coupled to #262/#295 (codemap generator limits) and #102 (repo-index research).

---

## Candidate mechanisms (PROPOSALS ONLY — nothing built here; contract item 7)

Carrier / gate / routine candidates that would convert the DEFECT/DEFER rows above into mechanism. **All are proposals for operator/architect ruling; none is implemented in this session.**

- **C1 — Fleet CLAUDE.md diff-routine (open-Q d; addresses Surface 2).** **[FILED 2026-07-11 as #312, DESIGN-ONLY — marker form + CLAUDE.md-first spec for operator ruling; the build is downstream. See Amendment.]** A read-only routine/generator that concatenates each repo's CLAUDE.md **methodology sections** and diffs them fleet-wide, surfacing drift continuously (the "3 months and still invisible" gap the operator named). Precondition: an **explicit, hub-owned methodology-block marker** in CLAUDE.md (e.g. a fenced `<!-- methodology-block -->…<!-- /methodology-block -->` region, or promoting §1/§6/§7/§8/§9 into a floor-imported fragment like the existing `@.claude/CLAUDE-FLOOR.md` pattern). Layer-2-safe (read-only reporter, `fleet_health.py`/audit sibling). Kin to the ORGAN-INDEX generator (#132).
- **C2 — Commit-msg + pre-push enforcement carriers (Surface 3).** Already filed **#302** (pre-push `block-ff-push` carrier) + **#309** (commit-msg `backlog-id-on-close`/`filing-backpressure`, portable subset) via the deploy manifest — this audit is the witnessed evidence they are armed-but-empty in both consumers; no new filing needed, recommend prioritizing.
- **C3 — `.claude/` surface spec + skill-home ruling (Surface 9).** An explicit hub-owned statement of which `.claude/` members are methodology-carried (commands `/handoff`/`/save`; skills `verify`/`gotchas`) vs project-local, feeding a carrier. Ties to **#308** (verify-skill home) and the **#132** ORGAN-INDEX generator.
- **C4 — Architecture/dependency-visualization research spike (open-Q j).** Evaluate current libraries for file→file / file→code / code→code visualization vs the home-grown codemap (coupled to #262/#295, #102). Research-only; sky-is-the-limit budget (SUPPLEMENT A6).
- **C5 — ADR-101 refusal-gate + audit-filename rename (naming census / R4).** The unbuilt **#306** `validate_hermetization.py` would prospectively enforce the R4 casing rule that fixes corp's UPPERCASE `_AUDIT_`/`_BRIEF_` divergence — the census judged it **actively growing precisely because corp's `docs/audits/` has no README and no gate**, while ai-council's README-enforced discipline holds the line (census brief L183, L236). Also: rename *this* file to `2026-07-11-technical-fleet-boundary-matrix.md` for ADR-101 conformance (see filename note).

---

## Scope / method / UNVERIFIED

- **Read-only, evidence-cited.** dev-knowledge column = main-thread `ls`/`grep`/`cat` sweep; ai-council + corp columns = two read-only `Explore` subagents (cannot Edit/Write). No mutation of any repo occurred; the only writes are this file + its commit on `docs/audit-fleet-boundary-matrix` (contract item 6).
- **corp `tests/`** was flag-only by contract — its nested shape is noted, not analyzed.
- **UNVERIFIED / flagged:** corp's two absences (commit-msg/pre-push gates) are cited from the corp QA scorecard *and* re-witnessed here via `.pre-commit-config.yaml`; the `.methodology.yaml` present-in-corp / absent-in-ai-council asymmetry is noted but its deploy-manifest cause (per-consumer prune scoping, #276/#245) was not traced this pass. Line-level citations into the 2026-07-11 census brief (Phase 4/5) are by-section; exact line numbers can be added if required.
- **No aggregate verdict** is stated anywhere (contract item 5); each surface disposition stands alone.

---

## Amendment — operator rulings on the DEFER dispositions (2026-07-11)

> **In-file amendment marker (CLAUDE.md §5 item 3 / ADR-94 pattern).** The matrix + dispositions above are preserved verbatim as authored at audit time; this section records the operator's subsequent rulings on the two DEFER rows and the C1/C5 filings. Audits are immutable — the original DEFER findings stand as the audit-time record; these rulings supersede them going forward. Filed BACKLOG ids: **#312, #313, #314, #315**.

- **Surface 5 (`protocols/` genre): DEFER → RULED.** `protocols/` is a **methodology-mandated genre, fleet-wide** — every onboarded repo carries it. Contents split by the standard boundary: **methodology protocols = hub-pointer (never copied)**; **project protocol docs (corp per-package interfaces, ai-council Council domain) = local + marked**. The universal boundary applies *inside* the one mandated genre. **Rationale:** the same folder name held two genres (hub = methodology-authoring, ai-council = project domain, corp = absent); the operator ruled one mandated genre with the boundary applied within, over leaving it ambiguous. Reversible. Tracked **#314**.
- **Surface 8 (`INSTALL.md`): DEFER → RULED.** `INSTALL.md` is **uniform fleet-wide, hub-owned, deploy-carried** — the tier1-plugin-install content becomes a hub-canonical, deploy-manifest-carried file in every onboarded repo. **Rationale:** the content is methodology-generic (tier1 plugin install) but its placement was accidental — only the co-authoring repo (ai-council) carried a root copy; the operator ruled uniform-everywhere over accept-local. Reversible. Tracked **#315**.
- **C1 (fleet methodology-boundary marker + CLAUDE.md diff-routine):** filed **design-only** as **#312**. Governing principle (operator): the hub is the ROOT of a decision tree that traverses repo-by-repo and must classify every surface **methodology vs application without searching** — the boundary must be machine-readable. Scope: choose the marker form (fenced methodology-block region vs floor-import promotion of §1/§6/§7/§8/§9), define it for CLAUDE.md first, assess extension to root files. The **build is a downstream task gated on this design**.
- **C5 (ADR-101 filename conformance):** the rename to `2026-07-11-technical-fleet-boundary-matrix.md` is filed as **#313**.

The Surface 5 and Surface 8 rows above are no longer open DEFERs (RULED as recorded here); every other row's disposition (DEFECT / DEFER / METHODOLOGY-GENERIC / PROJECT-SPECIFIC) is unchanged. No mechanism was built and no file renamed in this filing session — capture only.
