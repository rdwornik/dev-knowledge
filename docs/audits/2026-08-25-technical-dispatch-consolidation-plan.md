# DISPATCH CONSOLIDATION — the systemic plan · for seat 2026-08-25-dev-knowledge-architect
**Sources, both to be landed in docs/audits/ with this plan:** `DISPATCH-SURFACE-MEASURED.md`
(2083 lines, probed 2026-08-25) + the operator-playbook research report (Claude Code invocation
mechanics, orchestration prior art, Codespaces-via-gh patterns). **This AMENDS
SYSTEMIC-FIX-DISPATCH.md with what measurement forced** — three of its assumptions were wrong and
are corrected in §5. Nothing below is from memory; every claim carries the report's locator.

## 0 · The measured diagnosis, in one breath
`Dispatch-Lane` works everywhere (module DispatchHelpers v1.1.0, auto-loading, SHA-256-deployed,
zero drift — report §1). The intended one-liner `dispatch <contract.md>` works on its own fixtures
2-for-2 and fails 0-for-4 on hub contracts because of ONE regex expecting a two-column
`| Model | opus |` row where the hub writes `| Model | Mode | Effort |` (§3.4,
`Invoke-Dispatch.ps1:364-369`). The repo documents FOUR rival launch commands for one act
(§ VERDICT), `/lane-boot:62` — the surface a seat most often invokes — emits the form
PLAYBOOK:2445 itself calls "the FALLBACK form, not the default" while silently dropping
`--model`/`--effort`. Contracts are hand-authored in `~/Downloads`, so `gen_lane_contract.py`
(which already emits correct lines, with a test forbidding their absence — §4.9) and every
commit-time gate are structurally blind to them (§5.3). Codespaces has NO launch command on any
surface while two of today's contracts mandate it (§ SUBSTRATE 5). **Thirty seats were not
uninformed; they were informed by four sources that disagree. Only collapsing four onto one
converges this.**

## 1 · TODAY — launch the current batch (no repo change needed)
Use the measurement report's **§6 COPY-THIS CARD** verbatim — it is probed, current, and covers
every shape in today's batch:
- **LANE-RL and INTEGRATE (primary-checkout, interactive):** substrate-6 shape —
  `claude`, then `Read <path> and execute it exactly.` (PLAYBOOK:2268-2278; the one shape with no
  conflict found).
- **LANE-G and LANE-X (worktree lanes; Codespaces-mandatory clause already operator-waived to
  LOCAL):** `Dispatch-Lane <slug> <contract.md> -Effort high` with a slug beginning `lane-` so the
  produced `worktree-lane-*` branch satisfies the hub grammar (§ SUBSTRATE 1, discrepancy (c)).
  Record in each lane's report: "launched via Dispatch-Lane per DISPATCH-SURFACE-MEASURED §6;
  Codespaces deviation operator-approved; devcontainer wall-time measurement carried to wave 2 as
  named debt."

## 2 · THE RULING TO PUT TO THE OPERATOR (one sentence, this batch)
Report §7.3 states it exactly: four rival forms is the root cause; picking one is a ruling, not
an implementation. **Proposed ruling:** *`dispatch <contract.md>` is THE sole operator verb for a
local lane; `Dispatch-Lane` remains the documented manual fallback; the raw `claude --bg/--worktree`
form is FALLBACK-ONLY and never appears in a command file or template; interactive seats keep the
substrate-6 shape.* Rationale: `dispatch` derives model/effort/worktree/label from the contract
itself — the only form where the contract cannot disagree with the launch. Lands as a register
section; the operator ratifies.

## 3 · FIVE ACTS (report §7's ranked list, mapped onto owners; four are one-liners)
1. **Reconcile the table shape — one line, win-tooling.** Teach `Get-TableField`
   (`Invoke-Dispatch.ps1:364-369`) the three-column header form (accept BOTH; no contract churn).
   Owner: a small operator-run CC session in win-tooling (operator-owned repo; edit source,
   re-run `Apply-DispatchHelpers.ps1` / the dispatch applier, deployed copy is SHA-verified).
   Done-when: `dispatch <each-of-today's-4> -DryRun` prints a launch line, 4-for-4.
