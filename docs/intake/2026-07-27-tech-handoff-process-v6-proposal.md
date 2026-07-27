---
intake-id: 18
status: DRAFT
origin: operator-directed audit arc, worktree handoff-review, 2026-07-27 (evidence base = the same-day verification audit; browser-witnessed seed 2026-07-26/27 folded with provenance labels)
consumers: operator ratification → the intake #17 D3 "handoff ADR" and/or a HANDOFF_PROCESS version bump (v5.8-additive or v6 — §9 below); until then nothing in protocols/ changes
note: PROPOSED pack. Every amendment is a MECHANISM (probe leg / template field / generator or assembler beat / validator rung / hook extension), never a stronger sentence; each carries an explicit DEFER. Filed at DRAFT on the operator's explicit filing order (the arc brief); the §6 confirm-gate is satisfied for FILING by that order — CONTENT ratification is pending, which is what DRAFT means here.
---

# HANDOFF_PROCESS v6 — amendment proposal pack (PROPOSED)

**Evidence base:** `docs/audits/2026-07-27-verification-handoff-process-audit.md` (same arc; finding IDs BW-a…BW-h / RM-1…RM-6 / W1…W9 cited below without re-arguing them).
**Reading contract:** Status PROPOSED — nothing in `protocols/` changes until the operator ratifies. Amendments are paste-ready: each **Mechanism** block contains the literal text/change to apply, executable from this intake alone. The evaluation frame is the equilibrium contract (ADR-87): every amendment states which SIDE it loads (browser emits intent/contract/off-repo inputs; CC self-loads and mechanizes the rest) and why that side is the cheap one.

## 1. Prior art (mandatory row — the intake #17 precedent)

