---
id: "[#475]"
title: "`verify_seal_identity` runs only at generation — a hand-edited bundle file bypasses the seal check entirely"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#475] [P2][S] **`verify_seal_identity` runs only at generation — a hand-edited bundle file bypasses the seal check entirely** — [#473] closed the generation door: `gen_handoff` now derives every internal self-reference from the FINAL directory name and REFUSES to seal a bundle whose internal slug ≠ its own directory. But the refusal fires **inside `generate()` only**, so it governs the machine path and nothing else. A bundle directory renamed by hand, a `HANDOFF_BOOT.md` Slug row edited in place, or a bundle copied to a new slug all reach `git commit` unchecked — and the resulting artifact is *committed and immutable*, at which point the defect is permanent and only absorbable at check time (the [#473] B′ locator rebase). The gate belongs where the artifact becomes durable, not only where it is born: a `pre-commit` hook over staged `docs/handoffs/**` boot files asserting internal-slug == directory name. Cheap and mechanical — the predicate already exists and is tested; this is wiring, not new logic. Note the honest limit before building: this catches the *slug row*, not a stale P0c/P3/P8 locator inside an otherwise correctly-labelled bundle — worth deciding whether the hook checks locators too, or whether the check-time advisory remains their sole owner. · Done when: a staged bundle boot file whose internal slug disagrees with its directory name blocks the commit, with a test that trips the hook and one that proves a conforming bundle passes · refs [#473] (`scripts/gen_handoff.py::verify_seal_identity`), .pre-commit-config.yaml, CLAUDE.md §9, ADR-101 (the prospective-only refusal-gate precedent) · kill-candidates: none — [#473] is closed and shipped the seal-time half; no open row owns commit-time bundle validation
