# ARTIFACT — LANE-ARCH: lifecycle archival, ADRs + audits (batch 1, lane C)

- **Lane:** `lane-arch-adr-audits` · branch `worktree-lane-arch-adr-audits` · repo `.dev-knowledge`
- **Contract of record:** `LANE-ARCH-adr-audits.md` (frozen, operator-supplied)
- **Backlog row executed:** `[#564]` — *Lifecycle archival — a pass over implemented ADRs and decided intakes, plus a check so archival cannot silently lag*
- **Date:** 2026-08-21
- **Scope split honoured:** ADRs + `docs/audits/` only. `docs/intake/**` (0/34) **untouched** — deferred to lane D per the contract's binding scope split.

---

## 0. Headline

**Zero files were moved. Both legs stop on their own governance, not on hesitation.**

| Leg | Eligible | Moved | Why |
|---|---|---|---|
| ADRs (`docs/decisions/`) | **0 of 86** | 0 | H3's bar is unmet on **both** of its halves — measured, not assumed |
| Audits (`docs/audits/`) | **leg stopped** | 0 | ADR-100 §1 rules audit files **never physically moved**; §3 gates any future move behind two preconditions this lane does not hold |

The operator demand behind `[#564]` was *archival EXECUTED*. What this lane executed is the
**measurement that decides what is archivable** — and the answer the repo returns is *nothing, yet*.
That is a substantive finding about `[#564]`, recorded in §5, not a lane that declined to work.

---

## 1. Per-class counts, before and after

| Class | Live location | Before | After | Archive location | Before | After |
|---|---|---|---|---|---|---|
| ADRs | `docs/decisions/ADR-*.md` | 86 | 86 | `docs/decisions/archive/` | 2 | 2 |
| Audits | `docs/audits/*.md` | 641 tracked (640 audit documents + `README.md`) | 641 | `docs/audits/archive/` | **does not exist** | **does not exist** |

`git mv` operations performed by this lane: **0**.

Measurement commands (run in the worktree, read-only):

```
ls docs/decisions/ADR-*.md | wc -l          -> 86
ls docs/decisions/archive/                  -> ADR-40-scale-tier-evaluation.md, ADR-52-agents-md-convention.md
git ls-files docs/audits/ | grep -c '\.md$' -> 641
ls -d docs/audits/*/                        -> (no subdirs under docs/audits)
```

The audits index header independently states **"640 audit documents."** — consistent: 641 tracked
`.md` files minus the generated `README.md` itself.

---

## 2. ADR leg — eligibility evidence

### 2.1 The bar

`protocols/STANDING_RULINGS.md` **H3**, quoted in full:

> A terminal-status ADR (`Superseded` / `Deprecated`) moves to `docs/decisions/archive/` when its
> inbound reference count is zero. A live prose reference elsewhere in the corpus holds it in place.

Two conjunctive halves: **terminal status** AND **zero inbound references**.

`[#564]`'s Done-when quotes only the second half (*"every ADR meeting H3's zero-inbound-reference
predicate"*). **Both readings were measured, and both return 0** — so the ambiguity is moot and no
judgment call was made on the operator's behalf.

### 2.2 Half one — terminal status: 0 of 86

Parsed with a three-format parser (bold `**Status:**`, bare `Status:`, and YAML frontmatter), because
`[#552]` records that a single-format parser returns a false `None` on ADR-61:

| Status value | Count | Terminal per the enum? |
|---|---|---|
| `Accepted` | 83 | no |
| `Partially superseded` | 2 (ADR-46, ADR-47) | **no** |
| `Explored, not adopted` | 1 (ADR-45) | **no** |
| `Superseded` | **0** | yes |
| `Deprecated` | **0** | yes |

This is not this lane's discovery — `docs/decisions/README.md` § *Status enum* already records it, and
is quoted here as the corroborating in-repo carrier:

> **H3's archival bar keys on `Superseded` / `Deprecated`**, two values that appeared on
> zero live ADRs, so the bar's trigger was unreachable by its own wording.

