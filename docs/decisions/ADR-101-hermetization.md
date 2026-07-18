# ADR-101: Hermetization — sanctioned top-level set, per-class name grammar, refusal gate (d.i/d.ii/d.iii)

- **Status:** Accepted (ratified 2026-07-11 — operator ruling via the 2026-07-11 morning verdict sheet [M1]; the three embedded ratification-decisions are resolved in the **Ratification amendment (2026-07-11)** below)
- **Date:** 2026-07-10 (drafted) · 2026-07-11 (ratified)
- **Decision tier:** Architecture (Path A — operator ruling; drafted lane B 2026-07-10, ratified 2026-07-11 by operator — the lane never self-accepts, ADR-94)
- **Amends:** ADR-34 (file-naming convention) — extends its `Audits / handoffs` naming row into the `<date>-<class>-<slug>` grammar AND realizes its ~2.5-month-deferred "pre-commit hook validates new file paths" enforcement (ADR-34 §Enforcement / §Follow-ups). Reclassified from *Related* to *Amends* at ratification (verdict sheet B1c): ADR-101 modifies ADR-34's operative naming row and delivers its deferred gate, which is an amendment, not a mere relation.
- **Related:** ADR-34 (file-naming convention — this **extends** its `Audits / handoffs` row into `<date>-<class>-<slug>` and **realizes** its long-deferred "pre-commit hook validates new file paths (follow-up)" — ADR-34 §Enforcement/§Follow-ups), ADR-60 (docs/ folder taxonomy — the genre-folder roles this seals), ADR-98 (intake pipeline — genre-folder-first, `docs/intake/README.md` §4), ADR-36 (audit-tool architecture — cites `docs/audits/` structurally, the tree d.iii names), CLAUDE.md §4 (Naming conventions), protocols/HANDOFF_PROCESS.md §16 (functional mode-boot), #300 (this decision's backlog task), #299 (runbook Layer-6 fix landed in-place — the d.i keep basis), #301 (session-plan artifact class — "bundle-resident only, no new top-level docs class"), #131 (docs/runbooks created without surfacing — the d.i root-cause), #190 (#300's kill-candidate)
- **Decommission:** the committed `docs/handoffs/2026-07-07-dev-knowledge-functional/` bundle — obsoleted by the d.ii ephemeral-mode-boot ruling; removed in the one migration pass (operator-signed, **post-ratification**), tracked under #300. **This draft removes nothing.**
- **Source:** 2026-07-08 incident-recovery arc (operator remediation prompt) → BACKLOG #300; night-hygiene audit `docs/audits/2026-07-09-night-hygiene-audit.md` §S3 (the d.iii ruling shape) + §S4-3 (superseded-era bundles); 2026-07-10 architect bundle `PLAN.md` §C (D1 demoted to interim) + `SUPPLEMENT.md` A2/A4 (the d.ii/d.iii open items). Drafted lane B (EPIC I peg), commit-and-STOP, no merge.

<!-- Decommission: if non-empty, each listed item becomes a BACKLOG entry and stays open until removed. A decision is not complete while its Decommission items remain. -->

## Context

The repo tree accreted without a sealing rule. It carries **14 top-level directories** and **~19 top-level files**, and `docs/` holds **6 genre folders** (`archive/ audits/ decisions/ handoffs/ intake/ runbooks/`). One of those, `docs/runbooks/`, entered the tree **on #131's task text without an explicit operator surfacing** — a recurring "keep or move?" open question across the architect handoffs (`2026-07-09-dev-knowledge-architect/RESIDUAL.md`) that the 2026-07-10 bundle **demoted to interim-keep**, deferring the final ruling here (D1 → "hermetization ADR d(i)").

**ADR-34 already anticipated the enforcement and never built it** — its §Enforcement names "Now (active): pre-commit hook validates new file paths against conventions table (separate task, follow-up)" and its §Follow-ups repeats "Pre-commit hook implementation in .dev-knowledge (small task, separate session)." That follow-up is ~2.5 months overdue; #300 is where it lands.

Meanwhile audit-class slugs proliferated. The 2026-07-09 night-hygiene audit **§S3 quantified `docs/audits/`** (measured basis, verified live this lane):

