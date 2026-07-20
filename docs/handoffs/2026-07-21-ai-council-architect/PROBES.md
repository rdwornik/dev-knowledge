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
> manifest **withholds every answer value** by construction: no counts, SHAs, dates, verdicts, exit
> codes, group-memberships, or orienting lines are stated. That withholding IS the teeth. The pass
> criterion is **"answered from the live source at check-time,"** never "matches a remembered number."
> Generation hints live in the JOURNAL generation-entry, which the browser never sees — never here. The
> validator `scripts/verify_handoff_probes.py` FAILs any probe row that prints an `expected:` value.
>
> **Branch note.** This bundle was generated on hub branch `docs/ai-council-architect-handoff-0721`.
> That names only *which* branch hosts the bundle — **re-derive the TARGET's HEAD / tree / branch /
> ahead-behind live (P3); do not trust this line.**
>
> > **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

## ⚠ CROSS-REPO BUNDLE — read this before running anything

This is a **cross-repo** handoff (ADR-36/41): the **target** is `ai-council`; the **bundle** is
generated and stored in the `.dev-knowledge` hub. The two live in different working directories, so
every probe below names its **run-in root** explicitly:

| Run-in root | Path | Which probes |
|---|---|---|
| **TARGET** (`ai-council`) | `Dev/ai-council` | **all of them — P1a, P1b, P2–P12** |
| **HUB** (`.dev-knowledge`) | `Dev/.dev-knowledge` | none (the hub only *hosts* this bundle) |

Every probe binds to the target and resolves from the target root — the bundle declares
`| **Target repo** | `ai-council` |` in `HANDOFF_BOOT.md`, which is what makes the hub's
`check_handoff_probes` resolve foreign paths against `ai-council` instead of against itself (and so
avoids both false FAILs and false PASSes from basename collisions like `JOURNAL.md`).

**The generator's default probe set was hub-bound and has been re-authored.** `ai-council` carries
**no** `scripts/audit.py` / `ALL_CHECKS`, **no** `validate_git_backlog.py`, **no**
`validate_doc_claims.py`, **no** `ecosystem/doc-counts.md`, and **no**
`ecosystem/disposition-register.yaml` — the stock P2/P4/P6/P7/P9 rows would have FAILed
`anchor-missing` on every one. Each was re-bound to a **verified-live** `ai-council` surface (anchors
confirmed at generation time by running each command in the target). Where the hub has an organ
`ai-council` genuinely lacks, the probe says so rather than inventing an equivalent. **P11 and P12 are
new in this bundle** — they bind the two live findings that are §1's headline.

**READ-ONLY ON THE TARGET (ADR-36/41 — hard).** Every command below is read-only. Do **not** run
`pre-commit run --all-files` in `ai-council` as a probe: its header-normalisation hooks are
**formatters that rewrite files**, which would violate the read-only contract on a cross-repo target.
P7 calls the read-only validators directly instead. **P11 is diagnostic only — do not `git
cherry-pick`, `git branch`, or otherwise mutate the target to "rescue" the object; surfacing it is the
handoff's job, recovering it is the target session's call.**

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
by CC, substring-matched. **Then, before design, the operator-context beat fires (§13d):** the browser
asks the operator for **off-repo** context.
This bundle's supplement is **generated EMPTY**, so the beat fires **FULL** — *"what off-repo context: intent, priorities, findings not in the repo, changed decisions?"* — not a narrowed "anything changed since?". (If the operator runs `supplement filled`, its ANSWERS fold in and the beat narrows.)

