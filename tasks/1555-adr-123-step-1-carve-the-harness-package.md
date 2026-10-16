---
id: "[#1555]"
title: "ADR-123 step 1: carve the harness into one versioned package, Codespace verbs included"
status: open
priority: P2
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1555] [P2][L] **ADR-123 step 1: carve the harness into one versioned package, Codespace verbs included** - ADR-123 is Accepted (R96, 2026-10-11) and its step 0 passed (P-1..P-3 PASS in a corp-monorepo codespace, `docs/audits/2026-10-13-verification-harness-probes-receipts.md`), but no row carries step 1. UC10 and UC5 spec item 7 need it: a consumer runs the loop and the Codespace path from the shipped package, so the hub drives no state in a child repo (core invariant 1); step 2 (corp-monorepo runs one lane in its own codespace) is the consumer's row · Done when: carried verbatim from ADR-123 §Migration step 1 -- "the hub suite is outcome-identical to its pre-move baseline under the same baseline id (ADR-121); `uv build` produces one wheel; `harness --version` prints the tag", and the package carries the `codespace-*` verbs and `codespace_parity.py` · touches: `packages/harness/`, `scripts/`, `pyproject.toml`, tests · kill-candidates: none -- `[#670]` is the floor deploy, a different carrier · refs `docs/decisions/ADR-123-the-harness-ships-as-one-versioned-artefact-pinned-in-each-consumer.md`, `[#670]`, `[#644]`, `docs/intake/2026-10-15-tech-outcome-scoreboard-rows.md` · source: `to-cc/BATCH-DEFINE-OUTCOMES-2026-10-15.md` §1 UC10 and §2 item 7; `to-browser/DIGEST-OUTCOME-SCOREBOARD-2026-10-15.md`
