# Contributing

<!-- scope: meta -->

Sole contributor: Rob Dwornik. Audience: future Rob + AI agents (Claude Code, Codex) reading for orientation.

## Branch naming

<!-- scope: meta -->

```
feat/short-description
fix/short-description
docs/short-description
chore/short-description
```

Default branch: `main` (ADR-30). Never commit directly to `main`. Branch → commit → merge.

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
- `<id>` is the entry's stable `id:` field (monotonic, never reused — PLAYBOOK §10 schema).

This indexes commits **going forward only.** Git history is immutable — **historical commits are never rewritten** (ADR-65). Pre-convention closures are located via the SHAs already embedded in retired entries (preserved in the one-time migration JOURNAL map).

## Pre-commit setup

<!-- scope: meta -->

Install once per machine:

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

One auto-format hook runs on commit:

| Hook | What it does |
|------|--------------|
| `normalize-dated-headers` | Rewrites dated-log entry headers to canonical `### YYYY-MM-DD` form. Idempotent. Auto-format style: rewrites; never fails. |

Run standalone (e.g. to clean up before commit):

```
python scripts/normalize_headers.py LESSONS.md JOURNAL.md
```

## ADR process

<!-- scope: meta -->

Decisions that bind future sessions live in `docs/decisions/ADR-NN-topic.md`.

- Numbering: next integer after highest existing ADR
- Filename: `ADR-NN-short-kebab-topic.md`
- Status values: `Accepted | Superseded | Withdrawn`
- Minor prescription drift → amend in-place (add dated `## Amendment YYYY-MM-DD` section)
- Intent change or reversal → new ADR or AI Council reopen

See ADR-27 through ADR-41 for style reference.

## Handoff process

<!-- scope: meta -->

Protocol: `protocols/HANDOFF_PROCESS.md` (v2.0, 2026-04-28 — folder format per ADR-32; ADR-37 two-phase overlay pending — P1 in BACKLOG.md).

Trigger phrase (browser chat): `wygeneruj handoff`
Claude Code: `/session-summary`

`BACKLOG.md` (root): cross-session pending items per ADR-41. Universal mandate (ADR-38 amendment A5 — every repo, no tier gating). Review before chartering new session.
