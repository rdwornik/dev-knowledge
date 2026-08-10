# Research-corpus distillate — the 48 proposals of the six 2026-08-09 memos, triaged against measured repo state

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-10
- **Source-session:** batch lane A, worktree `ingest-research-corpus`, branch `worktree-ingest-research-corpus`; base HEAD `12ef9c91`; corpus landed this lane at `f571ac3c`
- **Status:** PROPOSAL-ONLY — this artifact decides nothing. It is the instrument the plan-v3 Phase-3 ratification batch rules from.
- **Model:** opus (effort high), unattended background lane

## Executive so-what

The six memos carry **59 distinct proposals** (rows R01–R59; R60 is a cross-cutting numbers row, not a proposal). Triaged against live repo state:

- **27 rows carry something in `LANDED-ALREADY`.** Seven are landed outright with nothing left to ratify (R10, R30, R32, R35, R38, R39, R58); the rest are partial or pattern-landed — the mechanism's shape already runs here, applied to a different surface.
- **12 declines on measured repo grounds** — 8 in the table (R09, R16, R23, R27, R38, R42, R49, R53) plus 4 the memos make about themselves (§3). In each case either the memo declines its own premise on this fleet's numbers, or a landed ruling already refuses the mechanism.
- **7 rows rest on a claim that is false, stale, or mis-cited about this repo** (R05, R24, R41, R44, R45, R55, R60 — nine distinct claims, since R60 carries three). Among them: two "your model is missing X" findings where X is present and ruled, and one enforcement mechanism that **cannot exist** on this repo's GitHub tier.
- **The remainder are genuine open decisions** — roughly 40 rows, of which the partial-landed ones are the cheapest because their pattern already exists here. Exactly one *half of a commission* is un-owned by any intake: the **session-continuity half of memo SC** (§4.7).

**The single highest-value un-landed artifact is the seeded-defect corpus** (row R29, memo TM). It gates `[#491]`, `[#492]` and any Copilot lane by ruled precedent, and it is the only proposal in the batch that another already-ruled decision explicitly waits on: `#29` Fold A ruled that **"no bake-off runs before the seeded-defect corpus exists."** Its full extracted spec is §4.

**Two verdicts the batch should read before anything else.** (1) The memos' most confident structural criticism — that this repo lacks a Proposed ADR state and a durable rejected/parked intake home — is **false in both halves**, with locators (R45, R44). (2) The compute memo's own headline is a **refusal of its own premise**, already filed as intake `#32`; the batch should ratify the *rule* it carries (fail-closed attestation, R55) and not the spend.

## 1. The table

Columns are exactly as the lane contract specifies. Cells are terse by design; every non-obvious cell is expanded in §2, keyed by row id. `—` means "nothing to record in this column", never "not checked".

Memo codes: **CS** `wf-8a83eb70` code-style · **GR** `wf-f6851745` dependency/ontology graph · **TM** `wf-02c940ef` telemetry & model comparison · **PT** `wf-d68b2f7f` multi-provider portability · **SC** `wf-fafd931b` session continuity & decision lifecycle · **CP** `wf-1dc18e42` compute placement. All six are at `docs/archive/2026-08-09-research-*.md`.

