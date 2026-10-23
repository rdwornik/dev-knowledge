from __future__ import annotations

from pathlib import Path

import yaml

_REPO = Path(__file__).resolve().parents[1]
_WORKFLOW = _REPO / ".github" / "workflows" / "conductor.yml"


def test_commit_gate_seeds_local_main_before_audit_health():
    workflow = yaml.safe_load(_WORKFLOW.read_text(encoding="utf-8"))
    audit_jobs = {
        name: job["steps"]
        for name, job in workflow["jobs"].items()
        if any("pre-commit run audit-health" in step.get("run", "")
               for step in job.get("steps", []))
    }
    assert "commit-gate" in audit_jobs, "commit-gate must run the audit-health hook"

    for job_name, steps in audit_jobs.items():
        audit_indexes = [
            index for index, step in enumerate(steps)
            if "pre-commit run audit-health" in step.get("run", "")
        ]
        for audit_index in audit_indexes:
            earlier_runs = [step.get("run", "") for step in steps[:audit_index]]
            assert any(
                "git branch main origin/main" in run
                and "refs/heads/main" in run
                for run in earlier_runs
            ), (f"{job_name} must create refs/heads/main from origin/main before "
                "pre-commit runs audit-health")
