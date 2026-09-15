# lane-z-11 — what we adopt, and what we refuse with the reason

> **Step 3 of `lane-z-11-three-repo-comparison`.** Slots:
> `2026-09-15-technical-lane-z-11-comparison-slots.md`. Matrix, with the measurements:
> `2026-09-15-technical-lane-z-11-comparison-matrix.md`.
>
> **Two lists, and the second is the load-bearing one.** A comparison that records only what
> it adopts leaves every rejection looking like an oversight, and the next reader re-opens
> it. Every refusal below carries its reason, and ADR-111 §2(d) is explicit that a rejection
> is *"recorded with its reason, and not relitigated"*.
>
> **Route.** ADR-111 names exactly one path from a finding to a row — **CANDIDATE → intake
> (ADR-98) → ratification** — and ratification is the operator's act. This lane therefore
> files intakes and **no `tasks/` rows**. Nothing here is closed, scheduled or promised.

---

## LIST A — adopt-candidates, filed

Four candidates, each filed as an intake document. They are listed in the order this lane
would recommend, with its own grading of each, and the grading is deliberately hard: two of
the four are small, one is measured-low-yield, and one is large enough that its own intake
flags it.

|Intake|Title|Matrix row|Size|This lane's grade|
|---|---|---|---|---|
|[#95](../intake/2026-09-15-tech-preflight-cannot-evaluate-verdict.md)|A locator predicate that cannot look must say so|G-7|small|**strongest** — a defect, not a preference|
|[#97](../intake/2026-09-15-tech-command-declares-the-module-it-runs.md)|A command file does not declare the module it runs|G-2|small–medium|strong — unblocks two live surfaces|
|[#96](../intake/2026-09-15-tech-corpus-wide-locator-resolution.md)|Nothing checks our own living documents' locators|G-1|small|honest-but-thin — yield is 1 in 127|
|[#98](../intake/2026-09-15-tech-provider-agreement-over-behaviour.md)|Provider agreement is asserted over strings, never behaviour|G-4|**large**|real, but gated on a question only the operator can answer|

**`#95` first, and it is the one this lane would defend hardest.** It is not an import from
another project at all — it is a defect this lane tripped over while trying to use our own
organ, in our own substrate. `preflight_contract.py` renders a SHA that is merely outside a
shallow clone's depth as *"not present in this repo's object store"*: 3,774 false refusals
out of 3,894 in this session. The repo already owns the distinction the fix needs — the same
module keeps exit 2 apart from exit 1 so *"I could not look" stays distinguishable from "I
looked and it is wrong"* — and simply has not extended it to an incomplete object store.
Harmless while ungated; wrong in exactly the substrate ADR-119 and `[#664]` are deciding
about.

**`#97` second, because it unblocks work already in flight.** ADR-119 asks whether a command
is adopted, and `[#664]` asks what nothing triggers; both need to know what a command
*reaches*, and today that edge exists only as prose in a fenced bash block. Intake `#94`
already records the consequence — 21 of 37 disposition rows reading as orphans by
construction. spec-kit shows the alternative is ordinary: put the invocation in frontmatter
and it becomes testable.

**`#96` third, and filed thinner than it looks.** The measurement is one live broken locator
across 127 files — `protocols/STANDING_RULINGS.md:4074` citing line 96 of a 77-line
template. This lane will not inflate that. What earns it a slot is *where* it sits: a living
governing document, carrying an unresolvable citation, defending the failure class
`CLAUDE.md` §4 calls the most-recorded. The intake asks for warning-only and says so.

**`#98` last, and flagged in its own text as the largest thing here.** It is a test
substrate, not a checker, and its cost scales with the provider count — which is a
functional question (ADR-108 §A) this lane has no standing to answer. It is filed because
the failure class is *measured*, not hypothetical: `.claude/settings.json` records that a
bare `$CLAUDE_PROJECT_DIR` *"turned any other reader honouring this file (cursor-agent,
measured over two paid runs) into total refusal of every tool call"* while every declared
string agreed.

---

## LIST B — what we will NOT adopt, and why

Mandatory list. Each entry names what was seen, in which repo, and the reason it is refused
here. A reason is either **structural** (adopting it would break a ratified invariant) or
**economic** (the cost is real and the demand is not). Both are terminal for this lane;
neither is an oversight.

### R-1 — an installable CLI that initialises a consumer repo *(spec-kit `specify init`)* — STRUCTURAL

spec-kit ships `src/specify_cli` with `specify init` and `specify check`, which scaffold and
inspect a consumer project. We will not.

**Reason: it is forbidden by the invariant this repo is built on.** `CLAUDE.md` §5 rule 4:
*"Layer 2 never executes — no orchestration scripts: no script drives state in a child repo
(ADR-28, ADR-36)."* A tool whose purpose is to write into a child repo is the definition of
what Layer 2 does not do. This is not a cost judgement that better tooling could overturn —
a one-command installer and the Layer-2 invariant cannot both hold, and the invariant is
ratified.

Our answer to the same need is already chosen and is a different shape: a deploy manifest
plus carriers, with `templates/consumer-onboarding-runbook.md` and `INSTALL.md` as the
operator-executed path. **If the convenience is ever wanted badly enough, the route is an
ADR superseding ADR-28/36 — not a script.**

### R-2 — corpus internationalisation *(BMAD `docs/cs|fr|ko-kr|vi-vn`, `README_CN|KR|VN`)* — ECONOMIC

**Reason: one operator, who has specified English.** BMAD translates because it has a global
contributor base; this repo has a named audience of one and a standing instruction that
professional documents are written in English. The cost is not one-off — it is every
governing document multiplied by every language, forever, against zero demand. Translation
would also fork the single-source regions that `CLAUDE.md` §5 rule 6 requires to stay
byte-identical, which turns a cost into a correctness risk.

### R-3 — exporting tasks to an issue tracker *(spec-kit `taskstoissues`)* — STRUCTURAL

**Reason: it would create a second authority over row state.** `tasks/` files are the
source, `BACKLOG.md` is generated from them, and ADR-109 discharges that relationship with a
byte-exact round-trip plus a residue manifest. An issue export makes a row exist in two
places that can disagree, and reconciling them is exactly the drift the generated-BACKLOG
design exists to prevent. The funnel's integrity (ADR-111: no finding becomes a row without
triage) depends on there being one place a row can be born.

### R-4 — a ten-rule skill-shape validator *(BMAD `tools/validate_skills.py`)* — ECONOMIC

**Reason: the rule count exceeds the corpus it would govern.** `.claude/skills/` holds two
skills. BMAD's validator is proportionate to a corpus of dozens of role and process skills;
here it would be more validator than validated, and `CLAUDE.md` §5 rule 5 asks for a
navigation/growth check before adding surface.

**Recorded so it can be re-opened on evidence rather than on taste** — this is the one
refusal in this list with a named revisit trigger: *when the hub's own skill corpus exceeds
its command roster, or when a consumer repo begins authoring skills against the deployed
floor.* Until one of those happens, the answer is no.

### R-5 — agent-persona roles as skills *(BMAD `bmad-agent-analyst|architect|dev|pm|ux-designer`)* — STRUCTURAL

**Reason: it would be a third role vocabulary, and the registry already warns about exactly
this.** We hold two on purpose: `ecosystem/routing-table.yaml` (four coarse roles → CLI, the
authority) and `provider-registry.yaml`'s `roles:` (six fine-grained roles → ordered
provider list, a ranking). That file states the constraint in its own words — the two are
kept distinct *"because they answer different questions, and collapsing them would make one
of the two lie"* — and names the failure mode a third would revive: *"the
four-rival-dispatch-commands disease in a new costume."*

Role separation itself is not rejected; we already have it, routed by ADR-108 §A (operator
rules functional questions, architect technical ones). What is rejected is a **third
vocabulary** for it.

### R-6 — a blanket test-driven-development mandate *(superpowers `test-driven-development`)* — STRUCTURAL

**Reason: adopting it would reverse a Council ruling by import.** `CLAUDE.md` §4 is explicit:
TDD here is *"a build-arc standard, not a blanket mandate"*, ADR-108 §B binds build arcs
with RED-first witnesses, and *"a blanket mandate is **not** live — Council rejected
'Mandatory TDD'."*

The mechanism is not missing — ADR-81 as amended lets the architect strengthen a frozen
pass/fail criterion but never weaken it, and `impacted-tests-guard` refuses a changed
`scripts/*.py` that no test covers, naming the RED-first test in its refusal. A superpowers
skill that applies TDD to everything would quietly overturn a decision that was taken
deliberately. **A ruling is reversed by a new ruling, never by importing a skill that
assumes the opposite.**

### R-7 — a second rendered documentation site *(BMAD `docs-site/`, Astro)* — ECONOMIC

**Reason: the direction is already held, and adopting a second one forks it.** Intake `#9`
("Dashboards as local HTML") already carries the human-surface direction, and
`ecosystem/conformance.html` is the live instance. A Node/Astro site would add a build
toolchain, an npm dependency tree and a sidebar to keep in sync, to serve one reader who has
the repo open locally.

Not refused: the *specific idea* inside BMAD's site tooling — that a navigation surface
should be validated rather than hand-maintained (`quality.py` runs `validate-sidebar`). That
principle is already ours and better enforced, by the freshness gates over the generated
rosters and indices.

---

## Considered, deferred — explicitly NOT refused

Three matrix rows this lane judged real but did not file. Recorded here so that the two
lists above stay honest: these are **not** in List B, and a later reader is free to pick
them up without re-litigating anything.

- **G-5 — content-level cross-artifact consistency** (spec-kit `analyze`). Our
  `coherence-nudge` is non-blocking and fires on a spec version-bump signal rather than on
  artifact content. A genuine narrowing, but the gap runs into ADR-108 §B and the
  `_SPEC_REGISTRY` design, which is a doctrine conversation rather than a lane finding.
- **G-6 — generated clarification questions** (spec-kit `clarify`, ≤5 targeted questions
  encoded back into the spec). We route questions well (ADR-108 §A) and surface OPERATOR
  ASKS at boot, but nothing *generates* the question set from a frozen contract. Adjacent to
  the `--freeze` predicates and to the V-2 decision budget; deferred as design, not defect.
- **G-9 — one aggregated "run what CI runs" entry point** (BMAD `quality.py`). The `verify`
  skill already runs pytest + ruff + git-status and `audit.py health` is one command; the
  increment is convenience, and this lane could not measure a cost it removes.

---

## What this lane did not do

- **No `tasks/` rows.** ADR-111's only route is CANDIDATE → intake → ratification, and
  ratification is the operator's act.
- **No fix to the one measured defect.** `protocols/STANDING_RULINGS.md:4074` is a living-doc
  edit outside this lane's footprint, and the lane is declared read-only.
- **No index regeneration.** `docs/intake/README.md`'s generated Contents block does not list
  intakes `#95`–`#98`; the integrator is gate-of-record and regenerates once at the merge.
- **No gate run.** Substrate is cloud; no hook is armed there.

---

**Lane:** `lane-z-11-three-repo-comparison` · **Substrate:** cloud · **Date:** 2026-09-15
