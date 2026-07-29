# Intake #18 ratification dossier — per-amendment input for the 2026-07-30 session ([#435])

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-29 · **Slug:** intake18-ratification-dossier
- **Serves:** the intake #18 ratification session (planned 2026-07-30, stewarded by **[#435]**) — one row per
  amendment of `docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md` (intake #18, PROPOSED).
- **Arc:** NIGHT BATCH 2026-07-28→29, cloud session, branch `claude/night-2026-07-28-prep-5my46t`.

> **INPUT, NOT AUTHORITY.** Recommendations below are the architect lane's; every ADOPT/DEFER/REJECT is the
> operator's per-amendment ruling to make ([#435] Done-when). **Cloud-session caveat:** produced WITHOUT the
> operator's user-level gates and without the Codex lane — every live check below is UNVERIFIED-UNTIL-LOCAL and
> must be re-verified at ruling time. Live-state anchors read at `f65065b` (branch base == main 2026-07-28).
> **Naming note (recorded, not silent):** filename ordered verbatim by the batch prompt; the batch spans into
> 2026-07-29, which is the session date the dossier serves.

**Evidence shorthand:** intake = `docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md` · audit =
`docs/audits/2026-07-27-verification-handoff-process-audit.md` (BW-*/RM-*/W-* IDs live there) · "this window" =
the 2026-07-28 shipped run (JOURNAL (k)–(n): [#437] core, [#439] flip, [#444] release, P9 closures, P6 prep;
plus rows [#440]–[#443] filed).

---

## Pack-level live findings (read these before the per-amendment rows)

1. **RM-7's premise was already stale inside the audit.** `scripts/audit.py` `_select_active_bundle`
   (landed in the `f3ead30` merge, **2026-07-23** — four days before the audit base `feb95e18`) selects the
   gate's bundle by **git add-date** with an ambiguous-FAIL on ≥2 fresh bundles, and its own docstring cites the
   07-20 arc5 incident as "the defect this replaces" (`scripts/audit.py:1592-1596`). The audit's RM-7 ("covers
   only the lexically-latest bundle") was probe-sourced from the historical 07-20 JOURNAL entry and not re-checked
   against the 07-23 fix. A11's first new guard must be re-scoped accordingly (see A11).
2. **[#441] condition (2) vs A5 — two mechanisms for one collision.** [#441] (`BACKLOG.md:134`) names
   "pre-allocated JOURNAL letters" as a condition-(2) contract example; A5 rules the opposite (lanes never
   allocate; letters assigned at integration). The corpus must not ratify both. See A5.
3. **The window strengthens, not weakens, the pack's frame.** The 2026-07-28 run was serial fat-prompts on
   primary (letters (k)…(n), zero collisions) — [#441]'s prove-then-codify evidence. That demotes the
   *frequency* of the parallel-lane classes (BW-c/BW-d) without touching their mechanism-when-parallel need:
   worktrees stay sanctioned behind the four-condition test, so the coordination amendments still have a live
   surface on every ALL-YES day.
4. **Intake #19 §B is in play for the same session** and rides on specific amendments (register at the end):
   §B(b)'s one-round-trip boot redesigns the exact probe-ferry loop that A7 and A4-item-3 would add legs to —
   sequence the §B(b) direction ruling BEFORE adopting those two probe legs, or the loop gets rebuilt twice.

---

## Per-amendment rows

### A1 — Truncation-visible artifacts (end-sentinel + section count)
- **Claims:** BW-a — chat-paste transport corrupted several pastes in one window; browser cannot detect a
  partial paste (audit §2 BW-a; class ancestry LESSONS:344, 2026-05-09).
- **Live check:** NOT shipped, not obsoleted. `scripts/assemble_paste.py` has no END sentinel (grep
  `END OF PASTE|sentinel` → zero hits); the boot ack is unchanged at `protocols/HANDOFF_BOOT.md:24` (no
  section count). Nothing in this window touches the surface.
- **Recommendation: ADOPT.** Oldest still-alive failure class in the longitudinal record (11 weeks, §5.3);
  S-cost; generalizes a mechanism v5 already ratified once (the §4 ack line).
- **Minimal cut-to-v6:** assembler END line + ack-line `({n} sections received.)` only; defer the PLAYBOOK Ch4
  report-direction sibling if trimming.

### A2 — Transport-medium contract (M+ artifacts travel as files)
- **Claims:** BW-a — the file-upload rule lives only in a consumed transient; violated the same window it was
  written (audit §2 BW-a).
- **Live check:** NOT shipped. HANDOFF_PROCESS §13 has no transport paragraph (grep `upload` → only the
  supplement-relay senses); ESSENTIALS carries only the outbound Scale-M+ rule (`protocols/ESSENTIALS.md:51`).
- **Recommendation: ADOPT.** XS text mirroring an existing rule; the terra H1 carve-out (supplement Q/A relay
  stays chat) is already folded into the intake text.
- **Minimal cut-to-v6:** the §13 paragraph alone; ESSENTIALS one-liner + assembler warn-string can follow.

### A3 — Branch-grammar reconciliation (`worktree-` / `epic/` sanctioned)
- **Claims:** BW-b/RM-6-adjacent — canon self-contradiction: PLAYBOOK Ch8's verified `worktree-<name>` vs
  CLAUDE.md §4 "these four only"; every worktree session boots into a grammar it violates.
- **Live check:** NOT shipped (CLAUDE.md §4 region unchanged — "these four only"). The window RAISES urgency
  twice over: (a) the [#441] codification (drafted this batch, DRAFT) writes worktree-launch doctrine into
  PLAYBOOK §8 — a third canon surface citing branch shapes the grammar forbids; (b) **the amendment's two-shape
  enum is already incomplete**: this batch's own branch `claude/night-2026-07-28-prep-5my46t` is a third
  machine-produced lane prefix (`claude/…`, Anthropic cloud sessions), witnessed live, covered by neither
  `worktree-` nor `epic/`.
- **Recommendation: ADOPT, with the enum widened** to cover machine-produced cloud-lane branches (`claude/…`)
  or re-worded as "machine-produced lane prefixes are sanctioned as produced by their sanctioned tool" — else
  the contradiction is re-created the first cloud night-batch after ratification. The `~/.claude/rules/`
  core-invariants #5 edit stays a separate explicit operator ruling (global infra, as the intake itself flags).
- **Minimal cut-to-v6:** the §4 region + template-extract lockstep edit; the global-infra edit deferred to its
  ruling.

### A4 — Destination contract + multi-agent mandate checklist
- **Claims:** BW-b (brief-side validation) · BW-d (declare-the-lane share) · BW-g (mandate standard).
- **Live check:** NOT shipped — PLAYBOOK §2 carries no fan-out checklist (grep `Multi-agent` → nothing);
  `templates/handoff/v5/PROBES.md.tmpl` + `scripts/gen_handoff.py` have no `Destination` row (grep → nothing).
  Window interaction: [#441]'s four-condition test IS an ex-ante lane-launch declaration in spirit — the two
  texts land adjacently in PLAYBOOK and must cite each other, not duplicate (the §8 draft produced this batch
  cites the destination contract as A4's).
- **Recommendation: ADOPT items 1–2** (s7 §4 checklist adoption + §13 destination paragraph — text-only, the
  checklist already exists drafted); **DEFER item 3** (the `Destination` boot-header row + P3 comparison leg)
  until the intake #19 §B(b) one-round-trip-boot direction is ruled — it adds a ferry leg to the exact loop
  §B(b) restructures (same surface, one build).
- **Minimal cut-to-v6:** items 1–2 verbatim; item 3 rides the §B(b) design.

### A5 — JOURNAL lane-letter allocation
- **Claims:** BW-c — two lanes both wrote "(b)"; landed duplicates (f)×2/(g)×2 already in the file.
- **Live check:** NOT shipped; **pressure reduced but not removed by [#441]** — the serial-default window
  produced zero collisions ((k)–(n) sequential), and worktrees remain sanctioned behind the four-condition test.
  **CONFLICT (pack-level finding 2):** [#441] condition (2) cites "pre-allocated JOURNAL letters" as the
  pre-resolving contract; A5 rules letters are assigned at integration and never by lanes. Both cannot be canon.
- **Recommendation: ADOPT the A5 convention** (assign-at-integration is the allocation that cannot collide by
  construction; pre-allocation still fails on the second unplanned lane) **and amend [#441]'s condition-(2)
  example list in the same ruling** to cite the A5 convention as the JOURNAL contract. DEFER the
  `normalize-dated-headers` hook leg (S, later — as the intake itself stages it).
- **Minimal cut-to-v6:** the PLAYBOOK §8 convention line only, worded into the [#441] codification's
  parallel-exception path so the corpus carries one statement.

### A6 — SUPPLEMENT question 7: ratified-in-chat register
- **Claims:** BW-e — chat-born terms have no provenance path (K1–K5, S3d precedents).
- **Live check:** NOT shipped (`templates/handoff/v5/SUPPLEMENT.md.tmpl` — no question 7; spec still says
  "fixed 6-question" at `protocols/HANDOFF_PROCESS.md:385`). **The window added a fresh witness:** intake #19
  itself is a chat-born design input that had to be hand-relayed into the repo as a SEED — exactly the BW-e
  class this question mechanizes at the boundary.
- **Recommendation: ADOPT.** XS; deliberately browser-side per ADR-87; rides the built fill→fold pipeline
  (W2 held under load — the filled-supplement precedent).
- **Minimal cut-to-v6:** the template question + the §13 "6→7" schema line, nothing else.

### A7 — Standing-topic reconciliation probe (P0 class)
- **Claims:** BW-f — the reconcile-first rule failed three consecutive windows as paste-prose.
- **Live check:** NOT shipped (§13(c) opening sequence still `role → vision → …`,
  `protocols/HANDOFF_PROCESS.md:314`; no P0 in generator/template). Two window interactions: (a) **intake #19
  §B(b) collides head-on** — P0 adds three probe legs to the operator-ferried loop §B(b) exists to collapse to
  one paste; (b) P0a binds to `BACKLOG.md` `[E#]` preambles — post-flip ([#439]) BACKLOG.md is GENERATED; the
  preambles still render there (manifest-sourced), so the binding survives, but the probe text should name the
  generated file knowingly (quote-from-generated-surface, source of truth `tasks/manifest.json`).
- **Recommendation: DEFER to the §B(b) design** — adopt the P0 *content* (standing-topic legs, honest-narrowed
  per terra H3) as rows inside the one-evidence-block emission §B(b) directs, not as three more ferry turns.
  DEFER here is not the intake's "keep the failed prose" option: the §13(c) opening-sequence extension
  (`role → vision → standing topics → backlog`) is XS text and can ADOPT now.
- **Minimal cut-to-v6:** the §13(c) sequence line now; P0 legs land with the §B(b) build.

### A8 — BINDING-line fold inventory (promotion debt surfaced)
- **Claims:** BW-h — rulings stranded in consumed transients; the Pyrefly near-reversal.
- **Live check:** NOT shipped (no promotion/BINDING scan in `scripts/assemble_paste.py` — grep → zero hits).
  **Window strengthens the case:** [#433] (the structural owner A8 defers to) STAYED OPEN at the P9 sweep with
  two NOT-MET verdicts (JOURNAL 07-28 (m)) — the "cheap interim, deletable when [#433] lands" argument now has
  a longer interim to cover.
- **Recommendation: ADOPT** (S; advisory-never-blocks; fires at the exact beat the transient is consumed).
- **Minimal cut-to-v6:** the assembler grep + stdout block; the §10 one-sentence search-soundness rule.

### A9 — PLAN.md, the D3 four-state artifact (spec text)
- **Claims:** BW-g + RM-2 — the ruled D3 lifecycle has no committed spec home; the runbook overstates PLAN.md.
- **Live check:** NOT shipped (no four-state text in HANDOFF_PROCESS — grep `DRAFT → REVIEWED` → nothing);
  [#301] still `DEFER — peg: #298` (`BACKLOG.md` [S2]); `docs/handoffs/README.md` untouched this window
  (its reconciliation stays its owner's next freshness window, as the intake routes it).
- **Recommendation: ADOPT.** XS text landing an already-made operator ruling (intake #17 D3); builds stay #301.
- **Minimal cut-to-v6:** the §13 paragraph verbatim.

### A10 — Spec-currency batch (four independent XS items)
- **Claims:** RM-1 (§15 LESSONS order wrong) · RM-3 (§4 "~3-line core" false) · RM-4 (§5 lacks a boundedness
  condition) · s4-row-1 (§14a missing RULING-W + ADR-101 cross-refs).
- **Live check:** ALL FOUR still stale, none obsoleted: `HANDOFF_PROCESS.md:590` still "append-only
  (oldest-first)" (live LESSONS.md is newest-first per its own header + ADR-29); `:71` still "a ~3-line core"
  against a 230-line HANDOFF_BOOT; §5 has no bounded-deterministic condition (grep → nothing); §14a names
  neither RULING-W nor ADR-101 (grep → nothing).
- **Recommendation: ADOPT all four** — each an independently ratifiable line, as the intake stages them.
  Item 3 (bounded-deterministic) is the one with teeth: it is the RM-4/S3d law that already killed P10 and
  narrowed A7 — putting it in §5 makes the next mis-shaped probe rejectable at design time.
- **Minimal cut-to-v6:** items 1+3 if trimming (the factual error + the design law); 2+4 next window.

### A11 — Probe/generator tooling debts (three adoptions + two new guards)
- **Claims:** RM-6/RM-7/RM-8 + [#421]/[#422] absorptions.
- **Live check — mixed, one leg stale:**
  - *Same-day gate coverage (RM-7 guard):* **premise stale** — see pack-level finding 1. Live behavior is
    add-date selection + ambiguous-FAIL (`audit.py:1575-1676`), not lexical. The residual true gap is
    narrower: the gate still verifies exactly ONE bundle; a second bundle touched in the same diff (both
    committed) escapes. Re-scope before ruling.
  - *Committed-bundle overwrite refusal (RM-8 guard):* NOT shipped — `scripts/gen_handoff.py:436`
    `bundle_dir.mkdir(parents=True, exist_ok=True)`, no tracked-file refusal, no auto-suffix.
  - *[#421] second tokenizer variant (backticked `#id` as anchor):* still unfiled — the live [#421] row text
    covers the leading-dot defect only.
  - *[#422] detector-as-validator-rung:* **already absorbed** — the live [#422] row's own Done-when specifies
    exactly this (`a --check-shaped leg over the bundle, wired where the fold runs`); the amendment adds no
    content beyond the row.
  - *`verify_handoff_probes.main()` params:* NOT shipped — `main()` still calls bare `verify(bundle)`
    (`scripts/verify_handoff_probes.py:444`) while `verify()` has `repo_root`/`cross_repo` (`:409`).
- **Recommendation:** ADOPT the overwrite refusal + the `main()` params + the [#421] absorption (S each);
  **RE-SCOPE then adopt** the gate-coverage guard as "every candidate bundle in the staged diff", crediting the
  shipped add-date selector; **REJECT-as-already-owned** the [#422] leg (the row carries it — ruling it again
  here creates two owners for one build).
- **Minimal cut-to-v6:** overwrite refusal + `main()` params; the rest ride their rows.

---

## Intake #19 §B rider register (which amendments §B rides on)

- **§B(a) clean-handoff contract** (write the existing ADR-85/ship-gate guarantee into the boot contract):
  rides on **A10 item 2** (the §4 honest-boot rewrite is the natural landing for the incoming-seat guarantee)
  and touches the same HANDOFF_BOOT surface as **A1**'s ack-line change — one edit pass, not two.
- **§B(b) one-round-trip boot** (one CC-side command → one evidence block → one paste): rides on **A7**
  (P0 legs must land inside the block, not as ferry turns), **A4 item 3** (the P3 destination comparison is a
  leg of the same block), and **A11's `main()` params** (the CC-side command that batch-runs the gate is this
  CLI grown up). Sequencing recommendation for the session: rule §B(b)'s direction FIRST, then rule A7/A4-item-3
  as its content.

## Label note (v5.8 vs v6)

The pack is additive → v5.8 by precedent, as the intake's §13 says. If the session also rules the §B(b)
one-round-trip boot direction (a workflow reshape v5 never claimed), the v6 label earns its scope honestly.
Operator's call; the content does not force it either way.
