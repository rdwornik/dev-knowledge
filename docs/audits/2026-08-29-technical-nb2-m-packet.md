# NB2 · WAVE 2 · LANE M packet — FPG-1: the file-purpose graph, first slice (A3)

**Batch:** night-batch-2, wave 2 · **Lane:** M · **Substrate:** local
**Branch:** `worktree-lane-m-1-fpg-file-purpose-graph` · **Merge-base:** `77096131`
**Contract:** `docs/audits/2026-08-28-technical-fm-wave2-frozen-bundle.md` §FPG-1
**Consumers:** `[#595]` (its citation machinery is input 3 of this graph), `ADR-106` (the
dependency act), `ADR-88`/`ADR-89`+`[#194]` (the doc→code edge this graph joins),
`protocols/STANDING_RULINGS.md` R-A (the rustworkx reservation this lane consumes).

---

## 0. THE EX-ANTE, VERBATIM — then the measured result

> **Ex-ante:** `why` answers correctly on 3 named governed files (witnessed transcripts) and
> FAILs on a planted unknown.

**MET.** Four witnessed transcripts below (three governed files of three genuinely different
kinds, plus both refusal flavours), pasted as produced rather than described.

### Witness 1 — a GENERATED surface

```
> uv run --locked python scripts/file_purpose_graph.py why docs/audits/README.md --limit 4
path     : docs/audits/README.md
node     : file:docs/audits/README.md
purpose  : Audits index — generated navigation map of `docs/audits/`

consumers (0) -- what reads this
  (none)

edges (787) -- what this reads / is coupled to
  - indexes              file:docs/audits/2026-03-30-dev-practice-os-state-audit.md [audits-index]
  - indexes              file:docs/audits/2026-04-21-corp-monorepo-operating-model-analysis.md [audits-index]
  - indexes              file:docs/audits/2026-04-21-council-27-brief.md      [audits-index]
  - indexes              file:docs/audits/2026-04-21-dev-knowledge-inventory.md [audits-index]
  ... 783 more not shown (--limit 0 for all; the count above is the evidence)
```

`consumers (0)` is a TRUE answer, not a thin one: none of the five inputs reads this index.
Its real consumers — the `audit-index-freshness` pre-commit hook and `CLAUDE.md` §9 — are
outside the frozen input list. Filed as candidate C-2 rather than quietly widened.

### Witness 2 — a HAND-AUTHORED canonical doc

```
> uv run --locked python scripts/file_purpose_graph.py why protocols/PLAYBOOK.md --limit 6
path     : protocols/PLAYBOOK.md
node     : file:protocols/PLAYBOOK.md
purpose  : Dev Practice Playbook

consumers (11) -- what reads this
  - declares             rule:canonical-freshness                             [doc-code-edge]
  - declares             rule:coherence-amendment                             [doc-code-edge]
  - declares             rule:coherence-doc-claims                            [doc-code-edge]
  - declares             rule:coherence-doc-rot                               [doc-code-edge]
  - declares             rule:coherence-doc-structure                         [doc-code-edge]
  - declares             rule:coherence-spec-reconciled                       [doc-code-edge]
  ... 5 more not shown (--limit 0 for all; the count above is the evidence)

edges (17) -- what this reads / is coupled to
  - consumes             file:docs/audits/2026-05-11-ai-council-scrum-master-review.md [consumer-at-landing]
  - consumes             file:docs/audits/2026-05-19-dev-knowledge-posture-audit.md [consumer-at-landing]
  - consumes             file:docs/audits/2026-06-05-conformance-nightly-digest.md [consumer-at-landing]
  - consumes             file:docs/audits/2026-06-05-living-doc-staleness.md  [consumer-at-landing]
  - consumes             file:docs/audits/2026-06-07-platform-max-audit.md    [consumer-at-landing]
  - consumes             file:docs/audits/2026-07-06-changelog-review.md      [consumer-at-landing]
  ... 11 more not shown (--limit 0 for all; the count above is the evidence)
```

### Witness 3 — a SCRIPT

```
> uv run --locked python scripts/file_purpose_graph.py why scripts/session_end_backpressure.py --limit 8
path     : scripts/session_end_backpressure.py
node     : file:scripts/session_end_backpressure.py
purpose  : #8 Stop-hook session-end backpressure + ADR-85 gate.

consumers (1) -- what reads this
  - is shipped by        component:session-end-backpressure                   [deploy-manifest]

edges (1) -- what this reads / is coupled to
  - enforces             rule:seal-journal-anchor                             [doc-code-edge]
```

