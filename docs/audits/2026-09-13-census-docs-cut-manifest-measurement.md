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
