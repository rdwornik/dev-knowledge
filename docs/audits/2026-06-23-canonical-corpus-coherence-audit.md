# Canonical-corpus coherence & staleness audit — 2026-06-23

<!-- scope: meta -->

> **Read-only diagnostic audit** of the canonical methodology corpus — the prompt's named seven:
> `protocols/PLAYBOOK.md` (3352 L), `protocols/ESSENTIALS.md` (448 L), `protocols/DEFINITION_OF_DONE.md`
> (91 L), `protocols/HANDOFF_PROCESS.md` (574 L), `protocols/HANDOFF_BOOT.md` (121 L), `ARCHITECTURE.md`
> (574 L), `CLAUDE.md` (185 L). **DIAGNOSTIC ONLY — no audited file was edited; the only writes this arc
> made are this report + a one-line JOURNAL wrap.** It produces a *candidate list*; the cleanup is a
> separate, rule-by-rule-approved arc. Immutable per repo convention (supersede with a new dated file;
> never edit in place).
>
> **Confidence discipline.** **MACHINE-VERIFIED** = a command (`test -e` / `grep` / `ls` / `pytest` /
> `audit.py`) was run and is named in the evidence. **JUDGMENT** = reasoned from text, not machine-
> confirmed. Maps to the Witnessed / Doc-asserted / Confirm-live grading of the 2026-06-19 precedent.
>
> **Method.** 12 read-only Explore agents (8 PLAYBOOK section-agents + ESSENTIALS-with-DoD + CLAUDE +
> ARCHITECTURE + HANDOFF-pair), a Phase-0 machine baseline, an orchestrator cross-file synthesis with
> **orchestrator re-verification of every high-impact MACHINE-VERIFIED agent claim** (§6). Locators are
> content-signatures; line numbers are **as-of-audit and drift** — the BACKLOG's own #77 line refs are
> already stale.

---

## 0. Headline

**The corpus is structurally healthy, not rotting.** `audit.py health` is GREEN; every audited file was
edited within the last week; the machine baseline shows 5/5 doc→code edges resolved and the one declared
reconciliation edge (`handoff-process@5.2`) matching. The rot that exists is **referential and editorial**
(stale *content* inside fresh files), not abandonment — and most of it is **already tracked** in BACKLOG.

**The single biggest integrity finding is methodological, not a doc defect: agent "MACHINE-VERIFIED" claims
are not self-certifying.** Orchestrator re-verification **refuted six high-impact dead-reference findings**
(§6) — ADR-72/73, the `/verify` skill, `surface-closures.ps1`, `docs/research/`, the pytest count, the
Codex protocol — every one because an agent ran a real command **in the wrong scope** (only `scripts/`, not
`~/.claude/hooks/`; `SKILL.md` not `verify.py`; one repo, not the ecosystem). **Any future cleanup must
re-confirm-live before acting on a removal.** This is the load-bearing lesson of the audit.

**The genuinely actionable, high-confidence items are few and known:** one dead *procedure* to cut
(PLAYBOOK tier-transition subsection), three stale *labels/paths* to correct (L855 "v4 bundle", the
`docs/archive/tech-radar/` path, the L2929 self-declared STALE marker), one unenforced-but-asserted rule to
promote (the `Decommission:` field), the ESSENTIALS over-length (448 L vs its own "~1 page" contract), and
the CLAUDE.md §4/§5 duplication + §5 self-contradiction — all already carried as #77 / #157 / #112 / #199.
The lesson→rule "three divergent statements" that #77 names are **already reconciled** to one canonical
statement + two pointers.

**Coherence picture:** low fragmentation. The corpus mostly *points* rather than *restates*
(ESSENTIALS L360→DoD, PLAYBOOK §8→HANDOFF_PROCESS, PLAYBOOK §13→§4 are all correct pointer patterns). The
duplication that remains is intra-CLAUDE.md (§4/§5) and a few teaching-vs-authority overlaps — condense
targets, not contradictions.

---

## 1. Phase-0 machine baseline (the hard-evidence floor)

All read-only; captured 2026-06-23 on `audit/canonical-corpus-coherence` (based on `main` 9ebef41).

