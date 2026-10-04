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


#: The hand-authored FILL-IN regions a WARM bundle carries (B2-W1 W1-9 item 8): the boot's Purpose
#: and the three Destination prose fields, and the residual's drift-flags (+ its two other
#: regions, so the completeness gate has nothing left to refuse).
_WARM_FILLS = {
    "HANDOFF_BOOT.md": {
        "purpose": "Warm fixture: prove the onboarding predicate on a filled bundle.",
        "dest-worktree": "none (primary tree)",
        "dest-scope": "a dry cut under the test tmp dir only",
        "dest-mode-basis": "a planning session, so architect mode (ADR-87 item 5)",
    },
    "RESIDUAL.md": {
        "driftflags": "None of the NEW organs is a decision; all are defects to dispose.",
        "shipped": "#1 fixture row, ADR-1.",
        "frontier": "Whether the warm predicate also gates the paste.",
    },
}


def _fill_regions(bundle_dir: Path) -> None:
    """Write real text into each FILL-IN region, in place (what CC and the seat do by hand)."""
    for fname, fills in _WARM_FILLS.items():
        path = bundle_dir / fname
        text = path.read_text(encoding="utf-8")

        def _repl(m: "re.Match", fills=fills) -> str:
            body = fills.get(m.group("name"))
            return m.group(0) if body is None else m.group("open") + body + m.group("close")
        path.write_text(gh.FILL_IN_RE.sub(_repl, text), encoding="utf-8", newline="\n")


def _cut_architect_bundle(tmp_path_factory, name: str, *, warm: bool):
    """ONE fresh architect dry cut of this branch (a generator: the monkeypatches live for the
    caller's whole use); yields the bundle dir. `warm=True` fills every FILL-IN region and
    re-cuts, so the splice (RF-6) carries the fills through the re-render."""
    mp = pytest.MonkeyPatch()
    tmp_path = tmp_path_factory.mktemp(name)
    today = date.today().isoformat()
    mp.setenv("CLAUDE_PROMPTS_DIR", str(_fixture_transport(tmp_path, today)))
    mp.setattr(gh, "_linked_worktrees", lambda repo_root: [])
    mp.setattr(dd, "find_powershell", lambda: "pwsh-fixture")
    mp.setattr(dd, "resolve_via_get_command",
               lambda names, **kw: [dd.Resolution(n, True, "fixture: resolved") for n in names])
    memory = tmp_path / "MEMORY.md"
    memory.write_text("# memory fixture\n", encoding="utf-8")

    def _cut():
        return gh.generate(
            gh._REPO_ROOT, mode="architect", slug="onboarding-trial", repo=".dev-knowledge",
            date=today, bundle_root=tmp_path / "dry-cut-out", assemble=True, dry_cut=True,
            memory_path=memory, sessions_root=tmp_path / "no-sessions-store")
    try:
        result = _cut()
        if warm:
            _fill_regions(result.bundle_dir)
            result = _cut()
        yield result.bundle_dir
    finally:
        mp.undo()


def _boot_and_rows(bundle_dir: Path):
    text = (bundle_dir / "HANDOFF_BOOT.md").read_text(encoding="utf-8")
    rows, _prose = vhp.parse_boot_blocks(text)
    return _BOOT.read_text(encoding="utf-8"), dict(rows or [])


@pytest.fixture(scope="module")
def cold_bundle(tmp_path_factory):
    yield from _cut_architect_bundle(tmp_path_factory, "onboarding-cold", warm=False)


@pytest.fixture(scope="module")
def warm_bundle(tmp_path_factory):
    yield from _cut_architect_bundle(tmp_path_factory, "onboarding-warm", warm=True)


@pytest.fixture(scope="module")
def trial_cut(cold_bundle):
    """ONE fresh trial cut of this branch; yields (boot text, BOOT-DATA rows dict)."""
    return _boot_and_rows(cold_bundle)


def test_a_fresh_seat_finds_all_13_onboarding_items(trial_cut):
    boot, rows = trial_cut
    found = evaluate(boot, rows)
    n = sum(1 for ok, _ in found.values() if ok)
    print("\n" + report(found))                       # shown with -s and in the failure report
    assert n == len(ITEMS), report(found)


