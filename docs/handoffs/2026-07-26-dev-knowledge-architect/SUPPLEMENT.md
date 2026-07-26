# Architect strategic supplement — 2026-07-26-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-26

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the
   repo.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

=== ANSWERS ===

1. STRATEGIC INTENT (way-of-working, not task)
Make SELECTION and CLOSURE mechanical instead of remembered — unchanged from intake #17,
now with its root cause named: BACKLOG.md is not too big, it is the WRONG DATA STRUCTURE.
One file serves five workloads (work queue, dependency graph, archive, decision register,
evidence store). Every defect of this window maps to that: the 1200-char ceiling blocks
records because EVIDENCE does not belong in a queue row; the [E8] R-table rotted because
DECISIONS do not belong in a queue file; nothing is ever deleted because closing means
editing a 170KB file; id collisions because the counter is prose, not a directory.
The next arc is the MAIN ARC from intake #17 — the backlog restructure — and its goal is
to split by workload, not to compress.
Second, generalized rule for the whole loop: every stage is a folder of frontmattered .md
files, and every EDGE of the loop is a TYPED FIELD, not prose (intake_id -> from_intake ->
from_adr -> verified_by -> route_to). ADR-105's "a routine must name its consumer"
generalizes: every artifact names its consumption edge, and orphanhood becomes computable.
Falsifiable exit test, unchanged: a fresh session boots and its FIRST message quotes the
top-5 ready-set with rationales plus every ruling overdue >8 days, zero operator memory.

