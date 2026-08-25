# REGISTER RULING PACKET — 37 rows adjudicated (architect, 2026-08-25)

**Inputs:** `VERIFIED-REGISTER-REPORT.md` (five lanes, 37/37 coverage, verdicts verbatim) over the
landed register + addendum. **This packet is the batch ruling** — ADR-111 funnel applies: ADOPT →
carrier, INTAKE → intake, REJECT → reason recorded, COVERED → cite. Row births spend the births
D38 banks; **nothing lands until D38-FINAL is confirmed.**

## 0. Errors owned first — mine, caught by the lanes

| # | My claim | Measured truth | Consequence |
|---|---|---|---|
| E13 | addendum: #34's artifact in-repo "since 2026-08-10, six days before" | `git log --diff-filter=A`: **2026-08-13**, three days (CONTRA-1) | substance holds; my date was carried, not measured |
| E14 | addendum sequencing note: "four contention incidents, fourth corrupted a measurement" | count exists **only in an off-repo Downloads digest**; in-repo: 2 witnessed HEAD-swaps + 3 coexisting executions (CONTRA-2) | C17 evidence downgraded; the NEED survives on in-repo incidents + the live LAND-vs-SWEEP near-miss this window |
| E15 | addendum carrier shorthand `intake-4` / `intake-5` | real ids: **45** (substrate router) and path-located contract-integrity intake (CONTRA-11) | packet below cites resolvable ids/paths only |
| E16 | HARVEST-V brief: "17 measured-here rows" | grep on `origin/main`: **14** | the brief's number was mine and wrong; all 14 discharged |

Same class as E1–E12: a carried fact where a measured one was available. The fix is already in the
pipeline (contract-integrity: a contract names the command, never the fact) — these four are its
freshest evidence.

## 1. Cross-cutting adjudications (CONTRA items that are mine to rule)

1. **CONTRA-6 — one vocabulary for the substrate axis.** The **gated enum wins as the surface**:
   `SHAPE_ENUM = ("local","cloud","interactive")` at `gen_lane_contract.py:104` is live and
   hook-enforced. My A1 three-substrate vocabulary is DESCRIPTIVE until intake **45**'s ADR extends
   the enum **in one act** (generator + hook + table together). No parallel vocabulary lands.
2. **CONTRA-9 — the three baseline numbers are three moments, not a contradiction.** 441 =
   pre-R12 · 445 = probe branch pre-merge · **443 = live** (`ecosystem/silent-rule-baseline.yaml:20-23`,
   `measured_at: 2026-08-24`, detector v5). Adjudicated; C14 adoption scopes against **443/v5**.
3. **CONTRA-10 — the "R13" label collision.** My normative-home definition enters the register as a
   **content-named section** (e.g. "Silent-rule detector — the normative-home test"), never as
   bare "R13". D38's E8a covers R12 only; **the definition section is added to ARC-F below.**
4. **CONTRA-12 — carrier correction:** code-style doctrine = intake **31, ACCEPTED**;
   architecture-enforcement = intake **34, DRAFT**. ARC-A uses both, correctly.
5. **CONTRA-1 — V3's git-measured date governs.** Substance (C23 unblocked) unchanged.
6. **U-1 / A-5 — accepted as a defect of mine to repair:** three window-rulings
   (sentinel-on-tip, regenerate-never-pick, measure-once/N-dependent) bind in practice but have no
   register entry. **They get entries in ARC-F.** A rule that binds owes a locator.

## 2. Immediate repo self-contradictions — two paste-sized fixes, first wave

- **FIX-1 (CENSUS-1, A-3): `/lane-boot:132-133` vs P-1.** Ruled: **P-1 stands; `/lane-boot` is
  scope-corrected** — the journal instruction applies to an ARC (PLAYBOOK Ch8 law), never to a
  batch LANE; the command gains the lane/arc branch explicitly. P-1's own provenance (the N4
  breach) decides it.
- **FIX-2 (CENSUS-2): `handoff-verify.md:73`** bare `python` → `uv run --locked python` (the last
  bare invocation across all 11 capability files; CLAUDE.md:71 rules it a defect).

## 3. The rulings — 37 rows into ten arcs

