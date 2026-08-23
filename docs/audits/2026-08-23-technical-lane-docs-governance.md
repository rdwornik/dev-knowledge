# LANE-DOCS — governance-drift discharge: ARCHITECTURE.md · CLAUDE.md · VISION.md

<!-- scope: meta -->

**Lane:** `lane-docs-governance` · branch `worktree-lane-docs-governance` · effort high
**Base:** `19476e3f` (main tip at lane boot) · **Repo:** `.dev-knowledge`
**Sole owner this batch of:** `ARCHITECTURE.md`, `CLAUDE.md`, `VISION.md` — the three
freshness-gated collision files, which is why one lane owns all three.

**Inputs (binding):** `docs/audits/2026-08-21-fresh-eyes-cloud-r1-governance-drift.md`
(verdict tables A/C/V, the M-lines, the top-10) and
`docs/audits/2026-08-21-fresh-eyes-cloud-r3-conformance.md` **F2** (the `[#171]` leg-2
pointer). Architect rulings carried in: top-10 items **8, 9, 10 = YES as written**;
`[#171]` leg 2 = the ARCHITECTURE Ch2 pointer to `ecosystem/conformance.md` (reading R-A).

> **Locator note, and it is not a formality.** Every `:NNN` in R1 was measured against
> `78267fd` on 2026-08-21. Main has advanced substantially since — read the distance off
> `git log --first-parent --oneline 78267fd..main`, not off this sentence (an earlier draft
> of this line said "four times" against a live 30, which is **M2 caught inside the artifact
> that lands M2** — corrected here rather than quietly). **Every site below was
> re-resolved by anchor text against the live tree before it was edited** — which is M1,
> the audit's own top finding, applied to the audit. It changed the work twice (items 4
> and 6) and corrected the audit once (A6).

---

## 0 · What the preflight changed before any edit was made

R1 is a good audit measured against a tree that has since moved. Four of its
recommendations did not survive contact with live state:

| R1 said | Live on 2026-08-23 | Consequence |
|---|---|---|
| **item 4** — ARCHITECTURE lacks the ADR-113 bullet | **Already landed.** `9debc348` (2026-08-22) added it; live at the Governing-ADRs tail | **No act taken.** Executing it would have been a duplicate bullet. Reported, not performed |
| **item 5** — Ch2 gate list is "18 of 19"; add `block-commit-on-main` | List names **18**; `.pre-commit-config.yaml` declares **21** (`lane-contract-check` and `provider-registry-agreement` landed after R1) | The literal fix would have landed **19-of-21** — a knowingly-false claim and a *fourth* recurrence. Took R1's **second written option** instead (§2) |
| **A6** — replace `validate_doc_claims.py:225-236` with `:224-240` | `_CLAIMS = [` is at **224**, its `]` at **239** | R1's own replacement locator was **off by one**. Landed `:224-239`. M1 catching M1 |
| **A15** — `UNVERIFIABLE-IN-CLONE`; operator must check the stamp on a full clone | `git log --no-merges -1 -- ARCHITECTURE.md` → `9debc348`, **2026-08-22**; `last_reviewed` was **2026-08-22** | **Premise refuted.** The stamp did NOT lag, so `canonical_freshness` was NOT failing. The re-stamp here is owed to *today's* edits, not to a pre-existing lapse |

---

## 1 · Per-item before/after

### Item 1 — C1: `BACKLOG.md` is GENERATED (CLAUDE.md §4) · {SAFE-MECHANICAL}

R1's highest-operator-impact finding: CLAUDE.md was the one surface of three still
telling the executor to hand-edit a file generated since 2026-07-28.