- **`python scripts/audit.py health` → `health: OK`** (no FAIL). Standing WARNs, all **known**:
  - `git_backlog_drift`: `#77` closed-in-`77e5d7df9` but still in BACKLOG (the CLOSURE-VOIDED item).
  - `no_ff_merges`: two FF/direct commits on `main` — `3a894eeb5`, `d0f9ead67` (both 2026-06-19). **Already
    grandfathered** via `ecosystem/disposition-register.yaml`, operator-ratified 2026-06-20 (merge
    `0941855`). Not a live defect — the invariant holds going forward (`git log --first-parent` shows only
    `--no-ff` merges since).
  - `doc_rot`: BACKLOG `#164` / `#77` / `#134` history-accretion (known grooming backlog).
  - `handoff_probes`: P1a/P1b/P8 skipped in the 2026-06-21 bundle (tools `grep`/`sed`/`ls` absent —
    environmental, not a doc defect).
  - `handoff_tag_canonicity`: "§3.1 not found (consolidated) — nothing to lint" (the v4 tag-lint surface is
    legitimately gone).
- **`doc_code_edge`: 5/5 resolved, none broken** — `seal-journal-anchor`, `canonical-freshness`,
  `coherence-spec-reconciled`, `coherence-amendment`, `governance-backlog-schema`. Declaration docs =
  PLAYBOOK + DEFINITION_OF_DONE only. Deferred gaps tracked as #201 (two-organ) / #202 (Tier-3).
- **`reconciled_versions`: 1 edge, matches** — `docs/handoffs/README.md → handoff-process@5.2`.
- **`doc_claims`: match** — incl. `pytest_collected` (doc **793** / actual **793**, re-confirmed by
  orchestrator `pytest --collect-only` = 793).
