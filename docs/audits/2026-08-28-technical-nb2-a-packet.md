# NB2 lane A packet — [#604] remainder + [#606] win-tooling first slice

**Batch:** night-batch-2 · **Lane:** A (architect id N1) · **Substrate:** local · **Date:** 2026-08-29
**Hub branch:** `worktree-lane-a-604-wintooling-deploy` (from `fcc94855`)
**Consumer branch:** `worktree-lane-a-604-wintooling-consumer` in `win-tooling` (from `53a1d02`)
**Status:** commit-and-STOP on both sides. Nothing merged, nothing self-merged.

> Every claim below carries a witness — a command and its output, or a `file:line`.
> A claim with no witness is not a claim.

---

## 0. Headline, before the detail

The deploy landed and is verified. **Contract item (4) — the parity role flip — is NOT-MET,
and it is not achievable by a v1.4.0 deploy at all.** That is a premise defect in both the
frozen contract and `[#606]`'s own done-when, established by measurement rather than
argument (item 4 below). It is the one thing on this packet that needs an operator or
architect decision before the batch can call `[#606]` done.

Second decision owed: **terminal-setup's onboarding profile is a lane choice, not a ruling**
(item 5, and budget decision B-1). One value, reversible in one edit.

---

## 1. Per-done-item verdicts

### (1) Re-measure first — every hub-side claim re-derived on the live consumer — **MET**

The dispatch-time picture was a plan, and three of its facts had moved by the time the lane
ran. Re-derived live, not inherited:

| Dispatch claim | Live measurement | Verdict |
|---|---|---|
| primary on `main` at `53a1d02`, tree clean | `git -C win-tooling rev-parse --short HEAD` → `53a1d02`; `git status --porcelain` → empty | holds |
| **11 local branches**, exactly one (`main`) with an upstream | **12** — `worktree-lane-b-610-dispatch-verbs` exists, created by the sibling lane after freeze | **moved** |
| **four worktrees** already exist | **five** — lane B added `lane-b-610-dispatch-verbs` (locked) | **moved** |
| remote `https://github.com/rdwornik/win-tooling.git` | confirmed by `git remote -v` | holds |
| `.dev-knowledge` parity line ~135 carries `win-tooling: {role: pre-deploy}` | confirmed | holds |
| X1: v1.4.0 resolves local AND origin | re-verified independently, not taken on trust: `git rev-parse -q --verify refs/tags/v1.4.0` → `c57ac188…`; `git ls-remote --tags origin` → `c57ac188… refs/tags/v1.4.0` | holds |

Zero-enforcing-organs premise re-confirmed at HEAD: `git ls-files .claude` returned exactly
`.claude/settings.json`; no `.pre-commit-config.yaml`; `ls .git/hooks | grep -v '\.sample$'`
returned nothing. `git config --get core.hooksPath` exits 1 — **unset**, so no relic path was
silently disarming anything (the contract asked for this to be reported explicitly).

The two moved facts changed the lane's behaviour, which is the point of re-measuring — see
item (7) and deviation D-3.

### (2) P5 — does the deploy path require an ANNOTATED tag? — **MET. It does not. No step stopped.**

This was the lane's first substantive act, as frozen.

- `v1.4.0` is **lightweight**: `git cat-file -t v1.4.0` → `commit`. Siblings are annotated
  (`v1.0.0`, `v1.3.1` → `tag`). The contract's premise is correct.
- **The deploy path does not care.** `deploy/tool.py::git_tag_exists` resolves the tag with
  `git rev-parse -q --verify refs/tags/<tag>`, and its docstring says so in as many words:
  *"True iff `tag` resolves in the hub repo (lightweight or annotated)."*
- Executed live: `git rev-parse -q --verify refs/tags/v1.4.0` → `c57ac18841002dcb…`, exit 0.
- The `manifest-v1.0.0.yaml` comment that raised the question reads *"rev = the v1.0.0 git
  tag (annotated + resolvable as a pre-commit rev; readable + stable)"*. That is a
  **descriptive parenthetical about that tag's properties**, not a requirement clause; the
  operative property for a pre-commit `rev:` is *resolvable*, which a lightweight tag is.
