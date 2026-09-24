# Residual — 2026-09-24-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.
>
> **Supplement fill-state:** stated once, in this bundle's `HANDOFF_BOOT.md` session header
> ([#611] — not duplicated here).

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

> **Standing vs NEW — generated, names only.** Three lists computed from `ecosystem/disposition-register.yaml` ∩ this window's own diff. **No verdict, count, stale-disposition line, sha or backlog id appears here** — those are P7/P4/P6/P9's live answers and the evidence block carries them. The frame covers the standing-WARN family only; an organ outside it is the FILL-IN's business, not silently filed as standing.

**Window** — the diff since `docs/handoffs/2026-09-19-dev-knowledge-architect/` was added.

**Dispositioned by the register.** The register already carries an entry for these organs, so a WARN from one is standing unless its evidence signature is new:
- `no_ff_merges`
- `journal_spine_anchor`
- `doc_rot`
- `undeclared_edges`
- `funnel_coverage`

**Dispositioned by absence from the window diff.** This window touched nothing these organs read, so a WARN from one is not this window's doing:
- _(none)_

**NEW-and-undispositioned.** No register entry, and this window DID touch what they read — so a WARN from one of these is this window's, and the note below says which is a decision rather than a defect:
- `reconciled_versions` (reads the registered specs and the docs declaring a `reconciled_with:` edge)
- `fleet_parity` (reads the parity-surface manifest and the surfaces it names)

<!-- FILL-IN:driftflags START (hand-authored — ONE judgment only: name which NEW flag above is a DECISION rather than a defect. The standing-vs-new attribution is GENERATED directly above; do not restate it. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**`fleet_parity` is a DECISION, not a defect — the same decision the previous window carried.**
Its `settings-deny-and-point` row (`ecosystem/parity-surfaces.yaml`) is still deliberately
hub-INVERSE: the PreToolUse guard stays unwired under BUILD MODE rule 8, so the hub is expected to
lack it and a consumer that still ships it is the divergence. A flag from that row is the mechanism
working. What is still NOT decided: the parity schema holds no row-level expiry a checker reads, so
the inversion cannot lapse with BUILD MODE by itself. Every other parity flag is a defect.

**`reconciled_versions` is a defect if it flags.** Nothing this window did makes a spec/dependent
version mismatch intentional; the `check-against-spec` skill is the repair path.

**Not a drift-flag, but read before acting on the ship-gate:** STANDING_RULINGS AL-A O-8 makes a
WARN left undispositioned for 30 days a hard-fail. The standing families above are therefore now on
a clock rather than standing indefinitely; which of them is closest to its date is a live P7 read,
not a claim this bundle makes.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Terse map — detail is in `JOURNAL.md` 2026-09-20..24 and in the window digest
`docs/audits/2026-09-24-technical-digest-window-2026-09-19-24.md` (the Friday-vs-today table).

- **The loop, connected** (waves 3, 4, 4B, 5A — rows `[#929]`-`[#1014]` filed across them): spine
  moments with receipts; one launcher (`dispatch.py launch`); lane-end reporting from a real Stop
  event; one handback organ; plan-lint on contracts before freeze; one ship-gate comparator; CI
  verdicts read as data and paired against local; diff-scoped test selection; memory-gated heavy runs.
- **ADR-120** (Accepted) — the spine is the whole 16-stage loop. **ADR-121** (Proposed; direction
  ratified by AL-B1) — operational state as a single-writer event log. **ADR-122** (Proposed;
  **DEFERRED** by AL-B13 pending the GitHub Issues trial).
- **Handoff repair** — the paste is shed and gated at 20,000 B (this bundle is its first live cut).
- **Copilot Enterprise** admitted for implement in the provider registry, on in-repo evidence.
- `[#960]` retired on operator-approved Tier-1 closure.
- **Precut landing** — today's rulings and digests landed verbatim under `docs/audits/2026-09-24-*`,
  plus `protocols/STANDING_RULINGS.md` **AL** (O-6..O-12 delegation, B1..B15 decisions).

**Six QUESTION files dispositioned at this cut.** The preflight's `question_disposition` row refused
the first cut attempt: six lane/integrator QUESTION files had been answered by existing rulings
(`ANSWER-integrator-wave4b-handback-organ`, `ANSWER-lane-l1-spine-moments-2026-09-20`,
DECLARE-WAVE3-CONNECT R-W3-1/5/6/8/9, DECLARE-WAVE4A R-W4-3) but carried no `disposition:` line, and
two ANSWER files carry a suffix the row's exact-name lookup cannot see. Each got one flush-left
`disposition:` citing its answer; nothing was ruled at the cut. One item was left unruled on purpose:
the two empty husk directories in QUESTION-lane-l2 were the operator's call.

**Carried decisions — `carried-by: OPEN`, named here because the residual is their only carrier
(P11 leg 2).** Each states an OPEN carrier and has no repo home yet; the next session lands each one
or re-declares the carriage:

- `to-cc/AMEND-ACCEPTANCE-TEST-CARRIER-2026-09-17.md`
- `to-cc/AMEND-BATCH-night-2026-09-17.md`
- `to-cc/AMEND-DISPATCH-UNBLOCK-2026-09-17.md`
- `to-cc/AMEND-HANDOFF-BOOT-INTEGRATOR-SECTION-2026-09-20.md`
- `to-cc/AMEND-MODEL-ROUTING-AND-SCOPE-2026-09-17.md`
- `to-cc/AMEND-NIGHT-ORDER-CONSOLIDATED-2026-09-17.md`
- `to-cc/AMEND-NIGHT-SALVAGE-2026-09-17.md`
- `to-cc/AMEND-ORGAN-USE-2026-09-17.md`
- `to-cc/BATCH-ADR-BACKLOG-2026-09-24.md`
- `to-cc/BATCH-ADR-STATE-STORE-2026-09-23.md`
- `to-cc/BATCH-ENV-GLOBALS-2026-09-23.md`
- `to-cc/BATCH-RESEARCH-HANDOFF-2026-09-24.md`
- `to-cc/BATCH-TRIAL-GH-ISSUES-2026-09-24.md`
- `to-cc/BATCH-WAVE5A-2026-09-23.md`
- `to-cc/BATCH-dispatch-order-2026-09-17.md`
- `to-cc/BATCH-night-2026-09-17.md`
- `to-cc/DECLARE-ACCEPTANCE-TEST-CARRIER-2026-09-17.md`
- `to-cc/DECLARE-BATCH-AC-CLOSE-2026-09-18.md`
- `to-cc/DECLARE-BATCH-AC-CLOSE-AMENDED-2026-09-18.md`
- `to-cc/DECLARE-BATCH-AC-NOT-CLOSED-2026-09-18.md`
- `to-cc/DECLARE-BUILD-MODE-2026-09-18.md`
- `to-cc/DECLARE-CENSUS-VERDICTS-2026-09-18.md`
- `to-cc/DECLARE-HARNESS-IS-PROCESS-2026-09-08.md`
- `to-cc/DECLARE-HARNESS-PROVENANCE-2026-09-08.md`
- `to-cc/DECLARE-LANE-HANDBACK-CONTRACT-2026-09-18.md`
- `to-cc/DECLARE-SEAT-KNOWLEDGE-2026-09-24.md`
- `to-cc/DECLARE-STATE-STORE-LEARNING-2026-09-23.md`

**Owed rows not filed.** The precut lane could not file its owed rows because the BACKLOG view is at
its byte ceiling; they are listed in full in `to-browser/SESSION-lane-precut-landing.md` and wait on
ADR-122 step 0.

**Carried WARN debt.** This window hands off with the ship-gate's open WARNs unresolved rather than
silenced; P7 re-derives them live and §1 attributes them by organ. Nothing was dispositioned to make
a gate pass.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
`SUPPLEMENT.md` was generated empty (cold cut), so there is no folded architect "why" this time;
the §13(d) beat fires full. What follows is the executor-side residue, each item with its owning
surface.

**1. ADR-122 step 0 comes before everything that files a row.** The generated BACKLOG view is at its
byte ceiling, so `--emit-source` refuses any new row and filing is blocked fleet-wide. AL-B11 rules
the principle ("truth has no ceiling; the view has a budget") and points at
`docs/audits/2026-09-24-technical-declare-adr-122-rulings.md` for the mechanism. It is a small
decision with a large blast radius: until it lands, every lane that should file a row writes it into
a session file instead, which is the drift ADR-122 exists to end.

**2. Where a task lives is decided by a live trial, not by the ADR.** AL-B13 deferred ADR-122
because its rejection of GitHub Issues was argued on paper (option O2 never run). The trial order is
`to-cc/BATCH-TRIAL-GH-ISSUES-2026-09-24.md`: the same 20 rows through `gh` only, issue forms as the
schema, `Closes #N`, one issue to the Copilot coding agent, the compatibility renderer on the 13
readers, and a re-weighted matrix (offline weighted 0; "no custom code" and "Copilot pipeline"
added). The known trap is `#N` auto-linking once `[#id]` numbers migrate. AL-O-12 is the
tie-breaker: an existing product CC can drive from the console wins over a custom organ unless the
recorded reason says otherwise.

**3. The merge path as code on ADR-121's event log.** The digest's honest list puts this second
after CI-as-gate. ADR-121's direction is ratified (AL-B1, with pilot thresholds and the files
fallback); debate D1 (AL-B2) says a seat acts only on pushed state. The open question is sequencing:
required checks go on only after the baseline is honest and the commit gate is diff-scoped (AL-B8),
so the event-log merge path and the honest CI baseline land in that order or together, never with
the gate first.

**4. Delegation now has clocks — watch the first time each one fires.** AL-A O-6 (auto-close on a
green runnable check), O-7 (30-day unconsumed removal sweep) and O-8 (30-day undispositioned WARN →
hard-fail) turn standing debt into dated debt. None has fired yet. The first O-8 hard-fail and the
first O-7 sweep will be the real test of whether "explicit and owned" is enforced or only stated.

**5. The carried OPEN decision files are still the real queue**, and the queue grew (now including
today's batch orders). A decision file can declare an OPEN carrier indefinitely and nothing ages
it; O-8's clock does not reach them. Landing them is work, not filing.

**6. A preflight blind spot, surfaced by this cut.** `question_disposition` finds an answer only by
exact name (`ANSWER-<seat>.md`); answers written with a suffix or a date are invisible to it. Here
that cost one refused cut. The mirror case is the risk: a mis-named answer file could be believed
answered by a reader and flagged unanswered by the row. The `answers:` header those files already
carry is the natural key. This needs a row; one cannot be filed until step 0.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
