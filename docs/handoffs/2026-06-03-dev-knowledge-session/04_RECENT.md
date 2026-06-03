# 04 · What just happened

A narrative of recent work on `.dev-knowledge`, written so a chat with zero prior
context can pick up the thread. Prose, not a log dump.

## The arc

**The headline: the hub moved from *describing* its standards to *enforcing and
distributing* them.** This was a four-act session; the through-line matters more than
any single artifact. Everything merged to `main`; **nothing was pushed** — push is
Rob's standing, deliberately-open decision, not an oversight.

**Act 0 — Tier-1 closure-loop closeout.** The session opened mid-cleanup. Closed #76
(hub converged onto the plugin's `/review-closures`; duplicate hub-local command
deleted, `scripts/review_closures.py` kept as canonical) and #77 (CONTRIBUTING
§Handoff rewritten to v4/ADR-62) — the first real use of the `closes [#id]`
convention. The substantive moment was the *"gate-reliability quirk"*: a misleading
`Skipped` in the pre-commit output that both Rob and the architect first read as a
coverage hole. It wasn't — CC root-caused it as a **cosmetic double-fire**: pre-commit
was installed for both `pre-commit` and `commit-msg` hook types, and five stage-less
hooks defaulted to *all* stages, so they re-ran at commit-msg, found nothing staged,
and printed `Skipped`. The gates always fired and passed the first time. One-line fix
(`default_stages: [pre-commit]`). *We nearly patched a bug that didn't exist* — that
episode set the diagnostic tone for the whole session.

**Act 1 — protocols/ doc-rot cleanup (five revertable bricks).** A read-only rot audit
of `protocols/` (~5000 lines) then five bricks. The ones that matter: **`audit.py`
became self-documenting** — `--help` and a new `checks` command now read from
`ALL_CHECKS`, killing check-count drift *at the source* rather than via a doc that
goes stale. PLAYBOOK §18 deleted (259 lines), prose de-duplicated to a single
canonical lesson→rule in §4, ten embedded "Section history" blocks removed (ADR-49
violation), CHANGELOG mentions retired. A counter-intuitive one: the ESSENTIALS "light
fix" *grew* the file 426→430 lines — and that growth was the *proof* it was a
drift-fix, not a trim. ESSENTIALS is for the LLM; "1-page" was the wrong contract, and
Rob reframed it mid-act. The last brick attempted AGENTS.md single-source via symlink;
**the symlink was blocked** (Windows, no admin/Dev-Mode), so it stayed copy-deploy and
the drift-guard was only proposed, not built.

**Act 2 — doc-tooling universalization (the main arc; where the headline lives).** An
inventory audit established the real state: the generators (`scripts/codemap`,
`scripts/toc`) lived only in the hub; children carried hub-generated artifacts but no
generator and no gate. After research → **ADR-71: the hub becomes a pre-commit hook
*source repo*** (the standard `repo:`/`rev:` + root `.pre-commit-hooks.yaml` pattern).
Hooks implemented as `language: script` thin wrappers in `scripts/` (not a pip
package); 4 hooks; the codemap CLI was parametrized with `--arch-file`. Codex caught a
`100644`→`100755` exec-bit defect (would fail on POSIX consumers) and we fixed it.
Piloted on **corp-monorepo** (TOC validated end-to-end, Codex clean) and rolled TOC to
**ai-council** (29-entry TOC, second consumer). Then we **stopped**: corp-ops and
corp-sca got no TOC because neither has a doc over the ~400-line threshold.

**Act 3 — closeouts.** Codemap #79 resolved to **"build nothing"** (reasoning below).
Fleet branch hygiene across all five repos — including a **preserve-then-delete** on
three unmerged corp-monorepo branches that recovered a live path-traversal security
finding the ADR-66 backlog migration had skipped. And the backlog was groomed into a
coherent **agentic arc** (#80/#81/#82). Parallel chronological detail (TOC mechanism,
ADR-71 amendment, the grounding audits) lives in JOURNAL if load-bearing.

## Four-tag discipline (canonical)

The sage tagged every claim using this discipline (canonical per HANDOFF_PROCESS v4.3
Amendment A; supersedes the earlier three-tag body in spec §3.1):

- **witnessed** — sage just verified this OR saw it happen recently AND has no reason
  to think it changed since
- **recall** — sage remembers from earlier in the session; **state may have changed** —
  verify via CC inline if the claim is load-bearing
- **inferred** — reasoning from evidence (not direct knowledge)
- **unknown** — sage doesn't know — flagged explicitly

When you encounter `recall` or `unknown` on a load-bearing claim in this file, verify
via CC before acting on it. This is the "handoff is back-and-forth" rule.

## What the sender chat said (interview)

The sender framed the present state (`recall`-tagged): `.dev-knowledge` at HEAD
`d439969`, `main`, clean, **unpushed** — *re-verify with `git log --oneline -15`
first, because the sender never inspected this directly*. PLAYBOOK ~2710 lines (see
drift below), `audit.py` self-documenting (12 checks), 230 tests, ADR-71 + its
amendment the latest significant decision.

The hub is now a **live pre-commit hook source repo** — root `.pre-commit-hooks.yaml`,
four hooks, wrappers in `scripts/`. Two consumers wired and validated: **corp-monorepo
and ai-council**, both pinned to rev `69558c7`, both via the relative local path
`../.dev-knowledge`. Codemap is in its **correct terminal state**: hub
generates-and-gates; the three child repos hand-author and human-maintain (marked
`not generator-managed`); corp-sca is text-only (S-scale).

Backlog (`recall`): #79 resolved; #80/#81/#82 added as the agentic arc and framed as
next-session focus; #78 (freshness-gated doc edits) and #70 (AI-Council loop) pending.
**Half-done by choice:** AGENTS.md single-source (still copy-deploy, drift-guard
unbuilt) and #78.

