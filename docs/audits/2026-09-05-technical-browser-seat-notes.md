# Browser seat notes — outgoing window 2026-09-02 -> 2026-09-05 (landed verbatim)

> **Genre: landed external artifact.** Everything below the rule is the outgoing Layer-1
> browser architect's own handover note, landed **unmodified**. This header is the only
> hub-authored text in the file; nothing in the body was edited, reordered or summarized.
>
> **Integrity.** The source arrived LF-terminated, so the body needed no line-ending
> normalization and the landing is byte-identical — one digest, not the two-hash form a
> CRLF source would have forced:
>
> ```
> source, as authored (LF)   10,483 B   sha256 685633c33c49c7d37de5dba70f3162d4d1841a98b12896ee8d28ee465f06b196
> body, as landed  (LF)      10,483 B   sha256 685633c33c49c7d37de5dba70f3162d4d1841a98b12896ee8d28ee465f06b196
> ```
>
> The builder asserts the digest before writing and asserts that the landed file **ends
> with** the body, so "unmodified" is a checkable fact rather than a promise.
>
> **Provenance.** Authored by the Layer-1 browser architect (Fable) on the bundle
> `2026-09-01-dev-knowledge-architect-v7`; addressed to the next browser seat via CC.
> Landed by lane `worktree-docs-seat-notes` on operator instruction.
>
> **What this document is NOT.** It is not a plan, not a ruling and not a triaged finding
> set. Its own preamble says so, and §4 explicitly separates rulings that LANDED from
> those **owed to the repo** — this lane verified neither class. A reader acting on any
> line here resolves its locator first (CLAUDE.md §4, `/preflight`).
>
> **Derived filings, per ADR-111 (CANDIDATE -> intake -> ratification).** Three sections
> were routed onward in the same commit; the rest of the document is carried as context
> only, with no triage claimed:
>
> - **§2** (ten v7.1 deltas) -> intake **#68**,
>   `docs/intake/2026-09-05-tech-handoff-process-v71-amendment-pack.md` — status DRAFT.
>   Filed as a CANDIDATE **amendment pack**, deliberately with **no version bump**: §2's
>   own heading says *"file through the funnel; not a bump by fiat"*.
> - **§3** (the prioritisation order) -> intake **#69**,
>   `docs/intake/2026-09-05-tech-boot-frontier-prioritisation-weights.md` — status DRAFT.
>   Scoped to class weights inside `boot_frontier.default_score`'s existing `ScoreFn`
>   seam; **not a new script**.
> - **§6** (five one-line lessons) -> `LESSONS.md`, five entries, prepended per that
>   file's newest-first rule.
>
> §1 (the error register), §4 (rulings landed and owed) and §5 (open threads) are landed
> here and routed nowhere. They are the incoming seat's reading, not this lane's.

---

# BROWSER SEAT NOTES — window 2026-09-02 → 2026-09-05 (outgoing)

From: Layer-1 browser architect (Fable), window booted on bundle `2026-09-01-dev-knowledge-architect-v7`.
To: the next browser seat, via CC. Everything here is either witnessed in this window or marked OPINION.
Not a plan. Batch G is closed; H0-prep, R5, AJ, corpus audit, #627, groom and the Python arc are in flight.

---

## 1. ERROR REGISTER — this seat, this window (the recorded error class, extended)

Sixteen defects, six classes. Class A alone caused the 9-lanes → 3-closures result.

