# Seal-rule attribution — which rules actually manufacture the 336 WAIVEs

> **Step 2 of lane `lane-v-000-seal-rules-rerun` (batch V, V-3).** DECLARE-REVIEWS §A.4 names
> *"336 waivers produced by two hub-local seal rules"* and rules that those two are fixed before
> the operator is ever asked to rule a list. This file identifies the two, proves each one
> produces the waivers it is charged with, and records — because the measurement forces it — that
> a **third** rule contributes 28 of the 336.
>
> **Read-only against every consumer.** The only command that touched a repo other than the hub
> is `git -C <repo> ls-files`. Nothing was written, moved or armed anywhere.

## 1 · The two rules, and the property that selects them

§A.4 does not name the two rules by identifier; it names their *count* and their *character* —
**hub-local**. The surface it is quoting does name them, in one sentence:

> `docs/audits/2026-09-07-technical-seal-report-fleet.md` §11 — *"`B2 + H1 + B1 = 305 of 348 items`
> — 88% of the fleet's out-of-pattern surface is two rules whose content is hub-local. … **The rule
> that works produces the actionable findings; the two that do not produce the waivers.**"*

So the two are **Rule B** (`rule_b_violation` — the audit-filename grammar) and **Rule C**
(`rule_c_violation` — the home allowlist), and the property that selects them is not "produces
waivers" but **"applies a vocabulary that belongs to one repo as though it were the fleet's"**:

| rule | the hub-local content it applies to every repo | the spec's own words |
|---|---|---|
| **B** | `naming_grammar.audit_class_enum` — 11 class tokens adopted from *"what three repos already write"* | `audit_class_enum_scope: repo-local`, written **into the spec** and read by nothing |
| **C** | `home_grammar.patterns` — a tuple that enumerates the hub's own subdirectories (`scripts/audit_checks`, `scripts/codemap`, `scripts/hooks`, `scripts/toc`, `templates/handoff`, `ecosystem/schema`, …) | *"WAS 'DERIVED FROM THE LIVE TAXONOMY' of this repo — which is precisely the substitution operator amendment D5 ended"* |

Rule A's content is no longer hub-local: amendment D5 moved it into
`ecosystem/fleet-shape-spec.yaml` as `root_allowlist`, and the `.corp-monorepo.code-workspace`
literal became the `.*.code-workspace` glob. That is the sense in which Rule A is *"the rule that
works"*.

**The mechanical shape of the defect, stated once.** `rule_b_violation(path)` and
`rule_c_violation(path)` are pure functions of a path string. They carry **no repo identity**, so
there is no seam through which the repo under test can declare its own class vocabulary or its own
homes. A rule with no such seam, run against a consumer, cannot measure *out-of-shape*; it measures
*difference-from-the-hub's-tree*. That is the packaging bug, and it is one bug wearing two rules.

## 2 · The measurement — the 348 reproduced from the live rules

Driven through the hub's own `validate_hermetization` rule functions, at the grain both predecessor
reports declare (Rule A per ITEM, Rule B per FILE, Rule C per distinct HOME; short-circuit parity
because `classify()` is `A or B or C`):

```
repo                       head       branch                          tracked  items    A    B    C (files)
.dev-knowledge             33bcb0bd   worktree-lane-v-000-seal-…         3063    137    0  137    0   (0)
ai-council                 7a3c057    main                                254     32    4   26    2  (26)
corp-monorepo              37b8aa1    main                                821     74    3   39   32 (297)
corp-ops                   3bde930    main                                 60      5    4    1    0   (0)
corp-sca-time-automation   3661b3a    feature/tenrox-loader                75      8    5    2    1   (1)
demo-prep                  1f7c35c    feat/leadership-template-deck       883     37    8   28    1   (5)
life-architect             7688b76    main                                 45      5    5    0    0   (0)
terminal-setup             d8a7b61    main                                  3      2    2    0    0   (0)
win-tooling                61120b7    feat/prompts-dir-user-scope-au…     178     48    6    0   42 (111)
                                                                         -----   ----  ---  ---  ---
                                                                          5382    348   37  233   78 (440)

Rule B, split by the LEG that refused:   class 194  ·  casing 39
```

