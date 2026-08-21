# ARTIFACT — CLOUD-R4: ADR full-set review (86 live)

- **Slug:** `cloud-r4-adr-review`
- **Lane:** read-only cloud review lane, bound at `main`
- **Date:** 2026-08-21
- **Subject:** all 86 live ADR files in `docs/decisions/` (the 2 in `docs/decisions/archive/` — ADR-40, ADR-52 — are out of scope)
- **Authority:** none. Findings are EVIDENCE + RECOMMENDATION. The architect rules. This lane archived nothing, edited nothing, moved nothing.

---

## 0. Lane conditions and honest limits

**Shallow-clone guard FIRED.** `git rev-parse --is-shallow-repository` → `true`; `git log --oneline | wc -l` → 314 (not full history). Per the brief, spine-walking instruments were **NOT run**: `validate_git_backlog`, `check_no_ff_merges`, `check_journal_spine_anchor`, `block_ff_push`, `block_unanchored_push` and kin. No finding below rests on a spine walk.

**`audit.py` was NOT executed.** `audit.py run` writes reports and `_commit_routine_outputs` pushes to `origin/automation/fleet-audit` (`scripts/audit.py:4707`); a read-only lane does not invoke a writer to look at it. The check registry was read statically from `scripts/audit.py:3398-3446` and `scripts/audit_checks/registry.py` instead.

**Scope boundary.** Verdicts are about **the ADR corpus as a governing surface** — is the decision still true of the live tree, and is a reader told so. Where a mandate's execution lives outside this repo (ai-council, corp-monorepo, `~/.claude/`, Windows Task Scheduler), that is stated in the row rather than guessed at.

**Counting note.** 86 files = 84 distinct ADR numbers + 2 standalone amendment files (`ADR-51-amendment-2026-07-05`, `ADR-70-amendment-2026-07-07`). ADR-44 is a **documented reserved id**, not a gap-defect: `docs/decisions/README.md:66` records it as "Reserved — held pending N=2", and `protocols/PLAYBOOK.md:4313` records ADR-63 as superseding the hold.

---

## 1. Verdict census

| Verdict | Count |
|---|---|
| ACTIVE-CURRENT | 60 |
| ACTIVE-BUT-CONTRADICTED | 14 |
| SUPERSEDED-unmarked | 4 |
| ARCHIVAL-ELIGIBLE | 4 |
| DEFECTIVE | 4 |
| **Total** | **86** |

---

## 2. The mechanical root cause, stated once

Four incompatible `Status:` grammars are live across the 86 files, so **no parser can read the corpus** and the enum `docs/decisions/README.md:24-31` declares is a domain with no gate:

- `- **Status:**` (leading list dash) — **39** files
- `**Status:**` (bold, no dash) — **34** files
- `Status:` (bare) — **12** files (ADR-34/35/36/37/38/39/41/42/43/45/46/47)
- YAML frontmatter `status:` — **1** file (ADR-61)

`docs/decisions/README.md:41-43` already names limit (1) — "Nothing checks this enum — it is a declared domain, not a gate". ADR-94 filed the missing check as **#242 (header↔README status-coherence), not built**. Everything in §4 below — four unmarked supersessions, one self-contradicting ADR, one status line off-grammar — is downstream of that one un-built check. **This is the single highest-leverage finding in this review.**

---

## 3. Full classification — all 86 live ADRs

Verdict key: **AC** = ACTIVE-CURRENT · **ABC** = ACTIVE-BUT-CONTRADICTED · **SU** = SUPERSEDED-unmarked · **AE** = ARCHIVAL-ELIGIBLE · **DEF** = DEFECTIVE

