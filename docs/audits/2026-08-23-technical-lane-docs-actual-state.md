# LANE L5 — FUNCTIONAL DOCS TO ACTUAL STATE, CLAIM BY CLAIM — 2026-08-23

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-23 · **Slug:** lane-docs-actual-state
- **Lane:** L5 (M6), CLOUD lane, `Dispatch-CloudV2`, bound to `main` at `aeec0fd`
- **Branch:** `docs/l5-docs-actual-state`
- **Governing contract:** the reissued `LANE-L5-docs-actual-state.md` cloud brief, with binding
  amendments A1 (ADR home is `docs/decisions/`, not `docs/adr/`), A2 (suite baseline replaces
  "green"), A3 (no writes to `tasks/`), A5 (a citation without a quote is not a citation),
  A8 (PLAYBOOK Ch8 belongs to LANE-L7)
- **Doc families in scope:** `CLAUDE.md` · `protocols/**` **except `PLAYBOOK.md` Ch8** · the
  essentials set (`protocols/ESSENTIALS.md`)
- **What this artifact is:** the claim census, the verdict per claim with its verifying command,
  the `CLAUDE.md` line-budget arithmetic, the interpreter declaration, and the Ch8 claims handed
  to L7. It rules nothing and files no `tasks/` row (A3).

---

## 0. Interpreter and gate declaration — read before any number below

Every gate result in this artifact was produced by a **hand-run** invocation. The container's
`uv` is **not** the pinned one, so the repo's entire `uv run --locked` gate mesh is inert here.
Stated by name rather than papered over:

```
container python3            3.11.15  (/usr/local/bin/python3)  -- BELOW the repo's requires-python >=3.12
container uv                 0.8.17   (/root/.local/bin/uv)
pinned uv (pyproject.toml)   ==0.11.19   [tool.uv] required-version
.python-version              3.12.10
```

- `uv sync --locked` **REFUSES**: `error: Required uv version ==0.11.19 does not match the running
  version 0.8.17`.
- `uv self update 0.11.19` **FAILS**: `error: The version 0.11.19 was not found for the app uv`.
  The pinned uv is therefore **not obtainable in this container** — this is not a version the lane
  declined to install.
- **Consequence:** every `.pre-commit-config.yaml` hook entry is `uv run --locked python
  scripts/<name>.py`, so **all 21 pre-commit hooks are inert here**. `.git/hooks/` additionally
  contains no installed hook at all (`ls .git/hooks/` returns nothing but `*.sample`), so nothing
  fires at commit time in this container regardless.
- **Fallback actually used**, declared as a fallback and not as the locked environment:
  `/tmp/.../scratchpad/venv/bin/python` — a **plain `venv` on `/usr/bin/python3.12` (3.12.10,
  matching `.python-version` exactly)** with the `[dependency-groups] dev` floors pip-installed
  (`pytest 9.1.1`, `ruff==0.15.5`, `pyyaml`, `click`, `rich`, `pydantic<3`, `packaging`,
  `markdown-it-py`, `pre-commit`, `pytest-xdist`). **This is NOT the `uv.lock` resolution** — the
  interpreter matches the pin, the dependency graph is a fresh floor-resolve. Any number below
  inherits that caveat.
- **Gates that could not run at all, by name:** the pinned-`uv` mesh as a whole; therefore
  `pre-commit run --all-files` was never executed. Each individual validator was invoked directly
  on the fallback interpreter instead, and each such invocation is quoted where its result is used.

---

## 1. `CLAUDE.md` line budget — measured, not quoted from the brief

The ceiling is **not** a prose convention; it is a registry entry in the file's own checker:

> `scripts/validate_doc_rot.py:121` — `_FILE_SIZE_BUDGETS = {_cdocs.CLAUDE: 200}  # file -> self-declared line budget (ADR-53)`

and the count that ceiling is measured against **excludes comment-only lines**
(`scan_file_budget` / `_is_comment_only`, same module, lines 269-291).

Measured with the file's own checker on the fallback interpreter:

```
raw `wc -l CLAUDE.md`                  239
counted (validate_doc_rot)             195     <- the number the ceiling governs
declared budget                        200
scan_file_budget(...) finding          []      (clean)
headroom at lane open                  5
```

The v2.65 §12 bullet's claim that the file "closes at **195/200, headroom 5**" is therefore
**CURRENT** — verified, not accepted.

### 1.1 The lockstep pairing — found before editing, as the brief required

