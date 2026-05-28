# Ecosystem Cross-Doc Harmony — scratch (2026-05-29)

<!-- scope: meta -->

Overnight ecosystem-coherence audit, Phase 6. Read-only: do JOURNAL, PLAYBOOK,
ESSENTIALS, CLAUDE.md, LESSONS.md tell the same story about recent
decisions/conventions?

## Same-facts test (Dimension A) — 3 spot-checked facts

| Fact | PLAYBOOK | ESSENTIALS | Verdict |
|---|---|---|---|
| Mermaid theme v2 (ADR-51 amendment 2026-05-28; audit.py check #7) | :2763 — full, "ADR-51 amendment 2026-05-28 (v2)", "check #7 `mermaid_theme_directive`" | :268-271 — same wording, same ADR, same check #7 | **coherent** ✓ |
| audit.py = 7 checks | references "check #7" | references "check #7" | **coherent** ✓ (matches actual 7-function audit.py) |
| Handoff v3.4 | (not restated — defers to HANDOFF_PROCESS) | (not restated) | **CLAUDE.md disagrees — see CD-1** |

## Findings

| ID | Sev | Dim | Evidence (file:line) | Description | Fix scope | Owner |
|---|---|---|---|---|---|---|
| CD-1 | medium | A/B/D | `CLAUDE.md:94` | The `/handoff` command description says "generate/complete handoff per **ADR-42 v3.3.3** three-stage flow." Stale: the spec (`HANDOFF_PROCESS.md` v3.4), the rewritten skill (`.claude/commands/handoff.md`), and `ARCHITECTURE.md` are all v3.4. This is the **same straggler class** as the abort root cause, and was **outside** the 13-finding fix-campaign scope (campaign covered the spec/skill/templates/ADRs, not CLAUDE.md §7's command blurb). | One-line edit: `v3.3.3` → `v3.4` in CLAUDE.md §7. | self |
| CD-2 | low | B | `CLAUDE.md:148` vs `:144` | Footer "**Last updated:** 2026-05-24" contradicts the §12 section-history entry "v2.3 (2026-05-28)". The last edit (v2.3) didn't bump the footer date. Minor self-inconsistency. | Bump footer to the latest §12 history date on next CLAUDE.md edit (fold in with CD-1). | self |

## Version / reference integrity (Dimensions B, C)

- **ADR refs (CLAUDE §11 → files):** ADR-57/58/59/60/61 all exist on disk — §11
  references resolve. ✓
- **ESSENTIALS ↔ PLAYBOOK alignment** (CLAUDE.md §6 invariant): the spot-checked
  shared facts (mermaid v2, audit #7) are summarized in ESSENTIALS and detailed in
  PLAYBOOK with no divergence. The "summarizes-not-copies" invariant holds for the
  sample. ✓
- **No handoff file-count drift in narrative docs:** the 11/12/13/14 count question
  lives only in the spec/skill/template (all reconciled to 13/14 this session); it
  does not leak into CLAUDE/PLAYBOOK/ESSENTIALS. ✓
- **LESSONS.md v3.2 references** (`:109`, `:167`, `:171`): correct **append-only
  historical** record of what v3.2 did at the time (dated 2026-05-11). NOT stragglers
  — leaving them is correct per the append-only invariant. ✓

## Recency (Dimension D)

PLAYBOOK + ESSENTIALS reflect the 2026-05-28 mermaid-v2 / audit-#7 arc; CLAUDE.md §11
reflects ADRs 57–61. The only recency lag is CLAUDE.md §7 (CD-1) + the footer date
(CD-2) — both predate the 2026-05-26 v3.4 cutover. The day's v3.4 fix campaign +
this ecosystem audit are not yet in these living docs, which is expected (they land
via JOURNAL/BACKLOG, not per-session edits to PLAYBOOK/ESSENTIALS).

## Notes

- CD-1 is the headline: the abort post-mortem named the v3.3.3-straggler pattern, and
  here is one more instance the fix campaign's scope didn't reach. Worth a fast
  follow-up edit and worth flagging as evidence the straggler sweep should include
  CLAUDE.md §7 next time.
