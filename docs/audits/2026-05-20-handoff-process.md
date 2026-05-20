# Audit — Handoff Process at HEAD

<!-- scope: meta -->

Date: 2026-05-20
Branch: `docs/audit-handoff-process`
Auditor: Claude Code (read-only, file-state-verified)
HEAD at audit time: see `git rev-parse HEAD` in commit metadata.

---

## 1. Scope & method

**Goal.** Describe how the handoff process *actually works* in `.dev-knowledge` at HEAD on 2026-05-20 — the live mechanism that just produced `docs/handoffs/2026-05-19-dev-knowledge-session-sync/`. Not a restatement of ADR-42's principle.

**Method.** File inspection only. Every claim below traces to a file in this repo (path + line number where relevant). No script was executed. No conversation memory or session inference was used.

**Scope boundary.** `.dev-knowledge`-side machinery only — protocol, templates, slash command, scripts, archive layout. The OLD/NEW browser chat behaviour is part of the mechanism but only inspected through the artifacts they produce/consume (`stage1-question.md`, `stage2-response.md`, 11-file bundle). No cross-repo audit.

**Out of scope.** Runtime execution of any handoff tool. Cross-repo handoff flow (`ai-council`, `corp-monorepo`). Restating ADR-42 verbatim.

---

## 2. Mechanism overview

### 2.1 Three actors

Per `protocols/HANDOFF_PROCESS.md` §"Three actors" (lines 86–131):

| Actor | Role | Lifecycle |
|---|---|---|
| **Claude Code in `.dev-knowledge`** | Orchestrator + generator | Runs Stage 1 and Stage 3 |
| **OLD browser chat** for `{repo}` | Stage 2 source — the existing chat being wrapped up due to context exhaustion | Reads `stage1-question.md`; produces `stage2-response.md` |
| **NEW browser chat** for `{repo}` | Stage 3 receiver — opened *after* Stage 3 emits the bundle, with zero history | Reads 11-file bundle + `00_first-message.md`; fills `09_EXECUTION_EVIDENCE.md` |

The OLD-vs-NEW distinction is load-bearing: a fresh chat at Stage 2 collapses to restating known audit findings (the rejected "audit-sync shortcut", removed in the 2026-05-09 afternoon ADR-42 amendment).

### 2.2 Three stages

Per `docs/decisions/ADR-42-handoff-format-v3.md` §"Three-stage flow" (lines 183–200):

```
Stage 1 (Claude Code)  →  Stage 2 (OLD chat)  →  [Stage 2.5 Q&A, optional]  →  Stage 3 (Claude Code)  →  NEW chat
                                                                                                          ↓
                                                                                          09_EXECUTION_EVIDENCE.md
                                                                                          (return trip)
```

All handoff types — `audit-sync`, `session-sync`, `feature-X-sync` — run the full three-stage flow. No shortcut exists (`.claude/commands/handoff.md` line 30).

### 2.3 Authority layers

| Layer | File | Role |
|---|---|---|
| Principle | `docs/decisions/ADR-42-handoff-format-v3.md` (v3, amended through v3.2) | Canonical structural decision |
| Operational protocol | `protocols/HANDOFF_PROCESS.md` (v3.3.3) | Triggers, state tracking, validation checkpoints |
| Stage 1 template | `templates/HANDOFF_QUESTION_TEMPLATE.md` | Question prompt skeleton |
| Stage 3 template | `templates/HANDOFF_FOLDER_TEMPLATE.md` (references v3.3.2) | Folder structure spec |
| Slash command | `.claude/commands/handoff.md` (references v3.1) | Trigger router |

Authority order on conflict: ADR-42 wins (`protocols/HANDOFF_PROCESS.md` lines 11–14). The version-string skew across these surfaces is a real finding — see §7 Gap M-1.

### 2.4 State tracking

Three filesystem locations encode handoff lifecycle:

- `docs/handoffs/_in_progress/{slug}/` — cycle in flight. Holds `stage1-question.md` + `stage2-response.md` (placeholder, then populated).
- `docs/handoffs/{slug}/` — final 11-file flat bundle (emitted by Stage 3).
- `docs/handoffs/archive/{slug}/` — Stage 1+2 inputs moved here after Stage 3 (preserved for traceability without violating flat structure).

Stage detection is a function of which files exist under `_in_progress/{slug}/` (`protocols/HANDOFF_PROCESS.md` lines 153–177).

