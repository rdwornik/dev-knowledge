---
date: 2026-05-19
type: audit
scope: dev-knowledge-posture
repos: [.dev-knowledge]
adrs: [ADR-28, ADR-35, ADR-38, ADR-42, ADR-51, ADR-53, ADR-54]
status: complete
mode: read-only
auditor: browser-chat-architect (Claude Opus 4.7)
---

# `.dev-knowledge` — Read-Only Audit

**Date:** 2026-05-19
**Auditor:** Browser-chat architect (Claude Opus 4.7)
**Mode:** Read-only — observations, findings, and reasoning only. No edits, no commits, no executable prompts.
**Subject:** `.dev-knowledge` governance, methodology, and decision-record posture, audited against principles articulated across the recent multi-chunk session arc.

---

## 1. Scope and Limits — Read First

**What this audit IS:**
- A structural assessment of `.dev-knowledge`'s governance posture against principles articulated in the recent session arc (anti-drift, layering, single-source, present-moment, standard-first, etc.)
- A surface of drift risks, coverage gaps, principle tensions, and meta-patterns observed across the session
- Witness-knowledge anchored — based on what the architect directly observed during the session and the contextual memory carried in

**What this audit IS NOT:**
- A file-by-file inspection of `.dev-knowledge`'s actual repository contents — the architect does not have read access to the operator's filesystem; verification against actual file state requires a follow-up session with Claude Code access
- An exhaustive review of every ADR, every LESSONS entry, every Council decision
- A prescriptive list of actions — by mandate read-only; the prioritization in Section 7 is input to the operator's decision, not a directive set

**Therefore each finding carries:**
- **Evidence** — what was witnessed or inferred from session context
- **Why it matters** — the impact / leverage assessment
- **Recommendation** — read-only proposal (input only)
- **Verify** — what next session would check against actual files

"**Unknown — verify against repo**" is used freely where the architect cannot verify directly. This is honest, not weak. The audit's value is in conceptual / structural depth, not file-state precision.

---

## 2. Posture Verdict (Executive Summary)

**Overall: `.dev-knowledge`'s governance posture is structurally sound and currently improving.** The ADR-53 / ADR-54 effort just closed a multi-month thread (per-repo agent-instruction contracts + Codex tool configuration) with the ecosystem in a cleaner state than before: three repos identical on CLAUDE.md v2.1, zero per-repo `AGENTS.md` in any repo, Codex reviewer config fully global. The methodology demonstrably worked under stress — a five-chunk effort across three repos, multiple Plan Mode revisions, an in-session reversal (thin-overlay → full retirement) driven by operator instinct, and a clean handoff process — without breaking discipline.

**Top strengths:**
- Decision-of-record discipline (ADRs) is healthy and reactive rather than speculative
- Drift-detection mechanism (Plan Mode + architect review + operator pushback) caught real issues this session: vault-writer drift pair, OneDrive corp-specific phrasing, time-bound clauses, the thin-overlay miss
- Standard-first sequencing with corrected stable-end-state phrasing is becoming established practice

**Top risks (five):**
1. **ARCHITECTURE.md freshness is now load-bearing for Codex review correctness, with no automated check.** ADR-54 routes Codex to ARCHITECTURE.md; ADR-51's codemap generator + CI freshness check is the open implementation item.
2. **ADR-38 auditor self-compliance gap** — the auditor fails its own checks. Foundational credibility risk.
3. **Sacred-files drift pattern across 9 canonical files** — explicit BACKLOG item identifying drift in the very files that ought to be drift-free.
4. **Lessons corpus is browse-only, not queryable.** With ~39 entries and growing, the lesson that would prevent a current mistake is the one nobody finds.
5. **ESSENTIALS lags recent ADRs 35–41** (and likely 42, 51, 53, 54). High-leverage cheat-sheet is stale.

