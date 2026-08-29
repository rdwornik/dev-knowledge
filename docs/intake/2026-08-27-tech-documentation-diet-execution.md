---
intake-id: 57
status: READY
origin: cloud night batch C1 (Dispatch-Cloud, 2026-08-26, `.dev-knowledge` @ d8211b0, read-only), harvested and ruled 2026-08-27 in the night-harvest consumption ledger section B (I-DOC); architect ruling X7
consumers: "`docs/audits/2026-08-27-technical-doc-diet-plan.md` (the landed C1 report, this intake's evidence); the `[#569]` 19-finding census at `docs/audits/2026-08-20-technical-playbook-status.md` item 3; PLAYBOOK, ESSENTIALS and ARCHITECTURE as the three edited surfaces; STANDING_RULINGS section X7"
---

# The doc diet has a fixed first step — the mechanical correction, before any structure moves

## Problem / motivation

`protocols/PLAYBOOK.md` is 5208 lines. It is the largest governance surface in the hub, it is
consulted on demand rather than at boot, and the `[#569]` census found **19 distinct defects** in
it — dead pointers, contradicted version pins, a command table that lists 7 where disk carries 8,
two unresolved `[TBD]` markers, and a **hard-coded absolute secrets path written into a governance
document**. `[#569]` closed 2026-08-26 with that census explicitly **not discharged**.

Separately, the same surfaces are candidates for a structural diet: PLAYBOOK Ch2 restates
CLAUDE.md's own section model, ESSENTIALS carries four sections that could point rather than
restate, and ARCHITECTURE carries prose rosters that CLAUDE.md §4's M2 rule already forbids.

**The two are not independent, and the order is not free.** C1's measured finding, adopted as
ruling **X7**: the purely mechanical correction discharges **17 of the 19** census findings without
moving a single heading. A structural pass run first relocates the very lines those corrections
target, and the corrections are then silently discarded — the census would read as "addressed" when
nothing was fixed. This intake exists to make that ordering a filed requirement rather than a
remembered one.

The secrets path is the part that should not wait for any diet at all: PLAYBOOK's "Secrets storage
path" section hard-codes a live absolute path under an operator home directory, behind a `[TBD]`
that mis-points at ADR-33 (ADR-33 is VISION universalization, not secrets). Its sibling `[TBD]` one
section down points at ADR-34, which was **Accepted 2026-04-29** and already answers it.

## Scenarios (+1 view)

- As the operator I open PLAYBOOK to check a convention, and the section I land on cites a line
  number that rotted two waves ago, or a Claude Code version pin the same file contradicts twice
  elsewhere. I cannot tell which of the three numbers is live, so I verify by hand — every time.
- As an executor I am told to "run the doc diet". I start with the biggest win (structure), move
  Ch11 and section 5 to their canonical homes, regenerate the TOC, and land it green. The 19 census
  findings are now in different files at different line numbers, and nobody will ever reconcile
  them. The census reads discharged; nothing was corrected.
- As a reader of a governance doc I find an absolute filesystem path to a secrets store. That path
  is not itself a secret, but publishing the location of one in the fleet's most-copied protocol
  file is a habit the fleet should not carry, and the file is a deploy-carried surface.

## Functional requirements

- **Must:** the mechanical correction lands **before** any structural relocation (X7). The
  hard-coded secrets path is deleted in the first doc act of the consuming arc, not deferred to the
  diet. Every one of the 19 census findings is dispositioned individually — corrected, re-anchored,
  or recorded as already-moved — never in aggregate.
- **Must:** `H6`–`H12` are re-anchored as **heading/symbol** citations carrying no bare line
  numbers, so the same rot cannot recur in the same place. This is CLAUDE.md's own M1/M2 discipline
  applied to the file that violates it most.
- **Must:** `PLAYBOOK.md:3700` stays **byte-identical** — it is a `provider-registry-agreement`
  gate seam, and rewording it trips a live pre-commit gate.
