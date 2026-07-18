# CROSS-CONSUMER DIVERGENCE LEDGER — night 2026-07-17

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-17
- **Source:** 2026-07-17 night-run scratchpad (`DIVERGENCE-LEDGER.md`), content unchanged below this block.
- **Night rule:** the run was READ-ONLY / zero-commit — no writes to any real repo tree; all
  outputs went to scratchpad. This docs-only arc (branch `docs/2026-07-17-night-audit`, filed
  2026-07-18) is its first commit.
- **Companion night-run audits (same arc):** `2026-07-17-technical-night-verdict-sheet.md`, `2026-07-17-technical-night-divergence-ledger.md`, `2026-07-17-technical-night-live-fire-sheet.md`, `2026-07-17-technical-night-handoff-evidence-pack.md`.

Witnessed file-level state across the three methodology repos. Every row framed as the
operator's own question — *"why is X like this here and different there?"* — answered from
**witnessed state** (live `ls`/`cat`/`git check-ignore`/`grep`), never memory.

**Repos (roots resolved live via `git rev-parse --show-toplevel`):**
- hub — `C:/Users/1028120/Documents/Dev/.dev-knowledge` @ `e0cbffdb` (main, clean)
- corp — `C:/Users/1028120/Documents/Dev/corp-monorepo` @ `560a38d` (branch `docs/2026-07-17-night-process-audit`, 0/0 vs main, clean)
- ai-council — `C:/Users/1028120/Documents/Dev/ai-council` @ `3862749` (main, clean)

**Verdict doctrine (operator-ruled, binding):** toolchain/infra surfaces (L1–L5, caches,
config layout) have NO product reason to diverge → **default ALIGN-NOW**. Any KEEP/DECLARE
must carry a reason the operator would accept in ONE sentence; "historical accident" is not
a reason, it is an ALIGN.

**Parity coverage note:** `fleet_parity.py` measures **hub↔consumer** only (161 at-parity, 20
pass-declared, 1 gate-ahead-declared, 0 refused/warn-undeclared). It does NOT measure
**cross-consumer** (corp↔ai-council) alignment — which is exactly what several rows below
expose as GAPs.

`sol:` column = filled by the P3 Codex gpt-5.6-sol adversarial pass.

---

## L1 — pre-commit config location

| repo | witnessed |
|---|---|
| hub | root `.pre-commit-config.yaml` (9670 B) **+** root `.pre-commit-hooks.yaml` (ADR-71 hook-source manifest). No `assets/`. |
| corp | root `.pre-commit-config.yaml` (5009 B). No `assets/`. |
| ai-council | root `.pre-commit-config.yaml` (2611 B) **+** `assets/ruff-pre-commit.yaml` (1074 B, git-tracked). |

- **SAME/DIFFERENT:** config **location** SAME (all root). Auxiliary files DIFFERENT: hub carries a hook-source manifest; ai-council carries a lone vendored `assets/` yaml; corp carries neither.
- **Parity coverage:** `root-sweep` covers top-level entries (hub `assets/` absent so N/A; ai-council `assets/` is a declared/allowed dir but its *contents* are not rowed) → **partial GAP** on the vendored yaml.
- **Ownership:** location = methodology-generic. hub `.pre-commit-hooks.yaml` = hub-source (conditional). ai-council `assets/ruff-pre-commit.yaml` = the divergent item.
- **VERDICT:** location → no action (SAME). hub `.pre-commit-hooks.yaml` → **KEEP-LOCAL** (reason: ADR-71 makes the hub a pre-commit hook-source repo; hub-only by construction). ai-council `assets/ruff-pre-commit.yaml` → **ALIGN-NOW** (see L7 — redundant vendored copy of the already-inline stanza; drift hazard).
- **Proposed change:** `rm ai-council/assets/ruff-pre-commit.yaml` + drop its `INSTALL.md` reference (consumer edit → operator-run or ADR-36-compliant carrier). `sol:` ____

---

## L2 — ruff config  ← operator's centerpiece pain