**One emergent meta-pattern from this session:** time-bound clauses in governance docs ("to be retired in a follow-up chunk", "corp-monorepo not yet started") accumulate stale references. The principle "governance docs phrased as stable end-state; transient status lives in JOURNAL" emerged implicitly this session but is not yet codified. See Lessons (H3) and Tensions (T5).

---

## 3. Audit Framework — Principles Anchored

Quick reference. Findings below cite these by tag.

| Tag | Principle |
|---|---|
| **P1** | Single source of truth. Every rule has exactly one canonical home; pointers reference, do not restate. |
| **P2** | No drift pairs. Same content in two files is a drift surface regardless of current sync state. |
| **P3** | Layering / scope discipline. Generic → global; repo-specific → per-repo only when genuinely warranted. |
| **P4** | Layer 2 invariant. `.dev-knowledge` is methodology and governance; not orchestration. |
| **P5** | Universal self-containment of handoffs (ADR-42). Directives never target other repos. |
| **P6** | Decision-of-record discipline. ADRs codify decisions reactively, with N≥2 empirical grounding where applicable. |
| **P7** | Never delete content without asking. Condense and relocate allowed; remove rules requires explicit confirmation. Exception: deleting duplicates of canonical content where canonical is preserved. |
| **P8** | Append-only and immutable docs. Append-only: LESSONS, TOKEN-LOG, JOURNAL. Immutable: ADRs, audits, transcripts, handoffs. |
| **P9** | No big-bang restructures. Incremental, revertable changes; commits per file independently revertable. |
| **P10** | Standard-first sequencing. Standards ahead of repos OK transiently; phrased as stable end-state, not time-bound. |
| **P11** | Defer requires justification. "Later" without concrete reason is avoidance, not discipline. |
| **P12** | Present-moment focus. Trust the step after will be clear when reached. |
| **P13** | Verify destination before drop. When relocating or dropping content, confirm destination genuinely covers it. |
| **P14** | Claude Code builds, Codex reviews. Browser-chat architect designs prompts; never touches operator's filesystem. |
| **P15** | Plan Mode gates content-disposition. Destructive ops and relocation decisions go through Plan Mode. |
| **P16** | ARCHITECTURE.md is canonical structural source (ADR-51). Modules, layers, invariants live there. |
| **P17** | CLAUDE.md is per-repo instruction contract (ADR-53). v2.1 template; ~200-line ceiling; no per-repo AGENTS.md. |

---

## 4. Findings by Area

### Area A — ADR-53 / ADR-54 Effort Closure

**[INFO] A1 — Effort genuinely closed.** Cites: P1, P2, P17.
- *Evidence:* across the session, all three repos migrated to CLAUDE.md v2.1; `corp-monorepo/AGENTS.md` retired entirely (chunk B-prime, 5 commits including a bonus catch of a live script reference); global Codex config deployed at `~/.codex/AGENTS.md`; canonical source tracked at `.dev-knowledge/codex/AGENTS.md`; ADR-54 merged in `.dev-knowledge` at HEAD `c4d7c85`.
- *Why it matters:* positive — multi-month drift surface eliminated.
- *Verify:* `.dev-knowledge/codex/AGENTS.md` exists and matches deployed `~/.codex/AGENTS.md`; no repo has a per-repo `AGENTS.md`; ADR-54 frontmatter status is "accepted" or equivalent.

**[OBSERVATION] A2 — Per-repo `AGENTS.md` mechanism documented but currently unused.** Cites: P3.
- *Evidence:* ADR-54 retains the per-repo overlay mechanism in the model ("per-repo AGENTS.md for genuinely repo-specific review rules"); in practice no repo currently uses one.
- *Why it matters:* low and forward-looking. Not wrong (the mechanism is correctly a policy, not an inventory) but creates a tiny gap where a future contributor adding a per-repo overlay may not understand the layering relationship without reading ADR-54 in full.
- *Recommendation:* optional — the `codex/AGENTS.md` header note could be slightly strengthened with an "in practice currently unused" state pointer. Minor.
- *Verify:* read `.dev-knowledge/codex/AGENTS.md` header.

