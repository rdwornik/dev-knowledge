# NB4-D — the equilibrium audit: every browser-seat ACT of this window, classified

- **Class:** verification (ADR-101 enum) · **Date:** 2026-08-16
- **Source-session:** cloud lane `nb4-D`, read-only, branch `claude/nb4-equilibrium-audit-el1o0w`
  (the operator brief names `claude/nb4-equilibrium`; the harness provisioned the suffixed form —
  recorded, not silently reconciled). HEAD at start `d137cc6` (`main` @ the phase-2 Position-0 merge).
- **Status:** **DRAFT — PROPOSAL-ONLY.** No BACKLOG row is born, closed or edited; no register entry
  is written; no contract, template, script or gate is created. Every mechanization below is a
  sketch for the architect to rule on, not applied work.
- **Model:** claude-opus-5
- **Inherited-vs-measured:** the act inventory (§2) is **reconstructed** from committed artifacts
  named per row — JOURNAL entries, `docs/audits/` contracts/manifests/packets, the active handoff
  bundle, `protocols/STANDING_RULINGS.md`. The duplication arithmetic (§3), the boilerplate md5
  identity across all seven phase-1 contracts, the `preflight_contract` non-use, the audit-class
  admission of this file's own name, and the register/detector scope reads are **MEASURED live this
  run** against the tree at `d137cc6`. The off-repo packs (`PHASE2-MAX-PACK.md`,
  `MORNING-ADJUDICATION-2026-08-15.md`, `W4-WAVE2-INPUT.md`, `PHASE1-REVIEW-PACKET.md`,
  `CLEANUP-AND-NIGHT-BATCH-3.md`) are **UNVERIFIABLE from this clone** — they live in the operator's
  Downloads and are cited here only as the in-repo record cites them.

---

## §0 · The question, the frame, and what counts as an ACT

**Operator North Star (verbatim from the brief):** *the browser architect should only make
architectural decisions and emit contracts; everything mechanical should be repo-side.*

The frame already exists in-repo and this audit is measured against it, not against a fresh
opinion: **ADR-87** (*Architect↔CC equilibrium contract — conditional intent-only prompting*,
Accepted 2026-06-18) §Decision item 2 already assigns the division of labour —

> **The architect emits:** *intent* · *closure* · *anti-patterns* · the **plan/auto mode** · a
> **thin per-task governance-context pointer**.
> **CC owns:** *code-impact context* · *generic gotchas* · the prompt **skeleton** (PLAYBOOK §2 —
> now CC's consumption-spec, not the architect's authoring burden) · *model/effort*.

So the North Star is not a new policy; it is ADR-87's contract, and this audit asks a narrower,
checkable question: **in the 2026-08-14 → 2026-08-16 window, which browser-seat acts fell outside
what ADR-87 assigns to the architect, and of those, which have a repo-side home already?**

**Window boundary, derived not assumed.** A window is a batch (`gen_handoff.assert_batch_boundary`
refuses to cut a bundle while a batch is open —
`docs/audits/2026-08-16-technical-batch-6-manifest.md`, §"One standing consequence"). This window
opens with the bundle cut `2026-08-14-dev-knowledge-architect` (`JOURNAL.md` 2026-08-14 (e)/(f)),
spans batch 5 open→closed and batch 6 open, and is still open at the time of writing. Newest
handoff bundle by git add-date = `docs/handoffs/2026-08-14-dev-knowledge-architect`
(2026-08-14 19:21:01 +0200) — the `audit.py::_select_active_bundle` predicate CLAUDE.md §1 item 3
names, re-derived live.

**Definition of an ACT, held constant:** *one discrete thing the browser seat produced or decided
that left a trace in this window's committed record.* Grain is deliberately coarse enough that a
40-item ruling block is one act at the block level and its individual verdicts are counted inside
it, and fine enough that "author a contract" and "decide the merge order" are not merged.

**The three classes, defined before use:**

| Class | Test |
|---|---|
| **JUDGMENT** | The act consumes information no repo file holds (operator intent, off-repo context, a value trade-off), or it *selects* among options rather than deriving them. ADR-87 assigns it to the architect. Stays. |
| **MECHANIZABLE** | The act's output is fully determined by repo state plus a rule that could be written down. A script or a committed fragment could produce it. No such organ exists today. |
| **ALREADY-MECHANIZED-BUT-BYPASSED** | An organ that produces this output **exists in the tree** and was not used for this act. Sub-labelled `(used)` where the organ exists and *was* used — those are counted, but they are not findings. |

**One decomposition rule, and it is load-bearing.** An adjudication is not one act. It is three:
**(a) derive the option set and its evidence**, **(b) pick**, **(c) transcribe the pick into a
durable surface**. ADR-87 assigns only (b) to the architect. Collapsing the three is exactly how a
judgment seat acquires mechanical load, so this audit splits them everywhere they occur.

---

## §1 · What the record shows, in one paragraph

The browser seat ran four adjudication events (morning-adjudication `D1.1–D1.7` / `D5.1–D5.3`;
phase-1 integration `R1–R7`; the night-3 decision queue `D1–D14`; phase-2 `§A1–§A10`), emitted
seven phase-1 lane contracts and twelve phase-2 lane contracts, authored five off-repo packs, set
two merge-queue orders, and gave (or withheld) a small number of GO words. **The picking half is
almost entirely judgment and belongs where it is.** The derivation half is already repo-side for
exactly one of the four events — night-3, where a lane pre-computed 14 decisions with evidence and
labelled 5 of them batch-ratifiable — and hand-carried for the other three. The transcription half
is hand-carried everywhere. And two organs that would have caught this window's two most expensive
mechanical failures were in the tree, unused.

