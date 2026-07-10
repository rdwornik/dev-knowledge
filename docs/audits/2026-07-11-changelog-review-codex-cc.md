# Changelog review — claude-code + codex (2026-07-11 morning brief)

- **Class:** `changelog-review` (ADR-101 enum) · **Date:** 2026-07-11 (morning-delivery; run overnight 2026-07-10)
- **Source-session:** NIGHT HUB v2 consolidation run, lane `lane-n-night-consolidation`, HEAD `47f31b5`
- **Status:** PROPOSAL-ONLY — this file adopts nothing, bumps no state file, files no intake SEED. `/changelog-review` (the live command that DOES bump `tool-versions.yaml` + drops a SEED) is operator-invoked; this is a read-only research pass whose outputs route to the morning menu.
- **Model:** Opus 4.8 (`claude-opus-4-8[1m]`), effort max. Web research fanned out to a read-only subagent; every factual row carries an official-source URL or an explicit `UNVERIFIED` flag.

## Baseline (from `ecosystem/tool-versions.yaml`)

- **claude-code:** `last_reviewed_version: 2.1.204` (reviewed 2026-07-09). Installed / SessionStart-reported: **2.1.206**. Delta this pass: **2.1.205, 2.1.206**.
- **codex:** `last_reviewed_version: 0.143.0` (reviewed 2026-07-09). Installed: **0.136.0** (reviewed-ahead-of-installed is intentional). Delta this pass: **0.144.0, 0.144.1**.
- Prior review `docs/audits/2026-07-09-changelog-review.md` closed 2.1.203–204 + codex 0.143.0 at **0 ADOPT / 0 OBSOLETES**. This is a thin 2-version delta on each tool.

> NOTE on the brief's premise: the brief said "last-reviewed 2.1.205" and "OpenAI Codex 5.6 release." Both are imprecise — the state file's last-reviewed is **2.1.204**, and there is **no Codex CLI "5.6"** (see §1b). Corrected here rather than carried forward.

## 1a. Claude Code changelog (2.1.204 → 2.1.206)

Evidence (all rows): `https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md` (human URL: `https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md`). Ordered by operator-interest.

| # | Finding (version) | Verdict | Why | Effort |
|---|---|---|---|---|
| 1 | **2.1.205** — Windows worktree removal no longer deletes files OUTSIDE the worktree when an NTFS junction/dir-symlink sits inside it | IGNORE (auto) | Data-loss fix; lands free on 2.1.206. Directly hardens this fleet's Windows + heavy-worktree + no-leftovers pattern (cf. the `worktree-remove-blocked-by-live-session` lesson). | S |
| 2 | **2.1.206** — `/doctor` proposes trimming checked-in `CLAUDE.md` by cutting content Claude can derive from the codebase | **TRIAL** | UNDERUSED-NATIVE. This repo already manages CLAUDE.md size (ADR-49/65 §12 condensation, ≤200-line target, `doc_claims`/freshness-gated). Run `/doctor`, read its suggestions, **do NOT auto-apply** — governance prose here is deliberately dense. | S |
| 3 | **2.1.205** — auto-mode rule blocking tampering with session transcript files | IGNORE (near-miss) | Looks like it could retire the ADR-77 `block_immutable_edits.py` guard, but it protects Claude Code's OWN `.jsonl` session transcripts, whereas ADR-77 protects the repo's immutable **markdown** (decisions/handoffs/audits). Different target → does NOT retire our guard. One operator glance. | S |
| 4 | **2.1.205** — background-task notifications now explicitly state no human input occurred | IGNORE (auto) | Reinforces this ecosystem's execution-truthfulness / anti-bluff doctrine for unattended runs (this very run received those notifications). | S |
| 5 | **2.1.206** — `EnterWorktree` confirms before entering a worktree OUTSIDE `.claude/worktrees/` | IGNORE (auto) | This repo's worktrees live inside `.claude/worktrees/` (this lane included) → no prompt fires; effectively blesses the convention. Awareness only for ad-hoc out-of-convention worktrees. | S |
| 6 | **2.1.205** — auto-mode asks before `rm -rf` on an unresolved variable | IGNORE (auto) | Safety improvement aligned with no-leftovers + OneDrive-exclusion discipline. | S |
| 7 | **2.1.206** — background agents self-upgrade after a CC update (no stale-session upgrade on attach) | IGNORE (auto) | Smoother nightly/unattended background runs. | S |
| 8 | **2.1.206** — fixed `CLAUDE_CODE_EXTRA_BODY` silently ignored by `claude agents` / `--bg` workers | IGNORE (auto) | Only matters if the fleet sets that env var for background workers. | S |
| 9 | **2.1.205** — verify skills rewritten only when a documented command changed (was: every session) | IGNORE (auto) | Reduces churn on auto-generated verify skills; low relevance to the repo-local `.claude/skills/verify`. | S |
| 10 | **2.1.206** — MCP per-server `request_timeout_ms` now respected (was defaulting 60s) | IGNORE (auto) | Minimal MCP usage in this markdown-governance repo. | S |
| 11 | **2.1.206** — `/commit-push-pr` auto-allows push to the configured push remote, not just `origin` | IGNORE (auto) | This repo pushes to `origin`; no behavior change. | S |

**Net 1a:** **0 ADOPT-NOW · 1 TRIAL** (`/doctor` CLAUDE.md-trim) · rest automatic hardening that already landed on the installed 2.1.206. Consistent with the 2026-07-09 review's 0-ADOPT outcome. (Cosmetic/unrelated entries — TUI/scroll/`/model`-picker/Bedrock-egress/macOS — omitted per scope.)

