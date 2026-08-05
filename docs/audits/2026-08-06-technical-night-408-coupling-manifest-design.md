# [#408] doc-code coupling manifest — design proposal against the operator's three-layer spec

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-06
- **Source-session:** unattended night batch, Claude Code on the web; branch `claude/night-batch-2026-08-06-p59kml`; HEAD `8e2be6a1`
- **Status:** PROPOSAL-ONLY — DRAFT design, zero build, nothing ratified
- **Model:** Opus-class orchestrator

> **Voice and status.** This is a proposal, not doctrine. Nothing here is decided; every
> section states an option and the evidence behind it. It carries no normative keywords by
> intent (the silent-rule ratchet sits at its 441 ceiling — measured live this session,
> 441 ≤ 441 over 57 files — and although `docs/` is outside the detector's corpus, the file
> is written clean so it can be lifted into `protocols/` later without re-editing).
>
> **Routing note, and why this is not in `docs/intake/`.** The contract for this batch asked
> for `docs/intake/2026-08-06-func-408-coupling-manifest-design.md` with `status: DRAFT`.
> That destination turns out to require a filing act this batch is forbidden to perform:
> **every** one of the 12 live intake docs carries an operator-assigned `intake-id:`, and
> `scripts/gen_intake_index.py:136-139` renders a missing one as a loud `MISSING-ID` schema
> break (`grep MISSING-ID docs/intake/README.md` → zero hits today, so it would be the
> first). `[#408]` is a BACKLOG row, not an intake number, and inventing an intake id is a
> birth. The cited "landed night-draft precedent"
> (`docs/intake/2026-08-05-tech-currency-wave-1.md`) carries `intake-id: 24` — an id the
> operator had already assigned. So this lands in the sanctioned `docs/audits/` genre
> instead, which is also the repo's documented promotion path: `docs/intake/README.md:247-250`
> — "an **audit** (evidence, `docs/audits/`) feeds intake by hand when a finding turns out
> **requirement-shaped** — it crosses the folder line as a SEED". Promotion is one operator
> move; the exact command is in §9.

## 1. What the design has to work with (substrate, verified live)

Five substrate facts shape every choice below. Each was read from disk this session.

**1.1 — `ARCHITECTURE.md` has only eleven addressable section anchors.** The file is
1 H1 + 11 H2 and **zero H3-or-deeper headings**. The "six chapters" are *bold-text labels
inside H2 bodies* (`**Chapter 2 — Organ map.**` at `:183`, and ~30 siblings), which have no
heading anchor, no ToC entry, and no unit any checker can address. Consequence, stated
plainly because it bounds the whole design: **an edge can bind to an H2 section and nothing
finer.** Sub-chapter granularity would first require promoting bold labels to real
headings — a separate, larger change with its own ToC and `doc_structure` consequences, and
not proposed here.

