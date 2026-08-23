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

---

## 4. Premise verification (Step 4 — closes PK5)

**Rule applied literally: no verdict without a quoted primary source.** Where a premise is
partly right, it is split rather than rounded to the nearest verdict.

| # | Premise | Verdict |
|---|---|---|
| **A** | `[#171]` leg 1 is **already ruled as option (b)** — an execution item, not a fork | **REFUTED** |
| **B** | f7 conformance-freshness and `[#171]` leg 1 are the **same root defect** | **CONFIRMED** |
| **C** | `review_artifact_coverage` exists / registered / owned by `[#560]` / known defect; funnel taxonomy codified in PLAYBOOK Ch8 | **CONFIRMED** (both halves) |
| **D** | Intake §5 makes CONSUMED/SUPERSEDED/REJECTED terminal-and-archived, ACCEPTED deliberately not; "0 archived" is not a defect | **CONFIRMED** — and the underlying "0 intakes archived" claim is **factually false** |
| **E** | `[#577]` is the provider-configuration carrier (mandate) vs the AGENTS.md lane (architect) | **ARCHITECT CORRECT; mandate REFUTED** |
| **F** | `[#563]` and `[#566]` are closed with outputs wired to no consumer | **CONFIRMED as fact**; "merged but never in effect" **REFUTED as characterization** |

### Premise A — REFUTED. It is a live fork, not a ruled execution item.

Three negative searches and one positive quote.

1. **`[#171]` appears NOWHERE in `protocols/STANDING_RULINGS.md`** (`grep -n "#171"` → no output). No
   ruling under an alias either: `conformance dashboard`, `gen_dashboard`, `ADR-80`, `writer policy`
   and `committed-generated` all return **zero** hits in that file.
2. **`[#171]` appears in NO 2026-08-22 artifact.** All 23 `docs/audits/2026-08-22-*.md` were
   grepped; not one names it. The "2026-08-22 batch-ruling artifact" the mandate cites as a source
   for this ruling does not discuss the row.
3. **The named artifact says the opposite, in the present tense.**
   `docs/audits/2026-08-23-technical-lane-docs-governance.md`, Item 6:

> Leg 2 is discharged by this commit. **Leg 1 is not, and no code path performs it** — verified
> live, not carried from R3: `gen_dashboard.py::write_outputs` (`:1193-1200`) writes two files and
> returns `0`; `main` has no commit path; the sole `subprocess` site is `GitReader` (`:236-250`),
> which reads. Both artifact faces nonetheless assert *"Generated, committed, read-only"*. That is
> R3 **F3**, a P1 whose disposition is **an architect choice between (a) implement the ADR-80
> writer policy or (b) rule that human-committed satisfies "committed"** and amend ADR-86 §2 plus
> the two artifact strings. R3 says *"Do not leave (c)."* Closing the row today would be leaving (c).

and again in its §4 *Found, reported, NOT acted on*:

> **R3 F3 — `[#171]` leg 1** (P1): the generator claims to commit its own output and has
> no commit path. Blocks the row's close. **Needs the architect's (a)/(b) choice.**

**What went wrong in the premise.** The mandate reads *"amendments owed to ADR-86 §2 and two
artifact strings"* as the **consequence of a decision already taken**. In the source those words are
the **description of option (b)** — the cost of a choice nobody has made. The fork is open. This is
material rather than pedantic: the mandate would have sent a lane to *execute* a ruling that does
not exist, and `[#171]` leg 1's disposition is a **decision the architect still owes**.

### Premise B — CONFIRMED. One root defect, two filings.

The root is quoted from the generator's own module docstring (`scripts/gen_dashboard.py:9-11`):

> LOCATION + ZONE CLASS are ruled, not chosen here: ADR-86 puts the dashboard at
> `ecosystem/conformance.md` as an ADR-80 **committed-generated** zone -- a read-only validator
> generates it and **commits its own output**.

**No such commit path exists.** `write_outputs` in full:

```python
def write_outputs(repo_root: Path, git) -> int:
    dashboard = build(repo_root, git)
    for relpath, renderer in _TARGETS:
        path = repo_root / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(renderer(dashboard), encoding="utf-8", newline="\n")
        print(f"gen_dashboard: wrote {relpath}")
    return 0
```

It writes and returns. The only `subprocess` site is `GitReader`, whose own docstring reads *"The
only place a subprocess is spawned. Injectable so every renderer stays pure."* — and it reads.

