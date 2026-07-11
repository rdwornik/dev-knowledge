# Fleet-parity register — hub · ai-council · corp-monorepo
- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-11
- **Source-session:** operator-dictated READ-ONLY fleet-parity sweep (recurring consolidation list → one canonical register); HEAD `e746fe1` on `main`, cut on branch `docs/fleet-parity-register`
- **Status:** PROPOSAL-ONLY — verdicts are proposals for operator verb-ruling; no file was moved, renamed, or deleted in any of the three repos

> **Scope.** Read-only across three repos: hub `.dev-knowledge`, `ai-council`, `corp-monorepo`. One row per divergence. Verdict vocabulary (proposal only): **FIX-NOW** (align now, cheap/ruled) · **DECLARE-LOCAL** (record as sanctioned in that repo's `.methodology.yaml`) · **TICKET** (file to BACKLOG, needs an arc) · **AT-PARITY** (no divergence / already correct-by-design). Owner = the repo that carries the change.
>
> **Evidence basis.** Three parallel read-only evidence-gatherers (one per repo) + operator-verified spot checks (runbox/temp premise, gitignore parity). Every row cites live-verified state.

---

## 0. Register — master table (one row per divergence)

The register proper. Each row is verb-rule-ready; §1–§7 below carry the per-row evidence and rationale, grouped by the operator's dictated items (a)–(g).

| # | Surface | hub | ai-council | corp-monorepo | Verdict (proposal) | Owner |
|---|---|---|---|---|---|---|
| a1 | ARCHITECTURE.md Mermaid | ABSENT (stripped #326) | ABSENT (converted #262) | **PRESENT — 2 flowchart blocks** | FIX-NOW *or* DECLARE-LOCAL | corp |
| a2 | ARCHITECTURE.md ToC | PRESENT (gen, gated) | **ABSENT** | PRESENT (gen, gated) | TICKET *or* DECLARE-LOCAL | ai-council |
| b1 | BACKLOG epic-id scheme | E1–E7 epic ids | theme-prose + `[S-n]` | flat `[#N]` + theme-prose | DECLARE-LOCAL + TICKET (P6) | consumers |
| b2 | BACKLOG story-map schema gate | `validate_backlog.py` + `validate-backlog` hook | ABSENT | ABSENT | TICKET (P6, bundle w/ b1) | hub→consumers |
| c1 | `/save` command | PRESENT (repo) | ABSENT | ABSENT | DECLARE-LOCAL *or* TICKET | hub |
| c2 | review-command duplication | `/code-review` (built-in skill) + `/codex-review` (user cmd) | same pair (fleet-global) | same pair (fleet-global) | DECLARE-LOCAL (keep both, ruled) | hub (fleet policy) |
| c3 | `/evolve` command | ABSENT (archived 2026-06-05) | ABSENT | ABSENT | AT-PARITY (archived-correct) | — |
| d1 | audit filename casing | lowercase kebab `<date>-<class>-<slug>` (ADR-101) | lowercase kebab (legacy UPPER quarantined) | **UPPERCASE `_AUDIT_`/`_BRIEF_`** (ADR-14, actively growing) | FIX-NOW (ADR-101 R4 already ruled lowercase wins) | corp |
| e1 | `.vscode/` | **TRACKED** (`settings.json`, no ignore line) | absent (would-ignore) | absent (would-ignore) | FIX-NOW *or* DECLARE-LOCAL | hub |
| e2 | `.hypothesis/` gitignore | no ignore line | no ignore line | ignored (`.gitignore:37`) | FIX-NOW (add line, hub+ai-council) | hub + ai-council |
| e3 | `.github/` | absent | absent | **TRACKED** (2 CI workflows) | DECLARE-LOCAL (corp-only CI) | corp |
| e4 | `assets/` | absent | **TRACKED** (`ruff-pre-commit.yaml`) | absent | DECLARE-LOCAL | ai-council |
| e5 | `node_modules/` | PRESENT (ignored) | absent | absent | AT-PARITY (hub-only tooling, ignored) | hub |
| e6 | caches (`.pytest_cache`/`.ruff_cache`/`.mypy_cache`) | all ignored | all ignored | all ignored | AT-PARITY | — |
| f1 | hub `temp/` | empty · untracked · unsanctioned by ADR-101 §1 | — | — | DELETE-CANDIDATE (local rm) | hub |
| f2 | hub `runbox/` | **ABSENT** — premise unmatched | — | — | NO-ACTION (premise void) | hub |
| g1 | CLAUDE.md handoff-process version | v5 (ADR-82) | v5 | **v4 (stale)** — §6/§11 | FIX-NOW (reconcile v4→v5) | corp |
| g2 | CLAUDE.md `/boot` in §6 | archived but literal step-1 | no `/boot` | no `/boot` | TICKET-low (de-emphasize) | hub |
| M | `.methodology.yaml` presence | **ABSENT** | present (1 divergence) | present (2 divergences) | design-input (see §9) | hub |

**Legend for "verdict … *or* …":** two viable dispositions; the operator's verb-ruling picks one. Where I lean, §1–§7 say so.

---

## 1. (a) ARCHITECTURE.md — ToC + Mermaid presence (#326 execution map)

**a1 — Mermaid.** The #326 ruling stripped Mermaid from the hub's **CC-facing** canonical `ARCHITECTURE.md` (ADR-51 amendment 2026-07-05; persistent diagrams live on the separate human-facing viz surface, ADR-59).

- **hub:** ABSENT — `grep '```mermaid'` → none. Codemap is generated compact text (`## Codemap [CORE]`, tool-managed).
- **ai-council:** ABSENT — already converted to hand-authored compact-text under its own **#262** (`d5c4e25`, 2026-07-08). At parity with hub, by a different arc.
- **corp-monorepo:** **PRESENT — 2 `flowchart TD` blocks** (lines 72, 275, both `%%{init: … darkMode …}%%`). Plus a hub-format ToC. corp still carries exactly what #326 removed.

**Verdict a1 — FIX-NOW (align corp to #326) *or* DECLARE-LOCAL.** ADR-101/#326 doctrine treats canonical `ARCHITECTURE.md` as CC-facing → strip Mermaid, park diagrams on the ADR-59 human-facing surface. Lean **FIX-NOW** (corp converts the 2 flowcharts to compact-text or moves them to a human-facing viz doc), since the #326 execution map explicitly names the consumer carry-over as the target. **DECLARE-LOCAL** is legitimate only if corp deliberately keeps its ARCHITECTURE.md human-facing — in which case it must be recorded in corp's `.methodology.yaml` (it is **not** today; only `ruff-gate` + `hub-codemap-hooks` are). Owner: **corp**.

**a2 — ToC.** hub + corp carry a generated, `toc-freshness`-gated ToC. **ai-council lacks one** (no `<!-- TOC -->` markers, no anchor list) despite consuming the `toc-freshness` hook. **Verdict a2 — TICKET *or* DECLARE-LOCAL:** cheap to add a generated ToC to ai-council's ARCHITECTURE.md for parity; or declare ai-council's flat single-package doc intentionally ToC-free. Owner: **ai-council**.

---

## 2. (b) BACKLOG schema parity — E-prefix / S-n story-map

| | hub | ai-council | corp-monorepo |
|---|---|---|---|
| Epic ids | **E1–E7** (`## [E1] …`) | theme prose (no `E`-id) | theme prose (no `E`-id) |
| Story ids | `[S-n]` | `[S-n]` | none (flat) |
| Task ids | `[#NNN]` | `[#id]` | `[#N]` |
| Schema gate | `validate_backlog.py` + `validate-backlog` (ADR-66) | ABSENT | ABSENT |

**b1 — epic scheme.** Only the hub carries the E-prefix backbone (E1–E7, added on the BACKLOG theme backbone). ai-council uses theme-prose + `[S-n]`; corp uses theme-prose + flat `[#N]` (no story layer). **This is the operator's dictated choice point:** propagate E-prefix/S-n to consumers, **or** rule consumer backlogs exempt. **Verdict b1 — DECLARE-LOCAL (interim) + TICKET (P6).** ADR-99 already says *"Track-X now, ADR-66 story-map fleet-wide at P6"* — so fleet-wide story-map is the standing plan; until P6, record each consumer's lighter scheme as sanctioned in its `.methodology.yaml`. Owner: **consumers** (rollout: hub deploy at P6).

**b2 — schema gate.** The `validate_backlog.py` story-map validator + `validate-backlog` pre-commit hook are **HUB-ONLY** (neither consumer has the script or the hook). This is coupled to b1: a consumer can't pass a story-map schema gate until it adopts the story-map schema. Note the known hazard (memory: *new-validate-backlog-rule-hits-twin-and-child-conformance*) — a hub `validate_backlog` hard-fail rule flips un-migrated child backlogs to needs-migration, so the gate must ship **with** the schema, not before. **Verdict b2 — TICKET (P6), bundled with b1.** Owner: **hub → consumers**.

---

## 3. (c) Command roster diff

Repo-level `.claude/commands/*.md` actually present:

| command | hub | ai-council | corp | note |
|---|---|---|---|---|
| `/override` | ✅ | ✅ | ✅ | at parity |
| `/save` | ✅ | ✗ | ✗ | hub-only |
| `/handoff` | ✅ | ✗ | ✗ | correct — handoffs generated in hub only (ADR-36) |
| `/changelog-review` | ✅ | ✗ | ✗ | hub-local (tool-changelog review) |
| `/ship`, `/review-closures` | via plugin | via plugin | via plugin | `tier1-lifecycle` plugin, at parity |
| `/codex-review` | user-level | user-level | user-level | `~/.claude/commands/`, fleet-global |
| `/code-review` | built-in skill | built-in skill | built-in skill | Claude Code built-in, not a repo file |
| `/session-summary` | user-level | user-level | user-level | at parity |
| `/evolve` | ✗ archived | ✗ | ✗ | archived 2026-06-05 |

**c1 — `/save`.** Present only at the hub (repo-level `save.md`). Consumers commit via plugin `/ship` + manual commits. **Verdict — DECLARE-LOCAL *or* TICKET:** either declare `/save` a hub-local convenience, or deploy it fleet-wide (it is a thin Conventional-Commits helper — low-risk to distribute). Lean **DECLARE-LOCAL** (hub authoring convenience; consumers already have `/ship`). Owner: **hub**.

**c2 — `code-review` vs `codex-review` duplication (operator-named).** There is **no** repo-level `code-review` command in any repo — `/code-review` is the **Claude Code built-in skill**; `/codex-review` is a **custom user-level command** invoking the Codex reviewer. So the "duplication" is two *review pathways* that coexist fleet-wide (Claude-native review vs Codex review), not a duplicated repo file. They target **different reviewers** and serve distinct purposes (corp `AGENTS.md`/ADR-54 wires Codex globally). **Verdict — DECLARE-LOCAL (keep both, ruled):** record the deliberate two-reviewer policy so the coexistence reads as intentional, not redundant. If the operator wants one, TICKET a consolidation. Owner: **hub (fleet policy)**.

**c3 — `/evolve` absence (operator-named).** `/evolve` was archived at the hub 2026-06-05 (Phase-C3). Its absence in consumers is therefore **correct parity**, not a gap. **Verdict — AT-PARITY.** No action; a flat "consumers lack /evolve" would manufacture a false gap.

---

## 4. (d) Audit filename convention clash — one fleet convention must win

| repo | governing rule | current convention | actively growing? |
|---|---|---|---|
| hub | **ADR-101 R3/R4** | lowercase kebab `<date>-<class>-<slug>.md`, CLOSED 11-class enum, `_`/UPPER forbidden | yes (gated by `validate-hermetization`) |
| ai-council | ADR-34 lineage | lowercase kebab `YYYY-MM-DD-<topic>.md`; legacy `_UPPER_` **quarantined** in `docs/audits/archive/legacy/` | yes (lowercase) |
| corp-monorepo | **corp ADR-14** | **UPPERCASE `_TYPE_`** date-first `{YYYY-MM-DD}_{TYPE}_{slug}.md` (`_AUDIT_`, `_BRIEF_`, `_EVIDENCE_`, `_HANDOFF_`) | **yes — UPPERCASE, ungated** |

Representative corp names (verbatim): `2026-07-11_AUDIT_root-parity-disposition.md`, `2026-07-08_BRIEF_metadata-charter-T1.md`, `2026-07-07_EVIDENCE_by-product-docs-tree-analysis.md`. corp ADR-14 (*"New format `{YYYY-MM}_{TYPE}_{CLIENT}_{Description}.{ext}`"*) formally governs **MyWork content files** (RFP/DECK/CERT — a controlled vocab in `config/naming_config.yaml`); the `_AUDIT_`/`_BRIEF_` **doc-artifact** names re-apply that same UPPERCASE `_TYPE_` grammar to docs.

**The clash is direct and the direction is already ruled.** Hub **ADR-101 R4** states verbatim: *"This is the rule that fixes the cross-repo divergence the census found (corp-monorepo's UPPERCASE `_AUDIT_`/`_BRIEF_` family, actively growing for lack of a gate)."* So the fleet convention that wins is **hub ADR-101 lowercase**, and ADR-101 already named corp as the target.

**Verdict d1 — FIX-NOW (corp adopts ADR-101 lowercase for `docs/audits/`), prospective-only + grandfather existing** (mirroring how ADR-101 itself grandfathers the hub's own legacy corpus — no retroactive rename). **Boundary to preserve:** corp ADR-14 continues to govern **MyWork content files** (a different domain, controlled TYPE vocab); only the `docs/audits/` **doc-artifact** naming migrates to ADR-101 lowercase. ai-council is already at parity (lowercase; legacy quarantined). Owner: **corp**. *Sub-question for the operator: does corp also want ADR-101's `validate-hermetization` gate deployed to stop the UPPERCASE growth at source? (currently HUB-ONLY, n=1).*

---

## 5. (e) Root dot-folder / file matrix — gitignore-parity verdict each

| item | hub | ai-council | corp | gitignore-parity verdict |
|---|---|---|---|---|
| `.pytest_cache/` | present · ignored | present · ignored | present · ignored | **AT-PARITY** |
| `.ruff_cache/` | present · ignored | present · ignored | present · ignored | **AT-PARITY** |
| `.mypy_cache/` | absent · ignore-line ✅ | present · ignored | absent · ignore-line ✅ | **AT-PARITY** |
| `.hypothesis/` | absent · **no line** | absent · **no line** | present · ignored (`:37`) | **FIX-NOW** — add `.hypothesis/` to hub + ai-council `.gitignore` (cheap; prevents a future accidental commit if hypothesis testing lands) |
| `.venv/` | absent · ignore-line ✅ | present · ignored | present · ignored | **AT-PARITY** |
| `.vscode/` | **present · TRACKED** (`settings.json`) | absent · ignore-line ✅ | absent · ignore-line ✅ | **FIX-NOW *or* DECLARE-LOCAL** (e1 below) |
| `.github/` | absent | absent | **present · TRACKED** (2 workflows) | **DECLARE-LOCAL** (e3) |
| `assets/` | absent | **present · TRACKED** (`ruff-pre-commit.yaml`) | absent | **DECLARE-LOCAL** (e4) |
| `node_modules/` | present · ignored | absent | absent | **AT-PARITY** (hub-only Node toc/codemap tooling, correctly ignored) |

**e1 — `.vscode/` asymmetry.** The hub **tracks** `.vscode/settings.json` (no gitignore line); both consumers gitignore `.vscode/`. The hub is the outlier. **Verdict — FIX-NOW (add `.vscode/` to hub `.gitignore` for parity) *or* DECLARE-LOCAL (hub deliberately shares an editor config).** Operator ruling needed — tracking a shared workspace settings file is a legitimate choice, but it is currently *undeclared*. Owner: **hub**.

**e2 — `.hypothesis/`.** Only corp ignores it. Adding the one line to hub + ai-council `.gitignore` is a cheap parity fix with a real payoff (prevents committing a Hypothesis example DB if property tests ever run there). **Verdict — FIX-NOW.** Owner: **hub + ai-council**.

**e3 — `.github/`.** corp is the only repo with CI (2 tracked workflows: `nightly-conformance-triage.yml`, `tach.yml`). Legit corp-only surface. **Verdict — DECLARE-LOCAL** in corp's `.methodology.yaml` (currently undeclared). Owner: **corp**.

**e4 — `assets/`.** ai-council tracks a single pinned `assets/ruff-pre-commit.yaml`. **Verdict — DECLARE-LOCAL.** Owner: **ai-council**.

---

## 6. (f) hub `runbox/` and `temp/` — origin + disposition

**Operator-flagged premise vs live state — reported faithfully:**

**f1 — `temp/`.** PRESENT on disk, **EMPTY**, **UNTRACKED**, mtime 2026-07-08 00:15. `git ls-files temp` → empty; `git log --all -- temp` → empty (git does not track empty dirs, so there is **no creating commit** and no README to keep). Origin: a **local scratch directory**, no git trace. It is **not** in ADR-101 §1's sanctioned Tier-1 top-level set (`.claude .claude-plugin .vscode codex config deploy docs ecosystem logs plugins protocols scripts templates tests`) — an unsanctioned empty local dir that the ADR-101 gate never saw (the gate is prospective on staged **ADDs**; nothing was ever added). **Verdict — DELETE-CANDIDATE:** a purely local `rmdir temp` (no git operation, nothing to commit). Operator rules; per core-invariant #3 I did **not** remove it. Owner: **hub**.

**f2 — `runbox/`.** **ABSENT.** No `runbox/` directory anywhere on disk (root or nested), and **no git history** (`git log --all -- runbox` → empty). The prompt's premise — *"hub runbox/ (single file)"* — **does not match current hub state.** Likeliest explanations: already removed, or it existed transiently in a worktree/other machine, or a misremembered name. **Verdict — NO-ACTION (premise void):** there is nothing on disk or in history to keep-with-README or delete. Flagged, not fabricated. Owner: **hub** (operator to confirm whether a `runbox/` was expected).

---

## 7. (g) CLAUDE.md stale references — session-start & archived artifacts

**g1 — corp handoff-process version (STALE).** corp `CLAUDE.md` §6 (line 104) and §11 (line 174) cite the handoff process as **"v4 canonical; supersedes ADR-42 v3"** / *".dev-knowledge ADR-62: v4 handoff process"*. The hub is on **HANDOFF_PROCESS v5 (ADR-82)**. Stale at the major level. (Not an *archived-artifact* pointer, but a stale cross-repo version ref — corp doesn't generate handoffs itself per ADR-36, so it's vestigial, but still wrong.) **Verdict — FIX-NOW:** reconcile corp CLAUDE.md handoff refs v4 → v5/ADR-82. Owner: **corp**.

**g2 — hub `/boot` heads §6.** hub §6 step-1 is `/boot`, correctly annotated *"(archived 2026-06-05 Phase-C3, archive path …)"* — so it is **marked, not silent** — but an archived command still literally heads the "Session start protocol" numbered list, so a reader following §6 top-down hits an archived instruction first. **Verdict — TICKET-low:** reorder or demote `/boot` below the live steps. Owner: **hub**.

**No true stale *archived-artifact* live-pointers found in any of the three CLAUDE.md files** — every reference to `/boot`, `/evolve`, root `README.md`, `CHANGELOG`, `AGENTS.md`, and the archived `verify` skill carries an explicit archived/deleted/retired marker. ai-council's CLAUDE.md is fully clean (no `/boot` at all). The only genuine staleness is corp's handoff-version (g1).

---

## 8. Cross-cutting meta-finding (M) — `.methodology.yaml` presence

- **hub `.dev-knowledge`: ABSENT** (`git ls-files .methodology.yaml` → empty).
- **ai-council: present** — 1 declared divergence: `hub-codemap-hooks` (hand-authored codemap; codemap-freshness hook not consumed).
- **corp-monorepo: present** — 2 declared divergences: `ruff-gate` (own ruff gate, pre-methodology) + `hub-codemap-hooks`.

The `.methodology.yaml` files are already *"read by the hub Informant (`scripts/enforcement_coverage.py`, [#244] P4 / D2)."* Several divergences this register surfaces are **legitimate-but-undeclared** — they belong in `.methodology.yaml` today: corp's ToC+Mermaid (a1, if kept), corp's `.github/` CI (e3), ai-council's `assets/` (e4). The hub having **no** `.methodology.yaml` is the design input for §9: the proposed check must treat the hub as the **baseline** (it declares nothing *from itself*), and hub-only surfaces (node_modules, `.vscode` tracking, `/save`) are baseline-defining, not divergences — unless the operator wants the hub to carry its own `.methodology.yaml` for symmetry.

---

## 9. PROPOSED (design only — not built) — a fleet-parity audit CHECK

**Goal (operator-stated):** every register row is either **at parity** or **declared** in a repo's `.methodology.yaml`; anything undeclared = **WARN** in the ecosystem audit — so this list can never silently regress.

**Design — `fleet_parity` check (WARN-only surfacing, not a gate):**

1. **Baseline = hub.** The hub `.dev-knowledge` defines the reference state for each parity surface. Consumers are compared against it. Hub-only surfaces (tooling the hub alone carries) are baseline-defining, not divergences.
2. **Machine-readable surface manifest.** Add a small `ecosystem/parity-surfaces.yaml` (hub-owned) enumerating the checkable surfaces with a probe each:
   - `arch_mermaid` (grep ` ```mermaid ` in `ARCHITECTURE.md` == 0)
   - `arch_toc` (TOC markers present)
   - `backlog_epic_scheme` (E-prefix present) / `backlog_schema_gate` (`validate_backlog.py` present)
   - `audit_name_casing` (no `docs/audits/*_[A-Z]` UPPERCASE `_TYPE_` on ADDs)
   - `gitignore_line:<pattern>` (e.g. `.hypothesis/`, `.vscode/`) for each parity-critical ignore
   - `command_present:<name>` for the roster (`/save`, `/override`, …)
   - `tracked_dir:<path>` for `.github/`, `assets/`, `.vscode/`
3. **Per consumer, per surface:** compute `state`. If `state == baseline` → **PASS**. Else look up the surface key in that consumer's `.methodology.yaml` `sanctioned_divergences[].component`. If **declared** (and `review_date` not past) → **PASS (declared)**. If **undeclared** → **WARN** (`{repo}: {surface} diverges from hub baseline and is not declared in .methodology.yaml`).
4. **Home:** extend the existing hub Informant `scripts/enforcement_coverage.py` (already the declared reader of `.methodology.yaml`) — reuse its loader, add a `fleet_parity` finding class. Surface it in the **nightly ecosystem audit** (`audit.py` / the conformance-nightly-digest), **WARN severity only** — informs, never blocks (matches the operator's "= WARN" and the fleet's fail-open surfacing posture).
5. **Anti-regress property:** a new undeclared divergence (e.g. corp grows another `_AUDIT_` file, or ai-council drops its ToC further) flips its surface to WARN on the next nightly, forcing either a FIX or an explicit `.methodology.yaml` declaration — the register can't silently rot.
6. **Two open design choices for the operator:**
   - **(i)** Does the **hub** get its own `.methodology.yaml` (for symmetry / to declare hub-only surfaces like `.vscode` tracking), or stay baseline-only?
   - **(ii)** Is `review_date` **enforced** (an expired declaration re-WARNs, forcing periodic re-justification), or advisory? Recommend **enforced** — it gives declarations a shelf-life so "sanctioned" doesn't become "forgotten".
7. **Follow-up filing (capture-precedes-construction, ADR-70):** this is a **design proposal only** — no code, no manifest, no hook built here. Building `fleet_parity` + `ecosystem/parity-surfaces.yaml` is a named BACKLOG task for the operator to file (HUB-ONLY first, consumer carrier at P6, mirroring `roster-freshness`).

---

## 10. Summary — what the operator is verb-ruling

**Ruled-direction-already-exists (lean FIX-NOW):** d1 (corp → ADR-101 lowercase, ADR-101 R4 already named it) · e2 (`.hypothesis/` gitignore, cheap) · g1 (corp handoff v4→v5).

**Needs a genuine choice:** a1 (corp Mermaid: strip vs declare) · b1/b2 (consumer story-map: P6 rollout vs permanent exempt) · c1 (`/save`: deploy vs hub-local) · c2 (two review commands: keep-both-ruled vs consolidate) · e1 (`.vscode`: hub ignore vs declare-shared).

**Declare-and-move-on:** e3 (corp `.github/`) · e4 (ai-council `assets/`) — legitimate, just record them.

**At-parity / no-action (surfaced so the list is exhaustive, not to action):** a2-optional · c3 (`/evolve` archived-correct) · e5/e6 (caches) · f2 (`runbox/` premise void).

**Local cleanup:** f1 (`temp/` empty untracked — delete-candidate, operator confirms).

**Design to approve then file:** §9 `fleet_parity` WARN check.

*Read-only sweep: no file in any of the three repos was moved, renamed, or deleted. This register is committed on `docs/fleet-parity-register`, no merge.*

## Amendment — 2026-07-11 (post-authoring execution record)

> In-file amendment marker (CLAUDE.md §5 item 3 — the rows above are an immutable audit; an executed verdict is recorded here, never by editing a row in place).
>
> **f1 `temp/` — DELETE-CANDIDATE → EXECUTED (DONE).** Operator-approved deletion during the 2026-07-11 session-closure arc (the operator's paste was the approval; core-invariant #3 satisfied). `temp/` was re-verified **EMPTY and UNTRACKED** (`find temp -mindepth 1` → 0 entries; `git ls-files temp` → empty; `git log --all -- temp` → empty) and then removed via a local `rmdir temp` — no git operation, because git never tracked the empty dir. The row-32 / §6-f1 DELETE-CANDIDATE verdict is now resolved; anchored in the same closure arc's JOURNAL day-addendum.
