# Census consolidated — morning action brief (2026-07-11)

- **Class:** `census` (ADR-101 enum) · **Date:** 2026-07-11 (morning-delivery; run overnight 2026-07-10)
- **Source-session:** NIGHT HUB v2 consolidation run, lane `lane-n-night-consolidation`, base HEAD `47f31b5` (main spine: lane-b #300 ADR-101 ← lane-a c08ac47 A5-hygiene)
- **Status:** PROPOSAL-ONLY. Executed mutations this run were limited to: new report files in `docs/audits/`, `Status:`-line updates in `docs/intake/` (Phase 3), and the JOURNAL append. Every verdict below is a proposal for the operator; nothing was deleted, renamed, moved, ratified, or filed to BACKLOG.
- **Model:** Opus 4.8 (`claude-opus-4-8[1m]`), effort max. Web + cross-repo research fanned to read-only subagents; every claim carries a SHA / file:line / URL, or an explicit UNVERIFIED flag.

> **Brief assembly status:** Phase 1 ✓ (separate file) · Phase 2 ✓ · Phase 3 ✓ · **Phase 4 ✓** · Phase 5 _pending_ · Exec summary + Action menu + Kill-list _pending_.
> Built incrementally with a checkpoint commit per phase (Fable-flip-safe — Finding 1). Sections marked _(pending)_ are not yet authored; a partial file is expected mid-run.

---

## 1. Executive so-what

_(assembled last — Phase 6)_

---

## 2. Audit utilization trace (Phase 2)

**Inputs (full read):** `docs/audits/2026-07-09-night-hygiene-audit.md`, `…-deletion-candidates-report.md`, `…-night-verification-report.md`.

**Headline:** the three night-of-2026-07-08/09 reports are **largely already actioned** — the 2026-07-09 **morning-ops arc `e097212`** and **session-close `57ae83a`** closed most of the deletion/verification queue *before* the later night-hygiene report even ran; that report's own S1-2/S2-2/S5-1 then closed via the **A5-hygiene batch `c08ac47`**, and S3/S4-3 are addressed-in-draft by **ADR-101 (`47f31b5`, Proposed)**. Genuine OPEN residue is small and named in each table's OPEN rows. **The same backup-posture finding appears in all three reports** (night-hygiene Phase-0 ref → deletion item-2 → verification F1) — one issue, closed once by `e097212`/#291.

Verdict legend: **DONE (SHA)** · **IN-FLIGHT (#id)** · **ADDRESSED-IN-DRAFT (ADR-101, ratification-pending)** · **OPEN (act|file|kill)** · **NO-ACTION (as-designed)**.

### 2A — Night hygiene audit (`2026-07-09-night-hygiene-audit.md`)

| Finding | Orig disp | Verdict | Evidence |
|---|---|---|---|
| Phase-0 fleet-audit push + #254 legs | PROPOSAL | IN-FLIGHT #254 | part (b) `origin/automation/fleet-audit` pushed+tracks (`e097212` morning-ops leg D4; BACKLOG:185 progress line); part (a) organ-map decl **open**; night-hygiene's fresh sub-finding (routine re-lags origin post-push, no auto-push step) = #254(b) durability **recurring** |
| S1-1 intake-SEED age signal | PROPOSAL | IN-FLIGHT #270/#271 | no age-based backstop exists; pegged to the load-gauge (#270, P1) + nightly loop (#271); both unbuilt. **Highest-value open item** (a rotted SEED = silent scope loss — 4 of 6 open SEEDs are the sole surviving record of 7 groomed-away tasks) |
| S1-2 2 stale intake `Status:` lines | PROPOSAL | **DONE `c08ac47`** | both body lines now read `CONSUMED`, matching frontmatter (`2026-07-06-functional-architect-nightly-loop.md:9`, `2026-07-06-platform-feature-scan.md:9`) — live-verified |
| S2-1 ADR-82 3rd frozen-`Proposed` header | FILED:#242 | IN-FLIGHT #242 | open (BACKLOG:33); live count 3 (82/88/89) sharpens #242's fixture set |
| S2-2 ADR-51 README one-liner stale | PROPOSAL (verify-then-fix) | **DONE `c08ac47`** | `docs/decisions/README.md:38` now carries BOTH the 2026-05-23 (tier→universal) AND 2026-07-05 (LLM-first) amendments — live-verified |
| S3-1 embedded dots in 3 slugs | PROPOSAL (no-op) | ADDRESSED-IN-DRAFT | ADR-101 §2 grammar allows `.` in slug (explicit S3-1 carve-out); keep-as-is confirmed |
| S3-2 class-token position inconsistent | PROPOSAL (d.iii input) | ADDRESSED-IN-DRAFT | ADR-101 §6 d.iii — prospective-only + grandfather, **no retroactive rename** |
| S3-3 ≥4 class-less files | PROPOSAL (d.iii input) | ADDRESSED-IN-DRAFT | ADR-101 §3/§6 — gate inspects only ADDED paths; existing grandfathered |
| S3-4 filename date = content date | informational | NO-ACTION | as-designed; codified in ADR-101 §3 ("name-shape only, never date-accuracy; a misdated detector must diff the content header, never git log") |
| S3-5 31 recurring-report files already compliant | PROPOSAL | ADDRESSED-IN-DRAFT | ADR-101 §2 enum carries `ecosystem-audit`/`conformance-digest`/`changelog-review` — the compliance precedent |
| S4-1 2026-07-05 architect bundle cold | PROPOSAL (backfill-or-annotate) | **OPEN (act)** | bundle STILL leaks **8 `(fill:` markers** (HANDOFF_BOOT/PASTE_THIS/RESIDUAL — live `grep -rl` this run). Immutable handoff → **annotate as-cold, don't fabricate** the retrospective. Not a night-fix |
| S4-2 BACKLOG #292 evidence text stale | PROPOSAL | **OPEN (act)** | BACKLOG:68 still cites the *fixed* 07-09 bundle as the leak example, omits the still-leaking 07-05 bundle → refresh #292 evidence + point at 07-05 when next touched |
| S4-3 27 superseded-era bundles persist | PROPOSAL (awareness) | ADDRESSED-IN-DRAFT | ADR-101 §5 — superseded-era pre-v5 bundles **STAY** (grandfathered, by-design; `archive/` holds a different class) |
| S5-1 #181 SUPPLEMENT-B citation | PROPOSAL | **DONE `c08ac47`** | BACKLOG:54 now cites `docs/handoffs/2026-06-17-dev-knowledge-architect-2/SUPPLEMENT.md §B` (dated path + section), not the vague shorthand — live-verified |
| S6-1..S6-4 ai-council mirror | ai-council PROPOSAL | **OPEN (cross-repo)** | route to the ai-council chat (ADR-41); hub cannot write a child. Plus the S6 trend: hub-side reconcile of the now-**resolved** ai-council-residuals BACKLOG footer pointer |

### 2B — Deletion-candidates sweep (`2026-07-09-deletion-candidates-report.md`)

| Item | Orig | Verdict | Evidence |
|---|---|---|---|
| 1. Delete 3 merged-and-undeleted branches | [LOW] ratify | **DONE `e097212`** (hub) | 2 hub branches (`docs/2026-07-08-architect-handoff`, `worktree-cadence-teeth`) deleted (morning-ops "deletion-queue exec: 2 hub branches deleted"); live `git branch` confirms **absent**. demo-prep `feat/master-deck-audit` = child/ADR-41 scope, unverified from hub |
| 2. Back up 3 unbacked repos (corp-ops/corp-sca/demo-prep) | [HIGH BACK-UP] | **DONE `e097212`** | "F1 fleet backup fix — corp-ops/corp-sca/demo-prep pushed+verified 0/0"; refiled+closed as #291 |
| 3. `origin/automation/conformance-digest` dormant | [MED verify-then-delete] #255 | **DONE `57ae83a`** | session-close "#255 conformance-digest mechanism retired — workflow + remote branch deleted; surface_triage Surfacing-2 removed; orphaned parser test/fixture removed [#255]" |
| 4. `automation/fleet-audit` push-not-delete | [LOW push] #254 | **DONE (part-b) `e097212`** | pushed; organ-map decl = #254(a) IN-FLIGHT (row 2A) |
| 5. 3 zero-code-referrer modules | [UNKNOWN keep] #218 | NO-ACTION (keep) | keep-by-design confirmed (`probe_child_backlogs.py` dormant-by-design · `review_closures.py` plugin-twin · `release_lint.py` manual CLI); #218 M2/M3 boundary open but these are keeps, not removals |
| 6. v4 numbered handoff templates | [GATED] #164 | **OPEN-GATED** | #164 v5-generator FINISHED (`9e6ceb6`) but archival gated on "v5 cross-repo lands + corp migrates off v4"; corp migration **unverified** → still gated. Deferred cross-repo seeder half = #293. Coherence: `HANDOFF_PROCESS.md` L245 "LIVE" reconciles at archival |
| 7. `docs/archive/` triage-queue (9 files) | [operator periodic] | OPEN (operator) | periodic archive-review, out of night-sweep remit |
| Proposed [P2][S] fleet-backup task | proposal | **DONE (filed+closed) #291** | `e097212` |

### 2C — Night verification report (`2026-07-09-night-verification-report.md`)

| Finding | Tier | Verdict | Evidence |
|---|---|---|---|
| F1 #284 backup false-close (data-loss risk persists) | P1 | **DONE `e097212`** | "#284 false-close corrected via [#291] refile+close"; backups pushed+verified 0/0. (Same issue as 2B-item-2 / night-hygiene Phase-0) |
| F2 groom-parser counts past `Next quarterly:` as a groom | P1 | **DONE `e097212`** | "F2 groom-parser fix — past Next-quarterly no longer masks escalation"; proposed [P3][S] harden task executed inline |
| F3 `kill-candidates:` accepts bare `none`/any `#id` | P2 | **OPEN (kill?)** | lenient-by-design (proposals-only nudge, never blocks meaningfully). Optional low-value hardening → recommend **accept-as-designed** or KILL the note |
| F4 any `intake` substring satisfies L-epic WARN | P2 | **OPEN (kill?)** | advisory-only (WARN never blocks). Optional tighten to `intake-id`/`SEED-N` → recommend accept or KILL |
| F5 `check_floor_hash` consumer-scoped / #215 runbook markings | P2 | **DONE `6cf51a6`** | "#215 conformance-verify [hub-runnable]/[consumer-only] markings + --run-date note (night-audit F5)"; the further Layer-6 interpreter fix = #299 (`5ee7fb2`) |
| F6 3 `block-onedrive.SUPERSEDED*` backups (expected 2) | P2 | IN-FLIGHT #289 | retained per no-delete invariant; `~/.claude/` global-infra → **core-invariant #6** bars a unilateral hub edit; revisit at #289's build |
| F7 pre-commit stash dropped an unstaged JOURNAL edit | P2 (process) | **CAPTURED (memory), OPEN for LESSONS** | captured as auto-memory ("Pre-commit stash drops unstaged across commits"); `grep` confirms it is **not** in `LESSONS.md` → propose promoting to a LESSONS entry (see Phase 5) |

**Day-scorecard carried gaps** (all downstream of the above, none new): SEED 6–9 triage deferred to the architect session; #164 re-scoped M (residual → #293); Wave-1 repo onboarding not yet started (runbook ready; ai-council first).

### 2D — Cross-cutting so-what (Phase 2)

1. **The reporting→action loop is working.** ~70% of the 3 reports' findings are closed with a nameable SHA; the residue is genuinely hard (immutable cold bundle, cross-repo ai-council, an unbuilt age-gauge), not neglected.
2. **The one structural gap the night-hygiene cross-cut named is still fully open: no clock-triggered staleness anywhere** (every freshness organ is edit-triggered). Intake-SEED age (S1-1), cold-bundle age (S4-1), second-amendment summary drift (S2-2 class) all live here. This is #270/#271's charter — the single highest-leverage OPEN.
3. **`#299` is FIX-LANDED but TASK-OPEN:** the runbook Layer-6 interpreter fix shipped (`5ee7fb2` + JOURNAL anchor `d9ef53c`) yet BACKLOG:86 still carries #299 as DEFER → **formal close pending** (verify the "test proves proxy-passes-but-hook-fails" clause; see Action menu M-close and Phase 3 G14).

---

## 3. Intake census + archival ruling + G10–G14 filings (Phase 3)

### 3a — Intake census (`docs/intake/`, 9 docs)

Verdict per file (frontmatter `status:` is authoritative; body Status checked for the S1-2 contradiction class):

| id | file | status | verdict | evidence |
|---|---|---|---|---|
| 1 | `2026-07-06-functional-architect-nightly-loop.md` | CONSUMED | **CONSUMED** | consumed-by ADR-98/#268; body `:9` now `CONSUMED` (fixed by A5 `c08ac47`) |
| 2 | `2026-07-06-platform-feature-scan.md` | CONSUMED | **CONSUMED** | consumed-by #272/#273/#274 (Arc-5, evidence audits cited in frontmatter); body `:9` now `CONSUMED` (A5) |
| 3 | `2026-07-07-test-suite-hygiene.md` | CONSUMED | **CONSUMED** | consumed-by #278; body `:71` coherent (ACs → #278 UAT verbatim) |
| 4 | `2026-07-07-arc5-pilot-followup-seeds.md` | SEED | **OPEN-SEED** | no epic cites intake-id 4; still an active reference (doc #9 "counters #4 §S4") |
| 5 | `2026-07-07-changelog-review-seeds.md` | SEED | **OPEN-SEED** | 1 item (S1 `/config` workflow-size) STILL-OPEN — Phase 1 confirmed no release closes it |
| 6 | `2026-07-08-func-new-project-bootstrap.md` | SEED | **OPEN-SEED** | body `:102` SEED (folds #43); awaiting functional elaboration |
| 7 | `2026-07-08-func-ai-council-interface.md` | SEED | **OPEN-SEED** | body `:85` SEED; build lands in ai-council (ADR-41) |
| 8 | `2026-07-08-func-night-routines-suite.md` | SEED | **OPEN-SEED** | body `:96` SEED; behind #270/#271 (load-gauge gates it) |
| 9 | `2026-07-08-func-dashboards-local-html.md` | SEED | **OPEN-SEED** | body `:91` SEED; feeds #264 re-scope; awaiting triage |

**Census result: 3 CONSUMED · 6 OPEN-SEED · 0 PARTIAL · 0 DEAD. All 9 body Status lines are coherent with frontmatter → 0 Status-line updates made this run.** The only two docs that carried the S1-2 body-vs-frontmatter contradiction (ids 1 & 2) were already reconciled by A5 (`c08ac47`), so this run makes **no intake mutation**. No SEED was flipped: SEED→CONSUMED is a triage transition (intake README §5/§6, the technical-architect's confirm-gated lane), not a night-run action.

**Note the standing structural gap (from Phase 2 S1-1):** there is still **no age-based staleness signal** for these 6 open SEEDs against the README §7 ~1-month survival metric — the load-gauge (#270) / nightly loop (#271) that would provide it are unbuilt. Oldest open SEED (~2–3 days) is nowhere near the backstop, so nothing is breached — but 4 of the 6 open SEEDs are the *sole surviving record* of 7 groomed-away tasks, so a future rot = silent scope loss. This is the single highest-leverage OPEN across the whole brief.

### 3b — Archival mechanism (NEEDS-RULING — designed, NOT built)

**The gap:** CONSUMED (and any future REJECTED) intake docs accumulate in `docs/intake/` with no defined archival path. The design space (WHERE × WHEN × HOW):

| Axis | Options |
|---|---|
| WHERE | (i) new `docs/intake/archive/` subfolder · (ii) existing `docs/archive/` genre · (iii) **status-line-only, never move** |
| WHEN | on-consume (event) · periodic sweep (clock) |
| HOW | pre-commit hook · generator · manual |

**Recommendation: (iii) status-line-only + never move, navigation solved by a status-grouped generated index, derived on-edit (no sweep), built as a small generator.**

Rationale + trade-offs:
- **Preserves the `intake-id` join-key path stability.** A CONSUMED intake doc is cited back by its consuming ADR(s) and epic(s) (README §3) — moving it (options i/ii) breaks those references, the same reason ADRs are immutable-in-place. This is the decisive factor.
- **Zero ADR-101 amendment.** Option (i) mints a new `docs/<genre>/` subfolder, which ADR-101 §1 just *sealed* against — it would need a deliberate amendment. Option (iii) needs none (no new path).
- **No class-mixing.** Option (ii) drops requirements-spine docs into `docs/archive/`, which holds a different artifact class (same objection ADR-101 §5 raised for handoffs).
- **The real need is navigation, not physical archival** — keeping the active SEED view uncluttered by CONSUMED docs. A generated index grouping by lifecycle state (SEED / DRAFT / READY-FOR-TECHNICAL / CONSUMED / REJECTED) solves that *without a move* — exactly the pattern `docs/audits/README.md` and the ADR README already use (files never move; the index navigates).
- **Trigger = on-edit, not a sweep:** the grouping derives from each doc's frontmatter `status:`, so it regenerates on any intake edit (like `audit-index-freshness`) — no clock-trigger, no cron. Avoids adding the fleet's-first sweep organ for a 9-doc folder.
- **Mechanism = a small `gen_intake_index.py`** mirroring `gen_audit_index.py` (+ optional freshness gate), reusing the proven generated-index machinery. **Note: there is no intake index generator today** — the hub `docs/intake/README.md` is a hand-authored spec with no Contents listing (ai-council's has one; night-hygiene S6-1). So this IS a small build, deferred to a follow-up if ratified.
- **The one real cost of (iii):** `docs/intake/` file-count grows monotonically. Mitigation: revisit only if it crosses the ADR §5.5 navigation-overhead trigger (as `docs/audits/` did near ~200 files) — at 9 docs today that is years away; a year-subfolder or DevVault migration is a *future* trigger, not now.

Morning ruling needed: **build the status-grouped `gen_intake_index.py` (option iii) — yes/no**; if yes, file as a small [P3][S] task. Do NOT create an archive folder.

### 3c — G10–G14 routing (paste-ready; corp-monorepo Wave-1 n=2 gap-notes)

Source: `corp-monorepo/docs/intake/2026-07-10-runbook-gap-notes.md` (B-S2, executed 2026-07-10, HEAD `47f31b5`). These are the n=2 onboarding gate's product. **Proposed ids assume next-free `#303` (max bracketed = #302 this run — VERIFY at filing time; a departed id reused reds `git_backlog_drift`).** Each new-task line carries a `kill-candidates:` clause so it passes `backlog-filing-backpressure` as-is. **Do NOT write BACKLOG here — these are for morning filing.**

**G10 → NEW task (seeder / ADR-36):**
```
- [#303] [P2][S] Make seed_runbook.py child-class-aware (ADR-36 no-local-handoffs) — the leg-b seeder (scripts/seed_runbook.py, #164 leg b) unconditionally writes <target>/docs/handoffs/README.md, but ADR-36 children (corp-monorepo, and the class the #131/#293 fan-out will hit) carry NO local docs/handoffs/ by contract — a literal seed creates the exact dir ADR-36 forbids. Same class as ai-council's G3 (hub resolved: "create docs/intake/ only"). Make the seeder read the target's handoff-locality class and either (a) seed intake guidance instead, or (b) skip + emit a documented "hub-handoff-only, nothing to seed" status, so the deferred fan-out (ADR-41) cannot silently create forbidden dirs. · Done when: a --check/seed run against an ADR-36 child skips-or-redirects (never writes docs/handoffs/) with a test, and the seeder encodes the ADR-36 child class · refs scripts/seed_runbook.py, ADR-36, #293, #164, docs/audits/2026-07-08-census-amendment-docs-handoffs-ruling.md, corp-monorepo docs/intake/2026-07-10-runbook-gap-notes.md G10 · kill-candidates: #293 (the deferred fan-out this de-risks — gating the seeder on local-handoff class makes ADR-36 children a first-class skip) · serialize-group: architecture
```

**G11 → REQUIREMENT-AUGMENT to #262 (not necessarily a new id):** append corp as the SECOND concrete failing codemap layout, alongside ai-council #295. Key correction to the plan-v3 premise: **tach-presence does NOT rescue #262** — the blocker is node-granularity (the generator's node = top-level dir under `src/`; corp has exactly one, `src/corp/`, collapsing 13 subpackages to a single orphan node, 0 edges). The #262 fix must derive sub-module nodes from `src/<pkg>/<subpkg>/` and match `tach.toml` `corp.<subpkg>` layer keys (or use the AST import graph at that granularity), handling **both** flat (ai-council #295) and single-package-with-subpackages (corp). *If the operator prefers a discrete task rather than augmenting #262: `[#306] [P3][M] … refs #262, #295, corp gap-notes G11`.* **kill-candidate:** if generator-managed codemaps are only ever pursued for genuinely multi-top-level-package repos, close #262/#295 for single-package + flat layouts and keep them HAND-AUTHORED by policy (corp's ARCHITECTURE L120 marker already says so) — decide before building the fix.

**G12 → NEW task (notation):**
```
- [#304] [P3][S] Fix runbook deploy-command notation + add a consumer-identifier arg-form table — docs/runbooks/repo-onboarding.md L40/L43 reads `deploy/tool.py <consumer> --target 1.2.0` where its notation key (L26) defines <consumer> = filesystem path, but deploy/tool.py takes the registry NAME (deployed-versions.yaml key) — a literal-reading operator's first runbook command aborts preflight ("not a registered consumer"). Fix to <name> (or make tool.py path-tolerant). Compounding: the toolchain's consumer identifier is inconsistent across the #215 commands (tool.py <name>; audit.py repo <name> --repo-path <path>; enforcement_coverage --consumer <name>; floor_conformance --consumer <path>; seed_runbook --target-root <path>) — 3 take a name, 2 take a path — so the uniform notation cannot predict the form. Add a runbook table mapping each command → its actual arg form. · Done when: the runbook deploy command uses the working arg form AND a per-command arg-form table exists · refs docs/runbooks/repo-onboarding.md, deploy/tool.py, #215, corp gap-notes G12 · kill-candidates: doc-only fix, no build — trivial; the optional resolver path-tolerance is the only code portion (drop it and this is pure docs)
```

**G13 → NEW task (verify-only mode):**
```
- [#305] [P3][S] Add a verify-only / already-onboarded re-run mode to the onboarding runbook — the runbook's only path is the deploy/tool.py --execute converge, which requires a clean consumer tree (forcing stash/move when re-verifying a repo you're working in) and hits the prune-refusal on methodology-removed components (corp's present_modified ruff-gate). There is no "just re-verify, write nothing" mode, yet the n=2 gate and every future re-verify is verify-heavy. Document a verify-only re-run (assess + the #215 battery, no converge) and let the read-only assess run on a dirty tree (only --execute needs the clean-tree guard). · Done when: the runbook documents a verify-only re-run path AND assess runs on a dirty tree · refs docs/runbooks/repo-onboarding.md, deploy/tool.py, #215, corp gap-notes G13 · kill-candidates: may be a doc-note only ("for re-verify, skip the converge, run #215") with no new code — decide before building
```

**G14 → CLOSE #299 (bookkeeping, NOT a filing):** #299 (runbook Layer-6 verify) is FIX-LANDED — the corrected verify merged at `5ee7fb2` (+ JOURNAL anchor `d9ef53c`) and the two-direction fire-test is GREEN — but `BACKLOG.md:86` still carries `[#299] … · DEFER — peg: post-Wave-1`. Close via `/review-closures` citing the fire-test evidence. **VERIFY before close:** #299's "Done when" requires *a test proving the proxy-passes-but-hook-fails gap is caught* — confirm that test exists (the merge did the fix; confirm the test clause landed with it). **Bonus linkage for the close note:** #299's own text predicted corp's fragility verbatim (`pre_commit` in `.venv` but undeclared in pyproject → fresh re-clone won't repopulate) — B-S2 remediated exactly that (corp commit `5798598`: declared `pre-commit>=4.0` + `tach>=0.35`), so the fragility class is now closed on **both** legs (hub runbook-verify #299 + consumer pyproject B-S2).

> **G-notes X-refs (no new id):** G6/#296 (audit.py repo report not persisted) and G7/#297 (observe-arc needs a billed authenticated child) both reproduce on corp — cross-references, already tracked. #302/F1 branch-guard parity applies to corp (armed-but-empty pre-push, private remote) — already #302. corp audit **D4** (stale ARCHITECTURE.md, 7+ weeks) surfaced-only this session → corp-local `fix/` refresh session, gate the codemap portion on hub #262 (G11).

---

## 4. Audit-naming: census + universal template spec + enforcement carrier (Phase 4)

### 4a — Naming census (hub full history + fleet LOOK)

**Hub `docs/audits/` — 209 files** (207 at the ADR-101 §S3 census + this run's 2, both ADR-101-conforming — dogfooded). The §S3 measured basis (independently re-confirmed this run: `codex ×34`, `ecosystem-audit ×16`, `conformance-nightly-digest ×10`, `changelog-review ×5`, `fresh-eyes ×4`):

| Class-position bucket | Count | Examples |
|---|---|---|
| **Already class-led** (class token right after date) | 41 | `codex ×34`, `fresh-eyes ×4`, `draft-tier ×2`, `census-amendment ×1` |
| **Trivially compliant** (whole slug IS the class — recurring reports) | 31 | `ecosystem-audit ×16`, `conformance-nightly-digest ×10`, `changelog-review ×5` |
| **Subject-before-class** (class buried at slug-end) | ~130 | `-audit`, `-discovery`, `-verification`, `-inventory`, `-census`, `-execution-plan`, `-retrofit-plan` |
| **Class-less** (no class token) | 4 | `2026-05-20-handoff-process.md`, `2026-06-26-corpus-graph-justify-or-retire.md`, `2026-04-21-dev-knowledge-scope-tagging.md`, `2026-05-29-harness-engineering-positioning.md` |
| **Dot-slug carve-out** (embedded `.` is a repo/version token) | 3 | `2026-05-23-.dev-knowledge-audit.md`, `2026-05-29-handoff-v3.4-*.md ×2` |

Hub is **100% lowercase-kebab** — no UPPERCASE / underscore in the live tree. The proliferation pattern is **shallow**: one-off audits invent a bespoke *trailing* suffix rather than reuse a controlled vocabulary. Retroactive compliance would rename ~65% for near-zero gain (the index disambiguates by date; ~78% of citations are in immutable/append-only docs — ADR-100) → ADR-101's **prospective-only + grandfather** is the honest call.

**Fleet LOOK (read-only; no writes) — the operator's "diverging naming" concern, sourced:**

| Repo | Audit folder | Dominant patterns | Divergences vs the hub `<date>-<class>-<slug>` lowercase enum |
|---|---|---|---|
| **ai-council** | `docs/audits/` (22 + README) | `<date>-codex-<slug> ×13`, `<date>-<subject>-audit ×5`, no-class ×4 | **Cleanest child** — README *documents & enforces* the hub rule (`YYYY-MM-DD-<topic>`, hyphen+lowercase) and **quarantines** pre-ADR-34 UPPERCASE to `archive/legacy/` (`2026-03-15_CODE_REVIEW_REPORT.md`). Live divergences minor: `qa-lived-exercise` (qa class ✓ in enum), subject-before-class, bare `codex`, one dup-date anomaly (`…-review-2026-05-12.md`). |
| **corp-monorepo** | `docs/audits/` (65, **NO README, no convention**) | `<date>-conformance-nightly-digest ×18`, `<date>_UPPERCASE_<slug> ×10`, `<date>-deep-<slug> ×12 (+.html)`, `<date>-functional-<slug> ×5`, `<date>-codex-<slug> ×4` | **Least-disciplined.** A rich **UPPERCASE-underscore class enum runs parallel** to the lowercase files in the *same folder* and is **actively growing** (2026-07-07/08: `_AUDIT_`, `_BRIEF_`, `_EVIDENCE_`, `_HANDOFF_`, `_BRAINSTORM-BACKLOG_`). Also: `.html`/`.json` in the audit folder; no-date `DECISION_NN_…_SUPERSEDED.md ×28` transcripts; `conformance-baseline-digest` vs `-nightly-digest` split. |

**Operator's concern, mapped to the fix:** (a) *uppercase variants* → **corp's `_AUDIT_`/`_BRIEF_` family** (cross-repo; the casing rule §4b fixes it) + ai-council's quarantined legacy; (b) *Functional/QA/code-review styles* → corp `functional-* ×5`, ai-council `qa-lived`, corp `code-quality-audit`/`codex-hotfix-review` — the enum's semantic `functional`/`qa` classes cover these as **lowercase** tokens, and `code-review`→on-disk `codex`; (c) *subject-before-class* → the hub ~130 + common in both children, all grandfathered.

**Lane-B Flag-1 token-form reconciliation — proposed DIRECTION: adopt the on-disk forms (grammar describes reality, zero rename).**

| Enum label (ADR-101 draft) | On-disk token | Volume | Recommendation |
|---|---|---|---|
| `codex-review` | **`codex`** | 34 hub + 4 corp + 13 ai-council | **Enum adopts `codex`** — grammar matches what 3 repos already write; the alternative (rename 51 grandfathered files) is what ADR-101's prospective-only doctrine explicitly rejects. |
| `conformance-digest` | **`conformance-nightly-digest`** | 10 hub + 18 corp | **Enum adopts `conformance-nightly-digest`** (dominant form). The rarer `conformance-baseline-digest` (corp ×1) / `conformance-rerun-delta-digest` (hub ×1) stay grandfathered variants. *Secondary option if the operator wants the variants covered going-forward: a family longest-match `conformance-<*>-digest`.* |
| `ecosystem-audit`, `changelog-review` | exact match | 16+5 hub | no change — already reality. |

Direction rationale: this **makes ADR-101's "stays conforming, zero rename" property TRUE rather than assumed** (§2 flags it as a build-time choice). It is an implementation choice, not a re-opened policy question — grandfathering holds either way.

### 4b — Canonical audit-file template spec (DRAFT — canonical home is a morning ruling)

> One universal convention for every `docs/audits/*.md`. Base: ADR-101 §2 d.iii grammar, extended with a casing rule + a required header block.

**1. Filename grammar.** `<YYYY-MM-DD>-<class>-<slug>.md`, or the degenerate `<YYYY-MM-DD>-<class>.md` for pure recurring reports (no slug).

**2. Casing rule (NEW — the operator's uppercase concern).** **All-lowercase kebab-case**, everywhere: date, class, slug. No `UPPERCASE`, no `_underscore_`, no `CamelCase`. Sole charset carve-out: a literal `.` inside the slug when it is a meaningful repo/version token (`.dev-knowledge`, `v3.4`) — a rename there would be lossy (ADR-101 S3-1).

**3. Class ∈ the CLOSED enum** (whole-token **longest-match**, not split-on-first-hyphen — required for the multi-word tokens):
- *semantic:* `technical` · `functional` · `qa` · `census` · `verification`
- *recurring/automated:* `ecosystem-audit` · `conformance-nightly-digest` · `changelog-review`  ← on-disk forms per §4a
- *reviewer-origin:* `codex`  ← on-disk form per §4a
- *incident:* `incident-evidence`
- *`fresh-eyes`* — **[RATIFICATION-DECISION: recommend INCLUDE as the 11th]**: real corpus evidence (4 files, exact on-disk token), and it is a genuine reviewer-origin family, not a bespoke one-off. Adding it is the anti-bloat clause's first legitimate test, not drift.
- **Adding a class = a one-line ADR-101 amendment** (deliberate), never convention drift.

**4. Slug rules.** kebab-case, lowercase; `.` allowed only for repo/version tokens; optional (omit for recurring reports). No date-in-slug redundancy (ai-council's `…-review-2026-05-12.md` anomaly).

**5. Minimal REQUIRED header block** (every audit file — dogfooded by both this run's outputs):
```
# <Title>
- **Class:** <class> (ADR-101 enum) · **Date:** YYYY-MM-DD
- **Source-session:** <run/lane/HEAD or session context>
- **Status:** <PROPOSAL-ONLY | complete | …>
```
(Model-in-effect is recommended for unattended runs, per ADR-80 §5 silent-swap doctrine.)

**Canonical-home options (morning ruling):** (a) a section in `templates/` as `templates/audit-template.md` (mirrors `templates/intake-template.md` — **recommended**, it is the natural peer); (b) an ADR-101 amendment folding §4b's casing rule + header block into the decision; (c) a hub skill. Recommend **(a) + (b)**: the template gives authors a fill-in skeleton; the ADR-101 amendment gives the rule its enforceable home (feeds §4c).

### 4c — Enforcement carrier (NEEDS-RULING — design only, NOT built)

How the grammar gets **enforced** fleet-wide rather than merely requested:

| Option | Covers | Teeth | Verdict |
|---|---|---|---|
| **(i) Refusal-gate validator** (`validate_hermetization.py`, ADR-101 §3 Rule A+B) — a `language: system` pre-commit hook inspecting only ADDED paths; shipped to consumers via the floor/plugin carrier like `block-ff-push` / the enforcement mesh | hand-authored **AND** automated | **Yes** (deterministic BLOCK) | **RECOMMEND — primary.** Already specced in ADR-101 §3 (build is a named follow-up); the only option that catches the actual proliferation source (§S3: one-off hand-authored audits inventing bespoke suffixes). |
| (ii) Hub skill read at session start | hand-authored (agent-created) | No (advisory) | Skip as the sole mechanism — relies on agent compliance, no teeth. Fine as author guidance *alongside* (i). |
| (iii) Generator-side naming (report-writers name their own output) | automated reports only | Partial | Useful **complement** for the high-volume automated families (`ecosystem-audit`/`conformance-nightly-digest`/`codex`/`changelog-review`), but leaves hand-authored one-offs unchecked. |

**Recommendation: build (i) as primary** (ADR-101 §3 realizes ADR-34's 2.5-month-overdue enforcement), **optionally pair with (iii)** for the generators (belt-and-suspenders). The fleet evidence is decisive: **corp-monorepo's UPPERCASE `_AUDIT_` names are actively growing precisely because its `docs/audits/` has no README and no gate**, while ai-council's README-enforced discipline + quarantine holds the line — a shipped gate is what closes that gap. **Scope caveat (ADR-101 §Consequences):** the gate is **HUB-ONLY until a P6 rollout** (mirroring `roster-freshness`/`claude-rosters-freshness`); the consumer carrier (floor/plugin) is the P6 step, not now. Note (iii) covers automated reports but **not** hand-authored audits — so it cannot substitute for (i).

---

## 5. Skills / gotchas universalization matrix + new-gotcha draft (Phase 5)

_(pending — Phase 5)_

---

## 6. Changelog adoption shortlist (Phase 1)

_(folded here in Phase 6 — full analysis in `docs/audits/2026-07-11-changelog-review-codex-cc.md`)_

---

## 7. MORNING ACTION MENU

_(assembled last — Phase 6)_

---

## 8. Kill-list

_(assembled last — Phase 6)_
