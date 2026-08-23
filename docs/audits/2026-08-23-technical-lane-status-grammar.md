# LANE L3 — ADR status-grammar validator + marker sweep (M5, `[#242]`)

- **Date:** 2026-08-23 (batch date; executed 2026-08-24)
- **Lane:** `worktree-status-grammar`, branch `worktree-status-grammar`
- **Contract:** `LANE-L3-status-grammar.md` (frozen, authored before the build)
- **Merge base:** `aeec0fd1` (main tip at dispatch)
- **Scope:** the status *grammar* and its gate. Not deciding any ADR's status, not archiving.

---

## Contract-locator corrections (preflight)

Resolved before acting, per CLAUDE.md §4 M1.

| Contract cites | Actual | Impact |
|---|---|---|
| `docs/adr/` (dispatch gate) | `docs/decisions/` | None on intent — both name the ADR corpus. The dispatch gate's ordering claim still reads correctly against the real path. |
| "four incompatible `Status:` grammars" | **four in the live zone, five corpus-wide** | The fifth (`G5`, blockquote) lives only in `docs/decisions/archive/`. The contract's figure is right for the zone it was measuring. |

Dispatch gate verified satisfied: the ADR-100 ruling landed at `a40bac40`, an ancestor of the
merge base; the Phase-0 packet is present at
`docs/audits/2026-08-23-technical-phase0-preconditions.md`.

---

## Step 1 — Measured divergence (the evidence base)

Method: every `docs/decisions/ADR-*.md` (and `archive/`) scanned over its first 30 lines for a
status field under five candidate grammars, most-specific-first, one match per line. Measured
2026-08-24 against merge base `aeec0fd1`.

**Live zone: 87 ADR files, 87 status fields — a clean 1:1.** No file lacks a status field; no
live file carries two.

### The syntactic axis — four live grammars

| ID | Shape | Live | Archive |
|---|---|---|---|
| **G1** | `- **Status:** V` — list item, bold, colon outside the bold | **40** | 1 |
| **G2** | `**Status:** V` — bare bold paragraph | **34** | 0 |
| **G3** | `Status: V` — plain text, no markup | **12** | 1 |
| **G4** | `status: V` — YAML frontmatter, lowercase key | **1** | 0 |
| **G5** | `> **Status: V**` — blockquote banner, **colon inside the bold** | **0** | 1 |

### Roster by grammar (live zone)

- **G1 (40)** — ADR 48, 49, 50, 51×2, 53, 54, 55, 56, 57, 58, 59, 60, 62, 63, 70, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 94, 95, 96, 97, 98, 99, 100, 101, 104, 111, 112, 113, 114
- **G2 (34)** — ADR 27, 28, 29, 30, 31, 32, 33, 64, 65, 66, 67, 68, 69, 70, 71, 72, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 102, 103, 105, 106, 107, 108, 109, 110
- **G3 (12)** — ADR 34, 35, 36, 37, 38, 39, 41, 42, 43, 45, 46, 47
- **G4 (1)** — ADR 61
- **G5 (0 live / 1 archived)** — ADR 40

`51` and `70` each appear twice because two files carry each number (see "Collateral findings").

### The semantic axis — the value vocabulary is separately divergent

The grammar axis is *how the field is marked up*. The value axis is *what vocabulary it uses*,
and it diverges independently:

| Head token | Count | Files |
|---|---|---|
| `Accepted` | 82 | — |
| `Partially superseded` | 2 | ADR-46, ADR-47 |
| `PARKED` (bold-wrapped `**PARKED**`) | 1 | ADR-114 |
| `Explored, not adopted` | 1 | ADR-45 |
| `Accepted 2026-05-28` (date fused, no separator) | 1 | ADR-61 |

Qualifier shape across all 87: **47 bare**, 20 em-dash-qualified (`Accepted — 2026-06-06`),
17 paren-qualified (`Accepted (ratified by merge 2026-06-29)`), 3 other.

**Neither `Superseded` nor `Deprecated` appears on any live ADR.** Both appear only in the
archive. This independently confirms the `[#552]` observation that a terminal-status check keyed
on those two values is *structurally unreachable* against the live corpus — nothing ever writes
them.

