# Batch 4 — end-of-batch packet (the closing act)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-11 · **Slug:** `batch-4-packet`
- **Closes:** `docs/audits/2026-08-11-technical-batch-4-manifest.md` (`status: open`; its
  `closed_by:` names this exact path). Committing this file is the single act that expires the
  batch — nobody flips a flag.
- **Written by:** the primary integrator seat (CC, Opus 5), 2026-08-12, in the pre-handoff closing
  arc. Numbers computed against `main` at **`2730eb7d`**, after both night-lane merges and the
  organ-index arc.
- **Sources:** the night-1 truth audit
  (`docs/audits/2026-08-12-verification-night-1-truth-audit-and-handoff-numbers.md`) supplied
  B1/B2/B3. **Every figure was re-measured at this HEAD before being carried**, and where the
  re-measurement disagrees, the disagreement is stated rather than smoothed (§7).
- **Tag key:** **M** = measured at this HEAD · **I** = inherited, not re-derived (night-1 PRE-1
  carries the 8-entry I-list).

---

## 1 · H2 VELOCITY LINE

**The filter, named first, per H2** (*"the velocity line names the filter it was measured on"*):

```
VELOCITY (batch 4 / window 2026-08-10-11, measured 2026-08-12 on main @ 2730eb7d)

  opened      2      [#521] [#522]
  closed      3      [#270] [#132] [#521]
  net        -1
  open-total  195    filter = LIVE (status: open + status: deferred)
                     = 170 open + 25 deferred
                     narrower reading (status: open only) = 170
```

**Three independent reads agreeing (M, re-run at this HEAD):**

- `tasks/*.md` frontmatter parse → 170 open + 25 deferred + 58 closed + 1 retired + 1 superseded
  = 255 task files → **live 195**
- `python scripts/validate_backlog.py --all` → `OK (9 themes, 26 stories, 195 tasks, 1 warning(s))`
- `tasks/manifest.json` node count → **195**

**Movement vs H2's 2026-08-09 baseline (I):** 194 → **195** live (+1); 168 → **170** open (+2);
26 → **25** deferred (−1, exactly `[#117]`).

**Per-id ledger (M, every row re-read at this HEAD):**

| id | Claim | Measured `status:` | Evidence |
|---|---|---|---|
| `[#521]` | born **and** closed in-window | `closed` | born `3aaf5140`; closed `afe79c8c` |
| `[#522]` | born | `open` | born `3aaf5140` |
| `[#270]` | closed | `closed` | `679d8eca` (close + inbound-clause strip, one commit) |
| `[#132]` | closed | `closed` | `83a869e6`, merge `e624a172` |
| `[#117]` | un-parked | `open` | `64ea92bb`; peg `#270` met at `7e4d503e` |
| `[#513]` | amended, not born | `open` | `3aaf5140` rewrote its Done-when |

**Arithmetic (M):** 170 open (boot, I) **+2** born **−3** closed **+1** un-parked = **170**.
Measured **170**. Reconciles exactly.

## 2 · THREE-WAY LANE-BUCKET SPLIT

Buckets per **I-D10 G-8**: `feature/satellite` · `finish-line` · `hub-introspection`.
Cap: **≤ 1/4 of lanes may be hub-introspection**, evaluated per batch. Denominator declared:
**EXECUTED lanes** — a lane that reached a merge SHA.

| Lane | Bucket | Merge |
|---|---|---|
| W1 `[#514]`+`[#510]` | hub-introspection | `0136cec6` |
| W2 `[#270]` | feature/satellite | `c7f4fd92` |
| W5 `[#132]` | feature/satellite | `e624a172` |
| W-521 `[#521]` | finish-line (substrate, per amendment B-3) | `aafe3c8e` |
| W3 `[#513]` | finish-line | **NOT DISPATCHED** — contract pending |
| W4 conversions | finish-line | **NOT DISPATCHED** — id-gated (A-2) |
| W6 arch-soft-obs | hub-introspection | **DROPPED** (A-1) |

```
  feature/satellite   2 of 4   =  50.0%   (W2, W5)
  finish-line         1 of 4   =  25.0%   (W-521)
  hub-introspection   1 of 4   =  25.0%   (W1)

  Cap check (G-8): floor(4/4) = 1 permitted; 1 occupied.  WITHIN CAP, AT THE LINE.
```

