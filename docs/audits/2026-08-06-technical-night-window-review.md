# Adversarial review of the 2026-08-05 architect window — register locators, the v1.6 ceremony clause, and the three rulings

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-06
- **Source-session:** unattended night batch, Claude Code on the web (cloud sandbox); branch `claude/night-batch-2026-08-06-p59kml`; HEAD `8e2be6a1`
- **Status:** complete (review artifact — findings reported, nothing fixed)
- **Model:** claude-opus-5 orchestrating; Sonnet-class bounded read-only probe lanes

## Environment honesty (read before trusting any number below)

This ran in a **fresh cloud clone, ungated by construction** — `pre-commit` is not
installed here, so every commit on the night branch is gate-unverified. That is acceptable
only because `main` was never touched, nothing was merged, and the morning integrator
re-runs the hooks and the full suite locally before any merge.

Three environment facts materially bound the evidence, and each one produced a false
finding that this review had to chase down and retract:

1. **The clone is SHALLOW.** `git rev-parse --is-shallow-repository` → `true`; `.git/shallow`
   carries 13 boundary commits; 203 commits reachable; earliest reachable commit dated
   2026-08-01. Any SHA older than that is unresolvable here. Scope of the limit, stated
   precisely: it hits `82227f08` / `57ae83a6` (2026-07-08, cited in `ARCHITECTURE.md` Ch6)
   and `3c5e476ba` (2026-06-07, the proposal baseline). It does **not** hit any SHA cited in
   `protocols/STANDING_RULINGS.md` — all of those are dated 2026-08-05 and all resolve.
   An earlier draft of this review asserted the opposite; the probe lane re-derived the
   SHAs directly and overruled it. The corrected position is the one recorded here.
2. **`logs/PROPOSALS-*.md` does not exist in this container.** `ls logs/` returns exactly
   `TOKEN-LOG.md`. The artifacts are gitignored (`.gitignore:26`) and live only on the
   operator's machine — the repo's own words, at
   `docs/audits/2026-08-04-technical-closure-proposal-ranked-sheet.md:35-36`. So the
   62-files / 149-headers / `3c5e476ba`-frozen figures are **not verifiable here**. What
   replaces them is git-tracked corroboration (§4).
3. **The container's `uv` did not satisfy the repo's own pin.** `pyproject.toml:25` sets
   `required-version = "==0.11.19"` (ADR-106); the container shipped 0.8.17, and
   `uv self update 0.11.19` fails ("version not found for the app uv in workspace uv").
   Since **every** hook `entry:` in `.pre-commit-config.yaml` is wrapped in
   `uv run --locked`, nothing in the gate mesh can execute until the pin is satisfied.
   Resolved by installing `uv==0.11.19` from PyPI into a scratchpad venv outside the repo
   tree; `uv sync --locked` then completed clean. This is a first-class B1 requirement, not
   a container quirk — see §5.

## 1. `protocols/STANDING_RULINGS.md` — locator verification, line by line

Every locator in the file (229 lines, landed `90351bd0`) was resolved against live state:
each cited `file:line`, every `[#id]`, every SHA, every section reference. Result:
**two defects, in the same bullet, both in entry A2** — and everything else CONFIRMED.

### The A2 double mislocation — both legs confirmed

The packet's §7 correction is itself correct, and it is a **double** defect, not one.

**Leg 1 — wrong file.** A2's honest-divergence bullet (`STANDING_RULINGS.md:67-71`) reads
"The live register carries one **PERMANENT** entry (`preflight_backlog_ids`)". Its
antecedent "the live register" is `ecosystem/disposition-register.yaml`, named one
sentence earlier at `:64`. That file contains **zero** occurrences of the token
`PERMANENT` — `grep -rn PERMANENT ecosystem/` returns hits only in a sibling file. The
genuinely PERMANENT entry is at `ecosystem/doc-code-edge.yaml:120-127`, inside the
`doc_code_coverage_drift` exemption list:

```
  # [#483] R3 advisory leg. PERMANENT exemption, not a temporary one: it reads BACKLOG row
  # syntax (a `kill-candidates:` field value) against BACKLOG row liveness -- both sides are the
  # same generated artifact, so there is no doc->code rule for an edge to bind.
  - preflight_backlog_ids
```

Two entries below it, the contrast the packet predicted is present: a
`TEMPORARY -- expires with [#499]` exemption. The permanent/temporary distinction is
explicit house doctrine in that file.

