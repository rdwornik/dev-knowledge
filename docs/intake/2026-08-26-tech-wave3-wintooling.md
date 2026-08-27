---
intake-id: 56
status: READY
origin: read-only cloud recon (Dispatch-Cloud, 2026-08-26, Mode B — bound to `.dev-knowledge`; win-tooling NOT observed), relayed to file by the browser architect and landed by lane `g2-consume-recon` at `docs/audits/2026-08-26-technical-w3prep-recon.md`
consumers: `ecosystem/deployed-versions.yaml`; `ecosystem/satellite-onboarding-rulings.yaml`; `deploy/tool.py` + `scripts/audit.py` consumer-root resolution; the `docs` carrier; the wave-3 lane contract
---

# Wave 3 — win-tooling is declared in the fleet and outside its enforcement, and the verb that would fix that is a thin composition

## Problem / motivation

`win-tooling` is **in the fleet declaration and outside the fleet's enforcement in one move**: its
parity role is `pre-deploy`, so every parity MUST row renders "skipped", and it is absent from the
deploy registry, so the tool refuses it outright. Eight organs were gap-mapped; it **LACKS** five
of them outright, and two more are present-but-unverifiable. It has zero enforcing organs.

The recon's larger finding is that the fix is **cheaper than it looks**. The north-star verb
`instantiate-methodology <repo>` is a thin composition over organs that mostly exist and are
proven at n=1: preflight, carrier application, the version record and re-measurement are all built.
**The missing half is path-portability and the canonical-doc seed — not orchestration.**

**Two corrections this intake carries so no wave-3 lane re-derives them wrongly:**

1. **Premise correction on `[#463]`.** It is commonly cited as open consumer debt. Its frontmatter
   reads `status: closed` — closed **by ruling, not by fix**: the register's T-16 accepts all four
   items as consumer-repo debt *"the hub may surface but not close"*, and says in terms that the
   section *"accepts a REASON, not a measurement."* **The debt is live; the row is not.** Wave 3
   cannot reopen `[#463]`; it needs new rows, which is what this intake proposes.
2. **A freshness ceiling on every win-tooling claim below.** The newest hub baseline for the repo
   is dated 2026-07-31 and `ecosystem/index.yaml` stamps its last audit 2026-08-05 — **21 days
   stale** at the recon date. Worse, `[#463]`'s own body records **51 further baseline commits
   existing locally only — unpushed, unread**. The hub cannot see win-tooling's current state at
   all. Everything here is *hub-recorded, not observed*; treat it as a plan against a 21-day-old
   snapshot, never as a measurement.

## Scenarios (+1 view)

- **As the operator**, one command onboards a repo: preflight → read its profile ruling → seed the
  canonical docs → apply the carriers → write the version record → re-measure — in the sanctioned
  RULING-W consumer-worktree→report shape, enforced by the tool rather than remembered by the seat.
- **As a wave-3 lane**, I read `deploy/tool.py`'s docstring and it tells me the truth about which
  paths are implemented, so I do not plan around a capability the module wrongly disclaims.
- **As a wave-3 lane running anywhere but the operator's laptop**, the consumer resolves from an
  explicit root instead of a filesystem-sibling assumption, so neither instantiation nor
  measurement silently becomes unreachable.
- **As win-tooling**, the first slice takes me from unonboarded to the floor plus the pre-commit
  set plus a session gate plus `/ship`, and my parity role flips `pre-deploy → consumer` — visible
  in one `audit repo win-tooling` diff.

## Functional requirements

- **Must:** win-tooling (and `terminal-setup`) are **admitted** — a registry key and a ruled
  onboarding profile — because the tool rejects an unregistered repo before anything else runs.
- **Must:** consumer-root resolution is **explicit**, in both the deploy tool and the audit
  entrypoint, with the sibling layout kept as the default fallback.
- **Must:** the first slice runs as a consumer worktree/branch → report, per ADR-41 / RULING-W, and
  **mechanism-before-act**: the authorizing amendment lands before the write, never retroactively.
- **Should:** the docs carrier seeds a greenfield consumer's canonical docs — today its entire
  payload is three source→path pairs, and **two of the seven mandatory docs have no skeleton
  anywhere** in `templates/`.
- **Should:** `deploy` **reads** the onboarding-profile ruling instead of ignoring it (the rulings
  file exists and only a read-only validator consumes it).
