# LANE lane-e-5-vision-relocation — relocate VISION.md out of the root with a REAL end-to-end re-read of ARCHITECTURE.md and README.md behind the stamps

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

**No-consumer:** a frozen lane contract is consumed by its DISPATCH and by the batch manifest that enumerates its slug, never by a governance-surface citation — and its filename carries no `YYYY-MM-DD` prefix, so neither `consumer_at_landing` token regex could resolve a citation even if one existed. Declared per that check's own escape.

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-e-5-vision-relocation LANE-e-5-vision-relocation.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · lane-e-5-vision-relocation · lane-e-5-vision-relocation]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-e-5-vision-relocation` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-e-5-vision-relocation` -> branch `worktree-lane-e-5-vision-relocation` -> contract `LANE-e-5-vision-relocation.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Write-scope (frozen)

- `VISION.md`
- `docs/archive/VISION.md`
- `docs/archive/README.md`
- `README.md`
- `ARCHITECTURE.md`
- `CLAUDE.md`
- `scripts/canonical_docs.py`
- `scripts/nopack_sandbox.py`
- `scripts/consumer_at_landing.py`
- `tests/test_canonical_docs.py`
- `ecosystem/parity-surfaces.yaml`
- `deploy/manifest-v1.5.0.yaml`
- `protocols/DEFINITION_OF_DONE.md`
- `protocols/ENVIRONMENT.md`
- `protocols/FUNNEL_LIFECYCLE.md`

**This IS the collateral set**, measured and enumerated at
`docs/audits/2026-09-01-technical-dc3-split.md` §4 rather than rediscovered here. It is
deliberately NOT the whole set that file lists: `protocols/HANDOFF_PROCESS.md`,
`protocols/HANDOFF_BOOT.md` and the two `.claude/commands/handoff*.md` files carry VISION
pointers too, and they belong to **lane-b-2**, which is rewriting them for v7 in the same
batch. Two lanes writing one file is a merge conflict the batch has already decided to have
(`substrate-lane-write-scope-disjoint`), so those four move there and this scope stays
disjoint. Their pointers are stale TODAY, independently of this relocation.

## Done-contract (immutable)

1. **`VISION.md` is RELOCATED, not deleted, and the destination is `docs/archive/VISION.md`.**
   `git mv`, byte-identical, so `git log --follow` resolves in one hop and ADR-114 option (C)'s
   nine-repo program can move it again in a single act. `docs/archive/` is an admissible home
   under the hermetization gate (Rule C's `docs/audits/*`-style home allowlist carries
   `docs/archive`), and Rule B's audit-filename grammar does NOT reach it — that rule applies
   only to direct children of `docs/audits/`. If the lane finds a ruled destination that
   contradicts this, that is escalation class (b), not a silent substitution.
2. **EVERY falsified claim in the write-scope is re-pointed, and the two FRESHNESS files are
   re-read END-TO-END before their stamps move.** `ARCHITECTURE.md` (~1,203 lines) and
   `README.md` both state VISION is *"retained and still tracked"*, and both are
   `canonical_docs.FRESHNESS_FILES`: the A2 gate FAILs a canonical doc edited since its last
   review, so `last_reviewed` MUST move — and in this repo that means *re-read end to end and
   confirmed accurate, or the drift filed*, never "touched". **This is the entire reason the
   relocation was deferred out of the DC-3 split rather than rushed into it.**
3. **The read is delegated, the STAMP is not.** Sonnet workers read `ARCHITECTURE.md` and
   `README.md` end to end and report what they found; opus adjudicates whether each stamp is
   earned and writes the per-document review record naming what the read found. A stamp with no
   record of what was reviewed is the fake stamp operator ruling 6 refused on 2026-09-01.
4. **The two LATENT sites are fixed, not just the loud ones.** `scripts/nopack_sandbox.py:226`
   holds the literal `"VISION.md"` in `NEVER_REMOVE` and matches by `fnmatch` full-string, so
   `docs/archive/VISION.md` would silently lose its spine protection;
   `scripts/consumer_at_landing.py:124` carries the same literal in `POOL_ROOT_FILES`. Both
   should read the registry rather than a literal.
5. **The parity WARN is DECLARED, not left undeclared.** With VISION moved, `fleet_parity`
   reports `.dev-knowledge canonical-doc-vision WARN-undeclared: SHOULD surface absent`. The
   `canonical-doc-vision` row gains the declaration; the eight consumers that still carry
   `VISION.md` are untouched, because relaxing a SHOULD cannot red a member.
6. **`deploy/manifest-v1.5.0.yaml`'s archival note is corrected.** It records the archival as
   *"MEASURED AND BLOCKED"* on a `vision_md` FAIL that no longer exists — the check learned the
   registry-driven RETIRED tier on 2026-09-01.
7. `audit.py health` exits OK and `deploy/release_lint.py --version 1.5.0` stays at 0 FAIL. Both
   were measured GREEN with the file already moved, so a regression here is this lane's, not
   inherited.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. Re-read `ARCHITECTURE.md` and `README.md` END TO END (delegate the reading, adjudicate the
   stamp) and write the per-document review record. Do this BEFORE the move, so the stamp is a
   review and not a consequence. **COMMIT**
2. `git mv VISION.md docs/archive/VISION.md`, then re-point every falsified claim in the frozen
   scope in the SAME commit — a tree that states something untrue between two commits is the
   defect this ordering avoids. **COMMIT**
3. Fix the two latent literal sites, declare the parity row, correct the v1.5.0 archival note.
   Re-measure `audit.py health` and `release_lint --version 1.5.0`. **COMMIT**
3. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
