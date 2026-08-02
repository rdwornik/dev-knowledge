# Night batch 2026-08-02 · lane L-D — currency & consistency audit

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-02 · **Slug:** night-batch-ld-currency-audit
- **Status:** PROPOSAL — read-only night batch, unattended. Nothing was regenerated, re-stamped,
  or fixed. Every finding is reported, not repaired.
- **Base:** `main` = `a02dd111`. Clone unshallowed to `2026-03-30`; `origin/automation/fleet-audit`
  fetched read-only (refs only — the working tree was verified clean before and after).
- **Method:** read-only. Generators run in `--check` mode only; no `--write` was issued.

---

## 1. Headline

**Six mechanical currency checks PASS. Three doc-currency findings survive verification, and two
in-lane findings were REFUTED before they reached this report.**

The mechanical layer (indexes, rosters, registries, generated artifacts) is in good order — the
regen-and-diff gates are doing their job. The rot is in **hand-written prose describing organs
that no longer exist**, which no gate covers.

---

## 2. Mechanical checks — all PASS

| # | Check | Verdict | Evidence |
|---|---|---|---|
| 1 | Intake statuses coherent | PASS | 19 docs; generated `docs/intake/README.md` Contents block matches on-disk `status:` frontmatter exactly |
| 2 | ADR index reflects **both** ADR-109 amendments | PASS | verified independently — see §3 |
| 3 | Audits index current | PASS | `gen_audit_index.py --check` exit 0; 360 files indexed |
| 4 | Ecosystem files consistent | PASS | `terminal-setup` row present `ecosystem/registry.md:31`; `doc-counts.md` "38 registered checks" matches the live registry — see §4 |
| 5 | Generated artifacts not stale | PASS | 7 generators, all with safe `--check` modes; audit-index and intake-tree verified current |
| 6 | GitHub-side state | PASS (reachable, not guessed) | see §5 |

### 3. ADR-109's two amendments — verified, not accepted on report

Both amendment markers exist in-file:

- `docs/decisions/ADR-109-*.md:287` — `## Amendment — 2026-07-31 (§4 DISCHARGED: the
  second-surface round-trip proof landed)`
- `docs/decisions/ADR-109-*.md:341` — `## Amendment — 2026-08-01 (the Related-line matrix-width
  gloss corrected: **9 governs**)`

And `docs/decisions/README.md:98` reflects **both** — it carries the F1 no-over-claim clause from
the first and, verbatim, `**AMENDED 2026-08-01** … **9 governs.**` from the second. This was the
gap the 2026-08-01 JOURNAL entry (f) recorded fixing (`16ebdeb0`); the fix is confirmed landed.

### 4. The "38 checks" claim — verified against the live registry

`ecosystem/doc-counts.md:14` declares **38 registered checks**. Parsing the `ALL_CHECKS` literal
in `scripts/audit.py:3309` yields **39** `check_*` tokens — of which one,
`check_mermaid_theme_directive`, sits inside a retirement **comment** (`retired 2026-07-05, ADR-51
amendment`). Live registered count is therefore **38**. **`doc-counts.md` is accurate.**

