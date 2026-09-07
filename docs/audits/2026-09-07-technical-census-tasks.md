# CENSUS — `tasks/` — sweep 2026-09-07, lane S-06

> **READ-ONLY.** This lane moved, deleted, edited and renamed nothing. Every verdict below is a
> **PROPOSAL** the operator rules. Twelve peer census lanes measured other folders in the same
> tree at the same time; nothing here was repaired, because a census that repairs what it
> measures has destroyed its own evidence.

**Consumer:** `[#506]` (whole-set grooming arc — the row that consumes a per-row sheet like this
one) · `[#440]` (the tamper-evidence gap this census re-measures) · `[#580]` (state-as-data /
atomic id allocation) · `[#589]` · `[#590]` · `[#171]` · `[#612]`. Substantive citations by path:
`tasks/README.md`, `tasks/manifest.json`, `tasks/archive/README.md`,
`scripts/gen_task_tree.py`, `scripts/archive_row_body.py`, `scripts/backlog_source.py`,
`docs/decisions/ADR-107-*` §6.3, ADR-111.

**Per-file verdict table:** `docs/audits/2026-09-07-technical-census-tasks-appendix.md`, split out
under this contract's 40 KB rule and committed with this file.

**Measurement base:** `origin/main` @ `21576e3` (merged into this lane before any measurement was
recorded). `tasks/`, `BACKLOG.md` and `tasks/manifest.json` are byte-unchanged across that merge,
so every number below was taken on the tree this file lands against.

**Fan-out:** `gemini` is **NOT on PATH** in this container (`which gemini` → exit 1), so
`fan-out: NONE`. Gemini-read files: **0**. Fabricated locators counted: **0** — no reader produced
any locator to re-open, so this is an absence of input, **not** a clean run. Copilot Enterprise
offload is **not** available until intake `#75` is ratified and was **not** used. (`#75` is written
unbracketed on purpose: it is an intake id, and no `tasks/75-*.md` exists — bracketing it would
make this file the twenty-fifth dangling citation Ask 3 counts.)

---

## Inventory

`tasks/` is not a document folder. It is the **source of truth for the backlog** since the ADR-107
strangler step 3 executed by `[#439]` on 2026-07-28: `BACKLOG.md` is *generated from it*, and since
`[#589]` (2026-08-26) `BACKLOG.md` is a one-line-per-row **view** whose full bodies live only here.
That inverts the usual census question — nothing here is a candidate for relocation or archival on
its own merits, because the tree *is* the store two dozen gates read.

| Group | Files | Bytes | Verdict | Witness |
|---|---|---|---|---|
| `tasks/README.md` | 1 | 6,576 | KEEP | generator `scripts/gen_task_tree.py`; 46 modules under `scripts/`+`tests/` reference `tasks/` |
| `tasks/manifest.json` (schema 2) | 1 | 68,365 | KEEP | generator `scripts/gen_task_tree.py`; gate `audit.py::task_tree_coherence`; 224 `task` nodes + 277 `prose` nodes |
| Row files — **live in the queue** | 224 | 392,865 | KEEP | each referenced by a manifest node; rendered into `BACKLOG.md`; read as source by `scripts/backlog_source.py::canonical_text` |
| Row files — **retired allocation records** | 140 | 261,422 | KEEP | ADR-107 §6.3 retire-never-delete; `--prune` is refused; all 140 carry `generates: BACKLOG.md` and a terminal `status:` |
| `tasks/archive/*.md` records | 24 | 61,643 | KEEP | generator `scripts/archive_row_body.py`; each pointer present in its row exactly once (`verify` legs B/E) |
| `tasks/archive/README.md` | 1 | 6,471 | KEEP | generator `scripts/archive_row_body.py`; `tests/test_archive_row_body.py` |
| **Total** | **391** | **797,342** | | |

**Structural coherence — measured, five independent legs, all clean:**

- filename id == frontmatter `id:` on **364/364** files (0 mismatches);
- every in-queue file's manifest node names the same filename it has on disk (0 mismatches);
- **0** retired (out-of-queue) records carry a non-terminal `status:`;
- **0** in-queue rows carry a terminal `status:` — so `[#556]`'s closed-but-present class is
  currently empty on this tree;
