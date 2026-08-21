# ARTIFACT — CLOUD-R3 conformance review, `[#171]` leg 2 scope

- **slug:** `cloud-r3-conformance` · **lane:** read-only cloud review · **effort:** medium
- **Bound at:** `main` · session HEAD `78267fd` (*Merge branch 'docs/journal-i-2026-08-20'*)
- **Subject:** `ecosystem/conformance.html` AND its generator `scripts/gen_dashboard.py`
- **Posture:** evidence only. Nothing repaired, nothing moved, no disposition taken. The architect rules.

## 0 · Environment guard (declared, per the brief)

`git rev-parse --is-shallow-repository` → **`true`** (314 commits present). Per the brief's
shallow-clone guard, **no spine-walking instrument was run** — `validate_git_backlog`,
`validate_no_ff`, `journal_anchor` and kin were all skipped, and nothing below rests on a
first-parent spine walk. Every finding is anchored to a file/line in the working tree or to
`git log -1`.

## 1 · SCOPE AMBIGUITY — flagged, not resolved (blocking for disposition)

The brief says to scope this review "EXACTLY per `[#171]` leg 2 **as written in that row**".
**The row contains no leg enumeration.** It is one sentence plus one `Done when:` clause, and
the strings "leg", "leg 2", "stage", and "conformance.html" do not appear in it. The row is
byte-identical at both of its homes:

- `BACKLOG.md:83`
- `tasks/171-build-the-conformance-dashboard-at-ecosystem-con.md:12`

Its full `Done when:` reads: *"`ecosystem/conformance.md` is generated + committed by a
read-only validator (Layer-2-safe) **and** ARCHITECTURE Ch2 carries the pointer"*.

Three readings exist, and they are not compatible. I did **not** pick one:

| # | Reading | Where it comes from | What "leg 2" then means |
|---|---|---|---|
| **R-A** | **Literal — the row's own text.** The only enumerable structure in the row is the two-conjunct `Done when:`. | `BACKLOG.md:83` | **"ARCHITECTURE Ch2 carries the pointer."** |
| **R-B** | **Operational — the handoff's phrase.** The exact string "`[#171]` leg 2 scope" exists only in the 2026-08-20 handoff bundles, where it means *stage 2, whose scope the operator's review of the HTML will set*. | `docs/handoffs/2026-08-20-dev-knowledge-architect-2/PASTE_THIS.md:528` and `:613`; `.../SUPPLEMENT.md:97`, `:182`; `docs/handoffs/2026-08-20-dev-knowledge-architect/PASTE_THIS.md:530`, `.../SUPPLEMENT.md:94` | **"Whatever the operator's review of `conformance.html` decides stage 2 is."** Undetermined by construction. |
| **R-C** | **Build-stage — the generator's own claim.** `scripts/gen_dashboard.py:2` self-describes as "`[#171]` **stage 1**". | `scripts/gen_dashboard.py:2` | **"Stage 2 of the dashboard build"** — sections/behaviour not yet specified anywhere in the repo. |

**The brief's own done-contract presupposes R-B** (it asks for a review of `conformance.html`,
which only R-B/R-C touch), while its scoping instruction ("as written in that row") mandates
**R-A** — and under R-A the HTML is out of scope entirely, because the row names only
`ecosystem/conformance.md`. **This is the conflict the brief told me to report rather than
improvise around.** I therefore reviewed **both**: §2 carries R-A's finding, §3 carries the
`conformance.html` + generator review the done-contract asked for. Severity of the ambiguity
itself: **P1** — under R-A leg 2 is a two-line documentation act that is *currently
undischarged*; under R-B it is an open-ended stage-2 build. Those are not the same work item,
and closing `[#171]` under one reading silently leaves the other undone.

