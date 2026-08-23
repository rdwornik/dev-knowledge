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

---

## 3. Ship-gate (Step 3 — closes PK3)

Run in **git-bash**, not PowerShell, per the known PowerShell false-RED on `handoff_probes`.

### 3.1 Verdict and arithmetic

```
$ python scripts/audit.py ship-gate       # git-bash, PYTHONUTF8=1
ship-gate: RED — not shipped-ready (25 new/undispositioned WARN(s))
real exit code: 1

findings                95
  fail                   0      <- no hard-fail organ; the RED is WARN-driven only
  warn                  52
    dispositioned       27
    UNDISPOSITIONED     25      <- the whole reason the gate is RED
register entries        30
  [stale] (matched no live WARN)  3
```

Note the exit code was captured **unpiped**. Piping the run through `tail` reports the
*pipe's* exit code (0) and hides the gate's 1 — the same masking trap the repo has recorded for
`pytest`.

### 3.2 The three `[stale]` lines, verbatim

```
[stale] disposition warn-row-length-533-audit-decomposition matched no live WARN — review/remove (ADR-75 decoration rule)
[stale] disposition warn-row-length-529-telemetry-emit      matched no live WARN — review/remove (ADR-75 decoration rule)
[stale] disposition warn-row-length-530-single-flight       matched no live WARN — review/remove (ADR-75 decoration rule)
```

### 3.3 Enumerating the undispositioned 25 — and why the mandate was right that no mode does it

**No mode enumerates them.** This is not a search failure; it is visible in the source.
`cmd_ship_gate` computes the list and then never prints it:

```python
for f in findings:
    click.echo(f"  {_marker.get(f.status, '[??]')} {f.check_name}: {f.evidence}")
for f, e in dispositioned:
    click.echo(f"  [disp] {f.check_name}: WARN dispositioned by {e.get('id')} ...")
for d in stale:
    click.echo(f"  [stale] disposition {d.get('id')} matched no live WARN ...")
```

The first loop prints **all 52** WARNs under one undifferentiated `[~~]` marker — dispositioned
and undispositioned alike. The `[disp]` loop then prints the *register entry* that matched, not
the WARN evidence it matched. So the operator is given 52 warnings, 27 disposition ids, and a
count of 25, with **no rendered mapping between them**. The `undispositioned` list is a live
local variable that only ever reaches `len()`.

**Closest existing surface:** the `[~~]` block of `ship-gate`, set-differenced by hand against the
`[disp]` block. That is the honest answer to "which surface gives me this today".

**The list itself** was derived by importing `audit.py` and reusing its own
`ALL_CHECKS` + `_load_dispositions()` + `_match_disposition()` — not by reimplementing the
matcher, so the derivation cannot drift from the gate. It reproduces the gate exactly
(95 findings / 52 warn / 27 disp / **25 undisp** / 0 fail).

| # | Organ | Count | Owner row | Owner status |
|---|---|---|---|---|
| 1 | `doc_rot` — `backlog-row-length` | **20** | `[#532]`/A9 (the ruling all six row-length dispositions cite) | **CLOSED** |
| 2 | `doc_rot` — `grooming-cadence` | 1 | `[#348]` Backlog grooming as a standing routine | open |
| 3 | `undeclared_edges` | 2 | `[#241]` Undeclared-edge groom | open |
| 4 | `fleet_audit_replication` | 1 | `[#460]` | **CLOSED** |
| 5 | `review_artifact_coverage` | 1 | `[#560]` | open |

The 20 row-length WARNs, verbatim (`chars (declared ceiling 1320)`):

```
#344 1485   #533 2239   #534 1640   #549 1491   #564 1826
#569 2476   #571 1602   #420 1370   #559 3073   #577 3193
#568 1671   #491 3164   #578 2711   #570 1439   #541 1758
#561 2386   #567 1746   #348 1360   #426 1370   #555 1508
```

