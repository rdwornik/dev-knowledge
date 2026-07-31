# Night batch 2026-08-01 — L4: frontmatter-parser swap analysis

**Status: PROPOSAL — measured input plus a drafted why-not line. Nothing placed, nothing filed.**

**Done-contract: MET.** A morning reader can decide "keep the hand parser / swap to a library" on
observed round-trip evidence. Full measurement report (362 lines, per-file diagnosis):
`<scratchpad>/L4/report.md`. All experiments ran in a scratchpad venv; the repo's uv environment,
`pyproject.toml`, and `uv.lock` were untouched.

---

## Leg 1 — inventory: does a written why-not line exist?

**No. Zero hits.** Grepping `python-frontmatter`, `python_frontmatter`, and `ruamel` across
ADR-107, ADR-109, `scripts/gen_task_tree.py`, `scripts/gen_intake_tree.py`, `docs/audits/*`,
`LESSONS.md`, and `protocols/PLAYBOOK.md` returns nothing.

The two closest adjacent artifacts are about a *different* question — avoiding a read-only
dependency, not round-trip fidelity:
- `scripts/gen_intake_index.py:47-49` — "no yaml dep … for two fields"
- `scripts/gen_claude_rosters.py:61-65` — same rationale

**The gap is real**, and it is the reason this lane exists: the hand parser is load-bearing by
accident of history, with no recorded justification a future session could check.

---

## Leg 2 — measured round-trip fidelity

**Method:** 20 real fixtures copied (not moved) into the scratchpad — 10 `tasks/*.md`, 10
`docs/intake/*.md` — deliberately covering the awkward cases: empty scalars (`consumed-by:` with
nothing after it), a folded `>-` block scalar, mixed quote styles, unicode (em-dash, middle-dot,
arrows), long values, and `depends-on` values containing `#`. Each file: `load → dump → compare
bytes to original`.

| library / config | byte-identical | verdict |
|---|---|---|
| `python-frontmatter` 1.3.0 | **0 / 20** | **disqualified** |
| `ruamel.yaml` 0.19.1 (`typ='rt'`, `preserve_quotes=True`, `width=4096`) | **20 / 20** | **passes fidelity** |
| `ruamel.yaml` same, at its default `width` (~80) | 8 / 20 | fails on line-rewrapping only |

### `python-frontmatter` — fails unconditionally, with no config escape

Root-cause chain, all confirmed in the library's source:

1. **Key order destroyed.** `YAMLHandler.export()` never sets `sort_keys=False`, so PyYAML's
   `sort_keys=True` default reorders every file's keys alphabetically. This is the *first* line of
   divergence on all 20 files — e.g. `id: "[#102]"` displaced by `generates: BACKLOG.md`,
   `intake-id: 4` displaced by `consumed-by: null`.
2. **Quote style discarded** and re-derived from scratch (double → single, or dropped entirely).
3. **Trailing newline stripped** — `BaseHandler.format()` unconditionally `.strip()`s it.

**None of the three is exposed as a parameter.** This is not a tuning problem; the library has no
setting that would make it byte-faithful.

### `ruamel.yaml` — the surprising result, stated plainly rather than suppressed

**ruamel passes.** 20/20 byte-identical once `width` is raised above the corpus's longest line
(401 chars) — **including exact reproduction of the folded `>-` block scalar at its original fold
points**, confirmed with `cmp`.

At ruamel's default width (~80), 12/20 fail, and **every single failure is purely line-rewrapping** —
nothing else diverges. That is the classic byte-exactness killer and it is entirely a config choice,
not a fidelity ceiling.

Both libraries preserve unicode literally (em-dash, middle-dot, arrows survive as UTF-8). Not a
failure axis for either.

**Synthetic edge probes** (verified first that zero real files need them): missing-trailing-newline
confirms ruamel's body-untouched splice preserves it exactly; CRLF confirms ruamel's emitter always
writes LF internally — which independently validates why `gen_task_tree.py:144-145` refuses CRLF
loudly rather than trying to handle it.

---

## The contract question: is byte-exactness even the right thing to protect?

**It is a ratified obligation, not a style preference.** Three anchors:

- **ADR-107 §2** — the byte-exact reassembly requirement, recorded as "still normative".
- **ADR-109 §3 finding 2** — `write_policy: round-trip-unknown-byte-stable`, **explicitly naming
  `tasks/`**.
