# Changelog review — 2026-07-09

<!-- scope: meta -->

- **Model in effect:** Opus 4.8 (`claude-opus-4-8[1m]`). *(The morning-ops brief nominated Sonnet; the live session runtime is Opus 4.8 — stated honestly per execution-truthfulness. A changelog classification is judgment work, well within tier.)*
- **Trigger:** PUSH — SessionStart sentinel nudge (claude-code installed 2.1.204 > last-reviewed 2.1.202). Operator-invoked via morning-ops leg F.
- **Tools + ranges reviewed:**
  - claude-code **2.1.203 → 2.1.204** (2 versions; last-reviewed 2.1.202 @ 2026-07-07)
  - codex **0.143.0** (1 new stable; last-reviewed 0.142.5 @ 2026-07-06; installed still 0.136.0 — reviewed-ahead is intended)
- **Bucket counts:** ADOPT **0** · OBSOLETES-WORKAROUND **0** · STALE-NAMES **0** · VERIFY **2** · NOTABLE-fixes (relevant, automatic) **~15** · NOISE **~24**
- **SEED doc:** none written (step 6 — no ADOPT / OBSOLETES-WORKAROUND this run; the rubric forbids empty SEED docs).

---

## Headline

The claude-code 2.1.203 release is a **background-sessions + worktrees + Windows hardening** release — and this fleet is a heavy background/worktree/Windows user (this very arc ran as a background job). Most entries are **reliability fixes that benefit us automatically** (no action, no adoption). Nothing new to queue, nothing of ours retired. **Two items warrant a live VERIFY** because they touch documented LESSONS/gotchas. Codex 0.143.0 is all-NOISE for our `/codex-review`-only usage.

## ADOPT (0)

None. No new configurable capability we lack. (The 2.1.203 "login-expiry warning before background sessions are interrupted" is relevant to unattended runs but is automatic — nothing to adopt or configure.)

## OBSOLETES-WORKAROUND (0)

None cleanly. The closest is the 2.1.203 worktree-subagent fix (below) vs our LESSON — but it targets subagent **shell-command cwd**, not our documented **absolute-path-edit-lands-in-primary** failure, so it does not cleanly retire the workaround. Filed as VERIFY, not OBSOLETES.

## STALE-NAMES (0)

No renames/removals hit our live docs/config by name. ("Removed the startup 'claude command missing or broken' warnings — now in `/doctor`/`/status`" changes behavior, not a name we reference.)

## VERIFY (2) — live check before assuming impact

- **V1 — worktree subagent cross-lane contamination may be reduced.** 2.1.203: *"Fixed worktree-isolated subagents sometimes running shell commands in the parent checkout instead of their own worktree."* This is adjacent to our LESSON **`worktree-edits-land-in-primary-via-absolute-paths`** (subagent edits landing in the primary, false-green tests). Re-test whether that class still reproduces on 2.1.204 before trusting or retiring the workaround:
  - `git worktree add` a scratch lane → spawn a subagent that edits a worktree-relative file + runs a shell command → confirm the edit + cwd land in the worktree, not the primary (`git -C <primary> status` clean; inode compare).
- **V2 — background task output empty-file behavior on Windows.** 2.1.203: *"Fixed background task output on Windows being permanently replaced by an empty file after `/clear`."* During THIS arc, background-task output files read as empty (the pytest monitor files) — though we did not `/clear`, so likely a different cause. Confirm background-output reads are reliable on 2.1.204:
  - run a trivial `run_in_background` command → read its output file → confirm non-empty. (If still flaky without `/clear`, capture as a fresh gotcha — not covered by the 2.1.203 fix.)

## NOTABLE FIXES — relevant to our stack, applied automatically (no action)

These land free on 2.1.204 and harden our exact usage pattern (unattended background sessions, worktrees, Windows, SessionStart surfacing hooks):

- **2.1.204:** SessionStart hooks now stream during headless sessions — previously could idle-reap a remote worker mid-hook. *(Directly our nightly headless + SessionStart `fleet_health`/`surface_triage` pattern.)*
- Background agents no longer inherit a stale daemon `PATH` (missing tools on **Windows**).
- Background sessions no longer drop a shell-exported `ANTHROPIC_BASE_URL` (which had sent API keys to the default endpoint → 401).
- `TaskStop`/`TaskOutput` now find background agents spawned by another agent.
- Worktree creation no longer rejects nested repos in **multi-repo workspaces** (our `Dev/` layout).
- Bash no longer fails "argument list too long" in repos with many worktrees.
- `effortLevel` changes in `settings.json` now respected when forked through the daemon.
- Background daemon auto-upgrade failure no longer silently kills running background sessions; stale-token sessions now self-recover; crash-loop on deleted working dir now fails once with a clear error.
- Returning to `claude agents` no longer silently stops running subagents / re-runs from scratch — work carries over.
- Subagents are now less likely to re-delegate their whole task to another subagent.
- Context-usage indicator no longer re-analyzes the full transcript every turn (memory/CPU regression fixed).

## NOISE (~24) — counted, not itemized

macOS-only stalls; TUI/rendering polish (⏸ badge, scroll jump, bash-mode flicker, reattach escape codes, left-arrow nav change, empty-agents-view sections, removed nav hints/startup warnings); MCP `roots/list` additions; VSCode toggle; mouse opt-outs; binary-size/startup-memory reduction; `/exit` false warning; LSP-plugin disuse flag. **Codex 0.143.0 in full:** remote-plugins-by-default, system-proxy/PAC routing, `remote-control pair`, Bedrock GPT-5.6 models, MCP tool-search default, app-server env inspection, Windows ConPTY input + sandbox-credential-retry fixes, security dep bumps (OpenSSL et al.) — all irrelevant to our read-only `/codex-review` usage.

## Operator routing

**No ADOPT or OBSOLETES-WORKAROUND items — nothing needs an architect adoption decision this cycle.** Two VERIFY checks (V1 worktree contamination, V2 background-output) are CC-runnable spot-checks, not architect decisions; run them opportunistically. State bumped: claude-code → 2.1.204, codex → 0.143.0.
