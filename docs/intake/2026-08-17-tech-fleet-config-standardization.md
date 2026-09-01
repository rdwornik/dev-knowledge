---
intake-id: 38
status: ACCEPTED
origin: browser research artifact wf-460fee76, commissioned + landed 2026-08-17; converted to intake by lane R (unrostered, running alongside batch 7a)
decided-by: "operator GO on the 2026-08-19 S-1 night-adjudication seat arc (docs/audits/2026-08-19-technical-s1-seat-arc-contract.md act 4), ratifying the N3 ratification pack's CLEAR verdict"
disposition: active
note: Sections A-D are required by the lane-R contract of record (docs/audits/2026-08-17-technical-research-intake-lane-contract.md section 1). All eight ADR-98 template sections are present and carry them; Section C is the one added top-level section, because a doctrine-delta is neither a requirement nor an open question.
consumers: "carrier [#559] kernel/lab check tiering + `dev-knowledge-kernel` as an installable package; no ADR — rows only, per the N3 pack §6.2. R18 (the conformance scorecard) is recorded as not-born at §6.4 with its un-parking conditions"
---

# Multi-repo config standardization and fleet conformance at N=8

## Problem / motivation

This hub publishes a methodology to ~8 consumer repos and already has the machinery to do it:
a versioned `deploy/manifest-v*.yaml`, carried replicas, a hash-guarded floor
(`.claude/CLAUDE-FLOOR.md`, ADR-78/93), a `fleet_parity` audit check, and
`ecosystem/deployed-versions.yaml`. What it does not have is a **single instrument that answers
"which consumer has drifted, and how"** — conformance today is inferred from several partial
signals rather than read off one scorecard.

The memo's most useful contribution is a hard negative result that saves wasted work: **Python
tooling cannot inherit config from an installed package.** Ruff's `extend`, mypy, pytest, and
coverage all resolve a *file path*, never a package name. So "one source of truth" for Python
config means *distributing a file*, not *importing a package* — and every shared-config package
in the wild ships a file plus a copy step. This repo already chose file-distribution, so the
finding is an endorsement rather than a redirection; it means the obvious "just publish a
config package" refactor is a dead end and should not be attempted.

Its second contribution is a currency fact with teeth: **Repolinter — the obvious off-the-shelf
conformance tool — was archived by the TODO Group on 6 February 2026 and is read-only.** Any
plan that reaches for it is reaching for an unmaintained dependency.

### Section A — the artifact's own TL;DR, quoted

> - **Build a hub-published "standard" as three separable layers — a shared config surface, a Copier template with `copier update`, and a conformance checker that runs in the hub's CI against all 8 repos.** No single tool does all of this; the realistic solo-operator stack is Copier (scaffold + re-apply), a small Python conformance checker (drift detection), and reusable GitHub Actions workflows pinned to a floating major tag (CI uniformity). Policy-as-code engines you already researched are overkill at N=8.
> - **The hard technical constraint is that Python tools do NOT support inheriting config from an installed package the way ESLint/tsconfig do** — Ruff's `extend` and mypy/pytest configs can only reference a file path, not a package name, so "one source of truth" for Python config means *distributing a file* (via template re-apply or a copy step), not *importing a package*. This is the single most important finding and it shapes the entire architecture.
> - **Cache directories (`.ruff_cache`, `.pytest_cache`, `.mypy_cache`, `__pycache__`, `.venv`) mean nothing about conformance — they are local build artifacts, each relocatable via a per-tool env var or config key, and their presence/absence in a repo is noise, not signal.** Gitignore them and exclude them from your checker; do not treat them as drift.

## Scenarios (+1 view)

- **As the operator I** ask which of the 8 consumers is behind on the methodology, **and then**
  assemble the answer from `ecosystem/deployed-versions.yaml`, the `fleet_parity` WARN, and a
  memory of what shipped when — instead of reading one dated, per-rule, waiver-aware scorecard.
- **As the operator I** grant a consumer a legitimate exception from a hub rule, **and then**
  have nowhere to record it with an expiry, so the exception either becomes permanent by
  silence or gets re-litigated every time the check runs.
- **As the operator I** change a hub config file, **and then** cannot push that change into the
  8 already-generated repos, because the hub's distribution is one-shot at deploy time and
  nothing re-applies a later change to an existing consumer.

### Section D — the smallest first build the artifact names

Quoted from the memo's own "The smallest first build":

> - **Q1 (shared config):** a single hub-owned **`.pre-commit-config.yaml` + `.editorconfig` + `.gitignore`** trio distributed by the Copier template. Accept that Python tool config is *copied*, not *imported* — do not waste time trying to make Ruff/mypy import a package; it cannot.
> - **Q2 (drift):** the conformance checker (below).
> - **Q3 (environment):** `.python-version` + committed `uv.lock` + `uv sync --check` in CI in every repo.
> - **Q4 (onboarding):** the Copier template + a `bootstrap.ps1`/`bootstrap.sh` that runs `uv sync && pre-commit install` and appends the repo to the hub's fleet manifest.

The checker sketch it gives is concrete: a `fleet_check.py` in the hub reading a `fleet.yml`
(the 8 repos, each with a declared tier and `standard_version`) and a `fleet-exceptions.yml`
waiver registry (id, repo, rule, reason, `expiresOn`); asserting required files, folder
taxonomy, config keys, pinned hook revs, CI ref and recorded standard version; **exiting
non-zero on any unwaived failure** and emitting a `CONFORMANCE.md` scorecard. An unexpired
waiver renders as waived rather than failing; an expired waiver reverts to failing **and is
itself reported**.