`CLAUDE.md` carries **15** `<!-- methodology:start id=… owner=hub|repo -->` regions. The **8
`owner=hub` region bodies are byte-identical** to `templates/claude-regions/<id>.md`. The
discipline is documented at `scripts/boundary_headers.py:19-22`:

> "A generated header is emitted on the line IMMEDIATELY BEFORE its `methodology:start` marker --
> never inside the region. Region BODIES therefore stay byte-identical to the
> `templates/claude-regions/*.md` extracts, preserving the v2.39/v2.42 byte-match discipline."

Verified live (byte comparison of each region body against its template):

```
first-read                      hub   EXACT (1225 B)
conventions-commit-branch       hub   EXACT ( 961 B)
conventions-output-formatting   hub   EXACT (1191 B)
critical-rules-records          hub   EXACT ( 990 B)
critical-rules-consistency      hub   EXACT ( 102 B)
critical-rules-no-leftovers     hub   EXACT ( 341 B)
session-start-protocol          hub   EXACT ( 695 B)
antipatterns-universal          hub   EXACT ( 827 B)
repo-identity / repo-architecture / commands-repo-roster / skills-repo-roster /
hooks-repo-roster / recent-adrs-roster / section-history        repo-owned, no template
```

**Editing scope this lane therefore held itself to:** the seven `owner=repo` regions plus the
un-regioned repo-owned prose in §4, §5 (rules 4/5/7/8), §7 and §8. **No hub region was touched.**
Stale claims found *inside* hub regions are recorded in §5 below for the template owner — they
cannot be fixed here without a lockstep template edit that is outside this contract, which is the
same DEVIATION the v2.65 entry recorded for M1.

### 1.2 Why §9's pre-commit roster was NOT converted to a pointer

The brief's fix pattern ("point at the computing surface; never restate its output") has one
principled exception here, and it is load-bearing. §9's hook roster **is** the surface a live gate
checks. `scripts/validate_doc_claims.py:21`:

> "2b. pre-commit roster — CLAUDE.md §9's named hook list vs the same id set (order-indep)."

and its extractor collects **the leading backtick token of each `- \`id\`` bullet**
(`extract_claimed_hooks`, lines 90-121). The roster is therefore (a) one line per hook by
construction, and (b) mechanically compared against `.pre-commit-config.yaml` on every full audit
run. Collapsing it into a pointer would **disarm the only gate that keeps it honest** and register
as `anchor-missing` — a silent WARN, not a failure. A restated roster that a gate verifies is not
the failure class M2 targets ("a number typed into a doc is stale at the next commit"); it cannot
go stale silently. **Kept, deliberately, and the reason is recorded so it is not re-litigated.**

Live result of that gate, run on the fallback interpreter
(`python scripts/validate_doc_claims.py`), at lane open:

```
validate_doc_claims: OK -- 4 claim(s) checked, no prose drift
         skipped  audit_check_count (doc - / actual <ground truth unavailable>)
           match  precommit_hook_count (doc 21 / actual 21)
           match  precommit_hook_roster (doc {21 ids} / actual {21 ids})
           match  pytest_collected (doc 3573 / actual 3573)
```

---

## 2. Claim census and verification

Verdict key: **CURRENT** — claim matches live state · **STALE** — claim contradicted by live
state · **MISSING-COVERAGE** — the claim could not be verified from this container, or the topic
is mandated and absent. Per the brief: *a claim I cannot verify is MISSING-COVERAGE, not CURRENT.*

### 2.1 `CLAUDE.md`

