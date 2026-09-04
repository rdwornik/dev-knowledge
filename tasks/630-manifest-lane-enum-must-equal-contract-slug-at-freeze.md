---
id: "[#630]"
title: "Manifest lane enum must equal contract slug at freeze"
status: closed
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#630] [P2][S] **Manifest lane enum must equal contract slug at freeze** — **Integrator defect (b), ruled 2026-09-01.** Batch E's manifest enumerates `lane-b-2-essentials-and-claude-md`; what was dispatched, and what carries the commit, is `lane-b-3-claude-md-genre`. The slug was renumbered between draft and dispatch and **nothing anywhere compared the two**, so the manifest — the surface the ADR-110 exemption reads, the teardown iterates, and a fresh seat boots from — names a lane that does not exist while the lane that does exist is unnamed. **This is the same CLASS as the teardown-enum defect the batch-E manifest already documents at its head** (`LANE_BRANCH_RE` matching one letter then digits, so 14 two-letter lanes fell outside the enum that teardown iterates) — a name that appears in two places with only a human keeping them equal. That one was caught at freeze by predicate 5; this one was not caught at all, because no predicate crosses from the CONTRACT to the MANIFEST. **The freeze gate currently validates contracts against the registry and against each other; it never validates the set of contracts against the manifest that declares them.** That is the gap, and it is one comparison wide · Done when: the freeze gate REFUSES unless the set of lane slugs in the manifest's lane table equals the set of contract slugs in the batch's contract directory — set equality both ways, so a manifest naming a lane with no contract fails as loudly as a contract no manifest names; the refusal names both sides of the mismatch rather than only the count; and a test freezes a batch with a renumbered slug and asserts the refusal · refs `docs/audits/2026-08-31-technical-batch-e-manifest.md` ("THE TEARDOWN ENUM" and "THE FREEZE GATE — six predicates"), `scripts/batch_manifest.py`, `scripts/validate_substrate.py`, `[#629]`, `[#614]` · kill-candidates: none — `[#629]` is the sibling defect from the same dispatch and stays separate: that one is about a contract contradicting itself, this one about two surfaces disagreeing · source: operator ruling 2026-09-01, integrator defect (b)
