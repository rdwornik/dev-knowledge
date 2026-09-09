---
intake-id: 89
status: DRAFT
origin: browser seat (Fable), closing ruling of window 2026-09-08-dev-knowledge-architect-2, 2026-09-09 — `DECLARE-RECOVERY-2026-09-09.md` on the transport; filed into the repo by batch V lane `lane-v-000-window-rulings`
consumed-by:
---

# The recovery plan — four files, one map, one conductor; delete without fear, git has it

<!-- class: tech (corpus structure + the mechanisms that keep it true) · status: DRAFT — the
DECLARE is a browser-seat plan carrying the operator's stated want ("simplify the whole system
starting from ARCHITECTURE"); it is NOT an operator ratification of this plan's shape, and this
doc does not claim one. Non-citable as doctrine until it is ruled. The repo wins on any conflict.
Genre note (ADR-98 §3): the source DECLARE is plan-shaped. What is WHAT/WHY is carried in the
canonical sections; the declared sequence and delete list are carried verbatim-in-substance under
"The plan as declared", which is a RECORD of the source, not a specification this doc invents. -->

## Problem / motivation

`ARCHITECTURE.md` and `protocols/PLAYBOOK.md` are the two files a fresh seat is supposed to be
able to read to know this system, and neither currently does that job. The measured inputs the
window ran on: **30% doc congruence**, a **246-line review prologue** standing between a reader
and `ARCHITECTURE.md`'s first fact, **PLAYBOOK Ch8 at 163 KB**, a **160 / 24 / 32** process
census (triggered processes / … / orphans), and **8 of 16 loop stages mechanical**. The operator's
word closing the window was to simplify the whole system starting from `ARCHITECTURE.md`, on a
two-file split: `ARCHITECTURE.md` technical, `PLAYBOOK.md` functional.

`protocols/ESSENTIALS.md` is the third file in that space and it is unexplained — de-blessed on
2026-09-01, `status: superseded`, routing nobody, and still present. It has been re-asked three
times and is still not finished.

What happens if this stays unaddressed is already observable: "list all processes" is answered by
re-reading the repo rather than by asking anything; a seat that pastes `ARCHITECTURE.md` into a
fresh window does not come out knowing what fires at commit; and every doc-vs-repo divergence is
found by a reader tripping over it rather than by a gate.

## Scenarios (+1 view)

- **As a fresh architect seat**, I am handed `ARCHITECTURE.md` and nothing else, and I answer ten
  questions about this system from it — what fires at commit, what fires at push, what fires at
  session start and stop, what the operator triggers, which module owns stage N of the delivery
  loop, what reads and writes file X, which repos are consumers, where the dispatch verb lives,
  which organs are orphans, and what changed since the last cut. I answer none of them with
  "grep the repo". Today I would answer most of them that way.

- **As the operator**, I read `PLAYBOOK.md` chapter by chapter in one sitting and rule keep / cut
  / merge on each, from a map that already tells me what each chapter is for, whether it is live,
  dead or duplicated, and which modules implement it. Today no such map exists, and the file is
  500 KB, so the sitting cannot happen.

- **As a lane**, I change a file and a commit-tier query refuses because no OPEN task claims it —
  "nothing deploys without a task", enforced at OPEN and not only at close. Today the coupling is
  checked at close, which is the one moment it cannot prevent anything.

- **As a reader of `ARCHITECTURE.md` Ch2**, I read a rendered table rather than a hand-maintained
  one, and prose naming a process the graph does not hold is a `dangling_reference` rather than a
  sentence nobody re-read.

- **As the operator asking for the fourth time**, I get `ESSENTIALS.md` finished rather than
  re-explained: its consumers re-pointed and the file gone, as one release act.

## Functional requirements

