# Wave-3 reading-friction census — hub · ai-council · corp-monorepo

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-13
- **Source:** operator-dictated walkthrough, verified read-only against all three live repositories
- **Snapshot:** `.dev-knowledge` `1c11f261` on `docs/wave3-census`; `ai-council` `52b0952` on `main`; `corp-monorepo` `e349d8b` on `main`; all three working trees clean
- **Status:** census only — no disposition was executed in any repository
- **Model:** Codex `gpt-5.6-sol`

## Executive result

Eighteen verified rows resolve to **6 BY-RULING · 6 OPEN · 6 NATURAL-LOCAL**.
The dictated legacy cases are stable: LESSONS and JOURNAL history remains untouched under
C1/C2; corp's UPPERCASE audit set is still exactly the 11 enumerated d1 grandfathered files;
corp CI remains declared-local under e3; and the uppercase-E3 `settings.local.json` tracking
defect is gone. The current reading-friction work is narrower:

1. unique `.claude/` ownership still awaits #328 declarations;
2. corp has an intake artifact but no `docs/intake/README.md`;
3. the carried ToC component still exists and ai-council still binds both ToC hooks, contrary
   to the operator's dictated post-#326 expectation of zero consumer bindings;
4. lint configuration still has two root forms;
5. the hub still lacks its ruled `.methodology.yaml`; and
6. `.gitattributes` expresses three materially different normalization baselines.

## Evidence protocol

Every row below was re-derived from live disk. Tracked presence and blob equality used
`git ls-files -s` / `git rev-parse HEAD:<path>`; runtime-only presence used `Test-Path` and
`Get-ChildItem -Force`; ignored state used `git check-ignore`; empty/non-empty used byte length
only; hook presence used the live YAML; headings used `rg -n`; the audit-name count used the
tracked `docs/audits/*.md` set. No `.env` or `settings.local.json` content was read or printed.

Negative path claims have no possible file line, so they are paired with the live command
witness and the governing positive source line. Reproducible probes:

```powershell
git -C <repo> ls-files -- <path>
git -C <repo> check-ignore -q <path>
Get-Item <repo>/.env | Select-Object Length
git -C corp-monorepo ls-files 'docs/audits/*.md'
rg -n 'id:\s*toc-(freshness|generate)' <repo>/.pre-commit-config.yaml
git -C <repo> ls-files -s
```

## Census rows

### W3-01 — LESSONS legacy entry formats — BY-RULING (C1 grandfather)

**Live:** all three files now advertise the six-field future heading. Ai still has the older
two-field `title` plus `CONTEXT/MISTAKE/RULE` body, explicitly labelled grandfathered
(`ai-council/LESSONS.md:4-7`, sample `:11-14`); hub entries use the six-field line
(`.dev-knowledge/LESSONS.md:4-6`, sample `:12`); corp retains its historical explanatory-body
variation. **Ruling:** C1 says template-sync future entries only and rewrite zero historical
entries (`.dev-knowledge/docs/audits/2026-07-13-technical-content-parity-inventory.md:167-175`);
the closure records the preamble rollout as DONE with existing entries preserved
(`.dev-knowledge/docs/audits/2026-07-13-technical-a0-traceability-closure.md:109`).
**Disposition:** no action; historical form differences are lawful append-only evidence.

### W3-02 — JOURNAL legacy entry formats — BY-RULING (C2 grandfather)

**Live:** the current hub and ai preambles specify `Did / Result / Changes / Abandoned / Next`
and newest-first order (`.dev-knowledge/JOURNAL.md:5-18`; `ai-council/JOURNAL.md:5-18`). Corp
uses the same semantics in bullet form and explicitly preserves pre-cutover `Did / Failed /
Next` entries (`corp-monorepo/JOURNAL.md:5-14`). Hub history also contains the older
`Did / Failed / Next` form (sample `.dev-knowledge/JOURNAL.md:7237-7248`). **Ruling:** C2 changed
the preamble, not history (`.dev-knowledge/docs/audits/2026-07-13-technical-content-parity-inventory.md:177-185`);
the closure marks that rollout DONE (`.dev-knowledge/docs/audits/2026-07-13-technical-a0-traceability-closure.md:110`).
**Disposition:** no action; do not normalize immutable history.

