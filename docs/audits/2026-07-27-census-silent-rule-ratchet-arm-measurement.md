# Silent-rule ratchet — arm-time re-measurement (BUILD STOPPED)

- **Class:** census (ADR-101 enum) · **Date:** 2026-07-27 · **Slug:** silent-rule-ratchet-arm-measurement
- **Source-session:** `[#436]` execution lane (parallel session, commit-and-STOP), worktree `.claude/worktrees/ratchet`
- **Measured at:** HEAD `b4dd3e48` · **Compared against:** census HEAD `bf49cbf959acf1ca0dfb970b17bf02f34a9862ef`
- **Prior measurement:** `docs/audits/2026-07-19-census-silent-rule-ledger.md` (N_silent 176, pinned `bf49cbf9`)
- **Why archived here:** the `[#436]` build contract required a live re-measurement of N_silent before pinning a
  baseline. The re-measurement returned **greater than 176**, which is the contract's STOP branch. This artifact is
  the measurement evidence that branch requires. **No ratchet check was built and no baseline file was committed.**

---

## Verdict

**Measured N_silent > 176. Build stopped at the arm-time gate; nothing beyond this evidence is committed.**

The governed corpus gained normative MUST-shaped rules between the census (`bf49cbf9`, 2026-07-19) and the arming
attempt (`b4dd3e48`, 2026-07-27) — including **one entirely new governed protocol file**, `protocols/REPO_ONBOARDING.md`
(249 lines), which no census has ever swept. Pinning 176 would have armed the gate RED on its first run; adopting the
higher number would have laundered eight days of unadjudicated growth into the baseline. Both are ruled out.

---

## Method

Read-only. Three probes, no mutations outside this artifact.

**Scope** — the census's ruled denominator roots (ledger, ruling 3): `protocols/**/*.md` · `templates/**/*.{md,tmpl}` ·
`ecosystem/*.yaml`. Enumerated from `git ls-tree -r --name-only <ref>`, so both refs are read from git rather than the
working tree and the comparison is layout-independent.

**Detector** — a line is a *candidate* when, after stripping, it matches the census's own Pass-1 token set
`\b(MUST|never|only|required|shall)\b` (case-insensitive). Candidates are keyed by
`sha1(path \x00 whitespace-normalised lowercased line)`, so a line that **moves** is the same candidate and a line
whose **text changes** is a different one. This is deliberately content-keyed: line anchors rot, and the census's own
anchors are already 8 days stale.

**Decoding** — `git show` output is decoded as UTF-8 explicitly. The first probe run used the platform default
(cp1252) and **silently zeroed several files** before the error surfaced; every count below is from the corrected run.
Recorded because a silent decode failure is exactly the class of measurement error the prior census flagged.

**Sensitivity** — the verdict was re-run at three detector strictnesses to confirm it is not an artifact of token
choice.

| Detector | census `bf49cbf9` | HEAD `b4dd3e48` | added | removed | **net** |
|---|---:|---:|---:|---:|---:|
| census tokens `MUST\|never\|only\|required\|shall` | 1025 | 1068 | 51 | 8 | **+43** |
| strict `MUST\|shall\|never` (any case) | 533 | 552 | 22 | 3 | **+19** |
| hard `MUST` (uppercase) `\|never\|shall` | 382 | 395 | 15 | 2 | **+13** |

Files in scope: 62 at the census, **63 at HEAD**. The verdict is direction-stable across all three.

**Why the raw counts exceed the census's own Pass-1 figure (812/44).** The census's exact regex and file filter were
not recorded, only its token set. This probe's filter is therefore its own, and its absolute counts are **not**
comparable to 812. Only the *delta between two refs measured with one identical detector* is load-bearing here, and
that delta is what the verdict rests on.

---

## Delta — what entered the corpus after the census

Full itemisation of the 51 added candidate lines follows the summary. At most 8 of them are rewordings of the 8
removed lines (all in `AI_COUNCIL_PROCESS.md` / `PLAYBOOK.md`, from the ADR-43 routed-mirror retirement reflow), so
**at least 43 candidate lines are net-new**.

