# Surface-Responsibility & Duplicated-Authority Audit — 2026-06-11

<!-- scope: meta -->

> **Read-only, adversarial audit.** Immutable per repo convention (supersede with a new
> dated file; never edit in place). No fixes are applied here — this audit *maps*; the
> follow-on **architect-mode session** takes the map and designs the resolution. Findings
> were verified against live repo state during the session that produced this file; line
> numbers are as of 2026-06-11. **Companion** to `2026-06-11-architecture-coherence-audit.md`
> — same lens (resident-copy drift), a different surface (the *responsibility map*), so this
> references that audit's tickets (#150–#156) rather than re-minting them.

---

## Orientation (read this first)

**What `.dev-knowledge` is.** The ecosystem's methodology brain — Layer 2 of the ADR-28
three-layer model. It absorbs lessons from every `Dev/` repo, universalizes them into enforced
conventions, and audits the ecosystem against them. It is *passive storage + governance
authority*, not an execution engine: protocols, ADRs, handoffs, templates, and **read-only**
validators. Layer 1 = browser chat (architect); Layer 2 = this repo (storage & governance);
Layer 3 = Claude Code in child repos (execution).

**Why this audit exists.** Two operator questions, answered read-only: *(1) does `PLAYBOOK`
still earn its size, and (2) where is authority duplicated across the governance surfaces?* The
repo's **own named failure class is "resident-copy drift"** — two surfaces that *both
authoritatively define* the same fact, which then diverge. This audit maps each surface to its
**one job**, lists the **duplicated authority**, and classifies `PLAYBOOK`'s content against its
proper homes.

**The load-bearing distinction (used throughout).** A single authoritative definition with
*pointers / reinforcement* elsewhere is **healthy** (defense-in-depth). Two places that *both
authoritatively define* the same thing is a **flag** (it drifts). The goal is single-**authority**,
not single-**mention** — a rule may be echoed in ten files and still be healthy if exactly one
of them *defines* it and the rest point.

