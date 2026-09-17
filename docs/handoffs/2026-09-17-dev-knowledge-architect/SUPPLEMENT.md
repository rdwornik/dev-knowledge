# Architect strategic supplement — 2026-09-17-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-09-17

> **Operator — 3 steps:**
>
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context — changed INTENT only.** Intent, priorities and decisions that moved
   this window and are not in the repo. **Not** the operator's interface mechanics — file
   exchange through Downloads, `.md` uploads because a large inline paste arrives empty,
   shipping the exact start command, reports travelling as files. Those are constants, they
   live at `protocols/OPERATOR-INTERFACE.md`, and the incoming bundle's forms card already
   carries them; one of them being wrong is a defect report about that file, not an answer
   here.
7. **Ratified-in-chat register** — terms, rulings, or contracts ratified in this window's
   chats that are NOT yet recorded in the repo, **and interface BEHAVIORS you relied on that
   are not yet named in `protocols/OPERATOR-INTERFACE.md`** — e.g. a copy-ready block
   substituting for a described action, a paste arriving as a `.md` upload rather than inline
   text, reliance on the `PASTE_THIS.md` END sentinel to detect a truncated paste, or a
   Downloads-directory fallback for file exchange. For either kind: the verbatim term/behavior ·
   a one-line definition (or what relying on it looked like) · its intended durable home
   (BACKLOG id / ADR / LESSONS / PLAYBOOK §, or `OPERATOR-INTERFACE.md` for an interface
   behavior). "None" is a valid answer.

<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

SUPPLEMENT ANSWERS — authored by the browser architect, transcribe VERBATIM, do not summarise or reword.

Q1 — STRATEGIC INTENT
Stop adding mechanisms. Prove throughput. This window added ~15 mechanisms and removed none until the system stopped working; the commit gate reached 34 hooks at ~244 s while the guards it fronted were failing open and nothing counted either fact. The next session's goal at the way-of-working level is a single falsifiable acceptance test: ONE LANE RUNS END TO END, DISPATCH TO MERGED, IN UNDER ONE HOUR, WITH NOTHING WEDGED AND NO HUMAN DECISION IN THE MIDDLE. Until that passes, no new organ is built. Governing rule for everything after it: a mechanism ships with a COUNTER — what it caught, what it cost, over what window — and a gate with no catch in its window is REMOVED, not tuned. Every ruling this window carried a refusal criterion and none carried a cost criterion; that asymmetry is why the harness became its own bottleneck.

Q2 — TENSIONS WEIGHED, AND WHERE THIS SEAT LANDED
(a) Enforcement vs throughput. Landed: enforcement must be priced. Evidence: 34 hooks / ~244 s mean; ~17 agent-hours lost to a gate-bound commit starving subagents; a 6-hour wedged integrator; a full night lost to hook processes. Enforcement moves EARLIER where it can (a refusal that prevents work beats one that discovers it) but nothing joins the commit tier without a measured cost in its Done-when.
(b) Emergency blanket disable vs measured individual disable. Landed: individual, measured. The blanket disableAllHooks was this seat's panic; lane ab-808's measurement later showed the three REQUIRED hooks were never among the nine that wedge. We disabled hooks that never failed in order to stop hooks that did.
(c) Prose vs data as the source of truth. Landed: data is the source, prose is a rendered view, and a divergence is a refusal. Evidence: 115 citations of PLAYBOOK/STANDING_RULINGS with 57 the ONLY carrier of their rule; dispatch_drift parsing a prose table and passing only because one machine carried an unmerged branch; the manifest's id blocks being prose, which is why a row landed outside every block.
(d) Windows vs portable. Landed: this is NOT primarily an OS problem. 8.9 % of lines are Windows-only and 43 of 51 Linux failures are fleet-shape assumptions, not OS. The coupling that hurts is to THIS WORKSTATION, not to Windows.
(e) Browser as mechanism vs repo as mechanism. Landed: the repo. Three times this seat offered its own vigilance as the safeguard — sampling transcripts, remembering to boot an integrator, holding rules in pastes. All three failed. The operator's standing rule stands: the browser is the weakest link and the repo must protect itself from it.