- **Could:** a uv/pyproject/`.python-version` carrier — the ADR-106 toolchain is hub-local and no
  carrier ships it.

**The ranked build order, carried verbatim in shape from the recon's §4 so the sequencing is not
re-derived** (each item unblocks the next; the recon's own §1 gap map and §3 blockers B1–B9 carry
the file:line evidence for every one): **1st** de-hardcode consumer-root resolution · **2nd** the
tag and the registry admission (operator acts, cheap, gate everything) · **3rd** extend the docs
carrier to a canonical-doc seed set and author the two missing templates · **4th** make deploy read
the profile ruling instead of ignoring it · **5th** put the RULING-W branch mode inside the tool so
the shape is enforced, not remembered · **6th** a uv/pyproject carrier · **7th** the backlog-engine
carrier, **last**, and only after its two blocking rows.

## Acceptance criteria (ex-ante)

1. `audit repo win-tooling` reports the floor present, the pre-commit set armed, the parity role
   flipped `pre-deploy → consumer`, and a fresh baseline landed in the repo's history directory.
2. A **non-sibling** consumer layout resolves in both modules, proven by a test, and `audit repo
   <name>` runs from a checkout with no sibling tree.
3. Both admitted repos carry a registry key **and** a rulings entry naming `full | floor-only` with
   `ruled_by` and a date.
4. The four ruled-accepted findings clear, except `workspace_settings`, which **cannot close by
   deploy** — the `editor-config` carrier is declaration-only — and so must be recorded as
   hand-fixed or as accepted debt.
5. No wave-3 act writes into a consumer outside the RULING-W shape.

## Non-goals

- **Reopening `[#463]`.** It is closed by ruling; the debt travels on new rows.
- **The backlog engine** (`tasks/` + generator) — three independent blocks, one of them a deferred
  row and one an unruled consumer schema. It is explicitly last, and *do not attempt yet*.
- Rows the hub already owns and this intake deliberately does not re-propose: the validator
  de-hardcode, the consumer BACKLOG schema ruling, the seed-runbook child-class awareness, the
  runbook fan-out, the verify-only re-run mode, and the fleet dependency-parity row.
- **Tag creation** — CC does not tag (ADR-91). The tag is an operator act.
- The private `origin` remote for win-tooling: already ruled, owed to win-tooling's own list, not
  hub work.

## Impact sketch (4+1 lite)

- **Logical:** the fleet's declaration and its enforcement stop disagreeing for this member.
- **Process:** onboarding becomes one gated act with a re-measurement, instead of a remembered
  sequence.
- **Development:** two small data edits, one portability refactor with a test, one carrier
  extension, one composition command.
- **Physical:** the hub stops requiring that every consumer be a filesystem sibling under `Dev/`,
  which is what makes any off-laptop substrate viable.

## Open questions

1. **Held, not birthed — the release act.** The deployable target declares a tag that **does not
   resolve on the remote**, and preflight hard-aborts without it. Either the tag is cut, or the
   manifest is recorded undeployable and the prior version is named the wave-3 target in the lane
   contract. Operator act; blocks the first slice.
2. **Held, not birthed — the canonical-doc seed set** (recon row W3-4). It is a **carrier change,
   which is a release act**, so it depends on question 1; and it needs two templates authored that
   do not exist. Held here rather than filed, on ledger headroom.
3. **Held, not birthed — the `instantiate-methodology` verb itself** (recon row W3-5, size L). It
   depends on the portability row and the seed set, and it carries an **overlap to adjudicate**:
   the hub already has an open row proposing a kernel as an installable package, which is an
   adjacent answer to the same portability problem. The architect should rule whether this verb
   rides that arc or precedes it — that ruling is owed before the row is worth filing.
4. Is the ADR-log gap real? **No hub surface records it either way** — the canonical-doc check
   covers six files and not `docs/decisions/`. This is an **evidence hole, not a finding**, and it
   stays labelled as one until win-tooling is observed.
5. Three claims are labelled **hypotheses, not evidence**, by the recon itself: that win-tooling has
   no ADR log, that the four ruled-accepted items are still live (unconfirmable — 51 baselines
   unpushed), and that it still has no `origin`.

## Status

READY — evidence-complete and landed. Three of the six proposed rows are birthed by lane
`g2-consume-recon` citing this intake; W3-1 is an operator act (question 1) and W3-4 / W3-5 are
**intake-held** at questions 2 and 3, blocked on the tag decision and on ledger headroom.
