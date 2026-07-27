# Conformance-branch extraction aggregate — [#434]

**Date:** 2026-07-27 · **Arc:** [#434] conformance-branch extraction pass (read-only survey; this artifact is the arc's one committed write)
**Method:** STEP 0 ref enumeration → STEP 1 seven parallel read-only probes (Haiku-pinned, `git show` only, verbatim extraction, no interpretation) → STEP 2 deterministic stdlib-only aggregation (scratch script outside the repo, not committed) → live-state classification of every survivor against `origin/main` as of `fb62c510`, each evidence command executed this session.
**Not ruled here:** the [#434] pre-registered verdict fork is the operator's; §5 states where the evidence points, labelled as observation.

---

## 1. THE SHARP TEST (answered first, per the arc brief)

**(a) Did any digest flag ARCHITECTURE.md's "ratified through ADR-103" while ADR-104 and ADR-105 existed and bound?**

**PARTIAL YES — the one-ADR-stale version only; NO digest flagged it while ADR-105 also existed.**

- The 2026-07-25 digest flagged it (S1, Med), verbatim: *"ARCHITECTURE.md:46 states 'The six chapters below are the system as built and ratified through ADR-103'"* — `docs/audits/2026-07-25-conformance-nightly-digest.md` L69; skeptic note L74: *"Evidence definitively confirmed: ADR-104 Accepted 2026-07-24, last_reviewed 2026-07-23 (one day prior), exact stale phrase on line 46, Governing ADRs section has no ADR-104 entry."*
- No digest ever mentions ADR-105 (grep across all seven digests: zero hits). Timeline: ADR-105 landed on main `f4948744` 2026-07-26 12:41 (+0200); the stale phrase was fixed by `9bd74a5f` 2026-07-26 17:30 ("currency to ADR-105 + organ Status column + Ch6 severance"). The both-ADRs-stale window was ~4h49m and contained **no nightly run** (the 07-26 nightly ran 04:24 +0200, before ADR-105 existed; the 07-27 nightly ran post-fix).
- **Adjacent miss:** at the 07-26 nightly's run time the ADR-104 staleness still held (fix came ~13h later), yet the 07-26 digest did not re-flag it. Its own summary explains why: *"Strong overall health on returning after a 42-day gap. The one persisting finding from the 2026-06-14 baseline…"* (`2026-07-26-conformance-nightly-digest.md` L47) — its delta baseline was 2026-06-14, not the 07-25 digest, which lives only on its unmerged branch.

**(b) Did any digest flag the organ map listing 31 checks while a 32nd was live?**

**NO — and no nightly ran inside a stale window.** No digest reports a 31-vs-32 mismatch. The 32nd check (`routine_consumers`) landed `bd9de975` 2026-07-26 13:00:39 (+0200) with `ecosystem/doc-counts.md` bumped 31→32 **in the same commit** ("ALL_CHECKS 31 -> 32" in its subject); ARCHITECTURE carries no literal count (moved to doc-counts per #222). Digests through 07-25 verified the count as consistent while it was — e.g. *"ecosystem/doc-counts.md '31 registered checks' matches ALL_CHECKS in scripts/audit.py (31 active) — verified"* (`docs/audits/2026-07-25-conformance-nightly-digest.md` L115) — and the 07-27 digest verified *"ARCHITECTURE.md registered check count (32) — matches ALL_CHECKS in scripts/audit.py"* (`docs/audits/2026-07-27-conformance-nightly-digest.md` L130). A clean NO with no missed window on the count claim.

**(c) Did any digest flag Ch6 describing a nightly loop whose own Action was dead?**

**NO — six digests ran inside the 18-day stale window and none flagged Ch6.** The `nightly-conformance-triage` Action was deleted `82227f08` 2026-07-08 12:36 (+0200); ARCHITECTURE Ch6 kept describing *"The nightly outcome loop (the GitHub Action that turns a cloud run into a…"* as live until the `9bd74a5f` Ch6 severance 2026-07-26 17:30. All six nightlies 07-21→07-26 ran inside that window; zero flagged it. The class was caught by the **operator lane**, not the Routine. One day after the severance, the 07-27 digest caught the sibling remnant (S1, High), verbatim: *"CONTRIBUTING.md lines 132-156 present `.github/workflows/nightly-conformance-triage.yml` as an active organ ('The repo's first GitHub Action handles the morning so the operator touches only findings')"* (`docs/audits/2026-07-27-conformance-nightly-digest.md` L58–L66) — noting ARCHITECTURE:708-710 now warns while CONTRIBUTING remains uncorrected (still true on main at `CONTRIBUTING.md:135`).

---

## 2. STEP 0 census

Enumerated live against refs after `git fetch origin` (2026-07-27, this session): **7 branches**, `origin/claude/conformance-2026-07-21` → `-2026-07-27`, one per night, no gaps; commit dates 2026-07-21 01:31:36 +0000 → 2026-07-27 03:39:58 +0000. Each carries exactly one digest at `docs/audits/<date>-conformance-nightly-digest.md`; the 07-25 branch additionally carries a 28-line JOURNAL.md entry (its own ADR-85 anchor for merge `8e2ecc8`). The prior census figure of six was wrong; the previously-verified seven is re-confirmed.

## 3. Aggregate — one row per night

Cell entries are finding ids; §4 carries each id's verbatim quote + file:line, so every non-empty cell is auditable without re-running the aggregation.

| date | raw | survived (claimed) | real defect, since fixed | real defect, still live | false positives | contested |
|---|---|---|---|---|---|---|
| 2026-07-21 | 7 | 4 | 3 (F1, F3, F4) | 1 (F2) | 0 | 0 |
| 2026-07-22 | 7 | 5 | 3 (N1, N2, N3) | 0 | 2 (N4, N5) | 0 |
| 2026-07-23 | 2 | 2 | 0 | 2 (S1, S2) | 0 | 0 |
| 2026-07-24 | 5 | 3 | 0 | 1 (N1) | 0 | 2 (N3, N2) |
| 2026-07-25 | 3 | 2 | 1 (S1) | 1 (S2) | 0 | 0 |
| 2026-07-26 | 4 | 3 | 2 (N2, N3) | 0 | 0 | 1 (N1) |
| 2026-07-27 | 7 | 2 | 0 | 2 (S1, S2) | 0 | 0 |
| **total** | **35** | **21** | **9** | **7** | **2** | **3** |

"raw" = findings before the digest's own skeptic; "survived (claimed)" = what the digest actually reports as findings; the 14 self-killed findings are not counted as claims. Classification is against `origin/main` at `fb62c510`, 2026-07-27.

**Self-check: PASS — 7 aggregate rows == 7 digests found in STEP 0; per-night raw = survived + killed holds for all rows; classified survivors 21 == survived 21.**

## 4. Per-finding evidence (verbatim quote + file:line for every cell entry)

Digest citations are `<digest path> L<lines>`; live-state evidence was executed this session against `origin/main`.

**2026-07-21** (`docs/audits/2026-07-21-conformance-nightly-digest.md`):
- **F1** (High, L59–L66, since fixed): *"ARCHITECTURE.md states deploy tool has 'four carriers' (globalconfig/plugin/precommit/floor) in five locations (lines 193, 204, 345, 500, 663) and ADR-92 Decision 8"* → real at run time; fixed `037d9f08` 2026-07-23 ("carrier count 4->5 (5 sites)"); main now has zero "four carriers" hits.
- **F2** (Med, L69–L76, still live): *"ARCHITECTURE.md states doc->code check is 'live on 12 rules' (lines 310, 385, 396)"* vs 13 entries in `ecosystem/doc-code-edge.yaml` → still on main at ARCHITECTURE.md:349/:432/:443. Recurs 07-23 S1, 07-24 N1, 07-27 S2 — flagged four of seven nights, never fixed.
- **F3** (Med, L77–L84, since fixed): *"ARCHITECTURE.md pre-commit gates list (lines 401-411) names 13 hooks as the full set"* vs 15 in config → fixed in the `037d9f08` currency lane; both missing hook names now present.
- **F4** (Low, L87–L94, since fixed): *"CONTRIBUTING.md line 114 describes ruff hook as 'language: system'"* → no such text on main; CONTRIBUTING last touched 2026-07-23.

**2026-07-22** (`docs/audits/2026-07-22-conformance-nightly-digest.md`):
- **N1** (Med, L67–L74, since fixed): *"CONTRIBUTING.md line 114 describes ruff as 'Lint gate — ruff check (version-pinned >=0.15.5, language: system). Blocks on violations.'"* → same defect as F4; fixed.
- **N2** (Med, L75–L82, since fixed, with caveat): *"CONTRIBUTING.md frontmatter `last_reviewed: 2026-07-12` but git last-commit date is 2026-07-17"* → the content-staleness compound (via N1) was real and is fixed (stamp 2026-07-23 == git date). Caveat: the 2026-07-17 git date does not hold on real main — CONTRIBUTING's last pre-run touch was `af4a1ad2` 2026-07-12, equal to the then-stamp (see §5, cloud-clone artifact).
- **N3** (Med, L83–L90, since fixed): *"ARCHITECTURE.md Ch2 'Pre-commit gates' paragraph names 13 hooks; actual `.pre-commit-config.yaml` has 15"* → same defect as F3; fixed.
- **N4** (Low, L93–L100, false positive): *"VISION.md frontmatter `last_reviewed: 2026-06-19` but git last-commit date is 2026-07-17"* → on real main, VISION's last pre-run content touch was `7e6f996b` 2026-06-19 == its stamp; the cited 2026-07-17 is `e6fa80a2`, a token-log merge that did not change VISION. The digest itself hedged *"plausible false positive by content"*.
- **N5** (Low, L101–L108, false positive): *"`docs/handoffs/README.md` frontmatter `last_reviewed: 2026-07-10` but git last-commit date is 2026-07-17"* → real main: last touch `285e5f14` 2026-07-10 == stamp; no 2026-07-17 commit touches the file. Same artifact as N4.

**2026-07-23** (`docs/audits/2026-07-23-conformance-nightly-digest.md`):
- **S1** (Med, L64–L71, still live): *"ARCHITECTURE.md states '12 rules' for the doc→code coverage_scope at lines 314, 397, and 408. contradicted — returns 13, not 12"* → same defect as F2.
- **S2** (Low, L74–L81, still live): *"every correction logged to corrections.jsonl → same mistake 2× → auto-promoted to permanent rule with verify: check (Stop hook). unsupported — session_end_backpressure.py (the actual wired Stop hook) has zero references to 'corrections'; corrections.jsonl does not exist anywhere in the repo"* → still on main at `protocols/ESSENTIALS.md:138` and `protocols/PLAYBOOK.md:3153`. Recurs 07-25 S2.

**2026-07-24** (`docs/audits/2026-07-24-conformance-nightly-digest.md`):
- **N3** (Med, L65–L71, contested): *"#292 Done-when says the gate 'refuses a bundle carrying an unfilled `fill:` marker' (whole-bundle scope); the delivered `validate_residual_completeness.py` is diff-triggered/prospective-only"* → the factual substrate is confirmed by the closing commit `9fc1a8b` itself ("the shipped gate is NARROWER than the ticket asked"); disposition contested between nights — 07-24 survived it citing ADR-81 prohibits scope-narrowing; the 07-27 digest killed the identical claim (K5) citing ADR-81(d) documented deferral + #365/#366. Not adjudicated here.
- **N1** (Low, L75–L81, still live): *"ARCHITECTURE.md states 'live on 12 rules' … but `ecosystem/doc-code-edge.yaml` has 13 entries"* → same defect as F2.
- **N2** (Low, L83–L89, contested): *"ARCHITECTURE.md (~line 422), CLAUDE.md §9 (~line 172), and CONTRIBUTING.md (~line 114) all list ruff before coherence-nudge in hook order, but `.pre-commit-config.yaml` runs coherence-nudge (line 118) before ruff (line 165)"* → the ordering facts are confirmed and unchanged on main (ARCHITECTURE.md:455-456), but prose enumeration order is not an explicit execution-order claim — whether this constitutes a defect is contested (terra doc-lane concurrence, 2026-07-27), so it is not counted as a confirmed defect.

**2026-07-25** (`docs/audits/2026-07-25-conformance-nightly-digest.md`):
- **S1** (Med, L68–L74, since fixed): the sharp-test (a) finding, quoted in full in §1 → fixed `9bd74a5f` 2026-07-26 17:30; main ARCHITECTURE.md:59 now reads "ratified through ADR-105".
- **S2** (Med, L76–L82, still live): *"ESSENTIALS.md:138 states 'every correction logged to corrections.jsonl → same mistake 2× → auto-promoted to permanent rule with verify: check (Stop hook)'"* → same defect as 07-23 S2; also cites PLAYBOOK.md:3153, still present on main.

**2026-07-26** (`docs/audits/2026-07-26-conformance-nightly-digest.md`):
- **N1** (Med, L67–L74, contested): claim that the ai-council handoff bundle merge `2a3d57b` lacks a JOURNAL merge-SHA anchor; skeptic note: *"grep is definitive (zero output). Entry 4 addendum explicitly planned this step; every other comparable main merge in the window has an anchor. No ADR documents an exception."* → still absent on main (`grep -c '2a3d57b' JOURNAL.md` → 0). But merge `2a3d57be` carried a 28-line JOURNAL.md entry, and the 07-27 digest killed same-class findings (K3/K4) citing the ADR-85 amendment *"a --no-ff merge that carries the branch's journal still anchors"*. The two nights' skeptics contradict; not adjudicated here.
- **N2** (Med, L75–L82, since fixed): *"child repos include win-tooling as part of the machine-registered set (defined by `ecosystem/<repo>/state.yaml` presence)"* (ARCHITECTURE.md:41) → zero win-tooling references in main ARCHITECTURE.md now; removed in the 2026-07-26 evening lane.
- **N3** (Low, L85–L92, since fixed): *"Layer 3 projects (machine registry) includes win-tooling"* (ARCHITECTURE.md:122) → same fix.

**2026-07-27** (`docs/audits/2026-07-27-conformance-nightly-digest.md`):
- **S1** (High, L58–L66, still live): the sharp-test (c) remnant, quoted in full in §1 → `CONTRIBUTING.md:135` still presents the deleted Action as the live morning organ.
- **S2** (Med, L69–L77, still live): *"ARCHITECTURE.md states 'live on 12 rules per the ADR-89 OQ1 naming convention (the #194 cohort-1 five + the #201 governance trio + the #202 Tier-3 quartet)' at lines 349, 432, and 443; actual `ecosystem/doc-code-edge.yaml` has 13 entries"* → same defect as F2; verified live this session.

## 5. Structural observations (aggregate-level, from the evidence)

1. **The delta chain is broken by the unconsumed branches themselves.** The 07-26 digest baselined against 2026-06-14 (*"returning after a 42-day gap"*, L47) — it could not see the 07-21…07-25 digests because they live only on unmerged branches. Direct consequence: the still-unfixed 07-25 S1 was reported "0 persisting" the next night.
2. **Every fix of a digest-flagged defect arrived via operator/session lanes, not via digest consumption.** The 9 fixed-since findings were fixed by, among others, `9a04e23c` (07-23 night-batch P4 — the CONTRIBUTING ruff-row fix behind F4 / 07-22 N1–N2), `037d9f08` (07-23 currency lane) and the 07-26 evening lane (`bd9de975`/`9bd74a5f`/`caec439d`) — lanes whose commit subjects cite their own arcs, not any conformance digest. The recurring "12 rules" defect (4 nights) and the corrections.jsonl phantom (2 nights) remain unfixed on main.
3. **Cloud-clone history artifact:** the three 07-22 stamp-vs-git-date evidences all cite a 2026-07-17 date traceable to `e6fa80a2` (a token-log merge) in the runner's clone; on real main, two of the three files' stamps matched their true last-touch dates (N4, N5 → false positives). Environment-fidelity caveat for freshness-class findings from the cloud runner.
4. **Inter-night skeptic inconsistency:** the same claim class flips between survived and killed across nights (#292 narrowing: survived 07-24, killed 07-27; JOURNAL-anchor class: survived 07-26, killed 07-27 under an ADR-85 amendment the 07-26 skeptic said didn't exist).

**Observation on the [#434] fork (not a ruling):** the evidence does not fit the "nothing beyond noise" arm — 16 of 21 claimed findings named real, evidence-confirmed defects (9 since fixed independently, 7 still live including one High), 3 more are contested rather than refuted, and the false-positive rate was 2/21 among claims (2/35 among raw, the internal skeptic having killed 14/35 before claiming). But it also does not fit the "merely unconsumed producer works" arm cleanly: on the sharp test itself the Routine caught the one-ADR staleness (a), was structurally unable to catch (b) (no run inside the window), and missed (c) six nights running while the operator lane caught it. Where it points, as an observation: the producer finds real defects but its consumption loop and its cross-night memory are the broken halves — consistent with the [#419] framing. The ruling is the operator's.

## 6. Live state that contradicted the arc brief

- The worktree branch is `worktree-434-conformance-extraction`, not `wt/434-conformance-extraction` as briefed; committed on the actual branch.
- The prior census figure of six branches was wrong; seven verified (§2).

*Probes: 7 × Haiku, read-only `git show`, no checkouts, no index writes. Aggregation script: stdlib-only, scratchpad-resident, not committed. No branch was deleted, merged, or checked out (RULING 1 and RULING 2 honored).*
