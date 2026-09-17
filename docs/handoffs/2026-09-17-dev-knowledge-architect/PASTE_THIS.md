=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-09-17-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-09-17-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Rule the decisions this window could not take, and get ONE lane through the loop. Intake 103 §0.6 sets the successor's bar — one lane from dispatch to merged in under an hour, nothing wedged, no human decision in the middle — and records that no row carries it; that is the first thing to place. The second is the hook settlement: three required hooks are restored and witnessed running, but `propose_closures.py` still runs with no per-repo lever, and `[#888]` says the repo has no way to record a required component as deliberately absent. Row state: `BACKLOG.md` (themes E1–E2, stories S2–S3).<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->`none (primary tree)`<!-- FILL-IN:dest-worktree END --> · branch `main` · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->planning and governance surfaces — `docs/intake/`, `docs/decisions/`, `tasks/` + the generated `BACKLOG.md`, `protocols/`; NOT `scripts/` build work, which belongs to a lane under the batch protocol<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->the open items are rulings, not builds (ADR-87 item 5): an uncarried acceptance test, a plugin-hook lever that does not exist, ADR-102's never-waivable rule versus a DEGRADED state, and ~25 intake-103 §G findings owed one ADR-111 funnel state each<!-- FILL-IN:dest-mode-basis END --> |
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

1. **`propose_closures.py` is RULED KNOWN-UNGOVERNABLE and stays RUNNING** (plugin `Stop`, 15%,
   operator 2026-09-17) — loaded in place from `plugins/tier1-lifecycle/hooks/hooks.json`, so every
   lever is machine-wide/fleet-wide or reds parity `settings-plugin-tier1` (MUST). No per-repo
   option exists, so disabling it costs more than it saves. **Do not re-derive this dead end**; the
   settings register carries the reason. It reopens only if Claude Code gains a per-hook off switch
   outside the tracked settings file.
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

### The six contradicting rule pairs are ANSWERED and UNBUILT — "ruled" is not "done"

`to-cc/ANSWER-contradicting-rules-2026-09-16.md` — **P1=C P2=A P3=B P4=C P5=A P6=B**, reason per pair.
**Nothing is implemented, and the operator rules that this be said plainly rather than left to read
as done.** P4 (drop the `allow` from the gitignored `settings.local.json`, add a narrow ask rule for
merges onto `main`) and P5 (wire ADR-110's refusal into the dispatch verb, so it fires before a lane
session starts) name acts **no commit has made**. An answered decision with no implementing act is
the exact gap this window spent itself finding: the answer changes nothing until something enforces
it, and no row yet carries these six.

### FINDING — a cut can never be complete at its own preflight