- **Should:** the H13/H15 handoff v5 to v6 re-stamp runs through the `check-against-spec` skill,
  with all 11 sites individually verdicted in the re-stamp commit message and the
  `templates/handoff/v5/` path explicitly recorded as out of scope.
- **Should:** ARCHITECTURE's Organ map and Validators inventory become pointers to
  `ecosystem/organ-index.md` and `ecosystem/doc-counts.md` (W2/D5), restating no count or roster in
  prose.
- **Could:** the human-facing diet — PLAYBOOK Ch11 relocated to ARCHITECTURE Ch3, section 5 to
  `AI_COUNCIL_PROCESS.md`, each leaving a one-line pointer; ESSENTIALS' four pointerisable sections
  point rather than restate.

## Acceptance criteria (ex-ante)

1. No absolute operator-home path remains in PLAYBOOK's Secrets-storage section, and the
   `[TBD — Stream C session 3, ADR-33]` marker is either re-pointed at a live decision or retired
   with a recorded reason.
2. The `[TBD — ADR-34]` marker in "Capitalization conventions" is replaced by a pointer to ADR-34,
   mirroring the correctly-pointerised sibling in the same file.
3. All 19 census findings from `docs/audits/2026-08-20-technical-playbook-status.md` item 3 carry a
   named per-finding verdict in the correcting commit's message.
4. No bare line number remains in the re-anchored `H6`–`H12` citations.
5. `protocols/PLAYBOOK.md:3700` is byte-identical to its pre-arc content, proven by a `git diff`
   showing the line unchanged; `provider-registry-agreement` passes.
6. The `toc-freshness-playbook` hook is green in the same commit as every heading act.
7. `uv run --locked pytest -x --tb=short` green; `uv run --locked ruff check` clean.

## Non-goals

- **`CLAUDE.md` is out of scope entirely** (R-F2): it is a Form-A fleet-parity surface whose hub
  regions are byte-matched to `templates/claude-regions/*`, so an edit there is a lockstep fleet
  act, not a diet act.
- Not in scope: `.claude/generated/*`, `ecosystem/organ-index.md`, `ecosystem/doc-counts.md`, and
  the ARCHITECTURE `CODEMAP` region — all generated, all regen-gated.
- Not a token budget. C1's ~955 / ~30 / ~270 line figures are **line counts**, and a pointerised
  line is cheaper than a prose line by more than 1:1, so they understate the saving and must not be
  quoted as a target.
- No structural relocation is authorised by this intake on its own — the Could tier above needs its
  own ratification.

## Impact sketch (4+1 lite)

- **Logical:** three canonical surfaces (PLAYBOOK, ESSENTIALS, ARCHITECTURE) converge on
  pointer-over-restatement; no new organ.
- **Process:** the diet becomes a **sequenced** arc with a named first step, not a single sweep.
- **Development:** doc-only for the mechanical half; the structural half touches `doc_code_edge`
  rule tokens and needs all 14 to still resolve.
- **Physical:** none — no new file class, no new directory, no deploy change.

## Open questions

- Is the "Secrets storage path" section worth **keeping at all** once the path is deleted? It has
  been a `[TBD]` since Stream C and no ADR has claimed it; retiring the section may be honester
  than re-pointing it. Recorded, not answered here.
- Does the structural half (Ch11 / section 5 relocation) need its own intake, given it changes what
  PLAYBOOK *is* rather than what it *says*? C1 proposed it as one arc; this filing does not decide.
- R3's ARCHITECTURE work overlaps `[#569]`'s successor surface and the M2 rule in CLAUDE.md
  section 4 — whether that is one row or two is a technical-architect call.

## Status

READY — filed 2026-08-27 from the night-harvest consumption ledger section B. Ruling X7 (sequencing)
already taken; the first act is the mechanical correction, including the secrets path.
