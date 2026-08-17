# DRAFT — consumer-side home for the hub handoff runbook (`[#293]` BLOCKED-ON-RULING)

<!-- scope: meta -->

> **Status: DRAFT — decision-support for an architect ruling. This report rules nothing,
> changes no path, and touches no consumer repo.** It reads the governing sources and three
> live consumer trees, derives candidate consumer-side homes from what those trees *already*
> contain, scores each against ADR-60's own stated rationale, and recommends one.
>
> **Read-only, and verifiably so:** the only files written by this lane are this report and
> the regenerated `docs/audits/README.md` index. Three consumer repos were read from
> throwaway clones (`/workspace/...`); no consumer branch, commit, PR, or comment was
> created, edited, or closed by this lane.

---

## 0. Scope, method, and the limits of this report

**Method.** Every path, rule, and quotation below was read live from disk at
`43cd1ce` (hub `main`) or from a read-only clone of the consumer named. Where a candidate
home is proposed, the **directory** is quoted from a live tree and the **filename** is
labelled as a proposal — no path in this report is asserted to exist unless it was read.

**Consumers read live (3 of 8).** ADR-104 declares the fleet as *"the hub `.dev-knowledge`
… plus `ai-council`, `corp-monorepo`, `corp-ops`, `corp-sca-time-automation`, `demo-prep`,
`life-architect`, `terminal-setup`, `win-tooling`"* (ADR-104 §Context). Of the eight
non-hub members, only three are reachable from this session:

| Consumer | Read live | HEAD read | Note |
|---|---|---|---|
| `ai-council` | **yes** | `7a3c057` | public; the Wave-1 onboarding pilot |
| `corp-monorepo` | **yes** | `fd3325e` | private, attached read-only; the ADR-36 no-write class |
| `corp-sca-time-automation` | **yes** | `1a80a9e` | public |
| `corp-ops` | no | — | not present in this account's GitHub repo list |
| `demo-prep` | no | — | not present in this account's GitHub repo list |
| `life-architect` | no | — | not present in this account's GitHub repo list |
| `terminal-setup` | no | — | not present in this account's GitHub repo list |
| `win-tooling` | no | — | not present in this account's GitHub repo list |

The five unread consumers appear to be local-only (they are in ADR-104's declaration and in
`ecosystem/satellite-onboarding-rulings.yaml`, but not on the GitHub remote this session can
reach). **Their governance is unverified here.** §7 states what the architect must confirm
before a ruling generalizes to them.

**On the brief's "7 reverted PR READMEs preserved in lane k's packet" — partially verified,
and two parts do not hold.** Stated precisely, because the difference matters to the ruling:

1. **One reverted PR is verified, not seven.** `rdwornik/corp-monorepo#54`
   (`docs/seed-handoffs-runbook` → `main`, opened 2026-08-16T13:16:55Z, **closed unmerged**
   13:51:02Z, +243 lines across 1 file — the hub runbook's 247 lines minus its 4 frontmatter
   lines, i.e. exactly what `seed_runbook.generalize_body` emits). Its closing comment is the
   clearest statement of the block in existence and is quoted in full at §1.
2. **The other six could not be checked from this session.** GitHub API scope covers only
   `rdwornik/dev-knowledge` and `rdwornik/corp-monorepo`; `git ls-remote` against the two
   other public consumers shows **no** `seed`/`runbook`/`handoff` branch surviving on either.
   The count 7 is neither confirmed nor refuted here — it is simply out of reach.
3. **The named preservation site does not exist in the hub remote.** The closing comment says
   content is *"preserved in the hub's
   `docs/audits/2026-08-16-technical-k-293-cross-repo-seeding-lane-packet.md`"*. That path is
   **absent from `origin/main` and from every branch on `origin`** (`git cat-file -e` →
   *"does not exist in 'origin/main'"*; `git ls-remote --heads origin` lists no lane-k
   branch). Consistent with `docs/audits/2026-08-16-technical-batch-6-manifest.md:12`, which
   records lane **k** as *"defined in the pack but **NOT dispatched** — it is
   operator-word-gated and no word was given"*. The likeliest reading is an unpushed local
   worktree; either way, **the reverted content is not currently recoverable from the hub
   remote**, and that is a fact the architect should know before treating it as banked.