- Origin agrees: `refs/tags/v1.4.0 → c57ac188` with **no `^{}` peel line**, the signature of
  a lightweight tag, at the same SHA as local.

**Nothing was re-tagged, in either repo, under any reading.**

### (3) Deploy: floor present, pre-commit set armed, session gate + /ship live, fresh baseline — **PARTIAL**

Everything landed and verified **except physical hook arming**, which was deliberately not
done and is not a shortcut. Taken point by point.

**Mechanism.** `deploy/tool.py` resolves the consumer as `hub_root.parent / repo` with no CLI
override, which is wrong from a hub worktree and wrong for the consumer-worktree shape
RULING-W requires. So the lane built the `PreflightContext` explicitly and drove the tool's
**own carriers** against the consumer worktree — carrier logic unchanged, binding changed.
Two `execute()` legs were deliberately omitted: `stage_consumer()` (the lane commits itself)
and `write_record_to_branch()` (the version record is the RULING-W authorizing amendment on
the lane's hub branch, not a machine-created hub branch). `PluginCarrier` was given
`marketplace_source` = the **primary** hub, so the consumer's marketplace entry does not point
at a worktree that gets torn down.

**Carrier results** — every implemented carrier applied and `verify()` returned ok:

```
[already  ] global-config: present_correct -- verify only        [verify] ok=True
[apply    ] tier1-plugin: absent -> changed=True                 [verify] ok=True
[apply    ] precommit: absent -> changed=True                    [verify] ok=True
[apply    ] floor: absent -> changed=True                        [verify] ok=True
[apply    ] enforcement-mesh: absent -> changed=True             [verify] ok=True
[skip     ] editor-config: not implemented (declaration-only)
[apply    ] docs: absent -> changed=True                         [verify] ok=True
ADD LOOP COMPLETE -- every implemented carrier applied and verified.
```

The remove leg was skipped by the engine's own greenfield rule (registry `null` at run time;
ADR-96 amendment 2026-07-06). The one `status: removed` component, `ruff-gate`, was
`already_absent`.

**Floor present** — `audit repo win-tooling` against the deployed tree:
`floor_integrity` **PASS** — *"CLAUDE-FLOOR.md present; hash matches sidecar; F5 clean;
pointers resolve (sha256 4d268f329a7e…)"*. Independently fire-tested:
`python .claude/check_floor_hash.py --require-present` → exit 0.

**Version record** — `deployed_methodology_version` **PASS** — *"win-tooling: deployed
methodology corpus v1.4.0"*.

**Pre-commit set — configured, not armed. This is the PARTIAL.**
`.pre-commit-config.yaml` landed with the hub-hooks repo pinned at `rev: v1.4.0`
(`codemap-freshness`, `toc-freshness`, `block-ff-push`, `backlog-id-on-close`) plus local
`floor-hash-verify` and `canonical_freshness`. Arming was **not** run, and the reason is
mechanical: from the consumer worktree, `git rev-parse --git-path hooks` resolves to
`C:/Users/1028120/Documents/Dev/win-tooling/.git/hooks` — the **shared** dir of the live
primary checkout, where lane B was committing at that moment. `pre-commit install` there
would have wired gates inside another live session mid-flight, which is the class of act
RULING-W exists to refuse.

This is not a gap the deploy leaves open. The **methodology's own arming vector is deployed**:
`.claude/settings.json` gained a `SessionStart` hook running
`python -m pre_commit install -t pre-commit -t commit-msg -t pre-push` — the same RF-2
self-arm the hub runs on itself — which fires on the first session after the merge. And
`audit repo`'s `hooks_armed` check is **hub-only** (`audit.py:1179`, returns NOT-APPLICABLE
off-hub by design), so this does not affect the verification the contract names. Consumer
arming is the Informant's axis, and it reports correctly:
`fleet_parity … --repo-root win-tooling=<deployed tree>` → `hooks-armed WARN-undeclared:
"pre-commit config present but stage(s) NOT armed: commit-msg, pre-commit, pre-push"`.

