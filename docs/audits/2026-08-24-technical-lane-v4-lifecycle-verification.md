# LANE V4 — register verification, domain V4 (lifecycle: ADR / intake / audit / registry)

- **Class:** technical (ADR-101 R3 enum) · **Date:** 2026-08-24 · **Slug:** `lane-v4-lifecycle-verification`
- **Inputs:** `docs/audits/2026-08-24-technical-research-candidate-register.md` (rows) +
  `docs/audits/2026-08-24-technical-research-register-addendum.md` (**governs on conflict**)
- **Rows owned:** every register row with `domain: V4` — C24, C25, C26, C27, C28, C29 (six)
- **Substrate:** `cloud-session`, read-only lane. Clone of `origin/main` at `e4e5b6b`.
- **This lane RULES NOTHING.** Every verdict below is evidence for the architect's batch ruling.
- **Writes made:** this file, and the regenerated `docs/audits/README.md` index (hook-forced).
  No writes to `tasks/`, `BACKLOG.md`, `protocols/`, `docs/decisions/`. No merge, no JOURNAL entry.

## Environment declaration

`uv --version` on the container returned **0.8.17**; `pyproject.toml:25` pins
`required-version = "==0.11.19"`. Mismatch, so the pinned uv was installed per the brief
(`python3 -m pip install --target ./uvpin "uv==0.11.19"` → `uv 0.11.19`) and **every command in
this artifact ran under `./uvpin/bin/uv run --locked …`**. The `uvpin/` directory is untracked
scratch and is removed at lane close (CLAUDE.md §5 rule 9, no leftovers).

Registry read once, under that env: `uv run --locked python scripts/audit.py checks` →
**46 registered checks** in `ALL_CHECKS`. Every "no such check exists" claim below is measured
against that list, not remembered.

## The addendum's V4-named duty, discharged first

> *"M4 closed CLEAN on 2026-08-24 … The V4 lane's first act on these two rows is to locate that
> ruling."* — addendum, C26/C27

**Located.** The ruling is **R3**, at
`docs/audits/2026-08-23-technical-phase0-preconditions.md:1170-1178` (landed there verbatim by
LANE-L6, commit `4b19c375`, recorded at
`docs/audits/2026-08-24-verification-l6-rulings-landing.md:16`), and its window-close record is
`docs/audits/2026-08-24-technical-batch-close.md:62-68`. Neither C26 nor C27 is new work: both
are already decided, and the residual is R3's own item (i), which the batch close flags as
**not verified as landed**.

## Verdicts

