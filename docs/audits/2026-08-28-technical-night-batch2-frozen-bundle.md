# NIGHT-BATCH-2 CONTRACTS — 2026-08-28 · frozen by the Layer-1 architect

**Shape (prior-seat R-Q2):** local mutation lanes = worktrees, commit-and-STOP, NO self-merge,
morning integration in TWO queues · cloud = READ-ONLY research, exactly ONE self-contained
artifact per lane, returned by operator paste (Harvest-Cloud ships tonight in N2 but is not
relied on) · no waved/self-integrating acts — no pre-authorized mission file exists tonight.
**Dispatch:** every launch line COPIED from PLAYBOOK Ch8's dispatch table (SOLE literal-command
site), Q1–Q4 cut per lane, receipt captured. Local substrate default per Z-G3. Cloud lanes may
NOT run hub gates (uv 0.8.17 vs pin, measured); any gate-dependent claim in a cloud artifact is
marked MEASUREMENT-OWED-LOCAL, never estimated.
**Night manifest:** produced per the 2026-08-27 reference instance, correct schema, before any
lane boots. **Reviewer:** terra pre-merge on every LOCAL lane, tally-in-body.

## RULINGS FOLDED (decisions owed → decided)

- **D1/N5:** MOOT — `ecosystem/routing-table.yaml` + agreement check ALREADY LIVE on main
  (batch-1 L5, merge 85f3e71c). The [#613] row body is stale; integrator updates it in the
  morning. Remainder: operator's L0 one-liner (pending) → check green → tier promotion =
  MORNING INTEGRATOR ITEM, not a lane. N5's slot is taken by N8.
- **D2:** ratchet move authorized for **N3 ONLY**, carried in the operator's GO, bounded to the
  night-protocol section + the HANDOFF_PROCESS forms-card delta; old→new count reported.
- **D3:** [#612]'s archival destination = **`tasks/archive/`** — the operator's own stated
  requirement ("archive folder w taskach, żeby widzieć co ubywa"); new-folder approval carried
  in the GO.
- **D4:** merge order CONFIRMED: win-tooling queue **N2 before N1**; hub-adjacent coupling
  **N1 before N6** (N1 exercises the tool N6 rewires — files disjoint, behaviour not).
- **P5 (tag):** v1.4.0 is a LIGHTWEIGHT tag; siblings are annotated and manifest-v1.0.0's
  comment says "annotated + resolvable". N1's first act includes the annotation-requirement
  check; if annotation is required, that step STOPS and reports (morning operator fix —
  re-tagging is a history-adjacent act, never improvised at night).

## SHARED CLAUSES (every local lane)

A5: generated surfaces (BACKLOG.md, doc-counts.md, doc-code-edge.yaml, indices, ALL_CHECKS
registrations) resolved by REGENERATION at integration, ONCE on the merged result. N4 is the
batch's EXCLUSIVE tasks/ writer; every other lane REPORTS candidate filings for the integrator.
RATCHET: only N3 may move 443; every other lane's protocols/+templates/ delta must be 0,
verified pre-commit. Decision budget: standing rulings silently; ask only curated-baseline /
rule-vs-ruling / no-ruling fork / out-of-scope path (P1); everything else per defaults, ONE
lane packet: per-item MET/NOT-MET, commits, terra tally, candidate filings, budget decisions.

---

## LOCAL — hub queue (5): N3 · N4 · N6 · N7 · N8

### N3 — [#610] doc half: the night-batch protocol chapter — M — RATCHET LANE
Write-scope: `protocols/PLAYBOOK.md` + `protocols/HANDOFF_PROCESS.md` (forms-card delta ONLY) —
the batch's single ratchet authorization covers both; no other protocols/ file.
Intent: the night protocol stops being operator habit; and the two rules this window proved can
die in a seat's head become bundle-carried doctrine.
Done: (1) a named PLAYBOOK section enumerating all five phases — dispatch, manifest, night run,
morning adjudication, ledger — each with inputs, outputs, refusal conditions; (2) manifest shape
specified so two seats produce identical sections; the 2026-08-27 landed manifest validates as
the reference instance; (3) byte-identical-or-state-the-deviation rule, citing the two C-reports
that opened with prose; (4) report-selection rule names the Stop-hook-noise trap; (5) ledger is a
REQUIRED output; (6) intake-#60 constraints travel here: ~5 proposals/night cap, 7-day
auto-expire, no autonomous semantic refactoring at night, proposals land as docs/intake/ SEEDs;
(7) **prior-seat R-Q1/R-Q2 land as doctrine:** the session-boundary rule (five-pillar close;
architect never initiates the bundle; operator declares closure) + the substrate-routing answer
(local/cloud/Codespace, incl. the measured uv-provisioning nuance — "unrunnable by default,
runnable after `pip install --target` provisioning", per the Ch8 Q1 amendment candidate) +
HANDOFF_PROCESS forms-card carries both, so every future bundle boots them; (8) ratchet old→new
reported.
Anti-patterns: naming N2's verbs as though they already resolve · touching Ch8's dispatch table ·
any protocols/ file beyond the two named.

### N4 — [#612] doc-rot row-body archival — M — EXCLUSIVE tasks/ owner
Write-scope: `scripts/validate_doc_rot.py` · `tasks/archive/` (destination per D3) · `tasks/*.md`.
Intent: row annotation is unbounded debt; the fix is RELOCATION, not trimming — a durable
per-row record takes the narrative load, the row keeps a pointer. This is the operator's
"widzieć co ubywa" made mechanical.
Done: (1) `tasks/archive/` exists with a ruled write path; (2) validate_doc_rot re-run shows
backlog-row-length STRICTLY REDUCED with NO CONTENT DESTROYED — byte-identical relocation,
provable; (3) P4 discharged: the 77-findings figure re-measured BEFORE and AFTER, both recorded;
(4) doctrine documented at the doc-rot home; (5) integrator's filing wave lands through this
lane's mechanism where applicable.
Anti-patterns: trimming instead of relocating · any non-byte-identical move · deleting a row ·
touching protocols/.

### N6 — [#605] de-hardcode consumer-root resolution — M
Write-scope: `deploy/tool.py` · `scripts/audit.py` · one new test file.
Intent: the hub stops assuming every consumer is a filesystem sibling under Dev/ — the premise
any off-laptop substrate needs.
Done: (1) consumer-root resolution EXPLICIT in both modules with the sibling default as
fallback; (2) a non-sibling layout resolves in both, PROVEN BY A TEST; (3) `audit repo <name>`
runs from a checkout with no sibling tree; (4) deploy/tool.py's docstring tells the truth.
MERGE ORDER: after N1 (D4). Anti-patterns: changing preflight refusal semantics · touching
manifest files · widening into the profile-ruling read (separate row).

### N7 — CANDIDATE C-A: the [#577] byte-cap test — S
Write-scope: `tests/` — one new file (reads AGENTS.md + CLAUDE.md, edits neither).
Intent: batch-1 measured the combined global+root payload at 9,161 B = 28.0% of Codex's 32 KiB
project_doc_max_bytes cap and reported it UNGUARDED. The figures exist; the gate does not.
Done: (1) a test asserts the combined payload IN BYTES against the cap; (2) fails on a planted
oversize fixture; (3) [#577]'s done-when fully discharged — said so in the packet.
Anti-patterns: editing AGENTS.md/CLAUDE.md · asserting lines (this corpus averages ~117 B/line) ·
regenerating doc-counts (integrator, once).

### N8 — pre-freeze contract validator: [#591] extension, prior-seat R-Q4 — M
Write-scope: the [#591] validator module (`scripts/validate_substrate.py` or its ruled sibling —
extend the existing organ, LIBRARY-FIRST on our own organs, never a new rival) + its tests.
Intent: the three architect premise errors of 2026-08-28 become mechanically impossible at
freeze time, and the live `**Shape:**`→'one' mis-parse (finding C-F) is fixed in the same organ.
Done: four predicates run on a contract FILE at freeze time, each with a failing-then-passing
test: (i) every referenced off-repo input EXISTS at freeze; (ii) every "verified"/"measured"
claim carries a witness (command or file:line); (iii) every cited [#id]/ADR/register id resolves
live; (iv) the declared do-not-touch set is checked against detector scope roots. Plus: (v) the
C-F defect fixed — `**Shape:**` prose no longer parses as a substrate declaration, regression
test included; (vi) batch-1's frozen contract, run through the validator, reproduces exactly the
three known defects (the validator's own acceptance evidence).
Anti-patterns: a new standalone checker beside [#591] · predicates as prompt prose · weakening
the substrate check to make C-F "pass".

## LOCAL — win-tooling queue (2): N2 then N1 — RULING-W shape, both

### N2 — [#610] carrier half: Dispatch-After · Harvest-Cloud · cp-quote — M
Write-scope: win-tooling `config/dispatch-helpers/DispatchHelpers.psm1` + `tests/
test_dispatch_helpers_*.py`. Consumer repo ⇒ RULING-W: consumer worktree/branch → report;
never direct hub writes; mechanism-before-act.
Intent: the two verbs the 2026-08-26 night performed BY HAND get names — the missing half of the
cloud fleet the operator wants. Harvest-Cloud is an EXTRACTION (the paginated
GET /v1/code/sessions/{id}/events loop already exists inside Start-DispatchCloudV2 ~line 1079);
Dispatch-After is documented as a FORM OF the ruled Dispatch verb, never a rival.
Done: (1) both verbs exist, each with a usage line and its API surface recorded; (2) **P2 first:
locate and REPRODUCE the cp-quote defect** (the argv seam is correct by construction — suspect
the remote-path construction at ~lines 1279/1282/1402), then fix with a test that FAILS before
and passes after; if it cannot be reproduced without a live codespace, ship the verbs, mark the
cp fix MEASUREMENT-OWED with the reproduction recipe, and say so; (3) targeted tests only — the
full suite is ~18 min and carries ONE pre-existing env RED (faster_whisper) that is NOT this
lane's; (4) commit-and-STOP on the win-tooling branch.
Anti-patterns: renaming the existing Dispatch-* family · touching .claude/ or
.pre-commit-config.yaml (N1 owns them) · reporting the known env RED as a lane failure.

### N1 — [#604] remainder + [#606] win-tooling first slice — L
Write-scope: HUB `ecosystem/{deployed-versions,satellite-onboarding-rulings,parity-surfaces}.yaml`
+ `ecosystem/win-tooling/history/` · CONSUMER win-tooling `.claude/` (CLAUDE-FLOOR.md,
settings.json) + `.pre-commit-config.yaml`. RULING-W throughout: the authorizing amendment lands
BEFORE the consumer write.
Intent: win-tooling goes from zero enforcing organs to floor + pre-commit set + session gate +
/ship at engine v1.4.0, parity flips pre-deploy→consumer, and the repo stops being one disk
failure from loss. The operator's deployment mandate, landing.
Done: (1) **re-measure first** — every hub-side claim about win-tooling re-derived on the live
consumer (the hub picture is a PLAN: 51 baseline commits are local-only; treat X1 as the one
verified discharge — v1.4.0 resolves local AND origin, so [#606]'s blocking precondition is
DISCHARGED); (2) **P5 check** — establish whether the deploy path requires an ANNOTATED tag; if
yes, STOP that step, report for the morning; (3) deploy: floor present, pre-commit set armed,
session gate + /ship live, verified by `audit repo win-tooling` reporting so, with a FRESH
baseline in `ecosystem/win-tooling/history/`; (4) parity `role: pre-deploy → consumer` flipped
AFTER the proof, never before; (5) [#604] fold: terminal-setup carries a null-valued
deployed-versions key + a rulings entry naming full|floor-only with ruled_by and date; (6)
workspace_settings recorded hand-fixed or accepted-debt — the editor-config carrier is
declaration-only and CANNOT close it; (7) **branch backup:** 11/11 win-tooling branches carry
upstreams (`git push -u origin <branch>` each; backup only, zero merging, zero cleanup —
`git branch -vv` recorded); (8) commit-and-STOP on both sides.
Anti-patterns: writing into win-tooling outside RULING-W · touching DispatchHelpers (N2 owns it) ·
retroactive amendment · trusting the stale hub baseline · improvising a tag rewrite at night.

## CLOUD — read-only (5): C1..C5 — one artifact each, harvested by paste

Shared: zero writes, zero deletions, zero commits; no gate runs (uv mismatch); gate-dependent
claims = MEASUREMENT-OWED-LOCAL. Each ends with EXACTLY ONE self-contained artifact.

- **C1 — 11-CANDIDATE triage sheet.** Input: the batch-1 packet's candidate set, exactly 11
  (2 standing: ratchet zero-headroom; cloud uv · 5 from L3: producer-pack prereqs, corpus
  rotation, served-id, transport-health preflight, locate/re-verify · 4 discovered: byte-cap
  [scheduled as N7 — mark it], Shape-ambiguity [fixed by N8 — mark it], tile manifest, the 664+
  anchored-by-mention WARNs). One row per candidate: proposed ADR-111 disposition — OWNED (name
  the open row) / DISCHARGED (resolving locator) / CANDIDATE (draft one-liner) / REJECTED
  (reason) — each with evidence. A pass routing most items to CANDIDATE has not triaged; say so
  about your own output if it happens.
- **C2 — [#598] slow-marker selector evidence.** Marker taxonomy, selector shape, and what a
  --durations run must produce for the marker set to be REGENERABLE. Durations themselves:
  MEASUREMENT-OWED-LOCAL, never guessed. State the fast set's coverage gap explicitly.
- **C3 — intake-61 ratification sheet.** Options-and-consequences for all five open questions;
  q1 ("what exactly IS the engine?" — assembler, probe gate, seal-identity, boot contract) and
  q2 (copy-with-hash on the floor pattern VS consumer-side pin to a hub release tag — a stale
  copy is detectable, a stale pin is not) get the deepest treatment; q5 tested against the
  ADR-28/36 Layer-2 invariant rather than waved through. NO row proposed — this feeds
  ratification, not filing.
- **C4 — codex-surface census.** Corrected figures: **168** codex-* audit artifacts (not 155),
  587 files tree-wide with codex- references. MUST classify the precedence-trap edge explicitly:
  the codex/ tree is the third precedence layer root AGENTS.md documents BY NAME — a removal
  proposal that deletes the file the precedence section describes is unusable. Every consumer
  counted and classified, removal-ready. ZERO deletion.
- **C5 — README/VISION consumer census.** Every reference into VISION.md and README, classified,
  merge-ready. Two constraints reckoned with up front: root README.md was DELETED 2026-05-23
  (do not propose recreating it as a side effect) and ADR-114 (may a root README be recreated)
  is PARKED, not decided. A merge proposal ignoring either is unusable. ZERO edits.

## MORNING — integration + adjudication

1. Win-tooling queue: N2 → N1, --no-ff, B1 teardown each. Hub queue: N3 → N4 → N8 → N6 (after
   N1) → N7; two integrator sessions IF the first exceeds capacity (prior-seat R-Q2c), split by
   dependency cluster.
2. Regenerate all generated surfaces ONCE; filing wave through N4's mechanism (Z-G1 applied);
   [#613] row body corrected to live state; check promotion once the operator's L0 one-liner has
   run; win-tooling's 4 stale merged worktrees removed (X3: proven fully merged).
3. Cloud artifacts pasted in by the operator; C1's dispositions become the triage I rule on.
4. THEN the solo arc: JOURNAL/LESSONS split (seam 0b08c3e1), hard-bounded to the morning, no
   sibling lanes.
5. ONE packet per queue + the estate numbers the operator asked for: what LEFT the estate
   (archived/discharged counts), what is now visible, what got unlocked.

## DEFERRED, named: [#592] dispatch-drift organ (three-way race with N2+N3 — clean next-batch
triple: N2 ships → N3 documents → #592 asserts) · [#611] v7 (ratchet collision with N3) ·
Codex producer trial (rides AFTER SDA-1 producer prerequisites, per the persisted artifact).
