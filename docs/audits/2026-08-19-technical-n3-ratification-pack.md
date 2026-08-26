# N3 RATIFICATION PACK — intakes #35–#39 (DRAFTS ONLY)

<!-- scope: meta -->

**Class:** technical · **Date:** 2026-08-19 · **Lane:** night research lane, claude cloud channel
**Branch:** `claude/n3-ratification-pack-35-39-nhqkd3` · **Contract of record:**
`docs/audits/2026-08-19-technical-n3-ratification-pack-contract.md`

**Posture — read this before acting on anything below.** Nothing in this file is live. Every
intake still reads `status: DRAFT`; no row was born; no ADR file exists; `BACKLOG.md` and
`tasks/` were not touched; nothing was merged. This artifact is a **staging pack**: five
ratification proposals, drafted so the seat can execute them tomorrow by copying rather than
re-deriving. Every id in every drafted row is the literal placeholder `#RESERVED`, which
deliberately fails `validate_backlog._TASK_RE` (`^- \[#(\d+)\]`) — a draft row cannot be pasted
live by accident, it has to be given a real integer first.

---

## 0 · The governance frame this pack executes against

Four rules bind, and they are cited rather than restated:

1. **ADR-98 §3** — an ADR is authored *only at a genuine fork* (**0..n per intake**); a backlog
   epic is the work (**1..n per accepted intake**), citing its `intake-id` **and** the ADR-id(s)
   it rests on; acceptance criteria copy **VERBATIM** from the intake into the row's Done-when.
2. **ADR-111 §4** — birth requires a **ratified intake**. The only path from a finding to a row
   runs (c) CANDIDATE → intake → ratification. Outcome **(a) OWNED** — "an open row already
   covers it, attach evidence and birth nothing" — is the cheapest lawful discharge and this pack
   uses it once (#39 / `[#554]`).
3. **ADR-112 fork test** — two legs, both must pass for an ADR: (leg 1) a reasonable person could
   choose otherwise, and (leg 2) reversal is asymmetric and expensive. Every ADR-vs-rows verdict
   in §3–§7 states which legs it passes and where a leg is weak.
4. **The seat's anti-orphan rule** (ruled, reviewer-approved; supplied by this lane's dispatch and
   **not yet carrying an in-repo locator** — the seat should record it, `protocols/STANDING_RULINGS.md`
   is the obvious home): each intake, on flip to ACCEPTED, carries either **≥1 carrier row** or
   **`disposition: deferred` with a LIVE, DATED trigger**. Never ACCEPTED-with-zero-carrier.

**How the anti-orphan rule reconciles with ADR-98 §3.** §3's "1..n per accepted intake" reads as
an absolute — every ACCEPTED intake owes at least one epic. The deferral escape is not a weakening
of it but the honest expression of `disposition: deferred` = *"parked but alive"*
(`docs/intake/README.md` §5): the rows are still owed, the trigger says when. What the rule
forbids is the third state — ACCEPTED, `disposition: active`, zero carriers — which is the shape
that produces an authority nobody is building. That shape has a measured instance in this repo:
the census found **`dev-knowledge-kernel` → 0 hits tree-wide**, ACCEPTED by intake on 2026-08-05,
and §6 of this pack is the act that closes it.

