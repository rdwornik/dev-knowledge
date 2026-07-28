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

---

## AMENDMENT 2026-07-28 (same arc, post terra design review — pre-build)

Terra design review `docs/audits/2026-07-28-codex-437-closure-design.md` (@ `3b2142be`):
verdict **not CLEAR** — 2 HIGH / 2 MEDIUM. All four ACCEPTED; the design is amended as
follows before any implementation. (In-file amendment marker per §5 rule 3 — the original
sections above stand as reviewed; this section is the delta terra reviews next.)

**H1 — plugin release path (ACCEPTED).** §5's twin edit is incomplete without the
version-keyed-cache rollout (INSTALL.md:95): consumers execute a cached copy keyed by
`plugin.json` version, so an unreleased twin edit leaves the false-positive scanner live
in every installed repo. Added to the build plan: bump
`plugins/tier1-lifecycle/.claude-plugin/plugin.json` `0.1.10 → 0.1.11` IN this arc;
post-merge rollout = `claude plugin marketplace update dev-knowledge-methodology` +
`claude plugin update tier1-lifecycle@dev-knowledge-methodology --scope project` (hub) +
session restart to apply; the two installed consumers (corp-monorepo, ai-council) are
OWED the same update — recorded as named follow-through in the arc report, not silently
skipped.

**H2 — sweep provenance (ACCEPTED).** §6's full-history sweep compares **`(sha, id)`
occurrence pairs**, not id sets — an id-set diff cannot see a real occurrence in one
commit masked by a quoted one in another. Every occurrence the new detector drops
relative to raw `CLOSES_RE` is individually reviewed and listed as an explicit allowlist
in the build report; any non-allowlisted drop = design error, stop.

**M1 — multi-line quoting + delimiter edges (ACCEPTED — scope-declare + fixtures).**
Paired **multi-line** double quotes are declared OUT of scope: pairing across lines can
blank real text between two unrelated quote characters — that error direction HIDES a
real directive, which is the worse failure for `git_backlog_drift` (a drift detector
that under-reports). Every observed false positive is same-line/backtick/block-quote;
the multi-line-quoted residual class is accepted and named. Same-line principle applied
consistently: the inline-code regex excludes newlines (`` `[^`\r\n]*` ``) so an unpaired
backtick can never blank across lines (the analogous hide-real-directive hazard in the
original `_INLINE_CODE_RE`, which pairs across lines). Unicode policy: curly double
quotes `“…”` are stripped as a same-line pair exactly like straight quotes; mixed
straight/curly pairs are not paired. New fixtures: CRLF messages, unpaired fence,
unpaired double quote, curly-quote pair, two-line inline span (stays detected —
documented residual).

**H1 build-discovery (second marker, same day — supersedes the "bump in-arc" clause
above):** the in-arc `plugin.json` bump is NOT executable as designed. The plugin
version is a release-lint anchor: C4 (`deploy/release_lint.py:223`) pins
`anchors.plugin_version` — declared in EVERY manifest (`deploy/manifest-v1.4.0.yaml:100`
back through v1.1.0, all `"0.1.10"`) — against the LIVE `plugin.json`, and the suite
lints the HISTORIC manifests against it too (`tests/test_release_lint.py:64/:77`
lint v1.1.0/v1.2.0 live). Witnessed: the bump alone turned 5 release-lint tests red;
bare main green (worktree check). A plugin version bump is therefore a RELEASE ACT
(new anchor + historic-test reconciliation + marketplace/consumer updates), out of this
arc's reviewed scope. Disposition: bump REVERTED in-arc; the release act is filed as
**[#444]** (S8) so the rollout H1 demands cannot rot in prose; until it ships, every
live session — hub included (cache `…/tier1-lifecycle/0.1.10/` verified) — still runs
the un-stripped scanner, which is exactly why [#444] is P2.

**M2 — parity-test mechanics (ACCEPTED).** `inspect.getsource` cannot compare a compiled
pattern. Follow the `test_validate_backlog_twin_parity.py` precedent split exactly:
regexes compared by `.pattern` AND `.flags` (`_TWIN_REGEXES` style — covers `re.I`),
functions by `getsource` (`_TWIN_FUNCS` style). Twin symbol list: `CLOSES_RE` +
`_STRIP_RES` members (pattern/flags), `strip_quoted_contexts`, `closure_ids`,
`find_strong`, `find_weak` (source).

---

## AMENDMENT 2026-07-28 (third marker — terra diff review, both HIGHs fixed pre-merge)

Diff review `docs/audits/2026-07-28-codex-437-closure-diff.md` (@ `4ff31ff7`): verdict
not CLEAR — 2 HIGH, both verified live and FIXED in-arc (TDD: 5 new tests witnessed
failing first):

**H-A (FIXED) — whitespace substitution SYNTHESIZED directives.** `closes "x" [#5]`
raw-matched NOTHING, but blanking the quoted span to spaces let `CLOSES_RE`'s `\s+`
bridge keyword and id — the strip was manufacturing closures. Fix: stripped spans are
replaced by a non-whitespace barrier (`\x00` — NUL cannot appear in a git commit
message), so nothing can be assembled across a removed context. Regression tests cover
the quote / inline / block-quote / fence bridges plus the plain multi-line true
positive (`closes\n[#5]` still matches — no quoted context involved).

**H-B (FIXED) — equal-length multi-backtick runs.** `` ``closes [#99]`` `` (a standard
quoted inline form) survived the single-backtick regex. Fix: the inline pattern pairs
equal-length backtick runs same-line (``(`+)[^`\r\n]*?\1``), superseding the M1
single-backtick wording above; the unpaired/cross-line fail-safes are re-asserted by
the existing residual tests.

Post-fix: the full-history sweep re-derived — the drop set is byte-identical to the
reviewed 10-occurrence allowlist, GAINED still empty (the barrier synthesized nothing
across 4,163 commits). Verification notes from the same review confirming the build:
no remaining duplicate implementation, WEAK quoted-only wiring correct, twin test
catches one-character divergence, `0.1.10` consistent with [#444] carrying the release
coupling.

Two further terra-pinned passes (recorded verbatim with dispositions in
`docs/audits/2026-07-28-codex-437-closure-recheck.md`): pass 2 found tilde fences
matchable — FIXED in-arc (TDD-witnessed, both copies) — and confirmed H-A/H-B dead
with counterexamples plus twin byte-identity; pass 3 proposed stripping indented code
blocks — REJECTED-BY-DESIGN (the §2 non-strip list this review's own design pass
endorsed; indent-stripping would hide real directives), made loud with a residual test.
