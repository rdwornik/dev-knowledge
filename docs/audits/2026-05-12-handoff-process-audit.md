---
audit: handoff-process
date: 2026-05-12
scope: meta
status: complete
purpose: ground next browser chat understanding before improvement proposals
---

<!-- scope: meta -->

# Handoff process audit — natural-language end-to-end description

**Audience.** A new browser chat asked to propose improvements to the
handoff process, plus the operator reviewing his own methodology. Neither
has filesystem access in the moment of reading. The job of this audit is
to put the whole process on one screen, in plain prose, before any
proposals get drafted.

**Method.** Read the protocol document, the two templates, the slash
command, and four real handoff artifacts (one current audit-sync, one
current session-sync, one archived stage-1+2 pair, one legacy single-file
handoff). Then trace a specific handoff end-to-end as a story. No
process changes proposed.

---

## What the process is supposed to do

**A handoff is how a session hands its working context to whatever
session comes next, without that next session having to reconstruct the
context from logs.** In this repo's vocabulary a "session" is a single
browser chat (claude.ai) or a single Claude Code run. Browser chats die
when their context window fills up; Claude Code sessions reset when
closed. The handoff exists because the work being done — designing
governance for a small ecosystem of repos — is too long-running for one
session to finish, and the most valuable thing in a maturing session
(the architect's accumulated judgment about what matters, what was
tried, what to avoid) is also the most perishable. The handoff captures
that judgment while the session is still lucid, and packages it so a
brand-new session can pick up the work without re-deriving it.

**The current implementation is a three-stage relay between three
actors.** Claude Code in the `.dev-knowledge` repo is the orchestrator:
it reads the target repo's git state, generates artifacts, runs
validators, commits. The "OLD" browser chat is the one being wrapped up
because its context is full — it holds the irreplaceable tacit knowledge
the handoff is trying to preserve. The "NEW" browser chat is opened
fresh after the handoff bundle is ready; it has no prior history and
gets everything from the uploaded bundle. Stage 1 asks Claude Code to
generate a question prompt that Rob carries to the OLD chat. Stage 2 is
the OLD chat answering those questions from lived knowledge. Stage 3
goes back to Claude Code, which reconciles the answer against the
current repo state and emits a flat 11-file folder for the NEW chat to
consume. Between Stage 2 and Stage 3 there is an optional Stage 2.5
Q&A loop where the NEW chat can route clarification questions back to
the OLD chat before any prompts get generated.

**The governance that backs this lives in three layered decisions.**
The earliest, ADR-32 (April 2026), introduced the basic idea: split
roles (browser plans, Claude Code executes), use a folder rather than a
single markdown file, ground the folder with a manifest and a HEAD pin.
ADR-37 (also April) added the "current state vs. future state" framing
on top — every handoff should explicitly say where the project is now
and where the next session should take it. ADR-42 (May 9, amended three
times the same day) is the current authority: it specifies the
three-stage relay, the 11-file flat folder, full copies of VISION /
PLAYBOOK / ESSENTIALS as invariants, and SHA-256 checksums for drift
detection. The operational counterpart of ADR-42 — the actual step
list a session follows — is `protocols/HANDOFF_PROCESS.md` v3.2. If the
two ever disagree, ADR-42 wins.

---

## How templates and slash commands implement it

**Two templates do most of the structural work.**
`templates/HANDOFF_QUESTION_TEMPLATE.md` shapes Stage 1 (the prompt that
goes to the OLD chat). `templates/HANDOFF_FOLDER_TEMPLATE.md` shapes
Stage 3 (the 11-file bundle the NEW chat reads). There is also a
`HANDOFF_TEMPLATE.md` left over from ADR-32's 9-section single-file
format; it is no longer used for current handoffs but has not been
removed and is not marked deprecated in the file itself.

**The Stage 1 template is split into two audiences with a thick visual
delimiter between them.** Section A is Rob's operating instructions
(open the OLD chat, copy from the boundary line down, paste, then save
the response into a pre-created file). Section B is the message Rob
actually pastes into the OLD chat. The boundary between them is a row
of `═` characters — chosen so that if Rob scrolls or copies
inattentively, the boundary is still visually unmistakable. Inside
Section B, four orienting blocks precede the questions: a role
description (you are the project architect, not the ecosystem oracle),
a list of what the NEW chat will already have (so the OLD chat does not
repeat ecosystem-wide facts), an epistemic-honesty instruction
(distinguish *Witnessed* / *architect inference* / *Unknown*), and a
strict format spec. The order is load-bearing: an earlier iteration
buried the format requirements at the end and the OLD chat consistently
fabricated specifics it did not actually know — captured as a lesson
on 2026-05-09 (`LESSONS.md:236`, "handoff-audience-confusion").

