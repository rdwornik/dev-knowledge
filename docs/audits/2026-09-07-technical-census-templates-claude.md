# Census — `templates/` + `.claude/` (commands, hooks, rules, skills)

> **Consumer:** intake #73 — the shape-spec / tree-seal row, whose "dawn ruling" scenario is a
> per-tree list of out-of-pattern items with a proposed RELOCATE / RETIRE / WAIVE beside each.
> Substantive citation: `docs/intake/2026-09-05-tech-shape-spec-tree-seal-to-consumers.md`.
> Secondary: `[#526]` (root-hygiene census, same read-only genre, adjacent scope).
>
> **Lane** S-11 of the 2026-09-07 SWEEP. **READ-ONLY:** zero moves, zero deletes, zero edits
> outside this file. Every verdict below is a PROPOSAL the operator rules.
> **HEAD measured:** `5f27b20` (`origin/main` at lane start; `git merge origin/main` → already
> up to date).

---

## Method — what counts as a witness

A **witness** resolves the file: a manifest `source:` entry, a generator path constant, a
validator/test that opens it, a generated organ row, or a ruling that names it. Adopted
unchanged from the prior census of this same tree
(`docs/audits/2026-08-31-census-templates-consumers.md`, Class method block), so the two are
comparable rather than rival.

**Excluded, for the reason that census gives:** glob-scope sweepers that ingest `templates/`
wholesale (`silent_rule_detector.SCOPE_GLOBS`, `preflight_contract` ratchet scope,
`validate_hermetization` home allowlist, `funnel_coverage` baseline, `consumer_at_landing`
landing roots). Counting them makes dead stock empty by construction.

**This census is a DELTA, not a re-derivation.** `templates/` was censused 7 days ago at 47
files. It is 49 today. Re-deriving 47 settled verdicts would spend the night to reprint them.
What is new here: the 4-file delta, the whole of `.claude/` (never censused as a tree), and the
three lane questions.

---

## Inventory

### `templates/` — 49 tracked files

