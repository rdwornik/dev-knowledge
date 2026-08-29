Research and measurement complete. Here is the artifact.

**Lane declaration:** read-only. No commit, no push, no backlog row, no `tasks/` edit, no intake, no ADR draft. `git status` untouched. **Environment:** the container carries `uv 0.8.17` against the repo's pinned `==0.11.19`, so I ran **no gates**; every number below comes from `python3` and `grep` over the working tree, and I say so at each one.

```
=====================================================================
AUT-R2 — DECISION-QUALITY FRAMEWORKS IN SOFTWARE ENGINEERING
Pattern catalog with sources + fit-assessment
Arc: AUTONOMY · dispatched 2026-08-29 · substrate: cloud, read-only
=====================================================================

HOW TO READ THIS
- Evidence tier on every claim: [MEASURED] a study or reported result ·
  [PRACTICED] organizations do it, no measurement · [ASSERTED] someone
  recommends it.
- Verdict enum, exactly three: already-have-it · partial · absent.
- Sources are real and were checked this session against live search
  results. Where I could not verify, the line says "no source found"
  and the item is labelled a hypothesis. Direct arxiv.org and
  idl.iscram.org fetches were BLOCKED by the egress proxy, so a few
  citations below rest on search-result metadata rather than on my
  having opened the paper — each of those is flagged
  [METADATA-ONLY: verify before citing in an ADR].

---------------------------------------------------------------------
PART 0 — WHAT I MEASURED IN THIS REPO (numbers, not impressions)
---------------------------------------------------------------------

Method: python3 + grep over the working tree, 2026-08-29. No gates run.

A. ADR corpus size
   88 files match docs/decisions/ADR-*.md. Two of those are amendment
   files (ADR-51-amendment-..., ADR-70-amendment-...), so ~86 distinct
   ADR numbers, running 27..115 with gaps.

B. Considered-options coverage — THE HEADLINE NUMBER
   57 of 88 files (64.8%) carry a heading matching /^#{1,4} .*Alternativ/.
   Exact heading strings, counted:
     43  "## Alternatives considered"
      3  "## Alternatives rejected"
      1  "## §9 Alternatives considered"
      1  "## §4 — Alternatives considered and rejected, with their
          recorded reasons"
      1  "## Alternatives considered (the #86.2 operator fork)"
      1  "## 10. Alternatives considered"
   (the remainder match on sub-headings inside a decision body)

C. Is it a template obligation or a habit? — IT IS A HABIT.
   templates/ADR-template.md, final section, verbatim:
     "## Alternatives considered
      <Optional. What else was evaluated and why it was not chosen?>"
   The word is "Optional". Nothing gates it: I found no audit check
   and no pre-commit hook asserting the section's presence. So 64.8%
   compliance is 64.8% VOLUNTARY compliance — which, against the
   published base rate (see axis 2), is unusually high.

D. Depth of the sections that exist (n=57)
   median 104 words · mean 115 · min 16 · max 350
   4 sections under 40 words (thin: ADR-73 @16, ADR-74 @17,
     ADR-75 @22, ADR-57 @29)
   12 sections at or above 150 words
   51 of 57 enumerate 2 or more distinct options
   Deepest: ADR-112 (350 w), ADR-107 (269), ADR-104 (236),
     ADR-115 (227), ADR-101 (221)

E. Coverage TREND by ADR number — this is the finding, not (B)
   ADR-27..59   13/31  (42%)
   ADR-60..79   18/21  (86%)
   ADR-80..99   17/20  (85%)
   ADR-100..115  9/16  (56%)
   The practice was learned (42% -> 86%), held for 40 ADRs, and has
   DECAYED by 30 points in the most recent block. That is the classic
   ritual-decay curve from the premortem/checklist literature showing
   up in this repo's own corpus, and it is visible only because the
   section is optional — a mandated section would have decayed into
   ceremony instead, which is harder to detect.

F. Absence search (grep, whole tree excluding .git, *.md/*.py/*.yaml)
   "premortem"            0 files
   "pre-mortem"           1 file  (docs/archive/2026-08-09-research-
                                   session-continuity-decision-
                                   lifecycle-wf-fafd931b.md)
   "prospective hindsight" 1 file (same)
   "devil's advocate"     0 · "tenth man" 0 · "red team" 0
   "sunk cost" 0 · "planning fallacy" 0 · "confirmation bias" 0
   "base rate" 0 · "inter-rater" 0
   "reference class"      1 file (same archive file, and there it means
                                  "hub-reference classes" — a FALSE
                                  POSITIVE; the forecasting sense
                                  appears in that file's Klein citation
                                  only)
   "cognitive bias"       4 files, ALL handoff bundles, all the same
                          relayed ai-council objective line
   "dissent"              7 files
   "LLM-as-judge"         3 files
   ("anchoring" 101 and "calibrat" 123 are dominated by JOURNAL-anchor
    and gate-calibration senses — not decision-quality usage.)

G. Intake corpus: 56 docs under docs/intake/. NONE is about decision
   quality, debiasing, dissent, or judgment. Confirmed by title scan
   plus the "cognitive bias" grep above.

---------------------------------------------------------------------
PART 1 — THE SIX AXES
---------------------------------------------------------------------

=====================================================================
AXIS 1 — PREMORTEMS
=====================================================================

WHAT IT IS
Gary Klein's technique: before committing, the team is told the plan
HAS FAILED, twelve months on, and each member independently writes why.
The mechanism is "prospective hindsight" — an event framed as settled
is explained more richly than one framed as uncertain.

WHO ACTUALLY DOES IT
- Klein, "Performing a Project Premortem," Harvard Business Review,
  September 2007. The canonical statement. [PRACTICED/ASSERTED]
- Atlassian Team Playbook ships "Pre-Mortem" as a named, templated Play
  alongside Retrospective / Health Monitor, at
  atlassian.com/team-playbook/plays/pre-mortem. This is the clearest
  case of INSTITUTIONALIZATION in software engineering I can evidence:
  a facilitated ritual with a template and a defined output, published
  by a vendor and used internally. [PRACTICED]
- Beyond Atlassian, published engineering institutionalization is
  THINNER than its reputation. Most citations are consultancy blogs
  recommending it. I found no engineering-org study reporting standing
  premortem practice with outcomes. NO SOURCE FOUND for "company X has
  run premortems on every project for N years and here is what
  happened" — treat any such claim as a hypothesis.

EVIDENCE IT WORKS
- Mitchell, Russo & Pennington, Journal of Behavioral Decision Making
  2(1):25-38 (1989): prospective hindsight increases correct
  identification of reasons for future outcomes by ~30%. This is the
  foundation result and it is about REASON GENERATION, not outcomes.
  [MEASURED, 1989 — old]
- Veinott, Klein et al., "Evaluating the effectiveness of the PreMortem
  technique on plan confidence," ISCRAM 2010 (Seattle). N=178
  evaluating an H1N1 pandemic plan; conditions were premortem vs
  critique vs pro/con vs cons-only vs baseline. Result: the premortem
  reliably reduced confidence MORE than every other condition.
  [MEASURED, 2010] [METADATA-ONLY: the PDF host is egress-blocked from
  this container; N, conditions and the direction of the result come
  from search-result text, not from my reading the paper.]

THE HONEST LIMIT, AND IT MATTERS
The measured outcome is REDUCED OVERCONFIDENCE AND MORE FAILURE MODES
SURFACED. It is NOT "fewer failed projects." No controlled study
demonstrates premortems improve real-world project outcomes. Anyone
selling a premortem as an outcome intervention is over-reading a
confidence-calibration result. [MEASURED-limits]

COST: 30-90 minutes of a group's time, once per plan.
FAILURE MODES: (1) run once as a workshop and never again — the decay
mode; (2) surfaces risks nobody then owns, so the list is theatre;
(3) held after the decision is socially locked, making it ratification
with extra steps; (4) facilitator anchors the failure list.

TRANSFER TO ONE-HUMAN / MANY-AGENT
Transfers WELL, and arguably better than to humans, for a specific
reason: the human premortem's active ingredient is defeating social
reluctance to voice doubt. An agent has no such reluctance, so the
ritual's cost collapses to tokens. But the SAME collapse removes its
diagnostic value — an agent asked "why did this fail" will always
produce a fluent list, whether or not the plan is bad. The human
version's signal is partly "someone was willing to say it"; the agent
version has no such signal and must be judged on content alone.
The correct one-operator form is therefore NOT a meeting but a
CONTRACT SECTION: an ex-ante "assume this lane failed — enumerate why"
block, written before the lane is dispatched, whose output is
adjudicated rather than filed.

=====================================================================
AXIS 2 — ADR CONSIDERED-OPTIONS PRACTICE
=====================================================================

WHAT IT IS
Michael Nygard's original ADR form (2011, "Documenting Architecture
Decisions") is deliberately minimal: Title, Status, Context, Decision,
Consequences. NOTE: Nygard's original has NO alternatives section. The
options discipline is a LATER addition — MADR (Markdown Any Decision
Records, adr.github.io) introduced "Considered Options" plus
"Decision Drivers" and per-option pros/cons; Y-statements
(Zimmermann) compress the same into one sentence. [PRACTICED]

WHAT THE LITERATURE ACTUALLY MEASURES
- Ding et al. (2014) surveyed ~2000 open-source projects and found
  architectural RATIONALE is rarely recorded, attributing it to the
  tension between documentation overhead and agile delivery.
  [MEASURED, 2014 — old]
- A GitHub-mining result reported in current ADR literature: adoption
  is low but rising, and ~50% of repositories that have ADRs have
  between one and five — i.e. the concept is TRIED and abandoned far
  more often than it is sustained. [MEASURED]
  [METADATA-ONLY: I could not open the source paper; the figure came
  through search-result text. Verify the exact study before citing.]
- Ahmeti et al. (2024), "Architecture Decision Records in Practice: An
  Action Research Study" — industrial case study in a microservice
  environment; seven core challenges across documentation culture,
  distributed system parts, knowledge transfer, prioritization.
  [MEASURED, 2024]
- "One Size Fits All? An Empirical Comparison of ADR Templates
  regarding Comprehension, Usability, and Ease of Adoption"
  (arXiv 2604.27333, 2026) — the first head-to-head empirical
  comparison of ADR TEMPLATES I can find. [MEASURED, 2026]
  [METADATA-ONLY: arxiv.org is egress-blocked here; I have title and
  framing, not results. This is the single most relevant external
  paper to axis 2 and I could not read it — flagging it as the top
  follow-up fetch.]

IS THERE MEASUREMENT OF ADR QUALITY IN THE WILD?
Barely. What exists measures ADOPTION (do repos have ADRs, how many)
and PRACTITIONER EXPERIENCE (interviews, action research). I found no
published metric of whether an ADR's options section genuinely weighed
alternatives. So: this repo's Part-0 measurement is, as far as I can
evidence, a MORE quantitative statement about one ADR corpus's options
practice than the published literature offers about any corpus. That
is a small, real, defensible novelty.

WHAT DISTINGUISHES WEIGHED FROM CEREMONIAL
From the corpus itself rather than from the literature, three
discriminators, all checkable:
  (1) Does a rejected option carry an argument that could have won?
      ADR-112's "Keep the single bar" does — it is recorded as "the
      position with a real argument" and as leg 1 of the fork test.
      That is the shape of a genuine weighing.
  (2) Is the rejection reason SPECIFIC to this decision, or generic?
      "Rejected: more complex" is ceremony. ADR-112's "the bar's cost
      is paid per-candidate while its benefit accrues only to
      code-impacting candidates" is not.
  (3) Word count is a weak proxy and I will not overclaim it — but
      the 4 sections under 40 words (ADR-73/74/75/57) cannot be doing
      (1), and 51 of 57 enumerating 2+ options means the corpus is
      mostly not single-option-with-a-nod.

COST: 20-60 minutes per ADR of genuine option authoring.
FAILURE MODES: post-hoc rationalization (options written after the
decision, chosen to lose); the "straw alternative"; and decay — which
this corpus is currently exhibiting (Part 0E).

TRANSFER: transfers fully. An ADR is already a single-author artifact.

=====================================================================
AXIS 3 — RED TEAMS AND DESIGNATED DISSENT
=====================================================================

THE MOST VALUABLE THING ON THIS AXIS IS THE APPOINTED-vs-AUTHENTIC
DISTINCTION, AND IT IS MEASURED, NOT ASSERTED.

- Schulz-Hardt, Jochims & Frey, "Productive conflict in group decision
  making: genuine and contrived dissent as strategies to counteract
  biased information seeking," Organizational Behavior and Human
  Decision Processes 88(2), July 2002. Design: three-person groups,
  either homogeneous (all favour the same option) or heterogeneous
  (a real minority faction) — that is GENUINE dissent; crossed with
  use/non-use of devil's advocacy — that is CONTRIVED dissent.
  RESULT: heterogeneity was MORE effective at preventing confirmatory
  information-seeking than devil's advocacy was. [MEASURED, 2002]

- Nemeth et al., "Devil's advocate versus authentic dissent:
  stimulating quantity and quality," European Journal of Social
  Psychology 31(6):707-720 (2001); companion, Nemeth, "Improving
  decision making by means of dissent," Journal of Applied Social
  Psychology 31(1):48-58 (2001). RESULT: authentic dissent produced a
  greater proportion of original thoughts, more consideration of the
  opposite position, and direct attitude change. Devil's advocacy
  produced COGNITIVE BOLSTERING of the initial position — i.e. the
  appointed critic can make the group MORE confident in what it
  already thought. [MEASURED, 2001]

  Read that again: THE APPOINTED DEVIL'S ADVOCATE CAN BACKFIRE. The
  mechanism offered is that a role-player's commitment is ambiguous,
  so the group discounts the objection and treats having heard it as
  having answered it.

- Schwenk, "Effects of devil's advocacy and dialectical inquiry on
  decision making: a meta-analysis," Organizational Behavior and Human
  Decision Processes 47(1):161-176 (1990). RESULT: devil's advocacy
  beat the expert/no-conflict approach in general; dialectical
  inquiry's superiority was NOT demonstrated on ill-structured tasks;
  and NEITHER technique was shown superior to the other. [MEASURED,
  1990 — old, and note it partly cuts the other way from Nemeth: DA
  beats no-conflict even if it loses to authentic dissent.]

THE "TENTH MAN"
Widely repeated as an Israeli intelligence doctrine after the 1973 Yom
Kippur War, and popularized by the film World War Z. I could NOT verify
a primary source establishing it as codified doctrine. NO SOURCE FOUND
for a primary document. Treat as folklore that encodes a real idea, not
as a citable institution. [ASSERTED — hypothesis]

SECURITY RED-TEAMING'S TRANSFER TO DESIGN REVIEW
[PRACTICED]. Real and widespread as a practice; I found no measurement
of design-review red-teaming's effect on decision quality specifically.

COST: an appointed dissenter is nearly free; an AUTHENTIC dissenter is
expensive because you cannot appoint one — you have to have hired,
retained and protected someone who actually disagrees.
FAILURE MODES: bolstering (measured, above); the advocate becoming
socially costly and quietly dropped; dissent-as-ritual where the
objection is heard and unrecorded.

TRANSFER TO ONE-HUMAN / MANY-AGENT — THIS IS THE SHARPEST TRANSLATION
IN THE WHOLE ARTIFACT
The entire measured advantage of authentic over appointed dissent
turns on the dissenter genuinely holding a different position. A
prompted "you are the critic" agent is, definitionally, CONTRIVED
dissent — the exact condition Nemeth measured as inferior and
potentially bolstering. A single-model critic role is therefore the
WEAK form, and this repo should stop treating a prompted critic as
equivalent to a second opinion.
The strong analogue of AUTHENTIC dissent for an agent fleet is
HETEROGENEITY OF THE UNDERLYING MODEL — a different vendor, different
training, genuinely different priors. Schulz-Hardt's heterogeneous
group is a cross-vendor panel; his homogeneous group with a devil's
advocate is one model told to argue.
That is not a metaphor stretched to fit. It is why the Codex terra
lane (below) is the strongest decision-quality organ this repo owns,
and why it is stronger than any prompt-role critic could be.

=====================================================================
AXIS 4 — DIALECTIC / DEBATE PROTOCOLS FOR LLM AGENTS
=====================================================================
THIS IS THE AXIS WITH THE WORST HYPE-TO-EVIDENCE RATIO. Negatives
first, deliberately.

THE NEGATIVE FINDINGS (all [MEASURED])
- "Large Language Models Cannot Self-Correct Reasoning Yet"
  (arXiv 2310.01798, 2023) contains a section titled, literally,
  "Multi-Agent Debate Does Not Outperform Self-Consistency," comparing
  the two head-to-head on GSM8K. Multi-agent debate significantly
  UNDERPERFORMS plain self-consistency majority voting at an equivalent
  number of sampled responses.
- "If Multi-Agent Debate is the Answer, What is the Question?"
  (arXiv 2502.08788, Feb 2025; later revised under the title "Stop
  Overvaluing Multi-Agent Debate"). Evaluated five representative MAD
  methods across 36 experimental configurations: NONE achieved a win
  rate above 20% against plain chain-of-thought, "often performing
  worse despite consuming significantly more tokens."
- "Should we be going MAD? A Look at Multi-Agent Debate Strategies for
  LLMs" (OpenReview) — comparative study across medical and
  non-medical datasets, same sceptical direction.
- "Stay Focused: Problem Drift in Multi-Agent Debate"
  (arXiv 2502.19559, 2025) — names PROBLEM DRIFT as a distinct failure:
  the debate wanders off the question it was convened to answer.
- Sycophancy: Sharma et al. (Anthropic), "Towards Understanding
  Sycophancy in Language Models," arXiv 2310.13548 (2023). Five
  state-of-the-art assistants exhibit sycophancy across four
  free-form tasks, AND analysis of human preference data shows that
  matching a user's stated view is one of the MOST PREDICTIVE features
  of a human preference judgment — i.e. the training signal itself
  rewards agreement. Agent-to-agent agreement is not a bug someone
  forgot to fix; it is downstream of the objective.
- The repo's own banked 2026-04-24 report already lists error
  amplification, false consensus and cost/latency blowup as production
  challenges [PRACTICED/ASSERTED].

THE POSITIVE FINDINGS, WHICH ARE NARROWER THAN THE FIELD IMPLIES
- Khan et al., "Debating with More Persuasive LLMs Leads to More
  Truthful Answers," ICML 2024 (PMLR 235:23662-23733, arXiv 2402.06782).
  RESULT: debate raised non-expert accuracy to 76% (model judge) and
  88% (human judge) against naive baselines of 48% and 60%. [MEASURED]
  READ THE SETUP BEFORE GENERALIZING: this is an information-asymmetric
  setting — expert debaters who can see a passage, a judge who cannot.
  It is evidence that debate helps a WEAK JUDGE ADJUDICATE STRONG
  ARGUERS. It is NOT evidence that two peers arguing improves the
  answer, which is the configuration the negative results above test
  and reject.
- Bai et al., "Constitutional AI: Harmlessness from AI Feedback,"
  arXiv 2212.08073 (2022) — the critique-and-revise loop, then RLAIF.
  Works, and is shipped. But note what it is: a SELF-critique against
  an EXPLICIT WRITTEN PRINCIPLE SET, not a debate between peers. The
  active ingredient is the constitution, not the plurality.
- Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot
  Arena," NeurIPS 2023 Datasets & Benchmarks (arXiv 2306.05685):
  a strong judge model reaches >80% agreement with human preference —
  "the same level of agreement between humans." [MEASURED]

THE SYNTHESIS, STATED PLAINLY
The measured pattern across all of it: PLURALITY BUYS LITTLE;
ASYMMETRY AND HETEROGENEITY BUY A LOT. Debate among same-model peers
loses to self-consistency at equal cost. Debate helps when one side
holds information or capability the judge lacks. Critique helps when
it is anchored to a written standard. Anything that makes agents more
alike makes the ensemble worse, and RLHF-trained agents are already
biased toward agreeing.

COST: MAD is 4-15x tokens for effects the sceptical papers cannot
reliably detect. This is the axis where cost blowup for marginal gain
is documented rather than feared.

=====================================================================
AXIS 5 — COGNITIVE-BIAS CHECKLISTS IN ENGINEERING DECISIONS
=====================================================================

THE DEBIASING LITERATURE IS MORE NEGATIVE THAN PRACTITIONERS THINK,
WITH ONE IMPORTANT EXCEPTION.

THE NEGATIVE CORE
Awareness does not debias. The standing result in the judgment-and-
decision-making literature is that telling people about a bias, or
warning them, produces little durable change; Fischhoff's classic
debiasing taxonomy separates "warn the judge" (weakest) from
"restructure the task" (strongest). I am stating this at [ASSERTED]
strength rather than pinning it to one study, because I did not verify
a single canonical citation for it this session. Do not put a specific
paper behind this sentence without checking.

THE EXCEPTION, AND IT IS REAL
- Morewedge, Yoon, Scopelliti, Symborski, Korris & Kassam, "Debiasing
  Decisions: Improved Decision Making With a Single Training
  Intervention," Policy Insights from the Behavioral and Brain
  Sciences (2015). Two longitudinal experiments; a SINGLE intervention
  (a computer game, or an instructional video) targeting bias blind
  spot, confirmation bias and fundamental attribution error produced
  effects reported at Cohen's d > 1 that held at 2 months. [MEASURED,
  2015]
- Sellier, Scopelliti & Morewedge, "Debiasing Training Improves
  Decision Making in the Field," Psychological Science (2019) —
  the field follow-up. [MEASURED, 2019]
  So: TRAINING WORKS BETTER THAN CHECKLISTS in the one place it has
  been measured well. That is an inconvenient result for anyone whose
  plan is "add a checklist."

REFERENCE-CLASS FORECASTING — THE STRONGEST ITEM ON THIS AXIS
- Kahneman & Tversky's outside view, operationalized by Bent Flyvbjerg.
  The UK Treasury Green Book was revised in 2003 to require explicit,
  empirically based optimism-bias adjustments; in summer 2004 the UK
  Department for Transport and HM Treasury adopted reference class
  forecasting, appointing Flyvbjerg (with COWI) to produce optimism-
  bias uplifts per reference class. First application: Edinburgh Tram
  Line 2, 2004, against a reference class of 46 comparable rail
  projects. DfT typically accepts the 80th percentile — a 20% risk of
  overrun. In use on major UK transport projects since. [MEASURED /
  PRACTICED AS GOVERNMENT POLICY, 2003-2004, still live]
  This is the single best-institutionalized debiasing mechanism in the
  entire catalog: a named bias, a named countermeasure, mandated in
  national policy, with published uplift numbers. It is also the one
  that works by RESTRUCTURING THE TASK rather than warning the judge —
  which is exactly what the debiasing literature predicts.

CHECKLISTS: THE HONEST RECORD, INCLUDING THE REPLICATION FAILURE
- Haynes et al., "A Surgical Safety Checklist to Reduce Morbidity and
  Mortality in a Global Population," NEJM 2009: eight hospitals,
  3,733 patients before / 3,955 after; 30-day mortality 1.5% -> 0.8%,
  any complication 11% -> 7%. [MEASURED, 2009]
- Urbach et al., "Introduction of Surgical Safety Checklists in
  Ontario, Canada," NEJM 2014: 101 hospitals, 109,341 procedures
  before / 106,370 after. Mortality 0.71% -> 0.65%, OR 0.91, P=0.13 —
  NOT SIGNIFICANT. The flagship checklist result DID NOT REPLICATE at
  system-wide scale. [MEASURED, 2014]
  The accepted reading is that mandated rollout produced compliance
  without fidelity — the checklist was performed, not used. That is
  the ritual-decay failure mode with 100,000 data points behind it,
  and it is the best argument in this catalog against MANDATING a
  decision ritual as opposed to earning its use.

WHO OPERATIONALIZED BIAS CHECKS AS AN ACTUAL PROCESS STEP?
Reference-class forecasting in UK transport appraisal: yes, verified.
Beyond that, engineering-specific bias checklists wired into a decision
process: NO SOURCE FOUND that survives scrutiny. The posters exist;
the process steps mostly do not.

TRANSFER TO ONE-HUMAN / MANY-AGENT — SAY IT PLAINLY, THIS ONE IS
PARTLY A MISMATCH
Anchoring, sunk cost, planning fallacy and confirmation bias are
properties of a HUMAN decision-maker under commitment and ego. In this
repo there is exactly one such decision-maker — the operator — and the
biases that actually bind are the operator's, not the agents'. Agents
have DIFFERENT pathologies (sycophancy, confabulated locators, fluent
wrongness) that the human bias taxonomy does not name and does not
address. So:
  - Human-bias checklists transfer to the OPERATOR'S functional
    rulings (ADR-108 §A item 1) and essentially nowhere else.
  - Reference-class forecasting transfers COMPLETELY and is the best
    fit in the catalog, because the repo already has the reference
    class: a JOURNAL of every prior arc, and an audit corpus. "How
    long did the last five arcs of this shape actually take, and what
    did they cost" is an outside-view question this repo can answer
    from its own history and currently does not ask.
  - An agent bias checklist is largely a category error and I would
    not build one.

=====================================================================
AXIS 6 — MULTI-AGENT DISAGREEMENT ARCHITECTURES
=====================================================================

THE QUESTION THAT SEPARATES ARCHITECTURES: WHERE DOES A MINORITY
POSITION GO?

Three observed topologies, ordered by how much disagreement survives:

(1) VOTE-AND-DISCARD. N agents answer, majority wins, minority is
    gone. Self-consistency (Wang et al., "Self-Consistency Improves
    Chain of Thought Reasoning," ICLR 2023) is the honest, cheap,
    strong version — and per axis 4 it BEATS debate at equal budget.
    [MEASURED] Disagreement is not represented at all; it is averaged
    into a count. Cheapest, and for many tasks best.

(2) SYNTHESIZE-WITH-DISSENT-SUMMARY. A distinct synthesizer reads the
    panel and writes a verdict that names the dissent. This is what
    this repo's AI Council does (see fit-assessment). Disagreement is
    REPRESENTED but its preservation depends on the synthesizer's
    diligence, and the synthesizer is the same class of model as the
    panel. [PRACTICED]

(3) ASYMMETRIC ADJUDICATION. Arguers and judge have different
    information or capability; the judge rules and the arguments are
    retained. Khan et al. 2024 (axis 4) is the measured instance.
    [MEASURED]

WHO BREAKS A TIE, AND ON WHAT AUTHORITY? This is the question the
research literature is WEAKEST on and this repo is STRONGEST on. The
MAD papers overwhelmingly resolve by majority vote or by a judge model
— authority by construction, never by legitimacy. Nothing in the
literature I found asks who is ENTITLED to rule. ADR-108 §A does ask,
and answers by KIND OF QUESTION. That is, as far as I can evidence, an
unusual design.

HOW IS A MINORITY POSITION PRESERVED? Almost nowhere in the LLM
literature. Preserved dissent is a governance practice (US Supreme
Court dissents; IPCC minority statements; the NTSB's dissenting-opinion
record) far more than an ML one. [PRACTICED]

COST: (1) is N samples. (2) is N samples plus a synthesis pass plus a
human read. (3) is the most expensive and the only one with a measured
win.
FAILURE MODES: (1) loses the one right answer to four confident wrong
ones — and axis 4's sycophancy result says the four will tend to
agree; (2) synthesizer sycophancy toward the majority, and dissent
"summarized" into invisibility; (3) judge-model bias (axis 4/Zheng).

---------------------------------------------------------------------
PART 2 — FIT-ASSESSMENT AGAINST ORGANS THAT ALREADY EXIST HERE
---------------------------------------------------------------------
Verdicts use the enum exactly. Every locator below I opened.

P1. PREMORTEM / EX-ANTE FAILURE ENUMERATION      VERDICT: absent
    Searched: 0 files contain "premortem"; 1 contains "pre-mortem" and
    it is a CITATION inside a research archive, not an organ
    (docs/archive/2026-08-09-research-session-continuity-decision-
    lifecycle-wf-fafd931b.md, the "Q3 — Plan-and-outcome continuity"
    section, which cites Klein 2007 and Mitchell/Russo/Pennington 1989).
    NEAREST ORGANS, and they are close but not this:
      - ADR-81's frozen ex-ante acceptance contract (docs/decisions/
        ADR-81-feature-lifecycle-definition-of-done.md) fixes what
        SUCCESS means before the build. A premortem fixes what FAILURE
        would look like. Complementary, not the same.
      - ADR-112's "Consequences / Harder, and named rather than
        minimized" and its "Honest limits" section do enumerate how the
        decision could go wrong — that is a premortem's output shape
        appearing as an ADR convention. It is the strongest existing
        trace and it is a HABIT of good ADR authoring, not an organ.

P2. ADR CONSIDERED-OPTIONS                       VERDICT: partial
    Organ: docs/decisions/ADR-*.md + templates/ADR-template.md.
    Present at 57/88 files (64.8%), median 104 words, 51/57 enumerate
    2+ options (Part 0B/0D).
    PRECISELY WHAT IS MISSING, three things:
      (a) It is OPTIONAL in the template — verbatim "<Optional. What
          else was evaluated and why it was not chosen?>" — and no
          gate asserts it. Compliance is voluntary.
      (b) There is no quality discriminator, only presence. Four
          sections are under 40 words and cannot be weighing anything.
      (c) THE DECAY IS MEASURED AND UNNOTICED: 86% -> 85% -> 56%
          across the last three blocks (Part 0E). Nothing surfaces it.
    Related and correct: ADR-94 narrows immutability so only an ADR's
    STATUS LINE is editable in place (docs/decisions/
    ADR-94-adr-status-line-mutable-on-ratification.md, "## Decision":
    "The immutability rule is narrowed to distinguish decision content
    from the status line"). ADR-112 shows the cost of that narrowness
    done right — it could not retract its own "this ADR is Proposed"
    section, so it appended a RATIFICATION MARKER and left the wrong
    text byte-unchanged, citing STANDING_RULINGS B6. That is a
    decision-quality practice in its own right: the record of the gap
    between promotion and ratification is preserved rather than tidied.

P3. HETEROGENEOUS SECOND READER (the authentic-dissent analogue)
                                                 VERDICT: already-have-it
    Organ: the Codex review lanes. protocols/PLAYBOOK.md, the
    Codex-lane bullet reading "terra is the doctrinal default review
    lane, and BOTH lanes now pin it explicitly" — with the provenance
    stated in the same bullet: the pin exists because an unpinned run
    the operator asked for as terra silently EXECUTED as sol, with
    nothing in the artifact recording which model had run. Task
    tasks/469-codex-review-code-lane-runs-an-unpinned-model.md carries
    the closure: the code lane now pins gpt-5.6-terra and the artifact
    frontmatter records "Model used" + "Review profile".
    WHY THIS IS THE STRONGEST DECISION-QUALITY ORGAN IN THE REPO:
    per axis 3, cross-vendor heterogeneity is the agent analogue of
    Schulz-Hardt's HETEROGENEOUS GROUP — the condition measured as
    superior to devil's advocacy. A different vendor's model has
    genuinely different priors; a prompted critic does not. The repo
    arrived at the measured-best structure. Also note PLAYBOOK's
    dispatch requirement that every plan NAME its Codex lane per task
    — that converts reviewer choice from a runtime accident into a
    recorded, addressable decision, which is the reproducibility half
    of the same idea.
    Live proof it produces real dissent rather than agreement:
    docs/audits/2026-08-28-technical-nb2-a-packet.md, "Reviewer
    dissent, recorded rather than buried" — terra rated a hold
    CRITICAL against the packet's own position, the disagreement is
    named "genuine", and it is escalated as C-1 rather than overridden.
    That is preserved minority position, in production, with a locator.

P4. APPOINTED / PROMPTED DISSENT                 VERDICT: partial
    Traces: the conformance-hub skill runs "an adversarial skeptic
    [that] kills false positives"; docs/archive/2026-04-24-multi-agent-
    debate-patterns.md banks proposer/critic/synthesizer.
    WHAT IS MISSING: nothing records that a prompted critic is the
    CONTRIVED form Nemeth measured as inferior and potentially
    bolstering. The repo uses both forms and treats them as the same
    kind of thing. The gap is doctrinal, not mechanical.

P5. DEBATE WITH DISSENT-CARRYING SYNTHESIS       VERDICT: already-have-it
    Organ: protocols/AI_COUNCIL_PROCESS.md v2.2. Three mechanisms
    there are genuine decision-quality engineering and each is better
    than its reputation:
      (a) SYNTHESIZER EXCLUSION (Stage 3, runner.exclude_synthesizer_
          from_panel, ADR-01) — the synthesizer is dropped from the
          panel before debate starts and "never participates on the
          panel". This is a structural defence against exactly the
          SELF-ENHANCEMENT BIAS Zheng et al. 2023 measured (GPT-4 +10%,
          Claude +25% preference for their own outputs). The repo built
          the countermeasure; I found no note that it knows why it
          works.
      (b) BLIND VOTE (Stage 3, _anonymize_responses(), ADR-03) —
          "Round 2 anonymises responses before voting". That is an
          anti-anchoring and anti-authority mechanism, structural
          rather than exhortative, i.e. Fischhoff's strong form.
      (c) DISSENT IS READ, NOT COUNTED (Stage 4, "How to read the
          vote") — verbatim: "A 3-2 split with strong dissent
          reasoning is not the same as a 4-1 with weak dissent; read
          the dissent before treating the majority as binding."
    Against axis 6's taxonomy this is topology (2), and it is a
    well-built (2).
    THE KNOWN GAP IS ALREADY RECORDED IN THIS REPO, and I did not
    have to derive it: docs/handoffs/2026-07-02-ai-council-architect/
    RESIDUAL.md, finding G7 — "minority report is not a first-class
    output (dissent buried in the synthesis narrative)." That is the
    exact axis-6 weakness of topology (2), self-diagnosed in 2026-07
    and still open.

P6. DECISION-AUTHORITY ROUTING BY KIND           VERDICT: already-have-it
    Organ: ADR-108 §A (docs/decisions/ADR-108-decision-routing-and-
    engineering-standards.md), items 1-4: operator rules FUNCTIONAL
    questions; architect rules TECHNICAL ones in its own lane and
    "relies on revertability instead of escalation"; AI Council is the
    distillation organ for genuinely CONTESTED technical decisions;
    and the retired anti-pattern — "presenting the operator with option
    menus of technical forks."
    ASSESSMENT: I found nothing comparable in the decision-quality
    literature. The MAD papers resolve ties by vote or judge-model;
    none asks by what AUTHORITY. Routing by KIND OF QUESTION, with
    revertability rather than escalation as the standard for
    uncertainty, is a genuinely unusual design and it is the correct
    shape for a one-human fleet — it puts the scarce human where only
    a human can rule and nowhere else.
    HONEST LIMIT, and the ADR states it itself: "§A is doctrine, not
    mechanism. It routes authority; it arms no gate. Nothing in this
    repo mechanically detects an option-menu brief or an escalated
    technical question."

P7. RECORDED REJECTION AS ANTI-RELITIGATION      VERDICT: already-have-it
    Organs: ADR-111 §1(d) REJECTED, "recorded with its reason, and not
    relitigated"; docs/intake/README.md §5's "REJECTED (reason, kept)"
    with byte-identical relocation to docs/intake/archive/; and
    protocols/ENVIRONMENT.md's "Rejected (do NOT revisit before Q3)"
    list.
    That ENVIRONMENT list is a better artifact than it looks, for two
    reasons. First, it holds "Mandatory TDD (council rejected)" WITH an
    annotation recording that ADR-108 §B later made TDD standing for
    every build arc — "both facts hold; cite the one that matches the
    scope you are in." Second, it holds a REVERSAL kept visible:
    "~~Codex CLI (no advantage over Haiku subagents)~~ — REVERSED, and
    no longer binding," struck through rather than deleted, with the
    2026-08-28 note that the prior annotation pass fixed one of the
    two homes and left the contradiction standing in the other.
    Against the literature: this is the Rust-RFC / PEP-rejection
    pattern (banked in the 2026-08-09 archive file, Q5) — and this
    repo's version is STRONGER than the reference model, because it
    annotates rather than erases when a rejection is later narrowed or
    reversed. That is a decision-quality practice I did not find
    published anywhere.

P8. THE FINDING FUNNEL (ADR-111)                 VERDICT: already-have-it
    Organ: docs/decisions/ADR-111-finding-triage-pipeline.md §1-§3;
    operationalized as the D4 FUNNEL TABLE in protocols/PLAYBOOK.md's
    wave close (D0-D5), with five classifications each citing its
    clause.
    ASSESSMENT AS A DECISION-QUALITY MECHANISM IN ITS OWN RIGHT — and
    it deserves one, because it is the most unusual thing here:
      - It is a FORCED-CHOICE CLASSIFIER over findings, and its
        anti-degeneracy clause is the part with no analogue I could
        find: "a triage pass that routes most items to (c) has not
        triaged." Most triage schemes fail by routing everything to
        "needs a decision"; this one names that failure as a property
        of the triage rather than of the queue.
      - DISCHARGED requires a resolving locator — verbatim, "'we
        already do that' without a locator is not a discharge." That
        is an evidentiary standard on a disposition, which is rare.
      - It has a measured origin, not an aesthetic one: 153 findings
        and 38 requested rulings from one night batch, with four of
        five lanes independently re-deriving a gap that open row
        [#453] already recorded. It was built against an observed
        consumption failure.
      - Closest published kin is the "audit-finding-to-backlog forcing
        function" the 2026-08-09 archive file recommends (Q8 item 5);
        ADR-111 is strictly stronger, because the forcing function
        only demands a disposition while ADR-111 constrains WHICH
        dispositions exist and bars the direct finding->row path.
    HONEST LIMIT: it governs findings, not decisions. It has no
    equivalent for "a technical fork was ruled" — that is ADR-98/108's
    territory, and the two are not joined by a gate.

P9. DECISION BUDGET / ESCALATION CLASSES         VERDICT: already-have-it
    Organs: protocols/PLAYBOOK.md item 2, "A V-2 decision budget. A
    lane escalates on three classes only: (a) curated-baseline touches,
    (b) genuine rule-vs-ruling conflicts, (c) fork classes with no
    standing ruling"; and protocols/STANDING_RULINGS.md "The decision
    budget (how an agent uses this file)", quoting intake #25
    AMENDMENT-b V-2 verbatim, with the target metric "<=2 operator
    interactions per lane-batch" and the rule "a fork covered by an
    entry below is decided, applied, and reported — not escalated. A
    fork in class (a)/(b)/(c) is batched into one packet, not delivered
    one at a time."
    ASSESSMENT: against axis 6 this is the missing half of every
    published multi-agent architecture — a budget on ESCALATION, not
    just on compute. The MAD literature measures tokens; nothing I
    found measures interruptions of the human. For a one-operator
    fleet the human's attention is the actual scarce resource, and
    this is the only mechanism in the catalog that treats it as such.
    It also implements the batching insight independently: D4's "One
    batched ruling instead of N interruptions is the point."
    HONEST LIMIT: "<=2 operator interactions per lane-batch" is a
    target with, as far as I could find, no organ measuring it. I found
    no surface reporting actual interactions per batch.

P10. RUBRICS / CALIBRATED RATINGS / INTER-RATER RELIABILITY
                                                 VERDICT: absent
    "inter-rater" 0 files. "rubric" hits 100 files but on inspection
    the usages are gate-rubric and audit-trio-rubric senses, not
    scored-rating instruments. "LLM-as-judge" appears in 3 files, all
    as a PROPOSED escalation path never taken (docs/handoffs/
    2026-05-14-.../06_STATE_OF_PLAY.md: "or Stage 3 LLM-as-judge
    auditor"; docs/archive/2026-08-17-research-machine-verifiable-done-
    when-...: "LLM-as-judge scoring against 29148 is emerging ... but
    unproven for gating").
    CRITICAL CONSTRAINT I FOUND AND THE BRIEF DID NOT NAME:
    protocols/ENVIRONMENT.md's Rejected list contains
      "Confidence scoring in council debates (LLMs poorly
       self-calibrate)"
    That is a STANDING COUNCIL REJECTION of exactly the calibrated-
    rating family, and it constrains the fuzzy band directly. Any
    proposal to have agents emit calibrated scores has to answer it.
    It is also, on the evidence, CORRECT — see Part 5.

P11. REFERENCE-CLASS FORECASTING / OUTSIDE VIEW  VERDICT: absent
    "reference class" appears once and in an unrelated sense; "base
    rate" 0; "planning fallacy" 0. There is no organ that answers
    "what happened the last N times we did an arc of this shape."
    The reference class EXISTS — JOURNAL.md, docs/audits/, the task
    corpus — and is not queried as one.

P12. COGNITIVE-BIAS MITIGATION AS AN OBJECT      VERDICT: absent
    See Part 3 — the brief's thin spot, CONFIRMED.

---------------------------------------------------------------------
PART 3 — THE KNOWN THIN SPOT: CONFIRMED, WITH ONE CORRECTION
---------------------------------------------------------------------

CONFIRMED. There is no object in this repo's funnel for cognitive-bias
mitigation. Evidence:
  - "cognitive bias" appears in exactly 4 files, ALL handoff bundles,
    ALL carrying the same relayed ai-council objective line
    ("T1  minimize cognitive bias / raise debate value"):
      docs/handoffs/2026-07-23-ai-council-architect/PASTE_THIS.md:579
      docs/handoffs/2026-07-23-ai-council-architect/SUPPLEMENT.md:62
      docs/handoffs/2026-07-17-.../PASTE_THIS.md:413
      docs/handoffs/2026-07-17-.../SUPPLEMENT.md:77
    A handoff bundle is immutable and is not a funnel object.
  - 56 intake docs, none on the topic. No ADR. No task row. No audit.
  - Per-bias search: "sunk cost" 0, "planning fallacy" 0,
    "confirmation bias" 0, "anchoring" 0 in the bias sense,
    "base rate" 0.

ONE CORRECTION TO THE BRIEF'S FRAMING, offered because the brief asked
me to confirm or refute from my own read: the brief treats axis 5 as
the sole thin spot and axis 1 as unmentioned. In fact AXIS 1 HAS A
TRACE THE BRIEF DID NOT NAME — docs/archive/2026-08-09-research-
session-continuity-decision-lifecycle-wf-fafd931b.md already cites
Klein (HBR 2007) and Mitchell/Russo/Pennington (1989) with the 30%
figure and the correct caveat ("prospective, the conceptual opposite
of carrying a realized outcome forward; cite as complementary, not
direct support"). So the premortem is BANKED AS EVIDENCE and UNBUILT
AS AN ORGAN — a different state from axis 5, which is banked nowhere.
The distinction matters for cost: axis 1's literature review is
already paid for.

---------------------------------------------------------------------
PART 4 — WHAT THIS SURVEY ADDS BEYOND
         docs/archive/2026-04-24-multi-agent-debate-patterns.md
         (a fit-assessment obligation, discharged explicitly)
---------------------------------------------------------------------

I read that file in full (233 lines). What it already holds, which I do
NOT restate: framework landscape (LangGraph / AutoGen / CrewAI / WISE),
the proposer-critic-synthesizer and sequential-peer-review patterns,
WISE's +2-7% weighted-verification gain, LangGraph's 40-50% stateful
cost saving, the five-agent quant-finance case, and — to its credit —
a Competing Perspectives section already naming cost/latency, error
amplification, sycophancy, evaluation complexity, model lock-in, and
"some research even suggests that current MAD methods do not
consistently outperform simpler single-agent strategies."

FIVE THINGS THIS SURVEY ADDS:

(1) THE NEGATIVE CASE, NAMED AND CITED RATHER THAN GESTURED AT. The
    archive file's strongest sceptical line is "some research even
    suggests" with no citation. I can now name the papers and the
    numbers: arXiv 2310.01798's section "Multi-Agent Debate Does Not
    Outperform Self-Consistency"; arXiv 2502.08788's five methods
    across 36 configurations with none exceeding a 20% win rate over
    plain CoT; arXiv 2502.19559 on problem drift. That converts a
    hedge into a finding.

(2) THE RIGHT BASELINE. The archive file benchmarks debate against
    "single-agent." The sceptical literature benchmarks it against
    SELF-CONSISTENCY AT EQUAL SAMPLE BUDGET — and debate loses. The
    2-7% gains the archive file reports are not measured against that
    baseline. This is the single most decision-relevant correction: it
    changes the comparison an adoption decision should run.

(3) THE MECHANISM THAT PREDICTS WHEN DEBATE HELPS. The archive file
    lists patterns without a theory of which wins. Khan et al. 2024
    supplies one: debate helps under INFORMATION ASYMMETRY (76%/88%
    vs 48%/60% naive). Combined with Schulz-Hardt 2002 and Nemeth
    2001 from axis 3, the unifying rule is heterogeneity-and-asymmetry
    over plurality. The archive file's own note that "persona-driven
    debate may degrade accuracy; role-based approaches are preferred"
    is a shadow of this and stops short of the explanation.

(4) SYCOPHANCY WITH A CAUSE, NOT AS A RISK BULLET. The archive file
    lists sycophancy as a challenge. Sharma et al. (arXiv 2310.13548)
    shows it is downstream of the preference objective — matching a
    user's view is among the most predictive features of human
    preference judgments. That reframes it from a bug to be prompted
    away into a property to be architected around, which is a
    different design conclusion.

(5) THE JUDGE-SIDE LITERATURE, ABSENT FROM THE ARCHIVE FILE ENTIRELY.
    Zheng et al. 2023 on position / verbosity / self-enhancement bias,
    and the inter-rater-reliability material in Part 5. The archive
    file says "new evaluation frameworks are needed" and stops; the
    judge literature exists and is where the fuzzy band has to look.

I also note, as a fit-assessment finding: the archive file carries a
2026-08-26 RETENTION header verdict KEEP / exempt-permanent, cited by
6 files, every citer immutable or append-only. It is load-bearing and
should be read alongside this artifact, not replaced by it.

---------------------------------------------------------------------
PART 5 — THE ADR-81 FUZZY BAND (the brief's priority target)
---------------------------------------------------------------------

THE DEFERRAL, VERBATIM, from docs/decisions/ADR-81-feature-lifecycle-
definition-of-done.md:
  "Scope — deterministic only; fuzzy deferred. This binds deterministic
   build tasks, where 'done' can reduce to an exact, executable
   assertion. The fuzzy band — decks, prose, judgment artifacts where
   closure cannot be an exact pass/fail — is explicitly deferred to its
   own arc (it needs a different, non-binary acceptance shape). Naming
   the deferral here keeps it honest rather than silently
   over-claiming."

WHAT THE LITERATURE OFFERS THAT ARC, AND — MORE USEFULLY — WHAT IT
RULES OUT.

RULED OUT (1): AGENT SELF-SCORED CONFIDENCE. Already rejected here
("Confidence scoring in council debates (LLMs poorly self-calibrate)",
protocols/ENVIRONMENT.md Rejected list), and the rejection is
well-founded. Do not reopen it as the fuzzy band's answer.

RULED OUT (2): A NAKED LLM-AS-JUDGE SCORE AS A GATE. Zheng et al. 2023
measured, in the same paper that reports >80% human-level agreement:
position bias, verbosity bias (judges prefer longer answers even when
the extra content is redundant), and self-enhancement bias (GPT-4 +10%,
Claude +25% on their own outputs). This repo's ADR-01 synthesizer
exclusion already defends against the third — which is evidence the
design instinct here is sound and should be generalized, not that the
judge is safe.

THE HARD NUMBER THE ARC NEEDS, AND IT IS NOT ENCOURAGING:
On RUBRIC-satisfaction judgments, reported agreement sits around
kappa 0.366-0.424 across domains, dropping BELOW 0.35 on precisely the
subjective criteria a fuzzy band cares about — "well justified
rationale", "no overlooked flaws". [MEASURED, 2026 — figures from
current LLM-judge/rubric literature surfaced in search; METADATA-ONLY,
arxiv is blocked here, VERIFY BEFORE CITING IN AN ADR.]
Kappa 0.37 is fair-to-moderate agreement. It is not a gate.

AND THE TRAP THAT WOULD OTHERWISE BE WALKED INTO: THE KAPPA PARADOX.
High raw agreement can coexist with near-zero kappa when the base rate
is extreme. A judge that says "pass" on everything scores 90% raw
agreement on a corpus that is 90% passes, and kappa ~0. Since almost
everything this repo ships passes, ANY naive agreement metric on a
fuzzy gate will look excellent and mean nothing. If the fuzzy arc
measures its judge, it must measure chance-corrected agreement, and it
must do so on a deliberately balanced sample including known-bad
artifacts.

WHAT SURVIVES AND IS BUILDABLE:
  (a) ANCHORED RUBRICS OVER SCORES. The measured pattern is that
      agreement collapses on abstract criteria and holds on concrete
      ones. So the fuzzy band's unit should be a CHECKABLE OBSERVATION
      ("every locator in this artifact resolves"; "each rejected option
      carries a reason specific to this decision"), not a 1-5 quality
      rating. This repo already writes acceptance in that shape.
  (b) AUTHOR != VERIFIER, AND HELD-OUT CRITERIA. Already banked in
      docs/archive/2026-08-17-research-machine-verifiable-done-when-
      wf-bfb9405b.md (SpecBench's validation-vs-held-out split;
      EvilGenie on test-file edits; the evaluator-optimizer pattern
      "works only when we have clear evaluation criteria"). That file
      already prescribes the fuzzy band's ESCAPE HATCH — the
      "human_verdict_required: true" marker with a rationale, "so
      unverifiable work is explicitly quarantined rather than faked
      green." What it does NOT supply, and what this survey adds, is
      how to judge the quarantined work once it is quarantined.
  (c) HETEROGENEOUS JUDGE. Per axis 3/4, the defensible non-binary
      verdict comes from a different-vendor reader, which this repo
      already runs (terra) and already lets dissent (the nb2-a packet).
      The fuzzy band's cheapest credible shape is not a new scoring
      system; it is EXTENDING THE EXISTING TERRA LANE TO JUDGMENT
      ARTIFACTS with an anchored checklist and a preserved dissent
      line.
  (d) DISAGREEMENT AS THE SIGNAL. The most useful thing a fuzzy gate
      can emit is not a score but a FLAG THAT TWO READERS DISAGREED.
      Under kappa ~0.37 the agreement is unreliable; the disagreement
      is informative, because it localizes the contested claim. That
      inverts the usual design and is, I think, the right one here.

STATED AS A HYPOTHESIS, NOT A FINDING: I found no published
acceptance-contract formalism for non-binary artifacts in an agent
workflow. The "specification-rigor ladder" in the 2026-08-17 archive
file is explicitly flagged there as "a synthesis, not a single citable
model." If the fuzzy arc builds one, it is building something the
literature does not have — which is worth knowing both for ambition
and for the absence of a template to copy.

---------------------------------------------------------------------
PART 6 — RANKED BY FIT x VALUE, WITH THE CHEAPEST SETTLING EXPERIMENT
---------------------------------------------------------------------
Tier per ADR-112: Tier S = install, 30-minute sandbox try, KEEP or
DELETE, one ledger line either way, NO backlog births. Tier L = the
measured-divergence bar, because it touches gates, blocking hooks, or
scripts/ — "anything that would, is Tier L by definition."

RANK 1 — ADR OPTIONS-DECAY SURFACING              value HIGH / fit HIGH
  Why first: the defect is MEASURED (86% -> 56%, Part 0E), it is in the
  repo's most load-bearing decision surface, and nothing sees it.
  Cheapest experiment: run the Part-0 script as a one-off over the
  corpus and put the four-block trend in front of the architect. That
  is done — it is Part 0E. THE EXPERIMENT IS ALREADY RUN; the only
  open question is whether the trend is a defect or a correct response
  to more of the recent ADRs being narrow amendments. THAT question
  costs one read of the 7 recent ADRs lacking the section.
  Adoption tier if pursued: reporting-only = Tier S. A gate asserting
  the section = Tier L by the guard sentence.

RANK 2 — REFERENCE-CLASS FORECASTING OVER OWN HISTORY
                                                  value HIGH / fit HIGH
  Why: best-evidenced debiasing mechanism in the catalog (UK Green
  Book / DfT since 2004), works by restructuring the task rather than
  warning the judge, and the reference class ALREADY EXISTS here
  (JOURNAL + audits + tasks). Directly attacks the planning fallacy on
  arc sizing, which the V-2 budget's "<=2 interactions" target
  currently asserts without a base rate.
  Cheapest experiment: pick the next arc; before dispatch, pull the
  last 5 arcs of the same shape from JOURNAL.md and record actual
  duration/interaction counts; state the outside-view estimate
  alongside the inside-view plan; compare at close. One arc, no build.
  Adoption tier: Tier S.

RANK 3 — MINORITY REPORT AS A FIRST-CLASS OUTPUT  value HIGH / fit HIGH
  Why: the gap is already self-diagnosed here (G7, docs/handoffs/
  2026-07-02-ai-council-architect/RESIDUAL.md), it is axis 6's central
  question, and the repo has already shown it can do it well in the
  ad-hoc case (nb2-a packet's recorded terra dissent). Turning a habit
  into a shape is cheap.
  Cheapest experiment: on the next Council run or terra review, require
  the artifact to carry a DISSENT block that survives synthesis
  verbatim — position, holder, and why it lost. One run. Compare
  whether the operator's read changes.
  Adoption tier: Tier S as a template change; Tier L if any gate
  asserts the block's presence.

RANK 4 — PREMORTEM AS A CONTRACT SECTION          value MED-HIGH / fit HIGH
  Why: absent (verified), literature already banked, and the ex-ante
  slot already exists — ADR-81 freezes success before the build, so
  freezing failure beside it is a section, not an organ. Note the
  honest ceiling: the measured effect is reduced overconfidence and
  more surfaced failure modes, NOT better outcomes. Buy it for what it
  measures.
  Cheapest experiment: add ten lines to ONE lane contract — "assume
  this lane failed; enumerate why" — before dispatch; at close, check
  how many enumerated modes actually occurred and how many real
  failures were unlisted. One lane. The second number is the one that
  matters.
  Adoption tier: Tier S.

RANK 5 — DOCTRINE: CONTRIVED vs AUTHENTIC DISSENT value MED-HIGH / fit HIGH
  Why: costs nothing to state and changes how three existing organs are
  read. The repo currently treats a prompted critic and a cross-vendor
  reviewer as the same class of second opinion; Nemeth 2001 and
  Schulz-Hardt 2002 measure them as different, with the prompted form
  capable of BOLSTERING the original position. This is the highest
  value-per-token item in the catalog.
  Cheapest experiment: none needed to state it; the settling
  experiment is whether a prompted-critic pass and a terra pass on the
  SAME diff produce different findings. One diff, two passes, compare.
  Adoption tier: Tier S (doctrine line), and it is arguably not an
  adoption at all — it is a correction to how existing organs are
  described.

RANK 6 — FUZZY-BAND ACCEPTANCE (the ADR-81 deferred arc)
                                                  value HIGH / fit MED
  Why not higher: it is the most valuable target and the most
  expensive, and Part 5 shows the literature supplies more
  CONSTRAINTS than materials — kappa ~0.37 on subjective rubric
  criteria, the kappa paradox, judge biases, and a standing local
  rejection of confidence scoring. The honest recommendation is to
  build the SMALL version (anchored observations + heterogeneous
  reader + disagreement-as-signal) and not the general one.
  Cheapest experiment: take ONE existing judgment artifact — this
  catalog would do — write 6-8 anchored binary observations for it,
  have terra evaluate them, and count disagreements against the
  architect's own reading. If disagreement localizes real problems,
  the shape works; if it scatters, it does not.
  Adoption tier: Tier L. It would steer acceptance of work, which is
  gate-adjacent by the guard sentence.

RANK 7 — MULTI-AGENT DEBATE AS A DECISION MECHANISM
                                                  value LOW / fit LOW
  RECOMMEND AGAINST, and this is the lane saying so. Measured to lose
  to self-consistency at equal budget; five methods, 36 configurations,
  none above a 20% win rate over plain CoT; 4-15x tokens. The repo
  already has the two configurations that DO have evidence —
  cross-vendor heterogeneity (terra) and asymmetric adjudication
  (ADR-108 §A routing) — and adding same-family debate on top would
  buy the weakest form at the highest price.
  Cheapest experiment: don't. If run anyway, the only informative
  version is debate vs self-consistency at EQUAL sample budget on the
  same questions — anything else reproduces the flattering baseline.

RANK 8 — COGNITIVE-BIAS CHECKLIST FOR AGENTS      value LOW / fit LOW
  RECOMMEND AGAINST as scoped. Mostly a category error (axis 5's
  transfer note): the named human biases belong to the operator, not
  the agents, and the agents' actual pathologies are not in the human
  taxonomy. Urbach 2014 is the cautionary case for mandating a
  checklist without fidelity. The useful residue of axis 5 is Rank 2,
  which is already ranked high on its own merits.

---------------------------------------------------------------------
PART 7 — HONESTY LEDGER
---------------------------------------------------------------------

RAN / DID NOT RUN
- Gates: NONE. Container uv is 0.8.17 vs the pinned ==0.11.19; I did
  not run pytest, ruff, or audit.py, and I report no gate result.
- All repo numbers come from python3 + grep, stated with their method.
- Zero writes. No commit, no push, no row, no intake, no ADR draft.

WHAT I COULD NOT VERIFY, LISTED SO IT IS NOT MISTAKEN FOR VERIFIED
- arxiv.org and idl.iscram.org are EGRESS-BLOCKED from this container.
  Every [METADATA-ONLY] tag above marks a citation resting on search-
  result text rather than on my reading the paper. Highest-priority
  re-fetches: arXiv 2604.27333 (ADR template comparison — the most
  relevant external paper to axis 2, and I have only its title), the
  rubric-kappa figures in Part 5, and Veinott et al. 2010's N and
  conditions.
- The "tenth man": NO SOURCE FOUND for a primary document. Labelled a
  hypothesis, not a citation.
- "Awareness alone does not debias": stated at [ASSERTED] strength
  because I did not verify a canonical study this session. Do not
  attach a specific paper to it without checking.
- Engineering orgs with standing premortem practice + outcomes: NO
  SOURCE FOUND beyond Atlassian's published Play.
- ADR-03 (blind vote) and ADR-01 (synthesizer exclusion) are cited BY
  protocols/AI_COUNCIL_PROCESS.md; those ADRs live in the ai-council
  repo, which is outside this session's scope. I verified the
  PROCESS-file text, not the ADRs themselves.

STALENESS FLAGS
- Axis 4's sceptical papers are 2023-2026 preprints; rates will move
  with models. The DIRECTION (heterogeneity/asymmetry over plurality)
  has held across three independent negative results and is the durable
  part; specific win rates are not.
- Schwenk 1990, Nemeth 2001, Schulz-Hardt 2002, Mitchell et al. 1989
  are old but are the foundational results and have not, to my
  knowledge, been overturned. I did not search for post-2010
  replications of Nemeth or Schulz-Hardt; if this catalog's axis-3
  conclusion is going to drive a build, that search is worth running.
- Zheng et al. 2023 predates several judge-model generations; the
  bias TYPES persist in later literature, the MAGNITUDES will not.
- Anything about Claude Code / Codex model behaviour is version-bound
  and my knowledge may lag.

THE ONE THING I WOULD FLAG TO THE ARCHITECT ABOVE ALL
This repo is measurably better at decision quality than the literature
it would be borrowing from — blind-vote anonymisation, synthesizer
exclusion, authority routing by question kind, a locator-bearing
discharge, an escalation budget, and annotated-rather-than-erased
rejections are, individually, practices I could not find published
together anywhere. The gaps are narrow and specific: options-practice
decay that nothing surfaces, dissent that is read but not structurally
preserved, no outside view over its own history, and an unbuilt fuzzy
band. The correct posture is not adoption of frameworks. It is
naming what is already here so it stops being reinvented, and closing
four specific holes.
=====================================================================
```

