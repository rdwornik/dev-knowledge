# Night-3 lane C — the WARN ledger: path to zero, a `doc_rot` amendment, and the lane-grammar row

- **Class:** verification (ADR-101 R3 enum) · **Date:** 2026-08-15 · **Slug:** night3-warn-ledger
- **Status:** **DRAFT** — proposals only. Nothing here was applied: no register entry written, no
  row born, no detector edited, no test changed. Every act below needs an architect ruling.
- **Lane:** night-3 C, branch `claude/night3-warn-ledger-audit-fgreiw`, read-only.
- **Input:** the batch-5 end-of-batch packet
  `docs/audits/2026-08-15-technical-batch-phase1-packet.md` §3 (WARN attribution) and §6 (the
  owned `doc_rot` delta); lane R's filed `[#523]` young-row observation; the batch-4
  `lane-a-514-lane-regex` filesystem orphan.
- **Deliverables:** (1) path-to-zero ledger for the 36 WARNs, with `undeclared_edges` sampled
  edge-by-edge · (2) ONE `doc_rot` detector amendment covering three measured defect classes,
  plus a folded `stale_worktrees` leg · (3) the W3 lane-grammar row draft + mechanism sketch ·
  (4) the `routine_consumers` 1-vs-2 adjudication.

---

## 0. Measurement environment — read this before reading a number

This lane ran in an **Anthropic cloud container on a shallow clone**, not on the operator's
machine. That changes what is measurable, and the difference is stated up front rather than
discovered in the middle of a table.

```
git rev-parse --is-shallow-repository  -> true
git rev-list --count HEAD              -> 283      (the operator's main is far deeper)
git cat-file -t 24882f8cc              -> fatal: Not a valid object name
git worktree list                      -> primary only (the 7 lane worktrees are not here)
pre-commit hooks                       -> not armed (fresh clone)
```

**What this means per check, honestly:**

| Check | Reproduces here? | Why |
|---|---|---|
| `doc_rot` (7) | **YES — exactly** | reads `BACKLOG.md` text only; no git, no host |
| `undeclared_edges` (20) | **YES — exactly** | reads tracked `.md` text only |
| `reconciled_versions` (1) · `preflight_backlog_ids` (1) | **YES — exactly** | file-local |
| `no_ff_merges` | **NO** — 1 here vs 3 in the packet | needs full first-parent history |
| `git_backlog_drift` (`#505`) | **NO** — passes here | needs full history to see the closing commit |
| `journal_spine_anchor` | **NO** — hard FAIL here | the ADR-85 floor `24882f8cc` is not in a shallow clone |
| `review_artifact_coverage` | **NO** — 1 here vs 2 | merge window differs |
| `stale_worktrees` | **NO** — passes vacuously | no worktrees registered in this container |

**29 of the packet's 36 WARNs reproduce byte-for-byte here** (`doc_rot` 7 + `undeclared_edges` 20
+ `reconciled_versions` 1 + `preflight_backlog_ids` 1). Those 29 carry live evidence below. The
other 7 are taken from the packet's attribution and are **cited, not re-measured** — each is
marked `[packet]` in the ledger.

**A coincidence worth defusing so nobody mistakes it for confirmation:** this container's
`audit.py health` also totals **36 WARNs** — but with a *different composition* (it gains
`fleet_parity` ×4 and `deployed_methodology_version` ×1 from the unarmed fresh clone, and loses
history-dependent findings). The two 36s are not the same 36. Do not read the match as
agreement.

---

## 1. The 36 WARNs — the concrete path to zero

### 1.1 The reframe: there are TWO targets, and only one of them is at 36

This is the single most load-bearing finding in the ledger, and it changes the whole shape of
the work.

`ecosystem/disposition-register.yaml` holds 29 entries. **`audit.py ship-gate` applies them;
`audit.py health` does not.** The register's own header says it: *"`audit.py ship-gate` runs the
verification organs against the feature arc and BLOCKS /ship on red … A WARN BLOCKS unless an
entry here dispositions it."* `health` has no dispositioning pass at all — the only check that
consults the register from *inside itself* is `check_landing_predicate`, and its docstring
explains exactly why it had to: *"audit-health … is FAIL-only and never runs ship-gate's
dispositioning pass, so a check that wants a dated exemption to actually suppress a pre-commit
block has to consult the register itself."*

Measured live, this container, same tree:

```
audit.py health     -> 36 WARNs                (register NOT applied)
audit.py ship-gate  -> 23 [disp] + 13 undispositioned
```

So the 36 is a **health-surface count**, and 23 of the 36 are already adjudicated. Chasing "36 →
0" as one number is chasing a number nothing gates on. The two real targets are:

- **Target A — ship-gate green:** drive the **13 undispositioned** WARNs to zero (by fix or by
  ruled disposition). This is the number that blocks `/ship`.
- **Target B — health quiet:** drive the raw 36 down. Only reachable by *fixing* or by *changing
  the detector*, never by dispositioning — which is the honest reason the health count stays
  high while the gate is clean.

**Neither target is served by dispositioning `undeclared_edges` again — all 20 already are.**

### 1.2 The ledger

Per-class, with the concrete path to zero. `[live]` = measured in this container; `[packet]` =
cited from the batch-5 packet, not re-measured here.

