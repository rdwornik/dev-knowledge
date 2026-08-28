# FM-WAVE2-CONTRACTS-2026-08-28 — the FUNNEL-MACHINE batch (auto-boots after wave-1 integration)

Binding clauses on EVERY lane (operator appendix): **A1** state is first-class — every governed
object carries explicit state + dated transitions; all health numbers are TIME-SERIES on the
existing telemetry-store pattern (append-only records, derived views; NO second store). **A5**
trust contract — every claim carries a witness; the packet reports the ex-ante numbers verbatim.
Terra pre-merge on every mutating lane, tally-in-body. RED-first everywhere: a gate that never
fired is not proven. Library-first named per lane. Alias standing: "Gemini" (operator speech) =
**agy**; the retired Gemini-CLI registry entry stays retired.

## FM-C — CLOUD read-only, dispatched in WAVE 1 (this section IS the brief file)
FULL FUNNEL CENSUS. Zero writes/deletes/commits; no gate runs (uv 0.8.17 vs pin — gate-dependent
claims marked MEASUREMENT-OWED-LOCAL). ONE self-contained artifact.
Scope: every file under docs/intake/, docs/decisions/, docs/audits/ (the conformance HTML
dashboard enters like any artifact) + BOTH directions: every OPEN tasks/ row's source: resolves.
Classify EVERY object with a resolving evidence locator: CONSUMED-BY <ids> /
CONSUMED-AND-ARCHIVABLE (all consumers terminal) / ORPHAN (no consumer AND no rejection record) /
PROTECTED (cite the retention or ruling). Carry each object's status + dated transitions where
derivable (frontmatter, git dates). Output: (1) headline counts per directory per class —
the BEFORE numbers; (2) the ARCHIVAL WORKLIST, decision-ready; (3) the ORPHAN LIST, both
directions; (4) UNCLASSIFIED — must be 0, each exception explained. Do not propose deleting the
codex/ precedence-layer file. Ex-ante: 100% classified, every claim locatored; a census routing
most objects to ORPHAN without evidence has not censused — say so of your own output.

## FM-1 — the lifecycle written ONCE (doctrine) — M
Write-scope: PLAYBOOK section if post-N3 ratchet headroom allows; else the ONE justified new
protocols/ file, operator-authorized by the mandate (measure headroom FIRST — witness the count).
Collision note: starts only after N3 merges (wave-1 step 4). Content: the state machine —
states, allowed transitions, terminal conditions, who archives what and when, the session's two
standing jobs — citing ADR-98/111/100/70 as the sources unified, superseding nothing silently;
the N-days READY threshold ruled here (FM-2 reads it). A1: this machine is the TEMPLATE for all
governed objects, stated as such. Ex-ante: two seats could run one funnel pass from this text
alone and produce identical transitions.

