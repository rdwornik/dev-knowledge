# ADR-114: May a root `README.md` be recreated — and what does substituting a canonical living-doc filename actually cost?

- **Status:** **PARKED** — ruled by the operator 2026-08-22. *The priced options below are retained unchanged as the input the ruling selected against; the Decision section, authored blank for exactly this moment, now carries the ruling.*
- **Date:** 2026-08-22
- **Decision tier:** Architecture — **RULED (parked) by the operator 2026-08-22.** Authored by the CLOUD-4 v2 mutation lane, which was not competent to make it and correctly did not.
- **Amends (if accepted):** ADR-101 §1 — the closed Tier-1 file enum in `SANCTIONED_TIER1_FILES` would gain `README.md`
- **Supersedes (if accepted):** ADR-38 amendment A5, in the single respect that A5 deprecated the root `README.md` and `CLAUDE.md` §5 rule 5 hardened that into *"do not recreate it"*
- **Related:** ADR-33 (VISION.md frontmatter), ADR-51 (canonical-doc structure), ADR-53 (single instruction file), ADR-104 (fleet repository shape — the nine members), ADR-85 amendment 2026-08-03 §A5 (why the Stop hook is advisory), ADR-98 (intake → ADR traceability)
- **Intake:** none — this ADR is not intake-born. It is cut from the READ-ONLY review artifact `docs/audits/2026-08-21-fresh-eyes-cloud-r2-universalization.md` §0.3 / §1.4 / §1.5, whose §5 table verdicts the rename **NO-GO as briefed** and hands this question to the architect as **CONFLICT-2**.
- **Decommission:** none while Proposed. **If accepted**, three surfaces are decommissioned in the accepting commit and each becomes a BACKLOG row: (a) `CLAUDE.md` §5 rule 5's *"do not recreate it"* clause, (b) `ARCHITECTURE.md:366`'s echo of it, (c) the `README.md`-is-optional docstring in `scripts/audit_checks/check_adr38_baseline.py`.
- **Source:** CLOUD-4 v2 lane, session branch `feat/cloud-4v2-universalization`, bound at `ff01fd10`. Measurements below are reproducible at that revision with the commands quoted inline.

---

## Context

Two decisions collide, and neither is wrong.

**The standing prohibition.** Root `README.md` was deleted 2026-05-23 under ADR-38 amendment A5 as *"redundant with VISION + CLAUDE.md + ARCHITECTURE for this internal-only repo"*. `CLAUDE.md` §5 rule 5 hardened that into an instruction — *"do not recreate it"* — echoed at `ARCHITECTURE.md:366`, and `scripts/validate_hermetization.py` Rule A turned it into a gate: `README.md` is absent from `SANCTIONED_TIER1_FILES`, so an added root `README.md` is a pre-commit BLOCK.

**The pressure against it.** A repo that publishes a methodology to nine fleet members, and that is increasingly read by non-Claude agents (R2 §2), has a real argument for the one filename every tool and human already knows how to find. That argument was made as a *rename* — `VISION.md` → `README.md` — in the CLOUD-R2 brief.

R2's review found the framing itself to be the error, and said so in terms:

> **this is not a rename, it is the reversal of a 2026-05-23 deletion decision plus a fleet-wide canonical-file substitution.**

This ADR exists because a lane cannot resolve that, and because the question deserves to be ruled on **priced** rather than on intuition. What follows is the price. Three costs, each measured at `ff01fd10`.

---

## The price — measurement 1: fleet sequencing (parity MUST ×9)

`ecosystem/parity-surfaces.yaml:133–139` declares:

```yaml
- id: canonical-doc-vision
  kind: path
  tier: {hub: MUST, consumer: MUST}
  probe: {type: path_tracked, path: VISION.md}
```

`tier: {hub: MUST, consumer: MUST}` means **every fleet member is required to carry `VISION.md`**. The membership is not a matter of opinion: `docs/decisions/ADR-104-fleet-repository-shape.md` carries the delimiter-anchored `adr104-fleet-members` declaration, verified at this revision to enumerate **nine** ids —

```
.dev-knowledge · ai-council · corp-monorepo · corp-ops · corp-sca-time-automation
demo-prep · life-architect · terminal-setup · win-tooling
```

*Reproduce:* `sed -n '/declaration:start id=adr104-fleet-members/,/declaration:end/p' docs/decisions/ADR-104-fleet-repository-shape.md`

**What this costs.** Renaming in the hub alone turns `fleet_parity` RED for **all nine members at once**, and `CLAUDE.md` §5 rule 4 forbids the hub driving a child repo's state — Layer 2 may not execute the fix. So the migration is a **nine-repo program with an ordering constraint**, not a commit:

1. the parity surface's probe path is the coupling, so it can only move once every member can satisfy the new value;
2. four of the nine (`demo-prep`, `life-architect`, `terminal-setup`, `win-tooling`) are recorded in `parity-surfaces.yaml` as `role: pre-deploy` — several carry *no* `VISION.md` and no `CLAUDE.md` today, so for them the rename is an onboarding act, not a rename;
3. the hub cannot verify any of it from its own tree, which is the part that makes a lane-shaped attempt structurally unsound rather than merely large.

