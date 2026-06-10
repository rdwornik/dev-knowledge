# Codex Review — amendment-gate-11

**Date:** 2026-06-10
**Branch:** `feat/amendment-gate-11`
**HEAD:** `4b27125`
**Diff range:** `main..feat/amendment-gate-11`
**Codex version:** codex-cli 0.136.0
**Mode:** diff-review

---

## Focus

- check_amendment_coherence correctness: straggler detection, _norm_version major/full + 3.4==3.4.0 trailing-zero normalization, child-repo safety (absent anchor/surface skip), WARN-on-drift vs FAIL-on-straggler.
- Regex robustness in _COUPLED_VERSION_SETS: false-positive risk (matching historical 'v4.2 Amendment' mentions) and false-negative risk; the surfaces are CLAUDE.md + .claude/commands/handoff.md.
- Manifest design: is the _sets injection seam sound? Any way a straggler is silently missed?
- Test rigor: does the enforcement-path E2E (cmd_health exit 1) genuinely prove FAIL-blocking? Circular-testing / teeth.

---

## Findings
## Critical
(none)

## High

severity: HIGH  
file:line: `scripts/audit.py:1091`  
what: Present coupled surface files can match zero version mentions and still return PASS.  
why: If `CLAUDE.md` or `.claude/commands/handoff.md` rewords or drops the manifest-matched line, the gate reports coherence instead of surfacing drift, so a straggler can be silently missed.  
fix direction: Track matches per present surface and report zero-match surfaces as drift, with tests for present-but-unparseable surfaces.

severity: HIGH  
file:line: `scripts/audit.py:1022`  
what: The surface regex scans whole files and matches any `HANDOFF_PROCESS.md ... vN` mention, not just live authority declarations.  
why: Historical prose such as a future “HANDOFF_PROCESS.md v4.2 Amendment” note in `CLAUDE.md` or `handoff.md` can become a false FAIL when the anchor major advances, blocking the health gate on non-authoritative text.  
fix direction: Anchor regexes to the intended declaration lines, such as the `/handoff` command row and command frontmatter/source-of-truth line, or otherwise constrain matches to normative surfaces only.

## Medium
(none)

## Low
(none)
