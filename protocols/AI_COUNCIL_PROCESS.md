---
last_reviewed: 2026-07-29
status: active
owner: Rob
---

# AI_COUNCIL_PROCESS v2.2

<!-- version: 2.2 — 2026-07-29 (post-flip stale-procedure fix: Stage 6 BACKLOG follow-up routed through the Tier-1 closure loop + `tasks/` retirement, ADR-107 step 3) -->
<!-- version: 2.1 — 2026-07-23 (ADR-43 amendment: routed-mirror retired — transcripts canonical-only in ai-council/output/; synthesizer default gemini→openai per 2026-07-18 ruling) -->
<!-- version: 2.0 — 2026-06-01 (ADR-67: gated loop + /council-question trigger + deterministic ADR return) -->
<!-- version: 1.0 — 2026-05-28 (initial; companion to ARCHITECTURE.md C3 AI Council pipeline diagram) -->
<!-- scope: meta -->

Version: 2.2
Effective: 2026-07-29
Authority: ADR-67 (process operationalization — gated loop, this amendment); ADR-43 (cross-project transcript routing; routed-mirror clause RETIRED by amendment 2026-07-23 — transcripts are canonical-only in `ai-council/output/`); ADR-60 (folder taxonomy, ephemeral briefs); ADR-03 (blind voting); ADR-08 (research degradation exit code); council-question-guide.md (question format)

> **Authoritative sources.** Question format: `ai-council/docs/council-question-guide.md`.
> Routing semantics: `docs/decisions/ADR-43_cross_project_transcript_routing.md`.
> Live flow: `ai-council/src/ai_council/{cli,inbox,orchestrator,routing,synthesis}.py`.
> Visual: `ARCHITECTURE.md` § Processes → "AI Council debate pipeline".
> This protocol is the prose operational counterpart of that diagram. If
> diagram and prose disagree, both are wrong — both are grounded in the same
> code; fix whichever drifted.

---

## Purpose

End-to-end operational lifecycle of a Council debate: from drafting a brief, to
running the CLI, to the transcript, to the ADR that records the binding
decision, to BACKLOG follow-up. Closes the "Option B" runbook gap left open
after ADR-60 fixed *where* artifacts live but not *who does what when*.

The pipeline has six stages. Each stage names its inputs, outputs, gate
checks, and the file or code path that grounds it.

---

## When to convene Council

Per `PLAYBOOK.md` § "Council debate threshold" and § "When to run Council vs
single-model + critic": Council is justified when ALL of these apply —

- **Architectural impact** — module boundaries, layer taxonomy, dependencies, data model
- **Multi-ADR ripple** — touches 2+ existing ADRs or creates a new binding constraint
- **Reversal cost > 1 hour** — backing out the decision means meaningful rework

For everything else (single-file edits, mechanical refactors, library choices
with well-known answers, decisions reversible in minutes), use the
single-model + critic loop instead. Council overhead (~$0.50, ~5 min,
operator attention) is wasted on non-ADR decisions.

Hard cap: **max 2 Council debates before implementation starts**. More than
that is procrastination, not deliberation (PLAYBOOK §5).

---

## Gated loop (ADR-67)

Six deterministic steps — the same pattern as `HANDOFF_PROCESS`. Each step
has a named owner and a gate; a step must pass its gate before the next
starts.

| Step | Name | Owner | Gate |
|------|------|-------|------|
| 1 | **Frame** | operator | one-sentence problem statement; two questions = split |
| 2 | **Generate** | Claude Code | fills Council-question template via `/council-question` |
| 3 | **Gate** | Claude Code | template sections present; exactly one decision; ADR context attached; fail → fix |
| 4 | **Run** | Claude Code / operator | `council --inbox`; transcript written to `ai-council/output/` |
| 5 | **Verdict → ADR** | Claude Code | ADR drafted in target repo; `docs/decisions/README.md` updated |
| 6 | **Deterministic return** | Claude Code | ADR written to `council.return_dir` (see Stage 6); no relocation guesswork |

**Trigger:** `/council-question` — Claude Code generates and self-gates the
question (Steps 2–3). Operator reviews, then drops into the inbox (Step 4).

