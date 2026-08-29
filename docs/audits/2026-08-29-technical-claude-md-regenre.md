# CLAUDE.md re-genre — the relocation ledger, the byte measurements, and what was not done

**Lane:** `lane-c-000-claude-md-regenre` (batch-D) · **Date:** 2026-08-29 · **Substrate:** local
worktree, commit-and-STOP
**Rows born:** ZERO. No `tasks/` edit, no intake, no ADR, no JOURNAL entry — the integrator's
filing pass acts (`protocols/STANDING_RULINGS.md` P-1).
**Footprint:** `CLAUDE.md` · `tests/test_claude_md_byte_cap.py` (new) · this file. The last two
are outside the contract's frozen write-scope line and are declared in §6.

---

## §1 — The measurement

Taken with `wc -l` / `wc -c`, and re-taken by the gate at every run so no figure here is a
remembered constant.

```
                 lines      bytes    B per line
before             240     39,588           165
after              230     23,931           105
delta              -10    -15,657        -39.5%

ceiling                    24,576         97.4% used, headroom 645 B
frozen owner=hub regions    7,607         31.8% of the file, unreachable from this repo
repo-owned remainder       16,324
```

Baseline as witnessed at contract freeze was **39,147 B**; the file measured **39,588 B** when this
lane opened. The +441 B is lane-b's `[#614]` edit to §5 rule 5, merged at `023a7797` between freeze
and dispatch. The larger figure is used throughout — measuring against the tree actually in front
of the lane, not against the frozen prose.

**The finding the numbers make.** The line count moved by 10; the byte count fell by two fifths.
The file was satisfying ADR-53's `≤200 lines` **by density** — 165 B/line against the ~117 B/line
this corpus averages (the figure `tests/test_agents_md_byte_cap.py` records for the same estate),
i.e. 41% above the norm. Lines were the gamed proxy. Bytes were the unbudgeted cost, and they are
paid at *every session start*, not at every edit.

Per-section, after:

```
HEADER        876   §4 Conventions     6,248   §8 Skills             1,097
§1 First read     1,494   §5 Critical rules  3,404   §9 Hooks              3,796
§2 Repo identity  1,112   §6 Session start   1,003   §10 Anti-patterns     1,388
§3 Architecture     967   §7 Commands        1,044   §11 Recent ADRs         464
                                                     §12 Section history   1,039
```

## §2 — The ceiling: 24,576 B, and why it is not reverse-engineered

The number was fixed **before** the re-genre and the file was cut to fit it, not the other way
round. It is ADR-53's own `≤200 lines` re-denominated in the metric the claim was trying to bound,
rounded up to the next binary KiB. Three independent derivations land in the same place:

