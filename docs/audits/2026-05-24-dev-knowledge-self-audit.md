---
type: audit
scope: .dev-knowledge self-audit post Prompt-10 reconciliation + session 2026-05-23/24
date: 2026-05-24
auditor: Claude (Opus) via .dev-knowledge browser-chat session
status: immutable (after this prompt merges)
basis-adrs: [ADR-31, ADR-33, ADR-34, ADR-38, ADR-39, ADR-40, ADR-41, ADR-46, ADR-47, ADR-49, ADR-51, ADR-53]
---

# `.dev-knowledge` Self-Audit — 2026-05-24

Comprehensive audit of `.dev-knowledge`'s own canonical files against its own
amended standards, post the 2026-05-23 tier-deprecation reconciliation (Prompt 10),
root-hygiene pass 2 (Prompt 11), and the workspace combo iterations. Goal:
verify `.dev-knowledge` is internally consistent and ready as the clean reference
that child repos mirror against during universalization.

Operator-flagged seed: ARCHITECTURE.md still carried `[M/L]` tier-letter residue
despite the deprecation — empirical evidence that Prompt 10's self-application had
gaps. This audit finds and dispositions all such residue.

## Summary

| Severity | Count | Findings |
|----------|-------|----------|
| HIGH | 2 | A1 (ESSENTIALS live "Project Scale Tiers" section), A2 (ARCHITECTURE `## Diagrams [M/L]`) |
| MEDIUM | 10 | A3, A4, A5, A6, A7, B1, B2, B3, E1, E2 |
| LOW | 3 | B4, B5, E3 |
| **Total to fix** | **15** | across 7 files |

(A7 was caught by the post-remediation confirmation re-grep, not initial discovery — see Category A.)

Cross-file consistency findings (C1, C2, C3) are resolved by the A/B/E fixes above
(not separately counted). Preserved-as-historical and preserved-as-correct items are
documented per category. Two judgment calls are recorded as **Open Questions**.

Baseline at audit time: `pytest` 72 passed; `ruff check` clean; `audit.py health` OK
(3 repos registered). No child-repo files in scope.

---

## Category A — Tier/scale residue

The repo-tier system (declared `tier:`/`scale:` per repo, ADR-40 algorithmic
computation) was deprecated ecosystem-wide 2026-05-23. Active prescriptive residue
in living docs is drift; historical narration and the task-complexity S/M/L taxonomy
are not.

### A1 — ESSENTIALS.md "Project Scale Tiers" section [HIGH] — WILL FIX
- **Evidence:** `protocols/ESSENTIALS.md:337-346`. Live section: "Every project
  declares its scale in CLAUDE.md. Playbook sections tagged `[L only]` or `[L+M]`
  apply only to matching tiers" + S/M/L definitions + "Full matrix … in PLAYBOOK
  Section 'Project Scale Tiers'."
- **Why a finding:** Directly prescribes the deprecated system. References `[L only]`/
  `[L+M]` tags that were struck from PLAYBOOK (commit 4c036a9) and a PLAYBOOK section
  ("Project Scale Tiers") that was renamed to "Project complexity bands" with a
  universal-baseline reframe (Prompt 10). This is the cheat-sheet contradicting the
  reconciled PLAYBOOK — the exact drift CLAUDE.md anti-patterns warn against
  ("ESSENTIALS summarizes PLAYBOOK, not copies"). It sat beyond the 200-hit cap of a
  naive grep, which is why Prompt 10 missed it.
- **Recommendation:** Replace with an "informal complexity" summary mirroring PLAYBOOK
  "Project complexity bands" (small/medium/large as judgment descriptors, universal
  baseline, no declared tier, no `[L only]` tags).

### A2 — ARCHITECTURE.md `## Diagrams [M/L]` [HIGH] — WILL FIX
- **Evidence:** `ARCHITECTURE.md:100`. Section header carries the `[M/L]` tier-letter
  tag. Operator-flagged.
