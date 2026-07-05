# EPIC RETURN — doc-consolidation · (filled by the lane at close)
<!-- scope: meta -->

Required before any merge (HANDOFF_PROCESS §14b). Fill each section; keep the headers.
Closure is claimed on the epic done-contract's **hard metric**, never on "committed".

## 1. Commits + branch state

- `90c4cdb` docs(playbook): absorb ESSENTIALS-canonical detail into canonical homes — S2 of epic [#258]
- `15660c3` docs(essentials): trim to the 1-2-page charter frame — S1 of epic [#258]
- `e35b7ad` feat(claude-md): generability phase 1 — §7/§11 lists generated, not authored — S3 of epic [#258]
- (this closing commit) docs(epic): EPIC RETURN + own-block checkboxes + JOURNAL — lane close [#258]

Branch `epic/doc-consolidation`, tree clean at close. Suite green ON THE BRANCH — full-suite run after the S2 PLAYBOOK edits:

```
1294 passed, 7 skipped in 674.95s (0:11:14)
```

Post-S3 full-suite re-run tail (delta since the S2 run: ESSENTIALS/CLAUDE.md doc edits + the read-only generator + fragments):

```
1294 passed, 7 skipped in 505.75s (0:08:25)
```

Probes: E1–E5 PASS at boot; E3 re-audited at every story commit and at close (§5). E4 note: `audit.py ship-gate` in THIS WORKTREE reports RED solely on `deployed_methodology_version: epic-doc-consolidation not listed in deployed-versions.yaml` — verified environmental (the check keys by repo **directory name**; the worktree dir ≠ `.dev-knowledge`). Branch content adds no WARN; the same tree audits clean from the primary. Not dispositioned (environmental, per the standing memory rule).

## 2. Contract-vs-outcome per story

**S1 — ESSENTIALS back to charter: MET.** 448 → **174 lines** (~61% cut; a true 1–2-page frame is the operator's read — metric supplied, verdict not self-declared). Zero canonical detail duplicated against PLAYBOOK, spot-checkable: every trimmed section is now a 1–3-line pointer naming its canonical home (PLAYBOOK chapter/section or ADR); the only full-text sections kept are those with NO PLAYBOOK home by design (How Claude thinks; Starting/Ending a Session checklists; The 5 Rules; Three Homes table — frame material). SUPERSEDED-inline section (the `<repo>-parallel` sibling-dir recipe, incl. its struck-through history text) removed. Externally-cited section titles preserved (see §3).

**S1 deletion list (operator approval required BEFORE merge — per-section disposition):**

| Removed from ESSENTIALS | Disposition |
|---|---|
| Roles — full Does/Does-NOT lists + three-layer flow diagram | MOVED → PLAYBOOK §8 "Roles" (90c4cdb); compact frame + pointer kept |
| Architect → operator channel-discipline (full text) | MOVED → PLAYBOOK Ch4 (new subsection); bold-lead-in stub kept |
| Architect epistemic discipline: verification markers (full text) | MOVED → PLAYBOOK §8 (new subsection); merged stub kept |
| Architect epistemic discipline: completion claims (full text) | MOVED → PLAYBOOK §8 (new subsection); merged stub kept |
| Architect routing for technical proposals (full text) | MOVED → PLAYBOOK §8 (new subsection); bold-lead-in stub kept |
| Artifact generation direction (full text incl. Council-distillation note) | MOVED → PLAYBOOK §8 (new subsection); stub kept |
| Continuous Improvement posture (full text incl. VISION wrong/correct examples) | MOVED → PLAYBOOK Ch13 "Project-evolution posture"; one-liner kept |
| Commit message standard (full text) | MOVED → PLAYBOOK Ch3 (new subsection); one-liner kept |
| JOURNAL entry structure detail (Did/Result/Changes/Abandoned/Next semantics) | MOVED → PLAYBOOK §7 session-end step 2; checklist line kept |
| Multi-prompt overlap rule | MOVED → PLAYBOOK §2 Key rules bullet |
| Data-sanitization placeholder detail | MOVED → PLAYBOOK §13 (enriched); one-liner kept |
| Auto-TOC threshold note (≥~400 lines / ~8+ sections) | MOVED → inlined in PLAYBOOK "Auto-TOC" (which had pointed at ESSENTIALS for it) |
| Parallel sessions (ADR-61) — SUPERSEDED sibling-dir recipe + strikethrough history | DELETED as duplicate-of-canonical (live procedure: PLAYBOOK Ch8 "Parallel sessions & worktree discipline"); pointer kept; history in git |
| Key Shortcuts table + slash-command line | DELETED as duplicate (verified superset: PLAYBOOK Appendix A); 1-line pointer kept |
| Writing a Prompt — skeleton/[A]-[CC] sequence, skills-reference para, per-scale detail | DELETED as duplicate (PLAYBOOK §2 + Ch4 + ADR-87 equilibrium table); 6-line frame kept incl. the per-step verify command |
| Repo visual pattern detail (exception list etc.) | DELETED as duplicate (ADR-59 canonical; PLAYBOOK Ch3 pointer); 1-line index entry kept |
| Mermaid theme detail | DELETED as duplicate (PLAYBOOK "Codemap workflow" theme paragraph / ADR-51 v2); index entry kept |
| Auto-TOC mechanism detail | DELETED as duplicate (PLAYBOOK "Auto-TOC for large canonical docs"); index entry kept |
| docs/ taxonomy detail (two-variant tables, move rules) | DELETED as duplicate (ADR-60 canonical; PLAYBOOK Ch3 pointer); index entry kept |
| Rule-ID convention detail | DELETED as duplicate (PLAYBOOK Ch3 "Rule-ID naming convention" / ADR-89 OQ1); index entry kept |
| Managing Tokens — 7-bullet list | DELETED as duplicate (PLAYBOOK Appendix C, verified superset incl. golden rule); 3-line habit summary kept |
| Council output convention paragraph | DELETED as duplicate (PLAYBOOK §5 "Council output convention (current state)", verified fuller); pointer kept |
| Backlog schema detail (story-map layout line) | CONDENSED (PLAYBOOK §10 canonical); behavioral bits (closes/advances, done-items-leave) kept |
| Repo complexity band definitions (small/medium/large bullets, wrong/correct framing) | DELETED as duplicate (PLAYBOOK Ch5, verified fuller); 3-line pointer kept |
| Process versioning detail | DELETED as duplicate (PLAYBOOK Ch2, verified fuller); 2-line pointer kept |
| Supersession rationale prose | CONDENSED to the rule + pointer (PLAYBOOK Ch6 canonical) |
| Starting a Session — historical v4-bundle parenthetical | DELETED (history; preserved in git + PLAYBOOK Ch6 handoff-format history) |
| Feedback Loop — new-tool 30-second decision-rule sentence | CONDENSED to pointer (PLAYBOOK §3 evaluation flow + §11 maturity check canonical) |

**S2 — PLAYBOOK absorbs orphaned canonical detail: MET.** Absorb committed BEFORE the trim (90c4cdb precedes 15660c3); every S1 removal is either a MOVED row above (now in PLAYBOOK) or a verified-duplicate DELETE with the canonical home named. Verification method: each candidate section grep/read-verified against live PLAYBOOK text before cutting (verify-destination posture, Ch7). PLAYBOOK's four pointers that previously pointed INTO ESSENTIALS for this content were inverted/updated in the same commit (Roles §2805, artifact-direction §2570, channel-discipline §2830, TOC-threshold §3489).

**S3 — CLAUDE.md generability phase 1: MET** on the contract's own wording ("hand-synced ADR/command lists → generated"): §7's repo-level command list and §11's last-5 ADR list are now **generated-not-authored** (`scripts/gen_claude_rosters.py` → `.claude/generated/commands-repo.md` + `recent-adrs.md`, `@`-imported; `--check` regen-and-diff clean; CLAUDE.md 188 lines). **Scope narrowing vs the Tier-3 draft's fuller §7+§8+§9 recommendation (deliberate, evidence-cited):** §9's pre-commit list is NOT generated — `validate_doc_claims.extract_claimed_hooks` window-anchors that list in CLAUDE.md's **raw text** (an @import voids the anchor → doc_claims WARN → ship-gate RED), and the draft itself (migration risk 3) rules that retiring a check leg needs its own arc + ADR note; `audit.py` and the disposition register are outside this lane's boundary. §8 skills stay hand-prose (enumeration interwoven with archival doctrine, not a bare list). §11's curated one-liners retire from the CLAUDE.md surface (mechanical list replaces them; editorial depth remains in `docs/decisions/README.md` + the ADRs) — flagged for operator approval as part of this return.

**S4 — #220 semantic-currency: DROPPED (per contract).** No natural fallout — #220 is a MODIFY/semantic-drift detector axis; nothing in S1–S3 advanced it. Left untouched as the contract instructs.

**Epic done-contract:** ESSENTIALS ≤ charter length (174 lines; operator adjudicates "1–2 pages") · zero canonical detail duplicated against PLAYBOOK (spot-checkable via the table above) · phase-1 sections generated-not-authored (two fragments + `--check` clean) · gates green on branch (audit health OK; ship-gate RED only on the environmental worktree-name artifact, §1).

## 3. Self-adjudications + ARCHITECT-REVIEW-PENDING

1. **`.claude/generated/` fragments vs the literal boundary list** — the may-touch list names "hub CLAUDE.md (generability seam only) + new generator script under scripts/" but not the generated fragment files. Adjudged IN-boundary: the fragments ARE the @-import seam (the [#244] mechanism the story orders; the Tier-3 draft's seam is exactly `.claude/generated/` fragments). Flagged for root confirmation.
2. **S3 scope narrowed vs the Tier-3 draft** (§9/§8 not generated) — see S2/S3 above; grounded in the draft's own migration-risk 3 + the out-of-boundary audit surfaces. The root may re-scope the remainder as its own arc.
3. **§11 curated one-liners retired from CLAUDE.md** — content-surface change beyond a pure mechanical swap; preserved in README/ADRs/git. OPERATOR-GATED via this return (part of the deletion-approval).
4. **Four ESSENTIALS sections merged into "Architect disciplines" + a "Conventions (canonical homes)" index** — section headers cited by out-of-boundary files survive as bold lead-ins (`ARCHITECTURE.md` L125/L161, `.claude/commands/changelog-review.md` L23 verified resolvable); prose refs, not anchors, so they still land.
5. **E4 boot-gate reading** — PROBES say "any FAIL blocks the lane boot"; E4's RED was adjudged obtained-ground-truth + environmental (not a probe FAIL), lane booted. Evidence in §1.
6. **Pre-existing stale refs observed, NOT fixed** (minimal-diff discipline; for root): PLAYBOOK L584 + L622 cite "per ESSENTIALS… English-only" — English-only exists in neither old nor new ESSENTIALS; `protocols/AI_COUNCIL_PROCESS.md` L324 cites `ESSENTIALS § "Repo artifacts in…"` — a section title that predates this lane's file (already fuzzy before the trim).
7. **ESSENTIALS `last_reviewed` re-stamped 2026-07-05** — genuine-review basis: full-file read at boot + every section individually verdicted against PLAYBOOK during the trim. CLAUDE.md stamp stands (same-day arc rule; v2.30 recorded).

## 4. Proposed BACKLOG delta

For the ROOT to apply at integration (lane applied only its own-block S1–S3 checkbox ticks):

1. **NEW task (P3/S, serialize-group: pre-commit-config):** wire `gen_claude_rosters.py --check` as a `roster-freshness`-style regen-and-diff pre-commit hook for the two `.claude/generated/` fragments (currency today = regeneration only; `.pre-commit-config.yaml` was out of this lane's boundary). Companion: consider a `--files`-scoped trigger on `.claude/commands/*` + `docs/decisions/ADR-*.md` + the generator itself.
2. **NEW task (P3/S, follow-up to the Tier-3 draft):** phase-2 generability — §9 pre-commit list generation REQUIRES retiring/reworking the `validate_doc_claims` §9 window-anchor leg (gate-semantics change; own arc + ADR note per the draft's risk 3). §8 skills optional in the same arc.
3. **Optional hygiene (root's call):** fix the two pre-existing stale refs in §3 item 6.
4. **[#258] closure** itself: root's, on this return (`closes [#258]` on the merge or a root follow-up per convention).

## 5. Merge-readiness checklist

- [x] Diff touches ONLY the declared FILE-BOUNDARY (`git diff --name-only main...HEAD` at close: `protocols/ESSENTIALS.md`, `protocols/PLAYBOOK.md`, `CLAUDE.md`, `scripts/gen_claude_rosters.py`, `.claude/generated/*` [§3 item 1], `BACKLOG.md` [own block only], `JOURNAL.md` [prepend], this bundle's `EPIC_RETURN.md`)
- [x] No merges to main performed from this lane (commit-and-STOP honored; `git log --first-parent main` untouched by this lane)
- [x] JOURNAL entry on the branch names this lane's session SHAs (90c4cdb / 15660c3 / e35b7ad)
- [x] Working tree clean; suite green on the branch (§1 tails)
