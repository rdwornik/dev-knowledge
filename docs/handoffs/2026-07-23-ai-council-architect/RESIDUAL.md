# Residual — 2026-07-23-ai-council-architect — the part the repo does not already encode

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

Produced by the live read-only drift-checks **the target actually has** — the four `ai-council`
validators (P7) + `validate_backlog` (P9) — plus hand intersection where the hub organ has no target
equivalent (P4, P11). **Re-derive each at read-time — the teeth are in `PROBES.md`
(P4/P6/P7/P9/P11), not in trusting these lines.** This bundle states **no** validator verdict,
count, drifted `#id`, or sha — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**Cross-repo re-frame:** `ai-council` carries **no automated drift-check organ** — no `audit.py`
ship-gate, no `validate_doc_claims`, no `validate_git_backlog`, no disposition register. The drift
surface is therefore: the four read-only validators (**P7**, several of which pass *silently* — the
exit code is the signal), `validate_backlog` (**P9**), and hand intersection (**P4**). The organ that
would mechanize doc-vs-reality checking is specified but not built (§4 item 2).

**STANDING + DELIBERATE (the headline):** `ARCHITECTURE.md`'s **Layer-edges allowed set is a
map-derived understatement** against `cli.py`'s real import surface — proven by the window's last
merge (rule-14 leg-b live validation; JOURNAL 2026-07-23 `chore/rule14-legs` entry), **report-only by
instruction**: no doc edit was applied, the follow-up edit awaits the operator's ruling. This is a
*known, held-open* drift, not an oversight — do not "fix" it before the ruling. **P11** re-derives
the live gap; §4 item 1 carries the decision context.

**STANDING (fenced, not yet resolved):** the dangling `refs #96` occurrences in the carried hub-id
tasks (`#110`/`#128`) — hazard contained by the BACKLOG **Id-reservations note** (ids reserved until
the renumber arc lands; **P12** re-derives the fence). And a cosmetic residue flagged in the JOURNAL:
the ARCHITECTURE Modules-table header still claims the `src/ai_council/` root while its config row
correctly points at repo-root `config/`.

**RESOLVED THIS WINDOW — do not re-flag:** the panel-default "3-vs-5 authority conflict" was
**DISSOLVED by archaeology** (code, ADR-02, ARCHITECTURE, GUIDE mutually consistent; the batch
report carries a dated withdrawal AMENDMENT — re-raising it is the false positive checker rule 5 now
guards against); the `#96` id collision was repaired by renumber; the moratorium lift is now recorded
in the grooming log; the E4 exit-3 claim was verified against source.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Window = since the 2026-07-21 handoff. One line each; detail lives in `JOURNAL.md` (all entries
2026-07-22/23) + the merge messages. All ids/paths are **ai-council's**.

- `3bf3ca9` — **`council boost` input stage shipped** (Unit 2 P1, TDD-first, owner-**C** per the
  ADR-11 amendment; terra-reviewed; chain witnessed end-to-end incl. one operator-authorized billed
  run). Closed `#37`; `#36` struck superseded-by-boost with remainder `#88`.
