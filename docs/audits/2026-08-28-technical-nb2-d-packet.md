# NB2 · LANE D — [#612] doc-rot row-body archival — lane packet

**Batch:** night-batch-2 (architect lane id **N4**) · **Repo:** `.dev-knowledge` (hub)
**Branch:** `worktree-lane-d-612-docrot-archival` · **Substrate:** local · **Date:** 2026-08-29
**Status:** COMMIT-AND-STOP — not merged, not pushed, not journalled, no closure proposed.

**Headline:** `validate_doc_rot` **77 → 60**. Twenty rows drained, **zero content destroyed**,
proven twice by two independent instruments. The mechanism is
`scripts/archive_row_body.py`; the destination is `tasks/archive/` per operator decision D3.

---

## 1. Per-done-item verdict

### (1) `tasks/archive/` exists with a ruled write path — **MET**

`tasks/archive/` holds 20 records plus `README.md`. The write path is ruled at three levels,
each checkable:

| leg | witness |
|---|---|
| destination ruled | **D3** (operator, night-batch-2 GO 2026-08-28), cited verbatim at the `"tasks", "tasks/archive",` entry in `scripts/validate_hermetization.py` and at `tasks/archive/README.md` head |
| home admitted | `uv run --locked python scripts/validate_hermetization.py` → `RC=0` with the wave staged |
| write path mechanical | `scripts/archive_row_body.py` — `propose` / `relocate` / `verify` |

**Rule C refused it first, exactly as the contract predicted.** Witness, captured with the
wave staged and *before* the allowlist edit:

```
validate_hermetization: refused -- ADR-101 hermetization violation(s):
  tasks/archive/112.md: new path outside allowlisted homes -- operator approval required:
  'tasks/archive/' is not an admissible home for a new file. The repo's homes are derived
  from the live taxonomy (see _HOME_PATTERNS); a genuinely new one is an operator decision
  recorded as a ruling, not a drive-by add
```

The home was then admitted **in the same commit as the records**, narrowly, with the ruling
cited — **no `--no-verify`**. Admitted as the **bare literal** `tasks/archive`, not
`tasks/archive/*`: the tree is flat by construction, so a sub-directory stays a surfaced
act. Same narrowness `.devcontainer` carries, and the same `<parent>/archive` shape as
`protocols/archive`, `templates/archive`, `docs/decisions/archive`, `docs/intake/archive`.
**Rule A needed no amendment** — `tasks` is already in `SANCTIONED_TIER1_DIRS`, so this is a
home *below* an existing sanction, not a new top-level class.

### (2) `backlog-row-length` strictly reduced, no content destroyed — **MET**

**Strictly reduced:** `backlog-row-length` **68 → 55**. Whole surface **77 → 60**.

**No content destroyed — proven by two instruments that do not share a witness:**

*Proof A — the tool's five legs, re-derived from the tree:*
```
$ uv run --locked python scripts/archive_row_body.py verify
archive_row_body: OK - 20 record(s), 20 byte-identity PROVEN (legs A/B/C/D/E)
```

*Proof B — independent of the tool's own records, against the committed blobs at `main`.*
Reconstruct each row from **the live tree plus its archive record** and compare to
`git show main:<row>`. This never consults the recorded `body_before_sha256`; ground truth
comes from git, the one witness the tool did not write.
```
$ uv run --locked python <the script in §9> . main
git-identity-proof vs main: 20 byte-identical, 0 MISMATCH, 0 absent
```
(The script is reproduced verbatim at §9 so this claim stays re-runnable after the lane's
scratch directory is gone. Point it at `main`, not `HEAD` — once the lane commits, `HEAD`
*is* the relocated state and every row correctly "mismatches".)

Also asserted, not assumed: **zero CRLF** across every written file (`tasks/*.md`,
`tasks/archive/*.md`, the new script and test). All IO in the module is
`read_bytes` / `write_bytes` with strict utf-8, because `Path.write_text` launders LF→CRLF
on Windows and a `read_text` round-trip cannot detect that it did.

