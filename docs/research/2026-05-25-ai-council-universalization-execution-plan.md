---
type: execution-plan
scope: ai-council universalization actions for dedicated ai-council session
date: 2026-05-25
basis: 2026-05-25-ai-council-universalization-audit-refresh.md
status: research artifact (consumed by separate ai-council session for implementation)
contract: this plan does NOT execute changes; consumed by ai-council session per Layer-2 invariant
---

# AI Council Universalization Execution Plan — 2026-05-25

This plan closes the 14 findings in
`2026-05-25-ai-council-universalization-audit-refresh.md`. It is **consumed by a
separate ai-council Claude Code session** that has write access to ai-council; the
`.dev-knowledge` session that produced this plan does not. Every action cites the
finding it closes. No action invents a requirement not already in the audit refresh.

Each finding ID below (AR-CF*, AR-D*) is defined in the audit refresh — read it first.

## Sequencing principle

Ordered by: **dependencies first** (the README disposition decision gates three other
actions, so it is Action 1); **structural/frontmatter before content polish**;
**low-risk edits batched into single commits** to keep the ai-council session small.
The codemap upgrade (Action 6) is sequenced last because it is the only action with a
tooling choice (generator opt-in vs hand-authored Mermaid) and the largest blast radius.
Actions 2–5 are mutually independent and may run in any order or in parallel.

## Pre-flight requirements (must hold before executing this plan)

- ai-council working tree **clean**, on `main`, HEAD `2a980ab` (or later — if ai-council
  has moved, re-verify the audit refresh's file:line citations first, since they were
  captured at `2a980ab`).
- The ai-council session has read, from `.dev-knowledge`:
  - `ARCHITECTURE.md` (reference: `[CORE]`-only tags, `scale`-free frontmatter, the
    inline Mermaid layer flowchart and generated codemap)
  - `VISION.md` (reference frontmatter: `version`/`owner`/`last_reviewed`/`status`, no tier/scale)
  - `templates/ARCHITECTURE-template.md` (single canonical template; `[CORE]` convention; text-only-override note)
  - `protocols/PLAYBOOK.md` § Root hygiene (`:196`), § Root hygiene pass-2 (`:223`), § Codemap workflow, § VS Code workspace (`:414`)
  - `docs/decisions/ADR-33` amendment, `ADR-38` amendment A5, `ADR-51` amendments, `ADR-49`, `ADR-40` deprecation note
- ai-council tests green at start: `pytest tests/ -m "not integration and not envcheck"` (per `ai-council/CLAUDE.md:35`).
- **Operator decisions resolved** (see "Operator decisions required" below) — at minimum the README disposition, because Action 1 branches on it.

---

## Actions (sequenced)

### Action 1 — README disposition decision + execution
- **What:** Decide keep-or-delete for `README.md`, then execute. If **delete**: remove `README.md`; AR-CF5/CF6/CF7 close as moot. If **keep** (external/open-source audience): fix the three README defects in the same edit — (a) `:234` test count → current collected count (`pytest --collect-only -q`) or drop the absolute number; (b) `:152` options-table synthesizer default `claude` → `gemini` (verify against `runner.py:pick_synthesizer()`); (c) `:294-298` reconcile or remove "Related repos"; and fix the `:288` "See `CLAUDE.md` for full architecture details" pointer → `ARCHITECTURE.md`.
- **Where:** `ai-council/README.md` (delete, or edit `:152,:234,:288,:294-298`).
- **Why:** AR-D5 [MEDIUM] (ADR-38 A5 — README optional/deprecated). Gates AR-CF5/CF6/CF7. Operator concern "bez readme."
- **Verification:** if deleted — `git ls-files | grep -x README.md` returns nothing; `grep -rn README ai-council/CLAUDE.md` shows no dangling "read README" instruction (CLAUDE.md §1 already omits README — confirm). If kept — the three values match repo reality (synthesizer = gemini everywhere; test count matches collection; related-repos reconciled).
- **Dependencies:** none (but blocks the closure of AR-CF5/CF6/CF7).
- **Commit suggestion:** `docs: delete deprecated README (ADR-38 A5)` **or** `docs: fix README synthesizer default, test count, related repos`.