| # | Path | Witness | Verdict |
|---|---|---|---|
| 1 | `child-methodology-floor.md.tmpl` | `deploy/manifest-v1.5.0.yaml:825` `source:`; `scripts/generate_floor.py:53` `TEMPLATE_PATH` | KEEP |
| 2 | `child-methodology-floor.sha256` | `scripts/generate_floor.py:55` `HUB_CANONICAL_SHA`; `deploy/release_lint.py:95` `FLOOR_SIDECAR_REL`; `tests/test_deploy_floor.py` | KEEP · genre flag F9 |
| 3 | `intake-template.md` | `deploy/manifest-v1.5.0.yaml:521-522` `source:`+`path:`; `deploy/carrier_docs.py` | KEEP |
| 4 | `handoff/v5/HANDOFF_BOOT.md.tmpl` | `scripts/gen_handoff.py:1266` `_render` | KEEP |
| 5 | `handoff/v5/RESIDUAL.md.tmpl` | `scripts/gen_handoff.py:1267` | KEEP |
| 6 | `handoff/v5/PROBES.md.tmpl` | `scripts/gen_handoff.py:1268`; `scripts/verify_handoff_probes.py` | KEEP |
| 7 | `handoff/v5/SUPPLEMENT.md.tmpl` | `scripts/gen_handoff.py:1256` | KEEP |
| 8 | `handoff/epic/EPIC_BOOT.md.tmpl` | `scripts/gen_handoff.py:1228` (`_TMPL_DIR_EPIC`) | KEEP |
| 9 | `handoff/epic/EPIC_RETURN.md.tmpl` | `scripts/gen_handoff.py:1226` | KEEP |
| 10 | `handoff/epic/PROBES.md.tmpl` | `scripts/gen_handoff.py:1229` | KEEP |
| 11 | `handoff/functional/FUNCTIONAL_BOOT.md.tmpl` | `scripts/gen_handoff.py:1243-1244` | KEEP |
| 12–20 | `claude-regions/{antipatterns-universal, conventions-commit-branch, conventions-library-first, conventions-output-formatting, critical-rules-consistency, critical-rules-no-leftovers, critical-rules-records, first-read, session-start-protocol}.md` | `tests/test_boundary_headers.py:279-290` — byte-match + **`assert checked == 9`**; removing any one REDs the suite | KEEP (9) |
| 21 | `prompt-template.md` | `scripts/validate_reconciliation.py:121` `_SPEC_REGISTRY`; `scripts/dispatch_surface.py:44` `AGREEMENT_SITES` | KEEP |
| 22 | `CLAUDE-md-template.md` | `tests/test_canonical_docs.py` | KEEP |
| 23 | `CONTRIBUTING-md-template.md` | `tests/test_validate_reconciliation.py` (the placeholder-exemption case) | KEEP |
| 24–30 | `handoff/{01_ROLE, 02_METHODOLOGY, 03_PROJECT, 04_RECENT, 05_NOW, 06_QUESTIONS, 07_ASK_BACK}.md.tmpl` | `.claude/commands/handoff.md:73,215-216` — "Templates (retained live) … kept for cross-repo v4 per ADR-83"; `protocols/HANDOFF_PROCESS.md:570` | KEEP (7) |
| 31 | `handoff/README.md.tmpl` | same ADR-83 retention ruling, `.claude/commands/handoff.md:215` | KEEP |
| 32 | `handoff/v5/README.md.tmpl` | `protocols/HANDOFF_PROCESS.md:933` — "**No script reads** `templates/handoff/v5/README.md.tmpl` (it stays a deferred stub until #164 lands)"; `STANDING_RULINGS` T-35 | KEEP (deferred stub, retained by ruling) |
| 33 | `ADR-template.md` | `protocols/PLAYBOOK.md` (ADR-distillation prompt) | KEEP |
| 34 | `ARCHITECTURE-template.md` | `protocols/PLAYBOOK.md` (named remedy for a missing ARCHITECTURE.md) | KEEP |
| 35 | `audit-template.md` | `docs/decisions/ADR-101-hermetization.md` — ratified citation, "author-facing skeleton … carries the filename grammar" | KEEP |
| 36 | `codex-review-config-template.md` | `protocols/PLAYBOOK.md` | KEEP |
| 37 | `consumer-onboarding-runbook.md` | `protocols/PLAYBOOK.md` (Stage-4 worked example) | KEEP |
| 38 | `scrum-master-cover-letter.md` | `protocols/PLAYBOOK.md` | KEEP |
| 39 | `ruff-config-block.toml` | `ecosystem/parity-surfaces.yaml`; `deploy/release-v1.3.x-contract.md` | KEEP |
| 40 | `workspace-S.code-workspace` | `protocols/PLAYBOOK.md:1158` literal `cp` example | KEEP |
| 41 | `workspace-M.code-workspace` | `protocols/PLAYBOOK.md:1155` brace form `workspace-{S,M,L}` only | KEEP (weak witness) |
| 42 | `workspace-L.code-workspace` | `protocols/PLAYBOOK.md:1155` brace form only | KEEP (weak witness) |
| 43 | `README-md-template.md` | `deploy/manifest-v1.5.0.yaml:40-47` — named payload of the **deliberately undeclared** `readme-front-door` component, blocker recorded | KEEP (staged payload) |
| 44 | `archive/AGENTS-md-template.md` | in-file header `RETIRED 2026-05-19 — superseded by ADR-53` | KEEP · see F4 |
| 45 | `archive/HANDOFF_FOLDER_TEMPLATE.md` | in-file header `ARCHIVED 2026-06-26`; `protocols/archive/HANDOFF_PROCESS_v3.4.md` | KEEP |
| 46 | `archive/HANDOFF_QUESTION_TEMPLATE.md` | `tests/test_normalize_headers.py:431` — named real-world unterminated-fence case; **load-bearing fixture** | KEEP |
| 47 | `archive/HANDOFF_TEMPLATE.md` | `tests/test_scan_undeclared_edges.py:319` — named case proving `templates/archive/` is not an immutable prefix; **load-bearing fixture** | KEEP |
| 48 | `archive/JOURNAL-md-template.md` | in-file header `RETIRED 2026-08-31 … HY-3 Rule-D disposition` | KEEP (in retention home) |
| 49 | `archive/LESSONS-md-template.md` | in-file header `RETIRED 2026-08-31 … HY-3 Rule-D disposition` | KEEP (in retention home) |