Per-row, read back out of the records themselves (bytes of the row body):

| row | before | after | delta | clauses |
|---|---|---|---|---|
| [#112] | 3119 | 1347 | −1772 | 1 |
| [#130] | 2137 | 975 | −1162 | 2 |
| [#139] | 1481 | 1045 | −436 | 1 |
| [#145] | 2338 | 1309 | −1029 | 2 |
| [#146] | 2622 | 1301 | −1321 | 2 |
| [#171] | 2359 | 627 | −1732 | 2 |
| [#218] | 1522 | 1261 | −261 | 1 |
| [#267] | 3071 | 2210 | −861 | 2 |
| [#277] | 2842 | 1357 | −1485 | 2 |
| [#294] | 1586 | 1228 | −358 | 1 |
| [#301] | 1552 | 1258 | −294 | 1 |
| [#308] | 1481 | 1249 | −232 | 1 |
| [#325] | 1770 | 1259 | −511 | 1 |
| [#420] | 1383 | 1196 | −187 | 1 |
| [#491] | 3773 | 2078 | −1695 | 2 |
| [#492] | 1902 | 1312 | −590 | 1 |
| [#533] | 2259 | 2107 | −152 | 1 |
| [#541] | 1781 | 1248 | −533 | 1 |
| [#555] | 1526 | 1381 | −145 | 1 |
| [#561] | 2423 | 2330 | −93 | 1 |
| **total** | **42 927** | **28 078** | **−14 849 (34.6 %)** | **27** |

No row was deleted, closed, re-sized or re-prioritised, and no derived frontmatter field
moved — `relocate` refuses on any change to title, status, priority, size,
`serialize-group` or `depends-on`. Every drained row keeps a path-qualified pointer as its
last clause.

### (3) P4 — the 77 figure re-measured BEFORE and AFTER — **MET**

| | result |
|---|---|
| BEFORE — dispatch, on `main`, 2026-08-28 23:36 | `validate_doc_rot: 77 doc-rot locus(es) past threshold` |
| BEFORE — re-witnessed in-lane on an untouched tree | `validate_doc_rot: 77 doc-rot locus(es) past threshold` |
| AFTER — last act | `validate_doc_rot: 60 doc-rot locus(es) past threshold` |

By family:

| family | before | after | note |
|---|---|---|---|
| `backlog-row-length` | 68 | 55 | −13 |
| `backlog-accretion` | 8 | 4 | −4 — the B1 class this drain targets |
| `grooming-cadence` | 1 | 1 | out of scope: a groom is an operator act, not a relocation |
| **total** | **77** | **60** | **−17** |

The BEFORE is **measured here, not inherited from the dispatch line** — it was re-witnessed
on an untouched tree after the naming revert at DEV-1, which restored the lane to `main`'s
exact row bytes before the wave was re-run.

### (4) Doctrine documented at the doc-rot home — **MET**

`scripts/validate_doc_rot.py`, module docstring, new section **"THE REMEDY DOCTRINE —
ARCHIVAL, NOT TRIMMING ([#612], 2026-08-28)"**. That is the honest home the contract's
RESOLVED LOCATORS named — the checker's own docstring, **not `protocols/`**, which was not
touched. It states the one-line doctrine (*the row carries a pointer; the record carries the
record*), grounds it in ruling **B1**, and adds the three consequences a reader who arrives
at a finding actually needs: a finding is not an accusation; relocation is not a closure;
and **this module stays DETECT-ONLY** — it calls nothing and the tool is wired into no gate.

Second home, for whoever runs the mechanism: **`tasks/archive/README.md`** — layout, the
naming rationale, the commands, the refusal set, the five proof legs, the honest limits, and
a recovery recipe.

### (5) The integrator's filing wave lands through this mechanism — **MET**

Built to be run by someone who did not read this reasoning: `propose` is read-only and is
the entry point; every refusal explains itself and names the gate it is protecting; the
eligibility rule and the minimum-gain rule are declared constants, not judgement calls.

Four rows remain proposable and are deliberately **not** taken here — see C-1.

---

## 2. Commits on this branch, in order

| # | sha | subject |
|---|---|---|
| 1 | `45ff9a74` | `feat(tasks): [#612] doc-rot row-body archival — relocation, not trimming (77 -> 60)` |
| 2 | `8d1bcf9b` | `fix(scripts): [#612] close the six terra findings on archive_row_body` |
| 3 | *this file's own commit* | `docs(audits): [#612] NB2 lane D packet` — the SHA cannot be written into the file it names; `git log --oneline -1` on this branch is it |

**No generated-surface regeneration was needed, and none was committed.**
`gen_task_tree.py --emit-source` reports `BACKLOG.md already current (208 task(s))` and
`--check` reports `check ok`. The [#589] one-line view renders id / band / title / DEFER /
pointer, none of which a *body* relocation touches, and every derived frontmatter field is
guarded by an explicit refusal — so there is no forced-regen commit to name.

---

## 3. Terra tally

Reviewer: `codex exec` over the lane diff (**not** `/codex-review` — a mixed doc/code diff
kills that lane). Reviewed at commit `45ff9a74`.

```
Critical: 1  High: 5  Medium: 0  Low: 0
```

**All six are closed at commit 2**, each with a test that fails without its fix. Three share
one root class — *a field rendered as proof but never read*.

| # | sev | finding | disposition |
|---|---|---|---|
| T1 | Critical | relocation not atomic — a writable record + an unwritable row left a record describing a row that was never changed | **FIXED** — snapshot both, roll both back on ANY exception incl. the post-write proof (`test_a_failed_post_write_proof_rolls_the_pair_back`) |
| T2 | High | a row already quoting the pointer literal got a duplicate pointer | **FIXED** — refused pre-write on `after.count(pointer) != 1` (`test_relocate_refuses_when_the_row_already_quotes_the_pointer`) |
| T3 | High | refusal set omitted `consumer=` / `consumption_path=` — the routine declaration's fields are their own clauses AFTER the marker, so a trailing one could be relocated out of a declared-routine row and break `check_routine_consumers` | **FIXED** — four field markers added; **and all 27 already-archived clauses were re-checked against the widened set: none is structural**, so the landed wave stands (`test_routine_declaration_fields_are_structural`) |
| T4 | High | `verify` had no completeness leg — deleting a record, or all of `tasks/archive/`, left the rows pointing at nothing and printed a clean empty "proven" | **FIXED** — new **LEG E** enumerates the live ROWS, so absence is a failure (`test_verify_fails_on_an_orphan_pointer_with_no_record`) |
| T5 | High | `parse_record` ignored declared event/clause counts, byte lengths and sequencing — deletion of a whole event or one clause block verified clean | **FIXED** — every rendered field is now parsed and compared (3 tests) |
| T6 | High | a corrupted post-relocation digest *disabled* leg C instead of failing it — one flipped hex character turned the check off and the run still exited 0 | **FIXED** — the reconstruction is attempted UNCONDITIONALLY; the post digest only classifies a failure (2 tests) |

T1 and T2 were also found by self-review before the tally arrived and were already fixed in
the working tree when it landed; recorded here as terra's because terra reported them
against the reviewed commit.

**Reviewer deviation, recorded rather than smoothed over:** the first `codex exec`
invocation ended mid-investigation without emitting a verdict; a monitor matched the
prompt's own echoed tally template rather than a real tally. The run was allowed to complete
and did emit the tally above. Its final narrative before the verdict — *"the durable-record
parser/validator is the higher-risk surface: several metadata fields are rendered as proof
inputs yet are not parsed or checked"* — is what became T5, and it was acted on before the
formal tally arrived.

---

## 4. Candidate filings for the integrator — REPORTED, NOT FILED

**C-1 — four rows remain proposable; every one is UNDER the ceiling, so none is a finding.**
```
$ uv run --locked python scripts/archive_row_body.py propose
  [#169]  1123 -> 625 chars  (1 clause(s))  under ceiling
  [#188]   856 -> 559 chars  (1 clause(s))  under ceiling
  [#298]   886 -> 819 chars  (1 clause(s))  under ceiling
  [#535]  1309 -> 1259 chars  (1 clause(s))  under ceiling
```
This lane scoped its wave to rows that are **currently doc-rot findings**. These four carry
dated narration but breach no declared contract, so draining them is *preventive*, not
*owed* — an integrator call, not an executor's.

**C-2 — INHERITED SUITE RED, not caused here, and this lane moved it toward green.**
`tests/test_validate_doc_rot.py::test_live_corpus_has_no_accretion_arm_findings_only_length_findings`
asserts the live corpus carries **zero** `backlog-accretion` findings. Evidence that it was
RED before this lane, measured against the `tasks/` tree **as committed at the merge base**,
without touching the working tree:
```
tasks/ tree at HEAD -- validate_doc_rot BACKLOG arms:
  backlog-accretion: 8  BACKLOG#145 #146 #171 #267 #276 #277 #297 #82
  backlog-row-length: 68
  TOTAL (both BACKLOG arms): 76
```
So: RED at 8 before the lane, RED at 4 after it. Its premise — the [#532] measurement that
"every live locus is a LENGTH finding" — went stale when ARM 1 acquired live members, and
the test is now an ownerless standing count assertion. Editing a pre-existing test is
outside this lane's write-scope and the contract says to report an inherited RED with its
evidence rather than fix it here. **Candidate:** re-pin or re-scope that assertion, and
decide whether ARM 1's live-member count deserves a declared ceiling of its own.

**C-3 — the four surviving `backlog-accretion` loci ([#145] [#146] [#267] [#277]) are drained but still fire.**
Each retains a *structural* clause that itself carries dates (`Done when:` / `refs` /
`kill-candidates:`), which the tool refuses to move by design. Relocation cannot clear
them; a disposition or an operator trim can. **Candidate:** disposition these four under
B1's trim-vs-disposition rule now that the narration half is gone.

**C-4 — `worth_relocating` has no reporting surface for sub-threshold rows.**
The minimum-gain rule ("a row must save at least what its pointer costs") is a declared
constant, but nothing lists rows that fall *below* it, so a row can accrete many small
dated clauses and never become proposable. Measured today: `[#457]` (+43 against a 48-char
pointer) is exactly that shape. **Candidate:** a `propose --all` mode that lists them.

**C-5 — `archive_row_body.py` is wired into no gate, deliberately.** `verify` is a CLI and a
test; it is not an `audit.py` check and not a pre-commit hook. That was the right default
for a lane that must not expand the gate mesh, but a mechanism whose whole value is a
standing proof is a natural gate candidate. **Candidate:** decide whether `verify` earns an
`audit.py` leg (it would need a check-name registration and an ALL_CHECKS count bump, both
of which are generated/pinned surfaces this lane must not touch).

---

## 5. Decisions taken under the V-2 budget

**D-a — Wave scope: rows that are CURRENTLY doc-rot findings.** Per defaults, no ask.
`propose` offered rows beyond the measured surface; the lane drained the intersection of
*proposable* and *currently a finding* and reported the rest as C-1. The contract's success
criterion is stated against the 77, and relocating a row that breaches no declared contract
is unrequested churn.

**D-b — Minimum gain is the pointer's own length, not a tuned constant.** Per defaults.
[#532]'s recorded lesson is that a percentile always has members, so no tuned number is a
rule; the pointer's length is self-scaling and cannot go stale.

**D-c — Retired rows are excluded from the drain.** Per standing rulings (ADR-107 §6.3),
silently. An unreferenced task file is an **allocation record** — out of `BACKLOG.md`, out
of `canonical_text`, therefore not part of the doc-rot surface. Measured: an earlier
unfiltered walk proposed four of them (`[#71]`, `[#122]`, `[#127]`, `[#296]`), none a
finding. Rewriting a frozen ledger record to shorten a row nobody reads would be tampering
with the one thing `tasks/` has to be trustworthy about.

**D-d — Records are named `<id>.md`, not `<id>-<slug>.md`.** Per defaults; a *correction*,
recorded in full at DEV-1 rather than smoothed over.

**D-e — Footprint beyond the literal write-scope line.** The frozen write-scope names
`scripts/validate_doc_rot.py` · `tasks/archive/` · `tasks/*.md`. Three files outside it were
written, each load-bearing for the contract's own text rather than scope creep:
* `scripts/archive_row_body.py` — the contract's §"THE MECHANISM" requires a mechanism the
  integrator can run, and it cannot live inside the detector without breaking that module's
  DETECT-ONLY contract (ADR-28/36).
* `scripts/validate_hermetization.py` — **explicitly authorized by the contract itself**:
  *"the operator's approval is the authorization to add that home to the allowlist in the
  same commit, narrowly, with the ruling cited."*
* `tests/test_archive_row_body.py` — a **new** file for the new module; ADR-108 §B binds a
  build arc to tests. **No pre-existing test file was edited** (see C-2).

`protocols/` was **not** touched (anti-pattern honoured; lane C holds the batch's only
ratchet authorization). No row was closed. No merge was performed or suggested.

---

## 6. Deviations, each with an owner

**DEV-1 (this lane; found and fixed in-lane) — the first record naming was wrong, and the
repo's own test caught it.** The first build named records `tasks/archive/<id>-<slug>.md`,
mirroring the row, which put the row's slug inside the *row's own pointer*. `[#492]`'s slug
ends `-2026-08-07-mea` — a date-shaped token that `validate_doc_rot._ARTIFACT_DATE_RE`'s
bare-bundle-name alternative strips as a citation for a handoff bundle that does not exist.
`test_citation_regex_strips_only_real_dated_artifact_identifiers` exists precisely to keep
that defect out of the canonical text — its own docstring names `[#492]` and
`2026-08-07-mea.md` for the one-line view — and it RED-ed on the first wave.
**Fix:** name records by id alone. **Remediation:** the entire wave was reverted
(`git checkout -- tasks/`, records deleted, BEFORE re-witnessed at 77) and re-run under the
corrected naming; the shorter pointer also brought `[#555]` and `[#561]` above the
minimum-gain threshold, so the second wave drained 20 rows rather than 18.
Owner: closed in-lane.

**DEV-2 (this lane; found and fixed in-lane) — `propose` still derived the pointer from the
ROW filename after the naming change**, so it charged the old, longer pointer against
`worth_relocating` and silently hid two eligible finding rows (`[#555]`, `[#561]`). Found by
diagnosing why four rows had left the proposal list. Owner: closed in-lane.

**DEV-3 (inherited) — one suite RED not caused here.** See C-2, with HEAD-tree evidence.
Owner: integrator / a follow-up row.

**DEV-4 (stated limits, not defects) — two, both pinned by tests so they cannot quietly
become claims of more.**
*(a)* Leg C can only PROVE a record while the live row is still the one the latest event left
behind. After a legitimate later edit the pre-relocation body is not derivable from the tree,
and *a legitimate edit* and *a corrupt record* are indistinguishable from the tree alone —
so `verify` reports **UNPROVEN**, states both readings, and names git at the relocation
commit as the witness that separates them. The headline counts what was PROVEN, so an
all-UNPROVEN run cannot read as clean. Pinned by
`test_verify_reports_unproven_not_failed_when_the_row_is_edited_later`.
*(b)* On a multi-event record, unwinding the chain in reverse reproduces every clause of the
original but its original ORDER only when nothing was appended between relocations — a limit
about order, never about loss. Pinned by
`test_a_chained_unwind_is_only_exact_when_nothing_was_appended_between_events`.
*(c)* Deletion is **detectable, not impossible**: the declared counts make removing an event
or a clause block a parse failure, but editing the counts to match defeats it. The durable
witness against that is git, and the module says so.

**DEV-5 (batch protocol, deliberate) — the session-end Stop hook's JOURNAL demand is
DECLINED, explicitly, and here is why.** A batch lane never journals; the integrator writes
one anchor for the whole queue after every lane has STOPped. ADR-85 amendment 2026-08-03 §A5
made that hook advisory in full, its hard leg is `block-unanchored-push` at pre-push, and
**this lane does not push**. Not silently ignored, not "fixed".

**DEV-6 (reviewer) — the first `codex exec` run ended without a verdict.** See §3. Recorded
rather than hidden; the completed run produced the tally.

---

## 7. Gate state at hand-back

| gate | result |
|---|---|
| `archive_row_body.py verify` | **OK — 20 record(s), 20 PROVEN (legs A/B/C/D/E)** |
| independent git byte-identity proof vs `main` | **20 byte-identical, 0 MISMATCH, 0 absent** |
| `validate_hermetization.py` (wave staged) | **RC=0** |
| `gen_task_tree.py --check` | **check ok** |
| `ruff check` (the four touched/added files) | **All checks passed** |
| `pytest tests/test_archive_row_body.py` | **45 passed** |
| targeted suite (archive + hermetization + doc_rot + gen_task_tree + validate_backlog) | **281 passed, 1 failed** — the failure is C-2's inherited RED |
| `silent_rule_detector.py` | **443 / 61 files / silent-rule-v5 — delta ZERO**, measured before the first commit and again before the last |
| pre-commit (commit 1) | every hook **Passed**, including `audit-health` and `validate-hermetization` |
| full suite | **NOT run** — [#528] / PLAYBOOK Ch5: the full suite runs once, at integration |
| CRLF audit over every written file | **none** |

---

## 8. What a reader should check first

If you verify one thing, verify §2's second proof — it is the only one whose ground truth
this lane did not author:

```bash
uv run --locked python scripts/archive_row_body.py verify
# then the script at §9, pointed at the merge base:
uv run --locked python <script> . main
```

If you verify a second thing, open `tasks/archive/171.md` beside
`tasks/171-build-the-conformance-dashboard-at-ecosystem-con.md`: that row went 2359 → 627
bytes and reads better for it, and the 1663-byte clause it lost is sitting in the record
with its own sha256.

---

## 9. The independent proof, verbatim

Reproduced here so §1 item (2)'s Proof B stays re-runnable after this lane's scratch
directory is gone. It is deliberately **not** landed in `scripts/`: it compares against a
named git rev, so it is a lane instrument, not an organ, and adding it would have moved the
generated codemap and organ index this lane must not regenerate.

```python
"""INDEPENDENT byte-identity proof: reconstruct each relocated row from the live tree +
its archive record, and compare against the row body as committed at a given git rev.

This does NOT trust archive_row_body's own recorded `body_before_sha256` — it takes the
ground truth from git, which is the only witness the tool did not write.
"""
import subprocess
import sys
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
REV = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
sys.path.insert(0, str(REPO / "scripts"))

import archive_row_body as arb  # noqa: E402
import gen_task_tree as gtt  # noqa: E402


def git_body(rel: str) -> str | None:
    out = subprocess.run(["git", "-C", str(REPO), "show", f"{REV}:{rel}"],
                         capture_output=True)
    if out.returncode != 0:
        return None
    return gtt.extract_body(out.stdout.decode("utf-8"))


ok = bad = missing = 0
for p in arb.record_files(REPO):
    rec = arb.parse_record(p)
    live = arb._row_body(REPO / rec.row_rel)
    got = live
    for ev in reversed(rec.events):
        got = arb.reconstruct_before(got, ev, rec.pointer)
    want = git_body(rec.row_rel)
    if want is None:
        print(f"  ?? [#{rec.task_id}] not present at {REV}")
        missing += 1
    elif got == want:
        ok += 1
    else:
        bad += 1
        print(f"  !! [#{rec.task_id}] MISMATCH vs {REV}: "
              f"reconstructed {len(got)} chars, committed {len(want)} chars")
        for i, (a, b) in enumerate(zip(got, want)):
            if a != b:
                print(f"     first divergence at char {i}: {got[i-40:i+40]!r} "
                      f"vs {want[i-40:i+40]!r}")
                break

print(f"git-identity-proof vs {REV}: {ok} byte-identical, {bad} MISMATCH, {missing} absent")
sys.exit(1 if bad else 0)
```

---

## 10. STOP

Branch `worktree-lane-d-612-docrot-archival` — committed, **not merged, not pushed, not
journalled**. It enters the integrator's frozen merge queue in that queue's own order.

---

## AMENDMENT 1 — 2026-08-29, same lane, before hand-back

> Appended, not edited in place: an audit artifact is immutable and is superseded by a new
> file or an **in-file amendment marker** (CLAUDE.md §5 rule 3). Everything above stands
> except where this section says otherwise.

**What prompted it.** Spot-checking a landed record (`tasks/archive/171.md`) showed its
static prose still saying *"the four legs"* — written before LEG E existed. Twenty committed
records were each carrying a sentence that misdescribed their own proof. That is precisely
the doc-rot class this lane exists to drain, sitting inside the drain's own output, so it
was fixed rather than noted.

**What changed.**

* `render_record`'s prose now names all five legs (A–E) and both honest limits.
* A new subcommand — **`archive_row_body.py rerender`** — re-emits every record's prose from
  its own parsed content. Twenty hand-edits would have been twenty unverifiable acts; this
  is one reproducible one. It is payload-preserving *by construction*: each record is
  re-rendered from what `parse_record` read out of it, then re-parsed and compared event for
  event, and **any** disagreement — or any raise — rolls the file back before the next is
  touched.
* All 20 records rerendered. Witnesses that only prose moved:
  ```
  archive_row_body: rerendered 20 record(s): [#112], [#130], ... [#561]
  archive_row_body: OK - 20 record(s), 20 byte-identity PROVEN (legs A/B/C/D/E)
  git-identity-proof vs main: 20 byte-identical, 0 MISMATCH, 0 absent
  git diff --stat -> 21 files changed, 107 insertions(+), 42 deletions(-)
  ```

**A defect the new test found, recorded because it is the interesting part.** The first
`rerender` put its rollback *after* the round-trip check. A renderer that drops a clause
makes the declared counts stop matching, so `parse_record` **raises** rather than returning
a disagreeing record — and the raise escaped past the rollback, leaving a mangled record on
disk. `test_rerender_rolls_back_if_it_would_change_content` caught it on its first run. The
rollback now wraps the whole round-trip. This is the same shape as terra's T1 (relocation
was not atomic) reappearing in new code written the same day, which is worth naming: a
"roll back on failure" that does not cover the *raising* failure is not a rollback.

**Amended figures.**

| | §7 said | now |
|---|---|---|
| `pytest tests/test_archive_row_body.py` | 45 passed | **47 passed** |
| proof legs named in each record's prose | four | **five (A–E)** |
| commits on this branch | 3 | **4** |

Unchanged and re-measured after the rerender: `validate_doc_rot` **60**;
`silent_rule_detector` **443 / 61 files, delta ZERO**; `archive_row_body verify` **20
PROVEN**; the independent proof vs `main` **20 byte-identical**.

**Commit 4** carries this amendment together with the `rerender` subcommand, its two tests,
the reworded records and the fixed rollback.