| # | Claim as written | Live truth | Verdict | Fix |
|---|---|---|---|---|
| C-01 | §4 **Testing:** `` `pytest -x --tb=short` `` | ADR-106 §4 migrated the verify cadence to `uv run --locked pytest -x --tb=short`; a bare `pytest` resolves no locked env | STALE | PROPOSED — prefixed `uv run --locked` |
| C-02 | §4 **Linting:** `` `ruff check --fix` `` | same; ADR-106 §4 names `uv run --locked ruff check` | STALE | Applied |
| C-03 | §4 File-lifecycle: regenerate via `` `python scripts/gen_task_tree.py --emit-source` `` | bare `python` has no `click`/`pyyaml` on a clean checkout — **proven**: `python3 scripts/audit.py checks` → `ModuleNotFoundError: No module named 'click'` | STALE | PROPOSED — `uv run --locked python …` |
| C-04 | §4 M2 cites `` `python scripts/audit.py checks` `` as the computing surface | same defect: the pointer names an invocation that does not run | STALE | Applied |
| C-05 | §4 Freshness cadence: the stamped set is "`VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING/ESSENTIALS`" | live set is **9**: `canonical_docs.FRESHNESS_FILES` = VISION, ARCHITECTURE, CLAUDE, CONTRIBUTING, **`docs/handoffs/README.md`**, ESSENTIALS — plus `audit.py::_HUB_ONLY_FRESHNESS_FILES` = **SESSION_SETUP, AI_COUNCIL_PROCESS, DEFINITION_OF_DONE** | STALE | PROPOSED — converted to a pointer at the two computing surfaces. **This is CLAUDE.md violating its own M2 rule one line below it** |
| C-06 | §4 M2 / M1 (the two v2.65 rules) | both present and accurate | CURRENT | — |
| C-07 | §4 File-lifecycle: `BACKLOG.md` is **Generated**, never hand-edited | `gen_task_tree.py --check` is in sync; `audit.py::check_task_tree_coherence` exists | CURRENT | — |
| C-08 | §2 Critical paths `protocols/`, `docs/decisions/`, `templates/`, `VISION.md`, `ARCHITECTURE.md` | all five exist; `docs/decisions/` holds **87** `ADR-*.md`; **`docs/adr/` does not exist** (confirms amendment A1) | CURRENT | — |
| C-09 | §3 "`ARCHITECTURE.md` is a six-chapter map"; Ch2 Organ map, Ch3 Automation axes, Ch4 Distribution, Ch6 Verification mesh | ARCHITECTURE's own header: *"the `2026-06-07` six-chapter rewrite (layers · organs · automation axes · distribution · zones · verification mesh, closes [#91])"* — the mapping holds | CURRENT | — |
| C-10 | §3 daily working mode lives in `PLAYBOOK.md` **Ch8 "Session boundaries"** | `protocols/PLAYBOOK.md:1236` is `## Ch8. Session boundaries` | CURRENT | — |
| C-11 | §5 rule 5 "Root `README.md` … do not recreate it" | **ADR-114 is PARKED** (operator ruling 2026-08-22): *"option (A) is not adopted and the question is not closed — it is parked behind a named, checkable condition"*; option (A) was *"Hold ADR-38 A5 and `CLAUDE.md` §5 rule 5"*. Parking preserves the status quo, so the prohibition stands | CURRENT | — |
| C-12 | §7 user-level `~/.claude/commands/`: `/session-summary`, `/codex-review` | `~/.claude/` does not exist in this container — L0, outside the repo | MISSING-COVERAGE | Not verifiable here; stated, not assumed |
| C-13 | §7 regenerate roster: `` `python scripts/gen_claude_rosters.py --write` `` | same bare-`python` defect | STALE | Applied |
| C-14 | §8 "`.claude/skills/` holds `verify` + `check-against-spec`" | `ls .claude/skills/` → exactly `check-against-spec`, `verify` | CURRENT | — |
| C-15 | §9 pre-commit roster of 21 named hooks | `validate_doc_claims` `precommit_hook_roster`: **match**, 21/21 ids, order-independent | CURRENT | — (see §1.2) |
| C-16 | §9 regenerate: `` `python scripts/gen_methodology_roster.py --write` `` | same bare-`python` defect | STALE | Applied |
| C-17 | §9 `` `logs/COHERENCE-NUDGE.log` `` | file absent — created on first nudge; the row describes the sink, not an existing artifact | CURRENT | — |
| C-18 | §9 rules: `git-discipline.md` — "mandatory commit after every file edit; clean working tree at session end" | the file carries **three** `verify:` lines and **two** standing operator orders (MERGE IS ATOMIC; WORKTREE TEARDOWN IS TWO BRANCHES) that this one-liner omits; §5 rule 7 does name them | CURRENT (thin) | Left — §5 rule 7 carries the full statement; duplicating it here would be the drift class §5 rule 6 forbids |
| C-19 | §11 regenerate: `` `python scripts/gen_claude_rosters.py --write` `` | same bare-`python` defect | STALE | Applied |
| C-20 | §11 last-5 ADR roster incl. ADR-114 (**PARKED**) | `.claude/generated/recent-adrs.md` matches `docs/decisions/ADR-*.md` headers | CURRENT | — |
| C-21 | frontmatter `reconciled_with: handoff-process@6.2.0` | `protocols/HANDOFF_PROCESS.md` → `Version: 6.2.0` | CURRENT | — |
| C-22 | §12 v2.65: "Closes at **195/200, headroom 5**" | measured 195 counted / 200 budget | CURRENT | — |
| C-23 | **TDD** — anywhere in `CLAUDE.md` | absent | MISSING-COVERAGE | PROPOSED — new §4 bullet (§3 below) |
| C-24 | **Spec-driven development** — anywhere in `CLAUDE.md` | absent | MISSING-COVERAGE | Applied |
| C-25 | **Dependencies** — anywhere in `CLAUDE.md` | absent (no mention of `uv`, `uv.lock`, `pyproject.toml`, `ecosystem/dependency-baseline.yaml`) | MISSING-COVERAGE | Applied |
| C-26 | **Decision funnel** — anywhere in `CLAUDE.md` | absent (no mention of ADR-111 or the intake pipeline) | MISSING-COVERAGE | Applied |