### Witness 4 — THE REFUSAL, both flavours, exit code shown

```
> Set-Content scripts/_fpg_planted_unknown.py -Value 'x = 1'
> uv run --locked python scripts/file_purpose_graph.py why scripts/_fpg_planted_unknown.py
REFUSED: scripts/_fpg_planted_unknown.py: nothing explains this file. It is on disk and no
governed input (doc-code-edge registry, audits index, consumer-at-landing citation, tasks/
depends-on, deploy manifest) names it. A file nothing explains is a defect, not a mystery.
exit code: 1

> Remove-Item scripts/_fpg_planted_unknown.py
> uv run --locked python scripts/file_purpose_graph.py why scripts/_fpg_planted_unknown.py
REFUSED: scripts/_fpg_planted_unknown.py: no such path in this repo (nothing to explain).
exit code: 1
```

The planted file was removed and its removal verified (`git status --porcelain` clean of it;
`ls` reports no such file) — no leftovers.

### Bonus witness — why the LIBRARY earns its place

```
> uv run --locked python scripts/file_purpose_graph.py why protocols/DEFINITION_OF_DONE.md --depth 2 --limit 6
consumers (2) -- what reads this
  - declares             rule:seal-journal-anchor                             [doc-code-edge]
  - declares             rule:seal-journal-spine-anchor                       [doc-code-edge]

transitive consumers (6) -- any depth
  - component:session-end-backpressure
  - file:scripts/audit.py
  - file:scripts/block_unanchored_push.py
  - file:scripts/session_end_backpressure.py
  - rule:seal-journal-anchor
  - rule:seal-journal-spine-anchor
```

`rustworkx.ancestors` over the JOINED graph reaches three enforcing organs and a deploy
component two and three hops out, through nodes no single input shares. That is the query the
five separate surfaces cannot answer at all.

---

## 1. PER-DONE-ITEM VERDICTS

### D1 — verify the two facts R-A left open · **MET**

| half | result | witness |
|---|---|---|
| prebuilt Windows wheels + CI matrix (externally witnessed by the architect) | **re-confirmed locally** | `uv.lock` pins `rustworkx-0.18.1-cp310-abi3-win_amd64.whl` by sha256 — a prebuilt abi3 wheel, no sdist, no Rust toolchain |
| installability under pinned uv 0.11.19 (MEASUREMENT-OWED-LOCAL) | **PASS** | `uv lock` → `Resolved 35 packages; Added rustworkx v0.18.1`; `uv sync --locked` → `Installed 2 packages: numpy==2.5.1, rustworkx==0.18.1`; import witness `rustworkx 0.18.1` on `3.12.10 [MSC v.1943 64 bit (AMD64)]` |

**The fallback was NOT taken.** R-A's sqlite/stdlib edges with a swap-ready seam were the
contingency for a failed measurement; the measurement passed, so library-first ran in the
direction the evidence pointed. There is no measured divergence to record because there is no
divergence — the evidence is above rather than asserted.

**Transitive cost, stated rather than discovered:** rustworkx requires numpy. numpy was
ALREADY in `uv.lock` (via pandas), so the lock gains ONE package, not two — but numpy moves
from the opt-in `analytics` group into the DEFAULT `dev` group, so a plain `uv sync --locked`
now installs it where it previously did not.

### D2 — the dependency act, done the ruled way · **MET**

`pyproject.toml` → `uv lock` → `uv sync --locked`, committed together as `cdccaafa` with the
operator's A3 mandate quoted verbatim in the commit body as the authorization. No `uv add`
into a drifted lock, no bare `pip install`, and the `uv` pin (`==0.11.19`) is untouched.
**No `ecosystem/dependency-baseline.yaml` row** — the pandas / packaging / markdown-it-py
precedent: the graph is HUB-ONLY and ships in no carrier and no manifest component roster, so
it is not a dep a consumer needs to operate a methodology mechanism, which is what that
surface governs.

### D3 — resolve all five inputs, record real path and shape and edge type · **MET**

