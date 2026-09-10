# LANE lane-w-683-override-manifest-node — The /override manifest node and its payload go together, and release_lint proves they cannot part.

| Model | Mode | Effort |
|---|---|---|
| opus | plan | high |

## Dispatch

**Shape:** `codespace` — an off-machine lane in the repo's own devcontainer, receipt-gated, committing on the `worktree-` prefix like a local lane.

```
Dispatch-Codespace -Contract LANE-w-683-override-manifest-node.md -Slug lane-w-683-override-manifest-node
```

The operator runs the line above verbatim. The contract is shipped IN **as a
file**, and so is the runner: nothing on the ssh command line is a quoted
payload, because a PowerShell string reaching a bash login shell through gh's
transport is parsed twice. Tier is on the record in the routing table above
(`opus` / `high`) — `Dispatch-Codespace` carries no `-Effort`.
Permission mode is `bypassPermissions`, as on every substrate.
**The container is CREATED, never rebuilt** (ruling 2026-08-31): a rebuilt
container has not applied its own `devcontainer.json` — no features, no
`postCreateCommand`, a stale clone — while a fresh create from the same HEAD
applies all of it. The clone starts at `origin`, so every input this contract
names is pushed before dispatch. Cost flags (`-Machine`, `-IdleTimeout`,
`-Retention`) are the operator's at dispatch and are deliberately not frozen
here; board label `[.dev-knowledge · #683 · lane-w-683-override-manifest-node]`.

## Worktree pairing

slug `lane-w-683-override-manifest-node` -> branch `worktree-lane-w-683-override-manifest-node` -> contract `LANE-w-683-override-manifest-node.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). A codespace lane runs on `worktree-`, the SAME prefix as a local lane and not
the cloud transport's `claude/`: it commits and pushes like a local lane,
merely elsewhere, so `claude/` would name a branch nothing creates (R-ENUM
leg 3, 2026-08-31). Off-machine and cloud are different axes.

## Receipt gate

This lane runs off-machine in the repo's own devcontainer, so it carries a receipt
(`protocols/STANDING_RULINGS.md` Q5) — `receipt.json`, pulled back out. Both
fields, checked as a conjunction — either one alone reports a success the other
refutes:

- `transport-ok-and-remote-exit-code-read-separately:` `<Ok=…, RemoteExitCode=…, read separately>`
- `is-error-false-not-subtype-success:` `<is_error, verbatim from receipt.json>`

`Ok` is the TRANSPORT's verdict and `RemoteExitCode` is the WORK's: gh's own exit
code is 1 regardless, so a caller branching on `Ok` alone reads a failed lane as a
success. And a receipt can carry a success `subtype` while `is_error` is true, so
`is_error` is the verdict field and `subtype` is the trap — a consumer keying on
`subtype` records a successful run of an agent that never ran. A dispatch missing
either half is treated as not having started, and is re-dispatched into a FRESH
container (created, never rebuilt).

## Sequencing

**HELD: starts on `GO delete`**, not on `GO W`.

## Frozen intent -- VERBATIM from `BATCH-2026-09-10-W-CONTRACTS.md`

> Carried byte-for-byte from the batch render (CC, amended in place by AW-1..AW-4, A6-1, A7-1/A7-2/A7-6 and AW2-1..AW2-3). This is the lane's authoritative content; the sections around it are the dispatcher's skeleton, which is all the dispatcher owns.

## W-4 · `[#683]` — the `/override` manifest node and its payload go together

- **Row.** **`[#683]`** — resolved by title from `docs/intake/2026-09-10-tech-review-consumption.md`
  ("/override"; P1, M, `[E2]` / `[S8]`).
- **HELD: starts on `GO delete`.** Does not start on `GO W`.
- **Intent.** `/override` was RETIRED by the ADR-85 amendment 2026-08-03 §A2 and its own description
  says it discharges no gate, yet it remains a node in `deploy/manifest-v1.5.0.yaml` (:995-1004) with
  a payload behind it, so every fully-deployed consumer installs a working-looking escape hatch that
  escapes nothing. **Node and payload are one act:** removing the node alone orphans the payload in
  the carried corpus, removing the payload alone leaves a node pointing at nothing — which is what
  `deploy/release_lint.py` catches.
- **Done-when (verbatim from `[#683]`).** *"node absent, payload absent, `release_lint.py` green, one
  test fails if either returns"*
- **Closure.** manifest node **present → absent** · payload **present → absent** · `release_lint.py`
  **→ green, witnessed** · regression test **absent → present, RED if either returns** · ship-gate
  undispositioned WARNs **46 → ≤ 45, re-derived on the primary (AW2-3)**.
- **Anti-patterns.** Do not remove one half and file the other. Do not tag `v1.5.0` —
  `AMEND-SESSION-PLAN-004` A4-7 puts the tag **after** this removal, the tag does not exist today
  (highest release tag is `v1.4.0`), and tagging is the operator's act. Do not touch `[#670]`/Stage
  10, which needs the tag this row precedes. Do not regenerate `.claude/methodology-roster.md` by
  hand — it is generated (`gen_methodology_roster.py --write`) and `roster-freshness` gates it. Do
  not widen the deletion: the GO covers `/override`, and `/override` only.
- **AW-4 applies.** The codespace receipt is a RED list; `release_lint.py` green and the ship-gate
  WARN delta are re-derived by the integrator on the Windows primary before merge.
- **AW2-3 — the acceptance addendum, verbatim.** *"W-4 acceptance addendum: closing `[#683]` must
  clear the `doc_rot` backlog-accretion WARN it raised at 1c27ad4f (ship-gate back to ≤ 45
  undispositioned)."* **Filing the row is what raised it** — 45 → 46 at the review-consumption merge —
  so closing the row is what clears it, and the delta belongs to this lane's acceptance rather than to
  a follow-up nobody owns. It is re-derived on the Windows primary with the rest of AW-4's list; a
  container's count is a RED list, never the verdict.
- **MODE: plan.** Basis (DECLARE §2): deletion plus a manifest edit.
- **SUBSTRATE: CODESPACE — cut at Q4, ratified by AW-4.** Q1 fires *not-cloud* (`release_lint.py`
  plus the `roster-freshness` and floor-hash gates). **Q2 does not fire, and the reason is worth
  stating because it looks like it should:** the deletion GO is an operator gate at **dispatch**, not
  operator-disk state the lane reads and not one of Q2's operator-gated *acts* (merge, push,
  integration). Both targets — `deploy/manifest-v1.5.0.yaml` and `.claude/commands/override.md` — are
  tracked in-repo. Q3 does not fire: the lane mutates. Q4 → CODESPACE.