### ARC-A · Code doctrine & FDD — **P1** (operator's named goal) · local
**C22 ADOPT + C23 ADOPT, merged into one arc.** Evidence: `extend-select = []`, no mypy table, no
architecture contract beyond a fixture. Path: execute intake **31 (ACCEPTED)** + ratify intake
**34 (DRAFT)** into ONE code-doctrine ADR: functional-first style, ruff rule selection, complexity
ceilings, import-linter contract, mypy decision. The #34 artifact is in-repo and unblocked. **This
is the FDD vehicle** — one ADR, then mechanized by the gates it names.

### ARC-B · State-as-data: id allocation + SOLE source — **P1** · local
**C08 ADOPT (the missing "SOLE") + C09 ADOPT, one carrier.** The 777-vs-577 double-bite is
measured (`JOURNAL.md:1719`); ADR-107:463 names the hole itself. Deliver: an allocation mechanism
(ADR-107's `max+1` made atomic, or content-hash per C09's option — the row's ADR fork, decided in
its spec) + manifest ceases to be hand-edited for membership. Protects every future parallel batch.

### ARC-C · Operator visibility: vitals + digest + readiness — **P1** · local, feeds Codespace later
**C10 ADOPT + C11 ADOPT + C13 ADOPT, one carrier ("backlog vitals").** Three instruments
(age-of-open, aging outliers, throughput-per-window vs the R2-ruled denominator) + the committed
digest (ledger line, next-5, flow vitals, since-last-window) + what-is-unblocked-now from the
existing `depends-on`. C10's downgrade to practitioner changes the EVIDENCE label, not the
priority — the practitioner is the operator, and this is his most-repeated ask. **The pending
telemetry research (DORA/attribution) feeds v2 of this arc; v1 does not wait for it.**

### ARC-D · Substrate router — **P1** (efficiency) · local build, cloud beneficiary
**Operator mandate (2026-08-25, binding input for the router ADR):** batches shrink to 4–6 lanes
and the DEFAULT execution substrate is GitHub compute — gate-dependent lanes route to the
Codespaces devcontainer (gates armed, suite ~4× faster), read-only fan-out to Dispatch-CloudV2
containers (gates NOT armed — never gate-dependent work), local reserved for operator-gated acts
(merges, pushes) and vendor-CLI-on-operator-disk work. Sequential-local as a default is retired. **Second criterion (operator, 2026-08-25):
provider-agnosticism** — GitHub compute is the only substrate where non-Anthropic producers
(Codex, Copilot agent, Gemini, future DSH) can execute against the same armed gates; routing
toward it is therefore a universalization act, not just a speed one. Local and CC-cloud bind
execution to one vendor and become: operator-gated acts + vendor-CLI-on-disk (local), and
read-only fan-out (CC-cloud). **Open learning the router intake must carry:** the cost/time/loop
column per substrate — time is measured (commit ~7× cheaper, suite ~4× faster on Codespace),
cost and feedback-loop latency are NOT (Codespaces billing/quota to be verified, not assumed) —
the ADR routes on measured numbers only.
**Prior-art note (third owned-unconsumed incident, measured 2026-08-25):**
`docs/archive/2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md` already carried a
per-tool AGENTS.md matrix, unremembered when R-L was commissioned — cited as corroborating prior
art in intake #42; the incident itself is ARC-C's digest argument (unconsumed-findings count).
**C30 ADOPT via intake 45 (READY) + C32 ADOPT (doctrine line) + C31 ADOPT (generator).**
Per CONTRA-6 ruling: one ADR extends the gated enum, lands the capability-keyed table
(`reviewer_cli` / `full_history` / `operator_approval` / `inputs_on_operator_disk` — today zero
hits repo-wide), and `gen_lane_contract` derives substrate + command from it. C32's two-leg
reviewer reason (binary absent AND auth absent) moves from immutable audit prose into the table —
closing the "someone adds an install line" hole. C31: the capability file generated from **three**
sources (module exports + PATH scripts + `.claude/commands|skills`) and carried into the bundle.

