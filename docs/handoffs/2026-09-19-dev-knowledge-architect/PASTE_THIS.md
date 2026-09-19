=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-09-19-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-09-19-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Run the spine, read its first STOP, fix that one thing, and re-run — do not open by planning a wave from a list. The standing way-of-working question this window leaves live is how a temporary measure expires by itself when the schema it lives in cannot hold an expiry; one shape now works in code and one surface refuses it. Task-state is `BACKLOG.md` (the carried `carried-by: OPEN` decisions are named in `RESIDUAL.md` §2 and are work, not filing). **AMENDMENT 2026-09-19 (P0c name-match, additive — nothing above is altered):** this Purpose serves **`[E2] Enforced governance`** — "load-bearing conventions enforced by tools, not memory, so they can't silently drift", which is exactly the expiry-by-mechanism question — and **`[E9] Fleet Desired-State System (North Star)`**, whose reconciliation spine is the STOP this session takes. Added because the gate's P0c leg is a NAME-MATCH (§5 amendment A2) and the original text named no enumerated authority.<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->`none (primary tree)`<!-- FILL-IN:dest-worktree END --> · branch `main` · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->planning and decision surfaces only — `BACKLOG.md` via `tasks/`, `docs/decisions/`, `docs/intake/`, `protocols/`, `JOURNAL.md`; an executing change goes to a lane worktree, never to this seat's tree<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->the open items are way-of-working shape (how an exception expires, where the task graph comes from, what a refusing gate means), not a named backlog item to advance — that is the architect profile, not execution<!-- FILL-IN:dest-mode-basis END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `main`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

> **The `Destination` row is declared ex-ante** — a lane inherits none of it. Only its **branch**
> field has a mechanical counterpart (`PROBES.md` **P3**; mismatch = FAIL). Worktree, write-scope
> and MODE-basis stay prose and carry no probe leg — a leg that cannot fail honestly discredits
> the block (R3).

> **Nothing doctrinal is copied into this paste — five pointers, one hop each.** Launch commands:
> `protocols/PLAYBOOK.md` Ch8 "The dispatch table — the SOLE literal-command site" (**copy** a row;
> a composed line is the defect class that cost ~30 consecutive seats their lane —
> `STANDING_RULINGS.md` §V). Dispatch prep, batching, completion: Ch8 "Handoff prep for the next
> architect". Standing rulings applied without asking: `protocols/STANDING_RULINGS.md`. Operator
> runbook (who each file is for, the run loop): `docs/handoffs/README.md` — bundles carry no
> per-bundle README. Anti-bluff contract: this bundle's own `PROBES.md` header, spec
> `HANDOFF_PROCESS.md` §5. Ask CC to pull any of them.

---

=== ROLE PIN (protocols/HANDOFF_BOOT.md — RESIDENT, not inlined) ===

ROLE PIN — HANDOFF_BOOT.md @ handoff-process v7.1.0
sha256: a9a5a7a86408ef3bea3c4fdbac4cdf8fde3dff0c042ebb1e0c165357c0b0ed71
If your project instructions do not carry this contract at this version+sha, say so before answering.

---

=== RESIDUAL.md ===

# Residual — 2026-09-19-dev-knowledge-architect — the part the repo does not already encode

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

**Window** — the diff since `docs/handoffs/2026-09-17-dev-knowledge-architect/` was added.

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
**`fleet_parity` is a DECISION, not a defect.** Its `settings-deny-and-point` row was deliberately
set to hub-INVERSE this window: BUILD MODE rule 8 unwired that PreToolUse guard, so the hub is
expected to lack it and a consumer that still ships it is the divergence. The inversion is
therefore the correct reading of the live fleet, and a parity flag from that row is the mechanism
working. What is NOT decided: the parity schema has no row-level expiry the checker reads, so the
inversion cannot expire with BUILD MODE by itself — that gap is owned by its own row, and no field
was invented to paper over it. Every other parity flag is a defect and is owned as such.

**`reconciled_versions` is a defect if it flags.** It reads the registered specs against the docs
declaring a `reconciled_with:` edge; nothing this window did makes a mismatch intentional.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Terse map — detail is in `JOURNAL.md` 2026-09-19 entries (aq)-(au) and the rows themselves.

- `[#926]` — the two refuse-forever gates (`journal_day_letters`, `substrate_declaration`) narrowed
  to recognise the correction their own invariants permit. Temporary by construction: each check
  reads its own expiry constant, and past it the narrowing switches off and the finding names the
  row for re-ruling. **Row stays OPEN** — the expiry needs an operator re-ruling, not a closure.