**Standing posture.** This audit **MAPS**; it does not execute the resolution. The doc carries
the full map (every duplication + every extraction candidate). BACKLOG gets only the *clearly-
actionable, net-new, high-value* tickets (#157, #158); everything whose resolution is itself a
new-authority design decision is **mapped and handed to the architect session**, because
minting it here would pre-empt that design role and add overlap-management against #150–#156.

**How to read each finding.** The plain-language **finding** leads; the `file:line` evidence is
the *proof underneath*, not the headline. Tags: **FLAG** (net-new, ticket it) · **MAP**
(resolution is design → architect session) · **OVERLAP** (already owned by an existing ticket,
reference it) · **HEALTHY** (the model — record, don't touch).

---

## Lens 1 — Responsibility matrix (each surface → its one job)

The surfaces, verified against actual content. The matrix is **descriptive of today's reality**;
whether it should be *promoted to a canonical, authoritative map* — and where that map would
live — is itself a design decision left to the architect session (see MAP-2).

| Surface | Its one job | Verified anchor |
|---|---|---|
| Pre-commit hooks · `audit.py` checks | **ENFORCE** — can't-violate (fail-closed gates) + fail-soft awareness | `.pre-commit-config.yaml`; `scripts/audit.py` `ALL_CHECKS` |
| ADRs | **WHY** — immutable rationale, the source of a binding rule | `docs/decisions/`; e.g. ADR-39 (file lifecycle) |
| `ARCHITECTURE.md` | **STRUCTURE** — the navigation map; *points to* doctrine, never restates it | self-charter at `:10–14` |
| `CLAUDE.md` | **THIS-REPO runtime contract** — the per-repo session contract (≤200 lines) | `:7–13` |
| Skills · commands | **PROCEDURE / ACTOR** — how, on demand; run a workflow | `.claude/commands/*`; `.claude/skills/verify/` |
| `~/.claude/rules` | **GLOBAL invariants** — cross-repo posture (out-of-tree) | `core-invariants.md` (e.g. `--no-ff` #5, OneDrive #1) |
| `ESSENTIALS.md` | **CONDENSED index** — summarize PLAYBOOK + point, never copy | self-charter at `:3–4` |
| `PLAYBOOK.md` | **JUDGMENT / heuristics** — the un-mechanisable reasoning | see Lens 3 |
| Browser (L1) · Claude Code (L3) | **ACTORS** — architect designs / executor acts | ADR-28 |

**One surface already states its job precisely — and mostly keeps it.** `ARCHITECTURE.md:10–14`:
*"Living document — the **navigation map**… it **points** to the ADRs/protocols that hold the
doctrine; it never restates doctrine text (resident-copy drift is the failure class this repo
exists to kill)."* That self-charter is the cleanest single-sentence statement of the
single-authority principle in the repo — which makes its two lapses (MAP-1) legible.

---

## Lens 2 — Duplicated-authority list (the deliverable)

### FLAG-1 — `CLAUDE.md` defines the file-lifecycle rule twice, in one file → **#157**

**Finding.** `CLAUDE.md` states the append-only/immutable file-lifecycle disposition **twice,
authoritatively, in full** — once as a §4 conventions bullet, once as the §5 critical rules.
This is the cleanest, smallest instance of the repo's own failure class: a single file holding
two authoritative copies of one rule. A clean mechanical fix (keep one as authority; make the
other a pointer).

**Evidence.**
- `CLAUDE.md:54` (§4 Conventions, "File lifecycle"): *"Append-only: `LESSONS.md`,
  `logs/TOKEN-LOG.md` (never edit), `JOURNAL.md` (newest-first prepend). Immutable: ADRs,
  transcripts, handoffs, audits (supersede with new file). Living: …"*
- `CLAUDE.md:69–71` (§5 Critical rules #1–3): *"`LESSONS.md` and `logs/TOKEN-LOG.md` are
  append-only — never edit… `JOURNAL.md` is append-only newest-first… ADRs, transcripts,
  handoffs, audits are immutable — supersede…"*

Both are full definitions, not one-points-to-the-other. **Coordination note:** #112 already
plans to edit `CLAUDE.md:71`'s immutability wording (a *different* contradiction — supersede-vs-
never-edit under the adr_amend helper). #157 and #112 both touch §5 and must be sequenced to
avoid a collision; #140 (mechanized doc-rot checker) would catch this whole class.

### MAP-1 — the file-lifecycle rule is authoritatively defined in 4+ places across 3 files → **architect session**

**Finding.** Beyond the intra-`CLAUDE.md` copy, the same disposition is authoritatively restated
across `CLAUDE.md`, `ARCHITECTURE.md` (itself **twice**), and `PLAYBOOK` — all sourced to ADR-39.
**Which surface should be the single authority, and which should become pointers, is a
new-authority design decision** (ADR-39 is the rationale source; the structural table is
arguably ARCHITECTURE's legitimate job; the contract restatement is arguably CLAUDE's). That
trade-off is the architect session's to make, not a mechanical fix — so this is mapped, not
ticketed.

**Evidence (the same rule, five authoritative statements).**
- `CLAUDE.md:54` and `CLAUDE.md:69–71` (FLAG-1 above) — two.
- `ARCHITECTURE.md:137–140` (Ch1 Invariants #4 *"Append-only files are never edited"* + #5
  *"Dated artifacts are immutable"*) — three.
- `ARCHITECTURE.md:378–383` (Ch5 "File lifecycle" table — Append-only / Append-only newest-first
  / Immutable / Living) — four.
- `PLAYBOOK` §"Documentation file types" + "Order conventions" — five.

**Sub-observation (sharp).** `ARCHITECTURE.md` restates the ADR-39 lifecycle disposition (Ch1
*and* Ch5) despite its own charter at `:10–14` to *"never restate doctrine text."* Whether the
lifecycle disposition counts as "doctrine" (→ pointer to ADR-39) or "structure" (→ ARCHITECTURE
defines it) is exactly the authority question the architect session must settle. Recorded as the
canonical example of how subtle the single-authority line is.

### OVERLAP-1 — "Layer 2 never executes" over-broad restatement → already **#152**

**Finding.** The "Layer 2 never executes" invariant is precisely scoped in the canon but
over-broadly restated in the copies, which the sibling audit already flagged and #152 already
owns (pointerize the copy).

**Evidence.**
- Canon (correct, scoped): `ARCHITECTURE.md:130–131` — *"Layer 2 never executes. **No script
  here orchestrates actions in, or drives state changes in, another repo.**"*
- Over-broad copy: `CLAUDE.md:72` — *"no orchestration scripts; `scripts/` contains read-only
  validators **only**"* (the live `scripts/` runs ~17 audit checks + generators + a 424-test
  suite, and `audit.py run` commits its own output per ADR-80). The PLAYBOOK §System-Architecture
  copy is the larger drift surface.
- **Disposition:** #152 owns the PLAYBOOK pointerization (System-Architecture half landed
  2026-06-11; §8 half deferred to the #150 handoff redesign). `CLAUDE.md:72`'s over-claim folds
  into the same drift class — fix it when #152's family is resolved, not as a separate ticket.

### OVERLAP-2 — `--no-ff` + append-only have no CC-side enforcement → already **#153**

**Finding.** `--no-ff` and append-only ordering are authoritatively defined (healthily, see
HEALTHY-2) but only *prose-enforced* — a fast-forward or an in-place log edit is detectable only
after the fact. This enforcement gap is #153, not a duplication.

**Evidence.** `core-invariants.md` #5 (`--no-ff`) is prose + a `verify:` line, no FF-guard hook;
the `no_ff_merges` audit check shipped 2026-06-11 as detect-and-surface WARN (true prevention
deferred). **Disposition:** #153 owns the remaining mechanization; reference, don't re-mint.

### HEALTHY-1 — `ESSENTIALS.md` summarizes-and-points; it does not duplicate authority (the model)

**Finding.** `ESSENTIALS` is the **counter-example** that makes the flags legible: it
consistently summarizes a rule and then points to its authority, rather than re-defining it.
This matches the sibling audit's recorded counter-finding and should be left exactly as is.

**Evidence.** The "summarize, then `Full: PLAYBOOK §X`" pattern at `ESSENTIALS.md:295`
(Auto-TOC), `:302` (docs/ taxonomy), `:382` (Backlog → *"Full: PLAYBOOK §10"*), `:397`
(lesson→rule → *"see… PLAYBOOK §4"*), `:412` (complexity → *"Full guidance: PLAYBOOK"*). A grep
of ESSENTIALS for `append-only|immutable|never edit|prepend|supersede` returns only a prose
mention and one JOURNAL *procedure* step (`:347`) — **no** authoritative critical-rules block.

**Correction recorded (audit hygiene).** A planning sub-agent confabulated that
`ESSENTIALS.md:69–71` verbatim-duplicate the append-only/immutable rules (matching
`CLAUDE.md:69–71`). Direct verification **refutes** it — those are `CLAUDE.md`'s line numbers;
ESSENTIALS has no such block. The lesson — *verify every candidate duplication at file:line; do
not trust an agent's line numbers* — is captured in `LESSONS.md` and is why every finding above
carries a directly-read anchor.

### HEALTHY-2 — `core-invariants.md` is the sole authority for `branch + merge --no-ff`

**Finding.** `--no-ff` is defined in exactly one place; `CLAUDE.md` only *names the branch
prefixes*, it does not re-define the mandate. Single-authority + pointer = healthy.

**Evidence.** `core-invariants.md:36–41` fully defines the rule + rationale + `verify:` line.
`CLAUDE.md:50` states only *"Branches: `feat/ fix/ docs/ chore/` off `main`"* — the naming
convention, not the `--no-ff` mandate. No duplication.

---

## Lens 3 — `PLAYBOOK` content classification (does it earn its size?)

**Framing (operator-directed).** The percentages and the per-section labels below are the
**auditor's proposed classification with reasoning**, *not* measured fact. "What counts as
genuine judgment" is itself a judgment call the architect session may revisit — so these are
**approximate ranges and a direction of travel**, not metrics to act on literally.

**Proposed shape.** `PLAYBOOK.md` is ~3,284 lines. On the auditor's reading, **roughly a quarter**
is genuine un-mechanisable JUDGMENT that legitimately stays; **the majority** is extractable
(rules a hook already ENFORCES, rationale that is really a DECISION/ADR, STRUCTURE that is
ARCHITECTURE's job, step-by-step PROCEDURE that could be an on-demand skill, or LOCAL runtime
detail); and **a meaningful slice** is pointer overhead. The direction is clear even if the exact
split is arguable: **PLAYBOOK carries substantially more than its irreducible judgment core.**

**PLAYBOOK's irreducible job** — the content that is un-mechanisable, un-recordable as a single
decision, and un-structural; it *stays*:
- Session-boundary heuristics: stop-signs, the decision-fatigue threshold, the recursive-planning
  anti-pattern (`§Session boundaries`).
- The review postures, the Anti-Patterns list, and The 10 Commandments.
- The diagram-form selection algorithm (`§14`); the render-layer discipline for copied output (`§8`).
- The drift-proofing precedence philosophy (source → gate → agent); the LLM↔LLM back-and-forth
  (bilateral, not unilateral, context transfer).
- The shallow-clone false-positive class; the "after 2 failed attempts → /clear" golden rule;
  knowledge-organization migration triggers.

**Extraction candidates (proposed homes).** By dominant type, roughly:
- **ENFORCED → pointer to the hook/ADR:** `§Repo conventions` (ADR-30/34/59/60); the freshness/
  amendment-coherence/codemap/TOC subsections (audit checks are the authority).
- **STRUCTURE → ARCHITECTURE / a taxonomy doc:** the file-type taxonomy; the three-homes model;
  the automation-tier table.
- **PROCEDURE → skill / CLAUDE.md:** the numbered recipes (§1 new project, §9 weekly review, §11
  tool eval); the Council archival mechanics (full lifecycle already in `AI_COUNCIL_PROCESS.md`);
  the BACKLOG grooming ritual.
- **LOCAL / drift-prone → `~/.claude` / CLAUDE.md:** Appendix A (CC shortcuts), Appendix B (model
  routing — `~/.claude/ROUTING.md` is already the source), Appendix C (token techniques).

**Dedup against existing tickets — most of the *specific* extraction work is already owned:**
- **#77** owns the targeted protocols/ consolidation (extract PLAYBOOK §18; reconcile the three
  divergent lesson→rule statements; trim ESSENTIALS to its 1-page contract; strip the PLAYBOOK
  Section-history blocks). Genuinely open (CLOSURE-VOIDED).
- **#140** owns the *mechanized* doc-rot checker (intra-file duplication, file bloat, Section-
  history accumulation, cross-file fidelity drift) — the durable detector for this whole class.