and the fifth doc_rot WARN:

```
history-accretion bloat: grooming-cadence BACKLOG#grooming-cadence
  (last groom 2026-07-30, 24d ago (> 21d cadence, ADR-41))
```

the two edges:

```
undeclared prose edge (ADR-88 FC2): docs/intake/2026-08-22-tech-document-dependency-graph-organ.md -> handoff-process (tier 1)
undeclared prose edge (ADR-88 FC2): ecosystem/conformance.md -> handoff-process (tier 2)
```

and the two singletons:

```
fleet_audit_replication: automation/fleet-audit is 2 commit(s) ahead of origin -- a recent push
  likely failed; ADR-80's durable record is behind
review_artifact_coverage: 22 code-impact merge(s) since 2026-08-05 carry no linked review artifact
```

**`fleet_audit_replication` is the one WARN with a mechanical, non-judgment fix**: the branch is
literally 2 commits ahead (`git rev-list --count origin/automation/fleet-audit..automation/fleet-audit` = 2,
tip `e3fecaf5 chore(routine/fleet-audit): record 2026-08-23 baseline`). Pushing that branch clears
it. It was **not** pushed here — the mandate freezes this session to its own branch and forbids
unplanned mutation, and pushing a sibling automation branch is outside the write-scope even as
amended. **Flagged for the operator as a one-command clear.**

**Two of the five owner rows are CLOSED**, so **21 of the 25** blocking WARNs (the 20 row-length
plus `fleet_audit_replication`) currently have **no open row that owns them**. A WARN whose owner
is closed cannot be worked off through the ledger; it can only be re-dispositioned or re-filed.

### 3.4 Does a RED ship-gate block the ADR-85 pre-push leg on `main`? — **NO**

**Answer: only the anchor leg (and the FF leg) block a push. A RED ship-gate does not.**
Dispositioning is therefore **housekeeping with respect to pushing**, and a **hard precondition
with respect to `/ship`**. This is settled mechanically, not by reasoning:

**(1) There are exactly two pre-push hooks, and neither is ship-gate.** Parsed from
`.pre-commit-config.yaml`:

```
id=block-ff-push          stages=['pre-push']  entry=uv run --locked python scripts/block_ff_push.py
id=block-unanchored-push  stages=['pre-push']  entry=uv run --locked python scripts/block_unanchored_push.py
```

No hook in the config has `ship-gate` or `ship_gate` in its entry, and neither pre-push script
mentions either token (`grep` over both files returns nothing).

**(2) `ship-gate`'s own docstring names its moment, and it is `/ship`, not push:**

