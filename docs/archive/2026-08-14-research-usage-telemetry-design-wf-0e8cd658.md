> **What was asked:** usage-telemetry design for a solo, local-first methodology ecosystem — event schema, storage, read surfaces, and explicit adopt/do-not-adopt verdicts (OpenTelemetry/Prometheus+Grafana/Zabbix/Splunk).
> **When:** commissioned 2026-08-09 (the same wave as the six-memo research corpus below), landed 2026-08-14 — `docs/archive/` is the sanctioned Tier-2 genre folder for this holding-zone role (ADR-101 §1: "Tier-2 — `docs/` genre folders. Sanctioned: `archive/ audits/ decisions/ handoffs/ intake/ runbooks/`").
> **EXTERNAL EVIDENCE — advisory until ratified, never doctrine by virtue of existing.**

# Usage Telemetry for a Solo, Local-First Methodology Ecosystem: A Library-First Design

## TL;DR
- **Build a single append-only event log in SQLite (WAL mode), write to it from ~8 event types via a ~40-line `structlog` helper, and read it with a `rich`/`plotext` in-terminal `dispatch report` command plus ad-hoc `datasette telemetry.db` — this stays well under ~200 lines of glue and answers "is what I ship actually used?" without any server.** Combine that live event stream with three *derived* (recomputed on demand) signals: `deptry` for dead dependencies, `coverage.py` for code-path usage evidence, and git-history parsing for task-flow metrics.
- **OpenTelemetry, Prometheus+Grafana, Zabbix, and Splunk are all overkill here and should NOT be adopted.** They are architected for multi-host fleets and continuous scraping/ingest; Zabbix's server/frontend do not even run natively on Windows, and Splunk's model targets enterprise log volumes. Their standing databases, services, and agents are exactly the maintenance burden the operator wants to avoid.
- **The highest-value signals are "organ usage" (which of the ~42 checks, hooks, and CLI commands actually fire) and "blocker efficacy" (did a gate ever refuse an action).** These directly drive methodology decisions — retire a never-firing check, promote a high-value hook, prune a dead dependency — and cannot be derived from git history alone, so they are the events genuinely worth instrumenting.

## Key Findings

1. **You already have most of the raw data; the gap is a uniform event log.** Git history, task markdown files, BACKLOG.md, mutmut output, and pytest timings are all queryable retroactively. What you *cannot* reconstruct after the fact is "how often did check X fire and pass/fail" and "did guardrail Y ever block me." Those are the events worth actively logging.
2. **One SQLite append-only log covers all live signals.** A single schema — `timestamp, event_type, name, outcome, duration_ms, context` — handles hook fires, check results, CLI/dispatch invocations, and blocker events. SQLite's official Write-Ahead Logging documentation states that in WAL mode "readers do not block writers and a writer does not block readers. Reading and writing can proceed concurrently," which matters when pre-commit/pre-push hooks and agent lanes run in parallel. (One caveat from that same doc: "All processes using a database must be on the same host computer; WAL does not work over a network filesystem" — irrelevant for a single local machine, but worth knowing before any future sync.)
3. **Dead-dependency and dead-code detection are "derived" signals — run them on demand, don't stream them.** `deptry` (release 0.25.1, published March 18, 2026 on PyPI with `win_amd64` wheels; conda-forge lists `win-64` support; supports uv/PEP 621) answers "which declared deps are never imported." `coverage.py` (7.15.x, 2026) answers "which of my own code paths actually execute." Neither belongs in the event log; both are commands you run and whose one-number summaries you can append to the log for trending.
4. **Industry CLI telemetry (Homebrew, Next.js, Angular, GitHub CLI) validates the "feature usage → keep/kill" loop but its privacy/opt-out/network machinery does not transfer.** The transferable idea is precisely Homebrew's stated purpose. The non-transferable part is anonymization, remote ingestion, and consent — you are the only user, so log locally and richly.
5. **DORA-style flow metrics are computable for a solo repo but must be reinterpreted.** Deployment frequency, lead time, and change-failure rate can be derived from git, but with no production and no external users, they degrade to "commit cadence," "task cycle time," and "revert/fix rate." Treat them as personal-cadence trends, not performance scores.