Q3 — CONSIDERED AND REJECTED (do not relitigate)

- Rewriting the hooks: REJECTED. The defect is upstream process spawn — hook processes were created SUSPENDED, 0 s CPU, no image path, one thread in Wait/Suspended. Our scripts never executed a line. Rewriting them fixes nothing.
- The bounded-hook wrapper as THE fix: REJECTED as sufficient (kept as a module). A timeout cannot fire on a process that never starts, and the wrapper adds one more interpreter to every hook.
- Restoring hook declarations while execution stays disabled: REJECTED as a workaround. The gate would report "required hooks present" when they do not run — green without substance, the exact class this window spent itself finding.
- Handoff without a bundle: REJECTED by the operator, correctly. Capitulation, not a solution.
- disableAllHooks as a resting state: REJECTED. Emergency measure only; it must not become normal by habit.
- A separate per-batch state carrier in the benchmark's shape: REJECTED structurally — a second authority over row state.
- Sequential-only lane execution: REJECTED. Worktrees exist for parallelism; the sequencing was this seat's caution under a memory constraint and it outlived the constraint by two days.
- Migrating dispatch to Python NOW: DEFERRED, not rejected — only three dispatch pieces are truly Windows-only and DispatchHelpers.psm1 makes 0 Start-Process / job-object calls; `claude --bg --worktree` does the launching and isolation itself.

Q4 — OPEN QUESTIONS

