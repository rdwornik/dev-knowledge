# ARTIFACT — CLOUD-4 v2 · universalization build (registries + decision drafts)

- **Slug:** `cloud-4v2-universalization` · **Lane:** MUTATING · **Effort:** high
- **Bound at:** `0360d6d` (detached from `refs/heads/main`), working tree clean at entry; session branch **`feat/cloud-4v2-universalization`**
- **Environment:** Anthropic cloud session, **shallow clone** (`.git/shallow` present) — the shallow guard was honoured, see §0.1
- **Cut from:** `docs/audits/2026-08-21-fresh-eyes-cloud-r2-universalization.md`. **Its §5 verdict table is the binding scope.** This lane built the two GO items and authored the two NO-GO items' decision inputs. **It executed no NO-GO item.**
- **Rules honoured:** committed on the session branch, **never merged**; no new root file; no `tasks/`, `BACKLOG.md`, `STANDING_RULINGS.md` §Q or `docs/intake/` status edits; `.pre-commit-config.yaml` untouched (its proposed entry ships as a fenced diff, §4).

---

## 0. Guards and honest limits — read before anything else

### 0.1 Shallow-clone guard: HONOURED

`.git/shallow` is present. No spine-walking instrument was run — `validate_git_backlog`, `validate_no_ff` / `block_ff_push` range scans, `journal_spine_anchor`, `check_fleet_audit_replication` and kin were all skipped. Every count below is derived from the **working tree**, never from a history walk. Where R2 quoted a count from its own bound revision, this lane **re-measured at its own** rather than inheriting the number; where the two differ the difference is stated (§1.2).

### 0.2 Terra (`/codex-review`) COULD NOT RUN — tally is honest, not blank

The brief asks for `/codex-review` on all code. **It is unavailable in this container**, verified three ways:

```
which codex            -> command not found
ls ~/.codex            -> no such directory
ls ~/.claude/commands  -> no such directory   (the user-level /codex-review command)
```

`/codex-review` is a user-level command that shells out to the `codex` CLI, pinned to `gpt-5.6-terra` in `~/.claude/bin/codex-review.ps1` — all three at **L0, outside this repository**, which is R2 §3.3's own headline finding (seam S19/S21) arriving as a lived constraint rather than a note.

**Tally: 0 findings, review NOT RUN, reason = second-reader toolchain absent from the cloud container.** No substitute is claimed to be equivalent. What *was* run, in its place, is recorded at §5: a manual adversarial re-read of this lane's own diff, which produced **4 self-caught defects, all fixed before commit**, plus the full pytest suite and `ruff` across every touched file. **The pre-merge second-reader leg is still OWED**, and this artifact is the record that it is owed rather than done.

### 0.3 What this lane deliberately did not touch

The **12 doctrine seams** and the **10 code seams** of R2 §3.2, in full (§3 lists them by id with their reasons). `tasks/`, `BACKLOG.md`, `protocols/STANDING_RULINGS.md`, `.pre-commit-config.yaml`, `.gitignore`, `docs/intake/` (read only — no status edited), `~/.claude`, `~/.codex`. No file renamed or moved. No `AGENTS.md` created. No root path added.

---

## 1. What landed

Three commits on `feat/cloud-4v2-universalization`. Two mechanisms, two decision documents.

*Commit hygiene, recorded rather than tidied away: the four self-review fixes of §5 items 3 and 4 (the frontmatter scoping and the S17 anchor) were made after the first commit and landed inside the second, whose message is otherwise about the decision documents. The diff is right; the commit boundary is not, and saying so costs less than rewriting the branch.*

### 1.1 Provider/model registry — R2 §3.3 GO (item 1)

**`ecosystem/provider-registry.yaml`** — one file, beside `tool-versions.yaml`, **mirroring its shape deliberately**: a two-collection `<collection>: <id>: <fields>` mapping (`providers:` and `models:`). That mirror *is* the library-first precedent the brief named — the repo already has an ecosystem-state shape and this does not invent a second one.