This report therefore does not depend on the packet. Everything it needs — the seeded body,
the destination, and the reason for reversion — is reconstructible from committed hub sources
plus the live PR record, and is cited as such.

---

## 1. The block, from the sources themselves

Four independent sources say the same thing; none of them is the seeder's own docstring
speaking about itself.

**ADR-60 (amendment 2026-05-27), the taxonomy table** — `ADR-60-docs-folder-taxonomy.md:112`:

> `handoffs/` | OUTPUTS — ALL handoff bundles (centralized canonical home; child repos do NOT carry `handoffs/`)

and `:123`:

> Child code repos do **not** carry `handoffs/`, `research/`, or `council-questions/`. Handoffs centralize in `.dev-knowledge`.

**The 2026-07-08 census amendment ruling** —
`docs/audits/2026-07-08-census-amendment-docs-handoffs-ruling.md:25-29`:

> **ADR-60 / ADR-42 WIN.** Child repos do **NOT** create a local `docs/handoffs/`. Handoffs
> are centralized in `.dev-knowledge` — this is **intended divergence, not drift**. The
> census f.6 / §B-6 target is **amended to `docs/intake`-only** for child repos;
> `docs/handoffs/` is **removed** from any child-repo `docs/` target.

and, decisively for this report, `:50-52`:

> Any runbook / onboarding surface that names `docs/handoffs` as a child-repo target is
> stale and must read `docs/intake`-only.

**ADR-36's read/write boundary** — `ADR-36-audit-tool-architecture.md:109`, `:118`:

> ### Read/write boundary (Q5) — Hard constraint, read-only for child repos
> … NEVER touches child repos. Read-only contract is hard constraint in ADR-36, enforced via
> tool architecture (no write paths to child repo paths).

**The reversion itself** — `rdwornik/corp-monorepo#54`, closing comment, 2026-08-16T13:51:02Z,
verbatim:

> Closing per architect ruling: ADR-60 (docs/ folder taxonomy) explicitly states child repos
> do NOT carry a local docs/handoffs/ directory -- handoffs centralize in .dev-knowledge. The
> 2026-07-08 census amendment ruling resolved this exact question, and hub BACKLOG #303 (open)
> flags that scripts/seed_runbook.py needs to become ADR-60-aware before this fan-out runs.
> **This PR's destination path was wrong, not the intent to seed a runbook** — content is
> preserved in the hub's docs/audits/2026-08-16-technical-k-293-cross-repo-seeding-lane-packet.md
> pending a corrected-destination ruling. Not merged.

The emphasis is the closer's framing and it is the exact question this report answers:
**the destination was wrong; what is the right one — if any?**

### 1a. The mechanical detail that constrains every candidate

`scripts/seed_runbook.py:42` hardcodes the destination:

```
_RUNBOOK_REL = Path("docs") / "handoffs" / "README.md"
```

and `:97` creates it unconditionally (`target.parent.mkdir(parents=True, exist_ok=True)`).
So the tool **creates the forbidden directory as a side effect** — which is precisely what
open row `[#303]` says: *"a literal seed creates the exact dir ADR-36 forbids."* Any home the
architect rules is a change to that constant, not merely to a runbook.

### 1b. The seeded body is wrong for a consumer even if the path were legal

This is the finding that turns "wrong destination" into "wrong artifact", and it is visible
in the runbook's own text. `docs/handoffs/README.md:30`:

> A v5/v6 handoff is a small folder under `docs/handoffs/{YYYY-MM-DD}-{slug}/` with **four** files

`generalize_body` (`seed_runbook.py:56-61`) substitutes exactly one token — the H1's repo name
(`_TITLE_RE`, `:45`). Everything else is copied verbatim. So a seeded copy in `ai-council`
would be titled ``# Handoffs — operator runbook (`ai-council`)`` and would then instruct the
reader to open `docs/handoffs/{date}-{slug}/` **in a repo that has no such directory and is
forbidden to have one**. The seeded runbook is not merely mis-filed; **its body is false in
the tree it would be filed in.** Re-homing the same bytes to a legal path does not fix this.

---

## 2. ADR-60's rationale, extracted as scoring criteria

The brief asks that candidates be scored against ADR-60's rationale, so the criteria are
lifted from ADR-60's own text rather than invented.