**348 items, identical to the fleet report**, and the Rule B leg split reproduces its classes B2
(194) and B1 (39) exactly. Two rows were measured on a head that has moved since the predecessor
(`win-tooling` `49cb75e`→`61120b7`, off `main`; the hub is this lane's worktree at `33bcb0bd`) and
neither moved its item count — recorded so the agreement is not read as a stronger claim than it is.

**Re-run command** — the harness is a throwaway, these calls are the artifact:

```
uv run --locked python -c "import sys,subprocess; sys.path.insert(0,'scripts'); import validate_hermetization as vh; R=r'C:/Users/1028120/Documents/Dev/<repo>'; ps=[p for p in subprocess.run(['git','-C',R,'ls-files'],capture_output=True,text=True).stdout.splitlines() if p.strip()]; print(len(ps),'tracked'); [print(p,'->',vh.classify(p)) for p in ps if vh.classify(p)]"
```

## 3 · The WAIVE split — 336 attributed to its producers

The fleet report verdicts 11 items RELOCATE and 1 ESCALATED; the remaining 336 are WAIVE. Each of
those twelve was re-classified through the live rule functions rather than read off the class table:

```
VISION.md            x7   ai-council corp-monorepo corp-ops corp-sca demo-prep life-architect win-tooling  -> Rule A (top-level file)
intake/              x1   life-architect                                                                   -> Rule A (top-level dir)
docs/diagrams/       x1   win-tooling                                                                      -> Rule A (docs genre)
docs/ loose files    x2   corp-sca-time-automation, win-tooling                                            -> Rule C (home)
docs/decisions/transcripts/  x1   corp-monorepo                                                            -> Rule C (home, ESCALATED)
```

Subtracting them from §2's totals:

```
              items   non-WAIVE   WAIVE
Rule A           37           9      28
Rule B          233           0     233
Rule C           78           3      75
              -----       -----   -----
                348          12     336      <- reconciles to the fleet report exactly
```

**Each of the two charged rules is proven to produce the waivers charged to it.** Rule B produces
233 of 336 (69%) and every one of them is a WAIVE — the rule has never produced an actionable
finding anywhere in the fleet. Rule C produces 75, of which 72 are the "one level deeper than the
hub organizes it" class and 3 are genuine.

## 4 · THE STOP — three rules produce WAIVEs, not two

The contract's step 2 requires a stop and a naming if more than two rules are implicated. **The
measurement implicates three, and this is the naming.**

- **Rule A — 28 WAIVEs.** Class D domain top-level directories (14), Class I `INSTALL.md` (4),
  Class P standard Python root files (4), Class N ADR-59 dot-prefix (2), Class F repo-local root
  living docs (2), Class U the unonboarded 3-file repo (2).

**Why the fix nevertheless stays at two, stated rather than assumed.** Three facts, each checkable:

1. **The contract's own footprint binds this lane to two** — *"the two hub-local seal rules named
   in DECLARE-REVIEWS §A.4"* — and §1 above shows the selector is hub-local *content*, which
   Rule A no longer carries.
2. **Rule A's 28 are not rule-code defects.** Every one of them is fixed by a **data line in
   `ecosystem/fleet-shape-spec.yaml`** — `INSTALL.md` into `root_allowlist.files`, `conftest.py`
   and the pre-uv root files likewise, a repo-kind axis for the domain directories. That file is
   **V-2's footprint and is pinned OUT of this lane**. Widening here would mean editing another
   lane's file, which is the failure the pin exists to prevent.
3. **Rule A already produces actionable findings** — 9 of the fleet's 11 RELOCATEs are Rule A's.
   A rule that discriminates is not the rule §A.4 is describing.

**What this costs, stated honestly:** after this lane, Rule A's 28 WAIVEs remain. `N` will not be
zero and was never going to be. The residue is a spec-data question with a named owner (V-2 for the
kind axis; the operator's Sitting-3 list for the rest), not a silent leftover.

## 5 · The counterfactual — the proof that the seam is the cause

Re-running §2's measurement with each hub-local leg scoped out, one at a time and then together:

```
repo                        now   -B(class)    -C   -both
.dev-knowledge              137           0   137       0
ai-council                   32           6    30       4
corp-monorepo                74          46    42      14
corp-ops                      5           4     5       4
corp-sca-time-automation      8           6     7       5
demo-prep                    37          37    36      36
life-architect                5           5     5       5
terminal-setup                2           2     2       2
win-tooling                  48          48     6       6
                           ----        ----  ----    ----
                            348         154   270      76
```

**348 → 76 when both hub-local legs stop travelling: 272 of 348 items, 78% of the surface, exist
only because two rules carry one repo's vocabulary.** The columns also separate the two rules
cleanly — `demo-prep`'s 37 are untouched by the class leg (they are the *casing* leg, which is a
fleet clause and stays), and `win-tooling`'s 48 are untouched by Rule C's removal of the class leg.
No repo's number is explained by both.

**This is a diagnostic bound, not the design.** Deleting a leg is not the fix; giving it a repo
seam is. Two properties the counterfactual deliberately overstates:

- **The hub's 137 must not move.** They are `docs/audits/*.md` files that predate the class enum
  and are grandfathered by ADR-101 §6 — the live gate is **prospective-only** and has never
  inspected them. `-B(class)` showing `137 → 0` is an artifact of running the rule
  **retrospectively**, which is report mode's declared limit, not a defect the fix should chase.
- **Rule C has a fleet leg worth keeping.** All three of its genuine findings are `docs/` homes,
  and the spec states that leg explicitly — *"docs: GENRE trees only. `docs` itself is absent BY
  DESIGN — that absence is the rule this clause exists to state"*. Scoping the whole rule out
  would lose live drift that a consumer seal should catch.

## 6 · What the fix therefore has to be

Both rules split along the same seam, and the spec has already written both halves down:

| rule | FLEET leg — always applied | REPO-LOCAL leg — applied only from the repo's own declaration |
|---|---|---|
| **B** | the `YYYY-MM-DD-` date shape and the R4 casing rule | the audit class enum (`audit_class_enum_scope: repo-local`) |
| **C** | the `docs/` genre-tree rule (`docs` is not a home; a home under `docs/` opens with a sanctioned genre) | the home tuple — *"never with the hub's tuple"* |

The declaration surface is `.methodology.yaml`, the per-consumer sanctioned-divergence register
ADR-101 already sanctions at every root and two readers already parse — library-first, and not a
second convention. A repo that declares nothing gets the fleet legs and no repo-local leg; the hub
keeps today's behaviour byte-for-byte, so every in-repo gate and test is unaffected.

**Out of this lane's footprint, named so the residue has an owner rather than a silence:**
`docs/audits/*` → `docs/audits/**` (Class H2, 2 items), `INSTALL.md` into `root_allowlist.files`
(Class I, 4 items) and the repo-kind axis (Class D, 14 items) are all **spec-data** edits in
`ecosystem/fleet-shape-spec.yaml`, which V-2 owns. `<sanctioned-parent>/archive` (Class H3, 1 item)
is a **pattern-grammar** defect — the shape is stated as six literals instead of one rule — and it
lives in the rule code, so it belongs to this lane.

---

**Lane:** `lane-v-000-seal-rules-rerun` · batch V, V-3 · substrate local
**Measured:** 2026-09-09, from `worktree-lane-v-000-seal-rules-rerun` at `33bcb0bd`
**Writes in any consumer repo:** none — `git -C <repo> ls-files` only
