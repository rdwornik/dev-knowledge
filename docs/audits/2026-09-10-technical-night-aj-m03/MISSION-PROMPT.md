NIGHT MISSION 2026-09-09 — Architekt Jutra M01–M03 + Maister vs our harness: what the spine,
the self-improvement loop and model-agnosticism still lack. Unattended. Pre-authorised; no
approval gate anywhere in this run.

STOP CONDITIONS: wall cap 6 h → kill the process tree · abort if free RAM < 1 GB · no
commit to main · all work in ONE worktree `night-aj-m03-review` · every output under
docs/audits/2026-09-10-technical-night-aj-m03/ · no BACKLOG.md or tasks/ edit (row
candidates go to a list, the day seat files) · no code copied from any external repo, ever.

HARD RULES (each failed today, each is a refusal here):
R1 · If an ordered tool does not answer, you do NOT substitute another tool silently. Record
     the exact command, the exact response, mark the leg SUBSTITUTED-PENDING-OPERATOR, and
     continue only with what was ordered elsewhere. The operator rules on substitutions in
     the morning.
R2 · Every locator (file:line, URL, commit, page, lesson number) from any reader is verified
     by a CC subagent against the source before it enters a report. Unverified = marked
     UNVERIFIED, never dropped, never promoted.
R3 · Every output file records: model, exact invocation, wall time, and whether the reader
     was ordered or substituted.
R4 · Our own prior conclusions are TARGETS. Attack: "Maister offers nothing beyond a spine"
     (DECLARE-HARNESS-IS-PROCESS §5) · the 16-stage delivery-loop map · the census's 32
     orphans · the conductor decision E · the five DEAD PLAYBOOK sections. A reader that
     merely agrees has not read.
R5 · Provider invocations that WORK, verified 21:52 today — use these, no others:
     codex: `codex exec -c model=gpt-5.6-sol -s danger-full-access ...` (default model
     gpt-6-astra returns 400; not an auth failure)
     agy:   the non-interactive shape recorded in [#676] (gemini-3.8-flash-low answered in
            2.37 s); if it fails, R1 applies — do not fall back to Claude subagents
     grok:  as probed in [#676]
     cursor-agent: absolute path, `-p --trust`
     copilot: ONE call maximum — it meters premium requests
     glm / deepseek: do not attempt (corrupt binary / absent)

INPUTS
A · Architekt Jutra M03, local: C:\Users\1028120\Documents\Priv\Architekt Jutra\
    Transcripts: AJ_M03L01..L06_transkrypcja.pdf (+ AJ_M03_transkrypcje.md.zip — prefer the
    .md if it unzips clean). Presentations: AJ_M03L01..L06_prezentacja.pdf. Do NOT process
    the mp3s — the transcripts are the text.
B · https://github.com/Architekt-Jutra/architekt-jutra-code — clone read-only to a temp dir.
C · https://github.com/SkillPanel/maister — clone read-only. Target: the orchestrator state
    file and phase triggers §5 names; how tasks carry state; what fires what.
D · Our prior AJ work, in-repo: docs/intake/2026-09-05-tech-aj-second-pass.md (#20, M01–M02)
    and the tools/evals intake of 2026-09-07; DECLARE-REVIEWS (R-1…R-8) and
    DECLARE-HARNESS-IS-PROCESS §5 as landed in rows [#644]–[#663].
E · Our measurements this window: docs/audits/2026-09-08-technical-process-trigger-census.md
    (160/24/32); DECLARE-DELIVERY-LOOP-MAP (16 stages); DECLARE-RECOVERY; DECLARE-CONDUCTOR-
    DECISION (E, and AMEND-001: Free plan blocks required checks); DIGEST-playbook-chapter-map
    (content stands; its "agy abandoned" attribution is withdrawn).
F · The hub itself: scripts/, protocols/, .claude/, ecosystem/, deploy/, tests/.

PHASE 1 — READ (cheap models, parallel, each writes one file with locators)
 1a agy   → M03 lesson by lesson: what practice it teaches · the mechanism it implies
           (trigger → organ → artifact) · what it says about telemetry, testing, naming,
           task/intake flow, model switching. One file per lesson, one line per claim, each
           claim with page/timestamp.
 1b agy   → repo B: what it implements, in what shape (state file? hooks? commands?), what
           its task lifecycle looks like, where the human sits. Locators = file:line.
 1c codex sol (ONE adversarial pass) → repo C (Maister): derive independently what the
           process spine IS — state carrier, phase set, trigger per phase, gate per phase —
           and where a task's state lives. Then, separately, the same derivation for OUR
           repo (F). Two tables, same columns. Do not read §5 first; derive, then compare.
 1d grok  → our repo F, census-style: every script/hook/command/skill → trigger or NONE.
           Independent of the 2026-09-08 census. Diff against it. Every disagreement is a
           finding about one of the two methods.
 1e cursor-agent → our repo F: naming, layout, test-presence per module, "is there a test
           that cannot fail" scan (assertions that hold for any input). One table.
 1f one Claude Sonnet subagent → model-agnosticism audit of OUR process: list every place
    the handoff bundle, SEAT-BOOT renders, ROUTING.md, PLAYBOOK Ch8, the dispatch verbs,
    and the browser contract assume a specific vendor/model. Table: file:line · assumption
    · what a swap to (Codex | Gemini | Grok) would break.
 CC verification subagents run R2 over every table before Phase 2.

PHASE 2 — COMPARE (Sonnet, you)
 Build ONE matrix: rows = every practice from M01 (from #20), M02 (from #20), M03 (1a),
 Maister (1c), repo B (1b). Columns: IMPLEMENTED-MECHANICALLY (name the organ + trigger) /
 IMPLEMENTED-IN-PROSE (name the doc line) / MISSING / REJECTED-WITH-REASON (cite the ruling).
 A cell is filled only from a verified locator. Then three focused sections:
   SPINE — what Maister's state carrier does that our tasks/ + FPG-1 + (planned) conductor
           do not; what E (Actions as runner, Free plan, no required checks) cannot do.
   SELF-IMPROVEMENT LOOP — telemetry consumed by which process (today: none); which M01–M03
           practice closes stage 12 (eval) and stage 15 (nightly) of our 16-stage map.
   MODEL-AGNOSTIC — from 1f: the minimum set of changes for "swap the architect model" to
           be one config line.
 Plus: the DELETE LIST — from the census 32, the 1d diff, the 1e cannot-fail tests, the five
 DEAD PLAYBOOK sections, and anything M03/Maister makes redundant. One line each, evidence,
 "delete" or "wire" — no third verb.

PHASE 3 — REVIEW (claude opus, one subagent, last)
 Read Phase 2 only. Output docs/audits/2026-09-10-technical-night-aj-m03/REVIEW.md:
   1. The ten things that are missing, ranked by what unblocks stage 10 (deploy to
      corp-monorepo) soonest. Each: one line · which M-lesson or Maister mechanism it comes
      from · row candidate in ADR-87 shape (intent · closure number · anti-pattern · pointer).
   2. Which of our prior conclusions Phase 1 overturned, with the locator that overturns it.
   3. What this mission could not verify (R2 UNVERIFIED count per reader).
   4. Substitutions that occurred (R1), for the operator's morning ruling.
 No new organs proposed. Consolidation and deletion only, plus the spine's missing pieces.

CLOSE
 Commit all outputs to the worktree branch `night-aj-m03-review`, push, STOP. No merge.
 Write docs/audits/2026-09-10-technical-night-aj-m03/NIGHT-LOG.md as you go: command · model
 · start · end · result, one line per leg, appended not rewritten. First line of the log:
 this prompt's sha256.