| File | added | note |
|---|---:|---|
| `protocols/REPO_ONBOARDING.md` | 14 | **file did not exist at the census** — 249 lines, never swept |
| `protocols/PLAYBOOK.md` | 13 | 5 removed alongside — partly reflow, partly net-new rules |
| `protocols/AI_COUNCIL_PROCESS.md` | 9 | 3 removed alongside — largely the ADR-43 amendment reflow |
| `protocols/HANDOFF_PROCESS.md` | 6 | the verbatim-definition + probe-region additions |
| `ecosystem/parity-surfaces.yaml` | 4 | new MUST rows (ADR-106 uv, `[#433]` tasks/) |
| `ecosystem/disposition-register.yaml` | 3 | commentary |
| `protocols/ESSENTIALS.md` | 1 | ADR-43 amendment pointer |
| `templates/handoff/v5/PROBES.md.tmpl` | 1 | probe row |

### Sampled adjudication — enough to establish the verdict, not a full census

The exact new N_silent requires the census's judgment pass (mechanism lookup keyed on each rule's subject), which is
`[#357]`-class work and outside this build's scope. Establishing `> 176` only requires demonstrating that **at least
one** genuinely new MUST-shaped rule is unenforced and undeclared. Four were checked against live mechanisms:

| New rule | Mechanism search | State |
|---|---|---|
| `PLAYBOOK.md:1270` — "**Never branch, commit, or merge under a live session.**" | `grep -l "live session" scripts/*.py` → **zero hits** | **silent** |
| `REPO_ONBOARDING.md:92` — "`marketplace add` **must** precede `install`" | `grep -n "marketplace" scripts/*.py` → only an unrelated tokenizer comment | **silent** |
| `REPO_ONBOARDING.md:199` — "`.gitignore` floor negations **must use the contents form**" | restated in `generate_floor.py:123` — a **generator docstring**, not a verifier; nothing checks a consumer's `.gitignore` | **silent** (off-surface admission fails the declaration test — the control-(ii)b pattern) |
| `parity-surfaces.yaml:236,240,248,256` — new `tier: {hub: MUST, …}` rows | `fleet_parity.py`, a blocking `ALL_CHECKS` member, reads these rows | **enforced** — excluded from the silent delta |

The parity rows are called out deliberately: they are the case where a mechanism **does** exist, and counting them as
silent would have inflated the delta.

**Floor: N_silent ≥ 179.** Three demonstrated new silent rules on top of a 176 baseline that itself lost nothing
verifiable. The true figure is higher — 43 net-new candidate lines remain unadjudicated — but 179 is what this probe
establishes without judgment.

---

## The measurement problem this exposed

**N_silent is not mechanically reproducible, and the ratchet's design has to account for that.** 176 was produced by a
mechanical token sweep followed by a four-extractor *judgment* pass that collapsed ~1000 candidate lines to 320 rules
and 176 silent ones — roughly a 17% conversion. No script reproduces that judgment. Two consequences for the eventual
build:

1. **A live count cannot be recomputed from scratch each run.** The ratchet has to carry the census's classification
   as committed data and measure only the *delta* against it — the shape this probe used.
2. **The census's itemisation cannot serve as that committed data as written.** Parsing the ledger's §A–D anchors
   yields **182** entries, not 176: §A=90, §B=68, §D=3 match their stated counts, but **§C lists 21 anchors under a
   heading claiming 15**. Any inventory derived from the ledger prose starts 6 rows off. The itemisation is also
   line-anchored at `bf49cbf9`, and `protocols/` has since churned.

Neither point is a defect in the census — it stated its limits, including that 176 is a floor. Both are constraints
the ratchet's baseline file has to be designed around, and neither was visible before this measurement.

---

## What the operator has to rule before `[#436]` can be built

1. **The baseline number.** 176 is stale as of this measurement. Re-pin at a re-measured figure, or arm at
   `bf49cbf9`'s 176 and accept that the delta above is the ratchet's first drain queue.
2. **Whether the 43 net-new candidate lines are adjudicated first, or grandfathered with the delta recorded as
   owed.** Grandfathering at HEAD is the only path that arms the gate GREEN immediately; it is also the path that
   makes the eight-day growth permanently invisible.