Supporting authority read, for the architect's convenience:
`docs/decisions/ADR-86-conformance-dashboard-location.md:11-13` (location · zone class ·
Ch2 pointer, the ADR's own numbered items 1/2/3) and
`docs/audits/2026-08-19-technical-171-dashboard-lane-contract.md:54-57` (the operator addendum
of 2026-08-19 that birthed the HTML sibling — **the only authority for the HTML anywhere in
the repo**; it is an addendum to a lane contract, never folded back into the `[#171]` row).

## 2 · R-A finding — leg 2 read literally

**The `Done when:` second conjunct is NOT discharged.** `ARCHITECTURE.md` Ch2 (§"Organ map",
lines 255–369) carries **no pointer to the conformance dashboard in any form** — not
`ecosystem/conformance.md`, not `ecosystem/conformance.html`, and no organ row for
`scripts/gen_dashboard.py`. Verified two ways:

- A scan of lines 255–369 for `conformance|dashboard|gen_dashboard` returns exactly one hit,
  `ARCHITECTURE.md:314` — and it is a **different organ**: `conformance-hub.js`, the ADR-70
  Tier-3 read-only Workflow. Name-adjacent, decision-unrelated. A reader skimming for
  discharge could easily mistake it for the pointer; it is not.
- `gen_dashboard` appears in **no** living doc — zero hits across `ARCHITECTURE.md`,
  `VISION.md`, `CLAUDE.md`.
- The dashboard's only mention anywhere in `ARCHITECTURE.md` is at **line 994**, in
  §"Governing ADRs" — and it is a *description of ADR-86*, not a navigation pointer, and it
  sits in the wrong chapter for the row's requirement.

Compounding: `ARCHITECTURE.md:260-266` declares the generated `ecosystem/organ-index.md` to be
Ch2's **"verified source"** ("when they disagree, trust the index"). That index has no
dashboard row either — `ecosystem/organ-index.md:77` lists only `conformance-hub.js`, and
`ecosystem/organ-registry.yaml` carries no dashboard entry, so the index cannot grow one by
regeneration. **Both the hand-maintained table and its verified source are silent**, so the
gap is not a stale-table artifact.

ADR-86 anticipated exactly this: item 3 (`ADR-86:13`) says the pointer *"lands with the build,
not before — a pointer to a not-yet-generated file would itself be drift"*. The build has now
landed. The pointer has not.

## 3 · Findings table — `conformance.html` + `scripts/gen_dashboard.py`

Severity is this reviewer's proposal. Dispositions are **proposals to the architect**, not acts.

| # | Item | Evidence (path:line) | Sev | Proposed disposition |
|---|---|---|---|---|
| **F1** | **Leg-2 scope is unresolvable from the row.** Three incompatible readings (§1); the row never says "leg", never mentions the HTML. Any close of `[#171]` today is ambiguous about what was closed. | `BACKLOG.md:83` · `tasks/171-…:12` · handoff `PASTE_THIS.md:528`,`:613` · `gen_dashboard.py:2` | **P1** | **Architect ruling required** — pick a reading and write it INTO the row (the row is the checkable surface). If R-B, the HTML addendum at `docs/audits/2026-08-19-…-lane-contract.md:54-57` needs folding into the row too; it currently governs a shipped artifact from inside a lane contract. |
| **F2** | **Leg 2 read literally is undischarged.** No dashboard pointer in `ARCHITECTURE.md` Ch2; none in its declared verified source `ecosystem/organ-index.md`; none in `organ-registry.yaml`. Only near-hit is a different organ. | `ARCHITECTURE.md:255-369` (miss) · `:314` (near-hit, `conformance-hub.js`) · `:994` (wrong chapter, ADR description) · `ecosystem/organ-index.md:77` · `ADR-86:13` | **P1** | Land the Ch2 pointer as its own act. Note it touches `ARCHITECTURE.md`, a freshness-gated collision file — the batch-4 W5 / v2.57 precedent (integrator-owed row) applies. If the registry route is chosen instead, `organ-registry.yaml` gains the entry and Ch2 points at the index. |
| **F3** | **Both artifacts claim to be "committed" by the validator; the generator never commits.** `write_outputs` writes two files and returns 0; `main` has no commit path; the only `subprocess` use is `GitReader` (reads only, `gen_dashboard.py:235-250`). Grep for a git-commit invocation across the module: **zero**. Yet the artifact face asserts *"Generated, committed, read-only (ADR-86 location + ADR-80 zone class)"*. | claim: `ecosystem/conformance.html:45`, `ecosystem/conformance.md:7` · code: `gen_dashboard.py:1188-1196` (`write_outputs`), `:1214-1236` (`main`) · requirement: `ADR-86:12`, `BACKLOG.md:83` | **P1** | This is leg **1**'s other half, and it is a **self-claim the code does not implement** — the class the repo treats most seriously. Either (a) implement the ADR-80 writer policy (pathspec-bounded, never `git add -A`, fail-soft, commits only its own two files), or (b) rule that human-committed output satisfies "committed" and **amend both the ADR-86 §2 wording and the two artifact strings** so no surface claims a mechanism that does not exist. Do not leave (c). |
| **F4** | **The committed dashboard is stale against the tree it describes.** Artifact says `HEAD d436d64fff86`; live HEAD is `78267fd`. The generator's determinism contract means this is expected drift — but nothing surfaces it. | `ecosystem/conformance.html:43` vs `git log -1` → `78267fd` | **P2** | Regenerate at integration time. Pair with F5 — without a gate this recurs every window. |
| **F5** | **`--check` is armed nowhere.** The generator's own docstring concedes it: *"that is a 'regenerate me' signal, and it gates nothing (no hook is armed)"*. Every sibling generated surface in this repo **is** gated — `audit-index-freshness`, `organ-index-freshness`, `claude-rosters-freshness`, `roster-freshness`, `intake-index-freshness` (CLAUDE.md §9). The dashboard is the lone ungated committed-generated artifact. | `gen_dashboard.py:36-37` · `:1203-1220` (`check_outputs`, correct and unused) · CLAUDE.md §9 roster | **P2** | Propose a `dashboard-freshness` regen-and-diff pre-commit hook on the `_TARGETS` pair, mirroring the five siblings. **NOT ACTED ON — `.pre-commit-config.yaml` is on this lane's never-touch list.** Flagged for the architect only. |
| **F6** | **The HTML — the artifact the operator was asked to review — silently carries LESS than the markdown.** Missing from the HTML entirely: the **Determinism** bullet (so an HTML reader has no way to learn the page is HEAD-pinned and goes stale — F4 is invisible to them), the `--check` **verify** line, and Section 2's **"Terminal docs … belong in `docs/intake/archive/`"** legend (so the `Archived` column of `—`/`yes` is unexplained). Also lost: the closed-count `(22)` on the Section 1 roll-up. Counts: `Determinism` md 1 / html 0 · `--check` md 2 / html 0 · `Terminal docs` md 1 / html 0. | md: `:10`, `:11`, `:110` · html: `render_html` body list, `gen_dashboard.py:1163-1181`, and `_html_intake:1067-1091` (no trailing legend) | **P2** | The two renderers drift because they are hand-parallel prose, not one source. Propose either a shared section-prose constant or a test asserting HTML ⊇ markdown's normative notes. Highest operator impact of the P2s: the HTML is the review surface. |
| **F7** | **Section 5's headline commit-tax figure is ~3× the live one.** Dashboard reports **290.9 s (median), measured 2026-08-18**. The 2026-08-20 handoff records the `--parallel` flip **live on main** (`54633041`) with commit tax **~97 s quiet**. The generator is not lying — `_COMMIT_TAX_RE` requires the literal `**median: N s**` shape (`gen_dashboard.py:757`), and a repo-wide scan finds that shape in exactly **one** file, the 2026-08-18 baselines. The post-flip number was never published in the parseable shape. But the artifact presents the stale figure as *the* commit tax with only a date qualifier. | dashboard: `conformance.html:92`, `conformance.md:246` · regex: `gen_dashboard.py:757` · only parseable source: `docs/audits/2026-08-18-technical-phase0-baselines.md:41` · superseding measurement: `docs/audits/2026-08-20-technical-parallel-flip-lane-contract.md:21` + handoff §9 (`54633041`, ~97 s) | **P2** | Two independent halves. (a) **Data**: publish the post-flip median in the `**median: N s**` shape so the generator can see it. (b) **Honesty**: have the renderer state the figure's *age* relative to HEAD, or say "newest parseable measurement" — a silently-stale headline number is the failure mode this dashboard exists to prevent. |
| **F8** | **ADR-ledger twins are mislabelled — a real parser defect, not a display quirk.** `by_number: dict[int, Path]` is keyed on ADR number, so a duplicate number is **last-writer-wins**. ADR-51 and ADR-70 each have a parent + an amendment file. The amendment's H1 (`# ADR-51 Amendment 2026-07-05 — …`) does not match `_LEGACY_TITLE_RE` (which needs a separator straight after the number), so its title falls back — and reads the **parent's** file. Result on the operator's screen: two `ADR-51` rows, *identical status and title*, differing only by date; likewise `ADR-70`. `AdrRow.filename` is populated only for off-grammar rows, so nothing on the page disambiguates them. | `gen_dashboard.py:614-619` (collision), `:626-637` (fallback + `filename` unset), `:548` (`_LEGACY_TITLE_RE`) · rendered: `conformance.html:84` · sources: `docs/decisions/ADR-51-amendment-2026-07-05-….md:1`, `ADR-51-architecture-doc-convention.md` | **P2** | Key `by_number` on the **path**, not the number (or make it `dict[int, list[Path]]`), and surface `filename` in the full-ledger table for every row. Until then the ledger's amendment rows carry another decision's title — a wrong claim, not a missing one. |
| **F9** | **"Full ledger (88 ADRs)" is a file count presented as an ADR count.** 88 = rows = files under `docs/decisions/` + `archive/`. Distinct ADR numbers = **86**. The two-file amendments (F8) inflate it. | `gen_dashboard.py:1116` (html), `:685` (md) · rendered `conformance.html:84` | **P3** | Relabel to "88 decision files (86 ADRs)", or count distinct numbers. Cosmetic alone, but it is the same root cause as F8 and should ride with it. |
| **F10** | **`<!-- scope: meta -->` is markdown-only.** The HTML sibling carries no scope tag. Informal/unenforced (CLAUDE.md §4, ADR-27/ADR-48), so noted for completeness only. | `conformance.md:3` · html: absent | **P3** | Accept as-is, or add an equivalent `<meta>`. No gate reads it either way. |

### Conformance PASSES worth recording (checked, not assumed)

- **Layer-2 invariant holds.** The generator drives no state in any other repo, imports no gate,
  arms no hook, and writes exactly two paths — and only under `--write` (`gen_dashboard.py:16-18`,
  `_TARGETS:1185`). `GitReader` (`:235-250`) is the single `subprocess` site and reads only.
- **"Reports, never repairs" holds.** 5 anti-orphan VIOLATIONs and 3 ADR flags are rendered and
  left exactly where found (`conformance.html:77`, `:83`).
- **The HTML is genuinely self-contained.** Zero occurrences of `http`, `src=`, or `<script>` —
  no network reference of any kind, inline CSS only. It opens without running anything, which is
  the operator addendum's whole purpose.
- **Library-first holds.** Borrowed parsers, loaded by path (`gen_dashboard.py:24-32`, `:141-152`).
- **The encoding defect recorded at `JOURNAL.md:747` is fixed** — every read now passes
  `encoding="utf-8"` explicitly (`:392`, `:485`, `:629`, `:644`, `:817`, `:839`, `:889`).

## 4 · What the operator SEES today vs what `[#171]` leg 2 says they should see

Opening `ecosystem/conformance.html` today, the operator sees a clean, self-contained, offline
page that genuinely answers their four standing questions — what finished (Section 0's 22
release-note lines), where the telemetry is (Section 4: absent, lane L2 in flight), whether the
intakes passed the gate (Section 2: five red VIOLATIONs, named), and whether implemented ADRs
are archived (Section 3: three flags over an 88-row ledger). What they cannot see from that page
is that it describes a tree two merges old (`d436d64fff86`, not today's `78267fd`), that its
headline commit-tax figure of 290.9 s was superseded by the `--parallel` flip's ~97 s, that two
of its ADR rows carry the wrong decision's title, and that nothing anywhere will tell them when
any of this goes stale — because the HTML omits the very Determinism bullet its markdown sibling
uses to disclose exactly that. Against `[#171]` **as literally written**, the mismatch is
sharper still and runs in the other direction: leg 2 of that row is not a dashboard feature at
all but a **navigation** promise — *"ARCHITECTURE Ch2 carries the pointer"* — and an operator
who opens `ARCHITECTURE.md` Ch2 looking for the conformance surface finds no pointer, only a
same-named different organ (`conformance-hub.js`, `:314`) that will send them somewhere else
entirely. So the honest summary is that the operator sees a **stage-1 artifact that is better
than its own documentation admits and staler than its own face reveals**, sitting at the end of
a road the architecture map does not yet draw — while the row's leg 2, read as it is actually
written, is one undischarged pointer, and read as the handoff uses the phrase, is a stage-2
scope that only their review can set. Which of those two the architect is closing is F1, and it
is the one thing this lane cannot decide for them.

---

*Read-only review lane. No repo file was modified other than this artifact. No merge, no push to
`main`, no disposition taken.*
