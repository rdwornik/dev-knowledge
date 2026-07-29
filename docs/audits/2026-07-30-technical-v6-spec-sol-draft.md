---
class: technical
date: 2026-07-30
slug: v6-spec-sol-draft
Status: "DRAFT — NOT CANON"
producer: sol
pin_sha: bcbff91b
pinned_inputs:
  - "docs/audits/2026-07-30-technical-intake18-ratification-record.md (whole file)"
  - "protocols/HANDOFF_PROCESS.md (whole file; Version: 5.7)"
  - "docs/intake/2026-07-27-func-operator-design-input-night-shift-handoff-reform.md, Section B item (b) only, lines 95-106"
  - "Deferred-leg register: input 1 Direction, label, riders plus its named per-amendment deferrals; tasks/446-section-b-b-one-round-trip-boot-build-the-v6-ca.md (whole file)"
  - "scripts/audit.py, _select_active_bundle, lines 1575-1673"
---

# HANDOFF_PROCESS v6 spec — sol producer draft

> **Status: DRAFT — NOT CANON.** Input to the `[#446]` build arc. It neither changes nor
> supersedes canonical HANDOFF_PROCESS v5.7.

## 1. Boundary and v6 cut

This draft discharges only the ruled `§B(b)` carrier pack: U1's one-round-trip boot; A7's
P0a/P0b/P0c standing-topic rows; A4 item 3's boot-header `Destination` row and P3 comparison
leg; A10 item 2's numeric `HANDOFF_BOOT` byte budget and assembler warn; A11's re-scoped
candidate-bundle guard, RM-8 overwrite refusal, `verify_handoff_probes.main()` parameters,
and `[#421]` second-tokenizer absorption; and U5's v6 cut.

The canonical build is to stamp `Version: 6.0`. The bump lands with `[#446]`, not before it,
and the five `reconciled_with` edges named by `[#446]` are swept in that same build per
`check-against-spec`.

Except for the deltas stated here, HANDOFF_PROCESS v5.7 carries forward unchanged. This draft
adds no new handoff leg, mode, artifact, ferry turn, or standing topic beyond the ruled pack.

## 2. One-round-trip boot

### Normative flow

One CC-side command MUST run the entire live probe gate at check-time, perform the architect
orientation reads, verify inherited claims, run the A7 P0a/P0b/P0c standing-topic legs, run
the A4 P3 destination comparison leg, and emit exactly ONE evidence block.

The operator pastes that block exactly once. The browser consumes its table instead of
dictating or relaying individual commands one at a time.

The evidence block is check-time command output, not a generation-time answer embedded in a
handoff bundle. The bundle continues to ship questions, source locators, and exact verification
commands without answers. This preserves the v5.7 answer-free bundle while removing operator
ferrying.

The command's public name is `OPEN`; no pinned input rules one.

### Evidence-block contract

The single block is one table. Every row reports its source locator, check performed,
PASS/FAIL, and the live evidence needed by the browser. No required row may be emitted in a
second block or deferred to another ferry turn.

| Required row | Live source / locator | Required check-time behavior |
|---|---|---|
| Live check count | `ALL_CHECKS` in `scripts/audit.py` | Run the v5.7 manifest command and report count + last name. |
| Exact-line quote | Named `PLAYBOOK` / `ESSENTIALS` / spec section | Read the live section; the quote must be a substring. |
| Live HEAD / tree | Live git | Run the v5.7 manifest commands and report the check-time SHA and tree state. |
| Ship-gate read-back | `audit.py ship-gate` ∩ `ecosystem/disposition-register.yaml` | Re-derive and report the final GREEN/RED verdict, dispositioned-WARN count, and any `[stale]` line. |
| Pointer round-trip | Live `PLAYBOOK` section named by the pointer | Open the live section and compare. |
| Architect orientation: vision | `VISION.md` `## Vision` opening sentence | Perform the v5.7 §13(c) exact-line substring check; never put the generation-time answer in the bundle. |
| Architect orientation: architecture | `ARCHITECTURE.md` Ch1 opening line | Perform the v5.7 §13(c) exact-line substring check; never put the generation-time answer in the bundle. |
| Inherited claims | Claims inherited through the handoff/supplement | Verify CC-side against the live repo. Inherited-claim verification stays; the work moves CC-side and does not disappear. |
| P0a standing topic | `OPEN` | MUST be in this block. The pinned inputs name P0a but do not define its locator, command, or honest-narrowed assertion. |
| P0b standing topic | `OPEN` | MUST be in this block. The pinned inputs name P0b but do not define its locator, command, or honest-narrowed assertion. |
| P0c standing topic | `OPEN` | MUST be in this block. The pinned inputs name P0c but do not define its locator, command, or honest-narrowed assertion. |
| P3 destination comparison | Boot-header `Destination` row and `OPEN` comparison target | MUST be in this block. Compare with the ruled target once settled. |