**1.2 — a doc↔code coupling mechanism already exists, and edge identity is already
move-safe.** `ecosystem/doc-code-edge.yaml` (168 lines) is a **scan-scope registry**, not a
list of edges: `declaration_docs:` (3 docs scanned for markers), `coverage_scope:` (15
rule-IDs owed an annotation), `multi_site:` (9 rule-ID → expected-site-count entries),
`exempt:` (28 checks with no doc→code rule, each with an inline permanent-vs-temporary
reason). The edge object itself is synthesized at scan time by
`scripts/validate_doc_code_edge.py:57-86` (`Site`, `EdgeResult`, `StructuralFinding`), and an
edge exists iff a doc-side `<!-- rule: ID -->` and a code-side `# rule: ID` share an ID.
**Identity is the ID string, not a path** — so the existing mechanism already survives file
moves and line drift, which is the property the [#359] locator-rot mode attacks. Live status:
`doc_code_edge` — 15 edges resolved, none broken (this session). `doc_code_coverage_drift` —
all 40 `ALL_CHECKS` members covered; **FAIL**-class.

**1.3 — the check contract is narrow and locked.** `ALL_CHECKS`
(`scripts/audit.py:3871-3917`) is a bare list of function references — 40 entries, no
metadata tuple. A member is `def check_<name>(repo_path: Path) -> list[Finding]`. `Finding`
(`audit.py:322-339`) is a frozen dataclass of **exactly three string fields** —
`check_name`, `status`, `evidence` — and its docstring says the shape is "LOCKED — do not
add/rename fields without updating that consumer", pinned by
`tests/test_coherence_integration.py::test_finding_format_is_locked`. Severity is not a
registration property: it is whichever status string the check emits, classified downstream
by `cmd_health` (`audit.py:4549`) and ship-gate (`:4656`).

**1.4 — no new script is needed, and adding one costs more.** The Layer-2 invariant is
binding: `CLAUDE.md:89` — "**Layer 2 never executes** — no orchestration scripts; `scripts/`
contains read-only validators only (ADR-28, ADR-36)"; `ARCHITECTURE.md:132-133` — "No script
here orchestrates actions in, or drives state changes in, another repo." A new check added
*inside* `audit.py` clears this by construction and also sidesteps ADR-101 Rule A, which
structurally blocks unsanctioned new top-level file classes. That is the low-friction path
and the one proposed.

**1.5 — nothing re-validates a pointer, and the only tool of that class is unwired.**
`scripts/preflight_contract.py` verifies four claim kinds against a named contract —
`file-line`, `heading`, `sha`, `backlog-id` (role-aware, ASSERTION vs CITATION, `:78-201`) —
and self-describes at `:36-38`: "**ADOPTION FIRST: this is wired into NO gate.**" It is in no
`ALL_CHECKS`, no pre-commit hook, no Stop hook, and it is forward-only (pre-action) by
design. Confirmed absent: any standing check that walks docs and re-resolves their
citations. This is the gap the addendum's pointer-validation leg names, and §7 reuses this
tool rather than writing another.

## 2. Layer 1 — the coupling manifest data model

**Proposal: extend `ecosystem/doc-code-edge.yaml` with one new top-level key rather than
adding a new file.** Rationale, and it is the repo's own adoption order (PLAYBOOK §11,
`:3442-3454`: stdlib > an existing dependency > a new distribution): the file already exists,
already carries the doc↔code concern, already has three loader functions in `audit.py`
(`_load_declaration_docs` `:1929-1950`, `_load_coverage_scope` `:1953-1972`, `_load_multi_site`
`:1975`) whose pattern a fourth would mirror exactly, and already models the
permanent-vs-temporary exemption distinction this design needs. A sibling file
`ecosystem/doc-code-coupling.yaml` is the fallback if the operator prefers separation; it
clears ADR-101 Rule A either way, since `ecosystem/` is a sanctioned directory.

Proposed shape:

```yaml
# ecosystem/doc-code-edge.yaml  (new top-level key)
coupling:
  version: 1
  edges:
    - id: organ-map-hooks                    # stable, move-safe identity (the 1.2 pattern)
      source:                                 # one or more globs; git-index semantics
        - "scripts/hooks/*.py"
        - ".pre-commit-config.yaml"
        - ".claude/settings.json"
      doc: "ARCHITECTURE.md"
      section: "## Organ map"                 # an H2 heading, verbatim (see 1.1)
      granularity: members                    # model | members
      last_synced: "8e2be6a1"                 # the SHA the doc was last reconciled against
      last_synced_date: "2026-08-05"           # shallow-clone fallback (see 2.3)
      review_date: "2026-11-06"                # shelf-life, ADR-75 anti-paper-suppression
```

**2.1 — the `granularity` parameter.** `members` means the doc *enumerates* the source set,
so any add / remove / rename of a member can make it stale. `model` means the doc describes
the *shape* of the set, so a membership change is not by itself interesting and only a
structural change is. The parameter exists to keep the signal-to-noise ratio survivable: a
`members` edge over `scripts/hooks/*.py` fires on a new hook, which is exactly right; a
`model` edge over the same glob would not.

**2.2 — no new SHA-storage invention.** Four house patterns exist and one fits:

| pattern | where | shape | fit |
|---|---|---|---|
| rotating gitignored log frontmatter | `propose_closures.py:184-185`, `since_commit:`/`head_commit:` in `logs/PROPOSALS-*.md` | ephemeral, per-run | no — the manifest is durable |
| committed durable YAML, written-by-command / read-by-a-check | `ecosystem/tool-versions.yaml` (`last_reviewed_version`, `reviewed_date`) | committed, low-churn, audit-worthy | **yes — this is the precedent** |
| regex-parsed prose inside a ratified ADR | `journal_anchor.py:74-101`, `floor_sha` reading ADR-85 | one fixed floor, rarely moved, visible governance act | no — per-edge values move too often |
| committed durable version record | `ecosystem/deployed-versions.yaml` (ADR-91) | same as row 2 | confirms row 2 is a repeated house pattern, not a one-off |

`ARCHITECTURE.md:737-738` names row 2 explicitly — "the `tool-versions.yaml` durable-version
pattern — committed · written-by-command · read-by-a-check". The manifest adopts it: a
committed value, bumped by an explicit command, read by a check. No new mechanism.

**2.3 — why `last_synced_date` sits beside `last_synced`.** A bare SHA is not resolvable in
a shallow clone, and this session proved that is not hypothetical: `audit.py health` ran here
against a 203-commit shallow clone and produced **three classes of false finding** —
`canonical_freshness` (5 false FAILs, because graft root `27c82d4` appears to add whole files:
`git show --numstat 27c82d4 -- CONTRIBUTING.md` → `219 0`), `no_ff_merges` (1 false WARN on a
real 2-parent merge whose parents are truncated), and `journal_spine_anchor` (a FAIL-class
AnchorError, floor SHA resolvable but ancestry truncated). A manifest keyed only on SHAs
inherits that class the moment it runs in CI. Carrying a date beside the SHA lets the check
degrade to a date comparison and say so, rather than silently re-flagging every edge.

## 3. The per-section granularity table — proposed, not decided

One row per addressable `ARCHITECTURE.md` H2 (per 1.1, these are the only bindable units),
one line of rationale each. This is the "separate small operator decision" pre-chewed.

| # | Section (line) | Proposed | Rationale |
|---|---|---|---|
| 1 | `## Purpose` (:53) | **members** | Carries the ADR-104 nine-repo fleet declaration; membership is the content, and `membership_agreement` already proves it drifts (5 of 9 resolved today). |
| 2 | `## Codemap` (:79) | **members**, peg only | Already regen-gated by the `codemap-freshness` pre-commit hook — the manifest should peg to that hook, not duplicate it. Listing it as an edge with no check attached keeps the map honest without adding a second opinion. |
| 3 | `## Layer Boundaries & Invariants` (:103) | **model** | Pure doctrine (ADR-28/36/39/41). It enumerates invariants, not code; only a change to the invariant set matters, which is an ADR event, not a diff event. |
| 4 | `## Authority and governance` (:155) | **model** | Describes the authority chain and that `audit.py` hosts a check suite; it does not enumerate the suite. Adding a check does not touch this section's claims. |
| 5 | `## Organ map` (:181) | **members** | The highest-value edge in the file. It enumerates every organ with trigger/layer/posture/status, and all three of the (f) sweep's unowned stale claims (U-1 `:327`, U-2 `:226`, U-3 the absent `block_unanchored_push`) live in this chapter's reach. |
| 6 | `## Validators and enforcement` (:288) | **members** | Enumerates named validator scripts and the pre-commit gate list; a new or renamed validator makes it stale immediately. |
| 7 | `## Automation axes` (:505) | **model** | A policy chapter (channels, model routing, adoption). No code enumeration to go stale member-wise. |
| 8 | `## Distribution and transfer` (:567) | **members** | Enumerates the five carriers and the channel set; `[#403]`'s own row cites a five-site carrier-count drift, so this is a measured-stale surface. |
| 9 | `## Key conventions & zones` (:617) | **members** | Carries the file-lifecycle table and the ADR-75 zone register — both enumerations keyed to live guards. |
| 10 | `## Verification mesh and decision flow` (:702) | **members** | Enumerates the mesh layers and the nightly loop's three stages. U-3's missing organ belongs here, and a B1 server-side row would land here. |
| 11 | `## Governing ADRs` (:820) | **members** | A pure index of `docs/decisions/ADR-*.md`; `[#403]` names its "stopping at ADR-93" drift, i.e. member drift by definition. |

