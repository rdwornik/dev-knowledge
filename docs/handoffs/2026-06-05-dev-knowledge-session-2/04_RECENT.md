===== FILE: 04_RECENT — start =====

# 04 · What just happened

A narrative of recent work on `.dev-knowledge`, written so a chat with zero prior
context can pick up the thread. Prose, not a log dump.

## The arc

The recent window was dominated by **HANDOFF_PROCESS evolution** plus one instructive
verification failure. Three threads landed, all merged to `main`:

**Thread 1 — the Phase-D handoff completed (Phase 2).** The
`2026-06-05-dev-knowledge-session` bundle was generated (8 files), the
`docs/handoff-2026-06-05` branch merged, and `in-progress/` removed. That bundle is
stamped `HANDOFF_PROCESS v4.3.2 (status: beta)` — generated from the live spec,
deliberately overriding the then-stale skill stamp. It is the Phase-D chat's onboarding
material and is **immutable** — do not regenerate it under v4.4.

**Thread 2 — the ARCHITECTURE verification incident** (the window's most instructive
failure). A cross-repo sweep's staleness map claimed "cloud-night + nightly Action ARE
present" in `ARCHITECTURE.md`. Rob distrusted it; a grep of the live ~543-line file
proved him right — **zero** coverage of the GitHub remote/push, the nightly Routine,
spec-orchestration, the in-repo workflow, or the Action. Worse, the ADR-68 night-agent
passage still describes a never-registered mechanism as if live `[REFUTED — historical:
the night-agent was never a registered task; superseded in reality by the cloud
Routine]`. The map's parenthetical was a verification miss (likely confused with
CONTRIBUTING's real section). Corrected on the handoff branch **before** Phase 2
(`19c2b72`): the ARCHITECTURE row was rewritten to the operator-verified verdict. Two
durable insights: (a) **a staleness map is itself prose-about-state — verify-from-source
applies to verification artifacts too**; (b) **coverage drift is a third rot class**
(docs not knowing a new subsystem exists), distinct from mechanically-checkable claims
(`[#89]`) and semantic claims — its guardian is the change process (arc done = doc-touch
OR an explicit deferral entry).

**Thread 3 — handoff-process research + v4.4.** Rob asked whether the handoff process
maximizes what an LLM can actually absorb. Web research across four independent lines
(U-shaped positional attention / lost-in-the-middle; Chroma's context-rot + distractor
findings; Anthropic long-context guidance incl. quote-grounding; the multi-turn
lost-in-conversation study with its CONCAT result) **validated five existing pillars**
— single-message paste, the comprehension gate + abort ladder, tight line budgets,
pointers-over-copies, four-tag discipline — and motivated **six amendments (A1–A6)**,
shipped as **v4.4** on `feat/handoff-v4.4`, merged `--no-ff` (`ec1d0cf`). The six: **A1**
`05_NOW` top-landmines tail (two sub-blocks at the recency peak); **A2** dual-position
safety invariants (01_ROLE primacy + 05_NOW recency), anti-dedup guarded; **A3** `06`
answers must cite bundle file + section; **A4** `04_RECENT` final-state narrative,
refuted threads labelled `[REFUTED — historical]`; **A5** `===== FILE: NN =====`
separators on 01–07; **A6** fixed permanent Q8 first-move recitation. No budget number
changed. Bonus: the `/handoff` skill's version-drift class was killed — it now reads
version/status from the spec header + latest amendment Status line.

> **Phase-2 currency note (verified this handoff):** since the sender's stated capture
> (`d031d39`), two more increments landed on `main`: the `2026-06-05-dev-knowledge-v44-wrap`
> handoff bundle merged (`e90a1fe`) and a template-refresh chore (`2bac2d2`: 01_ROLE
> standing-preferences refresh + README Q-count fix). Current `main` tip at this Phase-2
> capture is `e90a1fe`. See the Load-bearing facts table for the HEAD cross-check.

## Four-tag discipline (canonical)

The sage tagged every claim using this discipline (canonical per HANDOFF_PROCESS
v4.3 Amendment A; supersedes the earlier three-tag body in spec §3.1):

