# Residual — 2026-07-21-ai-council-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> ## ⚠ CROSS-REPO BUNDLE (ADR-36/41)
>
> **The subject of this handoff is `ai-council`. The bundle lives in the `.dev-knowledge` hub.**
> Every `#id`, file path, ADR number, and `BACKLOG.md` reference below is **ai-council's** unless
> explicitly marked hub. The two repos have same-named files with different contents — `BACKLOG.md`,
> `ARCHITECTURE.md`, `VISION.md`, `LESSONS.md`, `JOURNAL.md`, and even `scripts/validate_backlog.py`
> exist in both. Reading the wrong one is the primary failure mode of a cross-repo bundle; `PROBES.md`
> names a **run-in root** per probe for exactly this reason.
>
> **The hub is read-only w.r.t. the target** — this session plans `ai-council` work; it does not edit
> the hub's governance corpus. The stock generator probes were hub-bound and have been **re-authored
> against verified-live ai-council surfaces** (see the `PROBES.md` cross-repo header for which and why).
> Note the ADR numbers in this residual are **hub** ADRs when cited as governance (ADR-36/41/65/66/70),
> and **ai-council** ADRs when cited as product decisions (ADR-01/03/05/11/12/43/95) — the residual
> marks which each time.

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks. **Re-derive each at read-time — the teeth are in
`PROBES.md` (P2/P4/P7/P9/P11), not in trusting these lines.** This bundle states **no** verdict,
WARN count, `[stale]` status, drifted `#id`, sha, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**Cross-repo note first (structural, and it IS part of the headline).** `ai-council` has **no
counterpart to the hub's drift-flag machinery** — no `audit.py ship-gate`, no
`ecosystem/disposition-register.yaml`, no `validate_doc_claims`, no `validate_git_backlog`. There is
therefore **no dispositioned-WARN set to inherit and no standing-vs-new distinction** in the hub's
sense. The target's drift surface is four independent read-only validators plus judgment over
`BACKLOG.md` ∩ git — which is why `PROBES.md` P2/P4/P6/P7 were re-bound rather than run as generated.
**Treat the absence of a consolidated verdict as the flag**, not as a green light: several of those
gates pass *silently*, so "no output" is not "no drift" (P7 reads exit codes explicitly for this reason).

**THE HEADLINE — the record and the ticket-space are deliberately out of sync, and that is a
*decision state*, not an accident.** A **filing moratorium** held across this entire window: four
night audits ran, a combined review synthesized them, and two fix lanes landed real code — and
**nothing was filed and nothing was struck** except the two verified-done items. The consequence is a
drift class the hub's machinery has no equivalent for:

- **Fixed-but-never-ticketed.** The six defects repaired this window (the night code audit's own
  `P1-*` finding ids, not `#id`s) were confirmed by that audit as **not already tracked**, so no
  `[#id]` applied and none was created. They are now fixed on `main` and recorded **only** in
  `JOURNAL.md` + git — neither "open" nor "closed" anywhere in `BACKLOG.md`. A backlog-∩-git drift
  check would see nothing, because the tickets never existed.
- **Found-but-never-filed.** The remainder of that audit's new `P1` set is still **unfiled** — it
  lives only in `docs/audits/2026-07-20-night-code-audit-opus.md`. The combined review names this the
  strongest argument for lifting the moratorium, because night 2 re-reports the same set until the
  backlog absorbs it.
- **Therefore:** `BACKLOG.md` is currently an **under-count** of known defects by construction, and it
  is the only surface the ADR-66 gate validates. P9/P10 re-derive the live counts; the *judgment* that
  the number is deliberately incomplete is what does not survive a compaction summary.

**Doc-vs-config drift (P2 is the tooth).** `ARCHITECTURE.md` carries a **Pre-commit roster** in prose;
the repo-root pre-commit config carries the live hook set. `ai-council` has **no automated doc-claim
check**, so if these two have diverged, nothing in the repo reports it. **P2 re-derives whether they
match** — do not assume either direction from this line.

