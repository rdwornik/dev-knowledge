# Handoff Stage 2 Response: corp-monorepo (session-sync)

**Slug:** `2026-05-25-corp-monorepo-session-sync`
**Stage 1 HEAD:** `32a47f85b07d697be20066c1ec69df3cf92cb1f6`
**Populated by:** Rob (copy-paste from old browser chat for corp-monorepo)

<!-- Instructions: Open docs/handoffs/in-progress/2026-05-25-corp-monorepo-session-sync/stage1-question.md
     Copy from the PASTE_BOUNDARY line to end of that file.
     Paste into the OLD corp-monorepo browser chat.
     Replace EVERYTHING below the marker line with the architect's verbatim response.
     Save this file, then run "complete handoff for corp-monorepo" in Claude Code. -->

═══ REPLACE EVERYTHING BELOW THIS LINE ═══

### **1. OBJECTIVE**

This section assumes zero prior session knowledge.

The next session has two intertwined goals: **execute the highest-impact backlog item that unblocks all subsequent work, AND clarify the working pattern itself**. These cannot be separated — the backlog priorities below reveal process gaps which must be addressed in how the session is conducted, not just in what it ships.

**Recommended session lead:** verify the implementation status of corp-monorepo's safety-invariants ADR (drafted during work culminating in commit `eee56ca` on 2026-04-21, current state unknown to me). If the 4-PR implementation plan (foundation `corp/safety/onedrive.py` + migration of 4 guard sites + AST-based CI scanner + vault writer narrowing) did NOT execute, this technical debt overrides every P1 BACKLOG item because the hotfix relies on inline-duplicated guards that are bypassable in known ways the ADR resolves.

**Recommended session sequence:**

1. Status check on the safety-invariants ADR implementation (5-minute audit)
2. If implementation is missing or partial: route accordingly (ADR work is in scope; full implementation may not fit one session)
3. If implementation is complete: proceed to ADR namespace collision fix (GAP 2)
4. Tier-deprecation removal (P1, mechanical, fast win, exercises process)
5. Scrum-master review authority ADR codification (P1, judgment-heavy, mid-session slot)
6. ADR-34 vault underscore disambiguation (PARTIAL finding, small)
7. README disposition (P2, if time)

**Rationale for not leading with mechanical P1s:** "Way of working" clarity that Rob explicitly requested is not improved by mechanically deleting frontmatter from N files. It is improved by surfacing whether prior architectural commitments shipped, and by resolving ambiguities (namespace collision, ADR-34 disambiguation) that propagate to every future ADR reference.

(architect inference): If implementation of the safety-invariants ADR is in fact complete, Codex `/review` cross-check against the audit findings from `1d733b1` would be a higher-value session lead than the tier-deprecation P1 — but I cannot verify implementation status from my witnessed window.

### **2. REALITY**

This section assumes zero prior session knowledge.

**Witnessed state (limited to ~2026-04-22, ~1 month before current HEAD):**

During work culminating in the merge of `hotfix/onedrive-safety-p1` to main (commit `eee56ca`):

- Three P1 OneDrive safety vulnerabilities in `corp cleanup` and `archive_project` flows were verified and fixed
- Two new exception types added: `OneDriveSafetyError(RuntimeError)` and `PathTraversalError(RuntimeError)` in `src/corp/cleanup/errors.py`
- An amendment cycle followed Codex `/review` discovering symlink/junction bypass (substring-only guard) and test-layer ambiguity; all four guard sites unified with `.resolve(strict=False)` + fail-closed on `OSError`/`RuntimeError`
- One drift carried forward: `src/corp/project/renderer.py` raises `ValueError` instead of `OneDriveSafetyError` because the CLI catches `(FileNotFoundError, ValueError)` — silently switching exception class was rejected; unification deferred to the safety-invariants ADR
- One unfixed write-intent caller flagged: `src/corp/actions/deck_actions.py:104` still uses `_resolve_project_path` with default `writable=False`; not patched in hotfix scope

During work on 2026-04-22:

- AI Council debate (panel: Claude Opus 4.7, Gemini 3.1 Pro, Grok 4.20, GPT-5.4; synthesizer: Claude Sonnet; mode pick; 91k tokens; $0.59 cost) on centralization pattern for OneDrive safety guards
- Winner: Option C — centralized `corp/safety/onedrive.py` module in foundation layer + AST-based CI scanner. 3-of-4 consensus; Grok dissented on AST-theater grounds (acknowledged in synthesis, overruled on enforcement strength)
- Strongest insight from debate: secondary AST rule forbidding `guard_path()` inside `try`/`except OneDriveSafetyError` without re-raise (closes silent-neutering attack vector)
- Built `codex-review.ps1` wrapper in `~/.claude/bin/` using `codex exec --output-last-message`, replacing manual TUI clipboard-paste workflow
- Council transcript archived; safety-invariants ADR drafted as combined OneDrive centralization + vault single-writer invariant narrowing (Option B — narrow invariant to explicit zone whitelist rather than rewrite 8 existing action write sites)

**Unknown — Stage 3 should verify against repo:**

- Whether the safety-invariants ADR merged to main
- Whether `src/corp/safety/onedrive.py` exists
- Whether `tests/safety/test_no_unguarded_writes.py` (AST scanner) exists
- Whether the 4 guard sites were migrated to use the centralized module
- Whether `renderer.py` exception type was unified
- Whether `deck_actions.py:104` was patched
- Whether the vault writer narrowing PR shipped, and whether `VaultZone` enum was extended (DASHBOARDS existed; METADATA and BRIEFS were noted gaps; PROJECTS and NAVIGATE appeared in active use)
- Whether `2026-04-21-p1-verification.md` was ever recovered into main from the `verify/codex-p1-findings` branch (Claude Code surfaced this as missing during ADR drafting)
- The content and topic of `.dev-knowledge` ADR-27 (the namespace-colliding ADR)
- The content and rationale of ADR-54 (deletion of corp-monorepo's AGENTS.md)
- What replaced AGENTS.md as the source of Codex severity definitions

**Process drift witnessed (relevant to "way of working" goal):**

Across multiple sessions before the audit work, the assistant generated formal Claude Code prompts that referenced files which did not exist in corp-monorepo (`PLAYBOOK.md`, `LESSONS.md`, `gotchas.md` are in `.dev-knowledge`, not the repo). The assistant also omitted JOURNAL.md updates for seven consecutive turns despite JOURNAL's header explicitly requiring per-session entries. Both omissions were discovered late; backfill was performed manually.

ESSENTIALS.md at the time did not mention JOURNAL.md, did not enumerate `.claude/skills/`, did not name ARCHITECTURE.md as a living-doc convention, and did not name `docs/decisions/transcripts/` as the audit-trail folder for AI Council outputs. The omission compounded — assistants writing prompts had no canonical checklist of what to read first, so they read a partial subset and drift accumulated.

**(architect inference) on the conformance gap audit findings:**
Some of the findings in commit `1d733b1` (deep audit) and `8a24fae` (conformance gap audit) likely have this exact root cause — assistants operating on corp-monorepo with incomplete view of `.dev-knowledge` conventions and corp-local conventions both. Each assistant fix may have addressed surface drift without resolving the upstream cause (no canonical read-first checklist).

**On GAP 2 severity (witnessed audit context, inferred severity):**
The ADR namespace collision is annoying-but-low-blast-radius today. Severity compounds with each new ADR. Renumbering existing ADRs to resolve the collision invalidates every cross-reference in JOURNAL, prior audits, and inline citations in source code. Preferred fix (architect inference): prefix corp-local ADRs (e.g., `CMR-NN`) going forward, leave history intact.

### **3. RATIONALE**

This section assumes zero prior session knowledge.

**On tier-deprecation reasoning**: Unknown — no specific rationale witnessed in this session. The decision date (2026-05-23) is after my witnessed window. Stage 3 verifies against ADR-33/38/40/51 amendments and the ecosystem decision record.

**On scrum-master review authority codification deferred to N=3**: Unknown — no specific rationale witnessed. (architect inference): waiting for N=3 empirical instances before codifying a pattern is sound discipline against premature abstraction — one instance is an anomaly, two could be coincidence, three is a pattern. But this is reconstruction from common engineering practice, not witnessed reasoning. Stage 3 verifies against JOURNAL entries documenting the three instances.

**On ADR-34 vault underscore pattern PARTIAL finding**: Unknown — no insight into ADR-34's content or why disambiguation in `CLAUDE.md §4` was deferred at audit time.

**Witnessed reasoning that may inform the next session:**

The work culminating in `eee56ca` followed an audit-fix-verify-merge cycle that empirically caught bugs the primary assistant missed:

1. Verification audit on a dedicated branch with no code changes — purely classification work
2. Hotfix branch with failing-on-main regression tests committed BEFORE the fixes (TDD-red proof)
3. Mandatory Codex `/review` before merge for safety-critical paths
4. Amendment cycle when re-review surfaces a missed bug class
5. Atomic per-finding commits, no squash, each revertable

This pattern caught two real bugs from a single primary author — symlink bypass via string-based substring check, and test-layer ambiguity letting tests pass even when runtime guards were broken. Two-AI-reviewer empirically pays for itself on High-risk paths. This rationale should inform how the next session approaches the safety-invariants ADR implementation if that work is still pending.

A second pattern, witnessed implicitly: AI Council debates produce real architectural decisions only when fed real data. The OneDrive centralization debate was anchored in a verification report (4 guard sites enumerated, exception types tabulated, INCIDENT 2026-03-14 context, hotfix data) — not hypothetical. Council with hypothetical scenarios produces hypothetical decisions.

**A pattern that did not work and should be corrected:**

Formal prompts generated without an explicit, complete "READ FIRST" checklist of repo conventions (skills, JOURNAL, ARCHITECTURE.md, transcripts folder, gotchas) lead to faithful execution of incomplete prompts. The defect is in the prompt template, not in the execution. The next session should propose a canonical READ FIRST block to be inlined in every formal prompt for corp-monorepo work, sourced from a single authoritative location (ESSENTIALS.md amendment or equivalent).

### **4. DIRECTIVES**

This section assumes zero prior session knowledge.

Numbered sequential actions for the next corp-monorepo session. Each is an action verb + target + verification step. (architect inference) where not directly witnessed.

1. **Audit safety-invariants ADR implementation status.** List all files matching `docs/decisions/ADR-27-*` AND `docs/decisions/transcripts/ADR-27-*`. Verify whether `src/corp/safety/onedrive.py` exists, whether `tests/safety/` exists with an AST scanner, and whether `src/corp/cleanup/disk.py`, `src/corp/cleanup/executor.py`, `src/corp/actions/_helpers.py`, `src/corp/project/renderer.py` still contain inline `_guard_onedrive` or `_guard_writable` functions or now import from the central module. Verification: produce `docs/audits/2026-05-25-adr27-status.md` with a 1-line status per artifact (exists/missing/partial). If implementation is partial or missing, treat this as the session's highest-priority work, overriding the P1 BACKLOG items below.

2. **Resolve ADR namespace collision (GAP 2).** Propose a corp-local ADR prefix (e.g., `CMR-NN`) for ADRs authored against corp-monorepo. Do NOT renumber existing ADRs. Update `CLAUDE.md §11` to document the prefix convention and explain that historical ADRs (ADR-01 through ADR-NN) retain their original numbering. Verification: `CLAUDE.md §11` mentions both the convention and the rationale for not renumbering; new ADRs created in step 5 use the prefix.

3. **Tier frontmatter removal (P1).** Enumerate affected files with `grep -r "^tier:" .` and `grep -r "^scale:" .`. Strip the frontmatter mechanically. Use a dedicated branch `chore/tier-deprecation`. Commit with a clear message referencing the relevant ADR amendment numbers (ADR-33/38/40/51 per Stage 1 context). Verification: greps return zero matches; full test suite passes; JOURNAL entry follows the 3-line Did/Failed/Next convention.

4. **ADR-34 vault underscore disambiguation (PARTIAL finding).** Add a 1-2 sentence note to `CLAUDE.md §4` clarifying corp-monorepo's treatment of the underscore convention in Obsidian references. If the convention is unclear from ADR-34's content: ask Rob before guessing. Verification: `CLAUDE.md §4` mentions the convention explicitly; broken vault references are not introduced.

5. **Scrum-master review authority ADR codification (P1).** Given three empirical instances per Stage 1 context, write the ADR using the corp-local prefix from directive 2. Cite the three instances by date and short description. Verification: ADR file exists in `docs/decisions/`, registered in any local ADR index, JOURNAL entry.

6. **README disposition (P2).** Read current `README.md`. Decide keep / delete / update with a one-paragraph rationale recorded in JOURNAL. If keep-and-update: ensure README does not duplicate `CLAUDE.md` (different audiences). Verification: JOURNAL entry with decision and rationale.

7. **DEFER to subsequent sessions**: Phase 2 universalization rollout, hyphen migration ADR-38 sub-items, handoff folder format adoption (11-file flat format), root hygiene application. These are mechanical-but-multi-step P2 items that should not interleave with the architectural work above; each deserves its own scoped session.

**Cross-cutting session-close verification:**

- Every directive above results in atomic commits with COMMIT marker per local convention
- Every directive results in JOURNAL entry per 3-line Did/Failed/Next convention (prepend, do not edit prior entries)
- Session closes with `docs/audits/2026-05-25-session-summary.md` (or equivalent) so the next handoff is not blind to this session's output
- `tach check`, `pytest -x --tb=short`, `ruff check src/ tests/` pass before any merge

### **5. BOUNDARIES**

This section assumes zero prior session knowledge.

**Do NOT:**

1. **Renumber existing ADRs** to resolve the namespace collision in directive 2. Renumbering invalidates every cross-reference in JOURNAL.md, prior audits, source code citations, and the conversation history embedded in transcripts. Prefix new corp-local ADRs going forward; leave history intact.

2. **Touch the `OneDrive - Blue Yonder` synced tree under any operation, even read-only**. Multiple safety guards exist in the codebase precisely because this class of bug already produced an incident requiring bulk restore. Even diagnostic operations should treat OneDrive paths as suspect.

3. **Write commit messages containing the literal string `OneDrive - Blue Yonder`**. A local pre-commit hook blocks commits whose message text contains that string, regardless of file paths touched. Workaround: write message to a temporary file and use `git commit -F <file>`. (witnessed in prior session)

4. **Skip Codex `/review` on safety-critical or architecturally-significant changes**. Empirically, Codex caught bugs the primary assistant missed (symlink-bypass guard, test-layer ambiguity). Two-AI-reviewer is not optional for High-risk paths. Mechanical changes (tier-frontmatter removal, README edits) may skip; judgment-heavy changes (ADR codification, namespace collision resolution) require it.

5. **Reference `PLAYBOOK.md`, `LESSONS.md`, or `gotchas.md` as if they exist in corp-monorepo without verifying first**. These files historically lived in `.dev-knowledge`. When a prompt or directive needs content from those files, either inline the relevant content or cite the full path. (witnessed: prompts that referenced bare filenames led to Claude Code failing to find them and falling back to inferior assumptions.)

6. **Omit JOURNAL.md entries**. Append-only, 3-line entries (Did/Failed/Next), prepend (newest first). The JOURNAL header instructs reading the last 5 entries before starting work. (witnessed: a prior session omitted JOURNAL for seven consecutive turns; backfill was performed manually after the omission was caught.)

7. **Start Phase 2 universalization rollout in the same session as tier-deprecation removal or scrum-master ADR codification**. Different blast radii, different review needs.

8. **Bypass `tach check`**. Foundation / core / orchestration / interface layer boundaries are enforced. New modules (like `src/corp/safety/` if implementation work is taken on) must be placed in the correct layer in `tach.toml`.

9. **Auto-merge architectural changes**. Boundary 4 applies.

10. **Assume `.dev-knowledge` conventions are auto-loaded by Claude Code in corp-monorepo work**. They are not. If a directive depends on a `.dev-knowledge` rule, the prompt must explicitly cite the relevant ADR essence or the full path to the file. (witnessed: drift from this assumption caused multiple prompt failures in prior sessions.)

**Fallback contingencies:**

- If directive 1 reveals safety-invariants ADR implementation is incomplete: route the session into implementation work (foundation module first — it unblocks migration and CI). Defer P1 BACKLOG items.
- If directive 2 (namespace collision) is contested or the prefix scheme has unforeseen consequences: defer to a small AI Council debate (mode pick) before committing to a fix.
- If Rob is unavailable for clarification on ADR-34 underscore convention (directive 4): default to "do not modify Obsidian-reference files until disambiguation is confirmed," and document the deferral in JOURNAL.
- If implementation status audit (directive 1) takes the entire session: that is the correct session outcome. The next session resumes from the audit's conclusions.
