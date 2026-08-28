=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-08-28-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-08-28-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Resume the architect seat on **[E2] Enforced governance** and **[E9] Fleet Desired-State System (North Star)** at the point the 2026-08-25 → 2026-08-28 window left them: the ruling packets have landed *and* been consumed, so what remains is not backlog execution but the questions the window ruled **around** rather than **on**. The residual §4 carries five, of which the substrate contradiction (U(b) makes GitHub compute the default; W4 measures that rung as unable to run a single hub gate) is the one that **blocks** a wave-2 act rather than merely waiting on one. Navigate from `BACKLOG.md` and the register sections U/W/X/Y it points at — do not re-derive the window.<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->none (primary tree)<!-- FILL-IN:dest-worktree END --> · branch `main` · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->governance surfaces — `tasks/` (then regenerate `BACKLOG.md`, never hand-edit it), `docs/intake/`, `docs/decisions/`, `protocols/STANDING_RULINGS.md`, `JOURNAL.md`; gate/script edits only under a named row<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->the next act **defines the way of working** rather than advancing a named row — five open design questions, two of which (G1 the funnel-vs-births rule, G3 the substrate router) need a ruling before anything can honestly be filed against them (ADR-87 item 5)<!-- FILL-IN:dest-mode-basis END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/handoff-2026-08-28`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

> **The `Destination` row is declared ex-ante — a lane inherits none of it from a prior prompt.**
> Only its **branch** field has a mechanical counterpart: `PROBES.md` **P3** compares it against
> live `git branch --show-current`, and a mismatch is a FAIL. Worktree, write-scope and MODE-basis
> stay **prose** and deliberately carry no probe leg — a leg with no mechanical counterpart cannot
> fail honestly, and one that cannot fail honestly discredits the whole block (R3).

> **Dispatching a lane from this bundle — the literal command is not here.** Every launch
> command lives in ONE place: **`protocols/PLAYBOOK.md` Ch8, "The dispatch table — the SOLE
> literal-command site"** — the Q1–Q4 substrate decision, the verb per substrate, its argument
> shape, its receipt and its cost guards. Ask CC to pull it and **copy** a row; a launch line
> composed rather than quoted is the defect class that cost ~30 consecutive seats their lane
> (`STANDING_RULINGS.md` section V; measurement
> `docs/audits/2026-08-25-technical-dispatch-surface-measured.md`).

> **Anti-bluff in effect.** The contract, what the withholding buys, and where generation-time
> hints go instead are stated **once** in this bundle's own `PROBES.md` header (spec:
> `HANDOFF_PROCESS.md` §5) — one hop inside the same paste, rather than a second copy free to
> disagree with the first.

> **Operator runbook is not copied here.** The stable who-each-file-is-for / run-loop / rationale lives
> **once** in the canonical per-repo runbook **`docs/handoffs/README.md`** — read it for the walkthrough.
> This file carries only the **session header** (above) + the **paste-pointer** (below). v5 bundles carry
> **no per-bundle README** (HANDOFF_PROCESS §13).

> **Dispatch prep is not copied here either.** A seat taking the architect role finds how a dispatch
> prompt is made, how model + effort are routed, how a batch runs, and how completion is managed at
> **`protocols/PLAYBOOK.md` Ch8 "Handoff prep for the next architect"** — itself an index of pointers,
> so this is one hop to the index and one more to each home. Standing rulings applied without asking:
> `protocols/STANDING_RULINGS.md`. Same pointer-not-copy rule as the runbook above.

---

=== ROLE PIN (protocols/HANDOFF_BOOT.md — RESIDENT, not inlined) ===

ROLE PIN — HANDOFF_BOOT.md @ handoff-process v6.3.0
sha256: ae661a7c070d0fabee0a186ba0069a2e40e6c4d47feb8c2ace8555add7c735ce
If your project instructions do not carry this contract at this version+sha, say so before answering.

---

=== RESIDUAL.md ===

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

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

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
ruled, and the ids it names must be **open**. (3) This bundle's `SUPPLEMENT.md` is **cold** — no
answers were folded — so the §13(d) operator-context beat fires **FULL**, not narrowed: ask for
off-repo context before designing.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.

---

=== PROBES.md ===

# Probe manifest — architect mode: orientation first, then teeth (HANDOFF_PROCESS §5 + §13c)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and **no
> answer**. The browser has no file access, so the answers reach it one way only: **CC** runs every
> command against **live state at check-time** via `/handoff-verify`, re-derives ground truth, and
> emits **one evidence block** carrying each row's PASS/FAIL and live evidence. The operator pastes
> that block once (HANDOFF_PROCESS §5 — the v6 one-round-trip boot). **Any FAIL blocks onboarding**,
> and a missing required row is not a pass. Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor (never a synthesized
> pass); git/tooling absent → reported *skipped* (degraded coverage visible), never counted as pass.
>
> **Anti-bluff (HANDOFF_PROCESS §5 — a probe that bakes its answer is bluffable, rejected).** This
> manifest **withholds every answer value** by construction: no counts, SHAs, dates, verdicts,
> group-memberships, or orienting lines are stated. That withholding IS the teeth. The pass criterion
> is **"answered from the live source at check-time,"** never "matches a remembered number." Generation
> hints (if any) live in the JOURNAL generation-entry, which the browser never sees — never here. The
> validator `scripts/verify_handoff_probes.py` FAILs any probe row that prints an `expected:` value.
>
> **Branch note.** This bundle was generated on branch `docs/handoff-2026-08-28`. This line names only *which*
> branch is checked out so CC knows which live value to compare — **re-derive HEAD / tree / branch /
> ahead-behind live (P3); do not trust this line.**
>
> > **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.
>
> **Windows note:** `audit.py checks` (P2) can crash mid-listing on a bare cp1252 PowerShell console
> (a non-ASCII glyph in a check docstring) — run with `PYTHONUTF8=1` (or `PYTHONIOENCODING=utf-8`); this
> is Python's stdout encoding, shell-independent, so git-bash does **not** avoid it. `ship-gate` (P7)
> can false-RED on `handoff_probes` under PowerShell — **verify in git-bash.**

## P0 — Standing-topic reconciliation (emitted **above** P1 — A7 / R2)

The **standing authorities** a session reconciles against before it plans: the live epic
themes and the live accepted intakes. This was a §13 prose rule and it failed three consecutive
windows — *a rule with no probe has no teeth* — so it is mechanized here. **Deterministic legs
only** (the RM-4 / S3d boundedness law): there is no open-ended adjudication leg, because
whole-set grooming is an **arc, not a probe** (JOURNAL 2026-07-26 (h)). P0c is narrowed to a
**name-match** for exactly that reason (amendment A2): "does the Purpose *serve* this authority"
is a judgment a probe cannot terminate on, and a leg that cannot fail honestly discredits the
block. Same contract as every row below: question + source-locator + command, **no answer**.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P0a | Quote, **substring-exact**, the theme-preamble line of each **active** `[E#]` epic theme in `BACKLOG.md` — **and** separately confirm the generated backlog is **CURRENT**, not stale. | `BACKLOG.md` `[E#]` theme headers + the preamble line under each | the preamble set drifts on any theme edit, and `BACKLOG.md` is GENERATED since [#436] — a probe that can pass on stale generated content is bluffable, so currency is asserted mechanically, not assumed | `grep -A1 '^## \[E' BACKLOG.md` → each quote substring-matches the live preamble (a paraphrase is a FAIL); **then** `python scripts/gen_task_tree.py --check` exits 0 — a non-zero exit is a FAIL (currency — R2's second assertion) |
| P0b | Enumerate, live, every doc under `docs/intake/` whose frontmatter carries `status: ACCEPTED`, and quote each one's **TITLE line** (its first level-1 `#`-heading). **Titles only.** | `docs/intake/*.md` frontmatter + first heading; area definition at `docs/intake/README.md` | the accepted set and its titles drift on any intake status change; neither the set nor any title appears in this bundle | `grep -l '^status: ACCEPTED' docs/intake/*.md` then read each hit's first heading line |
| P0c | Does **this bundle's own Purpose** NAME at least one authority present in the P0a/P0b enumeration? **No match = FAIL**, route to the escalation ladder. (Whether the Purpose genuinely *serves* that authority is an architect judgment, deliberately outside the mechanical check — amendment A2.) | this bundle's `docs/handoffs/2026-08-28-dev-knowledge-architect/HANDOFF_BOOT.md` Purpose ∩ the live P0a/P0b output | the Purpose is hand-authored per bundle and the authorities are live, so the name-match is computable only after P0a and P0b have both been run | `sed -n '/FILL-IN:purpose/,+1p' docs/handoffs/2026-08-28-dev-knowledge-architect/HANDOFF_BOOT.md` → check it names an authority the P0a/P0b output enumerates; no match = FAIL |

**Honest narrowing (terra H3).** P0b quotes **titles**, not wave/sequence detail: wave content is
unstructured prose today, so quoting it would overclaim determinism (the RM-4 law applied to this
row's own design). Wave-level teeth require the intake schema to first gain a required,
machine-locatable plan-of-record heading — an intake-schema change owned by `docs/intake/README.md`,
offered as an option, not assumed.

## P1 — Orientation (the architect's **first move**, before any mechanism — §13c)

A plain-language "what is this project" is **summary-bluffable** and so fails §5's own bar; a copy of
VISION into the handoff is barred (§2/§3). So orientation is a **forced exact-line read**: the line
enters the session **only** by CC reading the **live** primary source, and the quote must match as a
**substring** (never a paraphrase). The browser has no files, so CC reads live and substring-checks,
and the result arrives in the evidence block. The grep is a **tool** that confirms the frame — **the
backlog navigates** (§13c), not this read.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1a | Quote, **substring-exact**, the **opening sentence** of `VISION.md` `## Vision` — *what .dev-knowledge is*. | `VISION.md` `## Vision` | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *where this work sits*. | `ARCHITECTURE.md` `## Purpose [CORE]` | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read live
by CC, substring-matched. **Then, before design, the operator-context beat fires (§13d):** the browser
asks the operator for **off-repo** context.
This bundle's supplement is **generated EMPTY**, so the beat fires **FULL** — *"what off-repo context: intent, priorities, findings not in the repo, changed decisions?"* — not a narrowed "anything changed since?". (If the operator runs `supplement filled`, its ANSWERS fold in and the beat narrows.)

## Teeth probes (state fidelity — same contract; **answers deliberately withheld, §5**)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both | `python scripts/audit.py checks` (set `PYTHONUTF8=1` on a bare PowerShell console — see the cp1252 note) |
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, how many commits is `main` **ahead of / behind** `origin/main` — and does that live branch **match the `Destination` row's branch field** in this bundle's boot header? A mismatch is a **FAIL**: the lane is not where the handoff sent it. | live git ∩ the **Destination** row of `docs/handoffs/2026-08-28-dev-knowledge-architect/HANDOFF_BOOT.md` | the summary holds the generation-time state; this handoff's own commit + the later `/ship` merge move HEAD and push `main` ahead until pushed. The `Destination` branch is declared **ex-ante** at generation while the live branch is read at check-time, so whether they agree is computable only now | `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` then `git rev-list --left-right --count origin/main...main` (the last is REQUIRED: `git status -sb` reports the CHECKED-OUT branch's upstream, not `main` vs `origin/main`, and prints no divergence at all when the branch has no upstream), then compare the live branch against the **Destination** row of `docs/handoffs/2026-08-28-dev-knowledge-architect/HANDOFF_BOOT.md` — mismatch = FAIL |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? The claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline** — the GREEN/RED verdict, the dispositioned-WARN count, and any `[stale]` line are computed at answer-time over live git ∩ `main`; a new direct-on-`main` commit re-REDs it; the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-08-28-dev-knowledge-architect/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-08-28-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-08-28-dev-knowledge-architect/SUPPLEMENT.md` (is there substantive text below the divider?) |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **right now**, which `#id`(s) are in the **code-edge** group, and which `#id`s are in the **coherence** group? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | group membership is a live schema fact that drifts on any BACKLOG edit; it is absent from this bundle | `python scripts/validate_backlog.py` (the serialize-groups summary line) |

## Gate procedure (CC)

1. **Run the whole gate in one pass** (`/handoff-verify`), in table order: **P0 first, then P1**,
   then the remaining rows — every row against **live state now**. Table order IS the execution order. The
   architect cannot begin design until both orienting lines are read live and substring-matched.
   **The operator-context beat (§13d) fires after the block is in hand.**
2. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
3. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
4. Probes P0a–P9 are *designed to move* between generation and check-time — that is the point. **Answer
   values are deliberately absent (§5)**: the pass criterion is **"answered from the live source,"**
   never "matches a remembered number." P7 is the headline (GREEN/RED + dispositioned-WARN count +
   any `[stale]` line). P8 pins the bundle shape **and the live supplement fill-state**. First check
   which branch is live (P3), then re-derive every load-bearing fact from the live primary source.
5. **Every row is BOUNDED (§5 cond. 4).** A probe whose honest answer requires unbounded judgment
   over an open set is an **arc, not a probe**, and is rejected — `verify_handoff_probes.py` FAILs
   any row that quantifies over one. The former **P10** ("groom every OPEN item in `BACKLOG.md` at
   boot") was exactly that row: ratified-against at intake #18 as this condition's own origin, and
   shipped anyway in 35 bundles until it was removed 2026-08-26. Backlog grooming is real work; it
   is a task the successor takes on with a contract, not a gate it clears before it may begin.

---

=== END OF PASTE — 4 sections · 35528 bytes ===