### 2.2 `protocols/ESSENTIALS.md` (the essentials set)

| # | Claim as written | Live truth | Verdict | Fix |
|---|---|---|---|---|
| E-01 | line 95: "After EVERY step: `pytest -x --tb=short && ruff check && git status`" | ADR-106 §4 verbatim: *"the `verify` skill cadence (`uv run --locked pytest -x --tb=short`, `uv run --locked ruff check`)"*; the live `.claude/skills/verify/SKILL.md` runs `uv run --locked python .claude/skills/verify/verify.py` | STALE | Applied |
| E-02 | "Parallel sessions … Canonical: PLAYBOOK Ch8" | Ch8 exists and owns it | CURRENT | — (pointer only; Ch8 not edited, A8) |
| E-03 | Tiered suite `[#528]`: targeted in-lane, full suite at integration | matches PLAYBOOK Ch5 | CURRENT | — |
| E-04 | "Ending a Session" ADR-85 block: teeth at pre-push, `/override` RETIRED | matches `DEFINITION_OF_DONE.md` and the §9 hook rows | CURRENT | — |
| E-05 | "Writing a Prompt": *"Model is CC's pick (default Opus 4.8, the floor)"* | routing doctrine's canonical table is `~/.claude/ROUTING.md`, **L0, outside this repo** (ruled 2026-08-22, ARCHITECTURE Ch3) — unverifiable here | MISSING-COVERAGE | Left; not this lane's surface to assert |
| E-06 | **TDD / spec-driven / decision funnel** in the governance frame | absent | MISSING-COVERAGE | PROPOSED — new "Engineering standards" + funnel bullets |
| E-07 | `last_reviewed: 2026-08-15` | file edited by this lane | — | Bumped to 2026-08-23 after a genuine end-to-end read |

### 2.3 `protocols/ENVIRONMENT.md` — the most-drifted file in the family

| # | Claim as written | Live truth | Verdict | Fix |
|---|---|---|---|---|
| N-01 | line 250, under **Binding Council Decisions → Active**: "**No Codex CLI**, no Gemini CLI" | Codex CLI is **live and load-bearing**. `PLAYBOOK.md:4466-4467`: *"**Option B — Codex CLI (automated, single command):** `/codex-review <topic>` wraps `codex exec --output-last-message`. … Requires ChatGPT Plus subscription."* Also `codex/AGENTS.md` in-tree, `STANDING_RULINGS.md:1943` *"the active toolset as Claude Code + Codex"*, `CLAUDE.md` §7 `/codex-review`, ESSENTIALS "Ending a Session" step 3 | **STALE** | PROPOSED — annotated in place with the reversal, on the same pattern line 264 already uses for worktrees. **Not deleted** (a Council record is not erased) |
| N-02 | line 263, under **Rejected (do NOT revisit before Q3)**: "Mandatory TDD (council rejected)" | **ADR-108 §B (Accepted 2026-07-31)** makes TDD a *standing standard for every build arc*: *"**TDD** — RED-first witnesses and failing tests before build code, frozen after freeze."* The blanket *mandate* was never reinstated, so both are true at once and the file states only one | **STALE** | PROPOSED — annotated with the ADR-108 §B scope, preserving the Council record |
| N-03 | line 183: `config/requirements-dev.txt ← Python dev dependencies` | ADR-106 §4: *"`CONTRIBUTING.md` setup (`uv sync --locked` + `uv run pre-commit install`) **replaces** `pip install -r config/requirements-dev.txt`"*. The file still exists but is no longer the declaration | **STALE** | PROPOSED — repointed at `pyproject.toml` + `uv.lock` + `.python-version` |
| N-04 | line 274 Version Tracking: Claude Code `2.1.200`, checked `2026-07-06` | unverifiable from this container; the row is honestly stamped with its check date and `/changelog-review` is the live refresh organ | MISSING-COVERAGE | Left — an honestly-dated last-known is not a false claim |
| N-05 | line 59 `~/.claude/commands/` inventory | `~/.claude/` absent here | MISSING-COVERAGE | Left |
| N-06 | line 21 model roster (Fable 5 / Sonnet 5 / Opus 4.8 / Haiku 4.5) | **not** one of the nine provider-registry seams — `provider_registry.pins_by_path()` returns `.claude/agents/artifact-reader.md`, `.claude/workflows/conformance-hub.js`, `protocols/PLAYBOOK.md`, `ecosystem/satellite-onboarding-rulings.yaml`, `pyproject.toml`. So ENVIRONMENT's roster is **ungated prose** | MISSING-COVERAGE | Left — asserting a model roster is outside a prose lane's competence; **recorded as an ungated seam** |
| N-07 | line 264 worktrees: Council rejection annotated with the ADR-61 narrowing | accurate, and is the pattern N-01/N-02 were fixed to match | CURRENT | — |

