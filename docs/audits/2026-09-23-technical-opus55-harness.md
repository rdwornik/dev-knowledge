# DIGEST — S1: Copilot at work / tool changes / Opus 5.5

> **Status:** landed verbatim by `lane-landing-window` (LANE-5A-5) from the transport, where it
> was `carried-by: OPEN` with no repo citation. Source:
> `to-browser/DIGEST-OPUS55-HARNESS-2026-09-23.md`. Part A's finding is corrected/superseded by
> `AMEND-WINDOW-DEFECTS-2026-09-23.md` D30-D31 (landed as
> `2026-09-23-technical-window-defects-amend.md`): the Copilot admission trace and the
> Opus-alias-vs-pin gap became provenance for D30/D31 rather than open questions.
> Carrier rows: D30, D31 (`to-cc/AMEND-WINDOW-DEFECTS-2026-09-23.md`); D34
> (`to-cc/DECLARE-WINDOW-DEFECTS-2026-09-23.md`), filed by `lane-landing-window`.

carried-by: OPEN
lands-via: operator triage of Part A's blocker, and #105 (Part B ADOPT findings)
date: 2026-09-23
from: postwave-changelog (Sonnet 5, background session, S1 of POSTWAVE-CHAIN-2026-09-22)

## Part A — Copilot as producer: BLOCKED, not executed

```
rows_selected: 0
reason: blocked before selection was reached
```

**Blocker.** `ecosystem/provider-registry.yaml` (current HEAD, clean tree) lists `copilot-enterprise`
on the `implement` role with `admission: verdict: unevaluated`, annotated in the file itself: *"NOT
ADMITTED and NOT LICENCE-CLEARED — two independent blocks."* AX22-1 is coded there too: *"Implement
order until admission: Sonnet first."* `scripts/provider_router.py` refuses a non-admitted provider
in a producing role — this is an enforced technical gate, not a stale comment.

**The claimed admission doesn't trace.** `to-cc/RATIFICATION-2026-09-23-copilot.md` states Copilot
was *"admitted and measured on 2026-09-17 as a bounded producer (3/3 correct, 0.46 AI credits, 14s)
and produced two lanes that day."* I searched `JOURNAL.md`, `docs/audits/`, and git log for
2026-09-17 for this event. The only 2026-09-17 JOURNAL entry mentioning "copilot" is lane `ab-832`:
*"the three-repo comparison re-run for **copilot-collections** only"* — a repo-name comparison
target, unrelated to the GitHub Copilot Enterprise CLI as a code producer. No commit, audit, or
registry change reflects a 2026-09-17 admission of Copilot as a producer anywhere in this repo.

**Even the RATIFICATION agrees this isn't landed yet.** Its own header: `lands-via: the next
window's landing step (STANDING_RULINGS) and the launcher-routing row` — the operator's licence
ruling (O-3) exists on the transport, but the registry/router that actually gates routing has not
been updated to reflect it.

**Action taken: none.** Per this task's own instruction ("Use that admitted invocation; do not
invent flags") — there is no admitted invocation to use, so none was invented. I did not create a
worktree for Copilot, did not invoke the `copilot` CLI, and did not spend the Copilot budget.
Separately from the in-repo gate: `copilot-enterprise` bills to an employer-provisioned enterprise
org seat (`BY-Product-Development`); spending it on unlanded/untraceable authorization is not a call
I'll make unilaterally from a background session.

**Recommendation.** Before Part A can run for real: either (a) locate and land the actual
2026-09-17 admission evidence into `ecosystem/provider-registry.yaml` with a `decided_by` /
`decided_on` / `evidence` entry — matching the pattern already used for the `anthropic`/`implement`
row (2026-09-11, `docs/audits/2026-09-11-technical-batch-x-manifest.md`) — or (b) re-run the
admission measurement fresh, since the original isn't traceable in-repo. This is exactly the kind
of gap S3's "operator requests with no row" section should also name.

## Part B — `/changelog-review`

Full digest: `docs/audits/2026-09-23-changelog-review.md` (committed, branch
`worktree-postwave-changelog`). Headline: **77 claude-code versions** reviewed (2.1.205→2.1.281;
last review was 2026-07-09 — a 2.5-month gap matching the same "standing request went unactioned"
pattern the Copilot RATIFICATION names) plus **~30 codex stable releases** (0.144.0→0.156.1).