## Teeth probes (state fidelity — same contract; **answers deliberately withheld, §5**)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via (run in **TARGET**) |
|---|---|---|---|---|
| P2 | **[RE-BOUND — `ai-council` has no `scripts/audit.py`/`ALL_CHECKS` and no `validate_doc_claims`; this row restores the missing doc-vs-reality tooth by hand.]** How many hook `id`s does the pre-commit config declare, what is the **id of the last one** in file order, and does `ARCHITECTURE.md`'s **pre-commit roster** prose list that **same set** — or has the doc drifted behind the config? | `ARCHITECTURE.md` (pre-commit roster prose) ∩ the repo-root pre-commit config | the roster drifts every time a gate lands, and `ai-council` has **no automated doc-claim check** to catch the doc falling behind — so the mismatch is invisible until someone reads both; neither the count, the tail id, nor the verdict is in this bundle | `grep -n -i 'pre-commit' ARCHITECTURE.md` for the doc side; for the config side run a `grep -c` and a grep-tail over the `^  - id:` lines of the repo-root pre-commit config (path deliberately **un-backticked** — see the dotfile note below), then compare the two sets by hand |
| P3 | What is the current **short HEAD sha**, is the working tree clean, which **branch** is checked out, and how many commits is `main` **ahead of / behind** `origin/main`? | live git | the summary holds the generation-time state; any new commit or push moves it | `git rev-parse --short HEAD` then `git status -sb` then `git branch --show-current` |
| P4 | **[RE-BOUND — `ai-council` has no `validate_git_backlog.py`.]** Which **open** `#id`s in `BACKLOG.md` appear in a merge subject on `main`'s first-parent spine, and for each: is that merge an actual **closure**, or a merge that deliberately did **not** close the ticket? | live git ∩ `BACKLOG.md` | the set is computed at answer-time by intersecting two live sources, and the closure/non-closure judgment cannot be read off either one alone | `grep -o '\[#[0-9]\+\]' BACKLOG.md \| sort -u` then `git log --first-parent --oneline main` — intersect by hand. **A bracketed id in a merge subject does NOT imply closure**: this window merged one ticket *without* closing it, and at least one hub-range id appears on the spine. Judge each, don't count them |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` stamp **on/after or before** its last git-commit touch — and what are the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a *relation* over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs `grep '^last_reviewed:' ARCHITECTURE.md` |
| P6 | **[RE-BOUND — `ai-council` has no `doc-counts.md`/`validate_doc_claims`, so there is no doc-claim to compare against; this probe is the LIVE count alone.]** How many tests does the suite **collect right now**? | live pytest over `tests/` | the collected count drifts on any test change — and this window added a large block of them; the integer appears nowhere in this bundle | `python -m pytest --collect-only -q \| tail -3` (read the `N tests collected` line) |
| P7 | **[RE-BOUND — `ai-council` has no `audit.py ship-gate` and no disposition register, so there is no single GREEN/RED headline verdict.]** Run the four **read-only** repo validators and report **each one's exit code** and any output: freshness, docs-registry, sealed-keys, audit-casing. Which (if any) are non-zero? | `scripts/canonical_freshness_gate.py` + `scripts/validate_docs_registry.py` + `scripts/validate_sealed_keys.py` + `scripts/validate_audit_casing.py` | **THIS is the §1 headline substitute** — each verdict is computed at answer-time over live tree state; a new edit can flip any of them; none of the values are in this bundle. Several pass **silently** (exit 0, no stdout) — the exit code *is* the signal, so it must be read explicitly | `python scripts/canonical_freshness_gate.py` then `python scripts/validate_docs_registry.py` then `python scripts/validate_sealed_keys.py` then `python scripts/validate_audit_casing.py` — **read each one's exit status explicitly** (in bash, echo the exit variable after each; several print nothing on success, so the status is the only signal). Re-derive; do **not** trust the residual's prose |
| P8 | **[RE-BOUND — the stock row bound to the hub bundle dir, unresolvable from the target root.]** How many `ADR-NN-*.md` files does the decision registry hold **right now**, what is the **number + slug of the highest-numbered one**, and does its `README.md` index list that same ADR? | `docs/decisions/` ∩ `docs/decisions/README.md` | the registry grows whenever a Council verdict is authored into an ADR — the governance surface this repo exists to produce; count, tail slug, and whether the index kept pace are all live-only and absent from this bundle | `ls docs/decisions/ADR-*.md \| wc -l` then `ls docs/decisions/ADR-*.md \| tail -1` then `grep -c 'ADR-' docs/decisions/README.md` |
| P9 | **[RE-BOUND — `ai-council`'s `validate_backlog` prints NO serialize-groups line; its summary is counts-only.]** What does `validate_backlog` report **right now** for the number of **themes**, **stories**, **tasks**, and **warnings**? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | all four integers drift on any BACKLOG edit — and this window filed several tickets; none are in this bundle | `python scripts/validate_backlog.py` (read the `OK (N themes, N stories, N tasks, N warning(s))` summary line) |
| P10 | **BACKLOG grooming (operator ruling 2026-07-17).** For **every OPEN item** in `BACKLOG.md`, is each still **live** (actively in-progress), **dead** (superseded / obsoleted / already-shipped — a grooming close per ADR-65), or **awaiting-ruling** (blocked on an operator / Council decision)? The successor grooms the **whole open set** at boot — no open `#id` may pass unreconciled. | `BACKLOG.md` ∩ live git | the live / dead / awaiting-ruling status of each open item is an at-boot judgment over current git ∩ `BACKLOG.md`; a summary holds a stale snapshot and cannot tell a still-live item from one already shipped or superseded | `python scripts/validate_backlog.py` then `git log --first-parent --oneline main` to cross-check each open `#id` (this subsumes P4's mechanical half — P10 is the judgment layer over it). **Expect a sizeable open set**; grooming it is the boot obligation, not optional |
| P11 | **[NEW — binds the §1 headline.]** The deleted spike branch's evidence artifacts (`spike/FINDINGS.md`, `spike/evidence.py`, and the implementation files beside them) are **not on any branch**. Locator: commit **`26192dd`**. **Does that object still exist, is it reachable from any ref, and what does its tree still contain?** If it exists — is recovering it, or deliberately discarding it, the ruling? | live git object store (dangling/unreachable objects) | **the answer changes irreversibly the moment `git gc` runs** — this is the one probe in the bundle whose window can close on its own. No summary can know whether collection has already happened; only the live object store can | `git cat-file -t 26192dd` (does it still exist?) then `git branch -a --contains 26192dd` (reachable from anything?) then `git ls-tree -r --name-only 26192dd \| grep spike` (what survives). **Diagnostic only — do not mutate the target to rescue it** |
| P12 | **[NEW — binds the §1 pre-push finding.]** How many **non-merge commits** sit on `main`'s **first-parent spine** right now (the population core-invariant #5 forbids and `block-ff-push` refuses), and what **kind** of commit dominates that population? | live git | the JOURNAL narrates this as a small, recent anomaly; the live population is the only way to see whether it is an anomaly or a standing practice — and the number is deliberately absent from this bundle | `git rev-list --first-parent --no-merges main \| wc -l` then inspect the recent ones' subjects (`git rev-list --first-parent --no-merges main \| head -20`, then `git log -1 --format='%h %cs %s'` per sha) to classify the dominant kind |

> **Dotfile note (P2) — a live limitation of the hub validator, not sloppiness.** The repo-root
> pre-commit config filename is written **un-backticked** in P2's command cell on purpose. The hub's
> `scripts/verify_handoff_probes.py` tokenizer (`file_tokens`) **strips a leading dot** from any path it
> extracts, so a backticked dotfile is looked up without its dot, resolves nowhere, and the probe is
> FAILed as a missing target even though the file plainly exists. **Consequence: no probe in any bundle
> — hub or cross-repo — can currently bind to a dotfile.** That is a hub tooling defect worth filing
> (dotfiles are exactly where config gates live); it is deliberately **not** patched from inside this
> handoff, because hub infra changes are exception-with-ruling (core-invariant #6). The probe's teeth
> are unaffected — the comparison is still live-only and answer-free.

## Gate procedure (CC)

1. **Confirm the run-in root before every command** (the table at the top). A probe run in the wrong
   repo is a **FAIL**, not a pass — the hub and the target have same-named files with different
   contents (`BACKLOG.md`, `ARCHITECTURE.md`, `VISION.md`, `LESSONS.md`, `JOURNAL.md`, and
   `scripts/validate_backlog.py` all exist in both). This is the single most likely failure mode of a
   cross-repo bundle.
2. **P1 first** — the architect cannot begin design until both orienting lines are read live and
   substring-matched. **Then run the operator-context beat (§13d).** Then run P2–P12, each against
   **live state now**.
3. For each, record **PASS** (live ground truth obtained and consistent) or **FAIL** (anchor missing /
   command errored / receiver tried to answer from memory or this bundle).
4. **Any FAIL → ABORT onboarding** and route through the escalation ladder (re-read the named primary
   source → CC re-derives the fact → abort if still unmet).
5. Probes P2–P12 are *designed to move* between generation and check-time — that is the point. **Answer
   values are deliberately absent (§5)**: the pass criterion is **"answered from the live source,"**
   never "matches a remembered number." **P7 is the headline substitute** (four exit codes, read
   explicitly — several gates pass silently, so "no output" must not be scored as "no drift").
   **P2 is the hand-built doc-vs-reality tooth** this repo otherwise lacks. **P10 grooms the whole
   open BACKLOG at boot.** First check which branch is live (P3), then re-derive every load-bearing
   fact from the live primary source.
6. **Run P11 EARLY — it is the only probe with an expiring window.** Every other probe's answer is
   recoverable at any later time; P11's ceases to exist when `git gc` collects the object. If P11
   reports the object gone, that is **not** a probe failure — it is a finding, and §1's item is then
   closed as *unrecoverable*, which is itself the answer the architect must rule against.
7. **Bundle-shape / supplement fill-state is NOT a probe here** (the stock row was re-bound — it
   pointed at the hub bundle dir, unresolvable from the target root). This bundle carries
   `HANDOFF_BOOT` + `RESIDUAL` + `PROBES` + `SUPPLEMENT` + `PASTE_THIS` and **no per-bundle README**
   (HANDOFF_PROCESS §13); the supplement is **generated EMPTY**, so the §13(d) beat fires **FULL**
   unless the operator runs `supplement filled` first. Confirm by looking at the bundle directory in
   the hub — it is CC-side bookkeeping, not target state.
