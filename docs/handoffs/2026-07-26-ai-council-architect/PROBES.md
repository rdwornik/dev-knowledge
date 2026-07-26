# Probe manifest — architect mode: orientation first, then teeth (HANDOFF_PROCESS §5 + §13c)
<!-- scope: meta -->

> **Contract.** Each probe ships a **question + source-locator + verification command** and **no
> answer**. The browser has no file access, so for every probe it must reply **"run `<command>`"** —
> surfacing the off-bundle dependency instead of bluffing it. **CC** runs each command against **live
> state at check-time**, re-derives ground truth, and records PASS/FAIL. **Any FAIL blocks
> onboarding.** Degrade loudly: a moved anchor → WARN `anchor-missing`, re-anchor (never a synthesized
> pass); git/tooling absent → reported *skipped* (degraded coverage visible), never counted as pass.
>
> **Anti-bluff (HANDOFF_PROCESS §5 — a probe that bakes its answer is bluffable, rejected).** This
> manifest **withholds every answer value** by construction: no counts, SHAs, dates, verdicts,
> exit codes, set-memberships, or orienting lines are stated. That withholding IS the teeth. The pass
> criterion is **"answered from the live source at check-time,"** never "matches a remembered number."
> Generation hints (if any) live in the JOURNAL generation-entry, which the browser never sees — never
> here. The validator `scripts/verify_handoff_probes.py` FAILs any probe row that prints an answer hint.
>
> **Branch note.** This bundle was generated on branch `docs/handoff-2026-07-26-ai-council` **in the
> hub**. That names only which hub branch hosted generation — **re-derive the TARGET's HEAD / tree /
> branch / ahead-behind live (P3); do not trust this line.**

## ⚠ CROSS-REPO BUNDLE — read this before running anything

This is a **cross-repo** handoff (ADR-36/41): the **target** is `ai-council`; the **bundle** is
generated and stored in the `.dev-knowledge` hub. The two live in different working directories, so
every probe below names its **run-in root** explicitly:

| Run-in root | Path | Which probes |
|---|---|---|
| **TARGET** (`ai-council`) | `Dev/ai-council` | **all of them — P1a, P1b, P2–P16** |
| **HUB** (`.dev-knowledge`) | `Dev/.dev-knowledge` | none (the hub only *hosts* this bundle) |

Every probe binds to the target and resolves from the target root — the bundle declares
`| **Target repo** | ai-council |` in `HANDOFF_BOOT.md`, which is what makes the hub's
`check_handoff_probes` resolve foreign paths against `ai-council` instead of against itself (and so
avoids both false FAILs and false PASSes from basename collisions like `JOURNAL.md`).

**The generator's default probe set is hub-bound and has been re-authored.** `ai-council` carries
**no** `scripts/audit.py`, **no** `validate_git_backlog.py`, **no** `ecosystem/doc-counts.md`, and
**no** `ecosystem/disposition-register.yaml` — the stock P2/P4/P6/P7 rows would have FAILed
`anchor-missing` on all four. Each was re-bound to a **verified-live** `ai-council` surface (every
anchor below was confirmed present at generation time by running its command in the target). Where the
hub has an organ `ai-council` genuinely lacks, the probe says so rather than inventing an equivalent.

**What changed since the last cross-repo bundle — three probes were retired or re-pointed because the
thing they measured was RESOLVED this window.** Do not carry the previous bundle's framing:

- **The registry-completeness gap is closed.** Last bundle's P11 asked which of the fourteen specified
  rules had no row in the checker's registry. All fourteen are now registered (implemented, held-stub,
  or structural). **P11 is re-bound** to the defect that replaced it: rule 4's *implementation* reads
  fewer doc surfaces than its spec claims.
- **The `gc.auto` probe is retired.** Last bundle's P15 bound to an **uncommitted local config value**
  holding unreachable objects alive. That mechanism was **replaced by real refs** this window. **P15 is
  re-bound** to those refs — whose whole point is that they are now verifiable from a clone.
- **The id-reservation fence moved.** Two reservations were **discharged** and a different id is now
  fenced. **P13 re-derives the live set** rather than the remembered one.

**READ-ONLY ON THE TARGET (ADR-36/41 — hard).** Every command below is read-only. Do **not** run
`pre-commit run --all-files` in `ai-council` as a probe: its `normalize-headers` / `toc-generate`
hooks are **formatters that rewrite files**, which would violate the read-only contract on a
cross-repo target. The P7 sweep calls the read-only validators directly instead. `scripts/check.ps1`
is likewise **not** a probe — it is the full pytest+mypy+ruff trio, far past read-only-cheap; P6 and
P12 call the two pieces a probe actually needs.