- **3 ADOPT**, filed to `docs/intake/2026-09-23-changelog-review-seeds.md` (intake-id **105**):
  - `/skill-doctor` (2.1.261) — shows unused skills and their context cost.
  - `/doctor`'s new CLAUDE.md-trim proposal (2.1.206) — a native second opinion on this repo's own
    byte-budget doctrine (`CLAUDE.md` ≤24,576 B, ADR-53).
  - `omitClaudeMd` agent frontmatter (2.1.271-range) — lets a bounded subagent/producer skip
    loading this repo's (large, by-design) governance `CLAUDE.md`; ties directly to the
    Copilot-offload intake line and to Part A's blocked producer pattern above.
- **0 OBSOLETES-WORKAROUND. 0 STALE-NAMES** — two near-misses checked against live repo files and
  ruled out (`TaskOutput` tool removal, `codex exec --full-auto` removal — neither is referenced
  outside immutable historical audits).
- **3 VERIFY** (none blocking): Task/Todo tools' model-gating vs. our live Sonnet-5/Opus-5.5
  sessions; Monitor's removed `persistent` option; and a worktree-isolation Bash false positive
  (`curl ... -o file 2>&1`) this very session hit live, which isn't one of the range's documented
  fixed shapes — candidate for a fresh gotcha if it reproduces on 2.1.281.
- Codex: all ~30 stable releases are NOISE for our narrow non-interactive `codex exec` reviewer
  usage (dominated by its "Guardian" auto-review subsystem, a new voice mode/TUI, Windows sandbox
  hardening).

State bumped: `ecosystem/tool-versions.yaml` claude-code → 2.1.281, codex → 0.156.1. Committed
`66a616a9` on `worktree-postwave-changelog`, all pre-commit gates passed, pushed to origin.

**HANDBACK.** Branch `worktree-postwave-changelog` @ `66a616a9`, 5 files (2 new: the digest +
SEED doc; 3 changed: `docs/intake/README.md`, `docs/intake/manifest.json` regenerated,
`ecosystem/tool-versions.yaml` state bump). Ahead of `origin/main` by one commit, no conflicts
expected. Next integrator: `--no-ff` merge, push, delete the branch (MERGE IS ATOMIC).

## Part C — Claude Opus 5.5: what changed per harness role

**What changed.** Claude Code 2.1.280 adds Opus 5.5 (`claude-opus-5-5`), now the *default* Opus
model: **1M context, $4/$20 per Mtok, $0.20/Mtok cache reads.** That is cheaper and larger-context
than the Opus generation this repo currently has admitted and pinned
(`claude-opus-4-8`, `ecosystem/provider-registry.yaml`, admitted 2026-09-11).

**Per role:**
- **orchestrate / plan** — both pinned Opus-only and explicitly `rerankable: false` (AX21-1: *"a
  cheap model scoring well on pass-rate-per-cost stays out of the seat that decides what the
  expensive ones do"*). A model swap here is **not automatic** by design — that non-rerankable
  clause exists specifically to keep this off the automatic reranker path. Moving to Opus 5.5
  needs a fresh admission entry (operator ruling + evidence audit), the same ceremony
  `claude-opus-4-8` went through on 2026-09-11. **Candidate win, unearned:** if quality holds,
  the architect/orchestrator seat gets cheaper per token and can hold more batch-state before
  compaction — but "if" is exactly what an admission measurement is for.
- **implement / producer** — unaffected. Sonnet remains first per AX22-1 pending Copilot/Grok
  admission (see Part A); Opus 5.5 isn't in this role's fallback chain, and nothing here proposes
  adding it.
- **reviewer** — unaffected. Codex terra stays the adversarial reviewer specifically because it
  must never be the producing model; an Opus-generation bump on the Anthropic side doesn't touch
  that constraint.
- **reader** (Sonnet/Haiku for lookups, per this chain's own S3 preamble) — unaffected.

**A/B design (proposed only — not run, no routing change made).** Reuse the evidence pattern
`docs/audits/2026-09-11-technical-batch-x-manifest.md` already established: take a small set of
real recent orchestrate/plan-role artifacts (a batch manifest, a lane contract) as fixed inputs,
produce each once on `claude-opus-4-8` and once on `claude-opus-5-5`, score both against the
architect's existing rubric (did it pass ship-gate, did it need rework), and price both legs from
`cost_usage_telemetry.py`/`lane_cost.py`'s per-model rate table — which needs an Opus 5.5 rate row
added to `ecosystem/provider-registry.yaml` first, since it isn't there yet. The decision to move
orchestrate/plan to Opus 5.5 stays an explicit operator ruling on that A/B's result.

DONE 2026-09-23T20:02Z
