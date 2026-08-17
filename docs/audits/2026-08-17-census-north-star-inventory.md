# 2026-08-17 — census: north-star inventory

**Lane c, batch 7a.** Contract of record: `docs/audits/2026-08-17-technical-batch-7a-lane-c-contract.md`.
Branch `worktree-lane-c-505-north-star-inventory`. BIRTHS NOTHING — no reserved id block; any
gap found below that needs a row is recorded as **DECIDED-UNFILED** and named, not filed.

**Purpose, in the operator's own words:** *"The operator wants to SEE the whole plan, derived
from the tree, not from anyone's memory."* Every row below is locator-backed; a claim with no
locator does not appear here.

**Method:** seven parallel research passes swept the full tree — every ADR (87 files, incl.
`docs/decisions/archive/`), every intake (36 files, incl. `docs/intake/archive/`), `protocols/`
+ `VISION.md` + `ARCHITECTURE.md` (14 files), `BACKLOG.md` (469 lines) + `tasks/` (268 files),
a grep-driven wiring audit of `pyproject.toml` / `.pre-commit-config.yaml` / `scripts/` /
`.github/` excluding `tests/`, a grep sweep of `docs/audits/*.md` (567 files) for sole-carrier
commitments and measured numbers, and a consumer-repo survey (`ai-council`, `corp-monorepo`,
`corp-ops`, `corp-sca-time-automation`, `win-tooling`) for the universalization section. Currency
note per contract: lane **b** is concurrently archiving terminal ADRs/intakes on its own branch;
this is a snapshot of `main` at this lane's branch point and is correct as such.

**Honest scope limit, stated so it is not mistaken for completeness:** the ADR/intake/BACKLOG
sweeps returned several hundred distinct rows. The master table below carries the full 39-item
contract floor plus every additional item that carries either a live wiring verdict, an open
BACKLOG row, or a clean adopt/reject disposition. Items that are DRAFT-status intake prose with
no ratifying ADR and no BACKLOG row are folded into §A/§D rather than given their own master-table
line, to keep the table checkable rather than a second copy of the intake corpus. Nothing found
was dropped silently — see §A for the unfiled residue.

---

## Step 1 — Master table

Columns: item · what it is for · source locator · committed-where · STATUS · evidence.

### Contract floor (39 named items)