| # | Defect | Class | Cost | Mechanism that would have caught it |
|---|---|---|---|---|
| 1 | Contract closures cut from close-packet §3 (terra's defect text), not from each row's Done-when | A premise-from-summary | 9 lanes, 3 rows closed | freeze gate refuses a closure clause not quoting the owning row's Done-when |
| 2 | #629 and #630 conflated into one lane; both rows said they were separate | A | #629 untouched, 99 commits | same as 1 |
| 3 | G3 write-scope frozen without a coupling scan (fallback literal, release_lint C7) | B unwitnessed footprint | 2 escalations, G3b cut mid-batch | freeze-gate coupling scan: every symbol in the contract grepped; referencing files in scope or excluded |
| 4 | "ship-gate GREEN at G0" — did not know undispositioned WARNs RED the gate | A | G0 STOP, ruling R-G0-1 | bundle carries the gate's RED conditions in one line |
| 5 | `lastfailed` cited as current base set — a day-stale superset (45 vs 13) | A | R-G0-3 | base set from the run report, never a cache (now doctrine) |
| 6 | Per-lane full-suite delta A2 — duplicated the integrator's run; 7 concurrent suites, 550 MB free | C concurrency model | hours lost, R-G-A2 | targeted tests in lanes; delta once at merge (now in CLAUDE.md §4) |
| 7 | "G3 merged before G6" written as a boot precondition; lanes run in parallel | C | G6 paused | contract template separates BOOT preconditions from INTEGRATION order |
| 8 | #634 ruled from AMENDMENT 2; win-tooling had fixed it 4 days earlier (d6cbd92) | A cross-repo stale premise | L2 retired, row rescoped | bundle carries last-commit-touching for every cross-repo file the agenda names |
| 9 | Hotfix criterion "133 → ≤123" — clock-sensitive (doc_rot moves with the date) | E criterion design | re-ruled to 19 named findings | closure criteria name findings, never aggregate counts |
| 10 | "ceiling-12" cited as ADR-110 (it is SUPPLEMENT:90); PARKED item filed as a BACKLOG row (funnel violation) | A | corrected at freeze | resolve-a-locator applies to the architect |
| 11 | Read-only arcs (R5 prep, corpus audit) sent LOCAL; doctrine says read-only = CLOUD | F doctrine inertia | contention on the operator's host | the dispatch verb is derived from the arc class, printed in the contract header |
| 12 | "git mv, byte-identical" for gitignored logs (untracked) | B | harmless, reported | witness tracked-ness before prescribing git verbs |
| 13 | NC4 tied #611 (bundle size) to the v1.5.0 tag with no ruling behind it | A | operator asked to decide | NC lists cite the ruling per condition |
| 14 | Two CC pastes re-emitted for form: dangling "delete them"; browser-side path; description instead of copy-ready block | D interface | operator time ×2 | OPERATOR-INTERFACE §7 (now filed) + form probe candidate |
| 15 | Allowed six sessions on the primary checkout until the TOCTOU put a commit on main under a passing gate | C | one recovered commit | primary is integrator-only (candidate: SessionStart refusal) |
| 16 | Step 0 (~/.claude commit) implied as progress on NC1; measured: still diverge 4/4 | A | none, CC flagged | a precondition is not progress — say which |

Root cause across A: the seat read **summaries and defect reports** where the row's Done-when and the live file were one pull away. The bundle made this easy by carrying §3 of the close packet and not the rows.

---

## 2. WHAT THE v7 BUNDLE DID NOT CARRY — deltas for v7.1 (file through the funnel; not a bump by fiat)

1. **Rows on the agenda: Done-when VERBATIM**, one block per row, with the row's file path. The close-packet defect text is context, never the closure source.
2. **Gate semantics in one line each**: what REDs ship-gate (hard-fail organs OR undispositioned WARN count), what the Stop hook can block (nothing), what pre-push blocks (unanchored range). The seat ruled on gates it had not read.
3. **Cross-repo state for every path the agenda names**: `git log -1` in win-tooling for dispatch helpers; the L0 (`~/.claude`) dirty-file list. Two rulings this window were stale on cross-repo facts.
4. **Substrate block, rewritten**: the three verbs with the doctrine line; base failed-set PER SUBSTRATE with its source rule (run report); the current hold (if any) with its row id; the last codespace witness SHA.
5. **Live-session census**: which session holds the primary, which worktrees are live and whose. The seat could not see six concurrent writers.
6. **Coupling-scan output for the agenda's symbols** (or a probe row that runs it): the files that reference each constant/function the agenda will touch.
7. **Scorecard section** (ten numbers, candidate under `window_metrics.py`): rows closed/touched · hard-fail + WARN with trend · failing nodeids + baseline seconds · P1 pre-merge / regressions at merge · time-to-merge per lane · % lanes on codespace · asks RED/re-asked · bundle bytes + window-specific % · consumers at 0 FAIL · tokens by model class. Numbers in the bundle name the SHA they were measured at.
8. **Interface behaviours**, not only constants (Q7 extension landed in G7 clause 5): copy-ready blocks, .md transport, END sentinel, Downloads fallback, "which session tile" naming.
9. **Probe prose once** (G7 landed the measure: cut 29,776 B / 32 % window-specific against 20 KB / 70 %). The next cut should show the trend line, not just the miss.
10. **Providers used vs promised**, per window: this window — terra used (8 reviews, 10 P1); Gemini used ONCE with measured fidelity (6/6 locators, 0 fabrications, 1 overclaim of files read); Grok not admitted; sol unconfirmed on G7; codespace used once (G5) then held.

---

## 3. BOOT — what would make the next seat faster (OPINION, with the measured basis)

- **Verify → orient in one command** (`/boot-session` merge-with-verify, PARKED by the operator as a CANDIDATE). Basis: this window needed three operator pastes (handoff-verify, boot-session, evidence) before the first ruling. One command, RED-verify = STOP, would cut that to one.
- **Prioritisation is a sort, not an engine** (library-first: no new scorer). `boot_frontier` today scores P1 flow rows. Proposed order, computed from surfaces that already exist:
  1. rows whose Done-when is already witnessed on main (`propose_closures`) — cost ≈ 0, closure rate ↑ first;
  2. rows on the current NC list for the next tag/H0 (the agenda), by NC order;
  3. rows unblocking a held substrate or provider (holds like [#634]);
  4. P1 by serialize-group disjointness (today's frontier);
  5. everything else.
  Batch G's divergence (frontier proposed 5 rows, none on the agenda) is the measured defect this fixes. Implementation: a weight per class in `boot_frontier`, not a new script.
- **The equilibrium metric**: "needs input" events per batch. Batch G: ~10, of which 7 traced to architect premise errors (§1). Target for the next batch: ≤ 3. The browser emits intent + Done-when-quoted closure + mode; the repo emits the batch proposal with the coupling scan attached; the browser rules. Fewer questions is the number that says the equilibrium moved.
- **Skills over reference**: PLAYBOOK Ch8 (dispatch) and Ch12 (contracts) as CC skills loaded on trigger, not grepped from a 3000-line file. Not ruled; the corpus audit and the AJ gap analysis should say whether the outside harness does it this way.

---

## 4. RULINGS MADE IN CHAT THIS WINDOW — landed or owed

Landed (SHA-witnessed by CC): R1 routing carrier + R-2 reason (1e064921); R-G0-1..4; R-G-A2 (CLAUDE.md §4); R-G-G3b; #634 rescoped (win-tooling owner); #630/#276 closed; interface constant §7 + Z-C candidates; retention per-run grammar; PLAYBOOK ESSENTIALS routes 8 → 0.
Owed to the repo (verify at boot, do not assume): H order (g corpus audit → R5 window → tag → H0 → TRACE → derived-copies registry → rest) — recorded in the batch-G packet §11 as proposal; NC4 (#611) downgraded to non-tag-blocking (operator's decision, taken in chat, not yet written); read-only = CLOUD by verb, execution = CODESPACE after the [#634] hold was lifted (in chat, L2 dispatcher session); primary = integrator-only (integrator-2 notice, candidate filed?).

---

## 5. OPEN THREADS at wrap (deliverables land on branches; integrator-2 merges)

| Session | Returns | Then |
|---|---|---|
| integrator-2 | merges: corpus audit, hotfix 19-findings, doc_claims tiering, then queue | close packet with scorecard by hand |
| R5 disposition sheet | ≤12 bundles + GROWTH section | browser rules by bundle; operator declares; ship-gate GREEN is the tag gate |
| AJ gap analysis | gap doc + ≤10 CANDIDATEs (P1 → P6 running) | browser rules classification; candidates → intake |
| #627 re-adjudication | RATIFY / FLIP / INCONCLUSIVE + retrieval-fidelity test | routing-table decision if FLIP |
| funnel groom | ≤12 bundles (CLOSE/ARCHIVE/MERGE/REWORD/AMEND-ADR incl. ADR-110 §2) | operator rules; serial execution |
| H0-prep L5 → L4 → L3 (codespace) | suite speed number; logs/prompts traces; README front door | witnesses: 3 lanes ran in codespace, `gh codespace list` empty, traces openable |
| Python quality & speed research | I/O vs CPU split; audit.py decomposition map; python-style skill candidate | browser rules on Fable |

Tag v1.5.0 gate = NC1 (ship-gate GREEN after R5) + NC3 (#628 residual: CLAUDE.md first-read line 2, fleet-coupled release edit) + NC6 witnesses. Then H0 monorepo attended.

---

## 6. ONE-LINE LESSONS (append-only candidates, for LESSONS.md)
- A closure clause that does not quote the row's Done-when closes a defect, not a row.
- A criterion that the calendar can pass or fail is not a criterion.
- A precondition is not progress; say which one you delivered.
- Six sessions in one checkout is a race, not parallelism — worktrees are the unit, the primary is the integrator's.
- Read-only goes to the cloud by verb; the operator's host is for integration and explicit exceptions.

---

## AMENDMENT 1 — two further class-A defects, recorded after landing (2026-09-05)

> **This is an in-file amendment marker, not an edit.** Audits are immutable (critical rule
> 3): the register above is the outgoing seat's own text and **nothing in it has been
> altered** — no row added, renumbered or reworded. The two defects below arrived separately,
> from the architect inbox (item **005-D**), after this file was committed at `0c57e765`.
> They continue the register's own numbering because they belong to the same window and the
> same class, but they were **not written by the seat** and a reader must not attribute them
> to it.
>
> **Integrity claim, restated — the header above is now imprecise and is corrected here
> rather than edited.** That header says the builder asserted the landed file *"ends with"*
> the body. That was true at `0c57e765` and is false now, because this amendment sits below
> the body. The checkable claim going forward: the verbatim body is the **contiguous region
> from the line `# BROWSER SEAT NOTES` down to the blank line preceding this amendment's
> `---` rule**, and that region still hashes to
> `sha256 685633c33c49c7d37de5dba70f3162d4d1841a98b12896ee8d28ee465f06b196`, unchanged. The
> original tail form remains verifiable in history at
> `git show 0c57e765:docs/audits/2026-09-05-technical-browser-seat-notes.md`.

| # | Defect | Class | Mechanism that would have caught it |
|---|---|---|---|
| 17 | "channel is alive / nothing to paste" asserted without reading `to-browser\` | A premise-from-summary | the read rule is executed, not recalled — a claim about a directory's contents names the listing that produced it |
| 18 | a research brief carried a stale premise (mutation gate `<300 s`, superseded) and asked for a **computed** row to be quoted **as stored** | A premise-from-summary | a brief's premises are resolved at freeze; a value that is derived is cited by the surface that computes it, never restated as a stored fact |

Both are **class A** on the register's own taxonomy — the same premise-from-summary root
cause the seat identified as the window's dominant class. That is the point of recording
them here rather than elsewhere: the register's own conclusion is that class A accounted for
the largest share of the window's cost, and these two extend that count rather than opening a
new class. Neither is triaged by this lane, and neither becomes a backlog row without ADR-111
intake.

**Provenance:** architect inbox `005-D`, 2026-09-05, relayed by the inbox-processing seat,
which is the single writer of `STANDING_RULINGS` §AD and `protocols/OPERATOR-INTERFACE.md`.
Findings arising from this amendment route back to that seat, not into a new register entry
here.

---

## AMENDMENT 2 — one further defect, and a class-label collision (2026-09-05)

> **Same shape as AMENDMENT 1, and for the same reason.** Audits are immutable (critical
> rule 3). The seat's register is untouched, AMENDMENT 1 is untouched, and this marker is
> appended below both. The body's integrity claim is unchanged and still checkable in the
> form AMENDMENT 1 restated: the verbatim body is the contiguous region from
> `# BROWSER SEAT NOTES` to the blank line preceding AMENDMENT 1's `---` rule, still
> `sha256 685633c33c49c7d37de5dba70f3162d4d1841a98b12896ee8d28ee465f06b196`.

| # | Defect | Class | Mechanism that would have caught it |
|---|---|---|---|
| 19 | **role without a carrier** — a role that exists only in a paste can be violated by the same paste | F (see the collision note below) | the role is a routing-table row with a commit-shape hook, carried by the deploy manifest — so an organ can refuse what a paste cannot |

**What happened,** so the one-liner is not cryptic: the browser architect assigned two BUILD
hotfixes to the integrator session, which then produced code for ~1h48m while six branches
waited. The rule *"the integrator merges, never produces"* was real, agreed, and **had no
carrier** — so nothing could refuse it. The integrator was **not disobeying**: it read a
paste telling it to build, and nothing in the repo disagreed. That is the whole finding —
the defect is the absent carrier, not the session's conduct.

**CLASS-LABEL COLLISION — flagged, deliberately NOT resolved by this lane.** The inbox filed
this as *"class F (new class)"*, but **F is already bound** in the landed register: defect 11
is `F doctrine inertia` (*read-only arcs sent LOCAL against standing doctrine*). So either
this is a second instance of F — arguable, since both are "a real rule that nothing enforced"
— or it needs a fresh letter (G). The two readings differ: F-as-inertia is about a rule being
*ignored*, while this is about a rule being *unenforceable*, which is a stronger claim. The
label is left as filed and the ambiguity is recorded rather than silently decided; the register
is the seat's and the classification is the inbox seat's to rule.

**The body's count line is a LANDING-TIME figure.** Section 1 opens *"Sixteen defects, six
classes."* That was true at landing and is not edited here, because it sits inside the
immutable verbatim body. With amendments 1 and 2 the running total is **nineteen defects**,
and the class count depends on the collision above. A reader takes the count from the body
plus its amendments, never from the body's sentence alone — which is exactly why
`CLAUDE.md` §4 says never to restate a count in prose.

**Provenance:** architect inbox `008-D`, amended by `009-A` so the carrier is the **deploy
manifest** rather than hub-only. The inbox seat filed the mechanism as **intake #70** (roles
as routing-table rows with a commit-shape hook); that filing is theirs, not this lane's, and
nothing here triages it. Findings arising from this amendment route back to that seat.

---

## AMENDMENT 3 — the class-G ruling on #19, and five further defects (2026-09-05)

> **Same shape, same reason.** Audits are immutable (critical rule 3): the seat's register,
> AMENDMENT 1 and AMENDMENT 2 are all untouched, and this marker is appended below them. The
> verbatim body is still the contiguous region from `# BROWSER SEAT NOTES` to the blank line
> preceding AMENDMENT 1's `---` rule, still
> `sha256 685633c33c49c7d37de5dba70f3162d4d1841a98b12896ee8d28ee465f06b196`.

### 1. RULING — #19 is class **G**, not a second F

AMENDMENT 2 recorded #19 under the label the filing gave it (`F`) and flagged that F was
already bound to *doctrine inertia* by defect 11, explicitly leaving the collision for the
filing seat to rule. **That ruling has now been made (FILINGS-1, owner of the 008-D
routing):**

> **#19 is class G — "rule without a carrier (UNENFORCEABLE)". F stays "doctrine inertia"
> and is untouched.**

The reasoning, recorded so the label survives someone re-opening it. **F-as-inertia is a
rule that was IGNORED** — the doctrine existed, an organ could in principle have refused,
and a seat went around it. **G is a rule that was UNENFORCEABLE** — no carrier existed, so
*nothing in the repo could disagree with the paste*.

It is load-bearing because **the two have different remedies.** Inertia is fixed by
derivation and visibility — which is exactly defect 11's own corrective, the dispatch verb
derived from the arc class and printed in the contract header. Unenforceability is fixed
only by **building a carrier**, which is why #19's mechanism is intake #70 (roles as
routing-table rows with a `role-commit-shape` hook) rather than a reminder. Collapsing them
would make the register read *"we keep ignoring our rules"* when the finding is *"we ship
rules nothing can enforce"* — and the second recurs at H0 **by construction**, because in a
consumer repo the only rules that travel are the ones with carriers.

**AMENDMENT 2's `F` label is SUPERSEDED, not erased.** It stays visible there on purpose: a
later reader needs the evidence that the collision happened and was adjudicated, which an
in-place edit would have destroyed.

### 2. Five further defects, routed 2026-09-05

| # | Defect | Class | Mechanism that would have caught it |
|---|---|---|---|
| 20 | filings work ran **SERIAL where three file-disjoint lanes were possible** — 36 minutes on two items while nine waited; root cause named as *serial-by-caution* | C concurrency model | inbox `017-A`: a `files:` footprint in item frontmatter, so disjointness is **computed, not judged** — landed in `protocols/OPERATOR-INTERFACE.md` §1 |
| 21 | two pastes carried a **hardcoded drive path** instead of the variable | D interface | candidate (v) reshaped to resolve the prompts dir from **USER scope**, plus the third form-probe predicate |
| 22 | lane names in the brief **violated the lane-name grammar** `lane-<letter>-<id>-<slug>` | A premise-from-summary | *no mechanism named in the filing* — the grammar itself is the constraint that was not resolved at freeze |
| 23 | L2 **duplicated an already-committed branch**; `single_flight` refused it — **the mechanism worked and the brief did not** | A premise-from-summary | the brief resolves the **branch list** before dispatch; this is the coupling-scan class again, one layer out |
| 24 | protocol names **improvised under time pressure**: an unnumbered first inbox, an ad-hoc gate filename, ownership assigned by chat | D interface | the `017-B` naming grammar, replacing improvisation from the next window |

**#23 is the one worth not skimming.** The organ did its job — `single_flight` refused the
duplicate — and the defect is upstream of it, in a brief that never checked the branch list.
An enforcement success and a planning failure in the same event look like a caught error and
are not: the cost was paid before the refusal, and nothing about the refusal makes the brief
better next time.

**Running total: twenty-four defects.** No class count is stated here — with G admitted it is
derivable from the register plus its amendments, and `CLAUDE.md` §4 says not to type one into
prose. Section 1's *"Sixteen defects, six classes"* remains a **landing-time** figure inside
the immutable body, deliberately not edited (see AMENDMENT 2).

**Provenance:** architect inbox, routed by FILINGS-1 as the follow-up to `008-D`. As with the
previous amendments, **none of these are triaged by this lane** and none becomes a backlog
row without ADR-98 intake; the mechanisms named above (`017-A`, `017-B`, candidate (v),
intake #70) are that seat's filings, not this lane's. Findings arising here route back to it.

---

## AMENDMENT 4 — #22's mechanism and class, and the locators AMENDMENT 3 owed (2026-09-05)

> **Same shape as 1-3.** Audits are immutable: the seat's register and AMENDMENTs 1, 2 and 3
> are untouched; this marker is appended below them. The verbatim body is still the
> contiguous region from `# BROWSER SEAT NOTES` to the blank line preceding AMENDMENT 1's
> `---` rule, still
> `sha256 685633c33c49c7d37de5dba70f3162d4d1841a98b12896ee8d28ee465f06b196`.
>
> Three items land together rather than as three markers, per the integrator's cadence
> ruling: an amendment marker is a readability cost paid by the next reader of this file.

### 1. #22's mechanism — supplied, and phrased for what exists TODAY

AMENDMENT 3 recorded #22 as *"no mechanism named in the filing"* rather than inventing one.
The filing seat has now supplied it. It is recorded in two halves, because exactly one of
them is live:

- **The CHECK exists and is reusable today.** `scripts/validate_branch_naming.py` takes
  `--lane NAME` (`ap.add_argument("--lane", metavar="NAME", …)`), and
  `.claude/commands/lane-boot.md` already invokes it as its pre-flight
  (`uv run --locked python scripts/validate_branch_naming.py --lane lane-<letter>-<id>-<slug>`).
  Nothing needs building.
- **The PLACEMENT is what is owed, and it is advisory.** The mechanism is to resolve every
  lane name a brief proposes through that checker **at freeze, before dispatch**, rather
  than at boot — alongside the other freeze predicates in
  `scripts/preflight_contract.py` (`def freeze_predicates(contract, repo_root=…)`). That
  module's own docstring says it is **"wired into no gate"**, so this is *"the freeze
  predicate set (`preflight_contract.py --freeze`, **today advisory**)"* and deliberately
  **not** "the freeze gate".

**Why the wording was ruled rather than assumed.** A mechanism line reading *"the freeze
gate refuses…"* would describe enforcement a reader cannot find — a rule refusable by
nothing, which is **class G by the definition AMENDMENT 3 had just introduced**. Filing a
class-G fix for a defect is the failure mode the class exists to name, so the line says what
is true today and will not need re-amending when that organ is armed. **Arming
`preflight_contract.py` is a separate and larger question and is deliberately not decided
here.**

The placement argument, recorded because it is the reason freeze beats boot: checking at
boot means N lanes each rediscover the same naming defect independently, *after*
provisioning; checking at freeze refuses the brief **once, before anything is provisioned**.

### 2. #22's class — A is exclusive, and here is the test that makes it so

Terra's pre-merge review of AMENDMENT 3 (MEDIUM, upheld) asked the right question: a
violated lane-name grammar looks like it could be **F** (ignored doctrine) or **G**
(unenforceable rule) under the very taxonomy AMENDMENT 3 introduced, so **A** needs
defending rather than assuming. Applying the F/G test in order:

- **Not G.** G requires that *no carrier exists*. One does — `--lane`, already called by
  `/lane-boot`. A rule with a carrier is not class G, and supplying the mechanism in §1
  settles this rather than merely arguing it.
- **Not F.** F is a rule **gone around** when an organ could have refused. At the moment the
  error was made — the brief's freeze — **no organ ran at all**: `--lane` fires at lane
  boot, which is downstream of the mistake. There was nothing to go around.
- **A, and exclusively.** A is a fact asserted without resolving a locator that was one
  command away. The grammar and its checker were both exactly that. The lane names were
  written from pattern rather than derived from the authority that already existed.

**The classification and the mechanism turn out to be one insight, not two.** #22 is class A
*because* the carrier exists but runs after the moment of error; the fix is therefore to move
the existing check earlier, not to build a new one. Had the answer been G, the fix would have
had to be a new carrier — which is precisely the different-remedies argument that made G
worth admitting in AMENDMENT 3.

### 3. Locators for AMENDMENT 3's asserted rulings — a citation debt, not an accuracy one

Terra's second MEDIUM read AMENDMENT 3's ruling and mechanism statements as *"asserted
without support in this diff"*. **Every one of them is TRUE** — checked against the tree, not
relayed — so this is recorded as a **citation-practice** defect and not as a correction:

| Assertion in AMENDMENT 3 | Where it actually lives |
|---|---|
| the class-G ruling and intake #70 | `docs/intake/2026-09-05-tech-session-roles-with-a-carrier.md` (`intake-id: 70`) |
| `017-A` landed in `OPERATOR-INTERFACE.md` §1 | `protocols/OPERATOR-INTERFACE.md`, **"Transport v2 — schema, grammar, retention."**, amending **"FILE EXCHANGE — the transport constant."** |
| candidate (v) reshaped to USER scope | `protocols/STANDING_RULINGS.md`, **"(v) SESSIONSTART RESOLVES THE PROMPTS DIRECTORY FROM USER SCOPE, AND PRINTS IT"** |
| #22's checker and its freeze home | `scripts/validate_branch_naming.py` (`--lane`), `.claude/commands/lane-boot.md` (the pre-flight call), `scripts/preflight_contract.py` (`freeze_predicates`) |

**The generalisable rule, which is the actually useful part:** a reviewer handed only a diff
has no repo, so it **cannot** resolve an unlocated claim and correctly reads every one of
them as unsupported. The reviewer is not wrong to; resolving locators is the author's and
integrator's job, not the reviewer's. So a true statement without a locator costs a review
cycle every time, however true it is.

**Cited by ANCHOR TEXT, not line number, on purpose.** While preparing this amendment the
`/lane-boot` pre-flight call moved from line 25 to line 34 — within hours, on an unrelated
merge. A line number handed over in good faith was already stale by the time it was written
down, which is why the table above names headings and symbols that survive a reflow.

**Provenance:** items 1 and 2 from the architect inbox (FILINGS-1) and terra's pre-merge
review of AMENDMENT 3 (`gpt-5.6-terra`, doc lane, no HIGH); item 3 from that same review's
second finding, downgraded on the evidence. Terra's clean verdict on the immutability shape —
that AMENDMENT 3 **supersedes** AMENDMENT 2's `F` label rather than erasing it — is recorded
here because it is the property these markers exist to preserve. As before, **nothing here is
triaged by this lane** and no backlog row is born from it.

---

## AMENDMENT 5 — WITHDRAWING AMENDMENT 4's "not G" defence (2026-09-05)

> **Same shape as 1-4.** The seat's register and AMENDMENTs 1-4 are untouched; this marker is
> appended below them. The verbatim body is still the contiguous region from
> `# BROWSER SEAT NOTES` to the blank line preceding AMENDMENT 1's `---` rule, still
> `sha256 685633c33c49c7d37de5dba70f3162d4d1841a98b12896ee8d28ee465f06b196`.

### What is withdrawn

**AMENDMENT 4 §2's "Not G" bullet is WITHDRAWN. It was wrong.** It argued that #22 could not
be class G because *"a carrier exists — `--lane`, already called by `/lane-boot`"*. Also
withdrawn: §1's *"Nothing needs building."*

The defence treated **"a checker exists somewhere in the repo"** as equivalent to **"a carrier
exists."** Those are not the same thing, and on the first reading **class G is empty** — every
rule anyone troubled to write a checker for would escape it regardless of whether the checker
is wired to anything. A class that cannot be populated is not a class, and G was admitted
three amendments earlier precisely to name rules that nothing can refuse.

Raised as a HIGH by terra's pre-merge review of AMENDMENT 4 and sharpened by the integrator,
who found that the checker is wired into **no** gate at all — not merely that it fires late.
Verified here rather than relayed.

### The evidence, and it was already written down

The decisive statement is in the repo's own code. `scripts/batch_manifest.py`, in its posture
notes, says:

> *"The grammar is enforced **NOWHERE AT PROVISIONING**. `validate_branch_naming` is read-only
> and **wired into no gate** (its own posture note), and a batch lane dispatched straight
> through `claude --worktree <name>` **never passes `/lane-boot` step 1**. So an off-enum lane
> name is still creatable…"*

Independently confirmed: `validate_branch_naming` is referenced from `batch_manifest.py`,
`gen_lane_contract.py`, `validate_substrate.py`, `worktree_seed.py`, three test modules,
`AGENTS.md` (as a *"Checkable surface"* — a description, not a gate), and
`.claude/commands/lane-boot.md`. It appears in **no** pre-commit hook, **no** session hook and
**no** `audit.py` check. Every consumer **imports its regex**; none of them **refuses** on it.

**The witness that settles it is this lane itself.** These notes were landed by a lane
dispatched as `claude --worktree docs-seat-notes` — exactly the path the posture note names as
bypassing `/lane-boot` step 1. So the sole invocation of the "carrier" was skipped, in the very
session that argued it was one. A carrier you can decline by choosing a different dispatch verb
is not a carrier; it is a convention with a helper script.

### What this does to §1's mechanism

§1's mechanism survives in *direction* and is **weaker than it was written**. Moving the check
to freeze puts an ungated checker inside `preflight_contract.py`, which §1 already recorded as
**"wired into no gate"**. That composes **two** ungated organs and still yields nothing that can
refuse. The honest form: the fix requires **ARMING** something — the relocation alone is
necessary and not sufficient. §1's *"Nothing needs building"* was true of the *regex* and false
of the *enforcement*, and the distinction is the whole point of the class.

### What this lane does NOT do

**It does not reclassify #22.** The enforcement facts point at G under its "unenforceable"
limb, and the integrator's observation is the sharpest reading available — *a grammar with a
checker nobody runs is precisely a rule without a carrier*, which would make **#22 the best
worked example G has**. But classification belongs to the register's owner, not to an executor
and not to a gate, and this lane declining to self-rule the F-collision in AMENDMENT 2 is the
precedent it is following.

**Routing, stated because the adjudicator has changed:** the FILINGS seat that ruled G has
**exited**. This question therefore routes to a fresh FILINGS seat or to the operator via
`to-browser\STATUS.md`, alongside the other owed acts recorded there — not back to a session
that is gone. Two live options are on the table and both are defensible: **(1)** reclassify
#22 as G; **(2)** keep A for the authoring error and file the enforcement gap as a **separate**
G-shaped defect, on the ground that "the author did not resolve a knowable grammar" and
"nothing could have refused the result" are two true statements about one event.

**A note for whoever rules it.** The pending admission bar this exchange produced — *a class
that does not change what the fix has to look like is a label, not a class* — is itself
evidence for option (2): A and G here imply **different fixes** (resolve the locator at freeze
vs. arm an organ), which by that bar makes them genuinely different classes rather than rival
labels for one defect. That is an argument, not a ruling.

---

## AMENDMENT 6 — RULED by the register owner: #22 stays A, the gap files as #25 (2026-09-05)

> **Same shape as 1-5.** The seat's register and AMENDMENTs 1-5 are untouched; this marker is
> appended below them. The verbatim body is still the contiguous region from
> `# BROWSER SEAT NOTES` to the blank line preceding AMENDMENT 1's `---` rule, still
> `sha256 685633c33c49c7d37de5dba70f3162d4d1841a98b12896ee8d28ee465f06b196`.

### 1. AMENDMENT 4 §2 IS SUPERSEDED IN FULL

Not only its "Not G" bullet (already withdrawn in AMENDMENT 5), but **also its "A, and
exclusively" conclusion and its "the classification and the mechanism are one insight"
synthesis.** AMENDMENT 5 withdrew a premise and left the conclusion it supported standing —
in a file where nothing can be edited, that would have been a permanent incoherence, one
marker asserting exclusive-A while the next presented G as open. Recorded because it is a
reusable failure: **a retraction has to reach every claim that rested on the retracted
premise, not just the premise.**

### 2. The ruling

**FILINGS-1, owner of the §AD routing, is live and has ruled** — having verified the
enforcement facts independently rather than taking them:

> **Keep #22 as class A for the authoring failure. File the enforcement gap as a SEPARATE
> defect, class G.**

**Two failures were tangled in one row.** (1) A brief asserted lane names without resolving
them against the grammar — an *authoring* failure, fixed by resolving at freeze. (2) The
grammar has a checker no organ runs at the moment that mattered, so nothing *could* have
refused the brief — fixed only by *arming* an organ. They are not one event described twice:
arming the organ does not stop an author failing to resolve, and a careful author does not
close the gap for the next one. **Different fixes, therefore different classes** — the pending
admission bar doing work rather than decorating a decision already made.

This marker **records** that ruling; it does not make it. This lane's own position throughout
was that classification belongs to the register's owner, and the owner answered.

### 3. G's definition, sharpened — adopted by the ruling seat

> **A carrier is something that can REFUSE, not something that can be run.**

Under the loose reading — *"a checker exists somewhere in the repo"* — **G is empty**: every
rule anyone wrote a checker for escapes it regardless of wiring. This is the first thing to
give G edges, and it came out of the case that looked like a counter-example.

### 4. The new defect

| # | Defect | Class | Mechanism that would have caught it |
|---|---|---|---|
| 25 | **the lane-name grammar was not enforceable at the moment it was violated** — nothing could refuse the invalid names a brief proposed | **G** rule without a carrier (unenforceable) | **arm** the grammar into an organ that refuses at provisioning, rather than relocating an unarmed check |

**Running total: twenty-five defects.** No class count is stated, per `CLAUDE.md` §4.

### 5. #22's mechanism, CORRECTED — ordered, not alternatives

AMENDMENT 4 §1's *"move the existing check earlier, not build a second one"* is **superseded**:
you cannot move a check no organ runs and get enforcement; you get an unarmed check at freeze.
Ruled form:

> **The A-fix — the freeze predicate set resolves every lane name through the grammar — is
> BLOCKED ON the G-fix — arm the grammar checker into an organ that can refuse.**

### 6. SCOPING AMENDMENT 5's enforcement claim — it was over-broad

AMENDMENT 5 said *"Every consumer imports its regex; none of them refuses."* **That is too
strong**, and the correction is finer than the review that prompted it. Measured here:

- **A strict refusal DOES exist, at generator-EMIT time.** `gen_lane_contract.validate_slug`
  defaults to `strict=True` and calls `validate_lane_worktree_name`, raising
  `LaneContractError("lane slug refused by the batch-lane grammar: …")`. A contract *emitted
  by the generator* cannot carry an off-grammar slug.
- **The LIVE pre-commit hook does NOT apply that grammar.** `lane-contract-check`
  (`.pre-commit-config.yaml`, `files: LANE-*.md`) runs `gen_lane_contract.py check`, and the
  parse path calls `validate_slug(slug, strict=**False**)` — deliberately relaxed to
  hyphen-only kebab, with its own comment saying so. It refuses a malformed *shape*, not an
  off-grammar *batch-lane name*.
- **Nothing refuses at PROVISIONING.** `claude --worktree <name>` passes no checker at all.

So the accurate claim is **"nothing refuses at provisioning, and the live hook's check path
relaxes the grammar by design"** — not "none refuses". **The central withdrawal in AMENDMENT 5
survives untouched**: #22's names were in a hand-written brief, not a generator-emitted
contract, so the one strict refusal that exists could never have fired on them.

### 7. Correction to AMENDMENT 5's routing claim

AMENDMENT 5 recorded that the adjudicating seat *"has EXITED"* and routed accordingly. **That
was wrong** — the seat was live, still owned §AD, and ruled. The lane inferred an exit from a
close-out message; **a seat saying it is closing out is not the same fact as a seat being
gone**, and treating the two as one is the same unresolved-premise class this register is full
of. Corrected here rather than edited.

### 8. The symmetry, which is the actual evidence for G

Both seats made **the class-G mistake while working on the class-G classification**: this lane
argued a rule was enforceable by pointing at code that *exists*; the filing seat, in the same
message that correctly required `preflight_contract.py --freeze` be marked *advisory*,
asserted the CHECK half without applying that test to it. Neither is a fact about either seat.
It is evidence that **"code exists" reads as "rule enforced" by default** — the reflex class G
was admitted to name.

**Provenance:** ruled by FILINGS-1 (§AD owner); enforcement facts verified independently by
that seat, by the integrator's gate review (two terra rounds), and by this lane. **Nothing is
triaged by this lane** and no backlog row is born from it.

---

## AMENDMENT 7 — two corrections to AMENDMENT 6 (2026-09-05)

> Same shape as 1-6; the body and every prior marker are untouched. The verbatim body is
> still the contiguous region from `# BROWSER SEAT NOTES` to the blank line preceding
> AMENDMENT 1's `---` rule, still
> `sha256 685633c33c49c7d37de5dba70f3162d4d1841a98b12896ee8d28ee465f06b196`.

**1. Attribution.** AMENDMENT 6 §2's rationale — *"They are not one event described twice"*
and *"Different fixes, therefore different classes"* — is **FILINGS-1's, quoted from the
ruling it issued**, not this lane's reasoning. A6 gave it no speaker, which reads as the lane
re-deriving a disposition the same marker says belongs to the register's owner.

**2. The count is withdrawn.** AMENDMENT 6 §4's *"Running total: twenty-five defects"* is
**withdrawn**. `CLAUDE.md` §4 — never restate a count in prose, cite the surface that computes
it. It is worse on an immutable file: the number cannot be corrected in place, and the next
amendment falsifies it permanently. **The total is the register's own rows plus those added by
its amendments.**

---

## AMENDMENT 8 — §5 is non-dispositive, and the citation is OWED (2026-09-05)

> Same shape as 1-7; the body and every prior marker are untouched. The verbatim body is
> still the contiguous region from `# BROWSER SEAT NOTES` to the blank line preceding
> AMENDMENT 1's `---` rule, still
> `sha256 685633c33c49c7d37de5dba70f3162d4d1841a98b12896ee8d28ee465f06b196`.

**1. AMENDMENT 6 §5 is NON-DISPOSITIVE ANALYSIS.** Its *"Ruled form"* label is **withdrawn**:
the ruling recorded in §2 dispositions the two defects' classes and says nothing about the
order of their fixes, so the *"the A-fix is BLOCKED ON the G-fix"* dependency is this lane's
analysis, not the owner's ruling, and binds nothing.

**2. The provenance claim in AMENDMENT 7 §1 is a debt, DECLARED not discharged.** The ruling
reached this lane as a **cross-session message** and has no durable record anywhere in the
repo — not in `protocols/STANDING_RULINGS.md` §AD, not in any artifact a reader of `main` can
resolve. A7 named the speaker but supplied no locator because none exists to supply.
**The citation is owed once the §AD owner lands the ruling**; until then this file asserts a
provenance the record cannot yet support, and says so rather than implying otherwise. A
binding ruling living only in chat is a governance gap, not a defect of this file, and closing
it is not this lane's to do.

---

## AMENDMENT 9 — OPERATOR RULING: no classification; #22 is carrier-absent (2026-09-05)

> Same shape as 1-8; the body and every prior marker are untouched. The verbatim body is
> still the contiguous region from `# BROWSER SEAT NOTES` to the blank line preceding
> AMENDMENT 1's `---` rule, still
> `sha256 685633c33c49c7d37de5dba70f3162d4d1841a98b12896ee8d28ee465f06b196`.

**Ruled by the architect (operator), 2026-09-05.** This marker records that ruling; it does not
make it, and it endorses neither of the classifications the earlier markers argued.

### 1. AMENDMENTS 4 and 5 are SUPERSEDED IN FULL

Both, entirely — subsuming AMENDMENT 6 §1's partial supersession of A4 §2. Nothing in A4 or A5
is relied on below.

### 2. The finding, stated factually

> **#22 — the lane names violated the lane-name grammar, and the grammar has no carrier.**

- `validate_branch_naming` is **wired into no gate**: it appears in neither
  `.pre-commit-config.yaml`, nor `.claude/settings.json`, nor `scripts/audit.py` (verified by
  grep against those three surfaces).
- **`claude --worktree` bypasses the checker.** `scripts/batch_manifest.py:61-63` records the
  posture in the repo's own words: *"The grammar is enforced NOWHERE AT PROVISIONING.
  `validate_branch_naming` is read-only and wired into no gate (its own posture note), and a
  batch lane dispatched straight through `claude --worktree <name>` never passes `/lane-boot`
  step 1."*

**Scope note, so this marker does not contradict AMENDMENT 6 §6.** The two statements agree once
the entry point is named: nothing refuses **at provisioning**, which is where #22 happened, while
the one strict refusal that exists — `gen_lane_contract.validate_slug(strict=True)`, reached only
on the generator's **emit** path — could never have fired on hand-written brief text. The live
`lane-contract-check` hook's parse path passes `strict=False` by design.

### 3. Disposition

**The class question is WITHDRAWN.** Neither A nor G is endorsed here. The finding is recorded as
**carrier-absent** and is **folded into the roles-without-carrier intake** — architect inbox item
**008-A**, carried by **intake #70**, `docs/intake/2026-09-05-tech-session-roles-with-a-carrier.md`
(note: *008* is an architect-inbox item number, not an intake id; the two sequences differ).

**Nothing is triaged by this lane**, no backlog row is born from this marker, and the status of
defect **#25** — filed under the superseded reading — is **not** decided here.

---

## AMENDMENT 10 — the ruling extended to E-25, A6 §2 and §4 superseded, and the E-NN notation

*Architect ruling, 2026-09-05 evening. Written by the integrator because the authoring lane
had exited; it RECORDS the ruling and argues nothing.*

**Supersession, stated once and precisely — THIS marker is the superseding instrument.**
AMENDMENT 6 **§2 ("The ruling")**, **§4 ("The new defect")** and **§8 ("The symmetry, which is
the actual evidence for G")** are **superseded by AMENDMENT 10**, not by AMENDMENT 9.
AMENDMENT 9 is limited to what it actually did: withdraw the class question for E-22. It could
not reach §4 or §8, because both concern E-25 and the ruling extending the withdrawal to E-25
post-dates it — a marker cannot supersede a disposition it did not yet cover. §2 ruled E-22 as
class A, §4 filed E-25 as class G, and §8 argued the evidence FOR G. All three classificatory
conclusions are withdrawn here.

**§8's observation survives; only its conclusion is withdrawn.** That *"code exists" reads as
"rule enforced" by default* is a factual finding and it stands. It is simply no longer evidence
*for a class*, because there is no longer a class question for it to be evidence for.

**The withdrawal covers BOTH defects.** The class question is withdrawn for **E-22 and E-25**.
Neither A nor G is endorsed for either. AMENDMENT 9's scope was E-22 alone, which left E-25
under A6 §4's classification — live, not yet superseded, until this marker withdraws it; the
ruling is now extended to close that loop.

**E-25's disposition:** it remains a **factual entry with NO class**, status **OPEN**, carried
under the roles-without-carrier intake (`docs/intake/2026-09-05-tech-session-roles-with-a-carrier.md`,
intake #70). No backlog row is born from it, and nothing here triages it — the only route to a
row remains CANDIDATE → intake (ADR-98) → ratification (ADR-111).

**Notation, from this line forward:** the **defect register** is written **`E-NN`** (E-22,
E-25) and **intakes** keep **`#NN`** (#70). The two sequences had collided: "#25" resolved
BOTH to intake #25 (2026-08-05, an unrelated artifact) and to this register's twenty-fifth
defect, so a reader resolving the locator landed on the wrong document and got a false
confirmation. Two separate lanes hit it independently on 2026-09-05. Existing immutable text
is **not** rewritten; the notation binds new register lines only, and this marker is the
statement of it.