3. **`protocols/REPO_ONBOARDING.md` needs a census sweep.** A new governed protocol file entered `protocols/` without
   passing the denominator. This is the growth `[#436]` exists to stop, and it happened while the ticket sat open —
   which is itself the strongest available argument for the ratchet.
4. **The baseline file's data model**, given that the ledger itemisation cannot be parsed to 176 (§C's 21-vs-15
   discrepancy needs a ruling: is §C over-listed, or is the tally under-counted?).

---

## Acceptance

| Criterion | Status |
|---|---|
| Live re-measurement performed at arm time | ✓ HEAD `b4dd3e48` vs census `bf49cbf9` |
| Verdict direction robust to detector choice | ✓ three strictnesses, all net-positive |
| Delta itemised to file:line | ✓ §Delta + appendix |
| New-rule claims verified against live mechanisms | ✓ 4 sampled; 1 found **enforced** and excluded |
| Silent-decode / swallowed-error control | ✓ cp1252 failure caught and re-run under UTF-8 |
| Build stopped per contract | ✓ no check, no baseline file, no `ALL_CHECKS` edit |
| `BACKLOG.md` untouched | ✓ |

---

## Appendix — the 51 added candidate lines

`[H]` = matches the hard detector (uppercase `MUST` / `never` / `shall`).

### `ecosystem/disposition-register.yaml`
- `:178` doc -> spec edge. The only occurrence of the token in this file is a cross-reference…
- `:180` `[H]` … It therefore names a sibling capture, never the spec, and…
- `:257` # filing, NOT accretion — on an operator ruling that the accretion label must not absorb them.

### `ecosystem/parity-surfaces.yaml` *(adjudicated **enforced** — see sampling table)*
- `:236` `[H]` `tier: {hub: MUST, consumer: LOCAL}`
- `:240` `[H]` `uv.lock` — MUST at the hub now; consumer stays LOCAL until each repo's own rollout (ADR-106, `[#432]`)
- `:248` `[H]` `.python-version` — MUST at the hub now; consumer LOCAL until rollout (ADR-106, `[#432]`)
- `:256` `[H]` `tasks/` — MUST at the hub while the strangler runs (`[#433]`, ADR-101 amendment 2026-07-27)

### `protocols/AI_COUNCIL_PROCESS.md` *(3 removed alongside — largely reflow)*
- `:9` version 2.1 header · `:16` Authority line · `:169` synthesizer default `openai`
- `:172` `target-project` RETIRED — do not set · `:261` `[H]` never participates on the panel
- `:311` Canonical (only) landing path · `:346` `[H]` … decision content never
- `:389` `RoutingError` row · `:416` v2.1 history entry

### `protocols/ESSENTIALS.md`
- `:142` Council transcripts canonical-only; routed-mirror retired

### `protocols/HANDOFF_PROCESS.md`
- `:401` whitespace-only additions permitted · `:403` `[H]` **MUST be reported** when the transport is reported
- `:451` regions **must be authored before the bundle is committed** · `:459` not caught (`[#366]`)
- `:460` `[H]` never that any particular value is present · `:462` `[H]` `PROBES.md` never inspected by this check

### `protocols/PLAYBOOK.md` *(5 removed alongside — partly reflow)*
- `:154` ToC entry · `:950` transcripts RETIRED row · `:1052` canonical-only routing
- `:1235` merge/push/delete are ONE operation · `:1264` `Win32_Process` resolves only to `cmd`/`pwsh`
- `:1270` **Never branch, commit, or merge under a live session** *(adjudicated **silent**)*
- `:2421` cross-repo prompt first line · `:2590` `[H]` **Prove, then codify** — never a substitute for shipping
- `:2673` / `:2676` Council output convention · `:2808` Codex archival protocol
- `:3089` `[H]` **Witnessed is the operator's eye or a mechanical report — never a proxy**
- `:3649` Prove-then-codify pointer

### `protocols/REPO_ONBOARDING.md` *(file new since the census — 249 lines, never swept)*
- `:7` `[H]` … (ADR-41), never from a hub worktree
- `:41` `--run-date` is **required** (no wall-clock read)
- `:58` / `:61` / `:162` / `:210` read-only-first command guidance
- `:64` destroy-confirm required before pruning any `status:removed` component
- `:92` `marketplace add` **must** precede `install` *(adjudicated **silent**)*
- `:131` `[H]` `.git/hooks/` never travel … · `:132` every fresh checkout must arm them once
- `:189` `[H]` … inert until armed · `:190` bare `pre_commit install` arms the pre-commit stage only
- `:199` `.gitignore` floor negations **must use the contents form** *(adjudicated **silent**)*
- `:218` per-repo checklist scope line

