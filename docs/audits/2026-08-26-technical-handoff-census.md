# CLOUD-HANDOFF-CENSUS — what the browser seat is FOR

> Provenance: verbatim session result of the read-only cloud census (Dispatch-Cloud, 2026-08-26,
> `.dev-knowledge` @ 852e145c), relayed to file by the browser architect. Appendix B carries the
> same session's container-uv postscript verbatim.

**Substrate:** cloud, read-only, `.dev-knowledge` @ `852e145c65da04e6ce62429c30cefc316416e1f0` (`main`). No writes made.
**Measured:** 2026-08-26.

---

## 0. Method, sample, and honest limits

**Corpus, measured.**

```
find docs/handoffs -type f | wc -l                     -> 737 files
du -sb docs/handoffs                                   -> 10,580,882 B (10.6 MB)
ls -d docs/handoffs/2026-*/ | wc -l                    -> 115 date-named bundles
ls -d docs/handoffs/archive/*/ | wc -l                 -> 15 (+ 43 files, 649,960 B)
range: 2026-05-09-ai-council-audit-sync .. 2026-08-25-dev-knowledge-architect
```

**Seats, by mode and target repo.**

```
  71 architect · 20 session · 13 session-sync · 3 epic · 2 execution
  1 each: session-close, functional, executor, developer, cleanup
by target: 91 dev-knowledge · 14 ai-council · 5 corp-monorepo · 5 other
```

The brief's "~30+ browser-architect seats" is an undercount against the artifact record: **71 architect-mode bundles exist**, 87 in the v5/v6 era overall.

**Sample.**
- *Mechanical, whole corpus (n=115 bundles / 693 files):* every RESIDUAL.md, HANDOFF_BOOT.md, PROBES.md, SUPPLEMENT.md, PASTE_THIS.md parsed by script — file inventory, byte accounting, FILL-IN region extraction, line-recurrence tables, regex recurrence counts.
- *Prose read in full (n=52 windows, spanning the full date range):* all 46 generator-era purpose regions (2026-07-05 -> 2026-08-25); 3 driftflags regions (2026-08-20, -23, -25); the 2026-08-23 SUPPLEMENT ANSWERS entire; the 2026-08-25 PROBES.md entire plus an exact diff against 2026-08-05 and 2026-08-20; one v3-era bundle README (2026-05-14) and one v4-era 01_ROLE.md (2026-06-05); both live templates; HANDOFF_PROCESS.md (1,131 lines) entire; docs/handoffs/README.md; STANDING_RULINGS.md §V and its section index; the four LESSONS.md asserted-not-measured entries.

**Limits, stated so nothing here is over-read.**
1. **The clone is shallow.** git rev-list --count HEAD -> 320; first commit 2026-08-20; .git/shallow present. **No mechanism can be dated from git in this session.** Every "since when" below is dated from bundle directory names, the spec's own Section history, or ADR headers — in-repo claims, not git evidence. Where I say a date, I name its source.
2. Recurrence counts are regex over bundle text. A regex counts a *mention*, not an instruction obeyed. Each pattern is printed with its count so it can be re-run and disputed.
3. Nothing here measures operator chat turns. "The operator re-explains at nearly every seat" is the brief's premise; what I can measure is its repo-side trace.
4. One correction to a working assumption: docs/handoffs/archive/2026-05-*/ is **not** a duplicate of the top-level bundles. It holds the Council stage1-question.md / stage2-response.md pairs only (diff -rq per pair). No duplication to reclaim there.

---

## 1. What repeats

### 1.1 The single largest repetition is not prose — it is a constant re-transmitted per seat

Composition of all 70 assembled pastes (scripts/assemble_paste.py output, split on `=== <label> ===`):

```
protocols/HANDOFF_BOOT.md   n=70   total 1,036,814 B   avg 14,811 B
RESIDUAL.md                 n=70   total   887,634 B   avg 12,680 B
PROBES.md                   n=70   total   770,771 B   avg 11,011 B
SUPPLEMENT.md               n=62   total   520,862 B   avg  8,401 B
                                   sectioned total 3,246,667 B
```

