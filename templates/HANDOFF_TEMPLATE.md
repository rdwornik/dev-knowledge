# HANDOFF — [Session slug]

<!-- scope: meta -->

**Session:** [Stream X session N — short descriptor]
**Dates:** YYYY-MM-DD [→ YYYY-MM-DD if multi-day]
**Status:** [OPEN | CLOSED]
**Repo:** `[repo-name]`
**Scale:** [S | M | L]

> Skeleton matches `protocols/HANDOFF_PROCESS.md` v2.0 (ADR-32 §5). Sections are fixed and ordered; keep empty sections present (empty section is itself a signal). For S-scale handoffs, sections may each be 1–2 lines; for L-scale, expect this file to be 100–200 lines.

---

## 1. Session charter recap

Verbatim copy of the charter Rob authored at session open:

```
repo:
session type: [strategic | execution-support | governance-change | recovery/resume]
goal:
non-goals:
expected artifacts:
max message budget:
stop condition:
```

---

## 2. Decisions made

- **[Decision]** — [1-line rationale]. [ADR-NN if formalised]
- **[Decision]** — [1-line rationale]

---

## 3. Work completed

Prefer machine-verifiable claims (file paths, commit SHAs, test commands) over prose.

- [What changed] — [file path(s) or commit SHA(s)]
- [What changed] — [file path(s) or commit SHA(s)]

---

## 4. Pending items

Numbered for stable cross-session reference (next handoff can say "closes pending item 2a").

1. **[Item]** — [effort estimate, urgency]
2. **[Item]** — [effort estimate, urgency]
   2a. [Sub-item if needed]

---

## 5. Open questions

Items requiring human decision before the next binding step. Empty if none.

- [Question — what's blocking, what would resolve it]

---

## 6. Files actually modified

Distinct from §3 (which may name conceptual changes). This is the literal file list.

```
[path/to/file]
[path/to/file]
```

Verify with: `git diff --name-only [base]..HEAD`

---

## 7. Required inputs for next browser session

What must be uploaded / what state must hold at resume.

- Upload `contents/` folder (drag-drop)
- Paste `first-message.md` verbatim
- [Other required state — branch, validator pass, commit SHA]

---

## 8. Governance docs referenced

Which authoritative documents bound decisions in this session.

- `protocols/ESSENTIALS.md` § [section]
- `protocols/PLAYBOOK.md` § [section]
- `docs/decisions/ADR-NN_[slug].md`
- Council decision #NN

---

## 9. Next recommended first action

Single concrete next step for the next browser session. Not a list — pick one.

> [Action — what to do, where, what success looks like]

---

## References

- Predecessor handoff: `docs/handoffs/[YYYY-MM-DD-slug]/`
- Transcripts / research / audits: [paths]