| item | what it is for | source locator | committed-where | STATUS | evidence |
|---|---|---|---|---|---|
| pytest-xdist | parallel test execution (`-n auto`) | `pyproject.toml:30`; ADR-110 amend 2026-08-06; STANDING_RULINGS §E1 | `pyproject.toml` dev group + `[tool.pytest.ini_options] addopts` | **LIVE-WIRED** | `pyproject.toml:30` declares `pytest-xdist>=3.8`; `addopts = "-n auto"` fires on every invocation; 5.2× measured speedup (1785.61s→358.77s/330.15s, STANDING_RULINGS §E1) |
| filelock | filesystem lock candidate | `scripts/single_flight.py:7` | none | **EVALUATED-REJECTED** | "every filesystem-lock candidate (filelock, portalocker, ...) is single-host by construction" — rejected in favor of git-ref CAS, `docs/audits/2026-08-14-technical-night2-research.md:168-179` |
| portalocker | filesystem lock candidate | `scripts/single_flight.py:7` | none | **EVALUATED-REJECTED** | same site as filelock |
| datasette | telemetry read-surface | `docs/intake/2026-08-08-func-multi-model-execution-and-distillation.md` | none | **MENTIONED-ONLY** | "rich/plotext + Datasette read surfaces" — proposed sibling-memo design, zero code, zero backlog row |
| plotly | data-viz library | none found outside `docs/` | none | **MENTIONED-ONLY** | 0 hits outside docs/tests-fixtures; not a live proposal |
| altair | data-viz library | none found outside `docs/` | none | **MENTIONED-ONLY** | 0 hits outside docs/ |
| rich | CLI console output | `pyproject.toml:35`; `deploy/tool.py:48-50` | `pyproject.toml` dev group | **LIVE-WIRED** | `from rich.console import Console`, `from rich.table import Table` used in `deploy/tool.py` |
| plotext | terminal plotting | `docs/intake/2026-08-08-...distillation.md` | none | **MENTIONED-ONLY** | same telemetry-design memo as datasette; 0 code hits |
| structlog | structured logging backend | `scripts/telemetry_emit.py:313,329-332` | none in `pyproject.toml`/`uv.lock` | **BUILT-UNWIRED** | imported inside a try/except optional-import fallback; file's own header states "Library only; no call sites" (`scripts/telemetry_emit.py:2`) |
| SQLite WAL | telemetry event store | `scripts/telemetry_emit.py:140,287-290` | none | **BUILT-UNWIRED** | `WAL_PRAGMAS` + `sqlite3.connect` implemented, but file states "it wires nothing... A grep for telemetry_emit outside this file and its test is expected to return nothing today" |
| ruff | lint gate | `pyproject.toml:31`; `.pre-commit-config.yaml:232-242` | dev group + pre-commit hook | **LIVE-WIRED** | `ruff==0.15.5` exact-pinned to match the hook rev; fires on every commit |
| radon | complexity measurement | `docs/intake/2026-08-09-func-code-style-doctrine.md`, `2026-08-16-code-architecture-enforcement.md` (both DRAFT/unratified for the enforcement leg) | none | **MENTIONED-ONLY** | 0 hits outside docs/JOURNAL.md/tasks; "not installed" per `docs/audits/2026-08-14-qa-night2-quality.md:97-99` |
| xenon | hard-ceiling complexity gate | same intake docs, unratified | none | **MENTIONED-ONLY** | 0 code hits; EVALUATED-REJECTED once already on this repo's own numbers per `docs/audits/2026-08-09-technical-consolidation-report.md:322-341`, then re-proposed 2026-08-16 (DRAFT, not yet ruled) |
| import-linter | architecture/import-boundary gate | `docs/intake/2026-08-09-func-code-style-doctrine.md` (ACCEPTED), reiterated `2026-08-16-code-architecture-enforcement.md` ("named... as the natural [#533] follow-on") | none | **DECIDED-UNFILED** | ACCEPTED intake names it as preferred over `tach` (v2.13, actively maintained); no ADR, no BACKLOG row — see §A |
| mutmut | mutation testing (CI-only, Windows fork() constraint) | `pyproject.toml:52-91` `[tool.mutmut]`; `.github/workflows/report-only-wall.yml:256-301` | BACKLOG `[#502]` | **ROW-OPEN** (LIVE-WIRED in CI) | `[#502]` open P3, blocked on `[#501]`; config landed, ADOPT/REJECT verdict not yet run — "mutmut needs fork()... WSL is out by operator constraint" |
| pre-commit | git hook framework | `pyproject.toml:32`; `.pre-commit-config.yaml` (25 hooks, 3 stages) | dev group | **LIVE-WIRED** | primary gate mechanism, every entry prefixed `uv run --locked` |
| uv | environment isolation | `pyproject.toml:17-25`, `required-version=="0.11.19"` (ADR-106) | pinned toolchain | **LIVE-WIRED** | every pre-commit hook entry and CI step runs through `uv run --locked` |
| Click | CLI framework | `pyproject.toml:34`; `scripts/audit.py:47,3903` | dev group | **LIVE-WIRED** | `audit.py`'s CLI is Click-based (`@click.group()`, `@click.option`) |
| pandas | descriptive analytics (L5a) | `pyproject.toml:48-50` analytics group; `scripts/fleet_analytics.py:416,511,670` | ADR-109 | **LIVE-WIRED** | HUB-ONLY, lazy-imported; no consumer dependency-baseline row by design |
| lru_cache | memoization | `scripts/single_flight.py` grep: 0 hits per wiring sweep; BACKLOG `[#533]` claims a landed leg ("`lru_cache`, ~42.7s → ~17.8s per commit) with its test") | `[#533]` | **CONFLICTING EVIDENCE — flagged, not resolved** | wiring-sweep grep found zero `lru_cache` hits in `scripts/`; the BACKLOG row's own text asserts a landed leg with a test. This lane did not re-grep to adjudicate the conflict — reported honestly rather than guessed; see §D |
| concurrent.futures | parallel check execution | `docs/intake/2026-08-09-func-code-style-doctrine.md` cites stdlib `ThreadPoolExecutor` | `[#533]` LEG 2 (batch 7, in-flight) | **ROW-OPEN** | "stdlib `concurrent.futures.ThreadPoolExecutor`... `ProcessPoolExecutor` only if a measurement shows CPU-bound"; wiring sweep found 0 hits in `scripts/` as of this snapshot — leg is open, not yet landed |
| git-ref CAS | distributed compare-and-swap lock (git push --force-with-lease) | `scripts/single_flight.py` (full implementation + CLI) | `[#530]`, `[#531]` | **ROW-OPEN** (BUILT-UNWIRED as of this snapshot) | file states "This is an ADVISORY library + CLI. It is wired into no hook and gates nothing by existing"; `[#530]` open P2 (T2/T4 concurrency properties not yet demonstrated against real `origin`), `[#531]` open P2 (wire via `reference-transaction` git hook) |
| GitHub Actions | server-side report-only CI wall | `.github/workflows/report-only-wall.yml` (16,640 bytes); ADR-101 amend 2026-08-06 | ratified | **LIVE-WIRED** (report-only, non-blocking by design) | active workflow; mutmut pilot runs inside it; "report-only permanently, not pending promotion" |
| Codespaces | dev-container hosting | `docs/intake/2026-08-09-tech-compute-placement-and-remote-execution.md` | none | **MENTIONED-ONLY** | 0 hits in `scripts/`/`.github/`; intake states "No host is provisioned by this intake" |
| VPS/Hetzner | remote compute host | same intake | none | **MENTIONED-ONLY** | "Hetzner-vs-Hostinger is priced in the memo and deliberately not decided here" |
| Colab | remote compute host | same intake family (nb4-g-scaleout-substrate audits) | none | **MENTIONED-ONLY** | 0 hits in `scripts/` |
| Groq | inference provider | same intake family | none | **MENTIONED-ONLY** | 0 hits in `scripts/`; only 3 `docs/audits/` files (scale-out research) |
| Gemini CLI | coding-assistant CLI | `protocols/ENVIRONMENT.md` §Rejected | none | **EVALUATED-REJECTED** | "No Codex CLI, no Gemini CLI" — distinct from the Gemini *review-lane* item below |
| Gemini (scanning/review lane) | propose-only semantic scanning lane | `docs/intake/2026-07-25-tech-consolidation-decision.md` (ACCEPTED, ADOPTED) | `[#491]` | **ROW-OPEN** | `[#491]` open P3: "ruling + acceptance contract for subscribed Gemini CLI as read-only scanning lane (Antigravity excluded)" |
| Codex | pre-merge diff reviewer | `protocols/PLAYBOOK.md` §16/17; ADR-54; `scripts/audit.py:3142` (`_REVIEW_TITLE_RE`) | ADR-54, `/codex-review` command | **LIVE-WIRED** | repo scripts consume Codex-review artifacts (`^# Codex Review` regex) to identify review-coverage in `docs/audits/`; the reviewer role itself is a user-level (`~/.claude/commands/`) skill, not repo code |
| Kimi | fallback model (Moonshot API) | `docs/intake/2026-08-05-func-simplification-distribution-wave.md` (ACCEPTED) | none | **EVALUATED** | "validated fallback, never a daily driver, and carries documented breakage"; earlier `2026-05-17-kimi-k2-scoping.md` marked stale/delete-candidate `docs/audits/2026-07-22-technical-night-batch-deep-audit.md:189` |
| Copilot | AI coding assistant / review-lane test channel | `docs/intake/2026-08-05-...-wave.md`, `2026-08-06-tech-adoption-consolidation-intake.md` | none | **EVALUATED-REJECTED** (as standing review lane) | "the row stays filed with a trigger, not a rejection"; "NOT a standing review lane (quota); use as the free test channel" for Grok |
| prompt distillation | context/token-compression technique | `docs/intake/2026-08-01-func-distillation-and-library-first.md`; `2026-08-08-func-multi-model-execution-and-distillation.md` | none | **MENTIONED-ONLY / partially EVALUATED-REJECTED** | LLMLingua/LongLLMLingua cited as evidence (MENTIONED-ONLY); `repomix` measured at "0% compression on markdown on this corpus... rejected on evidence" |
| telemetry | check/hook/blocker event emission | `scripts/telemetry_emit.py` (full Stage-1 library) | `[#529]` | **ROW-OPEN** (BUILT-UNWIRED) | `[#529]` open P1, "STAYS OPEN on 4 legs: (1) wire the call sites (phase 3)..."; module explicitly documents zero non-test callers |
| dashboards | human-facing fleet-observability surface | `scripts/audit_checks/_common.py:37-42` (format exists, no dashboard) | `[#322]`, `[#171]`, `[#169]` | **ROW-OPEN** (NOT-PRESENT as code) | `[#171]` open P3 "a dashboard that does not exist... target now DEFERRED (parked)"; `[#322]` open P2, DEFER dated review 2026-09-09; `[#169]` open P3 DEFER on `[#171]` |
| codemap | auto-generated code-structure map | `scripts/codemap/` package (cli.py, generator.py, check.py, ast_walker.py) | ADR-51 (amend 2026-07-05) | **LIVE-WIRED** | called from 26 files incl. `scripts/audit.py`; `codemap-freshness` pre-commit hook runs on every commit touching `scripts/**.py` |
| fleet parity | cross-repo drift/parity checker | `scripts/fleet_parity.py` | ADR-102, ADR-103 | **LIVE-WIRED** (blocking `ALL_CHECKS` member) | imported by `scripts/audit.py`, `scripts/audit_checks/registry.py`; run as part of `audit.py health` / `audit-health` pre-commit hook |
| satellite runbooks | per-consumer operational runbook | `templates/consumer-onboarding-runbook.md`; `tasks/293-consumer-runbook-fan-out.md`; `docs/audits/2026-08-15-technical-293-consumer-runbook-fan-out-lane-contract.md` | `[#293]`-family (tracked in `tasks/`) | **ROW-OPEN** (NOT-PRESENT as a deployed artifact) | consumer-repo survey confirms: **no repo, hub or consumer, has a genuine `RUNBOOK.md`** — only the hub's generator template exists |
| archival lifecycle | append-only/immutable file governance + tombstone convention | CLAUDE.md §4/§5; ADR-29, ADR-39, ADR-83 | `[#244]` (P2–P4 shipped, P5/P6 unowned), `[#420]` | **ROW-OPEN** | `[#420]` open P3: "the top-level `docs/archive/` charter question (keep vs dissolve)" still open |
| closing campaign | whole-BACKLOG-set grooming arc | `docs/audits/2026-08-16-census-nb4-closing-campaign.md` | `[#506]` | **ROW-OPEN** | `[#506]` open P2: "189 of 200 open rows uncovered since the last whole-set dossier" |
| universalization / config packaging | cross-repo methodology distribution | `deploy/tool.py` + `deploy/manifest-v1.4.0.yaml` (the actual live mechanism) | ADR-91, ADR-92, ADR-96, ADR-109; `[#371]`,`[#325]`,`[#294]`,`[#276]`,`[#345]`,`[#244]` | **LIVE-WIRED** (the deploy mechanism itself) **+ ROW-OPEN** (multiple carrier gaps) | see §B for the full breakdown — the literal term has no code anchor, but the underlying carrier-based deploy system is real and running |

