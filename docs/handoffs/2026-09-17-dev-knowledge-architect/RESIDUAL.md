# Residual — 2026-09-17-dev-knowledge-architect — the part the repo does not already encode

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

**Window** — the diff since `docs/handoffs/2026-09-10-dev-knowledge-architect/` was added.

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
**`fleet_parity` is the DECISION, not the defect.** This window deliberately re-wired the surfaces
that organ reads. The 2026-09-17 emergency `disableAllHooks` had removed three MUST hook surfaces as
collateral; the operator's correction restored `arm_hooks`, `session_end_backpressure` and
`deny_and_point` on lane ab-808's measurement (they were never among the nine hooks over the bypass
bar) and disabled the nine individually with rate, owner and re-enable condition. The surfaces are
present because the hooks RUN, witnessed in three headless sessions this window, not because a
declaration says so. Two things are deliberately still divergent and owned: the plugin `Stop` hook
`propose_closures.py` could not be disabled per-repo without reddening `settings-plugin-tier1`, and
the ADR-77 transcript guard stays off under `[#863]`. **`reconciled_versions` is NOT claimed as a
decision:** this window edited `CLAUDE.md`, which declares a `reconciled_with:` edge, but bumped no
registered spec — so anything from that organ is a defect to investigate, and P7 is what says whether
it fired. No verdict, count or `[stale]` value is stated here.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Eight batches since the 2026-09-10 bundle; `JOURNAL.md` 2026-09-11 → 09-17 carries the detail, row
state is `BACKLOG.md`. This map does not repeat either.

- **W** (09-11) `[#683]` `[#638]` `[#278]` `[#688]` closed; HARNESS-IS-PROCESS → intake 92 (DRAFT);
  `/override` removed; prompts guard fail-closed.
