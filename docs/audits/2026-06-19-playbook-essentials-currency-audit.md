# PLAYBOOK + ESSENTIALS — currency & coherence audit — 2026-06-19

<!-- scope: meta -->

> **Read-only content audit** of `protocols/PLAYBOOK.md` (3318 lines) and
> `protocols/ESSENTIALS.md` (442 lines), produced from the two files uploaded to the
> architect on 2026-06-19. Companion to the date-stamp "doc-currency seal" of the same day:
> that seal verified `last_reviewed` freshness (the *easy* metric); this audit verifies
> **referential currency** — does what the docs *describe* still *exist* (the *hard* metric).
> Immutable per repo convention (supersede with a new dated file; never edit in place).
>
> **Confidence discipline (per ESSENTIALS "Architect epistemic discipline", L143–167).**
> Findings are graded. **Witnessed** = read directly in the uploaded text (line-cited).
> **Doc-asserted** = the doc's own annotation says so (e.g. "archived 2026-06-05"); corroborated
> by operator + memory, but live ground-truth (the filesystem / JOURNAL) was **not** available
> to this audit. **Confirm-live** = flagged for CC to resolve against `.claude/`, `~/.claude/`,
> `docs/decisions/`, and `JOURNAL.md`; **not asserted dead.** The architect has no filesystem
> access; every "purge" disposition is a *recommendation the operator ratifies* and CC verifies
> against live state before acting (core-invariant: never delete content without an explicit ask).

---

## 0. Headline