### `templates/handoff/v5/PROBES.md.tmpl`
- `:70` P3 probe row (HEAD sha / clean tree / branch / ahead-behind)

### Removed since the census (8)
`AI_COUNCIL_PROCESS.md:168`, `:257` `[H]`, `:314` · `PLAYBOOK.md:2637` `[H]`, `:2645`, `:2670`, `:2673`, `:2802`

---

## Amendment — Disposition (D4), operator-adopted 2026-07-27

Appended as an in-file amendment marker (CLAUDE.md §5 rule 3); nothing above this line is
edited. This records what happened to the STOP verdict, not a revision of it.

**Adopted semantics — D4 (architect-proposed, operator-adopted).** The census's `N_silent`
is not recoverable by code: its regex and file filter were never recorded, which is what
this report established. Rather than launder an unreproducible number into a gate, D4 pins
a **detector in code** and lets it define the metric. `scripts/silent_rule_detector.py`
(`silent-rule-v4`) is now the single source for *both* the baseline and every live count;
the census's detector is explicitly **not** reused. The measured baseline is **428**
normative-keyword occurrences across **56** files at `527958fb`, committed to
`ecosystem/silent-rule-baseline.yaml` as a number plus its detector id — never a parse of
the ledger, whose §A–D itemisation yields 182 anchors against a stated 176 (§C lists 21
under a heading claiming 15).

**What the new metric is.** A normative-keyword *occurrence* count, not a rule census: it
cannot distinguish a rule from a mention of one in an example. It is a **proxy** for the
pool's size, load-bearing only in its movement against a baseline measured the same way.
It is not comparable to 176, nor to this report's 812 Pass-1 figure.