- **Must:**
  - `ARCHITECTURE.md` becomes the technical map and nothing else: one graph diagram, one
    module / trigger / reads / writes / stage table, Purpose, layers, governing ADRs — **≤ 15 KB**,
    with the table rendered from the spine graph and only three hand-written sections.
  - `PLAYBOOK.md` becomes the process, functionally, by chapter, in plain language, every chapter
    naming the modules that implement it — hand-written, and congruence-checked against
    `ARCHITECTURE.md`.
  - `CLAUDE.md` becomes the agent contract — identity, rules, anti-patterns hand-authored; the
    command / skill / hook lists **generated**, the way §9's roster already is.
  - `protocols/ESSENTIALS.md` ceases to exist, after its consumer routes are re-pointed. It is a
    prose copy of what mechanisms already enforce.
  - The paste test of section 0 is run as an **eval**, scored per cut and kept by a freshness hook —
    not read as a slogan.
  - What keeps all of the above true is **mechanism, not discipline**: the spine graph, the
    commit-tier queries, the renders behind freshness hooks, and the conductor (see
    "The plan as declared" §3).
- **Should:**
  - PLAYBOOK Ch8's dispatch and batch manual moves to its own file (`protocols/DISPATCH.md`), and
    Ch8 keeps session boundaries only.
  - Generated blocks a reader never needs (Codemap, TOC) move to `.claude/generated/`, where the
    hooks keep reading them and readers stop paying for them.
- **Could:**
  - `ecosystem/` north-star and every other generated artifact no process reads is decided **by
    the census** — no inbound `reads` edge means delete. A query, not a judgment call.

## Acceptance criteria (ex-ante)

These are the test as it would actually be run, and they are the epic's UAT verbatim.

1. **The paste test, ARCHITECTURE.** A fresh seat is given `ARCHITECTURE.md` and no other file and
   answers the ten questions of §0 below. Score = questions answered from the file alone. Any
   question answered by "grep the repo" scores zero for that question. The score is recorded per
   cut and the freshness hook keeps it.
2. **The paste test, PLAYBOOK.** The same shape, ten process questions, same scoring.
3. **`ARCHITECTURE.md` ≤ 15 KB**, measured in bytes, gated.
4. **Doc congruence 34/113 → 113/113** on the `doc_congruence` query.
5. **`orphan_census` reaches 0** against its stated node class after dispositions, and it REFUSES
   at commit tier rather than reporting.
6. **`task_coverage` reports 0 FAIL on the merged tree**, and it refuses at commit tier on a file
   changed with no inbound `implements` edge from an **OPEN** task.
7. **`process_list` answers "all processes"** as a traversal, `ARCHITECTURE.md` Ch2 is rendered
   from it behind a freshness hook, and prose naming a process the graph lacks is a
   `dangling_reference`.
8. **`protocols/ESSENTIALS.md` does not exist**, its consumer references are re-pointed or removed
   in the same release act, and the floor sha and `deploy/release_lint.py` C5 agree afterwards.
9. **The conductor's transitions fire**: intake ACCEPTED → row filed; row + contract → dispatched;
   merged → docs rendered, telemetry written, closure proposed; ratified → row archived. The
   operator's five decisions are the only manual transitions.

## Non-goals

- **Not a content rewrite of the governance record.** ADRs, audits, handoffs and `JOURNAL.md` are
  untouched; git and `JOURNAL.md` hold every byte the delete list removes, which is the whole
  reason the delete list is safe.
- **Not a new registry file.** The registry is a **query over the graph**; a YAML or markdown copy
  of the graph is explicitly disqualifying (`DECLARE-SPINE-2026-09-09` §2, and `[#664]`).
- **Not an autonomy change.** No new decision moves from the operator to a mechanism; the
  conductor automates transitions that are already mechanical and leaves the operator's five
  decisions manual.
- **Not the deploy freeze decision.** Step G waits on `[#644]` and does not pre-empt it.
- **Not this doc's job to rule its own plan.** The sequence below is recorded, not ratified.

## Impact sketch (4+1 lite)

- **Logical:** the corpus becomes a graph with rendered views over it, rather than a set of files
  that each parse their own edges. Thirteen private answers to "what cites what" collapse to one.
- **Process:** the operator's chapter-by-chapter sitting (step B) becomes possible because step A
  produces the map it needs; the delivery loop gains a conductor, so transitions stop being a seat
  remembering to do them.
