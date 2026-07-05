"""Lived-workflow sandbox — proves the COMPOSED hub workflow runs end-to-end in a real
headless Claude Code session (Fable architecture review 2026-07-04 §6).

Slice A: the isolated `claude -p` SPAWN + clone/teardown + the isolation proof (the correctness
property — the child does NOT inherit the outer machine's ~/.claude L0 hooks). Modules:
`spawn` / `isolation` / `cli prove-isolation`.
Slice B ([#252]): the acceptance instrument — an OUTER deterministic observer proving
enforcement-in-effect (not presence) on a real six-hook branch->edit->commit->wrap arc, with the
essence-spec's `engages:` triples as the oracle. Modules: `oracle` (load the expectations) /
`observe` (verdict from transcript-events + hook-stdout + git-state, NEVER narration — C1) /
`arc` (consumer-shape the clone, run the arc, GATE-0 isolation-only) / `cli observe-arc`. The
closure proof (C4) is the discrimination between a frozen arc-green fixture (all six fired) and a
frozen arc-silent fixture (one gated hook disabled -> FLAGGED); both are captured by the operator's
live `observe-arc --freeze` run.

Layer-2-safe: every mutation lands under a tempfile.mkdtemp root that _rmtree_guarded refuses to
escape; no live sibling is ever touched. Not a worktree (ADR-68), not a container (Windows-native
fidelity is the point). The inner session is ONLY a stimulus generator; the outer layer reads
state, never trusts narration (LESSONS 2026-06-04).
"""