**One correction this build made to the report's own detector choice.** An uppercase-only
token set was measured first and rejected: it matched **0 of 3** of the rules adjudicated
silent in the sampling table above — all three are written in prose case (`**Never**
branch…`, `**must** precede`, `**must use**`). The pinned detector is therefore the
case-insensitive `must|shall|never` variant (this report's "strict" row, net +19).
`ecosystem/parity-surfaces.yaml` is excluded from scope for the reason this report already
gives for excluding its rows from the delta — they are `tier:` enum values read by
`fleet_parity`, enforced by construction; left in scope they were 120 of 148 candidate
lines (81%), which would have made the ratchet fire when someone *added enforcement*.

**Still owed, and deliberately not done here.** The three adjudicated silent rules
(`PLAYBOOK.md:1270`, `REPO_ONBOARDING.md:92`, `REPO_ONBOARDING.md:199`) and the wider
43-line net-new delta are **undrained** and are owed to the **drain list** — review date
**2026-08-26** ([#356], [#358]–[#361]). The ratchet stops the pool growing; it does not
drain it, and a green ratchet must never be read as a drained pool. The four rulings this
report asked for remain open on their merits; D4 unblocks the *build* by changing the
metric, and does not answer them.

**Terra CODE review corrections, applied before integration (2026-07-27).** The lane's
`gpt-5.6-terra` review returned **five HIGH** findings against the first implementation;
all five were fixed rather than dispositioned, and the detector id was bumped
`silent-rule-v1` -> `silent-rule-v2` because one of them changed the unit:

1. **Reflow-gameable unit.** v1 counted matching LINES, so joining two rule lines lowered
   the number without removing a rule and rewrapping one raised it without adding a rule.
   v2 counts keyword OCCURRENCES, which is reflow-stable. Baseline re-measured 379 -> 428
   (the same corpus, a different unit -- not growth).
2. **Raise-guard read `HEAD`.** Once a raise was committed, HEAD *was* the new value, so
   the guard compared the baseline against itself and passed; it also collapsed on a merge
   commit and a detached HEAD. It now reads the integration target (`origin/main`, falling
   back to `main`), and an unreadable target is surfaced as `raise-guard INACTIVE` in the
   finding rather than silently skipped.
3. **Detector failure was non-blocking.** A measurement error emitted `unavailable`, which
   ship-gate does not block on -- an unmeasured corpus would have shipped green. Now FAIL.
4. **Missing hub artifacts were non-blocking.** An absent `BACKLOG.md`/`tasks/` returned
   `n/a`, so deleting the derived tree disarmed the gate that watches it. Now FAIL on the
   hub; `n/a` is reserved for the off-hub guard.
5. **Path exclusions were case-sensitive.** Windows can surface `templates/Archive/...`,
   which the exclusion would then miss, making the metric differ by platform. All path and
   ordering comparisons are casefolded.

Each carries a named regression test. The residual limit terra raised and this build did
NOT close is recorded rather than hidden: occurrences inside examples, quotations and
already-enforced rules still count, because separating a rule from a mention of one needs
the semantic pass the census did by hand.

**Second and third terra passes (same day).** The re-review confirmed three of the five
fixes held and found two incomplete plus one new HIGH; a third pass found two further
fail-opens. All closed, and the detector id moved `v2` -> `v3` because the corpus
definition changed:

6. **Bootstrap did not prove absence.** "A ref resolved but reading a baseline failed" was
   treated as first-introduction, so a target baseline that existed but was malformed (or
   a `git show` that timed out) would have let a raised branch value pass uncompared.
   Absence is now established positively with `git cat-file -e`, and the target state is
   modelled explicitly as `valid` / `absent` / `invalid` / `unresolved` -- only proven
   absence bootstraps; `invalid` FAILs and `unresolved` WARNs.
7. **The corpus was still a filesystem walk.** A walk inherits the host's case semantics
   and its notion of which of two casefold-colliding names exists, so the same commit could
   enumerate a different FILE SET on Windows and on Linux -- a rule could disappear from
   the measurement by being on the wrong OS. The corpus is now git's tracked inventory
   (`git ls-files`), symlinks and gitlinks excluded, casefold-colliding tracked paths
   REFUSED rather than silently resolved, and an unenumerable corpus raises instead of
   degrading to a subset. Side effect, and a correct one: an untracked scratch draft can no
   longer move the ratchet.

Count unchanged at **428 across 56 files** through both corrections -- behaviour-preserving
on this tree, platform-stable off it.

**Fourth terra pass.** Three further HIGH findings, all closed; detector `v3` -> `v4`
because the content source changed:

8. **A failed git probe read as proven absence.** `git cat-file -e` returns non-zero for an
   inaccessible or corrupt object exactly as for a missing path, so an unreadable target
   baseline was classified `absent` and bootstrapped past. Absence is now proven with
   `git ls-tree`, which exits 0 and prints nothing when the path is genuinely missing --
   separating "not there" from "could not look". A failed lookup is `invalid` (blocking).
9. **The first valid ref could conceal a raise over the other.** With `origin/main` at 500
   and an ahead local `main` at 400, a branch baseline of 450 passed against 500 while
   raising the real local target from 400. All resolved refs are now reconciled: any
   `invalid` blocks, and the comparison uses the **minimum** valid baseline, which cannot
   be gamed by ref ordering or divergence.
10. **Content still came from the working tree.** `ls-files` gave canonical paths, but each
    was re-opened from disk -- handing the bytes back to the host, where smudge filters,
    filesystem aliases, junction/symlink ancestors and NFC/NFD-insensitive filesystems can
    make one index measure different bytes or read one physical file twice. Content is now
    read from the object store via `git cat-file --batch` using the index's blob ids, and
    path-collision detection folds NFC normalization as well as case.

Count unchanged at **428 across 56 files** through all four passes.

**Review-loop record, stated plainly.** Four terra passes returned 5, 3, 2 and 3 HIGH
findings; thirteen were fixed and none dispositioned. Every one was a fail-open in a gate
whose entire purpose is to refuse — a metric that could be gamed by reflow, a raise-guard
that compared a value against itself, statuses that did not block, a corpus that differed
by platform. That an arming attempt needed four adversarial passes is itself evidence for
the arm-time STOP this report recorded: the first implementation looked correct and was
not.
