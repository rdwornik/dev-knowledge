# LANE G — Governance spine: R-F1 ADR → 8 births → F3 ADR draft

| Model | Mode | Effort |
|---|---|---|
| Opus (opusplan default) | Execute per this contract — **no plan mode**; the contract is the plan | High |

**Repo:** `.dev-knowledge` · **Branch:** `lane/g-governance` (cut fresh from `origin/main`) ·
**Substrate:** Codespaces devcontainer (**gates armed** — required) ·
**Session:** fresh CC session, boot via `/lane-boot` with this contract. Commit-and-**STOP** — never merge.

**Purpose.** The 2026-08-25 window landed a binding adjudication (`protocols/STANDING_RULINGS.md`
section U → `docs/audits/2026-08-25-technical-register-ruling-packet.md`) and deliberately birthed
zero rows. This lane makes births lawful (one ADR-111 amendment), spends 8 of the 29 banked
births, and drafts the F3 single-act ADR. Serves `[E4]`; authority = section U (immutable).

## Read first
`CLAUDE.md` · `protocols/STANDING_RULINGS.md` section U · the ruling packet it points at ·
`docs/decisions/` ADR-111, ADR-98, ADR-53, ADR-101 · `docs/intake/2026-08-05-func-simplification-distribution-wave.md`.
**Gotchas:** `PYTHONUTF8=1` on any bare console before audit/validate commands · `BACKLOG.md` is
GENERATED (ADR-107 §7.2) — edit `tasks/`, run `gen_task_tree.py`, never hand-edit · the
filing-backpressure hook demands a `kill-candidates:` line per added id · ADR numbering: derive
the next free id from `docs/decisions/` — never assume one.

## Git workflow
Branch from fresh `origin/main` · one commit per step at the COMMIT markers · run
`python scripts/audit.py health` + relevant validators before each commit · end state: branch
pushed, **STOP** — integration is a separate session.

## UNDERSTAND (before step 1)
- **Problem:** a completed adjudication with no lawful path into the backlog; ADR-111 knows only
  CANDIDATE → intake → ratification.
- **Scope:** ONE amendment + 8 rows + ONE Proposed ADR draft. Nothing else.
- **Risks:** (a) creating a laundering path — the two guards exist to prevent it; (b) scope creep
  into re-adjudicating section U — forbidden; (c) births before the amendment lands — order is
  mandatory.
- **Failure mode:** editing anything outside `docs/decisions/`, `docs/intake/`, `tasks/`.

## Steps

**1. ADR-111 amendment (the R-F1 ruling — verbatim substance, you own the form).**
Draft and land an amendment to ADR-111 stating: *an adjudication packet pointed at by
`STANDING_RULINGS.md`, carrying per-row reasons, satisfies the CANDIDATE → intake → ratification
funnel; direct births are legal only under such a packet*, with two guards: **(i)** every direct
birth cites the packet row id it derives from — one-to-one traceable; **(ii)** birth rights flow
only from a **landed, byte-identical** packet pointed at by `STANDING_RULINGS.md`; an unlanded or
editable packet confers none. Status: Accepted (architect ruling per ADR-108 §A, revertable).
**COMMIT.**

**2. Births — exactly 8 rows in `tasks/`, then regenerate.**
Derive each row's citing packet-row id **from the packet itself** (do not accept ids from this
contract — it deliberately names none). Each row carries: the packet row id per guard (i) ·
`kill-candidates:` line · owner/theme per repo convention:
1–4. Anchor rows for arcs **A, B, C, D** (one each, per section U §4 arc definitions).
5. **Green-by-skip sweep row** — Done-when cites the FROZEN artifact path
   `docs/audits/2026-08-25-green-by-skip-sweep.md` (authored by a sibling lane; the path is
   contract-frozen in both lanes — do not rename it, do not wait for it).
6. **v2.65 lockstep row** — Done-when includes BOTH: the §10 + `templates/claude-regions/*.md`
   lockstep act AND the C02 substance (procedure extraction from `CLAUDE.md` §6/§9).
7. **Suite RED #2 `anchor_gate_probe`** — disposition-investigation row (inherited failure, owner
   assigned, outcome = fixed or formally dispositioned).
8. **Suite RED #3 `export_backlog_view`** — L4 residual row: the `ecosystem/` naming-vs-reading
   carve-out (`ecosystem/conformance.{html,md}` name the check).
Run `python scripts/gen_task_tree.py` · `python scripts/validate_backlog.py`. **COMMIT.**

**3. F3 ADR — draft as Proposed, ONE-act design, no code edits.**
Draft the ADR that **supersedes ADR-53 D2** (single instruction file) **and amends the ADR-101
hermetization class** — designed to execute as ONE commit at acceptance. Embed the exact intended
`SANCTIONED_TIER1_FILES` diff **as specification text inside the ADR** (the enum is a closed set,
currently size 20; verify live) — but do **NOT** edit `scripts/` in this lane; the acceptance
commit is a follow-up act after adversarial review. Record: criterion MET on ≥2 strict providers
(Codex, Cursor read `AGENTS.md` natively, not `CLAUDE.md`); DeepSeek **unmeasured** — named as an
open input, not a blocker. This birth path itself must satisfy guard (i): cite the packet row.
**COMMIT.**

**Final.** Full validator pass (`validate_backlog`, `validate_doc_claims`, `audit.py health`) ·
push branch · write the lane report per `/save` convention (do not re-author its procedure) ·
**STOP.**

## Decision budget
Ask ONLY about: (a) curated-baseline touches, (b) genuine rule-vs-ruling conflicts, (c) fork
classes with no standing ruling. Everything else: decide per contract defaults, batch into ONE
end-of-lane packet. Standing rulings (`protocols/STANDING_RULINGS.md`) apply silently.

## What NOT to do
- Do NOT re-adjudicate any of the 37 packet rows (section U binding; supplement §3/§5 lists apply:
  no C34/C16/C06/C25 reopen, no [#362] enumeration, no [#242] before [#362]).
- Do NOT hand-edit `BACKLOG.md`; do NOT edit `scripts/`, `ecosystem/`, `CLAUDE.md`, or any Form-A
  region; do NOT birth a 9th row; do NOT touch ADR-114 (PARKED, operator-owned).
- Do NOT merge or touch `main`. Commit-and-STOP.
- **Sibling-hook clause:** end-of-session hooks may attribute a CONCURRENT session's commits to
  this lane and demand anchors for them — **decline with the stated reason** (hooks cannot tell
  sessions apart within a checkout). Do not repair another lane's state.
