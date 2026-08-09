---
intake-id: 32
status: DRAFT
origin: "commissioned research memo (workflow wf-1dc18e42, \"Compute Placement & Remote Execution for a Solo-Operator LLM-Agent Fleet\"), read 2026-08-09; filed by the ARC-2 consolidation under architect amendment 3"
note: "ID CHOICE: 30 and 31 are RESERVED, not free — the operator holds two authored-but-unfiled drafts (INTAKE-30 verification-organ-and-repeatable-execution, INTAKE-31 code-style-doctrine) that the RESEARCH-INGEST contract assigns those ids. Taking 30 here would have collided with a permanent join key. Filed at 32 and the gap is reported, not silently closed. EXTERNAL EVIDENCE: the memo is advisory until ratified; nothing here is doctrine by virtue of being filed, and zero backlog rows are born by this document."
---
# INTAKE — compute placement and remote execution: fix local first, and make the cloud precondition a rule

*(technical mode. Sole owning intake for the compute-placement commission — the sixth research
commission, and the one that is **not** part of the other five. Commissions 1–5 decompose a single
question, "which rules survive without a human remembering them"; this one is an independent
capacity problem and must not be presented as part of that programme.)*

## WHY this is filed separately, and filed at all

The other five commissions were folded into existing intakes (#25 W-9a, #29 ×2) precisely because
they share a question. This one does not. It was still filed rather than dropped because the
operator feels the capacity problem directly, and because **its own research argues against the
thing it was commissioned to evaluate** — which is exactly the kind of finding that gets lost if it
lives only in a memo.

## WHAT the memo actually concludes — the headline is a refusal

**"Fix the laptop first — most of this is a local defect, not a capacity limit."** The memo declines
its own premise on this fleet's own instrumentation, and every number it cites is one this repo
measured, not one it supplied:

- the suite is **wait-bound at ~14.6% CPU** (N3-11), so more cores buy little;
- **~24% of the worktree slowdown is a fixable `rglob` path-walking defect** (N3-03/N3-26), not load;
- `pytest-xdist` already took the suite **1785.6s → ~539s** (STANDING_RULINGS E1);
- the remaining levers are **filesystem placement, antivirus scanning and editor indexing** —
  Defender dev-folder exclusions, WSL2 native filesystem (`/mnt/c` crosses the 9P boundary and is
  "10x or worse" for directory-walking), Pylance `exclude`/`openFilesOnly`, git `fsmonitor`.

**All of it is $0.** The memo's own words: *"Buying compute now would paper over a bug."*

## The one thing here that IS a rule, and is ruled

**Toolchain parity plus fail-closed attestation.** Any remote executor must reproduce the exact
`uv`/hook toolchain from the lockfiles and **fail closed if a gate did not run** — a run that cannot
prove its gates executed is treated as **untrusted, not as green**.

This is not aspirational. It is the direct generalization of a **four-times-witnessed** class: on
2026-08-09 all five night lanes ran with **no executable gate mesh at all** (`uv` 0.8.17 against the
ADR-106 `==0.11.19` pin, so every `uv run --locked` hook entry refused; `.git/hooks/` held only
samples), which is why those five reports had to be re-verified locally after the fact. `[#453]`
owns the container gaps; **the attestation rule is the part `[#453]` does not carry**, and it is
what this intake exists to get ratified.

## Non-goals, stated so a successor does not re-open them

- **No host is provisioned by this intake.** Hetzner-vs-Hostinger is priced in the memo and
  deliberately not decided here; Stage 0 (the free local fixes) precedes any spend.
- **What must never move remote**, per the memo and unchallenged: the interactive architect seat,
  the serial merge gate, and any secret that would land in a cloud-synced profile.
- **This is not a bake-off input.** Model comparison is intake #29's territory and is gated on the
  seeded-defect corpus.

## Open questions for the receiving architect

1. Does the attestation rule ratify **standalone** (it binds the existing cloud lanes today), or
   does it wait on a host decision it does not depend on?
2. Stage 0 is a list of **operator-machine** changes (Defender, WSL2, Pylance). Is any of it in
   scope for a repo-governed methodology at all, or is it operator-owned and merely recorded here?
3. The worktree model is called "defensible but over-provisioned" (ten full checkouts multiply
   indexing and scan load). Does that reopen the lane-count ceiling, or is it Stage 0 noise?

## Provenance

Commissioned memo, workflow id `wf-1dc18e42-7dc0-5290-acb9-1c22b6589fc4`, titled *"Compute Placement
& Remote Execution for a Solo-Operator LLM-Agent Fleet"*. **The memo file itself is deliberately NOT
landed in this repo** — no governance clause defines a home for external research artefacts, and
ADR-101 seals the tree against inventing one. It is cited by title and workflow id per the ARC-2
contract's instruction. Its GitHub-sourced maintenance claims are self-flagged UNVERIFIED (API 403
through the proxy); the PyPI versions and dates were verified by the producing lane.
