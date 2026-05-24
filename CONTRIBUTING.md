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