---

## §2 · The act inventory

### Family A — boot (4 acts)

| # | Act | Evidence | Class |
|---|---|---|---|
| A1 | Paste the assembled bundle into a fresh chat; emit the on-load acknowledgment | `docs/handoffs/2026-08-14-dev-knowledge-architect/HANDOFF_BOOT.md` "What the operator does" steps 2–3 | **ALREADY-MECHANIZED (used)** — `scripts/assemble_paste.py` builds `PASTE_THIS.md`; residual act is a copy-paste |
| A2 | Ask CC for `/handoff-verify`; paste the ONE evidence block | same file, step 5; `HANDOFF_PROCESS.md` §5 v6 one-round-trip | **ALREADY-MECHANIZED (used)** — the whole gate is one CC-side run |
| A3 | The §13(d) operator-context beat (narrowed to *"anything changed since the supplement was written?"*) | same file, step 6; `SUPPLEMENT.md` is FILLED | **JUDGMENT** — off-repo context exists nowhere in the tree by construction |
| A4 | Read `RESIDUAL.md` §1 drift-flags → §4 frontier → §2 shipped map | same file, step 7 | **ALREADY-MECHANIZED (used)** — `gen_handoff.py` + `PROBES.md` P4/P6/P7/P9 re-derive every value; the bundle deliberately states none |

Family A is healthy. The v6 boot is the one surface in this window where the mechanical half is
already fully repo-side, and the residual acts are reading and one operator question.

### Family B — adjudication (12 acts, covering 41 individual rulings)

Four events, decomposed by the (a)/(b)/(c) rule.

| # | Act | Evidence | Class |
|---|---|---|---|
| B1 | **Morning adjudication 2026-08-15 — derive** the option set + host-verification projection | `JOURNAL.md` 2026-08-15 (a): step 0 produced *"exactly the 41-WARN projection with zero hard-fail organs"* | **MECHANIZABLE** — the projection is a live `audit.py health` read; it was authored into the pack ex-ante and then confirmed by CC |
| B2 | **— pick** `D1.1–D1.7`, `D5.1–D5.3` (10 rulings) | `D1.1` at `JOURNAL.md` 2026-08-15 (a); `D1.3` at `CLAUDE.md` §12 v2.59; `D1.7` at `JOURNAL.md` 2026-08-16 (b); `D5.3` verbatim in `docs/audits/2026-08-15-technical-527-block-main-lane-contract.md:2` | **JUDGMENT** |
| B3 | **— transcribe** into the §B twelve-act boot contract | `JOURNAL.md` 2026-08-15 (a) *"executed §B of the operator's `MORNING-ADJUDICATION-2026-08-15.md` … twelve ruled acts"* | **MECHANIZABLE** |
| B4 | **Phase-1 integration — derive** the merge-blocking condition set | `JOURNAL.md` 2026-08-15 (b): the manifest absence, `open_batches(.) → []` | **ALREADY-MECHANIZED (used)** — `batch_manifest.open_batches` |
| B5 | **— pick** `R1–R7` | `JOURNAL.md` 2026-08-15 (c) *"Executed the phase-1 integration per architect rulings R1–R7"* | **JUDGMENT** |
| B6 | **— transcribe** R1–R7 into the integration arc | same entry; `tasks/528-*.md` carries *"INTEGRATION 2026-08-15 (R7)"* verbatim in the row body | **MECHANIZABLE** |
| B7 | **Night-3 queue — derive** 14 decisions, each with evidence, conflict flags and a batch-ratifiable label | `docs/audits/2026-08-15-technical-night3-decision-queue.md` — closing line *"Decisions queued 14, batch-ratifiable 5, stale drafts 0"* | **ALREADY-MECHANIZED (used)** — a night lane did this repo-side; **the model case** |
| B8 | **— pick** `D1–D14` | the queue's own §8 *"Everything here is a proposal"*; outcomes visible at `JOURNAL.md` 2026-08-16 (a)/(b) | **JUDGMENT** — and materially cheaper: the queue's HTML comment records 5 of 14 ratifiable with one word, 9 needing an individual word |
| B9 | **— transcribe** the picks into the phase-2 pack | `docs/audits/2026-08-16-technical-batch-6-manifest.md` §Authority | **MECHANIZABLE** |
| B10 | **Phase-2 — derive** the §B step list and §C lane decomposition | batch-6 manifest §Authority: *"rulings §A1–§A10 of 2026-08-16, issued on `PHASE2-MAX-PACK.md`"* | **MECHANIZABLE** (partly — see §3.1) |
| B11 | **— pick** `§A1–§A10` (10 rulings) | `§A3`/`§A4`/`§A6` cited at `JOURNAL.md` 2026-08-16 (b) and `CLAUDE.md` §12 v2.61 | **JUDGMENT** |
| B12 | **— transcribe** into `PHASE2-MAX-PACK.md` §A/§B/§C/§D | batch-6 manifest §Authority + §Closure contract clause 3 (the §D wrap items) | **MECHANIZABLE** |

**A finding this decomposition surfaces, which no single artifact states.** The window ran **four
distinct ruling namespaces** — `D1.x`/`D5.x`, `R1–R7`, `§A1–§A10` — plus a **second, colliding
`D`-series** in the night-3 queue (`D1–D14`), whose `D5` (*"close out the Issue backlog"*) is a
different object from the morning adjudication's `D5.3` (*"copy upstream `no-commit-to-branch`'s
`git symbolic-ref HEAD` predicate"*, quoted in CONTRACT O). Both were live on 2026-08-15. Nothing in
the tree distinguishes them; a reader resolves the collision by date-and-context or not at all.

