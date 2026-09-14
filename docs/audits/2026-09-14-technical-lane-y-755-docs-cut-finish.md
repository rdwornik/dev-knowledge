# Lane `lane-y-755-docs-cut-finish` — end-of-lane packet

**Batch:** Y, wave 1 · **Lane:** 4 of 6 · **Row:** `[#755]` (filed by this lane) ·
**Owners touched:** `[#628]` (discharged in part), `[#667]` / `[#664]` (handed back)
**Branch:** `worktree-lane-y-755-docs-cut-finish` · **Base:** `main` @ `8a41c650`,
sync-merged to `e6acb23e` mid-lane · **Mode:** execute · commit-and-STOP

---

## 1 · What changed

Four commits, in contract order.

| # | SHA | Act |
|---|---|---|
| 1 | `e791cffc` | `protocols/ESSENTIALS.md` DELETED; every live surface it broke followed to green |
| 2 | `55d03e46` | `ARCHITECTURE.md` ESSENTIALS anchors re-pointed; the `[#667]` render premise reported REFUTED |
| 3 | `d5dcfc95` | `[#755]` filed (task file + manifest node + regenerated view); `[#628]` split into discharged / not-discharged |
| 4 | *this commit* | this packet |

### 1.1 The deletion, and the release coupling that turned out to be discharged

`[#628]` frames the dissolution as a **fleet-coupled release act**. Measured against the
tree, that coupling no longer binds the deletion itself:

- `protocols/ESSENTIALS.md` is **not under `carriers:`** in any of the seven manifests. It
  appears only under `doc_shapes:`, which the manifest's own comment declares **INERT to
  `deploy/tool.py`** ("the tool reads only `carriers:`"). Deleting it is therefore not a
  fleet-distribution act.
- `release_lint` **C7** compares only entries with a **truthy spine** and those with
  **`freshness_gated: true`**. v1.5.0's ESSENTIALS row is `spine: []` +
  `freshness_gated: false`, so it is filtered out of *both* comparisons.
- `release_lint --version 1.5.0` before and after: **0 FAIL, 7 pass, 1 WARN** (C2, the
  pre-release tag). Unchanged.

The de-registration had already been done by `lane-x-628-docs-cut` (2026-09-13), which is
why the operational consumer set was reachable at all.

### 1.2 Surfaces followed (operational set 39 → 34 files)

Re-pointed, because each was a **live route** that dangles once the file is gone:

- `CLAUDE.md`, `README.md`, `protocols/README.md`, `protocols/ENVIRONMENT.md` — the
  "superseded, pending `[#628]`" roster and pointer lines.
- `templates/CLAUDE-md-template.md` — the onboarding template **every new repo is cut
  from**, which told each one to read `ESSENTIALS.md`.
- `protocols/PLAYBOOK.md` Ch2 "Authority hierarchy" item 1 — one of the two sites `[#628]`
  names **by anchor text**; reached by anchor, never by its quoted line number.
- `protocols/PLAYBOOK.md` living-doc registry rows, the per-repo table, the `last_reviewed`
  roster, the casing example.
- `protocols/HANDOFF_PROCESS.md` + `.claude/commands/{handoff,handoff-verify}.md` — the
  v6/v7 **exact-line-quote proof class** named ESSENTIALS as a quotable source. A deleted
  file cannot be quoted. No probe in the **active** bundle cited it (checked).
- `ARCHITECTURE.md` ×4 — two citations re-pointed to PLAYBOOK headings **verified live**
  (`:838` "Architect → operator channel-discipline", `:5290` "Architect routing for
  technical proposals"), the engine-loop conventions list, and the frontier-stages citation
  (VISION re-pointed to its real home `docs/archive/VISION.md`).
- `templates/handoff/02_METHODOLOGY.md.tmpl` — **five `{{PULL: ESSENTIALS#…}}` directives**,
  a breaker `[#628]`'s ten-consumer census did **not** enumerate.
- `ecosystem/disposition-register.yaml` — `warn-undeclared-essentials-handoff-process`
  **removed**, on the in-file VISION.md precedent (ADR-75: a source out of the organ's live
  scan can no longer match and would only decorate stale).
- `protocols/STANDING_RULINGS.md` **T-34** — **both** recorded Evidence locators were stale:
  `ESSENTIALS.md:86` was really `:90`, and `PLAYBOOK.md:1388` had drifted to `:1583`.

**RULING-W loses no home.** `ESSENTIALS.md:90` was a one-line summary pointing at PLAYBOOK;
the full statement lives at `protocols/PLAYBOOK.md:1583` and the ADR-36 / ADR-41 amendments
of 2026-07-18 carry the decision. Checked before deleting, not assumed.

### 1.3 Where an anchor could not be resolved, the death is stated

Only `Architect routing for technical proposals` survives as a live PLAYBOOK heading. The
other two `{{PULL}}` targets — `How Claude thinks`, `Starting a Session` — were dissolved
with the file, so the template now names its live home **by document** rather than by a
fabricated anchor. `STANDING_RULINGS` T-29 records that re-pointing by line number only
re-creates the rot; inventing a heading is the same error with better manners.

---

## 2 · The `[#667]` premise is REFUTED — the `≤ 15 KB` leg did not run

**Bytes: BEFORE 100,786 B → AFTER 100,845 B (+59 B).** The target is ≤ 15 KB. This lane did
not move toward it, and the +59 B is the cost of replacing four dead anchors with live ones.

Verified three ways rather than assumed:

1. `scripts/file_purpose_graph.py` exposes **only `why` and `stats`** — no emit/render
   subcommand, so there is nothing to render Ch2 *from*.
2. **No script writes `ARCHITECTURE.md`.** `audit.py`, `codemap/check.py`,
   `canonical_docs.py`, `canonical_freshness_gate.py` all only read it.
3. `[#664]`'s own body sequences the work away from here, verbatim: *"step D (the
   `ARCHITECTURE.md` Ch2 render) plus the organ map are **X3**, so a lane in X1 that does
   not render Ch2 is conforming, not short."* `[#667]` is `depends-on: #664`; `[#664]` stays
   open precisely because step D is X3.