| # | proposal | source memo | mechanism-or-taste | cost | owning intake | precondition | conflict flag | LANDED-ALREADY (locator) | declined-on-measured-repo-grounds | false-about-this-repo |
|---|---|---|---|---|---|---|---|---|---|---|
| R01 | "Functional core, imperative shell" as the one written paradigm doctrine | CS | TASTE | S | #31 | none | — | — | — | — |
| R02 | Ousterhout as source-of-truth; do NOT gate Clean Code's short-function rule | CS | TASTE | S | #31 | R01 | — | — | — | — |
| R03 | ruff complexity/size families `C901` `PLR0912` `PLR0913` `PLR0915` `PLR1702` | CS | MECH | S | #31 | baseline run (R15) | — | partial — ruff is the live lint gate, `.pre-commit-config.yaml` ruff @ v0.15.5 + `pyproject.toml [tool.ruff] required-version >=0.15.5`; the complexity families are NOT enabled | — | — |
| R04 | One type checker fleet-wide + baseline ratchet | CS | MECH | M | #31 | tool choice | — | — | — | — |
| R05 | import-linter contracts (layers/forbidden/independence) | CS | MECH | M | #31 | adopt grimp+import-linter as deps | R24 | — | — | see R24 — the dep does not exist here |
| R06 | Count ratchets extended to complexity + type debt (mypy-baseline, diff-cover) | CS | MECH | S | #31 | R03, R04 | — | pattern landed — `scripts/silent_rule_detector.py` + the `silent_rule_ratchet` audit check, live budget 440 ≤ 441 (`CLAUDE.md` §12 v2.55) | — | — |
| R07 | Published canonical config package (`devkit`), pinned per repo | CS | MECH | M | #31 | R03/R04 settled | — | — | — | — |
| R08 | copier/cruft template propagation + `sync-with-uv` for hook-version drift | CS | MECH | M | #31 | R07 | — | partial — the carrier/manifest model already propagates (`deploy/manifest-v*.yaml`, floor-hash guard); copier is not adopted | — | — |
| R09 | PostToolUse lint hook running the quality gate on every edit | CS | MECH | S–M | #31 | — | **R26** | — | **YES** — N3-22 anti-goal, carried into `#29` Fold A: no PostToolUse hook (fires on every tool call, sits on the operator's latency path) | — |
| R10 | PreToolUse guard enforcing "zero invented paths" | CS | MECH | S–M | #31 | none | — | **YES** — `scripts/validate_hermetization.py` (ADR-101 §3 Rule A), `scripts/hooks/block_immutable_edits.py` (ADR-77), `~/.claude/hooks/block-onedrive.ps1` (core-invariant #1) | — | — |
| R11 | Prompt pre-dispatch checker — refuse a contract lacking module target / size budget / governance path | CS | MECH | M | #31 | measured-divergence justification (hand-rolled, no OSS equivalent) | — | — | — | — |
| R12 | semgrep "don't hand-roll X" rules as mechanical LIBRARY-FIRST | CS | MECH | S–M | #31 | rule authoring | — | — | — | — |
| R13 | deptry for dependency drift (unused/missing/transitive/misplaced) | CS | MECH | S | #31 | none | — | — | — | — |
| R14 | jscpd duplication threshold | CS | MECH | S–M | #31 | none | — | — | — | — |
| R15 | Churn×complexity hotspot analysis BEFORE any refactor; strangler-fig / opportunistic over big-bang | CS | MECH+TASTE | S | #31 | none | — | — | — | — |
| R16 | Fleet aggregation via committed per-repo JSON, not SonarQube | CS | MECH | M | #31 | R15 | — | — | **YES** (SonarQube leg) — single-branch Community + JVM server violates the no-server rule at n=6 repos | — |
| R17 | Committed `nodes.jsonl` + `edges.jsonl` sorted by stable id, with a `--check` regen gate | GR | MECH | S | #29-B | schema fixed (GR Stage 0) | — | pattern landed — six regen-and-diff gates already run this shape (`roster-freshness`, `claude-rosters-freshness`, `audit-index-freshness`, `intake-index-freshness`, `codemap-freshness`, `toc-freshness-playbook`) | — | — |
| R18 | One emitter per existing mechanism, all writing typed edges into the one log | GR | MECH | S | #29-B | R17 | — | the *producers* all exist (`validate_reconciliation.py`, `validate_doc_claims.py`, `ecosystem/parity-surfaces.yaml`, ADR-101 tokens, serialize-groups); none emits edges | — | — |
| R19 | Query layer: DuckDB recursive CTEs or stdlib SQLite + a `graph query` CLI | GR | MECH | S | #29-B | R17 | storage choice **OPEN, not ruled** | — | — | — |
| R20 | Close task↔file: derive from git trailers + backfill `footprint:` + a hook requiring it | GR | MECH+curation | M | #29-B | R17 | — | ruled as a **landing predicate on new/touched rows, never a backfill migration** (`#29` Fold B) | — | denominator stale — see R60 |
| R21 | Local stdio MCP wrapper over the same query functions | GR | MECH | M | #29-B | R19 | — | — | — | — |
| R22 | Orphan/dangling-link check per curated edge type | GR | MECH | S–M | #29-B | R18 | — | template landed — `scripts/validate_reconciliation.py`; `#29` Fold B already names it the template | — | — |
| R23 | Avoid Kùzu (archived 2025-10-10) and Neo4j (server) | GR | TASTE | — | #29-B | none | — | — | **YES** — upstream read-only / no-server rule | — |
| R24 | grimp as the durable import-graph backbone | GR | MECH | S | #29-B | **adopt the dependency** | R05 | — | — | **YES** — "already the engine behind your import-linter usage" is false: neither `grimp` nor `import-linter` appears in `pyproject.toml`, `.pre-commit-config.yaml` or `uv.lock`. Re-verified live 2026-08-10 (zero hits) |
| R25 | `ccusage --json --offline` extraction as the first move | TM | MECH | S | #29-A | none | — | — | — | — |
| R26 | `SessionEnd` hook → committed `telemetry/sessions.jsonl`, OTel-GenAI-aligned | TM | MECH | S→M | #29-A | none | **R09** | — | — | — |
| R27 | OTel `console`/`prometheus` locally, then a local `duckdb-otlp` collector | TM | MECH | S→M | #29-A | R26 | — | — | **YES** (collector leg) — "extraction, not plumbing" is the ruled first move (`#29` Fold A); a collector is an always-running server | — |
| R28 | Extend parsers to Codex/Gemini/Grok; record Copilot premium-requests as a raw unit | TM | MECH | M | #29-A | R26 | — | — | — | — |
| **R29** | **Seeded-defect corpus (40→80, stratified, private, history-sanitized) + paired bake-off runner** | TM | MECH | L | #29-A | R26 for cost/time axes | — | **named, not built** — `[#492]` carries a lane-scoped precursor defect list (vacuous test · fail-open except · stale locator · fence corruption); the corpus artifact does not exist | — | — |
| R30 | Defensible-metric set; LOC / commit-count / self-reported speed banned | TM | MECH+TASTE | S | #29-A | R26 | — | **YES** — the ban and its DORA/SPACE basis are carried verbatim in `#29` Fold A | — | — |
| R31 | PreToolUse `.env`-block hook + pre-commit secret-scan over the telemetry file | TM | MECH | S | #29-A | R26 | — | partial — the PreToolUse guard family exists (R10); no `.env` block, no secret-scan | — | — |
| R32 | Record raw provider unit + a separately computed estimate; never sum subscription with API-billed | TM | TASTE(rule) | S | #29-A | R28 | — | **YES** — carried verbatim in `#29` Fold A | — | — |
| R33 | Canonical `AGENTS.md` + thin `CLAUDE.md` carrying `@AGENTS.md` | PT | MECH | S | #25 W-9(a) | W-9 ratification | R41, R59 | — | — | — |
| R34 | Point Gemini at AGENTS.md via `.gemini/settings.json` `context.fileName` | PT | MECH | S | #25 W-9(a) | R33 | — | — | — | — |
| R35 | Generation + version-stamp drift guard (`hashlib` + pre-commit), not a bare checksum | PT | MECH | M | #25 W-9(a) | R33 | — | **YES** — the floor-hash guard is this exact shape: `.claude/CLAUDE-FLOOR.md` + sha256 sidecar, `scripts/check_floor_hash.py`, `floor-hash-verify` pre-commit hook (ADR-78/93) | — | — |
| R36 | Canonicalize MCP: one `servers.yaml` → N provider formats | PT | MECH | M | #25 W-10 | R33 | — | — | — | — |
| R37 | Keep frozen-contract enforcement in provider-agnostic gates, never tool hooks | PT | TASTE(placement) | — | #25 W-10 | none | — | partial — the 17 client-side gates are pre-commit/commit-msg/pre-push (provider-agnostic); the `Stop`/`SessionStart`/`PreToolUse` organs are Claude-specific by construction | — | — |
| R38 | Reject symlinks as the canonical-file mechanism | PT | MECH | — | #25 W-9(a) | none | — | **YES** — re-confirmed, not re-opened, in the `#25` scope note 2026-08-09 | **YES** — degrade to text stubs under `core.symlinks=false` on this Windows/git-bash fleet | — |
| R39 | Hard rule: provider swaps use API keys only, never subscription OAuth | PT | TASTE(rule) | S | #25 W-10 | none | — | **YES** — carried in the `#25` scope note | — | — |
| R40 | Demonstrate one swap end-to-end (Codex CLI native, or Kimi via base-URL) | PT | MECH(test) | S–M | #25 W-10 | R33 | — | — | — | — |
| R41 | Keep AGENTS.md under ~150 lines (ETH Zurich 20%+ token cost) | PT | TASTE | S | #25 W-9(a) | R33 | **R33** | — | — | claim recorded but **NOT adopted** by the `#25` scope note — external, unreplicated here; flagged as a live W-9 ratification question |
| R42 | Do not flatten to a lowest-common-denominator methodology | PT | TASTE | — | #25 W-10 | none | — | — | **YES** — would amputate the Claude-specific organ mesh that is this repo's enforcement layer | — |
| R43 | Plan-carrying residual: planned vs landed vs remains+why, re-derived from git at CUT | SC | MECH | M | **NONE** (§4.7) | none | — | — | — | — |
| R44 | Intake WIP cap + a Parked state | SC | MECH | S | **NONE** (§4.7) | none | — | add-side backpressure landed — `scripts/check_backlog_filing.py` + the `backlog-filing-backpressure` commit-msg hook (`kill-candidates:` required on every new task id) | — | **YES** — "Missing state 2 — a durable Rejected/Parked intake home" is false: `docs/intake/README.md` §5 ruled enum carries `REJECTED (reason, kept) [terminal → archive/]` **and** `disposition: deferred` = "parked but alive (requires `trigger:` or `review-date:`)". Ruled 2026-07-19, deployed by `[#398]` 2026-07-23 |
| R45 | ADR review/sunset dates + a Proposed state | SC | MECH | S | **NONE** (§4.7) | none | — | Proposed state landed — `docs/decisions/ADR-111-finding-triage-pipeline.md` line 3 is `Status: Proposed`; ADR-94 codifies the in-place Proposed→Accepted status-line edit (`CLAUDE.md` §5 item 3). Live tally 2026-08-10: 70 Accepted, 1 Proposed | — | **YES** — "Your ADRs jump straight to immutable-accepted" is false (locator above). The `review_date` half is genuinely un-landed for ADRs; the grammar precedent exists at ADR-105 (`review_date=<YYYY-MM-DD>`) and ADR-102 §4 **deliberately declines** a `review_date` time-box with a stated reason |
| R46 | Audit-finding → backlog forcing function (a row id, or an explicit no-action + reason) | SC | MECH | S | **NONE** (§4.7) | none | — | **YES** — ADR-111 (Proposed, 2026-08-09) §1 triages every finding into exactly one of OWNED · DISCHARGED · CANDIDATE · REJECTED, and makes the DISCHARGED locator mandatory. Status is Proposed, not Accepted — ruled, not yet ratified | — | — |
| R47 | ADR-landing predicates — each accepted ADR maps to ≥1 fitness function | SC | MECH | M | **#30 §A** | register shape chosen | — | — | — | — |
| R48 | Conftest policy-as-code (single local binary, not OPA-the-server) | SC | MECH | M | **NONE** (§4.7) | R47 | — | — | — | — |
| R49 | Label-only aging; no backlog bankruptcy, no auto-close stale-bot | SC | TASTE | — | **NONE** (§4.7) | none | — | aligned already — ADR-65 retire-not-delete; a closed row keeps its task file with a terminal `status:` | **YES** — both are contested in the memo's own words and neither fixes birth rate | — |
| R50 | Drop the boot-time table of passes; exceptions-only | SC | TASTE | S | **NONE** (§4.7) | R51 | — | — | — | — |
| R51 | Verification-at-cut, exceptions-only boot; keep the probe-gated answer-withheld bundle | SC | MECH+TASTE | M | **NONE** (§4.7) | none | — | **YES** (verification-at-cut leg) — HANDOFF_PROCESS v6 §5 + `/handoff-verify`: one CC-side run of the whole live gate, one evidence block. The exceptions-only *trim* is not landed and is `[#511]`'s live fork | — | — |
| R52 | Stage 0 local fixes, $0: rglob skip-list defect · WSL2 native FS · Defender exclusions · Pylance scoping · `feature.manyFiles` · `.wslconfig` caps | CP | MECH | S | #32 | none | — | partial — Pylance scoping landed at **user-settings level** 2026-08-09 (`#30` §C: excludes for `.claude/worktrees/`, venvs, mutants, caches; `openFilesOnly`). The other five are open | — | — |
| R53 | One CLI-provisioned Linux VPS (Hetzner CX42 ≈ $18/mo) as agent/test host | CP | INFRA | M | #32 | **R52 first** | — | — | **YES** — the memo declines its own premise on this repo's numbers: wait-bound at ~14.6% CPU, ~24% of the worktree penalty is a fixable rglob defect. "Buying compute now would paper over a bug." `#32` is filed with that refusal as its headline | — |
| R54 | Toolchain parity: `uv sync --locked` · `mise.lock locked=true` · `sync-with-uv` · image built from lockfiles | CP | MECH | M | #32 | none | — | partial — `uv.lock` + `.python-version` are committed and ADR-106 pins the interpreter (ADR-101 amendment 2026-07-27); `mise.lock` and `sync-with-uv` are not adopted | — | — |
| **R55** | **Fail-closed "gates-ran" attestation — a run that cannot prove its gates executed is untrusted, not green** | CP | MECH | M | #32 | R54 | — | report-only precursor landed — `.github/workflows/report-only-wall.yml` records suite / `audit.py health` / anchor outcomes per SHA on main (ADR-101 amendment 2026-08-06); coverage gap is `[#507]` (3 of 17 gates re-run) | — | **YES** (the enforcement leg) — the memo prescribes "a layer the agent cannot skip (server-side gate / CI required-check)" and a pre-receive hook. Neither exists or can: ADR-101 amendment 2026-08-06 records the repo is **private on the Free tier, "where required checks are unavailable — no branch protection is touched and none can be"**, and the recorder is report-only **permanently**, not pending promotion |
| R56 | Push suite / gate mesh / mutation testing to GitHub Actions | CP | MECH | M | #32 | R54 | — | partial — the wall exists (R55); mutation testing is `[#502]`, **BLOCKED ON `[#501]`** | — | — |
| R57 | Cap concurrent mutating lanes to what the serial merge gate absorbs | CP | TASTE(rule) | S | #32 | none | — | aligned — the serial merge gate is doctrine; `#30` §C names batch-width cost as an unbudgeted class | — | — |
| R58 | Do-NOT-move-remote list: architect seat · serial merge gate · bundle cut · secrets · gate-bearing work without parity | CP | TASTE(rule) | — | #32 | none | — | **YES** — carried unchallenged into `#32` non-goals | — | — |
| R59 | Control loop: Tailscale + tmux + mosh + ntfy for remote observation | CP | INFRA | S | #32 | R53 | — | — | — | — |
| R60 | *(cross-cutting)* the corpus's own repo-state numbers | GR, SC, CP | — | — | — | re-measure at ratification | — | — | — | **YES, three counts** — see §2 R60 |

