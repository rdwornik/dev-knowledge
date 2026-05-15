# Handoff Bundle — ai-council (cross-repo-cleanup, 2026-05-15)

<!-- scope: meta -->

**Date:** 2026-05-15
**Type:** cross-repo-cleanup
**Target repo:** ai-council
**Format version:** v3.3.2 (ADR-42 three-stage flow)

This bundle drives a **Claude Code session in ai-council** that brings ai-council into
compliance with ADR-46 (dated-entries format) and ADR-47 (BACKLOG organization).
Migration decisions are locked — see `07_ACTION_PLAN.md` Hard Constraints.

---

## Operator workflow

1. Open Claude Code in the **ai-council** repo:
   `C:\Users\1028120\Documents\Dev\ai-council`
2. Start a new session (fresh context). Paste the content of `00_first-message.md` as the
   opening prompt.
3. The Claude Code session reads this bundle's context files (paths provided in prompt),
   executes the directives in `07_ACTION_PLAN.md`, and fills `09_EXECUTION_EVIDENCE.md`.
4. After ai-council session completes and commits, return to **.dev-knowledge** and run:
   ```
   python scripts/audit.py run
   ```
   Confirm ai-council shows no FAIL on the four checks.
5. Return the filled `09_EXECUTION_EVIDENCE.md` to this bundle directory:
   `docs/handoffs/2026-05-15-ai-council-cleanup/09_EXECUTION_EVIDENCE.md`
6. Flip Stream B P1 ai-council items in `.dev-knowledge` BACKLOG.md to `[done]`.

---

## File index (12 files)

| File | Purpose |
|---|---|
| `00_README.md` | This file — operator instructions |
| `00_first-message.md` | Opening prompt for ai-council Claude Code session |
| `01_MANIFEST.md` | Entry point, metadata, ai-council HEAD SHA pin |
| `01_manifest.json` | Machine-readable metadata + SHA-256 checksums |
| `02_VISION.md` | ai-council VISION.md — target repo's mission |
| `02b_ECOSYSTEM_VISION.md` | .dev-knowledge VISION.md — ecosystem methodology context |
| `03_PLAYBOOK.md` | .dev-knowledge PLAYBOOK.md — methodology reference |
| `04_ESSENTIALS.md` | .dev-knowledge ESSENTIALS.md — high-leverage rules cheat sheet |
| `05_GOVERNANCE_ESSENCES.md` | ADR-46 + ADR-47 full text; ADR-36 + ADR-31 excerpts |
| `06_STATE_OF_PLAY.md` | What landed in .dev-knowledge; audit findings; decisions locked |
| `07_ACTION_PLAN.md` | Directives for ai-council Claude Code session |
| `08_TREE.txt` | ai-council file inventory (`git ls-files`) |
| `09_EXECUTION_EVIDENCE.md` | Return trip template — ai-council session fills post-work |

---

## Notes

- This bundle implements ADR-42 v3.3.2 (three-stage flow)
- Cross-repo handoff (target ≠ .dev-knowledge): `02b_ECOSYSTEM_VISION.md` present
- Consumer is **Claude Code** (not browser chat) — no articulation gate or receiver synthesis required
- Migration decisions are locked — ai-council session must not re-debate them