**One gating fact, stated once rather than five times.** A DRAFT→ACCEPTED flip requires
`decided-by` naming a real ruling (`docs/intake/README.md` §3, REQUIRED at ACCEPTED). This lane
cannot manufacture one. Every "flip to ACCEPTED" below is therefore staged for an **operator/
architect ruling act**, not something the seat performs unilaterally; and the three drafted ADRs
land **`Status: Proposed`**, because ratification is a separate operator act (the ADR-112
precedent, which was authored Proposed and ratified later, and whose own "Status note — read this
before citing the ADR" block is the shape reproduced here).

---

## 1 · Ledger arithmetic

### 1.1 As supplied by the dispatch

> Ledger headroom after batch 1: **closures 6 / window births 3 → net +3**, so **up to ~5 births
> stay lawful** tomorrow.

### 1.2 As measured live on this branch (independent, so the seat can reconcile)

```
live task nodes in tasks/manifest.json         212
  status: open                                 188
  status: deferred                              24
  ------------------------------------------- ----
  H2 live denominator (open + deferred)        212

task files on disk under tasks/                288   (+ tasks/README.md, not a task)
  of which terminal: closed 72 / retired 3 /
    superseded 1                                  76   <- retired from the manifest, records kept
                                                      (ADR-107 section 6.3 retire-not-delete)
  live (= 288 - 76)                              212   <- reconciles with the manifest above

highest id allocated on disk                   558
highest id present in the live manifest        555
NEXT FREE ID                                   #559
```

**Reconciling "window births 3".** `[#556]` `[#557]` `[#558]` were all added on 2026-08-17 in one
commit (`69baa39`) and all closed at the batch-1 integration — those are the three. `[#554]` and
`[#555]` are the *prior* window's two births (JOURNAL 2026-08-17 (f), *"window close — two
births"*), which is why they are not in the count. The six closures are `[#505]` `[#556]`
`[#557]` `[#558]` `[#502]` `[#536]` (batch-1 integrator packet §4, *"Banked (6) … Births: 0 — as
instructed"*).

**Filter, per register H2.** The denominator above is the **live** count (`open` **plus**
`deferred`), because a deferred row is not a closed row. Stating the filter with the number is
H2's whole point — an unlabelled velocity figure is unreconcilable by the next seat.

### 1.3 What this pack spends

```
births drafted in this pack                      5
  #35 carrier (mechanize-not-prose pass)         1
  #36 carrier (gate-liveness harness)            1
  #37 carrier (done_when schema field)           1
  #38 carrier (kernel/lab tiering + package)     1   <- MANDATORY per the dispatch
  #39 carrier (CX re-base)                       1
  #39 second carrier                             0   <- OWNED by the existing open [#554]

headroom consumed                              5 of ~5      -> lands exactly on the ceiling
window arithmetic if all five land:
  births 3 + 5 = 8   vs   closures 6            -> window net +2 rows
  live denominator 212 -> 217 before any close tomorrow
```

**Consequence the seat should see before it starts.** Five births is the ceiling, not a target.
Landing all five puts the window at **net +2 rows**, so the seat needs **≥5 further closures in
the same window** to bring it back to net-non-positive. Against ADR-108 §B clause 3 (*"open
backlog < 100"*, scored on the H2 live denominator per register **L-3**), 212 → 217 moves in the
wrong direction. Two levers, both drafted below rather than merely named:

- **The cheapest cut is #38's R18** (`fleet_check.py` conformance scorecard). It is that intake's
  own *Must*, but it is **not** the mandatory one — the kernel row is — and §6.4 records what
  un-parks it. Cutting it costs nothing here because it was never in the five.
- **If the ledger squeezes the kernel row itself**, §6.5 carries the drafted deferral **with its
  dated trigger**, so the outcome is a recorded park, never silence. That is the dispatch's
  explicit instruction and it is honoured with text, not with a promise.

Every drafted row carries a `kill-candidates:` line, because the `backlog-filing-backpressure`
commit-msg hook BLOCKS a commit that adds a task id without one (≥1 existing `#id`, or
`none — <reason>`).

---

## 2 · Verdict table

| intake | subject | verdict | force-of-what | births | anti-orphan discharge |
|---|---|---|---|---|---|
| **#35** | agent instruction layers, distillation, unattended runs | **CLEAR** | **ADR** (AGENTS.md fork) **+ 1 row** | 1 | new carrier row |
| **#36** | repo autonomy, policy-as-code, gate liveness | **CLEAR** | **ADR** (bypass fork + autonomy rungs) **+ 1 row** | 1 | new carrier row |
| **#37** | machine-verifiable Done-when | **CLEAR — sequenced** | **ADR** (rule-7 reconciliation) **+ 1 row**; the row is BLOCKED until the ADR lands | 1 | new carrier row |
| **#38** | fleet config standardization at N=8 | **CLEAR** | **no ADR — rows only** | 1 | new carrier row (**mandatory**) |
| **#39** | off-machine agent substrate | **CLEAR** | **no ADR — rows only** | 1 | existing `[#554]` (OWNED) **+** new carrier row |

**No intake is BLOCKED outright.** #37 is the one conditional: its carrier row is blocked on a
ruling that this pack drafts, so the block is discharged *inside the same execution order* rather
than deferred out of the window. That conditional is real and the seat must not invert the
sequence — §5.2's ADR before §5.3's row.

---

## 3 · Intake #35 — Portable agent-instruction layers, prompt distillation, and unattended runs

`docs/intake/2026-08-17-tech-agent-instruction-layers-and-distillation.md` · **VERDICT: CLEAR**

### 3.1 Ratification summary (one paragraph)

What is accepted is the intake as a **requirements authority on the instruction surface**, and its
force is split: the AGENTS.md question is accepted **as an ADR**, because it is the one item in
this arc that cannot be built around — the intake's own R1 Done-when demands *"an ADR … that
either amends ADR-53 to admit AGENTS.md as a canonical layer or records the refusal with a stated
reason"*, and `CLAUDE.md` §10 currently names the memo's central recommendation as an
anti-pattern, so the two cannot both stand unruled. Everything else in the intake is accepted **as
rows**, of which exactly one is born now: the mechanize-not-prose classification pass (R2), which
is the intake's only proposal that relieves the 200-line budget *structurally* rather than by
condensing another history bullet into git. R3 (rule-adherence eval harness) is accepted in
principle and **not born**, on the intake's own instruction to fold it into the seeded-defect
corpus already gating `[#491]`/`[#492]` rather than birthing a second one; R4 and R5 are accepted
as *Could* and stay proposed, un-born, with no trigger owed because the intake itself rates
neither load-bearing until the fleet actually runs multi-vendor.

### 3.2 Draft ADR — fork test and text

**Fork test (ADR-112), both legs stated:**

- **Leg 1 — a reasonable person could choose otherwise: PASSES, demonstrably.** `CLAUDE.md` §10
  says AGENTS.md is retired; two independent commissions recommend it (this intake's
  wf-50111a08 and `docs/archive/2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md`);
  and the fleet has already ruled on it once — intake #25's W-9(a) proposed the same shim and the
  census records it *"reversed by ADR-53"*. Three positions, all coherent.
- **Leg 2 — reversal is asymmetric and expensive: PASSES.** Admitting it re-points the canonical
  instruction file across 8 consumer repos plus the hash-guarded floor replica; retracting later
  means re-authoring per-vendor files everywhere they landed. Declining costs one paragraph.

**ADR number is provisional.** Next free is **113** (highest on disk: ADR-112). If the seat
ratifies in a different order than §8 suggests, renumber — the numbers here are §8's order, not a
claim on the sequence.

```markdown
# ADR-113: The canonical instruction file is a content rule, not a filename rule — AGENTS.md admitted as a generated pointer layer

- **Status:** Proposed (authored 2026-08-19 by the N3 night lane as a ratification draft; **ratification is a separate operator act**)
- **Date:** 2026-08-19
- **Decided-by:** NOT YET RULED. This line is a placeholder and must name a real ruling before the status line moves to Accepted (ADR-94 permits the status-line edit in place; nothing else moves).
- **Decision tier:** Architecture (Path A — architect promotion from a ratified intake)
- **Amends:** ADR-53 (single-instruction-file ruling — the amendment is NAMED here rather than left as a silent second rule)
- **Related:** ADR-78 / ADR-93 (hash-guarded floor replica — the generation-plus-checksum mechanism this decision re-points rather than re-invents), ADR-98 (intake traceability), ADR-101 (Tier-1 tree seal — a new top-level file is a sanctioned-set question, see Consequences)
- **Intake:** #35 — `docs/intake/2026-08-17-tech-agent-instruction-layers-and-distillation.md`
- **Decommission:** `CLAUDE.md` §10's anti-pattern line *"Narrating or managing AGENTS.md — AGENTS.md is retired (ADR-53)"* is decommissioned by this ADR and must be re-stated to agree with it (R1's Done-when tests exactly this: `grep -c "AGENTS.md is retired" CLAUDE.md` reflects the ruling either way).
- **Source:** browser research artifact wf-50111a08 (2026-08-17), corroborated independently by `docs/archive/2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md`. Both are quoted in intake #35 §A and §C rather than re-derived here.

## Status note — read this before citing the ADR

This ADR is **Proposed**, not Accepted. Until the status line reads Accepted it records a decision
ruled worth writing down; it does not bind, and **no AGENTS.md file may be created on the strength
of it** — creating one before ratification is precisely the silent-build failure `CLAUDE.md` §10
exists to prevent.

## Context

ADR-53 retired AGENTS.md and made `CLAUDE.md` the single instruction file. That ruling solved a
real defect — two instruction files that can disagree — and it has held. What has changed since is
not the defect but the surrounding facts:

- `CLAUDE.md` is **at its declared ceiling**. Its own §12 v2.62 entry records the last edit landing
  *"exactly ON 200/200"*, forcing two history bullets into git to buy two lines. The budget is
  being relieved cosmetically, one condensation at a time.
- The fleet is **not single-vendor in practice**. `/codex-review` and the `codex` audit class are
  live, `AUDIT_CLASS_ENUM` carries `codex` and `fresh-eyes`, and the branch-prefix enum admits
  `claude/<slug>` cloud lanes.
- **Two independent commissions** reached the AGENTS.md recommendation, and a third position
  exists inside the corpus already: intake #25's W-9(a) proposed the same shim and was reversed.
- The interop mechanism this repo would need **already exists and is already trusted**: `CLAUDE.md`
  itself carries live `@`-imports (`@.claude/methodology-roster.md`,
  `@.claude/generated/commands-repo.md`, `@.claude/generated/recent-adrs.md`), and the
  hash-guarded floor (ADR-78/93, `floor-hash-verify`) is generation-plus-checksum — the exact
  pattern both memos recommend over symlinks.

The genuine question, which intake #35's open question 1 states and deliberately does not answer,
is what ADR-53 actually forbade: **AGENTS.md specifically, or two files that both carry content?**

## Decision

**ADR-53's single-instruction-file invariant is re-scoped as a CONTENT rule.** Exactly one file
may carry instruction *content*. A second file that carries no content of its own — a pointer, or
a generated artifact with a checksum guard — is not a second instruction file and never was the
thing ADR-53 refused.

On that reading, **AGENTS.md is admitted** as the portable canonical layer, under three conditions
that are the decision, not decoration:

1. **One content owner.** Whichever file carries content, the other is a pointer or a generated
   replica. Two files both carrying prose is refused exactly as ADR-53 refused it.
2. **The replica is guarded.** A generated instruction file carries a checksum sidecar and a
   regen-and-diff freshness gate, on the live `floor-hash-verify` / `claude-rosters-freshness`
   pattern. **No symlinks** — both memos independently reject them as Windows-hostile, and this
   repo independently reached generation-plus-checksum.
3. **Nothing is created before the budget work.** Admission authorizes the shape; it does not
   authorize a file. The line-budget win comes from the R2 classification pass (`[#RESERVED]`
   below), not from a rename, and a rename executed first would move a 200-line file to a new name
   and call it portability.

## Alternative, drafted so the architect can invert this by swapping one section

If the ruling is **REFUSAL**, replace the Decision section with:

> **AGENTS.md stays retired.** ADR-53's ruling is re-affirmed as a *filename* rule, on the ground
> that a pointer file is still a second file an agent can read, edit, or diverge, and that the
> portability the memos price is not yet owed at this fleet's live vendor count. The refusal is
> recorded **with its reason** so a third commission recommending AGENTS.md is answered by
> citation rather than re-litigated. `CLAUDE.md` §10's anti-pattern line stands and its
> `Decommission:` entry above is struck.

Both readings discharge R1. What R1 forbids is neither — it is leaving the question open while
memos keep arriving.

## Consequences

**Easier.** The budget question separates from the portability question, and each can be worked on
its own evidence. A future vendor is a generated file plus a gate, not a doctrine re-litigation.

**Harder.** ADR-101's Tier-1 seal is a **closed** set: `SANCTIONED_TIER1_FILES` does not contain
`AGENTS.md`, and `validate-hermetization` Rule A refuses an added unsanctioned top-level file.
Admission therefore owes an ADR-101 amendment as a separate, surfaced act — which is the seal
working as designed, not an obstruction.

**Honest limits.** This ADR **arms no gate**. Until the guard in condition 2 exists, the one-content-
owner rule is prose — the same class of unenforced invariant that intake #35's R2 exists to find.
It also does not measure anything: the memo's cited instruction-following degradation (IFScale,
68% adherence at 500 instructions) is the *basis* for preferring mechanisms over prose, not
evidence about this repo's own instruction file, which has never been measured.
```

### 3.3 Draft carrier row — exact `gen_task_tree` source form

Target file: `tasks/<id>-mechanize-not-prose-pass-over-the-always-on-inst.md` (the slug is
`gen_task_tree.slugify` applied to the title and truncated at 48 chars — do not hand-invent it;
`--emit-source` re-derives filenames from titles and a mistaken run re-slugs live ids, the [#473]
incident). Body line goes in `BACKLOG.md` under **[E5] Canonical-file integrity → [S14] Keep the
day-to-day docs right-sized and current**.

```yaml
---
id: "[#RESERVED]"
title: "Mechanize-not-prose pass over the always-on instruction surface"
status: open
priority: P2
size: M
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
serialize-group: claude-md
generates: BACKLOG.md
---

- [#RESERVED] [P2][M] **Mechanize-not-prose pass over the always-on instruction surface** — the `CLAUDE.md` 200-line budget is currently relieved COSMETICALLY, one history-bullet condensation at a time (§12 v2.59 and v2.62 both record a trim taken to buy 2 lines), which buys headroom without reducing what the file asserts. The structural relief is to classify every always-on line as **judgment** (stays prose) or **enforceable invariant** (owes a gate) and then move the second class out — the shape `CLAUDE.md` §5 rule 7 already asserts (*"No executable rules in this repo — those go in `~/.claude/` with `verify:` lines"*) but has never been applied line-by-line to the file that asserts it. The measured basis is the intake's, not invented here: instruction-following degrades under density (IFScale — 68% adherence at 500 instructions), so a crowded instruction file rots rather than merely costing tokens. Scope is the CLASSIFICATION and the gate-or-gap map, not the moves — a line that owes a gate names the gate or names its absence, and the removals are separate ruled acts. · Done when: a committed `docs/audits/<date>-technical-*` artifact lists every `CLAUDE.md` + `.claude/CLAUDE-FLOOR.md` line, classifies each as judgment or enforceable invariant, and names the existing gate or the gap for every line in the second class; the count of unclassified lines is **0** · refs docs/intake/2026-08-17-tech-agent-instruction-layers-and-distillation.md (R2), ADR-53, ADR-78, ADR-93, CLAUDE.md §5 rule 7 + §10 · kill-candidates: none — verified live, `instruction surface` / `always-on` / `line budget` each return 0 hits across `tasks/*.md`; no row covers instruction-surface classification · serialize-group: claude-md · source: intake #35 `docs/intake/2026-08-17-tech-agent-instruction-layers-and-distillation.md`, which carries the R2 rationale and the IFScale basis in full
```

**Why `serialize-group: claude-md`.** The row's subject is every line of a freshness-gated
collision file. A classification produced while another lane is rewriting `CLAUDE.md` is stale on
arrival, and §12 v2.57 / v2.60 record the standing batch practice of keeping lanes *out* of that
file for exactly this reason. The group is mutual exclusion on the read, not on a write.

### 3.4 Not born, and why — recorded so the omissions are visible

- **R3** (promptfoo rule-adherence harness) — accepted in principle, **not born**, on the intake's
  own kill-candidates line: *"propose FOLDING into that corpus rather than birthing a second
  one"*. The corpus is the one gating `[#491]` (open) and `[#492]` (deferred). Filing a second
  eval corpus alongside it is the duplication ADR-111 outcome (a) exists to prevent.
- **R4** (fleet-wide instruction-budget instrument) and **R5** (Codex 32 KiB truncation guard) —
  the intake rates both *Could* and states neither is load-bearing *"until the fleet actually runs
  multi-vendor"*. They stay proposed. **No trigger is owed** and none is invented: a *Could* with
  a manufactured peg reads as a commitment nobody made.

---

## 4 · Intake #36 — Repository autonomy, policy-as-code, and proving the gates are alive

`docs/intake/2026-08-17-tech-repository-autonomy-and-gate-liveness.md` · **VERDICT: CLEAR**

### 4.1 Ratification summary (one paragraph)

What is accepted is the intake's central inversion — at this maturity the dominant risk is no
longer a missing gate but **a gate that silently stopped working and now passes everything** — and
its force is again split. One genuine fork is accepted **as an ADR**: the intake's R9 sets the
memo's recommendation (a `PreToolUse` hook that rejects `--no-verify` / `SKIP=` outright) directly
against ADR-85 amendment 2026-08-03 §A2, which deliberately made `git push --no-verify` the *sole*
escape for the pre-push hard leg and made it non-silent via the `journal_spine_anchor` backstop;
the intake itself says the correct outcome *"may be a recorded REFUSAL"*, and a refusal recorded
nowhere is indistinguishable from an oversight. The same ADR carries R10's reversibility/autonomy-
rung doctrine, because R10's own Done-when demands *"an Accepted ADR"*. Everything else is
accepted **as rows**, of which exactly one is born: R6, the gate-liveness harness — the intake's
only *Must*, the memo's *"highest-leverage artifact in the entire report"*, and the one proposal
across all five memos that this repo's **own recorded history** most directly supports, with one
fixed dead-detector instance (`block_ff_push`, ADR-85 §A6) and one still-live documented hole
(`block_commit_on_main.current_branch()` fail-open, `CLAUDE.md` §9). R7 is **not born** and §4.4
shows why — its evaluation already closed and its trigger is already live.

### 4.2 Draft ADR — fork test and text

**Fork test (ADR-112), both legs stated, including where a leg is weak:**

- **Leg 1 — PASSES for both halves.** Bypass: block-it (memo) vs record-it (ADR-85) are both
  coherent and the corpus currently holds only one of them. Rungs: whether autonomy is rated at
  all, and against what, is unruled.
- **Leg 2 — PASSES for the rung half; WEAK for the bypass half, and this is stated rather than
  smoothed.** Re-rating every organ in `ecosystem/organ-index.md` after the fact is expensive;
  deleting a hook is not. The bypass half earns its ADR on a different ground — ADR-85 §A5's own
  recorded finding that *an organ that can be exhausted cannot carry teeth* is evidence that this
  decision class is not cheap to get wrong, and the escape is load-bearing across every lane.
  **If the seat judges leg 2 unmet for the bypass half, the correct alternative is a
  `protocols/STANDING_RULINGS.md` entry, not silence** — and §4.3's Decision item 1 transcribes
  cleanly into one.

```markdown
# ADR-114: Bypass is recorded, never blocked — and every automated action carries a reversibility class and an autonomy rung

- **Status:** Proposed (authored 2026-08-19 by the N3 night lane as a ratification draft; **ratification is a separate operator act**)
- **Date:** 2026-08-19
- **Decided-by:** NOT YET RULED — placeholder; must name a real ruling before the status line moves.
- **Decision tier:** Architecture (Path A — architect promotion from a ratified intake)
- **Related:** ADR-85 (session-end gate; amendment 2026-08-03 §A2 retired `/override` and named `git push --no-verify` the sole escape, §A5 the exhaustible-organ finding, §A6 the fail-open degradation), ADR-81 (organ definition-of-done), ADR-111 (finding triage — a negative-control failure is a finding, and this ADR classes it), ADR-101 (the organ index is generated ecosystem state)
- **Intake:** #36 — `docs/intake/2026-08-17-tech-repository-autonomy-and-gate-liveness.md`
- **Decommission:** none. `CLAUDE.md` §9's informal advisory-vs-blocking prose is NOT decommissioned by this ADR — it is left standing and deferred to the rung table only once the table exists and covers the same set (R10's own Done-when tests that coverage). Retiring prose before its replacement is live is how a claim stops being checkable.
- **Source:** browser research artifact wf-76d68c06 (2026-08-17), converted to intake #36 by lane R. The memo's escalation rule is quoted rather than paraphrased below because its precision is the point.

## Status note — read this before citing the ADR

**Proposed**, not Accepted. It binds nothing yet, and in particular **no organ may be promoted to
any autonomy rung on the strength of it** — the promotion rule below is the thing most likely to
be cited early, and citing it before ratification would grant exactly the autonomy it gates.

## Context

This repo's identity is its gate stack: roughly 43 audit checks, 20+ pre-commit / commit-msg /
pre-push hooks, a `PreToolUse` immutability guard, a `Stop` backpressure hook. Every one is trusted
to fire. **Almost none is tested for firing**, and the repo has witnessed the failure class twice
in its own records:

- `block_ff_push` printed *"degraded — allowing push"* and returned 0 — silently auto-allowing the
  exact push it exists to refuse (ADR-85 amendment 2026-08-03 §A6). **Fixed**; it now fails closed.
- `block_commit_on_main.current_branch()` *"returns `None` on ANY non-zero `git symbolic-ref`, so a
  genuine git failure silently ALLOWS the commit"* (`CLAUDE.md` §9). **Documented, live, untested**,
  and internally inconsistent with its own sibling `merge_in_progress()`, which raises by design.

A green `audit.py health` currently cannot distinguish *"43 checks ran and found nothing"* from
*"N checks silently no-opped"*. That is the whole problem.

The second question is sharper because the corpus already answers it, in the opposite direction
from the memo. The memo recommends a `PreToolUse` hook rejecting `--no-verify` and `SKIP=`. ADR-85
amendment 2026-08-03 §A2 retired `/override` and ruled that *"the sole escape for the pre-push hard
leg is `git push --no-verify`, made non-silent by the `journal_spine_anchor` audit backstop."*
Those cannot both stand.

## Decision

### 1. Bypass is RECORDED, never BLOCKED — the memo's R9 recommendation is REFUSED, with reason

ADR-85's escape stands. The repo's answer to bypass is *make it non-silent*; the memo's is *make it
impossible*; and on a client-side hook mesh that every `CLAUDE.md` §9 row already describes as
bypassable, blocking buys the **appearance** of teeth while removing the one sanctioned
pressure-release valve. An escape that is loud is an escape that is governed. An escape that is
absent is an escape that gets improvised.

What IS accepted from R9 is its other half: **an independent record**. For any merge range, whether
each commit was made with hooks armed must be answerable **without relying on the committer's
self-report** — which is the only evidence the batch-7a closure contract's *"zero `--no-verify` and
zero `SKIP=`"* item currently has. Until such a record exists, a batch packet claiming zero
bypasses is an **attestation** and must be labelled one.

### 2. Every automated action carries a reversibility class and an autonomy rung

Each automated action in `ecosystem/organ-index.md` is tagged **one-way door** (irreversible or
expensive to reverse) or **two-way door**, and assigned a rung on an **L0–L4** ladder from
surfacing through unattended auto-merge. The table and the index must cover the **same set** — no
organ unrated.

**Promotion rule:** *nothing promotes to L4 (unattended auto-merge) without a green liveness
harness and a merge-to-revert rate under a declared threshold.* Humans stay on one-way doors and on
security/architecture decisions; the reversible is what automates.

### 3. A negative control that passes is a Sev-1

Quoted from the memo, because the escalation level is the decision: *"if any negative control ever
passes, treat it as a Sev-1 — a detector that always passes is worse than none."* Under ADR-111
this is a finding like any other and is triaged like one; what this clause fixes is its **severity**,
not its route.

## Consequences

**Easier.** "The gates are fine" becomes a test result. A bypass claim becomes checkable or
honestly labelled. The advisory-vs-blocking distinction currently spread through `CLAUDE.md` §9
prose gains one table to defer to.

**Harder.** Rating every organ is real work, and it is only as good as `ecosystem/organ-index.md`
is complete — intake #36's open question 2 (can the table be derived mechanically from the index's
existing trigger × layer × failure-posture metadata, per `ARCHITECTURE.md` Ch2?) is **not answered
here** and should be settled before the table is hand-authored.

**Honest limits.** This ADR **arms no gate**. The L4 threshold is currently **unmeasurable** — no
merge-to-revert rate is recorded anywhere in this repo — so clause 2's promotion rule is, today, a
rule that no organ can satisfy. That is the intended posture (the memo's own non-goal forbids L4
promotion without the harness), but it should not be mistaken for a measured bar. And clause 1
refuses a mechanism without supplying its replacement: the independent record is authorized here
and **built by no row in this pack**, so the batch-packet attestation stays an attestation until
one lands.
```

### 4.3 Draft carrier row — exact `gen_task_tree` source form

Target file: `tasks/<id>-gate-liveness-harness-a-negative-control-per-cri.md`. Body line goes under
**[E2] Enforced governance → [S3] Turn advisory guards into enforced gates**.

```yaml
---
id: "[#RESERVED]"
title: "Gate-liveness harness — a negative control per critical gate"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: gates
generates: BACKLOG.md
---

- [#RESERVED] [P2][M] **Gate-liveness harness — a negative control per critical gate** — a green `audit.py health` today cannot distinguish *"43 checks ran and found nothing"* from *"N checks silently no-opped"*, and this repo has witnessed the second class twice in its own records: `block_ff_push` printed *"degraded — allowing push"* and returned 0 (fixed, ADR-85 amendment 2026-08-03 §A6), and `block_commit_on_main.current_branch()` still *"returns `None` on ANY non-zero `git symbolic-ref`, so a genuine git failure silently ALLOWS the commit"* (`CLAUDE.md` §9) — documented, live, untested, and inconsistent with its own sibling `merge_in_progress()`, which raises by design. The existing hook-stage trip-tests prove a stage **FIRES**; nothing proves a check **REFUSES**. Two legs, and leg 1 is a deliverable rather than a preamble: (1) a **declared critical-gate list** — nothing today says which of the ~43 checks and 20+ hooks are load-bearing versus informational, and the harness is only as good as that list; (2) a negative-control fixture per listed gate that deliberately violates it. Escalation is ruled, not left to judgement: a negative control that PASSES is a Sev-1, because a detector that always passes is worse than none. · Done when: `tests/test_gate_liveness.py` exists; the declared critical-gate list is committed; each listed gate has ≥1 fixture that deliberately violates it; the test FAILS if any gate ACCEPTS its own negative control; and the documented `block_commit_on_main.current_branch()` fail-open hole is one of the covered cases · refs docs/intake/2026-08-17-tech-repository-autonomy-and-gate-liveness.md (R6), ADR-85 amendment 2026-08-03 §A5/§A6, CLAUDE.md §9, ARCHITECTURE.md Ch2 organ map · kill-candidates: none — verified live, `negative control` / `gate-liveness` return 0 hits across `tasks/*.md`; the existing trip-tests assert a stage fires, not that a check refuses · serialize-group: gates · source: intake #36 `docs/intake/2026-08-17-tech-repository-autonomy-and-gate-liveness.md`, which carries the failure-class evidence and the Sev-1 escalation rule in full
```

### 4.4 R7 / mutation testing — NOT born, and the cross-check that says why

The intake proposes R7 (mutation testing over the audit-check implementation) and intake #37
proposes R17, flagging them as **the same build, to be filed once**. Neither is born here, because
the work is further along than either memo knew:

| what R7 asks for | live state, verified on this branch | residual |
|---|---|---|
| mutation testing adopted at all | **`[#502]` CLOSED** at batch-1 integration 2026-08-18 — decision 6 = **ADOPT** (Tier-L), transcribed verbatim into intake #27's adoption ledger row 8 | none |
| a run that executes | **live** — `.github/workflows/report-only-wall.yml` `mutation-pilot` job, `uv run --locked --with mutmut==3.7.0 mutmut run` | none |
| scope `scripts/audit_checks/` | **NO** — `[tool.mutmut]` in `pyproject.toml` scopes the pilot to `scripts/fleet_analytics.py` | **scope widening** |
| a committed floor, job FAILS on a surviving mutant in a highest-consequence check | **NO** — the ruling is *report-only ratchet*, baseline **1210 survivors**, direction **no-growth**; the job is explicitly *"recorded, never blocking"* | **promote report-only → blocking** |

Both residual items are **blocked on `[#533]`**, which is the row currently creating
`scripts/audit_checks/` — R7's target tree does not yet exist in the shape R7 names. And the
trigger is **already recorded in-repo**, so none is invented: intake #27 row 8 states *"survivor
triage **deferred**, trigger post-`[#533]` / next audit-py batch."*

**Triage verdict, ADR-111 outcome (b) DISCHARGED-in-part + a live deferral.** Filing R7/R17 now
would birth a row whose first act is to wait on `[#533]`, which is the open-set inflation the
filing-backpressure doctrine exists to prevent. The seat should confirm the intake-#27 trigger is
the one it wants to carry this; if it prefers a row, that row costs one birth and §1.3's ceiling
is already at five.

---

## 5 · Intake #37 — Machine-verifiable Done-when: making acceptance criteria executable

`docs/intake/2026-08-17-tech-machine-verifiable-done-when.md` · **VERDICT: CLEAR — sequenced**

### 5.1 Ratification summary (one paragraph)

What is accepted is the intake as the requirements authority on **acceptance evidence**, and its
force is split with a hard ordering constraint the seat must not invert. The intake's own *Must*
(R12 — `done_when` as a required, schema-validated field) is **blocked on a ruling it deliberately
declines to make**: `CLAUDE.md` §5 rule 7 says *"No executable rules in this repo — those go in
`~/.claude/` with `verify:` lines"*, the memo says *"store that predicate in the task file
itself"*, and the intake states flatly that *"these cannot both stand as written"*. That is a
genuine fork and it is accepted **as an ADR**, which is the act that unblocks the row; the row is
then accepted and born, and it must not land first. The rest is accepted **as rows** and none of
them is born: R13 (held-out verifier) and R14 (predicate smoke test) are *Should* and stay
proposed behind R12, which every one of them presupposes — R13 and R14 both operate on a
`done_when` schema that does not exist yet; R15 and R16 are *Could*; and **R17 is not born at all
and must not be**, because the intake flags it as deliberately the same build as #36's R7, whose
live state §4.4 already settles.

### 5.2 Draft ADR — fork test and text

> **INTEGRATION NOTE — added 2026-08-26 by the batch-1 integrator, architect-ruled; an attributed in-file amendment marker, not an edit to this pack's content.** ADR id **115** is now taken on disk by `docs/decisions/ADR-115-agents-md-portable-instruction-layer.md`, landed by lane G in this batch — **disk allocation wins**, and this held draft renumbers at landing. No ADR content is authored, amended or ratified here: the ADR-101 `prompts/` amendment and ADR-115 acceptance belong to a separate post-integration governance session.

**Fork test (ADR-112), both legs stated:**

- **Leg 1 — PASSES, on the intake's own words.** It offers the reconciliation *"as a reading and
  not as a ruling"* and says a technical-architect ruling is required before R12 is built. A
  reading that its own author declines to assert is the definition of a live fork.
- **Leg 2 — PASSES.** The field becomes required across 188 open rows and gains a `validate_backlog`
  leg at pre-commit. Retracting means unwinding a schema across the corpus and removing a gate leg
  that other rows (R13, R14) will by then be built on top of.

```markdown
# ADR-115: `done_when` predicates are acceptance evidence, not agent rules — CLAUDE.md §5 rule 7 does not reach them

- **Status:** Proposed (authored 2026-08-19 by the N3 night lane as a ratification draft; **ratification is a separate operator act**)
- **Date:** 2026-08-19
- **Decided-by:** NOT YET RULED — placeholder; must name a real ruling before the status line moves.
- **Decision tier:** Architecture (Path A — architect promotion from a ratified intake)
- **Clarifies:** `CLAUDE.md` §5 rule 7 + §10 (the "no executable rules in this repo" anti-pattern). This is a SCOPE clarification, not an amendment — the rule is unchanged in what it forbids; what changes is that the boundary is now stated instead of assumed.
- **Related:** ADR-107 (`tasks/` is the source of truth, `BACKLOG.md` is generated — the fact that decides WHERE the schema lands), ADR-66 (story-map schema), ADR-110 (frozen lane contracts — what R13's held-out verifier extends), ADR-98 §3 (acceptance criteria copy verbatim from intake to row — the seam this schema makes mechanical rather than clerical)
- **Intake:** #37 — `docs/intake/2026-08-17-tech-machine-verifiable-done-when.md`
- **Decommission:** none
- **Source:** browser research artifact wf-bfb9405b (2026-08-17), converted to intake #37 by lane R.

## Status note — read this before citing the ADR

**Proposed**, not Accepted. The `done_when` schema row is blocked on this ADR reaching Accepted;
building the schema against a Proposed ADR would be the enforcement-ahead-of-doctrine shape
`[#166]` exists to detect.

## Context

The repo already ran the campaign this intake is about — 29 rows converted from prose to testable
Done-when, roughly half remaining — and nothing distinguishes a *checkable* criterion from
better-written prose. A `Done when:` clause is text. No schema requires it to name a command that
exits zero.

The exposure this creates is measured rather than anecdotal, and it is this repo's exposure
specifically: it dispatches parallel lanes against frozen contracts and merges on the strength of
their reported greens. SpecBench's validation-vs-held-out "Reward Hacking Gap" and EvilGenie's
finding of models deleting or modifying test files both describe agents that **go green while
wrong** — not agents that fail loudly.

The blocker is a genuine collision of two live texts. `CLAUDE.md` §5 rule 7: *"**No executable
rules in this repo** — those go in `~/.claude/` with `verify:` lines"*, restated as an anti-pattern
in §10. The memo: *"store that predicate in the task file itself."*

## Decision

### 1. Rule 7 is scoped to agent-behavioural rules; it does not reach acceptance evidence

Rule 7 governs **rules that tell an agent how to behave** — those live in `~/.claude/` with
`verify:` lines, and this repo does not carry them. A `done_when` predicate is **evidence that a
work item is finished**: a different genre, addressed to a validator rather than to an agent,
which merely borrowed the same keyword. Rule 7's prohibition is unchanged; it simply never reached
this genre, and saying so is what stops the collision from being re-discovered every time someone
reads §5.

### 2. The two uses of the keyword are separated, because a shared keyword is how the collision happened

The task-side predicate key is **`check:`**, not `verify:`. `~/.claude/` rules keep `verify:`.
The specific token is the architect's to pick and is trivially swappable — what is decided is that
**they must not share one**, which is the intake's own recommendation (*"the two uses of `verify:`
should be named differently to stop them colliding"*).

### 3. The schema lands in `tasks/`, not in `BACKLOG.md` row bodies

This answers intake #37's open question 3, and it answers it from repo facts rather than
preference. Under ADR-107, `tasks/` is the source of truth and `BACKLOG.md` is generated
(`gen_task_tree.py --emit-source`), so a structured block in a row body would be **generated
output pretending to be source**. It would also fight the live `backlog-accretion` row-length
ceiling, which the batch-1 integration drained to zero loci — putting a YAML block inside each row
body would re-inflate the surface that campaign just cleared.

### 4. The gate is PROSPECTIVE

`validate_backlog` gates rows that are **added or changed** after the schema lands; the 188 existing
open rows are grandfathered and converted as they are touched. This is the `validate-hermetization`
precedent, which intake #37 invokes by name, and it is the difference between a schema that can
land next week and one that blocks every commit until a 188-row conversion finishes.

**This is a departure from R12's literal text**, which reads *"validate_backlog FAILs when an open
row lacks a done_when block"* — as written, a hard gate on every open row. The departure is
recorded here, in the decision, rather than silently applied when the row is written, so the row's
Done-when can stay verbatim per ADR-98 §3 and inherit the scoping by citation.

## Consequences

**Easier.** Judgment-bound work becomes visible as such (`human_verdict_required: true` with a
`rationale`) rather than silently green. The intake→row acceptance-criteria seam (ADR-98 §3,
"copy VERBATIM") becomes mechanical instead of clerical.

**Harder, and this is the real cost.** `gen_task_tree --check` currently verifies *"every task
file's frontmatter matches its own body"* — frontmatter is **derived from the body**. A structured
`done_when` block is the first field with no body counterpart, so it needs generator work before it
needs validator work. Anyone sizing this off the validator alone will size it wrong.

**Honest limits.** This ADR **arms no gate** and converts no row. It also does not answer intake
#37's open question 2 — *what is the actual current conversion coverage?* The memo's "29 converted,
~half remaining" is a stale snapshot and **no live number was measured for this pack either**;
quoting it as current would be the drift this repo files findings about.
```

### 5.3 Draft carrier row — exact `gen_task_tree` source form

Target file: `tasks/<id>-done-when-as-a-required-schema-validated-field-o.md`. Body line goes under
**[E2] Enforced governance → [S4] Extend structural validation to more governance artifacts**.
**Do not land this row before ADR-115 reads Accepted** — see §5.1.

```yaml
---
id: "[#RESERVED]"
title: "done_when as a required, schema-validated field on every open row"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#RESERVED] [P2][M] **`done_when` as a required, schema-validated field on every open row** — a `Done when:` clause is text today, and nothing distinguishes a criterion that is *checkable* from one that is merely better-written prose; the repo's own half-finished prose→testable conversion (29 rows converted, ~half remaining at the last snapshot) has no definition of success, so it cannot tell conversion from **weakening a criterion to be satisfiable**, which is goodharting. The schema is the intake's, quoted not re-derived: per entry an `id`, an EARS-style `statement`, a `kind` (`command|test|metric|file|human`), a non-empty predicate for every non-`human` kind, and `asserts: true` so a test-kind predicate with no assertion is refused. Scoping is ruled by ADR-115 and inherited rather than re-decided here: the block lands in `tasks/` (the ADR-107 source of truth), not in `BACKLOG.md` row bodies (generated output, and the `backlog-accretion` ceiling the batch-1 campaign just drained to zero loci); the predicate key is `check:` so it stops colliding with `~/.claude/`'s agent-rule `verify:`; and the gate is **PROSPECTIVE** — added/changed rows only, the 188 existing open rows grandfathered on the `validate-hermetization` precedent. **Sequencing is hard:** this row does not start until ADR-115 reads Accepted, and its first real cost is in `gen_task_tree`, not `validate_backlog` — `--check` asserts frontmatter matches its own body, so a structured block with no body counterpart needs generator work first. · Done when: `validate_backlog` FAILs when an open row lacks a `done_when` block carrying ≥1 non-human entry with a non-empty predicate, OR `human_verdict_required: true` with a `rationale`; a hand-crafted violating fixture is REFUSED in the test suite · refs docs/intake/2026-08-17-tech-machine-verifiable-done-when.md (R12), ADR-107, ADR-66, ADR-98 §3, scripts/validate_backlog.py, scripts/gen_task_tree.py · depends-on: none — ADR-115 is a doctrine precondition, not a task edge; recorded in prose because `depends-on` takes live task ids only and a dangling id hard-FAILs `validate_backlog` · kill-candidates: supersedes the informal prose `Done when:` convention currently carried in BACKLOG rows — the prose form is accepted only under `human_verdict_required`, never as the default · serialize-group: audit-py · source: intake #37 `docs/intake/2026-08-17-tech-machine-verifiable-done-when.md`, which carries the full schema and the reward-hacking evidence
```

### 5.4 Not born, and why

- **R13** (held-out verifier in the lane contract) and **R14** (predicate smoke test) — both
  *Should*, both **presuppose R12's schema**. R13 is the countermeasure the memo rates highest
  (*"The decisive mitigation is a held-out check the agent never sees"*) and it is cheap here
  because ADR-110 frozen lane contracts already exist — but it verifies predicates that do not yet
  have a form. Un-parked by R12's row closing; that is a live, in-repo trigger and needs no date.
- **R15** (hedge-word gate) and **R16** (test-file edit detection) — *Could*. R16 may already be
  discharged for integrators by the batch-2 condition-3 review rule, leaving only lanes uncovered;
  the intake's own open question 4 asks exactly this and **it is not answered here**.
- **R17** (mutation testing) — **must not be born.** The intake flags it as deliberately the same
  build as #36's R7 (*"do not birth both"*). §4.4 records the live state and the existing trigger.

---

## 6 · Intake #38 — Multi-repo config standardization and fleet conformance at N=8

`docs/intake/2026-08-17-tech-fleet-config-standardization.md` · **VERDICT: CLEAR**

### 6.1 Ratification summary (one paragraph)

What is accepted is the intake as the **fleet-conformance requirements authority**, and its force
is **rows only** — this is the one intake in the arc that rules nothing, because its own §C says
so: *"SUPERSEDES nothing"*, and its main contribution is a hard **negative** result that endorses
what the hub already built. Python tooling cannot inherit config from an installed package —
Ruff's `extend`, mypy, pytest and coverage all resolve a *file path*, never a package name — so
"one source of truth" for Python config means **distributing a file**, which is precisely what
`deploy/manifest-v*.yaml` carried replicas and the hash-guarded floor (ADR-78/93) already do. The
practical value of ratifying it is therefore not new doctrine but **a carrier for the fleet's
oldest ACCEPTED-unfiled debt**: intake #25's W-2 (kernel/lab check tiering plus
`dev-knowledge-kernel` as an installable package) was ACCEPTED on 2026-08-05 and is **still at
zero carrier rows fourteen days later**. The census recorded the carrier test as
*"`dev-knowledge-kernel` → 0 hits tree-wide"*; that phrasing is looser than the test it ran, which
its own header scopes to *"grep over `tasks/*.md`"*. **Re-run on this branch, precisely: 0 hits
across `tasks/*.md` — the carrier test holds — and 4 hits tree-wide, all of them prose records
(intake #25, the orphan census, the north-star inventory, the 08-17 supplement) and not one of
them a carrier.** That row is born here, mandatorily. The checker (R18) is the intake's own *Must* and is **not born**;
§6.4 says what un-parks it and why it lost the coin-flip against the ledger rather than against
its own merit.

### 6.2 No ADR — rows only, with the reason

Applying the ADR-112 fork test to every candidate decision in the intake:

| candidate | leg 1 (reasonable person could differ) | leg 2 (reversal asymmetric/expensive) | verdict |
|---|---|---|---|
| kernel/lab split + kernel as a package (W-2) | **already ruled** — intake #25 ACCEPTED 2026-08-05 with `decided-by` recorded | n/a — not re-opened | **no new ADR**; ratifying #38 files it, it does not re-decide it |
| Python config by file not package | **fails** — a hard technical constraint, not a choice | n/a | no ADR; a finding, recorded |
| stay polyrepo, not monorepo | **fails** — matches current shape, intake lists it as a non-goal | n/a | no ADR |
| should `disposition-register.yaml` gain `expiresOn`? (R19) | **PASSES** — the intake calls it *"an operator call"*, both readings coherent | **FAILS** — adding or dropping a register field is cheap and local | **register ruling, not an ADR** — `protocols/STANDING_RULINGS.md`, the ADR-112/L-10 precedent |
| adopt Copier / Repolinter / OPA at N=8 | **fails** — the intake rules all three out as non-goals (Repolinter archived read-only 2026-02-06) | n/a | no ADR |

**So: no ADR.** Exactly one candidate passes leg 1, and it fails leg 2 — which is the case
ADR-112 exists to route away from an ADR, and the register is where a cheap-to-reverse standing
rule belongs. The seat may still want that one-line register entry; it is not a birth and costs
nothing against §1.3.

### 6.3 MANDATORY draft carrier row — the kernel debt

**Provenance, stated precisely so it stays checkable.** The *decision* is intake **#25**'s W-2,
ACCEPTED 2026-08-05. Intake **#38** is where it lands a **carrier**, because #38 is the
fleet-conformance authority and two of its own proposals ride the same vehicle: R22 wants the
toolchain pin across the fleet, and R18 wants the checker's rule set derived from the live deploy
manifest. The row's `source:` cites **both**, so a later reader can tell who decided from who
carried.

Target file: `tasks/<id>-kernel-lab-check-tiering-dev-knowledge-kernel-as.md`. Body line goes under
**[E6] Cross-repo universalization → [S15] Converge every child repo on the universal baseline** —
its siblings there are `[#332]` (fleet dependency-version parity), `[#334]` (ruff hook-id
migration) and `[#351]` (fleet Python upgrade), each of which is waiting on exactly the pin this
row would define.

```yaml
---
id: "[#RESERVED]"
title: "Kernel/lab check tiering + dev-knowledge-kernel as an installable package"
status: open
priority: P2
size: L
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#RESERVED] [P2][L] **Kernel/lab check tiering + `dev-knowledge-kernel` as an installable package** — the fleet's **oldest ACCEPTED-unfiled debt**: intake #25's W-2 was ACCEPTED 2026-08-05 and has carried **zero rows for fourteen days**, verified by the census's own carrier test and re-run on filing (`dev-knowledge-kernel` → **0 hits across `tasks/*.md`**; the 4 tree-wide hits are prose records, not carriers). Two coupled legs, quoted from the accepted decision rather than re-derived: (1) **tier every `ALL_CHECKS` member** — `kernel` (portable, consumer-grade: git discipline, JOURNAL anchor, backlog schema, review-artifact coverage — target 8–12) vs `hub` (methodology-lab: `doc_rot`, `silent_rule_ratchet`, parity internals); (2) **the kernel ships as an installable package from the hub**, a git-tag-pinned dependency (`uv add dev-knowledge-kernel @ git+<hub>@vX.Y`), so consumers pull versioned CODE **by reference** rather than by copy. Python unification rides the same vehicle: the kernel package pins `requires-python` and uv `required-version` and exposes a shared ruff config consumers `extend`, so **one version bump = fleet-wide toolchain move** — which is the mechanism `[#332]`, `[#334]` and `[#351]` are each separately waiting on. Intake #38 supplies the constraint that shapes it and saves the wasted refactor: Python tooling **cannot** inherit config from an installed package (Ruff `extend`, mypy, pytest and coverage resolve a file path, never a package name), so the *config* is distributed as files while the *code* is imported — do not attempt a config package. W-2 is the design keystone and **precedes** W-1/W-3/W-4: you template and package what the tiering names. · Done when: every `ALL_CHECKS` member carries a `kernel`/`hub` tier; `dev-knowledge-kernel` is installable from the hub at a git tag and at least one consumer resolves it as a pinned dependency; and the package pins `requires-python` + uv `required-version` and exposes the shared ruff config a consumer `extend`s · refs docs/intake/2026-08-05-func-simplification-distribution-wave.md (W-2, ACCEPTED 2026-08-05), docs/intake/2026-08-17-tech-fleet-config-standardization.md (R22, and the file-not-package finding), docs/audits/2026-08-17-census-nb7-orphan-census.md item 17, ADR-78, ADR-93, #332, #334, #351 · kill-candidates: none — verified live on filing: `kernel` / `consumer-grade` / `ALL_CHECKS tier` each return 0 hits across `tasks/*.md`, and `[#332]`/`[#334]`/`[#351]` are **consumers** of the pin this row defines, not owners of it · serialize-group: audit-py · serialize-group: environment · source: intake #25 `docs/intake/2026-08-05-func-simplification-distribution-wave.md` W-2 (the ACCEPTED decision) carried under intake #38 `docs/intake/2026-08-17-tech-fleet-config-standardization.md` (the fleet-conformance authority that supplies its constraint)
```

**Three notes the seat should not have to re-derive:**

- **Two `serialize-group` clauses are deliberate and legal.** `validate_backlog` states a task *"may
  carry ≥1 such clause — one per shared surface it collides on (multi-surface collision, #167) —
  and is placed in EVERY named group."* This row mutates `scripts/` check registration (`audit-py`)
  **and** `pyproject.toml` packaging/toolchain (`environment`); declaring one would hide a real
  collision. Frontmatter carries a single key by convention, so the second clause lives in the body
  where the parser reads it — check the round-trip on filing.
- **Size L trips an advisory WARN, by design.** `check_backlog_filing.py` emits the ADR-98
  intake-id WARN on a new L-sized new-feature epic (#279). The row cites its intake-ids explicitly
  in `source:`, which is what that WARN asks for.
- **This row is `[#541]`-adjacent but not overlapping.** `[#541]` owns the *scale-out substrate*
  decision. Different subject; no discharge owed either way.

### 6.4 R18 (the conformance scorecard) — not born, and what un-parks it

R18 is intake #38's own *Must* (*"you cannot fix drift you can't see"*) and it lost to the ledger,
not to its merit. Recording that plainly so nobody re-derives it as an oversight:

- **The ceiling is five births** (§1.3) and the kernel row is mandatory. R18 was the sixth.
- **It has an unresolved design question that filing would not answer.** Intake #38's open question
  1 asks whether `fleet.yml` is a new file at all, or whether `ecosystem/organ-registry.yaml` /
  `ecosystem/deployed-versions.yaml` already carry the consumer roster the checker needs —
  *"birthing a fourth `ecosystem/*.yaml` when a third already lists the fleet would be exactly the
  proliferation ADR-101 seals against."* That is a cheap question to settle and an expensive one to
  get wrong after a file exists.
- **Un-parked by:** the kernel row's leg 1 landing (the tiering is the rule set the checker would
  assert), **or** the next window with ≥1 birth of headroom — whichever is first. Both are live
  conditions, neither is a date, and none is invented.

### 6.5 Fallback — the drafted deferral, if the ledger squeezes the kernel row

Per the dispatch: never silence. If the seat cannot spend a birth on the kernel row, intake #38
flips **ACCEPTED with `disposition: deferred`** and a live, dated trigger, so the debt is a
recorded park rather than a fourteenth-and-fifteenth day of nothing. Frontmatter delta:

```yaml
# docs/intake/2026-08-17-tech-fleet-config-standardization.md — DEFERRAL FALLBACK ONLY
# Use this ONLY if the kernel carrier row in 6.3 is not born. If it is born,
# disposition is `active` and this block is not written.
status: ACCEPTED
decided-by: "<the ruling that accepted it — REQUIRED at ACCEPTED, README §3; this pack cannot supply it>"
disposition: deferred
trigger: "the kernel/lab tiering row is born and carries W-2, or 2026-09-19 — whichever is first. Live leg: intake #25's W-2 has been ACCEPTED-with-zero-carriers since 2026-08-05 and the census carrier test (`dev-knowledge-kernel` → 0 hits tree-wide) is the standing measurement. Dated leg: 2026-09-19 is one month from this ratification; if the row still has no carrier then, the debt is 45 days old and the deferral itself is the finding."
```

**The schema has no combined live-and-dated form** — `docs/intake/README.md` §3 offers `trigger:`
*or* `review-date:` as alternatives, and the live precedent is a bare `trigger: "#328 build"`. The
dispatch requires the trigger be both live **and** dated, so the date is carried **inside** the
trigger string rather than by adding an off-schema second key. If the seat prefers two keys, that
is an intake-README §3 amendment and should be surfaced as one, not slipped in.

**Deferral is strictly worse than the row here, and the pack says so rather than presenting them as
equals.** A deferral parks a debt that is already the oldest in the corpus; a second park with a
new clock is how fourteen days becomes forty-five. Spend the birth.

---

## 7 · Intake #39 — Off-machine agent fleet substrate (the re-priced, verified-August-2026 plan)

`docs/intake/2026-08-17-tech-off-machine-agent-substrate.md` · **VERDICT: CLEAR**

### 7.1 Ratification summary (one paragraph)

What is accepted is the intake as a **currency correction on a standing authority**, and its force
is **rows only**. It is the only one of the five memos that audits a prior in-repo artifact and
finds part of it stale: intake **#32** is **ACCEPTED**, so it is a live authority, and it carries a
Hetzner price basis that two 2026 repricings have invalidated — the dedicated CCX line rose
2.13×–2.73× while the CX shared line rose only ~1.3×–1.4×, so the recommendation flips from CCX to
CX. Everything else in the memo **confirms** what this repo already believes (three planes,
worktree-per-lane, branch-per-lane, laptop-as-integrator, and the hourly ÷ ~624 monthly-cap
crossover model — the memo re-verifies CX53 at €0.0473/hr ÷ €29.49 ≈ 623 hours against the prior
~624). Ratification therefore costs **one small row** for the correction, because the anti-orphan
rule is already satisfied by an **existing open carrier**: `[#554]`'s `source:` line literally
reads *"intake #39"*, which is ADR-111 outcome **(a) OWNED** — attach the evidence, birth nothing.
§7.3 is the cross-check that proves that carrier is real and shows exactly where its coverage
stops.

### 7.2 No ADR — rows only, with the reason

| candidate | leg 1 | leg 2 | verdict |
|---|---|---|---|
| CX supersedes CCX as the spec | **fails** — a price fact, verified against two dated repricings; not a choice | n/a | no ADR — a correction, carried by a row |
| do not buy a GPU | **fails** — the intake rules it a non-goal; the memo's verdict is unambiguous and flips only above ~$500–1,000/mo sustained token spend | the decision is *not to buy*, i.e. the reversible direction | no ADR |
| which substrate to actually rent | **passes** | passes | **already owned by `[#541]`** — open, its Done-when is exactly *"a ruling records the chosen scale-out substrate with its crossover rule and time-to-deploy, or records the decision deferred with a dated peg"*. Not this intake's to re-decide. |
| open question 1 — which channel amends an ACCEPTED intake? | passes | **fails** | **DISCHARGED by live precedent — see below** |

**Open question 1 is answered by the repo, not by a ruling.** The intake asks whether amending an
ACCEPTED intake needs an ADR, a new intake, or an in-file amendment marker. Intake **#25** already
did it, twice: its `decided-by` field carries an **ERRATUM 2026-08-09** and an **ERRATUM E-2
2026-08-11**, each correcting a premise in place, each explicitly scoped (*"this corrects the
premise and its outcome only; no other clause, status, conclusion or open question changes, and
zero backlog rows are born"*), with zero body edits. That is the channel, it is live, and it needs
no new decision. Two consequences: R24 is an ordinary row rather than a governance question, **and**
§7.5's fallback becomes available if the ledger squeezes.

**Currency note.** The intake's dated external deadline — Oracle enforcing reduced Always Free
limits, *"18 August 2026 — tomorrow relative to this doc"* — is **now in the past**. Nothing is
owed (the intake lists Oracle Always Free as a non-goal and names it a trap), but a reader
encountering "tomorrow" in a doc dated 2026-08-17 should know it resolved on 2026-08-18 without
action from this fleet.

### 7.3 CROSS-CHECK — what `[#554]` already carries (the anti-duplicate test)

`[#554]` is **open** and is intake #39's carrier. Its own row already names its source as intake
#39, so the OWNED edge exists in the tree today and does not need to be created. Coverage, proposal
by proposal:

| #39 proposal | carried by `[#554]`? | evidence |
|---|---|---|
| **R25** — `.devcontainer` + `provision.sh` asserting the three traps closed | **YES — fully.** The row's four legs *are* R25: a pinned-`uv` assert, `git fetch --unshallow`, deterministic `pre-commit install` for all three hook types, and an env gate that refuses to start on a half-provisioned environment | row body; lane contract §1.3 enumerates them as L1–L4 |
| **R27** — prove ONE lane green off-machine at zero cost | **YES.** This is the row's Done-when clause (a) — *"one lane runs green (`audit.py health` **and** `pytest -m 'not slow'`) on the Codespaces free tier"* — tracked as **D1** | row Done-when; contract §1.3 |
| the VPS-portability half | **YES.** Done-when clause (b) — *"the identical script is runnable via `devcontainer up` on a VPS"* — tracked as **D2** | row Done-when |
| **R26** — env-flag gate so a single-repo lane is clean | **NO — and deliberately so.** Lane C's contract §1.4 resolved the row-vs-intake divergence in the row's favour and recorded R26 as *"an open dependency rather than silently folded in"*; it would require editing `scripts/audit.py`, outside that contract | contract §1.4 |
| **R24** — re-base the compute plan onto CX | **NO.** Verified live on this branch: `hetzner` / `CCX` / `price basis` each return **0 hits** across `tasks/*.md` | §7.4 births it |
| **R28** — plan lane width against the rate limit | **NO.** Not born: the intake's own kill-candidates line proposes *"one more line in that section, not a new gate"*, extending the existing ex-ante process-lane cap in the batch manifest (PLAYBOOK Ch8) | intake R28 |
| **R29** — off-machine gates-ran attestation | **NO.** Not born, and must not be: the intake flags it as overlapping #36's R9 and asks for *"ONE attestation record serving both"*. ADR-114 Decision 1 authorizes exactly that record — it belongs there | intake R29; §4.2 |

**`[#554]` stays open on its D1/D2 proof only, and nothing here re-opens it.** The batch-1
integrator packet §4 is explicit: *"The remaining items are D1 and D2 — the proof, and only the
proof. Everything else lane C owed (legs L1–L4) landed."* The row was left open rather than forced
because lane C found **no boot channel** — its `gh` token lacks the `codespace` scope — and took
the contract's authorized fork of reporting D1/D2 open rather than fabricating a boot log.

**Therefore: no row is drafted for R25 or R27.** Filing one would re-file work that has landed
except for a proof, which is the duplicate-carrier failure this cross-check was asked to prevent.

### 7.4 Draft carrier row — exact `gen_task_tree` source form

Target file: `tasks/<id>-re-base-the-compute-plan-onto-the-hetzner-cx-sha.md`. Body line goes under
**[E7] Tooling & evaluation → [S19] Decide the undecided artifact/tool models** — the story that
already holds `[#541]` (substrate decision) and `[#387]` (rewrite a stale intake before anything
ingests it), which is the same shape as this row.

```yaml
---
id: "[#RESERVED]"
title: "Re-base the compute plan onto the Hetzner CX shared line"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
serialize-group: architecture
generates: BACKLOG.md
---

- [#RESERVED] [P2][S] **Re-base the compute plan onto the Hetzner CX shared line** — intake **#32 is ACCEPTED**, so it is a standing authority *"live and visible"* (`docs/intake/README.md` §5), and it carries a price basis that two 2026 repricings (Apr 1, Jun 15) have invalidated: the dedicated **CCX** line it leaned toward rose **2.13×–2.73×** while the **CX** shared line rose only **~1.3×–1.4×**, so the recommendation flips from CCX to CX. This is a currency correction, not a re-plan — the *architecture* (three planes, worktree-per-lane, branch-per-lane, laptop-as-integrator) and the **hourly ÷ ~624 monthly-cap crossover model are CONFIRMED and survive intact** (CX53 verifies at €0.0473/hr ÷ €29.49 ≈ 623 against the prior ~624); only the per-instance figures fall. Left uncorrected it is the highest-cost error available here — acting on #32 as written budgets roughly 3× the real spend — and correcting it costs nothing. The amendment channel is settled by live precedent, not by a new ruling: intake #25's `decided-by` carries **ERRATUM 2026-08-09** and **ERRATUM E-2 2026-08-11**, each correcting a premise in place, explicitly scoped, zero body edits. Scope is the correction only; **which substrate to rent is `[#541]`'s question and is not answered here.** · Done when: intake #32 carries an amendment or superseded-by pointer naming intake #39, and no live doc cites a CCX price as current — a grep for the stale figures returns only historical or quoted contexts · refs docs/intake/2026-08-17-tech-off-machine-agent-substrate.md (R24), docs/intake/2026-08-09-tech-compute-placement-and-remote-execution.md (#32, ACCEPTED), docs/archive/2026-08-09-research-compute-placement-wf-1dc18e42.md, docs/intake/2026-08-05-func-simplification-distribution-wave.md (the ERRATUM precedent), #541, #554 · kill-candidates: none — this AMENDS an ACCEPTED intake rather than adding scope; if the triage rules the amendment unnecessary the row dies with a recorded reason, and `hetzner`/`CCX`/`price basis` each return 0 hits across `tasks/*.md` today · serialize-group: architecture · source: intake #39 `docs/intake/2026-08-17-tech-off-machine-agent-substrate.md`, which carries the repricing evidence and the crossover re-verification in full
```

### 7.5 Ledger lever — how to ratify #39 for ZERO births if §1.3 squeezes

Because §7.2 settles the amendment channel, **R24 can be discharged by the ratification act
itself**: write the erratum into intake #32's `decided-by` at the same time #39 flips, exactly as
intake #25 did twice. `[#554]` then remains #39's carrier and the anti-orphan rule is satisfied
with **zero births**.

**Recommended anyway: birth the row.** The erratum-in-the-act path does the correction but leaves
the *sweep* — the Done-when's second clause, that no live doc cites a CCX price as current — with
no owner, and a half-done correction on a standing authority is the shape R24 exists to fix. Take
this lever only if the kernel row would otherwise be squeezed; between the two, the kernel row wins.

---

## 8 · The five status flips — frontmatter deltas

`decided-by` is **REQUIRED at ACCEPTED** (`docs/intake/README.md` §3) and this lane cannot supply
it; every block below carries a placeholder that must be replaced with a real ruling reference
before the flip is committed. `disposition: active` is correct for all five **because all five get
a carrier row** — swap #38 to the §6.5 deferral block only if its kernel row is not born.

```yaml
# ALL FIVE — docs/intake/2026-08-17-tech-*.md
status: ACCEPTED                                   # was: DRAFT
decided-by: "<the ruling that accepted it — REQUIRED at ACCEPTED>"
disposition: active
```

**One more line moves in each of the five, and it is easy to miss.** Every one of these intakes
carries, verbatim:

```yaml
consumers: the technical-architect triage; no ADR and no backlog row has been born from this doc
```

That clause is **false the moment the flip lands**. `consumers` is an optional descriptive key
legal at any status, so it is not schema-gated and nothing will catch it — which is exactly why it
gets named here. Update each to name what was actually born (the ADR id where one exists, the row
id, or "carrier `[#554]`" for #39).

**Then run BOTH intake generators, in this order:**

```
python scripts/gen_intake_index.py --write     # the status-grouped Contents block in docs/intake/README.md
python scripts/gen_intake_tree.py  --write     # docs/intake/manifest.json (derived from README.md, so it must run SECOND)
```

**Only the first is hook-gated.** `intake-index-freshness` guards `gen_intake_index`; there is **no
pre-commit hook for `gen_intake_tree`**, and its manifest keys off `README.md`'s sha256 — which the
first generator just changed. A flip that forgets the second leaves `docs/intake/manifest.json`
stale with nothing to catch it. Both were verified clean on this branch before this pack was
written (`272 node(s), 16780 README.md byte(s)`), so any drift after tomorrow is the flip's.

**And for every born row:** edit `tasks/`, never `BACKLOG.md` — then
`python scripts/gen_task_tree.py --emit-source`. Each birth commit needs a `kill-candidates:` line
in its **commit message** or `backlog-filing-backpressure` BLOCKS it; every drafted row above
carries the text to use.

---

## 9 · Suggested execution order

Ordered so the un-cuttable thing lands first and the most contested thing cannot block the rest.

| # | act | births | why here |
|---|---|---|---|
| 1 | **#38** flip + the kernel carrier row (§6.3) | 1 | Mandatory, no ADR, no prerequisite. It is the oldest debt in the corpus (14 days ACCEPTED-with-zero-carriers) and the only row this pack is not authorized to cut — bank it before anything can squeeze it. |
| 2 | **#39** flip + the CX re-base row (§7.4) | 1 | No ADR, and the cross-check is already done (§7.3), so the carrier question needs no re-derivation. The erratum channel is settled by precedent, so this is close to a paste. |
| 3 | **#36** ADR-114 (§4.2) → then the gate-liveness row (§4.3) | 1 | Rule the bypass fork **before** #39's R29 or #36's R9 get re-derived by anyone: ADR-114 Decision 1 is what makes "one attestation record serving both" a decided thing rather than a recurring question. |
| 4 | **#37** ADR-115 (§5.2) → **then** the `done_when` row (§5.3) | 1 | The one **hard** ordering constraint in the pack. The row is blocked on the ADR reading Accepted; landing it first is enforcement-ahead-of-doctrine, which `[#166]` exists to detect. |
| 5 | **#35** ADR-113 (§3.2) → the mechanize-not-prose row (§3.3) | 1 | Last on purpose: it is the largest doctrine change in the arc (it re-seats the canonical instruction file) and the likeliest to consume operator debate. Its row is **independent of the ADR's outcome**, so if the ADR stalls, the row still lands and #35 still clears the anti-orphan rule. |

**Two things to check before you start**, both cheap and both able to invalidate a drafted number:

1. **Re-read the ledger.** §1.2's counts were measured on this branch on 2026-08-19. If anything
   merged overnight, re-run the count before spending the fifth birth.
2. **Re-derive the next free id.** §1.2 says **#559** (highest on disk 558; highest in the live
   manifest 555, because `[#556]`–`[#558]` were born and closed in-window and retired from the
   manifest per ADR-107 §6.3). Ids are never reused — allocate from the **disk** maximum, not the
   manifest maximum, or you will collide with a closed row's record.

**If the window forces a cut**, cut in this order, and record each cut rather than dropping it
silently: (a) #35's row → #35 defers with a trigger; (b) #39's row → §7.5's zero-birth lever;
(c) #37's row → #37 defers, since its ADR alone leaves the schema unbuilt. **Never cut #38's
kernel row** — §6.5's deferral exists for the case where the ledger leaves no choice, and it is
explicitly the worse outcome.

---

## 10 · What this pack does NOT do, and what it could be wrong about

**Did not do**, per the dispatch's NOT list — verified rather than asserted:

- **No status flips.** All five intakes still read `status: DRAFT`.
- **No births.** `tasks/` and `BACKLOG.md` are untouched; every drafted id is `#RESERVED`.
- **No ADR files.** ADR-113/114/115 exist only as text inside this artifact; `docs/decisions/`
  is unchanged and ADR-112 is still the highest on disk.
- **No BACKLOG / tasks writes. No merge.** The branch carries two files: this pack and its
  dispatch stamp, plus the generated `docs/audits/README.md` index row each one owes.

**Honest limits, so the seat does not inherit a false confidence:**

- **The ADR numbers are provisional** (113/114/115, assigned in §9's order). A different
  ratification order renumbers them, and each ADR also owes a one-line editorial entry in
  `docs/decisions/README.md` — not drafted here, because it should describe what was *ratified*,
  not what was proposed.
- **Every drafted ADR recommends a decision it has no authority to make.** #35's is the sharpest:
  it recommends admitting AGENTS.md against a live `CLAUDE.md` §10 anti-pattern and a prior ADR-53
  reversal of the same proposal. §3.2 carries the drafted **refusal** text too, precisely so
  inverting the recommendation is a section swap rather than a rewrite. Reading the recommendation
  as a ruling would be the failure this pack is most able to cause.
- **The anti-orphan rule has no in-repo locator.** It reached this lane through the dispatch as
  *ruled and reviewer-approved*, and grep finds it nowhere in `docs/` or `protocols/`. The rule is
  applied as given; the seat should record it (`protocols/STANDING_RULINGS.md` is the obvious
  home), because a rule that governs five ratifications and lives only in a prompt is the
  memory-resident state this repo files findings about.
- **The gate mesh could not be run in this container.** `audit.py health` needs `click`, and
  `pre-commit` is not installed here, so the usual gates did not execute against these commits.
  What DID run: `validate_hermetization.py` (clean — both filenames pass the ADR-101 Rule B
  grammar), `gen_audit_index.py --check`, `gen_intake_index.py --check` and
  `gen_intake_tree.py --check` (all clean). The pack is markdown only and touches no Python, so
  nothing lint- or test-shaped is at risk — but this is stated rather than left as an implied
  green.
- **Two numbers in this pack are re-derivations, not primary measurements.** The five-birth ceiling
  is the dispatch's arithmetic, reconciled against a live count in §1.2 but not independently
  re-ruled; and intake #37's conversion coverage (*"29 rows converted, ~half remaining"*) is a
  stale snapshot from the memo that **this pack did not re-measure either**, and it should not be
  quoted as current.
