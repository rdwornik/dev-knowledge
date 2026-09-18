---
batch: AC
seq: 1
status: open
closed_by: docs/audits/2026-09-17-technical-batch-ac-close-packet.md
---

# Batch AC — manifest (freeze half) · 2026-09-17

**Seat:** primary CC session (background) · **Order:**
`to-cc/AMEND-NIGHT-ORDER-CONSOLIDATED-2026-09-17.md` §10 · **Base at fire:** `main` `87638c8d`
plus this manifest's merge · **Open batches at freeze:** 0 (`batch_manifest.open_batches` = `[]`).

**This file is committed BEFORE any lane boots**, per §10 S3 and the batch AA precedent that
produced four task-id reallocations from a single missing manifest (`[#804]`).

## 0 · THE GO IS NOT YET GIVEN — recorded deliberately

§10 S6 ends **"Report back and STOP. Do not boot lanes."** This manifest is the FREEZE, not the
dispatch. The dispatch authorization is the separate order the browser seat writes to `to-cc/`
after S6, and the operator pastes into the DISPATCHER session (§11).

Recording the absence of the GO as a line in the manifest is the shape `[#685]` asks for — the
authorization becomes a file rather than a ceremony. It is recorded here as **PENDING**, not as
given, so an auditor reading this tree cannot mistake a frozen batch for a dispatched one.

**No lane in the table below may be provisioned until that dispatch order exists.**

## 1 · Id block and reservations

Block granted to batch AC: **889-899** (`id_allocator --block 889-899`, `kind=task-id`).
Reserved by create-only push to `origin` before this commit, never by a local maximum:

| id | ref | holder |
|---|---|---|
| `[#889]` | `refs/reservations/task-id/889` | `lane-ac-589-backlog-closures` — the acceptance-test row |
| `[#890]` | `refs/reservations/task-id/890` | `lane-ac-589-backlog-closures` — the per-task execution-state carrier row |

Unused ids in the block stay free. A reservation is permanent and a gap is cheaper than a
renumber (`id_allocator` HONEST LIMITS).

## 2 · The lanes

Every row below was resolved against the live index BEFORE this freeze (§10 S2). The `Rows`
column is the contract's `rows:` field; no lane's subject is duplicated into a new row where an
open row already owns it.

| # | Lane slug | Rows | Substrate | Ordered model / effort | Review |
|---|---|---|---|---|---|
| L1 | `lane-ac-741-dispatch-surface` | `[#741]` `[#509]` `[#582]` `[#604]` | LOCAL | sonnet / high | none — measurement only |
| L2 | `lane-ac-863-notification` | `[#863]` `[#886]` `[#888]` | LOCAL | sonnet / high | Codex terra before merge |
| L3 | `lane-ac-285-config-headers` | `[#285]` `[#863]` | LOCAL | sonnet / high | Codex terra before merge |
| L4 | `lane-ac-589-backlog-closures` | `[#589]` + FILES `[#889]` `[#890]` | LOCAL | sonnet / high | none — mechanical, witness-backed |
| L5 | `lane-ac-661-evals` | `[#661]` | LOCAL | sonnet / high | none |
| L6 | `lane-ac-582-dispatch-verb` | `[#582]` `[#741]` `[#675]` | LOCAL | sonnet / high | Codex terra MANDATORY |
| C1 | `ac-694-cloud-census` | `[#694]` `[#747]` `[#685]` | CLOUD — read-only, **no worktree, cannot commit** | haiku (fan-out) / sonnet (synthesis) | none |

**L6 IS CONDITIONAL.** It boots only if L1's item 1a reports the dispatch verb resolves INSIDE
this repo. The dispatcher reads L1's handback and boots L6 or does not — no human decision (§7).
If L1 reports another repo, L6 IS NOT BOOTED and the build is carried by `[#741]` with L1's
report as its input.

**Ran model is NOT recorded here** — this file lands before any lane exists, so a ran-model
column would be a prediction. ORDERED vs RAN is read off each lane's own transcript and reported
in its handback (§7).

**Model rationale:** §7 orders sonnet for every lane and states **OPUS RUNS NO LANE**. Routing is
manual today — nothing enforces the registry, `opusplan` is a no-op under `--bg`, and an unstated
model RUNS OPUS — so every contract states `-Model sonnet` explicitly.

