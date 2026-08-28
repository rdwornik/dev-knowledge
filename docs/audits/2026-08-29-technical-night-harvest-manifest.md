# NIGHT-BATCH-2 CLOUD HARVEST MANIFEST — 2026-08-28/29

Harvested read-only from the Anthropic cloud API
(`GET /v1/code/sessions/{cse_id}/events?sort_order=asc`, paginated by `next_cursor`), performed
here rather than by `Harvest-Cloud` because that verb is lane B's deliverable and had not merged
when the harvest ran — the mission's own fallback. All six sessions were COMPLETE at first wake
(C4 at +30 min; FM-C, the largest, at +55 min). No second sleep was needed. Nothing was written to
any repo by any cloud session; these six files are the only artifacts.

**Selection rule, encoded rather than assumed:** the report is the **LONGEST** assistant text, not
the last. The last is trailing Stop-hook backpressure noise from a container where
`uv run --locked` cannot start (`uv` 0.8.17 against the pinned `==0.11.19`). Written **verbatim,
UTF-8 without BOM**.

---

## Reports

| lane | file | bytes | assistant texts | report is # | byte 0 is `#` |
|---|---|---|---|---|---|
| C1 candidate triage | `NB2-CLOUD-C1-RESULT.md` | 25,230 | 10 | 2 | yes |
| C2 slow-marker evidence | `NB2-CLOUD-C2-RESULT.md` | 36,115 | 11 | 2 | yes |
| C3 intake-61 ratification | `NB2-CLOUD-C3-RESULT.md` | 42,570 | 10 | 2 | yes |
| C4 codex-surface census | `NB2-CLOUD-C4-RESULT.md` | 26,763 | 12 | 3 | yes |
| C5 README/VISION census | `NB2-CLOUD-C5-RESULT.md` | 46,524 | 10 | 2 | yes |
| FM-C full funnel census | `NB2-CLOUD-FMC-RESULT.md` | 32,953 | 10 | 2 | yes |

**Top recommendation, one line each:**

1. **C1** — dispositions the eleven batch-1 candidates **OWNED 2 · DISCHARGED 4 · CANDIDATE 5 ·
   REJECTED 0**, and collapses the five candidates into **at most three intake acts** (one ratchet
   policy, one SDA-1 admission instrument carrying three of them, one amendment joining the
   existing READY intake #59) rather than five rows.
2. **C2** — `[#598]`'s marker sweep was **already measured and STOPPED one day before the brief was
   frozen** (LONG-POLE at 21.42 % of worker-seconds; the lever is `[#597]`/W2A, not markers), yet
   the row is still `status: open`; the three deliverables ship as a design of record, and the
   substantive finding is that a *purely* durations-derived marker set cannot be regenerable.
3. **C3** — answers all five intake-61 questions options-and-consequences, deepest on q1 (which of
   assembler / probe gate / seal-identity / boot contract is *the engine*) and q2 (copy-with-hash
   vs pin-to-tag, on the asymmetry that a stale copy is detectable and a stale pin is not).
4. **C4** — **zero codex surfaces are REMOVAL-READY, zero bytes freed**, and the largest surface
   (168 artifacts, 630,460 B) is the **most** blocked: 166 of 168 are enumerated by filename inside
   two machine baselines that four live scripts read. The adversarial re-search **strengthened** the
   blocks.
5. **C5** — the README/VISION merge proposal, with both hard constraints (root `README.md` deleted
   2026-05-23; ADR-114 PARKED) quoted and respected up front, and the DANGLING set as the
   actionable output.
6. **FM-C** — **CONSUMED-AND-ARCHIVABLE = 0 corpus-wide over 951 objects, 100 % classified,
   UNCLASSIFIED = 0**; the archival mechanism has **zero backlog and zero mis-filings**; three
   intake docs are archivable only behind a **status ruling**, which is an operator act.

---

## PENDING

None. All six sessions had delivered before the harvest loop's second pass.

---

## Verification

- All six files are non-empty and byte-for-byte the session's own report text, UTF-8 without BOM.
- **All six satisfy "byte 0 is the report's own heading" literally** — a clean improvement on the
  2026-08-27 reference instance, where 2 of 4 wrapped themselves in a code fence behind one line
  of prose and the deviation had to be recorded instead. The fix was an explicit output-shape
  clause in the shared cloud brief, not a change to the harvester.
- **G1/G2 hard gates passed for all six at dispatch** (HTTP 200, id prefixed `session_`;
  `config.sources[0].type == git_repository` bound to `origin/main` @ `fcc9485`). G3 receipts
  landed in 21–72 s.
- **Every report ran the self-audit clause its brief demanded, and three overturned their own
  first pass**: FM-C cut a 19-orphan draft to 11 by keying on identifiers rather than filenames
  (a self-measured **42 % false-orphan rate**) and refuted one of its four archivable candidates by
  opening the file; C1 declined to claim OWNED for `[#591]` on the row alone; C4 re-searched with a
  second method and the blocks got stronger, not weaker.
- **Four premise defects in the briefs were found by the lanes themselves** and are carried into
  the ledger: FM-C's P1 (`tasks/` rows have **no `source:` field — 0 of 344**; `· refs …` is the
  de-facto one, 153/153 open rows), P2 (**the cloud clone is SHALLOW** — `.git/shallow` exists,
  history starts 2026-08-23, so `git log --diff-filter=A` returns the graft boundary for **835 of
  951 objects**; dated transitions came from frontmatter, never invented), P3 (the frozen bundle's
  in-tree name is `docs/audits/2026-08-28-technical-fm-wave2-frozen-bundle.md`, not the prompts-dir
  filename the brief cited — a defect this session introduced when it relocated the bundles out of
  the launch-contracts directory), and P4 (`docs/audits/` top level is **773** on the clone against
  the brief's 769 — the +4 this session's own dispatch commit added).
