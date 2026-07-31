# Intake #22 §D — research rows input dossier (repomix / pyadr / copier·cruft)

**Status: PROPOSED — research input; candidate rows are drafts, not filed**

**Scope:** Read-only grep-first sweep + bounded capability research for the three tools named in
intake #22 §D, prepared as morning-architect INPUT. Nothing here is a ruling. No candidate row has
been filed; `BACKLOG.md` and `docs/intake/` were not modified. This file is the only write.
Produced 2026-07-31 by a read-only analysis agent.

## Network access

**Research leg RAN.** `WebSearch` and `WebFetch` both reachable. Note: `repomix.com` returns
HTTP 403 to `WebFetch` (docs site blocks the fetcher), so repomix capability facts are sourced
from `github.com/yamadashy/repomix` and from `WebSearch` result summaries of the repomix docs
pages rather than from a direct fetch of those pages. One repomix sub-question could not be
resolved (see its §ii caveat) and is left open rather than guessed.

## What intake #22 section D actually says

Section D **exists** and names **exactly** the three tools in the task. Source:
`docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md` lines 50–60.

```
50  ## D. Context-distiller pre-phase (research 2026-07-27 — currently unfiled, do not lose)
51
52  - **repomix `--compress`** — deterministic Tree-sitter distillation of files before an agent
53    reads them (token counts per file, MCP server). Operator's intent: a "booster/pre-phase"
54    so agents stop skimming large markdown/code. Candidate consumer: the §B(b) boot bundle
55    itself (distillate instead of raw files) and any read-heavy lane.
56  - Siblings from the same research pass, also unfiled: **pyadr** (ADR lifecycle CLI),
57    **copier/cruft** (fleet template propagation — directly serves the "change X for all
58    repos at once" requirement in §E).
59  - Ask: verify none has a row (grep), then file as research-consumption rows; sequence after
60    [#446] as cheap standalone items.
```

Two governing facts about §D's status, both in-repo:

- The intake is `status: SEED` (frontmatter line 3) and carries
  `**NOTE 2026-07-31:** §A + §B ratified by promotion → ADR-108. §C–§H remain unratified.` (line 8).
- `docs/decisions/ADR-108-decision-routing-and-engineering-standards.md:60` lists
  `- **§D** context-distiller pre-phase (repomix `--compress`, pyadr, copier/cruft)` under the
  heading *"Scope boundary — what this ADR does NOT ratify"*, with the surrounding text
  (lines 56–57) reading: *"Intake #22 remains `status: SEED`; §C–§H are NOT ratified by this ADR.
  Specifically unratified and still SEED-class (non-citable as ruled doctrine)"*.

So §D's own ask — "verify none has a row (grep), then file as research-consumption rows" — is
itself unratified. The grep leg below is the part §D asks for; the filing decision is the
architect's.

---

## 1. repomix (`--compress`)

### (i) Grep-first — does this repo already reference or consume it?

**10 hit lines across 7 files. Zero in any dependency manifest. Zero in executable code.**

Sweep: case-insensitive `repomix` across the whole tree excluding `.git`.

Dependency-manifest result — **zero hits** in all four manifests present
(`package.json`, `package-lock.json`, `pyproject.toml`, `uv.lock`). The tool is **not installed
and not declared** anywhere.

Directory distribution: `docs/` only (7 files). Nothing in `scripts/`, `protocols/`,
`ecosystem/`, `deploy/`, `templates/`, `.claude/`, `plugins/`, `BACKLOG.md`, `JOURNAL.md`,
`LESSONS.md`.

Hits:

- `docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md:52` — the §D entry
  itself (quoted above).
- `docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md:104` —
  `what the plan already builds. §D's repomix is NOT injected into the boot build.)`
- `docs/decisions/ADR-108-decision-routing-and-engineering-standards.md:60` — the
  explicitly-NOT-ratified list.
- `docs/handoffs/2026-07-26-dev-knowledge-architect/SUPPLEMENT.md:83` (and its verbatim twin
  `.../PASTE_THIS.md:631`) — the 2026-07-26 research pass, the richest prior in-repo statement:
  `(e) Distiller: DETERMINISTIC extraction, not LLM summarization. repomix (--compress via`
  `Tree-sitter, git-aware, token counts, MCP) as session input; bounded one-question probes`
  `returning verbatim quote + file:line as verification. The PERMANENT distiller for the`
  `backlog is the restructure itself — per-task files are queried, not read.`
