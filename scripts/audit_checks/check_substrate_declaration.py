"""`check_substrate_declaration` — the `[#591]` substrate validator as a registered gate.

The thin ADAPTER half of a two-site rule; the logic lives in `scripts/validate_substrate.py`.
Same module-import + thin-adapter shape as `check_adr_status_grammar` / `check_safe_removal`.

WHAT IT GATES. The committed lane-contract corpus: every `*.md` under a
`docs/audits/<date>-technical-<batch>-launch-contracts/` directory (the in-tree home ruled
2026-08-26, ADR-101 amendment 2026-08-26 (b)) plus any `docs/audits/**/LANE-*.md`. That corpus
exists precisely so a batch's launch inputs are committed evidence — which is what makes them
gateable at all. Contracts hand-authored off-repo stay invisible to every commit-time gate, and
this check does not pretend otherwise.

THE DATE CUTOFF IS A GRANDFATHER, NOT A SKIP, and the precedent is this corpus's own. The
`lane-contract-check` pre-commit hook already grandfathers the eleven batch-1 contracts on a
ruled basis — *"retro-fitting them would falsify what was actually dispatched"* (architect,
2026-08-21). The same reasoning binds here: a contract is a RECORD of a dispatch that already
happened, so editing one to satisfy a validator written afterwards would falsify the record.
Everything dated before `ARM_DATE` is therefore reported as grandfathered debt in the evidence
line rather than silently dropped — the count is visible on every run.

MEASURED BEFORE ARMING, which is why the REFUSE legs are armed at FAIL rather than WARN. On
the live corpus at arm time the five committed batch-1 contracts produce four refusals
(one `codespaces` near-miss for the ruled `codespace`, three declaring no substrate at all) and
ALL FOUR are pre-`ARM_DATE`. The post-cutoff corpus measures **0**, so arming cannot RED a
clean tree — the same evidence bar `check_adr_status_grammar` used to arm its `enum` and
`single-field` legs. Leg 4 (`substrate-second-local-writer`) is a WARN by the row's own words.

FAIL-CLOSED ON ITS OWN INPUTS, deliberately. An unreadable substrate registry, an undecodable
contract or an undatable one are reported as `fail`/`warn`, never as `pass` and never as
`unavailable`: a validator that cannot compute its ground truth and reports a status the
caller renders green is the exact class `[#583]`/`[#596]` sweep for, and `_STATUS_LABEL`
renders `unavailable` as "N/A".

HONEST LIMITS, the module's own and its logic module's:
  * It gates the COMMITTED corpus. A contract dispatched from the prompts dir and never copied
    in-tree is not checked by anything, here or elsewhere.
  * An undatable contract cannot be placed relative to the cutoff. It is WARNed by name rather
    than assumed old — assuming old is how a cutoff becomes an escape hatch.
  * Everything `validate_substrate`'s own docstring records: leg 2 is token-based, leg 3 matches
    path shapes, leg 4 sees only the contracts in one directory, and none of them says a
    contract asks for the RIGHT work.

Child-repo-safe: a repo with no `docs/audits/` yields `n/a` (subject-absent), not a FAIL.
Read-only (Layer 2): no git, no writes.
"""

from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

from ._common import Finding, _na, _NA_SUBJECT_ABSENT

try:
    from scripts import validate_substrate as _vsub
except ImportError:
    import validate_substrate as _vsub

CHECK_NAME = "substrate_declaration"
AUDITS_RELPATH = "docs/audits"

#: Contracts landed on or after this date are gated; earlier ones are grandfathered records
#: of an already-executed dispatch. The date this check armed.
ARM_DATE = _dt.date(2026, 8, 27)