### Beyond the floor — additional items with a clean disposition and/or live code

| item | what it is for | source locator | committed-where | STATUS | evidence |
|---|---|---|---|---|---|
| pydantic | ecosystem desired-state schema (ADR-109 v1) | `pyproject.toml:36`; `ecosystem/schema/desired_state.py` | ADR-109 | **LIVE-WIRED** | `schema_version: "1.0.0"`, typed contract shipped |
| packaging | PEP 440 version comparison | `pyproject.toml:37`; `scripts/fleet_parity.py` | intake #23 | **LIVE-WIRED** | declared explicitly so fleet_parity doesn't ride a transitive edge |
| markdown-it-py | CommonMark fence-toggle / frontmatter parsing | `pyproject.toml:38`; `scripts/normalize_headers.py` | STANDING_RULINGS §N-1 | **LIVE-WIRED** | replaced a bespoke toggle "wrong four distinct ways over a 1578-file corpus" |
| yaml.safe_load | frontmatter parsing | STANDING_RULINGS §N-2 | ADOPTED | **LIVE-WIRED** (per protocols sweep) | "moves from a hand-rolled regex/prefix reader to `yaml.safe_load`" |
| Pyright (headless language server) | code↔code reverse-dependency oracle | `scripts/reverse_dep_oracle.py` | ADR-89 | **LIVE-WIRED** | `references()` query; vendored via `npm install`, `node_modules/` gitignored |
| networkx | fleet dependency-graph modeling | `docs/intake/2026-07-21-func-fleet-north-star.md` (ACCEPTED); `2026-08-01-func-distillation-and-library-first.md` "P3 networkx STANDS for [#383] v1" | ADR-109 (deferred for v1), `[#383]` | **ROW-OPEN** (NOT-PRESENT as code) | `[#383]` execution-waves ticket; ADR-109 explicitly defers networkx for schema v1 |
| PyDriller | git/session-history mining (L5a) | `docs/intake/2026-07-21-func-fleet-north-star.md` | `[#384]` | **ROW-OPEN → closed with carve-out** | `docs/intake/2026-07-28-north-star-delta-review.md`: "L5a analytics lane — PyDriller mining | DONE, with a named carve-out" — largely delivered |
| scikit-learn | L5b predictive scoring (gated) | same intake | `[#384]`-family, gated on L5a signal volume | **COMMITS-NO-ROW** (gated, not started) | "the doc itself gates it on 'L5a shows signal volume', not enough to trip that gate" |
| copier | fleet-wide living-template propagation | `docs/intake/2026-08-05-func-simplification-distribution-wave.md` (ACCEPTED, ADOPTED "W-1... as a LIVING TEMPLATE") | none confirmed | **DECIDED-UNFILED** | no ADR ratifies it, no dedicated BACKLOG row found; see §A |
| Backlog.md (MrLesk OSS tool) | per-ticket-file backlog engine | `docs/intake/2026-07-25-tech-consolidation-decision.md`; ADR-107 | ADR-107 | **EVALUATED-REJECTED** | "Pattern donor, not adopted as the tool"; ADR-107 also rejected `scrummd` ("bus factor 1") |
| gen_task_tree.py (build-thin engine) | fleet-owned BACKLOG↔`tasks/` engine | `scripts/gen_task_tree.py` | ADR-107 | **LIVE-WIRED** | chosen over Backlog.md/pyadr; "git is the state store" |
| AGENTS.md (fleet-wide rename target) | cross-provider instruction file | `docs/intake/2026-08-05-...-wave.md` ADOPTED "W-9a"; **directly reversed** by `docs/intake/2026-08-12-func-repo-self-description-consolidation.md`: "AGENTS.md is retired here (ADR-53)" | ADR-53 (retired), intake W-9a (superseded) | **EVALUATED-REJECTED** (net, per ADR-53) | flagged as a doctrine reversal, not a silent gap — the later intake explicitly cites ADR-53 to close the earlier ACCEPTED-but-unbuilt W-9a proposal |
| dev-knowledge-kernel package | versioned installable methodology kernel | `docs/intake/2026-08-05-...-wave.md` (ACCEPTED, ADOPTED) | none confirmed | **DECIDED-UNFILED** | "the kernel ships as an installable package from the hub" — no package exists in the tree; see §A |
| pytest-testmon | test-impact analysis for the dev loop | same intake, operator-endorsed; `2026-08-06-tech-adoption-consolidation-intake.md`: "SCHEDULED(batch-2 ledger per rider R-ii; targets 410s/run)" | none confirmed landed | **DECIDED-UNFILED** | see §A |
| GitHub reusable workflow | single CI definition for all consumers | `docs/intake/2026-08-05-...-wave.md` ADOPTED "W-4" | none confirmed | **DECIDED-UNFILED** | only the hub's own `report-only-wall.yml` exists; no reusable-workflow artifact found in consumer survey |
| README.md as universal front door | VISION.md rename target | same intake, ADOPTED | none | **DECIDED-UNFILED, and contradicted by current tree** | `VISION.md` still exists at hub root as of this snapshot — the rename was never executed |
| check-jsonschema / pydantic (W-6 schema-as-code) | governed YAML + `tasks/` frontmatter validation | `docs/intake/2026-08-05-...-wave.md` ACCEPTED; `2026-08-06-...-intake.md`: "DEFERRED(floats behind W-5)" | none | **DECIDED-UNFILED** | see §A |
| deptry | unused/missing/misplaced dependency scanner | `docs/intake/2026-08-09-func-code-style-doctrine.md` (ACCEPTED) | none | **DECIDED-UNFILED** | "v0.25.1, Mar 2026; uv/PEP-621 native" |
| semgrep | library-first-rule enforcement via custom patterns | same intake (ACCEPTED) | none | **DECIDED-UNFILED** | "the mechanical form of the library-first rule" |
| mypy / basedpyright | fleet-wide type checker + baseline | same intake (ACCEPTED) | none | **DECIDED-UNFILED** | "One type checker fleet-wide... with a baseline" |
| lychee | dead-link checker for markdown | `docs/intake/2026-08-05-tech-currency-wave-1.md`; `2026-08-06-...-intake.md`: "EVAL-RUN(ADOPT-candidate, --include-fragments)" | none | **DECIDED-UNFILED** | verdict reached (adopt-candidate), never built or filed |
| gh CLI findings-as-Issues | close the audit-loop's manual pump | `docs/intake/2026-08-05-tech-currency-wave-1.md` ADOPTED "P3"; `2026-08-06-...-intake.md`: "UNPLACED(reshaped: batch-per-run)" | none | **DECIDED-UNFILED** | |
| gh CLI (as installed tool) | de-facto load-bearing CLI | `docs/intake/2026-08-08-func-skills-tier-adoption-and-hub-finish-line.md` | none | **DECIDED-UNFILED** | "DE-FACTO ADOPTED — formalize (one ledger line)" — a one-line ledger entry, still unfiled |
| mise | per-repo toolchain pinning (uv-pin class fix) | `docs/intake/2026-08-06-...-intake.md`: "CLASS CHANGE PROPOSED, NOT RULED"; `2026-08-09-func-verification-organ...md` ACCEPTED "a pin strategy that a fresh container can satisfy (mise or equivalent)" | none | **DECIDED-UNFILED** | |
| markdown_it (fence detection, 2 of 3 sites) | markdown parsing, half-landed | `docs/intake/2026-08-09-func-verification-organ-and-repeatable-execution.md` ACCEPTED | none | **DECIDED-UNFILED (partial build)** | "ruled ADOPT, landed at 1 of 3 sites" |
| skill-creator (anthropics/skills) | official skill-authoring tool | `docs/intake/2026-08-08-...-finish-line.md` ACCEPTED, Tier S try-now | none confirmed | **DECIDED-UNFILED** | "the tool with which Ch8/contract templates get rewritten AS portable skills" |
| ponytail | "best code is none" always-on skill ruleset | same intake, Tier S try-now | none confirmed | **DECIDED-UNFILED** | "installs across Claude/Codex/Copilot/Gemini" |
| Pylance workspace excludes / `openFilesOnly` | editor-indexing hygiene | `docs/intake/2026-08-09-func-verification-organ...md` ACCEPTED | ADOPTED | **ADOPTED** (settings-level, not code) | analysis excludes for worktrees/venvs/mutants/caches |
| Vibe Kanban | in-IDE task board tool | ADR-110 | none | **EVALUATED-REJECTED** | 30-min eval, "Verdict wanted BEFORE the wide batch" |
| sol/terra/luna routing table | Codex model-lane routing | `docs/intake/2026-08-06-tech-adoption-consolidation-intake.md` | ADOPTED-live | **ADOPTED** | PLAYBOOK §16: "terra / sol / luna = gpt-5.6-terra / -sol / -luna" |
| standing-rulings register | ruling/precedent register mechanism | same intake | ADOPTED-live | **ADOPTED** | `protocols/STANDING_RULINGS.md` |
| tier1-lifecycle plugin | `/ship`, `/review-closures`, `propose_closures` | ADR-70, ADR-72, ADR-74 | ADOPTED | **LIVE-WIRED** | Stop hook active; marketplace-installed |
| CLAUDE-FLOOR.md + `.sha256` guard | generated child methodology floor | ADR-78, ADR-93 | ADOPTED | **LIVE-WIRED** (2 of 5 consumers fully; see §B) | `floor-hash-verify` pre-commit hook |
| block_ff_push.py / block_unanchored_push.py | pre-push spine-anchor + FF-push refusal | ADR-85 amend 2026-08-03 | ADOPTED | **LIVE-WIRED** | fail-closed since the 2026-08-03 amendment |
| single_flight.py (git-ref CAS impl) | distributed dispatch lock CLI | ADR (none dedicated — implements the git-ref-CAS pattern researched 2026-08-14) | `[#530]`, `[#531]` | **ROW-OPEN** (BUILT-UNWIRED) | see floor-table row above; duplicated here for cross-reference |

