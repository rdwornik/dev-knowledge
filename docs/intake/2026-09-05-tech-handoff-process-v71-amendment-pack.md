---
intake-id: 68
status: DRAFT
origin: outgoing Layer-1 browser-seat notes, window 2026-09-02 -> 2026-09-05, section 2; landed at docs/audits/2026-09-05-technical-browser-seat-notes.md and filed by lane worktree-docs-seat-notes on 2026-09-05
consumed-by:
reconciled_with: handoff-process@7.0.0
---

# HANDOFF_PROCESS v7.1 amendment pack — what the v7 bundle did not carry

## Problem / motivation

The v7 handoff bundle is the browser seat's entire view of the repo at boot. One window ran
against it end to end and produced a recorded error register: sixteen defects in six
classes, of which the largest single class is **premise-from-summary** — the seat ruled
from summaries and defect reports where the row's own `Done-when` and the live file were
one pull away. The outgoing seat's own diagnosis is that *"the bundle made this easy by
carrying §3 of the close packet and not the rows"*. That is a statement about what the
bundle **carries**, not about the seat's diligence: the same seat, given the row text,
would not have cut nine lane contracts from defect narrative and closed three rows.

So the deltas below are requirements on the **bundle's content**, gathered while the cost
of their absence was being paid. They are filed here rather than applied because §2 of the
source says so in its own heading — *"file through the funnel; not a bump by fiat"*. An
amendment pack that edits `protocols/HANDOFF_PROCESS.md` on the strength of one window's
frustration is exactly the rival-authority failure this corpus already has lessons about.

**No version bump is proposed by this document.** Whether these become v7.1, or some subset
does, or they land as a different mechanism entirely, is the ratification decision this
intake exists to feed — not a fact it asserts.

## Scenarios (+1 view)

- **As the browser seat, at boot, I open the bundle and read a row's acceptance condition
  in the row's own words.** I write a closure clause that quotes it. The clause is
  therefore about the row and not about the defect report that happened to sit next to it,
  and a lane built from it can be checked against something. Today I read close-packet §3
  and write a clause that closes a defect while the row stays open — witnessed nine times
  in one batch, three rows actually closed.
- **As the browser seat, I am about to rule that a gate is green.** The bundle tells me, in
  one line, what REDs that gate. I discover that undispositioned WARNs RED the ship-gate
  *before* I declare G0 green, rather than after the STOP and the ruling that followed it.
- **As the browser seat, I rule on a cross-repo file.** The bundle carries the last commit
  touching it. I see that win-tooling fixed the thing four days ago (`d6cbd92`) and do not
  spend a ruling and a rescope on a defect that no longer exists.
- **As the browser seat, I plan parallel lanes.** The bundle tells me which session holds
  the primary checkout and which worktrees are live and whose. I do not allow six
  concurrent writers into one checkout until a TOCTOU puts a commit on main under a passing
  gate.
- **As the operator, at the end of a window, I read a scorecard whose numbers each name the
  SHA they were measured at.** I can tell whether the window moved anything without
  reconstructing it from a merge list.

## Functional requirements

The ten deltas, **verbatim** from the source §2 — reproduced without edit, reordering or
renumbering, because the pack's value is that it was written while the absence was being
paid for. Interpretation belongs in ratification, not in transcription:

