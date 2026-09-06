---
intake-id: 75
status: DRAFT
origin: Operator ruling DECLARE-SITTING-2026-09-06 item D15 ("FILE the intake DRAFT today (filings) ... Ratified next sitting"), executed under BATCH-2026-09-06-DAY-CONTRACTS section 4 item 2; account map witnessed rather than stated, per that item's explicit instruction
consumed-by:
---

# The `offload` role, and a witnessed account / token-scope map

> **Filing note (provenance, not content).** D15 ruled this **FILED today and RATIFIED NEXT
> SITTING** — so this document is a DRAFT on purpose and nothing in it is in force. The role
> shape below is D15's own wording; the account map is measured. Where this seat adds anything,
> it is marked as a filing note like this one.
>
> **`intake-id` allocation, and a COLLISION found while allocating it.** This takes **75**,
> under **D8** (*next-free across ALL refs, not `main` only*). The number moved twice, and the
> reason is the point:
>
> - Allocated **74** pre-sync, when ids 1-73 were occupied with no gap.
> - Syncing this lane with `main` (it was 59 commits behind) brought in
>   `2026-09-06-tech-derived-copies-registry.md` carrying **`intake-id: 72`** -- which **this
>   seat's own 027 intake already held**. A live duplicate, on the merged tree.
> - D8's rule decides it: **earlier-merged keeps the id.** `derived-copies-registry` is on
>   `main`; the 027 intake is not. So the 027 intake moved 72 -> **74**, and this one took **75**.
>
> **Two findings fall out of that, and neither is cosmetic:**
>
> 1. **Nothing catches a duplicate `intake-id`.** Both mandatory generators were run against the
>    colliding tree and **both wrote output without a word** -- `gen_intake_index.py` and
>    `gen_intake_tree.py` alike. The id is described in `docs/intake/README.md` section 3 as a
>    *stable integer, next free across all history*, but that property is **stated, not
>    enforced**. Two seats allocating on the same night collide silently.
> 2. **The renumber breaks two citations in an immutable artifact.**
>    `docs/audits/2026-09-06-technical-batch-t-close-packet.md` -- already on `main`, and audits
>    are immutable -- names *"filings-N's intake #72"* at lines 208 and 211. Applying D8 is
>    correct and still leaves those lines pointing at a number the file no longer carries.
>    Recorded rather than quietly absorbed; the file *name* in those citations still resolves.
>
> **Reversible for one frontmatter line plus a regeneration, and only until this lane merges.**
> If the operator would rather the landed file move and the 027 intake keep 72, it is a
> two-minute change. See `QUESTION-filings.md`.

## 1 · The role, as D15 states it

An `offload` seat is a **read-only thinking** role:

- **ranked retrieval with locators** — it returns candidates and where they live
- **never a verdict** — it does not rule, close, merge, or dispose
- **carried-by: manifest** — consumers receive the role definition the same way they receive
  the rest of the methodology

**Admission is by seeded-defect measurement**, not by argument: the role is admitted if it finds
seeded defects at a rate that justifies its cost, measured, not asserted.

Two mechanism requirements D15 names:

- a **`-Model` / provider selector reaching the dispatch line**, so the seat's model is chosen
  at dispatch rather than inherited by accident
- **"tokens saved" as a scorecard line**, so the claim the role exists to make is one of the
  numbers the scorecard already reports

> **Filing note.** The scorecard is `scripts/window_metrics.py`. Lane 3.9's salvaged
> `collect_scorecard()` returns each row as `{value, basis}` and reports `NOT COMPUTED` with a
> reason rather than inventing a number — so "tokens saved" can be added as a row that honestly
> says it is not yet computed, instead of waiting for telemetry that does not exist.

## 2 · The account and token-scope map — MEASURED, not stated

> **How this was witnessed.** Remotes read from each repository's own `.git/config` under
> `Dev/`; accounts and scopes from `gh auth status`. **No token value is recorded here and none
> was read** — `gh` masks them by default and `--show-token` was not used.

### 2.1 Repositories under `Dev/` and their origin

Every repository resolves to the **same owner**, `rdwornik`, on `github.com`:

| Repo (`Dev/`) | origin owner/repo |
|---|---|
| `.dev-knowledge` | `rdwornik/dev-knowledge` |
| `ai-council` | `rdwornik/ai-council` |
| `corp-monorepo` | `rdwornik/corp-monorepo` |
| `corp-ops` | `rdwornik/corp-ops` |
| `corp-sca-time-automation` | `rdwornik/corp-sca-time-automation` |
| `demo-prep` | `rdwornik/demo-prep` |
| `life-architect` | `rdwornik/life-architect` |
| `terminal-setup` | `rdwornik/terminal-setup` |
| `win-tooling` | `rdwornik/win-tooling` |

**10 repositories carry an origin** (the nine above plus this hub's own worktree checkout
resolving to the same `rdwornik/dev-knowledge`). Six further directories under `Dev/` are **not
repositories** and have no remote: `.archived`, `.backups`, `.claude`, `.settings`, `_scratch`,
`illustrated-book-gen`, `overnight`.

### 2.2 Logins and token scopes

| Account | Active | Scopes |
|---|---|---|
| `rdwornik` | **yes** | `admin:public_key`, `codespace`, `gist`, `read:org`, `repo`, `user`, `workflow` |
| `Robert-Dwornik_ghub` | no | `codespace`, `gist`, `read:org`, `repo`, `workflow` |

**The two differ by exactly two scopes**: the active account additionally holds
`admin:public_key` and `user`. Both hold `repo` and `codespace`.

### 2.3 Three observations the map makes available

> **Filing note.** These are observations from the measurement, not proposals. A ratifying reader
> should treat them as things to check, not as recommendations this seat is making.

1. **The second login owns no remote in `Dev/`.** Every origin resolves to `rdwornik`. So
   `Robert-Dwornik_ghub` is authenticated but is not the owner of anything currently checked out
   here — which means a routing decision that assumes two account "halves" of the fleet has no
   basis in the remotes as they stand.
2. **Both accounts hold `codespace`.** Codespace dispatch is therefore not gated by which login
   is active, and a substrate decision cannot be explained by scope alone.
3. **Scope is not the same as reach.** Holding `repo` does not tell you what a token can *see*;
   a separately-recorded fact is that the cloud token is hub-scoped, so a fleet arc cannot route
   cloud work to a sibling repo. The map answers "what is authenticated", never "what is
   reachable" — those are different questions and only the first is measured here.

## 3 · What this document does NOT do

- It **rules nothing**. D15 ruled it FILED today and RATIFIED NEXT SITTING.
- It **proposes no owner** for the role and **admits nothing** — admission is by the
  seeded-defect measurement named in section 1, which has not been run.
- It does **not** add the table to `protocols/OPERATOR-INTERFACE.md`. D15 and the day contract
  both route the table there; that edit is a separate act on a repo file, and this intake is the
  requirements record, not the carrier.

> **Filing note, declared against this seat's own next act.** The `OPERATOR-INTERFACE.md` edit
> named above will add normative tokens to the one file that recently entered the silent-rule
> detector's scope carrying **+4** — an increase that never fired the ratchet because unrelated
> deletions offset it. That is recorded as a finding for the ratifying reader, not as an
> objection: the gate measures **net pool growth**, not additions, and it behaved to contract.