## Functional requirements

### Section B — the decisions this would force on THIS repo

Six proposed rows. **NOTHING BELOW IS BORN.** No `BACKLOG.md` line, no `tasks/` file, and no id
is consumed; lane R holds no reserved id block.

```
PROPOSED ROW R18 - fleet_check.py: one conformance scorecard for the 8 consumers
  Done-when: a single command emits a per-repo x per-rule scorecard with a fleet percentage,
             exits non-zero on any unwaived failure, and its rule set is DERIVED from the
             live deploy manifest rather than hand-listed (so a manifest change cannot leave
             the checker stale).
  kill-candidates: consolidates the partial signals fleet_parity + deployed-versions.yaml +
             the SessionStart fleet_health digest already emit -- propose folding
             fleet_health's Tier-2 digest into this rather than running both

PROPOSED ROW R19 - fleet-exceptions.yml: waivers that EXPIRE
  Done-when: a waiver carries id + repo + rule + reason + expiresOn; the checker renders an
             unexpired waiver as waived and an EXPIRED one as failing AND reports the expiry
             itself; a waiver with no expiresOn is REFUSED at parse time.
  kill-candidates: overlaps ecosystem/disposition-register.yaml, which records dispositions
             but carries no expiry -- propose the register gain expiresOn rather than a
             second registry being born

PROPOSED ROW R20 - Copier template with a recorded standard_version
  Done-when: a consumer generated from the template carries .copier-answers.yml naming the
             hub template tag; `copier update` re-applies a later hub change to an ALREADY
             generated consumer; the checker flags any repo whose recorded version is behind
             the hub's current tag.
  kill-candidates: none -- the current deploy path distributes but cannot RE-APPLY; this is
             the missing capability, not a duplicate of the deploy tool

PROPOSED ROW R21 - Zero-inheritance-cost artifacts standardized first
  Done-when: every consumer carries byte-identical .editorconfig and the gitignore cache
             block, and a pinned-rev .pre-commit-config.yaml; the checker asserts byte
             identity for the first two and rev equality for the third.
  kill-candidates: none -- cheapest drift reduction available and touches no Python config

PROPOSED ROW R22 - Toolchain pin across the fleet
  Done-when: every consumer has .python-version and a committed uv.lock, and `uv sync
             --check` (or `uv run --locked`) runs in its gate; a drifted lock exits non-zero.
  kill-candidates: none -- and see [#39], whose provisioning script asserts the same uv pin
             at container build time; propose ONE pin definition consumed by both

PROPOSED ROW R23 - Conformance measured as adoption, not as checkbox count
  Done-when: the scorecard reports at least one non-file-presence signal (e.g. exceptions
             requested, or time-to-onboard a new repo) alongside the percentage, so the
             metric cannot become vanity.
  kill-candidates: none -- but this is the memo's own warning about its own recommendation
             and should be built WITH R18 or not at all
```

- **Must:** R18 — the memo's own ordering, and its reason is sound: *"This gives you
  visibility before you change anything — you cannot fix drift you can't see."*
- **Should:** R21 and R22 — cheapest real drift reduction, no architectural commitment.
- **Could:** R19, R20, R23.

## Acceptance criteria (ex-ante)

1. One command answers "which consumer has drifted and how", with a date and per-rule detail.
2. A legitimate exception is recorded with an expiry and cannot become permanent by silence.
3. A hub standard change can reach an already-generated consumer without hand-editing it.
4. No conformance rule asserts on the presence of a cache directory.

## Non-goals

- Migrating to a monorepo. The memo's recommendation is explicit and matches the current
  shape: *"stay polyrepo; treat the hub as a platform repo the consumers reference."*
- Adopting OPA/Conftest or a codemod platform. The memo puts the graduation threshold at
  ~20 repos or additional contributors; at N=8 it names both as overkill.
- `github/safe-settings`, Terraform GitHub provider, or any settings-as-code system. The memo
  flags the shared hazard: such a system *silently reverts manual GitHub UI changes*, and
  Terraform auto-apply can reconcile destructively.
- Adopting Repolinter — archived and read-only since 2026-02-06.
- git submodules. The memo's warning is specific to this fleet's workflow: *"Given your
  LLM-agent worktree workflow, submodules will fight the agents."*

## Section C — what this supersedes or contradicts in current doctrine (locators)

**CONFIRMS the hub's existing architecture, and this is the memo's main value here:**

- *"'one source of truth' for Python config means distributing a file … not importing a
  package"* — this hub already distributes files: `deploy/manifest-v*.yaml` `components:[]`,
  the carried replicas noted in `.claude/methodology-roster.md`, and the floor as a
  "hash-guarded replica" (`CLAUDE.md` §9 roster / ADR-78/93). The memo confirms there was
  never a better option, so no refactor is owed.
- The memo prefers **generation-plus-checksum over symlinks**; `floor-hash-verify` "verifies
  `.claude/CLAUDE-FLOOR.md` matches its sha256 sidecar" (`.claude/methodology-roster.md`).
  Already built, on the recommended shape — and independently reached by the 2026-08-09
  portability memo (`docs/archive/…-multi-provider-portability-wf-d68b2f7f.md`).
- Renovate's `extends` + `#tag` versioning model is what `deploy/manifest-v*.yaml` version tags
  plus `ecosystem/deployed-versions.yaml` already approximate. The memo names the reference
  design this repo converged on.
- *"a `STANDARD_VERSION` field your checker reads … a consumer stuck on an old version is
  detected by comparing its recorded version to the hub's current tag"* — this is
  `fleet_parity` / `deployed-versions.yaml` in substance. R18 consolidates rather than invents.