**Sources** (verified this session via search; the code-fenced artifact carries the same citations in paste-safe plain text):

- [Schulz-Hardt, Jochims & Frey (2002), *Productive conflict in group decision making: genuine and contrived dissent*, OBHDP 88(2)](https://www.sciencedirect.com/science/article/abs/pii/S0749597802000018)
- [Nemeth et al. (2001), *Devil's advocate versus authentic dissent*, EJSP 31(6)](https://onlinelibrary.wiley.com/doi/abs/10.1002/ejsp.58) · [Nemeth (2001), *Improving decision making by means of dissent*, JASP 31(1)](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1559-1816.2001.tb02481.x)
- [Schwenk (1990), *Effects of devil's advocacy and dialectical inquiry: a meta-analysis*, OBHDP 47(1):161–176](https://www.sciencedirect.com/science/article/abs/pii/074959789090051A)
- [Veinott, Klein et al. (2010), *Evaluating the effectiveness of the PreMortem technique on plan confidence*, ISCRAM](https://www.semanticscholar.org/paper/Evaluating-the-effectiveness-of-the-PreMortem-on-Veinott-Klein/cdd2452cac315fdd7436d1b67dbf9c7de9034857) · [Atlassian Team Playbook — Pre-Mortem](https://www.atlassian.com/team-playbook/plays/pre-mortem)
- [Morewedge et al. (2015), *Debiasing Decisions*, Policy Insights BBS](https://journals.sagepub.com/doi/10.1177/2372732215600886) · [Sellier, Scopelliti & Morewedge (2019), *Debiasing Training Improves Decision Making in the Field*](https://journals.sagepub.com/doi/abs/10.1177/0956797619861429)
- [Flyvbjerg — reference class forecasting / optimism bias in UK transport appraisal](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2278346)
- [Haynes et al. (2009), NEJM surgical safety checklist](https://www.nejm.org/doi/full/10.1056/NEJMsa0810119) · [Urbach et al. (2014), NEJM Ontario checklist — replication failure](https://www.nejm.org/doi/full/10.1056/NEJMsa1308261)
- [Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet* (arXiv 2310.01798)](https://arxiv.org/pdf/2310.01798) · [*If Multi-Agent Debate is the Answer, What is the Question?* (arXiv 2502.08788)](https://arxiv.org/html/2502.08788v1) · [*Stay Focused: Problem Drift in Multi-Agent Debate* (arXiv 2502.19559)](https://arxiv.org/pdf/2502.19559) · [*Should we be going MAD?*](https://openreview.net/pdf?id=CrUmgUaAQp)
- [Khan et al. (2024), *Debating with More Persuasive LLMs Leads to More Truthful Answers*, ICML/PMLR 235](https://proceedings.mlr.press/v235/khan24a.html)
- [Sharma et al. (2023), *Towards Understanding Sycophancy in Language Models* (arXiv 2310.13548)](https://arxiv.org/abs/2310.13548) · [Bai et al. (2022), *Constitutional AI* (arXiv 2212.08073)](https://arxiv.org/abs/2212.08073)
- [Zheng et al. (2023), *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*, NeurIPS D&B](https://papers.nips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html)
- [*One Size Fits All? An Empirical Comparison of ADR Templates* (arXiv 2604.27333)](https://arxiv.org/html/2604.27333v1) · [Ahmeti et al. (2024), *ADRs in Practice: An Action Research Study*](https://www.researchgate.net/publication/383613501_Architecture_Decision_Records_in_Practice_An_Action_Research_Study) · [adr.github.io (MADR / Nygard templates)](https://adr.github.io/)