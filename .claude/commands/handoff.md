---
description: Generate or complete a handoff per HANDOFF_PROCESS.md v6 — CC-owned residual + thin browser boot
---

Invoked by Rob saying one of:
- `please create handoff for <repo>` — generate the bundle
- `complete handoff for <repo>` — finalize (fold the filled supplement, re-assemble)

`<repo>` defaults to `.dev-knowledge` (self-handoff). A different repo name is a
cross-repo handoff (read-only on the target — ADR-36/41).

**Source of truth:** `protocols/HANDOFF_PROCESS.md` (v6, canonical). This skill is a dispatch
summary, not a substitute. Where they disagree, the spec wins — fix the divergence.

## Modes & exact invocation (operator copy-paste)

The natural-language `/handoff` triggers above drive the **architect | execution** interview
lifecycle. All four bundle shapes are one generator, `scripts/gen_handoff.py --mode <mode>`,
which the operator can also invoke directly (run from the repo root). **When-to-use runbook —
the single home:** PLAYBOOK §8 "How to hand off". Exact syntax, one copy-paste example per mode:

**architect** — planning / reshaping the way-of-working (§13).
```
python scripts/gen_handoff.py --mode architect
```
→ `docs/handoffs/<slug>/`: `SUPPLEMENT.md` + `HANDOFF_BOOT.md` + `RESIDUAL.md` + `PROBES.md` + `PASTE_THIS.md`. Paste **`PASTE_THIS.md`** into a fresh Claude.ai chat.

**execution** *(default)* — advancing a named backlog item (§13).
```
python scripts/gen_handoff.py --mode execution
```
→ same minus `SUPPLEMENT.md` (`HANDOFF_BOOT` + `RESIDUAL` + `PROBES` + `PASTE_THIS`). Paste **`PASTE_THIS.md`**.

**epic** — one epic lane in a root-provisioned worktree (§14a).
```
python scripts/gen_handoff.py --mode epic --epic-slug 278-test-suite-hygiene
```
→ `docs/handoffs/<slug>/`: `EPIC_BOOT.md` + `PROBES.md` + `EPIC_RETURN.md` (no `PASTE_THIS`). Paste **`EPIC_BOOT.md` + `PROBES.md`** into the fresh epic chat.

**developer** — additive alias of `epic` (ADR-98; §14). Byte-identical bundle; `{{MODE}}` renders `epic` until the deferred naming flip.
```
python scripts/gen_handoff.py --mode developer --epic-slug 278-test-suite-hygiene
```
→ same as epic; same paste.

**functional** — requirements intake, **no probes** (§16).
```
python scripts/gen_handoff.py --mode functional
```
→ `docs/handoffs/<slug>/FUNCTIONAL_BOOT.md` (one file). Paste **`FUNCTIONAL_BOOT.md`** alone into a fresh functional-architect chat.

**Arguments.** `--epic-slug <epic-slug>` (epic / developer only): the epic name — sets branch
`epic/<epic-slug>` + worktree `epic-<epic-slug>`; kebab-case, no spaces; defaults to the bundle
slug. In PowerShell single-quote it: `--epic-slug '278-test-suite-hygiene'`. `--slug <name>`
overrides the bundle folder (default `<date>-<repo>-<mode>`); `--repo` / `--date` override the
display name / date; `--no-assemble` skips `PASTE_THIS` (architect / execution). Consuming a
generated bundle (booting the browser) is `docs/handoffs/README.md`.

## v5/v6 (canonical — default flow; HANDOFF_PROCESS v6 / ADR-82)

