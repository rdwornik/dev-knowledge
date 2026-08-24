---
intake-id: 45
status: READY
origin: integrator, 2026-08-24 batch close (mandate item M12); substrate facts measured across this batch's local, cloud and devcontainer lanes
---

# M12 — a lane is dispatched to one of THREE substrates, and nothing declares which

## Problem / motivation

Lane dispatch currently assumes a two-way world (here vs. cloud). The batch just closed proves
there are **three** substrates with materially different capabilities, and the differences are
not written down anywhere a generator or an executor can read:

| Substrate | Dispatch | Reaches | Measured properties |
|---|---|---|---|
| `local` | `Dispatch-Lane` | worktrees, reviewer CLIs, `~/Downloads` | full gate mesh armed; operator disk reachable |
| `cloud-session` | `Dispatch-CloudV2` | Anthropic cloud | **unpinned `uv`; no `click`; NO ARMED HOOKS; shallow clone** |
| `devcontainer` | `gh`-driven | Codespaces (`[#554]`) | container spec in `.devcontainer/`, read by a container runtime, carries no organ |

The `cloud-session` row is not a theoretical concern. **No cloud lane's commits passed a gate in
this batch, because no hook was armed in any container** — which is why the batch contract had to
instruct the integrator to re-run the mesh locally against every cloud branch before merging.
That instruction worked, and it found real defects: lane C1 shipped a new
`docs/audits/*.md` artifact **without regenerating the generated index**, a miss its container
had no hook to catch. The integrator regenerated it at merge.

So the compensating control exists, but it lives in **prose in a hand-written batch contract**.
If a future contract omits that paragraph, unpinned cloud output merges ungated and nothing
says so.

## Scenarios (+1 view)

- A contract dispatches a lane to a cloud session and says "run the gates before you finish".
  The container has no armed hooks and no `click`, so the lane cannot run them and reports green
  on a mesh it never executed.
- `gen_lane_contract` emits a contract naming a worktree for a lane that will actually run in a
  container, because nothing tells it the substrate differs.
- An integrator inherits nine branches and has to *know*, from outside the artifacts, which came
  from an ungated substrate.

## Functional requirements

- **Must:** a lane's substrate is declared, machine-readably, at dispatch.
- **Must:** the declaration carries the substrate's capability facts — at minimum whether the
  gate mesh is armed — so a consumer can derive the compensating control instead of remembering
  it.
- **Should:** `gen_lane_contract` consumes the declaration and emits the right dispatch shape.
- **Could:** the integrator's merge queue derives "needs a local mesh re-run" from the
  declaration rather than from contract prose.

## Acceptance criteria (ex-ante)

1. A single machine-readable source names the three substrates and their capability facts; no
   second copy exists in prose.
2. `gen_lane_contract` reads it, and a test asserts a cloud-substrate contract emits the
   mesh-re-run obligation without the author typing it.
3. A contract naming a substrate outside the enum is refused, the way the branch-prefix enum is
   the checkable surface for lane names.

## Non-goals

- Changing what any substrate *is*, or adding a fourth.
- Re-opening the 2026-08-20 substrate ruling (stay on Codespaces free 4-core). This is about
  declaring what exists, not choosing between them.

## Impact sketch (4+1 lite)

- **Logical:** substrate becomes a first-class property of a lane rather than an unstated
  assumption in whoever wrote the contract.
- **Process:** the "re-run the mesh for cloud lanes" rule stops depending on the contract author
  remembering it.
- **Development:** a config file plus a `gen_lane_contract` consumer; ADR-101 already sanctions
  `ecosystem/` and `.devcontainer/`.
- **Physical:** one new declared file, or an ADR appendix.

## Open questions

- **Fork: a machine-readable config consumed by `gen_lane_contract`, or an ADR with the table as
  an appendix.** The config is checkable and the generator can act on it; the ADR is
  authoritative but inert — `gen_lane_contract`'s own honest limit is that it checks SHAPE, never
  whether a contract's claims are true, so an inert table would not change that.
- Where does the config live — `ecosystem/` (alongside `provider-registry.yaml` and
  `tool-versions.yaml`, the established home for declared ecosystem state) or `deploy/`?
- Does the substrate declaration bind consumer repos, or is it hub-only like most of the batch
  machinery?

## Status

READY — filed by the integrator at the 2026-08-24 batch close. Fork named, no row banked.
