===== FILE: 02_METHODOLOGY — start =====

# 02 · How we work

Methodology floor for `.dev-knowledge`. The authoritative sources are
`protocols/PLAYBOOK.md` and `protocols/ESSENTIALS.md`; this is a working extract
generated from them at handoff time. When in doubt, the live files win.

## Model selection

- **Tier 1 (Sonnet):** ≤5 files, one layer, existing pattern, automated checks.
- **Tier 2 (Opus):** new abstractions, cross-module, unfamiliar APIs, security,
  judgment-heavy analysis. Implementation *waves* run on Opus, not Sonnet
  (PLAYBOOK model-note).
- **Trivial (<60s manual):** no AI at all.
- **How Claude thinks** (ESSENTIALS): think architecturally first (highest scope,
  then zoom); verify factual claims against source before stating them; push back on
  premises when warranted — concession without verification is sycophancy.

## Prompt format (the browser→CC contract)

Every formal CC prompt uses the **8-section structure** (PLAYBOOK "Writing prompts"):

1. **Model/Mode/Effort table** at the very top — e.g.
   `| Model | Sonnet | / | Mode | plan-then-auto | / | Effort | medium |`
   (Mode enumerates `plan` / `plan-then-auto` / bypass-permissions). This table is
   **non-negotiable and embedded verbatim**, never paraphrased (#25).
2. Title (imperative). 3. Repo + Purpose (absolute path + one-sentence outcome).
4. Read first (CLAUDE.md, gotchas, relevant docs). 5. Git workflow (branch + commit
   cadence + merge command). 6. UNDERSTAND (problem, what could break, likely failure
   mode). 7. Steps with COMMIT markers. 8. Final + What NOT to do (≥3 anti-patterns).

- **Per-scale:** Scale S = minimal (Title + Steps + What-NOT, skip UNDERSTAND if
  mechanical); Scale M = full, UNDERSTAND 1–2 sentences; Scale L = full + prefer
  `plan-then-auto` for a Step-1 review checkpoint.
- **Delivery:** prompts are downloadable `.md` artifacts in fenced code blocks
  (English-only; absolute paths; flat + code-fenced so the TUI doesn't paint
  box-drawing — CLAUDE §4 render-layer).
- **Pre-flight (hooks/commands in play):** name which hooks auto-fire vs which
  commands to invoke (PLAYBOOK "Usage protocol: which command / hook, when").

## Hooks & enforcement

**LLMs advise; hooks/tests enforce.** Don't put a rule in CLAUDE.md that isn't
backed by enforcement somewhere — it drifts. Precedence: **source → gate → agent**
(prefer the earliest tier that can hold the rule): make it self-documenting (derive
from code, auto-generate the artifact) → else an active gate (pre-commit/test/`verify:`
line) → else an agentic review for semantic/judgment/prose drift (the ADR-70 Tier-3
conformance workflow).

Live **pre-commit gates** (`.pre-commit-config.yaml`): `normalize-dated-headers`,
`codemap-freshness`, `toc-freshness` (×2: ARCHITECTURE + PLAYBOOK), `validate-backlog`,
`audit-health` (`audit.py health` — **FAIL blocks the commit**), `ruff` (lint gate,
blocks on violations), `backlog-id-on-close` (commit-msg: require `[#id]` when a commit
removes a task). Session hooks live in `.claude/settings.json` (SessionStart surfacing
+ a Stop backpressure hook + the ADR-77 PreToolUse immutability guard) — full organ
inventory is `ARCHITECTURE.md` Ch2.

There is now also a **pre-ship gate** (`audit.py ship-gate`, #147): at `/ship` it runs
the full self-audit against the arc, reads `Finding.status` objects directly (NOT exit
codes — the awareness organs exit 0 on drift), and blocks on any FAIL **or** any
new/undispositioned WARN. Expected WARNs are cleared via the read-only register
`ecosystem/disposition-register.yaml` (sha-keyed).

Codex is a separate code-review CLI (ADR-54, configured at `~/.codex/AGENTS.md`), not
Claude Code — a heterogeneous **second pair of eyes** on 3+ file or safety-critical
changes. Cross-vendor heterogeneity is the point: same-model self-review collapses to
sycophantic agreement.

## AI Council process

Convene **AI Council** for architecture/ADR-level decisions — never decide those
unilaterally. The architect does not seek operator validation on technical proposals
the operator can't adjudicate ("is this design right?"); instead → research mode, or
Council (a debate engine with blind voting + adversarial personas), or a trade-off
comparison the operator chooses from. The operator's role is constraints, priorities,
scope. Council transcripts archive to `docs/decisions/transcripts/`; the ADR
distillation is committed BY Claude Code (never a browser-chat placeholder hand-off).

## Conventions that bite

- **Commits:** Conventional Commits (`feat/fix/docs/chore/refactor`).
- **Branches:** `feat/ fix/ docs/ chore/` off `main`. **Every change — even a
  one-line doc edit — goes branch → merge `--no-ff`; never direct to main.** Finish
  via `/ship` (git-finish: merge, push, auto-delete the branch).
- **Naming:** UPPERCASE living docs (`VISION.md`, `CLAUDE.md`); `ADR-NN-topic.md`;
  `YYYY-MM-DD-slug.md` for dated artifacts; kebab-case otherwise.
- **Append-only:** `LESSONS.md`, `logs/TOKEN-LOG.md` (never edit); `JOURNAL.md`
  (newest-first prepend). **Immutable:** ADRs, transcripts, handoffs, audits
  (supersede, never edit in place).
- **Output the operator copies back** is flat + code-fenced (no column-padded tables
  — the TUI paints box-drawing client-side, ~3× tokens in browser chat).
- **Supersession closes the loop:** any decision that relocates/replaces an artifact
  names the obsolete one in a `Decommission:` field; non-empty → a BACKLOG item.

## Four-tag discipline canonicity

Four-tag discipline (witnessed/recall/inferred/unknown) is canonical per
HANDOFF_PROCESS v4.3 Amendment A. The §3.1 three-tag text in the spec body is
**superseded** — amendment-precedence applies. Phase 2 enforces four tags; the
definitions appear in `04_RECENT.md` of every bundle (so you don't need to read the
spec to apply them). Enforced **syntactically** by `audit.py` check #9 (verifies §3.1
enumerates all four tags OR points to Amendment A). **Check #9 does NOT catch
mis-labeled tags** — semantic accuracy needs sage discipline + Phase-2 cross-check.

## Bundle maintenance during session

If you discover drift between this bundle and repo state during your work — flag to
Rob, JOURNAL the discovery, and amend the `04_RECENT.md` Load-bearing facts table via
**append** (don't rewrite). The bundle is living until the next handoff. This is the
"handoff is back-and-forth, not a unilateral guess" rule.

## Parallel work

Same-repo parallel *committing* sessions need a worktree (different repos: none — separate
`.git/` already isolates them). Before splitting, run the **decide-first checks** (disjoint
substantive files? two distinct goals, not one? more than a single-file edit per stream?) —
the canonical safe pair is one code item ∥ one doc item. To start: keep stream A in the
**primary**, `claude --worktree <B>` for stream B, integrate **from the primary** (`/ship` A,
then `git merge --no-ff worktree-<B>` + push + teardown). Shared canonical files are handled,
not parallelized (BACKLOG removal via the closure loop; JOURNAL = trivial double-prepend;
operator is the serial gate). Full rule — START recipe, `.worktreeinclude`, `/ship`-from-
primary, no-leftovers teardown — in PLAYBOOK "Parallel sessions & worktree discipline."

## Session lifecycle

Start: `git status` clean (commit/stash first if dirty), read recent handoff +
JOURNAL, pick **max 2 objectives**, then wait for Rob's prompt — never improvise.
Test after each change; verify on filesystem (don't trust "done"). End: clean working
tree, JOURNAL entry prepended. **The 5 rules that matter most:** (1) test after each
change; (2) verify, don't trust; (3) scope is sacred; (4) Claude.ai challenges, Claude
Code executes; (5) date everything.

===== FILE: 02_METHODOLOGY — end =====