## Details

### Q1 — Signals worth collecting

**(a) Library/dependency usage — which installed deps are actually used vs dead.**
- *Why it matters:* Every declared-but-unused dependency is maintenance surface (upgrades, audit noise, lockfile churn) with zero value.
- *Cheapest credible method:* `deptry .` — it scans imports across all `.py` files and compares to `pyproject.toml`, flagging `DEP002` (declared but unused), `DEP001` (missing), `DEP003` (transitive), `DEP004` (misplaced dev dep). It natively supports uv/PEP 621 projects and ships Windows wheels. Run it as one of your ~42 audit checks and log the count of `DEP002` hits per run.
- *Complements:* `uv tree` (and `uv tree --outdated`) renders the resolved dependency graph from the lockfile so you can see transitive weight; `pip-audit` (runnable via `uv run pip-audit`) flags known CVEs. `coverage.py` gives *runtime* usage evidence for your own modules (0%-coverage functions are dead-code candidates, with the caveat that coverage measures *tested* execution, not *all* execution). `import-linter` (current stable 2.12, released June 23 2026; pure-Python, runs on Windows, needs Python ≥3.10) is a different tool — it enforces *architectural* import contracts (layering, forbidden imports), not dead-dep detection, so adopt it only if you want to codify module boundaries, not for usage telemetry.
- *Noise:* Low-to-moderate. `deptry` has documented false positives for side-effect-only imports and plugins loaded by name; suppress with `# deptry: ignore` or config. `coverage`-as-usage over-reports dead code because untested ≠ unused.

**(b) Feature/organ usage — which custom checks, hooks, CLI commands, and slash-commands actually fire.**
- *Why it matters:* This is the core "is my shipped organ used?" question and the single highest-value signal. You have ~42 audit checks, multiple git hooks, a `dispatch` command, and agent lanes — some are almost certainly dead weight.
- *Cheapest credible method:* Emit one event per fire from the entry points you already control. For the audit registry, wrap the check dispatcher so each check logs `{event_type: "check", name, outcome, duration_ms}`. For git hooks, add one line to your pre-commit/pre-push scripts that appends an event (pre-commit itself has no built-in metrics hook — an open upstream issue confirms per-hook metrics are not provided — so a wrapper is the established pattern). For `dispatch` and CLI commands, log at the top of the handler. For Claude Code / Codex lanes, use Claude Code's `PostToolUse`/`SessionStart`/`Stop` hooks, which are explicitly designed for telemetry and audit logging and receive JSON on stdin — the community `session-log` pattern is ~37 lines appending one JSONL line per tool call.
- *Noise:* Low. A counter per named organ is inherently clean. The only discipline needed is a stable `name` taxonomy.

**(c) Blocker efficacy — how often gates/hooks refuse an action.**
- *Why it matters:* A guardrail that never fires is either perfectly preventive or pure ceremony — and you cannot tell which without counting. This is distinct from (b): you want `outcome ∈ {pass, block}` per fire.
- *Cheapest credible method:* Reuse the same event schema; when a hook/check exits non-zero (blocks a commit/push/action), log `outcome: "block"` with the reason. Over weeks, a check with fires>0 and blocks=0 is a candidate for downgrade to warning; a check with a high block rate is a candidate for promotion/earlier placement.
- *Noise:* Low, but watch for "self-inflicted" blocks during your own experimentation vs genuine catches — a freeform `context` field helps disambiguate later.

**(d) Workflow/task-flow metrics — backlog growth/shrink, state transitions, cycle time.**
- *Why it matters:* Tells you whether the methodology is actually moving work, and where tasks stall.
- *Cheapest credible method:* Derive from artifacts you already generate — one markdown file per task plus BACKLOG.md — parsed from git history. Cycle time = first commit touching a task file → task marked done. Backlog size over time = line/entry count of BACKLOG.md across commits. This is a read-only git-log parse; no instrumentation needed. Tools like `github-dora-metrics` and GitLab's DORA API show the standard formulas, but for a solo local repo you compute the simplified versions yourself.
- *Noise:* Moderate. Task-state parsing depends on consistent markdown conventions; git timestamps reflect commit time, not work time.

