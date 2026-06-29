# ADR-91: Methodology corpus versioning — semver + git-tag release marker

<!-- scope: meta -->

**Status:** Accepted (ratified by merge 2026-06-29; baseline release `v1.0.0` tagged)
**Date:** 2026-06-27
**Decision tier:** Doctrine (a new corpus-wide versioning model — establishes semver + a git-tag release marker for the methodology corpus). Records the architect's design; **the operator ratifies by merge** (this ADR is not self-accepted). Path-A direct ADR, no Council.
**Deliberation basis:** the 2026-06-27 deployment-machinery recon (operator↔architect session) established the version axis is greenfield — no `VERSION` file, no methodology `CHANGELOG`, no release tag; the five carriers each have a different freshness model and no single version spans them; a consumer's only durable committed "what hub state I consume" record today is the pre-commit `rev:` SHA, and `ecosystem/*/state.yaml` is gitignored. This ADR formalizes the versioning doctrine that recon's findings call for.
**Related:** ADR-65 (git-is-the-changelog — BACKLOG numbers forward-index git history; this ADR adds a release **marker**, not a changelog file); ADR-71 (the pre-commit `repo:/rev:` consume-pin — the only durable per-consumer consume-record today); ADR-70/73/78/79 (the carrier set this version must span); ADR-88 (file-oriented dependency management — *declare what you cannot compute*; the deferred per-consumer version record is a declared edge); ADR-86/ADR-80 (committed-generated zones — relevant to where the deferred record/surface eventually lives).
**Decommission:** none.
**Source:** the 2026-06-27 recon findings (version-axis-greenfield) + the architect's corpus-versioning design. The deferred per-consumer record location is an explicit Open Question (below), **not** settled here.

## Context

The methodology corpus has **no version concept**. A consumer repo cannot be pinned to — or told it is behind — a methodology *release*, because no release line exists.

- **The version axis is greenfield.** There is no `VERSION` file and no methodology `CHANGELOG` (the latter was deliberately removed 2026-05-16; git is the changelog). The only git tag in the hub is `backlog-migration-2026-06-01`, a one-off migration marker, not a release line.
- **The version-like fields that exist do not version the corpus.** `plugins/tier1-lifecycle/.claude-plugin/plugin.json` `version: 0.1.10` versions the *plugin*, not the corpus. Per-document frontmatter versions (`VISION.md` 1.0, `CLAUDE.md` 2.x) are *doc-versions*, not a corpus release.
- **Five carriers, five freshness models, no spanning version.** The methodology ships via five carriers — L0 `~/.claude` · the `tier1-lifecycle` plugin · pre-commit `rev`-pin · the child floor + `.sha256` · the browser bundle — each with a *different* freshness/update model, and **no single version spans them**. That missing spanning version is the gap this ADR fills.
- **A consumer's only durable committed consume-record today** is the pre-commit `rev:` SHA in its own `.pre-commit-config.yaml` (e.g. `ai-council` pins hub `69558c7`). It is a git-SHA for *doc-tooling*, not a methodology release, and it covers one carrier only. `ecosystem/*/state.yaml` is **gitignored** → non-durable, so it cannot hold a reviewable version record.
- **The methodology already treats git as the changelog.** BACKLOG numbers + the CONTRIBUTING commit convention make `git log` the legible change history (ADR-65). Therefore versioning must add a **release marker, not a changelog file** — re-introducing a `CHANGELOG`/`VERSION` file would contradict that doctrine.

## Decision

**Establish semantic versioning for the methodology corpus, marked by a git tag on the hub. No changelog or version file is introduced.**

1. **The versioned unit is the methodology corpus** — `protocols/`, the accepted ADRs, `templates/`, the enforcement engine (`audit.py` + its validator modules), and the carrier contracts. It is explicitly **not** per-repo work, and not any single carrier.

2. **A release is marked by a git tag** on the hub, semver `vMAJOR.MINOR.PATCH` (e.g. `v1.0.0`). The changelog between releases is `git log vX..vY`, made legible by BACKLOG numbers — **no `CHANGELOG`/`VERSION` file is introduced** (consistent with git-is-the-changelog, ADR-65).

3. **Semver rules (major-ness tracks blocking-ness):**
   - **major** — a consumer must migrate: a new *blocking* gate, or a changed/removed carrier contract or a capability a consumer depends on.
   - **minor** — additive / optional: a new check, capability, or template a consumer adopts at will.
   - **patch** — a fix with no contract change.
   The alignment is deliberate: breaking changes are exactly the blocking-gate class consumers adopt deliberately, so they are the changes that force a major bump.

