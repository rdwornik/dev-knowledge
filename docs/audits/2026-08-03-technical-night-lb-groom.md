# Night batch 2026-08-03 · lane L-B — backlog + architecture currency groom

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-03 · **Slug:** night-lb-groom
- **Status:** PROPOSAL — read-only night batch, unattended. **RULING INPUT ONLY.** No repo file
  was edited, staged, committed, or generated. Nothing was closed, reworded, filed or deleted.
  Every verdict below is a proposal for the morning architect.
- **Base:** `main` (local branch ref) = `65a549bf`; `origin/main` = **`c7628a3e`** *after* an
  unshallow fetch (see §0 — the brief's premise is corrected there). HEAD =
  `c7628a3e552a3aedff341106e4fb889763bf5b12` on `claude/night-batch-2026-08-03-k8djp8`.
- **Method:** read-only. Validators and generators run in report/`--check` mode only; no
  `--write`, no `--fix`. Interpreter: the scratchpad testenv (pytest 9.1.1 / ruff 0.15.5 /
  pyyaml / pydantic), because `uv run --locked` refuses here (§4.5). Working tree verified
  clean at open; at close it carries only untracked night-lane audit files, six as of this
  writing, one of them this file (§4.6).

---

## Verdict

1. **The backlog counts are exactly as briefed and stable: 186 tasks = 157 open + 29 deferred.**
   The 29-deferred baseline holds, **delta = 0**. `validate_backlog` and `validate_git_backlog`
   are both clean, and an independent full-spine closure-token pass agrees with the validator.
2. **Two DEAD rows the mechanical checker structurally cannot see.** `[#455]` is declared moot by
   an Accepted ADR (`ADR-109:24-25` / §2) yet is still an open row; `[#433]`'s three-part
   Done-when is now fully satisfied across ADR-107 §6.1 + ADR-109 §5 + ADR-109's 07-31 amendment.
   Neither has a `closes [#N]` commit, so `validate_git_backlog` is silent by design.
3. **Fixing `[#424]` as written would immediately RED the gate.** Simulated in-memory: normalizing
   the bare `depends-on` ids makes `[#383]`'s clause point at `#382`, which closed at `f7abe228`
   and left the file — `depends-on references non-existent id #382 — [#383] line 439`. The
   inertness `[#424]` exists to remove is currently *hiding* a dangling edge.
4. **The Proposed-ADR set is confirmed exactly {82, 88, 89}** — nothing missed, nothing spurious.
   88 and 89 are Accepted-by-in-file-marker with frozen `Proposed` headers ([#242]'s Pattern A);
   **ADR-82 is the real one**: still `Proposed`, its amendment chain stops at v5.2, while the
   spec it governs is live at **v6.0.1** — seven versions of drift.
5. **One live ADR-vs-ADR contradiction and one living-doc drift, both about the same clause.**
   `ADR-107:458` says §6.2 "is still undischarged"; `ADR-109:337` says it "is **DISCHARGED**".
   `ARCHITECTURE.md:855` — `last_reviewed: 2026-08-02`, two days *after* the discharge — repeats
   the stale side. Also drifted: `ARCHITECTURE.md:381` says 13 doc->code rules, the organ reports 14.
6. **Naming hazard, verified empirically: 5 of tonight's 6 lane files — including this one — are
   refused by the hermetization gate** (`night` is not in `AUDIT_CLASS_ENUM`; only lane L-A kept
   the class token). Nothing is staged, so nothing tripped tonight — but `git add` + commit will
   BLOCK. See §4.6.

---

## §0 Spine correction — the brief's git premise is half wrong

The brief states local `main` and `origin/main` are both at `65a549bf` and that HEAD's work "is
not yet reachable from `origin/main` in this clone". **The clone was SHALLOW** (`.git/shallow`
present, history floor 2026-07-27), which made every history claim in it unsound — including
`validate_git_backlog`'s advertised "full history".

A read-only `git fetch --unshallow` (refs only; no checkout, no merge, no working-tree change)
returned:

```
65a549bf..c7628a3e  main -> origin/main
```

State after the fetch, verified:

| ref | SHA | note |
|---|---|---|
| HEAD | `c7628a3e` | branch `claude/night-batch-2026-08-03-k8djp8` |
| `origin/main` | `c7628a3e` | **identical to HEAD** — the 08-01/08-02 work IS on remote main |
| `main` (local branch) | `65a549bf` | a stale local pointer, never fast-forwarded in this clone |

So: **the "174 commits ahead" figure is ahead of a stale LOCAL ref only. Nothing is unpushed.**
The first-parent spine went from **89** commits (shallow) to **1286** (full, back to 2026-03-30)
after the unshallow, and every history claim below is made against the full spine. The sibling
L-D lane independently records `main = c7628a3` in its own header, corroborating this.

---

## §1 Backlog sweep

### 1.1 The counts, from the validator

`python scripts/validate_backlog.py` (no flags — the script hardcodes `BACKLOG.md`; there is no
`--path`, which is itself the open `[#294]`):

```
WARN  user story with no tasks — story "[S24] Declare desired state once, as data, inste" line 432
validate_backlog: OK (9 themes, 26 stories, 186 tasks, 1 warning(s))
```

| quantity | value | evidence |
|---|---|---|
| task rows | 186 | validator line above; `grep -cE '^- \[#[0-9]+\]' BACKLOG.md` = 186 |
| deferred | **29** | `grep -c 'DEFER — peg' BACKLOG.md` = 29 |
| open | **157** | 186 - 29 |
| baseline (2026-08-02 boot) | 29 deferred | `docs/audits/2026-08-02-technical-night-batch-lf-backlog-health.md` §1 |
| **delta** | **0** | the deferred pool did not move overnight |

Themes parse as 9 by the validator's own count and 10 by a raw `## ` scan (`vb.parse` reports 10
themes when called directly) — the difference is `## Big picture`, excluded by the validator's
summary. Not drift; recorded so the two numbers are not read as a discrepancy.

The one WARN is `[S24]` carrying zero tasks — expected: its only member `[#382]` closed at
`f7abe228` and a `chore/s24-completed-marker` merge (`a02dd111`) recorded the story-level
precedent. No action proposed.

### 1.2 Classification

**LIVE — 148 open ids, no finding against them.** Each parses clean, carries a band and a
`Done when:`, has no closure token anywhere on the 1286-commit first-parent spine, and its
premise survived the checks in §2:

```
#23 #43 #71 #99 #112 #116 #122 #123 #126 #127 #130 #132 #146 #153 #162 #170 #185 #189 #210
#213 #215 #220 #227 #234 #241 #242 #245 #263 #266 #267 #269 #270 #271 #273 #274 #276 #277
#278 #280 #281 #282 #283 #285 #288 #289 #290 #296 #303 #315 #317 #320 #323 #324 #327 #329
#331 #332 #334 #335 #338 #340 #341 #342 #343 #344 #345 #346 #347 #348 #349 #350 #351 #352
#353 #354 #356 #357 #358 #359 #360 #361 #362 #363 #364 #365 #366 #369 #371 #383 #385 #387
#388 #389 #390 #392 #393 #394 #397 #399 #400 #402 #403 #404 #405 #406 #407 #408 #409 #410
#411 #412 #413 #414 #415 #416 #417 #418 #419 #420 #422 #423 #425 #426 #427 #428 #429 #430
#431 #432 #438 #440 #441 #442 #443 #445 #447 #448 #449 #450 #451 #453 #454 #456 #463 #464
#465 #470 #472
```

**DEFERRED — 29 ids, all LIVE-deferred (peg intact).** Every one carries an explicit
`DEFER — peg:` clause; none has a closure token:

```
#4 #19 #82 #102 #117 #139 #144 #145 #166 #169 #171 #181 #188 #190 #218 #231 #239 #240 #293
#294 #297 #298 #300 #301 #305 #308 #310 #322 #325
```

Spot-verified peg reachability on the one deferral whose peg is machine-checkable —
**`[#181]`** (`DEFER — peg: coherence-nudge.log has enough entries to adjudicate`): the log does
not exist (`ls logs/` = `FLEET-PARITY.md`, `PARITY-EVENTS.jsonl`, `TOKEN-LOG.md`), it is created
lazily on first fire (`scripts/coherence_nudge.py:41` `_LOG_PATH = _REPO_ROOT / "logs" /
"COHERENCE-NUDGE.log"`), is gitignored (`.gitignore:73`) and has **never been committed on any
branch** (`git log --all -- logs/COHERENCE-NUDGE.log` = empty). **Zero firings ever.** The
deferral is correctly held and the peg is currently unreachable — worth an explicit
accept-or-retire rather than an indefinite wait.

### 1.3 DEAD — already shipped in substance

**`[#455]` — DEAD by ratified ADR. Recommend close.**
Row at `BACKLOG.md:79`: a drift checker for `ecosystem/registry.md`'s derived Status version.
Two Accepted-ADR lines dispose of it:

- `docs/decisions/ADR-109-*.md:24-25` (Decommission): *"`ecosystem/registry.md` loses authority
  (§2 ...); **[#455] becomes moot when §2 lands**."*
- `docs/decisions/ADR-109-*.md:64-67` (§2 item 1): *"**`ecosystem/registry.md` — RETIRED as
  authoritative.** ... It may later be regenerated as a human view; it is never again
  hand-authoritative. **[#455] dissolves.**"*

ADR-109 is `**Status:** Accepted (ratified 2026-07-31 ...)` (`:3`), landed at `7ef40567`. §2 has
therefore landed, so the moot-condition is met. The row's own `kill-candidates` reasoning is
also stale: it argues *"[#382] dissolves the registry sprawl ... but is gated behind the pilot,
so this drift [checker is still needed]"* — `[#382]` closed at **`f7abe228`** ("closes [#382]:
fleet desired-state contract v1"). The gate the row relies on is gone.
*Why no checker caught it:* the disposal is written in an ADR, not in a commit subject; no
`closes [#455]` token exists anywhere on the spine, so `validate_git_backlog` is silent by
construction.

**`[#433]` — Done-when fully satisfied. Recommend an operator `/review-closures` act.**
Row at `BACKLOG.md:254`. Done-when: *"the K1–K5 spike is recorded AND an ADR records engine +
viewer + swap-out contract AND the three obligations discharged"*. Leg by leg:

| leg | status | evidence |
|---|---|---|
| K1–K5 spike recorded | MET | `docs/audits/2026-07-27-verification-433-schema-spike.md` exists; results quoted in ADR-107 §3 (`:145-152`) |
| ADR records ENGINE | MET | `ADR-107:114` `### 2. ENGINE — build-thin, with a fleet-owned schema` |
| ADR records VIEWER | MET | `ADR-107:141` `### 3. VIEWER — Backlog.md REJECTED; the slot ... declared EMPTY` |
| ADR records SWAP-OUT contract | MET | `ADR-107:183` `### 4. SWAP-OUT CONTRACT — what the gate must pin ...` |
| obligation 1 | DISCHARGED | `ADR-107:263` *"**6.1 Obligation 1 — feed schema findings into [#382]: DISCHARGED**"* |
| obligation 2 (§6.2 generality) | DISCHARGED | `ADR-109:287` `## Amendment — 2026-07-31 (§4 DISCHARGED ...)`; `:337` *"§4's obligation is **DISCHARGED**, so ADR-107 §6.2's generalization clause ... is met."* Landed by `[#383]` wave 1, merge `1afd9579`, proof commit `9a75777e` |
| obligation 3 | DISCHARGED | `ADR-109:140` `## §5 Obligation 3 — recorded DISCHARGED (architect ruling at the 2026-07-31 checkpoint)` |

The only text still asserting otherwise is `ADR-107:458` (its own 07-28 amendment), which
predates the 07-31 discharge and is immutable. Under ADR-70 Tier-1 closure is an operator act,
so this is proposed, never performed.

**Secondary defect inside the same row:** `[#433]`'s live text still reads *"**VIEWER =
Backlog.md**, piloted as a **replaceable part over our schema**, pinned, **swap-out contract
required**"* — directly contradicted by `ADR-107:141` (Accepted, ratified 2026-07-28), which
**REJECTS** Backlog.md on K1/K2/K3 FAILs and declares the slot EMPTY. `ARCHITECTURE.md:855`
carries the ADR's version correctly. The BACKLOG row is the stale surface.

**`[#244]` — closure candidate, needs a ruling (not asserted DEAD).**
Row at `BACKLOG.md:208`. Its shipped-phase prose says *"**P2/P3/P4 all SHIPPED 2026-07-04**"*
(spine: `25b104ed6` *"[#244] P4 sync surfacing SHIPPED"*, `a7504565f` *"[#244] P3 generated
methodology roster SHIPPED"*), and each Done-when clause maps onto a shipped phase: P2 PRUNE
records *"n=1 ruff-gate pruned+verified-ABSENT on ai-council v1.2.0"*, P3 gives *"the roster
regenerates without it"*, P4 gives *"per-repo drift surfaces in fleet_health"*. P5/P6 remain
`UNOWNED` but are **not named in the Done-when**. I am not calling this DEAD: verifying
"demonstrably REMOVED from a consumer and verified ABSENT" requires reading the ai-council tree,
which is not present here. **UNVERIFIABLE from the hub — routed as a ruling input.**

### 1.4 AWAITING-RULING

**`[#452]` — its Done-when is now UNSATISFIABLE as written. Needs re-scoping or retirement.**
Row at `BACKLOG.md:67`. Premise: *"the pilot-precedes-contract ruling makes [#433] sequence
before [#382] ... neither `tasks/433-*` nor `tasks/382-*` carries a `depends-on` clause at all"*.
Done-when: *"the pair is either expressed as a parseable `depends-on` clause or recorded as
intentionally prose-carried"*. Three verified facts break it:

- **`[#382]` has left BACKLOG.** `grep -c "^- \[#382\]" BACKLOG.md` = 0;
  `tasks/382-desired-state-data-model-intake-adr.md` frontmatter reads `status: closed`; closed
  at `f7abe228`.
- **A `depends-on` clause naming it would now hard-fail** — `validate_backlog` enforces strict
  reference-existence (`scripts/validate_backlog.py:127-136`). The first branch of the Done-when
  cannot be taken without REDding the gate.
- **The ordering the clause was meant to encode was violated in fact**: `[#382]` (the contract)
  closed while `[#433]` (the pilot that was to precede it) is still open.

Only the "recorded as intentionally prose-carried" branch remains available. Recommend narrowing
the row to that branch or retiring it.

**`[#424]` — its own census has drifted, and the fix as written REDs the gate.**
Row at `BACKLOG.md:53`. The row states *"Census 2026-07-26: 8 clauses, **4 parse, 4 do not**"*
and lists `L391 [#382] '381'` among the inert four. Live state:

| | count | ids |
|---|---|---|
| `depends-on` clauses live | **7** (not 8) | see below |
| parse (hashed) | 4 | `[#112]->#23` L41 · `[#169]->#171` L71 · `[#271]->#270` L260 · `[#348]->#270` L262 |
| inert (bare) | **3** (not 4) | `[#389]->390` L50 · `[#383]->382` L439 · `[#385]->383` L451 |

The missing eighth is `[#382] '381'` — the row that carried it closed. So `[#424]`'s census, the
row's load-bearing evidence, is stale.

**The latent trap.** Simulated the fix in-memory (repo untouched — `re.sub` over a string, then
`vb.parse` + `vb._check_dep_references`):

```
live dep-ref hard-fails: []
=== SIMULATED #424 fix (in-memory only, repo untouched) ===
  FAIL depends-on references non-existent id #382 — [#383] line 439
```

**Normalizing the bare ids RED-lights the gate on the first commit.** `[#383]`'s edge points at
a closed id, and it survived the closure precisely *because* the clause is inert — nothing
reference-checked it. `[#424]` must therefore either clean `[#383]`'s edge in the same change or
its Done-when ("every `depends-on` clause parses") ships a broken gate.

**`[#457]` — leg (ii) RESOLVED-IN-FACT; leg (i) not reproducible here.**
Row at `BACKLOG.md:80`. Both named tests still fail on this checkout:

```
FAILED tests/test_audit.py::test_check_fleet_parity_green_on_live_repo
FAILED tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row
```

- **(ii) — the census the row asks for is answered.** Failure text:
  `assert '1 declared routine row' in '2 declared routine row(s) name a consumer and a
  consumption_path ...'`. Live BACKLOG carries exactly **two** six-field ADR-105 routine markers:
  `[#348]` (L262) and `[#426]` (L270). **The live check is right and the test pin is the stale
  side.** `tests/test_audit.py:2377-2378` even says so: *"If this number moves, the ADR, the
  docstring and [#426] must move with it."* ADR-105 §4's "governs one row" and
  `scripts/audit.py:2531`'s docstring are both scoped "at acceptance", so both are historically
  correct and need no edit; only the test pin does.
- **(i) — UNVERIFIABLE in this clone.** The row predicts an ai-council `conftest.py` disposition
  WARN. The live failure is a different one:
  `.dev-knowledge hooks-armed WARN-undeclared: pre-commit config present but stage(s) NOT armed:
  commit-msg, pre-commit, pre-push`. That is this fresh cloud checkout (hooks never installed),
  not the described defect. The row's leg-(i) evidence cannot be confirmed or refuted from here.

**`[#401]` clause (a)** is ai-council-side config. **UNVERIFIABLE — the consumer tree is not
present in this clone.** Clause (b) is ruled-but-unbuilt; no hub organ named in it exists.

### 1.5 Cheap Done-when spot-checks (all confirm LIVE)

| id | Done-when probe | result |
|---|---|---|
| #396 | does `scripts/gitenv.py` exist? | **No** — `ls` = No such file. LIVE |
| #391 | is `fleet_analytics.py` wired to a nightly lane? | **No** — only ref outside `scripts/` is a `pyproject.toml:45` comment. LIVE (matches `ARCHITECTURE.md:247` "nightly wiring open #391") |
| #424 | is `_DEPID_RE` still hash-requiring? | **Yes** — `scripts/validate_backlog.py:82` `_DEPID_RE = re.compile(r"#(\d+)")`. LIVE |
| #452 | do `tasks/433-*` / `tasks/382-*` carry `depends-on`? | **Neither does.** LIVE-but-unsatisfiable (§1.4) |
| #335 | does `reconciled_versions` skip `templates/`? | **No** `templates` skip in `scripts/audit.py`. LIVE |

---

## §2 Closed-but-present drift

### 2.1 The validator

`python scripts/validate_git_backlog.py` (no flags; it hardcodes `HEAD` + `--first-parent` and
never gates — `main()` always returns 0):

```
validate_git_backlog: OK — no closed-but-present drift (direction (a) STRONG, full history)
```

Run **twice** — once pre-unshallow, once post. The pre-unshallow run was hollow (history floor
2026-07-27); the post-unshallow run genuinely covers 1286 first-parent commits back to
2026-03-30. Same verdict both times.

### 2.2 My independent pass

Method, deliberately *wider* than the validator on every axis: `git log --first-parent
--format='%H|%s|%b' HEAD` over all 1286 commits; regex `\bcloses?\s*\[#(\d+)\]` case-insensitive
(the validator's core is narrower); **no quoted-context stripping at all** (the validator's
`[#437]` precision lever deliberately removes backticked prose — I left it in so any FP would
surface); plus a second sweep on bare `\[#(\d+)\]` tokens.

```
first-parent commits parsed: 1286
open ids: 186
distinct ids with 'closes [#N]' on spine: 113
distinct ids with any '[#N]' on spine: 353
=== RAW closes-token INTERSECT open (my pass, NO quote-stripping) ===
(empty)
```

**Zero intersection. Full agreement with the validator, and the agreement is strong** — my pass
had the stripping lever disabled and *still* found nothing, which means the clean verdict does
not depend on that lever today.

### 2.3 What each pass misses (the honest part)

Neither pass sees the two real disposals, because **neither disposal was written as a commit
token**:

| id | disposed by | token on spine? | caught by |
|---|---|---|---|
| `[#455]` | `ADR-109:24` + §2 item 1, Accepted 2026-07-31 | **no** `closes [#455]` anywhere | only the ADR read (§1.3) |
| `[#433]` | ADR-107 §6.1 + ADR-109 §5 + ADR-109 amendment | **no** `closes [#433]` anywhere | only the obligation-by-obligation read (§1.3) |

`validate_git_backlog`'s own docstring scopes it honestly ("direction (a) only"), so this is a
**stated** blind spot, not a defect: an ADR that moots a row is invisible to a commit-message
scanner. The open `[#139]` (a.k.a. #90b, DEFERred, peg `#170`) owns direction (b) — merged-arc
content inspection — but even that would not catch an ADR-carried disposal. Worth noting as a
third direction nobody owns: *ADR-declared row disposal*.

I found no id the validator misses in the direction it does cover, and no false positive.

---

## §3 ADR corpus

### 3.1 Proposed set — the claim is CONFIRMED, exactly {82, 88, 89}

Verified across all **82** `docs/decisions/ADR-*.md` files. Status lines are heterogeneous
(`**Status:**`, `- **Status:**`, `Status:`, `status:`), so I ran two passes: a per-file
head-extract of every status-ish line, and a global regex over all four shapes:

```
$ grep -rniE '^\s*[-*]?\s*\*{0,2}status\*{0,2}\s*:?\s*.*proposed' docs/decisions/ADR-*.md
docs/decisions/ADR-82-handoff-process-v5-model-c.md:3:- **Status:** Proposed
docs/decisions/ADR-82-handoff-process-v5-model-c.md:63:**Status note.** This ADR's header remains `Proposed` ...
docs/decisions/ADR-88-file-oriented-dependency-management.md:5:**Status:** Proposed
docs/decisions/ADR-89-computed-code-dependency-edges.md:5:**Status:** Proposed
```

Three ADRs with no status line in their first 20 lines were checked individually and are all
Accepted (ADR-64 `:5`, ADR-94 `:3`, ADR-96 `:3`). Two further non-Accepted-but-not-Proposed
states exist and are correctly excluded: ADR-45 (`Status: Explored, not adopted`) and
ADR-46/ADR-47 (`Status: Partially superseded`). **Set complete and correct.**

### 3.2 ADR-82 — ratification input

1. **Decides:** HANDOFF_PROCESS v5 model C — CC owns and initiates the handoff, emits only the
   residual + drift-flags; a thin browser boot replaces the 8-file bundle; methodology enforced
   mechanically, referenced thinly; probes whose answers exist only in live state (`:27-37`).
2. **Changed since filing (2026-06-11):** the spec advanced **seven versions** while the ADR's
   amendment chain stopped at v5.2 (2026-06-17). Live: `protocols/HANDOFF_PROCESS.md:4`
   `Version: 6.0.1`. `CONTRIBUTING.md:209` ledgers every bump the ADR does not: v5.3 §5
   probe-manifest consolidation, v5.4, v5.5 §14 epic-lane, v5.6 §14a, v5.7 §16 functional/intake,
   **v6.0 one-round-trip boot** (merge `7f8a0473`, `[#446]`), **v6.0.1** `Destination` field
   (merge `65a549bf`). `grep -n "Amendment" ADR-82` returns only `:51` (v5.1) and `:65` (v5.2).
3. **The Council gate was waived, not passed** — `:11-15` and `docs/decisions/README.md:285`:
   *"the **Council gate was waived (#149)**, so **no transcript** exists"*.
4. **Recommend: RATIFY, with a v6 amendment marker in the same act.** The ADR is operative in
   every practical sense (`CLAUDE.md` §7 cites it as the authority for v6 handoffs), so the
   `Proposed` header is a pure record defect; but ratifying without recording v5.3->v6.0.1 leaves
   the decision record seven versions behind the spec it governs.
5. **Reason:** ADR-94 makes the status flip legal in place, and the amendment-vs-reopen
   convention makes the version catch-up an append. Both are cheap and neither reopens the
   model-C decision. This is exactly the header-vs-effective-status divergence `[#242]` is filed
   to mechanize.

### 3.3 ADR-88 — ratification input

1. **Decides:** repo files (markdown first) are the unit of dependency; edges are *declared*
   (`reconciled_with` / `serialize-group` / `depends-on`) and coherence is held by machinery, not
   memory (`:29-35`). Names the paradigm behind the coherence spine.
2. **Changed since filing:** it is **already ratified in-file** — `:167`
   `## Amendment — 2026-06-21: Accepted (operator ratification)`, *"Proposed -> Accepted"*, an
   operator edit, not a Council debate. `ARCHITECTURE.md:847` records it as *"both Accepted
   2026-06-21 (`911b561`)"*. Only the frozen header still says Proposed.
3. **Its four carried open questions are still carried:** OQ4 (`:165`) is data-gated on
   `logs/coherence-nudge.log` firing signal — and §1.2 shows that log has **never** existed. That
   gate cannot open on its own.
4. **Recommend: RETIRE the header divergence — flip to Accepted per ADR-94 Pattern B.** Do not
   re-ratify; it is already ratified.
5. **Reason:** ADR-94 (Accepted 2026-07-03) standardized the go-forward flip on Pattern B and
   `[#242]` exists specifically because ADR-88/89 are the two stragglers left on Pattern A. The
   flip retires the anomaly the check is being built to detect.

### 3.4 ADR-89 — ratification input

1. **Decides:** computed code-dependency edges — the computed-edge sibling to ADR-88; *declare
   what you cannot compute, compute what you can*; a language-server (Pyright) reverse-dependency
   oracle for code->code.
2. **Changed since filing:** same shape as ADR-88 — `:306`
   `## Amendment — 2026-06-21: Accepted (operator ratification)`; the Track-A oracle **shipped**
   (`scripts/reverse_dep_oracle.py`, `#193`) and OQ2 is RESOLVED per that marker.
3. **Live scope has grown past the doc:** `ARCHITECTURE.md:381` claims the edge organ is *"live
   on 13 rules"*; `audit.py::check_doc_code_edge` reports **14** (§4.2). ADR-89's own OQ3
   (advisory->gate promotion) remains data-gated.
4. **Recommend: RETIRE the header divergence — flip to Accepted per ADR-94 Pattern B**, same act
   as ADR-88.
5. **Reason:** identical to ADR-88 and they were ratified in one edit pass ("ADR-88 lands its
   back-reference in this same edit pass", `:314`); splitting the flip would re-create the
   asymmetry. Its open `[#220]` MODIFY-axis spike is unaffected either way.

### 3.5 Contradiction hunt among Accepted ADRs

**Read FULLY:** ADR-104 (113 lines), ADR-105 (102), ADR-106 (119), ADR-108 (88), ADR-109 (393),
and ADR-107 (463) by full section map plus verbatim reads of §1–§4, §6, §7 and its 07-28
amendment. **Sample-checked** every ADR dated after 2026-07-25 — the enumeration returns exactly
{105 (07-26), 106 (07-27), 107 (07-27), 108 (07-31), 109 (07-31)}, i.e. the same set, so the
sample and the full read coincide. ADR-104 (07-24) read in full as the immediate predecessor.

**FINDING C1 — ADR-107 vs ADR-109 on the §6.2 generalization clause. Real, quoted both sides.**

`docs/decisions/ADR-107-*.md:458` (inside its 2026-07-28 amendment):

> **[#433] remains OPEN** (§7.5). §6.2's generalization obligation — a *second* governed surface
> split by the same pattern, *shown* rather than asserted — is **still undischarged**, and closure
> remains an operator `/review-closures` act (ADR-70).

`docs/decisions/ADR-109-*.md:337-338`:

> §4's obligation is **DISCHARGED**, so ADR-107 §6.2's generalization clause — the precondition on
> **[#382]** declaring the fleet contract *general* — is met.

Both files are Accepted. The contradiction is **resolvable by sequence** (ADR-107's amendment is
07-28, ADR-109's is 07-31, landed `1afd9579`) and both are immutable, so neither is *wrong* to
have said what it said. **But nothing marks the resolution on the ADR-107 side**, and a reader
arriving at ADR-107 — the ADR that owns the obligation — is told it is undischarged. Recommend an
append-only marker on ADR-107 pointing at ADR-109's amendment. Consequence for the backlog: §1.3.

**FINDING C2 — ADR-108 vs ADR-109 on intake #22 §E. Real, and it also drifts a live doc.**

`docs/decisions/ADR-108-*.md:56-67`:

> **Intake #22 remains `status: SEED`; §C–§H are NOT ratified by this ADR.** Specifically
> unratified and still SEED-class (non-citable as ruled doctrine): ... **§E** fleet-management
> requirement ... §E in particular asks to "ratify this paragraph as the chain's functional
> requirement" — that ask is **live and unanswered**; this ADR does not grant it.

`docs/decisions/ADR-109-*.md:8` and `:45-53`:

> **Intake:** #22 §E (transcribed verbatim in §1; **ratified by promotion into this ADR** — the
> doc stays SEED, §C/§D/§F–§H open)
> ...
> `## §1 Functional requirement — intake #22 §E, verbatim`

Both dated 2026-07-31, both Accepted. ADR-109 landed **after** (`7ef40567`, 2026-07-31) ADR-108
(`65a549bf`). ADR-109 is internally careful — it lists "§C/§D/§F–§H open", pointedly excluding §E.
ADR-108's bullet list is not scoped to itself and is now false; ADR-108 carries **no** amendment
marker (`**Amends:** none.`, `:9`, and no `## Amendment` section exists).

**The drift escapes into a mutable doc**, which is the actionable half:
`docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md:7`:

> **NOTE 2026-07-31:** §A + §B ratified by promotion -> ADR-108. **§C–§H remain unratified.**

§E is inside "§C–§H" and was ratified the same day. That NOTE is editable and should read
"§C, §D, §F–§H".

**No other contradiction found.** Specifically checked and found *coherent*: ADR-104's 9-repo
declaration vs ADR-109's 5-column matrix (ADR-109's 2026-08-01 amendment `:341-393` corrects
exactly that gloss and states "**9 governs**", with the census table at `:368-376`); ADR-105's
one-governed-row boundary vs the live two rows (ADR-105 §4 is scoped "at acceptance", so it is
historically true — the *test pin* is the stale surface, §1.4); ADR-106's uv pin vs ADR-101's
Tier-1 set (ADR-106 `:117-119` records the lockstep amendment explicitly); ADR-107's
`**Amends:** ADR-65 (narrow)` vs ADR-65 (a declared narrow amendment, not a silent one);
ADR-109 §2's "no new physical contract file in v1" vs §8's `ecosystem/schema/` authorization
(a directory of *models*, not a persisted contract — internally reconciled at `:248-250`).

---

## §4 Doc currency

### 4.1 What IS mechanized (so the hunt below is scoped to what is not)

```
$ python scripts/validate_doc_claims.py
validate_doc_claims: OK — 4 claim(s) checked, no prose drift
         skipped  audit_check_count (doc - / actual <ground truth unavailable>)
           match  precommit_hook_count (doc 16 / actual 16)
           match  precommit_hook_roster (doc {16 ids} / actual {16 ids})
           match  pytest_collected (doc 2195 / actual 2195)

$ python scripts/validate_doc_rot.py
validate_doc_rot: OK — no history-accretion bloat past thresholds
```

Mechanized coverage is **four claims across two files** (`ecosystem/doc-counts.md` +
`CLAUDE.md` §9's hook roster), per `scripts/validate_doc_claims.py:12-24`. Everything in
`ARCHITECTURE.md`, `protocols/PLAYBOOK.md` and the rest of `CLAUDE.md` is unmechanized prose.

Two honest notes on the green:
- `audit_check_count` **SKIPPED** on the standalone CLI path — ground truth is *injected by the
  caller* (docstring `:16-18`), so this claim only actually checks under `audit.py run`. I closed
  it by hand: `python scripts/audit.py checks` enumerates **38**; `ecosystem/doc-counts.md:14`
  says *"audit: **38 registered checks**"*. **CONFIRMED.**
- `precommit_hook_roster` compares CLAUDE.md §9 against `.pre-commit-config.yaml` ids only —
  it does not check the *prose describing each hook*, which is where §4.3's findings live.

### 4.2 Unmechanized prose claims — verdicts

| # | doc:line | claim | verdict |
|---|---|---|---|
| 1 | `ARCHITECTURE.md:855` | `[#433]` "does **not** close on this ADR (§6.2's generalization obligation is **undischarged**)" | **DRIFTED** — discharged 2026-07-31 (`ADR-109:287`, `:337`; merge `1afd9579`). Doc's `last_reviewed: 2026-08-02` post-dates the discharge by 2 days |
| 2 | `ARCHITECTURE.md:381` | doc->code edge organ "live on **13** rules" | **DRIFTED** — `audit.py::check_doc_code_edge` returns `pass 14 doc->code edge(s) resolved`; `ecosystem/doc-code-edge.yaml` `coverage_scope` lists **14** ids |
| 3 | `ARCHITECTURE.md:427` | writes "`logs/parity-events.jsonl`" (lowercase) | **DRIFTED** — live path is `logs/PARITY-EVENTS.jsonl`: `scripts/fleet_parity.py:113` `EVENTS_PATH = _REPO_ROOT / "logs" / "PARITY-EVENTS.jsonl"`, `.gitignore:56`, and the file on disk. The [#395] UPPERCASE-KEBAB ruling (CLAUDE.md §9) conformed it 2026-07-22. **Same file is internally inconsistent** — `:245`/`:247` use the correct casing |
| 4 | `ARCHITECTURE.md:273` + `:852` | "ADR-104's **9**-repo declaration" | **CONFIRMED** — `ADR-104:15` "The fleet is **9 git repos**"; corroborated by `ADR-109:355-357` and the `[#462]` census |
| 5 | `ARCHITECTURE.md:248,259,432,591` | "**five** carriers (`globalconfig`/`plugin`/`precommit`/`floor`/`mesh`)" | **CONFIRMED** — `ls deploy/carrier_*.py` returns exactly those five |
| 6 | `ARCHITECTURE.md:826` | "Most-recent five are mirrored in CLAUDE.md §11" | **CONFIRMED** — `.claude/generated/recent-adrs.md` lists ADR-105..109; `gen_claude_rosters.py --check` exit 0 |
| 7 | `ARCHITECTURE.md:820-857` | governing-ADR roster currency | **CONFIRMED current through ADR-109** (`:856` ADR-108, `:857` ADR-109). The "roster through **106**" at `:29` is inside a dated *changelog* line ("Prior: 2026-07-27"), historical by construction — not a live claim |
| 8 | `ARCHITECTURE.md:187` | a generated `docs/ORGAN-INDEX.md` | **CONFIRMED (correctly framed)** — file absent, but the prose says "**will** become its verified source **once it ships** (**#132**)"; `[#132]` is open |
| 9 | `ARCHITECTURE.md:245,247` | `logs/BOUNDARY-DRIFT.md`, `logs/FLEET-ANALYTICS.md` | **CONFIRMED (correctly framed)** — absent from `logs/`, but both rows read "**ARMED (manual)**" for manual-CLI reporters; both are gitignored (`.gitignore:43,49`). Absence is expected |
| 10 | `ARCHITECTURE.md:846` | ADR-86 dashboard at `ecosystem/conformance.md` | **CONFIRMED (correctly framed)** — a ruled *location*, not an existence claim; `[#171]` is DEFERred (peg: post-Wave-1 n=2 consumers) |
| 11 | `ARCHITECTURE.md:267` + `:857` | `ecosystem/schema/desired_state.py` | **CONFIRMED** — `ls ecosystem/schema/` = `__init__.py`, `desired_state.py` |
| 12 | `ARCHITECTURE.md:772` | nightly-triage Issues "currently **15** open" | **UNVERIFIABLE** — GitHub-side state, not checkable from the tree. Matches `ADR-105:21` ("Fifteen remain open") as of 2026-07-26; staleness cannot be excluded |
| 13 | `CLAUDE.md:174` | coherence-nudge "logs `logs/COHERENCE-NUDGE.log`" | **CONFIRMED (mechanism claim, not existence)** — `scripts/coherence_nudge.py:41` sets that exact path; file created lazily, gitignored `.gitignore:73`, never fired (§1.2) |
| 14 | `CLAUDE.md:§12` | condensed block "19,017 bytes ... **44.6%** of the file", recoverable at `c30af862:CLAUDE.md` | **CONFIRMED** — `git cat-file -t c30af862` = commit; `git show c30af862:CLAUDE.md \| wc -c` = **42,663**; 19,017 / 42,663 = **44.57%**, matching the stated 44.6%. Current `CLAUDE.md` = 26,209 bytes |
| 15 | `CLAUDE.md:§5` | `docs/decisions/transcripts/` deleted 2026-07-22, do not recreate | **CONFIRMED** — directory absent |
| 16 | `PLAYBOOK.md:324` | "v2.1 template, **12** sections" | **CONFIRMED** — `templates/CLAUDE-md-template.md` has exactly 12 `## N.` sections; live `CLAUDE.md` also has 12 |
| 17 | `PLAYBOOK.md:640` | prompt "Standard structure (**8** sections)" | **CONFIRMED** — the enumerated block contains exactly 8 numbered items |
| 18 | `PLAYBOOK.md:2072` | "The canonical, drift-tracked roster lives in **CLAUDE.md §9**" | **CONFIRMED** — that is precisely the surface `validate_doc_claims` claim 2b checks (16/16 match) |
| 19 | `PLAYBOOK.md:2869` | "CLAUDE.md template structure (**10** sections)" | **STALE-BY-DESIGN (soft)** — live template is 12 (row 16). The line is a cell in a historical decision-routing table (a record of a past Council-#28-era call), not a live spec claim; flagged for awareness, no fix proposed |
| 20 | `PLAYBOOK.md:2710` | "existing **123** entries are grandfathered" (scope tagging) | **UNVERIFIABLE** — no deterministic LESSONS entry-counter exists, and the ADR-29 2026-07-17 archival exception permits entries to have moved to `LESSONS-legacy-*`. Not asserted either way |

### 4.3 Every file path cited in the three docs

Machine-extracted every backtick-quoted `*.py|md|yaml|json|toml|ps1|jsonl|log|tmpl|txt` token and
resolved it against the tree: **CLAUDE.md 50 distinct paths · ARCHITECTURE.md 102 ·
PLAYBOOK.md 127**. Every non-resolving token was triaged by hand. Outcome: **one genuine
path drift** (row 3 above, `logs/parity-events.jsonl`). All other non-resolvers fall into four
benign classes — grammar placeholders (`ADR-NN-topic.md`, `YYYY-MM-DD-slug.md`), deliberately
deleted files named as do-not-recreate (`CHANGELOG.md`, `BACKLOG_ARCHIVE.md`,
`.github/workflows/nightly-conformance-triage.yml`), consumer-side or `~/.claude` paths that do
not exist in the hub tree (`surface-closures.ps1`, `.claude/CLAUDE-FLOOR.md`,
`corp-monorepo/.claude/skills/gotchas/SKILL.md`), and bare basenames used generically in prose
(`settings.json`, `manifest.json`, `PROBES.md`, `state.yaml`).

### 4.4 Generator / gate `--check` sweep

| gate | exit | note |
|---|---|---|
| `validate_backlog.py` | 0 | 1 WARN (empty `[S24]`, expected) |
| `validate_git_backlog.py` | 0 | clean, full history |
| `validate_doc_claims.py` | 0 | 4 claims, 1 skipped by design |
| `validate_doc_rot.py` | 0 | clean |
| `validate_hermetization.py` | 0 | clean (nothing staged) |
| `gen_methodology_roster.py --check` | 0 | current |
| `gen_claude_rosters.py --check` | 0 | current |
| `gen_intake_index.py --check` | 0 | current |
| `gen_doc_counts.py --check` | 0 | `pytest_collected (file 2195 / actual 2195)` |
| `gen_audit_index.py --check` | **1** | **stale — see §4.6, it is a batch artifact, not repo rot** |

### 4.5 `uv` — ADR-106 is inoperative in this environment

`ADR-106:37` pins `uv==0.11.19`; `pyproject.toml:25` `required-version = "==0.11.19"`. Live:

```
$ uv --version
uv 0.8.17
$ uv run --locked python -c "print('ok')"
error: Required uv version `==0.11.19` does not match the running version `0.8.17`.
```

So **every gate invocation ADR-106 §4 routes through `uv run --locked` — all 14 pre-commit hook
entries, the Stop gate, the SessionStart hooks, the `verify` skill — cannot execute in this
clone.** This is an *environment* fact, not repo drift: the committed pin, lock and
`.python-version` are internally consistent, and the refusal is exactly the "refuse-don't-resync"
posture ADR-106 §4 specifies working as designed. Recorded because it means **no gate in this
tree was exercised through its real invocation path tonight** — every check above ran through a
substitute interpreter, and that is the honest scope of the green.

### 4.6 Two naming/index findings the morning batch must handle

**(a) The audit index is stale, and it is this batch's own doing.**
`gen_audit_index.py --check` exits 1: `docs/audits/README.md is stale vs docs/audits/`. At the
moment I ran it the diff was one line — `**366 audit documents.**` -> `**367**`, adding
`2026-08-03-night-ld-472-option-b.md`, then untracked and belonging to the concurrent L-D lane.
By the end of this lane the tree carried **six** untracked 2026-08-03 lane files:

```
?? docs/audits/2026-08-03-night-lb-groom.md            (this file)
?? docs/audits/2026-08-03-night-lc-w4-staging.md
?? docs/audits/2026-08-03-night-ld-472-option-b.md
?? docs/audits/2026-08-03-night-le-library-first.md
?? docs/audits/2026-08-03-night-lf-rulings-prep.md
?? docs/audits/2026-08-03-technical-night-la-w2-verification.md
```

This is **not pre-existing repo rot** — the 2026-08-02 L-D audit recorded this gate green. The
night lanes are read-only and so cannot run `--write`; the index goes stale by one per lane
output. The morning batch must run `python scripts/gen_audit_index.py --write` before its first
commit, or the `audit-index-freshness` pre-commit hook will block.

**(b) 5 of the 6 lane filenames are REFUSED by the hermetization gate, this file included.**
Verified by calling the gate's own predicate (`validate_hermetization.rule_b_violation`) on each
path:

```
BLOCK docs/audits/2026-08-03-night-lb-groom.md
BLOCK docs/audits/2026-08-03-night-lc-w4-staging.md
BLOCK docs/audits/2026-08-03-night-ld-472-option-b.md
BLOCK docs/audits/2026-08-03-night-le-library-first.md
BLOCK docs/audits/2026-08-03-night-lf-rulings-prep.md
pass  docs/audits/2026-08-03-technical-night-la-w2-verification.md
```

The BLOCK reason, verbatim:

```
class: '2026-08-03-night-lb-groom.md' has no CLOSED-enum <class> token after the date
(ADR-101 R3: technical/functional/qa/census/verification/ecosystem-audit/
conformance-nightly-digest/changelog-review/codex/fresh-eyes/incident-evidence;
whole-token longest-match)
```

`night` is not in `scripts/validate_hermetization.py:89` `AUDIT_CLASS_ENUM`. Every 2026-08-01 and
2026-08-02 lane file carries the class token (`2026-08-02-technical-night-batch-lb-...`) and
passes; **five of tonight's six dropped it**, and lane L-A's name — which kept it — is the control
proving the grammar still works. Renaming this file to
`2026-08-03-technical-night-lb-groom.md` returns `None` (clean), confirmed by the same predicate.

The gate is **prospective-only on staged ADDs** and nothing was staged, so nothing tripped
tonight. I wrote the file under the exact name my brief mandated rather than silently renaming
it — a read-only lane should not resolve a naming ruling by fiat. Recommend the morning batch
rename the five before staging.

---

## Coverage

**Covered, with live evidence for every claim:**

- All 186 BACKLOG rows classified (157 open / 29 deferred), counts cross-checked three ways
  (validator summary, raw grep, in-process `vb.parse`). Deferred baseline verified against the
  2026-08-02 L-F audit; delta 0.
- `validate_backlog.py` and `validate_git_backlog.py` run read-only, both before and after
  unshallowing (the first run's "full history" claim was hollow and is reported as such).
- An independent closure-token pass over all 1286 first-parent commits, deliberately wider than
  the validator on three axes, cross-checked against the 186 open ids.
- In-process simulation of the `[#424]` fix (no repo mutation) proving the dangling `#382` edge.
- Two `[#457]` tests executed; failure text quoted verbatim.
- All 82 ADR status lines enumerated across four status-line grammars; the Proposed set proved
  complete by construction, not by sampling.
- ADR-104/105/106/107/108/109 read in full (ADR-107 by full section map plus verbatim §1–§4, §6,
  §7 and its amendment). The post-2026-07-25 sample set is identical to the full-read set.
- ~20 named prose claims in ARCHITECTURE / CLAUDE / PLAYBOOK verdicted, plus a machine-extracted
  resolution of all 279 distinct file-path citations across the three docs.
- Ten read-only gates / generators run in report or `--check` mode.

**NOT covered, and why:**

- **`[#244]`'s consumer-side leg** ("REMOVED from a consumer and verified ABSENT") and
  **`[#401]` clause (a)** (ai-council `settings.yaml`): the consumer trees are not present in this
  clone. Marked UNVERIFIABLE rather than guessed.
- **`[#457]` leg (i)**: not reproducible here — this fresh checkout's unarmed pre-commit hooks
  produce a different `fleet_parity` WARN than the row describes, masking the stated evidence.
- **`ARCHITECTURE.md:772`'s "15 open" GitHub Issues**: remote state, not checkable from the tree.
- **`PLAYBOOK.md:2710`'s "123 entries"**: no deterministic counter, and ADR-29's archival
  exception makes a hand count unsound.
- **Real gate-path execution**: `uv run --locked` refuses in this environment (§4.5), so no gate
  was exercised through its production invocation path. Every green above was produced by a
  substitute interpreter matching `uv.lock`'s pinned versions.
- **Done-when verification for the 148 LIVE ids** was *structural* (parse validity, band,
  Done-when presence, absence of any spine closure token, premise survival) plus five targeted
  probes — **not** a per-row semantic re-derivation. A row whose Done-when is quietly satisfied by
  work that named no id and left no artifact this pass touched could still be hiding in that set.
  `[#455]` and `[#433]` were found because their disposals were written into ADRs I read in full;
  an equivalent disposal written somewhere I did not read would have been missed.
- **`git fetch --unshallow` was executed** — refs only, no checkout, no merge, no working-tree or
  index change, and it advanced only the remote-tracking ref `origin/main`. Declared here because
  it is the one command in this lane that wrote inside `.git/`.

---

> **Editor's note (wrap, lane L-A) — this file was RENAMED before commit.** It was written to
> the brief's mandated path `docs/audits/2026-08-03-night-<lane>.md` and is committed as
> `docs/audits/2026-08-03-technical-night-<lane>.md`. Reason: the mandated pattern is refused
> by this repo's own `validate-hermetization` Rule B — `night` is not a member of the ADR-101
> R3 closed class enum (`scripts/validate_hermetization.py:89-98`). Inserting the `technical`
> class token is what every 2026-08-01/02 night-batch sibling already does. **The gate was not
> weakened, bypassed or amended.** Any occurrence of the old `2026-08-03-night-...` form below
> is preserved deliberately as the evidence that produced this finding — it is a quotation of
> the blocked name, not a live path. Verified post-rename: `rule_a_violation` and
> `rule_b_violation` both return `None` for all seven artifacts of this batch.
