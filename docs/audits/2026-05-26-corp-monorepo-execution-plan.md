---
type: execution-plan
scope: corp-monorepo universalization actions for dedicated corp-monorepo session
date: 2026-05-26
basis: 2026-05-26-corp-monorepo-audit-refresh.md
status: research artifact (consumed by separate corp-monorepo session)
contract: this plan does NOT execute changes; consumed by corp-monorepo session per Layer-2 invariant
---

# corp-monorepo Universalization Execution Plan — 2026-05-26

This plan closes the 17 findings in
`2026-05-26-corp-monorepo-audit-refresh.md`. It is **consumed by a separate
corp-monorepo Claude Code session** with write access to corp-monorepo; the
`.dev-knowledge` session that produced this plan does not. Every action cites
the finding(s) it closes. No action invents a requirement not in the refresh.

Finding IDs (CM-CF*, CM-D*) are defined in the audit refresh — read it first.

## Sequencing principle

Ordered by: **dependencies first** (README disposition gates CM-CF7, so it is
Action 1); **the one big artifact first** (ARCHITECTURE.md re-home is the
dominant gap — Action 2 — and the codemap step depends on it); **frontmatter /
prose residue batched**; **low-effort doc/config polish last**. corp-monorepo
is the largest of the four child repos and benefits most from lessons carried
forward from the smaller ones (see synthesis).

## Pre-flight requirements (must hold before executing this plan)

- corp-monorepo working tree **clean**, on a feature branch off `main` (corp
  CLAUDE.md §4 forbids committing to `main` directly), HEAD `f418c78` or later —
  if corp has moved, re-verify the refresh's `file:line` citations first (they
  were captured at `f418c78`).
- The corp-monorepo session has read, from `.dev-knowledge`:
  - `ARCHITECTURE.md` (reference: frontmatter, `[CORE]` tags, inline Mermaid
    layer model, CODEMAP block)
  - `VISION.md` (reference frontmatter: `version`/`owner`/`last_reviewed`/`status`, no tier/scale)
  - `templates/ARCHITECTURE-template.md` (single canonical template; `[CORE]` convention; text-only-override note)
  - `protocols/PLAYBOOK.md` §Root hygiene (`:196`), §Root hygiene pass-2 (`:223`), §Codemap workflow, §VS Code workspace (`:414`)
  - `docs/decisions/ADR-33` amendment, `ADR-38` A5, `ADR-51` amendments, `ADR-49`, `ADR-40` deprecation
- corp-monorepo tests green at start (corp CLAUDE.md test command).
- **Operator decisions resolved** (see below) — at minimum README disposition
  (Action 1) and the VISION §Values routing question (Action 6, needs a Council
  debate per corp VISION §Edit process).

## Operator decisions captured (apply uniformly per cross-repo decisions table)

