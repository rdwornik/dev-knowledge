<!-- scope: meta -->
# Nightly Conformance Digest — 2099-02-01 (SYNTHETIC TEST)

**Date:** 2099-02-01
**Branch:** `claude/conformance-2099-02-01`
**Nature:** **SYNTHETIC TEST — not a real audit record.** Action-path validation
(findings night, 1 survivor) per the 06-04 precedent. Safe to revert. Modeled on
the REAL generator shape (`docs/audits/2026-06-05-conformance-nightly-digest.md`):
level-2 headings, free-rendered prose counts, NO `### Counts` table. The only
machine-readable count contract is the marker line below.

<!-- counts: raw=2 survived=1 killed=1 -->

---

## Run

**Path:** SYNTHETIC (no real subagents ran).

---

## Summary

Synthetic findings-night. The skeptic killed 1 of 2 raw findings (kill-rate 50%),
leaving 1 genuine med survivor to exercise the survivor → triage-issue path. The
counts are carried by the machine-readable marker, not by this prose.

---

## Findings (PROPOSALS ONLY)

**Raw:** 2 · **Survived skeptic:** 1 · **Killed false positives:** 1

### High (0)

*(none)*

### Med (1)

**SYNTHETIC-F1** — `living-docs` — placeholder survivor finding to exercise the
triage-issue body

- **Location:** `docs/audits/example.md:1`
- **Evidence command:** `grep -n 'example' docs/audits/example.md`
- **Verdict:** contradicted
- **Proposed fix (proposal only):** SYNTHETIC — operator would resolve here.
- **Skeptic note:** SYNTHETIC survivor; kept to drive the survivor path. This
  Findings section SHOULD appear in the triage issue body.

### Low (0)

*(none)*

---

## Killed Findings

| Claim | Kill reason | Detail |
|---|---|---|
| SYNTHETIC-K1 — placeholder killed finding | true-but-irrelevant | SYNTHETIC — this Killed Findings section MUST NOT appear in the triage issue body (extractor exclusion test). |

---

## Checked-and-Clean

This Checked-Clean block MUST NOT appear in the triage issue body (extractor
exclusion test).

---

## Next Actions (proposals for operator)

1. SYNTHETIC — operator would resolve SYNTHETIC-F1 here. This Next-Actions text
   SHOULD appear in the triage issue body.

---

## Safety Tripwire

`git status --porcelain` at review completion (synthetic): clean. Only this
digest file would be written during a real review.