and, on where the two terminal members went:

> **Deprecated** (1 — ADR-40, archived), **Superseded** (1 — ADR-52, archived […])

Both terminal-status ADRs the corpus has ever carried are **already in `archive/`**. The enum's own
gloss confirms `Partially superseded` is non-terminal — *"still binding in part"* — against `Superseded`
— *"wholly replaced […] Terminal — eligible for `archive/` at H3's zero-inbound bar"*.

### 2.3 Half two — zero inbound references: 0 of 86

Scanned every `.md/.py/.yaml/.yml/.json/.toml/.txt/.html/.ps1` file in the worktree (excluding `.git`,
venvs, caches) for `ADR-NN` / `ADR_NN` / `ADR NN`, excluding each ADR's own file:

```
live ADR files scanned: 86
ZERO-INBOUND: 0
LOW-INBOUND (<=5 mentions): 0
```

**Not one live ADR has fewer than six inbound mentions.** The corpus is densely self-citing, which is
precisely the property H3's second half exists to respect.

### 2.4 The three non-`Accepted` ADRs, checked individually

Each is *also* named in the archival precedent itself, and each *also* fails the zero-inbound half today:

| ADR | Status line | Inbound today | Precedent's ruling (`216ce3a8` commit body) |
|---|---|---|---|
| ADR-45 | `Explored, not adopted; ADR-42 v3.2 remains canonical authority` | 245 mentions / 64 files (incl. `protocols/PLAYBOOK.md` ×3) | *"ADR-45 deliberately STAYS (PLAYBOOK prose refs fail the zero-refs bar)"* |
| ADR-46 | `Partially superseded — retained as convention, NOT audit-enforced` | 176 mentions / 68 files | *"ADR-46/47 stay (partially-superseded, retained as convention)"* |
| ADR-47 | `Partially superseded — retained as convention, NOT audit-enforced` | 203 mentions / 59 files | same |

The precedent's stated reason for ADR-45 is **still live and still true**: `protocols/PLAYBOOK.md`
carries three prose references to it today.

### 2.5 The precedent, quoted — and mirrored

Done-contract item 1 asks that the two existing archived ADRs be quoted and mirrored. Commit
`216ce3a8` (2026-07-22), the first and only decisions archival:

> `chore(decisions): archive ADR-40 (Deprecated) + ADR-52 (Superseded) to docs/decisions/archive/ (operator ruling 2026-07-22)`
>
> First decisions archival under the archive-inside-each-folder ruling; the path is proven:
> `scan_undeclared_edges` covers `archive/` via the `docs/decisions/` prefix
> (`scripts/scan_undeclared_edges.py:84`), `gen_claude_rosters --check` byte-unchanged (last-5 =
> 99-103), README ledger rows annotated with the archive location. ADR-45 deliberately STAYS
> (PLAYBOOK prose refs fail the zero-refs bar); ADR-46/47 stay (partially-superseded, retained as
> convention). **Byte-identical moves.**

Its mechanics, extracted as the shape this lane would have mirrored:

1. `git mv` into `docs/decisions/archive/` — git records `R100`, i.e. **byte-identical**, history preserved.
2. `docs/decisions/README.md` ledger rows annotated with the archive location **in the same commit**.
3. Generator check re-run and shown byte-unchanged.
4. Non-movers named in the commit body **with their reason**.

**Nothing to mirror it onto**: the eligible set is empty. The destination convention is settled and
needs no proposal — `docs/decisions/archive/` exists, is populated, and is reachable by
`scan_undeclared_edges`. There is **no `PROPOSED-PATH` item for this class**.

---

## 3. Audits leg — STOPPED, with governance quoted

### 3.1 The class has a convention, and the convention is "do not move"

`docs/decisions/ADR-100-audit-retention-index-rule.md` (**Accepted**, 2026-07-07), §1:

> Every accepted audit is **kept, unbounded**; audit files are **never physically moved, rolled up, or
> compacted.** Audits are the **evidence spine** — ADRs, LESSONS, transcripts, and the tooling cite them
> by path, and ~78% of those citations are in immutable/append-only files that can never be re-pointed.
> The storage cost is trivial; the referential cost of a move is permanent breakage. Keep-all is the
> deliberate, recorded call — not silent drift.

§2, on what "archive" means for this class:

> **Everything older moves to an archive *section of the index*** — **a section of the index, not the
> filesystem.** **Files never move; only their index grouping does.**

§3, the gate on any future physical move:

> Should a physical move of audit files ever be contemplated, it requires **both** a
> **referential-currency scan** (closing the known gap above — audit→audit + `ecosystem/*.yaml`) **and an
> explicit architect ruling.** Keep-all is the default precisely because the move is expensive and
> under-scanned.

ADR-100's own *Alternatives considered* rejects the exact act this leg would perform:

> **Physically move older audits to an `archive/` dir.** Rejected here and gated for the future (§3): no
> `archive/` dir exists, the move is under-scanned (the known gap), and ADR-36/ADR-60 cite the directory
> structurally — a move needs a full referential-currency scan **plus** an explicit architect ruling.

**This lane holds neither precondition.** It is not an architect seat, and its contract explicitly
forecloses the scan half (*"docs-only lane: no terra"*, no index regeneration, zero questions).

### 3.2 Corroborating carriers

- `BACKLOG.md` **[#552]** scopes the archival ratchet it specifies to `docs/intake/**` plus
  `docs/decisions/**`, *"with `docs/audits/**` and `docs/handoffs/**` **EXCLUDED by the ADR-100 keep-all
  ruling** and that exclusion stated in the check's own docstring so a future reader cannot mistake
  silence for an oversight."*
- `BACKLOG.md` **CONSIDERED + REJECTED** block: *"physical file moves for archival as the default (R2
  decides; convention says stay-in-place)"*.
- Cross-repo, corroborating not binding — `docs/handoffs/2026-07-19-ai-council-architect/PASTE_THIS.md`
  records *"Moving EPI-1 into `docs/audits/archive/` — rejected on three independent grounds"* under its
  own **CONSIDERED + REJECTED — do not relitigate** heading.

### 3.3 PROPOSED-PATH — `docs/audits/archive/` (and `docs/audits/archive/legacy/`)

Recorded per Done-contract item 2. **Archived nothing of this class. Zero invented paths.**

| Candidate | Governance basis, quoted | Status |
|---|---|---|
| `docs/audits/archive/` | `LESSONS.md:389` — *"Archive subfolder location follows artifact type, not generic grab-bag. […] `audits/archive/` for audits **if archival needed**."* Conditional by its own wording, and a lesson, not a ruling. | **`PROPOSED-PATH` — BLOCKED** by ADR-100 §1; unblockable only via §3's two preconditions |
| `docs/audits/archive/legacy/` | Executed convention **in the `ai-council` repo**, not here — `docs/audits/2026-05-23-ai-council-deep-audit.md` I6: *"2 legacy `_CODE_REVIEW_REPORT.md` to archive — **CLOSED** — moved to `docs/audits/archive/legacy/`"*; also `docs/audits/2026-07-11-technical-fleet-parity-register.md`. Verified **not** present in `.dev-knowledge` (`ls -d docs/audits/*/` → no subdirs). | **`PROPOSED-PATH` — BLOCKED**, same gate; additionally a cross-repo import, which is a fleet-parity decision, not a lane's |

**What would unblock this leg, stated so the next seat does not re-derive it:** (a) a referential-currency
scan that closes ADR-100's own declared gap — audit→audit cross-references and `ecosystem/*.yaml`, neither
of which the 125-citation/42-doc figure covered, so those figures are *"a floor, not a ceiling"*; and
(b) an explicit architect ruling. Both, not either.

### 3.4 Eligibility grading was not performed, and why

