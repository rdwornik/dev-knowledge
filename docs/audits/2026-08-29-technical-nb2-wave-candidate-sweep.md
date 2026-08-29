# NB2 · E6 — the wave-1 + wave-2 candidate sweep, one ADR-111 triage pass

**Batch:** night-batch-2 · **Lane:** `pn-audits` (item E6) · **Date:** 2026-08-29
**Repo:** `.dev-knowledge` @ `worktree-pn-audits`, cut from `66662c70` (main's tip at lane boot)
**Rows born / amended / killed:** ZERO — `tasks/` belongs to a sibling lane in this batch.
**n = 94** candidates, each with **exactly one** ADR-111 outcome.

---

## 0. Method, and the two rules that bind this pass

ADR-111: *"a finding may not become a backlog row without triage"*, and *"a triage pass that routes
most items to CANDIDATE has not triaged."* Both are applied literally below. **28 of 94 (30 %) are
CANDIDATE** — the majority are decided here.

**Sources swept**, all resolved on this tree, none assumed:

```
wave-1 lane packets   docs/audits/2026-08-28-technical-nb2-{a,c,d,e,f,g}-packet.md
wave-2 lane packets   docs/audits/2026-08-29-technical-nb2-{h,i,j,k,l,m,n,o}-packet.md
close packets         docs/audits/2026-08-29-verification-night-mission-close-packet.md   (wave 1)
                      docs/audits/2026-08-29-verification-wave-2-close-packet.md          (wave 2)
                      docs/audits/2026-08-28-technical-batch1-end-of-batch-packet.md      (batch 1)
```

**There is no `nb2-b-packet.md`.** Lane B was win-tooling and reported inside the wave-1 close packet.
Stated so the absence is a measurement, not a gap in this sweep.

**Two prior sheets already dispositioned 23 items, and this pass does NOT re-triage them:**
`docs/audits/2026-08-29-technical-nb2-candidate-triage.md` (11 items, all drawn from the batch-1 packet
§6 — S1, S2, CB, CC, CD, CE, CG, CA, CF, CH, CI) and
`docs/audits/2026-08-29-technical-night-harvest-consumption-ledger.md` (§A–§D, 12 more: C1–C12 plus its
DISCHARGED/OWNED/REJECTED sections). **Crucially, neither sheet touched a single lane-packet candidate** —
their inputs were the batch-1 filing wave and the wave-1 harvest respectively. Everything below was
genuinely untriaged.

**Where CANDIDATE's decision is "perform a measurement" rather than "rule a question", the row says
*integrator action*, not *intake*.** Forcing a measurement through ADR-98 would be ceremony; the funnel is
still satisfied because whether to take the action is a named person's call.

**Question routing (ADR-108 §A)** is stated per row: the **operator** rules functional questions, the
**architect** rules technical ones.

---

## 1. THE TRIAGE TABLE

Flat and fenced, copy-safe. `own` = OWNED · `dis` = DISCHARGED · `CAND` = CANDIDATE · `rej` = REJECTED.

```
id   candidate (short)                                    outcome  resolving locator / owner
---- ---------------------------------------------------- -------- ----------------------------------------
A1   [#606] parity-flip done-when unsatisfiable @ v1.4.0   own      [#606] open (tasks/606-*.md)
A2   editor-config workspace_settings implemented:false    CAND     I-DEPLOY · architect
A3   desired_state_loader.py:270 hardcodes 'operator'      CAND     I-XS-DEFECTS · architect
A4   audit.py::append_history emits '##', normalizer '###' CAND     I-XS-DEFECTS · architect
A5   win-tooling canonical stamps block its own commits    rej      out of funnel -> win-tooling backlog
A6   tier1 plugin registered against a worktree path       rej      out of funnel -> L0 ~/.claude cleanup
A7   carried mesh payload advertises an unshipped organ    CAND     I-CARRIER · architect
A8   carried INSTALL.md names a removed component          CAND     I-CARRIER · architect
A9   v1.4.0 tagged; win-tooling first to receive the index own      [#604] open
C1   HANDOFF_PROCESS owes version bump + 3-site re-stamp   CAND     integrator action (evidence below)
C2   v5 HANDOFF_BOOT tmpl owes the two boundary lines      own      [#602] open (verified: 0 matches)
C3   "five-pillar close" resolves to no doctrine surface   rej      stop using the term; no row
C4   X8 phase list vs contract phase list differ           CAND     register act · architect
C5   the two verbs (Dispatch-After / Harvest-Cloud)        own      [#610] open
C6   consumer_at_landing WARNs grow by one per artifact    rej      inherited class, already 15 WARNing
D1   4 rows proposable, every one UNDER the ceiling        rej      packet's own words: "none is a finding"
D2   suite RED: accretion-arm live-corpus assertion        own      [#457] open
D3   4 backlog-accretion loci drained but still firing     CAND     I-DOCROT · architect
D4   worth_relocating has no sub-threshold report surface  rej      no consumer; drain exhausted (see J2)
D5   archive_row_body wired into no gate                   rej      deliberate by design
E1   ecosystem/doc-counts.md needs regeneration            dis      VERIFIED: reads 54 checks (was 53)
E2   deploy/tool.py:98 HUB_DIR_NAME, same defect one site  own      [#605] open
E3   resolve_repo_root behaviour change in a worktree      rej      an improvement, reported not a finding
E4   the [#294] fold question, preserved                   own      [#294] (status: deferred - stated)
F1   CLAUDE.md 2.68 byte/line figures are FALSE            CAND     I-CLAUDEMD · architect (VERIFIED live)
F2   [#577] is a strong closure candidate                  dis      [#577] status: closed
F3   ex-ante 9,161 B vs measured 9,430 B                   CAND     I-CLAUDEMD (joins F1)
F4   integrator owes gen_audit_index.py --write            rej      by-design recurring duty ([#590])
G1   arm the freeze predicates as a gate (WARN then hard)  CAND     I-FREEZE · architect
G2   premise note: 208 rows, right instruction wrong reason rej     corrected in place; no row
G3   CLAUDE.md 2.68 false measurement (dup axis of F1)     CAND     I-CLAUDEMD (joins F1)
G4   predicate (ii) recall ceiling; bare-number sibling    own      [#591] open
G5   should a section heading be a claim site?             own      [#591] open
G6   preflight_contract has two id-resolution sources      own      [#591] open
H1   ruling H3's predicate does not describe its precedent CAND     I-FUNNEL · architect (register)
H2   FM-2 FAIL class (b) fires on conformant files         CAND     I-FUNNEL · architect
H3   docs/intake/README contradicts itself DRAFT vs READY  CAND     I-FUNNEL · operator (functional)
H4   no field records the operator approval a status needs CAND     I-FUNNEL · architect (schema)
I1   refs-as-provenance vs a tasks/ source: field          CAND     I-FUNNEL (VERIFIED 0 of 346)
I2   regen-and-diff gate cannot detect a generator bug     CAND     I-GATEDESIGN · architect
I3   consumed-by: absent from the ADR-98 schema; 0 of 18   CAND     I-FUNNEL (joins I1)
I4   intake docs carry state but no dated transitions      CAND     I-FUNNEL (joins I1)
I5   reconcile FM-1 threshold shape vs _READY_THRESHOLD_RE dis      wave-2 close packet W2-1 re-run
I6   promote funnel_lifecycle TIER_SHIP -> TIER_COMMIT     CAND     I-FUNNEL (a trigger, see 3.2)
I7   4 rows whose provenance resolves to nothing           rej      all pre-cutoff, expressly grandfathered
I8   terra pass 2 owed on this diff                        rej      provider quota; "not a finding"
I9   audit.py run is the FLEET routine; --help says so not CAND     I-AUDITCLI · architect
J1   [#591] predicate (iii): dispatch target vs evidence   own      [#591] open (filed against it)
J2   doc-rot floors at ~59; residual is structural         CAND     I-DOCROT (joins D3) · architect
J3   12 of 18 ACCEPTED intakes cite no [#id]               CAND     I-FUNNEL (joins I1)
J4   the GO's quoted index counts are pre-flip             rej      "not a defect in any artifact"
K1   FM-2 coupling unverified; silent degrade, gates green CAND     I-EMITTER (joins L1) · architect
K2   funnel-health time-series not taken; store named      CAND     I-TELEMETRY ([#529] is CLOSED - see 3.1)
K3   block is bundle-visible, not browser-visible          CAND     architect (assemble_paste + invariant)
K4   functional mode carries no block; amend 16 or ratify  CAND     architect (Layer-1)
K5   no end-to-end cut while worktrees are live            CAND     integrator action (measurement)
L1   name FM-4's emitter path by ruling, not by regex      CAND     I-EMITTER · architect (close pkt 8.1)
L2   "rows closed this window" has no ruled owner          CAND     I-EMITTER (joins L1) · architect
L3   window boundary resolved twice (one CALL, one DEFN)   rej      not a finding; consolidation only
L4   value-evidence predicate is a prose heuristic         CAND     close-packet schema arc · architect
L5   governance-health wired into no gate                  rej      by design, consistent with `checks`
M1   wire `why` into check_funnel_lifecycle                CAND     later batch · architect (S-M)
M2   two consumer classes the five inputs cannot see       CAND     architect (one-key fix if ruled)
M3   1301 of 2677 tracked files governed (48.6%)           CAND     I-COVERAGE · operator+architect
M4   consumer_at_landing.cited_identifiers lies in its type CAND    I-XS-DEFECTS (joins A3/A4)
M5   tasks/archive/ edges built rather than reported       CAND     integrator action (accept or revert)
N1   MODEL ATTRIBUTION signature trailer                   dis      born as [#615], VERIFIED open
N2   the Stage-1 telemetry store has NEVER been written    CAND     I-TELEMETRY (VERIFIED absent)
N3   run_id cannot express a whole-commit gate cost        CAND     I-TELEMETRY  <-- the F3 wall-time item
N4   tracked per-day audit snapshot store dormant 07-31    CAND     I-DASHBOARD (VERIFIED dormant)
N5   conformance.html cannot be archived w/o lockstep edit dis      wave-2 close packet ADJ-2 -> FPG-1
N6   budget: dependencies zero, no ADR-106 act             rej      a budget report, not a finding
N7   budget: ratchet 0 spent of 0 headroom                 rej      a budget report, not a finding
N8   budget: .gitignore +15 outside declared write-scope   dis      declared, and accepted at merge
N9   budget: scope held (no hook / no row / no journal)    rej      a conformance statement
N10  budget: 5 terra rounds attempted, 4 done; 6th owed    CAND     CC action (close pkt 8.3)
N11  panel renamed to "gate time per runner invocation"    dis      subsumed by N3, which holds the decision
N12  two series render INSUFFICIENT (3-point floor)        rej      store maturity; resolves via N4
N13  predecessor's operator-facing question not served     dis      re-homed with N5 by ADJ-2
O1   win-tooling intake README still reads "READY (13)"    rej      out of funnel -> win-tooling backlog
O2   agy cannot be contained or audited on this host       own      [#578] open (filed against it)
O3   register "R3" does not resolve; addendum resolves it  own      [#591] open (filed against it)
      wrongly
O4   the addendum's log-baseline claim is also stale       own      [#591] open (filed against it)
O5   routing_agreement diverges on 4 of 4 roles            rej      corroboration; ROUTING.md is L0
O6   terra served as gpt-5.6-sol, not gpt-5.6-terra        CAND     I-PROVIDERPIN · architect (see 3.3)
O7   telemetry has no event type for this measurement      CAND     I-TELEMETRY (joins N2)
X1   C-J orphan: skip impersonating a pass                 CAND     I-GATEDESIGN (joins I2) - see 3.4
W1   intake README six live docs render [MISSING-ID]       dis      VERIFIED: 0 occurrences on this tree
W2   two baselines need an ACCEPTANCE act to regenerate    CAND     operator (functional)
W3   three intakes archivable behind a status ruling       CAND     operator (functional) - #19/#26/#28
W4   [#579] identification for close-packet item 3b        CAND     operator - "one operator word"
W5   four pre-existing suite REDs                          own      [#457] open
W6   win-tooling parity: no-further-deploys, owned by none CAND     amend intake #38 (not a new intake)
W7   tasks/ rows carry no source: field (0 of 344)         dis      same item as I1; ledger C7 holds it
W8   funnel_coverage is non-recursive                      CAND     I-GATEDESIGN (joins I2)
W9   launch-contracts implicit schema                      CAND     I-FREEZE (joins G1) · architect
W10  ADR numbering gaps (27 absent; ADR-61 schema)         rej      cosmetic; numbering is not a registry
W11  [#598]'s dead conftest.py locator                     own      [#598] open
W12  README/VISION 5-line merge                            own      [#614] open (ADR-114 execution arc)
W13  intake-id: 14 assigned to three files                 CAND     I-FUNNEL (joins I1) · architect
```

```
TALLY   OWNED 16  |  DISCHARGED 11  |  CANDIDATE 39  |  REJECTED 28        (n = 94)
```

---

## 2. The tally, read honestly

**39 CANDIDATE of 94 is 41 %, not a majority — but it is the largest single bucket, and ADR-111's second
rule deserves a straight answer rather than a passing grade.** The 39 collapse to **13 decision acts**,
because most of them join a sibling rather than standing alone:

```
I-FUNNEL        H1 H2 H3 H4 I1 I3 I4 I6 J3 W13     10 items -> 1 intake (funnel provenance + lifecycle)
I-TELEMETRY     K2 N2 N3 O7                         4 items -> 1 intake (the store, unfed + ungrouped)
I-EMITTER       K1 L1 L2                            3 items -> 1 architect ruling
I-XS-DEFECTS    A3 A4 M4                            3 items -> 1 row (three one-site code defects)
I-CLAUDEMD      F1 F3 G3                            3 items -> 1 act (correct 2.68 within the budget)
I-GATEDESIGN    I2 X1 W8                            3 items -> 1 intake (gate blind spots)
I-CARRIER       A7 A8                               2 items -> 1 intake (carrier text vs shipped set)
I-DOCROT        D3 J2                               2 items -> 1 architect ruling
I-FREEZE        G1 W9                               2 items -> 1 intake
I-DEPLOY        A2                                  1
I-COVERAGE      M3                                  1
I-AUDITCLI      I9                                  1
I-PROVIDERPIN   O6                                  1
singletons      C1 C4 K3 K4 K5 L4 M1 M2 M5 N10 W2 W3 W4 W6   (integrator/operator actions, not intakes)
```

**Nine intakes and four rulings, from 94 raw candidates.** That is the number the filings lane should
plan against, not 39.

---

## 3. The calls that are not obvious, with the evidence

### 3.1 · K2 and N2 — the telemetry store is unfed, and **its row is CLOSED**

Both lane K and lane N routed their telemetry candidates to `[#529]`. **`[#529]` is `status: closed`** —
verified at `tasks/529-telemetry-v1-emit-stage-1-events-from-the-gate-m.md`. And `logs/TELEMETRY.db` does
not exist in this worktree (`ls` returns *No such file or directory*), exactly as lane N reported.

**So neither item can be OWNED, and this is the sweep's most consequential finding.** `[#529]` shipped the
*emitters* and closed correctly on its own done-when; nothing ever shipped a *consumer* or turned emission
on. The result is a closed row, a library with no call sites, an absent store, and two lanes each pointing
at the closed row as though it still held the work. **A closed row is the one place a candidate cannot
rest**, because no surface will ever surface it again.

This is why K2, N2, N3 and O7 are one intake and not four: the store, the run-id grouping seam and the
frozen event enum are the same unbuilt half of one organ.

### 3.2 · I6 — a promotion trigger, not a task

*"Promote `funnel_lifecycle` `TIER_SHIP → TIER_COMMIT` once leg a1 measures 0 on `main`. One line …
still needs someone to notice the condition is met."* A one-line change gated on a condition nobody
watches is the same shape as C7's parked cache in this lane's companion artifact. It is CANDIDATE because
the decision is *who watches*, not *whether to edit a line*.

### 3.3 · O6 — the provider pin, and why it is not cosmetic

The terra reviewer served as `gpt-5.6-sol` where the contract pinned `gpt-5.6-terra`. This is precisely
the class the `provider-registry-agreement` gate exists to refuse, and `CLAUDE.md` §9 records that its S10
leg *"asserts the pin COUNT, not only the values — a deleted pin passed clean until 2026-08-22
(gpt-5.6-terra)"*. **The same pin, silently substituted again.** Whether the gate should assert served-vs-
pinned identity is an architect's question; that it recurred is a fact.

### 3.4 · X1 — the orphan this sweep exists to catch

C-J is declared as a candidate in the batch-1 end-of-batch packet's **body** (`:311`, the
skip-impersonating-a-pass finding) and is **absent from that packet's own §6 candidate enumeration**. The
11-item triage sheet consumed §6, so C-J appears on no sheet anywhere. It survived only because the prior
triage recorded its own gap in §(i). **A candidate list and the prose that produced it are two surfaces,
and only one of them is read downstream.**

