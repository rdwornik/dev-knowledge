# `.vscode` consumer write-through — sizing decision surface (W1 shelf-life 2026-08-13)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-28 · **Slug:** vscode-sizing-decision-surface
- **Returns to:** the operator. The W1 `.vscode` ruling (operator, 2026-07-19: `.vscode` is a SHARED FLEET
  CONFIGURATION the hub owns — `deploy/manifest-v1.4.0.yaml:13-15`) carries a **2026-08-13** shelf-life; the
  consumer write-through is the unbuilt half. This artifact prices the options. **Recommendation included;
  the decision is the operator's.**
- **Arc:** PROMPT P6 prep arc, branch `docs/p6-dated-pressure-prep`.

> **PREP, NOT EXECUTION.** Nothing is built, deployed, re-dated, or declared here. Live-state reads below are
> dated 2026-07-28; the deciding session re-verifies them.

---

## 1. What exactly is built (file:line)

- **The hub material:** `.vscode/settings.json` (3,847 bytes — the #312 Form-A boundary decoration: highlight
  keys keyed on the marker vocabulary, grey = `owner=hub` / navy = `owner=repo`, [#352] spec as corrected
  v2.44) + `.vscode/extensions.json` (526 bytes — the `fabiospampinato.vscode-highlight` recommendation).
- **The fleet declaration:** `deploy/manifest-v1.4.0.yaml:326-346` carrier `editor-config`
  (**`implemented: false`** at `:328` — "DECLARATION-ONLY at v1.4.0 … no carrier module writes it to a
  consumer yet … The consumer leg is the next ticket") + component `vscode-boundary-decoration`
  `:348-366` (kind config, verify hash, waivable).
- **The ticket that owns the consumer leg:** **[#371]** (`tasks/371-*.md`, [P2][S], serialize-group
  `settings-json`) — filed after the gap "sat untracked". Its recorded constraint is load-bearing:
  **"Vehicle decided by the buy-vs-build fleet-template ADR (intake pending) — do NOT implement bespoke
  (R7 pattern)."** ADR-93 constraint also recorded there: a write MERGEs into the consumer-authored
  `settings.json` (`files.watcherExclude` preserved), never clobbers.
- **One consumer already carries it — by hand:** ai-council adopted the decoration MANUALLY 2026-07-22 per
  operator GO (clause (f) of the [E8] closure contract: the boundary must be VISIBLE in the consumer),
  declared **DECLARED-UNTIL-MECHANISM** at `ai-council/.methodology.yaml:97-109`, ADR-93-conform merge done
  by hand. Live read 2026-07-28: `ai-council/.vscode/settings.json` = **2,280 bytes, 2 highlight keys**.
- **Stale-claim correction (flagged, not smoothed):** [#371]'s row text says "both consumers carry a
  77/72-byte `.vscode/settings.json` with zero highlight keys". True at its ~2026-07-20 filing; **stale for
  ai-council** since the 2026-07-22 manual adoption. Still true for corp-monorepo.

## 2. What exactly is unbuilt (file:line)

1. **No carrier module.** `deploy/tool.py:303-323` `make_carriers()` returns exactly five carriers
   (global-config, tier1-plugin, precommit, floor, enforcement-mesh) — no editor-config carrier exists; the
   manifest declaration has no executor.
2. **corp-monorepo has no decoration at all.** Live read 2026-07-28: `corp-monorepo/.vscode/settings.json` =
   **77 bytes, 0 highlight keys**. The W1 Done-when ("the operator opens any governed file in **any** repo and
   SEES which lines are methodology" — `BACKLOG.md:275`) is unmet for corp.
3. **The vehicle decision itself.** [#371] gates the mechanism on the buy-vs-build fleet-template ADR, whose
   intake precondition is **[#387]** ("rewrite the buy-vs-build intake before any ADR cites it" — open,
   unscheduled). Chain: [#387] → vehicle ADR → [#371] build. No date owns any link of it.

## 3. Effort class, with evidence

- **Mechanism build (the carrier): M.** A sixth Carrier class in `deploy/tool.py` at the peers' size, PLUS the
  one thing no existing carrier does: **ADR-93 merge-not-clobber JSON semantics** into a consumer-authored
  `settings.json` (the five existing carriers copy/generate whole artifacts they own — see `_APPLY_HINT`,
  `deploy/tool.py:337-343`; none merges into a consumer-authored file). Add tests, the `implemented:` flip,
  and a parity expectation, and it is a solid M — **and it is vehicle-gated by [#371]'s own recorded
  constraint**, so building it now means the operator overriding his own R7-pattern ruling or racing
  [#387] + a vehicle ADR inside 16 days.
- **Manual corp adoption (the ai-council precedent): S.** One hand-done ADR-93 merge into corp's 77-byte
  `settings.json` + `extensions.json`, one DECLARED-UNTIL-MECHANISM entry in corp's `.methodology.yaml`
  (template exists verbatim at `ai-council/.methodology.yaml:97-109`). Consumer-write rules apply (RULING-W
  worktree + consumer-leg merge delegation, PLAYBOOK:1239/:1274) — a bounded, precedented S. Note honestly:
  the 2026-07-22 operator GO named **ai-council**; corp needs its own word.

## 4. Risk of the 2026-08-13 lapse, in plain words

Nothing goes RED and no gate blocks. Three real costs:

1. Both consumers' `.vscode` e1 declarations expire (`corp-monorepo/.methodology.yaml:100` and
   `ai-council/.methodology.yaml:94`, both `review_date: 2026-08-13`) → `fleet_parity` flips them to
   **advisory-rewarn** — recurring advisory noise in every fleet digest until re-dated or resolved
   (mechanism: `2026-07-16-technical-fleet-structure-census.md` §declared-divergence — "a past
   `review_date`/`expiry` flips the finding to `advisory-rewarn` rather than clearing it").
2. **The operator's recorded deadline is missed on its own terms.** [E8] W1: "must land before the P4a
   `.vscode` ruling shelf-life 2026-08-13" (`BACKLOG.md:275`); W1 exists on operator priority precisely for
   visible results, and the visible half stays invisible in corp — the fleet's largest working repo.
3. [#352] carries "P4a, shelf-life 2026-08-13 (**revisit/kill if not advanced**)" — a lapse converts the row
   into a due revisit/kill decision on top of the build question.

## 5. Three options, priced

| Option | What lands by 08-13 | Effort | Risks / costs |
|---|---|---|---|
| **(a) Build-now (mechanism)** | The editor-config carrier, `implemented: true`, both consumers written through the tool | **M** | Overrides [#371]'s recorded "do NOT implement bespoke" vehicle constraint, or races [#387]+vehicle-ADR in 16 days; rework risk if the vehicle ADR later picks a template engine; largest diff surface (deploy tool + tests + parity) |
| **(b) Schedule-with-date (split visibility from mechanism)** | Visibility: the S-sized manual corp adoption per the ai-council precedent (needs a corp GO). Mechanism: scheduled behind [#387] → vehicle ADR with an explicit date; e1 declarations re-dated to that date | **S now + M scheduled** | The manual copy is a second hand-carried artifact until the carrier lands (drift risk is bounded by the hash-verify component once implemented); requires the operator to pick the mechanism date |
| **(c) Re-date-with-reason** | Nothing builds; e1 `review_date`s + the W1 deadline move out with a recorded reason | **~0** | The operator's most-repeated ask stays unmet in corp; W1 stays open past its own deadline; honest only if priorities genuinely changed |

**Recommendation (architect's, not a ruling): option (b).** The 2026-08-13 date was set to force the
*visibility* question, and visibility is deliverable at S by a precedent the operator already GO'd once; the
*mechanism* is gated behind his own recorded vehicle constraint and should keep its ordering rather than be
rushed or bespoke-built against [#371]'s text.

## 6. What the deciding session re-verifies

Both consumers' `settings.json` byte/key state · `make_carriers()` still five carriers · [#371]/[#387] still
open · the two `review_date: 2026-08-13` entries unchanged · whether a vehicle-ADR intake has appeared.