**The GATE (pre-commit ruff hook) — witnessed IDENTICAL across all three:**
`repo: https://github.com/astral-sh/ruff-pre-commit` · `rev: v0.15.5` · `id: ruff` · `args: []` (check-only).
→ **SAME / already ALIGNED.** Parity: `ruff-gate` row PASS-declared all three (tombstone re-activated per 2026-07-12 fleet ruling). Ownership: methodology-generic. **No action.**

**The RULE SET (`pyproject.toml [tool.ruff]`) — witnessed DIVERGES 3 ways:**

| repo | select | ignore | line-length | target-version | required-version | format |
|---|---|---|---|---|---|---|
| hub | (unset→defaults E/F) | — | (88 default) | — | `>=0.15.5` | — |
| corp | E, F, I | E501 | (88 default) | — | — | omitted (CRLF) |
| ai-council | E, F, I, W | — | 120 | py312 | — | quote-style double |

- **SAME/DIFFERENT:** **DIFFERENT (3-way).** No two repos share a rule set.
- **Parity coverage:** ruff **rule-set content** is NOT a parity surface — only the gate rev/mode is. → **GAP** (the exact cross-consumer divergence tonight must expose).
- **Ownership:** rule-set currently unclassified. A fleet-canonical baseline would be methodology-generic.
- **VERDICT (nuanced):**
  - **corp → DECLARE.** corp documents deliberate reasons in-file: `ignore = ["E501"] # don't fight this battle now` (large-monorepo line-length lint-debt) and `# ruff-format omitted: core.autocrlf=true Windows CRLF/LF conflict`. Both are one-sentence-acceptable → record, don't force.
  - **ai-council → ALIGN-NOW** toward a canonical baseline (no documented reason; its E/F/I/W + line-length 120 + py312 is the closest to a sane fleet default and could BE the baseline).
  - **hub → ALIGN-NOW** toward the baseline (tiny validators-only Python surface, but should model fleet canon). KEEP hub's `required-version` floor — it is a legitimate hub-specific anti-downgrade guard, additive to any baseline.
- **Proposed change:** either (a) adopt a fleet-canonical `[tool.ruff.lint]` baseline (candidate: `select = ["E","F","I","W"]`, `line-length = 120`, `target-version = "py312"`) and converge hub + ai-council, corp DECLARE-until-scheduled on E501; **or** (b) add a `parity-surfaces` row `ruff-ruleset` that DECLARES each repo's config + reason so the divergence is at least *tracked*. Doctrine leans (a). `sol:` ____

---

## L3 — caches on disk + gitignore coverage

| cache | hub | corp | ai-council |
|---|---|---|---|
| `.ruff_cache` | on-disk, ign `.gitignore:5` | on-disk, ign `:6` | on-disk, ign `:7` |
| `.pytest_cache` | on-disk, ign `.gitignore:4` | on-disk, ign `:7` | on-disk, ign `:8` |
| `.mypy_cache` | absent on disk; **IS ignored** at `.gitignore:6` | absent, `.mypy_cache/` in gitignore `:8` | on-disk, ign `:9` |

> **CORRECTION (sol WITNESS-ERROR, verified live):** my hub witness agent reported `.mypy_cache`
> "NOT IGNORED" — that was a **false negative**. `git check-ignore -v .mypy_cache` returned empty
> only because `.mypy_cache` doesn't exist on disk in hub and a **trailing-slash pattern
> (`.mypy_cache/`) doesn't match a non-existent bare path** — the exact inference I correctly made
> for corp but wrongly reversed for hub. Live grep: `hub/.gitignore:6:.mypy_cache/` IS present.

- **SAME/DIFFERENT:** **SAME** — all three repos ignore all three caches. Hub simply hasn't
  materialized `.mypy_cache` on disk (never ran mypy). Line numbers differ (expected).
- **VERDICT:** **RETRACTED — NO ACTION.** There is no gitignore gap. (This was the ledger's one
  false actionable finding; sol caught it, live state confirms the retraction.)

---