| Decision | Default | corp-monorepo application |
|---|---|---|
| README disposition | **Delete** | Action 1 — but corp's README is the most product-facing of the four; **explicitly confirm before deleting** (this is the one repo where keep-as-external is defensible). |
| Codemap maintenance | **Hand-authored Mermaid** | Action 3 — hand-author the inline codemap between CODEMAP markers; **no** generator opt-in, **no** `codemap check` pre-commit hook (corp has `tach.toml`, so a future generator opt-in would get layer colors — but that is out of scope here). |
| `.env.example` | **Remove** | Action 7 — confirm no contributor flow relies on it (corp's auth is not env-based), then `git rm`. |
| LESSONS scope-tag backfill | **Defer (optional)** | N/A — corp has no LESSONS.md (routes to `.dev-knowledge`). |
| Workspace tier-residue | **Separate `.dev-knowledge` change** | Out of scope; the `.code-workspace` dot-prefix (Action 7) is the only workspace action. |

---

## Actions (sequenced)

### Action 1 — README disposition (DELETE, pending explicit confirmation)
- **What:** Per the baked-in default, remove `corp-monorepo/README.md`. This
  closes CM-CF7 (stale `2,412` total + bad `[dev,llm]` extras group) as **moot**.
- **Where:** `corp-monorepo/README.md` (`git rm`).
- **Why:** CM-D-README [MEDIUM] (ADR-38 A5 — README deprecated, optional for
  external-audience repos only).
- **Caveat — confirm first:** corp-monorepo's README is the most product-like of
  the four child repos (module/CLI/test-count overview). If the operator wants
  corp treated as external-audience, **keep + fix** instead: `README.md:18`
  total → drop the count column or pin "counted YYYY-MM-DD"; `README.md:28`
  `".[dev,llm]"` → a real extras group (`.[dev,dedup,graph]` per CONTRIBUTING:33).
- **Verification:** `git -C corp-monorepo ls-files | grep -x README.md` returns
  nothing (delete path), or counts/extras corrected (keep path); confirm no
  "read README" instruction dangles (CLAUDE.md §1 does not require it).
- **Dependencies:** none (gates CM-CF7).
- **Commit suggestion:** `docs: delete deprecated README (ADR-38 A5)` *(or)*
  `docs: fix README test total + extras group (kept as external-facing)`.

### Action 2 — ARCHITECTURE.md template re-home + refresh
- **What:** Re-home the existing (high-quality) architecture content into the
  canonical template skeleton: (a) add YAML frontmatter (`last_reviewed`,
  `status`, `owner`); (b) rename the three CORE sections to `Purpose [CORE]`,
  `Codemap [CORE]`, `Layer Boundaries & Invariants [CORE]`; (c) tag only those
  three with `[CORE]`, leave the rest untagged; (d) insert
  `<!-- CODEMAP:START -->` / `<!-- CODEMAP:END -->` markers in §Codemap (filled
  in Action 3); (e) **refresh stale state** — update "Last updated", reflect
  ADR-30/31/53/54, VISION/BACKLOG additions, AGENTS.md retirement, current
  OneDrive-guard status. Content depth is already L-grade — this is a structural
  re-flow + currency refresh, not a rewrite.
- **Where:** `corp-monorepo/ARCHITECTURE.md` (whole file).
- **Why:** CM-CF1 [HIGH] (template form) + CM-CF3 [HIGH] (staleness). Also
  satisfies the ADR-51-universal presence requirement in *form*.
- **Verification:** frontmatter present; the three CORE sections carry `[CORE]`;
  CODEMAP markers present; "Last updated" is current; no reference to retired
  artifacts as live.
- **Dependencies:** none. **Do before Action 3** (codemap needs the markers).
- **Commit suggestion:** `docs: re-home ARCHITECTURE.md into canonical template + refresh (ADR-51)`.

### Action 3 — Codemap + layer model → inline Mermaid (hand-authored)
- **What:** (a) Between the CODEMAP markers from Action 2, hand-author an inline
  Mermaid codemap of the `src/corp/` package graph (one node per top-level
  module — `schema`, `extractor`, `ingest`, `retrieve`, `cli`, `project`, `rfp`,
  `opportunity` — with import edges and `tach.toml`-derived layer colors,
  mirroring the `.dev-knowledge` exemplar). This supersedes the hand-drawn
  `container-module.svg` as the canonical codemap (retire or keep it only as a
  curated higher-level view). (b) Convert the ASCII layer model to an inline
  Mermaid flowchart in §Layer Boundaries (`interface > orchestration > core >
  foundation`, `classDef` colors, cite Tach + `tach.toml`).
- **Where:** `corp-monorepo/ARCHITECTURE.md` §Codemap + §Layer Boundaries.
- **Why:** CM-CF2 [HIGH] (embedded-Mermaid codemap form) + CM-CF8 [LOW] (Mermaid
  layer model). `system-context.svg` + `magistrala-pipeline.svg` **stay separate**
  (they are §Diagrams complementary views, not the codemap).
- **Verification:** §Codemap is a ```` ```mermaid ```` fence between the markers
  and renders in VS Code/GitHub; §Layer Boundaries has an inline Mermaid
  flowchart; no remaining ASCII layer line.
- **Dependencies:** Action 2 (markers + template). **No generator opt-in**
  (operator decision: hand-authored).
- **Commit suggestion:** `docs: embed Mermaid codemap + layer model in ARCHITECTURE.md (ADR-51)`.

### Action 4 — VISION frontmatter: drop `tier`/`scale`
- **What:** Remove `tier: standard` and `scale: L` from `VISION.md` frontmatter.
  Keep `version`, `owner`, `status`, `last_reviewed` (bump `last_reviewed` to the
  edit date). Final key set = `version`, `owner`, `last_reviewed`, `status`.
- **Where:** `corp-monorepo/VISION.md:1-8`.
- **Why:** CM-D1 [MEDIUM] (ADR-33 amendment). (The `vision_md` check already
  PASSES — this removes residue, it does not fix a WARN.)
- **Verification:** `grep -n "tier:\|scale:" corp-monorepo/VISION.md` returns
  nothing; the four required keys remain.
- **Dependencies:** none.
- **Commit suggestion:** `docs: remove tier/scale from VISION frontmatter (ADR-33 amendment)`.

### Action 5 — CLAUDE.md: strike tier-residue prose + namespace-prefix ADRs
- **What:** (a) Edit the three tier-residue lines: `:25` "**Scale:** `L` (per …
  Project Scale Tiers)" → drop the Scale line (or a tier-free complexity note);
  `:30` "required at Scale M+, per ADR-51" → "required per ADR-51 (mandatory for
  every repo)"; `:136` "ADR-51 … (Scale M+)" → "ADR-51 … (universal)". (b) In
  §11, prefix cross-namespace ADR references ("corp ADR-27" vs "`.dev-knowledge`
  ADR-42") to resolve the namespace collision.
- **Where:** `corp-monorepo/CLAUDE.md:25,30,136` and §11.
- **Why:** CM-D2 [MEDIUM] (tier-residue) + CM-CF11 [LOW] (namespace prefixing).
- **Verification:** `grep -ni "scale\|tier" corp-monorepo/CLAUDE.md` returns no
  live tier-classification reference (past-tense §section-history mention OK); §11
  references are namespace-prefixed.
- **Dependencies:** none. (Single CLAUDE.md edit pass covers both.)
- **Commit suggestion:** `docs: strike tier-residue prose; prefix ADR namespaces in CLAUDE.md`.

### Action 6 — VISION §Values routing claim resolution (needs Council)
- **What:** Resolve the contradiction in VISION §Values ("one routing authority /
  single source of truth") vs the code-distributed routing reality. Either (a)
  consolidate routing into one canonical config/module + an ADR, or (b) amend
  §Values to describe routing as intentionally per-aspect/code-distributed.
- **Where:** `corp-monorepo/VISION.md` §Values (+ possibly `src/corp/*router*`).
- **Why:** CM-CF4 [HIGH] (aspirational-vs-actual; corp's own VISION §Lifecycle
  flags this as a drift signal).
- **Verification:** §Values describes the actual routing state (consolidated or
  explicitly distributed); no unrealized single-source-of-truth claim.
- **Dependencies:** **Independent + gated on an ai-council debate** (corp VISION
  §Edit process requires Council for a material Values change). The largest-risk
  action; can run in parallel with the rest once the debate concludes.
- **Commit suggestion:** `docs: resolve VISION routing-authority claim (Council <ref>)`.

### Action 7 — Root hygiene: `.env.example` + workspace dot-prefix + ruff consolidation
- **What:** (a) `git rm corp-monorepo/.env.example` after confirming env-var docs
  live in CLAUDE.md/VISION (corp auth is not env-based — low risk). (b)
  `git mv corp-monorepo.code-workspace .corp-monorepo.code-workspace`. (c)
  Consolidate ruff config: move the `ruff.toml` rule set into `pyproject.toml
  [tool.ruff]` as the single source (or delete the redundant `[tool.ruff]` block
  and keep `ruff.toml`) — **decide which strictness is intended first** (the
  lenient `E,F,I` currently wins via root `ruff.toml`; the stricter
  `E,F,I,W,B,UP` sits dead in pyproject). Deleting `ruff.toml` in favor of
  pyproject also moots the `.ruff.toml` dot-prefix (CM-D5).
- **Where:** root `.env.example` (rm), `corp-monorepo.code-workspace` (mv),
  `ruff.toml` + `pyproject.toml [tool.ruff]` (consolidate).
- **Why:** CM-D3 [LOW] (`.env.example`) + CM-D4 [LOW] (workspace dot-prefix) +
  CM-CF12 [LOW] (ruff duplication) + CM-D5 [LOW] (mooted by the ruff consolidation).
- **Verification:** `git -C corp-monorepo ls-files | grep -E "env.example|code-workspace|ruff.toml"`
  shows `.corp-monorepo.code-workspace`, no `.env.example`, and a single ruff
  config source; `ruff check` passes under the chosen rule set (expect new
  findings if the stricter set wins — fix or re-scope before committing).
- **Dependencies:** none. **Risk:** if the stricter ruff set becomes active,
  `ruff check` may surface real lint errors — budget for fixing them or keep the
  lenient set deliberately. Decide intended strictness before flipping.
- **Commit suggestion:** `chore: root hygiene — remove .env.example, dot-prefix workspace, single ruff config`.

### Action 8 — Low-effort doc batch
- **What:** (a) `CONTRIBUTING.md:119` ADR count "26" → actual (verify with
  `ls docs/decisions/ADR-*.md | wc -l`); `:105-114` replace the Phase-1-pending
  block with one line ("Phase 1 baseline violations resolved in Phase 2, JOURNAL
  2026-04-15; current baseline: 0"). (b) `BACKLOG.md:3-5` header → cite "ADR-41
  as relaxed by ADR-47" (or ADR-47). (c) Opportunistic `docs/archive/*` rename to
  hyphen form **only if** touching those files anyway (do not run a dedicated
  migration — CM-CF9 is opportunistic by design).
- **Where:** `CONTRIBUTING.md:119,105-114`; `BACKLOG.md:3-5`; `docs/archive/*`
  (opportunistic).
- **Why:** CM-CF6 [MEDIUM] (CONTRIBUTING) + CM-CF10 [LOW] (BACKLOG header) +
  CM-CF9 [LOW] (archive naming, opportunistic).
- **Verification:** CONTRIBUTING count matches actual; Phase-1 block replaced;
  BACKLOG header cites ADR-47.
- **Dependencies:** none.
- **Commit suggestion:** `docs: fix CONTRIBUTING counts + BACKLOG header citation`.

### CM-CF5 (INFO, no action)
The ADR-51 conformance gate the prior corp audit cited ("PARTIAL — best-possible
under the upstream gap") is **closed** (the codemap generator shipped 2026-05-22).
This is a status refresh, not a defect — corp may opt into the generator at will
(out of scope here per the hand-authored decision). No action.

---

## Verification gates (between phases)

- **After Action 2 (template re-home):** `ARCHITECTURE.md` has frontmatter + the
  three `[CORE]` sections + CODEMAP markers; corp tests still green.
- **After Action 3 (codemap):** the CODEMAP block is a `mermaid` fence and
  renders; §Layer Boundaries has inline Mermaid; no ASCII layer line remains.
- **After Actions 4–5, 7–8 (frontmatter / prose / hygiene / doc):** corp `git
  status` clean; tests green; `ruff check` clean under the chosen rule set; from
  `.dev-knowledge` `python scripts/audit.py repo corp-monorepo` → all 3 checks
  PASS (they already do — this confirms no regression).
- **Whole-plan exit:** `grep -rn "tier\|scale\|Scale M" corp-monorepo/{VISION,CLAUDE}.md`
  returns only acceptable past-tense history; `grep -c CODEMAP:START
  corp-monorepo/ARCHITECTURE.md` → 1; README resolved per Action 1.

## Risk register

- **ruff strictness flip (Action 7c).** Consolidating to the stricter
  `pyproject.toml` rule set may surface real lint errors across `src/corp/`. Decide
  intended strictness *before* flipping; if keeping lenient, delete the dead
  `[tool.ruff]` block instead. Do not let a consolidation commit also carry a
  large unreviewed lint-fix diff — split them.
- **VISION routing resolution needs Council (Action 6).** It is the highest-risk
  item and gated on an ai-council debate; do not let it block Actions 1–5, 7–8.
- **ARCHITECTURE re-home blast radius (Action 2).** The doc is mandated
  session-start reading; a botched re-home misleads every fresh agent context. Do
  the structural re-flow and the currency refresh in one reviewed PR; preserve the
  existing high-quality content verbatim where possible.
- **CLAUDE.md line drift (Action 5).** `:25/30/136` + §11 in one pass to avoid
  editing against stale line numbers.
- **README deletion vs product audience (Action 1).** Confirm the external-audience
  question before deleting — corp's README is the most product-like of the four.

## What this plan does NOT include

- **Methodology codification** (scrum-master review ADR, workspace-template
  framework fix) — `.dev-knowledge` standards work.
- **New ADRs in corp-monorepo** beyond what Action 6's routing resolution may
  require (a corp-local ADR, the operator's call).
- **Generator opt-in for the codemap** (operator decision: hand-authored).
- **Internal code-correctness work** (the corp internal deep-audit items —
  `manifest.load_status()`, MinHash wiring — are out of `.dev-knowledge`-standards
  scope).
- **Cross-repo modifications** outside corp-monorepo.
- **A proceed/no-proceed recommendation** — the operator decides after reading.

## Estimated execution scope

- **Required actions:** 8 (Action 6 gated on a Council debate). **INFO-only:** CM-CF5.
- **Estimated commits:** 8–10 (Action 2 + Action 3 are 2 commits on ARCHITECTURE;
  Action 7 bundles rm + mv + ruff but may split if the ruff flip carries lint fixes).
- **Estimated session size:** **medium–large.** The ARCHITECTURE re-home + codemap
  (Actions 2–3) is the bulk; the rest is frontmatter/prose/hygiene edits. Largest
  of the four child-repo sessions. No source-code changes except the possible
  ruff-driven lint fixes (Action 7c) and any routing consolidation (Action 6a).
- **Findings closed at completion:** 16 of 17 directly (CM-CF7 via Action 1's
  disposition; CM-D5 via Action 7's ruff consolidation; CM-CF5 is INFO). Action 6
  closes CM-CF4 once the Council debate concludes.

## Operator decisions required before execution

1. **README disposition (gates Action 1).** Delete (default) or keep-as-external
   (corp is the most product-like repo — keep+fix path documented in Action 1).
2. **VISION `status` value (Action 4).** `active` is current; confirm it stays.
3. **ruff strictness (Action 7c).** Adopt the stricter `E,F,I,W,B,UP` set (and fix
   resulting lint) or keep lenient `E,F,I` (delete the dead pyproject block)?
4. **VISION routing resolution (Action 6).** Consolidate routing vs amend §Values
   — and schedule the required ai-council debate.

## Lessons transferable to corp-ops + corp-sca-time-automation

- **The tier-residue pattern is corp-monorepo-specific among the three.** corp-ops
  and corp-sca carry **no** tier/scale (verified zero hits) — their gap is the
  *absence* of VISION/ARCHITECTURE/BACKLOG, not residue removal. Do not look for
  tier-residue to strip in those two.
- **ARCHITECTURE adoption differs by source shape.** corp-monorepo has a real
  package graph (8 modules + `tach.toml`) → a rich Mermaid codemap. corp-sca is
  flat-module → text-only override. Match the codemap form to the source.
- **README disposition is per-repo and gates the doc-quality findings** — decide
  it first.
- **Confirm ruff config source before assuming consolidation is free** — corp has
  a real strictness divergence; the smaller repos already have clean single configs
  (corp-ops in pyproject; corp-sca has none).

---

**Contract preserved:** this plan executes nothing; it is consumed by a separate
corp-monorepo session. The `.dev-knowledge` session that authored it made zero
changes to corp-monorepo and wrote only to `.dev-knowledge/docs/audits/`.
