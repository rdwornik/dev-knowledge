# ADR-59: Universal Visual Repository Pattern

- **Status:** Accepted
- **Date:** 2026-05-27
- **Amends:** Extends ADR-38 (universal baseline), ADR-34 (file naming), ADR-51 (ARCHITECTURE convention); builds on PLAYBOOK "Root hygiene" (`:196`, `:223`).
- **Decommission:** none (additive standard + audit checks)
- **Source:** Operator decision (Rob, 2026-05-27). No Council transcript. Grounded in empirical verification performed this session — VS Code sort semantics and `tach` config discovery were tested, not assumed (see Decision 3 and the Verification notes).

## Context

The 2026-05-26 cross-repo universalization mega-session achieved audit-tool 3/3
PASS across all four child repos (`docs/audits/2026-05-26-cross-repo-universalization-verification.md`).
But operator inspection of `corp-monorepo` afterward revealed **visual chaos at
the repository root**: lowercase tool configs (`pyproject.toml`, `ruff.toml`,
`tach.toml`) interleaved with the ALL-CAPS canonical Markdown files, splitting
`VISION.md` from its siblings. The audit tool reported conformance because it
checks content presence + frontmatter only — never visual ordering or file-name
discipline.

The operator's requirement: every repository must look and be named the same, so
that opening any repo — or creating a new one — presents a universalized layout.
("Nazewnictwo, forma jest ta sama.") Consistent naming and visual ordering reduce
re-orientation cost across a multi-repo solo ecosystem.

This is the gap between "audit tool PASS" and "operator visual order." It must be
**codified** (enforceable standard), **encoded in the audit tool** (so violations
surface), **applied to `.dev-knowledge` itself** (self-consistency), and **rolled
out** to the four child repos (retrofit, executed in separate sessions).

## Decision

### 1. Dot-prefix discipline (file naming)

**Default rule.** Every tool/config file at a repository root is **dot-prefixed**
if the tool supports a dot-prefixed variant. Dot-prefixing groups configs together
(they sort ahead of ALL-CAPS names under the workspace sort settings in Decision 3)
without hiding them — visibility of what is configured is preserved (no
`files.exclude` for config files; PLAYBOOK `:238`).

**Exceptions — industry-standard names that MUST NOT be dot-prefixed** (the tool
requires the exact name, or ecosystem convention fixes it):

- `pyproject.toml` (Python PEP 518)
- `package.json` (npm)
- `Cargo.toml` (Rust)
- `setup.py`, `setup.cfg` (Python legacy)
- `requirements.txt`, `requirements-dev.txt` (pip convention)
- `Dockerfile`
- `Makefile`
- `LICENSE`
- `tach.toml` — **verified 2026-05-27**: `tach` 0.34.0 does **not** discover a
  `.tach.toml` ("Configuration file not found"); only `tach.toml` (or a
  `[tool.tach]` block in `pyproject.toml`) is read. Keep `tach.toml` at root, or
  embed under `pyproject.toml` per the PLAYBOOK root-hygiene caveat.
- `README.md` (deprecated from the baseline per ADR-38 A5, but if present, no dot)

**Dot-prefix REQUIRED — tools that accept the dotted variant:**

- `.ruff.toml` (ruff reads both `ruff.toml` and `.ruff.toml`)
- `.pre-commit-config.yaml` (standard dotted name)
- `.gitignore`, `.gitattributes`, `.editorconfig` (standard dotfiles)
- `.eslintrc.*` (standard dotted convention)
- The VS Code workspace file (Decision 3): `.{repo-slug}.code-workspace`

**Verification process when adopting a new tool:** check the tool's documentation
(or test empirically, as was done for `tach` here) for dot-prefix support. If
supported → dot-prefix. If not → add the exact name to the exception list in this
ADR **and** in `scripts/audit.py`, and note the outcome in the commit. The
exception list is the single source of truth, mirrored in the audit tool.

### 2. Canonical Markdown visibility

All canonical governance files live at the repository root with **ALL-CAPS**
names (existing convention per ADR-34; codified here for the visual goal).

**Universally mandatory (every repo — per ADR-38 A5 / ADR-51):**
`VISION.md`, `CLAUDE.md`, `ARCHITECTURE.md`, `BACKLOG.md`.

**Optional / repo-specific** (present by judgment; ALL-CAPS when present):
`JOURNAL.md`, `ENVIRONMENT.md`, `CONTRIBUTING.md`.

**`.dev-knowledge`-only** (never required in a child repo): `ESSENTIALS.md`,
`PLAYBOOK.md`, `LESSONS.md`, `TOKEN-LOG.md`.

