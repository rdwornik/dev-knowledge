# SESSION lane-dz-0-m1-model-probe -- PARTIAL

what is now true: tasks a-d, their keys, validated deterministic checks, `probe.py`, and one measured Copilot cell exist under
`scratch/m1-model-probe/`; the 12 Claude cells and the blind grading are NOT run (no headless Claude login). Details: `RESULT.md`.
value: the harness is ready to produce the model/effort table with one login; no number in it is estimated.
self-check: reference RED test fails on base with `assert 5 == 0`, green under the reference fix; seeded task c RED, green after the original fix with `tests/test_transport.py` 254 passed (with the new tests).
purity: the branch carries only `scratch/m1-model-probe/**` over base `d8aa4dd7`.
model served per step: Copilot cell -- UNVERIFIED; Claude cells -- none ran (USD 0.00).
DECIDED-BY-LANE: task c re-seeded to the pre-fix lock because [#1350] is already fixed at base (a9ae5280).
DECIDED-BY-LANE: claim exit 2 (no transport) treated as an environment fault, not contention; no marker written.
OPERATOR-ACTION: provide a Claude login to the lane's tool environment, then run the 12 cells (see RESULT.md).
USD by model/effort: all 0.00 (claude-haiku-5-5: 0, claude-sonnet-5-5: 0); Copilot: 17.32 AI Credits, up 290.2k / down 1.8k tokens.

HANDBACK worktree-lane-dz-0-m1-model-probe @ 5e98a7c9 docs
