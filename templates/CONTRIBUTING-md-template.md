---
last_reviewed: <YYYY-MM-DD>
reconciled_with: handoff-process@<version>
status: active
owner: <Rob | other>
---

# Contributing

<!-- scope: meta -->

<!-- TEMPLATE NOTE (delete when instantiating): sections marked CANONICAL below are
     synced verbatim from the hub CONTRIBUTING.md and must stay byte-identical (they are
     the universal contract). Sections marked LOCAL carry repo-specific facts — fill them
     in / set-match them per this repo. Hub-only sections (e.g. "Nightly outcome
     management") are intentionally absent; add repo-local operational sections as needed. -->

<contributor / audience line — e.g. "Sole contributor: <name>. Audience: future <name> + AI agents (Claude Code, Codex) reading for orientation.">

<!-- CANONICAL: Branch naming (sync verbatim from hub) -->
## Branch naming

<!-- scope: meta -->

```
feat/short-description
fix/short-description
docs/short-description
chore/short-description
```

Default branch: `main` (ADR-30).

Branch prefixes are `feat/ fix/ docs/ chore/` (these four only). Commit **types** follow Conventional Commits and additionally include `refactor` and `test` — commit types are **not** branch prefixes. Never commit directly to `main`: branch → `--no-ff` merge.

<!-- CANONICAL: Commit style (sync verbatim from hub) -->
## Commit style

<!-- scope: meta -->

Conventional Commits. Format: `type(scope): short imperative sentence`

```
docs(adr): add ADR-31 file naming convention
docs(journal): record session close
feat(scope): add scope tag validator enforcement
fix(validator): handle missing HEAD baseline
chore: update dev dependencies
```

Scopes are optional but use the file/folder slug when it clarifies. See recent commits in `git log` for live examples.

<!-- CANONICAL: Backlog-id references — closure grammar + the D2 cross-repo rule sync verbatim from hub; the enforcement teeth are stated at pointer level (the concrete gate script is in the LOCAL comment below, not the contract prose). -->
### Backlog-id references (forward-only index)

<!-- scope: meta -->

Commit messages **extend** Conventional Commits (they do not replace them) with an optional backlog/ADR reference, so a closure is locatable by id (ADR-65: git is the technical record, forward-indexed via this convention):

```
fix(audit): widen check-8 stamp regex [#42]      # touches backlog item 42
feat(scripts): add backlog validator, closes [#57]   # closing commit for item 57
docs(adr): ADR-65 done-item disposition           # ADR number is itself the index
```

- **Touching** a backlog item: append `[#<id>]` to the summary.
- **Closing** a backlog item: add `closes [#<id>]` (summary or body) — pairs with the item leaving `BACKLOG.md` in the same or a following commit.
- **`closes` vs `advances`:** use `closes [#<id>]` on the commit that **finishes** an item — not `advances [#<id>]`. `advances` records intermediate progress only: the item stays open in `BACKLOG.md` **and** invisible to the closure detector (which keys on `closes`), so it silently accumulates as done-but-open and must be closed manually (this is what forced the manual close of #73). A multi-commit arc may use `advances` along the way, but the commit that completes the work must use `closes`.
- `<id>` is the entry's stable `id:` field (monotonic, never reused — PLAYBOOK §10 schema).
- **Cross-repo references are repo-qualified.** A bare `[#<id>]` denotes a task in THIS repo only. To reference another fleet repo's backlog item, qualify it: `hub#<id>`, `ai#<id>`, `corp#<id>`. (Operator ruling, content-parity inventory D2 / #331 — qualified-refs chosen over a global allocator. Automated enforcement lands with #328; this is the convention it will check.)

This indexes commits **going forward only.** Git history is immutable — **historical commits are never rewritten** (ADR-65). Pre-convention closures are located via the SHAs already embedded in retired entries (preserved in the one-time migration JOURNAL map).

**Enforced by the carried `commit-msg` gate** (where installed): a commit that removes a `- [#id]` task from `BACKLOG.md` without referencing that id (`[#id]` or `closes [#id]`) is rejected. A reworded task (id present before and after) does not trigger. Install the commit-msg stage once per machine:

```
pre-commit install --hook-type commit-msg
```

<!-- LOCAL: the concrete gate script in this repo is `scripts/check_backlog_commit_msg.py` (pre-commit `commit-msg` stage). -->

**"What's been implemented" query.** Because done tasks **leave** `BACKLOG.md` (ADR-65) and git is the implementation record, the list of completed tasks with their implementing commits is:

```
git log --grep 'closes \[#'
```

This is the detailed implementation history the active file deliberately does not carry.

## Pre-commit setup

<!-- scope: meta -->

Install once per machine (adjust the dev-requirements path to this repo):

```
pip install -r config/requirements-dev.txt
pre-commit install
```

Run manually at any time:

```
pre-commit run --all-files
```

## Validators

<!-- scope: meta -->

<!-- LOCAL: set-match this roster to THIS repo's live `.pre-commit-config.yaml`. The hook
     set is repo-local — hub-only hooks (roster-freshness, claude-rosters-freshness,
     audit-index-freshness, validate-hermetization, intake-index-freshness,
     backlog-filing-backpressure, …) do NOT ship to every consumer. Verify the id set
     matches `.pre-commit-config.yaml` and the repo's CLAUDE.md §9. -->

| Hook | Stage | What it does |
|------|-------|--------------|
| `<hook-id>` | `<commit \| commit-msg \| pre-push>` | `<one-line purpose>` |

## ADR process

<!-- scope: meta -->

Decisions that bind future sessions live in `docs/decisions/ADR-NN-topic.md`.

- Numbering: next integer after highest existing ADR
- Filename: `ADR-NN-short-kebab-topic.md`
- Status values: `Accepted | Superseded | Withdrawn`
- Minor prescription drift → amend in-place (add dated `## Amendment YYYY-MM-DD` section)
- Intent change or reversal → new ADR or AI Council reopen

<!-- LOCAL: point at this repo's foundational ADRs for style reference (e.g. "See ADR-NN through ADR-NN"). -->

## Handoff process

<!-- scope: meta -->

Protocol: the hub methodology protocol `HANDOFF_PROCESS.md` (read at the hub `.dev-knowledge/protocols/` set; hub-pointer, never copied into a consumer) — **v5** (stamp `v<version>`). CC owns the handoff: it emits a lean **residual** + a **probe manifest** under `docs/handoffs/<slug>/`, and a fresh browser chat boots from the thin hub protocol `HANDOFF_BOOT.md` (same hub `.dev-knowledge/protocols/` location). The ADR-36 read-only contract holds: a handoff never writes to a target repo.

Claude Code command: **`/handoff`** — `create handoff for <repo>` emits the residual + probe manifest and points the next browser at the thin boot; `complete handoff for <repo>` cross-checks repo state and finalizes.

`BACKLOG.md` (root): cross-session pending items per ADR-41. Universal mandate (ADR-38 amendment A5 — every repo, no tier gating). Review before chartering new session.

<!-- CANONICAL: Definition of done — pointer level; the concrete Stop-hook script is in the LOCAL comment below (do not hard-code hub-local paths). -->
## Definition of done (session close)

<!-- scope: meta -->

The hub methodology protocol `DEFINITION_OF_DONE.md` (read at the hub `.dev-knowledge/protocols/` set; hub-pointer, never copied into a consumer) is the single source of truth for what "done" means at session close (ADR-85): a session that produces commits adds a `JOURNAL.md` entry naming ≥1 commit SHA from this arc (**hard-gated**), and should update `BACKLOG.md` with a structural marker (**advisory** in v1). It is enforced **mechanically and deterministically** by the carried session-end Stop-hook (no LLM in the gate) — and the only escape is `/override [reason]`. The other living docs (`ARCHITECTURE`, `VISION`, `LESSONS`, this file) are "update when materially affected", not per-session-gated. Pointer only — the rules live in that file, not here (resident copies drift).

<!-- LOCAL: the concrete Stop-hook script in this repo is `scripts/session_end_backpressure.py`. -->