**The rot is real, and it is one class wearing two masks: referential currency (do referenced things still exist) + structural coherence (is the document one coherent artifact).** It is the unenforced half of ADR-88 — markdown-as-object-with-edges — applied to prose. The BACKLOG has a dangling-edge detector (#156/#179); prose has none.

**The doctrine already exists and is unenforced.** ESSENTIALS L200–207 ("Supersession closes the loop") states the rule verbatim: *any decision that relocates/replaces/centralizes an artifact must name the obsolete artifact in a `Decommission:` field; a non-empty field becomes a BACKLOG item until removed; creation without decommissioning is how orphans accumulate.* The decommissions happened (`/boot`, `/evolve`, §18, tier-system); the **doc-reference cleanup loop never fired.** So the proposed detector **enforces an existing rule** — it does not invent doctrine. That is the strongest possible footing for the Council step.

**Two kinds of retirement-annotation — do NOT conflate them:**
- **Kind B — dead reference in a *usable position*** (a command table, a "type this" step, a cheat-sheet). Misleads on sight. **Purge.** (`/boot`, `/evolve`.)
- **Kind A — anti-regression *context note*** (an inline "X retired — use Y instead"). Mostly load-bearing; prevents reintroduction. **Condense, don't blanket-purge.** (`CHANGELOG retired`, `tier deprecated`, `tech-radar retired`.) Removing these risks losing the guard.

A naive "flag every mention of a retired thing" detector would false-positive on the ~18 `CHANGELOG retired` notes. The note-vs-usable distinction is a **load-bearing requirement of the detector spec** (§8).

---

## 1. Dead references in usable positions — PURGE (high confidence)

Status of `/boot` and `/evolve`: **doc-asserted archived 2026-06-05 Phase-C3** (the docs tag every occurrence with the archive path) + operator-confirmed ("boot nie używam; evolve już nie ma") + memory (self-evolution system retired). **Confirm-live:** CC verifies neither resolves in `.claude/commands/` or `~/.claude/`.

| Locus | What it is | Why it's Kind-B (misleads) |
|---|---|---|
| PLAYBOOK L1648, L1650 | `/boot`, `/evolve` rows in the **command reference table** | Presented as commands with a parenthetical archive-tag; a scanner of the table reads them as options |
| PLAYBOOK L1750–1751 | `/boot`, `/evolve` in a **"commands in play" list** | Same |
| PLAYBOOK L3154, L3158 | `/boot`, `/evolve` in **Appendix A › Slash Commands** cheat-table | A cheat-sheet is the highest-traffic "what can I run" surface — worst place for a dead command |
| PLAYBOOK L1741, L1864 | `/boot` in inline examples (`/session-summary`, `/boot context loading`) | Listed alongside live commands as a peer |
| PLAYBOOK L2711 | `/evolve` as **step 1 of §9 Weekly Review** | Instructs running an archived command |
| ESSENTIALS L227 | "Type `/boot`" as **step 2 of "Starting a Session"** | A daily-driver session-start step that is dead |
| ESSENTIALS L259 | `/boot`, `/evolve` in the **slash-commands cheat-line** | Daily cheat-sheet, same as PLAYBOOK Appendix A |

**§9 Weekly Review (PLAYBOOK L2706, ToC L157)** — the whole chapter's engine (`/evolve`) is archived; the section is hollow. *Disposition: retire the chapter or rewrite around a live cadence — operator decides which; do not leave it engine-less.*

**Recommended disposition for §1:** remove `/boot`/`/evolve` from every *usable* position (tables, steps, cheat-sheets). If a record of the archival is wanted, keep **one** line in a single "retired machinery" note (not nine scattered tags). Operator ratifies.

---

## 2. Structural defects — LINT / FIX (Witnessed)

- **Missing §18.** Chapter numbering runs 1…17, then **jumps to §19** (PLAYBOOK L3004 `## 17.` → L3047 `## 19.`; L3040–3044 is the tail of §17). §18 was removed and the sequence was never re-closed. *This is the literal proof of "things get removed, structure isn't groomed."*
- **PLAYBOOK is two documents glued together.** First half (L214–1932) is **un-numbered** reference chapters (`## System Architecture`, `## Repo conventions`, `## Claude Code internals`, …). Second half (L1933–3122) is **numbered** workflow chapters (`## 1. Starting a New Project` … `## 19.`). Then two un-numbered sections are tacked on after the appendices (`## Codemap workflow` L3237, `## Auto-TOC for large canonical docs` L3308). The numbered "playbook" begins at **line 1933 — past the halfway point.** This is the source of "kropki potem liczby" in the ToC (un-numbered sections render as bullets; numbered ones as 1–19) and of "wygląda jak sklejone."
- **Embedded templates at H2 pollute the chapter structure and the ToC.** These are example templates, not chapters, but sit at `##`: `## What this project does` / `## Architecture` / `## Dev standards` / `## Key commands` / `## What NOT to do` / `## Folder governance` / `## Global skills` (CLAUDE.md template, L1956–1984); `## Question:` (L2294); `## Severity breakdown` / `## Findings` / `## Resolution summary` / `## Notes` (audit template, L2548–2572); `## Big picture` / `## <Theme>` (BACKLOG template, L2739–2740). *Fix: demote embedded templates to fenced code blocks or H4+, so they stop masquerading as chapters.*
- **ToC scheme is inconsistent** (bullets for the un-numbered half, numbers for the numbered half). *Operator preference: numbers throughout.* The ToC is generator-driven (`toc-freshness` hook; ESSENTIALS L305) — so the fix is upstream in the generator + a consistent header scheme, not hand-editing.

---

## 3. Coherence defects — RECONCILE (Witnessed)

- **ADR-87 skeleton contradicts its own section — in BOTH files.**
  - PLAYBOOK §2 states the ADR-87 split correctly (L2013–2024: *architect emits intent/closure/anti-patterns/mode/governance-pointer; CC owns code-impact context, generic gotchas, skeleton, model/effort*). But the **skeleton subsection of the same section** (`### Structure`, ~L2111) leads with `→ Read CLAUDE.md + relevant gotchas` **without marking which lines the architect emits vs which CC self-loads.** On its face it reads as instructing the architect to do what ADR-87 (eleven lines above) assigns to CC.
  - ESSENTIALS repeats the same shape: L276 skeleton (`Title → Read CLAUDE.md + gotchas → …`) immediately followed by L278 stating the ADR-87 architect-output rule (CC self-loads gotchas).
  - *This is exactly the operator's "prompt structure już nie respektowany."* **Fix:** tag the skeleton lines (architect-emitted vs CC-self-loaded) so the skeleton visually matches the ADR-87 split it sits under. Low-risk, high-clarity.
- **Self-referential note:** the same-day refutation of "PLAYBOOK lags ADR-87" checked **one locus** (the contract statement, L2012–2020) and found it current — but did not catch this skeleton contradiction in the same section. Even the verification measured a locus, not whole-document coherence. The defect this audit exists to fix, in miniature.

---

## 4. Over-annotation — CONDENSE (lower priority; operator judgment — these are mostly load-bearing)

Kind-A context notes. Each is short, but heavily repeated. **Do not blanket-purge** — they guard against reintroducing the retired thing.

- **`CHANGELOG.md retired (ADR-49)`** — ~18 inline occurrences (PLAYBOOK L409, 830, 897–898, 941, 1586, 1904, 1944, 2003, 2164, 2476, 2581, 2583, 2617, 2649, 2951, 2967, 3072; ESSENTIALS L319). *Candidate: state once in Markdown Governance / Commit-message standard; drop the ~18 inline reminders. Net readability win; the regression-guard survives in the single canonical statement.*
- **Repo-tier system DEPRECATED 2026-05-23** — ~10 occurrences (PLAYBOOK L51, 630, 799, 842, 850, 2726, 2981; ESSENTIALS L416, …). *Mostly keep (explains why no tier-gating).* **Exception — purge target:** the **deprecated tier-transition *procedure* subsection** (PLAYBOOK L799–810, in ToC L51) is a dead *procedure* kept in-document, distinct from the inline notes. Archive it.
- **`tech-radar` / `docs/research/` retired** — ~8 occurrences (PLAYBOOK L1528, 1562, 1591, 1610, 1905, 904, 2347; …). *Keep the canonical statement (Continuous Improvement); the scattered repeats are condense-candidates.*

---

## 5. Placeholder / forward-pointer accretion — RESOLVE (Witnessed)

- **`[TBD — Stream C session 3, ADR-33]` and `[TBD — Stream C session 3, ADR-34]`** (PLAYBOOK L490, L497) — placeholders pointing at a planning phase ("Stream C session 3") that reads stale. *Confirm-live: still pending, or stale-and-removable?*
- **`#18 / #27 "not yet written"` forward-pointer** (PLAYBOOK L2066, decision-routing family) — a promise of sibling rules that don't exist yet. *Either file #18/#27 as real BACKLOG items or trim the forward-pointer; an unwritten promise that lingers is accretion.*

---

## 6. Confirm-live candidates — operator / CC decide (NOT asserted dead)

- **§19 Scrum-Master Review Propagation** (PLAYBOOK L3047) — substantive, **not** archived, with a 2026-05-11 empirical example. Operator was unsure it is still practiced. *Confirm: live → keep; retired → archive the section. This audit does not assume.*
- **`/save`** (PLAYBOOK L1652) — operator believes it is live ("save to chyba ty używasz"). *Confirm in `.claude` / `~/.claude`; almost certainly live.*
- **ADR references throughout** (ADR-28/33/34/38/40/43/45/49/51/53/59/60/61/64/65/66/70/77/78/80/82/84/85/87, …) — *CC verifies each cited ADR resolves to an existing `docs/decisions/ADR-*.md`.* Cannot be checked from the two uploaded files alone. (Note: ADR-45 is **doc-asserted "explored but not adopted / never implemented"** — ESSENTIALS L167, L194 — so several "operator review only" disciplines rest on an unbuilt validator. Worth surfacing as its own pattern: doctrine designed, enforcement never shipped.)

---

## 7. ESSENTIALS as a lens of PLAYBOOK — RESHAPE candidate (operator's vision)

Today ESSENTIALS is a **thematic digest** of load-bearing essentials, each section ending in a `Full: PLAYBOOK §X` pointer (L9 declares this design). Its sections do **not** map 1:1 to PLAYBOOK's chapters.

Operator's vision: ESSENTIALS = **one lens-line per PLAYBOOK chapter** — a structured projection. That is a genuine reshape, and it creates a **checkable dependency** (each ESSENTIALS lens-line ↔ a PLAYBOOK chapter; if a chapter is added/removed, the lens-line is added/removed). That dependency is itself an instance of the ADR-88 file-as-object pattern, and the structural linter (§8) can assert the projection stays 1:1. *Deliberate decision — route with the groom or the Council scope; do not silently reshape a daily-driver doc.*

---

## 8. What this audit seeds — the detector spec (mechanism-not-memory)

The findings above are the seed for the durable organ. Three load-bearing design points fall straight out of this audit:

1. **Truth source = live existence ∪ retirement ledger.** For each reference in a living doc, resolve it against {does the command/skill/hook/file EXIST in `.claude/`, `~/.claude/`, the repo} ∪ {is it marked retired in `JOURNAL.md` / `docs/archive/` / an ADR}. Classify **live / confirmed-dead / unknown**. Derived from the repo's own records — never a hand-maintained "dead list." (Operator's instinct "analyze PLAYBOOK *with the JOURNAL*" is exactly this: the JOURNAL is the removed-ledger.)
2. **Note-vs-usable, or the detector cries wolf.** It must flag dead references **in usable positions** (tables, "do this" steps, cheat-sheets) — not every historical mention. Otherwise the ~18 `CHANGELOG retired` notes (§4) are 18 false positives. The registry distinguishes *retired-and-must-not-appear-as-usable* (`/boot`, `/evolve`) from *retired-but-cited-as-history* (`CHANGELOG`, `tech-radar`).
3. **It enforces an existing rule.** This is the mechanical teeth for "Supersession closes the loop" (ESSENTIALS L200) — promoting that advisory rule to an enforced one. Pairs with promoting **ADR-88 Proposed → Accepted** so the doctrine the organ enforces is itself load-bearing.