Two facts about the top two entries:

- **protocols/HANDOFF_BOOT.md is byte-identical every seat by construction** — it is one repo file inlined 70 times. 1.04 MB of the 3.25 MB paste corpus is one file. It is now 17,196 B against assemble_paste.HANDOFF_BOOT_BYTE_BUDGET = 18_000 (95.5% of budget), grown from 5,903 B in the first paste (2026-06-15).
- **PROBES.md is 96% invariant window to window.** diff of 2026-08-05 vs 2026-08-20 -> **4 changed lines of 101**, and all four deltas are the bundle slug substituted into a path (P0c, P3, P8, and the branch note). Nothing about the *questions* changed in fifteen days.

On the latest paste (2026-08-25, 50,794 B): role 16,266 + probes 14,475 = **30,741 B = 60.5% of what the operator pastes is a constant.** Adding the template half of the bundle boot header, **~77% of the payload is not window-specific**; roughly 11.3 KB (22%) is the hand-authored residual and ~1 KB the purpose.

### 1.2 Ranked recurrence in hand-authored text

Corpus: FILL-IN region bodies from RESIDUAL.md/HANDOFF_BOOT.md, plus whole pre-generator residuals, plus SUPPLEMENT.md ANSWERS. **n = 86 bundles, 1,694,583 B.** Count is *distinct bundles containing the pattern*.

```
 67/86  a fact restated where a command exists ("re-derive", "asserted-not-measured")
 60/86  an explicit do-NOT-relitigate list
 50/86  a terra / Codex adversarial-review reference
 45/86  "this is the operator's call / operator-gated"
 42/86  the no_ff_merges standing WARN, narrated by hand
 39/86  the intake / ADR-98 funnel re-explained
 36/86  a ruling debt / unruled queue / "adjudicate first"
 36/86  "the browser has no file access" restated
 32/86  the doc_rot standing WARN, narrated by hand
 29/86  the undeclared_edges standing WARN, narrated by hand
 23/86  "BACKLOG is the spec — do not re-narrate it here"
 19/86  the reconciled_versions standing WARN
 16/86  "do not re-derive what is already ruled"
 16/86  the fleet_parity standing WARN
 15/86  the ADR-110 batch shape (one plan -> N lanes -> one integrator)
 12/86  "the SUPPLEMENT is an INPUT / read it first / it overrides §4"
 12/86  a STANDING_RULINGS pointer
 11/86  "a report travels as a FILE, not chat-paste"
 10/86  operator file-exchange mechanics (Downloads, .md upload, inline paste arrives empty)
  8/86  close capacity / "births are the lever, not throughput"
  8/86  audits produced but not consumed
  8/86  cost / quota / window-exhaustion discipline
  7/86  the journal_spine_anchor WARN
  7/86  a literal dispatch / launch command form
  4/86  "every session ships its exact start command"
```

**The standing-WARN family is the largest single mechanizable class.** Across the 44 bundles that carry a driftflags region (avg **1,847 B each**, 81,279 B total), the named organs recur at: no_ff_merges 25, undeclared_edges 22, doc_rot 21, reconciled_versions 15, fleet_parity 10.

### 1.3 Classification

**(a) NOW MECHANIZED — mechanism and first bundle appearance**

```
answer-free probe manifest        PROBES.md              first bundle 2026-06-11
one-paste assembly                PASTE_THIS.md          first bundle 2026-06-15
architect strategic why           SUPPLEMENT.md          first bundle 2026-06-15
anti-bluff contract header        PROBES.md header       first bundle 2026-07-04
re-render-safe hand regions       FILL-IN markers        first bundle 2026-07-05
ex-ante lane declaration          Destination row + P3   first bundle 2026-07-31
standing-topic reconciliation     P0a/P0b/P0c            first bundle 2026-07-31
one-round-trip evidence block     /handoff-verify        first bundle 2026-07-31
rulings applied without asking    STANDING_RULINGS ptr   first bundle 2026-08-06
the four typed operator forms     "Operator-facing forms" first bundle 2026-08-10
dispositioned known WARNs         ecosystem/disposition-register.yaml (66 entries)
the sole literal-command site     PLAYBOOK Ch8 dispatch table — IN THE TEMPLATE,
                                  IN NO BUNDLE YET (landed after the 2026-08-25 cut)
```