The v5.7 §13(c) opening sequence remains unchanged in substance:
**role → vision → standing topics → backlog**. Batching does not remove or reorder a read.

Any FAIL in any required row blocks onboarding. A missing required row is not a pass. Degraded
coverage is reported, never silently counted as pass. The reshape changes the transport count,
not the proof threshold.

## 3. §5 teeth-y forced primary-source read

### Unchanged v5.7 carry-forward

The four conditions, complete five-row probe manifest, empirical promotion gate, and structural
anti-bluff enforcement carry forward word-for-word in substance.

> The forced read has **teeth** when its verification **cannot be answered from the compaction
> summary** — the answer exists only in the live primary file/state at answer-time. A probe is
> teeth-bearing when all four hold (the fourth — bounded-deterministic — ratified at intake #18):
>
> 1. **Live-only answer** — volatile or high-entropy (a count that drifts, a sha, an exact
>    line) that a summary rounds off or omits.
> 2. **Generator-excluded** — the handoff ships the **question + source-locator + the exact
>    verification command**, and **never the answer**. (A probe that bakes its answer in is, by
>    construction, bluffable — and is rejected.)
> 3. **CC-checkable** — CC re-derives the ground truth read-only from disk/git at check-time
>    and compares, exactly as the existing validators do.
> 4. **Bounded-deterministic** — the verification terminates in bounded mechanical steps at
>    check-time. A probe whose honest answer requires unbounded judgment over an open set is an
>    arc, not a probe, and is rejected (origin: P10, JOURNAL 2026-07-26 (h); LESSONS 2026-07-27
>    S3d).

The manifest carries forward unchanged:

| Probe | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|
| **Live check count** | `ALL_CHECKS` in `scripts/audit.py` | the count drifts every time a check lands; a hardcoded number goes stale | `python scripts/audit.py checks` (count + last name) |
| **Exact-line quote** | a named `PLAYBOOK`/`ESSENTIALS`/spec section | a paraphrase from a summary is not byte-identical | read the live section; the quote must be a substring |
| **Live HEAD / tree** | live git | the summary holds the *generation-time* sha; new commits move HEAD | `git rev-parse --short HEAD` + `git status` |
| **Ship-gate read-back** | `audit.py ship-gate` ∩ `ecosystem/disposition-register.yaml` | the GREEN/RED verdict, dispositioned-WARN **count**, and any `[stale]` line are computed at answer-time over live git ∩ `main`-history; the values are absent from the bundle. Folds the former **drift-flag set** + **freshness witness** probes: `git_backlog_drift` and `canonical_freshness` are `ALL_CHECKS` members, so the gate re-derives them and prints evidence inline | `python scripts/audit.py ship-gate` (read final GREEN/RED verdict + disposition count + any `[stale]` line) |
| **Pointer round-trip** | the live `PLAYBOOK` section a pointer names | re-narration is outlawed (§2/§3); the answer exists only by opening it | read the live section; compare |

The empirical promotion gate carries forward verbatim from v5.7:

> That the teeth *bite* is proven empirically, not by review: at promotion, dogfood one real v5
> handoff and attempt to answer each probe **from the compaction summary alone** — every probe
> **must fail** to be bluffed. A probe answerable from the summary is removed or hardened. The
> flip gate tests that the teeth force a primary-source read, not merely that the spec reads
> well (§11).

Structural enforcement carries forward verbatim from v5.7:

> Item 2's "never the answer" contract is **machine-held, not hand-discipline** (landed
> `9d5ebe5`, 2026-07-04, after the 06-20..07-03 `expected:`-hint erosion showed hand-copy
> alone regresses):
>
> - **Answer-hint FAIL rung** — `scripts/verify_handoff_probes.py` FAILs any probe **row**
>   carrying an `expected[ :]`-form answer hint (row-scoped, so historical bundles stay judged
>   by their own era; the deployed `handoff_probes` check reads the latest bundle and gates
>   `/ship`).
> - **Answer-free by construction** — `scripts/gen_handoff.py` never hands the render
>   functions the generation-time hint VALUES (HEAD / check counts / ship-gate verdict /
>   backlog counts); those are diverted to a **stdout JOURNAL-draft** for the wrap entry —
>   never into a browser-visible bundle file, never auto-appended.
> - The empirical dogfood above therefore re-runs **structurally on every bundle** via the
>   gate, not once at promotion.