- **Net-new → #158:** the high-confidence pointerizations that #77 does *not* enumerate — chiefly
  `§Repo conventions` → ADR pointers and Appendices A/B/C → `~/.claude`/CLAUDE.md. The deeper
  per-section extraction (procedures → skills) is *mapped here* for the architect session to
  sequence, not pre-committed as tickets.

---

## Self-check / reconciliation (no two findings may both be true and contradict)

- **FLAG-1 vs MAP-1 — same rule, different disposition, not a contradiction.** The intra-
  `CLAUDE.md` copy (FLAG-1) is a *clean mechanical* fix (one file, one rule, two copies → keep
  one, point the other) and is ticketed. The 4-way cross-file spread (MAP-1) requires choosing
  *which surface is the authority* — a design decision — so it is mapped, not ticketed. Both can
  be true: the small fix proceeds; the big authority question waits for design.
- **HEALTHY-1 vs the sub-agent's "ESSENTIALS duplicates" claim.** Reconciled by direct file:line
  verification: ESSENTIALS summarizes-and-points (`:295/:302/:382/:397/:412`); the duplication
  claim was confabulated. Consistent with the sibling audit's Scope-A counter-finding.
- **OVERLAP-1 ("Layer 2 never executes" is over-broad) vs the invariant being intact.** Same
  reconciliation the sibling audit made: the *invariant* (no cross-repo orchestration) is correct
  and current in `ARCHITECTURE.md:130–131`; only the over-broad *restatements* (`CLAUDE.md:72`,
  the PLAYBOOK copy) drift. The canon is right; the copies are stale.
