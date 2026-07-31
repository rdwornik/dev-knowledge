# Night batch 2026-08-01 — L1: filing pre-pack

**Status: PROPOSAL — drafts ready to promote. NOTHING WAS FILED.** `docs/intake/` gained no file,
`BACKLOG.md` and `tasks/` gained no row, no `status:` was flipped. Everything below is report text.

**Done-contract: PARTIALLY MET — one item cannot meet it, and the reason is stated loudly below
rather than approximated.** Items (ii) and (iii) meet the contract in full: every drafted row would
pass `scripts/validate_backlog.py` unchanged. Item (i) **cannot**, for a reason no amount of drafting
fixes.

**Schema basis** (gathered read-only, quoted from validator source):
- Task row grammar — `scripts/validate_backlog.py:57` (`_TASK_RE`) + required-element checks at
  `:295-298`. Required: `[#NNN]`, `[P1-3][S|M|L]`, `Done when:`. Optional `·`-delimited clauses:
  `refs`, `depends-on:`, `serialize-group:`. `kill-candidates:` is carried inline by convention
  (115 occurrences in `BACKLOG.md`) **and** required in the commit message by
  `scripts/check_backlog_filing.py:35`.
- Accretion cap — `scripts/validate_doc_rot.py:56-58`: >1200 chars after `- [#id]` regardless of
  dates, **or** ≥3 dated blocks AND >700 chars. **Every row below was drafted under the 1200 cap.**
- Task filename — `scripts/gen_task_tree.py:231-247`, slug lowercased, non-alphanumerics → `-`,
  **truncated to 48 chars**, trailing hyphens stripped.
- Next free task id: **467** (highest present 466, verified by enumeration). Next free
  `intake-id`: **23** (highest present 22).

---

## ⚠ (i) The SEED intake doc — CONTRACT NOT MET, and here is exactly why

**The lane was asked for "schema-conformant frontmatter + operator text verbatim." The operator's
verbatim text is not in this repository, and was not supplied to the batch.**

Evidence (read-only sweep, whole tree excluding `.git`):
- `grep -rn "library-first\|library first" --include=*.md .` → **zero hits.**
- `grep -rn "rustworkx" ...` → **zero hits anywhere in the repo.**
- No intake doc, audit, JOURNAL entry, handoff `SUPPLEMENT.md`, or `RESIDUAL.md` carries a
  distillation/library-first operator dictation.

The nearest existing material is intake **#22 §D**
(`docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md:50-60`), which is a
*different, already-filed* item — it names repomix/pyadr/copier-cruft, not a library-first doctrine —
and it is `status: SEED`, explicitly NOT ratified by ADR-108.

**Why this is a stop, not a thing to paper over.** An intake doc's whole value is that its operator
text is verbatim — `docs/intake/README.md` §3 makes `origin` a required field precisely so a reader
can tell dictation from reconstruction. Writing CC-authored prose into a `func` intake and labelling
it operator input would corrupt the one property the corpus exists to guarantee. It would also be
undetectable later. So the draft below carries a **hard-fenced empty slot** instead.

### Drafted scaffold — schema-conformant, promotable ONLY after the slot is filled

**Filename:** `docs/intake/2026-08-01-func-distillation-and-library-first.md`
(grammar `YYYY-MM-DD-{func|tech}-slug.md`, ratified `docs/intake/README.md` §4:146 — convention,
not machine-enforced.)

```markdown
---
intake-id: 23
status: SEED
origin: operator, dictated <DATE/WINDOW — FILL FROM THE SOURCE CHAT>
consumed-by:
---

# Operator design input — distillation and library-first

<!-- class: func (operator design input) · status: SEED — NOT ratified; ingest per the intake
convention. Non-citable until ingested; repo wins on conflict. -->
<!-- origin: operator, dictated <DATE/WINDOW> -->

<!-- ============================================================================
     VERBATIM OPERATOR TEXT — PASTE BELOW THIS LINE, UNEDITED.
     This block is EMPTY BY DESIGN. The 2026-08-01 night batch could not fill it:
     the operator's dictation exists only in the source chat, not in this repo
     (verified: zero repo hits for "library-first" or "rustworkx").
     DO NOT promote this file with the slot empty, and DO NOT let an agent
     reconstruct the text from context — a `func` intake's frontmatter asserts
     the body is dictation. Paraphrase here is a false provenance claim.
     ============================================================================ -->

<!-- PASTE OPERATOR TEXT HERE -->

<!-- ==================== END VERBATIM OPERATOR TEXT ==================== -->
```

**Frontmatter conformance check** (against `docs/intake/README.md` §3 + `scripts/gen_intake_index.py:40`):
`intake-id` ✓ integer, next-free · `status: SEED` ✓ in the 7-value enum · `origin` ✓ required, slot
marked · `consumed-by:` ✓ present-and-empty, matching the live #22 pattern. No conditional key is
triggered (`decided-by`/`disposition` are ACCEPTED-only; `consumed-by` value is CONSUMED-only).
**No off-schema key.**

**Promotion checklist (three steps, in order):**
1. Paste the operator's verbatim text into the slot; fill both `<DATE/WINDOW>` placeholders; delete
   the fence comments.
