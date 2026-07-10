# Census consolidated — morning action brief (2026-07-11)

- **Class:** `census` (ADR-101 enum) · **Date:** 2026-07-11 (morning-delivery; run overnight 2026-07-10)
- **Source-session:** NIGHT HUB v2 consolidation run, lane `lane-n-night-consolidation`, base HEAD `47f31b5` (main spine: lane-b #300 ADR-101 ← lane-a c08ac47 A5-hygiene)
- **Status:** PROPOSAL-ONLY. Executed mutations this run were limited to: new report files in `docs/audits/`, `Status:`-line updates in `docs/intake/` (Phase 3), and the JOURNAL append. Every verdict below is a proposal for the operator; nothing was deleted, renamed, moved, ratified, or filed to BACKLOG.
- **Model:** Opus 4.8 (`claude-opus-4-8[1m]`), effort max. Web + cross-repo research fanned to read-only subagents; every claim carries a SHA / file:line / URL, or an explicit UNVERIFIED flag.

> **Brief assembly status:** Phase 1 ✓ (separate file) · **Phase 2 ✓** · Phase 3 _pending_ · Phase 4 _pending_ · Phase 5 _pending_ · Exec summary + Action menu + Kill-list _pending_.
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

_(pending — Phase 3)_

---

## 4. Audit-naming: census + universal template spec + enforcement carrier (Phase 4)

_(pending — Phase 4)_

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
