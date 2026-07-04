"""deploy/release_lint.py — release-anchor + essence-spec lint (P1, closes R6).

**Read-only** (Layer-2, ADR-28/36): reads the hub tree + one ``git rev-parse``;
writes nothing, never touches a consumer.

One methodology release must carry ONE version truth. Before this lint, that
truth was smeared across five anchors with nothing checking agreement (finding
R6): the ADR-91 git tag, the manifest's ``methodology_version``, the precommit
carrier's ``hub_hooks.rev``, the tier1-lifecycle plugin version (read live from
plugin.json, pinned nowhere), and the floor template sha256 sidecar. This lint
reconciles ALL of them to ``source_tag`` and FAILs on any disagreement.

It also validates the essence-spec sections the P1 manifest conversion added
(``components:`` / ``doc_shapes:`` / ``anchors:``), including the P1 lifecycle
boundary: only ``status: active`` is legal this release — ``deprecated`` /
``removed`` (tombstones) unlock in P2, gated on operator decision D3, so a
tombstone landing early fails loud here instead of silently meaning nothing.

Checks (each FAIL exits 1; WARN informs):

- C1 spec coherence — manifest for the version exists + parses;
  ``methodology_version`` matches the requested version; ``source_tag`` ==
  ``v<methodology_version>``.
- C2 git tag — ``source_tag`` resolves in the hub. Missing tag is a **WARN**,
  not a FAIL: the operator tags at release (ADR-91), so pre-tag lint runs are a
  legitimate authoring state; ``deploy/tool.py`` preflight is the hard gate at
  execute time.
- C3 hub_hooks rev — the precommit carrier's ``hub_hooks.rev`` == ``source_tag``
  (the version-coupling anchor).
- C4 plugin pin — ``anchors.plugin_version`` == the live
  ``plugins/tier1-lifecycle/.claude-plugin/plugin.json`` ``version``.
- C5 floor pin — ``anchors.floor_sha256`` == the shipped
  ``templates/child-methodology-floor.sha256`` sidecar == the recomputed
  sha256 of ``templates/child-methodology-floor.md.tmpl`` bytes.
- C6 components schema — section present + non-empty; ids unique; ``kind`` /
  ``status`` / ``verify`` in vocabulary; ``removed_in`` required iff
  ``status: removed`` (forbidden on active); every component's ``carrier``
  resolves to a manifest carrier id; every IMPLEMENTED carrier has >=1
  component (the two sections cannot drift apart silently); ``roster`` is null
  or ``{section, line}`` with a known section; ``waivable`` is a bool when
  present and REQUIRED on every ``status: active`` component once the manifest
  declares it ([#244] P4 — the hub-side non-waivable floor set the Informant
  Tier-3 classifier reads; older pre-P4 manifests without the field stay green).
- C7 doc_shapes mirror — the spec's ``doc_shapes`` exactly mirrors the current
  authoritative constants: non-empty spines == ``audit.py::_CANONICAL_SPINE``;
  the ``freshness_gated: true`` set ==
  ``canonical_freshness_gate.DEFAULT_FRESHNESS_FILES``. The mirror fails loud
  instead of drifting; audit.py stays the reader of record this release.
- C8 engages ([#252] Slice B) — every ``status: active`` component carries a
  well-formed ``engages: {trigger, observable, expect}`` triple (the lived-workflow
  observer's enforcement-in-effect oracle, ADR-81 leg-e). ``trigger`` in the arc
  vocabulary, ``observable`` a valid external channel, ``expect`` a non-empty
  string or ``{absent: true, signature}`` (tombstone/prune-conformance). Gated only
  once the manifest DECLARES engages, so pre-Slice-B manifests stay green (the
  waivable [#244] P4 pattern). Removed components MAY carry it (validated if present).

HONEST LIMIT (state-what-it-does-not-do): this lint is **manually invoked**
this phase — it is wired into neither ``ALL_CHECKS`` nor the deploy preflight,
so nothing runs it automatically. Recommended wiring (a later, behavior-
changing step for the architect to place): ``deploy/tool.py`` preflight, so an
anchor-inconsistent release cannot be assessed/executed at all.

CLI::

    python deploy/release_lint.py --version 1.1.0        # exit 1 on any FAIL
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import click
import yaml

_DEPLOY_DIR = Path(__file__).resolve().parent
_HUB_ROOT = _DEPLOY_DIR.parent

PLUGIN_JSON_REL = "plugins/tier1-lifecycle/.claude-plugin/plugin.json"
FLOOR_TMPL_REL = "templates/child-methodology-floor.md.tmpl"
FLOOR_SIDECAR_REL = "templates/child-methodology-floor.sha256"

COMPONENT_KINDS = {"organ", "hook", "command", "skill", "doc-shape", "config"}
# P2 (D3): 2-state lifecycle — active | removed (no `deprecated` tier). A removed
# component is a tombstone: retained entry, artifacts pruned by the remove leg.
# C6 requires `removed_in:` iff status:removed and forbids it on active.
ALLOWED_STATUSES = {"active", "removed"}
# `engaged` (Slice B, [#252]): a leg-e acceptance class for a component whose firing is
# proven by the lived-workflow observer against a real arc (not fire_test/hash/config).
VERIFY_CLASSES = {"fire", "hash", "wired", "engaged"}
ROSTER_SECTIONS = {"header", "command", "skill", "precommit-hook", "session-hook"}
# engages: vocabulary (C8). Triggers split arc-stage (the branch->edit->commit->wrap
# lifecycle the observer gates) from non-arc (present in the oracle, classified OUT-OF-ARC).
ENGAGES_TRIGGERS = {
    "session-start", "edit", "pre-commit", "commit-msg", "pre-push", "stop",  # arc stages
    "operator-invoke", "deploy-time",  # non-arc
}
ENGAGES_CHANNELS = {"hook-stdout", "git-state", "transcript-event"}  # external channels only


@dataclass(frozen=True)
class Finding:
    """One lint result: check id, pass|warn|fail, and human evidence."""

    check: str
    status: str  # "pass" | "warn" | "fail"
    evidence: str


def _fail(check: str, evidence: str) -> Finding:
    return Finding(check, "fail", evidence)


def _warn(check: str, evidence: str) -> Finding:
    return Finding(check, "warn", evidence)


def _pass(check: str, evidence: str) -> Finding:
    return Finding(check, "pass", evidence)


# ---------------------------------------------------------------------------
# Git tag probe — injectable so tests never need a real tag.
# ---------------------------------------------------------------------------

TagProbe = Callable[[str, Path], "bool | None"]


def default_tag_probe(tag: str, repo_root: Path) -> bool | None:
    """True/False = tag resolves / doesn't; None = git itself errored."""
    try:
        res = subprocess.run(  # noqa: S603,S607 — fixed argv, no shell
            ["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}"],
            cwd=str(repo_root), capture_output=True,
        )
    except OSError:
        return None
    return res.returncode == 0