Both artifact faces carry the false claim:

```
ecosystem/conformance.md:7    > **Generated, committed, read-only** (ADR-86 location + ADR-80 zone class)...
ecosystem/conformance.html:45 <p class="note">Generated, committed, read-only (ADR-86 location + ADR-80 zone class)...
```

**Measured live this session, which is what makes B more than a code-read:**

```
gen_dashboard.py --check   ->  STALE ecosystem/conformance.md
                               STALE ecosystem/conformance.html
--check armed anywhere?    ->  NO  (no reference in .pre-commit-config.yaml or .claude/settings.json)
last 5 commits to the artifact:
  5e776542 2026-08-20 rdwornik    docs(dashboard): regenerate over every landing of the day...
  a53b961b 2026-08-19 rdwornik    chore(dashboard): [#171] regenerate so Section 0 carries...
  ee601894 2026-08-19 rdwornik    chore(dashboard): [#171] regenerate the conformance dashboard...
  7f2f4096 2026-08-19 robdwornik  chore: [#171] refresh the dashboard onto the tree that carries it
  278211e3 2026-08-19 robdwornik  feat: [#171] land ecosystem/conformance.{md,html}...
```

**Every commit that has ever updated the artifact was made by a human**, and the newest is
2026-08-20 against a `main` that has advanced well past it. So the same single absence — no writer
in the generator — produces *both* filings: the **"committed" leg of `[#171]`'s Done-when** is
undischarged, and the artifact **goes stale** because nothing but operator memory refreshes it.
Same root, two symptoms. **CONFIRMED.**

**One boundary the architect should not let a lane blur.** The adjacent finding *R3 F5 — `--check`
is armed nowhere* is a **different** defect: a gating gap, not a writer gap. Implementing the ADR-80
writer policy would fix B and leave F5 exactly as it is (an unarmed check is unarmed whoever
commits). They travel together in the same lane; they are not one item.

### Premise C — CONFIRMED, both halves.

**Half 1 — the organ.**

```
scripts/audit.py:3184   def check_review_artifact_coverage(repo_path: Path) -> list[Finding]:
scripts/audit.py:3443       check_review_artifact_coverage,   # [#480] P3 — ADVISORY (WARN-tier by ruling);
ALL_CHECKS members: 43   |   review_artifact_coverage present: True
```

Owned by **`[#560]`, status `open`**, and the "known defect" is not inferred — it is the row's
own **title**:

> `review_artifact_coverage` reads only the FIRST branch/HEAD triple per file, and one title
> literal, so a real review can be invisible to it

with the mechanism in the body: *"lane E was reviewed but sits in the SECOND triple of a
two-branch artifact and `.search` takes the first"*, and *"Artifacts are IMMUTABLE (§5 rule 3), so
the repair is reader-side."* The organ is **advisory by ruling**, which the live WARN restates:
*"advisory per the [#480] P3 ruling; the hard pre-push leg is deferred pending 0 false positives
over two consecutive windows."*

*Minor, flagged under M1 rather than swept:* `[#560]`'s `refs` cite `scripts/audit.py:3117-3320`;
the function now begins at **3184**. The range still contains it, so the locator resolves, but its
start has drifted — worth re-pointing when the row is next touched.

**Half 2 — the taxonomy.** `protocols/PLAYBOOK.md` Ch8, *"The wave close — every dispatched wave
ends D0–D5, and the funnel table is mandatory"*, carries it verbatim:

> **The five classifications, and the clause each answers to** (ADR-111 §1's four outcomes, plus the
> executed case):
> - **MECHANICAL** — §1(b) DISCHARGED. The fix is judgment-free, so the integrator may execute it in
>   the session. **List these first**, and a discharge is only a discharge **with a locator that
>   resolves**...
> - **ADR** — §1(c) CANDIDATE where ADR-98 §3's fork test is met... **PROPOSED with the Decision blank**...
> - **INTAKE** — §1(c) CANDIDATE otherwise. **A finding may not become a backlog row directly** (§2)...
> - **REJECT** — §1(d), **with the reason recorded where the finding lives**...
> - **COVERED** — §1(a) OWNED. Cite the id and **add nothing**.

The five-vs-four question the ADR-111 title raises is answered in the source itself — *"ADR-111
§1's four outcomes, **plus the executed case**"*. Nothing to build; **D4** already makes the table
mandatory (*"A table that classifies nothing is not a wave close"*).

