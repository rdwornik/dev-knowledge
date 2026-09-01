# DC-3 SPLIT — the ledger of what was reconstructed, what was refused, and what was measured and deferred

**Date:** 2026-09-01 · **Class:** technical · **Arc:** `[#614]` batch E · **Seat:** CC (Opus 5,
fresh orchestrator) · **Branch:** `docs/dc3-acts-two-three`

Consumed by `CLAUDE.md` §12 v2.71 and by the batch-E close packet.

---

## 1 · What this is

DC-3 (lane `worktree-lane-b-3-claude-md-genre`, single commit `6f226b34`, 9 files, +77/-223) was
adjudicated a **PARTIAL ACCEPT** by the operator on 2026-09-01. Acts TWO and THREE accepted; Act
ONE refused and re-filed as `[#628]`. This file is the ledger of the reconstruction.

**The reconstruction is act-by-act, not a revert.** A revert of Act One's hunks would have left
the lane's commit as the parent of the merge, which is exactly the shape the adjudication
refused. A fresh branch means the merged history contains the accepted acts and nothing else.

## 2 · The act split, hunk by hunk

`6f226b34` touched 9 files. The split assigns every hunk:

```
LANDED (Acts TWO + THREE)
  CLAUDE.md                                                 partial -- see below
  protocols/PLAYBOOK.md                                     partial -- new Ch3 section, TOC, carve-out
  templates/claude-regions/conventions-commit-branch.md      whole hunk (Act TWO)
  templates/claude-regions/conventions-output-formatting.md  whole hunk (Act TWO)

NOT LANDED (Act ONE, preserved as [#628]'s input artifact)
  protocols/ESSENTIALS.md                                    the 185-line deletion
  templates/child-methodology-floor.md.tmpl                  the floor edit -- a RELEASE act
  templates/claude-regions/first-read.md                     first-read item 2 removal
  templates/claude-regions/critical-rules-consistency.md     rule 6 rewrite
  templates/claude-regions/antipatterns-universal.md         the duplication bullet
```

CLAUDE.md's own hunks, split:

```
LANDED   version 2.70 -> 2.71
LANDED   section 2 critical-paths: VISION.md dropped                (Act THREE)
LANDED   section 2 Related: ObsidianVault clause dropped            (Act TWO, CUT-2)
LANDED   section 4 conventions-commit-branch region                 (Act TWO)
LANDED   section 4 file-lifecycle: VISION.md dropped                (Act THREE)
LANDED   section 4 Out-of-scope: Obsidian-vault clause dropped      (Act TWO, CUT-2)
LANDED   section 4 conventions-output-formatting region             (Act TWO)
LANDED   section 12 a v2.71 history entry, rewritten for the split
REFUSED  header blockquote "Universal rules: protocols/ESSENTIALS.md"  (Act ONE)
REFUSED  section 1 first-read region                                  (Act ONE)
REFUSED  section 5 rule 6 critical-rules-consistency region           (Act ONE)
REFUSED  section 10 antipatterns-universal bullet                     (Act ONE)
```

**Because ESSENTIALS stays, every citation of it stays.** That is the whole discipline of the
split: the four refused CLAUDE.md hunks and the ~20 PLAYBOOK citation fixes are not "correct
anyway" -- they are only correct in a tree where `protocols/ESSENTIALS.md` is gone.

## 3 · One defect fixed rather than inherited

DC-3's rewritten output-formatting bullet cites *"the Mermaid/diagram carve-out"* at PLAYBOOK
section 8 **"Output the operator copies into browser chat"**. That subsection was read end to end
before the bullet was reused: **it did not contain a Mermaid or diagram carve-out.** The lane
deleted the carve-out from `CLAUDE.md` (ADR-59; the ADR-51 amendment 2026-07-05) and pointed at a
destination that did not hold it.

This is a relocation to an unverified destination -- the precise failure the v2.69 re-genre exists
to prevent (*"every removal is a relocation to a named, verified destination"*), committed by the
lane whose whole subject was that genre. The carve-out now exists in Ch8, so the pointer resolves.
The other cited destination, Ch3 **"Branch prefixes -- the closed enum"**, is NEW in this diff and
its own forward reference to Ch8 **"Tree orchestration"** was resolved before use
(`PLAYBOOK.md:1881`).

## 4 · The `vision_md` retirement — mechanism landed, path change DEFERRED with evidence

The operator's instruction was that the same merge teaches `vision_md` and its one test a
**registry-driven RETIRED state**, and that VISION's archival is a **relocation**.

**The mechanism landed, and it needed no new registry.** DC-1 (`ea1e32a9`) had already built
`canonical_docs.CANONICAL_RETIRED = (VISION,)` and moved every registry-reading check onto it.
`check_vision_md` was the one surface that never read it -- written under ADR-33, asserting root
presence unconditionally, and `TIER_COMMIT`, so its FAIL refuses **every** commit in the repo.
`gen_handoff._vision_extract` gained the matching fallback to README's `## Vision`, which ADR-114
made the front door.

**The path change is NOT in this merge, and the reason is measured, not preferred.** Three
measurements were taken with `VISION.md` actually moved to `docs/archive/VISION.md`:

```
audit.py health                          OK -- vision_md reports n/a, the block is gone
deploy/release_lint.py --version 1.5.0   0 FAIL, 1 WARN (the pre-release tag WARN)
scripts/fleet_parity.py --run-date 2026-09-01
     .dev-knowledge  canonical-doc-vision  WARN-undeclared: SHOULD surface absent: VISION.md
```

