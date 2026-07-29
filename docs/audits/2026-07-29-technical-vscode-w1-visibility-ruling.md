# `.vscode` consumer write-through — operator ruling on the W1 sizing surface

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-29 · **Slug:** vscode-w1-visibility-ruling
- **Arc:** window wind-down 2026-07-28→29 (architect window), branch `docs/window-winddown-2026-07-29`.
- **Answers:** `docs/audits/2026-07-28-technical-vscode-sizing-decision-surface.md` — the prep artifact
  that priced the options and returned the decision to the operator. That file is immutable; this is its
  ruling record, not an amendment to it.
- **Status of execution:** **RECORD ONLY.** Nothing in this ruling is executed in this arc. Every leg it
  authorizes is cross-repo and runs as its own follow-up arc under RULING-W (consumer worktree/branch →
  report; PLAYBOOK Ch8 "Hub→consumer writes"). The arc is queued in this window's handoff bundle residual.

---

## The ruling (operator, 2026-07-29)

**Option (b) — the S-size manual visibility copy, with the mechanism left gated.** Four parts:

1. **corp GO.** The operator grants corp-monorepo the same manual `.vscode` adoption ai-council received
   on 2026-07-22 — the ADR-93 merge-not-clobber hand-copy plus its `DECLARED-UNTIL-MECHANISM` entry in
   `corp-monorepo/.methodology.yaml`. The 2026-07-22 GO named ai-council only; this is corp's own word,
   which the sizing surface correctly said it needed. **Precedent to follow verbatim:**
   `ai-council/.methodology.yaml:97-109`.
2. **The mechanism stays gated.** The `editor-config` carrier remains `implemented: false`. Building it
   still runs behind **[#387]** (rewrite the buy-vs-build intake) → the vehicle ADR → **[#371]**. The
   ruling does **not** override [#371]'s own recorded constraint against a bespoke build; the visibility
   copy is the *outcome* bought early, not the mechanism bought cheap.
3. **Mechanism-DATE selection is folded into the 2026-08-26 session.** No date is attached to the
   mechanism here; choosing one is business for that session, alongside the drain slice and the D-queue.
4. **e1 `review_date` re-dates to 2026-08-26.** Both consumer declarations
   (`corp-monorepo/.methodology.yaml`, `ai-council/.methodology.yaml`, currently `review_date:
   2026-08-13`) move to **2026-08-26**, aligning the parity register's re-warn date with the session that
   will actually decide the mechanism.

## What this resolves, and what it does not

**Resolves.** The 2026-08-13 lapse risk the sizing surface priced: the visible half of W1 gets satisfied
in corp by hand (cost 1 of 3), and the `advisory-rewarn` flip (cost 2 of 3) is pre-empted by the re-date
rather than absorbed as recurring digest noise. [#352]'s "revisit/kill if not advanced" shelf-life (cost
3 of 3) is answered by the same move — advanced manually, mechanism deferred deliberately.

**Does not resolve.** The mechanism gap itself. `deploy/tool.py` still has five carriers and no sixth;
the manifest declaration still has no executor; ADR-93 merge-not-clobber JSON semantics are still unbuilt.
[#371] stays open on exactly those grounds, and this ruling is not a partial closure of it.

## Execution legs owed (none run in this arc)

| # | Leg | Repo | Shape |
|---|---|---|---|
| 1 | Manual `.vscode` decoration copy + `extensions.json` + `DECLARED-UNTIL-MECHANISM` entry | corp-monorepo | RULING-W: worktree/branch → report; ADR-93 merge, never clobber `files.watcherExclude` |
| 2 | `review_date: 2026-08-13` → `2026-08-26` in `.methodology.yaml` | corp-monorepo | RULING-W, same arc as leg 1 |
| 3 | `review_date: 2026-08-13` → `2026-08-26` in `.methodology.yaml` | ai-council | RULING-W, own branch |

Re-witness each consumer live before editing (the RULING-W first step), and note that the sizing
surface's live reads are dated 2026-07-28 — the executing session re-verifies them rather than trusting
this table's premises.

## Recording limitation, stated rather than worked around

This ruling is **not** mirrored into the [#371] or [#352] task rows. Both sit within ~16 and ~34
characters of the 1200-char `doc_rot` gross cap, so no faithful summary fits. That is the [#364] defect
in its natural habitat — a gate degrading the record it exists to protect — and it is recorded here as a
fresh instance rather than resolved by compressing the ruling into something uninformative. The rows'
pointer to this file travels in the handoff residual and the JOURNAL entry for this window.
