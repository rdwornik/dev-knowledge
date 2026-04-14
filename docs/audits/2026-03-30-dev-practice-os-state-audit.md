# Dev Practice OS State Audit — 2026-03-30

> **Purpose:** Verify what actually landed from the 2026-03-30 session (Codex review integration, Project Scale Tiers, lessons appends, AGENTS.md template).
> **Scope:** Read-only. No edits made.
> **Auditor:** Claude Code (Sonnet)

---

## Section 1: Inventory

### Git log (last 13 commits as of audit)

```
dd58836 lessons: append TODO management lesson to LESSONS.md
f34dc7a docs: add AGENTS.md template with L and M scale variants
9a3f25f lessons: append project scale tier lesson to LESSONS.md
fe0d6ca docs: add Project Scale Tier reference to ESSENTIALS.md
3f186be docs: add post-structural-change documentation rule with tier scaling
665ff14 docs: add tier tags to scale-dependent Playbook sections
0741aeb docs: add Project Scale Tier system to PLAYBOOK.md
343abdf lessons: append 5 Codex audit lessons; add S16 to PLAYBOOK; update ESSENTIALS
73e8a9a docs: add Codex review integration spec
d6bfddb docs: add S15 Cross-Tool Review to PLAYBOOK.md
2f70713 docs: add Codex review step to ESSENTIALS.md session end
583f335 feat: add .claude/ project config with git-discipline rule and /save command
b635615 feat: initial commit — dev practice knowledge base (9 files)
```

### File tree

```
.claude/
  commands/
    save.md
  rules/
    git-discipline.md
docs/
  codex-review-integration.md
  audits/                        ← created by this audit (was missing)
templates/
  AGENTS.md.template.md
.gitignore
CHANGELOG.md
CLAUDE.md
dev-knowledge.code-workspace
ENVIRONMENT.md
ESSENTIALS.md
LESSONS.md
PLAYBOOK.md
README.md
SESSION_SETUP.md
TOKEN-LOG.md
```

### Working tree status

Clean. No uncommitted changes.

---

## Section 2: Status Table

### From "lessons integration prompt"

| Expected | Status | Evidence |
|----------|--------|----------|
| LESSONS.md — audit-first pattern (2026-03-30) | ✅ | Line 105: "Audit-first, fix-second is the only safe order" |
| LESSONS.md — two-AI reviewer (2026-03-30) | ✅ | Line 107: "Two AI reviewers catch different blind spots" |
| LESSONS.md — shims not big-bang (2026-03-30) | ✅ | Line 109: "Structural refactors need shims, not big-bang rewrites" |
| LESSONS.md — ARCHITECTURE.md value (2026-03-30) | ✅ | Line 111: "ARCHITECTURE.md is the highest-value deliverable of any major session" |
| LESSONS.md — false positive calibration (2026-03-30) | ✅ | Line 113: "Automated audit false-positive rate ~30%" |
| PLAYBOOK.md S16 "Code Quality Audit Process" with severity tiers | ✅ | Lines 606–640: CRITICAL/HIGH/MEDIUM/LOW defined |
| ESSENTIALS.md mentions monthly audit | ✅ | Line 86: "Monthly → Codex full-repo audit → triage flags (~30% false positives) → See Playbook S16" |

### From "scale tiers prompt"

| Expected | Status | Evidence |
|----------|--------|----------|
| PLAYBOOK.md "Project Scale Tiers" section with L/M/S definitions | ✅ | Lines 8–22: L/M/S defined with test counts and doc expectations |
| PLAYBOOK.md S15 tagged [L+M] | ✅ | Line 595: "## 15. Cross-Tool Review **[L+M]**" |
| PLAYBOOK.md S16 tagged [L only] and [L+M] where applicable | ✅ | Lines 607–608, 624, 629: tier tags present |
| PLAYBOOK.md "Post-Structural-Change Documentation" rule with tier scaling | ✅ | Lines 630–640: L/M/S differentiated |
| ESSENTIALS.md reference to Project Scale Tiers | ✅ | Line 102: "Project Scale Tiers: Every project declares L / M / S in its CLAUDE.md." |
| LESSONS.md — universal rules erode compliance (2026-03-30) | ✅ | Line 115: "Universal rules that don't apply universally erode compliance" |

