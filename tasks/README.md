# tasks/ — DERIVED task tree (source of truth: BACKLOG.md)

> **This tree is DERIVED. `BACKLOG.md` is the SOURCE OF TRUTH** — [#433]
> restructure strangler STEP 1–2 (ADR-101 amendment 2026-07-27 sanctions this
> directory). The source-of-truth flip is a later, separate arc: until it
> lands, edit `BACKLOG.md` and regenerate; never hand-edit files here.

- **Regenerate:** `uv run --locked python scripts/gen_task_tree.py --write`
- **Verify:** `uv run --locked python scripts/gen_task_tree.py --check`
  (regen-and-diff over every task file + `manifest.json`, plus a full disk
  reassembly proving `BACKLOG.md` is byte-identically reconstructible from
  this tree)

**Layout:** one file per task — `<id>-<slug>.md`. Frontmatter carries the
byte-exact `[#N]` id plus conservatively derived fields (`status`, `priority`,
`size`, `theme`, `story`, `serialize-group`, `depends-on` — the raw value,
never normalized). The body below the frontmatter is the task's `BACKLOG.md`
line **verbatim** — zero content edits, zero reformatting. `manifest.json`
records ordering and all non-task prose, making the whole source file
reconstructible.
