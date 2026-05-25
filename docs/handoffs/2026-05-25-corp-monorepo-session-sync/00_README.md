# Handoff Bundle — corp-monorepo (session-sync)

**Handoff ID:** 2026-05-25-corp-monorepo-session-sync
**Type:** session-sync
**Generated:** 2026-05-25
**Format version:** v3.0

## What this folder is

This folder is a structured context bundle for handing off a corp-monorepo session to a new Claude browser chat. The prior chat accumulated context about safety-invariant architecture, conformance gap audit findings, and a prioritized action plan for the next session. This bundle preserves that knowledge so the new chat can begin without context loss.

This is a **cross-repo handoff**: the bundle was generated in `.dev-knowledge` (the governance repo) but targets `corp-monorepo`. Upload all 12 files to the new chat.

## Operator workflow

Follow these steps in order:

1. Open a **NEW** claude.ai browser chat. Do NOT reuse the old chat.
2. Upload all 12 files from this folder to the new chat.
3. Copy the full contents of `00_first-message.md` and send it as your first message.
4. Wait for the new chat to write its **4-item articulation** (role, current phase, immediate next action, top 3 Hard Constraints).
5. If the articulation is correct, reply **"role confirmed"**. If anything is wrong, correct it before confirming.
6. After "role confirmed", wait for the new chat to complete its **receiver synthesis**.
7. Review the synthesis for accuracy. Correct anything wrong before proceeding.
8. Ask any clarifying questions via the Q&A loop.
9. When ready, ask the new chat to generate formal Claude Code prompt(s) for the session work.
10. Download the prompt(s), open Claude Code in `corp-monorepo`, and run the prompt.

## File index

| File | Purpose |
|---|---|
| `00_README.md` | This file — upload instructions and bundle orientation |
| `00_first-message.md` | Copy-paste as first message in new chat |
| `01_MANIFEST.md` | Metadata, HEAD SHA, file index, drift verification instructions |
| `02_VISION.md` | corp-monorepo mission and scope (full copy) |
| `02b_ECOSYSTEM_VISION.md` | .dev-knowledge ecosystem context (cross-repo; full copy) |
| `03_PLAYBOOK.md` | Full methodology — how we work (full copy) |
| `04_ESSENTIALS.md` | High-leverage rules cheat sheet (full copy) |
| `05_GOVERNANCE_ESSENCES.md` | ADR operational rules relevant to this session's directives |
| `06_STATE_OF_PLAY.md` | Current state, completed work, deferred items, architect judgment |
| `07_ACTION_PLAN.md` | Next session goal, action plan, constraints, success criteria |
| `08_TREE.txt` | corp-monorepo file inventory (git ls-files snapshot) |
| `09_EXECUTION_EVIDENCE.md` | Empty return-trip template — fill after session execution |

## Notes

- The HEAD SHA is `32a47f85b07d697be20066c1ec69df3cf92cb1f6`. Before beginning work, verify this matches `git rev-parse HEAD` in corp-monorepo.
- `01_manifest.json` (in the same folder) contains SHA-256 checksums for drift detection. If any file was corrupted in upload, the checksums will not match.
- `09_EXECUTION_EVIDENCE.md` is intentionally empty — fill it after the session completes, then use it as input for the next handoff.
- The bundle was generated with no drift: Stage 1 SHA equals current corp-monorepo HEAD SHA.