### Family C — contract emission (9 acts)

*(C1 is a header row naming the artifact set; the acts inside it are C2 and C3, so C1 is **not counted**
in §3.)*

| # | Act | Evidence | Class |
|---|---|---|---|
| C1 | *(header)* the **7 phase-1 lane contracts** (M N O P Q R S) | the seven `docs/audits/2026-08-15-technical-*-lane-contract.md` files, 29,208 bytes total | *not counted — see C2/C3* |
| C2 | Author the **per-lane judgment head** — Purpose · OWNED-FILES class · UNDERSTAND · Steps — for every contract this window (phase-1 and phase-2 alike) | 9–11 lines per contract (measured) | **JUDGMENT** |
| C3 | Author the **"Common law (all phase-1 contracts)" block**, once per contract | **17 lines / 2,014 bytes, md5 `ab56434a232166ff692819f4be1ff89e`, byte-identical in 7 of 7 contracts** (measured live); same block re-carried ×12 in phase-2 | **MECHANIZABLE** |
| C4 | Emit the **12 phase-2 lane contracts** (`CONTRACT-W2A…G`, `L8`, `L9`, `H1`, `H2`, `H3`) **without running the available locator verifier** | batch-6 manifest lane roster, "Contract of record" column; zero `preflight` runs recorded (§2-BYPASS-2) | **ALREADY-MECHANIZED-BUT-BYPASSED** — the judgment head of these 12 is counted at C2, the boilerplate at C3; what is counted *here* is the un-run verification |
| C5 | Compose each lane's **branch/worktree name** | roster column "Branch (to be provisioned)" ×12 | **ALREADY-MECHANIZED-BUT-BYPASSED** — `validate_branch_naming.LANE_BRANCH_RE` is the single definition (`batch_manifest.py:134` imports it); `/lane-boot` §1 already runs it. See §2-BYPASS-1 |
| C6 | Assign **rows → lanes** and **bucket labels** (feature/satellite · finish-line · hub-introspection) | roster columns "Rows"/"Bucket" | **JUDGMENT** |
| C7 | Set the **process-lane cap** declaration ex-ante | manifest §"Process-lane cap" — 3 of a permitted ⌊12/4⌋ = 3 | **MECHANIZABLE** — floor arithmetic over the roster plus the I-D10 three-way split |
| C8 | Set the **merge-queue order** (batch 5 `S→Q→R→N→M→P→O` per R4; batch 6 `a b c e f g d h i l x y` per §D) | `JOURNAL.md` 2026-08-15 (c); manifest §Closure contract clause 1 | **JUDGMENT** — footprint-collision ordering has a mechanical input but the tie-breaks are risk judgments |
| C9 | Run the **12×12 OWNED-FILES collision matrix** | `JOURNAL.md` 2026-08-16 (b) **Next:** *"run the 12×12 OWNED-FILES collision matrix"* | **MECHANIZABLE** — a set-intersection over declared footprints; no organ exists |

### Family D — off-repo pack authoring (5 acts)

| # | Act | Evidence | Class |
|---|---|---|---|
| D1 | `MORNING-ADJUDICATION-2026-08-15.md` (§B, twelve ruled acts + step 0 host verification) | `JOURNAL.md` 2026-08-15 (a) | **MECHANIZABLE (transcription half)** |
| D2 | `PHASE2-MAX-PACK.md` (§A rulings, §B steps 1–7, §C twelve contracts, §D merge order + wrap items) | batch-6 manifest §Authority; `JOURNAL.md` 2026-08-16 (b) | **MECHANIZABLE (transcription half)** |
| D3 | `CLEANUP-AND-NIGHT-BATCH-3.md` §0b (the night-2 landing shape) | `JOURNAL.md` 2026-08-15 (d) *"Executed the architect ruling of 2026-08-15 (§0b of …)"* | **MECHANIZABLE (transcription half)** |
| D4 | `W4-WAVE2-INPUT.md` (operator-side wave-2 input) | active bundle `HANDOFF_BOOT.md` Purpose row | **JUDGMENT** — operator-authored input, not a derivation |
| D5 | `PHASE1-REVIEW-PACKET.md` | cited in the window record | **MECHANIZABLE (assembly half)** — the packet shape is fixed by ADR-110 |

**Honest limit on Family D:** none of these five files is in this clone. They are classified from
what the in-repo record says they contained, and a classification of a file I cannot read is weaker
evidence than everything else in this table. Flagged rather than smoothed.

### Family E — operator-word gates (4 acts)

| # | Act | Evidence | Class |
|---|---|---|---|
| E1 | The pending GO words: wave-2 width GO · telemetry v1 lane GO · `[#528]` GO · single-flight GO-or-park | active bundle `HANDOFF_BOOT.md` Destination write-scope; `SUPPLEMENT.md` §7 | **JUDGMENT** |
| E2 | Withhold the word for **lane k** (`[#293]` cross-repo seeding) | batch-6 manifest §Protocol: *"operator-word-gated and no word was given — so it is absent from this roster rather than silently carried"* | **JUDGMENT** — and correctly recorded as a withholding, not an omission |
| E3 | Authorize teardown only after the push + per-branch blob proof | `JOURNAL.md` 2026-08-15 (d) **Next**; manifest §Closure contract clause 5 | **JUDGMENT** on the trigger; the proof itself is mechanical and already scripted per-branch |
| E4 | Leave **`#371`** explicitly un-ruled | manifest §Closure contract clause 3, *"the explicit `#371` left un-ruled` line"*; the night-3 sessionplan §4 item 1 gives the reason (`#387` has not landed) | **JUDGMENT** — an explicit non-ruling is a ruling |