2. TENSIONS WEIGHED — and where they landed
(a) Nightly routine: PAUSE vs KEEP. Landed KEEP the producer, FIX the false announcement,
BUILD the consumer. The architect first recommended pausing and REVERSED on the operator's
challenge: the digest is cheap and re-derivable, so the daily damage is not the branch —
it is SessionStart announcing 15 findings from a producer dead since 2026-07-09. The real
answer is the morning loop, which is the missing audit->intake edge and the missing PM
surface. Building it retroactively legitimizes all ~30 currently-consumerless routines and
turns [#426] from a 30-item retrofit into one field per routine.
(b) uv: APPROVED by the operator as a fleet decision NOW, ahead of the restructure. It
kills methodology-intake classes A (environment/test isolation) and E (gate reproducibility)
at the root: `uv run` cannot execute in a foreign environment, and `uv sync --locked` makes
a stale lockfile fail the build instead of being silently rewritten. The ai-council
conftest.py import guard stays as the second leg, not the only one.
(c) Adopt vs build-thin: REOPENED as a THREE-WAY bake-off, not decided. Backlog.md
(mature; acceptance criteria, DoD, milestones, dependencies, search over tasks/docs/
decisions, MCP; TypeScript) vs scrummd (Python, GPL-3.0, cards as .md with frontmatter,
[[wiki-link]] dependencies, console board — our validators could IMPORT it rather than
parse alongside; ~15 stars, single author) vs build-thin. Frozen criteria: [#N] preserved
exactly, frontmatter extensible with serialize-group / verified_by / Fibonacci scoring,
dependency graph, Windows, agent integration, maintenance risk, license. The restructure
ADR decides ON PILOT EVIDENCE. Intake #17's named flip condition still governs: name the
trade explicitly, never split the difference silently.
(d) Terraform (operator asked): PATTERN yes, TOOL no. The declare-desired-state / diff /
plan / gated-apply pattern IS [#382] desired-state data model, now unblocked as head of
the [E9] chain. The tool is refused because GIT is our state store — diff is plan, gated
merge is apply, fleet_parity is drift detection, copier/cruft is apply for templates.
Terraform would duplicate git with a worse tool and its own state file. Parking lot only:
the GitHub provider, if repo settings are ever managed as code (moot — no CI exists).
(e) Distiller: DETERMINISTIC extraction, not LLM summarization. repomix (--compress via
Tree-sitter, git-aware, token counts, MCP) as session input; bounded one-question probes
returning verbatim quote + file:line as verification. The PERMANENT distiller for the
backlog is the restructure itself — per-task files are queried, not read.
(f) LLM role in the migration: PROPOSE-ONLY. Gemini long-context (or grok shadow) receives
each body >233 chars and proposes a three-way split (stays <=233 / relocate as evidence
link / dead candidate), each with a quote; a deterministic verifier confirms the quoted
text exists; the operator ratifies in batches. This is intake #17 §2's propose-only
doctrine applied to migration — the LLM does what grep structurally cannot (semantic
classification) and cannot break anything.
(g) Genre lifecycle: named as the restructure's SECOND LEG. The operator's complaint
"ADRs rot, nothing is archived" is not a backlog problem — it is a missing lifecycle
engine. One schema for every genre: status in frontmatter <-> folder, a validator FAILs
the mismatch, a command moves the file. This mechanizes the 2026-07-22
archive-inside-each-folder ruling, which is correct but manual and therefore never runs.
pyadr covers the ADR transitions (proposal/accepted/rejected/deprecated/superseded) off
the shelf. Per-task files WITHOUT this leg would be the same rot in smaller packages.

3. CONSIDERED + REJECTED — do not relitigate
Backlog libraries, all five verified live 2026-07-26 (four fetched; BacklogPy from its own
docs, flagged as such):
- pypi `backlog` — "A Glorified TODO list", last release 2020-03-23. Personal todo. NO.
- rebacklogs — Rails + PostgreSQL + docker-compose server app; data in a DB, not in git,
  so neither our validators nor agents can read it. NO.
- github-backlog-generator — AI tool generating milestones/epics/tasks INTO GitHub Issues;
  single release 2025-07. Wrong direction: our .github/ is deleted. NO.
- BacklogPy — API client for Nulab's commercial "Backlog" SaaS. Not a tracker; a live
  example of the name-collision hazard in methodology-intake section H. NO.
- scrummd — NOT rejected; promoted to the three-way pilot (2c).
Calibration recorded so it is not re-learned: PyPI "Verified details" verifies maintainer
identity, not quality — `backlog` carries the "Production/Stable" classifier and is dead.
Also rejected/settled: Terraform as a tool (2d) · pausing the nightly producer (2a) ·
big-bang migration · six-state PLAN.md lifecycle · a managed id-counter file (the
directory is the counter) · product-form scoring · weekly full re-scoring · Backlog.md as
ENGINE-by-assumption (it must win the bake-off on evidence, not by default) · relitigating
ADR-104 or ADR-105's activation gate.

4. OPEN QUESTIONS — unresolved or deliberately deferred
- Which of the three backlog options wins. Pilot decides; nobody decides in chat.
- Is scrummd's GPL-3.0 + single-author bus factor acceptable for an imported dependency?
  (Internal use under GPL is fine and the project is small enough to fork — but it is a
  real risk to name in the ADR, not to wave away.)
- R-G: which Gemini CLI is the scanning lane (blocks every Gemini job, incl. 2f).
- R-N: confirm 8 days as the overdue-ruling threshold. R-S: the seeded-defect set for grok.
- [#431]: needs a core-invariant #6 ruling — the codex wrapper is global infra, operator-owned.
- registry.md 8->9 fleet count (hand-maintained; needs purpose + verified status per repo).
- R8: the corp #38 channel pick — operator's alone, never delegated.
- CODEMAP SCOPE, asked twice and still unanswered: widen --source-root so the artifact maps
  more than two packages, or stop calling it canonical. By this repo's own "no organ =
  decoration" doctrine it cannot stay as is.
- NO CI EXISTS. Nothing runs the suite or the clean-room leg except a human on one machine.
  This is a precondition of the morning-loop wave, not a detail.

5. DECOMPOSITION RATIONALE — and what NOT to redo
Wave order, each a separate merged arc (one wave = one arc; the six-lane packing was
already ruled a defect):
  1. MICRO-WINDOW (~1h, prompt already delivered, awaiting paste) — ARCHITECTURE currency,
     the reserved-id line, three merged branches, the R1-R12 liveness sweep, the
     codex-wrapper filing. Pure implementation, zero rulings.
  2. uv adoption (approved) — smallest arc that removes a whole defect class fleet-wide.
  3. MAIN ARC: the restructure, TWO LEGS — (a) per-task split via the strangler sequence
     (verbatim split -> byte-stable round-trip -> source-of-truth flip -> prose relocation),
     (b) the genre lifecycle engine (2g). The bake-off (2c) is its first step; the
     propose-only migration lane (2f) is its middle.
  4. MORNING LOOP — the audit->intake edge, one surface, findings routed, the false
     announcement fixed. Requires (3) to have somewhere to route findings.
  5. A-J methodology-intake decomposition, AFTER (3), with its dedupe map: I.1=[#421],
     I.2=[#422], D=[#427], B=[#423] plus the still-unfiled #121 hub twin, A partially
     [#429]. Filing a dozen tickets into an unmaintainable file first would repeat the
     mistake, and ARC-5's closure contract demands net accretion <= 0.
  [E8] ARC-5 waves resume with the tool in hand; W1 carries a 2026-08-13 deadline.
MUST NOT be redone or re-decided: intake #17's D1-D6 · the strangler sequence · the four
PLAN.md states · the scoring form (sum over one Fibonacci scale, unblock_count separate,
event-driven re-scoring, sticky override) · verified_by as required · ADR-104 · ADR-105's
activation gate (a routine may not ACTIVATE without a named consumer; FILING a proposal
without one is explicitly legal) · the five library rejections (3) · Terraform-as-tool.

6. OFF-REPO CONTEXT
OPERATOR'S FRAMING, his words, treat as design input: the architect "can build but cannot
delete or manage" and needs a TOOL that manages for it; almost everything we build already
exists as a library or a GitHub project, and the job is to COMBINE and optimize with LLMs
rather than rebuild. He also reversed the architect's priority: deployment/onboarding of
further repos was the WRONG next step while the methodology itself is unmaintainable.
METHOD RULES NOW BINDING ON THE ARCHITECT SEAT, each paid for this window:
- No claim about repo state without file:line evidence from a deterministic read. Every
  correct finding this window came from a script; every error came from prose read in long
  context. The architect claimed a file was "read" from a chat preview without opening it
  on disk — do not repeat.
- Where an [E8] R-row already carried a ruling, the architect's recommendation CONTRADICTED
  it 3 times out of 3. Never present a decision table to the operator without a per-row
  liveness check first.
- BINDING RULINGS ALSO LIVE IN docs/handoffs/. A ruling-existence probe that searches only
  JOURNAL and LESSONS is unsound — this nearly reversed the binding Pyrefly-universal
  ruling (SUPPLEMENT.md:113/:119, 2026-07-20).
- Line-anchored citations rot inside their own branch; cite by anchor text, not line number.
- Producer != reviewer, hard: terra passed the R1b diff clean, sol caught it.
- Session boot reconciles against [E8] ARC-5 AND intake #17 BEFORE touching the handoff's
  named topic. Three consecutive windows drifted by planning from the topic instead.
- Findings discovered during a close are RECORDED, not chased.
- Load-bearing artifacts travel as FILE UPLOADS, never chat paste — transport corrupted
  several pastes this window, including CC's own reports.
- ONE CC prompt per turn, destination as the first line inside the block; not every turn
  needs a block at all.
WORKTREE, generalized: half the pain was environmental (interpreter/venv/editable leak) and
uv removes it entirely; the remaining half is git-shaped (single writer on the primary,
base-ref when local main is ahead, session attribution) and must be WRITTEN, not remembered.
Option worth costing in the ADR: satellites may use full clones per lane instead of
worktrees — disk is cheap and the whole shared-HEAD/index class disappears.
CARRIED DEBT, enumerated not silent: registry.md 8->9 · five stale R-status cross-references
· one merged branch awaiting the operator's word to delete · the #121 hub twin unfiled.

=== 7. AMENDMENT — the accumulating conformance branches (operator-raised) ===

THE CONDITION. The nightly conformance Routine still writes claude/conformance-YYYY-MM-DD
branches nightly. The triage Action that consumed them required .github/, retired
2026-07-08. Since then the branches accumulate unread, SessionStart still announces stale
nightly findings, and 15 GitHub Issues sit open from before the retirement. The operator
has been ignoring the noise for weeks. Verify the live branch set and its span before
acting — do not assume the count; the census saw six, the true span since 2026-07-08 may
be larger.

RULING 1 — DO NOT MERGE. ADR-84 forbids it by design: unattended writers commit only to
their own automation/* or claude/* branches and are NEVER merged into main; the digest IS
the record, on its branch. Merging would break writer isolation, which is the whole point
of the channel. The operator's instinct to merge is understood and explicitly overruled
here so it is not revisited.

RULING 2 — DO NOT BULK-DELETE YET. These branches are the only surviving record of every
nightly run since the Action died, and they are the evidence base for a decision we have
not made: whether this Routine earns a consumer at all. Delete only after extraction.

THE EXTRACTION PASS (one bounded arc, read-only, before the morning-loop wave):
Aggregate every digest deterministically — one row per night: date, findings claimed,
findings that name a real defect, findings already fixed since, false positives. Read-only
fan-out is appropriate here (luna/Haiku, one branch per probe, verbatim quote + file:line);
the aggregation itself is a script, not a judgement.
THE NAMED TEST, and it is sharp: throughout this window ARCHITECTURE.md asserted "ratified
through ADR-103" while ADR-104 and ADR-105 existed and bound; the organ map listed 31
checks while a 32nd was live; Ch6 described a nightly loop whose own Action was dead. That
is precisely the claims-vs-docs class this Routine exists to catch. DID ANY NIGHTLY DIGEST
FLAG ANY OF THEM? Answer that first — it decides everything below.

THE VERDICT FORK, pre-registered so the answer cannot be rationalized after the fact
(ADR-74's adoption rubric with kill criteria, applied to an organ we already run):
- Digests DID surface real, actionable findings -> the producer works and was merely
  unconsumed. It earns a named slot in the morning loop, and [#428] narrows to rebuilding
  the consumer edge.
- Digests surfaced nothing, or nothing beyond noise, across the whole span -> the producer
  is not broken-by-accident, it is mis-scoped. RESHAPE (narrow its checks to classes it can
  actually detect) or RETIRE. Wiring the morning loop to it would be [#419] with a schedule
  attached — a consumer reading noise.
Either way the result is a ruling recorded in the same window, not a chat conclusion.

AFTER EXTRACTION. Archive the aggregate as the durable record (one dated artifact), then
delete the branches — deletion is the operator's call per standing rule, requested once for
the whole set rather than per branch. Do not delete before the aggregate is committed.

THE 15 OPEN ISSUES are the same class and travel with this arc: disposition each (real /
obsolete / already fixed) or retire the surface that announces them. A count announced at
every session start from a producer that no longer runs is the exact defect [#428] names.

SEQUENCING. This arc runs BEFORE the morning-loop wave and AFTER the restructure, because
its verdict decides what the morning loop is allowed to consume. It does not run before the
micro-window and it is not folded into the restructure — one wave, one arc.

WHY THIS IS NOT JUST CLEANUP. This is the first empirical measurement of a Tier-3 organ
that has been running unattended for weeks with no consumer. ADR-105 says a routine may not
activate without a named consumer; this Routine predates that rule and has been grandfathered
by inertia. The extraction pass is how it gets judged by the rule everything else now obeys.