> **`SUPPLEMENT.md` is generated EMPTY.** Unless the operator fills it before this bundle is pasted,
> the assembler folds nothing and the incoming §13(d) operator-context beat fires **FULL** — a full
> off-repo ask, not the narrowed *"anything changed since?"*. The residual is therefore the **only**
> carried "why" this window, and it is repo-derived by construction: it cannot carry operator intent.
> **The probes outrank it on every number.**

## P1 — Orientation (the architect's **first move**, before any mechanism — §13c)

A plain-language "what is this project" is **summary-bluffable** and so fails §5's own bar; a copy of
VISION into the handoff is barred (§2/§3). So orientation is a **forced exact-line read**: the line
enters the session **only** by CC reading the **live** primary source, and the quote must match as a
**substring** (never a paraphrase). The browser has no files → it replies **"run `<command>`"**; CC
reads live and substring-checks. The grep is a **tool** that confirms the frame — **the backlog
navigates** (§13c), not this read.

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via (run in **TARGET**) |
|---|---|---|---|---|
| P1a | Quote, **substring-exact**, the **opening sentence** of `VISION.md` `## Vision` — *what ai-council is*. | `VISION.md` `## Vision` | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' VISION.md` → the quote must be a substring of the live section |
| P1b | Quote, **substring-exact**, the **opening line** of `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — *where this work sits in the `Dev/` ecosystem*. | `ARCHITECTURE.md` `## Purpose [CORE]` | the orienting line is in the live file only; a summary holds a gist, not the substring | `sed -n '/^## Purpose \[CORE\]/,+3p' ARCHITECTURE.md` → the quote must be a substring of the live section |

**Gate:** the architect may not proceed to design until it **holds both orienting lines** — read live
by CC, substring-matched. `ARCHITECTURE.md` was amended **again** this window (a governance-roster
reconciliation), so the live lines, not any remembered ones, are the frame. **Then, before design, the
operator-context beat fires (§13d) — FULL** (the supplement is generated empty; there is nothing to
narrow against).

**P7, P11 and P12 are unusually load-bearing this window.** The residual's headline is that a *green
report was published without the predicate that produced it* — several separate instances, including
inside the checker built to catch exactly that class. P7 measures whether silent exit codes are being
read as verdicts; P11 measures whether one rule's implementation still covers fewer surfaces than its
spec; P12 measures what the clean summary line actually covers. **Run all three before accepting any
claim in the residual that the quality surface is sound.**

