# 04 · What just happened

A narrative of recent work on `.dev-knowledge`, written so a chat with zero prior
context can pick up the thread. Prose, not a log dump.

## The arc

The last few days (2026-05-26 → 2026-05-30) were a **multi-day ecosystem
consolidation arc** whose closing chapter is a self-referential story: the **handoff
process tested itself end-to-end three times in 24h — v4.1 → v4.2 → v4.3 — each
cycle catching what the previous missed.** That convergence loop is the single most
important thing to understand here; the rest is detail.

The disease being treated was **multi-surface fragility**. The prior handoff process
(v3.4) was retry-ready but over-engineered (13–14 hand-maintained files, multi-stage
ratification). Its first real end-to-end test **aborted at Stage 3** when the
architect produced a fabricated claims structure — the operator chose ABORT over
shipping UNVERIFIED. An empirical process audit then returned **13 findings** (2
critical), and the meta-observation (§7) named the structural disease: when audit
findings cluster, **the cluster IS the diagnosis** — patching the bug list leaves
the next 13 inevitable. That insight drove the **v4 redesign**: collapse 13–14 files
to **8**, multi-stage to **two-phase**, hand-maintained to **generated-from-source**,
with a **sage→apprentice** teaching frame.

v4 then iterated under its own methodology. **v4.1** (first end-to-end run; bundle at
`docs/handoffs/2026-05-29-dev-knowledge-session/`, merged) — Phase 2 verification
caught two live drifts (an aborted-folder "preserved" claim that was actually
deleted; a corp-monorepo branch the operator thought merged but wasn't). Insider deep
review found 7 refinement issues, no architectural defects. **v4.2** (branch
`fix/handoff-v4.2-refinements-and-rerun`) added the four-tag sage discipline, an
always-emit verification table, the moved-up README drift section, and version
stamps. Its bundle was re-run and reviewed — and here the key empirical result
landed: the **insider review (the sage itself) caught only 1 of 4 critical findings**
that an **independent fresh-eyes Opus 4.8** (zero project context) then caught. **The
curse-of-knowledge was confirmed: the insider sees scaffolding; the outsider sees the
user experience.** That is why triangulation is now non-optional.

**v4.3** (branch `feat/handoff-v4.3-comprehensive-close`, 8 commits, merged to `main`
at `5a5ab83`) closed all 14 fresh-eyes findings + the architectural meta-question. It
inlined the four-tag definitions in `04_RECENT` (C1/C2), added the §3.1→Amendment-A
cross-reference (C3), restructured `01_ROLE` with the "Who's who" table (C4),
relabelled the verdict column (M1), rewrote Q5 + added Q7 to test *application* not
paraphrase (M4/M5), shipped **audit.py checks #8 + #9** (health **7/7 → 9/9**), added
the AGENT_FRAMEWORK v0.1 stub, and codified the **beta→stable promotion criterion**.
It also **sharpened v4's architectural claim** from "8 files generated from source"
to the honest version: *persistently-maintained surfaces collapsed via ephemeral
per-handoff generation + per-generation verification* — explicit that v4 accepts
synthesis-time imperfection and feeds it back into the next iteration, rather than
claiming zero-imperfection.

**This very bundle is the v4.3 first real test.** It exists to be reviewed by a fresh
pair of eyes; if that review returns **<2 critical findings**, v4 promotes
`beta → stable`.

*Parallel workstreams over the same days (see `JOURNAL.md` for chronological detail
if load-bearing): ADR-59/60/61 (visual pattern, docs taxonomy, git-worktree); four
Mermaid process diagrams + AI Council CLI v1.0 + `protocols/AI_COUNCIL_PROCESS.md`;
Mermaid dark-theme v1→v2 + `audit.py` check #7; cross-repo branch cleanup (~73
branches); a 22-finding overnight ecosystem coherence audit; and a harness-positioning
analysis — all at `docs/audits/2026-05-29-*`.*

## Four-tag discipline (canonical)

The sage tagged every claim using this discipline (canonical per HANDOFF_PROCESS
v4.3 Amendment A; supersedes the earlier three-tag body in spec §3.1):

- **witnessed** — sage just verified this OR saw it happen recently AND has no
  reason to think it changed since
- **recall** — sage remembers from earlier in the session; **state may have
  changed** — verify via CC inline if the claim is load-bearing
- **inferred** — reasoning from evidence (not direct knowledge)
- **unknown** — sage doesn't know — flagged explicitly

When you encounter `recall` or `unknown` on a load-bearing claim in this file,
verify via CC before acting on it. This is the "handoff is back-and-forth" rule
from PLAYBOOK methodology.

## What the sender chat said (interview)

**Past (what shipped).** This session is the closing chapter of the consolidation
arc; treating it as "just v4.3 work" understates it. Quantitative outcomes
(witnessed): tests **90 → 103**, audit health **7/7 → 9/9**, spec **395 → 443 lines**
(ADR-39 append-only growth), skill 134/200 lines, branch merged to `main` at
`5a5ab83`. The self-referential meta-pattern: the v4.1→v4.2→v4.3 cycle **is the
methodology operating on itself**; triangulation (insider catches structural,
outsider catches blindness) emerged as the central anti-drift mechanism and is now
codified as the beta→stable criterion.