### `.claude/` — 19 tracked files

| # | Path | Witness | Verdict |
|---|---|---|---|
| 50 | `commands/boot-session.md` | `ecosystem/organ-index.md:48` ARMED; `scripts/boot_frontier.py`; `deploy/manifest-v1.5.0.yaml` | KEEP |
| 51 | `commands/changelog-review.md` | `ecosystem/organ-index.md:49` ARMED; `scripts/changelog_sentinel.py` (surfaces it) | KEEP |
| 52 | `commands/handoff.md` | `ecosystem/organ-index.md:51` ARMED; `tests/test_handoff_modes.py` | KEEP |
| 53 | `commands/handoff-verify.md` | `ecosystem/organ-index.md:52` ARMED; `protocols/HANDOFF_PROCESS.md` §5 | KEEP |
| 54 | `commands/lane-boot.md` | `ecosystem/organ-index.md:53` ARMED; `scripts/dispatch_surface.py:44` `AGREEMENT_SITES`; `tests/test_dispatch_drift.py` | KEEP |
| 55 | `commands/lane-integrate.md` | `ecosystem/organ-index.md:54` ARMED; `protocols/PLAYBOOK.md:2113` | KEEP |
| 56 | `commands/override.md` | `ecosystem/organ-index.md:55` **RETIRED** status; still carried by `deploy/manifest-v1.5.0.yaml` | KEEP (status already RETIRED; file is the retirement notice) |
| 57 | `commands/preflight.md` | `ecosystem/organ-index.md:56` ARMED; `scripts/preflight_contract.py` is its engine | KEEP |
| 58 | `commands/save.md` | `ecosystem/organ-index.md:58` ARMED; `tests/test_canonical_docs.py` | KEEP |
| 59 | `generated/commands-repo.md` | emitted by `scripts/gen_claude_rosters.py:147`; gated by pre-commit `claude-rosters-freshness`; `@`-imported by `CLAUDE.md` §7 | KEEP (generated) |
| 60 | `generated/recent-adrs.md` | same generator + gate; `@`-imported by `CLAUDE.md` §11 | KEEP (generated) |
| 61 | `methodology-roster.md` | emitted by `scripts/gen_methodology_roster.py`; gated by pre-commit `roster-freshness` | KEEP (generated) |
| 62 | `rules/git-discipline.md` | `ecosystem/organ-index.md:87` rule row ARMED; `protocols/STANDING_RULINGS.md` | KEEP |
| 63 | `settings.json` | declares **7** hub session hooks, all 7 present as `ecosystem/organ-index.md` rows `:97,98,99,100,101,103,106`; `deploy/carrier_plugin.py`, `deploy/floor_conformance.py` | KEEP |
| 64 | `skills/verify/SKILL.md` | `ecosystem/organ-index.md:70` ARMED; `tests/test_canonical_docs.py` | KEEP |
| 65 | `skills/verify/verify.py` | `scripts/audit.py`; `tests/test_review_artifact_coverage.py` | KEEP |
| 66 | `skills/check-against-spec/SKILL.md` | `ecosystem/organ-index.md:68` ARMED; `scripts/validate_reconciliation.py:318-330` emits its invocation | KEEP |
| 67 | `agents/artifact-reader.md` | `ecosystem/provider-registry.yaml:292` — one of the nine gated provider/model seams | KEEP |
| 68 | `workflows/conformance-hub.js` | `ecosystem/provider-registry.yaml:295`; `ecosystem/organ-index.md:78`; the nightly Routine's canonical spec | KEEP |

