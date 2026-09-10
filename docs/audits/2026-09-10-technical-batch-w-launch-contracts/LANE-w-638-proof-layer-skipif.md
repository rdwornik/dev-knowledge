# LANE lane-w-638-proof-layer-skipif — The four proof_layer properties come out from behind the skipif, or a skipped proof reads NOT-PROVEN.

| Model | Mode | Effort |
|---|---|---|
| opus | plan | high |

## Dispatch

**Shape:** `codespace` — an off-machine lane in the repo's own devcontainer, receipt-gated, committing on the `worktree-` prefix like a local lane.

```
Dispatch-Codespace -Contract LANE-w-638-proof-layer-skipif.md -Slug lane-w-638-proof-layer-skipif
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
here; board label `[.dev-knowledge · #638 · lane-w-638-proof-layer-skipif]`.

## Worktree pairing

slug `lane-w-638-proof-layer-skipif` -> branch `worktree-lane-w-638-proof-layer-skipif` -> contract `LANE-w-638-proof-layer-skipif.md`

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

Dispatches in the **first wave, on `GO W`** (AW-1 order of start).

## Frozen intent -- VERBATIM from `BATCH-2026-09-10-W-CONTRACTS.md`

> Carried byte-for-byte from the batch render (CC, amended in place by AW-1..AW-4, A6-1, A7-1/A7-2/A7-6 and AW2-1..AW2-3). This is the lane's authoritative content; the sections around it are the dispatcher's skeleton, which is all the dispatcher owns.

## W-3 · `[#638]` — the four `proof_layer` properties come out from behind the `skipif`, or a skipped proof reads NOT-PROVEN

- **Row.** **`[#638]`** (P2, S, `[E2]` / `[S3]`).
- **Intent.** Four function-level `skipif`-on-`git` guards in `tests/test_review_artifact_coverage.py`
  render byte-identically in `proof_layer.ratchet_findings`, which names the module and the gated-test
  count but never the guard key. No `#147` register `match` is narrow enough to be honest: one entry
  would suppress all four **plus the next guard added to that module**, which is the whole-Finding
  masking the register's own contract forbids. Lane C-1 left them a NAMED REMAINDER rather than write
  a dishonest disposition. Either route the properties out from behind the guard, or make a skipped
  proof render NOT-PROVEN — **never suppress**.
- **Done-when (verbatim from `[#638]`).** *"(a) `ratchet_findings` carries the guard KEY in its
  evidence so a disposition can be per-guard, and (b) the four guards are ruled on their merits - the
  module's subject IS git-derived data, which is the "a guard on the tool that is the subject may
  still be self-policing" question `scripts/proof_layer.py` raises about itself - and
  `ecosystem/proof-layer-baseline.json` is re-stamped, or the properties are routed out from behind
  the guard"*
- **Closure.** `ratchet_findings` evidence carries the guard KEY **no → yes** · the four guards
  **undispositionable → ruled on their merits, each ruling recorded** · baseline **re-stamped with
  its measured count printed, or the properties routed out and the baseline unchanged**.
- **Anti-patterns.** **Do not write a `#147` register entry that matches the module** — that is the
  exact dishonest disposition C-1 refused, and it silently absorbs every future guard in the file. Do
  not delete the guards to make the count move. Do not re-stamp the baseline against a RED population
  the batch has not agreed: `[#638]`'s baseline was stamped at `2d531321` (243 guards, 247 live, 0
  dropped).
- **AW-4 resolves the substrate risk this lane was carrying, and the resolution is a rule, not
  reassurance.** The first render flagged that a container whose RED set differs from the batch
  baseline would re-stamp against the wrong population and look clean. **AW-4 makes the container
  structurally incapable of deciding that**: the codespace receipt is a RED list, the acceptance
  verdict is re-derived by the integrator on the Windows primary, and FR-8 already forbids Codespaces
  as a comparison base. **The lane therefore does not re-stamp the baseline from a container reading
  at all** — it prepares the re-stamp with its measured count printed, and the stamp is taken from
  the primary's re-derivation at integration.
- **MODE: plan.** Basis (DECLARE §2): touches the audit-py group; ADR-108 §B RED-first.
- **SUBSTRATE: CODESPACE — cut at Q4, ratified by AW-4.** Q1 fires *not-cloud* (the result depends on
  the ship-gate ratchet). Q2 does **not** fire: no operator-disk state, no vendor CLI, and the lane
  performs no merge, push or integration — that is the integrator's act from the primary. Q3 does not
  fire: the lane mutates. Q4 → CODESPACE, `execution = CODESPACE` being the default since the
  2026-09-01 `[#632]` n=2 acceptance.
- **Pointer.** AW-4 · FR-8 (`docs/intake/2026-09-09-tech-window-close-rulings.md:83`) · `[#596]` ·
  `scripts/proof_layer.py` · `scripts/audit_checks/check_proof_layer.py` ·
  `ecosystem/proof-layer-baseline.json` · `#147` register contract · batch CLOSE lane C-1
  `shipgate-to-green` (measured on main `a415d720`).
- **Budget: 2.** Guard-key evidence format; route-out vs re-stamp, where the merits are genuinely
  balanced. A third fork = commit-and-STOP.

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

1. RED first: make `ratchet_findings` carry the guard KEY in its evidence, so a disposition can be per-guard. **COMMIT**
2. Rule the four `skipif`-on-`git` guards in `tests/test_review_artifact_coverage.py` on their merits, recording each ruling: route the properties out from behind the guard, or make a skipped proof render NOT-PROVEN. **Never suppress**, and write no `#147` register entry that matches the module. **COMMIT**
3. Prepare the baseline re-stamp with the measured count PRINTED -- **do not re-stamp from the container reading** (AW-4). The stamp is taken from the primary's re-derivation at integration. **COMMIT**
4. Final: emit the receipt as a **RED list, never a verdict** (AW-4), targeted tests green, one end-of-lane artifact. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
