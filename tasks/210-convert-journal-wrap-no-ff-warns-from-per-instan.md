---
id: "[#210]"
title: "Convert journal-wrap no-ff WARNs from per-instance disposition to a standing rule"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#210] [P3][S] Convert journal-wrap no-ff WARNs from per-instance disposition to a standing rule — 3 instances of one class (journal-wrap direct-to-main) are now ratified one-by-one in `ecosystem/disposition-register.yaml`, so it is a recurring structural gap, not one-offs. Likely shape: a path-scoped EXEMPT in `no_ff_merges` for a direct-to-main non-merge commit whose diff is CONFINED to `JOURNAL.md` + `docs/.../transcripts/` (any OTHER path in the diff still WARNs — must NOT weaken core-invariant #5 for real code). Alternative: enforce branch-then-merge for the session-end JOURNAL wrap (eliminate the class, not exempt it). Decide the shape when built. · Done when: the shape is recorded in `protocols/STANDING_RULINGS.md` in a section naming `[#210]`, AND either (a) the `no_ff_merges` exemption ships with a test proving a JOURNAL-only direct commit passes while a same-commit code-path edit still WARNs, or (b) the wrap moves behind a `--no-ff` arc; and `ecosystem/disposition-register.yaml` carries none of the 3 journal-wrap per-instance entries · refs ecosystem/disposition-register.yaml, scripts/validate_no_ff.py, core-invariants #5, ADR-75 · serialize-group: audit-py
