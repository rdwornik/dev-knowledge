# Codex Review — canon-inoculation

**Date:** 2026-07-19
**Branch:** `docs/canon-inoculation`
**HEAD:** `ee5b1302`
**Diff range:** `main..docs/canon-inoculation`
**Codex version:** codex-cli 0.144.5
**Mode:** doc-review

---

## Focus

- Fidelity: does each transcription faithfully match its ratified source (ADR-36/41 RULING-W; ADR-101 two-tier new-path amendment; [#353] worktree side-effect; the consumer-leg merge-delegation composite)? Flag any paraphrase that drifts from the ADR wording.
- Placement: is PLAYBOOK the operational home (what to do, when, by whom) and ESSENTIALS a one-liner invariant that POINTS rather than duplicating PLAYBOOK text?
- Cross-doc consistency: stale claims, dangling refs, collision with Ch10 "two-tier automation doctrine" (unrelated axis, same adjective).
- Honest-limits: are the prose-only/not-yet-gated statements accurate (#353 has no boot organ; ADR-101 rule in force but #345 gate unbuilt)?

---

## Findings
## Critical

(none)

## High

(none)

## Medium

### protocols/ESSENTIALS.md:83 — RULING-W loses its “SHOULD” requirement

**What:** The summary says the hub “MAY write” into a consumer, while ADR-36/41 say it “MAY and SHOULD” do so for methodology/cleanup work.  
**Why:** This weakens the ratified disposition from encouraged sanctioned work to mere permission and conflicts with PLAYBOOK’s fuller wording.  
**Fix direction:** Preserve “MAY and SHOULD” in the one-line invariant.

### protocols/PLAYBOOK.md:1249 — Consumer-leg composite broadens the required pre-merge review

**What:** “gates + review pre-merge” paraphrases the recorded composite, which specifically requires Terra pre-merge before commit-and-STOP.  
**Why:** A generic review is not an unambiguous operational instruction and allows a weaker workflow than the source sequence.  
**Fix direction:** Name the Terra/Codex pre-merge review explicitly, or point to its canonical review procedure.

### protocols/PLAYBOOK.md:1250-1251 — “Cross-repo twin” is ambiguous against the preceding integration rule

**What:** This says the operator merges consumer branches, then calls it the “cross-repo twin” of the preceding rule, which says CC-primary executes merges and the operator is not the executor.  
**Why:** Readers cannot tell whether consumer integration is an intentional exception or should follow the CC-primary model.  
**Fix direction:** State explicitly that consumer-leg integration is a separate delegation shape and identify who executes it after operator GO.

## Low

(none)
