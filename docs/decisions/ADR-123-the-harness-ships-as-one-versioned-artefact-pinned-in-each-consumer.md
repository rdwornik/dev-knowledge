# ADR-123: The harness ships as one versioned artefact, pinned in each consumer and upgraded by pull request

- **Status:** Proposed
- **Date:** 2026-09-25
- **Decision tier:** Architecture (Path A — the architect's technical proposal under ADR-108 §A, drafted by
  `lane-adr-drafts` on `LANE-5B2-11-adr-drafts.md`, batch WAVE5B-N2 row 11). **Stays Proposed until the operator
  ratifies.** The functional questions are in §Operator decision options, not decided here.
- **Amends:** none. **Would supersede, step by step,** the byte-copy carriers of ADR-92 (`deploy/tool.py` +
  `deploy/carrier_*.py`) as each is replaced (§Migration). **Admits** the package layout that
  `pyproject.toml:250` excludes "absent an ADR" — for one workspace member only, not the hub root.
- **Related:** ADR-28 (Layer 2 never drives a child repo — a package that runs *inside* the consumer keeps it),
  ADR-78/93 (child floor), ADR-91 (corpus versioning; the operator tags), ADR-92 (carriers, reconcile/verify),
  ADR-101 (tree seal — a new package directory needs admission), ADR-106 (uv pinned exactly), ADR-120 (the
  spine), ADR-124 (the code standard the artefact carries), ADR-126 (where consumer lanes run).
