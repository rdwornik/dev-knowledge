> **What was asked:** multi-repository configuration standardization and fleet conformance for a solo polyrepo operator -- what Python tooling can and cannot inherit, scaffold re-application (Copier/cruft), drift detection at N=8, settings-as-code, standard versioning, and conformance measurement
> **Provenance:** BROWSER-PRODUCED external research, commissioned and landed 2026-08-17 from `compass_artifact_wf-460fee76-8c63-5cc5-acc5-fe66e2f83a3c_text_markdown.md`. Body is a BYTE-FAITHFUL copy of the source artifact -- this header is the only addition. Home derived per ADR-101 section 1 Tier-2 (`archive/` is in `SANCTIONED_GENRES`) + ADR-60 (`docs/archive/` = pending-classification holding zone); the ADR-101 Rule B audit-class enum has no class for an external research memo. Derivation recorded in full at `docs/audits/2026-08-17-technical-research-intake-lane-contract.md` section 2.
> **EXTERNAL EVIDENCE -- ADVISORY UNTIL RATIFIED. THIS DOCUMENT BINDS NOTHING.** It is not doctrine, not an ADR, not a ruling, and not this repo's own audit evidence. Nothing here becomes binding by virtue of having landed in the tree. Its ratification channel is the intake spine (`docs/intake/2026-08-17-tech-fleet-config-standardization.md`, currently `status: DRAFT`) -- DRAFT -> READY -> ACCEPTED, per `docs/intake/README.md` section 5.

# Multi-Repository Configuration Standardization and Fleet Governance for a Solo Polyrepo Operator

## TL;DR

- **Build a hub-published "standard" as three separable layers — a shared config surface, a Copier template with `copier update`, and a conformance checker that runs in the hub's CI against all 8 repos.** No single tool does all of this; the realistic solo-operator stack is Copier (scaffold + re-apply), a small Python conformance checker (drift detection), and reusable GitHub Actions workflows pinned to a floating major tag (CI uniformity). Policy-as-code engines you already researched are overkill at N=8.
- **The hard technical constraint is that Python tools do NOT support inheriting config from an installed package the way ESLint/tsconfig do** — Ruff's `extend` and mypy/pytest configs can only reference a file path, not a package name, so "one source of truth" for Python config means *distributing a file* (via template re-apply or a copy step), not *importing a package*. This is the single most important finding and it shapes the entire architecture.
- **Cache directories (`.ruff_cache`, `.pytest_cache`, `.mypy_cache`, `__pycache__`, `.venv`) mean nothing about conformance — they are local build artifacts, each relocatable via a per-tool env var or config key, and their presence/absence in a repo is noise, not signal.** Gitignore them and exclude them from your checker; do not treat them as drift.

## Key Findings