| # | input, at its real path | shape read | edge types contributed |
|---|---|---|---|
| 1 | `ecosystem/doc-code-edge.yaml` | `declaration_docs:` list (4 docs) + `<!-- rule: ID -->` in those docs + `# rule: ID` comment tokens under `scripts/` | `enforces` (organ → rule), `declared-in` (rule → doc) |
| 2 | `docs/audits/README.md` | generated month-grouped rows `- [date](target.md) — Title` | `indexes` (index → artifact) |
| 3 | `[#595]` citations, `scripts/consumer_at_landing.py` | audit corpus recursive under `docs/audits/` minus `README.md`; governance pool = `POOL_DIRS` + `POOL_ROOT_FILES`; four citation forms | `cites` (artifact → row/ADR/register/intake), `consumed-by` (pool file → artifact) |
| 4 | `tasks/**` (346 rows) — **SOURCE OF TRUTH, `BACKLOG.md` never read** | YAML frontmatter (`id`, `title`, `depends-on`, `generates`) + the body row's `· depends-on: …` clauses; plus `tasks/archive/NNN.md` records | `depends-on` (row → row), `generated-from` (view → row), `archives` (row → archived body) |
| 5 | `deploy/manifest-v1.4.0.yaml` (highest version, not a union across releases) | `carriers[].target.{source_path,source_paths,doc_paths}`, `components[].{carrier,artifacts[].source,adr}` | `carrier-source`, `ships`, `carried-by`, `governed-by` |

Live contribution, machine-counted (`stats`), so no input is asserted to work:

```
nodes    : 1646
edges    : 10606
  doc-code-edge          45
  audits-index           787
  consumer-at-landing    9345
  tasks-depends-on       385
  deploy-manifest        44
```

`tests/test_file_purpose_graph.py::test_live_repo_builds_and_carries_all_five_inputs` asserts
every one of the five actually contributed, so an input that silently stops resolving FAILS
rather than thinning the graph unnoticed.

### D4 — the `_parse_deps` trap: say which you did · **MET — I wrote my own, and here is the divergence**

I reuse `validate_backlog`'s REGEXES (`_DEPENDS_CLAUSE_RE`, `_DEPID_RE` — imported, never
re-derived) but apply **`finditer()`** where that helper applies `search()`, and I additionally
read the frontmatter `depends-on:` key. So **I can see edges the rest of the repo cannot**, in
two ways, both pinned by tests
(`test_multi_target_depends_on_reads_every_id_in_the_clause`,
`test_frontmatter_depends_on_is_read_too`).

**Measured on the live tree, 2026-08-29: the two readings AGREE.** 28 files carry a
`depends-on`; no row carries a SECOND body clause today, so multi-target edges are all written
as one comma-separated clause exactly as the trap predicts. The divergence is **latent, not
active** — which is the honest statement, and it is why the tests exist: they pin the
difference so it cannot regress into an accidental match.

### D5 — `why <path>`: purpose + consumers + edges, FAILing on unknown · **MET**

Section 0. Three answers per governed path, two distinguished refusal flavours, exit 1 on
either. `UnknownFile.exists` separates "on disk and nothing explains it" (the governance
defect) from "no such path" (a typo or stale locator) — genuinely different facts with
different fixes, so they are not collapsed.

### D6 — RED-first, the refusal built first · **MET — two witnesses, in order**

| stage | result | what it proves |
|---|---|---|
| module absent | collection error, 0 tests ran | that the file is missing. A WEAK red — nothing discriminates |
| **STUB present, `why` answers EVERY path** | **`21 failed, 3 passed`**, all three refusal tests reporting `Failed: DID NOT RAISE UnknownFile` | **the discriminating RED** — the assertion refuses a stub that looks like the real thing |
| real module | `25 passed in 28.79s` | GREEN after |
| Terra fixes, run against reviewed `0874150e` | **`5 failed, 29 passed`** | each fix has its own failing witness |
| after fixes | **`34 passed in 28.46s`**, `ruff check` clean | GREEN after |

The stub is the load-bearing witness: it existed, imported, and answered — so a green test
here proves discrimination, not merely that the module is present.

### D7 — phase fence: new-files-first, wire into no gate · **MET**

