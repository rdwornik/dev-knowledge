# BATCH-1 LANE CONTRACTS — 2026-08-28 · SEQ 2 · ADR-110 shape

**Shape:** ONE plan → 5 file-disjoint lanes → ONE integration. Operator gates at exactly two
points: GO at batch start · end-of-batch packet. Nothing dripped between them.
**Dispatch:** every lane launch line is **copied** from PLAYBOOK Ch8's dispatch table (SOLE
literal-command site) — Q1–Q4 cut per lane, receipt captured. Substrate default is **LOCAL**
per Z-G3; the cloud rung additionally carries the NEW measured defect below (uv 0.8.17 vs pin
==0.11.19 → hub gates unrunnable there), so no lane that must run gates may route cloud.
**Worktrees:** `claude --worktree <name>` / `EnterWorktree` per Ch8 — never raw
`git worktree add`. Lanes **commit-and-STOP, never self-merge.** Batch runs under `/lane-boot`
/ `/lane-integrate` per Ch8 "The batch protocol".
**Review:** reviewer = terra on EVERY lane pre-merge, severity tally written INTO the persisted
artifact. Absence of a lane's review = that lane does not merge.

## SHARED CLAUSES — copied into every lane's working contract

**A5 — generated surfaces.** `doc-counts.md`, `doc-code-edge.yaml`, `BACKLOG.md`, indices:
resolved by REGENERATION at integration, never hand-merged. Count pins regenerate ONCE on the
merged result, not per lane. Lanes do NOT touch `tasks/` and do NOT regenerate `BACKLOG.md` —
candidate filings are REPORTED in the lane packet; the integrator files them all (Z-G1 applied)
and regenerates once.

**SPINE.** `JOURNAL.md` is the integration spine. No lane writes it except L2's seam commit
(zero bytes moved). Lane anchoring happens at integration per ADR-85/ADR-110.