**Consumed-correctly proof (F25-2).** Both proof columns are non-empty: **8 rows** carry `declined-on-measured-repo-grounds` (R09, R16, R23, R27, R38, R42, R49, R53 — plus the four self-declines in §3, for 12 declines total) and **7 rows** carry `false-about-this-repo` (R05, R24, R41, R44, R45, R55, R60 — nine distinct claims, R60 carrying three). The table is not a summary of the memos; it is the memos *consumed*, and it records where they were wrong about the repo that commissioned them.

## 2. Row notes (only where the cell needed evidence)

**R03.** ruff is live as a gate, but as a *lint* gate. `.pre-commit-config.yaml` pins `astral-sh/ruff-pre-commit` @ v0.15.5 in gate mode; `pyproject.toml [tool.ruff]` carries `required-version >=0.15.5`. No complexity family is enabled, so the memo's structural ceiling — the one enforceable slice of its paradigm doctrine — is not in force. Enabling it is a real decision, not a config tweak: it interacts with R06's ratchet baseline.

**R09 / R26 — the one hard conflict inside the batch.** CS recommends a PostToolUse hook running the quality gate after every `Edit|Write|MultiEdit`, calling it the mechanism that converts doctrine from request to guarantee. TM's own fold into `#29` Fold A carries the opposite as a *landed anti-goal* (N3-22): **no PostToolUse hook** — it fires on every tool call, sits on the operator's latency path, and re-records data already on disk; one `SessionEnd` hook, fail-soft, **not** `Stop`. Two memos in the same batch, opposite verdicts on the same organ. The repo's ruling already picked TM's side. If the batch wants CS's per-edit feedback loop it must overturn a landed anti-goal explicitly, not adopt R09 quietly.

