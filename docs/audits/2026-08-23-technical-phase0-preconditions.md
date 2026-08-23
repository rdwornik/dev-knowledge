# PHASE-0 PRECONDITION PACKET — 2026-08-23

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-23 · **Slug:** phase0-preconditions
- **Session:** SESSION 00 — Phase 0, primary checkout, `main` frozen to this seat, no lane dispatched
- **Branch:** `chore/phase0-preconditions-2026-08-23`
- **Governing contract:** the operator's `SESSION-00-phase0-preconditions.md` mandate
- **What this packet is:** evidence and one packet. It rules nothing, files no rows, and designs
  nothing. Every premise verdict below carries a quoted primary source or reads UNCONFIRMED.

---

## 1. The amended write-scope (Step 1)

`AMENDMENT A1` is appended to
`docs/handoffs/2026-08-23-dev-knowledge-architect/HANDOFF_BOOT.md` under a new `## Amendments`
heading — an **appended marker**, not an in-place edit of the `Destination` row. That form is
the standing one, not a choice made here: `protocols/STANDING_RULINGS.md` **J-3** ratifies it —

> **J-3 · A manifest row flip lands as an appended amendment marker** — the batch-3 precedent is
> ratified as the standard form — `docs/audits/` is immutable, so a disclosed marker is the route
> and a silent in-place row rewrite is out.

