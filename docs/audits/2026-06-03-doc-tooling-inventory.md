<!-- scope: meta -->

# Cross-repo doc-tooling inventory — grounding for the universalization plugin

**Date:** 2026-06-03
**Author:** Claude Code (read-only inventory; writes only into `.dev-knowledge`)
**Purpose:** Before designing a doc-tooling plugin that universalizes the **codemap** +
**TOC** generators across the fleet, ground the actual current state. The distribution
design hinges on one unknown: **how does the codemap reach and stay current in child
repos today** — copied generator, hand-maintained, or absent? This report answers that,
plus the copy-drift question, and captures the proven `tier1-lifecycle` plugin as the
build template.

**Contract honored:** READ-ONLY on every sibling repo (ADR-69 cross-repo read-only). No
sibling repo was modified, generated into, or applied to. The only write is this file.

---

## Central finding (the thing that unblocks the design)

> **The codemap/TOC generators live in exactly ONE repo — the `.dev-knowledge` hub.**
> The three children that show a codemap (`ai-council`, `corp-monorepo`, `corp-ops`)
> carry **hub-generated mermaid content between `<!-- CODEMAP:START/END -->` markers but
> NO generator** (`scripts/codemap/` absent in all four children) and **no freshness
> hook**. The codemaps there are **frozen, hand-maintained snapshots** — generated once
> (the mermaid `%%{init}%%` theme block is byte-identical to the hub's `mermaid_emit.py`
> output, so the hub generator produced them), then the generator was never left behind.
> Nothing re-generates or gates them.

**Implication:** there is **no existing distribution** of the generators to single-source.
The plugin must **DEPLOY FRESH** (ship the generator + freshness hook into each repo),
not de-duplicate existing copies. See "What this implies" below.

---

## Step 1 — Per-repo doc-tooling matrix

Flat key:value per repo (render-layer rule — no box-drawing; copy-safe).

### .dev-knowledge (hub — the canonical source)
- ARCHITECTURE.md: PRESENT, 541 lines (TOC-worthy: yes)
- CODEMAP markers: YES — codemap present and **live** (generator in-repo)
- TOC markers: YES (ARCHITECTURE) + YES (protocols/PLAYBOOK.md)
- scripts/codemap/: **PRESENT** (canonical generator)
- scripts/toc/: **PRESENT** (canonical generator)
- codemap-freshness hook: YES
- toc-freshness hook: YES (ARCHITECTURE) + toc-freshness-playbook (PLAYBOOK)
- Other TOC candidates: protocols/PLAYBOOK.md (~2710 lines) — already has a TOC
- Status: **the only repo where the codemap/TOC are generated + gated.**

### ai-council
- ARCHITECTURE.md: PRESENT, 317 lines (below the ~400 TOC threshold — borderline)
- CODEMAP markers: YES — content populated (55 lines of mermaid), but **frozen**
- TOC markers: no
- scripts/codemap/: absent · scripts/toc/: absent
- .pre-commit-config.yaml: present, but **no** codemap-freshness / toc-freshness hook
- Other TOC candidates: `docs/council-question-guide.md` (570 lines) — evaluate.
  (NOT candidates: the ~150 files in `output/` are immutable council transcripts;
  `JOURNAL.md` 373 lines is append-only newest-first — navigated by date, not TOC.)
- Codemap maintenance: **hand-maintained / frozen** (no generator, no gate)

### corp-monorepo
- ARCHITECTURE.md: PRESENT, 551 lines (**TOC-worthy: yes** — strongest child candidate)
- CODEMAP markers: YES — content populated (49 lines of mermaid), but **frozen**
- TOC markers: no
- scripts/codemap/: absent · scripts/toc/: absent
- .pre-commit-config.yaml: present, but **no** codemap-freshness / toc-freshness hook
- Other TOC candidates: ARCHITECTURE.md only (JOURNAL.md 395 lines is append-only)
- Codemap maintenance: **hand-maintained / frozen** (no generator, no gate).
  This is the highest-value target — largest source tree, real codemap, no freshness.

### corp-ops
- ARCHITECTURE.md: PRESENT, 289 lines (below TOC threshold)
- CODEMAP markers: YES — content populated (31 lines of mermaid), but **frozen**
- TOC markers: no
- scripts/codemap/: absent · scripts/toc/: absent
- .pre-commit-config.yaml: **ABSENT** — no pre-commit framework at all in this repo
- Other TOC candidates: none ≥300 lines
- Codemap maintenance: **hand-maintained / frozen**, and a freshness hook can't just be
  added — the repo has **no `.pre-commit-config.yaml`**, so the framework must be
  bootstrapped first.

