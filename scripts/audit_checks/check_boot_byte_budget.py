"""`check_boot_byte_budget` — extracted from `scripts/audit.py` by [#533].

Moved BYTE-IDENTICAL. The `# rule: handoff-boot-budget` annotation above the `def` travels
with it — it is one of the two declared sites for that rule (the other is
`assemble_paste.py`), so dropping it would break the pinned 2-site count in
`ecosystem/doc-code-edge.yaml`. The `assemble_paste` dual-import is reproduced in `audit.py`'s
`scripts.`-first order and `audit.py` re-exports `_assemble_paste` from here.
"""

from __future__ import annotations

from pathlib import Path

from ._common import _na, Finding

# [#446] A10 item 2 / R4 — the boot byte budget lives ONCE, in the assembler that also warns
# on it; this check reads the constant rather than re-declaring the number. Same shape.
try:
    from scripts import assemble_paste as _assemble_paste
except ImportError:
    import assemble_paste as _assemble_paste


# rule: handoff-boot-budget
def check_boot_byte_budget(repo_path: Path) -> list[Finding]:
    """A10 item 2 / R4 ([#446]): `protocols/HANDOFF_BOOT.md` stays within its stated numeric
    byte budget — 18,000 bytes, ruled 2026-07-31 (architect technical lane).

    WHY A GATE AND NOT JUST A WARN (operator ruling 2026-07-31). Enforcement is split by
    site: `assemble_paste.py` WARNs and still assembles, so an over-long boot stays
    GENERATABLE; this check FAILs, so it stops being SHIPPABLE. The guarantee belongs in the
    organ that blocks the merge — a warning nobody has to clear is how the 36.5 KB -> 59 KB
    paste creep happened in the first place (the precedent that motivated a budget at all).

    The budget VALUE is single-sourced from `assemble_paste.HANDOFF_BOOT_BYTE_BUDGET`, never
    re-declared here: two organs enforcing the same rule against two different numbers is the
    drift this pairing exists to prevent. Scope is the boot file ALONE — the per-bundle
    session header is explicitly NOT governed by it (R4), and the assembled `PASTE_THIS.md`
    keeps its own separate `_SIZE_WARN_BYTES` budget.

    Portable: every repo with a `protocols/HANDOFF_BOOT.md` is measured. Absent file -> n/a
    (a consumer that has not adopted the browser boot is not in breach). Read-only.
    """
    boot = Path(repo_path) / "protocols" / "HANDOFF_BOOT.md"
    if not boot.exists():
        return [_na("boot_byte_budget", "NOT-APPLICABLE",
                        "no protocols/HANDOFF_BOOT.md — repo has not adopted the browser boot")]
    try:
        size = len(boot.read_bytes())
    except OSError as exc:
        return [Finding("boot_byte_budget", "warn",
                        f"could not read protocols/HANDOFF_BOOT.md: {exc!r}".replace("|", "/"))]
    budget = _assemble_paste.HANDOFF_BOOT_BYTE_BUDGET
    if size > budget:
        return [Finding("boot_byte_budget", "fail",
                        f"protocols/HANDOFF_BOOT.md is {size} bytes, over its {budget}-byte "
                        f"budget by {size - budget} — trim the browser role file "
                        f"(A10 item 2 / R4)")]
    return [Finding("boot_byte_budget", "pass",
                    f"protocols/HANDOFF_BOOT.md is {size} bytes, within its {budget}-byte budget")]
