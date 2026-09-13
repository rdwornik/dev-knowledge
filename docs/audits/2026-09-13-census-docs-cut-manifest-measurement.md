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

*(added in the next commit)*
