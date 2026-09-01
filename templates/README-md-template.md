---
last_reviewed: <YYYY-MM-DD>
status: <active | maintenance | archived>
owner: <Rob | other>
---

# `<repo-name>`

> **Root front door.** The first file a human opens. What this is, why it exists, how to start,
> and where to go deeper — in that order, and nothing else.
>
> **Working here?** `CLAUDE.md` is the session contract, `AGENTS.md` the portable
> build/test/land layer every provider reads, `ARCHITECTURE.md` the structural map.

## Applicability

**This template is the fill-in counterpart to the hub's own root `README.md`**, in the same
relation `templates/intake-template.md` has to `docs/intake/README.md`. It exists because the
`readme-front-door` deploy carrier ships **repo-specific** content: a verbatim copy of the hub's
own front door would carry the hub's title, its strategic emphasis and its relationships into a
consumer, which the manifest calls *"not a migration, a mis-carry"*. A template is the thing a
carrier can ship; a front door is not.

**Genre — the load-bearing constraint, ruled by the operator (R-README, 2026-09-01).** The README
is the HUMAN front door. **Fleet-internal governance states do not live here** — parity postures,
member statuses, migration order, deployment sequencing and "which repos are in or out" belong on
an `ecosystem/` surface beside the roster they qualify. A reader arriving at the front door does
not need them in order to start, and a governance state restated here becomes wrong in a second
place the moment the surface that computes it moves.

**Two conventions inherited from `CLAUDE.md` §4, restated because a front door invites breaking
both.** A count or a roster is cited, not retyped — point at the surface that computes it. And a
locator is resolved before it is written down.

---

## What this is [CORE]

`<One paragraph, present tense. What the repo IS and what it does — the answer someone needs`
`before they can decide whether to keep reading. No history, no roadmap, no aspiration.>`

## Why it exists [CORE]

`<One or two paragraphs. The problem this repo solves and for whom. If the repo would be`
`difficult to justify without this section, that is a signal about the repo, not the section.>`

## How to start [CORE]

`<The shortest path from a fresh clone to something working. Prefer three commands that run over`
`three paragraphs that describe. Name the declared environment rather than assuming one:>`

```bash
<dependency install / environment rebuild — e.g. uv sync --locked>
<the suite — e.g. uv run --locked pytest -x --tb=short>
<the entry point, or the command that proves the install>
```

`<If a gate has to be armed once per clone, say so here — a guarantee that arms itself only on a`
`fresh install is a guarantee a second clone does not have.>`

## Where to go deeper [CORE]

| If you want | Read |
|---|---|
| The session contract for an agent working here | `CLAUDE.md` |
| The portable build/test/land facts | `AGENTS.md` |
| The structural model | `ARCHITECTURE.md` |
| What changed and when | `JOURNAL.md` |
| What is pending | `BACKLOG.md` |
| Decisions and their reasoning | `docs/decisions/` |
| `<repo-specific surface>` | `<path>` |

## Scope

**In scope:** `<the two or three things this repo owns.>`

**Out of scope:** `<what belongs elsewhere, with the elsewhere named. This half earns its place:`
`a boundary stated once here saves the argument each time it is tested.>`

## Relationships

`<How this repo relates to its siblings — as FUNCTIONAL ROLES, not authority. Cite the registry`
`for who the members are rather than listing them; the list moves and this file does not.>`

→ Fleet roster, member status and migration posture: `ecosystem/registry.md` *(hub only)*

## Lifecycle

**Review triggers** (not deadlines): `<major shift · new consumer · scope reinterpretation ·`
`the "what this is" section reading as already-realized>`

**Ownership:** `<owner>` · **Edit process:** `<how a change to this file is decided>`

---

**Last updated:** `<YYYY-MM-DD>`
