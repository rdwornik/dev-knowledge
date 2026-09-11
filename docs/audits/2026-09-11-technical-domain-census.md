# Domain census — one page per top-level folder

> **Class:** technical · **Date:** 2026-09-11 · **Lane:** `lane-x-000-domain-census`, dispatched
> `sonnet`/high per its frozen contract.
> **Base SHA censused:** `e4929b09` (local `main` tip at dispatch — `main` is moving under this
> lane; W-4 is pending and will drop the organ count from 65 to 64 on merge. This is a **dated
> snapshot against a named base**, not a live view — do not read it as current after `main` moves.)
> **Authority:** AX6-1, `to-cc/AMEND-BATCH-X-ROSTER-006.md` (2026-09-11). The `owner`/`lifecycle`
> column addendum is `to-browser/RESEARCH-2026-09-11-folder-as-domain.md` §3 item 1.
> **Consumer:** stated input to **AX6-4's operator packet D14** (folder-as-domain, decided AFTER
> this census with its per-folder verdicts as the input) and to **AX6-2's management map**.
> no-consumer: neither D14 nor the AX6-2 management map resolves to a `[#id]`, `ADR-<n>`,
> `STANDING_RULINGS` section, or `intake #<n>` on this lane's base SHA — both are operator-side
> packets tracked outside this repo's governance pool, so this line satisfies `consumer_at_landing`
> explicitly rather than leaving the citation implicit in the prose above.
> **Posture:** read-only aggregation. This lane repairs nothing it finds; `GARBAGE-CANDIDATE` is a
> proposal awaiting the operator's GO (AX6-1), not an action.

## Method — read before the pages

**Sources, exactly as the contract names them, read and not re-derived:**

1. `ecosystem/organ-index.md` — the generated organ inventory (65 organs, 8 classes).
2. `uv run --locked python scripts/graph_queries.py process-list --render` — FPG-1's process
   list (159 processes: 146 script + 11 command + 2 skill; 119 triggered, 40 not).
