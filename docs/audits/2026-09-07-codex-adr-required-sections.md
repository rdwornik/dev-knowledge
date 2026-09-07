# Codex Review — adr-required-sections

**Date:** 2026-09-07
**Branch:** `worktree-lane-u-000-adr-template-flip-condition`
**HEAD:** `96994389`
**Diff range:** `main..worktree-lane-u-000-adr-template-flip-condition`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/5/0/0 <!-- Critical/High/Medium/Low. Counted BY HAND from the Findings section: the script's severity heuristic reported 0/0/0/0 against five HIGH findings, so the suggested tally was wrong and is not what shipped. All five were assessed; four were fixed in code (blockquoted body read as empty; empty ATX heading not a boundary; unbalanced emphasis, resolved deliberately in the lenient direction; adapter read-error masking a real FAIL) and the fifth (unnumbered ADR filename is ungateable) is kept as a named leniency, now stated in the WARN evidence and filed as a CANDIDATE. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- The two REQUIRED-SECTION legs in scripts/validate_adr_status.py: section_state / required_section_defects / REQUIRED_SECTIONS.
- FALSE POSITIVES on a FAIL-armed leg are the worst failure available here. Attack _FLIP_HEADING_RE, _ALTS_HEADING_RE, _ENUMERATOR and _strip_placeholders for inputs where a conforming ADR is reported as missing/empty.
- FALSE NEGATIVES: can a QUOTED heading (fence, HTML comment, blockquote) or a placeholder-only body be laundered into "present"?
- Grandfather split: FLIP_GRANDFATHER_MAX_ADR = 116, adr_number parsing, unnumbered filenames.
- Does the adapter (check_adr_status_grammar.py) agree with the CLI (main) about which defects exist?

---

## Findings
## CRITICAL

(none)

## HIGH

[HIGH] `scripts/validate_adr_status.py:620` — Blockquoted section content is discarded as if it were always quoted material.

**What:** After a real required-section heading, a body consisting of `> Reverse if…` is reported `empty`.
**Why:** A conforming ADR can legitimately state its condition or rationale in a blockquote, causing a false FAIL on a new ADR.
**Fix direction:** Ignore blockquoted headings before a section opens, but retain blockquoted body content once a real section is open.

[HIGH] `scripts/validate_adr_status.py:557` — Empty ATX headings do not end a required section.

**What:** `_ATX_HEADING_RE` requires whitespace after `#`, so valid empty headings such as `##` are not section boundaries.
**Why:** Text belonging to the next section can fill a placeholder-only Flip-condition/Alternatives section and launder it into `present`.
**Fix direction:** Recognize end-of-line as a valid ATX-heading terminator as well as whitespace.

[HIGH] `scripts/validate_adr_status.py:524` — Flip-condition accepts unbalanced emphasis as a valid heading.

**What:** The closing emphasis backreference is optional, so `## **Flip-condition` is accepted.
**Why:** A malformed heading can satisfy the FAIL-armed requirement without containing the required Markdown heading.
**Fix direction:** Require the matching closing wrapper whenever the opening wrapper matched; apply the same correction to Alternatives.

[HIGH] `scripts/validate_adr_status.py:675` — Any future unnumbered `ADR-*.md` file bypasses both FAIL-armed legs.

**What:** An unparseable filename is permanently classified as grandfathered, regardless of when it was added.
**Why:** A new ADR named, for example, `ADR-draft-no-number.md` receives only legacy WARNs and can omit both required sections.
**Fix direction:** Grandfather only a recorded legacy exception set, or make malformed ADR filenames independently blocking before applying the required-section rules.

[HIGH] `scripts/audit_checks/check_adr_status_grammar.py:97` — A second-pass read race suppresses already-computed blocking defects and diverges from the CLI.

**What:** If `required_section_defects()` raises after `corpus_defects()` found an enum/single-field FAIL, the adapter returns only a WARN; the CLI does not take this path.
**Why:** Concurrent file changes can downgrade a real commit-blocking defect and leave the adapter and CLI reporting different defect sets.
**Fix direction:** Preserve and classify previously computed defects when the required-section pass is unusable, adding the read error as supplemental evidence.

## MEDIUM

(none)

## LOW

(none)