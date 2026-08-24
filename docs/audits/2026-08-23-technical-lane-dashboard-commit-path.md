# LANE L4 — Generated-output commit path + freshness gate (M8 + `[#171]` leg 1)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-23 · **Slug:** `lane-dashboard-commit-path`
- **Lane:** L4, batch of 2026-08-23 · **Worktree:** `worktree-dashboard-commit-path`
- **Merge base:** `aeec0fd1` (`main`, "Merge branch 'chore/phase0-preconditions-2026-08-23'")
- **Governing contract:** `LANE-L4-dashboard-commit-path.md` (REISSUE, 2026-08-23) — frozen,
  immutable to this lane
- **Ruling executed:** **R1 — option (b)**, plus a freshness leg that is not a writer. This lane
  executed the ruling; it did not evaluate it, and found no rule-vs-ruling conflict.

---

## 1. Ground truth (Step 1)

Everything in this section was measured live in the lane worktree at merge base `aeec0fd1`,
before any file in this lane was edited.

### 1.1 The two artifact strings, verbatim

Both are **committed artifact text**, quoted from the tracked files rather than from the
generator that emits them.

`ecosystem/conformance.md:7` —

```
> **Generated, committed, read-only** (ADR-86 location + ADR-80 zone class). It answers four standing operator questions — what finished, where the telemetry is, whether the intakes passed their gate, and whether implemented ADRs are archived — and it **reports rather than repairs**: every VIOLATION and flag below is left exactly where it was found.
```

`ecosystem/conformance.html:45` —

```
<p class="note">Generated, committed, read-only (ADR-86 location + ADR-80 zone class). It reports rather than repairs: every VIOLATION and flag below is left exactly where it was found.</p>
```

Their emitters are `scripts/gen_dashboard.py:931` (`_preamble`) and `scripts/gen_dashboard.py:1175`
(`render_html`).

**A third false claim, in the same family, that the contract's "two strings" does not name.** The
generator's own module docstring, `scripts/gen_dashboard.py:9-11`:

```
LOCATION + ZONE CLASS are ruled, not chosen here: ADR-86 puts the dashboard at
`ecosystem/conformance.md` as an ADR-80 **committed-generated** zone -- a read-only validator
generates it and commits its own output.
```

This is the sentence the Phase-0 packet quotes as *the root* (§Premise B). It is not an artifact
string — it never reaches `ecosystem/` — but it asserts the same non-existent mechanism, to the
next reader of the code rather than the next reader of the dashboard. Corrected in Step 3 and
recorded here so the correction is not mistaken for scope creep.

### 1.2 What runs `gen_dashboard.py` today — **nothing**

Searched every arming surface in the repo (`.pre-commit-config.yaml`, `.claude/settings.json`,
`*.yaml`/`*.yml`/`*.json`/`*.ps1`/`*.py`/`*.md`), excluding the generator, its own outputs, its
test file and prose that merely names it:

```
grep -rn "gen_dashboard" --include=*.yaml --include=*.yml --include=*.json \
     --include=*.md --include=*.ps1 --include=*.py .
grep -rn "dashboard" .pre-commit-config.yaml .claude/settings.json   ->  rc=1 (no match)
```

Every hit is prose (`ARCHITECTURE.md`, `JOURNAL.md`, the handoff bundle) or
`tests/test_gen_dashboard.py`. **No hook, no session hook, no scheduler, no routine, no CI job
invokes it.** Its only non-test caller is a human typing the command.

This is R3 **F5** — `--check` armed nowhere — and the Phase-0 packet is explicit that F5 is a
**different defect** from this lane's (a gating gap, not a writer gap). It is recorded here as
measured ground truth, **not fixed**: arming `--check` is not in this lane's closure contract, and
the ship-gate leg this lane does arm (§5) answers a different question — *is the committed output
current?* — from the one `--check` answers — *does the output byte-match a regeneration?*

### 1.3 Who consumes the output

| Consumer | Site | Nature |
|---|---|---|
| `ARCHITECTURE.md` Ch2 organ map | `ARCHITECTURE.md:335-348` | Doctrinal pointer, required by **ADR-86 §3** ("lands with the build, not before"). Already carries the honest-limits note naming F3 and F5. |
| The operator, by opening the file | `ecosystem/conformance.md` · `ecosystem/conformance.html` | The HTML sibling exists (operator addendum, 2026-08-19) precisely so the artifact is **openable without running anything** — which is what makes a stale committed copy a stale *trust surface* rather than a stale cache. |
| `ADR-85 R2` / `[#169]` staleness signal | Designated landing site (ADR-86 §4) | Designated, not yet wired. |

No machine consumer reads it. That matters for the freshness leg's severity: a stale dashboard
misleads a **reader**, it does not corrupt a computation.

### 1.4 How stale it is right now — the number

Artifact's last commit — both faces, one commit:

```
5e776542c5d14f226cad101a36bb450d598bcfe7  2026-08-20  rdwornik
docs(dashboard): regenerate over every landing of the day, and anchor the Codespaces landing
```

Newest commit date per declared input path (§5.1 derives the set), by the relation the leg
finally shipped with — **committer date, `--first-parent`** (§5.2 says why both halves matter):

```
2026-08-23  BACKLOG.md
2026-08-23  tasks/
2026-08-23  docs/intake/
2026-08-22  docs/decisions/
2026-08-24  docs/audits/            <- newest
2026-08-19  scripts/gen_dashboard.py
2026-08-22  scripts/gen_task_tree.py
2026-08-03  scripts/gen_intake_index.py
2026-08-13  scripts/gen_claude_rosters.py
```

| Metric | Value at `aeec0fd1` |
|---|---|
| **Staleness, in days** (newest input commit date − artifact commit date) | **4** (2026-08-24 − 2026-08-20) |
| Commits on `HEAD` since the artifact was committed | **213** |
| …of those, on the first-parent spine | **42** |
| …of those, touching the declared input set | **78** |
| `gen_dashboard.py --check` | **rc=1** — `STALE ecosystem/conformance.md`, `STALE ecosystem/conformance.html` |

The day-delta (**4**) is the metric the §5 leg uses, because it is the metric probe **P5** uses for
the same question. The commit counts are recorded as context: they are what makes "4 days" concrete
— **42 first-parent landings** happened against a dashboard that claims to describe the repo.

**This number read 3 until 2026-08-24, and the correction is worth more than the digit.** The first
measurement here was taken with the leg's FIRST relation — author date, no `--first-parent`, and
listing only the DATA half of the input set. Both halves of that relation were later replaced
(§5.2: committer date on both sides; §5.1: DATA + CODE inputs), and **nobody re-derived the number
they had produced**. `docs/audits` reads `2026-08-23` by author date and `2026-08-24` by committer
date, so the ground-truth metric — and the `baseline_days` constant taken from it — sat one day
wrong, describing a measurement the code no longer performed. Found by terra at **round 8**, after
seven rounds had graded it clean. It is the lane's own defect class, one level up: a true-sounding
number about a mechanism that had moved underneath it. Corrected in place here, in
`generated_artifact_freshness.DASHBOARD`, in the pinning test, in §5.3, in the ADR-86 amendment and
in intake #42 — every site that carried it.

### 1.5 Library-first check — the internal move, and the absence it found

The contract asks for the generator that already commits its own output, to follow its shape.

**There is none.** Every `git add` / `git commit` subprocess site in `scripts/` was enumerated:

| Site | What it is |
|---|---|
| `scripts/enforcement_coverage.py:493,494,515,516,635,636` | Builds throwaway probe **clones** to prove gates fire. Not the repo. |
| `scripts/nopack_sandbox.py:1167,1176` | Sandbox fixture tree. Not the repo. |
| `scripts/review_closures.py:187` | `git_commit_exists` — a **read**. |
| `scripts/single_flight.py:419` | `git cat-file commit` — a **read**. |
| `scripts/cloud_provisioning.py:322` | Compares `cat-file -t` output to the string `"commit"` — a **read**. |

**No generator in this repo commits its own output.** Per the contract, that absence is itself a
finding, and it is the strongest single piece of evidence for R1 option (b): the ruling does not
decline a working convention in favour of prose — it ratifies the **only** convention the repo's
generators have ever actually run.

> **CORRECTION — this census was wrong once, and the wider claim it originally carried is
> withdrawn.** Step 1 as first written said *"ADR-80 §3's writer policy has zero implementations
> here."* **That is false.** `scripts/audit.py::_commit_routine_outputs` (`:3991`) is a complete
> ADR-80 §3 writer: it commits its own durable audit outputs, pathspec-bounded (Rider 1) and
> fail-soft (Rider 2). The sweep above could not see it because it commits via `commit-tree`
> plumbing against a separate `GIT_INDEX_FILE` — not `git add` / `git commit` — so a search keyed
> on those two verbs was structurally blind to it. **Found by the terra reviewer (round 2,
> 2026-08-23), corrected in the ADR-86 amendment, this artifact, and the generator docstring.**
>
> The narrow claim survives and is what the ruling actually rests on: **no *generator* commits its
> own output.** And the correction *strengthens* (b) rather than weakening it — the repo's one
> ADR-80 §3 writer exists for an **unattended nightly routine**, and writes to the orphan
> `automation/fleet-audit` branch precisely so `main` is never touched. That is the ADR-84
> isolation pattern applied to the case ADR-84 is for. The dashboard is the opposite case: a
> person regenerates it, on `main`, as a navigable surface. So the single existing implementation
> is evidence about *which* jobs need a self-committing writer, and this is not one of them.
>
> Recorded as a correction rather than silently rewritten, because a lane whose subject is *"the
> artifact's self-description is not its mechanism"* does not get to quietly fix its own false
> claim about the mechanism.