### corp-sca-time-automation
- ARCHITECTURE.md: PRESENT, 200 lines (small)
- CODEMAP markers: **no** — the one repo with neither markers nor codemap
- TOC markers: no
- scripts/codemap/: absent · scripts/toc/: absent
- .pre-commit-config.yaml: **ABSENT**
- Other TOC candidates: none ≥300 lines
- Codemap maintenance: **none exists.** Likely a small (S) repo where ADR-51's M/L
  codemap mandate may not bind — confirm scale before deploying.

### Matrix summary (one line per repo)
- `.dev-knowledge`  — ARCH 541 · codemap LIVE (gen+hook) · TOC LIVE (ARCH+PLAYBOOK)
- `ai-council`      — ARCH 317 · codemap FROZEN (no gen/hook) · no TOC · has pre-commit
- `corp-monorepo`   — ARCH 551 · codemap FROZEN (no gen/hook) · no TOC · has pre-commit
- `corp-ops`        — ARCH 289 · codemap FROZEN (no gen/hook) · no TOC · **no pre-commit**
- `corp-sca-time-*` — ARCH 200 · **no codemap at all** · no TOC · **no pre-commit**

---

## Step 2 — Copy-drift detection

**Result: N/A — there are no copies to diff.**

`scripts/codemap/` and `scripts/toc/` exist in **only one repo** (`.dev-knowledge`). A
recursive search across all four children for any `*codemap*` / `*toc*` file under
`scripts/` (any path) returned **nothing**, and a grep across the children for any
invocation of the hub generator (`scripts.codemap` / `scripts/codemap` / `scripts.toc` /
`scripts/toc`) returned **nothing** — the children do not even call the hub's generator
by module path or shell-out. So:

- There is **no generator drift** to fix (no second copy exists anywhere).
- There IS **content drift risk**: the frozen codemaps in the three children have no
  freshness gate, so they silently diverge from their source trees over time. That is a
  *staleness* problem, not a *copy* problem — and it's exactly what deploying the
  generator + freshness hook would close.

**Conclusion for the design:** the plugin is **deploy-fresh**, not single-source. There is
no duplicated generator to consolidate; the work is to *introduce* the generator + gate
where today there is only frozen output (or, in corp-sca, nothing).

---

## Step 3 — Plugin build-template (proven `tier1-lifecycle` mechanism)

The doc-tooling plugin should mirror the shipped, working `tier1-lifecycle` plugin
exactly rather than invent a new distribution path. Captured structure:

**Marketplace (the hub IS the marketplace):**
- `.dev-knowledge/.claude-plugin/marketplace.json` — name `dev-knowledge-methodology`,
  owner Rob, a `plugins[]` list whose entries are `{name, source: "./plugins/<name>",
  description}`. A second plugin is **one more entry** in this same array.

**Plugin layout** (`.dev-knowledge/plugins/tier1-lifecycle/`):
- `.claude-plugin/plugin.json` — `{name, version, description, author, keywords}`.
  **`version` is the cache key** (see update dance below).
- `hooks/hooks.json` — hook registrations. Scripts referenced via
  `${CLAUDE_PLUGIN_ROOT}/scripts/<x>.py`; they operate on the **host** repo via
  `$CLAUDE_PROJECT_DIR`. **NOTE (verified 2026-06-02):** plugin `SessionStart` hooks
  register too late for the one-shot init event and never fire — only per-turn hooks
  (Stop) are reliable. (Relevant if the doc-tooling plugin ever wants session-time
  surfacing; freshness is better as a **pre-commit** gate anyway — see caveat below.)
- `commands/<name>.md` — slash commands (e.g. `/review-closures`).
- `scripts/*.py` — the bundled logic; resolves host paths via `$CLAUDE_PROJECT_DIR`.
- `assets/` — files a CC plugin **cannot** install itself (e.g. `ruff-pre-commit.yaml`),
  to be merged into the host by hand per INSTALL.md.
- `tests/` — e.g. `test_plugin_paths.py`.
- `INSTALL.md` — per-repo install + the **version-bump cache-refresh dance**.

**Install / update commands (from INSTALL.md, verified 2026-06-02):**
- First install per repo (project scope, config committed into host):
  - `claude plugin marketplace add /path/to/.dev-knowledge --scope project`
  - `claude plugin install <plugin>@dev-knowledge-methodology --scope project`
  - `/reload-plugins`
- Writes to host `.claude/settings.json`: `extraKnownMarketplaces` +
  `enabledPlugins`. **Gotcha:** repos that gitignore `.claude/` (e.g. ai-council) need
  `git add -f` or the install isn't committed.
