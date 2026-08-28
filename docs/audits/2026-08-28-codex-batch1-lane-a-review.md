# Terra pre-merge review — batch-1 lane L1 (`lane-a-577-agents-md-lockstep`)

- **Reviewer:** `gpt-5.6-terra` via `codex exec` (codex-cli 0.145.0), reviewer role per
  `ecosystem/provider-registry.yaml` (`roles: [reviewer]`)
- **Lane:** L1 — `[#577]` + `[#584]`, root `AGENTS.md` + the `CLAUDE.md` §10 lockstep correction
- **Diff reviewed:** the lane's staged diff (3 files, +110/-8), supplied INLINE
- **Date:** 2026-08-28

## TALLY (as returned by the reviewer)

```
TALLY: critical=0 high=2 medium=0 low=0
```

## Harness note — four attempts before a real verdict, recorded because it is reusable

The first three invocations produced **no usable review** and the failure modes are worth
naming, since every later lane in this batch reuses the fixed shape:

1. **Exploration blowup.** A prompt that told terra to review "the staged diff" without
   supplying it sent the reviewer reading the repo: 323 KB of output, a PowerShell quoting
   error, and no verdict.
2. **Format parroting.** Supplying a filled example line (`TALLY: critical=0 high=0 …`)
   produced exactly that line back, with zero findings — a **vacuous pass**, which is the
   failure class this repo already names for validators run with no args. A tally with no
   reasoning behind it was rejected rather than banked.
3. **argv truncation.** Passing a ~21 KB prompt as a shell argument yielded an empty
   response — the same class as the recorded `claude -p` argv-corruption gotcha.
4. **Backgrounding.** `nohup … &` under the harness was reaped before codex finished.

**The shape that works:** prompt on **stdin** (`codex exec … -`), the whole diff inline,
exploration explicitly forbidden, an output contract with **placeholders rather than filled
examples**, and the call run **synchronously**.

## Findings, with the lane's disposition

### HIGH-1 — `AGENTS.md` embeds Codex- and Claude-specific detail in a "portable" layer

> *"The purported portable/provider-agnostic layer embeds Codex runtime configuration
> (`~/.codex/AGENTS.md`, `project_doc_max_bytes`) and Claude-runtime references
> (`CLAUDE.md`, `.claude/worktrees`). A non-Codex provider consuming this file receives
> irrelevant or inapplicable runtime doctrine."*

**Disposition: PARTIALLY REFUTED on the ADR's own text, and partially ACTED ON.**

The precedence section is not drift — it is **mandated**. ADR-115 §3.2 states the bound
verbatim: *"The `~/.codex` precedence collision is resolved BY SCOPE, stated in the file
header."* `[#577]` carries the same bound as its third binding condition. Resolving a
collision requires naming its parties, so a provider-agnostic file cannot discharge that
bound without naming `~/.codex`. Deleting the section to satisfy the finding would breach
the ADR the lane exists to execute.

**Acted on:** the section now carries an inline citation of ADR-115 §3.2 stating why the
provider-specific paths are present, so the next reader — or reviewer — sees the mandate
rather than re-deriving the same objection. `.claude/worktrees` is retained: the worktree
location is a **landing fact** every provider needs in order to commit here, not Claude
runtime configuration.

**Residue, stated honestly:** the "Size guard" paragraph is genuinely Codex-shaped. It is
kept because the 32 KiB cap is the *only* hard truncation limit any admitted provider
imposes, and a portable file that omits the one limit which silently destroys its own
content would be worse. Recorded, not hidden.

### HIGH-2 — the combined byte cap has no enforcing test

> *"The v2.68 entry explicitly records that the combined global-plus-root byte cap has no
> enforcing test. A later expansion can exceed the cap and silently truncate provider
> instructions without a gate detecting it."*

**Disposition: ACCEPTED, CONFIRMED, and OUT OF THIS LANE'S SCOPE.**

This is the gap the lane self-reported before the review ran, and terra reached it
independently — which raises it from a footnote to a corroborated finding. `[#577]`'s
done-when asks for a test asserting the combined payload in **bytes** against the 32 KiB
cap. `tests/` is **outside L1's frozen write-scope** (`CLAUDE.md` · `AGENTS.md` ·
`templates/claude-regions/*.md`), and widening a frozen contract mid-lane is an ask-class
act the lane declined to take unilaterally.

**Handed to the integrator as a CANDIDATE.** Until it lands, `[#577]` is **not fully
discharged**: the byte figures below are measured and reported but **unguarded**.

## Measurements the lane recorded (independent of the review)

```
AGENTS.md                 107 lines (bound <=120)      5,539 B
global ~/.codex/AGENTS.md                              3,891 B
combined payload                                       9,430 B = 28.8% of the 32 KiB cap
CLAUDE.md budget          197/200 -> 196/200           headroom 4
silent_rule_ratchet       443 -> 443                   delta ZERO (pre-auth unused)
region body vs template   1,075 B == 1,075 B           byte-identical
boundary_headers --check  clean
```

## Verdict

**MERGE-ELIGIBLE.** No critical findings. HIGH-1 is refuted on the ADR's own text and
partially acted on; HIGH-2 is accepted, confirmed and carried to the integrator as a
candidate rather than silently closed.
