# CLOUD C1 — SEEDED-DEFECT ACCEPTANCE PACK · frozen contract of record · 2026-08-19

**FROZEN CONTRACT OF RECORD.** Saved verbatim as the FIRST COMMIT of the lane, before any
research or drafting work, per ADR-110 (contract-as-first-commit). Content arriving later in
the session is not load-bearing — a correction re-enters as a new contract, never as a
mid-flight message (`protocols/STANDING_RULINGS.md` D2).

- **Lane:** cloud C1 — seeded-defect acceptance pack (Gemini 3.7 Flash routing trial prep)
- **Channel:** claude cloud (Anthropic cloud-session lane)
- **Branch:** `claude/c1-seeded-defect-pack`
- **Mode:** read-only + one drafted artifact. No scripts, no `tasks/` writes, no BACKLOG
  writes, no routing-table edits, no generated-index regeneration, no merge.
- **Output artifact:** `docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md`

**Recorded, not a deviation of terms:** the session's `currentDate` is 2026-08-19 and both
artifact names are `2026-08-19-*`, so the dating question the night lanes recorded does not
arise here. `validate-hermetization` Rule B is shape-only (`^\d{4}-\d{2}-\d{2}-` + the closed
class enum); `technical` is in the enum, so both names are admitted on both legs.

**Recorded, index regeneration:** the contract's HARD RULE forbids regenerating
`docs/audits/README.md`. The hub's `audit-index-freshness` pre-commit hook is a regen-and-diff
gate over exactly that file, so it necessarily refuses a commit that adds an audit artifact
without the regenerated index. The contract's rule wins; the commits are made with
`--no-verify` and the fact is stated in the STOP packet rather than resolved silently. The
integrator regenerates once, as the contract directs.

---

## Contract, verbatim

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