> Pre-ship verification-organ gate (#147): make "Definition of shipped" point
> (6) enforceable at **/ship time**. No file writes (read-only, Layer-2).

and it states the seam against the *commit* gate explicitly:

> - `audit-health` gates each COMMIT: FAIL-only (WARNs pass), gate-mode SKIPS the
>   expensive claim-3 (pytest --collect-only) to stay fast.
> - `ship-gate` gates the feature ARC at /ship: FAIL **and** new/undispositioned WARN

Note what this pairing implies and the mandate should hear plainly: because `audit-health` is
**FAIL-only**, all 25 undispositioned WARNs pass every commit — which is why every commit in this
session went green against a RED ship-gate. There is no contradiction; they are different postures.

**(3) The only consumer that blocks on it is the `/ship` command**, which owns the arc-merge:

> `python scripts/audit.py ship-gate`. If it exits non-zero, stop:
> `Pre-flight FAILED: ship-gate red — verification organs not green for this arc (see the gate
> output; fix a FAIL or disposition/clear a new WARN in ecosystem/disposition-register.yaml — do
> NOT disposition a real drift).`

`/handoff-verify` also *reads* the gate, but as a read-back row in an evidence table — it reports,
it does not gate.

**Consequence for the window.** The five lanes can branch, commit and push all day with the gate
RED. What they cannot do is `/ship`. So dispositioning is **not** a precondition for opening the
batch — it **is** a precondition for closing any arc through `/ship`, and it will surface at the
integrator, not at the lanes. Sequencing it before dispatch is optional; sequencing it before the
first `/ship` is not.

### 3.5 The three `[stale]` dispositions — the mandate's hypothesis is HALF right

The mandate proposed one shape: *"they orphaned when their rows closed or were pointer-ized"*.
Measured, **there are two distinct shapes, and the second is the more serious**:

| Disposition | Subject row | Row status | Live WARN? | Why it orphaned |
|---|---|---|---|---|
| `warn-row-length-529-telemetry-emit` | `[#529]` | **closed** | no | Row left the ledger — hypothesis holds |
| `warn-row-length-530-single-flight` | `[#530]` | **closed** | no | Row left the ledger — hypothesis holds |
| `warn-row-length-533-audit-decomposition` | `[#533]` | **OPEN** | **YES** | The row was *edited*, not closed |

`[#533]` is the interesting one. Its row is open, over budget, and **emitting a live WARN right
now** — it is item 2 in the undispositioned list above at `2239 chars`. Its disposition reads:

```yaml
id:    warn-row-length-533-audit-decomposition
organ: doc_rot
match: 'backlog-row-length BACKLOG#533 (4210 chars'
ref:   '[#532]/A9'
```

The `match` pins **`4210 chars`**. The row has since been shortened to **2239**. The substring no
longer matches, so the entry orphans as `[stale]` **and** its WARN silently re-enters the blocking
set. One edit produced both a false `[stale]` line and a new RED contributor.

**This is a class defect, and it is measurable.** All **6** `doc_rot` row-length dispositions in
the register embed a volatile character count in `match`; the other **24** entries are count-free:

```
volatile (embeds "(NNNN chars"):  6 of 30   — every row-length disposition
  546 (2227)  547 (2099)  552 (3576)  533 (4210)  529 (2001)  530 (1871)
count-free:                      24 of 30   — no_ff, undeclared_edges, reconciled_versions,
                                              review_artifact_coverage, journal_spine_anchor
```

**3 of those 6 have already orphaned — a 50% failure rate in the class.** The surviving three
(`#546`, `#547`, `#552`) are dispositioned only because nobody has edited those rows yet; each
will orphan on its next edit. Since `doc_rot` row-length WARNs are **20 of the 25** things keeping
the gate RED, this one design choice is the dominant cause of the current verdict.

### 3.6 Is the stale shape mechanically detectable? — **YES, both shapes, separately**

Reporting only, per the mandate; nothing was built.

- **Shape (a), closed subject row.** Deterministic. `match` carries the id in a fixed literal
  (`backlog-row-length BACKLOG#(\d+)`); resolve `tasks/<id>-*.md` and read its `status:`
  frontmatter. Terminal status (`closed` / `retired` / `superseded`) + no live WARN = provably
  orphaned. No judgment. Both `#529` and `#530` are caught by this with certainty.
- **Shape (b), drifted evidence.** Also deterministic, but a *different* predicate: key the
  register entry by its **id-prefix** (`backlog-row-length BACKLOG#533 (`) rather than the full
  string, and compare against the live WARN set. A live WARN sharing the prefix but not the full
  `match` is a **drifted** disposition, distinguishable from a genuinely-cleared one. `#533` is
  caught only by this leg, and it is exactly the case a shape-(a)-only detector would mislabel as
  "row still open, so the disposition must be fine".

The cheaper structural fix — noted, not proposed as work — is upstream of detection: **stop
embedding the measurement in `match`.** A `match` of `backlog-row-length BACKLOG#533` (no count)
is still a whole-Finding substring match, still satisfies the register's stated disposition
contract, and cannot be invalidated by an edit that does not change which row is over budget.
That would retire shape (b) rather than detect it.
