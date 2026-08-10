# Enforcing a Universal Code-Style Doctrine Across an LLM-Written Python Fleet

## TL;DR
- **Mechanize almost everything, write down almost nothing.** For a 5–6 repo Python fleet written mostly by LLM agents, the enforceable core is a shared, versioned config package (ruff + a type checker) + count-based ratchets + import-linter contracts + a PostToolUse lint hook + a pre-dispatch prompt checker. The "philosophy" (OO vs functional) is mostly taste; the only enforceable slice is function/module size, complexity ceilings, naming rules, and import boundaries.
- **Pick one paradigm doctrine and enforce only its measurable shell.** "Functional core, imperative shell" (from Cosmic Python) is the right written doctrine for your fleet; "Functional Programming in Scala" is a mismatch — the Python-native equivalents are *Effective Python*, *Fluent Python*, and Cosmic Python. Ousterhout's *A Philosophy of Software Design* is a better source-of-truth than *Clean Code* (whose short-function/comment rules are widely contested).
- **Your existing "silent_rule_ratchet" is already best practice — extend it, don't refactor blindly.** Before any big refactor, run a churn-vs-complexity hotspot analysis; the evidence says big-bang rewrites usually fail and incremental "strangler fig" + opportunistic refactoring on hotspots is the safer, better-supported path. Only refactor where high churn meets high complexity.

---

## Key Findings