# ---------------------------------------------------------------------------
# Authoritative doc-shape constants (C7's comparison targets). Imported from
# scripts/ with the enforcement_coverage.py fallback pattern; the import is
# module-global (the hub's constants), independent of the linted repo_root —
# deliberate: the spec MIRRORS the hub organs, wherever the spec file lives.
# ---------------------------------------------------------------------------


def _authoritative_doc_shapes() -> tuple[dict[str, list[str]], list[str]]:
    scripts_dir = _HUB_ROOT / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    import audit as _audit  # noqa: E402
    import canonical_freshness_gate as _cfg  # noqa: E402

    return dict(_audit._CANONICAL_SPINE), list(_cfg.DEFAULT_FRESHNESS_FILES)


# ---------------------------------------------------------------------------
# The checks. Each takes what it needs and returns findings; ``lint`` composes.
# ---------------------------------------------------------------------------


def _load_spec(repo_root: Path, bare_version: str) -> tuple[dict[str, Any] | None, list[Finding]]:
    path = repo_root / "deploy" / f"manifest-v{bare_version}.yaml"
    if not path.exists():
        return None, [_fail("C1-spec", f"no manifest for v{bare_version} (expected {path})")]
    try:
        spec = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return None, [_fail("C1-spec", f"manifest did not parse ({path.name}): {exc}")]
    if not isinstance(spec, dict):
        return None, [_fail("C1-spec", f"manifest is not a mapping ({path.name})")]
    return spec, []