- **Lens-3 percentages vs "do not act on them literally."** No contradiction: the *direction*
  (PLAYBOOK exceeds its judgment core) is the finding; the *exact split* is explicitly the
  auditor's proposal, revisable by the architect session.

---

## Summary — what feeds the architect session

**Flag-now (ticketed this audit):**
- **#157** — collapse the intra-`CLAUDE.md` file-lifecycle restatement (§4:54 ↔ §5:69–71) to one
  authority + a pointer; coordinate with #112 (also edits §5); cross-ref #140.
- **#158** — pointerize the high-confidence PLAYBOOK extractions not owned by #77 (`§Repo
  conventions` → ADRs; Appendices A/B/C → `~/.claude`/CLAUDE.md).

**Map-for-design (no ticket — the architect session owns these as new-authority decisions):**
- The 4-way file-lifecycle authority question (MAP-1): which of ADR-39 / ARCHITECTURE / CLAUDE is
  the single authority, the rest pointers — including whether the lifecycle disposition is
  "doctrine" or "structure."
- Whether the **responsibility matrix (Lens 1)** should be promoted to a canonical surface→job
  map, and where it would live (MAP-2).
- The deeper PLAYBOOK per-section extraction sequencing (procedures → skills) beyond #158's
  high-confidence set.

**Overlap (already owned — reference, do not re-mint):** #152 (PLAYBOOK §System-Architecture /
§8 + the `CLAUDE.md:72` over-claim drift class) · #153 (`--no-ff` / append-only CC-side
enforcement) · #77 (targeted protocols/ consolidation) · #140 (mechanized doc-rot checker).

**Healthy / do-not-touch (the model):** `ESSENTIALS` summarize-and-point derivation;
`core-invariants.md` as the sole `--no-ff` authority; `ARCHITECTURE.md:10–14`'s points-not-
restates self-charter (the principle the whole audit measures against).

**Noted limitation (out of scope here).** The operator's **user-preferences profile is
browser-side** — it is not in this repo and could not be read. Any `profile ↔ repo` overlap
(e.g. working-style rules stated both in the browser profile and in ESSENTIALS/PLAYBOOK) is
flagged as a **browser / architect-session input**, not assessed by this audit.

**Sequencing note.** This audit produces a **map, not a rewrite**. The single-authority
resolution and the PLAYBOOK slimming are incremental pointerizations (the #152 pattern: replace
the copy with a pointer so nothing is left to sync), sequenced by the architect session — *not* a
big-bang PLAYBOOK rewrite. Beware the "nothing until the structure is perfect" treadmill: a
living system's foundation is never *done*.

---

*Audit produced read-only on 2026-06-11. Companion captures: 1 LESSONS entry (2026-06-11) and
BACKLOG #157–#158. No source files were modified by this audit.*
