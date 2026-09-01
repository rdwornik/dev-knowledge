# [#629] + [#630] lane-g-7 — end-of-lane packet

**Lane:** `lane-g-7-contract-validator-predicates` · branch
`worktree-lane-g-7-contract-validator-predicates` · batch F · local, commit-and-STOP.
**Contract of record:**
`docs/audits/2026-09-01-technical-batchf-launch-contracts/LANE-g-7-contract-validator-predicates.md`.
**Rows:** `[#629]`, `[#630]`.

**No-consumer:** an end-of-lane packet is consumed by the integrator reading it at merge and
by the two rows it closes, never by a governance-surface citation naming its path — the same
posture the frozen contract this packet discharges declares about itself. Filing a citation
into `tasks/629-*.md` / `tasks/630-*.md` is the integrator's closure act, outside this lane's
write-scope.

**Commits, in contract-step order:**

```
e53f75b4  step 1  RED-first witnesses for both predicates (fail before the code exists)
e752a89b  step 2  [#629] -- amendment-cannot-subtract, into validate_substrate.py
a20f4f5e  step 3  [#630] -- manifest/contract slug set-equality, into batch_manifest.py
<this>    step 4  pytest green + this packet
```

---

## 1. Done-contract, item by item

| # | Item | Discharge |
|---|---|---|
| 1 | `[#629]` — a new predicate REFUSES a contract whose amendment block negates, removes or forbids an act/step/write-scope entry present in its own body; refusal text names the REISSUE path; joins the closed `RULE_IDS` set | `RULE_AMENDMENT_SUBTRACTS` ("amendment-subtracts-an-act"), `validate_substrate.py:{amendment_subtractions, _amendment_blocks, _AMENDMENT_HEADING_RE, _NEGATION_RE}`, wired into `validate_contract`; detail string names `gen_lane_contract`/REISSUE explicitly; `RULE_IDS` now 8-tuple, order pinned by test |
| 2 | `[#630]` — the freeze REFUSES unless the manifest's lane-table slug set equals the batch directory's contract slug set, both ways; refusal names both sides | `batch_manifest.freeze_manifest_contract_agreement()` + `manifest_lane_slugs()`, using `validate_substrate.contract_slug()` (new) for the contract side; one `Refusal` naming `manifest_only`/`contracts_only` explicitly, never a count |
| 3 | RED-first witnesses, both — DC-3 amendment shape; renumbered-slug (`lane-b-2` vs `lane-b-3`) shape | `test_leg7_refuses_an_amendment_that_negates_an_act_still_in_the_body`; `test_freeze_refuses_when_manifest_slug_and_contract_slug_disagree` — both confirmed RED (`AttributeError`, missing symbols) before step 2/3 landed |
| 4 | Armed at FREEZE, grandfathered at the commit sweep; both legs carry a `LEG_ARM_DATES` entry | `validate_substrate.LEG_ARM_DATES = {RULE_AMENDMENT_SUBTRACTS: 2026-09-01}`; `batch_manifest.LEG_ARM_DATES = {RULE_MANIFEST_CONTRACT_SLUG_AGREEMENT: 2026-09-01}` — §3 below states the honest limit this creates |
| 3′ | English, hyphen-only names, logging not print, Click where warranted, `pytest` green | no CLI added (neither predicate needed one to satisfy the Done-contract); suite evidence §5 |

## 2. What changed

Exactly the frozen write-scope, nothing else:

```
scripts/batch_manifest.py         108 ++++++++++++++++++++++++++++++++-
scripts/validate_substrate.py     126 +++++++++++++++++++++++++++++++++++++++
tests/test_batch_manifest.py       79 ++++++++++++++++++++++++
tests/test_validate_substrate.py   87 ++++++++++++++++++++++++++-
4 files changed, 397 insertions(+), 3 deletions(-)
```