def check_version_coherence(spec: dict[str, Any], bare_version: str) -> list[Finding]:
    """C1 — methodology_version == requested version; source_tag == v<version>."""
    declared = str(spec.get("methodology_version", "")).strip()
    tag = str(spec.get("source_tag", "")).strip()
    problems: list[str] = []
    if declared != bare_version:
        problems.append(f"methodology_version {declared!r} != requested {bare_version!r}")
    if tag != f"v{declared}":
        problems.append(f"source_tag {tag!r} != v{declared}")
    if problems:
        return [_fail("C1-spec", "; ".join(problems))]
    return [_pass("C1-spec", f"methodology_version {declared} / source_tag {tag} coherent")]


def check_tag(spec: dict[str, Any], repo_root: Path, tag_probe: TagProbe) -> list[Finding]:
    """C2 — the release tag resolves (WARN pre-tag: the operator tags at release)."""
    tag = str(spec.get("source_tag", "")).strip()
    resolved = tag_probe(tag, repo_root)
    if resolved is True:
        return [_pass("C2-tag", f"git tag {tag} resolves in the hub")]
    if resolved is False:
        return [_warn("C2-tag", f"git tag {tag} does not resolve yet -- pre-release state; "
                                "the operator tags at release (deploy preflight is the hard gate)")]
    return [_warn("C2-tag", "git tag probe errored -- could not read hub tags")]


def check_hub_hooks_rev(spec: dict[str, Any]) -> list[Finding]:
    """C3 — precommit carrier hub_hooks.rev == source_tag (version-coupling anchor)."""
    tag = str(spec.get("source_tag", "")).strip()
    for entry in spec.get("carriers") or []:
        if isinstance(entry, dict) and entry.get("id") == "precommit":
            rev = str((((entry.get("target") or {}).get("hub_hooks")) or {}).get("rev", "")).strip()
            if not rev:
                return [_fail("C3-hub-hooks-rev", "precommit carrier declares no hub_hooks.rev")]
            if rev != tag:
                return [_fail("C3-hub-hooks-rev",
                              f"hub_hooks.rev {rev!r} != source_tag {tag!r} (anchor disagreement)")]
            return [_pass("C3-hub-hooks-rev", f"hub_hooks.rev {rev} == source_tag")]
    return [_fail("C3-hub-hooks-rev", "no precommit carrier with a hub_hooks.rev found")]


def check_plugin_pin(spec: dict[str, Any], repo_root: Path) -> list[Finding]:
    """C4 — anchors.plugin_version == the live tier1-lifecycle plugin.json version."""
    pinned = str((spec.get("anchors") or {}).get("plugin_version", "")).strip()
    if not pinned:
        return [_fail("C4-plugin-pin", "spec declares no anchors.plugin_version")]
    pj = repo_root / PLUGIN_JSON_REL
    if not pj.exists():
        return [_fail("C4-plugin-pin", f"plugin.json not found: {PLUGIN_JSON_REL}")]
    try:
        live = str(json.loads(pj.read_text(encoding="utf-8")).get("version", "")).strip()
    except (OSError, json.JSONDecodeError) as exc:
        return [_fail("C4-plugin-pin", f"plugin.json unreadable: {exc}")]
    if pinned != live:
        return [_fail("C4-plugin-pin",
                      f"anchors.plugin_version {pinned!r} != live plugin.json {live!r}")]
    return [_pass("C4-plugin-pin", f"plugin_version {pinned} == live plugin.json")]


