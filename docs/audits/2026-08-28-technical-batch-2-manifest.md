---
batch: 2
seq: 3
shape: ADR-110 — ONE pre-authorized mission -> 7 local file-disjoint lanes + 6 cloud read-only -> TWO integrator queues
dispatched: 2026-08-28
status: open
closed_by: docs/audits/2026-08-29-verification-night-mission-close-packet.md
substrate: LOCAL (7) + CLOUD (6)
---

# NIGHT-BATCH-2 MANIFEST — 2026-08-28 · SEQ 3 · the gate-readable key

**This file is the gate-readable manifest.** `scripts/batch_manifest.py` resolves open batches
with `MANIFEST_GLOB = "docs/audits/*-batch-*-manifest.md"`, reads every input from **HEAD**, and
grants the ADR-110 declared-integration-arc exemption only to `--no-ff` merges of branches
matching `validate_branch_naming.LANE_BRANCH_RE` (`worktree-lane-<letter>-<id>-<slug>`) while a
committed manifest declares an open batch. `batch:` is a **bare number** —
`tests/test_batch_manifest.py::test_the_live_repos_own_manifest_is_well_formed` asserts
`b.batch.isdigit()` over the LIVE manifest, so a descriptive value REDs the suite.

**The dispatch record** — the frozen contracts, the substrate cut, the roster, the merge order and
the dispatch-time measurements — lives at
`docs/audits/2026-08-28-technical-batch2-launch-contracts/`. That directory is the record; this
file is the key.

**What this manifest does NOT cover, stated so nobody assumes it does:** the two integration
branches (`docs/batch-2-dispatch`, `docs/batch-2-integration`) are ordinary author-chosen `docs/`
branches, outside `LANE_BRANCH_RE`, so **they anchor in `JOURNAL.md` like any other arc**. The
same is true of every win-tooling merge (a different repo, no hub gate) and of any cloud
`claude/*` branch (the runtime's naming is outside the grammar — the exemption is unreachable
there by construction). Batch-1 learned the dispatch-merge half the hard way; this batch anchors
its dispatch arc in the same commit range that introduces it.

## Authorization

**Operator GO, 2026-08-28**, pasted as the ratification of `NIGHT-MISSION-2026-08-28.md`
(per-mission pre-authorization; precedent `NIGHT-MISSION-2026-08-27.md`). The GO carries four
decisions: **D2** ratchet move GRANTED to lane C only, bounded, old→new reported · **D3**
`tasks/archive/` APPROVED as the archival destination · **D4** merge order confirmed
(win-tooling N2→N1; hub N1→N6) · **self-merge authorized ONLY for the mission's serialized
integration steps** — lanes remain commit-and-STOP.

## Substrate — Layer-1 cut, Q1–Q4, per lane

**Local (7).** Q1 = YES for every one: each result depends on the pre-commit gate mesh, the
suite, or both. Q1's own row routes that **NOT cloud**, and the 2026-08-26 measurement (container
`uv` 0.8.17 against the repo pin `==0.11.19`) stands. Q2 is additionally YES for every lane — the
frozen contract lives in the operator's prompts dir. **Cut stops at Q2: LOCAL.** Z-G3 keeps local
the default until the W4 defects close; a Codespace smoke-6 receipt is attempted once during
wave-1 verification as Z-G3's entry condition, and its outcome is recorded either way.

**Cloud (6).** Q1 = NO (read-only research, zero gate dependence — every gate-dependent claim is
marked `MEASUREMENT-OWED-LOCAL` by contract), Q2 = NO (own clone of `origin/main`, no
operator-disk state), **Q3 = YES -> CLOUD.**

## Launch lines — copied from PLAYBOOK Ch8 "The dispatch table — the SOLE literal-command site"

Row 1 (LOCAL background lane) and row 2 (CLOUD lane), copied rather than composed:

```
dispatch <FILE.md>                  prompts [y/N], then fires
dispatch <FILE.md> -DryRun          prints the resolved line, sends nothing
Dispatch-Cloud <FILE.md> -Title '<slug>'
```

Every local contract carries an explicit `## Dispatch` fenced block, which is precedence 1 in
`Invoke-Dispatch.ps1` — the line is executed verbatim, so the contract and the launch cannot
disagree and no derivation WARN fires. `dispatch` is **cwd-bound**: lane B was fired from the
win-tooling root, every other lane from the hub root.

## Lane roster — the architect's N-ids mapped onto the ratified lane grammar

The frozen bundle names its lanes `N1…N8`. `validate_branch_naming --lane` requires
`lane-<letter>-<id>-<slug>` — a single letter — so every `N<n>` name is **BAD** and would have
lost the merge exemption silently. Names are derived from the validator, not from the bundle
(STANDING_RULINGS F2). All eight validate `OK`; N5's slot was taken by N8 in the bundle itself.

