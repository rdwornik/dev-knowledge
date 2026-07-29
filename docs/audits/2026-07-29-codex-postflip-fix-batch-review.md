# Terra doc-lane review — post-flip stale-procedure fix batch + the two night artifacts

- **Class:** codex (ADR-101 enum) · **Date:** 2026-07-29 · **Slug:** postflip-fix-batch-review
- **Lane:** `gpt-5.6-terra` (doc-lane profile), codex-cli 0.145.0, `--sandbox read-only`
- **Arc:** MORNING BATCH 2026-07-29, branch `docs/postflip-stale-procedure-fixes`, reviewed at `1d9a0096`.
- **Serves:** the review leg owed by the night lane (cloud session had no Codex).

> **Invocation note (recorded, not silent).** Run as an ad-hoc `codex exec` with the wrapper's
> doc-lane profile and its pinned `-c model=gpt-5.6-terra`, **not** via `/codex-review`. Two reasons,
> both structural: (1) the fix diff contains `plugins/tier1-lifecycle/scripts/review_closures.py`,
> and the wrapper's code-vs-doc path-guard filters a mixed diff down to the code subset and reviews
> it with the **code** profile — the prose would not have been doc-reviewed at all (the `.py` change
> is docstring-only, i.e. prose wearing a code extension); (2) two of the three review surfaces
> (the intake-#18 dossier, the [#441] DRAFT block) are already on `main` and therefore outside any
> branch diff the wrapper can resolve. Profile text and severity bands are the wrapper's verbatim.

**Surfaces reviewed:** (1) the fix diff `main..1d9a0096` — audit rows 1–12; (2)
`docs/audits/2026-07-29-technical-intake18-ratification-dossier.md`; (3) the `[#441]` DRAFT block in
`protocols/PLAYBOOK.md` Ch8.

**Verdict: 0 Critical · 3 High · 1 Medium · 0 Low.** Two adopted-and-fixed, two dispositioned.

## Findings and dispositions

| # | Sev | Site | Finding | Disposition |
|---|---|---|---|---|
| H1 | High | `protocols/AI_COUNCIL_PROCESS.md:380` | New follow-up filing said "file it as a `tasks/` add" — hub-only shape stated universally, contradicting the host-shape branching the same item had just introduced for closure. Consumers have no `tasks/`. | **FIXED** — filing now branches by host shape (`tasks/` add on the hub, direct `BACKLOG.md` add on an unflipped consumer). Text this batch authored, so correcting it is inside row 11, not beyond the table. |
| H2 | High | `protocols/PLAYBOOK.md:3212` | ADR-65 done-item disposition claims "Closing a backlog item adds **no** new per-item write" — on the hub a closure *does* write (terminal `status:` on the retained task record). | **DISPOSITIONED — routed, not fixed.** Pre-existing line, **not** in the adjudicated table (the night audit swept this class and did not flag it), and this batch's contract is zero fixes beyond the table. Genuine pass-11 miss: the original clause means "no new *record-keeping* write" (no archive entry, no changelog line), which survives the flip, but the wording now reads as a mechanical claim that does not. Route to the next stale-procedure batch. |
| H3 | High | `protocols/PLAYBOOK.md:1295` | The `[#441]` DRAFT block is marked UNRATIFIED while simultaneously installing a normative default and *replacing* the prior three-check launch test; it also says "merging this branch IS the ratification act" — and that branch already merged at `14bcb1c4`. A reader cannot tell whether the four-condition test is binding. | **DISPOSITIONED — operator's call, not this batch's.** This is verbatim MORNING.md "Needs your word" item 2 ([#441] draft adoption + the condition-2 vs A5 conflict), which the morning-batch prompt did not delegate. The dossier's pack-level finding 2 and A5 row carry the reconciliation. Ratifying (or re-marking) the block is a ruling, not a fix. |
| M1 | Medium | `protocols/SESSION_SETUP.md:214` | "there is no status field to update" is false for the hub's retained task records, which require a terminal `status:`. | **FIXED** — reworded to "no `done` marker to set in the queue; a hub retirement instead sets a terminal `status:` on the retained `tasks/` record". Text this batch authored. |

**Not flagged (worth recording):** terra raised nothing against the intake-#18 dossier (surface 2) —
no disposition-faithfulness, cross-doc or structural finding across its 200 lines and 11 amendment
rows. It also raised nothing against rows 1–10 and 12 of the fix diff, i.e. the audit-row fixes
land as specified.

## Post-fix state

H1 + M1 fixed on this branch before merge. The silent-rule ratchet was re-measured after the fixes
(neither introduced a `must`/`shall`/`never` token). H2 and H3 remain open and are named here as the
record; H3 additionally stays live in MORNING.md's consumed brief via this file and the JOURNAL entry.