1. **Rows on the agenda: Done-when VERBATIM**, one block per row, with the row's file path. The close-packet defect text is context, never the closure source.
2. **Gate semantics in one line each**: what REDs ship-gate (hard-fail organs OR undispositioned WARN count), what the Stop hook can block (nothing), what pre-push blocks (unanchored range). The seat ruled on gates it had not read.
3. **Cross-repo state for every path the agenda names**: `git log -1` in win-tooling for dispatch helpers; the L0 (`~/.claude`) dirty-file list. Two rulings this window were stale on cross-repo facts.
4. **Substrate block, rewritten**: the three verbs with the doctrine line; base failed-set PER SUBSTRATE with its source rule (run report); the current hold (if any) with its row id; the last codespace witness SHA.
5. **Live-session census**: which session holds the primary, which worktrees are live and whose. The seat could not see six concurrent writers.
6. **Coupling-scan output for the agenda's symbols** (or a probe row that runs it): the files that reference each constant/function the agenda will touch.
7. **Scorecard section** (ten numbers, candidate under `window_metrics.py`): rows closed/touched · hard-fail + WARN with trend · failing nodeids + baseline seconds · P1 pre-merge / regressions at merge · time-to-merge per lane · % lanes on codespace · asks RED/re-asked · bundle bytes + window-specific % · consumers at 0 FAIL · tokens by model class. Numbers in the bundle name the SHA they were measured at.
8. **Interface behaviours**, not only constants (Q7 extension landed in G7 clause 5): copy-ready blocks, .md transport, END sentinel, Downloads fallback, "which session tile" naming.
9. **Probe prose once** (G7 landed the measure: cut 29,776 B / 32 % window-specific against 20 KB / 70 %). The next cut should show the trend line, not just the miss.
10. **Providers used vs promised**, per window: this window — terra used (8 reviews, 10 P1); Gemini used ONCE with measured fidelity (6/6 locators, 0 fabrications, 1 overclaim of files read); Grok not admitted; sol unconfirmed on G7; codespace used once (G5) then held.

**Item 11 — appended 2026-09-05, NOT from the source §2.** It arrives from the architect
inbox (item 005-C) and is kept outside the verbatim block above so that block stays exactly
the ten deltas the outgoing seat wrote. Same standing as items 1-10 for ratification; a
different provenance, stated rather than blended:

11. **The bundle's interface section names the TRANSPORT** — prompts dir, `to-cc\`,
    `to-browser\`, the read rule, and the `DONE <sha>` copy witness. `HANDOFF_BOOT.md` gets
    **one pointer line** to `protocols/OPERATOR-INTERFACE.md` §1. The hub-canonical route is
    via this amendment pack, **not** a direct edit to `HANDOFF_BOOT.md`; the browser's memory
    entry is a **CACHE** of §1, never its source.

    Filing note, resolved rather than assumed: §1 exists on `main` today as *"File exchange
    goes through the Downloads directory"*, but the **transport constant** this item points at
    — the prompts-dir/`to-cc\`/`to-browser\`/read-rule/copy-header/session-start/inbox-naming
    block — is landed on `worktree-filings` (`6998d2b0`) and is **not on `main` at the time of
    this filing**. So the pointer target is real but not yet integrated; a ratification that
    lands item 11 before that branch merges would be citing a section whose cited content the
    reader cannot open. Deliberately a **pointer**, not a restatement — a second copy in the
    bundle is the drift this item exists to prevent.

Grouped into the shape a ratification would rule on (this grouping is the filing lane's,
not the source's):

- **Must:** items 1-3 — the three that map directly onto recorded defects with measured
  cost (rows' `Done-when` verbatim; gate semantics; cross-repo state). Item 1 alone is the
  named cause of the 9-lanes/3-closures result.
- **Should:** items 4-6 — substrate block, live-session census, coupling-scan output. Each
  has a witnessed incident behind it (contention on the operator's host; six concurrent
  writers; a write-scope frozen without a coupling scan, costing two escalations and a lane
  cut mid-batch).
- **Could:** items 7-10 — scorecard, interface behaviours, probe-prose trend, providers used
  vs promised. These improve the record rather than prevent a recorded defect class, and
  item 7 in particular names a mechanism (`window_metrics.py`) that does not exist and would
  itself need triage.
- **Must (appended):** item 11 — a pointer line, not content. It is grouped Must because the failure it prevents is a seat reading a stale cache of a transport it cannot otherwise resolve, and because its cost is one line.

## Acceptance criteria (ex-ante)

Written before any build, and deliberately phrased as things a reader can check on a
generated bundle rather than as impressions of it:

1. For a bundle generated against an agenda of N rows, **each of the N rows has a block
   carrying its `Done-when` text and its `tasks/` file path**, and the text matches the
   row's file byte-for-byte. A bundle that carries a close-packet section and no row blocks
   fails this criterion.
2. **Every gate the bundle names carries a one-line RED condition.** Checkable by
   enumerating the gate names in the bundle and asserting each has such a line;
   specifically, the ship-gate's line names undispositioned WARNs, and pre-push's names an
   unanchored range.
3. For **every cross-repo path the agenda names**, the bundle carries a last-commit line
   (SHA + date) derived at generation time. A path with no such line fails.
4. **Every number in the bundle names the SHA it was measured at.** A bare number fails.
   This is the criterion the source states explicitly for the scorecard and it generalises.
5. The bundle carries a **live-session census** — which session holds the primary, which
   worktrees are live — derived at generation time, not restated.
6. **No criterion in the pack can be satisfied by the calendar.** Aggregate-count targets
   that move with the date (the `133 -> <=123` shape, defect 9 in the source register) are
   rejected at review; criteria name findings.
7. The equilibrium measure the source proposes — **"needs input" events per batch** — is
   recorded for the batch that first runs under the amended bundle, against the stated
   baseline of ~10 for batch G. This is a **measurement**, not a pass/fail bar; whether <=3
   becomes a target is a ratification question, not an ex-ante assertion here.

## Non-goals

- **A version bump.** This document proposes no edit to `protocols/HANDOFF_PROCESS.md` and
  does not assert that the result is called v7.1.
- **Building `window_metrics.py`.** Item 7 names it as a candidate home; naming a module is
  not filing it. If the scorecard is ratified, its home is a separate technical question.
- **Re-litigating the source's error register.** §1 of the landed notes is the incoming
  seat's reading of its own window. It is context for why these ten items exist, not a
  finding set this intake triages.
- **Ruling on the §3 boot proposals.** Those are intake #69 and are deliberately separate:
  #69 changes what the repo *proposes*, this changes what the bundle *carries*.
- **Deciding whether the constants belong in the bundle or in a skill.** The source's §3
  raises "skills over reference" as an open direction; it is not resolved here.

## Impact sketch (4+1 lite)

- **Logical:** the bundle gains three classes of content it does not model today — per-row
  acceptance text, per-gate RED conditions, and derived cross-repo/live state. The third
  class is the structurally new one: today's bundle is assembled from in-repo text, and
  these are facts that must be *derived at generation time* or they decay in transit.
- **Process:** shifts work from the seat's boot (three operator pastes before the first
  ruling, per the source) into generation. The seat reads rows instead of reconstructing
  them; the review step gains an explicit check that no criterion is calendar-satisfiable.
- **Development:** touches the handoff generator and `protocols/HANDOFF_PROCESS.md`. Items
  3, 5 and 6 need generation-time derivation (cross-repo `git log -1`, a worktree/session
  census, a symbol coupling scan) — the coupling scan may already exist as a probe and
  should be reused rather than re-declared.
- **Physical:** bundle bytes go **up** against a live thinning arc ([#611], and G7's
  measured 29,776 B / 32 % window-specific cut). This is the pack's main tension and it is
  named here rather than smoothed over — see Open questions.

## Open questions

- **Bytes vs completeness.** Every item adds to a bundle that a separate arc is actively
  cutting. Which wins where they conflict is an operator/architect call, not a filing
  decision. Item 9 hints at the reconciliation (measure the trend, not just the miss) but
  does not resolve it.
- **Which items are DERIVED and which are AUTHORED.** A derived item stays true; an authored
  one decays in transit, which is the failure class the source's own §1 keeps producing.
  Items 3, 5 and 6 look mechanically derivable; items 1, 2 and 4 may be partly authored.
  Classifying all ten is a technical-architect question.
- **Does item 7's scorecard duplicate an existing surface?** FUNNEL HEALTH and the fleet
  digest already emit numbers at boot. Whether the scorecard is a new surface or a re-cut of
  those is unanswered here.
- **Item 2's gate semantics are a restatement.** A one-line RED condition copied into the
  bundle is a fact carried, not derived — the exact shape LESSONS already rules against
  ("a transferred fact carries a locator or is derived on site"). Whether the bundle should
  carry the line or the command that prints it is open.
- **Genre.** The ten items are phrased as bundle contents, which reads closer to HOW than
  ADR-98's WHAT/WHY line strictly admits. They are landed verbatim because the operator's
  instruction was verbatim and because paraphrasing a requirements list is how scope is
  lost. A ratification may legitimately re-cut them into problem statements.

## Status

DRAFT — filed 2026-09-05 by lane `worktree-docs-seat-notes` as a CANDIDATE per ADR-111
(CANDIDATE -> intake -> ratification). Not triaged, not ratified, no backlog row born from
it. Source landed verbatim at `docs/audits/2026-09-05-technical-browser-seat-notes.md` §2.