**[LOW] A3 — CLAUDE.md v2.1 condensation rationale not consistently captured.** Cites: P6.
- *Evidence:* the v2.1 template includes three documented condensations from prior versions (ADR list trimmed to last 5; scope tags reduced; per-file triggers dropped). The Stage 2 handoff sub-question asked whether the architect witnessed reasoning for these — Unknown across this session arc.
- *Why it matters:* low. The condensations were applied; the rationale may be in ADR-53 itself or a prior ADR.
- *Recommendation:* spot-check during next ESSENTIALS update; if rationale is genuinely undocumented (not merely session-unwitnessed), add to ADR-53 or the template frontmatter.
- *Verify:* read ADR-53 and CLAUDE.md template; confirm rationale present somewhere.

### Area B — ARCHITECTURE.md Governance Arc

**[HIGH] B1 — ARCHITECTURE.md freshness is load-bearing with no automated check.** Cites: P1, P2, P16.
- *Evidence:* ADR-54 instructs Codex to read each repo's `ARCHITECTURE.md` for structural context — this is now the load-bearing assumption for review correctness. ADR-51 specified the convention; the codemap generator and CI freshness check remain unbuilt per BACKLOG ("Codemap generator output specification — ADR-51 open item").
- *Why it matters:* HIGH. If `ARCHITECTURE.md` silently drifts from actual code structure (new modules, removed modules, refactored layers), Codex reviews against a stale model — either missing real issues or flagging non-issues. Severity rises with codebase change rate.
- *Recommendation:* prioritize the codemap generator + CI freshness check. Already named as Stage 2 OBJECTIVE for the next `.dev-knowledge` session.
- *Verify:* read ADR-51; check whether the codemap section format is already specified or absent.

**[MEDIUM] B2 — ADR-51 size-tiered policy (S vs M/L) not yet operationalized.** Cites: P16.
- *Evidence:* ADR-51's policy (M/L repos receive graphical codemap; S repos receive text-only module overview, no diagrams) is established but unimplemented. `.dev-knowledge` is S; ai-council is S; corp-monorepo is M/L.
- *Why it matters:* medium. Until built, the policy lives only in ADR text — no rendering, no enforcement, no per-repo example.
- *Recommendation:* fold into codemap generator scope; the tool must support both modes from the start, with `.dev-knowledge` as the dogfood test for the S mode.

### Area C — Sacred Files / Canonical Docs Coherence

**[HIGH] C1 — Sacred-files drift pattern across 9 canonical files.** Cites: P1, P2.
- *Evidence:* BACKLOG entry "Sacred-files maintenance enforcement (drift pattern across 9 canonical files)" — an explicit open item identifying drift in the very files that ought to be drift-free. The 9 files are not enumerated in session context; likely candidates: VISION, PLAYBOOK, ESSENTIALS, CLAUDE.md, ARCHITECTURE.md, BACKLOG, JOURNAL, LESSONS, plus one (taxonomy.yaml?). Exact list — Unknown — verify against BACKLOG entry detail.
- *Why it matters:* HIGH. If the canonical methodology docs drift among themselves, the methodology itself is unstable — the operator cannot trust any single doc as the source of truth.
- *Recommendation:* enumerate the 9 files explicitly; design a sacred-files coherence check that runs on commit or in CI, analogous in shape to the codemap freshness check. May warrant its own ADR if design choices are contested.
- *Verify:* `.dev-knowledge/BACKLOG.md` sacred-files entry detail; identify the 9 files; check for any existing coherence-check script.