- **R1 — a location declares a role.** `:17` *"a file's folder should tell you what it is"*;
  `:40` *"**One role per folder.** A file's location declares its semantic role."*
- **R2 — no hub-specific surface propagated into children.** `:103` *"**Over-propagated.**
  Child code repos received `.dev-knowledge`-specific folders … Child code repos do not need
  these folders."*
- **R3 — cross-repo navigational uniformity.** `:156` *"when the operator opens any child
  repo, the `docs/` tree should look the same. A future ADR or audit should land in an
  already-present folder rather than triggering folder creation on each first use."*
- **R4 — a home must earn its permanence.** `:100` *"**Over-built.** `council-questions/` and
  `research/` don't earn permanent folders"*; `:102` *"a 'working scratchpad' folder becomes a
  junk-drawer"*; `:187` *"'Add only on first need' remains the rule for folders **outside**
  the baseline."*
- **R5 — the centralization invariant survives.** `:112`, `:123` (quoted at §1) — handoffs
  centralize in the hub, and any home must leave that true rather than re-import it.

Three mechanical criteria are added because a home that cannot be delivered or checked is not
a home:

- **M1 — a carrier already exists.** The hub can put the content there without new deploy
  machinery.
- **M2 — a gate already watches it.** Presence/freshness is enforced by something live, so the
  home cannot silently rot.
- **M3 — it does not re-open `[#303]`.** The remedy should make the ADR-36-child hazard
  *unreachable*, not merely handled.

**A sixth criterion is added from outside ADR-60**, because the 2026-07-22 ADR-101 amendment
is the fleet's most recent ruling on exactly this question (where does a runbook live) and it
priced a cost ADR-60 does not name — `ADR-101-hermetization.md:201`, operator verbatim:

> "ADR-101 priced the cost of moving (~4 refs) but never priced the standing cost of a
> one-member genre with no queue; repo-onboarding.md is a process spec, the same content class
> protocols/ already holds."

- **R6 — no one-member surface with no queue.** A home that will hold exactly one file forever
  carries a standing cost the fleet has already ruled against paying.

---

## 3. Consumer-side ground truth (read live)

### 3a. All three verified consumers already state the rule, in their own trees

- `ai-council/docs/archive/README.md:14` (and `corp-monorepo/docs/archive/README.md:14`,
  `corp-sca-time-automation/docs/{archive,audits,decisions}/README.md:14/:15/:12` — the same
  sentence, four to six times over):

  > This is a child code repo. Its `docs/` carries `decisions/` + `audits/` + `archive/` (+
  > `diagrams/` where applicable). It does **not** carry `handoffs/` (centralized in
  > `.dev-knowledge/docs/handoffs/`), `research/`, or `council-questions/`.

- `ai-council/docs/intake/README.md:14-16`:

  > Note: ai-council has **no `docs/handoffs/`** — per ADR-60/ADR-42, handoffs centralize in
  > `.dev-knowledge`, not in child repos.

- `ai-council/docs/intake/2026-07-08-runbook-gap-notes.md:42-48` — the consumer's own G3,
  which is the origin of the whole thread:

  > ### G3 — `docs/handoffs` census target conflicts with ADR-60/42 (NEEDS-RULING) … created
  > `docs/intake/` only (operator GO); did **not** create `docs/handoffs/`.

**Live `docs/` trees, as read:** `ai-council` → `archive audits decisions intake`;
`corp-monorepo` → `archive audits decisions intake`; `corp-sca-time-automation` →
`archive audits decisions` (no `intake/`). **None carries `handoffs/`.** The rule is not
merely written down; it is the observed state of every consumer this session could open.

### 3b. There is already a consumer-side handoff *section*, and it is spine-enforced

Every verified consumer carries `CONTRIBUTING.md` → `## Handoff process`, and that heading is
a **required canonical spine heading**, `scripts/audit.py:1326`:

```
"CONTRIBUTING.md": ["## Branch naming", "## Commit style", "## Handoff process"],
```

`CONTRIBUTING.md` is also on the freshness gate's default list —
`scripts/canonical_freshness_gate.py:32-33` — so the section cannot be edited-and-forgotten
without `canonical_freshness` reddening. What the three consumers put under that heading
today:

- `ai-council/CONTRIBUTING.md:147` —
  > Handoffs **centralize in `../.dev-knowledge/docs/handoffs/`** (ADR-42/60) — this repo
  > carries no local `docs/handoffs/`. Continuing a prior session: read the most recent bundle
  > there.
- `corp-monorepo/CONTRIBUTING.md:144` —
  > Handoffs centralize in `../.dev-knowledge/docs/handoffs/` per ADR-36/62 — **this repo
  > carries no `docs/handoffs/`** (ADR-36 read-only contract; a handoff never writes to a
  > target repo). Continuing a prior session: read the most recent corp-monorepo bundle there
  > (start with its `HANDOFF_BOOT.md`), then the last 5 `JOURNAL.md` entries here.
- `corp-sca-time-automation/CONTRIBUTING.md:70-73` —
  > Handoffs centralize in `../.dev-knowledge/docs/handoffs/` (ADR-42/60) — this repo carries
  > no `docs/handoffs/`. Continuing a prior session: read the most recent bundle there, then
  > recent commits + the last `JOURNAL.md` entries here.

**The consumer-side home already exists and is already populated.** The `[#293]` fan-out is
not filling a hole; it is proposing a second, redundant surface next to a filled one.

### 3c. The one real defect this survey found

The hub-owned `first-read` region — `templates/claude-regions/first-read.md:3`, materialized
byte-verbatim into consumer `CLAUDE.md` files — tells the reader to open *"the canonical
operator runbook `docs/handoffs/README.md`"*. **In a consumer that path does not resolve, and
is forbidden to.** Two of the three verified consumers patch this locally with an adjacent
`owner=repo` note:

- `ai-council/CLAUDE.md:23` (hub region, mis-pointing) vs `:29` (local patch):
  > **Repo note (ai-council):** this repo carries no local `docs/handoffs/` — handoffs
  > centralize in `../.dev-knowledge/docs/handoffs/` (ADR-42) …
- `corp-monorepo/CLAUDE.md:26` (hub region, mis-pointing) vs `:35` (local patch):
  > Item 4 handoff bundles: corp carries **no local `docs/handoffs/`** (ADR-36 read-only
  > contract). Read the most recent corp-monorepo bundle at `../.dev-knowledge/docs/handoffs/`
  > instead.

`corp-sca-time-automation` has **not** adopted the hub `first-read` region at all (its
`CLAUDE.md:12-20` is a local §1, `last_reviewed: 2026-06-02`, with no handoff line), so it has
nothing to mis-point and nothing to patch.

**This — not a missing runbook copy — is the live boot defect.** It is a one-line fix at a
hub-owned carrier, and it is the same shape as the fix `CLAUDE.md` §12 v2.55/v2.56 already
made twice to this exact region. A second per-repo patch is a symptom; the region is the site.

One further stale line, recorded for the architect but out of this report's scope: the hub's
own consumer CONTRIBUTING carrier `templates/CONTRIBUTING-md-template.md:139` still says CC
*"emits a lean **residual** + a **probe manifest** under `docs/handoffs/<slug>/`"* — the same
child-repo `docs/handoffs` claim the 2026-07-08 ruling `:50-52` declares stale. It has
propagated verbatim into `ai-council/CONTRIBUTING.md:145`. `corp-sca` is clean of it.

---

## 4. Candidate homes

Three candidates. For each: the directory is quoted from a live tree; where a filename is new
it is explicitly labelled a proposal, never asserted.

### H1 — no consumer-side file; `CONTRIBUTING.md` → `## Handoff process` is the home

**Path:** `CONTRIBUTING.md`, heading `## Handoff process`. **Exists in all three verified
consumers today** (§3b), is required by `scripts/audit.py:1326`, and is freshness-gated by
`scripts/canonical_freshness_gate.py:32-33`.

**What lands there:** nothing new. The section already carries the pointer. The ruling would
(a) declare this the canonical consumer-side home for hub-runbook guidance, (b) fix
`templates/claude-regions/first-read.md:3` so the boot instruction resolves in a consumer, and
(c) close the fan-out as *not-applicable-by-construction* rather than deferred.