4. **Component versions nest under the corpus release.** The plugin (`0.1.10`), the floor templates, and any other independently-versioned component are **pinned by** a corpus release: a release records which component versions it includes. Bumping a component implies at least a corpus patch (or minor, if the component change is additive-capability).

5. **Baseline `v1.0.0`.** Propose `v1.0.0` as the first tagged release, placed on `main` at ratification. **CC does not create the tag** — tagging is the operator's release act. The proposed command, for the operator to run **after merging this ADR** (tagging the ratification-merge HEAD; substitute the exact SHA if a different commit is preferred — the current pre-ADR `main` HEAD is `a32f0cc`):

   ```
   git tag -a v1.0.0 -m "Methodology corpus v1.0.0 — baseline release (ADR-91)"
   git push origin v1.0.0
   ```

## Record-home decision (resolved in this arc)

The first Open Question — **where the durable per-consumer deployed-methodology-version record lives** — is **resolved**: a dedicated committed registry **`ecosystem/deployed-versions.yaml`**, modeled 1:1 on the existing `tool-versions.yaml` durable-version pattern (committed · written-by-command · read-by-a-check).

- **NOT `ecosystem/index.yaml`.** A live read refuted that candidate: `index.yaml` is a **derived rollup** — `audit.py::regenerate_index()` rewrites it wholesale from the gitignored per-repo `state.yaml` on every `audit.py run` / `registry update` (its docstring: *"do not edit by hand — manual edits are lost on the next run"*). A field written there by the deploy-runbook would be **silently clobbered**.
- **NOT `state.yaml`** — gitignored → non-durable (already excluded in Context).
- **A dedicated file, not folded into `tool-versions.yaml`** — separate writer (the deploy-runbook vs `/changelog-review`) and separate per-deploy lifecycle; same *pattern*, new *axis* (repo-keyed deployed-corpus-version vs tool-keyed reviewed-changelog-version), so not a literal-duplicate fold.

**Built in this arc (the READ side):** the registry slot (`ecosystem/deployed-versions.yaml`, values **unset/`null`** — no release tagged yet), the reader (`audit.py` check `deployed_methodology_version`, surfaced per-repo through `fleet_health`), and the operational doctrine (PLAYBOOK Ch6). The second Open Question — **`fleet_health` version-surfacing** — is addressed in substance by that reader check: the version-aware per-repo signal now exists, superseding a raw-commit-count indicator.

**Remaining (separate piece, deliberately NOT built here):** the **deploy-runbook** — the *writer* that populates `deployed_methodology_version` at deploy time. Until it runs (and a release is tagged), every repo's field stays `null` and the reader reports `n/a` (the expected pre-deploy state).

## Rejected alternatives

- **A `VERSION` / `CHANGELOG` file.** Rejected — it duplicates the change history git already holds (ADR-65) and adds a file to keep in sync. The git tag is the release marker; `git log vX..vY` + BACKLOG numbers is the changelog.
- **Versioning each carrier independently (no corpus version).** Rejected — it perpetuates the five-freshness-models gap. A consumer would still have no single number to pin to. The corpus version is the spanning version the carriers lack; component versions nest under it (Decision 4).

## Consequences

- A single methodology semver becomes the **spanning version** the five carriers lacked.
- With the record-home decided (`ecosystem/deployed-versions.yaml`) and the reader built, each repo's deployed version is **recorded + surfaced**; drift ("repo X is two majors behind") becomes detectable once the deploy-runbook populates the field.
- Releases become legible via **git tags + BACKLOG numbers** — no new changelog mechanism is added; git-is-the-changelog is preserved.
- The remaining piece is the **deploy-runbook** (the writer); the record slot + reader + doctrine land in this arc.

## Links

- The 2026-06-27 deployment-machinery recon (version-axis-greenfield finding) — the empirical basis.
- ADR-65 — git-is-the-changelog (BACKLOG numbers forward-index git history).
- ADR-71 — the pre-commit `repo:/rev:` consume-pin (today's only durable per-consumer consume-record).
- ADR-88 — file-oriented dependency management (declared-edge paradigm; the deferred version record is a declared edge under it).
- ADR-70 / ADR-73 / ADR-78 / ADR-79 — the carrier set the corpus version must span.
