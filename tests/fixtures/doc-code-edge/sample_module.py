"""Sample module for the doc-code-edge move-safety spike fixture (#194).

Neutral name (NOT test_*.py) so pytest never collects it; lives under tests/fixtures/
(NOT scripts/) so the real ship-gate never sees a stray TEST-01 annotation.
"""


def do_thing():
    # rule: TEST-01
    return 42