## 1b. "Codex 5.6" vs /codex-review

**Label mismatch (reported first):** there is **no Codex CLI version "5.6."** The current Codex CLI is **0.144.1** (2026-07-09; `https://github.com/openai/codex/releases`). "GPT-5.6" is a *model* family, appearing in the codex changelog only as "Amazon Bedrock GPT-5.6 Sol/Terra/Luna" added in **0.143.0** — already classified NOISE (Bedrock, unused here) by the 2026-07-09 digest. The real delta reviewed: **0.143.0 → 0.144.0 → 0.144.1**.

**What /codex-review assumes** (the command is USER-level, not in this repo — CLAUDE.md §7):
- `~/.claude/commands/codex-review.md:3` — wraps `codex exec --output-last-message`.
- `~/.claude/bin/codex-review.ps1:24` — `codex` on PATH (`npm i -g @openai/codex`).
- `~/.claude/bin/codex-review.ps1:47` — `codex --version` first line parsed verbatim into audit frontmatter.
- `~/.claude/bin/codex-review.ps1:165` (load-bearing) — `$prompt | & codex exec --sandbox read-only -c model_reasoning_effort=high --output-last-message $tempFile -`. Assumes: `codex exec` subcommand · `--sandbox read-only` · `-c key=value` override · `--output-last-message <file>` · trailing `-` = stdin prompt.

**What changed (0.144.0 + 0.144.1):** all interactive/hosted-session-oriented — `writes` app-approval mode, interactive MCP auth, app-server auth + redirect, usage-credit UI, global pnpm-install detection, an "ultra reasoning" high-concurrency warning; fixes to ChatGPT thread recovery, Intel-macOS Code-Mode crashes, Windows sandbox file deletion. 0.144.1 is installer-only. Evidence: `https://github.com/openai/codex/releases/tag/rust-v0.144.0`, `.../rust-v0.144.1`.

- **New capabilities to wire: NONE.** Every 0.144.0 feature is irrelevant to a non-interactive `codex exec --sandbox read-only` review. The "ultra reasoning" warning concerns `--ultra` fan-out, not the single-shot `model_reasoning_effort=high` lever /codex-review already uses. Verdict all: **IGNORE**.
- **Breaking / silent-degradation risk: NONE documented.** Neither release note mentions any change to `codex exec`, `--output-last-message`, `--sandbox`, `-c key=value`, stdin `-`, `--version` output, or the default model. Honest caveat: these are terse *summaries* → this is **absence-of-announced-change, not a byte-level guarantee**. A 30-second smoke-test would positively confirm: `echo hi | codex exec --sandbox read-only --output-last-message tmp.md -`.
- **Forward-only, LOW:** codex is installed at **0.136.0**, so the 0.144.x deltas cannot degrade /codex-review until a local `npm i -g @openai/codex` upgrade. Any exec-contract risk is deferred to that future upgrade, not live today.
- **Pre-existing fragility, LOW (UNVERIFIED):** `codex-review.ps1:47` takes `codex --version` first line verbatim into frontmatter — a future banner reformat would pollute the audit header. Not known to have changed in 0.144.x; cosmetic blast radius.

**Net 1b:** /codex-review is **safe across 0.143.0 → 0.144.1** — nothing to wire, no documented break, and it runs against the older installed 0.136.0. No action.

## 1c. Seed-list reconciliation (`docs/intake/2026-07-07-changelog-review-seeds.md`, intake-id 5, status SEED)

The seed doc holds **exactly one** item:

- **S1 — dynamic-workflow-size `/config` setting (ADOPT / UNDERUSED-NATIVE)**, from claude-code 2.1.202 → **STILL-OPEN.** Neither 2.1.205 nor 2.1.206 touches the `/config` workflow-size control (evidence: full CHANGELOG for both versions, no matching entry). Not a bug a release can "close" — only an operator/architect adoption ruling can (candidate homes per the seed: #155 loops-architecture or a PLAYBOOK workflow-doctrine note; ties to #270). The 2026-07-09 review produced no new seeds, so S1 is the sole outstanding candidate.

## Scope note + honesty flags

- **URLs fetched (official, all reachable):** the claude-code raw CHANGELOG; `https://developers.openai.com/codex/changelog` (308 → `https://learn.chatgpt.com/docs/changelog`); `https://github.com/openai/codex/releases`; the two `releases/tag/rust-v0.144.*` notes.
- **Not independently re-verified this session:** the installed codex version `0.136.0` (taken from the `tool-versions.yaml` comment, not a live `codex --version`); the `codex --version` banner format across 0.144.x (§1b, UNVERIFIED, low severity). No `codex exec` smoke-test was run (read-only scope cap).
- **No fabricated versions/dates.** Where an official source could not positively confirm, the row is marked UNVERIFIED rather than guessed.

## Morning adoption shortlist (ADOPT-NOW / TRIAL only)

- **TRIAL — `/doctor` CLAUDE.md-trim (2.1.206):** run once, read suggestions, do NOT auto-apply. Effort S.
- **Optional confirm (not an adoption):** 30-second `codex exec` smoke-test to positively close the 1b "absence-of-announced-change" caveat, if the operator wants certainty before the next codex upgrade.
- Everything else: 0 ADOPT-NOW; seed S1 (`/config` workflow-size) remains an open architect ruling, unaffected by this delta.