1. **Style/paradigm choice is mostly unenforceable taste.** Respected sources (PEP 8/20/257, Google Python Style Guide) legislate *mechanics* (naming, imports, comprehensions-on-one-line, lambdas-for-one-liners) but deliberately avoid mandating OO vs functional. The one enforceable paradigm rule is structural: bounded function/module size and a complexity ceiling.
2. **The mechanical toolchain is mature and Rust-fast in 2026.** ruff consolidates dozens of linters (including pylint refactor rules, mccabe, pep8-naming); import-linter and tach enforce architecture; radon/xenon/wily measure complexity trends; deptry catches dependency drift; semgrep is the mechanical form of LIBRARY-FIRST.
3. **Ratchets are the proven "never worse than today" mechanism** (mypy-baseline, diff-cover, count baselines) but have real failure modes (Goodhart's law, freeze-on-refactor).
4. **Hooks beat prompts for agents.** The 2026 consensus, articulated by practitioner Chirag Hasija ("Claude Code Hooks vs CLAUDE.md — When to Use Which in 2026"): "CLAUDE.md instructions get roughly 80% compliance… Hooks get 100% compliance. A PostToolUse hook that runs prettier after every file write will fire every single time. No exceptions. No 'it forgot.' The hook is a script on disk, executed by the Claude Code harness, not by the LLM." This exactly matches your "instructions are requests, MECHANISMS are guarantees" doctrine.
5. **Cross-repo consistency is best done via a published config package + template propagation (copier/cruft)**, not copy-paste.
6. **Fleet aggregation can be done cheaply** with self-hosted radon/wily/ruff-JSON collection; SonarQube Community is heavier and single-branch.
7. **Big-refactor decisions should be data-driven** (hotspots, complexity distribution, coverage on hotspots) — not vibes.

---

## Details

### Q1. Paradigm doctrine for Python — what's a source of truth vs. taste

**MECHANISM (enforceable):**
- **PEP 8** (style/naming), **PEP 257** (docstrings), **PEP 20** (Zen — aspirational but quotable). ruff enforces the mechanical subset directly.
- **Google Python Style Guide** is the most *decision-oriented* written source: it gives explicit, falsifiable rules — comprehensions/generators only if they fit on one line and have no more than one `for` clause; lambdas "okay for one-liners" and if longer than 60–80 chars use a named nested function; prefer `operator.mul` over `lambda x,y: x*y`; use list comprehensions/for-loops instead of `filter`/`map` with inline lambdas, and for-loops instead of `reduce`; global variables strongly discouraged. These map cleanly onto ruff rules and are the parts worth copying verbatim into your doctrine.

**TASTE (write down briefly, don't try to gate):**
- **OO vs functional vs procedural.** No respected source mandates one. The enforceable proxy is *consistency of structure*, not paradigm: cap function/module length, cap complexity, forbid deep nesting, require typed public interfaces. That prevents the "agent drifts between OO and functional" failure without adjudicating taste.
- **A Philosophy of Software Design (Ousterhout) vs Clean Code (Martin).** Genuinely useful as written doctrine: Ousterhout (deep modules, information hiding, complexity as the enemy) is more evidence-based and less dogmatic — the community consensus (and the published Ousterhout–Martin debate on GitHub) leans toward Ousterhout. **Clean Code is contested**: its rules that functions should be very short (2–4 lines) and that code should be self-documenting with minimal comments are widely criticised as producing "lasagna code" (too many thin layers) and losing the "why" that comments capture. **Present both; do not encode Clean Code's short-function rule as a gate** — it conflicts with Ousterhout's "deep modules."
- **Architecture Patterns with Python (Percival & Gregory, "Cosmic Python")** is the right architectural source-of-truth for your fleet: ports & adapters (hexagonal), repository/unit-of-work, and especially **"functional core, imperative shell."** That last phrase is the single best one-line paradigm doctrine you can adopt: pure logic in the core, side effects at the edges. Caveat from practitioners (Hacker News threads on the book): full DDD/ports-and-adapters can be over-engineering and can make code "way too complex and unnecessarily slow" for small tools — apply it to the monorepo and AI-council CLI, not necessarily the small Windows/ops toolboxes.
- **Effective Python (Slatkin)** and **Fluent Python (Ramalho)** are the correct *idiom* references — item-based, Python-native, enforceable in spirit through ruff (SIM, RET, C4, PERF, UP, RUF families).

**Explicit answer on Functional Programming in Scala (Chiusano & Bjarnason):** it is a **mismatch** as a source of truth for a Python fleet. Its type-driven FP (typeclasses, higher-kinded types, effect systems, `IO` monads) has no idiomatic Python equivalent and actively fights Python's culture (Google explicitly steers away from `reduce`/heavy lambda/recursion). The **Python-native equivalent** is: *Effective Python* + *Fluent Python* for idiom, *Cosmic Python* for the "functional core, imperative shell" discipline, and — if you want library support for FP patterns — the `returns` or `toolz` libraries (LIBRARY-FIRST compliant), but adopt those only with a measured divergence justification since they push a non-idiomatic style your LLM agents may not reproduce consistently.

**Adoption cost:** S (writing a 1-page doctrine); the value is in the *gates below*, not the prose.

---

### Q2. Mechanical enforcement of style and structure

**ruff (Astral) — the hub of the toolchain. MECHANISM. Cost: S.**
Actively maintained, Rust-fast, consolidates flake8+isort+pylint-subset+pyupgrade+more. (Note the ownership context: OpenAI announced it is acquiring Astral — the makers of ruff/uv/ty — reported Feb 2026; this does not change ruff's open-source status but is worth tracking.) Relevant rule families:
- **Complexity/size:** `C901` (mccabe cyclomatic, `max-complexity`), `PLR0911` (too-many-returns), `PLR0912` (too-many-branches), `PLR0913` (too-many-arguments), `PLR0915` (too-many-statements, default 50), `PLR0904` (too-many-public-methods), `PLR1702` (too-many-nested-blocks). These directly attack "over-long unreadable modules."
- **Naming:** `N` (pep8-naming) — enforces class/function/constant naming consistency, killing "inconsistent naming" drift.
- **Design smells:** `PLR2004` (magic values), `SIM` (simplify), `RET` (return consistency), `ARG` (unused arguments), `TRY` (exception anti-patterns), `ERA` (commented-out code), `FURB` (refurb modernizations), `B` (bugbear).
- **Import discipline:** `I` (isort), `TID` (banned/relative imports), `TC` (type-checking imports).
- **Per-file ignores + gradual ratchet:** teams use `[tool.ruff.lint.per-file-ignores]` for tests/scripts (commonly ignoring `S101`, `PLR2004`, `PLR0913`, `PLR0915` in tests) and enable rule families incrementally.
- **What ruff CANNOT do:** ruff's complexity rules measure *structural* (branch/statement counts), not *cognitive* complexity (nesting-weighted). It does not do cross-file/architecture analysis, cross-file duplicate detection, or type checking. (A known edge case: ruff currently treats `match`/`case` as a single statement for `C901`/`PLR0912`/`PLR0915`.)

**complexipy — cognitive complexity. MECHANISM. Cost: S.** Complements ruff: ruff's `PLR0912` catches "wide" functions (many branches); complexipy catches "deep" functions (heavy nesting) via cognitive-complexity scoring with a `--max-complexity-allowed` gate. Optional add-on.

**radon / xenon / wily — complexity metrics & trend. MECHANISM (xenon) + REPORTING (radon/wily). Cost: S–M.**
- **radon**: reporting tool — cyclomatic complexity (A–F grades), maintainability index (MI), Halstead, raw LOC. Note: radon's own docs (radon.readthedocs.io, "Introduction to Code Metrics") warn that "Maintainability Index is still a very experimental metric, and should not be taken into account as seriously as the other metrics" (echoing van Deursen's "Think Twice Before Using the Maintainability Index"). radon's last PyPI release predates 2024, so treat it as stable-but-quiet.
- **xenon**: the *enforcement* wrapper around radon — exits non-zero when thresholds (per-block/module/average grade) are exceeded. This is your hard ceiling.
- **wily**: git-history trend tool — `wily build` indexes revisions, `wily rank`/`wily graph` show complexity trends over time; supports cognitive complexity. This is your trend ratchet. Caveat: wily's maintenance cadence is slower; validate before adopting fleet-wide.

**Module-boundary / layering — MECHANISM. Cost: M.**
- **import-linter (seddonym)** — **actively maintained; latest 2.13, uploaded Jul 3, 2026 on PyPI**, Development Status "5 - Production/Stable," officially supporting Python 3.10–3.14. Declarative "contracts" (forbidden, layers, independence) checked against the import graph (built on grimp/NetworkX). This is the cleanest way to enforce "functional core, imperative shell" and "zero invented paths": e.g., forbid `domain` importing `infrastructure`. Works with pre-commit. **This is my recommended layering tool.**
- **tach** — Rust-based module-boundary + public-interface (`__all__`) enforcement. **Caution on maintenance:** the original `gauge-sh/tach` was effectively abandoned mid-2025 (Cory Donnelly's blog noted on 2025-06-03 that "Tach is no longer being maintained"); a community continuation at `tach-org/tach` has since shipped releases (0.34.1, ~Apr 2026). Given a governing hub and the need for stability, **prefer import-linter** unless you specifically need tach's public-interface enforcement.
- **pydeps** — dependency graph *visualization* (not enforcement); useful for the initial refactor assessment.
- **deptry (osprey-oss)** — **actively maintained; latest 0.25.1, released Mar 18, 2026** (per the release notes, "Release 0.25.0 was yanked in PyPI because of a failure during the release. 0.25.1 is identical, but includes a fix… deptry has moved from fpgmaas/deptry to osprey-oss/deptry under the new Osprey OSS organisation"). Finds unused (DEP002), missing (DEP001), transitive (DEP003), and misplaced (DEP004) dependencies. Supports uv/PEP 621 natively — fits your stack. This is a direct LIBRARY-FIRST enforcer: it catches "declared but unused" and "imported but undeclared." FawltyDeps is an alternative.

**Duplication detection — MECHANISM. Cost: S–M.**
- **jscpd** — Rabin-Karp copy/paste detector, 223+ formats incl. Python, now Rust-powered, emits SARIF, has a `--threshold` to fail CI and a GitHub Action. Set `min-tokens`/`min-lines` and a threshold. This catches agents re-implementing the same helper in multiple files.
- **pylint's `duplicate-code` (R0801)** — built-in but slower; ruff does not yet implement cross-file duplicate detection.
- **semgrep custom rules — the mechanical form of LIBRARY-FIRST.** Write rules like "don't hand-roll X, use Y": ban a deprecated/hand-rolled function and point to the library equivalent, ban direct imports that should go through a facade, enforce naming with `metavariable-regex`. Semgrep is widely used for exactly this (coding standards, API-usage, architectural constraints) and can fail CI (exit 1) or comment on PRs. This is the highest-leverage tool for stopping agents "inventing their own utilities."

**Type discipline — MECHANISM. Cost: M.**
- **mypy** — the reference checker; largest stub ecosystem; `# type: ignore[code]` best understood; plugin API (Django etc.). mypy 2.0 (2026) added parallel checking (`--num-workers`) and flipped some strict flags on by default.
- **pyright / basedpyright** — faster (Rust-adjacent/Node), stricter in some edge cases; basedpyright adds `recommended`/`all` modes and checks unannotated code by default. A codebase passing *both* mypy and pyright strict is genuinely well-typed.
- **Does typing help LLM-generated code?** Strong types act as a machine-checkable contract that constrains agent output and catches interface drift — a real consistency win for a fleet. Adopt one checker fleet-wide (mypy for ecosystem/plugins, or basedpyright/pyright for speed+strictness), ratchet strictness up.

**"Architecture fitness functions" (2026 standard):** the combination of import-linter contracts + ruff complexity gates + deptry + a type checker, all run in pre-commit + CI, *is* the modern Python fitness-function stack. Keep Goodhart's law in mind — every metric that becomes a target degrades.

---

### Q3. Ratchet patterns — "never worse than today"

Your existing `silent_rule_ratchet` (a counted metric that must never exceed baseline) is textbook and matches emerging community practice. Concrete mechanisms:

- **Count baselines committed to the repo** (your approach). Real-world example: a project ratcheting ruff `C901`/`PLR0912`/`PLR0915` via a `.ruff-complexity-baseline` JSON, auto-lowering on decrease, failing on increase, and requiring a review-justified `--update-baseline` (tracked diff). This is exactly your model, and pairing it with an ADR-style "accepted debt" policy is the mature form.
- **mypy-baseline** — records existing type errors, reports only *new* ones, shows progress; baseline crafted to avoid merge conflicts. The canonical type-debt ratchet.
- **diff-cover / diff-quality** — run full analysis but report only on *changed lines*; drives coverage/lint quality on diffs. `vcs-diff-lint` (csdiff-based) does the same for ruff/mypy/pylint by comparing branch vs. main.
- **diff-scoped linting** — run ruff/pylint on changed files only in pre-commit; full run weekly in CI (the enterprise pattern for taming thousands of legacy findings).
- **betterer** (JS-origin) / home-grown counters (your model) generalize this to any metric.

**Failure modes (present honestly):**
1. **Goodhart's law** — the metric becomes a target and stops measuring quality (agents game line counts by splitting files arbitrarily).
2. **Permanent freeze on legitimate refactors** — a strict ratchet punishes a refactor that *temporarily* raises a count. Mitigation: allow a reviewed `--update-baseline` escape hatch (tracked in git, requires justification), and ratchet on *trend* (wily) not just instantaneous count.
3. **Baseline rot** — large inherited baselines normalize debt. Mitigation: pair with a scheduled "amnesty burn-down" and ownership mapping.
4. **False sense of safety** — ratchets stop *regression*, not *existing* debt; they say nothing about whether today's baseline is acceptable.

---

### Q4. Style doctrine for LLM agents specifically

**The central 2026 finding matches your doctrine exactly:** a rule that lives only in prose (CLAUDE.md/AGENTS.md) is a *request* with ~80% compliance that degrades under context pressure on long sessions; a **hook** is a *guarantee* with ~100% compliance because it runs at the system level outside the model's reasoning. As practitioner David (@DavidAi311) put it after writing 200 lines of ignored rules, "CLAUDE.md is a wish list, not a contract." The hook fires "on every write: session 1, session 47, session 200 — the hook does not forget."

**Instruction files (necessary, not sufficient). Cost: S.**
- **AGENTS.md** is the cross-tool open standard (Linux Foundation stewardship; ~60,000+ repos; read natively by Codex, Cursor, Copilot, Gemini CLI, Aider, Windsurf, and others); **CLAUDE.md** is Claude Code's richer native format with `@imports` and subdirectory scoping. Best practice: put shared conventions in AGENTS.md, keep a thin CLAUDE.md that imports it (`@AGENTS.md`) plus Claude-specific hooks. 2026 authoring rules: keep it short (a low line cap so it fits in a small % of context), **every rule must be falsifiable** (delete soft "consider…" directives — they're followed inconsistently), and **pair every rule with its enforcement layer** (hook/CI/linter) or tag it advisory-only. Subdirectory-scoped files give per-repo overrides in a monorepo.
- The "Language & Style" section should hold only what the linter can't enforce (type policy, import conventions, naming the linter misses).

**Hooks (the guarantee). Cost: S–M.**
- **Claude Code PostToolUse hooks** run a formatter/linter after every `Edit|Write|MultiEdit`. Pattern: on file write, run `ruff --fix` (or your full quality gate) on the touched file; if it fails, inject errors back into the agent's context as `additionalContext` so it self-corrects on the next action. Multiple hooks (format AND lint) can run in parallel before the agent's response appears.
- **PreToolUse hooks** can block risky actions (e.g., writing to an invented path — enforcing "zero invented paths"). This is where your path-tracing check belongs; PreToolUse can block/modify, PostToolUse can only react.

**Subagents / slash-commands for diff review. Cost: M.** Custom review subagents that check a diff against a style rubric (e.g., a `code-reviewer` subagent with its own PostToolUse lint hook) are common and supported via skill/agent frontmatter. These add judgment where deterministic checks can't reach — but treat their output as advisory, since it's probabilistic.

**Prompt-level / "prompt distillation" enforcement (your goal c). Cost: M.** This is the frontier and your most distinctive lever: a **pre-dispatch checker that refuses or rewrites a task contract lacking style/scope constraints** — e.g., reject a prompt that doesn't name the target module, doesn't state the size/complexity budget, or doesn't reference a governance path. This is a mechanism (a gate on the contract), consistent with "MECHANISMS are guarantees." There is no published standard for this yet — it is a home-grown gate. Because it is home-rolled, document a measured divergence justification per your LIBRARY-FIRST rule (there is no established OSS "prompt linter" to prefer; treat any emerging one as unproven).

**Evidence on what actually changes agent output:** the strongest published signal is the reliability-gap point above (hooks ~100% vs prompts ~80%). Concrete anecdote widely repeated in 2026 guides: an agent kept generating class components in a functional-hooks codebase (ignoring the README and contributing guide) until a single explicit AGENTS.md line — "Always use functional components with hooks" — fixed it. So short, specific, falsifiable rules *do* change output, but only hooks guarantee it. Conversely, vague/long/LLM-generated instruction files are reported to make agents *worse*.

---

### Q5. Cross-repo universalization (no copy-paste drift)

Options, with trade-offs, for your one-hub / 5–6 satellite topology:

1. **Published internal config package (installed as a dependency). MECHANISM. Cost: M. RECOMMENDED CORE.** Ship a versioned `your-org-devkit` package containing the canonical ruff/mypy config (and semgrep rules), pinned per repo, upgraded centrally with migration notes. This is the documented enterprise pattern ("publish a versioned company rules package that ships the canonical config and plugins; pin per service, upgrade centrally, track rule changes with migration guidance"). Fits your hub model best: `.dev-knowledge` publishes it. Trade-off: ruff config is not fully composable via `extend` across packages for every setting, so some conventions still ride along in files.
2. **Template repo + copier or cruft. MECHANISM. Cost: M. RECOMMENDED for files that can't be packaged** (pre-commit config, CI workflows, AGENTS.md). copier/cruft record the template source+commit in the repo and let you `copier update` / `cruft update` to propagate changes to all repos in minutes ("I changed the template once and ran copier update in each project… The improvements propagated in minutes"). copier is generally the more actively developed and update-friendly of the two. Trade-off: updates can conflict and need per-repo merge; one `.cruft.json` limits multi-template use.
3. **Shared pre-commit config.** pre-commit has **no native mechanism to share a subset of config across repos** (acknowledged open upstream issue #3422) — so you either template it (option 2) or wrap it. `sync-with-uv` helps keep pre-commit hook versions in lockstep with your uv lockfile, killing version drift (directly relevant to your pinned-uv constraint).
4. **"Carrier" that ships canonical files + verifies checksums. MECHANISM. Cost: M–L.** A home-grown propagator that copies canonical files and fails if a repo's copy diverges from the hub checksum. This is essentially what your `.dev-knowledge` hub + audit.py already imply. It's the most controlling option and matches your governance model, but it's hand-rolled — justify per LIBRARY-FIRST vs. copier (copier already does propagation; the checksum-verify piece is the only genuinely custom part).

**Recommendation:** config-package for tool settings + copier for the un-packageable files + a small checksum audit in your existing audit.py. Avoid pure copy-paste and avoid global git `core.hooksPath` tricks (they don't version well across a fleet).

---

### Q6. Aggregation and measurement across repos

**Lightweight, dependency-cheap (RECOMMENDED for ~6 repos). Cost: M.** Have each repo emit machine-readable JSON in CI — `ruff check --output-format=json`, `radon cc/mi -j`, `wily` history, `deptry --json`, jscpd JSON — and collect them into one store (even a git repo of JSON, a SQLite DB, or a small dashboard). This is self-hosted, no SaaS, no per-seat cost, and gives you the fleet-wide trend comparison you want for AGGREGATION. It aligns with your existing audit.py/validator philosophy. The cost is that *you* build the aggregation + dedup + normalization layer (there is no unified dashboard for free — as one survey of SonarQube alternatives notes, "results live in CI logs and per-repo SARIF views… answering 'what are our top ten risks across all services?' requires building your own aggregation").

**SonarQube Community Build. Cost: M–L.** Free, self-hosted, 20+ languages, quality gates, SQALE technical-debt model (remediation effort in time → a trackable "technical debt ratio"), duplication + complexity built in. **Limits:** Community is **single-branch** (no PR decoration / multi-branch without paid editions), JVM-heavy to run, and portfolio/multi-project aggregation dashboards are an Enterprise feature. For 6 repos it's more infrastructure than the JSON-collection approach.

**SaaS options (flag, don't necessarily adopt):** SonarCloud, CodeClimate, Codacy (~$15/user/month, unlimited scans) — faster to stand up, per-seat cost, data leaves your environment. **OpenSSF Scorecard** measures *security/supply-chain posture*, not code style — useful as a separate fleet check, not for style aggregation.

**Verdict:** for a 6-repo fleet that already has audit.py, the self-hosted JSON-collection approach is the right call; adopt SonarQube only if you want the SQALE debt model and a ready-made UI and can run the server.

---

### Q7. Deciding on a big refactor

**Standard, evidence-based procedure — measure first, in this order:**
1. **Churn-vs-complexity hotspot analysis** (the "Your Code as a Crime Scene" / CodeScene method). Overlay how often each file changes (git churn) with its complexity. Adam Tornhill's finding (CodeScene docs): "There's a strong correlation between Hotspots, maintenance costs and software defects," and "change alone is the single most important metric when it comes to quality issues in code" — his data shows 1–2% of a codebase can account for up to ~70% of development work. Complex code that rarely changes is cheap to leave alone; complex code that changes constantly is where refactoring pays. **This is the single most important measurement.**
2. **Complexity distribution** (radon cc, xenon) — where are the F-grade functions?
3. **File-length distribution** — find the over-long modules (your specific concern with LLM output).
4. **Test coverage on hotspots** — refactoring uncovered hotspots is high-risk; add characterization tests first.
5. **Duplication rate** (jscpd) — high duplication favors consolidation.
6. **Dependency cycles / boundary violations** (import-linter, pydeps) — cycles are strong refactor signals.

**Thresholds commonly used (as heuristics, not laws):** ruff/flake8 `max-complexity` guidance around 10 (McCabe), `PLR0915` at 50 statements, jscpd thresholds of ~5–10% duplication, radon A–F grades with C or worse flagged. Treat these as *triggers for review*, not automatic refactors.

**Contested evidence — present both sides:**
- **Cyclomatic complexity's validity as a defect predictor is genuinely disputed.** Martin Shepperd's classic critique ("A critique of cyclomatic complexity as a software metric," *Software Engineering Journal* 3(2), March 1988) argues CC is "based upon poor theoretical foundations and an inadequate model of software development," and that "a considerable number of studies… indicate that LOC actually outperforms cyclomatic complexity" (Shepperd & Ince: static measures are "no more than a proxy for, and in many cases outperformed by, lines of code"). Landman/Serebrenik/Vinju show CC and SLOC are strongly linearly correlated (CC is partly redundant with size). Other controlled studies find CC, Halstead volume, and LOC all correlate with defect rate. **Net:** use complexity as a *smell/triage signal*, not as proof of defect risk; combine it with churn (which is better-supported) rather than trusting it alone.
- **Maintainability Index** is explicitly flagged by radon's own docs and by van Deursen as unreliable — use for coarse trend only.

**Big refactor vs. incremental — what the literature and practice say:**
- **Big-bang rewrites usually fail or overrun** and deliver no value until the end while chasing a moving target (AWS Prescriptive Guidance, microservices.io, and multiple 2025–2026 practitioner accounts converge on this).
- **Strangler fig pattern** (Fowler) — incrementally build the new around the old behind a facade/routing layer, migrate piece by piece, decommission the old. Lower risk, continuous delivery, validates decisions in production early. Best for large modules/services.
- **Opportunistic / preparatory refactoring + boy-scout rule** — refactor the code you're already touching, especially "make the change easy, then make the easy change." Best for the everyday case and ideal for an LLM fleet: bake "leave hotspots slightly better" into the agent contract.
- **Defect-rate caveat:** refactoring itself can introduce defects (the whole rationale behind diff-scoped tooling like vcs-diff-lint is that mass rewrites "risk introducing even more bugs"), which is why hotspot-scoped, test-backed, incremental change beats a fleet-wide rewrite.

**Decision rule for your fleet:** Do **not** launch a big refactor of code written before these patterns existed *solely because it predates them.* Run the hotspot analysis; refactor only where high churn ∩ high complexity ∩ (low coverage → add tests first). Everywhere else, apply ratchets + opportunistic refactoring so the code improves as agents touch it. Reserve strangler-fig for a genuinely load-bearing, high-churn, high-complexity module.

---

## MECHANISM vs TASTE — the dividing line

| Concern | MECHANISM (hook/gate/CI) | TASTE (short written doctrine) |
|---|---|---|
| Naming | ruff `N` (pep8-naming), hyphen-only folder check in audit.py | "names should reveal intent" |
| Module/function size | ruff `PLR0915`/`C901`/`PLR0912`, complexipy | "prefer deep modules" (Ousterhout) |
| OO vs functional | *(cannot gate)* structural caps only | "functional core, imperative shell" |
| LIBRARY-FIRST | deptry, semgrep "don't hand-roll X" rules | measured-divergence justification prose |
| Architecture layering | import-linter contracts | "zero invented paths" narrative |
| Duplication | jscpd threshold, pylint R0801 | DRY guidance |
| Types | mypy/pyright strict + baseline ratchet | "type all public interfaces" |
| Debt direction | count ratchets, mypy-baseline, diff-cover | ADR "accepted debt" policy |
| Agent compliance | PostToolUse lint hook, PreToolUse path guard, prompt pre-dispatch checker | AGENTS.md/CLAUDE.md conventions |

---

## Recommendations (staged, in adoption order)

**Stage 0 — Baseline the fleet (1 week). Cost: S.**
Run radon/xenon, ruff (all rules, report-only), jscpd, deptry, and a git-churn hotspot script across all 6 repos; dump JSON to one store. This gives you the refactor decision inputs *and* the initial ratchet baselines. **Benchmark that changes the plan:** if any repo has hotspots where high churn meets F-grade complexity and <50% coverage, that repo (only) is a refactor candidate.

**Stage 1 — Publish the canonical config package (1–2 weeks). Cost: M. Retires: per-repo ad-hoc ruff configs.**
From `.dev-knowledge`, publish `devkit` with canonical ruff + type-checker config + semgrep LIBRARY-FIRST rules. Pin it (via uv) in every repo. Add copier for the un-packageable files (pre-commit, CI, AGENTS.md); add `sync-with-uv` to kill hook-version drift.

**Stage 2 — Wire the gates into pre-commit + CI (1 week). Cost: S–M. Replaces: manual review of style.**
pre-commit stages (you already have commit-msg/pre-commit/pre-push): ruff (fix + check) and hyphen-naming/path checks at commit stage; type checker, deptry, jscpd threshold, import-linter contracts, and complexity ratchet at pre-push. Diff-scoped on commit; full run in GitHub Actions with pytest-xdist.

**Stage 3 — Turn on ratchets (1 week). Cost: S. Extends your silent_rule_ratchet.**
Add count baselines for `C901`/`PLR0912`/`PLR0915`, mypy-baseline for type debt, and diff-cover for coverage. Auto-lower on improvement; require a reviewed, git-tracked `--update-baseline` to raise. Add a scheduled burn-down.

**Stage 4 — Agent enforcement layer (1–2 weeks). Cost: M. This is your differentiator.**
Thin AGENTS.md (imported by CLAUDE.md) with short, falsifiable rules; PostToolUse hook running the quality gate on every edit and feeding errors back; PreToolUse guard enforcing "zero invented paths"; and the **prompt pre-dispatch checker** that refuses/rewrites contracts lacking module target, size/complexity budget, and a governance path reference.

**Stage 5 — Fleet aggregation dashboard (ongoing). Cost: M.**
Collect the Stage-0 JSON continuously; trend complexity, duplication, type coverage, and lint debt per repo. Only consider SonarQube Community if you want SQALE/UI and can run the server.

**Thresholds that change the recommendation:** if the fleet grows past ~15–20 repos, revisit SonarQube/SonarCloud or a portfolio tool; if agent non-compliance persists despite hooks, tighten PreToolUse blocking rather than adding prose; if a ratchet blocks legitimate refactors more than occasionally, switch that metric from instantaneous-count to wily trend.

---

## The Minimal Starter Set (smallest enforceable universal doctrine)

In adoption order, the *smallest* set that gives a Python fleet a universal, enforceable style doctrine:

1. **ruff** (config shipped in the `devkit` package) — retires flake8, isort, most of pylint, pyupgrade, pydocstyle. One tool, one config, fleet-wide.
2. **One type checker** (mypy *or* basedpyright) with a **baseline** — the machine-checkable contract that most constrains agent output.
3. **Count ratchets** on ruff complexity + type debt (your existing silent_rule_ratchet, extended) — "never worse than today."
4. **import-linter contracts** — the one architecture gate; enforces "functional core, imperative shell" and "zero invented paths."
5. **PostToolUse lint hook + PreToolUse path guard** — converts the doctrine from request to guarantee for agents.
6. **copier + config package** — makes items 1–4 identical across all repos without copy-paste.

Everything else (complexipy, wily, jscpd, semgrep, deptry, SonarQube) is a valuable *add-on* layered on once the core holds. semgrep and deptry are the highest-value additions for your specific LIBRARY-FIRST goal.

---

## Caveats & conflicts to flag

- **LIBRARY-FIRST tension in the toolchain itself:** the **prompt pre-dispatch checker** and the **checksum "carrier"** are the two genuinely hand-rolled pieces with no established OSS equivalent — document measured-divergence justifications for both. copier/cruft already cover propagation, so don't hand-roll that. `returns`/`toolz` for FP are libraries (LIBRARY-FIRST compliant) but push non-idiomatic style — adopt only with justification.
- **Metric validity is contested:** cyclomatic complexity may be no better than LOC as a defect predictor (Shepperd 1988; Landman et al.), and Maintainability Index is flagged unreliable by its own tooling (radon docs; van Deursen). Use them as triage smells combined with churn, never as standalone proof.
- **Goodhart's law is the master risk:** every gate you add can be gamed by an LLM optimizing to the metric (splitting files to dodge length caps, trivial wrappers to dodge complexity). Keep a human in the loop on the ratchet-raise escape hatch.
- **tach maintenance uncertainty:** the original `gauge-sh/tach` lapsed in 2025; a community continuation (`tach-org/tach`) ships releases. Prefer import-linter (actively maintained, v2.13 Jul 2026) for stability unless you need public-interface enforcement.
- **Clean Code's rules are contested** — do not encode its short-function/minimal-comment rules as gates; they conflict with Ousterhout's deep-modules doctrine you're adopting.
- **Claude Code vs AGENTS.md:** native support has shifted across 2025–2026 (Claude Code historically preferred CLAUDE.md; AGENTS.md support arrived later). Maintain AGENTS.md as the source of truth and a thin CLAUDE.md importer to avoid divergence.
- **Aggregation build cost:** the cheap self-hosted route means you own the normalization/dedup layer; budget for it.
- **Astral/OpenAI:** ruff/uv/ty are made by Astral, which OpenAI announced it would acquire (reported Feb 2026). No change to open-source status today, but a governance signal worth monitoring for a fleet that pins these tools.