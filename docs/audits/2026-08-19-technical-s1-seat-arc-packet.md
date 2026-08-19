# S-1 SEAT ARC PACKET — 2026-08-19 night adjudication

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-19 · **Slug:** s1-seat-arc-packet
- **Contract of record:** `docs/audits/2026-08-19-technical-s1-seat-arc-contract.md`, committed
  first per ADR-110 at `afbc45f7`
- **Source of truth for every act:** `MORNING-REPORT-2026-08-19.md`'s pointers into the merged
  packs; each pointed section was re-read before its act, and the artifact governed over the digest
- **Authorization:** operator GO covering ruling b′ for N4, the two `STANDING_RULINGS` entries,
  D8 Route 2 and the birth-release scheme; the architect's eight-ruling L-5 block, delivered
  in-session, for act 7
- **Branch:** `docs/seat-s1-night-adjudication`, 12 commits, `--no-ff` into `main`

---

## 1 · Per-act ledger — sha + verification line

| act | sha | what landed | verification |
|---|---|---|---|
| 0 | `afbc45f7` | contract of record | ADR-110 order honoured — committed before any act |
| 1 | `d9d636f6` | N4 sheet, audits-only (ruling b′) | blob `14cebf7c5ba88cbb1be8157634783547c86fa4d8` on **both** sides, 56933 B — byte-identical to the branch tip's version |
| 2 | `0bbaaab7` | `STANDING_RULINGS` §P (P-1, P-2) | `silent_rule_detector` **440** after staging, unchanged, against baseline 441 |
| 3 | `db1e0238` | `.devcontainer` declared, D8 Route 2 | `fleet_parity --run-date 2026-08-19 --repo .dev-knowledge` → 62 at-parity, 16 pass-declared, **0 warn-undeclared** (was 1); root-sweep line reads PASS-declared |
| 4a | `29ab7a1b` | birth `[#559]` kernel row | `--check` ok; `[#559]` appears in **both** the `audit-py` and `environment` serialize-groups — the two-clause round-trip N3 asked to be confirmed |
| 4b | `8f428e21` | birth `[#560]` review-linkage | 1311 chars, unchanged by the same-width id swap, against the 1320 ceiling |
| 4c | `d85490d0` | birth `[#561]` CX re-base | `--check` ok; `validate_backlog` OK at 215 tasks |
| 4d | `f26f8a21` | intakes #38/#39 → ACCEPTED | DRAFT 9→7, ACCEPTED 14→16; both generators run in the required order, both `--check` green |
| 5 | `bae19b0a` | LESSONS promotion | 278 → **287** entries; `gen_doc_counts --check` matches on all three pinned counts (no LESSONS count is pinned — checked, not assumed) |
| 6 | `b099f3ff` | `[#534]` corroboration ref | `--check` ok; `validate_backlog` OK at 215 tasks |
| 7a | `746fa410` | ADR-113 · ADR-108 §B-4 amendment · intake README §5a | `gen_claude_rosters --check` green; both intake generators `--check` green |
| 7b | `6c62fce4` | 8 verdicts transcribed, 7 rows closed | `--check` ok; `validate_backlog` OK at **208** tasks; all 7 files retained with `status: closed` |

---

## 2 · Ledger table — window totals

```
                          at act 4 start      after act 7
banked closures (window)       6                  13      (+7: #323 #407 #450 #449 #406 #281 #494)
births (window)                3                   6      (+3: #559 #560 #561)
window net rows               +3                  -5
live task nodes (H2)          212                 208      (open 188->184, deferred 24 unchanged)
task files on disk            288                 291      terminal 76 -> 83
next free id                 #559                #562
```

**Re-derived live at act 4, not taken from the pack.** N3 §1.2's counts reproduced exactly on the
live tree — 212 live / 188 open / 24 deferred / 288 files / 76 terminal / highest disk id 558. The
`#777` hit in history is the documented synthetic trip-test and is excluded, on the precedent
recorded in the repo's own prior next-free derivations.

### Releases and holds