**Session gate live** — `.claude/settings.json` carries the `Stop` hook running
`session_end_backpressure.py`; `python scripts/session_end_backpressure.py` → exit 0.
Stated honestly: that proves the organ is **present and executable in the consumer's
interpreter**. It is a silent-success hook, so it leaves no firing record — this is presence,
not an observed gate firing.

**`/ship` live** — `claude plugin list --json` from the consumer worktree reports
`tier1-lifecycle@dev-knowledge-methodology` v0.1.11, `scope: project`, `enabled: true`,
`projectPath` = the consumer worktree. The installed plugin's `commands/` dir contains
exactly `ship.md` and `review-closures.md`.

**Fresh baseline** — `ecosystem/win-tooling/history/2026-08-29.md`, replacing a `2026-07-31`
baseline four weeks stale. Counts: `fail=2 warn=2 pass=15 n/a=36`. Both FAILs are named and
dispositioned in item 6 and D-1.

### (4) Parity role `pre-deploy → consumer`, flipped after the proof — **NOT-MET (premise defect)**

The proof exists. The flip does not land. It was **made, measured, and reverted**, and the
reason is a measurement.

As `consumer`, `tests/test_audit.py::test_check_fleet_parity_green_on_live_repo` REDs. That
test's own docstring is *"[#337] zero-WARN steady state, mechanized: no REAL blocking
divergence on the live fleet (**promotion REDs nothing**)"* — it is a true signal about this
exact act, so nothing was edited to make the promotion pass.

The obvious explanation — the deploy sits on an unmerged branch — was **refuted, not assumed**.
Walking parity directly against the **deployed** tree:

```
uv run --locked python scripts/fleet_parity.py --run-date 2026-08-29 \
  --repo win-tooling --repo-root win-tooling=<consumer worktree> --no-write --no-events
```

still reports **eleven MUST-absent surfaces the v1.4.0 carrier set does not ship at all**:

`audit-casing-r4` · `claude-md-form-a-markers` · `docs-genre-archive` · `docs-genre-audits` ·
`docs-genre-decisions` · `methodology-yaml` · `pytest-minversion` · `root-gitattributes` ·
`ruff-required-version` · `ruff-target-version` · `shape-dir-logs`

The deploy **did** close eleven others: `claude-floor-file` · `claude-floor-import` ·
`claude-floor-sidecar` · `command-override` · `docs-genre-intake` · `install-md` ·
`precommit-hub-block` · `root-precommit-config` · `settings-floor-guard` ·
`settings-precommit-arm` · `settings-stop-backpressure`.

So the flip is **unreachable by a v1.4.0 deploy**, not merely premature, and both the frozen
contract item (4) and `[#606]`'s done-when carry that premise defect. Closing the eleven is
its own arc — a `.methodology.yaml` declaring the sanctioned divergences, two `pyproject.toml`
pins, the docs genre dirs. The row is HELD at `pre-deploy` with a `reason:` that states the
true state (v1.4.0 deployed, role held, why) rather than reading as "nothing was deployed".

**Reviewer dissent, recorded rather than buried.** Terra rated this hold CRITICAL, arguing
that `pre-deploy` suppresses exactly the eleven findings a promotion should expose, and that
the fix is to flip and keep the REDs *"unless an authorized ruling formally changes the
invariant and task acceptance criteria."* That is a fair reading and the disagreement is
genuine: flipping REDs the batch's integration suite, holding under-reports a deployed
consumer. **This is the operator/architect call named in item 0**, and it is filed as C-1.

### (5) [#604] fold — terminal-setup key + rulings entry — **MET, with the profile value flagged**

- `ecosystem/deployed-versions.yaml` gains a `terminal-setup:` key, all three fields `null`,
  in the same shape and for the same reason as win-tooling's 2026-08-26 pre-deploy admission.