Two new files only (`scripts/file_purpose_graph.py`, `tests/test_file_purpose_graph.py`) plus
the two dependency-declaration files. `check_funnel_lifecycle` is untouched. No hook, no
`ALL_CHECKS` member, no `.pre-commit-config.yaml` entry. `grep -rn file_purpose_graph` outside
those two files returns nothing. The wiring is filed as candidate C-1.

### D8 — A1 (state / telemetry) · **MET, by non-engagement, with the store named**

This lane emits **no health number**, so A1's time-series clause is not engaged and no second
store was created. The store that WOULD receive one is named in the module docstring so a later
slice neither rediscovers it nor invents a rival: **`logs/TELEMETRY.db`**, written through
`scripts/telemetry_emit.py` (SQLite, WAL, append-only; `DEV_KNOWLEDGE_TELEMETRY_DB` overrides
the path). The module is read-only throughout — Layer-2 posture intact.

### D9 — A5 (trust contract) · **MET**

Every claim in this packet carries a witness: a pasted transcript, a machine count, a commit
SHA, or an ancestry proof. The ex-ante numbers are reported verbatim in section 0.

---

## 2. COMMIT SHAs, IN ORDER

| # | SHA | subject |
|---|---|---|
| 1 | `cdccaafa933633d5148fb8d31f949a193f873659` | `chore(deps): declare rustworkx — the named consumer standing ruling R-A reserved` |
| 2 | `0874150ec41ce2f7051928659eed20a7f863e460` | `feat(scripts): the file-purpose graph, first slice — why <path> and its refusal` |
| 3 | `c829f41bf6fb332270aa4a314430570f0ab39dc6` | `fix(scripts): terra pre-merge — five confirmed defects in the file-purpose graph` |

**No generated surface was regenerated**, so there is no such commit to name. `docs/audits/README.md`
is deliberately left stale for this packet — the integrator regenerates it ONCE on the merged
result.

Whole-branch diff, four files: `pyproject.toml`, `uv.lock`, `scripts/file_purpose_graph.py`,
`tests/test_file_purpose_graph.py`.

---

## 3. TERRA TALLY

Reviewer reached. `codex exec` (codex-cli 0.145.0) over `git diff main...HEAD`, NOT
`/codex-review` — a mixed doc/code diff kills that lane.

```
TALLY: Critical=0 High=7 Medium=0 Low=0
```

Disposition — **five FIXED, one accepted-with-a-correction, one fixed in the TEST**. Nothing
was waved through, and findings 3 and 4 were verified against the live manifest and the live
`tasks/archive/` frontmatter before being believed rather than accepted on assertion.

| # | finding | disposition |
|---|---|---|
| 1 | `_normalise` used `lstrip("./")`, a character SET — `.vscode/settings.json` became `vscode/settings.json` and `why` REFUSED three files the live manifest governs | **FIXED** (`removeprefix`). After: `why .vscode/settings.json` → 2 consumers; before, a refusal |
| 2 | `cites` direction reads backwards under `[#595]`'s "declares its consumer" phrasing | **ACCEPTED WITH A CORRECTION.** Direction stays and is right — the edge asserts that the artifact's text REFERENCES a governance object, a coupling it owns; the object naming it BACK is the separate `consumed-by` edge, and the pair IS `[#595]`'s declaration and consumption legs. The WORD invited the misreading, so the rendered phrase is now "references"/"is referenced by", and a new test fails on a reversal of either |
| 3 | only 1 of 3 carrier `target:` shapes read — live `editor-config` uses `source_paths:`, live `docs` uses `doc_paths:` | **FIXED.** Verified in `deploy/manifest-v1.4.0.yaml:343,368` before believing it. A `~`-rooted target is still skipped: a user-machine path is not a file in this repo's space |
| 4 | `tasks/**` scanned non-recursively | **FIXED**, and it was already on this lane's own findings list as a 14-file FALSE-REFUSAL class. `tasks/archive/NNN.md` records are explained by the row their own frontmatter names. Guarded against over-correction: an orphan archive record whose row is absent is STILL refused. Measured: `tasks/` unknowns 16 → 3, and the three remaining are genuinely not rows |
| 5 | a manifest artifact could mint a rival `file:` node for a row that already owns `task:NNN` | **FIXED.** All path→node resolution now funnels through `PurposeGraph.node_for_path()`. Same failure the pass ORDER in `build()` already prevented, reachable by another route; both routes closed |
| 6 | duplicate audit identifiers silently redirected consumption edges by sort order | **FIXED.** `dict[str, set[str]]` — an ambiguous citation edges to every claimant and becomes visible in the answer instead of being resolved silently. (`consumer_at_landing` records this same keying limit for itself) |
| 7 | `test_every_edge_is_consumer_to_consumed` did not test direction — reversing every src/dst would pass it | **FIXED IN THE TEST**, and it was the sharpest finding: a test whose name claims more than its body checks is worse than none, because it gets counted. Renamed to `..._is_registered_for_rendering`; the direction claim now lives in two tests that CAN fail on a reversal, one naming exact src and dst for eight structural kinds. **Stated plainly: those two were GREEN against `0874150e`** — the code was never wrong here; the assertion was |