**R24 — the false claim, re-verified this lane.** GR's recommendation section states grimp is "already the engine behind your import-linter usage". `#29` Fold B recorded this as false on 2026-08-09. Re-verified live 2026-08-10 on this branch: `grep -rn "grimp|import-linter|import_linter" pyproject.toml .pre-commit-config.yaml uv.lock` returns **zero hits**. The consequence is not cosmetic — grimp is GR's *cheapest* proposed edge source (cost S) and CS's recommended layering tool (R05), and in this repo it is an **unadopted dependency**. Both rows inherit that cost.

**R29 — see §4** for the extracted spec. Note the standing coupling: `#29` Fold A ruled that **no bake-off runs before this corpus exists**, and that the 2026-07-31 single-diff A/B is "precedent for METHOD, not an admission instrument". `[#502]` (mutmut 3.7.0) is the nearest live row and is **BLOCKED ON `[#501]`** — mutmut needs `fork()`, Windows needs WSL, WSL is out by operator constraint, so it is CI-only. That makes R29 and R56 the same dependency chain, not two independent items.

**R44 / R45 — the memo's central structural criticism, false in both halves.** SC's Q5 concludes the decision lifecycle has "an explicit rejection state your model is missing" and lists two missing states. Both are present:

- *Missing state 1 (a Proposed/Provisional ADR):* `docs/decisions/ADR-111-finding-triage-pipeline.md` line 3 reads `- **Status:** Proposed`. ADR-94 codifies the in-place status-line edit on ratification, which is exactly the Proposed→Accepted transition SC asks for. Live tally 2026-08-10 across `docs/decisions/ADR-*.md`: **70 Accepted, 1 Proposed**.
- *Missing state 2 (a durable Rejected/Parked intake home):* `docs/intake/README.md` §5 carries the ruled enum with `REJECTED (reason, kept) [terminal → archive/]` — "rejections are knowledge, not garbage" — and `ACCEPTED` + `disposition: deferred` = "parked but alive (requires `trigger:` or `review-date:` — the un-park condition is part of the record, not tribal memory)". Ruled 2026-07-19, deployed by `[#398]` 2026-07-23, replacing an earlier enum.

