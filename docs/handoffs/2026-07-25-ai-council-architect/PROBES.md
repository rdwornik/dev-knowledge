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
> group-memberships, or orienting lines are stated. That withholding IS the teeth. The pass criterion
> is **"answered from the live source at check-time,"** never "matches a remembered number." Generation
> hints (if any) live in the JOURNAL generation-entry, which the browser never sees — never here. The
> validator `scripts/verify_handoff_probes.py` FAILs any probe row that prints an answer hint.
>
> **Branch note.** This bundle was generated on branch `docs/handoff-2026-07-25-ai-council` **in the
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

**The generator's default probe set was hub-bound and has been re-authored.** `ai-council` carries
**no** `scripts/audit.py`, **no** `validate_git_backlog.py`, **no** `ecosystem/doc-counts.md`, and
**no** `ecosystem/disposition-register.yaml` — the stock P2/P4/P6/P7 rows would have FAILed
`anchor-missing` on all four. Each was re-bound to a **verified-live** `ai-council` surface (every
anchor below confirmed present at generation time by running its command in the target). Where the hub
has an organ `ai-council` genuinely lacks, the probe says so rather than inventing an equivalent.

**What changed since the last cross-repo bundle:** the "no automated doc-vs-reality organ" gap is now
**partially closed** — `scripts/validate_claims.py` landed this window as a read-only, **non-blocking**
report-only checker (a fifth validator surface, deliberately **not** a gate). Two probes are new
because of it: **P11** (registry completeness — the window's headline defect) and **P12** (its live
finding set). P2, which existed to hand-build the missing doc-vs-reality tooth, is **kept** — the
checker does not yet cover the hook-roster claim.

**READ-ONLY ON THE TARGET (ADR-36/41 — hard).** Every command below is read-only. Do **not** run
`pre-commit run --all-files` in `ai-council` as a probe: its `normalize-headers` / `toc-generate`
hooks are **formatters that rewrite files**, which would violate the read-only contract on a
cross-repo target. The P7 sweep calls the read-only validators directly instead. `scripts/check.ps1`
is likewise **not** a probe — it is the full pytest+mypy+ruff trio, far past read-only-cheap; P6 and
P12 call the two pieces a probe actually needs.

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS
> region is empty → the assembler folds nothing → the incoming §13(d) operator-context beat fires
> **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

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
by CC, substring-matched. `ARCHITECTURE.md` was amended **again** this window (the R1 allowed-set
correction), so the live lines, not any remembered ones, are the frame. **Then, before design, the
operator-context beat fires (§13d) — FULL** (the supplement is empty; there is nothing to narrow
against).