HANDOFF_PROCESS **v6** is canonical at `protocols/HANDOFF_PROCESS.md` (CC-owned handoff,
thin browser boot, teeth-y forced read — model C) since the #149 flip (2026-06-11; v4.4
archived to `protocols/archive/HANDOFF_PROCESS_v4.4.md`). The v5 lineage is the **default** flow;
**v6** (2026-07-31, [#446]) reshapes only the *transport*: one CC-side `/handoff-verify` run emits
ONE evidence block the operator pastes once. Generation is unchanged and stays answer-free.

> **v4 two-phase mechanics removed (#164 leg g).** The v5 generator (`scripts/gen_handoff.py`)
> has replaced the old 8-file two-phase interview, so the hand-copied v4 `## Conventions` /
> `## Phase 1` / `## Phase 2` / `## Hard constraints` prose is gone from this file — it was the
> exact "hand-copied process that drifts" the v5 self-updating rule below forbids. The v4
> mechanics survive intact, un-duplicated, at their immutable homes for any legacy v4 cross-repo
> handoff: the spec `protocols/archive/HANDOFF_PROCESS_v4.4.md` + the retained bundle templates
> `templates/handoff/01_ROLE…07_ASK_BACK.md.tmpl` + `templates/handoff/README.md.tmpl`
> (kept live for cross-repo v4 per ADR-83; `docs/handoffs/README.md` "Format eras").

**Self-updating — the #148(c) rule, applies to BOTH modes.** This command carries **no
hand-copied process or methodology.** At handoff time it pulls live:
- the **current process** — read the canonical spec header for version/status (never
  hardcode); `protocols/HANDOFF_PROCESS.md` is the canonical source of truth;
- the **methodology** — as **pointers** to `PLAYBOOK` / `ESSENTIALS` / `CLAUDE.md`, never as
  copied prose (a hand-copy drifts — the `/review` vs `/codex review` class).

**v5/v6 behavior** (governed by `protocols/HANDOFF_PROCESS.md` — read it, don't restate
it here):
- Emit the **residual** to `docs/handoffs/<slug>/` — un-committed reasoning + pointers +
  **drift-flags as the headline** (from `validate_doc_claims` #89 + `validate_git_backlog`
  #90 + the state read).
- Emit the **thin boot** — point the operator at `protocols/HANDOFF_BOOT.md` (the browser's
  whole boot; the browser operating role travels with it — never assume a CC-held file
  reaches the file-less browser).
- Emit the **probe manifest** — questions + source-locators + verification commands, **never
  the answers**; CC runs the commands against live state at the comprehension gate and
  PASS/FAILs each (any FAIL blocks onboarding).
- Lean **task-state** — a pointer to `BACKLOG.md` + live branches + any drift-flag; never
  re-narrated IDs.

**Mode: `architect | execution`** (governed by `protocols/HANDOFF_PROCESS.md`
§13 — read it, don't restate it here). The generator takes an optional mode parameter, default
`execution`, selecting the residual **profile** + browser **posture**. Parse it alongside the
`v5` flag: `… v5` / `… v5 execution` → execution; `… v5 architect` → architect. Mode applies
**only** in the v5/v6 lineage — v4.4 has no modes. Three further generator flags exist
(`scripts/gen_handoff.py`, not §13 residual profiles): `epic` (§14a scope-contract bundle),
`developer` (additive alias of epic per ADR-98 — bundle header renders `epic` until the
deferred naming flip), and `functional` (§16 one-file intake-capture boot, no probes).
- **execution** — the four emissions above, unchanged (lean residual + thin boot + probe
  manifest + pointer task-state); the browser gets the §7 reactive-filter role.
- **architect** — re-profile the residual for a *planning* session: scope it to the planning
  "why" + the open architecture questions; task-state points at the **whole `BACKLOG.md` /
  relevant theme** (the task-graph, carried as residual prose — the ADR-66 schema encodes no
  dependencies/parallelization this pass, so do **not** claim a durable graph; durable encoding
  = #156). Add the **orientation probe** — a §5 *exact-line-quote* probe bound to `VISION.md`
  `## Vision` + `ARCHITECTURE.md` Ch1: ship the source-locator + the substring-check command,
  **never the line** (generator-excluded); CC reads the **live** file and substring-checks the
  architect's quote — never a paraphrase. CC serves the **generative/decompositional** posture
  from `HANDOFF_BOOT.md` so the role reaches the file-less browser. Return channel stays §2/§6 —
  emit **no** new *return-leg* artifact.
- **architect — strategic supplement (always-generated fillable file; §13 "Architect strategic
  supplement").** **Always write `docs/handoffs/<slug>/SUPPLEMENT.md`** (architect mode,
  **unconditionally**) from `templates/handoff/v5/SUPPLEMENT.md.tmpl` — the fixed 7-question *why*-only
  schema interpolated with the bundle's slug/repo/date (you MAY append 1–2 session-specific items you
  observed as `A./B.` addenda after Q6; add nothing else). The file is **self-documenting + fillable**:
  an operator 3-step header, a **QUESTIONS** section for the **outgoing** architect chat, and an empty
  **ANSWERS** section below the divider. **Commit it on the handoff branch** (empty or filled) for
  durable tracking — so the artifact exists even for a cold/`/clear`ed handoff (no missing-deliverable
  look). The operator pastes the QUESTIONS to the outgoing chat, pastes the answers back below the
  divider, and says **`supplement filled`**; you then commit the filled file and re-run
  `scripts/assemble_paste.py`, which folds the **ANSWERS region only** into the next `PASTE_THIS` —
  **only when non-empty** (an empty ANSWERS section is the defined cold-handoff disposition: not folded;
  the incoming §13(d) beat fires full). The supplement is **advisory** (never teeth), asks **only**
  non-re-derivable *why* — never repo state / methodology / task-state — and you **never fabricate
  answers** (unanswered = committed empty). It is a **forward** brief, not the return leg above. Full
  mechanism + schema: `protocols/HANDOFF_PROCESS.md` §13 — read it, don't restate it here.
- **Supplement ↔ the one-block boot ([#446] §B(b), v6).** The 7-question schema is **unchanged** by
  the one-round-trip reshape, and it stays **outside** the evidence block: the supplement is the
  operator's *forward* brief, filled **before** the next session boots, whereas the block is CC's
  *check-time* output. What the reshape changes is how a folded answer is treated **on arrival**,
  and the split is **narrow on purpose**: `/handoff-verify`'s `Inherited claims` row verifies only
  a supplement answer that **asserts a repo-verifiable fact** (a count, a sha, a file's state, "X
  landed") — those are checked CC-side against the live repo, and a contradicted one is a FAIL.
  The supplement's *actual* payload — intent, tensions weighed, options rejected, off-repo context
  — has **no live repo source by construction**, stays **advisory**, and is **never** failed for
  being unverifiable. Verifying the unverifiable would make every filled supplement blocking,
  which would invert the §13 contract that the supplement is advisory and never teeth.

**Architect-mode completion output (lead-by-hand — keep it SHORT, not a dense dump).** When the
architect bundle is ready, end with this concrete message (substitute `<slug>`):

```
Handoff bundle ready: docs/handoffs/<slug>/  (paste PASTE_THIS.md into a fresh chat to start the next session)

To capture this session's strategic "why" (optional but recommended):
  1. Open docs/handoffs/<slug>/SUPPLEMENT.md
  2. Paste its QUESTIONS into the outgoing architect chat; paste answers back below the line
  3. Tell me `supplement filled` -- I'll commit it and fold it into the next PASTE_THIS

Operator-gated, mine to run on your OK: push main; -d the merged stragglers
```

## Legacy v4 cross-repo handoffs (pointer, not mechanics)

The v4 two-phase 8-file interview mechanics that used to live here are **removed** (#164
leg g) — see the blockquote under *v5 (canonical)* above. For the rare legacy **v4
cross-repo** handoff (a v4 repo not yet on the v5/v6 lineage), do not re-derive the flow from memory:
read the frozen spec and drive the retained templates directly.

- **Spec (frozen):** `protocols/archive/HANDOFF_PROCESS_v4.4.md` — the full two-phase
  interview + consolidate mechanics, immutable per ADR-83.
- **Templates (retained live):** `templates/handoff/README.md.tmpl` +
  `templates/handoff/01_ROLE…07_ASK_BACK.md.tmpl` — kept for cross-repo v4 per ADR-83
  (`docs/handoffs/README.md` "Format eras & navigation").

Everything else (self-handoff, and every mode `architect | execution | epic | developer |
functional`) is **v6** — governed by the sections above + `protocols/HANDOFF_PROCESS.md`.

