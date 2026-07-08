---
kind: hygiene-audit
generated: 2026-07-09
owner: Rob
status: complete
run: night (unattended, auto) — Opus orchestrator + 6 Sonnet read-only subagents
head_commit_at_start: 1545c0d
---

# Night hygiene audit — docs corpus lifecycle + BACKLOG coherence (hub + ai-council mirror)

> **Unattended night run.** Opus orchestrated; six **Sonnet** subagents fanned out
> READ-ONLY, one per corpus; every git mutation ran serially in the main thread under a
> 90 s timeout. Per the autonomy contract, this run COMMITS only four classes (report,
> named BACKLOG filings, the next handoff bundle, JOURNAL); **everything else below is a
> PROPOSAL** for the morning — nothing was deleted, renamed, moved, or fixed in a
> consumer. The report **analyses** (trends + root cause), it does not merely list — the
> operator's standing critique of night output.

## Method & honesty

- Corpora: `docs/intake` (S1), `docs/decisions` (S2), `docs/audits` (S3), `docs/handoffs`
  (S4), `BACKLOG↔corpus` (S5), **ai-council** read-only mirror (S6).
- Subagents returned structured findings; the orchestrator synthesised. The **headline
  hygiene finding (S4 fill-leak)** was **independently re-verified** by the orchestrator
  from live disk (`grep -rl '(fill:'`), not taken on the subagent's word.
- Disposition tags: **FIXED** = committed this run (report + regenerated audit index only);
  **PROPOSAL** = routed to the morning briefing; **FILED:#id** = already tracked;
  **ai-council PROPOSAL** = routed to the ai-council chat (ADR-41), never a hub write.

## Phase 0 — preflight + branch disposition

- Hub + ai-council: on `main`, clean, `HEAD == origin` at run start (`1545c0d` / `7b15e7f`).
  WMI sane (`platform.machine()` → `AMD64`, 832 ms; G9 dormant, consistent with the
  2026-07-08 lived-QA precondition). Hooks armed (`hooks_armed [OK]`, `core.hooksPath`
  unset). Baseline `audit.py health: OK`, `validate_backlog: OK`.
