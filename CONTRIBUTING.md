---
last_reviewed: 2026-08-07
reconciled_with: handoff-process@6.1.0
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

Branch prefixes are `feat/ fix/ docs/ chore/` — **author-chosen branches, these four only** — **plus four machine-produced lane prefixes: `worktree-<name>` (native parallel-session worktrees, `claude --worktree` / EnterWorktree), `epic/<slug>` (root-provisioned epic lanes), `claude/<slug>` (Anthropic cloud-session lanes), and `automation/<slug>` (organ-produced replication lanes — admitted 2026-08-06 by architect ruling, register `protocols/STANDING_RULINGS.md` B5). Lane branches are never self-merged and never author-invented; a new machine-produced lane prefix enters this enum only via a recorded ruling (never silently) — the enum stays the checkable surface.** Commit **types** follow Conventional Commits and additionally include `refactor` and `test` — commit types are **not** branch prefixes. Never commit directly to `main`: branch → `--no-ff` merge.

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
| `check-seal-identity` | commit | Bundle seal-identity gate over staged `docs/handoffs/**`: runs `gen_handoff.verify_seal_identity` (reused, not reimplemented) so a hand-renamed directory / edited Slug row / copied bundle whose internal slug names a *different* directory cannot become an immutable committed artifact. Exit 0 clean / 1 violation / **2 internal error, which BLOCKS** — an error is never a silent pass. `scripts/check_seal_identity.py`. Hub-only, [#475]. |
| `validate-backlog` | commit | Validates the BACKLOG.md story-map structure (ADR-66). |
| `audit-health` | commit | Runs `audit.py health` (the self-conformance checks incl. canonical-file freshness). **FAIL-level findings block the commit; WARN-level only inform.** Runtime scales with the check registry. Bypass: `--no-verify`. |
| `ruff` | commit | Lint gate — `ruff check` (fleet-canonical pinned-rev `astral-sh/ruff-pre-commit` @ v0.15.5, rev == the `pyproject.toml` required-version floor). Blocks on violations. [#13] closed. |
| `coherence-nudge` | commit | **Non-blocking** nudge: a registered spec changed without a version bump → stdout nudge + `logs/COHERENCE-NUDGE.log`; always exits 0 (pairs with the `reconciled_versions` audit check). |
| `backlog-id-on-close` | commit-msg | Requires `[#id]` / `closes [#id]` when a commit removes a `- [#id]` task. |
| `backlog-filing-backpressure` | commit-msg | Add-side sibling of `backlog-id-on-close`: a commit that ADDS a new BACKLOG task id must carry a `kill-candidates:` line (≥1 existing `#id`, or `none — <reason>`) — BLOCK if absent. `scripts/check_backlog_filing.py`, proposals only. Hub-only. |
| `block-ff-push` | pre-push | Refuses a push placing a non-merge commit on `main`'s first-parent spine (a direct-to-`main` commit or a true FF merge); a `--no-ff` merge passes. Hub-only. **Fails CLOSED (exit 2) on internal error** since the ADR-85 amendment 2026-08-03 §A6 — it previously printed *"degraded — allowing push"* and returned 0, silently auto-allowing the exact push it exists to refuse. Bypass `git push --no-verify` (the `no_ff_merges` audit WARN is the post-hoc backstop). **Activate once per machine: `uv run pre-commit install --hook-type pre-push`** (`default_install_hook_types` only wires it on a fresh install). |
| `block-unanchored-push` | pre-push | **The ADR-85 HARD leg** (amendment 2026-08-03 §A5): refuses a push targeting `main` whose range carries first-parent spine entries with **no JOURNAL anchor**. Discharge is range-level — a JOURNAL entry naming ≥1 SHA the range *introduced*. It lives at pre-push because a Stop hook can be exhausted by the host's block-cap, and an organ that can be exhausted cannot carry teeth. **Fails CLOSED (exit 2).** Sole escape `git push --no-verify`, made non-silent by the `journal_spine_anchor` audit backstop (a gap is a **FAIL**, not a WARN). Shares its range resolver with `block-ff-push` and its anchoring predicate with the backstop via `scripts/journal_anchor.py`. `scripts/block_unanchored_push.py`. Hub-only. **Same one-time `--hook-type pre-push` activation.** |

`audit.py health` (the gate above) is also runnable standalone for an on-demand sweep: `uv run python scripts/audit.py health`. It runs the self-conformance checks incl. the canonical-file **freshness** check (`last_reviewed` staleness; see PLAYBOOK); FAIL blocks a commit, WARN (e.g. the 30-day freshness backstop) only informs.

Run the auto-format hook standalone (e.g. to clean up before commit):

```
uv run python scripts/normalize_headers.py LESSONS.md JOURNAL.md
```

## Nightly outcome management

<!-- scope: meta -->

The nightly conformance Routine (cloud, read-only) reviews the repo and synthesizes a digest,
`docs/audits/YYYY-MM-DD-conformance-nightly-digest.md`, carrying a machine-readable counts marker
`<!-- counts: raw=N survived=N killed=N -->`. **Where to look:** open `nightly-triage` Issues are
surfaced at session start by `scripts/surface_triage.ps1` (a `[triage] …` line) and live in the
repo's Issues tab.

**RETIRED 2026-07-08 — the conformance-digest mechanism** (`closes [#255]`, commit `82227f08`).
The repo's first GitHub Action, `.github/workflows/nightly-conformance-triage.yml`, was
`pull_request`-triggered rather than scheduled, so under the fleet's local `--no-ff` merge
workflow (no PRs) it last fired 2026-06-25 and never again — while still appearing active. It was
removed **together with everything built on it**: the clean-night / findings-night / anomalous-PR
routing, the divert onto `automation/conformance-digest` (remote branch deleted), and the
one-added-file diff guard with its fail-closed counts-marker parser. `surface_triage.ps1` lost its
Surfacing 2 in the same commit; **the successor fleet-health surface is the local
`scripts/fleet_health.py` SessionStart digest.** **There is no automated PR triage of any
kind** — nothing auto-diverts, auto-closes, or auto-files a nightly digest. (`.github/` was
deleted with that Action and **returned 2026-08-06** carrying an unrelated organ: the [#501]
report-only wall, which triggers on `push`, re-runs the gate set off-host and records the
outcome. It performs no triage and reads no digest — see ARCHITECTURE Ch2/Ch6.)

**Why the `.js` workflow exists, and when it runs as a spec.** The nightly run is
defined by `.claude/workflows/conformance-hub.js` — but the native `Workflow` launcher
is **not enabled in the cloud runtime** (re-probed; still unavailable). So each nightly
Routine **attempts the native launcher first and falls back to reading the `.js` as a
*specification*** — orchestrating its stages by hand via read-only Explore agents
(spec-orchestration). Doctrine: **native-attempt-first, with a nightly re-probe**; the
digest reports which path ran, and execution swaps back to native automatically when the
platform re-enables it. The load-bearing consequence: any guarantee written as in-script
code is **inert on the fallback path** (the `.js` is read, not run). Full standard: PLAYBOOK
"Routine/night deployment standard"; ADR-72 (cloud self-containment).

**Residual risk (widened by the [#255] retirement).** The survivor count is a code-owned marker
in the digest body (`<!-- counts: raw=N survived=N killed=N -->`; the agent's free-form prose is
never trusted). The only enforcement left is **in-script** — `conformance-hub.js` refuses to emit
a digest whose `counts_marker` does not match the code-computed marker verbatim. By the paragraph
above, that guarantee is **inert whenever the run falls back to spec-orchestration**, and the
Action's fail-closed parser that used to backstop it on the executing path was removed with the
Action. There is currently **no executing-path counts backstop**. `conformance-hub.js` still
describes the marker as the line "the nightly Action parses" — stale prose left standing where
this file could not reach it. **Layer-2 note:** the surviving pieces are read-only — the Routine
never writes to a target repo and `surface_triage.ps1` only reads — so the Layer-2 "validators
only / never executes cross-repo" invariant holds.

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

Protocol: `protocols/HANDOFF_PROCESS.md` — **v6** (stamp v6.1.0, *stable*; ADR-82, operator-ratified 2026-06-11 per #149, amended 2026-06-16 for the v5.1 architect strategic supplement, 2026-06-17 for the v5.2 always-generated supplement file, 2026-06-25 for the v5.3 §5 probe-manifest consolidation, 2026-07-05 for the v5.4 §5 structural anti-bluff + §13 generator note, 2026-07-05 for the v5.5 §14 epic-lane handoffs — EPIC + EPIC RETURN, ADR-97, 2026-07-06 for the v5.6 §14a execution-MODE item, 2026-07-07 for the v5.7 §16 functional/intake mode + §14 developer alias, ADR-98, and **2026-07-31 for the v6.0 one-round-trip boot** — one CC-side command (`/handoff-verify`) runs the whole live gate and emits ONE evidence block the operator pastes once, plus the P0 standing-topic legs, the `Destination` boot-header row + its P3 comparison, the `HANDOFF_BOOT` byte budget, and the A11 generation/verification guards; intake #19 §B(b), rulings R1..R7, built under [#446]; and **2026-07-31 for the v6.0.1 `Destination` branch-field clarification** — the field is the BOOT DESTINATION compared once by P3 at boot, so `main` is legal for a primary-tree architect seat and lane branches are declared at delegation, §13(c″), architect ruling, revertable); and **2026-08-07 for the v6.1.0 boundary invariants
at the cut** — generation refuses while a committed batch manifest declares an open batch
(WINDOW = BATCH) and refuses over a linked worktree or a live stash (NO LEFTOVERS), plus the §13
supplement-authorship re-statement and the successor-boot dispatch-visibility note. v6 keeps the
v5 model:  instead of a browser-delivered 8-file bundle, **CC owns the handoff** — it emits a lean **residual** + a **probe manifest** under `docs/handoffs/<slug>/`, and a fresh browser chat boots from the thin `protocols/HANDOFF_BOOT.md`. Verification has teeth: the probes force CC to re-derive every load-bearing fact from the live primary source at check-time. v4.4 is archived at `protocols/archive/HANDOFF_PROCESS_v4.4.md`. The ADR-36 read-only contract holds: a handoff never writes to a target repo.

Claude Code command: **`/handoff`** — `create handoff for <repo>` has CC emit the **residual** + **probe manifest** under `docs/handoffs/<slug>/` and point the next browser at the thin boot (`protocols/HANDOFF_BOOT.md`); `complete handoff for <repo>` cross-checks repo state and finalizes. `<repo>` defaults to `.dev-knowledge` (self-handoff). Not `/session-summary` — that is a separate session-summary command, not the handoff generator.

`BACKLOG.md` (root): cross-session pending items per ADR-41. Universal mandate (ADR-38 amendment A5 — every repo, no tier gating). Review before chartering new session.

## Definition of done (session close)

<!-- scope: meta -->

`protocols/DEFINITION_OF_DONE.md` is the single source of truth for what "done" means at session close (ADR-85): every first-parent spine entry integrated onto `main` is anchored by a `JOURNAL.md` entry naming ≥1 commit SHA that entry **introduced** (**hard-gated**), and a session that lands commits should update `BACKLOG.md` with a structural marker (**advisory**). It is enforced **mechanically and deterministically** — no LLM in the gate. Since the **ADR-85 amendment 2026-08-03** the teeth are the pre-push hook `scripts/block_unanchored_push.py` plus the `journal_spine_anchor` audit backstop (§A5); the session-end Stop-hook (`scripts/session_end_backpressure.py`) is **advisory in full**, and the sole escape is `git push --no-verify` — the `/override` local-token path is **retired** (§A2). The other living docs (`ARCHITECTURE`, `VISION`, `LESSONS`) are "update when materially affected"; **this file is `last_reviewed`-gated** by the `canonical_freshness` A2 check. Pointer only — the rules live in that file, not here (resident copies drift).
