# SEAT ARC — WINDOW-CLOSE TRANSCRIPTION: THE REPO INHERITS EVERY RULING (2026-08-20)

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — frozen seat contract, NO plan-mode | high |

**PRIMARY checkout, serial acts, branch + --no-ff merge per act-group, push at the end.**
ADR-110: commit this prompt first as
`docs/audits/2026-08-20-technical-transcription-seat-contract.md`.
Operator GO covers everything below — decision budget: transcribe as ruled, ask NOTHING unless
a ruling conflicts with a repo core-invariant (then PAUSE verbatim).

## ACT 1 — STANDING_RULINGS entries (each one line, dated, sourced "architect 2026-08-19/20")
1. Integrator is gate-of-record for index freshness on lane material; a declared single-hook
   bypass on lane branches is sanctioned (declaration in commit body).
2. Primary checkout is seat-arc-only; helper tasks run zero git ops in primary.
3. Harvest order: push-before-delete, always.
4. Cloud lanes branch fresh off origin/main and never touch foreign dirty files.
5. Every cloud dispatch carries a receipt gate (git source non-empty + first assistant text).
6. Contract-as-file without exception; inline-with-dummy-filename is a forbidden dispatch form.
7. Fabrication scope for model-acceptance runs: Φ is trajectory-inclusive (a fabricated source
   in the trajectory counts even with an empty response).
8. Canonical effort tier for fan-out candidacy: medium.
9. New-model admission: ADMIT iff G1∧G2∧G3 on the seeded-defect pack; refusal items are
   architect-hand-scored; a version/substitution probe is a hard precondition (P-item).
10. A lane that discovers a refuted premise PAUSEs with the fact — deviation-with-disclosure is
    not a license.

## ACT 2 — verdict transcriptions (row bodies / new rows as fits the taxonomy)
- [#491]: annotate — the 2026-08-20 Gemini A/B (docs/audits/...-gemini-ab-results.md) is
  EVIDENCE for the identity ruling; run classed evidence-only; Gemini NOT ADMITTED this run
  (G1 fail + G2 fail under trajectory-Φ); clean rerun follows the #491 ruling, tier medium.
- Grok 4.6: NOT ADMITTED this run (G1 fail on clean evidence; C1-R4/C1-N2 contaminated —
  candidate read the pack); rerun requires a no-pack sandbox guard. New S-row for the guarded
  rerun, blocked-on: #491-class instrument rulings NOT required (direct API) — only the guard.
- Systemic finding (LESSONS entry): incumbent fan-out also classified both role items (0/2) —
  role discipline lives in architect routing, not in any model; the gate works, none pass yet.
- Codespaces: the RULING block already rides in docs/audits/2026-08-20-technical-codespaces-
  audit.md — add the row-side pointer: [#561] body gets the LEAN v2 acceptance line + the
  never-meter-buy rule + the 30–37 h thresholds + "commit-tax pain gone on CS" framing.
- Erratum note appended to the codespaces audit: the §ruff 1.6–1.7 s figure did not reproduce
  (0.33 s quiet, --no-cache ruled out); measurement-method artifact, does not affect the
  pytest/health numbers or the LEAN.

## ACT 3 — births (ledger check first: today's banked closures ≥ 15, births so far 3;
release these 4, kill-candidates named per house rule)
1. run_id in telemetry emit (S) — sequenced BEFORE the read-path build lane (ruled).
2. [#488] constraint-contention tiebreak implementation (S/M) — per the accepted LEAN.
3. CX53 daily-driver substrate lane (M) — carrier under [#561]: same devcontainer, VS Code
   Remote, claude on the box; goal = the operator's every-prompt requirement; Codespaces
   free 4-core stays the parallel-burst substrate (30 h/mo watched).
4. Provider-config-as-code + dynamic links (M) — dev-knowledge as source of truth for
   .claude/.gemini/.grok/.codex, machine-global dirs as junctions (the existing .claude link
   pattern generalized); routing table reads from one model registry.

## ACT 4 — pointers, not duplicates
[#539] body: note the Ch8 gap-map is on main (playbook-status audit path) and the dispatch
runbook (Dispatch-Lane + Dispatch-CloudV2 + receipt + harvest) currently lives in win-tooling —
Ch8 lane writes it into PLAYBOOK. Suite's 2 pre-existing REDs: file ONE grouped hygiene row
(stale routine-rows pin; constant-refusal test) — counts within the birth release above if the
ledger demands (then it is birth 5 of 5; closures cover it).

## FINAL
gen_task_tree --emit-source · validate_backlog · JOURNAL entry anchoring the arc · full gates,
no SKIP · push. END PACKET: per-act shas, ledger line (closures/births/live), the exact
STANDING_RULINGS lines added, and one sentence: "the repo now governs what the chat ruled."
NOT: no security-related items anywhere in the repo · no Ch8 writing (its lane owns that) · no
admission reversals · no supplement edits (architect owns that file).

---

## BINDING ADDENDUM (operator, at dispatch — landed with the prompt as issued, per ADR-110)

- **STEP 0.** Another session is finishing a docs rename arc on primary — poll `git status` every
  60 s (up to 30 min) and START only when the tree is clean and `main == origin/main`; never touch
  foreign staged files.
- **ACT 2.5 (between acts 2 and 3).**
  (a) BIRTH the `Backlog.md` view-layer implementation row (M) per the ratified 2026-08-19 verdict
      (one-way export, disposable gitignored export dir, governance stays bespoke; source =
      `docs/audits/2026-08-19-technical-backlogmd-trial.md`).
  (b) BIRTH one lifecycle-archival row (S/M): a pass archiving implemented ADRs and decided intakes
      per existing conventions PLUS a check so archival can never silently lag (operator's measured
      complaint: 2 ADRs archived, ~8 intakes).
  (c) ANTI-ORPHAN SWEEP over every ratification transcribed: each ends this arc with a carrier row
      or an explicit `deferred(dated)` — violations are listed in the END PACKET.
- **ACT 2.6.** CONSUME `docs/audits/2026-08-20-technical-playbook-status.md`: verify `[#539]`'s body
  points at its gap table and Ch8 brief; fold its hygiene-census findings into the grouped hygiene
  row from ACT 4.
- **(d) END PACKET carries the LIFECYCLE CENSUS:** ADRs total/implemented/archived, intakes by
  status, rows opened vs closed today with the net.
- Operator GO covers all acts; PAUSE verbatim only on core-invariant conflict.