and `CLAUDE.md` §5 rule 3 puts handoffs in the same immutable class ("supersede with a new file
or an in-file amendment marker; never edit in place").

Landed at `b97bca5b`. The commit passed the full pre-commit stack, including
`check-seal-identity` (the bundle's Slug row still names its own directory) and `audit-health`.

**One defect in the amendment text, reported and NOT silently corrected.** A1 grants write-scope
over **`docs/adr/`**. That directory **does not exist** in this repo; the ADR home is
**`docs/decisions/`** (`CLAUDE.md` §2 critical paths: "`protocols/`, `docs/decisions/`,
`templates/`, `VISION.md`, `ARCHITECTURE.md`"). The text was landed verbatim as instructed. A
lane that reads A1 literally will either create an unsanctioned `docs/adr/` tree — which
`validate-hermetization` Rule A is armed to refuse — or stall. **This needs a one-line operator
correction before any lane that writes an ADR is dispatched.**

---

## 2. Ledger baseline (Step 2 — closes PK2)

### 2.1 The measured numbers

```
validate_backlog: OK (9 themes, 26 stories, 212 tasks, 1 warning(s))
  WARN  user story with no tasks — story "[S24] Declare desired state once, as data, inste" line 459

validate_git_backlog: OK — no closed-but-present drift (direction (a) STRONG, full history)

tasks/ on disk        309 files
  status: open        185
  status: deferred     27   <- open(185) + deferred(27) = the 212 validate_backlog renders
  status: closed       91
  status: retired       4
  status: superseded    1

gen_task_tree.py --check   ok   (BACKLOG.md is in sync; nothing regenerated this step)
```

The full serialize-groups line, which the architect's copy truncated:

```
validate_backlog: serialize-groups — architecture (#401, #519, #303, #305, #572, #388, #526, #420, #327, #574, #387, #440, #523, #561, #567, #358, #402, #383, #385)
audit-py (#242, #153, #349, #353, #485, #389, #424, #425, #451, #533, #552, #139, #190, #210, #234, #277, #296, #166, #335, #408, #457, #477, #418, #454, #240, #294, #297, #324, #285, #332, #343, #342, #559, #430, #470, #403, #415, #357, #361, #362, #365, #366, #448, #391, #392, #393)
claude-md (#112, #346, #577, #400, #413, #427)
code-edge (#218)
codex-review (#338, #341, #431, #445)
coherence (#181, #220, #241)
docs-gate (#571)
environment (#484, #71, #559, #453, #528, #576, #575, #570, #463, #464)
gates (#447, #510, #531)
handoff (#162, #511, #301, #344, #350, #390, #404, #422, #310, #520, #522, #359, #399)
playbook (#547, #146, #438, #443, #569, #347, #354, #356)
pre-commit-config (#345, #573, #334, #351, #369)
settings-json (#116, #117, #405, #417, #414, #442, #289, #308, #325, #329, #273, #322, #348, #419, #426, #428, #371)
```

`audit-py` is by far the largest serialize-group at **46 rows** — any batch that puts two lanes
into `scripts/audit.py` serializes them against each other. This is the ledger's own statement of
the Step-5 collision risk, arrived at independently.

### 2.2 Distribution across the whole open set

```
theme   P1   P2   P3   total
[E1]     0    7    5     12    Handoff continuity
[E2]     3   40   32     75    Enforced governance
[E3]     0    2    6      8    Lessons feedback loop
[E4]     0    5    4      9    Decision management
[E5]     1    4   10     15    Canonical-file integrity
[E6]     0    9    8     17    Cross-repo universalization
[E7]     2   32   19     53    Tooling & evaluation
[E8]     1   10    6     17    ARC-5 execution
[E9]     0    1    5      6    Fleet Desired-State (North Star)
        ---  ---  ---   ----
         7  110   95     212
```

This reconciles **exactly** with the SessionStart load line (`7 P1 / 110 P2 / 95 P3`), so the
parse is not an independent estimate that happens to agree — it is the same population.

### 2.3 The triage table

| Bucket | Count | Basis |
|---|---|---|
| **DEAD-provable** | **0** | No open row survives the bar "superseded / already-shipped, with a named closing merge sha". Three independent sweeps, all negative — section 2.4. |
| **AWAITING-RULING** | **3** explicit + 2 mandate-named | `[#347]`, `[#389]`, `[#549]` carry an explicit blocked-on-a-ruling marker in their own text. `[#171]` leg 1 and the intake-41 carrier are named by the mandate itself. |
| **LIVE** | **209** | Everything else: in progress, deferred-with-a-peg, or simply not yet started. |

**`banked = 0`.**

The three explicit AWAITING-RULING rows:

```
[#347]  open      P2 M  [E7]  Formalize the engineering loop/harness end-to-end + sanctioned safe-delete
[#389]  open      P2 S  [E2]  Prompt-lint — gate the five architect fields before a lane runs
[#549]  deferred  P2 S  [E4]  The operator-approved Fleet-Hygiene plan-of-record (intake 13 v4) has no carrier
```

### 2.4 Why zero — three sweeps, each negative

**Sweep 1 — the purpose-built organ.** `propose_closures.py` (ADR-70 Tier-1) produced
`logs/PROPOSALS-2026-08-23.md`. The SessionStart line advertises "181 closure(s) proposed". The
split is **2 STRONG / 179 WEAK**. WEAK is inference and the file itself forbids bulk-approving it:

> **Confirm one:** type its `#N`; ignore the rest. No bulk-approve
> (precision guard — these are inferences, not declarations).

Both **STRONG** hits were verified against their evidence SHAs, per the standing discipline of
re-reading closure content before acting. **Both fail:**

- **`#430`** — evidence `3cf3a5b0b`. Its body reads `Closes [#430] half (a) and clears the
  standing RED`. **Half (a) only.** Half (b) — `fleet_parity` reading LIVE sibling-repo state, so
  a concurrent merge elsewhere reddens this repo's ship-gate with no action available here — is
  untouched. A partial closure, not a closure.
- **`#554`** — evidence `6c9369298`, subject `fix(devcontainer): terra review round 1 — all five
  HIGH findings closed [#554]`. The row is **not** closed by it; the same commit's own trailer
  says so explicitly: `kill-candidates: none — review fixes inside the open row [#554]`.

**This is a reportable defect in the STRONG tier, not just two unlucky rows.** The detector is

```python
CLOSES_RE = re.compile(r"\b(?:closes?|closed|fixes?|fixed)\s+\[#(\d+)\]", re.I)
```

which matches a **verb-adjacent token**, not a **declaration**. In `#554` the word `closed` is a
past participle modifying *findings* — "five HIGH findings closed [#554]" — and the regex cannot
tell that apart from the directive form `closes [#554]`. In `#430` the regex cannot see the
`half (a)` qualifier that immediately follows. `strip_quoted_contexts` already defends the
quoted-prose false positive ([#437]); **neither of these two is quoted**, so that guard does not
reach them. STRONG's advertised precision ("a commit message in the window says `closes [#N]`")
is therefore weaker in practice than the docstring claims: today it is **0-for-2**.

**Sweep 2 — terminal markers in the task bodies.** All 212 open/deferred bodies were scanned for
`SUPERSEDED` / `ABSORBED BY|INTO` / `FOLDED INTO` / a close-verb followed by a SHA / `OBSOLETE|MOOT`.
**18 rows matched; none is dead.** Every match is one of three innocent shapes: the row is the
**absorber** (`[#285]` "absorbs #67 #18 #27 #39 #217 #219 ... folded into this re-read";
`[#411]`, `[#412]` fold *in from* `[#348]`); the word sits inside a **Done-when condition** the
row has not yet met (`[#549]`, `[#551]`, `[#561]`, `[#564]`, `[#399]`, `[#362]`); or it is prose
about a *different* id (`[#244]` mentions "#221 closed at 8aab4356").

The closest single candidate, `[#43]`, is explicitly held open **by its own text**:

> 2026-07-08: scaffold scope folded into `docs/intake/2026-07-08-func-new-project-bootstrap.md`
> (intake-id 6) — superseded-by that intake, now the requirements spine for this work; **this task
> persists as the decomposition target the technical triage will decompose**

Superseded in *scope*, deliberately alive as a *carrier*. And `[#117]` states the same pattern as
doctrine: "Same treatment ARC-2 gave `[#293]` and `[#298]` when their pegs were met: **un-defer,
do not close** — the work itself is untouched."

**Sweep 3 — the spine.** Every open/deferred id was cross-checked against all **1553**
first-parent commit subjects on `main`. **120 of the 212 appear in at least one spine subject** —
which is a measure of *activity*, not of completion: this ledger's convention is that a row
accumulates progress commits across many windows and is removed only by an explicit `closes`.
`validate_git_backlog` independently confirms the opposite direction is clean (no closed-but-present
drift, direction (a) STRONG, full history), so the ledger is not leaking in either direction — it
simply contains no mechanically-provable corpses.

### 2.5 What this means for the batch

The mandate's premise was that a mechanical sweep would bank enough closures to make new rows
affordable. **It does not.** `banked = 0` is not a failure of the sweep — it is the finding: this
ledger has already been groomed to the point where **every remaining row carries a judgment
component**. Grooming 212 is an arc, as the mandate anticipated, and no mechanical shortcut into
it exists. The affordability question for births therefore returns to the architect **unchanged
and unassisted by this step**, which is the honest result.

### 2.6 One structural finding, filed not fixed

`validate_backlog` emits exactly one WARN: story **`[S24]` "Declare desired state once, as data,
instead of..."** has **no tasks**. An empty story is a story-map defect (it renders a heading with
nothing under it). This is left untouched — the mandate forbids filing rows and this session
rules nothing.