## Load-bearing facts (cross-checked vs repo at Phase 2)

| Claim from sender | Repo fact | Phase-2 verdict | Verification command |
|---|---|---|---|
| HEAD `d439969`, `main`, clean, unpushed | `d439969` is the tip of `main`; tree clean | ✅ confirmed | `git branch --contains d439969` · `git status --porcelain` |
| PLAYBOOK ~2710 lines (`recall`) | **2888 lines** | ⚠️ drift — recall predated the auto-TOC re-add (`fc0797f`) | `wc -l < protocols/PLAYBOOK.md` |
| `audit.py` self-documenting, 12 checks | self-documenting; **12** registered checks | ✅ confirmed | `python scripts/audit.py checks` |
| 230 tests | 230 collected | ✅ confirmed | `python -m pytest --collect-only -q` |
| ADR-71 + amendment exists | `ADR-71-doc-tooling-hook-source-repo.md` present | ✅ confirmed | `ls docs/decisions/ADR-71*.md` |
| Root `.pre-commit-hooks.yaml`, 4 hooks | present; 4 hook ids | ✅ confirmed | `grep -c '^\s*- id:' .pre-commit-hooks.yaml` |
| #79 resolved; #80/#81/#82 added; #78/#70 pending | BACKLOG matches exactly | ✅ confirmed | `grep -nE '#(70\|78\|79\|80\|81\|82)' BACKLOG.md` |
| AGENTS.md copy-deploy (symlink blocked) | `codex/AGENTS.md` present as a real file | ✅ consistent | `ls codex/AGENTS.md` |
| ruff is a wired pre-commit gate (#13) | `.pre-commit-config.yaml` id `ruff`, `entry: ruff check`, gate mode; #13 closed **2026-06-02** — the *prior* session, inside this multi-session handoff window | ✅ gate real; ⚠️ the "this session" attribution was wrong and was corrected in `02_METHODOLOGY` | `grep -ni ruff .pre-commit-config.yaml` · `git log --oneline --grep="#13"` |

**One drift, non-blocking:** the PLAYBOOK line count. The 2710 was measured after the
§18 deletion but *before* the auto-TOC was applied to PLAYBOOK, which added the table
back (~178 lines). Current = **2888**. No action needed — just don't quote 2710.

## Decisions & reasoning to carry forward

- **The organizing thesis — drift-proof at the source first.** Make it
  self-documenting (code, single-source canon, auto-generated artifacts); use an
  *active gate* only for what can't be made self-documenting; reserve *agents* as the
  safety net for what neither covers. "A lesson that isn't always-loaded doesn't fire."
  Every act was an instance: `audit.py checks` (source), the freshness/TOC hooks
  (gate), #81 (agent).
- **Why hook-source-repo, not a CC plugin (the pivotal call).** A plugin handles git's
  pre-commit lifecycle awkwardly and couples to a cache path; the source-repo pattern
  is the industry-standard way to share custom hooks. The expensive insight: **true
  central-push (deploy once, all repos update) would require the hub to *write into*
  its siblings — a Layer-2 violation by definition.** So there is no zero-touch
  propagation model here; the honest architecture is **pinned-pull** (each consumer
  pins a rev, updates by a deliberate bump). Per-repo wiring is one-time, not
  per-update. Convenience and Layer-2 separation are genuinely opposed — we chose
  separation.
- **Why `language: script`, not a pip package.** The generators are pure stdlib
  (argparse/ast/difflib/re/pathlib); venv isolation buys nothing, and packaging would
  force the repo to look like a distributable — contradicting its "validators only,
  doesn't execute as a product" identity.
- **Why TOC universalized but codemap didn't.** TOC is layout-agnostic, so it travels.
  Codemap is layout-coupled and the generator *breaks* on the fleet's actual layout
  (every child nests its package one level under `src/`, so the AST walker keys edges
  on the prefixed import root → zero edges, all-orphan dust). The generated graph is
  strictly *worse* than the hand-authored one. So #79 collapsed to "build nothing": a
  marker-aware gate would be a no-op on every child (cargo-cult), and fixing the
  generator is unneeded because no repo wants its output. The codemap is *already* in
  its correct universalized state — it just doesn't look uniform, and **uniformity was
  never the goal.**
- **Why preserve-then-delete earned its cost.** One of three unmerged corp-monorepo
  branches held a path-traversal security finding genuinely missing from the backlog
  (the ADR-66 migration skipped it because it lived on an unmerged branch in the old
  format). A blind `-D` would have silently destroyed a live security finding. The
  discipline paid for itself exactly once — which is all it needs to.
- **The architect's honest self-review (Rob asked for it; carry it).** The dominant
  failure signature was **architecting before grounding** — designing against *assumed*
  state, repeatedly (the codemap-pilot premise; the §18-home assumption). CC's
  grounding caught each one before damage. Secondary lapses: declaring "clean" against
  the cheap metric (tests-pass) while branches lay around the fleet; oscillating on the
  400-line TOC threshold instead of surfacing the trade-off once as a matrix and
  holding; and slipping this very handoff into Polish twice when artifacts are
  English-only. **The apprentice should treat prior prompts as proposals to be
  ground-checked, not settled truth — that's how this layered system fails safe.**
- **Lessons worth feeding into the methodology** (candidates for LESSONS / the eventual
  #81 verifiers): diagnose before fixing; ground state before architecting; don't
  cargo-cult a gate that gates nothing; preserve before delete; declare closure against
  the hard goal, not the easy proxy; a doc that *grows* during a cleanup can be
  evidence of a fix, not a regression.