- **41 already class-led** (a class token directly after the date): `codex` ×34, `fresh-eyes` ×4, draft-tier ×2, census-amendment ×1.
- **31 trivially compliant** (the whole slug *is* the class — recurring reports): `ecosystem-audit` ×16, `conformance-nightly-digest` ×10, `changelog-review` ×5.
- **~130 subject-before-class** (`-audit`, `-discovery`, `-verification`, `-inventory`, `-census`, … buried at slug-end) and **4 class-less** (no class token at all — a strict regex cannot classify these without opening the file, S3-3).

**Retroactive enforcement would rename ~65% of the corpus for near-zero gain** — the index already disambiguates by date, and ~78% of audit citations live in immutable/append-only docs that can never be re-pointed (ADR-100). §S3's honest ruling shape is therefore **prospective-only + grandfather existing + a canonical CLASS enum** (not just a position rule — "or proliferation continues under the new grammar").

#300 folds three sub-rulings (d.i/d.ii/d.iii) that share **one doctrine: seal the tree; a new artifact class gets a genre folder; within a genre folder, names follow a controlled grammar.**

## Decision

### 1. Sanctioned top-level set (CLOSED, two-tier)

The tree is **hermetic**: its top level is a closed set. Growing it is a deliberate, surfaced act (an amendment to this ADR or an explicit operator ruling), never a drive-by folder.

- **Tier-1 — repo root.** Sanctioned directories: `.claude/ .claude-plugin/ .vscode/ codex/ config/ deploy/ docs/ ecosystem/ logs/ plugins/ protocols/ scripts/ templates/ tests/`. Sanctioned file **classes** (not an enumerated whitelist — a class rule): living docs `UPPERCASE.md` (`VISION ARCHITECTURE CLAUDE CONTRIBUTING JOURNAL LESSONS BACKLOG`); dotfile/tool config (`.gitignore .gitattributes .pre-commit-config.yaml .pre-commit-hooks.yaml .ruff.toml .worktreeinclude .dev-knowledge.code-workspace`); build/package manifests (`package.json package-lock.json pyproject.toml`).
- **Tier-2 — `docs/` genre folders.** Sanctioned: `archive/ audits/ decisions/ handoffs/ intake/ runbooks/`.
- **Refused:** any **new** Tier-1 top-level directory, any **new** Tier-1 top-level file outside a sanctioned class, or any **new** `docs/<genre>/` folder. A new artifact class **must** nest under `docs/<genre>/` (genre-folder-first — ADR-98, `docs/intake/README.md` §4), and a genuinely new genre folder is surfaced *before* creation — directly fixing the #131 root-cause.

### 2. Per-class name grammar + canonical CLASS enum (d.iii)

- **Grammar** for `docs/audits/`: `<YYYY-MM-DD>-<class>-<slug>.md`, where `<class>` ∈ the CLOSED enum below and `<slug>` is kebab-case **allowing `.`** (S3-1 carve-out: `.dev-knowledge`, `v3.4` are meaningful repo/version tokens; a rename would be lossy). A pure recurring report may omit `<slug>` (the degenerate `<date>-<class>.md`, e.g. `2026-06-14-ecosystem-audit.md` — already the norm for the 31 trivially-compliant files).

- **CLOSED CLASS enum (drafted; operator ratifies the exact list).** Three axes, union intentional so the ~72 already/trivially-compliant files stay valid and the high-volume automated reports stay conforming going forward:
  - *audit-type (semantic — the EPIC-I declared set):* `technical` · `functional` · `qa` · `census` · `verification`
  - *recurring/automated report-family:* `ecosystem-audit` · `conformance-digest` · `changelog-review`
  - *reviewer-origin:* `codex-review`
  - *incident:* `incident-evidence`

  That is the **ruled ten**. The enum is **CLOSED as ratified** — the **anti-bloat clause (operator-directed): adding a class is a one-line ADR amendment (deliberate), never ad-hoc growth via convention drift.**

- **Token-form reconciliation (live-verified; resolved by the refusal-gate build).** Three enum tokens are family *labels*; the on-disk generator token differs, and existing files are grandfathered regardless:
  - `codex-review` — on-disk token is bare **`codex`** (34 files). 
  - `conformance-digest` — on-disk token is **`conformance-nightly-digest`** (10 files) + 2 variants.
  - `ecosystem-audit` (16) and `changelog-review` (5) match on-disk exactly.
  The gate build (§3) reconciles enum-token ↔ generator-output in one direction — **either** the generators adopt the canonical token **or** the enum adopts the on-disk token — so the "stays conforming, zero rename" property is *made* true rather than assumed. This is an implementation choice at build time, not a re-opened policy question; grandfathering holds either way.