**[MEDIUM] C2 — ESSENTIALS lags recent ADRs.** Cites: P6.
- *Evidence:* BACKLOG entry "ESSENTIALS.md cheat-sheet additions for ADRs 35-41". Implies ESSENTIALS misses 7 ADRs that have been merged. Likely also missing ADRs 42, 51, 53, 54 (all merged this session arc) — Unknown.
- *Why it matters:* medium. ESSENTIALS is the high-leverage cheat-sheet that new architects read first; if recent ADRs are absent, the most recent governance is invisible at first read.
- *Recommendation:* a tactical ESSENTIALS update pass covering ADRs 35-54. One focused session; smaller than codemap work.
- *Verify:* read ESSENTIALS.md; diff against ADR list in `docs/decisions/`; confirm the gap.

### Area D — Audit and Tooling Self-Compliance

**[HIGH] D1 — ADR-38 auditor fails its own checks.** Cites: P6, plus a foundational self-compliance principle.
- *Evidence:* BACKLOG entry ".dev-knowledge ADR-38 self-compliance gap — `src/` + `pyproject.toml` (auditor fails own checks)".
- *Why it matters:* HIGH. An auditor that cannot pass its own audit undermines the credibility of any audit it produces. The principle "we audit ourselves first" is broken if the audit tool's home repo fails the audit.
- *Recommendation:* prioritize. The fix may be small (add `src/` layout + `pyproject.toml`) but the credibility-restoration value is large.
- *Verify:* `.dev-knowledge` root layout; presence of `src/`, `pyproject.toml`.

**[LOW] D2 — check_backlog_organization regex false-positive.** Cites: tool reliability.
- *Evidence:* BACKLOG entry "Audit tool check_backlog_organization — code-span-aware done-token regex (false-positive fix)".
- *Why it matters:* low — tool false-positives are noise, not structural risk.
- *Recommendation:* queue with other tooling fixes; no urgency.