### Action 2 — VISION frontmatter: de-tier + add `status`
- **What:** In `VISION.md` frontmatter remove `tier: M` and `scale: M`; add `status: active`; keep `version`, `owner`, `last_reviewed` (bump `last_reviewed` to the edit date). Final key set = `version`, `owner`, `last_reviewed`, `status` (matches `.dev-knowledge/VISION.md:1-6`).
- **Where:** `ai-council/VISION.md:1-7`.
- **Why:** AR-D1 [MEDIUM] (ADR-33 amendment; clears the `vision_md` WARN). Closes the BACKLOG P1 "Apply tier-deprecation to ai-council" frontmatter half.
- **Verification:** `python .dev-knowledge/scripts/audit.py repo ai-council` (run from `.dev-knowledge`, by the ai-council operator or the .dev-knowledge owner) → `vision_md` PASS; or static check: frontmatter keys == `{version, owner, last_reviewed, status}`, no `tier`/`scale`.
- **Dependencies:** none.
- **Commit suggestion:** `docs: remove tier/scale from VISION, add status (ADR-33 amendment)`.

### Action 3 — ARCHITECTURE frontmatter + section tags: de-tier
- **What:** (a) Remove `scale: M` from `ARCHITECTURE.md` frontmatter (final keys = `last_reviewed`, `status`, `owner`, matching the template). (b) Replace the seven `[L-opt]` section tags with **no tag** (keep the sections — they suit ai-council's complexity; the template tags only the three CORE sections). Do **not** delete the sections.
- **Where:** `ai-council/ARCHITECTURE.md:2` and `:99,125,136,154,170,184,202`.
- **Why:** AR-D2 [LOW] + AR-D3 [LOW] (current `templates/ARCHITECTURE-template.md` — `[CORE]`-only tags, `scale`-free frontmatter). Realizes the operator's "one maximal template, select elements by judgment" model.
- **Verification:** `grep -n "\[L-opt\]\|scale:" ai-council/ARCHITECTURE.md` returns nothing; the three CORE sections still carry `[CORE]`.
- **Dependencies:** none. (Do **before** Action 6 so the codemap pass touches a clean doc.)
- **Commit suggestion:** `docs: de-tier ARCHITECTURE frontmatter and section tags (ADR-51 template)`.

### Action 4 — CLAUDE.md: strike tier-residue prose
- **What:** Edit three lines: `:20` "**Scale:** `M` (per … Project Scale Tiers)" → drop the Scale line (or replace with a one-line complexity note that does not reference tiers); `:28` "required at Scale M+, per ADR-51" → "required per ADR-51 (mandatory for every repo)"; `:129` "ADR-51: ARCHITECTURE.md convention (Scale M+)" → "ADR-51: ARCHITECTURE.md convention (universal)".
- **Where:** `ai-council/CLAUDE.md:20,28,129`.
- **Why:** AR-D4 [MEDIUM] (ADR-40 deprecated; ADR-51 universal). This is the CLAUDE.md prose half of tier-deprecation that the BACKLOG P1 item under-specified.
- **Verification:** `grep -ni "scale\|tier" ai-council/CLAUDE.md` returns no live tier-classification reference (a historical mention in §12 section-history is acceptable if clearly past-tense).
- **Dependencies:** none.
- **Commit suggestion:** `docs: strike tier-residue prose from CLAUDE.md (tier system deprecated)`.

### Action 5 — Naming-guidance fix + ADR-08 rename
- **What:** (a) Correct `CLAUDE.md:32` `ADR-NN_topic.md` → `ADR-NN-topic.md`. (b) Correct `docs/decisions/README.md:3` "underscore naming per ADR-34" → "hyphen naming per ADR-34". (c) Rename `docs/decisions/ADR-08_research-degradation-alarm.md` → `docs/decisions/ADR-08-research-degradation-alarm.md` (use `git mv`); update the `docs/decisions/README.md` index link, the in-file reference `ADR-08…:83`, and any cross-references. Optionally close/keep the BACKLOG P2 "CI enforcement of hyphen-only separator" item in the same pass.
- **Where:** `ai-council/CLAUDE.md:32`; `ai-council/docs/decisions/README.md:3` + index link; `ai-council/docs/decisions/ADR-08_research-degradation-alarm.md` (rename) + `:83`.
- **Why:** AR-CF3 [MEDIUM] (ADR-34 universal hyphen mandate). Root-cause is the misguidance (self-propagating); the filename is its symptom.
- **Verification:** `git -C ai-council ls-files docs/decisions | grep -i "adr-08"` shows the hyphen form only; `grep -rn "ADR-NN_\|underscore naming" ai-council/` returns nothing; README index link resolves.
- **Dependencies:** none. (Touches CLAUDE.md `:32` — coordinate with Action 4 to avoid a stale-line conflict; either do both in one CLAUDE.md edit pass or apply Action 4 first.)
- **Commit suggestion:** `docs: fix ADR naming guidance to hyphen form; rename ADR-08 (ADR-34)`.

### Action 6 — ARCHITECTURE codemap: refresh note + Mermaid upgrade (+ optional layer Mermaid)
- **What:** (a) Replace the false "Open item" note (`ARCHITECTURE.md:21`) with a one-liner: the generator shipped 2026-05-22 and adoption is opt-in. (b) Upgrade the codemap between the existing `<!-- CODEMAP:START/END -->` markers to embedded Mermaid — **either** opt into the generator (`python -m .dev-knowledge.scripts.codemap.cli generate <ai-council-path> --source-root src --write`; note ai-council has no `tach.toml` → degraded mode, no layer colors, acceptable, or add `tach.toml` first) **or** hand-author inline Mermaid mirroring the `.dev-knowledge` exemplar. (c) **Optional:** convert the layer model (AR-CF2) to an inline Mermaid flowchart in the same pass.
- **Where:** `ai-council/ARCHITECTURE.md:21` (note), `:23-` (codemap block), layer section (optional).
- **Why:** AR-CF1 [MEDIUM] + AR-CF2 [LOW] (ADR-51 amendment 2026-05-22 — Mermaid is the canonical codemap form; the markers are already present, so this is a one-block swap).
- **Verification:** `ARCHITECTURE.md:21` no longer claims the spec is "undecided"; the CODEMAP block is a ```` ```mermaid ```` fence; if the generator was used, `codemap check` exits zero; the block renders in VS Code/GitHub.
- **Dependencies:** Action 3 (de-tier the doc first). If opting into the generator + freshness hook, that adds a `.pre-commit-config.yaml` entry — a per-repo commitment (ADR-51 amendment § Per-repo adoption).
- **Commit suggestion:** `docs: upgrade ARCHITECTURE codemap to Mermaid; refresh open-item note (ADR-51)`.

### Action 7 — Root hygiene: dot-prefix workspace + remove `.env.example`
- **What:** (a) `git mv ai-council.code-workspace .ai-council.code-workspace`. (b) Decide on `.env.example`: per pass-2 "do not create," remove it and ensure required env-var names are documented in `CLAUDE.md`/`VISION.md` (confirm they are before deleting — `CLAUDE.md:46` already points to the global secrets path). If a contributor genuinely relies on `.env.example`, the operator may keep it with a noted exception.
- **Where:** root `ai-council.code-workspace` (rename); root `.env.example` (remove, conditional).
- **Why:** AR-D7 [LOW] (PLAYBOOK:211 dot-prefix) + AR-D6 [LOW] (PLAYBOOK:227 no `.env.example`).
- **Verification:** `git -C ai-council ls-files | grep -E "code-workspace|env.example"` → shows `.ai-council.code-workspace`, no `.env.example` (if removed). VS Code can still "Open Workspace" on the dotted file.
- **Dependencies:** none. (Tool-config consolidation is already done — no action.)
- **Commit suggestion:** `chore: dot-prefix workspace file; remove .env.example (root hygiene)`.

### Action 8 — BACKLOG header citation
- **What:** Update `BACKLOG.md:3` `<!-- schema: ADR-41 | … -->` → cite "ADR-41 as relaxed by ADR-47" (or "ADR-47").
- **Where:** `ai-council/BACKLOG.md:3`.
- **Why:** AR-CF4 [LOW] (ADR-47 is the governing demoted schema).
- **Verification:** header references ADR-47.
- **Dependencies:** none.
- **Commit suggestion:** `docs: BACKLOG header cite ADR-47 (relaxed ADR-41 schema)`.

### Action 9 (optional) — LESSONS scope-tag backfill
- **What:** Add `[scope: X]` to each `LESSONS.md` entry's 6-field schema position (ADR-46 advisory). This is a pre-existing BACKLOG P3 (`.dev-knowledge` BACKLOG Stream B), advisory WARN only, **not** a universalization gap surfaced by this refresh.
- **Where:** `ai-council/LESSONS.md`.
- **Why:** Pre-existing ADR-46 advisory; included only so the ai-council session can batch it if convenient. **Lowest priority; safe to defer.**
- **Verification:** each entry carries a `[scope: …]` substring.
- **Dependencies:** none. Append-only file — backfilling tags edits existing entries, so it needs operator sign-off under the ADR-29 "never edit old entries" rule (the tag is metadata, not lesson content — same caveat as the `.dev-knowledge` LESSONS parenthetical item).
- **Commit suggestion:** `docs: backfill scope tags in LESSONS entries (ADR-46)`.

---

## Verification gates (between phases)

- **After Actions 1–5 + 7–8 (structural / frontmatter / hygiene):** ai-council
  `git status` clean; `pytest tests/ -m "not integration and not envcheck"` green;
  `ruff check src/ tests/` clean. From `.dev-knowledge`: `python scripts/audit.py repo
  ai-council` → `vision_md` PASS, `adr38_baseline` PASS, `claude_md` PASS (no WARN).
- **After Action 6 (codemap):** the CODEMAP block is a `mermaid` fence and renders;
  if the generator was adopted, `codemap check` exits zero and the freshness hook is wired.
- **Whole-plan exit:** `grep -rn "tier\|scale\|\[L-opt\]\|ADR-NN_" ai-council/{VISION,ARCHITECTURE,CLAUDE}.md ai-council/docs/decisions/README.md` returns only acceptable past-tense history; no governance doc carries live tier-residue.

---

## What this plan does NOT include

- **Methodology codification.** It does not create or amend the "one complex, scale-adaptive workspace template" framework (operator concern), the scrum-master review ADR, or any complexity-adaptation methodology. Those are `.dev-knowledge` standards work.
- **New ADRs in ai-council.** Universalization *applies* existing standards; it adds none.
- **`.dev-knowledge`-side template fixes.** The three `templates/workspace-{S,M,L}.code-workspace` files and PLAYBOOK §VS Code workspace still carry the tier-residue the operator flagged — that is a separate `.dev-knowledge` change, not an ai-council action.
- **Cross-repo modifications** outside ai-council.
- **Corp-monorepo equivalent work** — the next test case after AI Council.
- **A proceed/no-proceed recommendation** — the operator decides after reading.

## Estimated execution scope

- **Required actions:** 8 (Actions 1–8). **Optional:** 1 (Action 9).
- **Estimated commits:** 7–9 (Actions 5 and 7 each bundle a rename + edits; Action 6 may be 1–2 commits depending on generator-vs-hand-authored).
- **Estimated session size:** **small–medium.** Mostly frontmatter/prose edits + two `git mv` renames + one codemap upgrade. No source-code changes. One dedicated ai-council session should complete Actions 1–8; Action 6's generator opt-in is the only step that may need a follow-up if `tach.toml` is added.
- **Findings closed at completion:** all 14 (AR-CF5/6/7 close via Action 1's disposition; the rest map 1:1 or 1:n to Actions 2–8). Optional Action 9 closes the pre-existing ADR-46 advisory.

## Operator decisions required before execution

1. **README disposition (gates Action 1).** Delete (internal-only, per "bez readme") **or** keep (open-source/external audience) and fix in place? ai-council's README reads as product-facing, so this is a genuine choice, not a default.
2. **VISION `status` value (Action 2).** `active` is the expected value; confirm it is not `maintenance`/`archived`.
3. **Codemap maintenance mode (Action 6).** Generator opt-in (adds a pre-commit freshness hook + a per-repo commitment; consider adding `tach.toml` for layer colors) **vs** hand-authored inline Mermaid (no tooling commitment). Both satisfy ADR-51.
4. **`.env.example` (Action 7).** Remove per pass-2, or keep with a noted exception if a contributor relies on it.
5. **LESSONS scope-tag backfill (Action 9).** Opt in now or leave as the standing BACKLOG P3? Requires ADR-29 sign-off since it edits existing entries.

## Risk register

- **Workspace tier-residue specifics.** The operator's "tier-residue" concern is in the `.dev-knowledge` *template framework*, not in ai-council's workspace file (verified: the file carries no tier marker). The only ai-council workspace action is the dot-prefix. **Do not** attempt to "remove tier-residue" from inside `ai-council.code-workspace` — there is none.
- **Audit may have missed standards.** This refresh read the named standards end-to-end, but `.dev-knowledge` evolves continuously. The ai-council session should re-confirm the audit refresh's file:line citations against ai-council HEAD at execution time (they were captured at `2a980ab`); if ai-council has moved, re-verify before editing.
- **CLAUDE.md line-number drift (Actions 4 + 5).** Both touch CLAUDE.md (`:20/28/129` and `:32`). Apply them in one CLAUDE.md pass, or sequence Action 4 then Action 5, to avoid editing against stale line numbers.
- **Codemap generator path.** The generator lives in `.dev-knowledge/scripts/codemap/`; ai-council invokes it cross-repo with `--source-root src`. No `tach.toml` in ai-council → degraded mode (no layer colors) — acceptable, or add `tach.toml` first.
- **README deletion vs dangling pointers.** If README is deleted, confirm nothing in ai-council instructs reading it (CLAUDE.md §1 already omits it; the §Transcript-Routing `:288` pointer is inside the README itself, so it dies with the file).
- **Scrum-master codification is a parallel `.dev-knowledge` P1, not a blocker.** The BACKLOG marks "Codify scrum-master review authority pattern" P1 and "universalization-blocking" for the *authority reference* a reviewed child repo needs. This plan is the *output* of such a review; executing it does not require the ADR to exist first, but the operator may wish to land the codification ADR in `.dev-knowledge` in parallel so future rollouts (corp-monorepo) cite a formal authority. **Flagged as a dependency to be aware of, not a hard gate.**

## Lessons from this plan applicable to corp-monorepo (forward-look)

- **The standard moves faster than frozen repos.** ai-council's conformance dropped 90%→70% with zero repo changes — purely from standards advancing. corp-monorepo (last deep-audited 2026-05-23, BACKLOG confirms `adr38_baseline` PASS) will show the same tier-residue pattern in VISION/ARCHITECTURE/CLAUDE; plan for it.
- **The audit tool under-reports.** It sees file presence + 4 VISION keys + CLAUDE non-emptiness only. tier-residue, root-hygiene, README disposition, codemap form, and naming are all below its resolution. A tool-green repo can be ~70% on full standard. Budget a read-only deep pass per repo, not just an `audit.py` run.
- **Tier-residue is a three-file pattern** (VISION + ARCHITECTURE frontmatter, CLAUDE prose), plus `[L-opt]` section tags and root-hygiene. The same Action 2/3/4 shape transfers directly to corp-monorepo (corp-monorepo is tier L, so its residue letter is `L`/`scale: L` and its `[L-opt]`-equivalent tags, plus it is a code project so config-consolidation may have real work unlike ai-council).
- **README disposition is per-repo and gates the doc-quality findings** — decide it first, because it determines whether README polish items are real or moot.
- **Keep the workspace-template fix out of rollout.** Recognize it as `.dev-knowledge` standards work; rolling it into a per-repo session conflates standards-authoring with standards-applying.

---

**Contract preserved:** this plan executes nothing; it is consumed by a separate
ai-council session. The `.dev-knowledge` session that authored it made zero changes to
ai-council and wrote only to `.dev-knowledge/docs/research/`.