# --- item 8: the same predicate on a WARM bundle (Purpose, Destination, drift-flags filled) ------
# RED-first: this test is new at e67f27ac, where no test cut a warm bundle at all (the one cut
# was cold, so a bundle whose fills had gone through the RF-6 splice was never judged).

def test_a_warm_bundle_is_filled_and_the_seat_still_finds_all_13_items(warm_bundle, cold_bundle):
    import validate_residual_completeness as vrc
    assert vrc.scan_bundle_dir(cold_bundle), "the cold cut must still carry unfilled regions"
    assert vrc.scan_bundle_dir(warm_bundle) == [], vrc.scan_bundle_dir(warm_bundle)
    boot_file = (warm_bundle / "HANDOFF_BOOT.md").read_text(encoding="utf-8")
    residual = (warm_bundle / "RESIDUAL.md").read_text(encoding="utf-8")
    assert _WARM_FILLS["HANDOFF_BOOT.md"]["purpose"] in boot_file          # the splice kept the fills
    assert _WARM_FILLS["RESIDUAL.md"]["driftflags"] in residual
    boot, rows = _boot_and_rows(warm_bundle)
    found = evaluate(boot, rows)
    assert all(ok for ok, _ in found.values()), report(found)
    assert {"Plan", "Rulings", "Landed"} <= set(rows)                       # the rows survive a warm cut


# --- item 6: no probe table in an architect-mode paste -----------------------------------------

def test_an_architect_paste_carries_no_probe_table_and_the_bundle_keeps_its_file(cold_bundle):
    paste = (cold_bundle / "PASTE_THIS.md").read_text(encoding="utf-8")
    assert "=== PROBES.md ===" not in paste
    assert vhp.parse_probes(paste) == [], "the paste still carries probe rows"
    # the cut's own probe gate (HANDOFF_PROCESS §5) is CC's and still reads the bundle's file
    assert vhp.parse_probes((cold_bundle / "PROBES.md").read_text(encoding="utf-8"))
    print(f"\nPASTE {len(paste.encode('utf-8'))} bytes; last line: {paste.rstrip().splitlines()[-1]}")


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


# =============================================================================================
# B2-W1 lane W1-9 (b2-handoff-hardening) -- the boot's own defects, found by the boot test. Every
# test below was written RED at e67f27ac (the base this lane merged at step 0): each failed there
# on the text/plumbing it names (no `boot_version`, a first move in three places, a hand-typed
# plan path, §5 and §6 naming different install targets, no fill-in author statement).
# =============================================================================================

import hashlib  # noqa: E402

import assemble_paste as ap  # noqa: E402

_TMPL_DIR = _REPO / "templates" / "handoff" / "v5"
_OI = _REPO / "protocols" / "OPERATOR-INTERFACE.md"
_HP = _REPO / "protocols" / "HANDOFF_PROCESS.md"


def _plain(text: str) -> str:
    """Markdown emphasis and code ticks removed, whitespace collapsed -- a phrase fence must not
    break on a `**bold**` span (the structural-fence gotcha)."""
    text = re.sub(r"(?m)^\s*>[ \t]?", "", text)                  # blockquote markers
    return re.sub(r"\s+", " ", text.replace("*", "").replace("`", "")).strip()


# --- item 3: one first move, in core item 3 -------------------------------------------------

_FIRST_MOVE = ("booted as the layer-1 browser under handoff_process",
               "the role pin is the whole onboarding check",
               "read cc's handoff and nothing else until it arrives")


def _core_item_3(boot: str) -> str:
    m = re.search(r"(?ms)^3\. \*\*First move\.\*\*.*?(?=^\d+\. \*\*|^## )", boot)
    assert m is not None, "core item 3 (First move) not found"
    return m.group(0)


