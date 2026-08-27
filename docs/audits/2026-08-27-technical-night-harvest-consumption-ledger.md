# NIGHT-HARVEST CONSUMPTION LEDGER — 2026-08-26/27

**Purpose.** Every finding from the four night cloud reports, with the architect's verdict and its
destination. This file is the durability mechanism: if this chat or seat is lost, the next seat
executes THIS file and nothing from the night is dropped. Rejected items stay listed with their
reason — rejected is a recorded verdict, not a deletion.

**Sources (all in the operator's Downloads, all owed a byte-identical landing in `docs/audits/`):**
`CLOUD-NIGHT-C1-RESULT.md` (doc diet) · `CLOUD-NIGHT-C2-RESULT.md` (Python kodeks) ·
`CLOUD-NIGHT-C3-RESULT.md` (append-only rotation) · `CLOUD-NIGHT-C4-RESULT.md` (backlog census) ·
`CLOUD-NIGHT-MANIFEST.md` (harvest manifest).
Landing targets: `docs/audits/2026-08-27-technical-doc-diet-plan.md` ·
`-technical-python-kodeks-census.md` · `-technical-journal-rotation-recon.md` ·
`-technical-backlog-quality-census.md` · `-technical-night-harvest-manifest.md`.
Note for the landing lane: C1 and C3 open with one line of prose before the report's heading
(recorded in the manifest's Verification section) — land verbatim anyway, do not trim.

---

## A · Architect rulings taken 2026-08-27 (ADR-108 §A, technical, revertable)
Destination: `STANDING_RULINGS.md` new section (X), one line each.

| id | ruling | source |
|---|---|---|
| X1 | **Backlog order of operations is fixed:** `[#424]` (inert `_DEPID_RE`) lands FIRST → then the 17 inferred `depends-on` edges → then re-peg the 9 deferred rows whose pegs point into the kill list → ONLY THEN closures and the icebox sweep. Any other order orphans deferred rows. | C4 §3, §4 |
| X2 | **The 52-row active slice is adopted as a RANKING, not as a cap.** The census's own arithmetic shows a cap would admit rows born the same day while excluding five kill candidates older than 45 d, and leaves 30 unblocked P2s with no disposition. Ranking yes, cap no. | C4 §5 |
| X3 | **Python standard splits on enforceability (Option C).** Ruff-decidable clauses become an executable rule set + a fifth MUST-uniform parity surface; the three ruff-unrepresentable clauses stay doc-level intent. **No new hub checker for them** — a hub-hardcoded standalone checker lands as `absent` on consumers by measurement. | C2 §3, §4 |
| X4 | **The standard's three unrepresentable clauses are amended, not enforced:** Rich → operator-facing CLI output only (measured 1 of 135 files: the clause as written is fiction); Click → intent for NEW CLIs, no retrofit (13 of 78); dataclasses-over-dicts → intent (141 dict-returners). | C2 §1–2 |
| X5 | **Rotation rotates the FILE, not the PREDICATE (option a′).** `journal_anchor.journal_text()` tiles `JOURNAL.md` with sorted `JOURNAL-legacy-*.md`; the gates' universe is unchanged by construction. The seam lands first, moving zero bytes, needing no governance act. | C3 §5 |
| X6 | **Premise correction, recorded against the architect:** rotation is NOT a performance fix. After W2A it buys ~0.1 s of gate time. Its real case is context (736k tokens), grep, and merge collisions (21% of commits prepend at the same offset). Any row written against a performance premise is mis-specified. | C3 |
| X7 | **Doc diet sequencing:** the mechanical PLAYBOOK correction runs BEFORE any structural diet — it discharges 17 of the 19 `[#569]` census findings without moving a heading, and a structural pass run first would silently discard them. | C1 |
| X8 | **The night protocol is doctrine:** dispatch → sentinel → harvest → manifest → morning adjudication. Belongs in PLAYBOOK as a named protocol, with `Dispatch-After` and `Harvest-Cloud` as its two missing verbs (win-tooling, operator-owned). Harvest mechanics measured and working: `GET /v1/code/sessions/{id}/events`, paginated by `next_cursor`. | this window |

---

## B · Intakes owed (ADR-98/111 funnel — file, then birth)
| intake | carries | evidence |
|---|---|---|
| **I-DOC** documentation diet & PLAYBOOK census discharge | C1 R1–R4 (mechanical correction · H13/H15 v5→v6 re-stamp · ARCHITECTURE prose→functional+pointer per W2/D5 · Ch11/§5 relocation + ESSENTIALS pointerisation per R-F2) + the `[#569]` 19-finding census as consumed input | C1 landing path |
| **I-KODEKS** Python standard as an executable surface | C2 rows 1–4 (free ratchet of 12 zero-cost families · rule the three unrepresentable clauses per X4 · ruff rule set as a fifth parity surface · costed phase-in of T201/ANN/C901/PLR2004) + the `templates/ruff-config-block.toml:34-40` REPO-PERSONAL declaration that X3 supersedes | C2 landing path |
| **I-ROTATE** append-only surfaces rotation | C3 C-1 (tiling seam, depends on `[#587]`) · C-2 (ADR-29 amendment + ADR-39 registry entry + cross-doc reconciliation) · C-3 (one parameterised splitter, two surfaces) + **LESSONS.md at 303 entries against the ratified 300 trigger — tripped, nothing fired** | C3 landing path |
| **I-NIGHT** night-batch protocol (X8) | the protocol section + the two missing verbs + the harvest-manifest shape | this ledger |

---

## C · Immediate acts (not rows — do them in the governance session)
1. **`PLAYBOOK:610` carries a hard-coded secrets path** (C1 R1). Fix in the first doc act; do not wait for the diet.
2. **Land the five night artifacts** byte-identical + regenerate the audits index once.
3. **Register section X** (the eight rulings above).
4. **`[#424]` first** — it gates the whole backlog sequence (X1).

## D · Backlog acts, in X1's fixed order (governance session)
1. `[#424]` lands (inert `depends-on` parser).
2. Adopt the **17 inferred edges** (C4 §4) — takes declared dependencies from 4 → 21 rows; 13 rows become genuinely blocked, so "ready now" stops meaning "everything".
3. **Re-peg the 9 deferred rows** with spent/dead pegs: `[#325]` `[#294]` `[#308]` `[#139]` `[#169]` `[#188]` `[#218]` `[#301]` `[#492]`.
4. **Rule the top-40 kill list** (C4 §1) row by row against its counter-case. Standing sub-rulings:
   - `[#171]` and `[#244]`: **re-cut / split-and-close-the-shipped-half**, never a bare delete.
   - `[#269]`: settled by one `git show docs/audits/README.md` — cheapest verdict on the list.
   - `[#43]`: close only if intake #6 is re-anchored first.
   - `[#82]`: a ruling is owed before it can close from the hub at all — decision, not kill.
5. **Icebox sweep, 47 rows** (C4 §3), honouring the carve-outs: `[#210]` PROTECTED stays open;
   `[#242]` cannot move independently of `[#362]`.
6. **PROTECTED, never proposed:** `[#210] [#341] [#347] [#351] [#362] [#389] [#414] [#418] [#585]`.
7. Every ruled closure **refills the banked-births ledger** (currently 1 of 29) — this is how wave 3 gets its birth budget.

## E · Rejected — recorded, with the reason
| item | verdict | reason |
|---|---|---|
| 52-row cap as a hard cap | REJECTED as cap, kept as ranking | X2 — the census's own arithmetic falsifies it |
| A new hub checker for Click/Rich/dataclasses | REJECTED | X3 — lands as `absent` on consumers; measured, not assumed |
| Rotation justified on performance | REJECTED as premise | X6 — ~0.1 s after W2A; re-justify on context/grep/merge or not at all |
| Structural diet before the mechanical correction | REJECTED as sequencing | X7 — would discard 17 census findings silently |

## F · Open decisions the architect still owes (not lost, just unruled)
- Which of the 30 unblocked P2s below the ranking cut need a second disposition (C4 §5 note 3).
- `[#82]`'s hub-closability ruling (D.4).
- Whether `[#548]`/`[#559]`'s multi-edge dependencies imply a manifest-producer row that nobody owns (C4 §4 edges 6–11).

---
*Nothing in this ledger has been filed, born, or landed at the time of writing. Its execution is
the governance session that follows batch-W2 integration. If that session does not run, this file
is the complete statement of what is owed — it is the artifact, not the memory.*