### Premise D — CONFIRMED on doctrine, and the "0 archived" claim is factually FALSE.

The doctrine is quoted exactly as the premise states it — `docs/intake/README.md` §5:

> Terminal docs (CONSUMED | SUPERSEDED | REJECTED) relocate byte-identical to
> `docs/intake/archive/` (operator ruling 2026-07-22, archive-inside-each-folder; terminal set per
> the [#398] deploy — **ACCEPTED is deliberately NOT in it, a standing authority must stay visible
> live**); live docs stay here.

and on the ACCEPTED status itself:

> **ACCEPTED (decided-by + disposition)** — ruled standing authority... **Not archival** — an
> ACCEPTED doc stays live and visible.

So the premise's reasoning is right. **But its factual predicate is wrong**, and the correction is
worth more than the confirmation. Measured by parsing YAML frontmatter (not grep — two prose lines
in doc bodies contain a literal status token and would have corrupted a naive count):

```
LIVE  docs/intake/*.md          36 files   SEED 10 · DRAFT 6 · READY 1 · ACCEPTED 19
ARCHIVE docs/intake/archive/*.md 7 files   CONSUMED 5 · SUPERSEDED 1 · REJECTED 1

METRIC A   ACCEPTED-docs-in-archive   = 0    <- the metric the mandate asked for. It is ZERO.
METRIC B   terminal-docs-still-LIVE   = 0    <- the inverse metric; also ZERO
METRIC C   total archived             = 7    <- so "0 intakes archived" is simply not true
```

The live counts reproduce the generated Contents index (SEED 10 / DRAFT 6 / READY 1 / ACCEPTED 19)
exactly. **Metric A = 0** is the answer to the question asked. **Metric B = 0** is the stronger
result and was not asked for: not one terminal doc is sitting un-relocated. The archival rule —
which §5 notes is *"MANUAL for now — the status-coupled validator that would gate/automate it is
wave work, not built"* — is being executed **7-for-7 by hand, with zero violations in either
direction**. There is no defect here to file, and the ungated-but-perfectly-observed state is the
finding.

### Premise E — the ARCHITECT is right; the mandate is wrong. And the lane already handles it.

**`[#577]` is the AGENTS.md lane.** Its frontmatter and title:

```yaml
id: "[#577]"
title: "Adopt `AGENTS.md` as the portable instruction layer — the bounded execution lane"
status: open
priority: P2
size: M
theme: "[E6] Cross-repo universalization"
serialize-group: claude-md
```

and its body opens *"**RULED ADMITTED (architect, 2026-08-22); this row is the execution, not the
decision.**"* — with four binding bounds, all about `AGENTS.md` (≤120 lines, portability-not-quality,
the `~/.codex` precedence collision, a guard stated **in bytes** because the Codex
`project_doc_max_bytes` cap measures bytes). **Nothing in the row concerns
`ecosystem/provider-registry.yaml`.**

**`ecosystem/provider-registry.yaml` EXISTS** — 5,889 bytes, added 2026-08-22. What it holds:

```
providers:  3   anthropic (cli: claude) · openai (cli: codex) · xai (cli: null)
models:     5   claude-sonnet-5 · claude-opus-4-8 · gpt-5.6-terra · gpt-5.6-sol · grok-l5
```

**Seams — three different numbers, and conflating them is how this gets misread:**

```
9  DECLARED in scope by the file's own header (R2 §3.2 table-edit seams):
     S7, S8, S9, S10, S11, S17, S26, S29, S30
7  ASSERTED by the pre-commit gate scripts/check_provider_registry.py:
     check_s8_tool_versions · check_s9_artifact_reader · check_s10_conformance_hub
     check_s17_playbook · check_s26_settings · check_provenance_pins (S29+S30)
     (+ check_registry_shape, which validates the registry itself, not a seam)
5  PINNED sites actually listed in the registry pinned_at blocks:
     .claude/agents/artifact-reader.md (S9) · .claude/workflows/conformance-hub.js (S10)
     protocols/PLAYBOOK.md (S17) · ecosystem/satellite-onboarding-rulings.yaml (S29)
     pyproject.toml (S30)
```

The remainder resolve honestly: **S7** is read at *runtime* by `scripts/changelog_sentinel.py`
via `scripts/provider_registry.py`, and **S11** is explicitly **not a model seam** — the header
says *"S11 is a canonical-DOC seam... It is repointed at the sibling canonical-doc-name registry
(`scripts/canonical_docs.py`)"*. Mechanical consumers, whole set: `scripts/provider_registry.py`
(reader), `scripts/check_provider_registry.py` (checker), `scripts/changelog_sentinel.py`
(runtime), `tests/test_provider_registry.py`, `.pre-commit-config.yaml` (gate wiring).