| # | WARN class | n | Already dispositioned? | Path to zero | Kind |
|---|---|---|---|---|---|
| 1 | `undeclared_edges` | 20 `[live]` | **YES — 20/20**, all `ref: #241` | **Nothing owed at the gate.** For health: 3 DECLARE acts + 17 permanent-defer re-annotations. §1.3 | **detector + acts** |
| 2 | `doc_rot` backlog-accretion | 7 `[live]` | **NO — 0/7**; the register holds no `doc_rot` entry | **Dies with the §2 amendment: all 7 are false positives of the class the detector names.** Interim: 7 paste-ready entries below | **detector amendment** |
| 3 | `review_artifact_coverage` | 2 `[packet]` | 1 of 2 (`warn-review-artifact-387b794a-repin-close`) | **Act.** Land a canonical `docs/audits/2026-08-15-codex-<slug>.md` carrying a `**Tally:**` header, OR disposition the 4 batch-5 merges with the Downloads file as the named artifact of record. W9 — this is a decision, not hygiene | **act (operator)** |
| 4 | `no_ff_merges` | 3 `[packet]` | **YES — 3/3** (`3a894eeb5`, `d0f9ead67`, `533109f20`) | **Zero — permanently.** Immutable June history; unfixable without a rewrite, which is forbidden. Never revisit | **done** |
| 5 | `git_backlog_drift` `#505` | 1 `[packet]` | **YES** (`warn-git-backlog-drift-505-zero-closed`) | **Dies when `[#505]` closes.** Verified pre-existing in the packet (closing commit is an ancestor of the base) | **wave-2 / row close** |
| 6 | `journal_spine_anchor` mention-not-record | 1 `[packet]` | **YES** (`warn-journal-spine-anchored-by-mention`) | **Zero by design.** Advisory SHAPE leg, WARN by ruling (`STANDING_RULINGS` L-10); it never changes the hard verdict | **by design — leave** |
| 7 | `reconciled_versions` | 1 `[live]` | **YES** (`warn-reconciled-versions-contributing-template`) | **Act, one line.** `templates/CONTRIBUTING-md-template.md:3` holds the literal placeholder `reconciled_with: handoff-process@<version>`. It is a *template*, so the placeholder is correct — the fix is a detector carve-out for `templates/*-template.md`, not a value | **detector (1-line)** |
| 8 | `preflight_backlog_ids` | 1 `[live]` | **YES** (`warn-preflight-backlog-ids-310-292`) | **Act, one row.** `[#310]`'s `kill-candidates:` names `#292`, which is no longer open. Re-point or re-word `#310`'s clause | **act (1 row)** |

**Totals: 36 · 23 dispositioned · 13 undispositioned.** Of the 13, **7 are `doc_rot`** — so
**§2's amendment alone clears 54% of the ship-gate's blocking set**, and it clears it by
correcting a detector rather than by paperwork. That is the highest-leverage single act in this
ledger.

**Six stale register entries surfaced in this container** (ADR-75 decoration rule) — but **five
of them are artifacts of the shallow clone** (`no_ff` ×3, `review-artifact-lane-c-504`,
`git-backlog-drift-505`) and are almost certainly live on the operator's machine. The sixth,
`warn-journal-spine-anchored-by-mention`, is stale here only because the check hard-FAILs on the
missing floor object. **Do not prune any of the six on this container's evidence** — re-run
`ship-gate` on a full clone first. Recorded because a reader seeing `[stale]` in a night-lane log
would otherwise act on it.

### 1.3 Special depth — `undeclared_edges` (20), the largest inherited class

#### The finding that reframes it: the class is already fully adjudicated

All 20 carry a register entry with `ref: #241`, and **zero of the 20 are stale** — every
`match:` string still binds to a live WARN. The register is doing its job precisely.

`[#241]` is the owning row, and it already prescribes the discharge shape: *"DECLARE the
genuinely version-coupled current refs … and PERMANENTLY-DEFER the analogy / ticket / pointer
refs with a recorded reason."* Its Done-when is even denominator-proof: *"the predicate reads
the live surfaced set, never a fixed count."*

**But the row's prose is stale where its Done-when is not.** It says *"adjudicate the **6**
tier-1 candidates … (BACKLOG / VISION / AI_COUNCIL_PROCESS / ESSENTIALS / PLAYBOOK /
SESSION_SETUP → handoff-process)"*. Measured against the ADR-80 baselines:

```
2026-07-31 baseline : 10 distinct edges, ALL -> handoff-process
2026-08-15 (today)  : 20 distinct edges — the same 10, plus 10 -> prompt-template
```

**The class doubled in one commit.** Registering `prompt-template` in `_SPEC_REGISTRY` on
2026-08-09 (ARC-1) minted 10 new WARNs by construction — and the registry comment shows the
author knew: *"no doc declares a `reconciled_with: prompt-template@…` edge yet."* Registration
was the right act (it arms `coherence_nudge` on the template's edits, and the template's version
had moved 1.6 → 1.13 with no organ watching). **The mint was unavoidable and unaccounted-for.**
This is the same shape as §2's minted-loci class, in a different organ — which is why §2 treats
it as a class rather than a `doc_rot` quirk.

#### Every edge, sampled and classified

All 20, each with its strongest evidence line, grouped by defect kind.

**K1 — GENUINE COUPLING, currently STALE (3 edges). The strongest case in the ledger: these
undeclared edges are masking live version drift right now.**

| Edge | Evidence (live line) | Drift |
|---|---|---|
| `protocols/PLAYBOOK.md` → `handoff-process` | L1183 **"Authoritative spec: `protocols/HANDOFF_PROCESS.md` v5 — the single live source of truth"**; L3716 "Operational authority: … v5" | spec is **6.2.0** |
| `protocols/SESSION_SETUP.md` → `handoff-process` | L191 "follow HANDOFF_PROCESS **v5**"; L203 "**Mechanics live in `protocols/HANDOFF_PROCESS.md` (v5 — the single source of truth)**" | spec is **6.2.0** |
| `protocols/PLAYBOOK.md` → `prompt-template` | L1739 "`templates/prompt-template.md` **(v1.7)** carries a separate ~10 ceiling" | template is **1.14** |

PLAYBOOK L1111 states the governing rule in its own text — *"A doc that declares a dependency on
a versioned spec must not drift from it"* — three lines of doctrine away from asserting v5 about
a v6.2.0 spec. `CLAUDE.md` declares `reconciled_with: handoff-process@6.2.0` and is correctly
absent from the scan, which proves the declared path works. `[#367]` already names this exact
failure mode for the *declared* case.