### Replaced v5.7 “Who runs it” transport paragraph

The proof boundary stays unchanged: the browser has no file access, so the teeth are enforced
at the **CC ↔ primary-source** boundary. CC ships the manifest in the handoff (questions +
locators + commands, no answers).

Instead of the browser responding “run `<command>`” for each probe, one CC-side command runs
every verification against live state at check-time, performs orientation and inherited-claim
checks, re-derives ground truth, and emits PASS/FAIL in the single evidence block. The operator
pastes once and the browser consumes the table.

**Any FAIL blocks onboarding.** The reconciliation remains: “force the receiver to open the
primary source” becomes “**force CC to re-derive every load-bearing fact from the live primary
source at check-time, and block onboarding on any mismatch.**”

## 4. `Destination` row and P3

Every lane-opening boot header MUST carry a `Destination` row declaring ex-ante:

- worktree name;
- branch in a sanctioned lane shape;
- write-scope; and
- execution MODE with basis.

A lane inherits none from a prior prompt. This is the v5.7 §13 destination contract carried
forward unchanged; v6 makes the boot-header row mechanical.

P3 is a required row inside the single evidence block, not a ferry turn. Its exact second
operand and PASS comparison are `OPEN` because the pinned inputs do not define them.

## 5. `HANDOFF_BOOT` byte budget

`protocols/HANDOFF_BOOT.md` MUST have a stated numeric byte budget. The assembler MUST use its
existing size machinery to emit a warning when the boot exceeds it.

`OPEN: HANDOFF_BOOT_BYTE_BUDGET = <number>`.

The inputs require a number but supply none. The operator/architect must rule the value before
A10 item 2 can be implemented. The assembler action is a warning; this draft does not turn it
into a blocking gate.

## 6. A11 guards and callable verification

### Active-bundle premise correction

RM-7's premise is stale. Live `_select_active_bundle` already selects by git add date rather
than slug order and exposes `sole`, `fresh`, `add-date`, `no-git`, `ambiguous`, and `degraded`.
It returns no bundle for ambiguous multiple-fresh candidates or degraded git-probe conditions.
V6 MUST retain that behavior; it does not rebuild lexical “latest” selection.

### Re-scoped staged-diff guard

The gate-coverage guard MUST verify **every candidate bundle in the staged diff**. Selecting
one active bundle is insufficient. An uncovered staged-diff candidate is a guard failure.
This is additive to `_select_active_bundle`; it does not erase any selector outcome above.

### RM-8 overwrite refusal

Generation MUST refuse an overwrite rather than replace an existing target. The exact target
set and diagnostic are `OPEN`; the inputs rule refusal but not those implementation details.

### `verify_handoff_probes.main()`

`verify_handoff_probes.main()` MUST gain `repo_root` and `cross_repo`. Their types, defaults,
CLI mapping, and interaction are `OPEN`; the inputs name but do not define them.

### `[#421]` second-tokenizer absorption

The `[#421]` second-tokenizer leg is absorbed into `[#446]`, not killed. Its exact tokenizer
contract and acceptance assertion are `OPEN`; the inputs name the absorption but do not define
its behavior.

