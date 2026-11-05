# Residual — 2026-11-05-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.
>
> **Supplement fill-state:** stated once, in this bundle's `HANDOFF_BOOT.md` session header
> ([#611] — not duplicated here).

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

> **Standing vs NEW — generated, names only.** Three lists computed from `ecosystem/disposition-register.yaml` ∩ this window's own diff. **No verdict, count, stale-disposition line, sha or backlog id appears here** — those are P7/P4/P6/P9's live answers, which CC re-derives from PROBES.md. The frame covers the standing-WARN family only; an organ outside it is the FILL-IN's business, not silently filed as standing.

**Window** — the diff since `docs/handoffs/2026-10-28-dev-knowledge-architect/` was added.

**Dispositioned by the register.** The register already carries an entry for these organs, so a WARN from one is standing unless its evidence signature is new:
- `no_ff_merges`
- `journal_spine_anchor`
- `doc_rot`
- `undeclared_edges`
- `funnel_coverage`

**Dispositioned by absence from the window diff.** This window touched nothing these organs read, so a WARN from one is not this window's doing:
- `reconciled_versions` (reads the registered specs and the docs declaring a `reconciled_with:` edge)

**NEW-and-undispositioned.** No register entry, and this window DID touch what they read — so a WARN from one of these is this window's, and the note below says which is a decision rather than a defect:
- `fleet_parity` (reads the parity-surface manifest and the surfaces it names)

<!-- FILL-IN:driftflags START (hand-authored — ONE judgment only: name which NEW flag above is a DECISION rather than a defect. The standing-vs-new attribution is GENERATED directly above; do not restate it. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
`fleet_parity` is a DECISION, not a defect: the one surface it reads that this window changed is `.claude/commands/map.md`, added by [#1748] (the ADR-133 system view). `/map` is a hub-local command, the same class as `/decide`, `/spine` and `/why`, and hub-local items carry no deploy-manifest row by design (CLAUDE.md section 9: sections 7-9 hold the hub-LOCAL surface, the items with no manifest entry). Source: CC's state read, `git diff 1004f63f4 origin/main` over the parity surfaces plus `audit.check_fleet_parity` (witnessed).
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
source: `git log --first-parent main` since the 2026-10-28 cut landed (witnessed); row ids from each landing's `JOURNAL.md` heading (recall). Detail: `JOURNAL.md`; rows: `BACKLOG.md`.
- e30-bootstrap (E3.0): [#1747] [#1748] [#1749]
- e30-phases-from-contract (E3.0): [#1689]
- e30-served-model (E3.0): [#1687]
- e30-rulings (E3.0): [#689] [#885], ADR-130
- e30-view-decide (E3.0): [#1748], ADR-133
- e30-actions-window (E3.0): [#1801]
- backlog-reconcile (E3.0): [#1749]
- e30-ci-verdict (E3.0): [#1747]
- e30-seat-registry-binds (E3.0): [#1845]
- codespace pin write (config-only hand landing, Q-PIN-1)
- e30-queue-runner (E3.0): [#1633]
- e30-conductor-phase-order (E3.0): [#1848]
- e30-commit-gate (E3.0): [#1800] [#1862]
- e32-provider-billing (E3.2): [#1833] [#1844]
- e31-system-view (E3.1): [#1748]
- e31-decide (E3.1): [#1811] [#1837] [#1838], ADR-124 ADR-133 ADR-134 ADR-139
- intake 123 SEED (E3.1 hand path), ADR-111
- e31-handoff-v5 (E3.0): [#1834], HANDOFF_BOOT boot_version 5
- e30-round-loop-dispatch (E3.0): [#1861]
- e30-distill-contract (E3.0): [#1855]
- e30-round-loop (E3.0): [#1856] [#1861]
- e30-backlog-legacy-sweep (E3.0): [#1854]
- e30-land-on-handback (E3.0): [#1859]
- e30-commit-gate-green (E3.0): [#1862]
- HAND-STEP Q-1862-R: [#1862]
- e30-round-verdict-handback (E3.0): [#1857]
- e30-landing-stage-receipts (E3.0): [#1858]
- N2 tasks-only follow-ups: close [#1800] [#1833] [#1854] [#1855] [#1856] [#1857] [#1858] [#1859] [#1861] [#1862]; file [#1866] [#1867] [#1868]
- A-1 hand step (N1): the operator's admission of copilot gpt-6.1-sol, [#1844]
- N4: ADR-140 r3 Accepted and row [#1869]
- S2: the 2026-11-05 session-close rows [#1865] [#1873]-[#1885]
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
Slot 1 - the first end-to-end run (M1 = 1): [#1879] (phase prompts state the Finding shape; run_phase fails loud), then one non-critical row through the conductor (admission), then the W-1 witness. With it: test dedupe (criterion <= 3 suite runs per landed change over 3 landings).
Slot 2 - [#1869] ADR-140 seat lifecycle on the stage0 path (model engine; T1 RED, CI, terra, judge sol); includes the logs/migrated ignore gap found at the close.
Beside the slots (read-only): Anthropic cloud sessions restored as the read-only substrate (trial: a backlog per-row sample with output on the transport); Copilot per-row backlog check.
Waits: Codespace (frozen; one whole-lane trial when a slot frees), graph/git memory at boot, mutation, trailers, Copilot cloud agent (verify the Enterprise-seat precondition only), corp-monorepo (gate E1-E7 = 0/7).
Lesson rows already filed: [#1882] L13, [#1883] L15 (no-stop table as code), [#1884] L16 (engine admission), [#1885] L17 (gate ledger).
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