2. Add the node to `docs/intake/manifest.json` — shape:
   `{"intake-id": 23, "status": "SEED", "filename": "2026-08-01-func-distillation-and-library-first.md", "title": "..."}`.
3. **Regenerate the index** — `python scripts/gen_intake_index.py --write`. The
   `intake-index-freshness` pre-commit hook (`.pre-commit-config.yaml:92-102`) **BLOCKS** a commit
   that adds an intake file without this.

---

## (ii) Rows a–e — drafted at ids 467–471, row-schema conformant

Ids are re-derived, not inherited: highest present is 466, so a–e take **467, 468, 469, 470, 471**.
All five are drafted under the 1200-char accretion cap.

### [#467] — repomix pilot (a)

```
- [#467] [P3][S] **Pilot repomix for CODE-context packing only — reject it for handoff/paste distillation** — intake #22 §D proposed repomix `--compress` as a boot-bundle distiller; the 2026-08-01 night batch measured it on OUR corpus and the premise fails: markdown is not a Tree-sitter compression target in repomix 1.17.0, so `--compress` is a byte-identical no-op that adds a ~37-token banner. Measured 0% reduction on 13/13 `protocols/` files and 5/5 bundle files, against -35.5% on `scripts/` Python; the live 52,119-B `PASTE_THIS.md` re-renders LARGER under every mode tested. What survives is a narrowed candidate: CLI-only code-context packing for an external-reviewer lane. Cost is real — repomix would be the second-ever npm dependency and `ecosystem/dependency-baseline.yaml` tracks Python surfaces only, so it lands outside the fleet parity gate · Done when: a ruling records either that repomix is declined for all surfaces, or that the code-context pilot ran with its ≥25%-savings-and-no-recall-regression bar met or missed · refs docs/audits/2026-08-01-technical-night-batch-l2-repomix-pilot.md, docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md §D, ADR-108, #449 · kill-candidates: none — no open row owns repomix; #449 is adjacent (paste budget) but this batch showed repomix cannot move that number
```

### [#468] — copier conditional re-open (b)

```
- [#468] [P3][S] **Record the copier/cruft evidence correction on [#387] — do NOT open a new template-engine row** — intake #22 §D lists copier/cruft as unfiled, but the question is not undecided: the 2026-07-21 vision audit weighed and REJECTED template engines as the fleet engine, restated under "do not relitigate" in three handoff records, and the copier deletion-propagation MODEL is already shipped and ratified (ADR-96). The 2026-08-01 night batch verified one sub-claim is WRONG and was wrong at authorship — copier#1833 (conflict markers vanishing in GUI merge tools) closed via PR#1907, shipped v9.5.0 2025-02-17, 17 months before the audit cited it. New and decision-relevant: cruft has had zero commits since 2024-12-25 with an open "Future of cruft" issue, while copier ships monthly. The load-bearing verdict (architectural fit, not bug-contingent) is unweakened · Done when: [#387] carries a note recording both corrections, or a ruling reopens the question with the audit's own falsification pilot as the entry gate · refs docs/audits/2026-08-01-technical-night-batch-l3-copier-record.md, docs/audits/2026-07-21-technical-night-vision-audit.md H4, ADR-96, ADR-109, #387 · kill-candidates: this row itself — if the architect rules the note belongs on [#387], fold it there and close this
```

### [#469] — why-not-python-frontmatter hygiene (c)

```
- [#469] [P3][S] **Record why the tasks/intake frontmatter parser is hand-rolled — no written rationale exists** — grep confirms zero hits for `python-frontmatter`/`ruamel` in ADR-107, ADR-109, `gen_task_tree.py`, `gen_intake_tree.py`, `docs/audits/`, LESSONS, or PLAYBOOK, so the hand parser is load-bearing with no checkable justification. Measured 2026-08-01 on 20 real fixtures: `python-frontmatter` is 0/20 byte-identical with no config escape (PyYAML `sort_keys=True` reorders every key; quote style re-derived; `BaseHandler.format()` strips the trailing newline). `ruamel.yaml` IS 20/20 faithful at `width>401` — the expected "library breaks byte-exactness" answer is TRUE of one library and FALSE of the other, so the honest rationale is redundancy, not fidelity: `gen_task_tree.py` templates frontmatter fresh from the body rather than round-tripping it · Done when: the why-not rationale is placed at one home (script docstring or LESSONS entry), naming both measured results · refs docs/audits/2026-08-01-technical-night-batch-l4-frontmatter-parser.md, ADR-107 §2, ADR-109 §3, scripts/gen_task_tree.py · kill-candidates: none — no open row owns parser rationale
```

### [#470] — codex-review model override (d)

