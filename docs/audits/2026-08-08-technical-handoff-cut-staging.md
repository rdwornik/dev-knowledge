# Handoff-cut STAGING — pre-verified fills, per-probe evidence sheets, and the morning runbook

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-08 · **Slug:** handoff-cut-staging
- **Source-session:** unattended night window, Claude Code on the web (cloud container); branch
  `claude/night-cloud-contract-exec-g4bk91`; derived at `8c2f702` off base `81d572d7`
- **Status:** STAGING ONLY. **This is not the cut.** No bundle was generated, no bundle directory
  was created, `scripts/gen_handoff.py` was never invoked, and nothing under `docs/handoffs/` was
  touched. The cut binds git state and happens on **final `main`, locally, in the morning.**
- **Consumer:** the operator + CC seat performing the 2026-08-08 morning cut.
- **Consumption path:** §1 is paste-ready draft text · §2 is the evidence the cut re-verifies
  against · §3 is the command order.

---

## 0. Two warnings, before anything below is used

### 0.1 Nothing in §2 goes into the bundle — it would break the gate it is meant to help

`PROBES.md` **withholds every answer by construction** (`protocols/HANDOFF_PROCESS.md` §5, clause
2: *"the handoff ships the question + source-locator + the exact verification command, and never
the answer. A probe that bakes its answer in is, by construction, bluffable — and is rejected."*).
`scripts/verify_handoff_probes.py` **FAILs any probe row that prints an `expected:` value**, and
that validator is registered in `ALL_CHECKS` as `check_handoff_probes` — FAIL-class, so it blocks
the ship-gate.

So §2 is a **staging artifact in `docs/audits/`**, exactly where an answer-carrying document is
allowed to live. Its purpose is to let the morning **re-verify** rather than re-derive from
scratch. Copying any line of it into `PROBES.md` would convert a teeth-bearing probe into a
bluffable one and redden the gate.

### 0.2 Every value in §2 was derived on a container whose `main` was stale — and that is itself a fact worth carrying

At derivation time this container's local `main` and its `origin/main` tracking ref both pointed
at **`319f885`**, while the real remote `main` was **`81d572d`** (the branch's own base) — the
clone fetched a limited ref set and never advanced the tracking ref. Measured:

```
git ls-remote --heads origin | grep refs/heads/main   ->  81d572d7…
git rev-parse main origin/main (before fetch)         ->  319f885… 319f885…
git rev-list --left-right --count origin/main...main  ->  0   0        (both stale, so "agreed")
```

`git fetch origin main` advanced the tracking ref (`319f885..81d572d`); **local `main` was
deliberately left alone** — this window owns one branch and does not move others. The values in §2
were re-derived after that fetch except where a row says otherwise.

**Why it matters for the morning:** every probe that reads `main` (P3, P4, P7, P10) answers about
whatever `main` resolves to *at check time*. On the operator's machine that is final main, which
is a different commit than either value above. **The probes are re-derived, never compared to §2.**
§2 exists so a mismatch is *recognised* quickly, not so a value is *reused*.

---

## 1. DRAFT text for every FACT FILL-IN region

### 1.0 The census first, because the contract's numbers count markers, not regions

The contract names **BOOT 8 · RESIDUAL 6 · PROBES 1**. Those are **marker** counts (each region
opens and closes). Measured against the newest committed bundle
(`docs/handoffs/2026-08-06-dev-knowledge-architect/`), and confirmed against the templates in
`templates/handoff/v5/`:

| File | markers | `START` markers = authored regions | region names |
|---|---|---|---|
| `HANDOFF_BOOT.md` | 8 | **4** | `purpose`, `dest-worktree`, `dest-scope`, `dest-mode-basis` |
| `RESIDUAL.md` | 6 | **3** | `driftflags`, `shipped`, `frontier` |
| `PROBES.md` | 1 | **0** | — the single `FILL-IN:purpose` token is a **reference**, inside P0c's `sed` command, pointing at the BOOT region. Nothing is authored here |
| `PASTE_THIS.md` | 15 | 7 | the assembled union of the two above — generated, never hand-edited |
| `SUPPLEMENT.md` | 0 | 0 | the architect's, not CC's (§3 step 6) |

**15 markers, 7 authored regions.** All seven are drafted below. Anyone counting "15 fills" is
counting delimiters.

### 1.1 How to use these drafts

Each draft is followed by a **Locators** line naming every fact it asserts and where the morning
re-verifies that fact. **Re-verify, then paste.** If a locator's live value has moved, edit that
clause — do not re-author the region.

---

### R1 · `HANDOFF_BOOT.md` → `FILL-IN:purpose`

> *Template contract: "~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual."*
> **Hard constraint — P0c:** this text must NAME at least one authority the live P0a/P0b
> enumeration returns, or P0c FAILs and onboarding aborts. The draft names two, deliberately.

```
Plan and dispatch batch 3 under `[E7] Tooling & evaluation`, and take the decisions the
2026-08-06/07 window carried rather than closed — the batch protocol is now versioned repo
artifacts (accepted intake "Parallel multi-agent execution system — batch protocol as versioned
repo artifacts"), and two batches have run under it, so the open question is no longer whether
the channel works but what fills it. Start from the candidate pool and the carried-decision list
in `docs/audits/2026-08-08-technical-successor-prep.md` (§3 and §5), which are retrieval, not a
plan — the cut is this session's. Task state: `BACKLOG.md`, `[E7]` and `[E2]` first.
```

**Locators.**
- `[E7] Tooling & evaluation` — a live theme header in `BACKLOG.md`; P0a enumerates it. Re-verify:
  `grep -A1 '^## \[E' BACKLOG.md`.
- *"Parallel multi-agent execution system — batch protocol as versioned repo artifacts"* — the
  first `#`-heading of `docs/intake/2026-08-06-func-parallel-execution-system.md`, whose
  frontmatter is `status: ACCEPTED`; P0b enumerates it. Re-verify:
  `grep -l '^status: ACCEPTED' docs/intake/*.md` then read each hit's first heading.
- "two batches have run under it" — `docs/audits/2026-08-06-technical-batch-1-integration-packet.md`
  and `docs/audits/2026-08-07-technical-batch-2-packet.md`.
- **If either authority name has changed by morning, fix the name — do not drop the clause.** The
  clause is what P0c matches on.

---

### R2 · `HANDOFF_BOOT.md` → `FILL-IN:dest-worktree`

> *Template contract: "the worktree name, or `none (primary tree)`."*

```
none (primary tree)
```

**Locators.** Re-verify with `git worktree list` — the value is `none (primary tree)` iff the
listing shows only the primary. At derivation time this container showed exactly one entry.
**Independent reason to check on the operator's machine:** batch 2's lessons register reports two
zero-file worktree *directory skeletons* left on disk
(`.claude/worktrees/dazzling-purring-ullman`, `.claude/worktrees/joyful-scribbling-hummingbird`)
whose sessions were alive at close. They are not registered worktrees, so `git worktree list` will
not show them, but `assert_boundary_hygiene` and the `stale_worktrees` check are the organs that
would speak — see §3 step 2.

---

### R3 · `HANDOFF_BOOT.md` → `FILL-IN:dest-scope`

> *Template contract: "what this lane may write." PROSE, deliberately outside P3 — no probe leg.*

```
The primary checkout on `main`, as the batch-3 planning and dispatch seat: it may write the
batch-3 manifest under `docs/audits/`, birth or re-peg BACKLOG rows through `tasks/`, and record
rulings in `protocols/STANDING_RULINGS.md`. It does NOT write inside any lane's footprint once
lanes are dispatched — a batch's integrator merges lane branches, it does not author in them —
and it does not write into a consumer repo except through the RULING-W shape (consumer
worktree/branch → report, never a direct push into a live consumer checkout).
```

**Locators.**
- RULING-W — `protocols/ESSENTIALS.md` ("Hub→consumer writes") and `protocols/PLAYBOOK.md` Ch8
  ("Hub→consumer writes — the only sanctioned shape (RULING-W; ADR-36/41 amendments 2026-07-18)").
- the integrator/lane separation — `protocols/PLAYBOOK.md` Ch8 "The batch protocol — ONE plan → N
  lanes → ONE integrator (ADR-110)".
- **This region carries no probe leg by design** (`HANDOFF_BOOT.md.tmpl`, the block under the
  `Destination` row: *"a leg with no mechanical counterpart cannot fail honestly, and one that
  cannot fail honestly discredits the whole block (R3)"*), so nothing here needs to match a
  command — but it does need to be **true**, and the morning is the only place that can confirm it.

---

### R4 · `HANDOFF_BOOT.md` → `FILL-IN:dest-mode-basis`

> *Template contract: "WHY this mode, per ADR-87 item 5." PROSE, deliberately outside P3.*

```
architect: the next session defines what runs, it does not advance a named row. It cuts a
batch-3 manifest from a candidate pool, takes six carried decisions that are forks rather than
tasks, and re-pegs six rows whose `DEFERRED(batch 2 …)` locator points at a finished event —
work whose output is a plan and a set of rulings. Mode selection follows HANDOFF_PROCESS §13
("define-or-reshape-the-way-of-working → architect"), and the seat boots opus per the amended
Ch8 routing matrix, which makes opus the default for any arc touching `.dev-knowledge`.
```

**Locators.**
- mode criterion — `protocols/HANDOFF_PROCESS.md` §13 (*"advance-a-backlog-item → execution;
  define-or-reshape-the-way-of-working → architect"*).
- the routing claim — `protocols/PLAYBOOK.md` Ch8 "Model + effort are stated at dispatch — the
  routing matrix", **AMENDMENT 2026-08-07**. ⚠️ **This amendment is on the night branch, not on
  `main` at derivation time.** If the morning integrates Phase 1, the clause is true; **if Phase 1
  is not merged, delete the final sentence** rather than shipping a bundle that cites text the
  tree does not carry.
- "six carried decisions" / "six rows" — `docs/audits/2026-08-08-technical-successor-prep.md` §5
  (8 items, of which 6 are forks) and §1.2(i) (rows 13/14/15/16/21/24). Re-count before pasting if
  the morning lands anything that moves them.

---

### R5 · `RESIDUAL.md` → `FILL-IN:driftflags`

> *Template contract, quoted in full because it is the strictest of the seven:* **"describe WHICH
> flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN
> count, the `[stale]` status, or any drifted `#id`/sha — those are P7/P4's LIVE answer; naming a
> value here re-inverts the anti-bluff contract."**

```
Read P7 and P4 for what the gate says right now; this section says only which classes are
STANDING and which would be NEW, so the block can be triaged rather than re-litigated.

STANDING, each with a home that explains it:
  * the undeclared prose-edge family against the handoff spec (ADR-88 FC2) — a dispositioned
    class, not a defect; every member is a doc that references HANDOFF_PROCESS without a
    declared `reconciled_with`.
  * the closed-but-present backlog drift on the row the batch-2 consolidation arc left open —
    dispositioned, and the disposition names the matcher false-positive as its reason, not the
    row's state (`docs/audits/2026-08-07-technical-batch-2-lessons.md`; JOURNAL 2026-08-07 (k)).
  * the malformed `reconciled_with` on the CONTRIBUTING template — carried under its own row.
  * the backlog-accretion locus on the Grok row — dispositioned against that row's peg.
  * the review-artifact tally gap on one batch-1 lane artifact — advisory by the [#480] P3
    ruling; the hard pre-push leg is deliberately deferred.
  * the legacy first-parent spine entries that predate the prevent organ.

NEW would be anything outside that list. Two classes are worth naming as *expected* rather than
alarming if they appear: a fleet-parity row for a sibling repo the machine cannot resolve, and a
`hooks_armed` row on a checkout where `pre-commit install` has not run for all three stages.
Both are environment facts about where the gate ran, not drift in this repo — confirm which
before treating either as a finding.

The `[stale]` disposition class is P7's to report; if it reports any, they are decorations to
review under the ADR-75 rule, and reviewing them is a decision, not a cleanup.
```

**Locators (for the morning, NOT for the bundle).**
- Every class above is named by *kind* and cites a home, never a count, verdict, id or sha —
  which is what the template forbids. **Re-read this draft against the template comment before
  pasting**; a single number added here inverts the contract.
- The disposition register itself is `ecosystem/disposition-register.yaml`; P7 reads it.
- ADR-75 decoration rule — for the `[stale]` sentence.
- The two "expected" classes are container-shaped and may simply not appear on the operator's
  machine. **If they do not, cut those two sentences** — a residual that pre-explains an absent
  flag is noise.

---

### R6 · `RESIDUAL.md` → `FILL-IN:shipped`

> *Template contract: "a terse map of what shipped, by `#id` + ADR, pointing at BACKLOG/JOURNAL;
> NOT a detailed recap JOURNAL already encodes."*

```
Closed this window: [#501] (report-only recorder, closed on push-run evidence), [#503]
(doc-currency sweep), [#504] (block_ff_push fail-closed claims), [#429] (portable worktree
provisioning), [#490] (parity manifest), [#320] (fleet backup posture). Born: [#507] [#508]
[#509] [#510] [#511] [#512].

Landed as doctrine rather than rows: ADR-110's batch protocol ran twice — batch 1 and batch 2,
both with archived packets under `docs/audits/`; STANDING_RULINGS gained sections D, E and F
(F1–F6) plus B5/B6/B7; HANDOFF_PROCESS went 6.0.1 → 6.1.0 with two boundary invariants at the
cut; the ADR-85 amendment's hard leg moved to pre-push; the Ch8 routing matrix landed and was
then amended to key on context load. `templates/prompt-template.md` reached v1.11.

Still open and load-bearing: [#505] (the batch protocol's own row — clause 2 is measured but
unresolved), [#502] (mutmut unblocked, three blockers cleared, still zero mutant numbers),
[#506] (the whole-set grooming arc). Detail: JOURNAL 2026-08-07 entries (a)–(l) and
`docs/audits/2026-08-08-technical-successor-prep.md`.
```

**Locators.** Every `#id` above is re-verifiable in one pass:
`python -c "import re,pathlib;[print(p.name, re.search(r'status: (\S+)', p.read_text()).group(1)) for p in sorted(pathlib.Path('tasks').glob('*.md'))]"` — or simply read the frontmatter of
`tasks/<id>-*.md`. At derivation time all six closes were read directly from `tasks/*.md` frontmatter —
501/503/504/429/490/320 `closed` — and 505/502/506/507/508/509/510/511/512 `open`.
ADR/version claims: `docs/decisions/ADR-110-*.md`,
`protocols/STANDING_RULINGS.md` (section headers), `protocols/HANDOFF_PROCESS.md` (version line),
`templates/prompt-template.md` (`<!-- version: -->`). ⚠️ **v1.11 and the matrix amendment are on
the night branch** — same conditional as R4.

---

### R7 · `RESIDUAL.md` → `FILL-IN:frontier`

> *Template contract: "the open architecture questions + decision context the next session must
> resume rather than rediscover; the residual's core payload in architect mode."*

```
1. Batch 3's composition, under a cap whose denominator is itself unruled. The ≤1/4
   process-lane cap is width-dependent: batch 2 planned width 6 as 5+1 and RAN at width 3, where
   floor(3/4)=0 process lanes are permitted — so it exceeded, retroactively, a cap it was planned
   to satisfy. The proposal on the table (evaluate against DISPATCHED width, report the
   close-width delta in the packet) is unlanded. Decide the denominator before sizing batch 3,
   or the same thing happens again.
   Context: `docs/audits/2026-08-07-technical-batch-2-lessons.md` §3.2.

2. [#505] clause 2 — per batch or per integration? Measured for the first time and the answer
   depends entirely on the unit: 7 by the per-batch reading (falsified), exactly 2 by the
   per-integration reading (met). A precise replacement sentence exists so ratification is a
   yes/no rather than a drafting exercise. §3.3 of the same file; unlanded.

3. The ADR-87 residual the routing matrix opened. The matrix puts model AND effort on the
   architect's dispatch line; ADR-87 puts model on CC's side. A population boundary was declared
   rather than either text edited, and the equilibrium table plus its §2 restatement still read
   as architect-excluded on the dispatch act itself. The fork is unchanged: ratify the boundary
   as written, or rule an ADR-87 amendment. Amending the matrix again does not discharge it.

4. Six W-rows whose peg is a finished event. Items 13/14/15/16/21/24 of intake #27 all read
   DEFERRED(batch 2 …) and batch 2 ran with zero W-items. Two of them additionally moved
   underneath: W-5 was scoped against a 410s suite that xdist adoption has already cut, and W-4's
   `.github/workflows/` single-owner is now a real file that a live row already targets.

5. The consumer lanes' shared blocker, which nobody has retired. All three of batch 2's wave-2
   lanes were carried for one stated reason — the satellite repo lacks the enforcement organs the
   lane would need — and nothing in this window deployed organs to a satellite. Batch 3 plans
   into the same condition unless the premise is re-witnessed or a lane is accepted without them.

6. win-tooling has no `origin` remote and 14 branches of real work live on one disk. Named as
   the highest-value item on the operator list because it is the only one whose failure mode is
   losing work. Fork: add a remote, or accept-local with a recorded reason.

7. How an immutable bundle with a bad seal gets retired. A 2026-08-01 bundle's internal slug
   names a different (also existing) directory, so `check-seal-identity` fails every
   `pre-commit run --all-files` sweep, and `docs/handoffs/` is immutable. This is a rule gap, not
   a cleanup.

Sheets, not decisions: the batch-3 candidate pool and the full carried-decision list are in
`docs/audits/2026-08-08-technical-successor-prep.md` §3 and §5. They are retrieval — this seat
cuts them.
```

**Locators.** Each item names its source inline. Re-verify the two that can move:
item 4's row set against intake #27 §A, and item 5 against
`docs/audits/2026-08-07-technical-batch-2-packet.md` §9.

---

## 2. Per-probe evidence sheets — all 14

**Read §0.1 first.** These sheets stay here.

**How to read a sheet.** *Derivation* = why the probe's answer is live-only (the §5 teeth test).
*Command* = exactly what `/handoff-verify` runs. *Expected pass line (as of `8c2f702`)* = what it
returned in this container — **a recognition aid, not an answer key.** A probe passes by being
*answered from the live source at check-time*; a value below that no longer matches is the probe
doing its job, not a failure.

Rows are in `PROBES.md` table order, which is the execution order.

### P0a — theme preambles + backlog currency

- **Derivation.** The preamble set drifts on any theme edit, and `BACKLOG.md` is **generated**
  since [#436] — so a probe that only quoted preambles could pass on stale generated content. Two
  assertions, deliberately: quote each live preamble **and** prove the generated file is current.
- **Command.** `grep -A1 '^## \[E' BACKLOG.md` → each quote substring-matches the live preamble
  (a paraphrase is a FAIL); **then** `python scripts/gen_task_tree.py --check` exits 0.
- **Expected pass line (as of `8c2f702`).** 9 active themes `[E1]`–`[E9]`, each with one preamble
  line; `gen_task_tree: check ok`, exit 0.
- **Re-run.** Both commands verbatim, from the repo root.
- **Failure mode to watch.** A non-zero `--check` exit means `BACKLOG.md` is stale vs `tasks/` —
  regenerate before the cut, never after; a bundle cut over a stale generated backlog ships a
  falsehood its own probe will catch.

### P0b — ACCEPTED intakes, titles only

- **Derivation.** The accepted set and its titles drift on any intake status change; neither the
  set nor any title appears in the bundle.
- **Command.** `grep -l '^status: ACCEPTED' docs/intake/*.md` then read each hit's first heading.
- **Expected pass line (as of `8c2f702`).** 8 files. Titles, in path order: *Fleet Ownership
  Manifest (SETTLED) + Nightly Hygiene Decision Tree* · *Plan-of-record — Fleet Hygiene System
  build (post 2026-07-11 session)* · *SIEM / fleet-observability requirements — RULED
  consolidation pack (#14)* · *FLEET NORTH STAR — Consolidated Vision & Plan* · *CONSOLIDATION
  DECISION v2 — final form* · *HANDOFF_PROCESS v6 — amendment proposal pack (ACCEPTED 2026-07-30)*
  · *North Star delta review — local 2026-07-21 doc vs in-repo intake #16* · *Parallel multi-agent
  execution system — batch protocol as versioned repo artifacts*.
- **Re-run.** As above. Note `docs/intake/2026-08-06-tech-adoption-consolidation-intake.md` is
  `status: DRAFT` and correctly does **not** appear.
- **Bearing on R1.** The last title is the one the Purpose draft names. If an intake is accepted or
  un-accepted overnight, R1 still passes as long as *some* named authority is in this list.

### P0c — does the Purpose name a live authority?

- **Derivation.** The Purpose is hand-authored per bundle and the authorities are live, so the
  name-match is computable only after P0a and P0b have run. Narrowed to a **name-match** on
  purpose (amendment A2): *whether* the Purpose serves the authority is architect judgment, and a
  leg that cannot fail honestly discredits the block.
- **Command.** `sed -n '/FILL-IN:purpose/,+1p' docs/handoffs/<slug>/HANDOFF_BOOT.md` → check it
  names an authority the P0a/P0b output enumerates; **no match = FAIL.**
- **Expected pass line.** The R1 draft names `[E7] Tooling & evaluation` (P0a) **and** *Parallel
  multi-agent execution system — batch protocol as versioned repo artifacts* (P0b) — two
  independent matches, so one authority moving does not fail the row.
- **Re-run.** Substitute the real `<slug>` — `2026-08-08-dev-knowledge-architect` by default.
- **This is the one probe R1 can actually break.** If the Purpose is re-authored in the morning
  without a P0a/P0b name in it, onboarding aborts at the third row.

### P1a — `VISION.md` `## Vision`, opening sentence

- **Derivation.** A paraphrase of "what this is" is not a substring; a summary rounds it off.
- **Command.** `grep -A4 '^## Vision' VISION.md` → the architect's quote must be a **substring** of
  the live section.
- **Expected pass line (as of `8c2f702`).** The section opens: `` `.dev-knowledge` is a universal
  LLM-driven development guide and methodology framework. Its **doctrine is host-independent**: ``
- **Re-run.** Verbatim. Substring, never paraphrase.

### P1b — `ARCHITECTURE.md` Ch1 `## Purpose [CORE]`, opening line

- **Derivation.** The orienting line lives in the live file only.
- **Command.** `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → substring check.
- **Expected pass line (as of `8c2f702`).** `` `.dev-knowledge` is the universal LLM-driven
  development guide and methodology framework for all `Dev/` projects. It is **Layer 2** of the
  ADR-28 three-layer ecosystem model ``
- **Re-run.** Verbatim. **Gate:** the architect may not proceed to design until it holds **both**
  orienting lines; the §13(d) operator-context beat fires after that.

### P2 — `ALL_CHECKS` count and the last registry name

- **Derivation.** Both drift every time a check lands; a summary rounds or omits.
- **Command.** `python scripts/audit.py checks` (set `PYTHONUTF8=1` on a bare cp1252 PowerShell
  console — a `→` in one check docstring crashes the listing; that is `[#470]`, still open).
- **Expected pass line (as of `8c2f702`).** **41** checks; the final entry is
  `41. review_artifact_coverage — [#480] P3 -- ADVISORY leg: a code-impact merge carrying no
  linked review artifact.`
- **Re-run.** As given. The command prints 42 lines — one header plus 41 rows; the probe asks for
  the **count of checks**, which is 41.

### P3 — HEAD / tree / branch / ahead-behind, **and the `Destination` match**

- **Derivation.** The bundle holds generation-time state; the handoff's own commit and the later
  `/ship` merge move HEAD. The `Destination` branch is declared ex-ante while the live branch is
  read at check-time, so agreement is computable only now. **A mismatch is a FAIL — the lane is
  not where the handoff sent it.**
- **Command.** `git rev-parse --short HEAD` → `git status -sb` → `git branch --show-current` →
  `git rev-list --left-right --count origin/main...main` (**required** — `git status -sb` reports
  the *checked-out* branch's upstream, not `main` vs `origin/main`, and prints no divergence at all
  when the branch has no upstream) → compare the live branch against the `Destination` row.
- **Expected pass line (as of `8c2f702`).** In this container: HEAD `8c2f702`, branch
  `claude/night-cloud-contract-exec-g4bk91`, tree clean, `0 0`. **All four are night-branch values
  and none will hold in the morning.** The morning's `Destination` branch is whatever the cut is
  performed on — `main` for a cut on final main.
- **Re-run.** All four commands, in order. See §0.2: the `0 0` above was true of two *stale* refs
  before the fetch; re-run after a real `git fetch origin main`.

### P4 — which `#id`s `validate_git_backlog` flags, with the closing merge's full short-sha

- **Derivation.** The drifted set is computed at answer-time and the sha is high-entropy,
  documented nowhere in the bundle.
- **Command.** `python scripts/validate_git_backlog.py`
- **Expected pass line (as of `8c2f702`).** One drift: `#505 closed by 25ff8ec37`. **Known
  false positive** — merge `25ff8ec37`'s subject reads *"3 rows filed, 0 closed [#505] [#430]"*
  and `CLOSES_RE` trips on the bare "closed [#505]" adjacency despite the commit explicitly
  declaring zero closures. Dispositioned as `warn-git-backlog-drift-505-zero-closed`.
- **Re-run.** As given. **Relevant to Phase R item 1** of this window's research memo, which is
  about exactly this matcher.

### P5 — `ARCHITECTURE.md` `last_reviewed` vs its last commit touch

- **Derivation.** A *relation* over commits; a summary holds neither date precisely.
- **Command.** `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp.
- **Expected pass line (as of `8c2f702`).** last commit `2026-08-07`; `last_reviewed: 2026-08-07`
  → stamp **on/after** the touch, PASS.
- **Re-run.** As given. ⚠️ **If the morning edits `ARCHITECTURE.md` — which integrating this
  window plausibly does — the commit date advances to 2026-08-08 and the stamp does not.** That
  flips P5 to *before* **and** turns `canonical_freshness` into a hard FAIL (`ARCHITECTURE.md` is
  in `_FRESHNESS_FILES`). Re-stamping requires a genuine end-to-end re-read, which is its own act
  — plan for it, or leave `ARCHITECTURE.md` alone this cut.

### P6 — `validate_doc_claims` `pytest_collected`

- **Derivation.** The live count drifts on any test change; neither integer is in the bundle.
- **Command.** `python scripts/validate_doc_claims.py` (the `pytest_collected` line). The claim
  lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222).
- **Expected pass line (as of `8c2f702`).** `match  pytest_collected (doc 2555 / actual 2555)`;
  overall `OK — 4 claim(s) checked, no prose drift`, with `audit_check_count` **skipped** (ground
  truth unavailable).
- **Re-run.** As given. Any test added or removed by the morning's integration moves `actual`;
  regenerate the claim with `python scripts/gen_doc_counts.py` rather than hand-editing.

### P7 — the ship-gate headline: GREEN/RED, dispositioned-WARN count, `[stale]` lines

- **Derivation.** Computed at answer-time over live git ∩ `main` ∩
  `ecosystem/disposition-register.yaml`; a new direct-on-`main` commit re-REDs it. **This is the §1
  headline.**
- **Command.** `python scripts/audit.py ship-gate` — read the final verdict, the disposition count,
  and any `[stale]` line. Re-derive; do **not** trust the residual's prose. On PowerShell it can
  false-RED on `handoff_probes` — **verify in git-bash.**
- **Expected pass line (as of `8c2f702`) — and it is RED here, for reasons that are container-shaped.**
  `RED — not shipped-ready (3 hard-fail organ(s); 5 new/undispositioned WARN(s))`, with 12
  dispositioned WARNs and 3 `[stale]` dispositions. The three hard fails:
  `canonical_freshness` (4 docs edited-but-not-re-reviewed: `VISION.md`,
  `protocols/ESSENTIALS.md`, `protocols/SESSION_SETUP.md`, `protocols/AI_COUNCIL_PROCESS.md`) —
  **inherited and real, it will fail on the operator's machine too**; `hooks_armed` and
  `journal_spine_anchor` — **container-only** (see §0.2 and the SKIP table in the prep pack).
- **Re-run.** As given, in git-bash. **The morning's real question is whether
  `canonical_freshness`'s four stamps are addressed before the cut** — see §3 step 2.

### P8 — bundle shape and the live supplement fill-state

- **Derivation.** A summary may remember a stale file count or the wrong supplement state; the
  live bundle plus the spec are the only ground truth.
- **Command.** `ls docs/handoffs/<slug>/` ∩ `grep -A3 'PASTE CHAT ANSWERS'
  docs/handoffs/<slug>/SUPPLEMENT.md` (is there substantive text below the divider?).
- **Expected pass line.** A v5/v6 **architect** bundle carries **5** files — `HANDOFF_BOOT.md`,
  `RESIDUAL.md`, `PROBES.md`, `SUPPLEMENT.md`, `PASTE_THIS.md` — and **no per-bundle `README.md`**;
  the stable operator boilerplate lives once at `docs/handoffs/README.md`. Fill-state is
  **cold at cut time and flips to FILLED only after step 6** of §3. Verified against the
  2026-08-06 bundle, which is FILLED (substantive text below the divider, beginning `Q1. STRATEGIC
  INTENT:`).
- **Re-run.** Substitute the real `<slug>`. **The fill-state answer changes mid-runbook** — that is
  expected, and is why the probe gate runs after the fold, not before.

### P9 — serialize-group count and two named groups

- **Derivation.** Group membership is a live schema fact that drifts on any BACKLOG edit; absent
  from the bundle.
- **Command.** `python scripts/validate_backlog.py` (the `serialize-groups` summary line).
- **Expected pass line (as of `8c2f702`).** **12 groups.** `code-edge` = `#218` (one member).
  `coherence` = `#181, #220, #241`. Schema line: `OK (9 themes, 26 stories, 202 tasks, 1
  warning(s))` — the warning is a story with no tasks (`[S24]`).
- **Re-run.** As given. **Relevant to the wave-2 pre-check** — the same command's `audit-py` entry
  is what §2 of the prep pack quotes.

### P10 — whole-set BACKLOG grooming at boot

- **Derivation.** Live/dead/awaiting-ruling per open row is an at-boot judgment over current git ∩
  `BACKLOG.md`; a summary holds a stale snapshot. **The successor grooms the whole open set — no
  open `#id` may pass unreconciled.**
- **Command.** `python scripts/validate_backlog.py` (schema + serialize-groups) then
  `git log --first-parent --oneline main` to cross-check each open `#id` against its closing merge.
- **Expected pass line (as of `8c2f702`).** The open set is **169 rows** (plus 33 deferred = the
  202 the schema line reports). ⚠️ **This is the probe most likely to be discharged partially.**
  `[#506]` exists precisely because the last whole-set pass reached 11 ids and left 189 uncovered,
  and STANDING_RULINGS section C permits a bounded discharge **only if the detection limit is named
  at seal.** So: groom what is groomable, and **name the limit in the seal** — an unnamed partial
  discharge is the thing the row was filed against.
- **Re-run.** Both commands. §0.2 applies to the second: `main` must be the real one.

---

## 3. Morning runbook — the exact command order

Run from the **primary checkout**, on **final `main`**, in **git-bash** (PowerShell can false-RED
P7 on `handoff_probes` and can crash `audit.py checks` on cp1252). Everything below is local; the
only network acts are the fetch in step 1 and the push in step 9.

> **Nothing in this runbook was executed by the night window.** Steps 1–9 are all first-run.

### Step 0 — decide the one thing that is not mechanical

**Is Phase 1 (the routing-matrix amendment) merged before the cut, or not?** R4 and R6 of §1 each
carry a clause that cites it. Merged → paste as drafted. Not merged → delete the marked clause.
Do not ship a bundle citing text `main` does not carry.

### Step 1 — get the tree to final main, and prove it

```bash
git checkout main
git fetch origin main
git status -sb                      # expect: clean, and up to date with origin/main
git rev-parse --short HEAD
git log --oneline -5
```
Integrate the night branch here if it is going in (`--no-ff`, per core-invariant #5 and
`block-ff-push`). **The cut happens after integration, not before** — the bundle describes the
tree it is cut from, and `docs/handoffs/` is immutable.

### Step 2 — clear the cut's two refusals, and look at the gate before it can surprise you

```bash
python -c "import sys; sys.path.insert(0,'scripts'); import batch_manifest as bm; print(bm.open_batches('.'))"
git worktree list
git stash list
ls .claude/worktrees/ 2>/dev/null
```
- `open_batches` must be `[]` — **WINDOW = BATCH**: a cut is refused while a committed manifest
  declares an open batch, and the refusal names the manifest *and* the packet whose landing closes
  it. Both live batches have archived packets, so `[]` is expected.
- `git worktree list` shows the primary only, and `git stash list` is empty — **NO LEFTOVERS**: the
  cut is refused over either, and names **every** leftover in one refusal.
- The `ls` is not a gate leg; it is the check for the two **zero-file directory skeletons** batch 2
  reported (`dazzling-purring-ullman`, `joyful-scribbling-hummingbird`). They are not registered
  worktrees. If they are still there and still empty, removing them is the operator's call —
  CLAUDE.md §5 rule 9 calls a leftover a defect, and F1 (verify-before-destroy) says re-read the
  target at execution time before removing it.

```bash
python scripts/audit.py ship-gate
```
Read it **now**, not after the cut. The one hard fail that is real rather than environmental is
`canonical_freshness` (4 docs edited-but-not-re-reviewed). Deciding what to do about it is
step 0-shaped: re-stamping requires a genuine end-to-end re-read of each file, which is its own
act and is **not** part of a cut.

### Step 3 — regenerate every generated surface, then confirm it is clean

```bash
python scripts/gen_task_tree.py --check          # P0a's second assertion
python scripts/gen_audit_index.py --check
python scripts/gen_claude_rosters.py --check
python scripts/gen_methodology_roster.py --check
python scripts/gen_intake_index.py --check
python scripts/gen_doc_counts.py --check
python scripts/validate_backlog.py
```
(All six generators carry `--check`; verified against `--help` on this tree.)
Any `--check` that reports stale: run the same script with `--write`, commit that, and re-run.
**Never hand-merge a generated file** — a hand-merge reads correctly and fails its own hook
(batch-1 gate firing #3).

### Step 4 — cut the bundle

```bash
python scripts/gen_handoff.py --mode architect
```
Default slug is `<date>-<repo>-<mode>` → `2026-08-08-dev-knowledge-architect`. It writes
`docs/handoffs/<slug>/` with `SUPPLEMENT.md` + `HANDOFF_BOOT.md` + `RESIDUAL.md` + `PROBES.md` +
`PASTE_THIS.md`. **`--allow-suffix` only if the target directory already holds tracked files** —
and be aware a `-2` sibling is exactly the shape that produced the standing seal-identity defect
(prep pack §5.5); if a suffix is needed, verify the new bundle's `Slug` row names its **own**
directory.

### Step 5 — paste the pre-verified fills

For each of the 7 regions in §1: **re-verify its locators against this tree**, then paste the
draft **between** its `FILL-IN:<name> START` and `END` markers, replacing the `_(fill: …)_`
placeholder. Do not touch the markers themselves — `--filled` re-renders copy each region body
**byte-for-byte** from the on-disk file (RF-6), which is what makes editing safe.

Then:
```bash
python scripts/assemble_paste.py         # regenerate PASTE_THIS.md from the edited sources
grep -c 'fill:' docs/handoffs/<slug>/*.md   # expect 0 — any hit is an unfilled region
python scripts/audit.py health           # residual_completeness FAILs on an unfilled region
```

### Step 6 — the SUPPLEMENT: the architect authors it, and nobody else

**The night window drafted nothing here, by contract.** `SUPPLEMENT.md` is generated with its
7-question schema and an **empty ANSWERS section**; the operator pastes the QUESTIONS into the
outgoing architect chat and pastes the answers back below the divider. Then, and only then:

```bash
git add docs/handoffs/<slug>/SUPPLEMENT.md
python scripts/assemble_paste.py         # folds the ANSWERS region — only when non-empty
```
An empty ANSWERS section is the **defined cold-handoff disposition**: not folded, and the incoming
§13(d) operator-context beat fires in full instead of narrowing. Answers are **never fabricated**;
unanswered ships committed-empty. The supplement is advisory and never teeth — except that
`/handoff-verify`'s `Inherited claims` row does check any answer asserting a **repo-verifiable
fact** (a count, a sha, "X landed"), and a contradicted one is a FAIL.

### Step 7 — the probe gate: one run, one block

```
/handoff-verify
```
One CC-side pass over **every** `PROBES.md` row against live state, emitting **one** evidence
block the operator pastes **once**. Table order is execution order: P0 → P1 → the rest. **Any FAIL
blocks onboarding**, and a missing required row is not a pass. §2 above is what to compare the
block against — as **recognition**, not as an answer key.

Machine-side backstop, which is a different organ:
```bash
python scripts/verify_handoff_probes.py     # FAILs any probe row printing an `expected:` value
```

### Step 8 — seal

```bash
git add docs/handoffs/<slug>/
git commit -m "docs(handoff): 2026-08-08 architect bundle — <one line>"
```
Committing **is** the seal; `docs/handoffs/` is immutable from here (CLAUDE.md §5 rule 3), so
everything above happens before this line. Two organs fire on this commit:
- `verify_seal_identity` refuses a bundle whose internal `Slug` row names a different directory —
  *"Regenerate; do not hand-patch the sealed artifact."*
- the `check-seal-identity` pre-commit hook runs the same function over every staged
  `docs/handoffs/**` file.

**Expect the known unrelated failure if you run `pre-commit run --all-files` here.** The
2026-08-01 `-2` bundle fails `check-seal-identity` on every all-files sweep and cannot be edited
(prep pack §5.5). Scope the run to staged files, or expect that one red.

Then the JOURNAL entry — **not removable by ceremony tiering**, and it must name a SHA the range
introduces, because `block-unanchored-push` refuses a push to `main` whose spine entries carry no
anchor and it **fails closed**:
```bash
# JOURNAL.md: prepend the newest-first entry, with an **Anchor:** line naming ≥1 introduced sha
git add JOURNAL.md && git commit -m "docs(journal): 2026-08-08 — <one line>"
```

### Step 9 — merge and push

```bash
git checkout main
git merge --no-ff <branch>
python scripts/audit.py ship-gate
git push -u origin main
```
`--no-ff` is not optional: `block-ff-push` refuses a push that would put a non-merge commit on
main's first-parent spine, and since the ADR-85 amendment §A6 it **fails closed on internal
error**. `MERGE IS ATOMIC` — merge, push and delete the source branch are one operation
(`.claude/rules/git-discipline.md`); verify with `git branch --merged main` before deleting, and
never force-delete.

### Step 10 — the paste

Open a fresh Claude.ai chat, paste `docs/handoffs/<slug>/PASTE_THIS.md` **once** (never hand-feed
individual files to the file-less browser), read back the on-load acknowledgment line, then paste
the step-7 evidence block **once**. The browser reads the table; it does not dictate commands one
at a time.

---

## 4. What this staging pass does NOT cover, stated so it is not mistaken for coverage

| Not covered | Why |
|---|---|
| the SUPPLEMENT answers | contract-forbidden to this window; the architect authors them (§3 step 6) |
| any actual bundle | the cut binds git state; it happens on final main, locally, in the morning |
| whether `canonical_freshness`'s four stamps get re-stamped | re-stamping requires a genuine end-to-end re-read per file — an act, not a runbook step |
| the operator's machine state (worktree skeletons, armed hooks, sibling repos, `~/.claude`) | outside this container by construction; §3 step 2 is where the morning looks |
| the `Destination` row's live branch value | P3's operand, and it is whatever the morning cuts on |
| any value in §2 as an answer | they are recognition aids from a night branch; every probe re-derives |