- **The operator-facing forms card (2026-08-10)** carries the four literal commands a seat *types* — dispatch, worktree entry, /lane-integrate, the four-step teardown — resident in the bundle, each pointing at its doctrine home. In 10 bundles. Template's own words: *"a pointer works for prose a seat reads once, and fails for a command a seat types."*
- **The dispatch collapse is the freshest and the largest.** STANDING_RULINGS §V (2026-08-25), on the 2,083-line measurement: the hub carried **four rival literal launch commands** for one act; /lane-boot emitted the form Ch8 itself labels a fallback while silently dropping --model and --effort; *"roughly thirty consecutive browser seats failed to launch a lane. They were not uninformed; they were informed by four sources that disagreed."* The mechanism (Ch8 SOLE site) exists and the template points at it. **It has reached zero bundles.** §V's own closing line: *"the drift organ that would assert every literal command in Ch8 resolves ... is owed and unbuilt; until it exists these rulings bind the seat and not the tree."*

**(b) MECHANIZABLE — ranked by recurrence x operator-pain**

**b1 · Standing-WARN attribution — a generated section, not a hand-authored paragraph.** 47/86 bundles; 1,847 B + one paragraph per bundle. Discriminator already written down (2026-08-25 driftflags): *"attribute a WARN by asking whether the arc's diff touched the file it fires against, not by counting."* Computable: live WARN set ∩ disposition-register (66 entries) ∩ window diff. **Smallest mechanism:** a generated `## Standing vs NEW` block in RESIDUAL.md §1 (gen_handoff.py), three lists — dispositioned-by-register / dispositioned-by-absence-from-the-diff / NEW-and-un-dispositioned — no verdict, count, or sha. Hand region narrows to: which NEW one is a decision rather than a defect.

**b2 · The dispatch line — finish the collapse into the bundle.** 65/116 dirs mention a launch form; 7/86 carry a literal one; cost ~30 failed lanes. Ruling landed; template pointer landed; **bundle has not shipped it once.** **Smallest mechanism:** gen_handoff.py puts the ruled verb into the forms card (form 1) + an agreement check asserting .claude/commands/lane-boot.md and templates/prompt-template.md name the Ch8-ruled verb and nothing else. This is §V's own "owed and unbuilt" organ.

**b3 · Retire protocols/HANDOFF_BOOT.md from the per-seat paste.** 70/70 pastes; 1.04 MB; 32% of every paste; nothing window-specific. **Smallest mechanism:** role becomes the browser Project's standing instruction; assemble_paste.py emits a 3-line stanza (role version + sha + "if your project instructions do not carry v6.2.0, say so before answering"). Saving ~16 KB/seat.

**b4 · PROBES.md is a constant with four slugs in it.** 84 bundles; 96% invariant; 14.5 KB/paste. **Smallest mechanism:** ship the variable rows + a version pin (probe-manifest v6.2.0, 14 rows, sha); invariant text moves to the b3 resident surface. Teeth unaffected — they live in /handoff-verify at check-time. Saving ~12 KB/seat.

**b5 · Operator's interface facts belong in a capability file, not Q6 answers.** 10/62 supplements record them + 4 record "ship the exact start command". The 2026-08-23 supplement states three in one line (Downloads exchange; inline paste arrives empty so uploads are .md; every session ships its exact start command). **Smallest mechanism:** protocols/OPERATOR-INTERFACE.md (or Ch8 subsection), resident in the forms card; supplement Q6 then means only changed intent.

