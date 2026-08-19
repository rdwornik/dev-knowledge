# Per-repo agentic-review profiles — draft pack (`[#82]`, E6)

**Lane:** CLOUD C2 · contract of record `docs/audits/2026-08-19-technical-c2-review-profiles-contract.md` @ `916e314`
**Date:** 2026-08-19
**Posture:** read-only over the tree + this one artifact. No live config lands, no check is edited, no profile is enforced.
**Items:** 1 CLEAR · 2 CLEAR · 3 CLEAR (with the §0 evidence boundary) · 4 CLEAR.

> **This memo is deliberately NOT admissible as a review artifact, and that is a designed property, not an accident.**
> `check_review_artifact_coverage` admits any file under `docs/audits/` that matches `^# Codex Review\b`
> **and** carries a `^**Branch:**` or `^**HEAD:**` line — the regexes are multiline-anchored and know nothing
> about code fences. A memo that quoted the required header shapes at line start would enter the candidate set
> and could link itself to a real merge, corrupting the exact false-positive count `[#499]`'s hard flip is gated on.
> Every header sample below is therefore **indented by two spaces inside its fence**, which defeats the `^` anchor
> while leaving the shape readable. §5.3 records the self-check that proves it.

---

## 0 · Method, and the one evidence boundary this lane could not cross

Read, in full or in the cited range: the `[#82]` row (`tasks/82-define-per-repository-agentic-review-profiles.md`,
mirrored `BACKLOG.md:208`); the fleet declaration (`ecosystem/parity-surfaces.yaml` `fleet:` map, version 1.4.0);
`ecosystem/registry.md`; `ecosystem/deployed-versions.yaml`; `.methodology.yaml`; `scripts/audit.py:3117-3320`
(`check_review_artifact_coverage` and its constants, read line-by-line); `codex/AGENTS.md` (the hub-owned global
reviewer config); `protocols/PLAYBOOK.md` §16 Codex-utilization doctrine (`:4230-4290`) and §17 Code Quality Audit
Process; `ARCHITECTURE.md` Ch6 verification-mesh table (`:844-856`); `docs/audits/2026-08-19-technical-n5-codification-pack.md`
§4.1-§4.5 **and** its post-STOP amendment; `docs/audits/2026-08-19-technical-n4-grooming-wave1.md` §[E6];
`docs/audits/2026-08-18-technical-review-lane-contract.md`.

Three recent review artifacts read end-to-end at their headers plus body structure:
`2026-08-15-codex-o-review.md`, `2026-08-18-codex-review-batch1-c-e.md`, `2026-08-18-codex-review-batch1-a.md`
(the two 08-18 files are the pair that failed admission and mislinked; the 08-15 file is the wrapper-shaped control).
`2026-08-15-codex-m-review.md` and `2026-08-14-codex-524-check-extensions.md` were read as further controls.

**EVIDENCE BOUNDARY — stated first because it bounds item 3.** This is a cloud container whose repository scope is
`rdwornik/dev-knowledge` alone. The two walked consumers (`ai-council`, `corp-monorepo`) are **not present and not
readable here**. Their profiles below are therefore derived from **hub-side records only** — the parity manifest, the
registry, the deployed-versions record, the `[#82]` row's own naming of their domains, and this repo's history files
under `ecosystem/<repo>/history/`. That is enough to draft a profile; it is **not** enough to assert what review
either repo runs today. Every consumer-side claim below is marked **(hub-record derived — unverified against the repo)**.
A filing seat with sibling-tree access closes that gap in one read per repo; nothing else about the drafts changes.

Gates were **not armed in this container** (no `pre-commit` install); §5.3 records what was run by hand instead.

---

# ITEM 1 — the repo classes that actually differ · **CLEAR**

## 1.1 · The denominator, from the declaration rather than the deployment registry

`ecosystem/parity-surfaces.yaml` (v1.4.0) carries the ADR-104 declaration as its `fleet:` map — 9 members,
each with a `role`:

```
  .dev-knowledge              hub
  ai-council                  consumer      deployed corpus 1.3.1 (2026-07-11)
  corp-monorepo               consumer      deployed corpus 1.2.0 (2026-07-07, held by ADR-102 ruling)
  corp-ops                    pre-deploy    reason: registered, unonboarded
  corp-sca-time-automation    pre-deploy    reason: registered, unonboarded (floor-carrying)
  demo-prep                   pre-deploy    reason: registered, methodology-unonboarded
  life-architect              pre-deploy    reason: registered, methodology-unonboarded
  terminal-setup              pre-deploy    reason: registered 2026-08-01 ([#462]), unonboarded
  win-tooling                 pre-deploy    reason: registered, unonboarded
```

N4's `[E6]` sweep measured **0 of 9 carrying a profile** — no `agentic-review` / `review_profile` key exists anywhere
in `ecosystem/`. That measurement is re-confirmed here by the same predicate; it is the baseline this pack drafts against.

**The population fact that decides the rollout's shape**, and it is already recorded rather than newly claimed:
`.methodology.yaml`'s `.devcontainer` entry (D8, ruled today) states it measured — *"parity-surfaces.yaml declares 9
members but 6 are pre-deploy and are not walked, so either route affects 2 repos today, not the 7 the dispatch framing
implied."* The same arithmetic governs `[#82]`: **3 repos are walked (hub + 2 consumers), 6 are not.** A profile pack
that drafts 9 live profiles would be writing 6 of them against trees nothing visits.

## 1.2 · Three classes — and the test that separates them is not "what kind of repo is it"

The tempting axis is domain (`[#82]`'s own row suggests it: *"corp-monorepo deep-audit, ai-council's flow"*). Measured
against the live machinery, domain is **not** the axis that changes a profile. Three properties are:

```
  P1  Is the repo WALKED?            hub + consumers yes; pre-deploy no (rendered "skipped (pre-deploy)")
  P2  Does it carry ENFORCEMENT      hub only: the gate mesh, audit.py's check suite, the deploy carriers.
      ORGANS whose own failure is    A consumer carries deployed gates but AUTHORS none.
      a fleet-wide event?
  P3  Does a code surface exist      hub: yes (~scripts/, deploy/, ecosystem/schema/). Consumers: yes, their own.
      under the RULED predicate?     pre-deploy: unknown/irrelevant while unwalked.
```

`P2` is the one that genuinely bifurcates hub from consumer, and it is visible in the checker itself:
`check_review_artifact_coverage` is **HUB-ONLY by repo identity** (`scripts/audit.py:3218-3219`, `if not _is_hub(...)`)
with the stated reason *"the codex-review artifact convention is a hub practice (108 artifacts here, none in a
consumer), so scanning consumers would manufacture a fleet gap."* So the artifact-coverage discipline this pack encodes
is, today, a **hub practice with no consumer enforcement** — a consumer profile records intent, not a checked property.

`P1` is what makes the pre-deploy class a *named absence* rather than a profile. `[#82]`'s Done-when already permits
exactly this: *"any member deliberately without one is named there with its reason."*

**Verdict — three classes, and the two consumers do NOT split into two.** `ai-council` and `corp-monorepo` differ in
domain, code volume and deployed-corpus version, but on all three properties above they are identical: walked,
enforcement-consuming, code-bearing. They differ in **review FOCUS** (a per-repo string) and in **full-audit cadence**
(a per-repo interval) — both of which the schema below carries as fields. Splitting them into separate classes would
put a per-repo value in the class axis, where it cannot be checked.

## 1.3 · What the three read artifacts show about the shape a profile has to produce

| artifact | producer | title | linkage fields | tally | outcome under the live check |
|---|---|---|---|---|---|
| `2026-08-15-codex-o-review.md` | `/codex-review` wrapper | canonical | Branch + HEAD, one triple | present, `0/1/0/0` | admitted, linked, tallied — green |
| `2026-08-18-codex-review-batch1-c-e.md` | hand-authored CC seat | canonical | **two** Branch/HEAD triples | present (branch C only) | admitted; links **C only** — E's merge WARNs though reviewed |
| `2026-08-18-codex-review-batch1-a.md` | hand-authored CC seat | `# TERRA REVIEW — …` | Branch + HEAD, well-formed | **absent** | **never admitted** — skipped before its fields are read |

