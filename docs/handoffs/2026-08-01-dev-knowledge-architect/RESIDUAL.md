# Residual — 2026-08-01-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**Everything standing is standing for a recorded reason; this window introduced no new
undispositioned flag that survived it.** Re-derive the live picture at P7/P4 — the lines below say
only *which families exist and who owns them*.

- **Fleet-parity, ai-council root `conftest.py`.** Dispositioned in
  `ecosystem/disposition-register.yaml` under **[#430]**, which owns the underlying defect (a
  consumer-role template that rejects standard pytest practice, plus a verdict that depends on
  another repository's working tree). Standing, not new.
- **The same fact has a NON-dispositionable twin in the suite.** `test_check_fleet_parity_green_on_live_repo`
  calls the check directly and asserts the stricter property, so the register is invisible to it —
  the gate and the suite encode different definitions of green (LESSONS 2026-07-26). Together with
  a stale routine-consumers pin, this is the pair filed as **[#457]**. Both are left RED and
  UNMARKED by standing operator ruling — no skip, no xfail, no deselect. **Expect them; they are
  owned, not forgotten.**
- **Self-induced, repaired within the window, NOT dispositioned:** two WARNs this arc created
  itself (a generated count left un-regenerated after a test-adding commit; a freshly-filed row
  carrying repeated same-day date stamps) were cleared **by fixing the content**, in their own
  `--no-ff` cycle. Recording the method matters more than the instances: a self-induced WARN is
  repaired, never dispositioned.
- **Read the register before triaging anything P7 surfaces** — a flag with a row against it is not
  a finding, it is a known cost with an owner.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
**One arc shipped end-to-end: [#382], the [E9] North Star's first build arc — CLOSED.** Detail is
in `JOURNAL.md` entries (l)–(s) and the audits named below; this is the map only.

- **[#382] CLOSED** (ADR-70 operator confirmation) — four waves, four `--no-ff` merges: ADR-109
  accepted → schema v1 under `ecosystem/schema/` → loader over the live registry sources →
  divergence report. Retire-not-delete: the task file remains as the allocation record with a
  terminal status; only its manifest node left.
- **ADR-109 (new, Accepted)** — *Fleet desired-state contract v1*. Rules the "four registries"
  enumeration the North Star asserted for ten days without naming, dispositions all seven ADR-107
  §5 schema findings, records obligation-3 DISCHARGED, and carries a **generality-pending** clause
  (§4) that is the next window's payload — see §4 below.
- **Intake movement:** #16 trigger fired → `disposition: active` with a NOTE-pointer, deliberately
  **NOT** flipped CONSUMED (its §6 plan spine stays live — a doc-level status must not over-claim
  partial consumption); #22 gained a §E→ADR-109 ratification NOTE and stays SEED.
- **Rows filed this window:** **[#457]** (two standing test failures), **[#458]** (gates and
  commits never race in one tree), **[#459]** (ARCHITECTURE prose for the new organ class +
  codemap-scope ruling), **[#460]** (night-routine dailies: keep / aggregate / stop), **[#461]**
  (mechanize the six window metrics). **[#344]** gained an `ai-council` repo prefix on its
  cross-repo citation.
- **LESSONS append:** *push is part of the act it verifies* — this act's own miss, named rather
  than quietly repaired.
- **Night-material resolution (2026-07-31 night, operator-authorized in full):** the three
  `claude/conformance-*` digests merged to `main` oldest-first (preserve-then-delete) and the
  branches deleted origin-side; their live findings absorbed the same night — ARCHITECTURE
  ADR-currency fixed, **[#462]** (terminal-setup membership gap) filed, uv-pin HIGH confirmed
  owned by [#453] item (2). `automation/fleet-audit` deep-reviewed read-only (98 commits, 36
  digests): **[#463]/[#464]/[#465]** filed, **[#460]** rewritten from open question to a recorded
  recommendation. The fleet-audit branch itself is untouched — report-only.
- **Audit artifacts** (all in `docs/audits/`, 2026-07-31): the **ladder evidence pack**
  (`verification-382-ladder-evidence` — L0–L5 answered from `main` with an anchor per level, plus
  the night-routine census and the six metrics), the **arc educate report**
  (`technical-382-arc-educate`), the **§C/§H grok shadow A/B** record, and three terra reviews
  (W2 schema, W3 loader, W4 report).

**Navigate from `BACKLOG.md`** — themes `[E9] Fleet Desired-State System` and `[E7] Tooling &
evaluation` — not from this list.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
### The frontier: [#383] wave 1 — and it carries a debt that is not obvious from the row

[#382] closed, so **[#383] execution waves per surface** is the live front. What the row does not
say, and what must not be rediscovered: **[#383] wave 1 carries the generalization discharge** for
ADR-109 §4 / ADR-107 §6.2. The contract shipped this window is **explicitly NOT declared general** —
one governed surface has been split by the engine pattern; a second has not. The discharge criteria
are fixed and quoted verbatim in ADR-109 §4, and the bar is *shown, not argued*: a **committed
round-trip proof** on a second surface — per-item frontmattered files, byte-exact identity, a
residue manifest, green regen-and-diff. Named candidates in order of cheapness: `docs/intake/*.md`
(already frontmattered, already status-indexed) and the `[E8]` ruling register (the surface whose
rot in a queue file motivated the restructure). **Choosing wave 1 to satisfy that clause is the
cheapest way to discharge it; choosing anything else leaves the fleet contract's generality claim
open indefinitely.**

### Open decisions the next window inherits (each needs a ruling, not a build)

1. **The three `claude/conformance-*` branches — RESOLVED 2026-07-31 night, operator-authorized.**
   Merged to `main` oldest-first (preserve-then-delete; the three digests now live in
   `docs/audits/`, index regenerated), branches deleted origin-side. Their live findings were
   absorbed the same night: the ARCHITECTURE ADR-currency line fixed, **[#462]** filed for the
   terminal-setup membership gap, the uv-pin HIGH confirmed already owned by [#453] item (2).
   Nothing here awaits a ruling.
2. **[#460] — now carries a RECORDED RECOMMENDATION; the ruling is still the operator's.** The
   2026-07-31 night deep review read all 98 unread `automation/fleet-audit` commits: the lane
   detects real defects — nine still live today, absorbed as **[#463]** (win-tooling debt),
   **[#464]** (corp-*/ai-council drift), **[#465]** (the writer's own integrity defects) — but its
   branch-commit leg has been **dead since 2026-07-16** and nothing noticed. Recommendation on the
   row: stop the branch lane, keep the SessionStart digest, add a persistence-triage consumer
   (ADR-105). The sequencing constraint stands: rule [#460] before putting the divergence report
   on any cadence.
3. **[#459] — ARCHITECTURE prose, NARROWED 2026-07-31 night.** The ADR-currency leg landed (the
   Purpose line reads "through ADR-109"; Governing ADRs carries ADR-108 + ADR-109 bullets). What
   remains is the organ-class prose: `ecosystem/schema/` + the loader/report pair are still absent
   from Ch2/Ch6, and the ruling inside it is not trivial — `ecosystem/schema/` sits **outside**
   the codemap's `--source-root scripts` scope, so the same edit must rule whether the source-root
   widens or the schema package is declared out-of-codemap **with a reason**.
4. **Does the divergence report earn a durable artifact and a declared consumer?** Today it prints
   to stdout on human invocation only — nothing schedules it, nothing reads it, no artifact is
   committed. Under ADR-105 it cannot *activate* without a named consumer + consumption_path. That
   is a decision about whether the report is a tool or an organ.
5. **§H portability — the builder lane is still untested.** Derivation and review ran
   multi-provider this window (sol derived the schema independently; terra and grok each landed
   accepted Criticals; CC built). **Every line of shipped code was written by Claude.** The probe
   the operator specified — one full arc with a non-Claude builder — remains unrun, with three debt
   items recorded verbatim in the §C/§H artifact.
6. **RESOLVED 2026-07-31 night — both former unabsorbed conformance findings are absorbed.** The
   ARCHITECTURE "through ADR-107" line now reads ADR-109 (with Governing bullets), and the
   terminal-setup gap is **[#462]** — deliberately reframed for **[#383] wave 1**: per ADR-109 §2
   `registry.md` loses authority, so the fix is the wave-1 desired-state member set carrying the
   full ADR-104 declaration (census method: declaration diffed against machine surfaces), not a
   hand-added registry row. The structural lesson is in the row.

### The honest ceiling, so the next window does not re-estimate it

The tech-currency lane (L4: the uv/venv fleet rollout, Gemini activation, the repomix distiller)
totals **4–7 windows** and is **serialized behind [#383]**, not parallel to it — Gemini cannot
activate until [#383] supplies the read-heavy consumer ADR-105 requires. Methodology
versioning/deployment (L2) is a further 3–5. Full derivation, level by level with anchors, is in
the ladder evidence pack; it is the input to any roadmap conversation this window opens, and it
should be argued with rather than re-derived.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