- **Development:** `ARCHITECTURE.md` Ch2 and `CLAUDE.md` §7–§9 stop being hand-maintained and
  start being generated; three hand sections survive in `ARCHITECTURE.md`. The docs-rewrite lane
  cannot start before the graph exists, because it renders from it.
- **Physical:** step A runs on Gemini (`agy`) read-only because 500 KB is a reader's job; step E
  runs on Codespaces because it is read-only compute; steps C, D, F and G are local lanes because
  they commit.

## Open questions

- **Is this plan ratified?** It is not. The DECLARE is the browser seat's closing plan for the
  window and carries the operator's stated want; the operator has not ruled the plan's shape. Who
  rules it, and when, is open. This doc stays DRAFT until then.
- ~~**The `ESSENTIALS.md` consumer count.**~~ **RULED 2026-09-09 (operator, relayed by the batch V
  integrator) and no longer open:** the disposition is **DELETE after re-point**, and the count is
  whatever the re-measurement gives. The "52" was REVIEW carry 4's figure and **yields to the
  measurement**; `[#628]` owns it and carries the measured number (amended by this lane). No
  second row, and the deletion itself is step D's fleet-coupled release act.
- **Which node class `orphan_census` reaches.** The census counts 32 orphans (20 script-class,
  3 hooks, 9 commands/skills) and the query as worded reaches the 20. Whether the remaining 12 get
  a widened node class or their own queries is `[#664]`'s call to record, not to drop.
- **`ecosystem/` north-star and the "no inbound `reads` edge = delete" rule.** The rule is stated
  as "not a judgment; a query" — but no one has yet confirmed the query's false-positive rate on
  artifacts a human reads directly and no process does.
- **What the eval's passing bar is.** "Ten of ten" is the obvious bar and is not stated. A score
  recorded per cut with no bar is telemetry, not a gate — the shape this plan exists to end.
- **Where the paste-test scores live** so the freshness hook can keep them.

## The plan as declared

> A record of `DECLARE-RECOVERY-2026-09-09.md`'s own sections, kept here so the plan is `git log`-able.
> This section is the SOURCE's content; it is not this doc inventing a specification.

### §0 · The ten questions the paste test asks

What fires at commit · what fires at push · what fires at session start/stop · what the operator
triggers · which module owns stage N of the loop · what reads/writes file X · which repos are
consumers · where the dispatch verb lives · which organs are orphans · what changed since last cut.

### §1 · The four-file target

| File | Is | Written by |
|---|---|---|
| `ARCHITECTURE.md` | the technical map: one graph diagram · one module/trigger/reads/writes/stage table · Purpose · layers · governing ADRs. **≤ 15 KB.** | rendered from the spine graph; three hand sections only |
| `PLAYBOOK.md` | the process, functionally, by chapter, plain language, every chapter naming the modules that implement it | hand-written, congruence-checked against ARCHITECTURE |
| `CLAUDE.md` | the agent contract: identity · rules · anti-patterns; command/skill/hook lists **generated** | hand rules; §7–§9 rendered like §9's roster already is |
| `ESSENTIALS.md` | **does not exist.** A prose copy of what mechanisms enforce. De-bless finishes: consumer routes re-pointed, then deleted. | — |

### §2 · The delete list (git and `JOURNAL.md` hold every byte)

- **ARCHITECTURE:** the 246-line review prologue → one `JOURNAL.md` entry naming the last SHA;
  Codemap and TOC blocks → `.claude/generated/` (hooks keep them; readers never see them); the
  47 KB organ-map and validators hand tables → replaced by the render.
- **PLAYBOOK:** Ch8's 163 KB dispatch/batch manual → `protocols/DISPATCH.md`, Ch8 keeps session
  boundaries; "review pass" / "living document" / intro prose that describes the file instead of
  the process → out; duplicated doctrine that Ch1 already refuses to restate → out everywhere
  Ch1's rule is violated.