`validate_substrate.py` gains: `RULE_AMENDMENT_SUBTRACTS`, its `LEG_ARM_DATES` entry,
`_PAIRING_SLUG_RE` + `contract_slug()`, `_AMENDMENT_HEADING_RE` / `_SUBTRACTION_TARGET` /
`_NEGATION_RE` / `_amendment_blocks()` / `amendment_subtractions()`, and the leg-7 branch
inside `validate_contract()` (checked first, unconditionally — before substrate resolution,
because contract self-consistency is orthogonal to substrate validity).

`batch_manifest.py` gains: an import of `Refusal`/`contract_slug` from `validate_substrate`
(one-directional; no cycle — checked), `RULE_MANIFEST_CONTRACT_SLUG_AGREEMENT`, its own
`LEG_ARM_DATES`, `_LANES_HEADING_RE` / `_SLUG_TOKEN_RE` / `manifest_lane_slugs()`, and
`freeze_manifest_contract_agreement()`.

**Proposed diffs:** none pending — both predicates are landed, not proposed. No follow-on
edit is queued.

## 3. The decision this lane took under contract defaults — reported, not asked

The V-2 budget escalates on (a) curated-baseline touches, (b) rule-vs-ruling conflicts, (c)
fork classes with no standing ruling. **One thing here is adjacent to (c) and is reported
rather than escalated, because it resolves to "matches existing precedent" on inspection.**