- **X, waves 1–4** (09-11→14) window rulings → `STANDING_RULINGS.md` §AH; conductor E built + proven;
  `[#664]` delivery spine; `[#727]` fail-closed; delete list executed; **ADR-119** (the window's only ADR).
- **Y** (09-14) `ESSENTIALS.md` deleted (`[#755]`; `[#628]` stays open by ruling); receipts; cost in money.
- **Z** (09-15) 51 failing tests frozen (`[#763]` `[#764]`); Codespace substrate; quality register;
  non-Claude execution; intakes 95–100.
- **AA** (09-15→16) prepend-order gate; integrator model split; enforced routing (`[#885]`, renumbered
  from `[#793]` by a reserved id); intake 101.
- **AB** (09-16→17) id allocator; closure census closing 25 rows; suite baseline re-frozen at 87 with
  four deliberate RED witnesses; intake 103.
- **The emergency arc** (09-17) all hooks disabled (`[#863]` `[#865]`); commit gate stripped to
  data-loss protection, 31 hooks → conductor job `commit-gate` (`[#883]`); then **this window's
  correction** (§4).
- **Filed at this cut** `[#886]` `[#887]` `[#888]`.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
### The successor's acceptance test exists and no row carries it

Intake **103** §0.6: *"one lane runs end to end, dispatch to merged, in under one hour, with nothing
wedged and no human decision in the middle"* — and until then *"no new organ is built."* Intake 103
says in its own text that **NO ROW carries this test**: rule it onto a row or call the sentence
decoration. Intake 103 is SEED, awaiting §G triage — ~25 findings with no row, each owed one ADR-111
state.

### The hooks: restored on a measurement, and three threads travel

The 2026-09-17 `disableAllHooks` was indiscriminate; ab-808's per-hook bypass rates showed the three
parity-REQUIRED hooks were never among the nine over the bar. Restored and **witnessed running** in
three headless sessions: `arm_hooks`, `session_end_backpressure`, `deny_and_point`. The nine are off
individually with rate, owner and re-enable condition (`.claude/settings.json` register key).

1. **`propose_closures.py` still runs** (plugin `Stop`, 15%) — loaded in place from
   `plugins/tier1-lifecycle/hooks/hooks.json`, so every lever is machine-wide/fleet-wide or reds
   parity `settings-plugin-tier1` (MUST). **Operator decision owed.**
2. **`deny_and_point` returned without meeting its own 2026-09-15 condition** (a bounded time that
   fails open with a LOUD in-band record). The harness `timeout` bounds it silently;
   `bounded_hook.py` stays unwired by the 2026-09-17 ruling. Restored on the 2% measurement, and the
   settings key says the condition is unmet rather than implying otherwise.
3. **`[#863]` owns the cause** — hook processes created SUSPENDED, never resumed. Unfixed; the ADR-77
   transcript guard stays off until it is.

### `[#888]` — the record type this repo does not have

Measured at this cut: `fleet_parity._eval_row` emits `MUST-absent` and returns **before** reading any
declaration, and ADR-102 refuses `waivable: true` on a MUST row. So the one machine-readable
time-boxed record here (`.methodology.yaml`) cannot carry a required component an emergency switched
off. That leaves lying to the gate (demote the tier → permanent by accident) or stopping work. A
third way existed today only because ab-808's measurement existed; the next emergency may have none.
`[#886]` is the parity-side half and `[#888]`'s declared kill-candidate.

### The six contradicting rule pairs are RULED, UNBUILT

`to-cc/ANSWER-contradicting-rules-2026-09-16.md` — **P1=C P2=A P3=B P4=C P5=A P6=B**, reason per pair.
Nothing is implemented: P4 (drop the `allow` from the gitignored `settings.local.json`, add a narrow
ask rule for merges onto `main`) and P5 (wire ADR-110's refusal into the dispatch verb, before a lane
session starts) name acts no commit has made.

### Carried decisions and questions (named here because P11 requires it)

- **`to-cc/DECLARE-HARNESS-IS-PROCESS-2026-09-08.md`** — `carried-by: OPEN`, carrier "successor's
  intake". Landed as intake 92, still DRAFT and unratified.
- **`to-cc/DECLARE-HARNESS-PROVENANCE-2026-09-08.md`** — `carried-by: OPEN`; its carrier is a
  candidate ADR that does not exist: *"nothing guarantees anything without a run record a second
  organ consumes."* The same class `[#888]` and `[#883]` reach from other sides.
- **`to-browser/QUESTION-github-private-now.md`** — CARRIED, dispositioned OUT OF SCOPE (the
  operator's GitHub account, not this repo), owned by OPEN **`[#887]`**: the preflight judges the
  whole shared transport instead of this repo's own files. Seven CV/GitHub decision files of that
  class were trashed at this cut; this question is the class's live witness.

### The WARNs handed over, by family (no verdict/count here — P7's live answer)

`consumer_at_landing` (largest; dispositioned by the R-citer ruling) · `funnel_coverage` (audits with
no disposition — ADR-111 triage, intake 103 §G) · `proof_layer` · `undeclared_edges` · `doc_rot`
(accretion, incl. the BACKLOG row-length ceiling) · `doc_code_edge` · `no_ff_merges` ·
`review_artifact_coverage` (advisory, `[#480]` P3) · `substrate_declaration` · `journal_spine_anchor`
· `generated_artifact_freshness` · `canonical_freshness` · `adr_status_grammar` · `fleet_parity`
(§1). Two dispositions read `[stale]` against the register and are owed review/remove (ADR-75).

### Still red, deliberately

Frozen baseline: 87 members at `c5108329`, `-n 4`, with **four `[#664]` witnesses kept OUT** so they
fail visibly — *"not a regression, do not 'fix' them"* (JOURNAL 09-17 (q)); a fifth would be real.
**0 of the old 51 departed** — nothing in that set was fixed this window. `[#763]` stays open though
the re-freeze landed. The BACKLOG view is over its `[#589]` byte bar and these three rows grow it.

### Operator's own open words

CI enforcement ON or documented report-only (ruleset still `enforcement: disabled`) · the Actions
credential, held on security grounds · whether dispatch moves to Python · the BACKLOG headroom route ·
*"what a tagged manifest means"* (intake 100, DRAFT) · RETIRE candidates `[#303]` `[#369]` `[#383]`
`[#604]` · the five DEAD `PLAYBOOK` sections, disposition owed (`[#665]` `[#666]`).
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
