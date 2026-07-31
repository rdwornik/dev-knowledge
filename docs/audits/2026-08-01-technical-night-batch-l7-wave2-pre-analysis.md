# Night batch 2026-08-01 — L7: wave-2 [#462] pre-analysis (SKETCH)

> **This is a SKETCH, not a contract.** Nothing here is a ruling, a Done-when, or a frozen scope.
> The wave-2 frozen contract is authored by the architect, not by a night batch. Findings are framed
> as *"the architect would need to decide X"*, never *"X is decided"*.

**Status: PROPOSAL — capacity-permitting lane, delivered.** Read-only; `git status --porcelain`
empty at lane close.

---

## One-line finding

[#462]'s Done-when has **two clauses with radically different costs**:

- **Clause 1** — the wave-1 member set includes `terminal-setup` → **data-only, satisfiable in
  schema v1 exactly as shipped, zero schema change.**
- **Clause 2** — the wave-1 census diffs the declaration against machine surfaces → **not
  satisfiable as shipped.** There is no loadable source today representing "the ADR-104/VISION
  declaration," so there is nothing for a machine surface to be diffed *against*.

**That gap — not the missing registry row — is the real work.**

---

## Timeline (why the reframe is real, not editorial)

`docs/audits/2026-07-30-conformance-nightly-digest.md:97-104` (finding N4) and
`docs/audits/2026-07-31-conformance-nightly-digest.md:80-86` (finding S3) **independently** found
`terminal-setup` missing from `registry.md`, and both proposed the same cheap fix: "add a row."

ADR-109 ratified the same day; §2 retires `registry.md`'s authority (`ADR-109:64-67`). [#462], filed
that night, **explicitly overrides both proposed fixes** on ADR-109 §2 grounds
(`tasks/462-*.md:13`, restated verbatim at
`docs/handoffs/2026-08-01-dev-knowledge-architect/RESIDUAL.md:144-147`).

---

## Q1 — Which machine surfaces exist to diff a declaration against?

The loader's seven sources (`scripts/desired_state_loader.py:308-319`):

| source | ADR-109 §2 status | `terminal-setup` present? |
|---|---|---|
| `ecosystem/registry.md` | RETIRED as authoritative | **No** — 8 data rows (`:24-31`), none |
| `ecosystem/index.yaml` | RECLASSIFIED observed-state input | **No** — 6 repos populated |
| `ecosystem/deployed-versions.yaml` | kept as STATE file + membership tie-break anchor (**not** one of "the four") | **No** — 5 keys (`:24-49`) |
| `ecosystem/parity-surfaces.yaml` `fleet:` | ABSORBED | **No** — 5 entries (`:98-103`) |
| `ecosystem/satellite-onboarding-rulings.yaml` | ABSORBED | **No** — 4 rulings (`:27-69`) |
| `.methodology.yaml` | not repo-keyed | n/a |
| `deploy/manifest-v1.4.0.yaml` | not repo-keyed | n/a |
| `ecosystem/<repo>/` state dirs | unread by any checker | **No** dir exists |

**All five repo-keyed operational surfaces agree by omission.** This is the same five-way membership
disagreement the registry-prep dossier already names as **C1**
(`docs/audits/2026-07-31-technical-382-registry-prep-dossier.md:236-243`) — [#462] is simply that
defect with a worked example attached.

### Where the declaration actually lives — and why that is the problem

Only in `ADR-104:15` (immutable ADR prose) and `VISION.md:107-114` (living-doc prose). **Neither is
YAML, and neither is a regex-parseable table** like the five loaded sources.

`SourceSurface` (`ecosystem/schema/desired_state.py:84-88`) has four closed values —
`registry | parity | onboarding-ruling | deployed-version` — **none meaning "ADR/VISION
declaration."** `RefKind` does carry `adr` (`:208`), but that is for citing an ADR as *provenance* on
some other fact, not for loading ADR prose as a fact source. Different job.

---

## Q2 — What would the declaration schema need?

1. **A new `SourceSurface` value** (e.g. `fleet-declaration`) — additive, low risk.
2. **A new loader step parsing ADR-104/VISION prose into repo ids** — a genuinely new parser *class*
   (free prose, vs. the YAML/one-table sources that exist). The architect's real choices:
   (a) brittle regex over ADR-104's sentence; (b) restructure `VISION.md` into a parseable block;
   or (c) a new persisted `ecosystem/fleet-declaration.yaml`.
   > **Option (c) directly collides with a named ADR-109 §9 rejection** — *"A new persisted
   > desired-state file in v1 — rejected"* (`ADR-109:265-266`) — and with its §8 F2 new-surface
   > discipline (`:248-250`). That is reopening a settled point, not a detail.
3. **A `LifecycleStage` / axis question.** The current four values
   (`source | unonboarded | floor_only | full`, `:68-72`) all presuppose *some* registration exists;
   `terminal-setup` has none anywhere. Whether "declared-only" is a fifth stage value or a **separate
   axis** (parallel to the D2 precedent that ruled `role` non-lifecycle-bearing, `ADR-109:196-202`)
   is open — and getting it wrong repeats the exact C3/G4 conflation ADR-109 exists to dissolve.
4. **A report/verdict axis for "declared, present nowhere."** `build_matrix`
   (`scripts/desired_state_report.py:120-140`) only ever iterates `resolve_fleet_members(...)` — so a
   repo absent from that set **never appears in the report at all, by construction**. No
   `DivergenceKind` or verdict token today means this.
5. **`resolve_fleet_members`** (`scripts/desired_state_loader.py:336-339`) resolves membership toward
   `deployed-versions.yaml` keys only — **a named ADR-109 §2 ruling, not incidental code.** Widening
   it to include "declared" repos *revisits that ruling*; it is not a field addition.
6. **Breaking vs additive.** New enum members and new default-valued fields are additive; v1 persists
   no document yet (`ADR-109:87-91`), so even a "breaking" model change today costs a revision to the
   loader's single `Repo(...)` call site plus tests, not a migration (`ADR-109:283-285`, verbatim).
   **Genuinely open:** does an additive-only change still need a `SCHEMA_VERSION` bump, per the ADR's
   *"v2 is a declared change"* wording (`:285`)? Ambiguous as written.
7. **The generality clause (§4) is a different axis — do not conflate.** §4's discharge
   (`ADR-109:287-339`, the `docs/intake/` split, commit `9a75777`) is scoped to the
   monolith-splitting **engine pattern**. It says nothing about whether the loader's *source
   coverage* extends to prose-shaped sources. That question is neither pending nor discharged — it
   was never raised.
8. **Naming collision worth catching early.** [#383]'s own enumerated surfaces
   (`tasks/383-*.md:14`) — caches, `.claude`+skills, archives, docs layout, Python parity,
   colours-via-carrier — do **not** include fleet membership; and "[#383] wave 1" is already a spent
   identifier for the §4 discharge. What [#462] calls "the wave-1 member set" may need a **new named
   surface**, not literally wave 1.

---

## The cheapest available answer (tell the architect this exists)

**Clause 1 — yes, data-only.** `terminal-setup` can become a *fact* via any of the five repo-keyed
sources, with zero schema change. Becoming a **resolved member** additionally needs a
`deployed-versions.yaml` entry, which is gated by that file's own write-contract on a real deploy or
an operator-sanctioned exception (precedent: the `corp-monorepo` `gate_rev_ahead` block,
`ecosystem/parity-surfaces.yaml:416-435`).

**Clause 2 — no.** Needs the Q2 items, at least one of which reopens a settled ADR-109 rejection.

**Suggested shape (architect's call):** split [#462] so clause 1 closes cheaply now and clause 2
carries the honest wave-2 scope. This is echoed in the L5 delta-groom triage.

---

## Side finding, offered for the architect's eye

`ADR-109:12`'s Related line glosses the report's matrix width as *"5 fleet repos"* attributed to
ADR-104 — but **ADR-104 ratified 9** and explicitly declined to rule which repos consolidate
(`ADR-104:15,97`). The 5 is a data artifact of `resolve_fleet_members` keying on
`deployed-versions.yaml`, not a ruled tree count. The phrasing invites misreading one as the other.
Not proposed as a row; flagged because it is the kind of gloss that hardens into doctrine if unread.

---

## Not examined (cut for time, stated rather than papered over)

ADR-107/105/108 full text (read only via ADR-109's quotations); intake #16/#22 full text; the three
`test_desired_state_*.py` files (codex w2/w3/w4 findings against them appear fixed per `git log`, not
re-verified line by line); the grok-shadow-ab, verification-ladder, and arc-educate audits; the six
non-repo-keyed `ecosystem/*.yaml` files (the registry-prep dossier already scopes these out);
`terminal-setup`'s actual on-disk/remote existence (outside this sandbox).

**Key paths:** `docs/decisions/ADR-104-fleet-repository-shape.md`,
`docs/decisions/ADR-109-fleet-desired-state-contract-v1.md`, `ecosystem/schema/desired_state.py`,
`scripts/desired_state_loader.py`, `scripts/desired_state_report.py`,
`tasks/462-terminal-setup-absent-from-every-machine-member.md`,
`tasks/383-execution-waves-per-surface.md`,
`docs/audits/2026-07-31-technical-382-registry-prep-dossier.md`,
`docs/handoffs/2026-08-01-dev-knowledge-architect/RESIDUAL.md`.
