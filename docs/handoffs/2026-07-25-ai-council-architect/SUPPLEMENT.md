# Architect strategic supplement — 2026-07-25-ai-council-architect

Repo: ai-council · Mode: architect · Date: 2026-07-25

> **Operator — 3 steps:**
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
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the
   repo.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

# Handoff answers — `ai-council` window 2026-07-23 → 2026-07-25

End state: `main 1fa0054`, pushed, in sync, tree clean, only `main`, primary worktree only,
`gc.auto 0`, `validate_backlog` OK 7 themes / 15 stories / **71 tasks**, `check.ps1` green with
the claim-checker running non-blocking. Hub `main d589844c`, in sync.

---

## Plan vs actual

| Planned | Result |
|---|---|
| FLOOR 1 — allowed-edge-set correction | ✅ `b1f3319` |
| FLOOR 2 — `#27` scoring materials | ✅ instrument ready, key sealed |
| PRIMARY 1 — checker v1, 14 rules | 🟡 **Unit 1 only** — rules 2/3/4/8 built, 12 structural, **nine outstanding** |
| PRIMARY 2 — `#27` blind-scoring sitting | ❌ **not run** (sixth consecutive window) |
| SECONDARY — filing batch | ✅ `6002aba`, 12 ids + 5 riders, 59→71 |
| SECONDARY — panel-default pin | ❌ |
| STRETCH — renumber, `#19` design | ❌ (`#103` filed, not executed) |

**Succeeded:** the window's closure criterion for *rulings* is fully met — no operator decision
from this window survives only in prose. The checker exists, runs automatically, and is honest
about its own gaps in its own output.

**Failed:** the only item that required the operator's hands did not happen, and it is the one
gating an entire theme.

---

## 1. Strategic intent — the way-of-working goal for next session

**Install external reference points wherever a mechanism currently verifies itself.**

This window's recurring discovery, five separate instances:

- rule 14 leg (a) validates the codemap against itself — an illegal import the map omits passes
- the Codex severity counter printed `0` over eight HIGH findings
- `grep -c '<<<<<<<' JOURNAL.md` counts its own logged quotation, so the counter inflates with
  every session that records the guard
- the Tier-1 gate cited proposal commits instead of build commits
- `@parametrize("leg", RULES)` iterates the registry, so 41 tests passed green while **two rules
  were missing from it entirely**

One principle unifies them: **self-referential verification is not verification.** A test that
enumerates a registry can only confirm what is present. A rule that compares a map to itself is
vacuous. A guard keyed on local directory state gives different answers in different checkouts.

The next session's methodology goal is not "build more rules." It is: every checking mechanism
must be anchored to something outside itself — a literal expected set, a spec, a second
derivation. `#97`'s new done-when clause (ii) is the first instance; the pattern is general.

**Second, smaller goal:** the architect seat should assert primitives, not conclusions. Five
architect errors this window, all the same class (see §6), all caught downstream. The pair works;
the failure concentrates in one half of it.

---

## 2. Tensions weighed, and where they landed

**Precision vs recall in rule 2 (terra H3).** Landed on **precision**, accepted for v1, on the
grounds that a report-only tool's only capital is credibility: a false negative costs one finding,
a false positive costs trust in all of them. **This position is now under revision, earlier than
planned.** The repo-rooted guard turned out to be implicated in three separate failures —
checkout non-determinism, suppression of LESSONS.md's one live defect, and unknown recall. The
revisit trigger I set ("at gating promotion") has fired early.

**Report vs gate.** Landed on **report-only, non-blocking**, but with the script exiting non-zero
from day one and only the `check.ps1` call site swallowing it. Promotion is a one-line call-site
change, never a rewrite.

