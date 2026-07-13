# Residual — 2026-07-13-dev-knowledge-architect-a0-closed — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6). Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred` = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"* — the strategic *why* (intent · tensions · rejected · decomposition order) lives there; this residual is the repo-side state.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`, `validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in `PROBES.md` (P4/P6/P7), not in trusting these lines.** This bundle states **no** ship-gate verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

All drift-flags standing at this wrap are **pre-existing dispositions** carried in `ecosystem/disposition-register.yaml` — the no-ff journal-wrap set, the BACKLOG history-accretion set (#262/#278/#328/#332/#333), the CONTRIBUTING-template `reconciled_versions` placeholder (auto-clearable by #335), and the six handoff-process undeclared-edge set (ref #241). This session's three arcs (ARC 1 ESSENTIALS/intake · ARC 2 consumer handoffs · ARC 3 this bundle) introduced **NO new drift** — every gate ran green and every WARN was already dispositioned. Do not trust these words for the live picture — **P4/P6/P7 re-derive** the ship-gate verdict, the dispositioned-WARN count, and any `[stale]`/drifted `#id`; this bundle states none of those values by construction.

---

## §2 — In-flight lanes + shipped this window (pointer, not re-narration)

**IN-FLIGHT / PARKED LANES (do NOT integrate — other lanes' property; each is the operator's or its owner's to close):**

- **Fable `#328` SIEM build — `feat/328-fleet-parity` in the locked worktree `.claude/worktrees/fable-328-build`** (`witnessed` at derivation: an advancing, locked worktree). Operator-sanctioned parallel lane, built overnight. **Pending: (1) review the Fable self-run table FIRST** (its witnessed #328 fleet-parity build), **(2) review the terra findings**, then **merge → teardown** (worktree remove + prune + branch delete + orphan check, per the no-leftovers rule). W3-07 / W3-15 are **#328 deliverables — never split from it** (SUPPLEMENT §Tensions). Leave untouched until the morning integration.
- **Codex satellite-onboarding lane — `docs/satellite-census`** (`witnessed`: 1 commit ahead of `main`, tip `docs(audits): add satellite onboarding census`; **commit-and-STOP, parked**). Pending **operator tier rulings** (4 satellite tier assignments — SUPPLEMENT §Open questions) + operator morning review. **Preserve unmerged; do NOT merge/rebase/delete** until the operator rules.

**CARRIED (this session's three arcs — the record is in `JOURNAL.md`, not recapped):** ARC 1 session-archive-closeout (ESSENTIALS Ch4/Ch12/§16 pointers + #14 draft `consumed-by`; merge `2db6dbc9`); ARC 2 two consumer architect product-resume handoffs in `docs/handoffs/` (merge `b16a011b`); ARC 3 = this bundle. All ship-gate GREEN, 0 drift introduced. This is a **map** — `JOURNAL.md` (2026-07-13 entries) is the record.

---

## §4 — Next-frontier decisions (the design "why" that travels)

**The full morning order + rationale lives in `SUPPLEMENT.md` (FILLED) §Decomposition rationale — read it first.** Repo-side carry-open items, each with its owner:

**Queued hygiene / tail (hub methodology, non-blocking to product):**
- **W3-16 renormalize arc** — the `.gitattributes` fleet-baseline renormalize deferred at the W3 hub-legs merge (`dc205263`): `git add --renormalize --dry-run` churn = **1283 files** > 0, so it is a **separately-reviewed single-piece-tree arc**, to run in the **first merge-free slot** (whole-file EOL diffs would otherwise ride interim commits). Corp carries the same at ~802 paths, ai-council at 0 (already normalized).
- **W3-13 ToC retirement** — **operator-present** (not an overnight item): the release-machinery / ToC-convention reshape the operator wants to shape in-session. Deferred until then.
- **CLAUDE.md first-read diet** (SUPPLEMENT §Open questions) — ESSENTIALS yes; PLAYBOOK as a pointer? — operator's call.

**Deferred-with-owner supplement items (A0 traceability closure, `docs/audits/2026-07-13-technical-a0-traceability-closure.md`):**
- **SUP-01 [#254]** — hub `automation/fleet-audit` data branch (owner: **hub ops/architecture maintainer**). Push the ~16-commit delta, reconcile the stale progress text, **close the ticket WITHOUT merging the data branch to `main`** (it is a data branch, named at `ARCHITECTURE.md`).
- **SUP-03 corp [#15]** — corp `docs/backlog-transcript-mime-fix` (owner: **corp product-code maintainer**). Integrate the ticket-only branch, then replace the literal MP4 MIME with the uploaded-file MIME + non-MP4 regression coverage (the same corp#15 carried in the ARC 2 corp bundle).
- **SUP-04 [#280]** — the five-day-stalled intake-scene-build session (owner: **Rob** closes the stale session after confirming no uncommitted state → the **hub deploy/carrier owner** then propagates the intake scene under #280).

**Pending BACKLOG builds:**
- **#333 [P2]** — `codex-review` skill doc-lane branch (doc-only diffs get a prose/structural review profile instead of exiting unreviewed) + re-pin the doctrine to the verified codex 5.6 registry (`gpt-5.6-{terra,sol,luna}` valid; bare `gpt-5.6` invalid — SUPPLEMENT §Off-repo context).
- **#334 [P3]** — fleet-wide `ruff` → `ruff-check` hook-id migration, ONE coordinated arc across hub + corp + ai-council (never per-repo drift; `id: ruff` is a working legacy alias today).

**Standing (do NOT relitigate — SUPPLEMENT §Decomposition rationale):** the W3 census classifications, the traceability dispositions, the ruled #14 pack, the U2-class rulings, and the operator's 6 own reading-friction rulings.

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to **`BACKLOG.md`** (E1–E7 story-map, machine-checked by `validate_backlog` — serialize-groups + counts re-derived live, `PROBES.md` P9), the live in-progress branches (`git branch -v` / `git worktree list` — the §2 lanes; P3 re-derives HEAD/branch/ahead-behind), and any **drift-flag** `validate_git_backlog` raises (§1 / `PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is the whole task-state.