- **Why a finding:** The ARCHITECTURE-template was stripped of these vestigial
  tier-letter section tags (commit 55f3766) but the instance was not — a
  self-application gap.
- **Recommendation:** `## Diagrams [M/L]` → `## Diagrams`.

### A3 — ARCHITECTURE.md ADR-38 governing-ADR description [MEDIUM] — WILL FIX
- **Evidence:** `ARCHITECTURE.md:154`. "ADR-38 — universal repo baseline: mandatory
  files per scale tier (S/M/L)".
- **Why a finding:** Self-contradictory post-amendment — "universal repo baseline" then
  "per scale tier (S/M/L)". ADR-38 A5 is universal; tier gating removed.
- **Recommendation:** Describe as universal baseline (tier gating removed 2026-05-23, A5).

### A4 — ARCHITECTURE.md ADR-40 governing-ADR description [MEDIUM] — WILL FIX
- **Evidence:** `ARCHITECTURE.md:156`. "ADR-40 — scale tier evaluation: …" with no
  deprecation note.
- **Why a finding:** ADR-40 is DEPRECATED (2026-05-23). Description presents it as live.
- **Recommendation:** Mark `(DEPRECATED 2026-05-23)`.

### A5 — ARCHITECTURE.md ADR-41 governing-ADR description [MEDIUM] — WILL FIX
- **Evidence:** `ARCHITECTURE.md:157`. "ADR-41 — … BACKLOG.md mandate at M+ tier".
- **Why a finding:** "at M+ tier" is stale gating; BACKLOG is now universal (PLAYBOOK
  :544, :1904).
- **Recommendation:** "BACKLOG.md mandate (universal post tier-deprecation)".

### A6 — CONTRIBUTING.md BACKLOG "M+ tier mandate" [MEDIUM] — WILL FIX
- **Evidence:** `CONTRIBUTING.md:92`. "`BACKLOG.md` (root): cross-session pending items
  per ADR-41. M+ tier mandate."
- **Why a finding:** Stale tier gating; BACKLOG is universal.
- **Recommendation:** "universal mandate (per ADR-41, ADR-38 A5)".

### A7 — ESSENTIALS.md residual `[L+M]` tier tag [MEDIUM] — WILL FIX
- **Evidence:** `protocols/ESSENTIALS.md:316`. Monthly Codex-audit cadence bullet:
  "… → see PLAYBOOK Section 17 `[L+M]`".
- **Why a finding:** A `[L+M]` tier tag gating the audit cadence — the same class as A2,
  on a PLAYBOOK section whose tier tags were struck in Prompt 10. Missed by initial
  discovery because the line carries no "tier"/"scale" word, so the Category-A grep didn't
  match it; caught by the post-remediation confirmation re-grep on `[L+M]`/`[L only]`.
- **Recommendation:** Strip the tag; reframe cadence as judgment-by-complexity per
  PLAYBOOK's audit-cadence stance ("not tier-gated; a tiny single-script repo may skip").
- **Process note:** demonstrates the value of a tag-specific re-grep after remediation —
  exact-string discovery on "tier"/"scale" alone under-covers bare `[L+M]`/`[L only]` tags.

### Category A — preserved (not findings)
- **VISION.md:20, 69-71, 136-142; ARCHITECTURE.md:11, 122, 149** — tier mentions framed
  as *retired/deprecated* (deprecation notes + historical context). Correct; PRESERVE.
  (ARCHITECTURE:149 ADR-33 description reviewed — documents the amendment accurately;
  left unchanged.)
- **BACKLOG.md** — tier residue lives in closed/superseded/resolved items (e.g.
  :154-167, :227-232) that *narrate* the tier system's retirement (historical record,
  append-context) and in open cross-repo rollout items (:269, :361-378) where former
  tier labels are *descriptive prioritization context*, not prescriptive gating. Matches
  the prompt's expectation ("likely closed items"). PRESERVE. No prescriptive-living
  residue requiring removal.
