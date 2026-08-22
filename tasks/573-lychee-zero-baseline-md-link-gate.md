---
id: "[#573]"
title: "lychee as a zero-baseline markdown-link gate on the actionable corpus"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: pre-commit-config
generates: BACKLOG.md
---

- [#573] [P3][S] **lychee as a zero-baseline markdown-link gate on the actionable corpus** — the library-first research measured the actionable corpus at **exactly 0 broken links**, the cheapest possible moment to arm a gate: it can only ever fire on new rot. Cost: one `.pre-commit-config.yaml` block plus one `lychee.toml`. Two config halves are mandatory and both are proven in the research: `--exclude '/[a-z]$'` for the `[#id](a)` grammar collision (our own annotation syntax parses as a relative link), and five `--exclude-path` entries (`docs/audits`, `docs/handoffs`, `docs/decisions`, `docs/archive`, `tests/fixtures`). Measured: `total 274 | successful 268 | excludes 6 | errors 0`. **HONEST SCOPE — NOT `[#534]`:** lychee extracts link syntax and was measured **blind** to our 6.9% prose-locator rot class on an eight-probe fixture · Done when: the gate is armed with its `lychee.toml`, a fixture proves it FAILs on an introduced broken link and passes on the live corpus, and the hook comment states its link-syntax-only scope · refs `docs/audits/2026-08-21-technical-library-first-research.md` (Trial C, recommendation 1), #534 · kill-candidates: none — no row owns markdown-link rot; `[#534]` owns prose-locator rot, which this does not cover · serialize-group: pre-commit-config
