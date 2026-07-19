# Codex `sol` lane — independent adversarial derivation + diff vs consolidated

- **Class:** codex (ADR-101 enum) · **Date:** 2026-07-19 · **Slug:** cycle-close-sol-adversarial-diff
- **Lane:** `sol` — independent adversarial re-derivation. Model `gpt-5.6-terra` via `codex exec` (read-only reviewer per `codex/AGENTS.md`).
- **Independence guarantee:** sol was run with a hard rule forbidding it from opening any `docs/audits/2026-07-19-*` file (the streams' drafts + the consolidated report), and derived gaps from **primary sources only** (JOURNAL/BACKLOG/intake/ADRs/protocols/scripts/ecosystem/CLAUDE.md). sol's own output header confirms: *"Independent review; no `docs/audits/2026-07-19-*` files read."* The derivation was launched **before** the consolidated report existed. This file then diffs sol's independent result against the consolidated report.
- **Codex line-references** below are sol's own; treated as pointers to verify, not gospel (codex line numbering can be approximate).

---

## 1. sol's independent derivation (verbatim structure, 8 domains + HIGH flags)

1. **[HIGH] Intake lifecycle/status enum** — *Gap:* the canonical intake lifecycle is not enforced; live `READY-TO-FIRE` bypasses it into `OTHER`, so status no longer signals pipeline position. *Evidence:* `docs/intake/README.md:138`, `docs/intake/2026-07-16-satellite-onboarding-prompts.md:3`, `scripts/gen_intake_index.py:35`. *Mechanism:* a `validate_intake.py` **pre-commit gate** — closed status enum, unique IDs, required `consumed-by` for CONSUMED, verified intake→ADR→epic/UAT joins.
2. **Backlog decision-ops** — *Gap:* no executable lifecycle harness from ruled requirement → implementation → dynamic proof → closure → **real deletion**; safe-deletion explicitly unruled. *Evidence:* `BACKLOG.md:219` (#347). *Mechanism:* a `lifecycle_harness` ship gate requiring a machine-readable intake/ADR/task/proof/closure chain + a `safe-delete` verifier before a superseded artifact can be removed; a scheduled `backlog-groom` reporter for age/accretion/closure-candidates.
3. **Archives/lifecycle records** — *Gap:* ADR headers can assert `Proposed` while the index treats them accepted; no checker detects the contradiction. *Evidence:* `ADR-88…:5`, `ADR-94…:36`, `BACKLOG.md:35` (#242). *Mechanism:* implement #242 as an `audit.py` ADR-status reconciliation check under `audit-health` with header/index-disagreement fixtures.
4. **Doctrine currency** — *Gap:* merge-delegation is canonical, but the newer consumer→hub write exception and two-tier new-path authorization remain **non-mechanized exception doctrine — a consumer session cannot prove its authorization**. *Evidence:* `PLAYBOOK.md:1193`, `ADR-101…:193`, `BACKLOG.md:23` (#344). *Mechanism:* a consumer-side PreToolUse guard denying hub/global writes unless a **HEAD-bound operator authorization token** names the dedicated worktree, branch, and allowed paths; paired with the #346 durable runtime rule.
5. **Worktree/parallel discipline** — *Gap:* primary-checkout self-merges and mid-session dirty-tree side effects are prose-only; Git cannot distinguish an unauthorized self-merge. *Evidence:* `PLAYBOOK.md:1399`, `BACKLOG.md:42` (#353). *Mechanism:* a mutating-tool PreToolUse gate requiring clean-tree-or-declared-worktree-binding, plus a merge wrapper/pre-merge hook requiring a **signed integration-return token**.
6. **Browser↔CC prompt equilibrium** — *Gap:* the required governance pointer + formal prompt contract have no inbound completeness check; even handoff fill-markers pass ungated. *Evidence:* `PLAYBOOK.md:2241`, `BACKLOG.md:75`. *Mechanism:* `validate_prompt_contract` invoked by the browser-paste/assembly path, issuing a **prompt-hash attestation**; a PreToolUse gate rejects state-changing work without a current attestation for formal prompts.
7. **Fleet-state management** — *Gap:* parity telemetry is hub-local, rotation-capped, fail-open JSONL from checker runs only; **no consumer collection, no watermarks — so silence is indistinguishable from absence at fleet scale.** SQL/SIEM is premature, but a collector is not. *Evidence:* `fleet_parity.py:59`, `docs/intake/2026-07-13-siem-fleet-management-requirements-codex.md:163`. *Mechanism:* a scheduled hub `fleet_collect` **PULL collector** with per-repo checkpoints, watermarks, unavailable/gap events, raw JSONL retention; SQLite/DuckDB only after measured thresholds.
8. **[HIGH] Testing harness** — *Gap:* dynamic sandbox/console testing before review is not a required, configured stage; agentic-review profiles deferred — "tests then review" is task prose. *Evidence:* `BACKLOG.md:219` (#347), `BACKLOG.md:161`. *Mechanism:* a versioned `test-harness.yaml` mapping change-classes → sandbox setup / dynamic tests / expected evidence / reviewer profile; `/ship` refuses without a matching successful attestation.

**sol's own HIGH-under-weight flags:** #1 (status vocabulary silently breaks traceability), #4 (cross-repo write exception lacks an authorization guard), #8 (review can occur without dynamic behavioral evidence).

---

## 2. Diff: sol (independent) vs the consolidated report

**Headline: full convergence, zero misses.** sol independently reproduced a gap in **all 8** domains, and every gap it found maps onto a stream finding in the consolidated report. Because sol never saw the streams, this is strong triangulated validation that the consolidated report's gaps are real and not an artifact of one reviewer's framing. sol surfaced **no gap that the consolidated missed entirely** — but it proposes **stronger mechanisms** in four places and **sharpens two diagnoses**.

| sol domain | consolidated stream | verdict | delta |
|---|---|---|---|
| 1 intake enum | S1 + S3 | **converge** | sol wants a **hard `validate_intake.py` pre-commit gate** w/ join-verification; consolidated proposed an `audit.py` WARN. sol is stronger. |
| 2 backlog lifecycle/deletion | S2 | **converge** | sol adds a **`lifecycle_harness` machine-readable chain gate** (the #347 harness as an executable ship-gate), beyond S2's grooming+`safe_remove` extension. |
| 3 ADR status #242 | S3 | **converge (exact)** | same mechanism, same tickets. No delta. |
| 4 doctrine currency | S4 (+ S6) | **converge, reframed** | sol elevates **authorization-PROVABILITY** ("a consumer session cannot prove its authorization") as the central gap + a HEAD-bound token guard — where the consolidated split this across S4 (doctrine transcription) and S6/#344 (write guard). |
| 5 worktree discipline | S6 | **converge** | sol adds a **signed integration-return token / merge wrapper** to detect an unauthorized self-merge — a mechanism no stream proposed. |
| 6 prompt equilibrium | S7 | **converge, stronger** | sol proposes a **`validate_prompt_contract` hash-attestation** enforced at PreToolUse; S7 proposed a soft self-check (noting the off-repo prompt is unreachable). sol's attestation-at-paste-time partially defeats that limit. |
| 7 fleet-state | S8 | **converge, sharpened** | both agree SQL/SIEM is premature. sol sharpens the real gap to a **PULL collector with watermarks (silence≠absence)**, not merely reporters — elevating S8's FR-8/9 fire-telemetry to the headline. |
| 8 dynamic/agentic testing | S9 | **converge (both HIGH)** | sol proposes a versioned **`test-harness.yaml`** change-class→evidence manifest; S9 proposed a `ship.md` code-impact tier + `AGENTIC_TESTING.md`. Compatible; sol's manifest is the config-artifact form of S9's gate. |

### One tension to reconcile (not a contradiction)
sol#4/#5 cite `PLAYBOOK.md:1193` / `:1399` and call **merge-delegation "canonical,"** whereas S4 judged the **consumer-leg merge-delegation composite un-encoded**. Both are correct at different granularities: the **components** (commit-and-STOP, parallel-worktree discipline) are in PLAYBOOK (~:1399), but the **named cross-repo consumer-leg composite** is not — S4's own report says exactly this (the hub-internal commit-and-STOP at HANDOFF_BOOT.md:155-159 is git-structurally scoped to same-repo worktrees and does not cover the separate-consumer case). No consolidated edit needed; the diff simply confirms the components exist while the composite does not.

---

## 3. Adjudication — sol sharpenings folded into the record

These sol contributions are **accepted as strengthenings** and are carried into the HANDOFF-PREP material (the operator decides which to build; this run files nothing structural):

- **A. Prefer a hard `validate_intake.py` pre-commit gate over an `audit.py` WARN** (sol#1) — closed enum + unique `intake-id` + `consumed-by`-on-CONSUMED + intake→ADR join. Directly fixes S1's `intake-id:14` collision **and** S1's unenforced ADR-citation in one gate. **Upgrade to consolidated seed #2.**
- **B. The authorization-PROVABILITY framing (sol#4) is the unifying mechanism** for #344 Ask-2 / #353 / the RULING-W consumer-write path: a **HEAD-bound operator-authorization token** naming worktree+branch+allowed-paths, checked by a PreToolUse guard, is one organ that satisfies S4 (doctrine), S6 (#353/#344), and S7 (attestation) at once. **Strengthens consolidated seeds #6 + #7.**
- **C. The fleet-state gap is a collector-with-watermarks, not just reporters (sol#7)** — "silence ≠ absence" is the sharper diagnosis; a scheduled `fleet_collect` PULL collector subsumes S8's two reporters. Still zero-new-dep, still Layer-2-legal (read-model, not a mutating store). **Sharpens consolidated seed #8.**
- **D. A signed integration-return token / merge-wrapper (sol#5)** is a novel mechanism for self-merge detection beyond the SessionStart/PreToolUse organs S6 proposed. **Adds to consolidated seed #6.**

**Net:** sol confirms the consolidated report is sound and complete on coverage, and contributes four mechanism upgrades + one reframing (authorization-provability as a unifying organ). No consolidated finding is refuted; no gap is added or removed. See `2026-07-19-codex-cycle-close-terra-review.md` for the independent review of the consolidated report itself.
