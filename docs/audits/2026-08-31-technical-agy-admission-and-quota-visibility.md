> **PROVENANCE - harvested cloud artifact, body VERBATIM below this header.**
> Lane `batch-e-a7-agy-admission-and-quota-visibility` | receipt id `cse_0161NBLfKDSitbRmTbZtQ3oq` | dispatched 2026-08-31, harvested 2026-08-31 by
> `Save-CloudSessionReport` (the `Harvest-Cloud` alias). Batch E tier (A); the frozen contract is
> `docs/audits/2026-08-31-technical-batche-launch-contracts/LANE-batch-e-a7-agy-admission-and-quota-visibility.md`.
> Selection rule: the LONGEST assistant text, not the last - text #2 of 11 across 6 pages.
> Bytes written unchanged: **33,517**.
> Harvester DEVIATION, recorded not repaired: the report contains no markdown heading at all; bytes UNCHANGED.
> Nothing below this line was edited, reflowed or trimmed.
>
> **Consumed by:** HY-4 (`lane-n-14-trends-burndown-and-quota-panel`, the quota panel folded in by CUT-5) and `[#578]`.
>
> **This lane was READ-ONLY by contract** - zero tree writes, zero commits, zero rows, no gate
> run and none asserted.

---

All reads are done. Here is the lane's entire deliverable — read-only, no file written, no commit, no branch, no row.

