# R2 — locator verification

**Rule being discharged (R2):** every locator from any reader is verified by a CC subagent
against the source before it enters a report. Unverified = marked UNVERIFIED, never dropped,
never promoted.

**Verifier:** Claude Sonnet subagent, read-only, adversarial framing ("a locator that is off by
a few lines, or that points at real text making a DIFFERENT claim, must be reported as such —
do not be generous"). 24 tool calls, 107,329 tokens.

**Scope actually verified:** leg 1c in full (the spine derivation — 24 locators across two
trees), plus three independent structural questions about the Maister tree. Legs 1a, 1b and 1f
are **UNVERIFIED at row level** and are labelled as such in their own files and in the table at
the bottom of this file. That is a real limit of this run, stated rather than papered over.

---

## 1. Leg 1c — verdicts

### Maister phase locators — 14 of 14 CONFIRMED

Every `### Phase N:` heading cited by the reader exists at the line cited, in
`plugins/maister/skills/development/SKILL.md`. Counted independently by the verifier from the
source: **14 phases, 1–14, present and sequential.** Two conditional triggers were checked
against body text rather than heading text and both hold —
`Skip if: task_characteristics.has_reproducible_defect is false` (Phase 3) and
`Skip if: options.e2e_enabled = false` (Phase 12).

Phase 4's "live gallery" claim CONFIRMED: the body carries an explicit companion-server section
and the gate text reads *"review the live gallery at [companion URL]"*.

Phase 14's gate CONFIRMED: *"**State**: Set `task.status: completed`"*.

### Our PLAYBOOK spine locators — 8 of 8 CONFIRMED, 2 with unsourced glosses

`protocols/PLAYBOOK.md:6064–6071` is a real 8-row table and each row is what the reader said it
was. Two glosses the reader added are **not at the line** and are demoted to UNVERIFIED:

| LOCATOR | GLOSS THE READER ADDED | STATUS |
|---|---|---|
| `PLAYBOOK.md:6070` | "closure cites a named SHA, actual command output, or operator observation" | **NOT AT LINE.** Line reads `\| 7 \| **OPERATOR WITNESS** \| §8 "Discharge with evidence" \|`. The detail is in §8; the gloss is the reader's own. |
| `PLAYBOOK.md:6071` | "JOURNAL.md, LESSONS.md, ADRs or archive records" | **NOT AT LINE**, and not in the "Lifeline 1" text it links (`:361` reads `decide → plan → delegate → verify → archive → educate`). |

Neither gloss is wrong about the repo. Both are wrong about *where the repo says it*. They are
kept, labelled, and not promoted into MATRIX.md as citations.

### Three defective locators

| LOCATOR | VERDICT | WHAT IS ACTUALLY THERE |
|---|---|---|
| `SKILL.md:559` | **WRONG** | The line is only the intro sentence `Development-specific fields in \`orchestrator-state.yml\`:`. The domain-extension block at **561–608** does carry the routing flags (`has_reproducible_defect`, `modifies_existing_code`, `creates_new_entities`, `involves_data_operations`, `ui_heavy`), the option flags (`spec_audit_enabled`, `skip_test_suite`, `e2e_enabled`, `user_docs_enabled`, `code_review_enabled`, `pragmatic_review_enabled`, `reality_check_enabled`, `production_check_enabled`) and `task_context.{risk_level, architecture_decision}`. But `completed_phases`, `failed_phases` and `auto_fix_attempts` are **in a different file** — `orchestrator-framework/references/orchestrator-patterns.md` ~218–236. |
| `tasks/README.md:81` | **OFF-BY-2** | Line 81 is the heading `## Layout`. The field enumeration is at **83–89**; ordering/manifest at **93–98**. The claim's *content* is accurate. |
| `PLAYBOOK.md:6070`, `:6071` | glosses **UNVERIFIED** | see table above |

**Net:** the substance of leg 1c survives verification. Its citation discipline does not, in
three places out of twenty-four. That ratio is itself the argument for R2.

---

## 2. The finding that overturns leg 1c's own framing

The verifier was asked three structural questions the reader had not been asked. The answers
change what the spine comparison means.

> **Q: Is `orchestrator-state.yml` actually WRITTEN by anything, or only described in prose?**
>
> **A: Described in prose only.** 33 mentions across the Maister tree, **all in `.md` files**,
> plus exactly one non-markdown hit: `plugins/maister/hooks/post-compact-reminder.sh:12,15`. The
> verifier read that script in full — 21 lines. It does a directory-existence check
> (`[ -d "$TASKS_DIR" ]`) and emits a **static JSON reminder string** telling the calling LLM to
> *"read the orchestrator-state.yml file… to verify completed_phases and determine the next
> phase."* **It never opens, parses or writes the YAML.**

> **Q: Is there executable code that reads or writes this state?**
>
> **A: None.** `find` for `*.py`, `*.js`, `*.ts` across `plugins/maister/` and
> `plugins/maister-copilot/` returns **zero results**. The Maister tree contains no executable
> code at all beyond that one 21-line shell hook.

**Consequence, and it cuts both ways.**

- Against us: Maister's state *shape* is genuinely richer than ours. It expresses execution
  position, per-phase attempts and results, conditional routing, and enabled/skipped branches.
  Our `tasks/` frontmatter — verified independently, union of keys across three real task files:
  `id, title, status, priority, size, theme, story, serialize-group, depends-on, generates` —
  expresses **none** of those. That half of the reader's claim stands.
- For us: Maister's spine is **prose an LLM is asked to honour**. Ours is **executable refusal** —
  the pre-commit, commit-msg and pre-push gates that blocked this very bundle's first commit
  attempt tonight and would not let it through until the tree was synced. A phase Maister
  "gates" can be skipped by a model that simply does not write the YAML; a gate of ours cannot
  be skipped by a model at all.

So the honest reading of R4's target claim is **neither the prior conclusion nor the reader's
refutation of it**:

> **"Maister offers nothing beyond a spine" is FALSE about content and TRUE about enforcement.**
> It carries substantially more than a spine — conditional phase routing, verification-option
> selection, UI-mockup machinery with a reviewable gallery, per-phase risk and architecture
> decisions. And it enforces none of it. We carry less shape and enforce what we carry.

That sentence is the load-bearing output of this leg, and it is the one MATRIX.md builds the
SPINE section on.

---

## 3. UNVERIFIED register — per reader

Per R2, nothing below was dropped. Everything below is carried in its own file and is marked
UNVERIFIED there.

| READER | LEG | ROWS PRODUCED | ROWS R2-VERIFIED | UNVERIFIED | WHY NOT VERIFIED |
|---|---|---|---|---|---|
| `agy` | 1a L01 | 18 | 0 | **18** | Verification budget went to 1c, whose claims are load-bearing for the SPINE section. Locators here are line numbers in a split transcript in a temp dir — cheap to re-verify, and the source is preserved. |
| `agy` | 1a L02 | ~30 | 0 | **~30** | as above |
| `agy` | 1a L03 | 32 | 0 | **32** | as above |
| `agy` | 1a L04 | 30 | 0 | **30** | as above |
| `agy` | 1a L05 | ~28 | 0 | **~28** | as above |
| `agy` | 1a L06 | ~35 | 0 | **~35** | as above |
| `agy` | 1b | 16 | 0 | **16** | Source is a temp clone; locators are `path:line` into it. |
| `codex` | 1c | 24 locators | **24** | 0 (3 defective, carried) | **fully verified** |
| `grok` | 1d | **0** | — | — | **LEG UNFULFILLED — R1.** Free-tier quota refusal. No substitute reader was run. |
| `cursor-agent` | 1e | 0 at first two attempts | — | — | Blocked by our own `PreToolUse` guard; see NIGHT-LOG. Third attempt with `CLAUDE_PROJECT_DIR` set. |
| Claude Sonnet | 1f | 31 | 0 | **31** | Self-reported as opened-and-quoted; not independently re-verified. A Claude subagent verifying a Claude subagent is weak evidence, and is labelled rather than claimed. |

**Total UNVERIFIED locator-bearing rows carried into Phase 2: ~218.**
**Total independently verified: 26** (24 from leg 1c, plus the two spot-checks in §4).

That ratio is the honest headline of this mission's evidence quality, and REVIEW.md §3 states it
in those terms. The one leg whose conclusions the mission most depends on — the spine
comparison — is the one that was verified, which was the deliberate allocation; but no reader's
table should be cited downstream as though it had been checked.

---

## Rows this file is evidence for

- **[#676]** - *no check verifies a provider CLI's non-interactive invocation shape.* The UNVERIFIED register records which readers answered, which refused, and why.
- **[#582]** - *substrate router.* The verification finding that Maister's state carrier is prose-only bears directly on what a capability-keyed router would and would not buy us.


---

## 4. Spot-check of leg 1a (agy) — the two load-bearing rows, verified first-hand

MATRIX.md rests two of its three focused sections on single agy claims. Both were re-opened
directly against the Polish source by the session (not by a subagent), because a section built on
an unverified row is not worth writing.

### L02.md:37 — "logical model aliases" (the MODEL-AGNOSTIC section rests on this)

**agy reported:** *"Logical model aliases (e.g. `prod-model`) decouple application code from
physical models, allowing provider swaps and model upgrades via gateway configuration changes
without code refactoring."*

**The source line says (verbatim, Polish):**

> "…możemy sobie użyć modelu **prod-model**, który tak naprawdę jest **nazwą logiczną**, która
> poprzez odpowiednie filtry czy reguły na samym gateway'u będzie dopiero zamieniona na jakiś
> **fizyczny model** danego providera. I to daje nam coś bezcennego, dlatego że samo wdrożenie
> takiego LiteLLM … powoduje, że **nie mamy vendor locka na poziomie kodu aplikacji** na
> konkretnego providera. Teraz **podmiana providera to jest tylko zmiana konfigu gateway**[a]"

**VERDICT: CONFIRMED, exactly.** The line even carries the mission's own phrasing of the target —
*swapping the provider is only a change of gateway config* — and names the failure it prevents,
vendor lock at the application-code level. The same line independently confirms the "unified API
standardised on the OpenAI schema" claim also cited at L02.md:37.

### L05.md:31 — reviewer rubber-stamping (the SELF-IMPROVEMENT LOOP section rests on this)

**agy reported:** two claims — detect rubber-stamping by monitoring approval rate and review
duration; prevent it by injecting synthetic flawed blind tests into reviewer queues.

**The source line says (verbatim, Polish):**

> "Takim głównym antywzorcem to jest taki **człowiek pieczątka** … bezmyślnie tak naprawdę
> zatwierdzający **w ułamku sekundy** wszystko, co produkuje AI. No i jak to możemy rozpoznać? Na
> przykład na podstawie tego, jaki jest **approval rate**, jaki jest **czas przeglądu**. Jak możemy
> temu zapobiegać? Możemy na przykład sprawdzać i **podrzucać jakieś ślepe, błędne testy** do
> wyłapania ludziom, którzy … ten czas przeglądu mają za mały albo approval rate mają wyższy, niż
> byśmy się tego spodziewali."

**VERDICT: CONFIRMED, exactly.** Both halves are on the cited line, including the two named
metrics and the blind-test countermeasure.

### What the spot-check licenses, and what it does not

Two of two agy rows checked came back exact — correct line, correct content, no drift and no
invention. That is a **calibration signal, not a verification of the other ~218 rows.** Two
samples from one reader on one source cannot license the set.

What it does license: MATRIX.md's §3 and §4 no longer rest on unverified ground, which was the
point of spending the check there. The `†` marks stay on every row that was not opened, and these
two rows are upgraded to `‡` in MATRIX.md's terms.

**Re-verification is cheap and the inputs are preserved.** The split transcripts remain at
`C:\Users\1028120\.claude\jobs\99120201\tmp\night\m03\L0{1..6}.md`, and the two clones at
`…\night\maister` and `…\night\ajcode`. Anyone re-running R2 over the remaining rows needs only
those paths — but note the job tmp directory is deleted with the job, so a re-run wanting the same
bytes should re-unzip `AJ_M03_transkrypcje.md.zip` and re-clone, which are both deterministic.