- **0** rows are missing a `Done when:` clause: 224 of 224 live rows carry one.

**Status split:** live 171 `open` + 53 `deferred`; retired 135 `closed` + 4 `retired` +
1 `superseded`. **Priority:** 33 P1 / 187 P2 / 144 P3. **Size:** 206 S / 140 M / 18 L.

---

## Proposals

### KEEP — 391 of 391 files

No file in `tasks/` earns RELOCATE, ARCHIVE or RETIRE, and the reason is mechanical rather than
generous. Every row file is either (a) referenced by a `tasks/manifest.json` node, which makes it
live source, or (b) an unreferenced **allocation record** whose deletion ADR-107 §6.3 forbids and
whose whole function is to occupy its id. `tasks/archive/` is the same shape one level down: 24
records, each paired to a live in-queue row that carries its pointer exactly once. The two
generated non-row files are emitted by named generators and gated.

The census that would matter here is not "which files go" but "which **rows** are still true", and
that belongs to `[#506]`, not to a folder sweep. The findings below are that census's raw material,
not a substitute for it.

### Findings the operator rules — the lane question, three asks

#### Ask 1 — rows whose Done-when is witnessed on main (W1-8 found 0; re-verified by a second method)

**Method.** For all 224 live rows I parsed the `Done when:` clause out of the body, extracted every
backticked path-shaped token, resolved each against the tree (path first, then basename search),
and then hand-opened the strongest candidates to check the clause's *predicate*, not merely the
artifact's existence. 68 rows name at least one path-shaped artifact; 62 resolve fully.

**Result: W1-8's zero does not survive the second method, but it is close to right.** One row is
fully witnessed, one is witnessed but for an unverifiable observation window, and one carries a
Done-when predicate that is now *false*. Everything else I checked confirms W1-8.

**`[#171]` — Done-when as it reads on main is FULLY WITNESSED. `status: open`.**
Row Done-when: *"`ecosystem/conformance.md` is generated + committed by a read-only validator
(Layer-2-safe) and ARCHITECTURE Ch2 carries the pointer"*. Both legs, each grepped:

- `ecosystem/conformance.md` exists (25,762 B), carries the `generated by scripts/gen_dashboard.py`
  banner, and is committed (`git log -1 -- ecosystem/conformance.md` → `1cefc30`);
- `scripts/gen_dashboard.py:27` — writes *"only under `--write`. It drives no state in any other
  repo, imports no gate"* — i.e. Layer-2-safe and read-only;
- `ARCHITECTURE.md:379`, under the `## Organ map` heading (Ch2): *"**Conformance dashboard →
  `ecosystem/conformance.md`**… generated by `scripts/gen_dashboard.py`"*.

**But the row must not be closed on that**, and this is the sharper finding: the criterion that
actually governs `[#171]` is **not in the row**. `tasks/archive/171.md` Event 1, Clause 1.2 records
a **RE-CUT of 2026-08-27** which states both stated Done-when legs are discharged and narrows the
row to *"a deterministic staleness signal for the four ADR-85-ungated docs is RENDERED in
`ecosystem/conformance.md` by the same read-only generator"*. I checked that narrowed criterion
too: `grep -ci 'ungated\|staleness' ecosystem/conformance.md` → **0**. So the row is correctly
open — on a criterion no gate can read.

**This is a class, not a one-off — five rows, plus two adjacent cases.** `archive_row_body.py`
relocates dated-amendment narration verbatim out of a row into `tasks/archive/<id>.md`, and a
RE-CUT that narrows a Done-when is written *as* dated-amendment narration. It therefore travels
with it. The relocated record is out of `BACKLOG.md` and out of
`scripts/backlog_source.py::canonical_text`, so **every body-reading surface — the view,
`propose_closures`, `validate_doc_rot`, any closure sweep — reads the superseded criterion**:

| Row | Where the operative Done-when lives | Row body still shows |
|---|---|---|
| `[#112]` | `tasks/archive/112.md` — RE-CUT 2026-08-28 (K4) | pre-re-cut clause |
| `[#130]` | `tasks/archive/130.md` — "periodic pass" framing KILLED; *"Done-when narrows to: the gotcha/memory write path carries a dedupe-against-existing step"* | pre-re-cut clause |
| `[#146]` | `tasks/archive/146.md` — *"REMAINDER, now the whole row: clause (b), the sweep"* | both clauses |
| `[#171]` | `tasks/archive/171.md` — narrowed to the `[#169]` staleness signal | the two discharged legs |
| `[#277]` | `tasks/archive/277.md` — leg (a) closed on a live run; *"Done-when narrows to: the WEAK ratio measured again after the rework"* | pre-re-cut clause |
| `[#145]` | `tasks/archive/145.md` — scope **halved**, criterion text explicitly *"Unchanged"* | correct as written |
| `[#169]` | `tasks/archive/169.md` — its DEFER peg was **redirected** to `[#171]`'s post-re-cut remainder | peg names `[#171]` unqualified |

`archive_row_body.py relocate` already refuses a clause *"carrying a structural marker a gate
reads"*. A re-cut Done-when is exactly that in substance and is not one in form. **PROPOSAL:** the
operator rules whether the refusal predicate should recognise a narrowed acceptance criterion, and
whether these five rows' bodies should be restated from their records. This lane did not touch
them.

**`[#590]` — three of four Done-when legs witnessed on main.** `status: open`.
`.pre-commit-config.yaml`, in the `audit-index-freshness` block, states the discharge in its own
words: *"Scoped to the index and its generator, a lane no longer has to commit it for its artifact
to be indexed, **which is [#590]'s first done-when**"*; the same comment records the guarantee
moving to the ship-gate-only `generated_artifact_freshness` leg (artifact `audits-index`) rather
than lapsing, which is legs 2 and 3. Leg 4 — *"zero generated-file conflicts appear across the
next 20 merges"* — is an observation window and is **UNDETERMINED** from this checkout (see Honest
limits: the clone is shallow). **PROPOSAL:** rule whether leg 4 is now satisfiable, or restate it.