- `[#921]` — filed: ARCHITECTURE re-read and restamped, R-2 re-landed, AX9-5 consumer declared.
- `[#922]`-`[#927]` — filed: the quick-fix arc's carried debt (silent rules drained, parity
  inverted, four audits given real consumers). No check was changed by that arc.
- `[#928]` — filed: the parity schema cannot express a row-level expiry (see §1).
- `[#916]` — amended: the ratchet drop removed prose, not risk; it is explicitly NOT a fix.

**Carried decisions — `carried-by: OPEN`, named here because the residual is their only carrier
(P11 leg 2).** Each of these states an OPEN carrier and has no repo home yet; the next session
either lands each one or re-declares the carriage:

- `to-cc/AMEND-ACCEPTANCE-TEST-CARRIER-2026-09-17.md`
- `to-cc/AMEND-BATCH-night-2026-09-17.md`
- `to-cc/AMEND-DISPATCH-UNBLOCK-2026-09-17.md`
- `to-cc/AMEND-MODEL-ROUTING-AND-SCOPE-2026-09-17.md`
- `to-cc/AMEND-NIGHT-ORDER-CONSOLIDATED-2026-09-17.md`
- `to-cc/AMEND-NIGHT-SALVAGE-2026-09-17.md`
- `to-cc/AMEND-ORGAN-USE-2026-09-17.md`
- `to-cc/BATCH-dispatch-order-2026-09-17.md`
- `to-cc/BATCH-night-2026-09-17.md`
- `to-cc/BATCH-night-wave2-2026-09-19.md`
- `to-cc/BATCH-night-wave2-CORRECTED-2026-09-19.md`
- `to-cc/BATCH-night-wave2-FINAL-2026-09-19.md`
- `to-cc/BATCH-night-wave2-FULL-2026-09-19.md`
- `to-cc/DECLARE-ACCEPTANCE-TEST-CARRIER-2026-09-17.md`
- `to-cc/DECLARE-BATCH-AC-CLOSE-2026-09-18.md`
- `to-cc/DECLARE-BATCH-AC-CLOSE-AMENDED-2026-09-18.md`
- `to-cc/DECLARE-BATCH-AC-NOT-CLOSED-2026-09-18.md`
- `to-cc/DECLARE-BUILD-MODE-2026-09-18.md`
- `to-cc/DECLARE-CENSUS-VERDICTS-2026-09-18.md`
- `to-cc/DECLARE-HARNESS-IS-PROCESS-2026-09-08.md`
- `to-cc/DECLARE-HARNESS-PROVENANCE-2026-09-08.md`
- `to-cc/DECLARE-LANE-HANDBACK-CONTRACT-2026-09-18.md`
- `to-cc/DECLARE-SPINE-AND-B3-2026-09-19.md`

**Carried WARN debt.** This window hands off with the ship-gate's open WARNs unresolved rather than
silenced; P7 re-derives them live. The organ-level attribution is generated in §1 above, and the
standing families are the register's. Nothing was dispositioned to make a gate pass — the two
gates that blocked the cut were fixed at their scoping defect, with a test proving the uncorrected
case still fails.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
The outgoing architect's own "why" is folded into this paste from `SUPPLEMENT.md` and is not
restated here. What follows is the executor-side residue: the questions this window's *work* left
open, each with the surface that would answer it.

**1. What makes a temporary measure expire by itself — and what happens when the schema cannot
hold an expiry?** This window landed two narrowings whose expiry is a constant the check itself
reads against one date seam, so they switch themselves off with no human in the loop. That shape
worked, and it is the pattern to generalise. But the same window hit a surface where it does not
fit: the parity schema has no row-level expiry field a checker reads, so a deliberately inverted
row cannot expire with the order that justified it. Inventing a field was refused. The open
question is whether expiry belongs in each schema or in one surface every dated exception
registers with. Owning rows: the narrowing row and the parity-schema row.

**2. Does a gate that refuses forever mean debt, or a scoping defect?** Both gates that blocked
this cut turned out to be the second kind: their invariant permitted exactly one correction, and
neither could recognise it. Neither was waived and neither was widened — the sanctioned escape on
one of them was refused on the record, because its own docstring says using it would falsify the
record. The transferable question: at a refusing gate, ask first whether the correction the
invariant permits is expressible to the check, before reaching for a disposition. There is still
no sanctioned FAIL waiver in this repo, which is a deliberate absence, not a gap to fill.