The visibility rule is about **casing/naming consistency**, not forcing optional
files into existence. With dot-prefix discipline (Decision 1) + the sort settings
(Decision 3), the mandatory + optional canonical files cluster as one ALL-CAPS
block between the dot-prefixed configs and any lowercase exceptions.

> Rationale for not requiring more than the four: PLAYBOOK's file-presence baseline
> makes only those four universal. `LESSONS.md`/`PLAYBOOK.md`/`ESSENTIALS.md`/
> `TOKEN-LOG.md` are `.dev-knowledge`-only; requiring them everywhere would falsely
> fail every child repo. (The plan that motivated this ADR initially listed seven
> required files — corrected here against governance.)

### 3. Workspace settings

Every repo carries a VS Code workspace file at root, dot-prefixed:
`.{repo-slug}.code-workspace`.

Required `settings` keys:

```json
{
  "settings": {
    "explorer.sortOrder": "default",
    "explorer.sortOrderLexicographicOptions": "upper"
  }
}
```

- `explorer.sortOrder: "default"` — folders first, then files, each group sorted
  by name.
- `explorer.sortOrderLexicographicOptions: "upper"` — **uppercase grouped before
  lowercase.** This is the key that makes ALL-CAPS canonical `.md` files cluster
  ahead of lowercase configs/folders.