**COMPLEMENTS, no conflict:**

- The folder taxonomy the checker would assert is already declared and machine-enforced here:
  ADR-101's Tier-1/Tier-2 seal, `scripts/validate_hermetization.py` (`SANCTIONED_GENRES`, the
  Rule C home allowlist). The hub can hand the checker its taxonomy rather than restating it —
  and a live-tree test already asserts Rule C admits every tracked path (`CLAUDE.md` §12 v2.58).
- The memo's *cache dirs are not signal* finding conflicts with nothing here; recorded so a
  future checker author does not add the rule by reflex.

**PARTIAL CONTRADICTION — the exceptions registry:**

- `ecosystem/disposition-register.yaml` and `protocols/STANDING_RULINGS.md` record dispositions
  and standing rulings, but **carry no expiry field**, so a disposition is permanent until
  someone re-opens it. The memo is explicit that a waiver without an expiry "becomes an
  undocumented bypass". The nearest live precedent for the memo's shape is *outside* this repo:
  `~/.claude/rules/core-invariants.md` §1's T1 read-grant table carries an `Expires` column and
  states an expired grant "is dead code and the path blocks again with no edit required."
  **R19 proposes extending the existing register rather than birthing a second one** — but
  whether a disposition *should* expire is a doctrine question, not a lane's call.

**SUPERSEDES nothing.**

## Impact sketch (4+1 lite)

- **Logical:** adds one conformance surface; consolidates several partial ones.
- **Process:** onboarding a consumer becomes template + bootstrap + gate, with "in the fleet"
  defined as "passes the checker".
- **Development:** one new script plus two manifests; no change to the deploy tool unless R20
  lands.
