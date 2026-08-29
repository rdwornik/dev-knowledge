---
date: 2026-08-29
class: technical
lane: lane-d-000-codex-fate
branch: worktree-lane-d-000-codex-fate
contract: docs/audits/2026-08-29-technical-batchd-launch-contracts/LANE-d-000-codex-fate.md
status: PAUSED — refuted premise (Q10)
---

# `codex/` fate — inbound reference map, and the premise the map refutes

Lane `lane-d-000-codex-fate`, step 1 of 3. The contract asks for the inbound-reference map
and a universalize-vs-delete decision taken **on** that map. The map is below. It does not
support either branch inside the lane's frozen write-scope, so step 2 is **not** executed and
the lane PAUSEs per the contract's Q10 clause.

## 1. What was verified first

| Claim under test | Source | Result |
|---|---|---|
| `codex/` holds exactly one file | `find codex -type f` | CONFIRMED — `codex/AGENTS.md`, sole entry |
| That file is 3,891 B | `wc -c` | CONFIRMED — 3,891 |
| Ratchet baseline is 443 | `silent_rule_detector.measure` | CONFIRMED — 443 |
| Contract handed = contract frozen | `diff` vs the committed copy | CONFIRMED — byte-identical, no drift |

The contract's factual premises hold. Its **decision** premise does not.

## 2. The inbound-reference map

Twenty-one citing sites across seven surfaces. Grouped by what a removal or a move would do
to each.

### 2a. Live code — a move breaks execution, not just prose

```
deploy/carrier_globalconfig.py:53   DEFAULT_SOURCE_REL = "codex/AGENTS.md"   # ADR-54
deploy/carrier_globalconfig.py:18   docstring: source_path: codex/AGENTS.md
deploy/tool.py:461                  "global-config": "copy hub codex/AGENTS.md -> ~/.codex/AGENTS.md"
```

`codex/AGENTS.md` is the **canonical deploy source** of the live `global-config` carrier
(ADR-54, Accepted 2026-05-19; carrier doctrine ADR-92, Accepted 2026-06-29). It is not an
orphan doc — it is the file that *becomes* `~/.codex/AGENTS.md` on an operator machine.

### 2b. Manifests — five versioned declarations plus a test fixture

```
deploy/manifest-v1.0.0.yaml:45      source_path: codex/AGENTS.md
deploy/manifest-v1.1.0.yaml:77      source_path: codex/AGENTS.md   (+ :230 source:)
deploy/manifest-v1.2.0.yaml:82      source_path: codex/AGENTS.md   (+ :299 source:)
deploy/manifest-v1.3.0.yaml:97      source_path: codex/AGENTS.md   (+ :317 source:)
deploy/manifest-v1.3.1.yaml:106     source_path: codex/AGENTS.md   (+ :326 source:)
deploy/manifest-v1.4.0.yaml:118     source_path: codex/AGENTS.md   (+ :458 source:)
tests/fixtures/manifest-v1.1.0-pre-essence.yaml:34   source_path: codex/AGENTS.md
```

Tagged manifests are **immutable version records**. Re-pointing them would falsify what those
versions actually declared; leaving them is correct and therefore the edge cannot be fully
retired by any act this lane could take.

### 2c. Tests — two files read the path live

```
tests/test_deploy_globalconfig.py:33   _GC_TARGET = {"source_path": "codex/AGENTS.md", ...}
tests/test_deploy_globalconfig.py:15   "the hub source (codex/AGENTS.md) is read LIVE so tests track the real"
tests/test_deploy_precommit.py:255     assert gc["target"]["source_path"] == "codex/AGENTS.md"
tests/test_agents_md_byte_cap.py:25    the tracked in-repo codex/AGENTS.md as the global stand-in
tests/test_agents_md_byte_cap.py:75    "it is the in-repo copy that makes the gate hermetic"
```

`test_agents_md_byte_cap.py` is the load-bearing one: the in-repo copy is what makes the
ADR-115 byte-cap gate **hermetic**. Remove it and the gate silently degrades to reading the
author's own machine.

### 2d. Canonical docs — a removal invalidates a required section

```
AGENTS.md:19,21,23   the ADR-115 §3.2 precedence table, naming codex/AGENTS.md BY NAME
ARCHITECTURE.md:335  canonical source `codex/AGENTS.md`; ADR-54
.methodology.yaml:134-135  authoring home is hub-local
protocols/PLAYBOOK.md:5186  canonical source tracked in `.dev-knowledge/codex/AGENTS.md` (ADR-54)
protocols/PLAYBOOK.md:5201  canonical source `.dev-knowledge/codex/AGENTS.md`, ADR-54
```

## 3. Three findings that refute the contract's premise

### F1 — The write-scope cannot reach the references the done-contract requires