Witnessed at this cut, and the same shape as everything else this window: **a gate that cannot see
the thing it is meant to guarantee.** `gen_handoff.py`'s ten preflight rows run BEFORE the generator
writes a byte, so no row can see an unfilled `FILL-IN` region in a file that does not yet exist. The
organs that do see it — `residual_completeness` and `handoff_probes` (P11 leg 2) — are **ship-gate**
members, and the gate's next run is normally AFTER the bundle is committed. This bundle proved it:
ten rows passed, `RESIDUAL.md` was filled, the assembler re-run, the bundle committed, merged and
pushed — with `HANDOFF_BOOT.md`'s four header regions still carrying `_(fill: ...)` placeholder text,
embedded verbatim into `PASTE_THIS.md`. A seat booting that paste would have read *"(fill: why this
mode)"* as its session header. Caught by `audit.py ship-gate` afterwards (9 of its 12 hard-fails were
these regions across BOOT + PASTE_THIS) and repaired in a follow-up commit; JOURNAL 2026-09-17 (y).
**The rule this leaves:** filling is part of the cut, and the cut is not done until a POST-fill check
runs — `validate_residual_completeness.py` and `verify_handoff_probes.py` take seconds each, against
the ~4.5 minutes of the full gate. Whether that belongs in the handoff command as a mechanism rather
than this sentence is the successor's call.

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
| P0c | Does this bundle's **Purpose** NAME an authority the P0a/P0b enumeration returned? No match = **FAIL**. | `docs/handoffs/2026-09-17-dev-knowledge-architect/HANDOFF_BOOT.md` Purpose ∩ live P0a/P0b output | Purpose is hand-authored, the authorities are live; computable only after P0a and P0b run | `sed -n '/FILL-IN:purpose/,+1p' docs/handoffs/2026-09-17-dev-knowledge-architect/HANDOFF_BOOT.md` → it names an enumerated authority, or FAILs |

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
| P3 | Short **HEAD sha**, tree clean?, **branch** checked out, `main` **ahead/behind** `origin/main` — and does the live branch match the **Destination** row's branch field? Mismatch = **FAIL**. | live git ∩ the **Destination** row of `docs/handoffs/2026-09-17-dev-knowledge-architect/HANDOFF_BOOT.md` | Destination is declared ex-ante, the branch is read now | `git rev-parse --short HEAD`, `git status -sb`, `git branch --show-current`, `git rev-list --left-right --count origin/main...main` (the fourth leg is REQUIRED — §5), then compare against `docs/handoffs/2026-09-17-dev-knowledge-architect/HANDOFF_BOOT.md` |
| P4 | Which `#id`(s) does `validate_git_backlog` flag **now**, and the **full short-sha** of each closing merge? | live git ∩ `BACKLOG.md` | the set is computed at answer-time; the sha is high-entropy and in no document | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` **on/after or before** its last commit touch — and the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a relation over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — doc integer, live integer, do they match? | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer is in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) |
| P7 | Is `audit.py ship-gate` **GREEN or RED** now, **how many WARNs are dispositioned**, any `[stale]` disposition? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | the §1 headline, computed at answer-time; one direct-on-`main` commit re-REDs it | `python scripts/audit.py ship-gate` — read the verdict, the disposition count, any `[stale]` line; do **not** trust the residual's prose |
| P8a | File count of this bundle, is `SUPPLEMENT.md` present, ANSWERS empty or filled — and does each filled answer **CITE A FILE** (repo or transport path) rather than a chat turn? Chat-only = **FAIL** (§5). | `docs/handoffs/2026-09-17-dev-knowledge-architect/` listing ∩ `protocols/HANDOFF_PROCESS.md` §13 | a summary holds a stale count or fill-state; the citation form is readable only in the live text | `ls docs/handoffs/2026-09-17-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-09-17-dev-knowledge-architect/SUPPLEMENT.md` — substantive text below the divider, each answer naming a path |
| P8b | For the transport's `STATUS-<seat>.md` files: each one's **byte size**, and is its **first `## ` heading** the "now" section? Over **5,000 bytes**, or a first heading that is not "now", = **FAIL** (§5 — the threshold is bytes, not an ambiguous "5 KB"). | the live transport dir ∩ the grammar table in `protocols/OPERATOR-INTERFACE.md` `## 1. File exchange goes through the Downloads directory` | these belong to files written after this bundle was cut | `ls -l "$env:CLAUDE_PROMPTS_DIR/to-browser"` then `grep -n -m1 '^## '` per hit — report size + first heading each |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **now**, and which `#id`s are in the **code-edge** and **coherence** groups? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | group membership drifts on any BACKLOG edit and is absent here | `python scripts/validate_backlog.py` (the serialize-groups line) |
| P11 | For the window's decision files on the transport (`DECLARE-`, `AMEND-`, `BATCH-` prefixes): does a **flush-left `carried-by:`** appear in the file HEAD, and does its value name a repo home that **resolves on `main`** or state the literal `OPEN` (an `OPEN` being named in this bundle's residual)? Neither = **FAIL**. **Anchored and valued — a bare substring match is NOT this check** (§5). | the live transport dir ∩ `protocols/HANDOFF_PROCESS.md` §5 ∩ `docs/handoffs/2026-09-17-dev-knowledge-architect/RESIDUAL.md` | written after this bundle is cut: neither the file set, nor a carrier value, nor the residual's naming of them exists here | in the transport dir, per decision file: `head -6 "$f" \| grep -m1 -E '^carried-by:'` — an empty result is the FAIL set (the HEAD window and the `^` anchor are both load-bearing; `grep -l` over the whole file is a different and broken check, §5). Then take the value: `git cat-file -e main:<path>` for a path, else match the literal `OPEN` in `docs/handoffs/2026-09-17-dev-knowledge-architect/RESIDUAL.md`. Report per file WHICH value resolved and from where |