**The Stage 3 template prescribes the 11-file flat folder.** Three
files are full copies of the ecosystem's own governance documents
(`02_VISION.md`, `03_PLAYBOOK.md`, `04_ESSENTIALS.md`) — explicitly
"never curated"; the template's content invariants say this twice. One
file (`05_GOVERNANCE_ESSENCES.md`) carries 2-4 sentence summaries of
the ADRs actually cited by the directives, and only those. Two files
hold Stage 2's structured answer split into Current and Future state:
`06_STATE_OF_PLAY.md` (Stage 2's REALITY + RATIONALE plus Stage 3's
verification of architect claims against the repo) and
`07_ACTION_PLAN.md` (OBJECTIVE + DIRECTIVES + BOUNDARIES). A flat text
tree (`08_TREE.txt`) gives structural orientation. An empty
`09_EXECUTION_EVIDENCE.md` is the return-trip slot. A
`01_manifest.json` carries SHA-256 of every file and the captured HEAD
SHA. Two README-ish files at the front (`00_README.md`, `00_first-message.md`)
walk the operator and the NEW chat through what to do.

**The templates are not neutral about content — they invite a register.**
The Stage 1 template's pipeline questions use SBAR/I-PASS vocabulary
borrowed from medical handoff protocols: OBJECTIVE, REALITY, RATIONALE,
DIRECTIVES, BOUNDARIES. That vocabulary buys consistency between
handoffs but also pulls the response toward a status-report
register. The format requirements section (`HANDOFF_QUESTION_TEMPLATE.md:130-187`)
prescribes "no preamble", "no closing remarks", section headings to a
fixed name and order, and an output that will be copy-pasted verbatim
into a parsed file. Combined, this asks the OLD chat for something
shaped like a form, not a memo — which then propagates into the
generated `06_STATE_OF_PLAY` and `07_ACTION_PLAN`. The format
prescriptions are tight for a reason (Stage 3 has a tolerant parser
but still parses); the cost is that prose drifts toward enumeration.

**The slash command is thin glue.** `.claude/commands/handoff.md`
(40 lines) routes one of three trigger phrases — "make handoff for X",
"save this response as stage 2 for X", "complete handoff for X" — to
the matching stage in `HANDOFF_PROCESS.md`, then enumerates a handful
of constraints whose violation is a process failure: no audit-sync
shortcut; Stage 3 must not run without Stage 2 present; HEAD-SHA drift
must be flagged not silently absorbed; full VISION/PLAYBOOK/ESSENTIALS
in the bundle; only ADR essences (not full ADR copies) in
`05_GOVERNANCE_ESSENCES.md`; flat folder, no subdirectories. There is
no separate skill file; the command is the entire user interface to
the process.

---

## What artifacts look like in practice

**The current bundles are uniform and well-formed.** Both 2026-05-09
handoffs (ai-council audit-sync, dev-knowledge session-sync) have all
12 files in the expected flat layout (the 11 in the spec plus
`01_MANIFEST.md` as the human-readable counterpart to the JSON).
Sections appear in the right order; HEAD SHAs are pinned; manifest
checksums are present; the archive folder contains the matching Stage
1 question and Stage 2 response. The legacy file
`archive/legacy/2026-04-15-tech-radar-session.md` is a single markdown
file under 100 lines organized by topic-headed "COMPLETED — X"
sections — visibly a different format and a different register, much
closer to a personal status note than to a parseable handoff.

**The Stage 1 prompt artifacts are clear and operator-friendly.**
Reading `archive/2026-05-09-ai-council-audit-sync/stage1-question.md`
cold, the role explanation, the list of things the NEW chat will
already have, the epistemic-honesty rule, and the format spec all
arrive before the questions, so the OLD chat reaches the questions
already framed. The format examples (`example WRONG opening:` with the
buried-in-code-fence anti-pattern) are concrete enough to act on
without further explanation.