### The two BYPASS findings, stated separately because they are the expensive ones

**§2-BYPASS-1 — `/lane-boot` step 1 / `validate_branch_naming.py`.**
`.claude/commands/lane-boot.md` §1 runs
`uv run --locked python scripts/validate_branch_naming.py --lane lane-<letter>-<id>-<slug>`
**before provisioning anything**. Batch 5 dispatched two lanes whose names that regex refuses —
`worktree-lane-s-w20-draft-landing` (`w20` where `\d+` is required) and
`worktree-lane-r-gateclose-drain8` (no id slot) — and the failure surfaced at the integrator's first
merge, where it would have wedged the queue (`JOURNAL.md` 2026-08-15 (b), *"S is merge #1 under the
R4 order"*). It was resolved by hand-anchoring both tips in a JOURNAL `Anchors:` line. `batch_manifest.py`'s own
honest-limits block names the mechanism: *"a batch lane dispatched straight through
`claude --worktree <name>` never passes `/lane-boot` step 1."* **Third occurrence of the class** —
batch 4 hit it and dropped two lanes; batch 5 hit it and hand-anchored. Batch 6 reached
`refused: 0`, but by a **hand-run of the regex at manifest-authoring time** (manifest §"THE
OFF-GRAMMAR HAZARD…", §B step 9), which the manifest itself is careful to call *"a checked roster,
not a gated one"*.

**§2-BYPASS-2 — `/preflight` / `scripts/preflight_contract.py`.**
The tool exists precisely for this act class — its docstring opens *"Nine architect premise errors
landed in the 2026-08-03/04 window, every one caught downstream by accident"* — and it extracts and
resolves `file:line`, heading, sha and `[#id]` claims from a contract. **It was run against zero of
this window's 19 contracts.** Measured: `grep -rn preflight docs/audits/2026-08-1[4-6]*.md` returns
nine hits, every one of them either the unrelated `preflight_backlog_ids` check, a code-quality-scan
row, or a test-file name — no run, no evidence block, no citation. `JOURNAL.md` lines 1–470 (the
whole window) contain no `preflight` mention at all. The cost is not hypothetical: CONTRACT N cites
`protocols/PLAYBOOK.md` Ch5 L815–825 and L1793 and `ESSENTIALS.md` L78–86, and its lane had to
spend a whole step-0b derivation (`docs/audits/2026-08-15-technical-528-legs12-manifest.md` §1)
establishing what the contract's candidate class actually resolved to. The tool is **adoption-first
and wired into no gate by design** — its own docstring says so — so this is a non-adoption, not a
violation. It is still the second-largest mechanical load the seat carried unaided.

---

## §3 · Counts

| Class | Acts | Which |
|---|---|---|
| **JUDGMENT** | **13** | A3 · B2 · B5 · B8 · B11 · C2 · C6 · C8 · D4 · E1 · E2 · E3 · E4 |
| **MECHANIZABLE** | **13** | B1 · B3 · B6 · B9 · B10 · B12 · C3 · C7 · C9 · D1 · D2 · D3 · D5 |
| **ALREADY-MECHANIZED-BUT-BYPASSED** | **2** | C5 (`validate_branch_naming` / `/lane-boot` §1) · C4 (`preflight_contract` / `/preflight`) |
| *(ALREADY-MECHANIZED and used — counted, not a finding)* | *5* | *A1 · A2 · A4 · B4 · B7* |
| **Total acts inventoried** | **33** | 13 + 13 + 2 + 5 |

*Count note, so the arithmetic is checkable rather than asserted.* Family sizes: A = 4, B = 12,
C = 8 (C1 is a header row and is not counted), D = 5, E = 4 → **33**. Every act appears in **exactly
one** class list above and every class list is disjoint; the four lists sum to 33. Where an act has
both a judgment and a mechanical half (contract emission), the halves are separated into distinct
numbered acts — C2 carries the judgment head for all 19 contracts, C3 the boilerplate — rather than
double-counted.

**The measured duplication, since it is the single hardest number here:**

```
common-law block          17 lines / 2,014 bytes
identical in              7 of 7 phase-1 contracts   (md5 ab56434a232166ff692819f4be1ff89e)
boilerplate total         14,098 bytes
all-contract total        29,208 bytes
boilerplate share         48.3%
per-contract judgment     9-11 lines out of 26-28
phase-2 exposure          the same block x 12 lanes = ~24 KB
```

---

## §4 · Top 3 mechanizations, library-first

All three respect two standing constraints, stated up front so they are visible in every sketch:

1. **ADR-62 alternative 2 — "Fully automated mechanical generation … Rejected as aspirational"**
   (`docs/decisions/ADR-62-v4-handoff-process-ratification.md:119`). That rejection is about
   handoff generation, and its reasoning generalizes exactly: the v4.3 review found the
   "generated from source" claim was *hybrid in practice*, and v4.3 sharpened it to *"ephemeral
   per-handoff generation + per-generation verification, accepting synthesis-time imperfection."*
   **Nothing below proposes a template engine, and nothing below generates judgment content.** The
   shape that survives the rejection is **assembly with hand-authored FILL-IN regions** — the model
   `scripts/gen_handoff.py` already ships and ADR-82 ratified, whose 15 FILL-IN regions are the
   living proof that the boundary is drawable and holds. ADR-56's companion rejection
   (*"Move authority to Claude Code — rejected: unevidenced architectural change; browser chat is
   where operator intent is shaped"*, `docs/decisions/ADR-56-prompt-generation-card.md:85`) draws the same line
   from the other side, and none of these three moves authority.
2. **ADR-112's two-tier adoption bar** — Tier S tries and keeps or deletes; Tier L evaluates on
   measurement. All three below are Tier L (they ship into `scripts/`), so each names its bar.
   *(Incidental, reported not fixed: `ADR-112`'s status line reads Accepted while its in-body
   "Status note" still says Proposed — an ADR-94 in-place ratification that left the note stale.
   Out of this audit's scope.)*

### M1 — `scripts/gen_lane_contract.py`: **assemble** a contract; `--check` gates it *(the pick)*

**What it does.** Emits a lane contract from four inputs, three of them derived:

| Part | Source | Authored by |
|---|---|---|
| Common-law block | `templates/lane-common-law.md`, committed once | nobody — copied byte-identical |
| Header (id, title, priority, size, `serialize-group`) | `tasks/<id>-*.md` frontmatter via `yaml.safe_load` | derived |
| `worktree`/branch name | computed, then asserted against `validate_branch_naming.LANE_BRANCH_RE` | derived + gated |
| Purpose · OWNED-FILES · UNDERSTAND · Steps | **`<!-- FILL-IN:… -->` regions, hand-authored** | the architect |

**Library-first, honestly.** Stdlib only, plus two libraries this repo has already ADOPTED with
recorded rulings — `yaml.safe_load` for frontmatter (register `STANDING_RULINGS.md` **N-2**) and
`markdown_it` for fence/region parsing (**N-1**). **No Jinja2, no new dependency, no template
engine**: string assembly of four parts is not a templating problem, and reaching for an engine here
is precisely what ADR-62 alternative 2 refused. The `--emit-source` / `--check` duality is the
`gen_task_tree.py` shape already in the tree.

**The `--check` leg is where the leverage is, and it subsumes both BYPASS findings.** As a
pre-commit hook on any added `docs/audits/*-lane-contract.md` — the file class register **I-D3**
already requires committed before dispatch — it does three things no organ does today:

- **regen-and-diff the common-law block** against the committed fragment (the exact shape of
  `roster-freshness`, `claude-rosters-freshness`, `audit-index-freshness`, `organ-index-freshness`);
- **run `validate_branch_naming.LANE_BRANCH_RE`** over the contract's declared worktree name — which
  arms §2-BYPASS-1 **at the manifest/contract side**, complementing `[#531]`'s provisioning-side gate
  rather than duplicating it. Two sides, one regex, one definition;
- **run `preflight_contract.py`** over the contract's locator claims — which arms §2-BYPASS-2 at the
  moment the contract enters the tree, with no change to `preflight_contract` itself and no new
  authority. Its own PASS semantics carry over verbatim: *"A PASS here means 'every locator
  resolves', never 'the contract is correct'."*

**Payoff, measured:** 14,098 bytes of byte-identical text stop being authored for phase-1's width,
~24 KB for phase-2's; the per-contract authoring surface drops to the 9–11 judgment lines ADR-87
assigns to the architect. **Tier L bar:** ADOPT if a contract emitted through it is byte-equal to a
hand-authored one on its judgment regions AND the `--check` leg catches a seeded off-grammar name
and a seeded dead locator (RED-first, the repo's standing proof shape). REJECT if the FILL-IN
regions start absorbing derived content — that is the ADR-62 failure recurring, and it is the one
thing to watch.

**What it must not do, stated as a refusal:** it must never author Purpose, Steps, OWNED-FILES or
UNDERSTAND. A generator that guesses a lane's steps is the "hybrid in practice" defect ADR-62 named,
wearing a new costume.

### M2 — `scripts/check_rulings_register.py`: **validator first**, emitter deferred

**The problem, measured.** 41 rulings this window across four namespaces plus a colliding second
`D`-series (§2, Family B). The register's own **Editing note** already states three shape
obligations — declarative phrasing (the `silent_rule_ratchet` corpus), an `Expiry` bullet or an
explicit `PERMANENT per [#NNN] R3` citation (entry **A2**), and the `landed:` predicate block shape
(`[#513]`/W3). Today all three are enforced by *an agent reading carefully* — the control register
entry **I-D9** itself calls *"the control that does not scale"*.

**Sketch.** Read `protocols/STANDING_RULINGS.md` with `markdown_it` (N-1, adopted). For every `###`
entry under a lettered section assert: (i) the id matches its section's grammar; (ii) an `Expiry`
bullet exists **or** a `PERMANENT per [#…]` citation does; (iii) ids are unique **across
namespaces**, which is the collision this window produced; (iv) delegate the declarative-phrasing
check to `silent_rule_detector` by import — never reimplement it, the `journal_anchor.py` precedent
(one predicate shared by `block_unanchored_push` and the audit backstop, so the organs cannot drift).

**Why the emitter is deferred and not built.** A `--emit` that turns a YAML ruling block into the
register's markdown is easy and is **the wrong first move**: the paste format's cost is not typing
it, it is *getting it wrong silently*, and a writer with no validator just writes wrong entries
faster. Ship the validator, run it adoption-first exactly as `/preflight` was shipped, and let the
n=2 evidence decide the writer. That sequencing is also what register **I-D9** ruled for the
adjacent `kill-candidates:` refusal check — deferred behind ADR-111's own n=2 clause — so this is
the standing precedent, not a new caution.

**Tier L bar:** ADOPT if it reproduces, RED-first, the four defects the record already documents
(the A2 citation misattribution corrected 2026-08-06, the O-2 supersession, the I-D7 retirement
line, and this window's `D5` namespace collision). REJECT if it can only find defects that were
already found by hand.

### M3 — `scripts/pending_words.py`: the GO-package checklist, **computed, never answered**

**Evaluated honestly, and this is the weakest of the three — it is ranked third on merit, not
listed for completeness.** The GO package is real (four pending words at `SUPPLEMENT.md` §7 /
`HANDOFF_BOOT.md` Destination write-scope; lane k's withheld word at the batch-6 manifest), but the
*list* is short and the *assembly* is already half-mechanized: `gen_handoff.py` writes the supplement
with the §7 region, and CC fills it. So the honest scope is narrow: **compute the list of things
currently blocked on an operator word, from the tree, instead of remembering them.**

**Sketch.** Derive three sets and print their union with locators: (i) `tasks/*.md` bodies carrying
an operator-word-gated clause (a small, checkable phrase set — *"operator-word-gated"*,
*"awaiting a word"*, *"GO-or-park"* — matched declaratively, never a `must|shall|never` token, since
`tasks/` is outside the ratchet corpus but the phrasing discipline is cheap to keep); (ii) lanes
**defined but not dispatched** in the open manifest, via `batch_manifest.open_batches` + the roster
table (lane k is the live instance); (iii) `docs/intake/*.md` with `status: DRAFT` past their
declared decision date. Stdlib + `yaml.safe_load`. Read-only, Layer-2 clean (ADR-28/36).

**What it explicitly does not do:** it never proposes a verdict, never ranks, never defaults.
`window_metrics.py` already models the honest posture — it prints `NOT COMPUTED` with a reason for
the two of six metrics that are judgment inputs rather than observations, *because a
computed-looking number here would launder an estimate into a measurement*. A GO list that suggested
its own answers would be that failure.

**Tier L bar:** ADOPT if it reproduces this window's four §7 words plus lane k **from the tree
alone**, with zero hand-seeded input. REJECT if it needs a curated phrase list longer than it saves —
at which point the list *is* the checklist and the tool is ceremony.

### Candidates evaluated and NOT ranked

- **Merge-queue ordering (C8).** Footprint-disjointness is computable; the tie-breaks are risk
  judgments (which lane's failure poisons the most downstream work). ADR-87 assigns that class to
  the architect. A tool could *propose* an order — but a proposal a seat must audit anyway is not
  obviously cheaper than the decision. **Not ranked; genuinely borderline.**
- **The 12×12 collision matrix (C9).** Real, mechanical, and a clean set-intersection over declared
  OWNED-FILES — but the declarations are *prose classes* in six of seven phase-1 contracts
  (*"the Python call sites that invoke pytest for gate purposes"*), not path lists, and lane N's
  step-0b derivation exists precisely because of that. A matrix tool needs machine-readable
  footprints first, which is M1's header block. **Deliberately sequenced behind M1, not dropped** —
  it is M1's natural second leg.
- **Process-lane cap arithmetic (C7).** ⌊width/4⌋ against the I-D10 three-way split is trivially
  computable and the bucket *label* is the judgment. Too small to rank alone; belongs inside M1's
  `--check` as one assertion over the roster.

---

## §5 · `[#412]` prompt-distillation measurement — **DESIGN ONLY, not started**

**Gate status, stated precisely because the brief asks for the design and forbids the leg.** The
frozen roadmap scopes this *"after batch-4 closes"*
(`docs/audits/2026-08-12-technical-roadmap-north-star-frozen.md:26`, the *Prompt/command/skill
distiller* row). **Batch 4 has closed** (`docs/audits/2026-08-14-technical-batch-4-true-close-packet.md`),
so the roadmap gate is *discharged* — but the night-3 sessionplan §4 item 2 independently rules the
leg **out of the current window** (*"a next-window headliner, not a rider"*), and the roadmap §6
anti-goals name `[#412]` as an owned scope with **no re-derivation**. In batch 6, `#412` rides lane
**g** as a Done-when *conversion* row (`#271 #324 #391 #412 #491`), which is not this leg.
**Nothing below is started, and the design deliberately re-derives none of `[#412]`'s owned scope**
— it designs only the *measurement*, which the row's own Done-when leaves open.

**What the row actually asks for** (`tasks/412-*.md`, read live): three halves — (a) research
Anthropic's published organ set + fleet adoption; (b) a routing doctrine for fan-out / workflow /
subagent; (c) configured self-orchestrated fan-out for the night batch. Done-when: *"the research is
captured … AND a routing doctrine covering configured fan-out is recorded, or recorded
deferred-with-reason"*. **The row's Done-when contains no measurement clause.** So this design is
the answer to *"what would make the doctrine evidence-based rather than asserted"* — an input to
the leg, not a substitute for it, and if the architect prefers the doctrine be recorded
`deferred-with-reason` this design is the reason.

**The library-first move, and it is the whole point: the instrument already exists.**
`scripts/telemetry_emit.py` is landed (`[#529]`, Stage 1 of the 2026-08-14 telemetry memo) — three
event types, one append-only SQLite table in WAL mode, `emit_event()`. Its own docstring states the
constraint that makes this design cheap and honest: *"it wires nothing … A grep for `telemetry_emit`
outside this file and its test is expected to return nothing today."* **So the measurement needs no
new store, no new dependency, and no new organ family — it needs call sites.** That is already an
owed phase-3 step with a named CALL SURFACE section. Building a second measurement family here would
be exactly the *"no orchestration machinery where CC-native covers"* anti-goal (roadmap §6).

**The design, four parts.**

**(1) The unit of measurement — a *dispatch*, not a session.** One row per dispatched lane, keyed by
the branch name (which `LANE_BRANCH_RE` already makes unique and parseable into letter/id/slug).
The batch manifest already declares the roster ex-ante, so the denominator is known before any data
exists — which is the property that stops the measurement being reconstructed from survivors.

**(2) Three fields, and no more, because each has a named source that exists today.**

| Field | Source | Status today |
|---|---|---|
| `t_start` | the contract's own *"T_start: first line of your packet records dispatch timestamp"* clause — already in the common-law block of all 7 phase-1 contracts | **already collected, unaggregated** |
| `t_end` / lane wall-clock | the lane's final commit timestamp | derivable from git, no instrumentation |
| `prompt_bytes` | the committed contract file's size (I-D3 requires it committed) | derivable from git, no instrumentation |

The night-3 sessionplan §4 item 8 independently proposes exactly this cheap route and names its
payoff: *"one `T_start` line per lane, which converts the whole latency row from UNVERIFIABLE to
derivable at essentially zero cost."* This design adopts that proposal rather than competing with it.

**(3) The measurement question, stated as a falsifiable hypothesis before any data is taken.**
*Does reducing a contract's authored byte-count (via M1's assembly) change lane outcome?* Outcome is
the tuple already recorded in every packet: deviations self-reported · STOP-and-report escalations ·
targeted-test verdict. **Pre-registered prediction: no effect on outcome, a reduction in authoring
cost.** Recording the prediction before the data is what separates this from a post-hoc
rationalization of M1, and if the prediction fails, M1 is the thing that is wrong.

**(4) The honest limit, and it is severe enough to state before anyone runs it.** n is tiny — 7
phase-1 lanes, 12 phase-2 lanes, and a contract's byte-count is confounded with its task's
difficulty. **This design yields a descriptive series, not a controlled comparison, and must be
reported as one.** `window_metrics.py`'s posture is the standard to hold: print the gap rather than
a number that looks measured. A distillation ratio computed over 19 heterogeneous lanes would be
exactly the "easy-metric trap" ADR-62 alternative 4 already refused once
(`ADR-62…:127`, the pure-mechanical promotion criterion, restated as judgment-augmented).

**What this design does NOT propose:** no new dependency; no `repomix` (rejected on measurement,
`tasks/467-*.md`, and *"Closing does NOT re-open repomix for paste distillation: that half is
rejected on measurement"*); no re-derivation of `[#412]`'s owned research scope; and no start.

---

## §6 · Honest limits of this audit

1. **Five off-repo packs are classified from the record, not read** (§2 Family D). That is the
   weakest evidence in this report and every row carrying it says so.
2. **The act grain is a choice.** A finer grain inflates MECHANIZABLE (boilerplate decomposes
   further than judgment does); a coarser one hides the (a)/(b)/(c) split that is this audit's main
   analytic move. The rule is stated in §0 and applied uniformly; a different rule yields different
   counts, and the *ratio* is more robust than the absolute numbers.
3. **"Bypassed" is a claim about absence**, and absence is the hardest thing to prove from a
   record. Both BYPASS findings rest on greps returning nothing across the window's JOURNAL range
   and its 31 added `docs/audits/` files; a run that left no trace anywhere would be invisible here.
4. **No mechanization below M1 was prototyped.** Every payoff figure for M1 is measured from the
   tree (bytes, md5, line counts); every payoff figure for M2 and M3 is an argument.
5. **This audit does not adjudicate.** It proposes; the architect rules. Consistent with the
   night-3 decision-queue precedent (`§8`, *"Everything here is a proposal"*), which is the shape
   this window showed works.
6. **This report was run through `/preflight` — and it earned its keep on the first pass**, which is
   the §2-BYPASS-2 argument demonstrating itself rather than asserting itself. The run flagged
   `2` of `7` extracted locator claims. One was a **real defect**: `ADR-56-…:85` was cited as a bare
   filename with no `docs/decisions/` path, i.e. a locator that resolves for a reader who already
   knows where it lives and for nobody else — **fixed before commit**. The other is a **tool false
   positive, left standing and reported**: the 32-hex-char md5 digest in §3 is extracted as a `sha`
   claim and correctly not found in the object store, because it is not a git object. That is a
   real limit of the `sha` extractor (its docstring already records the adjacent
   `if sha.isdigit(): continue` carve-out for pure-digit tokens); a hex digest of non-git origin is
   the same class and is not carved out. **Reported here, not fixed** — this lane is read-only and
   widening a live extractor from an audit is exactly the out-of-scope edit this repo files rather
   than sweeps in.
7. **The gate stack did NOT run on this commit, and that is a container fact, not a bypass.** This
   is a shallow cloud clone (29 grafts, 281 commits reachable, history begins mid-window), `uv sync`
   refuses (`Required uv version ==0.11.19` vs a running `0.8.17`), `pre_commit` and `click` are
   absent, and `.git/hooks/` carries **only `.sample` files** — so `audit.py health` and the
   pre-commit stack could not be executed here and **no `--no-verify` or `SKIP=` was used or needed,
   because nothing was armed to bypass.** What *did* run and pass: `validate_hermetization --staged`
   (exit 0), `gen_audit_index.py --write` (536 → 537, +1 exactly, staged before regen per the
   tracked-files-only ordering gotcha at `JOURNAL.md` 2026-08-15 (d)), the ADR-101 filename
   admission (`validate_hermetization.classify` → `None`), and `preflight_contract` (item 6). Every
   §3 measurement is a live read of file contents, which a shallow clone does not affect; nothing in
   this report depends on history older than the graft boundary. **The full gate stack is owed at
   integration on the operator's clone** — the same disclosure the night-2 and night-3 lanes made,
   and the reason their tree-content numbers stayed usable.

---

## AMENDMENT 1 — 2026-08-16, post-commit: the container gaps are `[#453]`, witnessed a third time

*(In-file amendment marker per `CLAUDE.md` §5 rule 3 — this file is immutable, so the addition is
marked rather than woven into §6. Nothing above this line is edited.)*

§6 item 7 records the container limits as bare facts. They are not novel: they are **`[#453]`**
(*Cloud night-run runbook — the container gaps that silently degrade an unattended session*, P2/M,
open, `serialize-group: environment`), and two of its three enumerated gaps reproduced here exactly.

| `[#453]` gap, as the row states it | This container | Verdict |
|---|---|---|
| (1) *"the container arrived a **SHALLOW CLONE**, grafted mid-window"* | 29 grafts, 281 commits reachable | **REPRODUCED** |
| (2) *"shipped uv 0.8.17 against the ADR-106 `==0.11.19` pin and `uv self update` could not reach the pinned version"* | `uv --version` → **0.8.17**; pin at `pyproject.toml:25` | **REPRODUCED, verbatim** |
| (3) *"`audit-health` exits 1 on `repos registered (none)` … forcing a recorded `--no-verify`"* | not reachable — `click` absent, so `audit.py` cannot start | **UNTESTED here** |

Gap (2) first recorded **2026-07-31**; witnessed again in this window's night-2/night-3 cloud lanes
(each disclosed its `health: DEGRADED` as a graft artifact); witnessed here **2026-08-16**. The
row's own Done-when names the fix — *"a session preflight performs the unshallow and asserts the
`uv` pin with a test"* — and it is unbuilt.

**Three deliberate non-actions, since each is a rule this repo already carries.** The pin is **not
bumped**: `pyproject.toml:17-25` states *"A uv upgrade is its OWN gated change — bump this pin and
regenerate `uv.lock` in a dedicated reviewed commit, never incidentally mid-arc"*, and this is a
read-only lane mid-arc. `uv self update` is **not attempted**: the row already records that it
cannot reach the pinned version, so re-running it buys a second data point on a settled question at
the cost of mutating the environment under a live audit. And **no row is born** — `[#453]` owns this
class, its `kill-candidates:` line already reads *"none — no open task owns cloud-container
preflight"*, so a birth here would be the duplicate the filing-backpressure gate exists to refuse.

**Scope limit, stated so this is not read wider than it is.** This is evidence about the **cloud
container image**, not about batch 6. The twelve batch-6 lanes are `claude --bg` worktree sessions
on the operator's own machine (batch-6 manifest, §"This is the first manifest committed BEFORE its
lanes run"; `/lane-boot` §2), where the pinned `uv` is presumably present. **Nothing here predicts a
batch-6 lane failure**, and the contracts' *"17/19 prior lane reds were this miss"* line refers to a
skipped `uv sync`, not to an unsatisfiable pin. What it does predict is that **any cloud-dispatched
lane on this image fails `uv sync --locked` at step 0** — which is the runbook gap `[#453]` is open
against.

---

## AMENDMENT 2 — 2026-08-16: `uv self update` re-tested LIVE; Amendment 1's basis was stale

*(Second in-file amendment marker, same rule. Amendment 1 is **not edited** — it is corrected here,
which is this repo's standing move for a claim that has since been overtaken.)*

Amendment 1 declined to run `uv self update` on the grounds that *"the row already records that it
cannot reach the pinned version."* **That basis was stale and is now replaced by a live test.**
`[#453]`'s record dates to **2026-07-31**, and uv 0.11.19 has landed in the repo's own pin since —
so "it could not be reached two weeks ago" was not evidence about today. Re-tested this session:

```
$ uv self update 0.11.19
info: Checking for updates...
error: The version 0.11.19 was not found for the app uv in workspace uv
```

**The conclusion is unchanged — the workaround still does not exist — but the reason is sharper than
the row records, and the sharpening is the point.** `[#453]` gap (2) says only that
`uv self update` *"could not reach the pinned version"*, which reads as an update-mechanism failure.
The live error says something narrower and more actionable: the update mechanism works and reports
correctly; **0.11.19 is absent from this container's uv distribution channel.** Those imply different
fixes — the first suggests retry or a different invocation, the second says no invocation of
`uv self update` will ever succeed on this image and the preflight `[#453]` owes must either assert
the pin and **fail fast with a named reason**, or obtain uv from a source other than its own updater.

**Still no row born and still no pin bumped** — both non-actions from Amendment 1 stand on their own
reasoning, which this test does not touch. What changed is only that the third non-action
("`uv self update` is NOT attempted") is now "attempted, and here is what it returned."

**One further limit accepted rather than papered over.** With uv unusable, `audit.py health` and the
pre-commit stack remain un-runnable here (`click` and `pre_commit` absent). Installing them by
another route was considered and **declined**: on a 29-graft shallow clone with no sibling repos,
`audit.py health` returns DEGRADED for reasons that are clone artifacts — precisely what the
night-2/night-3 lanes each disclosed — so the run would produce a verdict needing more explanation
than it carries. §6 item 7's honest "could not run, owed at integration" is a better record than a
DEGRADED that has to be argued away.

---

**JUDGMENT 13 · MECHANIZABLE 13 · ALREADY-MECHANIZED-BUT-BYPASSED 2 (+5 already-mechanized and used, of 33 acts); the single highest-leverage mechanization is M1 — `gen_lane_contract.py` as assembly-not-generation with a `--check` pre-commit leg — because it moves the measured 48.3% mechanical half of contract emission repo-side while leaving every judgment region hand-authored, and its check leg arms both bypassed organs (`validate_branch_naming`, `preflight_contract`) instead of creating a third.**
