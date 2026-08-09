# Decision-sheet verification — every claim on the ruling surface, independently established

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-10 · **Slug:** decision-sheet-verification
- **Seat:** CC (Opus 5), CLOUD lane N-B, branch `claude/night-batch-cloud-lanes-a4mpkp`
- **Subject:** `docs/audits/2026-08-09-technical-decision-sheet.md` (90 lines, committed `0323e071`)
- **Posture:** **rules nothing, corrects nothing.** The sheet is a committed artefact and is left
  untouched; this report supersedes it by reference where a verdict differs.

## Run conditions — hand-run, not gate-passed

Cloud container, `[#453]` conditions confirmed: `uv 0.8.17` vs the `==0.11.19` pin at
`pyproject.toml:25`, so every `uv run --locked` hook entry refuses and **no gate fired for this
report**; `.git/hooks/` samples only; `audit.py health` structurally unpassable in a cloud clone;
clone arrived shallow and `git fetch --unshallow` ran before every history claim below (4777
commits). Filename pre-verified against `validate_hermetization.classify()` (returns `None`) and
`gen_audit_index.py`'s date/title parser.

## Method

Every claim was followed **to its origin**, not to the sheet's summary of it. Where the sheet
cites an audit, the audit's own evidence was read. Verdicts: **VERIFIED** (evidence read),
**REFUTED** (contradicting evidence + locator), **UNVERIFIABLE** (with the search run).

---

## 1. The headline defect, established

The sheet's **K-4** entry claims, for `[#310]`:

> *"`#292` — the precondition named in the row's OWN escape clause — is verified closed"*
> → source recommendation **"KILL via its own escape clause (a close, not a deletion)"**

**Verdict: the factual half is VERIFIED; the inference is REFUTED — and was refuted in writing
on 2026-07-21, nineteen days before the sheet was cut.**

- `#292` **is** closed. `9fc1a8b4` (2026-07-21) carries `closes [#292]`. VERIFIED.
- The escape does **not** follow. The same commit body says, verbatim:

  > *"`[#310]` — the pair partner of `#292` … `#310`'s escape hatch (its own kill-candidates
  > line: if the 07-05 bundle's cold state is adequately recorded in `#292`'s evidence, no
  > surface need be built) **rests on a premise that is false in fact**: the gate that discharged
  > `#292` is diff-triggered/prospective-only, so already-committed bundles are grandfathered and
  > the 07-05 bundle is explicitly **NOT** covered by it. The cold-annotation surface remains
  > genuinely unbuilt, so `#310` stays OPEN on its own merits."*

Independently re-established tonight, not taken from the commit body:

- `scripts/validate_residual_completeness.py` docstring: *"DIFF-TRIGGERED, prospective-only …
  only bundle files ADDED or MODIFIED against HEAD are examined … Already-committed bundles are
  historical artifacts and are never re-litigated."*
- The 07-05 bundle still leaks exactly **8** `(fill:` markers —
  `HANDOFF_BOOT.md` 1, `RESIDUAL.md` 3, `PASTE_THIS.md` 4 (`grep -ro "(fill:"`, counted tonight).

The refutation is also carried **on the row itself**:
`tasks/310-*.md` → *"kill-candidates: #292 — REFUTED at 9fc1a8b4: escape premise FALSE,
`validate_residual_completeness.py:33-35` is prospective-only and grandfathers this bundle
(8 `(fill:` live). **Do NOT re-propose**."*

**So the claim was refuted in three places** — the closing commit's body, the row's own
`kill-candidates:` line, and the validator's docstring — and still reached a ruling surface as
a kill recommendation. The row carried an explicit *"Do NOT re-propose"* and it was re-proposed.

**Disposition since:** ARC-4 caught it. `9a7ffcb4` — *"chore(backlog): K-4 — `[#310]` stays open;
attach the ruling that saves it to the row"*. The defect was contained by an adjudicator reading
carefully, which is exactly the control that does not scale.

## 2. Verdicts — one row per claim