**Suppress vs classify (rule 8's tracking citations).** Landed on **classify, never suppress.**
Filing `#112` and `#105` doubled rule 8's finding count, because both tickets name the dangling
SHAs they track and the checker cannot tell a tracking citation from a careless one. The cheap fix
— obfuscating the SHAs so rule 8 stops matching — was rejected: hiding a real dangling reference
to lower a count inverts the tool's purpose. `#105`'s distinct-defect accounting is the real fix.

**Rider vs own id (`#101` / `#113`).** Landed on **two tickets.** A deferred clause inside a
ticket that will eventually close either blocks that closure or vanishes with it, carries no
open-id status, and cannot enter a ranked queue.

**Ordering: filing batch vs more code.** Landed on **batch first.** Every operator decision from
this window existed only in chat; the batch is the persistence mechanism, and it is cheap.

**Verification cost vs speed.** I demanded verbatim artifacts four times rather than accepting a
summary. Twice it changed the outcome; once my suspicion was wrong but the check was still correct
to make; once I deliberately skipped it and took the artifact in the post-merge report instead.
That calibration is itself a result: demand the artifact when it gates a freeze or a merge, take
it after the fact when it is cheap to amend.

**CLI default vs measured parity.** The operator stated this window that **CLI is the default
transport for debate, API for research mode**, with deliberate opt-in to API otherwise. That is a
coherent architectural split — research has different needs (retrieval, longer context). My
position: the ruling stands, but it does not remove the reason `#27` exists. Twelve blinded pairs
measure *what the preference costs in quality*, not *whether it is preferred*. The sitting becomes
a cost control, not a decision. **Not yet confirmed by the operator, and `#27`'s done-when should
be rewritten accordingly.**

---

## 3. Considered and rejected — do not relitigate

- **Widening the ARCHITECTURE allowed-edge set** to legalise `cli.py`'s real 14-edge profile.
  Rejected on the repo's own precedent: rewording an invariant to match a defect launders the
  defect. The set is held as **TARGET**; `#92`'s refactor shrinks the real surface toward it, and
  re-derivation is triggered by `#92` landing — not by opinion.
- **`markdown-it-py`** for the options scanner. Rejected by the `#80`/`#81` spike: it inverts the
  failure mode (the scanner fabricates options from a fence; the library loses the whole list) plus
  a large in-parse performance regression. Settled.
- **Stop-hook as the checker's wiring surface** — fires every session end including doc-untouched
  ones, constant noise. **Pre-commit** — pass/fail by construction and sits with formatters, which
  breaks the read-only requirement. Landed on a non-blocking `check.ps1` findings section.
- **Allowlisting `.claude/skills/`** to silence the self-negating finding. Rejected: an allowlist
  would hide the whole negation class. Named in KNOWN LIMITATIONS instead.
- **Worktrees for any pytest-bearing work.** A worktree shares the primary's editable install, so
  pytest inside one silently tests the primary's source. Separately, `.worktreeinclude` does not
  exist in this repo, so worktrees are blocked outright until it does.
- **`pytest -n auto` in `ai-council`'s `check.ps1`** — rejected on clean numbers (1.42×, not
  3.9×). The hub *does* use it; the asymmetry is deliberate, not drift.
- **Assigning `#107`** — reserved instead. Third hub/local id-space collision.
- **`sol` for a second derivation of the rule spec** — the spec is already an evidence-backed
  derivation from a real manual run. Cost without added evidence.
- **The parallel cloud session's branch** — discarded. It converged on identical output (free
  corroboration of the id assignment), but its pre-commit gates were *skipped, not passed*, and it
  filed two claims it could not verify from its checkout.

---

## 4. Open questions

1. **Is the H3 precision-over-recall ruling still right?** Evidence now says the guard is the
   single highest-leverage fix in the checker. Revisit is due now, not at gating promotion.
2. **Is context-adjudication harness-level or per-rule?** `#108` landed rule-2-local, correctly —
   rule 2's case is a false positive (suppression loses nothing) while rule 8's is a true finding
   with near-zero actionability (suppression would hide real fragility). But both need the same
   underlying predicate: *is this token inside a statement about the defect?* A shared helper is a
   third option neither ticket currently holds.
3. **Should `LESSONS.md` enter rule 2's surface?** Adding it buys nothing until the guard is fixed
   — its one live defect (`tasks/lessons.md`, twice, `tasks/` is not a directory) would be
   suppressed anyway. Separately, the exclusion comment at `validate_claims.py:156-157` claims a
   symmetry the code does not implement.
4. **What pushed `origin/main` at 13:58?** Not CC, and not the cloud (it had no remote, and the
   reflog verb says push-from-here). Governance-relevant: "operator is the serial merge gate" is
   not enforced against a background pusher.
5. **`#27`'s done-when** under the CLI-default ruling — decide the flip, or price a flip already
   decided?
6. **`#8` / `#73` / `#87`** — three done-whens, recommendations issued mid-session, never
   confirmed.
7. **ADR-11 decision-1 interactivity ruling** — blocks `#113`, and nothing schedules it.
8. **How much should the boost boost?** Unruled. Bears on whether `#101`'s emitted annotations are
   machine-satisfiable and on the GUIDE's `### Questions` template.

---

## 5. Decomposition rationale — and what not to redo

**Why this shape:**

- The allowed-set correction had to land **before** any rule-14 work, because leg (a) validates the
  codemap against that set. A factually wrong set means validating against a false standard.
