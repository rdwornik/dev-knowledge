---
description: Generate or complete handoff per ADR-42 v3.1 three-stage flow
---

Invoked by Rob saying one of:
- "Make handoff for {repo}" or "Make handoff for {repo}, type {type}"
- "Complete handoff for {repo}" or "Stage 3 for {slug}"
- "Save this response as stage 2 for {slug}"

When invoked:

1. Read `protocols/HANDOFF_PROCESS.md` (v3.1) for the full operational procedure.

2. Determine which action based on trigger phrase + state of
   `docs/handoffs/_in_progress/{slug}/`:

   | Trigger | _in_progress state | Action |
   |---|---|---|
   | "make handoff" | No dir for slug | Stage 1 |
   | "save this response as stage 2" | stage1-question.md exists | Write stage2-response.md |
   | "complete handoff" / "stage 3" | Both stage1 + stage2 exist | Stage 3 |

3. Execute the stage per HANDOFF_PROCESS.md procedure exactly.

4. Report to Rob: what was done, what file(s) created, what Rob does next.

5. Validators must pass; single commit per stage on feature branch.

Critical constraints — violation is a process failure:
- ALL handoff types (audit-sync, session-sync, feature-X-sync) are 3-stage.
  No audit-sync shortcut. No implicit Stage 2. Period.
- Stage 3 MUST NOT run if stage2-response.md is absent — FLAG and STOP.
- Stage 1 captures target repo HEAD SHA; Stage 3 verifies vs current HEAD.
  Drift = FLAG both SHAs to Rob, ask whether to proceed.
- Full VISION + PLAYBOOK + ESSENTIALS as invariants (02/03/04 files).
- Only ADR essences in 05 — never full ADR copies, never target repo ADRs.
- 11 files flat in final folder — no subdirectories.
- Stage 1+2 inputs archived at docs/handoffs/archive/{slug}/, NOT inside final folder.
- State ambiguity (both files exist but Rob says "make handoff"): FLAG and ask.
