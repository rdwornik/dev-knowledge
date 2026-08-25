# Residual — 2026-08-25-dev-knowledge-architect — the part the repo does not already encode

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
**Every flag in this window is STANDING, and the standing set is dispositioned in two different
places — which is itself the thing to notice.** Do not read a verdict here; P7 re-derives it.

- **Dispositioned-by-register.** `ecosystem/disposition-register.yaml` is the only surface that
  suppresses an awareness-organ WARN, one entry per WARN, keyed on the *specific benign
  signature* rather than a bare id (precision-over-recall, by its own header contract). Its
  ADR-75 decoration rule means an entry matching nothing live is SURFACED rather than silently
  rotting — so some of what P7 prints is the register reporting on itself, not new drift. Read
  the register before treating any single line as an arc's cost.
- **Dispositioned-by-absence — the larger half, and the one that misleads.** The bulk of the
  standing set is *not* in the register at all: it is `doc_rot` row-length against `BACKLOG.md`,
  `undeclared_edges` against `ecosystem/`, and `adr_status_grammar` against untouched ADRs. These
  are baseline conditions of files the recent arcs never opened. The 2026-08-25 (b) JOURNAL entry
  established the discriminator that works: attribute a WARN by asking whether the arc's diff
  touched the file it fires against, not by counting.
- **NEW-this-window, and deliberately left un-dispositioned.** The `funnel_coverage` rows for the
  audit artifacts landed 2026-08-25 (b)/(c) are the expected, predicted cost of landing them. The
  landing contract's own stop-list **forbade** dispositioning them — the register-ruling packet
  owns that adjudication. So their presence is a contract being honoured, not a regression; wave 1
  is where they get ruled.
- **The flag that is not a flag — read `protocols/STANDING_RULINGS.md` section U's defect note
  first.** `validate_doc_claims`' `audit_check_count` leg reports `skipped` and the run still
  prints `OK`. That is **green-by-skip**, not green: it is the GAP-1 cycle-break design (the
  standalone CLI injects `None`; only `audit health` / `audit run` supply the count), compounded
  by — but *not* caused by — a cp1252 `UnicodeEncodeError` in `cmd_checks`. Section U records the
  precise mechanism and assigns the fail-loud fix to wave 1. `audit.py health` is unaffected, so
  the pre-commit gate is intact. Treat any "no prose drift" line from that leg as unverified until
  the fix lands.
- **Re-derivation note.** Under the default Windows console the checks roster command in
  `ecosystem/doc-counts.md` does not run; `PYTHONUTF8=1` is the measured workaround. Set it before
  running P7/P9 or you will mistake a crash for a clean pass.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
**Window = the three 2026-08-25 sessions (a)/(b)/(c). Detail lives in `JOURNAL.md`; this is the
map only.** No `tasks/` row was born, closed or edited in any of the three — `window: 0 closed /
0 born / net 0` is a deliberate contract outcome, not an omission, and it is the single most
important fact for the next seat to carry.

- **(a) Evidence landed, no ruling taken** — two external research reports into `docs/audits/`
  byte-identical (sha256 verified both ends), plus a dated evidence note on the AGENTS.md
  admission intake. C01's measured criterion (">=2 admitted providers consume `AGENTS.md` and not
  `CLAUDE.md`") reads **MET** against the six admitted providers, counted strictly — the wider
  roster reads both files and was excluded rather than used to inflate it. DeepSeek stays
  **unmeasured**. The ADR-53-vs-R-1 precedence question the intake exists to force was left
  untouched on purpose.
- **(b) The five verification lanes integrated** — sentinel-first and serial, none skipped;
  index conflicts resolved by regeneration rather than hunk-picking; all five remote lanes torn
  down behind an ancestor proof taken before each delete. See the entry's addendum for the merge
  SHAs and the teardown proofs.
- **(c) The register-ruling packet landed** — five artifacts byte-identical, and
  `protocols/STANDING_RULINGS.md` gained **section U**, which POINTS at
  `docs/audits/2026-08-25-technical-register-ruling-packet.md` as the binding adjudication of all
  37 candidate rows (ten arcs A–J; the REJECTs with reasons; the CONTRA adjudications; four errors
  the architect owns as their own). **Section U is the pointer the next seat starts from.**
- **Governance surfaces touched:** `protocols/STANDING_RULINGS.md` (+section U), `docs/audits/`
  (+7 artifacts across the window, index regenerated each time), `docs/intake/` (evidence note
  only, status untouched). `BACKLOG.md`, `tasks/` and every registry yaml were **not opened**.
- **Still parked, and unchanged by this window:** `ADR-114` (root `README.md` recreation) is
  **PARKED** by operator ruling 2026-08-22 with its priced options retained as the input the
  ruling selected against. Do not reopen it as if it were merely Proposed.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**The window closed with a ruling landed and nothing built against it. Wave 1 is where that gap
closes, and the first four questions below are the ones that decide *how*, not *whether*.**
Start from `protocols/STANDING_RULINGS.md` section U, then the packet it points at.