- **One attribution error against a lane, recorded rather than repeated:** C2 states that the
  brief's "WHAT TO GROUND IT IN" names `conftest.py`. It does not — `grep -i conftest` over
  `NB2-CLOUD-C2-slow-marker.md` returns nothing. The **substantive** half of that finding is true
  and useful: `tasks/598-*.md`'s own `refs` list carries `conftest.py`, and no `conftest.py` exists
  anywhere in the repo. The dead locator is real; its attribution to the brief is not.

---

## Landing — the six reports in the tree, byte-identical, md5-proven

Harvested filename -> committed path under `docs/audits/`, with the md5 that proves the copy moved
zero bytes. The audit-filename grammar `<date>-<class>[-<slug>]` picks the class per artifact:
a census is a `census`, a design/evidence report is `technical`.

| harvested | committed as | md5 |
|---|---|---|
| `NB2-CLOUD-C1-RESULT.md` | `2026-08-29-technical-nb2-candidate-triage.md` | `c95139f4a0eb77877d9f82e8bbdc4c99` |
| `NB2-CLOUD-C2-RESULT.md` | `2026-08-29-technical-nb2-slow-marker-evidence.md` | `c5f52dfacdb56ab6b9a6fc8beec0e089` |
| `NB2-CLOUD-C3-RESULT.md` | `2026-08-29-technical-nb2-intake61-ratification.md` | `9395ca83532c0593b7f43b2579238350` |
| `NB2-CLOUD-C4-RESULT.md` | `2026-08-29-census-nb2-codex-surface.md` | `3fca0709fb0c99fb7aa7f3e0b83166c5` |
| `NB2-CLOUD-C5-RESULT.md` | `2026-08-29-census-nb2-readme-vision.md` | `e0a61c25fdcda72d5cf8f604a1693f33` |
| `NB2-CLOUD-FMC-RESULT.md` | `2026-08-29-census-nb2-funnel.md` | `b74dadbac99ee4fb3426fc67fc17f361` |

Each md5 was computed on both sides of the copy and matched. Nothing was trimmed, re-wrapped or
re-headed — including the one place where trimming would have been tempting, which this year did
not arise because all six reports already start at byte 0 with their own heading.

## Session ids (read ids — the `cse_` form every read endpoint wants)

```
C1   cse_01CdseDXnBfKr2WErXyYVzqP   nb2-c1-candidate-triage
C2   cse_01N9YRqy2nfSkbDhknipqd8s   nb2-c2-slow-marker
C3   cse_01DW317CRUhjSLG87xiyrvjJ   nb2-c3-intake61
C4   cse_01WBswFKhVETzCGSKZz6KpKd   nb2-c4-codex-census
C5   cse_01LYCkMctQmJAi5xeu66uz1V   nb2-c5-readme-vision
FM-C cse_012N7sbwDaNqmvwLZ5knoY6n   nb2-fmc-funnel-census
```

The **ID TRAP** applies and was handled: create mints `session_<suffix>`, every read/manage
endpoint wants `cse_<suffix>`; feeding the minted id to a read returns 404, which reads as
"no such session".
