# Closure-token detector is blind to negation — `Does NOT close [#367]` reads as a closure

Status: PROPOSED — defect note, analysis only; no fix chosen, no code changed

**Scope.** Read-only analysis of `propose_closures.closure_ids` (the [#437] shared
closure-token core) and its two callers, on the working tree of
`/home/user/dev-knowledge` at branch `claude/night-2026-07-31-morning-prep-yo7pgw`,
2026-07-31. No source file was modified; no git mutation was performed. This note
reproduces the defect empirically, maps its blast surface, and sets out bounded fix
options **without recommending one** — the architect rules.

---

## Mechanism

### The regex

`scripts/propose_closures.py:49-51` — verbatim:

```
# A closing keyword immediately before a [#id] — the documented convention is
# `closes [#N]` (mirrors check_backlog_commit_msg.py / `git log --grep`).
CLOSES_RE = re.compile(r"\b(?:closes?|closed|fixes?|fixed)\s+\[#(\d+)\]", re.I)
```

The pattern is **keyword-adjacency only**. It asserts a word boundary *before* the
keyword and nothing about what precedes that boundary. Any sentence that puts a
closing keyword immediately before `[#N]` matches, regardless of the sentence's
polarity.

### The function

`scripts/propose_closures.py:87-92` — verbatim:

```
def closure_ids(text: str) -> list:
    """THE closure-token detector ([#437] shared core): ids declared closed by
    `text`, counting a token only as a plain-text directive (quoted contexts
    stripped). Both scanners — this module's STRONG/WEAK detection and
    validate_git_backlog.reconcile — flow through here; do not re-derive."""
    return CLOSES_RE.findall(strip_quoted_contexts(text or ""))
```

### The only pre-filter that exists

`strip_quoted_contexts` (`scripts/propose_closures.py:79-84`) applies the six
patterns of `_STRIP_RES` (`scripts/propose_closures.py:63-70`): fenced ``` block,
`~~~` fence, same-line inline-code span, block-quote line, straight-double-quoted
span, curly-double-quoted span — each replaced by the NUL barrier
`_STRIP_BARRIER` (`scripts/propose_closures.py:76`).

That filter answers a *different* question: "is this token quoted prose about the
convention?" ([#437], comment at `scripts/propose_closures.py:53-62`). It has **no
polarity component**. A plain-text negated sentence is, to this pipeline,
indistinguishable from a plain-text directive.

### Where the result is consumed

- `find_strong` — `scripts/propose_closures.py:141-148`, calls `closure_ids(c.message)`
  at `:145`; every returned id that is still open in BACKLOG becomes a STRONG closure
  proposal written into `logs/PROPOSALS-YYYY-MM-DD.md`.
- `find_weak` — `scripts/propose_closures.py:151-169`, calls `closure_ids` at `:158`
  to decide which commits count as "plain" (no closure declared). A negated sentence
  therefore also *removes* a commit from WEAK evidence — a second-order effect.
- `validate_git_backlog.reconcile` — `scripts/validate_git_backlog.py:82-100`, reuses
  `find_strong` (see its own comment at `:74-79` and `:22`), which feeds
  `audit.py check_git_backlog_drift` (`scripts/audit.py:1278-1315`; WARN, never FAIL,
  per its docstring at `:1287-1289`).

### The documented convention the parser is meant to implement

- `CONTRIBUTING.md:53` — `feat(scripts): add backlog validator, closes [#57]`
- `CONTRIBUTING.md:58` — closing adds `closes [#<id>]` in summary or body
- `CONTRIBUTING.md:59` — `closes` vs `advances`: only `closes` is seen by the detector
- `protocols/ESSENTIALS.md:150`, `protocols/PLAYBOOK.md:1674` — same convention

Observed in history (`git log --first-parent -40`, grep `clos`): the real forms are
`closes [#N]`, `close [#N]`, `Closes [#N]`, `closed [#N]` — e.g. `eea2c1c`
("closes [#437], closes [#439], closes [#444]"), `4911f00`, `5e331d7`, `6195d93`.
The convention has **no negative form**: nothing in CONTRIBUTING or PLAYBOOK tells an
author how to write "this does *not* close #N" safely.

---

## Empirical reproduction

All results below are **observed output**, not static inference. Runner (hub copy):

```
python -c "import sys; sys.path.insert(0,'scripts'); import propose_closures as p; print(p.closure_ids('<string>'))"
```

The function is importable and callable in isolation (module-level constants only;
no git or filesystem access on the `closure_ids` path), so no static fallback was
needed.

### (a) The negation case — DEFECT REPRODUCED

- String: `Does NOT close [#367]`
- Expected by intent: `[]` — the sentence denies a closure
- **Observed: `['367']`**

Not a synthetic case. The identical sentence exists in this repo's history —
commit `6489391340c4b2cf36c41a14bb30df0317304835`, body line:

```
Does NOT close [#367] — that row owns the general held-version mechanism.
```

Run against the real message read back from git:

- `p.closure_ids(<git show --format=%B --no-patch 6489391340c4>)` → **`['367']`**

And the full detector path on the current branch window (`main..HEAD`), with the
real BACKLOG parsed by `validate_backlog.parse`:

- `[#367]` is open in BACKLOG (`BACKLOG.md:408`) → observed `True`
- `find_strong` over `main..HEAD` → **`{'367': [('648939134', 'docs(protocols): HANDOFF_PROCESS 6.0 -> 6.0.1 — §13(c″) Dest…')]}`**

So the Stop-hook detector currently proposes closing `[#367]` on the strength of a
commit whose sentence says it does not close `[#367]`. This is a STRONG-tier
proposal — the tier documented as "precision over recall"
(`scripts/propose_closures.py:9-14`).

The incident is already on the record as a self-induced false positive: `JOURNAL.md:69-74`
("Ship-gate is RED-on-branch by one self-induced false positive … the remedy is
backticking or avoiding the token").

### (b) True-positive control — must keep working

- String: `chore(backlog): closes [#434] — extraction pass`
- Expected by intent: `['434']`
- **Observed: `['434']`** — control holds; the defect is not "the parser is broken",
  it is "the parser has no polarity".

### (c) Adversarial third — a closure that already happened / was undone

- String: `chore: reopen — previously closed [#367] but the work regressed`
- Expected by intent: `[]` — this is a *historical reference plus a reopen*, the
  opposite of a closure declaration
- **Observed: `['367']`**

### Additional observed cases (same runner)

- `does not close [#367]` → **`['367']`**
- `doesn't close [#367]` → **`['367']`**
- `never closes [#367]` → **`['367']`**
- `no longer closes [#367]` → **`['367']`**
- `Reverts a08f1c2 which closed [#367]` → **`['367']`**
- `Does not close [#367] but closes [#368]` → **`['367', '368']`** (mixed-polarity
  line: the true positive and the false positive are indistinguishable in the output)
- `not closing [#367]` → **`[]`** (accidental miss — `closing` is not in the keyword
  alternation; not evidence of negation-awareness)
- `Does NOT \`close [#367]\`` → **`[]`** — the *existing* [#437] quoting strip is the
  only working mitigation today, and it is an author-side manual habit, not a
  parser property.

### Side finding, observed while testing (unrelated to negation, worth one line)

`fixes?` in `CLOSES_RE` expands to `fixe` / `fixes` — it does **not** match bare
`fix`. Observed: `does not fix [#367]` → `[]` *and* `fix: fixes [#7]` → `['7']`,
i.e. `fix [#N]` alone is invisible to the detector. That is a latent
false-**negative** in the keyword set, distinct from the defect this note is about.
Recorded, not analysed further.

---

## Twin + test coverage

### Twin: YES — it exists and shares the defect

`plugins/tier1-lifecycle/scripts/propose_closures.py` is a hand-mirrored ADR-78
carrier copy and is the **live** Stop-hook scanner (CLAUDE.md §8/§9; the parity test's
own docstring says so at `tests/test_propose_closures_twin_parity.py:3-8`).

- `plugins/tier1-lifecycle/scripts/propose_closures.py:80` — `CLOSES_RE`, byte-identical
  pattern; verified at runtime: `hub.CLOSES_RE.pattern == plugin.CLOSES_RE.pattern` → `True`
- `plugins/tier1-lifecycle/scripts/propose_closures.py:92-99` — `_STRIP_RES`, identical
- `plugins/tier1-lifecycle/scripts/propose_closures.py:108-113` — `strip_quoted_contexts`
- `plugins/tier1-lifecycle/scripts/propose_closures.py:116-121` — `closure_ids`

Observed on the plugin copy (loaded by path with `CLAUDE_PROJECT_DIR` set):

- `Does NOT close [#367]` → **`['367']`**
- `does not close [#367]` → **`['367']`**
- `Reverts the commit that closed [#367]` → **`['367']`**
- `closes [#367]` → **`['367']`**

**Lockstep is not optional, it is gated.** `tests/test_propose_closures_twin_parity.py:31-33`
declares the pinned twin surface — `_TWIN_REGEXES = ("CLOSES_RE",)`,
`_TWIN_REGEX_TUPLES = ("_STRIP_RES",)`,
`_TWIN_FUNCS = ("strip_quoted_contexts", "closure_ids", "find_strong", "find_weak")` —
compared by `.pattern`/`.flags` (`:56-67`) and by `inspect.getsource` (`:70-74`). Any
parser fix that touches one copy and not the other turns this test RED. The copies are
allowed to diverge only outside the core (host-root resolution — real diff at
hub `:44-45` vs plugin `:45-74`, plus `git_log_commits(first_parent=…)` present only
on the hub at `scripts/propose_closures.py:270`).

### Test coverage: the negation case is NOT covered

`tests/test_closure_token_quoting.py` is the closure-token suite (36 assertions).
What it covers:

- live quoting reproductions — `:54-55`, `:70-71`, `:83-84`, `:99-106`
- seeded quoted forms: inline code `:111-112`, ``` fence `:115-116`, `~~~` fence
  `:119-121`, unpaired fence `:124-125`, block-quote `:128-133`, straight-quoted
  `:136-137`, curly-quoted `:140-141`
- true positives (no-regression): `:146-157` — eight forms incl. `closes`, `close`,
  `Closes`, `closed`, `fixes`, `fixed`
- mixed / unpaired-delimiter cases: `:160-181`
- documented residuals: `:186-203` (multi-line quotes, indented lines, multi-line
  inline spans stay DETECTED, by design)
- H-A barrier / bridging: `:210-228`; H-B multi-backtick: `:233-242`
- detection-core integration: `:247-262`

What it does not cover: **nothing anywhere in `tests/` asserts anything about polarity.**
`grep -rn -i "not close\|NOT clos\|negat\|polarity" tests/` returns only unrelated hits
(`test_deploy_mesh.py:61,195`, `test_validate_doc_claims.py:338,355`,
`test_scan_undeclared_edges.py:72`, `test_e2e_consumer_lifecycle.py:4`,
`test_v6_frozen_contract.py:44,116,172,199`) — none about closure-token polarity.
The twin-parity behavioural fixtures (`tests/test_propose_closures_twin_parity.py:79-84`)
are quoting fixtures only.

The [#437] design note (`docs/audits/2026-07-28-technical-437-closure-token-design.md`)
names its residual classes at `:196-207` and `:250`, `:264` — multi-line quotes,
indentation, and the out-of-scope `check_backlog_commit_msg.py` semantics (`:124`).
**Negation is not among them.** This is a new, previously un-named class, not a
knowingly-accepted residual.

### Adjacent, currently open row

`BACKLOG.md:29` / `tasks/447-ratchet-raise-local-hook-bootstrap-deadlock.md` ([#447])
uses the phrase "Closure polarity" but for an unrelated meaning (ordering of owning
rows at closure time). It does **not** own this defect. No open row was found that
covers closure-token polarity.

---

## Fix options with blast radius

Three bounded options. **No position taken.**

### Option A — parser change: make `closure_ids` polarity-aware

What changes: `CLOSES_RE` (or a new negation guard applied inside `closure_ids`)
gains a negative-lookbehind / preceding-window check so a closing keyword preceded by
a negator in the same clause does not match.

Files touched:
- `scripts/propose_closures.py:51` (and/or `:87-92`)
- `plugins/tier1-lifecycle/scripts/propose_closures.py:80` (and/or `:116-121`) —
  **mandatory lockstep**, byte-identical, enforced by
  `tests/test_propose_closures_twin_parity.py:31-33`
- `tests/test_closure_token_quoting.py` — new polarity section; the residual list in
  its module docstring (`:13-16`) should gain the newly-accepted residuals
- `docs/audits/2026-07-28-technical-437-closure-token-design.md` is immutable
  (CLAUDE.md §5 rule 3) — a new design note or an amendment marker, not an in-place edit

Not touched: no pre-commit config change (`closure_ids` is not wired to a commit
hook; `backlog-id-on-close` uses the separate, deliberately permissive `_REF_RE` in
`scripts/check_backlog_commit_msg.py:23` — declared out of scope at the [#437] design
note `:124`). `audit.py` and `validate_git_backlog.py` inherit the fix with no edit.

Honest limit — measured, not assumed. A representative lookbehind sketch
(`(?<!\bnot\s)(?<!\bnever\s)` before the keyword alternation) was run over the same
strings. Observed:

- `Does NOT close [#367]` → `[]` (fixed)
- `never closes [#367]` → `[]` (fixed)
- `Does not close [#367] but closes [#368]` → `['368']` (fixed, both halves correct)
- `chore(backlog): closes [#434]` → `['434']` (control preserved)
- `doesn't close [#367]` → **`['367']`** (still wrong — `n't` is not `not `)
- `no longer closes [#367]` → **`['367']`** (still wrong)
- `previously closed [#367] but the work regressed` → **`['367']`** (still wrong)
- `Reverts a08f1c2 which closed [#367]` → **`['367']`** (still wrong)

So Option A catches the *literal* incident form and a couple of neighbours, and
leaves the general class open: negation in English is unbounded (contractions,
distance, "no longer", "fails to", subordinate clauses, past-tense reference to a
prior or reverted closure). Each widening of the negator set adds a
**false-negative** risk in the opposite direction — a real `closes [#N]` suppressed
because an unrelated "not" happened to sit nearby, which the [#437] design already
identifies as the *worse* failure direction for a drift detector
(`docs/audits/2026-07-28-technical-437-closure-token-design.md:196-200`;
`tests/test_closure_token_quoting.py:186-189`). Note also that the current pipeline
is regex-over-whole-message: a lookbehind has no sentence or clause boundary to work
with unless one is introduced.

### Option B — convention change: a strict closure token

What changes: the closure declaration becomes a token that cannot occur in ordinary
prose — e.g. a dedicated trailer line (`Closes: [#N]` at line start, git-trailer
shaped) or a sigil form — and `closure_ids` matches only that shape. Denials,
narration, and reverts then never collide with it because they are not the token.

Files touched:
- `CONTRIBUTING.md:53`, `:58-59`, `:116` — the documented convention and the hook table
- `protocols/ESSENTIALS.md:150`, `protocols/PLAYBOOK.md:1674` — the same convention
  restated (ESSENTIALS summarises PLAYBOOK — CLAUDE.md §5 rule 6; both move or neither)
- `scripts/propose_closures.py:51` + the plugin twin `:80` — lockstep as in Option A
- `tests/test_closure_token_quoting.py:146-157` — the eight true-positive forms are
  asserted against the *old* convention and would have to be re-based
- `scripts/check_backlog_commit_msg.py` — its `_REF_RE` is permissive by design and
  need not change, but the CONTRIBUTING text that describes it (`:58`, `:65`) does
- possibly `.pre-commit-config.yaml` if the new token is to be *enforced* at
  commit-msg time rather than merely documented

Migration cost: the whole existing history is written in the old convention. Every
past `closes [#N]` either (i) stops being recognised — `validate_git_backlog` runs
over **full history** (`scripts/validate_git_backlog.py:82-100`, and
`audit.py:1278-1315` calls it), so a hard cutover silently re-opens the drift
question for the entire back-catalogue; or (ii) the parser keeps accepting the old
form as legacy, in which case the defect survives for every commit written in the
legacy shape — which is every commit an author writes from muscle memory. Who has to
change: every author, human and agent, plus every doc that teaches the convention.

Honest limit: a convention only binds when something enforces it. Without a
commit-msg gate that *requires* the strict token on closing commits, this option
converts a parser defect into an author-discipline defect — and the incident on record
(`6489391340c4`, `JOURNAL.md:69-74`) was produced by exactly this repo's own
best-informed author. It also does nothing about the second-order `find_weak` effect
until the parser is re-based, and it does not retroactively fix any message.

### Option C — both: strict token forward, negation guard as a backstop

What changes: adopt the strict token as the go-forward declaration (Option B) *and*
add a bounded negation guard (Option A) that protects the legacy `closes [#N]` form
still present in history and in un-retrained habits.

Files touched: the union of A and B, in one lockstep change set — hub parser + plugin
twin + `tests/test_closure_token_quoting.py` + `tests/test_propose_closures_twin_parity.py`
(if the pinned symbol list changes) + `CONTRIBUTING.md` + `protocols/ESSENTIALS.md` +
`protocols/PLAYBOOK.md` + a new design/decision record (the [#437] note is immutable).

Honest limit: the largest surface and the largest review cost of the three, and it
inherits **both** honest limits — the guard is still heuristic and still carries
false-negative risk on legacy-form messages, and the strict token still needs an
enforcement organ to be more than documentation. It also creates a period in which
two closure grammars are simultaneously valid, which is itself a drift surface (the
parser must be tested against both, and a future reader must be told which is
canonical).

### An option deliberately not developed

"Leave it; the `--first-parent` lever already handles it" was checked and does **not**
hold as a general answer. It is true that `validate_git_backlog` passes `--first-parent`
(`scripts/validate_git_backlog.py:15-17`) and that the offending commit `6489391340c4`
is branch-internal — verified: it appears 0 times in `git log --first-parent main`, and
`python scripts/validate_git_backlog.py` currently reports `OK — no closed-but-present
drift`. But `propose_closures.main()` calls `git_log_commits` with the default
`first_parent=False` (`scripts/propose_closures.py:270`, called at `:396`), so the
Stop-hook scanner sees branch-internal text — which is precisely how the live
`{'367': …}` STRONG hit above was produced. And a negated sentence written in a
**merge** commit body lands on the first-parent spine, where the lever gives no
protection at all. Recorded so the architect can price it, not proposed.

---

## Honest limits of this note

- **Scope.** Only `closure_ids` and its two callers were analysed. The commit-msg
  gate `scripts/check_backlog_commit_msg.py` has different, deliberately permissive
  semantics ([#437] design note `:124`) and was not evaluated; whether it should also
  become polarity-aware is not addressed here.
- **The reproduction is of the current working tree**, branch
  `claude/night-2026-07-31-morning-prep-yo7pgw`. The `find_strong` result over
  `main..HEAD` will change as that branch's history changes; the unit-level results
  (`closure_ids('Does NOT close [#367]') == ['367']`) are branch-independent.
- **The lookbehind sketch in Option A is a measurement instrument, not a proposal.**
  It was run only to price the option's residual. It was not written into any source
  file and carries no endorsement.
- **No blast-radius claim about consumer repos was verified.** The plugin ships to
  consumers under ADR-78 carrier doctrine (`tests/test_propose_closures_twin_parity.py:3-8`),
  so a parser change is a fleet-distribution event, but which consumers currently run
  which version was not checked in this pass.
- **No false-negative rate is offered.** Neither option was measured against the full
  commit corpus; doing so would require a labelled sample of real messages, which does
  not exist. Every "still wrong" line above is a single observed string, not a rate.
- **No ticket was filed and no row was closed.** `[#447]` (`BACKLOG.md:29`) uses the
  words "closure polarity" for an unrelated concept and does not own this. Whether
  this becomes a new row is the architect's call.
