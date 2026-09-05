# The verdict rule — frozen BEFORE arm 3c ran

- **Consumers:** `[#627]`, whose admission verdict this rule binds; the parent
  artifact `docs/audits/2026-09-05-technical-627-readjudication.md`, whose
  VERDICT section is required to follow it.

Committed while N-05 was still in flight and before any arm-3 draw existed.
The point is to make the verdict a function of the evidence rather than a
judgement I reach after seeing which way it fell, which is the failure this
whole re-adjudication is about.

## Why this file exists at all

Halfway through, the evidence moved against my own working hypothesis. I opened
believing the seeded 0/5 result would ratify the REFUSE. Then the pack arm on
CLI 1.1.27 came back substantially cleaner than batch-F's 1.1.22 cell — N-02
and N-10 flipped FAIL to PASS, N-04 improved from "PASS, contaminated" to a
clean uncontaminated pass that independently matched a mechanical recount
batch-F got wrong, and N-09 held, which puts the self-kill gate N4 at 2/2
rather than batch-F's regressed 1/2.

That leaves exactly one live failure mode — the bare deictic "this repository" —
and my seeded corpus is confounded on precisely that axis: it is deictic AND it
is not a git repository, while every tree the pack ran against was one.

So my headline result may be my own artifact. Arm 3c settles it, and the rule
below is written before it runs.

## The evidence sets

```
A  batch-F's own record, arithmetic corrected: 2 PASS / 6 FAIL / 1 UNCALIBRATED
   on agy 1.1.22. NOT re-verifiable -- the CLI moved and no artifacts survived.
   Carries five verified defects (D-A..D-E), one of which fires the very
   fabrication clause batch-F was applying.
B  this lane, agy 1.1.27, the frozen pack against .dev-knowledge.
C  this lane, seeded corpus, deictic prompt, NON-git directory: 0/5 at k=3.
D  arm 3c -- byte-identical corpus that IS a git repository. PENDING.
E  arms 3a / 3b -- absolute path in the prompt; --add-dir. PENDING.
```

## The rule

**If D finds the planted defects** (recall >= 3/5, inventions 0, on either draw):
then C is substantially an artifact of my own harness, not a provider property.
Set A is non-reproducible and defective; set B is near-clean. In that case the
honest verdict is **INCONCLUSIVE**, because:
  - the REFUSE cannot be *ratified* on evidence that no longer reproduces and
    that fails its own gate; and
  - it cannot be *flipped to ADMIT* either, because no clean, in-scope, k>=3
    admission run against the ruled bar has ever been completed under a pinned
    CLI. Absence of a demonstrated failure is not a demonstrated pass.

**If D also wanders or scores 0/5:** C is a real provider property, reproduced
on a git repository, on a fresh corpus, on the current build. The ruled
admission bar fails on its own terms and the verdict is **RATIFY REFUSE**, with
the claim reclassified from "fabricates" to "cannot be scoped".

**E does not change the verdict either way.** It changes only the RE-OPEN
CONDITION: if an absolute path or `--add-dir` binds the workspace, re-opening is
cheap and mechanical; if neither does, re-opening requires a vendor fix and the
condition must say so.

## What I will not do

I will not report INCONCLUSIVE as a hedge if D fails, and I will not report
RATIFY REFUSE to preserve the shape of the work already written if D passes.
The sections already committed (D-A..D-E, the corrected 9/9 cell) stand on their
own evidence and are unaffected by which way D falls — they are findings about
batch-F's reasoning, not about the verdict.