- **Physical:** the memo runs the checker in hub CI on `ubuntu-latest`. This repo has no CI —
  see [#39].

## Open questions

1. Is `fleet.yml` a new file, or does `ecosystem/organ-registry.yaml` /
   `ecosystem/deployed-versions.yaml` already carry the consumer roster the checker needs?
   Birthing a fourth `ecosystem/*.yaml` when a third already lists the fleet would be exactly
   the proliferation ADR-101 seals against.
2. Should `disposition-register.yaml` gain `expiresOn` (R19's proposal), or is a permanent
   disposition the deliberate design? Both readings are coherent; this is an operator call.
3. Does `copier update`'s "no clean adopt path for an existing repo" (open Copier issue #2486)
   make R20 too expensive for 8 *already-existing* consumers? The memo names this as "the
   biggest one-time cost in the plan."
4. Where does the checker run, given there is no CI? Locally on demand is possible but forfeits
   the scheduled-drift-detection property that motivates it.

## Cross-links to the four sibling intakes landed in the same arc

- **[#39] `2026-08-17-tech-off-machine-agent-substrate.md`** — strongest pair. Both memos
  independently converge on `.devcontainer` + a **pinned-and-asserted uv version**: R22 here
  wants the pin across consumers, #39's Stage-0 wants it asserted at container build. **One pin
  definition should serve both.** #39 also supplies the compute the checker needs.
- **[#36] `2026-08-17-tech-repository-autonomy-and-gate-liveness.md`** — the same subject at
  two scopes: #36 is policy-as-code *within* a repo, this is conformance *across* repos, and
  both cite Nx's evaluated→enforced lifecycle and both want expiring exceptions. #36's R10 rung
  table would be a per-repo rule in this checker; conversely, this checker is itself a gate and
  therefore owes #36's R6 a negative control.
- **[#37] `2026-08-17-tech-machine-verifiable-done-when.md`** — the conformance rules here
  ("repo X has file Y, config key Z, standard version N") are literally #37's `kind: file` and
  `kind: command` `done_when` predicates evaluated across repos. If #37's R12 lands first, this
  checker should emit its rules in that schema rather than inventing a second one.
- **[#35] `2026-08-17-tech-agent-instruction-layers-and-distillation.md`** — if #35's R1 admits
  AGENTS.md, distributing it to 8 repos is this doc's problem, and the file-not-package finding
  applies to instruction files exactly as it does to Ruff config. #35's R4 (fleet-wide
  instruction-budget instrument) is one more rule in R18's checker.

Also related to the already-filed **[#33]
`2026-08-12-func-repo-self-description-consolidation.md`** (DRAFT — architecture freshness,
docs taxonomy, per-provider config), which overlaps this doc's per-provider-config and taxonomy
concerns and should be triaged alongside it rather than in isolation.

## Status

**DRAFT** — landed 2026-08-17 by lane R, unratified. Not operator-approved; the
`docs/intake/README.md` §6 confirm-gate has not been cleared. Zero rows born; six proposed.


---

## AMENDMENT — 2026-08-29: THE ROOT-CONTRACT, the operator's requirement verbatim

> Appended, not edited. This intake is **ACCEPTED**; the amendment adds a requirement to an
> accepted object rather than birthing a rival, per the reconcile-before-birth correction
> (Z-G1 / ADR-111): *"map it to its existing funnel object(s) … land the ruling as an
> amendment ON that object, citing it. Birth a NEW object ONLY where the ledger shows a true
> gap."*

**Why HERE.** This intake is *"Multi-repo config standardization and fleet conformance at N=8"*,
and its own `consumers:` line already names carrier **`[#559]`** and records **R18 — the
conformance scorecard — as NOT-BORN at §6.4 with its un-parking conditions**. The root-contract
IS R18's subject matter. Filing a new intake would have duplicated an ACCEPTED one, which is
exactly the outcome the correction exists to prevent.

**THE OPERATOR'S REQUIREMENT, verbatim (2026-08-29):**

> THE ROOT-CONTRACT — every fleet repo carries an identical canonical root (same file set,
> non-standard files relocated, same workspace settings, same ordering), versioned spec + parity
> check; feeds intake-61 q1 (part of what the engine IS). No further consumer deploys beyond the
> landed floor until it is ruled.

**Three things this changes about the intake, stated so they are not inferred.**

1. **R18's un-parking conditions are now the thing to test**, not a deferred question. The
   requirement above IS a conformance scorecard with a versioned spec; if R18's conditions are
   met, R18 births under this intake rather than beside it.
2. **It feeds intake #61 q1** — *"What, exactly, is 'the engine'?"* — and does **not** duplicate
   it. #61 q1 asks where the *handoff engine's* boundary falls; the root-contract asks what a
   *repo root* must contain. The operator's phrasing is "part of what the engine IS", so the
   dependency runs root-contract → q1, and q1's ratification should read this amendment.
3. **A STANDING CONSTRAINT is now live and belongs to no lane:** *no further consumer deploys
   beyond the landed floor until it is ruled.* win-tooling's v1.4.0 floor **is** landed
   (`floor_integrity` PASS, `deployed_methodology_version` PASS), so the constraint bites the
   *next* deploy, not this one. Its parity role stays **pre-deploy** until the divergence arc
   closes — filed as a candidate in the same act.

**Related, measured this window:** the divergence set that holds win-tooling at pre-deploy —
`docs-genre-decisions`, `methodology-yaml`, `pytest-minversion`, `root-gitattributes` and others —
is recorded in night-batch-2 lane A's packet, which made the parity flip, measured that it REDs
`test_check_fleet_parity_green_on_live_repo`, and **reverted it** rather than edit the instrument.

## AMENDMENT — 2026-08-29 (b): R18's un-parking conditions TESTED, not deferred again

> Appended, not edited. This is the integrator act the batch-D freeze owed (architect CUT-1:
> the ROOT-CONTRACT is an amendment to this intake, landed serially, and explicitly NOT folded
> into the CLAUDE.md re-genre lane).

The 2026-08-29 amendment above said *"R18's un-parking conditions are now the thing to test, not a
deferred question."* This amendment tests them, so the claim does not stand unexercised for a
second window.

**The conditions, quoted from where they actually live** — `docs/audits/2026-08-19-technical-n3-ratification-pack.md`
§6.4. Note for the next reader: this intake's `consumers:` line cites "§6.4" with no document, and
§6.4 is **not in this file** — it is in the N3 ratification pack. The locator resolves, but only
after a search; it is written down here so the next reader does not repeat it.

> **Un-parked by:** the kernel row's leg 1 landing (the tiering is the rule set the checker would
> assert), **or** the next window with ≥1 birth of headroom — whichever is first.

**Condition (a) — the kernel row's leg 1: NOT MET, and the reason is a taxonomy mismatch rather
than absent work.** `[#559]` is `status: open`. Its leg 1 requires *"every `ALL_CHECKS` member
carries a `kernel`/`hub` tier"*. A tiering DOES exist and is live — but it is `[#597]`'s, and its
enum is `TIER_COMMIT` / `TIER_SHIP` (`scripts/audit.py:357-358`), declared inline in `ALL_CHECKS`
per the comment at `scripts/audit.py:340`. Measured at freeze: **54 checks discovered, 0 carrying a
`kernel`/`hub` tier.** So the axis that landed is *when a check runs* (commit ⊂ ship), and the axis
R18 would assert against is *what layer a check belongs to* (kernel vs hub). These are different
questions and one does not satisfy the other. Recording that distinction is the point: a future
reader seeing "tiering landed" could otherwise mark leg 1 met by name-matching.

**Condition (b) — a window with ≥1 birth of headroom: NOT MET this window.** The 2026-08-29
post-night window birthed `[#616]`, `[#617]`, `[#618]`, `[#619]` plus intakes #62 and #63, each
operator-directed and each carrying its own `kill-candidates:` line. Those births SPENT the
window's filing capacity rather than evidencing spare headroom; a window that fills its ledger is
not a window with headroom in it.

**VERDICT: R18 stays PARKED, on tested conditions rather than on silence.** Both un-parking
conditions were live, both were checked, and both are unmet. The intake's open question 1 —
whether `fleet.yml` is a new file at all, or whether `ecosystem/organ-registry.yaml` /
`ecosystem/deployed-versions.yaml` already carry the consumer roster — remains the cheap thing to
settle before R18 births, and remains unsettled.

**Consumed by:** the batch-D freeze, 2026-08-29
(`docs/audits/2026-08-29-technical-batchd-launch-contracts/`).


---

## AMENDMENT — 2026-08-31: THE ROOT-CONTRACT v1, STATED — permitted set, relocation, workspace, ordering

> Appended, not edited. Batch E lane `c-3-root-contract`, done-contract DC-4. The 2026-08-29
> amendment recorded the operator's requirement verbatim and named the standing constraint it
> carries; it did **not** state the contract. This amendment states it, and states it **before
> the first consumer deploy**, because the surface that deploys is the surface whose shape has
> to be settled first — shipping a consumer against an unstated root ships the ambiguity.

**What "contract" means here, said first so the clauses are read at the right strength.** This
is a STATEMENT of the required shape plus the NAME of the surface that checks each clause — not
a new instrument. Every clause below is either already machine-asserted by a named surface, or
is declared unasserted in the same breath. Nothing here births a file, a row or a check; where
an assertion is missing the gap is **written down rather than closed**, because closing it is
R18's job and R18 is parked (below).

### C1 — The permitted root set is CLOSED, and it is closed by two surfaces at two scopes

**The rule.** A repo root holds exactly what a sanctioning surface admits. Nothing at the root
is permitted by mere presence.

**The surfaces — never a list retyped here:**

- **Hub, prospective:** `scripts/validate_hermetization.py` Rule A, reading
  `SANCTIONED_TIER1_DIRS` and `SANCTIONED_TIER1_FILES` — ADR-101 §1's closed sets, which grow
  or shrink only through that ADR's amendment channel. `SANCTIONED_TIER1_FILES` splices in
  `scripts/canonical_docs.py::CANONICAL_MANDATORY` rather than retyping the living-doc names,
  so the ADR-38 canonical set and the ADR-101 file enum provably name the same strings.
- **Fleet, retrospective:** `scripts/fleet_parity.py::_eval_sweep` — every TRACKED top-level
  entry not covered by an applicable `ecosystem/parity-surfaces.yaml` row is `WARN-undeclared`,
  which `audit.py::check_fleet_parity` maps to RED. The `root-*` rows in that manifest are the
  declared members; a repo's own `.methodology.yaml` may declare a local divergence, which is
  the sanctioned way a root entry exists without a fleet row.

**The honest limits, both of them:**

1. Rule A is **HUB-ONLY and prospective-only** (its own docstring; ADR-101 §6). It never
   inspects an existing file and it does not run in a consumer at all. It cannot be the fleet's
   instrument for "identical canonical root", and no reading of this contract may treat it as
   one.
2. The sweep is **fleet-wide but top-level-grain only**, and sees only TRACKED entries — its
   own docstring names both limits. An untracked or ignored root entry is invisible to it by
   construction.

Between them the two cover growth-at-the-hub and divergence-across-the-fleet. Neither covers
**an already-present unsanctioned file inside a consumer**, and that is the one hole C1 leaves
open by name.

**A confirmation the memo earns.** The sweep's tracked-only construction is exactly this
intake's own *cache dirs are noise, not signal* finding: `.venv`, `__pycache__` and their peers
are ignored, therefore invisible, therefore never drift. The finding needed no rule — the
design already had the property.

### C2 — Non-standard files are RELOCATED, not tolerated in place

**The rule.** A root entry that is not a sanctioned member moves to the home its class belongs
to; it is not waived at the root. The genre tree, never a sibling folder, is where an
accumulating artifact class lives — the ADR-101 amendment of 2026-08-26 (b) ruled precisely
this and is the standing precedent: *"root is sacred, the docs disease is cured by the consumer
gate, not by a sibling folder."*

**The surface.** `validate_hermetization.py` Rule C (home allowlist `_HOME_PATTERNS`; standing
ruling K-1) is the hub-side leg — it reads the rest of the path, where Rule A stops at the top
level.

**The limit, stated rather than implied.** There is **no fleet-side depth leg**; the sweep
declines depth in its own docstring. C2 is therefore contracted fleet-wide and enforced
hub-only, and a consumer's misplaced file is caught by nobody today.

### C3 — The workspace declaration

**The rule.** Every fleet repo carries exactly one **dot-prefixed** `<repo>.code-workspace` at
its root, and that file's first `folders[]` entry is the repo itself.

**The surfaces.** `scripts/audit_checks/check_workspace_settings.py` — FAIL if absent or
unparseable as JSONC, WARN if present but not dot-prefixed — and the
`ecosystem/parity-surfaces.yaml` row `root-code-workspace`, whose probe is
`glob_tracked: *.code-workspace` at `{hub: MUST, consumer: MUST}`.

**What is contract-bound and what is HOST-LOCAL — the distinction this clause exists to make.**
Presence, the dot-prefix, the one-file rule and C4's sort settings are fleet-contracted.
Everything else in the file is host-local and travels with **no** fleet claim: this hub's own
workspace carries provider-config folder roots as host-absolute paths measured on one machine
on one date, and copying those into a consumer would assert something false about that
consumer's host. The contract is over the file's ROLE and its sort settings — never over its
folder list.

### C4 — Ordering

**The rule.** The root's presentation order is **declared in the workspace file**, not left to
the editor's default.

**The surface, at the exact grain of what it asserts.**
`check_workspace_settings._WORKSPACE_REQUIRED_SETTINGS` pins two keys — `explorer.sortOrder`
and `explorer.sortOrderLexicographicOptions` — per ADR-59 Decision 3. `"upper"` is the value
that clusters the ALL-CAPS canonical living docs ahead of the lowercase configs, which is what
makes a conforming root READ as a canonical set rather than as an alphabet.

**The gap, named because "same ordering" would otherwise be over-claimed.**
`explorer.sortOrderReverse` is carried by this hub's workspace and is **NOT** a member of
`_WORKSPACE_REQUIRED_SETTINGS`. The newest-first behaviour inside dated folders is therefore a
hub practice, not a fleet-asserted clause. Either it joins the required set or the contract
stops claiming it; this amendment does neither, and says so rather than letting the ambiguity
ride.

### Reconciliation against ADR-101's tree seal — three findings, no contradiction

DC-4 required this contract not to contradict the hermetization allowlist. It does not. The
three places where the two surfaces are merely DIFFERENT rather than in conflict are recorded
so a later reader mistakes neither for drift.

1. **The ADR states CLASSES; the gate enumerates MEMBERS.** ADR-101 §1 says the Tier-1 file
   rule is *"not an enumerated whitelist — a class rule"*, while `SANCTIONED_TIER1_FILES` is a
   frozenset of literals. They agree in effect and differ in kind: the class rule governs what
   an AMENDMENT may admit; the enumeration is what a gate can actually check. This contract
   binds itself to the enumeration for checking and to the class rule for admission, which is
   how both stay true at once.
2. **§1's prose list is not the live set and must not be read as one.** ADR-101's amendments
   append rather than edit, so `.github/`, `.devcontainer/` and `tasks/` are sanctioned by
   amendments *below* §1 and are absent from §1's own sentence, while `prompts/` appears in an
   amendment and was then revoked. A reader who quotes §1's directory list as the permitted set
   will be wrong. **The live set is the code** — this contract cites the module, never the
   sentence.
3. **The workspace member is a hub-specific literal; the fleet grain is a glob.**
   `SANCTIONED_TIER1_FILES` carries the literal `.dev-knowledge.code-workspace`, which is
   correct for a HUB-ONLY gate and wrong as a fleet rule; `root-code-workspace` uses
   `glob_tracked: *.code-workspace`. C3 is stated at the glob grain for exactly that reason.
   This is the general shape of the hub-only-gate-versus-fleet-rule seam, and it will recur.

### The hub's own root, MEASURED against the seal — 2026-08-31

Not restated as a roster. The measurement is a comparison anyone can re-run, and its result
this window is: **every tracked top-level entry of this repo is a member of the sealed sets.**
The delta runs the other way — two sanctioned members are simply absent (`codex/`, `.ruff.toml`),
and sanction is permission, never a mandate to carry.

Re-run it from the repo root:

```
uv run --locked python -c "import sys; sys.path.insert(0,'scripts'); import subprocess, os, validate_hermetization as vh; top=sorted({p.split('/',1)[0] for p in subprocess.run(['git','ls-files'],capture_output=True,text=True).stdout.splitlines()}); print('unsanctioned:', [t for t in top if t not in (vh.SANCTIONED_TIER1_DIRS if os.path.isdir(t) else vh.SANCTIONED_TIER1_FILES)])"
```

An empty `unsanctioned:` list is the conforming state. This is the **hub's instance** of the
contract, not a fleet result: the same comparison against a consumer needs that consumer's own
root and C3's fleet grain — which is why the fleet answer is R18's scorecard and not a command
pasted into a document.

### The requirement's own ordering clause: this lands BEFORE the first consumer deploy

The 2026-08-29 amendment recorded a STANDING CONSTRAINT belonging to no lane: *no further
consumer deploys beyond the landed floor until it is ruled.* That constraint is **still live
and is NOT discharged by this amendment.** What lands here is the contract's STATEMENT; what
the constraint waits on is a RULING on it. The distinction matters because a reader could
otherwise read "the contract is written down" as "the deploy gate is open". It is not, and this
act does not open it.

win-tooling's v1.4.0 floor remains the landed floor, so the constraint continues to bite the
NEXT deploy rather than a past one, and win-tooling's parity role stays **pre-deploy** until the
divergence arc closes — unchanged from 2026-08-29, restated because carrying a constraint
forward by silence is the exact failure this batch refuses.

### R18 stays PARKED — conditions RE-TESTED this window, not carried by assertion

The 2026-08-29 (b) amendment tested R18's two un-parking conditions and found both unmet. Two
days is long enough for either to have moved, and DC-4 requires the parking to be carried on
tested conditions rather than on silence. Both were re-measured 2026-08-31:

- **Condition (a) — the `[#559]` kernel row's leg 1: STILL NOT MET, taxonomy mismatch
  unchanged.** `[#559]` is `status: open` in `tasks/`. Leg 1 requires every `ALL_CHECKS` member
  to carry a `kernel`/`hub` tier; the live tiering is still `[#597]`'s `TIER_COMMIT`/`TIER_SHIP`
  enum in `scripts/audit.py`, and the token `kernel` does not occur in that module at all
  (`grep -c kernel scripts/audit.py` → 0). The `ALL_CHECKS` roster has GROWN since the batch-D
  measurement (`grep -c "_tier(TIER_" scripts/audit.py`), which moves the condition **further**
  from met rather than closer: more checks, none tiered on the axis leg 1 names.
- **Condition (b) — a window with ≥1 birth of headroom: STILL NOT MET.** The 2026-08-30/31
  window birthed `[#624]` and `[#625]`. As in the previous window those births SPENT filing
  capacity; a window that fills its ledger is not a window with headroom in it.

**VERDICT: R18 remains PARKED, on conditions measured this window.** The intake's open question
1 — whether the checker needs a new `fleet.yml` at all, or whether
`ecosystem/organ-registry.yaml` / `ecosystem/deployed-versions.yaml` already carry the consumer
roster — remains the cheap thing to settle first, and remains unsettled. This contract makes
that question sharper rather than answering it: C1–C4 now name exactly four surfaces a
scorecard would read, which is a smaller and far more concrete input than "the fleet's
conformance rules" was two days ago.

### What this amendment does NOT do

- **No row is born.** Not R18, not R19–R23, no `[#id]` consumed. Reconcile-before-birth binds
  this batch, and this act lands ON an ACCEPTED intake rather than beside it.
- **No consumer repo is touched.** The hub states the contract; the DEPLOYMENT WAVE carries it,
  in CUT-1's ruled order.
- **No versioned spec FILE is created.** The operator's requirement names a *versioned spec +
  parity check*; this is **ROOT-CONTRACT v1** and its version lives in this heading. A
  standalone spec file with its own stamp, and a check that reads it, is R18's build — parked
  above. Birthing that file now would create exactly the second registry R19's own reasoning
  argues against.
- **No gap is silently closed.** Four are named — Rule A's absence consumer-side, the missing
  fleet depth leg, the unasserted `explorer.sortOrderReverse`, and the hub-only literal versus
  the fleet glob — and all four are left open ON PURPOSE, each with the surface that would have
  to change.

**Consumed by:** batch E's close packet. **Lane:** `worktree-lane-c-3-root-contract`, contract
`LANE-c-3-root-contract.md` (DC-4).

## AMENDMENT — 2026-09-01: a root `dashboard/` is REQUESTED against ROOT-CONTRACT v1 — recorded, not granted

> **Source:** operator direction, 2026-09-01 (the OBSERVABLE HARNESS), filed under
> *reconcile-before-birth*. Appended, not edited. This amendment lands here rather than on a new
> intake on this file's own 2026-08-29 precedent — *"the root-contract maps to intake #38"* — and
> it **grants nothing**: no directory is created, `SANCTIONED_TIER1_DIRS` is untouched, and no
> ADR-101 amendment is drafted. **The request is recorded so the ruling can read the contract it
> would amend.** ROOT-CONTRACT v1 stands unchanged.

### The request

The OBSERVABLE HARNESS (intake **#66**) places its VIEW layer in a **`dashboard/` directory at the
repo root** — one self-contained HTML file, generated only from `scripts/` + `protocols/` +
`logs/`, openable in VS Code — and asks the operator to sanction it *"via an ADR-101 amendment +
root-contract update"*, with the folder then deploying to every consumer as an organ. `dashboard/`
would be a **sibling of `ecosystem/`**, where both HTML artifacts live today.

### Finding 1 — the request runs directly at C2's standing precedent, and the precedent is six days old

**C2 above** states the rule as *"non-standard files are RELOCATED, not tolerated in place"* and
cites as its **standing precedent** the ADR-101 amendment of **2026-08-26**:

> *"root is sacred, and the docs disease is cured by the consumer gate ([#595]), not by a sibling
> folder at the root."*

That ruling **revoked** the root `prompts/` directory which had been admitted the day before, and
in doing so the closed Tier-1 set took **the first and only contraction in its history**
(`scripts/validate_hermetization.py`, the `prompts` comment block retained deliberately *"so a
reader who finds `prompts/` in the git history must be able to see why it is gone"*). The
replacement home was **inside the genre tree** — `docs/audits/<date>-technical-<batch>-launch-contracts/`.

**This is a conflict, and it is NAMED rather than adjudicated here.** The filer does not rule it,
for the same reason C1 does not: admission is the ADR's channel and the operator's call. Two
readings are available and both are honest — (a) a *generated view surface* is a different class
from a *dispatch-input folder*, so the precedent does not reach it; or (b) the precedent is about
**root siblings as such**, in which case `ecosystem/` is the existing home and the burden is to say
why it will not do. **The direction asserts the sanction but does not argue against the precedent**,
and a ruling made without reading it would be made on half the record.

### Finding 2 — what a root `dashboard/` would actually be checkable by, which is less than it looks

Read against C1's two surfaces and their two honest limits, a `dashboard/` holding **generated**
output is weakly observed:

- **Rule A** (`validate_hermetization.py`) is **prospective and HUB-ONLY** — it would block the
  directory's creation until ADR-101 admits it, and after that inspects nothing. It cannot be the
  fleet instrument for "every consumer carries an identical dashboard organ".
- **The fleet sweep** (`fleet_parity.py::_eval_sweep`) is **retrospective but sees TRACKED entries
  only**. `ecosystem/trends.html` — the artifact the direction moves into this folder — is
  **gitignored** (`.gitignore:84`). **A `dashboard/` containing only generated, ignored output is
  invisible to the sweep by construction**, and a `root-dashboard` parity row would have nothing to
  observe.

**So the sanction and the deploy-as-an-organ clause pull in opposite directions**, and the
contradiction is in the direction itself rather than introduced here: an organ that every consumer
must carry needs a **tracked** artifact for the sweep to see, while the VIEW layer's own
regenerate-on-demand shape argues for an **ignored** one. `ecosystem/conformance.html` is committed
and `ecosystem/trends.html` is ignored, so the two artifacts the folder would hold are **already in
different zone classes today**. Whichever way this is ruled, **it must be ruled for both**, and the
committed branch inherits the currency question intake **#42** records as still unanswered.

### What this amendment does NOT do

- **No directory is created**, and none is authorised. Creating `dashboard/` before ADR-101 admits
  it is exactly what Rule A exists to block, and doing it under a *filing* would be worse than
  doing it under a lane.
- **No amendment to ROOT-CONTRACT v1.** C1–C4 stand as written; this is a request recorded against
  them, and the contract's version does not move.
- **No row is born**, on this file's own reconcile-before-birth precedent.
- **No conflict is resolved.** Finding 1 is left open ON PURPOSE, in the same spirit as the four
  gaps the 2026-08-31 amendment named rather than closed.

## AMENDMENT — 2026-09-01 (b): the root `dashboard/` request is RESOLVED — REFUSED at root, relocated to `docs/dashboard/`

> **Source:** operator ruling, 2026-09-01, same day as and immediately following the amendment
> above. **Appended, not edited** — that amendment recorded a *request*; this one records the
> *ruling on it*, so the record shows what was asked before it shows what was decided. **ROOT-
> CONTRACT v1 is UNCHANGED: C1–C4 stand as written and the contract's version does not move.**

### The ruling, in the terms this file uses

**A root `dashboard/` is WITHDRAWN.** The dashboard is ruled a **per-repo organ** whose home is
**`docs/dashboard/`** — inside the genre tree, not at the root. `ecosystem/dashboard` is withdrawn
in the same act, as **hub-only and therefore non-scalable**: `ecosystem/` is the hub's fleet-facts
tree keyed by consumer repo name, no carrier ships it, and a consumer repo has none, so an organ
placed there could not be per-repo at all.

### Finding 1 is DISCHARGED — and the precedent is UPHELD, not overridden

The amendment above named a conflict and declined to adjudicate it: C2's standing precedent, the
2026-08-26 ADR-101 amendment that **revoked** root `prompts/` on the reasoning *"root is sacred,
and the docs disease is cured by the consumer gate (`[#595]`), not by a sibling folder at the
root"*, against a direction that asserted a root sanction **without arguing against that
precedent**.

**The ruling resolves it by taking the precedent's own remedy rather than its exception.** When
`prompts/` was revoked, its convention was not deleted — it was **relocated under the genre tree**,
to `docs/audits/<date>-technical-<batch>-launch-contracts/`. `docs/dashboard/` is that same move
applied to this request. So the amendment's reading **(b)** — *"the precedent is about root
siblings as such, in which case the existing home is the answer and the burden is to say why it
will not do"* — is the one that holds, with one correction the ruling supplies: the existing home
is **not** `ecosystem/`, and the reason it will not do is that it is hub-only. **The closed Tier-1
set takes no second contraction and no expansion.** `SANCTIONED_TIER1_DIRS` is untouched.

### Finding 2 is HALF DISCHARGED, and the surviving half is named rather than dropped

Finding 2 observed that a root `dashboard/` holding generated output would be weakly observed —
Rule A prospective and hub-only, the fleet sweep retrospective and **TRACKED-only**, and the two
artifacts the folder gathers already in **different zone classes** (`ecosystem/conformance.html`
committed, `ecosystem/trends.html` gitignored).

- **DISCHARGED:** the root-sanction half. There is no root entry, so there is no `root-dashboard`
  parity row that would have had nothing to observe, and the fleet-sweep objection to the *root*
  placement no longer applies to anything.
- **SURVIVING:** the **zone-class** half, which was never about the root. Whether `docs/dashboard/`
  is tracked or ignored is still unruled, still must be ruled **the same way for both artifacts**,
  and the committed branch still inherits the currency question intake **#42** records as
  unanswered. Finding 2's closing sentence — *"whichever way this is ruled, it must be ruled for
  both"* — stands verbatim and is **not** discharged by the relocation.

### What the relocation COSTS against ROOT-CONTRACT v1 — the honest ledger

The move is cheaper than a root admission. It is **not free**, and the difference is a tier, not an
exemption:

- **C1 (the permitted root set is CLOSED) is not engaged at all.** No top-level entry is added or
  removed; Rule A's Tier-1 leg has nothing to say about this request any more.
- **Rule A's TIER-2 leg IS engaged, and it refuses today.**
  `validate_hermetization.py`'s `SANCTIONED_GENRES` is a closed set and **`dashboard` is not a
  member**; an added path under an unsanctioned `docs/<genre>/` is refused with *"unsanctioned new
  docs genre folder"*. **An ADR-101 amendment is therefore still owed** — a Tier-2 genre admission
  against a closed genre set, rather than a Tier-1 fight against the set's only contraction
  precedent. **None is drafted here and the folder is not created.**
- **C2 is satisfied by construction**, and is the reason the ruling reads as it does: relocation
  into the genre tree *is* C2's prescribed remedy.
- **C4 (ordering) is untouched.** The standing constraint the 2026-08-29 amendment recorded — *no
  further consumer deploy before the contract lands* — is neither discharged nor disturbed by this
  ruling, which changes a placement and no sequencing.

### One correction to the record, so a later reader does not inherit it

The ruling states that `docs/dashboard/` *"deploys with the `docs/{intake,handoffs,decisions,
audits,archive}` tree at instantiation"*. **That tree is not a carried payload.** The docs carrier
declares exactly three `doc_paths` pairs in the live manifest — `docs/intake/README.md`,
`templates/intake-template.md`, and the plugin `INSTALL.md` at the consumer root; the other genre
directories are **consumer-created, not shipped**. The clause's useful half survives and is what
makes the placement work: `deploy/carrier_docs.py` is **fully manifest-driven** and hardcodes no
payload, so extending it is *"a manifest edit, not a code change"* (its own docstring). The
correction matters because the same manifest block already rules that this carrier ships
**verbatim, hash-guarded replicas** — right for methodology-generic content, wrong for
repo-specific content, where declaring a pair *"is not a migration, it is a mis-carry"*. **A
rendered dashboard is repo-specific output, so what deploys is the generator and the doctrine, not
the page.** Full statement: intake **#66**'s amendment of this date, §3.

### What this amendment does NOT do

- **No directory is created**, at the root or under `docs/`. `docs/dashboard/` does not exist after
  this commit.
- **No ADR-101 amendment is drafted**, and neither `SANCTIONED_TIER1_DIRS` nor `SANCTIONED_GENRES`
  is touched.
- **No change to ROOT-CONTRACT v1.** C1–C4 stand as written; the contract's version does not move.
- **No row is born**, on this file's own reconcile-before-birth precedent.
- **No ruling on the zone class.** Finding 2's surviving half is left open ON PURPOSE, exactly as
  its predecessor left Finding 1 — and it is now the *only* thing this request waits on here.
