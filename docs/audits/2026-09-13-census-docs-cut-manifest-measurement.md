# Docs-cut manifest — byte and reader census (lane-x-000)

> Proposal-only measurement for `LANE-x-000-docs-cut-manifest.md`. **Nothing is cut here.**
> Five named sections — ARCHITECTURE's prologue, ARCHITECTURE's table of contents,
> CLAUDE.md's prologue, ESSENTIALS.md, PLAYBOOK's prologue — measured for bytes (Step 1)
> and readers (Step 2). The docs-cut list this census feeds is
> `to-browser/DOCS-CUT-LIST-2026-09-13.md`.

## Step 1 — bytes per section, measured from the files

Boundaries are the line ranges given below; each was located by the first heading/marker
that ends the section, not by any prose restating a size. Byte counts are `sed -n
'<range>p' <file> | wc -c` against the checked-out LF-encoded files (verified: `file`
reports "Unicode text, UTF-8 text" for all four, no CRLF).

| Section | File | Lines | Bytes | Boundary evidence |
|---|---|---|---|---|
| ARCHITECTURE's prologue | `ARCHITECTURE.md` | 1–276 | **30,122 B** | ends immediately before `## Purpose [CORE]` at `ARCHITECTURE.md:277` |
| ARCHITECTURE's table of contents | `ARCHITECTURE.md` | — | **0 B — does not exist** | see below |
| CLAUDE.md's prologue | `CLAUDE.md` | 1–17 | **964 B** | ends immediately before `## 1. First read (session start)` at `CLAUDE.md:18` |
| ESSENTIALS.md (whole file) | `protocols/ESSENTIALS.md` | 1–189 | **16,461 B** | whole file — already SUPERSEDED per its own header, `[#628]` |
| PLAYBOOK's prologue | `protocols/PLAYBOOK.md` | 1–102 | **7,836 B** | ends immediately before `<!-- TOC:START -->` at `protocols/PLAYBOOK.md:103` |

For context, whole-file totals (same measurement method): `ARCHITECTURE.md` 129,213 B ·
`CLAUDE.md` 24,090 B · `protocols/PLAYBOOK.md` 506,729 B · `protocols/ESSENTIALS.md`
16,461 B.

### ARCHITECTURE's table of contents does not exist

`grep -in toc ARCHITECTURE.md` finds no TOC heading or marker — only prose mentions of
"ToC" as a concept in Ch2/Ch6/Governing-ADRs text. `git show f7a548d2` (2026-07-11,
*"docs(architecture): strip ToC + un-gate toc-freshness (hub leg [#326])"*) confirms this
was deliberate: the commit deleted the TOC block from `ARCHITECTURE.md` **and** removed
the file-specific `toc-freshness` pre-commit hook in the same act (the commit's own
"mandatory gate-collision pairing" note), because *"ARCHITECTURE.md is CC-facing"*
(operator ruling 2026-07-11). `PLAYBOOK.md` keeps `toc-freshness-playbook`; the ToC
convention is PLAYBOOK-only from that commit forward. This item of the Done-contract is
therefore not "measure a section" but "confirm a section's absence" — a materially
different finding from a section that exists but has no reader (§2 below).

### CLAUDE.md's prologue against its own byte cap

`CLAUDE.md`'s prologue (964 B) states the file's own cap: **≤ 24,576 B**, gated by
`tests/test_claude_md_byte_cap.py`. The whole file measures 24,090 B — **486 B of
headroom** against the cap, of which the prologue itself consumes 964 B (4.0% of the
file). Headroom is what would make a cut of this file's *other* sections decidable; the
prologue's own share of the budget is reported here as the fact a cut proposal would need,
not as a recommendation — this lane proposes nothing.

## Step 2 — readers found per section

Method: for each section, find what currently imports it, links to it, cites it as a
locator, or reads/parses it at gate time. Excluded as non-readers: `docs/handoffs/**` and
`docs/audits/**` — dated, immutable records that once mentioned a filename are not a
*current* reader of it. A whole-file reader (e.g. a freshness-gate script that opens the
file for its frontmatter) is reported separately from a reader of the specific
prologue/TOC prose, because the two are different claims — a section can have the first
and lack the second, and that gap is itself a finding per the Done-contract's own framing
("a section with no reader is the finding").