**Why the runbook body is not needed locally:** the runbook is instructions for consuming a
bundle that lives in the hub (`docs/handoffs/README.md:30`). An operator or agent who cannot
reach the hub checkout cannot reach the bundle either, so a local copy of the instructions is
inert exactly when it would be needed. The copy is redundant **by construction**, not by
preference.

**Carrier:** `templates/CONTRIBUTING-md-template.md:135` (hub-owned, already materialized in
all three verified consumers).

### H2 — `protocols/` in the consumer (proposed filename `protocols/HANDOFF_RUNBOOK.md`)

**Directory quoted live:** `ai-council/protocols/` (holds `COUNCIL_INVOCATION_CONTRACT.md`,
`COUNCIL_QUESTION_GUIDE.md`, `README.md`, `SYNTHESIS_QUALITY_RUBRIC.md`);
`corp-monorepo/protocols/` (holds `CORP_INTERFACE.md`, `README.md`).
**`corp-sca-time-automation` has no `protocols/` directory at all** (root read live).
**The filename is a proposal**, following the ADR-34 `Protocols → UPPERCASE_WITH_UNDERSCORES.md`
row that ADR-101's 2026-07-22 amendment `:200` cites.

**Basis:** the strongest precedent in the corpus. ADR-101 §4 d.i was **REVERSED** on
2026-07-22 exactly on the question "where does a runbook live", and the answer was
`protocols/` — `ADR-101-hermetization.md:200`: *"`docs/runbooks/repo-onboarding.md` moves
content-byte-identical to `protocols/REPO_ONBOARDING.md` … `docs/runbooks/` is deleted;
`runbooks` **leaves** the §1 sanctioned Tier-2 genre set."* The hub tree confirms the outcome:
`docs/runbooks/` is **absent**, `protocols/REPO_ONBOARDING.md` is **present**, and
`scripts/validate_hermetization.py:94-98` records the removal in code —
*"`runbooks` LEFT the set 2026-07-22 (ADR-101 amendment: d.i REVERSED — the one-member genre
collapsed into protocols/)."*

**The cost this precedent also names:** the same amendment is why H2 scores badly on R6. A
consumer `protocols/HANDOFF_RUNBOOK.md` in `corp-sca` would require creating `protocols/` to
hold exactly one file with no queue behind it — the precise standing cost the operator's
verbatim reason at `:201` refuses to pay.

**Direct contradiction to weigh:** the hub's own consumer CONTRIBUTING carrier says the hub
protocol set is *"read at the hub `.dev-knowledge/protocols/` set; **hub-pointer, never copied
into a consumer**"* (`templates/CONTRIBUTING-md-template.md:139`, materialized at
`ai-council/CONTRIBUTING.md:145` and `corp-monorepo/CONTRIBUTING.md:144`). H2 copies a hub
protocol-class document into a consumer `protocols/`, which is the thing that sentence forbids.

### H3 — `.claude/` in the consumer (proposed filename `.claude/HANDOFF-RUNBOOK.md`)

**Directory quoted live:** present in **all three** verified consumers, each already holding a
hub-owned, hash-guarded replica: `ai-council/.claude/` and `corp-sca-time-automation/.claude/`
and `corp-monorepo/.claude/` each contain `CLAUDE-FLOOR.md`, `CLAUDE-FLOOR.md.sha256`,
`check_floor_hash.py`, `settings.json`. **The filename is a proposal.**

**Basis:** the only *mechanically proven* hub→consumer document carrier in the fleet. The
floor model (`deploy/carrier_floor.py:9-13`, source `templates/child-methodology-floor.md.tmpl`)
already ships a hub-authored body into every consumer as a **replica with a hash sidecar**,
detected as `ABSENT` / `PRESENT_CORRECT` / `PRESENT_DRIFTED`. A second such replica is a
manifest edit, not new code — `deploy/manifest-v1.4.0.yaml:355-362` says of the docs carrier:
*"Alone among the carriers it hardcodes NO payload … so shipping one more hub doc is a
manifest edit, not a code change."* It also has a live cross-class precedent: the same carrier
ships `plugins/tier1-lifecycle/INSTALL.md` to the **consumer root** under an operator ruling
(*"INSTALL.md uniform fleet-wide, hub-owned, deploy-carried"*, manifest `:377-385`), and
`INSTALL.md` is present at the roots of `ai-council` and `corp-monorepo`.