- **`fresh-eyes` — [RATIFICATION-DECISION].** A reviewer-origin family with real corpus evidence (**4 files**, all `2026-06-01-fresh-eyes-*`, exact on-disk token) but **beyond the ruled ten**. Per the anti-bloat clause, it is **not** silently added — the operator rules at ratification whether the enum is 10 or 11. (Recorded so the clause's first test case is not this ADR's own draft.)

### 3. Refusal gate (MECHANISM spec; the build is a named follow-up)

A new `language: system` **local pre-commit hook** (`entry: python scripts/validate_hermetization.py`, name indicative), **prospective-only** — it inspects only **ADDED** paths (`git diff --cached --name-status`, filter `A`); existing files are grandfathered and never checked.

- **Rule A (top-level seal).** An added path that introduces an unsanctioned Tier-1 top-level entry, an unsanctioned Tier-1 top-level file class, or a new Tier-2 `docs/<genre>/` folder → **BLOCK**.
- **Rule B (audit grammar).** An added `docs/audits/*.md` whose name fails `<date>-<class>-<slug>` with `<class>` **whole-token matched against the CLOSED enum** (longest-match, **not** naive hyphen-split — the multi-word tokens `ecosystem-audit`/`conformance-nightly-digest`/`codex-review`/`incident-evidence` require this; a split-on-first-hyphen validator is undecidable, S3-3) → **BLOCK**.
- **Name-shape only.** The gate validates the *filename shape* — never date-*accuracy*: filename date = content/session date and lags git-add date by ~15–19% by design (S3-4), so any future "misdated" detector must diff the content-header date, **never** `git log`.
- **Follow-up, not built here.** The ADR **specs** the gate; the validator + `.pre-commit-config.yaml` wiring is a **BACKLOG task the ADR names** (filed at ratification), realizing ADR-34's deferred enforcement — capture precedes construction (ADR-70 pattern). Bypass parity with peer hooks: `--no-verify`.

### 4. d.i — `docs/runbooks/` location: KEEP + sanction

The D1 interim closes as **keep**. `docs/runbooks/repo-onboarding.md` stays **in-place** — the #299 Layer-6 verify fix just landed there, so a move now is churn without benefit — and `docs/runbooks/` is ratified as a Tier-2 genre folder (§1). The process defect that created it unsurfaced (#131) is fixed structurally: under the §3 gate, the *next* genre folder is a surfaced, gated act, not a silent one.

### 5. d.ii — mode-boot bundles: EPHEMERAL; sweep functional, leave superseded

