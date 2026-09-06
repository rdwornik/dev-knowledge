---
intake-id: 72
status: DRAFT
origin: lane lane-t-000-nc1-clear, 2026-09-06 NIGHT batch §3.6 candidate (c); witnessed while clearing the `routing_agreement` hard-fail under operator consent #6 (to-cc/DECLARE-GO-2026-09-06.md ruling 2)
consumed-by:
---

# A derived copy has no registry, so its rebind is caught at ship time instead of at commit time

## Problem / motivation

Some facts in this repo are authored in one place and **derived** into another, where the
derived copy lives outside the tree that produced it. `ecosystem/routing-table.yaml` is
authoritative for role → CLI routing; `~/.claude/ROUTING.md` at L0 carries a rendered copy of
it. `scripts/routing_agreement.py --render` produces the copy, and a check asserts the two
agree.

**The check is a ship-gate leg, and the authoring act is a commit.** Those are different
moments, and the gap between them is the whole problem. On 2026-09-05, commit `5be038ff`
(*"docs(rulings): file candidates (o)-(r) from the AJ gap analysis, and rebind the adversarial
role off an absent CLI"*) changed the table's `adversarial` row from `sol` to `codex`. The
derived copy was not re-rendered in that commit and nothing at commit time asked for it. The
divergence then sat undetected until it surfaced as a **hard-fail** — not a WARN —
at a ship gate the following night, where it blocked a release act that had nothing to do with
routing. This lane measured it live at boot before clearing it:

```
[!!] routing_agreement: the L0 derived copy diverges from ecosystem/routing-table.yaml:
     adversarial (table: codex) -- the L0 copy mentions the role but not codex beside it
```

The cost is not the fix — the fix is one render, and it is cheap. The cost is **when** the fix
is demanded: at the moment a release is being attempted, by a seat that did not author the
divergence, on a file in a different repository from the one being shipped.

**The narrow reading of this is "routing needs a hook".** The wider one, and the reason this is
an intake rather than a row, is that the repo has **no registry of which facts are derived and
where their copies live**. `routing-table.yaml → ~/.claude/ROUTING.md` is one such pair. There
are others of the same shape — a source of truth in the tree, a rendered consumer elsewhere,
a generator that reconciles them, and a check that notices only later. Each has been
discovered and wired one at a time. Nothing enumerates the class, so nothing can answer "what
else is derived, and is it current?" without a person remembering.

## Scenarios (+1 view)

- **As the author of a rebind**, I change one row in `ecosystem/routing-table.yaml` and commit.
  I am not told that a derived copy of that row exists, or that I have just made it stale. My
  commit is green.
- **As the seat trying to ship two days later**, I meet a hard-fail naming a file in a
  different repository, authored by someone else's commit, with no indication of which commit
  caused it. Clearing it requires operator consent, because the divergent file is on the
  operator's disk and outside the tree I am shipping.
- **As the operator**, I am asked to consent to a re-render of my own L0 config in the middle
  of a release window, for drift introduced by a routine commit days earlier.
- **As a new seat**, I want to know what else in this repo is derived-and-copied-outward. There
  is no surface that answers, so I find out when a gate tells me.

## Functional requirements

- **Must:** a seat can enumerate every derived-copy relationship in the repo — source, derived
  location, the generator that renders it, the check that verifies it — from one place, without
  reading each generator.
- **Must:** the moment a derived copy goes stale is nameable. Whether that moment is *at the
  commit that staled it* or *at ship* is a design question, but which one it currently is must
  not be an accident of where the check happens to be registered.
- **Should:** a copy that lives outside this repository is marked as such, because the act that
  fixes it is the operator's and not a seat's — and a check whose remedy needs consent behaves
  differently from one a lane can just fix.
- **Could:** the registry is the thing generators and checks read, rather than a document that
  restates what they already hardcode.

## Acceptance criteria (ex-ante)

1. Given the derived-copy registry, a seat can list every source → derived pair without opening
   `scripts/`, and the list agrees with the checks that are actually armed.
2. Given a commit that edits a registered source without re-rendering its derived copy, the
   staleness is surfaced at a named moment, and the registry says which moment that is.
3. Given a registered pair whose derived copy is outside this repository, the surface says so,
   and says whose act the remedy is.
4. Given a new derived-copy relationship, adding it to the registry is the act that makes it
   checked — not a second, separate wiring step that can be forgotten.

## Non-goals

- **Deciding that every derived copy must be gated at commit time.** L0 copies live on the
  operator's disk and are absent on CI, in containers and on cloud lanes;
  `routing_agreement`'s own module docstring already reasons carefully about that
  (`ABSENCE IS A REPORTED GAP, NOT A PASS`, register ruling Z-G4). Whether a commit-time leg is
  even *possible* for an out-of-repo copy is exactly the technical question this intake refuses
  to answer.
- **Auto-writing L0 or any other out-of-repo file from a gate.** Layer 2 does not execute
  (ADR-28/36), and `routing_agreement` is explicitly read-only.
- **Re-opening the routing decision itself.** Which CLI fills which role is L0 doctrine and out
  of scope here; this is about the copy, not the content.
- **A new gate.** Whether this ends as a gate, a registry read by existing gates, or a
  generator convention is the triage's call.

## Impact sketch (4+1 lite)

- **Logical:** introduces "derived copy" as a named relationship the repo can talk about,
  alongside the `reconciled_with:` spec-edge relationship it already has. The two are similar
  in shape — a dependent that must be re-verified when its source moves — and their similarity
  is worth examining rather than assuming.
- **Process:** changes when a rebind's cost is paid: at authoring rather than at shipping.
- **Development:** touches the generator/check pairs that already exist; the library-first
  question is whether `validate_reconciliation`'s registry shape already fits, since it solves
  the adjacent problem for spec versions.
- **Physical:** at least one registered copy lives in a different repository (`~/.claude`),
  which is a genuine constraint rather than an inconvenience — it is why the remedy needs
  operator consent.

## Open questions

- Is this the same problem as `reconciled_with:` spec edges, or only rhyming with it? If the
  same, the answer is probably an extension rather than a new organ. **Technical-architect
  question — recorded, not answered.**
- How many derived-copy pairs actually exist today? This intake witnessed exactly one and
  asserts nothing about the count; a census is the first thing the triage would want, and
  "never restate a count in prose" (CLAUDE.md §4) applies.
- Can a commit-time leg exist at all for an out-of-repo copy without either failing open on the
  hosts where the copy is absent, or failing closed on hosts where its absence is normal? Z-G4
  says a check that cannot compute its ground truth FAILs rather than skips — which may make a
  commit-time leg for L0 copies actively wrong.
- Does the operator want L0 divergence to block a commit at all, given the remedy is his act?
- Is `~/.claude/ROUTING.md`'s divergence the only one currently live, or the only one currently
  *checked*? Those are different facts and only the second is knowable today.

## Status

DRAFT — filed by `lane-t-000-nc1-clear` on 2026-09-06 as candidate (c) of its contract §3.6;
awaiting the operator's dawn ratification pass. The witness is recorded above; nothing was
built and no row was born.