**K2 — LOCATOR / POINTER, no version claim (5 edges) → PERMANENT-DEFER.**
`VISION.md`→`handoff-process` (L162, one "per HANDOFF_PROCESS.md" pointer) ·
`protocols/ESSENTIALS.md`→`handoff-process` (L133 "**Browser chat checkpoint:** … → see
**HANDOFF_PROCESS.md**") · `protocols/HANDOFF_BOOT.md`→`prompt-template` (L213 "it lives in
PLAYBOOK §2 + templates/prompt-template.md") · `protocols/HANDOFF_PROCESS.md`→`prompt-template`
(L704, spec-to-spec carrier pointer) · `protocols/STANDING_RULINGS.md`→`prompt-template` (L278,
a ruling's carrier clause). A pointer says *where*, never *what version*.

**K3 — ANALOGY or EXAMPLE-OF-A-PROBLEM (2 edges) → PERMANENT-DEFER.**
`protocols/AI_COUNCIL_PROCESS.md`→`handoff-process` (L62 "the same pattern as HANDOFF_PROCESS" —
an analogy) · `VISION.md`→`prompt-template` (L20 "templates/prompt-template.md and some ADR
examples cite absolute paths" — the template is named as an *instance of a defect*, the inverse
of a dependency).

**K4 — WORK-ITEM POINTERS in a GENERATED file (2 edges) → STRUCTURALLY UNDECLARABLE.**
`BACKLOG.md`→`handoff-process` (15 sites, all task rows naming the file they *plan to change* —
`[#359]`, `[#399]`, `[#404]`, `[#422]`…) · `BACKLOG.md`→`prompt-template`. Two independent
blockers: a ticket naming its target is not a content dependency, **and** `BACKLOG.md` is
generated from `tasks/` since the ADR-107 strangler flip, so a hand-authored frontmatter edge
would be destroyed by the next `gen_task_tree.py --emit-source`.

**K5 — GENERATED INDEX inheriting a title (1 edge) → STRUCTURALLY UNDECLARABLE.**
`docs/intake/README.md`→`handoff-process` — L51 is inside the `INTAKE-INDEX` generated block,
rendering the v6-proposal's *title*. The file carries "Do not hand-edit between the markers"; a
declaration would have to be emitted by `gen_intake_index.py`.

**K6 — DATED RECORD / not-yet-coupled proposal (7 edges) → DEFINITIONALLY UNDECLARABLE.**
All seven are `docs/intake/*`: the v6-proposal (→ both specs), the night-shift design input
(whose only hit is a **cross-reference to a sibling intake's filename** — an intake→intake edge,
not doc→spec at all), the 2026-07-30 orientation snapshot, the simplification-wave erratum, the
adoption-consolidation ledger row (which cites "v1.6 … at `12dbb65a`" — a state *at a commit*,
deliberately historical), and the verification-organ intake. An intake doc records what was true
or proposed **on a date**; `reconciled_with` asserts currency it never claimed.

**Tally: K1 3 · K2 5 · K3 2 · K4 2 · K5 1 · K6 7 = 20.** By target: 10 → `handoff-process`,
10 → `prompt-template`.

#### The discharge shape — compared, with a recommendation

| Option | What it is | Verdict |
|---|---|---|
| **A — batch declaration** | one act adding `reconciled_with` to all 20 | **REJECT.** 12 of 20 (K4+K5+K6) *cannot* carry one — two are generated, seven are dated records. It would also commit 5 pointer docs to permanent version-coupling they don't have, manufacturing future `reconciled_versions` churn |
| **B — per-edge acts** | 20 individually-ruled acts | **PARTIAL — right for K1 only.** 3 acts, each fixing real drift. For the other 17 it is 17 rulings to re-affirm what the register already says |
| **C — detector amendment** | teach the scan the kinds | **PARTIAL — right for K4+K5 (3 edges).** A generated file cannot carry a hand-authored edge; that is a property of the corpus, not a judgment call, so it belongs in code. `_is_immutable_artifact` already has the exact hook: extend it to prune files declaring `generates:`/`generated by` |
| **D — A+B+C split by kind** | **RECOMMENDED** | 3 DECLARE acts (K1) · 3 detector prunes (K4+K5) · 14 re-annotated permanent-defers (K2+K3+K6) |

**Under D the path to zero is: health 20 → 3 → 0.** The 3 detector prunes drop it to 17; the 3
K1 declarations (which are *drift fixes*, not paperwork) drop it to 14; the remaining 14 stay as
permanently-recorded defers — visible in the register, silent at the gate, which is the correct
terminal state for a class whose members are structurally undeclarable.

**The one sequencing hazard, stated because it will bite:** `VISION.md` and
`protocols/ESSENTIALS.md` are `canonical_freshness`-gated. `[#241]` already flags it — *"VISION /
ESSENTIALS declarations must ride a genuine freshness re-stamp"*. Both land in K2 (permanent-
defer), so under D neither is touched and the hazard does not arise. Worth stating that this is
**why** they are K2 and not a convenient dodge: their evidence lines really are bare pointers.

#### Paste-ready register entries — live schema

The 20 `undeclared_edges` entries **need no new writes**. What is undispositioned at the gate is
`doc_rot` ×7, so those are the paste-ready entries below (§2.6), written as an **interim** while
the amendment is ruled — not as the answer.

The one `undeclared_edges` register change worth proposing is a **re-annotation**, not a new
entry: the three K1 entries currently say "a likely DECLARE outcome, deferred". If D is ruled,
they should be **removed** at the same commit that adds the `reconciled_with` lines, so the
ADR-75 decoration rule surfaces any that were missed.

---

## 2. `doc_rot` detector design memo — one amendment, three defect classes

### 2.1 The three measured classes

**Class 1 — minted-loci-by-ruled-legs** (packet §6; `[#529]`, `[#530]`). Architect rulings R2 and
R7 *required* leg text on two rows. Measured before the edit: `#530` sat **1 char** under the
1320 ceiling, `#529` sat **27** under. Any compliant leg text minted a locus. Three avoidance
routes were tried and all failed — `gen_task_tree` refused the `[#480]` below-the-row shape
outright (*"a task is ONE physical line"*, ADR-107 §2), trimming saved one locus of eight, and
only `[#293]` had headroom. **The detector taxed compliance with a ruling.**

**Class 2 — the `[#523]` young-row misfire** (lane R, filed as instructed). `[#523]` was born
**2026-08-12** and flagged for *history-accretion* on **2026-08-15**. Its 1738 chars are birth
content plus one 2026-08-14 leg. Lane R's contract anticipated it precisely: *"if the accretion
metric misfires on young rows → EXCLUDE #523 from the drain, and write the finding (metric
misfire on <p-age rows) into the packet."*