2. **Fix `/lane-boot:62` — one line, hub (Lane RL scope).** Replace the raw-form instruction with
   the ruled verb (`dispatch <contract-path>`), restoring model/effort fidelity by construction.
3. **Collapse the four voices — hub (Lane RL scope).** PLAYBOOK Ch8 §2225-2278 is ALREADY the
   operator page (measured correction — see §5); make its table the ONLY literal-command site:
   `templates/prompt-template.md:113` and the two other PLAYBOOK sites become pointers to it; the
   raw form stays documented once, labeled FALLBACK.
4. **Contracts get a home a gate can see — hub ruling + tiny mechanism.** Keep the operator's
   Downloads flow untouched; make `dispatch` the gate at the point of use: on launch it (a)
   validates the contract (the same checks `gen_lane_contract check` runs), (b) copies it
   byte-identical into `prompts/<date>/` in-repo so the batch's launch inputs are committed with
   the batch. Hand-authored contracts stop being invisible without changing how the operator
   receives them. (Win-tooling half of this rides act 1's session; hub half is a wave-2 row.)
5. **Codespaces gets a verb — wave-2 build row (born under R-F1, cites this plan).**
   `Dispatch-CS <contract.md>` in DispatchHelpers wrapping the research-documented pattern:
   `gh codespace create -R <repo> --machine 2-core --idle-timeout 30m --retention-period 24h` →
   `gh codespace cp` the contract in → `gh codespace ssh -c <name> -- "claude -p ... --output-format json > receipt.json"`
   → `cp` the receipt out → `stop`. Cost guards from the research are part of the spec (stopped ≠
   deleted; 120 free core-hours/month ≈ 60h on 2-core). Done-when: one real lane runs end-to-end
   on Codespaces with a receipt, and the wall-times land as D1's evidence.

## 4 · THE DRIFT ORGAN (wave 2, small)
One check, fire-test shape: every literal command in PLAYBOOK Ch8's table must resolve via
`Get-Command` on the operator's machine at commit time (local hooks run there), and `/lane-boot`
must contain the ruled verb. A doc that names a dead or rival command goes RED. This is what makes
"four voices" structurally unrecurrable — the page cannot drift from the machine again.
Plus two one-line doc debts the report surfaced: land the 2026-08-20 `POST /v1/sessions` AMEND
that never landed (§ SUBSTRATE 3 (a)), and document the `session_` → `cse_` id trap hub-side (b).

## 5 · Corrections to SYSTEMIC-FIX-DISPATCH.md (measurement over my assumptions)
1. **Wrap, don't rename — stronger than assumed:** the functions are a versioned, tested,
   SHA-deployed module, not profile cruft. No `LaneKit` rebuild; `dispatch` + DispatchHelpers ARE
   the LaneKit the research recommends. Library-first satisfied by what exists.
2. **The operator page exists:** PLAYBOOK Ch8 §2225-2278, landed 2026-08-23. The fix is not a new
   `DISPATCH_RUNBOOK.md` — it is making Ch8 the SOLE voice and wiring HANDOFF_BOOT's step-0
   pointer at it. (SYSTEMIC-FIX's boot/bundle wiring stands; its "no page exists" premise falls.)
3. **The gates were never blind by negligence** — contracts live off-repo by operator flow design;
   act 4 relocates enforcement to the point of use instead of moralizing about location.

## 6 · Acceptance test (unchanged from SYSTEMIC-FIX, operator judges)
A person who has never seen this fleet dispatches one lane on each substrate using ONLY PLAYBOOK
Ch8's table — zero questions asked. Interim rule stays binding until then: **no seat emits a
launch command that is not a verbatim quote from the measurement report §6, PLAYBOOK Ch8, or the
operator's own message.**
