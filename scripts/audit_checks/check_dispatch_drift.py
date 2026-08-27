"""`check_dispatch_drift` — the `[#592]` dispatch drift organ as a registered gate.

The thin ADAPTER half; the logic lives in `scripts/dispatch_drift.py`. Same module-import +
thin-adapter shape as `check_adr_status_grammar` / `check_substrate_declaration`.

WHY IT IS A GATE AND NOT A NOTE. `protocols/STANDING_RULINGS.md` section V closes with its own
honest limit: *"The drift organ that would assert every literal command in Ch8 resolves via
`Get-Command` on the operator's machine, and that `/lane-boot` names the ruled verb, is owed
and unbuilt; until it exists these rulings bind the seat and not the tree."* Registering it
here is what moves those rulings from the seat to the tree.

TIER IS REPORTED, NEVER SKIPPED — intake #52's open question 2, answered as the requirement
answers it. On a host with a PowerShell the resolution leg runs for real and an unresolvable
command is a **fail**. On a host without one (CI, a container, a cloud lane) the leg reports a
**warn** naming the tier and every command it did not resolve.

`warn` AND NOT `unavailable`, deliberately, because this check's entire subject is
machine-dependence and getting it wrong here would be self-refuting. `audit.py`'s
`_STATUS_LABEL` renders `unavailable` as "N/A", `_check_outcome` projects it onto `pass`, and
`cmd_ship_gate` blocks only on `fail` plus undispositioned `warn` — so an `unavailable` verdict
SHIPS GREEN having measured nothing. That is the green-by-skip class the 2026-08-25 sweep
closed, and `check_silent_rule_ratchet` refused the same word for the same reason at terra HIGH
on 2026-07-27.

THE ORGAN NEVER DEGRADES TO MEASURING NOTHING. Leg 2 (`/lane-boot` names the ruled verb, and
carries no copyable rival launch form) reads two files and is host-independent, so it runs on
every tier. A shell-less host still gets a real verdict on the half that does not need a shell.

MEASURED BEFORE ARMING. On the live tree at arm time: tier `host`, 12 literal commands
extracted from Ch8's dispatch table, all 12 resolving; `/lane-boot` names the ruled verb
`dispatch` in a fence and its one prose mention of the raw `claude --worktree` form is the
file's own labelled supersession note, which the label predicate admits. The check measures
**0 findings**, so arming its FAIL leg cannot RED a clean tree — the evidence bar
`check_adr_status_grammar` used for its own FAIL-armed legs.

COST, stated because this check spends a subprocess on a hook that already costs ~200 s: ONE
`pwsh -NoProfile` invocation resolving every command at once, ~1 s. A per-command spawn would
have been twelve.

HONEST LIMITS — the logic module's own, restated because they bound a green verdict:
  * resolution says a name EXISTS on this PATH, not that it is the right implementation;
  * the corpus is Ch8's dispatch-table section, which is sound only while the
    "SOLE literal-command site" ruling holds — and this organ does not enforce that ruling;
  * a `host`-tier green is a claim about the machine that ran it and no other seat's.

Child-repo-safe: a repo with no `protocols/PLAYBOOK.md` or no `/lane-boot` yields `n/a`
(subject-absent), not a FAIL. Read-only (Layer 2): no git, no writes.
"""

from __future__ import annotations

from pathlib import Path

from ._common import Finding, _na, _NA_SUBJECT_ABSENT

try:
    from scripts import dispatch_drift as _dd
except ImportError:
    import dispatch_drift as _dd

CHECK_NAME = "dispatch_drift"


def check_dispatch_drift(repo_path: Path) -> list[Finding]:
    """`[#592]`: every literal command in Ch8's dispatch table resolves, and `/lane-boot`
    names the ruled verb.

    One Finding PER concern, never a bundle. The `#147` disposition register suppresses an
    ENTIRE Finding on a substring match, so a bundled Finding would let one dispositioned
    command wave through every other drift beside it.
    """
    root = Path(repo_path)
    missing = [rel for rel in (_dd.PLAYBOOK_RELPATH, _dd.LANE_BOOT_RELPATH)
               if not (root / rel).is_file()]
    if missing:
        return [_na(CHECK_NAME, _NA_SUBJECT_ABSENT,
                    f"no {' / '.join(missing)} — this repo carries no dispatch surface")]

    try:
        tier, findings, commands = _dd.scan(root)
    except _dd.DispatchDriftError as exc:
        # FAIL, not "unavailable": an unreadable or unlocatable corpus reports zero drift,
        # which is precisely what a broken scan looks like.
        return [Finding(CHECK_NAME, "fail",
                        f"the dispatch corpus could not be scanned, so no command was "
                        f"checked: {exc}".replace("|", "/"))]

    out = [Finding(CHECK_NAME, f.status, f"[{f.leg}] {f.detail}".replace("|", "/"))
           for f in findings]
    if not out:
        out.append(Finding(
            CHECK_NAME, "pass",
            f"tier {tier}: {len(commands)} literal command(s) in "
            f"{_dd.PLAYBOOK_RELPATH} Ch8's dispatch table resolve, and "
            f"{_dd.LANE_BOOT_RELPATH} names the ruled verb {_dd.RULED_VERB!r}"))
    return out