**[INFO] D3 — Bonus discovery this session: hard-coded reference lists in live scripts are drift surfaces.** Cites: P2.
- *Evidence:* chunk B-prime's report noted Plan Mode caught `scripts/check_doc_refs.py` carrying `AGENTS.md` in its DOCS list — a live script reference that would have broken after deletion if not caught. Bonus commit handled it.
- *Why it matters:* not a `.dev-knowledge` finding directly (the script was corp-monorepo's) but the pattern generalizes — **any live script maintaining a hard-coded list of canonical files, ADR numbers, or doc names is a drift surface** when the underlying set changes.
- *Recommendation:* grep `.dev-knowledge/scripts/` (or wherever audit / hook scripts live) for hard-coded file / ADR / canonical-doc references. Each is a small drift surface.
- *Verify:* grep result.

### Area E — Lessons / Knowledge Retrieval

**[MEDIUM] E1 — Lessons corpus growing without indexing / retrieval.** Cites: P6 (decisions of record must be retrievable).
- *Evidence:* ~39 LESSONS entries per session memory; BACKLOG entry "Lessons activation P1 implementation (lessons-index.json + retrieval + querying per ADR-35)".
- *Why it matters:* medium and rising. As LESSONS grows, browse-only access becomes less useful — the lesson that would have prevented a current mistake is the one nobody finds. ADR-35 anticipated this; the implementation gap leaves the principle aspirational.
- *Recommendation:* design the index + retrieval as its own focused multi-chunk effort (index schema → generator → query CLI → CI freshness). Same shape as codemap generator; could follow it.
- *Verify:* count LESSONS entries; confirm no `lessons-index.json` exists yet.

**[MEDIUM] E2 — Council decisions retrievability.** Cites: P6.
- *Evidence:* ~25 Council decisions per session memory. This session itself surfaced a retrieval cost — "ADR-54 point 5 said retired" required Plan Mode to load and read the ADR text rather than being a quick lookup.
- *Why it matters:* medium. Council decisions are a parallel canonical-source corpus to ADRs and LESSONS. If hard to query, contradictions go undetected (see F1) and prior reasoning gets re-litigated.
- *Recommendation:* extend lessons-index design to Council decisions, or sibling council-index. Cross-stream P1 BACKLOG item "Council decisions management consolidation" already exists.

### Area F — Contradiction Detection / Cross-Decision Coherence

**[HIGH] F1 — Council decisions contradiction detection unbuilt.** Cites: P6 (coherence is foundational to decision-of-record discipline).
- *Evidence:* BACKLOG entry "Council decisions management consolidation (contradiction detection + ownership model sub-items remain)".
- *Why it matters:* HIGH. With 25+ Council decisions and 22+ ADRs accumulated, the surface for contradictions or near-contradictions is real. This session surfaced one such tension: ADR-54's point 3 ("per-repo overlays allowed for repo-specific rules") versus point 5 ("corp-monorepo/AGENTS.md to be retired") — the thin-overlay chunk B leaned on point 3; the eventual delete (chunk B-prime) honored point 5. The contradiction was *internal to ADR-54 itself*. Without detection tooling, these surface only when execution forces them.
- *Recommendation:* prioritize. Detection design is non-trivial (semantic, not just text matching) but cost of NOT having it grows non-linearly with corpus size. Plausible candidate for the first LLM-assisted governance tool in the ecosystem.
- *Verify:* BACKLOG entry detail; any existing contradiction-detection prototype.

### Area G — Universalization Patterns

**[MEDIUM] G1 — Skills universalization across repos open.** Cites: P3.
- *Evidence:* BACKLOG entry "Skills universalization across repos". The same pattern just resolved with `AGENTS.md` (global vs per-repo) applies to Claude Code skills — `~/.claude/skills/` global plus `<repo>/.claude/skills/` per-repo for genuinely repo-specific. Per session memory, `corp-monorepo/.claude/` already holds project-specific skills tracked in git.
- *Why it matters:* medium. Same drift surface as `AGENTS.md` had before ADR-54. The principle is now well-tested; the application is the next natural step.
- *Recommendation:* design a "skills-global" ADR following the ADR-54 template (canonical source tracked in `.dev-knowledge`, deployed to `~/.claude/skills/`, per-repo only for genuinely repo-specific). Lower risk than ADR-54 because the model is established.

**[MEDIUM] G2 — Hooks audit + consolidation open.** Cites: P2, P3.
- *Evidence:* BACKLOG entry "Hooks audit + consolidation". Per session memory, SessionStart / Stop hooks exist (`/boot`, `/evolve`); coverage and consistency unverified.
- *Why it matters:* medium. Hooks run silently; drift in them is particularly hard to notice — they fail in ways that look like environmental flakiness rather than coverage gaps.
- *Recommendation:* scope-bound audit chunk after current priorities settle. Tool inventory + drift check.

**[MEDIUM] G3 — Phase 2 universalization rollout half-done.** Cites: P10 (standard-first; rollout must close).
- *Evidence:* BACKLOG entry "Phase 2 universalization rollout (ai-council substantially complete; corp-monorepo not yet started)".
- *Why it matters:* medium. Asymmetric rollout across repos is a transient inconsistency that becomes permanent if not closed.
- *Recommendation:* clarify what Phase 2 includes (Unknown from session context); identify the corp-monorepo work and either schedule or explicitly defer with justification per P11.

### Area H — Process / Methodology (Lessons Observed)

**[INFO] H1 — Multi-chunk session demonstrated method works under stress.** Cites: P9, P15.
- *Evidence:* the just-closed effort spanned 5 chunks across 3 repos, multiple Plan Mode revisions, an in-session reversal (thin-overlay → full delete), and a successful handoff process — without breaking discipline (no commits to wrong repo after the initial mix-up; no destructive deletions without Plan Mode + operator approval; no big-bang restructures; all working trees clean at the end).
- *Why it matters:* positive evidence that the methodology scales to multi-chunk multi-repo work.
- *Recommendation:* operator-driven JOURNAL or LESSONS entry capturing the validation. (LESSONS is append-only — entry must come from the operator.)

**[LESSON] H2 — Operator's consistent instinct is data, not noise.** Cites: P12.
- *Evidence:* across the entire effort the operator's stated direction was "AGENTS global, not for corp-monorepo." Plan Mode (chunk B) proposed thin-overlay as a defensible reading of ADR-54 point 3. Architect approved without flagging the deviation from ADR-54 point 5 ("retired") AND from the operator's consistent multi-session instinct. Operator's pushback ("nie rozumiem dlaczego plik AGENTS nadal jest w rootie") triggered re-analysis and the cleaner end state (chunk B-prime).
- *Why it matters:* process-level. When the operator's instinct is consistent across a multi-session effort AND the implementation deviates from it, the consistent signal should weigh more heavily than per-step plan defensibility. Per-step plans can be locally defensible AND collectively suboptimal.
- *Recommendation:* operator-driven LESSONS entry.

**[LESSON] H3 — Time-bound clauses in governance docs accumulate stale references.** Cites: P10.
- *Evidence:* this session caught three instances: the "known violations → 0" parenthetical implying corp-monorepo special-case; "to be retired in a follow-up chunk" in the ARCHITECTURE.md fix that chunk A produced; framing patterns like "corp-monorepo not yet started" in BACKLOG. Each was correct at writing time and stale at reading time.
- *Why it matters:* a documentation-craft principle worth codifying. Governance docs describe end-states; transient status (what's done / pending) lives in JOURNAL or a rollout-tracker.
- *Recommendation:* explicit principle added to PLAYBOOK — "Governance docs phrased as stable end-state; transient status lives in JOURNAL." Could be a short ADR or PLAYBOOK addition with N≥2 grounding (the three instances above).

**[LESSON] H4 — "Verify destination before drop" pattern earned its keep.** Cites: P13, P15.
- *Evidence:* chunk B's feedback explicitly asked Plan Mode to confirm `corp-monorepo/ARCHITECTURE.md` covered each sub-part of the dropped "Architecture Context" section. Plan Mode performed the verification; nothing was lost. Chunk B-prime applied the same — confirmed the vault-writer invariant lived in ARCHITECTURE.md before deleting the pointer.
- *Why it matters:* small but reliable safety guard. Worth being a standard prompt-template line, not a per-prompt insertion.
- *Recommendation:* PLAYBOOK addition — "When relocating or dropping content, Plan Mode confirms destination genuinely covers it." Likely already implicit; explicit codification helps.

### Area I — ADR Hygiene

**[MEDIUM] I1 — ADR relationship map / index Unknown.** Cites: P6.
- *Evidence:* 22+ ADRs accumulated. ADRs cited across this session include 27, 35, 38, 42, 51, 53, 54. Their relationships (supersession, dependency, clarification) are clear to the architect having lived through them; they may not be navigable for a fresh reader.
- *Why it matters:* medium. New contributors reading ADRs in sequence miss relationship structure — which ADR supersedes which, which clarifies which, which depend on which.
- *Recommendation:* an ADR index doc or graph (DOT / mermaid) showing supersession and dependency edges. Could be machine-generated from ADR frontmatter if ADRs carry `supersedes:` / `related:` fields. Same shape as codemap.
- *Verify:* `.dev-knowledge/docs/decisions/` contents; ADR frontmatter conventions.

**[LOW] I2 — ADR-42 amendment open.** Cites: P5.
- *Evidence:* BACKLOG entry "ADR-42 amendment — single vs multi-artifact handoff format clarification".
- *Why it matters:* low — ADR-42 worked in practice this session (Stage 2 response flowed into bundle cleanly). The clarification likely addresses an edge case not encountered here.
- *Recommendation:* defer until a real instance forces the clarification. Per P11, defer is justified — concrete trigger absent.

### Area J — Stream Taxonomy

**[INFO] J1 — Cross-stream bucket exceeds 33% — taxonomy health signal.** Cites: P6.
- *Evidence:* BACKLOG entry "Stream taxonomy grooming — Cross-stream exceeds 33% kill criterion (deferred to 2026-07-01 quarterly grooming)".
- *Why it matters:* low-medium (deferred per quarterly cadence). But notable: when Cross-stream exceeds its kill threshold, it usually means primary stream categories (A/B/C) are too narrow OR the methodology has matured beyond the original stream model. Either way, grooming should re-examine whether the streams are still the right cut.
- *Recommendation:* leave deferred per operator's cadence. At grooming time ask "are streams still the right categorization?" rather than just rebalancing.

---

## 5. Tensions Between Principles

Pairs of principles that can collide in specific situations. Surfacing them so the next architect does not re-discover.

**T1 — "Never delete content" (P7) vs "Single source of truth" (P1).**
*Situation:* eliminating a drift pair requires deleting the duplicative copy.
*Reconciliation:* P1 takes precedence WHEN the deletion targets a duplicate of canonical content that is preserved elsewhere. Tested this session (vault-writer pointer deletion; corp-monorepo `AGENTS.md` deletion). Codification useful — explicit "no-delete exception for duplicates of canonical content."

**T2 — "No new ADR without N≥2 grounding" vs "Decision-of-record discipline" (P6).**
*Situation:* a decision is genuinely new but encountered only once.
*Reconciliation:* N≥2 prevents PATTERN extraction without evidence ("we keep needing this rule"). A single architectural CHOICE with no prior precedent can be an ADR-with-N=1 because the choice itself is the record, not a pattern claim. ADR-54 itself is an example — a singular decision about Codex config placement, recorded because the choice deserved a record. Worth explicit articulation in PLAYBOOK.

**T3 — "Universal self-containment of handoffs" (P5) vs "External dependencies in play."**
*Situation:* real cross-repo work is in flight at handoff time.
*Reconciliation:* directives never target other repos (handoff produces only own-repo directives); factual state observations CAN reference other-repo state, marked Unknown / Verify if not directly observed. Tested this session — REALITY section of Stage 2 marked corp-monorepo as external dep with state Unknown. Works.

**T4 — "Present-moment focus" (P12) vs "Forward-planning ADRs" (P6).**
*Situation:* ADRs by nature codify decisions for future application; present-moment focus says trust the next step.
*Reconciliation:* ADRs are REACTIVE records (decision made now, recorded now, applied as encountered), not PREDICTIVE (we will decide X later). If `.dev-knowledge` carries any ADRs that codify speculative future decisions, those are inverted ADRs and should be either grounded in present need or retracted.
*Verify:* scan ADR titles / abstracts for speculative phrasing ("we will...", "in the future...", "to be applied when...").

**T5 — "Standard-first sequencing" (P10) vs "Stable end-state phrasing."**
*Situation:* writing the standard before the repos conform means the standard describes the target.
*Reconciliation:* standards describe end-state independent of conformance status. Conformance status (which repos have rolled out) lives elsewhere (BACKLOG / JOURNAL / a rollout-tracker). Tested and violated this session — the ARCHITECTURE.md "to be retired in a follow-up" wording was a tension violation; the corrected stable phrasing resolved it. See H3.

**T6 — "Defer requires justification" (P11) applies to the architect's own recommendations.**
*Situation:* architect can be tempted to recommend "in next session" / "later" without concrete reason.
*Reconciliation:* when no concrete dependency / scope mismatch / cognitive-load reason exists, the recommendation is "now" or silence. Operator's preferences make this explicit; architect must apply it to self with the same strictness as to operator.

---

## 6. What This Audit Did NOT Cover

**File-state verification.** Audit is witness-based, not file-based. A follow-up audit with Claude Code access should verify:
- ADR frontmatter conventions and supersession links
- Exact LESSONS.md count, most-recent entry date
- Presence of `pyproject.toml` and `src/` layout (ADR-38 self-compliance)
- The 9 sacred files (enumerated from BACKLOG)
- ESSENTIALS.md ADR coverage diff against actual ADR list
- Exact text of recent JOURNAL entries
- `~/.codex/config.toml` contents (mentioned briefly this session, not verified)
- pre-commit hook coverage in `.dev-knowledge`

**Content of cited ADRs.** Treated ADRs by their session-witnessed role, not by their full text. ADR text may contain provisions not surfaced here.

**Test / CI state.** No verification of pytest counts, CI green status, or hook execution. `.dev-knowledge` is primarily doc + some scripts; smaller surface than corp-monorepo.

**Cross-repo deep audit.** Audit is `.dev-knowledge`-focused per the operator's request. Cross-repo state noted where relevant but not deeply audited.

**Individual ADR review.** No ADR was reviewed for internal consistency, age, or supersession status. The contradiction-detection finding (F1) flags this as a structural gap; this audit does not substitute for it.

**Council decisions deep dive.** ~25 decisions referenced collectively but not individually.

**Skill / hook inventory.** `~/.claude/` and per-repo `.claude/` not inventoried; flagged in G1, G2.

---

## 7. Recommended Prioritization

Ranked by leverage. Read-only audit — sequencing is the operator's call.

**Tier 1 — Highest leverage**
1. **Codemap generator + CI freshness check** (B1) — load-bearing for ADR-54 review correctness; matches Stage 2 OBJECTIVE for the next session
2. **ADR-38 auditor self-compliance fix** (D1) — credibility-restoring; likely small fix
3. **Sacred-files coherence check** (C1) — addresses drift in the most-important files

**Tier 2 — Structural quality**
4. **Council decisions contradiction detection** (F1) — corpus-scale risk; non-trivial design
5. **Lessons activation P1** (E1) — addresses knowledge-retrieval decay
6. **ESSENTIALS update for ADRs 35–54** (C2) — small tactical pass; high leverage per effort

**Tier 3 — Extensions of established patterns**
7. **Skills universalization** (G1) — apply ADR-54 pattern to skills; lower risk now
8. **Hooks audit** (G2) — scope-bound, manageable
9. **ADR relationship index** (I1) — supports F1 and general navigability

**Tier 4 — Deferred / scheduled**
10. **Stream taxonomy grooming** (J1) — 2026-07-01 quarterly
11. **ADR-42 amendment** (I2) — defer until forced
12. **check_backlog_organization regex** (D2) — queue with tooling fixes

**Process / codification candidates (small PLAYBOOK or LESSONS entries)**
13. Time-bound clauses in governance docs principle (H3)
14. "Verify destination before drop" principle (H4)
15. "Operator's consistent instinct is data" lesson (H2)
16. No-delete exception for canonical-source duplicates (T1 codification)
17. ADR-with-N=1 valid for singular choices (T2 codification)

---

## 8. Closing

This audit was produced read-only, without access to `.dev-knowledge`'s actual file contents. Its value is in the structural / principle-level mapping of where governance is strong, where it has gaps, and where principles can tension. The next session — or any session with Claude Code access — can use this document as input to a file-state audit verifying each finding against ground truth.

The methodology came through the just-closed session arc intact and arguably stronger: the methodology itself caught the operator-instinct-vs-plan-defensibility miss and produced a cleaner end state. The dominant near-term theme is **automation of freshness checks** — codemap freshness, sacred-files coherence, lessons retrieval, contradiction detection — the same anti-drift principle that drove ADR-53 / ADR-54 applied to the remaining manually-maintained governance surfaces. The first one (codemap) is already the next session's OBJECTIVE per the Stage 2 handoff. The rest form a multi-session arc whose internal logic is consistent with what just shipped.

---

*End of audit.*
