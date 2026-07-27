---
intake-id: 19
status: SEED
origin: "operator design input, 2026-07-27 — relayed via Layer-1 review chat"
note: "Two-section capture. Section A feeds the morning-loop wave; section B feeds the intake #18 ratification session. Verbatim relay — not a functional-architect conversation."
consumers: "morning-loop wave (section A); intake #18 / [#435] ratification session (section B)"
---

# operator design input 2026-07-27 (night shift + handoff reform), relayed via Layer-1 review chat

## What this is, and what it is NOT

Operator design input captured **verbatim** from the Layer-1 review chat on 2026-07-27 and
relayed here so it exists in the repo rather than in a chat turn (the addressability rule,
LESSONS 2026-07-12). It is a **SEED** — a pre-intake capture dropped by a feed, not yet
worked by a functional-architect conversation (`docs/intake/README.md` §5).

- **Section A (night shift)** is design input for the **morning-loop wave**.
- **Section B (handoff reform)** is design input for the **intake #18 ratification session**
  (`2026-07-27-tech-handoff-process-v6-proposal.md`, stewarded by **[#435]**).

**NEITHER section is citable by prompts or contracts until ratified in the session named
for it.** Nothing here is a ruling, a requirement, or an acceptance criterion yet; a prompt
or contract that cites this document before its ratifying session has cited a capture, not a
decision. The verbatim text below is reproduced without paraphrase or trimming — including
the operator's own labelling of external research as evidence **to be verified by whoever
builds this, not inherited from this message**.

---

## SECTION A — night shift

> Design input for the **morning-loop wave**. Verbatim.

The operator wants an overnight process and asked what to run at night and how. His
named pains, in his order: dependency/code rot · testing and end-to-end · archiving ·
preparing intakes and ADRs so that what ships and how is known in the morning. He
explicitly wants Opus orchestrating Sonnet/Haiku fan-out plus the Gemini lane, and he
wants a METHODOLOGY for night work rather than ad hoc jobs.

Open-web research (Anthropic's published Claude Code engineering guidance) -- offered as
external evidence, to be verified by whoever builds this, not inherited from this message:

- Headless mode is stateless and machine-paced; it is the documented foundation for
  scheduled and overnight work.
- The published batch pattern is a loop of `claude -p` invocations over an enumerated
  task list, with --allowedTools scoping permissions.
- Large jobs are distributed across many parallel invocations rather than one long run.
- Writer/Reviewer with a FRESH context is the documented quality pattern -- a reviewer
  that did not write the code is less biased toward it. (This is our producer!=reviewer
  rule, arrived at independently.)
- Practical scaling boundary reported: subscription auth suits a small number of steady
  agents; a separate API key is the supported path for many parallel or overnight bursts.
- Isolation caution: parallel runs sharing one home directory corrupt each other's
  session state; each run needs its own.

THE FRAME, which matters more than the job list: the night shift is not a new project.
It is the morning-loop wave seen from the night side. Our doctrine already covers most of
it -- model routing by stage size (PLAYBOOK Appendix B), unattended-writer branch isolation
(ADR-84), propose-never-mutate for Tier-3, and ADR-105's rule that a routine may not
activate without a named consumer. What is missing is executable, not doctrinal:

(a) a HOST -- no CI exists, so nightly work today has nowhere to run but the operator's
    own machine or the cloud Routine;
(b) a NIGHT-JOB REGISTRY where each job declares trigger, scope, consumer and
    consumption path -- the ADR-105 shape, which also converts [#426] from a 30-item
    retrofit into one field per job;
(c) a MORNING RATIFICATION SURFACE -- the consumer whose absence is the root of [#419].

HARD RULE to carry into that wave's contract: nothing merges unattended. The night
produces proposals and evidence; the morning is the operator plus ONE report. This is the
existing propose-only doctrine, stated where it will be tested.

Job-to-pain mapping, as candidates only: rot -> nightly edge/rot scan (Gemini propose-only,
gated on R-G) · testing -> full suite plus a CLEAN-ROOM leg, which is exactly
methodology-intake commission E, since a nightly build from declared ranges is what kills
"green only on this machine" · archiving -> the genre-lifecycle sweep · intake/ADR
preparation -> propose-only drafts for morning ratification. Every job names its consumer
before it activates, or it does not activate.

---

## SECTION B — handoff reform

> Design input for the **intake #18 ratification session** ([#435]). Verbatim.

(a) THE CLEAN-HANDOFF CONTRACT. The operator's position: the OLD chat guarantees it hands
over a clean, merged, pushed repo; the NEW chat does zero cleanup and spends all of its
fresh context on planning. Note for the session: this is already mechanically enforced --
the ADR-85 Stop-gate blocks a stop without a JOURNAL commit-SHA anchor, ship-gate blocks
the merge, merges are serialized. So this is not new machinery; it is writing an existing
guarantee into the boot contract so the incoming seat can rely on it instead of
re-verifying it.

(b) ONE-ROUND-TRIP BOOT. The operator's complaint, and it is fair: the probe gate currently
makes HIM ferry command output -- git HEAD, counts, clean-tree status -- between CC and the
browser, one probe at a time. That is machine-cheap work costing human turns. Direction:
a single CC-side command runs the entire gate plus the orientation reads and emits ONE
evidence block; the operator pastes once; the browser consumes a table instead of dictating
commands.

NON-NEGOTIABLE to keep in any redesign: verification of INHERITED CLAIMS stays. It is what
caught the near-reversal of a binding ruling this week (a claim inherited through a
supplement, refuted only because someone checked). But it is CC-side grep work, not
operator ferrying. Cheap-to-verify state (HEAD, counts, tree) can be batched; inherited
claims still get checked.
