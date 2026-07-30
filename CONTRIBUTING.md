---
last_reviewed: 2026-07-31
reconciled_with: handoff-process@6.0
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

Default branch: `main` (ADR-30).

Branch prefixes are `feat/ fix/ docs/ chore/` (these four only). Commit **types** follow Conventional Commits and additionally include `refactor` and `test` — commit types are **not** branch prefixes. Never commit directly to `main`: branch → `--no-ff` merge.

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
- **Cross-repo references are repo-qualified.** A bare `[#<id>]` denotes a task in THIS repo only. To reference another fleet repo's backlog item, qualify it: `hub#<id>`, `ai#<id>`, `corp#<id>`. (Operator ruling, content-parity inventory D2 / #331 — qualified-refs chosen over a global allocator. Automated enforcement lands with #328; this is the convention it will check.)

This indexes commits **going forward only.** Git history is immutable — **historical commits are never rewritten** (ADR-65). Pre-convention closures are located via the SHAs already embedded in retired entries (preserved in the one-time migration JOURNAL map).

**Enforced by a `commit-msg` hook.** `scripts/check_backlog_commit_msg.py` (pre-commit `commit-msg` stage) **fails any commit that removes a `- [#id]` task from `BACKLOG.md` without referencing that id** (`[#id]` or `closes [#id]`) in the message. A reworded task (id present before and after) does not trigger. Install it once per machine alongside the standard hooks:

```
uv run pre-commit install --hook-type commit-msg
```

**"What's been implemented" query.** Because done tasks **leave** `BACKLOG.md` (ADR-65) and git is the implementation record, the list of completed tasks with their implementing commits is:

```
git log --grep 'closes \[#'
```

This is the detailed implementation history the active file deliberately does not carry.

## Pre-commit setup

<!-- scope: meta -->

