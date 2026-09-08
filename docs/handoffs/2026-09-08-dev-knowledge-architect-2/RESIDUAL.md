# Residual — 2026-09-08-dev-knowledge-architect-2 — the part the repo does not already encode

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

> **Standing vs NEW — generated, names only.** Three lists computed from `ecosystem/disposition-register.yaml` ∩ this window's own diff. **No verdict, count, stale-disposition line, sha or backlog id appears here** — those are P7/P4/P6/P9's live answers and the evidence block carries them. The frame covers the standing-WARN family only; an organ outside it is the FILL-IN's business, not silently filed as standing.

**Window** — the diff since `docs/handoffs/2026-09-08-dev-knowledge-architect/` was added.

**Dispositioned by the register.** The register already carries an entry for these organs, so a WARN from one is standing unless its evidence signature is new:
- `no_ff_merges`
- `journal_spine_anchor`
- `doc_rot`
- `undeclared_edges`
- `funnel_coverage`

**Dispositioned by absence from the window diff.** This window touched nothing these organs read, so a WARN from one is not this window's doing:
- `reconciled_versions` (reads the registered specs and the docs declaring a `reconciled_with:` edge)
- `fleet_parity` (reads the parity-surface manifest and the surfaces it names)

**NEW-and-undispositioned.** No register entry, and this window DID touch what they read — so a WARN from one of these is this window's, and the note below says which is a decision rather than a defect:
- _(none)_