**Cross-domain split (three-domain separation):**

| Piece | Domain | Status |
|-------|--------|--------|
| This process spec + ADR-67 | `.dev-knowledge` | Implemented |
| Council-question template + gate check + known-path I/O | `ai-council` | Follow-on per-domain work (ADR-41) |
| Return-dir path (`council.return_dir` config key) | `~/.claude` global config | Follow-on per-domain work |

Detailed stage mechanics follow. The stage numbers (0–6) map to loop steps
(1–6) as: Stage 0 = Step 1, Stage 1 = Step 2, Stage 1a = Step 3, Stages 2–3
= Step 4, Stages 4–5 = Step 5, Stage 6 = Step 6.

---

## Stage 0 — Frame the question

**Owner:** operator (in head, in a scratch doc, or in browser chat).
**Output:** a single sentence stating the *problem*, not a candidate answer.
**Gate:** if you can't state the question in one sentence, it is two questions;
split them into two debates.

Anti-patterns (from `council-question-guide.md` § Neutralizing bias):

- Leading headline — names a candidate answer instead of the problem
- Asker-leakage — "I think…", "obviously…", "ideally…" anywhere in the brief
- False dichotomy — forces binary when a hybrid exists
- Choice-set bias — debating among three options without an explicit escape
  ("a different approach (name it)")
- Loaded terminology — "bloated", "messy", "obvious" — replace with observable
  facts

The bias self-check is question 6 of the council-question-guide pre-flight:
*if a fast unanimous agreement would not surprise you, the question is leading*.

---

## Stage 1 — Generate / Author the brief

**Owner:** operator (manual) or Claude Code via `/council-question` trigger (ADR-67).
**Tool (manual):** any markdown editor — browser, Obsidian, VS Code, paper-to-md.
**Tool (automated):** `/council-question` — Claude Code fills the Council-question
template and self-gates it (see Stage 1a). Use this path by default; manual
authoring is the fallback when the question requires off-device or browser-only
context not available to Claude Code.
**Output:** a `.md` file. **Ephemeral** — never committed to a repo folder.
Per ADR-60 amendment 2026-05-27, there is no `council-questions/` folder; the
permanent record is the canonical transcript (`ai-council/output/`) + the ADR
it informs, not the brief.

**Decision-mode format** (`pick`, `ideas`, `judge`):

```markdown
---
models: claude,gemini,deepseek,grok
synthesizer: openai
rounds: 2
mode: pick                            # optional — usually auto-detected
---

## Question: [one sentence stating the problem]

### Current State

[Concrete facts: numbers, paths, file counts, what exists today. No opinions.]

### Questions

1. **[sub-question]?**
   - A: [option with trade-off baked in]
   - B: [option]
   - C: [option]
   - D: a different approach (name it)        # explicit escape — choice-set bias mitigation

### Constraints

- [hard constraint that ELIMINATES at least one option]
```

Size guide: 40–80 lines total, 3–7 sub-questions, 2–4 options each (never >5).
A brief over 100 lines has narrative that should be facts — trim.

**Research-mode format** is different — it is a retrieval brief, not a ballot.
See `council-question-guide.md` § Research-mode questions for the full schema.
Key differences: no `Questions`/`Constraints`; uses `Background`/`What to find
out`/`Source rules`/`Output wanted`; recency window and source-type rules are
mandatory.

### Frontmatter reference

