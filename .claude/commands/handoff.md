---
description: Generate or complete handoff per ADR-42 (amended through Q5) / HANDOFF_PROCESS.md v3.4 three-stage flow
---

Invoked by Rob saying one of:
- "Make handoff for {repo}" or "Make handoff for {repo}, type {type}"
- "Complete handoff for {repo}" or "Stage 3 for {slug}"
- "Save this response as stage 2 for {slug}"

When invoked:

1. Read `protocols/HANDOFF_PROCESS.md` (v3.4) for the full operational procedure.
   It is authoritative; this skill is a dispatch summary, not a substitute. Where
   they disagree, the spec wins and the divergence is a bug to fix.

2. Determine which action based on trigger phrase + state of
   `docs/handoffs/in-progress/{slug}/` (`{slug}` = `{YYYY-MM-DD}-{repo}-{type}`):

   | Trigger | in-progress state | Action |
   |---|---|---|
   | "make handoff" | No dir for slug (or empty) | Stage 1 |
   | "save this response as stage 2" | `stage1-question.md` exists, `stage2-response.md` is still the placeholder | Write `stage2-response.md` (+ `stage2-claims.md` if provided) |
   | "complete handoff" / "stage 3" | `stage1-question.md` + **populated** `stage2-response.md` exist | Stage 3 |

   **State detection is content-aware, not existence-only:**
   - Stage 1 pre-creates `stage2-response.md` (and a `stage2-claims.md` placeholder)
     as templates. Their mere existence does NOT mean Stage 2 is done.
   - Stage 2 is "done" only when content below the
     `═══ REPLACE EVERYTHING BELOW THIS LINE ═══` marker contains all 5 headings
     (`### 1. OBJECTIVE` … `### 5. BOUNDARIES`) with substantive content (not the
     `[old chat answer]` placeholder). If still placeholder → report "Stage 2 not
     yet provided" and do NOT proceed to Stage 3.
   - State ambiguity (both files populated but Rob says "make handoff" again):
     FLAG and ask — delete and restart, or proceed to Stage 3?

3. Execute the stage per HANDOFF_PROCESS.md procedure exactly.

4. Report to Rob: what was done, what file(s) created, what Rob does next.

5. Validators must pass; single commit per stage on a feature branch.

Stage 3 pre-flight gates — each is FLAG-and-STOP, never silent-proceed:
- **Stage 2 present:** `stage2-response.md` absent → STOP ("Paste browser-2 response first").
- **Thinness (M-5):** each of the 5 sections has ≥3 non-blank substantive lines below
  its heading; thinner → FLAG the offending section(s), ask proceed-or-return.
- **HEAD ancestry:** current HEAD must be a descendant of (or equal to) the Stage 1
  SHA in `stage1-question.md` — `git merge-base --is-ancestor {STAGE1_SHA} HEAD`.
  Exit 1 → FLAG both SHAs, ask proceed-or-abort.
- **Claims:** `stage2-claims.md` → `11_CLAIMS.md`; validate every citation (file
  existence + line-range locatability + decision-reference format). If missing,
  FLAG and STOP. If executor validation is unavailable, mark the bundle
  `UNVERIFIED` and require explicit operator acknowledgment — no silent bypass.

Critical constraints — violation is a process failure:
- ALL handoff types (audit-sync, session-sync, feature-X-sync) are 3-stage.
  No audit-sync shortcut. No implicit Stage 2. Period.
- Full VISION + PLAYBOOK + ESSENTIALS as the unconditional invariant floor
  (02/03/04 files). Only ADR essences in 05 — never full ADR copies, never the
  target repo's own ADRs.
- **13 fixed files flat** (self-applied) / **14 cross-repo** (adds
  `02b_ECOSYSTEM_VISION.md`), plus the generated `01_manifest.json` sidecar and any
  conditional `12_OPERATIONAL_*` operational-layer artifacts. No subdirectories.
  The v3.4 fixed set includes `10_GATE_PROBE.md` (CC-drafted applied-task probe +
  operator-only answer key, ADR-55) and `11_CLAIMS.md` (sender-produced load-bearing
  claims, ADR-58).
- `00_first-message.md` carries the applied-task gate (ADR-55) + the Prompt
  Generation Card (ADR-56). `01_MANIFEST.md` / `01_manifest.json` carry
  `next_session_scope` (ADR-57) + invariant canonical hashes (ADR-42 Q5).
- **Operational layer (ADR-57):** `12_OPERATIONAL_*` skills/gotchas/JOURNAL slices
  are included only as selected by the declared `next_session_scope` (controlled
  vocabulary: `code-implementation` / `architecture-decision` / `audit-work` /
  `documentation` / `mixed-uncertain`) via the published scope→artifact mapping.
  The governance floor is always full + unconditional.
- **Structured ratification (ADR-55/58):** bare `role confirmed` is decommissioned.
  Stage 3 hands off to operator ratification `role confirmed + probe passed`,
  checked against `11_CLAIMS.md` + CC's citation-validation report + the gate-probe
  answer key. Gate failure protocol: first fail → point to contradicted bundle
  location + one retry; second fail → terminate + regenerate upstream.
- Stage 1+2 inputs (`stage1-question.md`, `stage2-response.md`, `stage2-claims.md`)
  archived at `docs/handoffs/archive/{slug}/` (Move, not Copy), NOT inside the final
  folder.