#: PER-LEG arm dates, for legs added AFTER this check armed. A leg written today cannot
#: honestly gate a contract dispatched last week: the contract is a RECORD, and editing it to
#: satisfy a validator written afterwards falsifies what was dispatched — the same ruled basis
#: as `lane-contract-check`'s batch-1 grandfather (architect, 2026-08-21).
#:
#: Legs 5 and 6 arrived at batch E's freeze (prerequisite 0a and CUT-6) and arm on 2026-09-01,
#: the day AFTER they were written, so that every contract already in the tree — including
#: batch E's own tier-(A) contracts, dispatched hours before the legs existed — is grandfathered
#: debt that is COUNTED IN THE EVIDENCE LINE rather than silently dropped.
#:
#: This grandfather scopes the COMMIT-TIME sweep only. At FREEZE the legs are fully armed:
#: `validate_substrate.validate_batch` is called directly on the batch being frozen, which is
#: the moment CUT-6 puts them at. Same logic module, two scopes — continuous conformance over
#: the committed corpus, and a gate over the batch about to dispatch.
#: Leg 8 (`substrate-heartbeat-dead`, [#554]/[#746]) declares its date in the LOGIC MODULE and
#: this map READS it rather than restating it. A second literal would be a second answer to a
#: settled question, and the lane that added the leg measured exactly what one costs: the date
#: lived only in `validate_substrate.LEG_ARM_DATES`, this adapter never consulted it, and the
#: commit gate RED'd with 20 refusals against committed contracts back to 2026-08-29 — every
#: one of them a record of a dispatch that had already happened, and undischargeable without
#: editing it. The grandfather existed and was not reachable from the place that grandfathers.
LEG_ARM_DATES: dict[str, _dt.date] = {
    _vsub.RULE_TEARDOWN_ENUM: _dt.date(2026, 9, 1),
    _vsub.RULE_WRITE_SCOPE_DISJOINT: _dt.date(2026, 9, 1),
    _vsub.RULE_HEARTBEAT_DEAD: _vsub.LEG_ARM_DATES[_vsub.RULE_HEARTBEAT_DEAD],
}

#: [#926] PRE-LAUNCH SCOPE for leg 8, TEMPORARY BY CONSTRUCTION (operator order 2026-09-19).
#: Leg 8 asks whether the substrate a contract names is live NOW -- a dispatch-time question.
#: Refusing it before a launch prevents an outcome; refusing it on a contract whose batch has
#: CLOSED (its `closed_by:` packet is committed) cannot change any outcome, and the contract is
#: an immutable record, so the refusal could only be discharged by falsifying it. Until this
#: date such a refusal is reported as scoped-out debt in the pass line; after it the scope
#: switches itself off, the refusal FAILs again and names [#926] for re-ruling. BUILD MODE's own
#: expiry (protocols/BUILD-MODE.md), the mode the narrowing was ruled under. Only leg 8 is
#: scoped; the in-contract `**Substrate deviation:**` escape is deliberately NOT used.
POST_LAUNCH_NARROWING_EXPIRES = _dt.date(2026, 11, 18)
_POST_LAUNCH_SCOPED_RULES = frozenset({_vsub.RULE_HEARTBEAT_DEAD})


def _today() -> _dt.date:
    """The date the time-boxed narrowing is read against -- one seam, so tests can move it."""
    return _dt.date.today()


def _batch_key(date_part: str, token: str) -> str:
    """Only the ONE sanctioned spelling variation is folded: the optional dash directly after
    `batch` (`batchac` == `batch-ac`). Every other dash is identity -- stripping them all made
    `batch-x3` and `batch-x-3` one key (Codex terra HIGH 2026-09-19); case is not folded either
    (pass 3)."""
    tok = token.removeprefix("batch")   # case is identity
    return f"{date_part}:{tok.removeprefix('-')}"


_LAUNCH_KEY_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-technical-(?P<tok>batch.*)-launch-contracts$")
_MANIFEST_KEY_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-technical-(?P<tok>batch-.+)-manifest\.md$")


def _batch_key_of_launch_dir(name: str) -> str | None:
    """`2026-09-17-technical-batchac-launch-contracts` -> `2026-09-17:ac`. The dash after
    `batch` is dropped on BOTH sides because the two homes spell the batch differently (the live
    witness: `batchac` beside `batch-ac-manifest.md`); no other dash is."""
    m = _LAUNCH_KEY_RE.match(name)
    return _batch_key(m.group("date"), m.group("tok")) if m else None


def _batch_key_of_manifest(rel: str) -> str | None:
    m = _MANIFEST_KEY_RE.match(Path(rel).name)
    return _batch_key(m.group("date"), m.group("tok")) if m else None