**A ruling that accepts this ADR is committing the fleet to that program.** That is the first thing being decided.

## The price — measurement 2: the immutable-locator cost (R2 §1.4 R4/R7)

Measured at `ff01fd10` over the whole tree (`grep -rn "VISION\.md" --binary-files=without-match . --exclude-dir=.git`):

```
total occurrences ............ 1,956
total files ..................   678
markdown links among them ....     0
```

*(R2 measured 1,924 / 672 nine days earlier; the corpus grew, the shape did not.)*

**Zero of them are markdown links.** `grep -rcE "\]\(\.?/?VISION\.md"` returns no non-zero file. Nothing in this repo — no link checker, no CI job, no gate — can notice a broken canonical-doc reference. **The corpus has no detector for the failure class the rename creates.** That is the single most important fact in this section, and it is why the substitution's cost is *silence*, not breakage.

The costly subset is the one that cannot be repaired:

- **`docs/handoffs/` — 104 of the 114 committed bundles reference `VISION.md`; 69 distinct `PROBES`-named files carry a row citing it**, most descending from `templates/handoff/v5/PROBES.md.tmpl`'s probe **P1a**, whose literal verification command is `grep -A4 '^## Vision' VISION.md`. Handoffs are immutable under `CLAUDE.md` §5 rule 3. **These can never be corrected.** *Reproduce:* `grep -rl "VISION\.md" docs/handoffs/ | cut -d/ -f3 | sort -u | wc -l` → `104`; `... | grep -i probes | wc -l` → `69`.
  The mitigating fact, verified in code: `check_handoff_probes` validates **only the active bundle**, so the live blast radius is *the active bundle at rename time plus every bundle cut afterwards*. Bounded — but it means **the accepting commit has to re-cut or retire the active bundle's probe and move the template in the same commit**, or the very next handoff bakes a dead command into a new immutable artifact.
- **`ecosystem/index.yaml` (17 refs) and `ecosystem/disposition-register.yaml` (5 refs) need OPPOSITE treatment.** `index.yaml` quotes past audit findings verbatim; rewriting it **falsifies history**. `disposition-register.yaml` carries the live disposition match keys `"VISION.md -> handoff-process"` and `"VISION.md -> prompt-template"`; *not* rewriting it **orphans two live dispositions** so their WARNs resurface undispositioned. A mechanical sweep gets at least one of the two wrong by construction.

**What this costs.** The rename permanently degrades ~69 immutable artifacts into carrying a command that no longer runs, and it requires two adjacent ecosystem files to be treated by opposite rules in one commit. Neither cost is recoverable later.

## The price — measurement 3: the `gen_handoff` degrade contract

`scripts/gen_handoff.py::_vision_extract` is a **content** dependency, not a path dependency: it opens the canonical file and regex-matches the `## Vision` heading. Its degrade contract does **not** raise —

```
"(VISION.md `## Vision` section not found — fix VISION.md before using this boot)"
```

— it returns that literal, and the generator writes it into the boot bundle. **A handoff bundle is immutable the moment it is committed.** So a filename substitution that misses this site produces a failure that is silent, permanent, and stamped into the record: every new bundle boots a seat with a placeholder where its repo's purpose should be, and no gate says a word.

**This lane has already de-risked exactly this site**, and it is the reason the mitigation was worth landing ahead of any ruling. `scripts/canonical_docs.py` now holds the canonical filename and its degrade string **together** —

```python
VISION_EXTRACT_HEADING = "## Vision"
VISION_EXTRACT_MISSING = (
    f"({VISION} `{VISION_EXTRACT_HEADING}` section not found — fix {VISION} before using this boot)"
)
```

— so the name cannot move without the message following it, and `tests/test_canonical_docs.py::test_gen_handoff_name_and_degrade_string_move_together` pins that. Nine other machine constants read the same table. **The mechanism is landed; only the decision is open.**

**Honest limit, stated rather than left to be discovered.** The registry covers ten machine constants and one cross-language site. It does **not** cover the `## Vision` **H2 spine**, which is a second, independent migration surface: five deploy manifests (`deploy/manifest-v{1.1.0,1.2.0,1.3.0,1.3.1,1.4.0}.yaml`) each declare `VISION.md: spine: ["## Vision", …]`, mirrored by `check_canonical_structure`. A substitution that keeps the H1 `# VISION — .dev-knowledge` inside a file named `README.md` is internally incoherent; one that changes the H1 without the spine reds `check_canonical_structure` on all five manifest versions. **Filename and spine are two decisions, and this ADR prices only the first.**

---

## Decision

**Decision: PARKED** — *revisit only if A2's `AGENTS.md` track fails the universal-entry
purpose.* Priced: fleet parity ×9, 104/114 immutable bundles, 69 `PROBES`, and the
`## Vision` H2 spine as a second migration axis (unpriced by R2, priced here).

