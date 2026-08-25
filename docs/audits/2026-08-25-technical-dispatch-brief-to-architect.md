# DISPATCH — COMPLETE BRIEFING · what shipped, how it works now, what you must standardize
**To: seat 2026-08-25-dev-knowledge-architect · From: operator + outgoing seat · 2026-08-25 · BINDING**
*This supersedes every earlier dispatch note. Everything you need is in this one document.*

---

## 0 · Why this exists
A browser architect has exactly one interface job: **author prompts and dispatch them.** ~30
consecutive seats failed at it and the operator re-explained it every time. That ends here.
Everything below is **measured** — two probe reports, one build report, five live runs. Your job
is not to re-derive it. Your job is to **write it into the repo so no future seat ever asks
again**, and to use it for this batch.

---

## 1 · What shipped today (measured, not claimed)

**The launch surface was never missing — it was quadrupled.** The hub documented FOUR rival
commands for one act (`Dispatch-Lane`, `dispatch <file>`, and two raw `claude --bg/--worktree`
forms). `/lane-boot:62` — the surface a seat most often invokes — emitted the form PLAYBOOK:2445
itself calls *"the FALLBACK form, not the default"*, silently dropping `--model` and `--effort`.
Seats were not uninformed; they were consistently informed by sources that disagree.
Evidence: `DISPATCH-SURFACE-MEASURED.md` (2083 lines, probed in three shells).

**Shipped in win-tooling (operator-owned repo, merged, pushed, 240+ tests green):**
- **Verbs renamed by SUBSTRATE**, one per substrate, every prior name kept as a working alias:
  `Dispatch-Local` · `Dispatch-Cloud` (Anthropic-hosted) · `Dispatch-Codespace` (GitHub).
- **`Dispatch-Codespace` BUILT and PROVEN end-to-end** — wraps `gh codespace create/cp/ssh`,
  receipt-gated, with `-IdleTimeout` / `-Retention` / machine-type cost guards. Run 4 created the
  machine, shipped contract + runner in, **executed inside the container**, and retrieved the
  receipt: `{"error":"claude is not installed in this devcontainer"}` (the runner's own guard,
  exit 91). The Codespaces substrate had a destination (`[#554]` devcontainer + prebuild) and
  **no transport at all**; that gap is closed.
- **`Ok` and `RemoteExitCode` separated.** `Ok` = the transport succeeded. `RemoteExitCode` = the
  work's own exit code, parsed from gh's `shell closed: exit status N` text (gh's own code is 1
  regardless, so reading it would report a meaningless number forever). A caller branching on
  `Ok` alone would read a failed lane as a success.
- **Bypass permissions enforced on every verb.** Verification caught that the Codespaces runner
  invoked `claude -p` with **no `--permission-mode` at all** — the first run reaching a working
  Claude would have stalled headless on a machine billing per minute. Fixed, with mutation-proven
  tests. Note the pedigree: same defect `Dispatch-Local` shipped with and fixed on 2026-08-20,
  reappearing on a new substrate because the flag moved somewhere the old tests don't look.
- **`dispatch <contract.md>`'s three-column table parse FIXED** (was 0-for-4 on hub contracts).

**Measured Codespaces wall-times (five runs, stable):** create returns **5.4–6.1 s** · Available
**~60 s** · cp-in **~74 s** (blocks until the container is up) · in-container run **5.9 s** ·
receipt out **6.2 s** · **total ~95 s** · machine `basicLinux32gb` · **~0.85 of 120 free
core-hours consumed across all runs.** Use these as **D1 evidence**.

---

## 2 · Ratified rulings — apply, do not relitigate
1. **`dispatch <contract.md>` is THE sole operator verb for a local lane** (it derives
   model/effort/worktree/label from the contract, so contract and command cannot disagree).
   `Dispatch-Local` (née `Dispatch-Lane`) is the documented manual fallback. The raw
   `claude --bg/--worktree` form is FALLBACK-ONLY and **never appears in a command file or
   template**. Interactive/primary-checkout sessions: `claude`, then one line —
   `Read <path> and execute it exactly.` (PLAYBOOK:2268).