```
LANE batch-e-a7-agy-admission-and-quota-visibility — STATUS REPORT
Substrate: cloud (claude/ prefix) · Mode: read-only by contract · Gate legs run: NONE

================================================================================
0. RECEIPT
================================================================================
git-source-resolves-non-empty: https://github.com/rdwornik/dev-knowledge
  (origin fetch+push, `git remote -v`); HEAD = ec8731a9b2fdcc7fffee59bb0743a8b467f65c0b
  ("Merge branch 'docs/window-close' -- WINDOW CLOSE: two rulings, ADR-116 recovered,
  the five pillars"); working tree clean (`git status --porcelain` empty); no branch
  created, no commit, no push.
first-assistant-text-echoed: 124 lines total; final line verbatim:
  "- No edits outside this lane's declared footprint. Prose in English; hyphen-only names."

Evidence pins used throughout:
  ecosystem/provider-registry.yaml  blob 086b4a567994db68a9c136d1ab5eeedb4194c18d
  ecosystem/routing-table.yaml      blob 83ac4cac3c76d95300e0535c0712317bef94d08a

GATE POSTURE, declared: this lane ran NO gate — no pytest, no ruff, no audit.py. I did
not invoke python3 or uv at all. Every claim below is a file read, a git read, or a
network read, each labelled as such. No gate result is asserted.

================================================================================
1. ADMISSION STATUS, VERIFIED AT HEAD — the agreement table
================================================================================
Answer: agy is NOT ADMITTED for the ANALYSIS role, and nothing at HEAD has changed
that. It is REGISTERED PRESENT and DELIBERATELY UNROLED, exactly as the contract's
freeze-time reading says. Verified surface by surface:

surface: ecosystem/provider-registry.yaml
  says: `antigravity` provider row EXISTS (:182-224). council_alias: null (NOT
    PANELLED). cli: agy · version_command: ["agy","--version"]. Measured facts carried:
    PRESENT/VERSION 1.1.20 (2026-08-25), 1.1.21 (2026-08-26), AGENTS.md-native by
    execution, AUTH by server round-trip, PATH 19/39, SERVED families incl.
    gemini-3.7-flash-{high,medium,low} and gemini-3.1-pro-{high,low}.
  admission: the block at :212-216 is byte-for-byte what the contract quotes — "NO ROLE,
    AND THE CONSEQUENCE IS NAMED RATHER THAN ACTED ON ... That is a `[#578]` RERUN
    QUESTION, not a registry act ... R3 owns roles; nothing here admits, refuses, or
    re-opens an admission verdict."
  last touched: ddf6202 (2026-08-28) for this row; the only later edit, 86bed82
    (2026-08-29), added `copilot-enterprise` and did not touch `antigravity`.
  verdict: REGISTERED PRESENT, NO ROLE. Unchanged at HEAD.

surface: ecosystem/routing-table.yaml (the AUTHORITATIVE role -> CLI table, Z-G3 A2)
  says: four roles only — producer (claude-code, bounded_alternate codex), reviewer
    (codex, gpt-5.6-terra), adversarial (sol), fan_out ([luna, haiku, gemini],
    mode retrieval-only).
  agy: ABSENT. Zero occurrences of `agy` or `antigravity` in the file.
  verdict: NOT ROUTED. And see FINDING A below — there is no `analysis` role row at all.

surface: ecosystem/substrate-registry.yaml
  says: substrates (local, interactive, cloud, codespace) with verbs and capability
    flags. Carries providers/models/roles NOWHERE by construction (:12-15 "WHAT THIS
    FILE IS NOT").
  agy: ABSENT, correctly. This surface structurally cannot carry an admission.
  verdict: NOT APPLICABLE — and its silence is not evidence either way.

surface: `~/.claude/ROUTING.md` in-repo counterpart
  resolution: the in-repo counterpart IS ecosystem/routing-table.yaml; L0 holds only a
    DERIVED copy (routing-table.yaml:54-59, l0_derived_copy). So the L0 leg is covered
    by the row above.
  L0 itself: `/root/.claude/ROUTING.md` DOES NOT EXIST on this cloud host — expected,
    since a cloud lane has no operator disk (substrate-registry cloud.operator_disk:
    false). Per Z-G4 / scripts/routing_agreement.py's own docstring, absence is a
    REPORTED GAP that warns, never a pass. I assert nothing about the operator's copy.
  verdict: L0 UNREADABLE FROM THIS SUBSTRATE — declared, not inferred.

surface: protocols/STANDING_RULINGS.md
  says: literally nothing. `grep -ci "agy\|antigravity"` = 0 across the whole file.
  verdict: SILENT. No ruling admits agy, and none refuses it either. The refusals that
    exist (2026-08-23, architect) are on MODEL ids — gemini-3.7-flash (fan-out, G1) and
    grok-4.6 (fan-out, G1+G2) — carried in provider-registry role_admission, not here.

--- FINDING A (the disagreement item 1 asks for, first of two) ------------------
THERE IS NO `analysis` ROLE IN THE AUTHORITATIVE ROUTING TABLE. The question "is agy
admitted for the ANALYSIS role" presumes a role that ecosystem/routing-table.yaml does
not define. "analysis" exists in the corpus only as vocabulary: provider-registry.yaml:85
calls copilot-enterprise "a reviewer / adversarial / analysis provider" in a COMMENT;
the frozen A4-AGY bundle and the NB2 lane-O packet compute an "(agy, analysis)" cell.
`grep -i "analysis role"` across protocols/*.md returns ZERO.
Consequence, stated plainly: admitting agy "for the analysis role" is not one act but
TWO — (i) create the role row in the authoritative table, (ii) route a CLI to it. The
schema also constrains (ii): ecosystem/schema/provider_registry.py puts `roles:` and
`role_admission:` on MODEL rows, not provider rows, so an admission would attach to a
served model id — and see FINDING C.

--- FINDING B (the second disagreement, and it is live) ------------------------
routing-table.yaml routes `gemini` for fan_out while provider-registry.yaml declares the
gemini CLI RETIRED for this fleet.
  provider-registry.yaml:155-163 — "RETIRED BY OPERATOR RULING (2026-08-26, provider
  surface v2) ... `UNSUPPORTED_CLIENT` is the SERVER refusing this CLIENT ... `agy` is
  the channel to Google models".
  routing-table.yaml:43-44 — `fan_out: cli: [luna, haiku, gemini]`.
  Dates: the retirement ruling is 2026-08-26; routing-table.yaml was CREATED 2026-08-28
  at 09fd7a0 ([#613]), i.e. TWO DAYS AFTER the retirement, and shipped the retired CLI in
  a live role list.
This is not a stale-file story; it is a new file that did not inherit a two-day-old
ruling. It is also the exact drift `check_routing_agreement` cannot catch by design —
that organ compares in-repo vs L0 for AGREEMENT, and explicitly disclaims correctness
("Detection, not adjudication"). Two copies can agree on a dead CLI.
Not repaired by this lane: read-only by contract, and a routing row is an operator
surface. Reported as the finding item 1 asks for.

--- FINDING C (recorded, lower weight) -----------------------------------------
The model agy actually served for the analysis-role acceptance — `gemini-3.1-pro-high`,
70/70 `Resolving model` lines, NB2 lane-O packet §2 — is NOT a row in
provider-registry.yaml `models:`. It appears only inside the antigravity row's SERVED
comment (:209). The registry's own header calls itself "the declared source of truth for
every provider, CLI and model string the repo's LIVE surface names". Honest bound: an id
named only in immutable audits may be out of that scope, so I report this as a candidate
observation, not a violation. It becomes a real gap the moment an analysis admission is
written, because a `role_admission:` record must hang on a model row that exists.

================================================================================
2. WHAT ADMITTING agy FOR ANALYSIS WOULD ACTUALLY UNBLOCK
================================================================================
PREMISE I COULD NOT RESOLVE, reported rather than repaired (contract Q10):
the contract cites "the batch brief routes 'whole-repo analysis -> agy when admitted'".
That brief is NOT IN THE TREE. `grep -rn "when admitted\|whole-repo analysis"` over the
whole repo returns ZERO hits, and there is no docs/audits/ artifact for batch-e or dated
2026-08-31. It is operator-side and a cloud lane cannot see it. I therefore report on the
IN-TREE consumers that match its description, and I do not reconstruct the brief.

The would-be consumer, named in tree: a whole-repo coherence/orphan scan. The live
instrument of that class is docs/audits/2026-08-29-census-nb2-funnel.md (FM-C, "FULL
FUNNEL CENSUS"), which produced the 11-orphan set, the 8 false orphans a filename-only
census would emit, and the four-directory consumption classification.

What each alternative route costs, measured, not estimated:

route: CC (Claude Code) on a CLOUD lane — THE INCUMBENT, ALREADY PROVEN
  evidence: FM-C ran exactly this way — substrate cloud, revision origin/main @ fcc94855,
    zero writes, full four-directory coverage, and it caught its own four premise defects
    before executing. Cost is a Claude session on the operator's existing subscription;
    no per-call price, no new admission act, no new role row.
  limits it carries: shallow clone (`.git/shallow`, history starts 2026-08-23), so git
    birth dates are fiction on that substrate; no gate can run there (substrate-registry
    cloud.admits_gate_dependent_work: false).
  net: the scan is ALREADY SERVICEABLE on this route. Admitting agy does not unblock a
    blocked scan — it would provide a SECOND, cross-vendor instrument.

route: agy (gemini-3.1-pro-high) — WHAT THE MEASUREMENT ACTUALLY SHOWS
  evidence: NB2 lane-O packet, 2026-08-29, 10-item analysis-role pack at head 77096131.
    Computed gates cell (agy, analysis): F0 SUBSTITUTION PASS (70/70). F1 FABRICATION
    FAIL, F2 LOCATOR FAIL, N2 CROSS-CHECK FAIL on the bound item, N5 HONESTY FAIL, N6
    FAIL. N3 RESTRAINT PASS (2/2 controls held), N4 SELF-KILL PASS (2/2 planted false
    positives killed). Depth 4/6 = 0.67, printed UNCALIBRATED.
  the item that matters most here: N-01 was THE WHOLE-REPO SCAN ITEM, and it NOT-MET on
    BOTH draws — every finding cited `~/.gemini/antigravity-cli/scratch/repo`, i.e. a
    DIFFERENT REPOSITORY. Zero findings about .dev-knowledge. The packet is scrupulous
    that this is scope failure, not invention ("agy did not fabricate anything in this
    pack"), but for the coherence/orphan use case the distinction does not help: the one
    item shaped like this batch's would-be consumer produced nothing usable, twice.
  cost shape: 1,921,786 tokens over the scored pack; per item 60,842–603,188 input;
    N-04 alone was 34% of the pack and 9.8x the cheapest. Wall time 97s–969s per item.
    `$` deliberately NOT computed — agy runs on the operator's Google SUBSCRIPTION and
    SDA-1 C-8 forbids dividing a subscription into a per-call price.
  operational cost the packet records as owed: agy --print soft-denies every filesystem
    tool by default (deviation D-1, owner OPERATOR, ruling owed) — the pack could not run
    without --dangerously-skip-permissions; and agy "trusts all of C:\Users\1028120",
    i.e. it wanders into the primary checkout and siblings, which is precisely how N-01
    ended up scanning another repo.
  net: admitting agy for this scan would buy a cross-vendor second instrument whose ONLY
    measured attempt at this exact task failed on scope, twice, and whose token draw is
    ~1.9M for ten items.

route: the fan_out lane (luna, haiku, gemini) — RULED OUT BY DOCTRINE, not by cost
  evidence: routing-table.yaml:45-52, mode retrieval-only, with the scar recorded: "A
    fan-out head asked to COUNT returned a fabricated count ... a fabricated count is
    worse than a refusal because it reads as evidence. Widening this mode is an operator
    act with its own ruling."
  A coherence/orphan census IS a counting-and-classifying task. This route is closed for
  it by ruling, and `gemini` in that list is additionally dead at the server (FINDING B).

route: codex / terra as reviewer — NOT A PRODUCER OF THIS ARTIFACT, and it was down
  evidence: NB2 lane-O §5a — `codex exec` returned "You've hit your usage limit ... try
  again at 4:20 PM" on 2026-08-29; that lane's diff is recorded UNREVIEWED. Also observed:
  the session launched as gpt-5.6-sol while routing-table pins reviewer to gpt-5.6-terra.

route: Anthropic API path — MEASURED DEAD for calibration purposes
  evidence: NB2 lane-O §2 — ANTHROPIC_API_KEY re-measured 2026-08-29: HTTP 400, "Your
  credit balance is too low", request_id req_011CeWnLW9y4qixTcbaZuUdG. This is why every
  floor in the (agy, analysis) cell prints UNCALIBRATED: no in-window incumbent exists,
  and per SDA-1 B0 every comparative leg drops.

Bottom line for item 2: admitting agy for analysis unblocks NOTHING that is currently
blocked — the scan runs today on a CC cloud lane. What it would buy is heterogeneity (a
second vendor over the same corpus), and the price of that, on the only measurement that
exists, is one FAIL on the very item class the batch wants plus a permissions/scope
posture that needs an operator ruling first.

================================================================================
3. `[#578]` — LIVE STATUS, READ FROM tasks/
================================================================================
File: tasks/578-the-earned-mitigated-rerun-one-slot-role-reminder.md
Frontmatter, verbatim: id "[#578]" · status: OPEN · priority P3 · size S ·
  theme "[E7] Tooling & evaluation" · story "[S19] Decide the undecided artifact/tool
  models". Rendered in BACKLOG.md:299.
So: OPEN — not deferred, not closed.

What it holds, and this matters for the admission question:
  - The 2026-08-23 architect verdict REFUSED both candidates (gemini-3.7-flash on G1;
    grok-4.6 on G1+G2) and closed [#562]. [#578] exists because a closed row cannot carry
    an obligation.
  - It carries exactly ONE earned rerun, on R3's promptable-failure clause. "A mitigation
    is not a gate discharge: admission stays REFUSED until this rerun clears the floor."
  - It is itself BLOCKED-ON a real gate: intake 41
    (docs/intake/2026-08-23-tech-nopack-guard-refusal-surface.md) must be triaged first,
    "a guard whose refusal surface still reaches a scored item makes the rerun measure the
    instrument, and the slot is one, not many."
  - Its carried P/Phi/R baseline is declared STALE (unguarded head d2dc2fa6, 2026-08-20).
  - Its second half — whether the INCUMBENT's own refusal failure is promptable — is
    still UNMEASURED, and the row says outright: "until it exists, no ruling touching the
    fan-out pin should be made from this evidence."
Adjacent, checked so it is not assumed: [#491] (the Gemini scanning lane / ruling R-G) is
DEFERRED as of 2026-08-22 and, per JOURNAL 2026-08-31 (a), was found to be deferred AND
to carry no corpus scope at all. [#492] is annotated "superseded for this purpose" and
left deferred. Neither is a live path to an agy admission.

Net: the rerun question the antigravity row defers to is OPEN, blocked on an untriaged
intake, and holds one slot. Nothing in tasks/ authorizes an admission act today.

================================================================================
4. THE QUOTA CURVE — where agy/Gemini burn becomes VISIBLE
================================================================================
PROVENANCE DISCIPLINE FIRST. Two classes below, never mixed:
  [NET]  = read over the network in this session.
  [TREE] = read from this repository at HEAD.
And the honest gap, stated before the answer:

FETCH RESULT — PARTIAL FAILURE, DECLARED.
  BLOCKED by this session's egress proxy (403 CONNECT / EGRESS_BLOCKED), both curl and
  WebFetch: antigravity.google (the vendor's own docs — /docs/cli/credits/, /docs/plans/),
  support.google.com (Google One help), realpython.com, ooo.run.
  So I NEVER READ GOOGLE'S OWN DOCUMENTATION PAGE. What I have from those pages is
  search-engine snippet text quoting them, plus GitHub issues I could fetch directly. I
  mark each accordingly. I am not printing a URL as if I had opened it.
  REACHABLE and actually fetched: github.com issue pages, and web search results.

--- 4a. The surfaces, best evidence first --------------------------------------

SURFACE 1 — the agy CLI itself, INTERACTIVE ONLY. [NET, mixed strength]
  what: the right side of the CLI statusline shows a remaining credit count (e.g.
    "AI Credits: 42") and highlights when the balance drops below a warning threshold;
    a `/credits` slash command opens a dedicated credits panel with detailed usage stats.
  strength: MEDIUM. This is search-snippet text quoting antigravity.google/docs/cli/credits/
    and /docs/cli/commands/credits/ — pages the proxy would not let me open. A secondary
    source also dates `/credits` to CLI v1.0.12.
  THE CATCH, and it is decisive for this fleet: [NET, STRONG — fetched directly]
    antigravity-cli issue #234 records a user running `agy -p '/usage'`, `agy -p '/quota'`
    and `agy -p '/credits'` and getting them "interpreted as ordinary agent tasks rather
    than direct quota queries", with an explicit request for "a direct non-agent CLI
    command for usage/quota" because none exists. Issue #46 separately reports "/stats
    does not work in AGY and so cannot see the usage or the remaining quota available".
    This repo runs agy in EXACTLY that mode — `agy --print`, headless, per the NB2 lane-O
    contract [TREE]. So the one in-CLI surface that works is the interactive TUI, which no
    lane here uses.

SURFACE 2 — the 429, which is the only quota signal a HEADLESS lane gets. [NET, STRONG]
  fetched from antigravity-cli issue #234, verbatim:
    "RESOURCE_EXHAUSTED (code 429): Individual quota reached. Contact your administrator
     to enable overages. Resets in 167h39m40s."
  This is operationally the most useful fact in this section: for a batch lane, agy quota
  is invisible until it is exhausted, and then it is visible as an error string that
  carries its own reset countdown (~167h, i.e. roughly one week, in that report).

SURFACE 3 — the Google One AI-credits activity page. [NET, MEDIUM]
  what: a Google One "AI credits activity page" shows the remaining balance and usage
    detail; credits are shared with a Google One family group (total usage visible to the
    group, not individual activity). Search results surfaced the URLs one.google.com/ai/credits
    and one.google.com/ai/activity.
  strength: MEDIUM and I want the caveat on the record — support.google.com is proxy-
    blocked, so the description is snippet text, and I could not open one.google.com
    either (it is sign-in gated in any case). Treat the URL as a lead to verify from the
    operator's own browser, not as a resolved locator.
  also snippet-level, so LOW-MEDIUM: post-I/O-2026 reporting describes AI Pro moving to a
    compute-based credit system with five-hour usage windows applying across Gemini, Flow
    AND Antigravity; and that subscription plans no longer bundle free AI credits. If the
    quota curve matters to planning, this is the fact to verify first, because it changes
    the shape (rolling 5h windows + weekly individual cap) rather than the number.

SURFACE 4 — programmatic read: NONE KNOWN. [NET, STRONG — fetched directly]
  CodexBar issue #1178 (a third-party status-bar tool trying to add agy support) states:
  "I do not know yet whether Antigravity CLI exposes a local usage endpoint, a config/cache
  file, or an API suitable for CodexBar integration", and proposes inspecting where the CLI
  stores auth/session and usage metadata as a FIRST STEP. As of that issue, no local
  endpoint, cache file or API is documented. So there is no scriptable quota source to
  point a hub organ at today.

SURFACE 5 — the Gemini API / AI Studio path: PRESENT BUT OUT OF BOUNDS HERE. [NET+TREE]
  [NET] Gemini API usage is visible in Google AI Studio under Dashboard > Usage, with
  billing documented at ai.google.dev/gemini-api/docs/billing.
  [TREE] This route is CLOSED for this fleet: provider-registry.yaml:161-163 records that
  the only documented way past the gemini CLI's server refusal "is an API key the standing
  auth ruling forbids", and agy runs on the operator's OAuth subscription. Naming AI
  Studio as "where you see agy burn" would be wrong: it meters the API-key path this fleet
  does not use.

--- 4b. What the HUB already records, independent of the network [TREE] ---------
  - agy's rate shape is declared SUBSCRIPTION, and dividing it into a per-call price is
    forbidden: NB2 lane-O §2.1 tags the cell `subscription` and cites SDA-1 C-8; the
    SDA-1 adversarial review (2026-08-28) puts agy's cost column at "gates + $" and warns
    agy "may be structurally unable to reach ADMIT" because its envelope is untrusted.
  - The one real consumption record the hub holds is a TOKEN DISTRIBUTION, hand-recorded
    per item in NB2 lane-O §2.1: 1,921,786 tokens over 10 items, N-04 at 660,124 alone.
    That is the closest thing to a quota curve in this repository, and it is an immutable
    audit table, not a live surface.
  - The served-model attestation path is a VENDOR LOG, not an API: `~/.gemini/antigravity-
    cli/log/cli-<date>_<time>.log`, one file per invocation; agy's JSON envelope carries no
    model field and its `status` field is known to report ERROR while carrying a complete
    answer (provider-registry.yaml:200-206; lane-O contract). If a quota reader is ever
    built, that log directory — not the envelope — is where it would have to look.
  - Precedent for how this fleet records billing visibility: provider-registry.yaml:99-103,
    landed 86bed82 (2026-08-29), for copilot-enterprise — "consumption is metered to the
    ENTERPRISE ORG SEAT ... and is visible ONLY on that org's Copilot billing page, which
    needs `admin:org`. A zero on the user premium-requests meter is CORRECT and is not a
    routing defect ... NO FURTHER PROBING from our side." It is a COMMENT, not a field.
  - The generic telemetry answer is not available: logs/TELEMETRY.db has no consumer and no
    query ([#575] store perf + silent drops, [#576] read path — both OPEN per the AUT-R4a
    audit), and ecosystem/trends.html is gitignored with "per-model quality" listed as an
    ABSENT series because no store exists.

--- 4c. THE ANSWER, in one paragraph ------------------------------------------
For an INTERACTIVE agy session the burn is visible in the CLI itself — statusline credit
counter, `/credits` panel [NET, snippet-strength]. For the way THIS fleet uses agy
(`agy --print`, headless), there is NO usage surface at all: the slash commands degrade
into agent prompts, no local endpoint or cache file is documented, and the first visible
signal is a 429 "Individual quota reached ... Resets in 167h39m40s" [NET, strong]. The
account-level surface is the Google One AI-credits activity page (one.google.com/ai/...)
[NET, medium, unverified — proxy-blocked, sign-in gated]. Google AI Studio's usage
dashboard meters the API-key path this fleet is forbidden to use, so it is the wrong
surface here [TREE]. Inside the repo, the only consumption record is the hand-authored
per-item token table in the lane-O packet, and the only machine-readable per-invocation
evidence is the vendor's own `~/.gemini/antigravity-cli/log/cli-*.log` [TREE].

================================================================================
5. DRAFTED `quota-source` FIELD SPEC — reconciled against the correction
================================================================================
RECONCILIATION FIRST, because the correction is binding on what may be proposed.
docs/audits/2026-08-30-technical-autonomy-decision-tree.md:120-128 carries "The
'quota-source field'" under CORRECTIONS TO THE RECORD. Its source is AUT-R4a
(2026-08-29-technical-aut-r4a-harness-evals-observability.md:364-372, :757):
  "INCUMBENT D — 'the quota-source field' -> UNLOCATABLE AS A FIELD ... searched `quota`,
   `quota_source`, `quota-source` across *.py *.md *.yaml *.json (repo-wide) ... Hits are
   PROSE ONLY ... NO quota field ... Flagged for the operator to name what he meant."
I RE-RAN that search at HEAD and confirm it: `quota-source` appears in FOUR places, all of
them audit prose ABOUT its own non-existence (the R4 dispatch record, the R4a brief, the
R4a report, the synthesis, the decision tree). Zero code, zero YAML, zero schema.
So the correction stands at HEAD: THERE IS NO SUCH FIELD AND NEVER WAS. Anything below is
a BIRTH proposal, not a repair — and per ADR-111 / Z-G1 it is a CANDIDATE, which this lane
may draft and may not file.

WHICH REGISTRY SHOULD CARRY IT: ecosystem/provider-registry.yaml, on the PROVIDER row.
  why not substrate-registry.yaml — it declares dispatch substrates and disclaims doctrine
    and provider facts (:12-15). Quota is a vendor-account fact, not a transport fact.
  why not routing-table.yaml — Z-G3 scopes it to WHICH ROLE RUNS ON WHICH CLI and it
    explicitly does not rule on model tiers. A quota locator is not a routing fact.
  why not the MODEL row — quota on every plan surveyed is metered per ACCOUNT/PLAN
    (Google One credits; the copilot org seat), not per model id.
  why provider-registry — it already IS the home of exactly this content, in comment form:
    the copilot-enterprise billing note (:99-103) and the google/antigravity "NO
    changelog_tool_key" notes are quota/billing-visibility facts living as prose because
    the schema refused them.

THE HARD CONSTRAINT ANY PROPOSAL MUST CLEAR, and it is why this is a real act:
  ecosystem/schema/provider_registry.py sets `extra="forbid"` on the contract base. A new
  YAML key is a BLOCKED COMMIT until the pydantic model declares it. That is deliberate
  ("Forbidding extras converts a typo into a blocked commit and makes 'add a field
  deliberately' a real act with a real diff"). It also carries the base validator that
  refuses blank / untrimmed strings, and `_lookup_keys_are_lowercase` for lookup keys.
  PRECEDENT AGAINST, stated because it is the strongest counter-argument and it is only
  two days old: on 2026-08-29 (86bed82) a RICH copilot-enterprise entry was REFUSED by
  this same schema and the content went to a comment plus L0 ~/.claude/ROUTING.md, with
  the commit message recording "the registry is a provider/CLI identity surface". A
  `quota_source` field cuts against that ruling-in-practice. The operator/architect should
  settle that before anything lands.

DRAFT SPEC (name in snake_case to match every existing schema field; the prose name
"quota-source" is kept only as the human label):

  YAML shape, on providers.<id>:
    quota_source:
      surface: <free string — what the operator opens or runs>
      kind: <closed enum: cli-interactive | web-console | error-signal | vendor-log | none>
      locator: <URL, menu path, command, or repo-relative/absolute path>
      requires: <optional — the access needed, e.g. "google account sign-in",
                 "admin:org", "interactive TTY">
      measured_on: <date — when a human last SAW this surface work>
      note: <optional one-line honest limit>

  Cardinality: a LIST of such records per provider, because the measured reality is that
  one provider has several partial surfaces and no single one answers the question. A
  single-valued field would force a false choice and hide the headless gap.

  Pydantic addition (ecosystem/schema/provider_registry.py):
    QuotaKind = Literal["cli-interactive","web-console","error-signal","vendor-log","none"]
    class QuotaSource(_Contract):
        surface: StrictStr
        kind: QuotaKind
        locator: StrictStr
        requires: Optional[StrictStr] = None
        measured_on: Optional[datetime.date] = None
        note: Optional[StrictStr] = None
    Provider gains:  quota_source: tuple[QuotaSource, ...] = ()
    SCHEMA_VERSION bumps 1.0.0 -> 1.1.0 (additive, optional, no existing row invalidated).

  Rules the spec must state, each earned from something measured this lane:
    R1 — OPTIONAL, defaulting to empty, exactly as `role_admission` is. An absent
         quota_source means "nobody has measured this", never "unmetered". Mirrors the
         schema's own `unevaluated` posture.
    R2 — `kind: none` is a FIRST-CLASS VALUE and must be usable. agy headless is precisely
         that: CodexBar #1178 establishes no programmatic surface exists, and recording
         "none, measured on <date>" is a fact, not a gap.
    R3 — NO SCHEMA-SIDE URL EXISTENCE CHECK, and no network from Layer 2 (ADR-28/36). The
         schema validates SHAPE only, the way RoleAdmission.evidence does; if existence is
         ever asserted it belongs in scripts/check_provider_registry.py, not here.
    R4 — `measured_on` is a HUMAN OBSERVATION stamp, on the same footing as
         `last_reviewed_version` in tool-versions.yaml: it means someone opened the surface
         and saw it work. A stamp is never written from documentation alone. This lane
         could not open antigravity.google or support.google.com, so on the evidence I
         hold, the antigravity row's web-console entry would land WITHOUT a measured_on.
    R5 — the field records WHERE TO LOOK. It never records a BALANCE or a THRESHOLD — a
         number typed into a doc is stale at the next commit (CLAUDE.md §4 M2).

  What the antigravity row would carry, on THIS lane's evidence, if the field existed
  (illustrative — nothing was written):
    quota_source:
      - surface: "agy statusline credit counter + /credits panel"
        kind: cli-interactive
        locator: "/credits (interactive TTY only)"
        requires: "interactive TTY — NOT available under `agy --print`"
        note: "vendor docs unread (antigravity.google proxy-blocked 2026-08-31); issues
               #46/#234 record /usage,/quota,/credits degrading to agent prompts in -p mode"
      - surface: "RESOURCE_EXHAUSTED 429 with reset countdown"
        kind: error-signal
        locator: "stderr of the failing agy invocation"
        note: "the ONLY quota signal a headless lane receives; carries `Resets in <hh>m<ss>`"
      - surface: "Google One AI credits activity page"
        kind: web-console
        locator: "one.google.com/ai/activity   # UNVERIFIED — see note"
        requires: "Google account sign-in"
        note: "search-snippet strength only; support.google.com and antigravity.google were
               proxy-blocked this session. Operator to confirm from a browser before use."
      - surface: "per-invocation vendor log"
        kind: vendor-log
        locator: "~/.gemini/antigravity-cli/log/cli-<date>_<time>.log"
        note: "carries the served-model attestation, not a credit balance"

  THE ALTERNATIVE I AM OBLIGED TO PUT BESIDE IT: do NOT birth a field. Formalize the
  comment convention the copilot-enterprise note already established, and put the
  structured version in ~/.claude/ROUTING.md at L0 where the copilot capability/billing
  profile already lives. Cost: unqueryable, invisible to any hub check, and it repeats the
  present-but-unread failure mode. Benefit: consistent with a two-day-old refusal and adds
  no schema surface. This is a functional question (what the operator needs to see), so by
  ADR-108 §A it is the OPERATOR's to rule, not the architect's — and not this lane's.

================================================================================
6. LANE CLOSE
================================================================================
Write-scope honoured in full: ZERO files written, ZERO tree writes, ZERO commits, ZERO
branches, ZERO rows born, ZERO registry edits, ZERO pushes. Nothing was admitted, refused,
or re-opened — the (agy, analysis) admission question stands exactly where HEAD left it,
deferred to [#578], which is OPEN and itself blocked on intake 41. No hook fired and no
closure proposal was accepted; had one been offered I would have declined it, this lane
being read-only by contract.
Escalations under the V-2 budget: NONE of classes (a) curated-baseline, (b) rule-vs-ruling
conflict, or (c) an unruled fork was hit. FINDING B (routing-table routes a retired CLI)
is a defect in a surface, not a rule conflict, and is reported rather than repaired.
One refuted premise reported, not repaired: the batch brief this contract cites is not in
the tree and a cloud lane cannot see it; item 2 was answered against in-tree consumers and
says so.
One declared network gap: the vendor's own documentation (antigravity.google) and Google's
help pages were blocked by the egress proxy. Every network claim above is tagged with its
strength and its actual source. No URL is presented as read that was not read.

Sources (network reads this session):
- https://github.com/google-antigravity/antigravity-cli/issues/234 (fetched)
- https://github.com/google-antigravity/antigravity-cli/issues/46 (fetched)
- https://github.com/steipete/CodexBar/issues/1178 (fetched)
- https://antigravity.google/docs/cli/credits/ (BLOCKED — snippet only)
- https://antigravity.google/docs/cli/commands/credits/ (BLOCKED — snippet only)
- https://antigravity.google/docs/plans/ (BLOCKED — snippet only)
- https://support.google.com/googleone/answer/16287445 (BLOCKED — snippet only)
- https://one.google.com/ai/activity (surfaced by search; NOT opened)
- https://ai.google.dev/gemini-api/docs/billing (surfaced by search; NOT opened)
```