### ARC-E · Gate integrity — **P1/P2** · local
**C17 ADOPT** (serialize integration by mechanism — extend `single_flight` to the integrator;
new row, `[#530]` is closed and cannot carry it per A-6). Evidence rests on the two registered
HEAD-swaps + this window's live near-miss; the "four incidents" phrasing is retired with E14.
**C18 ADOPT** (extend `fire_test` to the 21 local pre-commit gates + the substrate-inertness
class — A-1's five-way re-witness is the motivation written by the lanes themselves).
**C19 COVERED** by the contract-integrity intake (READY) — execute, don't re-adopt.

### ARC-F · Rulings as records — **P2** · local
**C24 ADOPT-scoped:** extend the `landed:` predicate block with `status` / `supersedes` /
`enforced_by`. **C29 ADOPT-cheap:** one register section shaping transcript→proposal (verbatim
quotes + L6's zero-diff extraction as the proven method + operator approval mandatory).
**Register repairs from this packet:** entries for the three unregistered binding rulings (U-1),
the normative-home definition section (CONTRA-10), and R12's entry if D38's E8a did not land.
**C25 REJECT-for-now, reason recorded:** a path-keyed hard gate on governed-doc edits is
disproportionate before C24 makes rulings recordable; F5 + the register already carry the
discipline. Revisit after C24.

### ARC-G · Progressive disclosure & skills — **P2** · local
**C02 ADOPT-scoped** (headroom is 5, not 2-3 — keep extracting procedure; §6/§9 named).
**C03 ADOPT-phased:** chapter→skill split starting with the highest-invocation chapters; the two
existing skills prove the shape. **C05 ADOPT-cheap, P3:** split the universal-glob rule file when
a second rule arrives. **C04 COVERED-BY the normative-home definition** + one doctrine sentence:
prose a gate READS is a fixture and stays; prose a gate merely ENFORCES is deletable
(CLAUDE.md:232's hook roster is the canonical example of the first class).

### ARC-H · Register & lifecycle hygiene — **P2** · local
**C20 ADOPT:** leg 2 lands with intake #44's implementation (pin what+as-of, loud expiry — bans
the volatile matcher class by schema); leg 1 extends `preflight_backlog_ids` to disposition refs.
**C26 ADOPT-narrow:** record §5 as ratified in place + arm its two invariants as a check member
(U-6 closes). **C28 ADOPT Class A only:** the 47 mechanical normalizations execute under the live
validator; **Classes B/C/D stay BLOCKED and their trigger defect is ruled**: ADR-94's ratification
trigger ("`Proposed` corpus-wide") is unmeetable-by-construction — same defect class as
`[#356]`/`[#577]` — and gets a one-line trigger amendment in the same act. **C27 COVERED** —
decided this window; the one predicted HAVE landed as predicted.
**H-plus (operator-priority 2026-08-25): JOURNAL rotation.** The append-only JOURNAL has grown
into a measurable performance tax (slow greps, slow spine hooks, heavy context). NOT a research —
log rotation is solved prior art (library-first). Row spec: split into a small LIVE file (current
period; the spine/anchoring predicate and block-unanchored-push keep reading THIS file only) +
dated archives under docs/; universal across fleet repos; before/after timing measured in the
closing artifact. Same diet applies as a pattern to any unbounded append-only surface the fleet
carries.

### ARC-I · Model governance — **P2/P3** · local
**PROBE-PROVIDERS consumption (measured 2026-08-25, report in Downloads → lands with wave 1):**
(1) **Registry repairs owed:** `xai` row is configured-as-absent but measured-live (`grok 1.0.5`
on PATH, self-updated alpha→stable mid-probe — dated-snapshot argument for C35); `google` row's
liveness claim is FALSE (server refuses free tier: IneligibleTierError; version claim still
true); **Antigravity (`agy` 1.1.16) is live, authenticated, first on PATH, serving
gemini-3.7-flash-{high,medium,low} AND claude-opus models — entirely unregistered**; Copilot CLI
present outside the six, noted; `deepcode` reads settings.json not DEEPSEEK_API_KEY (env var
likely dead). (2) **Operational: the admitted Gemini retrieval role (R-G) has NO working surface
today** — fan-out via Gemini CLI is dead until paid tier or migration; `agy` is the named
migration target and the natural rerun route for `[#578]`, but `agy` enters roles ONLY through
the R3 measured-acceptance gate. (3) **Poisoned-name rule CONFIRMED by measurement:** `agent.exe`
is byte-identical to `grok.exe` (same SHA256); Cursor's own install-verification command
(`agent --version`) false-positives to another vendor on this host; PATH order would shadow a
correct Cursor install. `agent` never appears in contracts, docs, or the registry; Cursor gets
no pin until an actual install is measured. (4) Small operator-queue items: dedupe the two
Claude installs (npm shim emits stderr noise every call).
**C33 ADOPT-cheap:** one doctrine line elevating cross-family review from practice to rule
(forbids same-family self-review in one session). **C35 ADOPT-scoped:** harden the registry —
dated snapshot ids, `effort` key, `-latest` prohibition; the drift job (diffing provider model
lists) is P3. **C36 ADOPT-narrow:** record DeepSeek's actual verdict basis in the registry (today:
configured-without-a-recorded-verdict; the row's ZDR reason vs the recorded "no verified id" gets
reconciled, not guessed). **Correction 2026-08-25 (operator-sourced, verified at
deepseek.com/harness):** DeepSeek now ships a FIRST-PARTY harness — DSH, developer preview, MIT,
`npx @deepseek-ai/dsh web`, Cordis plugin kernel, append-only session logs with a Trajectory
view. **PROBE-DSH executed 2026-08-25 (report in Downloads → lands with wave 1) — the probe's
three questions are ANSWERED, from shipped source (tarballs), runtime never observed:** config
root = `$DSH_HOME` else `~/.dsh` (NOT created — enters the operator workspace only after an
install creates it); **instruction files: DSH consumes BOTH `AGENTS.md` AND `CLAUDE.md`**
(candidates walked `.git`-root→cwd, `.local.md` overlays, 64 KiB batch budget) — so DSH is
NEUTRAL in the intake-#42 matrix (fails the "and not CLAUDE.md" leg, like Grok) and a
CLAUDE.md-only repo is fully consumed; auth = `DEEPSEEK_API_KEY`, resolver reads inherited env
FIRST — **correction to the providers-probe note: the env key is NOT dead, only unused by
`deepcode`; dsh would authenticate promptlessly on this machine.** Runtime verdict: NOT viable
today — `npx @latest` livelocked npm's resolver 46 min / 2688 s CPU / zero output; retry paths
recorded (pinned `@0.1.1-rc.2`, global install, `--prefer-offline`; `pnpm` absent blocks custom
profiles; orphaned npx lock dir needs clearing first). **Separate defect evidenced by this
probe's session:** end-of-session hooks attributed a CONCURRENT session's commits to the probe,
including a hard JOURNAL-anchor demand it rightly declined — fresh evidence for the
session-coordination gap (C17's neighborhood): hooks cannot tell sessions apart within one
checkout. R-J's "no first-party convention" is superseded. Consequences: (a) the C36 row gains a
bounded DSH probe — install, measure its config directory (no invented paths; the operator's
workspace root is added only after that measurement), check `AGENTS.md` consumption (R-L did not
cover DSH); (b) any DSH lane admission goes through the R3 measured-acceptance gate like every
new lane — preview status raises, not lowers, that bar; (c) its session-log/Trajectory design is
noted as prior art for the telemetry arc. **C34 REJECT-as-written, reason recorded:** it collides with ruling R3
(binding: floor + control item carry the gate) and presumes suspended verdicts that in fact stand
(`verdict: refused` with decider/date/evidence). The McNemar/paraphrase design is noted as
INTAKE-grade input to any future R3 amendment — by ruling, not by ignoring R3.

### ARC-J · Distribution & portability — **P3 / next-window research consumption**
**C37 ADOPT-phased:** the mechanism exists (manifest + carriers + plugin marketplace); the Copier
question, `[project.scripts]` CLI, and S/M/L tiers are **R-I's consumption**, decided when that
report's register rows are cut — not invented here.

### Decisions & rejections outside arcs
- **C01 — the AGENTS.md fork gets a DECISION CRITERION, and my lean is now conditional.** The
  operator's universalization mandate changes the weighing: ADR-53's rejection rested on "both
  tools read CLAUDE.md directly" — a premise that predates a six-provider fleet, and
  `codex/AGENTS.md` already exists as an L0 carrier. **Ruled: intake #42 is decided next window on
  a measured provider-consumption matrix** (which admitted providers natively read which
  instruction files). **If ≥2 admitted providers natively consume `AGENTS.md` and not `CLAUDE.md`
  → supersede ADR-53 D2 with C01's thin-file spec (≤120 lines, non-inferable facts, importer).
  Otherwise → retire R-1.** Criterion over lean; the matrix is a one-session measurement.
- **C06 REJECT (do not retire ESSENTIALS), reason = the row's own escape clause:** five code
  surfaces read it + §1 boot-read. The census was run and says keep. (Protocol note: the verdict
  lacked a quoted sentence — U-11 — but code-reader locators are stronger evidence than a quote
  here; accepted.)
- **C07 — half COVERED, half REJECT:** generated structural claims exist (codemap + freshness
  gate); the `pyreverse→Mermaid` proposal collides with the landed ADR-51 amendment that moved
  Mermaid OUT. The operator's "is ARCHITECTURE.md needed" resolves to: its generated half earns
  its place; its prose half falls under ARC-G's diet.
- **C12 → OPERATOR, with my recommendation attached:** adopt the icebox with a hard cap and
  one-in-one-out **after** D38's drop lands — momentum plus a visible number make the cap
  enforceable rather than aspirational. Your call, Rob; this one is genuinely yours.
- **C16 REJECT-as-written, reason corrected by V3:** required checks are ruled permanently
  unavailable (ADR-101:219, private repo on Free tier) — the obstacle is the tier, not the Actions
  budget. Revisit trigger: a tier change (operator decision, priced separately).
- **C21 COVERED** by `[#573]` (open; pre-commit scope stands — CI scope dies with C16's reason).

### ARC-D addendum · **D-vis — provider status surface (operator-priority within ARC-D)**
Symlinks are ruled OUT for this need: on Windows checkouts git materializes them as plain text
files (`core.symlinks=false` default) and creating real ones needs elevated rights — visibility
that silently breaks per-clone. **Ruled shape:** a GENERATED per-provider status block in the
already-landed Tier-1 section — CLI present? · auth alive? · root path as a clickable link ·
role verdict · last-verified date **with the probing command** — generated from
`provider-registry.yaml` + live probes, freshness-gated. Always current because a machine
re-derives it; loudly red when a provider disappears. Covers all six: Claude, Codex/OpenAI, Grok,
Gemini, DeepSeek, Cursor (Cursor + OpenAI entries added to the registry in the same act).

## 3b. Research slate (Advanced Research, browser-side; consumed via the register funnel)

| id | Topic | Feeds | Status |
|---|---|---|---|
| R-J | Delivery telemetry (DORA/SPACE) + AI code-attribution conventions, git-native | ARC-C v2, `Model:` trailers | operator-endorsed, launchable |
| R-K | Cross-model review effectiveness & self-preference bias | ARC-I C33 doctrine, reviewer routing table | proposed |
| R-L | `AGENTS.md` / instruction-file standard adoption across coding agents | the C01 / intake #42 decision matrix | proposed |

**Rejected with reasons:** code-doctrine research (owned in-repo since 2026-08-13 — #34; almost
re-commissioned, which is itself this window's lesson) · backlog-at-scale (R-D) · handoff (R-B) ·
skills (R-A) · evidence-provenance (our HAVE/PARTIAL/ABSENT+locator protocol is ahead of the
external literature, not behind it).

## 3c. The simplification criterion (VISION challenge, recorded)

The register measured the framework paying rent mostly to itself: 68% mechanism-without-doctrine,
consumer repos queue-only, zero consumer-repo work this window. **Ruled as the measurable
north-star of "compose and simplify": an S-tier instantiation of the framework in a foreign repo
via one command (R-I's smallest tier).** Document dieting (ARC-G) serves that test; it is not the
test. Next window's mandate includes ONE consumer-repo application arc — the framework closes a
row outside the hub or the simplification claim stays unproven.

## 4. Sequencing

1. **Confirm D38-FINAL** (closures bank the births this packet spends). Operator pushes `main`.
2. **First wave (one batch):** FIX-1 + FIX-2 · ARC-F register repairs · the C01 provider-matrix
   measurement · ARC-A ADR drafting. Small, high-leverage, mostly appends.
3. **Second wave:** ARC-B, ARC-C, ARC-D builds (parallel lanes, file-disjoint — D routes future
   waves' suites to the devcontainer).
4. **Third wave:** ARC-E, ARC-H, ARC-I remainder.
5. **Telemetry research consumption + ARC-J + intake #42 decision:** next window's mandate.

**Ledger discipline:** every ADOPT above lands as a row spec against banked births or an existing
carrier named here; INTAKE-grade items are already intakes (31/34/42/44/45 + contract-integrity);
REJECTs carry their reason in this packet, which lands in-repo with the wave.
