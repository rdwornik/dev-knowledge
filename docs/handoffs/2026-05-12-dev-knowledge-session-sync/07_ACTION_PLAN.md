# Action Plan — dev-knowledge session-sync (2026-05-12)

<!-- scope: meta -->

Future State per ADR-37 two-phase overlay. Source: Stage 2 OBJECTIVE + DIRECTIVES +
BOUNDARIES answers from old chat architect.

---

## OBJECTIVE

**Primary goal (operator-confirmed at session start):**

Fresh session should pick **one** of three operator-flagged M-scale items as primary
scope: **(a) hooks review, (b) skills review, or (c) token logging analysis**. These
were explicitly stated at prior session wrap as next-session work; each is M-scale
standalone, none depends on the others.

Architect's recommendation: **hooks review** as highest concrete value — operator
flagged Codex has two hooks both named `review` (concrete name-conflict bug, bounded
scope, immediate value). Skills review is broadest in scope; token logging addresses
an operator pain point (hook reportedly too slow during session tooling use).

**Mandatory smaller item (fold inline regardless of primary scope):**
Structure scrum-master review propagation process (PLAYBOOK section + cover-letter
template) — S-scale, BACKLOG entry exists, unblocks clean corp-monorepo second instance.

**Operator priority must be confirmed at session start** before primary scope locks in.

---

## DIRECTIVES

Execute in this order. Each directive: action + target + verification step.

**1. Confirm operator priority**
Ask operator which of hooks review / skills review / token logging they want as primary
scope. Do not lock scope without explicit operator confirmation.
*Verification: operator confirms primary scope in writing before execution begins.*

**2. Resolve working tree state**
Complete deletion of orphaned `docs/handoffs/2026-05-12-session-handoff/` folder
(single `.md` file, folder-with-one-file approach abandoned mid-session). Stage deletion,
commit.
*Verification: `git status` shows clean working tree post-commit.*

**3. Mark "Cross-repo handshake: ADR-34 amendment propagation to ai-council" BACKLOG P1 entry as DONE**
Cycle 2 closed this session — Turn 1 routed, Turn 2 received, Turn 3 closure routed.
Update BACKLOG.md status field. Commit.
*Verification: BACKLOG.md entry shows `[P1] [done]` with closure date and commit.*

**4. Structure scrum-master review propagation process**
Add PLAYBOOK.md section covering: Stage 1 strażnik audits → Stage 2 operator routes
(cover-letter template) → Stage 3 architect implements → addendum mechanism for
post-routing corrections. Also add cover-letter template to `templates/`.
*Verification: PLAYBOOK.md section present and navigable; cover-letter template file
exists in `templates/`. Scope-tag validator passes.*

**5. Execute primary scope**
Execute operator-confirmed primary scope (hooks review / skills review / token logging).
Apply scrum-master review pattern for cross-repo scope (e.g., skills review may require
review of skills across repos). Verification depends on scope chosen — define at execution.
*Verification: scope-specific output committed.*

**6. Check ai-council repo state for scrum-master review evidence**
(architect inference) Routine completion expected via CHANGELOG/commits. If CHANGELOG
and commits in ai-council show no evidence after reasonable interval, operator may need
to follow up. No browser-to-browser delivery turn expected per "handshake = 1 round trip"
principle.
*Verification: check ai-council CHANGELOG for entries referencing scrum-master review findings.*

**7. Note ADR-42 folder-vs-flat-file amendment candidate in BACKLOG**
Single-artifact handoff = flat `.md` file in `docs/handoffs/` was empirically established
this session. ADR-42 v3.2 folder format is for multi-artifact bundles. If not already in
BACKLOG, add a P3 item: "ADR-42 amendment — clarify single vs multi-artifact handoff format."
*Verification: BACKLOG.md has entry for this, or existing entry confirmed.*

**8. Apply N=2 codification gate**
Do NOT codify scrum-master review authority as ADR-44 this session. N=2 not yet reached
(corp-monorepo review = N=2 trigger). Structuring propagation process via PLAYBOOK section
is appropriate; new ADR is not.
*Verification: no new ADR-44 file in commits.*

---

## BOUNDARIES

Hard do-nots grounded in this session's witnessed patterns:

1. **Do NOT punt cleanup to "next prompt."** Punted-migration anti-pattern produced 13+
   meta-work commits before any file-level cleanup landed this prior session.
   Counter-pattern: do cleanup inline; expand scope only after current cleanup ships.

2. **Do NOT generate multi-turn handshake ceremony for S-scale cross-repo changes.**
   Operator principle: handshake = 1 round trip. Cycles 1 and 2 (4 turns each for 3-30 LoC
   changes) retroactively recognized as over-ceremony. Multi-turn = badly framed request.

3. **Do NOT ask operator to paste terminal output.** Three+ instances this session of
   browser chat defaulting to "send me PowerShell output" instead of generating Claude Code
   prompts. All read/write/inspect on repos delegates to Claude Code. Operator never the terminal.

4. **Do NOT accept target-repo CLAUDE.md / local config as "by-design" justification
   in cross-repo audits.** Universal convention applies wherever artifact exists. Local
   config can be wrong relative to ecosystem baseline — that is exactly what scrum-master
   review is for.

5. **Do NOT create patchwork audits.** When recommending new compliant pattern, simultaneously
   flag existing same-content-type non-conforming items. (Scrum-master review I8 failure
   mode: recommended `docs/audits/archive/legacy/` without flagging existing
   `docs/handoffs/_archive/` for rename.)

6. **Do NOT create folder-with-one-file artifacts.** Single-artifact handoffs = flat `.md`
   file. Folder format reserved for multi-artifact bundles with `contents/` subfolder.

7. **Do NOT write ADR-44 this session.** N=2 codification gate not yet reached. PLAYBOOK
   section for propagation process is appropriate; ADR creation is not.

8. **Do NOT touch ai-council files directly.** Cross-repo changes route to ai-council
   architect; architect implements in their own repo. Strażnik → operator → producer.

9. **Do NOT bundle hooks + skills + tokens reviews into one prompt.** Each is M-scale
   standalone scope. Bundling violates incremental-revertable-changes principle.

10. **Do NOT begin Phase 2 corp-monorepo structural migration before scrum-master review
    of corp-monorepo completes.** Review identifies findings; migration implements them.

---

## Success criteria

- Operator has confirmed primary scope (hooks / skills / tokens)
- Working tree is clean (orphaned deletion committed)
- ADR-34 cross-repo handshake BACKLOG entry marked done
- Scrum-master propagation process structured in PLAYBOOK + cover-letter template created
- Primary scope executed and committed
- All validators pass (`python scripts/validate_scope_tags.py`, `pre-commit run --all-files`)
- `git status` clean at session end
