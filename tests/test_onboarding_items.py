"""The onboarding check as a repository test: of the 13 things a fresh architect seat must know
(`to-cc/BATCH-ONBOARDING-CHECK-2026-10-02.md`), how many does the seat find in
`protocols/HANDOFF_BOOT.md` plus the generated rows of a FRESH trial cut? (batch FOUNDATION lane 3,
`foundation-3-handoff-boot`, Done-contract item 8; baseline 2/13 per DIGEST-CI-TRIAGE section 3.)

THE SURFACES, exactly two: `protocols/HANDOFF_BOOT.md` (RESIDENT, never inlined in PASTE_THIS --
`assemble_paste.py` ROLE PIN) and the BOOT-DATA rows of a bundle cut now (`gen_handoff.generate(...,
dry_cut=True)`, into a tmp dir outside the repository). Nothing else counts: not the residual, not
the supplement, not a READ FIRST transport file. A fact that can go stale belongs in a generated row
(Value line), so the volatile items (6, 7, 8, 12) are asserted on ROW KEYS, and the prose items on
phrases that name their rule.

No platform skip, no network: the cut runs against a FIXTURE transport (the same plumbing as
`tests/test_handoff_cut_acceptance.py`, whose host-dependent probes are pinned the same way); the one
live read, the CI row, degrades to a visible `unavailable` value and is still a row.

The integrator runs this file; an isolated session then runs the onboarding check on the same bundle.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import pytest

import audit as aud  # noqa: F401 -- imported so the cut's organ set resolves as in the acceptance test
import gen_handoff as gh
import verify_handoff_probes as vhp

try:                                              # same resolution order as the acceptance test
    from scripts import dispatch_drift as dd
except ImportError:                               # pragma: no cover
    import dispatch_drift as dd

_REPO = Path(__file__).resolve().parents[1]
_BOOT = _REPO / "protocols" / "HANDOFF_BOOT.md"

ITEMS = {
    1: "role and equilibrium",
    2: "goal, plan order, feature freeze",
    3: "where live truth is, what working means",
    4: "dispatch step by step, paste addressing",
    5: "what the harness does not do by itself",
    6: "every ruling in force, which are not yet landed",
    7: "open decisions and dated pressures",
    8: "CI, known reds, triage first",
    9: "failures before any summary",
    10: "the no-assert rule",
    11: "cut prerequisites",
    12: "current model availability",
    13: "context budget",
}


def _section(boot: str, title_re: str) -> str:
    m = re.search(rf"(?m)^#{{2,3}} {title_re}.*$", boot)
    if m is None:
        return ""
    nxt = re.search(r"(?m)^#{2,3} ", boot[m.end():])
    return boot[m.start(): m.end() + nxt.start()] if nxt else boot[m.start():]


def _row(rows: "dict[str, str]", key: str) -> str:
    return rows.get(key, "")


def evaluate(boot: str, rows: "dict[str, str]") -> "dict[int, tuple[bool, str]]":
    """item -> (found, evidence). `boot` is protocols/HANDOFF_BOOT.md; `rows` the cut's BOOT-DATA
    `key -> value`. Each predicate names the rule it looks for, so a passing item says why."""
    low = boot.lower()
    out: "dict[int, tuple[bool, str]]" = {}

    out[1] = ("R47.1" in boot and "R41" in boot and "junior" not in low
              and bool(re.search(r"reads? no code|does not read code", low)),
              "HANDOFF_BOOT names R41 + R47.1, the browser reads no code, and no 'junior'")
    out[2] = ("R46.4" in boot and "freeze" in low and "master plan" in low and "Batches" in rows,
              "the master-plan pointer + R46.4 feature freeze in HANDOFF_BOOT + the generated Batches row")
    out[3] = ("STATE-BATCH" in boot and "idle" in low and "CI" in rows,
              "STATE-BATCH/digest sources + 'idle' caveat in HANDOFF_BOOT + the CI row")
    out[4] = ("dispatch.py launch --help" in boot and "names its target" in low
              and "seat order" in low and "queue" in low and "render" in low,
              "launcher --help pointer, seat order, render, queue + 'names its target' (paste addressing)")
    sec5 = _section(boot, "What the harness does not do by itself")
    out[5] = (len(re.findall(r"(?m)^- ", sec5)) >= 4
              and all(t in sec5.lower() for t in ("registry", "manual_until", "daemon", "usage limit")),
              f"section 'What the harness does not do by itself' with {len(re.findall(r'(?m)^- ', sec5))} bullets"
              " naming registry-at-launch, manual_until, the daemon resume and usage limits")
    out[6] = ("Rulings" in rows and "Landed" in rows and "STANDING_RULINGS.md" in boot
              and not re.search(r"R1\s?[–-]\s?R\d+", boot) and bool(re.search(r"R\d+", _row(rows, "Landed"))),
              "Rulings + Landed rows, a STANDING_RULINGS.md pointer, and no hard-coded range in the prose")
    out[7] = ("Decisions" in rows and "Dates" in rows and "evidence:" in _row(rows, "Decisions")
              and "evidence:" in _row(rows, "Dates") and bool(re.search(r"\d{4}-\d{2}-\d{2}", _row(rows, "Dates"))),
              "Decisions + Dates rows, each with an evidence locator, Dates carrying dates")
    out[8] = ("CI" in rows and "known_reds.py compare" in boot and "triage" in low,
              "CI row + 'known_reds.py compare' + the triage-first rule")
    out[9] = ("R46.6" in boot and "quote them first" in low,
              "R46.6 + 'quote them first'")
    out[10] = (bool(re.search(r"quotes? the code line", low)),
               "'quotes the code line' (no-assert rule)")
    out[11] = ("gen_handoff.py --help" in boot and "--preflight-only" in boot,
               "cut command's own --help + --preflight-only (O-5 pointer, no recited list)")
    out[12] = ("Models" in rows and "not live availability" in _row(rows, "Models")
               and "implement" in _row(rows, "Models"),
               "Models row, labelled routing order and not live availability")
    out[13] = (bool(re.search(r"30\s?%", boot)) and bool(re.search(r"60\s?%", boot)),
               "30 % verification reserve and ~60 % cut point")
    return out


def report(found: "dict[int, tuple[bool, str]]") -> str:
    n = sum(1 for ok, _ in found.values() if ok)
    lines = [f"ONBOARDING {n}/{len(ITEMS)}"]
    lines += [f"  {i:>2} {'PRESENT' if found[i][0] else 'MISSING'} -- {ITEMS[i]}"
              for i in sorted(found)]
    return "\n".join(lines)


# --- the fresh trial cut ---------------------------------------------------------------------

def _fixture_transport(tmp_path: Path, today: str) -> Path:
    t = tmp_path / "transport"
    (t / "to-browser").mkdir(parents=True)
    (t / "to-cc").mkdir(parents=True)
    (t / "to-browser" / "LEDGER-dev-knowledge.md").write_text(f"refreshed {today}\n", encoding="utf-8")
    (t / "to-browser" / f"RATIFICATION-{today}.md").write_text(
        "# Ratification -- test fixture\n\n## R70 — a fixture ruling\n\n## R71 — another\n", encoding="utf-8")
    (t / "to-cc" / "BATCH-FIXTURE-OPEN.md").write_text(
        "carried-by: OPEN\nlands-via: a fixture\n\n# an open decision\n", encoding="utf-8")
    return t


@pytest.fixture(scope="module")
def trial_cut(tmp_path_factory):
    """ONE fresh trial cut of this branch; yields (boot text, BOOT-DATA rows dict)."""
    mp = pytest.MonkeyPatch()
    tmp_path = tmp_path_factory.mktemp("onboarding")
    today = date.today().isoformat()
    mp.setenv("CLAUDE_PROMPTS_DIR", str(_fixture_transport(tmp_path, today)))
    mp.setattr(gh, "_linked_worktrees", lambda repo_root: [])
    mp.setattr(dd, "find_powershell", lambda: "pwsh-fixture")
    mp.setattr(dd, "resolve_via_get_command",
               lambda names, **kw: [dd.Resolution(n, True, "fixture: resolved") for n in names])
    memory = tmp_path / "MEMORY.md"
    memory.write_text("# memory fixture\n", encoding="utf-8")
    try:
        result = gh.generate(
            gh._REPO_ROOT, mode="architect", slug="onboarding-trial", repo=".dev-knowledge",
            date=today, bundle_root=tmp_path / "dry-cut-out", assemble=True, dry_cut=True,
            memory_path=memory, sessions_root=tmp_path / "no-sessions-store")
        text = (result.bundle_dir / "HANDOFF_BOOT.md").read_text(encoding="utf-8")
        rows, _prose = vhp.parse_boot_blocks(text)
        yield _BOOT.read_text(encoding="utf-8"), dict(rows or [])
    finally:
        mp.undo()


def test_a_fresh_seat_finds_all_13_onboarding_items(trial_cut):
    boot, rows = trial_cut
    found = evaluate(boot, rows)
    n = sum(1 for ok, _ in found.values() if ok)
    print("\n" + report(found))                       # shown with -s and in the failure report
    assert n == len(ITEMS), report(found)


# --- the predicates are not vacuous (every leg, no cut) --------------------------------------

_FULL_BOOT = """\
Role: R41 and R47.1 -- the browser reads no code; CC leads and challenges every order.
Plan: the master plan; R46.4 feature freeze.  Live truth: to-browser/STATE-BATCH-X.md; a session shown as working may be idle.
Dispatch: `uv run --locked python scripts/dispatch.py launch --help`; seat order, render, queue; every paste names its target.
## What the harness does not do by itself
- registry is not read at launch
- manual_until is never read
- the daemon may resume a stopped job
- usage limit is recorded nowhere
Rules: protocols/STANDING_RULINGS.md.  Triage CI first: `known_reds.py compare`.
Failures: R46.6 -- quote them first.  A ruling about a mechanism quotes the code line.
Cut: `gen_handoff.py --help`, `--preflight-only`.  Context: keep 30 % for verification, cut at ~60 %.
"""
_FULL_ROWS = {
    "Batches": "no batch open", "CI": "x", "Rulings": "R1–R9", "Landed": "through R9 — evidence: f",
    "Decisions": "1 — evidence: f", "Dates": "2026-10-04 ×1 — evidence: f",
    "Models": "registry routing order (not live availability): implement x",
}


def test_the_predicates_pass_on_a_complete_fixture():
    found = evaluate(_FULL_BOOT, _FULL_ROWS)
    assert all(ok for ok, _ in found.values()), report(found)


@pytest.mark.parametrize("item,mutate", [
    (1, lambda b, r: (b + "\nCC is your junior.", r)),
    (2, lambda b, r: (b.replace("the master plan; ", ""), r)),
    (3, lambda b, r: (b.replace("STATE-BATCH", "STATE"), r)),
    (4, lambda b, r: (b.replace("names its target", ""), r)),
    (5, lambda b, r: (b.replace("## What the harness does not do by itself", "## Other"), r)),
    (5, lambda b, r: (b.replace("- manual_until is never read\n", ""), r)),
    (8, lambda b, r: (b.replace("known_reds.py compare", ""), r)),
    (10, lambda b, r: (b.replace("quotes the code line", ""), r)),
    (6, lambda b, r: (b + "\nrulings R1–R54 are in force", r)),
    (7, lambda b, r: (b, {k: v for k, v in r.items() if k != "Dates"})),
    (9, lambda b, r: (b.replace("quote them first", ""), r)),
    (11, lambda b, r: (b.replace("--preflight-only", ""), r)),
    (12, lambda b, r: (b, {**r, "Models": "claude-sonnet-5"})),
    (13, lambda b, r: (b.replace("30 %", "most"), r)),
])
def test_removing_the_evidence_for_an_item_fails_that_item(item, mutate):
    boot, rows = mutate(_FULL_BOOT, dict(_FULL_ROWS))
    found = evaluate(boot, rows)
    assert not found[item][0], f"item {item} still passes with its evidence removed"