---

## Step 2 — §A DECIDED-UNFILED, ranked by age of the committing source

Ranked oldest-committing-source → newest, date of the ADR/intake/ruling that commits to the item,
through today (2026-08-17):

| # | item | committing source (date) | age | note |
|---|---|---|---|---|
| 1 | dev-knowledge-kernel package (versioned installable methodology kernel) | intake 2026-08-05 (ACCEPTED) | 12 days | largest undelivered structural commitment found — no package artifact exists anywhere in the tree |
| 2 | GitHub reusable workflow (single CI definition for all consumers) | intake 2026-08-05 (ACCEPTED, "W-4") | 12 days | only the hub's own `report-only-wall.yml` exists; no shared/reusable workflow found in any of the 5 consumer repos |
| 3 | README.md as universal front door (VISION.md rename) | intake 2026-08-05 (ACCEPTED, ADOPTED) | 12 days | contradicted by current tree — `VISION.md` still the live file |
| 4 | pytest-testmon (test-impact analysis for the dev loop) | intake 2026-08-05 (ACCEPTED, operator-endorsed) | 12 days | reiterated 2026-08-06 as "SCHEDULED(batch-2...)"; still not landed |
| 5 | check-jsonschema / pydantic schema-as-code (W-6) | intake 2026-08-05 (ACCEPTED) | 12 days | "DEFERRED(floats behind W-5)" per the 2026-08-06 follow-on intake |
| 6 | gh CLI findings-as-Issues | intake 2026-08-05 (ACCEPTED, "P3") | 12 days | "UNPLACED(reshaped: batch-per-run)" |
| 7 | copier (fleet-wide living-template propagation) | intake 2026-08-05 (ACCEPTED, "W-1") | 12 days | no ADR, no dedicated BACKLOG row; config-packaging BACKLOG rows (`[#371]` etc.) are adjacent, not this item |
| 8 | lychee (dead-link checker) | intake 2026-08-05/06 ("EVAL-RUN(ADOPT-candidate...)") | 11-12 days | verdict reached, never built or filed |
| 9 | import-linter (architecture/import-boundary gate, preferred over `tach`) | intake 2026-08-09 (ACCEPTED) | 8 days | reiterated 2026-08-16 as "the natural [#533] follow-on" |
| 10 | deptry (dependency scanner) | intake 2026-08-09 (ACCEPTED) | 8 days | |
| 11 | semgrep (library-first custom-rule enforcement) | intake 2026-08-09 (ACCEPTED) | 8 days | |
| 12 | mypy / basedpyright (fleet-wide type checker + baseline) | intake 2026-08-09 (ACCEPTED) | 8 days | |
| 13 | markdown_it fence detection (2 of 3 planned sites) | intake 2026-08-09 (ACCEPTED) | 8 days | "landed at 1 of 3 sites" — partial build, not a clean gap |
| 14 | mise (toolchain pinning, uv-pin-class fix) | intake 2026-08-06→09 (ACCEPTED by 08-09) | 8 days | "CLASS CHANGE PROPOSED, NOT RULED" as of 08-06 |
| 15 | gh CLI (de-facto adopted, one ledger line owed) | intake 2026-08-08 (ACCEPTED) | 9 days | smallest-cost item on this list — a single ledger line closes it |
| 16 | skill-creator / ponytail (Tier S try-now skills) | intake 2026-08-08 (ACCEPTED) | 9 days | no confirmed install evidence found in this snapshot |