**Class 3 — dated-tokens-in-citations** (packet §6 item 3, `[#293]`). `_DATE_RE` is a bare
`\d{4}-\d{2}-\d{2}`, so a citation of `docs/audits/2026-08-15-technical-…md` contributes a "dated
block". Under the repo's **own** naming convention (CLAUDE.md §4: `YYYY-MM-DD-slug.md` for every
dated artifact), *every* citation of an audit, handoff or intake file is guaranteed to inject a
phantom date. The packet records `[#293]` tripping on **dates, not length**, cleared only by
rewording the citation — i.e. **the detector taxed citing evidence.**

### 2.2 The measurement that unifies them

Measured across all **195** live task rows.

**(a) Citation pollution is corpus-wide.** 59 of 195 rows (**30%**) carry ≥1 date token that is
part of a filename. Its effect on the date arm:

```
rows firing (>=3 RAW dates AND >700 chars)                : 5
rows firing (>=3 CITATION-BLIND dates AND >700 chars)     : 2
```

**(b) The gross-length arm is a percentile ranker, and its calibration went stale the same day
it was set.** D1.1 raised the ceiling 1200 → 1320 on the morning of 2026-08-15, calibrated as
**p90** of the then-live distribution. Measured tonight on the post-drain tree:

```
1320 sits at rank 188/195 = p96.4 of the CURRENT distribution
```

The source comment already concedes the shape of the problem — at 1200 *"it was ranking the top
fifth of an ordinary distribution, not detecting outliers."* The fix chosen was a higher
percentile. **A percentile always has members by construction**, so no percentile turns a ranker
into a detector; and lane R's own drain shifted the distribution out from under the new number
within hours.

**(c) The decisive one — the detector has INVERSE correlation with the class it names.** Counting
distinct, citation-blind, non-future dates per row:

```
distinct history dates : 0 -> 89 rows | 1 -> 83 | 2 -> 22 | 3 -> 1
```

Exactly **one** row in the whole corpus carries ≥3 distinct citation-blind history dates
(`#492`, span 6 days). And the 7 current loci, under a time lens:

```
#514  2420ch  1 date   span  0d      #529  2001ch  1 date   span  0d
#530  1871ch  1 date   span  0d      #523  1738ch  2 dates  span  2d
#528  2397ch  2 dates  span  1d      #419  1908ch  2 dates  span  5d
#492  1807ch  3 dates  span  6d
```

**Every one of the seven has a history span of ≤10 days.** Meanwhile the widest-span rows in the
corpus — `#102` (49d), `#293`/`#171`/`#239`/`#297`/`#82` (33d) — are **not** loci, at 537–1272
chars.

So: the check named `backlog-accretion`, whose doctrine is ADR-65/49 *"condense inline history to
git"*, **is firing on the seven longest rows, all of which are young, and firing on none of the
eight rows with the widest date spans.** It measures length and reports recency. All three defect
classes are symptoms of that one root cause: **the predicate uses current text size as a proxy
for accreted history, and the proxy has three independent leaks.**

### 2.3 The amendment — exact predicate change

The unifying insight is that the detector conflates **two different contracts under one name**.
Split them; each then becomes checkable.

```python
# --- BEFORE (scan_backlog_accretion, validate_doc_rot.py:99-115) -------------
dates  = len(_DATE_RE.findall(line))
length = len(line)
if (dates >= _BACKLOG_DATED_BLOCKS and length > _BACKLOG_LONG_CHARS) \
        or length > _BACKLOG_GROSS_CHARS:
    out.append(RotFinding("backlog-accretion", f"BACKLOG#{m.group(1)}", ...))

# --- AFTER --------------------------------------------------------------------
# (c) citation-blind: a date inside a `YYYY-MM-DD-slug` artifact identifier is an
#     IDENTIFIER, not an inline history entry. One regex, applied before counting.
_ARTIFACT_DATE_RE = re.compile(
    r"[A-Za-z0-9_./-]*/\d{4}-\d{2}-\d{2}-[A-Za-z0-9_.-]+"   # path-qualified
    r"|\b\d{4}-\d{2}-\d{2}-[a-z0-9][A-Za-z0-9_.-]*")        # bare bundle-dir name

_MIN_ACCRETION_SPAN_DAYS = 30     # NEW — the time term the predicate never had

history = sorted({d for d in _DATE_RE.findall(_ARTIFACT_DATE_RE.sub(" ", line))
                  if date.fromisoformat(d) <= today})       # future re-check pegs dropped
span = 0 if len(history) < 2 else (date.fromisoformat(history[-1])
                                   - date.fromisoformat(history[0])).days

# ARM 1 — backlog-accretion: the ADR-65/49 class, now with its time term.
if len(history) >= _BACKLOG_DATED_BLOCKS \
        and span >= _MIN_ACCRETION_SPAN_DAYS \
        and length > _BACKLOG_LONG_CHARS:
    out.append(RotFinding("backlog-accretion", ...,
                          f"{len(history)} history dates spanning {span}d, {length} chars"))

# ARM 2 — backlog-row-length: RENAMED, because it was never accretion.
if length > _BACKLOG_ROW_CEILING:
    out.append(RotFinding("backlog-row-length", ...,
                          f"{length} chars (declared ceiling {_BACKLOG_ROW_CEILING})"))
```

**Three coupled changes, one coherent idea — measure what the name claims:**

1. **Citation-blind counting** (Class 3). A date inside an artifact identifier is a name, not a
   history entry.
2. **A span term + future-date drop** (Classes 1 & 2, together). Accretion is a *time-extent*
   property. This kills the young-row misfire **and** the ruled-legs mint with one term, and it
   needs no new frontmatter field and no git call: **a row's own oldest history date is its age
   proxy**, already in the text. (Checked: `tasks/*.md` frontmatter carries no birth date, so
   deriving age any other way would mean a new field or a git walk — library-first says use the
   data already present.)