### W3-03 — commands roster form — NATURAL-LOCAL

**Live:** the hub hand-lists user commands, imports its generated repo roster, and imports a
second manifest-derived methodology roster (`.dev-knowledge/CLAUDE.md:111-121`, `:172-176`;
`.dev-knowledge/.claude/generated/commands-repo.md:1-13`). Both consumers keep the same
user/repo/plugin order inline (`ai-council/CLAUDE.md:113-126`; `corp-monorepo/CLAUDE.md:140-150`).
The common local `/override` file is one identical Git blob in all three; hub-only authoring
commands remain hub-local. **Disposition:** retain; generator form belongs to the source repo,
while consumer rosters truthfully enumerate their smaller installed surface.

### W3-04 — skills/rules roster form — NATURAL-LOCAL

**Live:** hub owns two repo skills plus `git-discipline` (`.dev-knowledge/CLAUDE.md:128-144`);
ai owns three repo rules and no repo skill (`ai-council/CLAUDE.md:128-141`); corp owns a local
gotchas skill (`corp-monorepo/CLAUDE.md:153-164`). The earlier taxonomy defect is closed: ai
now calls rules rules, and each roster names provenance
(`.dev-knowledge/docs/audits/2026-07-13-technical-a0-traceability-closure.md:107`).
**Disposition:** retain project-local organs; no cosmetic copying.

### W3-05 — hooks roster form, excluding the ToC row — NATURAL-LOCAL

**Live:** hub carries its large source/gate/session-hook roster (`.dev-knowledge/CLAUDE.md:146-176`);
ai lists its consumer gates plus floor/session hooks (`ai-council/CLAUDE.md:144-166`); corp lists
its application gates (`corp-monorepo/CLAUDE.md:166-179`). B5 roster currency is recorded DONE
(`.dev-knowledge/docs/audits/2026-07-13-technical-a0-traceability-closure.md:108`). The sets differ
because hub, small app, and monorepo enforce different local concerns. **Disposition:** retain
inline local rosters; the ToC exception is W3-13.

### W3-06 — CONTRIBUTING canonical-section order — BY-RULING

**Live:** template, ai, and corp all order the shared spine identically: Branch naming → Commit
style → Backlog-id → Pre-commit setup → Validators → ADR process → Handoff process → Definition
of done (`.dev-knowledge/templates/CONTRIBUTING-md-template.md:21-146`;
`ai-council/CONTRIBUTING.md:17-149`; `corp-monorepo/CONTRIBUTING.md:15-151`). Corp appends Tach
and Development Flow only after that spine (`corp-monorepo/CONTRIBUTING.md:163-225`).
**Ruling:** C3 fixed shell/order while retaining local appendices, and C3-C7 are recorded DONE
(`.dev-knowledge/docs/audits/2026-07-13-technical-content-parity-inventory.md:187-195`;
`.dev-knowledge/docs/audits/2026-07-13-technical-a0-traceability-closure.md:111-115`).
**Disposition:** no action; canonical order is at parity and corp's tail is lawful local content.

### W3-07 — unique `.claude/` subtrees and `settings.json` ownership — OPEN

**Live:** the child floor, sidecar, guard, and `/override` are exact ai/corp pairs; `/override`
also matches the hub. Unique surfaces remain role-shaped: hub owns agent/generated/skills/workflow
(`.dev-knowledge/.claude/agents/artifact-reader.md:1`;
`.dev-knowledge/.claude/generated/commands-repo.md:1-13`), ai owns three rules
(`ai-council/.claude/rules/code-standards.md:1`), and corp owns gotchas plus its workflow
(`corp-monorepo/.claude/skills/gotchas/SKILL.md:1`;
`corp-monorepo/.claude/workflows/conformance-corp.js:1`). Their `settings.json` blobs differ by
local hook block, as expected. What remains open is machine-readable ownership: CP-E1/E2 are
explicitly DEFERRED to #328 (`.dev-knowledge/docs/audits/2026-07-13-technical-a0-traceability-closure.md:119-120`).
**Proposed disposition:** declare subtree and hook-block ownership through #328; never copy local
organs for parity. **Blast radius:** `ecosystem/parity-surfaces.yaml` plus the three repos'
`.methodology.yaml` declarations (the hub file is itself missing; W3-15); zero `.claude/` payload files.