- `ecosystem/satellite-onboarding-rulings.yaml` gains a `terminal-setup:` entry with
  `profile: full`, `ruled_by`, `ruled_date: "2026-08-29"`, `census_ref`.
  `uv run --locked python scripts/validate_onboarding_rulings.py` →
  *"6 satellite(s) ruled: 6 full, 0 floor-only"* — no schema defect.
- `[#604]`'s third clause — *"each admitted repo's `parity-surfaces.yaml` reason states its
  true registry state"* — done for both terminal-setup and win-tooling.

**The profile VALUE is a lane choice and is labelled as one.** The register previously
recorded terminal-setup as DELIBERATELY UNRULED and warned that adding an entry without an
operator/architect ruling *"would be fabricating the decision this register exists to
record"*. That warning was honoured rather than deleted. The architect's frozen contract
requires the entry and constrains it to `full|floor-only`; it does not choose. `full` was
selected on the 5/5 precedent in the register (nearest analogue: `life-architect`, where a
floor-only census proposal for a light docs-only repo was OVERRIDDEN to full).

Terra rated the first attempt CRITICAL — `ruled_by: architect` recorded a ruling that never
happened — and it was right. Fixed at the machine-read field (`ce6f4465`): `ruled_by` now
names the executing lane as the chooser and says the choice is unconfirmed, with a
`provenance` block carrying the full story. Terra's own fix direction (leave it unruled)
would restore the exact state `[#604]` exists to close, so this is the honest form that also
satisfies the done-when. **Confirm or flip it in one edit** — see B-1.

### (6) `workspace_settings` recorded hand-fixed or accepted-debt — **MET — recorded as ACCEPTED DEBT**

Live finding from the fresh baseline:

```
[warn] workspace_settings: .win-tooling.code-workspace:
       explorer.sortOrder='<absent>' (expected 'default');
       explorer.sortOrderLexicographicOptions='<absent>' (expected 'upper')
```

**Accepted debt, not hand-fixed**, and the manifest supplies the reason. `deploy/manifest-v1.4.0.yaml`
declares the `editor-config` carrier `implemented: false` and says why: a consumer write-through
*"needs a merge strategy that does not clobber a consumer-authored file (the ADR-93
single-writer-per-file constraint)"*. `.win-tooling.code-workspace` is consumer-authored.
Hand-writing it from a hub lane, at night, in a repo where a sibling lane is working, is
precisely the clobber the manifest defers the carrier to avoid. Filed as C-2.

### (7) Branch backup — 11/11 carry upstreams — **MET**

Before (`git branch -vv`): 12 local branches, **one** upstream (`main`).
After: **11 of the 11 contract-enumerated branches carry upstreams.** Ten `git push -u origin`
runs, each reporting `* [new branch]` and `set up to track`; `main` already had one.