- `docs/handoffs/2026-07-31-dev-knowledge-architect-2/SUPPLEMENT.md:70` (twin
  `.../PASTE_THIS.md:566`) — `research rows (repomix / pyadr / copier — **grep-first**) + **§C/§H**: the grok shadow and the`
- `docs/archive/2026-04-27-handoff-patterns-external-research.md:133` and `:309` — an external
  research dump that describes Repomix third-hand (packing a codebase into one XML/Markdown file
  for a browser chat) and cites `repomix.com` as source 26.

**Reading:** no row, no dependency, no consumption path. There IS prior architect-side research
(2026-07-26) that already characterized it favorably as *session input*, and the same record
already ruled the permanent backlog distiller is the restructure, not a tool. §D's grep
precondition ("verify none has a row") is satisfied — no `BACKLOG.md` row exists.

### (ii) Capability summary vs our need (HANDOFF COMPRESSION)

Our need anchor, measured: `scripts/assemble_paste.py` carries two byte budgets —
`_SIZE_WARN_BYTES = 65_000` for `PASTE_THIS.md` (line 32, comment at line 29 notes "The healthy
filled paste is ~59 KB") and `HANDOFF_BOOT_BYTE_BUDGET = 18_000` for `protocols/HANDOFF_BOOT.md`
(line 44, ruled 2026-07-31, enforced as WARN at assembly and FAIL via
`audit.py::check_boot_byte_budget`).

Researched (sources below):

- `--compress` uses Tree-sitter parsing to keep imports/exports/class+function/interface
  signatures and drop function bodies, loop/conditional internals, and local variable
  assignments. Documented as roughly **~70% token reduction**, explicitly **lossy**, and marked
  **experimental** by the maintainers.
- Repomix packs a whole repo into one file; output styles are XML (default), Markdown, JSON,
  plain text. It is `.gitignore`-aware.
- `--token-count-tree` gives hierarchical per-directory/per-file token counts with a minimum
  threshold — this is the *measurement* half and is independent of `--compress`.
- `repomix --mcp` runs an MCP server exposing pack-local/pack-remote, search-packed-output, and
  partial file reads.
- **Fit caveat, unresolved:** the compression is described purely in terms of *code* constructs
  (signatures, bodies, imports). Our handoff corpus is **markdown**, not code. The docs found do
  not enumerate the Tree-sitter language list, and `repomix.com/guide/code-compress` 403s to the
  fetcher, so I could not confirm whether Markdown is a supported compression target or what
  happens to unsupported types. **This is the load-bearing question for our use case and it is
  open** — do not assume markdown compresses.
- Secondary caveat: repomix is an npm/Node tool; the repo's Python toolchain is uv-pinned
  (ADR-106), so it would add a second runtime to the gate environment.

Sources: [github.com/yamadashy/repomix](https://github.com/yamadashy/repomix),
[repomix.com/guide/code-compress](https://repomix.com/guide/code-compress) (via search summary; direct fetch 403),
[repomix.com/guide/command-line-options](https://repomix.com/guide/command-line-options) (via search summary).

### (iii) Draft candidate row — QUESTION-SHAPED, NOT FILED

```
- [#TBD] [P3][S] **Does repomix `--compress` actually help the handoff byte budget, or is it a code-only tool pointed at a markdown corpus?** — intake #22 §D (SEED, explicitly NOT ratified by ADR-108) asks that repomix be filed as a research-consumption row; grep confirms zero rows, zero manifest entries, zero code references. The open question is fit, not availability: `--compress` is documented as Tree-sitter extraction of *code* structure (signatures kept, bodies dropped, ~70% token reduction, lossy, vendor-marked experimental), while our budget pressure is on markdown — `PASTE_THIS.md` at a 65,000-byte warn and `HANDOFF_BOOT.md` at an 18,000-byte ruled budget. Unresolved by research: whether Markdown is a supported compression language at all, and what the tool does with unsupported types. Also unasked: whether the wanted capability is compression or merely `--token-count-tree` measurement, which needs no adoption decision; and whether an npm/Node tool is admissible beside the uv-pinned toolchain (ADR-106). Prior in-repo research (2026-07-26) already characterized repomix as *session input* and ruled the permanent backlog distiller is the restructure, not a tool — so this row must not silently re-scope that. · Done when: a ruling records whether repomix is evaluated, deferred, or declined for handoff compression, naming the markdown-support finding and the compression-vs-measurement distinction · refs docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md §D, docs/decisions/ADR-108-decision-routing-and-engineering-standards.md, scripts/assemble_paste.py, protocols/HANDOFF_PROCESS.md, docs/handoffs/2026-07-26-dev-knowledge-architect/SUPPLEMENT.md §(e) · kill-candidates: TBD by architect — this row is itself a kill candidate if the answer is "measurement only, no adoption question exists"
```

---

## 2. pyadr

### (i) Grep-first — does this repo already reference or consume it?

**7 hit lines across 7 files. Zero in any dependency manifest. Zero in executable code.**

Sweep: case-insensitive `pyadr` (also swept `py-adr`, `adr-tools`, `adr_tools` — no additional
hits) across the whole tree excluding `.git`.

Dependency-manifest result — **zero hits** in `package.json`, `package-lock.json`,
`pyproject.toml`, `uv.lock`. Not installed, not declared.

Directory distribution: `docs/` only. Nothing in `scripts/`, `protocols/`, `ecosystem/`,
`deploy/`, `templates/`, `.claude/`, `plugins/`, `BACKLOG.md`, `JOURNAL.md`, `LESSONS.md`.

Hits:

- `docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md:56` — the §D sibling
  entry: `- Siblings from the same research pass, also unfiled: **pyadr** (ADR lifecycle CLI),`
- `docs/decisions/ADR-108-decision-routing-and-engineering-standards.md:60` — the
  NOT-ratified list.
- `docs/decisions/ADR-107-backlog-restructure-engine-schema-viewer.md:365` — the most
  load-bearing prior mention, **already a deferred evaluation**:
  `use `pyadr` off the shelf; that is a later evaluation, not a decision here.`
  In context (lines 360–365) this attaches pyadr to the **genre-lifecycle second leg** of the
  backlog restructure: *"one schema for every genre, `status` in frontmatter ⇄ folder, a
  validator that FAILs the mismatch, and a command that moves the file… Its ADR-transition half
  may use `pyadr` off the shelf"*.
- `docs/handoffs/2026-07-26-dev-knowledge-architect/SUPPLEMENT.md:98` (twin `PASTE_THIS.md:646`) —
  the originating research line:
  `pyadr covers the ADR transitions (proposal/accepted/rejected/deprecated/superseding) off`
  `the shelf. Per-task files WITHOUT this leg would be the same rot in smaller packages.`
- `docs/handoffs/2026-07-31-dev-knowledge-architect-2/SUPPLEMENT.md:70` (twin `PASTE_THIS.md:566`)
  — the task-assignment line.

**Reading:** no `BACKLOG.md` row, but pyadr is **not un-owned** — ADR-107 §7.3/7.4 already names
it as a later evaluation belonging to the genre-lifecycle leg of the backlog restructure. A new
standalone row risks creating a second home for a question ADR-107 already parked.

### (ii) Capability summary vs our need (ADR TOOLING)

Our need anchor, measured: 81 ADR files in `docs/decisions/` plus 2 in `docs/decisions/archive/`
(83 total; highest number ADR-108, so numbering is sparse), a hand-maintained
`docs/decisions/README.md` index with 128 `| ADR-` rows covering 82 unique ids, the
`ADR-NN-topic.md` naming grammar (CLAUDE.md §4), and the §5 rule-3 immutability rule with the
ADR-94 status-line exception.

Researched (sources below):

- pyadr is a CLI for the ADR lifecycle — proposal / acceptance / rejection / deprecation /
  superseding — over Markdown files plus git.
- Commands: `init`, `new`/`propose`, `accept`, `reject`, `deprecate`, `supersede`, `toc`,
  `helper`, `check-adr-repo`, `config`; a `git adr` extension adds branch/staging/pre-merge
  validation.
- `toc` generates a table of contents as `index.md` — the closest thing to our hand-maintained
  `README.md` index.
- **Naming collision:** pyadr follows the MADR-0005 convention, `<next-available-id>-<title-in-lowercase>.md`
  (e.g. `0007-use-postgres.md`). Our grammar is `ADR-NN-topic.md`. Not the same shape.
- **Immutability collision:** on accept/reject pyadr **renames the file** (`XXXX-<title>` →
  `<next-id>-<title>`) **and rewrites in-file metadata (status, date)**. Our §5 rule 3 forbids
  in-place ADR edits except the ADR-94 status-line carve-out; a rename is not covered by that
  carve-out at all.
- **Maturity:** the project self-describes as **pre-alpha**; `deprecate` and `supersede` are
  documented as *not yet implemented* — which are precisely the two transitions ADR-107's
  genre-lifecycle leg is about. ~58 stars, ~258 commits, 9 open issues / 10 open PRs at time of
  fetch; latest PyPI line seen is 0.19.0. Low-traffic project.

Sources: [github.com/opinionated-digital-center/pyadr](https://github.com/opinionated-digital-center/pyadr),
[libraries.io/pypi/pyadr](https://libraries.io/pypi/pyadr),
[adr.github.io/adr-tooling](https://adr.github.io/adr-tooling/).

### (iii) Draft candidate row — QUESTION-SHAPED, NOT FILED

```
- [#TBD] [P3][S] **Is pyadr a standalone research row at all, or is it already ADR-107's deferred evaluation wearing a second ticket?** — intake #22 §D (SEED, NOT ratified by ADR-108) lists pyadr as an unfiled sibling; grep confirms zero rows and zero manifest entries, but ADR-107:365 already says its ADR-transition half "may use `pyadr` off the shelf; that is a later evaluation, not a decision here", scoped to the genre-lifecycle SECOND LEG of the backlog restructure. So the first open question is routing, not tooling: does a new row duplicate a parked ADR-107 evaluation? If it survives that, the tool-fit questions are unanswered too — pyadr's MADR-0005 naming (`<id>-<title-lowercase>.md`) is not our `ADR-NN-topic.md` grammar; its accept/reject path RENAMES the ADR file and rewrites in-file status/date, which the §5 rule-3 immutability rule permits only for the ADR-94 status-line carve-out and not at all for renames; and its `deprecate`/`supersede` commands — the two transitions the genre-lifecycle leg actually needs — are documented as not yet implemented in a self-declared pre-alpha project. Whether the wanted artifact is the tool or only its `toc` behaviour (against a hand-maintained 128-row README index over 83 ADR files) is also unasked. · Done when: a ruling records either that pyadr is subsumed by ADR-107's deferred evaluation, or that it is a distinct row, naming the naming-grammar and immutability findings either way · refs docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md §D, docs/decisions/ADR-107-backlog-restructure-engine-schema-viewer.md §7.3–7.4, docs/decisions/ADR-108-decision-routing-and-engineering-standards.md, docs/decisions/README.md, CLAUDE.md §4–§5 · kill-candidates: TBD by architect — this row is a kill candidate against ADR-107's existing parked evaluation
```

---

## 3. copier / cruft

### (i) Grep-first — does this repo already reference or consume it?

**Heavily referenced: 45 `copier` hit lines, 28 `cruft` hit lines, 2 `cookiecutter` hit lines.
Zero in any dependency manifest. Two references in executable code — both as an adopted MODEL,
not as a dependency. This tool pair is NOT un-referenced; it has already been RULED ON.**

Dependency-manifest result — **zero hits** for `copier`, `cruft`, `cookiecutter` in
`package.json`, `package-lock.json`, `pyproject.toml`, `uv.lock`. Not installed, not declared.

Directory distribution for `copier`: `docs/` 17 files, `deploy/` 2 files, `BACKLOG.md`,
`tasks/`. For `cruft`: `docs/` 10 files only.

Load-bearing hits:

**Code (model-only, not a dependency):**
- `deploy/carrier_precommit.py:925` —
  `# delete — surface the conflict (copier deletion-propagation model).`
- `deploy/contract.py:128` —
  `the copier deletion-propagation hash-guard: a template-deleted file the`

**Ratified decision:**
- `docs/decisions/ADR-96-deploy-remove-leg.md:22` —
  `2. **Hash-guard (the copier deletion-propagation model, adopted — not the tool).**`
- `docs/decisions/ADR-96-deploy-remove-leg.md:45` — `…the copier model compares against last-rendered…`
- `docs/decisions/README.md:85` — the ADR-96 index row repeats
  `Hash-guarded (the copier deletion-propagation model: a locally-modified target is **REFUSED**, never clobbered)`

**Standing rejection with evidence — `docs/audits/2026-07-21-technical-night-vision-audit.md`:**
- `:38` frames the brief's bet: `adopt a template engine (Copier/cruft), hub as template repo…`
- `:155–167` the evidence: cruft has *"no common ancestor → conflicts harder than git merges;
  users 'roll back and give up'"*, emits `.rej` but *"**still bumps the pinned hash** — drift
  marked resolved while never applied"*, 3-way merge breaks in clean CI clones (cruft#181, open
  since 2022); Copier better but *"its inline conflict markers silently disappear in GUI merge
  tools (copier#1833)"*.
- `:178–183` the verdict: *"adopting Copier/cruft as the engine would be trading a working
  regenerate-model for a merge-replay model the field is abandoning at exactly this fleet's
  divergence profile. What IS worth taking from Copier is the one idea the brief names
  correctly — **the consumer pins a template version and the pin is the desired-state hash**"*.
- `:185–188` a **named falsification test**: *"pilot `copier update` on one consumer across 3 hub
  template revisions with its real `.methodology.yaml` divergences in place; count conflicts and
  silent mis-merges… If Copier wins on cost at n=1 consumer, H4 is wrong and the pivot is
  justified; record either outcome as an ADR so the fork stops living in prompts."*
- `:300–303` `**Hand-rolled carrier/regen engine instead of Copier/cruft** — JUSTIFIED divergence`

**Explicit do-not-relitigate markers (handoff records):**
- `docs/handoffs/2026-07-21-dev-knowledge-architect/SUPPLEMENT.md:82–84`, under the heading
  `3. CONSIDERED + REJECTED (do not relitigate)`:
  `- Template engine adoption (Copier/cruft as the fleet engine) — REJECTED by the vision audit on`
  `  evidence: merge-replay fails at this divergence profile; the hub is already regenerate-shaped.`
  `  Keep only the version-pin scalar. Do not re-open "should we adopt Copier".`
- `docs/handoffs/2026-07-23-dev-knowledge-architect/SUPPLEMENT.md:95–97`, same heading:
  `Template engines (Copier/cruft: merge-replay fails our divergence profile; hub is already regenerate-shaped; kept only the per-consumer version-pin scalar)`
- `docs/handoffs/2026-07-03-dev-knowledge-architect/SUPPLEMENT.md:75–76`:
  `- copier-LITERAL (adopt as a dependency) — rejected (templating doesn't fit organs with firing acceptance; the carriers are proven). Adopt the copier MODEL (deletion-propagation), not the tool.`

**Live open row referencing it:**
- `BACKLOG.md:249` = `tasks/387-rewrite-the-buy-vs-build-intake-before-anything.md:13` — `[#387]`
  `**Rewrite the buy-vs-build intake BEFORE anything ingests it** — intake **#2** … **argued FOR
  the template engine that was subsequently rejected** … Rewrite it against the ruled position —
  **adopt the MODEL, not the tool** (Copier → regenerate-and-diff; …)`
- `docs/intake/2026-07-21-func-fleet-north-star.md:59, :69, :119` — the "adopt the model, not the
  tool" doctrine and `per-consumer version-pin scalar (the one idea kept from Copier)`.
- `docs/intake/2026-07-28-north-star-delta-review.md:97` — `the doc's own Copier precedent is
  settled. But **[#387]** is OPEN`.

**Reading — the most important finding in this dossier:** §D's premise for copier/cruft
("also unfiled") is **incorrect as to the decision**, though technically correct as to the row.
There is no `BACKLOG.md` row *proposing copier/cruft adoption*, but the fleet-template-engine
question was **weighed on evidence and REJECTED** (2026-07-21 vision audit), the rejection was
recorded twice under explicit "do not relitigate" headings, the Copier *model* is already adopted
in shipped code (`deploy/`) and ratified (ADR-96), and there is an **open row [#387]** whose whole
purpose is to stop a stale pro-template-engine argument from being re-imported. Filing §D's
copier/cruft row as written would do approximately what [#387] exists to prevent.

### (ii) Capability summary vs our need (TEMPLATE PROPAGATION)

Our need anchor: methodology corpus pushed hub → consumers via `deploy/manifest-v*.yaml` +
`templates/`, with per-consumer drift/pins as the pain point.

Researched (sources below):

- Copier: platform team maintains versioned templates; consumers scaffold and later run
  `copier update`, which pulls latest template changes, compares against the project's recorded
  template version, and merges the differences. Supports versioned tags and scripted migrations.
- Conflict handling: `--conflict inline` (default, conflict markers written into files) or
  `--conflict rej` (separate `.rej` files).
- Cruft: Cookiecutter-based; the consensus in the sources is that cruft only makes sense when an
  existing Cookiecutter template is already in place *and* customized-file/template-update overlap
  is minimal — i.e. when conflicts are rare. Copier is described as the clear choice otherwise.
- This **matches**, rather than contradicts, the 2026-07-21 in-repo audit: both are merge-replay
  engines, and their conflict behaviour is the failure surface at heavy declared divergence.
- The in-repo audit's alternative (regenerate-don't-merge, projen-shaped) is already what the hub
  is; the audit's own recommendation was to keep the engine and take only the version-pin scalar.
- Nothing found in this pass contradicts the 2026-07-21 evidence; no capability change since then
  surfaced in the search results.

Sources: [copier.readthedocs.io/en/stable/updating](https://copier.readthedocs.io/en/stable/updating/),
[copier.readthedocs.io/en/stable/comparisons](https://copier.readthedocs.io/en/stable/comparisons/),
[cruft.github.io/cruft](https://cruft.github.io/cruft/),
[blenddata.nl — Cruft vs copier](https://www.blenddata.nl/en/blogs/cruft-vs-copier-automating-template-updates-at-scale).

### (iii) Draft candidate row — QUESTION-SHAPED, NOT FILED

```
- [#TBD] [P3][S] **Does intake #22 §D's copier/cruft ask survive the standing rejection, or is filing it the exact re-import [#387] exists to prevent?** — §D (SEED, NOT ratified by ADR-108) lists copier/cruft as an "unfiled" sibling serving §E's "change X for all repos at once" requirement. Grep says: no BACKLOG row proposing adoption, but the question is not un-decided — the 2026-07-21 vision audit weighed and REJECTED template engines as the fleet engine on merge-replay evidence (cruft bumps the pinned hash on unresolved conflicts; copier's inline markers vanish in GUI merge tools), the rejection is recorded under explicit "do not relitigate" headings in two handoff records, the Copier deletion-propagation MODEL is already adopted in shipped code and ratified by ADR-96, and [#387] is OPEN precisely to stop a stale pro-template-engine argument being re-imported as live. Open questions for the architect, none answered here: is §D's mention a genuine reopen request or an operator restating an unfiled research note without knowing it was already ruled; if a reopen, does it clear the audit's own named falsification bar (pilot `copier update` on one consumer across 3 hub template revisions with real `.methodology.yaml` divergences, count conflicts and silent mis-merges, record either outcome as an ADR); and does §E's fleet-management requirement need copier at all, or only the already-kept per-consumer version-pin scalar. Independent research this pass found nothing contradicting the 2026-07-21 evidence. · Done when: a ruling records either that §D's copier/cruft item is closed by the standing rejection, or that it is reopened with the falsification pilot as its entry gate · refs docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md §D+§E, docs/audits/2026-07-21-technical-night-vision-audit.md H4 (lines 150–188, 296–303), docs/decisions/ADR-96-deploy-remove-leg.md, docs/handoffs/2026-07-21-dev-knowledge-architect/SUPPLEMENT.md §3, deploy/contract.py, #387, #382 · kill-candidates: this row itself, if the architect rules §D's mention is already answered by the standing rejection — in which case the correct action is a note on [#387], not a new row
```

---

## Cross-cutting observations for the architect (input, not rulings)

1. **§D's grep precondition is satisfied for all three** — none has a `BACKLOG.md` row, none is
   in any dependency manifest, none is installed. Filing three rows is *mechanically* consistent
   with §D's ask.
2. **But two of the three are already owned elsewhere.** pyadr is ADR-107's deferred evaluation;
   copier/cruft is a standing evidence-based rejection with an open corrective row ([#387]).
   Only repomix is genuinely unowned. Three rows may over-file by two.
3. **§D is itself unratified** (ADR-108 scope boundary, line 60) — the filing decision is open,
   not implied by the ADR-108 promotion of §A/§B.
4. **Backlog-equilibrium tension:** §F of the same intake states "The backlog must SHRINK — that
   is a functional requirement, not a review item"
   (`docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md:74`). Filing three
   new rows from §D runs against §F of the same document. The hub's own
   `backlog-filing-backpressure` commit-msg gate would require a `kill-candidates:` line on each.
5. **Sequencing as written:** §I item 3 places §D's filing in the "first ruling batch after
   [#446]" alongside the §A/§B ratification that has now happened — so the timing trigger has
   fired even though the content is unratified.

## Method note

Read-only. Sweeps were case-insensitive `grep -rniI` across the full tree excluding `.git`,
plus targeted greps of `package.json`, `package-lock.json`, `pyproject.toml`, `uv.lock`,
`BACKLOG.md`, `JOURNAL.md`, `LESSONS.md`, and the `scripts/ protocols/ ecosystem/ deploy/
templates/ .claude/ plugins/` trees. Counts are hit *lines*, not files, unless stated. No git
operations were performed; no file other than this one was created or modified.
