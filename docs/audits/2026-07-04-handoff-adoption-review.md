# Handoff process — adoption & quality review (Fable audit)

<!-- scope: meta -->

- **Date:** 2026-07-04
- **Author:** CC (Fable, Mythos-tier, architect role), read-only, isolated worktree `fable-handoff-review`
- **Type:** audit (analysis only — NO implementation; routing to architect/operator/Council)
- **Scope:** HANDOFF_PROCESS **v5.3** end-to-end — spec, boot contract, probe machinery, supplement
  fill/fold, assembler, teeth validator, `/handoff` command, the ~20 live v5 bundles
  (2026-06-11 → 2026-07-03), the JOURNAL handoff arc, BACKLOG #26/#159/#161/#162/#164/#234.
- **Relation to prior work:** builds ON the 2026-06-23 handoff-process audit (whose 8-item rework
  landed 2026-06-24/25) — this assesses post-rework state + the adoption/verifiability axes that
  audit did not cover. The 2026-07-04 architecture review touched handoffs only at RF-5/RF-8 depth.
- **Verified against live files** (not a summary): `protocols/HANDOFF_PROCESS.md` (v5.3),
  `protocols/HANDOFF_BOOT.md`, `docs/handoffs/README.md`, `.claude/commands/handoff.md`,
  `scripts/assemble_paste.py`, `scripts/verify_handoff_probes.py`, `scripts/audit.py`,
  `templates/handoff/v5/SUPPLEMENT.md.tmpl`, the live `2026-07-03-dev-knowledge-architect` bundle
  (all five files), the 06-23 audit, BACKLOG, LESSONS, JOURNAL handoff entries.

---

## 0. Verdict in one paragraph

The handoff process is the single most-exercised organ in the repo — ~20 v5 bundles in 22 days,
near-daily architect handoffs, the supplement fill→fold lifecycle run 12 of 15 times, three
operator-adjudicated supplement-vs-residual divergences resolved cleanly, and one demonstrated
end-to-end strategic carry (the 2026-07-02 enforcement-transfer P0 entered via a filled `SUPPLEMENT`
and was EXECUTED by the next window). It is also the organ where the methodology's own standards are
most visibly eroding under load: the anti-bluff probe contract — the innovation that justified v5 —
has been quietly inverted (every recent bundle ships its probes' answers as `expected:` hints; §5
says such probes are "rejected"), the generator that would hold the bundle shape is still unbuilt
(#164) while every bundle is hand-copied from its predecessor (which is exactly HOW the erosion
propagated), and the entire browser-side half of the contract is prose the repo structurally cannot
witness — #159 remains open after 12 filled supplements because its done-when is unobservable from
inside the repo. The process WORKS — but it works the way v4 worked: by operator discipline
compensating for unmechanized spec, which is the failure mode v5 was written to kill. CC-side
adoption: strong and verifiable. Browser-side adoption: unverifiable by construction. Spec-vs-practice
fidelity: degrading, unguarded.

**The pattern, stated once:** every handoff property with a mechanical guard held; every property
held by prose eroded. The repo's own thesis, demonstrated on its own handoff organ.

---

## 1. What is genuinely working (credit where evidenced)

- **Exercised, not shelfware.** 15 architect bundles 06-12→07-03 (near-daily), plus the first
  cross-repo v5 bundle (`2026-07-02-ai-council-architect`). Supplements: **12 of 15 FILLED**; the 3
  empty are 2 pre-v5.2 bundles (06-15/06-16, before the fillable file existed) + 1 genuine cold
  handoff (06-21). A real operator-side fill discipline, not a decaying ritual.
- **The supplement carries load the repo cannot.** The 07-02 fill delivered a CC-verified
  browser-side finding (5 hub enforcement organs ABSENT across all 4 consumers) that SUPERSEDED the
  repo-derived frontier and re-scoped the P0 (JOURNAL 07-02, `99d97c2`); the 07-03 window then
  executed it. "Held by mechanism, not memory" demonstrably crossed a session boundary here.
- **Divergence adjudication works.** Supplement-vs-residual priority conflicts surfaced and were
  operator-ruled three times (ai-council `0b61b6e`; dev-knowledge `9dbea9a`; the 07-02 MAJOR
  re-scope) — v5 §9 bidirectional adjudication functioning as designed.