- **`doc_structure`: OK** — the §18 numbering gap is **allowed** via a `structure-allow` marker (the
  2026-06-19 audit's §18 finding was dispositioned, not a live defect).
- **`scan_undeclared_edges`: 12 `→handoff-process` undeclared edges** across ARCHITECTURE / CLAUDE /
  CONTRIBUTING / VISION / ESSENTIALS / PLAYBOOK / BOOT / SESSION_SETUP / AI_COUNCIL_PROCESS + 2 templates —
  the **known #172/#199 coherence-spine gap** (only `docs/handoffs/README.md` declares the edge today).
- **Per-file staleness clock:** all 7 fresh — PLAYBOOK / ESSENTIALS / DoD / ARCHITECTURE 2026-06-22;
  CLAUDE 2026-06-21; HANDOFF_PROCESS 2026-06-17; HANDOFF_BOOT 2026-06-18.

**In-flight overlap (must not double-count):** a same-day comprehensive HANDOFF_PROCESS audit
(`docs/audits/2026-06-23-handoff-process-audit-findings.md`, KEEP 12 / CUT 6 / ADD 3) exists on sibling
branch `feat/legibility-graph-conformance` (commit `31e0cd2`), **not yet on `main`**. The HANDOFF section
below cross-refs it rather than re-deriving it.

---

## 2. Cross-file findings (the coupling worklist — the audit's centerpiece)

**C1 — Lesson→rule "three divergent statements" (#77): ALREADY RECONCILED.** `grep` confirms exactly one
full canonical statement — PLAYBOOK §4 "When a lesson becomes a rule" (L2295, *"a lesson that sounds like
'always do X'… when a lesson matures into a rule: [3 steps]"*) — plus **two pointers**: PLAYBOOK §13 (L2908,
"See §4… for the canonical trigger + 3-step process") and ESSENTIALS (L415, same pointer). **#77's cited
refs (L1687/L2318/L393) are stale**; the divergence they name no longer exists. *Verdict: this sub-item of
#77 is effectively DONE; record it so the cleanup arc doesn't re-do it.* **MACHINE-VERIFIED** (`grep -nE
"becomes a rule|matures into a rule"`). backlog: #77.

**C2 — ADR-85 single-source triangle (DoD ↔ ESSENTIALS ↔ ADR-85): COMPLIANT.** ESSENTIALS L360 carries a
blockquote-summary of the journal-anchor closure rule **followed by an explicit "Canon:
`protocols/DEFINITION_OF_DONE.md`" pointer** — the correct summarize-then-point pattern. No other ESSENTIALS
spot *declares* the closure rule. DoD's `<!-- rule: seal-journal-anchor -->` resolves to
`session_end_backpressure.py` (baseline: edge resolved). *Verdict: KEEP — this is the template the rest of
the corpus should match.* **MACHINE-VERIFIED**. backlog: #77/#5 (ESSENTIALS trim is separate, C7).

**C3 — CLAUDE.md append-only authority (#157 + #112): CONFIRMED, two coupled defects.** (a) §4 "File
lifecycle" bullet (L54) **and** §5 Critical-rules #1–3 (L69–71) *both* authoritatively define the
append-only/immutable disposition → **duplicate authority** (#157, serialize-group claude-md). (b) §5 rule
#3 says immutable artifacts may be superseded "with a new file **or in-file marker**; never edit in place" —
but ADR-77 + #112 move ADRs to **helper-only** amendment (`adr_amend.py` the sole writer,
`block_immutable_edits.py` denies all other in-place edits). #112's own text names this "the CLAUDE.md §5
self-contradiction". *Verdict: CONDENSE §5 #1–3 to a pointer to §4 (single authority) + UPDATE §5 #3's
"or in-file marker" once #112 ships.* **MACHINE-VERIFIED**. backlog: #157, #112 (both edit §5 → serialize).

**C4 — PLAYBOOK §7 polish (#67): still OPEN, not a new defect.** The skill/command **naming-convention**
note exists (the rule-ID naming subsection); the **orchestrator/worker how-to** for subagents is thin. This
is the tracked #67 gap, not a defect to surface fresh. *Verdict: leave to #67.* JUDGMENT. backlog: #67.

**C5 — Organ-list DoD (PLAYBOOK ~1484) vs closure-gate DoD (DEFINITION_OF_DONE.md): COHERENT, distinct
scopes.** PLAYBOOK "Definition of done (organs)" is the ADR-81 feature-lifecycle (methodology-home +
deployment-path + cadence + deployment-or-deferral); DoD is the ADR-85 session-close gate
(JOURNAL/BACKLOG). Different scopes, no contradiction — but PLAYBOOK's "Definition of *shipped*" (~1500)
restates a 6-point checklist whose point-6 is "operator-enforced until #147". *Verdict: KEEP + recommend a
one-line cross-ref at ~1500 pointing the session-gate half to DoD, to lower drift risk.* JUDGMENT.
backlog: #147 (the deferred ship-gate).

**C6 — doc→code unenforced edge (#194/#201/#202): no new gaps.** The 5 enforced rules resolve; the
asserted-but-unenforced candidates the agents flagged all map to the **known** deferred set — two-organ
(#201: `governance-no-ff`, `governance-child-floor`, `governance-backlog-leave`) and Tier-3 (#202:
`handoff-probes-bind`, `coherence-doc-claims/-rot/-structure`). *Verdict: nothing new; do not surface as
fresh.* MACHINE-VERIFIED (baseline + `ecosystem/doc-code-edge.yaml`). backlog: #194/#201/#202.

**C7 — ungated-doc staleness + conformance dashboard (#169/#171): ARCHITECTURE pointer pending = KEEP-known.**
`ecosystem/conformance.md` does not exist yet (`test -e` absent); ARCHITECTURE Ch2's missing pointer is the
**intentional** pending state ("lands with the build #171, not before"), not a defect. *Verdict: KEEP-known.*
MACHINE-VERIFIED. backlog: #169/#171.

---

## 3. Per-file findings

### 3.1 PLAYBOOK.md

**Confirmed REMOVE / UPDATE (high confidence):**
- **PB-A `Tier transition procedures` subsection (~818) — dead DEPRECATED procedure kept in-document.**
  Marked "DEPRECATED 2026-05-23"; describes a tier-transition flow that no longer exists (tier system
  deprecated). Distinct from the load-bearing inline tier-deprecation *context notes*. **REMOVE-candidate.**
  MACHINE-VERIFIED. prior-audit §4. backlog: #77 (protocols consolidation).
- **PB-B `| docs/handoffs/YYYY-MM-DD-*/ (v4 bundle) |` table label (L855)** — labels the format "(v4
  bundle)" though v5.2 is canonical; L960 already marks v4 historical, so the table label is the stale
  surface. **UPDATE** (tag "(v4 bundle, historical)" or demote). MACHINE-VERIFIED.
- **PB-C `docs/archive/tech-radar/` path (~1637)** — PLAYBOOK states tech-radar "archived to
  `docs/archive/tech-radar/`", but that subdir is **absent** (`test -e` fail; `docs/archive/` holds dated
  research-note `.md` files, no `tech-radar/`). **UPDATE** the path claim. MACHINE-VERIFIED.
- **PB-D L2929 self-declared STALE marker (§14 Markdown Governance)** — *"> STALE — Handoff and
  Snapshots/reports rows…"* The doc admits its own staleness: the Handoff row predates the folder format,
  and the Snapshots "delete after 90 days" lifecycle "does not match practice (audits kept indefinitely)".
  **UPDATE** the table. MACHINE-VERIFIED. (PB8-01 + PB8-07.)

**CONDENSE (judgment, operator-gated):**
- **PB-E ~19 "CHANGELOG.md retired (ADR-49)" inline annotations** → state once in Markdown Governance,
  drop the scattered reminders (the regression-guard survives in the canonical statement). prior-audit §4.
- **PB-F "two-documents-glued" structure** — un-numbered reference chapters (first half) then numbered
  §1–§19 recipes (second half), mixed ToC scheme. Structural condense; the §18 gap itself is **allowed**
  (KEEP). prior-audit §2.
- **PB-G Hooks "auto vs manual" table (~1693) drift** — omits `toc-freshness`, `toc-freshness-playbook`,
  `coherence-nudge`, `block-ff-push` (live in `.pre-commit-config.yaml` + CLAUDE §9); its version-stamp
  reads 2026-06-01. The table itself says "the filesystem wins — re-ground before trusting"; it has
  drifted. **UPDATE/re-ground.** MACHINE-VERIFIED. backlog: #77.
- **PB-H Quick-reference model/mode/effort examples table (~2170)** + **model/platform pins (~2118, stamped
  2026-06-07)** — accurate but version-dated; add a `last-verified` marker, condense the 10-row example
  table. JUDGMENT.

**Minor UPDATE (provenance / internal pointers):**
- **PB-I [TBD — Stream C session 3, ADR-33/34] placeholders (~494/501)** — ADR-33/34 now exist; the
  placeholders are stale forward-pointers. **UPDATE/resolve.** prior-audit §5.
- **PB-J decision-fatigue threshold "observed empirically from 2026-04-24"** (predates the JOURNAL window) →
  reword to "working threshold" to avoid false precision. JUDGMENT.
- **PB-K "PLAYBOOK Section 6 Continuous Improvement" internal cross-ref (~1870)** — Continuous Improvement is
  an un-numbered section, not "§6" (which is Code Review). Minor broken internal pointer. **UPDATE.**

**KEEP (verified healthy or already-fixed):**
- §9 Weekly Review — **already updated 2026-06-19**: the `/evolve` step was dropped, replaced by the
  `corrections.jsonl` Stop-hook note (L2752); `/boot`+`/evolve` consolidated into one "Retired machinery"
  note (L1784) with command-tables cleaned — **the prior audit's exact recommendation, implemented.** Not
  hollow. MACHINE-VERIFIED.
- ADR-87 prompt-skeleton — the architect/CC `[A]`/`[CC]` tags were added (commit `34e1ff4`); the
  2026-06-19 §3 contradiction is **resolved.** MACHINE-VERIFIED.
- Worktree-discipline / "no leftovers" (~1084–1356) — enforced by `check_no_sibling_orphans`; exemplary
  dual-layer (process + gate). KEEP.
- The enforced-rule teaching subsections (`canonical-freshness` ~882, `coherence-amendment` ~897,
  `coherence-spec-reconciled` ~907, `governance-backlog-schema` ~2766) — correctly annotated + resolved.

**PROMOTE-to-enforcement:**
- **PB-L "Supersession & decommissioning" `Decommission:` field rule (~933)** — stated as MUST ("a
  non-empty `Decommission:` field becomes a BACKLOG item until removed"), but **no detector** (`grep
  Decommission scripts/audit.py` = 0 hits). The field is in the ADR template (observed in practice) but the
  cleanup loop is unenforced. **PROMOTE-to-enforcement.** MACHINE-VERIFIED. prior-audit §8. backlog: #199.

### 3.2 ESSENTIALS.md + DEFINITION_OF_DONE.md

- **ED-A ESSENTIALS is 448 lines against its own "~1 page / condensed-by-design" contract (L9).** The
  headline ESSENTIALS finding; the trim is the substance of #77's "trim ESSENTIALS" sub-item. CONDENSE map
  (agent ED's estimate ~200 L recoverable): JOURNAL-procedure detail → pointer; the ADR-87 skeleton detail →
  PLAYBOOK pointer; the commit-message standard → CONTRIBUTING pointer; "How Claude thinks" / epistemic-
  discipline blocks → trim to lens-lines. **CONDENSE.** MACHINE-VERIFIED (`wc -l`). backlog: #77, #5.
- **ED-B ESSENTIALS L154 cites "ADR-45 Stage 3 verification" as a mechanical cross-check that was never
  built.** ADR-45 *exists* (so not a dead ADR ref) but its Stage-3 shared validator was never implemented
  ("explored but not adopted"); ESSENTIALS L167 itself admits "enforcement is operator review only". L154's
  "mechanical cross-check" promise is aspirational. **UPDATE** L154 to match L167's honest admission.
  JUDGMENT. prior-audit §6.
- **ED-C ESSENTIALS L340 "Declare a rule at its authoritative source, never in a summary" vs ESSENTIALS's
  own restatements.** The meta-rule is correct; ESSENTIALS includes it (for daily reference) while itself
  restating several rules to teach. **CONDENSE / scope-clarify** (the rule binds *enforced code-checked*
  rules; working summaries may restate-then-point). JUDGMENT.
- **ED-D DoD embeds two amendment narratives (L33–99).** The 2026-06-16 / 2026-06-19 amendment history sits
  in the derived gate-spec; per ADR-49 (changelog-in-git) it belongs appended to ADR-85, leaving DoD a clean
  current-state statement. **CONDENSE.** JUDGMENT.
- **ED-E DoD scope-freeze "until ~2026-07-14" is in-window** (21 days remain as of 2026-06-23); not machine-
  watched, but that's the documented grace period. **KEEP**; surface a signal when it expires. MACHINE-
  VERIFIED (date arithmetic).
- **KEEP:** ESSENTIALS L360 closure-rule pointer (C2, the good pattern); the L238 `⚠️ SUPERSEDED`
  parallel-sessions banner (the supersession template to preserve); DoD `/override` reference (`test -e
  .claude/commands/override.md` ✓); DoD "NOT gated" list matches ADR-85 R2.

### 3.3 CLAUDE.md

- **CL-A §4/§5 file-lifecycle DUPLICATION → CONDENSE (#157).** See C3. MACHINE-VERIFIED.
- **CL-B §5 rule #3 "in-file marker" self-contradiction → UPDATE (#112).** See C3. MACHINE-VERIFIED.
- **CL-C §8 lists `verify` under "User-level (`~/.claude/skills/`)" (L120), but the skill is repo-level**
  (`.claude/skills/verify/verify.py`; `~/.claude/skills/` holds only `gotchas`). **UPDATE** — move `verify`
  to the repo-level list. MACHINE-VERIFIED. **NEW** (no existing id). *(This is the corrected, accurate
  version of the refuted "`/verify` is a dead reference" claim — see §6.)*
- **CL-D §6 step 7 "Wait for Rob's prompt — never improvise" is unqualified vs ADR-87** (CC self-loads for
  code-impact tasks). **UPDATE** to qualify/point to ADR-87. JUDGMENT.
- **CONDENSE (judgment, budget-edge — file is 185/200 L):** §9 hook descriptions restate
  `.pre-commit-config.yaml` (CL-E); §4 "Output formatting (render-layer)" ~11 lines duplicates PLAYBOOK §8
  (CL-F); §10 anti-pattern #3 "managing AGENTS.md" is vacuous (AGENTS.md is gone) → reframe (CL-G).
- **KEEP (verified accurate):** §11 ADR-85–89 "last 5" + the ADR-88/89 **Proposed** annotations match
  `docs/decisions/README.md`; §6/§7 `/boot`+`/evolve` archive paths resolve (`~/.claude/archive/2026-06-05-
  machinery-c3/`); §4 Council-transcripts path resolves (`docs/decisions/transcripts/`). MACHINE-VERIFIED.

### 3.4 ARCHITECTURE.md

- **AR-A ARCHITECTURE → handoff-process undeclared edge** (prose at L214/L321/L534; no frontmatter
  `reconciled_with`). The known #172/#199 spine gap; ARCHITECTURE is a prime candidate to **declare
  `reconciled_with: handoff-process@5.2`**. PROMOTE/UPDATE. MACHINE-VERIFIED (`scan_undeclared_edges`).
  backlog: #172.
- **AR-B L534 references "`HANDOFF_PROCESS.md`" without the `protocols/` prefix** (other surfaces use the
  qualified path). Minor **UPDATE**. JUDGMENT/low.
- **AR-C conformance pointer absent → KEEP-known (#171).** See C7.
- **AR-D the 2 FF commits → KEEP (grandfathered).** ARCHITECTURE's core-invariant-#5 assertion is correct;
  the violations are historical + dispositioned (§1). MACHINE-VERIFIED.
- **KEEP (verified healthy):** organ-map / Validators inventory matches live (`audit.py checks` = 23
  registered; `.pre-commit-config.yaml` = 10 hooks; `scripts/` validators present); Governing-ADRs index
  spot-checked (ADR-28/68/82/84 exist, statuses match); "Layer 2 never executes" holds (no mutation code in
  `scripts/*.py`); mermaid theme directive passes; `last_reviewed` fresh. Count-claims (23 checks, 10 gates,
  793 collected) **match** (baseline + orchestrator `pytest --collect-only` = 793). Strong health signal.

### 3.5 HANDOFF_PROCESS.md + HANDOFF_BOOT.md

Cross-referenced against the in-flight `2026-06-23-handoff-process-audit-findings.md` (commit `31e0cd2`) —
**bound, not re-derived.** That audit's CUT-6 → REMOVE-candidate, ADD/rework → UPDATE/PROMOTE, KEEP → KEEP.
Its headline items (C5 stale "deferred validator" text in §11 + `audit.py`; C1 the dead v4 8-file generator
in `.claude/commands/handoff.md`, gated to #164; C6 PASTE_THIS thinness) are **its** to carry.

This audit's **complement** (gaps it under-weighted):
- **HB-A HANDOFF_BOOT.md is complete** — all §7/§13 role dimensions present (execution + architect +
  verification + adjudication + plan-review + closing), no orphaned role; the §4 "role must be resident in
  the boot, not left only in this spec" constraint is satisfied. **KEEP.** Content-verified.
- **HB-B v5.2 SUPPLEMENT.md mechanism is parenthetical in BOOT's architect-mode** (L59) where PROCESS §13
  treats it as first-class → **UPDATE** (promote to a front-loaded sentence; clarity, not correctness).
  JUDGMENT. backlog: #159/#164.
- **HB-C BOOT title says "(HANDOFF_PROCESS v5)" while PROCESS/CONTRIBUTING stamp v5.2** — acceptable (BOOT
  is a deployment artifact, not a version-locked surface; it never claims a wrong patch). **KEEP.**
- **No re-narration across PLAYBOOK §8 / ESSENTIALS §Roles / the two HANDOFF files** — PLAYBOOK §8 explicitly
  defers ("must not duplicate its mechanics"); ESSENTIALS stays at layer level. The pointer hierarchy is
  intact. **KEEP.** MACHINE-VERIFIED.

---

## 4. Roll-up tables

### Table A — every surviving finding

| ID | File | Lens | Verdict | Confidence | backlog |
|---|---|---|---|---|---|
| C1 | PLAYBOOK+ESSENTIALS | duplicated | DONE (record) | MACHINE | #77 |
| C2 | ESSENTIALS+DoD | duplicated | KEEP | MACHINE | #77/#5 |
| C3 | CLAUDE | duplicated/contradicted | CONDENSE+UPDATE | MACHINE | #157,#112 |
| C5 | PLAYBOOK+DoD | duplicated | KEEP+xref | JUDGMENT | #147 |
| PB-A | PLAYBOOK | obsolete-process | REMOVE-candidate | MACHINE | #77 |
| PB-B | PLAYBOOK | superseded | UPDATE | MACHINE | — |
| PB-C | PLAYBOOK | dead-reference | UPDATE | MACHINE | — |
| PB-D | PLAYBOOK | dead-ref/unenforced | UPDATE | MACHINE | #77 |
| PB-E | PLAYBOOK | cruft | CONDENSE | MACHINE | — |
| PB-F | PLAYBOOK | cruft | CONDENSE | JUDGMENT | — |
| PB-G | PLAYBOOK | contradicted | UPDATE | MACHINE | #77 |
| PB-H | PLAYBOOK | cruft | CONDENSE | JUDGMENT | — |
| PB-I | PLAYBOOK | aspirational | UPDATE | MACHINE | — |
| PB-J | PLAYBOOK | aspirational | UPDATE | JUDGMENT | — |
| PB-K | PLAYBOOK | dead-reference | UPDATE | MACHINE | — |
| PB-L | PLAYBOOK | unenforced | PROMOTE | MACHINE | #199 |
| ED-A | ESSENTIALS | cruft | CONDENSE | MACHINE | #77,#5 |
| ED-B | ESSENTIALS | aspirational | UPDATE | JUDGMENT | — |
| ED-C | ESSENTIALS | contradicted | CONDENSE | JUDGMENT | — |
| ED-D | DoD | cruft | CONDENSE | JUDGMENT | — |
| ED-E | DoD | unenforced | KEEP | MACHINE | — |
| CL-A | CLAUDE | duplicated | CONDENSE | MACHINE | #157 |
| CL-B | CLAUDE | contradicted | UPDATE | MACHINE | #112 |
| CL-C | CLAUDE | dead-reference | UPDATE | MACHINE | NEW |
| CL-D | CLAUDE | superseded | UPDATE | JUDGMENT | — |
| CL-E/F/G | CLAUDE | cruft | CONDENSE/reframe | JUDGMENT | — |
| AR-A | ARCHITECTURE | unenforced | PROMOTE/UPDATE | MACHINE | #172 |
| AR-B | ARCHITECTURE | dead-reference | UPDATE | JUDGMENT | — |
| AR-C | ARCHITECTURE | aspirational | KEEP-known | MACHINE | #171 |
| AR-D | ARCHITECTURE | unenforced | KEEP | MACHINE | #153 |
| HB-A | HANDOFF_BOOT | — | KEEP | judgment | — |
| HB-B | HANDOFF_BOOT | cruft | UPDATE | JUDGMENT | #159/#164 |

### Table B — REMOVE-candidates (the future cleanup worklist, highest-confidence first)

1. **PB-A** — PLAYBOOK tier-transition DEPRECATED procedure subsection (~818). MACHINE-VERIFIED.
2. **PB-E** — ~19 scattered "CHANGELOG.md retired" annotations → collapse to one (a *content* removal, not a
   rule removal). MACHINE-VERIFIED.

*(Every other negative finding is UPDATE/CONDENSE — re-word or trim, not delete. No rule is recommended for
deletion. Per the delete-invariant, even PB-A/PB-E need explicit per-item operator approval and a
confirm-live before the cleanup arc acts.)*

### Table C — PROMOTE-to-enforcement

1. **PB-L** — `Decommission:` field rule asserted (MUST) but no detector (#199; the 2026-06-19 audit's
   "Supersession closes the loop" teeth).
2. **AR-A** — declare `reconciled_with: handoff-process@5.2` on ARCHITECTURE (and the other 11
   `scan_undeclared_edges` candidates) to close the #172/#199 spine.

---

## 5. New vs known

**Genuinely NEW (no existing BACKLOG id) — candidates for intake:**
- **CL-C** — CLAUDE.md §8 mis-categorizes the `verify` skill as user-level (it's repo-level). MACHINE-
  VERIFIED. *(Smallest possible fix; the only clean "new dead-reference" in the corpus.)*
- **PB-B** (L855 "v4 bundle" label), **PB-C** (`docs/archive/tech-radar/` path), **PB-D** (L2929 STALE
  marker / §14 lifecycle), **PB-G** (hooks-table drift), **PB-K** (Continuous-Improvement §6 mis-pointer) —
  each a small UPDATE; could fold under a single "PLAYBOOK referential-currency groom" item or under #77.

**KNOWN (cross-ref, do not re-file):** #77 (PB-A, PB-D, PB-E, ED-A, C1), #157 (CL-A), #112 (CL-B), #199
(PB-L), #172 (AR-A), #169/#171 (AR-C), #194/#201/#202 (C6), #5 (ED-A), #67 (C4), #147 (C5), #153/#84 (AR-D),
#159/#164 (HB-B).

**Already-fixed since 2026-06-19 (record so the cleanup doesn't re-open):** the ADR-87 skeleton tags;
`/boot`+`/evolve` consolidated to one retired-machinery note + removed from command tables; §9 Weekly Review
re-pointed to `corrections.jsonl`; the §18 gap dispositioned via `structure-allow`; the lesson→rule
statements reconciled to canonical + pointers (C1).

---

## 6. Confidence ledger — REFUTED agent claims (the integrity record)

Six high-impact findings that section-agents tagged **MACHINE-VERIFIED** were **refuted on orchestrator
re-verification** — each because the agent ran a real command in the **wrong scope**. They are recorded here
so the cleanup arc never acts on them:

| Refuted claim | Agent(s) | Why it was wrong (re-verification) |
|---|---|---|
| "ADR-72 & ADR-73 don't exist; child-floor authority is broken" | PB-1 | Both exist (`ADR-72-cloud-routine-hub-independence`, `ADR-73-per-repo-orchestration-distribution`); cited correctly for cloud self-containment, not child-floor. `ls docs/decisions/ADR-7{2,3}*`. |
| "`/verify` is a dead-reference skill" | PB-6, CL | Lives at `.claude/skills/verify/verify.py` (repo-level) + is in the live skill picker. Agents checked `~/.claude/skills/` + `SKILL.md` only. *(Survives as the weaker CL-C: mis-categorized, not absent.)* |
| "`surface-closures.ps1` is a dead reference" | PB-4, PB-5 | Exists at `~/.claude/hooks/surface-closures.ps1`; agents checked only repo `scripts/`. (PB-5's "rename to `surface_triage.ps1`" is also wrong — that's a different script.) |
| "`docs/research/` is kept-not-retired (PLAYBOOK wrong to say retired)" | PB-5 | `docs/research/` is **absent** — PLAYBOOK's "retired" is accurate. |
| "pytest count stale (793→781)" | AR | `pytest --collect-only` = **793**; matches the doc. |
| "Codex review protocol is for a retired tool → REMOVE" | PB-7 | `/codex-review` is a **live** command (CLAUDE §7 + skill picker); Codex is in active use for code diffs. |

**Also down-weighted:** ED-09 ("`seal-journal-anchor` has no `# rule:` code annotation") contradicts the
machine baseline (`doc_code_edge`: that edge **resolves**); the baseline wins — the annotation exists, the
agent's `grep` missed it.

**Ledger totals:** ~34 surviving findings — **~17 MACHINE-VERIFIED, ~17 JUDGMENT**; **6 refuted + 1
down-weighted** on re-verification. **What a cleanup must confirm-live before acting:** every Table-B removal
and every "dead-reference / path" UPDATE (PB-B/C/D/K, CL-C) — re-run the named referent check in full scope
(`~/.claude/` *and* repo, both filename conventions) at cleanup time.

---

## Proposed cleanup sequencing (recommendation, not an executed plan)

1. **Batch 1 — safe, high-confidence, low-risk (one groom session):** PB-B, PB-C, PB-D, PB-K (label/path/
   pointer UPDATEs), CL-C (verify mis-categorization). All MACHINE-VERIFIED; each a 1–2 line correction;
   confirm-live each referent first.
2. **Batch 2 — the tracked serialize-groups:** CLAUDE §4/§5 + §5 self-contradiction (#157 + #112, edit §5
   together); ESSENTIALS trim (#77 + #5, the ED-A condense map). These touch the most-loaded files —
   operator-gated, one serialize-group at a time.
3. **Batch 3 — REMOVE-candidates (explicit per-item approval, delete-invariant):** PB-A (tier-transition
   subsection), PB-E (CHANGELOG-retired annotations collapse).
4. **Batch 4 — PROMOTE-to-enforcement (separate build arcs, not a doc edit):** PB-L (`Decommission:`
   detector, #199), AR-A (declare `reconciled_with`, #172).
5. **Defer to their owners:** the in-flight HANDOFF audit's CUT-6 (its arc); #67 (PLAYBOOK §7); #147
   (ship-gate); #169/#171 (conformance dashboard).

---

*Produced read-only 2026-06-23 by a 12-agent fan-out + orchestrator synthesis with full re-verification of
high-impact claims. No audited file was modified. Line numbers are as-of-audit. Every removal/UPDATE is a
recommendation the operator ratifies and CC confirms-live before any cleanup acts.*