> **Verified 2026-05-27 (corrected from the originating plan):** VS Code's
> `"default"` lexicographic option **mixes** uppercase and lowercase names —
> it does **not** put uppercase first. Only `"upper"` clusters ALL-CAPS files
> first, which is the actual visual goal. The plan's `"default"` would have left
> canonical files un-clustered. Source:
> [VS Code PR #97272](https://github.com/microsoft/vscode/pull/97272).

**Resulting root order** (with Decisions 1–3 applied): folders (alphabetical) →
dot-prefixed config files (`.gitignore`, `.pre-commit-config.yaml`, `.ruff.toml`,
`.{repo}.code-workspace`) → ALL-CAPS canonical `.md` block (ARCHITECTURE → VISION)
→ lowercase exceptions (`pyproject.toml`, `tach.toml`).

**No `files.exclude` to hide config files** (PLAYBOOK `:238`). `files.exclude`
remains acceptable only for noise like `**/__pycache__`, `*.pyc`, `projects`.

### 4. Date-sorted content

Dated folders (`docs/audits/`, `docs/handoffs/`, `docs/decisions/transcripts/`)
use an ISO date prefix: `YYYY-MM-DD-{slug}.md` (ADR-34). ISO alphabetical sort =
chronological **ascending** (oldest first).

> **Verified 2026-05-27:** VS Code has **no native per-folder reverse sort.**
> `explorer.sortOrderReverse` is **not a real setting** — it is a rejected feature
> request ([microsoft/vscode#149951](https://github.com/microsoft/vscode/issues/149951)).
> A workspace previously carried `"explorer.sortOrderReverse": true` believing it
> produced "newest dates first"; VS Code silently ignored it, so newest-first was
> never actually in effect. The no-op key is removed (Decision 6 / Phase D).

Operators navigate dated folders by: scroll to the bottom for newest, `Ctrl+P`
(Quick Open) by date prefix, or the workspace's `open-latest-*` tasks. Native
reverse sort is **not** part of the standard. (If reverse sort ever becomes
high-friction, evaluate a third-party Explorer-sort extension as a future BACKLOG
item — not adopted now.)

### 5. Enforcement

`scripts/audit.py` gains three read-only checks (consistent with ADR-36 — the
audit tool reads child repos and writes only to `.dev-knowledge`):

- **`dot_prefix_discipline`** — for config files at the repo root (`.toml`,
  `.yaml`, `.yml`, `.json`, `.ini`, `.cfg`, `.conf`): PASS if dot-prefixed or on
  the exception list; FAIL otherwise. Root only — subfolder files ignored.
- **`canonical_md_visibility`** — the four mandatory canonical files present at
  root (delegated/complementary to `adr38_baseline` + `claude_md`); plus, for any
  canonical file present, correct ALL-CAPS casing (a `Vision.md`/`readme.md`-style
  mis-case FAILs because it breaks the visual clustering).
- **`workspace_settings`** — a `.{repo}.code-workspace` file exists, parses as
  JSON, and contains the two required `settings` keys with the specified values;
  WARN if the file exists but a key is missing/wrong; FAIL if absent or malformed.

All three are wired into `audit.py health` and the per-repo audit findings.

### 6. Rollout

- **`.dev-knowledge` itself:** applied in the same session as this ADR (the
  workspace gains `sortOrderLexicographicOptions: upper` and drops the no-op
  `sortOrderReverse`; configs are already dot-prefixed).
- **Four child repos** (`ai-council`, `corp-ops`, `corp-sca-time-automation`,
  `corp-monorepo`): retrofit **plans** generated this session into `docs/audits/`;
  **execution happens in separate per-repo sessions** (Layer-2 invariant — this
  repo never writes to child repos).

## Consequences

**Positive.**
- Visual + naming consistency across all repos — faster re-orientation.
- New repos inherit the pattern via template + audit check.
- The audit tool now catches the drift class it previously missed (visual order,
  config naming, workspace settings).
- One standard reduces per-repo decision fatigue.

**Costs / trade-offs.**
- The dot-prefix exception list will grow as new tools are adopted; managed via
  the documented verify-then-list process (Decision 1).
- Dated content remains ascending (oldest-first) in the Explorer — native reverse
  sort is impossible; the navigation workarounds (Decision 4) are the accepted
  answer.
- Retrofit is four separate sessions of work (~15–30 min each).

**Risks.**
- Tool dot-prefix support can change between versions; the verify step (not
  assumption) is the guard. The `tach` exception is pinned to the verified
  behavior of 0.34.0 and should be re-checked if `tach` changes config discovery.

## Alternatives considered

- **`files.exclude` to hide configs** (a clean root by hiding clutter). Rejected:
  the operator wants configs **visible** (what's configured matters); dot-prefix
  + sort achieves grouping without hiding (PLAYBOOK `:238`).
- **`sortOrderLexicographicOptions: "default"`** (as the originating plan stated).
  Rejected on verification: `default` mixes case and does **not** cluster the
  ALL-CAPS files — it does not meet the goal.
- **Keep `explorer.sortOrderReverse: true`** for newest-first dated content.
  Rejected: it is not a real VS Code setting (no-op); keeping it is misleading.
- **Require all seven canonical `.md` files everywhere** (plan's initial list).
  Rejected: contradicts ADR-38 A5 / PLAYBOOK — `LESSONS.md` et al. are
  `.dev-knowledge`-only; would falsely fail every child repo.
- **A third-party Explorer-sort extension** for true reverse/custom order.
  Deferred: adds a per-machine dependency for marginal benefit; revisit only if
  ascending dated-folder order becomes a real blocker.

---

## Amendment — 2026-05-27: `explorer.sortOrderReverse` is real (correction)

The original ADR claimed (Context line 140, "Alternatives considered" line 210,
PLAYBOOK Visual Pattern subsection) that `explorer.sortOrderReverse` is **not a
real VS Code setting** — a rejected feature request — and removed it from the
workspace on that basis. Empirical re-verification this session shows that claim
was wrong.

**Evidence (verified 2026-05-27):**

- [microsoft/vscode#149951](https://github.com/microsoft/vscode/issues/149951)
  was the feature request and is **closed**, labelled `insiders-released` and
  `verified`.
- [microsoft/vscode#149952](https://github.com/microsoft/vscode/pull/149952) is
  the implementation PR and was **merged on 2024-07-30**.
- The setting exists in current VS Code and reverses the order produced by
  whatever `explorer.sortOrder` resolves to (an ASC/DESC toggle, per the PR
  author's framing — not a third sort mode).

**Operator-observed regression.** Removing `explorer.sortOrderReverse: true` in
commit `ea79a20` caused the operator's dated folders (`docs/audits/`,
`docs/handoffs/`, `docs/decisions/transcripts/`) to flip from newest-first to
oldest-first — a clear UX degradation the operator surfaced explicitly.

**Corrected decision.** Keep both settings together:

```jsonc
"explorer.sortOrder": "default",
"explorer.sortOrderLexicographicOptions": "upper",
"explorer.sortOrderReverse": true
```

`lexicographic: upper` continues to cluster ALL-CAPS canonical `.md` files
(visual pattern intent). `sortOrderReverse: true` flips the natural ordering so
dated folders show newest-first. The two compose: the visual pattern survives;
the operator's preferred dated ordering is restored.

**Status of the original "Alternatives considered" bullet** ("Keep
`explorer.sortOrderReverse: true` … Rejected: it is not a real VS Code setting"):
**superseded.** The rejection rationale was based on a false premise.

**Status of the Consequences "ascending dated-folder order" trade-off:**
**no longer a trade-off** — newest-first is now native, via this amendment. The
"open-latest-*" workspace tasks remain useful as a fast keyboard path but are no
longer the *only* answer.

**Why the correction was missed in the original session.** The original
session's verification step inspected a stale or partial reference and treated
the GitHub issue title ("would like to reverse the file order") as a rejected
ask. It did not inspect the linked PR (`#149952`) or check current VS Code
behavior. Lesson logged at the protocol layer: when removing a workspace setting
on the basis that it does not exist, the verification must reach the
implementation PR or the running editor — not just the issue page.

**No changes** to Decisions 1–4, the audit checks, the dot-prefix exception
list, or the retrofit plans. The amendment is workspace-scoped.

**Files touched by this amendment:** `.dev-knowledge.code-workspace` (restore the
setting + corrected comment), this ADR (append-only). No PLAYBOOK rewrite —
PLAYBOOK already references this ADR by number and its body will be touched
only if a future divergence surfaces during use.

---

## Amendment — 2026-06-01: usage logs live under `logs/`, not the canonical root

**Trigger.** The G1 doc-coherence audit found `TOKEN-LOG.md` referenced bare in
several docs (CLAUDE §4/§5/§10, ARCHITECTURE §Invariants/§Key-conventions,
PLAYBOOK), implying a repository-root location, while the file actually lives at
`logs/TOKEN-LOG.md` (and has since at least 2026-04-27). This created an apparent
conflict with Decision 2 (ALL-CAPS canonical `.md` at root).

**Clarification (no change to Decisions 1–6 or the audit checks).** The
root ALL-CAPS-canonical rule (Decision 2) covers **governance documents** —
`VISION` / `ARCHITECTURE` / `CLAUDE` / `BACKLOG` (mandatory), and the optional
`JOURNAL` / `ENVIRONMENT` / `CONTRIBUTING` / `LESSONS`. **Usage / telemetry logs
are not governance documents**: `TOKEN-LOG.md` is a Claude-usage snapshot log and
lives under `logs/` (`logs/TOKEN-LOG.md`). The `canonical_md_visibility` audit
check (#5) already scopes its mandatory set to the four governance docs, so
`logs/` placement was always conformant — this amendment records the intent so
the docs stop implying root.

**Boundary.** A future usage/telemetry log follows the same rule: lives under
`logs/`, named in `UPPER-CASE` for scannability, not promoted to the canonical
root. Governance docs (decisions, conventions, vision, backlog) stay at root or
in `protocols/` per their existing homes.

**Files touched by this amendment:** the doc references corrected to
`logs/TOKEN-LOG.md` (CLAUDE.md, ARCHITECTURE.md, PLAYBOOK.md), and this ADR
(append-only). No audit-check or workspace change.

---

## Amendment — 2026-06-02: `pytest.ini` joins the dot-prefix exception list

**Trigger.** An ecosystem readiness scout found `corp-sca` FAILs the
`dot_prefix_discipline` audit check (#4) on its root `pytest.ini`. But
`pytest.ini` **cannot** be dot-prefixed: pytest does not discover a
`.pytest.ini` — only `pytest.ini` (or a `[pytest]` / `[tool:pytest]` block in
`pyproject.toml` / `tox.ini` / `setup.cfg`) is read. It is an industry-standard
config name in exactly the same category as the already-exempt `pyproject.toml`,
`setup.cfg`, and `tox.ini`. This was a gap in the standard, not a repo defect —
any repo using `pytest.ini` would have failed conformance with no in-place fix
available.

**Clarification (no change to Decisions 1–6 or to the audit-check logic).**
`pytest.ini` is added to the exception list — the set of industry-standard names
that MUST NOT be dot-prefixed. It joins the canonical list in Decision 1's
"Exceptions" block (the body list above remains the historical record; this
amendment is the authoritative addition) and is mirrored in
`scripts/audit.py` (`_DOT_PREFIX_EXCEPTIONS`), per the single-source-of-truth
maintenance rule. A repo may keep `pytest.ini` at root, or embed its config
under `pyproject.toml`/`tox.ini`/`setup.cfg`; both are conformant.

**Boundary.** A future tool config that the tool will not read under a dotted
name follows the same path: verify empirically that the dotted variant is
unsupported, then add the exact name to this exception list (amendment) and to
`audit.py`. Configs whose tool *does* read the dotted variant stay dot-prefixed.

**Files touched by this amendment:** `scripts/audit.py`
(`_DOT_PREFIX_EXCEPTIONS` + comment), `tests/test_audit.py` (exemption test),
and this ADR (append-only). No workspace or Decision change.
