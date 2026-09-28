# Evidence -- claims_good

## Subagent claims

- decide_checks.py exists in scripts/ {probe: scripts/decide_checks.py:1}
- pyyaml is a declared dependency {probe: grep -c 'pyyaml' pyproject.toml}
- .venv is gitignored {probe: git check-ignore .venv/pyvenv.cfg}
- this cannot be recovered from the transcript {unverified}