The contract's audit-eligibility test — *findings transcribed into rows, verified, row ids cited in the
move commit* — was **not run over the 640 audit documents**. It is moot: item 2 stops the leg at the
destination question, and a per-file eligibility grade whose only possible consequence is a move that
governance forbids would be work presented as evidence for a decision it cannot inform. Recorded as a
deliberate omission rather than left as a silent gap.

---

## 4. Dangling-reference check (Done-contract item 4)

Item 4 binds *"any index/reference to a moved file"*. **Zero files moved, so the obligation is
vacuous** — but the grep is shown rather than asserted, because the reference census is the same
measurement the ADR leg turns on:

```
$ python temp/inbound_scan.py        # read-only; transient scratch, REMOVED per CLAUDE.md §5 rule 9
live ADR files scanned: 86
ZERO-INBOUND: 0
LOW-INBOUND (<=5 mentions): 0

$ grep -rn "audits/archive" --include=*.md --include=*.py --include=*.yaml .
  -> 13 hits across 11 files (this artifact excluded), ALL of them prose ABOUT the
     ai-council repo or ABOUT rejecting the move. ZERO are a live .dev-knowledge path.
     Directory confirmed absent by `ls -d docs/audits/*/`.
```

No index was regenerated (`docs/audits/README.md` is the integrator's, once — per contract).
`docs/decisions/README.md` was not edited: its ledger annotates *archived* rows, and no row changed class.

**The scan is reproducible without the deleted script**, which is why its predicate is stated rather than
only its output: for each of the 86 `docs/decisions/ADR-*.md`, count `re.findall(r"ADR[-_ ]0*<N>")`
across every `.md/.py/.yaml/.yml/.json/.toml/.txt/.html/.ps1` file in the tree (excluding `.git/`, venvs,
caches, `temp/`), skipping the ADR's own file. Zero-inbound ⇒ 0; minimum observed ⇒ 6.

---

## 5. Finding for `[#564]` — reported, not acted on

`[#564]`'s half (a) is *"a one-time pass archiving what qualifies under the existing convention."*
Measured, **what qualifies is the empty set**, and for two structurally different reasons:

- **ADRs** — the bar is reachable but unmet. Nothing is `Superseded`/`Deprecated` **because nothing ever
  writes those values**; supersession happens in ADR *prose* and in `README.md` ledger strikethrough
  (ADR-45's ledger row reads `~~…~~ Superseded by …` while its status line reads `Explored, not adopted`)
  but never in the field H3 keys on. `[#552]` already names this exact limit — *"leg (a) cannot fire on an
  ADR whose supersession was never written into its status line, which is the live corpus's actual state
  — that gap is `[#242]`'s status half plus `[#362]`'s substantive half"*. **This lane did not flip any
  status line**: `[#564]` itself rules *"no ADR is superseded […] by this row."*
- **Audits** — the bar is not reachable at all. ADR-100 decided the opposite of archival for this class.

**Consequence the operator may want to weigh:** `[#564]`'s half (a) as scoped to ADRs + audits is
**already complete and always was** — 2-of-86 was never a backlog of un-archived terminal records, it was
the correct output of the bar applied to a corpus with two terminal records. The complaint's real
referent is more likely the **intake** class (0 archived of 34, 16 `ACCEPTED`), which is lane D's, and the
**status-line gap** above, which is `[#242]`/`[#362]`'s. Half (b) — the lag check — is unaffected and
still worth building; `[#552]` already specifies it, correctly excluding `docs/audits/**` per ADR-100.

**One stale census observed, NOT fixed** (it belongs to `[#553]`, which owns the ADR census in
`decisions/README.md`): the Status-enum block states *"across the 86 ADR files in this folder and
`archive/`"* with `Accepted` at 81 — a 2026-08-12 measurement. Today it is **88 files (86 live + 2
archived)** with `Accepted` at **83**. The drift is +2 `Accepted` ADRs added since, so it moves no
archival verdict: the terminal-status count it reports as zero is still zero. Recorded, not edited.

Reported here per the contract's zero-questions budget. **No BACKLOG, `tasks/`, §Q or PLAYBOOK edit was
made.**

---

## 6. Nothing-touched list

Verified untouched by this lane:

- `docs/intake/**` — contract-forbidden (lane D); **0 reads that could mutate, 0 writes**
- `docs/audits/**` — 0 moves, 0 edits; `docs/audits/README.md` **not regenerated** (integrator, once)
- `docs/decisions/**` — 0 moves, 0 edits; `docs/decisions/archive/` unchanged at 2 files
- `docs/decisions/README.md` — not edited
- `BACKLOG.md`, `tasks/**` — not edited
- `protocols/STANDING_RULINGS.md` (incl. §Q), `protocols/PLAYBOOK.md` — read-only, not edited
- `.pre-commit-config.yaml`, `.gitignore` — not edited
- `JOURNAL.md` — not edited (a batch lane does not journal; the integrator does)
- No merges, no deletions, no branch operations beyond this lane's own commit

Two files are added by this lane and nothing else:

- `ARTIFACT-lane-arch.md` (this file) — the contract-named deliverable
- `temp/inbound_scan.py` — the read-only measurement script; `temp/` is gitignored (`.gitignore:107`), so it is **not committed** and leaves no residue

One environment change, declared because it is a change even though it is not a tracked one: the lane
venv (`.venv/`, gitignored) was provisioned with `uv sync --locked --group analytics`, installing
`pandas`/`numpy` from the **existing** lockfile. `uv.lock` and `pyproject.toml` are **untouched** — no
dependency was added, an already-declared optional group was installed into a lane venv that lacked it.

---

## 7. Gate results

| Gate | Result | Detail |
|---|---|---|
| `pytest` (full suite) | **3 RED**, every one reproduced on a pristine tree with the artifact removed — **none this lane's**. 17 further REDs were an unprovisioned lane venv and are now green. | §7.1 |
| `python scripts/audit.py health` | **`health: OK`** — gate GREEN, every hard-fail organ passed | §7.2 |
| New WARNs of this lane's making | **exactly 1** (46 → 47, isolated by name): `fleet_parity` root-sweep on the artifact's own contract-frozen root path. **Zero** new WARNs in `docs/decisions/**` or `docs/audits/**`. | §7.3 |
| Commit gate | one **declared** single-hook bypass, `SKIP=validate-hermetization`, per Q1. `--no-verify` NOT used. | §7.4 |

### 7.1 pytest — 3 REDs, all pre-existing, none this lane's

Full suite, lane venv, `-n auto`: **20 failed / 3111 passed / 11 skipped / 1 xfailed in 1086s (18m06s)**.
(The shell reported `exit code 0`; that is the *pipe's* code, not pytest's — the summary line is the record.)

**17 of the 20 were an unprovisioned lane venv, not a defect.** `tests/test_fleet_analytics.py` failed
17× with `ModuleNotFoundError: No module named 'pandas'`. Fixed by the documented lane-setup step
`uv sync --locked --group analytics` (installs a declared optional group from the existing lockfile —
**no dependency was added, `uv.lock` is untouched**). Re-run: `tests/test_fleet_analytics.py` → **64 passed**.

**The remaining 3 were proven not-mine by removal, not by argument.** The artifact was moved out of the
tree (`git status` → clean, zero untracked), and the three were re-run isolated (`-n 0`):

```
$ git status --short          # nothing — pristine tree, artifact removed
$ pytest -q -p no:randomly -n 0 <the three tests>
FAILED tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row
FAILED tests/test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent
FAILED tests/test_stale_worktrees.py::test_linked_worktrees_reader_excludes_the_primary
3 failed in 8.96s
```

Identical failures on a tree this lane had not touched. Their causes, named so they are not re-diagnosed:

| Test | Cause | Class |
|---|---|---|
| `test_stale_worktrees::…excludes_the_primary` | `aud._REPO_ROOT` **is** a linked worktree here, so the "primary" it excludes is this lane | structural lane-worktree RED |
| `test_enforcement_coverage::test_anchor_gate_probe…` | the pre-push organ refused an *anchored* probe push too — a constant refusal, the lane-tree-lag class (the lane's `JOURNAL.md` lags main's spine) | lane tree-lag |
| `test_audit::test_routine_consumers…exactly_one_row` | live-`BACKLOG.md`-coupled: the test pins 1 routine row, the live backlog now declares **3**. `audit.py` itself reports this state `[OK]` | pre-existing test/corpus drift; **this lane did not touch `BACKLOG.md`** |

### 7.2 audit.py — `health: OK`

`python scripts/audit.py health` → **`health: OK`**. The gate is GREEN; every hard-fail organ passed
(`journal_spine_anchor` OK, `fleet_audit_replication` OK at 0 ahead, `task_tree_coherence` OK,
`intake_tree_coherence` OK, `silent_rule_ratchet` live **440 ≤ baseline 441**).

`audit.py run` was **deliberately not used**: it *"writes a report to `docs/audits/`"*, i.e. it would add
a file to the very class this lane is forbidden to touch. `health` is the check set the `audit-health`
pre-commit hook carries, so it is the gate the contract's "green" means.

### 7.3 New WARNs — exactly one, and it is this lane's

Measured by differential, not asserted: **46 WARNs unstaged → 47 with the artifact staged.** The delta
was then isolated by name rather than inferred:

```
[~~] fleet_parity: .dev-knowledge root-sweep WARN-undeclared:
     top-level entry 'ARTIFACT-lane-arch.md' is not in the template for role 'hub'
```

**That is the one new WARN of this lane's making, and it is caused solely by the artifact's
contract-frozen location.** No WARN was introduced in `docs/decisions/**` or `docs/audits/**` — the two
trees this lane was scoped to — because nothing in them changed. The other 46 are pre-existing and
untouched (BACKLOG row-length `doc_rot`, the 21-day grooming cadence, 18 ADR-88 `undeclared_edges` prose
edges, `journal_spine_anchor` anchored-by-mention, `review_artifact_coverage`).

### 7.4 The root-path collision — TWO gates object, and the bypass is declared

The contract freezes the artifact's path **and** filename (*"`ARTIFACT-lane-arch.md` (worktree root)"*).
The repo root is a **sealed set**, and two independent surfaces say so:

1. **`validate-hermetization` Rule A — BLOCK** (pre-commit). Verified by calling the classifier directly
   rather than by predicting it:
   ```
   >>> validate_hermetization.rule_a_violation('ARTIFACT-lane-arch.md')
   "unsanctioned new top-level file 'ARTIFACT-lane-arch.md' -- Tier-1 files are a closed
    class (ADR-101 section 1); a genuinely new class is an ADR-101 amendment, not a
    drive-by add"
   ```
   `SANCTIONED_TIER1_FILES` is a closed frozenset: 7 living docs + dotfile/tool config + build manifests.
2. **`fleet_parity` root-sweep — WARN** (§7.3 above). Same verdict from the fleet-template axis.

The available moves were: relocate the file (violates the frozen contract), edit the gate (contract
forbids `.pre-commit` edits), or **declare the bypass**. The third is the sanctioned instrument —
`protocols/STANDING_RULINGS.md` **Q1**:

> the integrator is gate-of-record, and a declared single-hook bypass on a lane branch is sanctioned,
> with the declaration carried in the commit body.

**Declared: `SKIP=validate-hermetization`, one hook, one commit, on a lane branch, declared in the commit
body.** `--no-verify` was **not** used — every other hook, including `audit-health`, ran and passed.

**Open for the integrator, who is gate-of-record.** Two gates independently refusing this path is a
signal, not noise: the artifact probably should not remain at the repo root. The honest options are
relocation into `docs/audits/` under the ADR-101 `<date>-<class>-<slug>.md` grammar (which would also
retire the WARN), or deletion once its content is consumed at integration. **Neither is a lane's call**,
and this lane invented no path in either direction.