**Cost:** `.claude/` is agent-runtime configuration, not an operator-facing docs surface —
R1's role test cuts against it. And the floor it would sit beside already discharges the same
need in one line: `templates/child-methodology-floor.md.tmpl`, *"Depth escape-hatches"* —
*"The methodology hub (`.dev-knowledge`) — full protocols (PLAYBOOK / ESSENTIALS). Depth only;
this floor is self-sufficient for a normal session."*

---

## 5. Scoring

Scale: **++** fully satisfied · **+** satisfied with a caveat · **−** violated · **−−**
violated in the way the criterion was written to prevent.

| Criterion (source) | H1 CONTRIBUTING §Handoff process | H2 consumer `protocols/` | H3 consumer `.claude/` |
|---|---|---|---|
| R1 location declares role (`ADR-60:17,:40`) | **++** the section's role *is* process guidance; no folder role invented | **+** `protocols/` = process specs, correct class | **−** agent-runtime config, not operator docs |
| R2 no hub surface propagated (`ADR-60:103`) | **++** nothing propagates | **−** copies a hub protocol-class doc into a child — the exact over-propagation shape | **−** propagates a hub doc, though as a declared replica |
| R3 navigational uniformity (`ADR-60:156`) | **++** heading is spine-required in every repo, present in 3/3 | **−−** `corp-sca` has no `protocols/`; uniformity requires creating it | **+** `.claude/` present in 3/3 |
| R4 earns permanence (`ADR-60:100,:102,:187`) | **++** zero new files | **−** new file, and in one repo a new folder | **+** new file in an existing, populated dir |
| R5 centralization intact (`ADR-60:112,:123`) | **++** the text *states* centralization | **+** intact — the body would still point at the hub | **+** intact |
| R6 no one-member surface (`ADR-101:201`) | **++** no new surface at all | **−−** `corp-sca` gets a one-member `protocols/` with no queue | **+** joins an existing multi-file dir |
| M1 carrier exists | **++** `templates/CONTRIBUTING-md-template.md:135`, already materialized 3/3 | **−** no carrier ships to consumer `protocols/`; new manifest work | **++** `carrier_docs` ships arbitrary doc pairs today |
| M2 gate watches it | **++** `audit.py:1326` spine + `canonical_freshness_gate.py:32-33` | **−** nothing gates a consumer `protocols/` file | **+** hash-verified (`verify: hash`), though drift-detected not content-checked |
| M3 closes `[#303]` | **++** makes the ADR-36-child hazard **unreachable** — no seeder path to a consumer `docs/` | **+** removes the hazard by moving the target | **+** removes the hazard by moving the target |

**Second-order fact that separates H1 from both alternatives.** H2 and H3 both re-home the
runbook *body*, and §1b showed that body is false in a consumer tree: it instructs the reader
to open `docs/handoffs/{date}-{slug}/` in a repo forbidden to have one. Adopting H2 or H3
therefore does **not** close the work — it adds a second obligation (rewrite or parameterize
the body so it is true where it lands), and `generalize_body` (`seed_runbook.py:56-61`)
substitutes only the H1 repo-name token, so that rewrite is new machinery, not a flag.

---

## 6. Recommendation

**Recommend H1: the consumer-side home for hub-runbook guidance is `CONTRIBUTING.md` →
`## Handoff process`, and no runbook file is seeded into any consumer.**

Stated as the ruling it asks for:

> The `docs/handoffs/README.md` runbook is **hub-resident and hub-only**. Its consumer-side
> surface is the already-required `CONTRIBUTING.md` → `## Handoff process` section, which
> points at `../.dev-knowledge/docs/handoffs/` — the state every verified consumer is already
> in. `[#293]`'s fan-out is **not-applicable-by-construction**, not deferred.

Why, in one line each:

1. **It is already true.** 3 of 3 verified consumers already carry the pointer at that
   heading; the ruling records reality instead of building toward it.
2. **The artifact is wrong for the destination, not just the path.** §1b — re-homing the same
   bytes moves a false statement rather than fixing it.
3. **It is the only candidate with both a live carrier and a live gate** (M1+M2), so it cannot
   silently rot; H2 has neither.
