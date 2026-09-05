# Corpus coherence audit (candidate g) — Gemini as whole-corpus reader

> **Class:** technical · **Date:** 2026-09-05 · **Mode:** read-only, LOCAL
> **Reader:** Gemini 3.1 Pro (High) via the `agy` (Antigravity) CLI — the fan_out lane
> **Verifier:** Claude Code, live locator re-read against the working tree
> **Baseline:** reader ran against `main` @ `6de676fb`; every locator re-verified after a
> sync-merge at `main` @ `3200757d` and all six still hold exactly (`protocols/PLAYBOOK.md`
> changed in between, so the line numbers were re-checked rather than assumed)

## 1. What was run

One structured, retrieval-only question was put to a single non-Claude whole-corpus reader.
Every locator it returned was then re-opened on disk by CC; a finding whose locator does not
hold is dropped and counted as a fabrication.

**Corpus (declared to the reader):** `CLAUDE.md`, `AGENTS.md`, `README.md`, `ARCHITECTURE.md`,
`protocols/**` (14 files, incl. `protocols/STANDING_RULINGS.md` and `protocols/PLAYBOOK.md`),
`docs/decisions/ADR-*.md` (89 files), `LESSONS.md`. Measured size **2,438,199 B**.

Note on the brief: it named `STANDING_RULINGS.md` at top level. The file lives at
`protocols/STANDING_RULINGS.md` and is therefore already inside the `protocols/**` leg — no
top-level `STANDING_RULINGS.md` exists.

**Invocation** (flags per the recorded `agy` gotchas — `--dangerously-skip-permissions` because
print mode soft-denies filesystem tools, and no `--sandbox`, which is a known timeout driver):

```
agy --model gemini-3.1-pro-high --output-format json --print-timeout=45m \
    --dangerously-skip-permissions --add-dir . --log-file <log> --print='<one question>'
```

**Served-model attestation.** `model_resolver.go:80] Resolving model gemini-3.1-pro-high` in the
CLI log. `agy` exits at zero tokens on an unknown id rather than substituting, so this is a real
attestation — no model was silently swapped, and nothing here is a Claude answer relabelled.

## 2. Verification result — headline

Four findings returned, one per category. **Six locators, all six EXACT on disk. Zero
fabrications.** Nothing was dropped on locator grounds.

But locator-exactness is not claim-correctness. Re-testing the substance changed the standing of
two of the four:

| id | category | locator verdict | substance after CC verification |
|---|---|---|---|
| C1 | contradiction | 2/2 EXACT | **CONFIRMED — and materially stronger than reported** |
| U1 | unenforced rule | 1/1 EXACT | **CONFIRMED** |
| D1 | duplicated clause | 2/2 EXACT | **CONFIRMED — and it breaches a self-declared invariant** |
| N1 | uncited file | 1/1 EXACT | **REFUTED on substance** (true only under a scope that excludes the ADR index) |

## 3. Verified findings

### C1 — `LESSONS.md` never received the amendment that governs it

- **A** `CLAUDE.md:89` — *"1. **`LESSONS.md` and `logs/TOKEN-LOG.md` are append-only** — never edit old entries; only append (ADR-29, ADR-39). **LESSONS.md-only exception (ADR-29 amend. 2026-07-17):** a contiguous *older* block MAY be relocated **byte-identical** into a dated `LESSONS-legacy-<span>.md` …"*
- **B** `LESSONS.md:5` — *"> New entries go at the top of the Entries section. Never edit old entries. Never delete."*

CC verification went past what the reader claimed. `docs/decisions/ADR-29-*.md:122` defines a
**"Required cross-doc reconciliation set (atomic with ratification)"**, and `:126` records
**"Ratified 2026-07-17"** together with the surfaces that landed. Checked one by one:

- `CLAUDE.md:89` — reconciled
- `ARCHITECTURE.md:322-325` and `ARCHITECTURE.md:957` — reconciled
- `protocols/PLAYBOOK.md:5347` — reconciled
- `docs/decisions/README.md` ADR-29 row — reconciled (per ADR-29:126)
- **`LESSONS.md` itself — NOT reconciled.** Its header still reads "Never delete."