### W3-08 — `.claude/settings.local.json` tracking — BY-RULING (E3)

**Live:** hub and corp each have an ignored, untracked runtime file; ai has no runtime file and no
tracked file. All three ignore the path (`.dev-knowledge/.gitignore:16`;
`ai-council/.gitignore:29`; `corp-monorepo/.gitignore:31`). **Ruling:** uppercase-E3 required ai
to untrack the machine-local file; the execution is recorded DONE
(`.dev-knowledge/docs/audits/2026-07-13-technical-a0-traceability-closure.md:121`;
`ai-council/JOURNAL.md:38-42`). **Disposition:** no action; runtime presence may vary, tracking may not.

### W3-09 — `logs/` content differences — NATURAL-LOCAL

**Live snapshot:** hub 49 files (41 `PROPOSALS-*`, 7 other runtime outputs, 1 tracked
`TOKEN-LOG.md`); ai 13 files (12 proposals + `pcinstall.log`), none tracked; corp 15 files
(14 proposals + `OVERRIDES.md`), none tracked. Consumer logs are ignored wholesale
(`ai-council/.gitignore:45-49`; `corp-monorepo/.gitignore:58-62`); hub ignores its named runtime
outputs (`.dev-knowledge/.gitignore:24-57`). `TOKEN-LOG.md` is explicitly hub-only
(`.dev-knowledge/protocols/PLAYBOOK.md:922`, `:947`). **Disposition:** retain; these are local
execution traces, not a fleet content corpus.

### W3-10 — `docs/intake/README.md` presence — OPEN

**Live:** hub has the schema/index README (`.dev-knowledge/docs/intake/README.md:1-19`); ai has a
project-local intake index (`ai-council/docs/intake/README.md:1-21`); corp has one tracked intake
artifact (`corp-monorepo/docs/intake/2026-07-10-runbook-gap-notes.md:1-6`) but no README
(`git ls-files -- docs/intake/README.md` and `Test-Path` both negative). The universal workflow
points to `docs/intake/README.md` as the format/lifecycle source
(`.dev-knowledge/protocols/PLAYBOOK.md:2227`), while the settled manifest requires the intake
genre (`.dev-knowledge/docs/intake/2026-07-11-tech-ownership-manifest.md:22`).
**Proposed disposition:** seed a thin corp-local README describing the genre and current artifact;
do not copy the hub's generated index mechanism unless corp gains enough intake volume.
**Blast radius:** 1 file — `corp-monorepo/docs/intake/README.md`.

### W3-11 — corp UPPERCASE audit set — BY-RULING (d1 grandfather)

**Live:** exactly **11** tracked names match the pre-ruling UPPERCASE `_TYPE_` family, byte-for-byte
the enumeration in `corp-monorepo/.methodology.yaml:65-77`; the current count has **not grown**.
The prospective casing gate and boundary are declared at `corp-monorepo/.methodology.yaml:48-64`
and listed live in `corp-monorepo/CLAUDE.md:175`. **Ruling:** d1 selects lowercase for future
`docs/audits/` additions while grandfathering existing names
(`.dev-knowledge/docs/audits/2026-07-11-technical-fleet-parity-register.md:95-107`).
**Disposition:** no rename and no action; growth from 11 would be a regression.

### W3-12 — root `.env` metadata — NATURAL-LOCAL