4. **It pays no standing cost.** R4/R6 — and the 2026-07-22 amendment is the fleet's own
   ruling that a one-member surface with no queue is not worth its keep.
5. **It makes `[#303]` unreachable rather than handled** — with no seeder path into a consumer
   `docs/` tree, the ADR-36-child hazard has no instance to guard against.

**Three consequential acts follow (all hub-local, none touching a consumer):**

- **A1 — fix the mis-pointing boot instruction.** `templates/claude-regions/first-read.md:3`
  names `docs/handoffs/README.md` unconditionally; in a consumer it does not resolve.
  This is the real defect (§3c) and the only one that costs a live session anything. Same
  shape as the `CLAUDE.md` §12 v2.55/v2.56 fixes to this same region.
- **A2 — retire the hardcoded destination.** `seed_runbook.py:42` should stop being a
  consumer-facing tool: under H1 it is a hub self-seed / no-op, and `[#303]`'s
  "child-class-aware" requirement is satisfied by there being no child class to seed.
- **A3 — clear the stale carrier line.** `templates/CONTRIBUTING-md-template.md:139` still
  names a child-repo `docs/handoffs/<slug>/`, which the 2026-07-08 ruling `:50-52` declares
  stale, and it has already propagated to `ai-council/CONTRIBUTING.md:145`.

**Runner-up, if the architect rejects H1.** H3, not H2 — it has the only proven carrier and
keeps navigational uniformity, whereas H2's `corp-sca` gap forces exactly the one-member
surface ADR-101 ruled against. If H3 is taken, the body rewrite (§5, second-order) must be
scoped as part of it, not assumed away.

---

## 7. Per-repo exceptions

**Under H1 there are no exceptions in the ruling itself** — the home is a heading every repo is
already required to carry. What differs is the per-repo *starting state*:

- **`ai-council`** — compliant. Carries the pointer (`CONTRIBUTING.md:147`) plus a local
  `first-read` patch (`CLAUDE.md:29`). **Two cleanups owed after A1/A3:** the local patch
  becomes redundant once the region is fixed, and `CONTRIBUTING.md:145` carries the stale
  child-repo `docs/handoffs/<slug>/` line. **One unrelated stale reference found:**
  `docs/audits/README.md:60` — *"Cross-repo handoff artifacts → `docs/handoffs/archive/`"* —
  routes to a path this repo is forbidden to have.
- **`corp-monorepo`** — compliant, and the **strongest** no-write case: it is the ADR-36
  read-only class by its own governance (`CLAUDE.md:35`, `:136`; `CONTRIBUTING.md:144`), and
  it is the repo whose seeding PR was reverted. Under H1 nothing is owed here beyond A1's
  effect on `CLAUDE.md:26`.
- **`corp-sca-time-automation`** — compliant via `CONTRIBUTING.md:70-73`, and **immune to the
  A1 defect**: its `CLAUDE.md` §1 is a local variant with no handoff line, so nothing
  mis-points. **It is also the repo that disqualifies H2** (no `protocols/`) and the one with
  no `docs/intake/`. Its `last_reviewed: 2026-06-02` is the oldest of the three.
- **`corp-ops`, `demo-prep`, `life-architect`, `terminal-setup`, `win-tooling`** — **UNVERIFIED
  by this lane; not reachable from this session.** All five are ruled `profile: full` in
  `ecosystem/satellite-onboarding-rulings.yaml`. Before the ruling generalizes, one read-only
  check per repo settles it: *does `CONTRIBUTING.md` carry `## Handoff process`, and does
  `docs/handoffs/` exist?* If a repo lacks the heading, H1's home is absent there and that repo
  is a genuine exception needing the section seeded — a `CONTRIBUTING.md` edit, still not a
  `docs/handoffs/` directory.

**Denominator note.** The `[#293]` row's Done-when reads *"0 of 6 consumers"*; the phase-1
integration ruling R6 (BACKLOG `[#293]`) fixed the denominator at **8** on ADR-104's
declaration. Under H1 the denominator question dissolves — the count is not of seeded files
but of repos already carrying the heading, which is **3 of 3 verified, 5 unverified**.

---

## 8. What this report does not do