Read by **`scripts/provider_registry.py`** (loader + accessors, read-only). Non-readable sites are held in agreement by **`scripts/check_provider_registry.py`** (exit 0 clean / 1 violation / **2 internal error — an error BLOCKS**, matching the house posture of `check_seal_identity` and `validate_hermetization`).

**The honest limit, stated first because it is the shape of the whole cut:** you cannot make YAML frontmatter, a JavaScript string literal, or committed prose *read* a YAML file. What a registry buys at those sites is not indirection, it is **detection**. R2 §3.3's actual finding was that `claude-sonnet-5` sits in three formats *"with nothing asserting they agree"* — this is that assertion. A provider swap still edits N files; what changed is that it can no longer edit N−1 of them and ship.

### 1.2 Canonical-doc-name registry — R2 §1.5 GO-(b) (item 2)

**`scripts/canonical_docs.py`** — one table the ten machine constants read. **Value unchanged: `VISION.md` is still `VISION.md`.** This is plumbing, not the rename; R2 verdicts the rename NO-GO as briefed and recommends the table *"whether or not the rename ever happens"*.

Re-measured at this lane's own revision (`grep -rn "VISION\.md" --binary-files=without-match . --exclude-dir=.git`): **1,956 occurrences across 678 files**, of which **0 are markdown links** (`grep -rcE "\]\(\.?/?VISION\.md"` returns no non-zero file). R2 measured 1,924 / 672 nine days earlier — **the corpus grew, the shape did not**, and the "nothing can detect a stale canonical-doc reference" finding survives re-measurement.

### 1.3 Draft ADR — R2 §1.5 / CONFLICT-2 (item 3)

**`docs/decisions/ADR-114-readme-recreation-legality.md`** — **Status: Proposed, Decision section deliberately blank for the operator.** It prices the three costs the brief named — fleet sequencing (parity MUST ×9), the immutable-locator cost (R2 §1.4 R4/R7), and the `gen_handoff` degrade contract — and offers three selectable options, including one **the CLOUD-R2 brief did not consider** (admit `README.md` as an *additional* front door without substituting `VISION.md`, which pays measurement 1 only partially and measurements 2 and 3 not at all).

### 1.4 Intake-R1 decision packet — R2 §2.5 (item 4)

**`docs/audits/2026-08-22-technical-intake-r1-decision-packet.md`** — the four inputs R2 §2.5 names, shaped so R1 can be ruled from it alone. **No `AGENTS.md` file was created**; the intake's gate (*"Must: rule on R1 before any AGENTS.md file is created"*) is honoured.

Its load-bearing new measurement — which also closes the intake's own **open question 3** (*"nobody has measured it"*):

```
Codex 32 KiB cap (project_doc_max_bytes)              32,768 B   32.00 KiB  100.0% of cap
~/.codex/AGENTS.md  (= in-repo codex/AGENTS.md)        3,891 B    3.80 KiB   11.9% of cap
hypothetical root AGENTS.md (R2 2.3 mover set)        11,548 B   11.28 KiB   35.2% of cap
COMBINED (global + root)                              15,439 B   15.08 KiB   47.1% of cap
                                                    headroom:   17,329 B   16.92 KiB
CLAUDE.md whole file, for contrast                    40,651 B   39.70 KiB  124.1% of cap
COMBINED if CLAUDE.md were copied wholesale           44,542 B   43.50 KiB  135.9% of cap
                                              -> OVER cap by:   11,774 B   11.50 KiB
```

**R2 §2.5's refusal conditional does not fire.** It said *"If it cannot [survive the layering], R1 must refuse the root filename"*. It can, with 17 KiB to spare. **The size argument for refusal is unavailable to the ruling** — refusal, if ruled, has to rest on doctrine.

