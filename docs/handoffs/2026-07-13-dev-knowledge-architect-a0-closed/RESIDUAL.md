# Residual — 2026-07-13-dev-knowledge-architect-a0-closed — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6). Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred` = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"* — the strategic *why* (intent · tensions · rejected · decomposition order) lives there; this residual is the repo-side state.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`, `validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in `PROBES.md` (P4/P6/P7), not in trusting these lines.** This bundle states **no** ship-gate verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

All drift-flags standing at this wrap are **pre-existing dispositions** carried in `ecosystem/disposition-register.yaml` — the no-ff journal-wrap set, the BACKLOG history-accretion set (#262/#278/#328/#332/#333), the CONTRIBUTING-template `reconciled_versions` placeholder (auto-clearable by #335), and the six handoff-process undeclared-edge set (ref #241). This session's three arcs (ARC 1 · ARC 2 · ARC 3) **and the follow-on consolidation** (satellite + #328 merges + wrap, spine `2bc02196`) introduced **NO new drift** — every gate ran green and every WARN was already dispositioned. **Note (post-consolidation):** the fleet's parity layer is now live — `fleet_parity` reports **8 WARN-undeclared** rows (the FIX/DECLARE/TICKET triage, §4); these are the parity checker's own advisory output, **not** ship-gate drift. Do not trust these words for the live picture — **P4/P6/P7 re-derive** the ship-gate verdict, the dispositioned-WARN count, and any `[stale]`/drifted `#id`; this bundle states none of those values by construction.

---

## §2 — Merged this consolidation + shipped this window (pointer, not re-narration)

**MERGED — the consolidation is DONE (both formerly-parked lanes integrated; spine `2bc02196`; worktree torn down, zero leftovers). `witnessed` post-consolidation; re-derive the live branch/worktree set via `PROBES.md` P3:**

- **Fable `#328` fleet_parity build** — merged `--no-ff` (`2bc02196`, message `[#328] [#332]`): `scripts/fleet_parity.py` checker + hermetic tests + `ecosystem/{parity-surfaces,dependency-baseline}.yaml` + hub `.methodology.yaml` (§9a executed via an ADR-101 in-file amendment). The `fable-328-build` worktree was **removed + pruned + branches deleted** (`feat/328-fleet-parity`, `worktree-fable-328-build`). W3-07 / W3-15 landed **as #328 deliverables — were never split** (SUPPLEMENT §Tensions). **#328 / #332 stay OPEN** — #328's Done-when includes consumer-side deployment (a later carrier arc), so merged as bracket-references, not `closes`.
- **Codex satellite-onboarding census** — merged `--no-ff` (`71b92f82`, audit index regenerated in-merge): `docs/audits/2026-07-13-technical-satellite-onboarding-census.md`. The lane branch is deleted. **Its open decision — the operator's 4 satellite tier rulings — moves to §4** (the census content is landed; the rulings are not yet made).

**SHIPPED (this session's arcs + the consolidation — the record is in `JOURNAL.md`, not recapped):** ARC 1 (ESSENTIALS Ch4/Ch12/§16 pointers + #14 `consumed-by`; `2db6dbc9`); ARC 2 (two consumer product-resume handoffs in `docs/handoffs/`; `b16a011b`); ARC 3 (this bundle; `94249356`); then the **consolidation** (`71b92f82` satellite + `2bc02196` #328 + the JOURNAL wrap). All ship-gate GREEN, 0 drift introduced; `fleet_parity` POST-merge = 157/17/8/0 (exact match to the overnight self-run). **Branches now `main` + `automation/fleet-audit` only.** This is a **map** — `JOURNAL.md` (2026-07-13 entries) is the record.

---

## §4 — Next-frontier decisions (the design "why" that travels)

**The full morning order + rationale lives in `SUPPLEMENT.md` (FILLED) §Decomposition rationale — read it first.** Repo-side carry-open items, each with its owner:

**Post-consolidation morning tail (hub methodology, non-blocking to product — full order + rationale in `SUPPLEMENT.md` §Decomposition):**
- **8 `fleet_parity` WARN triage → FIX / DECLARE / TICKET** (the parity layer is now live post-#328): corp hub-block `rev v1.3.1` vs recorded deploy `v1.2.0` → FIX; corp `pytest-xdist` absent → FIX (per #332); ai `pytest-xdist` installed-but-undeclared → DECLARE; `.vscode` ×2 (ai + corp) → DECLARE; hub+ai ignore-parity (`.hypothesis` / `egg-info`) → FIX. Proposals live in the closing browser chat; each becomes a micro-arc. Surfacing mode — recommendation: informational ship-gate step now, full `ALL_CHECKS` after triage zeroes — is an open ruling.
- **W3-16 renormalize arc** — the `.gitattributes` fleet-baseline renormalize deferred at the W3 hub-legs merge (`dc205263`): a **separately-reviewed single-piece-tree arc** (whole-file EOL diffs would otherwise ride interim commits). **The window is NOW OPEN** (trees merged, no open branches — hub ~1283 / corp ~802 / ai ~803 paths); run it per repo before new work accretes interim diffs.
- **Satellite tier rulings (4)** — the census (`docs/audits/2026-07-13-technical-satellite-onboarding-census.md`, now merged) proposes tiers; the operator's verdict is pending. **Flagged contradiction:** the census proposes **floor-only for life-architect**, which contradicts the operator's stated *"life-architect must be the same"* — his ruling resolves it, then fires the census's draft onboarding prompts.
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

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to **`BACKLOG.md`** (E1–E7 story-map, machine-checked by `validate_backlog` — serialize-groups + counts re-derived live, `PROBES.md` P9), the live branches (`git branch -v` / `git worktree list` — post-consolidation this is `main` + `automation/fleet-audit` only, worktrees = primary only; P3 re-derives HEAD/branch/ahead-behind), and any **drift-flag** `validate_git_backlog` raises (§1 / `PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is the whole task-state.
