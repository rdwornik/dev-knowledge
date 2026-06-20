---
date: 2026-06-21
status: for-operator-review
owner: Rob
scope: PROCESS layer — PLAYBOOK.md, ESSENTIALS.md, protocols/*
auditor: Claude Code (overnight; worktree `audit-process`, branch `feat/audit-process`)
source_of_truth: JOURNAL.md (+ live state where it points at counts/code)
---

# Overnight audit — PROCESS layer findings (2026-06-21)

## Headline

The process layer is **substantially current**. The pair flagged as historically drift-prone —
**PLAYBOOK §2 ↔ ESSENTIALS on the ADR-87 equilibrium contract — is aligned** (and consistent with
`HANDOFF_BOOT.md` "Architect mode" + `templates/prompt-template.md` v1.5). `HANDOFF_PROCESS.md` is
correctly **v5.2**; `DEFINITION_OF_DONE.md` correctly encodes the **ADR-85 Stop-gate** (incl. the
2026-06-19 C1 amendment + `/override`). **Zero hub-organ leakage** into the universal docs (#77
doctrine holds). Baseline `audit.py`: **health OK · ship-gate GREEN · handoff_version_stamp v5.2 ·
doc_claims match**.

| Lane | Count | Status |
|---|---|---|
| **Auto-applied** (mechanical currency) | 1 fix (2 sites) | committed `f321eda` |
| **Proposals** (judgment — your call) | 5 | this doc, §B |
| **Cross-domain flags** (not mine to fix) | 4 | this doc, §C |
| **Audit-passed** (checked, confirmed current) | 7 areas | this doc, §D |

**Merge-back owed.** Review, then merge `feat/audit-process` `--no-ff` from the **primary** checkout.
Nothing was pushed; nothing reached `main`.

---

## A. Auto-applied (mechanical, committed)

### A1 — PLAYBOOK: stale "ruff not wired" claim corrected · `f321eda`

| | |
|---|---|
| **What** | Two PLAYBOOK sites claimed ruff is "documented but **NOT wired** as a hook (BACKLOG #13)": the §7 usage-protocol hooks table (was line 1677) and the §7c hooks-examples prose (was line 1787). Both corrected to: ruff is an **Auto blocking pre-commit gate** (`ruff check`, blocks on violations), **#13 closed**. |
| **Why** | Provably stale — a wrong status that the JOURNAL/config show shipped. Squarely the auto-apply lane. |
| **Evidence** | `.pre-commit-config.yaml` L67-76 (`id: ruff`, `entry: ruff check`, "blocks on violations", version-pinned ≥0.15.5) · `CLAUDE.md` §9 (ruff gate, "added by [#13]") · `CLAUDE.md` change-history v2.7 (2026-06-02, "ruff gate wired (#13 closes)"). |
| **Risk** | None — corrects a false negative; minimal diff (2 lines); TOC + audit-health + all pre-commit gates green post-edit. |

> Note on what was deliberately **not** auto-added: the §7 table is a curated operational subset
> ("CLAUDE.md is the inventory authority"). It is missing `toc-freshness` ×2, `coherence-nudge`, and
> `block-ff-push`. I did **not** add them — `block-ff-push` is a **hub-only organ** and adding it
> would leak it into the universal doc (the exact #77 failure this audit guards against). The §7c
> prose now points at CLAUDE.md §9 for the full roster instead.

---

## B. Proposals (judgment — operator decides; NOT auto-applied)

### B1 — Reconcile the §7 review-command to the resolved **graduated rule**  ·  *priority: high*

| | |
|---|---|
| **What** | PLAYBOOK §7 usage table (line ~1651), the §"Writing prompts" pre-send checklist (line ~571), and ESSENTIALS "Ending a Session" (line 357) all name **only `/codex-review`** as the pre-merge gate. The architect resolved this to a **graduated rule**: `/code-review high` *interim/in-flight*, `/codex-review` *final pre-merge*. The docs were never updated. |
| **Why** | A surfaced, still-open doc-vs-practice gap — sessions actually used `/code-review high` while the doc said `/codex-review`. Leaving it means the doctrine and the practice keep diverging. |
| **JOURNAL evidence** | L400 (2026-06-17 supplement answers): *"the §7 review-command canon resolves to a **graduated rule** (`/code-review high` interim, `/codex-review` final pre-merge — confirm Codex auth-mode)."* · L426: *"R3 drift note: PLAYBOOK §7 … names `/codex-review` … but this feature's actual practice … used `/code-review high` — **surfaced for reconcile**, not left silent."* · L416: deferred "for a future reconcile." · L180 (recent Next): *"the §7 graduated review-command reconcile"* still listed open. |
| **Risk** | Low — additive clarification, not a removal. One open input: "confirm Codex auth-mode" (the supplement's own caveat). |
| **Recommended** | Approve a small edit across the 3 surfaces: state the two-rung rule (interim `/code-review high` → final `/codex-review`), keeping the 3-files/safety-critical threshold. I can apply on your nod. |

### B2 — SESSION_SETUP.md "Handoff workflow trigger" still documents **v4 mechanics**  ·  *priority: high*

| | |
|---|---|
| **What** | `protocols/SESSION_SETUP.md` lines 197-215 describe the **v4 two-phase interview flow** (`in-progress/{slug}/`, `_handoff-interview.md`, the `README + 01_ROLE…07_ASK_BACK` bundle) as the operative mechanics, behind a caveat: *"v4 mechanics — superseded; **retained until the v5 residual/probe generator lands**, per HANDOFF_PROCESS.md §11."* |
| **Why** | The caveat's condition is **false** — the v5.2 generator HAS landed (live `/handoff`, `assemble_paste.py`, the 4-file bundle). And the cross-ref is broken: HANDOFF_PROCESS.md §11 is now *"Promotion record (v5 → canonical)"* and contains **no** such "retained until…" language (verified — HANDOFF_PROCESS.md is clean of all v4-mechanics residue). So a reader following SESSION_SETUP gets a superseded process pointed at a non-existent justification. |
| **JOURNAL evidence** | v5.0→v5.1→v5.2 all shipped: L529 (v5.1), L542 (v5.1 bump), L560 (v5.2). Live generator dogfooded repeatedly (L396-418). |
| **Risk** | Medium — needs a small rewrite, and the "create/complete handoff" **trigger phrases** (still valid in v5) must be **preserved**. |
| **Recommended** | Replace the stale v4-mechanics body with a **thin pointer to `HANDOFF_PROCESS.md`** (the canonical source), keeping the phrase-trigger table. Preserves the rule, drops the dead mechanics. Propose-only because it's a section rewrite, not a one-token fix. |

### B3 — PLAYBOOK §"Writing prompts" (line 505) predates ADR-87  ·  *priority: medium*

| | |
|---|---|
| **What** | PLAYBOOK has **two** prompt-authoring treatments: §"Writing prompts for Claude Code" (line 505, "Standard structure (8 sections)") and "## 2. Creating a Claude Code Prompt" (line 2007, the ADR-87 `[A]`/`[CC]` split). The line-505 section frames the **architect as authoring all 8 sections** (incl. "Read first" and "Git workflow") — with no ADR-87 caveat that **CC self-loads** most of the skeleton. |
| **Why** | Directly the equilibrium-contract consistency the audit was told to check hard. §2 is correct; the older §505 is a latent drift surface that still teaches the pre-ADR-87 "architect hand-authors everything" model — internally inconsistent with §2. |
| **JOURNAL evidence** | L326 (ADR-87 codification): the skeleton is *"now CC's consumption-spec, not the architect's authoring burden."* |
| **Risk** | Low-medium. Cheapest: add an ADR-87 cross-pointer at the top of §505. Larger: consolidate §505 into §2 (heavier; pruning = propose-only per the hard invariant). |
| **Recommended** | Add a one-line ADR-87 pointer to §505 ("the architect's actual output is thinner — see §2 'Architect output vs CC consumption-spec'"). Flag the §505↔§2 overlap as a candidate consolidation for a later focused groom. |

### B4 — `max` effort tier exists in the harness but not in the effort tables  ·  *priority: medium*

| | |
|---|---|
| **What** | The Claude Code harness now exposes a **`max` effort tier** (this very audit session is running "max effort"). PLAYBOOK and ESSENTIALS effort enumerations top out at **`xhigh`** (PLAYBOOK summary table line 2030 + "How to choose Effort" line 2081; ESSENTIALS line 270/273). `templates/prompt-template.md` is even narrower (`low|medium|high`, line 16). |
| **Why** | A platform fact that postdates the methodology's last platform refresh. The PLAYBOOK "Model/effort platform doctrine" subsection was "refreshed for #84 from `docs/audits/2026-06-07-platform-max-audit.md`" (line 2086) and still treats `xhigh` as the top single-session tier — accurate as of 2026-06-07, now lagging the harness. |
| **JOURNAL evidence** | None directly (the tier emerged via tool-changelog, not a JOURNAL build entry). Witnessed: the running session's effort = "max"; harness effort enum = `low|medium|high|xhigh|max`. |
| **Risk** | Low — but it's a methodology-adoption decision (a runtime fact needs a methodology home), not a pure currency fix; hence propose, not auto-apply. |
| **Recommended** | Decide whether `max` earns a place in the effort vocabulary (and what distinguishes it from `xhigh`). If yes, I add it to the PLAYBOOK/ESSENTIALS effort tables + a one-line "when to use max vs xhigh." |

### B5 — PLAYBOOK §7b commands "Real examples" list is incomplete  ·  *priority: low*

| | |
|---|---|
| **What** | §7b (lines 1748-1751) lists only `/session-summary` and `/codex-review` as command examples. Missing the current set: `/save`, `/ship`, `/handoff`, `/review-closures`, and notably **`/override`** (the ADR-85 escape hatch) and `/verify`. (The §7 usage-protocol table above it is fuller.) |
| **Why** | Not *wrong* (framed as "Real examples"), but stale-by-omission — `/override` especially, given it's load-bearing for the ADR-85 gate. |
| **JOURNAL evidence** | `/ship`, `/override`, `/review-closures` all shipped (ADR-85 / ADR-70 / tier1-lifecycle plugin). |
| **Risk** | Low. |
| **Recommended** | Expand the §7b examples to the current command set, or convert it to a thin "see the §7 usage table / CLAUDE.md §7" pointer to avoid re-drift. |

---

## C. Cross-domain flags (NOT fixed — operator reconciles across domains)

### C1 — ENVIRONMENT.md is broadly stale (runtime/ops snapshot)

`protocols/ENVIRONMENT.md` is stamped **"Last updated: 2026-06-03"** and predates several changes.
It is a **runtime/ops** doc (every section `<!-- scope: runtime -->`), so per the audit's hard
invariant I flag rather than edit it. Concrete staleness (all witnessed):

- **Dead command refs** — lines 54-55 list `boot.md` / `evolve.md` as live `~/.claude/commands/`
  files; line 66 lists `memory/evolution-log.md`. **Verified gone:** `~/.claude/commands/` has no
  boot/evolve; `~/.claude/archive/2026-06-05-machinery-c3/` exists; no `evolution-log.md`. (Archived
  2026-06-05 Phase-C3.)
- **Evolution hooks** — lines 59-60 ("SessionStart → Evolution boot reminder", "Stop → Evolution
  scorecard reminder") reference the retired self-evolution loop.
- **Model list** — line 14 "Available models: Opus 4.8, Sonnet 4.6, Haiku 4.5" omits **Fable 5**
  (GA; see C2). Effort note mentions only `xhigh`, not `max` (see B4).
- **CC version** — line 11 "Version: 2.1.161"; the session-start changelog hook reports the live CLI
  at **2.1.183**.

**Recommendation:** a dedicated ENVIRONMENT.md refresh against live `~/.claude/` (its own session,
its own reviewer — it's ops, not process). I left it untouched to avoid half-freshening a coherent
dated snapshot.

### C2 — Fable 5 absent from the t-shirt routing doctrine (ARCHITECTURE's)

Fable 5 is **GA** but not in the routing doctrine. PLAYBOOK/ESSENTIALS **correctly do not add it**
(the changelog contract is capture/flag-only; the routing doctrine lives in `ARCHITECTURE.md`).
This is an **ARCHITECTURE-layer** decision, flagged here only for cross-domain visibility.

- **JOURNAL evidence** — L593 (2026-06-15 changelog review): *"Fable 5 now GA … but **absent from the
  t-shirt routing doctrine** (`ARCHITECTURE.md:323` = Haiku/Sonnet/Opus) — **flagged for operator +
  browser architect**."*
- **Recommendation:** architect/operator decision on whether Fable 5 earns a routing tier; then the
  ARCHITECTURE-layer audit carries it (and the PLAYBOOK "T-shirt model pins" pointer follows).

### C3 — `verify` skill description diverges from the live skill (PLAYBOOK §7 ↔ CLAUDE.md §8)

PLAYBOOK §7 (line 1661) and CLAUDE.md §8 both describe `verify` as a **user-level** *"domain
verification scripts for the ecosystem; consult/run after pytest passes."* The **live** skill is
**repo-level** (`.claude/skills/verify/SKILL.md`), runs the **pytest + ruff + git-status cadence**
(it *runs* pytest, not "consult after"), and is an explicit **hub-local pilot** (`#9` canonical-home
open).

- This spans **PLAYBOOK (process) + CLAUDE.md (governance)**, and the "right" description depends on
  the still-open `#9` (where the skill's canonical home lands), so it's a cross-domain reconcile, not
  a one-side fix. (Editing only PLAYBOOK would create a *new* PLAYBOOK↔CLAUDE divergence.)
- **JOURNAL evidence** — #104 shipped the repo-level cadence skill (2026-06-06); `#9` tracks the
  canonical home. SKILL.md line 14: *"canonical-home question deliberately open — refs #9; hub-local
  pilot."*
- **Recommendation:** reconcile both descriptions when `#9` resolves; until then, both should at
  least say what the skill *does* (the 3-line pytest/ruff/git cadence).

> **Note (no action):** ESSENTIALS "Writing a Prompt" (line 283) shows the **raw** `pytest -x
> --tb=short && ruff check && git status` rather than invoking the `verify` skill. This is **correct**
> for a *universal* doc — the verify skill is a hub-local pilot, not yet universal. Not a drift.

### C4 — PLAYBOOK §7 lists `~/.claude/` evolution hooks (runtime)

PLAYBOOK §7 hooks table lines 1670-1671 ("SessionStart evolution reminder", "Stop notify +
evolution scorecard") describe `~/.claude/settings.json` (runtime) hooks tied to the retired
evolution loop. This is **runtime config (`~/.claude/`)**, out of this repo's edit scope — flag for
verification against the live `~/.claude/settings.json` during a runtime/ops pass. (The global
CLAUDE.md still carries a Self-Evolution Protocol, so the corrections/scorecard *logging* may persist
even though the `/evolve` *command* was archived — hence verify, don't assume.)

---

## D. Audit-passed (checked end-to-end, confirmed current)

1. **ADR-87 equilibrium contract** — consistent across all four durable surfaces: PLAYBOOK §2
   ("Architect output vs CC consumption-spec", lines 2012-2020) ↔ ESSENTIALS "Writing a Prompt"
   (one-line standing rule, line 277, exactly as ADR-87 §7 prescribes) ↔ HANDOFF_BOOT "Architect
   mode" (pointer, lines 66-72) ↔ prompt-template.md v1.5 (Governance pointer field). **The
   historically drift-prone pair is aligned.**
2. **HANDOFF_PROCESS v5.2** — `Version: 5.2` (line 4), version history coherent (v5.0 bundle →
   v5.1 supplement interview → v5.2 always-generated SUPPLEMENT), 4-file bundle shape current, clean
   of all v4-mechanics residue.
3. **DEFINITION_OF_DONE = ADR-85 Stop-gate** — hard JOURNAL leg (per-session SHA anchor incl. the
   2026-06-19 C1 boundary fix), advisory BACKLOG leg, `/override` escape, 4-week scope-freeze. Canon
   matches the ADR + both amendments.
4. **`/boot` and `/evolve` retired** — zero usable-position references in PLAYBOOK/ESSENTIALS; one
   consolidated retired-machinery note (PLAYBOOK §7b line 1752). Witnessed dead in `~/.claude/`.
5. **Hub-organ omission (#77)** — **zero** occurrences of `block_ff_push` / `scan_undeclared_edges`
   / `reverse_dep_oracle` / `validate_no_ff` / the closure/undeclared-edge organ in PLAYBOOK or
   ESSENTIALS. Confirmed correctly hub-only (JOURNAL L60: *"PLAYBOOK/ESSENTIALS … correctly OMIT the
   hub edge-model organ — #77 doctrine; no currency edit"*).
6. **HANDOFF_BOOT.md / PROBES** — HANDOFF_BOOT current (v5 boot + v5.2 supplement-ANSWERS behavior +
   ADR-87 pointer + ADR-85 DoD). PROBES.md exists only as per-bundle immutable artifacts (not a
   process doc to edit); HANDOFF_PROCESS §13 describes it correctly.
7. **audit.py baseline** — `health: OK`; `ship-gate: GREEN` (8 WARN dispositioned);
   `handoff_version_stamp` = v5.2; `doc_claims` 4/4 match; `canonical_freshness` 6/6 fresh;
   `reconciled_versions` OK. AI_COUNCIL_PROCESS.md / AGENT_FRAMEWORK.md scanned — no dead refs
   (AGENT_FRAMEWORK is a clearly-labelled v0.1 stub).

---

## E. Coverage & method

- **Source of truth:** JOURNAL.md read for process-layer evidence (full-file structured extraction +
  targeted line reads at 180, 326, 396-438, 588-597); reconciled against live state (`.pre-commit-config.yaml`,
  `audit.py health/ship-gate`, `~/.claude/` filesystem, the live `verify` SKILL.md + `prompt-template.md`).
- **Files audited:** PLAYBOOK.md (3319 ln), ESSENTIALS.md (441 ln), HANDOFF_PROCESS.md (574 ln),
  DEFINITION_OF_DONE.md, HANDOFF_BOOT.md, SESSION_SETUP.md, ENVIRONMENT.md, AI_COUNCIL_PROCESS.md,
  AGENT_FRAMEWORK.md. (`protocols/archive/` not in scope.)
- **Invariants honored:** no rule removed; no folder/path created (findings doc lands in existing
  `docs/audits/`); cross-domain items flagged not fixed; one mechanical fix auto-applied + logged.
- **Branch:** `feat/audit-process` (off `main`). Commits: `f321eda` (ruff fix) + this doc + the
  JOURNAL wrap entry. **Merge-back owed to the operator** — do not `/ship` from the worktree.