**Stated plainly, because a cap passing is not the same as a cap holding:** it passed at the line
**only because W6 was dropped**. At the dispatched width of 6 the manifest itself recorded
**2 hub lanes against a permitted 1** — an overage cleared by roster change (A-3), not by
conformance.

**Cross-window split for batches 1–3: DECLARED ABSENT, not estimated.** G-8 — the ruling that
created the three-way split — was made at the batch-4 GO on 2026-08-11, and buckets are declared
ex-ante per batch. Batches 1–3 were dispatched before the vocabulary existed; retro-assigning
buckets would be an invented cell. Batch 4 is the only batch dispatched under G-8, so **the cap has
been evaluated exactly once.**

## 3 · SURVIVAL & QUOTA

### Birth ledger, with both cap-defence lines

```
  BIRTHS THIS WINDOW: 2        [#521], [#522]
  AMENDMENTS-IN-LIEU: 1        [#513]  (the exemption resolved as an amendment;
                                        double-birth stopped PRE-birth)
  NON-BIRTHED WITH REGISTER DISPOSITIONS: >= 2   (I-D8 drive-by; I-D9 deferral)

  CAP DEFENCE, LINE 1 - adjudication class:   3 (ARC-2) / 0 (ARC-4)          [I]
  CAP DEFENCE, LINE 2 - execution class:      5.67 avg / 8-in-batch-3        [I]
  BATCH-4 ACTUAL:                             3 closes at width 4            [M]
                                              [#270] [#132] [#521]
                                              -> consistent with the EXECUTION-class line
```

### AM-4 / AM-5 and the dispatch surface

- **AM-4 — VISIBLE = DISPATCHED.** Repo law at `0094b09a`, merged `ea4ddf23`; register
  `STANDING_RULINGS` **B7**.
- **AM-5 — a nested session carries no Agent View row, so the operator dispatches.** Ruling
  `dcafcb51`, merged **`5259b0f0`**.
- **Dispatch is a PATH command — `win-tooling@fb52bf6`** *(cross-repo SHA, named as one)*. The
  mechanism class changed from a dot-sourced profile alias to a file on PATH. Four failures in five
  hours were **one wrong mechanism class, not four bugs**. **PLAYBOOK Ch8 still described the alias
  route, and this arc corrected it** (`10822b09`): the section claimed `dispatch` was "live in every
  branded terminal", which no dot-source route ever achieved — profile args reach 1 of 8 terminal
  types, `CurrentUser $PROFILE` sits inside the OneDrive exclusion zone and cannot be written at
  all, and `$PROFILE.AllUsersAllHosts` needs an elevation no agent can perform.

### Register confirmations

| Item | Confirmation |
|---|---|
| `[#430](b)` | Deferred **with direction**: subject-scoped severity over pinned snapshots; to be ruled as ADR input, not inherited as decided. `status: open` |
| `[#491]` Gemini leg | Owned and **gated** — fan-out is RETRIEVAL ONLY; admission runs through the seeded-defect corpus, **which does not exist**. `status: open`, blocked |
| `[#492]` Grok | `status: deferred`, dated re-check **2026-08-17** — also gated behind the absent corpus |
| win-tooling S-list (G3) | Remote **landed** (`https://github.com/rdwornik/win-tooling.git`). Privacy not probed from here |

---

## 4 · WINDOW-CLOSE ITEMS

### 4.1 The VS Code incident and its repairs — **CLOSED during this arc**