def _closed_batch_keys(repo_path: Path) -> set[str]:
    """Batch keys whose `closed_by:` packet is COMMITTED -- the batch is over, every contract
    in it is post-launch. Reuses `batch_manifest`'s committed-tree reading, so an uncommitted
    packet closes nothing. Fails toward NO scope-out: unreadable git => empty set => leg 8
    keeps refusing."""
    try:
        from scripts import batch_manifest as _bm
    except ImportError:            # pragma: no cover - the alternate launch path
        import batch_manifest as _bm
    audits = _bm._committed_audits(Path(repo_path))
    if audits is None:
        return set()
    manifests = _bm._manifests_in(audits)
    texts = _bm._committed_texts(Path(repo_path), manifests)
    keys = [_batch_key_of_manifest(rel) for rel in manifests]
    ambiguous = {k for k in keys if k is not None and keys.count(k) > 1}
    out: set[str] = set()
    for rel in manifests:
        text = texts.get(rel)
        if text is None:
            continue
        closed_by = _bm._frontmatter(text).get("closed_by", "")
        key = _batch_key_of_manifest(rel)
        # A key two manifests share names no single batch: it closes nothing (refusing side).
        if key and key not in ambiguous and _bm._valid_closer(closed_by) and closed_by in audits:
            out.add(key)
    return out


def _is_post_launch(rel: str, closed: set[str]) -> bool:
    """A contract is post-launch iff it sits in a launch-contracts dir whose batch is closed.
    No matching manifest => pre-launch (the refusing side). The NEAREST launch-contracts dir
    owns the contract, so a dir nested inside a closed batch's dir is judged by its own batch."""
    for part in reversed(Path(rel).parts[:-1]):
        key = _batch_key_of_launch_dir(part)
        if key is not None:
            return key in closed
    return False


#: The in-tree launch-contract home's directory-name shape (PLAYBOOK Ch8, "Where the contract
#: file lives"). The leading date is the contract's landing date.
_LAUNCH_DIR_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-.*-launch-contracts$")
#: A dated artifact filename, for a contract sitting directly under `docs/audits/`.
_DATED_NAME_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-")


def _contract_date(path: Path, audits_dir: Path) -> _dt.date | None:
    """The landing date of one contract, or None when nothing on the path carries one.

    Read from the launch-contracts directory name first (the ruled home names the batch's
    date), then from the file's own leading date. None is returned rather than a guess: the
    caller WARNs by name instead of silently placing the file on the safe side of the cutoff.
    """
    for parent in path.parents:
        if parent == audits_dir.parent:
            break
        match = _LAUNCH_DIR_RE.match(parent.name)
        if match:
            try:
                return _dt.date.fromisoformat(match.group("date"))
            except ValueError:
                return None
    match = _DATED_NAME_RE.match(path.name)
    if match:
        try:
            return _dt.date.fromisoformat(match.group("date"))
        except ValueError:
            return None
    return None


def _corpus(audits_dir: Path) -> list[Path]:
    """Every committed lane CONTRACT, deduplicated and ordered.

    NARROWED 2026-08-31 (batch E) from `*.md` to `LANE-*.md`, and the reason is a measured
    false positive rather than a preference. A launch-contracts directory holds more than
    contracts: batch E landed a `PLAN.md` (the derivation) and a `CUT.md` (the ruling) beside
    its seven contracts, and the old glob read both as contracts. `CUT.md` was REFUSED for
    "declares no substrate" — a true statement about a file that should never have been asked,
    because a ruling is not a lane. Worse, `PLAN.md` PASSED for the wrong reason: its lane list
    quotes `substrate: LOCAL` inside a fenced block, which the prose fallback parsed as a real
    declaration. A gate that refuses one non-contract and green-lights another on a quoted
    string is measuring the wrong corpus in both directions.

    `LANE-*.md` is the name shape `gen_lane_contract` emits, and it is the SAME shape the
    sibling `lane-contract-check` pre-commit hook globs on. Two gates over one corpus now agree
    on what that corpus is.

    HONEST LIMIT: a contract that is not named `LANE-*.md` is invisible here. That is the trade
    — the batch-1 contracts (`*-lane-contract.md`, directly under `docs/audits/`) were already
    outside both globs and are grandfathered by ruling anyway.
    """
    return sorted(p for p in audits_dir.rglob("LANE-*.md") if p.is_file())