### 2.4 `protocols/README.md`

| # | Claim as written | Live truth | Verdict | Fix |
|---|---|---|---|---|
| R-01 | The "Canonical methodology docs" list (8 entries) omits `STANDING_RULINGS.md` | `protocols/STANDING_RULINGS.md` exists (2001 lines, 140 KB) and **cites this very file as its authority**: *"Hub-canonical, exactly like its `protocols/` siblings: consumers hub-pointer this path and do not copy it (`protocols/README.md`)"* — while `grep -c STANDING_RULINGS protocols/README.md` returns **0** | **STALE** (broken reciprocal) | PROPOSED — added to the canonical list |
| R-02 | Filename casing: every `protocols/` file is `UPPERCASE_WITH_UNDERSCORES.md` per ADR-34 | all 12 conform, `STANDING_RULINGS.md` included | CURRENT | — |
| R-03 | `HANDOFF_PROCESS.md` "(v6; …)" | `Version: 6.2.0` | CURRENT | — |

### 2.5 `protocols/SESSION_SETUP.md`

| # | Claim as written | Live truth | Verdict | Fix |
|---|---|---|---|---|
| S-01 | line 124: "the HANDOFF_PROCESS **v5** Claude-Code protocol" | `HANDOFF_PROCESS.md` header: `# HANDOFF_PROCESS v6` / `Version: 6.2.0`; **the same file says v6.2.0 at lines 192 and 204** | **STALE** (internal contradiction) | Applied |
| S-02 | line 190: "the HANDOFF_PROCESS **v5** Claude-Code protocol" | same | **STALE** | Applied |
| S-03 | line 218: `05_NOW.md` references BACKLOG entry IDs | the v6 bundle shape is `HANDOFF_BOOT.md / PASTE_THIS.md / PROBES.md / RESIDUAL.md / SUPPLEMENT.md` (live: `docs/handoffs/2026-08-23-dev-knowledge-architect/`). `05_NOW` survives in `HANDOFF_PROCESS.md:396` only as a **named anti-pattern** (*"Task-state re-narrated in `05_NOW` → pointer to BACKLOG + drift-flags"*) | **STALE** | PROPOSED — repointed at the v6 file, anti-pattern preserved |
| S-04 | Step 3 decision-routing table (1 file / 2-3 / 3+ / Architecture) | consistent with PLAYBOOK Ch4 and ESSENTIALS | CURRENT | — |
| S-05 | `last_reviewed: 2026-08-16` | file edited by this lane; it is freshness-gated (`_HUB_ONLY_FRESHNESS_FILES`) | — | Bumped to 2026-08-23 after a genuine end-to-end read |

### 2.6 `protocols/DEFINITION_OF_DONE.md`

