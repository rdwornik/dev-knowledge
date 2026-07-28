# [#437] shared closure-token detection — design note (pre-build, gate-class posture)

**Date:** 2026-07-28 · **Arc:** `fix/437-closure-token-shared-core` · **Class:** gate code
([#438] posture — terra design review BEFORE implementation; this note is the review input).

## 1. Root cause (verified live this session)

Two divergent copies of closure-token detection over commit messages:

- `scripts/propose_closures.py:51` — `CLOSES_RE = re.compile(r"\b(?:closes?|closed|fixes?|fixed)\s+\[#(\d+)\]", re.I)`
  applied to **raw** message text (`find_strong` :104, `find_weak` :117). No quoting
  awareness: a backtick-quoted `closes [#N]` — prose ABOUT the convention — reads as a
  real closure declaration.
- `plugins/tier1-lifecycle/scripts/propose_closures.py:80/:133/:146` — the hand-mirrored
  plugin port of the same module. **This is the LIVE Stop-hook scanner** (the
  `tier1-lifecycle` plugin is enabled; CLAUDE.md §8/§9), so the false-positive generator
  in production is this copy.
- `scripts/validate_git_backlog.py:82–89` — holds the better lever: `_strip_code`
  (`_FENCE_RE` :82, `_INLINE_CODE_RE` :83) blanks fenced + inline-code spans before its
  `reconcile` (:106–110) hands commits to the SAME `find_strong` it imports from
  `propose_closures`. The precision lever exists once, one file over, unshared.

**Live reproductions (TDD fixtures — verified against the current regex this session):**

1. `12e6b45b` — body sentence "no commit carries a `` `closes [#370]` `` tag" →
   `CLOSES_RE.findall` returns `['370']`; `[#370]` is open → false STRONG proposal in
   every window sampled ([#437] row n=1).
2. `d993922e` — [#437]'s **own filing commit**: the defect description quotes
   `` `closes [#370]` `` → returns `['370']` → self-match (verified live: findall on the
   real message returns `['370']`).
3. `096364ac` — [#437] row n=2: the pre-amend draft quoted the removed README index-row
   clause "Closes [#433] on ruling" verbatim → matched → `git_backlog_drift` reported
   `#433` closed-but-present; amended pre-merge. The COMMITTED message is clean (findall
   `[]` — regression fixture: must STAY clean). The pre-amend quoting form is
   reconstructed as a fixture (quotation-mark context, not backticks).

## 2. Semantics to build

One function decides what counts as a closure directive. A token counts **only as a
directive** — plain-text, per the CONTRIBUTING convention (`feat: …, closes [#57]`).
Occurrences inside the following contexts NEVER match:

| Context | Strip rule | Rationale |
|---|---|---|
| Fenced block ` ``` … ``` ` | blank whole span (dotall) | quoted file/doc content |
| Inline code span `` `…` `` | blank span (non-greedy pair, no inner backtick) | convention-quoting prose — both live fixtures |
| Block-quote line | blank any line whose first non-space char is `>` | quoted ruling/doc text in commit bodies |
| Same-line straight-double-quoted span `"…"` | blank span (both quotes on one line, non-greedy) | the `096364ac` pre-amend form ("quoted the offending phrase verbatim") |

Order: fenced → inline code → block-quote lines → double-quoted spans.

**Error-direction analysis (why stripping is safe):** propose_closures' own doctrine
(docstring :9–10) is precision-over-recall — under-surfacing is the stated safer error.
A REAL directive is a plain trailer/subject clause and never sits inside any of the four
contexts (empirically checked: the design was swept over full history — see §6 sweep
beat). A missed real closure still has three independent backstops: the
`backlog-id-on-close` commit-msg hook (remove-side, different regex), the operator's own
`/review-closures` act, and `git log --grep`. A false POSITIVE has none — it lands in
PROPOSALS/`git_backlog_drift` every window until someone investigates (the lived cost).

**Deliberately NOT stripped:** single-quoted spans (apostrophes make pairing unsafe:
"it's … won't" would blank real text between two apostrophes) and 4-space-indented lines
(commit bodies indent freely; e.g. `d993922e` indents its filing text — treating indent
as code is a markdown-document rule, not a commit-message rule).

## 3. One home, both consumers

**Shared home: `scripts/propose_closures.py` (the detection core it already owns).**
No new module: `validate_git_backlog` ALREADY imports `find_strong`/`Commit`/… from
`propose_closures` (:54–71) — the import edge exists; adding a third module adds a file
and (worse) a third thing the plugin would have to bundle.

New/changed symbols in the core:

- `_STRIP_RES` / `strip_quoted_contexts(text) -> str` — the four-context blanking pass.
- `closure_ids(text) -> list[str]` — **the** single detector:
  `CLOSES_RE.findall(strip_quoted_contexts(text or ""))`.
- `find_strong` (:104) uses `closure_ids(c.message)`; `find_weak`'s plain-commit filter
  (:117) becomes `not closure_ids(c.message)` — a commit whose only closes-token is
  quoted is correctly "plain" (eligible for WEAK file-touch evidence).

Consumers:

- `scripts/validate_git_backlog.py` — **deletes** its duplicate lever: `_FENCE_RE`,
  `_INLINE_CODE_RE`, `_strip_code` (:82–89) and the pre-strip Commit-rebuild in
  `reconcile` (:107–110). `reconcile` passes raw commits; stripping now happens inside
  `find_strong`. The `--first-parent` lever (its other precision lever) is untouched.
  This deletion IS the sanctioned removal — the replaced duplicate logic, nothing else.
- `plugins/tier1-lifecycle/scripts/propose_closures.py` — identical detection-core edit,
  hand-mirrored. The plugin ships standalone into consumer repos (ADR-78 carrier
  doctrine: operator-generated, child-committed — no shared module, no symlink, and it
  must run stdlib-only in an arbitrary consumer), so it CANNOT import hub `scripts/`.
  The established mechanism for exactly this axis is the **carrier-twin parity test**
  (`tests/test_validate_backlog_twin_parity.py` precedent, #206/GAP-2): a new
  `tests/test_propose_closures_twin_parity.py` pins the detection-core symbols
  (`CLOSES_RE`, `strip_quoted_contexts`, `closure_ids`, `find_strong`, `find_weak`)
  **byte-identical** (`inspect.getsource` compare) between the two copies AND asserts
  behavioral parity on the live fixtures. That is what closes the divergence CLASS:
  within-hub = one implementation; hub↔plugin = a twin that can no longer drift silently
  (no such test exists today — this is how :51 and :80 diverged from :87 unnoticed).

## 4. LIBRARY-CHECK beat

Candidates considered: **markdown-it-py** / **mistletoe** (CommonMark span detection).
**Rejected — bespoke justified in one line:** commit messages are not markdown documents
(CommonMark rules like indent-as-code would misparse routine commit-body indentation,
e.g. `d993922e`), the repo is deliberately stdlib-only (`pyproject.toml` declares zero
runtime deps; P0 no-new-deps), and the plugin copy must run dependency-free in consumer
repos. Additional reuse check: the repo's own `audit.py:2326 _strip_code_regions` /
`:2431 _inline_code_spans` (CommonMark equal-backtick-run matcher) serves the
doc-claims DOC domain — importing the 3k-line audit module from a Stop-hook script (and
into the plugin) is a worse coupling than four small regexes; named here as the known
second stripper, not unified (different domain, different grammar needs).

## 5. Blast radius — every consumer of closure-token semantics (file:line)

| Site | Role | Disposition |
|---|---|---|
| `scripts/propose_closures.py:51,104,117` | core (hub) | MODIFIED — shared home |
| `plugins/tier1-lifecycle/scripts/propose_closures.py:80,133,146` | LIVE Stop-hook scanner | MODIFIED — twin mirror + new parity test |
| `scripts/validate_git_backlog.py:82–89,106–110` | better-lever copy | duplicate DELETED; consumes core |
| `scripts/audit.py:1289` (`check_git_backlog_drift` → `_vgb.reconcile`) | audit leg / ship-gate feed | inherits via reconcile — no edit |
| `scripts/review_closures.py:117` (`plan_closures`) + plugin copy | `/review-closures` command | downstream of PROPOSALS text + sha-aliveness; holds NO closure-token regex — no edit |
| `scripts/check_backlog_commit_msg.py:23` (`_REF_RE`) | `backlog-id-on-close` hook | DIFFERENT semantics (remove-side: any `[#id]` reference satisfies; permissive by design — a quoted ref still locates the commit) — out of scope, named |
| `scripts/check_backlog_filing.py` | filing-backpressure hook | kill-candidates grammar, not closure tokens — out |
| `scripts/audit.py:2326,2431` | doc-domain code-span stripper | different domain (markdown files) — out, named in §4 |
| `git log --grep 'closes \[#'` (CONTRIBUTING / check_backlog_commit_msg:6 docstring) | manual locate convention | prose-level tool, unaffected |
| Tests: `tests/test_propose_closures.py` (299 ln), `tests/test_validate_git_backlog.py` (251 ln), `plugins/tier1-lifecycle/tests/test_plugin_paths.py:88` (real-closes fixture) | | updated/extended; must stay green |
| Registry check: `validate_reconciliation._SPEC_REGISTRY` | coherence-nudge | neither scanner registered — no version-bump obligation (verified) |

Outside-the-engine (pass-11 sweep): hooks — `backlog-id-on-close` (different regex, above);
commands — `/review-closures`, `/ship` (downstream, above); audit legs —
`git_backlog_drift` (inherits), ship-gate (consumes its findings — inherits); fleet —
consumers run the PLUGIN copy, which this arc edits; they receive it at next plugin
update (no manifest/roster change: no component added or removed).

## 6. Test plan (TDD — written first, witnessed failing)

False-positive class (must FAIL pre-fix, PASS post-fix):
1. `12e6b45b` full message (verbatim from git) → `closure_ids` returns `[]`.
2. `d993922e` full message (verbatim) → `[]`.
3. Reconstructed `096364ac` pre-amend form (double-quoted "Closes [#433] on ruling") → `[]`.
4. Seeded forms per context: fenced block, inline code, block-quote line ([#437] Done-when's "seeded quoted tag").

True-positive class (must PASS pre- AND post-fix — no regression):
5. History-real forms: `closes [#434]` (`d66aef63`), `close [#386]` (`3ed29345`),
   mid-sentence multi (`closes [#262], closes [#295]` — `27f033df`), `closes [#339] @ <sha>`,
   capitalized `Closes [#N]`, `fixes`/`fixed` variants.
6. Mixed: `` fix `quoted closes [#5]` prose, closes [#6] `` → exactly `['6']`.
7. Unpaired-backtick robustness: `` fix `dangling, closes [#7] `` → still `['7']` (an
   unpaired backtick must not hide a real directive).
8. `096364ac` committed (amended) message stays `[]`.

Integration: `reconcile` end-to-end on a fixture repo (existing test_validate_git_backlog
idiom) proving the strip now fires inside the shared core; twin-parity test (§3).

**Empirical sweep beat (build-phase verification, not a committed test):** run
`closure_ids` vs raw `CLOSES_RE.findall` over ALL of main's history; diff the id-sets.
Expected delta: exactly the known false positives (#370 class) disappear; every id the
operator actually closed stays detected. Any other delta = a design error, stop and
re-review.

## 7. Contract with the frozen A–H

Single atomic `--no-ff` merge; no BACKLOG row closed ([#437] stays open — closure is an
operator `/review-closures` act); no BACKLOG prose touched (G expected N/A); JOURNAL
single-writer letter at integration.