- Unit 1 = harness + finding contract + four legs, deliberately small, because `#105` and `#106`
  both change the **frozen** `Finding` interface. Every leg inherits it. Fixing at four legs is
  cheap; fixing at eleven is a retrofit.
- The filing batch ran last among code work but before session end, because it is the persistence
  mechanism for everything decided in chat.
- `#27` was never sequenced behind anything, by design. Defect-driven ordering structurally cannot
  see an operator-blocked task, which is exactly why it fell out of six consecutive windows.

**Consequence for next session — invert the obvious order: Unit 1.5 before Unit 2.**
`#105` adds a subject field to `Finding`; `#106` changes `printed()`. Both are harness surface.
Land them while the blast radius is four legs.

**Unit 2 is NINE rules, not seven.** Rules 1 and 7 are absent from the registry entirely — not
stubs. Rule 1 (module-table completeness) shares `src/` enumeration machinery with rule 14 leg (b);
build them together. Rule 7 (stamp honesty) extends `canonical_freshness` and is precisely the rule
that would audit this window's three `last_reviewed` re-stamps.

**Do NOT redo or re-decide:**

- The fourteen-rule spec. It now lives **inline in `#97`** with earned-by traces per rule, which
  resolves the earlier split between the immutable audit §3 (twelve rules) and the ticket (13/14).
  Read it there; do not re-derive it.
- The allowed-edge-set correction (`b1f3319`) and its TARGET framing.
- The wiring surface, the `#101`/`#113` split, the `#107` reservation, the `markdown-it-py`
  rejection.
- The `Finding`/`RuleResult` divergence from hub `#89`'s scalar `ClaimResult`. It is deliberate —
  a scalar cannot carry rule 12's per-finding evidence command. It needs **recording** in the hub
  packet, not re-deciding.

---

## 6. Off-repo context

**The three standing themes, honestly graded:**

- **Boost / protocol to other repos — strongest motion.** `#101` (sharpening-annotation block:
  candidate narrowings, missing-constraint questions, criterion pushback — questions and flags
  only, never an invented fact, no ADR-11 reopen), `#113` (interactive variant, both exits named so
  it cannot become a zombie), `#100` (verdict-package JSON Schema — the contract is at 1.0 and
  describes its field set in prose, so a foreign caller has nothing to validate against), `#88`
  named by name to the P2 arc.
- **CLI as default — stated, unwritten.** The operator's ruling exists only in chat. It belongs in
  an ADR or at minimum a ticket. It also reframes `#27`.
- **Non-cognitive debate — weakest, and this must be said plainly.** `#103` was filed as a *design
  commission* (research → design → filed tasks, explicitly not a build) and was not executed.
  `#55` — the matched-compute baseline, the adjudicator of the entire debate bet — remains
  operator-gated and untouched. `#27` unscored. The theme moved on paper only, for the fifth
  window. Everything else this session had a mechanism behind it; this one still has an intention.

**Other context not in the repo:**

- The `#27` instrument (`READING-INDEX.md` + `SCORING-RECORD.md`, rubric inline, items 2 and 4
  zero-margin, key sealed and gitignored) has been ready and unused for a full day. Scoring is
  resumable in parts — the key stays sealed until 12/12, so four pairs now and eight later costs
  nothing.
- **Five architect errors this window, all one class**, all caught downstream by CC: `HEAD` instead
  of `main` in a merge-tree preflight; a stale test count authorized as `N=41`; a "13 commits
  disappeared" conclusion drawn from derived arithmetic; a backup asserted from a truncated report
  that did not exist; and approving a rule split covering 12 of 14 without summing it. Treat
  browser-seat pointers as claims to verify, not facts.
- A concurrent Ultraplan cloud session executed the same filing batch independently and produced
  identical ids, placements, riders and counts. Discarded for the reasons in §3, but the
  convergence is real corroboration.
- Unfiled: three gotchas (`git merge -F -` rejects the stdin dash unlike `git commit`; a called
  script's exit leaks into `check.ps1`'s own exit without an explicit `exit 0`; the ADR-85 JOURNAL
  gate fires per session-stop rather than per substantive change). Home is
  `~/.claude/skills/gotchas/gotchas.md`, needs its own window.
- Uncarried hub packet: the `grep -c '^<<<<<<<'` guard fix, and the `Finding`/`ClaimResult`
  divergence record.
- Token spend 2026-07-18 → 07-25: 8 active days, ~$1.4k, 9.88M tokens, Opus 4.8 at 92%.