<!-- FILL-IN:driftflags START (hand-authored — ONE judgment only: name which NEW flag above is a DECISION rather than a defect. The standing-vs-new attribution is GENERATED directly above; do not restate it. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->**`reconciled_versions` is the DECISION, not the defect.** This window changed `/handoff` preflight behaviour twice under operator ruling and did **not** bump `HANDOFF_PROCESS.md`'s `Version:`. `DECLARE-BOOT-REVIEW-2026-09-08.md` defect 1 rules it explicitly: declare 7.1.0 at the first sitting, re-stamp `reconciled_with`, re-issue the PIN. So the flag is a filed obligation with a ruling and an owner, not drift nobody noticed. `fleet_parity` is the other NEW organ and is **not** claimed as a decision: this window added no parity surface, so a WARN there would be a defect to investigate, and P7 is what says whether one fired.<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->Two gate amendments, the row they required, and a superseded bundle. Detail is in `JOURNAL.md` 2026-09-08 (e), (f), (g); this is the map.

- **preflight row 1** -- `hard-fail = 0 AND every undispositioned WARN named in the residual with its owning row`. Ruling `to-cc/DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08.md`. A handoff is not a release; the TAG gate's GREEN criterion (NC1 / 028-A) is unchanged.
- **preflight row 7** -- `ANSWERED (an ANSWER-*/DECLARE-* answers it) OR CARRIED (named in the residual with the OPEN backlog row that owns it)`; a CLOSED row does not carry, no owner is a FAIL. Ruling `to-cc/DECLARE-PREFLIGHT-QUESTION-ROW-2026-09-08.md`.
- **`[#642]`** (P1/S, new) -- the receiving surface the row-7 ruling presupposed and the repo did not have.
- **This bundle supersedes `2026-09-08-dev-knowledge-architect`**, which failed its own verify on P0c (Purpose named backlog rows, not an enumerated authority), P8a (5 of 7 answers cited no file) and P11 (two DECLAREs carried no `carried-by:`). All three are cleared here: the gate caught them, which is the gate working.<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->**FIRST, before any batch: the consolidated suite has not run.** Six OOM kills this window
(~2.6-3.5 GB free of 28 GB, held by OneDrive/VS Code/Chrome -- the operator's machine, not the
fleet's); one took a bundle generation mid-preflight. Targeted tests, the full pre-commit battery
and the ship-gate all ran and passed; the *consolidated* run is the one thing nobody has
witnessed. It runs first.

**The debt handed over is OWNED -- the point of both amendments.**

*Ship-gate remainder: `[#638]` (P2) owns all four.* All four undispositioned findings are
`proof_layer` and render **identically**, which is why `[#638]` says no honest narrow `match`
exists: *`test_review_artifact_coverage.py` gates 1 test behind a function-level `skipif` on
`git`*. Fix, not suppression: move the property out from behind the guard, or make a skipped
proof render NOT-PROVEN. **No verdict or count is stated here -- P7 re-derives both live.**

*Carried questions, each with the OPEN row that owns it* (row 7's contract; files under
`to-browser/`, 2026-09-07 archive unless noted):

- `dispatcher-N2` -> `[#610]` (missing-manifest half) + `[#642]`
- `dispatcher-T` -> `[#628]`. **Answered in full** by `DECLARE-SITTING-2026-09-06`; reads as
  carried only because its disposition cites `[#628]` for the D12 ask. True, not a defect
- `integrator-N2-win-tooling-merge` -> `[#642]` (RAW vs UNRESOLVED HIGH)
- `lane-t-000-reds-spine` -> `[#642]` (does the batch-T GO discharge AF-1's owed ADR-98 intake)
- `lane-u-000-adr-carrier-split` -> `[#642]` (ADR-117: keep `Proposed`, admit `DRAFT`, or should
  not have landed)
- `lane-u-000-branch-enum-parity` -> `[#642]` (are the two ADR-85 organs SUPPOSED to differ)
- `lane-u-000-carrier-floor-v150-mechanisms` -> `[#642]` (`INSTALL.md` into
  `root_allowlist.files`, or retire the root path)
- `lane-u-000-deploy-tool-consumer-override` -> `[#605]` (its body names the same
  `deploy/tool.py` consumer-root site) + `[#642]`
- `lane-u-000-dispatch-receipt-is-work` -> `[#642]` (does `gh auth status` OK gate `absent`; may
  a lane DEPLOY to the operator's host)
- `lane-u-000-handoff-v71-build` -> `[#642]` (the 7.0.0 -> 7.1.0 bump + 3 re-stamps are OWED;
  **ruled** by `DECLARE-BOOT-REVIEW-2026-09-08.md` defect 1 -- declare 7.1.0 at the sitting)
- `lane-u-000-shape-spec-finalize` -> `[#642]` (does the spec landing warrant a version bump)
- `lane-u-628-release-commit` -> `[#642]` (`reconciled_with` on an intake doc; a standing
  silent-rule ratchet headroom, currently ZERO)
- `handoff-cut-2026-09-08` (live) -> ANSWERED by `DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08`

**`[#642]` receives; it rules nothing.** Filed because the row-7 ruling named a "ratification list
row" that did not exist -- measured, not assumed: `RATIFICATION-2026-09-08.md` names none of the
eleven, and `docs/audits/2026-09-07-technical-batch-u-close-packet.md`, the one carrier that would
have covered them all, names **no QUESTION file at all**. Owner of record: this window's first
sitting. Rows 604 and 447 were checked and rejected as owners.

**Two decision files on the transport are OPEN carriers, named here because P11 requires it.**
`DECLARE-BOOT-REVIEW-2026-09-08.md` states its carrier (`[#642]` + the batch V docs lane) *inside*
its HTML comment rather than flush-left, and `AMEND-037-001.md` names none. Both arrived after
this window's carrier pass; neither was edited by this seat. Their carriers are **OPEN** and the
first sitting closes them -- which is the exact disposition P11 provides for a decision with no
repo home yet.

**Ten ratification seals still PENDING and unchanged** (`to-browser/RATIFICATION-2026-09-08.md`
section 1) -- nine of ten pending at the 2026-09-07 dawn list, nine of ten now; no sitting between.
`[#640]` owns seals 3 and 7, `[#641]` seal 10. `protocols/ESSENTIALS.md` is **not retired** --
census 52 consumers; re-point lane in batch V (D9 stands).<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