**3. Adversarial review is worth more than one pass, and the cost is bounded.** The narrowings
went through four cross-provider passes; the first three each found a way the narrowing was
WIDER than ordered (key collision, nested scope inheritance, case folding) and one finding was
rejected on the record with reasons. None would have been caught by the tests as first written.
The open design question is whether "review until a clean pass" becomes the lane standard, given
the passes are cheap relative to a landed widening.

**4. The preflight's cut criterion versus the tag's.** This cut proceeded on zero hard-fails with
the open WARNs carried explicitly in this residual, which is the preflight's actual contract — a
window may hand off with debt when the debt is explicit and owned, never when it is silent. Worth
knowing that the earlier reading (treating the tag's green as the cut's bar) is what deadlocked
this window in the first place.

**5. The carried decisions above are the real queue.** They accumulated because a decision file
can declare an OPEN carrier indefinitely and nothing ages it. The next session should treat
landing them as work, not as filing.
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

> **Contract, rationale, execution order, escalation ladder: `protocols/HANDOFF_PROCESS.md` §5 —
> there ONCE ([#611]).** Every row ships a **question + source-locator + command**, never an
> answer. CC runs the whole set against live state via `/handoff-verify` and emits **one evidence
> block**. **Any FAIL blocks onboarding; a missing required row is not a pass.** Table order IS
> execution order. Cut on `main` — which branch, not a value; re-derive live (P3). Run
> with `PYTHONUTF8=1`, and verify `ship-gate` (P7) in git-bash — a bare cp1252 PowerShell console
> false-REDs `handoff_probes`.

## P0 — Standing-topic reconciliation (above P1 — A7 / R2; rationale §5)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P0a | Quote, **substring-exact**, the theme-preamble line of each **active** `[E#]` theme in `BACKLOG.md`, and confirm the generated backlog is **CURRENT**. | `BACKLOG.md` `[E#]` theme headers + each preamble line | preambles drift on any theme edit, and a generated file can be stale | `grep -A1 '^## \[E' BACKLOG.md` → each quote substring-matches (a paraphrase FAILs); then `python scripts/gen_task_tree.py --check` exits 0 |
| P0b | Enumerate live the docs under `docs/intake/` with `status: ACCEPTED`, and quote each one's **TITLE line**. Titles only (§5). | `docs/intake/*.md` frontmatter + first heading; areas at `docs/intake/README.md` | the set and its titles drift on any status change; neither is in this bundle | `grep -l '^status: ACCEPTED' docs/intake/*.md` then read each hit's first heading |
| P0c | Does this bundle's **Purpose** NAME an authority the P0a/P0b enumeration returned? No match = **FAIL**. | `docs/handoffs/2026-09-19-dev-knowledge-architect/HANDOFF_BOOT.md` Purpose ∩ live P0a/P0b output | Purpose is hand-authored, the authorities are live; computable only after P0a and P0b run | `sed -n '/FILL-IN:purpose/,+1p' docs/handoffs/2026-09-19-dev-knowledge-architect/HANDOFF_BOOT.md` → it names an enumerated authority, or FAILs |

## P1 — Orientation (the architect's **first move** — §13c)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1a | Quote, **substring-exact**, the opening sentence of `README.md` `## Vision` — what .dev-knowledge is. In a child repo still on `VISION.md`, re-bind the path (ADR-114). | `README.md` `## Vision` | a paraphrase is not a substring; a summary rounds it off | `grep -A4 '^## Vision' README.md` → the quote must be a substring |
| P1b | Quote, **substring-exact**, the opening line of `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — where this work sits. | `ARCHITECTURE.md` `## Purpose [CORE]` | the line is in the live file only; a summary holds a gist | `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → the quote must be a substring |

**Gate:** no design until both orienting lines are held, read live and substring-matched. Then the
operator-context beat fires (§13d).
The operator has **filled** the supplement, so its ANSWERS are in the paste and the beat **NARROWS** to *"anything changed since the supplement was written?"*.

## Teeth probes (state fidelity — answers withheld, §5)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the last one? | `ALL_CHECKS` in `scripts/audit.py` | count and last name drift every time a check lands | `python scripts/audit.py checks` |
| P3 | Short **HEAD sha**, tree clean?, **branch** checked out, `main` **ahead/behind** `origin/main` — and does the live branch match the **Destination** row's branch field? Mismatch = **FAIL**. | live git ∩ the **Destination** row of `docs/handoffs/2026-09-19-dev-knowledge-architect/HANDOFF_BOOT.md` | Destination is declared ex-ante, the branch is read now | `git rev-parse --short HEAD`, `git status -sb`, `git branch --show-current`, `git rev-list --left-right --count origin/main...main` (the fourth leg is REQUIRED — §5), then compare against `docs/handoffs/2026-09-19-dev-knowledge-architect/HANDOFF_BOOT.md` |
| P4 | Which `#id`(s) does `validate_git_backlog` flag **now**, and the **full short-sha** of each closing merge? | live git ∩ `BACKLOG.md` | the set is computed at answer-time; the sha is high-entropy and in no document | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` **on/after or before** its last commit touch — and the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a relation over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — doc integer, live integer, do they match? | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer is in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) |
| P7 | Is `audit.py ship-gate` **GREEN or RED** now, **how many WARNs are dispositioned**, any `[stale]` disposition? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | the §1 headline, computed at answer-time; one direct-on-`main` commit re-REDs it | `python scripts/audit.py ship-gate` — read the verdict, the disposition count, any `[stale]` line; do **not** trust the residual's prose |
| P8a | File count of this bundle, is `SUPPLEMENT.md` present, ANSWERS empty or filled — and does each filled answer **CITE A FILE** (repo or transport path) rather than a chat turn? Chat-only = **FAIL** (§5). | `docs/handoffs/2026-09-19-dev-knowledge-architect/` listing ∩ `protocols/HANDOFF_PROCESS.md` §13 | a summary holds a stale count or fill-state; the citation form is readable only in the live text | `ls docs/handoffs/2026-09-19-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-09-19-dev-knowledge-architect/SUPPLEMENT.md` — substantive text below the divider, each answer naming a path |
| P8b | For the transport's `STATUS-<seat>.md` files: each one's **byte size**, and is its **first `## ` heading** the "now" section? Over **5,000 bytes**, or a first heading that is not "now", = **FAIL** (§5 — the threshold is bytes, not an ambiguous "5 KB"). | the live transport dir ∩ the grammar table in `protocols/OPERATOR-INTERFACE.md` `## 1. File exchange goes through the Downloads directory` | these belong to files written after this bundle was cut | `ls -l "$env:CLAUDE_PROMPTS_DIR/to-browser"` then `grep -n -m1 '^## '` per hit — report size + first heading each |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **now**, and which `#id`s are in the **code-edge** and **coherence** groups? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | group membership drifts on any BACKLOG edit and is absent here | `python scripts/validate_backlog.py` (the serialize-groups line) |
| P11 | For the window's decision files on the transport (`DECLARE-`, `AMEND-`, `BATCH-` prefixes): does a **flush-left `carried-by:`** appear in the file HEAD, and does its value name a repo home that **resolves on `main`** or state the literal `OPEN` (an `OPEN` being named in this bundle's residual)? Neither = **FAIL**. **Anchored and valued — a bare substring match is NOT this check** (§5). | the live transport dir ∩ `protocols/HANDOFF_PROCESS.md` §5 ∩ `docs/handoffs/2026-09-19-dev-knowledge-architect/RESIDUAL.md` | written after this bundle is cut: neither the file set, nor a carrier value, nor the residual's naming of them exists here | in the transport dir, per decision file: `head -6 "$f" \| grep -m1 -E '^carried-by:'` — an empty result is the FAIL set (the HEAD window and the `^` anchor are both load-bearing; `grep -l` over the whole file is a different and broken check, §5). Then take the value: `git cat-file -e main:<path>` for a path, else match the literal `OPEN` in `docs/handoffs/2026-09-19-dev-knowledge-architect/RESIDUAL.md`. Report per file WHICH value resolved and from where |

## Gate procedure (CC)

`protocols/HANDOFF_PROCESS.md` §5 — "Who runs it" + "Execution order" ([#611]). Table order IS the
execution order.

---

=== SUPPLEMENT.md ===

answers-to: to-browser/HANDOFF-SUPPLEMENT-2026-09-19.md (7 questions, verbatim from
templates/handoff/v5/SUPPLEMENT.md.tmpl; schema HANDOFF_PROCESS v7.1.0 §13)
authored-by: 2026-09-17-dev-knowledge-architect (Layer-1 browser seat, SEQ 1) — architect-authored,
CC transcribes verbatim and authors nothing here
date: 2026-09-19
scope: strategic WHY only — no repo state, no counts, no SHAs, no methodology restatement

# SUPPLEMENT ANSWERS — .dev-knowledge · architect · 2026-09-19

## 1. Strategic intent

**Stop making the architect knowledgeable; make the system answerable.**

A window's context expires and the next seat starts from nothing. Knowledge held in a seat does not
transfer; a query does. Every hour this window spent re-deriving what the repo already knew is the
cost of getting that backwards.

The concrete way-of-working goal: **the task graph comes from the program, not from the architect's
memory.** The spine runs, stops at the first stage that is missing or miswired, and names it. That
STOP is the queue. The next session should fix that one thing, re-run, and take the next STOP —
not re-plan a wave from a list it authored.

The second goal, equal in weight: **the operator is currently the status board and the copy-paste
relay.** He is asked ten times a day what is running, and he moves files between surfaces by hand.
That is a design defect, not a workload preference. Removing it is a way-of-working objective.

## 2. Tensions weighed

**Understand the whole system first, versus make it answerable.** Landed on answerable. The spine
passed several stages knowing nothing about the corpus, which proves comprehension is not a
precondition for connection. But the reverse also held: you cannot connect what you cannot name, so
coverage of the self-description graph is a real constraint and roughly half the corpus is outside
it.

**Delete, segregate by pointer, or inject.** Landed on inject. Deleting prose was refuted against a
peer repo that holds far more prose and hands over far less. Pointers were refuted by a
retrieval-discipline test written before the conversion. What survived measurement is the mechanism
nobody designed: descriptions that the harness injects into every session are consumed, while
pointers to files are not.

**The distiller as a gate versus as an injection.** Landed on injection. A refusal inside the
agent's tool loop hung a session for half a day; injection changes what the model sees before it
starts and cannot wedge. This is the single most consequential architectural choice of the window
and it rests on a hook property that is only partly verified.

**Build versus wire.** Landed on wire, and the inventory forced it: nothing on the build list was
genuinely absent. Everything planned already existed, unwired or uncalled.

**Speed versus truthfulness at the gate.** Landed on truthfulness, at the cost of this window's
handoff bundle. The gate offered a sanctioned escape whose own documentation says using it would
falsify the record; it was refused. A bundle cut over a gate cleared by fiat is worth less than no
bundle.

## 3. Considered and rejected — do not relitigate

**Deleting documentation to shrink context.** Refuted by measurement against the peer repos: they
segregate what is handed over, they do not hold less.

**Replacing preloaded content with pointers.** Refuted by a test written before the change. A small
model follows a bare pointer a minority of the time.

**A preloaded prose architecture map.** Refuted by its own pre-registered test, twice, on both a
prediction leg and a reads leg. The existing architecture document is KEPT by operator ruling, with
his stated exit condition: it is needed only while the executor cannot view the repository
holistically. Its removal is a deliberate spine-document supersession, never a delete.

**Adopting a code repo-map tool now.** Deferred, not rejected. A standing ruling defers it until a
consumer demonstrably hurts; the consumer that would use it already works without it; and it reads
code only, while this corpus is overwhelmingly prose. Its evaluation is done and recorded — do not
re-run it.

**Adopting the peer harness plugin.** Rejected on a head-to-head on an identical task: same verdict,
same defect count, an order of magnitude more cost and time. Our own lane contract won. This is the
answer to "they do it better than us" — measured, they do not.

**Byte targets as acceptance criteria.** Rejected three times over, each time after producing a
worse artifact. Acceptance is the question an artifact answers, never its size. A large
well-organised file is valuable; a small chaotic one is not.

**Raising the silent-rule baseline a second time.** Rejected. The first raise was accepted as a
one-off and explicitly not a precedent; raising it again would have made that sentence false and
turned a ratchet into a counter. The prose was removed instead — and that removal is NOT a fix,
because the underlying rule remains unenforced.

## 4. Open questions

**Does a registered command with an injected description actually get called unprompted?** The first
measurement scored zero. The whole line "the harness knows, so the architect needn't remember" rests
on this. Until it is answered, treat that line as unproven — not as a foundation.

**Does the rule forbidding any session from launching a lane survive its falsified premise?** It was
ratified on the belief that a nested session gets no visible row; that belief is contradicted twice,
once in a container and once on the host. The operator has been firing lanes by hand because of it.

**What makes a temporary measure expire by itself?** An emergency order marked temporary ran for
days because nothing expired it and nothing reported it. Every dated exception now proposed inherits
this question.

**Can a spend cap be enforced at launch rather than observed after the fact?** Today it is polled, so
a lane spends whatever it can between polls. Every budget this window set was exceeded, several
times over.

**Should the two gates that refuse forever be narrowed, and in what expiring form?** One counts
headings in an append-only file where correction-by-addition is the only correction its own
invariants permit; the other refuses on an immutable dated artifact that has already run. Both are
scoping defects rather than debt — but narrowing a gate touches every future session and the
operator's condition is that any such change be temporary by construction, with a test proving the
uncorrected case still fails.

**Can the distiller carry a real payload at prompt-submit time?** The hook survey answered part of
it; a distiller-sized injection is untested.

## 5. Decomposition rationale — and what NOT to redo

The wave shape is settled and should not be re-derived: disjoint surfaces, one worktree per lane,
a failing test before any code, cross-provider review before handback, commit-and-STOP, and a single
integrator that merges and never builds. It worked unattended, including a lane that refused to
weaken a check it inherited and one that surfaced a genuine conflict in its own contract rather than
resolving it.

**The important shift is where the graph comes from.** Earlier waves were decomposed by the
architect from a list. The last one was not: the spine named its own next failure. The next session
should NOT open by planning a wave. It should run the spine, read the STOP, fix that, and re-run.

Do not redo: the four refuted beliefs in §3; the census that replaced a binary with three states
(observed / reachable-but-unobserved / unreachable) and dissolved a number that had misled this
project three times; the split that keeps the hub shipping executable code while the caller runs it,
which satisfies both the operator's ruling and the layer invariant without suspending either; and
the decision that the architecture document stays.

Do not re-open the peer-repo comparison or the repo-map evaluation. Both are done, recorded, and
their conclusions are in §3.

## 6. Off-repo context — changed intent

**Dependencies are a consequence of library-first, not a question.** The operator overruled a request
for per-dependency consent as stalling. His condition replaced it and is stronger: a library is not
adopted until it has been run live and its output pasted. A library added without ever being
executed is declared, not adopted — and he named this as the central failure mode of LLM-driven
work.

**The window's purpose changed mid-course to consolidation.** No new execution; conclusions, cleanup,
handoff preparation.

**The dispatcher is expected to dispatch.** The operator firing a lane himself was recorded by him as
an exception, not the design. He said this before we discovered the rule that forced it rests on an
unmeasured premise.

**Lane count comes from logic and need, not from a ceiling.** The ceiling was a prosthesis for an
integration problem that is now only partly fixed.

**The operator's frustration is itself intent and should be read as a requirement.** Being the status
board, relaying files by hand, and being asked to remember what the system should know are named as
defects to remove, not as inconveniences to tolerate.

## 7. Ratified in chat, not yet in the repo

**Terms and rulings:**

- **"The STOP is the work queue."** A spine stage with no command — or one whose command was never
  actually invoked — is a disconnection made visible, and an uninvoked command is indistinguishable
  from a miswired one until called. Durable home: the spine's own doctrine section in PLAYBOOK.
- **"Declared is not adopted."** A dependency, or any library, counts as adopted only once it has
  been run and its output recorded. Home: the contract's library-first field specification.
- **"prior-art is a citation, not a sentence — and it searches our own archive before the world."**
  Ruled in chat; still only prose. Repeatedly this window the answer already existed in our own
  audits and was paid for again. Home: the contract field specification plus the gate that reads it.
- **"A ratchet drop that removes prose is not a fix."** Recorded in one row body today; it is
  doctrine and belongs where metrics are defined.
- **"Temporary is only safe when its expiry is a mechanism."** From an emergency order that outlived
  its own label. Home: LESSONS, and as a precondition on every dated exception.
- **"Acceptance is the question the artifact answers, never its size."** Three byte targets, three
  worse artifacts. Home: the contract's done-when specification.

**Interface behaviours relied on and not yet named in the operator-interface doc:**

- **The supplement round-trip over the transport.** Questions written to the browser-bound folder,
  answers authored by the browser seat and written back to the agent-bound folder, with the operator
  handing the executor one line naming the file. This was invented in this window specifically to
  stop the operator being a copy-paste relay in both directions. It needs a durable home.
- **The browser seat writing its own ledger and ratification records directly to the transport**,
  rather than asking the operator to relay them. Both were owed all window and were only written
  when a gate refused for their absence.
- **The session list of the agent console used as the fleet status board**, because no
  "where is this lane right now" surface exists. This is a workaround standing in for a candidate
  that was costed weeks ago and never consumed.

---

=== END OF PASTE — 5 sections · 34940 bytes ===