Eight `members`, three `model`. The three `model` rows are the doctrine/policy chapters,
which is the expected split and a useful sanity check on the parameter: if a chapter's
content is *what the rules are* rather than *what exists*, a diff over code is the wrong
trigger for it.

**Excluded from edge candidacy, deliberately:** generated files. `docs/audits/README.md` is
written by `scripts/gen_audit_index.py --write` and gated by `audit-index-freshness`; the
intake Contents block by `gen_intake_index.py`; `docs/intake/manifest.json` is derived
*from* `README.md` by `gen_intake_tree.py`; the CLAUDE.md fragments by
`gen_claude_rosters.py`. Binding an edge to a generated artifact would fire on every
regeneration and teach the operator to ignore the check — the failure mode the whole design
exists to avoid.

## 4. Layer 1 — the trigger algorithm (specified as a check, not as code)

Pure diff, no heuristics, no model in the loop.

```
for each edge in coupling.edges:
    if edge.review_date < today:                 -> Finding(warn, "edge shelf-life expired")
    resolve last_synced:
        if SHA resolves in this clone            -> range = last_synced..HEAD
        elif last_synced_date present            -> range = --since=<date> ; note DEGRADED
        else                                     -> Finding(warn, "baseline unresolvable"); continue
    hits = git log <range> --oneline -- <edge.source globs>
    if hits is empty                             -> Finding(pass, "in sync")
    else                                         -> Finding(warn, "<doc>#<section> may be stale:
                                                     N commit(s) touched <globs> since <baseline>")
```

Four properties worth naming:

- **Git-index semantics, not worktree.** The glob resolution uses `git log -- <pathspec>`,
  which reads the index. This is the same rejection already on the record at
  `STANDING_RULINGS.md:157-162`: `glob.glob(recursive=True)` "walks the working tree rather
  than the git index, so a tracked file deleted from the worktree would silently leave the
  governed set", and `pathspec` speaks `gitwildmatch` rather than pure glob. Using
  `git log --` inherits the correct semantics for free.
- **Granularity is applied at the hit-classification step**, not the diff step: a `model`
  edge ignores pure add/remove/rename hits and fires only on modifications to existing
  members; a `members` edge fires on any hit. (The add/remove/rename discrimination comes
  from `git log --diff-filter`, so this stays a pure-diff rule.)
- **Where it lives:** one new function `check_doc_code_coupling(repo_path) -> list[Finding]`
  inside `scripts/audit.py`, appended to `ALL_CHECKS`. No new script, no new top-level file,
  no ADR-101 Rule A exposure. Registration is the append; `cmd_checks` (`audit.py:4743-4761`)
  prints from the registry, so the documented list cannot drift from what runs.
- **`serialize-group: audit-py`** — both `[#403]` and `[#408]` already carry it, so this work
  serializes against other `audit.py` edits by existing convention rather than by judgment.

**Cost note.** One `git log` per edge, ~11 edges. For scale reference, `fleet_parity`'s ~8s
walk already runs per-commit and its ship-gate-scoping is a filed follow-up — so a
per-commit cost in that range is a known concern in this codebase, and scoping the coupling
check to ship-gate rather than every commit is the conservative default.

## 5. Layer 2 — the bounded LLM evaluation contract

Layer 1 says *an edge moved*. Layer 2 says *whether the doc actually needs changing*. It runs
only on flagged edges, never on the whole corpus.