So a reconciliation set that declared itself *atomic* covered four surfaces and missed the fifth —
the file the rule is actually about. It is not a near-miss of timing either: `LESSONS.md:6` stamps
**"Last updated: 2026-08-03"**, i.e. the file was edited *after* the 2026-07-17 ratification and the
stale header survived. `grep -ci legacy` over the first 20 lines of `LESSONS.md` returns **0**.

**Consequence.** An operator reading the file's own header is told the sanctioned move is
forbidden — precisely the outcome ADR-29:122 wrote the reconciliation set to prevent.

### U1 — commit-summary rules are prose-only

- `protocols/PLAYBOOK.md:666` — *"- **Summary line.** Imperative mood, specific, describes WHAT changed. Under ~72 chars. **Never** \"wip\", \"fix\", \"updates\", \"stuff\", \"various changes\"."*

CC re-ran the negative search rather than trusting it. The `commit-msg` stage of
`.pre-commit-config.yaml` carries exactly two hooks — `backlog-id-on-close` and
`backlog-filing-backpressure` (both `stages: [commit-msg]`). Neither inspects the summary line.
No script under `scripts/` implements a subject-length check, an imperative-mood check, or the
banned-word list; the `wip` hits under `tests/` are worktree fixtures, not enforcers.

**Confirmed prose-only.** Four distinct rules (mood, specificity, ~72 chars, banned words) with no
mechanism. Worth noting this is a *rule-density* gap, not a missing-hook emergency: the enum-shaped
neighbours (branch prefixes, `[#id]` on close, `kill-candidates`) *are* mechanised, which is what
makes the unmechanised four easy to miss.

### D1 — the same rule in `CLAUDE.md` and `AGENTS.md`, against an explicit no-duplication invariant

- **A** `CLAUDE.md:63` — *"- **Commits & branches:** … Never commit directly to `main`: branch → `--no-ff` merge."*
- **B** `AGENTS.md:69` — *"- **Never commit directly to `main`.** Branch, then merge with `--no-ff`. A pre-commit hook"*

The reader filed this as ordinary drift risk. It is more than that. `CLAUDE.md:41` states, of these
two files specifically:

> *"No fact is duplicated across the two — the importer preserves ADR-53's substance"*

`CLAUDE.md` imports `AGENTS.md` via `@AGENTS.md` (`CLAUDE.md:43`), so both clauses load into the
same context, and the never-commit-to-`main` + `--no-ff` fact is carried twice. The duplication
therefore **falsifies an invariant the corpus asserts about itself 22 lines earlier** — which
promotes D1 from category (3) into category (1) as well.

## 4. Refuted on substance — N1

- Claim: `docs/decisions/ADR-83-protocols-archive-convention.md` is cited by nothing.
- Locator `…ADR-83-protocols-archive-convention.md:1` — **EXACT** (`"# ADR-83: Protocols-archive convention — where superseded protocols go"`). Not a fabrication.

The claim does not survive verification as a rot signal. `grep -rn "ADR-83"` over `*.md`, excluding
the ADR itself and `.claude/worktrees/`, returns **214 lines**, including
`docs/decisions/README.md:117` — the canonical ADR index that `CLAUDE.md` §11 explicitly designates
as the home for ADR one-liners — plus `.claude/commands/handoff.md` (3 sites) and multiple
`docs/audits/` files.

The reader's own stated `grep_run` scoped to `docs/decisions/ADR-*.md`, a glob that **excludes
`docs/decisions/README.md`**. Under that scope the sentence is literally true and operationally
meaningless. **Recorded as a false positive, not a fabrication** — the locator held, the inference
did not. It is a good illustration of why category (4) needs the citation surface named, not just a
glob.

## 5. Fabrications

**Count: 0.** All six returned locators matched the file at the stated 1-indexed line, byte-for-byte
after Unicode/whitespace normalisation (curly quotes, em-dashes, NBSP). No `MISSING`, no `NOFILE`,
no line-number `DRIFT`.

Verifier: `verify_locators.py`, which for each locator opens the cited file, compares the quoted
text at the cited line, and — on mismatch — searches the rest of the file to separate genuine
invention from line-number drift. Machine summary:

```
contradictions      returned 1  verified 1  dropped 0
duplicated_clauses  returned 1  verified 1  dropped 0
unenforced_rules    returned 1  verified 1  dropped 0
uncited             returned 1  verified 1  dropped 0
TOTAL               returned 4  verified 4  dropped 0
```

**But provenance strings are a separate matter, and they did not hold up.** The reader reported
shell commands as evidence — `"grep -i 'wip' scripts/* tests/*"` (U1) and a `grep -rnE 'ADR-83' …`
(N1). The CLI log records **10 auto-approved tool confirmations in total: 9 `ListDir`, 1
`ViewFile`, and zero `GrepSearch`**. The log does not record file paths, so this is not proof that
no search occurred through another path — but no evidence of those greps exists, and the quoted
commands should be read as *descriptions of intent*, not as executed commands. **The locators were
real; the stated method was not attested.**

Same caution applies to its `coverage_note`: *"Successfully opened and checked all 108 files
explicitly specified in the corpus."* The corpus is 2,438,199 B (~610k tokens); the run consumed
**383,742 input tokens**. Full-corpus ingestion is arithmetically not evidenced, and the claim is
an overclaim. Yield — 4 findings from a 2.44 MB corpus — is consistent with sampling.

## 6. Cost and wall-clock

`agy` exposes **no quota subcommand** (`agy help` has no quota/usage/limit entry), so consumption is
reported from the response envelope rather than from a quota counter:

```
status              SUCCESS
conversation_id     1b6c02fa-8587-4e87-8789-1066df26a497
input_tokens          383,742
output_tokens          29,615
thinking_tokens        18,368
cache_read_tokens   5,038,940
total_tokens          413,357   (input + output; thinking is inside output)
duration_seconds      749.18    (12m29s, agy-reported)
```

**Wall-clock, observed:** launched `2026-09-05T11:54:46Z`, envelope written `2026-09-05T12:07:06Z`
— **12m20s** for the reader leg. Verification and write-up ran after that in the CC session.

**Scoping check.** Per the standing warning that `agy` trusts all of `C:\Users\1028120`, the log was
swept for absolute paths outside the repo: none found beyond `agy`'s own config and binaries. The
run stayed in the tree.

## 7. Assessment of the lane

Worth keeping, with the verification leg treated as mandatory rather than optional.

- **Locator discipline held perfectly** (6/6 EXACT) once the prompt made verbatim line-text
  mandatory and told the reader that a mismatch would be counted as a fabrication. That constraint
  is doing real work and should stay in any re-run.
- **Precision was high, recall was low.** Four findings from 2.44 MB. Two of the three confirmed
  findings (C1, D1) are genuinely valuable and neither is obvious from inside the corpus.
- **Negative claims are the weak axis.** Both category (2) and (4) rest on "I searched and found
  nothing", and the search was not attested. U1 survived CC's independent re-search; N1 did not.
  Any future run should re-test every negative claim rather than accept it.
- **The reader's framing under-rated its own best finds.** C1 and D1 were both stronger than
  reported — C1 because the amendment declared an atomic reconciliation set that demonstrably
  missed a surface, D1 because an explicit no-duplication invariant sits 22 lines away. Value came
  from CC pulling the threads, not from the returned text alone.

## 8. Owed follow-ups (filed here, not executed — this audit is read-only)

1. **C1** — reconcile `LESSONS.md:5` with the ratified ADR-29 2026-07-17 amendment. Hub-canonical
   edit → operator ruling, per the same core-invariant #6 logic ADR-29:122 already invoked.
2. **D1** — resolve the `CLAUDE.md:63` / `AGENTS.md:69` overlap, or amend the `CLAUDE.md:41`
   no-duplication claim so it stops asserting something false.
3. **U1** — decide explicitly whether `protocols/PLAYBOOK.md:666` should acquire a `commit-msg`
   mechanism or be marked advisory. Leaving it silent is the status quo defect.
4. **Lane note** — if this candidate is re-run, require the reader to return, for every negative
   claim, the exact glob it searched, and name the citation index (`docs/decisions/README.md`)
   as in-scope. N1 was caused entirely by an under-specified scope.
