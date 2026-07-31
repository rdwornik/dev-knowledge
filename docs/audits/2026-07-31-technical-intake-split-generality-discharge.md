# Intake split — ADR-109 §4 generality discharge ([#383] wave 1)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-31 · **Slug:** intake-split-generality-discharge
- **Serves:** the durable evidence record for [#383] wave 1 — the committed round-trip proof
  that discharges ADR-109 §4's generality clause on the second governed surface,
  `docs/intake/`. Branch `feat/intake-split-generality-discharge`, cut from `f2ccda9a`.
- **Inputs:** `docs/decisions/ADR-109-fleet-desired-state-contract-v1.md` §4 (the obligation) ·
  `docs/decisions/ADR-107-*.md` §6.2 (its source) · `scripts/gen_task_tree.py` (surface 1, the
  engine pattern) · the operator's ex-ante frozen acceptance contract for this wave.
- **Authority:** the acceptance contract and the two architect rulings transcribed in §1 are
  the operator's/architect's, immutable to this arc; this record transcribes them and cites
  where each landed. Immutable record (CLAUDE.md §5 rule 3) — supersede, never edit.

## 1. Architect rulings this wave executed under

| # | Ruling | Where it landed |
|---|---|---|
| R1 | **Monolith = `docs/intake/README.md`**, accepted *with* the honest limit stated. §4's bar is byte-exact round-trip + residue manifest, **not a derivation ratio**. The inverted ratio must be recorded explicitly in the manifest header **and** the §4 amendment. Per-intake-file round-trip **rejected** — it inverts the engine pattern (items become the projection rather than the regenerated artifact). | `manifest.json` `honest_limit` block · ADR-109 §4 amendment "The honest limit this discharge is stated with" |
| R2 | **Split only — no flip.** §4 requires the round-trip proof, not a source-of-truth flip; [#439] was a later separate decision, and flipping intake changes `docs/intake/` governance semantics. **File a candidate row instead of building it.** | `gen_intake_tree.py` module docstring (direction: `derived-from`) · BACKLOG **[#466]** |
| R3 | **Verification loop vs [#457] standing REDs.** Two tests are RED and **UNMARKED** by standing operator ruling — no skip, no xfail, no deselect. The step gate is "no NEW failures beyond the two known ids": run without `-x`, compare the failure set. | §5 below; every suite run in this arc reported against that pair |
| R4 | AC-6 discharge via an **appended amendment marker** (ADR-94 / `ADR-107:436` precedent), dated with the **actual landing date at commit time**, not a pre-written stamp. | ADR-109 `## Amendment — 2026-07-31` |

## 2. AC-1 — §4 fidelity check (performed before planning)

§4 was pulled from the live ADR and diffed against its ADR-107 §6.2 source. **Faithful on all
four discharge legs; no mismatch, so no STOP was triggered.** Two cosmetic deltas recorded for
honesty: ADR-107 reads "and **already carrying** a generated status-grouped index" (§4
compresses to "and a"); and §4 omits §6.2's trailing sentence that the obligation "is **NOT** a
precondition of the §7 flip … but it **is** a precondition of [#382] declaring the fleet
contract *general*." Neither alters a discharge leg.

## 3. §H builder-lane evidence — who wrote what, and the verification outcome

**Producer lane.** `codex exec -m gpt-5.6-terra --sandbox read-only`, spec = AC-3/AC-5 verbatim.
Codex was directed to emit to **stdout only**: the global `codex/AGENTS.md` declares Codex a
read-only reviewer that must not modify files, so authorship was preserved without granting
write access. Codex produced (a) the `--check` regen-and-diff leg and (b) the
`check_intake_tree_coherence` audit wrapper.

**Verification outcome: NOT accepted as written — two defects found and corrected by CC.**

| # | Severity | Defect | Evidence | Disposition |
|---|---|---|---|---|
| D1 | **Fleet-breaking** | The audit wrapper keyed "adopted" off **`docs/intake/` existing**, returning FAIL when the folder was present without a carrier. `corp-monorepo` (4 intake docs) and `ai-council` (9) both carry `docs/intake/` and **no** `manifest.json` — the carrier is hub machinery never distributed. The leg would have reported FAIL on two consumer repos and manufactured a fleet gap that does not exist. | `ls docs/intake` + `test -f manifest.json` across the 4 consumer repos | **Repredicated on repo identity** (`repo_path != _REPO_ROOT → n/a`), matching the `check_task_tree_coherence` precedent. Verified: hub `pass`, corp-monorepo / ai-council / win-tooling all `n/a`. Regression-pinned by `test_audit_leg_is_hub_only_and_na_off_hub`. |
| D2 | Minor | Import alias `_git` **collides** with the existing git-subprocess helper `audit.py:2629`, shadowing it (`AttributeError: 'function' object has no attribute 'evaluate'`). | live import + `grep -n "_git\b" scripts/audit.py` | Renamed `_gint`. |

**CC-initiated refactor beyond defect repair.** Codex's shape duplicated the four legs across
the CLI and the audit wrapper — the duplication class this repo gates against, and drift-prone
(a fifth leg added to one and not the other). CC extracted `gen_intake_tree.evaluate()` as the
single definition, consumed by both. Behaviour re-witnessed identical after the refactor.

**Division of authorship, stated plainly:** Codex authored the leg logic and the exit contract;
CC authored the split engine (`parse_readme` / `Model` / `build_manifest`), corrected D1+D2,
performed the `evaluate()` extraction, and wrote the tests. Codex wrote no file.

## 4. AC-5 — RED witnessed before GREEN

Run on a quiet tree (no concurrent commit — [#458]).

| Mode | Command | Result |
|---|---|---|
| Residue drift | perturb one doctrine line, do **not** regenerate | **exit 1** — all three drift legs fired; round-trip pinpointed **line 52** (the edited line); manifest-stale and `source_sha256` legs both named |
| Missing carrier | remove `manifest.json` | **exit 2** — "manifest.json is missing", remedy named |
| Regenerated | `--write` then `--check` | **exit 0** — `256 node(s), 14465 README.md byte(s)` |
| Round-trip | `--roundtrip` | **exit 0** — 14465 bytes (14207 chars) reassembled byte-exactly |
| Existing hook unbroken | `gen_intake_index.py --check` | **exit 0** |

README.md was restored byte-exactly after the perturbation (confirmed clean in `git status`),
and the regenerated manifest is identical to the pre-perturbation one.

## 5. R3 verification-loop record — the [#457] pair

The two standing REDs, named once as R3 requires:

- `tests/test_audit.py::test_check_fleet_parity_green_on_live_repo`
- `tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row`

Neither was skipped, xfailed, or deselected. Full-suite runs, `-n auto`, no `-x`:

| Point | Result | Delta vs the known pair |
|---|---|---|
| Baseline (branch cut) | 2 failed, 2070 passed, 3 skipped | **none** — gate green |
| After the leg landed | **4 failed**, 2089 passed | **+2 NEW → RED for the step** |
| After repin | 2 failed, 2091 passed, 3 skipped | **none** — gate green |

The two new failures were `test_reverse_dep_oracle.py::test_position_points_at_name_not_keyword`
and `::test_finding_headline_resolves_with_provenance` — the known **`audit.py` line-shift
class**: the new import block sits above `class Finding:`, moving it **297 → 304**. Repinned at
3 sites (2 live assertions + 1 negative-membership pin). This is a real instance of the
"line pins above `class Finding:` drift" pattern; the pins were re-grepped, not remembered.

## 6. What the discharge does and does not show

**Shows:** the engine pattern extends to a second governed surface — per-item frontmattered
files, a residue manifest in the ADR-107 §5 finding-6 shape, byte-exact identity, and a green
regen-and-diff round-trip armed as a standing ship-gate leg (`ALL_CHECKS` 35 → 36).

**Does not show, named not claimed away:**

1. **The ratio is inverted** — 18 item-derived lines / 238 residue / 256 total. Surface 1's was
   the reverse. §4's bar is not a ratio, so this discharges; but the proof exercises less of
   the item corpus than surface 1's did (R1 required this be recorded, not glossed).
2. **Intake bodies are outside the round-trip** — the split projects only `intake-id`,
   `status`, and the `# ` title. Enumerated in the manifest's `not_captured`, deliberately
   **not hashed**: hashing would couple the carrier to every body edit and RED the gate on
   unrelated work, buying no round-trip strength.
3. **Split-only, not flipped** — README.md remains the hand-authored source of truth ([#466]).
4. **Nothing is claimed about surfaces beyond the two now shown** — notably the `[E8]`
   ruling/decision register, §4's other named candidate, which this wave did not touch.

## 7. Incidental observation (not fixed — out of scope)

`python scripts/audit.py checks` raises `UnicodeEncodeError: 'charmap' codec can't encode
character '→'` on a cp1252 console. **Verified pre-existing** — reproduced with this
arc's `audit.py` changes stashed. Not this wave's defect and not repaired here (minimal
diffs); recorded so the next session does not re-diagnose it. The check *count* was verified
by import instead. Same family as the gotchas-skill entry that motivated this wave's
ASCII-only output discipline.
