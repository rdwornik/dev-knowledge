"""dk-harness-probe -- the ADR-123 step-0 stand-in (not the harness; see ../../pyproject.toml).

Two verbs, deliberately dependency-free so the install under test is the git-URL mechanism and
nothing else:

    dk-harness-probe install <dest>   materialise a one-plugin marketplace from package data
    dk-harness-probe check            the "organ": report the installed version, call nothing
"""
from __future__ import annotations

import json
import logging
import sys
from importlib import metadata, resources
from pathlib import Path

logger = logging.getLogger("dk-harness-probe")

PLUGIN_NAME = "dk-harness-probe"
MARKETPLACE_NAME = "dk-harness-probe-local"
ORGAN_MARKER = "dk-harness-probe check ok"

# package-data file -> path inside the plugin root
_LAYOUT = {
    "plugin.json": (".claude-plugin", "plugin.json"),
    "hooks.json": ("hooks", "hooks.json"),
    "witness.py": ("hooks", "witness.py"),
}


def _version() -> str:
    try:
        return metadata.version(PLUGIN_NAME)
    except metadata.PackageNotFoundError:
        return "0.0.0+source"


def materialise(dest: Path | str) -> Path:
    """Write a marketplace at ``dest`` holding this package's plugin; return the plugin root.

    Idempotent: every file is rewritten from package data on each call.
    """
    dest = Path(dest)
    plugin_root = dest / "plugins" / PLUGIN_NAME
    data = resources.files(__package__).joinpath("plugin_data")
    for name, parts in _LAYOUT.items():
        target = plugin_root.joinpath(*parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data.joinpath(name).read_bytes())
    marketplace = {
        "name": MARKETPLACE_NAME,
        "owner": {"name": "Rob (.dev-knowledge methodology hub)"},
        "plugins": [{"name": PLUGIN_NAME, "source": f"./plugins/{PLUGIN_NAME}",
                     "description": "ADR-123 step-0 probe plugin"}],
    }
    (dest / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (dest / ".claude-plugin" / "marketplace.json").write_text(
        json.dumps(marketplace, indent=2) + "\n", encoding="utf-8"
    )
    return plugin_root


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(format="%(message)s", level=logging.INFO, stream=sys.stdout)
    args = list(sys.argv[1:] if argv is None else argv)
    if args[:1] == ["check"]:
        logger.info("%s version=%s", ORGAN_MARKER, _version())
        return 0
    if len(args) == 2 and args[0] == "install":
        root = materialise(args[1])
        logger.info("materialised plugin %s at %s", PLUGIN_NAME, root)
        return 0
    logger.error("usage: dk-harness-probe install <dest> | dk-harness-probe check")
    return 2