**Leg 2 — wrong item.** A2 cites the bundle's "`RESIDUAL.md` frontier item 6". At
`docs/handoffs/2026-08-05-dev-knowledge-architect/RESIDUAL.md:125-129`, §4 item 6 is
about something else entirely — `[#499]`'s false-positive reporting cadence. The correct
locator is unnumbered §1 prose at **`RESIDUAL.md:39-42`**: "…Distinct in kind from
`preflight_backlog_ids`' **PERMANENT** row." — the only place in the bundle joining those
two tokens.

**The aggravating detail.** Two sections later in the same file, **B4** cites frontier
item 6 *correctly*, for the `[#499]` cadence (`STANDING_RULINGS.md:186-188` →
`RESIDUAL.md:125-129`). So the citation format is right and the register contains the
correct use of the same locator; A2 simply points at the wrong item. And the author's own
JOURNAL account of writing the file (`JOURNAL.md:64-67`) states the same divergence
**without** citing frontier item 6 at all — the wrong locator appears to have been
introduced when drafting the register, not inherited from the source.

**The substance survives.** A PERMANENT exemption does exist against a rule reading "every
disposition **or exemption**", so the tension the browser rules on is intact. The
disposition-register row A2 names (`warn-preflight-backlog-ids-310-292`,
`disposition-register.yaml:327-348`) **conforms** to A2's rule: it carries
`review_date: 2026-09-04` and a RETIRE-ON-CLOSE comment at `:335-337`. Wrong file, wrong
line, right tension.

### The hunt for further mislocation of the same class — one minor, pre-existing

**A3** points the canonical-tally-header grammar at "`[#499]` rider R2". `[#499]`'s row
(`BACKLOG.md:58`, `tasks/499-*.md`) labels "rider R2" only for the doc-code-edge exemption
discharge clause, not for the tally grammar. This is **inherited verbatim** from the
ratified `SUPPLEMENT.md:116-118`, so it is not a defect the register introduced — but the
row does not yet unambiguously carry what Q7 says it does. Worth a note for whoever builds
that PLAYBOOK section; not a correction to this file.

### Everything else — CONFIRMED