**(e) Test/tooling health signals worth trending.**
- *Why it matters:* Mutation score and suite duration are leading indicators of test *quality* and *friction*, respectively.
- *Cheapest credible method:* After a `mutmut run`, append `{event_type: "mutation", score, killed, survived}` to the log; after pytest, append suite duration. mutmut's own docs note the baseline full-suite run time is already measured, so duration is free. Trend both over time rather than gating on absolute numbers.
- *Noise:* Moderate for mutation score (equivalent mutants inflate "survived"); low for suite duration.

### Q2 — Tools/libraries, library-first

**Storage.** Start with **SQLite in WAL mode** as the event store, not raw JSONL. Both are append-friendly, but SQLite gives you SQL queries, `datasette` for free exploration, and safe concurrency: per SQLite's official WAL docs, "readers do not block writers and a writer does not block readers. Reading and writing can proceed concurrently." Set `journal_mode=WAL`, `synchronous=NORMAL`, `busy_timeout=5000`. JSONL is a fine *transport* if you want dead-simple hook scripts that can't even import a DB driver; if you go JSONL-first, ingest into SQLite with `sqlite-utils insert` for reading. Recommendation: JSONL append from the lowest-level shell hooks (zero dependencies), everything else writes SQLite directly.

**Logging library.** Use **structlog** for the Python-side event helper. On Python 3.14 benchmarks it is "roughly 2× faster than stdlib and Loguru for simple messages," its processor chain cleanly produces JSON, and it can wrap stdlib logging. Loguru is the "zero-config" alternative and is fine, but structlog's structured-event model maps directly onto your event schema. Plain stdlib `logging` + `python-json-logger` is the "works everywhere, least deps" fallback. Avoid hand-rolling JSON formatting.

**Reader/report surface.** Two tiers:
- *In-terminal (primary):* a `dispatch report` subcommand using **rich** tables + **plotext** for sparkline/bar trends directly in the terminal (plotext has official rich integration and a matplotlib-like API, needs nothing but itself). This is your daily driver and fits the CLI-first workflow.
- *Ad-hoc exploration (secondary):* **Datasette** pointed at `telemetry.db` (`datasette telemetry.db`) gives an instant local web UI + JSON API with zero schema config. It's the right tool for "let me slice this six ways once a month." Simon Willison's `llm`/`sqlite-utils`/`datasette` stack is a proven local-analytics pattern.
- *Do NOT* stand up Streamlit for v1 — it reruns the whole script per interaction and is a standing process to maintain; Datasette covers the same need with less glue. Reserve Streamlit only if you later want interactive filtered dashboards.

**OpenTelemetry — overkill locally, but with a caveat.** OTel is designed for distributed tracing across services; running even the local Collector is described by practitioners as "overkill" for local dev. There *is* a minimal story — a `ConsoleSpanExporter` or the Collector's **file exporter** (still alpha for traces/metrics/logs) writing OTLP JSON to disk, optionally a local Jaeger in Docker on ports 4317/16686. But this buys you nothing over SQLite for single-user counting, adds a schema and a dependency, and its value (trace propagation across service boundaries) doesn't exist in your world. **Verdict: do not adopt for v1.** Revisit only if you ever want distributed tracing across many agent processes with parent/child spans.