**F1 — How do ten ruled ADOPT arcs become backlog rows without bypassing the ADR-111 funnel?**
This is the window's central unresolved tension, and it is a governance question, not a clerical
one. Section U deliberately births **zero** rows and defers all of them to wave 1, banking the 29
closures DISCHARGE-38 released. But ADR-111 states the only path to a row is **CANDIDATE → intake
(ADR-98) → ratification**, and CLAUDE.md §4 repeats it. A ruled ADOPT arc is arguably already
past triage — the packet *is* the adjudication — in which case birthing directly is legitimate and
the funnel is satisfied upstream. Or it is not, in which case ten arcs owe intakes first. **Nothing
in the corpus says which**, and getting it wrong in either direction is expensive: a bypass
launders ten decisions past the funnel; an over-application buries a completed adjudication under
ten redundant intakes. Rule this before filing anything. Note the filing-backpressure hook will
demand a `kill-candidates:` line per added id regardless of which way it goes.

**F2 — What does "documentation splits by audience" actually cost, and where does it stop?**
The operator's 2026-08-25 direction (section U) makes `PLAYBOOK.md` and `ESSENTIALS.md`
human-facing functional documentation, with code and generated surfaces as the machine layer, and
ARC-G (the doc diet) executes under it. The unresolved part is the **boundary**, because the hub's
own instruction files sit on both sides at once. `CLAUDE.md` is read by the agent every session
*and* by Rob; it closes at **195/200 lines** with headroom 5 by its own checker; and eight of its
twelve sections are HUB-single-sourced Form-A regions that must stay byte-identical to
`templates/claude-regions/*.md`. So a diet that touches those regions is a **fleet-parity act**,
not an editorial one. The v2.65 entry records this trap concretely: the M1 rule was contracted for
§10, could not land there, and shipped in §4 instead — **and still owes a lockstep §10 + template
act that no row currently owns.** Decide whether ARC-G is scoped to the human-facing pair only, or
whether it is licensed to move the region templates too.

**F3 — The AGENTS.md precedence ruling (#42) is now evidence-complete and still unruled.**
C01's measured criterion is MET (session (a)), so the blocking condition is discharged. The act the
criterion points toward is a **single** one: supersede ADR-53 D2 (single instruction file) *and*
amend the ADR-101 hermetization class in one commit — because `SANCTIONED_TIER1_FILES` is a closed
enum and an added root `AGENTS.md` is a pre-commit BLOCK until it is not. Two open sub-questions:
whether it is a real fork or a generated twin of `CLAUDE.md` (a hand-maintained second instruction
file is the exact drift class ADR-53 was written to kill), and what DeepSeek's **unmeasured**
consumption does to the criterion — the ruling packet predicted that gap and it is still open.
**This is also the natural test case for F1**, since it is a ruled arc that plainly needs an ADR
rather than a row.

**F4 — Green-by-skip is a failure class, not a bug, and only one instance is currently owed.**
Section U assigns the cp1252 fail-loud fix to wave 1. But the *pattern* is what deserves the
architect's attention: a gate whose ground truth is unavailable reports `skipped` and the run
still prints `OK`. That is the same shape as two defects this repo has already paid for — the
pre-push leg that printed "degraded — allowing push" and returned 0 (removed by the ADR-85
amendment §A6, now fails CLOSED), and the `block_commit_on_main` hole where a git failure
silently ALLOWS. **The question is whether "a check that cannot compute its ground truth must
FAIL, never skip" becomes a standing rule with a sweep**, or whether each instance keeps getting
fixed one at a time. A sweep is the higher-value act and nothing owns it.

**F5 — ARC-D substrate routing collides with a settled substrate ruling, and the collision is
undischarged.** Section U (b) mandates: batches shrink to 4–6 lanes, **GitHub compute is the
DEFAULT substrate**, provider-agnosticism is a ruled criterion alongside speed, lanes route by
table, sequential-local is retired with local reserved for operator-gated acts and
vendor-CLI-on-disk work. Standing against that: the 2026-08-20 ruling to stay on **Codespaces free
4-core and never buy overage**, which caps concurrency hard. A 4–6-lane default on a 4-core free
tier is either fine or a contradiction depending on lane weight, and nobody has measured it. The
routing table ARC-D calls for **does not exist yet**; note that the canonical routing table lives
at `~/.claude/ROUTING.md`, which is **L0 — outside this repo** (ruled 2026-08-22), so building it
in-hub is itself a boundary decision.

**F6 — Standing items that keep getting re-pegged rather than ruled.** Each is small, each is
blocking something, and each has now survived multiple windows on a deferral: **[#549]** — intake
#13's plan-of-record has no carrier; the SUPERSEDED-by-[E9] vs re-anchor fork was re-pegged to
[#572] and "waits for next window", which is now. **[#424]** — the `depends-on` gates are INERT
(`_DEPID_RE` requires a `#`; the [E9] chain is written bare), so the sequencing [E9]'s preamble
relies on is prose, not machinery. **[#359]** — phantom enforcement: §14a claims a mechanism that
does not exist, and the four-state ledger has **no cell** for a rule that claims a mechanism it
lacks. **ADR-114** stays PARKED — reopening it is an operator act, not this seat's.

**Two standing cautions for whoever picks this up.** (1) Row births are the *first* act of wave 1
and every prior contract in this window explicitly forbade them — if you find yourself editing
`BACKLOG.md` directly, stop: it is **generated** since the ADR-107 §7.2 flip, edit `tasks/` and
regenerate. (2) The unpushed-`main` ordering risk recorded in 2026-08-25 (b) resolves only at the
operator's push; until then the five torn-down lane branches exist on `origin` solely inside that
unpushed `main`.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