Install once per machine (uv toolchain, ADR-106 / [#432] — uv itself is pinned via `[tool.uv] required-version` in `pyproject.toml`):

```
uv sync --locked
uv run pre-commit install
```

Run manually at any time:

```
uv run pre-commit run --all-files
```

## Validators

<!-- scope: meta -->

Pre-commit hooks (`.pre-commit-config.yaml`):

| Hook | Stage | What it does |
|------|-------|--------------|
| `normalize-dated-headers` | commit | Rewrites dated-log entry headers to canonical `### YYYY-MM-DD` form. Idempotent. Auto-format style: rewrites; never fails. |
| `codemap-freshness` | commit | Checks the ARCHITECTURE.md compact-text codemap is current vs `scripts/` (compact text since the ADR-51 amendment 2026-07-05; gate retained). |
| `toc-freshness-playbook` | commit | Staleness check for `protocols/PLAYBOOK.md`'s TOC. Regenerate: `uv run python -m scripts.toc.cli generate protocols/PLAYBOOK.md --write`. |
| `roster-freshness` | commit | Regen-and-diff gate for `.claude/methodology-roster.md` vs `deploy/manifest-v*.yaml` (`gen_methodology_roster.py --check`); blocks a hand-edited or manifest-stale roster. Hub-only ([#244] P3). |
| `claude-rosters-freshness` | commit | Regen-and-diff gate for the two `@`-imported CLAUDE.md fragments `.claude/generated/{commands-repo,recent-adrs}.md` (`gen_claude_rosters.py --check`); fires on the command files / ADR headers / the fragments. Hub-only ([#258] phase-2). |
| `audit-index-freshness` | commit | Regen-and-diff gate for the generated `docs/audits/README.md` index vs `docs/audits/*.md` (`gen_audit_index.py --check`); shape-agnostic. Hub-only. |
| `validate-hermetization` | commit | ADR-101 tree-seal refusal gate, prospective-only on staged ADDs: blocks a new unsanctioned Tier-1 top-level dir/file-class or `docs/<genre>/` folder (Rule A) or an off-grammar `docs/audits/*.md` name (Rule B). `scripts/validate_hermetization.py`, bypass `--no-verify`. Hub-only. |
| `intake-index-freshness` | commit | Regen-and-diff gate for the status-grouped Contents block in `docs/intake/README.md` vs `docs/intake/*.md` frontmatter `status:` (`gen_intake_index.py --check`). Hub-only. |
| `validate-backlog` | commit | Validates the BACKLOG.md story-map structure (ADR-66). |
| `audit-health` | commit | Runs `audit.py health` (the self-conformance checks incl. canonical-file freshness). **FAIL-level findings block the commit; WARN-level only inform.** Runtime scales with the check registry. Bypass: `--no-verify`. |
| `ruff` | commit | Lint gate — `ruff check` (fleet-canonical pinned-rev `astral-sh/ruff-pre-commit` @ v0.15.5, rev == the `pyproject.toml` required-version floor). Blocks on violations. [#13] closed. |
| `coherence-nudge` | commit | **Non-blocking** nudge: a registered spec changed without a version bump → stdout nudge + `logs/COHERENCE-NUDGE.log`; always exits 0 (pairs with the `reconciled_versions` audit check). |
| `backlog-id-on-close` | commit-msg | Requires `[#id]` / `closes [#id]` when a commit removes a `- [#id]` task. |
| `backlog-filing-backpressure` | commit-msg | Add-side sibling of `backlog-id-on-close`: a commit that ADDS a new BACKLOG task id must carry a `kill-candidates:` line (≥1 existing `#id`, or `none — <reason>`) — BLOCK if absent. `scripts/check_backlog_filing.py`, proposals only. Hub-only. |
| `block-ff-push` | pre-push | Refuses a push placing a non-merge commit on `main`'s first-parent spine (a direct-to-`main` commit or a true FF merge); a `--no-ff` merge passes. Hub-only, fail-soft, bypass `git push --no-verify`. **Activate once per machine: `uv run pre-commit install --hook-type pre-push`** (`default_install_hook_types` only wires it on a fresh install). |

`audit.py health` (the gate above) is also runnable standalone for an on-demand sweep: `uv run python scripts/audit.py health`. It runs the self-conformance checks incl. the canonical-file **freshness** check (`last_reviewed` staleness; see PLAYBOOK); FAIL blocks a commit, WARN (e.g. the 30-day freshness backstop) only informs.

Run the auto-format hook standalone (e.g. to clean up before commit):

```
uv run python scripts/normalize_headers.py LESSONS.md JOURNAL.md
```

## Nightly outcome management

<!-- scope: meta -->

The nightly conformance Routine (cloud, read-only) opens a PR on
`claude/conformance-YYYY-MM-DD` that adds exactly one digest file,
`docs/audits/YYYY-MM-DD-conformance-nightly-digest.md`, and never auto-merges. The
repo's first GitHub Action (`.github/workflows/nightly-conformance-triage.yml`) handles
the morning so the operator touches only findings:

- **Clean night** (`survived=0` in the digest's machine-readable counts marker
  `<!-- counts: raw=N survived=N killed=N -->`) → the digest is **diverted** onto
  `automation/conformance-digest` and the PR is **closed** (its `claude/conformance-YYYY-MM-DD`
  branch deleted) — never merged to `main`. No operator action.
- **Findings night** (`survived=N`, N>0 in the counts marker) → the digest is **diverted** onto
  `automation/conformance-digest` too (it is the record, on the branch) **and** a `nightly-triage`
  Issue `Nightly triage <date> — <N> survivor(s)` is opened with the digest's Findings-by-Severity
  + Next-Actions sections and a link to the diverted digest (on the automation branch).
- **Anomalous PR** (anything other than exactly one ADDED digest file) → **nothing is
  recorded**; an `Anomalous nightly PR <date> — guard failed` Issue is opened listing the
  changed files, and the PR is left open for human review.

The **diff guard** is the safety gate: the Action **diverts** the digest only when
`git diff --name-status base...head` is exactly one `A` line matching
`docs/audits/*-conformance-nightly-digest.md` — a mislabeled or lying digest is therefore at
worst a stray document on `automation/conformance-digest`, never code and never on `main`. **Where to look:** open `nightly-triage` Issues are
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
missing or unparseable marker opens an Issue and blocks the divert rather than guessing. **Layer-2 note:** this Action runs in
GitHub CI and manages the hub's *own* review-output PRs only; it does not orchestrate child
repos, and `surface_triage.ps1` is read-only — so the Layer-2 "validators only / never
executes cross-repo" invariant still holds.

## ADR process

<!-- scope: meta -->

Decisions that bind future sessions live in `docs/decisions/ADR-NN-topic.md`.

- Numbering: next integer after highest existing ADR
- Filename: `ADR-NN-short-kebab-topic.md`
- Status values: `Proposed | Accepted | Superseded | Deprecated` (reconciled against
  on-disk reality 2026-07-23, [#398] — operator-ruled; the never-used `Withdrawn`
  dropped, the lived-but-undeclared `Proposed` and `Deprecated` admitted)
- Status lifecycle: `Proposed → Accepted` by editing the Status line **in place at
  ratification** (ADR-94 Pattern B — the status line is metadata, not decision
  content); `Superseded`/`Deprecated` are terminal — a terminal ADR relocates
  byte-identical to `docs/decisions/archive/` (operator ruling 2026-07-22)
- Legacy off-enum statuses on disk (named carve-outs, **not** precedent — retro-
  normalization is deferred to [#242] with reasons): ADR-88/89 frozen `Proposed`
  ratified by in-file markers (ADR-94's explicit operator-gated deferral); ADR-82
  frozen `Proposed` canonical-by-waiver since 2026-06-11 (same class, [#242]'s
  retro-normalize domain per the 2026-07-22 night-batch audit P2b); ADR-45
  `Explored, not adopted` + ADR-46/47 `Partially superseded` (any ADR-45 flip is
  additionally gated by [#362]'s dropped-rules disposition)
- Minor prescription drift → amend in-place (add dated `## Amendment YYYY-MM-DD` section)
- Intent change or reversal → new ADR or AI Council reopen

See ADR-27 through ADR-41 for style reference.

## Handoff process

<!-- scope: meta -->

Protocol: `protocols/HANDOFF_PROCESS.md` — **v6** (stamp v6.0, *stable*; ADR-82, operator-ratified 2026-06-11 per #149, amended 2026-06-16 for the v5.1 architect strategic supplement, 2026-06-17 for the v5.2 always-generated supplement file, 2026-06-25 for the v5.3 §5 probe-manifest consolidation, 2026-07-05 for the v5.4 §5 structural anti-bluff + §13 generator note, 2026-07-05 for the v5.5 §14 epic-lane handoffs — EPIC + EPIC RETURN, ADR-97, 2026-07-06 for the v5.6 §14a execution-MODE item, 2026-07-07 for the v5.7 §16 functional/intake mode + §14 developer alias, ADR-98, and **2026-07-31 for the v6.0 one-round-trip boot** — one CC-side command (`/handoff-verify`) runs the whole live gate and emits ONE evidence block the operator pastes once, plus the P0 standing-topic legs, the `Destination` boot-header row + its P3 comparison, the `HANDOFF_BOOT` byte budget, and the A11 generation/verification guards; intake #19 §B(b), rulings R1..R7, built under [#446]). v6 keeps the v5 model:  instead of a browser-delivered 8-file bundle, **CC owns the handoff** — it emits a lean **residual** + a **probe manifest** under `docs/handoffs/<slug>/`, and a fresh browser chat boots from the thin `protocols/HANDOFF_BOOT.md`. Verification has teeth: the probes force CC to re-derive every load-bearing fact from the live primary source at check-time. v4.4 is archived at `protocols/archive/HANDOFF_PROCESS_v4.4.md`. The ADR-36 read-only contract holds: a handoff never writes to a target repo.

Claude Code command: **`/handoff`** — `create handoff for <repo>` has CC emit the **residual** + **probe manifest** under `docs/handoffs/<slug>/` and point the next browser at the thin boot (`protocols/HANDOFF_BOOT.md`); `complete handoff for <repo>` cross-checks repo state and finalizes. `<repo>` defaults to `.dev-knowledge` (self-handoff). Not `/session-summary` — that is a separate session-summary command, not the handoff generator.

`BACKLOG.md` (root): cross-session pending items per ADR-41. Universal mandate (ADR-38 amendment A5 — every repo, no tier gating). Review before chartering new session.

## Definition of done (session close)

<!-- scope: meta -->

`protocols/DEFINITION_OF_DONE.md` is the single source of truth for what "done" means at session close (ADR-85): a session that produces commits adds a `JOURNAL.md` entry naming ≥1 commit SHA from this arc (**hard-gated**), and should update `BACKLOG.md` with a structural marker (**advisory** in v1). It is enforced **mechanically and deterministically** by the session-end Stop-hook (`scripts/session_end_backpressure.py`) — no LLM in the gate — and the only escape is `/override [reason]`. The other living docs (`ARCHITECTURE`, `VISION`, `LESSONS`, this file) are "update when materially affected", not per-session-gated. Pointer only — the rules live in that file, not here (resident copies drift).