**Live:** hub: absent, untracked, ignored; ai: present, **100 bytes (not byte-empty)**, untracked,
ignored; corp: absent, untracked, ignored. Ignore lines are `.dev-knowledge/.gitignore:13`,
`ai-council/.gitignore:26`, and `corp-monorepo/.gitignore:26`. The settled ownership manifest
names ai's gitignored CWD fallback as local (`.dev-knowledge/docs/intake/2026-07-11-tech-ownership-manifest.md:43-46`),
while ai's contract forbids repo-local keys (`ai-council/CLAUDE.md:79`, `:195`).
**Disposition:** retain metadata posture. Non-zero length is not evidence of a secret; content was
deliberately not inspected. Tracking any `.env` would be a defect.

### W3-13 — consumer ToC hook bindings after #326 — OPEN

**Live:** corp has zero ToC hook ids and documents the withdrawn binding
(`corp-monorepo/.methodology.yaml:35-46`). Ai still binds `toc-freshness` and `toc-generate` to
`protocols/COUNCIL_QUESTION_GUIDE.md` (`ai-council/.pre-commit-config.yaml:44-50`) and lists them
as active (`ai-council/CLAUDE.md:153`). The hub's generated deployable roster still carries
`toc-freshness` (`.dev-knowledge/.claude/methodology-roster.md:28-30`), sourced by the live
v1.3.1 manifest (`.dev-knowledge/deploy/manifest-v1.3.1.yaml:440-466`). The older ai execution
record treated protocol ToC as outside #326's ARCHITECTURE-only scope (`ai-council/JOURNAL.md:66-72`),
but the operator's 2026-07-13 walkthrough now dictates **no consumer ToC bindings**.
**Proposed disposition:** retire the carried `hub-toc-hooks` component in the next manifest,
remove ai's two bindings and §9 roster line, retire corp's waiver, regenerate the methodology
roster, and explicitly decide whether the Council-guide ToC remains unmanaged or is removed.
**Blast radius:** next manifest + generated roster; `ai-council/.pre-commit-config.yaml` and
`CLAUDE.md`; `corp-monorepo/.methodology.yaml`; optionally the Council guide (5 required files,
1 conditional). Existing release design already routes retirement through #245/#246
(`.dev-knowledge/BACKLOG.md:181`).

### W3-14 — root lint-configuration form — OPEN

**Live:** hub and corp place lint rules in `.ruff.toml`
(`.dev-knowledge/.ruff.toml:1-5`; `corp-monorepo/.ruff.toml:1-7`); hub's `pyproject.toml` carries
only the required-version floor (`.dev-knowledge/pyproject.toml:35-42`). Ai places its full rule
set in `pyproject.toml` (`ai-council/pyproject.toml:61-69`) and has no root `.ruff.toml`.
The settled manifest already calls the three-form state a convergence candidate
(`.dev-knowledge/docs/intake/2026-07-11-tech-ownership-manifest.md:43`).
**Proposed disposition:** standardize the *home*, not the rule sets, on `[tool.ruff]` in
`pyproject.toml` because that file exists in all three repos; retain project-local selections.
**Blast radius:** 4 files — hub and corp `pyproject.toml` plus removal of their two `.ruff.toml`
files. Ai is already in the proposed form.

### W3-15 — hub `.methodology.yaml` absence — OPEN