2. **The lane-contract `Model` cell carries a MACHINE TOKEN from the model enum — never prose.**
   Human gloss moves to its own column or outside the table. Enforce in `gen_lane_contract.py`;
   update the contract template. (Today's four contracts write `Opus (opusplan default)`, which
   `dispatch` correctly refuses — hence they launch this batch via `Dispatch-Lane`. win-tooling's
   enum and its tests stay untouched.)
3. **Substrate-named verbs are canonical**; version-named ones (`Dispatch-CloudV2`) are aliases.
4. **STANDING RULE — every dispatch verb runs Claude with bypass permissions.** No permission
   prompt may ever block a lane, on any substrate. Inside a codespace this is sanctioned rather
   than merely tolerated: the blast radius is a disposable isolated machine holding a fresh clone
   and nothing of the operator's, deleted by its retention period.
5. **Codespaces credential = the SUBSCRIPTION OAuth token, not a Console API key.**
   Secret name **`CLAUDE_CODE_OAUTH_TOKEN`** (from `claude setup-token`; ~1-year; model-requests
   only; **usage counts against the operator's plan — no separate API invoice**). The operator has
   **already set it** as a user-level Codespaces secret scoped to this repo. **Never introduce
   `ANTHROPIC_API_KEY` into the image or its config** — when both are present the API key takes
   precedence and would silently flip billing off-subscription. Register-section note: the token
   grants the operator's subscription model access to any lane running in that container;
   rotation = re-run `setup-token`; expiry ~1 year.
   *Contingency, recorded: if smoke 5 shows headless `claude -p` refusing the subscription token
   inside the container, the fallback is a spend-capped dedicated API key — but only on that
   measured evidence, never preemptively.*

---

## 3 · The two remaining blockers — BOTH YOURS, fold into THIS batch
| # | Blocker | Shape |
|---|---|---|
| **ACT 1** | **Claude Code is not installed in the devcontainer image** — zero "claude" occurrences across `devcontainer.json`, `Dockerfile`, `provision.sh`, `provisioning.yaml`; **confirmed by the container in its own words** | One feature or one `RUN` line in `.devcontainer/Dockerfile`. Derive the current documented Linux install path from code.claude.com and **quote the doc line in the commit** — never invent the command. Pin what is pinnable. |
| **ACT 2** | **No credential path into the container** — no `secrets` / `containerEnv` / `remoteEnv` key exists; the `containerEnv` block was deliberately removed under `[#554]` (`devcontainer.json:53-70`) and **that removal was correct and stays** | Reference the already-created `CLAUDE_CODE_OAUTH_TOKEN` Codespaces secret via the mechanism Codespaces documents for user secrets. Do **not** resurrect the removed self-referential `containerEnv`. Land the exposure/rotation note as a register section in the same commit. |

**DONE-WHEN (this batch's hard end-state for Codespaces):** **smoke run 5** via
`Dispatch-Codespace` returns **`Ok=True` AND `RemoteExitCode=0`** with a receipt carrying the
audit check count **from inside the container** — the first fully green lane on Codespaces. Land
its wall-times as D1 evidence. Then the substrate table's Q4 default becomes real.

---

## 4 · Standardization mandate — the part that must not slip
The browser cannot function without this knowledge and it evaporates at every handoff. Make it
**readable instead of rememberable**:

1. **PLAYBOOK Ch8 becomes the SINGLE literal-command site.** It already is the operator page
   (§2225-2278, landed 2026-08-23) — the fix is not a new runbook. Rewrite its table to carry,
   per substrate: the verb, its exact argument shape, where the contract file lives, the success
   receipt, and the cost guards. Every other site becomes a pointer:
   `templates/prompt-template.md:113`, the two other PLAYBOOK sites, and **`/lane-boot:62`**.
2. **`/lane-boot` must emit the ruled verb**, never the raw form. It is the most-invoked surface
   and today it teaches the retired one.
3. **Boot forces the read:** `HANDOFF_BOOT.md` step 0 points at Ch8; the bundle template carries
   the pointer; `/handoff-verify` gains one probe (Ch8 present + its commands resolve).
4. **Drift organ:** a fire-test-shaped check asserting that every literal command in Ch8 resolves
   via `Get-Command` on the operator's machine, and that `/lane-boot` contains the ruled verb. A
   doc naming a dead or rival command goes RED.
5. **Land three artifacts in `docs/audits/`** with this batch: `DISPATCH-SURFACE-MEASURED.md`,
   `DISPATCH-CONSOLIDATION-PLAN.md`, `DISPATCH-CODESPACE-REPORT.md`.

### 4a · SUBSTRATE DECISION TREE — two layers, both required

**LAYER 1 — Ch8 carries the decision table** (for humans AND for a fresh browser seat), cut in
this order, **first match wins**:

| | Question | Route |
|---|---|---|
| **Q1** | Does the result depend on a gate (suite / hooks / ship-gate)? | **NEVER cloud** — measured: no hook armed there, unpinned `uv`, no `click`. Codespace or local. |
| **Q2** | Does it need operator-disk state (Downloads contracts, authenticated provider CLIs, unpushed branches), or is it an operator-gated act (merge, push, integration)? | **LOCAL**, stop. |
| **Q3** | Is it read-only / reconnaissance (censuses, verification, fan-out)? | **CLOUD** — own clones, cheap, unlimited parallelism. |
| **Q4** | Everything else — repo-mutating, disk-independent | **CODESPACE** (the default once ACT 1 + ACT 2 land). |

Each row states its verb, concurrency ceiling and cost note:
- **local:** one WRITER per checkout; parallel only across worktrees.
- **codespace:** 2–4 concurrent (2-core, ~60 s to Available, 120 free core-hours/month ≈ 60 h).
- **cloud:** effectively unlimited (own clones); never for gate-dependent work.
- **Batch ceiling stays 4–6 lanes** regardless of substrate — bounded by integration capacity.

**LAYER 2 — THE VALIDATOR** (this is what makes it real; prose alone is a request). Extend the
substrate registry check so a lane contract is **REFUSED** when its declared substrate
contradicts its own content:
- declares a substrate with **no live verb** → REFUSE (today's Codespaces case, until ACT 1+2)
- declares **cloud** AND names a gate/suite/hook in its Done-when → REFUSE
- declares **codespace/cloud** AND references an operator-disk path (`C:\Users\...`, `~\Downloads`)
  → REFUSE
- declares **local** AND the batch already has another local WRITER on the same checkout → WARN

A seat may override only with an **explicit, recorded deviation line** — never silently.
**Done-when:** a seat that forgets the tree still cannot ship a wrong-substrate contract, because
the repo says no and names the rule.

---

## 5 · Use it in THIS session
Launch this batch with the ruled verbs (you already emitted the four launch lines; they stand).
Record in each lane report which verb launched it.

**Two defects to carry, not to fix silently:**
1. `Dispatch-Codespace`'s name lookup previously took `[0]` of display-name matches — **fixed**;
   an ambiguous display name is now a refusal naming every candidate and its state.
2. `test_worktree_hygiene::test_installer_whatif_registers_nothing` asserts the **ABSENCE of
   machine-global state**, so it turns RED the moment the feature it guards is genuinely adopted.

**Feed the R-F4 sweep two fresh exemplars (n=2 each family):**
- *green-by-skip*: a check that cannot compute its ground truth must FAIL, never skip.
- *absence-asserting tests*: a test that passes only until the thing it guards is adopted.
- *flag lost across substrates*: a discipline proven on one transport silently absent on the next,
  because the assertion looked at the old artifact. Tests must read the artifact actually shipped.

---

## 6 · Acceptance test for the whole standardization (the operator judges)
A person who has never seen this fleet dispatches one lane **on each substrate** using ONLY
PLAYBOOK Ch8 — zero questions asked. Until then the interim rule binds: **no seat emits a launch
command that is not a verbatim quote from Ch8, the measurement report §6, or the operator's own
message.** Inventing one is a defect, not a workaround.
