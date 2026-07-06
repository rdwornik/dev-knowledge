# Changelog review — 2026-07-06

**Trigger:** operator-invoked `/changelog-review` (PUSH half of #113). SessionStart sentinel nudge: `claude-code 2.1.200 > last reviewed 2.1.177`.
**Reviewer:** Claude Code (Opus 4.8) — in-session classification (operator present; not automation).
**Lineage:** v0 = 2026-06-07 audit trio; prior digests 2026-06-07 (2.1.168 / codex 0.137.0) and 2026-06-15 (2.1.177 / codex 0.139.0).

## Scope reviewed
- **claude-code:** `2.1.178 → 2.1.201` (CHANGELOG top). Installed: `2.1.200`. Source: raw GitHub `CHANGELOG.md`.
  - Absent from the changelog (version skips): 2.1.180, .182, .184, .188, .189, .192, .194. 2.1.190 = "bug fixes and reliability improvements" only.
- **codex:** `0.140.0 → 0.142.5` (8 stable releases). Installed: `0.136.0` (reviewed ahead of installed — intended; keeps the sentinel quiet). Alphas (`0.143.0-alpha.*`) skipped per contract. Source: `gh release view` bodies.

## Bucket counts
- **ADOPT:** 2 — both architect-decision (model-routing + cloud-night auto-mode)
- **OBSOLETES-WORKAROUND:** 0
- **STALE-NAMES:** 0 confirmed (1 model-pin caveat routed to VERIFY, not asserted)
- **VERIFY:** 1 — `claude-sonnet-4-6` deprecation check
- **NOISE:** claude-code ≈ 260 of ~276 bullets; codex ≈ all 8 releases (review-engine-irrelevant)

## ADOPT (flag only — architect decides; no item created)

### A1 — Refresh Sonnet model pins to Sonnet 5 (UNDERUSED-NATIVE)
- **What changed:** Claude Sonnet 5 became the default model in 2.1.197 — native 1M-token context, promo pricing $2/$10 per Mtok through Aug 31.
- **Our gap:** three organs still pin the prior-gen `claude-sonnet-4-6`:
  - `.claude/agents/artifact-reader.md:8` (frontmatter `model:`) + line 30 note
  - `.claude/workflows/conformance-hub.js:150-152` (V1/V2/V3 verifier `model:` pins)
  - `.claude/settings.json:73` describes these as "Sonnet verifiers" (prose, not a hard pin)
- **Value:** Sonnet 5's 1M context + promo pricing directly benefit the conformance-hub verifiers and artifact-reader ingestion; staying on 4-6 forgoes both and risks the 2.1.183 deprecation warning (see V1).
- **Candidate home:** model-routing doctrine — ADR-28 roles / ESSENTIALS "Architect routing" / ARCHITECTURE Ch3 t-shirt model routing. Pairs with V1.

### A2 — Native auto-mode safety nets for the #86 cloud-night envelope (UNDERUSED-NATIVE)
- **What changed:**
  - 2.1.178 — subagent spawns are now evaluated by the auto-mode classifier *before* launch (closes a gap where a subagent could request a blocked action unreviewed).
  - 2.1.183 — auto mode blocks destructive git (`git reset --hard`, `git checkout -- .`, `git clean -fd`, `git stash drop`), blocks `git commit --amend` on commits not made by the agent this session, and blocks `terraform/pulumi/cdk destroy` unless asked.
  - 2.1.193 — `autoMode.classifyAllShell` routes *all* Bash/PowerShell through the classifier (not just arbitrary-code-exec patterns).
- **Our gap:** the #86 cloud-night safety envelope (`.claude/settings.json:73`) currently leans on platform guards + a `git status --porcelain` tripwire and commits NO Write/Edit deny by design. These native auto-mode nets are a complementary layer specifically for the unattended nightly Routine.
- **Value:** reinforces the read-only-by-design nightly conformance run against destructive-command drift without a blanket deny that would break local work.
- **Candidate home:** #86 / cloud-night envelope note. Reinforces (does not replace) core-invariant #3.

## OBSOLETES-WORKAROUND
None identified. No native feature in this range retires one of our artifacts (the pre-commit gates, SessionStart/Stop/PreToolUse hooks, `session_end_backpressure.py`, `block_immutable_edits.py`, tier1-lifecycle plugin are all governance-specific with no native equivalent shipped). The 2.1.183 native destructive-git blocking *reinforces* core-invariant #3 but does not retire it (ours is broader doctrine, not an auto-mode-only gate) — captured under A2, not here.

## STALE-NAMES
None confirmed. Checked our config/docs against every rename/removal in range:
- `TeamCreate` / `TeamDelete` removed (2.1.178) — **not referenced** in-repo (grep clean).
- `/agents` wizard removed (2.1.198) — our references are to `.claude/agents/` dirs and the `claude agents` view, **not** the removed wizard; not stale.
- permission mode "default" → "Manual" (2.1.200) — **backward-compatible** (both accepted); our `.claude/settings.json` sets no permission mode. `defaultMode` at `deploy/lived_sandbox/spawn.py:93` + its tests is an anti-bypass assertion on an **unchanged** key name — not stale.
- `/realtime`, `respondToBashCommands` — not referenced.
- **Caveat (→ V1):** the `claude-sonnet-4-6` pins (above). Whether that id is *deprecated/removed* vs merely older is unconfirmed, so it is routed to VERIFY rather than asserted as stale.

## VERIFY (exact command; outcome not guessed)

### V1 — Is `claude-sonnet-4-6` still a valid, non-deprecated model id?
- **Why it matters:** 2.1.183 added a deprecation/auto-update warning that now *also* covers models set in agent frontmatter. Our artifact-reader frontmatter + conformance-hub verifiers pin `claude-sonnet-4-6`. If deprecated/auto-updated, A1 becomes mandatory and the pins are stale.
- **Command (operator runs — not run here to avoid a recursive `claude` spawn / credit use):**
  `claude --model claude-sonnet-4-6 -p "ok" --debug 2>&1 | grep -i "deprecat\|updated to"`
  (or inspect the `/model` picker for whether 4-6 still appears).
- **Cloud cross-check:** inspect the most recent nightly conformance PR/digest for a model-deprecation or fallback note — the cloud spec-orchestration path reads those same `conformance-hub.js` pins.

## Awareness (auto-fixed, no action — reliability/efficiency wins touching our organs)
- **Workflow `agent({schema})`** no longer loops forever on schema-validation failure — caps at 5 attempts (2.1.186) and can't re-call `StructuredOutput` after a success (2.1.187). Directly touches the conformance-hub verifiers (`verifierSchema`).
- **SessionStart / SubagentStart hooks** no longer hide stderr on exit-code-2 (2.1.199) — a previously-silent hook error now surfaces in-transcript; our 5 SessionStart hooks are fail-soft, so this is pure upside.
- **`/code-review`** cleanup finders merged 5→1, ~25% fewer tokens (2.1.196); **`/review <pr>`** now uses the `/code-review medium` engine (2.1.186).
- **`/deep-research`** no longer misreports verifier failures as "all claims refuted" (now `unverified`) (2.1.196).
- **Windows / OneDrive-adjacent env:** Write/Edit 0-byte/truncated-file fix on cloud-synced folders + Windows/OneDrive agent-create `EEXIST` fix (2.1.181); Windows Terminal TUI corruption under heavy nested-subagent load fixed (2.1.183) — relevant to our nested-subagent workflows.
- **PowerShell (our primary shell):** `git diff`/`git grep`, `egrep`/`fgrep`, and `|`-quoted patterns no longer mis-reported as failures when they exit 1 (2.1.196).
- **Confirmed NON-issues by reading our config:** the comma-separated-matcher silent-no-fire bug (2.1.191) — our matchers use pipe form (`Edit|MultiEdit|Write|NotebookEdit`), not commas; the hyphenated-matcher substring bug (2.1.195) — we have no hyphenated matchers.

## NOISE (counted, not itemized)
- **claude-code (~260 of ~276 bullets):** background-agent daemon/roster/handover reliability; Claude-in-Chrome GA + fixes; voice dictation; VSCode/JetBrains; tmux/Ghostty/Warp/Windows-Terminal rendering & a11y (screen-reader); MCP OAuth / enterprise-proxy / TLS; Bedrock/AWS/Vertex/Foundry/Mantle gateway + org-default / org-restricted models; remote-control; install script; streaming/retry/watchdog internals; sandbox internals; model-availability churn (the Sonnet-5-becomes-default line itself); AskUserQuestion no-auto-continue default change (our unattended agents don't call it); assorted `/stats` `/copy` `/branch` `/recap` `/btw` `/bug` `/desktop` `/doctor` `/config` UX.
- **codex (all 8 stable releases):** our usage is `/codex-review` only (staged-diff review engine). Nothing in 0.140.0–0.142.5 changes that engine except one auto-fixed review-path crash (0.140.0 #22879 — `/review` no longer crashes on `Esc` with queued guidance). Everything else — `/usage`, `/goal`, `/import`-from-Claude-Code, mentions menu, Bedrock/encrypted-secret auth, multi-agent v2, plugins/marketplace, remote/exec-server + PathUri refactors, Windows system-proxy (PAC/WPAD), OpenSSL/esbuild bumps, `0.142.3`/`0.142.4` maintenance-only, `0.142.5` websocket trace-log hygiene — is NOISE for review-only usage. Consistent with the 2026-06-15 digest.

## Operator routing
Two items want an architect decision (ADR-28 roles):
- **A1** — bump Sonnet pins to Sonnet 5 across `artifact-reader.md` + `conformance-hub.js` (model-routing doctrine, ARCHITECTURE Ch3).
- **A2** — adopt native auto-mode safety nets into the #86 cloud-night envelope.
- **V1 gates A1's urgency** — run the `claude-sonnet-4-6` deprecation check first; a warn/auto-update makes A1 mandatory.

No BACKLOG items created; no organs edited (per command contract — capture/flag only). #113 stays closed (this run is a pure ADD).