**Home grammar:** all 68 paths sit in a home `ecosystem/fleet-shape-spec.yaml` `home_grammar.patterns`
already admits — `templates`, `templates/archive`, `templates/claude-regions`, `templates/handoff`,
`templates/handoff/*`, `.claude`, `.claude/*`, `.claude/skills/*`. **No file in either tree is
out-of-pattern.** No RELOCATE is available on home-grammar grounds.

---

## Proposals

### KEEP — 68 of 68

Every tracked file in both trees resolves to a witness. **Zero RELOCATE, zero ARCHIVE, zero
RETIRE proposed.** Stated plainly because the alternative is padding: this census found no dead
stock, and the two files a naive sweep would flag (`workspace-M/L`) are cited as a set at
`protocols/PLAYBOOK.md:1155`.

Three KEEPs carry a flag rather than a clean bill:

- **`templates/workspace-{M,L}.code-workspace`** — cited only through the brace form; no literal
  path citation, no code reader, no `cp` example (S has one at `:1158`). The prior census recorded
  an **operator-stated preference, still unruled**: *"jeden complex workspace template,
  scale-adaptive content, NOT scale-different templates"*
  (`docs/audits/2026-05-25-ai-council-universalization-audit-refresh.md`). A 3→1 consolidation is
  the operator's call; **"consolidate" is not in this lane's verdict grammar**, so the files stay
  KEEP and the question is surfaced rather than smuggled into a verdict.
- **`templates/child-methodology-floor.sha256`** — a 64-hex hash sidecar in a template directory
  (F9). Genre mismatch, already flagged 2026-08-31, still unruled.
- **`.claude/commands/override.md`** — `organ-index` already carries status RETIRED and ADR-85
  amendment §A2 retired its local-token path. The file survives as the retirement notice and is
  still manifest-carried to consumers. Whether a deployed no-op command should keep shipping is
  an operator question, not a census verdict.

### UNDETERMINED — 1 file

- **`templates/archive/AGENTS-md-template.md`** — its own header reads `RETIRED 2026-05-19 —
  superseded by ADR-53. Use templates/CLAUDE-md-template.md instead.` **ADR-115 (2026-08-25)
  superseded ADR-53 Decision 2** and re-admitted `AGENTS.md` as the portable instruction layer and
  a sanctioned Tier-1 root file (`ecosystem/fleet-shape-spec.yaml`, `root_allowlist.files`, per-member
  provenance for `AGENTS.md`). The retirement therefore rests on a rule that no longer holds, and
  every consumer repo that gains an `AGENTS.md` now has no template for it. **I could not establish**
  whether the archived template's content is still fit for the ADR-115 shape — that is a content
  judgment, and this lane is read-only. Verdict withheld deliberately: it is neither a clean KEEP
  nor a defensible revival without a reading the operator or architect owns.

---

## The three lane questions

### Q1 — Templates with no generator consuming them

**23 of 49 have a machine consumer** (a generator, manifest carrier, validator or test that opens
the path): rows 1–23 above — 3 carrier · 8 `gen_handoff.py`-rendered · 9 byte-match-gated region
extracts · 1 registered spec · 2 test-resolved.

**26 of 49 have no generator at all.** They fall into four kinds, and only the first is a finding:

| Kind | n | Files | Status |
|---|---|---|---|
| Explicitly ruled unrendered | 1 | `handoff/v5/README.md.tmpl` | `HANDOFF_PROCESS.md:933`: "No script reads" it — deferred until #164. **By design.** |
| Ruled-live, agent-driven (ADR-83 v4 retention) | 8 | `handoff/01_ROLE…07_ASK_BACK` + `handoff/README.md.tmpl` | Copy material an agent drives, not a render target. `gen_handoff._TMPL_DIR` is `templates/handoff/v5`, not the flat parent. **By ruling.** |
| Reference-only (a live doc or ADR cites it; a human copies it) | 10 | `ADR-template`, `ARCHITECTURE-template`, `audit-template`, `codex-review-config-template`, `consumer-onboarding-runbook`, `scrum-master-cover-letter`, `ruff-config-block.toml`, `workspace-{S,M,L}` | Human-copy templates. A generator is not the right instrument for them. |
| Archived + staged | 7 | `archive/*` (6) + `README-md-template.md` | Retention home / recorded blocker. |

