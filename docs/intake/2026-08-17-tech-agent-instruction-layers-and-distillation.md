---
intake-id: 35
status: DRAFT
origin: browser research artifact wf-50111a08, commissioned + landed 2026-08-17; converted to intake by lane R (unrostered, running alongside batch 7a)
note: Sections A-D are required by the lane-R contract of record (docs/audits/2026-08-17-technical-research-intake-lane-contract.md section 1). All eight ADR-98 template sections are present and carry them; Section C is the one added top-level section, because a doctrine-delta is neither a requirement nor an open question.
consumers: the technical-architect triage; no ADR and no backlog row has been born from this doc
---

# Portable agent-instruction layers, prompt distillation, and unattended runs

## Problem / motivation

This repo's instruction surface is at its declared ceiling and is single-vendor by
ruling. `CLAUDE.md` is pinned to a 200-line budget (ADR-53) and its own §12 v2.62 entry
records that the last edit "landed the file exactly ON 200/200", forcing two older history
bullets into git to buy 2 lines of headroom. At the same time the fleet is not
single-vendor in practice — `/codex-review` and the `codex` audit class are live, and the
branch-prefix enum admits `claude/<slug>` cloud lanes. The memo argues the ceiling is real
but the *response* is wrong: shrink the always-on prose by moving enforceable invariants
into mechanisms, and make the remaining prose portable across vendors instead of
re-authoring it per tool. It also supplies the measured basis for why a crowded
instruction file degrades rather than merely costs tokens.