## Teeth probes (state fidelity — same contract; **answers deliberately withheld, §5**)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via (run in **TARGET**) |
|---|---|---|---|---|
| P2 | **[RE-BOUND — `ai-council` has no `scripts/audit.py`/`ALL_CHECKS` and no `validate_doc_claims`; the new checker does not cover this claim either.]** How many hook `id`s does the pre-commit config declare, what is the **id of the last one** in file order, and do **both** doc rosters — `ARCHITECTURE.md`'s prose roster **and** `CLAUDE.md` §9's — list that **same set**, including the total each states? | the pre-commit config ∩ `ARCHITECTURE.md` (hook-roster prose) ∩ `CLAUDE.md` §9 | the roster drifts every time a gate lands, and **two** doc surfaces must both stay reconciled — the checker's rule 3 covers *mention*, not set-equality or the stated total, so a divergence stays invisible until someone reads all three | **TARGET:** `grep -n 'hook' ARCHITECTURE.md` and `grep -n 'id:' CLAUDE.md` for the doc side; for the config side run grep -c and grep -n on the `^  - id:` lines of the repo-root pre-commit config (path deliberately un-backticked — see the dotfile note below the table), then compare the three by hand |
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time state; any new commit or push moves it, and several entries this window landed commit-and-STOP branches whose merge/push status is exactly the live question | **TARGET:** `git rev-parse --short HEAD` then `git status -sb` then `git branch -v` |
| P4 | **[RE-BOUND — `ai-council` has no `validate_git_backlog.py`.]** Which **open** `#id`s in `BACKLOG.md` already have a **closing merge** on `main`'s first-parent spine (i.e. are drifted-closed but still listed), and what is each such merge's **short sha**? | live git ∩ `BACKLOG.md` | the drifted set is computed at answer-time by intersecting two live sources; the shas are high-entropy and documented nowhere in this bundle. This window filed a double-digit id batch, so the intersection has genuinely moved | **TARGET:** `grep -o '\[#[0-9]\+\]' BACKLOG.md \| sort -u` then `git log --first-parent --oneline main` — intersect the two by hand |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely — and ARCHITECTURE took another merge of edits this window (the R1 correction), so the relation is among the freshest facts in the repo | **TARGET:** `git log -1 --format=%cs -- ARCHITECTURE.md` vs `grep '^last_reviewed:' ARCHITECTURE.md` |
| P6 | **[RE-BOUND — `ai-council` has no `doc-counts.md`/`validate_doc_claims`, so there is no doc-claim to compare against; this probe is the LIVE count alone.]** How many tests does the suite **collect right now**? | live pytest over `tests/` | the collected count drifts on any test change, and this window added a large new test module; the integer appears nowhere in this bundle | **TARGET:** `python -m pytest --collect-only -q \| tail -3` (read the `N tests collected` line) |
| P7 | **[RE-BOUND — `ai-council` has no `audit.py ship-gate` and no disposition register, so there is no single GREEN/RED headline verdict.]** Run the four **gating** read-only validators and report **each one's exit code** and any output: freshness, docs-registry, sealed-keys, audit-casing. Which (if any) are non-zero? | `scripts/canonical_freshness_gate.py` + `scripts/validate_docs_registry.py` + `scripts/validate_sealed_keys.py` + `scripts/validate_audit_casing.py` | **THIS is the §1 headline substitute** — each verdict is computed at answer-time over live tree state; a new edit can flip any of them; none of the values are in this bundle. Note several pass **silently** (exit 0, no stdout) — the exit code *is* the signal, so it must be read explicitly | **TARGET:** `python scripts/canonical_freshness_gate.py` then `python scripts/validate_docs_registry.py` then `python scripts/validate_sealed_keys.py` then `python scripts/validate_audit_casing.py` — **read each one's exit status explicitly** (in bash, echo the exit variable after each; several print nothing on success, so the status is the only signal). Re-derive; do **not** trust the residual's prose |
| P8 | How many `ADR-NN-*.md` files does the decision registry hold **right now**, what is the **number + slug of the highest-numbered one**, and does its `README.md` index list that same ADR? | `docs/decisions/` ∩ `docs/decisions/README.md` | the registry grows whenever a Council verdict is authored into an ADR — the governance surface this repo exists to produce; the count, the tail slug, and whether the index has kept pace are all live-only and absent from this bundle | **TARGET:** `ls docs/decisions/ADR-*.md \| wc -l` then `ls docs/decisions/ADR-*.md \| tail -1` then `grep -c 'ADR-' docs/decisions/README.md` |
| P9 | What does `validate_backlog` report **right now** for the number of **themes**, **stories**, **tasks**, and **warnings** — and what does `BACKLOG.md`'s grooming log name as the **next free local id**? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | all four integers drift on any BACKLOG edit — and this window moved every one of them (a double-digit task delta plus a reconciliation landed); the next-free pointer moved too; none of it is in this bundle | **TARGET:** `python scripts/validate_backlog.py` (read the `OK (N themes, N stories, N tasks, N warning(s))` summary line) then `grep -n 'Next free local id' BACKLOG.md \| tail -1` |
| P10 | **BACKLOG grooming (operator ruling 2026-07-17).** For **every OPEN item** in `BACKLOG.md`, is each still **live** (actively in-progress), **dead** (superseded / obsoleted / already-shipped — a grooming close per hub ADR-65), or **awaiting-ruling** (blocked on an operator / Council decision)? The successor grooms the **whole open set** at boot — no open `#id` may pass unreconciled. | `BACKLOG.md` ∩ live git | the live / dead / awaiting-ruling status of each open item is an at-boot judgment over current git ∩ `BACKLOG.md`; a summary holds a stale snapshot and cannot tell a still-live item from one already shipped or superseded. **The open set grew substantially this window** (a filing batch plus rider edits), so the grooming denominator itself has moved — and several of the new items are explicitly blocked on each other | **TARGET:** `python scripts/validate_backlog.py` then `git log --first-parent --oneline main` to cross-check each open `#id` against its closing merge (this subsumes P4's mechanical half — P10 is the judgment layer over it) |
| P11 | **[NEW — the window's headline defect, and the number the next build arc starts from.]** How many legs does the checker's `RULES` registry actually contain right now; of the fourteen rules `BACKLOG.md` `#97` specifies, **which rule ids have no row in the registry at all** (neither an implemented leg nor a Unit-2 stub); and does the checker's own **KNOWN LIMITATIONS** output disclose those absences? | `scripts/validate_claims.py` (`RULES`) ∩ the #97 task line in `BACKLOG.md` ∩ the checker's report header | the registry is a live code fact; the spec count is a live doc fact; the **set difference between them is the defect** — and it is invisible to the checker's own test suite, because the registry test is parametrized **over the registry** and so has no external denominator. A summary that read "4 built + 7 stubs" never sums it against fourteen — which is precisely how the gap survived a green suite | **TARGET:** `grep -n 'rule_\|_unit2_stub(' scripts/validate_claims.py` (read the `RULES` list in full) then `grep -n 'KNOWN LIMITATIONS' scripts/validate_claims.py` and read the block it heads, then `grep -n '\[#97\]' BACKLOG.md` — compute the set difference by hand |
| P12 | **[NEW — the checker's live finding set; the input to the `#104` zero-findings gate.]** Run the report-only checker: **how many findings** does it emit **right now**, **across which rule ids**, and how many legs report `skipped(Unit2)`? Then: how many of those findings are the **self-replicating** class (a rule-8 dangling-SHA finding whose citation is itself a JOURNAL entry about dangling SHAs)? | `scripts/validate_claims.py` run over the live tree | the count moves on **every JOURNAL prepend** — the self-replication `#105` predicts is a live, growing quantity, and the line numbers in each finding shift as the newest-first file grows. **`#104`'s done-when is a zero-findings gate**, so this number is the gate's live distance-to-passable; none of it is in this bundle | **TARGET:** `python scripts/validate_claims.py` — read the final `SUMMARY:` line (pass / FINDINGS across N rules / anchor-missing / skipped / errors), then read the per-finding lines above it. **Report-only and non-blocking by design — a non-zero finding count is NOT a failure**, it is the measurement |
| P13 | **[The reservation fence the renumber arc depends on — extended again this window.]** Which ids does `BACKLOG.md`'s **Id-reservations note** hold reserved **right now**, how many `refs #96` occurrences does the file still carry, and are the two carried hub-id tasks still sitting at their hub ids? | `BACKLOG.md` (Id-reservations note + task lines) | the reservation set and the dangling-ref count are the **preconditions of the pending renumber arc** — if either has moved, the arc's plan is stale. A **third** hub/local collision was caught and fenced this window, so the reserved set is not the one a summary remembers; both are live text facts | **TARGET:** `grep -n 'Id reservations' BACKLOG.md` (read the note in full) then `grep -c 'refs #96' BACKLOG.md` then `grep -n '\[#110\]\|\[#128\]' BACKLOG.md` |
| P14 | **[The allowed-set gap — now RECORDED as a dated note, so the live question changed.]** `ARCHITECTURE.md`'s Layer-edges allowed set is now labelled **TARGET, not current state**, with a dated current-state note recording `cli.py`'s real edge surface. Re-derive that surface **live**: how many real `src/ai_council/` inter-module imports does `cli.py` carry now (module-level and function-level; TYPE_CHECKING-only excluded), and does the **recorded note still match**? Has the re-derivation trigger — `#92`'s `cli.run()` refactor — **landed yet**? | `src/ai_council/cli.py` ∩ `ARCHITECTURE.md` "Layer edges" + its dated current-state note ∩ the #92 task line in `BACKLOG.md` | the doc now carries a **dated snapshot** of a live quantity — the exact shape that goes stale silently. The R1 ruling deliberately did **not** widen the set; it recorded the gap and named `#92` as the re-derivation trigger, so "has the trigger fired, and does the snapshot still hold" is answerable only by intersecting source, doc, and backlog at answer-time | **TARGET:** `grep -n 'from ai_council' src/ai_council/cli.py` for the source side; `sed -n '/^Layer edges/,+40p' ARCHITECTURE.md` for the doc side (read the dated current-state note **and** the TARGET label); then `grep -n '\[#92\]' BACKLOG.md` for the trigger's status — compare all three by hand, noting which listed edge is still the **open case** |
| P15 | **[NEW — an uncommitted local mechanism holding unreachable objects alive.]** What is this checkout's **local** `gc.auto` setting, and do **all four** of the dangling commit objects `#112` enumerates still resolve as commit objects right now? | `.git/config` (local, **uncommitted by nature**) ∩ live git object store | this is the one load-bearing fact in the repo that **is not in the repo** — a local config value no clone, summary, or file read can carry, protecting objects that are past git's default prune horizon. If it has reverted, the objects can vanish at any `gc --auto`; `#112`'s done-when includes **restoring** it, so its current value is also a debt marker | **TARGET:** `git config --get gc.auto` then `grep -n '\[#112\]' BACKLOG.md` to read the four shas it enumerates, then `git cat-file -t <sha>` for each one |
| P16 | Does the tag `spike/md-parser-evidence` exist **locally**, does it exist **on the remote**, and do the two point at the **same commit**? | live git ∩ `origin` | this tag anchors the evidence base the still-open extractor design forks depend on; a branch push does **not** carry tags, so local-remote divergence is a live possibility only git can answer, and the last two bundles both flagged this exposure — whether it was since resolved is answerable only live | **TARGET:** `git tag -l 'spike/*'` then `git ls-remote --tags origin` — compare the sha each side reports |

> **Dotfile note (P2) — a live limitation of the hub validator, not sloppiness.** The repo-root
> pre-commit config file is written **un-backticked** in P2's command cell on purpose. The hub's
> `scripts/verify_handoff_probes.py` tokenizer (`file_tokens`) **strips a leading dot** from any path it
> extracts, so a backticked dotfile name is looked up without its dot, which resolves nowhere — the
> probe is then FAILed as a missing target even though the file plainly exists.
> **Consequence: no probe in any bundle — hub or cross-repo — can currently bind to a dotfile.** That is
> a hub tooling defect worth filing (dotfiles are exactly where config gates live); it is deliberately
> **not** patched from inside this handoff, because hub infra changes are exception-with-ruling
> (core-invariant #6). The probe's teeth are unaffected — the comparison is still live-only and
> answer-free.

## Gate procedure (CC)

1. **Confirm the run-in root before every command** (the table at the top). A probe run in the wrong
   repo is a **FAIL**, not a pass — the hub and the target have same-named files with different
   contents (`BACKLOG.md`, `ARCHITECTURE.md`, `VISION.md`, `CLAUDE.md`, `scripts/validate_backlog.py`
   all exist in both). This is the single most likely failure mode of a cross-repo bundle.
2. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d) — FULL** (the supplement is empty).
   Then run P2–P16, each against **live state now**.
3. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
4. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
5. Probes P2–P16 are *designed to move* between generation and check-time — that is the point. **Answer
   values are deliberately absent (§5)**: the pass criterion is **"answered from the live source,"**
   never "matches a remembered number."
   **Order matters for three of them:** **P11 before any `#97` build work** (it supplies the registry
   gap the next arc repairs, and the reason the green suite did not catch it); **P12 before touching
   `#104`** (its finding count is that gate's live distance-to-passable, and it grows on its own);
   **P14 before any allowed-set or codemap edit** (the doc now carries a dated snapshot that may
   already be stale, and `#92` is its named re-derivation trigger).
   **P7 remains the headline substitute** (four exit codes, read explicitly — several gates pass
   silently, so "no output" must not be scored as "no drift"). **P12 is report-only: a non-zero
   finding count is the measurement, not a failure.** **P10 grooms the whole open BACKLOG at boot** —
   the operator-ruled boot obligation, not optional, and the open set grew this window.
6. **Bundle-shape / supplement fill-state is NOT a probe here** (the stock row pointed at the hub
   bundle dir, which is unresolvable from the target root). This bundle carries `HANDOFF_BOOT` +
   `RESIDUAL` + `PROBES` + `SUPPLEMENT` + `PASTE_THIS` and **no per-bundle README**
   (HANDOFF_PROCESS §13); the supplement is **generated EMPTY**, so the assembler folds nothing and
   the §13(d) beat fires **FULL**. Confirm by looking at the bundle directory in the hub — it is
   CC-side bookkeeping, not target state.