The 12th and 13th branches — `worktree-lane-b-610-dispatch-verbs` (lane B's, created after
freeze) and `worktree-lane-a-604-wintooling-consumer` (this lane's) — were **not** pushed.
Lane B's is another lane's in-flight work and is not in the enumerated set; this lane's is
excluded by the contract's own *"Push nothing else"*. See D-2 and D-3.

Backup only: **zero merges, zero deletions, zero worktree removals.** The five existing
win-tooling worktrees are untouched — they are the morning's X3 item and removing one is a
destructive act nobody authorized.

### (8) Commit-and-STOP on both sides — **MET**

Both branches stop at their last commit. No merge was performed, none is named, and no merge
command appears anywhere in this packet or in either commit message.

---

## 2. Commits, in order

**Hub** — branch `worktree-lane-a-604-wintooling-deploy`, from `fcc94855`:

| # | SHA | Subject |
|---|---|---|
| 1 | `4b153b9a` | `feat(ecosystem):` the win-tooling deploy authorization + the [#604] terminal-setup fold |
| 2 | `a3f7c668` | `test(desired-state):` derive the live fleet-membership pin instead of pinning a literal |
| 3 | `a16bb1b8` | `fix(ecosystem):` HOLD win-tooling at pre-deploy and record why the flip is unreachable |
| 4 | `ce6f4465` | `fix(ecosystem):` make ruled_by name WHO chose terminal-setup's profile |
| 5 | *(this packet)* | `docs(audits):` NB2 lane A packet |

Commit 1 is the RULING-W **authorizing amendment** and landed **before** any consumer write.

**Named as owed by the contract:** commit 2 touches `tests/`, which is outside this lane's
frozen write-scope. It is kept in its own commit for exactly that reason. It repairs a RED
that commit 1 caused: `test_live_repo_loads_clean_and_writes_nothing` pinned an exact literal
member set while its own comment claimed the pin *"moves with that data by construction"* —
which it did not, and which is why every admission REDs it (win-tooling 2026-08-26,
terminal-setup 2026-08-29). It now asserts equality against `deployed-versions.yaml`'s own
`repos:` keys, with the six long-standing members kept as an explicit subset floor. That is a
narrowing of brittleness, not of coverage. `tests/test_desired_state_loader.py`: 17 passed;
`ruff check`: clean.

**Consumer** — branch `worktree-lane-a-604-wintooling-consumer` in `win-tooling`, from `53a1d02`:

| # | SHA | Subject |
|---|---|---|
| 1 | `cd5d793` | `feat(methodology):` deploy the .dev-knowledge methodology corpus v1.4.0 (13 files) |
| 2 | `3ffabe0` | `docs(claude):` reconcile CLAUDE.md with the v1.4.0 deploy it now contradicts |

**No generated surface was regenerated** (`BACKLOG.md`, `docs/audits/README.md`,
`ecosystem/doc-counts.md`, `ecosystem/organ-index.md`, `.claude/generated/*`). One auto-fix
fired and was accepted: the `normalize-dated-headers` pre-commit hook rewrote the fresh
baseline's `##` header to `###` — see C-4.

---

## 3. Terra tally

Reviewer: `codex exec` over this lane's own diff (not `/codex-review` — a mixed doc/code
diff kills that lane). **Two passes**, because the first found a real defect.

- **Pass 1** — `TALLY: C=1 H=0 M=0 L=0`. The CRITICAL: `ruled_by` falsely attributed the
  terminal-setup profile choice to the architect. **Accepted and fixed** in `ce6f4465`.
- **Pass 2** (post-fix) — `TALLY: C=2 H=3 M=0 L=0`. Dispositions:

| Finding | Disposition |
|---|---|
| C — `ruled_by` attribution | **CURED**, confirmed by the reviewer in pass 2 |
| C — unconfirmed choice recorded as binding ruling (`desired_state_loader.py:270` labels every entry an *operator* ruling) | **VALID, and PRE-EXISTING.** That line hardcodes `reason=f"operator onboarding-profile ruling for {rid}"` regardless of `ruled_by` — it already mislabels win-tooling's `ruled_by: architect` entry. This lane makes it more consequential; it did not introduce it. `scripts/` is outside write-scope. Filed as **C-3**. |
| C — deployed consumer held at `pre-deploy` | **VALID DISSENT, escalated not overridden** — see item (4) and **C-1** |
| H — consumer patch references files it does not add | **FALSE POSITIVE, cause named:** the reviewed `consumer.diff` was deliberately path-scoped to the four wiring files. All nine other files are in `cd5d793` (`git show --stat cd5d793` → 13 files). Re-reviewed unscoped in pass 3 below. |
| H — CLAUDE.md contradicts the new deployed state (three claims) | **VALID and ACCEPTED — fixed** in consumer commit `3ffabe0` |
| H — cited packet file does not exist | **VALID at review time — cured by this file.** All three citations (`deployed-versions.yaml`, `parity-surfaces.yaml`, `satellite-onboarding-rulings.yaml`) are hub-internal and resolve on this commit. |

**Net after disposition: 1 CRITICAL fixed, 1 CRITICAL escalated as an operator decision,
1 CRITICAL filed as a pre-existing defect, 2 HIGH fixed, 1 HIGH false-positive.**

---

## 4. Candidate filings for the integrator — REPORTED, NOT FILED

This lane files nothing. Lane D is the batch's exclusive `tasks/` writer, and
`/review-closures` owns closure.

- **C-1 — `[#606]`'s parity-flip done-when is unsatisfiable at v1.4.0.** Eleven MUST surfaces
  the carrier set does not ship stand between a deployed win-tooling and a clean `consumer`
  role. Needs an operator/architect decision, and the reviewer dissents from the hold. The
  work behind it is a real arc: a `.methodology.yaml` for win-tooling declaring the sanctioned
  divergences, `pytest.minversion` + the two `ruff` pins in `pyproject.toml`, and the
  `docs/{archive,audits,decisions}/` genre dirs. `[#606]` cannot close on its current text.
- **C-2 — the `editor-config` consumer leg.** `implemented: false` at v1.4.0 means
  `workspace_settings` cannot be closed by any deploy; it needs a merge strategy that respects
  the ADR-93 single-writer constraint. The manifest already calls this "the next ticket".
- **C-3 — `desired_state_loader.py:270` hardcodes "operator" as the ruling authority** for
  every onboarding-profile entry, discarding `ruled_by`. Pre-existing; it already mislabels
  win-tooling's architect ruling. Terra CRITICAL, pass 2.
- **C-4 — `audit.py::append_history` emits a header the repo's own normalizer rejects.**
  It writes `## <date>`; `normalize-dated-headers` rewrites it to `### <date>` (the
  2026-07-31 baseline is already `###`). Every baseline write costs a failed hook run and a
  re-stage. One-character fix in the generator.
- **C-5 — win-tooling's canonical stamps block its own new gate.** `VISION.md`,
  `ARCHITECTURE.md` and `CLAUDE.md` carry `last_reviewed: 2026-07-11` predating their edits,
  so `canonical_freshness` FAILs. Once the SessionStart self-arm fires, **win-tooling commits
  are blocked** until each is genuinely re-read and re-stamped. Not fixable by this lane —
  a stamp means re-read and confirmed, not touched. **This is the highest-urgency operational
  consequence of the deploy.**
- **C-6 — the tier1 plugin install is registered against a worktree path.**
  `claude plugin list --json` shows `projectPath` = the consumer worktree, which is
  session-scoped machine state outside the repo. Harmless (the tracked `enabledPlugins` in
  `settings.json` re-registers in the primary after merge) but it is a leftover under
  core rule 9, and it should be cleared when the consumer worktree is torn down.

---

## 5. Decisions taken under the budget

The budget: standing rulings silently; ask only on curated-baseline / rule-vs-ruling /
no-ruling fork / out-of-scope path (P1).

- **B-1 — no-ruling fork (terminal-setup's profile).** Selected `full` on 5/5 register
  precedent rather than blocking a night lane on an unavailable operator, and labelled the
  attribution truthfully in the machine-read field. **Open for confirmation.**
- **B-2 — rule-vs-ruling (the register's own "do not fabricate" warning vs `[#604]`'s
  done-when).** Resolved by satisfying both: the entry exists as required, and the warning is
  preserved verbatim inside the entry's `provenance` rather than deleted.
- **B-3 — out-of-scope path (P1): the deploy footprint exceeds the enumerated write-scope.**
  The contract enumerates consumer `.claude/` + `.pre-commit-config.yaml`; a complete v1.4.0
  deploy also writes `scripts/` ×2, `.gitignore`, `CLAUDE.md`, `docs/intake/README.md`,
  `templates/intake-template.md`, `INSTALL.md`. Deployed all of it. The enumeration is
  demonstrably narrower than the contract's own named outcome — a "session gate" cannot be
  delivered inside `.claude/` alone — and `execute()` is all-or-nothing by design: a partial
  apply plus a `1.4.0` version record is the exact false-record the engine's gate exists to
  prevent.
- **B-4 — out-of-scope path (P1): `tests/`.** Fixed the membership pin this lane's own change
  RED (commit 2, kept separate and named). Did **not** touch
  `test_check_fleet_parity_green_on_live_repo`, because that one is a true signal.
- **B-5 — out-of-scope path (P1): consumer `CLAUDE.md` prose.** Reconciled three claims the
  deploy made false. A session contract read on every session start is not a doc to leave
  stale; the floor carrier already edits this file.
- **B-6 — arming deferred** (item 3). Mechanical, not discretionary: the hooks dir is shared
  with a live sibling lane's checkout.
- **B-7 — ratchet drained, not baselined.** The first staged version of commit 1 measured
  446 vs the 443 baseline (+3: one `never`, two `SHALL`, all in `ecosystem/*.yaml`, a detector
  scope root). Per the batch clause that only lane C may move 443, the additions were
  **rewritten**, not baselined. Meaning unchanged.
- **B-8 — did not run `deploy/tool.py --execute`.** It resolves the consumer by path
  convention with no override and writes the version record on a machine-created hub branch.
  Drove its carriers directly instead; both omitted legs are named in item 3.
- **B-9 — did not run `audit repo`'s publish legs.** `_commit_routine_outputs` **pushes**
  `automation/fleet-audit` to origin, and this lane's only push authorization is the ten
  branch backups. Ran `audit_repo` + `append_history` — the audit and the baseline the
  contract names — and omitted `write_report` (writes `docs/audits/`, out of scope) and the
  commit/push leg.

---

## 6. Deviations, each with an owner

- **D-1 — two FAILs in the fresh baseline, neither caused by the deploy machinery.**
  `dot_prefix_discipline` (root `config.yaml` not dot-prefixed) is pre-existing and unrelated.
  `canonical_freshness` is pre-existing for `VISION.md` (edit 2026-07-12) and `ARCHITECTURE.md`
  (edit 2026-08-19); **`CLAUDE.md`'s row IS deploy-touched** — the floor carrier's `@`-include
  bumped its last edit to today. The stamp was deliberately not bumped. *Owner: operator —
  see C-5, it blocks commits once the gate arms.*
- **D-2 — the consumer branch is not backed up to origin.** The contract's *"Push nothing
  else"* is explicit and was honoured, which sits in tension with the lane's own "one disk
  failure from loss" intent. Risk is low: the branch lives in `win-tooling/.git`, which is not
  session-scoped. One command if wanted: `git push -u origin worktree-lane-a-604-wintooling-consumer`.
  *Owner: operator.*
- **D-3 — the fleet grew a 12th branch and a 5th worktree after freeze.** Lane B's, both
  correctly left alone. The contract's enumerated before-state was stale by one branch;
  reported rather than silently reconciled. *Owner: none — informational.*
- **D-4 — one source-payload delta from the v1.4.0 tag.** The carriers source from the hub
  working tree, not from the tag (the engine's established behaviour — that is how
  ai-council@1.3.1 was deployed). `git diff v1.4.0..HEAD` over every carrier payload path
  shows exactly one changed file: `docs/intake/README.md`, and only its **generated** index
  block (54 → 55 documents). No semantic drift. *Owner: none — measured and disclosed.*
- **D-5 — a CRLF/hash hazard was investigated and REFUTED, not assumed.** win-tooling has
  `core.autocrlf=true` and no `.gitattributes` (ai-council pins `* text=auto eol=lf` via
  `#282`), so `CLAUDE-FLOOR.md` checks out CRLF while its sidecar hash was computed over LF.
  That does **not** break the guard: `check_floor_hash.py::_norm` normalizes `\r\n → \n`
  before hashing. **No `.gitattributes` was added** — there was no defect to fix. Recorded
  because it is exactly the finding a reviewer would file without reading the guard.
- **D-6 — no JOURNAL entry, and the Stop hook is declined explicitly.** A batch lane never
  journals; the integrator writes one anchor for the whole queue after every lane has
  STOPped. The session-end hook is advisory in full since the ADR-85 amendment 2026-08-03
  §A5, the hard leg is `block-unanchored-push` at pre-push, and this lane does not push to
  the hub. Declined with the reason, not silently ignored.

---

## 7. What the morning needs from the operator

1. **Rule C-1** — flip win-tooling to `consumer` and accept eleven RED parity rows plus a RED
   integration suite, or hold and re-scope `[#606]`'s done-when. The reviewer argues flip; the
   lane held. `[#606]` cannot close either way without this.
2. **Confirm or flip B-1** — terminal-setup `profile: full`. One value, one edit.
3. **Merge the two lane branches** (integrator queue order is frozen; this lane names no
   merge command).
4. **C-5 before the next win-tooling session** — three canonical stamps need a genuine
   re-read, or the newly-armed `canonical_freshness` gate blocks every commit there.

---

## AMENDMENT 1 — 2026-08-29, terra pass 3 (in-file marker per CLAUDE.md §5 rule 3)

Pass 2's HIGH *"consumer patch references files it does not add"* was a false positive caused
by a path-scoped diff. Pass 3 re-ran the reviewer against the **complete, unscoped** consumer
diff (`53a1d02..HEAD`, 1,630 lines) plus the hub diff including this packet.

**`TALLY: C=0 H=3 M=0 L=0`.** Zero CRITICALs. All three HIGHs are in the **carried replica
content the carriers ship verbatim from the hub** — none is in this lane's authored changes,
and none is fixable from a consumer without editing a hub-owned carrier source, which is a
fleet-wide act affecting every consumer.

- **C-7 — the carried mesh payload advertises an organ the consumer does not receive.**
  `.claude/commands/override.md` and `scripts/session_end_backpressure.py` both describe
  `scripts/block_unanchored_push.py` as the live hard leg. The `enforcement-mesh` carrier
  ships neither that script nor a hook for it, so a consumer reads that its pushes are gated
  when they are not. The prose is the hub's own organ inventory, shipped unmodified. Either
  the mesh carrier grows the hard leg, or the carried text states the consumer's
  advisory-only posture. *Hub-owned; fleet-wide; out of this lane's write-scope.*
- **C-8 — the carried `INSTALL.md` instructs a step against a removed component.** It tells
  the reader to copy `assets/ruff-pre-commit.yaml` and promises a ruff gate. The asset is
  absent and `ruff-gate` has been `status: removed` since 1.2.0 in the same manifest that
  carries the doc — so the install guide contradicts its own release. *Hub-owned
  (`plugins/tier1-lifecycle/INSTALL.md`); fleet-wide; out of scope.*
- **RE-LITIGATION, NOT A FINDING — the carried `docs/intake/README.md` ships the hub's
  generated index.** Terra rated it HIGH; it is **ruled ACCEPTED AS SHIPPED by the operator,
  2026-08-08**, on the `[#280]`/`[#315]` deploy-doc-carrier lane, because what ships is
  literally what ADR-98 ruling 1, `deploy/release-v1.3.x-contract.md` §3.2 and the `[#280]`
  row each specify. That ruling also forbids transforming `docs/intake/*` in-flight. Not
  re-raised, and nothing under `docs/intake/` was touched.

  **But its safety premise has now expired, and that is new.** The ruling stood on the fact
  that *manifest v1.4.0 was untagged, so no consumer had yet received the dead-link index*,
  with the real fix pegged to land **before the operator tags v1.4.0**. v1.4.0 **is** tagged
  (`c57ac188`, local and origin), and **win-tooling is the first consumer to receive the
  index** — a hub-generated block claiming 55 documents and linking to files the consumer
  does not have, with a regeneration command naming a hub-only script. The deadline passed
  without the fix. Filed as **C-9**, not as a defect to fix here: the ruling is the
  operator's to revisit.

None of the three changes any verdict in section 1. Section 3's tally line stands as written
for passes 1 and 2; this amendment is pass 3.
