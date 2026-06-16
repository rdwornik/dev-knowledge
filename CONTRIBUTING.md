---
last_reviewed: 2026-06-16
status: active
owner: Rob
---

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
- **`closes` vs `advances`:** use `closes [#<id>]` on the commit that **finishes** an item — not `advances [#<id>]`. `advances` records intermediate progress only: the item stays open in `BACKLOG.md` **and** invisible to the closure detector (which keys on `closes`), so it silently accumulates as done-but-open and must be closed manually (this is what forced the manual close of #73). A multi-commit arc may use `advances` along the way, but the commit that completes the work must use `closes`.
- `<id>` is the entry's stable `id:` field (monotonic, never reused — PLAYBOOK §10 schema).

This indexes commits **going forward only.** Git history is immutable — **historical commits are never rewritten** (ADR-65). Pre-convention closures are located via the SHAs already embedded in retired entries (preserved in the one-time migration JOURNAL map).

**Enforced by a `commit-msg` hook.** `scripts/check_backlog_commit_msg.py` (pre-commit `commit-msg` stage) **fails any commit that removes a `- [#id]` task from `BACKLOG.md` without referencing that id** (`[#id]` or `closes [#id]`) in the message. A reworded task (id present before and after) does not trigger. Install it once per machine alongside the standard hooks:

```
pre-commit install --hook-type commit-msg
```

**"What's been implemented" query.** Because done tasks **leave** `BACKLOG.md` (ADR-65) and git is the implementation record, the list of completed tasks with their implementing commits is:

```
git log --grep 'closes \[#'
```

This is the detailed implementation history the active file deliberately does not carry.

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

Pre-commit hooks (`.pre-commit-config.yaml`):

| Hook | Stage | What it does |
|------|-------|--------------|
| `normalize-dated-headers` | commit | Rewrites dated-log entry headers to canonical `### YYYY-MM-DD` form. Idempotent. Auto-format style: rewrites; never fails. |
| `codemap-freshness` | commit | Checks the ARCHITECTURE.md codemap block is current vs `scripts/`. |
| `toc-freshness` | commit | Fail-on-stale check that ARCHITECTURE.md's TOC matches its headers. Regenerate: `python -m scripts.toc.cli generate ARCHITECTURE.md --write`. |
| `toc-freshness-playbook` | commit | Same check for `protocols/PLAYBOOK.md`'s TOC. Regenerate: `python -m scripts.toc.cli generate protocols/PLAYBOOK.md --write`. |
| `validate-backlog` | commit | Validates the BACKLOG.md story-map structure (ADR-66). |
| `audit-health` | commit | Runs `audit.py health` (the self-conformance checks incl. canonical-file freshness). **FAIL-level findings block the commit; WARN-level only inform.** ~1.4s. Bypass: `--no-verify`. |
| `ruff` | commit | Lint gate — `ruff check` (version-pinned >=0.15.5, `language: system`). Blocks on violations. [#13] closed. |
| `backlog-id-on-close` | commit-msg | Requires `[#id]` / `closes [#id]` when a commit removes a `- [#id]` task. |

`audit.py health` (the gate above) is also runnable standalone for an on-demand sweep: `python scripts/audit.py health`. It runs the self-conformance checks incl. the canonical-file **freshness** check (`last_reviewed` staleness; see PLAYBOOK); FAIL blocks a commit, WARN (e.g. the 30-day freshness backstop) only informs.

Run the auto-format hook standalone (e.g. to clean up before commit):

```
python scripts/normalize_headers.py LESSONS.md JOURNAL.md
```

## Nightly outcome management

<!-- scope: meta -->

The nightly conformance Routine (cloud, read-only) opens a PR on
`claude/conformance-YYYY-MM-DD` that adds exactly one digest file,
`docs/audits/YYYY-MM-DD-conformance-nightly-digest.md`, and never auto-merges. The
repo's first GitHub Action (`.github/workflows/nightly-conformance-triage.yml`) handles
the morning so the operator touches only findings:

- **Clean night** (`survived=0` in the digest's machine-readable counts marker
  `<!-- counts: raw=N survived=N killed=N -->`) → the PR is squash-merged automatically and its
  branch deleted. No operator action.
- **Findings night** (`survived=N`, N>0 in the counts marker) → the digest is squash-merged too (it is
  the record) **and** a `nightly-triage` Issue `Nightly triage <date> — <N> survivor(s)` is
  opened with the digest's Findings-by-Severity + Next-Actions sections and a link to the
  merged digest.
- **Anomalous PR** (anything other than exactly one ADDED digest file) → **nothing is
  merged**; an `Anomalous nightly PR <date> — guard failed` Issue is opened listing the
  changed files, and the PR is left open for human review.

The **diff guard** is the safety gate: the Action merges only when
`git diff --name-status base...head` is exactly one `A` line matching
`docs/audits/*-conformance-nightly-digest.md` — a mislabeled or lying digest is therefore at
worst a document on `main`, never code. **Where to look:** open `nightly-triage` Issues are
surfaced at session start by `scripts/surface_triage.ps1` (a `[triage] …` line) and live in
the repo's Issues tab.

**Why the `.js` workflow exists, and when it runs as a spec.** The nightly run is
defined by `.claude/workflows/conformance-hub.js` — but the native `Workflow` launcher
is **not enabled in the cloud runtime** (re-probed; still unavailable). So each nightly
Routine **attempts the native launcher first and falls back to reading the `.js` as a
*specification*** — orchestrating its stages by hand via read-only Explore agents
(spec-orchestration). Doctrine: **native-attempt-first, with a nightly re-probe**; the
digest reports which path ran, and execution swaps back to native automatically when the
platform re-enables it. The load-bearing consequence: any guarantee written as in-script
code is **inert on the fallback path** (the `.js` is read, not run) — which is exactly
why the survivor-count backstop below lives on the **executing path** (the Action's
fail-closed parser), not inside the script. Full standard: PLAYBOOK "Routine/night
deployment standard"; ADR-72 (cloud self-containment).

**Residual risk:** the survivor count is read from a code-owned machine-readable marker in the
digest body (`<!-- counts: raw=N survived=N killed=N -->`, written by `conformance-hub.js`; the
free-form PR title and the agent's prose are not trusted) and the parse **fails closed** — a
missing or unparseable marker opens an Issue and blocks the merge rather than guessing. **Layer-2 note:** this Action runs in
GitHub CI and manages the hub's *own* review-output PRs only; it does not orchestrate child
repos, and `surface_triage.ps1` is read-only — so the Layer-2 "validators only / never
executes cross-repo" invariant still holds.

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

Protocol: `protocols/HANDOFF_PROCESS.md` — **v5** (stamp v5.1, *stable*; ADR-82, operator-ratified 2026-06-11 per #149, amended 2026-06-16 for the v5.1 architect strategic supplement). v5 inverts the v4 model: instead of a browser-delivered 8-file bundle, **CC owns the handoff** — it emits a lean **residual** + a **probe manifest** under `docs/handoffs/<slug>/`, and a fresh browser chat boots from the thin `protocols/HANDOFF_BOOT.md`. Verification has teeth: the probes force CC to re-derive every load-bearing fact from the live primary source at check-time. v4.4 is archived at `protocols/archive/HANDOFF_PROCESS_v4.4.md`. The ADR-36 read-only contract holds: a handoff never writes to a target repo.

Claude Code command: **`/handoff`** — `create handoff for <repo>` has CC emit the **residual** + **probe manifest** under `docs/handoffs/<slug>/` and point the next browser at the thin boot (`protocols/HANDOFF_BOOT.md`); `complete handoff for <repo>` cross-checks repo state and finalizes. `<repo>` defaults to `.dev-knowledge` (self-handoff). Not `/session-summary` — that is a separate session-summary command, not the handoff generator.

`BACKLOG.md` (root): cross-session pending items per ADR-41. Universal mandate (ADR-38 amendment A5 — every repo, no tier gating). Review before chartering new session.

## Definition of done (session close)

<!-- scope: meta -->

`protocols/DEFINITION_OF_DONE.md` is the single source of truth for what "done" means at session close (ADR-85): a session that produces commits adds a `JOURNAL.md` entry naming ≥1 commit SHA from this arc (**hard-gated**), and should update `BACKLOG.md` with a structural marker (**advisory** in v1). It is enforced **mechanically and deterministically** by the session-end Stop-hook (`scripts/session_end_backpressure.py`) — no LLM in the gate — and the only escape is `/override [reason]`. The other living docs (`ARCHITECTURE`, `VISION`, `LESSONS`, this file) are "update when materially affected", not per-session-gated. Pointer only — the rules live in that file, not here (resident copies drift).