Every `Ctrl+`` terminal in VS Code lost `claude` / `oh-my-posh` / `dispatch` while Windows Terminal
stayed healthy. The asymmetry localised the fault: a shell outside VS Code reads no VS Code
settings. Repaired in `win-tooling`, merged **`win-tooling@1f8b300`** (commit `7e3648d`), pushed.

- **Root cause — a settings key, and it was NOT ours.** `terminal.integrated.env.windows` carried a
  `"Path"` member: `"C:\\Program Files\\Git\\cmd;${env:Path}"`. A `Path` member there **REPLACES**
  the terminal PATH, and the `${env:Path}` substitution is the only thing putting the inherited PATH
  back. Reproduced exactly — with the literal unsubstituted, all three commands miss at once.
  **The key is in every `settings.json` backup back to 2026-07-12**, predating the dispatch arc.
  That arc's four writes were **exonerated by measurement** (file parses strict JSON, 60 keys, no
  BOM, no truncation; the PATH write lost zero entries, kind still `REG_EXPAND_SZ`). The override
  was redundant anyway — `Git\cmd` is already the last entry of the machine PATH — so the key was
  **removed**, with a comment recording why.
- **PATH junk cleaned.** **26 dead `pytest-of-*` entries**; the real PATH had grown
  **1286 → 4168 chars**, cleaned surgically back to **1322 chars**, value kind preserved.
- **Isolation defect — this one WAS ours, and it is FIXED.** The applier defaults
  `-UserPathRegistryKey` to `HKCU:\Environment`; the `check_mode` and `global_profile` suites
  sandboxed everything **except that key**, so every run appended its temp deploy dir to the
  operator's real PATH. Fixed by an **autouse `conftest` tripwire** that FAILS the offending test on
  any real-key write and restores the value first, plus session teardown disposing sandbox keys.
  Hardened alongside: `-Check` treats any `^path$` member as drift (case-insensitive, so `PATH`
  cannot slip through), and flags `pytest-of-*` / nonexistent-directory PATH entries; every profile
  is launch-tested for real. **90 tests pass.**
- **Measured, not assumed:** resolution survives a 32,058-char PATH (7.7× the polluted value) — so
  the bloat was real damage but **not** a contributor to the outage.

### 4.2 The night lanes ran LOCALLY — a deviation, and it produced a near-miss

Both night lanes (`claude/night-1-truth-and-handoff`, `claude/night-2-strategy`) executed against
the **primary working checkout** rather than one worktree per lane.

**The near-miss, recorded because it nearly cost work, not because it did.** Night-1 found night-2's
untracked artifact in its own tree. Between night-1's `git add` and its `git commit`, night-2
created and checked out its branch **in that same worktree** — so night-1's commit landed on
night-2's branch and swept night-2's artifact in with it (`e436ba80`). Repaired non-destructively:
both artifacts copied to a scratchpad *before* any git operation, then `git reset --mixed` (a
`git checkout` would have deleted both), then the correct branch and a single-file commit. **Nothing
was lost.**

**Two consequences that outlive the incident:**

1. **`git add` then `git commit` is not atomic against a concurrent branch switch in a shared
   tree.** The safe shape is one worktree per lane, or a branch-identity assertion immediately
   before commit.
2. **The shared index made `audit-index-freshness` unsatisfiable from inside a lane.**
   `gen_audit_index.py` reads the *directory*, so any regen would embed a row pointing at a file
   absent from that branch. Night-1 chose a declared `SKIP=` over a wrong index or a `--no-verify`
   that would have disarmed every other gate. **That generator defect is now fixed** (§4.4): the
   index reads tracked files only, so the same regen today would be correct and the SKIP
   unnecessary.

### 4.3 The two night artifacts ride UNADJUDICATED

**`night-1` and `night-2` are DRAFTS and are merged as drafts. Adjudicating them is the incoming
seat's first order of business.** Landing them makes their content reviewable in the tree; it
ratifies nothing. Not one proposal, lesson, or governance change either lane advances has been
accepted, and nothing in either artifact was acted on beyond the relocations and fixes this arc was
explicitly ruled to perform.

What that leaves on the table, named so it is not rediscovered:

- Night-1's **FLAG-1**: the manifest's integration marker at `:398` claims `[#514]` and `[#510]`
  closed. **M, re-verified at this HEAD: both are `status: open`**, and both rows carry explicit
  self-limiting text saying so. See §5.
- Night-1's **A3 finding**: two of the brief's three GAPs already have owners — `[#420]` owns
  GAP-2's archive leg under a live *"do NOT touch `docs/archive/`"* order, and GAP-3 is a work-item
  inside an **ACCEPTED** intake (W-9(a)) with a recorded `AGENTS.md` name-collision hazard. A
  consolidation intake drafted as GAP-1+2+3 would re-derive two owned scopes — which is the exact
  failure its own brief names as the thing to avoid.
- Night-1's **A1 tally**: 8 rulings are **RECORDED-ONLY** — the register line is the whole of them
  and nothing in the tree carries them. Two are quietly load-bearing (3b-4 citation convention,
  3b-5 inherited-vs-measured), and this window then produced exactly the defects they exist to
  prevent.
- Night-2's Parts C/D/E in full.

### 4.4 The ORGAN-INDEX relocation and the new-path guard

Operator ruling A of 2026-08-11, executed 2026-08-12; register `protocols/STANDING_RULINGS.md`
**K-1**. `docs/ORGAN-INDEX.md` → **`ecosystem/organ-index.md`** (`98d50e78`).

**The breach it corrects:** `docs/` is a Tier-2 **genre** tree (ADR-101 §1) whose members live in
`docs/<genre>/`, and the organ index is none of the five genres. It is generated ecosystem state —
the same class as the `ecosystem/organ-registry.yaml` it reads. It was the only file that ever sat
loose at the `docs/` root.

**How it got there is a gate-shape finding, not an authoring slip.** ADR-101's refusal gate reads
the top level and the `docs/<genre>/` level and stops. A file loose at `docs/` introduces no new
top-level entry and no new genre folder, so Rule A was silent **by its own literal spec** — and the
suite carried a test asserting exactly that silence.

**So the class was closed, not the instance.** `validate_hermetization.py` gains **Rule C**: an
added file whose home directory is outside an allowlist derived from the live taxonomy is refused
with *"new path outside allowlisted homes — operator approval required"*. Rule A's reading is left
exactly as it was and its test is kept, now paired with a Rule C assertion — re-interpreting an
existing rule to cover a case it was never written for is how a gate stops being checkable. A
live-tree test asserts Rule C refuses **none of the 2054 currently-tracked paths**.

**Honest limit, carried into both roster rows:** Rule C polices the HOME of an added file, and the
two open homes (`docs/handoffs/**`, `tests/fixtures/**`) admit arbitrary depth by design.

Also in the same arc: `gen_audit_index.py` gains the tracked-files filter (`0258a1dc`), applying
W5's `d5b19a2d` F1 fix to its twin; and **one terra review pass** over the combined code diff
(tally **0/1/1/0**, artifact `docs/audits/2026-08-12-codex-closing-arc-organ-index-guard.md`) found
that an untracked **symlink** walked straight back through that filter — the same defect through the
one door left open. Reproduced, fixed, re-verified, pinned (`0fba1be1`).

### 4.5 OPEN RULING CARRIED — the I-D6 working-set reading

**This is an operator decision, filed rather than adjudicated, and it gates the
consolidation-intake filing.** I-D6 defines the working set as **SEED / DRAFT / READY** and asserts
the GO *"takes the working set to 0"*. The BRIEF one day later applies a **DRAFT-only** reading
(*"Ceiling has room (3/6 DRAFT)"*). These are not reconcilable by evidence; they are two different
rules.

**M, at this HEAD** (`docs/intake/*.md` frontmatter — byte-identical to the `9b2a6559` night-1
measured against, so this is not tree movement):

```
  SEED 10 · DRAFT 3 · READY 1  ->  definition-reading   14   (ceiling 6 -> 8 OVER)
                                   applied reading       3   (within ceiling)
                                   the two readings differ by  11
```

**A ceiling that cannot be evaluated is not a ceiling** — which is I-D6's own stated reason for
adopting reading R1 over R2. Until this is settled, *"are we over?"* is unanswerable from the tree,
and any consolidation intake filed against the ceiling is filed against an undefined denominator.

---

## 5 · THE CLOSURE CONTRACT, ANSWERED HONESTLY

The manifest's **closure contract item 3** names five rows to be closed with ADR-65 evidence before
the batch closes: `[#514]` `[#510]` `[#270]` `[#513]` `[#132]`.

**M, at this HEAD:** `[#270]` **closed** · `[#132]` **closed** · `[#514]` **open** · `[#510]`
**open** · `[#513]` **open**.

**Three of five are open, so this packet does NOT claim item 3 discharged.** Batch 4 closes on the
three rows that did close (`[#270]`, `[#132]`, `[#521]`), with the other three recorded as
**CARRIED** — each by the lanes' own honest declaration:

- `[#514]` — leg 3 discharged in W1 (`92d735a7` + `ffc32099`); **leg 1 explicitly NOT discharged**
  ("the row's own `git branch --show-current` / `KIND_UNKNOWN` BLOCK is unbuilt").
- `[#510]` — W1 PARTIAL at `1c6d4255`; the self-grant is **narrowed, not closed**; all four roster
  legs stand.
- `[#513]` — amended, not discharged; its rewritten Done-when is mechanically testable and unmet.

**The manifest marker at `:398` is wrong, and the correction route is an appended amendment marker
(form A-4), not an edit** — `docs/audits/` is immutable. That marker is **owed** and is named here
so it is not discovered later. This packet is the honest record; the manifest is the artifact still
carrying the false claim.

---

## 6 · STATE AT CLOSE (M, at `2730eb7d`)

```
  main                     2730eb7d  (pushed)
  audit.py health          OK
  canonical_freshness      OK - 9 canonical living files fresh
  journal_spine_anchor     OK - every first-parent spine entry above floor 24882f8cc anchored
  silent_rule_ratchet      440 <= 441  (1 below baseline, UNMOVED by this arc)
  doc_claims               OK - 3 doc self-claims match repo state
  fleet_audit_replication  OK - automation/fleet-audit replicated, 0 commits ahead
  worktrees                primary only (0 linked)
  git stash                empty
  suite                    1 failed / 2856 passed - the [#426]-class RED only
  bypasses used this arc   NONE (no --no-verify, no SKIP=, at any point)
```

**The one standing RED, named:**
`tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row` — it expects
"1 declared routine row" and live reads 2. This is the **[#426]** retrofit class, not a regression
from this window.

**Standing WARNs, all dispositioned or advisory:** the `undeclared_edges` prose-edge family
(`[#241]`); `no_ff_merges` (three legacy June commits — never rewrite them); `doc_rot`
history-accretion on the large rows plus the `CLAUDE.md` file-budget (202 lines against a
self-declared 200 — this arc's §12 entry grew it further); `reconciled_versions` on a malformed
template edge; `preflight_backlog_ids` (advisory per `[#483]` R3); `review_artifact_coverage`
(advisory per `[#480]` P3).

**Branch hygiene, reported rather than claimed:** the two integrated night lanes are deleted local
and remote. **Five `claude/*` origin satellites remain and were NOT deleted** — each carries
unmerged commits (6 in total), ruling **3c-5** defers their census with an owner, and deleting
unexamined work needs operator word. They are `claude/nc-lessons-mechanisms-jw5dda`,
`claude/nd-governance-promotion-prune-77qc6b`, `claude/night-nb-handoff-prep`,
`claude/night-ne-northstar-value`, `claude/window-truth-audit-yr83j2`.

---

## 7 · CORRECTIONS TO THE SOURCE THIS PACKET WAS BUILT FROM

Recorded rather than silently absorbed, because this packet's own claim is that it re-measured.

1. **Night-1's I-D6 box undercounts SEED by one.** It reports *"SEED 9 · DRAFT 3 · READY 1 → 13
   working intakes"*. **M: SEED 10 · DRAFT 3 · READY 1 = 14**, and `docs/intake/` is byte-identical
   to the `9b2a6559` it measured against (`git diff 9b2a6559..HEAD -- docs/intake/` is empty), so
   this is a counting error, not tree movement. The consequence is not cosmetic: the
   definition-reading is **8 over** the ceiling of 6, not 7, and the two readings differ by **11** —
   which is the figure the carried ruling states.
2. **Night-1's A2 finding stands and is now acted on.** It found `fb52bf6` presented as a hub SHA
   when it is a `win-tooling` SHA. Every citation of it in this packet is written
   `win-tooling@fb52bf6` and flagged cross-repo, and PLAYBOOK Ch8 was corrected the same way — which
   is the 3b-4 citation convention applied at the sites edited, though 3b-4 itself is still
   RECORDED-ONLY and its ruled home in PLAYBOOK has still not received it.
3. **The VS Code repair is no longer in flight.** Night-1's B4 recorded it as "designed, partly
   committed, and NOT verified applied". It merged at `win-tooling@1f8b300` **during this arc** and
   is pushed; §4.1 is written from the landed commit, not from the plan.
4. **Night-1's ARCHITECTURE observation was incomplete.** It flagged `ARCHITECTURE.md:227` as stale
   on its own terms. The end-to-end re-read this arc performed found **two further defects** in the
   same file: §Validators described `validate_hermetization` as Rule A + Rule B only, and the
   pre-commit gate list was missing `organ-index-freshness` (seventeen of eighteen). All three are
   fixed.

---

**Batch 4 is CLOSED by this packet** — three closes at executed width 4, with `[#514]`, `[#510]`
and `[#513]` carried, one manifest amendment marker owed, and the I-D6 ruling open for the
operator.