def test_core_item_3_holds_the_whole_first_move_and_no_other_copy_exists():
    boot = _BOOT.read_text(encoding="utf-8")
    item3 = _core_item_3(boot)
    rest = boot.replace(item3, "")
    for phrase in _FIRST_MOVE:
        assert _plain(item3).lower().count(phrase) == 1, f"core item 3 lacks: {phrase}"
        assert _plain(rest).lower().count(phrase) == 0, f"a second copy of: {phrase}"
    for tmpl in sorted(_TMPL_DIR.glob("*.tmpl")):
        text = _plain(tmpl.read_text(encoding="utf-8")).lower()
        for phrase in _FIRST_MOVE:
            assert phrase not in text, f"{tmpl.name} carries a second copy of: {phrase}"


# --- item 2: a version that moves, and a first line that shows which boot the seat holds ------

#: version -> sha256 of the boot BODY (everything after the front matter, LF-normalised). The pair
#: lives HERE, outside the file, because a file cannot carry its own hash: bump `boot_version` in
#: the front matter AND add the new pair when the body changes. Old pairs stay (the history).
_BOOT_BODY_SHA256 = {1: "c353227c14bfcc0d3c74754a3e5c4c31e9e7ecc9e2fa269c8f771b9e1b5d68bb"}


def _split_boot(text: str) -> "tuple[str, str]":
    m = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", text, re.DOTALL)
    assert m is not None, "HANDOFF_BOOT.md has no front matter"
    return m.group(1), m.group(2)


def _boot_version_problem(text: str) -> "str | None":
    """None when the version line and the body agree; else why not. The front matter (the version
    line, `last_reviewed`, `reconciled_with`) is metadata and outside the hash, so a re-stamp is
    not a content change while any edit to the body is."""
    front, body = _split_boot(text)
    m = re.search(r"(?m)^boot_version:\s*(\d+)\s*$", front)
    if m is None:
        return "no boot_version line in the front matter"
    version = int(m.group(1))
    want = _BOOT_BODY_SHA256.get(version)
    if want is None:
        return f"boot_version {version} has no recorded body hash -- record the pair"
    got = hashlib.sha256(body.replace("\r\n", "\n").encode("utf-8")).hexdigest()
    if got != want:
        return (f"the body changed (sha256 {got[:12]}) but boot_version is still {version} "
                f"(recorded {want[:12]}) -- bump the version and record the new pair")
    return None


def test_the_boot_version_matches_its_recorded_body_hash():
    assert _boot_version_problem(_BOOT.read_text(encoding="utf-8")) is None


def test_a_content_change_with_the_version_kept_is_caught():
    text = _BOOT.read_text(encoding="utf-8")
    front, body = _split_boot(text)
    assert _boot_version_problem(f"---\n{front}\n---\n{body}\nA new rule.\n") is not None
    assert _boot_version_problem(f"---\n{front}\n---\n{body.replace('You are', 'You were', 1)}") is not None
    restamped = re.sub(r"(?m)^last_reviewed: .*$", "last_reviewed: 2099-01-01", front)
    assert _boot_version_problem(f"---\n{restamped}\n---\n{body}") is None      # a re-stamp is not content
    bumped = re.sub(r"(?m)^boot_version: \d+$", "boot_version: 99", front)
    assert "no recorded body hash" in _boot_version_problem(f"---\n{bumped}\n---\n{body}")


def test_the_on_load_line_carries_the_boot_version_and_the_pin_sha8():
    boot = _BOOT.read_text(encoding="utf-8")
    m = re.search(r"(?m)^\s*`(Booted as [^`\n]+)`\s*$", boot)
    assert m is not None, "the on-load line is not on one line of its own"
    line = m.group(1)
    assert line == ("Booted as the Layer-1 browser under HANDOFF_PROCESS v7, boot v{boot_version} "
                    "@ {sha8}. Ready for CC's handoff. ({n} sections received.)")
    # the placeholders are fed by what the paste and the file really carry
    pin = ap._role_pin(_BOOT, "7.1.0")
    sha8 = pin.splitlines()[1].split(": ", 1)[1][:8]
    assert sha8 == hashlib.sha256(_BOOT.read_bytes()).hexdigest()[:8]
    front, _body = _split_boot(boot)
    version = re.search(r"(?m)^boot_version:\s*(\d+)", front).group(1)
    shown = line.replace("{boot_version}", version).replace("{sha8}", sha8).replace("{n}", "5")
    assert f"boot v{version} @ {sha8}." in shown
    # ...and the item says where each comes from
    item3 = _plain(_core_item_3(boot))
    assert "boot_version" in item3 and "sha256: line of the paste's ROLE PIN" in item3
    assert "END OF PASTE" in item3