def check_floor_pin(spec: dict[str, Any], repo_root: Path) -> list[Finding]:
    """C5 — anchors.floor_sha256 == sidecar == recomputed sha256 of the floor template."""
    pinned = str((spec.get("anchors") or {}).get("floor_sha256", "")).strip().lower()
    if not pinned:
        return [_fail("C5-floor-pin", "spec declares no anchors.floor_sha256")]
    tmpl = repo_root / FLOOR_TMPL_REL
    sidecar = repo_root / FLOOR_SIDECAR_REL
    if not tmpl.exists() or not sidecar.exists():
        return [_fail("C5-floor-pin", "floor template and/or sha256 sidecar missing")]
    actual = hashlib.sha256(tmpl.read_bytes()).hexdigest()
    shipped = sidecar.read_text(encoding="utf-8").strip().lower()
    problems: list[str] = []
    if pinned != shipped:
        problems.append(f"spec pin {pinned[:12]}.. != sidecar {shipped[:12]}..")
    if shipped != actual:
        problems.append(f"sidecar {shipped[:12]}.. != actual template bytes {actual[:12]}.. (stale sidecar)")
    if problems:
        return [_fail("C5-floor-pin", "; ".join(problems))]
    return [_pass("C5-floor-pin", f"floor sha256 {pinned[:12]}.. == sidecar == template bytes")]


def check_components(spec: dict[str, Any]) -> list[Finding]:
    """C6 — components schema (incl. waivable, [#244] P4) + components<->carriers cross-check."""
    components = spec.get("components")
    if not isinstance(components, list) or not components:
        return [_fail("C6-components", "spec has no components: section (essence-spec v1 requires it)")]
    carrier_ids = {str(c.get("id")) for c in spec.get("carriers") or [] if isinstance(c, dict)}
    implemented = {str(c.get("id")) for c in spec.get("carriers") or []
                   if isinstance(c, dict) and c.get("implemented")}
    # waivable ([#244] P4): required on status:active ONLY once the manifest declares
    # it (so older pre-P4 manifests without the field stay green); bool when present.
    declares_waivable = any(isinstance(c, dict) and "waivable" in c for c in components)
    problems: list[str] = []
    seen: set[str] = set()
    covered: set[str] = set()
    for comp in components:
        if not isinstance(comp, dict):
            problems.append(f"non-mapping component entry: {comp!r}")
            continue
        cid = str(comp.get("id", "")).strip()
        if not cid:
            problems.append("component with no id")
            continue
        if cid in seen:
            problems.append(f"duplicate component id {cid!r}")
        seen.add(cid)
        if comp.get("kind") not in COMPONENT_KINDS:
            problems.append(f"{cid}: kind {comp.get('kind')!r} not in {sorted(COMPONENT_KINDS)}")
        status = comp.get("status")
        if status not in ALLOWED_STATUSES:
            problems.append(f"{cid}: status {status!r} not in {sorted(ALLOWED_STATUSES)} "
                            "(2-state lifecycle, D3)")
        # Tombstone coherence (P2): removed_in is REQUIRED iff status:removed and
        # FORBIDDEN on active — so a tombstone always names its retiring release and
        # an active component can never masquerade as one.
        removed_in = comp.get("removed_in")
        if status == "removed":
            if not str(removed_in or "").strip():
                problems.append(f"{cid}: status:removed requires a removed_in: (the retiring release)")
        elif removed_in is not None:
            problems.append(f"{cid}: removed_in {removed_in!r} set on a non-removed (status {status!r}) component")
        if comp.get("verify") not in VERIFY_CLASSES:
            problems.append(f"{cid}: verify {comp.get('verify')!r} not in {sorted(VERIFY_CLASSES)}")
        wv = comp.get("waivable")
        if wv is not None and not isinstance(wv, bool):
            problems.append(f"{cid}: waivable {wv!r} must be a bool (true/false)")
        if declares_waivable and status == "active" and "waivable" not in comp:
            problems.append(f"{cid}: status:active requires waivable: <bool> "
                            "(Informant Tier-3 non-waivable set, [#244] P4)")
        carrier = str(comp.get("carrier", "")).strip()
        if carrier not in carrier_ids:
            problems.append(f"{cid}: carrier {carrier!r} resolves to no manifest carrier")
        elif status != "removed":
            # A removed component's carrier must still RESOLVE (checked above), but it
            # does NOT count toward "implemented carrier covered" — a tombstone is not
            # live coverage.
            covered.add(carrier)
        roster = comp.get("roster")
        if roster is not None:
            if (not isinstance(roster, dict)
                    or roster.get("section") not in ROSTER_SECTIONS
                    or not str(roster.get("line", "")).strip()):
                problems.append(f"{cid}: roster must be null or {{section: {sorted(ROSTER_SECTIONS)}, line}}")
    uncovered = implemented - covered
    if uncovered:
        problems.append(f"implemented carrier(s) with no component: {sorted(uncovered)}")
    if problems:
        return [_fail("C6-components", "; ".join(problems))]
    return [_pass("C6-components",
                  f"{len(components)} components valid; all {len(implemented)} implemented carriers covered")]


