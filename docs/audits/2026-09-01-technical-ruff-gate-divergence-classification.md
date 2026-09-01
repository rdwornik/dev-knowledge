# RULING 3 — the `ruff-gate` divergence in both consumers is DECLARED, and the blocker is a deferred hub row

- **Class:** technical · **Date:** 2026-09-01 · **Author:** CC (Opus 5, attended)
- **Consumed by:** `[#614]` (whose instantiation prep named this as the shared hard blocker),
  `[#276]` (the hub row this classification hands the problem back to), and operator ruling 3.
- **Method:** read-only. Both consumer repos were read, neither was written to.

## The ruling, and the answer

> *"READ the local edits, classify each as legitimate consumer customization (→ parity type
> becomes conditional for that carrier) or drift (→ restore from hub). Never delete; report the
> diff and the classification."*

**Both are LEGITIMATE CONSUMER CUSTOMIZATION. Neither is drift. Both are already DECLARED, in the
consumer's own `.methodology.yaml`, and one of them is already RULED.** Nothing needs restoring
and nothing needs deleting.

## The diffs, and where each is declared

**ai-council** — `.pre-commit-config.yaml:80-87`

```
- repo: https://github.com/astral-sh/ruff-pre-commit
  # consumer-owned gate. See .methodology.yaml (consumer-ruff-gate waiver). Re-activated by
  # fleet ruling 2026-07-12 (overriding the [#244] prune). Gate mode: `ruff check` (no --fix).
  - id: ruff
```

Declared at `.methodology.yaml` → `component: ruff-gate`: *"ai-council runs its OWN consumer-owned
ruff gate … The fleet-generic managed hook set carries NO ruff ([#244] dropped it from the
manifest), so ANY consumer running a ruff gate is [divergent by definition]."* **Re-activation is
a recorded FLEET RULING of 2026-07-12 that explicitly overrides the `[#244]` prune.** The prune
refusing here is the guard doing its job against a change the fleet already sanctioned.

**corp-monorepo** — `.pre-commit-config.yaml:15-22`

```
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.15.5
  hooks:
    - id: ruff
      args: []   # check-only gate (fleet-canonical form)
    # ruff-format omitted: core.autocrlf=true on Windows causes CRLF/LF conflict
    # in pre-commit's stash/unstash cycle. Run `ruff format packages/` manually
```

Declared at `.methodology.yaml` → `component: ruff-gate`: *"corp-monorepo runs its OWN ruff gate,
now UNIFIED to the fleet-canonical pyproject `[tool.ruff.lint]` as of 2026-07-13 … It stays a
sanctioned divergence because the fleet-generic manifest DROPPED ruff as an add-target."* The
`ruff-format` omission is a **measured platform finding**, not a preference: `core.autocrlf=true`
on Windows collides with pre-commit's stash/unstash cycle.

**Both stanzas are deliberately PRUNE-SAFE in shape** — a bare `id: ruff` with no `name:` — which
each waiver states as an intentional design so a future hub ruff entry stays distinguishable.

## The finding that actually matters, and it is not about the consumers

**Both waivers say the same thing, in their own words:** *"the deploy tool does not yet read this
waiver (hub #276)"*. So `deploy/tool.py` sees `present_modified`, refuses the prune, and aborts
the whole instantiation with no record written — **while the divergence it is refusing over is
declared, sanctioned, and in one case ruled.**

**`[#276]` PREDICTED THIS EXACT REFUSAL** — *"once corp-monorepo records 1.2.0, a future remove-leg
run (v1.3.x+) re-enters the sweep and REFUSEs on corp's consumer-owned ruff"* — and its status is
**`deferred`**.

**So the corp-monorepo and ai-council instantiations are blocked on a DEFERRED HUB ROW, not on a
consumer question.** The morning order's *"GO monorepo instantiation from the derived contract"*
rests on `[#276]` being un-deferred first. That is the same class the north-star already warns
about from `[#624]`: *a plan resting on a deferred row is a plan resting on nothing* — and here it
is the deployment plan itself.

## What the ruling's own remedy implies

The ruling routes a legitimate customization to *"parity type becomes conditional for that
carrier"*. The parity surface can express that today. **What cannot express it today is the deploy
tool**, which is `[#276]`'s entire subject. Marking the parity row conditional would make the
registry honest and would still leave `--execute` aborting, so the two acts are not substitutes:
the parity edit records the truth, and `[#276]` is what unblocks the deploy.

**Not taken here, deliberately:** no parity row was edited and no consumer was written to. This is
the read-and-classify the ruling asked for; the acts it implies are hub-side and gated.
