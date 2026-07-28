# Codex Review — 437-closure-design

**Date:** 2026-07-28
**Branch:** `fix/437-closure-token-shared-core`
**HEAD:** `3b2142be`
**Diff range:** `main..fix/437-closure-token-shared-core`
**Codex version:** codex-cli 0.145.0
**Mode:** doc-review

---

## Focus

DESIGN REVIEW (pre-build, gate-class posture per [#438]) of docs/audits/2026-07-28-technical-437-closure-token-design.md.
This is GATE CODE design: the scanners feed PROPOSALS / git_backlog_drift / ship-gate. Review the DESIGN, not prose style.
Answer specifically:
- Semantics: are the four strip contexts (fenced, inline-code, block-quote line, same-line double-quote) right? Any context that would hide a REAL closure directive (fail-open) or leave a false-positive class alive? Is the deliberate non-strip list (single quotes, indented lines) sound?
- Single-home claim: is scripts/propose_closures.py the right shared home given validate_git_backlog already imports from it and the plugin ships standalone (ADR-78 carrier doctrine)? Is the byte-parity twin test the right divergence guard, or is there a stronger sanctioned mechanism?
- OUTSIDE THE ENGINE (pass-11 lesson): name anything ELSE that consumes closure-token semantics that the blast-radius table (section 5) missed - hooks, commands, audit legs, deploy/fleet surfaces, docs. Is check_backlog_commit_msg._REF_RE correctly out of scope?
- Test plan: any missing failure mode (regex edge, unpaired backticks, multi-line quoting, CRLF, unicode) in section 6? Is the empirical full-history sweep beat sound?
- Fail direction: confirm every proposed change fails CLOSED for the gate purpose (under-surfacing is the stated safe error) and name any spot where the design could fail OPEN silently.
Verdict: CLEAR or findings with severity.

---

## Findings
Verdict: **findings — not CLEAR.**

## Critical

(none)

## High

### docs/audits/2026-07-28-technical-437-closure-token-design.md:89 — Fleet plugin-release path is missing

**What:** The blast radius plans the plugin twin edit but omits the required plugin version bump and per-consumer cache-update workflow.  
**Why:** Installed consumers execute a version-keyed cached plugin copy; without the release/update steps, they silently retain the false-positive scanner. ADR-78’s floor mechanism is also not the plugin’s delivery mechanism.  
**Fix direction:** Add `plugin.json` versioning plus marketplace update, project-scope plugin update, and restart/verification to the blast radius and test/rollout plan.

### docs/audits/2026-07-28-technical-437-closure-token-design.md:157 — Full-history verification loses match provenance

**What:** Comparing raw and stripped results as ID sets cannot prove that every genuine closure occurrence survived.  
**Why:** A real and a quoted `closes [#N]` in different commits collapse to the same ID; stripping the real one could pass the proposed sweep unnoticed.  
**Fix direction:** Compare `(SHA, id[, match offset])` occurrences and require an explicit reviewed allowlist for every removed occurrence.

## Medium

### docs/audits/2026-07-28-technical-437-closure-token-design.md:48 — Multi-line quotation false positives remain unspecified

**What:** Double-quoted text is stripped only when both quotes occur on one line, leaving paired multi-line quoted examples detectable as closures.  
**Why:** This contradicts the precision objective and creates a known fail-open false-positive class; the test plan also omits CRLF, paired/unpaired fences and quotes, and an explicit Unicode-quote policy.  
**Fix direction:** Either support paired multi-line straight quotes or declare them out of scope; add fixtures for those delimiter/line-ending cases and assert the chosen behavior.

### docs/audits/2026-07-28-technical-437-closure-token-design.md:95 — Proposed byte-parity mechanism is not implementable as written

**What:** `inspect.getsource` cannot compare compiled `CLOSES_RE` objects, despite the design naming that symbol as byte-identical.  
**Why:** The parity test would either fail mechanically or silently reduce its declared coverage; regex flags also need parity coverage.  
**Fix direction:** Follow the established split: compare regex pattern and flags explicitly, and use source comparison only for functions (or compare AST/source segments for declarations).

## Low

(none)

`README.md`’s generated count, ordering, and new link are structurally consistent.

The shared home in `scripts/propose_closures.py` is appropriate, and a hub↔plugin parity test is the sanctioned practical guard for a standalone plugin. `check_backlog_commit_msg._REF_RE` is correctly out of scope: it verifies removed-task ID references, not closure-token semantics. Single quotes and indented commit-body lines are also sound non-strip choices.