**Inputs, per flagged edge (the whole context, nothing else):** the edge's `id`, `doc`,
`section`, `granularity`; the verbatim text of that H2 section as it stands; and the commit
subjects plus diff hunks for the source globs across `last_synced..HEAD`.

**Output — exactly one of three verdicts, plus a one-sentence rationale citing a hunk:**

| verdict | meaning | consequence |
|---|---|---|
| `NO-OP` | the code changed in a way the section does not claim anything about | bump `last_synced`; no doc edit |
| `PATCH` | the section carries a specific claim the diff falsified, and the correction is mechanical | emit a proposed diff for a human to apply; never self-apply |
| `ESCALATE` | the section's model, not merely its members, is now wrong | surface for architect judgment; no proposed diff |

**Cost bound, stated three ways so it cannot creep:** (i) only flagged edges are evaluated,
so a clean diff costs zero model tokens; (ii) one call per flagged edge, no retries beyond a
schema-validation retry; (iii) a declared per-edge input cap, with a hunk-count truncation
that is *reported* when it bites rather than silently applied — a truncated evaluation is
labelled DEGRADED, not passed off as complete.

**The propose-only boundary.** Layer 2 emits proposals. It does not edit `ARCHITECTURE.md`.
This is the same posture the closure loop already holds — `propose_closures.py` is
"**propose-only** (never mutates BACKLOG)" (`ARCHITECTURE.md:225`) — and the same reason:
the human gate is the point. Whatever an LLM leg proposes here should be at most as
authoritative as that.

## 6. Layer 3 — advisory-first rollout and its evidence bar

Advisory first, hard flip only on measured evidence. The precedent is landed, twice:
`STANDING_RULINGS.md:180-181` (B4) — "zero false positives over two consecutive windows,
reported at each seal (`[#483]` R3; re-ruled for `[#480]` → `[#499]`)" — and ADR-85's
asymmetry (`:13,19`), where the JOURNAL leg shipped hard and the BACKLOG leg shipped as an
advisory nudge.

Proposed bar for this organ: `warn`-class for two consecutive windows; promotion considered
only if **zero false positives** across both, with the count reported at each seal. A false
positive here has a precise definition worth writing into the row, because "the check fired
and the doc was fine" will otherwise be argued both ways: **a flagged edge whose Layer-2
verdict was `NO-OP`** is the false-positive case for Layer 1.

Two honest caveats to carry into the row rather than discover later:

- **The per-seal report is not mechanically enforced.** The same gap is already on the record
  for `[#499]` at that bundle's `RESIDUAL.md:125-129` — nothing enforces the cadence, so
  reporting it is a manual discharge. A coupling manifest inherits exactly that weakness.
- **The ADR moment is the hard flip, not now.** `STANDING_RULINGS.md` B3 lists "hard-wiring
  any advisory leg before its evidence bar" among the twice-ruled rejections
  (`:150-151`), and B4 says an ADR written now "would ratify an *advisory interim state*".

## 7. The pointer-validation leg (addendum requirement)

The diagnosis-home standard creates pointers, and §1.5 established that nothing re-validates
one. Proposal: **reuse `preflight_contract.py`, do not write a second pointer checker.** It
already implements the four claim kinds this needs — `file-line`, `heading`, `sha`,
`backlog-id` with the role-aware ASSERTION/CITATION split (`:78-201`) — and its own row
already carries the open question of whether it should become a gate.

Shape: a companion check `check_census_pointers(repo_path) -> list[Finding]` that walks the
manifest's `doc` targets plus the rows that carry `docs/audits/` pointers, and calls the
existing `preflight_contract` predicates. It answers three questions: does the cited audit
file exist; does the cited section heading still resolve; is the `[#id]` still in the state
the citation assumes.

The concrete case that motivates it, verified this session: `[#483]`'s ruling record has no
`BACKLOG.md` row and no node among `tasks/manifest.json`'s 473 nodes; its only live pointer
is a retired `tasks/483-*.md` with `status: closed`. Reported honestly, a probe lane read the
same facts and judged the pointer to be *resolving cleanly* — a properly closed-and-archived
task rather than an orphan. That disagreement is itself the argument for the leg: two careful
readers disagreed about whether a pointer was healthy, which is precisely the question a
deterministic check should be answering instead of a reader.

