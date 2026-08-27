# Codex Review — w2b-surfaces-r2

**Date:** 2026-08-26
**Branch:** `worktree-w2b-surfaces`
**HEAD:** `91a410f4`
**Diff range:** `be084c91..HEAD`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 1/4/0/0 <!-- Critical/High/Medium/Low. Counted from the Findings section below; the wrapper console printed 0/0/0/0 against these five, which is the known heuristic lie. Dispositions: docs/audits/2026-08-26-technical-w2b-surfaces.md section 3, round 2 — all five fixed. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

This diff is the FIX PASS for a prior review (docs/audits/2026-08-26-codex-w2b-surfaces.md, 1 Critical + 4 High). Review the fixes themselves; assume the prior findings' descriptions are accurate.
- gen_task_tree._looks_like_view: two legs (byte-equality with render_view, then is_projected_row over every row). Is there still a shape that gets a projection imported by --write --force, or a full-body backlog falsely refused?
- gen_task_tree.task_row_lines / _VIEW_ROW_RE / view_problems: fence handling vs parse_backlog, and whether the end-anchored grammar can be satisfied by a row that still carries body.
- generated_artifact_freshness: the new content_check field, _exact_verdict, and where it is placed inside measure() relative to deleted/uncommitted/absent classification. Any state where the exact answer masks or is masked by the wrong classification?
- gen_audit_index.collect_audits/render_index gained an explicit oot param. Any call site left passing the wrong root, or behaviour change for the live default?
- gen_dashboard._gain_from_task_file: revision choice (parent vs sha), pointer parsing, and failure modes.
- backlog_source.canonical_text: strict decode + CRLF normalization.
- session_end_backpressure._added_lines variadic change.

---

## Findings
## [CRITICAL] scripts/gen_task_tree.py:665 — Projection detection is defeated by the view-size limit

**What:** `is_projected_row()` requires the 400-byte budget, so a foreign/legacy `render_view()` projection with a long title fails the structural leg.  
**Why:** After exact comparison against a different populated tree fails, `--write --force` can import that projection and overwrite task bodies.  
**Fix direction:** Keep size validation separate from projection detection; use an unambiguous generated-view marker/provenance for the destructive-import guard.

## [HIGH] scripts/gen_task_tree.py:753 — Valid full-body rows can be permanently refused as views

**What:** Any full-body task row under 400 bytes that ends in ` · tasks/<file>.md` matches the fallback projection grammar.  
**Why:** `--write` refuses a legitimate bootstrap/recovery input, including with `--force`, despite it containing authoritative body content.  
**Fix direction:** Do not infer source type solely from overlapping row syntax; add explicit view identity or route ambiguous input through a safe recovery path.

## [HIGH] scripts/generated_artifact_freshness.py:346 — Verifier errors can become a clean freshness verdict

**What:** A raising configured `content_check` is swallowed and falls back to the date relation.  
**Why:** For same-day input/output commits, that relation returns `fresh`, so an index whose exact verification failed can be reported clean—the green-by-skip state this check is meant to prevent.  
**Fix direction:** Distinguish “no content checker” from “configured checker failed”; classify the latter as unverifiable/WARN.

## [HIGH] scripts/gen_dashboard.py:417 — A title can suppress retrieval of the real Done-when clause

**What:** The code trusts `row.gain` before checking whether the row is a projection. A title containing ` · Done when: …` produces a nonempty parsed gain.  
**Why:** `project_row()` preserves title text, so release notes can publish title text as the gain instead of reading the task body at the closing revision.  
**Fix direction:** Detect a terminal task-file pointer first and always derive projected-row gains from that historical task file.

## [HIGH] scripts/backlog_source.py:108 — Line-ending normalization regresses bare-CR backlog files

**What:** The replacement normalizes `\r\n` only, while the prior `Path.read_text()` universal-newline behavior also normalized lone `\r`.  
**Why:** A strictly decodable consumer backlog using bare-CR line endings now reaches `parse_backlog` with `\r` and fails instead of being processed as before.  
**Fix direction:** After strict UTF-8 decoding, normalize both CRLF and remaining lone CR line endings.

## [MEDIUM]

(none)

## [LOW]

(none)