**b6 · The supplement is filled after the paste is assembled, and no organ re-folds it.** 62/70 filled; **61 folded, 1 did not — the most recent:** docs/handoffs/2026-08-23-dev-knowledge-architect/SUPPLEMENT.md carries **87 answer lines** (commit c05aa37); its PASTE_THIS.md carries 4 sections and no `=== SUPPLEMENT.md ===` (assembled at 0216eb3, never regenerated). The outgoing architect's rulings, rejections, off-repo context and Q7 register did not reach the next seat — silent, irreplaceable loss. **Smallest mechanism:** audit check `supplement_folded` — FAIL when ANSWERS non-empty and PASTE_THIS has no SUPPLEMENT section.

**b7 · P10 is an unbounded arc shipped as a probe, in 35 bundles.** P10 asks the seat at boot to classify EVERY open item (176 live rows) as live/dead/awaiting-ruling. HANDOFF_PROCESS §5 condition 4 rejects exactly this and names P10 as its origin. P10 first appears 2026-07-17, still in the 2026-08-25 bundle — survived the v6 cut that ratified the condition rejecting it. **Smallest mechanism:** delete the row from templates/handoff/v5/PROBES.md.tmpl:101 + a verify_handoff_probes rung that FAILs unbounded rows.

**(c) GENUINELY JUDGMENT-PER-WINDOW — belongs in the supplement**
Which new flag is a decision vs a defect · which flag family is not evidence because its checker is structurally blind ([#560]) · the do-not-relitigate set (content differs every time) · tensions weighed + decomposition rationale · off-repo operator intent (60/62) · the sequencing call.

---

## 2. What the browser seat uniquely contributes

### 2.1 What survived downstream — cited instances

```
protocols/STANDING_RULINGS.md   3,034 lines, 120 ruling entries, 23 sections A..W
docs/decisions/ADR-*.md         88 ADRs, 81 Accepted; 29 (33%) dated on an architect-window day
docs/intake/*.md                50 (19 ACCEPTED, 13 READY, 10 SEED, 7 DRAFT)
lane contracts                  55
docs/audits/*.md                738 (350 technical, 155 codex, 25 verification, 23 conformance)
inbound references to bundles   322 files outside docs/handoffs/ cite it
```

Five instances where a browser-seat output demonstrably changed the tree: (1) §V dispatch ruling — consumed by Ch8 + the boot template; addresses ~30 failed lanes. (2) §B5 automation/ prefix — consumed verbatim by CLAUDE.md §4's enum. (3) §I-F3 — consumed by .claude/rules/git-discipline.md. (4) §K-1 — became the validate-hermetization Rule C gate. (5) The 2026-08-26 /codex-review "Do not ratify ADR-115" — re-measured, held; the acceptance was HELD and returned.

**The seat's durable output changed form.** ADRs by month — 04:14, 05:20, 06:28, 07:19, 08:7 — while architect seats rose; output migrated to the rulings register (120 entries in 21 days) and lane contracts (55). Not decline — the same judgment landing on a cheaper surface.

### 2.2 What was re-derivation — and the honest ratio

**Input side:** ~77% of every paste is not window-specific. Of 14 probe rows, **12 are pure state re-derivation**; P0c excises its judgment half; P10 is an unbounded arc.

**Error side — decisive.** LESSONS.md 2026-08-25: *"16 of 16 architect-seat errors in the window were asserted-not-measured — a fact stated from memory where a command existed that would have produced it. Not one was a reasoning error, a bad judgement call, or a disputed ruling."* Errors #17–#19 followed on 2026-08-26. **Nineteen recorded errors; nineteen of one class; zero errors of judgment.** The lesson's conclusion: *"the architect seat's error profile is entirely a FACT-SURFACE problem ... shrinking the number of facts the seat carries by hand moves all of it."*

**Output side:** 62 filled supplements, 557,665 B of authored why; 60/62 off-repo context; 60/62 do-not-relitigate; 30/62 Q7 register; 13/62 durable homes. None derivable from the repo.

**The ratio:** ~3 parts re-derivable-state to 1 part judgment in what the seat is fed; 19/19 failures were fact-handling, 0 judgment; everything with downstream citations is a ruling, contract, or ADR. **The golden mean is not "less browser" — it is "the same browser, holding fewer facts."**

### 2.3 The golden mean, as a role contract
**SHOULD:** adjudicate contested technical questions with durable homes; author lane contracts with ex-ante done-when; review packets against contracts; decide sequencing against close capacity; hold the system view; supply the why the repo cannot derive; emit the exactly-one plan-review output.
**MUST NEVER CARRY:** a count, sha, path, roster, status, line number, verdict, branch name, or date relation not read from a check-time evidence block; nor a procedure a capability file owns. Where a fact is needed, name the command that derives it. (Full contract: Appendix A.)

---

## 3. What the bundle should become

### 3.1 The trend the spec says should not exist
HANDOFF_PROCESS §2 design note (2026-08-25): *"a bundle SHRINKS as the mechanisms grow."* Measured: v3 182.9 KB → v4 31.5 KB (real 5.8x cut) → v5/v6 on-disk-excluding-paste **+27%** over three months, paste **+9%** — while mechanisms grew. The note is correct as doctrine and **falsified as description**; nothing has yet acted on it.

### 3.2 The minimal bundle
Target **≤20 KB pasted** (from 50.8 KB), ≥80% window-specific.
GENERATED: session header ~1.0 KB · Standing-vs-NEW ~1.2 KB · probe pin (version+sha+4 variable rows) ~2.0 KB · role pin ~0.2 KB · forms card (ruled verb) ~1.5 KB.
AUTHORED: §1 headline ~1.5 KB · §2 shipped ~1.5 KB · §4 frontier ~4.0 KB · purpose ~1.0 KB · SUPPLEMENT ANSWERS ~6.0 KB.
RESIDENT, NOT PASTED: the role file (project instruction, sha-pinned) + the invariant 97 probe lines.
Total ~20 KB at ~70% window-specific, vs today's 50.8 KB at ~23%.

### 3.3 Concrete deltas against HANDOFF_PROCESS v6.2.0
```
D1  §5   REMOVE P10 from the shipped manifest (contradicts §5 cond. 4, its own origin;
         35 bundles; site templates/handoff/v5/PROBES.md.tmpl:101) + boundedness rung.
D2  §4   The resident role file leaves the paste; residency + sha pin + on-load refusal
         satisfies the "role MUST reach the browser" clause; byte budget survives.
D3  §13  Generated Standing-vs-NEW block above the driftflags FILL-IN; FILL-IN narrows
         to decision-vs-defect. Anti-bluff contract untouched.
D4  §13  supplement_folded in ALL_CHECKS (FAIL-class); one live instance: 2026-08-23.
D5  §13  Correct the stale "a v5 bundle carries FOUR files" claim (70 carry five);
         P8 asks the seat this exact question, so the drift is load-bearing.
D6  §4   Forms card carries the Ch8-ruled dispatch verb + the agreement gate §V calls
         "owed and unbuilt."
```
**Keep exactly as is:** the answer-free contract and its structural enforcement — the reason the corpus contains no bluffable bundle. Every delta moves *constants* out of the paste and *derivations* out of the seat's head; none moves a value into the bundle.

---

## 4. Proposed rows — CANDIDATE per ADR-111
```
R1 · Retire the resident role file from the per-seat paste — M
     done-when: assemble_paste emits a role PIN; one bundle cut+booted end-to-end with
     project-instruction residency; avg PASTE_THIS < 36 KB on the next cut.
R2 · Generated Standing-vs-NEW drift block — M
     done-when: three lists above the driftflags FILL-IN, no verdict/count/sha; FILL-IN
     prompt narrowed; residual_completeness + verify_handoff_probes green.
R3 · Delete P10 and gate the boundedness condition — S
     done-when: P10 out of the tmpl; verify_handoff_probes FAILs unbounded rows
     (row-scoped, era-judged); RED-first test lands before the removal.
R4 · supplement_folded audit check — S
     done-when: FAIL-class in ALL_CHECKS; RED against 2026-08-23 bundle, green after
     regeneration or a recorded immutable-and-lost disposition.
R5 · Land the ruled dispatch verb in the bundle + gate the four sites — M
     done-when: forms card carries the Ch8-ruled verb in the next cut; agreement gate
     asserts lane-boot + prompt-template name that verb and no rival.
R6 · protocols/OPERATOR-INTERFACE.md — S
     done-when: file exists with the recurring interface facts; forms card points at it;
     SUPPLEMENT Q6 narrowed to changed INTENT only.
```
**Sequencing note:** R3/R4 are S, independent, pay immediately. R5 is highest pain and already ruled — execution, not decision. R1 is the only row changing how the operator sets up a chat — it needs an OPERATOR ruling.

---

## Appendix A — Draft browser role contract (one page)
**Identity.** You are the Layer-1 architect. You have no file access. Claude Code (Layer 3) holds the repo and is your junior. The operator relays, makes the calls you surface, and runs the promotion gate.
**What you decide.** Contested technical questions (revertability, not escalation). Sequencing against measured close capacity. Which fork is genuine. A lane's frozen acceptance criterion, before the lane opens. Whether a returned packet met its contract. Which design tension to surface now.
**What you author.** Lane contracts with ex-ante done-when. Rulings with verbatim term, one-line definition, durable home. The supplement ANSWERS at window close — a step of closing the window, not an errand. An explicit do-not-relitigate set.
**What you must never carry.** A count. A sha. A path. A roster. A status. A line number. A verdict. A branch name. A date relation. All nineteen recorded errors were this class; none was judgment. If a fact is load-bearing, name the command that derives it.
**What you must never re-explain.** A procedure a capability file owns: the dispatch verb, the teardown four-step, the batch shape, the file-exchange mechanics. Explaining one is a defect report about the capability file.
**How you receive state.** One evidence block from /handoff-verify, produced at check-time. Any FAIL blocks onboarding. A missing required row is not a pass. Degraded coverage is reported, never counted as a pass.
**How you emit a plan review.** Exactly one of: the option to select; verbatim paste-ready English; or approve.
**Your one standing refusal.** If your project instructions do not carry this contract at the pinned version+sha, say so before answering anything else.
**Your closing duty.** The window does not close until the supplement carries your answers. An empty supplement is an honest record of a duty undischarged, not an alternative to discharging it.

---
*Every count above is reproducible from the commands shown. Where the shallow clone prevented git-based dating, the date's in-repo source is named. Operator-identifying material — 27 v3/v4-era bundles carry an operator-profile section; the current role file carries none — is reported in aggregate and not quoted.*

## Appendix B — session postscript (container uv incident, same session)
The Stop hook could not run: container uv 0.8.17 vs repo pin ==0.11.19 (pyproject [tool.uv] required-version), so every `uv run --locked` gate refused before the script started — consistent with PLAYBOOK Ch8 Q1's routing ("gate-dependent → NOT cloud"). The session then provisioned the pinned build (pip install --target of uv==0.11.19; binary swap with backup; `uv self update` failed twice — version-not-found then GitHub rate limit — while PyPI carries 0.11.19), after which `uv run --locked python scripts/session_end_backpressure.py` → EXIT=0, provisioning CPython 3.12.10 + 27 locked packages. Pin untouched; read-only mandate held (git status --porcelain → 0 lines; the created .venv/ is gitignored). Finding carried forward: Ch8 Q1 records cloud uv as *unpinned*; measured it is **pinned-but-wrong and provisionable in one step** — a candidate amendment to that routing row, filed by the landing lane, not applied by this read-only session.