**What survives of SC's finding, honestly:** the states exist; the *ratio* is what SC is really pointing at. One Proposed ADR in 71 means the state is barely exercised, and SC's `review_date` proposal for ADRs is genuinely un-landed. But "missing" is the wrong word, and a ratification batch acting on "we lack a rejection home" would build a second one. Note also that ADR-102 §4 **deliberately declines** a `review_date` time-box for its own subject, with a stated reason (self-invalidating git predicates) — so R45's ADR-wide `review_date` is not a free add; it argues against a live ruling.

**R46.** SC lists the audit-finding forcing function as adoption #5. ADR-111 (Proposed, 2026-08-09 — one day before the memos were read) already rules it: every finding is triaged into exactly one of four outcomes, and **the DISCHARGED locator is mandatory and must resolve — "we already do that" without a locator is not a discharge.** This distillate is itself an instance of that pipeline; the `LANDED-ALREADY (locator)` column *is* ADR-111's DISCHARGED outcome, and the two proof columns are its REJECTED outcome. Recorded because it means R46 needs a *ratification* decision on ADR-111, not an adoption decision on SC.

**R51.** HANDOFF_PROCESS v6 §5 + `/handoff-verify` already run the whole live probe gate in one pass and emit one evidence block — the receiver re-derives rather than accepts, which is SC's I-PASS "synthesis by receiver" mapped onto this repo. What is *not* landed is SC's trim: moving probe *execution* to cut and delivering only exceptions at boot. That is `[#511]`'s live fork (cut FILL-IN count vs probe count vs verify pass), and R50 is the same decision seen from the other end. The batch should rule R50/R51 together with `[#511]` or not at all.

**R55 — the mechanism that cannot exist here as specified.** CP's Q6 is the memo's one genuine rule and `#32` was filed to get it ratified. But CP prescribes enforcement "at a layer the agent cannot skip (server-side gate / CI required-check)" plus a server-side pre-receive hook, and correctly notes pre-commit hooks are trivially bypassed by `--no-verify` / `SKIP=`. On this repo that layer is **unavailable, by a recorded ruling**: ADR-101's 2026-08-06 amendment states the recorder is "REPORT-ONLY **permanently**, not pending promotion: the repo is private on the Free tier, where required checks are unavailable — no branch protection is touched and none can be." So the attestation *rule* can ratify (it binds the cloud lanes today, which is `#32`'s open question 1), but its prescribed *teeth* cannot be built without changing tier or host. The honest form of R55 here is: receipts + a client-side integrity check + the report-only wall as the after-the-fact record — which is strictly weaker than what CP specifies, and the batch should ratify it knowing that.

**R60 — three stale or mis-cited numbers in the corpus, all cheap to correct.**

1. **`footprint:` denominator (GR, TL;DR).** GR says "164 of 169 open rows lack `footprint:`". Numerator is right and still right: **5** rows carry `footprint:`. Denominator is two windows stale — `#29` Fold B measured 168 on 2026-08-09; live count on this branch 2026-08-10 is **196 open rows**. So the live figure is **5 of 196 (2.6%)**, not 3.0%. The gap GR calls highest-leverage is *widening*, which strengthens R20 rather than weakening it.
2. **Open-row count (SC, Q6).** SC reasons from "~161 open rows, ~73% born in the last 30 days" to its WIP-cap conclusion. Live: **196**. ADR-111's own context cites 194. SC's conclusion is unaffected — a larger number argues its case harder — but the batch should not quote 161.
3. **xdist attribution (CP, Key Finding 1 — repeated verbatim into `#32`).** Both state "pytest-xdist already took the suite 1785.6s → ~539s", and `#32` attributes it to **STANDING_RULINGS E1**. E1 does not carry that number: it records the adoption on "serial 1785.61s vs `-n auto` 358.77s / 330.15s", commit `d11dda35`. The 539s figure is real but sourced elsewhere — `docs/audits/2026-08-08-technical-batch-3-packet.md` line 46 (`539.12s`), surfaced as X-3 and already flagged as "an observed divergence" in `docs/audits/2026-08-09-technical-challenge-retrieval.md` around line 452. **This is a mis-citation, not a wrong measurement**, and it now sits inside a filed intake. It is reported here, not fixed — the lane contract forbids intake edits.