- **PLAYBOOK.md S/M/L usages (:292-297, :348-359, :798-821, :2510, etc.)** — thoroughly
  reconciled in Prompt 10: repo-complexity bands reframed as informal descriptors
  (:351-359), with an explicit note that the *task-complexity* S/M/L taxonomy is
  unaffected. PRESERVE.

### Category A — Open Question (judgment call)
- **OQ-1:** `ESSENTIALS.md:122-125` uses "Scale S" / "Scale M+" to choose the
  communication channel (inline snippet vs downloadable prompt). This is the
  *task-complexity* taxonomy, which PLAYBOOK:359 explicitly preserves as unaffected by
  the deprecation — **not** a tier-deprecation violation. Left intact. Flagged only for
  the terminology collision between the two surviving "scale" uses; relabeling would be
  a preference change (no standard violation), so out of scope here.

---

## Category B — Deprecated-feature residue

CHANGELOG.md was retired ecosystem-wide (ADR-49); root README.md was deprecated from the
baseline (ADR-38 A5) and deleted in this repo (2026-05-23). References that *prescribe*
or *assume* these as live files are drift; references that *frame them as retired* are
correct.

### B1 — VISION.md References list cites CHANGELOG.md [MEDIUM] — WILL FIX
- **Evidence:** `VISION.md:153`. "`CHANGELOG.md` — notable changes timeline" listed as a
  repo artifact.
- **Why a finding:** CHANGELOG retired; file absent. Dangling reference.
- **Recommendation:** Remove the line (JOURNAL already listed two lines above).

### B2 — VISION.md verification mechanism cites CHANGELOG [MEDIUM] — WILL FIX
- **Evidence:** `VISION.md:124`. "CHANGELOG describes movement toward VISION" as a
  drift-detection artifact.
- **Why a finding:** Retired file; and JOURNAL already covers "traces work back to VISION"
  one bullet above (:123).
- **Recommendation:** Remove the CHANGELOG bullet.

### B3 — PLAYBOOK.md CHANGELOG row in file-type taxonomy [MEDIUM] — WILL FIX
- **Evidence:** `PLAYBOOK.md:524` lists `CHANGELOG.md` as a live file type, while the
  presence table at `:546` says "removed — superseded by ADR-49".
- **Why a finding:** Intra-file contradiction (also C2). Taxonomy presents a retired file
  as current.
- **Recommendation:** Annotate the taxonomy row as retired (ADR-49; git history replaces),
  mirroring how README is handled.

### B4 — PLAYBOOK.md branch-rename step references CHANGELOG [LOW] — WILL FIX
- **Evidence:** `PLAYBOOK.md:172`. master→main Phase 1: "Update repo's CHANGELOG.md and
  any docs naming the default branch".
- **Why a finding:** No repo should carry a CHANGELOG post-ADR-49.
- **Recommendation:** Drop the CHANGELOG clause; keep "any docs naming the default branch
  (e.g. JOURNAL)".

### B5 — ENVIRONMENT.md version-tracking references CHANGELOG [LOW] — WILL FIX
- **Evidence:** `protocols/ENVIRONMENT.md:266`. "Project versions tracked in each
  project's CLAUDE.md / CHANGELOG.md."
- **Why a finding:** CHANGELOG retired.
- **Recommendation:** "CLAUDE.md / git history".

### Category B — preserved (correct framing)
- `CLAUDE.md:64, :67`; `ARCHITECTURE.md:112`; `PLAYBOOK.md:519, :545`; `ESSENTIALS.md:254`;
  `JOURNAL.md:13`; `.claude/commands/save.md:6` — all frame README/CHANGELOG as
  deleted/deprecated/retired. Correct; PRESERVE.
