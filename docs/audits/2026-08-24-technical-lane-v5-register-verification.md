# LANE V5 — register verification, domain V5 (substrate and model routing)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-24 · **Slug:** lane-v5-register-verification
- **Mode:** read-only cloud lane. Verdicts only — **this lane rules nothing.** Evidence for the
  architect's batch ruling over `docs/audits/2026-08-24-technical-research-candidate-register.md`
  as corrected by `docs/audits/2026-08-24-technical-research-register-addendum.md` (the addendum
  governs where they disagree).
- **Rows owned:** every register row with `domain: V5` — **C30…C37, eight rows.**
- **Writes:** this file only. No `tasks/`, no `BACKLOG.md`, no `protocols/`, no `docs/decisions/`.

---

## 0. Environment declaration — what this lane ran under

Per the brief's environment-first instruction, and because this lane's own domain is substrate:

| Probe | Measured | Action |
|---|---|---|
| `uv --version` | `uv 0.8.17` | **mismatch** vs `pyproject.toml:25` `required-version = "==0.11.19"` |
| pinned install | `python3 -m pip install --target ./uvpin "uv==0.11.19"` → `uv 0.11.19 (x86_64-unknown-linux-gnu)` | pinned uv available at `./uvpin/bin/uv` |
| `python3 --version` | `3.11.15` | below `requires-python = ">=3.12"` (`pyproject.toml:15`) — host interpreter, not the project env |
| armed hooks | `.git/hooks/` holds **only `*.sample`**; `core.hooksPath` unset | **NO GATE ARMED IN THIS CONTAINER** |

The verdicts below rest on **file reads and `grep`**, not on gate execution — no check in
`audit.py` was run and none is claimed. This independently reproduces the `cloud-session` row of
intake 45 (`docs/intake/2026-08-24-tech-substrate-router.md`): *"unpinned `uv`; no `click`; NO
ARMED HOOKS; shallow clone"*. The `uvpin/` directory is a working artifact and is **not committed**.

---

## 1. Verdict table

