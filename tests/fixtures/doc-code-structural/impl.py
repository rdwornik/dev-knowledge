"""Structural-integrity fixture — code side (#194 L1 scan).

Neutral name (NOT test_*.py) so pytest never collects it; lives under tests/fixtures/ (NOT
scripts/) so the real ship-gate never sees these `# rule:` annotations. Companion to doc.md;
see that file for the per-rule-ID structural states this encodes.
"""


def clean():
    # rule: clean-ok
    return 1


def orphan():
    # rule: code-orphan-1
    return 2


def dup_doc_anchor():
    # rule: dup-doc-1
    return 3


def dup_code_first():
    # rule: dup-code-1
    return 4


def dup_code_second():
    # rule: dup-code-1
    return 5
