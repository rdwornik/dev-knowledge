# Residual — 2026-08-28-dev-knowledge-architect — the part the repo does not already encode

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

> **Standing vs NEW — generated, names only.** Three lists computed from `ecosystem/disposition-register.yaml` ∩ this window's own diff. **No verdict, count, stale-disposition line, sha or backlog id appears here** — those are P7/P4/P6/P9's live answers and the evidence block carries them. The frame covers the standing-WARN family only; an organ outside it is the FILL-IN's business, not silently filed as standing.

**Window** — the diff since `docs/handoffs/2026-08-25-dev-knowledge-architect/` was added.

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
Of the two NEW-and-undispositioned organs above, **`reconciled_versions` is a DECISION, not a
defect.** This window deliberately moved both halves of what that organ reads: `HANDOFF_PROCESS.md`
advanced to **v6.3.0** (role residency — the browser role file is now a three-line PIN rather than
inlined into the paste, `[#611]`) with its coupled `reconciled_with:` edge re-stamped in the *same*
act, and, separately, `templates/` placeholder files were **exempted from the check by ruling**
(`[#335]`, verified-then-closed after one live run refuted the row's own "the false positive may
already be gone" premise). Both are intended states. So a signature this organ raises **about the
template layer is a ruling being honoured**; a signature naming anything **outside** `templates/`
is a genuine defect and must be treated as one.

**`fleet_parity` is explicitly NOT dispositioned as a decision** — recorded here so its absence
from the sentence above is not read as an oversight. Ruling **X3** admitted a *fifth* MUST-uniform
parity surface (the ruff-decidable half of the Python standard) and deliberately did **not** build
it, and ruled out a hub-hardcoded checker for the three unrepresentable clauses because such a
checker lands `absent` on consumers by measurement. That organ's ground truth therefore moved while
its implementation did not. Read what it reports as **unwritten work**, not as accepted state — and
re-derive it, since this bundle asserts nothing about what it currently says.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Window = the diff since `docs/handoffs/2026-08-25-dev-knowledge-architect/` was added. Six arcs;
each line points, none recaps — `JOURNAL.md` carries the detail at the entry named.

- **Batch W2 — five lanes integrated serially.** Gate mechanisms and per-check tiering:
  `[#587]` `[#588]` (the per-commit anchor tax), `[#589]` `[#590]` (the `BACKLOG.md` view and the
  audits index stop being merge-resolvable), `[#591]` `[#592]` `[#595]` `[#596]`, `[#593]`
  (a codespace starts at current `origin/main`, not the image snapshot), `[#597]` `[#598]`.
  → `JOURNAL.md` 2026-08-27 (a)–(f).
- **ADR-115 ACCEPTED — `AGENTS.md` is the portable instruction layer.** Supersedes ADR-53
  Decision 2 and amends the ADR-101 Tier-1 file class **in one act**, exactly as the prior
  window's F3 said the act had to be shaped. Held first by ruling **W7**, then accepted.
  → `docs/decisions/ADR-115-*.md`; `JOURNAL.md` 2026-08-26 (b).
- **The 2026-08-26 endgame governance window** — register **section W**, rulings W1–W7
  (global provider env vars, documentation-splits-by-audience, the measured 45-day icebox
  parameter, the Codespaces-rung unavailability finding, `[#569]`'s closure, the `docs/archive/`
  KEEP verdict, the ADR-115 hold). → `JOURNAL.md` 2026-08-26 (b).
- **Root `prompts/` REVOKED** — the ADR-101 sanctioned top-level set **contracts for the first
  time**. → `JOURNAL.md` 2026-08-26 (c).
- **The night-harvest ledger, executed end to end** — register **section X**, rulings X1–X8, over
  four cloud reports; four companion intakes filed (**#57** I-DOC, **#58** I-KODEKS, **#59**
  I-ROTATE, **#60** I-NIGHT); `[#424]` **closed** (the inert `_DEPID_RE` — a prior-window F6 item),
  the 17 inferred `depends-on` edges adopted, the nine dead-pegged rows re-pegged, the 45-day
  icebox sweep executed, `[#607]` `[#608]` born. The arc's own negative headline: the kill
  algorithm, run faithfully, closed **zero**. → `JOURNAL.md` 2026-08-28 (a).
- **The K4 closure harvest** — eight rows closed, six re-cut, one held, three born (`[#609]`
  `[#610]` `[#611]`), with `HANDOFF_PROCESS` **v6.3.0** shipped as `[#611]`. Three verdicts did
  **not** survive their own evidence and were reported rather than executed as written.
  → `JOURNAL.md` 2026-08-28 (b).
- **`[#267]`'s mechanism RULED** — option (b): mechanism (iii) alone ratified, part (ii) **cut, not
  deferred**; register **section Y** generalises the **dead-peg rule** (a peg must name a carrier
  that exists). → `JOURNAL.md` 2026-08-28 (c).
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**The window's shape, stated once so it is not re-derived: the rulings landed AND were consumed.**
Sections U/W/X/Y are adjudicated, wave 1 executed, the night harvest was ledgered through the
funnel. What is left is not backlog — it is the set of things the window ruled *around* rather than
*on*. Five of them below. **G5 is the only one that blocks a wave-2 act rather than merely waiting
on one.** Start at `BACKLOG.md` and the register sections it points at; do not re-read the window.

**G1 — The funnel-vs-births rule is now settled in PRACTICE and still unwritten, and that is worse
than it was when it was merely open.** The prior window's F1 asked how a ruled ADOPT arc becomes a
row without bypassing ADR-111. The window answered it by *doing* it: `[#579]`–`[#586]` and
`[#607]`–`[#611]` were born straight from ruled packet rows, each carrying a `source:` clause
naming its packet row and register section, funded by a closure ledger (closures banked before
filing, PLAYBOOK D3/D5). But **section Y, landed 2026-08-28, restates the orthodox rule** for the
`[#267]` fleet-scale candidate — *"per ADR-111 the only path from here to a row is CANDIDATE →
intake (ADR-98) → ratification"* — and cites nothing about packet-born rows. So the corpus now
carries **two live paths and no statement of which applies when**. The working distinction is
almost certainly *"a ruled packet row is already past triage; a raw finding is not"* — but that
sentence exists **nowhere**, only as a pattern inferable from eleven commits. Write it as a
standing ruling, or the next seat re-derives it and may re-derive it differently. This is cheap and
it decays fast.

**G2 — ARC-G now has a direction (W2) and its first concrete act is a fleet-parity act, not an
editorial one.** W2 rules that `PLAYBOOK.md` and `ESSENTIALS.md` are human-facing functional
documentation and the machine layer is code plus generated surfaces, with D5 resolved on that split
— and states its own honest limit: **no ARC-G execution was taken by the session that landed it.**
The trap the prior window flagged is unchanged and has now acquired a forcing case. `CLAUDE.md` has
**eight of twelve sections as HUB-single-sourced Form-A regions** that must stay byte-identical to
`templates/claude-regions/*.md`, and its own line budget is near its ceiling (measure with
`validate_doc_rot.scan_file_budget`; v2.67 spent 2 lines on its own bullet). The forcing case:
§10's *"Narrating or managing AGENTS.md"* anti-pattern is, since ADR-115, **provably false
doctrine** — and it sits inside one of those hub regions, so correcting it requires a lockstep
template edit that no row authorises. `[#577]` owns the correction and is **open**. **Decide whether
ARC-G is licensed to move the region templates.** Until that is ruled, the hub ships an instruction
file that contradicts an Accepted ADR, and three consecutive CLAUDE.md revisions have each recorded
that they knowingly left it.

**G3 — The substrate mandate and the substrate measurement contradict each other, and the router
ADR is owed against the contradiction, not against either half.** Ruling **U(b)** mandates: batches
shrink to 4–6 lanes, **GitHub compute is the DEFAULT substrate**, provider-agnosticism ranks
alongside speed, lanes route by table, sequential-local is retired. Ruling **W4**, taken one day
later, measured that rung as **NOT available** on three independent fatal defects — `gh codespace
cp` receives literal single quotes; **`uv` is absent from the container**, so *no* hub gate can run
there under ADR-106; and the clone was silently stale, so the very merge declaring the Claude Code
install was not present. W4 concludes the wave-2 router ADR must not treat that substrate as a live
default. Standing behind both: the settled 2026-08-20 ruling to stay on **Codespaces free 4-core
and never buy overage**. And the routing table itself does not exist — the canonical one is
`~/.claude/ROUTING.md`, ruled **L0, outside this repo** (2026-08-22), so authoring it in-hub is
itself a boundary decision. **A default substrate that cannot execute a single gate is not a
default.** Either W4's three defects get owned rows and the mandate is conditional on them closing,
or the mandate is re-scoped. Nothing currently does either.

**G4 — Green-by-skip is now owned at two layers and the standing RULE is still not written.** The
prior window's F4 asked whether *"a check that cannot compute its ground truth must FAIL, never
skip"* becomes a standing rule with a sweep. Since then `[#583]` owns the **site** layer and
`[#596]` the **proof** layer (both open; `[#596]`'s mechanism shipped in batch W2), and section U
records the mechanism precisely — the `skipped` status is **not** caused by the cp1252 crash; it is
the GAP-1 cycle-break, where the standalone CLI passes `None` for the injected check count and only
`audit health` / `audit run` supply it. The two compound rather than cause one another, and the net
is that no surface fails when that number drifts. The cp1252 half still has three rows describing
it (`[#470]` one glyph, `[#486]` a different script and glyph, `[#484]` the environment divergence
underneath both). Rows exist; **the rule does not.** Ruling it once is what stops instance
number four being filed as a fourth row.

**G5 — The items the window itself recorded as owed, unruled, or ownerless.** These are not
discoveries; each is written down somewhere and none has a carrier:
- Section **X**'s own "still owed and explicitly unruled" list: which of the **30 unblocked P2s**
  below the ranking cut need a second disposition · `[#82]`'s hub-closability ruling · whether
  `[#548]`/`[#559]`'s multi-edge dependencies imply a **manifest-producer row nobody owns**.
- Section **Y**'s CANDIDATE — the fleet-scale discover-from-config half cut from `[#267]` — carries
  **no peg and no owner by design**, which is the point of the dead-peg rule; it is routed at the
  next intake pass, and this is that pass unless deferred deliberately.
- `[#267]`'s own unsettled tension, left standing by its ruling: the row calls itself a REFINEMENT
  and *"not a closure gate"* while the K4 table treated it as a decision row.
- `[#549]` — intake #13's plan-of-record still has **no carrier**; the SUPERSEDED-by-`[E9]` vs
  re-anchor fork has now been re-pegged across three windows and is `status: deferred`.
- `[#359]` — **phantom enforcement**: §14a claims a mechanism that does not exist, and the
  four-state ledger still has **no cell** for a rule that claims a mechanism it lacks. Open.
- The **doc-rot accretion corpus** — unbounded row-annotation debt that trimming cannot clear; the
  fix is a row-body archival mechanism and **nothing owns it** (figures at `JOURNAL.md`
  2026-08-28 (c); cite the surface, not this line).
- **ADR-114** stays **PARKED**. Reopening it is an operator act, not this seat's.

**Three cautions for whoever picks this up.** (1) `BACKLOG.md` is **generated** — edit `tasks/` and
regenerate (`gen_task_tree.py --emit-source`); a direct edit is the ADR-107 §7.2 failure and the
`check_task_tree_coherence` gate will catch it after you have wasted the act. (2) The filing-
backpressure hook demands a `kill-candidates:` line per added id regardless of which way G1 is
ruled, and the ids it names must be **open**. (3) This bundle's `SUPPLEMENT.md` is
**FILLED** — its ANSWERS are folded into the paste, so the §13(d) beat **NARROWS** to *"anything
changed since the supplement was written?"*. **Read the supplement before the G-list.** Its OPEN
QUESTION 1 — role residency — is **RESOLVED**: a Project is adopted, so **first boot verifies the
PIN against the project knowledge file** (version check mandatory) rather than settling residency.
The mechanism, its one-file constraint and the rejected alternative are stated once in the
supplement — read them there, not restated here. The supplement also carries a **CC
verification block** appended at fold time: of its three repo-verifiable claims, the
`automation/fleet-audit` one is **refuted and discharged**, and the other two stand.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