- Does the repo get a DEGRADED state? This is the cause behind every emergency this window: there is no way to record "this required component is deliberately absent, owned by X, expiring on Y". fleet_parity stops at a missing required hook before reading any waiver and ADR-102 forbids marking one waivable, so an emergency leaves only two options: lie to the gate or stop work. [#886] names the symptom.
- Per-task EXECUTION state: extend the existing row, or a new carrier. All three benchmarks converge on this and we still have no row. Phase 1 (establish what [#664], tasks/ frontmatter, manifest.json, FPG-1 and the organ index already hold) MUST run before anything is built beside what exists.
- The six contradicting rule pairs are ANSWERED this window (P1=C P2=A P3=B P4=C P5=A P6=B) but their ENFORCEMENT is not built.
- CI enforcement: on, or documented as report-only. Today it is disabled and three red pushes landed.
- The Actions credential, on SECURITY grounds (a narrower blast radius than every lane inheriting the whole .env), not on the CI claim — there is no runner.
- Codespace contract delivery: commit the contract to the repo before dispatch (expected answer), pass it in the prompt, or a skill reading Drive through its API. The Drive-has-no-Linux-client framing is a symptom of the browser being the transport, not a blocker.
- Non-Claude producers: capability is PROVEN (copilot 10/10, codex 10/10, agy 10/10) and production use is still ~zero against USD 8,721 at 99.47 % Opus.
- Dispatch layer to Python: ~9 lanes, evidence in the OS-coupling digest.

Q5 — DECOMPOSITION RATIONALE; WHAT THE NEXT SESSION MUST NOT REDO
Order work by MEASURED COST OF INACTION, not by size of problem. This seat ordered by size twice and the four cheapest wirings — each costing measured hours per week — waited behind one large structural lane.
DO NOT REDO, all of it is in intake 103 (docs/intake/2026-09-16-tech-browser-seat-findings-off-the-transport.md) and the transport digests:

- the rules-to-enforcement ladder audit (115 citations, 47 rule families, 33 hook events, exit 1 never blocks, allow/ask inert under bypassPermissions)
- the lane anatomy measurement (model time 13-25 %; 62-86 % is the box and our own mechanisms)
- the OS-coupling audit (8.9 %, DispatchHelpers 43.6 % of it, 43 of 51 Linux failures are fleet-shape)
- the AJ M04 matrix and the benchmark comparison
- the closure census (25 rows closable with a witness)
- the prose-as-source measurement
  ALREADY LANDED, do not rebuild: the task-id allocator (reserve by PUSH; the local maximum is never read), /lane-boot refusing a batch with no committed manifest, the prompts guard failing closed, the conductor reading the frozen baseline, the deletion method with paired before/after suites, BACKLOG narration relocation (99,961 → 75,143 B).
  READ THE EVIDENCE BASE FIRST: git log and JOURNAL carry every change this window with its reasoning. The next session should reconstruct what happened from those two, not from anyone's memory.

Q6 — OFF-REPO INTENT THAT MOVED THIS WINDOW

- TOKEN EFFICIENCY IS NOW THE OPERATOR'S TOP CONSTRAINT. Roughly half a weekly quota is spent; USD 8,721 measured at 99.47 % Opus. Every other model is to be maximised before Opus, without losing quality.
- He ruled, and does not want asked again, that the employer-paid GitHub Enterprise Copilot quota MAY be used on these repos.
- Direction: OS-agnostic, Python-first where it is cheap. His words, and the measurement supports the direction without supporting urgency.
- The harness must USE THE TOOLS IT BUILDS, and that use must be MEASURED — organ calls versus raw scans per session is his question and it has never had a number.
- Continuous work, no night gating; his workstation is available.
- Codespace is the intended off-box substrate; the container is proven, the transport is not.
- TRUST IS LOW AND EARNED BACK BY DELIVERY, NOT ANALYSIS. He has had a week of audits and measurements and cannot yet run one lane cleanly. The next session should ship the acceptance test in Q1 before it proposes anything.

Q7 — RATIFIED IN CHAT, NOT YET IN THE REPO
RULINGS AND TERMS:

- "A mechanism ships with a counter — what it caught, what it cost, over what window; a gate with no catch in its window is removed, not tuned." Home: LESSONS + PLAYBOOK.
- "A verb's reported success is not evidence of its effect." Four witnessed surfaces: `claude stop` returning success with the tree alive; Codespaces reporting healthy while serving a recovery container; a cloud request reporting "launched successfully" after falling back to local; our own hooks exiting 1 reporting a pass while blocking nothing. Home: ADR or LESSONS.
- "Prose is documentation, not a source of truth for execution; execution reads data, prose is a rendered view, a divergence is a refusal." The operator's own formulation. Home: ADR.
- "A rule with no enforcement point is not a rule." Home: the enforcement register.
- The one-hour acceptance test (Q1). Home: a BACKLOG row plus PLAYBOOK.
- The six-pair answers P1=C P2=A P3=B P4=C P5=A P6=B, answered in chat today; each pair's enforcement is unbuilt.
- "An emergency change records its temporary debt as DATA with an owner and an expiry, never as a JOURNAL sentence." [#886] filed.
- "A research dispatch states its agent cap, its per-agent deadline and its token budget up front." [#884] filed, after one research session consumed ~0.5M tokens over 17 hours and was killed mid-step with nothing written.
- "Declaration and execution are two different things" — conflating them is what made this window's hook debt unrecordable.
  INTERFACE BEHAVIOURS RELIED ON, not yet named in protocols/OPERATOR-INTERFACE.md:
- A LARGE INLINE PASTE ARRIVES EMPTY at the browser seat. The operator had to upload CC output as .md files, and the browser seat could only read them from disk with a shell tool rather than seeing them in context. This happened repeatedly and cost turns before it was diagnosed. Home: OPERATOR-INTERFACE.md.
- SESSION LIVENESS IS TESTED BY COMPARING TWO SAMPLES of the session's own counters (elapsed time, token count, last step), never by reading the transcript's content. This seat reported a wedged integrator as "working" for hours because it judged by content; the two-sample test was available and unused. Home: OPERATOR-INTERFACE.md or PLAYBOOK.
- A SESSION INSIDE A LONG TOOL CALL CANNOT RECEIVE AN INSTRUCTION until the call returns, so "stop" is undeliverable to the session that most needs it; the only remedy today is killing it, which loses what it held. [#769] covers the commit-gate case only. Home: OPERATOR-INTERFACE.md plus a row.
  === END OF SUPPLEMENT ANSWERS ===