### Verbatim — every live field whose value is not exactly `Accepted`

The other 47 fields carry the byte-identical string `Accepted`; they are listed by number in the
roster above and nothing is elided by not repeating one string 47 times.

```
ADR-42   [G3:5]  Accepted (amended four times: 2026-05-09 afternoon, 2026-05-09 later afternoon, 2026-05-09 night, 2026-05-26)
ADR-43   [G3:5]  Accepted — 2026-05-11
ADR-45   [G3:5]  Explored, not adopted; ADR-42 v3.2 remains canonical authority for handoff architecture
ADR-46   [G3:3]  Partially superseded — retained as convention, NOT audit-enforced
ADR-47   [G3:3]  Partially superseded — retained as convention, NOT audit-enforced
ADR-51a  [G1:3]  Accepted (ratified by ROOT at Wave-2 integration 2026-07-05, ADR-94 status-line-only path; authored in epic lane `llm-first-docs` [#259] under root conditional grant, ADR-97 — the lane did not self-accept). Ratification affirms the frozen direction: ... audit check #7 (`mermaid_theme_directive`) retired.
ADR-61   [G4:4]  Accepted 2026-05-28
ADR-62   [G1:5]  Accepted (post-implementation ratification; decision already made + implemented + validated)
ADR-64   [G2:5]  Accepted — 2026-06-01, via AI Council debate (pick mode, 4-model panel + openai synthesizer, 2 rounds).
ADR-65   [G2:5]  Accepted — 2026-06-01, **Path A** (direct ADR refining ADR-64; no Council convene — ...).
ADR-66   [G2:5]  Accepted — 2026-06-01, **Path A** (operator-chosen; no Council convene — ...).
ADR-67   [G2:5]  Accepted — 2026-06-01, **Path A** (operator-chosen; no Council convene — a process
                 >>> VALUE CONTINUES ON LINE 6: "formalization of an already-running loop, not an architectural decision)."
ADR-69   [G2:5]  Accepted — 2026-06-02, **Path A** (operator-confirmed; post-hoc record ...).
ADR-70a  [G1:3]  Accepted — 2026-07-07 architect ratification session (operator ruling R4). Ratifies the addition of an **XL** routing tier ...
ADR-70b  [G2:5]  Accepted — 2026-06-02. AI Council verdict (2026-06-02) + the operator's three-tier synthesis. ...
ADR-71   [G2:5]  Accepted — 2026-06-03 (operator-confirmed). **Consumption contract VALIDATED** ... **Codemap deployment is NOT validated** ...
ADR-72   [G2:5]  Accepted — 2026-06-06 (operator-ruled, Path A of the #86.2 fork). Records **#86 sub-decision 2** ...
ADR-73   [G1:5]  Accepted — 2026-06-06 (ratification date)
ADR-74   [G1:5]  Accepted — 2026-06-06
ADR-75   [G1:5]  Accepted — 2026-06-06
ADR-76   [G1:5]  Accepted — 2026-06-06
ADR-77   [G1:5]  Accepted — 2026-06-06
ADR-78   [G1:5]  Accepted — 2026-06-07
ADR-79   [G1:5]  Accepted — 2026-06-07
ADR-80   [G1:5]  Accepted — 2026-06-07
ADR-82   [G1:3]  Accepted (ratified 2026-08-04 — architect adjudication; canonical since 2026-06-11 by operator waiver of the Council gate, #149. Status line edited in place per ADR-94 Pattern B ...)
ADR-88   [G2:5]  Accepted (ratified 2026-06-21 by operator edit; header flipped 2026-08-04 per ADR-94 Pattern B — see the 2026-08-04 amendment. ...)
ADR-89   [G2:5]  Accepted (ratified 2026-06-21 by operator edit; header flipped 2026-08-04 per ADR-94 Pattern B — see the 2026-08-04 amendment. ...)
ADR-91   [G2:5]  Accepted (ratified by merge 2026-06-29; baseline release `v1.0.0` tagged)
ADR-92   [G2:5]  Accepted (ratified by merge 2026-06-29)
ADR-93   [G2:5]  Accepted (ratified by merge; authored DURING the #226(b) build ...)
ADR-101  [G1:3]  Accepted (ratified 2026-07-11 — operator ruling via the 2026-07-11 morning verdict sheet [M1]; ...)
ADR-107  [G2:3]  Accepted (ratified 2026-07-28 — operator word, architect session)
ADR-108  [G2:3]  Accepted (ratified 2026-07-31 — operator word, relayed via the outgoing browser seat)
ADR-109  [G2:3]  Accepted (ratified 2026-07-31 — accepted by operator GO, architect session; ADR-94 status-line-only edit)
ADR-110  [G2:3]  Accepted (operator GO 2026-08-06, on SESSION PLAN v2 §3 — acceptance granted in-session)
ADR-111  [G1:3]  Accepted (operator ruling 2026-08-10 — seat-27 ruling checklist, Fork 1 = Option A: ratify AS WRITTEN, the §4 departure intact)
ADR-112  [G1:3]  Accepted (operator ratification 2026-08-12 — ruled TAK on the ARC2 packet, Q2)
ADR-113  [G1:3]  Accepted (architect ruling 2026-08-19, the L-5 rulings block delivered to the S-1 night-adjudication seat)
ADR-114  [G1:3]  **PARKED** — ruled by the operator 2026-08-22. *The priced options below are retained unchanged ...*
```