Also verified accurate, so the batch can rely on them: the memos' "41 checks" figure matches **41** `check_`/`verify_`/`validate_` function definitions in `scripts/audit.py`, and the `silent_rule_ratchet` / `validate_reconciliation` / `validate_doc_claims` / floor-hash organs the memos point at all exist at the paths cited above.

## 3. The four additional declines, recorded so they are not re-litigated

These are declines the memos make about *themselves* on this repo's constraints. They carry no row because there is nothing to ratify — only something not to re-open.

- **Log4brains** for ADR lifecycle — declined by SC's own library-first flag: Node/Next.js bring-in for a static site the repo does not need. `pyadr` or plain frontmatter first.
- **sphinx-needs / Doorstop / StrictDoc as the store** — declined by GR: each imposes Sphinx or its own DSL, while this repo's YAML frontmatter already *is* the node/edge source. Copy the schema, not the tool.
- **Google Colab** — declined by CP as "wrong shape": ephemeral filesystem, no persistent git-worktree/CLI-agent model. "Do not build fleet workflow on Colab."
- **`returns` / `toolz`** for FP patterns — LIBRARY-FIRST compliant but push a non-idiomatic style LLM agents may not reproduce; CS gates them behind a measured-divergence justification.

## 4. The seeded-defect corpus spec, extracted (memo TM, Q5–Q6 + Stage 3)

This is the highest-value un-landed artifact in the corpus. It is extracted here in full because it gates `[#491]` (Gemini scanning lane), `[#492]` (Grok review-lane acceptance), any Copilot lane, and `[#502]` (mutmut) — and because `#29` Fold A ruled that **no bake-off runs before it exists**. Nothing below is authored by this lane; it is TM's spec, reorganised into buildable form with this repo's couplings named.

### 4.1 Why an internal corpus and not a public benchmark

Public benchmarks are contaminated, with numbers: SWE-Bench+ (arXiv:2410.06992) found **32.67% of "successful" patches involved solution leakage** and **31.08% passed on weak tests**; filtering both dropped SWE-Agent+GPT-4 from **12.47% to 3.97%**. The "SWE-Bench Illusion" work showed models recall buggy file paths up to **76%** from issue text alone. OpenAI **stopped reporting SWE-bench Verified on 2026-02-23** citing contamination. Even SWE-bench Pro containers leaked future git history recoverable via `git log`/`git show`.

Consequence for the build: the corpus must be **private and never published**, use **this fleet's own repos and gate mesh**, have **robust** hidden tests (not vacuous ones), have **git history sanitized** so the fix is not reachable, and be **regenerated/rotated** over time.

### 4.2 Generation — a blend, not one source

- **Mutation tools as defect generators:** `mutmut` v3+ (libcst-based, actively maintained), `cosmic-ray` v8.x, `mutatest`, MutPy, Poodle. Use **more than one operator set** — comparative studies show they differ in operator coverage and mutant difficulty. Cheap, large, stratifiable volume; many mutants are trivial or equivalent. **Repo coupling:** `mutmut` requires `fork()`, so Windows requires WSL, which is out by operator constraint — this is exactly why `[#502]` is ruled **CI-only and BLOCKED ON `[#501]`**. The corpus build inherits that host constraint.
- **Hand-authored realistic defects** — necessary for classes mutation cannot express, and these are named as *this fleet's real failure modes*: **vacuous test** (asserts nothing) · **fail-open exception handler** (`except: pass`) · **stale locator/selector** · **corrupted fence/format** (broken JSONL or markdown) · silent type coercions. **Repo coupling:** `[#492]` already names the first four verbatim as its lane-acceptance defect list — so a hand-authored core already has an agreed class vocabulary.
- **Mining real historical bug-fix commits** — highest ecological validity, but the **SZZ algorithm is known-inaccurate** (refactoring and cosmetic edits corrupt bug-inducing-commit attribution). Use **Defects4J** (357 real Java bugs / 5 projects) and **BugsInPy** (493 real bugs / 17 Python programs, ~831 man-hours to build) as **structural templates only** — Defects4J bugs are ≤2020 and likely in training data; do not reuse verbatim. Prefer GitBug-style recent reproducible packaging.

### 4.3 Size, classification, stratification