def _check_expect(cid: str, expect: Any) -> list[str]:
    """engages.expect: a non-empty string (must APPEAR), or {absent: true, signature: <str>}.

    The mapping form is the tombstone / prune-conformance oracle — the signature must
    NOT appear in the channel (the pruned component did not fire).
    """
    if isinstance(expect, str):
        return [] if expect.strip() else [f"{cid}: engages.expect is an empty string"]
    if isinstance(expect, dict):
        problems: list[str] = []
        if expect.get("absent") is not True:
            problems.append(f"{cid}: engages.expect mapping must set absent: true (tombstone form)")
        sig = expect.get("signature")
        if not isinstance(sig, str) or not sig.strip():
            problems.append(f"{cid}: engages.expect.signature must be a non-empty string")
        return problems
    return [f"{cid}: engages.expect must be a non-empty string or {{absent: true, signature}}"]


def check_engages(spec: dict[str, Any]) -> list[Finding]:
    """C8 — every active component carries a well-formed engages: triple ([#252] Slice B).

    The lived-workflow observer's enforcement-in-effect oracle (ADR-81 leg-e:
    presence != firing). Gated only once the manifest DECLARES engages — older
    pre-Slice-B manifests without it stay green (mirroring the waivable [#244] P4
    pattern). A removed component MAY carry engages (the ruff tombstone's expect-absent
    prune-conformance); when present it is validated the same way.
    """
    components = spec.get("components")
    if not isinstance(components, list) or not components:
        return []  # a missing/empty components section is already C6's FAIL
    declares = any(isinstance(c, dict) and "engages" in c for c in components)
    if not declares:
        return [_pass("C8-engages", "manifest declares no engages: (pre-Slice-B) -- not required")]
    problems: list[str] = []
    carried = 0
    for comp in components:
        if not isinstance(comp, dict):
            continue  # C6 handles non-mapping entries
        cid = str(comp.get("id", "?")).strip() or "?"
        eng = comp.get("engages")
        if eng is None:
            if comp.get("status") == "active":
                problems.append(f"{cid}: status:active requires an engages: triple ([#252] Slice B)")
            continue
        carried += 1
        if not isinstance(eng, dict):
            problems.append(f"{cid}: engages must be a mapping {{trigger, observable, expect}}")
            continue
        if eng.get("trigger") not in ENGAGES_TRIGGERS:
            problems.append(f"{cid}: engages.trigger {eng.get('trigger')!r} not in {sorted(ENGAGES_TRIGGERS)}")
        if eng.get("observable") not in ENGAGES_CHANNELS:
            problems.append(f"{cid}: engages.observable {eng.get('observable')!r} not in {sorted(ENGAGES_CHANNELS)}")
        problems.extend(_check_expect(cid, eng.get("expect")))
    if problems:
        return [_fail("C8-engages", "; ".join(problems))]
    return [_pass("C8-engages", f"{carried} components carry a valid engages: triple")]