**The Stage 2 response artifact (architect answer) is the most
narrative document in the bundle.** In the ai-council case the OLD
chat's REALITY section is essentially a prose recap of the session:
"ADR-38 structural migration was planned, prompted, executed, and
merged in this chat" (`stage2-response.md:19`); "Gemini was switched
to default synthesizer (replacing Claude Sonnet 4.6 which timed out on
5-model transcripts)" (`stage2-response.md:20`). Almost every claim is
marked with an explicit epistemic flag — "Witnessed", "Unknown — verify
against repo", "(architect inference)" — and the architect even
honestly catches itself in places ("council_inbox/ creation fix
committed... (architect inference) I believe the fix was committed
but should be verified", `stage2-response.md:26`). This is the most
accessible document in the whole chain.

**The Stage 3 outputs compress the same content but lose some of the
readability.** `06_STATE_OF_PLAY.md` is organized as
section-headed lists ("P1 — Governance-blocking, tier-independent",
"Verified claims", "Verification failures / corrections", "Architect
inferences (preserved with flag)"); each item is one line, often
referenced by a finding code (`F-01`, `F-02`, ..., `F-08`) plus an ADR
number. The information density goes up but the readability goes down
unless the reader already knows what `F-01` and `ADR-33` mean.
`07_ACTION_PLAN.md` is structured as a numbered directive list where
each directive bundles an action verb, a target, a commit message, and
a verify command — a usable runbook, but a runbook, not a brief. The
DO-NOT list at the end (10+ items in the ai-council case,
`07_ACTION_PLAN.md:96-111`) reads as a wall of negative space.

**One short quote that illustrates the readability gap.** From the
dev-knowledge session-sync, the Current State opener:
"Phase 1 governance closure (9 ADRs ratified): ADR-33 (VISION
universalization), ADR-34 (file naming), ADR-35 (lessons base
activation), ADR-36 (audit tool architecture), ADR-37 (session
boundary protocol), ADR-38 (universal repo architecture), ADR-39 (file
lifecycle governance), ADR-40 (scale tier evaluation), ADR-41
(cross-session backlog)." (`docs/handoffs/2026-05-09-dev-knowledge-session-sync/06_STATE_OF_PLAY.md:13-17`).
The line is a faithful index but it leaves the reader to decode what
"Phase 1 governance closure" was for, what those nine ADRs together
accomplish, and why a list of nine numbered decisions has shipped in
one cluster. One sentence of context ("we closed out the first wave of
governance ADRs — universalizing VISION, naming, lessons routing, the
audit tool, session boundaries, repo architecture, file lifecycles,
the tier algorithm, and the backlog model") would do the same work
without a decoder.

---

## Worked example: ai-council audit-sync, end-to-end

**The session that produced it.** Earlier in the day on 2026-05-09 the
`.dev-knowledge` repo had run an audit of `ai-council`, surfacing eight
findings (F-01 through F-08): two P1 governance gaps (no VISION.md, no
lessons-discovery configuration), two P2 deferred items (no BACKLOG.md,
no ARCHITECTURE.md), three P3 grandfathered or calibration items, and
one cross-ecosystem calibration concern. The same afternoon, Rob
decided to hand off to the next ai-council session via the brand-new
three-stage flow that was being built and amended live the same day.

**Stage 1 — Claude Code captured target state and produced the question
prompt.** Claude Code in `.dev-knowledge` read the current ai-council
HEAD (`c821157f...`), branch (`main`), and working tree (one modified
file: `config/settings.yaml`), then created
`_in_progress/2026-05-09-ai-council-audit-sync/stage1-question.md`
following the question template. The output file has the Section A /
Section B split, with the metadata at the top and the audit's eight
findings injected verbatim into Section B as the "Audit context"
block. The five pipeline questions in Section B carry a default
proposal each, derived from the audit, with an explicit "revise as
needed" hint and an inline epistemic note. Alongside it, Claude Code
pre-created `stage2-response.md` as a placeholder with an
`═══ REPLACE EVERYTHING BELOW THIS LINE ═══` marker so the architect
would not have to create a new file.

**Stage 2 — the OLD ai-council chat answered from lived knowledge.**
Rob pasted Section B into the OLD chat. The architect's response (now
in `archive/2026-05-09-ai-council-audit-sync/stage2-response.md`)
confirmed the P1 actions the audit had proposed, explained the
session's actual recent history (ADR-38 package migration, Grok added
as fifth research provider, Gemini becoming default synthesizer
because Claude Sonnet 4.6 was timing out on five-model transcripts),
flagged the modified `config/settings.yaml` as an intentional Grok
research-timeout increase, argued for tier M rather than the audit's
default L using a plain-English risk-and-blast-radius argument, and
laid out a six-step directive list with commit messages and verify
commands. Almost every claim was epistemically tagged. Rob saved this
into `stage2-response.md` and triggered Stage 3.