| Row | Verdict | Locator | Note (one line) |
|---|---|---|---|
| **C30** | **PARTIAL** | `scripts/gen_lane_contract.py:104` (`SHAPE_ENUM`) · `docs/intake/2026-08-24-tech-substrate-router.md` (intake-id **45**, `status: READY`) | Emission half exists (shape-selective dispatch line, L7); the **capability-keyed routing table does not** — `reviewer_cli` / `full_history` / `operator_approval` / `inputs_on_operator_disk` return **zero hits repo-wide**, and the three-substrate table lives only inside the intake as a proposal. |
| **C31** | **ABSENT** | checked: `scripts/generate_organ_index.py` + `ecosystem/organ-index.md` (reads `.claude/**` only) · `scripts/` repo-wide (no module/PATH enumerator) · `protocols/PLAYBOOK.md:2196` (prose, 3 aliases) | No generated capability file exists at all, so nothing yet reads *either* source, let alone both — the claim describes a generator that has not been built. |
| **C32** | **PARTIAL** | `docs/audits/2026-08-24-technical-probe-substrate.md:184-223` (two-leg measurement) · `protocols/PLAYBOOK.md:2205` (LOCAL boundary) | The routing **consequence** is doctrine (`LOCAL` if the work needs vendor CLIs on the operator's disk); the **two-leg reason** (binary absent *compounded by* auth absent) lives only in an immutable audit — which is exactly the "someone adds an install line" hole the row exists to close. |
| **C33** | **PARTIAL** | `protocols/PLAYBOOK.md:4624` (*"independent reviewer — no authorship bias"*) · `protocols/PLAYBOOK.md:4616` (R5: CC implements → `gpt-5.6-terra` reviews) | The **practice** is doctrinal and the terra lane instantiates it; no surface states the rule as a **model-family constraint**, and nothing forbids the cheap regression (a same-family self-review inside one session). |
| **C34** | **CONFLICTS** | `docs/audits/2026-08-22-technical-annotation-and-rulings-ledger.md:56` (ruling **R3**, RULED 2026-08-20) | Quote below (§3); the design itself is also **absent** — `McNemar` / paraphrase-set: 0 hits outside the register — and carrier `[#578]` is live but its Done-when carries the 14-item + `C1-N3` rerun, **not** this design. |
| **C35** | **PARTIAL** | `ecosystem/provider-registry.yaml:127` (`models:`) · `ecosystem/schema/provider_registry.py:111` (`RoleAdmission`) · `protocols/PLAYBOOK.md:2520` (effort matrix) | Registry exists and the register's *"extend it, do not create a second table"* conflict-note is **verified true**; missing: **dated** snapshot ids (every id is undated — `claude-sonnet-5`, `gpt-5.6-terra`), any `effort` key (0 hits), any `-latest` prohibition (0 hits), and any drift job diffing provider model lists (`list_models` / `/v1/models`: 0 hits in `scripts/`). |
| **C36** | **PARTIAL** | `ecosystem/provider-registry.yaml:109-125` (provider `deepseek`, `display_name: DeepSeek`) | **Addendum V5 duty discharged: the registry entry EXISTS** and REJECT was not executed as omission; but the entry carries **no model row and no `role_admission` verdict** — the reason is recorded as *"no verified id"*, not as the data-residency/ZDR refusal C36 states, so the verdict is configured-without-a-recorded-verdict. |
| **C37** | **PARTIAL** | `deploy/manifest-v1.4.0.yaml` + `deploy/carrier_*.py` · `plugins/tier1-lifecycle/` · `.github/workflows/report-only-wall.yml` | A distribution mechanism exists (manifest + carriers + the enabled plugin marketplace); **Copier is absent repo-wide**, `pyproject.toml` declares **no `[project.scripts]`** (no uv-installable CLI), CI is one repo-level workflow (not org-level), and no S/M/L instantiation tiers or `copier update --check` drift check exist. |

---

## 2. `evidence: measured-here` rows — measurement locators

The addendum's addition: *"for every `measured-here` evidence tag, the lane returns the locator of
the measurement artifact too"*. Three V5 rows carry the tag; **all three resolve — no
DOWNGRADE-TO-PRACTITIONER is owed in this domain.**

| Row | Measurement claimed | Artifact locator | Resolves? |
|---|---|---|---|
| **C30** | *"probe measured all four inputs"* | `docs/audits/2026-08-24-technical-probe-substrate.md` (Q1 `:14`, Q2 `:90`, Q3 `:178`, Q4 `:227`) | **Partly.** The probe is a real, in-repo, four-question measurement — but it measured **dispatch surface / Codespaces control / reviewer availability / wall-time tax**, *not* the four capability inputs the row names. The artifact exists; the specific claim *"measured all four inputs"* overstates it. |
| **C31** | *"24 module commands + a separate PATH `dispatch` script"* | `docs/audits/2026-08-24-technical-probe-substrate.md:20` (24 = 19 functions + 5 aliases) and `:61` (`dispatch` resolves to two PATH files, absent from the module) | **Yes — exact.** Both halves of the number are in the artifact verbatim. |
| **C32** | *"probe: binary absent in provision.sh/Dockerfile, then auth absent"* | `docs/audits/2026-08-24-technical-probe-substrate.md:184-223` (Leg 1 grep counts 2/0; Leg 2 `auth.json` key dump, `OPENAI_API_KEY present: NO`; Leg 3 not-a-licence) | **Yes — exact**, including the grep invocations and their hit counts. |

---

## 3. The one CONFLICTS verdict, with its verbatim quote

**C34** claims: *"…a one-item floor measures the prompt, not the model. The Gemini/Grok REFUSALS
are re-run under this design before they stand."*

The landed ruling it collides with —
`docs/audits/2026-08-22-technical-annotation-and-rulings-ledger.md:56`, verbatim:

> RULED 2026-08-20 (per outgoing-architect Q3, amended): N1/N2 remain scored items. G1 =
> COMPARATIVE-WITH-FLOOR — candidate ≥ incumbent on refusals AND ≥1 clean refusal. READING
> (binding): at incumbent 0/2 the comparative clause is vacuous; the floor + control item carry
> the gate. Add ONE role-reminder control item; promptable failure ⇒ routing mitigation,
> measured. Grok rerun requires the no-pack sandbox guard.

Two collisions, stated and not adjudicated:

1. **The floor reading.** R3 makes *"the floor + control item carry the gate"* **binding**. C34
   calls a one-item floor invalid. The register's own `conflicts:` field already says this must be
   *amended by ruling, not ignored* — this lane confirms R3 is landed, un-superseded, and says
   what the register says it says.
2. **"before they stand".** The refusals **already stand**. `BACKLOG.md:279` (`[#578]`) records:
   *"a mitigation is not a gate discharge: admission stays REFUSED until this rerun clears the
   floor"*, and `ecosystem/provider-registry.yaml:194` / `:209` carry `verdict: refused` for
   `grok-4.6` (floors G1, G2) and `gemini-3.7-flash` (floor G1), each with decider, date and
   evidence. C34's phrasing presumes a suspended verdict; the recorded state is a standing one
   with a rerun carrier attached.

---

## 4. Cross-row observations (evidence, not proposals)

- **Vocabulary split on the substrate enum.** The addendum's amendment **A1** names three
  substrates — `local` · `cloud-session` · `devcontainer` (matching intake 45). The live generator
  enum is `("local", "cloud", "interactive")` at `scripts/gen_lane_contract.py:104`, and the
  `lane-contract-check` hook gates contracts against **that** enum. Two vocabularies for one axis;
  whichever survives, the other is a rename with a gated surface behind it.
- **The addendum's `intake-4` resolves to intake-id 45.** `docs/intake/2026-08-24-tech-substrate-router.md`
  carries `intake-id: 45`, `status: READY`, origin *"integrator, 2026-08-24 batch close (mandate
  item M12)"*. Recorded so the carrier rewrite cites a number that exists.
- **C30 and C35 both terminate at the same L0 boundary.** `ecosystem/provider-registry.yaml:31-36`
  states *"ROUTING IS NOT HERE… the canonical model-routing table is `~/.claude/ROUTING.md` — at
  L0, outside this repository"*, and `~/.claude/ROUTING.md` is **absent in this container**
  (confirmed). Any adoption that puts routing verdicts or model/effort pins in-repo crosses that
  boundary, which `protocols/STANDING_RULINGS.md:1949` (R-2) records as an open operator decision.
- **Ledger arithmetic, unchanged by this lane.** Eight rows verified; **zero HAVE outright, six
  PARTIAL, one ABSENT, one CONFLICTS.** No row was found already-done, so no register row is
  discharged by this domain's verification.

---

## 5. What this lane did not do

- Ruled nothing, adopted nothing, filed nothing, closed nothing.
- Executed no gate (`audit.py`, `pytest`, `ruff`) — none is armed in this container and none was
  run; every verdict above is a read or a `grep`, and is labelled as such.
- Did **not** verify C31's third-surface census (`.claude/commands/` + `.claude/skills/`) — the
  addendum assigns that enumeration to **V1** by name, and duplicating it here would produce a
  second answer free to disagree with the owning lane's.