The shape every generator does follow, verified across `gen_task_tree`, `gen_audit_index`,
`gen_intake_index`, `gen_doc_counts`, `gen_methodology_roster`, `gen_claude_rosters`,
`generate_organ_index`, `gen_intake_tree`:

> **write → print what was written → a human commits it → a `--check` regen-and-diff pre-commit
> hook refuses a stale copy.**

`gen_dashboard.py` implements the first two legs and has the fourth available but unarmed (§1.2).
Steps 3–5 make it honest about the third and give it the freshness half of the fourth.

---

## 2. The ruling, and what executing it meant (Step 2)

**R1, executed not evaluated.** The contract names one condition under which this lane may stop
and ask — a genuine rule-vs-ruling conflict, of which "implement (a) instead of (b)" is the named
instance. **No such conflict arose.** The derivation ran the other way: the library-first sweep
(§1.5) found that **no generator** in this repo commits its own output, so (b) is not a concession
to convenience — it ratifies the only convention this repo's generators have ever actually run.
The repo's single ADR-80 §3 writer (`audit.py::_commit_routine_outputs`, found by terra and
recorded in §1.5's correction) is an unattended nightly routine writing to an isolated
`automation/*` branch — the ADR-84 case, not this one.

**Form.** `docs/decisions/ADR-86-conformance-dashboard-location.md` gains an **appended
`## Amendment — 2026-08-23`** marker at the file end. §2's original decision text is
byte-unmodified. The form is not a choice this lane made: `CLAUDE.md` §5 rule 3 and
`protocols/STANDING_RULINGS.md` **J-3** both prescribe it, and ADR-94's in-place exception is
scoped to the *status line* only — which this amendment does not touch (ADR-86 stays **Accepted**).

**What the amendment withdraws, and what it keeps.** Withdrawn: only the clause that the
**validator itself** commits. Kept: the location, the ADR-80 **committed-generated** zone class
*and its name*, the Layer-2 posture, pathspec-boundedness, and the diffable-and-auditable
rationale that rejected generate-on-demand. The zone class was always a claim about the artifact's
**state** — committed rather than regenerated on demand — and (b) preserves that property whole.
**ADR-80 §3 is not repealed:** it remains live doctrine for any unattended job that dirties the
tree. It is simply not this artifact's mechanism, and ADR-86 no longer says it is.

**A third thing the amendment settles, which the contract did not ask for but §2 left open.**
ADR-86's *Deferred to the build (#171)* paragraph explicitly deferred "the exact write channel
(committed on `main` as a navigable surface vs. an `automation/*` branch per the ADR-84
writer-isolation pattern)". (b) answers it: **committed on `main`**. ADR-84's isolation pattern
exists for *unattended* writers, and under (b) there is no unattended writer. Recorded because
leaving a settled fork marked "deferred" is the same class of stale claim this lane exists to
remove.

**One in-place edit, disclosed.** `docs/decisions/README.md`'s ADR-86 row carried the withdrawn
claim in its own editorial one-liner ("a read-only validator generates + commits its own output").
That file is a **living index**, not an immutable ADR, and its ADR-101 / ADR-104 rows already
carry in-row `**Amended <date>**` clauses — so the same in-place form was used. Left alone, the
index would still be describing a superseded reading of a file it points at.

---

## 3. Both artifact strings corrected — and the third site (Step 3)

The contract names two strings. **Three sites** carry the same false mechanism; all three are
corrected, and the third is called out rather than folded in silently, because it sits outside the
contract's literal wording.

| # | Site | Reaches | In the contract's "two strings"? |
|---|---|---|---|
| 1 | `gen_dashboard.py::_preamble` → `ecosystem/conformance.md:7` | The operator opening the markdown | **Yes** |
| 2 | `gen_dashboard.py::render_html` → `ecosystem/conformance.html:45` | The operator opening the HTML | **Yes** |
| 3 | `gen_dashboard.py` module docstring `:9-11` | The next reader of the code | **No** — but it is the sentence the Phase-0 packet quotes as *the root* (§Premise B) |