**Present (where things stand).** `main` clean, baseline green. v4.3 ships at status
**beta** awaiting this fresh-eyes validation. In-flight: this re-test cycle. Open
threads the apprentice should verify before acting (all surfaced with CC commands):
corp-monorepo `chore/extract-p1-2-to-backlog` branch (cross-repo — surface only,
ADR-41); **LESSONS.md staleness** (last touched 2026-05-25 — rich anti-patterns from
this 24h belong there); 22 ecosystem-audit findings in BACKLOG; agent-framework v0.1
stub anchored; a cosmetic `§`→`�` Windows-console mojibake in audit.py check #9
output (display-only).

**Future (natural next step).** Immediate: this Phase 2 → fresh-eyes review → the
decision point. **<2 critical → promote beta→stable** (single commit flipping the
stamp). **≥2 critical → v4.4 cycle** (convergence broke; re-evaluate the
architecture). After promotion, sequenced but operator-weighed: LESSONS.md update
(hygiene gate, first regardless), Council ratification ADR for v4/v4.2/v4.3,
scrum-master review-authority codification, doc-truth sweep, agent-framework full
implementation.

## Load-bearing facts (cross-checked vs repo at Phase 2)

The sender tagged many claims `recall`/`unknown`; Phase 2 verified the load-bearing
ones against repo state. **No drift detected** — and one `unknown` resolved to known.

| Claim from sender | Repo fact | Phase-2 verdict | Verification command |
|---|---|---|---|
| v4.3 merged to `main` at HEAD `5a5ab83`, tree clean | Confirmed; merge commit `5a5ab83` (no-ff) | ✅ matches | `git rev-parse main` |
| Tests 103 / audit health 9/9 / ruff clean | Confirmed all three green | ✅ matches | `pytest -x; python scripts/audit.py health; ruff check` |
| Spec 443 lines; skill 134; stub 48 | 443 / 134 / 48 exactly | ✅ matches | `wc -l protocols/HANDOFF_PROCESS.md .claude/commands/handoff.md protocols/AGENT_FRAMEWORK.md` |
| LESSONS.md stale since 2026-05-25 (`recall`) | Last commit `2026-05-25 13:56` | ✅ matches | `git log -1 --format='%ai %s' LESSONS.md` |
| `ecosystem/` registry has no dot prefix | `ecosystem/` exists; no `.ecosystem/` | ✅ matches | `test -d ecosystem; test -d .ecosystem` |
| corp-monorepo `extract-p1-2` branch unmerged at `a1007b1` (`recall`, cross-repo) | Branch is current HEAD there, unmerged, tip `a1007b1` | ✅ matches | `git -C ../corp-monorepo branch -v` |
| v4.1 + v4.2 bundles preserved as historical evidence | Both directories present | ✅ matches | `ls -d docs/handoffs/2026-05-29-dev-knowledge-session*` |
| 987edac aborted-folder cleanup intentionality (`unknown`) | **Resolved:** deliberate — commit msg `chore: delete aborted handoffs folder (2026-05-29 abort artifact)`, 3 files / 475 deletions | ✅ unknown→known (intentional) | `git show 987edac --format='%s' --stat` |

## Decisions & reasoning to carry forward

- **Cluster-as-diagnosis.** When audit findings cluster, treat the cluster as a
  single structural diagnosis, not N independent bugs. This is *the* generalizable
  insight of the whole arc — it drove v3.4→v4 and it is what Q5 tests.
- **Triangulation is mandatory for quality gates.** Insider review empirically caught
  1 of 4 critical findings. Fresh-eyes (independent Opus 4.8, ~20 min) caught 4 of 4.
  Cheap insurance, high coverage — now codified as the beta→stable criterion.
- **Hard-metric closure over easy-metric.** "Tests green" repeatedly failed to equal
  "issue closed" across this arc (dark-theme v1, v3.4 abort, bundle reviews). Verify
  the fix CLOSES the goal, not just changes the file. This is the recurring LLM-work
  failure mode.
- **ADR-39 immutability via append.** Six ADRs + two HANDOFF_PROCESS amendments
  touched this period — all amendment-only, each verified `git numstat` insertions-only.
- **Council skipped for v4/v4.2/v4.3 implementation** (operator's call, fatigue);
  ratification deferred to a single future Council convene. *Risk:* if v4 is modified
  substantively post-stable, the ratification gap compounds.
- **Enforcement landed via audit checks, not the full agent framework.** Checks #8/#9
  shipped; the agent framework remains a v0.1 stub. Operator's strongest structural
  signal — *"musimy zbudować agent framework... żebym nie musiał po prostu
  powtarzać"* — is anchored but not built.
- **Spec budget tension accepted** (443 vs ≤350 original) — consolidate at v5/Council.
