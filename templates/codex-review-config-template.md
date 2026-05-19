# Codex Code Review Configuration — Embeddable Template

> Codex-specific review configuration content. Embed relevant sections in CLAUDE.md Section 5 ("Tools active in this repo") per Scale tier. Scale L gets full version. Scale M gets simplified. Scale S does not embed Codex review (no Codex usage at that scale).
>
> **Cross-reference:** `templates/CLAUDE-md-template.md` is the parent governance template. This file provides Codex-specific content for Section 5 of that template.
>
> **Last updated:** 2026-04-24

---

## Scale L — Full Template (multi-package repos, 500+ tests)

```markdown
# CLAUDE.md — Codex Code Review Configuration

> This file is read automatically by Codex CLI (OpenAI).
> Codex is a **read-only code reviewer** in this repo. It does not build, fix, or modify.

## Role: Review Only

**Codex MUST NOT:**
- Modify any file
- Create branches or commits
- Run any command that writes, deletes, or modifies state. Read-only commands (git diff, git log, cat, type) are explicitly allowed.
- Suggest applying fixes directly — only report findings

**Codex MUST:**
- Read code and report issues
- Reference specific file:line locations
- Prioritize findings (critical / high / medium / low)
- Be concise — finding + why + suggested fix direction

## Architecture Context

### Repo: [REPO NAME]
[One-line description of repo structure]

### Module Structure
[List modules with layer numbers. Example:]
```
src/
  module_a/    Layer 0 — description
  module_b/    Layer 1 — description
  module_c/    Layer 2 — description
```

**Dependency Rule (ENFORCE)**
Dependencies flow DOWN layers only. Layer N may import from Layer 0..N-1, never from N+1.
[List concrete layer assignments]

### Key Invariants
[List 3-7 architectural rules that MUST NOT be violated. Examples:]

- [Module X] is the ONLY writer to [resource Y]
- [Module Z] is pure — no side effects
- [Safety constraint — e.g., certain paths are read-only]

### Databases
[List databases with table counts if applicable]

### Config
[List config approach — dataclasses, YAML, env vars]

## Review Checklist

### Review Modes
- **Diff review (default):** Check Critical + High only. Skip Medium and Low.
- **Full audit (explicit):** Check all severity levels. Use monthly or after major refactors.

Codex assumes diff review mode unless prompt explicitly says "full audit."

### Critical (block merge)
CRITICAL = Runtime bugs, data loss risk, security issues, architectural invariant violations.

- [ ] **Import direction** — no upward layer violations
- [ ] **Safety constraints** — [project-specific safety rules]
- [ ] **API keys** — no secrets in code or config
- [ ] **SQL injection** — parameterized queries only
- [ ] **Silent swallow** — no bare except without logging
- [ ] **Writer invariant** — [sole writer rule if applicable]

### High (should fix before merge)
HIGH = Issues that change runtime behavior or silently degrade data. Convention violations belong in MEDIUM or LOW.

- [ ] **Missing error handling** — file I/O, API calls without try/except
- [ ] **Hardcoded paths** — absolute paths, usernames in code
- [ ] **Broad exceptions** — except Exception: where specific types known
- [ ] **Race conditions** — concurrent access to shared resources
- [ ] **Test coverage** — new public functions without tests

### Medium (note for follow-up)

- [ ] **print() in library** — should be logging
- [ ] **os.path vs pathlib** — prefer pathlib
- [ ] **Magic numbers** — unnamed constants
- [ ] **Function length** — >100 lines = extraction candidate
- [ ] **Type hints missing** — public functions without annotations

### Low (cosmetic)

- [ ] **Docstrings** — missing on public classes/functions
- [ ] **Naming** — inconsistent patterns
- [ ] **Import order** — flag if obviously wrong

## Output Format

Report findings as:

```
## [SEVERITY] filename:line — short description

**What:** One sentence.
**Why:** One sentence.
**Fix direction:** One sentence.
```

Group by severity. Omit empty severity sections.
```

---

## Scale M — Simplified Template (standalone packages, 50-500 tests)

```markdown
# CLAUDE.md — Codex Code Review Configuration

> Codex is a **read-only code reviewer**. It does not modify files.

## Role

Read-only reviewer. May run: git diff, git log, cat, type. Must not modify any file or run write commands.

## Architecture

### Repo: [REPO NAME]
[One-line description]

### Key Rules
1. [Rule 1 — most important architectural constraint]
2. [Rule 2]
3. [Rule 3]
4. No hardcoded paths or API keys
5. No bare except without logging

## Review Checklist (Critical + High only)

- [ ] **[Project-specific safety rule]**
- [ ] **API keys** — no secrets in code
- [ ] **Missing error handling** — I/O and API calls
- [ ] **Hardcoded paths** — use config, not literals
- [ ] **Test coverage** — new public functions need tests
- [ ] **Broad exceptions** — use specific types

## Output Format

```
## [CRITICAL/HIGH] filename:line — description
**What:** One sentence. **Why:** One sentence. **Fix direction:** One sentence.
```
```

---

## Scale S — No dedicated Codex config needed

Projects under 50 tests with simple structure do not benefit from Codex review.
If needed ad-hoc, run Codex with inline instructions instead of a file.