> **Operator ruling, 2026-08-22**, given as part of the batched ruling over the cloud-wave
> funnel table (`docs/audits/2026-08-22-technical-cloud-wave-close-funnel.md` line A1). The
> ruling is a **selection, not a refusal**: option (A) is not adopted and the question is not
> closed — it is parked behind a named, checkable condition. **The condition is A2's outcome,
> not the calendar**, which is why no date-trigger is recorded here: `AGENTS.md` was ADMITTED
> in the same ruling and is the cheaper route to the same universal-entry goal, so this
> question only becomes live again if that route fails to serve it.
>
> The three priced options are retained verbatim below, because a parked decision that
> discards its own inputs has to be re-priced from scratch when it is revisited:
>
> - **(A) REFUSE.** Hold ADR-38 A5 and `CLAUDE.md` §5 rule 5. Root `README.md` stays prohibited;
>   `VISION.md` stays the canonical name. Cost: the repo keeps a canonical filename that no
>   external reader or non-Claude agent expects. Benefit: all three measured costs above are
>   avoided in full, and the registry landed by this lane is still worth its keep — it was
>   recommended *"whether or not the rename ever happens"*.
> - **(B) ADMIT `README.md` WITHOUT SUBSTITUTING.** Amend ADR-101 §1 to sanction a root
>   `README.md` as an **additional** Tier-1 file (a short front door that points at VISION /
>   ARCHITECTURE / CLAUDE), and leave `VISION.md` exactly where it is. This pays measurement 1
>   only in part (a new `parity-surfaces` row, tiered `{hub: MUST, consumer: MAY}`, is a
>   forward-only add — no member goes RED) and pays measurements 2 and 3 **not at all**, because
>   nothing is renamed. **If the goal is "the filename everyone knows", this option buys it at a
>   fraction of the price** — and it is the option the CLOUD-R2 brief did not consider.
> - **(C) SUBSTITUTE.** Supersede ADR-38 A5, amend ADR-101 §1, and run the nine-repo program.
>   Pays all three costs. Requires a sequencing plan across the ADR-104 members before the first
>   commit, and requires the spine decision (above) to be made in the same ruling.
>
> A ruling on (A)/(B)/(C) is what unblocks — or closes — this ADR. **Until it is ruled, nothing
> in this repo may cite ADR-114 as authority**, and the `README.md` prohibition stands unchanged.

## Consequences

**If (A) — refuse.** Nothing moves. `CLAUDE.md` §5 rule 5 and `ARCHITECTURE.md:366` become *ruled* rather than merely inherited, which is a small gain: the prohibition currently rests on a 2026-05-23 amendment whose reasoning (*"internal-only repo"*) is weakening as the fleet grows. This ADR should then be marked **Rejected** rather than deleted, so the price stays on the record and the question is not re-opened un-priced.

**If (B) — admit without substituting.** Easier: an external reader gets a front door; the nine-repo program is not triggered; no immutable artifact degrades. Harder: the repo gains an eighth root living doc and a new drift surface (a front door that goes stale is worse than none), so (B) should carry a generated-and-gated shape — the repo already runs regen-and-diff seven times over and would not be inventing an organ. `CLAUDE.md` §5 rule 5 inverts and `check_canonical_md_visibility` moves `README.md` from `_CANONICAL_ALL` to `_CANONICAL_MANDATORY` — a one-line change now that both lists come from `scripts/canonical_docs.py`.

**If (C) — substitute.** Easier afterwards: one filename, universally recognized, and the ten machine constants already read it from one table so the *code* half of the migration is nearly free. Harder: the nine-repo sequencing program; ~69 immutable PROBES rows permanently carrying a dead command; two ecosystem files needing opposite treatment in one commit; a second (spine) decision; and `check_adr38_baseline` / `check_canonical_md_visibility` / `check_dot_prefix_discipline` each needing their `README.md`-is-optional inversions ruled, not just edited.

**In every case**, the two mechanisms this lane landed stand: the canonical-doc-name registry and the provider/model registry are decision-independent, which is exactly why they were landed while the decision stays open.

## Alternatives considered

- **Do the rename in a lane and file the fleet fallout as follow-up work.** Rejected on R2's evidence: 90.9% of `VISION.md` references sit in files the repo forbids editing (append-only + immutable), so a tree-wide substitution is a core-invariant violation on contact, and the nine-member parity break is not a follow-up — it is the immediate, simultaneous consequence.
- **Add `README.md` as a git-ignored or untracked convenience file.** Rejected: `parity-surfaces`' `path_tracked` probe and ADR-101's tree seal both key on tracked paths, so an untracked front door is invisible to every mechanism that would keep it honest — a file with no gate is the drift this repo spends most of its enforcement budget preventing.
- **Symlink `README.md` → `VISION.md`.** Rejected on measured evidence, not preference: the portability memo (`docs/archive/2026-08-09-research-multi-provider-portability-wf-d68b2f7f.md`) records that on Windows without `core.symlinks=true` + Developer Mode, *"git silently checks out a plain text file containing the link target string"*. The fleet is Windows + git-bash. A symlink degrades to a one-line stub that looks like a file and reads like garbage.