- **Pointer.** AW-4 · `docs/audits/2026-09-10-technical-night-aj-m03/REVIEW.md` :56 finding, :79
  pointer · ADR-85 amendment 2026-08-03 §A2 · `deploy/release_lint.py` · `[#644]` context · `[#670]`
  (Stage 10).
- **Budget: 2.** Regression-test placement; how the floor hash sidecar is re-derived after the payload
  leaves. A third fork = commit-and-STOP.

## Done-contract (immutable)

**The Done-when and Closure legs are carried VERBATIM in "Frozen intent" below and are this lane's acceptance.** They are not restated here, because a restatement is a paraphrase and the legs are quoted text.

1. Every **Done-when** leg quoted in the frozen body below holds, witnessed.
2. Every **Closure** transition in the frozen body below is carried to its right-hand side.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green via `uv run --locked`.

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. RED first: write the regression test that FAILS if either the manifest node or the payload returns. **COMMIT**
2. Remove the `/override` node from `deploy/manifest-v1.5.0.yaml` (:995-1004) AND its payload `.claude/commands/override.md` -- **node and payload are ONE act**. Regenerate `.claude/methodology-roster.md` with `gen_methodology_roster.py --write` (never by hand) and re-derive the floor-hash sidecar. **COMMIT**
3. Run `deploy/release_lint.py` and witness it green. Do **not** tag `v1.5.0` -- the tag is the operator's act and follows this removal. **COMMIT**
4. Final: emit the receipt as a **RED list, never a verdict** (AW-4); the `release_lint.py` green and the ship-gate WARN delta (46 -> <= 45, AW2-3) are re-derived by the integrator on the Windows primary. One end-of-lane artifact. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