## 8. How this subsumes-or-pegs `[#403]` and `[#169]`

Both rows read live from `BACKLOG.md` and their task files.

**`[#403]` — PEG, not subsume, against its own row's invitation.** `[#403]`
(`BACKLOG.md:246`, `tasks/403-*.md`, open · P3 · S · `serialize-group: audit-py`) extends
`doc_claims` to ARCHITECTURE's machine-derivable claims; its Done-when is "carrier-set AND
child-roster gated (doc_claims or a regen-and-diff sibling) with tests". `[#408]`'s row names
it "the mechanism seed" and its `kill-candidates:` field says "#403 (if its doc_claims
extension already discharges the coupling, fold in)". The honest answer is that it does not
discharge it, because the two do different jobs: **`[#403]` verifies a claim's value**
(is the carrier count really 5?), while **the manifest flags that a value may need
re-verifying** (the carrier code changed since this section was last reconciled). They
compose — the manifest is the trigger, `[#403]` is the verifier — and folding one into the
other would lose the half that fires when no machine-derivable claim exists at all, which is
where U-1/U-2/U-3 actually lived. Recommended disposition: keep `[#403]`, record the peg, and
have the manifest cite it as the verifier for `members` edges. Supporting evidence that the
verifier half is thin today: `doc_claims` currently checks only **3** self-claims (live run,
this session).

**`[#169]` — PEG, with the distinction recorded.** `[#169]` (`BACKLOG.md:74`,
`tasks/169-*.md`, **deferred** · P3 · M · `depends-on: #171`) wants "a deterministic staleness
signal for the four ADR-85-ungated docs" in "the digest / conformance dashboard, **NOT** a
per-session gate". Three differences make subsumption wrong: its trigger is
**time-since-touched vs code churn**, not a diff against a stored baseline; its surface is a
**digest/dashboard**, not `audit.py health`; and it is pegged to `#171`, a dashboard that does
not exist (Ch6 records it unbuilt, and `ARCHITECTURE.md:846` names
`ecosystem/conformance.md`, a path with no git history). A coupling manifest would give
`[#169]` a *cheaper input* — an edge-level staleness fact it could surface — but it does not
do `[#169]`'s job. Recommended disposition: peg, and note that the manifest lands the
deterministic half `[#169]` was waiting on, which may shrink `[#169]` to a surfacing row.

**Reconciliation against the coupling surface generally.** The manifest absorbs the
coupling *surface* — the question "which doc sections are bound to which code" — from both
rows, and leaves each row its own distinct job (value-verification for `[#403]`, digest
surfacing for `[#169]`).

## 9. Library verdict, and the promotion path

**Library verdict (Part 3 item 3, folded in): BUILD-thin — with one design change the research
forces.** Full comparison and citations in
`docs/audits/2026-08-06-technical-night-library-research.md`.

Nothing off-the-shelf covers Layer 1, and the divergence is categorical rather than a matter
of taste: the adjacent classes each solve a *different* problem — include/transclusion tools
(Sphinx `literalinclude`, mkdocs snippets, mdBook `include`) guarantee freshness by
**inclusion**, inapplicable to prose that describes rather than quotes code; markdown
code-block runners (`doctest`-class) verify **executable examples**; link checkers verify
**reference existence**, not semantic currency. Explicit negative finding: **no Vale or
markdownlint plugin does code-reference staleness.** The commercial class (Swimm, Dosu) is
closest in intent and excluded on the no-external-SaaS constraint. Corroborating signal worth
noting: Dosu independently ships the *same three-layer shape* — deterministic checks, then an
LLM layer for the gray zone, then a score — which suggests the operator's spec is the shape
this problem converges on.

