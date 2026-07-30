# P10 grooming dossier — every open BACKLOG row classified (night batch 2026-07-31)

**Status: PROPOSED — input dossier. Every verdict below is a PROPOSAL for the morning architect to ratify or reject. Nothing here is a disposition, and no row was edited.**

**Scope:** all open `#id` rows in `BACKLOG.md` at `65a549b` (branch `claude/night-2026-07-31-morning-prep-yo7pgw`, cut off `main`). Read-only. `BACKLOG.md`, `tasks/`, `docs/decisions/` and every generator were left untouched.

## 0. Live count — the brief's 177 is stale; the live number is 181

Three independent sources agree, so the count is not an artifact of one parser:

- `BACKLOG.md` rendered rows matching `^- \[#\d+\] \[P\d\]\[SML\]` — **181**
- `tasks/manifest.json` `nodes[]` entries carrying a `task` key — **181**
- set difference between the two — **empty in both directions** (no manifest-only id, no BACKLOG-only id)

`tasks/` holds 189 `*.md` files. The 8-file gap is not drift: 7 are `status: closed` task bodies retained as id-allocation records (`#386 #421 #435 #437 #439 #444 #446`) and correctly excluded from the manifest, plus `README.md`. **The ADR-107 engine is coherent** — a closed task drops out of the manifest and therefore out of the rendered file. No already-shipped row is being rendered as open. That was the first thing checked and it came back clean.

Frontmatter status across the 181 open rows: **151 `open`, 30 `deferred`**.

## 1. Headline — proposed grooming closes

Four rows are proposed DEAD. Each was verified individually against the live tree, not inferred from a keyword scan.

### PROPOSED CLOSE — [#35] P3/S · [E5]
- **Row:** Fix the self-owned low-severity cleanups (ARCHITECTURE diagram attribution + SBAR label; VISION adoption-signal + stale last_reviewed) · Done when: WF…
- **Evidence:** ARCHITECTURE Mermaid diagram removed (ADR-51 amendment 2026-07-05 — zero `mermaid` fences in ARCHITECTURE.md); zero `sbar` hits in ARCHITECTURE.md; commit `e6f9bd73` states it outright — *"[#35] GO-2 (VISION stale last_reviewed) resolved here; [#35] stays open for WF-3 + GO-1"* — so that leg was discharged long ago and is now owned by a **mechanism rather than a row** — the `canonical_freshness` organ, which is live and covers `VISION.md` (it reads clean on full history: true last edit `30a8c42b` 2026-07-25 == `last_reviewed`). 3 of 4 named referents no longer exist as backlog-owned defects.
- **Verdict:** PROPOSED DEAD. Architect ratifies.

### PROPOSED CLOSE — [#41] P3/S · [E5]
- **Row:** Split ARCHITECTURE §Processes into PROCESS.md if it grows past the comfort threshold · Done when: re-evaluated at the next process addition · refs ADR…
- **Evidence:** Split target gone — ARCHITECTURE.md carries no `Processes` heading at all (`grep '^#\+.*Process'` = zero); the six-chapter map replaced it in the ADR-51 restructure. The DEFER peg 'next process addition' can never evaluate against a section that does not exist.
- **Verdict:** PROPOSED DEAD. Architect ratifies.