def check_substrate_declaration(repo_path: Path) -> list[Finding]:
    """`[#591]` layer 2: a committed lane contract whose substrate contradicts its content.

    One Finding PER refusal, never a bundle. The `#147` disposition register suppresses an
    ENTIRE Finding on a substring match, so a bundled Finding would let one dispositioned
    contract wave through every other refusal beside it — the reason `git_backlog_drift` emits
    one per drifted id and `funnel_coverage` one per artifact.
    """
    audits_dir = Path(repo_path) / AUDITS_RELPATH
    if not audits_dir.is_dir():
        return [_na(CHECK_NAME, _NA_SUBJECT_ABSENT,
                    f"no {AUDITS_RELPATH}/ — this repo carries no committed lane contracts")]

    try:
        registry = _vsub.load_registry(Path(repo_path))
    except _vsub.SubstrateRegistryError as exc:
        # FAIL, not "unavailable": the ship-gate blocks only on `fail` plus undispositioned
        # `warn`, so an "unavailable" verdict here would ship a validator that measured
        # nothing (`check_silent_rule_ratchet`'s 2026-07-27 terra call, swept 2026-08-25).
        return [Finding(CHECK_NAME, "fail",
                        f"substrate registry unreadable, so no contract was validated: "
                        f"{exc}".replace("|", "/"))]

    try:
        paths = _corpus(audits_dir)
    except OSError as exc:
        return [Finding(CHECK_NAME, "fail",
                        f"could not enumerate {AUDITS_RELPATH}: {exc!r}".replace("|", "/"))]

    out: list[Finding] = []
    gated: dict[str, str] = {}
    landed_at: dict[str, _dt.date] = {}
    grandfathered = 0
    for path in paths:
        rel = path.relative_to(repo_path).as_posix()
        landed = _contract_date(path, audits_dir)
        if landed is None:
            out.append(Finding(CHECK_NAME, "warn",
                               f"{rel} carries no resolvable landing date, so it cannot be "
                               f"placed against the {ARM_DATE.isoformat()} cutoff — it is "
                               f"reported rather than assumed grandfathered"))
            continue
        if landed < ARM_DATE:
            grandfathered += 1
            continue
        landed_at[rel] = landed
        try:
            gated[rel] = path.read_text(encoding="utf-8")
        except OSError as exc:
            out.append(Finding(CHECK_NAME, "fail",
                               f"could not read {rel}: {exc!r}".replace("|", "/")))
        except UnicodeDecodeError as exc:
            out.append(Finding(CHECK_NAME, "fail",
                               f"{rel} is not valid UTF-8 ({exc}), so it was not "
                               f"validated".replace("|", "/")))

    leg_grandfathered = 0
    post_launch: list[str] = []
    closed = None
    expired = _today() > POST_LAUNCH_NARROWING_EXPIRES
    for refusal in _vsub.validate_batch(gated, registry=registry):
        leg_arm = LEG_ARM_DATES.get(refusal.rule)
        if leg_arm is not None:
            # A multi-source refusal (leg 6 names a PAIR) is grandfathered when EITHER side
            # predates the leg: the pair contains a record that cannot be edited, so the
            # finding is undischargeable by any act this repo permits.
            sources = [s.strip() for s in refusal.source.split(",")]
            if any(landed_at.get(s, _dt.date.min) < leg_arm for s in sources):
                leg_grandfathered += 1
                continue
        detail = refusal.render()
        if refusal.rule in _POST_LAUNCH_SCOPED_RULES:
            if closed is None:
                closed = _closed_batch_keys(Path(repo_path))
            if _is_post_launch(refusal.source, closed):
                if not expired:
                    post_launch.append(refusal.source)
                    continue
                detail += (f" -- the [#926] pre-launch scope for this leg expired on "
                           f"{POST_LAUNCH_NARROWING_EXPIRES.isoformat()}, so this post-launch "
                           f"contract counts again; re-rule [#926]")
        status = "fail" if refusal.severity == _vsub.SEVERITY_REFUSE else "warn"
        out.append(Finding(CHECK_NAME, status, detail.replace("|", "/")))

    if not out:
        legs = ", ".join(sorted(LEG_ARM_DATES))
        out.append(Finding(CHECK_NAME, "pass",
                           f"{len(gated)} lane contract(s) landed on/after "
                           f"{ARM_DATE.isoformat()} agree with their declared substrate "
                           f"({grandfathered} earlier contract(s) grandfathered as records "
                           f"of an already-executed dispatch; {leg_grandfathered} finding(s) "
                           f"from later-armed legs [{legs}] grandfathered as debt — those "
                           f"legs are fully armed at FREEZE)"))
    if post_launch:
        # Its OWN line, emitted whatever else the run found: a narrowing that disappears
        # whenever an unrelated WARN is present is not visible debt, it is a hidden one.
        out.append(Finding(CHECK_NAME, "pass",
                           f"{len(post_launch)} leg-8 refusal(s) on post-launch contracts "
                           f"(batch closed) scoped out under [#926] until "
                           f"{POST_LAUNCH_NARROWING_EXPIRES.isoformat()}: "
                           f"{', '.join(post_launch)}"))
    return out
