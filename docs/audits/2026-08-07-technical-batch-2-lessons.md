---
batch: 2
consolidates: docs/audits/2026-08-07-technical-batch-2-packet.md
---

# Batch 2 — lessons register: the defect classes, and the mechanism each one became

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-07 · **Slug:** batch-2-lessons
- **Arc:** the consolidation arc dispatched after batch 2 closed (`8bef876e`), branch
  `docs/consolidate-batch2-lessons`, primary checkout.
- **Input:** `docs/audits/2026-08-07-technical-batch-2-packet.md` (the integrator's packet) and
  its manifest `docs/audits/2026-08-07-technical-batch-2-manifest.md`.

**What this file is for.** The packet closed the batch and listed ten deferred items with owners.
This file does the next thing: it turns the recurring **classes** into landed mechanisms, records
the three machinery findings as **proposals for adjudication rather than as landed decisions**,
and hands the operator the decisions only they can take. A lesson that stays a lesson is a lesson
that gets re-learned.

**Second-seat note, applied to this file itself.** Where a count or a claim came from the arc's
frozen contract rather than from an artifact I could re-read, it says so. Section 2 contains one
class whose instance-mapping is my inference and is marked as such, and one class whose stated
count I could not fully reconstruct. Recording that is cheaper than a tidy table that is wrong —
and it is the same F3 discipline this arc landed.

---

## 1. Defect class → mechanism — what actually shipped

| # | Defect class | Batch-2 instance | Mechanism landed this arc | Where it lives |
|---|---|---|---|---|
| 1 | **Ruling without a locator** | `[#430]`(a) and the AM-1/AM-2 ratification | **STANDING_RULINGS F5** — every ruling that steers a lane, picker answers included, gets a register line in the same batch it steers; **first instance executed in the same commit** | `protocols/STANDING_RULINGS.md` F5 |
| 2 | **Invented identifier** | the manifest's digit lane-grammar; the minted `declared_by` token; batch-1's two off-enum audit filenames | **STANDING_RULINGS F2** — names, paths and identifiers derive from validators and enums, in contracts *and* manifests | `protocols/STANDING_RULINGS.md` F2 |
| 3 | **Author verifying their own premise** | the integrator repeating lane-1's ruling claim as fact; lane-2's proof putting cwd on `sys.path` | **STANDING_RULINGS F3** — an author's packet carries claims; a second seat converts a claim into a finding | `protocols/STANDING_RULINGS.md` F3 |
| 4 | **False-resolve over declared absence** | `[#490]` closing at 9/9 with 4 genuinely unonboarded | **STANDING_RULINGS F4** — declare the absence with its count | `protocols/STANDING_RULINGS.md` F4 |
| 5 | **Destructive act against a stale authorization** | (no batch-2 instance — carried in by the contract) | **STANDING_RULINGS F1** — re-verify reflog + parents at execution time, halt on mismatch | `protocols/STANDING_RULINGS.md` F1 |
| 6 | **A gate with no mechanism behind it** | `win-tooling` has no `origin` at all, so its backup posture is unenforceable by construction | the operator decision in §4 + `[#509]` for the dispatch-wrapper half | §4 below; `BACKLOG.md` `[#509]` |
| 7 | **The exemption is self-grantable** | renaming lane-1's branch is what granted it R-1 | `[#510]` filed (M, not S — §3.1) **plus** a behavioural pin so the push leg's unconditionality is tested, not asserted | `tests/test_adr85_integration_enforcement.py::test_t5d_…` |
| 8 | **Dispatch routing left to inheritance** | model/effort unstated per lane | the **routing matrix** at Ch8; the dispatch line becomes authoritative; S-class contracts drop the Model/Mode/Effort table | `protocols/PLAYBOOK.md` Ch8; `templates/prompt-template.md` v1.10 |
| 9 | **The plan is in the tree, the contracts are not** | `[#505]` clause 1 falsified on exactly this | the **contract-of-record** path: at dispatch the manifest links or embeds each frozen lane contract as a committed artifact | `protocols/PLAYBOOK.md` Ch8 |
| 10 | **The successor inherits a chat, not a system** | four things a new architect cannot infer | the **handoff-prep index** — pointers only, no restatement | `protocols/PLAYBOOK.md` Ch8 |

**GREEN-on-branch ≠ GREEN-on-main** is the eleventh class and is the one that needed **no** new
mechanism: PLAYBOOK Ch8 already carries it ("A claim of green names WHERE it is green",
transcribed 2026-07-31, `[#446]`). Batch 2 honoured it — per-lane greens were treated as evidence
about each lane in isolation, and the verdict came from **one suite run on the merged tree**
(packet §5). Recorded here as a class that held, because a lessons register that lists only
failures mis-describes the batch.

---

## 2. The two classes this file cannot close cleanly, stated rather than smoothed

**2.1 · "Author + author's-test blind spot ×4" — I can locate two with citations, not four.**
The contract names four instances. Re-reading the packet, the two that are unambiguously this
class are: the integrator's own `a96040c3`, which repeated lane-1's "permitted fleet-wide" as
verified fact and was self-corrected at `63b7b6a9` (§4); and lane-2's proof running
`python -m pytest`, which puts cwd on `sys.path`, so a flat-layout package passed **because the
proof put it there** (§11). Two further candidates exist and are *not* the same class on
inspection — lane-1's and lane-2's terra findings are an **independent** reviewer catching author
defects, which is the mechanism working rather than the blind spot. The remaining two instances
are presumably in the lane transcripts, which are not repo artifacts and which I did not read.
**So: the class is real and landed as F3; the count of four is the contract's, not this file's.**

**2.2 · "Mid-flight-sample misread" — the label is the contract's; the mapping below is my
inference and is flagged as such.** The best-fitting instance I can locate is the manifest's
own "five gate firings per batch" rationale at width 6: an estimate produced before execution,
which the packet then showed to be an **upper bound rather than a prediction** (§2), because
`pre-commit` does not run on a conflict-free merge. A figure sampled from a plan and carried as
though it were a measurement is the shape the label describes. **I did not find an artifact
naming this label**, so if the architect meant a different instance, this mapping is wrong and
the correction belongs in the next window. Recorded this way deliberately: this is itself an F5
instance — a lesson label whose only carrier is the frozen contract.

---

## 3. The integrator's three machinery findings — PROPOSALS, not landed decisions

Each is recorded with a proposed resolution for the operator to adjudicate. **None is
implemented.** ADR content is untouched, per this arc's contract.

### 3.1 · `pre-commit` does not fire on a conflict-free merge, so R-1's commit-time leg is narrower than designed

**The finding (packet §2), independently confirmed here.** Git invokes `commit-msg` for an
auto-committing merge but not `pre-commit`. On batch 2's two conflict-free lane merges
(`ea4ddf23`, `e685a306`) only the two commit-msg hooks ran — `audit-health` never fired. It ran,
and passed, on the two **conflicted** merges (`47bd4f52`, `ad9332c3`), where conflict resolution
forces an explicit `git commit`.

**What this does and does not mean.** R-1's protection is real but **conditional on a merge
conflicting**. This is not a hole: a conflict-free merge needs no exemption because nothing
evaluates it. What it does mean is that the manifest's width-6 "five firings per batch" figure is
an upper bound, and that R-1's value is smaller than its design assumed.

**Proposal for adjudication — a simplification candidate, deliberately phrased as a question.**
If the exemption only ever fires on conflicted merges, is the exemption machinery worth its
second exemption surface on a gate whose value is having none (the third of
`batch_manifest.py`'s own honest limits)? Two coherent answers: **(a) keep it** — the conflicted
case is exactly the case a human is already stopped in, which is the worst moment for a gate to
force `SKIP=audit-health`; or **(b) narrow it** — record the conflict-only reality in ADR-110's
amendment text so no successor plans capacity around five firings. **This file recommends (a)
plus the (b) text**, since the two are not exclusive and (b) costs one paragraph. Not landed.

### 3.2 · The ≤1/4 process-lane cap is width-dependent and breaks under truncation

**The finding (packet §8).** The manifest planned width 6 as 5 feature/consumer + 1 process,
compliant. The batch **ran at width 3**, and `floor(3/4) = 0` process lanes are permitted at that
width — so the executed batch exceeds a cap it was planned to satisfy, **retroactively**, without
anyone doing anything. Under the stricter reading the manifest itself surfaced, all three lanes
are hub-methodology work and the hub supplies zero product lanes by construction.

**Proposal for adjudication.** Evaluate the cap against **dispatched width**, and report the
**close-width delta** in the end-of-batch packet. Rationale: the cap exists to stop methodology
work expanding to fill available width, and that expansion is a **planning-time** behaviour — so
planning-time width is the honest denominator. Truncation is a schedule event, not a
composition choice, and a cap that a schedule event can violate is measuring the wrong thing. The
close-width delta keeps the shortfall visible, which is the property the cap's own
"report the shortfall and run narrower" clause already asks for. Not landed; the cap's text is
operator-directive doctrine (2026-08-06) carried by intake #27.

### 3.3 · `[#505]` clause 2 is ambiguous — per batch or per integration?

**The finding (packet §7).** Measured for the first time, and the answer depends entirely on the
unit. Counted from session transcripts: AM4-FOLD 1, lane-1 2, lane-2 1, lane-3 1, integrator 1 =
**6**, plus the packet hand-back = **7**. Per-batch reading: **7 ≫ 2, falsified.** Per-integration
reading — the GO plus the packet, which is what `/lane-integrate` §0 actually says: **exactly 2,
met.** The row does not say which it means, and the packet declined to pick, correctly: a single
number there would have been a choice dressed as a measurement.

**Proposed wording, for operator ratification — the precise sentence, so ratification is a yes/no
rather than a drafting exercise:**

> **Clause 2 (proposed).** The 2-touch budget is measured **per seam, per batch**, and the two
> seams are counted separately. *operator ↔ integration*: the GO at dispatch and the
> end-of-batch packet at close — target exactly 2. *operator ↔ lanes*: one dispatch per lane,
> plus any ask-class (a)–(c) escalation — target ≤1 escalation per batch, reported in the packet
> rather than budgeted away. A batch reports both numbers; neither substitutes for the other.

**Why this shape.** It keeps the metric the row was filed for (the integration seam, where 2 is
achievable and was achieved) without pretending the lane seam is free — batch 2's single
mid-lane escalation was legitimate and would be punished by a per-batch total of 2. It also makes
the existing "2-touch transport, on both seams" PLAYBOOK text and the row agree, which they
currently do not. **Not landed** — `[#505]` stays open and this clause is a proposal.

---

## 4. Operator decisions — the list only the operator can take

1. **`win-tooling` has no `origin` remote at all, and 14 branches of real typewhisper work are
   local-only, on one disk.** Found by lane-3 outside `[#320]`'s done-when (which names three
   repos, all discharged), so it did not block that close — but it is the same single-disk
   data-safety class the row was filed for. The fork is **add a remote** or **accept-local with a
   recorded reason**; both are dispatch acts, forbidden to batch 2's integrator and to this arc.
   *Highest-value item on this list: it is the only one where the failure mode is losing work.*

2. **The ADR-87 residual opened by this arc's own routing-matrix ruling.** The matrix puts model
   **and** effort on the architect's dispatch line; ADR-87's equilibrium ("The two lifelines"
   § Lifeline 1, restated at §2 "How to choose Model") puts model selection on CC's side and keeps
   the architect out. This arc declared a **population boundary** rather than editing either — the
   architect states the tier a session *boots at*, CC keeps routing sub-steps *inside* it — and
   added reciprocal pointers, following the `prompt-template` v1.7 precedent. **The residual: the
   ADR-87 table and its §2 restatement still read as architect-excluded on the dispatch act
   itself.** Ratify the boundary as written, or rule an ADR-87 amendment. Recorded here because
   the Ch8 text points at this file for it.

3. **`check-seal-identity` fails `pre-commit run --all-files` on an immutable bundle.**
   `docs/handoffs/2026-08-01-dev-knowledge-architect-2` declares slug
   `2026-08-01-dev-knowledge-architect` while its directory carries the `-2` suffix. Verified
   pre-existing (added at `80dd54d6`) and untouched by batch 2. `docs/handoffs/` is immutable, so
   this is a real defect in an artifact that cannot be edited, and it will fail every `--all-files`
   sweep until someone rules **how an immutable bundle with a bad seal gets retired**.

4. **Two directory skeletons survive on disk** — `.claude/worktrees/dazzling-purring-ullman` and
   `.claude/worktrees/joyful-scribbling-hummingbird` — because their lane sessions were still
   alive at close (pids 19884, 12560). Both contain **zero files**; `git worktree list` returns
   the primary only. They vanish when those sessions close. Against CLAUDE.md §5 rule 9 this is a
   reported residue, and killing an operator's sessions was correctly not the integrator's call.
   **Confirm they are gone, or authorize the force-removal.**

5. **Wave 2 (`[#283]` `[#416]` `[#393]`) is carried, not run**, and the manifest's own instruction
   applies before it does: `[#430]` (lane-1) and `[#393]` (lane-6) share `serialize-group:
   audit-py`, and `[#430]` is now **partly landed** — so that pair needs re-checking before lane-6
   runs.

---

## 5. What this arc landed, in one place

| Step | Artifact | Commit |
|---|---|---|
| 1 | Ch8 routing matrix + `prompt-template` v1.10 + reciprocal §2 pointer | `e03df5c4` |
| 2 | Ch8 prompts-dir + contract-of-record; `[#509]` filed | `c4d6db25` |
| 3 | `STANDING_RULINGS` section F (F1–F5) + the `[#430]`(a) locator | `6ae62c64` |
| 4 | push-leg behavioural pin (RED witnessed); `[#510]` filed | `69ddcb80` |
| 5 | handoff-cut profiled; `[#511]` filed | `e0a07c30` |
| 6 | Ch8 handoff-prep index + `HANDOFF_BOOT` template pointer | `ede671bb` |
| 7 | this file | *(this commit)* |

**Three rows filed, zero closed.** `[#509]` (win-tooling dispatch wrapper resolves
`CLAUDE_PROMPTS_DIR`), `[#510]` (scope the R-1 exemption to enumerated lanes), `[#511]` (the
handoff cut's session-time cost). `[#505]` and `[#502]` stay open per contract; `[#430]` stays
open on (b) and its (a) ruling now has a locator.

**`silent_rule_ratchet` held at 441 ≤ 441 at every commit**, measured against the staged blobs
before each one. Four of the seven commits touch files inside the detector corpus
(`protocols/*.md`, `templates/**`), and every payload was pre-checked at zero normative-keyword
occurrences before it was applied rather than measured afterwards and reworded.

---

**Batch 2's lessons are mechanisms now, not notes.** Five register entries, two Ch8 sections plus
an index, one template version, one behavioural test with its RED witnessed, three rows filed with
their evidence, and five decisions handed to the operator with the fork stated for each. The two
places where the record could not carry the contract's own claim are marked as such rather than
tidied — which is the F3 discipline this arc landed, applied to the arc.