- **`automation/fleet-audit` disposition (PROPOSAL — do NOT touch):** orphan data-branch
  (no merge-base with `main`; root `333ae85` 2026-06-15), 78 auto-commits
  `chore(routine/fleet-audit): record <date> baseline`, never merged (by design). Already
  ruled **KEEP** (#254, architect 2026-07-05). **Fresh sub-finding:** the branch's local
  tip (`d74d88c`, 2026-07-09) is **ahead of `origin`** (`3fa7cc2`, a 2026-07-08 baseline)
  by ≥3 unpushed baselines — the routine has **no auto-push**, so `origin` silently lags
  until a manual push (the morning-ops 2026-07-09 arc pushed it, then the routine advanced
  again the same night). This is #254 part-(b)'s durability concern **recurring, not
  closed**; #254 part-(a) organ-map declaration also still open. → morning proposal:
  (i) push the lagging baselines, (ii) either give the routine an auto-push step or accept
  the manual-catch-up cadence in the #254(a) organ-map entry.

---

## Per-corpus findings

### S1 — docs/intake (9 docs: ids 1–9, sequential; 3 CONSUMED, 6 SEED; naming 9/9 conform)

| # | Sev | Disp | Finding | Evidence | Root cause / analysis |
|---|---|---|---|---|---|
| S1-1 | med | PROPOSAL | No mechanical staleness/rot detection for intake SEEDs vs the README §7 ~1-month survival metric | `scripts/audit.py` (0 "intake" matches); #270 load-gauge unbuilt | The two candidate enforcement points — an `audit.py` check or the #270 SessionStart load-gauge — **both** cover intake zero today. **Compounded**: the 2026-07-08 leg-c groom DELETED 7 tasks (#16/#17/#109/#129/#70/#96/#264) and folded their scope into intake docs #6/#7/#9, so **4 of 6 open SEEDs are now the SOLE surviving record** of that scope. Nothing breached yet (oldest SEED ~3 days) but the 30-day backstop is entirely absent → a rotted SEED = silent, irreversible scope loss, not a missed reminder. |
| S1-2 | low | PROPOSAL | 2 CONSUMED docs carry a stale in-body `Status:` line contradicting their (correct) frontmatter | `2026-07-06-functional-architect-nightly-loop.md:9` + `2026-07-06-platform-feature-scan.md:9` vs each `:3` `status: CONSUMED` | Both predate the finalised 8-section template; the old freeform header line was never retrofitted when disposition changed. Cosmetic (`gen_handoff._intake_index()` parses frontmatter, not this line) but misleads a human skimming the body. |

**S1 trends:** SEED→CONSUMED was fast for ids 1–3 (same-session operator/technical triage) but there is **zero age-based backstop** — the survival metric exists on paper only. The leg-c fold was a **step-change** (4 new SEEDs in one batch) the prior per-doc cadence hasn't been tested against. **No doc has ever passed through DRAFT / READY-FOR-TECHNICAL** — every SEED→CONSUMED skipped straight from a raw drop to technical disposition; the functional-architect elaboration step (the very reason the role was proposed) is **unwitnessed** for all 6 open SEEDs.

### S2 — docs/decisions (ADR-27..100; 73 unique numbers, 75 files [2 amendment-file pairs]; only gap ADR-44 reserved+documented; README index clean)

| # | Sev | Disp | Finding | Evidence | Root cause / analysis |
|---|---|---|---|---|---|
| S2-1 | low | FILED:#242 | ADR-82 is a **third** frozen-`Proposed`-header instance (Pattern A) beyond ADR-88/89 | `ADR-82:3` `Status: Proposed` vs its own L11–15 "canonical by operator waiver"; README narrates it accepted | #242 was scoped against 2 known instances; live count is **3** (82/88/89). Same root cause (freeze header, reconcile via in-file marker). Sharpens #242's fixture set. |
| S2-2 | med | PROPOSAL (verify-then-fix) | `docs/decisions/README.md` one-liner for **ADR-51** presents pre-amendment (superseded) content as current and **omits an entire amendment** | `README.md:38` "mandatory at M/L scale… graphical at M/L, text-only at S" vs `ADR-51:93–115` Amendment 2026-05-23 "mandatory for **every** repo regardless of scale… no longer tier-determined" | Distinct from #242 (that's the Status field). The curated one-liner was written pre-2026-05-23 and only ever patched for the *later* amendment, never diffed against the ADR's full content when the earlier in-file amendment landed. **Consistent with the tier-system deprecation (CLAUDE.md §2, 2026-05-23)** — the README still speaks tier language. Systemic risk wherever an ADR has ≥2 amendments and the index tracks only the latest. |

**S2 trends:** relation-field integrity is **clean** — 58 unique ids across `Amends/Supersedes/Related`, **zero dangling**; the #23 validator would currently pass vacuously (nothing to catch yet). Status-drift is **not** systemic — confined to the 3 Pattern-A cases. A **third amendment pattern ("Pattern C": in-file dated `## Amendment` sections**, ADR-38/42/51) is the one the README index lags most, because there is no separate file or header flip to prompt an index re-check — S2-2 is its first witnessed instance.

### S3 — docs/audits (207 files; index 100% accurate, `gen_audit_index.py --check` clean; dominant class codex-review ×34)

| # | Sev | Disp | Finding | Evidence | Root cause / analysis |
|---|---|---|---|---|---|
| S3-1 | low | PROPOSAL (no-op recommended) | 3 slugs carry embedded literal dots | `2026-05-23-.dev-knowledge-audit.md`, 2× `2026-05-29-handoff-v3.4-*.md` | The `.` is a **meaningful** repo-name / version token; the outer `<date>-<slug>` shape holds. A rename would be lossy — recommend **keep as-is**, add a charset carve-out only if #300 tooling ever regexes slug internals. |
| S3-2 | med | PROPOSAL (d.iii input) | Class-token **position** is inconsistent corpus-wide | ~41 files put class after the date; ~130 bury it at slug-end or omit it | The corpus grew slug-first (repo/topic), class-suffix-second; #300 d.iii's `<date>-<class>-<slug>` **inverts** that → retroactive compliance would rename ~65% of the corpus. |
| S3-3 | med | PROPOSAL (d.iii input) | ≥3 files have **no** class token in the filename at all | `2026-05-20-handoff-process.md`, `2026-06-26-corpus-graph-justify-or-retire.md`, `2026-04-21-dev-knowledge-scope-tagging.md`; `2026-05-29-harness-engineering-positioning.md` may be scope-mismatched for `docs/audits/` | A regex validator can't classify these without opening the file — the true worst case for a strict grammar. |
| S3-4 | low | informational (as-designed) | Filename date = **content/session** date, not git-add date (~15–19% show a 1–15-day lag) | `2026-03-30-dev-practice-os-state-audit.md` (git-added 2026-04-14, header says 03-30) | Intentional content-date convention. **Any future "misdated" detector must diff the content-header date, never `git log`**, or it false-positives at scale. |
| S3-5 | low | PROPOSAL | 31 recurring-report files (ecosystem-audit ×16, conformance-digest ×10, changelog-review ×5) are already `<date>-<class>` compliant | identical slug, date-only differs | The cleanest precedent for d.iii's canonical CLASS enum. |

**d.iii input (for the #300 ruling):** **41 already-compliant** (codex-* 34, fresh-eyes 4, draft-tier 2, census-amendment 1) · **31 trivially compliant** (whole slug IS the class) · **~130 violating** (subject-before-class: `-audit`, `-discovery`, `-verification`, `-execution-plan`, `-audit-refresh`, `-retrofit-plan`, `-inventory`, `-census`…) · **4 class-less** (S3-3). **Retroactive enforcement is impractical (~65% renamed)** → the honest ruling shape is **prospective-only + grandfather existing**, and d.iii needs a **canonical CLASS enum**, not just a position rule, or proliferation continues under the new grammar.

**S3 trends:** class proliferation is real but **shallow** — one-off audits invent a bespoke trailing suffix rather than reuse a controlled vocabulary. codex-review (16%) is the only large family already matching d.iii's ordering — the natural anchor. Index mechanism is **healthy** (207/207 both directions); nothing here blocks #269/ADR-100.

### S4 — docs/handoffs (65 live bundles + 14 archive + 7 legacy; multiple format eras coexist at top level)

**FILL-LEAK (headline, orchestrator-verified):** exactly **one** committed bundle leaks —
`docs/handoffs/2026-07-05-dev-knowledge-architect/` — **8** `(fill:` markers
(`HANDOFF_BOOT.md`:1, `PASTE_THIS.md`:4, `RESIDUAL.md`:3). All other 64 bundles clean.
The `2026-07-09-dev-knowledge-architect` bundle is **complete** (0 leaks, SUPPLEMENT ANSWERS
+ RESIDUAL §1/§2/§4 authored) — confirmed independently.

| # | Sev | Disp | Finding | Evidence | Root cause / analysis |
|---|---|---|---|---|---|
| S4-1 | med | PROPOSAL | The 2026-07-05 architect bundle shipped **fully cold** and sat untouched through 4 later architect sessions | single commit `53cfefa` "FIRST live gen_handoff.py adoption [#164]", no follow-up | It was the **first-ever live `gen_handoff.py` run**; nothing caught that it was never completed. **n=2** of the same pattern (07-05 uncaught, 07-09 caught+fixed via `eef8769`/#292) — confirms #292's premise and that the omission is not a one-off. **Fix = backfill or accept-and-annotate; NOT a night-fix** (immutable handoff + I cannot fabricate that session's retrospective). |
| S4-2 | low | PROPOSAL | BACKLOG **#292's own evidence text is now stale** | `BACKLOG.md:68` cites the 2026-07-09 bundle as still leaking, but `eef8769` fixed it; #292 doesn't mention the still-broken 07-05 bundle | A concrete BACKLOG-vs-reality drift the ref-scan (S5) can't catch (it's evidence-prose, not a broken path). #292 stays validly open (gate unbuilt); only its cited example rotted. → refresh #292's evidence + point it at the 07-05 bundle when next touched. |
| S4-3 | low | PROPOSAL (awareness) | 27 superseded-era bundles (15 v3.2 + 12 v4) persist in the top-level live tree | `README.md:187–199` calls them Historical/superseded; dirs still top-level | No rule mandates archiving superseded-era bundles (and `archive/` holds a *different* artifact class here), so likely by-design — but `ls docs/handoffs/` intermixes 4 historical shapes with current v5. |

**S4 trends:** fill-omission is **n=2 (~8% of the ~25 v5-architect bundles, 50% catch rate)** → supports building the #292 gate over manual catch; **early-adoption bundles are the highest-risk cohort**. Committed-ephemeral bundles (3 epic + 1 functional, all leak-free) are orthogonal to the fill-leak gate and already tracked as #300 d.ii — do not conflate.

### S5 — BACKLOG↔corpus (~120 refs checked; 0 broken; 0 state-contradictions)

| # | Sev | Disp | Finding | Evidence | Root cause / analysis |
|---|---|---|---|---|---|
| S5-1 | low | PROPOSAL | #181 `refs` cites "SUPPLEMENT-B" — an informal shorthand, no stat-able path | `BACKLOG.md:54` | 21 dated `SUPPLEMENT.md` exist, none disambiguated. Harmless today; rots silently once the filing session's memory fades. → convention note: cite the dated bundle path + section. |

**S5 trends:** **zero ref-rot** — every concrete `refs <path>` (~90 paths + ~30 ADR ids) resolves; this BACKLOG is unusually well-maintained referentially. Future-tense "Done when: X created" targets correctly absent (pre-build state, not drift). Closure hygiene sound (#164/#255/#284/#286/#291 all closed and left the file; residual mentions are historical pointers, never live "still-needs-doing"). The one weak spot is citation **precision** (S5-1), not existence.

### S6 — ai-council mirror (all findings route to the ai-council chat as PROPOSALS, ADR-41)

| # | Sev | Disp | Finding | Evidence |
|---|---|---|---|---|
| S6-1 | low | ai-council PROPOSAL | `docs/intake/README.md` Contents omits `2026-07-08-runbook-gap-notes.md` | index vs `ls docs/intake/` |
| S6-2 | low | ai-council PROPOSAL | `docs/audits/README.md` "Convention" says `_`-separator; all 22 files use `-` (ADR-34) | README vs listing |
| S6-3 | low | ai-council PROPOSAL | Orphaned empty `.claude/worktrees/` dir (JOURNAL surfaced `fable-audit` removal; empty parent remains) | `.claude/worktrees/` vs `git worktree list` |
| S6-4 | low | ai-council PROPOSAL | Cosmetic date-in-slug redundancy `2026-05-12-codex-scrum-master-review-2026-05-12.md` | filename |

**S6 trend (hub-relevant):** the hub BACKLOG footer's **"ai-council-residuals" pointer appears already RESOLVED in-repo** (per ai-council JOURNAL 2026-07-06: `settings.local.json` is now generic; `.pre-commit-config.yaml` pins the hub hooks by URL+rev `v1.2.0`) → a **hub-side reconciliation** of that footer pointer is warranted rather than a repeat of the residuals item. ai-council's Wave-1 pass already self-swept most debt into #294–297; these are small residue just outside that scope.

---

## Cross-cutting analysis (root causes, not a listing)

1. **The corpus is referentially clean but has no age-based backstop anywhere.** S5 found zero ref-rot and S3's index is 100% fresh — the *mechanical* freshness gates (audit-index, roster, claude-rosters, codemap, TOC, canonical_freshness) are doing their job. The gap is uniformly **temporal**: nothing measures *staleness-by-age* for intake SEEDs (S1-1), cold handoff bundles (S4-1), or index-summary drift after a *second* amendment (S2-2). Every freshness organ here is **edit-triggered** (regen-and-diff on a file change); none is **clock-triggered**. This is the single structural theme — and it is exactly what #270 (load-gauge) + #271 (nightly loop) are chartered to close, plus an intake-age signal that neither yet covers.

2. **First-live-adoption artifacts are the highest-risk cohort.** The one leaking bundle (S4) and the one place the pipeline skipped its own DRAFT rung (S1 trend) are both **first runs of a new mechanism** (first `gen_handoff.py` bundle; first intake docs). New machinery ships before its own completion discipline is habitual. #292 (fill-gate) is the right teeth; the general lesson is that a new generator should ship **with** its completeness gate, not gate-later.

3. **Index summaries lag in-file amendments — a "Pattern C" blind spot.** S2-2 is not status-drift (#242's target) but *content* drift: a curated one-liner that tracked only the latest of an ADR's ≥2 amendments. There is no organ that reconciles README editorial summaries against ADR in-file `## Amendment` sections. Low volume today (1 witnessed), but it is the decision-corpus analog of the intake in-body `Status:` drift (S1-2) — **hand-authored summaries drift from the source they summarise whenever the source changes twice.**

4. **The #300 d.iii audit-class grammar is decidable now, and the honest answer is prospective-only.** S3 quantified it: 41 already-compliant + 31 trivially-compliant vs ~130 subject-before-class + 4 class-less. Retroactive rename touches ~65% of the corpus and buys little (the index already disambiguates by date). The high-value half of d.iii is not the position rule but a **canonical CLASS enum** (codex-review / ecosystem-audit / conformance-digest / verification / census / incident-evidence / …) that stops bespoke-suffix proliferation going forward.

5. **Self-critique held.** The pipeline's own meta-doctrine works where exercised (ADR-98 §5's advisory→WARN n=2 trigger fired and was actioned as #279/`check_backlog_filing.py`). The failures found are all at the **edges the doctrine hasn't reached yet** (SEED-age, cold-bundle, second-amendment summary) — not doctrine being ignored.

---

## Disposition ledger

**FIXED this run (committed):** this report + the regenerated `docs/audits/README.md` index. **Nothing else** — no deletions, renames, moves, or consumer writes (autonomy contract).

**Named BACKLOG filings this run (Phase 1, separate arc `5fdd074`):** #301 session-plan artifact class (PLAN.md); #302 branch-protection parity (ai-council lived-QA F1).

**PROPOSALS for the morning (numbered queue in the briefing):** fleet-audit push + #254 legs; S1-1 intake-SEED age signal (peg #270/#271); S1-2 stale intake `Status:` lines; S2-2 ADR-51 README one-liner (verify-then-fix); S3 d.iii input (prospective-only + CLASS enum) for #300; S4-1 the 2026-07-05 cold bundle (backfill-or-annotate); S4-2 refresh #292 evidence text; S5-1 #181 SUPPLEMENT-B citation; hub-side reconcile the resolved ai-council-residuals footer pointer.

**FILED (already tracked):** S2-1 sharpens #242 (3rd Pattern-A instance); S4-3 archiving is #300 d.ii-adjacent; d.iii → #300; intake age → #270/#271.

**ai-council PROPOSALS (route to the ai-council chat, ADR-41):** S6-1..S6-4 + F2 auto-arm fix (`pip install -e ".[dev]"` into the ai-council `.venv`).

## Verification note

Independently orchestrator-verified from live disk: the S4 fill-leak set (exactly the
2026-07-05 bundle, 8 markers) and the 2026-07-09 bundle's completeness (0 leaks). All other
findings are Sonnet-subagent-reported with cited evidence paths/lines; each PROPOSAL above
is marked verify-then-fix where a content edit would follow. No finding was acted on beyond
this report + its index regen.
