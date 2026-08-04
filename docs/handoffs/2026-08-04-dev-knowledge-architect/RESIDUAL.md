# Residual — 2026-08-04-dev-knowledge-architect — the part the repo does not already encode

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
**All drift-flags carried out of this window are STANDING and dispositioned — none is new.** Their
entries live in `ecosystem/disposition-register.yaml`; read the live set through P7/P4 rather than
from here.

- **Standing, register-backed.** The dispositioned set is unchanged in *kind* from the window's
  start: the `undeclared_edges` family against `handoff-process` (ref `#241`), the
  `no_ff_merges` journal-wrap/transcript-archive entries, the `reconciled_versions`
  CONTRIBUTING-template entry (ref `#335`), and the `fleet_parity` ai-council root `conftest.py`
  entry (ref `#430`). Every one predates this window.
- **Nothing was dispositioned this window.** Three self-induced WARNs appeared during the arcs —
  each a BACKLOG row crossing the gross-character ceiling as it absorbed status text — and each
  was **trimmed, never dispositioned**. That is the standing rule (`PLAYBOOK` "the row carries a
  pointer, the record carries the record"): the ceiling is the mechanism saying the content is in
  the wrong container, and every historical `warn-doc-rot-backlog-*` register entry is `(cleared)`.
- **The suite's standing failure pair is `[#457]`** — two live-repo tests, unchanged all window,
  and deliberately not skipped/xfailed. Treat any *third* failure as new; the pair itself is the
  known baseline. P6 re-derives the live set.
- **One hard-fail organ is expected to be live at read-time and is not drift**: the ADR-85
  `journal_spine_anchor` backstop flags the most recent anchor-fix merge until the NEXT JOURNAL
  entry names what it introduced. This is the `[#447]` self-referential-gate family — *the
  committing act cannot satisfy the gate's own precondition* — already filed, not a new defect.
  See §4.

**Do not read a verdict from this section.** It names *classes and references only*; the
ship-gate verdict, the dispositioned-WARN count, the `[stale]` status and any drifted id are
P7/P4's live answers by design.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Map only — `JOURNAL.md` entries **2026-08-03 (h)–(l)** and **2026-08-04 (a)–(g)** carry the detail.

| closed | what |
|---|---|
| `[#479]` | SUPERSEDED — its Done-when died with ADR-85's FR5; closed on substance |
| `[#472]` | ADR-104's fleet declaration became machine-locatable (ADR-94 amendment + a check leg) |
| `[#465]` | fleet-audit writer integrity, all four legs — leg 4 retired an inert check |

| filed | what |
|---|---|
| `[#481]` | organ-id vs organ-measured disagreement (residue of `[#472]`'s repoint) |
| `[#482]` | boundary glob-engine REPAIR (true-glob) — ruled, not executed |
| `[#483]` | `preflight_contract` enforcement question — adoption-first, ungated |
| `[#484]` | ADR-106 system-Python divergence — named deferral, ~1 window |
| `[#485]` | shared LF-enforcing write helper — the mechanism replacing a gotcha |

| governance | what |
|---|---|
| ADR-82 | RATIFIED + the v5.3 → v6.0.1 catch-up in the same act |
| ADR-88 / ADR-89 | headers flipped to ADR-94 **Pattern B**, one pass — `[#242]`'s named instances |
| ADR-104 | amended — the declaration anchor (`[#472]`) |
| intake #22 §F.1 | the §F **flow rule** got its durable home, with its first application attached |
| `PLAYBOOK` §11 | library-first adoption order codified |

| surface work | what |
|---|---|
| `[#383]` | caches wave EXECUTED — **1 of 6 surfaces**; row stays OPEN |

**Flow (§F, first application): closed 3 / filed 5 → RED.** Recorded, not reconciled. Paying it
is the next window's opening obligation.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**The window's one finding, stated as a design fact rather than a war story:** across 12 review
runs the wrapper's severity tally read `0/0/0/0` **every single time**, over 1 CRITICAL and 21
HIGH in the bodies. Not a bad run — a mechanism that reports a verdict about something it is not
measuring, which is the same class as every defect the window closed. `[#480]` owns the gap and
is the **highest-value open item**; its evidence is now 12-for-12 and the row carries a pointer,
not the evidence.

**The layered ADR-85 design took its first live save — note it, because it is the reason to keep
the asymmetry.** The amendment deliberately made the pre-push organ's discharge **range-level**
and the audit backstop **per-entry**. Within two days that gap fired for real: a merge introduced
`b18bf29f` that no JOURNAL entry named; the pre-push gate passed the range, and the **backstop
caught it after the fact** — exactly the design's stated purpose (make a `--no-verify`-shaped hole
visible later). It then caught its own author a second time the same day. Nothing to fix; the
asymmetry is the feature. Do not "simplify" the two organs into one predicate.

**Open decisions the next session should resume, not rediscover:**

- **`[#480]` wrapper tally** — mechanism, not vigilance. The evidence is complete; what is unruled
  is whether a code-impact merge without a review artifact is *refused* or merely *surfaced*.
- **`[#483]` gate wiring** — adoption-first was deliberate. Two honest limits, both needed for the
  ruling. (i) A citation on the *wrong* line still passes, so the tool would not have caught the
  error that motivated it. (ii) **New, found running it on this bundle — its first production
  artifact:** the `backlog-id` check reads every `[#id]` as an assertion that the row is OPEN, and
  cannot tell that from a *historical* citation. This bundle drew 10 such FAILs and **all 10 were
  correct usage** — ids this window closed, cited in a table headed *closed*, plus `[#436]` cited
  as provenance (*"`BACKLOG.md` is GENERATED since `[#436]`"*). Zero were real staleness. So a
  handoff bundle — which is mostly historical narration — would go RED under a naive gate. Rule
  (b) "a gate on `docs/audits/` artifacts" with that in view, or the gate's first act is to red
  the seal of the window that built it.
- **`[#482]` glob engine** — REPAIR (true-glob) is ruled; the unbuilt half is the **governed-set
  pin**, without which a later tuple addition changes meaning silently under the new engine.
- **`[#481]` rename scope** — the id names a Stop-hook script while probing a pre-push one.
- **`[#485]` LF write helper** — the mechanism that lets a prose gotcha *retire* rather than fire
  again; it recurred this window against an entry that already existed, unread.
- **`[#383]`** — five surfaces remain, per SURFACE and named, never numbered. **Clause (c) of the
  caches wave is non-delegable and awaits the operator's read of the wave record §5.3**, where the
  coverage (3 of 9 repos, the six unwalked named) is tabled.
- **`[#447]`** already owns the self-referential-gate family surfaced above; the anchor recursion
  is a filed instance, not a new discovery.

**Settled — do not re-open without new evidence:** the ADR-85 model (obligation = integration onto
`main`; hard organ at pre-push; Stop advisory in full; backstop in `ALL_CHECKS`; the floor read
from the ADR). §F is a **flow** rule with seal-SHA boundaries, never a count target.
Retire-not-delete everywhere. One contract = one deliverable.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