**Enterprise monitoring — explicit "do not adopt" verdicts.**
- **Prometheus + Grafana: overkill.** It is a pull-based time-series system for scraping infrastructure metrics; even homelab users call a single-machine Grafana stack "totally overkill." It presumes a scrape target, a TSDB, and a dashboard server running continuously — three standing services to answer questions a SQL query answers. **Do not adopt.**
- **Zabbix: overkill and Windows-hostile.** Zabbix requires a minimum of three co-dependent components — the Zabbix server daemon, an RDBMS backend (MySQL/MariaDB or PostgreSQL), and a PHP web frontend on Apache/Nginx — plus agents on each monitored host. Its official docs describe it as built "around modern web servers, leading database engines, and PHP scripting language." Critically, the Zabbix **server and frontend are not supported natively on Windows** (Wikipedia's platform line reads "Windows (agent only)"; the official Windows install docs cover only the agent, which "run[s] as a Windows service"), so monitoring your Windows 11 machine would require standing up a separate Linux host/VM/container for the server+DB+frontend. It is architected for fleets of networks, servers, VMs, and cloud with SNMP/IPMI/JMX and proxies for scale. **Do not adopt.**
- **Splunk: overkill by an order of magnitude.** Splunk's reference indexer hardware is enterprise-grade — its Enterprise Security performance reference specifies indexers "with 32 GB of RAM and 16 CPU cores," and its capacity-planning reference hardware describes indexers with "12 physical CPU cores, or 24 vCPU" scaling to "48 physical CPU cores" with thousands of concurrent IOPS. Its architecture is distributed (separate indexers, search heads, management components), and its licensing is volume-based on data ingested per day, targeting enterprise log volumes. Per Splunk's official "About Splunk Free" docs, the Free license limit is "500 MB per day," and the Free tier strips core features — "Ingest actions is not available. Alerting (monitoring) is not available. There are no users or roles. This means: There is no login" — and after repeated license-violation warnings Splunk "continues to index your data but disables search functionality." Nothing about a solo dev's event trickle justifies this. **Do not adopt.**

### Q3 — Industry patterns and what transfers

- **The "keep or kill a feature" loop transfers directly.** GitHub CLI's telemetry rationale, verbatim from GitHub's docs — "when a new subcommand is shipped, telemetry reveals whether anyone is using it and how. If adoption is low, that signals a need to revisit the feature's discoverability or design" — is exactly your organ-usage question at solo scale. Homebrew's analytics documentation states the purpose plainly: analytics show "whether a feature is used enough to justify its maintenance cost," while wisely warning that "Analytics must not replace technical evidence or maintainer judgement" and "Low usage alone does not establish that removing a command or package is safe." Adopt that humility: treat low-usage organs as *review candidates*, not automatic deletions.
- **Event granularity transfers.** These CLIs log command name + flags + outcome + minimal environment — precisely your `name/outcome/context` schema. GitHub CLI logs ~20+ fields including `skill_names`, mirroring your slash-command/skill tracking.
- **What does NOT transfer:** anonymization, pseudonymization, opt-out/consent flows, background HTTPS shipping to a collector (Homebrew sends to InfluxDB with 365-day retention; Next.js ships to Vercel). You are the sole user on a local machine — skip all of it. No network, no consent banner, no PII scrubbing.
- **DORA transfers only in reinterpreted form.** With no production/deploys, map: deployment frequency → commit/merge cadence; lead time for changes → task cycle time; change failure rate → revert+hotfix rate from commit messages; MTTR → time-to-close on tasks labeled bug/fix. The DORA guidance itself stresses these are "a diagnostic tool, not a scorecard" and best judged "compared to our own baseline from three months ago" — apt for a solo operator.

### Q4 — Concrete minimal v1 design

**The v1 slice: one event log, ~8 event types, two read surfaces.**

*Storage:* `telemetry.db` (SQLite, WAL). Single table `events(id, ts, event_type, name, outcome, duration_ms, context_json)`. Optionally a `snapshots` table for daily derived rollups (dep count, mutation score, backlog size).

*The 8 highest-value events to log (v1):*
1. `check_run` — each audit check fires: `name`, `outcome` (pass/block/error), `duration_ms`. → *Feeds:* retire checks with fires>0/blocks=0; promote high-catch checks.
2. `hook_run` — each git hook (pre-commit/pre-push) fires: `name`, `outcome`. → *Feeds:* is a hook pure ceremony? Promote/demote.
3. `blocker_fired` — any gate that refuses an action, with reason in `context`. → *Feeds:* guardrail efficacy; the "did it ever fire" question.
4. `dispatch_invoked` — `dispatch` command + subcommand/lane. → *Feeds:* which lanes/commands are actually used.
5. `agent_session` — Claude Code/Codex session start/stop via hooks, with tool-call count in `context`. → *Feeds:* which agent lanes deliver work; session cost/verbosity.
6. `test_run` — pytest suite duration + pass/fail. → *Feeds:* suite-friction trend.
7. `mutation_run` — mutmut score/killed/survived (append after each run). → *Feeds:* test-quality trend.
8. `dep_scan` — deptry `DEP002` count + coverage % (append after each scan). → *Feeds:* dead-dependency / dead-code pruning.

*Read surface:* `dispatch report` (rich tables + plotext trends in terminal) for daily use; `datasette telemetry.db` for monthly deep-dives.

*Retention:* Keep raw events 90 days; roll up to daily `snapshots` indefinitely (snapshots are tiny). A single scheduled `DELETE FROM events WHERE ts < date('now','-90 days')` in a maintenance check is enough. No log rotation infrastructure needed.

*Staying under ~200 lines of glue:*
- ~40 lines: `emit_event()` helper (structlog → SQLite/JSONL) + WAL pragmas.
- ~30 lines: audit-registry and hook wrappers (one call each).
- ~40 lines: git-history/backlog parser for task-flow (derived, not logged live).
- ~60 lines: `dispatch report` (rich + plotext).
- Everything else (dep scan, coverage, mutation) is *existing tools* whose one-line summaries you append — no new code.

**What NOT to build in v1:**
- No web dashboard server (Streamlit/Grafana) — Datasette on demand suffices.
- No OpenTelemetry/tracing, no spans, no collector.
- No anonymization/consent/network shipping — it's local and single-user.
- No real-time alerting or thresholds — this is a review tool, not a pager.
- No custom time-series DB — SQLite is the time-series DB here.
- No per-line/verbose event firehose — log named organ fires, not every function call.

### Comparison table — tool options

| Option | Role | Fit for solo local | Maintenance cost | Windows / uv notes | Verdict |
|---|---|---|---|---|---|
| **SQLite (WAL) event store** | Storage | Excellent — SQL + concurrency | Near-zero (stdlib `sqlite3`) | Native; WAL is single-host only | **Adopt (v1 core)** |
| **JSONL append** | Transport from shell hooks | Good for zero-dep hooks | Near-zero | Native; git-bash friendly | **Adopt for lowest-level hooks** |
| **structlog** | Event emit helper | Excellent — structured events | Low; one dep via uv | Pure-Python, native | **Adopt** |
| loguru | Event emit helper | Good (zero-config) | Low | Native | Alternative to structlog |
| stdlib `logging` + `python-json-logger` | Event emit helper | Adequate | Lowest deps | Native | Fallback |
| **rich + plotext** | In-terminal report | Excellent — CLI-native | Low; two deps via uv | Native; rich integration official | **Adopt (primary read surface)** |
| **Datasette** | Ad-hoc web/JSON explorer | Excellent on demand | Low; run when needed | Pure-Python, native; `uvx datasette` | **Adopt (secondary)** |
| Streamlit | Interactive dashboard | Overkill for v1 | Medium (standing process, full reruns) | Native | Defer — conscious exception only |
| **deptry** | Dead-dependency scan | Excellent | Low; dev dep via `uv add --dev` | `win_amd64`/`win-64` wheels; supports uv | **Adopt (derived signal)** |
| **coverage.py** | Code-path usage evidence | Good (candidate signal) | Low; via pytest-cov | Native | **Adopt (derived, with caveat)** |
| import-linter | Architecture contracts | Optional | Low; via uv | Native (Windows fixes in changelog) | Adopt only for module boundaries |
| OpenTelemetry (+ Collector/Jaeger) | Distributed tracing | Poor — no service boundaries | High (collector/Docker; file exporter alpha) | Docker needed for Jaeger | **Do not adopt** |
| Prometheus + Grafana | Metrics scrape + dashboards | Poor — needs scrape target + TSDB + UI | High (3 standing services) | Runs but pointless locally | **Do not adopt** |
| Zabbix | Fleet monitoring | Poor — server+DB+PHP frontend+agents | Very high | **Server/frontend not native on Windows; agent only** | **Do not adopt** |
| Splunk | Enterprise log analytics | Poor — enterprise scale | Very high; volume licensing | Runs but grossly oversized | **Do not adopt** |

## Recommendations

**Stage 1 (week 1): instrument the two irreplaceable signals.** Add `emit_event()` (structlog + SQLite WAL) and wire `check_run`, `hook_run`, and `blocker_fired`. These are the events you cannot reconstruct later. Ship nothing else yet. *Benchmark to proceed:* two weeks of clean event data with a stable `name` taxonomy.

**Stage 2 (week 2–3): add the cheap derived signals.** Append `dep_scan` (deptry `DEP002` count + coverage %), `test_run` duration, and `mutation_run` score after their respective runs. Add the git-history task-flow parser as a read-time computation. *Benchmark:* you can answer "which check never blocks?" and "which dependency is dead?" from one `dispatch report`.

**Stage 3 (month 2): add read surfaces and the first methodology decisions.** Build `dispatch report` (rich + plotext); install Datasette for ad-hoc queries. Then run the first governance review: retire any organ with fires>0/blocks=0 over 30 days (after judgment, per Homebrew's caveat), prune any `DEP002` dependency, and promote any hook with a meaningful catch rate. *Benchmark:* at least one organ retired and one dependency pruned on evidence.

**Thresholds that would change these recommendations:**
- *If you add real external users or a deployed service* → revisit OpenTelemetry (now traces have meaning) and structured remote logging.
- *If agent lanes grow into many concurrent long-running processes with parent/child work* → OTel spans become justifiable; SQLite WAL still handles the writes.
- *If the event log exceeds millions of rows or query latency degrades* → add indexes on `(event_type, ts)`; only then consider a purpose-built TSDB (still not Splunk/Zabbix).
- *If you ever want an always-on visual dashboard* → Streamlit or Grafana-with-SQLite, but only as a conscious "features for features" exception.

## Caveats
- **Coverage ≠ usage.** `coverage.py` measures code executed *under tests*; a 0%-covered function may still be used in real runs, or may be genuinely dead. Use it as a *candidate* signal, corroborated by `deptry` (for deps) and by the live event log (for organs).
- **`deptry` false positives** exist for side-effect imports, plugin/entry-point loading, and optional-dependency patterns; always review `DEP002` before removing, and use `# deptry: ignore`.
- **Git timestamps are commit time, not work time**, so task cycle-time and DORA-style metrics are approximations of cadence, not audited durations.
- **Mutation score is noisy** due to equivalent mutants inflating "survived"; trend it, don't gate on it.
- **Solo-scale statistics are thin.** A check that fired twice tells you little; give signals weeks before acting, and honor Homebrew's warning that low usage alone doesn't prove an organ is safe to remove — combine telemetry with judgment.
- **Version/status notes (as of 2026):** deptry 0.25.1 (published Mar 18, 2026; Python ≥3.10; Windows wheels) — some sources indicate the project moved to an `osprey-oss` GitHub org while others still show `fpgmaas/deptry`, so confirm the canonical repo before pinning a source URL; coverage.py 7.15.x; import-linter 2.12 (Jun 23, 2026); mutmut requires fork support — **this is a Windows caveat**: mutmut historically relies on `os.fork`, which is unavailable on native Windows, so mutation runs may need WSL/git-bash-with-fork or a Linux CI path. Verify mutmut's current Windows support before assuming `mutation_run` events will emit natively on Windows 11.
- **OTel file exporter is alpha** for traces/metrics/logs — another reason it's unsuitable for a dependable v1.
- **SQLite WAL is single-host only** — per the official docs it "does not work over a network filesystem," so keep `telemetry.db` on local disk, not a synced/network drive.
