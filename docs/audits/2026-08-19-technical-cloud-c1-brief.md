# CLOUD C1 — SEEDED-DEFECT ACCEPTANCE PACK (Gemini 3.7 Flash routing trial prep) · read-only + drafts

Cloud lane. FIRST COMMIT = dispatch-stamp (this prompt as
`docs/audits/2026-08-19-technical-c1-seeded-defects-contract.md` on your claude/* branch).
**HARD RULE (new, 2026-08-19): do NOT regenerate docs/audits/README.md or any generated index —
the integrator regenerates once.** Read-only + one artifact; no scripts/tasks/BACKLOG writes.

CONTEXT: routing-table rule — a new model (candidate: `gemini-3.7-flash`, released 2026-08-13)
enters a lane role ONLY via measured acceptance on seeded defects vs the incumbent fan-out
baseline. Tonight's local evening slot runs the A/B; you build the pack it consumes.

ITEMS (CLEAR/BLOCKED each):
1. **Seeded-defect set (12–16 items)** drawn from REAL, already-fixed defects in this repo's
   history (each: the defective text/code as it was, the question a fan-out lane would be asked,
   the ground-truth answer with the fixing sha). Cover the fan-out role's actual duties:
   retrieval, ranking, verbatim extraction — NEVER classification-against-doctrine (fan-out is
   retrieval-only by standing rule; one seeded item must TEST that the model refuses/flags a
   classification ask rather than answering it).
2. **Scoring rubric**: per item PASS/FAIL definition + the acceptance bar (propose one, e.g.
   ≥ incumbent on correctness with ≤ incumbent fabrication count; fabrication anywhere = heavy
   penalty — the fan-out lane once fabricated a count, that incident is the bar's origin).
3. **Run protocol draft** for the local evening A/B: exact prompts, both CLIs' invocation
   lines left as FILL-INs for the local runner, result-table template.
OUTPUT: `docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md`. Commit, push, STOP packet.
NOT: no model calls yourself, no routing-table edits, no verdicts.