- `0611314` — the **boost→decide chain made explicit** in VISION / ARCHITECTURE / ADR-11 (the
  amendment last window's supplement demanded).
- `c35bc3e` — `.vscode/` boundary decoration landed (hub `#352` spec, declared-interim).
- `eb82fd5` — **night batch** (`chore/pre-handoff-cleanup`): dead-patch healthcheck test fix,
  ARCHITECTURE/VISION/CLAUDE/GUIDE doc-currency reconciliation, batch report
  `docs/audits/2026-07-22-pre-handoff-cleanup.md` (15 proposals + checker spec).
- `95b9e4f` — **session-close absorb**: the 8 live-unfiled P1s filed (`#89`–`#95`, `#98`; stories
  `[S17]`/`[S18]`), checker story `#97` filed, xdist declared + honestly re-measured
  (recommendation: do **not** adopt `-n auto` in `check.ps1`), panel-default conflict dissolved.
- `fe42bc2` — **record fixes**: `#96`→`#98` renumber + reservations-rule extension, `#69` P2
  constraint verified + attached, `#4` re-scoped (moratorium lift recorded), `#99` filed
  (batch-§2 pointer), `scripts/council-ask.ps1` deleted.
- `fc71328` — **ARCHITECTURE repair pass** (8 architect edits: layer-edge set completed +
  `cli -> boost` named the one open case, invariants 2/3 marked target-vs-state, boost in Data
  Flow, ADR-13 restored to the roster, stale pending-`#2` clause resolved).
- `6c297dd` — **`#97` rule 14 de-vacuated** (leg b: map completeness vs source), live-validated the
  same hour — the validation that produced §1's headline drift-flag.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
Ordered: rulings that gate build arcs first, then arc-shaping, then record debt.

1. **The ARCHITECTURE allowed-edge-set ruling (the headline's decision).** The completed Layer-edges
   set was audited **map-vs-map**; leg-b's map-vs-source check then showed `cli.py`'s real import
   surface far exceeds it (P11 supplies the live number). The un-ruled fork: **(a)** legalize cli's
   real edge profile as-is (interface→interface/orchestration/core/foundation/output — which
   falsifies "utility-exemption modules: none" and largely dissolves the layer discipline's bite at
   the interface layer), vs **(b)** hold the doc as **target**, and let `#92`'s `cli.run()` refactor
   shrink the real surface toward it before the set is re-derived. The JOURNAL's lean: the ruling
   rides the `#69`/P2 arc, because `#92` is what actually changes cli's import surface. Whatever is
   ruled, the doc must say *which* of current-state vs target it records (the repair pass already
   established that vocabulary for invariants 2/3).
2. **`cli -> boost` open case** — deliberately **not silently legalized** by the repair pass. Two
   candidate resolutions recorded in ARCHITECTURE: reclassify `boost` to orchestration, or admit a
   *scoped* interface→core edge. Bound to the same `#69`/P2 wiring arc; rule it together with item 1.
3. **The `#69` parity fix carries a verified P2 constraint** — the divergent frontmatter-`models:`
   gating expression **is also** the expression that makes `full_panel` the effective 5-model
   default. Any fix must **decouple the models-gate from the panel-default resolution** and land a
   bare-invocation panel-default regression test *first*, else the fix silently flips the default.
   The T8 strict xfail (`tests/test_boost.py`) errors the suite the moment boost wiring lands —
   wiring and parity fix are one arc by construction.
4. **`[S18]`/`#97` checker build** — 14 rules, each traced to a drift that actually occurred, both
   rule-14 legs now non-vacuous. Open design questions: build it as one script or per-rule
   validators; which rules gate vs report; and whether it becomes the target-side organ that closes
   the "no automated doc-claim check" gap (§1). The night-batch spec (`2026-07-22` report §3) is the
   authoritative rule list.
5. **`#4`'s ADR-02 amendment — scope is FENCED.** (a) overlap policy + (b) stale stamp only; the
   panel-default question is **DISSOLVED and out of scope** — the amendment must not reopen it
   (checker rule 5's refinement is the guard: adjudicate *effective flag-resolution behaviour*,
   never raw config keys).
6. **The renumber arc** — `#110`→`#84`, `#128`→`#85`, resolving/dropping their `refs #96` **in the
   same edit** (audit A1's instruction). P12 re-derives the reservation fence; until it lands, three
   ids stay un-assignable.
7. **`#99` triage** — the batch report §2 proposal set is *pointed at* but individually un-triaged
   (deliberate). A triage session decides file/drop per proposal; the un-filed xdist flake finding
   (first witnessed non-xdist-safe test) attaches to that thread.
8. **`#73` review-runner convention** — the review-lane routing posture (which reviewer lane runs
   what; one lane withdrawn on cost) lives only in `~/.claude` + the JOURNAL, not as a repo record —
   the fresh-architect gap the session-close entry names. A ruling here would also absorb it.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to **`ai-council`'s**
`BACKLOG.md` (themes `[E1]`–`[E7]`; the grooming log carries this window's rulings), the live
in-progress branches (`git branch -v`, run in the **target**), and the drifted-closed intersection
**P4 computes by hand** (§1 — the target has no `validate_git_backlog`). Re-narrating item text
splits the truth and drifts — the pointer + the drift-flag is the whole task-state. The whole-open-set
grooming obligation at boot is **P10**.