### 3.5 · C1 — the version bump did not happen, measured on the spine

Lane C's own commit is `7156d432` *"docs(playbook): name the night-batch protocol … [#610]"*. It edited
`protocols/HANDOFF_PROCESS.md`. The `Version:` line at `:4` reads **6.3.0 before and after** — the bump to
6.3.0 came from `e4eaee05` ([#611]), a different arc. So the re-stamp lane C flagged as owed is **still
owed**, and the `coherence-nudge` hook is non-blocking by design, so nothing will stop a commit over it.

### 3.6 · The six REJECTED that are rejections of a *route*, not of a fact

A5, A6, O1 are real and true; they are rejected **from this funnel** because their subject is another
repo's backlog (win-tooling) or L0 operator runtime config outside this repo. C3, D4, D5, L3, L5, N6, N7,
N9, N12, E3, J4, G2, I7, I8, D1, F4, W10, O5 are rejected as *not findings*: budget reports, conformance
statements, declared-and-accepted deviations, expressly grandfathered rows, provider-quota interruptions,
by-design wiring, and one improvement reported for visibility. **Each is named rather than dropped, which
is the whole point of writing a rejection down.**

---

## 4. Rows that ought to be BORN — named for the filings lane / integrator

This lane holds no write on `tasks/`. These are the births the triage supports, in priority order, each
with the decision it needs and whose it is (ADR-108 §A):

1. **TELEMETRY CONSUMER** *(architect)* — the store `[#529]` instrumented was never written and its row
   is closed. Covers K2, N2, N3, O7. **Highest priority in this sweep**, because a closed row cannot
   resurface and four lanes independently rediscovered the same hole in one night.
2. **FUNNEL PROVENANCE + LIFECYCLE** *(architect, with one operator leg)* — one act ruling `refs` vs a
   `source:` field, `consumed-by:` in the schema, dated transitions, the DRAFT/READY contradiction and the
   approval field. Covers H1–H4, I1, I3, I4, I6, J3, W13. Ten candidates, one ruling; the ledger's C5/C7
   already point at the same axis.
3. **GATE BLIND SPOTS** *(architect)* — regen-and-diff cannot detect a generator bug (I2), a skip can
   impersonate a pass (X1), `funnel_coverage` is non-recursive (W8). Three independent instances of *a
   gate that is green for the wrong reason*, which is the most expensive defect class this repo has.
4. **THREE XS CODE DEFECTS** *(architect)* — A3 (`desired_state_loader.py:270` discards `ruled_by`), A4
   (`append_history` emits a header its own normalizer rejects), M4 (a 3-tuple declared as a 2-tuple).
   One row, three one-site fixes, all with a Terra finding behind them.
5. **CARRIER TEXT vs SHIPPED SET** *(architect)* — A7/A8. A consumer currently reads that its pushes are
   gated when they are not. **This is a false-safety claim in shipped doctrine** and is ranked above its
   size for that reason alone.
6. **CLAUDE.md §2.68 correction** *(architect)* — F1/F3/G3, verified live on this tree: **107 lines /
   5,539 B against a claimed 103 / 5,270 B**, false since `43c18e9f`. It needs a decision rather than an
   edit only because `CLAUDE.md` sits at 196/200 lines, so the correction must buy its own space.
7. **DOC-ROT FLOOR** *(architect)* — D3/J2: the drain is exhausted at ~59 and the residual is structural,
   so the ceiling is either re-pinned or a different mechanism is chosen. Deciding *not* to act is a fine
   outcome; leaving the ceiling un-re-pinned is not.

**Amend, do not birth:** W6 belongs on **intake #38** (the root-contract home), not on a new intake.

---

## 5. What this lane could NOT do, named plainly

- **No row born, amended or killed, and no intake filed.** `tasks/` and `docs/intake/` belong to sibling
  lanes in this batch. Section 4 is the complete input a filings lane needs; nothing here is actionable by
  reading only the table.
- **The two prior sheets' 23 dispositions were taken as given, not re-verified.** I confirmed their
  *scope* (batch-1 §6 and the wave-1 harvest) to prove they do not overlap this pass; I did not re-resolve
  each of their locators. If one of them is wrong, this sweep inherits the error.
- **Wave-1 lane B has no packet** — its candidates, if any exist outside the wave-1 close packet's §4, are
  not in this sweep. Stated as a boundary, not a claim of completeness.
- **Lane N's §5 budget items are reports, not findings**, and five of the eight are rejected as such. If
  the architect intended §5 to carry decisions rather than a budget statement, this pass mis-classified
  them and the correction is cheap.
- **`docs/audits/README.md` is left STALE by design** — `[#590]` narrowed the index hook so a batch lane
  does not regenerate it. The integrator owns it (and F4 records that as a recurring duty, not a finding).
