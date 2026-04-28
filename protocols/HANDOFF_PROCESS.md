# Handoff Process
<!-- version: 2.0 — 2026-04-28 (full rewrite per ADR-32) -->

> **Authoritative source:** `docs/decisions/ADR-32_handoff_format.md`. This protocol is the operational counterpart of ADR-32 §1–§8: structural decisions live in the ADR; operational mechanics (triggers, generation workflow, extract-to-task, acceptance test) live here. If they conflict, ADR-32 wins — except for the diagram errata noted in §5.

A handoff transfers session state from one browser chat to the next. The artefact is a session folder under `docs/handoffs/{YYYY-MM-DD}-{slug}/`. The browser (architect) drafts content; Claude Code (executor) creates and verifies the folder; Rob triggers, reviews, and accepts.

---

## 1. Roles
<!-- scope: hybrid -->

Per ADR-32 §1 and ESSENTIALS § Roles (canonical definition):

- **Browser (architect).** Drafts the 9-section `HANDOFF.md` content, the `manifest.json` field values, the `first-message.md` opener, and the `upload-instructions.md` text. Browser output is advisory — it never claims filesystem state authoritatively.
- **Claude Code (executor).** Creates the folder, writes the files browser drafted, generates `tree.txt`, copies governance docs at session-close commit SHA, runs validators, commits. Claude Code is the trusted plane for everything Rob does not eyeball.
- **Rob.** Triggers (§2), authors the session charter (§3), reviews drafted content before paste-to-Claude-Code, accepts the folder via the walk-out test (§9).

Browser does NOT generate folders, run git, copy governance, or claim files exist. Claude Code does NOT redesign architecture or rewrite section text — it executes the browser's drafted content.

---

## 2. When to generate a handoff (triggers)
<!-- scope: meta -->

Handoffs are explicitly triggered by Rob. The browser does not propose handoff generation. **Anti-pattern (Vibe Code 4):** browser saying "good stopping point" or "let's wrap up" — Claude generates a handoff only when Rob says so.

**Triggers — any one fires:**