The discriminator is **producer, not reviewer**. All three record `gpt-5.6-terra`-class review of a real diff. The two
that fail were written by a Claude seat composing the artifact by hand; the one that passes was emitted by the wrapper,
which supplies the title and the tally line the reviewer config never mentions. `codex/AGENTS.md` §"Output Format"
specifies per-finding blocks and **no document title and no tally** — so a hand-authored artifact following the global
reviewer config faithfully will still fail admission. **That is the root cause of both 08-18 failures**, and it is why
§2 puts the title and tally into the *profile* rather than leaving them to the author's memory.

---

# ITEM 2 — draft profile schema · **CLEAR**

## 2.1 · The admission contract, quoted verbatim from the check

Source: `scripts/audit.py`, read at this lane's HEAD. Line numbers and byte-exact source:

```
  3137  _REVIEW_TALLY_RE   = re.compile(r"(?m)^\*\*Tally:\*\*[ \t]*(\d+)/(\d+)/(\d+)/(\d+)\b")
  3143  _REVIEW_TITLE_RE   = re.compile(r"(?m)^# Codex Review\b")
  3150  _REVIEW_BRANCH_RE  = re.compile(r"(?m)^\*\*Branch:\*\*[ \t]*`?([^`\s]+?)`?[ \t]*$")
  3151  _REVIEW_HEAD_RE    = re.compile(r"(?m)^\*\*HEAD:\*\*[ \t]*`?([0-9a-f]{7,40})`?")
  3152  _REVIEW_MERGE_SUBJECT_RE = re.compile(r"^Merge branch '([^']+)'")
  3117  _REVIEW_RULING_DATE   = "2026-08-05"
  3118  _REVIEW_CODE_SUFFIXES = (".py", ".ps1")
  3136  _REVIEW_CODE_EXACT    = (".pre-commit-hooks.yaml", ".pre-commit-config.yaml")
  3149  _REVIEW_CUTOFF_EPOCH  = int(datetime(2026, 8, 5, tzinfo=timezone.utc).timestamp())
```

Five consequences a profile must encode, each read off the code rather than inferred:

1. **The title is the sole admission criterion.** `if not _REVIEW_TITLE_RE.search(txt) or not (branch_m or head_m): continue`
   (`:3235`). No title → the file is skipped **before any field is read**, so a perfect Branch/HEAD/Tally block is invisible.
   `\b` after `Review` means `# Codex Review — <anything>` matches and `# Codex Reviews` does not.
2. **Linkage is either-or.** Branch equality against the merge subject's `Merge branch '<x>'` capture, **or** HEAD
   prefix-matching a commit in the merge's `introduced()` set. Either satisfies; neither is required if the other holds.
3. **The tally is required on top of linkage, and is exactly four slash-separated integers** at line start.
   A linked artifact without it produces the separate `untallied` WARN.
4. **One triple per file.** Every field is read with `.search` → first match wins. A two-branch artifact links one branch.
5. **The merge message is a join key the reviewer never writes.** Naming the artifact in a merge body does nothing;
   the leg never reads it. Squash merges carry no such subject and cannot link by branch at all.

Two facts a profile must *not* misstate, both from the check's own docstring: the leg is **advisory (WARN)** per the
`[#480]` P3 ruling, with the hard pre-push leg deferred behind *"0 false positives over two consecutive windows"*
(`[#499]`); and its honest limit is that it verifies an artifact **exists, is linked, and is tallied** — never that the
review happened or was competent.

## 2.2 · Live admission census, measured at this HEAD

```
  docs/audits/*.md total           : 606
  carry ^# Codex Review title      : 134
  carry ^**Branch:** field         : 148
  ADMITTED (title AND branch|head) : 133
    of those, parseable **Tally:** :  31
    of those, >1 **Branch:** line  :   1
```

Reproduce: §5.3. Three readings worth recording. **(a)** 15 files carry a `**Branch:**` field and no canonical title —
the docstring's "13 tracked non-review audit docs" has grown by two, and the title predicate is still doing the
discriminating work it was measured to do. **(b)** 1 titled file carries no Branch/HEAD and is not admitted.
**(c)** Exactly **one** admitted file carries more than one `**Branch:**` line — `2026-08-18-codex-review-batch1-c-e.md`,
the N5 §4.2 mode-2 case. The multi-triple defect is currently **n=1 in the whole tree**, which is why §2.3 encodes
one-branch-per-artifact as a *profile rule* rather than proposing a reader change: the reader change is `[#499]`-adjacent
scope this lane does not own, and a profile rule prevents the next instance at zero cost either way.

## 2.3 · The schema (draft — YAML-shaped, lands nowhere in this lane)

Field grammar deliberately **reuses the fleet's existing declaration grammar** (`value` / `reason` / `provenance`,
ADR-102/103, and the `review_date` shelf-life device `.methodology.yaml` already uses twice) rather than inventing a
parallel one. Every `reason:` is MANDATORY and non-blank on the same terms the parity loader already enforces.

```yaml
# DRAFT — no file. Shape only.
review_profile:
  repo: <fleet member id>                 # MUST equal a key of parity-surfaces.yaml `fleet:`
  role: hub | consumer | pre-deploy       # MUST equal that member's declared role — never restated by hand
  status: active | named-absent           # named-absent REQUIRES `reason:` ([#82] Done-when, second clause)
  reason: >-                              # MANDATORY when status: named-absent; MANDATORY-blank-forbidden always
    <why this repo runs what it runs, or why it deliberately runs nothing>

  lanes:                                  # WHO reviews. Exact model strings only (PLAYBOOK: never a bare `gpt-5.6`)
    reviewer: gpt-5.6-terra               # doctrinal default; a deviation states its reason inline
    adversarial: gpt-5.6-sol | null       # the "when stakes warrant" second reader
    adversarial_predicate: >-             # RULING NEEDED (§4 R5): "when stakes warrant" is not checkable as written
      <the stated condition, e.g. "any diff touching a gate/organ under scripts/ or .pre-commit-config.yaml">
    heterogeneity: cross-vendor           # the [#82] design input: a same-architecture second reader converges

  triggers:                               # WHEN it runs. One entry per trigger class; cadence is per-entry
    - class: pre-merge-code-impact
      predicate: >-
        path.endswith(".py"|".ps1") OR path in (".pre-commit-hooks.yaml", ".pre-commit-config.yaml")
      cadence: per-merge                  # the ruled hub predicate, audit.py:3118/3136 — quoted, never widened here
      surface: code                       # code | doc — the wrapper's own routing axis ([#333])
      instrument: /codex-review
    - class: full-audit
      predicate: whole repo (src/ scope)
      cadence: <interval>                 # PLAYBOOK §17: "cadence by repo complexity"; per-repo, not per-class
      surface: code
      instrument: codex exec (full audit)
    - class: conformance
      predicate: claims-vs-docs coherence
      cadence: <interval>
      instrument: <organ>                 # hub: .claude/workflows/conformance-hub.js

  severity:
    scale: [Critical, High, Medium, Low]  # codex/AGENTS.md — the ONLY scale; P1/P2/P3 is a lane alias, not a scale
    fix_before_merge_floor: High          # >= this band blocks the merge until fixed or itemized
    diff_mode_reports: [Critical, High]   # codex/AGENTS.md: diff review skips Medium/Low as noise
    verdict_enum: [MERGE-CLEAN, "FIX-BEFORE-MERGE (itemized)", "BLOCK (reason)"]

  artifact:                               # SHAPE. Every value below is dictated by a live check — see §2.4
    dir: docs/audits/
    name_grammar: "<YYYY-MM-DD>-<class>[-<slug>]"   # ADR-101 Rule B, all-lowercase kebab
    class: codex                          # a member of the CLOSED 11-class enum; `review` is NOT one
    title_must_match: '(?m)^# Codex Review\b'       # audit.py:3143 — sole admission criterion
    tally_must_match: '(?m)^\*\*Tally:\*\*[ \t]*(\d+)/(\d+)/(\d+)/(\d+)\b'   # audit.py:3137
    tally_order: Critical/High/Medium/Low
    linkage_fields: [Branch, HEAD]        # audit.py:3150-3151; EITHER satisfies linkage
    branches_per_artifact: 1              # first-match-wins (.search) — a second branch is invisible
    producer: wrapper-preferred           # a hand-authored artifact MUST supply title+tally itself (§1.3)

  home: <path>                            # RULING NEEDED (§4 R1) — where the profile block physically lives
  review_date: <YYYY-MM-DD>               # shelf-life; the profile returns to the calendar rather than rotting
  provenance:
    - {kind: <doc|code|ruling>, repo: <id>, ref: <path:line or ADR id>}
```

## 2.4 · Admission-safe by construction — the paste-ready header the schema mandates

Any artifact emitted under a profile carries this header block **verbatim in shape**, first in file
(two-space indent here is this memo's non-admission guard only — a real artifact starts these at column 0):

```
  # Codex Review — <topic>

  **Date:** <YYYY-MM-DD>
  **Branch:** `<branch-name-exactly-as-the-merge-subject-will-name-it>`
  **HEAD:** `<7-40 hex>`
  **Diff range:** `main..<branch>`
  **Codex version:** <codex-cli x.y.z>
  **Model used:** `gpt-5.6-terra`
  **Review profile:** code
  **Mode:** diff-review
  **Tally:** 0/0/0/0 <!-- Critical/High/Medium/Low -->
```

Five constructive properties, each mapping to a numbered consequence in §2.1: the title admits the file (1); Branch and
HEAD both present so a rename or a rebase cannot orphan it (2); the tally is present and four-valued (3); exactly one
branch per file (4); nothing depends on the merge message (5). Lane A's artifact violates (1) and (3); lane H's
violates (4). **Both 08-18 failures are prevented by this block and nothing else is needed to prevent them.**

---

# ITEM 3 — the three drafted profiles + rollout · **CLEAR**

## 3.1 · `.dev-knowledge` — hub

```yaml
review_profile:
  repo: .dev-knowledge
  role: hub
  status: active
  reason: >-
    The hub AUTHORS the fleet's enforcement organs, so a defect here is a fleet-wide event rather than a
    repo-local one; it is also the only member whose review-artifact discipline is machine-checked
    (check_review_artifact_coverage is hub-only, audit.py:3218).
  lanes:
    reviewer: gpt-5.6-terra
    adversarial: gpt-5.6-sol
    adversarial_predicate: >-
      DRAFT, ruling needed (R5): any diff that adds or changes a GATE — a hook in .pre-commit-config.yaml,
      a check registered in audit.py's ALL_CHECKS, or a deploy carrier under deploy/ — plus any diff that
      changes a refusal posture (fail-open <-> fail-closed).
    heterogeneity: cross-vendor
  triggers:
    - {class: pre-merge-code-impact, cadence: per-merge, surface: code, instrument: /codex-review}
    - {class: pre-merge-doc, cadence: per-merge, surface: doc, instrument: /codex-review}   # [#333] doc-lane
    - {class: full-audit, cadence: monthly, surface: code, instrument: codex exec (full audit)}
    - {class: conformance, cadence: nightly, instrument: .claude/workflows/conformance-hub.js}
  severity: {fix_before_merge_floor: High}
  artifact: {class: codex, branches_per_artifact: 1, producer: wrapper-preferred}
  home: <R1>
  review_date: 2026-11-19
```

Notes. The doc-lane trigger is not decoration: the hub's code-impact predicate is `.py`/`.ps1` + two exact paths, so a
governance-only arc — an ADR, a PLAYBOOK section, a carrier manifest — is **not** code-impact and gets no pre-merge
review at all unless the doc lane is named. `[#333]` already built that lane; the hub profile is where it becomes
standing rather than per-plan. The `conformance` trigger records the organ that exists (`conformance-hub.js`, ARMED,
ARCHITECTURE Ch2:314) at the cadence the Routine actually runs — while noting that ARCHITECTURE Ch6 declares the
**nightly outcome loop BROKEN AT THE TRIAGE EDGE**: the digest is produced and nothing consumes it. A profile that
claimed a working nightly conformance loop would be asserting a repaired edge. It claims a producer only.

## 3.2 · `ai-council` — consumer *(hub-record derived — unverified against the repo)*

```yaml
review_profile:
  repo: ai-council
  role: consumer
  status: active
  reason: >-
    Deployed corpus 1.3.1 (ecosystem/deployed-versions.yaml, 2026-07-11). Its output is BINDING ADRs governing
    every Dev/ repo (ecosystem/registry.md), so its failure mode is a wrong decision propagating fleet-wide, not
    a runtime crash: review weight belongs on the debate/synthesis flow and on the CLI entry point, not on breadth.
  lanes:
    reviewer: gpt-5.6-terra
    adversarial: null
    adversarial_predicate: >-
      DRAFT: escalate to sol only for a change to the debate-orchestration flow itself (the path that decides
      what an ADR says), where a same-architecture reader is most likely to converge with the author.
    heterogeneity: cross-vendor
  triggers:
    - {class: pre-merge-code-impact, cadence: per-merge, surface: code, instrument: /codex-review}
    - {class: full-audit, cadence: quarterly, surface: code, instrument: codex exec (full audit)}
  severity: {fix_before_merge_floor: High}
  artifact: {class: codex, branches_per_artifact: 1, producer: wrapper-preferred}
  focus: council flow correctness; ADR-output fidelity; the `council` CLI entry point
  home: <R1>
  review_date: 2026-11-19
```

## 3.3 · `corp-monorepo` — consumer *(hub-record derived — unverified against the repo)*

```yaml
review_profile:
  repo: corp-monorepo
  role: consumer
  status: active
  reason: >-
    The largest consumer surface (deployed corpus 1.2.0, held deliberately by the ADR-102 gate_rev_ahead ruling
    #336 — NOT a lapsed deploy). It touches OneDrive/SharePoint-synced material and corporate source data, which
    are precisely the two Critical-band items the global reviewer config already enumerates (synced-dir safety,
    API keys) — so its severity weight sits at the Critical band by the checklist that already exists.
  lanes:
    reviewer: gpt-5.6-terra
    adversarial: gpt-5.6-sol
    adversarial_predicate: >-
      DRAFT: any diff touching a synced-directory write path, a credential path, or a SQL query surface.
    heterogeneity: cross-vendor
  triggers:
    - {class: pre-merge-code-impact, cadence: per-merge, surface: code, instrument: /codex-review}
    - {class: full-audit, cadence: monthly, surface: code, instrument: codex exec (full audit)}
  severity: {fix_before_merge_floor: High}
  artifact: {class: codex, branches_per_artifact: 1, producer: wrapper-preferred}
  focus: synced-dir safety; secret handling; parameterized SQL; extraction-pipeline data integrity
  home: <R1>
  review_date: 2026-11-19
```

## 3.4 · The six pre-deploy members — one shared named-absence stanza

Drafted here because `[#82]`'s Done-when has two clauses and this is the second one; without it the row's denominator
stays 3/9 no matter how good the three profiles are.

```yaml
review_profile_absent:
  repos: [corp-ops, corp-sca-time-automation, demo-prep, life-architect, terminal-setup, win-tooling]
  status: named-absent
  reason: >-
    Declared ADR-104 fleet members with role pre-deploy: no deploy record in
    ecosystem/deployed-versions.yaml, so they are rendered "skipped (pre-deploy)" by the fleet walk and carry
    no methodology corpus to review against. Each member's own `reason:` in parity-surfaces.yaml `fleet:` is
    the per-repo statement of record and is NOT restated here. A member gains a profile at the same moment it
    gains a deployed-versions entry and its role flips to `consumer` — the identical onboarding trigger the
    parity manifest already documents.
  review_trigger: on role flip pre-deploy -> consumer
```

## 3.5 · Rollout order

Land the **hub profile first and alone**, because the hub is the only member where every clause is machine-checkable
today — `check_review_artifact_coverage` is hub-only, so the hub is where a wrong profile shows up as a WARN instead of
as silence, and it is also where the two known 08-18 failures happened. Land the **pre-deploy named-absence stanza
second**: it is six members of the nine at the cost of one block, it moves the row's denominator from 3/9 to 7/9, and
it cannot be wrong in a way that costs anything, since it asserts only what `parity-surfaces.yaml` already declares.
Land the **two consumer profiles last, and only after a seat with sibling-tree access has read each repo** (§0 evidence
boundary) — they are the two clauses that assert something about a tree the hub cannot see, and a consumer profile is
recorded intent rather than a checked property, so an unverified one buys the appearance of coverage without the fact.
Nothing in this order requires the `[#499]` reader repair to land first; equally, none of it substitutes for that
repair — profiles make **new** artifacts admission-safe, and the two immutable 08-18 artifacts stay unlinked either way.

---

# ITEM 4 — ruling vs mechanical adoption · **CLEAR**

## 4.1 · Needs a ruling

**R1 — WHERE a profile lives ("its stated home").** Three candidates, and they are not equivalent.
*(a)* a hub-side `ecosystem/review-profiles.yaml`, one concern per file on the `tool-versions.yaml` / `deployed-versions.yaml`
precedent — the only candidate a hub lane can land alone, and the only one that keeps all 9 members in one countable
place; *(b)* a per-repo `.methodology.yaml` key — closest to the existing declaration grammar, but a consumer's copy is
outside hub write scope and needs a deploy carrier to arrive; *(c)* a `parity-surfaces.yaml` surface row — makes the
profile a *parity* property, which promotes it to fleet doctrine and invites the same objection D8 raised against
Route 1 today (enshrining before proving). **Recommendation: (a) now, (b) later as an override layer.** This is a
ruling and not a preference because the choice decides whether `[#82]` can close from the hub at all.

**R2 — is `fix_before_merge_floor: High` doctrine-wide or per-repo?** The three drafts all say High, which makes the
field look decorative. It is worth ruling explicitly one way: doctrine-wide (delete the field, state it once in
PLAYBOOK) or per-repo (keep it and expect divergence). A field that is per-repo in shape and constant in practice is
how a schema starts lying.

**R3 — the title-predicate enum.** The admitted-title set has exactly one member while the tree carries more than one
review-artifact shape (N5 §4.2). This pack **deliberately does not widen it** — it makes new artifacts conform to the
existing predicate instead. Whether the reader should also admit other shapes is `[#499]`-adjacent and belongs to the
row N5 §4.5 drafted; smuggling it in as a profile field would change an enforcement surface under cover of a
convention doc. Named here so the omission is visible rather than silent.

**R4 — is a hand-authored review artifact admissible at all?** §1.3's discriminator is producer, not reviewer. Ruling
options: (i) `/codex-review` is the sole sanctioned producer and a hand-authored artifact is a process deviation;
(ii) hand-authored is fine provided it carries the §2.4 header. The drafts assume (ii) — `producer: wrapper-preferred`
— because the batch lanes that produced both failures were operating under contracts that told them to write the
artifact themselves. Ruling (i) would instead require those contracts to change.

**R5 — the adversarial predicate.** "Adversarial=sol when stakes warrant" is current doctrine and is not checkable as
written; each draft above proposes a concrete predicate marked DRAFT. Either ratify per-repo predicates or rule that
the field stays judgment-scoped and is documented as such — but not both silently.

**R6 — who executes a consumer's profile.** CLAUDE.md §5 rule 4 forbids the hub from driving a child repo's state, so
a hub-recorded consumer profile is a **record of what that repo's own sessions run**, never something the hub runs.
`[#82]`'s Done-when says "at its stated home", which is compatible with a hub-side record — but the ruling should say
so out loud, because the alternative reading (each repo hosts its own) makes R1(a) non-compliant.

## 4.2 · Mechanical adoption — no ruling required

Each of these is already ruled or already measured; a profile that states them is transcribing, not deciding.

- `reviewer: gpt-5.6-terra`, exact model strings, never a bare `gpt-5.6` — PLAYBOOK §16, `[#469]`.
- Severity vocabulary `Critical/High/Medium/Low` and the per-band checklists — `codex/AGENTS.md`.
- Diff review reports **Critical + High only**; full audit reports all four — `codex/AGENTS.md` §"Review Modes".
- Full-repo audit cadence is by repo complexity, whole-`src/` scope, distinct from per-change review — PLAYBOOK §17.
- Verdict enum `MERGE-CLEAN` / `FIX-BEFORE-MERGE (itemized)` / `BLOCK (reason)` — the review-lane contract of record.
- Artifact home `docs/audits/`, name grammar `<YYYY-MM-DD>-<class>[-<slug>]`, class `codex`, all-lowercase kebab, and
  the fact that `review` is **not** an enum member — ADR-101 R3/R4, `scripts/validate_hermetization.py`.
- The §2.4 header block in full — every line of it is dictated by a regex quoted in §2.1.
- One branch per artifact — a direct consequence of `.search` first-match-wins, measured at n=1 divergence today.
- Code-vs-doc routing by extension guard, doc-lane pinned to terra — `[#333]`, PLAYBOOK §16.
- The pre-deploy named-absence stanza's content — it restates `parity-surfaces.yaml` `fleet:` reasons and adds nothing.

---

# 5 · Limits, and what was actually run

## 5.1 · What this pack does not do

It lands no file, edits no check, and enforces nothing — the contract's `NOT` clause, honored literally. It does not
regenerate `docs/audits/README.md`. It writes no BACKLOG row. It does not close `[#82]`: 0 of 9 members carry a profile
before this pack and 0 of 9 carry one after it, because a draft in an audit artifact is not a recorded profile at a
stated home. What it produces is the schema, three drafted profiles, a named-absence stanza covering six more members,
and the six rulings that stand between the drafts and a close.

## 5.2 · Honest limits

The consumer profiles are hub-record derived and unverified (§0). The severity floors are proposed, not measured
against either consumer's history. The `full-audit` cadences (monthly / quarterly) are the first values anyone has
written down for these repos — PLAYBOOK §17 says "cadence by repo complexity" and nothing has ever instantiated it, so
these are defensible defaults rather than derived numbers, and R2's ruling should treat them as such. And the whole
pack inherits `check_review_artifact_coverage`'s own honest limit: an admission-safe header proves an artifact exists,
is linked, and is tallied — never that the review happened or found anything true.

## 5.3 · Commands run in this container (gates were NOT armed here)

```
  # the admission census of §2.2 — read-only, reproducible from repo root:
  python3 - <<'PY'
  import re, pathlib
  TITLE=re.compile(r"(?m)^# Codex Review\b"); BRANCH=re.compile(r"(?m)^\*\*Branch:\*\*[ \t]*`?([^`\s]+?)`?[ \t]*$")
  HEAD=re.compile(r"(?m)^\*\*HEAD:\*\*[ \t]*`?([0-9a-f]{7,40})`?")
  TALLY=re.compile(r"(?m)^\*\*Tally:\*\*[ \t]*(\d+)/(\d+)/(\d+)/(\d+)\b")
  adm=[p for p in sorted(pathlib.Path("docs/audits").glob("*.md"))
       if TITLE.search(p.read_text(encoding="utf-8",errors="replace"))
       and (BRANCH.search(p.read_text(encoding="utf-8",errors="replace"))
            or HEAD.search(p.read_text(encoding="utf-8",errors="replace")))]
  print(len(adm), sum(1 for p in adm if TALLY.search(p.read_text(encoding="utf-8",errors="replace"))))
  PY
```

**Non-admission self-check on this file** — the property claimed in the banner, verified rather than asserted; both
counts must be 0, and the result is recorded in the STOP packet rather than here, because this file is immutable once
committed and the check runs against its final bytes.

**Gate posture:** `pre-commit` is not installed in this container, so `audit-health`, `validate-hermetization`,
`audit-index-freshness` and the two pre-push organs did **not** run on this lane's commits. `validate_hermetization`'s
Rule B was satisfied by construction (class `technical`, all-lowercase kebab, both filenames); anything else this lane
would have tripped is unmeasured, and the integrator should expect the hub gates to run for the first time at the merge.

## 5.4 · One owed integrator act, measured rather than assumed

`python scripts/gen_audit_index.py --check` **exits 1 against this lane's tree**: `docs/audits/README.md` is stale.
It was **fresh before this lane** — the index already lists every 2026-08-19 artifact that predates it — so the
staleness is caused by exactly the two files this lane adds and by nothing else. The contract's `**No index
regeneration.**` clause is honored literally rather than reinterpreted, so the regeneration is **owed to the
integrator** at the merge, where the `audit-index-freshness` pre-commit gate will demand it:
`python scripts/gen_audit_index.py --write`. Stated here so the debt is a named hand-off rather than a surprise
red gate. `python scripts/validate_hermetization.py` exits 0 on the same tree.