| lane | bundle id | branch | row(s) | scale | model/effort | repo |
|---|---|---|---|---|---|---|
| A | N1 | `worktree-lane-a-604-wintooling-deploy` (+ consumer branch `worktree-lane-a-604-wintooling-consumer`) | [#604] + [#606] | L | opus/high | hub **and** win-tooling |
| B | N2 | `worktree-lane-b-610-dispatch-verbs` | [#610] carrier half | M | opus/high | win-tooling |
| C | N3 | `worktree-lane-c-610-night-protocol` | [#610] doc half | M | opus/high | hub — **the batch's only ratchet authorization** |
| D | N4 | `worktree-lane-d-612-docrot-archival` | [#612] | M | opus/high | hub — **exclusive `tasks/` writer** |
| E | N6 | `worktree-lane-e-605-consumer-root` | [#605] | M | opus/high | hub |
| F | N7 | `worktree-lane-f-577-byte-cap` | [#577] | S | opus/medium | hub |
| G | N8 | `worktree-lane-g-591-preflight-predicates` | [#591] | M | opus/high | hub |

Cloud (read-only, one artifact each, `claude/*` branches, **no exemption and none needed** — they
commit nothing): C1 candidate triage · C2 [#598] slow-marker evidence · C3 intake-61 ratification
· C4 codex-surface census · C5 README/VISION census · **FM-C** full funnel census (wave-2's
contract, dispatched in wave 1 because it is independent of every wave-1 lane).

Model routing is `opus` throughout per the Ch8 matrix — *"the default for any arc touching
`.dev-knowledge`"*, amended 2026-08-07 to key on **context load**, not diff size. Effort is
`high` for multi-file reasoning and `medium` for the one S-class lane.

## Merge order (frozen by D4)

**win-tooling queue:** B → A(consumer). **Hub queue:** C → D → G → A(hub) → E → F.
`--no-ff`, one at a time, from the primary checkout, ancestor-proven teardown after each.
D4 fixes two edges: **B before A** (win-tooling) and **A before E** (hub — A exercises the tool E
rewires: files disjoint, behaviour not). Lane A's two branches are the reason the hub queue
carries an A slot the bundle's own "N3→N4→N8→N6→N7" list does not: its `ecosystem/*.yaml`
amendment is a hub write and has to land in the hub, before E, by D4.

## Integrator branch

`docs/batch-2-integration`. ≥2 commits: carried edits + regenerated surfaces first, the JOURNAL
entry naming an earlier commit on that same branch second. The JOURNAL entry for the lane queue is
written **before** the queue runs, naming the lane tip SHAs, because a merge cannot name its own
hash and `journal_spine_anchor` gates `audit-health` at pre-commit.

## Measured preconditions at dispatch (2026-08-28, 23:35–23:47 local)

- `uv --version` = **0.11.19** against `pyproject.toml` `required-version = "==0.11.19"` — MATCH.
- `git status` clean on `main` at `3e52a2f8`; `origin/main` == `main` (0 ahead / 0 behind), so the
  six cloud clones see the same tree the local lanes branch from.
- `git worktree list` = primary only. No live sibling session; no leftovers inherited.
- `silent_rule_detector`: detector `silent-rule-v5`, **files 61, count 443**, live == baseline.
  **Zero headroom.** (Batch-1 measured 60 files; `AGENTS.md` is the 61st.)
- `validate_doc_rot`: **77** doc-rot loci past threshold — the P4 figure, **re-measured**, not
  inherited. Dominated by `backlog-row-length` (ceiling 1320 chars) plus a `backlog-accretion`
  family (≥3 dates, ≥30d span, >700 chars).
- Byte-cap payload: `~/.codex/AGENTS.md` **3,891 B** + repo-root `AGENTS.md` **5,539 B** =
  **9,430 B = 28.78 %** of the 32,768 B `project_doc_max_bytes` cap.
- win-tooling: on `main` at `53a1d02`, clean; **11 local branches, 1 upstream** (`main` only);
  4 pre-existing worktrees (the morning's X3 item, untouched tonight).

## Contract defects found at dispatch — recorded, not silently repaired

Three, all of the same class the batch's own lane G is being built to refuse at freeze time.
Each is written into the affected lane's contract so the executor meets it before the code.

- **D-F1 — lane F's Intent restates a false measurement.** It cites batch-1's *"9,161 B = 28.0 %"*
  combined payload. Measured tonight the payload is **9,430 B = 28.78 %**, because repo-root
  `AGENTS.md` is **5,539 B / 107 lines**, not the *"103 lines, 5,270 B"* `CLAUDE.md` §2.68 claims.
  `git cat-file -s 43c18e9f:AGENTS.md` == **5539**, and `43c18e9f` is the file's **only** content
  commit — so §2.68's figures were wrong when written, not stale by drift. Mitigation inside lane
  F's own footprint: the test asserts **against the cap**, re-measuring live, never against a
  remembered constant. Correcting §2.68 is a `CLAUDE.md` write outside every lane's scope (and
  that file sits at 196/200 of its budget) — carried to the integrator as a candidate filing.
- **D-B1 — lane B's "the paginated events loop already exists ~line 1079" is false.** Lines
  1078–1085 of `config/dispatch-helpers/DispatchHelpers.psm1` are a **receipt-polling** loop;
  `next_cursor` appears **nowhere** in the module (grep: 0 hits). The pagination the 2026-08-27
  harvest performed was done **by hand**. Consequence: Harvest-Cloud is half extraction, half new
  code, and the contract's own framing would have had the lane describe new code as an extraction.
- **D-B2 — lane B's cp-defect line numbers point at prose.** 1279, 1282 and 1402 are inside
  comment blocks. The live `gh codespace cp` argv arrays are at **1591**, **1637** and **1669**.

A fourth, pre-existing and not a defect of this batch: `[#577]` and `[#584]` are **still open** on
`main` although batch-1 landed their work. Closure is `/review-closures`' call; lane F reports the
candidacy and files nothing.

## Ratchet pre-authorization

**Lane C: GRANTED** (D2), bounded to the night-protocol section plus the `HANDOFF_PROCESS.md`
forms-card delta, old→new reported. **Every other lane: delta must be 0**, verified against the
dispatch measurement (443/61) before the lane's first and last commit. `validate_transition`
refuses a baseline *raise* in code regardless of authorization, so a token-free authoring is the
preferred outcome — batch-1's L1 spent **zero** of an identical grant.

## Stop conditions carried from the mission (any one freezes that queue)

S1 unresolvable merge conflict on `JOURNAL.md` or a generated surface · S2 ship-gate **NEW** WARN
naming a surface a tonight-lane touched · S3 ratchet delta outside lane C's authorized bound ·
S4 any lane attempting an act its contract forbids (a validator or gate refusal counts) ·
S5 hard stop **07:30 local** — whatever state holds, the packet is written and waits.

## How this exemption expires

`closed_by:` names `docs/audits/2026-08-29-verification-night-mission-close-packet.md`. The batch
is open only while that path is **absent from the committed tree**. The packet landing ends the
exemption automatically, with no edit anywhere — which is the only expiry compatible with
`docs/audits/` being immutable.

## D-M1 — a fourth defect, found by the gate mesh at freeze, and fixed before dispatch

`check_substrate_declaration._corpus` treats **every `*.md` in any `docs/audits/*launch-contracts/`
directory** as a committed lane contract, and `ARM_DATE = 2026-08-27` gates everything landing on
or after that date. So the first attempt to commit this record REFUSED — `substrate-no-live-verb`
on every file in the directory, which FAILs `audit-health` and would have blocked **every commit
in every lane** for the whole night. Three consequences, all taken before dispatch:

1. **The directory now holds only dispatchable per-lane contracts** — the 13 files a lane was
   actually launched from — and each declares `**Substrate:** local|cloud` in Ch8's own spelling
   plus a `**Worktree pairing:** slug `X` -> branch `worktree-X`` line. The pairing line is not
   decoration: `validate_substrate._checkout_key` reads exactly that shape, and without it seven
   local lanes all resolve to `<primary checkout>` and trip `substrate-second-local-writer`.
2. **The three non-contract source documents moved to top-level `docs/audits/`, byte-identical:**
   `2026-08-28-technical-night-mission-authorization.md` (the operator-ratified mission),
   `2026-08-28-technical-night-batch2-frozen-bundle.md` and
   `2026-08-28-technical-fm-wave2-frozen-bundle.md` (the architect's frozen bundles). They are the
   record; they are not contracts anything dispatches, and the gate is right to say so.
3. **The redundant copy of the 2026-08-27 harvest manifest was dropped** — it is already committed
   at `docs/audits/2026-08-27-technical-night-harvest-manifest.md`, and lane B's contract now cites
   that path instead of a copy.

**Residual, reported not repaired:** batch-1's own frozen contract still WARNs
`declares substrate 'one'` — `_SHAPE_RE` reading `**Shape:** ONE plan -> 5 file-disjoint lanes`.
That is finding **C-F**, and lane G is chartered to fix it tonight in the same organ. It is the
only substrate finding left on the tree at dispatch.

**Candidate filing for the integrator (not filed here):** the launch-contracts home has an
implicit schema nothing documents — every file in it must parse as a lane contract. Ch8's
"Where the contract file lives" subsection describes the directory as *"the contracts a batch was
ACTUALLY launched from … copied there byte-identical"*, which reads as permission to copy the
bundle in. It is not.