| ADR | Title (short) | Verdict | Evidence (one line) |
|---|---|---|---|
| ADR-27 | Scope tagging architecture | **ABC** | Body mandates pre-commit enforcement + hybrid ≤25% ceiling; ADR-48 withdrew it — no scope hook in `.pre-commit-config.yaml`, no scope check in `ALL_CHECKS`; its own Amendment 2026-04-24 "Commit-time enforcement prescription" is the dead clause and carries no forward pointer. |
| ADR-28 | Three-layer architecture | **AC** | Live invariant, cited `CLAUDE.md` §5 rule 4 + `ARCHITECTURE.md:977`; one broken historical handoff link only. |
| ADR-29 | LESSONS grandfathering | **AC** | Amended in-file 2026-07-17 (legacy-archival split); carried verbatim in `CLAUDE.md` §4/§5. |
| ADR-30 | Default branch `main` | **AC** | `Supersedes: none / Superseded by: none`; enforced by `block-commit-on-main` + `block-ff-push`. |
| ADR-31 | Authority model (prescriptive + audit) | **AC** | Live; `ARCHITECTURE.md:980`. Path drift only: cites `.dev-knowledge/tools/audit.py`, live path is `scripts/audit.py`. |
| ADR-32 | Handoff format v2 + role split | **SU** | Superseded by ADR-42 → **ADR-82** (v6 live). Body carries a forward pointer appended 2026-08-12, but `**Status:**` still reads `Accepted` — the index enum has no forward-pointer state. |
| ADR-33 | VISION.md universalization | **AC** | Its own 2026-05-23 amendment withdrew the `tier:`/`scale:` clauses; `check_vision_md.py:34` requires exactly `{version,last_reviewed,owner,status}` — amendment and organ agree. |
| ADR-34 | File naming convention | **AC** | Amended by ADR-101 (2026-07-11); enforced by `validate-hermetization` Rule B. |
| ADR-35 | Lessons base activation | **ABC** | Mandates `lessons-index.json` + `scripts/lessons_query.py` + `scripts/reindex_lessons.py` — **all three absent**; zero references in `scripts/`, `protocols/`, `ARCHITECTURE.md`; absent from ARCHITECTURE Governing-ADRs. Live carrier is the open row `tasks/4-build-lessons-index-json-sessionstart-retrieval.md`. Unbuilt ~3.8 months. |
| ADR-36 | Audit tool architecture | **AC** | Amended 2026-07-18 (RULING-W write path); `scripts/audit.py` live. Path drift: cites `.dev-knowledge/ecosystem-index.yaml`, live is `ecosystem/index.yaml`. |
| ADR-37 | Session boundary protocol (two-phase) | **SU** | Superseded by ADR-42 → ADR-62 → **ADR-82**. "Current State"/"Future State" appears **nowhere** in `protocols/HANDOFF_PROCESS.md` (v6.2.0). No forward pointer, no status change — the sibling it shares a lineage with (ADR-32/42) got pointers on 2026-08-12; this one was missed. |
| ADR-38 | Universal repo architecture baseline | **AC** | A5/A6 amendments live; `check_adr38_baseline` in `ALL_CHECKS`. Path drift: `docs/ARCHITECTURE.md` → root `ARCHITECTURE.md`. |
| ADR-39 | File lifecycle governance | **AC** | Amended 2026-07-17 (`LESSONS-legacy-<span>.md` class); its superseded registry entries each carry an in-file marker (e.g. `:241`). |
| ADR-41 | Cross-session backlog architecture | **ABC** | Its 2026-06-02 amendment closes "a single canonical cross-session `BACKLOG.md` as the source of truth … is unchanged" — **contradicted by ADR-107 step 3 ([#439], 2026-07-28)**: `BACKLOG.md:2` now reads "GENERATED FILE — do not edit directly. Source of truth: `tasks/`". No third amendment records the flip. |
| ADR-42 | Handoff format v3.0 | **SU** | Superseded by ADR-62 (v4) → ADR-82 (v5/v6). Forward pointer appended 2026-08-12 calls itself "the clearest instance of superseded-without-note"; `Status:` line still `Accepted`. |
| ADR-43 | Cross-project transcript routing | **AC** | Correctly re-scoped by its own 2026-07-23 amendment (routed-mirror retired, ai-council production stands). Carries 5 broken `docs/handoffs/_archive/...` links — the live dir is `docs/handoffs/archive/`. |
| ADR-45 | Handoff architecture v4 (explored) | **AC** | Status `Explored, not adopted`; supersession claim formally withdrawn 2026-05-25. Correct as a record. Note: this value is **not** on the README H3 archival bar, so it can never become archive-eligible under the current criteria. |
| ADR-46 | Cross-repo dated-entries format | **AC** | Status `Partially superseded`; demotion note in-file; `check_dated_entries_format` correctly absent from `ALL_CHECKS`; the surviving `normalize-dated-headers` hook is live. **But** its `Superseded by:` names "Council Simplification verdict 2026-05-16 (this branch)" — an unresolvable pointer (no artifact, no locator). |
| ADR-47 | Cross-repo BACKLOG organization | **AC** | Same shape as ADR-46 — correctly demoted, same unresolvable `Superseded by:` pointer. |
| ADR-48 | Trim documentation governance | **AC** | The withdrawal instrument for ADR-27/46/47; live. |
| ADR-49 | Consolidate past-recording files | **AC** | Cited live and repeatedly exercised — `CLAUDE.md` §12 condensations run on this ADR's authority. |
| ADR-50 | Machine-document encoding standard | **AC** | Binding but **thin**: its only inbound reference in live prose is the ARCHITECTURE grouping line `:983`; no organ enforces it. Archival-lane input, not a defect. |
| ADR-51 | Architecture doc convention | **ABC** | Its Amendment 2026-05-28 and 2026-05-28(v2) mandate Mermaid dark-theme / high-contrast directives **inside canonical `ARCHITECTURE.md`** — reversed by the separate 2026-07-05 amendment file (Mermaid left canonical docs; check #7 retired, `scripts/audit.py:3405`). Neither Mermaid-theme section carries a supersession marker **inside ADR-51**, so a top-to-bottom reader (or a child repo adopting the convention) obeys a retired rule. |
| ADR-51-amend-2026-07-05 | LLM-first canonical docs | **AC** | Verified live: `check_mermaid_theme_directive` is a comment-out at `scripts/audit.py:3405`; the codemap is compact text and `codemap-freshness` still gates it. |
| ADR-53 | CLAUDE.md single instruction file | **AC** | `check_claude_md` live; ADR-52 archived as its consequence. Broken link `templates/AGENTS-md-template.md` is the expected retirement residue. |
| ADR-54 | Codex reviewer config as global standard | **AC** | `codex/AGENTS.md` present; `/codex-review` in `CLAUDE.md` §7. The `~/.codex/AGENTS.md` deploy leg is outside this repo — unverified here, stated not assumed. |
| ADR-55 | Applied-task internalization gate | **AE** | Marked "Amendment 2026-05-29 — Superseded by v4"; **v4 is itself archived** (`protocols/archive/HANDOFF_PROCESS_v4.4.md`), so the pointer is stale by two generations. Findings transcribed into: `protocols/HANDOFF_PROCESS.md` §5 (probe gate) + ADR-62 Related line ("v3.4 amendment trail"). **Blocker:** status line still reads `Accepted`, so the H3 bar (keys on `Superseded`/`Deprecated`) cannot fire. |
| ADR-56 | Inline prompt generation card | **AE** | Same shape as ADR-55. Findings transcribed into `templates/handoff/` + `scripts/gen_handoff.py` (the card became generated). Same `Accepted`-status blocker. |
| ADR-57 | Two-layer bundle contract | **AE** | Same shape. Findings transcribed into `protocols/HANDOFF_PROCESS.md` v6 §5 + the thin-boot model (ADR-82). Same blocker. |
| ADR-58 | Structured claims + symmetric verification | **AE** | Same shape. Findings transcribed into `protocols/HANDOFF_PROCESS.md` v6 §5 probes + `scripts/verify_handoff_probes.py` / `check_handoff_probes`. Same blocker. |
| ADR-59 | Universal visual repository pattern | **AC** | All three organs live in `ALL_CHECKS`: `check_dot_prefix_discipline`, `check_canonical_md_visibility`, `check_workspace_settings`. Three in-file corrections, all marked. |
| ADR-60 | docs/ folder taxonomy | **ABC** | Names six semantic roles; **`docs/council-questions/` and `docs/research/` no longer exist on disk** and are absent from `SANCTIONED_GENRES` (`scripts/validate_hermetization.py:102-104` = `{archive, audits, decisions, handoffs, intake}`). Only the `runbooks` removal earned an ADR-101 amendment; these two removals earned none. `docs/decisions/README.md:351-352` still links both as live. |
| ADR-61 | Git worktree for parallel sessions | **DEF** | Status carried **only** in YAML frontmatter (`status: Accepted 2026-05-28`), off the corpus's own `**Status:**` grammar. Three sections marked "❌ SUPERSEDED, use native". Secondary defect: `docs/decisions/README.md:41` describes this file as carrying "**no parsable status line at all**" — that claim is itself wrong; the status exists, in a fourth grammar. |
| ADR-62 | v4 HANDOFF_PROCESS ratification | **SU** | Superseded by **ADR-82**, stated plainly at `ARCHITECTURE.md:985` ("superseded by v5 (ADR-82, canonical 2026-06-11)") and in ADR-82's own Related line. **No forward pointer, no status change** — and unlike ADR-32/42 it was not caught in the 2026-08-12 sweep. It ratifies as "canonical" a protocol that now lives at `protocols/archive/HANDOFF_PROCESS_v4.4.md`. |
| ADR-63 | Scrum-master review authority | **AC** | `protocols/PLAYBOOK.md:4313` — "Authorized by ADR-63 (Accepted 2026-05-30, N=3) — superseding the Reserved ADR-44". |
| ADR-64 | BACKLOG.md architecture | **ABC** | Decision 2 (flat layout) superseded by ADR-66 — recorded **in ADR-66, not here**. Compounded: ADR-107's flip makes `BACKLOG.md` generated, so its "lean active file" premise now describes an output, not a source. ADR-107 asserts "none superseded here", which is true of its decisions but not of its subject. |
| ADR-65 | BACKLOG done-item disposition | **AC** | Narrowly amended by ADR-107 ("retire, never delete" — `ARCHITECTURE.md:1003`); amendment lives in ADR-107, which cites ADR-65 explicitly, so the edge is traceable. |
| ADR-66 | BACKLOG story-map hierarchy | **AC** | `validate-backlog` pre-commit hook live; correctly declares its own narrow supersession of ADR-64 Decision 2. |
| ADR-67 | AI-Council process operationalization | **AC** | `protocols/AI_COUNCIL_PROCESS.md` at **v2.2, 2026-07-29** — actively versioned, and its changelog records both the ADR-43 re-scope and the ADR-107 post-flip fix. |
| ADR-68 | Autonomous overnight review agent | **ABC** | `ARCHITECTURE.md:987` marks it **"[REFUTED — historical]"**; `:956` records the local job "was never registered as a scheduled task"; its output path `briefings/YYYY-MM-DD.md` does not exist; `ARCHITECTURE.md:960-964` records that its backlog pointer (#85) died two months ago. **The ADR file itself carries no refutation marker** — its only amendment (2026-06-01) is about worktree lifecycle. |
| ADR-69 | Cross-repo audit reach model | **AC** | `audit run` iterates `ecosystem/`; read-only cross-repo runner intact per `ARCHITECTURE.md:980`. |
| ADR-70 | Three-tier self-enforcing process layer | **AC** | Tier-1 plugin `tier1-lifecycle@dev-knowledge-methodology` enabled (`.claude/settings.json`); Tier-2 `fleet_health.py`; Tier-3 Workflows — all three rows live at `ARCHITECTURE.md:649-650`. |
| ADR-70-amend-2026-07-07 | XL routing tier (Fable 5) | **AC** | Ratified amendment; `claude-fable-5` is a live model id. |
| ADR-71 | Doc-tooling hook source repo | **AC** | `.pre-commit-hooks.yaml` present, six ids exported. Live-fact refinement recorded **outside** the ADR at `ARCHITECTURE.md:704`: corp-monorepo consumes only 2 of 6, pinned `v1.3.1`, four withdrawn by recorded waiver. The ADR's own "Validated by the corp-monorepo pilot (pending)" is stale against its own status line. |
| ADR-72 | Cloud Routines are hub-independent | **AC** | Cloud Routine live (`ARCHITECTURE.md:642,650`); hub still private, so the closed URL-swap hatch still holds. |
| ADR-73 | Per-repo orchestration distribution | **AC** | Canonical templates hub-side under `templates/`; propagation via `deploy/` carriers. |
| ADR-74 | Automation doctrine consolidation | **AC** | Layer→job matrix canonical at `ARCHITECTURE.md` Ch3; amended 2026-06-07 in-file. |
| ADR-75 | Exclusion-zone register | **AC** | Register live in `protocols/PLAYBOOK.md` + `protocols/ENVIRONMENT.md`; extended by ADR-77/78 zone classes. |
| ADR-76 | Local fleet-baseline host | **AC** | `ARCHITECTURE.md:649` — "`fleet_health.py` (Task Scheduler → Python, **no `claude -p`**; ADR-76)". The Windows scheduler registration is off-repo and **not verifiable from this environment**; stated, not assumed. |
| ADR-77 | Immutable-paths zone class | **AC** | `block_immutable_edits.py` PreToolUse guard armed (`CLAUDE.md` §9). Broken link `scripts/hooks/adr_amend.py` — never built; carried live as `tasks/112-adr-amend-helper-adr-immutable-zone-extension.md`. |
| ADR-78 | Child methodology floor | **AC** | `templates/child-methodology-floor.md.tmpl` + `.sha256` present; `check_floor_integrity` live. |
| ADR-79 | Browser methodology carrier (bundle-only) | **ABC** | Its bundle-delivery half is superseded by ADR-82 — stated at `ARCHITECTURE.md:706` and `:992`, and at `protocols/HANDOFF_PROCESS.md:9-10` ("Supersedes: … the heavy-bundle delivery ADR-79 mandated"). Its Consequences still open an implementation item for consolidated `BUNDLE.md` output, which `ARCHITECTURE.md:706` records as never existing in the tree. **No marker in ADR-79.** The Projects-deferred half genuinely stands. |
| ADR-80 | Two-tier automation adoption | **AC** | Writer policy live; committed-generated zone model in force (ADR-86 depends on it). |
| ADR-81 | Feature-lifecycle definition of done | **AC** | Five-point bar (a)–(e) after its 2026-07-03 amendment; `ecosystem/organ-index.md` + `organ-index-freshness` are its mechanization. |
| ADR-82 | HANDOFF_PROCESS v5 (model C) | **ABC** | Title and entire Decision body say **v5**; the live spec is **v6.2.0** (`protocols/HANDOFF_PROCESS.md:1,4`, "v6 cut 2026-07-31"). Its 2026-08-04 amendment does record the "v5.3 → v6.0.1 catch-up", so the drift is marked — but the header, title and body are unreconciled, and `CLAUDE.md` §7 has to gloss it ("per HANDOFF_PROCESS.md v6 (ADR-82)"). Secondary: the `Decommission:` field is still written conditionally — "none active while **Proposed**" — on an Accepted ADR. |
| ADR-83 | Protocols-archive convention | **AC** | Convention live (`protocols/archive/` holds v3.4 + v4.4). Its "**Hard gate: v4.4 stays canonical** — its archival is a #149 flip-step, not done here" clause is **discharged** (v4.4 is archived) and says nothing about it. Broken relative link `archive/HANDOFF_PROCESS_v3.4.md` (actual: `protocols/archive/…`). |
| ADR-84 | Automation-writer isolation (Q9) | **AC** | `ARCHITECTURE.md:315,993`; `automation/*` explicitly protected in `.claude/rules/git-discipline.md`; `check_fleet_audit_replication` live. |
| ADR-85 | Session-lifecycle enforcement | **AC** | Heavily and **correctly** self-amended (2026-06-16, 2026-06-19, 2026-08-03 §A2/§A5/§A6, 2026-08-07). The retired `/override` path is marked in-file and re-warned at `CLAUDE.md` §7; `.claude/commands/override.md` ships self-labelled RETIRED. The model for how supersession should be recorded. |
| ADR-86 | Conformance-dashboard location | **AC** | `ecosystem/conformance.md` present (+ `.html`). |
| ADR-87 | Architect↔CC equilibrium contract | **AC** | Amended 2026-08-08 (population boundary on model/effort). |
| ADR-88 | File-oriented dependency management | **AC** | Header flipped to Pattern B 2026-08-04; `check_doc_code_edge` / `check_undeclared_edges` / `check_reconciled_versions` live. |
| ADR-89 | Computed code-dependency edges | **AC** | Header flipped to Pattern B 2026-08-04 with a re-measured live-scope correction; `check_import_edges` live. |
| ADR-90 | Doc→code resolver-allows-N | **AC** | `ecosystem/doc-code-edge.yaml` present; `check_doc_code_coverage_drift` live. |
| ADR-91 | Methodology corpus versioning | **AC** | `ecosystem/deployed-versions.yaml` present; `deploy/manifest-v1.4.0.yaml` is the current release; `check_deployed_methodology_version` live. |
| ADR-92 | Deploy-runbook doctrine | **AC** | Body's "four carriers" corrected by its own 2026-07-25 amendment; live roster is 7 declared / 6 implemented (`deploy/manifest-v1.4.0.yaml`). Correctly handled staleness. |
| ADR-93 | Floor provisioning model A | **AC** | Its two "missing" paths (`.claude/CLAUDE-FLOOR.md`, `.claude/check_floor_hash.py`) are **consumer-context by design** — `check_floor_integrity.py:36-38` records the hub as the floor SOURCE, not a carrier. Not a defect. |
| ADR-94 | ADR status line mutable on ratification | **AC** | The exception is live and used (ADR-82, ADR-88/89, ADR-111, ADR-112). **Its own filed follow-up #242 — the header↔README status-coherence check — is still not built**, and that omission is the direct cause of §4's findings. |
| ADR-95 | AI-council query lane-split | **AC** | Record-only by construction; arms nothing, so nothing can have rotted. |
| ADR-96 | Deploy remove leg | **AC** | `check_safe_removal` live; amended 2026-07-06. |
| ADR-97 | Tree orchestration (epic lanes) | **ABC** | Its "**2–3-lane concurrency cap**" coexists with ADR-110's "designed for **4–10**"; ADR-110 itself records the two as "different axes, **unreconciled here**". `CLAUDE.md` §4 carries both `epic/<slug>` and `worktree-<name>` prefixes. **Nothing in ADR-97 points forward to ADR-110**, so a reader booting an epic lane off ADR-97 obeys the narrower cap without knowing a wider one was designed. |
| ADR-98 | Intake pipeline | **AC** | `docs/intake/` live + `intake-index-freshness` hook; two 2026-07-07 amendments in-file. |
| ADR-99 | Epic-naming convention (Track-X) | **AC** | Hub-side record only, correctly scoped ("rename executes in ai-council's dedicated chat, never from hub"). The ai-council-side execution is **not verifiable from this repo** — stated, not assumed. |
| ADR-100 | Audit retention + count-tiered index | **AC** | `docs/audits/README.md` generated + `audit-index-freshness` hook (the #269 follow-up it deferred has since landed). |
| ADR-101 | Hermetization | **ABC** | Seven in-file amendments, `validate-hermetization` armed — exemplary. **But its own anti-bloat clause** ("a new class = a one-line ADR amendment, never drift") was **not honoured** for the 2026-08-11 organ-index relocation to `ecosystem/organ-index.md`: that landed by operator ruling K-1 in `protocols/STANDING_RULINGS.md`, with no ADR-101 amendment. The precedent is that the taxonomy can now move without touching the ADR that seals it. |
| ADR-102 | Parity-surfaces gate-rev axis | **AC** | `ecosystem/parity-surfaces.yaml` present; `check_fleet_parity` live and blocking. |
| ADR-103 | Parity-surfaces ownership axis | **AC** | Same organ; loader refuses a missing ownership block, so partial classification cannot reach `main`. |
| ADR-104 | Fleet repository shape | **AC** | Amended 2026-08-03 (machine-locatable declaration anchor); `check_membership_agreement` reds on drift. |
| ADR-105 | Routine consumer declaration | **AC** | `check_routine_consumers` live. Its own stated coverage limit (1 marked row vs ~30 live routines) is recorded in the check's docstring — honest, not drifted. |
| ADR-106 | Environment isolation via uv | **AC** | `uv.lock`, `.python-version`, `pyproject.toml` all present and Tier-1-sanctioned (`validate_hermetization.py:95-97`). |
| ADR-107 | BACKLOG restructure (strangler) | **AC** | Flip executed and visible: `BACKLOG.md:2` is a GENERATED-file header; `check_task_tree_coherence` live. **Drift it left behind:** `scripts/validate_hermetization.py:63-66` still comments "BACKLOG.md stays the source of truth until the flip arc" — stale by ~3.5 weeks (code comment, not doctrine). |
| ADR-108 | Decision routing + engineering standards | **AC** | Amended 2026-08-19 (§B fleet Python paradigm). Arms no gate and says so. |
| ADR-109 | Fleet desired-state contract v1 | **ABC** | §2 declares `ecosystem/registry.md` **loses authority** and [#455] dissolves it. The file is still on disk and still opens "**Hand-maintained human registry** … the human registry — name · path · purpose · status", with **no ADR-109 tombstone**. `ARCHITECTURE.md:1011` records the retirement as [#383] wave work, so this is known-and-scheduled — but a reader of `registry.md` today gets zero signal that its authority was revoked three weeks ago. |
| ADR-110 | Parallel execution batch protocol | **AC** | Four in-file amendments; `check_stale_worktrees` live; `/lane-boot` + `/lane-integrate` shipped in `.claude/commands/`. |
| ADR-111 | Finding pipeline (four outcomes) | **AC** | Ratified 2026-08-10; arms no gate and says so; register entry I-F1 cited. |
| ADR-112 | Two-tier adoption bar | **DEF** | **Self-contradicting on read order.** `Status:` line 3 = `Accepted`; line 5 `Decision tier` = "ratification … **has not happened**"; line 12 opens a section literally titled "**## Status note — read this before citing the ADR**" whose first sentence is "This ADR is **Proposed**, not Accepted … it does not yet bind." The retraction is a RATIFICATION MARKER at the file's **very end**, ~130 lines later. A reader who obeys the section's own instruction reaches the wrong conclusion. |
| ADR-113 | L0–L5 maturity ladder ratification | **AC** | Newest ADR (2026-08-19), correctly formed. Not yet listed in `ARCHITECTURE.md`'s Governing-ADRs block (which stops at ADR-112) — index staleness, not an ADR defect. |

---

## 4. Corpus-level defects (not attributable to a single ADR)

These are **DEFECTIVE** findings against the index and the corpus surface. They are listed here rather than in a row because no single ADR owns them.

**D1 — `docs/decisions/README.md` census is stale and off by two.** `:33-35` reads "across the **86** ADR files in this folder and `archive/`", then enumerates 81+2+1+1+1 = 86. Disk today: **86 live + 2 archived = 88**. ADR-113 (2026-08-19) post-dates the 2026-08-12 declaration, but the count was already off by one before it.

**D2 — the ADR↔transcript traceability table points into a deleted tree.** `README.md:279-324` cites ~20 `docs/decisions/transcripts/...` paths; that directory was deleted 2026-07-22 (`b4435fad`) and the README's own header `:5-7` says so. The table was never reconciled with the deletion the same file announces.

**D3 — `README.md:261-267` describes a live `transcripts/` folder.** "12 files currently in `transcripts/`" and "Relocated to `transcripts/archive/legacy/` (2026-05-12)" — both describe a tree that no longer exists.

**D4 — `README.md:351-352` links two dead genres.** `docs/council-questions/` and `docs/research/` are named as live "Related" surfaces; neither exists on disk, and neither is in `SANCTIONED_GENRES`. Same defect as ADR-60's row, surfaced at the index.

**D5 — 20 ADRs carry broken links into `docs/decisions/transcripts/`.** ADR-31, 32, 33, 34, 42, 45, 46, 47, 51, 55, 56, 57, 58, 64, 76, 78, 79, 84, 89, 92. These are **evidence pointers in immutable records**, so the right disposition is almost certainly a single index-level note, not 20 edits — but they are broken links and the brief asks for them.

**D6 — 71 unresolved in-repo path references across 40 ADR files** (measured by extracting backticked repo-relative paths and testing existence). Beyond D5, the load-bearing subset is: ADR-35 (`scripts/lessons_query.py`, `scripts/reindex_lessons.py` — never built), ADR-77 (`scripts/hooks/adr_amend.py` — never built), ADR-82 (`protocols/HANDOFF_PROCESS_v5.md` — the retired beta), ADR-43 (5× `docs/handoffs/_archive/…` — dir renamed to `archive/`), ADR-83 (`archive/HANDOFF_PROCESS_v3.4.md` — wrong relative root). The rest are historical artifacts or documented drafts-branch consumptions (ADR-98/99/100 cite `drafts/2026-07-07-proposals @ 3da29ea`, tag `archive/drafts-2026-07-07`, which is correct behaviour, not a defect).

---

## 5. Input to the archival lane

The brief asks ARCHIVAL-ELIGIBLE rows to cite where findings were transcribed. Four qualify, and they share one blocker.

| ADR | Findings transcribed into | Archival blocker |
|---|---|---|
| ADR-55 | `protocols/HANDOFF_PROCESS.md` §5 (probe gate); ADR-62 Related ("v3.4 amendment trail") | Status line reads `Accepted` |
| ADR-56 | `templates/handoff/` + `scripts/gen_handoff.py` (the card became generated) | Status line reads `Accepted` |
| ADR-57 | `protocols/HANDOFF_PROCESS.md` v6 §5; the ADR-82 thin-boot model | Status line reads `Accepted` |
| ADR-58 | `protocols/HANDOFF_PROCESS.md` v6 §5 probes; `scripts/verify_handoff_probes.py`; `check_handoff_probes` | Status line reads `Accepted` |

**The blocker is structural, and the archival lane needs to know it.** `README.md:19-21` states H3's archival bar keys on `Superseded`/`Deprecated`, "two values that appeared on **zero live ADRs**, so the bar's trigger was unreachable by its own wording". That is still true today. **Every candidate in this table is unreachable by the criteria until a status line is edited — and ADR-94 permits an in-place status edit only *on ratification*.** So the archival lane cannot proceed on these four without an architect ruling that either (a) extends ADR-94's in-place exception to a supersession restamp, or (b) re-bases H3's bar on the in-body supersession marker rather than the status line.

Two further candidates the archival lane will meet and should not archive: **ADR-32** and **ADR-42** both carry explicit `**Retained, not archived:**` clauses (appended 2026-08-12) on the ground that live `protocols/` prose still cites them — H3's zero-inbound bar is unmet. **ADR-45** ("Explored, not adopted") is a third: its status value is not on H3's bar at all.

---

## 6. Top-10 actions, ranked by the risk of someone OBEYING a dead ADR today

Ranking is by *obey-risk*: how likely a competent reader, arriving at that file today, acts on a statement that is no longer true.

**1. ADR-112 — resolve the self-contradicting status. — NEEDS-ARCHITECT-RULING**
A section titled "read this before citing the ADR" tells the reader the ADR does not bind; the retraction is 130 lines below it. This is the only ADR in the corpus that instructs the reader toward the wrong conclusion. It ranks first because the instruction is explicit. It needs a ruling rather than an edit: the Status-note section is *decision content*, `STANDING_RULINGS` B6 forbids rewriting it, and ADR-94's exception is status-line-only — the same wall §5 hits. A permitted move (e.g. a pointer line immediately under the Status note, or a marker relocated to the top) is an architect call.

**2. ADR-62 — record its supersession by ADR-82. — NEEDS-ARCHITECT-RULING**
ADR-62 ratifies as *canonical* a protocol now sitting in `protocols/archive/`. `ARCHITECTURE.md:985` and ADR-82's Related line both state the supersession; the ADR itself says nothing. It is the highest-consequence unmarked supersession: a session that reads ADR-62 to learn "the canonical handoff process" gets v4. The 2026-08-12 sweep gave ADR-32 and ADR-42 forward pointers and **missed this one** — the fix is the same append, but appending to an immutable ADR is a ruled act (B6 / ADR-94), not mechanical.

**3. ADR-68 — mark the refutation in the ADR. — NEEDS-ARCHITECT-RULING**
`ARCHITECTURE.md:987` calls it "[REFUTED — historical]" and `:956` records the scheduled task was never registered. The ADR carries no such marker. Someone asked to "stand up the night agent per ADR-68" would build a mechanism the architecture has already replaced with the cloud Routine. Same append-to-immutable constraint as #2.

**4. ADR-51 — mark the two Mermaid-theme amendments as retired. — NEEDS-ARCHITECT-RULING**
ADR-51 is the convention **child repos adopt**, and it still contains two amendment sections mandating Mermaid theme directives inside canonical `ARCHITECTURE.md`. The 2026-07-05 reversal lives in a *separate file*, so nothing inside ADR-51 warns a top-to-bottom reader. This is the highest cross-repo blast radius on the list.

**5. ADR-37 — record its supersession alongside ADR-32/42. — NEEDS-ARCHITECT-RULING**
Third file in the same lineage; the two-phase Current/Future State vocabulary appears nowhere in v6. It was in scope for the 2026-08-12 `N2-D2-ii` sweep by the sweep's own logic and was missed. Ruling wanted on whether the sweep is re-run to completion (ADR-37 + ADR-62 + ADR-79) as one act.

**6. ADR-79 — mark the bundle-delivery half superseded. — NEEDS-ARCHITECT-RULING**
`protocols/HANDOFF_PROCESS.md:9-10` and `ARCHITECTURE.md:706` both record the supersession; ADR-79's Consequences still open an implementation item for a `BUNDLE.md` that `ARCHITECTURE.md:706` confirms has never existed. Its Projects-deferred half genuinely stands, so the marker must be **partial** — which is precisely why it needs a ruling and not a mechanical stamp.

**7. Build #242 — the header↔README status-coherence check. — NEEDS-ARCHITECT-RULING (to schedule); the build is then mechanical**
Filed by ADR-94, never built. Its absence is the *shared cause* of items 1, 2, 3, 5, 6 and of §2's four-grammar problem. Fixing the six instances above without building the detector guarantees a seventh. Recommend the check parse all four live status grammars, validate against the README enum, and red on a header↔README disagreement. **This is the highest-leverage item on the list and is ranked 7th only because it prevents future obedience-risk rather than removing present risk.**

**8. ADR-109 — tombstone `ecosystem/registry.md`. — SAFE-MECHANICAL**
The ADR is right and the file is wrong: `registry.md` still presents itself as the authoritative human registry three weeks after ADR-109 §2 revoked that authority. `ARCHITECTURE.md:1011` already scopes physical retirement to [#383], so no decision is reopened — this is a header note on a *generated-adjacent, non-immutable* ecosystem file pointing readers at ADR-109. Safe because the ADR needs no edit and the file is not in an immutable class.

**9. ADR-60 — reconcile the genre set, and close the two dead index links. — SAFE-MECHANICAL (the links) / NEEDS-ARCHITECT-RULING (the ADR)**
`docs/decisions/README.md:351-352` advertising `docs/council-questions/` and `docs/research/` as live surfaces is a mechanical fix in a non-immutable index file. The underlying question — that two of ADR-60's six genres left `SANCTIONED_GENRES` with no amendment, while `runbooks` got one — is a ruling: it is the same anti-bloat-clause erosion recorded against ADR-101 (row above), and the two should be ruled together.

**10. ADR-35 — rule on whether the decision still stands. — NEEDS-ARCHITECT-RULING**
Accepted 2026-04-29; none of `lessons-index.json`, `scripts/lessons_query.py`, `scripts/reindex_lessons.py` exists; zero live references; absent from Governing ADRs. It is not contradicted — it is simply un-executed for ~3.8 months behind an open row (`tasks/4-…`). The obey-risk is real but low-velocity (someone budgets a build against a decision the fleet has de-facto dropped). Under ADR-111 this is a **CANDIDATE**: it needs a decision, not a row. Rank 10 because acting on it wastes effort; it does not corrupt state.

**Deliberately not in the top 10, and why:** D5's twenty broken transcript links are the largest *count* in this review but the lowest obey-risk — a dead evidence pointer in an immutable record misleads nobody about what to do. Recommend one index-level note over twenty edits. Likewise `scripts/validate_hermetization.py:63-66`'s stale flip comment (ADR-107 row) is a genuine SAFE-MECHANICAL fix with essentially zero obey-risk, and belongs in an ordinary cleanup pass rather than here.

---

## 7. Conflicts between this brief and repo core-invariants (reported, not improvised)

**C1 — the artifact's own filename violates ADR-101. Measured, not predicted.** The brief mandates `ARTIFACT-cloud-r4-adr-review.md`. `ARTIFACT-*.md` is not a member of `SANCTIONED_TIER1_FILES` (`scripts/validate_hermetization.py:82-98`), so at repo root it is a **new Tier-1 top-level file class**. Run live against the staged add:

```
validate_hermetization: refused -- ADR-101 hermetization violation(s):
  ARTIFACT-cloud-r4-adr-review.md: unsanctioned new top-level file
  'ARTIFACT-cloud-r4-adr-review.md' -- Tier-1 files are a closed class
  (ADR-101 section 1); a genuinely new class is an ADR-101 amendment,
  not a drive-by add
exit=1
```

**Disposition, per the brief's own precedence clause ("the repo wins: report the conflict, do not improvise"):** the file is committed at the repo-native home and grammar — `docs/audits/2026-08-21-census-cloud-r4-adr-review.md`. `census` is a member of ADR-101's closed 11-class enum and is the correct class for a full-set classification of 86 records; the brief's slug is preserved verbatim. That path returns `exit=0` from the same gate. **No gate was bypassed. `--no-verify` was not used** — the gate's own message offers it, and taking it would have been exactly the drive-by add ADR-101 exists to refuse.

**C2 — the ADR-101-compliant home forces a second file, and the brief's "ONE file" rule yields to it.** Adding any file to `docs/audits/` reddens the `audit-index-freshness` gate, because `docs/audits/README.md` is a **generated** index (`scripts/gen_audit_index.py --check` → `exit=1`, "README.md is stale vs docs/audits/"). Regenerating it is the mechanical closure the repo demands of every `docs/audits/` add, not a second authored artifact. `docs/audits/README.md` is not on the brief's forbidden list. Recorded here so the two-file commit is legible rather than surprising.

**C3 — nothing else conflicted.** The read-only boundary held: `tasks/`, `BACKLOG.md`, `protocols/`, `STANDING_RULINGS.md`, `.pre-commit-config.yaml`, `.gitignore` and `docs/intake/` were **read and not written**; no file was moved; no ADR was archived, restamped or edited; `main` was not touched (work is on `claude/cloud-r4-adr-review`, a lane prefix on `CLAUDE.md` §4's enum).

---

**Lane complete. This lane changes nothing. The architect rules.**
