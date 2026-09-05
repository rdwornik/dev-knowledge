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
