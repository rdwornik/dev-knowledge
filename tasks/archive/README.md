# `tasks/archive/` — relocated row narration, byte-for-byte

> **This is not a graveyard and not a trim log.** Every byte in this directory was moved
> out of a live backlog row **verbatim**, and the row it came from is still open, still in
> the queue, and still points here. Nothing was condensed, summarised, rewritten, deleted
> or closed. `[#612]`; destination approved by operator decision **D3** (night-batch-2 GO,
> 2026-08-28).

## The doctrine

**The row carries a pointer; the record carries the record.**

A backlog row accretes dated-amendment narration because that narration had nowhere else
to go, so every condense pass bought a few sessions and the ceiling came back.
`protocols/STANDING_RULINGS.md` **B1** ("trim-vs-disposition") already measured which drain
works — *dropping the dated-amendment narration*, not sentence-level pruning — and this
directory is that drain performed **without the loss**.

Full rationale lives with the detector, at `scripts/validate_doc_rot.py`'s module docstring
("THE REMEDY DOCTRINE"). The mechanism lives at `scripts/archive_row_body.py`.

## Layout

One record per row, named by **id alone**:

```
tasks/<id>-<slug>.md   the live row      (source of truth, ADR-107)
tasks/archive/<id>.md  its archived narration
```

**Why the id and not the slug** — the obvious name is the row's own `<id>-<slug>.md`, and
the first build used it. It is wrong, for a reason the doc-rot suite already had a test
for: a slug derived from a title containing a date carries a date-shaped token (`[#492]`'s
slug ends `...-2026-08-07-mea`), so a slug-named pointer feeds
`validate_doc_rot._ARTIFACT_DATE_RE`'s bare-bundle-name alternative a token it strips as a
citation while no such bundle exists.
`test_citation_regex_strips_only_real_dated_artifact_identifiers` documents that hazard for
the one-line `BACKLOG.md` view and pins it for the canonical text — and it caught the
slug-named pointer importing the view's defect into the source. An id is unique by
construction (ADR-107 §6.3), can never carry a date, and makes the shortest pointer, which
matters because `worth_relocating` charges the row for its pointer's length. The pairing is
not lost: the record's `row:` frontmatter names its row path exactly.

The tree is flat by construction, which is why `validate_hermetization._HOME_PATTERNS`
admits the bare literal `tasks/archive` and not `tasks/archive/*` — a sub-directory here
would be a surfaced act, not a routine one.

A record carries frontmatter (`id`, `row`, `pointer`, `events`) and one `## Event N`
section per relocation act. Each event records the pre- and post-relocation row-body
digests and, per relocated clause, a `` ````text `` fence holding that clause on exactly
one line beside its own sha256. The fence is four backticks because the payload is verbatim
row prose that routinely contains inline backticks.

## Using it

```bash
# What could be relocated, and what it would buy (read-only)
uv run --locked python scripts/archive_row_body.py propose

# Relocate one or more rows
uv run --locked python scripts/archive_row_body.py relocate --id 146,277

# Re-derive the byte-identity proof for every record here
uv run --locked python scripts/archive_row_body.py verify

# tasks/ is the source of truth -- regenerate the view after any relocation run
uv run --locked python scripts/gen_task_tree.py --emit-source
```

`relocate` refuses, before writing anything, on every condition under which the act would
not be a lossless strict reduction: no eligible clause run, a clause carrying a structural
marker a gate reads, a change to any derived frontmatter field (title, status, priority,
size, `serialize-group`, `depends-on`), or a saving smaller than the pointer it costs. A
**retired** row — one no `manifest.json` node references — is never touched: that file is
an allocation record (ADR-107 §6.3), it is out of `BACKLOG.md` and out of `canonical_text`,
so it is not part of the doc-rot surface and rewriting it would be ledger tampering.

## What `verify` proves, and the one thing it cannot

Four legs, re-derived from the tree rather than read off a recorded verdict — **A**
clause-integrity (every stored clause hashes to its recorded sha256), **B** pointer-present
(the live row ends with the recorded pointer, exactly once), **C** lossless-reconstruction
(re-splicing the stored clauses into the live row reproduces the recorded pre-relocation
digest), **D** strictly-shorter.

**Honest limit.** Leg C is computable only while the live row still matches the
`body_after` digest its latest event recorded. Once a human edits that row again, the
pre-relocation body is no longer derivable from the working tree, and `verify` reports the
record **UNPROVEN (row edited since relocation)** — loudly, never as a silent pass and
never as a false FAIL. Legs A, B and D still bind, and the superseded proof stays checkable
in git at the relocation commit. This is a real gap in the standing proof and it is the
price of letting rows keep being edited.

## Recovering a row

Nothing here is lost, so recovery is a splice, not an archaeology dig:

```python
import archive_row_body as arb
rec  = arb.parse_record(Path("tasks/archive/146.md"))
body = arb._row_body(Path("tasks") / Path(rec.row_rel).name)
for ev in reversed(rec.events):
    body = arb.reconstruct_before(body, ev, rec.pointer)   # -> the original row, verbatim
```

For a **single-event** record — every record here today — that returns the original row
byte for byte. For a multi-event record it returns every clause of the original, but their
original **order** only if the row was not edited between relocations; each event is exact
about the body *it* acted on. A limit about order, never about loss.
