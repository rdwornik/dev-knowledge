# Backlog testability census — every open Done-when graded, conversions drafted

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-10 · **Slug:** backlog-testability-census
- **Seat:** CC (Opus 5), lane E, worktree `backlog-testability-census`, branch `worktree-backlog-testability-census`
- **Purpose:** grade the mechanical testability of every open row's Done-when, and draft the
  conversions, so the "132 untestable rows" number becomes workable instead of famous.
- **Posture:** read-only. **Zero task-file edits, zero births, zero status changes, zero
  deletions.** Deletion candidates are FLAGGED for the operator (§5); this lane executes
  nothing and proposes no removal of its own authority.

## Run conditions — stated, not assumed

- Local worktree on the operator's machine, so the off-repo predicates N-A could not test from
  a cloud clone (`~/.claude/*`, sibling repos) **are** resolvable here, and five of them were
  resolved (§3, §4).
- **No test was executed.** Nothing in this lane changes code, so the suite has no bearing on
  the result; test *existence* is never reported here as test *passing*.
- The commit runs the live pre-commit gate set (`audit-health` among them). Nothing was skipped
  and no `--no-verify` was used.
- Filename verified against both parsers that consume `docs/audits/` **before** writing:
  `validate_hermetization.classify()` returns `None` (clean) for this path, and
  `gen_audit_index.py` parses the `YYYY-MM-DD-` prefix and the `# ` title above.
  `gen_audit_index.py --write` was run so the generated index carries this file.

## Method

Source of truth is `tasks/*.md` **frontmatter read directly** — never the generated
`BACKLOG.md`, never memory of a row. 254 files carry frontmatter; **170 are `status: open`**,
the figure N-A reported this morning, independently reproduced. All 170 Done-when clauses
parsed; all 170 are graded. There is no untested remainder in this census — the coverage limit
that bounded N-A does not apply here, because grading a clause is cheaper than testing it.

Referent liveness was screened mechanically (every path-shaped token in every row body resolved
against the tree, against sibling repos, and against `~/.claude`), then **every DEFECTIVE verdict
in §3 was hand-verified against live state** — no defect below rests on the screen alone.

### The rubric, and where its line falls

The four classes are the contract's. The line that actually decides most rows is this one, so
it is stated plainly:

- **MECHANICAL** — **every** leg of the Done-when is verdictable by a check, test, or command
  against repo (or declared-consumer) state, *as written*. One unverdictable leg disqualifies
  the row: a Done-when is a conjunction, and a finish line you cannot verdict in full is not a
  finish line.
- **PROSE-CONVERTIBLE** — at least one leg is not verdictable as written, **and** a rewrite
  exists that tests the *same substance* mechanically.
- **PROSE-JUDGMENT** — the substance **is** a human adjudication. The only mechanization
  available is a **hollow existence check** ("some document exists"), which verifies that
  somebody wrote something, not that the row's question was answered. Legitimate, and named.
- **DEFECTIVE** — a referent the clause depends on is dead, has drifted, or the clause is
  unmeetable as written. Where intent is recoverable this report says what the referent moved
  to; where it is not, the verdict stays DEFECTIVE rather than becoming a guess.

**The PROSE-JUDGMENT/CONVERTIBLE boundary is the load-bearing judgment in this census, and it
is contestable.** Nearly any ruling-shaped row can be made "mechanical" by checking that a
ruling *document* exists. That conversion is available for all 15 PROSE-JUDGMENT rows and is
deliberately not drafted for them: it would move the number without moving the testability, and
a §B amendment satisfied that way would be satisfied by ceremony. Whether the hollow wrapper is
acceptable is the operator's call — it is question Q1 in §8.

**`(off-repo)`** is a sub-tag, not a class: the predicate resolves against a consumer repo or
`~/.claude`. Following N-A, this is recorded as a **runtime** limit, not a phrasing defect.

---

## 1. Statistics

### Counts by class

| Class | Count | Share of 170 |
|---|---|---|
| MECHANICAL | 75 | 44.1% |
| PROSE-CONVERTIBLE | 72 | 42.4% |
| PROSE-JUDGMENT | 15 | 8.8% |
| DEFECTIVE | 8 | 4.7% |

By priority band:

| Class | P1 | P2 | P3 |
|---|---|---|---|
| MECHANICAL | 3 | 35 | 37 |
| PROSE-CONVERTIBLE | 0 | 42 | 30 |
| PROSE-JUDGMENT | 0 | 4 | 11 |
| DEFECTIVE | 2 | 2 | 4 |

Open set by priority: **P1 5 · P2 83 · P3 82**. Off-repo predicate: **21 rows**.

### Delta vs the 132 baseline — the baseline measures the wrong thing

N-A's "**Prose predicate — 132 rows**" was measured as *the Done-when cites no path at all*.
That measure is reproducible and it reproduces: applying it to today's 170 rows gives **130**,
against N-A's 132 this morning. Same population, same instrument, a 2-row parse-boundary
delta. **The 132 number is sound as a measurement.**

It is unsound as a *testability* claim, and this is the census's principal finding:

> **Of the 130 rows whose Done-when cites no path, 55 are MECHANICAL anyway.**

Path-citation is a bad proxy for testability. `[#242]`'s Done-when — *"a seeded ADR with a
header↔README status divergence is flagged by an audit check, with tests"* — cites no path and
is completely mechanical: it names a seed, a behaviour, and a test. Conversely `[#369]` cites a
path and is DEFECTIVE, because the count beside the path has drifted.

So the claim N-A drew from it — *"78% of the open set cannot be mechanically tested"* —
**overstates the untestable stock by about 42%**. The honest figures:

| Measure | Value | Share |
|---|---|---|
| N-A's baseline (Done-when cites no path) | 130 | 76.5% |
| Not mechanically testable as written (C + J + D) | **95** | **55.9%** |
| Not testable and not convertible either (J + D) | **23** | **13.5%** |
| Genuinely human-adjudicated, no defect (J) | **15** | **8.8%** |

The two measures are **comparable in population and instrument** (both over the same 170 open
rows, both read from `tasks/` frontmatter) and **not comparable in what they assert**: one counts
a syntactic feature of the clause, the other grades whether the clause can be verdicted.

### `footprint:` coverage

`footprint:` is **not** a frontmatter key — it is an inline body segment (`· footprint: …`).
Coverage among open rows is **5 of 170** (`[#502] [#505] [#506] [#507] [#508]`), which
reproduces the 5/169 baseline exactly against a denominator one row larger. All five are from
the 501+ block, so this is a convention that began with the newest rows and has not been
back-filled. For contrast, the sibling inline convention `kill-candidates:` has reached **117 of
170** — the difference is that `kill-candidates:` is enforced by a commit-msg hook
(`backlog-filing-backpressure`) at add-time and `footprint:` is enforced by nothing.

### One defect reproduced live

