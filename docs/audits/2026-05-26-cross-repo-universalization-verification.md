---
type: verification-audit
scope: cross-repo universalization execution verification
date: 2026-05-26
basis: 4 execution plans (ai-council, corp-ops, corp-sca-time-automation, corp-monorepo)
status: verification (validates Phase 1 of universalization rollout)
contract: read-only on child repos during verification; writes confined to .dev-knowledge/docs/audits/
---

# Cross-Repo Universalization Verification Report — 2026-05-26

## Method

Sequential execution of 4 universalization plans in one Claude Code session
(ai-council → corp-ops → corp-sca-time-automation → corp-monorepo), each on its
own `chore/universalization-2026-05-26` branch in its own workdir, followed by
line-by-line verification of each plan action against the actual committed
end-state. Execution dates 2026-05-27 (commits), report dated 2026-05-26 to align
with the plan/synthesis artifact series. Every status below cites commit SHAs and
`grep`/`ls`/`audit.py` evidence captured during the session. The audit tool was
re-run per repo at the end; results are embedded (the generated report files were
not committed — they bump `state.yaml`/`history` and are byproducts).

**Audit tool conformance (3 checks: `vision_md`, `adr38_baseline`, `claude_md`):**

| Repo | Pre (tool) | Post (tool) | Plan actions executed |
|---|---|---|---|
| ai-council | 2 PASS / 1 WARN | **3 PASS** | 8/8 required (Action 9 deferred per operator) |
| corp-ops | 1 PASS / 2 FAIL | **3 PASS** | 6/6 required + CHANGELOG retire (optional JOURNAL/workspace deferred) |
| corp-sca-time-automation | 1 PASS / 2 FAIL | **3 PASS** | 5/5 required + CHANGELOG retire (optional JOURNAL/workspace deferred) |
| corp-monorepo | 3 PASS (tier/scale residue) | **3 PASS** (residue stripped) | 6 of 8 (Action 6 + 7c deferred) + bonus VISION-prose residue |

All four repos were at HEAD matching their plan's pre-flight citation
(ai-council `2a980ab`, corp-ops `97c78ba`, corp-sca `d6dfb15`, corp-monorepo
`f418c78`) — so plan `file:line` citations were valid.

---

## Per-repo verification matrices

### ai-council (Pattern A — residue cleanup)

Branch `chore/universalization-2026-05-26`, 8 commits. Baseline `pytest -m "not
integration and not envcheck"` = 407 passed; post = 407 passed (zero `.py` files
changed — branch diff is markdown + workspace rename + `.env.example` deletion).

| Action | Plan spec | Actual | Status | Evidence |
|---|---|---|---|---|
| 1 | Delete README | `git rm README.md` | ✓ Clean | `505ea94`; `ls README.md` → absent; no live "read README" pointer (only `council_inbox/archive/` historical transcripts) |
| 2 | VISION frontmatter: drop tier/scale, add status, bump last_reviewed | keys = {version, owner, last_reviewed, status} | ✓ Clean | `06c2af2`; audit `vision_md` WARN→PASS |
| 3 | ARCHITECTURE: drop `scale:`, strip 7 `[L-opt]` tags | `scale:`=0, `[L-opt]`=0, `[CORE]`=3 | ✓ Clean | `1cbd732`; grep counts verified |
| 4 | CLAUDE.md strike tier prose (3 lines) | Scale line dropped; "Scale M+"→"universal" ×2 | ✓ Clean | `7548225`; `grep -ni "scale\|tier" CLAUDE.md` → none live |
| 5 | Naming fix + ADR-08 rename | CLAUDE `ADR-NN_`→`ADR-NN-`; README.md decisions-index "underscore"→"hyphen"; `git mv` ADR-08 to hyphen | ⚠ Deviation | `3466a53`; see deviation D-AC1 |
| 6 | Codemap + layer → hand-authored Mermaid; refresh open-item note | CODEMAP block now `mermaid` fence; layer Mermaid added; module table preserves responsibilities | ✓ Clean | `bd06523`; 1 CODEMAP pair, 2 mermaid fences, 0 "Open item" |
| 7 | Dot-prefix workspace; remove `.env.example` | `.ai-council.code-workspace`; `.env.example` removed (6 key names migrated to CLAUDE §5) | ✓ Clean | `1953400`; `git ls-files` shows dotted workspace, no env.example |
| 8 | BACKLOG header cite ADR-47 | `schema: ADR-41 as relaxed by ADR-47` | ✓ Clean | `071a150` |
| 9 | (optional) LESSONS scope-tag backfill | not done | Deferred | per operator decision (optional everywhere) |