**This is the second independent memo to reach the AGENTS.md recommendation.** The first is
`docs/archive/2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md` ("AGENTS.md as
the one portable layer, `@AGENTS.md` import for Claude Code, generation-plus-checksum over
symlinks on Windows"). Two independent commissions converging on a recommendation that
`CLAUDE.md` §10 lists as an **anti-pattern** is the reason this doc exists rather than
being filed as a note.

### Section A — the artifact's own TL;DR, quoted

> - **Build on AGENTS.md as your one canonical instruction file** — an open standard stewarded by the Linux Foundation's Agentic AI Foundation, "read natively by Codex, Cursor, Copilot, Gemini CLI, Aider, Windsurf, Zed, Factory, Jules, and over 20 other tools… adopted by more than 60,000 repositories." Keep it under ~30 always-on lines and make every other vendor file (CLAUDE.md, GEMINI.md, copilot-instructions) a generated or pointer file to it — a "lane-role → model" swap then becomes a one-table edit plus a regenerate step, not a rewrite.
> - **Distillation is real and measured** (LLMLingua reaches up to 20× compression with GSM8K Exact-Match dropping only 1.44 and 1.52 points at 14× and 20×; Anthropic Agent Skills load ~80–100 tokens/skill until activated), but the durable win is moving hard rules OUT of prose into mechanisms (hooks, linters, tests, CI gates) — instruction-following measurably degrades under load (Distyl AI's IFScale: "even the best frontier models only achieve 68% accuracy at the max density of 500 instructions"), so a prompt should carry judgment, not enforceable invariants.
> - **Unattended runs are buildable this week** with Claude Code headless (`claude -p`), the official `anthropics/claude-code-action@v1` on cron, and git worktrees for isolation; 3–6 concurrent agents is the real (review-bound) sweet spot, and moving off a Windows laptop onto GitHub Codespaces ("compute fees starting at $0.18/hr and storage fees at $0.07/GB per month") or a rented VPS is cheap — the gotchas are locking, secret handling, and pinned toolchains, not price.

## Scenarios (+1 view)

- **As the operator I** hit the `CLAUDE.md` 200-line wall again on the next roster row, **and
  then** instead of condensing another history bullet into git, I ask which lines in the file
  are *enforceable invariants* — and move those to gates, freeing budget structurally rather
  than cosmetically.
- **As the operator I** dispatch a lane to Codex for review, **and then** discover it read a
  different instruction file than the Claude lane did, so the two lanes were never held to the
  same rules — a divergence nothing currently detects.
- **As the operator I** shorten an instruction file to buy budget, **and then** have no way to
  tell whether the shortened version still enforces what the long one did, because no eval
  exists that tests rule-adherence rather than output quality.

### Section D — the smallest first build the artifact names

Quoted from the memo's own "The Smallest First Build":

> - **Q1 (portable layer):** In your hub repo, write one **AGENTS.md** (≤30 lines: build/test commands, boundaries, PR rules) + a one-line **`CLAUDE.md` = `@AGENTS.md`** + a **`.gemini/settings.json`** with `context.fileName: ["AGENTS.md"]`. That single trio makes Claude Code, Codex, and Gemini read the same rules today, Windows-safe.
> - **Q2 (distillation):** A **10-case `promptfooconfig.yaml`** encoding your non-negotiable behaviors, run as `npx promptfoo eval` original-vs-distilled with a ~95% pass gate — the minimum that proves a shorter instruction set still enforces the rules.
> - **Q3 (night run):** One **`.github/workflows/nightly.yml`** using `anthropics/claude-code-action@v1` on `cron`, with a scoped `--allowedTools`, `timeout-minutes`, and branch protection on `main` — one scheduled, guard-railed, unattended agent run you can watch succeed before you scale to a worktree fleet.

**Q1 is not buildable here without first resolving R1 below** — it is the exact act
`CLAUDE.md` §10 names as an anti-pattern. Q2 and Q3 carry no such conflict.

## Functional requirements

### Section B — the decisions this would force on THIS repo

Five proposed rows. **NOTHING BELOW IS BORN.** No `BACKLOG.md` line, no `tasks/` file, and no
id is consumed by this document; lane R holds no reserved id block. These are titles, testable
Done-whens, and proposed kill-candidates lines offered to the technical-architect triage.

```
PROPOSED ROW R1 - Rule on AGENTS.md: two memos vs ADR-53's single-instruction-file rule
  Done-when: an ADR exists with status Accepted that either amends ADR-53 to admit
             AGENTS.md as a canonical layer or records the refusal with a stated reason,
             AND CLAUDE.md section 10's "AGENTS.md is retired" line agrees with it
             (grep -c "AGENTS.md is retired" CLAUDE.md reflects the ruling either way).
  kill-candidates: none -- this is a fork ADR-53 left open, not new scope

PROPOSED ROW R2 - Mechanize-not-prose pass over the always-on instruction surface
  Done-when: a committed audit lists every CLAUDE.md + CLAUDE-FLOOR.md line, classifies
             each as judgment (stays prose) or enforceable invariant (owes a gate), and
             names the existing gate or the gap for every line in the second class;
             the count of unclassified lines is 0.
  kill-candidates: none -- no existing row covers instruction-surface classification

PROPOSED ROW R3 - Rule-adherence eval harness (promptfoo + seeded-defect corpus)
  Done-when: `npx promptfoo eval` runs >=10 cases encoding non-negotiables from
             ~/.claude/rules/core-invariants.md and exits non-zero below a declared
             threshold; a deliberately-weakened instruction set FAILS the run.
  kill-candidates: overlaps the seeded-defect-corpus spec already gating [#491]/[#492]
             (docs/archive/2026-08-09-research-agent-telemetry-model-comparison-wf-02c940ef.md)
             -- propose FOLDING into that corpus rather than birthing a second one

PROPOSED ROW R4 - Always-on instruction budget, measured across the fleet
  Done-when: a script emits per-repo always-on line + byte counts (CLAUDE.md, the
             hash-guarded floor, .claude/rules/**) and exits non-zero when any repo
             exceeds its declared ceiling; the hub's own 200-line budget is one row of
             its output rather than a separately-hand-checked number.
  kill-candidates: absorbs the manual `file-budget CLAUDE.md#size` doc_rot check into a
             fleet-wide instrument -- propose retiring the hand-check if superseded

PROPOSED ROW R5 - Codex 32 KiB silent-truncation guard
  Done-when: a check computes the combined size Codex would read (~/.codex/AGENTS.md +
             repo-root + cwd) and FAILS above 32 KiB, so truncation is refused rather
             than silent.
  kill-candidates: none -- no current check reads the Codex instruction path at all
```

- **Must:** rule on R1 before any AGENTS.md file is created — the memo's Q1 first build is
  currently a doctrine violation here, and building it silently would be the failure mode
  `CLAUDE.md` §10 exists to prevent.
- **Should:** R2 and R3 — both are budget-structural rather than cosmetic, and R3 is the only
  proposal here that can *prove* a shortened instruction set still enforces what it replaced.
- **Could:** R4 and R5 — real gaps, but neither is load-bearing until the fleet actually runs
  multi-vendor.

## Acceptance criteria (ex-ante)

1. A reader can determine, from a committed artifact, whether AGENTS.md is admitted or refused
   in this fleet — and `CLAUDE.md` §10 does not contradict that answer.
2. No instruction line claimed to be enforced is enforced only by prose: every line classified
   as an invariant in R2 names a gate or names its absence.
3. A distilled instruction set is never adopted on assertion. Adoption requires an eval run
   whose deliberately-weakened control FAILS.
4. Codex-side truncation cannot happen silently.

## Non-goals

- Adopting `rulesync`, `agentsync`, or any generator CLI. The memo itself ranks the
  `@import`/pointer pattern as sufficient below two vendors and >1 repo.
- Symlinks. The memo flags them as breaking on Windows without Developer Mode, and the
  2026-08-09 portability memo independently reached generation-plus-checksum instead — which
  is what the hash-guarded floor (`floor-hash-verify`, ADR-78/93) already implements.
- LLMLingua-style token compression of this repo's instruction files. The memo's own caveat is
  that its benchmarks measure QA/reasoning, not rule-adherence.
- Any change to `CLAUDE.md`, `protocols/`, or an ADR by this document. This is a DRAFT intake.

## Section C — what this supersedes or contradicts in current doctrine (locators)

**CONTRADICTS — head-on, and this is the whole reason the doc is filed:**

- `CLAUDE.md` §10, anti-patterns list: *"**Narrating or managing AGENTS.md** — AGENTS.md is
  retired (ADR-53); CLAUDE.md is the single instruction file"*. The memo's central
  recommendation is the named anti-pattern. Two independent commissions now recommend it
  (this one and `docs/archive/2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md`),
  which makes it a fork to rule on rather than advice to decline silently.
- `CLAUDE.md` §4 conventions + ADR-53: the 200-line budget vs the memo's "~20–30 line root
  file". Same direction, but ~6.7× apart in magnitude. The memo's supporting claim is
  stronger than a style preference: per its cited Morph guide, LLM-generated AGENTS.md files
  "reduced success rates by 2% and increased cost by 23%, primarily because they duplicated
  content already available in the repository."

**CONFIRMS existing doctrine (recorded so the confirmations are not mistaken for new asks):**

- *"rules that are deterministic, safety-critical, or verifiable should be mechanisms, not
  prose"* is `CLAUDE.md` §5 rule 7 already: *"No executable rules in this repo — those go in
  `~/.claude/` with `verify:` lines"*. The memo supplies the measured basis (IFScale: 68%
  adherence at 500 instructions) the existing rule asserts without one.
- *"never push to main = a mechanism, not a prompt"* is core-invariant #5 plus `block-ff-push`
  and `block-commit-on-main` (`CLAUDE.md` §9). Already built, on the memo's recommended shape.
- Progressive disclosure via Skills matches `.claude/skills/` (`CLAUDE.md` §8).

**CURRENCY — a repo-local fact the memo corroborates:**

- The memo cites GitHub issue **#6235** (the open "Support AGENTS.md" request, Anthropic
  declined). `docs/audits/2026-08-17-technical-batch-7a-manifest.md` independently excludes
  `[#6235]` from the backlog id space as *"a GitHub issue number, not a backlog id"*. Both
  refer to the same issue — worth noting so a future reader does not treat the collision as
  an id defect.

**UNRESOLVED TENSION, not a contradiction:**

- The memo recommends `claude -p` / `claude-code-action@v1` on cron for unattended runs. The
  nightly proposal loop here is explicitly **not live**, "gated on the load-gauge landing
  first, per standing operator ruling" (`docs/intake/README.md` §8). The memo does not know
  about that gate; adopting Q3 would need the ruling revisited, not bypassed.

## Impact sketch (4+1 lite)

- **Logical:** potentially re-seats the canonical instruction file — the single largest
  doctrine change any of these five memos proposes.
- **Process:** R2 changes how instruction-file budget pressure is relieved (structurally, not
  by condensing history).
- **Development:** R3/R5 add checks; R1 adds an ADR and touches no code.
- **Physical:** untouched unless Q3's cron runner is adopted, which R1 does not require.

## Open questions

1. Does ADR-53's "single instruction file" ruling forbid *AGENTS.md specifically*, or forbid
   *two files that both carry content*? A one-line `CLAUDE.md` = `@AGENTS.md` pointer arguably
   satisfies the second reading and violates the first. This is a technical-architect
   question about the ruling's intent and is deliberately not answered here.
2. Is the `.claude/CLAUDE-FLOOR.md` hash-guarded replica model (ADR-78/93) already the
   "generation-plus-checksum" pattern the memo recommends, such that adopting AGENTS.md would
   mean re-pointing an existing mechanism rather than building a new one?
3. What is the actual live Codex instruction size? R5 assumes it is under 32 KiB; nobody has
   measured it.
4. Does the load-gauge ruling that gates the nightly loop also gate a cron-driven
   `claude-code-action` run, or is that a different class of unattended run?

## Cross-links to the four sibling intakes landed in the same arc

- **[#36] `2026-08-17-tech-repository-autonomy-and-gate-liveness.md`** — strongest overlap.
  This doc's "move invariants out of prose into mechanisms" and #36's policy-as-code /
  gate-liveness thesis are the same claim from two directions: #35 says *what should leave the
  prompt*, #36 says *what the receiving gate must prove about itself*. R2 hands its
  invariant-class output straight to #36's negative-control harness.
- **[#37] `2026-08-17-tech-machine-verifiable-done-when.md`** — R3's eval harness and #37's
  held-out verifier are the same instrument at different altitudes: both refuse self-report as
  evidence. #37's mutation-testing recommendation is what would catch an R3 corpus whose cases
  assert nothing.
- **[#38] `2026-08-17-tech-fleet-config-standardization.md`** — if R1 admits AGENTS.md, its
  distribution to N repos is exactly #38's problem, and #38's finding that Python config
  cannot import from a package (only be *copied*) applies to instruction files too. R4's
  fleet-wide budget instrument is a rule in #38's conformance checker.
- **[#39] `2026-08-17-tech-off-machine-agent-substrate.md`** — this doc's Q3 (unattended runs,
  3–6 concurrent sweet spot, rate limits binding before hardware) and #39's substrate plan are
  the same subject; #39 is the priced, verified-August-2026 version and **its Hetzner figures
  supersede this memo's**, which are the pre-June-repricing ones. Prefer #39 on any pricing
  claim.

## Status

**DRAFT** — landed 2026-08-17 by lane R, unratified. Not operator-approved; per
`docs/intake/README.md` §6 the confirm-gate has not been cleared. Zero rows born; five
proposed. The AGENTS.md question (R1) is the one item here that cannot be built around.

**Prep pass, 2026-08-21 (batch-1 lane D).** Completeness pass run against
`docs/intake/README.md` §2–§5 and `templates/intake-template.md`: **conformant, no fixes
required.** All eight template sections present (Section C is the one added top-level
section, per the lane-R contract of record); frontmatter on-schema — `note:` and `consumers:`
are optional descriptive keys ratified at the [#398] deploy, and no companion field appears
out of its status; naming conformant (`tech` infix, origin date). **Status deliberately
untouched:** this doc is one of the three carrying an unruled doctrine fork (here, R1 —
AGENTS.md against `CLAUDE.md` §10 and ADR-53) and is held for the architect's R7 ADR-fork
ruling. The fork options and their consequences are laid out for that ruling in the lane
artifact `docs/audits/2026-08-21-technical-lane-rat-intake-ratification.md`.