Recorded because the naive token count is off-by-one in the *alarming* direction, and a future
check written against it would produce a false FAIL. The two newest members are
`check_fleet_audit_replication` ([#460]) and `check_membership_agreement` ([#462]), both landed
this window.

### 5. GitHub-side state — REACHABLE, and it confirms the local picture

Queried live via the GitHub API from the container (not inferred):

- **Workflows: 0.** `.github/` does not exist in the tree at all. Consistent with `82227f08`
  (2026-07-08, `chore(automation): retire conformance-digest mechanism [#255]`), which deleted
  `.github/workflows/nightly-conformance-triage.yml`.
- **Branches on origin: exactly two** — `main` at `a02dd1115` (identical to local HEAD) and
  `automation/fleet-audit` at `63b772fc`. This independently confirms the 2026-08-01 JOURNAL
  claim that "origin now holds exactly main + automation/fleet-audit, no worktrees, no feature
  or backup refs".
- **Changelog-review state:** the `/changelog-review` command exists; last recorded review
  **2026-07-11**. Three weeks stale against a PUSH-trigger-only contract — informational, not a
  defect, since the trigger is operator-initiated by design.

---

## 3. Findings — doc prose describing organs that no longer exist

### D-1 · CONTRIBUTING.md describes a retired GitHub Action in the present tense — KNOWN but UNOWNED

`CONTRIBUTING.md:128–178`, section **"Nightly outcome management"** (51 lines), describes the
nightly conformance Routine → PR → Action loop as live, naming
`.github/workflows/nightly-conformance-triage.yml` as "the repo's first GitHub Action" that
"handles the morning so the operator touches only findings", with a three-row behaviour table.

**That organ was deleted 2026-07-08** (`82227f08`, [#255]), along with the
`automation/conformance-digest` branch. There is no `.github/` directory.

**This is already known.** `ARCHITECTURE.md:776–780` names it precisely and defers it:

> **Do not follow CONTRIBUTING "Nightly outcome management" as live guidance** — at
> `CONTRIBUTING.md:132-136` it still describes the Action in the present tense … That is the same
> severance seen from the other side; reconciling it is out of this window's scope and is
> reported, not fixed here.

**The finding is not the staleness — it is that nothing owns the reconciliation.** A grep of
`tasks/` for `Nightly outcome management` or `nightly-conformance-triage` returns **zero rows**.
A defect recorded in a canonical doc with an explicit "out of scope, reported not fixed"
disposition, and no backlog row, is a debt that can only be found by re-reading ARCHITECTURE.
**Proposal: file a row, or record the deferral where a gate can see it.**

Two further notes the ARCHITECTURE marker does not cover:
- The marker cites `CONTRIBUTING.md:132-136`; the stale span is actually **128–178** (the whole
  section, including the diff-guard prose and the three-row table).
- `CONTRIBUTING.md` carries a `last_reviewed` stamp that has **passed** its freshness gate
  throughout. The stamp certifies "re-read end-to-end and confirmed accurate" (CLAUDE.md §4).
  A section describing a deleted organ survived that certification — which is a signal about the
  freshness ritual, not just this file.

### D-2 · PLAYBOOK.md references the same deleted Action as a live component — NOT covered by the marker

Two sites, neither named in the ARCHITECTURE deferral:

- `protocols/PLAYBOOK.md:1747` — in **"The envelope"**, which defines a nightly Routine
  deployment as *four* parts, item 3 is: *"**Action** — the outcome handler
  (`.github/workflows/nightly-conformance-triage.yml`): diff-guard + auto-merge / triage on the
  PR the run opens."* Item 4 then points the reader at the CONTRIBUTING section from D-1.
- `protocols/PLAYBOOK.md:1783` — cites the same file as one of two live shallow-clone guards
  (*"the Action sets `fetch-depth: 0`"*).

**Severity: higher than D-1.** PLAYBOOK is the universal-protocols reference consulted on demand
when a task needs it, and this passage is the definition of how to deploy a nightly Routine. An
agent following it would build against an organ that does not exist. D-1 at least carries a
"do not follow this" warning elsewhere in canon; **D-2 carries none**.

### D-3 · ADR-82 carries `Status: Proposed` and no row owns it

Three ADRs still carry `- **Status:** Proposed`:

| ADR | Subject | Owned? |
|---|---|---|
| ADR-88 | File-oriented dependency management | **yes** — [#242] |
| ADR-89 | Computed code-dependency edges | **yes** — [#242] |
| ADR-82 | HANDOFF_PROCESS **v5** — CC-owned handoff (model C) | **no row found** |

[#242] ("ADR status-flip coherence check") names ADR-88/89 explicitly and scopes its Done-when to
them. **ADR-82 is outside it.**

ADR-82 is the more consequential case: it governs the handoff process, and that process is now at
**v6.0.1** — two majors past the version ADR-82 proposes — and is in daily production use, with
six `reconciled_with` edges pointing at it (CLAUDE.md §12 v2.48). Its own header still says
*"Nothing is removed by this ADR in its Proposed state"* and lists a decommission set gated on a
Council flip that the README records as **waived (#149)**.

**Proposal: extend [#242]'s scope to ADR-82, or file the v5→v6 ratification question separately.**
Per the 2026-08-01 JOURNAL, flipping a status line *asserts a ratification event* and was
deliberately left alone — that judgment is respected here; this lane only reports that one of the
three is un-owned.

---

## 4. REFUTED in-lane — recorded so they do not propagate

Both were produced by this lane's own fan-out and killed on verification. Recording them because
intake #16 §5 lesson 6 ("Verify numbers before they propagate") makes an unverified number a
named failure class.

| Claim | Verdict | Why |
|---|---|---|
| "`ARCHITECTURE.md:294` lists 14 checks but current `ALL_CHECKS` has 41 — CONTRADICTS-LANDED-STATE" | **REFUTED, twice over** | (a) The count is **38**, not 41. (b) The list is *deliberately* partial — the same sentence reads "**not an exhaustive inventory**" and points at `ecosystem/doc-counts.md` for the count and `python scripts/audit.py checks` for the live registry. A curated example list that says it is curated is not drift. |
| "`PLAYBOOK.md` carries no section on the desired-state organ class — INCOMPLETE" | **NOT A DEFECT** | ADR-109 §8 defines the organ class and `ARCHITECTURE.md` §2 documents it (`bf373b1`, [#459] — which explicitly *named the ADR-109 organ class*). PLAYBOOK summarizing less than ARCHITECTURE is the intended relationship, not divergence (CLAUDE.md §5 rule 6). |

## 5. Freshness stamps

All canonical files carrying `last_reviewed` PASS both the audit.py check #10 condition
(stamp not older than last edit) and the 30-day backstop as of 2026-08-01. **No stamp finding.**

Caveat worth the architect's eye: D-1 shows a file can pass the freshness gate while containing a
51-line description of a deleted organ. The gate checks *stamp vs edit date*, not *prose vs
reality* — working as specified, but the specification is weaker than the stamp's stated meaning.

## 6. Intake #23 — correctly SEED, nothing should have moved

`docs/intake/2026-08-01-func-distillation-and-library-first.md` (intake **#23**, status `SEED`,
`consumed-by:` empty) was **filed 2026-08-01** — one day old at this batch.

Context that settles the "should anything have moved?" question: the 2026-08-01 night batch's
plan-prep report recorded that #23 **could not be written** that night — *"The SEED intake doc
cannot be written: the operator's verbatim text is not in this repo"* — and asked the operator to
supply the dictation. The operator did, and the doc landed the same window. **SEED is correct;
unconsumed is correct.** Tonight's lane L-E is its first *research* consumption (exercising the
library-first doctrine), which is not a status event.

## 7. Blocking questions for the architect

| # | Question | Decision shape |
|---|---|---|
| D-1 | File a row for the CONTRIBUTING "Nightly outcome management" reconciliation, or delete the section outright? | file-row / delete-section / keep-deferred |
| D-2 | PLAYBOOK "The envelope" still teaches a four-part deployment whose part 3 is deleted. Rewrite to three parts, or is a successor Action planned? | rewrite / successor-planned / defer |
| D-3 | Extend [#242] to cover ADR-82, or rule the v5 ADR superseded-by-v6 without a status flip? | extend-242 / supersede-ruling / leave |

---

*Read-only night batch. No generator was run with `--write`; no governed file was edited; the
working tree was verified clean after every probe.*