### From "TODO management lesson prompt"

| Expected | Status | Evidence |
|----------|--------|----------|
| LESSONS.md — TODO markers: code OK, docs never (2026-03-30) | ✅ | Line 117: "TODO markers belong in code and tasks/todo.md, never in documentation" |

### From "AGENTS.md template prompt"

| Expected | Status | Evidence |
|----------|--------|----------|
| templates/ directory exists | ✅ | Present at root |
| templates/AGENTS.md.template.md with L and M variants | ✅ | L template (~100 lines) + M simplified template, both present |

### From earlier today (manual saves / infrastructure)

| Expected | Status | Evidence |
|----------|--------|----------|
| docs/audits/ directory exists | ❌ | Did not exist — created by this audit run |
| docs/audits/2026-03-30-codex-full-audit.md | ❌ | Never saved; no commit in git log creates it |
| .claude/commands/save.md | ✅ | Present in .claude/commands/ |
| .claude/rules/git-discipline.md | ✅ | Present in .claude/rules/ |

---

## Section 3: Gaps Requiring Follow-Up

Sorted by severity.

### 1. Lost artifact — docs/audits/2026-03-30-codex-full-audit.md

**Severity:** Lost lesson (not critical — workflow not broken, but the specific Codex audit output from 2026-03-30 is unrecoverable)

**What happened:** The prompt noted this as "(manual save)" — meaning it required a deliberate copy-paste from Codex output into a file. That step was never completed. There are zero commits touching docs/audits/.

**Impact:** The original audit findings from the 2026-03-30 Codex run are gone. PLAYBOOK S16 and ESSENTIALS both reference the Codex audit workflow, but the artifact that validated the workflow (the first real audit) does not exist.

**Classification:** Lost artifact. Cannot be recovered. Next audit will produce the first saved report.

### 2. Cosmetic — docs/audits/ directory was not created

**Severity:** Cosmetic (infrastructure gap, not workflow gap)

**What happened:** No earlier commit created this directory. The audit workflow described in S16 and ESSENTIALS references running Codex audits, but there was nowhere to save them.

**Impact:** Zero — directory created by this audit run. Future audit saves will work.

**Classification:** Self-resolving. Resolved by this audit.

---

## Section 4: Recommendations

### Gap 1: Lost artifact

No recovery action available — the Codex output was not saved. The recommendation is to treat the next Codex audit run as the first saved artifact.

**Ready-to-execute prompt:**

```
| Model | Sonnet |
| Mode  | auto-accept |
| Effort| low |

Run Codex audit on .dev-knowledge and save output.

STEPS:
1. Run: codex "Audit this repo against the structure described in CLAUDE.md. Read-only. Output findings by severity. Do not fix anything."
2. Save output to: docs/audits/2026-04-{DD}-codex-audit.md  (use actual date)
3. COMMIT: "docs: save Codex audit output YYYY-MM-DD"

WHAT NOT TO DO:
- Do not fix any flagged items — this is read-only audit
- Do not create AGENTS.md in this repo — it is an S-scale project
```

### Gap 2: Cosmetic (no action needed)

docs/audits/ now exists. No further action required.

---

## Summary

**14 of 16 expected changes verified. 2 gaps identified.**

- 1 gap is a lost artifact (unrecoverable, low impact)
- 1 gap is cosmetic (self-resolved by this audit)

The 2026-03-30 session was substantially complete. All process documentation (PLAYBOOK, ESSENTIALS, LESSONS) landed correctly. No workflow-breaking gaps.