| Section | Frontmatter/whole-file readers | Prose-body readers | Verdict |
|---|---|---|---|
| ARCHITECTURE's prologue | 2 — `scripts/canonical_freshness_gate.py:180` (reads `last_reviewed`/`reconciled_with`, file is in `FRESHNESS_FILES`, `canonical_docs.py:166`); `scripts/audit.py:964-986` (`doctrine_table`, `reconciled_with` fallback) | **0 found** — no locator anywhere cites a line number inside 1–276; `CLAUDE.md` §3's own pointer ("Where to jump: Ch2… Ch3… Ch4… Ch6") routes *past* the prologue into chapters | frontmatter read; ~29.7 KB of prose (99% of the section's bytes) has no reader found |
| ARCHITECTURE's table of contents | n/a — does not exist | n/a | nothing to read; see Step 1 |
| CLAUDE.md's prologue | 2 — same freshness-gate mechanism (CLAUDE.md is also in `FRESHNESS_FILES`); plus line 14's `≤24,576 B` cap is read live by `tests/test_claude_md_byte_cap.py:138-157` via `_DECLARED_CEILING_RE` (line 90) | The prologue's own "auto-read at session start" claim (line 12) has **no in-repo mechanism performing that read** — `.claude/settings.json`'s SessionStart hooks (`fleet_health.py`, `surface_triage.ps1`, `billing_leak_sentinel.ps1`, `changelog_sentinel.py`, `arm_hooks.py`, `conductor.py`) open none of them; the auto-read is a Claude Code harness behavior external to this repo | 2 distinct live readers touch this prologue's actual content (frontmatter + the byte-cap line); the boot-read claim itself is unverified by any in-repo mechanism |
| ESSENTIALS.md (whole file) | 4 registry memberships (`CANONICAL_OPTIONAL` `canonical_docs.py:150`; `FRESHNESS_FILES` `:166-167`; `SECTION_HISTORY_DOCS` `:252`; `STRUCTURE_DOCS` `:259`) **+ 1 live content read** — `canonical_freshness_gate.py:52` (`DEFAULT_FRESHNESS_FILES`) parses its `last_reviewed` frontmatter and re-dates it | `scripts/assemble_paste.py:76`'s "ESSENTIALS one-liner" is a string literal in a nudge message, not a code path that opens the file | superseded per its own header and `CLAUDE.md` §4 ("do not boot from it"), but **not inert** — the freshness gate still re-reads and re-dates a file no session is told to open |
| PLAYBOOK's prologue | line 2's `reconciled_with: handoff-process@7.1.0` has 3 live readers — `scripts/coherence_nudge.py:37,89` (`_SPEC_REGISTRY` iteration); `scripts/audit_checks/check_reconciled_versions.py:24-58` (version-mismatch gate); `scripts/audit.py:964-986` (`doctrine_table` fallback) | **0 found** — `toc-freshness-playbook` (`.pre-commit-config.yaml:64-68`) drives `scripts/toc/generator.py`'s `parse_headers`, which scans for `## ` headings only, and the prologue's first `## ` is line 356 (outside 1–102), so this gate never reads the prologue's prose | frontmatter line 2 has 3 live readers; the review-pass blockquotes (the bulk of the section's 7,836 B) have none found |

**Cross-cutting pattern:** every prologue's *frontmatter* is live-gated (freshness, version
reconciliation, or a byte-cap test); every prologue's *prose body* — the bulk of the bytes
in every case — has zero readers found. ESSENTIALS.md is the partial outlier: superseded
and told not to be booted from, yet still content-parsed by the freshness gate that
governs every other canonical file.

## Step 3 — the docs-cut list (proposal only)

Five items, one per named section, in AX27-5's one-word shape (`to-browser/CLOSURE-VERDICTS-2026-09-13.md`
is the live precedent: *"Ask: ... GO/NO-GO"* + evidence + a bolded one-word
`Recommended:`). **A recommendation here is not a cut.** Per the Done-contract, this
lane's diff touches no governed doc body; the word below is this census's read of its own
evidence, for the operator to accept or reject in a *later* lane. `AX28-2` names this
list's own slot in that numbering — it carries no separate written ruling of its own;
`AX28-1` ("trustworthy suite", `JOURNAL.md:268`) and `AX28-3` (the single-batch-anchor
ask, `JOURNAL.md:275`) are its siblings, and `AX27-5` (`JOURNAL.md:123`) is the prior
one-word-shape instance this list's format is drawn from.

---