## FM-2 — check_funnel_lifecycle, the reaper's teeth — M
Write-scope: new check module + registration (audit.py) + tests. Collision note: after N6
merges. Extends existing organs (funnel_coverage, intake_tree_coherence, [#595]) — never a
rival. FAIL-class: (a) intake ACCEPTED, all rows terminal, not archived -> FAIL; (b) ADR
superseded/rejected, not archived -> FAIL; (c) post-cutoff row whose source does not resolve ->
FAIL; (d) intake READY beyond FM-1's N days, no ruling -> WARN. Z-G4 holds: cannot-compute ->
FAIL, never skip. Ex-ante: RED-first against live main reproducing FM-C's findings (that is the
proof of teeth), plus a seeded-violation test that FAILs then passes.

## FM-3 — the visible shrinkage (execution) — M — runs AFTER FM-2 merges
Write-scope: docs/intake/, docs/decisions/, the ruled archive destinations, tasks/ row-body
pointers via N4's landed mechanism. **STALENESS GUARD (self-review fix): FM-C's census is a
snapshot of the origin clone at dispatch time, and wave-1 merges land AFTER it. Before relocating
ANY item, re-verify its classification against the LIVE merged tree (consumers still terminal, no
new consumer born tonight); an item failing re-verification is SKIPPED and reported, never
relocated on the census's word alone.** Then execute the worklist under the NEW gate: archive
every re-verified consumed intake and superseded ADR per FM-1's rules — byte-identical relocation
on the ADR-29 precedent, md5 per object, ZERO deletion, ZERO content edits. Ex-ante: docs/intake
and docs/decisions counts DROP — exact before/after in the packet; check_funnel_lifecycle GREEN
on main afterwards; every relocation md5-proven; skipped items listed with reasons.

## FM-4 — the boot surface — S/M — parallel with FM-3
Write-scope: the handoff assembler module + tests (FIRST ACT: locate it and witness the path —
do not assume a filename; the N8 validator will check this contract). gen_handoff emits a
generated FUNNEL HEALTH block in every bundle: intakes consumed-unarchived / ADRs unexecuted /
orphans both directions / rows closed this window + value evidence attached — numbers only, no
verdicts, no shas (anti-bluff intact), sourced from the same derivations FM-2 uses (one truth).
Ex-ante: the next assembled bundle carries the block; a golden test pins its shape.

## FM-5 — the value half, scoped honest — S — parallel with FM-3
Write-scope: audit.py runner reuse (a `governance-health` command) + close-packet parsing +
tests. Renders FM-4's numbers on demand + a per-closed-row "what it bought" line sourced from
close packets; A1: emits into the telemetry store so trends exist. Telemetry intake #50 stays
its own arc — do NOT absorb it. Ex-ante: the command runs on merged main and its numbers equal
FM-4's block byte-for-byte for the shared fields.

## FPG-1 — the file-purpose graph, first slice (A3) — M
Write-scope: new query module + tests; reads doc-code-edge.yaml, the audits index, [#595]
citations, tasks/ depends-on, the deploy manifest — unified into ONE queryable graph. This IS
the named consumer ruling R-A reserved: **rustworkx** (per R-A: "if a consumer is ever named,
the library is rustworkx, not networkx"). **DEPENDENCY DISCIPLINE (self-review fix): adding
rustworkx is a dependency change and is never incidental (ADR-106) — its authorization is the
operator's A3 mandate verbatim ("a real graph library, not more hand-rolled traversal"); declare
it through the ruled dependency path, cite the mandate in the commit.** FIRST ACT: verify the two
facts R-A left open. Half one is now externally witnessed: rustworkx publishes prebuilt PyPI
wheels for 32/64-bit Windows and its CI covers Python 3.10–3.14 incl. Windows (rustworkx.org
install docs + project CI matrix, checked 2026-08-28 by the architect) — re-confirm locally.
Half two stays MEASUREMENT-OWED-LOCAL: installability under the pinned uv 0.11.19. On failure,
fall back to R-A's measured sqlite/stdlib edges with a swap-ready seam, and record the measured
divergence (library-first discipline both directions). Deliverable: `why <path>` answering purpose + consumers + edges
for governed surfaces, FAILING on unknown files (a file nothing explains is a defect, not a
mystery). Phase: new-files-first; FM-2 gains the predicate in a later batch, not tonight.
Ex-ante: `why` answers correctly on 3 named governed files (witnessed transcripts) and FAILs
on a planted unknown.

## DB-1 — the dashboard successor (A2) — M — after FM-4
Write-scope: new render module + tests; INPUT = telemetry/history data only. The conformance
HTML dashboard is censused by FM-C like any artifact (zero consumers -> orphan -> FM-3 archives
it). Replacement: ONE analyst-grade surface rendering TRENDS — open rows, banked ledger,
commit-gate wall-time, doc-rot findings, funnel orphans, paste bytes, suite time — as charts
over window history, regenerated, never hand-written. Library-first: pick an established
charting library by measured fit; record divergence if anything is hand-rolled. Ex-ante
(operator's acceptance verbatim): DIRECTION visible in one glance; zero colored-table markdown;
regenerable from the store with one command.

## A4-AGY — staff the big-context analysis role — M/L
Write-scope: docs/audits/ artifacts + the benchmark item files per the persisted SDA-1
discipline; NO routing-table change (that is the architect's ruling on the evidence). Measured
acceptance for **agy** FIRST, per R3/A4: seeded-defect items for the ANALYSIS role, one of which
IS the operator's use case — a whole-repo holistic scan (cross-file coherence, orphan spotting,
doc-vs-code drift) — judged against the named incumbent baseline in-window, never vibes. SDA-1
constraints bind: **TRANSPORT PRECONDITION (self-review fix): batch-1's preflight left WHICH
transport is alive as a hub-side record, not this contract's memory — re-verify agy's transport
end-to-end FIRST; if it is dead, STOP this lane, record the operator act owed, do not improvise
an alternate route at night.** Q2 served-id preflight next (agy's envelope is untrusted — a cap
at INDETERMINATE is a legitimate, recorded outcome per C-9, chosen deliberately, not discovered);
Φ_analysis defined in writing before the run; EXHAUSTED is a third outcome; floors without an
in-window incumbent print UNCALIBRATED. Kimi/GLM/DeepSeek follow the same gate AFTER transports
are repaired (operator acts — not tonight). grok stays pay-per-call point-use per registry.
Ex-ante: a computed-gates cell (agy, analysis) exists with every SDA-1 discipline token present;
the whole-repo-scan item's ground truth cross-checks at least one FM-C finding (two instruments,
one reality — agreement or a named discrepancy).

## SEQUENCING (CC executes; collisions pre-ruled)
FM-C: wave 1 (cloud, running). Wave 2 start: FM-1 ∥ FPG-1 ∥ A4-AGY ∥ FM-4 ∥ FM-5 (disjoint) →
FM-2 (after N6 in main) → FM-3 (after FM-2) ∥ DB-1 (after FM-4). Two integrator passes if the
queue exceeds capacity. All merges serialized, B1 teardown, generated surfaces regenerated once
per integrator pass. The morning packet's asset balance consumes: FM-C counts (VISIBLE), FM-3
deltas (SMALLER), FM-2/FM-4/FPG-1/A4 states (UNBLOCKED).