Each A11 leg lands with a test or is re-deferred by ruling. No silent omission completes it.

## 7. Unchanged v5.7 surface

All v5.7 text and mechanics not expressly changed above carry forward unchanged:

- §§1-4 retain the CC-owned model, residual, thin methodology reference, and thin browser boot;
  §4's deferred budget parenthetical is replaced by the settled v6 budget text;
- §5 retains the complete teeth, manifest, empirical gate, and structural anti-bluff contract;
  only the ferrying paragraph is reshaped;
- §§6-12 carry forward unchanged;
- §13 retains its modes, orientation sequence, inherited destination contract, bundle shape,
  and transport-medium contract; P0 and P3 now emit within the one block;
- §§14-16 carry forward unchanged; and
- v6 section history records the one-round-trip reshape and exact carried legs without
  rewriting earlier history.

## 8. Acceptance

The carrier is complete only when:

1. one CC-side command produces one complete evidence block;
2. the operator needs one paste and the browser consumes one table;
3. all five v5.7 manifest checks still run against live state;
4. inherited claims are verified CC-side;
5. P0a/P0b/P0c and P3 are rows in that block;
6. any FAIL blocks onboarding;
7. generation-time answers remain excluded from browser-visible bundle files;
8. the boot header carries `Destination`;
9. the numeric budget and assembler warning land;
10. every candidate bundle in the staged diff is covered;
11. RM-8, the `main()` parameters, and `[#421]` land with tests or are re-deferred by ruling;
12. HANDOFF_PROCESS stamps v6 and the five `reconciled_with` edges are swept in the same build.

## Deferrals carried

This is register coverage, not a claim that canon or code changed.

- [x] **U1** — one CC-side command → one evidence block → one operator paste.
- [x] **U5** — v6 CUT; the bump rides `[#446]` with the five-edge sweep.
- [x] **U6(a), DEFERRED** — intake #19 §B standing night-batch section + ADR-105 activation
  record. Trigger: the next night-batch request.
- [x] **U6(b), DEFERRED** — standing closure delegation (ADR-70 amendment). Trigger: the next
  `/review-closures` batch, operator's call.
- [x] **A3 OPEN sibling ruling** — `~/.claude/rules/core-invariants.md` #5 sibling edit remains
  OPEN. Trigger: operator's explicit go.
- [x] **A4 item 3** — `Destination` row + P3 row; exact P3 comparison remains OPEN.
- [x] **A5 hook leg, DEFERRED** — `normalize-dated-headers` remains S/later, as staged by the
  intake.
- [x] **A7** — P0a/P0b/P0c required inside the one block; exact contracts remain OPEN.
- [x] **A10 item 2** — numeric boot budget + assembler warn; number remains OPEN.
- [x] **A11** — stale premise corrected; staged-diff all-candidate coverage; RM-8 refusal;
  `verify_handoff_probes.main(repo_root, cross_repo)`; `[#421]` absorption.

## OPEN questions

1. **OPEN: What command name exposes the one-round-trip boot?** Settle by operator/architect
   ruling or a pinned build instruction naming the command surface.
2. **OPEN: What are P0a/P0b/P0c's exact source locators, commands, and honest-narrowed
   assertions?** Settle by a ruling mapping each label to its mechanical row contract.
3. **OPEN: What two values does P3 compare, and what is PASS?** Settle by a ruling defining
   the comparison target and mechanical check.
4. **OPEN: What numeric byte budget applies to `protocols/HANDOFF_BOOT.md`?** Settle by an
   operator/architect numeric ruling; A10 cannot close on a placeholder.
5. **OPEN: What exact targets and diagnostic does RM-8 govern?** Settle by a ruling or pinned
   generator acceptance contract.
6. **OPEN: What are the types, defaults, CLI mapping, and interaction of `repo_root` and
   `cross_repo`?** Settle by a pinned callable/CLI contract.
7. **OPEN: What tokenizer behavior and acceptance test constitute `[#421]` absorption?**
   Settle from an allowed ruling or build input defining that leg.