**Not ranked here** (excluded on purpose, with reason):
- Items with a confirmed **BACKLOG row** (`[#502]` mutmut, `[#529]` telemetry, `[#530]`/`[#531]`
  git-ref CAS, `[#322]`/`[#171]`/`[#169]` dashboards, `[#491]` Gemini lane, `[#383]` networkx,
  `[#371]` etc. config-packaging) are **ROW-OPEN**, not DECIDED-UNFILED — they are already
  someone's job, just not yet done. Counted separately in the packet line.
- **AGENTS.md rename (W-9a)** is excluded — it is not silently unfiled, it was explicitly
  reversed by a later intake citing ADR-53. That is a closed loop, not a gap.
- Items still at intake **status: DRAFT** (radon/xenon enforcement order, PostToolUse lint hook,
  the general "config packaging" umbrella) are excluded — a DRAFT has not yet been ruled ACCEPTED,
  so there is no decision yet to be unfiled.

---

## Step 3 — §B UNIVERSALIZATION, concrete

### Is there a shared config package, and which repos consume it?

**Yes, partially — the `deploy/manifest-v1.4.0.yaml` carrier system**, not a single package.
Two carriers matter most:

- **`floor` carrier** (`templates/child-methodology-floor.md.tmpl` → `.claude/CLAUDE-FLOOR.md` +
  `.sha256` + `check_floor_hash.py`, guarded by the `floor-hash-verify` pre-commit hook):

  | Consumer | Floor present? | Hub-hosted pre-commit hooks wired? |
  |---|---|---|
  | `ai-council` | YES | YES (`toc-freshness`, `backlog-id-on-close`, `block-ff-push`) |
  | `corp-monorepo` | YES | YES (`backlog-id-on-close`, `block-ff-push`) |
  | `corp-sca-time-automation` | YES | **partial** — only local `floor-hash-verify`, no hub-hosted repo entry |
  | `corp-ops` | **NO** | NO — no `.pre-commit-config.yaml` at all |
  | `win-tooling` | **NO** | NO — no `.pre-commit-config.yaml` at all |

