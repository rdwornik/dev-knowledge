# LANE V2 — register verification, domain V2 (backlog machinery)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-24 · **Slug:** verify-register-v2
- **Lane:** V2, READ-ONLY cloud lane. **This lane rules nothing** — every verdict below is
  evidence for the architect's batch ruling over the register.
- **Inputs:** `docs/audits/2026-08-24-technical-research-candidate-register.md` (rows) +
  `docs/audits/2026-08-24-technical-research-register-addendum.md` (**governs on conflict**).
  Both present in the clone; no substitutes used.
- **Rows owned:** every register row with `domain: V2` — **C08–C15**, eight rows, all verdicted.
- **Lane-specific addendum duty:** the addendum assigns none to V2 by name (the command/skill
  census is V1's, C26/C27 are V4's, C36 is V5's). The addendum clause that *does* bind this lane
  is the global one at `…addendum.md:118-120` — a `measured-here` tag returns its measurement
  locator or is downgraded. Four of these eight rows carry that tag; §3 discharges each.
- **Addendum row correction applied:** C14 only (`…addendum.md:33-40`).
- **Write scope honoured:** one artifact, this file. Nothing else in the tree was modified — no
  `tasks/`, no `BACKLOG.md`, no `protocols/`, no `docs/decisions/`, no JOURNAL entry (P-1).

## 1. Environment declared

`uv` on the container image measured **0.8.17**; `pyproject.toml:25` pins
`required-version = "==0.11.19"` — mismatch, so the gate mesh was inert as shipped. Installed the
pin per the brief (`python3 -m pip install --target ./uvpin "uv==0.11.19"`) and ran everything
under **`./uvpin/bin/uv run --locked …`** (uv 0.11.19, Python 3.11.15). The install directory
`./uvpin/` is untracked scratch and is not committed. This is the C18 failure class the register
itself names, observed again here.

Live measurement taken under that environment, used below:
`./uvpin/bin/uv run --locked python scripts/validate_backlog.py` → **`OK (9 themes, 26 stories,
212 tasks, 1 warning(s))`** — the register's `ledger_constraint: {open: 212}` **verifies exactly**
against the ruled denominator (`[#555]` R2: validate_backlog on main).

## 2. Verdicts

| row | verdict | locator | note (one line) |
|---|---|---|---|
| C08 | **PARTIAL** | `tasks/README.md:75` · `scripts/gen_task_tree.py:1113` | Aggregate half already landed (`BACKLOG.md:2` GENERATED, `generated_sha256` pinned `gen_task_tree.py:357,623,745`, gated `audit.py:2462`); **missing: "SOLE"** — `tasks/manifest.json` is *"the other half of the source"*, hand-edited for membership/ordering, so the two-agents-one-row conflict surface the claim targets survives untouched. |
| C09 | **PARTIAL** | `docs/decisions/ADR-107-backlog-restructure-engine-schema-viewer.md:305` | max+1 is HAVE and **normative** (*"`next_free = max(id parsed from tasks/<id>-<slug>.md) + 1`"*); ULID/content-hash + `[#NNN]`-as-display-alias **ABSENT** — no allocation code exists at all, ADR-107:249 records *"allocation rule not built"* and :463 leaves the concurrent-allocation hole open by name. |
| C10 | **PARTIAL** | `scripts/gen_task_tree.py:1312` · `scripts/export_backlog_view.py:1` | Ingredients exist and the row's carrier note is accurate; **missing: the digest itself** — no committed artifact carries a ledger line, next-5, flow vitals or since-last-window diff. `--rank` is an uncommitted read-only report, the view layer is deliberately disposable/gitignored, `fleet_health.py:591` gauges P-band counts only, and the operator-facing surface is still the 485-line generated `BACKLOG.md`. |
| C11 | **PARTIAL** | `tasks/555-closing-campaign-batch-1-kill-candidates-instrum.md:4` | Carrier verified as the register asks: `[#555]` is `status: open`, and its throughput denominator is **ruled** (R2, in-row → `docs/audits/2026-08-22-technical-annotation-and-rulings-ledger.md` §2). **Missing: the instrument** — grep across `scripts/` returns zero for average-age-of-open-rows, aging outliers and throughput-per-window; nothing computes any of the three. |
| C12 | **ABSENT** | checked `scripts/` · `tasks/` + `BACKLOG.md` · `protocols/` + `docs/decisions/` | Zero hits for `icebox`/`bankruptcy` in all four places; no cap, no one-in-one-out, no exemption grammar. Live set measured **212 open** (§1), so the row's premise stands unrefuted — it is simply unbuilt. Disposition is `OPERATOR`; this lane rules nothing. |
| C13 | **PARTIAL** | `scripts/gen_task_tree.py:1210` · `:1193` | A ranking mechanism exists but on a **different axis** — `[P1..P3]` primary, `serialize-group` contention secondary — and the module states its own honest limit at :1193: *"this ranks THROUGHPUT, not value"*. Dependency-aware readiness **ABSENT**: `depends-on` is carried raw (ADR-107:448) and `dependencies` is only *rendered outward* (`export_backlog_view.py:193,363`); nothing computes what-is-unblocked-now. Carrier note verified — `--rank` is `[#566]`, merged, row closed. |
| C14 | **PARTIAL** | `scripts/silent_rule_detector.py:51` · `:112` · `:142` | Per the **addendum** (governs): **R12 landed** — `protocols/STANDING_RULINGS.md` left the detector scope at v4→v5, in code and test. **R13 has no in-repo locator but the addendum itself** (`…addendum.md:36-38`); `STANDING_RULINGS.md` carries no R12/R13 entry. C14's own delta — counting **active imperative rule IDs**, authorizing ruling per change — is **ABSENT**: the pinned contract counts *normative-keyword occurrences* and says so (`:16-21`). |
| C15 | **PARTIAL** | `docs/audits/2026-08-21-technical-lane-rat-intake-ratification.md:278` | The practice is real and already contract-borne (lane-rat §6 emits carrier-row specs *"for the SEAT — `tasks/` is not this lane's to touch"*; L6 records the same self-denial at `docs/audits/2026-08-24-verification-l6-rulings-landing.md:9-10`). **Missing: the codification** — zero hits for a propose-don't-write clause in `protocols/PLAYBOOK.md`, `protocols/STANDING_RULINGS.md` or `.claude/commands/`; no row-spec format; and `lane-contract-check` asserts only that the `What NOT to do` **heading exists** (`scripts/gen_lane_contract.py:138` + `:580-582`), never its content. |

## 3. `measured-here` discharge (addendum `…addendum.md:118-120`)

Four of the eight rows carry the tag. Three resolve to a findable measurement; one does not.

| row | tag | measurement artifact | outcome |
|---|---|---|---|
| C09 | `measured-here` | `JOURNAL.md:1719-1721` — *"The next-free-id history scan returns **777** … Real next id was 577"*; corroborated `tasks/574-batch-manifest-emitted-by-gen-lane-contract.md:13` and ADR-107:463 | **Locator returned** — the double bite is recorded, contemporaneous, and names both real ids. |
| C10 | `practitioner+measured-here` | none — the operator quote *"looks the same, huge, huge, huge"* resolves **only to the register's own comment line** (`…candidate-register.md:129`); no in-repo measurement artifact exists | **DOWNGRADE-TO-PRACTITIONER** for the `measured-here` half. The `practitioner` half stands on its own and the row's substance is unaffected. |
| C14 | `measured-here` | `docs/audits/2026-08-24-technical-probe-substrate.md:344-371` — the 441→445 ownership proof (*"This lane's own content therefore contributes **zero** to the pool"*), plus commit `c559392`'s message | **Locator returned** — the foreign-growth charge is proven in the artifact, not asserted. |
| C15 | `measured-here` | `docs/audits/2026-08-21-technical-lane-rat-intake-ratification.md:278` (§6 *"Carrier-row specs (for the SEAT …)"*) | **Locator returned** — the de-facto claim is exactly what §6 did. |

## 4. Two things found while verifying, recorded for the architect — not ruled, not acted on

1. **An `R13` id collision.** The addendum's R13 (*"does the rule have a normative home
   elsewhere"*) shares its label with a **different** live R13 — *"Give ADR-112's Tier-S ledger a
   home"* (`docs/audits/2026-08-17-census-nb7-orphan-census.md:410`), and with an unrelated R13 in
   the 2026-08-19 N3 pack. Adopting C14 "scoped to the delta" cites an ambiguous label. Flagged
   only; disambiguation is a ruling.
2. **Out of my domain, handed to V1.** `.claude/commands/lane-boot.md:132` instructs a lane to
   *"Write the lane's JOURNAL entry on this branch, ahead of any merge"* — which contradicts
   `protocols/STANDING_RULINGS.md:1783` **P-1** (*"A lane leaves `JOURNAL.md` alone"*). The
   addendum makes procedure-vs-ruling conflicts in `.claude/` V1's census duty
   (`…addendum.md:93-97`), so it is reported here and not verdicted.

## 5. Scope statement

Eight rows owned, eight verdicted, one verdict each. Six PARTIAL, one ABSENT, zero HAVE, zero
CONFLICTS. No row was left unverified and nothing outside domain V2 was verdicted. The recurring
shape across these eight — worth the architect's attention because it repeats six times — is that
the **mechanism half is built and the doctrine half is not**: a ranking without a readiness axis,
a detector without an active-rule-ID metric, a source-of-truth flip with a second write surface
still open, a lane practice with no clause and no check. None of that is a ruling; it is what the
locators show.
