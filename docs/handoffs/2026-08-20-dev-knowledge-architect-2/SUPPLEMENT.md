# Architect strategic supplement — 2026-08-20-dev-knowledge-architect-2

Repo: .dev-knowledge · Mode: architect · Date: 2026-08-20

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the
   repo.
7. **Ratified-in-chat register** — terms, rulings, or contracts ratified in this window's
   chats that are NOT yet recorded in the repo: the verbatim term · a one-line definition ·
   its intended durable home (BACKLOG id / ADR / LESSONS / PLAYBOOK §). "None" is a valid
   answer.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

# HANDOFF SUPPLEMENT — outgoing 2026-08-17 architect window (closed 2026-08-19 night)

## 1 · Strategic intent for the next session (way-of-working level)
Shift the fleet's center of gravity from PRODUCING evidence to CONSUMING it. This window proved
production at scale (15 closures banked in one day, 5 cloud lanes = 4462 artifact lines, global
dispatch helpers); C3 then measured the systemic defect: **of 116 open rows with git activity, zero
carry a closure signature** — the fleet works but does not close. The next session's methodology goal:
make evidence → ruling → closure a routine, mechanized loop — adjudication seats as a standard form
(S-1 is the proven template), rulings transcribed same-day, the operator dashboard as the visibility
organ (leg 2 scoped by the operator's review), and the full dispatch runbook codified in-repo
([#539]/Ch8) so no future seat needs chat archaeology to execute.

## 2 · Tensions weighed, and where I landed
- **Velocity vs safety gates.** Landed: gates stay, enforcement points chosen by cost — #406 ruled
  accept-as-is (ship-gate WARN, NO new pre-commit leg); commit-tax 291→207s with the --parallel flip
  pending the §2.6 bar. Safety lives in ship/push gates, not in a tax on every commit.
- **Library-first vs bespoke governance.** Landed asymmetrically, on measurement: BUY the view layer
  (Backlog.md ADOPT-VIEW-LAYER, three conditions), KEEP governance bespoke — no library exists for the
  intake→ADR→archive gate; that is our model.
- **Broken cloud CLI vs operator's demand for terminal dispatch.** Landed: engineer the API path
  (POST /v1/sessions with receipt gate) rather than accept manual web-UI paste or a local fallback.
  The product bug is documented to the line; the workaround is itself verified machinery.
- **Lane autonomy vs index freshness.** Landed: the integrator is gate-of-record for index freshness
  on lane material; a declared single-hook bypass on lane branches is sanctioned (ruling 9).
- **Enterprise vs personal substrate.** Measured, not argued: corporate seat is EMU with no Codespaces
  entitlement (403 on all 9 repos) → substrate = personal Codespaces (stage 1 proven by lane J) +
  Hetzner CX53 (stage 2, carrier [#561]).

## 3 · Considered and rejected — do not relitigate
- CLI `claude --cloud` transports: ARG (truncates at newlines+quotes), STDIN (creates no session),
  BRIEF-ON-BRANCH (sessions have no remote). All measured dead 2026-08-19. The working paths are the
  API create (Dispatch-CloudV2) and web-UI sessions.
- GPU substrate — operator-rejected 2026-08-17, do-not-relitigate.
- Enterprise Codespaces — EMU dead end, measured (probe report).
- Backlog.md wholesale migration — its id ledger is unsafe as source of truth (archive frees ids,
  deletion is a supported verb; the #440 weakness class).
- WSJF / RICE ranking axes — rejected per C4's LEAN (3–4 recurring estimates across 183 rows for an
  ordering produced by judgment anyway); graph-centrality inert on a 3-edge population.
- Hard byte ceiling on the assembled paste (#449) — accepted-with-reason HOLD, warn-only stands.
- A pre-commit doc_rot leg (#406) — rejected on velocity grounds, explicitly chosen.
- `tkr` — unlocatable (no npm package, no repo); dropped.
- Local execution of the C-lanes — operator refused; the cloud channel was fixed instead.

## 4 · Open questions (unresolved or deliberately deferred)
- [#397] scripts/ grouping: 26 of 100 files fit no group; DEFERRED to a daytime window, dated. The
  refreshed 100-file map is in C4's artifact.
- [#529] structlog clause: wiring is merged but Done-when says "via structlog" and the lane shipped
  stdlib-logging; ruling owed (adequacy vs literal clause).
- [#530] legs (a) unconditional remote-ref delete on release, (b) `_local_holder` mapping — open.
- Intakes #35–#37: still DRAFT; ratifying them requires ruling their ADR fork (no authorization was
  taken this window — correctly).
- --parallel flip: the §2.6 five-run quiet bar was DELIVERED AS A DISPATCH BLOCK but its execution was
  never confirmed by the operator — treat all three night lanes (gemini A/B, doc-rot hygiene, §2.6
  bar) as QUEUED, not running; they are the next window's first batch.
- Gemini 3.7 Flash admission: same status — the A/B lane is queued (C1 pack + ruled ADMIT bar ready);
  the two refusal items C1-N1/C1-N2 are scored by the architect BY HAND (ruled — they encode rulings,
  not greppable facts).
- [#171] leg 2 scope: awaiting the operator's review of ecosystem/conformance.html.
- Two ruled-but-unlanded births: run_id emit row (sequenced BEFORE the read-path build lane) and the
  #488 constraint-contention tiebreak implementation.
- C3's six self-contained AWAITING-RULING rows (#549 #507 #420 #331 #541 #491) and the [#506] per-id
  verdict pass (179/183 evidence coverage) — the next window's adjudication seat.

## 5 · Decomposition rationale — and what must NOT be redone
Shape: seat-arc (frozen multi-act contract on primary) for governance mutations; file-disjoint
worktree lanes for builds; cloud lanes read-only + docs-only artifacts (the N4 rule); ONE integrator
as serial merge gate; harvest order push-before-delete. This shape held under fire — S-1 executed 8
acts with zero SKIPs while five lanes and a product-debug ran concurrently.
Do NOT redo or re-decide: the eight L-5 rulings (transcribed, closed); the nine digest rulings of
2026-08-19 night (listed in the window memory file; transcription is the next seat's FIRST act); the
cloud-channel verdicts (CLI bug + API path); the dispatch mechanics (shipped as win-tooling global
commands); batch-2 and C-harvest merges (all on origin/main at 1b8992ca).

## 6 · Off-repo context
- Dispatch-CloudV2 + Dispatch-Lane + Get/Archive-CloudSession live in WIN-TOOLING (cross-repo home),
  installed via PSModulePath — new terminals only. Endpoint/headers/environment_id verified against
  claude-code CLI 2.1.235 and may drift with CLI updates; the RE-TEST procedure is in the win-tooling
  README. An Anthropic bug-report draft (CLI silent bundle fallback) is written, NOT yet submitted.
- The operator↔architect paste channel is broken in this chat client: inline browser copy-paste
  arrives EMPTY. All session outputs must travel as uploaded .md files. The next architect must state
  this in its first message and never claim to have read an inline paste without verifying content.
- Operator interface rules ratified this window (now standing): revise the operator's output FIRST,
  then exactly ONE next step; every contract file ships with its runnable dispatch block in the same
  message; every board paste gets an answer block for every "Needs input" row, unprompted; deliverable
  value is stated in human release-notes language, not repo jargon.
- Operator state: velocity frustration is the dominant theme; the dashboard + ledger + release notes
  exist to answer it. Gemini 3.7 Flash (launched 2026-08-13) is real and awaits measured admission.
  `--effort` takes full names only (low/medium/high/xhigh/max) — short forms silently ignored.

## 7 · Ratified-in-chat register (NOT yet recorded in the repo)
1. "Integrator is gate-of-record for index freshness on lane material; declared single-hook bypass on
   lane branches is sanctioned" — home: [#539] contract template + PLAYBOOK Ch8.
2. The nine C-digest rulings of 2026-08-19 night (run_id birth-before-read-path; C6 static-HTML stack
   accepted; C1 ADMIT iff G1∧G2∧G3 with hand-scored refusal items; C2 R1=(a) profiles live in the hub
   now; R2–R6 accepted; #488 LEAN accepted; #397 deferred-dated; C3 six rows + #506 to an adjudication
   seat) — home: row bodies / STANDING_RULINGS via the next seat's act 1.
3. "Push-before-delete on every harvest" — JOURNAL entry (i) exists; PLAYBOOK Ch8 needs the rule.
4. "Primary checkout is seat-arc-only; helper tasks run zero git ops in primary" (two HEAD-swap
   incidents witnessed) — home: STANDING_RULINGS.
5. "Cloud lanes branch fresh off origin/main and never touch foreign dirty files" — home: Ch8.
6. "Every cloud dispatch carries a RECEIPT gate (sources non-empty + first assistant text echoed)" —
   home: Ch8 + the [#539] generator.
7. Backlog.md ADOPT-VIEW-LAYER ratification with three conditions (one-way export; disposable
   gitignored export dir; governance stays bespoke) — verdict is in the trial artifact as PROPOSED;
   the ratification itself needs a decision record (mini-ADR or row).
8. Gemini admission bar (item 2 above) doubles as the standing NEW-MODEL acceptance procedure — home:
   PLAYBOOK lanes section (routing-table governance).
"None" does not apply — items 1–8 above WERE the debt and are now DISCHARGED: the window-close
transcription seat (END PACKET, pushed 217c68cb..4acce74f) landed all of it in the repo. This
register stands as the historical map only.

## 10 · TRANSCRIPTION SEAT — the repo now governs what the chat ruled (origin/main 4acce74f)
- STANDING_RULINGS section Q, ten rulings Q1–Q10 (index-freshness gate-of-record; primary =
  seat-only; push-before-delete; cloud-lane hygiene; receipt gate; contract-as-file; trajectory-
  inclusive Φ; medium tier for fan-out; G1∧G2∧G3 admission with hand-scored refusals + version
  P-item; refuted-premise ⇒ PAUSE). Ratchet held at 440.
- EIGHT births, ledger lawful (15 banked > 11 window births): run_id emit · [#488] tiebreak ·
  CX53 daily-driver ([#561]-carried) · provider-config dynamic links · Backlog.md view-layer
  implementation · lifecycle-archival pass+check · grouped hygiene (suite REDs + census
  findings) · Grok guarded-rerun row. Verdict annotations landed in [#491]/[#561]/[#539] and
  the new rows [#562]–[#569].
- Anti-orphan sweep: 18 carried / 2 deferred(dated: Ch8 landing or 2026-09-19) / 0 VIOLATIONS.
- LIFECYCLE CENSUS (the operator's question, measured): ADRs 88 = 86 live + 2 archived;
  intakes 34 live, 0 archived — NO intake archive directory exists; rows today +8 born / 0
  closed (transcription arc births by design; window total remains net-closing 15 vs 11).
  The archival gap is now a carried row, not a complaint.
- Known state handed forward: 45 WARNs on main incl. doc_rot 19 (births over the 1320 ceiling
  per the [#559] scheme) — next window's hygiene inherits; [#539] gap-table pointer was ADDED
  by this seat (its absence was a real finding, not a confirmation).

## 8 · OPERATOR MANDATE for the next window (his closing list, honest status attached)
Priority 1 — THE DISPATCH SYSTEM IN THE REPO. The helpers exist (win-tooling global commands:
Dispatch-Lane local-worktree, Dispatch-CloudV2 cloud-with-origin), but every new chat still cannot run
worktrees without archaeology. [#539]/Ch8 codification (runbook + gen_lane_contract: which work goes
local vs cloud, receipt gates, harvest, all 2026-08-19 rules) is the FIRST execution lane of the next
window — not a theme, a lane.
Priority 2 — performance he can FEEL: land the --parallel flip (bar report pending), run_id birth +
telemetry read page (C6 contract ready) so prompt/hook timing is visible, devcontainer speedups.
Priority 3 — provider universalization, genuinely NOT started this window: codex folder retirement /
AGENTS.md / vendor-neutral CLAUDE.md; and the VISION→README rename, which is a REFERENCE MIGRATION
(grep census of every referencing surface, atomic migration, dead-path validator) — never a bare
rename. #82 profiles (R1 ruled: hub home now) is the first brick.
Priority 4 — visibility he asked for repeatedly: his review of ecosystem/conformance.html scopes
[#171] leg 2; the #488 tiebreak birth makes priority ranking visible; the adjudication seat runs the
full intake/ADR orphan audit (instrument is live, dashboard section 2 shows VIOLATIONS).
Measured-and-closed (do not reopen): Enterprise Codespaces (EMU, no entitlement), cloud CLI verdict,
GPU. Python-library adoption is point-wise real (mutmut, uv, Backlog.md-view) but has no program —
the next window should name one or explicitly decline one.

## 9 · FINAL-HOUR RESULTS (window truly closed at origin/main 53b904c2)
- **Everything landed and pushed**; final integrator END PACKET is the consolidation of record
  (its WHERE-TO-LOOK section lists the dashboard + five key audits by path). Teardown complete:
  1 worktree (primary), 3 local + 3 origin branches, no --no-verify/SKIP anywhere in the arc.
- **--parallel flip LIVE on main** (54633041): commit tax measured ~97 s quiet; on Codespaces the
  same gate is ~19–20 s.
- **A/B verdicts (architect, hand-scored G1): Gemini 3.7 Flash NOT ADMITTED** (G1 fail — classified
  N1 instead of declining; G2 fails under the trajectory-Φ ruling; run is evidence-only per #491's
  Antigravity exclusion) — but 11/12 mechanical parity at Φ=0 and a TEXTBOOK role-decline on N2;
  after the #491 identity ruling it earns a clean rerun (pinned tier medium, 2.9× wall noted).
  **Grok 4.6 NOT ADMITTED** (G1 fail on clean evidence; C1-R4/C1-N2 contaminated — candidate read
  the pack incl. ground truths; rerun requires a no-pack sandbox guard; $2.69 spend, 81% on the two
  contaminated items). **Systemic finding: the INCUMBENT (haiku fan-out) also classified both role
  items (0/2)** — role discipline today lives in the architect's routing, not in any model; the
  gate works, no model passes it yet.
- **Codespaces audit ON MAIN** (docs/audits/2026-08-20-technical-codespaces-audit.md) with the
  RULING block; substrate escalation recorded: the operator now requires EVERY prompt on fast
  substrate → far above the 30–37 h/mo threshold → the CX53 "daily driver" lane (same
  devcontainer, VS Code Remote, claude on the box; Codespaces as parallel burst) is the FIRST
  substrate lane of the next window under [#561]. Defender-tax measurement task in flight —
  CONFIRMED = free local recovery; POLICY-BLOCKED = one more measured CX53 argument.
- **Pending, with owners:** Ch8 codification (architect; census on main) · provider-config
  dynamic-links lane (architect; junction mechanism, dev-knowledge as truth for
  .claude/.gemini/.grok/.codex) · step-0 free ceiling test (operator, 2 min) · ssh BOM one-byte
  fix (operator; ssh currently non-functional machine-wide) · Gemini slot-1 branch: KEEP
  docs/night-ab-gemini-2026-08-20, next window's hygiene renames its files -slot1 and merges
  docs-only · two pre-existing suite REDs reported undispositioned (stale routine-rows pin;
  constant-refusal test) — next seat's triage.