**Deviation D-AC1 (Action 5):** the plan said "update the `docs/decisions/README.md`
index link" and "the in-file reference `ADR-08…:83`". In reality (a) ADR-08 was
**not present in the decisions-index table** (it lists only ADR-01–07), so there
was no index link to update — ADR-08 remains unindexed (pre-existing gap, out of
plan scope); (b) there is **no filename self-reference at `:83`** — the "ADR-08"
mentions are decision-*number* references, valid post-rename. The old underscore
filename still appears in an **immutable** dated audit
(`docs/audits/2026-05-18-codex-research-degradation-alarm.md:36`) and the
**append-only** `JOURNAL.md:49`; per ADR-29/ADR-39 these were **not** edited
(historical point-in-time records). The CLAUDE.md naming-line parenthetical was
also tightened ("7 existing kebab-case grandfathered per ADR-29" → "existing ADRs
hyphen-named per ADR-34") — within the AR-CF3 misguidance-fix intent.

### corp-ops (Pattern B — creation)

Branch `chore/universalization-2026-05-26`, 8 commits. Baseline `pytest` = 73
passed/1 skipped; post = 73 passed/1 skipped. `ruff check src/ tools/ tests/` =
All checks passed.

| Action | Plan spec | Actual | Status | Evidence |
|---|---|---|---|---|
| 1 | Create VISION.md (substantive) | 65 lines; keys {version, owner, last_reviewed, status} | ✓ Clean | `819c1ac`; audit `vision_md` FAIL→PASS |
| 2 | Create ARCHITECTURE.md w/ Mermaid codemap (real package graph) | 234 lines; 1 CODEMAP pair; 2 mermaid (codemap + layer); 3 CORE | ✓ Clean | `4c0673c` (+`0a4a42f` CLI Reference) |
| 3 | Create BACKLOG.md scaffold (ADR-47 header) | near-empty scaffold, header cites ADR-47 | ✓ Clean | `a7c0b5e` |
| 4 | Re-home CLAUDE.md into ADR-53 12-section; drop dangling `../ECOSYSTEM.md` | 12-section form; ECOSYSTEM link removed (verified absent) | ✓ Clean | `b0d8fee`; `audit claude_md` PASS |
| 5 | Delete README.md | removed after preserving run content | ⚠ Deviation | `09588db` (+`0a4a42f`); see D-CO1 |
| 6 | Remove `.env.example` | removed (note-only file; no refs) | ✓ Clean | `eb52df1` |
| 7 | CHANGELOG retire (CO-4) + optional workspace/JOURNAL | CHANGELOG removed; JOURNAL + workspace deferred | ⚠ Deviation | `117f3c1`; see D-CO2 |

**Deviation D-CO1 (Action 5):** to honor "verify destination before drop," the
README's per-tool command catalog (not present in VISION/CLAUDE) was preserved by
adding a **§CLI Reference to ARCHITECTURE.md** (`0a4a42f`, the template's optional
CLI section) before deleting README — info-preservation slightly beyond the literal
plan, which assumed CLAUDE already covered "run."

**Deviation D-CO2 (Action 7):** CO-4 (CHANGELOG retire) is required and was done.
The optional pairing — a `JOURNAL.md` and a dot-prefixed `.code-workspace` — was
**deferred** (operator-decides items; git history accepted as the record per
ADR-49). No workspace existed to dot-prefix; creating one was optional convenience.

### corp-sca-time-automation (Pattern B — creation, 2 adaptations)

Branch `chore/universalization-2026-05-26`, 6 commits. Baseline `pytest` = 69
passed/1 skipped; post = 69 passed/1 skipped. `ruff check src/` = All checks passed.

| Action | Plan spec | Actual | Status | Evidence |
|---|---|---|---|---|
| 1 | Create VISION.md | 62 lines; keys {version, owner, last_reviewed, status} | ✓ Clean | `ff7c1f3`; audit `vision_md` FAIL→PASS |
| 2 | Create ARCHITECTURE.md **text-only codemap** (flat modules); move arch content from CLAUDE | 150 lines; **0 CODEMAP markers, 0 mermaid** (text-only override); 3 CORE; data-flow + module map + invariants + priority table | ✓ Clean | `74ad0d1` |
| 3 | Create BACKLOG.md populated from "Known issues" | 7 entries traced to the 7 Known-issues items; ADR-47 header | ✓ Clean | `6fd0ac2` |
| 4 | Re-home CLAUDE.md into ADR-53; move `## Architecture`/`Known issues` out | 12-section; no embedded `## Architecture`/Known issues; dangling ECOSYSTEM link removed | ✓ Clean | `f4a42ba` |
| 5 | `.env.example` (referenced!) + README resolution | env docs migrated to CLAUDE §5; `cp .env.example .env` removed; `.env.example` + README deleted | ⚠ Deviation | `96db3fc` (+CLAUDE §5 enhancement); see D-CS1 |
| 6 | CHANGELOG retire + optional JOURNAL/workspace | CHANGELOG removed; JOURNAL + workspace deferred | ⚠ Deviation | `7d0dddc`; same rationale as D-CO2 |

**Deviation D-CS1 (Action 5):** the README carried setup steps **not** in the
plan's env-doc list — the `cscript scripts/calendar_export.vbs` export step, the
`az login` token fallback for `GRAPH_ACCESS_TOKEN`, and the `mklink` project-codes
symlink. To avoid information loss ("move, don't copy-and-leave"), CLAUDE.md §5 was
enhanced to capture all three before deleting README. The `cp .env.example .env`
instruction was removed from CLAUDE; the README:31 copy of it died with the file.
No `cp .env.example` instruction remains (2 residual "env.example" mentions are
descriptive prose / §12 history).

### corp-monorepo (Pattern A — residue cleanup, largest)

Branch `chore/universalization-2026-05-26`, 7 commits. Baseline `pytest -x
--tb=short` = green (exit 0); zero `.py` files changed (branch diff is doc/config
+ workspace rename). `tach check` = **0 violations** (All modules validated).

| Action | Plan spec | Actual | Status | Evidence |
|---|---|---|---|---|
| 1 | README disposition (DELETE per baked-in) | `git rm README.md` | ✓ Clean (operator-reversible) | `6a1ba20`; stale `2,412` total + `.[dev,llm]` extras (CM-CF7) die with file; correct install in CONTRIBUTING:33 |
| 2 | ARCHITECTURE template re-home + currency refresh | frontmatter added; 3 CORE sections renamed/tagged; CODEMAP markers; "Last updated" 2026-05-27; invariants consolidated into CORE section | ⚠ Deviation | `820ac4d`; see D-CM1 |
| 3 | Codemap + layer → inline Mermaid | CODEMAP block `mermaid` (8-module package graph); layer model Mermaid; ASCII arrow gone | ✓ Clean | `820ac4d`; 1 CODEMAP pair, 2 mermaid, 0 ASCII arrow |
| 4 | VISION frontmatter drop tier/scale | keys = {version, owner, status, last_reviewed} | ✓ Clean | `79dd01c`; audit keys no longer include tier/scale |
| 5 | CLAUDE tier prose + namespace-prefix ADRs | Scale line dropped; "Scale M+"→"universal" ×2; §11 split Local/Ecosystem, ADR-27 collision noted | ✓ Clean | `3e9e93b`; no live tier/scale (only §12 history) |
| 6 | VISION §Values routing claim resolution | **NOT done** | ❌ Deferred (gated) | Council-gated per plan + corp VISION §Edit process; see D-CM2 |
| 7 | `.env.example` rm + workspace dot-prefix + ruff consolidation | 7a `.env.example` removed; 7b `.corp-monorepo.code-workspace`; **7c ruff NOT done** | ⚠ Partial | `e5d1524`; see D-CM3 |
| 8 | CONTRIBUTING counts + BACKLOG header + archive rename | ADR count 26→30; Phase-1 block → "resolved, 0 violations (verified)"; BACKLOG header cites ADR-47; archive rename skipped | ⚠ Deviation | `562e2c2`; see D-CM4 |

**Deviation D-CM1 (Action 2 + bonus):** (a) the plan's currency refresh was done
**conservatively** — frontmatter + "Last updated" date + structural re-home — but
claims that could **not** be verified from docs alone were **not fabricated**: the
`1,972+ notes` count and the OneDrive-guard PR-completion status were left as-is
(flagged for operator; verifying needs code/runtime inspection). (b) The 7 "Key
Invariants" were **moved** from §Architecture Assessment into the renamed §Layer
Boundaries & Invariants [CORE] (template intent); the OneDrive-guards subsection
stayed in Assessment with its back-reference reworded to point at the CORE
invariant #5. (c) **Bonus cleanup (commit `498590d`):** VISION **prose** carried
live tier/scale residue (lines 30/113/116: "Scale L", "Standard tier, Scale L",
"Scale-L mandatory file set") that the plan's frontmatter-only Action 4 did **not**
cover. Per the baked-in operator decision "Tier/scale residue: **Remove residue
everywhere**," this was stripped and replaced with `.dev-knowledge`'s past-tense
"tier classification retired 2026-05-23" pattern (governance currency, not a
Vision/Scope change → no Council gate). This is the one place the session went
beyond a plan's literal action, justified by the explicit baked-in decision.

**Deviation D-CM2 (Action 6) — HARD-STOP honored:** the VISION §Values
routing-authority resolution is **Council-gated** (plan dependency + corp VISION
§Edit process requires Council for material Values changes). Per the session's
hard-stop rule ("Do NOT auto-resolve HIGH issues if plan ambiguous / requires
Council"), this action was **deferred untouched**. CM-CF4 remains open. **Follow-up:
schedule the ai-council debate** (consolidate routing vs amend §Values).

**Deviation D-CM3 (Action 7c) — operator decision:** the ruff strictness choice
(keep lenient `E,F,I` vs adopt stricter `E,F,I,W,B,UP` and fix resulting lint) is
an **operator decision not in the baked-in decisions table**. Per hard-stop
("ambiguous plan action → flag + skip + continue"), the ruff consolidation was
**deferred** — `ruff.toml` and the `pyproject.toml [tool.ruff]` block remain as-is
(functional, duplicated). CM-CF12 (duplication) and CM-D5 (`.ruff.toml` dot-prefix)
remain open, pending the strictness decision. Note: `ruff check src/` surfaces **1
pre-existing error** under the current lenient config — not introduced here (zero
`.py` changed); out of universalization scope.

**Deviation D-CM4 (Action 8):** CM-CF9 (opportunistic `docs/archive/*` hyphen
rename) was **skipped** — opportunistic by design ("only if touching those files
anyway"; no dedicated migration). The Phase-1-block rewrite asserts "0 violations"
only because `tach check` was **run and verified** (All modules validated) — not
assumed. ADR count fix grounded in `ls docs/decisions/ADR-*.md | wc -l` = 30.

---

## Cross-repo pattern analysis

### Pattern A — residue cleanup (ai-council, corp-monorepo)
- **Predicted:** tool-near-green but ~70% on full standard; work = strip
  tier/scale residue + upgrade codemap form + doc polish.
- **Actual:** confirmed. ai-council went 2P/1W → 3 PASS; corp-monorepo stayed 3
  PASS but the tool's blindness was visible — it reported PASS pre-execution while
  VISION frontmatter still carried `tier`/`scale` keys **and** VISION prose carried
  live tier residue the plan missed entirely. The tool **overstates** Pattern-A
  conformance exactly as the synthesis predicted; the deep read caught residue the
  tool and the plan's Action 4 did not.

### Pattern B — creation (corp-ops, corp-sca-time-automation)
- **Predicted:** tool-red (2 FAIL each), genuinely ~45%; work = build the
  governance scaffold from CLAUDE.md seeds, retire CHANGELOG/README.
- **Actual:** confirmed. Both went 1P/2F → 3 PASS. Substantive (not stub) files
  created: corp-ops VISION 65 / ARCH 234 / BACKLOG 12 / CLAUDE 100 lines; corp-sca
  VISION 62 / ARCH 150 / BACKLOG 53 / CLAUDE 111 lines. Codemap form matched source
  shape: **graphical Mermaid** for corp-ops (real package graph), **text-only
  override** for corp-sca (flat modules) — no empty CODEMAP markers authored.

### The recurring "verify destination before drop" cost
In **3 of 4** repos, README/`.env.example` deletion required migrating live content
first (corp-ops CLI catalog → ARCHITECTURE; corp-sca VBS/az/symlink setup → CLAUDE
§5; ai-council env-var names → CLAUDE §5). The plans under-specified this; treating
deletion as "verify destination, migrate, then drop" was necessary to avoid loss.

---

## Operator decisions verification

| Decision | Applied uniformly? | Notes |
|---|---|---|
| README delete | **Yes** (all 4) | ai-council, corp-ops, corp-sca, corp-monorepo all deleted. corp-monorepo's was the "most product-like" (plan caveat); deleted per baked-in "Delete / never override" — **operator-reversible at merge** if external-audience is desired. |
| Codemap hand-authored Mermaid | **Yes** | ai-council + corp-ops + corp-monorepo = graphical Mermaid; corp-sca = text-only override (flat layout). No generator opt-in anywhere. |
| `.env.example` remove | **Yes** (all 4) | corp-sca was the referenced exception — env docs migrated first. |
| LESSONS scope-tag defer | **Yes** | Not done anywhere (ai-council had a LESSONS.md; corp-ops/corp-sca/corp-monorepo route LESSONS elsewhere). |
| Tier/scale residue remove everywhere | **Yes** | ai-council (VISION+ARCH frontmatter, ARCH tags, CLAUDE prose); corp-monorepo (VISION frontmatter **+ prose**, CLAUDE prose). corp-ops/corp-sca carried none (confirmed zero hits). |
| CHANGELOG confirm-absent/remove | **Yes** | absent in ai-council + corp-monorepo; removed in corp-ops + corp-sca. |
| AGENTS.md confirm-absent | **Yes** | absent in all 4 (no removals needed). |
| ARCHITECTURE mandatory + Mermaid | **Yes** | present + CORE-tagged in all 4. |
| Dot-prefix workspace | **Where present** | ai-council + corp-monorepo had workspace files → dot-prefixed. corp-ops/corp-sca had none → optional add deferred. |

---

## Honest divergence report (consolidated)

1. **corp-monorepo Action 6 (VISION routing) — NOT executed** (Council-gated). CM-CF4 open.
2. **corp-monorepo Action 7c (ruff consolidation) — NOT executed** (operator strictness decision). CM-CF12 + CM-D5 open.
3. **corp-monorepo CM-CF9 (archive hyphen rename) — skipped** (opportunistic by design).
4. **corp-monorepo currency refresh — conservative**; unverifiable claims (notes count, OneDrive-guard PR status) left as-is rather than fabricated.
5. **corp-monorepo VISION prose residue — cleaned beyond plan's frontmatter-only Action 4** (per "remove residue everywhere" baked-in decision). The only intentional scope extension.
6. **README/`.env.example` content migration** (ai-council, corp-ops, corp-sca) — content preserved into CLAUDE/ARCHITECTURE before deletion (verify-destination-before-drop); slightly beyond literal plan text.
7. **ai-council ADR-08** — not in the decisions index (nothing to update); old filename retained in immutable audit + append-only JOURNAL (not edited per ADR-29/39).
8. **Optional adds deferred** — corp-ops/corp-sca JOURNAL + workspace (operator-decides).
9. **Pre-existing lint not addressed** — ai-council 17 ruff errors; corp-monorepo 1 ruff error (both pre-exist; zero `.py` changed; out of scope).

No action deleted content beyond plan specification. No `.py`/source logic changed in any repo. No automation script created in `.dev-knowledge`.

## Failed / incomplete actions

None **failed**. Two corp-monorepo actions are **intentionally incomplete** (deferred,
above): Action 6 (Council) and Action 7c (operator ruff decision). Recommended
follow-up: (a) schedule the ai-council routing debate; (b) operator decides ruff
strictness, then a follow-up session consolidates ruff config (+ closes CM-D5).

## Branches awaiting operator merge

| Repo | Branch | Commits | Tests | Recommendation |
|---|---|---|---|---|
| ai-council | chore/universalization-2026-05-26 | 8 | 407 pass | Merge |
| corp-ops | chore/universalization-2026-05-26 | 8 | 73 pass | Merge |
| corp-sca-time-automation | chore/universalization-2026-05-26 | 6 | 69 pass | Merge |
| corp-monorepo | chore/universalization-2026-05-26 | 7 | green | Merge; then schedule Action 6 (Council) + decide Action 7c (ruff) |
| .dev-knowledge | docs/cross-repo-universalization-verification-2026-05-26 | 1 (this report) | n/a | Merge |

## Conformance summary

| Repo | Pre (tool) | Post (tool) | Plan completion |
|---|---|---|---|
| ai-council | 2P/1W | 3 PASS | 8/8 required |
| corp-monorepo | 3P (residue) | 3 PASS (residue stripped) | 6/8 (Action 6 + 7c deferred) + bonus VISION prose |
| corp-ops | 1P/2F | 3 PASS | 6/6 + CHANGELOG (optional deferred) |
| corp-sca-time-automation | 1P/2F | 3 PASS | 5/5 + CHANGELOG (optional deferred) |

## Architectural contract verification

- **Layer-2 read-only on `.dev-knowledge` from child phases:** respected — each
  child repo's commits landed only in its own `.git/`; `.dev-knowledge` main was
  restored to pristine after each pre-flight/verification audit run (audit byproducts
  reverted/removed). Evidence: all 4 child repos end clean on their branch
  (`dirty=0`), each on `chore/universalization-2026-05-26`.
- **No automation script created in `.dev-knowledge`:** confirmed —
  `git diff --name-only main..HEAD -- scripts/` (verification branch) is empty. This
  session was operator-driven ad-hoc orchestration (CC switching workdirs), not a
  scripted Layer-2 orchestrator.
- **Writes confined to `.dev-knowledge/docs/audits/`:** this report is the only
  committed `.dev-knowledge` change on the verification branch.

## Next operator actions

1. Review this report.
2. Per-repo merge decisions (5 separate `git merge --no-ff` in each workdir).
   - corp-monorepo README delete is reversible here if external-audience is preferred.
3. Schedule the ai-council debate for corp-monorepo Action 6 (VISION routing).
4. Decide corp-monorepo ruff strictness (Action 7c); follow-up session consolidates ruff config + closes CM-D5.
5. Optionally: corp-ops/corp-sca JOURNAL adds; ai-council ADR-08 index entry; corp-monorepo currency-refresh items (notes count, OneDrive-guard PR status).

## What this verification does NOT cover

- Long-term consistency of the universalized state (post-merge drift).
- Audit-tool blind spots — already shown: it reported corp-monorepo 3 PASS while
  live tier residue sat in VISION frontmatter **and** prose.
- Internal code-correctness (the corp-sca Known-issues are now BACKLOG entries, not fixes).
- The deferred Council/ruff decisions (Actions 6, 7c).
- Pre-existing lint (ai-council 17, corp-monorepo 1).