| Prior art | What it is | How this pack uses it |
|---|---|---|
| 2026-07-04 adoption review, RF-1 option (b) | "strip expected-values… add a one-line rung" — adopted, landed `9d5ebe5`, became v5.4 §5 | The proof that mechanism-shaped amendments to this spec WORK: a prose contract that eroded for 3 weeks stopped eroding the day it grew a validator rung. Every amendment below copies that shape |
| §4 boot on-load acknowledgment (ADR-79 visible-paste) | The one existing truncation-visibility mechanism | A1 generalizes it to every cross-boundary artifact instead of inventing a new scheme |
| s7 night audit §4 (2026-07-19) | A drafted 7-item multi-agent mandate checklist (PLAYBOOK §2 amendment), unratified | A4 adopts it by reference — the text exists; re-drafting it here would fork it |
| s6 night audit §4 + #353/#344/#349 | Filed session-concurrency organ shapes (boot snapshot, PreToolUse refusal, session-lock advisory) | Deliberately NOT re-proposed (§10) — BW-d's owners exist; this pack takes only the handoff-side share (destination contract, A4) |
| intake #17 D3 (operator-ruled) | PLAN.md four-state lifecycle (DRAFT → REVIEWED → APPROVED → CLOSED(outcomes)), review SLA, deviation split — "lands where: handoff ADR" | A9 is the paste-ready §13 text for exactly that ADR; this pack does not re-decide D3 |
| [#301] (DEFER, peg #298) · [#423] · [#421]/[#422] | Filed build legs: PLAN generator; integration-sequence mechanization; probe-tooling defects | Cited as owners; A9/A11 route to them rather than duplicate |
| ADR-87 item 7 (the inoculation ladder) | ADR → PLAYBOOK → ESSENTIALS one-liner → per-session carrier | A8's promotion-debt beat mechanizes walking this ladder; s4 proved it works when driven (RULING-W reached ESSENTIALS only after an audit pushed it) |
| ADR-85 + `session_end_backpressure` | The deterministic session-end gate precedent | The advisory-beat shape A8 attaches to |
| v4 stage1/stage2 mechanism (archive/) | The pre-v5 receiving-session comprehension proof | Historical control: v5 §5 replaced prove-you-read with live-only probes; nothing below reverts toward stage-quizzes |

## 2. A1 — Truncation-visible artifacts (end-sentinel + section count)

- **Guards:** BW-a (transport corrupted several pastes in one window; the browser cannot know a paste is partial).
- **Mechanism (paste-ready):**
  1. `scripts/assemble_paste.py` appends a terminal section to every `PASTE_THIS.md`:
     `--- \n=== END OF PASTE — {n} sections · {bytes} bytes ===`
     (n = the manifest sections actually folded; deterministic, not an answer value).
  2. `protocols/HANDOFF_BOOT.md` on-load line extends: reply `Booted as the Layer-1 browser under HANDOFF_PROCESS v5. Ready for CC's handoff. ({n} sections received.)` — a count mismatch or missing END line = incomplete paste, re-paste.
  3. One rule line in the boot's Verification-split section: "An artifact that does not end with its `=== END …` sentinel is TRUNCATED — say so and stop; do not review a truncated artifact."
  4. PLAYBOOK Ch4 channel-discipline gains the report-direction sibling: any load-bearing CC→browser report longer than one screen ends with `=== END — {k} sections ===`.
- **Lives at:** `scripts/assemble_paste.py` · `protocols/HANDOFF_BOOT.md` · PLAYBOOK Ch4.
- **Equilibrium side:** CC/generator emits (deterministic, one function + three prose lines); the browser's share is a zero-cost visual check — the same split §4's ack line already ratified. Cheap side because only the emitter can make truncation visible.
- **Cost:** S (≈20 LOC + template lines + tests).
- **DEFER option:** keep the supplement's prose rule only. Deferral re-accepts the witnessed corruption class going undetected mid-review.

## 3. A2 — Transport-medium contract (M+ artifacts travel as files)

- **Guards:** BW-a (the upload rule lives only in a consumed transient; the outbound direction already has a codified sibling — ESSENTIALS "Scale M+ → downloadable `.md` prompt").
- **Mechanism (paste-ready):** add to HANDOFF_PROCESS §13 (`PASTE_THIS.md` convention paragraph):
  > `PASTE_THIS.md` is the ONLY sanctioned chat-paste artifact. Every other load-bearing artifact crossing the CC → operator → browser boundary (a report, review, aggregate, plan) travels as a FILE the operator uploads, never as chat-paste — the report-direction sibling of the ESSENTIALS Scale-M+ rule. CC states the transport at emission time ("this travels as a file").
  Plus the matching one-liner in ESSENTIALS "Architect disciplines" (the ADR-87-item-7 ladder step), and the assembler's over-budget warn text gains: "artifacts other than PASTE_THIS must not be pasted at all."
- **Lives at:** HANDOFF_PROCESS §13 · ESSENTIALS · `scripts/assemble_paste.py` warn string.
- **Equilibrium side:** the rule binds the operator relay, but the enforcing surface is CC's emission-time statement — CC-side, cheap because the rule already exists in the other direction and needs only mirroring.
- **Cost:** XS (text).
- **DEFER option:** status quo (supplement line only) — which demonstrably failed within the window it was written.

## 4. A3 — Branch-grammar reconciliation (`worktree-` / `epic/` sanctioned)

- **Guards:** BW-b / RM-6 (canon self-contradiction: PLAYBOOK Ch8's verified `worktree-<name>` vs the §4 "these four only" prefix rule; every worktree session boots into a grammar it violates; briefs invent names like `wt/<id>-<slug>` because the recorded contract loses to the louder rule).
- **Mechanism (paste-ready):** amend the hub-owned §4 region (`templates/claude-regions/conventions-commit-branch.md` + CLAUDE.md §4 in lockstep, byte-match):
  > Branch prefixes are `feat/ fix/ docs/ chore/` (author-chosen branches — these four only), **plus two machine-produced lane prefixes: `worktree-<name>` (native parallel-session worktrees, `claude --worktree` / EnterWorktree) and `epic/<slug>` (root-provisioned epic lanes, §14a). Lane branches are never self-merged and never author-invented — a brief that names a lane branch names it in one of these two shapes.**
  The same edit is owed to `~/.claude/rules/core-invariants.md` #5 — **global infra, exception-with-ruling (core-invariant #6): flagged for an explicit operator ruling, not executed by this pack.**
- **Lives at:** CLAUDE.md §4 region + its template extract (lockstep) · core-invariants #5 (ruling required).
- **Equilibrium side:** CC-side text; trivially cheap; removes a contradiction both actors currently resolve by improvising.
- **Cost:** XS + one operator ruling for the global file.
- **DEFER option:** live with the contradiction; briefs keep guessing branch names (the BW-b class recurs).

## 5. A4 — Destination contract + the multi-agent mandate checklist

- **Guards:** BW-b (brief-side validation), BW-d (the handoff-side share: declare the lane ex-ante), BW-g (mandate content standard).
- **Mechanism (paste-ready):**
  1. **Adopt s7 §4 by reference:** land the seven-item "Multi-agent / fan-out prompt checklist" drafted verbatim in `docs/audits/2026-07-19-technical-night-s7-prompt-authoring-quality.md` §4 into PLAYBOOK §2 (fan-out shape · worktree+branch · read-only-vs-write-scope · codex lane · plan-mode basis · deliverable naming+location · close discipline). Do not re-draft; the text exists.
  2. **HANDOFF_PROCESS §13 gains one paragraph:** "Every brief or prompt that opens a lane declares its destination ex-ante: worktree name · branch (in a sanctioned lane shape, §4 grammar) · write-scope · execution MODE with basis — the §14a items 3/4/7 shape generalized beyond epic lanes. A lane inherits none of these from a prior prompt."
  3. **Probe leg (generator):** the v5 probe-core template's branch-note becomes a checkable row — P3 extends: "state the live branch AND compare it to the bundle/brief-declared destination; mismatch = FAIL." Deterministic and live-only; the declared destination is a contract to check against, not an answer hint (the existing PROBES branch-note precedent: "re-derive… do not trust this line").
- **Lives at:** PLAYBOOK §2 · HANDOFF_PROCESS §13 · `templates/handoff/v5/PROBES.md.tmpl` + `scripts/gen_handoff.py`.
- **Equilibrium side:** the browser emits one destination line (already its ADR-87 load: intent + mode); CC mechanizes the check. CC is the cheap side — one template row + one comparison.
- **Cost:** M (spec text XS; probe leg S; the PLAYBOOK checklist is an adoption, not a build).
- **DEFER option:** ratify s7's proposal in its own lane and take only item 2 here; or full defer — briefs stay unvalidated and the `wt/` class recurs. Integration-sequence mechanization stays [#423]'s, untouched either way.

## 6. A5 — JOURNAL lane-letter allocation

- **Guards:** BW-c (two lanes both wrote "(b)"; the merge conflict is the current coordinator, one manual resolve per collision).
- **Mechanism (paste-ready):** lanes stop allocating letters. A lane's wrap header is `### YYYY-MM-DD (lane: <branch-name>) — …`; the letter is assigned at INTEGRATION on the primary (letters exist only on main). Convention line lands in PLAYBOOK §8 (parallel-session subsection). Build leg (optional, later): extend the existing `normalize-dated-headers` pre-commit hook to rewrite `(lane: …)` → next-free letter when committing on main — the hook already owns dated-header normalization, so this is its natural second rule.
- **Lives at:** PLAYBOOK §8 (convention, XS now) · `normalize-dated-headers` (hook extension, S, later).
- **Equilibrium side:** CC-side, deterministic.
- **Cost:** XS now / S for the hook leg.
- **DEFER option:** status quo — the conflict-resolve-at-merge ritual continues (witnessed working 07-27, at the price of one manual resolution and one misleading commit subject per collision).

## 7. A6 — SUPPLEMENT question 7: the ratified-in-chat register

- **Guards:** BW-e (chat-born terms have no provenance path; K1–K5 sat "undefined in-repo" until a recording batch; S3d reached LESSONS only the same way).
- **Mechanism (paste-ready):** `templates/handoff/v5/SUPPLEMENT.md.tmpl` QUESTIONS gains:
  > 7. **Ratified-in-chat register** — terms, rulings, or contracts ratified in this window's chats that are NOT yet recorded in the repo: the verbatim term · a one-line definition · its intended durable home (BACKLOG id / ADR / LESSONS / PLAYBOOK §). "None" is a valid answer.
  HANDOFF_PROCESS §13's schema list updates "the fixed 6-question schema" → 7, with the scope note: **capture-only** — an answer here is transcription DEBT surfaced at the boundary, not canon; recording happens in the next session (the recording-batch pattern, cf. `833e7f6b`), and the answer is advisory like every supplement answer (never trusted over the repo).
- **Lives at:** `templates/handoff/v5/SUPPLEMENT.md.tmpl` · HANDOFF_PROCESS §13 schema paragraph.
- **Equilibrium side:** **deliberately browser-side** — the one load only that side can carry (ADR-87: off-repo inputs are the browser's to emit; at ratification time the chat is the sole holder of a chat-born term). Cheap because the fill→fold→JOURNAL pipeline already exists end-to-end; this is one question riding built machinery.
- **Cost:** XS.
- **DEFER option:** keep relying on ad-hoc recording batches — accepts an unbounded chat-only interval for operator-ratified vocabulary.

## 8. A7 — Standing-topic reconciliation probe (P0 class)

- **Guards:** BW-f (the reconcile-[E8]+intake-#17-first rule failed three consecutive windows as paste-prose; "a rule with no probe has no teeth").
- **Mechanism (paste-ready):** `gen_handoff.py` emits, in architect mode, a **P0 — standing-topic reconciliation** row ABOVE P1, deterministic legs only (the RM-4/S3d boundedness law):
  | leg | question | binds to | CC verifies via |
  |---|---|---|---|
  | P0a | Quote live the reconciliation-debt / preamble list of the active epic theme(s) | `BACKLOG.md` `[E#]` preambles (machine-locatable headers) | read the live preamble; quote must substring-match |
  | P0b | Quote live the plan-of-record wave/sequence line of every intake with `status: ACCEPTED, disposition: active` | `docs/intake/*.md` frontmatter (already machine-parsed by `gen_intake_index.py`) | enumerate frontmatter → read each §plan line live |
  | P0c | State which wave/row this bundle's Purpose serves — unquotable or contradicted = FAIL | the bundle's own FILL-IN purpose vs P0a/P0b output | compare; mismatch = FAIL, route to the escalation ladder |
  §13(c)'s opening sequence extends: **role → vision → standing topics → backlog**. No open-ended adjudication leg — per JOURNAL 07-26 (h), whole-set grooming is an arc, not a probe.
- **Lives at:** `scripts/gen_handoff.py` + `templates/handoff/v5/PROBES.md.tmpl` · HANDOFF_PROCESS §13(c).
- **Equilibrium side:** CC/generator — both source surfaces are already machine-parsed, so the marginal cost is a template row and two greps; the browser's share is the run-loop it already performs.
- **Cost:** M (generator + template + validator fixture).
- **DEFER option:** keep the rule as §13 prose. Honest note: that exact configuration just failed three consecutive windows, so DEFER re-accepts a witnessed, named failure mode.

## 9. A8 — BINDING-line fold inventory (promotion debt surfaced)

- **Guards:** BW-h (rulings stranded in consumed transients; the Pyrefly near-reversal; s4: 4 of 6 rulings never walked the ADR-87-item-7 ladder; CC already hand-compensates by copying rules to JOURNAL).
- **Mechanism (paste-ready):**
  1. `scripts/assemble_paste.py`, when folding a non-empty ANSWERS region, scans it for `/(BINDING|do not relitigate|MUST NOT|ruling)/i` and prints a **PROMOTION DEBT** block (stdout + appended to the `gen_handoff` JOURNAL draft): each matched line verbatim + the ladder prompt "durable home: ADR / PLAYBOOK / ESSENTIALS one-liner / carrier?" Advisory — never blocks a fold.
  2. HANDOFF_PROCESS §5 failure-handling gains one sentence (promoting the sol-catch rule from supplement prose to spec): "A ruling-existence search that excludes `docs/handoffs/` is unsound — binding rulings also live in handoff artifacts until promoted."
- **Lives at:** `scripts/assemble_paste.py` · HANDOFF_PROCESS §10 (failure handling) + §13 supplement contract.
- **Equilibrium side:** CC/assembler — a deterministic grep at a beat that already runs; the operator sees the debt list at the exact moment the transient is consumed.
- **Cost:** S.
- **DEFER option:** full-defer to [#433]'s genre-lifecycle engine (the decision-register workload is the structural fix — "DECISIONS do not belong in a queue file"). Interim cost: the relitigation class stays live until the restructure ships; A8 is explicitly the cheap interim, designed to be deletable when [#433] lands.

## 10. A9 — PLAN.md, the D3 four-state artifact (spec text for the ruled handoff ADR)

- **Guards:** BW-g (the per-session prompt/plan lifecycle needs a committed carrier) + RM-2 (the runbook overstates PLAN.md as current; the practice decayed after two pilots because no spec text holds it).
- **Mechanism (paste-ready):** HANDOFF_PROCESS §13 bundle-shape paragraph gains:
  > An architect bundle MAY carry `PLAN.md` — the session plan, CC-authored, never pasted. Its lifecycle is **DRAFT → REVIEWED → APPROVED → CLOSED(outcomes)** (intake #17 D3, operator-ruled): review SLA one working day at DRAFT, then cold-review fires; deviations split — scope changes require a mid-session operator ruling (strict), order/mechanics changes require only an OUTCOMES entry with rationale (loose).
  The runbook's PLAN row reconciles to "optional (D3 states)" at its next freshness window. The generator/RETROSPECTIVE build stays [#301] (peg #298) — this amendment gives D3 its spec home, it does not build.
- **Lives at:** HANDOFF_PROCESS §13 · `docs/handoffs/README.md` (owner's next window — NOT this arc, the file is freshness-gated and outside this arc's write set) · build: #301.
- **Equilibrium side:** CC-side text; the operator's review beat is exactly the D3 ruling already made.
- **Cost:** XS (text; build already pegged elsewhere).
- **DEFER option:** leave D3 homeless until its ADR materializes on its own; the runbook keeps overstating.

## 11. A10 — Spec-currency batch (rides the same bump; no new mechanism)

- **Guards:** RM-1, RM-3, RM-4, plus the s4 row-1 reconciliation debt.
- **Mechanism (paste-ready), four independent XS items:**
  1. **§15 order fix (RM-1):** "LESSONS.md: append-only (oldest-first)" → "LESSONS.md: append-only, **newest-first** (new entries at the top of the Entries section, per the file's own header and ADR-29)."
  2. **§4 honest boot (RM-3):** "~3-line core" → "a compact boot core (identity / one meta-rule / first-move) plus the resident browser-role doctrine — resident because a CC-held file never transmits to the file-less browser"; AND a stated byte budget for `protocols/HANDOFF_BOOT.md` checked by the assembler's existing size machinery (it already measures the file as paste section 1) — growth past budget warns, mirroring the paste budget.
  3. **§5 condition 4 (RM-4):** add to the teeth-bearing conditions: "**Bounded-deterministic** — the verification terminates in bounded mechanical steps at check-time. A probe whose honest answer requires unbounded judgment over an open set is an arc, not a probe, and is rejected (origin: P10, JOURNAL 2026-07-26 (h); LESSONS 2026-07-27 S3d)."
  4. **§14a cross-refs (s4 row 1):** FILE-BOUNDARY (item 4) and Refusals (item 6) gain naming references to RULING-W (hub→consumer writes: worktree/branch → report, never direct push) and the ADR-101 two-tier new-path rule — both currently absent from the section that governs lane boundaries.
- **Cost:** XS each. **DEFER:** per-item; each is an independently ratifiable line.

## 12. A11 — Probe-tooling debt adoption pointer (no new proposal)

[#421] absorbs the second tokenizer variant (backticked `#id` in a source column parses as an anchor — witnessed 07-26, unfiled at window close); [#422] gets its detector as a validator rung (grep the bundle for cold-state claims when the shared fill-state says FILLED — deterministic, the manual sweep mechanized); `verify_handoff_probes.main()` exposes the `repo_root`/`cross_repo` params `verify()` already has (the 4 false-FAILs on hand-runs of cross-repo bundles). All S-cost, all in filed territory. **DEFER = the de-facto present.**

## 13. Version + ratification path

Every amendment above is **additive** — no v5 rule is removed or weakened, so by the v5.1–v5.7 precedent this pack lands as **v5.8** in one coupled atomic move: `CONTRIBUTING.md` stamp, the 5 `reconciled_with` edges (`ARCHITECTURE.md` · `CLAUDE.md` · `CONTRIBUTING.md` · `docs/handoffs/README.md` · `protocols/HANDOFF_BOOT.md`) @→5.8, each site enumerated + verdicted per `check-against-spec`, freshness-gated dependents genuinely re-read. The operator MAY still choose the **v6** label to mark the scope expansion (parallel-lane coordination, provenance capture, transport integrity — surfaces v5 never claimed); the content does not force it. A6/A9/A10 are pure spec/template text and can ratify first; A1/A7/A8 carry small builds; A3 requires one global-infra ruling; A4 is an adoption of s7's drafted text.

## 14. Explicitly NOT proposed here (anti-duplication kill-list)

- The BACKLOG/decision-register restructure and the genre-lifecycle engine — **[#433] / [E8]** own them (A8 defers to that engine by design).
- Session-concurrency organs (boot snapshot, PreToolUse refusal, session-lock) — **#353 / #344 / #349 + s6 §4** own the shapes; BW-d's prevention lives there, not in a transport spec.
- Integration-sequence mechanization — **[#423]**.
- The PLAN.md generator/RETROSPECTIVE build — **[#301]** (peg #298).
- Prompt-template fan-out fields — **s7 §4** owns the drafted text (A4 adopts, does not fork).
- The morning loop / nightly-consumer edge — **[#428] + the 07-26 §7 amendment's extraction-pass ruling** (executed as [#434]).
- Any edit to `docs/handoffs/README.md` this arc — freshness-gated and outside this arc's write set; A9 notes the reconciliation for its owner's next window.

## 15. Template-section map (honest, per the intake #17 precedent)

| Template section | Satisfied by | Honest status |
|---|---|---|
| Problem / motivation | §0 of the companion audit (verdict paragraph) + each amendment's Guards line | Present by reference |
| Scenarios (+1 view) | The witnessed incidents ARE the scenarios (BW-a…h with quotes) | Present as evidence, not as "as the operator I…" walkthroughs — genre caveat, same as intake #13/#14/#17 |
| Functional requirements | The Mechanism blocks (must-shaped, paste-ready) | Present as amendments rather than must/should/could |
| Acceptance criteria (ex-ante) | Per amendment: the mechanism exists + its DEFER not taken + (where a probe/validator) a fixture exercising it; pack-level: a future window where the BW-f/BW-h class CANNOT recur silently | Present, distributed per amendment |
| Non-goals | §14 kill-list | Present |
| Impact sketch (4+1 lite) | Logical: spec §§4/5/13/14a. Process: fold/generation beats. Development: 4 scripts + 2 templates. Physical: none (no new files, no new folders) | Present |
| Open questions | v5.8-vs-v6 label (§13); the A3 global-infra ruling; whether A8 ships or full-defers to [#433] | Present |
| Status | Frontmatter (DRAFT; body PROPOSED) | Present |