**Point-in-time claims inside `JOURNAL.md` that are already stale-by-design.** The newest JOURNAL entry
closes with a **"Push state (corrected)"** paragraph and a **tag-durability** claim about
`spike/md-parser-evidence` (the rescue of four commits that were reachable from no ref). Both were
written mid-session and both are **re-derivable facts about the remote**, not durable record. **P3 and
P11 re-derive them.** Read the JOURNAL's closing paragraph as *a claim made at a moment*, never as
current state — this is the same recency-peak trap §8 asks the browser to scan for.

**Standing, by reference — carried deliberately, not oversights:**

- **[#77]** `options_considered` corrupted on `main` — the delegation-surface defect, filed as **one
  contract-scoped ticket** precisely to stop a third round of partial patches. Still unruled on its
  *boundary* question (§4).
- **[#76]** verdict-package `artifacts[]` can name a copy the write never produced;
  `scripts/verify_output_writes.py` reports it as a standing **GAP** — visibility is the interim
  mitigation, **not a fix**.
- **[#75]** `secondary_dir` raises where ADR-43 `target_paths` swallows — the canonical-loss class.
- **[#66]** gated on **[#27]**; **[#27]** itself is operator-blocked, not stalled work (§4 item 8).
- **[#82]'s own premise is verifiably FALSE** (backlog audit A5, against source) — and the vision
  audit's H6 **propagated that false premise** before it was disproved. Correcting **[#82]**'s body
  repairs both. This is the one place in the corpus where **one night report corrected another the
  same night**; the correction is recorded but the ticket body is not yet fixed (moratorium).
- **Record-drift residue, unfixed under the moratorium:** the **[#110]/[#128] → [#84]/[#85]** renumber,
  a **dangling `#96` reference**, and **[#4]**'s fired condition (its "closed as not-needed if Gemini
  retained" escape hatch is void because Gemini was **not** retained, so it is now an unblocked
  required ADR-02 amendment — and ADR-02's own *"No open remainder"* stamp is stale the same way
  ADR-01's was before this window refreshed it).
- **Severity dispute, unadjudicated:** the combined review's **X2** — `BACKLOG.md` files **[#69]** as
  P2 while the code audit argues P1. Unaddressed in the ticket's own text.

**Do not trust any of the above as current state** — P2/P3/P4/P7/P9/P10/P11 re-derive it live.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Terse map only — `JOURNAL.md` (four entries dated **2026-07-21**) already encodes the detail; do not
re-read it as narrative here. **The window's defining property: heavy audit + real code, zero filing.**

- **Night-audit batch reintegrated** — four read-only reports off three worktrees (vision + input-layer
  on one branch; code; backlog-trust), then a **combined review** synthesizing all four. → JOURNAL
  2026-07-21 "night-audit reintegration"; `docs/audits/2026-07-21-night-audit-combined-review.md`.
  Three prompt-vs-reality mismatches were **recorded rather than silently repaired** (branch naming;
  only three worktrees existed, not four; all three worktree locks named **dead PIDs** — checked with
  `Get-Process` *before* touching anything, then `unlock` + plain `remove`, never `-f`).
- **LANE A — provider-layer fixes** (audit ids P1-1 / P1-3 / P1-7), merged. Typed error dispatch by SDK
  class **name** (so one table covers both hierarchies without importing either SDK into `base.py`);
  `_parse()` brought inside `generate()`'s guard; per-event-loop lazy client caching compared by object
  identity. `gemini.py` **untouched — it was already correct and stays the reference implementation.**
- **LANE B — orchestration-resilience fixes** (audit ids P1-2 / P1-8 / P1-9), merged. `return_exceptions`
  + isinstance triage; seat status derived from the **last completed round** (new `lost` status); a
  synthesis failure now **preserves the paid-for transcript + metrics** instead of discarding the run.
  Held **strictly inside contract-1.0** — discharged by grep before coding, pinned by a key-set equality
  test. **Four terra passes, three productive** — every finding reproduced with a failing test first.
- **Closure hygiene** — **[#2]** and **[#3]** struck (the only two done-but-listed of the open set; both
  done-whens **re-verified first-hand against source**, not accepted from the audit). **[S1]** fully
  delivered → collapsed per ADR-65 (hub). ADR-01's Deployment-Status stamp refreshed. → JOURNAL
  2026-07-21 "closure hygiene".
- **Orphan-evidence rescue** — `git tag spike/md-parser-evidence` anchored a **4-commit arc reachable
  from no ref at all** (`git fsck --unreachable`); a `gc --prune=now` would have destroyed it
  irreversibly. It is the evidence base **[#80]/[#81]**'s ruling depends on, and its tagged tip is the
  commit where the spike **retracted its own conclusion**. **P11 re-derives whether that rescue is now
  durable off-machine** — the JOURNAL's claim about it is point-in-time (§1).
- **Nothing filed, nothing struck beyond the two above** — the moratorium held in every one of the four
  sessions, each recording it explicitly. This is the state §4 item 1 asks you to rule on.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**This is a DECISION session, not a build session.** The window just past produced four audits, a
combined review, and six real fixes — and its own closing note says the same thing four times: the
work is now **queued behind unmade decisions**, not behind unwritten code. Ordered below by how much
each constrains the others.

> **Carried forward from the PREVIOUS architect supplement (2026-07-20) — do NOT relitigate.**
> These were settled by the outgoing architect one window ago and nothing since has disturbed them:
> **(i)** do **not** couple a *compliance* fix to a Contract-Version bump — a compliance fix forces no
> bump (precedent **[#39]**); **[#34]** + **[#76]** remain the 1.1 pair. **(ii)** The lane-split
> standing rule: *before splitting lanes, list each lane's changed **public signatures** and grep the
> others* — file-disjointness is **not** contract-disjointness (this cost a RED `main` once already).
> **(iii)** Do not redo: the A2→A1→C merge order, the two-contract split, the **[#68]** registry-check
> design, the F8 marker-drop, or the 1.0-stamp-holds ruling.

**(1) THE MORATORIUM — lift, hold, or scope it. This is the gating meta-decision.**
A filing moratorium has held for the whole window (§2). The combined review is explicit that it blocks
**two of its own top-five actions** — absorbing the new `P1` set into tickets, and closing the verified
record drift — while the other three are **not** blocked. It is also explicit that the moratorium, *not
audit design*, is what binds the **cadence** question (item 7): a finding-audit only becomes
re-runnable-with-value once the backlog has absorbed its previous output, so a held moratorium
guarantees the next code sweep re-reports the same findings. **The open question is not "is filing
good"** — it is *what the moratorium was protecting*, and whether a **scoped lift** (absorb-and-renumber
only, no new feature filing) buys the cadence back without reopening whatever the freeze was for. **CC
cannot see the reason for the moratorium — it is off-repo. Ask the operator first (§13d beat).**

**(2) Rule [#81] — the preferred-failure question. Highest-leverage unmade decision; NOT
moratorium-blocked.**
Both Opus reports independently name it the top outstanding *decision*, and two sessions have now spent
effort downstream of it. The fork: a fenced code block inside an options section is read as list items,
so a fenced diff **fabricates** authoritative options; but making extraction fence-aware **inverts the
failure mode** — if a model ever fences its real options list, fabrication becomes *total option loss*.
**Neither failure is free; the ruling is which one you prefer.** The relevant prior is the **F8
precedent**, where the operator chose *under-match toward the loud failure* — `[]` is honestly empty,
`['Risk one']` is plausibly wrong and consumed silently. That principle, if reaffirmed, decides this.
**It is also upstream of [#77]'s real architectural question** (below), and of **[#80]** (multi-line
option truncation, the same design-fork class). **The evidence base is the rescued spike tag** — whose
tip is the commit where the spike *reversed its own conclusion*, which is precisely the substance the
ruling turns on. Confirm the evidence is durable (**P11**) before ruling on it.

**(2b) [#77] — the boundary question underneath the ticket.**
Filed as **one** contract-scoped ticket to force an *ex-ante* contract with tests written before the
fix. But the open **architectural** question is not the regexes: **should option extraction remain
heuristic parsing of synthesizer prose at the output layer at all, or should the synthesizer be asked
to emit structured options directly, so there is nothing to parse?** Every patch so far has assumed the
former without ever deciding it. Rule the boundary, then the contract writes itself.

**(3) Rule H1 — the vision fork. NOT moratorium-blocked, and it gates item 4.**
`VISION.md` frames a *"multi-model AI debate and research tool for architectural decision-making"*;
the vision audit's H1 finds a **creativity/boosting engine** in the mission framing that the record does
not carry (the `ideas` mode is the least-developed path — one round, no divergence step, and the quality
rubric scores *fidelity*, not *novelty*). **Three of the four night reports touch this fork; none can
resolve it** — the combined review says so explicitly and assigns it to the operator. The vision audit
offers the same fork one level up as **Position 1** (keep the direction, buy the evidence) vs
**Position 2** (reframe from *debate engine* to **adjudication engine** — concentrate on heterogeneous
*verification* rather than heterogeneous *generation*). **Note the honest caveat the report makes about
itself:** its §1 for/against survey is **low-value and will regenerate verbatim** until its own
adjudicator (**[#55]** baseline experiment) actually runs — so H1 is a decision to be *made*, not a
decision to be *researched further* by re-running the same audit.

**(4) The input-layer architecture fork — do not start it before H1.**
The input audit is an **ADR seed, not a decision**: every contested point deliberately holds ≥2 live
options. Three boosting architectures are "held in tension" and the report is explicit that the
**first build choice is the load-bearing one, because each anchors a different owner** — **A** single-shot
reformulator (anchors caller-side), **B** bounded clarify-loop (anchors an interaction channel), **C**
classify-then-decompose (anchors a council-side entry stage). The routing fork (R1/R2/R3) is
**explicitly H1-sensitive** — the mechanism is shared either way, *only the default flips*. Two further
sub-forks stay open: gate posture (hard / advisory / hybrid) and the approval mechanic (two-phase
commit vs inline-with-consent). **ADR-11 reopening:** the report's verdict is that **A and C do not
reopen it** (both fit CLI-as-ABI); **only B done properly does**, because it needs MCP elicitation.
**One genuinely new ground-truth fact worth carrying:** `detect_mode()` **structurally cannot emit
`research`** — that mode is unreachable by auto-detection and must be forced via flag or frontmatter.
This is not in `BACKLOG.md`.

**(4b) The cross-repo governance tension inside item 4 — the architect's own call.**
The input audit names it directly: **hub ADR-95's lane discipline is in direct tension with boosting
itself**, because a boost that improves a weak question is *shaping substance*, which ADR-95 reserves
for the architect. The report offers a candidate line — **the boost may restructure, interrogate, and
flag; it may never assert a fact the caller didn't give.** That candidate is the thing to accept,
amend, or reject. It is a **hub-governance** question surfacing inside an ai-council build decision,
so it is genuinely yours and not delegable downward.

**(5) H7 — the crux artifact is excluded from the verdict package. Flagged as the strongest single new
finding in the night set.**
The tests pin that the crux artifact *"must stay OUT of the verdict package."* Consequence: **a Lane-A
caller cannot tell a grounded verdict from an ungrounded one without parsing the transcript — which is
exactly what the verdict package exists to spare it from.** Two live options: carry it as a **rider on
the [#34] + [#76] Contract-1.1 batch**, or **defend the exclusion explicitly in an ADR**. Either is
defensible; leaving it undecided while [S13]'s caller-side advisor gets built is not, because the
advisor is the consumer that would hit it.

**(6) Contract-Version 1.1 — decide the bundle and cut it. [#34] + [#76].**
Both change the delegation surface, so they version **together**, not piecemeal. **[#34]** =
research-path verdict-package parity (a Lane A *research* commission currently gets no transcript-free
deliverable at all — debate-path-only was an explicit architect ruling, not an oversight).
**[#76]** = two-pass write, so the manifest is serialized only after the writes it describes land.
**Open:** does **H7** (item 5) ride in this same bump? Per the carried-forward ruling above, **[#77]
does not** — it is a compliance fix.

**(7) Audit cadence — the practice is worth keeping; the *clock* is what is wrong.**
The combined review's answer to "which of these should run nightly" is *"none of them, as run"* — three
are **triggered** audits and one is triggered-at-full-scale. Named triggers: the vision axis fires when
H1 is ruled, when the **[#55]** baseline lands, or when an ADR changes direction; the input-layer axis
**should not re-run at all until a ruling lands**; the backlog axis fires at **merge-arc** cadence; the
code axis fires at full-sweep scale, and its *nightly-shaped* equivalent **already exists** as
diff-scoped `/codex-review`. **Decide the trigger set, and note the dependency: this is downstream of
item 1** (a held moratorium makes every re-run report the same findings).

**(8) [#27] Phase-3 blind scoring — CARRIED FORWARD UNMOVED, and the previous architect ranked it
FIRST.**
The 2026-07-20 supplement named it *"THE highest-leverage item, the one objective function of five that
missed"* — non-delegable, one operator sitting, and it gates the ADR-12 §5 flip → **[#41]** → **[#66]**.
**This window did not touch it.** It is surfaced here explicitly because the defect-driven ordering
above **structurally cannot see an operator-blocked scoring task** — the same blind spot the previous
residual had to be corrected for. **Decide where it ranks now; do not let it disappear for a fifth
consecutive window by default.**

**(9) Enforcement asymmetry with the hub — carried, still unruled, and evidence has accumulated.**
`ai-council` has four independent read-only validators and **no consolidated gate**; the hub has a
registry, a ship-gate verdict, and a disposition register. Two honest readings: **(a)** correct —
`ai-council` is a *code* repo, the hub is a *governance* repo, so their enforcement shapes should
differ; or **(b)** a gap — several `ai-council` gates pass **silently**, so there is no single place to
read *"is this repo healthy."* **New evidence for (b) this window:** the combined review's cross-cut
**C4** — *prose asserts guarantees the code does not honour* — which it calls **the most transferable
finding in the night set**, and which is the doc-vs-config drift **P2** exists to catch. **Do not close
this by defaulting to hub parity — rule on it.**

**(10) The inbox/CLI parity blind spot — [#69]. Structural fix, or stop calling it a blind spot.**
`LESSONS.md` records this pattern **three separate times**, each with the same rule: *investigate
whether the two paths can share a common processor; if not addressable structurally, add a parity
test.* **[#69]** is the next instance — the two entry points guard the same frontmatter key on
**different conditions**, so the same brief file yields a different panel via `--file` than via
`--inbox`. The recurrence count now argues the structural change was warranted several instances ago.
**Also unadjudicated: its severity** (combined-review **X2** — filed P2, the code audit argues P1).
Patching it in isolation makes it instance four of five.

**(11) Rulings owed, tracked but not expanded here.** Named in the JOURNAL's own "rulings still owed"
line: **[#6]**, **[#8]**, **[#73]**, plus the **[#4]** re-scope whose condition has now fired (§1).
These are listed so they are not rediscovered; none is expanded because none is this session's
gating decision.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to the backlog, the live
in-progress branches (`git branch -v`), and any **drift-flag** raised over it (§1 / `PROBES.md`
P4/P10). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is the
whole task-state.

**Cross-repo disambiguation (load-bearing — both repos have a `BACKLOG.md`):**

- **The spec for this session is `ai-council/BACKLOG.md`** — theme backbone `[E1]`–`[E7]`, story-map
  schema per hub ADR-66, `[S<n>]` story ids. Every `#id` in this residual is an **ai-council** id.
  `[E1]` (invocation surface & delegation-readiness) carries the delegation-surface work §4 items
  5/6 are about; `[E6]` (council process & epistemic quality) carries the H1/input-layer work.
- The hub's own `.dev-knowledge/BACKLOG.md` is **out of scope** — this is a cross-repo handoff and the
  hub is **read-only-adjacent**: it hosts the bundle, it is not the subject.
- **The backlog is a known under-count right now** (§1) — the moratorium means fixed-but-unticketed and
  found-but-unfiled work exists outside it. **P10 grooms the whole open set at boot** (live / dead /
  awaiting-ruling per open `#id`); **that grooming is the operator-ruled boot obligation, not optional**,
  and this window it must *also* reconcile against the unfiled audit set, which no validator can see.
- `ai-council` has **no `validate_git_backlog.py`** — the mechanical drift-check the hub row assumes
  does not exist. **P4** substitutes a manual `BACKLOG.md` ∩ `git log --first-parent` intersection, and
  **P10 is the judgment layer over it.**