**The design change: replace the raw-SHA trigger with a normalized fingerprint.** The closest
open-source prior art is **Fiberplane `drift`** (MIT, ~128★, repo touched June 2026, ships a
GitHub Action and a `drift check` CLI). Its `drift.lock` carries `doc`, `target`
(`path` or `path#Symbol`), `sig`, and an optional `origin` — and `sig` is a **normalized AST
fingerprint** (tree-sitter node-kinds plus token text, ignoring whitespace and position), not
a commit SHA. That matters concretely here: `§4`'s "any commit in the range touched the glob"
trigger will fire on every reformat, typo fix, comment edit and `ruff --fix` pass, and this
repo produces a lot of those. A manifest whose first month is mostly false positives teaches
the operator to ignore it — the one failure mode §3 already refuses for generated files.

Two options follow, and the choice is a real fork rather than a formality:

- **v1 as specified (raw range trigger), with the noise accepted and measured.** Cheapest to
  build, and the advisory-first rollout in §6 is exactly the instrument for measuring whether
  the noise is tolerable — a flagged-then-`NO-OP` edge is already defined as the
  false-positive case. If the rate is low, nothing more is needed.
- **v1 with a cheap fingerprint.** Not tree-sitter — that would be a new dependency class.
  A stdlib-only approximation is available: hash the concatenated `git show` output of the
  glob's files with comment-only and blank-line changes normalized out. Weaker than an AST
  fingerprint, far stronger than "a commit happened", and it stays inside the adoption order
  (stdlib first).

Recommended: build v1 raw, but **store the fingerprint field in the manifest from day one**
(`sig:`, unused at first) so adding the comparison later is not a schema migration. `drift`'s
own CLI output shape is also worth copying for the advisory rollout — `STALE <target>
(<reason>)` / `ok <target>` plus a one-line summary count — since it maps directly onto the
`Finding(check_name, status, evidence)` triple this repo is locked to.

Why not simply adopt `drift`: it binds **one file or symbol per edge**, not a glob, and anchors
to a whole **doc file**, not a doc section. Both are exactly the dimensions §1.1 and §2 need.

**Promotion path, if the operator wants this as an intake SEED.** One move, no rework:

```
cp docs/audits/2026-08-06-technical-night-408-coupling-manifest-design.md \
   docs/intake/2026-08-06-func-408-coupling-manifest-design.md
# then add the operator-assigned `intake-id:` + `status: SEED` frontmatter, and:
uv run --locked python scripts/gen_intake_index.py --write   # refreshes the README Contents block
uv run --locked python scripts/gen_intake_tree.py --write    # re-derives docs/intake/manifest.json
```

Both generators are gated (`intake-index-freshness`, and `intake_tree_coherence` in
`ALL_CHECKS`), so skipping either blocks the commit. This batch ran neither — it added no
intake file — and ran only `gen_audit_index.py --write`, the one generated-file write its
contract sanctioned.

## 10. Open forks left for the operator

Five, each with the evidence that makes it a real choice rather than a rubber stamp.

1. **Manifest home** — a new `coupling:` key in `ecosystem/doc-code-edge.yaml` (§2,
   recommended: reuses three loaders and the existing exemption doctrine) vs a sibling
   `ecosystem/doc-code-coupling.yaml`. Both clear ADR-101 Rule A.
2. **The granularity table** (§3) — eight `members` / three `model` proposed. Each row has a
   one-line rationale; disagreement on any single row is cheap to apply.
3. **Check scope** — ship-gate only vs every commit. The `fleet_parity` precedent (~8s
   per-commit walk, scoping filed as a follow-up) argues for ship-gate.
4. **Whether Layer 2 is in v1 at all.** Layer 1 alone already surfaces "this section may be
   stale", which is more than exists today. Deferring Layer 2 keeps v1 model-free,
   deterministic, and free of a per-edge token cost — at the price of a noisier signal, since
   without it every flagged edge needs a human read.
5. **Whether `[#403]` folds after all** (§8). The recommendation is peg-not-subsume, but
   `[#408]`'s own `kill-candidates:` field explicitly invites the fold, so overriding the
   recommendation is a one-line disposition rather than a re-argument.