**RATCHET.** `silent_rule_ratchet` counts `must|shall|never` over `protocols/*.md` +
`templates/*` and the live count must equal the committed baseline **exactly** (443 = 443,
zero headroom, both directions). Any lane whose edit moves that count has touched a curated
baseline: measure the delta BEFORE the edit, and proceed only under the operator's pre-granted
authorization recorded in the GO (bounded to that lane's named correction); report the measured
old→new count in the lane packet. Absent that authorization: STOP and report, do not edit the
baseline.

**DECISION BUDGET (all lanes).** Standing rulings applied silently. Ask only: (a) curated-
baseline touch outside a pre-granted bound · (b) genuine rule-vs-ruling conflict · (c) fork
class with no standing ruling · (d) any path outside the lane's write-scope (P1). Everything
else: decide per contract defaults, report in the lane packet. One packet per lane, batched.

**LANE PACKET (uniform).** Per done-contract item: MET / NOT-MET(+reason) · commits · terra
review artifact + tally · candidate filings to hand the integrator · anything decided under
budget an architect would want to have been asked · commit-and-STOP confirmation.

---

## L1 — [#577]+[#584]: root AGENTS.md + the §10 false anti-pattern, lockstep — M

**Write-scope:** `CLAUDE.md` · `AGENTS.md` (root; ADR-115) · `templates/claude-regions/*.md`.
**Licence:** Z-G2 — the region move is licensed, scoped to the §10 correction ONLY.
**Intent:** the hub stops shipping doctrine contradicting an Accepted ADR (3rd consecutive
revision). Root `AGENTS.md` lands per ADR-115; `CLAUDE.md` §10's "Narrating or managing
AGENTS.md" anti-pattern is corrected via the Form-A region template, lockstep with `CLAUDE.md`.
**Done-contract:**
1. §10 no longer carries the false anti-pattern; the region template and `CLAUDE.md` render
   identically (region mechanism verified, not eyeballed).
2. Root `AGENTS.md` exists per ADR-115's ruled shape and `CLAUDE.md` references it truthfully.
3. `CLAUDE.md` line budget measured with `validate_doc_rot.scan_file_budget` BEFORE and AFTER;
   post-edit within ceiling.
4. RATCHET clause satisfied: delta measured pre-edit; if ≠ 0, executed only under the GO's
   pre-authorization, old→new reported.
5. Terra review artifact persisted, tally-in-body. Commit-and-STOP.
**Anti-patterns:** editorial rewriting beyond §10 · touching other regions · touching the
ratchet baseline file without the pre-granted bound · doc-diet acts (that is L4/I-DOC).

## L2 — I-ROTATE: the SEAM ONLY — S

**Write-scope:** the [#587] tiling seam surfaces exactly as its landed mechanism defines them.
**Intent:** land the executable seam as a **zero-byte-moved** commit (X5/C3), so the actual
JOURNAL/LESSONS split can run later in a dedicated window with no sibling lanes.
**Done-contract:**
1. Seam commit lands with ZERO bytes of content moved; `[#587]`'s mechanism check green.
2. If the seam turns out to require moving any content: STOP, report, do not proceed — that
   discovery re-scopes the row, it does not widen this lane.
3. Terra review (tally-in-body). Commit-and-STOP.
**Anti-patterns:** moving even one entry · touching JOURNAL content · "while I'm here" fixes.

## L3 — Fan-out acceptance + provider preflights (SDA-1 per sol's sequencing) — M/L

**Basis:** the SDA-1 adversarial artifact (persisted by this lane, first act). Sol's verdict is
ACCEPTED as this lane's frame: **fan-out is safe to run now; producer is NOT run this batch**
(C-1/C-2/C-3 compound into a confident wrong ADMIT). No verdicts are emitted by the lane —
computed gates only; ADMIT/REFUSE/INDETERMINATE is the architect's ruling on the evidence.
**Write-scope:** `docs/audits/2026-08-28-*` artifacts (existing folder) · the existing fan-out
instrument's item home for the fresh-half items (answer keys stay OUTSIDE the tree — the
no-pack sandbox's standing rule). **No harness rewrite, no new folders, no producer pack.**
**Work, in order:**
1. Persist the SDA-1 design+critique artifact verbatim into `docs/audits/` (tally already
   in body), with a header noting its cloud provenance and receipt id.
2. **Preflights, per provider (Kimi · GLM · DeepSeek · agy), BEFORE any pack spend:**
   Q2 served-id probe per round (C-9 — a transport that cannot report it caps at
   INDETERMINATE; discover this now, not after 71 items) · rate-shape probe, one small call,
   tag `subscription|pay-per-call|unknown` (C-8; `unknown` = precondition failure) ·
   instruction-file precedence probe (C-10; recorded for the future producer pack).
3. Fan-out pack: carried half (C1-* verbatim, for commensurability with the Gemini/Grok
   record, reported separately) + fresh half (new items, ground truth never committed
   alongside — C-13). Gates G1v2/G2/G3 reused verbatim; `VACUOUS` printed where clause (a)
   is vacuous at R_i=0; G3's comparative leg DROPPED (incumbent billing-blocked) and every
   absolute floor printed with `UNCALIBRATED` beside it until an in-window incumbent run
   exists (C-2). Q0–Q7 preconditions hold or the run does not start.
4. Emit the computed-gates matrix (per provider: gate-by-gate, Φ_fanout with trajectory
   citation, cost, cap-exhaustion count; `EXHAUSTED` is a third outcome, never mapped to
   PASS/FAIL — C-7).
**Done-contract:** SDA-1 artifact persisted (1) · preflight table complete for all four (2) ·
fan-out matrix emitted with UNCALIBRATED/VACUOUS/EXHAUSTED discipline (3–4) · candidate
filings handed to the integrator: producer-pack prerequisites row-candidate (C-1 rejection-tax
cost model + C-6 adversarial suite + C-15 load-bearing list), corpus-rotation candidate
(C-13) · terra review · commit-and-STOP.
**Anti-patterns:** running ANY producer item · emitting a verdict word · comparing against
the carried P_i=9 across heads (B0) · laundering a carried gate defect the artifact names.

## L4 — I-DOC first slice: ARCHITECTURE slim-to-functional per W2/D5 — M

**Write-scope:** `ARCHITECTURE.md` only.
**Intent:** execute the already-ruled W2/D5 slice: functional doc + pointer; no new ruling.
**Done-contract:**
1. The slice matches W2/D5's ruling as written (CC pulls the ruling text; the ruling, not a
   memory of it, is the spec).
2. Nothing deleted without an in-ruling basis; content that leaves has a named destination or
   an in-ruling deletion basis (operator P1 rule: no unasked deletion — where the ruling does
   not already authorize removal, STOP and report).
3. `last_reviewed` frontmatter updated; doc gates green on the lane.
4. Terra review (tally-in-body). Commit-and-STOP.
**Anti-patterns:** slimming beyond the ruled slice · breaking the P1b orientation quote
(ARCHITECTURE Ch1 Layer-2 line must survive verbatim — the boot greps it).

## L5 — [#613]: in-repo routing table + L0 agreement check — S/M

**Unblocked:** operator selected `ecosystem/` (this session), lowercase per ecosystem
convention.
**Write-scope:** `ecosystem/routing-table.yaml` (new FILE in existing folder — path
operator-approved) · the agreement check's code home per the [#592] pattern · `[#613]`'s row
body update via integrator report (not direct tasks/ edit).
**Intent:** the authoritative role→CLI routing table becomes repo-resident and gate-readable;
`~/.claude/ROUTING.md` becomes a DERIVED copy; an agreement check ([#592]-shaped) asserts
they match.
**Done-contract:**
1. `ecosystem/routing-table.yaml` carries the current table: producer=CC (Codex bounded),
   reviewer=terra, adversarial=sol, fan-out=luna/Haiku/Gemini — retrieval-only, with the
   fabricated-count scar recorded as the reason.
2. Agreement check exists, [#592]-shaped, registered per the audit mechanism's existing
   pattern; FAILS (never skips — Z-G4) when L0 copy diverges; degrades to a named report,
   not a pass, when L0 is absent.
3. Ratchet untouched (ecosystem/ + code are outside its scope roots — verified, not assumed).
4. Terra review (tally-in-body). Commit-and-STOP.
**Anti-patterns:** writing to `~/.claude/` (operator-disk — the DERIVED copy is the
operator's act, the check must handle its absence) · a second authoritative copy anywhere.

---

## INTEGRATION — one session, serial, after all five lanes STOP

**Merge order:** L2 (spine seam first) → L1 → L4 (CLAUDE.md-budget interaction) → L5 → L3.
`--no-ff`, one at a time, ancestor-proven teardown per B1 after each (the codified mechanism).
**Acts, in order:**
1. Merge queue per above; per-merge targeted checks (tiered-gating cadence as codified in 0a).
2. Regenerate ALL generated surfaces ONCE on the merged result (A5).
3. **Filing wave** (integrator, Z-G1 applied): lane-reported candidates + the two standing
   ones — CANDIDATE: ratchet zero-headroom freeze on protocols/ (the 7a FLAG; raw finding) ·
   CANDIDATE: cloud-container uv 0.8.17 vs pin ==0.11.19 — hub gates silently unrunnable on
   the Dispatch-Cloud rung (sol session, measured) · L3's handed candidates. CANDIDATEs are
   not births; ledger untouched unless a row is born (then kill-candidates + ledger rules).
4. Full suite ONCE on the merged result; ship-gate read with the standing-WARN frame
   (bare-main comparison, the phase-0 pattern).
5. JOURNAL anchoring per ADR-85/ADR-110; regenerate `BACKLOG.md` via `--emit-source`.
6. **END-OF-BATCH PACKET:** per-lane MET/NOT-MET · merge SHAs + teardown proofs · terra
   tallies (5) · ship-gate delta vs bare main · filings landed · ledger state · the two
   reported numbers (banked delta · operator questions needed this batch) · anything decided
   under budget.
**Worktree hygiene:** teardown per B1 per lane + `git worktree prune`; verify no leftovers.

---

## INTEGRATOR FILING ANNOTATION — appended 2026-08-28 at dispatch, alters no contract clause

Everything above this rule is the operator's frozen contract, copied byte-for-byte from the
prompts dir. Nothing below it is part of the contract; it exists because committing the
contract in-tree subjects it to `check_substrate_declaration`, which the contract was not
authored against.

**Real substrate: LOCAL**, for all five lanes — the contract's own Dispatch paragraph says so
("Substrate default is **LOCAL** per Z-G3"), and the Q1-Q4 cut is recorded in `MANIFEST.md`.

**Why the gate refuses anyway — a parser collision, not a missing declaration.**
`validate_substrate.declared_substrate()` reads `_SHAPE_RE` (`**Shape:**`) FIRST, as the
generator's machine-produced field, and falls back to the prose `Substrate:` spelling only
when `**Shape:**` is absent. This hand-authored contract uses `**Shape:**` for the batch
TOPOLOGY — "ONE plan -> 5 file-disjoint lanes -> ONE integration" — so the parser takes the
value `one` and refuses it as outside the registry. The contract does declare its substrate;
the parser cannot reach the declaration past the collision.

**Substrate deviation:** substrate-no-live-verb — parser collision, not a missing declaration: `_SHAPE_RE` reads the batch-topology line `**Shape:** ONE plan -> 5 lanes` before the prose `Substrate: LOCAL`, yielding the non-registry value `one`; real substrate is LOCAL, Q1-Q4 cut recorded in MANIFEST.md

This deviation downgrades the refusal to a WARN and records the reason — it does not remove
it (`_apply_override` never removes a refusal, by design). Filed as a CANDIDATE for the
integrator's filing wave: `**Shape:**` is ambiguous between substrate-shape and batch-shape,
and a hand-authored contract has no way to know the token is reserved.