`[#470]` is not a hypothesis. Running `python scripts/audit.py checks` in this lane crashed at
check #22 with `UnicodeEncodeError: 'charmap' codec can't encode character '→' in position
30` — the exact defect the row describes, reproduced on the operator's own console today. The
row is MECHANICAL and its Done-when is currently unmet.

---

## 2. The grading table — all 170 open rows

Class · `footprint:` declared Y/N · serialize-group, one line each. **Read from the task file,
never from `BACKLOG.md`.**

| id | P/size | Done-when class | fp | serialize-group | basis |
|---|---|---|---|---|---|
| [#23] | P3/S | MECHANICAL | N | (none) | seeded ADR with a bad relation-field is flagged, with tests |
| [#43] | P3/L | PROSE-JUDGMENT | N | (none) | a decision + a conditional scaffold |
| [#71] | P3/S | MECHANICAL (off-repo) | N | environment | tree matches ls ~/.claude/{commands,skills} + the named lines reconciled |
| [#82] | P3/M | PROSE-CONVERTIBLE | N | (none) | 'each repo's profile is recorded' needs the per-repo home named |
| [#99] | P3/S | MECHANICAL | N | (none) | a red repo's digest line carries the failing check name(s) |
| [#112] | P2/M | PROSE-CONVERTIBLE | N | claude-md | legs 1-2 testable; leg 3 'CLAUDE.md SS5 is de-contradicted' has no predicate |
| [#116] | P3/S | MECHANICAL (off-repo) | N | settings-json | exec-form args:[] + an if: filter are both greppable in settings.json |
| [#122] | P3/S | PROSE-JUDGMENT | N | (none) | operator approval IS the substance; removal is downstream of it |
| [#123] | P2/S | PROSE-CONVERTIBLE | N | (none) | 'adopted by the fleet/routine jobs' + 'a value review records' need named homes |
| [#126] | P2/M | PROSE-JUDGMENT | N | (none) | a recorded go/no-go on a doctrine question |
| [#127] | P3/S | MECHANICAL | N | (none) | seeded failure -> named block; success stays 3-line |
| [#130] | P3/S | PROSE-CONVERTIBLE | N | (none) | digest artifact unnamed; 'a scrub step exists' has no locus |
| [#132] | P2/M | PROSE-CONVERTIBLE | N | pre-commit-config | 'covering all organ classes' has no denominator; the file+hook legs are mechanical |
| [#145] | P3/M | PROSE-CONVERTIBLE | N | (none) | 'each is filed or closed' is mechanical once the pass emits ids |
| [#146] | P3/S | PROSE-CONVERTIBLE | N | playbook | 'is doctrine' + 'a sweep is run' need a home and a candidate list |
| [#153] | P2/M | PROSE-JUDGMENT | N | audit-py | 'the boundary is defined' + 'the question is decided' are the deliverable |
| [#162] | P2/M | PROSE-CONVERTIBLE | N | handoff | 'all enumerated surfaces' -> the 4 refs; then a grep verdicts it |
| [#170] | P3/M | DEFECTIVE | N | (none) | DEAD REFERENT: no tasks/168-*.md exists in any status; you cannot add depends-on to it |
| [#171] | P3/M | MECHANICAL | N | (none) | file generated+committed, generator read-only, ARCHITECTURE pointer |
| [#185] | P2/M | MECHANICAL | N | (none) | seeded pattern -> injection, with tests |
| [#189] | P3/S | MECHANICAL (off-repo) | N | (none) | a session-end check surfacing ~/.claude drift is seedable |
| [#210] | P3/S | PROSE-CONVERTIBLE | N | audit-py | 'the shape is decided' is covered by (a)-or-(b) + the 3 dispositions retiring |
| [#220] | P2/M | PROSE-CONVERTIBLE | N | coherence | a fixture + a recorded organ-fired list makes the spike verdictable |
| [#227] | P3/S | MECHANICAL | N | (none) | path move + inbound refs resolve |
| [#234] | P3/S | MECHANICAL | N | audit-py | present-probe PASSes / absent-probe FAILs, with tests |
| [#239] | P3/M | PROSE-CONVERTIBLE | N | (none) | 'those methodology elements' needs pinning to an enumerated set |
| [#241] | P2/S | DEFECTIVE | N | coherence | DRIFTED CARDINALITY: 'each of the 6' vs 20 live warn-undeclared ids today |
| [#242] | P2/M | MECHANICAL | N | audit-py | seeded status divergence is flagged, with tests |
| [#244] | P2/L | MECHANICAL (off-repo) | N | (none) | REMOVED+ABSENT+roster+fleet_health are each observable |
| [#245] | P2/M | MECHANICAL | N | (none) | two behaviours, with tests |
| [#263] | P3/S | PROSE-CONVERTIBLE | N | (none) | 'the stale entries' unenumerated; removal itself is mechanical |
| [#266] | P3/S | PROSE-CONVERTIBLE | N | (none) | 'the grant-language guidance' names no file |
| [#267] | P2/S | MECHANICAL (off-repo) | N | (none) | FIRED measurement + engages: scope condition |
| [#269] | P3/S | MECHANICAL | N | (none) | shape + header pointer are both greppable |
| [#270] | P1/M | MECHANICAL | N | (none) | [load] line renders, CSV appends, metric recorded in the closing commit |
| [#271] | P3/L | PROSE-CONVERTIBLE | N | (none) | 'ALL SS6 constraints' lives in an archived intake; enumerate to convert |
| [#273] | P3/S | MECHANICAL | N | settings-json | escalation line with a test + thresholds recorded |
| [#274] | P3/S | PROSE-CONVERTIBLE | N | (none) | 'demonstrably applies it' is the unverdictable leg |
| [#276] | P2/M | MECHANICAL | N | (none) | SKIP + no-re-append, with tests |
| [#277] | P2/M | PROSE-CONVERTIBLE | N | audit-py | 'a representative run' undefined; 49:0 baseline log is gitignored/ephemeral |
| [#278] | P2/M | PROSE-CONVERTIBLE | N | (none) | 'both UAT ACs' live in an archived intake; enumerate to convert |
| [#281] | P2/S | PROSE-JUDGMENT | N | (none) | a re-peg decision |
| [#285] | P3/S | PROSE-CONVERTIBLE | N | audit-py | 'genuinely re-read' is unverifiable; the stamp + _FRESHNESS_FILES legs are not |
| [#288] | P3/S | MECHANICAL | N | (none) | detected+flagged, ledger line, with a test |
| [#289] | P2/M | MECHANICAL | N | settings-json | versioned source + policy doc + manifest entry + Informant coverage |
| [#293] | P3/S | MECHANICAL (off-repo) | N | (none) | per-repo runbook presence, n>=1 recorded |
| [#296] | P3/S | MECHANICAL | N | audit-py | path agreement, with a test |
| [#297] | P3/S | MECHANICAL | N | audit-py | dry mode reports armed/fired with no spawn, with a test |
| [#298] | P3/S | MECHANICAL | N | (none) | (a)(b)(c) each with a test |
| [#303] | P2/S | MECHANICAL | N | architecture | skips-or-redirects with a test + encoded child class |
| [#317] | P2/M | MECHANICAL | N | (none) | parallel-by-default + a timed <60s run + serial-nightly preserved |
| [#323] | P3/S | PROSE-JUDGMENT | N | audit-py | a design question decided and recorded |
| [#324] | P3/M | PROSE-CONVERTIBLE | N | audit-py | 'codified' unhomed; '(next session)' is an expired temporal peg |
| [#327] | P2/M | MECHANICAL (off-repo) | N | architecture | genre doc + per-repo protocols/README.md + >=1 interface doc |
| [#329] | P3/S | MECHANICAL | N | settings-json | generator emits + regenerates deterministically (regen-and-diff) |
| [#331] | P2/S | MECHANICAL (off-repo) | N | (none) | the ruling's output has a machine-readable home: .methodology.yaml per consumer |
| [#332] | P2/M | MECHANICAL | N | audit-py | manifest ships + drifted WARNs / at-parity does not, with a test |
| [#334] | P3/S | MECHANICAL (off-repo) | N | pre-commit-config | id migrated in 3 repos + a staged violation BLOCKED per repo |
| [#335] | P3/S | MECHANICAL | N | audit-py | no flag on a templates/ placeholder, with a test + auto-clear |
| [#338] | P2/S | PROSE-CONVERTIBLE | N | codex-review | (b)-(e) are body-enumerated; the defer branch has no home |
| [#340] | P2/S | MECHANICAL (off-repo) | N | (none) | validator applies the declared filter, witnessed green n=1 |
| [#341] | P2/S | PROSE-CONVERTIBLE | N | codex-review | (i)-(iv) body-enumerated; 'mechanism witnessed once' needs an artifact |
| [#342] | P3/S | MECHANICAL | N | audit-py | three named behaviours, each with a test |
| [#343] | P3/S | MECHANICAL | N | audit-py | a test proving both halves |
| [#344] | P2/M | PROSE-CONVERTIBLE | N | handoff | Ask 1 (a)(b)(c) are mechanical in-body; the defer branch has no home |
| [#345] | P2/M | MECHANICAL | N | pre-commit-config | registry ships, gate reads it, pass/block cases, with tests |
| [#346] | P2/S | PROSE-CONVERTIBLE (off-repo) | N | claude-md | rule+verify: line is greppable; the permanent-defer branch has no home |
| [#347] | P2/M | PROSE-CONVERTIBLE | N | playbook | 'filed sub-arcs' -> task ids; the safe-deletion ruling needs a home |
| [#348] | P3/S | MECHANICAL | N | settings-json | the row already carries a routine: block; routine_consumers is the live organ |
| [#349] | P2/M | PROSE-CONVERTIBLE | N | audit-py | 'verified on a cold session' + 'merged into #344' both need a recorded form |
| [#350] | P3/S | PROSE-CONVERTIBLE | N | handoff | (a)(b)(c) mixed; the permanent-defer branch has no home |
| [#351] | P3/M | PROSE-CONVERTIBLE | N | pre-commit-config | 'an upgrade path is defined' unhomed; the review-date branch is convertible |
| [#352] | P3/S | MECHANICAL | N | settings-json | coverage of >=1 governed file + no hand-maintained state; amendment says satisfied-by-elimination |
| [#353] | P2/M | PROSE-CONVERTIBLE | N | audit-py | leg 1 is a testable refusal; the permanent-defer branch has no home |
| [#354] | P2/M | MECHANICAL | N | playbook | seeded staged amendment is flagged, with a test |
| [#356] | P2/M | PROSE-CONVERTIBLE | N | playbook | cites a 'declared-unenforced' register that DOES NOT EXIST anywhere in the repo |
| [#357] | P2/M | PROSE-CONVERTIBLE | N | audit-py | silent-rule-baseline.yaml is the home; 'every ADR-borne MUST-rule carries a state' needs the sweep's denominator |
| [#358] | P2/S | PROSE-CONVERTIBLE | N | architecture | 'the three stale sites' body-enumerated; the record-with-reason branch has no home |
| [#359] | P1/M | DEFECTIVE | N | handoff | DRIFTED LOCATOR: the claim is no longer at HANDOFF_PROCESS.md:517-518; it is at :775-776 AND restated at :938-939 |
| [#360] | P3/S | DEFECTIVE | N | audit-py | DRIFTED LOCATOR: DoD:106-109 now holds the BACKLOG advisory; the referent is the '## Scope-freeze' section (expired 2026-07-14, still standing) |
| [#361] | P3/S | PROSE-CONVERTIBLE | N | audit-py | 'states the guard's real scope' needs the scope statement pinned to a checkable form |
| [#362] | P2/M | PROSE-CONVERTIBLE | N | audit-py | 'each dropped rule' needs the dropped set enumerated |
| [#364] | P3/S | PROSE-CONVERTIBLE | N | audit-py | leg 1 is mechanical (seed an over-length [#353], assert doc_rot green); the accept branch has no home |
| [#365] | P3/S | MECHANICAL | N | audit-py | markers + multi_site + edge resolves + row moves + ship-gate baseline |
| [#366] | P2/S | PROSE-CONVERTIBLE | N | audit-py | leg 1 mechanical with a regression test; the accept-with-reason branch has no home |
| [#369] | P3/S | DEFECTIVE | N | pre-commit-config | DRIFTED CARDINALITY: 'doc-counts reflects 16 gates'; doc-counts.md:15 says 17 today and moves with every gate added |
| [#371] | P2/S | PROSE-CONVERTIBLE | N | settings-json | 'the ADR rules the vehicle' + 'implemented: reflects reality' — the latter is mechanical, the former is not |
| [#383] | P2/L | DEFECTIVE | N | architecture | DRIFTED LOCATOR: 'the 8 rows at parity-surfaces.yaml:834-899'; there are 9 kind: gitignore-effect rows and they live at :910-978 |
| [#385] | P3/M | PROSE-CONVERTIBLE | N | architecture | 'flows end-to-end' needs the three artifacts named |
| [#387] | P2/S | PROSE-CONVERTIBLE | N | architecture | 'rewritten to the ruled position' unverdictable; 'before any ADR cites it' is greppable |
| [#388] | P3/S | MECHANICAL | N | architecture | grep the figure fleet-wide + the immutable four unedited in git |
| [#389] | P2/S | PROSE-CONVERTIBLE | N | audit-py | leg 2 is a testable refusal; 'R6 is ruled' and the defer branch are not |
| [#390] | P2/S | MECHANICAL | N | handoff | ADR carries the resolution AND the template matches it — both greppable |
| [#391] | P3/S | PROSE-CONVERTIBLE | N | audit-py | 'fires nightly' needs an observable; the narrow-and-file branch is convertible |
| [#392] | P3/S | MECHANICAL | N | audit-py | rename-back carries full history, with a covering test |
| [#393] | P3/S | PROSE-CONVERTIBLE (off-repo) | N | audit-py | 'confirmed-live or retired' per candidate, in corp-sca; needs a recorded verdict form |
| [#397] | P3/M | PROSE-JUDGMENT | N | audit-py | the operator rules adopt/reject on a structural map |
| [#399] | P2/S | PROSE-CONVERTIBLE | N | handoff | 'the claim and the mechanism agree' + 'status is explicit' need a declared form |
| [#400] | P3/S | PROSE-JUDGMENT | N | claude-md | an ownership-model ruling |
| [#401] | P2/S | MECHANICAL (off-repo) | N | architecture | (a) config edit in ai-council + (b) a path-refusal in routing.py — both observable |
| [#402] | P3/S | MECHANICAL | N | architecture | the 4 post-ratification docs are named in-body; the grammar is greppable |
| [#403] | P3/S | MECHANICAL | N | audit-py | two gated claim classes, with tests |
| [#404] | P2/S | MECHANICAL | N | handoff | an execution-mode render passes with zero SUPPLEMENT refs, per-mode test |
| [#405] | P2/S | MECHANICAL | N | settings-json | each named leftover class flagged, with a test |
| [#406] | P3/S | PROSE-JUDGMENT | N | audit-py | an architect ruling picks the enforcement point (ADR-108 SSA re-routed) |
| [#407] | P3/M | PROSE-JUDGMENT | N | playbook | an architect ruling on a paradigm stance |
| [#408] | P2/M | PROSE-CONVERTIBLE | N | audit-py | leg 1 is testable; the deferred-with-reason branch has no home |
| [#409] | P3/S | PROSE-CONVERTIBLE | N | (none) | routine: block + routine_consumers is the exact mechanical home (see [#348]/[#426]) |
| [#410] | P3/S | PROSE-CONVERTIBLE | N | (none) | routine: block + routine_consumers is the exact mechanical home (see [#348]/[#426]) |
| [#411] | P3/S | PROSE-CONVERTIBLE | N | (none) | routine: block + routine_consumers is the exact mechanical home (see [#348]/[#426]) |
| [#412] | P3/M | PROSE-CONVERTIBLE | N | (none) | 'the research is captured' + 'a doctrine is recorded' need named homes |
| [#413] | P2/S | PROSE-CONVERTIBLE | N | claude-md | review_date is machine-readable; 're-grounded on the ruled model' is not |
| [#414] | P2/S | PROSE-CONVERTIBLE | N | settings-json | leg 2 is a testable refusal; 'a ruling picks the organ(s)' needs its home |
| [#415] | P2/S | PROSE-CONVERTIBLE | N | audit-py | 'the sibling audit is run' + 'recorded justified' need an artifact and a home |
| [#417] | P3/S | PROSE-CONVERTIBLE | N | settings-json | leg 1 is testable; 'recorded rejected with a reason' has no home |
| [#418] | P2/S | PROSE-CONVERTIBLE | N | audit-py | 'reproduced under instrumentation' + a one-per-day contract are convertible |
| [#419] | P2/M | PROSE-CONVERTIBLE | N | settings-json | leg 1 IS routine_consumers today; 'unconsumed output is surfaced' has no organ |
| [#420] | P3/S | PROSE-JUDGMENT | N | architecture | a kept-vs-dissolved ruling; the '9 files' cardinality VERIFIES (docs/archive holds 9 + README) |
| [#422] | P2/S | MECHANICAL | N | handoff | a post-fold check FAILs, pinned by a seeded test |
| [#423] | P2/M | PROSE-CONVERTIBLE | N | (none) | 'each precondition checked mechanically' is convertible once the sequence is enumerated |
| [#424] | P2/S | MECHANICAL | N | audit-py | every clause parses + regression test + twin lockstep |
| [#425] | P2/S | PROSE-CONVERTIBLE | N | audit-py | 'audited for input-form coverage' + 'recorded justified' need a form |
| [#426] | P2/M | MECHANICAL | N | settings-json | routine_consumers already verdicts leg 1; 'nags resolved' follows from it |
| [#427] | P3/S | MECHANICAL (off-repo) | N | claude-md | substitution mechanism + the named divergence retires |
| [#428] | P2/S | PROSE-CONVERTIBLE (off-repo) | N | settings-json | leg 1 mechanical; 'the 15 open Issues' is an off-repo GitHub count that cannot be verified here |
| [#430] | P2/M | PROSE-CONVERTIBLE | N | audit-py | (a) is RULED already (conftest ruling, 3cf3a5b0); (b) 'reproducible from the subject's own state' is convertible |
| [#431] | P2/S | MECHANICAL (off-repo) | N | codex-review | both-profiles-or-loud-warning + counter agreement, with tests |
| [#438] | P3/S | PROSE-CONVERTIBLE | N | playbook | 'PLAYBOOK carries the rule' is greppable; 'one arc has run under it' needs an artifact |
| [#440] | P2/S | MECHANICAL | N | architecture | a deleted retired record FAILs, with a seeding test |
| [#442] | P2/M | MECHANICAL | N | settings-json | invalidation or stamp mismatch, with a test seeding a stale copy |
| [#443] | P3/S | PROSE-CONVERTIBLE | N | playbook | 'each uncovered class' needs the class list enumerated |
| [#445] | P2/S | MECHANICAL (off-repo) | N | codex-review | fail-loud or dual-route, with a seeded test |
| [#447] | P3/S | MECHANICAL | N | gates | two self-reference cases, with tests |
| [#448] | P2/S | MECHANICAL | N | audit-py | two-bundle staged diff fails when either is uncovered, with a test |
| [#449] | P3/S | PROSE-JUDGMENT | N | handoff | a budget ruling or an accepted-with-reason hold |
| [#450] | P3/S | PROSE-JUDGMENT | N | architecture | a schema-vs-convention ruling |
| [#451] | P2/M | MECHANICAL | N | audit-py | check exists + runs in the gate set + scope stated + ADR cites it |
| [#452] | P3/S | DEFECTIVE | N | audit-py | MOOT REFERENT: tasks/433 and tasks/382 are BOTH status: closed; the ordering between two closed rows cannot be enforced or violated |
| [#453] | P2/M | PROSE-CONVERTIBLE | N | environment | 'a runbook records all three gaps' is convertible; the accept-as-is branch has no home |
| [#454] | P2/S | MECHANICAL | N | audit-py | RED-first tests + both copies + a terra review artifact (review_artifact_coverage) |
| [#456] | P2/M | PROSE-CONVERTIBLE | N | (none) | 'the cohort' is defined in an external dossier, not in the row; enumerate ids to convert |
| [#457] | P2/S | MECHANICAL | N | audit-py | both tests pass on main + verification recorded in the fixing commit |
| [#463] | P2/S | PROSE-CONVERTIBLE (off-repo) | N | environment | the four map 1:1 onto live audit checks; 'accept-with-reason' has no home |
| [#464] | P2/S | PROSE-CONVERTIBLE (off-repo) | N | environment | 'each of the five' body-enumerated; 'accept-with-reason' has no home |
| [#470] | P3/S | MECHANICAL | N | audit-py | REPRODUCED LIVE this session: audit.py checks crashes on cp1252 at the U+2192 |
| [#477] | P2/S | MECHANICAL | N | audit-py | resolves from a differently-named root, with a seeding test |
| [#478] | P2/S | MECHANICAL | N | (none) | PEP 440 comparison, with tests |
| [#484] | P3/M | PROSE-CONVERTIBLE | N | environment | 'closed on the operator's machines' + two defer branches, none homed |
| [#485] | P3/S | MECHANICAL (off-repo) | N | audit-py | one helper + a CRLF-cannot-land test + the gotcha entry retired/re-scoped |
| [#486] | P3/S | MECHANICAL | N | (none) | ASCII swap + a cp1252-encodability regression |
| [#487] | P2/L | PROSE-CONVERTIBLE | N | (none) | (i)-(iv) body-enumerated and mechanical; 'a cadence prevents re-accumulation' is not |
| [#488] | P2/M | PROSE-JUDGMENT | N | (none) | the architect rules the ranking axis |
| [#491] | P3/S | PROSE-CONVERTIBLE | N | (none) | 'the ruling is recorded' + 'one acceptance run with evidence' need homes |
| [#493] | P2/S | PROSE-CONVERTIBLE | N | (none) | 'the cause is identified with evidence' -> a named report; convertible |
| [#496] | P3/S | MECHANICAL | N | (none) | mapping fixed or split declared, with a pinning test |
| [#497] | P3/S | MECHANICAL | N | (none) | both claims corrected + the carrier test asserts against the live probe |
| [#500] | P3/S | MECHANICAL | N | (none) | the advisory stays silent on a sanctioned close, pinned by a test |
| [#502] | P3/M | PROSE-CONVERTIBLE | Y | environment | 'a scoped pilot runs on CI' is blocked on [#501]; ADOPT/REJECT needs a home |
| [#505] | P1/M | DEFECTIVE | Y | playbook | UNMEETABLE CLAUSE: 'batch-1 executes under it with exactly 2 operator touches' — batch-1 is history (2026-08-06) and cannot be re-run under a later protocol; clause 1 already falsified 3x |
| [#506] | P2/M | PROSE-CONVERTIBLE | Y | (none) | 'a ranked evidence sheet covers the full open set' is mechanical once the sheet's fields are named |
| [#507] | P3/S | PROSE-JUDGMENT | Y | architecture | a ruling on whether the fourth leg lands |
| [#508] | P3/S | PROSE-CONVERTIBLE | Y | gates | leg 1 is fully mechanical; the row itself offers the unmechanized-ruling branch |
| [#509] | P3/S | MECHANICAL (off-repo) | N | (none) | resolves in either shape, with a test + an unedited variable-form launch |
| [#510] | P2/M | MECHANICAL | N | gates | roster-scoped exemption + a test proving an outside branch is not exempt + the field carried |
| [#511] | P2/M | PROSE-CONVERTIBLE | N | handoff | 'encoded (version bump + reconciliation)' + 're-measured cut' are mechanical; 'the operator rules which load' is not |
| [#513] | P2/M | PROSE-CONVERTIBLE | N | (none) | 'a detector reports' is mechanical; 'the three instances' are body-enumerated |
| [#514] | P1/M | MECHANICAL | N | (none) | provisioning refuses off-enum + exactly ONE definition remains (grep-countable) |
| [#518] | P2/S | MECHANICAL | N | (none) | scrub + explicit decode, with a test reproducing each defect first |
| [#519] | P1/M | MECHANICAL | N | architecture | a seeded status-only close FAILS the generator run |
| [#520] | P2/S | MECHANICAL | N | handoff | marker surface + the bundle carries one + check_seal_identity skips it, with a test |

---

## 3. DEFECTIVE — eight rows, each verified by hand

Every verdict here was checked against live state this session. Four are **drifted locators or
cardinalities** — the row was right when written and the world moved underneath it, which is
`[#503]`'s named failure class arriving inside the backlog itself. Two are **dead referents**.
Two are **unmeetable clauses**.

### `[#170]` P3/M — DEAD REFERENT: the row it depends on has no ledger record

Done-when: *"an ADR defines the issue-ID↔commit linkage **and #168 has a ratified anchor to
depends-on**."*

There is **no `tasks/168-*.md` in any status** — not open, not closed, not deferred, not
retired. `[#168]` has no record in the ledger at all, so the second clause names a row to which
nothing can be added. The row's own body says it *"absorbs #168"*, which contradicts its
Done-when treating `#168` as a separate row still owing a `depends-on` edge.

**Repair:** strike clause 2, or restate it as the absorbed obligation (*"the ADR's linkage is
what promotes the ADR-85 BACKLOG leg from advisory to hard"*). This is a phrasing repair, not a
build — needs an author decision on which reading was meant.

### `[#241]` P2/S — DRIFTED CARDINALITY: "each of the 6" against a live 20

Done-when: *"**each of the 6** is either declared (`reconciled_with`) or recorded
permanent-defer-with-reason, and its disposition entry retires or is re-annotated."*

`ecosystem/disposition-register.yaml` carries **20** `id: warn-undeclared-*` entries today
(counted this session; N-A reported the same 20 this morning). The population the row was
written against has more than tripled. **A Done-when that names a count silently expires when
the count moves** — and this one has no mechanism watching it.

Already surfaced by N-A §4; carried here with the count re-verified and the class named.

### `[#359]` P1/M — DRIFTED LOCATOR, and there is a second site the row does not know about

Title and subject: *"PHANTOM ENFORCEMENT — `protocols/HANDOFF_PROCESS.md:517-518` claims a
mechanism that does not exist."*

`HANDOFF_PROCESS.md:512-522` today holds an *honest-limits* passage about worktree / write-scope
/ MODE-basis carrying no probe leg — the opposite of a phantom claim. The claim the row is
about is alive and has **moved to `:775-776`**:

> *"**FILE-BOUNDARY** — the explicit file/dir set the lane may touch. This is the parallelism
> ruling made mechanical …"*

and it is **restated a second time at `:938-939`** (*"FILE-BOUNDARY as the parallelism ruling
made mechanical"*), a site the row does not name. So the row is not wrong about the defect —
it is wrong about where the defect is, and it under-counts it.

**This is a P1 whose locator rotted inside a file that advanced 6.1.0 → 6.2.0 under it.**
Repair: re-peg to the **anchor text** (`FILE-BOUNDARY … made mechanical`), not the line number,
and add the `:938-939` site to the correction scope.

### `[#360]` P3/S — DRIFTED LOCATOR, and N-A's "intent unrecoverable" is refuted

Title: *"`protocols/DEFINITION_OF_DONE.md:106-109` expired in place."* Done-when: *"the freeze
is lifted, renewed with a new window, or recorded expired-with-reason."*

N-A recorded that the locator had drifted and that *"whether that is the intended referent
cannot be established from the row … Needs the author's intent, not more searching."* **A
little more searching establishes it.** `DEFINITION_OF_DONE.md` carries a `## Scope-freeze`
section:

> *"**No docs are added to this gate for 4 weeks** from ADR-85 (i.e. until ~2026-07-14) — gather
> reliability and override-rate data first."*

That is a freeze, with a window, which **expired 27 days ago and is still standing verbatim** —
precisely "expired in place". The row's Done-when ("lifted, renewed, or recorded
expired-with-reason") fits it exactly and fits nothing else in the file. **Intent is
recoverable; the referent is the `## Scope-freeze` section.**

Verdict stays DEFECTIVE because the *locator as written* is dead, but the repair is now a
one-line re-peg to anchor text and the row can then be adjudicated on its merits.

### `[#369]` P3/S — DRIFTED CARDINALITY: "16 gates" against a live 17

Done-when: *"the hook is registered and blocks a hand-edited header, `CLAUDE.md` §9 lists it,
and **doc-counts reflects 16 gates**."*

`ecosystem/doc-counts.md:15` reads `- pre-commit gates (17)`. The row pinned the post-landing
number at authoring time; three gates have landed since. **The clause will drift again with
every gate added**, which makes the absolute count the wrong predicate regardless of repair.

Repair: replace the absolute count with a relative one — *"`ecosystem/doc-counts.md`'s
pre-commit-gate count increases by exactly one in the landing commit and `doc_claims` stays
green"* — which cannot expire.

### `[#383]` P2/L — DRIFTED LOCATOR **and** cardinality, in the corpus's best-phrased clause

Done-when: *"for the **8** gitignore-effect rows at `ecosystem/parity-surfaces.yaml:834-899`,
(a) `python scripts/desired_state_report.py` shows no `diverge` cell on any of the 8 rows; AND
(b) `python scripts/fleet_parity.py --run-date <run-date>` reports 0 warn-undeclared, 0
must-absent and 0 tombstone-violated across those same 8 rows …"*

Both pins are wrong today. `ecosystem/parity-surfaces.yaml:834-899` holds `changelog-review` and
`audit-casing-r4` rows; the `kind: gitignore-effect` rows live at **`:910-978`** and there are
**9** of them, not 8.

**This is the most instructive defect in the set.** Legs (a) and (b) are the *finest* Done-when
phrasing anywhere in the corpus — they name the command, the flag, the field and the expected
value, so a reader can verdict them without judgment. And the clause is still not verdictable,
because the *subject* is pinned by line range and count rather than by the `kind:` field that
actually defines it. Mechanical predicates over a drifting subject are still unverdictable.

Repair: *"for every row in `ecosystem/parity-surfaces.yaml` with `kind: gitignore-effect`
(9 today) …"* — a selector, not a location.

### `[#452]` P3/S — MOOT REFERENT: both subjects are closed

Done-when: *"the pair is either expressed as a parseable `depends-on` clause or recorded as
intentionally prose-carried …"* — the pair being `[#433]` → `[#382]`.

`tasks/433-backlog-restructure-build-thin-engine-backlog-md.md` is **`status: closed`** and
`tasks/382-desired-state-data-model-intake-adr.md` is **`status: closed`**. The row exists to
make a *sequencing* obligation machine-enforceable between two rows that can no longer be
sequenced. Adding a `depends-on` edge between two closed rows enforces nothing; recording it as
"intentionally prose-carried" records a fact about history.

**The generalisable half survives** — *nothing owns propagating a ruled ordering into the
dependency graph* — but that is `[#513]`'s shape (propagation completeness), not this row's.
**Kill candidate, §5.**

### `[#505]` P1/M — UNMEETABLE CLAUSE: a finish line in the past tense

Done-when clause 2: *"**batch-1 executes under it** with exactly 2 operator touches."*

Batch-1 executed on 2026-08-06, **before** ADR-110 and before the artifacts this row would
create. It cannot execute again, so the clause can never be satisfied by any future act. N-A
separately recorded it as UNDETERMINED because no operator-touch count was ever written down —
but the deeper problem is not the missing measurement, it is that **the measurement can no
longer be taken.**

N-A also recorded clause 1 (*"a fresh seat runs a full batch from repo artifacts alone"*) as
falsified three consecutive times. **Tonight is the fourth**: this lane's contract arrived as a
file in `~/Downloads`, not as a committed repo artifact.

**A P1 with one unmeetable clause and one clause falsified four times running is not being
tested — it is being re-observed.** Repair: re-peg clause 2 to the *next* batch
(*"the next batch executes under it with its operator-touch count recorded in the batch
manifest"*), which is both meetable and mechanically countable.
---

## 4. Conversion drafts — the P1+P2 band

**42 drafts.** Every PROSE-CONVERTIBLE row at P1 or P2 gets one. (There are no PROSE-CONVERTIBLE
P1 rows: the five P1s are three MECHANICAL and two DEFECTIVE.) P3 rows get a class verdict in §2
and no draft, per contract.

> **EVERY DRAFT BELOW IS A DRAFT.** It applies only under a later operator ruling. Nothing in
> this section has been written to any task file, and this lane has no authority to write one.

Each draft preserves the row's intent or says where it could not. **Where intent is
unrecoverable the verdict is DEFECTIVE (§3), never a guessed rewrite.**

### Form E — the single biggest lever, applied 21 times below

**37 of 170 open rows** end a clause with an unhomed escape hatch: *"…, or recorded
permanent-defer-with-reason"*, *"…, or recorded accept-with-reason"*, *"…, or the divergence is
recorded with a reason"*. **30 of them are PROSE-CONVERTIBLE for that reason alone** — the
build leg is already mechanical and the escape branch is what makes the clause unverdictable,
because *recorded where?* has no answer.

`protocols/STANDING_RULINGS.md` is the live in-repo register for exactly this: ratified
decisions, lettered sections, each with its reason. Naming it makes the branch checkable today
with no new machinery:

```
Form E — replace:   ..., or recorded <X>-with-reason
with:               ..., or `protocols/STANDING_RULINGS.md` carries a section
                    naming `[#NNN]` and stating the reason
Predicate:          a `###` section in protocols/STANDING_RULINGS.md whose body
                    contains the literal `[#NNN]`
```

`ecosystem/disposition-register.yaml` is the alternative **only** where the record suppresses a
specific audit-organ WARN — that file's contract is one entry per suppressed Finding, and using
it as a general "we decided not to" register would break the stale-decoration rule (ADR-75).

**Choosing the home is one decision that converts 30 rows by substitution.** It is question Q2
in §8. The drafts below are written against `STANDING_RULINGS.md` so they are paste-ready today;
if the operator names a different home, the substitution is textual.

---

#### `[#112]` P2/M — adr_amend helper + ADR immutable-zone extension
- **Now:** *"…and CLAUDE.md §5 is de-contradicted + restamped"*
- **DRAFT:** *"an in-place ADR edit NOT routed through the helper is blocked and a helper-written Amendment passes (both with tests), and `CLAUDE.md` §5 rule 3 states the helper as the sanctioned in-place path with `last_reviewed` re-stamped in the same commit"*
- **Intent:** "de-contradicted" names an outcome without naming the contradiction. §5 rule 3 already carries the ADR-94 status-line exception; the draft pins what the new text must assert, so a reader can verdict it by grep instead of by judgment. No scope added.

#### `[#123]` P2/S — Routine observability convention + value review
- **Now:** *"the marker convention is recorded + adopted by the fleet/routine jobs AND one morning-funnel value review records per-routine findings-acted-on vs noise"*
- **DRAFT:** *"the marker convention is recorded in `protocols/PLAYBOOK.md`, every routine declared under `routine_consumers` carries the marker, and one `docs/audits/<date>-technical-*` value review records per-routine findings-acted-on vs noise counts"*
- **Intent:** unchanged substance; "adopted by the fleet/routine jobs" gains the denominator that already exists (`routine_consumers`'s declared set) and the review gains a filed home.

#### `[#132]` P2/M — Organ-index generator
- **Now:** *"the generator emits `docs/ORGAN-INDEX.md` **covering all organ classes** and a freshness hook flags a stale index"*
- **DRAFT:** *"the generator emits `docs/ORGAN-INDEX.md` covering every organ class enumerated in `ARCHITECTURE.md` Ch2's organ map, a regen-and-diff pre-commit hook FAILs on a stale index (with a test), and `ecosystem/doc-counts.md` reflects the new gate"*
- **Intent:** "all organ classes" had no denominator, so completeness was unverdictable. Ch2's organ map is the live enumeration and is already the canonical one. Adds the doc-counts leg because every gate landing has needed it (`[#369]`'s lesson).

#### `[#162]` P2/M — Vocab decision
- **Now:** *"an ADR or operator ruling lands the disambiguation across all enumerated surfaces"*
- **DRAFT:** *"an ADR or a `protocols/STANDING_RULINGS.md` section lands the disambiguation, and each of `protocols/HANDOFF_BOOT.md`, `protocols/HANDOFF_PROCESS.md` §13, `ARCHITECTURE.md` Ch1 uses the ruled term with no surviving use of the superseded one"*
- **Intent:** "all enumerated surfaces" pointed at the row's own `refs` list; the draft inlines it so the clause is self-contained and greppable. Same three surfaces, no more.

#### `[#220]` P2/M — MODIFY / semantic-drift axis
- **Now:** *"a verify-first pass records whether any existing organ detects a semantic/MODIFY change on a fixture"*
- **DRAFT:** *"a committed fixture exercises a semantic/MODIFY change, a `docs/audits/` record names which organs fired and which did not against it, and the design leg stays deferred pending that result"*
- **Intent:** the spike is genuinely an experiment, and experiments are mechanizable by their artifact. Preserves the row's deliberate deferral of the design leg.

#### `[#277]` P2/M — propose_closures signal repair
- **Now:** *"the two STRONG FPs no longer surface AND the WEAK heuristic is reworked or retired so **a representative run** beats this run's 49:0 ratio, with tests"*
- **DRAFT:** *"the two STRONG false positives no longer surface (pinned by a test seeding each), and a single run over the last 30 days of `main` yields a STRONG:WEAK-actioned ratio better than 49:0 with the run's numbers recorded in the closing commit, with tests"*
- **Intent:** "a representative run" was undefined and the 49:0 baseline log (`logs/PROPOSALS-2026-07-07.md`) is **gitignored**, so the comparison had no reproducible referent. The draft fixes the window instead of the artifact — the 49:0 number survives in the row text and does not depend on a file that was never tracked.

#### `[#278]` P2/M — Test-suite hygiene epic
- **Now:** *"both UAT ACs hold AND the theatricality review + impacted-test selection ship"*
- **DRAFT:** *"both acceptance criteria from `docs/intake/archive/2026-07-07-test-suite-hygiene.md` hold with the criterion text quoted in the closing commit, and the theatricality review ships as a `docs/audits/` artifact and impacted-test selection is live in the verify cadence with a test"*
- **Intent:** "both UAT ACs" lived in an archived intake, so the finish line was one indirection away from any reader. Quoting them at closing time keeps the row short without leaving the referent floating.

#### `[#338]` P2/S — codex-review drift consolidation
- **Now:** *"each of (b)-(e) resolved or recorded permanent-defer-with-reason"*
- **DRAFT:** *"each of (b), (c), (d), (e) as enumerated in this row is resolved with its evidence in the closing commit, **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#338]` and that item's reason"* [Form E]
- **Intent:** the (b)-(e) set is body-enumerated and stays as-is; only the escape branch gains a home.

#### `[#341]` P2/S — Codex producer-lane activation mechanism
- **Now:** *"(i)-(iv) each resolved or recorded permanent-defer-with-reason, mechanism witnessed once, PLAYBOOK §16 reconciled"*
- **DRAFT:** *"(i)-(iv) as enumerated in this row are each resolved **or** named with their reason in a `protocols/STANDING_RULINGS.md` section citing `[#341]`; one activation run is recorded in a `docs/audits/` artifact; and `protocols/PLAYBOOK.md` §16 describes the shipped mechanism"* [Form E]
- **Intent:** "witnessed once" becomes an artifact rather than a memory; §16 "reconciled" becomes "describes the shipped mechanism", which a reader can check against the code.

#### `[#344]` P2/M — Session-close gate + consumer hub-write guard
- **Now:** *"Ask 1 and Ask 2 are each resolved or recorded permanent-defer-with-reason, with a test where a mechanism lands"*
- **DRAFT:** *"Ask 1 lands as a pre-handoff gate that REFUSES (re)generation unless (a) a `docs/audits/` session artifact exists, (b) the BACKLOG gate and `canonical_freshness` A2 are green for the session's merges, and (c) a HEAD-bound close-readiness token is recorded — with a test per leg; and Ask 2 lands as a consumer-side PreToolUse guard BLOCKING Write/Edit/NotebookEdit resolving under `.dev-knowledge/` or `~/.claude/`, with a test; **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#344]` and the reason for each Ask not built"* [Form E]
- **Intent:** Ask 1's (a)(b)(c) and Ask 2 are already fully mechanical **in the row body** — the Done-when just didn't inherit them. Note: the row's cited intake lives in **ai-council**, not the hub; that is an off-repo reference, not a dead one.

#### `[#346]` P2/S — Persist the two-tier new-path executor rule into `~/.claude`
- **Now:** *"the `~/.claude` executor rule lands under an explicit ruling with a `verify:` line, OR is recorded permanent-defer-with-reason"*
- **DRAFT:** *"`~/.claude/rules/` carries the two-tier new-path executor rule with a `verify:` line and the authorizing ruling cited in-file, **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#346]` and the reason it stays hub-side"* [Form E]
- **Intent:** unchanged. Leg 1 was already greppable once the file is named; core-invariant #6 keeps the edit ruling-gated either way, and the draft does not weaken that.

#### `[#347]` P2/M — Formalize the engineering loop/harness + safe-deletion pattern
- **Now:** *"the loop-harness is decomposed into filed sub-arcs AND the safe-deletion pattern is ruled (sanctioned path defined or recorded permanent-defer-with-reason)"*
- **DRAFT:** *"the loop-harness is decomposed into filed `tasks/*.md` rows whose ids are listed in this row's closing commit, and the safe-deletion pattern is documented in `protocols/PLAYBOOK.md` **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#347]` and the reason it stays unruled"* [Form E]
- **Intent:** "filed sub-arcs" becomes countable (task ids exist or they don't) without prescribing how many.

#### `[#349]` P2/M — Mechanize session-discipline inheritance
- **Now:** *"a fresh session inherits the test-then-close discipline from a mechanism (boot-injected + Stop-gated) with no operator reminder, verified on a cold session, OR merged into #344 with a recorded reason"*
- **DRAFT:** *"a boot-injected + Stop-gated mechanism carries the test-then-close discipline with a test per leg, and one cold-session run is recorded in a `docs/audits/` artifact; **or** this row is closed as folded into `[#344]` with the fold recorded in `protocols/STANDING_RULINGS.md`"*
- **Intent:** "with no operator reminder" is the row's real point and is unverifiable as phrased — a recorded cold-session run is the closest honest instrument, and it is what the row already asks for.

#### `[#353]` P2/M — Session-boot contract hardening
- **Now:** *"a mechanism refuses a mid-session order whose side effects aren't worktree-scoped while the tree is dirty (or lacks a worktree declaration), with a test, OR recorded permanent-defer-with-reason"*
- **DRAFT:** *"a mechanism refuses a mid-session order whose side effects are not worktree-scoped while the tree is dirty or no worktree is declared, with a test seeding each of the two refusal conditions; **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#353]` and the reason"* [Form E]
- **Intent:** unchanged; the parenthetical becomes two named seed cases so "with a test" has a defined obligation.

#### `[#356]` P2/M — RULING-W and the merge-delegation composite
- **Now:** *"RULING-W and the composite each carry either a mechanism or **a declared-unenforced entry (owner + review date)**, AND both … have a ratified decision record or a recorded permanent-defer-with-reason"*
- **DRAFT:** *"RULING-W and the merge-delegation composite each carry either a live mechanism with a test, or an entry in `ecosystem/silent-rule-baseline.yaml` with `owner:` and `review_date:` fields; and each carries a ratified ADR or a `protocols/STANDING_RULINGS.md` section naming `[#356]`"* [Form E]
- **Intent + a defect worth naming:** **the "declared-unenforced" register the row cites does not exist anywhere in this repo** — `grep -rn 'declared-unenforced'` over `scripts/`, `ecosystem/` and `protocols/` returns nothing. This row's Done-when has been unmeetable since it was written, not because a referent died but because one was never created. `ecosystem/silent-rule-baseline.yaml` is the nearest live surface (it already tracks the silent-rule pool for `silent_rule_ratchet`) and the draft points there; **if the architect wants a distinct register, that is a build, and this row is its trigger.** Flagged as Q3 in §8.

#### `[#357]` P2/M — Silent-rule census run 2
- **Now:** *"`docs/decisions/` is swept, every ADR-borne MUST-rule carries a state, and a combined denominator + N_silent supersedes the [E8] baseline"*
- **DRAFT:** *"every `must|shall|never` occurrence in `docs/decisions/ADR-*.md` is enumerated in the sweep artifact and carries a state in `ecosystem/silent-rule-baseline.yaml`, and the file's combined denominator and N_silent replace the [E8] figures with `silent_rule_ratchet` green at the new numbers"*
- **Intent:** the row's substance is a census, and a census is mechanical once the denominator is defined by a token rule. `silent_rule_ratchet` already uses exactly this token class, so the draft reuses the live definition rather than inventing one.

#### `[#358]` P2/S — `parity-surfaces.yaml` misdescribes its own enforcement posture
- **Now:** *"the three stale sites state the post-#337 blocking posture, or the divergence is recorded with a reason"*
- **DRAFT:** *"each of the three sites enumerated in this row states the post-`[#337]` blocking posture, **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#358]` and the reason the divergence stands"* [Form E]
- **Intent:** unchanged. The three sites are body-enumerated; only the escape branch gains a home.

#### `[#362]` P2/M — #242 carries a SUBSTANTIVE guard loss
- **Now:** *"each dropped rule is carried, consciously dropped with a reason, or superseded — before any status-flip closes #242"*
- **DRAFT:** *"the dropped-rule set is enumerated in this row or its closing commit, and each member is carried into a live surface, superseded by a named ADR, or recorded in a `protocols/STANDING_RULINGS.md` section naming `[#362]`; and `[#242]` does not reach a terminal status before this row does"* [Form E]
- **Intent:** "each dropped rule" had no roster, so completeness could not be verdicted. The ordering constraint is preserved and made checkable by status rather than by vigilance.

#### `[#366]` P2/S — `residual_completeness` scans the working tree, not the staged blob
- **Now:** *"the check validates staged blob content at commit time (e.g. `git show :<path>`), with a regression test seeding staged-unfilled + working-filled, OR the limit is recorded as accepted-with-reason"*
- **DRAFT:** *"`validate_residual_completeness` reads staged blob content at commit time, with a regression test seeding a staged-unfilled + working-filled pair that FAILs before the fix and passes after; **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#366]` and the accepted limit"* [Form E]
- **Intent:** unchanged. Leg 1 was already one of the better-phrased clauses in the corpus; only the escape hatch was unhomed. "RED-first" is made explicit because the row's value is the regression, not the code.

#### `[#371]` P2/S — Consumer editor-config write-through
- **Now:** *"the ADR rules the vehicle, the config reaches both consumers under it, and `implemented:` reflects reality"*
- **DRAFT:** *"an ADR names the carrier vehicle, both consumers carry the editor config under it (verified per repo), and `deploy/manifest-v1.4.0.yaml`'s `implemented:` value for this component matches the live per-consumer state with `fleet_parity` green"*
- **Intent:** "reflects reality" is exactly the claim `fleet_parity` exists to verdict; the draft routes the leg to the live organ instead of to a reader.

#### `[#387]` P2/S — Rewrite the buy-vs-build intake before anything ingests it
- **Now:** *"intake #2 is rewritten to the ruled position or superseded by a new intake doc, before any ADR cites it"*
- **DRAFT:** *"`docs/intake/archive/2026-07-06-platform-feature-scan.md` either carries the ruled position (with an amendment marker) or a superseding intake doc exists and the old one's `status:` names it, and no `docs/decisions/ADR-*.md` cites the un-rewritten doc"*
- **Intent:** "the ruled position" cannot be verdicted, but the *form* of the correction can — an amendment marker or a supersession pointer, both of which the intake genre already defines. Leg 2 was already greppable.

#### `[#389]` P2/S — Prompt-lint: gate the five architect fields
- **Now:** *"R6 is ruled AND a seeded prompt missing a required field is refused/WARNed, with tests, OR recorded permanent-defer-with-reason"*
- **DRAFT:** *"a seeded prompt missing any one of the five ADR-87 §5 fields is refused or WARNed, with one test per field; and R6's disposition is recorded in ADR-87 or a `protocols/STANDING_RULINGS.md` section naming `[#389]`"* [Form E]
- **Intent:** "the five architect fields" becomes five test obligations, so partial coverage cannot read as done. The R6 ruling keeps its human character but gains a home.

#### `[#399]` P2/S — `v5/README.md.tmpl` phantom source claim
- **Now:** *"the claim and the mechanism agree (built, corrected, or recorded) and the `.tmpl`'s status is explicit"*
- **DRAFT:** *"`templates/handoff/v5/README.md.tmpl`'s source claim matches what `scripts/seed_runbook.py` actually does — corrected, built, or recorded in a `protocols/STANDING_RULINGS.md` section naming `[#399]` — and the template's first line states whether it is live or superseded"*
- **Intent:** unchanged; "explicit status" gains a location so a reader knows where to look.

#### `[#408]` P2/M — Auto-coupled doc updates on close
- **Now:** *"closing a backlog item mechanically surfaces or blocks on the coupled ARCHITECTURE + JOURNAL updates (built on the [#403] seed), with a test, or recorded deferred-with-reason"*
- **DRAFT:** *"a test seeds a close with no `ARCHITECTURE.md` and no `JOURNAL.md` edit and asserts the organ surfaces or blocks it, and a second test asserts a close carrying both passes clean; **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#408]` and the reason"* [Form E]
- **Intent:** unchanged. Both the positive and negative case are named so the test obligation cannot be discharged one-sided.

#### `[#413]` P2/S — Colors semantics review
- **Now:** *"the ai-council interim is reviewed on or after 2026-10-22 AND the colors semantics are re-grounded on the ruled ownership model, or the interim is re-declared with a new review date"*
- **DRAFT:** *"on or after 2026-10-22, either the colors semantics cite the ruled ownership model in `deploy/manifest-v1.4.0.yaml` (with `[#400]`'s ruling referenced), or ai-council's declaration carries a new `review_date:` later than 2026-10-22"*
- **Intent:** the date-gated review is already machine-readable through `review_date:`; the draft makes the two outcomes symmetric so neither branch is a judgment call. Does not shorten or extend the interim.

#### `[#414]` P2/S — Self-acting-on-main incident family
- **Now:** *"an architect ruling picks the organ(s) and the mechanism refuses/flags a no-GO or unanchored change to main with a test, or records permanent-defer"*
- **DRAFT:** *"a mechanism refuses or flags (a) a change to `main` with no recorded operator GO and (b) an unanchored change to `main`, with a test per case; and the organ choice is recorded in an ADR or a `protocols/STANDING_RULINGS.md` section naming `[#414]`"* [Form E]
- **Intent:** the two incident shapes become two test cases. Note the unanchored half is now partly covered by `block-unanchored-push` + `journal_spine_anchor`; the no-GO half is not, and the draft keeps them separable so partial coverage is visible.

#### `[#415]` P2/S — Tests must bind fixtures, not live mutable repo content
- **Now:** *"the sibling audit is run and each live-content-coupled test is re-pointed to a fixture or recorded justified-as-integration-smoke-test with a reason"*
- **DRAFT:** *"an audit artifact enumerates every test reading live repo content, and each enumerated test is either re-pointed to a committed fixture or listed in that artifact as an intentional integration smoke test with its reason; **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#415]` and the blanket reason"* [Form E]
- **Intent:** the enumeration *is* the deliverable, so making it an artifact makes "each" countable. Preserves the row's acceptance of legitimate smoke tests.

#### `[#418]` P2/S — `automation/fleet-audit` records 0–10 baselines a day
- **Now:** *"the multiplicity is reproduced under instrumentation AND a one-baseline-per-day contract is enforced, or the multiplicity is recorded acceptable with a reason"*
- **DRAFT:** *"an audit artifact records a reproduction of the multiplicity with the observed per-day counts, and either a check FAILs on a second baseline for the same date (with a test) **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#418]` and why the multiplicity is acceptable"* [Form E]
- **Intent:** unchanged; "reproduced under instrumentation" becomes an artifact with numbers, which is what reproduction means here.

#### `[#419]` P2/M — Routines whose output nobody consumes
- **Now:** *"every standing routine has a named consumer and a consumption path, and unconsumed output is surfaced rather than silently accumulating"*
- **DRAFT:** *"`routine_consumers` reports zero routines missing `consumer:` or `consumption_path:`, and a surfacing leg reports any routine whose consumption path holds unread output, with a test seeding an unconsumed artifact"*
- **Intent:** leg 1 is **already** verdictable by the live `routine_consumers` organ — the row simply predates naming it. Leg 2 stays a build and gains its test obligation. Nothing added.

#### `[#423]` P2/M — The integration sequence runs on prose every time
- **Now:** *"`/ship` carries the sequence with each precondition checked mechanically, not remembered, or the gap is recorded permanent-defer-with-reason"*
- **DRAFT:** *"the integration sequence's preconditions are enumerated in `plugins/tier1-lifecycle/commands/ship.md` and each is checked by `/ship` at run time with a test per precondition; **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#423]` and which preconditions stay prose"* [Form E]
- **Intent:** "each precondition" needed a roster before "each" could be counted; the command file is where the sequence already lives, so the roster costs nothing new.

#### `[#425]` P2/S — The suite is green on a format the file does not use
- **Now:** *"parser-facing test corpora are audited for input-form coverage and each gap is closed with a negative-form fixture or recorded justified"*
- **DRAFT:** *"an artifact enumerates each parser-facing test corpus against the input forms its parser accepts, and every gap is closed with a negative-form fixture or listed there as justified; **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#425]`"* [Form E]
- **Intent:** same shape as `[#415]` and deliberately so — both rows are "enumerate, then dispose"; the enumeration artifact is what makes them countable.

#### `[#428]` P2/S — `nightly-triage` reports a dead producer to every session start
- **Now:** *"no session-start surface asserts pending work from a producer that does not run, AND **the 15 open Issues** are dispositioned or the surface is retired"*
- **DRAFT:** *"no session-start surface asserts pending work from a producer with no run in the last 30 days (with a test seeding a dead producer), and the GitHub Issue backlog is either closed out or `scripts/surface_triage.ps1` no longer reads it — with the Issue count at closing time recorded in the commit"*
- **Intent:** **"the 15 open Issues" is an off-repo GitHub count that cannot be verified from this tree, and it is the same expiring-cardinality shape that made `[#241]` and `[#369]` DEFECTIVE.** The draft replaces the fixed count with a state condition and records the count as evidence instead of as a target. Leg 1 gains a liveness definition so "does not run" is decidable.

#### `[#430]` P2/M — Consumer template rejects root `conftest.py`; `fleet_parity`'s verdict depends on outside state
- **Now:** *"(a) is ruled and the root entry is admissible or declared, AND (b) a ship-gate verdict is reproducible from the subject repo's own state"*
- **DRAFT:** *"(a) the conftest ruling is cited in `ecosystem/parity-surfaces.yaml` at the affected row and the root entry passes or is a declared divergence; and (b) two `ship-gate` runs on the same subject-repo state, from different checkouts, produce the same verdict — pinned by a test that varies the surrounding state"*
- **Intent:** **leg (a) is already ruled** — the conftest ruling was confirmed and landed at `3cf3a5b0`; the draft turns the remaining obligation into recording it at the surface that reads it, not re-litigating it. Leg (b) is the row's real content and "reproducible" gains an operational definition.

#### `[#453]` P2/M — Cloud night-run runbook
- **Now:** *"a cloud-session runbook records all three gaps with their workarounds AND the unshallow + uv-pin legs are mechanized as a session preflight, or each is recorded accept-as-is with reason"*
- **DRAFT:** *"`protocols/SESSION_SETUP.md` (or a named cloud runbook) records the three container gaps with a workaround each, and a session preflight performs the unshallow and asserts the `uv` pin with a test; **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#453]` and which legs stay manual"* [Form E]
- **Intent:** unchanged; "a cloud-session runbook" gains a canonical home so it cannot land somewhere nothing reads.

#### `[#456]` P2/M — Ruling-blocked cohort sweep
- **Now:** *"every remaining row in the cohort is either re-routed, confirmed operator-owned with the reason recorded, or recorded deferred-with-reason"*
- **DRAFT:** *"the cohort is enumerated as an explicit `[#id]` list in this row, and every member is either re-routed under ADR-108 §A, listed here as operator-owned with its reason, or named in a `protocols/STANDING_RULINGS.md` section citing `[#456]`"* [Form E]
- **Intent:** **"the cohort" is defined in an external grooming dossier, not in the row** — so the row's completeness cannot be verdicted by anyone reading the row. Inlining the id list is the whole conversion. **This census re-derives that cohort:** see §6, which supplies the list.

#### `[#463]` P2/S — win-tooling onboarding debt
- **Now:** *"each of the four is fixed in win-tooling or recorded accept-with-reason, and the fleet baseline shows win-tooling green"*
- **DRAFT:** *"`python scripts/audit.py repo win-tooling` reports no FAIL and no WARN from `dot_prefix_discipline`, `canonical_freshness`, `workspace_settings` or `deployed_methodology_version`; **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#463]` and the accepted reason per item"* [Form E]
- **Intent:** **the four items map one-to-one onto four live audit checks** — `config.yaml` not dot-prefixed, VISION/ARCHITECTURE never re-reviewed, workspace sort settings absent, absent from `deployed-versions.yaml`. The draft names the command that verdicts all four at once. One of the cheapest conversions in the set (§6).

#### `[#464]` P2/S — corp-*/ai-council governance drift, five findings
- **Now:** *"each of the five is fixed in its repo or recorded accept-with-reason"*
- **DRAFT:** *"each of the five findings enumerated in this row is absent from its repo's next fleet baseline, **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#464]` and the accepted reason per finding"* [Form E]
- **Intent:** "fixed" becomes "no longer surfaces in the baseline", which is how anyone would actually check it and removes the need to re-diagnose each finding at close time.

#### `[#487]` P2/L — Closure-proposal consumption arc
- **Now:** *"(i)-(iv) land twin-in-lockstep, a ranked sheet covers the set, verdict each, and a cadence prevents re-accumulation"*
- **DRAFT:** *"(i)-(iv) as enumerated in this row land in both `scripts/propose_closures.py` and the `plugins/tier1-lifecycle` copy with a lockstep test, a ranked sheet in `docs/audits/` covers every parked proposal with a verdict per id, and a routine declaring `consumer:` + `consumption_path:` passes `routine_consumers`"*
- **Intent:** "a cadence prevents re-accumulation" is unverdictable as a prediction; the declared-routine form is the live mechanism for exactly that promise, so the draft substitutes the mechanism for the prediction. The (i)-(iv) set is unchanged.

#### `[#493]` P2/S — B-2: the scheduled fleet-baseline task has been silent 10+ days
- **Now:** *"the cause is identified with evidence, and the report names the signal that would have surfaced the silence within one cadence"*
- **DRAFT:** *"a `docs/audits/` artifact names the cause with the evidence command that demonstrates it, and names the signal that would have surfaced the silence within one cadence — with that signal either filed as a `[#id]` or landed"*
- **Intent:** an investigation's finish line is its artifact; the draft adds only that the named signal must become a row or a build, so the report cannot end at a recommendation nobody carries.

#### `[#506]` P2/M — Whole-set P10 grooming arc
- **Now:** *"a ranked evidence sheet covers the full open set with per-id last-touch and closing-merge cross-check, the architect records live / dead / awaiting-ruling for each id, and the closes land per ADR-65"*
- **DRAFT:** *"a `docs/audits/` sheet carries one row per `status: open` task with its last-touch date and closing-merge cross-check (count matching the live open count at generation time), each id carries a live / dead / awaiting-ruling verdict, and every id verdicted dead is closed per ADR-65 or named as deferred"*
- **Intent:** the row is already close to mechanical; what it lacked was a coverage assertion, and "count matches the live open count" is the check that makes "the full open set" verdictable. **This census is a partial down-payment on clause 1 and does not discharge the row** — it grades testability, not last-touch or closing-merge, and the architect's per-id verdict and the closes are both still owed.

#### `[#511]` P2/M — The 30-minute handoff cut is ~99.8% session authoring
- **Now:** *"the operator rules which load is cut and by how much, encoded in `HANDOFF_PROCESS.md` (version bump + reconciliation), and a re-measured cut records the new cost vs baseline"*
- **DRAFT:** *"`protocols/HANDOFF_PROCESS.md` carries the ruled cut with a version bump and its dependents re-stamped (`reconciled_versions` green), and one post-change handoff records measured wall-clock and token cost against the recorded baseline in its bundle"*
- **Intent:** the ruling stays the operator's; its *encoding* was already mechanical and the draft names the organ (`reconciled_versions`) that verdicts the reconciliation leg. "Re-measured cut" gains the two units it is measured in.

#### `[#513]` P2/M — Propagation completeness
- **Now:** *"a detector reports any ruled adoption present at some sites and absent at others, AND the three instances are conformant or exempted with a reason"*
- **DRAFT:** *"a detector reports any ruled adoption present at some call sites and absent at others, with a test seeding a partial adoption; and each of the three instances enumerated in this row is conformant **or** named in a `protocols/STANDING_RULINGS.md` section citing `[#513]`"* [Form E]
- **Intent:** unchanged. The three instances are body-enumerated with their exact call sites, which is why this row is convertible rather than judgment — it already did the hard part.

---

## 5. Removal-system feed — FLAGGED, not acted on

**This lane executes nothing.** No row below is closed, edited, deferred or deleted, and none is
proposed for removal on this lane's authority. Each entry is evidence plus the escape or peg it
would use, for the operator to rule on.

| Row | Flag | Evidence | Escape / peg it would use |
|---|---|---|---|
| `[#452]` | **KILL candidate** | `tasks/433-*` and `tasks/382-*` are BOTH `status: closed`; the row exists to enforce an ordering between them | Kill-with-reason: the ordering is unenforceable and unviolatable. The generalisable half already lives at `[#513]` (propagation completeness) — peg the kill note to it so nothing is lost |
| `[#170]` | **RE-PHRASE or kill** | no `tasks/168-*.md` exists in any status; the row's own body says it *absorbs* `#168` | Strike clause 2 as absorbed, or kill if the traceability-spine ADR is being carried elsewhere. Needs an author call — flagged, not chosen |
| `[#505]` clause 2 | **CLAUSE strike** | batch-1 ran 2026-08-06 and cannot re-run under a later protocol | Re-peg to the *next* batch with its operator-touch count recorded in the batch manifest. Row survives; the clause does not |
| `[#359]` | **RE-PEG** | claim moved from `HANDOFF_PROCESS.md:517-518` to `:775-776`, plus an unnamed second site at `:938-939` | Re-peg to anchor text `FILE-BOUNDARY … made mechanical` and widen scope to both sites. P1 — highest-value repair here |
| `[#360]` | **RE-PEG** | `DoD:106-109` now holds the BACKLOG advisory; the real referent is the `## Scope-freeze` section, expired 2026-07-14 and still standing | Re-peg to the heading anchor. Then the row is adjudicable and probably a fast close |
| `[#241]` | **RE-SCOPE** | "each of the 6" vs 20 live `warn-undeclared` ids | Replace the cardinality with a selector (*"every `warn-undeclared-*` entry"*). Already flagged by N-A; carried with the count re-verified |
| `[#369]` | **RE-SCOPE** | row says "doc-counts reflects 16 gates"; `doc-counts.md:15` says 17 | Replace the absolute count with a relative one (*"increases by exactly one in the landing commit, `doc_claims` green"*) |
| `[#383]` | **RE-SCOPE** | 8 rows at `:834-899` — actually 9 rows at `:910-978` | Replace location+count with the `kind: gitignore-effect` selector |
| `[#356]` | **NEEDS A HOME BEFORE IT CAN CLOSE** | its Done-when cites a *"declared-unenforced entry"* register that does not exist anywhere in the repo | Either point it at `ecosystem/silent-rule-baseline.yaml`, or rule the new register as a build with this row as its trigger |
| `[#428]` | **RE-SCOPE (watch)** | "the 15 open Issues" is an off-repo GitHub count, unverifiable from the tree and free to drift | Replace with a state condition; record the count as evidence at close time, not as a target |

**Fold candidates surfaced by the grading, not proposed:** `[#409]` / `[#410]` / `[#411]` share one
Done-when shape verbatim (*"defined as a routine (trigger, scope, consumption path) and ruled in
or out"*), one activation gate (ADR-105), and one destination organ (`routine_consumers`). They
are three rows carrying one act. `[#415]` and `[#425]` likewise share the enumerate-then-dispose
shape over adjacent test-hygiene surfaces. **Whether either set folds is the operator's call —
recorded here as an observation, not a proposal.**

**Nothing in the DEFECTIVE class is proposed for deletion.** Six of the eight are repairs, not
removals; only `[#452]` reads as a genuine kill and even that is flagged, not filed.
---

## 6. Cheapest conversions, the ruling-blocked cohort, and the strategic read

### Top 10 cheapest conversions by expected effort

Ranked by *what the conversion costs*, not by what the row costs to build. "Free" means a
textual substitution against an organ or register that already exists.

| # | Row(s) | Conversion | Why it is cheap |
|---|---|---|---|
| 1 | `[#409]` `[#410]` `[#411]` | point the Done-when at a `routine:` block verdicted by `routine_consumers` | **Three rows, one substitution.** All three carry the identical clause; `[#348]` and `[#426]` already carry the target `routine:` block, so the shape is proven in-corpus |
| 2 | `[#463]` | *"`audit.py repo win-tooling` reports no FAIL/WARN from these four checks"* | The four debt items map **one-to-one** onto four live audit checks. One command replaces four prose findings |
| 3 | `[#419]` | leg 1 → `routine_consumers` reports zero missing declarations | Leg 1 is **already verdictable today**; the row predates the organ that verdicts it |
| 4 | `[#366]` | Form E only | Leg 1 is already among the best-phrased clauses in the corpus; only the escape hatch is unhomed |
| 5 | `[#358]` | Form E only | Three sites already body-enumerated |
| 6 | `[#346]` | Form E only | Leg 1 already greppable once the file is named |
| 7 | `[#353]` | Form E + name the two seed cases | Both refusal conditions already in the clause, just unseparated |
| 8 | `[#513]` | Form E only | The three instances already carry exact call sites |
| 9 | `[#430]` | record leg (a)'s existing ruling at the surface that reads it | **Leg (a) is already ruled** (`3cf3a5b0`); only the recording is owed |
| 10 | `[#162]` | inline the row's own `refs` list into the clause | Zero new information — the surfaces are already named one line away |

**Nine of the ten cost one sentence.** Twenty-one of the 42 P1/P2 drafts in §4 are Form E and
nothing else, which is why the register decision (Q2) dominates the cost curve.

### `[#456]`'s cohort, re-derived mechanically

`[#456]` asks for a sweep over *"the ruling-blocked cohort"* — enumerated in an external
grooming dossier as **33 rows (18%)**, with three re-routed and *"the remaining ~30
untriaged"*. That definition is why the row is PROSE-CONVERTIBLE: no reader of the row can tell
who is in the cohort.

Applying a mechanical definition — the Done-when carries a ruling-shaped token in **any** leg
(`is ruled` · `a ruling` · `the operator rules` · `an architect ruling` · `is decided` ·
`ruled in or out` · `ratified`) — gives **35 rows**, against the dossier's 33. The near-match
suggests the dossier's cohort and this predicate are the same population:

```
[#153] [#170] [#210] [#317] [#323] [#327] [#329] [#331] [#338] [#341] [#342] [#343]
[#347] [#349] [#351] [#353] [#356] [#389] [#397] [#402] [#406] [#407] [#409] [#410]
[#411] [#414] [#420] [#430] [#449] [#450] [#488] [#507] [#508] [#510] [#511]
```

By this census's grading those 35 split **8 MECHANICAL · 16 PROSE-CONVERTIBLE · 10
PROSE-JUDGMENT · 1 DEFECTIVE**. The important part: **only 10 of the 35 are genuinely
ruling-blocked.** The other 25 carry a ruling token but have a mechanical or convertible
finish line beside it — the ruling gates the *work*, not the *verdict*. `[#456]`'s sweep is
therefore about a third the size the dossier's framing implies.

**This is offered as evidence for `[#456]`, not as its discharge.** The row also asks for a
per-member re-route decision under ADR-108 §A, which is adjudication and stays with the
architect.

### Strategic read: does the convertible mass change the under-100 arithmetic?

**No. Not directly, and the honest answer is worth more than a hopeful one.**

170 open, target under 100, so 71 closes are owed. Conversion produces **zero** of them. A
converted Done-when is exactly as unmet as it was before; what changes is that you can now
*tell* whether it is met. That only unblocks closes if "we can't tell" was the binding
constraint — and N-A's result says it was not: within the cohort most likely to contain
already-satisfied rows, **zero were satisfied**. The rows are open because the work is not
done, not because the finish line is fuzzy.

What this lane found on the removal side is small and is reported as small: **one genuine kill
candidate** (`[#452]`), **one possible** (`[#170]`, pending an author call), and **two fold sets**
worth at most three rows if both fold. Six to eight rows against a gap of 71. **Neither
satisfied-row harvesting (N-A) nor testability grooming (this lane) closes that gap.**

Where the convertible mass *does* change something is the question the §B amendment actually
poses. If "zero mechanically-untestable Done-when" is to become part of the finish line, the
stock standing in its way is:

| | Count | What it needs |
|---|---|---|
| Already compliant | 75 | nothing |
| Compliant after a rewrite | 72 | 42 drafted here; 30 of the 72 need only the Form E decision |
| Compliant only after a repair | 8 | six re-pegs/re-scopes, one clause strike, one kill |
| **Cannot comply without a carve-out** | **15** | the amendment must either accept a hollow existence check or exempt them |

**That is the amendment's real design question, and it is a 15-row question, not a 132-row
one.** The A5 landing predicate governs new rows and would keep the stock from growing; the
stock itself is one register decision plus 42 sentences plus eight repairs away from
compliance — with 15 rows that need the amendment to say what it does about genuine judgment.

**The number that caps close capacity is not 132 and never was.** It is 71 undone rows.

---

## 7. Cross-reference — Lane C (`batch4-prep`)

Lane C builds evidence sheets for six subjects. Those subjects are **not duplicated here**; this
census contributes only its testability verdict for each, and defers the evidence, footprint
and skeleton work to Lane C's report:

| Lane C subject | This census's verdict | Note for Lane C |
|---|---|---|
| `[#270]` (P1, + 3 dependents) | **MECHANICAL** | all three legs verdictable as written; no conversion owed |
| `[#514]` (P1, merge-queue wedge) | **MECHANICAL** | *"exactly ONE definition remains"* is grep-countable — unusually good phrasing for a P1 |
| `[#502]` (substrate question §4A) | **PROSE-CONVERTIBLE** | P3, so no draft here; blocked on `[#501]`, and the ADOPT/REJECT record needs a home |
| `kill-candidates:` refusal-check (3b-3, no row yet) | n/a — no row | but note: `kill-candidates:` has reached **117/170** open rows under add-time backpressure while `footprint:` sits at **5/170** with no enforcement. That contrast is this census's contribution to the gap |
| ARC-6 carry-forward defect (`[#310]`) | **out of scope — not an open row** | `tasks/310-*.md` is `status: deferred`, so it is outside this census. Lane C should confirm which live row carries the evidence |
| ARC-7 §6-item-3 site (`CLAUDE.md` + carrier) | n/a — no row | filed, not ticketed; nothing to grade |

Two of Lane C's own asks are answered by data here rather than by re-derivation: its
**feature-class candidate search (F24-2)** can use §2's serialize-group column (no
serialize-group is a rough proxy for non-methodology work), and its **footprint map** should
know that `footprint:` is declared on **five rows only**, so a disjointness matrix must be built
from row bodies, not from the field.

---

## 8. Batched questions

Read-only lane; nothing here blocked the work. These are the decisions the conversions wait on.

1. **Is a hollow existence check acceptable for the §B amendment?** All 15 PROSE-JUDGMENT rows
   could be made "mechanically testable" by checking that a ruling document exists. That moves
   the number without moving the testability. Either the amendment accepts the wrapper, or it
   carves out genuine adjudication. **This is the amendment's central question and this census
   cannot answer it.**
2. **Where does a "recorded with a reason" record live?** 37 open rows carry an unhomed escape
   hatch; 30 are PROSE-CONVERTIBLE for that reason alone. The drafts in §4 assume
   `protocols/STANDING_RULINGS.md`. `ecosystem/disposition-register.yaml` is unsuitable as a
   general register (its contract is one entry per suppressed audit Finding, and ADR-75's
   stale-decoration rule would fight a general use). **One decision converts 30 rows.**
3. **`[#356]` cites a register that does not exist.** Its Done-when requires a *"declared-
   unenforced entry (owner + review date)"*; nothing named that exists anywhere in the repo.
   Point it at `ecosystem/silent-rule-baseline.yaml`, or rule the new register as a build with
   this row as its trigger?
4. **`[#170]` — strike clause 2 or kill the row?** No `tasks/168-*.md` exists in any status, and
   the row's body says it *absorbs* `#168`. Needs the author's reading, not more searching.
5. **`[#505]` clause 2 — re-peg or strike?** Batch-1 cannot re-execute. Re-pegging to the next
   batch keeps the intent and makes the clause meetable; striking it accepts that the
   two-operator-touch target was never measured.
6. **Do `[#409]`/`[#410]`/`[#411]` fold?** Three rows, one verbatim Done-when, one activation
   gate, one destination organ. Folding is cheaper than converting three times — but they are
   three distinct night batches and the operator may want them tracked apart.
7. **Should `footprint:` gain add-time backpressure?** The comparison is stark:
   `kill-candidates:` reached 117/170 with a commit-msg hook behind it; `footprint:` sits at
   5/170 with nothing. If footprint declarations are load-bearing for lane decomposition (Lane
   C is building a disjointness map without them), the gap is a mechanism gap, not a
   discipline gap. **Filing this needs a row and this lane files nothing.**

---

**Contract compliance.** Read-only: zero task-file edits, zero births, zero status changes, zero
deletions, no kill executed. Grading read from `tasks/*.md` frontmatter throughout, never from
`BACKLOG.md`. No merge, no push, no `SKIP=`, no `--no-verify`. No JOURNAL entry — lane rule; the
integrator journals the batch.
