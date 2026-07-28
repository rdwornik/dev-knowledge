"""[#437] propose_closures hub <-> plugin carrier-TWIN parity.

The plugin copy `plugins/tier1-lifecycle/scripts/propose_closures.py` is the LIVE
Stop-hook scanner (the enabled tier1-lifecycle plugin; CLAUDE.md sections 8/9). It is a
hand-mirrored port of `scripts/propose_closures.py` under ADR-78 carrier doctrine
(ships standalone into consumer repos — no shared module, no symlink), which is
exactly how the [#437] divergence class arises: nothing pinned the two copies, so
the hub's precision lever could exist without reaching the copy that runs.

This test pins the DETECTION CORE twin, following the
`test_validate_backlog_twin_parity.py` precedent split (terra design-review M2):
regexes compared by `.pattern` AND `.flags`; functions compared by
`inspect.getsource`; plus behavioral parity on the [#437] live fixtures.

The copies legitimately diverge OUTSIDE the core (host-root resolution:
$CLAUDE_PROJECT_DIR vs __file__) — only the declared twin symbols are pinned.
"""

import importlib.util
import inspect
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_HUB_PATH = _REPO / "scripts" / "propose_closures.py"
_PLUGIN_PATH = _REPO / "plugins" / "tier1-lifecycle" / "scripts" / "propose_closures.py"

# The declared detection-core twin ([#437] design note section 3 + amendment M2).
_TWIN_REGEXES = ("CLOSES_RE",)
_TWIN_REGEX_TUPLES = ("_STRIP_RES",)
_TWIN_FUNCS = ("strip_quoted_contexts", "closure_ids", "find_strong", "find_weak")


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # so inspect.getsource / linecache resolve cleanly
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def hub():
    return _load(_HUB_PATH, "pc_hub")


@pytest.fixture
def plugin():
    return _load(_PLUGIN_PATH, "pc_plugin")


@pytest.mark.parametrize("symbol", _TWIN_REGEXES)
def test_twin_regex_pattern_and_flags_identical(hub, plugin, symbol):
    h, p = getattr(hub, symbol), getattr(plugin, symbol)
    assert h.pattern == p.pattern, f"{symbol}.pattern diverged"
    assert h.flags == p.flags, f"{symbol}.flags diverged"


@pytest.mark.parametrize("symbol", _TWIN_REGEX_TUPLES)
def test_twin_regex_tuple_patterns_and_flags_identical(hub, plugin, symbol):
    hs, ps = getattr(hub, symbol), getattr(plugin, symbol)
    assert [(r.pattern, r.flags) for r in hs] == [(r.pattern, r.flags) for r in ps], (
        f"{symbol} diverged"
    )


@pytest.mark.parametrize("symbol", _TWIN_FUNCS)
def test_twin_function_source_identical(hub, plugin, symbol):
    h_src = inspect.getsource(getattr(hub, symbol))
    p_src = inspect.getsource(getattr(plugin, symbol))
    assert h_src == p_src, f"{symbol} source diverged between hub and plugin"


# --- behavioral parity on the [#437] live-fixture forms -------------------------

_FIXTURES = [
    "Verified inert: no commit carries a `closes [#370]` tag, so the stale refs",
    'the row asserted "Closes [#433] on ruling" which section 7.5 contradicts',
    "chore(backlog): closes [#434] — both Done-when clauses re-verified live",
    "fix `quoted closes [#5]` handling, closes [#6]",
]


@pytest.mark.parametrize("text", _FIXTURES)
def test_twin_behavioral_parity_on_fixtures(hub, plugin, text):
    assert hub.closure_ids(text) == plugin.closure_ids(text)


@pytest.mark.parametrize("text,expected", [
    (_FIXTURES[0], []),
    (_FIXTURES[1], []),
    (_FIXTURES[2], ["434"]),
    (_FIXTURES[3], ["6"]),
])
def test_plugin_copy_has_the_quoting_fix(plugin, text, expected):
    # the LIVE Stop-hook copy must itself carry the semantics, not just the hub
    assert plugin.closure_ids(text) == expected
