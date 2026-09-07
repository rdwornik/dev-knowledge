"""deploy/floor_mechanisms.py — floor v1.5.0's MECHANISMS as manifest components
with a declared version and a drift check on BOTH sides (024 packaging rule,
DECLARE-F F-1 split).

WHY THIS MODULE EXISTS. Inbox 024's packaging rule is one sentence: *"Every element
above is a COMPONENT with a version in the deploy manifest, shipped by the carrier,
with a drift check on both sides and a per-consumer waiver."* Before this module the
manifest carried 21 components and **zero** of them declared a version or a two-sided
drift check (measured 2026-09-07 against `deploy/manifest-v1.5.0.yaml`). Component
identity was therefore a claim: the manifest asserted a carrier shipped a thing, and
nothing measured whether the hub still HELD that thing or whether a consumer had it.

THE TWO SIDES, AND WHY BOTH. `verify:`/`engages:` already answer "is it present and
does it fire **at the consumer**". Neither asks the other question — *does the HUB
still hold the payload it declares?* That gap is not hypothetical: three of floor
v1.5.0's five ruled mechanisms have **no hub payload at all** (see
`floor_mechanisms_pending:` in the manifest), and until a hub-side leg existed a
manifest could declare them and lint green. The manifest's own header names this
failure mode — *"declaring a component against a payload that does not exist lints
green but is undeployable"* — and handles it in PROSE, per release, by hand. This
module makes that prose measurable:

- **hub leg** — does the payload this component declares exist in the hub tree, and
  does it still carry the token that makes it the thing declared? A RED hub leg means
  the manifest is describing something the hub cannot ship.
- **consumer leg** — is this component WAIVED here; if not, does the consumer carry the
  artifact, AND does its recorded `deployed_methodology_version`
  (`ecosystem/deployed-versions.yaml`, the ADR-91 durable record) reach the version this
  mechanism declares? A consumer can hold the file and still be behind the declared
  version; one leg alone cannot see that.

THE THIRD LEG IS THE WAIVER. 024's rule ends *"and a per-consumer waiver"*, so an
honored waiver is a first-class verdict here (`WAIVED`), not drift: a divergence the
consumer already sanctioned in its own `.methodology.yaml` must not be planned over,
which is the [#276] add-leg re-break in a new costume. The verdict is routed through
the Informant's `validate_allowlist_entry` — the same engine both deploy legs use — so
this module honors exactly the waivers they honor, and fails CLOSED on a waiver with no
reason, no time-box, or an expired one. A waiver against a `split: pull` mechanism is
REPORTED rather than obeyed: fleet-uniform-by-construction and per-consumer-waivable
are contradictory claims, and the contradiction is a finding.

THE F-1 SPLIT IS A FIELD, NOT A FOLDER. `DECLARE-F-2026-09-06` accepted §0.3: PUSH for
any component a consumer may pin or waive, PULL for anything fleet-uniform by
construction, **both legs remaining manifest components with a declared version and a
drift check on both sides**. The discriminator is a question asked per component —
*does this component have a legitimate per-consumer divergence?* — so each mechanism
records its `split:` **and** the `divergence:` answer that produced it. A component
whose divergence answer is blank is a finding, not a default: `validate_mechanism`
refuses it.

WHAT THIS MODULE DOES NOT DO. **It does not deploy.** ADR-92 Decision 3 is write-yes /
commit-no / autonomy-no, and NIGHT-2 §0 makes every consumer repo read-only: `plan()`
opens the consumer tree for reading only and returns text. There is no apply leg here
and adding one is a separate, operator-sequenced act. It is also NOT a second
`Carrier` — carriers reconcile a consumer toward a target (`deploy/contract.py`);
this reports whether a *declaration* is true on both sides, which is a different
question and deliberately not routed through `detect()`/`verify()`.

LIBRARY-FIRST (C-11). Checked before building: stdlib `pathlib` + substring for the
probes, `yaml.safe_load` for the manifest — the same reader every other `deploy/`
module uses; no second YAML parser, no expression evaluator, no new dependency. A
declarative `{path, contains}` probe was chosen over an importable callable
specifically so a manifest edit can never become code execution. No MEASURED
divergence from an established library was found, so nothing here is hand-rolled
against one.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import yaml

HUB_ROOT = Path(__file__).resolve().parent.parent

# Reuse the hub Informant's allowlist reader rather than hand-rolling a second
# waiver reader — the same reuse `deploy/carrier_precommit.py` already makes, and
# for the same reason: `validate_allowlist_entry` is the ONE engine that decides
# whether a declared divergence is honored (shape + ISO-8601 time-box), so a
# waiver this module honors is exactly a waiver the deploy legs honor.
_SCRIPTS = HUB_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from enforcement_coverage import AL_VALID, read_allowlist, validate_allowlist_entry  # noqa: E402

#: The F-1 discriminator's two legs. PUSH = a consumer may legitimately pin or waive
#: it; PULL = fleet-uniform by construction. Both remain manifest components.
SPLITS = ("push", "pull")

#: A mechanism's hub payload either exists today or is measured absent. `pending` is
#: not a lifecycle status (the manifest's `status:` stays the 2-state active/removed
#: of D3) — it records that the HUB cannot ship this yet, with its blocker.
PAYLOAD_STATES = ("present", "pending")

#: Where the ADR-91 durable per-consumer version record lives, hub-side.
DEPLOYED_VERSIONS = "ecosystem/deployed-versions.yaml"

#: Manifest blocks this module reads. `components:` entries are shippable today;
#: `floor_mechanisms_pending:` entries are declared with the identical mechanism
#: shape but have a measured hub-side blocker, so they are deliberately NOT active
#: components (a `status: active` entry with no payload is the failure this whole
#: module exists to surface).
COMPONENTS_BLOCK = "components"
PENDING_BLOCK = "floor_mechanisms_pending"

OK = "OK"
DRIFT = "DRIFT"
ABSENT = "ABSENT"
BEHIND = "BEHIND"
UNKNOWN = "UNKNOWN"
#: The consumer sanctioned this component's divergence in its own `.methodology.yaml`
#: and the entry is valid today. 024's rule is "a drift check on both sides AND a
#: per-consumer waiver" — an honored waiver is a legitimate end state, not drift.
WAIVED = "WAIVED"


@dataclass(frozen=True)
class DriftResult:
    """One side's verdict for one mechanism.

    ``state`` is one of the module verdicts above; ``detail`` always names the
    evidence (the path probed, the token missing, the versions compared) so a plan
    line can be acted on without re-deriving what was measured.
    """

    side: str
    state: str
    detail: str

    @property
    def clean(self) -> bool:
        return self.state == OK


@dataclass(frozen=True)
class Mechanism:
    """A floor mechanism as declared in the manifest, with its two-sided drift spec."""

    id: str
    version: str
    split: str
    divergence: str
    waivable: bool
    payload_state: str
    payload_blocker: str
    payload_source: str
    hub_probe: dict[str, Any]
    consumer_probe: dict[str, Any]
    declared_in: str

    @property
    def shippable(self) -> bool:
        """True when the hub holds a payload to ship (a `components:` entry)."""
        return self.payload_state == "present"


# ---------------------------------------------------------------------------
# Load + shape validation
# ---------------------------------------------------------------------------


def load_manifest(path: Path) -> dict[str, Any]:
    """Read a manifest with the same reader every other deploy module uses."""
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _mechanism_from_entry(entry: dict[str, Any], declared_in: str) -> Mechanism | None:
    """Build a Mechanism from a manifest entry, or None when it declares no `mechanism:`.

    Returning None (rather than raising) is what lets the 21 pre-existing components
    stay exactly as they are: a component with no `mechanism:` block is simply not a
    floor mechanism, and this module says nothing about it.
    """
    spec = entry.get("mechanism")
    if not isinstance(spec, dict):
        return None
    drift = spec.get("drift") if isinstance(spec.get("drift"), dict) else {}
    payload = spec.get("payload") if isinstance(spec.get("payload"), dict) else {}
    return Mechanism(
        id=str(entry.get("id", "")).strip(),
        version=str(spec.get("version", "")).strip(),
        split=str(spec.get("split", "")).strip(),
        divergence=str(spec.get("divergence", "")).strip(),
        waivable=bool(entry.get("waivable")),
        payload_state=str(payload.get("state", "")).strip(),
        payload_blocker=str(payload.get("blocker", "")).strip(),
        payload_source=str(payload.get("source", "")).strip(),
        hub_probe=drift.get("hub") if isinstance(drift.get("hub"), dict) else {},
        consumer_probe=drift.get("consumer") if isinstance(drift.get("consumer"), dict) else {},
        declared_in=declared_in,
    )


def load_mechanisms(spec: dict[str, Any]) -> list[Mechanism]:
    """Every floor mechanism the manifest declares, from BOTH blocks, in file order."""
    found: list[Mechanism] = []
    for block in (COMPONENTS_BLOCK, PENDING_BLOCK):
        for entry in spec.get(block) or []:
            if not isinstance(entry, dict):
                continue
            mech = _mechanism_from_entry(entry, block)
            if mech is not None:
                found.append(mech)
    return found


def validate_mechanism(mech: Mechanism) -> list[str]:
    """Shape problems with one mechanism's declaration; empty list == well-formed.

    This is the clause that keeps 024's packaging rule from decaying into a comment:
    a mechanism with no version, no split, no divergence answer, or only ONE drift
    leg is refused here rather than silently half-checked. A one-sided drift check is
    the specific defect the rule names, so it is an error, not a warning.
    """
    problems: list[str] = []
    if not mech.id:
        problems.append("mechanism with no component id")
    if not mech.version:
        problems.append(f"{mech.id}: mechanism.version is required (024 packaging rule)")
    if mech.split not in SPLITS:
        problems.append(
            f"{mech.id}: mechanism.split {mech.split!r} not in {list(SPLITS)} (F-1 split)"
        )
    if not mech.divergence:
        problems.append(
            f"{mech.id}: mechanism.divergence must answer F-1's question "
            "('does this component have a legitimate per-consumer divergence?') — "
            "a component you cannot classify is a finding, not a coin flip"
        )
    if mech.payload_state not in PAYLOAD_STATES:
        problems.append(
            f"{mech.id}: mechanism.payload.state {mech.payload_state!r} not in {list(PAYLOAD_STATES)}"
        )
    if mech.payload_state == "pending" and not mech.payload_blocker:
        problems.append(f"{mech.id}: payload.state pending requires a measured blocker")
    if mech.payload_state == "present" and not mech.payload_source:
        problems.append(
            f"{mech.id}: payload.state present requires payload.source — the hub file the "
            "carrier would actually ship. Without it 'the hub holds a payload' is a claim, "
            "which is the exact thing this module exists to stop being one"
        )
    for side, probe in (("hub", mech.hub_probe), ("consumer", mech.consumer_probe)):
        if not probe.get("path"):
            problems.append(
                f"{mech.id}: drift.{side}.path is required — 024 requires a drift check "
                "on BOTH sides, and one leg is not two"
            )
    # A PULL component is fleet-uniform BY CONSTRUCTION, so sanctioning a per-consumer
    # divergence in it contradicts the classification that put it on the pull leg.
    # PUSH is the leg that exists precisely to be pinned or waived.
    if mech.split == "pull" and mech.waivable:
        problems.append(
            f"{mech.id}: split:pull is fleet-uniform by construction, so waivable:true "
            "contradicts it (F-1: waivable belongs to the push leg)"
        )
    return problems


# ---------------------------------------------------------------------------
# The two drift legs
# ---------------------------------------------------------------------------


def _probe(root: Path, probe: dict[str, Any], side: str) -> DriftResult:
    """Resolve one declarative `{path, contains}` probe against a tree. Read-only.

    Absent path -> ABSENT; present but missing the declared token -> DRIFT (the file
    is there but is no longer the thing declared); otherwise OK. The token is what
    separates "a file with this name exists" from "the payload is still here", which
    is the whole difference between presence and identity.
    """
    rel = str(probe.get("path", ""))
    target = root / rel
    if not target.exists():
        return DriftResult(side, ABSENT, f"{rel} absent under {root}")
    token = probe.get("contains")
    if token:
        try:
            body = target.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:  # unreadable is not the same as missing
            return DriftResult(side, UNKNOWN, f"{rel} unreadable: {exc}")
        if str(token) not in body:
            return DriftResult(side, DRIFT, f"{rel} present but missing token {token!r}")
    return DriftResult(side, OK, f"{rel} present{' with token' if token else ''}")


def hub_drift(mech: Mechanism, hub_root: Path = HUB_ROOT) -> DriftResult:
    """Side 1 — does the HUB still hold the payload this mechanism declares?

    The leg that did not exist before this module. A RED here means the manifest is
    describing something the hub cannot ship, which no consumer-side check can see.

    TWO questions, because the declared `payload.source` and the declared drift probe
    can name different files and a mechanism is only shippable when BOTH resolve. The
    SOURCE is what the carrier would copy; the PROBE is what proves the mechanism is
    still the thing declared (for `floor-waiver-register` the source is the
    `.methodology.yaml` register and the probe is its reader, and losing either one
    breaks the mechanism in a different way). Source first — a missing payload makes
    the identity probe moot.
    """
    if mech.payload_source:
        source = _probe(hub_root, {"path": mech.payload_source}, "hub")
        if not source.clean:
            return DriftResult("hub", source.state, f"payload.source {source.detail}")
    return _probe(hub_root, mech.hub_probe, "hub")


def read_deployed_version(hub_root: Path, consumer: str) -> str | None:
    """The consumer's recorded corpus version from the ADR-91 durable record.

    Read from the HUB — `ecosystem/deployed-versions.yaml` is the hub-side register of
    per-consumer deployed versions, not a file in the consumer tree. Returns None when
    the repo is unknown or the value is null (pre-deploy), which the caller reports as
    UNKNOWN rather than treating as zero.
    """
    path = hub_root / DEPLOYED_VERSIONS
    if not path.exists():
        return None
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        # An unreadable or malformed register is NOT "no version recorded" — the
        # caller reports UNKNOWN either way, and inventing a value here would turn a
        # broken register into a confident verdict.
        return None
    if not isinstance(data, dict):
        return None
    entry = (data.get("repos") or {}).get(consumer) or {}
    value = entry.get("deployed_methodology_version") if isinstance(entry, dict) else None
    return str(value) if value else None


def _version_tuple(value: str) -> tuple[int, ...] | None:
    """Strictly parse a MAJOR.MINOR.PATCH corpus version, or None if it is not one.

    STRICT on purpose. An earlier draft coerced each dotted chunk by keeping its
    digits, which silently ordered `1.5.0rc1` ABOVE `1.5.0` and reported a
    pre-release consumer as at-target — a false-clean verdict, the worst failure
    this module can produce. The ADR-91 tag grammar is vMAJOR.MINOR.PATCH, so
    anything else is unrecognised, and unrecognised is reported as UNKNOWN rather
    than guessed. (`packaging.version` would order pre-releases correctly, but it is
    not a declared dependency of this project and adding one is its own gated
    change; strict-or-UNKNOWN needs no dependency and never lies.)
    """
    chunks = value.strip().lstrip("v").split(".")
    if not all(c.isdigit() for c in chunks) or not chunks:
        return None
    return tuple(int(c) for c in chunks)


def waived_components(consumer_root: Path, *, today: date | None = None) -> frozenset[str]:
    """Component ids the consumer's own `.methodology.yaml` sanctions, valid TODAY.

    024's rule has three legs — version, two-sided drift, **and a per-consumer
    waiver** — and this is the third. Routed through the Informant's
    ``validate_allowlist_entry`` (the same engine ``carrier_precommit`` uses), so an
    entry with no reason, no time-box, an unparseable date or an expired one is NOT
    honored here either: the waiver fails CLOSED and the component is reported as
    drifted exactly as if nothing had been declared. Fail-soft on an absent or
    malformed file, like every other reader of consumer-owned config.
    """
    run_date = today or date.today()
    return frozenset(
        e.component
        for e in read_allowlist(consumer_root)
        if e.component
        and validate_allowlist_entry(e, run_date=run_date, waivable_policy={})[0] == AL_VALID
    )


def consumer_drift(
    mech: Mechanism,
    consumer_root: Path,
    *,
    hub_root: Path = HUB_ROOT,
    consumer_name: str | None = None,
    waived: frozenset[str] | None = None,
) -> DriftResult:
    """Side 2 — does the CONSUMER carry the artifact AND reach the declared version?

    Three questions in order, because each earlier one makes the later ones moot.

    1. **Is this component WAIVED here?** A divergence the consumer has already
       sanctioned in its own `.methodology.yaml` is a legitimate end state, not
       drift — reporting it as drift and planning a deploy over it is precisely the
       [#276] failure the waiver register exists to stop, and it would re-break a
       consumer on the add leg. A waiver is honored ONLY on the PUSH leg: a
       `split: pull` mechanism is fleet-uniform by construction, so a waiver against
       it contradicts its own classification and is reported rather than obeyed.
    2. **Is the artifact there, and still itself?** (ABSENT / DRIFT.)
    3. **Does the recorded version reach the declared one?** (BEHIND.) A consumer can
       hold the file and be behind the version; one question alone cannot see that.
    """
    name = consumer_name or consumer_root.name
    sanctioned = waived if waived is not None else waived_components(consumer_root)
    if mech.id in sanctioned:
        if mech.split == "pull":
            return DriftResult(
                "consumer",
                DRIFT,
                f"{name} declares a waiver for {mech.id}, but it is a split:pull "
                "(fleet-uniform) mechanism — the waiver contradicts its classification "
                "and is NOT honored; report it, do not deploy over it",
            )
        return DriftResult(
            "consumer",
            WAIVED,
            f"{name} sanctions this divergence in its own .methodology.yaml (valid entry)",
        )

    artifact = _probe(consumer_root, mech.consumer_probe, "consumer")
    if not artifact.clean:
        return artifact
    recorded = read_deployed_version(hub_root, name)
    if recorded is None:
        return DriftResult(
            "consumer",
            UNKNOWN,
            f"{artifact.detail}; no deployed_methodology_version recorded for {name!r} (pre-deploy)",
        )
    have, want = _version_tuple(recorded), _version_tuple(mech.version)
    if have is None or want is None:
        unparseable = recorded if have is None else mech.version
        return DriftResult(
            "consumer",
            UNKNOWN,
            f"{artifact.detail}; version {unparseable!r} is not MAJOR.MINOR.PATCH — "
            "not comparable, so no verdict is claimed",
        )
    if have < want:
        return DriftResult(
            "consumer",
            BEHIND,
            f"{artifact.detail}; {name} records {recorded}, mechanism declares {mech.version}",
        )
    return DriftResult("consumer", OK, f"{artifact.detail}; {name} records {recorded}")


# ---------------------------------------------------------------------------
# The dry-run plan
# ---------------------------------------------------------------------------


def plan(
    consumer_root: Path,
    *,
    hub_root: Path = HUB_ROOT,
    manifest: Path | None = None,
    consumer_name: str | None = None,
) -> str:
    """Render the DRY-RUN plan for one consumer. Reads only; writes nothing, anywhere.

    The plan is the operator's surface: per mechanism, its F-1 leg, its declared
    version, both drift verdicts, and the ACT the deploy WOULD take. Deploying is his
    act (ADR-92 Decision 3), so this prints a plan and stops — a dry run that wrote
    into a consumer would be a contract breach, not an over-delivery.
    """
    manifest = manifest or (hub_root / "deploy" / "manifest-v1.5.0.yaml")
    spec = load_manifest(manifest)
    mechanisms = load_mechanisms(spec)
    name = consumer_name or consumer_root.name

    lines: list[str] = []
    lines.append(f"DRY RUN — floor mechanisms, manifest {manifest.name}")
    lines.append(f"  hub      : {hub_root}")
    lines.append(f"  consumer : {consumer_root}  (repo id {name!r}, READ-ONLY)")
    lines.append(f"  declared : {len(mechanisms)} floor mechanisms "
                 f"({sum(1 for m in mechanisms if m.shippable)} shippable, "
                 f"{sum(1 for m in mechanisms if not m.shippable)} payload-pending)")
    lines.append("")

    shape_problems: list[str] = []
    sanctioned = waived_components(consumer_root)
    for mech in mechanisms:
        mine = validate_mechanism(mech)
        shape_problems.extend(mine)
        hub = hub_drift(mech, hub_root)
        con = consumer_drift(
            mech, consumer_root, hub_root=hub_root, consumer_name=name, waived=sanctioned
        )
        # A malformed declaration is refused BEFORE anything else is weighed. Planning a
        # deploy off a declaration that failed its own shape check would make the shape
        # rule advisory, and 024's packaging rule is not advisory.
        if mine:
            act = f"REFUSE — malformed declaration ({len(mine)} problem(s), listed below)"
        elif not mech.shippable:
            act = "NO-OP — hub holds no payload; nothing to deploy"
        elif hub.state != OK:
            act = "REFUSE — hub-side drift; fix the hub before deploying"
        elif con.state in (OK, WAIVED):
            act = ("NO-OP — consumer at declared version" if con.state == OK
                   else "NO-OP — divergence sanctioned by the consumer's own waiver")
        else:
            act = f"WOULD DEPLOY — {mech.split} leg, to version {mech.version}"
        lines.append(f"[{mech.id}]  split={mech.split}  version={mech.version}  "
                     f"waivable={str(mech.waivable).lower()}  payload={mech.payload_state}")
        lines.append(f"    drift.hub      {hub.state:<8} {hub.detail}")
        lines.append(f"    drift.consumer {con.state:<8} {con.detail}")
        if mech.payload_blocker:
            lines.append(f"    blocker        {mech.payload_blocker}")
        lines.append(f"    act            {act}")
        lines.append("")

    if shape_problems:
        lines.append("DECLARATION PROBLEMS (024 packaging rule):")
        lines.extend(f"  - {p}" for p in shape_problems)
    else:
        lines.append("DECLARATION: every mechanism carries version + split + divergence "
                     "+ a drift check on BOTH sides.")
    lines.append("")
    lines.append("NO DEPLOY PERFORMED — this is a plan. Deploying is the operator's act "
                 "(ADR-92 Decision 3: write-yes / commit-no / autonomy-no).")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="floor_mechanisms",
        description="Print the DRY-RUN plan for floor v1.5.0's mechanisms against one "
                    "consumer. Read-only: it never writes into a consumer tree.",
    )
    parser.add_argument(
        "--consumer",
        required=True,
        help="Path to the consumer repo to plan against (read-only).",
    )
    parser.add_argument(
        "--consumer-name",
        default=None,
        help="Repo id used to look up ecosystem/deployed-versions.yaml "
             "(default: the consumer directory name).",
    )
    parser.add_argument(
        "--manifest",
        default=None,
        help="Manifest to read (default: deploy/manifest-v1.5.0.yaml).",
    )
    args = parser.parse_args(argv)
    consumer = Path(args.consumer).expanduser().resolve()
    if not consumer.exists():
        print(f"floor_mechanisms: consumer path does not exist: {consumer}", file=sys.stderr)
        return 2
    print(plan(
        consumer,
        manifest=Path(args.manifest).resolve() if args.manifest else None,
        consumer_name=args.consumer_name,
    ))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