3. **Rename the length arm and re-ground its ceiling** (Class 1's other half). `1320` stops being
   a rolling percentile and becomes a **declared contract**, exactly like `CLAUDE.md`'s ≤200 lines
   in `_FILE_SIZE_BUDGETS` — a number ADR-107 or the BACKLOG header states, that a row can be
   held to and a ruling can knowingly exceed.

**What the rename buys, and it is the point:** `#529`/`#530` stop being reported as *rot*. They
are reported as *long*, which is true, and a ruled leg is a legitimate reason to be long. That
converts an unanswerable accusation ("this row has rotted") into an answerable one ("this row is
over the declared ceiling — accepted, ruled R2/R7"). **A disposition against `backlog-row-length`
is honest; a disposition against `backlog-accretion` was a false confession.**

### 2.4 False-positive analysis

**The citation regex — measured, zero false strips.** Every token it removes across all 195 rows:

```
distinct tokens stripped : 51
  ...carrying a path separator ('/')  : 50
  ...without                          :  1   -> `2026-07-02-ai-council-architect`
```

The single path-less token is a **handoff bundle directory name** — still a dated-artifact
identifier, correctly stripped. **False-strip rate on the live corpus: 0/51.** Residual risk is
prose of the form `2026-08-10-to-08-12`; none exists today, and the failure mode is *under*-
counting a date, which loses recall on a class that currently has one member — a cheap direction
to be wrong in.

**The span term — the honest cost.** Under the amended ARM 1, calibrated:

```
N>=3 dates, span>=30d, >700ch  -> 0 rows
N>=3 dates, span>=14d, >700ch  -> 0 rows
N>=3 dates, span>= 0d, >700ch  -> 1 row  (#492, span 6d)
N>=2 dates, span>=30d, >700ch  -> 5 rows (#293 #298 #297 #82 #102)
```

**ARM 1 fires on ZERO rows today, and that is the finding, not a bug.** The ADR-88 FC4 history-
accretion class **has no live instances**: lane R drained the corpus 11 → 5, and what remains is
long-and-young, not accreted. A detector reporting zero on a clean corpus is *correct*; the
current one reports seven by mislabeling them.

**This is the amendment's one real risk and it is named rather than buried:** an arm that fires on
nothing is indistinguishable from an arm that is broken. Two mitigations, both cheap:
- **ARM 2 keeps the surface alive** — the length contract still reports, so the operator never
  loses backpressure. The amendment moves 7 findings from a wrong label to a right one; it does
  not go silent.
- **Pin ARM 1 with a fixture**, not with live data (`tests/fixtures/`), so "fires on zero" is
  proved to be *the corpus being clean* rather than *the arm being dead*. Without this the
  amendment is unfalsifiable, and it should not be ruled in without it.

If the architect judges a zero-firing arm unacceptable, the fallback is `N>=2, span>=30d` (5
rows) — but those 5 are 537–1272 chars, i.e. **ordinary rows citing two dates a month apart**,
and flagging them would re-import the precision problem at the other end. Recommendation: take
the zero, take the fixture.

### 2.5 Folded leg — `stale_worktrees` is blind to filesystem-only orphans

**The gap, stated exactly.** `check_stale_worktrees` reads `_git_linked_worktrees`, i.e. `git
worktree list --porcelain` — **git's registry**. It can therefore see a worktree that is
*registered but gone from disk* (it says so, and handles it). It structurally **cannot** see the
inverse: a directory that is **on disk but not registered**. That is the batch-4
`lane-a-514-lane-regex` orphan.

**Why the sibling check does not cover it either** — and this is the part that makes it a real
hole rather than an overlap. `check_no_sibling_orphans` looks for `<repo>-*` **siblings** next to
the repo (the `.dev-knowledge-cadence` failure of 2026-06-02). But the live provisioning path
puts worktrees **inside** the repo: `/lane-boot` step 2 and PLAYBOOK L1541 both land them in
`.claude/worktrees/<name>/`. So the two organs miss it for **different reasons** — one looks in
the right place with the wrong source (git's registry), the other uses the right source with the
wrong place (siblings). Nothing looks at `.claude/worktrees/` on disk.

`.gitignore:22` ignores `.claude/worktrees/`, so `git status` never surfaces it either. **The
orphan is invisible to every organ in the tree.**

**Proposed leg — a third finding from the same organ, mirroring the stash leg's precedent:**

```python
_WORKTREE_HOME = ".claude/worktrees"

def _orphan_dir_findings(repo_path: Path, registered: set[Path]) -> list[Finding]:
    """Directories under .claude/worktrees/ that git does NOT register.

    The inverse of the registered-but-gone case above: `git worktree list` cannot
    report a directory it has no record of. Reuses `_git_registered_worktrees`
    (the flat path set) + `_looks_like_worktree_remnant` -- the same two helpers
    `check_no_sibling_orphans` already composes, applied at the location the live
    provisioner uses (`/lane-boot` step 2, PLAYBOOK L1541) instead of at siblings.
    """
```

Same WARN tier, same `precision-over-recall` gate as the sibling check (**NOT registered** AND
remnant-shaped), so an in-flight lane is never flagged. Library-first: **no new helper** — both
already exist and are already composed this way one function above.

**Honest limit:** it catches an orphan under `.claude/worktrees/` only. A worktree provisioned to
an arbitrary path (the superseded `git worktree add ../…` recipe) stays invisible, and the
detector should say so rather than imply full coverage.

**Recommended home:** a **leg on `[#505]`** (which already owns batch hygiene and this organ),
not a new row — it is the same organ closing the same class from the other side.

### 2.6 Interim paste-ready register entries — `doc_rot` ×7

For use **only if** the amendment is deferred and the gate must go green first. Keyed on the
full signature including the char count, per the register's own precision-over-recall rule, so
**any growth in these rows re-surfaces and re-blocks**.

```yaml
  # ---- doc_rot backlog-accretion, INTERIM (night-3 lane C, 2026-08-15) ----
  # All seven are false positives of the class the detector names: every one has a
  # citation-blind history span of <=10d (measured), while the corpus's widest-span rows
  # are not loci. Superseded by the validate_doc_rot amendment (this audit S2.3) --
  # these entries retire at that commit and ADR-75 decoration will surface any missed.
  - id: warn-doc-rot-backlog-529-ruled-legs
    organ: doc_rot
    match: "BACKLOG#529 (3 dated block(s), 2001 chars"
    ref: "[#529] / batch-5 packet S6"
    reason: >-
      Minted by ruling R7, not by rot. The row sat 27 chars under the 1320 ceiling; the four
      required legs crossed it. History span 0d (all dates 2026-08-15, one of them a filename
      citation). Detector taxing compliance with a ruling.
    auto_clearable_by: validate_doc_rot span-term amendment
  - id: warn-doc-rot-backlog-530-ruled-legs
    organ: doc_rot
    match: "BACKLOG#530 (3 dated block(s), 1871 chars"
    ref: "[#530] / batch-5 packet S6"
    reason: >-
      Minted by ruling R2. The row sat ONE char under the ceiling before the two required P1
      legs. History span 0d. Same class as #529.
    auto_clearable_by: validate_doc_rot span-term amendment
  - id: warn-doc-rot-backlog-523-young-row
    organ: doc_rot
    match: "BACKLOG#523 (2 dated block(s), 1738 chars"
    ref: "lane R filed finding, 2026-08-15"
    reason: >-
      Young-row misfire, filed by lane R under its contract item 0b. Born 2026-08-12, flagged
      for history-accretion on 2026-08-15; the text is BIRTH content plus one 2026-08-14 leg.
      Span 2d. Fires on the gross-length arm only.
    auto_clearable_by: validate_doc_rot span-term amendment
  - id: warn-doc-rot-backlog-514-length-only
    organ: doc_rot
    match: "BACKLOG#514 (1 dated block(s), 2420 chars"
    ref: "[#514]"
    reason: >-
      ONE date in 2420 chars -- the longest row in the corpus and the clearest proof the gross
      arm is a length ranker, not an accretion detector. Span 0d.
    auto_clearable_by: validate_doc_rot arm rename + declared ceiling
  - id: warn-doc-rot-backlog-528-young-row
    organ: doc_rot
    match: "BACKLOG#528 (5 dated block(s), 2397 chars"
    ref: "[#528] / batch-5 packet S6"
    reason: >-
      5 raw dates, but 2 are filename citations; 2 distinct history dates spanning 1d. Grew
      under R7 having already been a locus.
    auto_clearable_by: validate_doc_rot span-term amendment
  - id: warn-doc-rot-backlog-492-hot-row
    organ: doc_rot
    match: "BACKLOG#492 (7 dated block(s), 1807 chars"
    ref: "[#492]"
    reason: >-
      7 raw dates reduce to 3 distinct history dates spanning 6d once 2 filename citations and
      1 FUTURE re-check peg (2026-08-17) are excluded. A hot row under active adjudication, not
      an accreted one. The corpus's only row with >=3 citation-blind history dates.
    auto_clearable_by: validate_doc_rot span-term amendment
  - id: warn-doc-rot-backlog-419-length-only
    organ: doc_rot
    match: "BACKLOG#419 (3 dated block(s), 1908 chars"
    ref: "[#419]"
    reason: >-
      3 raw dates reduce to 2 distinct history dates spanning 5d after one filename citation is
      excluded. Fires on the gross arm.
    auto_clearable_by: validate_doc_rot span-term amendment
```

**Recommendation: rule the amendment, do not paste these.** Seven dispositions to silence seven
findings the detector should not have made is the paperwork route, and it leaves the misfire
armed for the next ruled row update.

---

## 3. W3 — the lane-grammar row (provisioning enforcement)

### 3.1 The row draft

Third occurrence of the class (batch 4 W4/W6, batch 4 lane-a, batch 5 lanes S and R). Root cause
per the packet §1a: *"the lane grammar is enforced nowhere at provisioning"* — `validate_branch_
naming` is read-only and wired into no gate, and a lane dispatched straight through `claude
--worktree <name>` never passes `/lane-boot` step 1. The cost is silent: an off-enum name is
freely creatable, and **what it loses is the ADR-110 exemption** — which surfaces at the
integrator's merge queue, at merge #1 of 7, as a wedged pre-commit gate.

**Ready for the architect's birth ruling** (`[#NNN]` = next free id):

```
- [#NNN] [P2][S] **Lane-grammar enforcement at PROVISIONING — the enum is checkable but nothing
checks it** — `scripts/validate_branch_naming.py` transcribes the branch/worktree enum and is
wired into NO gate (its own docstring: "READ-ONLY, AND WIRED INTO NO GATE"); `/lane-boot` step 1
calls it, but a lane dispatched straight through `claude --worktree <name>` never reaches
`/lane-boot`. THIRD OCCURRENCE: batch-4 W4/W6 (resolved by dropping both lanes from the roster),
batch-4 `lane-a-514-lane-regex`, and batch-5 lanes S (`worktree-lane-s-w20-draft-landing`, id
slot reads `w20`) + R (`worktree-lane-r-gateclose-drain8`, no id slot) — where
`batch_manifest.is_lane_merge` REFUSED both, silently forfeiting the ADR-110 exemption and
surfacing as a would-be `check_journal_spine_anchor` FAIL at merge #1 of 7 (batch-5 packet §1a,
resolved by anchoring, not by renaming). The defect is not either name: an off-enum name is
freely creatable and loses the exemption without saying so. Wire the EXISTING validator at the
one point every provisioning path crosses — the `reference-transaction` git hook at the
`prepared` stage, measured to refuse `worktree-lane-w20-draft-landing` while admitting
`worktree-lane-a-505-batch-protocol` and leaving ordinary commits untouched (evidence:
`docs/audits/2026-08-15-verification-night3-warn-ledger.md` §3.2). · Done when: creating a
`refs/heads/worktree-lane-*` branch whose name is off-grammar is REFUSED at creation with the
reason, a conforming name is unaffected, non-lane ref updates are untouched, the escape is
explicit and non-silent, and `/lane-boot` step 1 is stated as the friendly pre-check rather than
the enforcement point · refs scripts/validate_branch_naming.py, scripts/batch_manifest.py,
.claude/commands/lane-boot.md, ADR-110, #505 · kill-candidates: none — [#505] owns batch hygiene
AFTER the fact (`check_stale_worktrees`, WARN-tier by ruling) and [#527] owns direct-to-main at
commit time; neither covers name conformance at provisioning, and the packet's W3 states no row
exists · serialize-group: gates
```

**Notes for the ruling.** (a) `kill-candidates: none — <reason>` is the form
`check_backlog_filing.py` Leg 1 accepts (`_KILL_RE`); the commit message must repeat it. (b)
Sized **S**, so the ADR-98 intake-id WARN (Leg 3, L-band only) does not apply. (c) `[P2]`: it has
cost a wedged merge queue once and near-wedged another, but it is a hygiene gate, not a
correctness one.

### 3.2 Mechanism sketch — library-first comparison, measured

All three candidates reuse `validate_branch_naming.LANE_BRANCH_RE` / `validate_lane_worktree_
name`. **No new grammar is authored in any option** — which matters, because the enum's own rule
is that a member enters "only via a recorded ruling, never silently."

| | **(a) `/lane-boot` step 1** | **(b) dispatch wrapper** | **(c) `reference-transaction` hook** |
|---|---|---|---|
| **Where** | command markdown, pre-provision | a PATH script wrapping `claude --worktree` | git, at ref-creation |
| **Reuse** | already calls `--lane` — zero new code | imports the module | imports the module |
| **Coverage** | only lanes booted *through the command* | only lanes booted *through the wrapper* | **every path**: `claude --worktree`, `EnterWorktree`, raw `git worktree add`, `git branch` |
| **Posture** | advisory; a model may skip a step | prevent, if invoked | **prevent — refuses at creation** |
| **Bypass** | don't run `/lane-boot` ← **the live failure** | don't run the wrapper | `git -c core.hooksPath=…` (explicit, loud) |
| **Status** | **shipped, and it is what failed** | not built | not built |

**Measured, not assumed** (git 2.43.0, throwaway clone in scratch, removed after — repo
untouched, `git status` clean, `git worktree list` primary-only):

```
git worktree add  ->  fires reference-transaction (prepared, committed) AND post-checkout
                      post-checkout $PWD = the NEW worktree dir; HEAD = the new branch

with a prepared-stage refusal wired to LANE_BRANCH_RE:
  A. worktree-lane-w20-draft-landing      -> REFUSED: fatal: ref updates aborted by hook
                                             branch created? NO
  B. worktree-lane-a-505-batch-protocol   -> branch created? YES
  C. ordinary `git commit`                -> unaffected
```

Case A is **lane S's actual branch name from batch 5**, refused at creation.

**Recommendation: (c), with (a) kept as the friendly pre-check.** Reasons, in order:

1. **It is the only option that closes the bypass.** (a) and (b) both enforce on a path the
   operator chooses to take; the witnessed failure is precisely a path not taken. A gate that the
   failure mode routes around is not a gate — the same argument the ADR-85 amendment made when it
   moved the hard leg off `Stop` and onto pre-push because *"an organ that can be exhausted cannot
   carry teeth."*
2. **Library-first: it adds no validator.** The grammar, the classifier and the error strings all
   exist. The hook is a ~20-line adapter.
3. **`post-checkout` is the wrong half.** It fires (measured), but *after* the worktree exists —
   detect, not prevent. It would leave the orphan §2.5 is about.

**Three costs, stated rather than discovered later.**

- **It is a hot path.** `reference-transaction` fires on *every* ref update — commits, fetches,
  resets, rebases. The adapter must exit 0 immediately unless `state == "prepared"` **and** the
  ref matches `refs/heads/worktree-lane-*` **and** `old == 0{40}` (creation only). Anything
  slower or broader degrades every git operation in the repo.
- **`pre-commit` cannot install it.** The framework's supported stages do not include
  `reference-transaction`; `.pre-commit-config.yaml:8` arms `[pre-commit, commit-msg, pre-push]`
  and `arm_hooks.py:29` mirrors that triple. So this hook needs a hand-installed shim, and
  `arm_hooks.py` + `check_hooks_armed` + the `hooks-armed` parity surface each grow a fourth type.
  **That is the real cost of (c), and it is an integration cost, not a design flaw** — but it
  should be priced into the ruling, not discovered at build time.
- **`--no-verify` does not apply here.** `git worktree add` has no such flag, so the escape is
  `core.hooksPath`. That is *more* explicit than `--no-verify`, not less — but it is also
  unfamiliar, so the refusal message must name it, the way `block_unanchored_push` names its own.

**If (c)'s hook-type cost is judged too high**, the honest fallback is **(a) + a detect backstop**:
keep `/lane-boot` step 1, and add an off-grammar `worktree-lane-*` branch as a WARN leg on
`check_stale_worktrees` alongside §2.5's orphan leg — same organ, same tier, both about lanes
that were provisioned wrong. That does not prevent; it makes the loss of the exemption *loud at
the next audit* instead of silent until the merge queue. It is strictly better than today.

---

## 4. `routine_consumers` 1-vs-2 — which is right

**Verdict: the LIVE COUNT (2) is right. The test pin (1) is stale and should move.**

**The evidence.** Two `BACKLOG.md` rows carry a complete ADR-105 six-field marker:

```
L275  [#348]  · routine: trigger=on-demand (operator/session boot) · scope=BACKLOG.md rows
              · consumer=any session reading BACKLOG.md · consumption_path=BACKLOG.md in place
L282  [#426]  · routine: trigger=operator night-batch request · scope=hub night-batch reports
              (branch-only) · consumer=the morning verification batch
              · consumption_path=branch-only night output -> local gates -> operator merge
```

`check_routine_consumers` PASSES both — each names a consumer and a consumption path, which is
the entire bar. **The check is behaving exactly as specified.**

**Why the second declaration is legitimate, not drift.** ADR-105 §2 gates at **ACTIVATION**: *"A
routine **may not ACTIVATE** without a named `consumer` and `consumption_path`."* The night-batch
routine is activated — **this lane is an instance of it running** — and it emits branch-only
reports consumed by the morning verification batch. Under §2 the marker on `[#426]` is not
optional; it is **required**. The marker landed 2026-08-10 with the ARC-9 rulings (`09020af`).
The count moved because the fleet correctly declared a newly-activated routine. **That is
ADR-105 working.**

**Why the test is the wrong surface to hold the line.** `tests/test_audit.py:2434`:

```python
f = aud.check_routine_consumers(root)      # <- the LIVE repo, not a fixture
assert "1 declared routine row" in f.evidence
```

Three defects, in ascending severity:

1. **It pins a dated observation as an invariant.** ADR-105 §4 says *"**At acceptance** this rule
   governs one row"* — a statement about a moment, deliberately so (§4 is titled "Coverage
   boundary — read this before reading a green check"). The test dropped "at acceptance" and kept
   the number.
2. **It reads live state in a unit test**, so any correct governance act can turn it red. The
   test's own docstring concedes the coupling: *"If this number moves, the ADR, the docstring and
   [#426] must move with it."* It moved; they did not.
3. **The assertion is a substring match, and it is weaker than it looks.** Verified:
   `"1 declared routine row" in "11 declared routine row(s) …"` → **`True`**. The pin **fails at
   2** but would **pass at 11, 21, 31**. It is not a count assertion at all — it is an assertion
   that the count's decimal representation ends in `1`. Whatever is ruled about the number, this
   line needs rewriting.

**A real question the fix must answer, flagged because it is a judgment call and not mine to
make:** `[#426]`'s subject is *"Declare `consumer` + `consumption_path` for every LIVE routine"* —
the retrofit — yet the marker it carries declares **the night-batch routine**, a different object.
That may be a **mis-homed declaration**: under ADR-105 §1 the marker is a row-shape for *the row's
own* routine. If the architect agrees, the fix is to move the marker to a row that owns the night
batch and the live count returns to 1 legitimately. If the architect reads `[#426]` as the row
that owns night-batch output until the retrofit lands, the count is 2 and stays 2.

**Proposed fix — the same four surfaces the test's docstring names, whichever way that goes:**

1. **`tests/test_audit.py:2434`** — replace the live-state pin with a **fixture** asserting the
   *behaviour* (N marked rows → `"N declared routine row"`), and add a **separate** live test
   asserting `f.status == "pass"` with **no** count. The count belongs in the ADR, not in a unit
   test. If a live count assertion is still wanted, make it exact (`f.evidence.startswith(f"{n} ")`),
   never a substring.
2. **`docs/decisions/ADR-105` §4** — an amendment marker recording the boundary moving 1 → 2 with
   the night-batch routine named (ADRs are immutable; §4's own text is dated "at acceptance", so
   an amendment is the correct instrument, not an edit).
3. **`check_routine_consumers` docstring** — *"which at acceptance is exactly ONE row ([#348])"* →
   the current set and the date it moved.
4. **`[#426]`'s row prose** — it opens *"ADR-105's activation gate governs exactly ONE backlog row
   ([#348])"*, which is now **self-falsifying: `[#426]` is itself the second**. This is the surface
   most worth correcting regardless of the marker-homing ruling.

**Ordering:** fix the test *last*. If the marker turns out to be mis-homed (surface 4's question),
moving it restores the count to 1 and surfaces 2–3 need no amendment at all — so ruling the
homing question first can make two thirds of this work disappear.

---

## 5. Final line

**Path-to-zero table** (`n` = health WARNs; `undisp` = undispositioned at ship-gate):

| Class | n | undisp | Path to zero | Dies with |
|---|---|---|---|---|
| `undeclared_edges` | 20 | **0** | 3 DECLARE acts (K1, fixing live v5-vs-v6.2.0 drift) · 3 detector prunes (generated files) · 14 permanent-defer re-annotations | acts + detector |
| `doc_rot` | 7 | **7** | **all 7 are false positives** — §2 amendment clears the class | **detector amendment** |
| `review_artifact_coverage` | 2 | 1 | land a canonical `codex` audit with a `**Tally:**` header, or disposition the Downloads artifact as the record | act (operator, W9) |
| `no_ff_merges` | 3 | 0 | **already zero** — immutable June history, permanently dispositioned | done |
| `git_backlog_drift` | 1 | 0 | dies when `[#505]` closes | row close |
| `journal_spine_anchor` | 1 | 0 | **zero by design** — advisory SHAPE leg (L-10) | leave |
| `reconciled_versions` | 1 | 0 | one-line carve-out for `templates/*-template.md` placeholders | detector (1 line) |
| `preflight_backlog_ids` | 1 | 0 | re-point `[#310]`'s `kill-candidates:` off the closed `#292` | act (1 row) |
| **Total** | **36** | **13** | **§2's amendment alone clears 7 of the 13 blocking WARNs** | |

**1 detector proposal** — `validate_doc_rot.scan_backlog_accretion`: split the conflated check
into **ARM 1 `backlog-accretion`** (citation-blind distinct dates ≥3 **AND** span ≥30d **AND**
>700 chars) and **ARM 2 `backlog-row-length`** (>a *declared* ceiling, no longer a rolling
percentile). One change, three defect classes closed — minted-loci-by-ruled-legs, the `[#523]`
young-row misfire, and dated-tokens-in-citations. Evidence: 59/195 rows (30%) carry phantom
filename dates; 0/51 false strips; 1320 has already drifted from its own p90 calibration to
p96.4 in under a day; **all 7 loci have a history span ≤10d while the 8 widest-span rows are not
loci** — the detector is inversely correlated with the class it names. Ships with a fixture, or
it should not ship. **Folded leg:** `check_stale_worktrees` gains a filesystem arm over
`.claude/worktrees/` — reusing `_git_registered_worktrees` + `_looks_like_worktree_remnant`
unchanged — closing the on-disk-but-unregistered orphan that neither it nor
`check_no_sibling_orphans` can currently see. Propose as a leg on `[#505]`.

**1 row draft** — §3.1, lane-grammar enforcement at provisioning, `[P2][S]`, `kill-candidates:
none — <reason>` in the `check_backlog_filing.py` Leg-1 form, ready for the birth ruling.
Mechanism: the `reference-transaction` hook at the `prepared` stage, **measured** to refuse lane
S's real batch-5 branch name while admitting a conforming one and leaving ordinary commits
untouched. Library-first — reuses `validate_branch_naming` and authors no grammar. Priced
honestly: `pre-commit` cannot install that hook type, so `arm_hooks.py` and `check_hooks_armed`
grow a fourth. Fallback if that cost is refused: `/lane-boot` step 1 plus a detect backstop on
`check_stale_worktrees`.

---

**Nothing in this document was applied.** No register entry written, no row born, no detector
edited, no test changed, no branch or worktree created or deleted. The one experiment (§3.2) ran
in a throwaway clone under the session scratchpad and was removed; `git status` is clean and
`git worktree list` reports the primary only.