- **Provenance:** `PLAN-HARNESS-CONSOLIDATE-DEPLOY-2026-09-25` §5 ADR-A and precondition W2 ("the harness's
  distribution form is decided by ADR before any consumer repository is touched"). **Intake:** none — born
  from a batch order.
- **Decommission:** none now. Each carrier in §Migration step 3 is removed only after its replacement is
  green in the first consumer (replace-then-remove).
- **Source (in-repo):** `ARCHITECTURE.md` Ch4 "Distribution and transfer" (five channels; "Cloud clones are
  hub-independent by design"); `deploy/tool.py`, `deploy/carrier_{precommit,floor,mesh,plugin,docs,globalconfig}.py`,
  `deploy/manifest-v1.5.0.yaml` header (the floor-digest drift it documents); `.claude-plugin/marketplace.json`;
  `plugins/tier1-lifecycle/INSTALL.md`; `pyproject.toml:17-19` (`package = false`) and `:250` (src-layout
  "excluded absent an ADR"); `.devcontainer/devcontainer.json:147` (the hub already consumes a devcontainer
  Feature). **Source (transport, in addition):** `to-browser/SESSION-lane-research-distribution.md` (C1: six
  forms compared, sources dated 2026-09-25); `to-browser/DIGEST-AJ-DELTA-2026-09-25.md` §"What the course says
  about deploying a method across many repositories" (M05 L05: a shared versioned CLI; the harness distributed
  as a version-controlled plugin); `to-cc/PLAN-HARNESS-CONSOLIDATE-DEPLOY-2026-09-25.md` §1-§5.

## Context

1. **Today six carriers ship the methodology, and none ships the harness.** `deploy/tool.py::make_carriers()`
   (`deploy/tool.py:428-449`) registers six: the global Codex config, the `tier1-lifecycle` plugin, pinned
   pre-commit hooks, the floor, the enforcement mesh and the docs templates (`carrier_docs.py`). `ARCHITECTURE.md`
   Ch4 counts *channels* (five, the browser boot among them), not carriers; C1 listed five carriers and missed
   `carrier_docs` (corrected here after the Codex terra review). The organs "harness mode" needs in a consumer
   lane — `dispatch.py`, the gates, `lane_handback_gate.py`, `plan_lint.py`, the contract grammar — are not
   carried at all; the mesh byte-copies two scripts (`session_end_backpressure.py`, `canonical_freshness_gate.py`).
2. **Byte copies drift invisibly.** Carried scripts sit outside any lock; the v1.5.0 manifest header records that
   every consumer carrying the floor holds the previous floor bytes until re-deployed. The consumer pins nothing;
   the hub pushes a reconcile.
3. **The goal needs no hub at run time.** Plan §1 outcome 1: a lane for `corp-monorepo`, `ai-council` or
   `win-tooling` starts in a codespace with hooks, gates, contract grammar and handback armed, without the laptop
   and without querying the hub. `ARCHITECTURE.md` Ch4 already states the invariant ("Cloud clones are
   hub-independent by design").
4. **The hub is not a package.** `pyproject.toml:19` `package = false` ("flat-layout governance repo, never built
   or installed"); `scripts/` and `deploy/` have no `__init__.py` and tests import 74 bare module names through
   `pythonpath = [".", "scripts", "deploy"]` (`pyproject.toml:236-257`). Any form that ships the organs has to
   carve them out — that cost is common to every option that meets outcome 1.
5. **External practice points the same way.** The Architekt Jutra course (M05 L05) names a shared, versioned
   internal CLI for deterministic operations and a harness distributed as a version-controlled plugin
   (DIGEST-AJ-DELTA). Uber/Shopify/Backstage are cited there, not measured here.

## Decision

- **D1 — One artefact, one coordinate per release.** The harness ships as one Python distribution (working name
  `dk-harness`), built from a **uv workspace member** inside the hub (`packages/harness/`); the hub root stays
  `package = false`. A consumer pins it by git URL + tag in its own `pyproject.toml`; `uv.lock` records the
  resolved commit. An upgrade is one consumer PR whose substantive diff is the lock line plus regenerated install
  outputs.
- **D2 — The artefact carries all three surfaces.** (a) **Organs** as console scripts (`harness dispatch`,
  `harness gate …`, `harness handback`, `harness plan-lint`). (b) **Gates** as `repo: local` pre-commit hooks whose
  entry is `uv run --locked harness gate <id>`, so the gate version *is* the locked version — no second `rev:` to
  bump. (c) **The Claude Code surface** (hooks, commands, skills, the floor) as package data that
  `harness install` materialises into the consumer, idempotently, as generated files stamped with the version.
- **D3 — Drift is a gate.** `harness check` fails when a materialised file differs from what the locked version
  would write; it runs as one of the D2(b) hooks and in CI.
- **D4 — Hub-only stays hub-only.** Governance prose, audits, handoffs, research, the browser boot, the task store
  and the global Codex config (`~/.codex/AGENTS.md`, user-machine-scoped) are not in the artefact.
- **D5 — Replace, then remove.** `deploy/tool.py`'s carriers retire one at a time, each after its replacement is
  green in the first consumer (§Migration), never before (plan W3).

## Quality attributes

<!-- Thesis fields (DIGEST-THESIS-ARCH-PROCESS §2 and "Proposed ADR template"), carried here as ADR-124 D5 proposes
     every ADR should. The closed set is the thesis's ten (ch.6 intro :6-7). -->

- **Quality attribute(s):** Deployability (primary), Modifiability.
- **Scenario (six parts):**
  - *Source:* the integrator seat of a consumer repository.
  - *Stimulus:* a harness release `vX.Y.Z` is tagged in the hub.
  - *Environment:* a fresh codespace of `corp-monorepo`, no laptop, no network path to the hub after `postCreateCommand`.
  - *Artifact:* the consumer's pinned harness (lock line + materialised files).
  - *Response:* one PR bumps the lock; `harness install` regenerates; `harness check` and the gates pass; a lane
    runs and merges with the gates armed.
  - *Response measure:* **1** coordinate changed per upgrade; **0** hub calls at lane run time; a consumer lane
    merged in the cloud **3/3** (plan P4 gate).
- **Decision evidence:** the matrix below (options × criteria, scored).

## Decision matrix

**Scoring rule.** Each option is scored 1-5 per criterion (5 best); total = Σ(weight × score), maximum 500.
**K4 is a threshold:** an option scoring below 4 on K4 cannot meet plan §1 outcome 1 by itself, so it is ranked
only as a *component* of a mix, never as the answer. Scores are from C1's findings and the in-repo facts above;
where C1 gave no number, the score is this lane's judgment and says so by being in the table, not in a source.

Criteria (weights sum to 100): **K1** run-time independence — no hub call once installed (20) · **K2** pin in the
consumer, upgrade as one reviewable PR (20) · **K3** a fresh codespace/cloud clone gets it with no laptop step (15) ·
**K4** covers the whole payload: CC surface + gates + Python organs (15, threshold ≥ 4) · **K5** consumer
footprint — ships only the consumer's part, no in-tree edits fighting upstream (10) · **K6** build effort from today,
5 = already built (10) · **K7** upgrade coordinates per release, 1 = 5 (10).

| Option | K1 | K2 | K3 | K4 | K5 | K6 | K7 | Total | K4 ≥ 4? |
|---|---|---|---|---|---|---|---|---|---|
| O0 status quo: `deploy/tool.py` byte-copy carriers | 5 | 2 | 3 | 2 | 4 | 5 | 3 | 335 | no |
| O1 CC plugin + marketplace alone | 5 | 4 | 3 | 3 | 5 | 4 | 5 | 410 | no |
| O2 devcontainer Feature | 4 | 3 | 5 | 2 | 4 | 2 | 4 | 345 | no |
| O3 uv package, git-URL pin, organs only | 4 | 5 | 4 | 3 | 4 | 1 | 5 | 385 | no |
| O4 template repository / copier | 5 | 2 | 2 | 4 | 2 | 3 | 4 | 320 | yes |
| O5 git submodule of the hub | 1 | 4 | 2 | 4 | 1 | 4 | 5 | 290 | yes |
| O6 git subtree (`--squash`) of a carved-out harness dir | 5 | 3 | 5 | 4 | 2 | 2 | 5 | 385 | yes |
| O7 pre-commit hook repository alone (today's carrier) | 5 | 4 | 4 | 2 | 5 | 5 | 5 | 420 | no |
| O8 C1's mix: plugin + pre-commit `rev` + uv package (three coordinates) | 4 | 4 | 4 | 5 | 4 | 2 | 2 | 375 | yes |
| **O9 one uv package carrying all three surfaces (D1-D3)** | 4 | 5 | 4 | 5 | 4 | 1 | 5 | **415** | yes |

**Reading.** Among options that meet the threshold, **O9 415** leads O6 385, O8 375, O4 320, O5 290. The two
single-surface options that outscore it (O7 420, O1 410) are exactly the components O9 folds in: O7's pinned-gate
shape becomes D2(b), O1's plugin payload becomes D2(c). **Sensitivity:** O9 minus O8 is +20 on K2 and +30 on K7
against −10 on K6; O8 overtakes O9 only if K6 (effort) weighs more than 50, i.e. only if effort outweighs every
other criterion combined. O9 leads O6 by 30: O9 gains on K2 (+40), K5 (+20) and K4 (+15); O6 gains on K1 (+20),
K3 (+15) and K6 (+10). The order flips if in-tree copies are judged as reviewable as a lock bump (K2 equal, −40),
or if consumer edits are judged harmless *and* the payload gap closes (K5 and K4 equal, −35).

## Migration — steps with measurable exit criteria

Each step is its own lane with RED-first witnesses (ADR-108 §B). Nothing is built by this ADR.

0. **Probes before build (read/create-only).** P-1: a Claude Code plugin materialised from package data loads in
   a fresh codespace (`CLAUDE_CODE_PLUGIN_SEED_DIR` or project `.claude/`), witnessed by one hook firing. P-2:
   `uv add "dk-harness @ git+https://…#subdirectory=packages/harness"` resolves under the pinned `uv 0.11.19`
   in a fresh codespace. P-3: a lane runs with the hub unreachable after `postCreateCommand`. **Exit:** three
   receipts; any failure routes to §Flip-condition before step 1.
1. **Carve the workspace member.** Move the organs harness mode needs behind `packages/harness/` with dotted
   imports; the hub's own `scripts/` re-export or call them. ADR-101 seal admission for the directory.
   **Exit:** the hub suite is outcome-identical to its pre-move baseline under the same baseline id (ADR-121);
   `uv build` produces one wheel; `harness --version` prints the tag.
2. **First consumer, N = 1.** `corp-monorepo` pins `v1`, runs `harness install`, and runs one lane in a codespace.
   **Exit:** a consumer lane merged 3/3 with gates armed and zero hub calls at run time (plan P4 gate);
   `harness check` refuses a hand-edited materialised file.
3. **Retire carriers, one per lane.** For each of `carrier_precommit`, `carrier_floor`, `carrier_mesh`,
   `carrier_plugin`, `carrier_docs`: remove only after the consumer's equivalent comes from the artefact and the
   hub's deploy tests are re-pointed. `carrier_globalconfig` stays (user-machine-scoped, D4). **Exit:** per carrier,
   0 readers broken and the gates green.
4. **Then the other consumers** (`ai-council`, `win-tooling`, in the order the operator sets).

## Flip-condition

- **Fall back to O8 (three coordinates)** if probe P-1 fails — a plugin cannot be materialised from package data
  and still load — or if step 1 needs more than two batches to reach an outcome-identical suite. O8 keeps the
  plugin and pre-commit carriers as they are and packages only the organs.
- **Fall back to O6 (subtree)** if P-2 fails on the pinned uv, i.e. git-URL subdirectory installs are not usable
  without a uv bump the operator does not grant (ADR-106: a uv bump is its own gated change).
- **Revisit entirely** if Claude Code ships first-party project-scoped plugin pinning that a fresh cloud clone
  honours without managed settings (C1: cloud sessions apply only server-managed plugin settings today) — then
  O1 + O7 cover the payload with two already-built coordinates and the carve-out cost may not be worth paying.

## Alternatives considered

Scored in the matrix; the reason each is not chosen:

- **O0 status quo** — carries no organs (K4 = 2) and pins nothing in the consumer; the drift the v1.5.0 header
  documents is the result.
- **O1 plugin alone** — built and cheap, one version string, offline after install; but no git-hook gates and no
  locked Python dependencies, a renamed plugin without a `renames` map breaks installs, and cloud sessions ignore
  project plugin settings (C1). Kept as D2(c)'s payload shape.
- **O2 devcontainer Feature** — Codespace-native, but installs tools into an image, not governance files into a
  repository (C1); a moving major tag (`:1`) absorbs point releases silently.
- **O3 package for the organs only** — the right mechanism for half the payload; O9 is O3 extended to the other two surfaces.
- **O4 template / copier** — GitHub's template has no update channel; copier's three-way merge into consumer-edited
  files is the drift class ADR-92 avoided by single-writer carriers.
- **O5 submodule** — needs the hub remote on every fresh clone, contradicting Ch4's hub-independence; drags 37 MB of
  hub docs into each consumer.
- **O6 subtree** — hub-independent and one coordinate, but an in-tree copy invites consumer edits that conflict on
  the next `subtree pull`; the named fallback if git-URL installs fail.
- **O7 pre-commit repository alone** — already built; gates only. Its pinned shape survives inside D2(b).
- **O8 three coordinates (C1's recommendation)** — covers the payload with less restructuring, at three pins per
  release, the shape that produced the floor drift. C1 itself recorded O9 as the counter-case; the matrix prefers it.

## Consequences

- One number moves per upgrade, and the consumer's own CI proves it; drift between hub and consumer becomes a
  failing `harness check`, not an audit finding.
- The hub gains a build product: a wheel, a release tag per version (the operator tags, ADR-91), and a public API
  surface that needs backward-compatible CLIs (common rules §3).
- The carve-out is real work: 74 bare-name modules and the tests that import them; step 1 is the risk and is
  measured, not assumed.
- A consumer lane needs GitHub reachable at build time (`uv sync`, `pre-commit install`), not at run time.

## Operator decision options

These are functional (ADR-108 §A); the technical choice above stands as proposed unless he rules otherwise.

1. **Ratify the direction** — Accept (O9, one pinned artefact) · Accept with O8 (three coordinates, less
   restructuring now) · Return for a different form.
2. **Consumer order after the hub** — proposed `corp-monorepo` → `ai-council` → `win-tooling` (plan §7.2) · another order.
3. **Who approves a consumer's upgrade PR** — merged automatically when the consumer's CI is green · the operator
   reviews each · automatic for patch releases, reviewed for minor/major.
4. **May a consumer opt out of a gate** — yes, declared in its `.methodology.yaml` with a reason and a time-box (today's
   mechanism) · no, every consumer runs the full gate set.
5. **Scope** — all his repositories · only the three named consumers · exclude the five employer-heavy private repositories.