**Slug-vs-row collision check (`[#749]`):** the seven slugs carry six distinct row digits
(741, 863, 285, 589, 661, 582) plus the cloud leg (694). No two lanes share a slug row id, so the
known duplicate-dispatch defect is not armed by this table. `[#741]` and `[#582]` each appear in
two lanes' `rows:` fields, which is a citation, not a second lane for the same row.

## 3 · Re-scopes forced by the S2 index query

Three lane subjects were RE-SCOPED against the index rather than taken as the order wrote them.
Each is a Class B instance (§3) found in the order itself:

1. **`[#740]` IS CLOSED** (2026-09-16, evidence `f903a24`). L1's item 1b as written — *"re-scope
   or close the row ON THE MEASUREMENT"* — is MOOT. The row's own body names the mechanism that
   closes it: AX25-2's generator-to-verb conformance test, delivered as **`[#675]` clause 1**, not
   in this batch. L1's 1b is therefore re-scoped to **measuring whether `[#675]`'s conformance
   assertion is GREEN today**, and it may not re-open `[#740]`.
2. **AX9-5 is owned by `[#694]`, not `[#685]`.** The order cites *"AX9-5 (`[#685]`)"*. `[#694]`'s
   body carries the AX9-5 metric clause verbatim and states that `[#685]` — the operator-GO
   artifact — *"is already open and is NOT re-filed here; the roster pairs them in one lane and
   they are two rows."* C1a is re-scoped to `[#694]`, with `[#747]` as the consumer of its counter
   and `[#685]` carried as the paired-but-distinct row.
3. **The `last_updated` header subject is `[#285]`, which sits DEFER** and whose scope was already
   WIDENED on 2026-09-05 to cover `protocols/ENVIRONMENT.md` alongside `protocols/PLAYBOOK.md` —
   exactly L3's two files. `[#285]` also carries a standing prohibition that binds L3 directly:
   **a bare stamp to green a gate is forbidden**; the stamp is lawful only behind a genuine
   end-to-end re-read evidenced by per-section notes in the stamping commit.

## 4 · Genuine absences — the two rows L4 files

The index query returned NO open row for either subject, so these are filed rather than re-scoped:

- **`[#889]` the acceptance-test row.** Done-when is intake 103 §0.6 VERBATIM — *"one lane runs end
  to end, dispatch to merged, in under one hour, with nothing wedged and no human decision in the
  middle"* — PLUS one sentence: the result names the set of guards armed while the measurement ran.
- **`[#890]` the per-task execution-state carrier row.** C1f establishes what `[#664]`,
  `tasks/` frontmatter, `manifest.json`, FPG-1 and the organ index already hold. Read-only, no
  build, Phase 1 only.

## 5 · What this manifest does NOT claim

- It does not claim a dispatch happened. See §0.
- It does not record a ceiling verdict as a refusal. `resource_lifecycle.ADMISSION_DISABLED` is
  non-empty, so the admission refusal is WITHHELD and its verdict is advisory only. Measured at
  freeze: total 27.67 GB, free 5.23 GB, non-Claude 20.40 GB, per seat 646.1 MB (n=1, PROVISIONAL,
  `[#827]`), ceiling 5 more seats against 4 live. **The order's premise that "at night the
  workstation is idle" is FALSE on this box at this hour** — 20.40 GB of the 27.67 GB total is
  held by non-Claude processes.
- It does not restate a count or roster that a surface computes. Row totals in §3/§4 come from
  `gen_task_tree`'s own parse of `tasks/` at freeze: 544 task files, 368 open, 176 terminal.

## 6 · Gates this freeze arms, stated so the integrator is not surprised

Declaring a batch open ARMS the batch-aware gates that lie dormant with no open batch — the
ADR-110 manifest refusal, the lane-exemption legs of the anchor gates, and the merge-queue
checks. Two consequences the integrator must plan for:

1. **The merge of THIS manifest gets no lane exemption** — it is the commit that opens the batch,
   so the exemption it creates does not cover it.
2. **Only four hooks run locally at commit today** (`audit-index-freshness`,
   `organ-index-freshness`, and the two pre-push gates). The other 32 are `stages: [manual]` and
   run in conductor job `commit-gate`, whose required-check ruleset ships
   `enforcement: disabled` — REPORT-ONLY. A lane that relies on a commit-tier gate to catch its
   mistake will not be caught (§3 Class A).