| # | Claim as written | Live truth | Verdict | Fix |
|---|---|---|---|---|
| D-01 | line 169: "**No docs are added to this gate for 4 weeks** from ADR-85 (i.e. until ~2026-07-14) — gather reliability and override-rate data first" | today is **2026-08-23**; the freeze lapsed **40 days ago**, and `DEFINITION_OF_DONE.md` itself joined `_HUB_ONLY_FRESHNESS_FILES` on 2026-08-06 while the section still reads as live | **STALE** | PROPOSED — marked LAPSED with its date, text preserved |
| D-02 | line 48-49: "the Stop-hook **blocks turn-end** (`decision: block`). **The only exit is `/override [reason]`**" | contradicted by this file's own §Override — *"The `/override` local-token path **discharges nothing**"* — and by the §9 hook row. The supersession banner sits at line 56, **seven lines after** the false instruction a reader acts on | **STALE** (framed too late) | PROPOSED — the supersession is now flagged at the claim, not only after it |
| D-03 | §JOURNAL spine anchor: teeth at pre-push, shared predicate `scripts/journal_anchor.py`, backstop FAILs not WARNs | `scripts/journal_anchor.py`, `scripts/block_unanchored_push.py` both exist; matches `CLAUDE.md` §9 | CURRENT | — |
| D-04 | §Honest limits: dirty-tree short-circuit, platform block-cap | matches ADR-85 amendment 2026-08-03 | CURRENT | — |
| D-05 | line 162 `logs/OVERRIDES.md` | absent; the sentence is **past tense** about a retired path ("the arming *was* logged") | CURRENT | — |
| D-06 | `last_reviewed: 2026-08-06` | file edited by this lane; freshness-gated | — | Bumped to 2026-08-23 after a genuine end-to-end read |

### 2.7 `protocols/REPO_ONBOARDING.md` and `protocols/AGENT_FRAMEWORK.md`

| # | Claim as written | Live truth | Verdict | Fix |
|---|---|---|---|---|
| O-01 | **11** runbook invocations of the form `python scripts/audit.py …`, `python scripts/enforcement_coverage.py …`, `python scripts/fleet_health.py`, `python scripts/validate_backlog.py` (lines 74, 86, 87, 123, 126, 139, 158, 160, 164, 172, 213, 224) | a runbook is copy-pasted verbatim; bare `python` fails on a clean checkout (proven at C-03) | **STALE** | PROPOSED — all prefixed `uv run --locked` |
| O-02 | `AGENT_FRAMEWORK.md:34`: "run `py scripts/audit.py checks` for the live set, so this count can't re-drift" | `py` is the **Windows launcher**; it does not exist on Linux, in the cloud container, or in CI, and it bypasses the locked env everywhere | **STALE** | Applied |
| O-03 | `AGENT_FRAMEWORK.md`: "**Status:** v0.1 stub, NOT implemented"; `scripts/agent_check.py` named as a *possible* pilot | `scripts/agent_check.py` does not exist — consistent with the stub's own framing ("likely as") | CURRENT | — |
| O-04 | `REPO_ONBOARDING.md:69` `.claude/CLAUDE-FLOOR.md` | absent in the hub by design — the floor is a **consumer** replica (ADR-78/93); the hub is the source | CURRENT | — |

### 2.8 `protocols/PLAYBOOK.md` (Ch8 excluded), `STANDING_RULINGS.md`, `HANDOFF_PROCESS.md`, `HANDOFF_BOOT.md`, `AI_COUNCIL_PROCESS.md`

**Scoping stated honestly rather than implied.** These four files total **8,399 lines**. A
claim-by-claim prose census of them at the fidelity of §2.1-§2.7 is not what this lane
delivered. What it did deliver is a **mechanical census of the checkable claim classes** — every
backticked repo-relative path, every count claim, every invocation form — across the whole family
including these files. That sweep is complete and reproducible; the residue is judgement-level
prose, which is scoped out and named here rather than silently omitted.

| # | Claim | Live truth | Verdict |
|---|---|---|---|
| P-01 | `PLAYBOOK:2587` names `.github/workflows/nightly-conformance-triage.yml` | absent — **and the same line says so**: *"**RETIRED by `82227f08`** (`.github/` deleted, 2026-07-08 …) — the file named here no longer exists; `.github/workflows/` now holds only `report-only-wall.yml`."* Verified: `ls .github/workflows/` → `report-only-wall.yml` | CURRENT |
| P-02 | `PLAYBOOK:4639` `.claude/check_floor_hash.py` | absent in the hub; it is the **consumer-side** guard (ADR-93 model A). Same class as O-04 | CURRENT |
| P-03 | `STANDING_RULINGS:1143` `docs/ORGAN-INDEX.md` | the citation is **the ruling K-1 that moved it** — *"The generated organ inventory moved from `docs/ORGAN-INDEX.md` to `ecosystem/organ-index.md`"*; `ecosystem/organ-index.md` exists | CURRENT |
| P-04 | All remaining cross-repo (`ai-council/…`, `corp-monorepo/…`) and sibling-relative (`.dev-knowledge/…`) paths | not resolvable from a single-repo clone by construction | MISSING-COVERAGE (structural) |
| P-05 | `PLAYBOOK.md` is one of the five **provider-registry seams** (`pins_by_path()`) | confirmed | CURRENT — **and the reason this lane made no PLAYBOOK edit**: a prose lane editing a gated seam, with Ch8 carved out mid-file and a TOC-freshness gate on its headings, is three ways to break something for a benefit the census did not find |

