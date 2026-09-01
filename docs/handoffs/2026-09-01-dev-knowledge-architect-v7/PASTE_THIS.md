=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-09-01-dev-knowledge-architect-v7` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-09-01-dev-knowledge-architect-v7 · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Rule on what batch F deliberately left open. Eight lanes merged and **zero rows closed** — five of them held open because terra found the defect defeats the row's own purpose, not because the work is unfinished. Decide which of those five G should fix, and rule on the substrate question the `[#632]` proof lane reopened (L1–L4 and L6 GREEN, L5 RED). Queue and provenance: `BACKLOG.md`, and `docs/audits/2026-09-02-technical-batch-f-close-packet.md` §3.<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->`none (primary tree)`<!-- FILL-IN:dest-worktree END --> · branch `main` · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->planning and rulings only — no build. If a fix is ruled in, it becomes a batch-G lane contract, not an edit from this seat<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->the open items are DECISIONS, not tasks — which rows to fix, whether an L5 RED made of pre-existing suite failures may gate a substrate default, and whether `routing` moves from OPERATOR to REPO. ADR-87 item 5: judgment scope, so architect<!-- FILL-IN:dest-mode-basis END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/v7-bundle`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

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

ROLE PIN — HANDOFF_BOOT.md @ handoff-process v7.0.0
sha256: 3b6d5691294e149844e16a2965d27ff49d2e95e3a69d138f6f77a33ecdef5858
If your project instructions do not carry this contract at this version+sha, say so before answering.

---

=== RESIDUAL.md ===

# Residual — 2026-09-01-dev-knowledge-architect-v7 — the part the repo does not already encode

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

**Window** — the diff since `docs/handoffs/2026-08-31-dev-knowledge-architect/` was added.

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
**The one judgment: the five OPEN rows are a DECISION, not a defect.** Batch F merged eight
lanes and closed **zero** rows. That is deliberate. Terra's pre-merge pass refused something in
all but one lane, and in five cases the defect defeats the row's own stated purpose — a
predicate that is never invoked, a waiver that fails open, a freshness gate pointing at a file
whose absence makes it silently skip. Those rows were left OPEN rather than closed on "tests
pass, merged". Read every one of them as *chosen*, and re-open the choice only with the packet
in hand: `docs/audits/2026-09-02-technical-batch-f-close-packet.md` §3.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
```
[#611]  HANDOFF_PROCESS v6.3.0 -> v7.0.0, cut as ONE coupled release act; /boot-session +
        boot_frontier.py + the FUNNEL HEALTH digest + spec sec17. ROW OPEN -- its Done-when
        also requires a measured paste from a real cut, which is THIS bundle.
[#632]  the codespace long-run proof RAN and REPORTED. Two Z-G3 W4 blockers measured CLOSED
        (uv IS present; the clone IS fresh); a third fixed at dispatch. Verdict RED at L5.
[#621][#626][#276][#629][#630][#627]  all merged, all OPEN, each with a named defect and a
        named fix direction -- see the close packet sec3. This is G's most concrete inventory.
[#614]  batch F CLOSED. dashboard home ruled to docs/dashboard/; the article brief disposed.
```
Detail lives in JOURNAL `(ai)` `(aj)` `(ak)` and the close packet — not restated here.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**1. The substrate decision is now evidence-bound, and the evidence is split.** The operator's
ruling was: Codespaces becomes the DEFAULT execution substrate *on green*. The proof lane's own
verdict is **RED at L5**, so it stays non-default — but L1–L4 and L6 are GREEN and two of the
three Z-G3 W4 blockers are now measured false. The open question is no longer *does it work*;
it is **whether an L5 RED made of pre-existing suite failures should gate a substrate decision
at all** — and terra removed the lane's argument that those failures are container-independent.
That is the first thing to rule on.

**2. The auth mechanism in the container is not what the runbook says it is.** `[#632]` L2:
`CLAUDE_CODE_OAUTH_TOKEN` is UNSET, the dispatched agent authenticates over some other live
channel, and a **nested** `claude -p` reproduces the "Not logged in" trap verbatim. Any design
that assumes a script can shell out to `claude` mid-lane is building on that trap.

**3. The lane/copy split is a doctrine gap, not six coincidences.** Five of eight lanes fixed a
root copy and missed the copy that executes. Nothing in the contract template asks "which copy
actually runs?" — that is a cheap, high-yield addition to the freeze gate.

**4. The integrator's own fan-out has no budget.** The 6/12 concurrency ruling governs LANES.
It held. What broke was the SEAT: three concurrent terra reviews produced two hard failures
(codex OOM twice; a fork-exhaustion that killed a push). Nobody has costed the integrator's
parallelism, and G should.

**5. HISTORY DELTA and EQUILIBRIUM MAP** — the operator's batch-G seed, this window. A first
hand-derived cut of both is committed at
`docs/audits/2026-09-01-technical-v7-history-delta-equilibrium-map.md`; the seed itself is the
close packet sec8. They are hand-derived ON PURPOSE — G builds the generator, and this cut exists
so G is specifying against a worked example rather than a description.
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
> **Branch note.** This bundle was generated on branch `docs/v7-bundle`. This line names only *which*
> branch is checked out so CC knows which live value to compare — **re-derive HEAD / tree / branch /
> ahead-behind live (P3); do not trust this line.**
>
> > **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.
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
| P0c | Does **this bundle's own Purpose** NAME at least one authority present in the P0a/P0b enumeration? **No match = FAIL**, route to the escalation ladder. (Whether the Purpose genuinely *serves* that authority is an architect judgment, deliberately outside the mechanical check — amendment A2.) | this bundle's `docs/handoffs/2026-09-01-dev-knowledge-architect-v7/HANDOFF_BOOT.md` Purpose ∩ the live P0a/P0b output | the Purpose is hand-authored per bundle and the authorities are live, so the name-match is computable only after P0a and P0b have both been run | `sed -n '/FILL-IN:purpose/,+1p' docs/handoffs/2026-09-01-dev-knowledge-architect-v7/HANDOFF_BOOT.md` → check it names an authority the P0a/P0b output enumerates; no match = FAIL |

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
| P1a | Quote, **substring-exact**, the **opening sentence** of `README.md` `## Vision` — *what .dev-knowledge is*. (ADR-114, Accepted 2026-08-29: `README.md` supersedes `VISION.md` as the hub's canonical purpose document. In a CHILD repo, whose canonical purpose document is still `VISION.md`, re-bind the path — cross-repo probes are re-bound against target surfaces regardless.) | `README.md` `## Vision` | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' README.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *where this work sits*. | `ARCHITECTURE.md` `## Purpose [CORE]` | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read live
by CC, substring-matched. **Then, before design, the operator-context beat fires (§13d):** the browser
asks the operator for **off-repo** context.
The operator has **filled** the supplement, so its ANSWERS are in the paste and the beat **NARROWS** to *"anything changed since the supplement was written?"*.

## Teeth probes (state fidelity — same contract; **answers deliberately withheld, §5**)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the final (last) one? | `ALL_CHECKS` in `scripts/audit.py` | the count + last name drift every time a check lands; a summary rounds/omits both | `python scripts/audit.py checks` (set `PYTHONUTF8=1` on a bare PowerShell console — see the cp1252 note) |
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, how many commits is `main` **ahead of / behind** `origin/main` — and does that live branch **match the `Destination` row's branch field** in this bundle's boot header? A mismatch is a **FAIL**: the lane is not where the handoff sent it. | live git ∩ the **Destination** row of `docs/handoffs/2026-09-01-dev-knowledge-architect-v7/HANDOFF_BOOT.md` | the summary holds the generation-time state; this handoff's own commit + the later `/ship` merge move HEAD and push `main` ahead until pushed. The `Destination` branch is declared **ex-ante** at generation while the live branch is read at check-time, so whether they agree is computable only now | `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` then `git rev-list --left-right --count origin/main...main` (the last is REQUIRED: `git status -sb` reports the CHECKED-OUT branch's upstream, not `main` vs `origin/main`, and prints no divergence at all when the branch has no upstream), then compare the live branch against the **Destination** row of `docs/handoffs/2026-09-01-dev-knowledge-architect-v7/HANDOFF_BOOT.md` — mismatch = FAIL |
| P4 | Which backlog `#id`(s) does `validate_git_backlog` flag **right now**, and what is the **full short-sha** (as the validator prints it) of the closing merge for each? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time; the sha is high-entropy, documented nowhere in the bundle | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — the doc-claim integer, the live-collected integer, and **do they match**? The claim lives in `ecosystem/doc-counts.md`, **not** `ARCHITECTURE.md` (decoupled by #222). | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer appears in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) |
| P7 | Does `audit.py ship-gate` come back **GREEN or RED** right now, **how many WARNs are dispositioned**, and **is there a `[stale]` disposition**? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | **THIS is the §1 headline** — the GREEN/RED verdict, the dispositioned-WARN count, and any `[stale]` line are computed at answer-time over live git ∩ `main`; a new direct-on-`main` commit re-REDs it; the values are absent from the bundle | `python scripts/audit.py ship-gate` (read the final GREEN/RED verdict + the disposition count + any `[stale]` line) — re-derive; do **not** trust the residual's prose |
| P8 | How many files does a **v5 architect bundle** carry, does it include a **per-bundle `README.md`**, is `SUPPLEMENT.md` present, **is its ANSWERS region empty or filled**, and where does the stable operator boilerplate live instead? | `docs/handoffs/2026-09-01-dev-knowledge-architect-v7/` listing ∩ `HANDOFF_PROCESS.md` §13 | a summary may "remember" a stale file count or the wrong supplement fill-state; the live bundle + spec are the only ground truth | `ls docs/handoffs/2026-09-01-dev-knowledge-architect-v7/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-09-01-dev-knowledge-architect-v7/SUPPLEMENT.md` (is there substantive text below the divider?) |
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

=== SUPPLEMENT.md ===

**1. Strategic intent — flip the operating mode from PUSH to PULL.** The seat stops carrying
state and starts answering `/boot-session`'s proposals: **repo proposes** (frontier, priorities,
next batch), **browser rules**, **operator decides**. The next session's way-of-working goal: run
the FIRST window that opens with `/boot-session`, executes `[#632]`'s n=2 acceptance, tags
v1.5.0, and performs the monorepo instantiation **attended** — proving the engine **deploys**,
not just governs itself.

**2. Tensions weighed.**
- **(a) speed vs trust — resolved for TRUST.** Terra pre-merge on every lane (~11 min/pass),
  after measuring **9 of 17 merges unreviewed**.
- **(b) visible shrinkage vs honest blockers — resolved for HONESTY.** VISION and ESSENTIALS
  waited for real re-reads and a fleet census rather than fake stamps.
- **(c) codespace-now vs window-close — resolved by doctrine option 4 + a PARKED precondition.**
  Local lanes ran; the codespace proved transport+gates but stays **NON-DEFAULT** until the n=2
  long-run acceptance.
- **(d) operator visibility vs token cost — resolved by ORGANS** (ledger, atlas, OPERATOR ASKS
  with `re-asked` RED) instead of chat answers.

**3. Considered + rejected — DO NOT RELITIGATE.**
- LangGraph-class orchestration for the hub — Layer-2 never executes; the moat is gates and
  contracts (A6 record).
- Fibonacci / golden-ratio graph aesthetics.
- TFP-class probabilistic inference over a ~1k corpus — R-A: sqlite answers in 1–4 ms.
- Harbor adoption NOW — DM-1 measured **risk relocation**, not effort reduction.
- Deleting `codex/` or `conformance.html` — live consumers measured.
- Cost caps on codespace before any spend.
- A root `dashboard/` folder — `docs/dashboard/` ruled, universal via the docs-tree carrier.
- `ecosystem/dashboard` — hub-only, non-scalable.
- A `SKIP=`-based v7 bump — atomic-at-integration ruled instead.

**4. Open questions.**
- `[#632]` acceptance **n=2** (M-sonnet + S + fuse test) — the hang's root cause is still only
  **bounded, not named**.
- `[#628]` ESSENTIALS dissolution scope — 10 consumers, rides with v1.5.0.
- ROOT-R1 `config/` verdict — FILL vs DISSOLVE into `pyproject`; census dispatched, **unruled**.
- intake #66 ratification — operator's.
- the scoring model for `/boot-session` — the BOOT-R1 artifact landed, the model is **unpinned**.
- `[#617]` distiller Tier-L design — eval-loop precondition met, build **unscheduled**.
- the equilibrium-map + history-delta bundle sections — batch-G seed.

**5. Decomposition rationale.** Batches are **file-disjoint frozen lanes with ONE serial
integrator** (Monitor-Object) because every defect class measured —
*five-lanes-consistent-alone*, *root-copy-vs-executing-copy*, *amendment-cannot-subtract* — is
**only catchable at integration**. **Do NOT redo:** the seven-predicate validator, the manifest
`closed_by:` exemption, terra pre-merge, R-MODELS routing (sonnet workers), the four-option
substrate doctrine, optimum-6 / ceiling-12. **The next seat inherits a working machine; its job
is throughput and deployment, not re-architecture.**

**6. Off-repo intent — changed this window.**
- Priority order **hardened**: **monorepo deployment FIRST**, ai-council second, win-tooling
  receives migration **last** though it remains consumer #1.
- **Token economics matter**: enterprise/free quotas before Anthropic quota — **measured, not
  capped**.
- The **master's thesis is the AUTONOMY arc's North Star** — adversarial debate as decision
  mechanism, flip-conditions on every ADR.
- The operator wants **pull-mode urgently** — handoffs shrink to `/boot-session` + residual.
- **Codespace-as-default is a standing operator expectation**, gated only by the n=2 proof.

**7. Ratified-in-chat register — NOT yet in the repo.**
```
term                                   definition                                durable home
OPERATOR ASKS re-asked>=2 => RED       a twice-asked ask with no visible-fix      landed in #66 --
                                       and no named blocker renders RED           VERIFY the digest
                                                                                  renders it
boot-* prefix-first command naming     commands sort by boot-* prefix             census candidate;
                                                                                  commands+skills
                                                                                  census row
TRACE before VIEW                      the trailer/signal lands BEFORE any        recorded in #66
                                       panel renders it
equilibrium map + history delta        two GENERATED /boot-session sections       batch-G seed --
                                                                                  NEEDS A ROW ID
integration=LOCAL always /             the four-option substrate doctrine,        VERIFY the dispatch
read-only=CLOUD /                      one line per axis                          chapter carries all
execution=CODESPACE-on-green /                                                    four VERBATIM
local-execution=explicit-request
```
Everything else ratified this window is, to the operator's knowledge, already in tree with ids.

---

=== END OF PASTE — 5 sections · 32206 bytes ===