- **`ESSENTIALS.md`** → deleted after re-point. The DECLARE names two sites as the live routes
  still outside the landed fix; both were re-measured by this lane and neither is a route today
  (see `[#628]`'s amendment).
- **The four retired-on-disk orphans** (3 SUPERSEDED hook copies, `/override`) → deleted; the
  operator's act.
- **`ecosystem/` north-star and any generated artifact no process reads** → the census decides:
  no inbound `reads` edge = delete. Not a judgment; a query.

### §3 · What keeps it true — mechanisms, not discipline

1. **Spine graph** — nodes and edges, rebuilt per commit, persisted. Filed as `[#664]`.
2. **Four queries at commit tier:** `orphan_census` · `task_coverage` (nothing without an open
   row, at OPEN) · `process_list` · `doc_congruence` (34/113 → 113/113).
3. **Renders with freshness hooks:** `ARCHITECTURE.md` Ch2 · `CLAUDE.md` §7–§9 · the paste-test
   scores.
4. **Conductor** — a state machine over rows: intake ACCEPTED → row filed; row + contract →
   dispatched; merged → docs rendered, telemetry written, closure proposed; ratified → row
   archived (`archive_row_body` gets its trigger here). The operator's five decisions are the only
   manual transitions.

### §4 · Sequence and substrate

| Step | What | Substrate | Why there | Row |
|---|---|---|---|---|
| A | Chapter map of `PLAYBOOK.md` (500 KB): per chapter — purpose · live/dead/duplicated · modules named · keep/merge/cut recommendation. Same for `ARCHITECTURE.md`. | Gemini (`agy`), read-only; CC verifies every locator before it is trusted | 500 KB is a reader's job, not the browser's | `[#665]` |
| B | Operator rules keep/cut per chapter from the map — one sitting, one file | operator + browser | functional call | `[#666]` |
| C | Spine lane | local lane | commits | **`[#664]`** (already filed) |
| D | Docs rewrite lane: ARCHITECTURE render + PLAYBOOK by chapter + `DISPATCH.md` split + `CLAUDE.md` generated lists + ESSENTIALS re-point and delete | local lane, after C | needs the graph to render from | `[#667]` |
| E | Paste-test eval run on the rewritten files; scores recorded | Codespaces | read-only compute | `[#668]` |
| F | Conductor lane | local lane | commits | `[#669]` |
| G | Stage 10: floor v1.5.0 to `corp-monorepo` — after the operator rules the 2026-08-29 freeze | local lane | the only step that reaches the operator's day | `[#670]` |

**The DECLARE's spine-row id is wrong and the error is recorded rather than repeated.** §3.1 and
§4 step C name the spine row `[#644]`. `[#644]` is a different live row — "the 2026-08-29 deploy
freeze has never been ruled" (`[E6]`/`[S15]`, filed by lane V-4). The DECLARE predicted an id that
V-4's filings consumed in between. **Every row that means the spine cites `[#664]`.** Step G is
the one step that genuinely cites `[#644]`, and it cites it as its blocker.

### §5 · The operator's four standing asks — true status as declared

| Ask | Since | Status |
|---|---|---|
| `logs/` litter | 4 sessions | **swept** (154 moved to `logs/2026-09/`, gitignored, inert); the source fix rides the spine row as a `writes` edge |
| ESSENTIALS de-bless | 2026-09-01, re-asked ×3 | **NOT done**; D9 cut from batch V; two named sites plus a large consumer set; step D finishes it |
| tasks at open / archived at close | 3 sessions | at close only; archiver orphan; `task_coverage` (step C) + conductor (step F) |
| telemetry used | 3 sessions | emitted, not consumed; the conductor's "merged → telemetry written" leg (step F) |

## Status

**DRAFT** — filed into the repo 2026-09-09 by batch V lane `lane-v-000-window-rulings` from
`DECLARE-RECOVERY-2026-09-09.md`, so the window's plan is `git log`-able rather than transport-only.
It carries the operator's stated want and the browser seat's plan for it; the operator has not
ruled the plan's shape, so this doc claims no ratification and binds nothing. Its steps are filed
as `[#665]`–`[#670]` under `[E2]`/`[S3]`, with step C already filed as `[#664]`.