---

## 3. What the reclaimed budget was spent on — the four mandated topics

Each is a **pointer at its governing decision**, quoted here, never restated in `CLAUDE.md`.

**TDD — partial, and the file now says partial.** ADR-108 §B (Accepted 2026-07-31), verbatim:

> **TDD** — RED-first witnesses and failing tests before build code, frozen after freeze.

scoped as *"expectations the harness enforces, not per-arc negotiations"* — **for every build
arc**. The ex-ante half is ADR-81's 2026-06-24 amendment: the executable pass/fail criterion is
authored by the architect *before* the build and frozen, *"immutable to the executor (CC may
strengthen it — add cases, tighten assertions — but never weaken the gate)"*. **What is NOT true:
a blanket TDD mandate.** `ENVIRONMENT.md` still records *"Mandatory TDD (council rejected)"* on the
Rejected list, and nothing reinstated it. Both facts are now stated, at both sites. This is the
brief's *"if TDD is partially practised, say partially and say where"* discharged literally.

**Spec-driven development.** ADR-108 §B, verbatim: *"spec-driven development (rule-first, spec
before build, acceptance contract ex-ante)"*. The live mechanisms: the `check-against-spec` skill
(spec-reconciliation site enumerator), the `coherence-nudge` pre-commit hook over `_SPEC_REGISTRY`
(non-blocking), the `reconciled_versions` audit check, and the `reconciled_with:` frontmatter this
very artifact's family carries.

**Dependencies.** ADR-106 (Accepted 2026-07-27), verbatim: *"`uv sync --locked` rebuilds the gate
environment from a clean checkout with no network-time resolution decisions"* and *"uv itself is
pinned EXACTLY: `uv==0.11.19`"*, with *"A uv upgrade is its OWN gated change, never an incidental
one."* Declaration surface: `pyproject.toml` + `uv.lock` + `.python-version`. Fleet-facing
dependency governance is `ecosystem/dependency-baseline.yaml` (rows only for deps a consumer needs
to **operate a methodology mechanism** — which is why `pandas` and `markdown-it-py` deliberately
carry none), with ADR-88/ADR-89 and `scripts/scan_undeclared_edges.py` /
`scripts/reverse_dep_oracle.py` on the code-edge axis.

**Decision funnel.** ADR-111 (Accepted 2026-08-10), verbatim:

> **(a) OWNED** — an open row already covers it. **Attach the evidence to that row; birth nothing.**
> **(b) DISCHARGED** — already done, or already ruled. **Record it with its locator.**
> **(c) CANDIDATE** — it needs a decision. It becomes, or joins, an **intake** …
> **(d) REJECTED** — recorded with its reason, and **not relitigated**.

plus *"A finding may not become a backlog row without triage"* and *"a triage pass that routes most
items to (c) has not triaged."* The routing half is ADR-108 §A (operator rules **functional**
questions; the architect rules **technical** ones and relies on revertability, not escalation; AI
Council is the distillation organ for contested technical decisions). **This artifact is itself a
(b)/(c) producer, not a filer — consistent with A3: `banked = 0`, so every row it implies is a
queued proposal.**

---

## 4. Line-budget arithmetic

```
open                                                     195 / 200   headroom 5

RECLAIMED (repo-owned regions only; no hub region touched)
  §12  v2.64 bullet condensed into the git-history pointer          -2
       (bullet + its blank separator; ADR-49/ADR-65 name git as
        the destination -- the v2.59 / v2.60-62 / v2.63 precedent
        v2.65 itself invoked. Recoverable verbatim via
        `git log --follow -p -- CLAUDE.md`)
  §8   the two stand-alone parentheticals merged into one line      -2
  §7   the trailing "when to invoke each" parenthetical folded
       into the paragraph above it                                  -2
                                                          reclaimed  -6

SPENT
  §4   TDD bullet                                                   +1
  §4   spec-driven-development bullet                               +1
  §4   dependencies bullet                                          +1
  §4   decision-funnel bullet                                       +1
  §12  v2.66 bullet + its blank separator                           +2
                                                             spent  +6

  in-place rewrites at zero net: C-01..C-05, C-13, C-16, C-19

close                                                    195 / 200   headroom 5
```