| Derivation | Result |
|---|---|
| 200 lines × ~117 B/line (this corpus's measured density) | 23,400 B |
| 200 lines × ~124 B/line (this file at ordinary prose density) | 24,800 B |
| 7,607 B of frozen hub regions + a 16 KiB budget for the repo-owned remainder | 23,991 B |

**Headroom is 645 B (~6 lines) and that is the design, not an accident.** It matches how this repo
already runs its line budget — `CLAUDE.md` v2.68 closed at "196/200, headroom 4 — bought, not
shaved". Room for a new rule is bought by condensing and relocating; the ceiling does not move.

**The line bound is KEPT, not replaced.** ADR-53's `≤200 lines` is ratified doctrine, restated in
ADR-115 and at several `protocols/PLAYBOOK.md` sites. `validate_doc_rot._FILE_SIZE_BUDGETS` is
untouched, and both budgets now run. This lane could edit none of ADR-53, ADR-115 or PLAYBOOK, so
promoting the byte bound into them is **owed** (§6).

**Not the Codex cap.** `tests/test_agents_md_byte_cap.py` considered and *rejected* asserting
`CLAUDE.md` against Codex's 32 KiB `project_doc_max_bytes`, correctly, because `CLAUDE.md` is not
part of the Codex payload. Nothing here disturbs that ruling: this is a different budget, for a
different consumer, at a different number. The new module says so in its docstring so the two are
never conflated.

## §3 — The relocation ledger

The operator's no-deletion rule binds: nothing was deleted, everything was **relocated to a named
destination that was opened and read before being relied on**. Ordered by bytes moved.

### 3.1 §9 Hooks active — 13,141 B → 3,796 B, the largest single move

§9 was a per-hook manual: rationale, ticket provenance, exit codes and an "Honest limit" paragraph
for each of 21 gates. Four destinations, each verified:

| What moved | Destination | How it was verified |
|---|---|---|
| the roster itself (21 hook ids) | generated `ecosystem/organ-index.md` | read its `## git-hook` section: all 21 ids present, with trigger · source · distribution · status |
| failure posture (fail-closed / fail-soft / propose-only) | `ARCHITECTURE.md` Ch2 | Ch2 states it is the source for this column *because* the generated index cannot carry it |
| curated per-validator detail | `ARCHITECTURE.md` "Validators and enforcement" | it already carries `block_ff_push`, `check_seal_identity`, `validate_hermetization` and `validate_residual_completeness` with their honest limits, near-verbatim — but only for **7 of the 21** hooks; see the correction below |
| per-hook rationale + honest limits | each module's docstring under `scripts/` | parsed every one: docstrings run 0.9–5.3 KB, and the specific limits §9 named are present — `block_commit_on_main` carries a "STATED HOLES, BY DESIGN" section, `validate_hermetization` its Rule C and its name-SHAPE-only caveat, `check_provider_registry` its checker-not-a-rewrite limit |

**The correction that matters most, and it corrects this lane's own step-2 commit message.**
That message claimed "ten of the twenty-one hooks have NO `ARCHITECTURE.md` entry at all". That is
wrong twice over, and the accurate figures were computed per-hook afterwards:

```
                                   named in ARCH   module in ARCH   in "Validators and
                                     (any form)                      enforcement"
of the 21 pre-commit hooks               15               8                7
```

So **15** are named somewhere in `ARCHITECTURE.md` — but mostly *in passing*: in the git-stage
grouping, in the `always_run` list, or in the paragraph explaining why the enumeration was deleted.
Only **7** have their rationale carried in the "Validators and enforcement" chapter. **14 of 21
have no rationale home in `ARCHITECTURE.md` at all**, which is a worse number than the one the
commit message gave, not a better one.

And the structural fact behind it: `ARCHITECTURE.md` **explicitly designates CLAUDE.md §9** as
*"the annotated roster … the one enumeration of this class a gate protects"*, and deliberately does
not re-enumerate — *"Read those three; this map points, and the pointer cannot rot."* It says so
because that enumeration rotted three times in ARCHITECTURE and the fix was to stop restating it.

**Therefore, stated plainly: this lane reduced the annotation depth of the surface ARCHITECTURE
points at.** The *enumeration* is untouched and still gate-protected — which is the property
ARCHITECTURE actually relies on. What thinned is the per-hook rationale, and for those 14 hooks it
now lives only in a code docstring. That is the single real cost of the re-genre. It is defensible
— the doctrine's own design is pointer-based, and §9 → module docstring is the same move one level
down — but it is a cost, not a free move, and §6 carries it as owed work rather than closing it.

Two things were **kept in §9 rather than relocated**, deliberately:

- **the 21 hook-id bullets**, because they are a machine-read surface (§4);
- **the `logs/` artifact-naming ruling** ([#395]), which was not per-hook detail at all. It moved
  *into* §4 Naming, where a naming convention belongs — a relocation within the file, not out of it.

### 3.2 §4 Conventions and §5 Critical rules — dated litigation → the citations already present

Every §4 and §5 line already ended in an ADR or PLAYBOOK pointer. What left was the narration
*between* the rule and its pointer: re-litigation, dated amendment histories, counts of how often a
lesson had been re-learned. The rule and the pointer both stayed in every case. Destinations, all
already cited by the line that carried the narration: ADR-27/ADR-48 (scope tags), ADR-53 and
ADR-115 (the two-file model), ADR-81 and ADR-108 §B (TDD), ADR-88/ADR-89 (edges), ADR-98 and
ADR-111 (the funnel), ADR-106 (dependencies), ADR-107 (BACKLOG generation), ADR-114 and `[#614]`
(the README recreation), plus `protocols/PLAYBOOK.md` Ch5, Ch8 and Ch12.1.

**§5 rule 5 was trimmed, and that deserves saying out loud:** it is lane-b's `[#614]` text, merged
hours earlier. The ruling and the ADR-114 pointer are preserved intact; what was condensed is the
fleet-migration justification, whose home is ADR-114 and the `[#614]` row. Deference to a sibling
lane's prose is not a reason to leave in place the exact narration this lane was dispatched to
relocate — but the integrator should see the overlap rather than discover it.

### 3.3 §12 Section history — the v2.68 entry → git history

On this section's own standing precedent: it already reads *"Entries v1.0–v2.67 condensed to git
history per ADR-49/65 (info-preserving — full prior history: `git log --follow -p -- CLAUDE.md`)"*.
The pointer now reads v1.0–v2.68 and the retrieval command is unchanged. The v2.69 entry that
replaces it is ~1,000 B and points here for everything else — a changelog entry in a boot contract
is precisely the genre error this lane exists to fix.

### 3.4 Fixed in passing

The header comment read `<!-- version: 2.67 -->` while §12 already carried a v2.68 entry whose own
text said "L10 version 2.67→2.68". The header is now `2.69`. No gate reads that comment (checked:
no `scripts/` consumer greps for it), which is exactly why it drifted.

## §4 — Machine-read surfaces: verified after the edit, not assumed

`CLAUDE.md` is parsed by two organs and byte-compared against eight templates. All three were
re-run against the edited file.

- **`validate_doc_claims.py` → `precommit_hook_roster@CLAUDE.md`: MATCH, 21/21.** The parser
  windows on `## 9. Hooks active`, waits for a line matching `/Pre-commit/i` that also contains
  `pre-commit-config.yaml`, then collects the leading backtick id of each `- ` bullet **until the
  first non-bullet, non-blank line**. Two consequences were designed around rather than discovered:
  the bullet list must stay complete and contiguous (an HTML comment now says so in place), and the
  new explanatory blockquote above it deliberately avoids the literal string `pre-commit-config.yaml`,
  which would otherwise open the collection window one line early and yield an empty set —
  reported as `anchor-missing`, i.e. a silent loss of the claim rather than a loud failure.
- **`boundary_headers.py --check`: clean** — every generated `> **[HUB - methodology]**` /
  `> **[REPO - local]**` header still matches its marker.
- **The eight `owner=hub` regions are byte-identical to `templates/claude-regions/*.md`:
  BYTE-MATCH 8/8**, measured rather than eyeballed:

```
first-read                     1,242 B    conventions-commit-branch        972 B
conventions-output-formatting  1,224 B    critical-rules-records         1,002 B
critical-rules-consistency       104 B    critical-rules-no-leftovers      346 B
session-start-protocol           716 B    antipatterns-universal         1,075 B
```

  Region == template in every case. These 7,607 B are 31.8% of the file and are **unreachable from
  this lane** — editing one without a lockstep `templates/` commit breaks fleet parity, and
  `templates/` was out of scope. The ceiling was derived around that floor for exactly this reason.
- **`validate_doc_rot.py`: zero `CLAUDE.md` findings.** Both the 200-line file budget and the
  section-history accretion locus are clean.

## §5 — Verification run

- **`tests/test_claude_md_byte_cap.py`: 6/6 green** after step 2 (2 failed / 4 passed at step 1,
  the RED-first witness, on purpose).
- **Targeted set** — the 10 modules covering this diff (`claude_md_byte_cap`, `agents_md_byte_cap`,
  `boundary_headers`, `boundary_report`, `canonical_docs`, `canonical_freshness_gate`,
  `validate_doc_claims`, `validate_doc_rot`, `gen_claude_rosters`, `coherence_integration`):
  **202 passed, 1 failed**.
- The single failure is
  `test_validate_doc_rot::test_live_corpus_has_no_accretion_arm_findings_only_length_findings`,
  on `BACKLOG#267` and three siblings. **Pre-existing, and provably not this lane's:**
  `git diff --stat main -- BACKLOG.md tasks/` is empty, so that check's inputs are byte-identical to
  `main` and its output cannot have changed.
- **`audit.py health`: DEGRADED, one `[!!]`** — `journal_spine_anchor` on `98c84569`
  ("Merge branch 'docs/lane-d-recut'"), a merge already on `main` and an ancestor of this lane's
  base. A batch lane never journals (P-1), so it is the integrator's to discharge. Re-checked after
  step 2 that it is still the **only** `[!!]`, so nothing here introduced a new one.
- **`ruff check`** on the new module: clean.
- **Bypass declared in both commit bodies:** `SKIP=audit-health`, for that one pre-existing FAIL.
  No other hook was skipped; `validate-hermetization`, `provider-registry-agreement`,
  `block-commit-on-main`, `backlog-id-on-close` and `backlog-filing-backpressure` all ran and passed.

## §6 — Decisions taken, and what is owed

Per V-2, forks decided per contract default are **reported here, not asked**. One item is a genuine
class-(b) conflict and is flagged as such rather than buried.

**(b) — the frozen write-scope and the done-contract cannot both be read literally.** The scope line
reads `CLAUDE.md` · `.claude/generated/**`. Done-contract item 1 requires a **gate**, and step 3
requires an **end-of-lane artifact**; neither can live in either of those two paths, so two of the
three steps are unexecutable on the literal reading. The contract itself points at the other home —
*"the byte-cap test PATTERN that already guards `AGENTS.md` in `tests/`"* — so the omission is in the
scope line, not in the steps. Resolution taken: **land both as ADDs** (`tests/test_claude_md_byte_cap.py`,
this file), colliding with no sibling lane, and keep the gate **isolated in its own commit** so the
integrator can drop it alone if they read the scope line as binding. `.claude/generated/**` was
declared in scope but is **untouched** — regenerating an index is the integrator's act (Q1).

**Decided per default, reported not asked:**

- **RED-first commit order.** Step 1's commit lands a knowingly-failing gate. That is not a defect:
  ADR-108 §B binds every build arc to "RED-first witnesses, failing tests before build code", and
  the contract's step order *is* that arc. The witness is recorded in the step-1 commit body.
- **Reuse stops at the message.** `payload_bytes` is imported from the sibling module — one site for
  the `stat().st_size`-not-`len(read_text())` rule. `assert_within_cap` is **not** imported: its text
  is Codex-specific ("Codex instruction payload … `project_doc_max_bytes` cap"), and emitting that
  for a `CLAUDE.md` overrun would name the wrong consumer and the wrong cap. The contract names the
  *pattern* as the reusable artifact; the shape is the sibling's, the wording is this budget's.
- **A fourth test beyond the pattern:** `test_declared_ceiling_agrees_with_the_gate` asserts that the
  ceiling `CLAUDE.md`'s header advertises equals the one the gate enforces. This is the file's own
  §4 rule ("never restate a number in prose — cite the surface that computes it") made checkable,
  and it costs one regex.

**Owed, and outside this lane's reach — named so it is not discovered later:**

1. **Fourteen of the twenty-one hooks have no rationale home in `ARCHITECTURE.md`** — only 7 are
   carried in its "Validators and enforcement" chapter (`audit-health`, `backlog-id-on-close`,
   `block-ff-push`, `check-seal-identity`, `normalize-dated-headers`, `validate-backlog`,
   `validate-hermetization`). The other 14 —
   `audit-index-freshness`, `backlog-filing-backpressure`, `block-commit-on-main`,
   `block-unanchored-push`, `claude-rosters-freshness`, `codemap-freshness`, `coherence-nudge`,
   `intake-index-freshness`, `lane-contract-check`, `organ-index-freshness`,
   `provider-registry-agreement`, `roster-freshness`, `ruff`, `toc-freshness-playbook` — now rest
   on a **code** docstring alone. Verified home, weaker surface. This supersedes the step-2 commit
   message's figure of ten, which was both wrong and too kind; §3.1 carries the correction and the
   per-hook table. Absorbing them into "Validators and enforcement" needs a lane whose scope reaches
   `ARCHITECTURE.md`, and it is the highest-value follow-up this lane leaves behind.
2. **The byte bound is not in the doctrine.** ADR-53, ADR-115 and PLAYBOOK still state a line budget
   only. Until one of them carries the byte ceiling, `CLAUDE.md`'s header and
   `tests/test_claude_md_byte_cap.py` are the only places it exists.
3. **`validate_doc_rot._FILE_SIZE_BUDGETS` is still a LINE budget** (`{CLAUDE: 200}`, hardcoded in
   `scripts/validate_doc_rot.py`, WARN-only). It is the residual proxy the byte gate supersedes.
   Deliberately left alone — `scripts/` was out of scope, and retiring it is a doctrine act, not a
   lane act.
4. **`ecosystem/doc-counts.md` `pytest_collected` drifts 4,622 → 4,628** from the six added tests.
   Ship-tier WARN; a lane must not touch that file. One command at integration:
   `gen_doc_counts.py --write`.

## §7 — Honest limits of what was built

- **The gate measures SIZE, never QUALITY.** A future edit that stays under 24,576 B by deleting a
  load-bearing rule passes green. The no-deletion discipline — every removal is a relocation to a
  named destination — is a review obligation no gate here enforces, and this ledger is the artifact
  that discharges it for *this* edit only.
- **The gate measures the file on disk, not the session payload.** `CLAUDE.md`'s `@`-imports
  (`@AGENTS.md`, `@.claude/generated/*.md`, `@.claude/methodology-roster.md`) are expanded by the
  Claude Code runtime at read time, so what a session actually pays is **larger** than 23,931 B.
  Bounding the expanded payload is a different, unbuilt gate. The figure asserted here is a floor on
  the real cost, not the real cost.
- **31.8% of the budget is spent on regions this repo cannot edit.** If the hub regions grow, the
  ceiling gets harder to hold and no amount of local discipline recovers it. That coupling is stated,
  not solved.
- **`ecosystem/organ-index.md` carries the roster but explicitly not the failure posture**, by its
  own header. So the §9 relocation is genuinely three-destination, and a reader chasing "what happens
  when this hook says no" must land on `ARCHITECTURE.md` Ch2, not on the index.