The gate is `banked-closures(window) > births(window)`, checked before each release; the order is
the contract's; the cap is 5 (N3's) + 1 (N5's) = 6.

```
release 1  kernel row [#559]        6 > 3  OK
release 2  review-linkage [#560]    6 > 4  OK
release 3  CX re-base [#561]        6 > 5  OK
release 4  ---                      6 > 6  FALSE -> halt at act 4
                    ... 7 closures land at act 7 ...
release 4  ---                     13 > 6  OPEN, and 3 of the 6 cap remain
```

**Three births are held and ZERO further were released, and the blocker is not the ledger.** The
remaining drafted carriers belong to intakes **#35, #36 and #37**, all still `DRAFT`, and
**ADR-111 §4 makes a ratified intake a precondition of birth**. Ratifying them means ruling their
ADR fork — N3 assigns all three a force of *"ADR + 1 row"* — and nothing in this arc's
authorization reaches that: the architect's block rules eight L-5 items, none of them #35/#36/#37,
and the operator GO covers the birth-release *scheme*, not the forks. N3 states the risk itself:
every drafted ADR *"recommends a decision it has no authority to make"*, and #35's recommends
AGENTS.md against a live `CLAUDE.md` §10 anti-pattern and ADR-53's prior reversal of the same
proposal. Held with the reason, drafts unconsumed — not cut.

### Draft consumption

| draft source | id | state |
|---|---|---|
| N3 pack §6.3 kernel carrier | `[#559]` | **CONSUMED** — landed verbatim, `[#RESERVED]` → `[#559]` |
| N5 pack §4.5 review-linkage row | `[#560]` | **CONSUMED** — landed verbatim, `[#NNN]` → `[#560]` |
| N3 pack §7.4 CX re-base carrier | `[#561]` | **CONSUMED** — landed verbatim, `[#RESERVED]` → `[#561]` |
| N3 pack §6.5 deferral fallback (#38) | — | **NOT WRITTEN** — conditional on the kernel row not being born; it was born |
| N3 pack §7.5 zero-birth lever (#39) | — | **NOT TAKEN** — drafted for the case where the kernel row would be squeezed; it was not |
| N3 pack §3.3 / §4.3 / §5.3 carriers | — | **UNCONSUMED, HELD** — see the holds above |
| N3 pack §3.2 / §4.2 / §5.2 ADRs 113/114/115 | — | **UNCONSUMED** — and their provisional numbers are now displaced; see §6 |

---

## 3 · WARN delta

```
audit.py health          baseline 12:35        after act 7
verdict                  OK                    DEGRADED  (one FAIL, not this arc's -- section 5)
WARN findings            32                    34        (net +2)
```

| movement | count | detail |
|---|---|---|
| `fleet_parity` | **−1** | the `.devcontainer` root-sweep WARN, cleared by act 3 exactly as the contract predicted |
| `doc_rot` `backlog-row-length` | **+3** | `BACKLOG#559` 2860 · `BACKLOG#561` 2243 · `BACKLOG#534` 1640, all against the declared 1320 ceiling |
| everything else | 0 | the other 6 pre-existing row-length loci (`#529 #530 #533 #546 #547 #552`) and every other check are unmoved |

**All three new WARNs are mine and each was unavoidable under the contract as written.** `[#559]`
and `[#561]` are N3's drafted rows landed *verbatim from the pack's draft source*, which is what the
contract asked for — trimming a drafted row's Done-when would be this seat editing a ratification it
was sent to execute. `[#534]` had **9 characters of headroom** at 1311, so *any* evidence ref crosses
the ceiling; there is no version of act 6 that both lands the corroboration and stays under it.

---

## 4 · Intake status map, #35–#39

| intake | before | after | disposition | carrier / discharge |
|---|---|---|---|---|
| **#35** agent instruction layers | DRAFT | **DRAFT** | — | held: ADR-113(prov.) fork unruled; carrier unborn (ADR-111 §4) |
| **#36** repo autonomy, gate liveness | DRAFT | **DRAFT** | — | held: ADR-114(prov.) fork unruled; carrier unborn |
| **#37** machine-verifiable Done-when | DRAFT | **DRAFT** | — | held: ADR-115(prov.) fork unruled; its row is hard-blocked on the ADR by N3's own sequencing |
| **#38** fleet config standardization | DRAFT | **ACCEPTED** | active | `[#559]` — the kernel row, the fleet's oldest ACCEPTED-unfiled debt |
| **#39** off-machine agent substrate | DRAFT | **ACCEPTED** | active | `[#561]` **+** the existing open `[#554]` (ADR-111 outcome (a) OWNED) |

`decided-by` on both flips names a real ruling, as `docs/intake/README.md` §3 requires at ACCEPTED:
the operator GO on this seat's contract. The `consumers:` line — which N3 flags as false the moment
a flip lands, and which nothing schema-gates — was updated in both files to name what was born.

**#35/#36/#37 stay DRAFT deliberately.** Neither branch of the anti-orphan rule recorded at
`STANDING_RULINGS` P-2 is available to them: no carrier landed, and no dated deferral is drafted for
them. Flipping them would create exactly the ACCEPTED-with-zero-carrier state P-2 forbids.

---

## 5 · Act 7 — delivered, and what remains

The architect's block arrived in-session during act 3 and was held until act 7, as the contract
required. **Seven of eight rulings discharged their row; one is held by the ruling itself.**

| row | verdict | outcome |
|---|---|---|
| `[#323]` | freshness-only STANDS; the two generate hooks not carried in `hub_hooks` | CLOSED |
| `[#407]` | functional-first + dataclasses; classes only for stateful lifecycles; PEP 8 | CLOSED — ADR-108 §B-4 amendment |
| `[#450]` | convention, not schema; promotion-to-ADR is terminal | CLOSED — intake README §5a |
| `[#449]` | accepted-with-reason HOLD; `_SIZE_WARN_BYTES = 65_000` warn-only stands | CLOSED |
| `[#406]` | enforcement point (c) accept-as-is, chosen explicitly; no pre-commit leg | CLOSED |
| `[#281]` | Track-X accepted as durable; no re-peg | CLOSED |
| `[#494]` | RATIFY the ladder by ADR | CLOSED — ADR-113 |
| `[#122]` | **HOLD** — the operator's one-word remove-vs-keep; architect recommends **keep-for-defence-in-depth** | **OPEN** |

**`[#122]` is the only thing act 7 still awaits**, and it awaits one word from the operator. The
row's own Done-when already required it (*"the operator approves and the shim is removed, or the
item is closed as keep-for-defence-in-depth"*) and the no-delete invariant makes the removal branch
unavailable without an explicit ask. The verdict is transcribed to the row; the row stays open.

---

## 6 · Relocated — LESSONS candidates 8 and 9, the channel-runbook items

Per the architect's act-5 ruling these two are **not** promoted to `LESSONS.md`: they are properties
of the **cloud-lane channel**, not of this repo's methodology. N5's runbook draft (its §1.4) lives
inside an immutable audit, so they are recorded here against the two rows that will mechanise that
runbook, which is the available honest home.

**→ `[#540]` (`harvest_batch.py` — read the board, then fetch packets by `git show`)**

> **In a fresh cloud container, verify clone DEPTH and ref CURRENCY before measuring anything
> against `main`.** N5's own clone was shallow (48 commits) with `main` four days stale, and the
> un-repaired reading of its item 4 returned *"0 unlinked"* — wrong **in the reassuring direction**.
> Measured that lane; `docs/audits/2026-08-19-technical-n5-codification-pack.md` §0 Limit 1.

**→ `[#539]` (`gen_lane_contract.py` — assembly-not-generation, with a `--check` leg)**

> **A cloud lane's commits pass WITHOUT the pre-commit gates** — they are not armed there, so
> nothing is bypassed and nothing is checked. The lane says so in its packet; the integrator meets
> those gates for the first time at the merge. Measured that lane; N5 pack §0 Limit 3.

Neither row is edited by this act — a relocation is not a scope change, and both rows are live and
open.

---

## 7 · Findings this arc owes the next seat

1. **`fleet_audit_replication` is FAILing and it is not this arc's.** `automation/fleet-audit` is
   **5 commits ahead of origin**, over the 3-commit threshold, so `audit.py health` reads DEGRADED
   and the `audit-health` pre-commit hook blocks **every** commit in the repo. Ownership proved
   rather than asserted: this seat's own 12:35 baseline recorded `[OK] fleet_audit_replication …
   0 commits ahead`, and the five commits are the routine's own
   `chore(routine/fleet-audit): record 2026-08-19 baseline`. The remedy is a push of
   `automation/fleet-audit`, which is outward-facing and belongs to the operator — **it was
   reported, not performed.** Acts 4d onward carry a declared `SKIP=audit-health` with the reason in
   the commit body; **no `--no-verify` was used anywhere in this arc**, and every other hook ran on
   every commit.

   > **RESOLVED 2026-08-19, after this packet was first written.** The operator pushed
   > `automation/fleet-audit` (`588fc11a..760da0f8`), and the FAIL is cleared — re-measured
   > directly, `git rev-list --count origin/automation/fleet-audit..automation/fleet-audit` returns
   > **0**, and a confirming `python scripts/audit.py health` reads **`health: OK`, zero FAILs**,
   > with `[OK] fleet_audit_replication: automation/fleet-audit is replicated to origin (0 commits
   > ahead)`. WARN count is unmoved at 34, so nothing else shifted underneath it. **`SKIP=audit-health`
   > was needed for acts 4d–8 and is needed no longer**; the `[#122]` closure arc that follows this
   > amendment ran every gate with no skip of any kind, which is the proof the earlier skips were
   > temporary rather than a bypass. Recorded as an amendment beneath the finding rather than by
   > editing it, since audits are immutable (`CLAUDE.md` §5 rule 3) and a resolved blocker that
   > leaves no trace of having been one is worse evidence than a blocker with its resolution
   > attached.
2. **A concurrent session contended for the primary checkout's HEAD and killed two commits.** The
   reflog records `checkout: moving from docs/seat-s1-night-adjudication to main` at **13:27:01**
   and **13:32:50**, both inside a hook run, failing the commit at the ref-update step
   (`fatal: cannot lock ref 'HEAD'`). Nothing was lost — every commit and every staged edit
   survived. A linked worktree was tried as a workaround and **abandoned**, because it distorts the
   very gate it was meant to preserve (`membership_agreement` state-dirs read **0/9** there against
   6/9 in the primary, the gitignored ecosystem state being absent). It was removed and verified
   removed; `git worktree list` shows no `seat-s1` entry.
3. **N4's contract-stamp file is NOT on `main`.** Ruling b′ named one path and this seat landed one
   path, so `docs/audits/2026-08-19-technical-n4-grooming-wave1-contract.md` (commit `3d08a56d`)
   stays on the branch — unlike N1/N2/N3/N5, whose contract stamps are all on `main`. Reported
   rather than fixed by widening an authorized scope. The branch is kept, so it is one
   `git checkout` away.
4. **`docs/decisions/README.md`'s corpus declaration was already stale before this arc.** It reads
   *"86 ADR files … Accepted (81)"*; the live count was **87 before ADR-113 and is 88 now**. It
   labels itself measured-at-declaration, and re-deriving the full five-value status breakdown is
   outside act 7 — recorded rather than half-corrected.
5. **N3's provisional ADR numbers are now displaced.** ADR-113 is the ladder ratification, so
   #35/#36/#37's drafted 113/114/115 renumber if and when they land. N3 anticipates this
   explicitly (*"a different ratification order renumbers them"*), so it is a note, not a defect.
6. **Two rows carry prose references to `[#449]` as open** — `tasks/467-*.md` (*"#449 owns the paste
   ceiling and stays open"*) and `tasks/511-*.md`. Both are reason prose, not
   `kill-candidates:` assertion values (both read `kill-candidates: none`), and
   `check_preflight_backlog_ids`' own docstring rules that non-assertion citations reference closed
   rows by design. **No repair owed**; named so the staleness is on the record.

---

## 8 · What this arc did NOT do

Verified against the contract's own NOT list, rather than asserted:

- **No `scripts/` or `tests/` edit.** `git diff --stat main..HEAD` touches neither.
- **No `#529` / `#530` / `#554` / seam work** — the lanes own those and none was entered.
- **No ruling of this seat's own.** Every verdict traces to the morning report, a merged pack, or
  the architect's block. Where this arc elaborated — ADR-113's namespace clause — the file says so
  in its own honest-limits section.
- **No `--no-verify`, no `git add -A`, no branch deletion.**
- **The N4 lane branch is kept**, unmerged, with its two discarded journal entries recoverable.