| Field            | Default                                  | Notes |
|------------------|------------------------------------------|-------|
| `models`         | `claude,gemini,openai,deepseek,grok`     | All 5 by default. `--lite` overrides to 3-model (claude, gemini, openai). |
| `synthesizer`    | `openai`                                 | Must NOT be on the panel; the default is auto-excluded. gemini→openai ratified 2026-07-18 (operator ruling, `docs/audits/2026-07-17-synthesizer-ruling-gemini-to-openai.md` in ai-council). |
| `rounds`         | `2`                                      | Max 2 (per ADR / debate.py policy). `1` for simple pick. |
| `mode`           | auto-detected                            | `pick` / `ideas` / `judge` / `research` (aliases: `p/d`, `i/e`, `j/a`, `r`). Force only when auto-detect would guess wrong. |
| `target-project` | omitted                                  | **RETIRED 2026-07-22 (ADR-43 amendment 2026-07-23) — do not set.** The routed-mirror landing zones are retired; transcripts are canonical-only in `ai-council/output/`. Config-side disarm tracked [#401]. |
| `full`           | `true` (panel default)                   | Rarely set explicitly. |

Frontmatter keys recognised as "this is a Council brief" by the Downloads
scanner: `mode`, `rounds`, `models`, `synthesizer`, `full`, `target-project`
(any one is sufficient; case-insensitive). Source: `inbox.scan_downloads_folder`.

---

## Stage 1a — Gate

**Owner:** Claude Code (when `/council-question` is used) or operator (when manual).
**Gate logic** *(implementation: `ai-council` — follow-on per-domain work)*:

- All required template sections present (`## Question`, `### Current State`,
  `### Questions`, `### Constraints`)
- Exactly one decision asked (multiple decisions = split into separate briefs)
- At least one option per sub-question, with an explicit escape option
- ADR context section attached (relevant prior ADRs cited or summarized inline)
- No asker-leakage patterns (`I think`, `obviously`, loaded terminology)

**Pass:** brief proceeds to Stage 2 (Route to inbox).
**Fail:** Claude Code reports the gap; operator fixes before routing. Do not
drop a failing brief into the inbox — a context-gap question produces
lower-quality verdicts that are more expensive to discard than to fix.

Until the `ai-council` gate check is implemented, perform this review manually
before dropping the brief into the inbox. The template fields above are the
checklist.

---

## Stage 2 — Route the brief to the inbox

**Owner:** operator.
**Mechanism:** drop the `.md` file in one of two locations. The CLI picks it
up on the next `--inbox` run.

| Location                     | Detection rule                                                                                                       |
|------------------------------|----------------------------------------------------------------------------------------------------------------------|
| `ai-council/council_inbox/`  | **Any** `.md` file. No naming token needed. Folder is gitignored. (Authoritative: `inbox.scan_inbox`.)               |
| `~/Downloads/`               | `.md` file whose stem contains `council` (case-insensitive) **OR** whose YAML frontmatter contains a recognised Council key (see Stage 1 table). Other `.md` files in Downloads are silently ignored. (Authoritative: `inbox.scan_downloads_folder`.) |

**Recommendation:** when in doubt, drop into `council_inbox/`. Use Downloads
only for files authored on another device or in a notes app and auto-detected
without a manual move.

**Files are processed oldest-first** (sorted by mtime ascending). Batch
ordering is deterministic.

---

## Stage 3 — Run the debate

**Owner:** Claude Code (or operator at the CLI).
**Command:** `python -m ai_council.cli --inbox` (or the `council` entry point).
**Working dir:** `ai-council/`.

What the CLI does, in order (source: `cli.main`, `runner.CouncilRunner`,
`debate.run_debate`, `synthesis.synthesize`):

1. **Load config** — `config/settings.yaml`; resolves `dev_root`, opt-in
   `target_projects` list, mode aliases, research config.
2. **Validate `--target-project` and `--mode` args early** — fail-loud
   `RoutingError` listing all known target names if unknown; unknown mode
   aliases exit non-zero before any debate work.
3. **Build providers** from `PROVIDER_CLASSES` (anthropic, openai, gemini, xai,
   deepseek). Missing API key → provider skipped, not fatal unless all skipped.
4. **Health check.** Non-research modes: blocking gate — failed providers
   listed, operator confirms `Continue with working providers only?`
   Research mode: only the summarizer is pinged, non-blocking (research falls
   back to a truncation summary on summarizer outage — ADR-08).
5. **Scan inbox + Downloads**, build the file list, batch oldest-first.
6. **For each file:**
   - `inbox.parse_file` extracts body + frontmatter and resolves `target-project`
     names to absolute paths via `TargetResolver` (ADR-43). The mechanism is still
     present in code, but routed mirrors are RETIRED as doctrine (ADR-43 amendment
     2026-07-23) — do not set `target-project`; disarm tracked [#401].
   - **Mode resolution precedence:** CLI `--mode` > frontmatter `mode:` > default.
   - **Models / synthesizer / rounds:** CLI flags override frontmatter; mode
     config supplies max_rounds when neither is set.
   - **Synthesizer exclusion** (`runner.exclude_synthesizer_from_panel`) drops
     the synthesizer from the panel before debate starts — ADR-01.
   - **Decision modes:** run N rounds (default 2). Round 2 anonymises responses
     before voting (`_anonymize_responses()` — blind vote, ADR-03).
   - **Research mode:** separate code path (`research.runner.run_research`);
     no debate rounds; parallel-retrieval; file cache (`--no-cache` to skip);
     `--deep` opt-in for slower o3-deep-research.
   - **Synthesise:** default `openai` writes the verdict (gemini→openai ratified
     2026-07-18, operator ruling); never participates on the panel.
   - **Write canonical** transcript to `ai-council/output/council-out-YYYYMMDD-HHMMSS-topic.md`
     (always; hard failure if it can't).
   - **Mirror to targets** (best-effort) — see Stage 4.
   - **Archive the brief** to `council_inbox/archive/YYYY-MM-DDTHHMM_<slug>.md`
     (or `FAILED_<...>` on exception). Originally-from-Downloads files print
     `Processed from Downloads: <name> -> archived`.
7. **Exit codes** (ADR-08 convention):
   - `0` — all runs ok
   - `1` — hard error (config, no providers, canonical write failed)
   - `2` — Click usage error
   - `3` — degraded (at least one research run completed with the truncation
     fallback)

What the operator sees during the run: per-provider health-check OK/FAIL list,
round-by-round progress (rich progress bars; ASCII only on Windows), cost
summary at end, transcript paths.

**Gate at end of Stage 3 (revised 2026-07-23):** no routed transcripts are
expected — the routed-mirror is RETIRED (ADR-43 amendment 2026-07-23). A
`docs/decisions/transcripts/` folder appearing as untracked files in any repo
is the [#401] re-creation hazard firing, not something to commit: do not commit
it; disarm the config per [#401].

---

## Stage 4 — Review the verdict

**Owner:** operator.
**Inputs:** the canonical transcript at `ai-council/output/council-out-*.md`.

**Transcript structure** (source: `synthesis.synthesize` + `output.save_to_file`):

- Header — question, panel, synthesizer, mode, rounds, timestamp, target
  paths (if any)
- Round 1 responses (per provider, attributed)
- Round 2 responses (per provider; in decision modes Round 2 is preceded by
  blind-vote anonymisation)
- **Synthesised verdict** — the synthesizer's structured recommendation.
  Decision modes: a pick with rationale and dissent summary. Ideas: clusters +
  wild cards. Judge: verdict + evidence. Research: sourced report.
- Cost breakdown (per provider, total)

**How to read the vote.** Decision modes report the verdict *and* the dissent.
A 3-2 split with strong dissent reasoning is not the same as a 4-1 with weak
dissent; read the dissent before treating the majority as binding. The
synthesizer summarises — the transcript carries the underlying argument.

**Where the transcript lands.**

- **Canonical (only):** `ai-council/output/council-out-YYYYMMDD-HHMMSS-topic.md`.
- **Routed mirrors — RETIRED 2026-07-22 (ADR-43 amendment 2026-07-23).** The
  former opt-in mirror (`target-project:` / `--target-project` → a byte-equivalent
  copy in `<dev_root>/<name>/docs/decisions/transcripts/`) is retired as doctrine;
  the hub's landing zone was deleted (`b4435fad`, operator ruling 2026-07-22). Do
  not set `target-project`; the config-side disarm is tracked [#401]. The binding
  record of a decision is its ADR (Stage 5) — there is no transcript archival
  step, manual or routed; git history retains the pre-retirement routed copies.

---

## Stage 5 — Author the ADR

**Owner:** Claude Code in the target repo (per ESSENTIALS § "Repo artifacts in
Claude Code, not browser chat"). **Mandatory** — a Council debate is not
complete until its ADR exists. Per ESSENTIALS: "Council ADR distillation is a
mandatory automated step of the post-debate protocol — never a browser-chat
hand-off with a placeholder."

**Pipeline:**

1. **Verify ADR number** — read `docs/decisions/README.md` index; next
   sequential `ADR-NN`.
2. **Draft `docs/decisions/ADR-NN-topic.md`** — lightweight format:
   `Status / Context / Decision / Consequences / Alternatives considered /
   References`. The transcript is the evidence; the ADR is the canonical
   record. Reference the transcript filename in `References`.
3. **Commit the ADR** — no transcript lands in the target repo (routed-mirror
   retired 2026-07-23; the canonical transcript stays in `ai-council/output/`).
   Conventional Commits: `docs(decisions): ADR-NN — [topic]`.
4. **Update `docs/decisions/README.md`** — add the new ADR row + any
   traceability entry. Same commit as the ADR.
5. **Amendments not rewrites.** ADRs are immutable. If the decision needs
   revision, write a new ADR that supersedes (or amends) the prior. Never
   edit a ratified ADR in place (sole exception: the *status line* on
   ratification, e.g. Proposed → Accepted — ADR-94; decision content never).

For pick/judge modes, the ADR is a Decision record. For ideas/research modes,
the transcript itself is the deliverable — no ADR is required unless the
operator subsequently makes a binding choice based on it (in which case the
*choice* gets the ADR, citing the research as evidence).

### Deterministic return (ADR-67)

After the ADR is drafted and committed, Claude Code writes a copy to the
operator's **return directory** (`council.return_dir` in `~/.claude` global
config) so the ADR is available at a known path without relocation guesswork.

*Implementation: `~/.claude` config key + `ai-council` I/O wiring — follow-on
per-domain work.* Until implemented, the operator locates the ADR at its
committed path in the target repo (no behavior change from v1.0).

---

## Stage 6 — Close out

**Owner:** operator + Claude Code.

1. **Discard the brief** — the brief in `council_inbox/archive/` is preserved
   only for run-recovery debugging; it is not the institutional record. Per
   ADR-60, briefs are ephemeral. Do not commit them anywhere.
2. **JOURNAL entry** in the target repo — one entry: `Did / Result / Changes
   / Abandoned / Next`. Cite the ADR number and the transcript filename.
3. **BACKLOG follow-up** — if the ADR closes a queue item, route it through the
   Tier-1 closure loop: `closes [#id]` in the commit plus the retirement per
   `tasks/README.md` on the hub (manifest node out, terminal `status:`,
   `--emit-source`); an unflipped consumer removes the line directly. Done items
   **leave** — there is no "closed" status marker (ADR-65). If the ADR *opens*
   new follow-up work (almost every architectural decision does), file it as a
   `tasks/` add carrying `Refs: ADR-NN`.
4. **Cross-repo propagation** — if the decision binds multiple repos (e.g.,
   ecosystem-wide convention authored in `.dev-knowledge`), the propagation
   happens via cross-repo routing artifacts, NOT via the originating repo's
   BACKLOG. See PLAYBOOK § "Cross-repo decision propagation".

---

## Troubleshooting

| Symptom                                                            | Likely cause                                                                                                        | Fix                                                                                          |
|--------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| `RoutingError: unknown target 'X'` at startup                      | `target-project: X` set on the brief — the field is RETIRED (ADR-43 amendment 2026-07-23); only reachable via the retired flag | Remove `target-project:` from the brief (do not add targets — routed mirrors are retired; see [#401]). Fail-loud is by design. |
| File in `~/Downloads/` not picked up                                | No `council` token in stem AND no recognised Council frontmatter key                                                | Rename to include `council` OR add `mode:` (or other key) to frontmatter — or move to `council_inbox/`. |
| Health check fails for one provider                                 | Missing/expired API key, network issue, provider outage                                                              | Choose "continue with working providers" when prompted (non-research modes). Restore key after the run. |
| Exit code `3` after `--inbox`                                       | At least one research run degraded (summarizer outage → truncation fallback per ADR-08)                              | Inspect the research report; rerun with `--no-cache` after summarizer recovers if a clean version is wanted. |
| Brief archived as `FAILED_<timestamp>_<name>.md`                    | Exception during debate or routing parse                                                                             | Read CLI error; fix the brief (or routing config) and move it back from `council_inbox/archive/` to `council_inbox/`. |
| Synthesis is biased toward the asker's pre-stated preference        | The brief leaked the asker's lean (Stage 0 / 1 bias)                                                                 | Discard the verdict; rewrite the brief per `council-question-guide.md` § Neutralizing bias; rerun. Blind voting cannot fix this. |
| Cost surprise (debate cost > $1.00)                                 | Full panel + 2 rounds + long question. Or research `--deep` opt-in.                                                  | Use `--lite` (3-model) and/or `--rounds 1` for simpler questions. Cost gate lives in operator judgment, not policy. |

---

## Cross-references

- **This amendment:** `docs/decisions/ADR-67-ai-council-process-operationalization.md` (gated loop + /council-question trigger + deterministic return).
- **Visual:** `ARCHITECTURE.md` § Processes → "AI Council debate pipeline" (Mermaid C3).
- **Question format authority:** `ai-council/docs/council-question-guide.md`.
- **Routing decision:** `docs/decisions/ADR-43_cross_project_transcript_routing.md`.
- **Blind voting:** `ai-council/docs/decisions/ADR-03-blind-voting.md` (tool-layer).
- **Folder taxonomy / ephemeral briefs:** `docs/decisions/ADR-60-docs-folder-taxonomy.md`.
- **Decision threshold + post-debate steps:** `protocols/PLAYBOOK.md` § "Council debate threshold", § "Post-debate protocol". (The archival protocol is retired — PLAYBOOK § "Council Debate Archival Protocol (RETIRED 2026-07-22)". The former § "After a Decision" ref was stale — no such section exists.)
- **Repo-artifacts-in-Claude-Code rule:** `protocols/ESSENTIALS.md` § "Repo artifacts".
- **Gated-loop pattern (handoff analogue):** `HANDOFF_PROCESS.md` + ADR-42/55/56/57/58/62.
- **Live code:** `ai-council/src/ai_council/{cli,inbox,routing,runner,orchestrator,debate,synthesis}.py`.

---

## Section history

- v2.2 (2026-07-29) — post-flip stale-procedure fix batch (audit `2026-07-29-technical-postflip-stale-procedure-audit.md`, row 11): Stage 6 item 3 no longer says "mark it closed" (not the ADR-65 shape — done items leave, no status marker) and no longer implies a direct `BACKLOG.md` edit; closure now routes through the Tier-1 loop with a `tasks/` retirement on the hub (ADR-107 step 3 / [#439]), and follow-up work is filed as a `tasks/` add. Genuine end-to-end re-read; `last_reviewed` re-stamped 2026-07-29.
- v2.1 (2026-07-23) — ADR-43 amendment (routed-mirror RETIRED; operator ruling 2026-07-22, hub zone deleted `b4435fad`): Purpose/Stage 3 gate/Stage 4 landing/Stage 5 step 3/frontmatter table/template example/troubleshooting/Cross-references all repointed — transcripts are canonical-only in `ai-council/output/`; `target-project:` not to be set; config disarm tracked [#401]. Re-read fixes: synthesizer default gemini→openai (2026-07-18 operator ruling), ADR-94 status-line exception added to Stage 5 item 5.
- v2.0 (2026-06-01) — ADR-67: added Gated loop overview (6 steps, cross-domain split table, stage mapping); Stage 1 updated to `/council-question` trigger (template+gate downstream); Stage 1a Gate inserted; Stage 5 Deterministic return subsection added; Cross-references updated.
- v1.0 (2026-05-28) — initial. Companion to ARCHITECTURE.md C3 "AI Council debate pipeline" diagram. Closes BACKLOG "AI Council Flow operationalization — lifecycle runbook" (open since 2026-05-27).