### §7, the fifteen operator-owed items

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 1 | `[#492]` Grok 4.6 release is an external fact | **VERIFIED (as unverifiable)** | correctly self-classified; no in-repo resolution exists, and this container's network posture cannot settle it either |
| 2 | Four kill proposals, each with an unmeetable clause | **PARTIALLY REFUTED** | see §3 — K-4's rationale is refuted; K-1/K-2/K-3 hold |
| 3 | OneDrive rule conflict across three surfaces | **UNVERIFIABLE** | two of the three surfaces (`ai-council`, global `~/.claude`) are outside this clone; `ls ..` shows no siblings |
| 4 | ADR-111 Proposed at `da274889` | **VERIFIED** | `da274889` (2026-08-09) *"docs(adr): ADR-111 (Proposed) — the finding pipeline, four outcomes per finding"* |
| 5 | `[#511]` — ~4.5 s mechanized cost of a ~30-min wall clock | **UNVERIFIABLE** | the figure is not reproducible from repo state; no measurement artefact located |
| 6 | Intake #30/#31 filed verbatim at `036385a6`, zero births | **VERIFIED** | `036385a6` (2026-08-09) adds both intake files (+52/+51) plus index/manifest; no `tasks/` add in the diffstat |
| 7 | n=5 unattributed HEAD swaps; reflog gitignored | **VERIFIED (as unverifiable)** | correctly self-classified |
| 8 | `2h43m` / `~9 minutes` unlocated in the tracked record | **VERIFIED** | independent search reproduces the absence |
| 9 | `trailing-whitespace`/`end-of-file-fixer` collide with append-only invariants | **VERIFIED** | rewriters vs `LESSONS.md`/`logs/TOKEN-LOG.md`/ADR immutability is a real conflict per CLAUDE.md §5 |
| 10 | 153 pending closures at reading, 143 today; store gitignored | **UNVERIFIABLE** | store is untracked; unreachable from a cloud clone. Correctly self-classified |
| 11 | Two engine amendments operator-endorsed but unratified | **UNVERIFIABLE** | endorsement is off-repo (session context), not a tracked artefact |
| 12 | *"ARCHITECTURE.md not re-read, not re-stamped … still true after this arc"* | **REFUTED** | **see §4 — this is the second inherited claim** |
| 13 | `[#322]` peg referent ruled against | **VERIFIED** | row is `status: deferred`, P2; consistent with the sheet |
| 14 | `[#502]` is the mutmut row, not the import-convention row | **VERIFIED** | `tasks/502-mutmut-mutation-testing-evaluation-ci-hosted.md`, `title: "mutmut 3.7.0 mutation-testing evaluation — CI-hosted"`. The sheet is **right** and the consolidation report it corrects was wrong |
| 15 | Intake #28 §B is DRAFT | **VERIFIED** | consistent with the intake index state |

### §2, the four kill entries

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| K-1 | `[#102]`: `#262`/`#295` verified closed at `19b5d598`; peg will never occur | **VERIFIED** | `19b5d598` (2026-07-25) *"closes [#339], closes [#262], closes [#295]"*; neither `tasks/262-*` nor `tasks/295-*` exists (done-items-leave). The row's own text carries the discharged verify-first |
| K-2 | `[#308]`: `#221` closed at `8aab4356` with no successor | **VERIFIED** | `8aab4356` (2026-07-07) *"Arc-4 close: corp-monorepo deployed at v1.2.0, n=2 recorded, closes [#221] + [#100]"*; no `tasks/221-*` |
| K-3 | `[#325]`: same dead `#221` referent; `[#294]` nearest live carrier | **VERIFIED** | same `8aab4356`; `[#294]` open |
| K-4 | `[#310]`: escape precondition satisfied → close | **REFUTED** | **§1 above.** The closure fact is true; the escape inference is false and was refuted 2026-07-21 |

### §3, ADR-111 §4 — the departure

| Claim | Verdict | Evidence |
|---|---|---|
| ADR-111 declines the ARC-2 clause because it contradicts ADR-98 §3 | **VERIFIED** | ADR-111 is Proposed (`da274889`); the departure is stated in the ADR itself, not invented by the sheet |
| *"intakes #16, #26 and #25 were each accepted by recorded operator ruling in `decided-by`, not by ADR"* | **VERIFIED** | consistent with `docs/intake/` frontmatter; this is the load-bearing empirical claim and it holds |

### §4, surfaced by ARC-3

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| A | No open row owns the `sys.path` substrate; `[#502]` misattributed | **VERIFIED** | `tasks/502-*` is the mutmut row (§7 item 14). The sheet correctly refutes its own source |
| B | `[#520]` birth-cap reading | **UNVERIFIABLE** | turns on intent in a contract, not on repo state |
| C | *"8 rows are P1/P2 **and** deferred, two of them P1 (`[#218]`, `[#300]`)"* | **VERIFIED — exactly** | reproduced from `tasks/` frontmatter: `[#4] [#102] [#139] [#181] [#218] [#300] [#301] [#322]` = 8, of which `[#218]` and `[#300]` are P1. Both count and named ids correct |
| D | 20th `undeclared_edges` WARN, 19 of 20 dispositioned, three same-shape precedents | **VERIFIED, now discharged** | `ecosystem/disposition-register.yaml` holds 20 `warn-undeclared` ids; ARC-4 landed the 20th at `201191f0`. True when written; the RED it named is now cleared |

---

## 3. Tally, and the real diagnostic

**24 claims: 15 VERIFIED · 2 REFUTED · 1 partially refuted · 6 UNVERIFIABLE.**

The count that matters is not the refutation count — it is **which claims were inherited rather
than measured.**

**Inherited and not re-measured — 2 of 24, and both are the sheet's two errors:**

- **K-4** — inherited from the consolidation report §4.5. What was measured was `#292`'s
  *closure status*; what was asserted was *escape satisfaction*. Those are different
  propositions and the second was refuted in the very commit that established the first.
- **§7 item 12** — inherited from ARC-2's statement and re-asserted as *"still true after this
  arc"*. It was not re-checked. See §4.