- **Manual.** Rob says `wygeneruj handoff` (PL) or `generate handoff` (EN).
- **Slash command.** Rob runs `/session-summary` in Claude Code (renamed from `/handoff` 2026-04-24).
- **Message-cap checkpoint.** Browser session reaches ~40 messages (ADR-32 §4 — empirical degradation cliff).
- **Time-cap checkpoint.** Browser session reaches ~2h elapsed (PLAYBOOK §8 — buffer before 3h decision-fatigue threshold).
- **Stop-sign signals (per Rob's UI preferences):** scope creep accumulating (>2 "while we're at it" expansions), topic shift (current discussion no longer matches charter goal), multiple unresolved follow-ups stacking without execution. These are mid-session quality regressions — checkpoint before they corrupt the handoff itself.
- **Charter stop condition met.** The session charter's `stop condition` (§3) is satisfied — session is *done*, not paused.

The 40-msg cap and 2h time-cap are independent: whichever fires first triggers a checkpoint handoff. Past either, browser reasoning quality degrades and any new handoff content drafted in-session is suspect.

**JOURNAL prepend ≠ handoff.** Workday-close JOURNAL entry (per PLAYBOOK Stream B Gap #4 spec — Did/Failed/Next, prepended) is a separate, lightweight artefact. It is *always* written at workday close. A folder handoff is generated *only* at session boundaries with substantive state to preserve. The two coexist; the JOURNAL entry summarises across all sessions in a workday, the handoff resumes a specific session in a fresh chat.

---

## 3. Session charter and step-verification handshake
<!-- scope: hybrid -->

These are the open-session and mid-session controls; the handoff at session close is the third leg.

### Charter (open)
<!-- scope: meta -->

Per ADR-32 §2 — Rob authors the charter (browser does not invent it) in the first 5 messages:

```
repo:
session type: [strategic | execution-support | governance-change | recovery/resume]
goal:
non-goals:
expected artifacts:
max message budget:
stop condition:
```

The charter is the scope contract. "Is this proposal in scope?" → check the charter. The session-close `HANDOFF.md` § 1 (Session charter recap) is a verbatim copy.

### Step-verification handshake (mid-session)
<!-- scope: dev -->

Per ADR-32 §3 — every multi-step Claude Code prompt must include between-step verification:

1. Complete Step N
2. Verify expected artifact/output exists (file path, test pass, validator clean, commit SHA)
3. Report verification result to Rob
4. Only then proceed to Step N+1

A plan step without a verify action is incomplete (per `~/.claude/rules/core-invariants.md` §2). Skipped verification was pain point #5 in the failure base behind ADR-32.

---

## 4. Folder anatomy
<!-- scope: dev -->

### Naming
<!-- scope: meta -->

`docs/handoffs/{YYYY-MM-DD}-{session-slug}/` — date is session-close date, slug is short kebab-case description (e.g. `stream-c-session-1-final`). Folder is immutable post-close (per PLAYBOOK Order conventions).

### Storage location
<!-- scope: meta -->

Per ADR-32 §8:

- **Single-repo session:** folder lives in that repo's `docs/handoffs/`.
- **Cross-repo session:** folder lives in `.dev-knowledge/docs/handoffs/` (authoritative). Per-repo `docs/handoffs/` may hold a stub pointing back.
- **Central index:** `.dev-knowledge` provides O(1) discoverability across repos (form deferred until cross-repo handoff frequency justifies tooling).

### Layout
<!-- scope: meta -->

```
docs/handoffs/{YYYY-MM-DD}-{slug}/
├── upload-instructions.md         (top — drag-drop guidance for Rob)
├── first-message.md               (top — paste verbatim into new chat)
└── contents/                      (single drag-drop target for browser)
    ├── HANDOFF.md                 (9-section session state — see §5)
    ├── manifest.json              (machine-readable orchestration)
    ├── tree.txt                   (repo structure snapshot at session close)
    ├── ESSENTIALS.md              (point-in-time copy)
    ├── PLAYBOOK.md                (point-in-time copy)
    ├── CLAUDE.md                  (point-in-time copy)
    └── JOURNAL.md                 (point-in-time copy)
```

> **ADR-32 §6 diagram errata.** The ADR-32 §6 ASCII diagram puts `HANDOFF.md` at the folder root and `manifest.json`/`tree.txt` inside `contents/`. The live first-instance folder (`docs/handoffs/2026-04-27-stream-c-session-1-final/`) and PLAYBOOK § "Handoff format spec" (line 569) put `HANDOFF.md` *inside* `contents/`. The live layout wins (drag-drop target = `contents/`, so `HANDOFF.md` must ship inside it). ADR-32 itself is not amended here; an errata pointer is added to JOURNAL pending so a future Council session can decide whether to reissue ADR-32 or accept the diagram as a known slip.

### Point-in-time copies
<!-- scope: meta -->

Governance docs in `contents/` are *copies* taken at session-close commit SHA, not symlinks or live references. Why: anti-drift on resume. The browser opening a handoff weeks later sees the rules that were binding *when decisions were made*, not the current rules (which may have moved on). The manifest pins each copy to its commit SHA so staleness is detectable.

Per ADR-32 rejected-alternatives §2: snapshots-only (no manifest) was rejected. Manifest + commit SHA is required.

### `manifest.json` — required fields
<!-- scope: meta -->

Schema v1.0 (matches live first instance):

| Field | Purpose |
|---|---|
| `schema_version` | `"1.0"` |
| `session_id` | folder slug (e.g. `2026-04-27-stream-c-session-1-final`) |
| `session_type` | matches charter session type |
| `repo` | primary repo |
| `previous_session` | predecessor folder slug, if any |
| `context_layers` | `{session_specific, structural_orientation, universal_governance, timeline}` — each lists files + purpose; `universal_governance` includes `live_state_path` + drift note |
| `reading_order` | ordered list of `{file, purpose}` for the next browser session |
| `token_budget_estimate` | rough total token cost of `contents/` (helps next session plan budget) |
| `next_session` | `{type, tool, primary_actions[], recommendation}` |
| `references` | `{transcripts[], research[], audits[], predecessor_handoff, workspace_config[]}` |

### `tree.txt`
<!-- scope: dev -->

`tree -L 3` (or equivalent) of the repo root at session-close commit. Gives the browser structural orientation without re-uploading the whole repo.

### `upload-instructions.md`
<!-- scope: meta -->

Drag-drop guidance for Rob: which folder to drag (`contents/`), what to do with `first-message.md` (paste verbatim), what's inside and why. Short — ~30 lines.

### `first-message.md`
<!-- scope: llm -->

The exact text Rob pastes as the new chat's first message. Includes: continuation context, list of uploaded files, reading order, next-session goal options, recommended choice. Short — ~50 lines max. Browser reads this *as a message*, not as an upload.

---

## 5. `HANDOFF.md` — 9 sections, fixed order
<!-- scope: meta -->

Per ADR-32 §5. Sections always present in this order; empty sections kept (consistency enables deterministic resumption — empty section is itself a signal).

| # | Section | Purpose | Machine-verifiable? |
|---|---|---|---|
| 1 | Session charter recap | Verbatim copy of charter from session open (§3). | n/a (verbatim) |
| 2 | Decisions made | Each binding decision + 1-line rationale. Link to ADR if formalised. | Decision text = no; ADR refs = yes (file exists) |
| 3 | Work completed | What changed in the repo. List file paths and commits. | Yes — `git log` / file existence |
| 4 | Pending items | Numbered list of next-session candidates with effort estimate. | No (forward-looking) |
| 5 | Open questions | Unresolved items needing human decision before next binding step. | No |
| 6 | Files actually modified | Explicit file list. Distinct from §3 (which may name conceptual changes). | Yes — `git diff --name-only` |
| 7 | Required inputs for next browser session | What must be uploaded / what state must hold. | Yes (file existence, commit SHA, validator pass) |
| 8 | Governance docs referenced | Which ADRs, PLAYBOOK sections, ESSENTIALS sections, Council decisions bound this session. | Yes — file paths |
| 9 | Next recommended first action | Single concrete next step for the next browser session. | Yes (action is verifiable when done) |

**Rule for §3, §6, §7:** prefer machine-verifiable claims (commit SHAs, file paths, test commands) over prose. Browser hallucinates state; commit SHAs do not.

---

## 6. Scale-tiered application
<!-- scope: meta -->

Per ESSENTIALS § Project Scale Tiers (S/M/L). Folder format is the default; legacy single-file is retired (§10).

| Tier | When | Folder required? | 9 sections? | Governance copies | manifest.json + tree.txt |
|---|---|---|---|---|---|
| **S** | Single-session quick checkpoint, no substantive state to preserve | Folder optional (single `HANDOFF.md` in `docs/handoffs/{date}-{slug}/contents/` acceptable) | Yes — empty sections kept | Optional | Optional |
| **M** | Default for any session boundary with decisions or pending work | Required | Yes | Required (at least ESSENTIALS + CLAUDE.md) | Required |
| **L** | Stream-level / cross-repo / governance-change sessions | Required | Yes | Required (ESSENTIALS + PLAYBOOK + CLAUDE.md + JOURNAL.md, plus any session-specific governance) | Required + extended `references` block |

Even at S, the 9-section structure is non-negotiable — what scales is the surrounding context, not the core content.

---

## 7. Generation and resume workflows
<!-- scope: hybrid -->

### Generation (session close)
<!-- scope: hybrid -->

1. Browser drafts the 9-section `HANDOFF.md` content, `manifest.json` field values, `first-message.md`, `upload-instructions.md`. All four are produced in the same browser turn — no mid-handoff drift.
2. Rob copies the drafted content.
3. Rob pastes to Claude Code with a prompt directing it to: create folder `docs/handoffs/{date}-{slug}/`, write the four files, copy governance docs from current commit into `contents/`, generate `tree.txt`, run `python scripts/validate_scope_tags.py` and `pre-commit run --all-files`, commit on a feat branch.
4. Claude Code reports commit SHA and validator status.
5. Rob runs the walk-out test (§9) before considering the handoff accepted.

### Resume (next session open)
<!-- scope: llm -->

1. Rob opens new browser chat.
2. Rob drags `contents/` folder into chat input. All files upload as a single batch.
3. Rob pastes `first-message.md` verbatim as the first message.
4. Browser reads files in `manifest.reading_order`, then proposes plan.
5. New browser does NOT re-litigate prior decisions — they are in `HANDOFF.md` §2 and any ADRs they reference.

---

## 8. Extract-to-task protocol
<!-- scope: hybrid -->

ADR-32 deferred operational mechanics here. Source: DECISION_29 transcript synthesis recommendation 3 + research synthesis ("the browser's only output is HANDOFF.md and DECISIONS.md entries" — claude-opus-4-7 R1, anchored).

**Trigger.** In a `strategic` or `governance-change` session, the browser identifies work that requires any of: file edits, file moves, git operations, test runs, validator runs, artifact existence checks, or multi-file coordination. Per ADR-32 §1, this is by definition Claude Code work.

**Action.**

1. **STOP discussion.** Do not continue planning the work conversationally — that is the bundling anti-pattern (DECISION_29 pain #6).
2. **Emit a Claude Code prompt** using `templates/prompt-template.md`. The prompt must include:
   - Repo path + branch workflow (per repo conventions).
   - Numbered steps with the step-verification handshake (§3) explicit between each.
   - Scope contract — what is in scope and what is deliberately out.
   - Success criteria — machine-verifiable where possible.
   - Read-first list — the files Claude Code must read before acting.
   - Default `>1 file changed` requires a prompt; ≤1 file may be inline-described, but only as advisory text Rob still pastes through Claude Code (DECISION_29 transcript: Grok R1, "tightly versioned" boundary). *(Threshold not anchored in ADR-32 itself — flagging as operational, revisitable.)*
3. **Return to strategy** only after Claude Code reports task completion + verification.

**Hard rule — defer requires explicit justification.**
"Defer" without a concrete reason is forbidden. Acceptable: "Defer until ADR-32 is amended (blocking)" / "Defer to next session — out of charter scope." Unacceptable: "Defer for later" / "Defer for now" / silent deferral. This rule blocks the recursive-planning anti-pattern (DECISION_29 pain #9) at its operational source.

**Why this lives here, not in ADR-32.** ADR-32 §6 deferred extract-to-task explicitly. Mechanics are operational (how prompts are formed, threshold for >1 file, defer rule), not structural. If the threshold or rule needs to change, this protocol is the place — not a new ADR.

---

## 9. Walk-out test (acceptance)
<!-- scope: meta -->

A handoff is accepted only if all of the following hold:

1. **Folder commit clean.** `git status` clean, validators pass, folder committed on its feat branch.
2. **Reading order parses.** `manifest.reading_order` lists files that exist in `contents/`.
3. **Governance copies present.** Per scale tier requirement (§6).
4. **First-message round-trip.** Rob simulates: open new chat → upload `contents/` → paste `first-message.md` → first response is substantive analysis of the next-session goal, with no clarification questions about prior session context.

If any check fails, the handoff is rewritten (not patched mid-resume — see ADR-32 rejected alternative §3, single-markdown-only). The walk-out test is the architect's "would I be able to resume this groggy on Tuesday?" gate.

---

## 10. Legacy migration note
<!-- scope: meta -->

- The legacy `handoff-prompts/` folder (typ-a-step1, typ-a-step2, typ-b-step1) was deleted 2026-04-27 with the adoption of folder-format handoffs. Do not recreate.
- Single-file legacy handoffs at `docs/handoffs/YYYY-MM-DD-*.md` (predating 2026-04-27) are read-only historical artefacts. Do not migrate, do not edit, do not promote to folder format.
- The Type A (programming) / Type B (conversational) taxonomy in v1.x of this protocol is **retired**. Folder format applies uniformly; scale tier (§6) replaces type taxonomy.

---

## 11. Related references
<!-- scope: meta -->

- `docs/decisions/ADR-32_handoff_format.md` — authoritative source (this protocol implements it)
- `docs/decisions/transcripts/DECISION_29_handoff_synergy.md` — Council debate behind ADR-32
- `docs/research/2026-04-27-handoff-patterns-council-research.md`
- `docs/research/2026-04-27-handoff-patterns-external-research.md`
- `docs/decisions/ADR-28_three-layer-architecture.md` — Layer 1/2/3 split (handoff bridges Layer 1 sessions)
- `docs/decisions/ADR-31_authority_model.md` — central audit grounding
- `docs/decisions/ADR-27_scope-tagging.md` — tagging vocabulary
- `protocols/ESSENTIALS.md` § Roles — canonical browser/Claude-Code role definitions
- `protocols/PLAYBOOK.md` § 8 (Handoff B) — predecessor description, now stale (one-line stale notice added; substantive rewrite deferred)
- `protocols/PLAYBOOK.md` § "Handoff format spec (since 2026-04-27)" — folder layout reference
- `templates/HANDOFF_TEMPLATE.md` — fillable 9-section skeleton
- `templates/prompt-template.md` — for extract-to-task Claude Code prompts
- Council #24 — "wygeneruj handoff" trigger phrase
- Council #28 — AGENTS.md as canonical cross-tool governance
- First folder-format instance: `docs/handoffs/2026-04-27-stream-c-session-1-final/`

---

## Section history
<!-- scope: meta -->

- v2.0 (2026-04-28) — full rewrite per ADR-32. Replaces v1.x single-file Type A/B framing and 3-artifact decomposition. New: 9-section structure, folder convention, point-in-time copies, charter + step-verification controls, extract-to-task mechanics (operational home, deferred from ADR-32), defer-requires-justification rule. Legacy `handoff-prompts/` retirement noted.
- v1.1 (2026-04-26) — superseded. Documented handoff = 3 artefacts (persistent doc + commit prompt + first-message). Self-referential paradox in v1.0 fixed but framing now retired.
- v1.0 (2026-04-25) — superseded. Vibe Code 4 protocol patch, single-artifact framing.
