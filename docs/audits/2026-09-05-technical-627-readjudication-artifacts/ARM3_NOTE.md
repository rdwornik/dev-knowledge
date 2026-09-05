# Arm 3 — the deictic-binding control, and why it was added mid-run

Added after the SEED-k1 draw returned, before it was scored against
`SEED_RUBRIC.md`'s outcome shapes. Recorded here as a named deviation rather
than folded silently into the design, per freeze §9 / SDA-1 C-15.

## The hypothesis this arm tests

Across two independent lane runs and this one, the items agy answers **in
scope** and the items it answers **out of scope** separate cleanly on one
feature of the prompt:

- **Prompts naming a concrete in-repo path** — `docs/intake/`,
  `docs/decisions/`, `docs/intake/README.md` — were answered about
  `.dev-knowledge`. Direct evidence: agy's own generated helper
  `~/.gemini/antigravity-cli/scratch/find_unmentioned.py` opens with
  `repo_dir = r'C:\Users\1028120\Documents\Dev\.dev-knowledge'`.
- **Prompts using the bare deictic "this repository"** with no path — N-01
  ("analysing this repository", whole-repo scan), and the H5 seeded prompt
  ("You are analysing this repository") — were answered about
  `~/.gemini/antigravity-cli/scratch/repo`, a clone of
  `gitlab.knx.org/public-projects/knx-iot-point-api/knx-iot-point-api-stack.git`
  that has sat in agy's own scratch since 2026-08-26, i.e. **before both prior
  measurement runs**.

So the mechanism is not "the model wanders" (batch-F §4 D-1). It is that agy
**does not bind the deictic "this repository" to `workspaceDirs`** — the log
records the correct workspace on every draw and the answer ignores it.

## Why this matters to the verdict rather than being trivia

A REFUSE resting on scope-wandering is a verdict about the PROVIDER only if the
provider cannot be scoped. If the deictic is the whole defect, the same evidence
is a verdict about the HARNESS, and the remedy is a prompt convention, not a
refusal. The two readings differ in what `[#627]` should do next, so the freeze's
own C-7(iii) applies: an item whose two plausible readings change a gate outcome
is reported INDETERMINATE and is not resolved by the reader who noticed it.

Arm 3 resolves it by measurement instead of by argument.

## The arm

One draw, identical corpus, identical model pin, identical flags. The ONLY
change is the first clause of the prompt: the bare deictic is replaced by the
absolute path of the corpus. Everything after that clause is byte-identical to
`seed_corpus.PROMPT`.

Scored against the SAME frozen `SEED_RUBRIC.md`. No new rubric, no new bar.

```
CONTROL  deictic  ->  "You are analysing this repository."        (SEED-k1..k3)
CONTROL  explicit ->  "You are analysing the repository rooted at
                       <ABSOLUTE PATH>. Analyse ONLY files under that
                       directory."                                (SEED-explicit)
```

## What each outcome licenses, frozen before the draw

- **Explicit lands in scope, deictic does not** -> the defect is a binding
  failure the harness can work around. The batch-F cell measures a harness
  defect, and its REFUSE is evidence about how the pack was issued as much as
  about agy. Re-open condition becomes concrete and cheap.
- **Explicit ALSO lands out of scope** -> agy cannot be scoped by any means
  available to a caller. REFUSE is ratified on the strongest possible ground,
  and no prompt convention rescues it.