### PROPOSED CLOSE — [#367] P2/S · [E8]
- **Row:** **HANDOFF_PROCESS held at `Version: 5.7` while gaining an additive normative rule** — codex HIGH 2026-07-19. The residual-completeness rule landed as …
- **Evidence:** Satisfied by supersession at a higher version. `protocols/HANDOFF_PROCESS.md:4` = `Version: 6.0.1`; all six dependents carry `reconciled_with: handoff-process@6.0.1` (ARCHITECTURE.md:3, CLAUDE.md:3, CONTRIBUTING.md:3, docs/handoffs/README.md:3, protocols/HANDOFF_BOOT.md:2, protocols/README.md:2). Zero `@5.7` edges remain. Done-when asked for 5.7→5.8 + every dependent reconciled; [#446] delivered 5.7→6.0→6.0.1 with the sweep (merge `7f8a047`).
- **Verdict:** PROPOSED DEAD. Architect ratifies.

### PROPOSED CLOSE — [#370] P3/S · [E8]
- **Row:** **Is the `owner=hub` / `owner=repo` ownership model two-state-complete?** — **RULED 2026-07-28 (operator word, architect session): NO — a third owners…
- **Evidence:** The question the row asks was RULED and the ruling is recorded in the row itself: 'RULED 2026-07-28 (operator word, architect session): NO — a third ownership state EXISTS, named owner=user' (commit `93f92ab` 'record the 2026-07-28 rulings — owner=user, launch-shape, command-cache staleness'). The row also states its own symptom is 'superseded; git holds it'. Residual Done-when is self-referential — 'the work the ruling now calls for is ruled into this row or into a follow-on' — i.e. it names no deliverable.
- **Prior closure history — the architect must see this:** the closure organ proposed #370 as a STRONG candidate at least twice and it was **REFUSED both times** (`4911f009`, `d66aef63`, 2026-07-28). Read the refusal reasons before reading the refusals as a verdict on the merits: both say the evidence was a **false positive** — *"the detector matched the sentence quoting the defect it describes"*, i.e. the pre-[#437] quoting defect matching a quoted `closes [#N]` inside a commit body. What was refused was the **organ's evidence**, not the substance of closing the row. This proposal rests on independent grounds (the row records its own ruling), so the refusals do not bind it — but a third proposal on this row deserves the explicit note that two prior ones were rejected. This is also the third distinct defect found in one detector: quoting ([#437], fixed), negation (W5, live), and these two false positives.
- **Verdict:** PROPOSED DEAD. Architect ratifies.

**Honest limit on [#35]:** three of its four named defects are verifiably gone. The fourth — "VISION adoption-signal" — could not be resolved to a specific claim in `VISION.md` (the file discusses adoption at `VISION.md:54-56`, but nothing identifies which signal the original coherence-audit flagged). If the architect wants that leg carried, close #35 and re-file the single surviving defect rather than keeping a four-part row alive for one unlocatable quarter of it.

**Cross-wave collision on [#367] — worth the architect's attention.** W5 of this same batch found that `propose_closures.closure_ids` parses negation blind, and its live end-to-end reproduction is *this exact row*: commit `6489391` says "Does NOT close [#367]" and `find_strong` returns a STRONG-tier proposal to close #367 from it. So the closure organ and this dossier both point at #367 — **for opposite reasons**. W1 proposes closing it because the spec advanced to 6.0.1 and all six edges were swept (verified above); the organ proposes closing it because it cannot read the word "NOT". If the architect ratifies the close, do it on the §1 evidence, not on the organ's proposal — and note that the organ being accidentally right here is exactly what makes the defect hard to notice in review.

**Deliberately NOT proposed dead.** Five rows looked like closes on a keyword pass and are not. They need a *text correction*, which is a different act:
- **[#181]** — DEFER peg is structurally unsatisfiable in a fresh clone: peg is 'coherence-nudge.log has enough entries to adjudicate', but `logs/` holds only TOKEN-LOG.md — every other logs/ artifact is gitignored and therefore per-working-tree (the same mechanism [#418] documents for logs/FLEET-HEALTH.md). Row also cites the pre-[#395] lowercase path `logs/coherence-nudge.log`; live name is `logs/COHERENCE-NUDGE.log`.
- **[#210]** — Live, but its proposed exemption shape is scoped to 'JOURNAL.md + docs/.../transcripts/' and the transcripts zone was deleted 2026-07-22. The exempt class narrows to JOURNAL.md alone; the row's shape needs correcting before it is built.
- **[#361]** — Premise is now UNDERSTATED, not satisfied — proposed SCOPE CORRECTION, not a close. `scripts/hooks/block_immutable_edits.py:83` scopes `_ZONE_SEGMENT = "/docs/decisions/transcripts/"`, and that directory was DELETED 2026-07-22 (`b4435fad`; CLAUDE.md §4 'do not recreate it'). The guard is armed over a zone that cannot exist, so the live count is four of four classes ungated, not three of four.
- **[#396]** — Row text has drifted (says 'in 3 places'); live count is 4 non-cache sites — scripts/fleet_parity.py, scripts/gen_handoff.py, scripts/fleet_analytics.py, scripts/audit.py. Task is LIVE (gitenv.py still absent); the number in the row needs a trim, not a close.

## 2. The finding that outranks the closes — the ruling backlog is mis-addressed

**33 of 181 rows (18%) have a Done-when that cannot be satisfied by building anything.** Their completion condition is a *ruling*: "an operator ruling picks…", "the shape is decided…", "is ruled kept-or-dissolved…". These rows are not blocked on effort. They are blocked on someone deciding.

ADR-108 (Accepted 2026-07-31) §A now routes that authority, and applying it to this cohort produces an uncomfortable result:

- **§A item 1** — the operator rules FUNCTIONAL questions only: what the system should do, how output should look, priorities between outcomes. Plain language, no technical vocabulary.
- **§A item 2** — the architect rules TECHNICAL questions *in its own lane*, records the call, and relies on revertability instead of escalation. "Uncertainty is not a reason to ask the operator; it is a reason to decide, record, and mark revertable."
- **§A item 4** — retires the anti-pattern of "presenting the operator with option menus of technical forks (R1/R2-style)".

Against that rule, roughly **three or four** of the 33 are genuinely operator-owned, and they are owned for a *reason other than being functional*:

- **[#122]** (retire the PATH shim) and **[#189]/[#346]** (`~/.claude` edits) — operator-owned by **deletion authority** and by **core-invariant #6** (global-infra is a class the hub may neither hold nor edit), not because the questions are functional.
- **[#322]** (fleet dashboard) — genuinely split: *what the dashboard should tell the operator* is functional; *which rendering layer* is technical and is the architect's call under §A item 2.

**The rest are technical, and three of them explicitly demand an operator ruling for a technical fork — the exact shape §A item 4 retires:**

- **[#406]** — "an operator ruling picks the enforcement point" between (a) a pre-commit nudge, (b) a pre-commit doc_rot leg, (c) accept-as-is. That is a three-option technical menu.
- **[#407]** — "an operator ruling records the functional-vs-OOP stance". Programming paradigm is not a functional question by any reading of §A item 1.
- **[#414]** — "an operator ruling picks the organ(s)".

**PROPOSED (architect ratifies):** these three rows' Done-when clauses were written before ADR-108 and now contradict it. Either the Done-when moves to the architect lane, or ADR-108 §A needs an exception class it does not currently have. This is a *doctrine-vs-backlog coherence defect*, and it is worth more than the four closes above — it unblocks a cohort, not a row.

**Second-order note:** ADR-108's own Consequences section already concedes "Nothing in this repo mechanically detects an option-menu brief". This cohort is the standing evidence for that gap, and it is measurable: the 33 rows are enumerable by parsing Done-when clauses, which is what produced this section.

## 3. Structural findings surfaced by the sweep

**(a) Two rows cite intake documents that have never existed.** Not moved, not archived — `git log --all` returns nothing for either path:
- **[#303]** cites `docs/intake/2026-07-10-runbook-gap-notes.md` — absent from `docs/intake/`, from `docs/intake/archive/`, and from all of git history.
- **[#344]** cites `docs/intake/2026-07-17-hub-feedback-session-close-gate.md` — absent from `docs/intake/`, from `docs/intake/archive/`, and from all of git history.

This is the [#359] "phantom enforcement" class applied to citations rather than mechanisms: a row's evidence anchor reads as verifiable and is not. Both underlying asks may be entirely real — the *citation* is what is false. PROPOSED: re-anchor both rows to a real artifact or mark the provenance as recalled-not-recorded.

**(b) The `logs/` evidence class cannot support a DEFER peg.** `logs/` holds exactly one tracked file, `TOKEN-LOG.md`. Every other artifact the backlog treats as accumulating evidence — `COHERENCE-NUDGE.log`, `FLEET-HEALTH.md`, `PROPOSALS-*.md`, `BOUNDARY-DRIFT.md`, `OPERATOR-LOAD.csv` — is gitignored and therefore **per-working-tree**. [#418] documents this mechanism for `FLEET-HEALTH.md` and correctly calls it the cause of its 0–10-baselines-a-day defect. The same mechanism silently disarms **[#181]**, whose peg is "the nudge log has enough entries to adjudicate": in a fresh clone the log starts empty, so the peg can never fire. PROPOSED: any DEFER peg naming a gitignored artifact is structurally unsatisfiable and should be re-pegged or the artifact promoted to tracked.

**(c) The transcripts deletion left three rows pointing at a deleted zone.** `docs/decisions/transcripts/` was deleted 2026-07-22 (`b4435fad`). [#361] and [#210] both scope their proposed mechanisms to it (details in §1), and `scripts/hooks/block_immutable_edits.py:83` still guards it exclusively. The ADR-77 guard listed as fail-closed in `CLAUDE.md` §9 is armed over a path that cannot exist — it is a **live no-op**. PROPOSED: this is worth its own row if the architect agrees it is not already inside [#361]'s scope.

## 4. Per-theme classification — all 181 rows

Verdict vocabulary: **DEAD** = proposed close, evidence in §1 · **AWAITING-RULING** = Done-when is satisfiable only by a decision · **LIVE (deferred/pegged)** = `status: deferred` in `tasks/` frontmatter, carries a DEFER peg · **LIVE** = buildable now.

Ruling-owner column applies ADR-108 §A: `arch` = architect-technical, `op` = operator-functional, `op(auth)` = operator-owned by deletion/global-infra authority rather than by being functional, `CONFLICT` = the row assigns the ruling to the operator but the question is technical.

### [E1] Handoff continuity — 11 rows
- `#162` P2/M — **AWAITING-RULING** · owner: arch — Vocab decision (architect-session): disambiguate "architect" as the Layer-1 actor (ARCHITECTURE.md / ADR-
- `#293` P3/S — **LIVE (deferred/pegged)** — Consumer runbook fan-out
- `#298` P3/S — **LIVE (deferred/pegged)** — Handoff-generator polish
- `#301` P2/M — **LIVE (deferred/pegged)** — Session-plan artifact class
- `#344` P2/M — **AWAITING-RULING** · owner: arch — Session-close gate for handoff generation + consumer hub-write guard (NEEDS-RULING; ai-council role-gov f
- `#350` P3/S — **LIVE** — Handoff-process refinements (operator priority-program item 5
- `#390` P2/S — **LIVE** — Resolve the ADR-87 effort-ownership contradiction, then true up the prompt template
- `#404` P2/S — **LIVE** — gen_handoff execution-mode SUPPLEMENT leak (mode-blind framing + P8 row)
- `#422` P2/S — **LIVE** — `reflow_framing`'s cold→FILLED flip is partial by design, and nothing detects the self-contradiction it l
- `#447` P3/S — **LIVE** — Self-referential gate family
- `#449` P3/S — **AWAITING-RULING** · owner: arch — Assembled-paste byte budget

### [E2] Enforced governance — 57 rows
- `#99` P3/S — **LIVE** — FLEET-HEALTH digest names the failing check per red repo
- `#112` P2/M — **LIVE** — adr_amend helper + ADR immutable-zone extension
- `#116` P3/S — **LIVE** — Hooks hygiene
- `#117` P3/S — **LIVE (deferred/pegged)** — Evaluate prompt/agent-based hooks (`type:"prompt"` Haiku-eval / `type:"agent"` multi-turn, experimental)
- `#132` P2/M — **LIVE** — Organ-index generator
- `#139` P2/L — **LIVE (deferred/pegged)** — merged-arc→record verifier (a.k.a. #90b
- `#146` P3/S — **LIVE** — De-hardcode-first doctrine + sweep
- `#153` P2/M — **AWAITING-RULING** · owner: arch — Enforcement-completeness pass
- `#166` P3/M — **LIVE (deferred/pegged)** — doctrine_enforcement_coherence check
- `#169` P3/M — **LIVE (deferred/pegged)** — Ungated-doc staleness detection (ADR-85 R2)
- `#170` P3/M — **LIVE** — Design + land the traceability-spine ADR (issue-ID↔commit anchor) that #168 depends on
- `#171` P3/M — **LIVE (deferred/pegged)** — Build the conformance dashboard at `ecosystem/conformance.md` (ADR-86 / ADR-85 R2)
- `#181` P2/S — **AWAITING-RULING** · owner: arch — Coherence v2 nudge-response
- `#185` P2/M — **LIVE** — GAP-2 deterministic gotcha-injection guard
- `#188` P3/M — **LIVE (deferred/pegged)** — Deny-rule + hook completeness audit
- `#189` P3/S — **LIVE** — Execute in ~/.claude (runtime-config repo; queue-only here, per the #100 execute-elsewhere precedent)
- `#190` P3/M — **LIVE (deferred/pegged)** — General intra-file duplication detector
- `#210` P3/S — **AWAITING-RULING** · owner: arch — Convert journal-wrap no-ff WARNs from per-instance disposition to a standing rule
- `#218` P3/M — **LIVE (deferred/pegged)** — Safe-removal gate M2+M3 boundary (the deferred phases of #195)
- `#220` P2/M — **LIVE** — MODIFY / semantic-drift axis
- `#234` P3/S — **LIVE** — Cross-repo probe validator
- `#239` P3/M — **LIVE (deferred/pegged)** — Follow-up
- `#240` P3/S — **LIVE (deferred/pegged)** — Follow-up
- `#241` P2/S — **LIVE** — Undeclared-edge groom
- `#242` P2/M — **LIVE** — ADR status-flip coherence check
- `#267` P2/S — **LIVE** — Scope-exercising arc extension (REFINEMENT, root-ratified 2026-07-06
- `#277` P2/M — **LIVE** — propose_closures signal repair
- `#289` P2/M — **LIVE** — Hub-own the OneDrive-Blue-Yonder guard (`block-onedrive.ps1`)
- `#294` P3/M — **LIVE (deferred/pegged)** — `validate_backlog` deploy-carrier + `--path` de-hardcode (ai-council pilot G1+G2)
- `#296` P3/S — **LIVE** — `audit.py repo <name> --repo-path` doesn't persist its report (ai-council pilot G6)
- `#297` P3/S — **LIVE (deferred/pegged)** — Lightweight/dry `observe-arc` coverage mode (ai-council pilot G7)
- `#303` P2/S — **LIVE** — Make seed_runbook.py child-class-aware (ADR-36 no-local-handoffs)
- `#305` P3/S — **LIVE (deferred/pegged)** — Add a verify-only / already-onboarded re-run mode to the onboarding runbook
- `#308` P3/S — **AWAITING-RULING** · owner: arch — Decide the `verify` skill's canonical home (#9 self-flagged open question), pegged to P6
- `#310` P3/S — **LIVE (deferred/pegged)** — Define the cold-bundle annotation surface + annotate the 2026-07-05 architect bundle as-cold
- `#323` P3/S — **AWAITING-RULING** · owner: arch — Design question: add `codemap-generate`/`toc-generate` to the carried `hub_hooks` install list?
- `#324` P3/M — **LIVE** — Phase-6 axis-2 carrier
- `#325` P3/S — **LIVE (deferred/pegged)** — Carry `/save` to consumers via a manifest command-artifact carrier
- `#335` P3/S — **LIVE** — Exempt `templates/` from the `reconciled_versions` check
- `#345` P2/M — **LIVE** — Externalize the ADR-101 frozensets → machine-readable path-pattern registry + generalize `validate_hermet
- `#346` P2/S — **AWAITING-RULING** · owner: op(auth) — Persist the two-tier new-path executor rule into `~/.claude` (durability)
- `#349` P2/M — **LIVE** — Mechanize session-discipline inheritance
- `#353` P2/M — **LIVE** — Session-boot contract hardening
- `#389` P2/S — **AWAITING-RULING** · owner: arch — Prompt-lint
- `#401` P2/S — **AWAITING-RULING** · owner: arch — ai-council routing still ARMED at the deleted hub landing zone
- `#405` P2/S — **LIVE** — Session-end leftover check
- `#406` P3/S — **AWAITING-RULING** · owner: **CONFLICT** (row says operator; question is technical — see §2) — Commit-time doc_rot surfacing
- `#408` P2/M — **LIVE** — Auto-coupled doc updates
- `#414` P2/S — **AWAITING-RULING** · owner: **CONFLICT** (row says operator; question is technical — see §2) — Self-acting-on-main incident family
- `#417` P3/S — **LIVE** — `check_dirty_tree` runs with no pathspec, so the Stop gate fires every session on non-work
- `#418` P2/S — **LIVE** — `automation/fleet-audit` records 0–10 baselines a day, not one
- `#423` P2/M — **LIVE** — The integration sequence runs on prose every time, never mechanized
- `#424` P2/S — **LIVE** — Backlog `depends-on` gates are INERT
- `#425` P2/S — **LIVE** — The suite is green on a format the file does not use
- `#442` P2/M — **LIVE** — Plugin command-cache staleness
- `#451` P2/M — **LIVE** — CA layer-edge check
- `#452` P3/S — **LIVE** — `[#433]`→`[#382]` pilot-precedes-contract dependency is prose-only

### [E3] Lessons feedback loop — 8 rows
- `#4` P2/M — **LIVE (deferred/pegged)** — Build lessons-index.json + SessionStart retrieval + CLI query
- `#130` P3/S — **LIVE** — Memory-hygiene review
- `#144` P3/M — **LIVE (deferred/pegged)** — Feature DoD = end-to-end / user-flow test
- `#145` P3/M — **LIVE (deferred/pegged)** — Codification-completeness pass
- `#266` P3/S — **LIVE** — Codify the test-scoped-grant language lesson (E4-1 precedent)
- `#438` P3/S — **LIVE** — Codify gate-class posture: terra design review BEFORE build for refusal-gate arcs
- `#441` P2/S — **AWAITING-RULING** · owner: arch — Way-of-working: the DEFAULT is one strong self-contained prompt on primary; worktrees are the exception b
- `#443` P3/S — **LIVE** — Planning artifacts outside the three enforced classes carry no rent rule

### [E4] Decision management — 3 rows
- `#19` P3/M — **AWAITING-RULING** · owner: arch — Complete the ADR-39 register
- `#23` P3/S — **LIVE** — Validate ADR frontmatter relation-fields (supersedes/related/amends resolvable)
- `#450` P3/S — **AWAITING-RULING** · owner: arch — Per-section intake ratification

### [E5] Canonical-file integrity — 11 rows
- `#35` P3/S — **DEAD (proposed close)** — Fix the self-owned low-severity cleanups (ARCHITECTURE diagram attribution + SBAR label; VISION adoption-
- `#41` P3/S — **DEAD (proposed close)** — Split ARCHITECTURE §Processes into PROCESS.md if it grows past the comfort threshold
- `#71` P3/S — **LIVE** — Reconcile ENVIRONMENT.md's `~/.claude/` directory tree with live contents (commands = codex-review + sess
- `#213` P2/L — **LIVE** — PLAYBOOK rule/history condensation
- `#227` P3/S — **LIVE** — Relocate AGENT_FRAMEWORK.md out of protocols/
- `#263` P3/S — **LIVE** — Protocols/edge-map reconciliation residuals (ADR-51 amendment)
- `#269` P3/S — **LIVE** — Audit-index count-tiered shape + freshness hook (ADR-100 Q2)
- `#285` P3/S — **LIVE** — Extend hub freshness gating to PLAYBOOK
- `#300` P1/M — **AWAITING-RULING** · owner: arch — Hermetization residual d.ii
- `#388` P3/S — **LIVE** — The "10–20 repo" fleet-scale target is FABRICATED
- `#420` P3/S — **AWAITING-RULING** · owner: arch — Does a TOP-LEVEL `docs/archive/` still make sense?

### [E6] Cross-repo universalization — 27 rows
- `#43` P3/L — **LIVE** — Decide + (if yes) author a one-step new-repo scaffold (ADR + templates/new-repo-skeleton/, no scripts) · 
- `#82` P3/M — **LIVE (deferred/pegged)** — Define per-repository agentic-review profiles
- `#215` P2/M — **LIVE** — Onboard + verify methodology in a new repo
- `#231` P3/M — **LIVE (deferred/pegged)** — Consumer → hub feedback report
- `#244` P2/L — **LIVE** — Essence-spec lifecycle epic
- `#245` P2/M — **LIVE** — Add-path status-awareness
- `#276` P2/M — **LIVE** — D2 per-consumer waiver-honoring
- `#280` P3/S — **LIVE** — Propagate the intake area to greenfield consumers via the deploy manifest
- `#281` P2/S — **LIVE** — Re-peg the ai-council ADR-66 story-map convergence (ADR-99 clause A)
- `#282` P3/S — **LIVE** — Fleet `.gitattributes` EOL-normalization parity
- `#283` P3/S — **LIVE** — corp-monorepo `hybrid_classifier.json` 1.08MB duplication
- `#290` P3/S — **LIVE** — Floor-carrier verify-teeth + self-heal (residual of #275b)
- `#315` P3/S — **LIVE** — `INSTALL.md` uniform fleet-wide, hub-owned, deploy-carried (operator ruling; fleet-boundary-matrix Surfac
- `#320` P2/S — **LIVE** — Fleet backup posture
- `#327` P2/M — **LIVE** — Protocols-as-interface genre ruling (fleet-parity register acceptance)
- `#329` P3/S — **LIVE** — VS Code ownership visualization
- `#331` P2/S — **AWAITING-RULING** · owner: arch — Consumer BACKLOG schema adoption ruling
- `#332` P2/M — **LIVE** — Fleet dependency-version parity
- `#334` P3/S — **LIVE** — Fleet-wide ruff hook id migration `ruff` → `ruff-check` (upstream `ruff-pre-commit` deprecation; flagged 
- `#342` P3/S — **LIVE** — fleet_parity gate-ahead max-fidelity hardening (deferred from #336/ADR-102, operator-ruled)
- `#343` P3/S — **LIVE** — fleet_parity ship-gate-only scoping (RIDER 2 perf follow-up, operator-ruled 2026-07-18)
- `#351` P3/M — **LIVE** — Fleet-Python-upgrade ticket ("always newest Python"
- `#352` P3/S — **AWAITING-RULING** · owner: arch — Versioned `.vscode` region decoration (RULING-S human-facing half)
- `#407` P3/M — **AWAITING-RULING** · owner: **CONFLICT** (row says operator; question is technical — see §2) — Universal fleet Python style
- `#416` P3/S — **LIVE** — ai-council `ARCHITECTURE.md` codemap drift at L23/L109
- `#429` P2/M — **LIVE** — Worktree provisioning is not portable across the fleet
- `#430` P2/M — **AWAITING-RULING** · owner: arch — Consumer template rejects root `conftest.py`; `fleet_parity`'s verdict depends on state outside its subje

### [E7] Tooling & evaluation — 35 rows
- `#102` P2/M — **LIVE (deferred/pegged)** — Machine-readable repo index for agent consumption
- `#122` P3/S — **AWAITING-RULING** · owner: op(auth) — Retire the PATH shim (`claude.cmd`)
- `#123` P2/S — **LIVE** — Routine observability convention + value review
- `#126` P2/M — **LIVE** — Backpressure-loop pattern evaluation
- `#127` P3/S — **LIVE** — verify skill failure-output contract
- `#270` P1/M — **LIVE** — Operator-load gauge
- `#271` P3/L — **LIVE** — Nightly proposal loop
- `#273` P3/S — **LIVE** — Changelog-review staleness escalation (intake doc #2 R3)
- `#274` P3/S — **LIVE** — Dogfood-signal prior in the /changelog-review ADOPT rubric (intake doc #2 R4)
- `#278` P2/M — **LIVE** — Test-suite hygiene epic (consumes intake-id 3)
- `#288` P3/S — **LIVE** — Model-identity guard for unattended runs
- `#317` P2/M — **LIVE** — Default-parallel test invocation + slow-tier markers
- `#322` P2/M — **AWAITING-RULING** · owner: op (split: what=op, how=arch) — Fleet dashboard
- `#338` P2/S — **LIVE** — codex-review drift consolidation (successor to closed #333)
- `#340` P2/S — **LIVE** — /ship pre-flight validator honors the consumer repo's canonical test gate
- `#341` P2/S — **LIVE** — Codex producer-lane activation mechanism (R2+R3; EPIC-H producer axis, ai-council 2026-07-17 role-gov fee
- `#347` P2/M — **AWAITING-RULING** · owner: arch — Formalize the engineering loop/harness end-to-end + sanctioned safe-deletion pattern (operator priority-p
- `#348` P3/S — **LIVE** — Backlog grooming as a standing routine, not ad-hoc (operator priority-program item 3, half (b))
- `#387` P2/S — **LIVE** — Rewrite the buy-vs-build intake BEFORE anything ingests it
- `#396` P3/S — **LIVE** — Extract `scripts/gitenv.py`
- `#397` P3/M — **LIVE** — scripts/ target structure
- `#403` P3/S — **LIVE** — Extend `doc_claims` to ARCHITECTURE's machine-derivable claims
- `#409` P3/S — **LIVE** — Standing night batch
- `#410` P3/S — **LIVE** — Standing night batch
- `#411` P3/S — **LIVE** — Standing night batch
- `#412` P3/M — **LIVE** — Subagent / workflow routing + configured fan-out + online research into Anthropic's published commands/sk
- `#415` P2/S — **LIVE** — Tests must bind fixtures, not live mutable repo content (heuristic-behaviour tests)
- `#419` P2/M — **LIVE** — We run routines whose output nobody consumes
- `#426` P2/M — **LIVE** — Declare `consumer` + `consumption_path` for every LIVE routine
- `#428` P2/S — **LIVE** — `nightly-triage` reports a dead producer to every session start
- `#431` P2/S — **LIVE** — `codex-review` silently drops the doc lane on any mixed diff
- `#432` P1/M — **LIVE** — Adopt `uv` as the environment/dependency toolchain
- `#433` P1/M — **LIVE** — BACKLOG restructure
- `#440` P2/S — **LIVE** — Make the `tasks/` id ledger tamper-evident
- `#445` P2/S — **LIVE** — `codex-review` wrapper path-guard reports SUCCESS having reviewed nothing

### [E8] ARC-5 execution — 22 rows
- `#354` P2/M — **LIVE** — W6 seed-1 recurrence half
- `#356` P2/M — **AWAITING-RULING** · owner: arch — RULING-W and the merge-delegation composite are LEGIBLE but have neither a mechanism nor a declaration
- `#357` P2/M — **LIVE** — Silent-rule census run 2
- `#358` P2/S — **LIVE** — `ecosystem/parity-surfaces.yaml` misdescribes its own enforcement posture at HEAD
- `#359` P1/M — **LIVE** — PHANTOM ENFORCEMENT
- `#360` P3/S — **LIVE** — `protocols/DEFINITION_OF_DONE.md:106-109` expired in place
- `#361` P3/S — **LIVE** — ADR-immutability's real coverage is declared only in code, never in the protocol
- `#362` P2/M — **LIVE** — #242 carries a SUBSTANTIVE guard loss, not status hygiene (bound to [#242])
- `#363` P2/S — **LIVE** — `codex-review` routed a CODE-shaped diff through the `gpt-5.6-sol` lane, not terra
- `#364` P3/S — **LIVE** — `doc_rot`'s length cap blocks [#353] from doing its job
- `#365` P3/S — **LIVE** — Promote `residual_completeness` from `exempt:` to `coverage_scope`
- `#366` P2/S — **LIVE** — `residual_completeness` scans the WORKING TREE, not the staged blob
- `#367` P2/S — **DEAD (proposed close)** — HANDOFF_PROCESS held at `Version: 5.7` while gaining an additive normative rule
- `#369` P3/S — **LIVE** — Wire `boundary_headers.py --check` into pre-commit
- `#370` P3/S — **DEAD (proposed close)** — Is the `owner=hub` / `owner=repo` ownership model two-state-complete?
- `#371` P2/S — **LIVE** — Consumer editor-config write-through
- `#399` P2/S — **LIVE** — `templates/handoff/v5/README.md.tmpl`
- `#400` P3/S — **AWAITING-RULING** · owner: arch — Ownership-model: the hub-mandated-STRUCTURE / repo-owned-CONTENT cell (rosters)
- `#402` P3/S — **LIVE** — Intake naming clause
- `#413` P2/S — **LIVE** — Colors semantics
- `#427` P3/S — **LIVE** — Region templates carry a repo-POSITION-DEPENDENT path (ai-council, 2026-07-26): `templates/claude-regions
- `#448` P2/S — **LIVE** — A11 staged-diff guard

### [E9] Fleet Desired-State System (North Star) — 7 rows
- `#382` P1/M — **LIVE** — Desired-state data model: intake → ADR
- `#383` P2/L — **LIVE** — Execution waves per surface
- `#385` P3/M — **AWAITING-RULING** · owner: arch — L4 tech-currency lane
- `#391` P3/S — **LIVE** — Wire fleet_analytics into a nightly lane, or narrow #384 to a manual reporter
- `#392` P3/S — **LIVE** — fleet_analytics rename-alias loses history on path-reuse
- `#393` P3/S — **LIVE** — corp-sca rot review
- `#394` P3/S — **LIVE** — Analytics coverage gap

## 5. Verdict totals (PROPOSED)

- LIVE: **125**
- AWAITING-RULING: **28**
- LIVE (deferred/pegged): **24**
- DEAD (proposed close): **4**
- TOTAL: **181**

## 6. Method + honest limits

**Method.** Four evidence sources, cross-checked:
1. `BACKLOG.md` parsed to structured rows (id, priority, size, theme, story, body, Done-when clause).
2. `tasks/*.md` frontmatter `status:` + `tasks/manifest.json` node set — the ADR-107 source of truth.
3. `git log --first-parent` over the last 200 merges, plus a full-log scan for closure-shaped language (`clos*/resolv*/fix*/land*/ship*` within 40 chars of a `[#id]`) to catch shipped-but-open rows.
4. Existence checks on every in-repo path cited by a row, plus targeted verification of each candidate's premise against the live file.

**Limit 1 — the DEAD list is deliberately small, and that is a finding, not a shortfall.** The closure-language scan over the full git log surfaced 11 open ids with closure-shaped commit text; all 11 were checked individually and 9 turned out to be *mentions* rather than closures (e.g. `eea2c1c` reads "closes [#437], closes [#439], closes [#444]; **[#433] stays open**"). A grep-only pass would have proposed closing #433. The engine is genuinely tidy; there is not a large hidden pile of dead rows.

**Limit 2 — every non-DEAD verdict is mechanical, not individually adjudicated.** LIVE vs AWAITING-RULING was decided by parsing the Done-when clause, and LIVE (deferred/pegged) by frontmatter. Each of the 181 rows was *read*; each was not *investigated to the depth the four DEAD candidates were*. A row classified LIVE here may still be dead on evidence this sweep did not reach — particularly the pre-#100 cohort, whose referents are oldest. Treat §4 as a triage map, not as 181 ratified verdicts.

**Limit 3 — ruling-owner assignments are the draftsman's reading of ADR-108 §A, applied one week after the ADR was accepted.** The three CONFLICT flags are the confident ones (they name an operator ruling for an explicitly technical fork). The `arch` default on the remaining ~26 is a *proposal*: it follows §A item 2's instruction that uncertainty is a reason to decide rather than escalate, but the architect may hold that some are genuinely functional.

**Limit 4 — the container arrived as a SHALLOW CLONE and the first pass ran against truncated history.** `.git/shallow` was present, history grafted at 2026-07-26 (264 commits). Two consequences were caught and corrected mid-session rather than shipped: (a) the `canonical_freshness` ship-gate organ hard-failed on `VISION.md` purely because the graft point *looked* like the file's last edit — `git fetch --unshallow` (4140 commits, back to 2026-03-30) cleared it, and the true last edit `30a8c42b` (2026-07-25) is not stale; (b) the closure-language scan behind §1 initially reached back only five days. **It was re-run over all 4140 commits after unshallowing**, which is what surfaced the [#35] `e6f9bd73` citation and the [#370] refusal history. Anyone reproducing this dossier on a fresh cloud checkout must unshallow first, or the evidence base is five days deep and the freshness organ lies.

**Limit 5 — no cross-repo verification.** Rows whose evidence lives in `ai-council` or `corp-monorepo` (e.g. [#401](a), [#416], [#429], [#430]) were classified on their in-repo text alone. This session had no access to consumer trees. **GAP: consumer-side premises unverified.**
