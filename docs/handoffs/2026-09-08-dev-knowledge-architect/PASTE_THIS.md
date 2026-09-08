=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-09-08-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-09-08-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Rule the eleven carried questions. Two preflight rows were amended on 2026-09-08 so a window may hand off with debt that is **explicit and owned**; `[#642]` is the row that now owns those eleven, and its Done-when is this sitting. Second act: `[#638]`, whose four proof-layer WARNs are the ship-gate remainder this bundle carries. Start at `BACKLOG.md` `[#642]`, then `[#638]`.<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->none (primary tree)<!-- FILL-IN:dest-worktree END --> · branch `main` · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->answers and rulings written as files on the transport (`to-cc/ANSWER-*` / `DECLARE-*`); `tasks/` + `BACKLOG.md` where a ruling closes or re-owns a row. No lane work.<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->architect: the window's open items are rulings and way-of-working, not a named build. The two gate amendments this window landed were both operator rulings, and eleven more are queued.<!-- FILL-IN:dest-mode-basis END --> |
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

ROLE PIN — HANDOFF_BOOT.md @ handoff-process v7.0.0
sha256: 562c7e454efcd26d81dd6c28be855d9f0ee6bbd68d3487c38c856a3af1867e18
If your project instructions do not carry this contract at this version+sha, say so before answering.

---

=== RESIDUAL.md ===

# Residual — 2026-09-08-dev-knowledge-architect — the part the repo does not already encode

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

**Window** — the diff since `docs/handoffs/2026-09-06-dev-knowledge-architect/` was added.

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