- **Policy.** Functional/epic **mode-boot bundles are ephemeral** — generate → paste into the mode chat → remove; **never committed.** This matches the operator runbook doctrine (`docs/handoffs/README.md` §Functional: one `FUNCTIONAL_BOOT.md`, "pasted alone into a fresh functional-architect chat"). Mode-boots are a transient carrier, not an artifact class — so they get **no genre folder** and leave no committed trace.
- **The stray.** The pre-existing committed `docs/handoffs/2026-07-07-dev-knowledge-functional/` bundle is the one instance that leaked into the tree (committed `4ed3657`, a prior session; already flagged, not actioned — `JOURNAL.md` 2026-07-08). It is removed in **one migration pass, operator-signed, no drive-by deletion** (core-invariant #3). Named in `Decommission:` above; tracked under #300.
- **Superseded-era bundles STAY.** The superseded-era **pre-v5 handoff bundles** (v3.2 + v4, 2026-05-09→2026-06-10) remain as by-design historical: §S4-3 found **no rule mandates archiving them**, and `docs/handoffs/archive/` holds a *different* artifact class here. They are grandfathered in place, not swept. *(Their exact count is flagged, not asserted — see "Inputs not fully pinned" below.)*
- **Pass scope (operator-ratified 2026-07-10).** The migration pass grandfathers-**forward** everything created **before ratification** — any mode-boot bundle minted mid-flight (e.g. a concurrent session's close-out) lands under this convention and is swept by the same single pass. There is **no sequencing coupling** between this ADR and any in-flight session.

### 6. d.iii — prospective-only + grandfather + CLOSED enum

The §S3 ruling shape, formalized by §2–§3 above: the grammar and enum are **prospective-only**; the ~130 subject-before-class and 4 class-less files are **grandfathered** — **no retroactive rename.** The value is the *canonical CLOSED enum* that stops bespoke-suffix invention going forward, not a position rule applied backward over a corpus the date-index already disambiguates.

## Consequences

- **Easier:** the tree is sealed — no silent folder sprawl (the #131 failure mode); a new artifact class becomes a surfaced, gated decision; the high-volume nightly reports stay conforming with zero rename; audit-class vocabulary is bounded and drift-resistant; ADR-34's 2.5-month-overdue enforcement finally has a home.
- **Cost / follow-ups (named, not executed here):** (a) **build** the refusal-gate validator + wire the pre-commit hook (§3), including the token-form reconciliation (§2); (b) the d.ii **one migration pass** — remove the committed functional bundle, operator-signed (§5). Both file to BACKLOG **at ratification** (this draft edits no BACKLOG task and moves no file). Recording the rule now / building later follows ADR-70's capture-precedes-construction pattern.
- **What this does NOT decide:** retroactive renames (explicitly rejected); the exact superseded-era bundle count (flagged); whether `fresh-eyes` joins the enum as an 11th token (ratification-decision, §2); the token-form reconciliation *direction* (implementation, §2); child-repo propagation (hub-only, n=1 — the gate is HUB-ONLY until a P6 rollout, mirroring `roster-freshness`/`claude-rosters-freshness`); whether draft-proposal artifacts (`YYYY-MM-DD-DRAFT-…-proposal.md`) join the enum (left grandfathered/separate — a pre-ADR staging genre, not an audit).

## Alternatives considered

- **Retroactive enforcement** — rename the ~65% subject-before-class + class-less corpus to `<date>-<class>-<slug>`. Rejected: near-zero gain (the index disambiguates by date), and it churns immutable/append-only citations that can never be re-pointed (ADR-100's ~78% finding). §S3's measured basis makes prospective-only the honest call.
- **Semantic-only 5-class enum** (`technical/functional/qa/census/verification`, the EPIC-I sketch). Rejected: it leaves the *actual* high-volume families (`ecosystem-audit`, `conformance-nightly-digest`, `changelog-review`, `codex`) non-conforming — even the already-compliant files would break, and every nightly report would need forcing into a semantic bucket.
- **Open / positional class rule** (a position convention, no controlled vocabulary). Rejected: undecidable by regex without opening the file (S3-3's 4 class-less cases), and it invites the very bespoke-suffix proliferation d.iii exists to stop.
- **Empirical-families-only enum** (drop the semantic axis, keep just the on-disk families). Not adopted: loses the clean semantic partition operator-authored human audits need; the reconciled union keeps both and pays for it only with the anti-bloat clause.
- **Move `docs/runbooks/`** to `protocols/` or a bundle-resident home. Rejected: the #299 fix just landed in-place; a relocation is churn that re-points references for no structural gain.
- **Archive the superseded-era bundles in the same pass.** Not chosen: §S4-3 judged them fine as historical, `archive/` holds a different class here, and sweeping ~28 dirs the audit called by-design violates the "minimal, no drive-by" spirit of the one pass.

---

## Ratification amendment (2026-07-11)

> **In-file amendment marker (CLAUDE.md §5 item 3 / ADR-94).** The decision body above is preserved verbatim as drafted; this section records the operator's ratification rulings on the three decisions the draft deliberately left open, and folds the audit-file casing rule + required header block into the decision. Ratified via the 2026-07-11 morning verdict sheet (Section B1, architect-co-signed, operator-ratified by launching the execution).

### R1 — `fresh-eyes` joins the CLOSED enum as the **11th** class (resolves §2 `[RATIFICATION-DECISION]`)

`fresh-eyes` is **IN**. Basis: real corpus evidence (**4 files**, all `2026-06-01-fresh-eyes-*`, exact on-disk token) and it is a genuine *reviewer-origin* family, not a bespoke one-off. Adding it is the anti-bloat clause's first legitimate test case (a deliberate, evidence-backed inclusion), not convention drift. The ruled ten becomes the **ruled eleven**.

### R2 — Token-form direction: the **enum adopts the on-disk forms** (resolves §2 token-form reconciliation)

The enum adopts what three repos already write on disk — **zero rename**:
- `codex-review` → the enum token is **`codex`** (34 hub + 4 corp + 13 ai-council files).
- `conformance-digest` → the enum token is **`conformance-nightly-digest`** (10 hub + 18 corp; the rarer `conformance-baseline-digest` / `conformance-rerun-delta-digest` stay grandfathered variants).
- `ecosystem-audit`, `changelog-review` — already exact on-disk matches, unchanged.

This makes ADR-101's "stays conforming, zero rename" property **true** rather than assumed; grandfathering holds either way. It is an implementation choice, not a re-opened policy question.

### R3 — CLOSED CLASS enum, as ratified (the ruled **eleven**)

Whole-token **longest-match** (never split-on-first-hyphen — the multi-word tokens require it):
- *semantic:* `technical` · `functional` · `qa` · `census` · `verification`
- *recurring/automated (on-disk forms per R2):* `ecosystem-audit` · `conformance-nightly-digest` · `changelog-review`
- *reviewer-origin (on-disk forms per R1/R2):* `codex` · `fresh-eyes`
- *incident:* `incident-evidence`

Adding a class remains a **one-line ADR-101 amendment** (deliberate), never ad-hoc convention drift.

### R4 — Casing rule (folded from verdict sheet §4b; the operator's uppercase concern)

Every `docs/audits/*.md` name is **all-lowercase kebab-case**, everywhere — date, class, and slug. **No `UPPERCASE`, no `_underscore_`, no `CamelCase`.** Sole charset carve-out: a literal `.` inside the slug when it is a meaningful repo/version token (`.dev-knowledge`, `v3.4`) — a rename there would be lossy (S3-1). This is the rule that fixes the cross-repo divergence the census found (corp-monorepo's UPPERCASE `_AUDIT_`/`_BRIEF_` family, actively growing for lack of a gate). The §3 refusal-gate (Rule B) enforces it prospectively.

### R5 — Required header block (folded from verdict sheet §4b)

Every audit file opens with this minimal block (dogfooded by both 2026-07-11 outputs):

```
# <Title>
- **Class:** <class> (ADR-101 enum) · **Date:** YYYY-MM-DD
- **Source-session:** <run / lane / HEAD or session context>
- **Status:** <PROPOSAL-ONLY | complete | …>
```

(Model-in-effect is recommended for unattended runs, per ADR-80 §5 silent-swap doctrine.)

### R6 — Enforceable home + named follow-up

- **Author-facing skeleton:** `templates/audit-template.md` (created this arc, peer of `templates/intake-template.md`) carries the filename grammar, the R4 casing rule, the R3 enum, the slug rules, and the R5 header block as a fill-in skeleton.
- **The rule's enforceable home** is this amendment (R3/R4/R5) feeding the §3 refusal-gate.
- **Named follow-up, filed at ratification:** build the refusal-gate validator + wire the HUB-ONLY pre-commit hook (§3 Rule A+B) — **BACKLOG #306**. Consumer carrier (floor/plugin) is the P6 rollout, not now. Capture-precedes-construction (ADR-70).
- The §5 d.ii one migration pass (remove the committed functional bundle, operator-signed) stays tracked under **#300**; this ratification does not itself remove the bundle.

## Amendment — 2026-07-13 (section-9a execution: `.methodology.yaml` joins the section-1 sanctioned Tier-1 file classes; [#328])

**Trigger (settled ruling, executed here — not a new decision).** The intake #12 ownership manifest was SETTLED at the 2026-07-12 A0 promotion with the operator's section-9a ruling: the hub carries its OWN root `.methodology.yaml` as a fleet member, no implicit source-role exception (the DRAFT's inverse rule listing the file as forbidden-in-hub was SUPERSEDED in that same reconciliation — `docs/intake/2026-07-11-tech-ownership-manifest.md`, Tier-1 A0-promotion note). Section 1's dotfile/tool-config class predates that ruling and omits the file, so the section-3 Rule-A gate refuses the very add the ruling mandates (`SANCTIONED_TIER1_FILES` is a closed set grown only by ADR-101 amendment — this is that amendment).

**Decision.** `.methodology.yaml` is ADDED to the section-1 sanctioned Tier-1 file classes (dotfile/tool config). Lockstep in the SAME commit: `scripts/validate_hermetization.py` `SANCTIONED_TIER1_FILES` += `.methodology.yaml`, a `tests/test_validate_hermetization.py` case pins the sanction, and the [#328] build lands the hub `.methodology.yaml` itself (census row W3-15 resolved; the hub file is read by the same `enforcement_coverage.read_allowlist` the consumers' files already flow through, now also consumed by `scripts/fleet_parity.py` per FR-4).

## Amendment — 2026-07-18 (two-tier new-path rule: convention-compliance IS authorization)

- **Source:** Operator ruling, relayed from corp-monorepo 2026-07-19 (binding); recorded here on the session date 2026-07-18 (the corp session date is the provenance label, quoted, not the record date). Refines this ADR's own refusal-gate invariant (§1 tree-seal + §3 gate) — recorded here as an **in-file amendment** per **ADR-94** (in-file amendment = own-invariant refinement, not a new domain) and **ADR-34** (the naming parent this ADR amends). By limited **analogy to ADR-102 §1** (which likewise preferred *extending an authoritative surface* — `parity-surfaces.yaml` — over spawning a parallel register), amending this ADR is preferred over a new one, and the standalone registry proposed below **externalizes this ADR's own frozensets into a single source of truth**, distinct from a duplicate register — ADR-102 is an analogy, not directing authority (ADR-94 is the amendment authority).
- **Decision tier:** Path A — an operator-settled refinement of an existing invariant; no Council convene.

**Universal rule (fleet-wide).** *Status (layered): the **rule is in force now** by operator ruling (relayed from corp-monorepo 2026-07-19, binding) — including the tier-1 proceed-with-citation executor behavior. Two follow-ups mechanize/persist it and **neither is a precondition**: **#345** mechanizes the §3 gate (registry-driven validation, replacing the bare CLOSED set); **#346** persists the executor rule into `~/.claude` so future sessions inherit it without reading this ADR. Two standing riders: (a) **any ambiguity about which pattern applies = tier 2 = STOP** (unchanged); (b) the **citation in the log/commit is MANDATORY for every proceed — no citation, no proceed**.* The rule: block convention-**VIOLATING** creations and **never** convention-**COMPLIANT** ones — *convention-compliance IS the authorization.* Two tiers:

1. **Pattern-sanctioned new paths** — a new **file** matching a **codified, citable** convention. The **currently-effective set** (each with an *existing* governing source, actionable today without the #345 registry): ADRs at `docs/decisions/ADR-NN-{slug}.md` (ADR-34); intake docs under `docs/intake/` (ADR-98); `docs/audits/*.md` per the §2 / R3 / R4 grammar; JOURNAL entries. The #345 registry is what makes this set **machine-checked and extensible** — a class **not** covered by a codified convention today is **tier-2** (ambiguity → STOP), not pattern-sanctioned. For a covered class the executor **derives the path, CITES the governing source in the log/commit message, and PROCEEDS** — **no per-instance operator STOP** (the citation is the audit trail). **Path authorization is not content authorization** — creating an ADR/intake file at its sanctioned path does not approve the decision or content inside it.
2. **Unsanctioned paths** — any **new FOLDER**, any file matching **no** codified pattern, or any **ambiguity** about which pattern applies: **operator authorization required; absent → STOP/block.**

**Folder creation stays hard-gated in ALL cases** — this is the **doctrine** (operator ruling): every new folder is surfaced *before* creation. The **current mechanism** enforces it for the seal §1 / §3 Rule-A already cover — new **Tier-1** dirs and new `docs/<genre>/` genres (unchanged); extending gate coverage to **deeper sub-folders** (e.g. a new folder under an existing sanctioned dir, which Rule-A does not catch today) is part of the #345 registry-gate build. No existing tier-seal is loosened.

**Repo application (.dev-knowledge hub).** This does **not** loosen the folder/genre seal — it corrects the over-blocking of convention-**compliant files**. The in-repo exemplar is the 2026-07-13 amendment above: a **bare CLOSED set** refused an operator-*mandated*, fully compliant add (`.methodology.yaml`), unblockable only by amending both this ADR and the frozenset allowlist in one commit — a manufactured false-positive (the same class as the #131 unsurfaced-`docs/runbooks/` root-cause, but from the opposite direction: too tight, not too loose). Corp-monorepo hit the same friction (operator-relayed: the deletion-manifest-template incident set the hard rule; an ADR-38 mid-run STOP on a *convention-compliant* path exposed the over-blocking). The fix moves the §3 gate from a **bare CLOSED set** → validating created paths against a machine-readable registry of sanctioned patterns (home + naming rule + governing-source pointer), so it **never blanket-blocks new paths**: a compliant path is recognized-and-allowed (the executor cites the registry entry), a violation is blocked. The **rule is in force now** (operator ruling); the **automated** gate that mechanizes it is the #345 build — until it lands, the rule is upheld by executor/reviewer discipline (cite-and-proceed / STOP), not yet by the registry-driven gate.

**Registry — DESIGN PROPOSAL (not built in this amendment).** A **standalone, single-responsibility** `ecosystem/<name>.yaml` (name avoids the token "sanctioned path", already overloaded by the core-invariant #1 OneDrive grant list). It **externalizes the frozensets** currently hardcoded in `scripts/validate_hermetization.py` (`SANCTIONED_TIER1_DIRS` / `SANCTIONED_TIER1_FILES` / `SANCTIONED_GENRES` / `AUDIT_CLASS_ENUM`) into data:

```
version: 1
patterns:
  - id: adr
    home: docs/decisions/
    name_rule: '^ADR-\d+-[a-z0-9.]+(-[a-z0-9.]+)*\.md$'
    folder: false
    source: {kind: adr, repo: .dev-knowledge, ref: ADR-34}
  - id: audit
    home: docs/audits/
    name_rule: '<YYYY-MM-DD>-<class>-<slug>.md'   # class ∈ closed enum (§2/R3), R4 casing
    folder: false
    source: {kind: adr, repo: .dev-knowledge, ref: ADR-101}
tier1_dirs: [...]          # externalized SANCTIONED_TIER1_DIRS
tier1_file_classes: [...]  # externalized SANCTIONED_TIER1_FILES
genres: [...]              # externalized SANCTIONED_GENRES
```

Reuses the ADR-103 `{kind, repo, ref}` provenance grammar (and the `scripts/fleet_parity.py` `_declaration_bad` predicate if it adopts `{reason, provenance}`). Consumed by a **refactored `validate_hermetization.py`** that reads the registry instead of the frozensets → **single source of truth**, collapsing today's four-surface lockstep (script + test + this ADR + `templates/audit-template.md`), and **generalizing naming validation beyond `docs/audits/`** to every registered class. Precedent: `ecosystem/doc-code-edge.yaml` / `ecosystem/disposition-register.yaml` (one-concern-per-file, `yaml.safe_load`, hand-edited, durable). **Replication-ready:** the schema lets a consumer carry **its own copy** (inherited methodology patterns + repo-local patterns); the `deploy/manifest-v*.yaml` carrier+component entry is the **P6 consumer rollout** (matching R6), not now. **Build-leg conditions (operator riders):** (a) the new registry-file creation carries an **explicit operator-authorization line** (it is itself a new path until this rule + the registry bootstrap themselves); (b) standalone schema, not folded into `parity-surfaces.yaml`.

**Fold-in — #344 Ask-2 (recorded, not built here).** The consumer hub-write guard (#344 Ask-2, NEEDS-RULING) must satisfy **both** constraints: **ALLOW** the RULING-W sanctioned write shape (consumer worktree/branch → report, ADR-36/41 2026-07-18) **AND** enforce this two-tier path rule (a compliant path proceeds; an unsanctioned path or any new folder → STOP). These are **orthogonal authorization axes** — path-*creation* authorization (this rule: compliance-via-citation) vs cross-boundary *write* authorization (#344 Ask-2's hub-ruling token for a consumer session writing into hub/global paths). Whether a registry citation satisfies, supplements, or is distinct from #344's token is part of **#344's** ruling, not resolved here. The guard's architecture is decided in **#344**, not here.

**Boundary (what this amendment does NOT carry).** This ADR is the **doctrine record**; the **gate** (`validate_hermetization.py`) and the **registry** (data) are hub validators. The **executor-behavior instruction** — that an agent MAY proceed-with-citation on a pattern-sanctioned path — is an **executable agent rule** and per CLAUDE.md §5 rule 7 belongs in `~/.claude/` with a `verify:` line; editing `~/.claude/` is global-infra (core-invariant #6, exception-with-ruling). The **behavior itself is authorized now** by this ruling; **#346 persists** it into `~/.claude` for durability (future sessions inherit it without reading this ADR) — a separate global ruling with its own `verify:` line, **not a precondition** for the rule being in force.