## Teeth probes (state fidelity — same contract; **answers deliberately withheld, §5**)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via (run in **TARGET**) |
|---|---|---|---|---|
| P2 | **[RE-BOUND — `ai-council` has no `scripts/audit.py`/`ALL_CHECKS` and no `validate_doc_claims`; the claim-checker does not cover this claim either.]** How many hook `id`s does the pre-commit config declare, what is the **id of the last one** in file order, and do **both** doc rosters — `ARCHITECTURE.md`'s prose roster **and** `CLAUDE.md` §9's — list that **same set**, including the total each states? | the pre-commit config ∩ `ARCHITECTURE.md` (hook-roster prose) ∩ `CLAUDE.md` §9 | the roster drifts every time a gate lands, and **two** doc surfaces must both stay reconciled — the checker's rule 3 covers *mention*, not set-equality or the stated total, so a divergence stays invisible until someone reads all three | **TARGET:** `grep -n 'hook' ARCHITECTURE.md` and `grep -n 'id:' CLAUDE.md` for the doc side; for the config side run grep -c and grep -n on the `^  - id:` lines of the repo-root pre-commit config (path deliberately un-backticked — see the dotfile note below the table), then compare the three by hand |
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time state; any new commit or push moves it, and this window closed with a rapid series of merge-and-push arcs whose live position is exactly the question | **TARGET:** `git rev-parse --short HEAD` then `git status -sb` then `git branch -v` |
| P4 | **[RE-BOUND — `ai-council` has no `validate_git_backlog.py`.]** Which **open** `#id`s in `BACKLOG.md` already have a **closing merge** on `main`'s first-parent spine (i.e. are drifted-closed but still listed), and what is each such merge's **short sha**? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time by intersecting two live sources; the shas are high-entropy and documented nowhere in this bundle. This window both **closed** and **filed** double-digit id batches, so the intersection has genuinely moved in both directions | **TARGET:** `grep -o '\[#[0-9]\+\]' BACKLOG.md \| sort -u` then `git log --first-parent --oneline main` — intersect the two by hand |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely — and ARCHITECTURE took another merge of edits this window (the governing-ADR roster reconciliation), so the relation is among the freshest facts in the repo | **TARGET:** `git log -1 --format=%cs -- ARCHITECTURE.md` vs `grep '^last_reviewed:' ARCHITECTURE.md` |
| P6 | **[RE-BOUND — `ai-council` has no `doc-counts.md`/`validate_doc_claims`, so there is no doc-claim to compare against; this probe is the LIVE count alone.]** How many tests does the suite **collect right now**? | live pytest over `tests/` | the collected count drifts on any test change, and this window landed new harness tests; the integer appears nowhere in this bundle | **TARGET:** `python -m pytest --collect-only -q \| tail -3` (read the `N tests collected` line) |
| P7 | **[RE-BOUND — `ai-council` has no `audit.py ship-gate` and no disposition register, so there is no single GREEN/RED headline verdict. THIS window filed a ticket asserting these gates report silence rather than a verdict — so read the codes, and read what each one actually printed.]** Run the four **gating** read-only validators and report **each one's exit code** and any output: freshness, docs-registry, sealed-keys, audit-casing. Which (if any) are non-zero, and how many produced **no stdout at all**? | `scripts/canonical_freshness_gate.py` + `scripts/validate_docs_registry.py` + `scripts/validate_sealed_keys.py` + `scripts/validate_audit_casing.py` | **THIS is the §1 headline substitute** — each verdict is computed at answer-time over live tree state; a new edit can flip any of them; none of the values are in this bundle. The residual's central claim is that a silent exit 0 was being read as a positive verdict when it is only an absence of output — so the **stdout-vs-exit-code split is itself part of the answer**, not incidental | **TARGET:** `python scripts/canonical_freshness_gate.py` then `python scripts/validate_docs_registry.py` then `python scripts/validate_sealed_keys.py` then `python scripts/validate_audit_casing.py` — **read each one's exit status explicitly** (in bash, echo the exit variable after each) **and note separately whether it printed anything**. Re-derive; do **not** trust the residual's prose |
| P8 | How many `ADR-NN-*.md` files does the decision registry hold **right now**, what is the **number + slug of the highest-numbered one**, and do **both** `docs/decisions/README.md` **and** `ARCHITECTURE.md`'s governing-ADR roster list that same ADR? | `docs/decisions/` ∩ `docs/decisions/README.md` ∩ `ARCHITECTURE.md` | the registry grows whenever a Council verdict is authored into an ADR — the governance surface this repo exists to produce. **The three-surface form is deliberate:** a newly-landed ADR reached some of these surfaces but not all of them this window, and the checker did not see it (that is P11's defect). The count, the tail slug, and whether **each** index has kept pace are live-only and absent from this bundle | **TARGET:** `ls docs/decisions/ADR-*.md \| wc -l` then `ls docs/decisions/ADR-*.md \| tail -1` then `grep -c 'ADR-' docs/decisions/README.md` then `grep -n 'ADR-01\|Governing' ARCHITECTURE.md` — compare all three by hand |
| P9 | What does `validate_backlog` report **right now** for the number of **themes**, **stories**, **tasks**, and **warnings** — and what does `BACKLOG.md`'s grooming log name as the **next free local id**? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | all four integers drift on any BACKLOG edit — and this window moved every one of them (a double-digit filing batch plus closures plus a renumber landed); the next-free pointer moved too; none of it is in this bundle | **TARGET:** `python scripts/validate_backlog.py` (read the `OK (N themes, N stories, N tasks, N warning(s))` summary line) then `grep -n 'Next free local id' BACKLOG.md \| tail -1` |
| P10 | **BACKLOG grooming (operator ruling 2026-07-17).** For **every OPEN item** in `BACKLOG.md`, is each still **live** (actively in-progress), **dead** (superseded / obsoleted / already-shipped — a grooming close per hub ADR-65), or **awaiting-ruling** (blocked on an operator / Council decision)? The successor grooms the **whole open set** at boot — no open `#id` may pass unreconciled. | `BACKLOG.md` ∩ live git | the live / dead / awaiting-ruling status of each open item is an at-boot judgment over current git ∩ `BACKLOG.md`; a summary holds a stale snapshot and cannot tell a still-live item from one already shipped or superseded. **The open set moved substantially in both directions this window** (a filing batch plus a closure batch), so the grooming denominator itself has moved — and several new items are explicitly blocked on each other | **TARGET:** `python scripts/validate_backlog.py` then `git log --first-parent --oneline main` to cross-check each open `#id` against its closing merge (this subsumes P4's mechanical half — P10 is the judgment layer over it) |
| P11 | **[RE-BOUND — last window's registry-completeness gap is CLOSED; this is the defect that replaced it, and it is the window's headline.]** Rule 4 is specified as **set-equality across four doc surfaces**. How many surfaces does the implementation's `_adr_roster_docs` actually return, **which** ones, and is the comparison **one-directional or both**? Then: does the checker's own report or its KNOWN-LIMITATIONS output **disclose** that narrowing anywhere? | `scripts/validate_claims.py` (`_adr_roster_docs` and its caller) ∩ the rule-4 spec line for ticket #97 in `BACKLOG.md` ∩ the checker's report header | the spec count is a live doc fact, the returned tuple is a live code fact, and **the gap between them is the defect** — one that a clean summary line actively conceals, because the rule reports *pass* while reading a fraction of what it claims. This is the "green without its predicate" class turned on the checker itself; a summary that read "rule 4 passes" never asked *passes against what* | **TARGET:** `grep -n '_adr_roster_docs' scripts/validate_claims.py` then read that function and its call site in full, then `grep -n 'KNOWN LIMITATIONS' scripts/validate_claims.py` and read the block it heads, then `grep -n '\[#97\]\|\[#125\]' BACKLOG.md` — compute the surface-set difference by hand |
| P12 | **[The checker's live coverage picture — and the reason its clean summary line must not be read alone.]** Run the report-only checker: what does the final `SUMMARY:` line report for **findings**, **rules covered**, **anchor-missing**, **skipped**, and **errors** — and what does the coverage block report as **implemented vs stubbed vs total**? How many rules are **held stubs** (registered but deliberately unbuilt), and does a reader of the summary line **alone** learn that? | `scripts/validate_claims.py` run over the live tree | the finding count moves on **every JOURNAL prepend**, and the skipped/total split is the whole question: a low finding count across a small covered set is not the same claim as a low count across the full set, and only the coverage block distinguishes them. **Held stubs are registered precisely so the report keeps saying "not checked"** — verifying that it still does is the point. None of these integers are in this bundle | **TARGET:** `python scripts/validate_claims.py` — read the final `SUMMARY:` line, the coverage block, **and** the per-rule SKIP lines above it. **Report-only and non-blocking by design — a non-zero finding count is NOT a failure**, it is the measurement |
| P13 | **[RE-BOUND — the reservation fence MOVED this window: reservations were discharged and a different id is now fenced. Re-derive the live set; the remembered one is wrong.]** Which ids does `BACKLOG.md`'s **Id-reservations note** hold reserved **right now**, which previously-reserved ids has it **discharged** (and are they now in use or free), and how many bare dangling references does the file still carry into the hub id space? | `BACKLOG.md` (Id-reservations note + task lines) | the reservation set is the **precondition of any new filing** — assigning a fenced id silently captures someone else's dangling reference, which has already happened repeatedly here. Both the reserved set and the discharged set changed this window, so a remembered set is actively dangerous; both are live text facts | **TARGET:** `grep -n 'Id reservations' BACKLOG.md` (read the note in full) then `grep -c 'refs #96' BACKLOG.md` then `grep -n '\[#84\]\|\[#85\]\|#107' BACKLOG.md` |
| P14 | **[The allowed-set gap — RECORDED as a dated note, so the live question is whether the snapshot still holds.]** `ARCHITECTURE.md`'s Layer-edges allowed set is labelled **TARGET, not current state**, with a dated current-state note recording `cli.py`'s real edge surface. Re-derive that surface **live**: how many real `src/ai_council/` inter-module imports does `cli.py` carry now (module-level and function-level; TYPE_CHECKING-only excluded), how many fall **inside** the allowed set, and does the **recorded note still match**? Has the re-derivation trigger — the `cli.run()` refactor ticket — **landed yet**? | `src/ai_council/cli.py` ∩ `ARCHITECTURE.md` "Layer edges" + its dated current-state note ∩ the refactor task line in `BACKLOG.md` | the doc carries a **dated snapshot of a live quantity** — the exact shape that goes stale silently. Note that a raw import grep and the note's counting rule do **not** agree by construction (the rule excludes TYPE_CHECKING-only edges), so the comparison requires reading the rule, not just counting lines. Answerable only by intersecting source, doc, and backlog at answer-time | **TARGET:** `grep -n 'from ai_council' src/ai_council/cli.py` for the source side; `sed -n '/^Layer edges/,+40p' ARCHITECTURE.md` for the doc side (read the dated current-state note **and** the TARGET label **and** its counting rule); then `grep -n '\[#92\]' BACKLOG.md` for the trigger's status — compare all three by hand |
| P15 | **[RE-BOUND — the uncommitted-local-config mechanism was REPLACED by real refs this window; verify the replacement actually holds.]** Do the `archive/cited-*` tags exist **locally**, do they exist **on the remote**, do the two sides agree, and does each still resolve to a reachable **commit** object? Is the local `gc.auto` override now **absent** (if it is still set, its value is part of the answer)? | live git refs ∩ `.git/config` (local) ∩ the object store | this replaced the one load-bearing fact that was **not in the repo** — a local config value protecting objects past git's prune horizon. The whole point of the fix is that the protection is now **verifiable from a clone**, so verifying it is not ceremony: if the tags are local-only, or the override silently persists as the real protection, the fix is not the fix it is recorded as | **TARGET:** `git tag -l 'archive/*'` then `git ls-remote --tags origin` then `git cat-file -t` on each tag's target, then `git config --get gc.auto` (**report whether it is set at all** — an unset value exits non-zero, which is a possible correct shape, not an error) |
| P16 | Does the tag `spike/md-parser-evidence` exist **locally**, does it exist **on the remote**, and do the two point at the **same commit**? | live git ∩ `origin` | this tag anchors the evidence base the still-open extractor design forks depend on; a branch push does **not** carry tags, so local-remote divergence is a live possibility only git can answer, and several bundles have now flagged this exposure — whether it stayed resolved is answerable only live | **TARGET:** `git tag -l 'spike/*'` then `git ls-remote --tags origin` — compare the sha each side reports |

> **Dotfile note (P2) — a live limitation of the hub validator, not sloppiness.** The repo-root
> pre-commit config file is written **un-backticked** in P2's command cell on purpose. The hub's
> `scripts/verify_handoff_probes.py` tokenizer (`file_tokens`) **strips a leading dot** from the final
> path segment, so a backticked repo-root dotfile is looked up without its dot and resolves nowhere —
> the probe is then FAILed as a missing target even though the file plainly exists. (Dot-*directories*
> are unaffected; it is specifically the last segment.) **Consequence: no probe in any bundle — hub or
> cross-repo — can currently bind to a repo-root dotfile.** That is a hub tooling defect, filed
> upstream as hub `[#421]`; it is deliberately **not** patched from inside this handoff, because hub
> infra changes are exception-with-ruling (core-invariant #6). The probe's teeth are unaffected — the
> comparison is still live-only and answer-free.

## Gate procedure (CC)

1. **Confirm the run-in root before every command** (the table at the top). A probe run in the wrong
   repo is a **FAIL**, not a pass — the hub and the target have same-named files with different
   contents (`BACKLOG.md`, `ARCHITECTURE.md`, `VISION.md`, `CLAUDE.md`, `JOURNAL.md`,
   `scripts/validate_backlog.py` all exist in both). This is the single most likely failure mode of a
   cross-repo bundle.
2. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d) — FULL** (the supplement is
   generated empty; there is nothing to narrow against). Then run P2–P16, each against **live state
   now**.
3. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
4. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
5. Probes P2–P16 are *designed to move* between generation and check-time — that is the point. **Answer
   values are deliberately absent (§5)**: the pass criterion is **"answered from the live source,"**
   never "matches a remembered number."
   **Order matters for four of them:** **P7 before accepting any "the gates are green" claim** (it is
   the headline substitute, and reading its stdout-vs-exit-code split is the window's whole lesson);
   **P11 before any checker work** (it supplies the live shape of the rule-4 narrowing the next arc
   repairs); **P12 before reading any finding count as coverage** (the skipped/total split is the real
   denominator); **P14 before any allowed-set or codemap edit** (the doc carries a dated snapshot that
   may already be stale, and its counting rule must be read, not assumed).
   **P10 grooms the whole open BACKLOG at boot** — the operator-ruled boot obligation, not optional,
   and the open set moved in both directions this window.
6. **Bundle-shape / supplement fill-state is NOT a probe here** (the stock row pointed at the hub
   bundle dir, which is unresolvable from the target root). This bundle carries `HANDOFF_BOOT` +
   `RESIDUAL` + `PROBES` + `SUPPLEMENT` + `PASTE_THIS` and **no per-bundle README**
   (HANDOFF_PROCESS §13); the supplement is **generated EMPTY**, so the assembler folds nothing and the
   §13(d) beat fires **FULL**. Confirm by looking at the bundle directory in the hub — it is CC-side
   bookkeeping, not target state.
