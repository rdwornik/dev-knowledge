# Lane ac-694 (insurance leg) — landed-vs-claimed verification

**Lane:** `lane-ac-694-insurance-census` · **Branch:** `worktree-lane-ac-694-insurance-census` ·
**Batch:** AC · **Date:** 2026-09-18 · **Scope:** read-only verification, no rows edited

## 1 · Question

For `[#665] [#666] [#667] [#668] [#669] [#670] [#760] [#755] [#628]`: quote each row's live state
against what actually landed, and resolve the two-owner contradiction on the `ESSENTIALS.md`
deletion between `[#755]` and `[#628]`.

## 2 · Per-id verdicts

| id | row's live claim | what actually landed | verdict |
|---|---|---|---|
| `[#665]` | Step A — chapter map of PLAYBOOK/ARCHITECTURE, gating steps B–G | No chapter-map artifact exists in the tree; correctly the gating blocker for the rest of the recovery plan | UNDERSTATED — status OPEN is right, but nothing downstream can start honestly until this lands |
| `[#666]` | Step B — per-chapter keep/merge/cut ruling, one sitting/one file | Depends on `[#665]`; no ruling file exists | MATCHES (OPEN, correctly blocked) |
| `[#667]` | Step D — ARCHITECTURE rendered, PLAYBOOK by chapter, DISPATCH split out, ESSENTIALS gone | ESSENTIALS.md: deleted (true). `protocols/DISPATCH.md`: does **not** exist — dispatch content is still inside PLAYBOOK.md (false). ARCHITECTURE ≤15 KB: false — live at 110,357 B | CONTRADICTS — 2 of 3 remaining claimed acts have not landed |
| `[#668]` | Step E — paste test becomes a scored eval | Depends on `[#667]`; no eval/scoring artifact deployed | MATCHES (OPEN, correctly blocked) |
| `[#669]` | Step F — the conductor: delivery-loop transitions as a state machine | Depends on `[#664]`; no state machine deployed | MATCHES (OPEN, correctly blocked) |
| `[#670]` | Step G — floor v1.5.0 reaches corp-monorepo | Depends on `[#644]` (deploy-freeze decision); no deploy attempted | MATCHES (OPEN, correctly blocked) |
| `[#755]` | Finish the docs cut — ARCHITECTURE ≤15 KB + 4 ESSENTIALS residues | ESSENTIALS.md deletion landed (16,461 B removed, per its close-packet audit); 5 residual items (A–E: floor-template prose, manifest `doc_shapes` rows, AI_COUNCIL_PROCESS history, STANDING_RULINGS T-29 premise, PLAYBOOK prose stamp) documented as **not** discharged by this row, handed to `[#628]` | UNDERSTATED — correctly OPEN; the audit itself records the residues as still-open work, not silently dropped |
| `[#760]` | X3 — ARCHITECTURE ≤15 KB behind the step-D render, from a 100.8 KB starting measurement | Current ARCHITECTURE.md: 110,357 B — **grew back** since `[#755]`'s post-cut figure (its own close-packet cites 95,288 B), and the X3 wave has not executed | MATCHES (correctly OPEN; filed 2026-09-14 as a separate wave once `[#667]`'s target was ruled unmet) |
| `[#628]` | DC-2 re-cut — dissolving ESSENTIALS.md is a fleet-coupled release act | File-deletion half discharged 2026-09-14 (by `lane-y-755`'s execution). Release-coupled half (floor-sha regen, `deploy/release_lint.py` C5 checks, pinned-manifest updates) **not done** — sequenced behind the v1.5.0 release, itself blocked by `[#644]` | MATCHES — merge commit `b7796` states explicitly: *"`[#628]` does NOT close — deletion discharged, floor sidecar and pinned manifests are a release act; the row stays open"* |

## 3 · ESSENTIALS.md two-owner resolution

**CLAUDE.md §2 currently states:** *"`protocols/ESSENTIALS.md` was **deleted 2026-09-14**
(`[#628]`)"* — attributing the deletion to `[#628]`.

**`[#755]`'s own task file** states the lane it ran under "deleted `protocols/ESSENTIALS.md`
(16,461 B) and closed `[#628]` on the file's absence" — but the merge commit for that lane
(`b7796`, 2026-09-14) explicitly says the opposite: `[#628]` does **not** close on the deletion.

**Verdict: not a genuine contradiction — a sequencing, with an imprecise attribution in
`CLAUDE.md`.**

- `[#628]` owns the *concept*: dissolving ESSENTIALS.md as a fleet-coupled release act (floor-sha
  regeneration, `release_lint.py` C5, pinned-manifest updates across versions).
- `lane-y-755` (running under `[#755]`'s scope) executed the mechanical half — the file delete and
  39-surface re-point (CLAUDE.md, templates, PLAYBOOK, HANDOFF_PROCESS, ARCHITECTURE, etc.) — per
  `docs/audits/2026-09-14-technical-batch-y-launch-contracts/LANE-y-755-docs-cut-finish.md` §1.1–1.2
  (commit `e791cffc`). `release_lint --version 1.5.0` showed 0 FAIL / 7 pass / 1 WARN, unchanged by
  the deletion — consistent with the release-coupled half genuinely not having fired yet.
- `[#628]` stays OPEN by explicit operator ruling in the merge commit, for the release-coupled part
  the deletion didn't (and structurally couldn't, being blocked on `[#644]`) reach.
- **Finding, not a fix (out of scope for this read-only lane):** `CLAUDE.md`'s parenthetical
  `(`[#628]`)` after "deleted 2026-09-14" is misleading as written — it reads as "this id is
  responsible for and closes on the deletion," when the deletion landed under `[#755]`'s lane and
  `[#628]` explicitly does not close on it. Recommend the operator correct the attribution (e.g.
  "deleted 2026-09-14 by `lane-y-755` for `[#755]`; `[#628]` owns the still-open release-coupled
  dissolution") rather than leaving the current phrasing to be read literally.

## 4 · Caveats

- Verified against file existence, the cited merge commit's message, and the two named
  close-packet audits — not against every commit in the ranges, so a later undocumented revert
  would not be caught here.
- `[#665]`/`[#666]` verdicts rest on absence-of-artifact checks (no chapter-map/ruling file found);
  a file living somewhere outside the searched conventions would overturn them.