3. `docs/audits/2026-09-08-technical-process-trigger-census.md` — the 2026-09-08 trigger census
   (216 rows across four overlapping populations; its orphan reasoning and `[owner: ...]` hints
   are carried into this census's Owner column rather than re-derived).
4. `scripts/file_purpose_graph.py` — FPG-1 itself. Read as a live query tool (`why <path>`),
   which is reading the persisted graph, not recomputing wiring by hand; used sparingly, for
   named items the other three sources leave silent (e.g. `protocols/PLAYBOOK.md`, `JOURNAL.md`).
5. `git log` — for `last touched` (computed per-file from `git log --name-only`, filtered against
   a live `git ls-files` so a deleted-but-historically-touched file cannot leak in — three such
   ghosts, `scripts/{backlog_extract,migrate_links,validate_scope_tags}.py`, were caught and
   excluded this way).

**One additional source consulted and disclosed here, since it is not on the contract's list but
resolves 29 otherwise-unattributable items:** `.pre-commit-config.yaml` itself. `organ-index.md`'s
`Source` column for every git-hook organ is the wiring declaration (`.pre-commit-config.yaml`)
rather than the implementing script, and that file lives at the repo ROOT — under none of the
twelve census folders. Reading its `entry:` lines directly (not re-deriving wiring, just reading
where organ-index.md's own generator reads) resolves every git-hook organ to its real implementing
script, which is how this census attributes all 29 git-hooks to `scripts/`. Recorded per Q10
disclosure rather than treated as silent scope creep.

**Item universe and folder attribution, decided in-contract (not a fork) and reported:**
An item's folder is the top-level path segment of its own implementing file — organ-index's
`Source`, cross-resolved through `.pre-commit-config.yaml`'s `entry:` for git-hooks and through
FPG-1's own script path for session-hooks, falling back to the organ-index literal `Source` only
where no implementation file resolves. For the three folders that host process code
(`scripts/`, `.claude/`, `plugins/`) this yields one row per implementing file. For folders that
are content/registry trees rather than process homes (`docs/`, `tasks/`, `tests/`, `templates/`,
`logs/`, `ecosystem/`'s per-child history streams) the sources name **zero** process rows — walking
every file in `docs/` (2,099 tracked files) or `tasks/` (447) to manufacture items would be
exactly the re-derivation the contract forbids, so those pages itemize at the **sub-domain /
named-registry / generated-artifact** grain instead, with the zero-process finding stated plainly
rather than papered over. This is disclosed once here rather than repeated on every such page.

**Lifecycle, adapted once and applied consistently:** the contract's rule (`production` =
triggered AND read) is calibrated for organs. Applied literally it would make every
hand-maintained reference doc — `PLAYBOOK.md`, `STANDING_RULINGS.md`, `README.md` files —
non-`production`, since a doc's own reading is never a "trigger" in the wiring sense. For a
non-organ item this census reads "triggered" as "actively consulted/maintained" (evidenced by
recent git history, explicit citation in a named source, or a gate that fires when it changes)
rather than requiring an automated wiring edge. Where this substitution is load-bearing for a
specific row it is stated beside that row.

**Owner resolution, applied uniformly:** hook-triggered → the pre-commit/session-hook gate run
(chained through intermediate scripts to the root trigger); operator-invoked → the operator,
naming the act where it is one of the census's seven closed acts (GO · ratification · tag ·
destructive acts · seat release · deploy · sitting), otherwise "operator, ad-hoc"; no trigger →
`NONE`, carrying the source census's own reasoning where given.

**Root files are out of scope by AX6-1's own premise** (folders, not files) but two are pulled in
by explicit contract direction or unavoidable relevance: `JOURNAL.md` (contract: "PLAYBOOK and
JOURNAL ahead of everything else" on the `protocols/` page, even though JOURNAL.md's file lives at
repo root) and `BACKLOG.md` (mentioned in prose on the `tasks/` page as the generated view of that
folder's source-of-truth, not itemized as its own row since its file is not under `tasks/`).

**Budget deviation, disclosed per Q10, including one failure along the way:** the contract's
"natural split" is one subagent per folder page. This census reconciled all five sources into one
reference table before drafting (the folder-attribution join above), then attempted exactly one
subagent fork for the `scripts/` page (144 items, 58% of the repo total) to write it up from that
table. **That fork did not produce the page** — it inherited this session's full conversation
context, including this lane's own narration of "waiting on the fork," and its final message
echoed that narration back rather than doing the assigned write-up; it consumed real budget
(~310k tokens, 41 tool calls) and returned nothing usable. Rather than retry the same failure
mode, the `scripts/` page was built directly instead: a small deterministic script parsed the
already-reconciled FPG-1 process-list text and the `.pre-commit-config.yaml` hook→script map (both
already read in full earlier in this session) into the table below, resolving trigger chains
programmatically rather than by hand. Two rows the script's naive one-hop chain-walk left `UNKNOWN`
(`gen_task_tree.py`, `validate_doc_rot.py`, both chained through an untriggered intermediate) were
corrected against a direct `file_purpose_graph.py why` query, which showed each also has a second,
triggered import path the process-list's single-parent rendering did not surface. The remaining
eleven pages were drafted directly throughout, never forked — each was small enough (2-33 items)
once the join was done that re-parallelizing would have cost more cross-page owner/lifecycle
consistency than it saved. None of this changes any per-item verdict or the contract's own
decisions — reported per the decision budget ("everything else is decided per contract defaults
and reported"), and the fork's failure is recorded here rather than smoothed into "one subagent was
used" as the Method originally stated before this correction.

---

## protocols/

17 items: 16 tracked files under `protocols/` plus `JOURNAL.md` (repo root — included here per
the contract's explicit ordering directive; this is JOURNAL's only appearance in the census).
PLAYBOOK and JOURNAL first, per the contract.

| Item | Trigger | Reader | Last touched | Owner | Lifecycle | Verdict |
|---|---|---|---|---|---|---|
| `protocols/PLAYBOOK.md` | gate | organ + seat | 2026-09-10 | the `toc-freshness-playbook` + `provider-registry-agreement` pre-commit gates (fire on edits); read at every session's on-demand consult per `CLAUDE.md` §1 | production (FPG-1 `why` shows 57 consumers: many `declares rule:*` [doc-code-edge] edges plus 9+ `is implemented by task:N` edges) | LIVE |
| `JOURNAL.md` | NOTHING | organ + seat | 2026-09-11 | **NONE, per FPG-1's own graph** — `file_purpose_graph.py why JOURNAL.md` REFUSES: *"nothing explains this file... no governed input names it. A file nothing explains is a defect, not a mystery."* Informally, `journal_anchor.py`/`block-unanchored-push` read its spine-anchor content on every push, and `CLAUDE.md` §1/§6 mandates reading its last 5 entries every session — **neither is a governed FPG-1 edge.** | production (last-touched TODAY; heavy convention-driven use) | LIVE — **flagship disagreement**: the repo's own boot contract treats JOURNAL.md as load-bearing while its own persisted process graph formally cannot explain it. Recorded per the contract's "record the disagreement, do not reconcile it." |
| `protocols/HANDOFF_PROCESS.md` | gate | organ + seat | 2026-09-10 | the `coherence-nudge` pre-commit gate (non-blocking, fires on edits); read at seat release via `/handoff` | production (`CLAUDE.md` frontmatter: `reconciled_with: handoff-process@7.1.0`) | LIVE |
| `protocols/HANDOFF_BOOT.md` | NOTHING | seat | 2026-09-10 | NONE (read per `CLAUDE.md` §1 boot sequence, no gate found) | production | LIVE |
| `protocols/AI_COUNCIL_PROCESS.md` | gate | organ | 2026-09-04 | the `provider-registry-agreement` pre-commit gate | production | LIVE |
| `protocols/STANDING_RULINGS.md` | NOTHING | seat | 2026-09-09 | NONE | production (heavily cited by this very contract's own decision-budget section) | LIVE |
| `protocols/SESSION_SETUP.md` | NOTHING | seat | 2026-09-10 | NONE | production (`CLAUDE.md` footer names it a verify-after-updates target) | LIVE |
| `protocols/ENVIRONMENT.md` | NOTHING | seat | 2026-09-06 | NONE | production (`CLAUDE.md` footer names it a verify-after-updates target) | LIVE |
| `protocols/README.md` | NOTHING | seat | 2026-09-10 | NONE | production | LIVE |
| `protocols/REPO_ONBOARDING.md` | NOTHING | seat | 2026-09-06 | NONE | production | LIVE |
| `protocols/OPERATOR-INTERFACE.md` | NOTHING | seat | 2026-09-10 | NONE | production | LIVE |
| `protocols/FUNNEL_LIFECYCLE.md` | NOTHING | seat | 2026-09-06 | NONE | production | LIVE |
| `protocols/AGENT_FRAMEWORK.md` | NOTHING | seat | 2026-09-06 | NONE | production | LIVE |
| `protocols/DEFINITION_OF_DONE.md` | NOTHING | seat | 2026-08-28 | NONE | production | LIVE |
| `protocols/ESSENTIALS.md` | NOTHING | NOBODY | 2026-09-01 | NONE | **deprecated** — `CLAUDE.md`'s own header states it is *"superseded, pending [#628] — do not boot from it"* | UNREAD (explicitly told not to boot from it) |
| `protocols/archive/HANDOFF_PROCESS_v3.4.md` | NOTHING | NOBODY | 2026-05-29 | NONE | deprecated (superseded by v7, kept immutable) | UNREAD |
| `protocols/archive/HANDOFF_PROCESS_v4.4.md` | NOTHING | NOBODY | 2026-06-11 | NONE | deprecated (superseded by v7, kept immutable) | UNREAD |

---

## docs/

**Zero rows in organ-index.md or FPG-1 process-list name a path under `docs/`.** `docs/` is a
content tree (2,099 tracked files: ~850+ audits, ~130 handoff bundles, ~90 intake files, 92 ADRs),
not a process home, so this page itemizes at the sub-domain / generated-artifact grain — see
Method above.

| Item | Trigger | Reader | Last touched | Owner | Lifecycle | Verdict |
|---|---|---|---|---|---|---|
| `docs/audits/` (sub-domain, ~850+ files, this census's own output location) | gate | organ + seat | 2026-09-11 | the `audit-index-freshness` + `audit-title-gate` pre-commit gates (fire on `docs/audits/*.md` changes) | production | LIVE |
| `docs/audits/README.md` (generated index) | gate | organ + seat | n/a (generated) | the `audit-index-freshness` pre-commit gate (`files: ^docs/audits/README\.md$`) | production | LIVE |
| `docs/decisions/` (sub-domain, 92 ADRs, immutable per `CLAUDE.md` §5) | gate | organ + seat | n/a (many files) | the `claude-rosters-freshness` pre-commit gate (`files:` includes `^docs/decisions/ADR-.*\.md$`, regenerates `.claude/generated/recent-adrs.md`) | production | LIVE |
| `docs/decisions/README.md` (hand-maintained editorial index, per `CLAUDE.md` §12) | NOTHING | seat | n/a | NONE | production | LIVE |
| `docs/handoffs/` (sub-domain, ~130 dated bundles, immutable per `CLAUDE.md` §5) | gate | organ + seat | n/a | the `check-seal-identity` pre-commit gate (`files: ^docs/handoffs/`) | production | LIVE |
| `docs/handoffs/README.md` (canonical operator runbook, `CLAUDE.md` §1) | NOTHING | seat | n/a | NONE | production | LIVE |
| `docs/intake/` (sub-domain, ~90 files, the ADR-98 requirements spine) | gate | organ + seat | n/a | the `intake-index-freshness` pre-commit gate (`files: ^docs/intake/.*\.md$`) | production | LIVE |
| `docs/intake/README.md` (generated Contents block) | gate | organ + seat | n/a | the `intake-index-freshness` pre-commit gate | production | LIVE |
| `docs/intake/manifest.json` (generator state) | gate | organ | n/a | the `intake-index-freshness` pre-commit gate (same `files:` scope) | production | LIVE |
| `docs/archive/` (VISION.md relocated here per `CLAUDE.md` §5 rule 5, marked superseded) | NOTHING | NOBODY | n/a | NONE | deprecated (explicitly superseded) | UNREAD |

---

## ecosystem/

108 tracked files. 33 items below: 6 compressed rows for the homogeneous per-child dated
`history/*.md` streams (90 files total — enumerating each dated file individually would be
re-derivation of a log the generator already produces; see Method), plus 27 individually itemized
registry/schema/generated files. Where no hook in `.pre-commit-config.yaml` names a specific file,
its trigger is marked UNKNOWN rather than guessed.

| Item | Trigger | Reader | Last touched | Owner | Lifecycle | Verdict |
|---|---|---|---|---|---|---|
| `ecosystem/organ-index.md` (generated organ inventory — this census's own source #1) | gate | organ + seat | 2026-09-11 | the `organ-index-freshness` pre-commit gate | production | LIVE |
| `ecosystem/organ-registry.yaml` | gate | organ | 2026-08-11 | the `organ-index-freshness` pre-commit gate (`files:` includes `^ecosystem/organ-registry\.yaml$`) | production | LIVE |
| `ecosystem/provider-registry.yaml` | gate | organ | 2026-08-29 | the `provider-registry-agreement` pre-commit gate | production | LIVE |
| `ecosystem/tool-versions.yaml` | gate | organ | 2026-07-08 | the `provider-registry-agreement` pre-commit gate (same `files:` group as provider-registry.yaml) | production | LIVE |
| `ecosystem/satellite-onboarding-rulings.yaml` | gate | organ | 2026-08-29 | the `provider-registry-agreement` pre-commit gate (same `files:` group) | production | LIVE |
| `ecosystem/derived-copies.yaml` | gate | organ | 2026-09-07 | the `derived-copies-rebind` pre-commit gate (`always_run`, reads this internally) | production | LIVE |
| `ecosystem/doc-code-edge.yaml` (FPG-1 input #1, per `file_purpose_graph.py`'s own docstring) | gate | organ | 2026-09-07 | the `graph-rebuild` pre-commit gate (`always_run`) | production | LIVE |
| `ecosystem/doc-counts.md` | gate | organ | 2026-09-11 | the `doc-counts-pytest-freshness` pre-commit gate | production | LIVE |
| `ecosystem/deployed-versions.yaml` | UNKNOWN | UNKNOWN | 2026-09-07 | UNKNOWN — not named in organ-index.md, FPG-1 process-list, or the process-trigger census; no `.pre-commit-config.yaml` `files:` match found | UNKNOWN (recent edit suggests active use, no wiring evidence) | UNKNOWN |
| `ecosystem/disposition-register.yaml` | UNKNOWN | UNKNOWN | 2026-09-08 | UNKNOWN — same absence as above | UNKNOWN | UNKNOWN |
| `ecosystem/fleet-shape-spec.yaml` | UNKNOWN | UNKNOWN | 2026-09-09 | UNKNOWN — same absence | UNKNOWN | UNKNOWN |
| `ecosystem/parity-surfaces.yaml` | UNKNOWN | UNKNOWN | 2026-09-05 | UNKNOWN — same absence | UNKNOWN | UNKNOWN |
| `ecosystem/routing-table.yaml` | UNKNOWN | UNKNOWN | 2026-09-05 | UNKNOWN — same absence (the `~/.claude/ROUTING.md` derived copy of this is out-of-repo/L0, per `derived-copies-rebind`'s own header comment, but this hub original's own trigger is not named by the five sources) | UNKNOWN | UNKNOWN |
| `ecosystem/north-star.md` | UNKNOWN | seat | 2026-08-31 | UNKNOWN — no wiring evidence in the five sources | UNKNOWN | UNKNOWN |
| `ecosystem/registry.md` | UNKNOWN | seat | 2026-09-01 | UNKNOWN — no wiring evidence | UNKNOWN | UNKNOWN |
| `ecosystem/substrate-registry.yaml` | UNKNOWN | UNKNOWN | 2026-08-27 | UNKNOWN — no wiring evidence | UNKNOWN | UNKNOWN |
| `ecosystem/silent-rule-baseline.yaml` | UNKNOWN | UNKNOWN | 2026-09-06 | UNKNOWN — no wiring evidence (name suggests a ratchet baseline read by `audit-health`'s `check_silent_rule_ratchet`, but no `files:` match confirms it) | UNKNOWN | UNKNOWN |
| `ecosystem/proof-layer-baseline.json` | UNKNOWN | UNKNOWN | 2026-08-27 | UNKNOWN — same pattern (likely read by `audit-health`'s `check_proof_layer`, unconfirmed by a named source) | UNKNOWN | UNKNOWN |
| `ecosystem/dependency-baseline.yaml` | UNKNOWN | UNKNOWN | 2026-07-13 | UNKNOWN — no wiring evidence | UNKNOWN | UNKNOWN |
| `ecosystem/index.yaml` | UNKNOWN | UNKNOWN | 2026-08-05 | UNKNOWN — no wiring evidence, oldest-touched of the registries (37 days stale against base) | deprecated (stale, no evidence of live use) | UNREAD |
| `ecosystem/audit-consumer-baseline.json` | UNKNOWN | UNKNOWN | 2026-09-01 | UNKNOWN — likely `check_consumer_at_landing`'s baseline, unconfirmed | UNKNOWN | UNKNOWN |
| `ecosystem/audit-funnel-baseline.json` | UNKNOWN | UNKNOWN | 2026-09-01 | UNKNOWN — likely `check_funnel_coverage`'s baseline, unconfirmed | UNKNOWN | UNKNOWN |
| `ecosystem/audit-title-baseline.json` | gate | organ | 2026-09-01 | the `audit-title-gate` pre-commit gate — named explicitly in its own `.pre-commit-config.yaml` comment ("grandfathered in `ecosystem/audit-title-baseline.json`") | production | LIVE |
| `ecosystem/conformance.html` / `ecosystem/conformance.md` | UNKNOWN | seat | 2026-09-05 | UNKNOWN — generated-looking pair, no confirmed generator in the five sources | UNKNOWN | UNKNOWN |
| `ecosystem/schema/*.py` (4 files: `__init__.py`, `derived_copies.py`, `desired_state.py`, `provider_registry.py`) | gate (partial) | organ | 2026-09-07 (newest) | `provider_registry.py` is named directly in `provider-registry-agreement`'s `files:` pattern; the other three's trigger is UNKNOWN | production (provider_registry.py); UNKNOWN (the rest) | LIVE (provider_registry.py); UNKNOWN (the rest) |
| `ecosystem/{.dev-knowledge,ai-council,corp-monorepo,corp-ops,corp-sca-time-automation,win-tooling}/history/*.md` (6 compressed streams, ~90 dated files total) | UNKNOWN | UNKNOWN | ranges 2026-05-15 to 2026-08-29 per stream | UNKNOWN — likely `fleet_analytics.py` (CI, `report-only-wall.yml`) or the fleet-baseline schedule, per naming convention, but no `files:` pattern in the five sources names this tree directly | production-looking by cadence, unconfirmed | UNKNOWN |

---

## scripts/

144 tracked files, cross-resolved from `ecosystem/organ-index.md`, FPG-1's `process-list --render`, the 2026-09-08 process-trigger census's orphan reasoning, and `.pre-commit-config.yaml`'s own `entry:` lines (all 28 local git-hooks implement through this folder -- confirmed directly rather than assumed, see Method). Three files version control surfaces for `scripts/` (`backlog_extract.py`, `migrate_links.py`, `validate_scope_tags.py`) are historical deletions, filtered out against a live tracked-file listing before this table was built. Two rows (`gen_task_tree.py`, `validate_doc_rot.py`) needed a direct FPG-1 `why` query to correct: `process-list --render` reports only one upstream trigger per item, and for both it happened to report a secondary import path through the untriggered `scripts/archive_row_body.py` rather than the direct, triggered import from `scripts/audit.py` that `why` also shows -- corrected here rather than left as a false UNKNOWN.

| Item | Trigger | Reader | Last touched | Owner | Lifecycle | Verdict |
|---|---|---|---|---|---|---|
| `scripts/archive_row_body.py` | NOTHING | NOBODY | 2026-08-29 | NONE -- V+1 retirement-or-wiring list | experimental (present, recently touched, not yet triggered) | UNTRIGGERED |
| `scripts/arm_hooks.py` | hook | organ | 2026-08-26 | the SessionStart session-hook run | production | LIVE |
| `scripts/assemble_paste.py` | gate | organ | 2026-09-09 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/audit.py` | gate | organ | 2026-09-07 | the `audit-health` pre-commit gate run | production | LIVE |
| `scripts/audit_checks/_common.py` | gate | organ | 2026-08-16 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/check_adr38_baseline.py -> scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_adr38_baseline.py` | gate | organ | 2026-08-29 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_adr_status_grammar.py` | gate | organ | 2026-09-07 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_amendment_coherence.py` | gate | organ | 2026-08-16 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_boot_byte_budget.py` | gate | organ | 2026-08-16 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_canonical_md_visibility.py` | gate | organ | 2026-08-22 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_canonical_structure.py` | gate | organ | 2026-08-22 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_claude_md.py` | gate | organ | 2026-08-16 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_consumer_at_landing.py` | gate | organ | 2026-08-27 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_dispatch_drift.py` | gate | organ | 2026-08-27 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_dot_prefix_discipline.py` | gate | organ | 2026-08-16 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_floor_integrity.py` | gate | organ | 2026-08-16 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_handoff_bundle_structure.py` | gate | organ | 2026-08-16 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_handoff_version_stamp.py` | gate | organ | 2026-08-16 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_proof_layer.py` | gate | organ | 2026-08-27 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_reconciled_versions.py` | gate | organ | 2026-08-16 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_residual_completeness.py` | gate | organ | 2026-08-16 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_routine_consumers.py` | gate | organ | 2026-08-26 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_routing_agreement.py` | gate | organ | 2026-08-28 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_safe_removal.py` | gate | organ | 2026-08-16 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_substrate_declaration.py` | gate | organ | 2026-08-31 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_vision_md.py` | gate | organ | 2026-09-01 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/check_workspace_settings.py` | gate | organ | 2026-09-09 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/audit_checks/registry.py` | gate | organ | 2026-09-07 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/backlog_source.py` | gate | organ | 2026-08-26 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/batch_manifest.py` | gate | organ | 2026-09-07 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/billing_leak_sentinel.ps1` | hook | organ | 2026-06-06 | the SessionStart session-hook run | production | LIVE |
| `scripts/block_commit_on_main.py` | gate | organ | 2026-08-19 | the `block-commit-on-main` pre-commit gate run | production | LIVE |
| `scripts/block_ff_push.py` | gate | organ | 2026-08-19 | the `block-ff-push` pre-push gate run | production | LIVE |
| `scripts/block_unanchored_push.py` | gate | organ | 2026-09-07 | the `block-unanchored-push` pre-push gate run | production | LIVE |
| `scripts/boot_frontier.py` | hook | organ | 2026-09-01 | the PreToolUse + SessionStart session-hook runs (chained via scripts/fleet_health.py) | production | LIVE |
| `scripts/boundary_headers.py` | NOTHING | NOBODY | 2026-08-04 | NONE -- V+1 retirement-or-wiring list | deprecated (untriggered and stale) | UNTRIGGERED |
| `scripts/boundary_report.py` | NOTHING | NOBODY | 2026-08-12 | NONE -- V+1 retirement-or-wiring list | deprecated (untriggered and stale) | UNTRIGGERED |
| `scripts/canonical_docs.py` | gate | organ | 2026-09-03 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/canonical_freshness_gate.py` | gate | organ | 2026-09-04 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/changelog_sentinel.py` | hook | organ | 2026-08-22 | the SessionStart session-hook run | production | LIVE |
| `scripts/check_backlog_commit_msg.py` | gate | organ | 2026-06-07 | the `backlog-id-on-close` commit-msg gate run | production | LIVE |
| `scripts/check_backlog_filing.py` | gate | organ | 2026-08-26 | the `backlog-filing-backpressure` commit-msg gate run | production | LIVE |
| `scripts/check_derived_copies.py` | gate | organ | 2026-09-07 | the `derived-copies-rebind` pre-commit gate run | production | LIVE |
| `scripts/check_provider_registry.py` | gate | organ | 2026-08-24 | the `provider-registry-agreement` pre-commit gate run | production | LIVE |
| `scripts/check_seal_identity.py` | gate | organ | 2026-08-02 | the `check-seal-identity` pre-commit gate run | production | LIVE |
| `scripts/cloud_provisioning.py` | NOTHING | NOBODY | 2026-08-21 | NONE -- V+1 retirement-or-wiring list | deprecated (untriggered and stale) | UNTRIGGERED |
| `scripts/codemap/__init__.py` | gate | organ | 2026-05-22 | the `codemap-freshness` pre-commit gate run | production | LIVE |
| `scripts/codemap/ast_walker.py` | gate | organ | 2026-05-22 | the `codemap-freshness` pre-commit gate run (chained via scripts/codemap/generator.py -> scripts/codemap/__init__.py) | production | LIVE |
| `scripts/codemap/check.py` | gate | organ | 2026-07-05 | the `codemap-freshness` pre-commit gate run (chained via scripts/codemap/__init__.py) | production | LIVE |
| `scripts/codemap/cli.py` | gate | organ | 2026-07-06 | the `codemap-freshness` pre-commit gate run | production | LIVE |
| `scripts/codemap/generator.py` | gate | organ | 2026-07-05 | the `codemap-freshness` pre-commit gate run (chained via scripts/codemap/__init__.py) | production | LIVE |
| `scripts/codemap/mermaid_emit.py` | gate | organ | 2026-05-28 | the `codemap-freshness` pre-commit gate run (chained via scripts/codemap/text_emit.py -> scripts/codemap/generator.py -> scripts/codemap/__init__.py) | production | LIVE |
| `scripts/codemap/text_emit.py` | gate | organ | 2026-07-05 | the `codemap-freshness` pre-commit gate run (chained via scripts/codemap/generator.py -> scripts/codemap/__init__.py) | production | LIVE |
| `scripts/codemap_hook.py` | hook (exported, consumer-only) | organ | 2026-06-03 | a consumer repo's own pre-commit run (via .pre-commit-hooks.yaml) -- does not fire in this hub | production | LIVE |
| `scripts/coherence_enumerator.py` | gate | organ | 2026-06-17 | the `audit-health` pre-commit gate run (chained via scripts/scan_undeclared_edges.py -> scripts/audit.py) | production | LIVE |
| `scripts/coherence_nudge.py` | gate | organ | 2026-07-22 | the `coherence-nudge` pre-commit gate run (non-blocking) | production | LIVE |
| `scripts/consumer_at_landing.py` | gate | organ | 2026-09-05 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/check_consumer_at_landing.py -> scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/cost_usage_telemetry.py` | NOTHING | NOBODY | 2026-09-01 | NONE -- V+1 retirement-or-wiring list | experimental (present, recently touched, not yet triggered) | UNTRIGGERED |
| `scripts/desired_state_loader.py` | NOTHING | NOBODY | 2026-07-31 | NONE -- V+1 retirement-or-wiring list | deprecated (untriggered and stale) | UNTRIGGERED |
| `scripts/desired_state_report.py` | NOTHING | NOBODY | 2026-08-19 | NONE -- V+1 retirement-or-wiring list | deprecated (untriggered and stale) | UNTRIGGERED |
| `scripts/dispatch_drift.py` | gate | organ | 2026-08-27 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/check_dispatch_drift.py -> scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/dispatch_surface.py` | gate | organ | 2026-08-27 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/enforcement_coverage.py` | gate | organ | 2026-09-02 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/export_backlog_view.py` | NOTHING | NOBODY | 2026-08-22 | NONE -- [#563] -- settled; reopening needs a ruling, not a lane | deprecated (nearest fit -- intentionally unwired by ruling, not decaying) | UNTRIGGERED (intentionally, by ruling -- not a garbage-candidate) |
| `scripts/failed_set.py` | NOTHING | NOBODY | 2026-09-02 | NONE -- V+1 retirement-or-wiring list | experimental (present, recently touched, not yet triggered) | UNTRIGGERED |
| `scripts/file_purpose_graph.py` | gate | organ | 2026-09-09 | the `graph-rebuild` pre-commit gate run (chained via scripts/graph_store.py) | production | LIVE |
| `scripts/fleet-baseline.task.xml` | schedule | organ | 2026-06-06 | the fleet-baseline Task Scheduler entry (daily 09:00, State=Ready) | production | LIVE |
| `scripts/fleet_analytics.py` | gate (CI) | organ | 2026-08-08 | the report-only-wall.yml CI run (push to main / workflow_dispatch) | production | LIVE |
| `scripts/fleet_health.py` | hook | organ | 2026-09-07 | the PreToolUse + SessionStart session-hook runs | production | LIVE |
| `scripts/fleet_parity.py` | gate | organ | 2026-08-25 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/funnel_coverage.py` | gate | organ | 2026-09-05 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/funnel_lifecycle.py` | gate | organ | 2026-08-29 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/gen_audit_index.py` | gate | organ | 2026-09-01 | the `audit-index-freshness` + `audit-title-gate` pre-commit gate runs | production | LIVE |
| `scripts/gen_claude_rosters.py` | gate | organ | 2026-08-13 | the `claude-rosters-freshness` pre-commit gate run | production | LIVE |
| `scripts/gen_dashboard.py` | gate | organ | 2026-08-26 | the `audit-health` pre-commit gate run (chained via scripts/generated_artifact_freshness.py -> scripts/audit.py) | production | LIVE |
| `scripts/gen_doc_counts.py` | gate | organ | 2026-08-01 | the `doc-counts-pytest-freshness` pre-commit gate run | production | LIVE |
| `scripts/gen_handoff.py` | gate | organ | 2026-09-09 | the `audit-health` pre-commit gate run (chained via scripts/assemble_paste.py -> scripts/audit.py) | production | LIVE |
| `scripts/gen_intake_index.py` | gate | organ | 2026-09-07 | the `intake-index-freshness` pre-commit gate run | production | LIVE |
| `scripts/gen_intake_tree.py` | gate | organ | 2026-09-07 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/gen_lane_contract.py` | gate | organ | 2026-09-02 | the `lane-contract-check` pre-commit gate run | production | LIVE |
| `scripts/gen_ledger.py` | NOTHING | NOBODY | 2026-09-09 | NONE -- V+1 retirement-or-wiring list | experimental (present, recently touched, not yet triggered) | UNTRIGGERED |
| `scripts/gen_methodology_roster.py` | gate | organ | 2026-08-01 | the `roster-freshness` pre-commit gate run | production | LIVE |
| `scripts/gen_north_star.py` | NOTHING | NOBODY | 2026-08-31 | NONE -- V+1 retirement-or-wiring list | experimental (present, recently touched, not yet triggered) | UNTRIGGERED |
| `scripts/gen_seat_boot.py` | gate | organ | 2026-09-09 | the `audit-health` pre-commit gate run (chained via scripts/gen_handoff.py -> scripts/assemble_paste.py -> scripts/audit.py) | production | LIVE |
| `scripts/gen_task_tree.py` | gate | organ | 2026-08-26 | the `audit-health` pre-commit gate run (imported directly by scripts/audit.py per FPG-1 `why`; process-list's `--render` reported a secondary, itself-untriggered import path via scripts/archive_row_body.py instead -- corrected here against the fuller `why` query) | production | LIVE |
| `scripts/gen_trend_dashboard.py` | NOTHING | NOBODY | 2026-09-01 | NONE -- V+1 retirement-or-wiring list | experimental (present, recently touched, not yet triggered) | UNTRIGGERED |
| `scripts/generate_floor.py` | gate | organ | 2026-07-01 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/check_floor_integrity.py -> scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/generate_organ_index.py` | gate | organ | 2026-08-12 | the `organ-index-freshness` pre-commit gate run | production | LIVE |
| `scripts/generated_artifact_freshness.py` | gate | organ | 2026-08-26 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/gitenv.py` | gate | organ | 2026-08-08 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/governance_health.py` | gate | organ | 2026-08-29 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/graph_queries.py` | gate | organ | 2026-09-09 | the `graph-orphan-census`+`graph-task-coverage`+`graph-process-list` pre-commit gate runs | production | LIVE |
| `scripts/graph_store.py` | gate | organ | 2026-09-09 | the `graph-rebuild` pre-commit gate run | production | LIVE |
| `scripts/hooks/block_immutable_edits.py` | hook | organ | 2026-06-06 | the PreToolUse session-hook run | production | LIVE |
| `scripts/impacted_tests.py` | gate | organ | 2026-09-11 | the `impacted-tests-guard` pre-commit gate run | production | LIVE |
| `scripts/journal_anchor.py` | gate | organ | 2026-09-07 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/logs_retention.py` | NOTHING | NOBODY | 2026-09-04 | NONE -- V+1 retirement-or-wiring list | experimental (present, recently touched, not yet triggered) | UNTRIGGERED |
| `scripts/nopack_sandbox.py` | NOTHING | NOBODY | 2026-09-01 | NONE -- V+1 retirement-or-wiring list | experimental (present, recently touched, not yet triggered) | UNTRIGGERED |
| `scripts/normalize_headers.py` | gate | organ | 2026-08-03 | the `normalize-dated-headers` pre-commit gate run | production | LIVE |
| `scripts/offload_admission.py` | NOTHING | NOBODY | 2026-09-09 | NONE -- V+1 retirement-or-wiring list | experimental (present, recently touched, not yet triggered) | UNTRIGGERED |
| `scripts/preflight_contract.py` | gate | organ | 2026-09-01 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/probe_child_backlogs.py` | NOTHING | NOBODY | 2026-06-19 | NONE -- V+1 retirement-or-wiring list | deprecated (untriggered and stale) | UNTRIGGERED |
| `scripts/proof_layer.py` | gate | organ | 2026-08-27 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/check_proof_layer.py -> scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/propose_closures.py` | NOTHING | organ | 2026-09-06 | NONE as a direct trigger -- DERIVED-COPY SOURCE per FPG-1's own note: "the armed process is the plugin copy plugins/tier1-lifecycle/scripts/propose_closures.py... a source is not an orphan, it is upstream"; paired via ecosystem/derived-copies.yaml | production | LIVE -- upstream of an armed process, not an orphan |
| `scripts/provider_registry.py` | hook | organ | 2026-08-24 | the SessionStart session-hook run (chained via scripts/changelog_sentinel.py) | production | LIVE |
| `scripts/reverse_dep_oracle.py` | gate | organ | 2026-06-20 | the `audit-health` pre-commit gate run (chained via scripts/safe_remove.py -> scripts/audit_checks/check_safe_removal.py -> scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/review_closures.py` | command | seat | 2026-09-01 | the operator (act: ratification) | production | LIVE |
| `scripts/routing_agreement.py` | gate | organ | 2026-09-02 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/check_routing_agreement.py -> scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/safe_remove.py` | gate | organ | 2026-08-01 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/check_safe_removal.py -> scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/scan_undeclared_edges.py` | gate | organ | 2026-06-20 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/seat_ch8.py` | gate | organ | 2026-09-09 | the `audit-health` pre-commit gate run (chained via scripts/gen_seat_boot.py -> scripts/gen_handoff.py -> scripts/assemble_paste.py -> scripts/audit.py) | production | LIVE |
| `scripts/seat_refusals.py` | gate | organ | 2026-09-09 | the `audit-health` pre-commit gate run (chained via scripts/gen_seat_boot.py -> scripts/gen_handoff.py -> scripts/assemble_paste.py -> scripts/audit.py) | production | LIVE |
| `scripts/seed_runbook.py` | NOTHING | NOBODY | 2026-07-18 | NONE -- V+1 retirement-or-wiring list | deprecated (untriggered and stale) | UNTRIGGERED |
| `scripts/session_end_backpressure.py` | hook | organ | 2026-08-26 | the Stop session-hook run | production | LIVE |
| `scripts/setup-fleet-scheduler.ps1` | NOTHING | NOBODY | 2026-06-06 | the operator (machine setup, one-shot installer -- not repo wiring); the TASK it registers (scripts/fleet-baseline.task.xml) IS triggered, the installer script itself is not | deprecated (one-shot, not a recurring process) | LIVE -- the registered task is live even though this installer script fires only once |
| `scripts/silent_rule_detector.py` | gate | organ | 2026-08-24 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/single_flight.py` | command | seat | 2026-08-22 | the operator (act: GO) | production | LIVE |
| `scripts/surface_triage.ps1` | hook | organ | 2026-07-08 | the SessionStart session-hook run | production | LIVE |
| `scripts/telemetry_emit.py` | gate | organ | 2026-08-21 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/toc/__init__.py` | gate | organ | 2026-06-03 | the `toc-freshness-playbook` pre-commit gate run | production | LIVE |
| `scripts/toc/check.py` | gate | organ | 2026-06-03 | the `toc-freshness-playbook` pre-commit gate run (chained via scripts/toc/__init__.py) | production | LIVE |
| `scripts/toc/cli.py` | gate | organ | 2026-08-01 | the `toc-freshness-playbook` pre-commit gate run | production | LIVE |
| `scripts/toc/generator.py` | gate | organ | 2026-08-03 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/toc_hook.py` | hook (exported, consumer-only) | organ | 2026-06-03 | a consumer repo's own pre-commit run (via .pre-commit-hooks.yaml) -- does not fire in this hub | production | LIVE |
| `scripts/trace_writer.py` | NOTHING | NOBODY | 2026-09-05 | NONE -- V+1 retirement-or-wiring list | experimental (present, recently touched, not yet triggered) | UNTRIGGERED |
| `scripts/validate_adr_status.py` | gate | organ | 2026-09-07 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/check_adr_status_grammar.py -> scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/validate_backlog.py` | gate | organ | 2026-08-27 | the `validate-backlog` pre-commit gate run | production | LIVE |
| `scripts/validate_branch_naming.py` | gate | organ | 2026-09-07 | the `audit-health` pre-commit gate run (chained via scripts/batch_manifest.py -> scripts/audit.py) | production | LIVE |
| `scripts/validate_doc_claims.py` | gate | organ | 2026-08-27 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/validate_doc_code_edge.py` | gate | organ | 2026-06-27 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/validate_doc_rot.py` | gate | organ | 2026-09-05 | the `audit-health` pre-commit gate run (imported directly by scripts/audit.py per FPG-1 `why`; process-list's `--render` reported a secondary, itself-untriggered import path via scripts/archive_row_body.py instead -- corrected here against the fuller `why` query) | production | LIVE |
| `scripts/validate_doc_structure.py` | gate | organ | 2026-08-22 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/validate_git_backlog.py` | gate | organ | 2026-07-28 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/validate_hermetization.py` | gate | organ | 2026-09-09 | the `validate-hermetization` pre-commit gate run | production | LIVE |
| `scripts/validate_landing_predicate.py` | gate | organ | 2026-08-13 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/validate_no_ff.py` | hook (exported, consumer-only) | organ | 2026-06-27 | a consumer repo's own pre-commit run (via .pre-commit-hooks.yaml) -- does not fire in this hub | production | LIVE |
| `scripts/validate_onboarding_rulings.py` | NOTHING | NOBODY | 2026-07-16 | NONE -- V+1 retirement-or-wiring list | deprecated (untriggered and stale) | UNTRIGGERED |
| `scripts/validate_reconciliation.py` | gate | organ | 2026-08-28 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/check_reconciled_versions.py -> scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/validate_residual_completeness.py` | gate | organ | 2026-07-19 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/check_residual_completeness.py -> scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/validate_substrate.py` | gate | organ | 2026-09-07 | the `audit-health` pre-commit gate run (chained via scripts/audit_checks/check_substrate_declaration.py -> scripts/audit_checks/registry.py -> scripts/audit.py) | production | LIVE |
| `scripts/verify_handoff_probes.py` | gate | organ | 2026-09-09 | the `audit-health` pre-commit gate run (chained via scripts/audit.py) | production | LIVE |
| `scripts/window_metrics.py` | NOTHING | NOBODY | 2026-09-07 | NONE -- V+1 retirement-or-wiring list | experimental (present, recently touched, not yet triggered) | UNTRIGGERED |
| `scripts/worktree_import_proof.py` | command | seat | 2026-08-07 | the operator (act: GO) | production | LIVE |
| `scripts/worktree_seed.py` | command | seat | 2026-08-07 | the operator (act: GO) | production | LIVE |

---

## tests/

**Both of the two most authoritative sources on this folder agree it is deliberately excluded
from the trigger graph.** `scripts/file_purpose_graph.py`'s own docstring states: *"`tests/` is
still UNKNOWN and `why` still refuses it... which remains the finding this header always claimed
it was."* The 2026-09-08 process-trigger census's own method section states: *"A `tests/`
reference is not a trigger... nothing schedules it."* 235 tracked files (172 top-level + `fixtures/`).

| Item | Trigger | Reader | Last touched | Owner | Lifecycle | Verdict |
|---|---|---|---|---|---|---|
| `tests/` (the suite as a whole) | NOTHING — per FPG-1's own explicit refusal and the census's own method rule | NOBODY, per strict source reading. **Mixed evidence, stated per the contract's own allowance:** `AGENTS.md` names `uv run --locked pytest -x --tb=short` as the standard build/test command, and `scripts/impacted_tests.py` (the `impacted-tests-guard` pre-commit gate, itself a `scripts/` item) selects and runs a subset of this suite on every commit that touches `scripts/*.py` — but neither organ-index.md, FPG-1, nor the census counts a test file itself as triggered or as a reader; this is the sources' own explicit exclusion, not an oversight of this lane. | 2026-09-11 (`impacted_tests.py`'s own companion test) | NONE, per the strict graph reading | production, by the same mixed-evidence override used elsewhere on this page (git-log cadence and the `impacted-tests-guard` gate both evidence active, current use even though no source counts a test as "triggered") | LIVE |
| `tests/fixtures/` | NOTHING | NOBODY, same reasoning | n/a | NONE | production (in active use by the suite above it) | LIVE |

---

## templates/

54 tracked files, zero organ-index/FPG-1 rows. Items below cover the named, individually-sourced
files; the remaining ~40 boilerplate templates (workspace configs, `*-template.md` authoring
scaffolds) are compressed into one row per the Method note.

| Item | Trigger | Reader | Last touched | Owner | Lifecycle | Verdict |
|---|---|---|---|---|---|---|
| `templates/claude-regions/*.md` (hub-region source of truth, `CLAUDE.md` §4 rule 6: "a hub region's body in CLAUDE.md stays byte-identical to its templates/claude-regions/*.md source") | UNKNOWN | organ | UNKNOWN | UNKNOWN — `CLAUDE.md` states the byte-identity requirement in prose ("divergence breaks deploy parity") but no git-hook enforcing it was found among the 29 read from `.pre-commit-config.yaml`; **this is itself a finding, not confirmed as absent** (a hook could exist outside the ones this census cross-checked by name) | production (actively used by deploy carriers, per `deploy/carrier_docs.py`'s naming) | LIVE, with the enforcement gap flagged rather than assumed closed |
| `templates/child-methodology-floor.md.tmpl` + `.sha256` sidecar | gate (indirect) | organ | UNKNOWN | the `audit-health` pre-commit gate, via `check_floor_integrity` → `scripts/generate_floor.py` (a `scripts/` item) | production | LIVE |
| `templates/ADR-template.md`, `templates/intake-template.md`, `templates/audit-template.md`, `templates/CLAUDE-md-template.md`, `templates/ARCHITECTURE-template.md`, `templates/README-md-template.md`, `templates/CONTRIBUTING-md-template.md`, `templates/prompt-template.md`, `templates/codex-review-config-template.md`, `templates/consumer-onboarding-runbook.md`, `templates/scrum-master-cover-letter.md`, `templates/ruff-config-block.toml`, `templates/workspace-{S,M,L}.code-workspace` (14 files, compressed to one row) | NOTHING | seat | n/a | NONE | production (authoring scaffolds, consulted on demand) | LIVE |
| `templates/handoff/` (bundle-authoring templates) | NOTHING | seat | n/a | NONE | production | LIVE |
| `templates/archive/` | NOTHING | NOBODY | n/a | NONE | deprecated (archival by design) | UNREAD |

---

## tasks/

FPG-1's own docstring names `tasks/**` `depends-on` as input #4 and `tasks/**` OPEN rows as
input #7: *"`tasks/` is the SOURCE OF TRUTH; `BACKLOG.md` is a generated one-line view and is
never read for edges."* 447 tracked files. `BACKLOG.md` itself lives at repo root, not under
`tasks/` — mentioned here in prose, not itemized (see Method).

| Item | Trigger | Reader | Last touched | Owner | Lifecycle | Verdict |
|---|---|---|---|---|---|---|
| `tasks/` (the row graph, source of truth — FPG-1 inputs #4 and #7) | gate | organ | n/a (447 files) | the `validate-backlog` pre-commit gate (`files:` includes `^tasks/.*\.(md\|json)$`) plus `graph-rebuild`/`graph-task-coverage` (`always_run`) | production | LIVE |
| `tasks/manifest.json` (generator state for `gen_task_tree.py`, which renders `BACKLOG.md`) | gate | organ | n/a | the `validate-backlog` pre-commit gate (same `files:` pattern matches `.json`) | production | LIVE |
| `tasks/README.md` | NOTHING | seat | n/a | NONE | production | LIVE |
| `tasks/archive/` (closed-task narration relief) | NOTHING | NOBODY (archival) | n/a | NONE | deprecated (closed rows, archived by design) | UNREAD |

---

## logs/

Only 2 tracked files exist under `logs/` — earlier drafts of this page picked up
`logs/DETECTOR-ERROR-2026-09-05.md` via a scoping bug in this lane's own git-log tooling (a commit
touching both `logs/` and another folder leaked the other folder's filename into the `logs/`
listing); re-verified against a live `git ls-files logs/` before this page was written, and that
file is **not** currently tracked under `logs/` — corrected here rather than left in, per the
contract's own "resolve a locator before acting on it."

| Item | Trigger | Reader | Last touched | Owner | Lifecycle | Verdict |
|---|---|---|---|---|---|---|
| `logs/TOKEN-LOG.md` (append-only, `CLAUDE.md` §4 file-lifecycle convention) | NOTHING | seat | 2026-08-04 | NONE (hand-appended by convention, no automated writer found in the five sources) | **deprecated, mixed evidence**: 38 days stale against this census's 2026-09-11 base, no recent appends found, yet still named as a live append-only convention in `CLAUDE.md` §4 — the git-log evidence favors staleness over active use; flagged as a lower-confidence call for the operator rather than asserted as settled | UNREAD |

`logs/COHERENCE-NUDGE.log` is named by the `coherence-nudge` hook's own comment as its append
target but is **not tracked by git** (a gitignored runtime artifact) — carries no git history, so
it is disclosed here in prose rather than given a row this census cannot source.

---

## deploy/

**A finding, not an oversight:** 28 tracked files, and **zero** of them appear in
`ecosystem/organ-index.md` or FPG-1's `process-list`. This is directly corroborated by
`.pre-commit-config.yaml`'s own comment on the `impacted-tests-guard` hook: *"`deploy/` and
`plugins/` are deliberately OUT of scope: they were not measured for this."* `deploy/` hosts a
whole class of "carrier" Python scripts invisible to both trigger-graph sources — recorded per the
contract's "record the disagreement, do not reconcile it," not repaired.

| Item | Trigger | Reader | Last touched | Owner | Lifecycle | Verdict |
|---|---|---|---|---|---|---|
| `deploy/tool.py` (likely CLI entry point, by naming convention) | command, inferred | seat | 2026-09-07 | the operator (act: **deploy** — one of the census's seven closed on-demand acts), inferred from the process-trigger census's own methodology naming "deploy" as a legitimate act; **not confirmed by organ-index.md or FPG-1, both of which are silent on this whole folder** | production | LIVE, with the sourcing caveat above |
| `deploy/carrier_docs.py`, `carrier_floor.py`, `carrier_globalconfig.py`, `carrier_mesh.py`, `carrier_plugin.py`, `carrier_precommit.py` (6 carrier scripts) | command, inferred | seat | 2026-07-03 to 2026-09-07 (range) | the operator (act: deploy), same inference and same caveat as `tool.py` | production | LIVE, same caveat |
| `deploy/contract.py`, `deploy/floor_conformance.py`, `deploy/floor_mechanisms.py`, `deploy/release_lint.py` (4 support scripts) | command, inferred | seat | 2026-07-04 to 2026-09-07 (range) | the operator (act: deploy), same inference | production | LIVE, same caveat |
| `deploy/lived_sandbox/*.py` (8-file subpackage: `__init__`, `arc`, `cli`, `consumer`, `isolation`, `observe`, `oracle`, `spawn`) | UNKNOWN | UNKNOWN | 2026-07-04 to 2026-07-06 (range, oldest cluster in `deploy/`) | UNKNOWN — absent from all five named sources, and unlike the carrier/support scripts above it has no clear "deploy act" naming tie | **deprecated**, evidence: 67+ days stale against the 2026-09-11 base and zero wiring evidence anywhere | UNTRIGGERED |
| `deploy/manifest-v1.5.0.yaml` (current — cited by name in `.pre-commit-config.yaml` comments and `.claude/methodology-roster.md`'s own header) | gate | organ | 2026-09-07 | the `organ-index-freshness` + `roster-freshness` pre-commit gates (`files:` patterns both include `^deploy/manifest-v.*\.yaml$`) | production | LIVE |
| `deploy/manifest-v{1.0.0,1.1.0,1.2.0,1.3.0,1.3.1,1.4.0}.yaml` (6 superseded manifests) | gate | organ | 2026-08-29 to 2026-08-31 (range) | same two gates fire on any manifest edit, but nothing currently cites these by version — superseded by v1.5.0 | deprecated (superseded, kept per the fleet's own "tagged manifests are maintained, not frozen" practice — historical record, not garbage) | UNREAD |
| `deploy/global-instructions-codex.md` (the `~/.codex/AGENTS.md` carrier source, per `AGENTS.md`'s own precedence section) | UNKNOWN | seat (external, at the L0 `~/.codex/` consumer) | 2026-08-29 | UNKNOWN — named as load-bearing by `AGENTS.md` itself but not by any of the five census sources; likely carried by `deploy/carrier_globalconfig.py`, unconfirmed | production | LIVE, unconfirmed wiring |
| `deploy/release-v1.3.x-contract.md` | NOTHING | seat | 2026-08-08 | NONE | deprecated (named for a superseded release line, v1.5.0 is current) | UNREAD |

---

## .claude/

19 tracked files (organ-index.md accounts for 14 of them as named organs — 9 commands, 2 skills,
1 workflow, 1 rule, 1 agent — with 5 more support/generated files carried alongside).

| Item | Trigger | Reader | Last touched | Owner | Lifecycle | Verdict |
|---|---|---|---|---|---|---|
| `.claude/agents/artifact-reader.md` | command (subagent-dispatch) | organ | 2026-07-07 | the harness's subagent-dispatch mechanism (agent-class organ, `ARMED`) | production | LIVE |
| `.claude/commands/boot-session.md` | command | seat | 2026-09-01 | the operator (act: sitting) | production | LIVE |
| `.claude/commands/handoff.md` | command | seat | 2026-09-09 | the operator (act: seat release) | production | LIVE |
| `.claude/commands/handoff-verify.md` | command | seat | 2026-09-01 | the operator (act: seat release) | production | LIVE |
| `.claude/commands/lane-boot.md` | command | seat | 2026-09-07 | the operator (act: GO) | production | LIVE |
| `.claude/commands/lane-integrate.md` | command | seat | 2026-09-07 | the operator (act: GO) | production | LIVE |
| `.claude/commands/changelog-review.md` | command | seat | 2026-08-28 | the operator, ad-hoc — its own frontmatter/the census both mark it "PUSH trigger only: a SessionStart sentinel NUDGES it, which is not a trigger" — not one of the census's seven named acts | experimental — evidence: present, recently touched, not yet a clean act | UNTRIGGERED (per the process-trigger census's stricter framing; this contract's own broader `command` trigger vocabulary still fires it on operator invocation, so verdict is a judgment call flagged here rather than smoothed) |
| `.claude/commands/preflight.md` | command | seat | 2026-08-04 | the operator, ad-hoc — own frontmatter: "wired into no gate"; not one of the seven acts | experimental (a self-declared adoption-first read-only helper — a legitimate shape for one, per the census) | UNTRIGGERED, same framing caveat as above |
| `.claude/commands/save.md` | command | seat | 2026-05-16 | the operator, ad-hoc — convenience wrapper, not one of the seven acts; FPG-1's own note: "INVISIBLE TO THE CENSUS'S OWN MECHANISM until this lane made every process file a node" | production (oldest command file, in continuous ad-hoc use) | LIVE |
| `.claude/commands/override.md` | command | seat | 2026-08-06 | the operator, ad-hoc | **deprecated** — organ-index.md Status: `RETIRED` (ADR-85 amendment 2026-08-03 §A2); "discharges no gate, arms only a local telemetry token"; kept deliberately as its own retirement notice (2026-09-07 ruling) | UNTRIGGERED (still typeable, but its original gate-bypass effect is inert) |
| `.claude/generated/commands-repo.md` | gate | organ + seat | 2026-09-01 | the `claude-rosters-freshness` pre-commit gate | production | LIVE |
| `.claude/generated/recent-adrs.md` | gate | organ + seat | 2026-09-07 | the `claude-rosters-freshness` pre-commit gate | production | LIVE |
| `.claude/methodology-roster.md` | gate | organ + seat | 2026-09-07 | the `roster-freshness` pre-commit gate | production | LIVE |
| `.claude/rules/git-discipline.md` | NOTHING (context-load) | seat | 2026-08-28 | NONE — loaded every session per its own `rule` class (organ-index.md), not fired by any wiring surface | production | LIVE |
| `.claude/settings.json` (the session-hook + rule wiring declaration itself) | gate | organ | 2026-09-07 | the `organ-index-freshness` + `provider-registry-agreement` pre-commit gates (both name it in `files:`) | production | LIVE |
| `.claude/skills/check-against-spec/SKILL.md` | NOTHING | seat | 2026-06-25 | NONE — "no event fires a skill; a skill is read when a seat chooses to read it" (census's own finding) | production | LIVE |
| `.claude/skills/verify/SKILL.md` | NOTHING | seat | 2026-09-11 | NONE, same reasoning | production | LIVE |
| `.claude/skills/verify/verify.py` (the skill's own script — not itself a named organ row, riding along under its `SKILL.md`) | NOTHING | seat | 2026-09-11 | NONE | production | LIVE |
| `.claude/workflows/conformance-hub.js` | command (operator Workflow tool, or cloud Routine) | seat | 2026-09-02 | the operator, ad-hoc (Workflow invocation) | production | LIVE |

---

## config/ — **ADDED, not named in AX6-1**

Flagged per the contract's own instruction: AX6-1's trigger note records the earlier pass "missed
ecosystem, logs/garbage, protocols-as-process, visualization/dashboard, scripts, templates" —
`config/` and `plugins/` are two more the ten-folder list omits, censused here so this pass does
not reproduce the defect it exists to find.

Exactly 1 tracked file.

| Item | Trigger | Reader | Last touched | Owner | Lifecycle | Verdict |
|---|---|---|---|---|---|---|
| `config/requirements-dev.txt` | NOTHING | UNKNOWN | 2026-05-15 | NONE — not named in organ-index.md, FPG-1 process-list, or the process-trigger census; oldest-touched file found anywhere in this census (119 days stale against the 2026-09-11 base) | **deprecated** — the repo's own declared dependency spine is `pyproject.toml` + `uv.lock` + `.python-version` per `AGENTS.md`'s Environment section, which names no role for a `requirements-dev.txt`; this file is not cited by any of the five sources and is the single oldest-touched tracked file in the entire repo | **GARBAGE-CANDIDATE** — the strongest candidate this census found: sole content of an entire top-level folder, unreferenced by any named source, untouched for 119 days, and superseded in role by the `uv`-pinned dependency chain `AGENTS.md` itself declares canonical. Per the contract: this is a **proposal awaiting the operator's GO**, not an action — nothing was deleted or moved. |

---

## plugins/ — **ADDED, not named in AX6-1**

Flagged per the same contract instruction as `config/` above. 11 tracked files, all under
`plugins/tier1-lifecycle/` — this repo's only plugin. `.pre-commit-config.yaml`'s own comment on
`impacted-tests-guard` names `plugins/` (alongside `deploy/`) as deliberately unmeasured for that
gate — disclosed, not reconciled.

| Item | Trigger | Reader | Last touched | Owner | Lifecycle | Verdict |
|---|---|---|---|---|---|---|
| `plugins/tier1-lifecycle/.claude-plugin/plugin.json` | NOTHING | organ | 2026-07-28 | NONE — read once at plugin-enable time (`.claude/settings.json`), which organ-index.md records as a state ("enabled in .claude/settings.json (v0.1.11)") rather than a repeatable trigger | production | LIVE |
| `plugins/tier1-lifecycle/commands/review-closures.md` | command | seat | 2026-07-29 | the operator (act: ratification) | production | LIVE |
| `plugins/tier1-lifecycle/commands/ship.md` | command | seat | 2026-07-05 | the operator (act: destructive acts) | production | LIVE |
| `plugins/tier1-lifecycle/hooks/hooks.json` | NOTHING (declarative wiring) | organ | 2026-06-02 | NONE — declares the Stop-hook wiring for `propose_closures.py` below; not itself triggered | production | LIVE |
| `plugins/tier1-lifecycle/scripts/propose_closures.py` (the ARMED copy) | hook | organ | 2026-09-06 | the plugin `Stop` session-hook, wired via `hooks.json` — fires every turn-stop; this session's own boot reported closures proposed, corroborating live firing | production | LIVE |
| `plugins/tier1-lifecycle/scripts/review_closures.py` | command | organ | 2026-09-02 | the operator, via `/review-closures` (act: ratification) — invokes this plugin copy | production | LIVE |
| `plugins/tier1-lifecycle/scripts/validate_backlog.py` | script (chained) | organ | 2026-08-27 | `propose_closures.py` (the Stop-hook run above) — called internally by it | production | LIVE |
| `plugins/tier1-lifecycle/assets/ruff-pre-commit.yaml` | UNKNOWN | organ | 2026-06-02 | UNKNOWN — likely a template asset for the `carrier_plugin.py`/`carrier_precommit.py` deploy carriers (`deploy/` items, also UNKNOWN-wiring per that page), unconfirmed by any of the five named sources | UNKNOWN | UNKNOWN |
| `plugins/tier1-lifecycle/INSTALL.md` | NOTHING | seat | 2026-07-29 | NONE — cited by `CLAUDE.md`'s methodology-roster header ("`INSTALL.md` — tier1-lifecycle plugin install guide") | production | LIVE |
| `plugins/tier1-lifecycle/tests/test_plugin_paths.py` | NOTHING | NOBODY (a test is not a trigger, per the census's own method) | 2026-06-02 | NONE | production (proves the plugin's path resolution) | LIVE |
| `plugins/tier1-lifecycle/tests/test_validate_backlog_floor.py` | NOTHING | NOBODY, same reasoning | 2026-06-19 | NONE | production | LIVE |

---

## MANIFEST

Computed directly from this document's own body (every row of every table above, tallied by its
Verdict cell) — the manifest and the pages cannot disagree because the manifest is a count of the
pages, not a separately-asserted number, per the contract's own requirement.

| Folder | Items | LIVE | UNTRIGGERED | UNREAD | GARBAGE-CANDIDATE | UNKNOWN |
|---|---|---|---|---|---|---|
| protocols/ | 17 | 14 | 0 | 3 | 0 | 0 |
| docs/ | 10 | 9 | 0 | 1 | 0 | 0 |
| ecosystem/ | 26 | 10 | 0 | 1 | 0 | 15 |
| scripts/ | 144 | 124 | 20 | 0 | 0 | 0 |
| tests/ | 2 | 2 | 0 | 0 | 0 | 0 |
| templates/ | 5 | 4 | 0 | 1 | 0 | 0 |
| tasks/ | 4 | 3 | 0 | 1 | 0 | 0 |
| logs/ | 1 | 0 | 0 | 1 | 0 | 0 |
| deploy/ | 8 | 5 | 1 | 2 | 0 | 0 |
| .claude/ | 19 | 16 | 3 | 0 | 0 | 0 |
| config/ (ADDED) | 1 | 0 | 0 | 0 | 1 | 0 |
| plugins/ (ADDED) | 11 | 10 | 0 | 0 | 0 | 1 |
| **REPO TOTAL** | **248** | **197** | **24** | **10** | **1** | **16** |

**Reading the totals.** `LIVE` dominates (197/248, 79%) because `scripts/` — 58% of all items —
is overwhelmingly gate-wired: 124 of its 144 rows chain to a pre-commit or session-hook trigger,
mostly through `audit-health`. The 20 `UNTRIGGERED` scripts/ rows are the 2026-09-08 census's own
V+1 retirement-or-wiring list, still open. `ecosystem/`'s 15 `UNKNOWN` cells are the honest cost of
this census's own discipline: registries with no `.pre-commit-config.yaml` `files:` match among
the 29 hooks this census read by name are marked unresolved rather than guessed — a different
census with time to check every hook individually against every ecosystem file might close some of
these. `GARBAGE-CANDIDATE` fired exactly once, on `config/requirements-dev.txt` — the single
strongest, most overdetermined case this census found (sole content of a whole top-level folder,
zero source citations, 119 days stale, superseded in role by the repo's own declared `uv` chain) —
and per AX6-1 it is a proposal awaiting the operator's GO, not an action taken.

**What this manifest does not claim.** It is not a census of every file in the repo — `docs/`,
`tasks/`, `tests/`, `templates/`, and most of `ecosystem/` are itemized at the sub-domain /
named-registry grain rather than file-by-file (Method, above), so their low item counts reflect
that choice, not an absence of content in those folders.
