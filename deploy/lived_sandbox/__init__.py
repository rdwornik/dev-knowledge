"""Lived-workflow sandbox — proves the COMPOSED hub workflow runs end-to-end in a real
headless Claude Code session (Fable architecture review 2026-07-04 §6).

Slice A (this scaffold): the isolated `claude -p` SPAWN + clone/teardown + the isolation proof
(the correctness property — the child does NOT inherit the outer machine's ~/.claude L0 hooks).
Slice B (post-review): the deterministic observer + engages-spec oracle + the six-hook arc.

Layer-2-safe: every mutation lands under a tempfile.mkdtemp root that _rmtree_guarded refuses to
escape; no live sibling is ever touched. Not a worktree (ADR-68), not a container (Windows-native
fidelity is the point). The inner session is ONLY a stimulus generator; the outer layer reads
state, never trusts narration (LESSONS 2026-06-04).
"""
