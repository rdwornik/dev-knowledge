# Evidence -- claims_bad

## Subagent claims

- decide_checks.py exists in scripts/ {probe: scripts/does_not_exist_decide_fixture.py:1}
- pyyaml is a declared dependency {probe: grep -c 'no_such_token_xyz' pyproject.toml}
- a claim with no marker of any kind