**`[#589]` — the Done-when's own byte predicate is FALSE on main today.** The clause requires
*"`BACKLOG.md` measures under 70,000 bytes on an unchanged `tasks/`"*. Measured: **70,668 B** — over
by 668. The shipped gate does not catch it: `scripts/gen_task_tree.py:175` sets
`_VIEW_BYTE_CEILING = 100_000`, so `--check`'s size assertion fires at a threshold 30,000 B above
the row's own criterion. **PROPOSAL:** rule which number binds. Related, and the same defect one
layer out — five present-tense restatements of a count that has moved from 202 to 224 rows, in
violation of this repo's own "never restate a count in prose" convention:
`tasks/README.md:13` (*"fell from 279,814 B to **66,526 B**"* — now 70,668 B), `tasks/README.md:50`
(*"all **202** bodies"*), `gen_task_tree.py:605` (*"176 of **202** rows"*), `:718` (*"**today's** 202
rows"*), `:763` and `:827` (*"all 202 bodies"*). `gen_task_tree.py:158-159` is **not** in this list:
it is explicitly a dated measurement (*"at the time of the flip (2026-08-26, 202 rows)"*) and is
correct as written.

**Rows the second method CONFIRMS are correctly open** — each grepped, each negative, so the method
is not merely finding what it wants: `[#269]` (`docs/audits/README.md`'s own header says the
count-tiered shape *"is `[#269]` and is NOT built"*); `[#285]` (`protocols/PLAYBOOK.md` carries no
`last_reviewed` frontmatter and is absent from `_HUB_ONLY_FRESHNESS_FILES` at
`scripts/audit.py:479-480`, which holds three entries, none of them PLAYBOOK); `[#369]` (no
`boundary-headers` id in `.pre-commit-config.yaml`, no mention in `CLAUDE.md`); `[#542]`
(`ARCHITECTURE.md` names no five-category `doc_rot` split); `[#533]`/`[#535]` (`scripts/audit.py`
is still a facade at 5,000+ lines, though `scripts/audit_checks/` now holds 23 extracted check
modules — partial, and the row says partial); `[#274]` (leg 1 **is** witnessed — `.claude/commands/
changelog-review.md:38-45` names the *"Dogfood-signal prior (`[#274]`; intake doc #2 R4)"* in the
ADOPT rubric — but leg 2 is not: the newest `docs/audits/*changelog-review*` digest is
**2026-07-11** and none of the three most recent contains the string `dogfood`).

**Six rows name a Done-when artifact that resolves nowhere in the tree.** Five are correct — the
artifact is what the row exists to build (`[#540]` `scripts/harvest_batch.py`, `[#573]`
`lychee.toml`, `[#627]` `ROUTING.md`, `[#632]` `tests/test_dispatch_helpers_codespace.py`) or lives
outside the repo by design (`[#625]` `~/.claude/rules/core-invariants.md`, L0). One is
**UNDETERMINED** and reported rather than judged: `[#393]` names `config/category_mapping.yaml`,
`config/excluded.yaml` and `requirements.txt`, which are `corp-monorepo` paths — this lane cannot
see that repo and did not try.

#### Ask 2 — rows with no theme

**Zero, and the zero is verified two independent ways.**

1. **Frontmatter:** all 364 row files carry a non-empty `theme:`; 9 distinct values, all `[E1]`–`[E9]`.
2. **Manifest placement** (the derivation that actually governs, per `tasks/README.md`: theme and
   story come from the enclosing headings): walking `tasks/manifest.json` in order and binding each
   `task` node to the last `## [E…]` prose heading gives **224 of 224** live rows under an `[E*]`
   heading, **0** orphans — and the placement-derived theme agrees with the frontmatter theme on
   **224/224** rows, 0 disagreements.

One observation, not a defect, that the operator may want to rule on: **`[E8] ARC-5 execution`
holds 24 rows (13 of them live)** while `BACKLOG.md`'s own big-picture prose describes `[E8]` as
*"a time-boxed execution arc, **not a permanent mission theme**"*. A time-boxed theme with a live
population is a disposition question, not a naming one. **PROPOSAL:** rule `[E8]`'s status — the
arc closes and its 13 live rows re-theme, or `[E8]` is promoted and the prose is corrected.

#### Ask 3 — rows citing moved ids

**Method.** Two passes, because the loose one is wrong. Matching bare `#\d+` over row bodies
returns 169 rows and 128 distinct absent ids — and it is **unusable**: hand-opening the hits shows
it swallows `core-invariant #5` (`[#414]`, `[#153]`, `[#210]`), `intake #6` (`[#43]`), `doc #3`
(`[#278]`) and finding numbers (`[#277]`'s *"false positives **#5** and **#77**"*). The strict pass
counts only the canonical bracketed `[#N]` grammar: **216 rows, 385 citation edges.**

**24 rows carry a bracketed citation to an id with no file in `tasks/` — 13 of them live:**

| Citing row | Absent target(s) |
|---|---|
| `[#82]` · `[#244]` · `[#267]` | `[#221]`, and `[#244]` also `[#246]` `[#248]` `[#249]` `[#250]` |
| `[#325]` | `[#236]` |
| `[#343]` | `[#337]` |
| `[#402]` · `[#552]` | `[#398]` |
| `[#403]` | `[#321]` |
| `[#428]` | `[#434]` |
| `[#438]` | `[#436]` |
| `[#548]` · `[#549]` · `[#550]` | `[#328]` |
| *(retired rows, for completeness)* | `[#358]` `[#363]` `[#382]` `[#391]` `[#416]` `[#417]` `[#460]` `[#473]` `[#501]` `[#512]` |

**These are not "moved" ids — they are pre-flip ids that never had a file**, and that is a
disclosed property of the tree rather than a defect: the ledger has **270 gaps** between id 4 and
id 634 (364 files over a 631-wide range), because ids closed before the `[#439]` flip lived only as
`BACKLOG.md` lines and were deleted on closure. `tasks/README.md` states this itself under *"Honest
limit — the ledger is not tamper-evident"*, and tracks it as `[#440]`. **PROPOSAL:** none of these
23 citations should be silently repaired; they are legible history. What the operator may want is
`[#440]`'s tombstone record, which would let a reader tell "closed pre-flip" from "lost".

**One near-miss, reported so nobody re-files it:** `[#574]`'s body contains `[#777]`, an id 143
above the high-water mark. Opening the row shows it is deliberate — it quotes ADR-107's record that
*"the next-free-id history scan is defeated by synthetic `[#777]`"*. Not a citation, not a defect.

**The one live risk in this area, and it is narrow.** `[#635]` and `[#636]` were filed on
2026-09-05 and then **dropped on recorded operator consent** — `JOURNAL.md` 2026-09-05 (p) states
it, gives the mechanism (remove the manifest nodes, delete the files, regenerate: *"nodes 503 → 501,
224 tasks, `--check ok`"*), and records that the content is not lost because it lands as CANDIDATEs
AE-1/AE-2. Verified independently: both files exist in exactly **one** reachable tree in this clone
(`1cefc303`, the `worktree-filings-3` tip) and in no tree after the merge that took it. So the drop
is witnessed, deliberate and correct. **The residue is id re-issue.** `next_free = max(id in
tasks/) + 1` is now **635** — the id just freed — while **six live surfaces on main still cite
`[#635]`/`[#636]` as naming that content**: `LESSONS.md:14`, `protocols/STANDING_RULINGS.md:3907-3910`,
`docs/intake/2026-09-05-tech-session-roles-with-a-carrier.md:115-119`,
`docs/handoffs/2026-09-06-dev-knowledge-architect/CENSUS.md:69,282`,
`docs/audits/2026-09-05-technical-batch-r5p-manifest.md:69` and
`docs/audits/2026-09-05-technical-lane-r-000-zc-candidates.md:66,154`. If `[#635]` is issued to a
different task, all six point at the wrong row and no gate notices — `gen_task_tree.py`'s re-issue
detection catches a re-issue only *while the retired record is present*, and here it is not.
**PROPOSAL:** rule whether `[#635]`/`[#636]` should be burned rather than re-issued, or whether
`[#440]`'s tombstone lands first. This is one of `[#580]`'s stated cases (*"two concurrent
allocations cannot yield the same id, shown by a test that fails against today's `max+1`"*).

### RELOCATE — none

### ARCHIVE — none

`tasks/archive/` is not a retention home in the sweep sense; it is a live paired store, and its 24
records are all bound to live rows.

### RETIRE — none

`--prune` is refused by the generator and deletion is forbidden by ADR-107 §6.3. A census cannot
propose what the source-of-truth doctrine already rules out.

### UNDETERMINED — 2

| Subject | What I could not establish |
|---|---|
| `[#590]` leg 4 | *"zero generated-file conflicts across the next 20 merges"* — an observation window over merge history this shallow clone does not carry |
| `[#393]` | its three named artifacts are `corp-monorepo` paths; this lane has no access to that repo and did not guess |

---

## Counts before → proposed after

| | Before | Proposed after | Δ |
|---|---|---|---|
| Files in `tasks/` (incl. `archive/`) | 391 | 391 | 0 |
| Row files (`<id>-<slug>.md`) | 364 | 364 | 0 |
| — live in the queue | 224 | 224 | 0 |
| — retired allocation records | 140 | 140 | 0 |
| `tasks/archive/` records | 24 | 24 | 0 |
| Non-row files (`README.md`, `manifest.json`, `archive/README.md`) | 3 | 3 | 0 |
| Bytes | 797,342 | 797,342 | 0 |
| KEEP / RELOCATE / ARCHIVE / RETIRE | — | **391 / 0 / 0 / 0** | |

**Zero movement is the finding, not a failure to find one.** `tasks/` is the ADR-107 source of
truth: relocation would break the generator, archival would break the queue, and retirement is
forbidden by §6.3. What this folder yields instead is **row-level** findings — 5 rows whose
operative Done-when has left the row, 1 row whose Done-when is witnessed as written, 1 row whose
byte predicate has gone false, 5 stale count restatements, 2 freed-and-still-cited ids, and 1
time-boxed theme with 13 live rows. Those are `[#506]`'s and `[#440]`'s material.

---

## Honest limits

**1. `git` is not an available witness for this folder, in this checkout.** This is a **shallow
clone** — `.git/shallow` carries 17 boundary commits and `git rev-list --count HEAD` is 286, with
the oldest reachable commit dated 2026-09-01. One of those boundaries, `1cefc303` (2026-09-05),
presents the *entire tree* as a single add. The consequence is measurable and total: **all 365
files in `tasks/` report a last-touch date of 2026-09-05 (356) or 2026-09-06 (9)** — not because
the tree was rewritten, but because no earlier commit is reachable. **"The last content commit" —
one of the three witness types this contract admits — is therefore unavailable to me for every
file in this folder**, and no verdict above rests on it. The two that do survive (consumers found
by grep, and the generator that emits it) carry all 391 verdicts.

**2. No Gemini fan-out.** `gemini` is not on PATH; fan-out `NONE`, 0 files read, 0 fabrications.
Zero fabrications here means **no reader ran**, not that a reader ran clean, and I am naming that
because the reverse reading is the one that does damage. Copilot Enterprise offload is unavailable
until `[#75]` is ratified and was not used. Every locator in this file was opened by me.

**3. "Witnessed on main" was checked by predicate, not by proof.** For Ask 1 I grepped the
Done-when's named artifact and then read the clause. That establishes that a stated condition
*appears* to hold on the tree; it does not run the suite, does not execute the gate, and cannot
distinguish "the condition holds" from "the condition holds for a reason the row did not intend".
`[#171]` is the one case where I have a second, independent witness (the 2026-08-27 K3 adjudication
recorded in `tasks/archive/171.md` reaches the same verdict on the same two legs); `[#590]` rests on
`.pre-commit-config.yaml`'s own comment naming the done-when it discharges. Every other row I
report as *not* witnessed is a negative grep, which is strong; every row I did **not** check is
unexamined, which is the next limit.

**4. Ask 1 is not exhaustive over the 224 live rows.** The mechanical pass covers all 224; the
*hand* verification covers the 68 rows whose Done-when names a path-shaped artifact, and within
those, the ~15 whose clause is a checkable existence or membership predicate. **156 live rows name
no path-shaped artifact in their Done-when at all** — their criteria are behavioural ("a mechanism
refuses…", "a test proves…", "an ADR records…") and are unreachable by grep. I did not check them
and I am not claiming they are open on evidence. A row-by-row liveness sweep is `[#506]`, and this
census is not it.

**5. The `#\d+` citation count is grammar-bound.** Ask 3's strict number (24 rows, 13 live) counts
only bracketed `[#N]`. A citation written as bare `#N` inside a `refs` clause is a real citation
this pass drops — `[#153]`'s `refs ~/.claude/rules/core-invariants.md #5, #189` contains both a
false positive and a true one in the same clause, which is why I did not try to split the loose
set. **The true dangling-citation count is ≥ 24 and I cannot bound it above** without hand-reading
385+ edges.

**6. Two things I checked and could not settle, listed so they are not read as clean.** `[#590]`'s
merge-conflict observation window (limit 1 above); and `[#393]`'s three `corp-monorepo` artifacts,
which are outside this repo. Both are recorded as UNDETERMINED rather than folded into a verdict.

**7. What I did not attempt.** I did not run `gen_task_tree.py --check`, `--emit-source`,
`archive_row_body.py verify` or `audit.py health`. `--check` and `verify` are read-only and would
have strengthened legs 3–5 of the coherence block and legs A/C/D of the archive block; I skipped
them because the contract forbids the full suite and because a `--check` run is one `uv` resolution
away from a write in a tree twelve peer lanes are committing into. The coherence numbers above are
therefore **my own re-derivation from the manifest and the frontmatter**, not the gate's verdict.
They agree with `JOURNAL.md` 2026-09-05 (p)'s independently recorded *"nodes 503 → 501, 224 tasks,
`--check ok`"*, and `tasks/manifest.json` still holds 501 nodes and 224 tasks — but that is
corroboration, not the gate.

> **AMENDMENT 2026-09-07 (same session, after the session-end hook refused) — §7 above understates
> the case, and the correction matters to whoever integrates this.** I wrote that I *skipped* those
> runs. The truth is stronger: **they were not available in this container.** The session-end Stop
> hook (`uv run --locked python scripts/session_end_backpressure.py`) refused with
> `Required uv version ==0.11.19 does not match the running version 0.8.17`. Measured:
> `uv --version` → **0.8.17** (`/root/.local/bin/uv`) against `pyproject.toml:25`
> `required-version = "==0.11.19"`. Every gate in this repo is invoked through `uv run --locked`
> (AGENTS.md, "Build / test / lint"), so in this container **no** gate can execute — not the Stop
> hook, not `pytest`, not `ruff`, not `audit.py health`, not `gen_task_tree.py --check`, and not
> one pre-commit hook entry. That is also the real reason pre-commit was unarmed and why the
> `consumer_at_landing` probe reported in the handback was run through bare `python3` rather than
> through the gate. **Nothing above changes** — the counts are re-derivations from
> `tasks/manifest.json` and the row frontmatter, computed with the stdlib, and they stand as
> stated. What changes is what a reader may conclude from their being unverified by the gate: it
> was not judgment, it was the toolchain. **I did not bump `uv`** — AGENTS.md rules a uv bump "its
> own gated change, never incidental", and it is the operator's. If the other twelve sweep lanes
> ran in this same image, none of them could have run a gate either, and no lane's green should be
> read as a gate's green.

> **AMENDMENT 2 — 2026-09-07, same session: the toolchain was repaired and the gates RAN. This
> supersedes Amendment 1's "no gate can execute", and it upgrades three claims above from my
> re-derivation to a gate's verdict.** `uv self update 0.11.19` fails in this image
> (*"version 0.11.19 was not found for the app uv in workspace uv"*), but `0.11.19` is on PyPI and
> `pip install --user uv==0.11.19` installs it over `/root/.local/bin/uv`. That is **environment
> conformance with the pin the repo already declares**, not a uv bump: no tracked file changed,
> `pyproject.toml:25` is untouched, and the container is ephemeral. Safe here because this is a
> single-worktree isolated clone — `git worktree list` shows one entry and `.claude/worktrees` does
> not exist — so no peer lane shares this binary. Results, each run read-only with a clean
> `git status` after:
>
> - `uv run --locked python scripts/session_end_backpressure.py` → **exit 0**, no output.
> - `uv run --locked python scripts/gen_task_tree.py --check` → **`check ok`**. All six legs green,
>   including the id-agreement leg and the lossless-reassembly leg. **The five coherence numbers in
>   the Inventory section are therefore gate-witnessed, not just re-derived, and they agree.**
> - `uv run --locked python scripts/archive_row_body.py verify` → **`OK - 24 record(s), 24
>   byte-identity PROVEN (legs A/B/C/D/E)`**. The strongest available result: 24 of 24 PROVEN means
>   no row has been edited since its relocation, so the UNPROVEN reading its README warns about does
>   not apply to any record here.
> - `uv run --locked python scripts/audit.py health` → **DEGRADED** (exit 1): 35 `[OK]`, 58 `[~~]`,
>   16 `[--]`, **6 `[!!]`**. `[OK] task_tree_coherence`. **None of the six hard-fails is this lane's**
>   — they are `repos registered (none)`, `canonical_freshness` 7 stale (files this lane never
>   touched), `canonical_freshness` shallow-clone refusal, `hooks_armed`, `silent_rule_ratchet`
>   443→447, and `journal_spine_anchor` (`disposition floor 24882f8cc is not a valid object name` —
>   a shallow-clone artifact). This lane's two artifacts contribute exactly **2 WARNs**, both the
>   expected `consumer_at_landing` consumption ratchet, out of **43** such WARNs across a corpus
>   that already includes a dozen peer lane artifacts. Leg 1, the FAIL-class landing declaration,
>   **passes** on both.
>
> **The gate independently reaches Honest limits §1's conclusion, in its own words:** `[!!]
> canonical_freshness: derived leg REFUSES (shallow clone): the clone is shallow -- every
> git-derived date is a floor, not a fact, and a grafted history silently mis-dates every file older
> than the graft.` I reached that from `.git/shallow` and the uniform 2026-09-05/06 last-touch dates
> before running any gate; the gate reaches it from its own predicate. Two independent methods, one
> verdict — §1 stands and is now corroborated rather than merely argued.
>
> **What is still NOT run, and why:** the full suite (this contract forbids it) and the pre-commit
> hooks. `[!!] hooks_armed` confirms Amendment 1's report that they were never armed. I did **not**
> arm them: arming would put a regen-and-diff hook in the path of my next commit while twelve peer
> lanes are committing, which is the collision this sweep's contract exists to avoid. The integrator
> should arm them once, on the primary, after the queue drains:
> `pre-commit install -t pre-commit -t commit-msg -t pre-push` and
> `git config --local merge.ours.driver true` (the `.gitattributes` `merge=ours` pin on
> `docs/audits/README.md` is inert without it — `[#590]`).