---

## 4. CANDIDATE FILINGS — reported, never filed

**C-1 · Wire `why` into `check_funnel_lifecycle` (or a successor).** The contract's own phase
fence defers this to a later batch; recorded so the deferral is a decision and not an omission.
Size S–M. The predicate is stable and its API (`build()` / `why()` / `UnknownFile`) is already
test-pinned.

**C-2 · Two real consumer classes the five inputs cannot see.** (a) A file consumed only by a
gate or hook — `docs/audits/README.md` shows `consumers (0)` despite the
`audit-index-freshness` pre-commit hook and CLAUDE.md §9 reading it. (b) A manifest artifact
declared only as a `wiring:` prose string contributes no edge (only `path:`/`source:` do), so
`scripts/block_ff_push.py` shows 0 consumers despite being carried by the `hub-block-ff-push`
component. Both are honest limits of a FROZEN input list, not bugs — but both make the graph
under-report coupling, and (b) is a one-key fix if a ruling admits parsing the wiring string.

**C-3 · The unknown-file surface IS the finding, and it is large.** Measured live:
**1301 of 2677 tracked files are governed (48.6%); 1376 are not.** By top-level directory the
unknowns concentrate in `docs` (836), `tests` (197), `scripts` (104), `ecosystem` (103). The
contract's premise — *a file nothing explains is a defect* — is therefore a claim about roughly
half the tree, and that number is the input to whatever decides how much of it is real debt
versus an input list that is deliberately narrow. It is reported, not triaged: triage is
ADR-111's funnel, not a lane's.

**C-4 · `consumer_at_landing.cited_identifiers` has a lying type annotation.** Declared
`-> tuple[set[str], int]`; returns `(tokens, len(paths), unreadable)` — a 3-tuple. Found while
reading it as a reuse source. Cosmetic today (every caller unpacks three), but the annotation
is the thing a future reader trusts. Size XS.

---

## 5. BUDGET DECISIONS

| decision | call | why |
|---|---|---|
| adopt rustworkx, or take R-A's fallback | **adopt** | the owed measurement PASSED (prebuilt hash-pinned wheel under the pinned uv). The fallback was contingent on failure, and there was none |
| dependency group: `dev` vs a new opt-in group | **`dev`** | the targeted tests and the CLI must resolve it under a plain `uv sync --locked`; an opt-in group would make the ex-ante witness conditional on a flag. Cost — numpy in the default sync — is on the record |
| reuse `build_edge_index` for input 1, or one pass | **one pass** | **measured**, not argued: `build_edge_index` re-tokenizes every `.py` once PER RULE — 14.53s for 16 rules vs 0.75s for a single pass, identical id set, on a query a human runs interactively. The hardened scanners (`markers_in_source`, `DOC_RE`) are still reused rather than re-derived |
| deploy manifest: latest version, or union across releases | **latest only** | the manifest is versioned WITH the methodology; unioning v1.0.0…v1.4.0 would report a component pruned two releases ago as a live consumer. Sorted on the parsed numeric tuple, or v1.10.0 would sort below v1.4.0 |
| default row truncation in `render()` | **20 rows, count never truncated** | a 787-edge answer is a scroll, not an answer. The COUNT is the evidence; a truncated count would be a lie rather than a summary. `--limit 0` prints all |
| `tasks/archive/` edges: build, or report only | **build** (reversed mid-lane) | initially reported as a candidate on phase-fence grounds. Reversed when Terra reached the same class independently: it reads `tasks/`, adds no sixth input, and a refusal firing on a file a row names by path corrupts the ONE thing the deliverable must be trusted on |
| Terra finding 2 (`cites` direction) | **keep direction, change the word** | the direction is correct under the stated convention; the label invited a misreading. Changing a rendering phrase costs nothing; flipping a correct edge to satisfy a reviewer would cost the `[#595]` declaration/consumption distinction |