So the gate story is clean. **What is not clean is the collateral.** A relocation done properly
re-points every live surface whose claim it falsifies, and the measured set is:

```
FALSIFIED CLAIMS -- a live doc would state something untrue
  CLAUDE.md section 5 rule 5        "VISION.md is retained ... and still tracked"
  README.md:11-12, :194             "retained and still tracked"
  ARCHITECTURE.md:482, :1195        "superseded, retained and still tracked"
  scripts/canonical_docs.py:36      "byte-identical, still tracked at the root"
  tests/test_canonical_docs.py      module docstring, the same claim
  deploy/manifest-v1.5.0.yaml:28-31 "VISION.md's ARCHIVAL IS MEASURED AND BLOCKED"
DECLARATIONS OWED
  ecosystem/parity-surfaces.yaml    canonical-doc-vision -- the WARN above is undeclared
LATENT -- silent rather than loud
  scripts/nopack_sandbox.py:226     NEVER_REMOVE holds the literal "VISION.md"; fnmatch is a
                                    full-string match, so docs/archive/VISION.md silently
                                    loses its spine protection
  scripts/consumer_at_landing.py:124 POOL_ROOT_FILES, same literal, safe-on-absence but drifts
POINTERS
  .claude/commands/handoff.md:111 · handoff-verify.md:99 · protocols/HANDOFF_BOOT.md:116
  protocols/HANDOFF_PROCESS.md:535 + :960 · protocols/DEFINITION_OF_DONE.md:148
  protocols/ENVIRONMENT.md:181 · protocols/FUNNEL_LIFECYCLE.md:260
```

**`ARCHITECTURE.md` and `README.md` are the blocker, and it is a doctrinal one.** Both are
`canonical_docs.FRESHNESS_FILES`; the `canonical_freshness` A2 gate FAILs a canonical doc edited
since its last review, so touching them requires bumping `last_reviewed` -- which in this repo
means *re-read end to end and confirmed accurate, or the drift filed*, never "touched".
`ARCHITECTURE.md` is a ~1,200-line governance surface. Stamping it without that read is the fake
stamp the operator refused eight hours earlier in ruling 6, and burying it inside a DC-3 split
merge would compound that.

**The honest shape is therefore: mechanism here, path change as `[#621]`'s first step.** The
relocation was performed, measured, and reverted (`git mv` there and back; the tree is
byte-identical). `[#621]` is *"ADR-114 option (C): the nine-repo VISION.md to README.md filename
migration"* -- the hub's own relocation is that program's step one, and the collateral list above
is its write-scope, enumerated here so the arc does not have to rediscover it.

**This is a deviation from the literal instruction and is recorded as one**, not presented as
compliance. What the instruction bought is real and permanent: `vision_md` no longer FAILs on a
ruled retirement, which was the only thing actually blocking the archival.

## 5 · Terra review — 2 passes, 3 findings, all fixed, pass 2 CLEAN

Run ad-hoc via `codex exec -c model=gpt-5.6-terra --sandbox read-only`, not `/codex-review`: the
wrapper routes a mixed `.py` + `.md` diff to the code profile and filters the prose out. Scope was
stated **inside** the focus prompt (`git diff 0f80fb4e...HEAD`) because `--base` and a prompt are
mutually exclusive, and a focus prompt is what makes the loop terminate.

```
pass  findings  disposition
1     3   HIGH  gen_handoff README fallback also masked a PRESENT-but-invalid VISION  fixed
          HIGH  test monkeypatched a possibly-wrong module namespace                  fixed, premise partly refuted
          MED   CLAUDE.md v2.71 recorded a byte count its own diff falsified          fixed
2     0   CLEAN -- "No real defects or style/design tensions to record"
```

**Tally: pass 2, the final pass -- 0 findings.** That is the final pass, not the loop total.

**The refutation, recorded as prominently as the acceptances.** Pass 1 claimed the namespace test
*"fails today"*. It did not -- the full targeted suite passed before the fix, so the two import
names resolved to one module object in this interpreter. The fragility is real and the fix stands;
the premise was wrong, and saying so is the point.

**The sharpest finding was the one the suite structurally could not catch.** The README fallback
keyed on a single `None` that meant two different things -- "file absent" and "file present,
section missing" -- so a retired-but-present `VISION.md` with a broken `## Vision` would have
served README's prose in its place. Every test reached that helper through the same door and so
confirmed the conflation rather than catching it. A three-case regression test now pins all three
branches in one predicate.

**Honest limit:** terra could not run the targeted pytest itself -- its sandbox denies `uv` cache
access. Every test result below is the seat's own run, not the reviewer's.

## 6 · Verification

```
targeted, serial (-n 0): test_claude_md_byte_cap · test_boundary_headers · test_toc ·
                         test_validate_doc_structure · test_canonical_docs      160 passed
targeted, serial (-n 0): test_audit · test_canonical_docs · test_gen_handoff    373 passed
ruff check scripts/ tests/                                                      clean
python -m scripts.toc.cli check protocols/PLAYBOOK.md                           clean
audit.py health                                                                 OK
CLAUDE.md                                                  24,282 B of a 24,576 B ceiling
```

The full suite runs once, at integration, per `[#528]` -- it belongs to the batch-E close packet,
not to this lane.
