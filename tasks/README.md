# tasks/ — the SOURCE OF TRUTH for the backlog (`BACKLOG.md` is generated from it)

> **This tree IS the source of truth. `BACKLOG.md` is GENERATED from it** — ADR-107
> strangler STEP 3, executed by [#439] on 2026-07-28 (ADR-101 amendment 2026-07-27
> sanctions this directory). **The arrow used to point the other way**; anything
> describing this tree as "derived", or `BACKLOG.md` as the source, predates the flip.
>
> **Edit here, then regenerate. Do not hand-edit `BACKLOG.md`** — it carries a
> generated-file banner and the next regen silently reverts anything written into it.

## The normal workflow

1. Edit a task's **body** in `<id>-<slug>.md` — the line below the frontmatter. That
   line is the authoritative text.
2. Run the regen:
   `uv run --locked python scripts/gen_task_tree.py --emit-source`
3. Commit the tree **and** the regenerated `BACKLOG.md` together.

`--emit-source` is a complete regen of the derived material: it re-renders each task
file's derived frontmatter, writes `BACKLOG.md`, and re-pins `manifest.json`'s
`generated_sha256`. It writes only what actually changed.

- **Verify:** `uv run --locked python scripts/gen_task_tree.py --check` — four legs:
  manifest structure resolves, every task file's frontmatter agrees with its own body
  and its manifest placement, the id agrees across filename/body/manifest (and no
  retired id is re-issued), and `BACKLOG.md` on disk equals what this tree generates.
  Armed as an `audit.py` ship-gate leg (`task_tree_coherence`), so drift blocks a ship,
  not just a test run.

## Two things that are NOT the normal path

- **`--write` is the IMPORT/RECOVERY direction** (`BACKLOG.md` → tree). It rebuilds the
  source from the generated file, so it **overwrites any tree edit not yet emitted**. It
  warns when run. Use it to bootstrap the tree or rebuild it from a `BACKLOG.md`
  restored out of git — not as a regen. Note it re-derives filenames from titles, so a
  title change emits a new slug and leaves the old file behind as a **rename remnant**
  that must be removed (it shares an id, which REDs the coherence gate).
- **`--prune` is REFUSED.** It used to delete a retired task's file. Post-flip that file
  *is* source, and deleting it also frees its id for re-issue. **Retire, never delete**
  (ADR-107 §6.3).

## Retiring a task

A task leaves the **queue**, not the tree: remove its node from `manifest.json` (it then
drops out of `BACKLOG.md` on the next `--emit-source`) and **leave its file in place**.
The file stays as the **allocation record** for its id. The coherence check treats an
unreferenced *engine-managed* file as a legitimate retired record and stays silent; an
unreferenced file **without** the provenance marker is reported as foreign, so "retired"
cannot become a hiding place.

**Honest limit — the ledger is not tamper-evident.** The gate REDs a re-issued id *while
the retired record is present* (active-vs-active and active-vs-retired are both caught).
It does **not** detect the record's **deletion**: nothing records that a given file ought
to exist, so deleting a retired file silently frees its id again. `next_free =
max(id in tasks/) + 1` is therefore trustworthy against accident and against concurrent
allocation, **not** against a deletion. ADR-107 §6.3 already states the directory "is not
complete today" as a ledger; closing that needs an explicit tombstone record and is
tracked as **[#440]**. Do not read a green gate as proof that no id has ever been dropped.

## Layout

One file per task — `<id>-<slug>.md`. The **body** below the frontmatter is the task's
`BACKLOG.md` line **verbatim** and is the authority. The **frontmatter is DERIVED** from
that body (plus the task's placement in the manifest, for `theme`/`story`): the byte-exact
`[#N]` id, `status`, `priority`, `size`, `theme`, `story`, `serialize-group`, and
`depends-on` — the raw value, never normalized ([#424]). Editing frontmatter by hand
achieves nothing and REDs the check; edit the body and regenerate. Each file carries
`generates: BACKLOG.md`, which is both its provenance and the engine-managed marker.

`manifest.json` (schema 2) is the other half of the source: it records ordering and every
non-task prose line, which is what makes the whole document reconstructible, and pins
`generated_sha256` — the output bytes this tree claims to produce.