The header also pre-empts a scope error the batch could easily make:

> **ROUTING IS NOT HERE.** R2 §3.3 records that the canonical model-routing table is
> `~/.claude/ROUTING.md` — at L0, outside this repository... This registry records model
> IDENTITY, not which model gets routed to which job.

**Where the mandate's confusion came from — and why it costs nothing.** The provider-config work is
**lane L1**, and `LANE-L1-provider-config.md` does name `[#577]` — as the *only* row id in the file.
But it names it **as the thing to check, with both branches pre-written**, and it is gated on this
very packet:

> **Dispatch gate:** Phase 0's packet has landed and premise **E** is answered — whether
> `ecosystem/provider-registry.yaml` already exists, what it holds, how many seams consume it,
> and what `[#577]` actually carries. **Do not dispatch before that.**

> **2. Carrier row.** **If premise E confirms `[#577]` is the AGENTS.md carrier, do not extend
> it** — subjects do not share rows. Write the specification for a new carrier row into your
> artifact; do **not** create the task file.

**So the operative answer to L1 is: `[#577]` IS the AGENTS.md carrier. L1 must NOT extend it, and
must instead specify a new carrier row in its artifact without creating the task file.** The
contract is sound; only the mandate's prose was wrong.

### Premise F — CONFIRMED as fact; the characterization is REFUTED for `[#563]`.