<!-- FILL-IN:driftflags START (hand-authored — ONE judgment only: name which NEW flag above is a DECISION rather than a defect. The standing-vs-new attribution is GENERATED directly above; do not restate it. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->**`reconciled_versions` is the DECISION, not the defect.** This window changed `/handoff` preflight behaviour twice under operator ruling and deliberately did **not** bump `HANDOFF_PROCESS.md`'s `Version:`. The bump plus its three dependent re-stamps is owed and named -- it is one of the eleven questions `[#642]` carries (`QUESTION-lane-u-000-handoff-v71-build`), so the flag is a filed obligation with an owner, not drift nobody noticed. `fleet_parity` is the other NEW organ and is **not** claimed as a decision: this window added no parity surface, so a WARN there would be a defect to investigate, and P7 is what says whether one fired.<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->Two gate amendments and the row they required. Detail is in `JOURNAL.md` 2026-09-08 (e) and (f); this is the map.

- **preflight row 1** -- `hard-fail = 0 AND every undispositioned WARN named in the residual with its owning row`. Ruling `to-cc/DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08.md`. A handoff is not a release; the TAG gate's GREEN criterion (NC1 / 028-A) is unchanged.
- **preflight row 7** -- `ANSWERED (an ANSWER-*/DECLARE-* answers it) OR CARRIED (named in the residual with the OPEN backlog row that owns it)`; a CLOSED row does not carry, no owner is a FAIL. Ruling `to-cc/DECLARE-PREFLIGHT-QUESTION-ROW-2026-09-08.md`.
- **`[#642]`** (P1/S, new) -- the receiving surface the row-7 ruling presupposed and the repo did not have. See `BACKLOG.md`.
- Both amendments state the residual half as an **obligation they do not verify** -- the residual does not exist at preflight time. That is deliberate and is written into the docstrings, the register header and `.claude/commands/handoff.md`.<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->**FIRST, before any batch: the consolidated suite has not run.** Five attempts OOM-killed this
window (~2.6-3.5 GB free of 28 GB, held by OneDrive/VS Code/Chrome -- the operator's machine, not
the fleet's); a sixth killed this bundle's own first generation. Targeted tests, the full
pre-commit battery and the ship-gate all ran and passed; the *consolidated* run is the one thing
nobody has witnessed. It runs first.

**The debt handed over is OWNED -- the point of both amendments.**

*Ship-gate remainder: `[#638]` (P2) owns all four.* All four undispositioned findings are
`proof_layer` and render **identically**, which is why `[#638]` says no honest narrow `match`
exists: *`test_review_artifact_coverage.py` gates 1 test behind a function-level `skipif` on
`git`*. Fix, not suppression: move the property out from behind the guard, or make a skipped
proof render NOT-PROVEN. **No verdict or count is stated here -- P7 re-derives both live.**

*Carried questions, each with the OPEN row that owns it* (row 7's contract; files under
`to-browser/`, 2026-09-07 archive unless noted):

- `dispatcher-N2` -> `[#610]` (missing-manifest half) + `[#642]`
- `dispatcher-T` -> `[#628]`. **Answered in full** by `DECLARE-SITTING-2026-09-06`; reads as
  carried only because its disposition cites `[#628]` for the D12 ask. True, not a defect
- `integrator-N2-win-tooling-merge` -> `[#642]` (RAW vs UNRESOLVED HIGH)
- `lane-t-000-reds-spine` -> `[#642]` (does the batch-T GO discharge AF-1's owed ADR-98 intake)
- `lane-u-000-adr-carrier-split` -> `[#642]` (ADR-117: keep `Proposed`, admit `DRAFT`, or should
  not have landed)
- `lane-u-000-branch-enum-parity` -> `[#642]` (are the two ADR-85 organs SUPPOSED to differ)
- `lane-u-000-carrier-floor-v150-mechanisms` -> `[#642]` (`INSTALL.md` into
  `root_allowlist.files`, or retire the root path)
- `lane-u-000-deploy-tool-consumer-override` -> `[#605]` (its body names the same
  `deploy/tool.py` consumer-root site) + `[#642]`
- `lane-u-000-dispatch-receipt-is-work` -> `[#642]` (does `gh auth status` OK gate `absent`; may
  a lane DEPLOY to the operator's host)
- `lane-u-000-handoff-v71-build` -> `[#642]` (the 7.0.0 -> 7.1.0 bump + 3 re-stamps are OWED)
- `lane-u-000-shape-spec-finalize` -> `[#642]` (does the spec landing warrant a version bump)
- `lane-u-628-release-commit` -> `[#642]` (`reconciled_with` on an intake doc; a standing
  silent-rule ratchet headroom, currently ZERO)
- `handoff-cut-2026-09-08` (live) -> ANSWERED by `DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08`

**`[#642]` receives; it rules nothing.** Filed because the row-7 ruling named a "ratification list
row" that did not exist -- measured, not assumed: `RATIFICATION-2026-09-08.md` names none of the
eleven, and `docs/audits/2026-09-07-technical-batch-u-close-packet.md`, the one carrier that would
have covered them all, names **no QUESTION file at all**. Owner of record: this window's first
sitting. Rows 604 and 447 were checked and rejected as owners.

**Ten ratification seals still PENDING and unchanged** (`to-browser/RATIFICATION-2026-09-08.md`
section 1) -- nine of ten pending at the 2026-09-07 dawn list, nine of ten now; no sitting between.
`[#640]` owns seals 3 and 7, `[#641]` seal 10. `protocols/ESSENTIALS.md` is **not retired** --
census 52 consumers; re-point lane in batch V (D9 stands).<!-- FILL-IN:frontier END -->

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
| P0c | Does this bundle's **Purpose** NAME an authority the P0a/P0b enumeration returned? No match = **FAIL**. | `docs/handoffs/2026-09-08-dev-knowledge-architect/HANDOFF_BOOT.md` Purpose ∩ live P0a/P0b output | Purpose is hand-authored, the authorities are live; computable only after P0a and P0b run | `sed -n '/FILL-IN:purpose/,+1p' docs/handoffs/2026-09-08-dev-knowledge-architect/HANDOFF_BOOT.md` → it names an enumerated authority, or FAILs |

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
| P3 | Short **HEAD sha**, tree clean?, **branch** checked out, `main` **ahead/behind** `origin/main` — and does the live branch match the **Destination** row's branch field? Mismatch = **FAIL**. | live git ∩ the **Destination** row of `docs/handoffs/2026-09-08-dev-knowledge-architect/HANDOFF_BOOT.md` | Destination is declared ex-ante, the branch is read now | `git rev-parse --short HEAD`, `git status -sb`, `git branch --show-current`, `git rev-list --left-right --count origin/main...main` (the fourth leg is REQUIRED — §5), then compare against `docs/handoffs/2026-09-08-dev-knowledge-architect/HANDOFF_BOOT.md` |
| P4 | Which `#id`(s) does `validate_git_backlog` flag **now**, and the **full short-sha** of each closing merge? | live git ∩ `BACKLOG.md` | the set is computed at answer-time; the sha is high-entropy and in no document | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` **on/after or before** its last commit touch — and the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a relation over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — doc integer, live integer, do they match? | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer is in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) |
| P7 | Is `audit.py ship-gate` **GREEN or RED** now, **how many WARNs are dispositioned**, any `[stale]` disposition? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | the §1 headline, computed at answer-time; one direct-on-`main` commit re-REDs it | `python scripts/audit.py ship-gate` — read the verdict, the disposition count, any `[stale]` line; do **not** trust the residual's prose |
| P8a | File count of this bundle, is `SUPPLEMENT.md` present, ANSWERS empty or filled — and does each filled answer **CITE A FILE** (repo or transport path) rather than a chat turn? Chat-only = **FAIL** (§5). | `docs/handoffs/2026-09-08-dev-knowledge-architect/` listing ∩ `protocols/HANDOFF_PROCESS.md` §13 | a summary holds a stale count or fill-state; the citation form is readable only in the live text | `ls docs/handoffs/2026-09-08-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-09-08-dev-knowledge-architect/SUPPLEMENT.md` — substantive text below the divider, each answer naming a path |
| P8b | For the transport's `STATUS-<seat>.md` files: each one's **byte size**, and is its **first `## ` heading** the "now" section? Over **5,000 bytes**, or a first heading that is not "now", = **FAIL** (§5 — the threshold is bytes, not an ambiguous "5 KB"). | the live transport dir ∩ the grammar table in `protocols/OPERATOR-INTERFACE.md` `## 1. File exchange goes through the Downloads directory` | these belong to files written after this bundle was cut | `ls -l "$env:CLAUDE_PROMPTS_DIR/to-browser"` then `grep -n -m1 '^## '` per hit — report size + first heading each |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **now**, and which `#id`s are in the **code-edge** and **coherence** groups? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | group membership drifts on any BACKLOG edit and is absent here | `python scripts/validate_backlog.py` (the serialize-groups line) |
| P11 | For the window's decision files on the transport (`DECLARE-`, `AMEND-`, `BATCH-` prefixes): does a **flush-left `carried-by:`** appear in the file HEAD, and does its value name a repo home that **resolves on `main`** or state the literal `OPEN` (an `OPEN` being named in this bundle's residual)? Neither = **FAIL**. **Anchored and valued — a bare substring match is NOT this check** (§5). | the live transport dir ∩ `protocols/HANDOFF_PROCESS.md` §5 ∩ `docs/handoffs/2026-09-08-dev-knowledge-architect/RESIDUAL.md` | written after this bundle is cut: neither the file set, nor a carrier value, nor the residual's naming of them exists here | in the transport dir, per decision file: `head -6 "$f" \| grep -m1 -E '^carried-by:'` — an empty result is the FAIL set (the HEAD window and the `^` anchor are both load-bearing; `grep -l` over the whole file is a different and broken check, §5). Then take the value: `git cat-file -e main:<path>` for a path, else match the literal `OPEN` in `docs/handoffs/2026-09-08-dev-knowledge-architect/RESIDUAL.md`. Report per file WHICH value resolved and from where |

## Gate procedure (CC)

`protocols/HANDOFF_PROCESS.md` §5 — "Who runs it" + "Execution order" ([#611]). Table order IS the
execution order.

---

=== SUPPLEMENT.md ===

_Transcribed VERBATIM by the handoff seat from `to-cc/SUPPLEMENT-ANSWERS-2026-09-07.md` (6,206 B, byte-for-byte). Nothing below this line was edited._

# SUPPLEMENT — ANSWERS from the browser architect (window 2026-09-06 → 2026-09-07) — authored by the browser; the handoff seat transcribes VERBATIM


## Q1 · Strategic intent for the next session (way of working)
Stop adding organs; make the existing ones one system. Three moves, in order: (1) the repo graph (FPG-1) becomes the single source for corpus-structure edges and `orphan_census` is its first query; (2) every rule that failed in batches T/U becomes a REFUSAL in a seat template or a launcher (sleeping poll, lane ceiling 4–6, `reads: path@sha` + PLAN/INFORMATION head, reviewer model in the tally, receipt = commit), so no seat can repeat this window's failures; (3) batch size ≤ 6, one sitting per browser window, decisions only as files. Measure by: substantive-commit share (was ≈ 10 %), human points on the critical path (was 14), orphans (count), tokens per window (browser ≤ 10 Fable turns).

## Q2 · Tensions weighed — where I landed
- Speed vs ceiling: I ran 15 and 19 lanes; merges cost 9–28 s but every coordination failure scaled with lane count (dispatcher turn-end on wait, superseded integrator, reaped sessions, destroyed handback). Landed: ≤ 6, mechanisms first.
- Graph as engine vs graph as view: the architecture review proved two-tree gates cannot be views and that Z-C3 stands. Landed: FPG-1 for corpus edges only; state gates stay gates; graph computed by the hub over consumer trees read-only (not shipped as a pull component — a consumer of identical shape yields an empty graph).
- Push vs pull carrier (ADR-117): landed on the divergence discriminator; flip-condition recorded ([#616]).
- Browser: two chats vs one: landed one chat, model per act, tags on every reply, ≤ 40 turns.
- LLM in the data structure: landed as METHODS with recorded outputs (`describe()`, `evaluate()` on the grey zone), never as the judge on a gate's hot path.
- Pre-handoff hygiene: landed as preflight ROWS (mechanism), not a checklist the operator invents each time — see Q7.

## Q3 · Considered + rejected (do not relitigate)
Second browser chat (synchronisation cost, no token gain) · URL-management engine (identity = id, layout identical → resolver is a dictionary) · an LLM instance in every node · hub-only graph · graph shipped as a pull component · Rust/C# for gates (measured) · multiplayer/ADE · reminder hooks that re-argue rules · HTML companions per artifact · judged score beside mechanical (deferred) · ruling 336 seal waivers by hand (fix the two hub-local rules first) · codespace as producer substrate until receipt = commit · pasting CC transcripts into the browser.

## Q4 · Open questions (deferred deliberately)
ADR-85 amendment (spine anchor from merge commit, WARN at commit) — operator ruling · the 2026-08-29 deploy freeze — never ruled, blocks H0 step 4 · which of the 24 hooks / 56 checks retire (S-10 census supplies zero-true-finding organs) · #75 offload admission (Enterprise) · #76 one-chat topology · MEMORY.md drop list · the two seal-rule fixes before any consumer ruling · what the interface review §5 says about the browser's cost (unread in full).

## Q5 · Decomposition rationale — do not redo
Batches T and U are CLOSED on the hard metric (packet on main after integrator-N3 lands it). Do not re-run: NC1 clearing, freshness stamps, README, PLAYBOOK re-read, seal report (fleet), shape spec, ADR-117, deploy-tool override, plugin drift, ADR template (Flip-condition + Alternatives REQUIRED), handoff v7.1 build, 13 censuses. The 5 human decisions stay human (GO, ratification, tag, destructive acts on live seats, seat release); everything else in 036 wave 2 is mechanism work.

## Q6 · Off-repo context — changed INTENT only
Operator's word this window: identical layout everywhere (shape, not content) — waivers are exceptions with a reason, not a way of life; universalization by mechanism; think-before-act as the browser's fixed order (033); "cook and clean" — every batch carries hygiene; the fleet is "a new programming paradigm": classic data structures and patterns are the skeleton, models complement them; he wants Enterprise tokens used ($90, product unidentified) and Gemini used as a reader; he leaves at night and wants ≥ 12-lane unattended batches — now bounded by the 4–6 ceiling per batch, so "unattended" means several small batches chained by files, not one large one.

## Q7 · Ratified-in-chat register (not yet in the repo unless noted)
- THINK-BEFORE-ACT order (033) → OPERATOR-INTERFACE §2 + floor item 7 (filed; not landed).
- Model tag on every browser reply (ROUTINE / RULING AHEAD with cost) → same (DECLARE-BROWSER-TOPOLOGY; not landed).
- Decisions are files with a `carried-by:` line; P11 probe → v7.1 (W1-9 landed P11; `carried-by:` fill owed by filings).
- Lane ceiling 4–6 enforced at dispatcher step 0 → PLAYBOOK Ch8 (not landed).
- No seat ends a turn on a peer wait; file is the only coordination primitive → PLAYBOOK Ch8 "Batch communication" (section landed via 30c6e587; the poll-as-code not landed).
- Reviewer model name in the tally; mismatch = review=NONE → PLAYBOOK Ch8 (not landed).
- "A cited SHA is checked, not inherited"; "a clean tree is not a stop signal"; "destroyed, not withheld" (a reaper destroying a handback channel) → LESSONS (JOURNAL (r) landed).
- Pre-handoff hygiene = preflight rows: ship-gate 0/0 or dispositioned · LEDGER refreshed · RATIFICATION current · STATUS ≤ 5 KB archived · living docs stamped · JOURNAL anchored · QUESTION files answered or carried · MEMORY.md within cap · no worktree without a live owner → `/handoff` preflight (CLOSE batch lane).
- Interface behaviours relied on: `.md` uploads for anything > a screen; the END sentinel; Drive connector for browser writes (rename-then-create to overwrite); the daemon's env block as the real source of `CLAUDE_PROMPTS_DIR` (E-29) → OPERATOR-INTERFACE §1.
=== END OF SUPPLEMENT ANSWERS ===

---

=== END OF PASTE — 5 sections · 27466 bytes ===
