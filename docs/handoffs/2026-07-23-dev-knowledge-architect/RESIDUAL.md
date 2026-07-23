# Residual — 2026-07-23-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**Standing (deliberate, not new):** the `VISION.md` `canonical_freshness` backstop WARN — left visible as honest, tracked by `[#368]` (VISION untouched pending its own re-review arc; deliberately NOT dispositioned). `witnessed` at generation; re-derive via P7. **Dispositioned:** `ecosystem/disposition-register.yaml` carries the two historical no-ff spine entries (`warn-no-ff-*-journal-wrap`, `warn-no-ff-*-transcript-archive`) — pre-existing main-spine hits, ruled benign with refs in the register. **New-this-window:** none known at generation (`validate_git_backlog` and `validate_backlog` were clean when this bundle was cut — `witnessed`); the live set at read-time is P4/P7/P9's answer, not this paragraph. **Known-latent:** `gen_handoff.py` leaks architect-mode SUPPLEMENT framing into *execution*-mode renders (`[#404]`, filed this window) — this architect bundle is unaffected (architect is the generator's home path); any execution/developer render before `[#404]` lands needs hand-correction.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Window = since the 2026-07-21 architect handoff (detail: `JOURNAL.md` 2026-07-21→23 entries; ids: `BACKLOG.md`).

- `[E9]` North Star ingested (intake #16; `[#381]`–`[#388]`) — **the brake is live: no new fleet machinery before `[#381]` rules**
- `[#386]` delivery loop codified into PLAYBOOK §21 (+ `[#389]`/`[#390]` filed)
- `[#384]` CLOSED — L5a fleet analytics reporter (`fleet_analytics.py`, read-only)
- Night batch: `docs/decisions/transcripts/` DELETED (operator ruling; ADR-77 guard kept armed) + archival audit; `[#400]` filed; integration filings `[#391]`–`[#396]`
- Hygiene lane: logs/ naming convention `[#395]` + ARCHITECTURE currency `[#321]`; filings `[#397]`–`[#399]`
- `docs/runbooks/` collapsed into `protocols/` + ADR-101 d.i reversal amendment
- ADR-43 routed-mirror clause RETIRED by amendment (re-scope); `[#401]` filed (ai-council routing armed at deleted hub zone)
- `[#398]` CLOSED — intake status-enum deployed, id:14 triple dissolved; `[#402]` filed (naming clause)
- ARCHITECTURE currency lane: carrier 4→5 (5 sites), Ch4 channel/carrier vocabulary split, child roster +win-tooling, Governing-ADRs refresh; `[#403]` filed (doc_claims coverage gap); ADR-92 stale-side finding REPORTED, not edited
- `[#404]` filed — gen_handoff execution-mode SUPPLEMENT leak, found cutting (and hand-correcting) the now-superseded same-day execution bundle; this architect bundle supersedes it
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
The open rulings/design questions this planning session should resume, in rough priority order (`recall` — re-check each against live `BACKLOG.md` at boot):

1. **`[#381]` polyrepo ruling** — the E9 brake gates ALL new fleet machinery; nothing in `[#382]`/`[#383]`/`[#385]` may start before it rules. THE standing architect decision.
2. **ADR-92 amendment call** — reality is five carrier modules; ADR-92's body still says "four hard-coded carriers". The divergence is annotated legible in `ARCHITECTURE.md` (Governing-ADRs row); the amendment itself is owed.
3. **`[#403]` derivations ruling** — which machine-derivable doc_claims checks to adopt (carrier count / child roster / Governing-ADR completeness); candidates named in the ticket, none chosen.
4. **`[#402]` naming-clause ruling** + **`[#401]` ai-council routing disarm** — both small, both blocked on an operator call.
5. **Conformance remotes + nightly-triage findings** — 2 remote conformance branches left for triage (2026-07-23 consolidation JOURNAL entry).
6. **`[#404]` generator mode-blindness** — execution/developer renders leak architect SUPPLEMENT framing + a dead P8 binding; fix = mode-aware framing tokens, mode-conditional P8 row, per-mode render test. Small, self-contained; a candidate first execution task once rulings land.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