---

## 6. DEVIATIONS, WITH OWNERS

**DEV-1 · `tasks/archive/` edges built rather than reported. Owner: this lane.** The contract
freezes five inputs and I added an edge type inside input 4 (`tasks/**`) that is not a
`depends-on` edge. Justification: it reads no new surface, and it removes a 14-file
false-refusal class from the deliverable's headline predicate. Guarded both ways — an orphan
archive record is still refused. Flagged for the integrator to accept or revert; reverting
costs 14 false refusals and no correctness.

**DEV-2 · A fourth ex-ante file was witnessed. Owner: this lane.** The contract asks for three;
section 0 shows four (`DEFINITION_OF_DONE.md --depth 2`) because the transitive query is the
evidence that the LIBRARY earns its place, which no single-file answer demonstrates. Additive,
not a substitution — the three named kinds are all present.

**DEV-3 · The ex-ante "script" is `session_end_backpressure.py`, not the first script tried.**
`scripts/consumer_at_landing.py` was the natural pick and the graph REFUSES it — it carries no
`# rule:` marker (it is `exempt` in the registry) and no manifest artifact names it. That is a
correct answer, and swapping to a script the graph does explain is a choice of witness, not a
suppressed failure. Recorded so it is not discovered as a gap.

**DEV-4 · One inherited RED in the targeted run, PROVEN inherited rather than asserted.**
Running the tests that touch `pyproject.toml`:
`1 failed, 439 passed in 124.94s` —
`tests/test_export_backlog_view.py::test_no_gate_hook_or_script_reads_the_export`, failing on
`ecosystem/conformance.html` / `.md` referencing `export_backlog_view`.

Proof, not assertion:
- this lane's whole-branch diff is four files, none under `ecosystem/` and none that test file;
- the offending files' last change is `83023bbc` (2026-08-24), and
  `git merge-base --is-ancestor 83023bbc 77096131` **exits 0** — it predates the merge-base;
- `git merge-base --is-ancestor 77096131 HEAD` exits 0 — this branch is a clean descendant.

It is the known `ecosystem/`-lacks-the-naming-vs-reading-carve-out false positive. Owner: not
this lane. Named so the integrator does not re-diagnose it.

`tests/test_file_purpose_graph.py` — the tests covering this lane's own diff — is **34 passed,
0 failed**. The full suite runs once, at integration, per the contract.

---

## 7. RATCHET

| point | detector | files | count |
|---|---|---|---|
| before the first commit | `silent-rule-v5` | 61 | **443** |
| before the last commit | `silent-rule-v5` | 61 | **443** |

**Delta ZERO.** Measured, not assumed to be 443 — the wave-1 dispatch figure was re-measured at
lane start rather than inherited, and `protocols/` + `templates/` were never touched by this
lane.

---

## 8. THE FOUR THINGS THIS LANE DID NOT DO

1. **No `JOURNAL.md` entry.** The Stop hook's demand is **declined explicitly, with the
   reason**: a batch lane does not journal — the integrator writes ONE anchor for the whole
   queue after every lane STOPs (ADR-85 amendment 2026-08-03 §A5 made that hook advisory in
   full; the hard leg is `block-unanchored-push`, and a lane does not push).
2. **No self-merge, and none suggested.** Commit-and-STOP. This branch enters the frozen queue.
3. **No row closures and no `tasks/` writes.** All four findings are section 4 candidates.
4. **No generated-surface regeneration.** `docs/audits/README.md` is left stale by this packet
   deliberately — the integrator regenerates it once on the merged result. No gate forced one,
   so there is no such commit to name.

**No leftovers:** the planted unknown, the reviewer prompt/output scratch files and the
commit-message scratch files are all `*.tmp` (gitignored) or removed; the working tree carries
nothing beyond this packet.

---

**STOP.** Branch `worktree-lane-m-1-fpg-file-purpose-graph`, three commits, gates green,
targeted tests 34/34, one proven-inherited RED elsewhere, terra 7 findings all dispositioned.