**Measured and correct — the sheet's §4 items A and C are the strongest work on it.** Item A
catches its own source in an error (the consolidation report's `[#502]` misattribution); item C
reproduces a count and two ids exactly. Both were computed rather than carried.

**The diagnostic, stated plainly: every claim the sheet measured is right; both claims it
inherited are wrong.** The defect is not carelessness in verification — it is the *absence* of
verification at the inheritance boundary. A claim that arrives already-phrased-as-a-conclusion
is not re-derived, because it does not look like an open question.

## 4. The second inherited claim, established

**§7 item 12** asserts: *"ARCHITECTURE.md not re-read, not re-stamped … **still true after this
arc** — ARC-3 did not re-read it either."*

**REFUTED.**

- `ARCHITECTURE.md:2` carries `last_reviewed: 2026-08-08`.
- The stamp was set by `8f09c12d` (2026-08-08), whose subject is: **"docs: clear the
  canonical_freshness RED by performing the review the stamp asserts."**

The re-read and the re-stamp both happened, on 2026-08-08 — **the day before the sheet was
cut** — and the commit that did it says so in its title. This is the same failure shape as K-4:
a state claim carried forward from an earlier arc and re-asserted as current without a
one-command check (`grep last_reviewed ARCHITECTURE.md`).

Note this is not the sheet inheriting from an *audit* — it is inheriting from *itself*, i.e. from
the arc's own earlier position. That is the harder case, because the claim's origin feels like
first-hand knowledge.

## 5. The smallest mechanism that would have caught the 2026-07-21 case

**Proposed, not built.** Deliberately the smallest thing that catches this class.

**The mechanism: a kill/close proposal that names a row id must surface that row's own
`kill-candidates:` line, and refuse when it contains a refutation token.**

Rationale — the evidence was already in the right place. `tasks/310-*.md` carried
`"REFUTED at 9fc1a8b4 … Do NOT re-propose"` **in the row's own `kill-candidates:` field**, which
is the field a kill proposal is by definition reading. Nothing needed to be discovered; the
proposal had to stop being written past a refusal already sitting in its input.

Shape, concretely:

- **Input:** the set of row ids a proposal/sheet marks for kill or close.
- **Check:** for each, read `tasks/<id>-*.md`'s `kill-candidates:` clause; match a small closed
  token set — `REFUTED`, `Do NOT re-propose`, `premise ... false`.
- **Verdict:** BLOCK the proposal, printing the row's own refutation text and the SHA it cites.
- **Discharge:** the proposal must either drop the row or carry an explicit counter-evidence
  clause naming *why the recorded refutation no longer holds* — which is precisely the sentence
  K-4 never wrote.

**Why this shape and not a bigger one.** A general "verify every claim on a decision surface"
gate is unbuildable — §2 shows 6 of 24 claims are legitimately unverifiable from repo state, and
a gate that cannot pass a legitimate claim will be bypassed. This one is narrow, mechanical,
fully local to files already in `tasks/`, and needs no network, no consumer repos, and no
judgment. It catches K-4 exactly.

**What it does NOT catch — stated honestly.** It would **not** have caught §7 item 12. That claim
is about a living doc's stamp, not about a row, and nothing in `tasks/` carries its refutation.
Item 12's class needs a different and even cheaper instrument: **a sheet that asserts the state
of a stamped canonical doc should cite the stamp value it observed.** A claim written as
*"ARCHITECTURE.md `last_reviewed: 2026-08-04`, not re-stamped"* is falsifiable at a glance;
*"not re-stamped"* is not. That is a drafting convention, not a gate, and it is offered as such.

## Needs a ruling

1. **Does K-4 need anything further?** ARC-4 already ruled `[#310]` stays open and attached the
   saving ruling to the row (`9a7ffcb4`). My verdict agrees with ARC-4's. **No further action
   appears owed on `[#310]` itself** — the question is whether the *sheet* needs a recorded
   supersession pointer, given it is immutable and its K-4 row still reads as a kill
   recommendation.
2. **Item 12 — correct the record?** The sheet asserts something false about `ARCHITECTURE.md`,
   and item 12's three options ("commission a re-read arc · re-stamp on a scoped read · leave the
   stamp honest and stale") are all premised on work that was already done at `8f09c12d`. The
   item may simply be closed as discharged. That is the architect's call, not mine.
3. **Build the `kill-candidates:` refusal check?** §5 proposes it and does not build it. If the
   answer is yes, it needs a row; no open row owns it — `[#508]`/`[#241]` are adjacent but
   neither covers proposal-time refutation surfacing.
4. **Adopt the citation convention?** *"A claim about a stamped canonical doc cites the stamp
   value observed."* This is a drafting rule, cheap, and would have caught item 12. It needs a
   home (PLAYBOOK, or the audit template) and a decision on whether it is advisory or checked.
5. **Is "inherited vs measured" worth tracking as a standing field?** 2 of 24 inherited claims
   produced 2 of 2 errors. If that ratio is stable, marking each claim on a decision surface as
   measured-here or carried-from is a higher-yield discipline than verifying claims after the
   fact — which is what this lane had to do.