- **Self-correction loop is fast.** The 06-23 audit's agenda (C5 stale text, A1 role residence, #200,
  A3/C3 opening reorder, A2 acceptance contracts, A4 gate-map, C1/C4/C6, C2→v5.3) landed within
  2 days, each with confirm-live discipline; C1/C4/C6's removal premise was verified-REFUTED rather
  than executed blind — the verify-don't-assert culture held under a deletion prompt.
- **Structural teeth exist and gate.** `verify_handoff_probes` (#163) is in `ALL_CHECKS`, FAIL-class,
  gates `/ship`; when the first cross-repo bundle false-FAILed it (07-02), the gap was fixed same-day
  with an 11-test matrix and the honest-partial residue filed (#234).
- **Degrade-loudly is honored in the artifacts.** Cold handoffs commit an EMPTY supplement as a
  defined disposition; the 06-19 bundle headlined its own ship-gate RED rather than hiding it.

---

## 2. Red-flag list (severity-ranked)

### RF-1 [HIGH — doctrinal breach, unguarded regression] — the anti-bluff contract is inverted: probes now ship their answers

**How it is implemented.** HANDOFF_PROCESS §5 condition 2: "the handoff ships the **question +
source-locator + the exact verification command**, and **never the answer**. (A probe that bakes its
answer in is, by construction, bluffable — and is rejected.)" The promotion dogfood (JOURNAL
2026-06-11, #149 gate-3) proved exactly this: "each of the 6 probes attempted from the
artifact/summary alone — **all 6 fail** (every answer kept out of the residual)."

**Evidence of erosion.** `grep -c 'expected'` across bundle `PROBES.md`: 06-11 → 1; 06-16 → 4;
06-18 → 5; 06-20 → 8; 06-25 → 10; 07-03 → 11. The live 07-03 bundle prints, in the bundle itself:
P2 "expected at generation: 28, last name `doc_code_coverage_drift`"; P7 "expected GREEN with `10`
dispositioned WARNs AND NO `[stale]` line"; P8's full answer including "NO `README.md`"; P9's exact
group memberships. **P7 is the sharpest self-contradiction:** v5.3's own §5 consolidation rationale
says the read-back's teeth "rest on the dispositioned-WARN count + any `[stale]` line ... not the
bluffable GREEN/RED verdict" — and the bundle prints precisely those two anti-bluff values. The
PROBES preamble papers over it ("the 'expected at generation' hints below are a **drift reference**
... the pass criterion is 'answered from the live source'") while the same preamble still claims "the
answers ... are deliberately **absent from this whole bundle**." Both sentences cannot be true; they
coexist in every recent bundle.

**Why it regressed unguarded.** The §5 empirical bluff-test is a **promotion** gate — it ran once
(2026-06-11) and is never re-run. `verify_handoff_probes` is structural by frozen contract ("the
'Why' column is checked for PRESENCE ONLY"). No organ — manual or mechanical — re-checks
bluffability post-promotion. On a same-day handoff, where values barely drift, most probes are now
answerable by echoing the bundle — the exact fake-green class the 2026-06-10 lesson named ("a
forced-read whose verification can be bluffed from a summary is fake-green").

**How to improve (pick ONE — the two are honest opposites).** (a) **Ratify the drift-reference
design** — amend §5 to permit generation-time hints under the re-derive rule, retire the "never the
answer / rejected" clause, and accept the teeth moved from *receiver-cannot-know* to
*CC-re-runs-anyway*. (b) **Restore the contract** — strip expected-values from generated `PROBES.md`
(hints can live in the JOURNAL generation entry, which the browser never sees), and add a one-line
rung to `verify_handoff_probes`: a probe row matching `/expected[ :]/` → FAIL (cheap, structural,
within its resolve-only charter). In **both** cases: make the bluff-dogfood **recurring**, not
promotion-only — e.g. at every minor version bump, one probe attempted from the paste alone must fail.

### RF-2 [HIGH — systemic cause] — the v5 generator is still unbuilt (#164); every bundle is hand-copied from its predecessor

**How it is implemented.** `/handoff` (`.claude/commands/handoff.md`) is a "dispatch summary" whose
v5 section is prose; the operative mechanics below it are the complete **SUPERSEDED v4 8-file
generator**, including a "Hard constraints" section ("Eight files, flat, markdown only") that flatly
contradicts the v5 bundle shape — resident in the very file that fires on `/handoff`, behind one
"superseded" banner. #164 (P2/L) has been open since the 06-11 flip; ~20 bundles produced manually
since.

**Witnessed consequences of hand-assembly.** The RF-1 hint creep (each bundle inherits the prior
`PROBES.md` as its template, hints included — imitation propagates deviation monotonically); the
06-25 bundle shipped a P2 command with an env-prefix that false-REDed ship-gate (caught, fixed by
hand); every fill→fold flip requires hand-reconciling cold→FILLED framing across BOOT/PROBES/RESIDUAL
+ P8 (witnessed 06-19, 06-25, 07-02 ×2, 07-03 — a 4-file manual coherence edit per fill, each an
opportunity for the §8 self-contradiction class it exists to prevent); paste growth with no budget
(`PASTE_THIS.md`: 36.5 KB on 06-15 → 59 KB on 07-03; the 06-23 audit flagged 40 KB as a "thin boot"
violation and deferred the tradeoff "to #164" — which never came, so the number grew 50%).

**How to improve.** #164 is no longer a nice-to-have — it is the control surface for RF-1, RF-4, RF-6,
RF-7 simultaneously. Its cheapest useful slice is NOT the full generator: (1) template-source the
per-bundle `PROBES.md` from a canonical probe-core template (also closes #161's hand-assembly half)
so hints/deviations stop inheriting; (2) make `assemble_paste.py` print the paste byte-size with a
`[warn]` threshold; (3) mechanize the cold→FILLED flip (a `--filled` mode that rewrites the four
framing sites deterministically). The v4-prose removal stays gated on corp-monorepo migration
(ADR-83) — that gate is legitimate; the slice above doesn't touch it.

### RF-3 [MEDIUM-HIGH — unverifiable half] — the browser-side contract is structurally unwitnessable, and #159 is unclosable as written

**How it is implemented.** Everything the browser must DO — the boot-ack, P1-before-design, the
§13(d) beat, the run loop, the plan-review 3-form contract, the role-stability self-check, the loop
transition gates — lives in `HANDOFF_BOOT.md` prose. The repo's only visible signal is the ack line,
checked by the operator's eyes. The 06-23 audit named this asymmetry (T1: "state gets teeth; role
gets good intentions"); the remedy delivered (A1/A4) was MORE resident prose, self-described as
"RESIDENCE, not machinery" — and the JOURNAL itself concedes "prose-residence already failed once
(a session self-merged despite the discipline)" (06-24 A1-prose entry).

**Evidence of the unclosable ticket.** #159's done-when — "the incoming §13(d) beat is exercised in a
real architect session with a *filled* supplement" — remains open after 12 filled supplements,
because the exercise happens in a browser chat the repo cannot see. Nothing in JOURNAL ever records
"the incoming beat fired"; only the CC-side fill→fold half is dogfooded (noted in the BACKLOG item
itself).

**How to improve.** (a) State the honest limit in the spec (a §8 note: browser-side steps are
operator-witnessed only; the repo verifies CC-side only) — right now §5's "any FAIL blocks
onboarding" reads as mechanical when it is honor-system. (b) Give the receiving end ONE auditable
artifact: a **boot-transcript echo** — the browser's onboarding output (ack + P1 quotes + probe
PASS/FAIL lines + the beat's answer) pasted back to CC and committed as a dated addendum to the
bundle. That single artifact makes "did a fresh session boot correctly" a checkable fact, closes #159
on evidence, and gives future audits a receiving-side record (today there are zero — this audit could
reconstruct only the CC side, exactly the mandate's suspicion). (c) Re-scope #159's done-when to that
artifact's existence.

### RF-4 [MEDIUM — doctrine contradiction] — CLAUDE.md §5 declares handoffs immutable; the v5 lifecycle requires in-place mutation, and practice follows the lifecycle

**How it is implemented.** CLAUDE.md §5 item 3: "ADRs, transcripts, handoffs, and audits are
**immutable** ... never edit in place," sole exception the ADR status line (ADR-94). Meanwhile
HANDOFF_PROCESS §13 **mandates** post-generation mutation (fill the supplement, re-fold, reconcile
framing), and practice goes further: operator-ruled re-scopes rewrote BOOT Purpose + RESIDUAL §4
headline priorities in place (`0b61b6e`, `9dbea9a` — "a contradictory orientation headline is a
defect, not a §9-reconciliation case"). The PreToolUse immutability guard deliberately EXCLUDES
handoffs (#105: "handoffs/audits REMOVED from scope — sanctioned append / dated-addenda flows"), so
enforcement already matches practice; the doctrine text does not.

**Failure scenario.** A fresh session following CLAUDE.md §5 literally refuses the `supplement filled`
flow (or worse, "supersedes with a new file," forking the bundle). A degraded-context session picks
whichever rule it read last.

**How to improve.** One-line amendment to CLAUDE.md §5.3 scoping handoff immutability to
post-consumption (a bundle is a LIVING artifact from generation until its session boots; immutable
thereafter), naming the §13 lifecycle as the sanctioned writer. Cheap, and it kills a live
self-contradiction in the most-read governance file.

### RF-5 [MEDIUM — teeth reliability] — the run loop is unreliable on the operator's default shell; the workaround is per-bundle folklore

**How it is implemented.** `audit.py checks` crashes mid-listing on cp1252 PowerShell (a `→` in a
docstring); `ship-gate` false-REDs on `handoff_probes` under PowerShell (grep/sed/ls absent →
`[~~] tool absent` WARNs undispositioned) — LESSONS 2026-06-26. The fix is "use git-bash," carried as
a prose note re-copied into every bundle's `PROBES.md` preamble ("Windows note") and re-dodged in
every JOURNAL wrap ("run from git-bash — PowerShell false-RED avoided", 8+ occurrences).

**Why it matters at THIS organ specifically** (beyond the architecture review's RF-5). §5 says "any
FAIL blocks onboarding." A forced-read gate that false-fails on the default shell trains the operator
to discount FAILs — alarm fatigue aimed at the exact mechanism whose credibility the teeth depend on.
The probe commands (grep/sed/ls) are Unix-only by authoring convention, ON a Windows box, in a repo
whose global rules say "PowerShell is default shell."

**How to improve.** Author probe commands shell-neutral (`python -c` / `audit.py` subcommands instead
of grep/sed — the P1 substring check is a 1-line python), or make check-time tooling resolve a
known-absent-on-PowerShell exe to its git-bash invocation. The cp1252 fix is already roadmapped by
the architecture review (its item 4); this is the handoff-side rider.

### RF-6 [MEDIUM — the v4 disease regrowing] — re-narration creep in BOOT/RESIDUAL

**How it is implemented.** §2's contract — the residual carries ONLY what the repo does not encode;
task-state is a pointer (§6); re-narration is "the v4 disease." Live 07-03 bundle: the BOOT Purpose
cell is a ~450-word state narration (SHAs, closed tickets, the ADR list, next-frontier); RESIDUAL §2
recaps the shipped window in detail JOURNAL already encodes (its own header says "the map, not the
narration" — it is narration with pointers attached); the supplement's headline answers are restated
in **four** places (BOOT header banner, BOOT paste-pointer steps, PROBES preamble + P1 gate note,
RESIDUAL preamble + §4 per-question banners). Each fill→fold reconciliation adds a layer. Paste: 59 KB
and growing (RF-2). The architecture review's §3.1 watch item is the same leak from the other side:
"what to change first rides in handoff residuals and the operator's head."

**Honest structural caveat.** The browser is file-less, so pointer-purity can never fully hold for it
— SOME narration is the payload. The defect is not that narration exists; it is that (a) it is
quadruplicated within one bundle, and (b) nothing bounds it (no size budget, no single-source rule
for the supersedes-banner).

**How to improve.** Single-source the supplement-supersedes banner (RESIDUAL preamble owns it; BOOT
and PROBES point); cap the BOOT Purpose cell (it is a session HEADER, not a second residual —
3 sentences + pointer); assembler size-warn (RF-2 item 2); and consider making "priority" a
first-class BACKLOG field so the residual can point instead of carry.

### RF-7 [LOW-MEDIUM — silent-staleness hole] — nothing verifies `PASTE_THIS.md` is current with its sources

**How it is implemented.** `assemble_paste.py` is manually re-run; the runbook says "never
hand-edited; regenerate each handoff." `grep PASTE_THIS|assemble_paste` over `scripts/audit.py`: zero
hits — no check compares the assembled paste to its four sources. A source edited after the last
assembly ships stale silently; the operator pastes it with no signal. Practice re-runs the assembler
at each fill by discipline (witnessed) — the "held by discipline" posture the repo distrusts.

**How to improve.** Trivial check — for the newest bundle, re-run the assembler in-memory and
byte-compare against the committed `PASTE_THIS` (FAIL on mismatch). Fits the existing
`check_handoff_probes` pattern and the Layer-2 read-only charter (assembly is a pure read + string
concat; only the COMPARISON is the check).

### RF-8 [LOW — spec-default vs practice divergence] — execution mode (the spec's DEFAULT) is dead in practice; an undocumented third shape exists

**Evidence.** After 2026-06-15, every browser-facing bundle is architect-mode (15 of 15; last
execution-mode bundle is 06-15). Meanwhile `2026-06-25-dev-knowledge-session-close` is a "lean
handoff" — BOOT + RESIDUAL only, no PROBES/PASTE — improvised for a CC-successor session ("Full v5.3
bundle not built — lean bundle chosen (next session is CC, not browser-architect)", JOURNAL 06-25).
Reasonable call; zero spec backing — §13 defines two modes, both browser-facing.

**Why it matters.** The spec models the wrong population. Real traffic is (a) architect browser
handoffs (dominant), (b) CC→CC continuity (JOURNAL / session-summary / lean bundle — un-specced), and
(c) execution browser handoffs (extinct — CC sessions self-boot from CLAUDE.md §1 + JOURNAL). A
default nobody uses is dead spec weight that #164 would faithfully implement.

**How to improve.** An architect-session decision (fits #162's vocabulary item): either demote
execution mode to a documented-legacy profile and spec the lean CC-successor shape (now n=1
precedent), or record why execution mode must stay default. Do not let #164 build the dead path
unexamined.

### RF-9 [LOW — tracked, coupling noted] — cross-repo probes are honest-partial and the per-repo runbook does not exist outside the hub

**Evidence.** #234 (foreign `.claude/` targets + ambiguous basenames degrade to WARN — accepted
honest-partial, 07-02); the ai-council bundle lives in the hub and its operator flow depends on the
hub's `docs/handoffs/README.md` — per-repo runbook seeding is a #164 deliverable. Both tracked; the
audit's addition is the **coupling**: fleet rollout (#221) multiplies cross-repo bundles, so the
honest-partial WARN class and the runbook gap scale with it. Sequence #234 + the runbook-seeding slice
of #164 before #221, or accept a fleet of WARN-decorated handoffs.

---

## 3. The mandate's questions, answered directly

**Well-adopted end-to-end, or discipline that degrades under load?** Split verdict. CC-side: adopted
and verifiable (generation, probes-bind gate, fill→fold, JOURNAL wrap — witnessed repeatedly).
Operator-side: adopted (12/15 fills, divergences adjudicated) — but load-bearing on one person's
discipline with no redundancy. Browser-side: unknowable — zero receiving-side artifacts exist (RF-3).
The spec-fidelity trend under load is negative where no gate holds it: hints crept (RF-1), paste grew
(RF-2), narration quadruplicated (RF-6). Every property with a mechanical guard held; every property
held by prose eroded.

**Where does it leak?** Ranked: (1) the anti-bluff property — leaked via hand-copied templates, no
standing guard (RF-1); (2) bundle-shape fidelity — the generator gap makes the spec advisory (RF-2);
(3) the browser contract — un-mechanizable as currently framed, but NOT inherently: a boot-transcript
echo is mechanizable and absent (RF-3); (4) the supplement's honesty-dependence — real but
empirically the STRONGEST link, not the weakest (12 high-content fills; the "never trusted over the
repo" safeguard + drift-checks held in the 3 divergence cases); (5) probe-gates verify structure, not
what they claim (bindability ≠ bluff-resistance — RF-1's mechanical face).

**Is the carried-vs-self-loads boundary correct?** Directionally yes — methodology travels as pointer
+ enforcement, task-state as pointer, supplement scoped to non-re-derivable why (the template's hard
scope constraint is honored in the 12 filled instances read). Two boundary defects: re-narration creep
on the carried side (RF-6), and priority/what-first living in residual prose rather than a durable
BACKLOG field (the architecture review's watch item — a carry that should be a self-load).

**Does it PREVENT held-by-memory loss or just document it?** One demonstrated prevention at the
strategic layer: the 07-02 supplement carried a browser-side P0 finding across `/clear` into a window
that executed it. Prevention is UNPROVEN at the receiving edge: whether the incoming architect
actually reboots from the primary sources (vs the 59 KB paste's narration) is exactly the part with no
evidence trail (RF-3). Honest summary: prevention proven CC→CC and operator→CC; asserted-but-
unwitnessed CC→browser.

**Testability — can you prove a fresh session boots correctly?** No. Structure is gated (probes bind,
`/ship` blocks); bluffability is not (RF-1); paste currency is not (RF-7); the boot itself leaves no
artifact (RF-3). Today "booted correctly" = the operator saw an ack line. The boot-transcript echo
(RF-3b) is the single cheapest change that converts the whole receiving end from presence-only to
evidence-bearing.

---

## 4. Suggested routing (decidable — NOT implemented here)

Ordered by leverage; each names a route. No item is implemented in this audit.

1. **RF-1 — decide the anti-bluff contract** (ratify drift-reference OR restore no-answer + add the
   `expected` FAIL rung + a recurring bluff-dogfood). *Architect/Council ruling + spec §5 edit.* The
   highest-stakes item: it is a live breach of the property that justified v5.
2. **RF-3b — the boot-transcript echo** (one receiving-side artifact; closes #159 on evidence).
   *Architect ruling + a §13 addendum-flow + #159 re-scope.*
3. **RF-4 — CLAUDE.md §5.3 handoff-immutability scoping.** *One-line spec edit (operator).*
4. **RF-2 — the #164 cheap slice** (template-source PROBES, assembler size-warn, mechanized
   cold→FILLED flip) — also closes #161's hand-assembly half. *#164 (respect the ADR-83 v4-live
   constraint).*
5. **RF-6 — single-source the supersedes banner + cap the BOOT Purpose cell.** *Spec/template edit.*
6. **RF-5 — shell-neutral probe commands.** *Rider on the architecture review's cp1252 item.*
7. **RF-7 — paste-currency check.** *audit.py leg (Layer-2 read-only).*
8. **RF-8 — spec the real population** (demote execution mode, spec the lean CC-successor shape).
   *Architect ruling (fold into #162) — do BEFORE #164 builds the dead path.*
9. **RF-9 — sequence #234 + runbook-seeding before #221.** *Fleet-rollout sequencing.*

---

## 5. What this audit deliberately did NOT do

- **No ADR, no spec edit, no BACKLOG edit, no code** — analysis only; routing is the architect's call
  (a Fable audit does not self-certify via an ADR — the exact failure the methodology kills).
- **Did not re-litigate the 2026-06-23 audit's settled items** — its rework landed (verified in
  JOURNAL 06-24/25 + live files); findings here are post-rework state.
- **Did not grade the v4/v3 eras** — archived; ADR-83 keeps v4 live for corp-monorepo by design.
- **Did not treat the supplement's advisory-not-teeth stance as a defect** — it is the correct honest
  posture; the defect class is elsewhere (RF-1/RF-3: things CLAIMED to be teeth that aren't).
- **Did not assert state from memory** — every claim is cited to a live `file` / SHA / `grep` count /
  `#id`, re-derived in the worktree.

> **Closure.** The handoff process is adopted, exercised, and self-correcting on its CC-side — and
> unguarded on exactly the three axes it was built to guarantee: bluff-resistance (RF-1), bundle-shape
> fidelity (RF-2), and receiver-boot verifiability (RF-3). These stand as a decidable agenda: one
> contract to re-ratify, one artifact to add, one generator to slice — after which "the handoff holds
> under load" becomes a checkable fact rather than a disciplined hope.
