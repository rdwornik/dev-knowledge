# Census — repo root (SWEEP 2026-09-07, lane S-01)

> **READ-ONLY.** Nothing in this lane was moved, deleted, edited or renamed. Every verdict
> below is a **PROPOSAL** the operator rules. Where something is broken it is reported, not
> repaired — a census that repairs what it measures has destroyed its own evidence.

**Consumers:** `[#628]` (the ESSENTIALS dissolution arc this census supplies re-point targets
for) · `[#614]` (the `README.md`/`VISION.md` canonical arc whose root state this measures) ·
`ADR-101` (the tree seal whose root allowlist this reconciles) · `ADR-115` (the `AGENTS.md`
portable-layer split this grades) · `ADR-53` (the `CLAUDE.md` boot contract and its budget) ·
`intake #73` (the fleet shape spec supplying the allowlist), filed at
`docs/intake/2026-09-05-tech-shape-spec-tree-seal-to-consumers.md`.

**Folder:** repo root — the 20 tracked top-level files.
**Question beyond inventory:** `CLAUDE.md` against the industry standard — boot-needed only,
nothing doctrinal; every `protocols/ESSENTIALS.md` reference with a re-point proposal; byte-cap
headroom; every root file allowlisted or proposed.

**Measured at:** `HEAD = 5f27b203c07138374d4cef2ff26564d5c1233d8b` (== `origin/main` at lane start).
**Gemini fan-out:** `NONE` — `command -v gemini` returns nothing in this container. **This is an
absence, not a clean result.** Fabrication count is therefore **0 of 0 locators**; no locator in
this census came from a model reader, every one was opened directly. Copilot Enterprise offload
was **not** available (gated on `#75` ratification) and was **not** used.

---

## Inventory

20 tracked files at the root. `Allow` = admitted by the `intake #73` root allowlist
(`ecosystem/fleet-shape-spec.yaml`, clause `root_allowlist`), computed by importing
`scripts/validate_hermetization.py` and testing each name against `SANCTIONED_TIER1_FILES`
(literal) then `SANCTIONED_TIER1_FILE_GLOBS` (fnmatch). `Bytes` from `stat`.

```
file                            bytes   allow      witness (consumer / generator / last content commit)   verdict
------------------------------  ------  ---------  ---------------------------------------------------   -------
CLAUDE.md                       23551   literal    session boot contract, ADR-53/ADR-115; gated by        KEEP
                                                   tests/test_claude_md_byte_cap.py                       (see Proposals)
AGENTS.md                        5775   literal    portable layer, ADR-115; imported by CLAUDE.md:43;     KEEP
                                                   gated by tests/test_agents_md_byte_cap.py;
                                                   last content c87d54b 2026-09-06
ARCHITECTURE.md               118186    literal    canonical_docs.CANONICAL_MANDATORY; codemap-           KEEP
                                                   freshness pre-commit hook regen-and-diffs it           (see Proposals)
README.md                        4221   literal    canonical_docs.CANONICAL_HUB_MANDATORY; ADR-114        KEEP
                                                   AMENDMENT 1; last content 28e3b1c 2026-09-06
CONTRIBUTING.md                 23503   literal    canonical_docs.CANONICAL_MANDATORY;                    KEEP
                                                   FRESHNESS_FILES member                                 (see Proposals)
BACKLOG.md                      70668   literal    GENERATED from tasks/manifest.json by                  KEEP
                                                   scripts/gen_task_tree.py; validate-backlog hook
JOURNAL.md                    3523990   literal    append-only newest-first; block-unanchored-push        KEEP
                                                   pre-push gate reads it; last content 4cf8559
LESSONS.md                     305245    literal    append-only; canonical_docs.CANONICAL_MANDATORY        KEEP
pyproject.toml                  15251   literal    ADR-106 declared environment; ruff hook rev ==         KEEP
                                                   its required-version floor
uv.lock                         93498   literal    ADR-106; every gate runs `uv run --locked`             KEEP
.python-version                     8   literal    ADR-106 interpreter pin (3.12.10)                      KEEP
.methodology.yaml               13371   literal    32 consumers under scripts/ tests/ .claude/            KEEP
                                                   (fleet_health, fleet_parity, verify_handoff_probes,
                                                   enforcement_coverage, …); intake #12 §9a
.pre-commit-config.yaml         26135   literal    23 hook ids; roster-reconciled against CLAUDE.md §9    KEEP
.pre-commit-hooks.yaml           3297   literal    19 consumers (codemap_hook, toc_hook, audit.py,        KEEP
                                                   tests/test_review_artifact_coverage)
.gitattributes                   3393   literal    12 consumers (audit.py, arm_hooks.py,                  KEEP
                                                   tests/test_floor_conformance)
.gitignore                       9599   literal    node_modules/ exclusion package.json depends on        KEEP
.worktreeinclude                  496   literal    GENERATED by scripts/worktree_seed.py --write          KEEP
                                                   ([#429] leg (a)); read by worktree_import_proof.py,
                                                   tests/test_worktree_seed.py, /lane-boot
package.json                      439   literal    pins pyright 1.1.410 for the [#193] reverse-dep        KEEP
                                                   oracle (ADR-89) driven by scripts/reverse_dep_oracle.py
package-lock.json                1253   literal    lockfile for the above; read by                        KEEP
                                                   scripts/fleet_analytics.py,
                                                   check_dot_prefix_discipline.py
.dev-knowledge.code-workspace   14281   GLOB       admitted by `.*.code-workspace`, not by literal —      KEEP
                                                   the literal was removed as measured leak #2 of
                                                   four (fleet-shape-spec.yaml, file_globs comment)
```