- It does not rule. `[#293]` stays open and BLOCKED-ON-RULING; no BACKLOG line was changed.
- It writes nothing into any consumer repo, and opens/closes/comments on no PR.
- It does not recover the lane-k packet, which is absent from the hub remote (§0.3). If that
  packet carries per-repo detail for the five unverified consumers, it should be pushed before
  the ruling generalizes.
- It does not re-verify the count "7" (§0.2), and the architect should not treat it as
  established by this report.

---

## Evidence index

Every claim above resolves to one of these. Hub paths are at `main` `43cd1ce`; consumer paths
are at the HEADs in §0.

**Hub — decisions**
- `docs/decisions/ADR-60-docs-folder-taxonomy.md` — `:17` `:40` `:100-103` `:112` `:123` `:156` `:187`
- `docs/decisions/ADR-101-hermetization.md` — `:197-202` (2026-07-22 d.i reversal)
- `docs/decisions/ADR-36-audit-tool-architecture.md` — `:109` `:118`
- `docs/decisions/ADR-104-fleet-repository-shape.md` — §Context (the 8-member fleet)
- `docs/audits/2026-07-08-census-amendment-docs-handoffs-ruling.md` — `:25-29` `:47-49` `:50-52`

**Hub — code and carriers**
- `scripts/seed_runbook.py` — `:10-16` `:24-26` `:42` `:45` `:56-61` `:97`
- `scripts/audit.py:1326` — `_CANONICAL_SPINE["CONTRIBUTING.md"]`
- `scripts/canonical_freshness_gate.py:32-33` — `DEFAULT_FRESHNESS_FILES`
- `scripts/validate_hermetization.py` — `:94-98` (genres; `runbooks` removed) `:171-176` (Rule C docs homes)
- `templates/claude-regions/first-read.md:3` · `templates/CONTRIBUTING-md-template.md:135,:139`
- `templates/child-methodology-floor.md.tmpl` (Depth escape-hatches) · `deploy/carrier_floor.py:9-13`
- `deploy/manifest-v1.4.0.yaml:355-362` (docs carrier hardcodes no payload) `:377-385` (INSTALL.md root ruling)
- `docs/handoffs/README.md:6-17` (header) `:19` (H1) `:30` (bundle location)
- `docs/audits/2026-08-16-technical-batch-6-manifest.md:12` (lane k not dispatched)
- `BACKLOG.md` — `[#293]` (row + R6 denominator) · `[#303]` (seeder not child-class-aware)
- `ecosystem/satellite-onboarding-rulings.yaml` (profiles) · `protocols/REPO_ONBOARDING.md` (the moved runbook)

**Consumers (read-only clones)**
- `ai-council` @ `7a3c057` — `CLAUDE.md:23,:29` · `CONTRIBUTING.md:145,:147` ·
  `docs/archive/README.md:14` · `docs/audits/README.md:60` · `docs/intake/README.md:14-16` ·
  `docs/intake/2026-07-08-runbook-gap-notes.md:42-48` · `docs/` tree · `protocols/` · `.claude/`
- `corp-monorepo` @ `fd3325e` — `CLAUDE.md:26,:35,:136` · `CONTRIBUTING.md:144` ·
  `docs/archive/README.md:14` · `docs/` tree · `protocols/` · `.claude/`
- `corp-sca-time-automation` @ `1a80a9e` — `CLAUDE.md:12-20` · `CONTRIBUTING.md:70-73` ·
  `docs/{archive,audits,decisions}/README.md:14/:15/:12` · `docs/` tree (no `intake/`) ·
  no `protocols/` · `.claude/`

**Live PR record**
- `rdwornik/corp-monorepo#54` — `docs/seed-handoffs-runbook` → `main`; opened
  2026-08-16T13:16:55Z, closed unmerged 13:51:02Z; +243 lines / 1 file; closing comment
  quoted in full at §1.
- `git ls-remote --heads origin` (hub) — no lane-k branch; `git cat-file -e
  origin/main:docs/audits/2026-08-16-technical-k-293-cross-repo-seeding-lane-packet.md` →
  does not exist.

---

**Compiled by:** CC (`claude-opus-5`), lane nb5-B, 2026-08-16. Read-only w.r.t. every consumer
repo and w.r.t. the hub spine; this report and the regenerated `docs/audits/README.md` index
are the lane's entire write footprint.