- Enforced as a **blocking ship-gate** (regen-and-diff), not an advisory check.

So a library that breaks byte-exactness is disqualified **by doctrine**, regardless of ergonomics.
That disposes of `python-frontmatter` twice over.

Independently of doctrine: relaxing to semantic-equivalence would trade a cheap `sha256` / `==` gate
for a bespoke comparator that is harder to trust and harder to test. That is not a simplification —
it moves complexity from a place where it is free into a place where it is bespoke.

---

## Verdict — stated per library, not averaged

**`python-frontmatter`: OUT, full stop.** Fails the ratified contract on three independent axes, none
of them configurable.

**`ruamel.yaml`: passes fidelity, but would not simplify anything.** This is the part that matters
for the decision and it is easy to miss:

> `scripts/gen_task_tree.py` does **not** load-then-dump. It derives frontmatter **fresh from the
> body via a fixed template** (`emit_task_file_text`, lines 250–289).

A ruamel swap would therefore still require hand-building key order, and would additionally require
remembering `width=4096` forever — a silent, action-at-a-distance footgun where the default value is
the wrong one. **The current hand parser already *is* that hardened configuration, with fewer
footguns and no dependency.**

**Recommendation: KEEP THE HAND PARSER** — but keep it for the *measured* reason, not the assumed
one. The batch brief anticipated "library breaks byte-exactness"; that is true of
`python-frontmatter` and **false of `ruamel`**. The honest justification is the second one: ruamel is
fidelity-capable but structurally redundant here, because the generator templates rather than
round-trips.

---

## Drafted why-not line — ready to place

Two forms, because the right home is arguably either. **Architect picks one; do not place both.**

### Form A — docstring addition, `scripts/gen_task_tree.py` (near lines 46–49)

```
Why a hand parser and not a library: the regen-and-diff gate is byte-exact (ADR-107 §2;
ADR-109 §3 `write_policy: round-trip-unknown-byte-stable`, naming tasks/). Measured
2026-08-01 on 20 real fixtures: python-frontmatter is 0/20 byte-identical and has no
escape — PyYAML's sort_keys=True default reorders every key, quote style is re-derived,
and BaseHandler.format() strips the trailing newline; none is exposed as a parameter.
ruamel.yaml (typ='rt', preserve_quotes=True) IS 20/20 faithful, but only with width raised
above the longest line (401 chars) — at its default ~80 it rewraps 12/20 — and it would buy
nothing here, because this generator templates frontmatter fresh from the body rather than
loading and re-dumping it. The hand parser is that hardened configuration already, minus the
silent width footgun and the dependency.
```

### Form B — `LESSONS.md` append entry (file's own newest-first format)

```
- **A library can be fidelity-capable and still be the wrong swap.** Measured 2026-08-01:
  python-frontmatter round-trips 0/20 of our real frontmatter files byte-identically (key
  reorder + quote re-derivation + trailing-newline strip, none configurable), so it fails the
  ratified byte-exact contract outright. ruamel.yaml round-trips 20/20 — but only at
  width>401, and our generator templates frontmatter rather than round-tripping it, so the
  swap would add a dependency and a silent default-width footgun while removing nothing. The
  reason to keep a hand parser is not always "the library is worse"; sometimes it is "the
  library solves a problem we don't have." [scope: dev]
```

**Placement caveat, load-bearing:** `LESSONS.md` is append-only newest-first, and Form A edits a
living script docstring. Neither is blocked, but Form A is the more checkable home — it sits where
the next person asking "why not just use a library?" will actually be standing.

---

## One thing this lane did NOT establish

The 20-fixture sample was chosen for *awkwardness*, not coverage — it is 20 of 204 `tasks/*.md` plus
18 `docs/intake/*.md`. The ruamel 20/20 result is strong evidence, **not a population proof**. If the
architect ever wants to act on ruamel's fidelity (rather than on the redundancy argument, which does
not depend on the sample), the cheap confirmation is to run the same round-trip over the **full**
corpus first. Flagging so the 20/20 is not later cited as if it were exhaustive.

---

## Method note

Read-only bounded probe. Libraries installed into a scratchpad venv only. Fixtures copied, never
moved. Root causes traced into library source rather than inferred from behaviour. No repo file was
created, edited, or deleted by this lane.