Building that generator here would be a build arc owing **ADR-108 §B RED-first witnesses**
against a frozen acceptance criterion the architect sets. Cutting ~86 KB of prose by lane
judgment instead is worse: `[#667]` names the anti-pattern itself — *"rendering from a graph
that is not built is hand-maintenance wearing a generator's name."* Per the decision budget,
a refuted premise **PAUSEs with the fact (Q10)**.

### 2.1 Measurement, so the X3 lane starts from measurement

| Chapter | Bytes | Note |
|---|---:|---|
| Organ map | 25,251 | 11,157 B of it is 37 table rows |
| Validators and enforcement | 24,927 | only 1,476 B in tables — **~23 KB is prose** |
| Governing ADRs | 11,920 | |
| Verification mesh | 10,574 | |
| Distribution and transfer | 6,870 | |
| Key conventions & zones | 6,124 | |
| Automation axes | 5,918 | |
| Layer boundaries & invariants | 2,970 | |
| Purpose | 2,099 | |
| Authority and governance | 1,518 | |
| Codemap | 906 | already generated; `[#667]` would relocate it |

**Two constraints the X3 lane must not trip:**

- `ecosystem/organ-index.md` states **in its own header** that it does *not* carry failure
  posture and that "Ch2 carries it by hand and stays the source for it". Ch2 is therefore
  **not redundant** with the generated index and cannot simply become a pointer to it.
- The **246-line review prologue** `[#667]` expects to relocate into a JOURNAL entry is
  **already gone** — the header is now a ~25-line "How to read this doc". That byte budget
  cannot be spent twice.

The bulk is prose, so a table render alone cannot reach 15 KB.

---

## 3 · Proposed diffs (NOT applied here — each needs an act this lane may not perform)

**A · `templates/child-methodology-floor.md.tmpl:41`** — drop ESSENTIALS from
`full protocols (PLAYBOOK / ESSENTIALS)`:

```
- The methodology hub (`.dev-knowledge`) — full protocols (PLAYBOOK). Depth only; this floor is self-sufficient for a normal session.
```

*Why not here:* the floor is hash-guarded **three ways** (template bytes, `.sha256` sidecar,
`anchors.floor_sha256` in three live manifests) and `deploy/release_lint.py` C5 asserts the
three-way equality. Editing it **is** a release act, which `[#628]` says sequences **with**
the v1.5.0 release. The deletion did not force it: the line is stale prose, not a broken
route.

**B · The six `deploy/manifest-v*.yaml` `doc_shapes:` rows** — remove the
`protocols/ESSENTIALS.md` stanza. *Why not here:* `scripts/canonical_docs.py:255-268` records
the precedent that a shipped manifest's `doc_shapes` is answered by a **version bump, not a
retro-edit**. C7 ignores the rows meanwhile, so nothing is broken by waiting.

**C · `protocols/AI_COUNCIL_PROCESS.md` § "Section history"** — the 2026-09-04 entry, the
other site `[#628]` names. *Why not here:* the file's **live** citations were already
re-pointed to PLAYBOOK; what remains is a dated entry recording that re-point, which routes
nothing and stays true. It is a member of `audit._FRESHNESS_FILES`, so editing it forces a
`last_reviewed` re-stamp — and a stamp means "re-read end-to-end and confirmed accurate",
which its 424 lines did not receive here. **Left rather than stamped falsely.**

**D · `protocols/STANDING_RULINGS.md` T-29** — re-adjudicate. Its disposition rests on
"the target still exists under another name". After the deletion the target does not exist
at all. The disposition may still be right; the **reasoning** no longer holds. A lane does
not reopen a closed ruling.

---

## 4 · Open items

- `[#755]` carries A–E above as its Done-when.
- **`[#628]` is NOT closed.** Its Done-when requires the write-scope to cover "the floor
  sidecar and every pinned manifest"; it does not. The **deletion** — the act the contract's
  Done-contract item 1 names — is discharged. Closure is operator-gated through the ADR-70
  Tier-1 loop; a lane that retired the row would be answering a question the funnel exists
  to ask.