Two findings the packet adds beyond the four owed inputs: **a line budget is not a byte budget** (this repo averages ~117 B/line, so a ≤N-line ceiling does not bound what the cap measures — the R5 guard should be stated in bytes), and **the precedence chain has an unpriced third layer** — `codex/AGENTS.md` sits at an *intermediate directory inside this repo*, so a cwd at or below `codex/` yields `role → doctrine → role` and the role wins by position rather than by intent.

---

## 2. Seam ids repointed — the nine, one row each

| Seam | Site | Format | How it is now coupled to the registry |
|---|---|---|---|
| **S7** | `scripts/changelog_sentinel.py` `_TOOLS` | Python dict | **Derived** — `provider_registry.version_commands()`. A real import; the literal is gone. Fail-soft to `{}` on error, which is this hook's own stated contract (*"any error → emit nothing, exit 0"*), not a second source of truth. |
| **S8** | `ecosystem/tool-versions.yaml` | YAML | **Asserted** — tool keys and `source_url`s. The file stays the DURABLE ADR-80 §3 last-reviewed record; the registry owns the identity half. |
| **S9** | `.claude/agents/artifact-reader.md` | `.md` frontmatter | **Asserted** — `model:` key (scoped to the `---` block), plus the prose note's `Pinned to <id>` and its declared upgrade path. |
| **S10** | `.claude/workflows/conformance-hub.js` | `.js` object literal | **Asserted** — every per-stage `model: '…'` pin, all three. |
| **S11** | `.claude/workflows/conformance-hub.js` | `.js` string list | **Asserted** against `canonical_docs.CONFORMANCE_V2_SCAN` (a canonical-**doc** seam, not a model seam — checked by `tests/test_canonical_docs.py`). |
| **S17** | `protocols/PLAYBOOK.md` | `.md` prose | **Asserted** — anchored on the tier *binding* (`…tier is X (\`model-id\`)`), not on a loose backtick. A deleted binding fails loud rather than passing quietly. |
| **S26** | `.claude/settings.json` | JSON config | **Asserted** — marketplace id + the absolute host source path. A host seam, not a provider seam (R2 flags it as such); recorded because it is a hardcoded absolute path in committed config. |
| **S29** | `ecosystem/satellite-onboarding-rulings.yaml` | YAML provenance | **Asserted** — the `gpt-5.6-sol` attribution resolves to a registered model id. |
| **S30** | `pyproject.toml` | comment provenance | **Asserted** — the on-disk form is the prose token `grok L5`, not the id; the registry carries `attribution_token` for exactly this. |

**The three formats the brief named** — `.md` frontmatter (S9), `.js` object literal (S10), `.md` prose (S17) — are pinned together by one test, `tests/test_provider_registry.py::test_the_three_formats_that_hardcode_the_subagent_model_all_agree`, which names *which* of the three drifted rather than only that something did.

### The ten canonical-doc machine constants, repointed

`check_vision_md` · `check_adr38_baseline` · `check_canonical_md_visibility` · `check_canonical_structure` · `canonical_freshness_gate` · `validate_doc_rot` · `validate_doc_structure` · `validate_hermetization` · `session_end_backpressure` · `gen_handoff`