def test_the_boot_stays_within_its_byte_budget():
    assert len(_BOOT.read_bytes()) <= ap.HANDOFF_BOOT_BYTE_BUDGET


# --- item 1: no hand-typed plan path; the Plan row is where the boot points ------------------

def test_the_boot_types_no_plan_path_and_points_at_the_plan_row():
    boot = _BOOT.read_text(encoding="utf-8")
    assert re.findall(r"PLAN-[A-Za-z0-9._*-]+", boot) == []
    assert "to-cc/PLAN" not in boot
    assert boot.count("`Plan` row") >= 2          # the where-things-live bullet and the freeze bullet


# --- item 5: one install mode, the live Project's --------------------------------------------

def _oi_section(n: int) -> str:
    text = _OI.read_text(encoding="utf-8")
    m = re.search(rf"(?ms)^## {n}\. .*?(?=^## \d+\. |\Z)", text)
    assert m is not None, f"OPERATOR-INTERFACE section {n} not found"
    return m.group(0)


def test_operator_interface_names_one_install_mode_in_5_and_6():
    s5, s6 = _plain(_oi_section(5)).lower(), _plain(_oi_section(6)).lower()
    assert "project knowledge holds exactly one file" in s6              # the live Project (§6, LIVE)
    assert re.search(r"install protocols/handoff_boot\.md as the project's one knowledge file", s5), s5[:600]
    assert "one-line pointer in the project instructions" in s5
    assert not re.search(r"install[^.]{0,160}(as|into) the (browser )?project's own project instructions", s5)
    assert "project knowledge holds exactly one file" in s5               # §5 quotes §6, not a second mode
    assert "re-install the current protocols/handoff_boot.md as the project's knowledge file" in s5


def test_the_role_pin_refusal_and_the_boot_say_the_same_install_mode():
    refusal = ap._ROLE_REFUSAL
    assert "project knowledge" in refusal and "instructions" not in refusal
    assert _plain(refusal) in _plain(_oi_section(5))                      # §5 quotes the refusal verbatim
    assert "your project knowledge" in _plain(_core_item_3(_BOOT.read_text(encoding="utf-8")))


# --- item 7: who fills the residual's fill-ins -- derived, quoted, and honest about silence -------

_HOME_QUOTES = ("CC's handoff is only the residual", "plus CC's state read")


def test_the_boot_and_the_templates_state_who_fills_the_fill_ins_and_quote_their_home():
    hp = _plain(_HP.read_text(encoding="utf-8"))
    for quote in _HOME_QUOTES:
        assert quote in hp, f"the quoted home text is not in HANDOFF_PROCESS.md: {quote}"
    boot = _plain(_BOOT.read_text(encoding="utf-8"))
    assert "Who wrote the fill-ins. Drift-flags: CC" in boot
    assert all(q in boot for q in _HOME_QUOTES)
    # Purpose and Destination: the homes name no actor, so the boot says so and picks none
    assert "Purpose and the Destination prose: no home names the author" in boot
    assert "authored before the bundle is committed" in hp and "The three prose fields are FILL-IN regions" in hp
    for name in ("HANDOFF_BOOT.md.tmpl", "RESIDUAL.md.tmpl"):
        tmpl = _plain((_TMPL_DIR / name).read_text(encoding="utf-8"))
        assert "FILL-IN AUTHORS" in tmpl, name
        assert all(q in tmpl for q in _HOME_QUOTES), name
    assert "NO HOME NAMES THE AUTHOR" in _plain((_TMPL_DIR / "HANDOFF_BOOT.md.tmpl").read_text(encoding="utf-8"))