**1 — ARCHITECTURE's prologue.** Ask: cut the dated change-history blockquote (roughly
lines 17–276, ~29 KB) down to just the "How to read this doc" reader-routing guide
(lines 260–276, ~1 KB)? **GO/NO-GO.**
Evidence: Step 2 found zero readers on the prose body; the blockquote is a chained
sequence of per-lane dated entries ("Last updated: `2026-09-12` — lane...", "Prior:
`2026-08-29` —...") that is structurally the same *history-accretion* shape `audit.py`'s
own `doc_rot` check already flags as bloat elsewhere in this repo (BACKLOG rows, not yet
extended to canonical-doc prologues) — 3+ dated entries chained is already this repo's own
bloat signature. The reader-routing guide is the one part of the prologue any session
persona is actually pointed at (CLAUDE.md §3's "Where to jump" line routes into chapters,
never into the history).
**Recommended: GO.**

**2 — ARCHITECTURE's table of contents.** Ask: cut it? **N/A — nothing exists to cut.**
Evidence: deleted 2026-07-11 (`f7a548d2`), hub leg `[#326]`, deliberately and already
closed for this file. No action is available here; this item exists in the list only
because the Done-contract named it.

**3 — CLAUDE.md's prologue.** Ask: trim it? **GO/NO-GO.**
Evidence: already the smallest of the five (964 B, 4.0% of the file); Step 2 found 2 live
readers touching its actual content (the freshness gate's frontmatter read, and
`tests/test_claude_md_byte_cap.py`'s live regex match on the declared cap); it states the
file's own governing budget and the boot-contract framing every other section depends on.
**Recommended: NO-GO.**

**4 — protocols/ESSENTIALS.md.** Ask: retire it now? **GO/NO-GO.**
Evidence: already marked `status: superseded` pending `[#628]`; Step 2 found the
freshness gate still content-parses and re-dates it despite `CLAUDE.md` §4 telling every
session not to boot from it — superseded but not inert. This finding does not open a new
decision; `[#628]` already owns the retirement. It is evidence that `[#628]`'s dissolution
is not yet complete (the registry memberships in `canonical_docs.py` — `CANONICAL_OPTIONAL`,
`FRESHNESS_FILES`, `SECTION_HISTORY_DOCS`, `STRUCTURE_DOCS` — still treat it as live),
not a reason to invent a second track.
**Recommended: GO — on the already-open `[#628]`, not as a new ask.**

**5 — PLAYBOOK's prologue.** Ask: cut the review-pass blockquotes (lines ~7–95) down to
the frontmatter, title, and the "Organization" paragraph? **GO/NO-GO.**
Evidence: Step 2 found zero readers on this prose (the `reconciled_with` frontmatter key
that DOES have 3 live readers sits above the blockquotes and is untouched by cutting them);
the blockquotes are the same chained dated-entry shape as item 1, and PLAYBOOK's own
frontmatter-adjacent text already states the governing principle that argues for the cut:
*"Section history lives in git (commit log + JOURNAL `Changes:` line), not in per-section
changelog blocks — per ADR-49."* ADR-49 is cited inside the very passage this item proposes
cutting.
**Recommended: GO.**

---

**Net:** 3 GO, 1 NO-GO, 1 N/A. No item is executed by this lane — Done-contract item 3
binds: nothing is cut here.

## Step 4 — confirmation: nothing cut

`git diff --stat 95e162c8..HEAD -- ARCHITECTURE.md CLAUDE.md protocols/PLAYBOOK.md
protocols/ESSENTIALS.md` returns empty across all three of this lane's commits — the four
governed files this census measured are byte-identical to the branch's base. The lane's
entire diff is one new file: this one. The Step 3 GO/NO-GO recommendations above are
findings for a later lane to act on, not actions this lane took.

The external copy at `to-browser/DOCS-CUT-LIST-2026-09-13.md` (this file's Step 3 section,
`<!-- COPY OF ... -->` header per `protocols/OPERATOR-INTERFACE.md` §1) is this lane's last
act before STOP.

**Known unrelated pre-existing failure, not in this lane's footprint:**
`tests/test_manifest_link_route.py::test_the_class_enum_is_the_hermetization_module_s_own_object`
fails on an `is`-identity assertion between two separately-imported copies of
`AUDIT_CLASS_ENUM` (`bm.AUDIT_CLASS_ENUM is vh.AUDIT_CLASS_ENUM`) — an xdist/module-import
duplication artifact reproducible with zero files staged, unrelated to any change in this
lane's diff (a single new markdown file cannot affect Python module identity). Not fixed
here: out of this lane's declared footprint (docs/audits/ + the external copy only).
