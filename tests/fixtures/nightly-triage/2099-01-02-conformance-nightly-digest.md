<!-- scope: meta -->
# Nightly Conformance Digest — 2099-01-02 (SYNTHETIC TEST FIXTURE)

**Date:** 2099-01-02
**Branch:** `claude/conformance-2099-01-02`
**Author:** Claude Code (synthetic), operator Rob
**Nature:** **SYNTHETIC TEST FIXTURE — not a real audit record.** Exercises the
nightly-conformance-triage Action's survivor path (1 survivor → triage issue).
Modeled on the REAL generator shape (`docs/audits/2026-06-05-conformance-nightly-digest.md`):
free-rendered prose counts, NO hand-made `### Counts` table. The only
machine-readable count contract is the marker line below — written by code
(`conformance-hub.js`) and read by code (the Action parser). See
`tests/test_nightly_triage_parser.py`.

<!-- counts: raw=1 survived=1 killed=0 -->

---

## Run

**Path:** SPEC-ORCHESTRATION fallback (synthetic — no real subagents ran).

---

## Summary

Synthetic findings-night. The skeptic killed 0 of 1 raw finding (kill-rate 0%),
leaving 1 genuine med survivor to exercise the triage-issue path. The counts
above are carried by the machine-readable marker, not by this prose.

---

## Findings (PROPOSALS ONLY)

**Raw:** 1 · **Survived skeptic:** 1 · **Killed false positives:** 0

### High (0)

*(none)*

### Med (1)

**SYNTHETIC-F1** — `living-docs` — placeholder finding to exercise the
triage-issue path

- **Location:** `docs/audits/example.md:1`
- **Evidence command:** `grep -n 'example' docs/audits/example.md`
- **Verdict:** contradicted
- **Proposed fix (proposal only):** SYNTHETIC — operator would resolve here.
- **Skeptic note:** SYNTHETIC survivor; kept to drive the survivor path.

### Low (0)

*(none)*

---

## Killed Findings

*(none — synthetic 0-killed run)*

---

## Checked-and-Clean

This Checked-Clean block MUST NOT appear in the triage issue body (extractor
exclusion test).

---

## Next Actions (proposals for operator)

1. SYNTHETIC — operator would resolve SYNTHETIC-F1 here.

---

## Safety Tripwire

`git status --porcelain` at review completion (synthetic): clean. Only this
digest file would be written during a real review.