## Gate procedure (CC)

`protocols/HANDOFF_PROCESS.md` §5 — "Who runs it" + "Execution order" ([#611]). Table order IS the
execution order.

---

=== SUPPLEMENT.md ===

SUPPLEMENT ANSWERS — authored by the browser architect, transcribe VERBATIM, do not summarise or reword.

Q1 — STRATEGIC INTENT
Stop adding mechanisms. Prove throughput. This window added ~15 mechanisms and removed none until the system stopped working; the commit gate reached 34 hooks at ~244 s while the guards it fronted were failing open and nothing counted either fact. The next session's goal at the way-of-working level is a single falsifiable acceptance test: ONE LANE RUNS END TO END, DISPATCH TO MERGED, IN UNDER ONE HOUR, WITH NOTHING WEDGED AND NO HUMAN DECISION IN THE MIDDLE. Until that passes, no new organ is built. Governing rule for everything after it: a mechanism ships with a COUNTER — what it caught, what it cost, over what window — and a gate with no catch in its window is REMOVED, not tuned. Every ruling this window carried a refusal criterion and none carried a cost criterion; that asymmetry is why the harness became its own bottleneck.

Q2 — TENSIONS WEIGHED, AND WHERE THIS SEAT LANDED
(a) Enforcement vs throughput. Landed: enforcement must be priced. Evidence: 34 hooks / ~244 s mean; ~17 agent-hours lost to a gate-bound commit starving subagents; a 6-hour wedged integrator; a full night lost to hook processes. Enforcement moves EARLIER where it can (a refusal that prevents work beats one that discovers it) but nothing joins the commit tier without a measured cost in its Done-when.
(b) Emergency blanket disable vs measured individual disable. Landed: individual, measured. The blanket disableAllHooks was this seat's panic; lane ab-808's measurement later showed the three REQUIRED hooks were never among the nine that wedge. We disabled hooks that never failed in order to stop hooks that did.
(c) Prose vs data as the source of truth. Landed: data is the source, prose is a rendered view, and a divergence is a refusal. Evidence: 115 citations of PLAYBOOK/STANDING_RULINGS with 57 the ONLY carrier of their rule; dispatch_drift parsing a prose table and passing only because one machine carried an unmerged branch; the manifest's id blocks being prose, which is why a row landed outside every block.
(d) Windows vs portable. Landed: this is NOT primarily an OS problem. 8.9 % of lines are Windows-only and 43 of 51 Linux failures are fleet-shape assumptions, not OS. The coupling that hurts is to THIS WORKSTATION, not to Windows.
(e) Browser as mechanism vs repo as mechanism. Landed: the repo. Three times this seat offered its own vigilance as the safeguard — sampling transcripts, remembering to boot an integrator, holding rules in pastes. All three failed. The operator's standing rule stands: the browser is the weakest link and the repo must protect itself from it.

Q3 — CONSIDERED AND REJECTED (do not relitigate)

- Rewriting the hooks: REJECTED. The defect is upstream process spawn — hook processes were created SUSPENDED, 0 s CPU, no image path, one thread in Wait/Suspended. Our scripts never executed a line. Rewriting them fixes nothing.
- The bounded-hook wrapper as THE fix: REJECTED as sufficient (kept as a module). A timeout cannot fire on a process that never starts, and the wrapper adds one more interpreter to every hook.
- Restoring hook declarations while execution stays disabled: REJECTED as a workaround. The gate would report "required hooks present" when they do not run — green without substance, the exact class this window spent itself finding.
- Handoff without a bundle: REJECTED by the operator, correctly. Capitulation, not a solution.
- disableAllHooks as a resting state: REJECTED. Emergency measure only; it must not become normal by habit.
- A separate per-batch state carrier in the benchmark's shape: REJECTED structurally — a second authority over row state.
- Sequential-only lane execution: REJECTED. Worktrees exist for parallelism; the sequencing was this seat's caution under a memory constraint and it outlived the constraint by two days.
- Migrating dispatch to Python NOW: DEFERRED, not rejected — only three dispatch pieces are truly Windows-only and DispatchHelpers.psm1 makes 0 Start-Process / job-object calls; `claude --bg --worktree` does the launching and isolation itself.

Q4 — OPEN QUESTIONS

- Does the repo get a DEGRADED state? This is the cause behind every emergency this window: there is no way to record "this required component is deliberately absent, owned by X, expiring on Y". fleet_parity stops at a missing required hook before reading any waiver and ADR-102 forbids marking one waivable, so an emergency leaves only two options: lie to the gate or stop work. [#886] names the symptom.
- Per-task EXECUTION state: extend the existing row, or a new carrier. All three benchmarks converge on this and we still have no row. Phase 1 (establish what [#664], tasks/ frontmatter, manifest.json, FPG-1 and the organ index already hold) MUST run before anything is built beside what exists.
- The six contradicting rule pairs are ANSWERED this window (P1=C P2=A P3=B P4=C P5=A P6=B) but their ENFORCEMENT is not built.
- CI enforcement: on, or documented as report-only. Today it is disabled and three red pushes landed.
- The Actions credential, on SECURITY grounds (a narrower blast radius than every lane inheriting the whole .env), not on the CI claim — there is no runner.
- Codespace contract delivery: commit the contract to the repo before dispatch (expected answer), pass it in the prompt, or a skill reading Drive through its API. The Drive-has-no-Linux-client framing is a symptom of the browser being the transport, not a blocker.
- Non-Claude producers: capability is PROVEN (copilot 10/10, codex 10/10, agy 10/10) and production use is still ~zero against USD 8,721 at 99.47 % Opus.
- Dispatch layer to Python: ~9 lanes, evidence in the OS-coupling digest.

Q5 — DECOMPOSITION RATIONALE; WHAT THE NEXT SESSION MUST NOT REDO
Order work by MEASURED COST OF INACTION, not by size of problem. This seat ordered by size twice and the four cheapest wirings — each costing measured hours per week — waited behind one large structural lane.
DO NOT REDO, all of it is in intake 103 (docs/intake/2026-09-16-tech-browser-seat-findings-off-the-transport.md) and the transport digests:

- the rules-to-enforcement ladder audit (115 citations, 47 rule families, 33 hook events, exit 1 never blocks, allow/ask inert under bypassPermissions)
- the lane anatomy measurement (model time 13-25 %; 62-86 % is the box and our own mechanisms)
- the OS-coupling audit (8.9 %, DispatchHelpers 43.6 % of it, 43 of 51 Linux failures are fleet-shape)
- the AJ M04 matrix and the benchmark comparison
- the closure census (25 rows closable with a witness)
- the prose-as-source measurement
  ALREADY LANDED, do not rebuild: the task-id allocator (reserve by PUSH; the local maximum is never read), /lane-boot refusing a batch with no committed manifest, the prompts guard failing closed, the conductor reading the frozen baseline, the deletion method with paired before/after suites, BACKLOG narration relocation (99,961 → 75,143 B).
  READ THE EVIDENCE BASE FIRST: git log and JOURNAL carry every change this window with its reasoning. The next session should reconstruct what happened from those two, not from anyone's memory.

Q6 — OFF-REPO INTENT THAT MOVED THIS WINDOW

- TOKEN EFFICIENCY IS NOW THE OPERATOR'S TOP CONSTRAINT. Roughly half a weekly quota is spent; USD 8,721 measured at 99.47 % Opus. Every other model is to be maximised before Opus, without losing quality.
- He ruled, and does not want asked again, that the employer-paid GitHub Enterprise Copilot quota MAY be used on these repos.
- Direction: OS-agnostic, Python-first where it is cheap. His words, and the measurement supports the direction without supporting urgency.
- The harness must USE THE TOOLS IT BUILDS, and that use must be MEASURED — organ calls versus raw scans per session is his question and it has never had a number.
- Continuous work, no night gating; his workstation is available.
- Codespace is the intended off-box substrate; the container is proven, the transport is not.
- TRUST IS LOW AND EARNED BACK BY DELIVERY, NOT ANALYSIS. He has had a week of audits and measurements and cannot yet run one lane cleanly. The next session should ship the acceptance test in Q1 before it proposes anything.

Q7 — RATIFIED IN CHAT, NOT YET IN THE REPO
RULINGS AND TERMS:

- "A mechanism ships with a counter — what it caught, what it cost, over what window; a gate with no catch in its window is removed, not tuned." Home: LESSONS + PLAYBOOK.
- "A verb's reported success is not evidence of its effect." Four witnessed surfaces: `claude stop` returning success with the tree alive; Codespaces reporting healthy while serving a recovery container; a cloud request reporting "launched successfully" after falling back to local; our own hooks exiting 1 reporting a pass while blocking nothing. Home: ADR or LESSONS.
- "Prose is documentation, not a source of truth for execution; execution reads data, prose is a rendered view, a divergence is a refusal." The operator's own formulation. Home: ADR.
- "A rule with no enforcement point is not a rule." Home: the enforcement register.
- The one-hour acceptance test (Q1). Home: a BACKLOG row plus PLAYBOOK.
- The six-pair answers P1=C P2=A P3=B P4=C P5=A P6=B, answered in chat today; each pair's enforcement is unbuilt.
- "An emergency change records its temporary debt as DATA with an owner and an expiry, never as a JOURNAL sentence." [#886] filed.
- "A research dispatch states its agent cap, its per-agent deadline and its token budget up front." [#884] filed, after one research session consumed ~0.5M tokens over 17 hours and was killed mid-step with nothing written.
- "Declaration and execution are two different things" — conflating them is what made this window's hook debt unrecordable.
  INTERFACE BEHAVIOURS RELIED ON, not yet named in protocols/OPERATOR-INTERFACE.md:
- A LARGE INLINE PASTE ARRIVES EMPTY at the browser seat. The operator had to upload CC output as .md files, and the browser seat could only read them from disk with a shell tool rather than seeing them in context. This happened repeatedly and cost turns before it was diagnosed. Home: OPERATOR-INTERFACE.md.
- SESSION LIVENESS IS TESTED BY COMPARING TWO SAMPLES of the session's own counters (elapsed time, token count, last step), never by reading the transcript's content. This seat reported a wedged integrator as "working" for hours because it judged by content; the two-sample test was available and unused. Home: OPERATOR-INTERFACE.md or PLAYBOOK.
- A SESSION INSIDE A LONG TOOL CALL CANNOT RECEIVE AN INSTRUCTION until the call returns, so "stop" is undeliverable to the session that most needs it; the only remedy today is killing it, which loses what it held. [#769] covers the commit-gate case only. Home: OPERATOR-INTERFACE.md plus a row.
  === END OF SUPPLEMENT ANSWERS ===

---

=== END OF PASTE — 5 sections · 37314 bytes ===