```
- [#470] [P3][S] **Does /codex-review pin a review model, and should it be overridable per-invocation?** — the command is user-level (`~/.claude/commands/codex-review.md`), OUTSIDE this repo, so the 2026-08-01 night batch could NOT verify what model it selects or whether an override exists; `templates/codex-review-config-template.md` (the in-repo half) is a CLAUDE.md content template and names no model at all. The question matters because the review lane's verdict quality is model-dependent and the §C/§H portability work has started recording cross-provider review differences (grok caught two load-breaking defects terra missed), so an unpinned or silently-drifting reviewer model makes those comparisons unreproducible · Done when: a ruling records what the command pins today and either that the pin is correct as-is or that a per-invocation override is added, with the reviewing model named in the review artifact either way · refs docs/audits/2026-07-31-technical-382-w2-grok-shadow-ab.md, templates/codex-review-config-template.md, ADR-108 · kill-candidates: none — no open row owns reviewer-model selection; VERIFY FIRST, this row is written from outside the file it is about
```

> **Honest flag on [#470]:** this row is the weakest of the five. `~/.claude/` is not in this
> container, so the row is written from the *absence* of evidence. It is drafted question-shaped and
> carries an explicit VERIFY-FIRST marker. **Do not promote it without one look at the actual command
> file** — if the command already pins a model cleanly, the row is a no-op and should be dropped
> rather than filed.

### [#471] — audit.py cp1252 fix (e)

```
- [#471] [P3][S] **`audit.py checks` still crashes mid-listing on a cp1252 console — one U+2192 glyph** — `cmd_checks` (scripts/audit.py:3739) echoes each check's FIRST docstring line via `click.echo`; enumerating all check docstrings finds exactly one non-cp1252 character in that position: the `→` in `check_doc_code_edge` ("#194 doc→code declared-edge integrity"). The other 9 non-ASCII first-lines use `—` (0x97) and `§` (0xA7), both cp1252-encodable and therefore harmless. This is the same defect class fixed once before at `633e44a` (ASCII `->` swap) and recorded as observed-but-not-repaired in JOURNAL; the earlier PROBES workaround (`PYTHONUTF8=1`) was moved to prose because an env-prefix broke probe parsing, so no live mitigation is in place · Done when: the U+2192 is ASCII-swapped and a regression asserts every ALL_CHECKS docstring first line is cp1252-encodable · refs scripts/audit.py:3739 cmd_checks, tests/test_doc_code_edge.py::test_doc_code_edge_output_is_cp1252_safe, ADR-89 · kill-candidates: none — the existing cp1252 test covers Finding fields, not the `checks` listing path
```

---

## (iii) The rustworkx-swappable note — exact target location, with the lifecycle constraint

**The one-line note (drafted):**

> *The graph library is an implementation detail, not a contract: `rustworkx` is a drop-in
> alternative to `networkx` for the same edge/reachability queries, and the choice is deferred to
> whoever builds the consumer.*

### Exact target location — and why it is NOT the obvious one

Seventeen `networkx` references exist across the repo. **Most candidate homes are ineligible on
file-lifecycle grounds**, which is the load-bearing part of this item:

| candidate | lifecycle class | eligible? |
|---|---|---|
| `docs/decisions/ADR-109-…:51,170,253,267` | **IMMUTABLE** (ADR; only the status line is editable, ADR-94) | **No** — needs a new ADR or an amendment marker, not a one-line edit |
| `docs/audits/2026-07-28-technical-382-charter.md:22`, `…registry-prep-dossier.md:25,649`, `…schema-derivation-sol.md:8,467`, `…ladder-evidence.md:105` | **EVIDENCE-IMMUTABLE** (audits; amendment marker required) | **No** — a bare inline edit is not sanctioned |
| `docs/intake/*` (5 files) | LIVING | Eligible, but these are *inputs*, not the build contract |
| **`tasks/382-desired-state-data-model-intake-adr.md:13`** | **LIVING** (task file + its BACKLOG row) | **YES — this is the target** |

**Cited target: `tasks/382-desired-state-data-model-intake-adr.md`, line 13** — the [#382] row where
`(**networkx**)` is asserted as the dependency-graph mechanism. It is freely editable, it is the
place a builder actually reads, and it regenerates cleanly into `BACKLOG.md`.

**Two mechanical constraints on placing it there:**
1. `BACKLOG.md` is a **GENERATED** file (`tasks/` + `tasks/manifest.json` are source of truth). Edit
   the task file, then regenerate — never hand-edit `BACKLOG.md`.
2. [#382] is **CLOSED** (retire-not-delete: the task file remains as the allocation record with a
   terminal status). Appending to a closed row's text may be the wrong home for that reason alone.

> **Architect's call, and this batch does not presume it:** if a closed row is the wrong home, the
> next-best eligible target is **[#383]**'s task file — it is the open row that will actually build
> the graph, and it is the consumer ADR-105 requires before any graph library is chosen at all. That
> is a one-line judgment, so it is surfaced rather than decided here.

---

## Method note

Schema facts gathered by a read-only fan-out agent, quoted from validator source with `file:line`;
next-free ids re-derived by enumeration, not inherited from any document. Row drafts written by the
orchestrator and checked against `_TASK_RE`'s required elements and the 1200-char cap by inspection.
**No validator was run against the drafts** — they are report text, not files, so there is nothing on
disk for a validator to read. Promotion should run `python scripts/audit.py health` (or the
`validate-backlog` hook) as the real check.