- **Update after editing plugin source (the cache is version-keyed):**
  1. bump `version` in `plugin.json`; 2. `claude plugin marketplace update
  dev-knowledge-methodology`; 3. **per repo:** `claude plugin update
  <plugin>@dev-knowledge-methodology --scope project`; 4. restart session.
  Three traps: `marketplace update` alone does NOT re-copy at an unchanged version;
  `plugin install` no-ops on an already-installed repo; `plugin update` defaults to
  user scope (pass `--scope project`).

**The critical CC-plugin limitation for THIS plugin:** *a CC plugin cannot ship a
`.pre-commit-config.yaml`.* The `tier1-lifecycle` plugin works around it by shipping the
ruff stanza as an **asset** that the operator merges into the host's pre-commit config by
hand (INSTALL §2). The doc-tooling plugin's freshness hooks (`codemap-freshness` /
`toc-freshness`) are pre-commit hooks → **same constraint applies**: ship them as an
asset stanza, document the merge, and bootstrap a `.pre-commit-config.yaml` in the two
repos that lack one (`corp-ops`, `corp-sca`).

**One structural difference to plan for:** `tier1-lifecycle`'s scripts run *in place* from
`${CLAUDE_PLUGIN_ROOT}` against the host via `$CLAUDE_PROJECT_DIR` — they never get copied
into the host. A **pre-commit hook**, by contrast, runs from the host repo root and needs
the generator importable *there* (`python -m scripts.codemap.cli ...`). So the codemap/TOC
generator either (a) gets **copied into each host's `scripts/`** at install (deploy-fresh —
and then re-introduces the copy-drift the plugin was meant to avoid, unless the version
bump + re-deploy is the discipline), or (b) the hook invokes the generator from the
**plugin cache path** rather than host `scripts/`. This is the **key open design decision**
the build must resolve — flagged here, not decided (grounding only).

---

## What this implies for the doc-tooling plugin

1. **Deploy-fresh, not single-source.** No generator copies exist to consolidate (Step 2).
   The plugin *introduces* the generator + freshness gate where today there's only frozen
   output. Single-sourcing only becomes a concern *after* first deploy (how to keep the
   N deployed copies from drifting — the version-keyed cache dance is the lever).

2. **Resolve the generator-location decision first (Step 3 caveat).** Pre-commit hooks run
   from the host root, but `tier1-lifecycle` scripts run from the plugin cache. Decide:
   copy the generator into each host `scripts/` (simple, but re-creates drift) **or** have
   the freshness hook shell into the plugin-cache generator (drift-proof, but couples the
   hook to the cache path + version dance). This choice drives everything else.

3. **Per-repo application targets (deploy priority):**
   - **corp-monorepo** — highest value: ARCHITECTURE 551 lines (TOC-worthy), real frozen
     codemap, has pre-commit already. Deploy codemap gen+hook AND add a TOC.
   - **ai-council** — frozen codemap, has pre-commit. Deploy codemap gen+hook. ARCH 317 is
     borderline for TOC; `docs/council-question-guide.md` (570) is the better TOC target.
   - **corp-ops** — frozen codemap but **no `.pre-commit-config.yaml`** → must bootstrap
     the pre-commit framework before any freshness hook can land. ARCH 289 < TOC threshold.
   - **corp-sca-time-automation** — **no codemap at all**, no pre-commit. Confirm repo
     scale vs ADR-51's M/L mandate before deciding whether it gets a codemap at all.

4. **Two repos need pre-commit bootstrapped** (`corp-ops`, `corp-sca`) before a freshness
   gate is even possible. The plugin's INSTALL must cover "host has no pre-commit yet."

5. **TOC scope is narrow.** Only corp-monorepo's ARCHITECTURE (551) clearly clears the
   ~400-line / 8-section bar among children; ai-council's council-question-guide (570) is
   the other candidate. The hub already has both ARCHITECTURE + PLAYBOOK TOCs. Do NOT
   auto-TOC the small ARCHITECTUREs (corp-ops 289, corp-sca 200, ai-council 317).

6. **Recommendation only — no plugin built, nothing applied.** This is grounding. Next
   step is the design doc / ADR for the doc-tooling plugin, then the build on the
   marketplace, then the one-time per-repo application (markers + first generate).

---

## Method note (reproducibility)

All sibling reads were non-destructive: `wc -l`, `grep -q` for markers/hooks, `find` for
generator presence, `awk` to slice between markers, and a `grep -rl` for cross-repo
generator invocation. No file in any sibling was opened for write. Verified against the
hub's canonical `scripts/codemap/cli.py` (hardwired to ARCHITECTURE.md) and
`scripts/toc/cli.py` (takes a file arg → reusable across docs).