- **The mature inheritance model (JS/TS) works because the config format resolves package names; Python's does not.** `tsconfig.json`'s `extends` and ESLint's shareable configs resolve an npm package name at runtime. Ruff, mypy, pytest, and coverage all resolve a *file path* only. The documented Python workaround is to ship a config file inside a PyPI package and run a copy script — the `nickineering-ruff-config` package's own README (PyPI v0.2.0) states verbatim: "You will also need to create a script to copy the file, since Ruff does not support extending from a package."
- **Copier is the correct scaffolding engine for a fleet because it is the only mainstream tool that re-applies a changed template to already-generated repos via a real 3-way merge** keyed on `.copier-answers.yml`. Cruft gives cookiecutter the same capability. Cookiecutter, Yeoman, and GitHub template repos are one-shot: they cannot push a later template change back into existing repos.
- **Drift detection at N=8 is a ~150-line Python script, not a platform.** Repolinter (the obvious off-the-shelf tool) was archived by the TODO Group — todogroup/repolinter (462 stars, 75 forks) "was archived by the owner on Feb 6, 2026. It is now read-only," and its README states "The Repolinter project has been archived." A self-hosted scripted checker that clones each repo and asserts required files/keys is now the pragmatic default. It should run as a scheduled failing job in the hub.
- **For repository *settings* as code, `github/safe-settings` is the strongest self-hostable option** (central admin repo, scheduled reconciliation that reverts out-of-band changes), but it is org-oriented and heavy for one owner; the lighter alternative is the Terraform GitHub provider with a scheduled `terraform plan -detailed-exitcode` as a drift alarm. Both have a real operational hazard: a settings-as-code system will *silently revert* your manual GitHub UI changes.
- **Fleet-standard versioning has two proven models you can copy directly: Renovate config presets (`extends` + `#tag` pinning) and Nx migrations (`migrations.json`).** Renovate untagged presets propagate instantly from the hub's default branch; `#tag` gives controlled rollout ("You can set a Git tag (like a SemVer) to use a specific release of your shared config"). Nx's model — version-keyed migration scripts a consumer runs once — is the reference design for evolving a standard past breaking changes.
- **Golden-path/paved-road literature is unanimous on one point relevant to a solo operator: make the standard the *easiest* path, not a *mandated* one, and record exceptions explicitly with an expiry.** The published target for voluntary adoption is above 80% (Tasrie IT Services' 2026 "Golden Paths" guide: "teams that invest in well-designed golden paths see voluntary platform adoption rates above 80%… The target is greater than 80% voluntary adoption"; the same >80% benchmark appears in the State of Platform Engineering Report Vol. 4, bex.co, Aug 6 2026). The documented failure mode is a standard that ossifies or changes too often and gets routed around.

## Details

### QUESTION 1 — The shared configuration package

**(a) What can and cannot be inherited, per tool.** *(VERIFIED — vendor docs)*

- **Ruff.** Ruff supports a top-level `extend` field that inherits settings from *another config file*: `extend = "../pyproject.toml"`. Critically, Ruff's docs state: "Unlike ESLint, Ruff does not merge settings across configuration files; instead, the 'closest' configuration file is used, and any parent configuration files are ignored." The `extend` value is a **path**, not a package. There is no documented way to write `extend = "some_installed_package"`. The community pattern (e.g. the `nickineering-ruff-config` PyPI package) is to publish a `ruff.toml` inside a wheel and run a copy script; the package's own README states "You will also need to create a script to copy the file, since Ruff does not support extending from a package." Pin the Ruff version explicitly in CI — different Ruff versions silently produce different lint results.
- **mypy.** No `extends`/inherit-from-package mechanism exists. mypy reads a single config file (`mypy.ini`, `.mypy.ini`, `pyproject.toml`, `setup.cfg`, or `~/.config/mypy/config`) with global `[mypy]` and per-module `[[tool.mypy.overrides]]` sections. Sharing means shipping the same file content. `MYPY_CACHE_DIR` relocates the cache.
- **pytest.** Config lives in `pyproject.toml` (`[tool.pytest.ini_options]`), `pytest.ini`, `tox.ini`, or `setup.cfg`. There is no config inheritance across files and no import-from-package. `cache_dir` is a settable ini option.
- **coverage.py.** Config in `.coveragerc`/`pyproject.toml`; no package-inheritance mechanism. (Distribute the file.)
- **pre-commit.** `.pre-commit-config.yaml` references *remote hook repos* pinned by `rev:` (a git tag/SHA) — this is genuine reuse: hooks come from `https://github.com/astral-sh/ruff-pre-commit@<rev>` etc. But there is **no native `include`/`extends`** to pull in another `.pre-commit-config.yaml`; a long-standing feature request (pre-commit issue #2337) confirms this is unsupported. So you can centralize *hook definitions* (each repo lists the same pinned repos) but not *the config file itself* without copying. Community tools like `centralized-pre-commit-conf` copy the config file from a URL. Update propagation is via `pre-commit autoupdate` (bumps `rev`s) or Renovate.
- **GitHub Actions.** Two real reuse primitives. **Reusable workflows** (`uses: owner/repo/.github/workflows/x.yml@ref`, called at job level, triggered by `on: workflow_call`) share whole jobs including matrix and secrets. **Composite actions** (`action.yml` with `runs.using: composite`) share a step sequence inside a job. `{ref}` can be a SHA, tag, or branch; GitHub docs state "Using the commit SHA is the safest option for stability and security." A floating major tag (`@v1`) that you force-push forward is the convention for auto-delivering patches.
- **EditorConfig.** `.editorconfig` has a `root = true` stop marker and cascades from parent directories, but there is no cross-repo inheritance — the file is copied into each repo. It is the simplest thing to standardize and the least likely to drift.

**Versioning/pinning summary:** pre-commit pins by `rev` (tag/SHA); Actions by `@ref` (SHA safest, floating major tag for convenience); Ruff/mypy/pytest have nothing to pin *at the config level* — you pin the *file version* implicitly by whatever mechanism distributes it (template commit, package version, or copy).

**(b) Scaffolding and re-application.** *(VERIFIED — vendor docs)*

- **Copier — the recommendation.** Copier records `.copier-answers.yml` (template URL, version tag, answers) in each generated repo. `copier update` "checks out the old template version, renders it with your saved answers to produce the 'old generated' state, checks out the new template version and renders it, computes a diff between old-generated and new-generated, and applies that diff to your working tree using a three-way merge." Template versions are Git tags compared with PEP 440; `copier update` checks out the latest tag by default (`--vcs-ref=HEAD` for latest commit). Conflicts are handled by `--conflict inline` (default; git-style conflict markers) or `--conflict rej` (`.rej` files). **Documented limits/failure modes:** (1) update only works with a known baseline — there is *no* first-class path to "adopt" an existing, non-template repo (open issue #2486; the synthetic-baseline `copier adopt` is still a proposal); (2) any file that "evolved" in the template shows as a "conflict" even if the consumer never touched it; (3) files marked to skip on update are excluded from the 3-way merge.
- **cruft** gives the same lifecycle to *cookiecutter* templates: stores `.cruft.json` with the template commit hash; `cruft check` (exit 1 if behind — CI-friendly), `cruft diff`, `cruft update` (3-way-style merge, standard conflict resolution), `cruft link` to attach an existing project. A scheduled GitHub Action can open a `cruft/update` PR automatically.
- **Cookiecutter, Yeoman, GitHub template repositories, Backstage software templates** are all **one-shot generators**: they create a repo and forget it. None can re-apply a later template change to existing repos. Backstage templates are the enterprise scaffolding-portal option (catalog metadata via `catalog-info.yaml`) but are far too heavy for a solo operator.
- **Which can RE-APPLY:** only **Copier** and **cruft**. Everything else requires a codemod tool (which you've already researched) to push changes into existing repos.

**(c) Monorepo vs polyrepo for standardization.** *(Community convention + practitioner blogs — evidence is experiential, not peer-reviewed)*

The widely repeated claim is true but conditional: a monorepo makes standardization trivial *because there is one config, one CI, one toolchain by construction* — but it imposes migration cost and coupling. For a fleet of 8 genuinely independent projects (a CLI, an ops toolbox, a life-management repo, etc.), the projects "are independent and teams need autonomy… different release schedules," which is the textbook polyrepo case. Practitioner consensus: "Start with a polyrepo for small teams (<20 engineers)." Migration to a monorepo is not free (history rewrites, build-tool adoption like Nx/Bazel/Pants). **Recommendation: stay polyrepo; treat the hub as a *platform repo* the consumers reference, not a monorepo to absorb them.**

Hybrid patterns and multi-repo operators:
- **git submodules** — pin a shared "platform" repo at an exact commit; well-documented pain: detached-HEAD editing, easy-to-forget `git submodule update --init`, CI friction. "Great for shared, stable dependencies. Painful if you're actively developing both projects." Given your LLM-agent worktree workflow, submodules will fight the agents.
- **git subtree / subrepo** — vendors the shared repo's content into the consumer; simpler for contributors, harder to push changes back upstream.
- **Multi-repo runners:** `meta` (Node; `.meta` file, `meta git ...` across all repos), `mu-repo`, `gita` (Python; `gita ll` status board, groups), `vcstool`/`vcstool2` (YAML manifest of repos, `vcs status/import/export`), and `mani` (Go; config-file + run commands over subsets). For 8 repos on Windows, **`gita` or a hand-rolled `git-all` loop** is the lowest-friction inventory/fan-out tool.

### QUESTION 2 — Drift detection and conformance

**(a) Lightweight "which repo deviates and how?"** *(Mixed: Repolinter VERIFIED but archived; scripted approach is community convention)*

- **Repolinter** (TODO Group) was the canonical off-the-shelf answer: JSON/YAML rulesets, `file-existence`/content checks, `repolinter lint --git <url>`, markdown report output, non-zero exit on failure, tiered rulesets (see DSACMS `repo-scaffolder`'s tier 0–4 `repolinter.json`). **But the repository was archived on Feb 6, 2026 and is now read-only** — use with caution as unmaintained.
- **The pragmatic default at N=8 is a scripted checker** (see "The smallest first build"). It clones/fetches each repo, asserts required files (CLAUDE.md, AGENTS.md, runbooks, gate configs), folder taxonomy, presence of config keys, hook installation, and CI workflow presence, then emits a scorecard. Present results as (1) a Markdown scorecard committed to the hub, and/or (2) a failing CI job in the hub that blocks on regressions.

**(b) Repository settings as code.** *(VERIFIED — vendor docs)*

- **`github/safe-settings`** — a Probot app; all settings live centrally in an `admin` repo (org/suborg/repo tiers via `.github/settings.yml`, `.github/suborgs/`, `.github/repos/`). It runs event-driven *and* on a `node-cron` schedule to "prevent configuration drift," and it actively reconciles: "Syncs teams and collaborators for human changes… User grants admin access manually → Safe Settings reverts to configured permission." It is protected against privilege escalation (unlike the older `probot/settings`). Strong, but org-scale and requires hosting a bot.
- **`probot/settings`** — reads `.github/settings.yml` from *each repo*; simpler but lets repo-writers change their own settings (no privilege protection).
- **Terraform GitHub provider / Pulumi** — declare repos, branch protection, rulesets, collaborators as code. Drift detection is via scheduled `terraform plan -detailed-exitcode` (exit 2 = drift); a non-empty diff means someone changed something out-of-band. **Critical caveat:** `plan` catches out-of-band changes only when you run it (schedule it — "Drift that enters the infrastructure on a Tuesday does not get caught until the next pipeline run"), and `apply -auto-approve` can *reconcile destructively* — a documented Terraform outage occurred when auto-apply chose destroy-and-recreate to reverse a one-way-door attribute change. Never pair fleet settings automation with unattended auto-apply.
- **Org-level defaults / GitHub rulesets** (already in your prior report) are the native, no-hosting option for branch/tag protection across repos.
- **Operational risk (all of them):** a settings-as-code system *fights manual changes* — the whole point is that it reverts them. For a solo operator this is usually desirable, but it means the GitHub UI stops being a source of truth; every change must go through the code path or it vanishes on the next reconcile.

**(c) Versioning a fleet standard.** *(VERIFIED — vendor docs, via targeted research)*

- **Renovate config presets — the closest ready-made model.** A central repo publishes a preset; consumers put it in an `extends` array: `{ "extends": ["local>owner/repo"] }` (or `github>owner/repo`). Renovate docs: "If you manage multiple repositories… you might want to consider publishing your own preset config so that you can 'extend' it in every applicable repository. That way when you want to change your Renovate configuration you can make the change in one location." **Versioning:** "You can set a Git tag (like a SemVer) to use a specific release of your shared config" via `#tag` — `github>abc/foo#1.2.3`. Untagged presets track the preset repo's default branch (instant propagation to all consumers); `#tag` freezes a consumer to a release (controlled rollout). A pinned tag is inherited by relative sub-preset references, so `github>org/repo#v2.0.0` reads all its sub-presets at `v2.0.0`. npm-hosted presets are officially deprecated ("We deprecated npm-based presets. We plan to drop the npm-based presets feature in a future major release"). Docs correspond to Mend Renovate 44.32.0. **This `extends` + `#tag` pattern is directly transferable to how your hub should declare "standard v3" and how consumers pin to it.**
- **Nx migrations — the reference design for breaking changes.** `nx migrate latest` writes a `migrations.json` of version-keyed migration scripts; `nx migrate --run-migrations` applies them; it's idempotent and re-runnable, and the recommended process is "at most one major version at a time." A package declares migrations via `nx-migrations` in `package.json` pointing at `migrations.json`, whose entries key on a `version` (with optional `requires` peer-version guards and `packageJsonUpdates` for dependency-only bumps). For your hub, the analog is: ship a `migrations/` folder of dated/versioned scripts a consumer runs once to move from standard vN to vN+1. (Nx docs cited correspond to Nx v23.)
- **Backstage catalog metadata** records which template/version a component came from in `catalog-info.yaml` (enterprise-scale; overkill here).
- **Platform-engineering "golden path" versioning guidance:** treat the golden path "as a product, not a launch," measure adoption, and evolve templates — but don't change so often that consumers can't keep up.

**How a consumer declares conformance / detecting a stuck consumer:** the concrete mechanism is the `.copier-answers.yml`/`.cruft.json` recorded template version (a `cruft check` / `copier` diff tells you which repo is behind), plus a `STANDARD_VERSION` field your checker reads. A consumer stuck on an old version is detected by comparing its recorded version to the hub's current tag.

### QUESTION 3 — Developer environment and toolchain uniformity

**(a) Identical toolchain across machines.** *(VERIFIED vendor docs + community for Windows specifics)*

- **uv — your anchor for Python uniformity.** `uv.lock` "pins every transitive dependency to an exact version and records platform-specific resolution so that uv sync produces identical environments on macOS, Linux, and Windows"; commit it. `uv python pin 3.x` writes `.python-version`; `uv sync --check`/`uv lock --check`/`uv run --locked` fail non-zero on drift (CI-friendly). Note: `uv.lock` is resolved against `requires-python`, not the pinned dev version, so changing `.python-version` within range leaves the lock valid; editing `requires-python` triggers re-resolve. Pin the uv version itself in CI.
- **devcontainers** (`devcontainer.json` + Features + prebuilds; devcontainer CLI for local/CI use) give a fully reproducible Linux environment. **Windows reality:** run them on the **WSL2 backend of Docker Desktop** ("less susceptible to file sharing issues"); keep the project folder *inside* the WSL2 filesystem, not `/mnt/c`, for performance. Documented gotchas: line-ending churn (fix with `.gitattributes`), Git credential forwarding needs `credential.helper` set on the host, SSH keys with passphrases need `ssh-agent` on the host, and commit `.devcontainer/` (don't gitignore it).
- **mise / asdf** (`.tool-versions`) manage multiple tool runtimes; mise is the more actively developed successor. asdf's core is POSIX-shell and historically weak on native Windows (works best under WSL2).
- **Nix/direnv** give the strongest reproducibility but the steepest curve and poor native-Windows story (WSL2 only) — not recommended for a Windows-primary solo operator.
- **Windows bottom line:** the reliable stack is **native uv for day-to-day Python** (uv is first-class on Windows) plus **WSL2 for anything containerized or hook-heavy**. Git hooks and shell-based pre-commit hooks are the most common native-Windows friction point; running pre-commit inside WSL2 or via Python (not bash) avoids most of it.

**(b) Cache directories and generated artifacts — precise answer.** *(VERIFIED — vendor docs)*

| Tool | Default location | Relocate via |
|---|---|---|
| Ruff | `.ruff_cache/` in project root | `cache-dir` config key or `RUFF_CACHE_DIR` env var |
| pytest | `.pytest_cache/` in rootdir | `cache_dir` ini option |
| mypy | `.mypy_cache/` | `cache_dir` config key or `MYPY_CACHE_DIR` env var |
| CPython bytecode | `__pycache__/` next to sources | `PYTHONPYCACHEPREFIX` env var (centralizes all bytecode); `PYTHONDONTWRITEBYTECODE=1` disables |
| coverage.py | `.coverage` data file | `[run] data_file` in config or `COVERAGE_FILE` env var |
| uv | project `.venv/` | `UV_PROJECT_ENVIRONMENT` / `--python`; uv's own cache via `UV_CACHE_DIR` |

There is an active proposal (discuss.python.org) for standard `cache-dir`/`config-dir` keys in `pyproject.toml` "so tools stop littering the project root" — but as of now it's **N separate settings for N tools, with no shared default**. **Does presence/absence mean anything? No.** These are local, regenerable build artifacts. A repo missing `.ruff_cache` just hasn't run Ruff yet on that machine; a repo that has one has. **Do NOT treat cache dirs as conformance signal** — gitignore them and have your checker skip them. Standard hygiene: one gitignore block (`__pycache__/`, `*.py[cod]`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.coverage`, `htmlcov/`, `.venv/`), and a cleanup tool like `cleanpy` for bulk removal.

**(c) Identical CI across repos.** *(VERIFIED — GitHub docs, via targeted research)*

- **Reusable workflows beat copied YAML.** Put one "standard CI" workflow in the hub (`on: workflow_call`), and have each consumer call it: `uses: owner/hub/.github/workflows/ci.yml@v1`. Consumers pass a matrix and inputs. This is the DRY answer for N repos.
- **Rollout safely (canary → fleet):** GitHub's versioning model enables this even though it doesn't use the word "canary." Publish an immutable tag (e.g. `v1.3.0` or a `v2-beta`); point **one canary repo** at that exact tag/SHA; validate; then **force-push the floating `@v1` tag forward** so the rest of the fleet picks it up on their next run. The floating major tag is *not moved automatically* — you (or an automation) must re-point it: `git tag -fa v1 -m "..." && git push origin v1 --force` (confirmed in GitHub community discussion #130777). GitHub recommends SHA-pinning as "safest"; the floating tag trades reproducibility for automatic patch delivery. The actions/toolkit guidance endorses staged rollout via `release/v1` branches and `v2-beta` prerelease tags.
- **Detecting silent CI divergence:** GitHub has **no turnkey drift detector.** Detection options: the workflow-run REST API surfaces which reusable-workflow file/ref each run used; GitHub Enterprise Cloud can query the audit log for workflow usage ("Organizations that use GitHub Enterprise Cloud can interact with the audit log via the GitHub REST API to monitor which workflows are being used"). For a solo operator, the practical detector is your **fleet conformance checker scanning each repo's `.github/workflows/*.yml` for the pinned `@ref`** and flagging any repo not on the current standard tag (or one that has a local, non-reusable CI file).

### QUESTION 4 — Onboarding and measuring conformance

**(a) Onboarding runbook.** *(Community/platform-engineering convention)*

A repeatable onboarding = **template + bootstrap + gate**: (1) generate from the Copier template (gets folder taxonomy, `pyproject.toml`, gitignore, `.editorconfig`, `.pre-commit-config.yaml`, CI caller workflow, CLAUDE.md/AGENTS.md, runbook stub, and a recorded standard version); (2) a bootstrap script runs `uv sync`, `pre-commit install`, and registers the repo in the hub's fleet manifest; (3) the conformance check must pass before the repo is "in the fleet." The minimum file set a new repo must have is exactly what your checker asserts — that's the definition of "in the fleet."

**(b) Measuring conformance over time — and avoiding vanity metrics.** *(Platform-engineering literature)*

- Report a **percent-conformant scorecard** and/or **maturity tiers** (the DSACMS tier 0–4 model is a concrete template). Track per-repo pass/fail per rule over time.
- **Avoiding the vanity trap:** the golden-path literature is explicit that the metric that matters is *voluntary adoption* ("the first metric we look at is voluntary adoption rate… The target is greater than 80% voluntary adoption"), not raw checkbox counts. A scorecard becomes vanity when it measures presence of files rather than whether the standard actually made the repo easier to work in. Pair the conformance % with a "did this help" signal (e.g., time-to-onboard, number of exceptions requested).
- CNCF's platform-engineering maturity model exists as an external ladder if you want a published rubric; DORA's 2024 *Accelerate State of DevOps* report quantifies the trade-off that a platform is not automatically a win: internal developer platforms raised individual productivity ~8% and team productivity ~10%, but were associated with an ~8% decrease in change throughput and a ~14% decrease in change stability when poorly implemented — a standard that adds friction is a net negative.

**(c) Documented failure modes and mitigations.** *(Platform-engineering literature + security-governance convention)*

- **Ossification / changing too often:** golden paths rot when teams "treat it as a launch, not a product… the moment real use leaves the happy path." Mitigation: version the standard (Renovate/Nx model) and give deprecation windows.
- **Mandating instead of paving:** "A good golden path is the fastest way to ship, not a fence. If the paved road is slower than the workaround, you built a speed bump." Developers "route around the platform." Mitigation: make conformance the easy default, not a gate that blocks legitimate work.
- **Legitimate exceptions → record, don't silently diverge.** Use an **exception registry / waiver with expiry**. A policy waiver "must record the request, approval, scope and expiry or revisit point, otherwise it becomes an undocumented bypass." The concrete pattern (mirroring Azure Policy exemptions, which use an `expiresOn` ISO-8601 date and retain the object for record-keeping after expiry while no longer honoring it): each entry has a unique ID, the affected repo/rule, a reason, and an expiry date. For your fleet: a `fleet-exceptions.yml` in the hub that the checker reads — a repo failing a rule it has an unexpired waiver for is reported as "waived," not "failing"; an expired waiver flips back to failing.
- **Opt-in tiers** let a repo declare a conformance tier (e.g., core vs. full) so a lightweight repo isn't held to the same bar as a production one.

## Recommendations

**Stage 1 — one work session (do these first):**
1. **Write the conformance checker** (sketch below) and wire it as a scheduled + manual GitHub Actions job in the hub that iterates all 8 repos via the GitHub API/clone and emits a Markdown scorecard. This gives you *visibility* before you change anything — you cannot fix drift you can't see.
2. **Standardize the zero-inheritance-cost artifacts immediately:** a single `.editorconfig`, `.gitignore` (with the cache block), and `.pre-commit-config.yaml` with pinned `rev`s. These are pure file-copy and instantly reduce drift.
3. **Pin uv + Python:** ensure every repo has `.python-version` and a committed `uv.lock`; add `uv sync --check` to each repo's CI.

**Stage 2 — second work session:**
4. **Build a Copier template** capturing the canonical folder taxonomy, config files, CLAUDE.md/AGENTS.md, runbook stubs, and a recorded `standard_version`. Adopt existing repos into it (accept the manual first-adoption cost — Copier has no clean `adopt` yet; expect to hand-resolve the first `copier update`).
5. **Extract one reusable CI workflow** in the hub; convert one *canary* repo to call it at a pinned tag; validate; then roll to the rest at a floating `@v1`.
6. **Create `fleet-exceptions.yml`** with waiver IDs + expiry dates, and teach the checker to honor unexpired waivers.

**Stage 3 — ongoing:**
7. **Version the standard** (`standard v1/v2/...` as git tags on the hub). Roll breaking changes via a Copier template bump + an `nx migrate`-style migration note; detect stuck consumers by comparing each repo's recorded version to the hub tag.
8. **Consider `github/safe-settings` or the Terraform GitHub provider** *only if* branch-protection/settings drift becomes a real problem — start with native org rulesets. Never run settings auto-apply unattended.

**Thresholds that change the plan:** if the fleet grows past ~20 repos or gains other contributors, graduate the scripted checker to a policy-as-code engine (OPA/Conftest) and codemod rollout (multi-gitter/git-xargs) — the tools from your prior report. If cross-repo *code* changes become frequent and tightly coupled, reconsider a monorepo with Nx. Below those thresholds, the scripted/Copier/reusable-workflow stack is correct.

## The smallest first build

**One minimal concrete artifact per question:**

- **Q1 (shared config):** a single hub-owned **`.pre-commit-config.yaml` + `.editorconfig` + `.gitignore`** trio distributed by the Copier template. Accept that Python tool config is *copied*, not *imported* — do not waste time trying to make Ruff/mypy import a package; it cannot.
- **Q2 (drift):** the conformance checker (below).
- **Q3 (environment):** `.python-version` + committed `uv.lock` + `uv sync --check` in CI in every repo.
- **Q4 (onboarding):** the Copier template + a `bootstrap.ps1`/`bootstrap.sh` that runs `uv sync && pre-commit install` and appends the repo to the hub's fleet manifest.

**Concrete sketch of the fleet-conformance checker (8 private Python repos, one owner, Windows):**

- **Form:** a small Python CLI in the hub (`fleet_check.py`), run with `uv run`, dependency-light (`PyGithub` or the `gh` CLI + `tomllib` + `PyYAML`).
- **Input:** a `fleet.yml` manifest listing the 8 repos and each repo's declared conformance tier and `standard_version`; a `fleet-exceptions.yml` waiver registry (id, repo, rule, reason, `expiresOn`).
- **What it asserts, per repo (via shallow clone or the GitHub contents API):**
  - **Required files present:** `pyproject.toml`, `.python-version`, `uv.lock`, `.pre-commit-config.yaml`, `.editorconfig`, `.gitignore`, `README.md`, `CLAUDE.md`, `AGENTS.md`, a `runbooks/` (or docs) dir, and the CI caller workflow under `.github/workflows/`.
  - **Folder taxonomy:** expected top-level layout (e.g. `src/`, `tests/`).
  - **Config keys present & correct:** `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]` blocks exist and key settings (line-length, target-version, strictness) match the standard's expected values; parse `pyproject.toml` with `tomllib`.
  - **Hook installation:** `.pre-commit-config.yaml` lists the standard hook repos at the standard pinned `rev`s.
  - **CI presence & version:** the workflow calls the hub's reusable workflow at the **current** `@vN` tag (flag any repo on an old tag or with a bespoke, non-reusable CI file).
  - **Gitignore hygiene:** the cache block is present (so artifacts stay untracked) — but **never** assert on the *existence* of cache dirs themselves.
  - **Standard version:** the repo's recorded `standard_version` (from `.copier-answers.yml` or a `STANDARD_VERSION` file) equals the hub's current tag; flag "stuck on vN".
- **How it reports:** exit non-zero on any unwaived failure (so it can gate); emit (1) a `CONFORMANCE.md` scorecard table committed to the hub (repo × rule, ✅/❌/🟡-waived, plus a per-repo % and a fleet %), and (2) a job-summary in the Actions run. Honor `fleet-exceptions.yml`: an unexpired waiver renders 🟡 not ❌; an expired waiver reverts to ❌ and is itself reported.
- **Where it runs:** as a **scheduled (e.g. weekly) + manually-dispatchable GitHub Actions workflow in the hub**, using a PAT/GitHub App token scoped to the 8 private repos. It runs on `ubuntu-latest` (fast, no Windows needed for the check itself even though you develop on Windows). Locally, `uv run fleet_check.py` gives the same scorecard on demand.

This is buildable in one focused session, needs no external platform, scales fine to a few dozen repos, and turns "the consumers have drifted" from a vague worry into a dated, per-rule, waiver-aware scorecard.

## Caveats

- **Repolinter is archived** (Feb 6, 2026, read-only) — I recommend the scripted checker over adopting an unmaintained tool, but note the DSACMS tiered-ruleset model remains a useful design reference.
- **Copier has no clean "adopt existing repo" path yet** (`copier adopt` is an open proposal, issue #2486); onboarding your 8 *existing* repos into the template will involve manual first-merge effort — this is the biggest one-time cost in the plan.
- **Python config genuinely cannot inherit from a package** — this is a hard limitation confirmed across Ruff/mypy/pytest docs, not a gap I could engineer around; every "shared Python config package" in the wild ships a file + copy step.
- **Settings-as-code will revert your manual GitHub changes** — desirable when intended, dangerous when forgotten; and Terraform auto-apply can be *destructive* on reconcile. Schedule `plan` as an alarm; do not auto-apply unattended.
- **Golden-path adoption evidence** (80%+ voluntary-adoption targets; DORA's ~8%/~10% productivity gains vs. ~8% throughput / ~14% stability decreases when poorly implemented) comes from enterprise platform-engineering contexts with many teams; the *mechanisms* transfer to a solo operator but the *numbers* are not calibrated for N=1 and should be read as directional, not as benchmarks you must hit.
- **Some cited how-to material is single-blog or vendor-marketing** (dev.to, Medium, tool vendors' own comparison posts); I've leaned on primary docs (Astral/Ruff, mypy, pytest, Copier, cruft, GitHub, Renovate, Nx, uv) for every load-bearing claim and flagged the softer sources inline.
- **Dates/versions:** Renovate docs cited correspond to Mend Renovate 44.32.0; Nx migration docs to Nx v23; mypy docs to 2.x. Tool behaviors can change — re-verify the exact `extend`/`#tag`/`@ref` syntax against current docs before building.