- `ARCHITECTURE.md:170`, `CLAUDE.md:129` references to `docs/decisions/README.md` — that
  file exists (ADR index); valid. PRESERVE.
- ADR-40 mentions in `PLAYBOOK.md:493-504`, `VISION.md:137,141` — framed as deprecated.
  PRESERVE.

---

## Category C — Cross-file consistency

- **C1 [MEDIUM]:** ESSENTIALS "Project Scale Tiers" (A1) contradicts PLAYBOOK's universal
  baseline. **Resolved by A1.**
- **C2 [MEDIUM]:** PLAYBOOK taxonomy :524 (CHANGELOG live) contradicts presence table :546
  (CHANGELOG removed). **Resolved by B3.**
- **C3 [MEDIUM]:** CLAUDE.md §8 claims a repo-level gotchas skill that does not exist.
  **Tracked as E1.**
- **Otherwise aligned:** VISION ↔ ARCHITECTURE (layer model, authority, scope), CLAUDE.md
  ↔ PLAYBOOK (conventions, file lifecycle, anti-patterns), ESSENTIALS ↔ PLAYBOOK
  (post-A1). No further inconsistencies found.

---

## Category D — Frontmatter accuracy

- **D1:** `ENVIRONMENT.md` "Last updated: 2026-04-30" → 2026-05-24 (file modified this pass).
- **D2:** `VISION.md` `last_reviewed: 2026-05-23` → 2026-05-24.
- **D3:** `ARCHITECTURE.md` `last_reviewed: 2026-05-23` → 2026-05-24.
- **D4:** `CLAUDE.md` footer "Last updated: 2026-05-19" → 2026-05-24 (no YAML frontmatter;
  footer line).
- **No stale `tier:`/`scale:` keys** remain in any living-doc frontmatter (VISION
  frontmatter already cleaned in Prompt 10: version/owner/last_reviewed/status only).
- **Disposition:** frontmatter/date refresh is folded into each file's own remediation
  commit (one commit per file), rather than a separate frontmatter-only commit — avoids
  re-touching files and keeps each commit a single coherent concern. ESSENTIALS,
  CONTRIBUTING, PLAYBOOK carry no top-level `last_reviewed` frontmatter (section-level
  version notes instead); their section version notes already carry 2026-05-23 from
  Prompt 10 and are not re-stamped for these edits.

---

## Category E — Aspirational vs actual

### E1 — CLAUDE.md §8 references a non-existent repo gotchas skill [MEDIUM] — WILL FIX (see OQ-2)
- **Evidence:** `CLAUDE.md` §8: "Repo-level (`./.claude/skills/gotchas/`): Read
  `.claude/skills/gotchas/SKILL.md` before making changes". The repo's `.claude/` contains
  only `commands/` and `rules/` — no `skills/` directory (verified by glob + tree).
- **Why a finding:** The canonical agent-instruction file directs reading a file that does
  not exist (process description referencing a non-existent path).
- **Recommendation:** Reframe §8 to reflect reality — repo-specific empirical patterns live
  in `LESSONS.md`; universal gotchas live in the user-level skill (`~/.claude/skills/gotchas/`,
  which exists). Do **not** create a new skill (new artifact = needs operator approval).
- **OQ-2 (Open Question):** alternative is to *create* `.claude/skills/gotchas/SKILL.md`.
  Reframing chosen here because it is the truthful, non-artifact-creating fix; operator may
  prefer to create the skill instead.

### E2 — ENVIRONMENT.md "Dev Practice Knowledge" structure diagram is stale [MEDIUM] — WILL FIX
- **Evidence:** `protocols/ENVIRONMENT.md:159-175`. Diagram lists `README.md ← Triage rules`
  (:161) and `CHANGELOG.md ← Notable changes history` (:164) — both deleted — and omits
  `ARCHITECTURE.md`, `VISION.md`, `BACKLOG.md`, `CONTRIBUTING.md`, which now exist at root.