- **Before:** `Living: VISION.md, ARCHITECTURE.md, CLAUDE.md, protocols/*.md, BACKLOG.md (update in place).`
- **After:** `Living (update in place): VISION.md, ARCHITECTURE.md, CLAUDE.md, protocols/*.md.` **`Generated: BACKLOG.md`** — never hand-edit it; edit `tasks/`, then `python scripts/gen_task_tree.py --emit-source` (ADR-107 §7.2, `[#439]`, 2026-07-28; `audit.py::check_task_tree_coherence` gates it).
- **Cost:** 0 net counted lines (in-place rewrite), as R1 priced it.

**Second site, found by this lane's re-read and fixed:** `ARCHITECTURE.md` Ch5's
File-lifecycle table carried the *identical* falsity — `| Living | … BACKLOG | update in
place |` — twenty lines above Ch5's own source-zone prose that states the flip correctly.
R1's C1 asserts *"ARCHITECTURE Ch5 and PLAYBOOK both state the flip correctly — CLAUDE.md
is the only one of the three"*; that is true of Ch5's **prose** and false of Ch5's
**table**. ARCHITECTURE now carries a `Generated` row.

### Items 2 + 3 — the `audit.py` "read-only" claim · {SAFE-MECHANICAL} · discharges `[#558]`

`[#558]` closed 2026-08-18 with a Done-when demanding *"a fleet-wide re-measurement of the
claim covers files beyond `CLAUDE.md`"*. **That re-measurement was never run** — which is
why R1 found sites four and five three days later. This lane ran it: repo-wide
`grep -rn --include=*.md` over the living-doc set, not a per-file sweep.

| Site | File | Before | After | Found by |
|---|---|---|---|---|
| 4 | `ARCHITECTURE.md` Purpose | "…templates, and **read-only validators**; it prescribes conventions…" | "…**hub-local validators, generators and gates**… **What Layer 2 may not do is drive a CHILD repo's state** — the prohibition is on siblings (invariant 2 is the checkable form)" | R1 **A2** |
| 5 | `VISION.md` Audit support | "`ship-gate`/`checks` commands, **read-only**)" | "It is **read-only on siblings** — the ADR-36 invariant, and the checkable one — **not read-only on this repo**: it writes findings, pushes to `origin` (`audit.py:3967`) and commits Routine output to `automation/fleet-audit`" | R1 **V1** |
| **6** | `ARCHITECTURE.md` Authority §Enforcement model | "Centralized, **read-only** `scripts/audit.py`" | "Centralized `scripts/audit.py` — **read-only on siblings**" | **this lane** |
| **7** | `ARCHITECTURE.md` §Validators, `audit.py` bullet tail | "**Read-only**; hub-only organs no-op on children" | "**Read-only on siblings, not on this tree** — `health`/`ship-gate` write findings, `_replicate_automation_branch` pushes to `origin` (`audit.py:3967`), `_commit_routine_outputs` commits to `automation/fleet-audit`" | **this lane** |