Write-scope is frozen at `codex/**` plus **one** PLAYBOOK line. Done-contract #2 requires that
**every** inbound reference re-point and that none dangle. Sites in 2a–2d live in `deploy/`,
`tests/`, `AGENTS.md`, `ARCHITECTURE.md` and `.methodology.yaml` — **none of which is in
scope**. Done-contract #1 (the folder is gone either way) and done-contract #2 (nothing
dangles) are therefore **mutually unsatisfiable** inside the frozen footprint. Executing #1
alone would leave nineteen dangling references, a broken carrier default and at least three
RED tests.

### F2 — The write-scope's own PLAYBOOK grant is off by one

It grants "the single citing line only". PLAYBOOK carries **two** citing lines, 5186 and 5201.
Even the in-scope half of the re-pointing cannot be completed as written.

### F3 — The standing register already ruled, and ruled the other way

`protocols/STANDING_RULINGS.md` Z-G5 ("No single-file folders, ever", operator ruling
2026-08-29) is the very ruling the contract invokes. Read in full it says the opposite of what
the contract asserts:

- *"That directory is **not** free to delete"* — because root `AGENTS.md` documents it by name
  inside a section **ADR-115 §3.2 requires the file to carry**.
- *"the lawful discharge is **universalisation into the per-CLI instruction architecture**,
  not deletion."*
- *"Both options are costed **for the operator's cut** in the doctrine-consolidation arc's
  contract."*

So the register rules deletion unlawful and reserves the universalize-vs-delete cut **to the
operator**. The contract's done-contract #1 — "`codex/` is gone either way … the operator's
ruling is that single-file folders do not survive" — reads Z-G5's *general* rule while
dropping its *specific* carve-out for this exact directory, and pre-empts a cut the register
says is still pending. No recorded operator cut exists: `grep -n "universalis\|universaliz"`
over the register returns only Z-G5's own pending-state line and the unrelated R-2.

Corroboration, independent and same-day: C4's census
`docs/audits/2026-08-29-census-nb2-codex-surface.md:366` classifies this file
`PRECEDENCE-TRAP (+ BLOCKED-BY x6)` with **ZERO removal-ready** across 168 artifacts, and its
§383-389 note records that the bare-stem re-search found the live carrier the
precedence-framing alone would have missed.

## 4. Decision taken on the map

**Universalize-vs-delete is not decidable by this lane.** Not because the map is unclear — it
is unusually clear — but because:

1. **Delete** is ruled unlawful by Z-G5 and blocked six ways by the census.
2. **Universalize** is the lawful discharge, but every one of its re-pointing acts lands
   outside the frozen write-scope (F1), and the cut authorising it is reserved to the operator
   and unmade (F3).

Per the contract's Q10 clause — *"A lane that discovers a refuted premise PAUSEs with the
fact; deviation-with-disclosure is not a license"* — the lane stops here rather than
executing a deletion the register forbids or a re-pointing its footprint forbids.

This is decision class **(b)**, a genuine rule-vs-ruling conflict, and arguably **(c)** as
well — both inside the V-2 escalation budget, so escalating is the contracted act, not a
shortfall.

## 5. What the operator's cut needs to decide

Stated so the cut is a decision, not a re-investigation:

1. **Where does the deploy source live?** The census (§119) argues `codex/`'s placement is an
   "authoring-home accident" and that root `AGENTS.md:21` mischaracterises layers 1 and 3 as
   two authorities when they are the same content. A `deploy/`-adjacent home matches what the
   file *is*.
2. **Who may edit the blocked surfaces?** Universalisation needs `deploy/carrier_globalconfig.py`,
   `deploy/tool.py`, the in-flight manifest, `tests/test_deploy_globalconfig.py`,
   `tests/test_agents_md_byte_cap.py`, `AGENTS.md`, `ARCHITECTURE.md`, `.methodology.yaml` and
   **both** PLAYBOOK lines. That is a re-scoped lane, not a footprint amendment.
3. **Tagged manifests stay as-is** — they are immutable version records (2b).
4. **Root `AGENTS.md`'s precedence section must be rewritten, not just re-pointed** — ADR-115
   §3.2 requires the section, and the census found its stated *reason* wrong independently of
   this lane.

## 6. Ratchet

| Point | Count | Delta |
|---|---|---|
| Before | 443 | — |
| After | 443 | **0** |

Zero, as required against a baseline with no headroom. This artifact adds no `protocols/**`
prose; it lands in `docs/audits/`, and no token was spent.

## 7. Lane state

- **Step 1 (map + decision):** complete — the decision is that the cut is not the lane's.
- **Step 2 (execute + re-point):** **NOT executed** — PAUSED on F1/F3.
- **Step 3 (final):** not reached.
- `codex/AGENTS.md` is **unmodified**. `protocols/PLAYBOOK.md` is **unmodified**. The lane's
  diff is this artifact alone.
- No merge, no push to `main`, no JOURNAL entry, no index regeneration — per the contract's
  *What NOT to do*.