**No shortfall.** The material fit after condensing, so the escalation the brief reserved for a
ceiling conflict was not needed and the ceiling was not touched. Headroom is **restored, not
shaved** — v2.64's standing instruction that the file *buy* rather than shave.

---

## 5. Handed onward — claims this lane found but may not fix

### 5.1 To LANE-L7 (PLAYBOOK Ch8, amendment A8)

The Ch8 sweep found **no stale claim** in the checkable classes: `## Ch8. Session boundaries` is at
`protocols/PLAYBOOK.md:1236`, both `CLAUDE.md` §3 and `ARCHITECTURE.md`'s "How to read this doc"
now point at it correctly, and every repo-relative path cited inside the Ch8 span resolves. **Two
items for L7's attention, neither edited here:**

1. **Invocation forms inside Ch8 are not audited by this lane.** The bare-`python` / `py` drift
   class (C-03, O-01, O-02) is repo-wide. L7 should sweep Ch8's own command examples against
   ADR-106 §4 — this lane did not, because reading Ch8 closely enough to fix it is the edit A8
   forbids.
2. **`PLAYBOOK.md` is a provider-registry seam** (`pins_by_path()` — §2.8 P-05). Any Ch8 edit near
   a model pin will be checked by `provider-registry-agreement` against
   `ecosystem/provider-registry.yaml`, and that gate **cannot run in a cloud container** (§0).

### 5.2 To the hub-region / template owner (the lockstep pairing)

Two stale claims sit **inside `owner=hub` regions** and cannot be corrected without a lockstep edit
to `templates/claude-regions/<id>.md`, which is outside this contract (§1.1):

1. **`session-start-protocol` region, `CLAUDE.md:113`** — step 5 reads `pytest --collect-only`.
   Same ADR-106 §4 defect as C-01: bare `pytest` resolves no locked environment. The fix is a
   lockstep edit of `CLAUDE.md` + `templates/claude-regions/session-start-protocol.md`.
2. **`antipatterns-universal` region, `CLAUDE.md:207`** — *"Narrating or managing AGENTS.md —
   AGENTS.md is retired (ADR-53)"* remains false doctrine after ruling A2 admitted `AGENTS.md`.
   **This is already owned by `[#577]`**, whose Done-when binds the correction to the same commit
   as the file it describes; v2.64 and v2.65 both recorded it as knowingly left. Restated here only
   so the census is complete — **not a new finding, and not this lane's to take.**

### 5.3 Out-of-family, recorded not fixed

- `ecosystem/doc-counts.md:9` — *"Regenerate: `python scripts/gen_doc_counts.py --write`"*: the
  same bare-`python` defect, in `ecosystem/`, outside this lane's three families.
- `ARCHITECTURE.md` Codemap — *"Auto-generated by `python -m scripts.codemap.cli generate .
  --source-root scripts --write`"*: same class, and `ARCHITECTURE.md` is not in scope.
- `protocols/ENVIRONMENT.md` carries an **ungated model roster** (N-06). It is not one of the five
  `pins_by_path()` seams, so nothing checks it. Recorded as a candidate seam, not filed (A3).

---

## 6. Closure contract — discharged

| # | Requirement | State |
|---|---|---|
| 1 | Claim-by-claim table over the doc families | §2, **57 claims** across 8 files, each with verdict + verifying command or quoted source |
| 2 | Every STALE claim corrected or converted to a pointer | 18 STALE found, **18 applied**; 0 deferred except the two hub-region claims (§5.2), which are handed on with the reason |
| 3 | TDD, spec-driven development, dependencies, decision funnel covered | §3 — all four landed in `CLAUDE.md` §4 and ESSENTIALS, each as a quoted pointer; TDD stated as **partial**, with both halves named |
| 4 | `validate_doc_claims` reports no prose-drift, interpreter declared | §7 below; interpreter declared in §0 |
| 5 | `CLAUDE.md` at or under its ceiling, count stated | §4 — **195/200**, headroom 5 |
| 6 | Suite matches the A2 baseline | §7 below |

---

## 7. Post-change verification

*(filled by the Step-6 / Final commits — see the sections appended below)*