**The honest headline: "no generator" is not a defect class in this tree.** 25 of the 26 have a
recorded reason for having none. The 26th is `README-md-template.md`, whose absent consumer is
itself recorded, with a measured blocker (`release_lint` C7 asserts exact dict equality between
manifest `doc_shapes` spines and the live `audit._CANONICAL_SPINE`, so adding `README.md` to one
side alone REDs shipped specs — the re-point needs a manifest version bump).

**Delta vs the 2026-08-31 census (47 → 49):**

| Change | Evidence |
|---|---|
| `+ claude-regions/conventions-library-first.md` | the byte-match cardinality assert moved `checked == 8` → `checked == 9` (`tests/test_boundary_headers.py:290`) |
| `+ README-md-template.md` | landed `eaaeafa2`, 96 lines, per `deploy/manifest-v1.5.0.yaml:40-47` |
| `JOURNAL-md-template.md` root → `archive/` | HY-3 executed; in-file header `RETIRED 2026-08-31` |
| `LESSONS-md-template.md` root → `archive/` | same |

The prior census's **Class D (dead stock) is now empty** — both members were dispositioned to the
retention home, not deleted, exactly as HY-3's Rule D prescribed.

### Q2 — Commands not in PLAYBOOK's dispatch/command tables

PLAYBOOK carries **two** command surfaces. Neither is the dispatch table at `:2870` — that one
routes *substrates* (`Dispatch-Local`/`-Cloud`/`-Codespace`), names no slash command, and is out
of scope for this question.

- **T1** — `### Usage protocol: which command / hook, when` (`:4035`), Commands table, 7 rows.
- **T2** — `### 7b. Slash commands`, "Real examples in Rob's ecosystem" (`:4138`, bullets `:4139-4146`), 8 entries.

| repo command | in T1 | in T2 | mentions anywhere in PLAYBOOK |
|---|---|---|---|
| `/save` | yes | yes | 5 |
| `/handoff` | yes | yes | 23 |
| `/changelog-review` | yes | no | 2 |
| `/override` | **no** | yes | 1 |
| `/lane-boot` | **no** | **no** | 8 (Ch8 prose) |
| `/lane-integrate` | **no** | **no** | 3 (Ch8 prose) |
| `/preflight` | **no** | **no** | 2 (Ch8 prose) |
| `/boot-session` | **no** | **no** | **0** |
| `/handoff-verify` | **no** | **no** | **0** |

**Answer: 5 of 9 repo commands are in neither table** — `/boot-session`, `/handoff-verify`,
`/lane-boot`, `/lane-integrate`, `/preflight`. Two of those five (`/boot-session`,
`/handoff-verify`) do not appear anywhere in PLAYBOOK at all. A sixth, `/override`, is in T2 only.
**Skills:** T1's skills table lists `gotchas` and `verify`; **`check-against-spec` is absent**,
though it is ARMED at `ecosystem/organ-index.md:68` and named in `CLAUDE.md` §8.