def check_doc_shapes(spec: dict[str, Any]) -> list[Finding]:
    """C7 — doc_shapes mirrors the authoritative audit/freshness constants exactly."""
    shapes = spec.get("doc_shapes")
    if not isinstance(shapes, dict) or not shapes:
        return [_fail("C7-doc-shapes", "spec has no doc_shapes: section")]
    spine_truth, freshness_truth = _authoritative_doc_shapes()
    spec_spines = {f: list(s.get("spine") or []) for f, s in shapes.items()
                   if isinstance(s, dict) and s.get("spine")}
    spec_gated = sorted(f for f, s in shapes.items()
                        if isinstance(s, dict) and s.get("freshness_gated"))
    problems: list[str] = []
    if spec_spines != spine_truth:
        only_spec = sorted(set(spec_spines) - set(spine_truth))
        only_truth = sorted(set(spine_truth) - set(spec_spines))
        diff = sorted(f for f in set(spec_spines) & set(spine_truth)
                      if spec_spines[f] != spine_truth[f])
        problems.append(f"spine mismatch vs audit._CANONICAL_SPINE "
                        f"(spec-only {only_spec}, audit-only {only_truth}, differing {diff})")
    if spec_gated != sorted(freshness_truth):
        problems.append(f"freshness_gated set {spec_gated} != "
                        f"DEFAULT_FRESHNESS_FILES {sorted(freshness_truth)}")
    if problems:
        return [_fail("C7-doc-shapes", "; ".join(problems))]
    return [_pass("C7-doc-shapes",
                  f"{len(spec_spines)} spines + {len(spec_gated)} freshness-gated files mirror the organs")]


# ---------------------------------------------------------------------------
# Composition + CLI.
# ---------------------------------------------------------------------------


def lint(repo_root: Path, version: str, *, tag_probe: TagProbe = default_tag_probe) -> list[Finding]:
    """Run every check for one release against ``repo_root``. Read-only."""
    bare = version[1:] if version.startswith("v") else version
    spec, findings = _load_spec(Path(repo_root), bare)
    if spec is None:
        return findings
    findings.extend(check_version_coherence(spec, bare))
    findings.extend(check_tag(spec, Path(repo_root), tag_probe))
    findings.extend(check_hub_hooks_rev(spec))
    findings.extend(check_plugin_pin(spec, Path(repo_root)))
    findings.extend(check_floor_pin(spec, Path(repo_root)))
    findings.extend(check_components(spec))
    findings.extend(check_doc_shapes(spec))
    findings.extend(check_engages(spec))
    return findings


def has_fail(findings: list[Finding]) -> bool:
    return any(f.status == "fail" for f in findings)


@click.command()
@click.option("--version", "version", required=True,
              help="Methodology release to lint (e.g. v1.1.0 / 1.1.0); selects the manifest.")
def main(version: str) -> None:
    """Lint one release's version anchors + essence-spec sections (read-only)."""
    findings = lint(_HUB_ROOT, version)
    marker = {"pass": "ok  ", "warn": "WARN", "fail": "FAIL"}
    for f in findings:
        click.echo(f"release-lint {marker[f.status]} {f.check}: {f.evidence}")
    fails = sum(1 for f in findings if f.status == "fail")
    warns = sum(1 for f in findings if f.status == "warn")
    click.echo(f"release-lint: {fails} FAIL, {warns} WARN, "
               f"{len(findings) - fails - warns} pass")
    if fails:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
