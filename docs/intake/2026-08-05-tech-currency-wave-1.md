---
intake-id: 24
status: DRAFT
origin: outgoing 2026-08-02→04 seat, operator-directed consolidation 2026-08-05; landed verbatim by the sealing architect's instruction
consumed-by:
---

> **Intake note:** Landed **verbatim** from PART B of the outgoing seat's two-part package.
> PART A of that package is chat-lane challenge material and is deliberately NOT landed
> here (operator ruling, 2026-08-05). Body unedited below — `status: DRAFT`, non-citable
> until ingested; the repo wins on conflict. **No rows are born by this filing.**

# PART B — INTAKE DRAFT: tech-currency wave 1 — buy the commoditized walls
*(functional mode — WHAT/WHY; the receiving architect triages, decides ADR-vs-rows, and
sequences under plan-governs. Library-first bar applies to every candidate: adoption follows a
MEASURED divergence on this repo, never this list's authority. Provenance: outgoing-seat
industry-standard assessment, 2026-08-05, operator-directed consolidation.)*

## WHY (the objective gap this intake closes)
Independent assessment: the fleet is AHEAD of industry standard on LLM-ops discipline and
decision traceability, BEHIND on exactly one axis — **all hard enforcement is client-side**.
Evidence: zero CI on the suite (verified); the night batch ran 4× `--no-verify` when a container
carried the wrong toolchain; a fresh clone is ungated until hooks are installed; the scheduled
fleet-baseline task was silent 10+ days with nothing noticing. Everything below is a
commoditized, mostly free remedy. Strategy: buy what is commoditized; keep building only the
LLM-ops layer that is the fleet's actual edge.

## WHAT — candidates, priority-ordered by value

**P1 — GitHub Actions as the second wall (the single biggest move).**
Workflow on push/PR to `main`: `uv sync --locked` (cached) → `pytest` → `audit.py health` →
the JOURNAL-anchor backstop. Closes: `--no-verify`-without-trace (server records RED regardless),
fresh-clone gap, wrong-toolchain bypass. Budget fits free tier (~120 merges/mo × ~6 min ≈ 720 of
2000 min; repos stay PRIVATE — employer material). **Open verification item:** on private repos,
*enforcing* required-checks/branch-protection may need the Pro plan — verify current pricing;
even report-only mode is a server-side, tamper-proof record (the backstop's twin, out of local
reach). Precedent exists: the nightly-triage Action (fail-closed parser, diff-guard).

**P2 — scheduled runs + dead-man's switch (resolves B-2 by replacement, not repair).**
`schedule:` cron replaces the silent Windows Task Scheduler; a second tiny job opens an Issue
when a nightly run left NO trace. Absence-of-run stops being invisible — the "green by absence"
class, mechanized. Fold the B-2 investigation into this: why fix a scheduler we can retire.

**P3 — `gh` CLI: findings-as-Issues (closes the loop's one manual pump).**
Every organ's finding files as a labeled Issue (`gh issue create`) instead of parking in branch
files; `surface_triage.ps1` already reads Issues at session start — the consumer exists. Also:
`gh run view --log` gives CC self-diagnosis of red CI without the operator as log courier;
`gh pr create/merge` plugs into the serial gate rather than around it. Rule to carry: a finding
cannot die except by an explicit verdict.

**P4 — `mutmut` (mutation testing): highest-leverage library on the list.**
The vacuous-test class cost ~6 hand-caught findings in one window; mutation testing is the
industry's MECHANICAL answer — an empty test becomes a number, not a reviewer's insight. Pilot
scope: the enforcement organs' test files first (where a vacuous test is most expensive).
Measured-divergence bar: mutation score on current suite, before any doctrine changes.

**P5 — CONTRIBUTING.md currency (doc-truth, S-size, already specified).**
Four stale claims post-ADR-85: §Definition-of-done describes the RETIRED Stop-hook/override
model; `block-ff-push` listed "fail-soft" (now fail-closed, FR6); the two new organs
(check-seal-identity, block-unanchored-push) absent from the hook table; ADR-82/88/89 carve-outs
still "frozen Proposed" (flipped 2026-08-04). Mechanism candidate in the same row: the hook
table becomes a regen-and-diff surface against `.pre-commit-config.yaml` (ends the class, not
the instance). Verify DEFINITION_OF_DONE.md for the same drift.

**P6 — evaluation-gated candidates (adopt ONLY on measured divergence):**
- `vale` — prose linting by config; candidate to absorb part of silent-rule-ratchet/doc_claims
  IF a measured overlap exists. The recorded tension (ecosystem/*.yaml explanatory prose
  tripping the ratchet twice) is the test case.
- `commitlint`/`gitlint` — commit-convention engine; our `closes [#id]` / kill-candidates rules
  become plugins instead of whole scripts IF the plugin API carries them without loss.
- `lychee` — dead links/pointers in markdown (the broken-pointer class caught by hand twice).
- Copilot free tier — NOT a standing review lane (quota); use as the free test channel for the
  Grok acceptance (Grok 4.5/4.6 in Copilot's picker) per the 2026-07-25 model rulings.
- `towncrier`/`git-cliff` — **LEAVE**: JOURNAL is narrative, not a release list; revisit only
  if a release-notes surface is ever wanted.

## Sequencing note (for the receiving architect, not binding)
P1+P2 are one arc (same workflow file family, same verification of GitHub plan limits). P3 rides
next (it changes how every later organ reports). P4 is independent and TDD-shaped. P5 is an
S-row any gap-week absorbs. P6 items each need their measured-divergence run before any adoption
decision — natural Gemini/luna fan-out material for the measurement, architect for the verdict.
§F honesty: this intake births ~5-6 rows; the compensating close engine is the 139-proposal
consumption (FR-8a class) — sequence accordingly, never file-without-close-capacity.

## Do-not-relitigate carried into this intake
Renovate (rejected at current scale — L4 lane owns the revisit trigger) · PyDriller (L5a runs on
own frames) · Backlog.md as engine (pattern donor only) · public repos for free CI minutes
(employer material — repos stay private).