**Sites deliberately NOT edited, with reasons:** `ARCHITECTURE.md` invariant 2 (already
correctly scoped to siblings — it is the wording everything else now converges on);
`ARCHITECTURE.md` Governing-ADRs "read-only auditor" (a summary of what ADR-31/36
*decided*, not a claim about live code — editing it would misreport an immutable ADR);
CLAUDE.md §10 "validators only, no scripts that drive state in child repos" (already
accurate as scoped); CLAUDE.md §12 (a record, not edited backwards — the v2.56/B6
precedent R1 itself cites at C14); `protocols/PLAYBOOK.md:1400` and `:1790` (both already
scoped "w.r.t. child repos" — **and `protocols/` is on this lane's never-touch list**).

> **The reusable finding, and it is the audit's own M3 landing on the audit.** `[#558]`
> declared this claim fixed at **0 sites** after a sweep scoped to `CLAUDE.md`. R1 then
> found sites 4 and 5 by widening to three files. This lane found sites **6 and 7** by
> widening to *the whole of one of those files* — both inside `ARCHITECTURE.md`, the file
> R1 reported as holding exactly one. **A sweep scoped to the sites a prior sweep named
> will keep reporting zero**, at every level of the recursion.

### Item 4 — the ADR-113 bullet · NOT PERFORMED (already landed)

Landed by `9debc348`, 2026-08-22, after R1's measurement. Verified live. No act.

### Item 5 — `block-commit-on-main` / the Ch2 gate enumeration · **DEVIATION, taken deliberately**

R1's A6-row fix reads, verbatim: *"Add `block-commit-on-main`; **or delete the enumeration
and keep only the pointer the sentence already carries**."* **This lane took the second
option.** Stated plainly because the contract's gloss named only the first.

**Why.** The list named 18; live is **21**. Adding one id lands 19-of-21 — still false, and
the *fourth* recurrence of a defect the sentence's own parenthetical already records three
times (sixteen-of-seventeen 2026-08-03→08-10; seventeen-of-eighteen 08-11→08-12; now
eighteen-of-twenty-one). The sentence simultaneously claimed *"the roster is not re-counted
here"* **while re-counting it**. And this same lane lands **M2** ("never restate a count or
roster in prose") into CLAUDE.md §4 — restating a corrected roster in the same pass would
contradict the rule at the moment of writing it.

**Supporting precedent, checked not assumed:** no `_CLAIMS` entry is coupled to
ARCHITECTURE's gate list (`validate_doc_claims.py:224-239` — claim 2b holds **CLAUDE.md
§9**, which *is* gate-protected and *is* correct, R1's own C7 control case), and
`validate_doc_claims.py:219-222` records that counts were **deliberately moved off
ARCHITECTURE.md** by `[#222]` for exactly this reason. Nothing reads the deleted list.

- **After:** the enumeration is replaced by a pointer to the three surfaces that hold it
  (`.pre-commit-config.yaml` · `ecosystem/doc-counts.md` · CLAUDE.md §9), plus the facts
  the pointer *cannot* carry: the **three git stages** and the one-time
  `pre-commit install --hook-type pre-push`. The three-recurrence history is kept as the
  recorded *reason*.
- **`block-commit-on-main` is still named** — in the `always_run` paragraph below it, which
  had *also* been wrong (it listed two always_run pre-commit hooks; live is three). That is
  where naming it is load-bearing: it is what refuses an edit to that file on `main`.

**Reversibility:** one hunk. If the architect wants the enumeration back, restore it and
add three ids.

### Item 6 — the `[#171]` Ch2 pointer (R3 **F2**) · {SAFE-MECHANICAL} · **row NOT closed**

- **Before:** `ecosystem/conformance.md` appeared in ARCHITECTURE **once**, in the
  ADR-85/86/87 Governing-ADRs bullet — the wrong chapter, as F2 records. Ch2: nothing.
- **After:** a Ch2 note pointing at `ecosystem/conformance.md` (+ its HTML sibling),
  naming what it answers (*does the repo currently match what it claims about itself*)
  against what the organ index answers (*what exists*) and what Ch2's table answers
  (*what happens when it says no*). ADR-86 §3 required exactly this, "with the build, not
  before"; the build has shipped.

**`[#171]` IS NOT CLOSED, and the Ch2 note says so on the page.** The contract anticipated
a flip (*"flip the row via `gen_task_tree --emit-source` only if no seat has; otherwise
report it"*). No seat has — and the row still should not flip, for a reason the contract
could not have known:

> `tasks/171-…md` Done-when: *"`ecosystem/conformance.md` is generated **+ committed** by
> a read-only validator (Layer-2-safe) **and** ARCHITECTURE Ch2 carries the pointer"*.

Leg 2 is discharged by this commit. **Leg 1 is not, and no code path performs it** —
verified live, not carried from R3: `gen_dashboard.py::write_outputs` (`:1193-1200`) writes
two files and returns `0`; `main` has no commit path; the sole `subprocess` site is
`GitReader` (`:236-250`), which reads. Both artifact faces nonetheless assert *"Generated,
committed, read-only"*. That is R3 **F3**, a P1 whose disposition is an architect choice
between (a) implement the ADR-80 writer policy or (b) rule that human-committed satisfies
"committed" **and amend ADR-86 §2 plus the two artifact strings**. R3 says *"Do not leave
(c)."* Closing the row today would be leaving (c).

Two further live facts recorded on the Ch2 note as honest limits: the dashboard is
HEAD-pinned and **nothing gates it** (`--check` exists and is armed nowhere — the lone
ungated committed-generated surface here; R3 **F5**), and it is currently stale against
HEAD (**F4**).

### Item 7 — locator repairs · {SAFE-MECHANICAL}

| Locator | Before | After | Evidence |
|---|---|---|---|
| Ch2 `fleet_health.py` throttle | `fleet_health.py:82` | `fleet_health.py:156` | `:82` is a comment about a result-set ceiling; `return d != date.today()` is at `:156` |
| §Validators `_CLAIMS` | `validate_doc_claims.py:225-236` | `validate_doc_claims.py:**224-239**` | `_CLAIMS = [` at 224, `]` at 239. **R1 proposed `:224-240` — itself off by one** |

**Checked and left alone:** `fleet_health.py:610,642,689` and `fleet_parity.py:123` all
still resolve exactly (R1 **A19**), confirming its observation that the most recently
added locators are the ones that hold.

### Item 8 — Ch2's completeness claim → the organ-index pointer · {RULED YES}

- **Before:** two completeness claims — the chapter opener (*"The behavioural inventory:
  every enforcement/awareness organ…"*) and the table preamble (*"Every
  enforcement/awareness organ, with its trigger…"*) — over a hand table of **35 rows**,
  against a generated index of **eight classes** that Ch2's own note calls its *"verified
  source"* and says to trust on disagreement. Whole classes absent: `agent`, `rule`,
  `plugin`.
- **After:** both claims retired. Ch2 declares itself **curated, not an inventory**, points
  at `ecosystem/organ-index.md` for *what exists and what fires it*, and **keeps the
  failure-posture column** — which the index states **in its own header** that it cannot
  carry ("a judgement about an organ's code, derivable from no frontmatter block or hook
  id"). A row's absence now means *posture not yet recorded here*, never *organ does not
  exist*.
- The note above the table had already licensed exactly this (*"may be replaced by a
  pointer to it"*). Per M2, **no count was restated** in the replacement text.

### Item 9 — PLAYBOOK Ch8 + the execution substrates · {RULED YES}

**Precondition verified first, as instructed:** `git show main:protocols/PLAYBOOK.md` →
`## Ch8. Session boundaries` at `:1236`, live on `main`. Confirmed before writing the
pointer.

- **ARCHITECTURE** "How to read this doc" gains: the daily working mode — parallel worktree
  lanes, dispatch, the ADR-110 batch protocol — is **PLAYBOOK Ch8**, which this map
  referenced **nowhere** (`grep -c "PLAYBOOK.*Ch8\|Session boundaries"` → 0) despite a
  JOURNAL that is overwhelmingly lane work. Ch2 rows the organs that police it; Ch8 holds
  the procedure.
- **CLAUDE.md §3** gains the same pointer (item 9 as written names CLAUDE.md too), at 0 net
  counted lines — appended to the existing chapter-pointer sentence.
- **ARCHITECTURE Ch4** gains an **execution-substrates** block: `.devcontainer/` and
  `deploy/lived_sandbox/`.

> **Shape decision, stated.** These are **not** a sixth channel row. Ch4's table is
> *carriage* — what travels to a consumer; nothing is carried through either of these.
> They are *venue* — where a session runs when it is not the primary checkout. Adding them
> as channel rows would have falsified the "Five distribution channels" sentence and
> restated a count (M2). They are what makes Ch4's existing *"inert by design in a fresh
> cloud clone"* bullet concrete: shallow clone, hooks unarmed, `uv` pin unsatisfiable.

Both verified from source rather than from R1: `.devcontainer/` holds **four** files (R1
and the ADR-101 amendment both say two — the amendment predates `Dockerfile` and
`provisioning.yaml`; all four sit at one level, so Rule C still admits them — **noted, not
acted on**: ADR-101 is immutable and `scripts/` is off this lane's list).
`lived_sandbox` was read from its own docstrings: an operator-invoked deterministic
observer that spawns a headless `claude -p` under an isolated `CLAUDE_CONFIG_DIR` inside a
`mkdtemp` clone and verdicts enforcement-**in-effect** from transcript events, hook stdout
and git state — never narration. Ch3's axis table has no cell for that shape; **recorded
as the honest gap rather than smoothed over.**

### Item 10 — CLAUDE.md budget + M1/M2/rule-7 · {RULED YES}

**Budget arithmetic**, measured with the file's own checker
(`validate_doc_rot.scan_file_budget`, which excludes comment-only lines):

```
 197  headroom  3   start  (NOT the 198 R1 measured, NOT the "headroom 4" v2.64's bullet claims)
 197  headroom  3   + C1 rewrite ...................... in-place, 0 net
 197  headroom  3   + SS3 PLAYBOOK-Ch8 pointer ........ in-place, 0 net
 198  headroom  2   + M2 line ......................... +1
 199  headroom  1   + M1 line ......................... +1
 199  headroom  1   + SS5 rule-7 re-scope ............. in-place, 0 net
 193  headroom  7   - condense v2.59 / v2.60-v2.62 / v2.63 to git ... -6 (3 bullets + separators)
 195  headroom  5   + the v2.65 SS12 bullet ........... +2
 195  headroom  5   FINAL       scan_file_budget: clean
```

Three bullets condensed rather than the minimum two, per v2.64's ruling that the file
*"buy real headroom rather than shaving under the cap"*; destination is the git pointer,
per ADR-49 / ADR-65 §1 and the v2.59/v2.62/v2.64 precedent. No content lost — all three
recoverable verbatim via `git log --follow -p -- CLAUDE.md`.

**What the freed budget bought:**

| Line | Home | Text (abridged) |
|---|---|---|
| **M2** | §4 | *Never restate a count or roster in prose* — cite the surface that computes it; ARCHITECTURE Ch2's gate list proved it three times |
| **M1** | §4 (**not §10** — see below) | *Resolve a locator before you act on it* — run `/preflight`; the audit's own replacement locator was itself off by one, so the rule binds the auditor too |
| **C1** | §4 | `BACKLOG.md` → Generated (item 1) |
| **rule 7** | §5 | re-scoped to record the `.claude/rules/` carve-out |

**§5 rule 7 — before/after.** Before: *"No executable rules in this repo — those go in
`~/.claude/` with `verify:` lines"*, which forbade at §5 precisely what §9 rosters
approvingly. After: `~/.claude/` named as the fleet-wide home, plus the recorded carve-out
that `.claude/rules/` **is** a live repo-local rule home (`git-discipline.md`: three
`verify:` lines and two standing operator orders — MERGE IS ATOMIC, WORKTREE TEARDOWN IS
TWO BRANCHES). Re-scoped on the v2.61 rule-4 precedent: converge on the accurate site.

---

## 2 · The one instruction this lane did not execute where it was told to

**M1 was contracted for §10. It landed in §4.** Stated here, in the §12 bullet, and in the
lane report, because a silent relocation is worse than the drift being fixed.

`CLAUDE.md` §10 is a **HUB-single-sourced Form-A region** —
`<!-- methodology:start id=antipatterns-universal owner=hub -->`, whose reader-visible
header says *"single-sourced from the hub; do not edit these lines here."* The binding
constraint is byte-parity: `scripts/boundary_headers.py:18-21` records that region bodies
*"stay byte-identical to the `templates/claude-regions/*.md` extracts, preserving the
v2.39/v2.42 byte-match discipline"*, and the satellite-onboarding census runs a
`BYTE-MATCH PASS: 8/8` check across all eight hub regions.

Consequences, both checked:

1. Editing §10 alone **breaks fleet byte-parity** across every consumer CLAUDE.md.
2. `templates/claude-regions/antipatterns-universal.md` is the surface that actually
   **carries** the rule to consumers — so a §10-only edit would mean the rule never
   reaches one. That template is **outside this lane's contract** (*"nothing beyond the
   three files + their generated fragments + the artifact"*) and is inside
   `silent_rule_ratchet`'s scope (`protocols/*.md`, `templates/**/*.md`,
   `ecosystem/*.yaml`), while the three lane files are **not** — verified via
   `silent_rule_detector._in_scope`.

So: land it correctly in a repo-owned section, or break parity, or drop the rule. **Took
the first.** §4 is a coherent home — M1 and M2 are one pair (do not trust a typed-in value;
resolve or cite the surface).

**Owed, and not taken by this lane:** if M1 is meant to be a *universal* anti-pattern, it
still needs a lockstep act editing §10 **and**
`templates/claude-regions/antipatterns-universal.md` in the same commit, with the ratchet
baseline considered. That is a one-commit follow-up for a lane whose contract permits both
files.

---

## 3 · Freshness stamps

| File | `last_reviewed` before | Last non-merge touch | After | Basis |
|---|---|---|---|---|
| `ARCHITECTURE.md` | 2026-08-22 | `9debc348` 2026-08-22 | **2026-08-23** | **A15 premise refuted** — the stamp did not lag. Re-stamped for *today's* edits, licensed by a genuine end-to-end re-read from disk (all six chapters + Governing ADRs), which is what found sites 6/7 and the Ch5 table |
| `CLAUDE.md` | 2026-08-22 | `66a2786e` 2026-08-22 | **2026-08-23** | Genuine full-file re-read, all 12 sections; the re-read is what surfaced the §10 region constraint above |
| `VISION.md` | 2026-08-18 | `82fb0363` 2026-08-18 | **2026-08-23** | Genuine full-file re-read (190 lines) |

`canonical_freshness` verified OK in the live pre-commit run.

---

## 4 · Found, reported, NOT acted on

Each is out of this lane's contract, or needs a ruling. None is swept.

- **R3 F3 — `[#171]` leg 1** (P1): the generator claims to commit its own output and has
  no commit path. Blocks the row's close. Needs the architect's (a)/(b) choice.
- **R3 F5 / F4** (P2): the dashboard's `--check` is armed nowhere — the lone ungated
  committed-generated surface — and the committed artifact is stale against HEAD.
  `.pre-commit-config.yaml` is on this lane's never-touch list.
- **R1 A17** (Ch6, *"currently 15 open, newest 2026-06-25"* GitHub Issues): still
  unverified. This lane exercised no `gh` reach. **Deliberately not restated at a guessed
  value** — that is the failure class it already is. R1's own fix (re-point at a computed
  surface) stands as the right act for a lane that can reach Issues.
- **R1 V4 / V5 / V6** (VISION MISSING-COVERAGE — ADR-109 registry authority, the four
  absent References, the mixed `docs/archive/` genre): **not in the top-10**, so outside a
  contract scoped to items 1–10. All three remain valid.
- **R1 C3 / C5 / C6** (CLAUDE.md MISSING-COVERAGE — no agent/workflow class, `tasks/` +
  `ecosystem/` absent from Critical paths, no off-machine session-start variant): not in
  the top-10. C5 costs **0** counted lines and C3 costs 1; headroom is now **5**, so all
  three are affordable in a follow-up.
- **ADR-101's `.devcontainer/` amendment says "two files"**; four are tracked. Harmless
  (all at one level, Rule C admits them) but the ADR prose and
  `validate_hermetization.py:169-171`'s comment both under-count. ADR immutable;
  `scripts/` off-list.
- **ARCHITECTURE Governing-ADRs tail out of numeric order** (110, 111, 109, 112, 113) —
  already recorded as knowingly-left by the 2026-08-22 pass; reflowing would bury this
  diff.
- **CLAUDE.md §10's AGENTS.md anti-pattern** is false doctrine after ruling A2. Owned by
  `[#577]` *"in the same commit"* as the file it describes — **and** it sits in the hub
  region this lane may not touch. Two independent reasons it stands.

---

## 5 · Gate evidence

Docs-only lane: **no terra owed**. Generators run, never hand-synced.

Five commits, each through the **full gate stack, no `SKIP=`, no `--no-verify`**:

```
6c0f3d0a  docs(architecture): R1 SAFE-MECHANICAL findings + 3 the audit missed
1ba75e1f  docs(architecture): retire Ch2's completeness claim; substrates + Ch8
ba08b0ea  docs(vision): re-scope the audit.py "read-only" claim -- 5th site [#558]
24637487  docs(claude): BACKLOG.md is GENERATED -- kill the hand-edit instruction
8025aa94  docs(claude): condense section 12 to git; spend it on M1 + M2 + rule 7
```

`audit-health` **Passed** on every one; `block-commit-on-main`,
`validate-hermetization`, `codemap-freshness`, `normalize-dated-headers`,
`backlog-id-on-close` and `backlog-filing-backpressure` all fired and passed.
`canonical_freshness` green with all three re-stamps.
`validate_doc_rot.scan_file_budget('CLAUDE.md', …, 200)` → **clean at 195**.

### The inherited blocker, and the mechanism that made waiting futile

Not this lane's defect, recorded because the diagnosis is reusable.

`audit-health` FAILed on `journal_spine_anchor` for merges the concurrent
`worktree-lane-562-local` session was landing on `main` while this lane edited —
`3832f2b4`, then `21fd20fd`, then `79e90dee`, then `4881383c`. Every commit here was
refused for ~50 minutes.

**The first instinct — wait for the sibling to journal — could not have worked, and the
reason is a genuine asymmetry inside the check.** `audit.py::check_journal_spine_anchor`
walks `git log --first-parent **main**` but sources its JOURNAL text from
`journal_anchor.journal_text(repo)` with `rev=None`, which reads **the working tree**
(`journal_anchor.py:116-127`; the docstring states the split deliberately — the pre-push
organ reads the pushed tip, the audit backstop reads the working tree "which is what a
ship-gate run is judging"). A lane worktree pinned at its base commit therefore evaluates
**main's advancing spine against its own frozen JOURNAL**. The sibling *did* journal —
entry (e) on `main` carries `**Anchors:** 1f2d68fb` — and the count still rose from 1 to 4,
because none of those entries existed in this tree.

**Resolution taken:** `git merge --ff-only main`. Safe and merge-commit-free precisely
because this lane had **0 commits** at that point and `git diff --name-only HEAD main`
showed main had touched **none** of `ARCHITECTURE.md` / `CLAUDE.md` / `VISION.md` — both
checked before running it. The fast-forward moved `19476e3f → 4881383c`, carried the
uncommitted work through untouched, and `journal_spine_anchor` went to **0 FAILs**
immediately. No lane-to-main merge was performed; the integrator's job is unchanged, and
the lane now branches from current `main` rather than from a 50-minute-old base.

**Not done, deliberately:** no `SKIP=audit-health`, no `git push --no-verify`, and no
JOURNAL entry written on the sibling's behalf — a lane never journals for another lane's
arc, and inherited spine lag is the exact case where `SKIP=` looks reasonable and is not.


---

**Lane:** `lane-docs-governance` · three files + this artifact + the generated audit index.
No `tasks/` or `BACKLOG.md` edit, no `protocols/` edit, no `.pre-commit-config.yaml` edit,
no merge. The integrator merges.
