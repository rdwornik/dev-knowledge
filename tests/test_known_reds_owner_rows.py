from __future__ import annotations

import json
import re
from datetime import date, timedelta
from pathlib import Path

import yaml

_REPO = Path(__file__).resolve().parents[1]
_REFERENCE_DATE = date(2026, 10, 23)


def test_expiring_known_reds_name_open_task_rows():
    registry = json.loads((_REPO / "logs" / "KNOWN-REDS-REGISTRY.json").read_text(
        encoding="utf-8"))
    entries = []
    entries.extend(("members", key, value) for key, value in registry.get("members", {}).items())
    for os_name, members in registry.get("members_by_os", {}).items():
        entries.extend((f"members_by_os[{os_name}]", key, value)
                       for key, value in members.items())
    entries.extend(("hooks", key, value) for key, value in registry.get("hooks", {}).items())

    deadline = _REFERENCE_DATE + timedelta(days=30)
    expiring = [
        (group, key, entry)
        for group, key, entry in entries
        if entry.get("expiry")
        and _REFERENCE_DATE <= date.fromisoformat(entry["expiry"]) <= deadline
    ]
    assert expiring, "the fixed 30-day window must cover registry entries"

    for group, key, entry in expiring:
        task = entry.get("task", "")
        match = re.fullmatch(r"\[#(\d+)\]", task)
        assert match, f"{group}[{key}] expiring {entry['expiry']} must name one task row: {task!r}"
        row_id = match.group(1)
        rows = list((_REPO / "tasks").glob(f"{row_id}-*.md"))
        assert rows, f"{group}[{key}] names missing task row #{row_id}"
        for row in rows:
            text = row.read_text(encoding="utf-8")
            frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
            assert frontmatter, f"task row #{row_id} has no readable YAML frontmatter: {row}"
            metadata = yaml.safe_load(frontmatter.group(1)) or {}
            assert metadata.get("status") == "open", (
                f"{group}[{key}] expires {entry['expiry']} but task row #{row_id} is "
                f"{metadata.get('status')!r}, not open")