---

## 3. Stage-by-stage walkthrough

### 3.1 Stage 1 — Claude Code generates the question

**Trigger.** `"Make handoff for {repo}"` (default type: `session-sync`) or `"Make handoff for {repo}, type {type}"` (`protocols/HANDOFF_PROCESS.md` lines 134–149).

**Procedure** (`protocols/HANDOFF_PROCESS.md` lines 180–251):

1. Compute `slug = {YYYY-MM-DD}-{repo}-{type}`.
2. Capture target-repo state: `HEAD SHA`, current branch, `git status --porcelain`.
3. Read `BACKLOG.md`, identify items relevant to `{repo}`; for `audit-sync`, also load `docs/audits/`.
4. Read `templates/HANDOFF_QUESTION_TEMPLATE.md`.
5. Generate `_in_progress/{slug}/stage1-question.md` — a two-section file split by a `PASTE_BOUNDARY` (thick `═` line):
   - **Section A** — operator instructions; not pasted into the OLD chat.
   - **Section B** — paste-into-OLD-chat block, ordered: title → architect role framing → bundle contents preview → epistemic-honesty rules (witnessed / inferred / unknown markers) → format requirements → captured repo state → audit context (if applicable) → BACKLOG references → 5 SBAR/I-PASS questions → end-of-paste divider.
6. Pre-create `_in_progress/{slug}/stage2-response.md` as a placeholder with `═══ REPLACE EVERYTHING BELOW THIS LINE ═══` marker and a 5-section skeleton.
7. Append JOURNAL entry under today's date.
8. Run validators (`pre-commit run --all-files`, `python scripts/validate_scope_tags.py`).
9. Single commit on feature branch.

**Output files.** `_in_progress/{slug}/stage1-question.md` + `_in_progress/{slug}/stage2-response.md` (placeholder).

**The five canonical questions.** OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES — SBAR + I-PASS hybrid per ADR-42 §"Question pipeline" (lines 256–267). Section ordering in `stage1-question.md` puts role / bundle / epistemic / format *before* the questions; v3.1 had them at the end and OLD chat produced fabricated specifics (`HANDOFF_PROCESS.md` lines 220–225).

### 3.2 Stage 2 — OLD chat answers (out of repo)

**Source.** The OLD browser chat for `{repo}` — emphatically not a fresh chat. Rob pastes Section B of `stage1-question.md` into that chat. The architect answers all 5 questions from lived knowledge.

**Returning the response into the repo.** Two paths (`HANDOFF_PROCESS.md` lines 270–279):

- **Option A.** Rob edits `_in_progress/{slug}/stage2-response.md` directly, replacing the placeholder block below the marker.
- **Option B.** Rob types `"save this response as stage 2 for {slug}"` in Claude Code; Claude Code overwrites the placeholder.

**No format validator runs at Stage 2.** Stage 3 detects population by checking that all 5 expected headings exist below the `═══ REPLACE EVERYTHING BELOW THIS LINE ═══` marker with non-placeholder content (`HANDOFF_PROCESS.md` lines 166–173).

**No separate commit at this step** — the populated file is included in Stage 3's commit.

### 3.2.1 Stage 2.5 — Optional Q&A loop (NEW chat ↔ OLD chat)

After Stage 3 emits the bundle and NEW chat presents synthesis, NEW chat may ask up to 3 rounds of clarification questions back to OLD chat. Rounds captured in `_in_progress/{slug}/stage2-amendments.md`. Bypassed when NEW chat has no questions. (`HANDOFF_PROCESS.md` lines 292–326.)

Stage 2.5 is *temporally* after Stage 3 in some readings (operator workflow runs synthesis *after* upload), but its inputs amend Stage 2. The protocol places it between Stage 2 and Stage 3 by intent and after Stage 3 by operator workflow — see §7 Gap L-2.

### 3.3 Stage 3 — Claude Code reconciles and emits the bundle

**Trigger.** `"Complete handoff for {repo}"` or `"Stage 3 for {slug}"`.

**Procedure** (`protocols/HANDOFF_PROCESS.md` lines 330–410):