**Root directories** (context, not this lane's verdict surface): 16 present, all sanctioned,
zero unsanctioned. Four sanctioned names have no directory here — `codex`, `src`, `eval`,
`models` — which is the spec working as designed: a clause admits a shape, it does not create a
folder. One sanctioned FILE name is likewise absent: `.ruff.toml` (ruff config lives in
`pyproject.toml` here).

---

## Proposals

### KEEP — all 20, and the allowlist question is closed

**Every root file is allowlist-covered: 19 by literal, 1 by glob. Zero root files need a new
allowlist entry, and zero are candidates for RELOCATE, ARCHIVE or RETIRE.** Every one carries a
live witness — a consumer, a generator, or both — recorded in the inventory above. This is the
one question in the brief that comes back completely clean, and it is stated plainly rather
than padded: the root is hermetic.

### R-1 — the byte cap measures the file, but a session pays for the tree (HIGH)

**Witness (vendor, re-opened):** `https://code.claude.com/docs/en/memory`, *Write effective
instructions* and *My CLAUDE.md is too large* — verbatim: *"Splitting into `@path` imports helps
organization but doesn't reduce context, since imported files load at launch."* And: *"Imported
files are expanded and loaded into context at launch alongside the CLAUDE.md that references
them."*

**Witness (measured, this tree):** `CLAUDE.md` resolves four `@`-imports at depth 1 and none
deeper. No import is missing.

```
CLAUDE.md                              23551 B   <- the only thing the cap measures
  @AGENTS.md                            5775 B
  @.claude/generated/commands-repo.md   2023 B
  @.claude/methodology-roster.md        2729 B
  @.claude/generated/recent-adrs.md     1229 B
TRUE LAUNCH PAYLOAD                    35307 B  = 143.7% of the 24,576 B cap
UNMEASURED IMPORT TAIL                 11756 B
```

`tests/test_claude_md_byte_cap.py::payload_bytes` is `stat().st_size` on one path — correct for
what it claims to measure and wrong for what the budget exists to bound. The gate reports
**1,025 B of headroom (95.8% of cap)** while the session boots on **1.44× the budget**. The
module's own honest-limits discipline is what makes this worth filing: the cap's docstring
argues at length for bytes over lines because *"a line count is gameable by density"*, and the
same argument applies one level up — a byte count on one file is gameable by import.

**PROPOSAL R-1.** Extend `payload_bytes` (or add a sibling assertion) to resolve `@`-imports
transitively and assert the **tree** against the cap, per the vendor's own load semantics.
Recalibrating the ceiling is a separate operator act, not a drive-by of the measurement fix:
today's tree does not fit 24 KiB and would not be made to fit by trimming `CLAUDE.md` alone.
Note the sibling gate `tests/test_agents_md_byte_cap.py` is **unaffected** — Codex's
`project_doc_max_bytes` genuinely measures `AGENTS.md` alone, and R-1 must not be read as
disturbing it.

### R-2 — the cap over-counts what a session actually reads (MEDIUM, favourable direction)

**Witness (vendor, same page):** *"Block-level HTML comments (`<!-- maintainer notes -->`) in
CLAUDE.md files are stripped before the content is injected into Claude's context."*

**Witness (measured):** 47 comment-only lines in `CLAUDE.md` = **2,293 B** — the `scope:`,
`version:` and `methodology:start|end` boundary markers. Of the file's 23,551 B, only
**21,258 B** reach context.

This repo already made exactly this exclusion **on the other budget**:
`validate_doc_rot._is_comment_only` exempts fully render-invisible lines from the LINE count,
with a recorded ruling (`#312`, 2026-07-10). The byte gate does not make the same exclusion, so
the two budgets on the same file disagree about what a byte is for.

**PROPOSAL R-2.** Fold `_is_comment_only`'s predicate into the byte gate so both budgets count
the same substance, and land it **together with R-1** — separately, R-2 alone hands back 2,293 B
of apparent headroom that R-1 shows does not exist. Net across both: the tree is over budget,
not under it.

### R-3 — the line budget is satisfied, and the number to quote is 187 (informational)

Recorded because it is the finding most likely to be mis-stated by a later reader.

- `CLAUDE.md` **physical** lines: **234**
- comment-only lines (`validate_doc_rot._is_comment_only`, replicated exactly): **47**
- **counted** lines, which is what the WARN-only budget reads: **187 / 200 — passing.**

Vendor guidance names the same ceiling — *"target under 200 lines per CLAUDE.md file. Longer
files consume more context and reduce adherence."* Since comments never enter context, 187 is
the honest comparand and this file is inside the standard **on its own**. Across the launch
tree it is **419 lines**. No proposal; do not "fix" 234.

### R-4 — §6 item 5 contradicts §4 and `AGENTS.md` (HIGH)

**Witness:** `CLAUDE.md:119` — `` 5. `pytest --collect-only` — test discovery sanity check ``.
Against `CLAUDE.md:65` — *"a bare `pytest` resolves nothing on a clean checkout (ADR-106 §4)"* —
and `AGENTS.md` *Environment* — *"A bare `python` or `pytest` resolves nothing on a clean
checkout — that is a defect in a doc, not a shorthand."* The boot file instructs, at step 5 of
its own session-start protocol, the exact command two of its other sections classify as a
defect.

**Witness (vendor):** *"Consistency: if two rules contradict each other, Claude may pick one
arbitrarily."*

**Constraint the fix inherits, and the reason this is a proposal rather than a note:** line 119
sits inside hub region `session-start-protocol` (`owner=hub`), whose body is **byte-identical**
to `templates/claude-regions/session-start-protocol.md` (verified — see R-6). Editing
`CLAUDE.md` alone breaks deploy parity (critical rule 6), and this is the very region `[#628]`
records as **omitted from a previous frozen write-scope**, making its own done-item
unsatisfiable. Any re-cut must name it.

**PROPOSAL R-4.** `uv run --locked pytest --collect-only`, landed in
`templates/claude-regions/session-start-protocol.md` **and** the rendered region in the same
commit. Two bytes of budget; one contradiction removed at the boot surface.

### R-5 — doctrinal ballast against the file's own genre rule (MEDIUM)

The standard applied is the file's **own**, stated at `CLAUDE.md:12`: *"a rule lives here only
if a session needs it before it can act; rationale, history and per-organ detail live at the
home each line cites."* The vendor states the same test twice — *"Keep it to facts Claude should
hold in every session: build commands, conventions, project layout, 'always do X' rules"*, and
`/doctor`'s trim rule: *keeps pitfalls, rationale, and conventions that differ from tool
defaults*, cuts what is derivable.

Section cost, measured:

```
section                          lines   bytes   %cap   genre verdict
-------------------------------  -----  ------  -----   -------------
(frontmatter + header + budget)     17     963   3.9%   IN GENRE
1. First read                       14    1494   6.1%   IN GENRE (one clause is provenance — below)
2. Repo identity                    14    1051   4.3%   IN GENRE
3. Architecture                     11     966   3.9%   IN GENRE (pure pointer — model row)
4. Conventions                      31    5797  23.6%   MIXED — largest section, ~1/4 of the cap
5. Critical rules                   22    3481  14.2%   MIXED
6. Session start protocol           17     967   3.9%   IN GENRE, but see R-4
7. Slash commands                   14    1043   4.2%   IN GENRE (roster)
8. Skills active                    12    1096   4.5%   IN GENRE (roster)
9. Hooks active                     46    3973  16.2%   IN GENRE (roster; reconciled clean, R-7)
10. Anti-patterns                   13    1441   5.9%   MIXED
11. Recent ADRs                     10     463   1.9%   IN GENRE (generated)
12. Section history                 14     804   3.3%   OUT OF GENRE — R-6
```

The four MIXED sections are not bloat in bulk; the ballast is **specific clauses** that argue a
past decision rather than state a present rule. Enumerated so the operator rules each on its
own, not as a block:

- **§4 TDD bullet** — *"A blanket mandate is not live — Council rejected 'Mandatory TDD'"* is
  re-litigation defence, not an instruction. The instruction ("ADR-108 §B binds every build
  arc; CC may strengthen but never weaken") is the first half and survives alone.
- **§4 Decision funnel (ADR-111)** — the OWNED/DISCHARGED/CANDIDATE/REJECTED taxonomy and the
  question-routing rule are governance procedure a session consults *when triaging*, not before
  it can act. Nearest home: `protocols/PLAYBOOK.md`, consulted on demand.
- **§4 Spec-driven bullet** — the "Live:" clause enumerates four surfaces; that is a roster,
  and §4's own rule says never restate a roster in prose.
- **§5 rule 5** — the `README.md` deletion→recreation history and the `VISION.md` relocation
  are narration of two closed arcs. The live rule is one clause: *no new markdown files without
  checking navigation/growth triggers.*
- **§5 rule 8** — *do not recreate `CHANGELOG.md` or `BACKLOG_ARCHIVE.md`* is genuinely
  boot-needed (it prevents an act) and should stay; its 2026-05-16 provenance need not.
- **§10 `AGENTS.md` anti-pattern** — carries a measured 43.50 KiB figure to justify a rule that
  states itself in six words.
- **§1 item 3** — names four organs that share `_select_active_bundle`'s predicate. The session
  needs the predicate; the roster of reusers is provenance.

**PROPOSAL R-5.** Relocate — do not trim — the clauses above to the home each already cites, per
the ruled remedy doctrine (*the row carries a pointer; the record carries the record*,
`[#612]`). Estimated recovery is deliberately **not** stated as a number here: seven of these
clauses sit in hub-owned regions and the recoverable figure depends on which the operator
rules, so quoting a total would be a count restated in prose. **Note this does not solve R-1** —
even a fully drained `CLAUDE.md` leaves the 11,756 B import tail untouched.

### R-6 — §12 Section history argues its own case for retirement (MEDIUM)

`CLAUDE.md:222-229`, 804 B / 3.3% of cap. After the 2026-09-05 relocation the section contains
**no history** — only a pointer to
`docs/audits/2026-09-05-technical-claude-md-section-history-ledger.md`, plus a sentence
explaining why the entries left: *"a changelog of this file's own past revisions is not
something a session needs before it can act, which is the genre rule this file states in its own
header."* The same reasoning retires the pointer. A session that needs the ledger is not booting.

**PROPOSAL R-6.** RETIRE the section; keep the ledger file. The region is `owner=repo`
(`section-history`), so there is **no fleet coupling and no template to move in lockstep** —
this is the cheapest clean byte recovery available at the root, and the only R- proposal here
that touches nothing outside this repo's own lines.

### R-7 — what is already clean, verified rather than assumed

Recorded because a census that reports only defects overstates its case.

- **All nine `owner=hub` regions are byte-identical to `templates/claude-regions/*.md`.**
  Critical rule 6 holds with zero drift. Verified by extracting each region body and comparing
  to its template: `first-read` 1243 B, `conventions-commit-branch` 538, `conventions-library-first`
  289, `conventions-output-formatting` 748, `critical-rules-records` 1002,
  `critical-rules-consistency` 168, `critical-rules-no-leftovers` 346, `session-start-protocol`
  681, `antipatterns-universal` 1129 — nine of nine identical.
- **§9's hand-authored pre-commit roster matches `.pre-commit-config.yaml` exactly**: 23 claimed,
  23 configured, zero claimed-not-configured, zero configured-not-claimed.
- **The `AGENTS.md` relation is exactly what the vendor prescribes.** Vendor: *"If your
  repository already uses `AGENTS.md` for other coding agents, create a `CLAUDE.md` that imports
  it so both tools read the same instructions without duplicating them."* `CLAUDE.md:43` is
  `@AGENTS.md`, with the Claude-runtime remainder below it. ADR-115 also refuses the symlink
  form for a Windows `core.symlinks=false` reason the vendor page independently notes. Correct
  on both counts.
- **Every root file has at least one live consumer**, including the four that look vestigial
  (`package.json`/`package-lock.json` → the `[#193]` pyright oracle; `.worktreeinclude` → 8
  consumers; `.gitattributes` → 12; `.pre-commit-hooks.yaml` → 19).

### R-8 — two restated figures that have drifted (LOW, both witnessed)

Both are instances of the rule `CLAUDE.md:70` states: *"Never restate a count or roster in prose
— a number typed into a doc is stale at the next commit."*

- **`CONTRIBUTING.md:19`** — *"`AGENTS.md` — now exists (added 2026-08-29, 5,714 B)"*. Actual
  today: **5,775 B**. Drift 61 B. PROPOSAL: drop the figure or cite `stat`; do not update it to
  a new number that will drift again.
- **`tests/test_claude_md_byte_cap.py`** docstring, third ceiling derivation — *"the eight
  frozen `owner=hub` regions cost 7,607 B"*. Measured today: **nine** regions costing **6,144 B**.
  Not a gate and not this lane's folder — reported so the ceiling's own rationale is not later
  quoted as current. The derivation's *conclusion* is unaffected; only its arithmetic input.

### R-9 — `README.md` frontmatter casing (LOW, cosmetic)

`README.md` carries `owner: rob`; `CLAUDE.md`, `AGENTS.md`, `ARCHITECTURE.md` and
`CONTRIBUTING.md` all carry `owner: Rob`. No gate reads the case. Noted only so a future
normalizer does not treat it as a finding.

---

## `protocols/ESSENTIALS.md` — every reference in this lane's folder, with a re-point proposal

`protocols/ESSENTIALS.md` is `status: superseded` (16,461 B, `last_reviewed: 2026-09-01`),
banner: *"SUPERSEDED — not a boot read. Dissolution tracked in `[#628]` with v1.5.0."* The
owning row is `[#628]`, **DE-BLESSED 2026-09-01**, whose remaining job is the mechanical
dissolution and its ten enumerated consumers. **None of the ten is a root file**, so every row
below is either already discharged or a re-point `[#628]` does not currently carry.

```
locator                  state                     re-point proposal
-----------------------  ------------------------  -----------------------------------------------
CLAUDE.md:16 (header)    ALREADY RE-POINTED        none — marked "superseded, pending [#628]".
                                                   Retire the clause when [#628] deletes the file.
CLAUDE.md:25 (§1 no.2)   ALREADY RE-POINTED, but   PROPOSE: at dissolution, DELETE the item rather
                         still occupies slot 2 of  than reword it a third time. A boot list whose
                         a 4-item boot list and    second instruction is "skip this" spends bytes
                         costs ~230 B to say       teaching a session not to read something.
                         "skip it"                 Hub region `first-read` -> template moves too.
README.md:65             ALREADY RE-POINTED        none — carries the same superseded marker.
ARCHITECTURE.md:309      NOT RE-POINTED —          PROPOSE: re-point to the PLAYBOOK span that
                         cites ESSENTIALS          absorbs channel-discipline, or mark the citation
                         "Architect -> operator    superseded in place. Anchor RESOLVES today
                         channel-discipline" as    (verified: 1 match in ESSENTIALS.md), so this is
                         a live authority          a live pointer into a dead doc, not a dangling one.
ARCHITECTURE.md:348      NOT RE-POINTED —          PROPOSE: same treatment. Anchor RESOLVES
                         "Architect routing for    (1 match). This is the routing rule ADR-108 §A
                         technical proposals"      also states; ADR-108 is the durable home.
ARCHITECTURE.md:960      NOT RE-POINTED —          PROPOSE: move `ESSENTIALS` out of the Living row
                         lists ESSENTIALS in the   into the same superseded treatment `VISION`
                         *Living* file-class row,  already has in that very cell. The row already
                         alongside VISION which    demonstrates the pattern — apply it twice.
                         IS marked superseded
ARCHITECTURE.md:1042     NOT RE-POINTED — the      PROPOSE: `Conventions (PLAYBOOK / CLAUDE.md)`.
                         conventions->enforcement  A superseded doc is not a live conventions
                         chain names ESSENTIALS    source, and this line is a model of the system.
ARCHITECTURE.md:1045     NOT RE-POINTED — cites    PROPOSE: same as :309/:348. Anchor RESOLVES.
                         ESSENTIALS "Feedback"
BACKLOG.md:218           GENERATED — it IS the     none. Editing BACKLOG.md is forbidden (generated
                         [#628] row                from tasks/); the source is
                                                   tasks/628-dc2-recut-essentials-dissolution-is-a-
                                                   release-act.md
BACKLOG.md:347, :389     GENERATED — emitted from  PROPOSE: any re-point targets the `prose` nodes
                         `prose` nodes in          in tasks/manifest.json, then
                         tasks/manifest.json (the  `gen_task_tree.py --emit-source`. These are W6
                         W6 theme heading and a    seed text and a rule-surface convention; both
                         rule-surface convention), name ESSENTIALS as a live co-edit target, which
                         NOT from any tasks/*.md   dissolution invalidates.
JOURNAL.md (243 hits)    APPEND-ONLY               NONE POSSIBLE, and this is the correct outcome,
LESSONS.md (19 hits)     APPEND-ONLY               not a gap. Critical rules 1-2 forbid editing
                                                   past entries. These are historical records of
                                                   what was true then. [#628] must not be scoped
                                                   to "zero ESSENTIALS references remain" — that
                                                   target is unreachable by construction and would
                                                   invite an append-only violation to reach it.
```

**Cross-boundary observation, reported not proposed** (the surface is outside this lane's
folder): `protocols/ESSENTIALS.md` remains a member of
`scripts/canonical_docs.py::FRESHNESS_FILES` via `ESSENTIALS_PATH`. A superseded doc is
therefore still enrolled in the A1/A2 freshness cadence — it must be periodically re-read and
re-stamped to satisfy a gate, in order to keep a file nobody may boot from. `[#628]` already
names the five `canonical_docs.py` memberships in its Done-when, so this is **inside** that
row's scope and needs no new filing; it is recorded here as corroboration that the row's
enumeration is correct.

---

## Counts before → proposed after

Nothing in this census proposes a file-count change at the root. The changes proposed are to
*content and to one gate*, not to the tree.

```
                                              before      proposed after
tracked root files                                20      20  (no RELOCATE / ARCHIVE / RETIRE)
root files on the intake #73 allowlist            20      20  (19 literal + 1 glob)
root files needing a new allowlist entry           0       0
unsanctioned root directories                      0       0
CLAUDE.md sections                                12      11  (R-6 retires §12)
CLAUDE.md counted lines / 200                    187     <187
CLAUDE.md bytes / 24,576 cap                   23551   unresolved by design — see R-1;
                                                       trimming this number alone does not
                                                       bring the payload under the cap
TRUE launch payload bytes / cap                35307   the figure R-1 asks the gate to measure
hub regions byte-identical to templates          9/9     9/9  (R-4 moves one in lockstep)
CLAUDE.md §9 hooks vs .pre-commit-config       23/23    23/23
root-file ESSENTIALS refs already re-pointed     3       3
root-file ESSENTIALS refs NOT re-pointed         5       0   (all five in ARCHITECTURE.md)
root-file ESSENTIALS refs re-pointable via
  a generator source (tasks/manifest.json)       2       0
root-file ESSENTIALS refs unreachable by
  construction (append-only JOURNAL/LESSONS)    262     262  (correct, not a gap)
restated figures found drifted                    2       0   (R-8)
```

---

## Honest limits

What this census could **not** establish, stated because the section is the point.

1. **The authority file was never opened.** The brief names
   `to-cc\BATCH-2026-09-07-SWEEP-CONTRACTS.md` (FROZEN, 5422 B) as the operator's word and
   instructs "read that file yourself." It is on the Drive transport, which is **not mounted in
   this container** — a filesystem search found no such file anywhere. Everything here follows
   the brief's working copy alone. **If the frozen contract disagrees with the working copy, it
   wins, and this census has not been checked against it.**

2. **Gemini fan-out was NONE, and that is an absence, not a clean bill.** No CLI on PATH. The
   ranking-and-retrieval pass the brief budgets for did not happen; coverage of the root rests on
   `git ls-files` (exhaustive for tracked files, so the *inventory* is complete) and on direct
   greps (not exhaustive for *consumers* — see limit 4). Fabrication count 0 is a consequence of
   0 model-supplied locators, not evidence of accuracy. Copilot Enterprise offload was
   unavailable pending `#75` and was not used.

3. **The clone is SHALLOW, so "last content commit" is a weak witness.** `.git/shallow` exists
   and the graft boundary is `428656f` (2026-09-05), which reports as parentless. Thirteen of the
   twenty root files resolve their last touch to that boundary commit — meaning *"not modified
   since the clone horizon"*, **not** *"last edited 2026-09-05"*. Only `AGENTS.md` (c87d54b),
   `README.md` (28e3b1c), `JOURNAL.md` (4cf8559) and `.methodology.yaml` (1cefc30) have a real
   last-content commit inside the horizon. **No root-file verdict here rests on a
   last-content-commit witness** — every KEEP is carried by a consumer or a generator instead,
   precisely because this witness class is unreliable in this container.

4. **Consumer counts are lower bounds.** They come from `grep -rl` over `scripts/ tests/
   .claude/ .github/ deploy/ ecosystem/` for the literal filename. A consumer that reaches a
   root file by a constructed path, a `Path(__file__).parent.parent / name`, or a glob is
   invisible to that method. Every count in the inventory should be read as "at least N", and
   no verdict here would flip if a count were higher.

5. **No gate was executed.** `uv` in this container is **0.8.17** against `pyproject.toml`'s
   `required-version = "==0.11.19"`, so every `uv run --locked …` invocation refuses. The
   pre-commit suite, `audit.py health`, `validate_hermetization` as a hook, and
   `tests/test_claude_md_byte_cap.py` were therefore **never run**. Allowlist membership was
   established by importing `scripts/validate_hermetization.py` under system Python 3 and
   reading its derived `SANCTIONED_TIER1_*` constants directly — the same values the gate uses,
   obtained without running the gate. Section byte counts, region byte-identity, the §9 hook
   reconciliation and the import-tail measurement are all independent recomputations, not gate
   output. **A green gate has not been demonstrated for anything in this census.** Per the
   brief, no full suite was attempted and the known main-branch RED is not claimed here.

6. **R-1's severity is measured; its remedy is not costed.** The 35,307 B figure is arithmetic
   and firm. Whether the fix is a wider `payload_bytes`, a raised ceiling, a split into
   `.claude/rules/` with `paths:` frontmatter (the vendor's own recommendation for exactly this
   problem), or some combination is an operator/architect decision this lane did not model, and
   any of them changes what a consumer receives. R-1 states the defect, not the design.

7. **R-5's recovery is deliberately unquantified.** Seven of the named clauses sit in hub-owned
   regions whose bodies are byte-matched to `templates/claude-regions/*.md` and deploy-carried
   to every ADR-104 member. What is recoverable depends entirely on which clauses the operator
   rules out, and each such ruling is a fleet act. A single "bytes saved" number would have been
   a guess dressed as a measurement.

8. **The vendor standard was read from one page, once.** `code.claude.com/docs/en/memory`,
   fetched during this lane. Every quotation in R-1/R-2/R-3/R-4/R-7 is verbatim from that
   fetch. Related pages (`/docs/en/large-codebases`, `/docs/en/context-window`) were **not**
   opened, so "industry standard" here means *this vendor's documented guidance plus this
   repo's own genre rule* — not a survey of practice across tools, which this lane did not
   attempt and does not claim.

9. **Scope discipline.** `docs/intake` shape-spec, `deploy/`,
   `ecosystem/deployed-versions.yaml`, `templates/ADR-template.md` and
   `docs/decisions/ADR-117` were **read, never written**, per batch-U wave-2 footprint rules.
   `ecosystem/fleet-shape-spec.yaml` and `scripts/validate_hermetization.py` were read (not
   written) because the allowlist question is unanswerable without them. Findings R-4, R-8 and
   the `FRESHNESS_FILES` observation land **outside** this lane's folder and are reported for
   the operator and the integrator rather than acted on — no census lane touches another lane's
   folder, and none of them was touched.