- **witnessed** — sage just verified this OR saw it happen recently AND has no
  reason to think it changed since
- **recall** — sage remembers from earlier in the session; **state may have
  changed** — verify via CC inline if the claim is load-bearing
- **inferred** — reasoning from evidence (not direct knowledge)
- **unknown** — sage doesn't know — flagged explicitly

When you encounter `recall` or `unknown` on a load-bearing claim in this file,
verify via CC before acting on it. This is the "handoff is back-and-forth" rule.

## What the sender chat said (interview)

The sender summarized the window as three merged threads (above), all `witnessed`. Two
operator decisions were recorded: (1) **the 8-file bundle count stays** — the
load-bearing distinction is *consolidation at generation* (bad: LLMs degrade producing
one long file) vs *consolidation at delivery* (good: one pasted message ≈ single-turn
quality); small files to produce, one message to consume. (2) **Improvement cadence is
step-by-step** — one refinement per handoff, no drastic redesigns. A small **v4.5
candidate was parked, deliberately not implemented**: Q5 elicits narrative but A1 needs
≤5 one-line imperatives — asking the sage to end Q5 with a ready top-5 do-not list would
remove one synthesis step. Evaluate after v4.4's first real exercise.

## Load-bearing facts (cross-checked vs repo at Phase 2)

| Claim from sender | Repo fact | Phase-2 verdict | Verification command |
|---|---|---|---|
| `2026-06-05-dev-knowledge-session` bundle generated, stamped v4.3.2/beta, immutable | Bundle dir exists; README stamp = `v4.3.2 (status: beta)` | ✅ matches | `grep -i "Generated by" docs/handoffs/2026-06-05-dev-knowledge-session/README.md` |
| v4.4 merged `--no-ff` (`ec1d0cf`); ARCHITECTURE fix (`19c2b72`) | Both SHAs present with the described messages | ✅ matches | `git log --oneline -1 <sha>` |
| "tip at capture: `d031d39`" | `d031d39` is one session back; **current `main` tip = `e90a1fe`** (the v44-wrap merge + the `2bac2d2` template chore landed since) | ⚠️ stale — sender narrated the prior window; this handoff captures `e90a1fe` | `git rev-parse main; git log --oneline d031d39..main` |
| v4.4 ships **beta** with a built-in promotion test | Spec v4.4 latest-amendment Status line = `beta` | ✅ matches | `grep -nE "Ships at status" protocols/HANDOFF_PROCESS.md` |
| `docs/machinery-inventory` branch **may still exist** — adjudicate `[recall]` | **No branch matching `*machinery-inventory*`** locally or on `origin` — already gone (also resolved in the v44-wrap bundle) | ⚠️ resolved — branch absent; recall was stale | `git branch -a --list "*machinery-inventory*"` |
| Current `main` tip = `e90a1fe` | session-2 branch merged (`239c19a`) + chore `a102c43`; tip now `a102c43` | superseded post-Phase-2 — anticipated movement, not drift | `git log --oneline e90a1fe..main` |

## Decisions & reasoning to carry forward

- **Research-before-amending.** v4.4 changed the process only where four independent
  research lines demanded it; the five validated pillars were explicitly left untouched.
- **Generation vs delivery consolidation** (the operator's resolved fear): output
  quality degrades on long single-file *generation*; input quality is preserved by
  single-message *delivery*. The 8-file/1-paste architecture hits both optima.
- **Positional redundancy is a feature.** A1/A2 deliberately duplicate content at the
  two attention peaks with anti-dedup guard comments — a future doc-rot audit *will*
  try to "fix" the duplication unless told not to. Encode the defense at write time.
- **Beta with a built-in measurement.** v4.4's promotion criterion doubles as the
  experiment: does the critical-finding count drop under the new bundle shape?
- **The contract-premise pattern cut both ways.** The architect's v4.4 contract carried
  wrong premises that CC's exploration corrected against repo reality. Verify-before-encode
  is symmetric — the executor's reality-check is as valuable as the architect's.

===== FILE: 04_RECENT — end =====
