# [#433] schema-spike verification — K1–K5 referents, round-trip proof, viewer pilot

**Date:** 2026-07-27 · **Arc:** [#433] spike + restructure strangler STEP 1–2 (verbatim split + byte-stable round-trip), branch `feat/433-schema-spike-split`, base `feb95e18`
**Method:** module 1 recorded the K-criteria referents (§1, commit `8fba071e`); modules 2–3 built the deterministic splitter/emitter + byte-identity round-trip and the derived `tasks/` tree (§2, commits `7852904a` / `9bd0d719`, terra P1 fix `25c734f3`); module 4 piloted the Backlog.md viewer against a scratch copy of the real tree with verbatim command+output evidence (§3); this completion adds the swap-out contract (§4), the [#382] schema findings (§5), and the review lanes (§6).
**Not ruled here:** the VIEWER verdict in §3 is labelled **evidence** — the ruling stays with the restructure ADR ([#433] Done-when). BACKLOG.md remains the source of truth this arc; the `tasks/` tree is DERIVED (the flip is a later, separate arc).

---

## 1. K-criteria definitions (module 1 — the undefined-terms flag, cleared)

[#433] records: the K1–K5 validation spike is "operator's term, undefined in-repo — the spike records it first." The referents are defined here, **verbatim from the operator paste of 2026-07-27** (the arc's authorizing order):

> K1 viewer operates over/beside our files WITHOUT forcing its folder taxonomy
>    (its tree confinable to a path we choose, or absent)
> K2 [#N] identity survives byte-exact -- no task-N rewrite, no renumbering
> K3 foreign frontmatter keys (serialize-group, verified_by) survive its read
>    AND write byte-stable
> K4 works on Windows (the fleet's actual host)
> K5 read surface scriptable (JSON/CLI) consumable without importing its code

And the sixth criterion, **SCHEMA COMPOSABILITY** (provenance: operator-ratified S3d, 2026-07-26):

> a task record must be expressible as one typed row inside a declared desired-
> state model -- identity, status, dependencies surviving as fields among others
> -- without requiring its own parallel store.

**Placement disposition (recorded, not silent):** the paste directs these definitions into "[#433]'s spike scope (and docs/audits report later)" under the 1200-char ceiling, with overflow to this report. The [#433] BACKLOG entry sits at **1189/1200** doc_rot chars (11 chars of headroom) and the arc's frozen acceptance contract requires `git diff` on BACKLOG.md to be **empty** this arc — so per the paste's ceiling clause the definitions overflow **entirely** to this report, cross-linked: this section is the in-repo record; the [#433] entry's own text ("the spike records it first") is the standing forward pointer to it. No BACKLOG edit was made.

**Cross-references:** [#433] (carrier), [#382] (receiver of the schema findings per the pilot-precedes-contract ruling, `docs/decisions/README.md` "Restructure pilots the pattern before the fleet contract", operator ruling 2026-07-26, obligation 1), SUPPLEMENT `docs/handoffs/2026-07-26-dev-knowledge-architect/SUPPLEMENT.md` §2(c) (frozen bake-off criteria: `[#N]` preserved exactly · frontmatter extensible with serialize-group / verified_by / Fibonacci scoring · dependency graph · Windows · agent integration · maintenance risk · license).

## 2. Round-trip proof (modules 2–3)

**Engine:** `scripts/gen_task_tree.py` (`7852904a`, prune fix `25c734f3`) parses BACKLOG.md (201,468 bytes, pure LF, 434 lines, 172 single-line tasks) into a lossless per-line model — theme/story lineage tracked, fence-guarded, duplicate ids refused, CRLF refused — and emits `tasks/`: one `<id>-<slug>.md` per task (frontmatter: byte-exact `id: "[#N]"` + derived `status`/`priority`/`size`/`theme`/`story`/`serialize-group`/`depends-on`, the depends-on value raw and never normalized — the [#424] bare-vs-hash distinction is load-bearing) with the task's BACKLOG line **verbatim** as body, plus `manifest.json` (every non-task prose line in order + source sha256), making the source byte-identically reconstructible.

**Proofs, all witnessed green under `uv run --locked`:**

- `parse → reassemble == source` asserted **inside** `parse_backlog` (the model cannot exist un-lossless) and by `--roundtrip` on the live file.
- The core acceptance test writes the full tree to a temp dir and reassembles **from disk through the files + manifest**: byte-identical to the live BACKLOG.md (`tests/test_gen_task_tree.py::test_disk_roundtrip_tmp_tree_byte_identity`).
- The **committed** tree coherence test reassembles from the repo `tasks/` tree: byte-identical (active since `9bd0d719`; 13/13 tests green at final HEAD).
- `--check` = full regen-and-diff over every task file + manifest + disk reassembly: ok at final HEAD.
- `git diff feb95e18..HEAD -- BACKLOG.md` is **empty** (contract C).
- Independent redundancy: **12/12 Haiku spot-check probes PASS** (three parallel read-only probes, stratified ids 162/4/23/433/424/300/82/123/354/382/278/126 — every body line character-identical to its BACKLOG line, lengths matching the source exactly, e.g. [#433] 1189 chars, [#278] 1516 chars).

**Lifecycle (terra P1, fixed):** a task line leaving BACKLOG.md (ADR-65 done-items-leave) retires its derived file via the explicit `--write --prune` verb — deletion is gated on the generator's own provenance markers (`source: BACKLOG.md` + `derived: true`), so a hand-authored file is never touched; bare `--write` still never deletes. Never invoked this arc (zero deletions, contract G).

## 3. Viewer spike — Backlog.md (MrLesk), pinned `backlog.md@1.48.0`

**Install provenance:** npm, exact pin `backlog.md@1.48.0` (`npm install --save-exact backlog.md@1.48.0`), scratch prefix **outside the repo** (session scratchpad `backlog-viewer/`); binary `node_modules/.bin/backlog` → `1.48.0` on win32 (node v25.2.1 / npm 11.18.0). All probes ran in a scratch git repo seeded with a **byte-copy of the real `tasks/` tree + BACKLOG.md** (baseline-committed so every viewer write is visible in `git status`); the real repo stayed byte-clean throughout (witnessed: `git status --porcelain` empty after the spike).

| Row | Verdict | Evidence (verbatim, from the probes) |
|---|---|---|
| K1 | **FAIL** | `backlog init spike --agent-instructions none …` creates exactly one dir, footprint `?? backlog/` ("Backlog directory: backlog", `config.yml` inside) — confinable and non-sprawling — **but** `backlog task list --plain` over our root `tasks/` → `No tasks found.` (rc=0), and `backlog config list` exposes **no key** to point it at another tree (`taskPrefix: task (read-only)`). It operates only on its own `backlog/` tree in its own schema — it cannot operate *over* our files at all; "beside" is physically true but functionally blind. |
| K2 | **FAIL** | Our schema files copied INTO `backlog/tasks/` (names + `id: "[#433]"` frontmatter unchanged) → `task list --plain` still `No tasks found.` — our `[#N]` records are invisible to it. Its native create writes `task-1 - K2-probe-native-task.md` with `id: TASK-1`; the `task-` prefix is read-only config. Adopting it as the viewer would require exactly the forbidden task-N rewrite. (It never renumbered our files — but only because it never ingests them; that is the mechanism of the FAIL, not a mitigation.) |
| K3 | **FAIL** | Foreign keys `serialize-group: architecture` + `verified_by: validate_backlog` injected into its native task file, then one viewer write (`backlog task edit 1 -s "In Progress"`): the file is re-serialized from its internal model (`id/title/status/assignee/created_date/updated_date/labels/dependencies/ordinal`) and **both foreign keys are DROPPED**. Witnessed before/after file contents; the write path discards unknown frontmatter. |
| K4 | **PASS** | Installs and runs natively on Windows (the platform binary via npm optional dep); every probe in this section executed on win32; version pinned. |
| K5 | **PASS (with recorded limit)** | `--plain` machine-consumable text on list/search/single-task (`In Progress:` / `TASK-1 - K2 probe native task`); `board export` writes markdown; an MCP server (`backlog mcp`) exists as the agent surface. **No JSON output flag anywhere on the CLI** (witnessed help-sweep) — the criterion's CLI half is met without importing its code; the JSON half is absent. Any adoption must pin the un-versioned `--plain` text shape. |
| Composability (S3d) | **PASS — on our engine, not the viewer** | The pilot's task record IS one typed row: identity (`id: "[#N]"` byte-exact), status, dependencies (`depends-on` raw) as fields among others, body verbatim, no parallel store (the tree is derived from BACKLOG.md; the manifest carries the residue). The viewer cannot host that row (K2/K3), so composability is satisfied by the fleet-owned schema, viewer-independent. |

**Hazard inventory (swap-out-contract inputs):** `backlog doctor` "diagnose and safely repair duplicate task IDs" (an id-rewriting organ); `backlog cleanup` "move completed tasks to completed folder based on age" (taxonomy-forcing file moves); `autoCommit` config (false by default — witnessed zero commits; it CAN commit); `init --check-branches/--include-remote` (scans git branches, remote included by default); `--install-claude-agent` / agent-instruction writers (default-on at interactive init).

**VIEWER: REJECT — labelled as evidence, not a ruling.** As piloted against the real tree, Backlog.md@1.48.0 fails K1/K2/K3: it cannot read the fleet-owned schema in place or in its own directory, its id model is `task-N` with a read-only prefix, and its write path drops foreign frontmatter. The engine is ours either way ([#433]'s build-thin ruling); a FAIL here is the cheap, valid result the spike was designed to buy. The restructure ADR rules.

## 4. Swap-out contract (what the gate must pin; how a viewer is replaced)

1. **Version pin:** any adopted viewer is installed at an exact version (this pilot: `backlog.md@1.48.0`) in a prefix **outside the repo**; the pin is recorded in the adopting ADR and re-verified by the spike probes on every bump.
2. **Write bar:** the viewer is READ-ONLY over the derived tree. Basis: K3 witnessed — a viewer write re-serializes from its internal model and drops foreign keys. Until a viewer proves unknown-key round-trip byte-stability, its write verbs (`edit`, `doctor`, `cleanup`, `autoCommit`) are barred from `tasks/`.
3. **The gate is ours:** `gen_task_tree.py --check` (regen-and-diff + full disk reassembly) plus the byte-identity pytest suite stay the enforcement regardless of viewer — any viewer-caused byte drift on `tasks/` or BACKLOG.md REDs the gate. The schema (filename `<id>-<slug>.md`, frontmatter `id: "[#N]"` byte-exact, foreign keys legal) is fleet-owned; a viewer consumes it as-is or is not the viewer.
4. **Replacement procedure:** swap the scratch-prefix install; re-run the K1–K5 probes against a scratch copy of the real tree (the §3 method, ~30 min); record verdicts in a dated verification artifact; the engine, tests, and tree need zero changes — that independence is the point of build-thin ENGINE + replaceable VIEWER.

## 5. Schema findings owed to [#382] (pilot-ruling obligation 1)

Fed forward to the fleet desired-state contract, from one governed surface piloted end-to-end:

1. **Identity must be an opaque, byte-exact string field** (`"[#433]"`), never a normalized integer or tool-native id: the first real tool encountered (Backlog.md) has its own id grammar (`task-N`, read-only prefix) and would silently re-key the space. The contract's identity column must be declared preserve-verbatim.
2. **Unknown-key survival is a WRITE-path property and must be a contract clause:** a consumer that serializes from an internal model drops fields it doesn't know (witnessed, §3 K3). The desired-state schema needs either "consumers must round-trip unknown keys byte-stable" or "third-party writers barred" per surface — silence here is silent data loss.
3. **Typed-row composability holds on real data:** 172 heterogeneous prose rows all fit one row shape (id, status, priority?, size?, theme, story, serialize-group?, depends-on? + verbatim body) with optional fields omitted-when-absent — no parallel store needed. The S3d criterion is satisfiable by frontmatter alone.
4. **Preserve-raw beats normalize-at-ingest:** `depends-on: "270"` vs `"#270"` is live semantic signal in this repo ([#424] — the bare form is inert to the gate parser). The contract should carry values verbatim and validate in a separate lane, or migration itself becomes an undetected behavior change.
5. **Provenance markers enable safe lifecycle mechanics:** `derived: true` + `source:` in every emitted row is what made a marker-gated `--prune` safe (delete only what you provably generated). The fleet contract should standardize a provenance field pair for every derived surface.
6. **A split needs a residue carrier:** the manifest (ordering + non-member prose + source hash) is what makes one-file→many-files reversible and gateable. Any [#383] wave that decomposes a monolith surface should budget the same artifact, or reversibility is lost at step one.
7. **Directory-as-id-counter is now mechanically real** (obligation 3 evidence): with one file per id, next-free = max over tree filenames — a property of the checked-out tree, immune to the unmerged-branch invisibility class ([#427]/[#429]) once the flip lands.

## 6. Review lanes (producer ≠ reviewer)

- **Terra CODE lane** (`codex exec review -m gpt-5.6-terra --base feb95e18`, codex-cli 0.145.0; body read, not the counter): **one P1**, verbatim: *"Support pruning task files removed from BACKLOG.md — scripts/gen_task_tree.py:291-294 — When a task leaves `BACKLOG.md` (the documented normal lifecycle for done tasks), `--write` leaves its prior generated file in place and `--check` then permanently fails on it as an orphan. The README instructs users to regenerate and never hand-edit this tree, so there is currently no supported way to restore a coherent derived tree after closing a task; provide a safe, explicit pruning path or otherwise handle retired generated files."* **Disposition: FIXED at `25c734f3`** (marker-gated `--write --prune`, three pinning tests). No other findings in the body. Lane note: `codex exec review` refuses `--base` combined with a prompt — the base-only precedent form was used; review outputs are recorded here rather than as separate codex-class artifacts (deviation from the [#434] precedent, chosen to keep this arc's record in one file).
- **Terra DOC lane** over this report: findings and dispositions in §6a.
- **Haiku verbatim probes:** 12/12 PASS (§2). **Producer chain:** splitter implemented by a Sonnet lane to a frozen spec; integrated, fence-lineage-tightened, and committed by the orchestrating session; reviewed by terra. No self-review.

### 6a. Terra DOC-lane findings + dispositions

*(appended after the DOC lane ran — see the commit that completes this file)*

## 7. Live-state contradictions witnessed this arc (recorded, not smoothed)

1. **Primary HEAD swapped mid-arc (n=3 of the class):** at 14:43:25 the checkout moved `feat/433-schema-spike-split` → `main` by an actor outside this thread (reflog witnessed; the idle sibling session's transcript mtime unchanged; the Sonnet lane reports running no git commands — attribution unresolved). Repaired non-destructively: branch ref intact, checked back out, zero commit loss; every subsequent commit re-verified `HEAD` first.
2. **npm prefix resolution:** `npm install` from a bare scratch dir resolved to the HOME package.json and installed there; fully reverted (`npm uninstall`, pre-existing `puppeteer` entry left intact) and redone anchored to a scratch `package.json` (no-leftovers rule).
3. **codex CLI contract:** `codex exec review --base <sha> [PROMPT]` is mutually exclusive — the wrapper-documented prompt+diff form does not hold for the `review` subcommand at 0.145.0.
