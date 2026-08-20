# PLAYBOOK status check + hygiene census — is the worktree/dispatch process in the PLAYBOOK?

<!-- scope: meta -->

**Lane:** cloud — read-only mapping lane (prep for the `[#539]`/Ch8 codification)
**Contract of record:** `docs/audits/2026-08-20-technical-playbook-status-lane-contract.md` (first commit)
**Branch:** `claude/playbook-status-census-2026-08-20` · **Base:** `origin/main` @ `1def12f`
**Target read:** `protocols/PLAYBOOK.md` @ `1def12f` — 4643 lines, read end to end
**Posture:** this lane MAPS. It edits no doctrine, rules nothing, and files no rows.

> **Citation note (PLAYBOOK Ch7 "Citation convention", :1229, applied to this artifact).** Every
> `:NNN` below is **a measurement taken against `1def12f` on 2026-08-20**, not an anchor. Each is
> paired with a quoted phrase or a heading so it stays resolvable after the lines move — which they
> will, since §3.3 of this census is a list of what happens when they don't.

---

## The operator's answer, in one paragraph

**No — the worktree/dispatch process is in the PLAYBOOK only for the LOCAL half, and only partly.**
Ch8 "Session boundaries" is already the dispatch chapter and it is substantial: it carries the
four-condition worktree launch test, provisioning, seeding, teardown, the ADR-110 batch protocol,
the `dispatch <file>` surface, and the model/effort routing matrix. What it does **not** carry is
anything about the **cloud** substrate as a dispatch target. Every occurrence of "cloud" in
PLAYBOOK.md refers to a **scheduled cloud Routine** (Ch11 — cron-triggered, self-contained,
Action-mediated, `claude/<task>-YYYY-MM-DD` branch → PR → squash-merge). That is a *different
object* from a cloud lane an operator dispatches against a frozen contract, and the file nowhere
distinguishes them. Of the **10 mechanics** the brief names, **2 are PRESENT**, **2 are PARTIAL**,
and **6 are ABSENT** — and the largest single hole is that the routing decision *"local or cloud?"*
has no home at all. Separately, the census found **19 hygiene findings**, the largest being an
11-site `HANDOFF_PROCESS v5` cluster in a file whose own frontmatter declares
`reconciled_with: handoff-process@6.2.0`.

---

## Item 1 — Coverage audit — **CLEAR**

Read `protocols/PLAYBOOK.md` end to end (4643 lines; TOC-listed headings all visited). **Ch8 already
exists** and is `## Ch8. Session boundaries` (line 1233 → 2283) — so the codification target is a NEW
SECTION INSIDE Ch8, not a new chapter. Ch8's dispatch-relevant subsections, for reference:

| Ch8 subsection | Lines |
|---|---|
| Parallel sessions & worktree discipline (per ADR-61) | 1352–1706 |
| Tree orchestration — architect-root + epic-chat lanes (ADR-97) | 1707–1791 |
| The batch protocol — ONE plan → N lanes → ONE integrator (ADR-110) | 1792–1991 |
| Dispatch visibility — Agent View shows DISPATCHED sessions only | 1992–2044 |
| Dispatch prompts and the contract of record — two locations | 2045–2086 |
| The dispatch surface is `dispatch <file>` ([#509] v2) | 2087–2171 |
| Model + effort are stated at dispatch — the routing matrix | 2172–2239 |
| Handoff prep for the next architect — an index, not a restatement | 2240–2283 |

### Verdict per mechanic

**Legend:** PRESENT = the rule is stated in PLAYBOOK.md and quotable · PARTIAL = a near-neighbour is
stated but the named mechanic is not · ABSENT = zero coverage.

---

#### 1 · Local worktree dispatch — **PARTIAL** (2 of 4 sub-mechanics)

**(a) `Dispatch-Lane` — ABSENT.** The name appears zero times. PLAYBOOK names the *predecessor*
surface only: `dispatch <contract.md>`, homed at `win-tooling scripts/dispatch/Invoke-Dispatch.ps1`
(:2106). The PowerShell module commands ratified in the 2026-08-19 window (`Dispatch-Lane`,
`Dispatch-CloudV2`, `Get-/Archive-CloudSession`, installed via `PSModulePath`) are unnamed here.

**(b) one-block dispatch — ABSENT.** `one-block` / `one block` = 0 hits. The nearest text argues the
*opposite* shape as the fallback, at :2018:

> *"Where a live nested dispatch cannot be exercised …, the fallback is dispatching `--bg` from
> inside a worktree the lane-boot protocol already provisioned — **the two steps run in sequence
> rather than composed on one command line**, with the same visibility result."*

**(c) skip-if-branch-exists (the `config.lock` race) — ABSENT.** `config.lock` = 0 hits;
`branch-exist` / `branch existence` = 0 hits. Nothing in Ch8 describes waiting on, or skipping for,
an already-created lane branch.

**(d) effort full names — PARTIAL.** The *enum-refusal* half is PRESENT and quotable (:2141):

> *"**Effort is a CLOSED enum — `{low | medium | high | xhigh}` — and a miss is a refusal, not a
> guess.** An effort value outside the enum stops the dispatch with a message naming the enum, so a
> typo surfaces at the operator's terminal rather than booting a session at an effort nobody chose."*

The *platform fact* is ABSENT: nothing states that `--effort` accepts **full names only** and that
**short forms are silently ignored** (SUPPLEMENT §6). That is the dangerous half — the enum refusal
fires on an unknown token, not on a silently-dropped abbreviation.

**What IS present and worth not re-deriving** — the doubled-prefix defect class, in full, at
:2096–2105: `--worktree` takes the **bare** lane name, the provisioner prefixes `worktree-` exactly
once, and batch 6 produced `worktree-worktree-lane-a-409-conversions` uniformly across twelve lanes
because a hand-assembled line passed the intended *branch* name. `[#531]` is named as the gate.

---

#### 2 · Cloud dispatch — **ABSENT** (0 of 4 sub-mechanics)

**(a) `Dispatch-CloudV2` API path (`POST /v1/sessions`) — ABSENT.** 0 hits.
**(b) receipt gate — ABSENT.** 0 hits.
**(c) web-UI fallback — ABSENT.** 0 hits.
**(d) CLI `--cloud` ban — ABSENT.** 0 hits. The three measured-dead transports (ARG truncation at
newlines+quotes, STDIN creating no session, BRIEF-ON-BRANCH with no remote) are recorded nowhere in
the repo outside the handoff bundle's answer 3.

**The load-bearing distinction the file does not draw.** PLAYBOOK's cloud material is Ch11
"Routine/night deployment standard" (:2347–2444) plus Ch10's row at :2318 — and it is entirely about
**scheduled Routines**:

> *":2318 — **Cloud Routine** — self-contained (clones only its own repo, reads no sibling — ADR-72/73);
> read-only schema-bound agents + skeptic; output via its **declared channel**: a
> `claude/<task>-YYYY-MM-DD` branch → PR → the GitHub Action diff-guards and **squash-merges**…"*

An operator-dispatched cloud lane shares the `claude/*` branch prefix and nothing else: no Routine
trigger, no PR, no diff-guard, no squash-merge — it is harvested by `--no-ff` merge like a local
lane. A reader arriving at Ch11 looking for "how do I dispatch a cloud lane" is served a section
that answers a different question without saying so. **Ch11's "Cloud-session closeout" (:2388) is
the one paragraph that half-applies** — "check for stranded `claude/*` branches … and prune the
orphans" — but it is scoped to Routine runs and never mentions push-before-delete.

---

#### 3 · Local-vs-cloud routing rule (substrate decides) — **ABSENT**

Zero coverage, and this is the single largest hole. PLAYBOOK carries **three** routing/launch
decisions and none of them is this one:

| Existing decision | Where | What it decides |
|---|---|---|
| Four-condition worktree test ([#441]) | Ch8 :1454–1493 | **whether** to parallelize at all |
| Model + effort routing matrix | Ch8 :2172–2239 | **which tier** a dispatched lane boots at |
| Dynamic-Workflow escalation ladder | §2 :3085–3109 | **which orchestration rung** (Sonnet / Opus / Workflow) |

None asks **where the work runs**. The nearest thing to the ratified rule (*needs-local-CLI / auth /
timing ⇒ local; read-only + drafts, docs-only ⇒ cloud*) is the SUPPLEMENT §5 sentence *"cloud lanes
read-only + docs-only artifacts (the N4 rule)"* — and `N4` and `docs-only` both return **0 hits** in
PLAYBOOK.md. The doctrine that governs which substrate a lane lands on lives entirely in chat.

---

#### 4 · Harvest procedure — **ABSENT** (0 of 3 sub-mechanics)

**(a) git-based harvest (never log-scraping) — ABSENT from PLAYBOOK**, though it is *specified* in
`BACKLOG.md [#540]` ("watch the board via `claude agents --json --all` on `state == "done"`, then
fetch each packet by `git show <branch>:<path>` — **never** by parsing `claude logs`, which is ANSI
screen replay rather than data"). A BACKLOG row is a build spec, not doctrine — the rule binds only
if `harvest_batch.py` ships.

**(b) push-before-delete — ABSENT.** `push-before-delete` = 0 hits in PLAYBOOK. It exists once, in
`JOURNAL.md` entry (i) :138, as a standing order:

> *"**Standing order recorded.** The operator accepted push-before-delete as the rule for every future
> harvest: a merged branch is deleted on origin only AFTER the merge is pushed, so no window exists
> in which integrated work lives solely in a local clone."*

A JOURNAL entry is an immutable record of a session, not a rule surface a future seat reads. Ch8's
teardown text (:1657–1706) is the *worktree* round-trip and says nothing about remote-branch deletion
ordering.

**(c) integrator as gate-of-record for index freshness — ABSENT.** `gate-of-record` = 0 hits.
Ch8's refuse-to-finish item 4 covers manifest/packet archival but not index regeneration; the
sanctioned **declared single-hook bypass on a lane branch** appears nowhere. This is the rule this
very lane executed under (`SKIP=audit-index-freshness` on its dispatch-stamp commit) — it is live
practice with no written home, which is exactly the condition `[#539]` exists to end.

*JOURNAL entry (h) :153–162 is the lived procedure in full* — survey `origin/claude/*`, verify each
artifact on its own branch tip and quote its receipt before merging, run the queue serially `--no-ff`,
re-check the docs-only rule immediately before each merge, regenerate the index ONCE after the queue
closes. That paragraph is the draft of the missing section.

---

#### 5 · primary-is-seat-arc-only — **ABSENT**

`seat-arc` = 0 hits. PLAYBOOK's primary-checkout doctrine points the *other* way — it establishes
the primary as the place where git work happens:

> *":1655 — **Integrate from the primary:** from the primary on `main`, `git merge --no-ff
> worktree-<name>` then `git push`"*
> *":1649 — **`/review-closures` also runs from a primary on-`main` session, not a worktree.**"*

The ratified rule ("primary checkout is seat-arc-only; helper tasks run **zero git ops** in primary",
two witnessed HEAD-swap incidents) is a *restriction* on top of that, and the restriction is
unwritten. Nearest cousin present: :1364 *"A long gate/suite run and a commit are mutually exclusive
IN THE SAME TREE"* — same family (one tree, one actor), different rule.

---

#### 6 · contract-as-file without exception — **PARTIAL**

The principle IS present, at :2045–2086, with its evidence and its honest limit:

> *"**The repair path, for batch 3: at dispatch, the batch manifest links or embeds each frozen lane
> contract as a committed repo artifact.** Dispatch convenience stays in the prompts dir; the
> authoritative copy lands with the manifest…"*
>
> *"**Honest limit, stated so this is not read as done.** This is a documented path, not a mechanism:
> nothing checks that a manifest's lane rows resolve to committed contracts, and [#505] clause 1 stays
> falsified until a batch actually runs that way."*

**Why PARTIAL and not PRESENT:** it is framed as *"the repair path, for batch 3"* — a forward-looking
remedy scoped to one batch — not as an unconditional standing rule. "Without exception" is the part
that is missing, and it matters: the same section still describes the prompts dir as a live delivery
channel and the fallback table-parsing path as available for *"an older contract"*. A seat reading
this today can lawfully conclude a chat-pasted contract is acceptable. `STANDING_RULINGS` I-D3 (cited
at :781) carries the stronger form; PLAYBOOK does not restate it here.

---

#### 7 · lane-never-journals — **ABSENT**, and the nearest present text reads the other way

`never journals` = 0 hits. Ch8 states, as its anchoring law (:1902):

> *"**JOURNAL-rides-the-branch is the anchoring law.** An arc's JOURNAL entry is written **on that
> arc's own branch, ahead of the merge** (STANDING_RULINGS B2)."*

and the only lane-scoped carve-out is about *letters*, not entries (:1504):

> *"**The letter-allocation convention** … JOURNAL letters are assigned **at integration**, by the
> primary's single writer — **lanes never allocate.**"*

**These are reconcilable but not reconciled.** "JOURNAL-rides-the-branch" is written about an *arc*
(which owns a merge); a *lane* hands its branch back and the integrator owns the merge, so the
integrator writes the entry — and Ch8's own ≥2-commit integrator-branch rule (:1915) assumes exactly
that. So the flat rule "a lane never journals" is consistent with Ch8's intent while being nowhere in
its text. **The codification lane must state it explicitly rather than let a reader infer it**, because
the literal reading of :1902 tells a lane to write a JOURNAL entry on its own branch, and a lane that
does so collides with the integrator on the fleet's single hottest file.

---

#### 8 · receipt-first on every cloud dispatch — **ABSENT**

`receipt` = 0 hits in PLAYBOOK. The gate ("sources non-empty + first assistant text echoed") is
recorded once, in SUPPLEMENT §7 item 6, as debt with a named home: *"home: Ch8 + the [#539]
generator."* The harvest side of the same discipline was practised in JOURNAL (h) — *"Verified each
lane's artifact on its own branch tip and **quoted its receipt** before merging anything"* — so the
verb is already in the repo's vocabulary with no definition behind it.

---

### Coverage tally

| | Count | Mechanics |
|---|---|---|
| **PRESENT** | **2** | *(sub-mechanics)* effort enum-refusal; `--worktree` bare-name / doubled-prefix rule |
| **PARTIAL** | **2** | local worktree dispatch (2 of 4); contract-as-file (principle yes, "without exception" no) |
| **ABSENT** | **6** | cloud dispatch (all 4 sub-parts) · local-vs-cloud routing · harvest procedure (all 3 sub-parts) · primary-is-seat-arc-only · lane-never-journals · receipt-first |

Counting the brief's ten named mechanics at top level: **0 fully PRESENT · 2 PARTIAL · 8 ABSENT**.
Counting sub-mechanics (18 total): **2 PRESENT · 16 ABSENT**.

---

## Item 2 — Gap table — **CLEAR**

Target homes are stated as **new subsections inside the existing Ch8**, in the order they should
appear (each slots between named live subsections so the chapter's argument still runs
whether→how→where→dispatch→harvest). Size: **S** ≈ ≤15 lines, one rule + its evidence; **M** ≈
25–60 lines, a rule set with a table or worked example.

| # | Mechanic (ABSENT/PARTIAL) | Where it lives today | Target PLAYBOOK home | Size |
|---|---|---|---|---|
| G1 | **Local-vs-cloud routing rule** — substrate decides: needs-local-CLI/auth/timing ⇒ local; read-only + drafts, docs-only ⇒ cloud | chat register (SUPPLEMENT §5 "the N4 rule"); nowhere in-repo | **NEW** Ch8 § *"Which substrate — local worktree or cloud lane"*, placed immediately after "0 — Launch decision"/four-condition test, :1454–1493 so WHETHER→WHERE read together | **M** |
| G2 | **Cloud dispatch — the API path** (`Dispatch-CloudV2`, `POST /v1/sessions`), incl. endpoint/headers/`environment_id` drift warning + RE-TEST pointer | win-tooling module + its README (cross-repo); SUPPLEMENT §6 | **NEW** Ch8 § *"Cloud dispatch — the API path"*, after "The dispatch surface is `dispatch <file>`" (:2171) | **M** |
| G3 | **Receipt gate + receipt-first** — sources non-empty + first assistant text echoed, on every cloud dispatch | SUPPLEMENT §7 item 6 (debt, home named as "Ch8 + the [#539] generator") | same NEW § as G2 (its gate clause) | **S** |
| G4 | **CLI `--cloud` ban** + the three measured-dead transports (ARG truncate, STDIN no-session, BRIEF-ON-BRANCH no-remote) | SUPPLEMENT §3 "do not relitigate" | same NEW § as G2 (a *"considered and measured dead"* clause, so it is not re-tried) | **S** |
| G5 | **Web-UI fallback** — when the API path is unavailable, and what it costs | chat register (SUPPLEMENT §2 tension) | same NEW § as G2 (fallback clause) | **S** |
| G6 | **`Dispatch-Lane`** — the local command name + its one-block shape + skip-if-branch-exists (`config.lock` race) | win-tooling module (cross-repo home); memory | **AMEND** the live Ch8 § "The dispatch surface is `dispatch <file>` ([#509] v2)" (:2087) — it already owns the local dispatch surface and currently names only the superseded `Invoke-Dispatch.ps1` route | **M** |
| G7 | **`--effort` takes full names only; short forms are silently ignored** | SUPPLEMENT §6 (operator state) | **AMEND** Ch8 § "Model + effort … routing matrix" (:2141, beside the closed-enum refusal it completes) | **S** |
| G8 | **Harvest procedure** — survey `origin/claude/*`, verify each artifact on its branch tip and quote its receipt, serial `--no-ff` queue, re-check docs-only per branch, regenerate indexes ONCE at close | `JOURNAL.md` (h) :153–162 (lived, immutable record); build spec in `BACKLOG.md [#540]` | **NEW** Ch8 § *"Harvest — the return leg"*, after the batch protocol's refuse-to-finish checklist (:1897) | **M** |
| G9 | **Push-before-delete** on every harvest | `JOURNAL.md` (i) :138 (standing order) | same NEW § as G8 (one clause) | **S** |
| G10 | **Integrator is gate-of-record for index freshness on lane material; a declared single-hook bypass on a lane branch is sanctioned** | chat register (SUPPLEMENT §7 item 1, ruling 9); `JOURNAL.md` :34 records it as *ruled off-repo, transcription owed* | same NEW § as G8 + a cross-reference clause in the lane-contract requirements list (:1819) | **S** |
| G11 | **primary-is-seat-arc-only** — helper tasks run zero git ops in primary (two HEAD-swap incidents) | chat register (SUPPLEMENT §7 item 4 — home named as STANDING_RULINGS) | **STANDING_RULINGS** primarily, per its own named home; a one-line Ch8 pointer beside "Integrate from the primary" (:1655) | **S** |
| G12 | **lane-never-journals** — and its explicit reconciliation with "JOURNAL-rides-the-branch" (:1902) | chat register / practice | **AMEND** Ch8 § batch protocol, at the JOURNAL-anchoring-law paragraph (:1902) — a lane clause beside the existing letter-allocation clause | **S** |
| G13 | **Contract-as-file WITHOUT EXCEPTION** — promote the batch-3 "repair path" (:2065) to an unconditional rule; retire the prompts-dir-as-storage reading | PLAYBOOK :2045–2086 (present as a scoped path) + `STANDING_RULINGS` I-D3 | **AMEND** Ch8 § "Dispatch prompts and the contract of record" (:2045) | **S** |
| G14 | **Cloud lanes branch fresh off `origin/main` and never touch foreign dirty files** | chat register (SUPPLEMENT §7 item 5 — home named as Ch8) | same NEW § as G2 (lane-hygiene clause) | **S** |

**Totals: 14 rows — 4 M, 10 S. 3 NEW Ch8 subsections + 4 amendments to live ones.**
Rough write budget: ~150–200 lines added to Ch8, which is the largest single addition Ch8 has taken.

**One authoring constraint the codification lane must respect, or it re-creates the problem it is
fixing:** PLAYBOOK's cloud vocabulary is already taken by Ch11's **scheduled Routines**. G1/G2 must
open by *naming the distinction* (dispatched cloud lane ≠ scheduled cloud Routine) and cross-link
Ch11, or the two populations silently merge — the same undeclared-scope-collision class Ch8 already
records twice (the epic-lane vs work-lane cap at :1740, the `execution` mode label at :3117).

---

## Item 3 — PLAYBOOK hygiene census — **CLEAR** (19 findings)

Scoped to `protocols/PLAYBOOK.md` only, at `1def12f`. Severity is this lane's judgment, not a ruling.

### 3.1 The two known sites — state at my HEAD

**Both are UNFIXED.** The hygiene lane did not reach either.

| Line | Claim as written | Live value | Verdict |
|---|---|---|---|
| **2194** | *"`audit.py`'s **41-member** `ALL_CHECKS` registry"* | **43** members; last = `check_landing_predicate` (counted from `scripts/audit.py:3398` — the literal list, `re.findall` over `^    (check_\w+),`) | **STALE by 2.** Verified mechanically, not by eye. Note `audit.py checks` could not be run in this container (`ModuleNotFoundError: click`), so the count is from the source list, which is the same list the CLI prints. |
| **1862** | *"A batch closes when all **five** hold … (ADR-110 §3 enumerates four, so the fifth rides as a recorded addition here until the ADR is amended.)"* | **SIX.** `.claude/commands/lane-integrate.md:53` — *"Run all six"* — item 6 = *"No `refs/locks/*` left held for this batch's contracts"* (`single_flight.py inspect`, `[#530]`). `CLAUDE.md` §7 already says *"six-item refuse-to-finish checklist"*. | **STALE by 1 — and it is the doctrine surface that is behind its own command.** PLAYBOOK is cited as the checklist's home (":1897 `/lane-integrate` walks this list mechanically") while the command walks a longer list. |

### 3.2 Stale counts and self-contradictions

| # | Line | Finding | Live value |
|---|---|---|---|
| H1 | 2194 | `ALL_CHECKS` "41-member" | **43** |
| H2 | 1862 | refuse-to-finish "five" | **six** (`lane-integrate.md:53`) |
| H3 | 2955 | *"Numbered, repeatable recipes (**§1–§19**)"* | The file's own header at :12 says *"numbered recipes **§1–§21**"*, and §20 + §21 both exist (:4388, :4421). Internal contradiction, 2 sites. |
| H4 | 1051 | CLAUDE.md described as a *"**10-section** template"* in the file-type taxonomy | **12 sections** — stated correctly 995 lines earlier at :334 (*"v2.1 template, 12 sections"*) and true of the live `CLAUDE.md`. Self-contradiction inside one file. |
| H5 | 8 | Header: *"Last updated: **2026-08-01**"* | The file carries content dated **2026-08-16** (the batch-6 doubled-prefix witness, :2090). Stale by 15 days / at least one substantive edit. |

### 3.3 Dead / drifted file:line locators

Every `path:line` and `path Lnn` locator in the file was resolved against the live tree. **6 of 7
are wrong.** (The file's own Ch7 citation convention at :1229 already rules that *"Line numbers are
recorded as **the measurement taken on a date**, not as the anchor"* — none of these six carries a
date, so they read as anchors and rot as anchors.)

| # | Line | Locator as cited | What is actually there | Live carrier |
|---|---|---|---|---|
| H6 | 298 | `ARCHITECTURE.md:106` — *"Claude Code, Layer 3, commits the handoff"* | *"organ map gained a **Status** column; Ch6's nightly loop marked broken at the triage"* | **`ARCHITECTURE.md:193`** — `L3 -> L2: handoff -> git commit` |
| H7 | 885 | `pyproject.toml` **L83–91** — cited for the `-p no:xdist` measurement | mutmut `source_paths` / `only_mutate` commentary | **`pyproject.toml:93–103`** (the CRITICAL INTERACTION block) |
| H8 | 937 | `scripts/gen_intake_index.py:44` — *"**Live instance**: compiles `_FM_KV_RE = r"^([a-z0-9-]+)…"`… The probe is green because it is looking at zero keys."* | line 44 is blank; **`_FM_KV_RE` no longer exists in the file** | **FIXED.** `_parse_frontmatter` (:48) uses a real YAML parse; its docstring at :55 records *"WHY THE HAND-ROLLED REGEX WENT: its key class was `[a-z0-9-]+`, which has no underscore."* The doctrine paragraph presents a **repaired** defect as live. |
| H9 | 1211 | `scripts/gen_audit_index.py:57` — *"reading `audits_dir.glob("*.md")` unfiltered"*, in a paragraph that says *"three instances, **one of them live and unfixed when this was written**"* | line 57 is blank | **FIXED, by the very repair the paragraph prescribes.** The glob is at **:134** and is now gated by `_is_tracked(...)` against `tracked_files()` (`git ls-files`, :66); the module header at :18 states *"TRACKED FILES ONLY, and this is the determinism boundary."* |
| H10 | 2637 | `tests/test_enforcement_coverage.py:389` | the `sys.path.insert` inside the `_SHADOW_PROBE` literal is at **:386** | off by 3 |
| H11 | 3117 | `HANDOFF_PROCESS.md:704` — *"the field name 'Execution MODE'"* | :704 is about `lane-boot.md` / `prompt-template.md` | **`HANDOFF_PROCESS.md:786`** — `7. **Execution MODE**` |
| H12 | 3117 | PLAYBOOK's own self-locator *"the handoff boot-mode at `:3148`"* | :3148 is a code-fence `LEGEND` line inside §2 "Structure" | the boot-mode is the `--mode execution` row of the §8 handoff table (:3756). A self-locator that has drifted inside its own file is the exact failure Ch7's citation ruling names. |

*(`ARCHITECTURE.md:14` at :298 is the one locator that still resolves — the phrase "class this repo
exists to kill" is genuinely on line 14. Not counted as a finding.)*

### 3.4 Sections contradicted by later rulings / superseded state

| # | Line(s) | Finding | Severity |
|---|---|---|---|
| H13 | **11 live sites** — 1061, 1194, 2677, 2769, 3268, 3277, 3731, 3737 (+ TOC 180), 3788, 3896, 4135 | **`HANDOFF_PROCESS v5` cluster.** The file's own frontmatter declares `reconciled_with: handoff-process@6.2.0`, and `protocols/HANDOFF_PROCESS.md:1` reads `# HANDOFF_PROCESS v6` / `Version: 6.2.0`. Meanwhile PLAYBOOK says *":3731 Operational authority: `protocols/HANDOFF_PROCESS.md` **v5** (ADR-82…)"*, has a heading *":3737 ### What the **v5** handoff carries"*, calls the current bundle *":1194 **v5 handoff (current)**"* and the taxonomy row *":1061 (**v5.4** bundle) … per HANDOFF_PROCESS **v5.4**"*, and describes `/handoff` twice as *"per HANDOFF_PROCESS **v5**"* (:2677, :2769) where `.claude/commands/handoff.md` and `CLAUDE.md` §7 both say **v6 (ADR-82)**. **The declared-edge stamp is current while the prose it governs is a version behind** — the `reconciled_versions` gate checks the stamp, which is exactly the split Ch6 :1111 warns about, and the `check-against-spec` re-stamp flow (Ch6 :1115) is the organ that should have caught it on the v5→v6 bump. *(Legitimately historical and NOT counted: :1193 "v4 … superseded by v5", :3279 "pre-v5 frozen copies", :3735 "ADR-82 (v5 ratification)". Process-version stamps :1751 "(v5.6)" and :3903 "v5.5" are separately unverified against the v6 spec.)* | **HIGH** |
| H14 | 2770 | **`/override` is described as live and load-bearing** — *"`/override` (repo) — logged, HEAD-bound bypass of the ADR-85 session-end gate (**the gate's only escape**)"*. Directly contradicted by the ADR-85 amendment 2026-08-03 §A2, carried in `CLAUDE.md` §7: `/override` *"no longer discharges the ADR-85 obligation… and the sole escape for the pre-push hard leg is `git push --no-verify`"*. `.claude/commands/override.md`'s own description reads **"RETIRED"**. PLAYBOOK tells a reader to reach for a retired organ **and** names it the only escape. | **HIGH** |
| H15 | 2677, 2769 | `/handoff` "per HANDOFF_PROCESS v5" (subset of H13, listed separately because these two are the *operator-facing invocation* rows) | MED |
| H16 | 2662–2686 | **Ch14 "Usage protocol" command table is incomplete against the live roster.** It lists 7 commands; `.claude/generated/commands-repo.md` (machine-generated from disk) carries 8, and the table omits `/handoff-verify`, `/preflight`, `/lane-boot`, `/lane-integrate`, `/changelog-review`(listed) and the plugin's `/review-closures` (present in the 7b list at :2772 but not in the "when to invoke" table). **Mitigated by design:** the section opens *"When it drifts from `ls ~/.claude/commands ~/.claude/skills`, **the filesystem wins**"*, and the hooks half already pointerizes to CLAUDE.md §9 after two witnessed re-drifts. The commands half has not taken the same treatment. | MED |
| H17 | 3128–3143 | **Platform pins are 45 days past their own stamp.** `<!-- last-verified: 2026-07-06 -->`, pinned to *"Claude Code 2.1.202"*. Ch8 checks the CLI twice at **2.1.224** (:2018, :2218), and the active handoff bundle's SUPPLEMENT §6 records verification against **2.1.235**. Three CLI versions cited across one file with no reconciliation, and the section's own instruction — *"re-ground them against `claude --version` … before trusting"* — is the correct posture but is not a gate. | MED |
| H18 | 4234 | *"Option A — `/code-review` **ultra** … (`/ultrareview` is the deprecated alias)"*. The live `/code-review` skill takes effort levels `low/medium/high/xhigh/max` and reuses the last level typed; `ultra` is not among them. | LOW |

### 3.5 TODO / TBD left in doctrine text

| # | Line | Finding | Severity |
|---|---|---|---|
| H19a | 605 | § **Secrets storage path** — *"**[TBD — Stream C session 3, ADR-33]**"*. **The ADR pointer is wrong**: `docs/decisions/ADR-33-vision-universalization.md` is *"VISION.md universalization across ecosystem repos"* (Accepted 2026-04-28) and has nothing to do with secrets. The section also hard-codes a live absolute path — `C:\Users\1028120\Documents\.secrets\.env` — into a governance doc. **Genuinely undone AND mis-pointed**, ~3.8 months past its named session. | MED |
| H19b | 612 | § **Capitalization conventions** — *"**[TBD — Stream C session 3, ADR-34]**"*. **This one is discharged and not marked**: `ADR-34-file-naming-convention.md` is **Accepted 2026-04-29** and carries the casing table (*"Living docs (root) │ UPPERCASE.md"*, *"Protocols │ UPPERCASE_WITH_UNDERSCORES.md"*) — the exact question the TBD poses. The sibling § at :507 already pointerizes to ADR-34 correctly. A live TBD sitting on a ratified decision. | MED |

*(No `TODO`/`FIXME` tokens appear in doctrine text. The three `TODO` hits at :1005/:1020/:3434 are
legitimate — two name the `todo-tree` VS Code extension, one forbids placeholder TODOs in ADRs. The
`[TBD]` at :470 is a correct forward-reference to the two above.)*

### 3.6 Census summary

**19 findings: 2 HIGH · 10 MED · 7 LOW-or-mechanical.**

- **stale counts / self-contradictions:** 5 (H1–H5)
- **dead or drifted file:line locators:** 7 (H6–H12) — 6 of the 7 distinct locators in the file are wrong; **2 of them (H8, H9) describe defects that have since been FIXED**, which is worse than a wrong line number: the doctrine paragraph teaches a repaired instance as a live one
- **contradicted by later rulings / superseded state:** 6 (H13–H18) — dominated by the 11-site v5/v6 cluster and the retired `/override`
- **TBD in doctrine:** 2 (H19a mis-pointed and undone; H19b discharged but unmarked)

**Cheapest high-value repairs, if a hygiene lane is dispatched:** H14 (`/override`, one bullet, and
it currently mis-directs a reader to a retired organ), H1/H2 (two integers), H19b (a TBD that a
ratified ADR already answers). H13 is the expensive one and is genuinely a `check-against-spec`
re-stamp arc, not a find-and-replace — several v5 sites are legitimately historical.

---

## Item 4 — The codification lane's brief, drafted — **CLEAR**

House pattern (frozen contract + `## Dispatch` block, per Ch8 :2165 — *"Every lane or arc contract
opens with a `## Dispatch` block carrying its own literal dispatch line"*). Sized **M**: one lane, one
file, ~150–200 added lines, no new machinery.

**The `[#539]` generator's role, stated as the brief states it:** `gen_lane_contract.py` is
**assembly, not generation** — it emits the *mechanical* regions of a lane contract from the batch
manifest and leaves the judgment regions as explicit FILL-IN, and its `--check` leg arms two organs
that are wired into no gate today (`validate_branch_naming`, `preflight_contract`). The codification
lane therefore **writes the doctrine `[#539]` will later assemble against, and does not build it**:
Ch8 must state the dispatch line's shape, the effort enum, the receipt gate and the substrate rule as
*checkable* rules, because those are precisely the regions the generator's `--check` leg will have to
verify. Doctrine first, generator second — the reverse order produces a generator that encodes rules
no document owns.

````markdown
# LANE — CODIFY THE DISPATCH RUNBOOK INTO PLAYBOOK Ch8 ([#539])

| Model | Mode | Effort |
|---|---|---|
| opus | execution — single-file doctrine write | high |

Local worktree lane (this one edits `protocols/PLAYBOOK.md`, so it is NOT a cloud lane — the
substrate rule this lane is writing routes it here: it touches a freshness-gated canonical file
and must run the local gate mesh). FIRST COMMIT = dispatch-stamp: this contract as
`docs/audits/2026-08-2X-technical-ch8-dispatch-codification-lane-contract.md`.
Fresh branch off origin/main. Commit-and-STOP; the integrator merges.

## Dispatch

```powershell
dispatch $env:CLAUDE_PROMPTS_DIR\2026-08-2X-technical-ch8-dispatch-codification-lane-contract.md
```

SOURCE OF RECORD — read these three first, in this order, and treat the third as the map:
1. `docs/audits/2026-08-20-technical-playbook-status.md` — the gap table (G1–G14) IS your work
   list; each row names its target home and size. Do not re-derive it.
2. `docs/handoffs/2026-08-20-dev-knowledge-architect/SUPPLEMENT.md` §3, §5, §6, §7 — the
   ratified-in-chat register. Items 1, 3, 4, 5, 6 are the rules you are transcribing; §3 is the
   do-not-relitigate list that G4 records.
3. `protocols/PLAYBOOK.md` Ch8 (lines 1233–2283) — the chapter you are amending. Read it end to
   end before writing one line; you are inserting into a live argument, not appending to a list.

FOOTPRINT — exactly one file: `protocols/PLAYBOOK.md`. Nothing else. Not BACKLOG, not `tasks/`,
not STANDING_RULINGS, not ARCHITECTURE, not JOURNAL (the integrator anchors this arc).

ITEMS (CLEAR/BLOCKED each):
1. **THREE NEW Ch8 subsections**, in the gap table's stated positions:
   (a) *"Which substrate — local worktree or cloud lane"* after the four-condition test, :1454–1493 —
       G1. State the rule as a checkable two-way test, not prose: needs-local-CLI / auth / timing /
       a gate-mesh-bound canonical file ⇒ LOCAL; read-only + drafts + docs-only artifact ⇒ CLOUD.
       OPEN WITH the distinction from Ch11's scheduled Routines and cross-link it — if you skip
       this the two populations merge and you have created the collision class Ch8 already
       records twice (:1740, :3117).
   (b) *"Cloud dispatch — the API path"* after :2171 — G2, G3, G4, G5, G14 as clauses of one
       section: the `Dispatch-CloudV2` `POST /v1/sessions` path with its drift warning and RE-TEST
       pointer; the RECEIPT gate (sources non-empty + first assistant text echoed) as a
       precondition, not a nicety; the three measured-dead CLI `--cloud` transports recorded as
       considered-and-refuted so nobody re-tries them; the web-UI fallback and what it costs;
       fresh-off-`origin/main` + never-touch-foreign-dirty-files.
   (c) *"Harvest — the return leg"* after the refuse-to-finish checklist (:1897) — G8, G9, G10.
       JOURNAL entry (h) :153–162 is your draft; push-before-delete is JOURNAL (i) :138 verbatim.
2. **FOUR AMENDMENTS to live Ch8 subsections** — G6 (`Dispatch-Lane` + one-block +
   skip-if-branch-exists into the `dispatch <file>` section, :2087), G7 (`--effort` full-names-only
   beside the closed-enum refusal, :2141), G12 (lane-never-journals beside the letter-allocation
   clause, :1504 — and RECONCILE it explicitly with "JOURNAL-rides-the-branch" at :1902, which a
   lane reading literally would obey and collide), G13 (promote contract-as-file from "the repair
   path for batch 3" to unconditional, :2045).
3. **State each rule so `[#539]`'s `--check` leg could verify it.** You are writing the doctrine
   `gen_lane_contract.py` will assemble against: the generator emits the mechanical regions of a
   contract and its `--check` refuses an off-enum branch name or an unresolvable locator. A rule
   phrased as taste gives it nothing to check. Ch4 "Checkable rules: concrete over aspirational"
   (:741) is the bar — apply it to your own output.
4. **Every rule carries its evidence and its honest limit**, in Ch8's existing voice: the witnessed
   incident (the doubled-prefix batch-6 case at :2093 is the model), and what is NOT mechanized.
   Say plainly which of these are prose-only today — most are.
5. **Budget + gate check before you stop:** re-run `python scripts/toc/…` (the
   `toc-freshness-playbook` hook regenerates the TOC — your three new headings MUST land in it),
   and confirm `audit-health` passes. Report the added-line count.

OUTPUT: amended `protocols/PLAYBOOK.md` on your branch, plus a STOP packet listing which of
G1–G14 landed, which were BLOCKED and why, and the line delta.

NOT: no BACKLOG/`tasks/` writes · no STANDING_RULINGS edits (G11 is routed there by its own
ruling and is NOT this lane's — say so in the packet and leave it) · no rulings of your own · no
hygiene fixes (the census H1–H19 is a SEPARATE lane; fixing a stale count while writing new
doctrine mixes two review surfaces in one diff) · no merge · no JOURNAL.
````

**Two notes for whoever dispatches it.**

1. **This lane is deliberately local, not cloud** — and that is the substrate rule it is writing,
   applied to itself. It edits `protocols/PLAYBOOK.md`, a `last_reviewed`-stamped canonical file
   behind the `toc-freshness-playbook` and `audit-health` gates, so it needs the local gate mesh and
   fails the docs-only test that admits a cloud lane.
2. **G11 (primary-is-seat-arc-only) is excluded on purpose.** Its own ratified home is
   `STANDING_RULINGS.md` (SUPPLEMENT §7 item 4), not Ch8, and this lane's footprint is one file.
   Routing it here would widen the lane past its contract — it belongs in the transcription act the
   handoff already names as the next seat's first move.

---

## What this lane did NOT do

No PLAYBOOK edits (Item 4 drafts the contract that would make them; it does not make them). No
rulings — every "should" above is a recommendation to the architect. No index regeneration; this
lane's two commits carry a declared `SKIP=audit-index-freshness`, and `docs/audits/README.md` is
the integrator's to regenerate once. No JOURNAL entry — a lane never journals.

**Unverifiable from this container, stated rather than assumed:** `python scripts/audit.py checks`
could not run (`ModuleNotFoundError: click`), so H1's live count of 43 is read from the `ALL_CHECKS`
literal at `scripts/audit.py:3398` rather than from the CLI that prints it. The win-tooling repo is
outside this session's repository scope, so every claim about `Dispatch-Lane` / `Dispatch-CloudV2` /
`Get-`/`Archive-CloudSession` is sourced from the handoff bundle's SUPPLEMENT, which is what makes
them *chat-register* items in the gap table rather than verified cross-repo facts.