**Live:** both consumers track `.methodology.yaml`; the hub does not (`git ls-files --
.methodology.yaml` and `Test-Path` negative). This is not an implicit source-role exemption: the
settled §9a ruling says the hub **MUST** carry its own file
(`.dev-knowledge/docs/intake/2026-07-11-tech-ownership-manifest.md:29-32`). The closure audit
already records FPR-M as DEFERRED to #328
(`.dev-knowledge/docs/audits/2026-07-13-technical-a0-traceability-closure.md:90`), and the live
ticket includes the file in Done-when (`.dev-knowledge/BACKLOG.md:172`).
**Proposed disposition:** execute #328 as written; do not invent an empty symmetry file outside
the checker/manifest contract. **Blast radius:** hub `.methodology.yaml`, parity-surface manifest,
checker/audit wiring, and tests (at least 4 hub files; exact code split belongs to #328 design).

### W3-16 — `.gitattributes` normalization baseline — OPEN

**Live:** ai applies global LF plus CRLF PowerShell (`ai-council/.gitattributes:1-5`); corp applies
LF by selected extensions plus CRLF PowerShell (`corp-monorepo/.gitattributes:1-8`); hub pins only
three generated artifact classes and has no general text/PowerShell baseline
(`.dev-knowledge/.gitattributes:1-22`). This can make cross-repo copied Markdown or scripts acquire
different checkout bytes even when Git blobs agree.
**Proposed disposition:** adopt the ai two-line baseline (`* text=auto eol=lf`, `*.ps1 ... crlf`)
fleet-wide, retaining hub's generated-file comments/pins as additive documentation.
**Blast radius:** 3 `.gitattributes` files; content blobs need no rewrite unless
`git add --renormalize --dry-run` proves churn, in which case treat that churn as a separately
reviewed migration.

### W3-17 — corp `.github/` — BY-RULING (e3)

**Live:** corp alone tracks the two workflows named in its declaration; hub and ai have no
`.github/` path. The declaration identifies the surface as legitimate corp-only CI and cites e3
(`corp-monorepo/.methodology.yaml:79-87`). **Ruling:** lowercase-e3 is DECLARE-LOCAL
(`.dev-knowledge/docs/audits/2026-07-11-technical-fleet-parity-register.md:121`, `:129`), and the
closure confirms it DECLARED (`.dev-knowledge/docs/audits/2026-07-13-technical-a0-traceability-closure.md:82`).
**Disposition:** no action; do not copy CI to the hub or ai.

### W3-18 — remaining same-relative-name content diffs — NATURAL-LOCAL

**Live exhaustive intersection:** 21 tracked relative paths occur in all three repos. Five are
exact blobs: `.claude/commands/override.md`, `.vscode/settings.json`, and
`scripts/{canonical_freshness_gate,normalize_headers,session_end_backpressure}.py`. The child
pair additionally matches exactly on `INSTALL.md`, floor, sidecar, and floor guard. All remaining
differences are accounted for above or are project payload: `ARCHITECTURE`, `VISION`, `BACKLOG`,
`CLAUDE`, the ruled LESSONS/JOURNAL history, genre indexes, and project dependency/config content.
The genre indexes state their local scopes directly (`.dev-knowledge/protocols/README.md:5-11`;
`ai-council/protocols/README.md:1-12`; `corp-monorepo/protocols/README.md:1-12`), and decision
indexes enumerate independent ADR namespaces (`.dev-knowledge/docs/decisions/README.md:1-12`;
`ai-council/docs/decisions/README.md:1-10`; `corp-monorepo/docs/decisions/README.md:1-8`).
**Disposition:** retain local bodies. Shared shells/regions are the parity unit; whole-file blob
identity would erase application truth.

## Coverage closure

The same-relative-name diff produced no uncategorized surface:

- `.claude/settings.json`, `.gitignore`, `.pre-commit-config.yaml` → W3-05/W3-07/W3-08/W3-13.
- `.gitattributes` → W3-16.
- `ARCHITECTURE/BACKLOG/CLAUDE/VISION` and genre READMEs → W3-18.
- `CONTRIBUTING` → W3-06.
- `JOURNAL/LESSONS` → W3-01/W3-02.
- `pyproject.toml` / `.ruff.toml` → W3-14 (dependency payload remains W3-18 local).
- `scripts/validate_backlog.py` → the two consumers are exact floor twins; their deliberate
  E/S-agnostic form is documented at `ai-council/.pre-commit-config.yaml:34-37` and
  `corp-monorepo/CLAUDE.md:176`; no unruled drift.
- exact shared blobs and child carriers → W3-07/W3-18 positive parity evidence.

Zero row is inference-only; every classification above has both a live-disk witness and a
durable path+line authority.