## L4 — `.claude/` inventory (depth 2)

| subdir | hub | corp | ai-council |
|---|---|---|---|
| commands/ | 4 (changelog-review, handoff, override, save) | 1 (override) | 1 (override) |
| skills/ | 2 (verify, check-against-spec) | 1 (gotchas) | **0** |
| workflows/ | 1 (conformance-hub.js) | 1 (conformance-corp.js) | **0** |
| rules/ | 1 (git-discipline) | 0 | 3 (code-standards, python-env, testing) |
| agents/ | 1 (artifact-reader) | 0 | 0 |
| generated/ | 2 (commands-repo, recent-adrs) | 0 | 0 |
| floor (CLAUDE-FLOOR.md + check_floor_hash.py + .sha256) | absent (hub=source) | present | present |
| settings.local.json / scheduled_tasks.lock | both | both | neither |

- **SAME/DIFFERENT:** DIFFERENT, but **most is by-design.** hub-only `agents/`+`generated/`+3 extra `commands/` = hub-local/source. `/review-closures`+`/ship` reach consumers via the `tier1-lifecycle` plugin, not `commands/`. floor present in both consumers, absent in hub = correct source-asymmetry.
- **Genuine cross-consumer divergences:**
  1. **rules/**: hub 1 / corp 0 / ai-council 3. → **KEEP-LOCAL** (reason: project-specific behavior rules — `code-standards`/`python-env`/`testing` are ai-council product rules; `git-discipline` is hub's; each repo owns its own).
  2. **skills/gotchas**: corp has a repo-level gotchas skill, ai-council does not. → **KEEP-LOCAL** (reason: CLAUDE.md §8 — repo-level `.claude/skills/gotchas/` holds *project-specific* gotchas; the universal gotchas skill is USER-level `~/.claude/`. corp accreted project gotchas, ai-council hasn't yet — content, not a methodology gap).
  3. **workflows/ (conformance)**: hub + corp each have a `conformance-<repo>.js`; ai-council has **no `workflows/` dir at all**. → **DECLARE / operator-confirm** (reason: the conformance workflow is an *optional* per-repo instrument, NOT a MUST parity surface — `fleet_parity` shows 0 must-absent. Verdict pends: does ai-council want one? If yes → ALIGN (author `conformance-ai-council.js`); if opted-out → DECLARE).
- **Ownership:** floor/generated/agents/hub-commands = hub-source/local. rules/gotchas = project. conformance-workflow = conditional.
- **Proposed change:** decide ai-council conformance workflow (author or declare opt-out); leave rules/ and gotchas project-local. `sol:` ____

---

## L5 — slash-command header format

- Witnessed: **all three `override.md` byte-shape-identical** — `---` YAML frontmatter, `name: override` + `description: …`, no `allowed-tools`, no dotted/plugin-prefixed names. hub's other three commands same format; **hub `handoff.md` lacks a `name:` key** (has `description:` only — cosmetic, command still resolves by filename).
- **SAME/DIFFERENT:** **SAME.** The operator's hypothesized "dots/plugins vs none" format delta is **NOT present** — every command in every repo uses plain `name:`/`description:` frontmatter.
- **Parity coverage:** `command-<x>` rows PASS-declared. Ownership: methodology-generic.
- **VERDICT:** **KEEP / no action** (format already uniform). Optional trivial: add `name: handoff` to hub `handoff.md` for internal consistency.
- **Proposed change:** (optional) add `name: handoff` line to hub `.claude/commands/handoff.md`. `sol:` ____

---

## L6 — root-file census vs ADR-101 sanctioned set

- Witnessed root entry counts: hub 34, corp 34, ai-council 32 (excluding `.`/`..`).
- Every divergent root entry is **either declared or product/env**:
  - Declared (root-sweep PASS-declared): `.vscode` (all), `.claude-plugin`/`codex`/`package.json`/`package-lock.json`/`.worktreeinclude` (hub), `.github` (corp, `github-ci` row).
  - Product source dirs: hub `deploy`/`ecosystem`/`templates`/`plugins` (methodology-source); corp `src`/`tests`/`data`/`eval`/`models`/`output`/`tach.toml`; ai-council `src`/`tests`/`council_inbox`/`output`/`assets`.
  - Env/build (all gitignored, verified): `.venv` (corp+ai, not hub), `.hypothesis` (corp `:46`), `ai_council.egg-info` (ai `:4`), `node_modules` (hub `:72`, untracked), all `settings.local.json`.
  - `INSTALL.md`: consumers yes / hub no → by-design (hub is the source; nothing to install).
- **SAME/DIFFERENT:** DIFFERENT but fully accounted. `validate-hermetization` (Rule A + B) + `root-sweep` both green; **0 refused, 0 unsanctioned root entries.**
- **VERDICT:** **KEEP** — ADR-101 gate satisfied; every extra is declared or product/env-local. No action.
- **Proposed change:** none. `sol:` ____

---

## L7 — assets/ & config-file layout

| repo | pyproject | extra config at root | assets/ |
|---|---|---|---|
| hub | ✓ | `.pre-commit-hooks.yaml` (hook-source), `package.json`/`-lock` (marketplace) | none |
| corp | ✓ | `tach.toml` (Tach import-boundary tool) | none |
| ai-council | ✓ | — | `assets/ruff-pre-commit.yaml` (lone yaml) |

- No `setup.cfg` / `tox.ini` anywhere. All three are pyproject-centric.
- **The operator's "is one lone yaml really all it holds?" — CONFIRMED:** ai-council `assets/` holds exactly ONE file, `ruff-pre-commit.yaml`. Its header says it is the ruff-gate stanza to "merge into the host repo's `.pre-commit-config.yaml`" (because a CC-plugin cannot ship a pre-commit config). **But** ai-council's active `.pre-commit-config.yaml` *already has that stanza inline* (line 57, identical `rev: v0.15.5`) — so the asset is a **redundant vendored copy** that can silently drift from the live stanza.
- **SAME/DIFFERENT:** DIFFERENT. Each repo's "extra config" is distinct.
- **VERDICT:**
  - ai-council `assets/ruff-pre-commit.yaml` → **ALIGN-NOW** (remove — redundant with the inline stanza; the canonical distribution template belongs to the HUB, not vendored per-consumer). *[Same item as L1.]*
  - corp `tach.toml` → **KEEP-LOCAL** (reason: Tach enforces import boundaries across a Scale-L monorepo — product-specific tooling with no fleet analog).
  - hub `.pre-commit-hooks.yaml` + `package.json` → **KEEP** (reason: hook-source manifest + plugin-marketplace packaging — hub-by-construction).
- **Proposed change:** `rm ai-council/assets/ruff-pre-commit.yaml` (+ INSTALL.md ref); consider promoting the canonical stanza to a hub `templates/` distribution asset. `sol:` ____

---

## L8 — additional walk-found divergences (root/toolchain)

| item | hub | corp | ai-council | verdict |
|---|---|---|---|---|
| `.venv` | absent | present | present | **KEEP** (env: hub runs base Python 3.12.10, no venv; consumers gitignore theirs) |
| `node_modules` | present (ignored, untracked) | absent | absent | **KEEP** (hub-only marketplace/JS tooling; properly ignored) |
| `scheduled_tasks.lock` | present | present | absent | **KEEP** (runtime scheduler lock; environmental) |
| `INSTALL.md` | absent | present | present | **KEEP** (hub=source, no install; consumers document install — by-design) |
| conformance workflow | ✓ | ✓ | **✗** | see L4.3 — **DECLARE/operator-confirm** |
| `.mypy_cache/` gitignore line | **missing** | present | present | see L3 — **ALIGN-NOW** |

---

---

## P3 — sol adversarial pass (Codex gpt-5.6-sol, effort high, read-only, `-s danger-full-access`)

Every sol claim below was **re-verified against live state** before acceptance (sol can be wrong
just as my witness was — and my L3 error proves the point cuts both ways).

**Per-row `sol:` verdicts:**
- **L1 — sol BREAKS-MECHANISM (accepted):** removing ai-council's asset dangles its tracked
  references at `ai-council/.claude/settings.json:13` + `INSTALL.md:70` (both verified live). REFINE:
  repoint both to the **existing hub canonical asset** `hub/plugins/tier1-lifecycle/assets/ruff-pre-commit.yaml`
  (verified present, 1074 B), THEN remove the vendored copy — never a bare `rm`.
- **L2 — sol CHALLENGE (accepted, sharpens verdict):** the py312 baseline is **invalid** — corp
  declares `requires-python = ">=3.11"` (verified `corp/pyproject.toml:9`), so a py312 target would
  break corp's support floor. sol's trial checks: ~41 hub + ~19 corp violations if aligned. REFINE:
  preserve the bare prune-safe gates; baseline `target-version` = **py311** not py312; align only
  after a measured clean-migration pass; **DECLARE corp's measured lint debt**, not force the whole
  ruleset. (Also: corp's CRLF comment explains the **ruff-format hook** omission, not its lint rules —
  my L2 conflated them slightly.)
- **L3 — sol WITNESS-ERROR (accepted, RETRACTED above):** hub already ignores `.mypy_cache/` at
  `.gitignore:6`. No action.
- **L4 — sol CHALLENGE (accepted):** "optional instrument" is NOT an acceptable one-sentence reason
  for ai-council's missing conformance workflow — the hub's own
  `docs/audits/2026-07-11-technical-fleet-boundary-matrix.md:122-123` already calls this `.claude/`
  boundary a **DEFECT**. REFINE: ai-council conformance workflow → **ALIGN-NOW or a concrete
  operational opt-out** (not a hand-wave).
- **L5 — sol CHALLENGE (accepted):** format is NOT fully uniform — hub `handoff.md` lacks `name:`
  (`hub/.claude/commands/handoff.md:2`). REFINE: **ALIGN-NOW** add `name: handoff`.
- **L6 — sol CHALLENGE (accepted, new surface):** root-sweep proves *presence*, not *content*.
  Hub's `.dev-knowledge.code-workspace` hardcodes the **username + absolute paths** (`:5,9,51`)
  while both consumers use **relative** workspace roots — a real portability divergence root-sweep
  can't see. KEEP the root-sanction verdict; ALIGN workspace portability separately (see L9).
- **L7 — sol BREAKS-MECHANISM (accepted):** the ai asset is a deliberate install input, and it is
  **NOT byte-identical** to the inline stanza — it carries `name:` (`:19`) which the inline gate
  deliberately omits for prune-safety. So my "redundant, can drift" framing was imprecise. The real
  alignable point: ai-council **vendors a copy of the hub plugin asset** — migrate the references to
  the hub asset, then remove the copy. sol CONFIRMS KEEP for `tach.toml` + hub source-role manifests.
- **L8 — sol:** drop the false mypy action; keep the evidenced env/source asymmetries; ALIGN or
  concretely DECLARE the ai-council workflow omission (per L4).

**sol MISSED surfaces (new rows — folded in as L9):**

## L9 — additional divergences (sol pass)

| # | surface | witnessed | verdict |
|---|---|---|---|
| L9.1 | non-ruff pre-commit corpus | corp excludes codemap + **removed TOC bindings under #326** (`corp/.pre-commit-config.yaml:77-94`); ai-council **retains** TOC bindings (`:44-56`) | **DECLARE** — corp's removals are waivered in `corp/.methodology.yaml`; ai-council retaining TOC is a real cross-consumer asymmetry to record |
| L9.2 | `.claude/settings.json` hook wiring | hub uses `scripts/arm_hooks.py`; consumers use `python -m pre_commit install`; only hub+corp carry extra conformance hooks | **KEEP** hub arm_hooks (hub-source); **DECLARE** the consumer conformance-hook asymmetry (ties to L4/L9.1) |
| L9.3 | dev-tool dependency floors | pytest/ruff/pre-commit ranges differ; ai-council alone declares mypy yet omits the installed `pytest-xdist` (parity already PASS-declares xdist) | **DECLARE** — record the floor matrix; low-risk but currently unmeasured |
| L9.4 | `*.code-workspace` content | hub hardcodes username + absolute paths; consumers relative | **ALIGN-NOW** — make hub workspace paths relative/portable (parity only checks glob presence, not content) |

**WITNESS-ERRORS sol found (all verified + corrected):** (1) L3 mypy gap = false (retracted).
(2) my L2 table omitted per-file-ignores (corp ignores E/F in `tests/**`; hub has `tests/fixtures/**`
exceptions) — noted. (3) corp's CRLF comment = ruff-**format** hook omission, not lint ruleset. (4)
the ai asset is not byte-identical (carries `name:`). (5) **#276 removed nothing** — it is an OPEN
deploy-waiver feature (`hub/BACKLOG.md:182`); corp **never consumed codemap hooks**, and removed
**TOC** hooks under **#326** — so the "corp #276 hook removal" framing (which I fed the sol prompt)
was wrong; the accurate mechanism is #326/TOC. (6) ai-council tree is **not clean** (concurrent
session — see LIVE-FIRE-SHEET).

---

## Verdict roll-up (POST-SOL — corrected)

**ALIGN-NOW (toolchain, no product reason):**
1. **L5** — add `name: handoff` to hub `.claude/commands/handoff.md` (hub edit; 1 line; trivial).
2. **L9.4** — make hub `.dev-knowledge.code-workspace` paths relative/portable (hub edit).
3. **L1/L7** — repoint ai-council's `settings.json:13` + `INSTALL.md:70` to the hub canonical asset
   `plugins/tier1-lifecycle/assets/ruff-pre-commit.yaml`, THEN remove the vendored
   `ai-council/assets/ruff-pre-commit.yaml` (consumer edit — operator-run/carrier; **references first**).
4. **L4/L8** — ai-council conformance workflow: ALIGN (author `conformance-ai-council.js`) or a
   concrete logged opt-out (the boundary-matrix audit calls the gap a DEFECT — "optional" is not a pass).

**DECLARE (record the divergence — reason holds, but nothing measures it today):**
5. **L2** — ruff **rule-set** (the one real toolchain gap: the *gate* is fleet-aligned, the *lint
   rules* diverge 3 ways and no parity row measures them). Add a `ruff-ruleset` parity row; corp's
   E501/format debt DECLARED-until-scheduled; **baseline target = py311, not py312**.
6. **L9.1** — corp TOC/codemap removal vs ai-council TOC retention (non-ruff pre-commit corpus).
7. **L9.2 / L9.3** — settings.json hook-wiring + dev-tool dependency floors (currently unmeasured).

**KEEP-LOCAL (one-sentence reason holds — sol-confirmed):**
- L1/L7 hub `.pre-commit-hooks.yaml` + `package.json` (hub-source/marketplace).
- L7 corp `tach.toml` (Scale-L import-boundary tool).
- L4 rules/ + repo-level gotchas skill (project-specific content).
- L6 all root divergences (declared or product/env; ADR-101 gate green).
- L8 `.venv` / `node_modules` / `scheduled_tasks.lock` / `INSTALL.md` (env or by-design).

**RETRACTED:** L3 `.mypy_cache/` (false finding — already ignored).

**Headline for the operator (post-sol):** the surfaces you feared were silently diverging are
mostly (a) already fleet-aligned (the ruff **gate**, root sanctioning) or (b) divergent-with-a-real
-reason. After sol's corrections the genuinely-actionable list is: **2 trivial hub edits** (handoff
`name:`, workspace portability), **1 consumer cleanup** (repoint-then-remove ai-council's vendored
ruff asset), **1 defect to close** (ai-council conformance workflow), and **1 real measurement gap**
(the ruff **rule-set** — aligned gate, unaligned lint rules, unmeasured). The `.mypy_cache` "gap"
was a witness false-negative and is retracted.