**Layered placement (same detect / groom / gate shape as the rest of the system):**
- **Detect** — nightly conformance digest (ADR-84, `origin/automation/conformance-digest`): full-repo scan → dangling-doc-reference report. Non-blocking.
- **Groom** — human-ratified purge (like the #140 grooming-gate). Detector proposes; operator approves removal.
- **Gate-on-regression** — pre-commit + handoff: block *adding* a reference to a known-dead entity. Universal hook on the root-7 canonical set + a `.dev-knowledge`-local extension for PLAYBOOK/ESSENTIALS (carrier-doctrine pattern; resolves the universal-handoff-vs-repo-local-PLAYBOOK tension). Surface-the-debt always; hard-gate only on regression.

**Separate organ — structural linter** (orthogonal to referential currency): chapter-numbering contiguity (catches the missing §18), single header scheme (numbers, per operator), no embedded-template H2s, ToC consistency, ESSENTIALS↔PLAYBOOK projection 1:1.

This is an architecture decision (how to realize ADR-88 for prose / doc-lifecycle) → **AI Council**.

---

## 9. Good patterns already present — DO NOT LOSE

The repo already knows how to do this right; the gap is *consistency*, not knowledge.

- **ESSENTIALS L238 ("Parallel sessions", ADR-61)** — a superseded section handled **correctly**: `⚠️ SUPERSEDED` banner, the dead recipe struck through (`~~…~~`), an explicit pointer to the live procedure, "Text kept below for history." **This is the supersession template the grooming standard should mandate** — the opposite of the `/boot` tag-bolted-on-a-usable-row anti-pattern. (Minor: even here, a daily-driver cheat-sheet may not be the right home for struck-through history — archive is.)
- **ESSENTIALS L143–167 (Witnessed / Inference / Unknown discipline)** — the house epistemics: bundle-asserted facts default to Inference/Unknown unless verified. The audit above applies it (the confidence grading). The same discipline applies to the architect's own inherited claims.

---

## Summary — disposition counts

- **Purge now (Kind-B dead refs in usable positions):** `/boot` ×~7, `/evolve` ×~4 across both files; §9 Weekly Review (retire/rewrite); deprecated tier-transition *procedure* subsection.
- **Fix structure:** close the §18 gap (renumber); demote embedded-template H2s; one ToC scheme (numbers).
- **Reconcile coherence:** tag the ADR-87 skeleton lines (architect vs CC) in PLAYBOOK §2 + ESSENTIALS "Writing a Prompt".
- **Condense (operator judgment, lower priority):** ~18 `CHANGELOG retired` + ~10 tier + ~8 radar/research inline notes → canonical-once.
- **Resolve placeholders:** `[TBD — Stream C session 3]` ×2; `#18/#27` forward-pointer.
- **Confirm-live (NOT asserted dead):** §19 Scrum-Master; `/save`; all ADR refs; the ADR-45-never-built pattern.
- **Reshape (deliberate):** ESSENTIALS → 1:1 projection of PLAYBOOK chapters.
- **File (durable):** referential-currency detector + structural linter (Council; enforces "Supersession closes the loop"; pairs with ADR-88 → Accepted).

---

*Produced read-only 2026-06-19 from uploaded `PLAYBOOK.md` + `ESSENTIALS.md`. Line numbers as of those uploads. Live-state items (filesystem, JOURNAL, ADR resolution, `.claude/` command presence) are flagged Confirm-live and must be verified by CC before any purge. No files were modified by this audit.*