**D-1 · `LEG_ARM_DATES` for both new legs lives in the LOGIC module, not an adapter, because
this lane's frozen write-scope does not reach `scripts/audit_checks/check_substrate_declaration.py`.**
The precedent (legs 5/6) put `LEG_ARM_DATES` in that adapter, where the commit-time
grandfather is actually applied. This lane cannot edit that file. So: both new legs are
declared in their own logic module (`validate_substrate.py` / `batch_manifest.py`) as
documentation-and-data for a future adapter change to consume, and — because the adapter
currently calls `validate_substrate.validate_batch()` unconditionally, with no per-leg
grandfather for a rule id it doesn't know about — **leg 7 is *de facto* armed everywhere,
immediately, the moment this lane merges.** [#630]'s check is not wired into any adapter at
all yet, so it carries no live-gate risk regardless.

Verified this is safe rather than assumed: `check_substrate_declaration.check_substrate_declaration()`
run directly against the live committed corpus after landing leg 7 reports **`pass`, 0 new
findings** — the same 14 pre-existing grandfathered leg-5/6 findings as before, unchanged.
`amendment_subtractions()` run over all seven of this batch's own committed contracts finds
nothing. The honest residual: a future contract that legitimately needs an `## Amendment`
heading whose body still contains something the amendment says not to do (the shape this
predicate exists to catch) will refuse **at commit time too**, not only at freeze, until a
follow-on lane teaches the adapter this rule's arm date. That is the same direction the
original four legs shipped in (measured-then-armed, no grandfather at all) — not a
regression this lane introduced, but stated so it is not mistaken for oversight.

## 4. Detection design, stated so the honest limits are visible

**Leg 7 is textual and conservative, per the requirement's own words.** A negation word
(`do not`, `no longer`, `never`, `skip`, `remove`, `drop`, `forbid`, `cancel`, `without
performing/running`) within 80 characters of a target (`Act <word>`, `Step <n>`, or a
backticked token) inside an `## Amendment` block, where that exact target also appears
**earlier in the same contract's body** — refuses. The "appears earlier" clause is what lets
an amendment explain itself in the negative about something it never claimed
(`test_leg7_ignores_a_negation_with_no_target_present_in_the_body`) without refusing.
**Honest limit:** it cannot see a subtraction phrased without one of the listed negation
words, or a target that isn't shaped like `Act X` / `Step N` / a backtick token — the same
trade every other leg in this module makes (leg 2 is token-based; leg 3 matches path shapes).

**Leg 630 reads the manifest's `## THE LANES` table and the contract's own pairing line, never
a filename.** Deliberate: inferring a contract's slug from its filename would make this
predicate blind to exactly the class of defect it exists to catch — a mismatch between what a
file is named and what it declares itself to be. **Honest limit:** a contract whose pairing
line does not resolve to a slug at all (malformed layer-1 shape) is silently skipped here,
because it already fails elsewhere (`gen_lane_contract` layer 1, or leg 1 of `[#591]`) and
stacking a second finding on the same defect helps nobody.

## 5. Evidence

**Targeted suite** (`pytest tests/test_validate_substrate.py tests/test_batch_manifest.py`),
the lane's own convention (`CLAUDE.md` §4: *"In a lane run the targeted tests for that lane's
diff; the full suite runs once, at integration ([#528])"*):

```
97 passed, 1 xfailed (the pre-existing known-open [#512] xfail, unrelated to this lane)
```

**The full suite was NOT run in this lane, on purpose, per that same convention** — it is the
integrator's act at merge, not a lane's. Two attempts to run it anyway (as an over-cautious
extra check) were made and both were killed by the environment before completing (background
xdist runs in this worktree did not survive across turn boundaries; matches this repo's own
recorded memory that a full suite inside a lane worktree is unreliable). Recognizing the
convention already answers the question the attempts were trying to answer, they were
abandoned rather than repeated a third time. **`ruff check .`: All checks passed.**

**Live-corpus sanity, run directly (not via a test):**

```
check_substrate_declaration(repo) -> pass, 0 new findings from leg 7 (14 pre-existing
  grandfathered leg-5/6 findings unchanged)
amendment_subtractions(text) -> [] for all seven of this batch's own committed contracts
manifest_lane_slugs(batch-f-manifest text) -> the same seven slugs the manifest's own
  hand-checked "THE MANIFEST'S LANE ENUM AND THE CONTRACT SLUGS ARE IDENTICAL" claim names
freeze_manifest_contract_agreement(batch-f-manifest, the seven real committed contracts) -> []
```

## 6. Scope discipline — what was NOT touched

Exactly the four frozen write-scope files, nothing else. No merge, no push, no other lane's
branch. No JOURNAL entry (integrator's surface). No index regeneration — this lane's single
hook-bypass declaration: **none used** (no `SKIP=`, no `--no-verify`, at any commit). No
edits to `scripts/audit_checks/check_substrate_declaration.py`, `scripts/gen_lane_contract.py`,
or `scripts/preflight_contract.py` — all three were considered (§3, §4) and left alone because
they sit outside this lane's declared footprint.

## 7. For the integrator

- No merge-order dependency: this lane's write-scope is disjoint from every other batch-F
  lane's (confirmed at freeze — batch-F manifest, "ZERO DEVIATIONS").
- `[#630]`'s check is not yet wired into any gate/adapter — it is a tested, callable predicate.
  Wiring it (and adding `LEG_ARM_DATES` support to `check_substrate_declaration.py` for both
  new legs, so the commit-time sweep actually grandfathers pre-2026-09-01 contracts) is
  follow-on work, not this lane's write-scope.
- Open items: none blocking. The residual named in §3 (leg 7 is unconditionally armed at
  commit time until an adapter change teaches it the grandfather) is the only thing worth a
  reader's attention, and it measures zero live impact today.
- **The full suite has not run against this lane's diff yet** — per `CLAUDE.md` §4, that is
  the integrator's act at merge, once, not a per-lane one. Run it there before closing the row.

## 8. Reproduce

```bash
git log --oneline c8396f5d..HEAD
uv run --locked pytest tests/test_validate_substrate.py tests/test_batch_manifest.py -q
uv run --locked ruff check scripts/validate_substrate.py scripts/batch_manifest.py
python -c "
from pathlib import Path
from audit_checks import check_substrate_declaration as csd
print(csd.check_substrate_declaration(Path('.')))"
```

**Consumer:** `[#629]`, `[#630]`.