1. Verify both `stage1-question.md` and populated `stage2-response.md` present — else STOP.
2. **Drift check (ancestor variant, v3.3.3).** Run `git merge-base --is-ancestor {STAGE1_SHA} HEAD`. Exit 0 → proceed; exit 1 → FLAG both SHAs to Rob, do not silently proceed. (Replaces v3.3.2's strict-equality check, which produced false-negative failures when Stage 3 commits had advanced HEAD by design; empirical case `b640bcf9` / `777af78`.)
3. Read `templates/HANDOFF_FOLDER_TEMPLATE.md`.
4. Read `.dev-knowledge` VISION.md, protocols/PLAYBOOK.md, protocols/ESSENTIALS.md.
5. Read populated `stage2-response.md`.
6. Identify ADRs cited in DIRECTIVES (→ `07_ACTION_PLAN.md`).
7. Emit `docs/handoffs/{slug}/` with **11 flat files** (table in §4 below).
8. Compute SHA-256 of every file in the folder; write `01_manifest.json` last.
9. **Move (not copy)** `_in_progress/{slug}/*` to `docs/handoffs/archive/{slug}/`; verify source directory removed via `Test-Path`.
10. Append JOURNAL entry; (legacy step: append CHANGELOG — see §7 Gap M-3).
11. Run validators.
12. Single commit on feature branch.

**Drift handling.** Manifest pins Stage 1 HEAD; NEW chat must re-verify the pinned SHA is an ancestor of current target-repo HEAD before acting (`HANDOFF_PROCESS.md` lines 493–498).

**Invariants vs essences.** `02_VISION.md` / `03_PLAYBOOK.md` / `04_ESSENTIALS.md` are *full copies* — never curated (ADR-42 lines 233–242). `05_GOVERNANCE_ESSENCES.md` carries only 2–3-sentence operational essences for ADRs *cited in `07_ACTION_PLAN.md` directives* — not full ADRs, not target-repo ADRs.

---

## 4. File artifacts produced per stage

| Stage | Path | Content origin | Lifecycle |
|---|---|---|---|
| 1 | `_in_progress/{slug}/stage1-question.md` | Generated from `HANDOFF_QUESTION_TEMPLATE.md` | Moved to `archive/{slug}/` at Stage 3 |
| 1 | `_in_progress/{slug}/stage2-response.md` (placeholder) | Generated by Claude Code | Populated at Stage 2; moved at Stage 3 |
| 2 | `_in_progress/{slug}/stage2-response.md` (populated) | OLD chat output, written by Rob or Claude Code | Moved at Stage 3 |
| 2.5 | `_in_progress/{slug}/stage2-amendments.md` (optional) | Q&A loop rounds | Moved at Stage 3 |
| 3 | `docs/handoffs/{slug}/00_README.md` | Generated | Immutable post-close |
| 3 | `docs/handoffs/{slug}/00_first-message.md` | Generated | Immutable post-close |
| 3 | `docs/handoffs/{slug}/01_MANIFEST.md` | Generated; HEAD pin + file index | Immutable post-close |
| 3 | `docs/handoffs/{slug}/01_manifest.json` | Generated last; SHA-256 of all 11 files | Immutable post-close |
| 3 | `docs/handoffs/{slug}/02_VISION.md` | Full copy of `.dev-knowledge/VISION.md` | Immutable post-close |
| 3 | `docs/handoffs/{slug}/03_PLAYBOOK.md` | Full copy of `protocols/PLAYBOOK.md` | Immutable post-close |
| 3 | `docs/handoffs/{slug}/04_ESSENTIALS.md` | Full copy of `protocols/ESSENTIALS.md` | Immutable post-close |
| 3 | `docs/handoffs/{slug}/05_GOVERNANCE_ESSENCES.md` | Curated ADR essences for ADRs cited in directives | Immutable post-close |
| 3 | `docs/handoffs/{slug}/06_STATE_OF_PLAY.md` | REALITY + RATIONALE from Stage 2; audit findings if audit-sync | Immutable post-close |
| 3 | `docs/handoffs/{slug}/07_ACTION_PLAN.md` | OBJECTIVE + DIRECTIVES + BOUNDARIES from Stage 2 | Immutable post-close |
| 3 | `docs/handoffs/{slug}/08_TREE.txt` | `git ls-files` in target repo | Immutable post-close |
| 3 | `docs/handoffs/{slug}/09_EXECUTION_EVIDENCE.md` | Empty return-trip template | Filled by NEW chat |

**Verified against the just-completed cycle.** `ls docs/handoffs/2026-05-19-dev-knowledge-session-sync/` returns exactly these 12 file names (note: `01_manifest.json` + 11 `.md`/`.txt` files = 12 entries despite the protocol's "11 files" framing — both the protocol and ADR-42 list 12 entries including the JSON manifest; "11 files" is a label, not a literal count). Archive `docs/handoffs/archive/2026-05-19-dev-knowledge-session-sync/` contains the expected `stage1-question.md` + `stage2-response.md`.

---

## 5. Coupling & dependencies

### 5.1 Cross-file references at HEAD

| From → To | Reference | Status |
|---|---|---|
| `.claude/commands/handoff.md` line 2 → `protocols/HANDOFF_PROCESS.md` | "ADR-42 v3.1 three-stage flow" | **Stale label** — protocol is now v3.3.3 |
| `.claude/commands/handoff.md` line 12 → `protocols/HANDOFF_PROCESS.md` | "Read … (v3.1) for the full operational procedure" | **Stale label** |
| `templates/HANDOFF_FOLDER_TEMPLATE.md` line 4 → `HANDOFF_PROCESS.md` | "HANDOFF_PROCESS.md v3.3.2 for full flow" | **Stale label** — protocol is v3.3.3 |
| `protocols/HANDOFF_PROCESS.md` line 9, line 656 → `ADR-42` | "Authority: ADR-42 (amended 2026-05-09 night)" | Current |
| `docs/decisions/ADR-42-handoff-format-v3.md` | Self — no upward reference | Canonical |
| `docs/decisions/ADR-45-handoff-architecture-v4.md` line 5 → ADR-42 | "Status: Superseded by 2026-05-13 night minimum-viable refinement" | ADR-45 *itself* is marked Superseded — see §6 |

### 5.2 What is enforced mechanically vs by prompt discipline

**Mechanically enforced** (executable check, fails noisily):

- Stage 3 ancestor check (`git merge-base --is-ancestor`) — flags drift before bundle emission.
- SHA-256 manifest — detects post-emission file tampering.
- `_in_progress/{slug}/` existence check — Stage 3 STOPs if missing inputs.
- `Test-Path` post-move verification — Stage 3 raises if source dir survives.
- pre-commit (`ruff check --fix`, `normalize_headers.py`) — gates every commit.
- `scripts/validate_scope_tags.py` — gates each stage commit.

**Discipline-only** (prompt rule, no validator):

- Universal Self-Containment Rule — "no cross-repo content in handoff" is policed by reader's judgement at all three actor roles (`HANDOFF_PROCESS.md` lines 31–82).
- Stage 2 5-section format — Stage 3 checks heading presence, not content quality.
- OLD-chat-vs-NEW-chat routing — the protocol can't tell which chat received the paste.
- ADR essence selection — "ADRs cited in directives" is curator judgement.
- Articulation gate (NEW chat must produce 4-item readback before acting) — depends on NEW chat following `00_first-message.md` and Rob confirming.

This split is intentional (`HANDOFF_PROCESS.md` lines 519–531). The gap is that *all the load-bearing semantic invariants are discipline-only*. Mechanical gates catch drift; they don't catch a hallucinated REALITY or a cross-repo DIRECTIVE.

---

## 6. Conformance to ADR-42

**ADR-42's principle.** Universal self-containment via 3-stage relay, full invariant carrying, structured 5-question pipeline, return-trip evidence (full text in `docs/decisions/ADR-42-handoff-format-v3.md`).

**How the live mechanism implements it.**

- Three-stage flow: implemented in `HANDOFF_PROCESS.md` §§180–410 and dispatched by `.claude/commands/handoff.md`.
- Full invariants: enforced by Stage 3 procedure step 4 (read VISION/PLAYBOOK/ESSENTIALS) and HANDOFF_FOLDER_TEMPLATE — confirmed by file presence in the 2026-05-19 bundle.
- 5-question pipeline: encoded in `templates/HANDOFF_QUESTION_TEMPLATE.md` and re-stated as Stage 2 section requirements.
- Drift mitigation: ancestor-check + SHA-256 manifest, both at Stage 3 and re-checked by NEW chat per `01_MANIFEST.md`.
- Return trip: `09_EXECUTION_EVIDENCE.md` shipped empty, filled by NEW chat.

**ADR-42 vs ADR-45.** ADR-45 was drafted on 2026-05-13 as a "v4" architecture (collapse bundle to MANIFEST + NEXT, deliver invariants via `@path` imports + operator upload, replace prompt discipline with mechanical gates). Per its own status line (`ADR-45-handoff-architecture-v4.md` line 5), it was *superseded the same night* by the minimum-viable refinement that became HANDOFF_PROCESS v3.3 — full invariants and 11-file bundle preserved because the audit's "what works, preserve" findings (`docs/audits/2026-05-12-handoff-process-audit.md`) conflicted with the bundle-replacement direction.

So the practice/governance position is: **ADR-42 v3.2 + HANDOFF_PROCESS v3.3.3 is canonical; ADR-45's structural pivot is shelved, not active.** This is healthy — but it means the ADR-45 file functions as a frozen design exploration rather than a live decision, which is a navigation hazard for newcomers (see Gap M-2).

---

## 7. Observed limitations & gaps

Severity legend: **CRITICAL** (mechanism broken), **HIGH** (real risk in normal flow), **MEDIUM** (drift / hygiene), **LOW** (minor), **INFO** (architectural note, not a defect).

### M-1 — Version-string skew across handoff surfaces *(MEDIUM)*

**Finding.** Three surfaces reference three different protocol versions:

| Surface | Version cited | Actual |
|---|---|---|
| `.claude/commands/handoff.md` (lines 2, 12) | v3.1 | v3.3.3 |
| `templates/HANDOFF_FOLDER_TEMPLATE.md` (line 4) | v3.3.2 | v3.3.3 |
| `protocols/HANDOFF_PROCESS.md` (line 6) | v3.3.3 | v3.3.3 (truth) |

**Why it matters.** v3.1 → v3.3.3 spans the audit-sync shortcut removal *and* the strict-equality → ancestor drift-check change. A reader landing on the slash command and following its "(v3.1)" reference would expect strict-equality semantics. The discrepancy did not break the 2026-05-19 cycle because Claude Code reads HANDOFF_PROCESS.md itself, not the version string in the command — but the labels are misleading.

**Recommendation.** Update both stale labels to `v3.3.3` (or to "current"). Single-line edits.

### M-2 — ADR-45 status semantics are ambiguous *(MEDIUM)*

**Finding.** ADR-45's title says "Supersedes ADR-42"; its status line says "Superseded by 2026-05-13 night minimum-viable refinement (HANDOFF_PROCESS v3.3 + HANDOFF_FOLDER_TEMPLATE update)". The supersession-by-protocol-version inverts normal ADR semantics (ADRs supersede ADRs; protocols implement ADRs). In effect ADR-45's *direction* was rolled back the same day it was drafted, and the practical authority returned to ADR-42 v3.2.

**Why it matters.** A newcomer reading the ADR index sees "ADR-45 supersedes ADR-42" and infers ADR-45 is canonical. They must read three paragraphs of ADR-45's own Context to learn the v1 conclusion was over-broad and rolled back. This is the worst case for governance navigability.

**Recommendation.** Either (a) issue a small ADR-45 amendment that re-states the rollback in the title/status field clearly (e.g., "Status: Explored, not adopted; ADR-42 v3.2 remains authority"); or (b) file a tiny successor ADR that formally rescinds ADR-45's supersession claim and re-anchors authority on ADR-42. Either resolves the read-order trap.

### M-3 — Stage 3 procedure still references deleted CHANGELOG *(MEDIUM)*

**Finding.** `protocols/HANDOFF_PROCESS.md` line 394 (Stage 3 step 12): "Append CHANGELOG entry under today's date (Changed or Added section)". `CHANGELOG.md` was deleted on 2026-05-16 per ADR-49. The Stage 3 procedure has not been updated.

**Why it matters.** A literal-minded executor would attempt to write to a file the governance forbids. In practice Claude Code may notice and skip the step, but the protocol's executable steps no longer match the repo's file invariants. This is the kind of drift ADR-49's consolidation was meant to prevent.

**Recommendation.** Delete step 12 from `HANDOFF_PROCESS.md` Stage 3 procedure. JOURNAL step 11 plus git history already satisfy the past-recording requirement per ADR-49.

### M-4 — `scripts/backlog_extract.py` targets deleted `BACKLOG_ARCHIVE.md` *(MEDIUM)*

**Finding.** `scripts/backlog_extract.py` line 22 (`archive = repo_path / "BACKLOG_ARCHIVE.md"`) and line 64 (print statement) target a file deleted on 2026-05-16 per ADR-49. The script is dormant (no schedule, no caller in HEAD) but live in the tree. It does not run as part of the handoff process — but it shares the past-recording governance domain that ADR-49 reset, and its existence is a trip-hazard for anyone scanning `scripts/` for handoff-adjacent tooling.

**Why it matters.** Mentioned in BACKLOG as P2 already. Inclusion here for traceability of the handoff-machinery audit (the script touches BACKLOG, which the handoff process reads at Stage 1 step 4).

**Recommendation.** Resolve per BACKLOG entry — retire, repurpose, or leave dormant with explicit "ADR-49 dormant" header comment.

### M-5 — Stage 2 has no format validator; Stage 3 inherits whatever shape OLD chat returned *(MEDIUM)*

**Finding.** Stage 3's pre-flight check only verifies that the five expected headings exist below the `═══` marker with non-placeholder content (`HANDOFF_PROCESS.md` lines 166–173). It does not check that BOUNDARIES contains rules, that REALITY is not empty prose, that DIRECTIVES are sequenced, or that the response is markdown-clean. The Stage 2 pre-send checklist (`HANDOFF_PROCESS.md` lines 64–71) is OLD-chat self-discipline.

**Why it matters.** A degenerate Stage 2 (e.g., five headings with `[old chat answer]` replaced by a single sentence each) would pass Stage 3's gate and produce a thin, possibly hallucinated `07_ACTION_PLAN.md`. Self-Containment Rule violation is one degenerate case; "too thin to act on" is another. NEW chat's articulation gate (per v3.3) is the last line of defense.

**Recommendation.** Add a Stage 3 pre-flight check that each Stage 2 section is at least N non-blank lines; if not, FLAG and ask Rob to confirm proceeding. Low-effort guard; meaningful coverage gain.

### M-6 — ADR-39 registry gap on handoff templates *(MEDIUM)*

**Finding.** ADR-42 §"Lifecycle entries" (line 322) explicitly defers registration of `templates/HANDOFF_QUESTION_TEMPLATE.md` and `templates/HANDOFF_FOLDER_TEMPLATE.md` to a follow-up session as a P3 BACKLOG item. That item is still open. The templates are load-bearing for the handoff flow but unregistered per ADR-39.

**Why it matters.** ADR-39 governs file lifecycle (creation, update authority, supersession). Unregistered means "exempt from lifecycle governance" — which is the wrong default for files that determine bundle structure.

**Recommendation.** Resolve per BACKLOG entry — register or formally exempt with rationale.

### L-1 — Stage 2.5 placement is ambiguous between protocol and operator workflow *(LOW)*

**Finding.** `HANDOFF_PROCESS.md` §"Stage 2.5" (lines 292–326) reads as if Q&A happens *between* Stage 2 and Stage 3 ("Between Stage 2 (architect response) and Stage 3 (folder generation)"). The operator workflow in ADR-42 amendment v3.2 (lines 48–63) places synthesis + Q&A *after* the bundle is uploaded to NEW chat — i.e., temporally after Stage 3. The two framings can both be true (logical placement vs operator-sequence placement) but the protocol does not name the distinction.

**Why it matters.** First-time readers infer there are two distinct Q&A phases. There is one — operated by NEW chat after upload, with answers routed back to OLD chat.

**Recommendation.** Add one sentence to §Stage 2.5: "Although named for its logical position (amendments to Stage 2 input), Stage 2.5 runs temporally *after* Stage 3 upload — NEW chat asks; Rob routes to OLD chat; answers return."

### L-2 — Drift detection assumes Stage 3 runs in the same session as Stage 1 *(LOW)*

**Finding.** Stage 3 uses the SHA captured in `stage1-question.md` and checks ancestry against current HEAD. If Stage 3 runs days later, the ancestor relationship may still hold (good) but the manifest's "expected HEAD" line in `01_MANIFEST.md` will pin an old SHA that is far behind the bundle's actual surrounding state. NEW chat's ancestor check still passes, but the gap is invisible.

**Why it matters.** Edge case; cleanly handled by the ancestor semantics. Worth flagging in case a future tightening (e.g., "Stage 1 SHA must be within N commits of HEAD") becomes desirable.

**Recommendation.** None required; document as known semantic in `HANDOFF_PROCESS.md` if revisited.

### L-3 — Time-bound clauses in REALITY persist as artefacts of past handoff cycles *(LOW)*

**Finding.** Observed in `docs/handoffs/2026-05-19-dev-knowledge-session-sync/06_STATE_OF_PLAY.md` (and earlier cycles): REALITY sections contain phrases like "as of yesterday" / "this morning" that have no anchor date once the bundle is consumed by NEW chat in a future session. The template does not require absolute-date conversion.

**Why it matters.** Bundles age. Time-bound prose becomes uninterpretable after the originating week.

**Recommendation.** Add Stage 3 directive to `HANDOFF_FOLDER_TEMPLATE.md`: when copying REALITY content into `06_STATE_OF_PLAY.md`, convert relative time references to absolute dates. Low-effort, durable improvement.

### INFO-1 — Self-Containment Rule has no mechanical gate

The Universal Self-Containment Rule is the *most-cited* invariant in `HANDOFF_PROCESS.md` (most of §31–§82). Its enforcement is entirely by reader-side flagging at three actors. This is a deliberate design choice (ADR-45's "mechanical gates" rewrite was explored and rolled back). The mechanism's robustness is correlated with discipline, not with code. Recording this as architectural context, not as a defect.

### INFO-2 — JOURNAL append timing

Both Stage 1 and Stage 3 append JOURNAL entries (`HANDOFF_PROCESS.md` lines 237, 393). Per `CLAUDE.md` §4, JOURNAL is newest-first prepended at session wrap or workday close — the per-stage append breaks the "session wrap" framing but is the intended pattern for handoff cycles. Recording the deviation; not a defect.

---

## 8. Recommendations (summary)

In priority order, all low-effort:

1. **M-3** — Strike CHANGELOG step from Stage 3 procedure in `HANDOFF_PROCESS.md`.
2. **M-1** — Update version labels in `.claude/commands/handoff.md` and `templates/HANDOFF_FOLDER_TEMPLATE.md` to current.
3. **M-2** — Clarify ADR-45 status with a small amendment or successor ADR.
4. **M-5** — Add Stage 3 pre-flight thinness check for Stage 2 sections.
5. **L-3** — Add absolute-date conversion rule to `HANDOFF_FOLDER_TEMPLATE.md` for REALITY content.
6. **M-4 / M-6** — Resolve per existing BACKLOG entries.

Each is a delete/add of < 10 lines. None require new architectural decisions; all are hygiene against the v3.0 → v3.3.3 evolution.

---

## 9. Cross-references (no restatement)

- Principle: `docs/decisions/ADR-42-handoff-format-v3.md`
- Operational protocol: `protocols/HANDOFF_PROCESS.md` (v3.3.3)
- Templates: `templates/HANDOFF_QUESTION_TEMPLATE.md`, `templates/HANDOFF_FOLDER_TEMPLATE.md`
- Slash command: `.claude/commands/handoff.md`
- Adjacent ADRs: ADR-32 (v2.0 origin, §1–§3 extended), ADR-37 (Current/Future overlay), ADR-39 (file lifecycle — templates unregistered), ADR-41 (BACKLOG canonical), ADR-45 (v4 explored, rolled back), ADR-49 (CHANGELOG/BACKLOG_ARCHIVE deletion), ADR-50 (machine-doc encoding for bundles)
- Live cycle audited: `docs/handoffs/2026-05-19-dev-knowledge-session-sync/` + `docs/handoffs/archive/2026-05-19-dev-knowledge-session-sync/`
- Prior audit (12 May): `docs/audits/2026-05-12-handoff-process-audit.md` — referenced by ADR-45

---

## 10. Audit method log

| Activity | Files touched |
|---|---|
| Read full | ADR-42, HANDOFF_PROCESS.md, `.claude/commands/handoff.md`, ADR-45 (head), backlog_extract.py (head), migrate_links.py (head), HANDOFF_FOLDER_TEMPLATE.md (head) |
| Listed | `docs/handoffs/`, `docs/handoffs/2026-05-19-.../`, `docs/handoffs/archive/2026-05-19-.../`, `docs/audits/` |
| Grep-verified | `CHANGELOG|BACKLOG_ARCHIVE` references under `scripts/` |
| Did not execute | any script, any handoff trigger, any git mutation beyond the audit branch + this commit |

Read-only contract preserved; no handoff tooling, ADR, template, or sample modified.
