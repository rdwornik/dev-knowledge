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