- **`docs` carrier** (`docs/intake/README.md` + `templates/intake-template.md` + root `INSTALL.md`):
  fully present in `ai-council` and `corp-monorepo` only; `corp-ops` carries a root `INSTALL.md`
  with no floor/pre-commit backing it (likely hand-copied); `corp-sca-time-automation` and
  `win-tooling` carry neither.

**Net: 2 of 5 registered consumers (`ai-council`, `corp-monorepo`) are fully deployed. 1 is
partial (`corp-sca-time-automation`). 2 consume nothing from the hub (`corp-ops`, `win-tooling`).**

### Every `configs/`-class directory in hub and consumers

No directory is literally named `configs` anywhere in the fleet; all instances are `config`
(`node_modules`, `.venv`, `.git` excluded).

| Repo | Path | Contents |
|---|---|---|
| hub (`.dev-knowledge`) | `config/` | **ONE file**: `requirements-dev.txt` — `pre-commit>=3.5.0`, `click>=8.0`, `pyyaml>=6.0` (superseded by `pyproject.toml`'s uv-managed groups per ADR-106, retained under the no-delete invariant) |
| `corp-ops` | `config/` | **ONE file**: `paths.yaml` — OneDrive/gdrive path declarations and sync-exclusion rules |
| `ai-council` | `config/` | multiple files: `config_loader.py`, `settings.yaml` (22.2KB), `settings.smoke.yaml` (14.3KB) — not near-empty |
| `corp-monorepo` | `config/` | multiple files/dirs: `agents.yaml`, `audit.yaml`, `content_registry.yaml`, `naming_config.yaml`, `paths.toml`, `workflows.yaml` + 4 subdirs — not near-empty |
| `corp-sca-time-automation` | `config/` | 4 small YAML files (`category_mapping.yaml`, `excluded.yaml`, `settings.yaml`, `tenrox_mapping.yaml`) |
| `win-tooling` | `config/` | no top-level files; 5 subdirectories only (`dev-terminals/`, `dispatch/`, `flow-launcher/`, `typewhisper/`, `vscode-agents/`) |

Two directories are genuinely single-file-thin (hub's own `config/`, `corp-ops`'s `config/`) — both
candidates for retirement or consolidation into the `deploy/` carrier system, not new territory.

### Per-repo Codex/agent readiness

| Repo | `CLAUDE.md`? | `AGENTS.md`? | Runbook present? |
|---|---|---|---|
| hub (`.dev-knowledge`) | YES | NO | NO — only the generator template `templates/consumer-onboarding-runbook.md` |
| `ai-council` | YES | NO | NO |
| `corp-monorepo` | YES | NO | NO |
| `corp-ops` | YES | NO | NO |
| `corp-sca-time-automation` | YES | NO | NO |
| `win-tooling` | YES | NO | NO |

No repo — hub or consumer — has a root `AGENTS.md`, consistent with ADR-53 ("AGENTS.md is retired
here — CLAUDE.md is the single instruction file"). **No repo has a genuine deployed runbook file.**
The only runbook-shaped artifact anywhere is the hub's template, which generates one but has
generated none yet (`[#293]`-family, ROW-OPEN, tracked in `tasks/293-consumer-runbook-fan-out.md`).

### What "universalization" is DEFINED as in the sources

**NO FORMAL DEFINITION EXISTS.** The term is used across 87 ADRs, 36 intakes, and 14
protocol/VISION/ARCHITECTURE files — never once formally defined as a noun. The closest the corpus
comes:

> VISION.md §Vision: *"It is the ecosystem's knowledge guardian and methodology author: it absorbs
> lessons from individual projects, universalizes them into patterns, and disseminates those
> patterns back as enforceable conventions."*

This describes the **verb** ("universalizes") as a three-step process — absorb → pattern →
disseminate — but the corpus never states "universalization is..." Every other occurrence
(VISION.md §Relationships "per ADR-33 universalization"; PLAYBOOK.md's BACKLOG theme name "Cross-
repo universalization"; three bare usages in intake docs) treats the word as a **label pointing at
ADR-33** or as a BACKLOG-theme name, not a defined concept. **ADR-33 itself** (`docs/decisions/
ADR-33-vision-universalization.md`, 2026-04-28) is the closest thing to a canonical source — it
establishes the recurring "Mandate / Recommendation / Migration cohort / Cross-repo audit"
operational shape that ADR-34 through ADR-41 (and the now-deprecated ADR-40) each instantiate —
but even ADR-33 never writes a sentence of the form "universalization means X." **The absence is
itself the finding**, per the contract's own instruction not to synthesize a definition.

---

## Step 4 — §C PERFORMANCE LEDGER

Every measured number located, with locator. Grouped by theme.

### Test-suite performance
| metric | value | locator |
|---|---|---|
| pytest-xdist speedup | 5.2× (serial 1785.61s → `-n auto` 358.77s/330.15s) | STANDING_RULINGS §E1; ADR-110 amend 2026-08-06 |
| Suite runtime, pre-instrumentation-fix | 1903.85s (0:31:43) | `docs/audits/2026-08-09-technical-night-n3-performance-instrumentation.md:91-92` |
| Suite runtime, post-fix | 539.12s (0:08:59) | same, :93-94 |
| Constant-population inflation | 532.28s → 1903.85s, ×3.58 (22m51s pure overhead) | same, :106,112 |
| Worktree-sweep scaling (0/3/6/13 worktrees) | 71.80s → 289.84s → 527.92s → 1086.56s (15.13× at 13) | same, :196-199 |
| Corpus size at measurement | 1,633 md files, 20.8 MB (JOURNAL.md alone 2.29 MB) | same, :160-162 |
| Full suite, 4 cores | 462.81s (0:07:42), 2721 collected | same, :243-244 |
| Collection-only cost | 4.97s / 2721 tests = 1.1% of run | same, :246-247 |
| CPU utilization (4-core full run) | 14.6% (269.7s CPU / 462.8s wall) | same, :254-256 |
| Host full suite wall-clock | 918.9s | PLAYBOOK Ch5 (JOURNAL.md 2026-08-15 (a)) |
| 4-core cloud container, serial vs `-n auto` | 701.6s vs 473.0s (1.48×) | PLAYBOOK Ch5 |
| Slowest single test's share of suite cost | 38.4% | PLAYBOOK Ch5 |
| Exclusion-set (Tier A) coverage/cost | 96.5% of tests at 22.1% of cost | PLAYBOOK Ch5 |
| pythonpath Shape `["."]` isolated-collection failures | 67 of 99 test files | STANDING_RULINGS §H4 |
| pythonpath Shape B isolated-collection failures | 0/99 | STANDING_RULINGS §H4 |
| sys.path.insert lines retired | 75 lines across 72 files | STANDING_RULINGS §H4 |
| `[#521]` pre/post-rollout measurement | 0/101 three times — "three greens carrying no information" | PLAYBOOK Ch12 |

### Repo/corpus scale
| metric | value | locator |
|---|---|---|
| CLAUDE.md line budget | ≤200 lines (self-declared) | CLAUDE.md §12, measured 193-200 across v2.59-2.62 |
| audit.py `ALL_CHECKS` registry size | 41 members | PLAYBOOK Ch8 |
| silent_rule_ratchet budget | 440 live ≤ 441 baseline | STANDING_RULINGS multiple; `docs/audits/2026-08-10-technical-research-corpus-distillate.md:34` |
| Backlog row char ceiling | 1320 chars (superseded 1200) | PLAYBOOK Ch6 |
| Open backlog + deferred (H2) | 168 open + 26 deferred = 194 task nodes | STANDING_RULINGS §H2 |
| Backlog testability census (2026-08-10) | 170 rows: 75 MECHANICAL / 72 PROSE-CONVERTIBLE / 15 PROSE-JUDGMENT / 8 DEFECTIVE | STANDING_RULINGS §O-3 |
| Rule-C allowlist admitted tracked paths | 2054 → 2147 (0 offenders) | STANDING_RULINGS §K-1/K-2 |
| Fleet repo count | 9 git repos | ARCHITECTURE.md §Purpose (ADR-104) |
| Deploy carrier roster (v1.4.0) | 7 declared (6 `implemented:true`, 1 `false`) | ARCHITECTURE.md §Validators |
| Child floor token budget | ≤1,500 tokens (hard) | ADR-78 §4; PLAYBOOK Ch2 |
| nb6 achievements window | 49 hours, 131 commits, 152 files, +17,539/−1,338 lines | `docs/audits/2026-08-16-verification-nb6-achievements.md:5` |

### Cost / model economics
| metric | value | locator |
|---|---|---|
| Council debate overhead | ~$0.50, ~5 min | AI_COUNCIL_PROCESS.md |
| Council synthesis cost | $0.04/debate | ENVIRONMENT.md §API Keys |
| Council cost-surprise threshold | >$1.00 | AI_COUNCIL_PROCESS.md Troubleshooting |
| Single-model + critic cost/time | ~$0.05, ~2 min | PLAYBOOK §5 |
| Share of decisions not needing Council | >70% | PLAYBOOK §5 |
| Claude Max plan cost | $100/month | ENVIRONMENT.md |
| GMKtec rejected local-inference cost/ROI | $2,500 / 38-month ROI | ENVIRONMENT.md §Rejected |

### Undelivered performance commitments (explicitly flagged in-tree, not yet measured)
| commitment | locator |
|---|---|
| Full-suite run not performed (only `--collect-only`, 2,897 items) | `docs/audits/2026-08-14-qa-night2-quality.md:477` |
| Worktree-sweep slowdown: "roughly a quarter... explained. About 17 minutes remain unexplained" | `docs/audits/2026-08-09-technical-night-n3-performance-instrumentation.md:218-220` |
| `[#528]` leg 3: `test_run` duration telemetry not yet emitted (owed after `[#529]`) | BACKLOG `[#528]` |
| `[#529]`: "a recorded gate run reads back without re-measurement" — phase-3 wiring owed | BACKLOG `[#529]` |
| `[#502]` mutmut: surviving-mutant count + ADOPT/REJECT verdict not yet run | BACKLOG `[#502]` |
| `[#502]` mutmut under `uv run --locked`: behavior NOT VERIFIED | BACKLOG `[#502]` |
| `[#278]`: "why did the suite get faster" — evidence owed before cleanup | BACKLOG `[#278]` |
| `[#317]`: "not slow" targeted run under 60s — time not yet recorded at build | BACKLOG `[#317]` |
| `[#492]`: Grok vs terra catch-rate comparison — not yet run (deferred, Grok 4.6 unreleased at last check) | BACKLOG `[#492]` |
| `[#332]`: automated dependency-version-drift WARN check — bootstrap only, clause-1 unbuilt | BACKLOG `[#332]` |
| `[#511]`: post-change handoff wall-clock/token cost vs baseline — not yet measured | BACKLOG `[#511]` |
| `[#418]`: controlled reproduction of fleet-audit's 0-10 baselines/day multiplicity — promised as FIRST build step, not yet run | BACKLOG `[#418]` |
| `[#530]`: single-flight T2/T4 concurrency properties not yet demonstrated against real `origin` | BACKLOG `[#530]` |
| `[#533]`: audit.py decomposition's parallel-execution promotion to default — gated on a before/after wall-clock not yet run | BACKLOG `[#533]` |

---

## Step 5 — §D HONEST TOP-10

Ranked by cost to the operator, not by how interesting the work is. Each: cost · smallest next
step · row status.

1. **Telemetry write-only-and-uncalled (`[#529]`).** A fully-built SQLite-WAL event-emission
   library with zero call sites — the repo cannot answer "is this gate actually firing" from data,
   only from prose. **Cost:** every enforcement-coverage claim in this repo rests on manual
   witnessing, not measurement. **Smallest next step:** wire ONE call site (the `journal_spine_anchor`
   check already named as the calibration target) and confirm a readback. **Row:** OPEN, `[#529]` P1.

2. **`dashboards`/`[#171]` conformance dashboard does not exist.** The read-format the dashboard
   will consume is built (`scripts/audit_checks/_common.py`); no dashboard reads it. **Cost:** the
   operator has no single-glance fleet-health view; every check requires running `audit.py`
   by hand. **Smallest next step:** the format is ready — build the thinnest possible read-only
   HTML viewer over it. **Row:** OPEN, `[#171]` P3, DEFERRED/parked.

3. **Two of five registered consumers (`corp-ops`, `win-tooling`) consume nothing from the hub.**
   No floor, no pre-commit hooks, no `docs/intake/`. **Cost:** methodology drift on these two repos
   is currently invisible — the fleet-parity gate cannot even see them as non-conformant if they
   were never wired in the first place. **Smallest next step:** run the floor-deploy carrier once
   against each. **Row:** UNFILED — no BACKLOG row names this specific gap (adjacent rows exist for
   config-packaging generally, not this).

4. **`git-ref CAS` (single_flight.py) is fully built, advisory, and wired into nothing.** The
   single-flight dispatch guard this repo needs to prevent duplicate concurrent lane provisioning
   exists as a library + CLI and gates zero real paths. **Cost:** the exact race the mechanism was
   built to prevent (duplicate/racing lane provisioning under a live batch — this very session is
   evidence: three overlapping `pre-commit` runs, section "Step 0" of this lane's own execution)
   remains possible. **Smallest next step:** `[#531]`'s own proposed fix — wire it via the
   `reference-transaction` git hook, the one point every provisioning path crosses. **Row:** OPEN,
   `[#530]`/`[#531]` P2.

5. **`import-linter` accepted twice (2026-08-09, reiterated 2026-08-16) as the preferred
   architecture-boundary tool, never filed or installed.** **Cost:** the module-boundary violations
   it would catch (the exact class of bug that made `[#533]`'s decomposition necessary) keep
   recurring without a mechanical gate. **Smallest next step:** `pip install import-linter`, one
   `.importlinter` config scoped to `scripts/`. **Row:** UNFILED (see §A #9).

6. **`lru_cache` evidence conflict, unresolved by this lane.** BACKLOG `[#533]` claims a landed,
   tested memoization leg (42.7s→17.8s per commit); the wiring-sweep grep found zero `lru_cache`
   hits in `scripts/`. **Cost:** either the BACKLOG row is stale (claims a win that isn't in the
   tree) or the grep missed something — either way, someone is trusting a number that hasn't been
   re-verified. **Smallest next step:** one `grep -rn lru_cache scripts/` and a `[#533]` status
   correction either way. **Row:** OPEN, `[#533]`, evidence conflict flagged not resolved.

7. **Five distributed, unratified "dev-knowledge-kernel package" and "GitHub reusable workflow"
   commitments (2026-08-05, 12 days old) sit unfiled.** These are the two largest structural
   promises in the entire intake corpus — a versioned installable methodology package, and a single
   shared CI definition for every consumer — and neither has a BACKLOG row twelve days later.
   **Cost:** every consumer keeps hand-rolling its own CI and its own copy of the methodology
   corpus, which is the exact drift class ADR-91/ADR-92 exist to prevent. **Smallest next step:**
   file both as BACKLOG rows (this lane cannot — births nothing). **Row:** UNFILED (§A #1, #2).

8. **No repo in the fleet has a deployed runbook**, despite a generator template existing and a
   tracked ticket (`[#293]`-family) for the fan-out. **Cost:** onboarding a new consumer or
   recovering from an incident requires the operator's own memory, which is precisely the failure
   mode this whole inventory exists to avoid. **Smallest next step:** run the generator once
   against `ai-council` (the most-deployed consumer) as the pilot. **Row:** OPEN, `[#293]`-family.

9. **`AGENTS.md` universalization reversed mid-flight (ACCEPTED 2026-08-05, retired by ADR-53
   citation 2026-08-12) with no trace of the reversal outside the two intake documents.** **Cost:**
   low direct cost (the reversal is coherent and correctly cited), but it is a documented instance
   of an ACCEPTED intake being silently overridden a week later — a pattern worth watching, since
   nothing currently diffs ACCEPTED-intake claims against later-superseding ADRs automatically.
   **Smallest next step:** none needed technically; flagged for awareness. **Row:** none needed.

10. **The word "universalization" has organized five ADRs' worth of structure (ADR-33 through
    ADR-41) since 2026-04-28 and has never been formally defined.** **Cost:** low-but-compounding —
    every new ADR that invokes "per ADR-33 universalization" inherits an undefined term, and this
    contract's own Step 3 instruction ("quote it, or state NO DEFINITION EXISTS") exists precisely
    because a prior session needed the definition and couldn't find one. **Smallest next step:** a
    single sentence added to ADR-33 or VISION.md stating the definition this report's §B synthesized
    from the existing "absorb→pattern→disseminate" language. **Row:** none — a documentation fix,
    not a backlog-shaped item.

---

## Packet

```
total 78 · LIVE-WIRED 21 · BUILT-UNWIRED 4 · ROW-OPEN 17 · DECIDED-UNFILED 16 · EVALUATED-REJECTED 9 · MENTIONED-ONLY 11
```

(Counts are of master-table rows in this report, not of every sub-item the research agents
returned — the full raw findings, including several hundred additional ADR/intake/BACKLOG rows
not promoted to the master table, are preserved in this lane's session transcript per the
scope-limit note at the top of this file.)

**Branch:** `worktree-lane-c-505-north-star-inventory`

**Commits this lane:**
- `be9a4c43` — docs(audits): commit lane c contract of record — batch 7a north-star inventory `[#505]`
- (this report's commit — see below)

**Decisions taken under budget:**
- Declared the `lru_cache` BACKLOG-vs-grep conflict rather than silently picking a side (no
  authority to re-verify scripts/ state beyond what the wiring-sweep agent already grepped).
- Excluded DRAFT-status (not yet ACCEPTED) intake proposals from §A's DECIDED-UNFILED ranking,
  since a DRAFT is not yet a decision.
- Excluded ROW-OPEN items from §A even where their BACKLOG row is old, since "decided but
  unfiled" and "decided, filed, and slow" are different problems — conflating them would make §A
  dishonestly long.
- Treated the AGENTS.md/W-9a reversal as a closed loop (ADR-53 citation), not a live gap.
- Capped the master table's "beyond the floor" section at items with a clean, locator-backed
  disposition (LIVE-WIRED / EVALUATED-REJECTED / DECIDED-UNFILED with a confirmed no-row check)
  rather than reproducing the full multi-hundred-row ADR/intake/BACKLOG corpus verbatim — this is
  the report's one significant scope decision, stated explicitly per the contract's own
  no-silent-caps spirit.

**This lane does not merge and does not push. Commit-and-STOP.**
