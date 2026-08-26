# LANE RL v2 — Registry truth-up (presence-only) · filings · D3 · MEMORY check · B9 DISPATCH RUNBOOK

| Model | Mode | Effort |
|---|---|---|
| Opus (opusplan default) | Execute per this contract — **no plan mode**; the contract is the plan | Medium |

**Repo:** `.dev-knowledge` · **Branch:** `lane/rl-registry-filings` (from fresh `origin/main`) ·
**Substrate:** **LOCAL, primary checkout — required** (this lane measures vendor CLIs on the
operator's host; a codespace cannot see them) · **Session:** fresh CC session, boot via
`/lane-boot` with this contract. Commit-and-**STOP** — never merge (the primary stays the
integration site, but this lane does not integrate).

**Purpose.** Make the provider registry tell the truth about the host (presence-only), land the
five chat-only rulings from the 2026-08-25 supplement into durable homes, execute the operator's
D2/D3 rulings, and settle which surface `MEMORY.md` is before anyone compacts it. Serves
`[E4]`/`[E5]`; authority = section U + the 2026-08-25 measured provider table (immutable).

## Read first
`CLAUDE.md` · `ecosystem/` registry yamls + `ecosystem/disposition-register.yaml` (its own header
contract: one entry per WARN, keyed on the specific benign signature) · `protocols/PLAYBOOK.md`
(research-slate + window-mandate sections) · `protocols/HANDOFF_PROCESS.md` · `LESSONS.md` ·
`protocols/STANDING_RULINGS.md` section U.
**Gotchas:** `PYTHONUTF8=1` before audit/validate commands on this host (cp1252 fix lands in a
sibling lane — not merged yet) · registry records **presence, verdict basis, dates** — roles are
R3's, never this lane's · `agent.exe` is a poisoned name (byte-identical SHA256 to `grok.exe`) —
only unambiguous names are ever pinned.

## Git workflow
Branch from fresh `origin/main` on the primary checkout · one commit per step · validators before
each commit · push · **STOP**.

## UNDERSTAND (before step 1)
- **Problem:** the registry contradicts the measured host (dead CLI claimed live; a live,
  authenticated, first-on-PATH runtime entirely unregistered); five ratified rulings live only in
  a chat transcript; 14 predicted WARNs sit undispositioned; a 19.6 KB always-read file has an
  unverified owner.
- **Scope:** registry truth-up · filings · D3 disposition · D2 filing · MEMORY surface check +
  conditional compaction · **B9: the dispatch runbook**. Nothing else.
- **Risks:** (a) recording a ROLE verdict for `agy` — forbidden, R3 owns roles; (b) dispositioning
  anything beyond the 14 section-U-predicted `funnel_coverage` entries; (c) editing an L0 surface.
- **Failure mode:** writing outside `ecosystem/`, `LESSONS.md`, `protocols/PLAYBOOK.md`,
  `protocols/HANDOFF_PROCESS.md`, `protocols/DISPATCH_RUNBOOK.md` (new file — pre-approved by
  operator via B9), `protocols/HANDOFF_BOOT.md` (pointer line only), the bundle template (pointer
  line only) (+ `MEMORY.md` only if step 4 proves it repo-owned).

## Steps

**1. Registry truth-up — presence-only, re-measured live (never transcribed).**
Re-derive each fact on this host with the command, then record: Gemini CLI status (registry claims
live; measured server-refusal on this tier — record DEAD with basis+date) · Grok present but
`cli: null` — repair the entry · **`agy` (Antigravity) registered as PRESENT** with version,
auth state, PATH position, served model families — **presence/basis/dates only, NO role** — plus a
recorded note: admitting `agy` would give the refused `gemini-3.7-flash` family a second route,
which is a **`[#578]` rerun question, not a registry act** · Cursor: absent from disk and registry
— record the absence · the poisoned-name rule (`agent` never pinnable; SHA256 evidence reference).
**COMMIT.**

**2. D3 execution — disposition the 14 `funnel_coverage` WARNs (operator-ruled 2026-08-25).**
One entry per WARN in `ecosystem/disposition-register.yaml`, each keyed on its specific benign
signature per the register's own header contract, each referencing **section U** as the
adjudicating authority (the artifacts are the packet's own predicted landing cost). Exactly 14 —
nothing else gets dispositioned in this lane. Verify with a live `audit.py ship-gate` read
(expect the WARN count to fall by 14; record before/after in the lane report). **COMMIT.**

**3. Filings — supplement §7 + D2, each to its durable home.**
- LESSONS (dated 2026-08-25): **coordination tax** (11 lanes exceeded the useful ratio; feeds the
  4–6 mandate) · **research-as-procrastination** (three same-window instances) ·
  **smaller-fact-surface-at-the-architect** (16/16 asserted-not-measured errors; contracts name
  the command, never the fact).
- PLAYBOOK research-slate: land *"does the repo already own this?"* as an **executable checklist
  step** (a required grep/inventory action before any research is commissioned), not prose.
- PLAYBOOK window-mandate: **governance/product parity** (≥1 consumer-arc per window) as
  PROPOSED · **C12 icebox cap + one-in-one-out** as RULED-ADOPTED (operator, 2026-08-25).
- HANDOFF_PROCESS: design note — bundles shrink as mechanisms grow (smaller fact surface) · the
  supplement is the **outgoing seat's duty**, part of window close (§ supplement).
**COMMIT.**

**4. MEMORY surface check — verify, then act or hand off.**
Witness which file the ~19.6 KB flag concerns: `ls -la` + `wc -c` on any repo-root `MEMORY.md`
AND on `~/.claude/projects/<slug>/memory/MEMORY.md`. **If repo-owned:** compact here (preserve
content by archiving per repo convention, never silent deletion) — **COMMIT**. **If L0**
(`~/.claude/...`): make NO edit; record path+size in the lane report as an **operator act**, done.

**5. B9 — `protocols/DISPATCH_RUNBOOK.md` (REQUIRED; outgoing seat + operator escalation).**
Root cause, measured: ~30 consecutive browser seats could not launch lanes because the procedure
exists only as fragments (PLAYBOOK Ch8 doctrine · `/lane-boot` + `/lane-integrate` command files
proven present-but-unread by the V1 census · `Dispatch-CloudV2`, an **L0** PowerShell profile
function the repo cannot see). Author ONE page, three sections — **local / CC-cloud / Codespaces
devcontainer** — each stating VERBATIM what the operator types or clicks to launch a lane, where
the lane prompt file lives (pasted / passed as file / picked up by `/lane-boot` from a path), and
the **receipt that proves dispatch succeeded**. **Source it from the verbatim pull artifact
(file:line quotes) delivered with this contract — never from memory.** Where mechanics live in L0
(`Dispatch-CloudV2`): record the function's CONTRACT and mark it operator-owned — do not copy or
reimplement it in-repo. Then TWO pointer lines so it can never be unread again: one in
`protocols/HANDOFF_BOOT.md` (the browser's first read) and one in the bundle template.
**Done-when: a fresh seat can dispatch a lane on any substrate from this page alone, with zero
questions to the operator.** **COMMIT.**

**Final.** Validators green (`PYTHONUTF8=1`) · push · lane report per `/save` convention —
including the ship-gate before/after and the MEMORY verdict · **STOP.**

## Decision budget
Ask ONLY about: (a) curated-baseline touches, (b) rule-vs-ruling conflicts, (c) unruled forks.
Filing wording is yours; rulings' substance is fixed. ONE end-of-lane packet.

## What NOT to do
- Do NOT record any role/admission verdict for any provider — presence only; R3 owns roles.
- Do NOT disposition anything beyond the 14 named entries; do NOT touch the register's standing
  entries (ADR-75 decoration rule surfaces them by design).
- Do NOT edit an L0 surface (`~/.claude/...`) under any framing; do NOT delete registry content
  without asking (P1 hard trigger) — repairs amend, absences are recorded as absences.
- Do NOT touch `scripts/`, `docs/decisions/`, `docs/intake/`, `tasks/`, `BACKLOG.md`, `CLAUDE.md`.
- Do NOT author the runbook from memory or from chat prose — the verbatim pull artifact is the
  ONLY source; a section whose mechanics cannot be quoted file:line is written as a named GAP,
  not filled in.
- Do NOT merge. Commit-and-STOP.
- **Sibling-hook clause:** end-of-session hooks may attribute a CONCURRENT session's commits to
  this lane and demand anchors — **decline with the stated reason**.