A1 (both `b8a3c483` and `JOURNAL.md` 2026-08-05 (e)), A4 (`SUPPLEMENT.md:119-121`, `[#488]`
open), A5/A6 (both confirmed *not* landed in LESSONS — negative findings verified by grep),
B1 (`SUPPLEMENT.md:54-56`; `23518240`; the `[#218]` 1820-against-1200 figure), B2 (all four
anchor commits `325bb585` / `9650c172` / `60b237a7` / `62dff902` resolve and carry the
claimed shape; merge `8b6afb2e` confirmed), B3 (`boundary_headers.py` `_glob_matches`
docstring at `:230-259`; PLAYBOOK §11 at `:3442-3454`), B4 (the audit file's verbatim
block; ADR-85's asymmetry at `:13,19`), the header/provenance block, the scope boundary,
the decision-budget quote, and the editing note's ratchet claim — which was verified by
running the detector live: `detector: silent-rule-v4 / files: 57 / count: 441` against
`baseline: 441`.

`[#id]` liveness, all eight resolving and all consistent with how the register uses them:
`#218` deferred · `#310` deferred · `#457` open · `#480` closed · `#483` closed · `#488`
open · `#492` deferred · `#499` deferred.

**§C is UNVERIFIABLE, by design.** Its source
(`SESSION-PLAN-2026-08-05-dev-knowledge-architect.md` v2 §H) is not in the checkout — the
file itself says so ("operator's Downloads, off-repo by design"). The label **NC-A5** does
not appear anywhere in-repo. NC-A1/A2/A3 and NC2 — a related but distinct series — *are*
in-repo at `JOURNAL.md:25-37`. This is worth naming because §C carries the
unverified-premise brake that R-A leans on: the register is currently the **only** in-repo
home for a ruling whose provenance cannot be checked from the repo.

## 2. `templates/prompt-template.md` v1.6 — the ceremony clause contradicts landed doctrine

Four conflicts, three of them hard. The v1.6 diff (`12dbb65a`) touched exactly one file;
the whole FR-7 arc touched three (`JOURNAL.md`, `STANDING_RULINGS.md`,
`prompt-template.md`). **`PLAYBOOK.md` and `HANDOFF_PROCESS.md` were not touched at all** —
and that is the root of every finding here.

**Finding 2.1 — the default mode for multi-step work. HARD CONTRADICTION.**
`prompt-template.md:14` — "The **default lane mode is execution**". `PLAYBOOK.md:2508` —
`plan-then-auto` "is the default for most multi-step prompts". Both name a different value
as the default for the same population.

**Finding 2.2 — Scale-L / L-sized epic stories. HARD CONTRADICTION.**
`prompt-template.md:10` gives Scale L "full ceremony, full template" and `:18-19` reserves
plan-mode for "M/L arcs needing genuine repo-derivation". Against that, three passages
across two files state the default unconditionally:
- `PLAYBOOK.md:659` — "prefer `plan-then-auto` mode… **L-sized epic stories default
  plan-first** (full plan mode, reviewed before execution)"
- `PLAYBOOK.md:1647-1650` — "**L-sized epic stories default plan-first**"
- `HANDOFF_PROCESS.md:704-708` (§14a item 7) — same, and every architect prompt re-declares MODE
For an L-sized item that does *not* need repo-derivation, the two cannot both be followed.
Note v1.5's Scale-L bullet said "plan-mode usually preferred" and the diff **deleted** that
clause rather than replacing it.

**Finding 2.3 — the concurrent-lane ceiling. HARD CONTRADICTION, with a real nuance.**
`prompt-template.md:25-27` — "up to ~10 parallel lanes within reason". `PLAYBOOK.md:1643` —
"**The cap: 2–3 concurrent epic lanes.** The root's review + serial-merge bandwidth is the
deliberate bottleneck — more lanes queue at the gate, they don't add throughput."
The nuance, stated because it changes the fix: PLAYBOOK is scoped to **epic lanes** under
ADR-97 tree orchestration (each with its own chat and a §14a/§14b handoff), while the
template's ~10 is about footprint-disjoint work lanes in one V-1 batch. These may be
different objects. But **neither text distinguishes them**, and PLAYBOOK's stated rationale
(integrator bandwidth) applies to both. So the defect is real either way: at best an
undeclared scope collision on the same words, at worst a flat numeric conflict. Also
relevant: the ~10 figure's justification ("V-1", an integrator ruling) is **not landed
anywhere** — repo-wide grep for `V-1` across `protocols/`, `CLAUDE.md`, `CONTRIBUTING.md`
and `ARCHITECTURE.md` returns nothing, and `STANDING_RULINGS.md` does not carry it either.

**Finding 2.4 — `execution` is an undefined value in a governed enum. TENSION.**
`prompt-template.md:36` lists `execution (default) | plan-then-auto (M/L repo-derivation
only) | auto-accept`. `PLAYBOOK.md:2463,2507-2509` defines the vocabulary as exactly three
values — `auto-accept / plan-then-auto / plan`. No value named `execution` is defined
there. Worse, `execution` is already a defined term in the same corpus for two other
things: a handoff boot-mode (`PLAYBOOK.md:3148`, `gen_handoff.py --mode execution`) and the
*name of the field itself* ("**Execution MODE**", `HANDOFF_PROCESS.md:704`). Whether
template-`execution` means `auto-accept` — and if so why the enum lists both — is
unresolved.

**Finding 2.5 — the window violated PLAYBOOK's own maintenance rule. HARD, and it is the
mechanism behind 2.1–2.4.** `PLAYBOOK.md:2665-2675`, verbatim:

```
**Any change to prompt conventions (model/mode/effort criteria, the summary
table, the mandatory skeleton, hook guidance) updates:**

1. this PLAYBOOK rationale (the live authority), and
2. the point-of-use card wherever it travels — under v5, `templates/prompt-template.md`.

Drift between the two is a process bug — the card is the point-of-use authority,
PLAYBOOK is the maintenance source.
```

v1.6 is squarely "a change to… mode… criteria" by that rule's own definition, so the rule
required a matching `PLAYBOOK.md` edit in the same change. `git show --stat` across all
three FR-7 commits confirms it did not happen. PLAYBOOK names this exact failure "a process
bug."

**Finding 2.6 — the template's backing pointer does not hold.** `prompt-template.md:29-30`
points at `protocols/STANDING_RULINGS.md` for "standing rulings an agent applies without
asking" and cites intake #25 AMENDMENT-b for V-2 and V-3. The register carries the **V-2
decision budget verbatim** (`:26-36`) but **not** V-3's ceremony tiers and **not** the
lane-count ruling. So the three rulings v1.6 enacts are sourced only in a commit message.

**Precedence: UNDECLARED.** v1.6 claims no precedence over PLAYBOOK/HANDOFF_PROCESS.
PLAYBOOK declares itself "the live authority" for rationale and the card "the point-of-use
authority" for consumption, and calls divergence a bug — a *synchronization* contract, not
a tie-breaker. Nothing states which wins when they disagree, and they now disagree.

**Negative findings, checked rather than assumed:** `CONTRIBUTING.md`,
`protocols/DEFINITION_OF_DONE.md`, and this repo's `CLAUDE.md` contain no mention of
plan-mode, ceremony, risk-tiering, Scale S/M/L, or a lane ceiling — no claim to conflict
with. `ESSENTIALS.md` mentions plan mode twice (`:52`, `:116`) but prescribes no default,
so at most a soft tension. `HANDOFF_PROCESS.md` §5's v6 gate is untouched by the clause and
NOT in conflict — it governs bundle verification, a different object.

## 3. Red-team of R-A / R-B / R-C

Steelmanned against the repo, then rebutted. Two of the three are dented in ways that
change a deliverable; none is overturned.

### R-A — "report-only wall = advisory observation organ, mesh unchanged"

**The strongest case against.** The premise "mesh unchanged" is false on the repo's own
text, and it is the premise carrying the conclusion.

1. The organ map's admission criterion is not enforcement. `ARCHITECTURE.md:183-184`: "The
   behavioural inventory: **every enforcement/awareness organ**…". A report-only wall is an
   awareness organ by construction.
2. Non-enforcing organs are already members, explicitly: `boundary_report.py` — "a
   reporter, NOT a gate — deliberately not in `ALL_CHECKS`" (`:245`) — and
   `fleet_analytics.py`, "`main()` always 0; NOT in `ALL_CHECKS`" (`:247`). Advisory is a
   value in the failure-posture column, not an exemption from the map.
3. **B1 introduces a Layer value that does not exist.** The enum is stated at `:193-196` —
   `L0` (global `~/.claude`), `hub`, `plugin`, `pre-commit` — every member client-side. Ch6's
   mesh table (`:720-726`) is the same: In-session / Pre-merge / Nightly (cloud) / Nightly
   (local) / Funnel, where "Nightly (cloud)" is the Claude conformance Routine, not
   GitHub-side CI. A server organ is a **new layer**, and adding a value to the model's own
   type is the plainest reading of "changes the mesh model" — the exact trigger §C R-5 names
   for an ex-ante ADR (`STANDING_RULINGS.md:212-214`).
4. **The precedent is a refutation, and it is about vacuity, not enforcement.**
   `ARCHITECTURE.md:748-749`: the `nightly-conformance-triage` Action "was retired by
   `82227f08` (`.github/` deleted), merged to `main` at `57ae83a6` under [#255], **because a
   PR-triggered organ under a local-merge workflow was vacuous — it never fired.**" So the
   live risk is manufacturing a third organ that is ARMED and tells you nothing — the
   pathology Ch2 built its Status column for (`:214`: "An organ can be ARMED and still tell
   you nothing"), already carried by two live rows: `surface_triage.ps1`
   **ARMED (stale input)** and `block_immutable_edits.py` **ARMED (no-op zone)**.
5. **A server organ has a failure mode the posture vocabulary cannot express.** fail-closed
   / propose-only / fail-soft all presuppose the organ runs. A GitHub-side organ can be
   switched off upstream by the platform, a plan change, or a permissions change. None of
   the three ARMED parentheticals covers "present, correct, and not running because the
   host disabled it" — the ADR-85 §A5 lesson (an organ that can be exhausted cannot carry
   teeth) recurring one layer out.

**Rebuttal, and what survives.** R-A's *conclusion* largely survives; its *stated reason*
does not. "No ADR is needed to arm nothing" is right, and independently anchored: NC-A5
(`STANDING_RULINGS.md:198-200`) already rules a report-only deliverable "is a *different
deliverable* and is named as one." But NC-A5 governs **whether a row may be born**; the ADR
question is **whether the mesh model changed**. R-A answers the second with the first one's
answer, and the register keeps them in different entries (§C bullet 1 vs bullet 6).

The dent is narrow, real, and **changes the deliverable**: B1 cannot land as "just a YAML
file." Minimum honest shape — (i) `on: push`, **not** `pull_request`, which is the [#255]
lesson restated as a requirement; (ii) a Ch2 organ row and a Ch6 mesh row in the same commit
as the workflow, with a Status qualifier honest about upstream disablement; (iii) the
operator decides whether adding a server value to the Layer enum is itself ADR-shaped — a
fork R-A currently forecloses by assumption.

**Assessment: dented on reasoning, not overturned on verdict.** Worth re-ruling the narrow
point only.

### R-B — "[#487] is a broken pipeline + judgment arc, not an engine"

**The strongest case against.** "0 confirms in 62 runs" is evidence about the operator's
usage, not the pipeline's health.

1. The contract the organ was built to was honored exactly. Ch2: "Detect-and-propose only;
   the human gate closes (ADR-70)" (`ARCHITECTURE.md:256`); posture "**propose-only** (never
   mutates BACKLOG)" (`:225`). It detected, it proposed, it never mutated. The stage that did
   not run is `/review-closures` — the human gate. Naming that "a broken pipeline" relabels a
   capacity failure as a code defect, and code repair does not fix it.
2. The frozen window is a **fail-safe, and the code confirms it.** `resolve_window()`
   (`propose_closures.py:329-361`) marks a file pending iff `unchecked & open_ids` is
   non-empty (`:348`), then deliberately re-covers from the **earliest** pending file's
   baseline — "files are date-sorted, so pending[0] is the earliest -> widest safe window"
   (`:350-351`). Advancing past unreviewed proposals is precisely what it refuses to do. Under
   that reading, "unfreeze `since_commit`" is a data-loss change dressed as a repair.

**Rebuttal, and what survives.** R-B survives, and the forensics sharpened rather than
weakened it — but two framings must change.

- **Two legs are genuine code defects that bite even with a perfectly attentive operator.**
  (i) The STRONG detector's miss is real and now measured (§4): the `[#432]` arc's five
  commits are all invisible to it. (ii) A **previously unfiled regex defect** was found in the
  same expression (§4) — narrow, testable, and independent of anyone's review cadence.
- **The correct diagnosis is sharper than "frozen".** The baseline is not stuck by accident,
  and it is not stuck because nobody looked: **one ancient unresolved WEAK id pins the window
  for everything, including STRONG detection.** That points the repair at *separating the
  STRONG and WEAK baselines*, not at "unfreezing a counter." Stated as a freeze, the spec
  asks for the wrong change.
- **One R-B premise is wrong on the code.** The "confirm one: type its `#N`" action has not
  merely gone unexercised — **nothing in the codebase ever writes a checked `- [x]` row.**
  `render()` emits `- [ ]` unconditionally (`propose_closures.py:226,241`); a grep across
  `scripts/`, the plugin scripts and the plugin commands finds no writer. The only real
  confirm signal is BACKLOG-row removal. The checkbox is a convention with no implementation,
  which is a different defect from an unused one — and a cheaper thing to fix or delete.

**Assessment: verdict survives; the ordering, the word "frozen", and the checkbox premise
should change.** This is a substantive dent because it changes what the spec asks for first.

### R-C — "option (iv): diagnosis-home standard"

**The strongest case against.** (iv) institutionalizes the mechanism that produced the
problem and pays for it in a liability nobody monitors.

1. **The cause is a threshold, and (iv) leaves it alone.** `validate_doc_rot.py:56-58` —
   `_BACKLOG_DATED_BLOCKS = 3`, `_BACKLOG_LONG_CHARS = 700`, `_BACKLOG_GROSS_CHARS = 1200`;
   predicate `(dates >= 3 and length > 700) or length > 1200`; **WARN-only, never FAIL** —
   confirmed three ways (module docstring `:38-40` "never gates"; `main()` `:254-263` returns
   0 unconditionally; zero occurrences of `"fail"` in the file, and `check_doc_rot`
   constructs only `warn`/`pass`). [#457] sat at 1197 of 1200; its own census pushed it to
   1949 and the diagnosis was evicted to prose.
2. **The overflow channel is unbounded and its integrity is unguarded.** ADR-100 keeps audits
   "unbounded… never physically moved, rolled up, or compacted", and the directory already
   holds **397** files. And there is **no gate that re-validates a pointer** — independently
   confirmed: the only tool of that class, `scripts/preflight_contract.py`, self-describes as
   "ADOPTION FIRST: this is wired into NO gate" (`:36-38`), is in no `ALL_CHECKS`, no
   pre-commit hook, no Stop hook, and is forward-only by design.
3. **A cheaper option is not on the record.** Exempting a delimited diagnosis region from the
   char count, or tiering the ceiling, is a constants-level change in one file — no new file
   class, no new pointer, no new immutable artifact.

**Rebuttal, and what survives.** (iv) is right that a 1949-char row is unreadable and right
that `docs/audits/` is already the sanctioned genre, so the channel exists whether or not it
is named. The disposition route is **foreclosed by a landed ruling**, so it is not the cheap
alternative it looks like: B1 of the same register (`STANDING_RULINGS.md:112-115`) —
"self-induced bloat is trimmed (dedup), a disposition is reserved for genuine
rule-vs-ruling conflict." That leaves ceiling-change vs (iv) as the real fork.

The addendum's pointer-validation leg already patches (iv)'s worst flaw, which is the tell
that the flaw is real. The correction: make that leg **load-bearing and gated**, not
advisory — without it (iv) inherits the rot it was written to cure.

One factual note on the `[#483]` evidence, reported as a disagreement rather than smoothed:
the probe lane confirmed every underlying fact (no `[#483]` row in `BACKLOG.md`; no `483`
node across `tasks/manifest.json`'s 473 nodes; `tasks/483-*.md` present with
`status: closed`; the ruling doc present) but read the pointer as **resolving cleanly** — a
properly closed-and-archived task rather than a dangling orphan. Both readings share the
facts; they differ on whether "the only live pointer is a retired task file" counts as
orphaned. The design consequence is unaffected, because nothing re-validates the pointer
either way.

**Assessment: survives, conditionally.** Two things belong on the record before it binds —
the pointer-validation leg is load-bearing, and the ceiling-change alternative deserves an
explicit rejection rather than silence.

## 4. Defects found by this review that no row carries

Four, each verified live. None was fixed (day-lane serial jobs).

**4.1 — `CLOSES_RE` matches a non-word and misses the real one. NEW.**
`scripts/propose_closures.py:51`:

```
CLOSES_RE = re.compile(r"\b(?:closes?|closed|fixes?|fixed)\s+\[#(\d+)\]", re.I)
```

`fixes?` parses as `fixe` + optional `s`, so it matches `fixes` and the non-word `fixe`,
but **never bare `fix`**. Executed against the live compiled object:

```
MATCH  'closes [#5]'      MATCH  'fixes [#5]'      MATCH  'fixe [#5]'
MATCH  'close [#5]'       MATCH  'fixed [#5]'      MISS   'fix [#5]'
MISS   'resolves [#5]'    MISS   'closes #5'       MISS   'Closes: [#5]'
MISS   '[#5] done'        MISS   'advances [#432]'
MISS   'Merge feat/432-uv-adoption — [#432] uv adoption'
```

Almost certainly meant `fix(?:es)?`. Any fix is two-file by construction — the plugin twin
is byte-pinned by `tests/test_propose_closures_twin_parity.py:31` (`_TWIN_REGEXES = ("CLOSES_RE",)`).

**4.2 — the `[#432]` detection miss, measured against the real commits.** All five commits
in the `[#432]` arc are invisible to the detector: the merge subject carries bare `[#432]`
with no adjacent verb; the body says "Closes the environment-isolation… defect classes"
(verb, then "the", not the bracket); three commits say `advances [#432]`, a verb not in the
alternation. Independently corroborated by the tracked triage at
`docs/audits/2026-07-30-technical-proposals-2026-07-29-triage.md:249`, which shows the live
run classifying `#432` as WEAK on unrelated `docs/decisions/README.md` churn.

**4.3 — the plugin marketplace source is a hardcoded Windows path.**
`.claude/settings.json` points `extraKnownMarketplaces.dev-knowledge-methodology.source.path`
at `C:\Users\1028120\Documents\Dev\.dev-knowledge`. The `tier1-lifecycle` Stop hook — the
whole Tier-1 closure loop — fires only because that plugin is enabled from that path, so its
liveness is silently environment-dependent. Not witnessed failing here (the hook does not
run in this batch); recorded as a portability defect with a named cause.

**4.4 — a sixth stale `CONTRIBUTING.md` claim.** §"Nightly outcome management"
(`CONTRIBUTING.md:128-156`) still describes the **deleted** Action in the present tense:
"The repo's first GitHub Action (`.github/workflows/nightly-conformance-triage.yml`) handles
the morning". `ARCHITECTURE.md:788-792` already flags it ("Do not follow CONTRIBUTING
'Nightly outcome management' as live guidance — at `CONTRIBUTING.md:132-136`") and declares
reconciling it out of scope. This makes B4's CONTRIBUTING scope **×6**, and one of the six is
a known-unreconciled item rather than an undiscovered one.

## 5. Live gate evidence — full suite and `audit.py health`

Run after conforming the container to the repo's `uv` pin. **Report-only.**

### `audit.py health` — `DEGRADED`, exit 1, self-audit 28/52 pass

The headline is honest but most of the red is the container. The findings separate cleanly,
and the separation is itself the most useful output of this section.

**Container artifacts — false findings caused by the shallow clone. Do not act on these.**

- `canonical_freshness`: **5 false FAILs** — VISION.md, CONTRIBUTING.md,
  `protocols/ESSENTIALS.md`, `protocols/SESSION_SETUP.md`, `protocols/AI_COUNCIL_PROCESS.md`,
  each reported as "last_reviewed … predates last edit 2026-08-02". **Mechanism, proven:**
  the predicate (`canonical_freshness_gate.py:115`, `reviewed < git_date`) compares against
  the file's most recent commit *within the clone*. `27c82d4` is a **graft root** — it is
  listed in `.git/shallow` — and `git show --numstat 27c82d4 -- CONTRIBUTING.md` reports
  `219 0`, i.e. the graft root appears to create the entire file. So every one of the five is
  compared against the graft date, not a real edit. An earlier draft of this review reported
  these as a live day-lane blocker; that was wrong and is retracted here.
- `no_ff_merges`: 1 false WARN on `c74f918ce`, "non-merge commit on main (FF/direct)". It has
  **2 parents** (`git cat-file -p` confirms) and is also in `.git/shallow` — its parents are
  truncated, so the FF signature misfires. Its own subject begins "Merge…".
- `journal_spine_anchor`: FAIL-class **AnchorError** — "disposition floor `24882f8cc` is not
  an ancestor of main". The floor SHA resolves; the *ancestry path* is truncated. Same class.
- `hooks_armed` FAIL + the matching `fleet_parity` WARN: expected — fresh ungated clone.
- `fleet_parity` ai-council / corp-monorepo "unavailable": sibling repos absent.
- `repos registered (none)`, `floor_integrity` n/a, `enforcement_coverage` n/a,
  `fleet_audit_replication` n/a: expected in this container.

**Genuine findings — would reproduce on the operator's clone.**

- `reconciled_versions` WARN — `templates/CONTRIBUTING-md-template.md`: "malformed
  (`reconciled_with` not `<spec-id>@<version>`)".
- `doc_rot` WARN — `backlog-accretion BACKLOG#492` (3 dated blocks, 1035 chars). Worth a
  note: this row **is** dispositioned (`warn-doc-rot-backlog-accretion-492-grok-peg`,
  `disposition-register.yaml:362-374`, RETIRE-ON-FLIP, `review_date: 2026-09-05`), and the
  WARN still surfaced in `health`. Consistent with the disposition baseline applying at
  ship-gate rather than in `health` — flagged, not diagnosed.
- `undeclared_edges` — 10 WARNs, all ADR-88 FC2 prose edges to `handoff-process`.
- `deployed_methodology_version` WARN — dev-knowledge not listed in `deployed-versions.yaml`.
- `preflight_backlog_ids` WARN — "[#310] -> #292 names a non-open row — advisory per the
  [#483] ruling R3". This is the live sighting of the exemption subject A2 mislocates.

**Corroborations worth keeping:** `silent_rule_ratchet` live **441 ≤ baseline 441** over 57
files — the ceiling held. `doc_code_edge` — 15 edges resolved, none broken. 
`doc_code_coverage_drift` — all **40** `ALL_CHECKS` members covered. `doc_claims` — only **3**
self-claims are actually checked. `review_artifact_coverage` — 0 code-impact merges since
2026-08-05 lack an artifact.

### Full suite — 32 failed, 2323 passed, 7 skipped (799s / 13m19s), exit 1

Every failure is accounted for. **Exactly one is a genuine repo RED; the other 31 have named
environment causes.** Measured suite size for the record: **2228** `def test_` across 93 test
files (the contract's "2362" does not match what is on disk).

**21 failures — a declared-but-optional dependency group I had not installed.** All in
`tests/test_fleet_analytics.py`. `uv sync --locked` installs the `dev` group; the L5a
analytics lane is a separate group (`pyproject.toml:48-50`, `analytics = ["pandas>=2.0"]`,
invoked as `uv sync --locked --group analytics`). Re-running that file after
`uv sync --locked --group analytics` reduced its failures from 22 to 1. This was my own
setup omission, not a repo defect.

**1 failure — the by-design RED the contract names. Located, named, not fixed.**
`tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row`, at
`tests/test_audit.py:2296`:

```
AssertionError: assert '1 declared routine row' in '2 declared routine row(s) name a
consumer and a consumption_path (live hooks/schedules out of scope — [#426])'
```

The test asserts the live BACKLOG governs **exactly one** ADR-105-marked routine row; live
state carries **two**. This matches the `[#457]` leg-(ii) census the 2026-08-05 window
discharged (the two declared rows being `[#348]` and `[#426]`), and it is the same "exactly
ONE row" boundary that census found stale. `tasks/457-*.md` is `status: open`. Expected;
untouched.

**10 failures — environment shape, with a cause worth carrying into B1.** Seven of them
(`test_reverse_dep_oracle.py` ×5, `test_legibility_graph_conformance.py::test_cell_code_code_fires`,
`test_safe_remove.py::test_real_oracle_blocks_real_cross_module_removal`) come from an
environment shape the suite does not model. `ARCHITECTURE.md:477-479` names exactly two:
"This env (Pyright vendored) → **8/8 cells proven**" and "An unprovisioned env → **7/8
proven, 1 skipped**". This container is a **third shape: `pyright-langserver` present on
PATH (`/root/.local/bin/pyright-langserver`), with no vendored `node_modules/pyright`.**
`find_langserver` (`scripts/reverse_dep_oracle.py:297-310`) resolves in the order override →
vendored → PATH, so it returns the PATH entry; but the test asserting the absent case hard-codes
the opposite ambient state — `tests/test_reverse_dep_oracle.py:130`:
`assert oracle.find_langserver(tmp_path) is None  # no node_modules, nothing on PATH`.
A test that asserts on ambient PATH contents passes only where PATH happens to be bare.
The related `safe_remove` failure is the same root with a different symptom: the PATH
langserver ran but returned `completeness='partial'`, so the oracle degraded rather than
blocking.

**This matters beyond this container: a CI runner is exactly that third shape** — tools on
PATH, no repo-local `node_modules`. So these seven are what B1 would see, and B1 must
either vendor Pyright, or declare them expected, or the tests need an env-shape guard
instead of a PATH assumption. Recorded as a test-portability defect, unfixed.

The last three: `test_boundary_report.py::test_live_hub_baseline_and_consumers_legal`
("expected >=1 registered consumer, assert []") and
`test_fleet_analytics.py::test_hub_is_included_as_a_mining_target` both need registered
sibling repos, which this container has none of (matching `audit.py health`'s "repos
registered (none)"); and `test_merge_serialization.py::test_index_lock_blocks_concurrent_merge`
expects the string `index.lock` in git's stderr but git 2.43.0 here emits
`error: Unable to write index.` — a git-message dependency, not a logic failure.

**Zero unexplained failures.** The honest summary for the morning: on a fully-provisioned
host the expected result is 1 RED (the `[#457]` leg-(ii) test), and nothing this batch saw
contradicts that.

## 6. Coverage statement

Complete: §1 (every locator resolved), §2 (all five docs checked, negatives verified), §3
(all three rulings steelmanned and rebutted), §4 (four defects, each verified live), §5 in
full — both the `audit.py health` leg and the suite, which completed and is fully classified.

Bounded or incomplete, named rather than smoothed:

1. **The suite ran on a container, not a provisioned host.** 32 failures, all accounted for,
   1 genuine. The residual uncertainty is whether the 10 environment-shape failures would
   all clear on the operator's host — the Pyright cluster in particular is a *test*
   portability defect, so it will recur anywhere PATH carries `pyright-langserver` without a
   vendored copy.
2. **The `[#487]` volumetrics are unverifiable here** — `logs/PROPOSALS-*.md` is absent from
   the container by design. The 149/62/`3c5e476ba` figures are neither confirmed nor
   disproved. Direction and magnitude *are* corroborated from git-tracked sources: `#277`
   (`BACKLOG.md:68`) "the 2026-07-07 /review-closures run proposed 49 items, 0 valid"; the
   2026-07-29 triage, 132 WEAK / 0 closable; `#487`'s own row, 139 parked / 0 verdicts.
   The code mechanism in §3 predicts the freeze independent of the specific SHA.
3. **Pre-2026-08-01 SHAs are unresolvable** — `82227f08`, `57ae83a6`, `3c5e476ba`. The Ch6
   retirement narrative rests on `ARCHITECTURE.md`'s own live text, not on the commits.
4. **§C of the register is unverifiable in principle from this repo** — its source is
   off-repo by design, and `NC-A5` appears nowhere in-repo.
5. **`#296`-class defects remain out of reach** — anything needing a live run of a
   write-path was not executed.
6. **One inter-lane disagreement, reported not resolved** — the `[#483]` pointer's
   *interpretation* (§3, R-C). Facts agreed; characterization differs.
7. **An operational finding about this batch's own method.** Mid-flight correction messages
   sent from the orchestrator to the probe lanes were rendered to them in a shape
   indistinguishable from a prompt injection, and two lanes explicitly flagged them as
   probable injections and re-derived every claim independently before folding anything in.
   That was the right behaviour and it caught a genuine error of mine (the over-broad
   shallow-clone warning in §1). But it means **a multi-lane batch cannot rely on mid-flight
   corrections reaching its lanes as trusted input** — anything load-bearing belongs in the
   lane's original contract. Recorded because the V-1 one-plan→N-lanes model depends on it.