**Both are closed.** `tasks/563-*.md` and `tasks/566-*.md` both carry `status: closed`, closed
together on operator GO at `5de708f1` and merged at **`ad3e10d9`** *"D5+D6: the ruling executed;
closes [#563] [#566] [#488]"*.

**Neither output is wired to a consumer — but for opposite reasons.**

- **`[#566]`** shipped `gen_task_tree.py --rank`. Every non-doc reference to `--rank` in the repo is
  **its own definition** (`gen_task_tree.py:37, 1251, 1312, 1316, 1336`); the rest are artifacts
  *describing* it. No hook, command, gate, test-runner or `.claude/` config invokes it. Its own
  artifact states this is intended: *"gates a permanent diff. `--rank` computes it on demand
  instead."* An on-demand operator report, unwired **by design**.
- **`[#563]`** shipped `scripts/export_backlog_view.py` (23,909 B, present). Non-wiring here is not
  an oversight — it is **binding condition 3, ratified**:

> **Three binding conditions, all three load-bearing:** (1) **one-way export only** — `tasks/`
> stays the single source of truth; (2) a **disposable, gitignored export dir**, regenerated per
> read; (3) **governance stays bespoke** — **no gate, hook or script is re-pointed at the export**.

Verified live: a repo-wide search for `export_backlog_view` across `*.yaml` / `*.json` / `*.py`
(excluding the script and its tests) returns **nothing**, and `.gitignore:114` carries
`.backlog-view/`. **Condition 3 is being honoured exactly.**

So the premise's *facts* hold — both closed, neither wired. Its *reading* — "merged but never in
effect" — is wrong for `[#563]`: wiring it to a consumer would **violate its ratified terms**. A
lane told to "wire up the unwired outputs" would break a binding condition. The honest statement is
**unwired by ruling**, not stranded.

### 4.1 `codex/` — mechanical inventory (no recommendation; M2 is the architect's to rule)

```
path              codex/
contents          exactly ONE file: codex/AGENTS.md
size              3,891 bytes (directory total 4.0 KB)
tracked           1 file (git ls-files codex/ -> codex/AGENTS.md)
last COMMIT       fcd4eb64  2026-05-19  "feat: add codex/AGENTS.md — canonical global Codex
                                          reviewer config"     (96 days ago; the only commit)
working mtime     2026-08-02 19:31 (checkout artifact — git content unchanged since 2026-05-19)
```

Its own first lines declare its role:

> # AGENTS.md — Global Codex Reviewer Configuration
> > **Canonical source** for `~/.codex/AGENTS.md`. Owned by `.dev-knowledge`. Deploy by copying to
> > `~/.codex/AGENTS.md`.

**Every inbound reference from a tracked file** (JOURNAL prose mentions excluded as narrative):

| Referencing file | Line | What it says |
|---|---|---|
| `.methodology.yaml` | 134 | `codex/ holds the canonical source of the global Codex reviewer config` |
| `deploy/carrier_globalconfig.py` | 18 | `source_path: codex/AGENTS.md  # hub canonical source, relative to the hub root` |
| `deploy/carrier_globalconfig.py` | 53 | `DEFAULT_SOURCE_REL = "codex/AGENTS.md"  # hub canonical source (ADR-54)` |
| `deploy/manifest-v1.0.0.yaml` | 33, 45, 48 | declared payload + `source_path` |
| `deploy/manifest-v1.1.0.yaml` | 77, 230 | `source_path` + `source` |
| `deploy/manifest-v1.2.0.yaml` | 82, 299 | `source_path` + `source` |
| `deploy/manifest-v1.3.0.yaml` | 97, 317 | `source_path` + `source` |
| `deploy/manifest-v1.3.1.yaml` | 106, 326 | `source_path` + `source` |
| `deploy/manifest-v1.4.0.yaml` | 118, 458 | `source_path` + `source` — **the live manifest** |

**Stated flatly, no recommendation attached:** `codex/` is not orphaned. It is the hub-canonical
source of a **deployed L0 carrier under ADR-54**, named by `deploy/carrier_globalconfig.py` and by
**all six** deploy manifests including the in-flight `v1.4.0`. Removing or relocating it breaks the
carrier's `source_path`. Its content has not changed in 96 days, which is a fact about its
stability, not evidence either way about its value.

**One live interaction the architect should hold alongside M2**, quoted from `[#577]`'s own row —
because it makes `codex/` and the AGENTS.md lane the same conversation:

> the precedence chain has an **unpriced third layer** — `codex/AGENTS.md` sits at an intermediate
> directory *inside this repo*, so a cwd at or below `codex/` yields `role → doctrine → role` and
> the role wins by position rather than by intent.

### 4.2 Dispatch readiness — both resolve, and the five prompts are already staged

```
Dispatch-Lane            RESOLVES  -> Alias -> DispatchHelpers\Start-DispatchLane
dispatch                 RESOLVES  -> ExternalScript -> C:\Users\1028120\.dev-terminals\bin\dispatch.ps1
                                      (the PATH command PLAYBOOK Ch8 specifies, not a dot-sourced
                                       alias; -DryRun is supported)
$env:CLAUDE_PROMPTS_DIR  = C:\Users\1028120\Downloads   EXISTS: yes   (347 .md files)
```

The directory holds this session's own contract (`SESSION-00-phase0-preconditions.md`, 12,541 B),
which is direct proof the channel works end-to-end.

**More usefully: all five lane prompts are ALREADY PRESENT**, so the batch is not waiting on
authoring:

| Prompt file | Bytes | Lane title | Mode / Effort | Row(s) named |
|---|---|---|---|---|
| `LANE-L1-provider-config.md` | 8,120 | Provider configuration (M1) | auto / high | `[#577]` (as a *check*, both branches written) |
| `LANE-L2-funnel-coverage.md` | 9,548 | Audit funnel coverage checker (M3) | **plan** / **xhigh** | `[#560]` |
| `LANE-L3-status-grammar.md` | 8,021 | Status-grammar validator + ADR marker sweep (M5) | auto / high | `[#242]`, `[#362]` |
| `LANE-L4-dashboard-commit-path.md` | 8,213 | Generated-output commit path (M8 + `[#171]` leg 1) | auto / **medium** | `[#171]` |
| `LANE-L5-docs-actual-state.md` | 8,454 | Functional docs to ACTUAL state, claim by claim (M6) | auto / high | none (unfiled sweep) |

Each declares a `worktree-<slug>` name conforming to the `CLAUDE.md` §4 lane-prefix enum, and each
names terra as a mandatory pre-merge reviewer (L2 adds an adversarial `sol` pass on the
gate-severity question).

**Two sequencing facts the architect should read together.** L1 is explicitly **gated on this
packet** (§Premise E). And **L4 carries `[#171]` leg 1 at effort `medium`** — but Premise A found
leg 1 is an **unruled (a)/(b) fork**, not an execution item. L4 cannot execute a ruling that does
not exist; either the architect rules the fork before L4 is dispatched, or L4's contract must be
re-scoped to price the fork rather than implement it. **This is the single highest-value
consequence of the premise pass**, and it is exactly the failure the mandate set out to prevent.