- **40–80 defects minimum** for a usable signal under paired design with bootstrap CIs. Start at **~40** to get moving, grow to **80+** as variance demands. (Agent benchmarks operate at 40–113 tasks; Claw-SWE-Bench's "Lite-80" argues 80 preserves the ranking/cost structure of a 350-set.)
- Tag every defect with: `defect_class` (vacuous-test · fail-open · stale-locator · corrupted-fence · off-by-one · wrong-boundary · dropped-error-path · …) · `difficulty` · `repo` · `subsystem` · **`detectable-by`** (which gate or test *should* catch it).
- Stratify so **no class dominates**, and report **per-class** detection.

### 4.4 Context-leakage prevention (the property that makes it an admission gate)

- Store in a **separate private repo or an encrypted/`.gitignore`d path the agent's tools cannot read**.
- Inject defects into a **throwaway worktree at eval time**.
- **Sanitize git history** — prune the fix commit so `git log`/`git show` cannot recover the answer.
- **Never** put defect descriptions in `CLAUDE.md`, prompts, or any committed artifact the agent sees.

*Repo coupling, flagged:* this constraint is in direct tension with this repo's committed-artifact discipline — the corpus is the one artifact that must **not** be readable from the tree the agent works in. That is a genuine placement decision for the batch, not a detail (see §4.7).

### 4.5 Scoring — four axes, and the admission rule

Score each defect on: **detection rate** (did the agent find it) · **fix correctness** (does the *robust hidden* test pass — not a weak one) · **false-positive rate** (did it "fix" non-defects or introduce regressions) · **cost & time per defect** (tokens, USD estimate, wall-clock). Report **per-class** and as **distributions with CIs**.

**Admission rule (verbatim intent):** a new model lane is admitted **only if** its paired detection + fix-correctness on the seeded corpus is statistically ≥ the incumbent baseline (bootstrapped) at acceptable cost.

### 4.6 The measurement design the corpus must be run under

Non-negotiable, because nondeterminism can exceed the signal: **temperature 0 does not give reproducibility** (batched inference, MoE routing, non-associative float accumulation). One benchmark found Claude 4.5 at 100% byte-identical on a short prompt but **20%** on a long open-ended one.

1. **Paired within-task design** — every model on the *same* seeded tasks; compare per-task, never pooled.
2. **≥5–10 rollouts per model per task**; report distributions, not single scores.
3. **Task-level bootstrap 95% CIs** (e.g. 10,000 resamples) + paired tests across the matched set.
4. **Control context/cache state** — fix repo state, standardize prompt-cache between runs (cache-read tokens are logged, so cache state can be *verified* not assumed), pin uv/tooling, record `effort` per run.
5. **Control confounds** — randomize task order, **interleave models** (not model-A-all-morning), log time-of-day/API latency, and **freeze model versions** for the window; record `app.version` and model id so a mid-window model update is *detectable* (and discard that window).

**Minimum window:** ≥40 seeded defects × ≥5 repeats per model; admit a lane only when the **paired CI excludes zero**. Separately, for "did development get faster" at all: **≥20–40 completed tasks per condition and ≥2–4 weeks** of routine work.

### 4.7 Reproducibility, versioning, and the two commission-5 halves flagged for the GO ruling

Pin the corpus with a **version tag and a manifest** (seed, tool versions, mutation operators, defect hashes); store as **committed JSON/YAML defect specs + a deterministic applier script**; record the uv-pinned environment; **regenerate on a cadence** to stay ahead of contamination.

**The two halves of commission 5 (memo SC), with candidate homes, as options for the GO ruling.** Memo SC is the one commission whose two halves have different destinations, and only one of them has a named home. Presented as options — this lane rules nothing:

| Half | What it carries | Candidate homes (options) |
|---|---|---|
| **(a) Decision lifecycle** — R44–R49 | rejection/parked states, ADR sunset + Proposed, the finding forcing function, **ADR-landing predicates** | **Option 1 (named by the lane contract): fold into intake `#30` §A** — §A already proposes exactly R47's organ ("every ruling that names an adoption or a mechanism carries a machine-checkable *landing predicate*… a periodic organ verifies the set") and calls it "the highest-value item in the whole answer". The convergence is independent and therefore strong. · **Option 2: a scope note on ADR-111**, since R46 is ADR-111 and R44/R45 are corrections *to* the memo, not adoptions. · **Option 3: split** — R47 to `#30` §A, R44/R45 to a correction note, R48/R49 declined per §3. Draft fold text: §5 of this file. |
| **(b) Session continuity** — R43, R50, R51 | plan-carrying residual, exceptions-only boot, verification-at-cut, keep-the-probe-bundle | **UN-OWNED — no intake covers it.** · **Option 1: intake `#18`** (`2026-07-27-tech-handoff-process-v6-proposal`) — R43/R50/R51 are all HANDOFF_PROCESS changes and #18 is the process-proposal intake. · **Option 2: intake `#19`** (`2026-07-27-func-operator-design-input-night-shift-handoff-reform`) — if the batch reads these as operator-design input rather than spec edits. · **Option 3: attach to `[#511]`** — R50/R51 *are* `[#511]`'s live fork (which load is cut); this is the tightest coupling and the smallest surface. · **Option 4: a new intake `#33`** — cleanest ownership, but takes the pending set up by one, which is the ceiling `#32` was filed at 32-not-30 to respect. |

**Recommendation, offered not taken:** (a) → Option 1 (`#30` §A), because the convergence is independent; (b) → Option 3 (`[#511]`), because R50/R51 are already that row's fork and a fourth handoff intake buys ownership the row already has. The operator rules.

## 5. Draft fold text for the GO ruling — NOT applied to any intake

Per the lane contract, the two expected-new elements are drafted here as report text for the operator's GO ruling. **No intake file was edited by this lane.** Both drafts are phrased to add no birth and change no verdict.

### 5.1 Draft — amendment to intake `#29` (seeded-defect corpus, from memo TM)

> **AMENDMENT DRAFT 2026-08-10 (research-ingest lane A) — the seeded-defect corpus is specified, and it is the batch's blocking artifact**
>
> Fold A already ruled that **no bake-off runs before the seeded-defect corpus exists** and that the 2026-07-31 single-diff A/B is precedent for method only. That ruling named an artifact it did not specify. The specification now exists in-repo at `docs/archive/2026-08-09-research-agent-telemetry-model-comparison-wf-02c940ef.md` (Q5–Q6, Stage 3), extracted to buildable form at `docs/audits/2026-08-10-technical-research-corpus-distillate.md` §4.
>
> **Carried as binding on any future bake-off:** 40→80 defects, stratified by `defect_class` with a `detectable-by` tag; a blend of mutation operators (≥2 tools) and hand-authored realistic defects; the four scoring axes (detection · fix-correctness · false-positive · cost/time); the admission rule (paired CI must exclude zero against the incumbent); and the leakage constraints (private/unreadable path, throwaway worktree at eval time, git history sanitized, nothing in `CLAUDE.md` or prompts).
>
> **Two couplings recorded, neither resolved here:** (1) the corpus inherits `[#502]`'s host constraint — mutation generation needs `fork()`, so it is CI-only and behind `[#501]`; (2) the leakage constraint requires an artifact that is deliberately **not** readable from the working tree, which is in tension with this repo's committed-artifact discipline and is a placement decision for ratification, not a build detail.
>
> **Births: zero.** The corpus build is a candidate at batch-4 planning (L), not a row filed by this amendment.

### 5.2 Draft — fold into intake `#30` §A (decision lifecycle, from memo SC)

> **§A FOLD DRAFT 2026-08-10 (research-ingest lane A) — external convergence on the landing-predicate organ, plus two corrections to the memo**
>
> §A's proposal — every ruling that names an adoption or mechanism carries a machine-checkable **landing predicate**, verified periodically — is **independently derived** by commissioned memo `wf-fafd931b` (`docs/archive/2026-08-09-research-session-continuity-decision-lifecycle-wf-fafd931b.md`, Q7), which names it the industry pattern **architecture fitness functions + ADR-to-code traceability** and calls it "the highest-value adoption" for this fleet. The published rule it supplies: **every non-retired ADR should map to at least one fitness function**; an accepted ADR with no mapped check fails the audit. That is §A's organ with an external name and a stated coverage bar — the strongest form of support §A can receive, since neither source saw the other.
>
> Library-first candidates it names, in preference order: **import-linter** contracts, **Conftest** (single local binary — explicitly *not* OPA-the-server), and plain `pytest` — plus the observation that `audit.py`'s 41 checks **already are** home-grown fitness functions, so the missing organ is the **binding from each accepted ADR to at least one of them**, not the checks. That narrows §A's ratification choice: the register shape, not the checker.
>
> **Two corrections to the memo, recorded so the fold does not import them:** (1) the memo asserts this repo lacks a Proposed ADR state — false; `docs/decisions/ADR-111-finding-triage-pipeline.md` is `Status: Proposed` and ADR-94 codifies the in-place Proposed→Accepted edit. (2) It asserts there is no durable rejected/parked intake home — false; `docs/intake/README.md` §5 carries `REJECTED (reason, kept) [terminal → archive/]` and `disposition: deferred` (parked-but-alive, `trigger:`/`review-date:` required), ruled 2026-07-19 and deployed by `[#398]`. What survives is the *ratio*, not the absence: 1 Proposed ADR in 71. The memo's ADR-wide `review_date` proposal is genuinely un-landed but argues against a live ruling — ADR-102 §4 declines a `review_date` time-box for its own subject with a stated reason.
>
> **Births: zero.** No W-item, no row, no verdict changed.

## 6. Scope / method

**What this covered.** All six memos read end-to-end from the in-repo copies landed by this lane at `f571ac3c` (not from the operator's Downloads), and every proposal in each memo's Recommendations / staged-plan / minimal-starter sections enumerated into the table. The reconcile baseline is commit `6a4a1d78` plus the four landed elements it produced, read in full: intake `#32`, intake `#29` Folds A and B, and the `#25` W-9(a) scope note.

**How claims were checked.** Every `LANDED-ALREADY` locator was verified to exist on this branch before being cited (file presence, and for counts the actual command). Every `false-about-this-repo` entry names the falsifying locator. Counts measured live on `worktree-ingest-research-corpus` at `f571ac3c`: 196 open BACKLOG rows · 5 rows with `footprint:` · 70 Accepted + 1 Proposed ADR · 41 `check_`/`verify_`/`validate_` definitions in `scripts/audit.py` · zero hits for `grimp`/`import-linter` in `pyproject.toml`, `.pre-commit-config.yaml`, `uv.lock`.

**What this did NOT cover, stated so it is not read as coverage.**

- **No intake, ADR, or BACKLOG file was edited.** §5 is draft report text awaiting a GO ruling.
- **The mis-citation in intake `#32` (R60-3) is reported, not fixed** — the lane contract forbids intake edits. It needs an operator ruling on the repair channel, since intakes are governed as amend-not-edit.
- **SC's "~150 un-adjudicated closure proposals" is UNVERIFIED here.** `logs/` on this branch contains only `TOKEN-LOG.md`; no `PROPOSALS-*.md` artifact is present to count. Neither confirmed nor refuted.
- **Cost estimates are the memos' own** (S/M/L), not re-estimated against this repo's measured arc costs.
- **Vendor prices, model versions, and maintenance-status claims are as-of 2026-08-09 and are the memos' own sourcing**, much of it self-flagged VENDOR or REPORTED. Nothing in the table re-verified a vendor price or a GitHub maintenance signal; CP's own caveat that its GitHub-sourced maintenance claims were UNVERIFIED (API 403 through the proxy) stands unchanged.
- **`ecosystem/` edge-registry design (GR Stage 0 schema)** was not evaluated against the existing `ecosystem/*.yaml` one-concern-per-file precedent; that is a build-time question, not a ratification one.

**Genre note (ADR-100).** This is an audit — evidence *about* state. It requests no change. The rows whose disposition is a change belong to their owning intake, and the one un-owned half is §4.7(b).
