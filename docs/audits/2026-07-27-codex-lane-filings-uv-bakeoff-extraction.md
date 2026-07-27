# Codex Review — lane-filings-uv-bakeoff-extraction

**Date:** 2026-07-27
**Branch:** `docs/lane-filings-uv-bakeoff-extraction`
**HEAD:** `98077673`
**Diff range:** `main..docs/lane-filings-uv-bakeoff-extraction`
**Codex version:** codex-cli 0.145.0
**Mode:** doc-review

---

## Focus

(none specified)

---

## Findings
## Critical

(none)

## High

### docs/decisions/README.md:100 — Binding non-ADR decisions conflict with the canonical decision-record model

**What:** The new section declares non-ADR notes “binding,” while the file and PLAYBOOK state that decisions live in ADRs.  
**Why:** It creates an ungoverned decision-record type with no defined template, lifecycle, or authority reconciliation.  
**Fix direction:** Either record these rulings as ADRs, or first codify the non-ADR record class and its rules in the canonical decision-record guidance.

## Medium

### docs/decisions/README.md:109 — The promised uv ADR has no owning work item

**What:** The note says the reasoned ADR is the uv arc’s deliverable, but the only uv ticket, [#432], explicitly excludes that ADR from its scope and no other uv ADR task exists.  
**Why:** The fleet-wide adoption is binding while its required decision record can be silently omitted.  
**Fix direction:** File and reference a dedicated ADR leg, or make an accepted ADR an explicit [#432] completion condition.

### docs/decisions/README.md:116 — rtk rejection lacks evidence provenance

**What:** The decision records specific benchmark and billing figures but provides no source, date, benchmark artifact, or reproducible measurement reference.  
**Why:** Future readers cannot verify the factual basis for a permanent rejection or distinguish it from an unsupported external claim.  
**Fix direction:** Cite the benchmark/source and preserve the relevant measurement context, or narrow the note to the operator ruling without presenting unsupported metrics as evidence.

### BACKLOG.md:240 — Bake-off has no pre-registered evaluation criteria

**What:** [#433] requires three pilots and “evidence,” but does not define the common measures or pass/fail criteria that decide among them.  
**Why:** The ADR can still select a candidate by preference, defeating the stated “pilot evidence, not chat” disposition.  
**Fix direction:** Add a shared evaluation rubric and required evidence for every candidate before the pilots begin.

## Low

### BACKLOG.md:254 — “Read-only arc” contradicts its required outputs

**What:** [#434] calls itself read-only but requires committing an aggregate and recording a ruling.  
**Why:** The scope label is misleading for an executor deciding what mutations are authorized.  
**Fix direction:** Describe it as read-only source analysis with explicitly authorized record/ruling writes.