**Framing that changes the severity, and it must be stated:** PLAYBOOK declares its own table
non-authoritative in the paragraph above it — *"When it drifts from `ls ~/.claude/commands
~/.claude/skills`, **the filesystem wins**"* — and closes the section with *"CLAUDE.md is the
inventory authority — §7 (commands), §8 (skills), §9 (hooks); this is the operational 'when'."*
`CLAUDE.md` §7 in turn `@`-imports the **generated** `.claude/generated/commands-repo.md`, which
enumerates all 9 from frontmatter and is drift-gated by pre-commit `claude-rosters-freshness`
(verified fresh: `gen_claude_rosters.py --check` exit 0).

So the machine roster is complete and gated; PLAYBOOK's is a hand-maintained cheat-sheet whose
drift is *sanctioned by construction*. That does not make it harmless — **it is 56% incomplete on
repo commands, and it has re-drifted before** (its own text records two prior instances: a
self-stamped "6 hooks" against a live 10, and rows describing the retired `/boot`+`/evolve`
machinery). **Proposal, operator's to rule:** replace T1's Commands table and T2's bullet list with
a pointer to the generated fragment, the same subtraction PLAYBOOK already applied to its Hooks
row. Not executed here.

**Also measured (F6):** T1's `/handoff` row (`:4050`) and T2's `/handoff` bullet (`:4142`) both
read "HANDOFF_PROCESS v5 (ADR-82)". The live spec is **7.0.0** — `python3 scripts/validate_reconciliation.py
--all` → `13 edge(s), 0 mismatch(es)`, every `handoff-process` edge at `declared 7.0.0 / current
7.0.0`. PLAYBOOK's own header (`:24`) already flags one such site (Ch14); these are two more.

### Q3 — Hooks not armed by `arm_hooks.py`

**`arm_hooks.py` arms exactly two things**, and its docstring says so: (1) the pre-commit-managed
git hooks, and (2) `merge.ours.driver` for the `[#590]` `.gitattributes` `merge=ours` pin. Its
roster is one tuple — `scripts/arm_hooks.py:36`, `HOOK_TYPES = ("pre-commit", "commit-msg",
"pre-push")` — passed verbatim to `pre_commit install` at `:154-155`.

**Within its remit — no gap.** `.pre-commit-config.yaml:8` declares
`default_install_hook_types: [pre-commit, commit-msg, pre-push]`, an exact match. All **23**
declared git hooks (= `organ-index` "git-hook 23") sit in one of those three stages: 19 `pre-commit`,
2 `commit-msg` (`backlog-id-on-close`, `backlog-filing-backpressure`), 2 `pre-push`
(`block-ff-push`, `block-unanchored-push`). **Zero configured-but-unarmable git hooks.**

**Outside its remit — 7 hub hooks, structurally.** Every hook declared in `.claude/settings.json`
is a Claude Code *lifecycle* hook, armed by the client reading that file. No script arms them, and
`arm_hooks.py` cannot: it is itself one of them.

| trigger | hook | armable by `arm_hooks.py`? |
|---|---|---|
| `Stop` | `session_end_backpressure.py` | no — client-armed |
| `PreToolUse` | `hooks/block_immutable_edits.py` (ADR-77 guard) | no — client-armed |
| `SessionStart` | `fleet_health.py` | no — client-armed |
| `SessionStart` | `surface_triage.ps1` | no — client-armed **and PowerShell (F8)** |
| `SessionStart` | `billing_leak_sentinel.ps1` | no — client-armed **and PowerShell (F8)** |
| `SessionStart` | `changelog_sentinel.py` | no — client-armed |
| `SessionStart` | `arm_hooks.py` | no — it is the armer |

Plus 1 plugin hook (`Stop: propose_closures`, from `plugins/tier1-lifecycle/hooks/hooks.json`) and
4 L0 hooks under `~/.claude/` — neither in this repo's `.claude/` and neither `arm_hooks.py`'s.
Total reconciles to `organ-index`'s "session-hook 12".

**And the finding that matters more than the taxonomy (F1):** in *this* container, **nothing is
armed at all**. `.git/hooks/` holds only `.sample` files; `git config core.hooksPath` is unset.
`arm_hooks.py` never ran, because the `SessionStart` command is `uv run --locked python …` and this
container's `uv` is **0.8.17** against the repo's `required-version = "==0.11.19"` — `uv` refuses
with `Required uv version ==0.11.19 does not match the running version 0.8.17`. This is precisely
the configured-but-unarmed window RF-2 exists to close, reproduced by a toolchain mismatch the
script's fail-soft posture is structurally unable to detect: it fails *before* `arm_hooks.py`'s
first line. **Reported, not repaired.**

---

## Other findings — reported, not repaired

- **F2 · stale citation in a deploy-carried file.** `deploy/manifest-v1.5.0.yaml:466-467` (and
  `v1.4.0:405-407`) reads *"as ARCHITECTURE / CLAUDE-md / CONTRIBUTING-md / JOURNAL-md / LESSONS-md
  already have one each"*. `JOURNAL-md-template.md` and `LESSONS-md-template.md` were RETIRED to
  `templates/archive/` on **2026-08-31** under HY-3. The comment names two archived files as live
  siblings, in the governance file that ships to consumers.
- **F3 · stale evidence in a generated index, and a census that cited it.**
  `ecosystem/index.yaml:78` still records `reconciled_versions` WARN:
  `templates/CONTRIBUTING-md-template.md: malformed`. `[#335]` landed the fix on 2026-08-28
  (`validate_reconciliation.is_template_placeholder`); a live run today returns `13 edge(s), 0
  mismatch(es)`. `ecosystem/index.yaml:1` reads `generated: '2026-08-05T10:36:01'` — 33 days stale.
  The 2026-08-31 census cited that line as current evidence for its C-EDGE class; that citation
  does not hold at HEAD.
- **F4 · a retirement header pointing at a superseded rule.** `templates/archive/AGENTS-md-template.md:1`
  cites ADR-53. ADR-115 superseded ADR-53 Decision 2 on 2026-08-25. See UNDETERMINED above.
- **F7 · a non-finding, recorded so it is not filed as one.** `.claude/CLAUDE-FLOOR.md` is absent at
  the hub, and `.claude/settings.json` carries no `check_floor_hash` invocation, while
  `.claude/methodology-roster.md` names both. This is **correct**: the roster's own header states it
  is the *manifest-declared deployable corpus*, "NOT a filesystem inventory of this repo", and the
  floor is a consumer-only carrier component (`deploy/manifest-v1.5.0.yaml:278-283`). Verified
  consistent.
- **F8 · cross-substrate gap.** Two of the seven hub `SessionStart` hooks are PowerShell scripts.
  On a Linux substrate — this container, a codespace, a cloud lane — they are inert. Not a defect
  in this tree; a fact about where the surfacing layer actually fires.
- **F9 · genre.** `templates/child-methodology-floor.sha256` is a 64-hex sidecar in a template
  directory. Flagged 2026-08-31, unruled since.

---

## Counts before → proposed after

```
templates/    49  ->  49    (KEEP 48, UNDETERMINED 1)
.claude/      19  ->  19    (KEEP 19)
TOTAL         68  ->  68

by verdict:   KEEP 67 · RELOCATE 0 · ARCHIVE 0 · RETIRE 0 · UNDETERMINED 1
moves proposed: 0        deletes proposed: 0        edits made: 0
files written by this lane: 1 (this file)
```

Shape at HEAD — `templates/`: 17 root · 9 `claude-regions/` · 8 `handoff/` flat · 3 `handoff/epic/`
· 1 `handoff/functional/` · 5 `handoff/v5/` · 6 `archive/` = 49.
`.claude/`: 9 `commands/` · 3 `skills/` · 2 `generated/` · 1 `rules/` · 1 `agents/` ·
1 `workflows/` · `settings.json` · `methodology-roster.md` = 19.

---

## Honest limits

**What I could not establish, in order of how much it costs the reader:**

1. **I never read the authority.** `to-cc\BATCH-2026-09-07-SWEEP-CONTRACTS.md` (FROZEN, 5422 B) is
   on the operator's Drive transport, off-tree and unreachable from this container — `to-cc/` does
   not exist in the clone and no file matching `*SWEEP-CONTRACTS*` is tracked. The brief says *"Read
   that file yourself; the rules below are a working copy and if they disagree with it, it wins."*
   **I worked entirely from the working copy.** If the frozen contract diverges, this census was
   built against the wrong rules and does not know it.
2. **No gate ran, and none can run here.** `uv` in this container is **0.8.17**; `pyproject.toml`
   pins `required-version = "==0.11.19"`. Every `uv run --locked …` invocation — the suite,
   `audit.py health`, every pre-commit hook — refuses before executing. Git hooks are additionally
   unarmed (`.git/hooks/` = samples only), so **`consumer_at_landing`, `audit-title-gate`,
   `validate-hermetization`, `block-ff-push` and `journal_spine_anchor` will not fire on my commit.**
   I satisfied `consumer_at_landing` by construction (an id-shaped `intake #73` on the consumer
   line), not by observing it pass. **Do not read this lane as gate-proven.**
   What I *did* run, on the system `python3` 3.11.15, stdlib-only, read-only:
   `scripts/validate_reconciliation.py --all` → exit 0, `13 edge(s), 0 mismatch(es)`;
   `scripts/gen_claude_rosters.py --check` → exit 0; `scripts/generate_organ_index.py --check` →
   exit 0. `validate_hermetization.py` produced **no output on any invocation including `--help`** —
   I could not determine whether it passed, and I do not claim it did.
3. **The "last content commit" witness class is mostly unavailable.** This clone's history is
   grafted: `428656f` is a **root commit** (`git rev-list --parents -n 1` returns it alone) touching
   **2934 files, 628336 insertions**, dated 2026-09-05. 61 of the 68 files in scope report that
   commit as their last content change. The date therefore separates only "touched since the graft"
   (7 files) from "not touched" (61) — it carries no age signal. This independently reproduces the
   2026-08-31 census's own finding that an age-keyed retention rule is unimplementable in this
   corpus. **Every verdict above rests on a consumer or generator witness, never on a date.**
4. **`.claude/` scope call, made by me.** The brief scopes the folder as
   `.claude/ (commands, hooks, rules, skills)`. There is **no `.claude/hooks/` directory** — hook
   implementations live in `scripts/` and `scripts/hooks/`, and `.claude/` holds only the
   *declaration* (`settings.json`). I inventoried all 19 tracked files under `.claude/`, which adds
   `agents/`, `workflows/`, `generated/` and `methodology-roster.md` beyond the parenthetical. If a
   peer lane owns those four, its verdicts supersede mine on rows 59–61, 67 and 68.
5. **Whether the archived `AGENTS-md-template.md` should be revived** — a content judgment under
   ADR-115, not a census verdict. Left UNDETERMINED rather than guessed.
6. **Whether `templates/handoff/01_ROLE…07_ASK_BACK` are still *needed*** — the ADR-83 retention
   ruling is a solid witness for the *decision*, and that is what I verdicted on. Whether any
   consumer repo is still on the v4 lineage is fleet state outside this repo, and I did not measure it.
7. **Fan-out: NONE.** `gemini` is **not on PATH** in this container (`which gemini` → not found).
   **Gemini-read files: 0. Fabricated locators: 0 — because zero locators were machine-supplied.**
   That zero is an artifact of the CLI's absence, not a clean bill: every locator here was opened by
   me directly, so the fabrication-detection this lane was meant to exercise did not run at all.
   **Copilot Enterprise offload was NOT used and was NOT available** — it is gated on intake #75
   (`docs/intake/2026-09-06-tech-copilot-offload-role-and-account-map.md`), unratified at HEAD.
   Recorded here so nobody later claims it was used.
8. **I did not verify the reference-only citations line by line.** For the 10 reference-only
   templates I confirmed each path resolves in `protocols/PLAYBOOK.md` or a live ADR by grep, and
   opened the workspace and `audit-template` sites. I did not re-open all 10 PLAYBOOK anchors; the
   2026-08-31 census did, and I carried its line numbers forward as prior work rather than
   re-deriving them. **Those specific line numbers are inherited, not re-witnessed by me.**