**Stage 3 — Claude Code reconciled and emitted the bundle.** Claude
Code re-checked HEAD (still `c821157`, no drift), re-read the
templates, copied VISION / PLAYBOOK / ESSENTIALS into the bundle in
full, generated `05_GOVERNANCE_ESSENCES.md` with 2-3 sentence essences
of only the two ADRs cited in the directives (ADR-33 and ADR-35),
split the architect's answers into Current state and Future state
files, regenerated `08_TREE.txt` from `git ls-files` in ai-council,
left `09_EXECUTION_EVIDENCE.md` empty, and computed SHA-256 of
everything into `01_manifest.json`. **Verification caught a real
mistake.** The architect had written that `config/settings.yaml`
contained a Grok research-timeout change from 120s to 300s. Claude
Code diffed the file and found a different change: the Grok *model
string* had moved from `grok-4.20` to `grok-4.3`, plus YAML whitespace
normalization. No timeout change at all. Rather than silently overwrite
the architect's claim or silently pass it through, Stage 3 recorded
both versions: it kept the architect's claim in the Stage 2 archive,
flagged it in `06_STATE_OF_PLAY.md:54-64` as VERIFICATION FAILED /
CORRECTION NEEDED with the actual diff, and rewrote the first directive
in `07_ACTION_PLAN.md:21-28` to say "Stage 3 verified that the actual
change is `grok model: 'grok-4.20' → 'grok-4.3'` ... Write accurate
commit message reflecting actual change." The architect's
`(architect inference)` warning about possible accumulated changes
turned out to be correct, and the verification step is what made it
visible. Inputs were moved from `_in_progress/` to `archive/`; JOURNAL
and CHANGELOG got entries; validators passed; a single commit shipped
the whole stage.

**Stage 4 — the NEW chat received the bundle, the operator carried it
into Claude Code, evidence came back.** A fresh claude.ai chat for
ai-council was given the bundle. It read `00_first-message.md` first,
verified state, presented a synthesis paraphrasing what it intended to
do, generated a Claude Code prompt, and Rob ran that prompt in Claude
Code in ai-council. The execution path is fully recorded in
`09_EXECUTION_EVIDENCE.md`: at session start HEAD was `62c1f7d`, one
commit ahead of the Stage 3 baseline — the missing
`config/settings.yaml` change had been committed in a different
session in the meantime. The HEAD-mismatch guard fired, the working
session retroactively verified that commit `62c1f7d` matched the
expected diff pattern (grok model + whitespace, no other functional
change), then proceeded. Three new commits landed
(`c85e8f9` VISION.md, `8def0f0` CLAUDE.md lessons discovery,
`9ff0391` CHANGELOG + JOURNAL), tests stayed at 310/310, Codex review
was run and recorded inline. The evidence file ends with three
recommendations for the next session, including one — that Stage 3
should know when newer commits are descendants of its pinned HEAD
rather than treating any drift the same — that fed back into the
process.

---

## Where the process generates decoder-required language

**The Stage 1 → Stage 2 vocabulary leaves a print.** OBJECTIVE /
REALITY / RATIONALE / DIRECTIVES / BOUNDARIES are SBAR/I-PASS-shaped
labels. Inside a section the response stays prose, but the section
*names* never get explained in the artifacts they generate downstream,
and the labels carry the weight of headers in `06_STATE_OF_PLAY` and
`07_ACTION_PLAN`. A reader who has not been briefed on the protocol
sees five capitalized words and has to infer that they are a question
pipeline. *Pattern: question pipeline as a name with no plain-language
gloss.*

**Status flags without narrative are common in `06_STATE_OF_PLAY`.**
The most concentrated example is the findings block:
`"P1 — Governance-blocking, tier-independent: F-01: VISION.md absent —
create per ADR-33 schema"` (`06_STATE_OF_PLAY.md:12-14`). Three layers
of compression — a priority code, a finding code, an ADR number —
stack into one bullet. The information is there if the reader can
expand all three; without the expansion it is decorative. The same
shape recurs as "F-03 BACKLOG.md: deferred pending tier calibration",
"F-04 ARCHITECTURE.md: deferred pending tier calibration" — finding
code, status flag, dependency. *Pattern: priority code + finding code
+ ADR reference compressed into a single bullet.*