### Archive zone (2 files, 3 status fields)

```
ADR-40   [G5:5]   DEPRECATED 2026-05-23.**  (blockquote banner; value bleeds past the bold close onto 3 more lines)
ADR-40   [G3:10]  Deprecated (was: Accepted)
ADR-52   [G1:3]   ~~Accepted~~ Superseded by ADR-53 (2026-05-19)
```

**ADR-40 carries two status fields, in two grammars, at two casings** (`DEPRECATED` vs
`Deprecated`) — the only intra-file status disagreement in the corpus.

---

## Parser hazards this measurement found (each one is a test case in Step 3)

These are the cases that make a naive parser wrong, and the reason the count above is
trustworthy only because each was handled explicitly:

1. **`Status update` is not `Status:`** — `ADR-82:11` opens an amendment marker
   `> **Status update (in-place marker — ...)`. A regex treating the colon as optional
   swallows it as a *second, bogus* status field for ADR-82. The discriminator is that a real
   field has `Status` **immediately** followed by `:`. This false positive was live in this
   lane's own first measurement pass and was caught by inspection, not by the regex.
2. **The value can wrap across physical lines** — `ADR-67:5` ends mid-parenthetical and
   continues on line 6. A line-oriented parser silently truncates it and reports a
   well-formed-looking value that is not the real one.
3. **The key case varies** — `Status:` (86) vs YAML `status:` (ADR-61).
4. **The colon can sit inside or outside the bold** — `**Status:**` vs `**Status: value**`.
5. **The value can carry markup** — `**PARKED**` (ADR-114), `~~Accepted~~` (ADR-52). A raw
   equality test against `"Accepted"` fails on markup that does not change the meaning.

**`[#552]`'s recorded parser hazard is incomplete.** That row names three formats — "bold
`Status:`, list-item bold `Status:`, and YAML frontmatter". It **misses G3-plain, which 12 live
ADRs use** (ADR 34–39, 41, 42, 43, 45, 46, 47), and misses G5 entirely. A parser built to
`[#552]`'s stated hazard returns a false `None` on those 12, not just on ADR-61. Filed below.

---

## Collateral findings (measured, not acted on)

- **Two ADR numbers are used twice.** `ADR-51-architecture-doc-convention.md` +
  `ADR-51-amendment-2026-07-05-llm-first-canonical-docs.md`, and
  `ADR-70-three-tier-process-automation.md` + `ADR-70-amendment-2026-07-07-fable-xl-tier.md`.
  Both collisions are amendment-ADRs deliberately numbered onto their parent. This is a real
  ambiguity for any tool keying on ADR number, and it is **out of this lane's scope** — recorded
  so the next tool author does not discover it the hard way.
- **One filename uses underscores** — `ADR-43_cross_project_transcript_routing.md`, against the
  `ADR-NN-topic.md` convention in CLAUDE.md §4. Not status-related; recorded.
- **ADR-44 does not exist** in either zone. ADR-40 and ADR-52 are archived; 44 is simply absent.