| row | verdict | locator | note (one line) |
|---|---|---|---|
| **C24** | **PARTIAL** | `protocols/STANDING_RULINGS.md:1982-1996` (the `landed:` predicate shape) · `scripts/audit.py:3407` (`check_landing_predicate`) · `ecosystem/doc-code-edge.yaml:28-31` | Stable ids (A1…R-n) and a machine-read per-ruling block exist, but only the **`landed:` site predicate** is machine-readable — missing: a status lifecycle, supersession pointers, `scope`, and the **required `enforced_by`** (that field exists only in `deploy/manifest-v1.4.0.yaml:145`, for a manifest component, never for a ruling). |
| **C25** | **ABSENT** | checked: `scripts/audit.py` `ALL_CHECKS` (46 checks, none keyed on governed-path→record) · `.pre-commit-config.yaml` (commit-msg gates are `backlog-id-on-close` / `backlog-filing-backpressure`, both backlog-keyed) · `ecosystem/doc-code-edge.yaml:28-31` (4 declaration docs, no gate on edits to them) | Nearest live organ is `check_review_artifact_coverage` (`scripts/audit.py:3252`), which is **advisory, code-impact-keyed, and asks for a review artifact — not a ruling record**; `boundary_headers.py:66` `_GOVERNED_GLOBS` is a marker-region gate, not a record requirement. |
| **C26** | **PARTIAL** | criterion: `docs/intake/README.md:213-219` · ruling: `docs/audits/2026-08-23-technical-phase0-preconditions.md:1170-1178` | The archivability criterion **already exists** (terminal = CONSUMED/SUPERSEDED/REJECTED relocate byte-identical; ACCEPTED deliberately excluded) and R3 retired the premise — *"Both directions clean, so there is no new rule to author"*; **missing is R3's M4 (i)**: §5 is not recorded as ratified in place, and its two invariants are **not armed** (no such member in the 46 checks; `check_intake_tree_coherence`'s four legs are regen/round-trip only — `scripts/gen_intake_tree.py:369-387`). |
| **C27** | **HAVE** | `docs/audits/2026-08-23-technical-phase0-preconditions.md:1177` — *"**M4 (ii): ADR-100 reaffirmed index-only**, with the reason recorded"* | Decided this window; `docs/audits/2026-08-24-technical-batch-close.md:62-64` records it as **CLOSED BY RULING**. Per the addendum this is **not adopted as new work** — doing so would re-decide a decided thing. ADR-100 §1/§3 (`docs/decisions/ADR-100-audit-retention-index-rule.md:25-37`) stands un-amended, which is what "reaffirmed" means here. |
| **C28** | **PARTIAL** | validator: `scripts/audit_checks/check_adr_status_grammar.py:28`, registered `scripts/audit.py:3561` (check #45 of 46) · sweep: `docs/audits/2026-08-23-technical-lane-status-grammar.md:497-560` | Exactly the addendum's expected split — **validator HAVE, sweep proposed-unexecuted**: Class A is 47 grammar normalizations, Classes B/C/D are **PROPOSED, BLOCKED** under ADR-94 (`Proposed` is empty corpus-wide, so the ratification trigger is unmeetable), Class E deliberately not re-proposed. Carriers `[#242]` (`BACKLOG.md:43`) and `[#362]` (`BACKLOG.md:437`) both **open**. |
| **C29** | **PARTIAL** | `protocols/PLAYBOOK.md:2777` (propose-only; a lane *"does not issue a ruling"*) · `protocols/STANDING_RULINGS.md:531-537` (F5 ruling-locator rule) · `docs/intake/README.md:272-276` (transcript → CC converts → **operator approves**) | The two *prohibitive* halves are live doctrine — never the system of record, human confirmation mandatory — and F5 additionally requires a same-batch register line for every ruling; **missing is the permissive half**: no rule authorises or shapes LLM ruling-**proposal from a transcript with verbatim quotes**. The practice exists un-ruled (`docs/audits/2026-08-24-verification-l6-rulings-landing.md:24-30`, verbatim extraction proven by a zero-output diff). |

## `evidence: measured-here` rows — measurement artifact locators

Three of the six rows carry the tag. All three artifacts are findable, so **no row downgrades to
`practitioner`**; two carry numbers the artifact does not support, recorded as evidence, not ruled.

| row | measurement artifact | agrees with the row's evidence line? |
|---|---|---|
| **C26** | `docs/audits/2026-08-23-technical-phase0-preconditions.md:563-590` (Premise D: frontmatter-parsed census — LIVE 36, ARCHIVE 7; METRIC A = 0, METRIC B = 0, METRIC C = 7) | **No.** The row's evidence reads *"the archival leg ran and returned EMPTY against 34 intakes for want of a criterion"*. The artifact measures **43 docs (36 live + 7 archived)**, records the archival rule being executed **7-for-7 by hand with zero violations in either direction**, and calls the underlying *"0 intakes archived"* claim **factually false**. The tag stands (a real measurement exists); the number in the row does not. |
| **C27** | `docs/audits/2026-08-21-technical-lane-arch-lifecycle-archival.md:190-197` (§3.3 PROPOSED-PATH, both rows **BLOCKED** by ADR-100 §1) | **Yes.** *"lane C stopped correctly; PROPOSED-PATH recorded BLOCKED"* is exact — the artifact's headline (`:12-18`) records the audits leg stopped, 0 moved, on governance rather than hesitation. |
| **C28** | `docs/audits/2026-08-23-technical-lane-status-grammar.md:36-75` (grammar census) and `:642-676` (archival-eligibility) | **Partly.** *"4 incompatible grammars"* holds — G1 40 / G2 34 / G3 12 / G4 1 live, G5 zero live. *"4 superseded-unmarked"* and *"4 archival-eligible blocked"* do **not**: the artifact measures **3** header↔index divergences (Class B: ADR-45, ADR-46, ADR-47) and **ZERO** archival-eligible ADRs across twelve candidates. |

## Cross-cutting observations (evidence for the ruling seat, not verdicts)

1. **Three of the six rows read `carrier: NONE`; two of those have a live carrier the register
   did not see.** `[#552]` (`BACKLOG.md:68`, open) specifies the window-close disposition +
   archival routine, including an `archival_residency` check scoped to `docs/intake/**` +
   `docs/decisions/**` with `docs/audits/**` **excluded by ADR-100** — that is C26's residual and
   C27's consequence already owned. And intake **#43** (`docs/intake/2026-08-24-tech-ruling-register-landing-gap.md`,
   status `READY`) is C25's requirement almost verbatim: *"a ruling made in a window is present in
   the register, or its absence is refused visibly at a boundary the window cannot cross
   silently."* Adopting C25 or C26 as new rows would birth against an existing carrier — ADR-111's
   OWNED outcome, not CANDIDATE.
2. **C24 has a self-imposed cost the row does not price.** `protocols/STANDING_RULINGS.md:1972-1980`
   records that the file sits inside the silent-rule ratchet corpus, so entries are *"phrased
   declaratively"* to avoid raising the baseline. A migration to records carrying a required
   `enforced_by` is a schema change to a file that is deliberately written to be non-normative in
   its own prose. (Incidental, unowned by this lane: that editing note states the live baseline as
   `441 = 441`, while `ecosystem/silent-rule-baseline.yaml:20-23` now reads **443**, detector
   `silent-rule-v5`, `measured_at: 2026-08-24`.)
3. **The register's conflict field for C24 is accurate and satisfiable.** *"migration must preserve
   section Q verbatim"* — section Q exists at `protocols/STANDING_RULINGS.md:1837`.