**Eight import the registry hard. Two import it SOFTLY, and that is a finding, not a shortcut.** `canonical_freshness_gate.py` and `session_end_backpressure.py` are **byte-copied into consumer repos as standalone single files** by `deploy/carrier_mesh.py` (`FRESHNESS_GATE_REL`, and the mesh's `session_end_backpressure` component). A hard import of a hub-local sibling would have **broken both consumers on the next deploy** — a defect this lane would have shipped had it not read the carrier. They therefore guard the import and keep a literal fallback, and `tests/test_canonical_docs.py` **parses each fallback out of the module source** and asserts it equals the registry, so hub-side drift reds where the file is authored instead of going silent at a consumer. Reading the live attribute would have proved nothing — at the hub the guarded import succeeds, so the attribute *is* the registry's value; only the source text shows the other branch.

`gen_handoff`'s filename and its degrade string now live **together** in the registry, because R2 §1.4 R2 prices that pair: a miss does not crash, it stamps a placeholder into a bundle that is immutable the moment it is committed.

### Out of scope, by id, with R2's reason

- **12 doctrine seams — NO-GO, untouched:** **S1** (branch-prefix enum — `CLAUDE.md` §4 says in terms that a prefix enters *"only via a recorded ruling (never silently)"*), **S12**, **S15**, **S16** (routing / t-shirt pins, operator-ruled on measured evidence), **S18**, **S19**, **S20**, **S21** (`~/.claude/ROUTING.md` — the canonical routing table, **not in this repo**), **S22**, **S23** (ADR-70's XL tier — immutable ADR, supersede never edit), **S28** (the ADR-78/93 floor), plus **S17's doctrine paragraph** (only its model *string* is asserted; the paragraph is untouched).
- **10 code seams — NO-GO, untouched:** **S2**, **S3**, **S4**, **S5**, **S13**, **S14**, **S24**, **S25**, **S27**, and **S6** in its third-provider form. Real ports, not parameterizations — and per the portability memo's own steelman, the mechanisms worth *keeping* Claude-specific.

---

## 3. Fenced diffs

### 3.1 Proposed `.pre-commit-config.yaml` entry — NOT APPLIED

The brief reserves `.pre-commit-config.yaml`; this ships as a proposal for the integrator, exactly as `[#539]` did. The registry's coupling is **already enforced by pytest today** — this entry moves it to commit time, where a drifted pin is refused rather than reported.

```diff
--- a/.pre-commit-config.yaml
+++ b/.pre-commit-config.yaml
@@
       - id: validate-backlog
         name: Validate BACKLOG.md story-map (ADR-66)
         entry: uv run --locked python scripts/validate_backlog.py
         language: system
         files: '^BACKLOG\.md$'
         pass_filenames: false
+      - id: provider-registry-agreement
+        name: Provider/model registry agreement gate (CLOUD-4 v2; HUB-ONLY)
+        # ecosystem/provider-registry.yaml is the declared home for every provider, CLI
+        # and model string on the live surface (R2 section 3.3). Sites that can read YAML
+        # read it; the rest -- .md frontmatter, a .js object literal, a JSON config,
+        # committed prose -- are held in agreement by this checker. Fires only when one of
+        # the checked files (or the registry itself) is staged, so it costs nothing on an
+        # unrelated commit. Exit: 0 clean, 1 violation, 2 internal error (an error BLOCKS,
+        # never silently passes). HUB-ONLY. Bypass: --no-verify.
+        #
+        # HONEST LIMIT, the checker's own: it asserts that the sites AGREE with the
+        # registry. It cannot make frontmatter or a JS literal READ the registry, and it
+        # says nothing about whether the pinned model is the RIGHT one -- routing is ruled
+        # doctrine and its canonical table (~/.claude/ROUTING.md) is not in this repo.
+        entry: uv run --locked python scripts/check_provider_registry.py
+        language: system
+        files: '^(ecosystem/(provider-registry|tool-versions|satellite-onboarding-rulings)\.yaml|\.claude/(settings\.json|agents/artifact-reader\.md|workflows/conformance-hub\.js)|protocols/PLAYBOOK\.md|pyproject\.toml)$'
+        pass_filenames: false
       - id: audit-health
```

**Roster row owed to the integrator** (the `[#539]` / batch-4 W5 precedent — a lane's footprint stays out of the freshness-gated `CLAUDE.md`, and the debt is paid at the merge where the gate is actually live), for `CLAUDE.md` §9's pre-commit roster:

```
- `provider-registry-agreement` (CLOUD-4 v2, HUB-ONLY) — agreement gate for the nine
  table-edit provider/model seams (R2 §3.2) against `ecosystem/provider-registry.yaml`:
  the `.md` frontmatter pin (S9), the `.js` object-literal pins (S10), the `.md` prose
  tier binding (S17), the JSON marketplace host path (S26), the durable tool-versions
  identity half (S8) and the two provenance attributions (S29/S30). `scripts/
  check_provider_registry.py`, exit 0/1/2 (an error BLOCKS), bypass `--no-verify`.
  **Honest limit, the module's own:** it asserts AGREEMENT, not correctness — frontmatter
  and a JS literal cannot read a YAML file, so the coupling is detection, and nothing here
  says the pinned model is the right one (routing is doctrine, and its canonical table
  `~/.claude/ROUTING.md` is at L0 outside this repo — R2 seam S21).
```

### 3.2 No other reserved-surface diff is owed

`.gitignore`, `deploy/manifest-v*.yaml`, `BACKLOG.md`, `tasks/`, `STANDING_RULINGS.md` and `docs/intake/` are all unchanged, and none of this lane's work requires an edit to them. In particular **no deploy-manifest change is owed**: the two carried modules were deliberately given literal fallbacks precisely so the carrier keeps working byte-for-byte as it does today.

---

## 4. Verification

| Check | Result |
|---|---|
| `python scripts/check_provider_registry.py` | exit **0** — clean on the live tree |
| `python scripts/validate_hermetization.py` | exit **0** |
| `python scripts/validate_doc_structure.py --all` | exit **0** |
| `python scripts/changelog_sentinel.py` | exit 0, nudge emitted, `_TOOLS` derived from the registry (verified live) |
| `ruff check` on every touched file | **All checks passed** |
| `pytest tests/test_provider_registry.py tests/test_canonical_docs.py` | **39 passed** |
| `python scripts/silent_rule_detector.py` | **440** vs baseline **441** — no raise (the new `ecosystem/*.yaml` carries zero `must/shall/never` tokens by construction) |
| `gen_audit_index --check` · `gen_claude_rosters --check` | exit **0** after regeneration |
| `ecosystem/doc-counts.md` | regenerated — tests 3,372 → **3,411** (+39); audit checks 43 and pre-commit gates 20 both unchanged, this lane arms neither |
| Full `pytest` suite | see §4.1 |

### 4.1 The full suite, and the environmental baseline

**The baseline is not green in this container, and it was not green before this lane touched anything.** Measured on the pristine tree at entry (`0360d6d`):

```
BEFORE   44 failed · 3,288 passed · 39 skipped · 1 xfailed   (3,372 collected)
AFTER    44 failed · 3,327 passed · 39 skipped · 1 xfailed   (3,411 collected)
                     +39 = exactly this lane's new tests
```

The 44 are environmental, not defects — no consumer repos are cloned (`expected >=1 registered consumer`), pre-commit hooks are not armed (`hooks-armed WARN-undeclared`), `pandas` and the language server are absent, `.git/shallow` breaks the history probes, and the shallow clone's commit dates make `canonical_freshness` A2 fire on four canonical docs nobody has edited since review.

**The root cause of the unarmed hooks, recorded because the next cloud lane will hit it in its first five minutes: this container ships `uv 0.8.17` and `pyproject.toml:25` pins `[tool.uv] required-version = "==0.11.19"`.** Every command of the form `uv run --locked …` therefore refuses before doing anything — which is *every* `.pre-commit-config.yaml` entry, `scripts/audit.py health`, and the `session_end_backpressure` Stop hook. So the hooks are not merely unarmed, they are **unarmable here**, and the `hooks-armed` WARN is a symptom rather than an oversight. **Workaround used throughout this lane, and it is a workaround rather than a fix:** every command was run as bare `python …` with dependencies installed via `pip`, and each gate was invoked directly (`python scripts/validate_hermetization.py`, `python scripts/check_provider_registry.py`, `python scripts/silent_rule_detector.py`, `python scripts/gen_*.py --check`) rather than through pre-commit. Run that way the Stop hook exits **0 with no advisories**. **Not fixed here on purpose:** moving the pin is a fleet toolchain decision touching `uv.lock` and `.python-version` (ADR-106 env), which is a doctrine surface this lane is scoped out of. Individually spot-checked as pre-existing by `git stash`-ing this lane's diff and re-running the same test — including `test_routine_consumers_live_backlog_governs_exactly_one_row`, which fails identically on the untouched tree.

**The arithmetic is the load-bearing evidence, and it is what caught the regression.** An intermediate run reported **60 failed / 3,311 passed**: +16 failures against +23 passes, summing to exactly the 39 tests added. That +16 was not noise — it was the `test_assemble_paste` breakage of §5, and the totals are what made it undeniable in a container whose baseline is already red. It was fixed, and the counts above are the post-fix run.

**Consequence for the reader, stated rather than buried:** *"pytest green"* is **not** claimable in this container in the absolute sense, and this artifact does not claim it. What is claimed, and verified twice, is **no regression** — same failure count, same failure set, +39 passes.

---

## 5. Second-reader tally, and what this lane caught on itself

`/codex-review` (terra) **NOT RUN** — §0.2. In its place, a manual adversarial re-read of the lane's own diff, before commit, asking only *"what would a reviewer reject?"*. It found four real defects:

1. **The deploy-carrier break (the serious one).** The first draft hard-imported `scripts/canonical_docs.py` from `canonical_freshness_gate.py` and `session_end_backpressure.py`. Both are **byte-copied into consumers as standalone single files**; the change would have broken every consumer on the next deploy, silently and at a distance. Caught by reading `deploy/carrier_mesh.py` rather than by any test — no test in this repo covers a consumer's post-deploy import. Fixed with guarded imports plus source-parsed fallback assertions.
2. **A vacuous fallback test.** The first fallback test compared the *live attribute* to the registry — but at the hub the guarded import succeeds, so it compared the registry to itself and would have passed against any fallback whatsoever. Fixed by parsing the `else:` branch out of the module source with `ast`, and pinned by a test that proves the parser itself has teeth.
3. **An over-broad frontmatter regex.** `^model:\s*(\S+)$` was applied to the whole of `artifact-reader.md`, so a `model:` line anywhere in the body could have satisfied or broken the pin. Scoped to the leading `---` block; a regression test adds a body-level `model:` line and requires the checker to stay clean.
4. **A prose check that could not fail usefully.** S17 originally asserted only that the backticked id appeared *somewhere* in a 4,500-line PLAYBOOK. Deleting the tier-binding sentence entirely would have passed. Re-anchored on the binding itself, with a test that deletes the sentence and requires a `was not found` finding.

**A fifth defect was caught by the SUITE, not by the review — and that is the honest ordering.** `tests/test_assemble_paste.py` copies `scripts/gen_handoff.py` into a tmp `scripts/` dir and runs it as a subprocess; its own fixture comment already said *"its sibling must sit beside it"*. `gen_handoff`'s new registry import made the sibling set two deep, and **16 tests went red** — the same defect class as item 1 (a module copied out of `scripts/` and run standalone), at a site the carrier read did not cover because the copier here is a test, not `deploy/`. Fixed by copying `canonical_docs.py` alongside, **not** by giving `gen_handoff` a fallback: that module is precisely the site R2 §1.4 R2 prices as the silent-failure one, so its filename and degrade string are deliberately allowed exactly one home.

**The lesson, stated because it generalises past this lane:** the repo has **two** independent mechanisms that copy a script out of `scripts/` and run it beside a partial sibling set — `deploy/carrier_mesh.py` and this test fixture — and neither is discoverable from the module being edited. Any future "read it from one table" repoint has to check both. The review caught the first; only the suite caught the second.

**This is not a substitute for the second-reader leg and is not offered as one.** It is one author re-reading their own work, which is exactly the sycophantic-convergence failure mode `[#82]`'s own design input names. **The `/codex-review` pass remains OWED before merge.**

---

## 6. The two operator decisions, restated

R2 named two questions that a lane cannot answer and that this lane has therefore preserved rather than resolved. Both are restated here because R2 §3.3's own instruction was *"the one thing CLOUD-4 must record even if it does nothing else"*.

### 6.1 The L0 boundary — DECISION OWED

**`~/.claude/ROUTING.md` is the canonical model-routing table and it is not in this repository.** Neither is the reviewer pin (`~/.claude/bin/codex-review.ps1`, seam S19) nor the Codex config (`~/.codex/config.toml`, seam S20). PLAYBOOK Appendix B killed the resident routing copy deliberately (#158 Decision B) to prevent drift — correct for drift, **fatal for a table-driven swap, because the table a provider swap would edit is not a file this repo owns.**

**This lane lived that finding rather than merely restating it:** §0.2's terra failure is the same fact, arriving as an inability to run the review the brief asked for.

The honest options, unchanged from R2 and still the architect's to pick:

- **(a)** bring a copy in-repo with a drift gate — reversing #158 Decision B for a stated reason. The repo already runs regen-and-diff seven times over, so the mechanism exists.
- **(b)** state explicitly in `ARCHITECTURE.md` Ch3 that routing is an L0 concern and out of the repo's universalization scope.

**Either is fine; silence is not.** And the decision has a downstream consumer: `[#82]`'s Done-when requires each fleet member to carry a review profile *"at its stated home"*. If the reviewer pin lives at L0, then either the home is L0 — and **[#82] is partly unverifiable from this repo by construction, which belongs in the row rather than being discovered at closure** — or the pin comes in-repo. **Decide before the schema, not after.**

The registry landed by this lane deliberately does **not** pre-empt this: `ecosystem/provider-registry.yaml` records model **identity**, and says so in its own header. It carries no routing table.

### 6.2 The `VISION.md` rename — PARKED, priced, not executed

**Parked.** ADR-114 is **Proposed with a blank Decision**, and nothing in this repo was renamed or moved. The three costs are now measured rather than estimated (fleet MUST ×9 across the ADR-104 members; 104 of 114 immutable handoff bundles and 69 `PROBES` files carrying a locator that can never be corrected; the `gen_handoff` degrade contract that stamps a placeholder into an immutable artifact without erroring), and a fourth is named that R2 did not price: **the `## Vision` H2 spine is a second, independent migration surface** replicated across five deploy manifests, so filename and spine are two decisions and ADR-114 prices only the first.

**What changed while the decision stays open:** the ten machine constants now read one table, so the *code* half of a future substitution is close to free, and the `gen_handoff` name/degrade pair can no longer move apart. **That was worth landing on its own merits** — which is precisely why R2 recommended it *"whether or not the rename ever happens"*.

---

## 7. Residual — what the next lane inherits

1. **The `/codex-review` second-reader pass on this lane's code.** OWED. §0.2 / §5.
2. **The `provider-registry-agreement` pre-commit entry + its `CLAUDE.md` §9 roster row.** Proposed as fenced diffs (§3.1); neither applied, both owed to the integrator at merge.
3. **R1 needs ruling** before any `AGENTS.md` work. The packet is complete (§1.4) and its finding narrows the ruling: the size objection is unavailable, so the ruling is about doctrine.
4. **ADR-114 needs ruling** — (A) refuse / (B) admit without substituting / (C) substitute. Option (B) is the one the original brief never considered and the cheapest by a wide margin.
5. **The L0-boundary decision** (§6.1) gates `[#82]`, not this lane.
6. **The missing detector R2 §1.5(c) recommends** — a `doc_claims`-family check asserting every canonical-doc token in the *live* corpus resolves to a tracked path — is **not built**. With 0 of 1,956 references being links, nothing today can tell you a canonical-doc reference has gone stale. Out of this lane's scope; still the right next mechanism.

---

*MUTATING lane. Mutation footprint: the four new files named in §1, the eleven repointed modules, two new test modules, and the regenerated indexes. Committed to `feat/cloud-4v2-universalization`; **no merge, no push to `main`, no file moved, no root path added.** Every measurement above is reproducible at the bound revision with the commands quoted inline.*