- **Why a finding:** Describes the repo as it was ~2026-04-30; aspirational-vs-actual drift.
- **Recommendation:** Update the diagram to current root layout.

### E3 — VISION.md "audit tool pending / until tool exists" [LOW] — WILL FIX
- **Evidence:** `VISION.md:128-129`. "Stream C audit tool — pending, per ADR-36 … Until
  tool exists, manual verification at session-close."
- **Why a finding:** `scripts/audit.py` exists and runs (`health`, `repo`, `run`, `registry`;
  3 repos registered). "Until tool exists" is stale.
- **Recommendation:** Reflect that the tool exists (manual verification remains a complement,
  not a stand-in for an absent tool).

### Category E — preserved
- `ESSENTIALS.md:243` skills-reference prose describes how skills work generically (not a
  claim that this repo has one). Correct; PRESERVE.

---

## Category F — Cross-references / link rot

- **F1:** README.md references — all framed as deleted/deprecated; no dangling navigation
  links. PRESERVE.
- **F2:** `docs/decisions/README.md` references — file exists; valid. PRESERVE.
- **F3 [MEDIUM]:** `.claude/skills/gotchas/SKILL.md` dangling reference — same as **E1**.
- **F4:** `docs/notes/` references — none in living docs; only `JOURNAL.md:26` narrates its
  removal (historical, correct). PRESERVE.
- Remaining link rot is resolved by the B/E fixes.

---

## Category G — Universalization-readiness

- **Assessment:** After the A–F fixes, VISION / ARCHITECTURE / CLAUDE.md / PLAYBOOK are
  authoritative and internally consistent. PLAYBOOK correctly labels universal-vs-per-repo
  scope on each file type (the "Universal (`.dev-knowledge` only)" tags), so a child-repo
  session reading this repo can distinguish what to mirror (universal conventions) from what
  is `.dev-knowledge`-specific (ESSENTIALS/PLAYBOOK/LESSONS/TOKEN-LOG live here only).
- **No mirror-blockers** identified that warrant changing `.dev-knowledge` content.
  Per scope discipline, no changes are proposed merely because a child repo might mirror
  differently — `.dev-knowledge` is authoritative; child repos adapt to it.
- **Conclusion:** post-remediation, `.dev-knowledge` is a clean reference for the
  corp-monorepo + ai-council tier-deprecation rollout sessions.

---

## Disposition ledger

| ID | File | Sev | Disposition |
|----|------|-----|-------------|
| A1 | protocols/ESSENTIALS.md | HIGH | WILL FIX |
| A2 | ARCHITECTURE.md | HIGH | WILL FIX |
| A3 | ARCHITECTURE.md | MED | WILL FIX |
| A4 | ARCHITECTURE.md | MED | WILL FIX |
| A5 | ARCHITECTURE.md | MED | WILL FIX |
| A6 | CONTRIBUTING.md | MED | WILL FIX |
| A7 | protocols/ESSENTIALS.md | MED | WILL FIX (caught in confirmation re-grep) |
| B1 | VISION.md | MED | WILL FIX |
| B2 | VISION.md | MED | WILL FIX |
| B3 | protocols/PLAYBOOK.md | MED | WILL FIX |
| B4 | protocols/PLAYBOOK.md | LOW | WILL FIX |
| B5 | protocols/ENVIRONMENT.md | LOW | WILL FIX |
| E1 | CLAUDE.md | MED | WILL FIX (OQ-2) |
| E2 | protocols/ENVIRONMENT.md | MED | WILL FIX |
| E3 | VISION.md | LOW | WILL FIX |
| OQ-1 | protocols/ESSENTIALS.md | — | PRESERVE (task-scale taxonomy, not a violation) |

Open Questions for operator: **OQ-1** (relabel task-scale "Scale S/M+" to avoid collision?)
and **OQ-2** (reframe vs create the repo gotchas skill?).