**ADR references serve as content-stand-ins.** "Create
`ai-council/VISION.md` per ADR-33 (handoff bundle has ADR-33 essence)"
(`07_ACTION_PLAN.md:29`) is fine because the essence travels with the
bundle. "F-05: ADR naming kebab-case (7 existing ADRs grandfathered)"
is also fine because the brackets explain. But "decisions locked: Path
3 calibration strategy ... applied 2026-04-30"
(`06_STATE_OF_PLAY.md:117-118`) names a path number without the path
content, and "applied" treats it as a process event rather than a
choice. *Pattern: ADR or path number standing in for the content of
the decision, with no in-line gloss.*

**Process-language fills space where movement happened.** "Stage 3
note — DoD fix target clarification" (`06_STATE_OF_PLAY.md:152`) and
"amendment cycle closed" (`LESSONS.md:240`) describe meta-states
rather than work. They mean something — the first means "the bug we
spotted is in the generated file, not the template, so fixing the
template would miss it"; the second means "we stopped amending the
ADR" — but the noun phrase form invites the reader to take the
process state on trust. *Pattern: a meta-event in noun form
("compliance verification", "amendment cycle closed", "cross-repo
hygiene check") substitutes for a sentence about what happened.*

**Long DO-NOT lists turn into wallpaper.** The boundaries section in
`07_ACTION_PLAN.md` (lines 96-111 in the ai-council handoff) has
twelve items. Many of them are critical (do not push without
confirmation; stop if pytest fails). A few are very narrow (do not
change the default synthesizer; do not change the default panel).
Reading them as a flat list, the critical and the narrow look the
same. *Pattern: undifferentiated boundary list, where high-stakes and
narrow-scope DO-NOTs share visual weight.*

**The audit's own caution.** This report is itself part of the audit;
the same patterns would degrade it if they slipped in. Where ADR
numbers appear above, they appear alongside a one-line meaning the
first time they show up. Where status codes appear (F-01, P1), they
appear inside an explanation rather than as the explanation. Where
process labels appear (Stage 1, Stage 2.5), they are paired with a
plain description of what happens in that stage.

---

## What works well, to preserve

**Drift detection is wired in at two places and caught a real problem
in the validation run.** Stage 1 captures the target HEAD; Stage 3
re-captures and compares; the NEW chat re-verifies on opening.
SHA-256 over every file in the bundle gives post-generation tamper
detection. In the ai-council case the second-session HEAD was already
one commit ahead of the Stage 3 pin (someone had committed the
pending `config/settings.yaml` change in another session). The
HEAD-mismatch guard fired, retroactive verification confirmed the
divergent commit matched the expected pattern, and the work
proceeded with the divergence documented in `09_EXECUTION_EVIDENCE.md`
rather than silently absorbed. *Preserve: the layered HEAD-pin and
checksum design and the explicit "STOP, flag both SHAs" behavior on
mismatch.*

**Stage 3 verifies architect claims against the repo, with results
made visible.** The Stage 2 architect explicitly tags claims as
*Witnessed*, *(architect inference)*, or *Unknown — verify*. Stage 3
takes the witnessed claims that are checkable, checks them, and
reports the result in `06_STATE_OF_PLAY.md` under "Verified claims" /
"Verification failures / corrections" / "Unverifiable claims
(preserved)" / "Architect inferences (preserved with flag)". The
ai-council case has a worked verification failure: the architect's
description of what `config/settings.yaml` changed was wrong (model
string, not timeout), and the bundle says so, including by rewriting
the first directive. *Preserve: the witnessed/inference/unknown
contract with the architect and the published verification summary
that makes corrections visible rather than silent.*

**Pre-creating Stage 2's response file removed an operator-friction
class.** Stage 1 commits `stage2-response.md` as a placeholder with a
"replace everything below this line" marker. Rob opens it, replaces
the placeholder block, saves. No risk of creating the file in the
wrong place under the wrong name. This was captured as a lesson on
2026-05-09 (`LESSONS.md:240`, "handoff-friction-precreate"). *Preserve:
upstream stages creating the input files downstream stages will need.*

**The OLD-chat / NEW-chat distinction is load-bearing.** The
operational argument is in `HANDOFF_PROCESS.md:114-130` and was
amended into ADR-42 the same day it shipped: Stage 2 must go to the
chat being wrapped up (the one with the tacit knowledge), not to a
fresh chat. The first attempt sent Stage 2 to a fresh chat and got a
response that collapsed to restating the audit findings — adding no
signal. The current direction is now explicit in the question
template's role section. *Preserve: the three-actor framing and the
specific assignment of Stage 2 to the dying chat.*

**The architect's epistemic-honesty markers actually work when used.**
The ai-council Stage 2 response is rich with self-flagging: "council
_inbox/ creation fix committed ... (architect inference) I believe
the fix was committed but should be verified"; "Unknown — verify
against repo: Exact commit count ahead of origin/main." These flags
travel into the bundle, and Stage 3 reads them to decide what to
verify. *Preserve: the explicit per-claim tagging contract — it is
the input to the verification step that catches errors.*

**The visible PASTE_BOUNDARY delimiter prevents an entire failure
mode.** The Stage 1 file has two audiences (Rob's instructions; the
OLD chat). The visually unmistakable `═` row between them keeps Rob
from accidentally pasting his own instructions into the OLD chat or
sending the OLD chat only the metadata. This came out of a lesson
about mixed-audience artifacts (`LESSONS.md:236`,
"handoff-audience-confusion"). *Preserve: explicit per-audience
delimiters in any artifact that serves multiple readers.*

**Full VISION / PLAYBOOK / ESSENTIALS copies prevent silent norm drift
in the NEW chat.** The template marks these as never curated; the
slash command's constraint list re-states it; the rationale (research
on the SECI tacit-knowledge bottleneck plus Rob's "preserve
conversational style" requirement) is in ADR-42's content principles.
The cost is bundle size; the benefit is that the NEW chat never has
to be told how this team writes commit messages or talks about scope.
*Preserve: full copies of the methodology invariants, never curated.*

**The return trip is a real artifact, not theatre.** The ai-council
`09_EXECUTION_EVIDENCE.md` records actual `git rev-parse` outputs,
the actual pytest counts at each commit, the actual Codex review
findings (with reasoning about which were false positives), and three
concrete recommendations for the next session — one of which fed
directly back into a future improvement. *Preserve: the return-trip
slot and the discipline of putting raw command output in it.*

---

## Open questions

- **Are these handoffs being read?** The artifacts are well-formed,
  but I cannot tell from files alone whether the NEW chats actually
  read the full 11-file bundle before synthesizing, or whether they
  read `00_first-message.md` + `07_ACTION_PLAN.md` and skim the rest.
  Receiver-synthesis transcripts (not in the repo) would tell us.

- **Is the SBAR vocabulary helping or only enforcing structure?**
  OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES gives
  uniform sections. It also leaves a register on downstream artifacts.
  Whether a different naming (e.g., "Goal / What's true now / What
  we tried / Next moves / What to avoid") would carry the same
  consistency with less status-report feel is open.

- **Is the priority code / finding code system load-bearing or
  inherited?** F-01 ... F-08, P1/P2/P3 — were these defined for this
  handoff's audit findings (in which case they could be expanded
  inline at no cost), or do they map to a numbering that other
  artifacts depend on (in which case expansion plus code is the
  answer)? The audit report they reference is not co-located with
  the handoff.

- **Should the legacy `HANDOFF_TEMPLATE.md` and the stale PLAYBOOK §8
  text still be in the repo?** Neither is current; both are surrounded
  by "stale" notices but not removed. A fresh reader cannot tell from
  inside either file alone that it does not represent current
  practice. (This audit does not propose action — flagging only.)

- **How heavy is the bundle in practice?** Three full governance docs
  + audit findings + a tree dump + Stage 2 response is a non-trivial
  upload. Whether the NEW chat's context budget actually fits all
  of it before synthesis, and whether the synthesis quality reflects
  having read it, is not observable from files alone.

- **Does the Q&A loop (Stage 2.5) fire often, never, or only when the
  architect's response was thin?** It was added on 2026-05-09 night
  after the first end-to-end test surfaced cases where the NEW chat
  had unanswered questions. No instance is yet visible in any bundle
  (no `stage2-amendments.md` files exist in any archive folder I
  inspected). Whether it gets used would tell us whether Stage 2 is
  consistently good enough on the first pass.

- **Is the per-handoff cost worth it for small sessions?** The
  three-stage relay plus an 11-file bundle plus validators and a
  commit is heavy if the next session is a small one. The flow makes
  no distinction between a session-sync covering one decision and an
  audit-sync covering eight findings. Whether a lighter variant
  would degrade or help is an open question; the spec currently
  treats every handoff the same.
