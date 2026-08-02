---
id: "[#475]"
title: "`verify_seal_identity` runs at generation only — a hand-edited bundle bypasses the seal check"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#475] [P2][S] **`verify_seal_identity` runs at generation only — a hand-edited bundle bypasses the seal check** — [#473] made `gen_handoff` refuse to seal a bundle whose internal slug ≠ its own directory, but the refusal fires inside `generate()`, so it governs the machine path and nothing else. A hand-renamed directory, an edited Slug row, or a copied bundle all reach `git commit` unchecked — and once committed the artifact is immutable, so the defect is permanent and only absorbable at check time (the [#473] B′ rebase). The gate belongs where the artifact becomes durable: a pre-commit hook over staged `docs/handoffs/**` boot files. Wiring, not new logic. Honest limit to decide first: it catches the slug row, not a stale P0c/P3/P8 locator in an otherwise correctly-labelled bundle. · Done when: a staged bundle boot file whose internal slug disagrees with its directory blocks the commit, with a test tripping the hook and one proving a conforming bundle passes · refs [#473], .pre-commit-config.yaml, CLAUDE.md §9, ADR-101 · kill-candidates: none — [#473] shipped the seal-time half and is closed; no open row owns commit-time bundle validation