**Not made true by being made vague.** The contract names the risk precisely: *"Generated" is not
an honest replacement for a false "generated and committed."* Both faces now state the mechanism
in full — **who** commits (the person or integrator who ran `--write`), **that** the generator
commits nothing, **what the commit is bounded to** (pathspec-bounded, both faces), **when the copy
is current to** ("nothing refreshes this file automatically: it shows the tree as of the last time
somebody ran `--write`, and it reaches the repo only when they commit it"), and **which ruling**
they describe (ADR-86 amended 2026-08-23).

> **The first wording of that currency clause was itself false, and terra caught it (round 5).**
> It read *"this copy is exactly as current as its own last commit, never fresher"* — which is
> wrong for the copy a reader is most likely to be looking at. `--write` deliberately leaves a
> **newer, uncommitted** working-tree copy; "never fresher" is exactly the state the intended
> workflow produces. A precise-sounding sentence, describing a state the mechanism does not have,
> inside the commit that exists to remove one. The replacement is true of both copies and still
> names the mechanism rather than retreating into vagueness.

**Both committed faces were regenerated**, so the correction is live on the surface a reader
actually opens — not merely in the generator that could produce it. Correcting the emitter and
leaving the committed artifact carrying the false string would have reproduced the exact failure
this lane exists to fix: judging a mechanism by its header rather than by the thing itself.

**Six tests pin it** (`tests/test_gen_dashboard.py`). A negative assertion alone would have been
insufficient — deleting the sentence entirely passes "the false string is gone" while telling the
reader nothing — so the positive content is asserted too: each face must name who commits, must
say what it is current to, and must cite the amendment. The sixth covers the docstring site.

---

## 4. The commit path, explicit and observable in the code (Step 4)

The contract's fourth closure condition is the sharp one: the human/integrator commit path must be
**observable in the code, not merely described in prose**. Prose describing a mechanism is exactly
what `[#171]` leg 1 already had, and it is what fooled an integrator review pass.

**What landed in `scripts/gen_dashboard.py`:**

- **`commit_pathspec()`** — derived from `_TARGETS`, the same tuple `write_outputs` iterates. The
  pathspec therefore *is* the write targets, never a re-typed literal that can drift from what was
  actually written. ADR-80 **Rider 1** ("stages exactly its own declared output paths — never
  `git add -A`") survives the amendment intact: what (b) changes is **who runs** the commit, not
  what it is bounded to.
- **`commit_path_commands()`** — the two-command path as **argv lists**, built in code. The
  pathspec is on the **`commit`**, not only on the `add`: a bare `git commit -m …` sweeps up
  whatever is already staged, so bounding only the `add` would leave an operator with unrelated
  staged work committing it by accident *while both faces tell them the commit is bounded*. That
  is terra's finding (2026-08-23) and it is the same defect class as the header this lane exists
  to fix — a true-sounding claim about a mechanism that does not hold.
  `test_advertised_commit_path_leaves_unrelated_staged_work_alone` runs the advertised commands
  in a real repo with an unrelated file staged, and asserts it survives uncommitted.
- **`render_commit_path()`** — the same commands as copy-pasteable shell.
- **`--commit-path`** — a CLI verb printing exactly those commands. It needs no git and touches no
  file, so an integrator or a runbook can ask the generator what its commit path *is* without
  running anything.
- **`--write` prints the path it did not run**, every time, immediately after writing.
- **Both artifact faces carry the same pathspec**, sourced from the same function.

Live output:

```
$ python scripts/gen_dashboard.py --write
gen_dashboard: wrote ecosystem/conformance.md
gen_dashboard: wrote ecosystem/conformance.html
gen_dashboard: NOT committed. This generator has no writer of its own; a human or integrator commit satisfies "committed" (ADR-86 amended 2026-08-23).
gen_dashboard: commit path, pathspec-bounded to exactly the files just written:
    git add -- ecosystem/conformance.md ecosystem/conformance.html
    git commit -m "docs(dashboard): regenerate ecosystem/conformance.{md,html}" -- ecosystem/conformance.md ecosystem/conformance.html
```

**And the negative half is asserted where it cannot lie.** A header that says "commits nothing"
can be wrong — that is this entire lane. So a test runs `--write` against a **real git repo** and
asserts that HEAD has not moved and both outputs are sitting dirty afterwards. That is the ADR-81
leg **(e)** functional proof for the ruling's negative half: not "the code appears to have no
writer", but "it was observed not to write".

*(Asserted behaviourally rather than by monkeypatching `subprocess.run`, which would rewrite the
stdlib module object for the whole xdist worker.)*

---

## 5. The freshness leg (Step 5)

### 5.1 The input set, named — and it *is* derivable

The contract's hardest constraint: *define "older than its inputs" concretely; name the input set;
if it is not derivable, report the gap rather than inventing a proxy.*

It is derivable, and from the generator's own constants rather than from judgment. The set has
**two halves** — what the artifact is rendered *from*, and what *renders* it.

**Data half — `gen_dashboard.DATA_INPUT_RELPATHS`:**

| Input | Read by | Generator constant |
|---|---|---|
| `BACKLOG.md` | `closed_rows_*`, `theme_stats`, `_rows_by_id` | `BACKLOG_RELPATH` |
| `tasks/` | `theme_stats` (the `tasks/` tree) | `TASKS_RELDIR` |
| `docs/intake/` | `intake_rows` (incl. `archive/`, which is inside it) | `INTAKE_RELDIR`, `INTAKE_ARCHIVE_RELDIR` |
| `docs/decisions/` | `adr_rows` | `DECISIONS_RELDIR` |
| `docs/audits/` | `gate_health` | `AUDITS_RELDIR` |

**Code half — `gen_dashboard.CODE_INPUT_RELPATHS`:** `scripts/gen_dashboard.py` itself plus the
three parsers it borrows at module scope (`gen_task_tree`, `gen_intake_index`,
`gen_claude_rosters`), derived from the `PARSER_MODULES` tuple the loads themselves iterate — one
list, used twice, rather than two lists that can drift.

**The code half was missing from the first version of this leg, and terra found it (2026-08-23).**
It is not a completeness nicety: a parser rewrite changes what `build()` renders while no data
path moves, so a data-only input set would have reported the artifact **fresh forever** across
exactly the change most likely to invalidate it. That single omission would have made the leg
decorative. `test_live_a_generator_source_change_alone_makes_the_artifact_stale` is the regression
proof — nothing in the data moves in that test, and the verdict is `stale`.

The union is exported as **`gen_dashboard.INPUT_RELPATHS`** — a declaration in the generator, not
a re-derivation in the gate.

**Two inputs are deliberately excluded, and both exclusions are stated rather than silent:**

1. **`logs/TELEMETRY.db`** — read by `telemetry_state` (existence + size), but **gitignored**
   (`.gitignore:95`) and absent from disk. It has no git history, so it cannot carry a commit date
   and cannot take part in a git-date relation. It is declared in the artifact spec's
   `untracked_inputs` field, so the carve-out is visible in code rather than missing from a list.
2. **HEAD itself** — `head_sha()` and `head_date()` are inputs to the *rendering*, not to the
   *content*. This is the load-bearing distinction, and it is why this leg can carry a baseline at
   all: because the dashboard prints HEAD's sha and commit date, **any** commit makes a
   regeneration differ — which is precisely why `gen_dashboard.py --check` "reports drift after
   HEAD moves" by the generator's own admission. A gate keyed on that would fire on every commit
   in the repo and be routed around within a day. Keying on the content input set asks the
   question an operator actually cares about: *has anything the dashboard describes moved since
   the dashboard was committed?*

### 5.2 The relation — probe P5's shape, not a second idiom

P5 asks whether `ARCHITECTURE.md`'s `last_reviewed` stamp is on-or-after that file's last git
touch: a relation between two git dates, passing on-or-after. The same relation, different subject:

```
staleness_days = max(0, newest_input_commit_date − stalest_output_commit_date)
WARN  iff  staleness_days > baseline_days
```

- **`min` over the outputs** — the two faces are written by one run and normally share a commit,
  but if one ever lagged, the pair is only as fresh as its stalest half.
- **`max` over the inputs** — any single input moving forward is what makes the artifact stale.
- **Committer date (`%cs`), on both sides** — the one place the leg deliberately diverges from its
  sibling, and terra forced the divergence over two rounds (2026-08-23). `canonical_freshness_gate`
  uses **author** date, and for *its* subject that is right: it compares a git date against a
  `last_reviewed` stamp a human wrote, so its question is *when was the content edited*, and author
  date survives rebase / cherry-pick / amend. This leg compares **two git dates against each
  other**, and its question is *did any input land in this history after the artifact landed* — an
  ordering question about **this** history, which is what committer date records.

  Author date is wrong here in **both** directions, and terra demonstrated each separately: a
  cherry-picked **input** keeps its original author date and hides behind it (reported `fresh`
  while the checked-out input is genuinely newer); a rebased **output** keeps its old author date
  and produces a spurious `stale`. An intermediate version took `max(author, committer)` on inputs
  and `min` on outputs to be conservative in both directions — which closed the first hole, left
  the second open, and gave the module no single stated relation at all. Committer date on both
  sides is **one semantic that answers the actual question**; a whole-branch rebase rewrites every
  committer date uniformly, so relative order — the only thing this relation reads — is preserved.
  Both directions are pinned live:
  `test_live_a_cherry_picked_input_cannot_hide_behind_its_author_date` and
  `test_live_a_rebased_output_is_not_spuriously_stale`.
- **Repo-location env vars are scrubbed** via `gitenv` (loaded by path, per that module's
  terra-hardened contract): an inherited `GIT_DIR` overrides both `cwd=` and `git -C`, which is how
  a validator comes to read the parent repo while labelling the answer with the target's id
  (`[#355]`). A live test proves the scrub by pointing `GIT_DIR` at a decoy repo. **If `gitenv`
  cannot be loaded the function refuses to answer rather than answering unscrubbed** — a wrong
  verdict delivered silently is strictly worse than no verdict.

The module is **`scripts/generated_artifact_freshness.py`** and returns `(fails, warns)` — the
identical signature to `canonical_freshness_gate.evaluate`, so the two freshness organs cannot
drift into two shapes.

### 5.3 The baseline is measured, and it is a ratchet

Re-derived at merge base `aeec0fd1` **with the relation the module actually ships** — committer
date, first-parent spine (§5.2), over the full DATA + CODE input set (§5.1):

```
$ git log -1 --first-parent --format=%cs aeec0fd1 -- ecosystem/conformance.md   ->  2026-08-20
$ git log -1 --first-parent --format=%cs aeec0fd1 -- ecosystem/conformance.html ->  2026-08-20
$ git log -1 --first-parent --format=%cs aeec0fd1 -- docs/audits                ->  2026-08-24  (newest input)
                                                                    staleness =  4 days
```

**`baseline_days = 4`**, and a test pins the number rather than leaving it a comment — silently
raising a baseline rebases the metric the gate exists to hold, a failure mode this repo has already
caught once at terra HIGH (`audit.py:2288`).

**It read 3 until terra's round 8, and that pin is exactly why the correction is cheap.** The 3 was
measured with the module's first relation (author date, no `--first-parent`) and never re-derived
when §5.2 replaced it; `docs/audits` differs by one day between the two date semantics. A constant
that outlives its measurement is the same defect as a header that outlives its mechanism — this
lane's whole subject. `test_dashboard_baseline_is_the_measured_value` was mutation-checked in both
directions (3 and 5 each RED it) so the number cannot drift back silently.

**The honest reading of "4" is not "four days of drift is acceptable."** It is *this repo
tolerated four days of drift once, and the leg forbids worse.* Tightening it is a later act.

**WARN, never FAIL — and the class is load-bearing rather than timid.** Verified against the two
gates' own source, not assumed:

- `audit.py::cmd_health` (the **pre-commit** gate) computes `self_fail = any(f.status == "fail")`
  and exits 1 only on that. **A `warn` does not block a commit.**
- `cmd_ship_gate`'s contract: *"any `warn` NOT dispositioned by the register → RED, exit 1."*

So a WARN-class Finding's **teeth** are at ship time. The leg also emits **one Finding per
artifact**, which the ship-gate's disposition contract requires (a matched token suppresses a whole
Finding, so aggregate organs must split). `evaluate` returns `fails == []` **unconditionally, by
construction**, with the reason written on the function: promotion to FAIL is a later act with its
own ruling, and one line.

**But the status class alone was not enough, and terra caught the gap between the verdict and the
work.** `cmd_health` runs *all* of `ALL_CHECKS`, so a WARN-class check still **spends its cost** on
every commit even though it cannot block one — an earlier draft of this section claimed it "taxes
no ordinary commit", which was true of the blocking and false of the runtime. Measured: **11
`git log` calls** for the dashboard, ~3.0s wall clock under this window's heavy contention (an
earlier version spent **20**, querying every input twice — also terra's finding). So the
registration uses **`_GATE_MODE`**, which is `audit.py`'s own existing answer to exactly this
problem — `check_doc_claims` already runs its expensive leg as `run_expensive=not _GATE_MODE`. At
the commit gate the leg returns an honest `n/a` NOT-APPLICABLE **without measuring anything**; at
ship time it measures. That is what makes *"ship-gate, not pre-commit"* true of the **work** and not
only of the verdict — and it reuses an idiom rather than inventing a second one.
`test_generated_artifact_freshness_is_skipped_at_the_commit_gate` proves it by making the date
function raise: if the leg measures under `_GATE_MODE`, the test fails.

### 5.4 It was observed to fire

ADR-81 leg **(e)**: presence is not proof. The leg's body — the exact code in the §5.5 fenced
diff, executed verbatim rather than paraphrased — was run against **five** trees. Re-run
2026-08-24 after the baseline correction, so the transcript below is of the code as it stands:

```
--- live repo ---
          pass  generated_artifact_freshness: conformance-dashboard: 0d stale (baseline 4d) — ecosystem/conformance.md committed 2026-08-24, newest input docs/intake committed 2026-08-24
--- a real repo with no dashboard ---
           n/a  generated_artifact_freshness: [n/a-reason:SUBJECT-ABSENT] output(s) not present in this repo — ecosystem/conformance.md, ecosystem/conformance.html
--- a tree that is not a repo at all ---
   unavailable  generated_artifact_freshness: git is unavailable here — freshness cannot be measured
--- a genuinely stale tree ---
          warn  generated_artifact_freshness: conformance-dashboard: 22d stale (baseline 4d) — ecosystem/conformance.md committed 2026-08-01, newest input BACKLOG.md committed 2026-08-23; regenerate + commit: python scripts/gen_dashboard.py --write
--- the commit gate (_GATE_MODE) ---
           n/a  generated_artifact_freshness: [n/a-reason:NOT-APPLICABLE] ship-gate-only leg — skipped at the audit-health commit gate (ADR-86 amd. 2026-08-23: freshness matters when you ship)
```

**The middle two rows are the ones worth reading, and the earlier three-tree version of this
transcript collapsed them.** A repo that HAS git and simply has no dashboard is `n/a`
SUBJECT-ABSENT — a consumer repo, correctly silent. A directory that is not a repo at all is
`unavailable` — the leg could not measure, and says so instead of inventing a verdict. They are
different answers to different questions and the module spends a `rev-parse` to keep them apart
(`_git_available`); an evidence block that shows only one of them cannot demonstrate that.

`tests/test_generated_artifact_freshness.py` (**27 tests**) pins the same behaviour, half against
injected dates for the boundary arithmetic and half against real throwaway git repos.

### 5.5 Registration — the fenced diff, and what this lane may NOT author

`scripts/audit.py`, `scripts/audit_checks/registry.py` and `ecosystem/doc-code-edge.yaml` are
shared-collision files this batch. Per the contract and the Phase-0 packet §5.3's amended
ownership model, this lane ships its **module** and **tests** as new files and its **registration**
as a diff.

**The lane authors no count pin, and that is correctness rather than politeness.**
`len(ALL_CHECKS)` is pinned by exact equality in **six** places (`tests/test_audit.py` ×2,
`tests/test_doc_code_edge.py` ×2, `tests/test_writer_integrity.py`, and the *generated*
`ecosystem/doc-counts.md`). Their correct value is **N-dependent**: if three lanes each add a
check, each would author `43 → 44` and all three would be wrong. **Preferred position:**
immediately after `check_canonical_freshness` — same family, same question. A preference, not an
assumption: `CHECK_ORDER` is byte-contract-load-bearing and the order is the integrator's call.

```diff
--- a/scripts/audit.py
+++ b/scripts/audit.py
@@ context: just after the canonical_freshness_gate dual-mode import (~:195-198) @@
 try:
     from scripts import canonical_freshness_gate as _cfg
 except ImportError:
     import canonical_freshness_gate as _cfg
 
+# Generated-artifact staleness leg (ADR-86 as amended 2026-08-23; `[#171]` leg 1 / f7). Exactly
+# the relationship this module already has with `_cfg` above: the relation lives in ONE module,
+# and the leg below only wraps its verdict in the Finding envelope. Dual-mode import for the
+# same reason (`python scripts/audit.py` vs `python -m scripts.audit`).
+try:
+    from scripts import generated_artifact_freshness as _gaf
+except ImportError:
+    import generated_artifact_freshness as _gaf
+
```

```diff
--- a/scripts/audit.py
+++ b/scripts/audit.py
@@ context: beside the existing audit-level freshness aliases (~:545-546) @@
 _parse_last_reviewed = _cfg.parse_last_reviewed
 _git_last_commit_date = _cfg.git_last_commit_date
+# Audit-level alias for the same reason the two above exist: it keeps a monkeypatch seam, so a
+# test that rewrites the name on the `audit` module still reaches the leg.
+_gaf_git_last_commit_date = _gaf.git_last_commit_date
```

```diff
--- a/scripts/audit.py
+++ b/scripts/audit.py
@@ context: immediately after check_canonical_freshness's return (~:592) @@
     return [Finding("canonical_freshness", "pass",
                     f"{len(_FRESHNESS_FILES)} canonical living files fresh "
                     f"(last_reviewed not before last edit; within {_FRESHNESS_CADENCE_DAYS}d)")]
 
+
+def check_generated_artifact_freshness(repo_path: Path) -> list[Finding]:
+    """Committed-generated staleness — is a committed generated artifact older than its inputs?
+
+    ADR-86 as AMENDED 2026-08-23 rules that a human or integrator commit satisfies "committed".
+    That makes the dashboard's header honest; it does nothing to keep the output CURRENT. An
+    honest header on a stale trust surface is still a stale trust surface, so this leg is the
+    other half of the same ruling: WARN when the committed artifact has fallen further behind its
+    declared inputs than the baseline measured when the leg was armed (dashboard: 4 days, at
+    `aeec0fd1`, by this leg's own committer-date/first-parent relation). The baseline is a
+    RATCHET, not an allowance — it records that this repo tolerated four days of drift once, and
+    forbids worse.
+
+    WARN-CLASS BY RULING, and the class is load-bearing rather than timid. `cmd_health` (the
+    pre-commit gate) exits 1 only on a `fail`, while `cmd_ship_gate` REDs on any undispositioned
+    `warn` — so the TEETH are at ship time. RED here is a later act with its own ruling, and when
+    it comes it is a one-line change in `generated_artifact_freshness.evaluate`.
+
+    AND THE WORK IS SKIPPED AT COMMIT TIME, not merely the blocking. Status class alone was not
+    enough: `cmd_health` runs the whole of ALL_CHECKS, so a WARN-class check still SPENDS its
+    cost on every commit — measured at 11 `git log` calls for the dashboard (terra, 2026-08-23,
+    against an earlier version that spent 20 by querying each input twice). `_GATE_MODE` is this
+    module's existing answer to exactly that — `check_doc_claims` already runs its expensive leg
+    as `run_expensive=not _GATE_MODE` — so the same guard is used here rather than a new idiom.
+    At commit time the leg is an honest `n/a` NOT-APPLICABLE; at ship time it measures. That is
+    what makes "ship-gate, not pre-commit" true of the WORK and not only of the verdict.
+
+    DISTINCT FROM `gen_dashboard.py --check`, deliberately: the Phase-0 packet is explicit that
+    the two must not be blurred. `--check` asks whether the committed bytes match a regeneration;
+    it is HEAD-pinned, so it drifts on EVERY commit and could carry no meaningful baseline. This
+    asks whether the committed copy is current with respect to its CONTENT inputs. That `--check`
+    is armed nowhere (R3 F5) is a gating gap this leg does not close.
+
+    ONE Finding PER ARTIFACT so the #147 ship-gate dispositions each independently — the same
+    contract `git_backlog_drift` carries, and required by the disposition rule that a matched
+    token suppresses a WHOLE Finding. Logic single-sourced in
+    `scripts/generated_artifact_freshness.py`; this leg only wraps it, passing the audit-level
+    git-date alias so a monkeypatch at the audit level still applies. Read-only; degrades rather
+    than inventing a verdict — an absent artifact is `n/a` SUBJECT-ABSENT (a consumer repo with
+    no dashboard), an unreadable history is `unavailable`.
+
+    THE STATUS MAPPING IS A TABLE LOOKUP, NOT AN `if/else`, and that is deliberate. Written as
+    `if stale: warn / else: pass`, this leg reported every verdict added AFTERWARDS as a silent
+    `pass` — terra hit that twice in one review cycle (2026-08-23). `STATUS_FOR_VERDICT` lives in
+    the module beside the verdicts it maps, so an unknown verdict raises `KeyError` here instead
+    of passing quietly, and a verdict cannot be added without deciding what it reports as.
+    """
+    name = "generated_artifact_freshness"
+    if _GATE_MODE:
+        return [_na(name, "NOT-APPLICABLE",
+                    "ship-gate-only leg — skipped at the audit-health commit gate "
+                    "(ADR-86 amd. 2026-08-23: freshness matters when you ship)")]
+    findings: list[Finding] = []
+    for artifact in _gaf.REGISTRY:
+        m = _gaf.measure(repo_path, artifact, git_date_fn=_gaf_git_last_commit_date)
+        status = _gaf.STATUS_FOR_VERDICT[m.verdict]   # KeyError on an unmapped verdict: loud
+        if status == "unavailable" and m.subject_absent:
+            findings.append(_na(name, "SUBJECT-ABSENT", m.detail))
+            continue
+        evidence = m.detail
+        if status == "warn":
+            evidence = f"{evidence}; regenerate + commit: {artifact.regen_command}"
+        findings.append(Finding(name, status, evidence.replace("|", "/")))
+    return findings
+
```

```diff
--- a/scripts/audit.py
+++ b/scripts/audit.py
@@ context: the ALL_CHECKS literal (~:3407) @@
     check_handoff_bundle_structure,
     check_canonical_freshness,
+    check_generated_artifact_freshness,   # ADR-86 amd. 2026-08-23 / `[#171]` leg 1 — WARN-tier
+                                          # by ruling; RED is a later act with its own ruling
     check_no_sibling_orphans,
```

```diff
--- a/scripts/audit_checks/registry.py
+++ b/scripts/audit_checks/registry.py
@@ context: CHECK_ORDER, beside check_canonical_freshness @@
     "check_canonical_freshness",          # facade — _git_last_commit_date seam
+    "check_generated_artifact_freshness",  # facade — _gaf_git_last_commit_date seam
     "check_no_sibling_orphans",           # facade — _git_registered_worktrees seam
```

```diff
--- a/ecosystem/doc-code-edge.yaml
+++ b/ecosystem/doc-code-edge.yaml
@@ context: the exempt: list, after review_artifact_coverage @@
   - review_artifact_coverage
+  # ADR-86 amd. 2026-08-23 generated-artifact staleness leg. **TEMPORARY**, on the
+  # `review_artifact_coverage` precedent directly above and for the same reason: enforcement
+  # ahead of its written rule runs only under a NAMED, EXPIRING exemption. The rule this leg
+  # embodies — "a committed generated artifact must not fall further behind its inputs than its
+  # measured baseline" — is currently written only in an ADR amendment, which is an immutable
+  # decision record, not a living doc a `# rule:` marker can bind to. When that rule lands in
+  # PLAYBOOK this entry converts to `coverage_scope` and the marker is added. Carried by intake
+  # #42; the row is specified in
+  # docs/audits/2026-08-23-technical-lane-dashboard-commit-path.md §7.4 and NOT filed
+  # (R2 `banked = 0`, no births this batch).
+  - generated_artifact_freshness
```

**The registration's own tests travel with it.** terra's third High (2026-08-23): the module's
tests prove the *relation*, and prove nothing about the audit **envelope** — the status mapping,
the `n/a`-vs-`unavailable` split, the monkeypatch seam, `ALL_CHECKS` membership. Those must be
asserted in `tests/test_audit.py`, which is itself a shared-collision file this batch (it holds
two of the six count pins), so they ship as a diff rather than as an edit.

```diff
--- a/tests/test_audit.py
+++ b/tests/test_audit.py
@@ context: after the canonical_freshness cluster (~:960) @@
+
+# ---------------------------------------------------------------------------
+# generated_artifact_freshness (ADR-86 amd. 2026-08-23; `[#171]` leg 1 / f7)
+# The MODULE's own relation is covered by tests/test_generated_artifact_freshness.py.
+# What is covered HERE is the audit ENVELOPE the module cannot test: status mapping,
+# the n/a-vs-unavailable split, the monkeypatch seam, and ALL_CHECKS membership.
+# ---------------------------------------------------------------------------
+
+def _gaf_dates(mapping):
+    return lambda _rp, pathspec: mapping.get(pathspec)
+
+
+def _gaf_all(outputs_on, inputs_on):
+    """Dates for EVERY declared output and input.
+
+    All of them, not a convenient subset: `measure` returns `unverifiable` if any DECLARED input
+    has no history, so a fixture that names only `BACKLOG.md` tests that rule instead of the one
+    it meant to. `DASHBOARD.inputs` has nine entries and is read from the module so this cannot
+    drift when the input set changes.
+    """
+    from scripts import generated_artifact_freshness as gaf
+    return _gaf_dates({**{p: outputs_on for p in gaf.DASHBOARD.outputs},
+                       **{p: inputs_on for p in gaf.DASHBOARD.inputs}})
+
+
+def _gaf_tree(tmp_path: Path) -> Path:
+    """A tree where the dashboard's output faces EXIST. `measure` checks presence before it asks
+    git — a fixture that skips this gets the `deleted` verdict, not the one it meant to test."""
+    from scripts import generated_artifact_freshness as gaf
+    for rel in gaf.DASHBOARD.outputs:
+        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
+        (tmp_path / rel).write_text("x", encoding="utf-8")
+    return tmp_path
+
+
+def test_generated_artifact_freshness_passes_when_current(
+        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
+    monkeypatch.setattr(aud, "_gaf_git_last_commit_date",
+                        _gaf_all(date(2026, 8, 24), date(2026, 8, 24)))
+    findings = aud.check_generated_artifact_freshness(_gaf_tree(tmp_path))
+    assert len(findings) == 1, "one Finding PER ARTIFACT — the ship-gate dispositions each"
+    assert findings[0].status == "pass", findings[0].evidence
+    assert findings[0].check_name == "generated_artifact_freshness"
+
+
+def test_generated_artifact_freshness_warns_past_the_baseline(
+        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
+    """WARN, never FAIL: cmd_health exits 1 only on `fail`, so this must not tax a commit;
+    cmd_ship_gate REDs on an undispositioned `warn`, which is where the teeth are. The evidence
+    is asserted to name STALENESS specifically — a bare `status == "warn"` would also be
+    satisfied by `unverifiable`, and would then pass even if the date relation regressed."""
+    monkeypatch.setattr(aud, "_gaf_git_last_commit_date",
+                        _gaf_all(date(2026, 8, 1), date(2026, 8, 23)))
+    f = aud.check_generated_artifact_freshness(_gaf_tree(tmp_path))[0]
+    assert f.status == "warn", f.evidence
+    assert "22d stale (baseline 4d)" in f.evidence, f.evidence
+    assert "regenerate + commit" in f.evidence, "a WARN must carry its own discharge"
+
+
+def test_generated_artifact_freshness_deleted_artifact_warns(
+        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
+    """Has git history, gone from the tree -> WARN, never `pass`. An `if stale / else pass` leg
+    made this silently green, which is why the status mapping is a table lookup."""
+    monkeypatch.setattr(aud, "_gaf_git_last_commit_date",
+                        _gaf_all(date(2026, 8, 24), date(2026, 8, 1)))
+    f = aud.check_generated_artifact_freshness(tmp_path)[0]   # tree NOT materialized
+    assert f.status == "warn", f.evidence
+    assert "MISSING from the tree" in f.evidence
+
+
+def test_generated_artifact_freshness_uncommitted_artifact_warns(
+        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
+    """Present in the tree, never committed. `--check` does not catch it (it reports MISSING only
+    for an ABSENT file), and "committed-generated" is the zone class's own claim — so it is a
+    WARN, not a quiet `unavailable` the ship-gate ignores."""
+    monkeypatch.setattr(aud, "_gaf_git_last_commit_date", _gaf_dates({}))
+    f = aud.check_generated_artifact_freshness(_gaf_tree(tmp_path))[0]
+    assert f.status == "warn", f.evidence
+    assert "never committed" in f.evidence
+
+
+def test_generated_artifact_freshness_absent_artifact_is_na_subject_absent(
+        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
+    """A consumer repo with no dashboard is SUBJECT-ABSENT, not a silent pass."""
+    monkeypatch.setattr(aud, "_gaf_git_last_commit_date", _gaf_dates({}))
+    f = aud.check_generated_artifact_freshness(tmp_path)[0]
+    assert f.status == "n/a"
+    assert aud._na_reason(f) == "SUBJECT-ABSENT"
+
+
+def test_generated_artifact_freshness_is_skipped_at_the_commit_gate(
+        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
+    """"Ship-gate, not pre-commit" must be true of the WORK, not only of the verdict class.
+    `cmd_health` runs all of ALL_CHECKS, so without this the leg would spend 11 `git log` calls
+    on every commit. Asserted by making the date fn explode: if it is called under _GATE_MODE,
+    the leg is doing commit-time work it promised not to do."""
+    def _explode(*_a, **_k):
+        raise AssertionError("freshness measured under _GATE_MODE — it must be skipped there")
+
+    monkeypatch.setattr(aud, "_gaf_git_last_commit_date", _explode)
+    monkeypatch.setattr(aud, "_GATE_MODE", True)
+    f = aud.check_generated_artifact_freshness(tmp_path)[0]
+    assert f.status == "n/a"
+    assert aud._na_reason(f) == "NOT-APPLICABLE"
+
+
+def test_generated_artifact_freshness_every_verdict_has_a_mapped_status() -> None:
+    """The leg is a table lookup precisely so an unmapped verdict RAISES rather than passing;
+    this asserts the table covers everything, so that safety net is never actually hit."""
+    from scripts import generated_artifact_freshness as gaf
+    assert set(gaf.WARN_VERDICTS) <= set(gaf.STATUS_FOR_VERDICT)
+    assert set(gaf.STATUS_FOR_VERDICT.values()) <= {"pass", "warn", "unavailable"}
+
+
+def test_generated_artifact_freshness_is_registered() -> None:
+    assert aud.check_generated_artifact_freshness in aud.ALL_CHECKS
+    from scripts.audit_checks.registry import CHECK_ORDER
+    assert "check_generated_artifact_freshness" in CHECK_ORDER
+    assert len(CHECK_ORDER) == len(aud.ALL_CHECKS)
```

That last assertion — `len(CHECK_ORDER) == len(aud.ALL_CHECKS)` — closes a gap `registry.py`'s own
docstring names ("nothing currently asserts that `CHECK_ORDER` still agrees with
`audit.ALL_CHECKS`"), and this batch is precisely the situation it exists for: several lanes
appending to both lists. It is a free-standing improvement and may be dropped without affecting
this leg. **These eight tests add eight to the collected-test count**, which is part of the same
one-shot arithmetic as the count pins.

**Integrator checklist for this diff** (the lane's own, offered rather than assumed):

1. Apply the six hunks above.
2. Count `ALL_CHECKS` **once**, across every sibling lane that added one, and set pins 1–5 to the
   resulting number.
3. Run `python scripts/gen_doc_counts.py --write` for pin 6 — it is generated and must never be
   hand-edited. It also absorbs the eight added `tests/test_audit.py` cases.
4. `python scripts/audit.py checks` should list the new member; `python scripts/audit.py health`
   should show it `pass` on a current tree.

### 5.6 Honest limits — stated, because the leg's value depends on knowing them

1. **Written and tested, not yet armed.** Until the fenced diff is applied, the leg is an ADR-81
   leg-**(d)** *explicit documented deferral*, not a live gate. It is named as such inside the
   ADR-86 amendment itself, so a later audit does not have to rediscover it.
2. **It measures currency, not correctness.** A dashboard regenerated from a broken parser is
   fresh and wrong; this leg would call it fresh.
3. **It cannot see an untracked input.** The telemetry store could change hourly and the relation
   would not move. Stated in §5.1, declared in code.
4. **Day granularity.** Two commits on the same day are indistinguishable — inherited from P5 and
   from git's short-date formats, and deliberately not "improved" into a second idiom. It is why
   the lane-tip measurement below reads `0d` rather than resolving to hours.
5. **No rename following.** `git log -- <path>` is used without `--follow`; if an input path is
   renamed, its pre-rename history stops counting until the declaration is updated. The
   declaration lives in `gen_dashboard.INPUT_RELPATHS`, next to the code that would be renaming it.
6. **It does not close R3 F5.** `gen_dashboard.py --check` is still armed nowhere. Different
   defect, different act — the Phase-0 packet draws that boundary explicitly.


---

## 6. terra review (Step 6)

The contract makes terra **mandatory, pre-merge**, at *"zero Critical / zero High, mutation-checked,
tally written into the artifact body."* This section is that tally. It is written here and not only
in commit messages because `review_artifact_coverage` parses a `**Tally:**` line out of the linked
artifact — an audit organ in this repo already treats a review whose numbers live only in a commit
message as an unparseable one.

**Tally:** 0/0/0/0 — Critical/High/Medium/Low, final pass (round 9, CLEAN)

The slash form is not a style choice: `audit.py::_REVIEW_TALLY_RE` is
`^\*\*Tally:\*\*[ 	]*(\d+)/(\d+)/(\d+)/(\d+)`, and a `Critical=0 High=0` line — which is
the shape terra itself emits — parses as **no tally at all**. `review_artifact_coverage`
already names one linked artifact in this repo that carries an unparseable tally; authoring
from the parser rather than from the reviewer's output format is what keeps this one off
that list.

**That is the FINAL pass, not the loop total.** Nine passes ran; the loop total was 26 findings.
Reporting only the last pass would make a nine-round argument look like a one-round formality, so
both numbers are given.

### 6.1 The loop, pass by pass

`codex exec review -m gpt-5.6-terra` over this lane's diff against merge base `aeec0fd1`. One pass
is not a review: each re-run reads the diff the previous fix produced, and passes 2–8 each raised
something the pass before had graded clean.

| Pass | C | H | M | L | What it caught |
|---|---|---|---|---|---|
| 1 | 0 | 3 | 1 | 0 | input set excluded the generator + its parsers; commit path bounded only the `add`; the fenced audit adapter had no envelope tests |
| 2 | 0 | 1 | 1 | 0 | a **deleted** output measured normally and could report `fresh`; ADR-86's "ADR-80 §3 has zero implementations" was false |
| 3 | 0 | 3 | 1 | 1 | author dates hid a cherry-picked input; fenced envelope mapped `deleted` → `pass`; fenced stale-test created no output files; `gitenv` fallback silently weakened the gate; "read-only, spawns `git log` and nothing else" was false |
| 4 | 0 | 2 | 2 | 0 | unmeasurable declared inputs were silently dropped from the relation; an **uncommitted** output greened the gate; the artifact documented `%as` while the code read `%as %cs`; `--commit-path`'s non-mutation claim was untested |
| 5 | 0 | 6 | 0 | 0 | fenced envelope fixtures supplied 3 of 9 declared inputs (×2 tests); the `unavailable` test contradicted the implementation; `logs/TELEMETRY.db` was an unmeasurable blind spot; **both** artifact strings claimed a currency the code does not provide right after `--write` |
| 6 | 0 | 2 | 1 | 0 | a missing first output face short-circuited to `n/a` while another face was stale; the leg spent 20 `git log` calls on **every pre-commit** |
| 7 | 0 | 1 | 0 | 0 | `git log -1 -- <path>` follows a `--no-ff` merge into the side branch, so an input that landed today measures as weeks old — `fresh` indefinitely, in the exact workflow this repo mandates |
| 8 | 0 | 1 | 0 | 0 | `baseline_days = 3` had been measured by a relation the code no longer performs (§6.2) |
| **9** | **0** | **0** | **0** | **0** | **CLEAN** |

**Round 9's verdict, verbatim, because a clean pass is evidence only if it is quoted rather than
summarised:**

> No real defects found in the scoped diff. The remaining limitations — untracked telemetry input,
> day-level measurement, rename history, and the intentionally unarmed `--check` gate — are
> explicitly documented accepted design limits rather than contradictions with the implemented
> freshness relation.

That is the stopping condition, and it is the right one: the four things it names are §5.6's honest
limits 3, 4, 5 and 6 — the reviewer independently re-derived this lane's own list of accepted
limits and agreed they are limits rather than defects. Each pass from 8 onward carried an explicit
*"classify as (a) a real defect I will fix, or (b) a design tension I will record"* instruction, so
"nothing found" is a classification the reviewer made, not a silence it fell into.

**Honest limit on the tally itself.** Passes 1–7 ran in an earlier session and their per-finding
dispositions were not recorded at the time — the per-round severities above are read back from
those runs' own `TALLY:` lines, which survive in the `codex` rollout logs, and the fixes that
actually landed are enumerated in `83023bbc`'s commit message. Passes 1–7 were **not** re-adjudicated
in this session; what was verified here is that the current tree passes round 9 clean. A loop that
records only its final pass is what made this note necessary, and it is why the table exists.

### 6.2 The one finding this session had to fix, and how it was proved

Round 8, classified by terra as *"(a) real defect"*:

> At `aeec0fd1`, this module's own `--first-parent` query reports `docs/audits` (a declared input)
> last touched on 2026-08-24, while both dashboard outputs were last touched on 2026-08-20, so the
> measured relation is 4 days, not 3.

It is the lane's own subject reproduced inside the lane's own code. `baseline_days = 3` was a
genuine measurement — of a relation that had since been replaced twice underneath it (round 3
swapped author date for committer date; round 7 added `--first-parent`; round 1 added the CODE half
of the input set). `docs/audits` reads `2026-08-23` by author date and `2026-08-24` by committer
date. The constant outlived its measurement, and a "measured baseline" that no longer describes any
measurement the code performs is exactly a true-sounding claim about a mechanism that moved.

**Mutation-checked, both directions**, because a pinned constant is only pinned if its test fails
when it is wrong:

```
baseline_days=4  ->  27 passed
baseline_days=3  ->  FAILED test_dashboard_baseline_is_the_measured_value - assert 3 == 4
baseline_days=5  ->  FAILED test_dashboard_baseline_is_the_measured_value - assert 5 == 4
```

Corrected at every site that carried it: the module docstring, `DASHBOARD.baseline_days`, the
pinning test, §1.4's ground-truth table, §5.3's derivation block, §5.4's re-run evidence, the §5.5
fenced audit docstring, the §5.5 fenced envelope-test assertion, the ADR-86 amendment, and intake
#42. Ten sites for one number is itself the argument for the CLAUDE.md §4 rule about restating
computed values in prose.

**The fenced diffs were executed, not just re-read.** Terra found the fenced envelope tests broken
twice (rounds 3 and 5), which is a failure mode a lane cannot see by inspection because the code
does not run from inside a markdown fence. So the `tests/test_audit.py` hunk was **extracted from
this artifact programmatically** and run against a shim of the fenced adapter: **7 passed,
1 skipped.** The skip is `test_generated_artifact_freshness_is_registered`, which asserts
`ALL_CHECKS` / `CHECK_ORDER` membership and can only become true once the integrator applies the
registration hunks — it is skipped rather than faked green, and that is the one assertion in the
diff this lane genuinely cannot prove from here.

### 6.3 The declared bypass, and why the standing remedy was withheld

Both commits in this session carry `SKIP=audit-health` — one hook, declared, never `--no-verify`
(which would drop the whole mesh including `validate-hermetization` and the commit-msg gates).
Stated here and not only in the commit messages, because an undeclared bypass is what the doctrine
actually refuses.

`audit.py health` has exactly **one** `[!!]` FAIL on this tree: `journal_spine_anchor`, naming 13
first-parent spine entries above the disposition floor `24882f8cc`. **All 13 are foreign**, proved
on two independent legs rather than asserted:

- `git merge-base --is-ancestor <sha> HEAD` returns **false for all 13** — not one is reachable
  from this branch.
- `journal_anchor.unanchored_on_spine` run against **main's own `JOURNAL.md`** returns **zero**.

So this is lane tree-lag, not a real gap: the check walks `main`'s spine from the shared ref store
(a worktree sees main's newest commits instantly) but reads `JOURNAL.md` from the local working
tree, which predates the integrator's entry. Main is already anchored; this worktree just cannot
see it. The batch merged to `main` after this lane was cut.

**The standing remedy is a sync-merge of `main` into the lane, and it is deliberately not used
here.** It was withheld under an explicit operator instruction for this lane — *do not rebase, do
not merge main in; commit, seal, stop; the integrator resolves the drift.* Recorded as a
**deviation from the standing remedy**, not as a discovery: the remedy would have cleared the FAIL
without a bypass, and the reason it was not taken is an instruction, not a technical obstacle. The
integrator inherits a lane whose merge base is `aeec0fd1` and which has never seen the batch.

A lane also **does not write `JOURNAL.md`** — `/lane-integrate` writes the anchor once, from the
primary, after every lane has stopped. Writing one here would contend with every sibling lane for
one file and would itself become the next unanchored commit. So the contract's "JOURNAL.md entry on
this branch" item is **declined with its reason**, not silently skipped.

### 6.4 What this review could not check

1. **It reviewed a diff, not a merge.** Every finding above was raised against
   `aeec0fd1...HEAD`. `main` has moved since — the batch landed — and this lane has deliberately
   not merged it (§6.3). Nothing here says the lane is conflict-free against current `main`; that
   is the integrator's act.
2. **The registration is still unapplied.** §5.6 limit 1 stands: until the fenced diffs land, the
   leg is an ADR-81 (d) documented deferral, not a live gate. Terra reviewed the diff's *content*
   and the extracted tests' *behaviour*; neither proves the hunks apply cleanly against a tree that
   several sibling lanes have also edited.
3. **No count pin was authored, so no count pin was reviewed.** `len(ALL_CHECKS)` is pinned in six
   places and its correct value is N-dependent across the batch (§5.5). The integrator's checklist
   in §5.5 is the surface that closes this; a reviewer looking only at this lane cannot.

---

## 7. The BACKLOG row this lane did **not** file

Two committed surfaces promise this section by name, and until now both pointed at nothing:

- `docs/intake/2026-08-23-tech-generated-artifact-currency.md` (intake **#42**), Status block —
  *"The BACKLOG row this work would need is specified in
  `docs/audits/2026-08-23-technical-lane-dashboard-commit-path.md` §7."*
- the `ecosystem/doc-code-edge.yaml` hunk of the §5.5 fenced diff, inside the comment that
  justifies the exemption — *"the row is specified in
  `docs/audits/2026-08-23-technical-lane-dashboard-commit-path.md` §7.4 and NOT filed."*

Both were **claims without evidence**: neither section existed. That is precisely the defect class
this lane was dispatched to fix — a true-sounding sentence about something that is not there — and
it had reproduced itself in the lane's own paperwork. It is fixed the way the rest of the lane
fixed it: by making the claim true, not by softening the wording.

### 7.1 Why the row is specified here rather than filed

Ruling **R2** sets `banked = 0` for the 2026-08-23 batch: **no task rows are born**. The frozen
contract restates it — *"File no task row. Ruling R2: `banked = 0`, so no births this batch. Write
the row specification into your artifact and file an intake if the work needs a carrier."*

The lane did both halves and neither more. It filed the **intake** (#42, DRAFT) as the carrier, and
it writes the **specification** at §7.4. Nothing under `tasks/` was created, `BACKLOG.md` was not
regenerated, and **no `[#id]` was consumed** — which is also why §7.4 does not pin one (note 1
there).

### 7.2 The debt the row exists to discharge

The §5.5 fenced diff adds `generated_artifact_freshness` to `ecosystem/doc-code-edge.yaml`'s
**`exempt:`** list. That is a real cost, and the file states it in its own header: `exempt:` is for
`ALL_CHECKS` members that owe **no** `# rule:` annotation because they are structural, presence, or
self-referential checks *"with no behavioral doc→code rule"*.

This leg is not one of those. It embodies a behavioural rule —

> a committed generated artifact must not fall further behind its declared inputs than its
> measured baseline

— and a rule that exists cannot honestly be filed under *there is no rule here*. The exemption is
therefore **TEMPORARY**, in the exact shape of the `review_artifact_coverage` entry immediately
above it in the same file, which the diff names as its precedent. That entry states the general
principle: enforcement ahead of its written rule runs only under a **named, expiring** exemption
(ADR-81 (d)), *"bound to a row rather than to memory"*. `[#499]` is that row for
`review_artifact_coverage`, and it carries the expiry as an explicit rider — *"this row owns the
exemption's expiry so it cannot outlive its reason."*

§7.4 is the same instrument for this leg. Without it, the word **TEMPORARY** in a YAML comment is
the only thing standing between this exemption and permanence — and a comment is not a mechanism.
That is the whole argument of this lane, applied to its own paperwork.

### 7.3 What the row must **not** be, and what it must decide first

Four constraints, because a row filed without them would be filed wrong.

1. **It is not a promotion to RED.** R1 armed this leg as a **WARN against a measured baseline**,
   and said RED *"is a later act with its own ruling."* The row below discharges a **coverage**
   debt and nothing else. It must not smuggle in a severity change; that needs its own ruling, and
   this lane has none to cite.
2. **It cannot be sized until intake #42's open questions are answered.** #42 asks three, and two
   of them move the row's scope by more than a size band: *is HEAD-pinning itself the defect* — if
   the dashboard stopped rendering HEAD's sha into its own text, `--check` would become usable as a
   gate and this leg could be **deleted** rather than promoted — and *should the registry cover
   artifacts that already have a `--check` gate*. A row written before those are answered pins a
   scope the architect has not chosen. §7.4 therefore states the **fixed** part (the coverage debt,
   owed whatever the answers are) and names the variable part as a deferral peg rather than
   guessing it.
3. **The rule's home is not a free choice.** #42's third open question — PLAYBOOK, ARCHITECTURE
   Ch2, or an ADR — is constrained by the mechanism: `doc_code_edge` resolves `<!-- rule: ID -->`
   markers **only** in the three files under `declaration_docs:` (`protocols/PLAYBOOK.md`,
   `protocols/DEFINITION_OF_DONE.md`, `protocols/HANDOFF_PROCESS.md`). An ADR home would leave the
   edge unresolvable and the exemption permanent **by construction** — which is the position
   `routine_consumers` is already stuck in, per its own comment in the same file. §7.4 says
   PLAYBOOK for that mechanical reason, and flags that choosing otherwise means also amending
   `declaration_docs:`, which is a separate ruling and not a side effect.
4. **It is a two-site edge, and saying so is load-bearing.** The strict resolver returns
   `ambiguous` for more than one code site, so a rule enforced in two organs that is *not* declared
   in `multi_site:` can never resolve — it would freeze `test_coverage_all_in_scope_rules_resolve`
   below 100% permanently. This leg is `audit.py::check_generated_artifact_freshness` (adapter) +
   `scripts/generated_artifact_freshness.py` (logic), which is exactly the shape already declared
   for `coherence-doc-claims`, `coherence-doc-rot` and `coherence-doc-structure`. The row states
   the count so a filer cannot discover it at the gate.

**Related drift this lane surfaced and did not touch.**
`tasks/171-build-the-conformance-dashboard-at-ecosystem-con.md` still reads *"a read-only validator
generates it and commits its own output (ADR-80 committed-generated-zone writer policy)"*, with
`Done when: … generated + committed by a read-only validator`. **R1 withdrew exactly that clause.**
The row's own text now describes the option the architect declined, and its `Done when` names a
mechanism this lane has established does not and will not exist. A lane does not edit `tasks/` this
batch (§7.1), and `[#171]` is not this lane's row to rewrite — **reported, not filed**, for the
integrator's ruling batch.

### 7.4 The row specification

Ready to file verbatim as `tasks/<id>-<slug>.md` once R2's `banked = 0` lifts. Frontmatter first,
then the `BACKLOG.md` line `gen_task_tree.py` emits from it.

```yaml
---
id: "[#<next>]"
title: "Write the generated-artifact currency rule and expire its doc→code exemption"
status: deferred
priority: P3
size: M
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
depends-on: "#171"
generates: BACKLOG.md
---
```

```text
- [#<next>] [P3][M] **Write the generated-artifact currency rule and expire its doc→code exemption** — the ADR-86 amd. 2026-08-23 staleness leg (`audit.check_generated_artifact_freshness` + `scripts/generated_artifact_freshness.py`) shipped under a **TEMPORARY** `ecosystem/doc-code-edge.yaml` `exempt:` entry, on the `review_artifact_coverage` / `[#499]` precedent: enforcement ahead of its written rule runs only under a named, expiring exemption (ADR-81 (d)). This row owns that expiry so it cannot outlive its reason. The rule is *"a committed generated artifact must not fall further behind its declared inputs than its measured baseline"*; it currently exists only inside an ADR amendment, which is an immutable decision record, not a living doc a `# rule:` marker can bind to. · Done when: the rule is written in `protocols/PLAYBOOK.md` carrying `<!-- rule: coherence-generated-artifact-currency -->`, **AND** `scripts/audit.py::check_generated_artifact_freshness` and `scripts/generated_artifact_freshness.py` each carry the matching `# rule:` marker with `multi_site: coherence-generated-artifact-currency: 2` declared (adapter + logic — the `coherence-doc-claims` / `coherence-doc-rot` / `coherence-doc-structure` shape, not a 1:1 edge), **AND** `generated_artifact_freshness` moves from `exempt:` to `coverage_scope:`, **AND** `tests/test_doc_code_edge.py::test_coverage_all_in_scope_rules_resolve` resolves it, **AND** `python scripts/audit.py health` still reports the leg `pass` on a current tree · refs docs/decisions/ADR-86-conformance-dashboard-location.md (amd. 2026-08-23), docs/audits/2026-08-23-technical-lane-dashboard-commit-path.md §5.5 + §7, docs/intake/2026-08-23-tech-generated-artifact-currency.md (#42), ecosystem/doc-code-edge.yaml, scripts/generated_artifact_freshness.py, #499, #171 · kill-candidates: none — no open row owns generated-artifact currency; the nearest neighbour `[#169]` scopes the four ADR-85-**ungated living docs**, not generated artifacts, and would be wrong to close for this · DEFER — peg: intake #42's three open questions answered (HEAD-pinning, registry breadth, rule home)
```

**Six notes on the fields, because each one was a decision rather than a default:**

1. **`id` is deliberately unpinned.** The next-free id is `max(bracketed id across history) + 1` —
   computed, not remembered, and invalidated by any sibling lane's filing. Pinning it here would
   restate a count in prose, which is the CLAUDE.md §4 rule this repo learned the hard way, and it
   would be stale before the row was ever filed. Resolve it at filing time.
2. **`status: deferred` with a named peg, not `open`.** Per §7.3 item 2 the scope is not knowable
   until #42 is answered, and this repo's own convention (`[#169]`, `[#499]`) is that an
   unanswerable row **defers against a named peg** rather than sitting open and rotting.
3. **`size: M`, matching `[#499]`** — the same act (write the PLAYBOOK rule, annotate both organs,
   flip the exemption, prove the edge resolves) at the same shape. **Honest limit:** if #42's
   HEAD-pinning question resolves toward *drop the HEAD stamp*, this leg may be **deleted** instead
   of promoted and M is then an overestimate. That is an argument for the deferral, not for sizing
   it smaller now.
4. **`story: [S5]`, not `[S3]`.** `[S3]` is *"turn advisory guards into enforced gates"*, which this
   row explicitly is **not** — §7.3 item 1, the leg stays WARN. `[S5]` is *"catch spec/dependent
   drift mechanically, not by memory"*, which is the rule almost verbatim, and it is where `[#171]`
   and `[#169]` already sit.
5. **`depends-on: #171`.** The leg does not exist in the tree until the §5.5 fenced diff is applied,
   and that application is `[#171]` leg 1's merge. Filing this row before that merge would create a
   dependency on code that is not there.
6. **`kill-candidates: none — <reason>`, and the reason is the point.** The
   `backlog-filing-backpressure` commit-msg gate **BLOCKS** a commit that adds a task id without
   that line, and `preflight_backlog_ids` checks that any row it names is actually open. `[#169]`
   is the row a hurried filer would reach for; the specification says why it is the wrong one
   instead of leaving that to be discovered at the gate.

---

## 8. Suite state at hand-back

Run unpiped, whole suite, at branch tip: **`6 failed, 3601 passed, 9 skipped, 1 xfailed in
1657.54s`**. Not "green" — the contract forbids reporting that, and it would be false.

Six is not two, so every failure is dispositioned below, and **the disposition is a measurement,
not a judgement.** A detached worktree was created at the merge base `aeec0fd1` — a tree containing
**none** of this lane's files (`scripts/generated_artifact_freshness.py` and
`tests/test_generated_artifact_freshness.py` are absent there; `git worktree add --detach` shares
the ref store but not the content) — and the four non-baseline failures were re-run inside it.
Result: **3 failed, 1 passed in 433.62s**. The worktree was then removed and its removal verified
(`git worktree remove --force` + `prune`; `git worktree list` shows three entries, none of them the
probe) — §5 rule 9, no leftovers.

| Test | Verdict | Proof |
|---|---|---|
| `test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent` | **inherited** | Named in the contract's own baseline as pre-existing and rooted in its `tmp_path` fixture |
| `test_stale_worktrees.py::test_linked_worktrees_reader_excludes_the_primary` | **environmental** | It asserts `aud._REPO_ROOT` is not among the linked worktrees; inside a worktree it *is* one. Structural to running the suite from a lane |
| `test_audit.py::test_health_ok_with_registered_repo` | **foreign** | FAILS at `aeec0fd1` with none of this lane's content present |
| `test_audit.py::test_health_stays_ok_with_na_status` | **foreign** | FAILS at `aeec0fd1` with none of this lane's content present |
| `test_silent_rule_ratchet.py::test_check_registered_and_green_on_live_repo` | **foreign** | FAILS at `aeec0fd1`; and independently, the detector's scan scope is `protocols/*.md`, `templates/**`, `ecosystem/*.yaml`, and this lane's diff touches **none** of those |
| `test_export_backlog_view.py::test_no_gate_hook_or_script_reads_the_export` | **THIS LANE'S** | **PASSES** at `aeec0fd1`; fails at tip |

**The three "foreign" rows are one cause with three names, and none of the names says so.** All
three assert `audit.py health` / the ratchet green **on the live repo**, so they read main's moved
spine through the shared ref store — the same `journal_spine_anchor` lane-lag proved on two legs in
§6.3, plus a detector-migration WARN (`silent-rule-v5` baseline vs a `silent-rule-v4` detector) that
is likewise nothing this lane can move. The widely-quoted worktree baseline is **2**; under a
foreign spine gap the honest baseline is **5**, and a lane that quotes 2 will read three inherited
failures as its own regressions.

### 8.1 The one failure that is this lane's

```
tests/test_export_backlog_view.py:521: in test_no_gate_hook_or_script_reads_the_export
    assert not offenders, "the export is read by governance: " + "; ".join(offenders)
E   AssertionError: the export is read by governance:
E     ecosystem/conformance.html references 'export_backlog_view';
E     ecosystem/conformance.md references 'export_backlog_view'
```

**Mechanism, measured rather than guessed.** At `aeec0fd1` both dashboard faces contain **0**
occurrences of `export_backlog_view`; at tip they contain **1** each. The dashboard's committed copy
was generated on **2026-08-20** over the window `2026-08-13 → 2026-08-20`. This lane had to
regenerate it — Step 3 corrects a string that lives in the rendered output — and the regenerated
copy is *"As of 2026-08-24, window 2026-08-17 → 2026-08-24"*. `[#563]` (the `Backlog.md`
read-only-view-layer row) left `BACKLOG.md` inside that newer window, so Section 0 now quotes its
row text, and that row text names `scripts/export_backlog_view.py`.

**It is a false positive, and the test already knows the distinction it is missing.** Its own
comment excludes `docs/` with the reason *"an audit artifact NAMES the export, which is not reading
it."* `ecosystem/conformance.md` is a **generated report that quotes BACKLOG prose verbatim** — it
names the export in exactly the sense the `docs/` carve-out was written for, and it reads nothing.
But `ecosystem` is in `_ENFORCEMENT_ROOTS`, so the carve-out does not reach it.

**It is this lane's by trigger, and latent by nature.** The trigger is this regeneration; the
condition is *any* regeneration while `[#563]` sits in the 7-day window. The next person to run
`python scripts/gen_dashboard.py --write` reds the same test, with no involvement from this lane —
which makes it a defect in the sweep's scope, not in the dashboard.

**Not fixed here, deliberately.** `tests/test_export_backlog_view.py` belongs to `[#563]`'s
exporter, not to this lane, and the correct shape of the carve-out is that organ's call: extend the
`docs/`-style exclusion to generated artifacts, add `ecosystem/conformance.*` to `_SKIPPED_DIRS`,
or strip quoted BACKLOG prose before matching. The minimal change that would clear it —

```python
# tests/test_export_backlog_view.py, beside the existing docs/ carve-out
_SKIPPED_FILES = {"ecosystem/conformance.md", "ecosystem/conformance.html"}
# generated REPORTS that quote BACKLOG row prose verbatim: same reason docs/ is
# excluded — an artifact that NAMES the export is not one that reads it.
```

— is offered rather than applied, and is **reported, not filed** (R2 `banked = 0`; §7.1). Flagged
for the integrator because it will red their post-merge suite run too.

### 8.2 Hand-back

- **Branch:** `worktree-dashboard-commit-path`, merge base `aeec0fd1`, never merged, never pushed.
- **`main` has moved** — the 2026-08-23 batch landed — and this lane has deliberately **not**
  synced (§6.3). The drift is the integrator's to resolve.
- **The registration is a fenced diff** (§5.5) with its own integrator checklist; the six
  `len(ALL_CHECKS)` count pins are N-dependent across the batch and are **not** authored here.
- **`ecosystem/doc-counts.md`** carries an in-lane edit that will be superseded at integration: it
  is generated and N-dependent, and is regenerated once, at the end, by `gen_doc_counts.py --write`.
- The branch tip sha is reported in the hand-back rather than written here — a commit cannot name
  its own hash, which is the same rule that makes a merge unable to anchor itself.