- **`tests/fixtures/repo-with-structural-checks/protocols/ESSENTIALS.md` KEPT.** `[#628]`
  asks the write-scope to say explicitly: it is a **293 B fixture stub, not a consumer**,
  and a sweep by filename would wrongly take it.
- `ecosystem/index.yaml` still carries an ESSENTIALS `undeclared_edges` evidence row. It is
  **generated audit state** (it still lists VISION.md, relocated long ago), and a lane does
  not regenerate indices — the integrator is gate-of-record.

---

## 5 · Verification

| Gate | Result |
|---|---|
| `ruff check .` | All checks passed |
| `canonical_freshness_gate.py --all` | exit 0 |
| `release_lint --version 1.5.0` | 0 FAIL, 7 pass, 1 pre-existing WARN (C2 tag) |
| `gen_task_tree.py --check` | ok — manifest, bodies and view reassemble byte-identically |
| `validate_backlog.py` | OK — 9 themes, 26 stories, 322 tasks, 2 pre-existing WARNs |
| pre-commit (all hooks) | pass, except the one declared bypass below |
| Targeted suite | **625 passed, 7 failed** — six pre-existing, **one caused by this diff**, attributed below |

### 5.1 Attribution — and one of them is mine

Per `[#528]` a lane runs the **targeted** tests for its own diff; the full suite runs once,
at integration. Attribution is by **reachability and measurement**, not by assertion.

**Caused by this lane — 1:**

- `test_the_live_playbook_doctrine_row_shows_its_reconciled_spec_and_a_derived_date` —
  **a tripwire that fired correctly.** This lane edited `protocols/PLAYBOOK.md` (Ch2
  "Authority hierarchy" item 1 — which `[#628]` *requires* by anchor text — plus the
  living-doc registry rows, the per-repo table, the `last_reviewed` roster and the casing
  example), so content landed 2026-09-14 **after** PLAYBOOK's prose `> Last updated:` stamp
  of 2026-09-08. The test asserts `CLASS_UNGATED_FRESH`, and its own comment says a flip
  back to STALE "is a real event that should be seen, not absorbed."
  **It is left RED deliberately.** Moving the prose date would turn it green without anyone
  re-reading the file — the exact false-stamp failure the test exists to catch, and ~6,100
  lines this lane did not read. The stamp is owed by the next pass that genuinely re-reads
  PLAYBOOK, and is filed as `[#755]` **item F**.

**Pre-existing — 6, none reachable from this diff:**

- `test_the_derived_leg_is_warn_class_on_arrival` — builds `_three_class_repo(tmp_path)` and
  monkeypatches `_FRESHNESS_FILES`. It **touches no live file**, so no edit here can reach
  it. (The deleted file carried `last_reviewed: 2026-09-01`, so it was never the "unstamped"
  member either.)
- `test_check_fleet_parity_green_on_live_repo` — names `settings.json` conductor/retention
  hooks and `ai-council` / `corp-monorepo` `.claude/commands/override.md`. Outside this diff.
- `test_health_ok_with_registered_repo`, `test_health_stays_ok_with_na_status` — both fail on
  `audit.py health` exit 1, whose **sole** blocking finding is the `journal_spine_anchor` gap
  in §5.2.
- `test_the_live_view_is_under_the_589_done_when_byte_bar` — `assert 91504 < 72000`.
  **Measured, not assumed:** `BACKLOG.md` was **91,281 B at `e6acb23e`**, already 19,281 B
  over the 72,000 B bar before this lane existed. Filing `[#755]` added 223 B to a
  long-standing red. Recorded plainly because the lane did make the number worse, even
  though it did not make the test fail — the `[#589]` byte-bar arc owns it.
- `test_registered_and_green_on_live_repo` (`test_task_tree_gate`) — **a dirty-tree artifact,
  not a defect.** The finding reads *"index and working tree disagree on
  `tasks/755-…md`"*: the suite ran while this packet's `[#755]` edit was still unstaged.
  `gen_task_tree --check` returns **ok**, and the gate is green once the tree is committed.

### 5.2 One declared single-hook bypass: `SKIP=audit-health`

After sync-merging `origin/main`, `audit.py health` carries **exactly one** `[!!]` finding:
`e6acb23e` — *the integrator's own anchor merge* — is itself unanchored on `main`.

The gate's **own prescribed discriminator** was run rather than assumed:

```
8a41c650 -> anchored in this tree: False / anchored at main: True   (tree lag — fixed by the sync)
e6acb23e -> anchored in this tree: False / anchored at main: False   (a real gap, on main)
```

Repairing it means writing a `JOURNAL.md` entry, which `STANDING_RULINGS` **P-1** and this
contract's *"What NOT to do"* both reserve to the integrator. So the finding is not
reachable from this diff and not repairable by this lane. Every other hook ran and passed on
all four commits. **This is the integrator's first item.**

---

## 6 · Handback

Nothing merged, nothing pushed, no JOURNAL entry, no index regenerated — commit-and-STOP.
The branch `worktree-lane-y-755-docs-cut-finish` holds four commits and a clean tree.
