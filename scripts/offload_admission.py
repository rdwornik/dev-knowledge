#!/usr/bin/env python
"""offload_admission.py — the admission gate for the `offload` role, and its seeded defects.

WHAT THIS IS. `docs/intake/2026-09-06-tech-copilot-offload-role-and-account-map.md` (intake
#75) describes an `offload` seat as **read-only thinking**: ranked retrieval with locators,
never a verdict. This module is the mechanism that decides whether a route may hold that role.
It takes an ADMISSION RECORD — what a candidate CLI actually returned on a scored run — and
adjudicates it against the corpus the record claims to have read and against
`ecosystem/provider-registry.yaml`, which is the closed vocabulary of providers and the CLIs
that reach them.

WHY IT IS BUILT AROUND SEEDED DEFECTS RATHER THAN A HAPPY PATH. The `[#627]` agy admission is
the precedent this follows, and its lesson is in its own verdict: a pack that is only ever RUN
against intact evidence measures the run, not the gate. An admission that passes because
nothing was broken proves nothing about what happens when something is. So the
`SEEDED_DEFECTS` below are not test fixtures that happen to live near the code — they are the
gate's specification, and their number is what `--seeded-defects` MEASURES on the day it runs
rather than what a line of prose here claims.
`build_seeded_suite()` constructs each one as the ADMISSIBLE record with
exactly ONE field mutated, so a refusal is attributable to the seed rather than to unrelated
breakage, and `run_seeded_suite()` re-measures the whole set rather than asserting a number.

EVERY SEEDED DEFECT IS A RECORDED SCAR, not an invented one. Named at each definition:

  substituted-model      `[#492]` — a client quietly served `grok-4.5` and cost a window;
                         standing ruling Q9 made the substitution probe a hard precondition.
  locator-escapes-corpus the `[#627]` verdict's flagship failure — the whole-repo-scan item
                         failed three consecutive draws "always by analysing a repository
                         that is not `.dev-knowledge`".
  fabricated-*           the 2026-09-05 Gemini corpus-coherence bar: every locator re-opened
                         on disk, "a finding whose locator does not hold is dropped and
                         counted as a fabrication". Six of six exact, zero fabrications.
  locator-drift          the same bar's second half — "locator-exactness is not
                         claim-correctness"; a quote that is not at the line it cites.
  verdict-bearing        intake #75 section 1: the seat "never a verdict — it does not rule,
                         close, merge, or dispose".
  cli-mismatch           the poisoned-name scar in the registry's own `xai` row: `agent.exe`
                         is byte-identical to `grok.exe`, so a name alone does not identify a
                         binary. The registry is the authority on which CLI reaches a
                         provider; a record that disagrees is refused, not reconciled.
  empty-run              this module's own reason to exist, stated above.
  unranked / duplicate   "ranked retrieval" is half the role definition. A ranking in which
                         two findings share a rank is not a ranking.
  unpinned-model         and
  attestation-is-a-      the registry's own `cursor` row: "Auto is a SELECTION MODE, not a
  selection-mode         model ... an undisclosed model is an UNREPRODUCIBLE RESULT". Both
                         were seeded from a LIVE Copilot run on 2026-09-09, not from theory:
                         `--model` refused every id the CLI's own `help config` documents,
                         and the seat then self-reported `auto` while the CLI's own
                         `--usage-output-file` named `mai-code-1.1-flash`. Evidence:
                         `docs/audits/2026-09-09-technical-offload-admission.md`.

WHAT THIS MODULE DOES NOT DO, stated so a green verdict is not over-read:

  * It does not RUN a candidate CLI. It adjudicates a record someone else produced, which is
    what keeps it Layer-2-clean (ADR-28/36): it reads files and compares strings, it executes
    nothing and it writes nothing.
  * It does not write `ecosystem/routing-table.yaml`. Creating the `offload` role row is a
    separate act with a separate owner — and on this host it would immediately diverge from
    the L0 derived copy that `scripts/routing_agreement.py` checks, which no in-repo change
    may repair. An ADMITTED verdict is the evidence for that act, never the act itself.
  * It says nothing about cost. Intake #75 makes "tokens saved" a scorecard line
    (`scripts/window_metrics.py`); a rate-versus-cost judgement is that surface's, not this
    one's.

ABSENCE IS A REPORTED GAP, NOT A PASS — register ruling Z-G4, the same posture
`scripts/routing_agreement.py` states for an absent L0 copy. With no admission record on file
the CLI reports NOT ADMITTED with the reason "no record", exits non-zero, and does not
manufacture a verdict out of silence.
"""
from __future__ import annotations

import json
import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any
from collections.abc import Callable

import click

try:
    import yaml
except ImportError as exc:  # pragma: no cover - declared dependency
    raise SystemExit(f"offload_admission: pyyaml is required: {exc!r}")

try:  # dual import shim — `from scripts import offload_admission` must work too
    from scripts import provider_registry as _pr
except ImportError:  # pragma: no cover - exercised by the package-mode regression test
    import provider_registry as _pr

#: The role this gate adjudicates. One role, named, because a gate that adjudicates "whatever
#: the record says" cannot refuse a record that names the wrong role.
ROLE = "offload"

#: The closed refusal vocabulary. Order is the order `adjudicate` emits in, and every member
#: has exactly one seeded case in `SEEDED_DEFECTS` — `test_offload_admission.py` asserts the
#: two sets are equal, so a code added here without a seed is a RED, not a silent gap.
REFUSAL_CODES: tuple[str, ...] = (
    "role-mismatch",
    "unknown-provider",
    "cli-mismatch",
    "unpinned-model",
    "missing-attestation",
    "attestation-is-a-selection-mode",
    "substituted-model",
    "empty-run",
    "unranked-finding",
    "duplicate-rank",
    "rank-gap",
    "verdict-bearing",
    "undeclared-field",
    "unknown-category",
    "locator-malformed",
    "locator-escapes-corpus",
    "fabricated-file",
    "fabricated-line",
    "locator-drift",
    "planted-defect-missed",
    "misclassified-defect",
)


#: The closed category vocabulary `PROBE_QUESTION` asks for. Checking it is not pedantry: a
#: record admitted with `category: "anything"` is a candidate that answered a question nobody
#: asked, and the admission would then certify retrieval the probe never measured.
FINDING_CATEGORIES: frozenset[str] = frozenset({
    "contradiction", "unenforced-rule", "duplicated-clause"})


#: The record's closed field set, and a finding's. The shape `PROBE_QUESTION` specifies is
#: EXACT, so anything outside it is refused rather than ignored. Refusing one field name --
#: `verdict` -- while accepting every other key was a denylist wearing an invariant's
#: clothes: a candidate escapes a denylist by writing `recommendation` instead, and the
#: retrieval-only boundary intake #75 states is about rulings, not about a spelling.
RECORD_FIELDS: frozenset[str] = frozenset({
    "role", "provider", "cli", "requested_model", "served_model", "findings"})
FINDING_FIELDS: frozenset[str] = frozenset({"rank", "category", "locator", "quote"})

#: Undeclared keys that already carry their OWN refusal code, so the schema check steps over
#: them. Two codes for one defect would make the seeded suite unattributable, which is the
#: property the suite exists to hold.
_FIELDS_WITH_OWN_CODE: frozenset[str] = frozenset({"verdict"})


#: Tokens that name how a model was CHOSEN rather than which model it was. Refused in BOTH
#: directions — as a pin and as an attestation — on the precedent already recorded in
#: `ecosystem/provider-registry.yaml`'s `cursor` row: *"Auto is a SELECTION MODE, not a model,
#: and Cursor does not disclose what served a call — so an undisclosed model is an
#: UNREPRODUCIBLE RESULT, and a lane whose result cannot be reproduced is not evidence."*
SELECTION_MODES: frozenset[str] = frozenset({"auto", "default", "inherit"})


class AdmissionError(RuntimeError):
    """The record or the registry could not be read. FAIL-LOUD: callers report, never swallow."""


@dataclass(frozen=True)
class PlantedSite:
    """One place a planted defect can legitimately be cited from."""

    rel: str
    line: int
    needle: str

    @property
    def locator(self) -> str:
        """The `<file>:<line>` form a candidate returns."""
        return f"{self.rel}:{self.line}"


@dataclass(frozen=True)
class PlantedDefect:
    """One defect a corpus plants: every place it can be cited, and what it IS.

    Both halves are the answer, and only the pair is retrieval. A locator proves the
    candidate looked at the right line; the category is the classification `PROBE_QUESTION`
    actually asks for, so a run that names three right lines and files all three as
    `contradiction` sits inside the vocabulary and has answered nothing. Membership in the
    enum is not the check -- agreement with the planted category is.
    """

    category: str
    sites: tuple[PlantedSite, ...]

    @property
    def locators(self) -> tuple[str, ...]:
        """The acceptable locators, in the form a record carries them."""
        return tuple(s.locator for s in self.sites)


@dataclass(frozen=True)
class Refusal:
    """One reason the record was refused, with the finding it attaches to when it has one."""

    code: str
    detail: str

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.code}: {self.detail}"


@dataclass(frozen=True)
class Verdict:
    """The adjudication. `admitted` is True only when `refusals` is empty."""

    admitted: bool
    refusals: tuple[Refusal, ...]
    findings_seen: int
    locators_verified: int
    detail: str

    @property
    def codes(self) -> tuple[str, ...]:
        """The refusal codes, in emission order — what a test asserts against."""
        return tuple(r.code for r in self.refusals)


# ---------------------------------------------------------------------------------------
# reading
# ---------------------------------------------------------------------------------------

def load_record(path: Path) -> dict[str, Any]:
    """Parse an admission record from YAML **or** JSON.

    One loader for both on purpose rather than as a shortcut: JSON is a YAML subset, and a
    candidate CLI's `--output-format json` is the shape a real run arrives in, while a record
    committed beside an audit artifact reads better as YAML. Accepting both means the
    committed evidence and the raw transport parse through the same code path, so a record
    cannot be admissible in one form and not the other.
    """
    p = Path(path)
    if not p.is_file():
        raise AdmissionError(f"admission record absent: {p}")
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise AdmissionError(f"admission record unparseable ({p}): {exc}") from exc
    if not isinstance(data, dict):
        raise AdmissionError(f"admission record is not a mapping: {p}")
    return data


def _registry_cli(provider: str, registry_path: Path | None) -> str | None:
    """The CLI the registry binds to `provider`, or None when the provider is not declared."""
    try:
        rows = _pr.providers(registry_path)
    except _pr.RegistryError as exc:
        raise AdmissionError(f"provider registry could not be read: {exc}") from exc
    except OSError as exc:
        # The reader normalises its own PARSE failures and not its I/O ones, so an existing
        # but unreadable registry escaped as a bare OSError. Same class as an unreadable
        # corpus: the gate has not found a defect in the record, it has failed to compute
        # its ground truth, and Z-G4 says report the gap. A traceback is not a report.
        raise AdmissionError(
            f"provider registry {registry_path} exists but could not be read ({exc}); "
            f"provider identity cannot be established, so this gate reports the gap") from None
    row = rows.get(provider)
    if row is None:
        return None
    cli = row.get("cli")
    return None if cli is None else str(cli)


# ---------------------------------------------------------------------------------------
# locator verification — the half the Gemini precedent measures
# ---------------------------------------------------------------------------------------

def _split_locator(raw: str) -> tuple[str, int]:
    """`"path:line"` -> `(path, line)`. Raises ValueError on anything else."""
    text = str(raw).strip()
    if ":" not in text:
        raise ValueError("carries no `:line` suffix")
    path, _, line = text.rpartition(":")
    if not path:
        raise ValueError("names no file")
    try:
        n = int(line)
    except ValueError:
        raise ValueError(f"line part {line!r} is not an integer") from None
    if n < 1:
        raise ValueError(f"line {n} is not a 1-based line number")
    return path, n


def _resolve_in_corpus(rel: str, corpus_root: Path) -> Path:
    """Resolve `rel` under `corpus_root`, refusing anything that leaves the tree.

    The string is never the final authority. A lexical check alone is porous on three axes —
    absoluteness is platform-flavoured, Win32 strips trailing dots and spaces so `".. "` and
    `".."` name the same directory while comparing unequal, and a symlinked ancestor
    redirects a textually-innocent path — so containment is proven on the RESOLVED path, with
    the lexical pass kept only for the better message.
    """
    if PureWindowsPath(rel).is_absolute() or PurePosixPath(rel).is_absolute():
        raise ValueError("is an absolute path, so it names no place in the declared corpus")
    parts = PureWindowsPath(rel).parts  # splits on both `/` and `\`
    if any(p.rstrip(" .") != p or p == ".." for p in parts):
        raise ValueError("climbs out of the declared corpus")
    base = Path(corpus_root).resolve()
    resolved = (base / rel).resolve()
    if not resolved.is_relative_to(base):
        raise ValueError("resolves outside the declared corpus")
    return resolved


def _verify_ground_truth(ground_truth: tuple[PlantedDefect, ...],
                        corpus_root: Path) -> None:
    """Prove the corpus still carries every planted clause, or FAIL LOUD.

    Coverage credited from a locator string and a category says nothing about the corpus: a
    replaced or arbitrary tree carrying any text at those lines would score a candidate as
    having found every planted defect, which measures the answer against nothing. A ground
    truth is a claim about a PARTICULAR corpus, so it is checked against the one in hand
    before it is used to score anyone.

    This raises rather than refusing, because it is not a statement about the record. The
    record may be perfect; the instrument is not the one the ground truth describes, and
    Z-G4 says report that gap.
    """
    for defect in ground_truth:
        for site in defect.sites:
            try:
                target = _resolve_in_corpus(site.rel, corpus_root)
                lines = target.read_text(encoding="utf-8", errors="replace").splitlines()
            except (ValueError, OSError) as exc:
                raise AdmissionError(
                    f"the declared ground truth places a {defect.category!r} at "
                    f"{site.locator}, and that site could not be read in {corpus_root} "
                    f"({exc}); nothing can be scored against a corpus this gate cannot "
                    f"open") from None
            if site.line > len(lines) or site.needle not in lines[site.line - 1]:
                raise AdmissionError(
                    f"the declared ground truth places a {defect.category!r} at "
                    f"{site.locator} carrying {site.needle!r}, and the corpus at "
                    f"{corpus_root} does not carry it there; this is not the corpus the "
                    f"ground truth describes, so no answer can be scored against it")


def _verify_locator(finding: dict[str, Any], corpus_root: Path) -> Refusal | None:
    """Re-open the finding's locator on disk. `None` means it holds exactly."""
    label = f"finding rank {finding.get('rank')!r}"
    raw = finding.get("locator")
    if not isinstance(raw, str) or not raw.strip():
        return Refusal("locator-malformed", f"{label} carries no locator")
    try:
        rel, line_no = _split_locator(raw)
    except ValueError as exc:
        return Refusal("locator-malformed", f"{label} locator {raw!r} {exc}")

    try:
        target = _resolve_in_corpus(rel, corpus_root)
    except ValueError as exc:
        return Refusal("locator-escapes-corpus", f"{label} locator {raw!r} {exc}")

    if not target.is_file():
        return Refusal("fabricated-file",
                       f"{label} cites {rel!r}, which does not exist in the corpus")
    try:
        text = target.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        # NOT a refusal: a refusal is a statement about the record, and this is a statement
        # about the corpus. The locator is candidate-controlled, so letting the OSError
        # escape hands a candidate a traceback where the documented outcome is a verdict.
        raise AdmissionError(
            f"{label} cites {rel}, which exists but could not be read ({exc}); the corpus "
            f"is unreadable, so this gate cannot compute its ground truth and reports the "
            f"gap rather than admitting or crashing (Z-G4)") from None
    lines = text.splitlines()
    if line_no > len(lines):
        return Refusal("fabricated-line",
                       f"{label} cites {rel}:{line_no}, but the file has {len(lines)} line(s)")

    quote = finding.get("quote")
    if not isinstance(quote, str) or not quote.strip():
        return Refusal("locator-drift",
                       f"{label} cites {rel}:{line_no} but quotes nothing, so the locator "
                       f"cannot be verified — an unverifiable locator is not a verified one")
    if quote.strip() not in lines[line_no - 1]:
        return Refusal("locator-drift",
                       f"{label} quotes {quote.strip()[:60]!r} at {rel}:{line_no}, which "
                       f"carries {lines[line_no - 1].strip()[:60]!r}")
    return None


# ---------------------------------------------------------------------------------------
# adjudication
# ---------------------------------------------------------------------------------------

def adjudicate(record: dict[str, Any],
               corpus_root: Path,
               registry_path: Path | None = None,
               ground_truth: tuple[PlantedDefect, ...] = ()) -> Verdict:
    """ADMIT or REFUSE one admission record. Refusals accumulate; they do not short-circuit.

    `ground_truth` is what the corpus plants: one `PlantedDefect` per defect, carrying the
    locators that legitimately name it AND the category a correct answer files it under. The
    record must name at least one locator per defect, under that defect's category. Without
    it a record clears this gate on SHAPE alone -- non-empty, uniquely ranked, locators that
    re-open -- so a candidate returning one unrelated real line would be admitted while
    having found nothing the probe exists to measure. Ground truth is corpus-specific, hence
    a parameter rather than a constant: the seeded suite and the live probe plant different
    defects, and an empty tuple means "this call is not scoring coverage" rather than
    "coverage passed".

    Accumulating is deliberate. A gate that stopped at the first refusal would report one
    defect per run, so a record with three would take three rounds to characterise and each
    round would read like a fresh discovery. The per-FINDING locator checks DO short-circuit,
    for the opposite reason: a file that does not exist has no line to be past the end of, so
    emitting `fabricated-line` beside `fabricated-file` would double-count one defect.
    """
    refusals: list[Refusal] = []

    role = record.get("role")
    if role != ROLE:
        refusals.append(Refusal(
            "role-mismatch",
            f"the record declares role {role!r}; this gate adjudicates {ROLE!r} only"))

    provider = str(record.get("provider") or "")
    declared_cli = record.get("cli")
    registry_cli = _registry_cli(provider, registry_path) if provider else None
    if not provider or registry_cli is None:
        refusals.append(Refusal(
            "unknown-provider",
            f"provider {provider!r} declares no CLI in "
            f"{_pr.REGISTRY_REL} — the registry is the closed vocabulary, so a route it "
            f"does not name is not a route this fleet can admit"))
    elif str(declared_cli or "") != registry_cli:
        refusals.append(Refusal(
            "cli-mismatch",
            f"the record runs {declared_cli!r} but {_pr.REGISTRY_REL} binds provider "
            f"{provider!r} to {registry_cli!r} — a CLI is identified by the registry, "
            f"never by the name the record happens to use"))

    requested = record.get("requested_model")
    served = record.get("served_model")
    if not isinstance(requested, str) or not requested.strip():
        refusals.append(Refusal(
            "unpinned-model",
            "the record declares no `requested_model` — a run whose model was chosen for it "
            "cannot be reproduced, and a result that cannot be reproduced is not evidence"))
    elif requested.strip().lower() in SELECTION_MODES:
        refusals.append(Refusal(
            "unpinned-model",
            f"`requested_model` is {requested!r}, which is a selection MODE rather than a "
            f"model — asking for `auto` is not a pin"))

    if not isinstance(served, str) or not served.strip():
        refusals.append(Refusal(
            "missing-attestation",
            "the record carries no `served_model` — without an attestation of what actually "
            "answered, a substituted model is indistinguishable from the pinned one"))
    elif served.strip().lower() in SELECTION_MODES:
        refusals.append(Refusal(
            "attestation-is-a-selection-mode",
            f"`served_model` is {served!r} — that names how the model was CHOSEN, not which "
            f"model answered, so the run is unattributable"))
    elif isinstance(requested, str) and requested.strip() and served.strip() != requested.strip():
        refusals.append(Refusal(
            "substituted-model",
            f"requested {requested!r} but {served!r} served — the run measured a model the "
            f"admission was not for"))

    findings = record.get("findings")
    findings = list(findings) if isinstance(findings, list) else []
    if not findings:
        refusals.append(Refusal(
            "empty-run",
            "the record carries no findings — an admission that passes because nothing was "
            "found proves nothing about the route"))

    ranks: list[int] = []
    for f in findings:
        if not isinstance(f, dict):
            refusals.append(Refusal("locator-malformed", f"finding {f!r} is not a mapping"))
            continue
        rank = f.get("rank")
        if not isinstance(rank, int) or isinstance(rank, bool) or rank < 1:
            refusals.append(Refusal(
                "unranked-finding",
                f"finding {f.get('locator')!r} carries rank {rank!r} — the role is RANKED "
                f"retrieval, and an unranked candidate list is not a ranking"))
        else:
            ranks.append(rank)

    duplicated = sorted({r for r in ranks if ranks.count(r) > 1})
    if duplicated:
        refusals.append(Refusal(
            "duplicate-rank",
            f"rank(s) {duplicated} are claimed by more than one finding — a ranking that "
            f"does not order its candidates is not a ranking"))
    elif len(ranks) == len(findings) and sorted(ranks) != list(range(1, len(ranks) + 1)):
        # Only when nothing else already accounts for the shape: ranks `1, 1` are ALSO
        # non-contiguous, and a second code for one defect is the unattributed refusal the
        # seeded suite exists to make impossible. `no repeats` was checked and `1..N` was
        # not, so `1, 3` -- or a lone `2` -- cleared a gate that asks for a ranking.
        refusals.append(Refusal(
            "rank-gap",
            f"ranks {sorted(ranks)} are not 1..{len(ranks)} — the question asks for a "
            f"ranking of the candidates returned, and a rank naming a place that is not "
            f"filled describes a list that was not returned"))

    # PRESENCE, not value. `verdict: ""` and `verdict: null` are not the absence of a
    # verdict field; they are a verdict field left blank, and the closed-schema check below
    # exempts `verdict` precisely because this code is supposed to own it. Reading the value
    # let the two checks hand the field to each other and admit it -- the pass-5 denylist
    # hole, one layer down.
    if "verdict" in record:
        refusals.append(Refusal(
            "verdict-bearing",
            f"the record carries a top-level verdict {record.get('verdict')!r} — the "
            f"offload seat returns candidates and where they live; ruling is another "
            f"seat's act"))
    for f in findings:
        if not isinstance(f, dict):
            continue
        if "verdict" in f:
            refusals.append(Refusal(
                "verdict-bearing",
                f"finding rank {f.get('rank')!r} carries verdict {f.get('verdict')!r} — the "
                f"offload seat returns candidates and where they live; ruling is another "
                f"seat's act"))

    undeclared = set(record) - RECORD_FIELDS - _FIELDS_WITH_OWN_CODE
    for f in findings:
        if isinstance(f, dict):
            undeclared |= set(f) - FINDING_FIELDS - _FIELDS_WITH_OWN_CODE
    if undeclared:
        # Sorted by REPR, never by value. YAML is a supported input and YAML keys are not
        # all strings, so `{extra: x, 1: x}` made this line compare a str against an int and
        # raise TypeError -- a traceback where the contract promises a refusal. The refusal
        # was already right; only the reporting of it could crash.
        named = ", ".join(sorted(repr(k) for k in undeclared))
        refusals.append(Refusal(
            "undeclared-field",
            f"the answer carries field(s) {named} "
            f"that the requested shape does not declare — the shape is CLOSED, so a ruling "
            f"cannot enter under a name the gate did not think to forbid"))

    for f in findings:
        if not isinstance(f, dict):
            continue
        category = f.get("category")
        if category not in FINDING_CATEGORIES:
            refusals.append(Refusal(
                "unknown-category",
                f"finding rank {f.get('rank')!r} is categorised {category!r}; the probe asks "
                f"for one of {', '.join(sorted(FINDING_CATEGORIES))}, and a category outside "
                f"that closed set is an answer to a question nobody asked"))

    verified = 0
    for f in findings:
        if not isinstance(f, dict):
            continue
        problem = _verify_locator(f, corpus_root)
        if problem is None:
            verified += 1
        else:
            refusals.append(problem)

    if ground_truth:
        _verify_ground_truth(ground_truth, corpus_root)
    for defect in ground_truth:
        at_site = [f for f in findings if isinstance(f, dict)
                   and str(f.get("locator") or "").strip() in defect.locators]
        if not at_site:
            refusals.append(Refusal(
                "planted-defect-missed",
                f"no finding names any of {', '.join(defect.locators)}; the corpus plants a "
                f"defect there and the record walked past it, so this is a MISS "
                f"— locator-exactness on the findings it DID return does not cover for it"))
        elif not any(f.get("category") == defect.category for f in at_site):
            filed = ", ".join(sorted({repr(f.get("category")) for f in at_site}))
            refusals.append(Refusal(
                "misclassified-defect",
                f"the defect at {', '.join(defect.locators)} is a {defect.category!r}; the "
                f"record cites the line and files it as {filed} — the right line under the "
                f"wrong heading answers the locator question, not the probe's"))

    admitted = not refusals
    if admitted:
        # Only claim coverage when coverage was actually scored: an ADMITTED line reading
        # "every planted defect named" on a call that supplied no ground truth would be the
        # same unearned certification this check exists to remove.
        covered = (f"all {len(ground_truth)} planted defect(s) named AND correctly "
                   f"categorised; " if ground_truth
                   else "coverage NOT scored, no ground truth supplied; ")
        detail = (f"ADMITTED — {verified}/{len(findings)} locator(s) re-opened on disk and "
                  f"exact, zero fabrications; {covered}{served!r} attested as served")
    else:
        detail = (f"NOT ADMITTED — {len(refusals)} refusal(s): "
                  + "; ".join(f"[{r.code}] {r.detail}" for r in refusals))
    return Verdict(admitted, tuple(refusals), len(findings), verified, detail)


# ---------------------------------------------------------------------------------------
# the seeded-defect suite — the gate's specification, re-measured rather than asserted
# ---------------------------------------------------------------------------------------

#: The corpus the seeded suite adjudicates against. Small, self-contained and written fresh
#: for each run so the suite never depends on the state of the repository it lives in — a
#: seeded case whose refusal moved because an unrelated file changed would be measuring the
#: repository rather than the gate.
_SUITE_CORPUS: dict[str, str] = {
    "protocols/EXAMPLE.md": (
        "# Example protocol\n"
        "\n"
        "A branch is merged with `--no-ff`, always.\n"
        "Commit summaries are imperative and under 72 characters.\n"
    ),
    "ecosystem/example.yaml": (
        "version: 1\n"
        "roles:\n"
        "  producer:\n"
        "    cli: claude-code\n"
    ),
}

#: A registry that satisfies `ecosystem/schema/provider_registry.py`, carrying only the row
#: the suite needs. Written per-run beside the corpus so the suite adjudicates against a
#: registry it controls, not against the live one — otherwise every seeded refusal would move
#: the day someone edits `ecosystem/provider-registry.yaml`.
_SUITE_REGISTRY = (
    "providers:\n"
    "  copilot-enterprise:\n"
    "    display_name: GitHub Copilot Enterprise\n"
    "    council_alias: null\n"
    "    cli: copilot\n"
    "    version_command:\n"
    "      - copilot\n"
    "      - --version\n"
    "models: {}\n"
)


def admissible_record() -> dict[str, Any]:
    """The record every seeded case is a single mutation of — and the POSITIVE CONTROL.

    The control is not decoration. A gate that refused everything would also refuse every
    seeded defect, so the negative suite means nothing without a case that this gate ADMITS.
    `test_offload_admission.py` asserts both halves.
    """
    return {
        "role": ROLE,
        "provider": "copilot-enterprise",
        "cli": "copilot",
        "requested_model": "claude-sonnet-4.5",
        "served_model": "claude-sonnet-4.5",
        "findings": [
            {
                "rank": 1,
                "category": "unenforced-rule",
                "locator": "protocols/EXAMPLE.md:4",
                "quote": "Commit summaries are imperative and under 72 characters.",
            },
            {
                "rank": 2,
                "category": "duplicated-clause",
                "locator": "ecosystem/example.yaml:4",
                "quote": "cli: claude-code",
            },
        ],
    }


#: A seed: one in-place mutation of an otherwise admissible record.
Mutation = Callable[[dict[str, Any]], Any]


def _mutate(fn: Mutation) -> dict[str, Any]:
    """Apply `fn` to a FRESH admissible record and return it.

    Fresh, not shared: `admissible_record()` rebuilds the nested finding dicts every call, so
    a mutation reaching into `record["findings"][0]` cannot leak into the next seeded case —
    which would make one seed's refusal appear under another's name.
    """
    rec = admissible_record()
    fn(rec)
    return rec


#: `{refusal code: (why this defect is realistic, mutation)}`. ONE mutation each, applied to
#: the admissible record — which is what makes a refusal attributable to the seed.
SEEDED_DEFECTS: dict[str, tuple[str, Mutation]] = {
    "role-mismatch": (
        "a record produced for a different role, filed against this gate",
        lambda r: r.__setitem__("role", "fan_out"),
    ),
    "unknown-provider": (
        "a route the registry's closed vocabulary does not name",
        lambda r: r.__setitem__("provider", "copilot-personal"),
    ),
    "cli-mismatch": (
        "the poisoned-name scar: a binary named by the record, not by the registry",
        lambda r: r.__setitem__("cli", "gh-copilot"),
    ),
    "unpinned-model": (
        "MEASURED on the live Copilot route 2026-09-09: `--model` refuses every id, so the "
        "server chooses and the run cannot be reproduced",
        lambda r: r.pop("requested_model"),
    ),
    "missing-attestation": (
        "[#492]: no record of what actually answered",
        lambda r: r.pop("served_model"),
    ),
    "attestation-is-a-selection-mode": (
        "MEASURED on the live Copilot route 2026-09-09: the seat self-reported `auto` while "
        "the CLI's usage file named `mai-code-1.1-flash`",
        lambda r: r.__setitem__("served_model", "auto"),
    ),
    "substituted-model": (
        "[#492] verbatim: the client quietly served a different model",
        lambda r: r.__setitem__("served_model", "gpt-5.4"),
    ),
    "empty-run": (
        "an admission that passes because nothing was found",
        lambda r: r.__setitem__("findings", []),
    ),
    "unranked-finding": (
        "ranked retrieval with no ranks",
        lambda r: r["findings"][1].pop("rank"),
    ),
    "duplicate-rank": (
        "a ranking in which two candidates share a place",
        lambda r: r["findings"][1].__setitem__("rank", 1),
    ),
    "rank-gap": (
        "a ranking with a hole in it: ranks that are unique and still not 1..N",
        lambda r: r["findings"][1].__setitem__("rank", 3),
    ),
    "verdict-bearing": (
        "intake #75: the seat rules, closes or disposes",
        lambda r: r["findings"][0].__setitem__("verdict", "CONFIRMED — close the row"),
    ),
    "unknown-category": (
        "a finding filed under a category the probe question does not define",
        lambda r: r["findings"][0].__setitem__("category", "anything"),
    ),
    "undeclared-field": (
        "a ruling smuggled in under a field name the requested shape does not declare",
        lambda r: r["findings"][0].__setitem__("recommendation", "close the row"),
    ),
    "locator-malformed": (
        "a locator with no line, so nothing can be re-opened",
        lambda r: r["findings"][0].__setitem__("locator", "protocols/EXAMPLE.md"),
    ),
    "locator-escapes-corpus": (
        "the [#627] flagship failure: a finding about a repository that is not this one",
        lambda r: r["findings"][0].__setitem__("locator", "../elsewhere/OTHER.md:1"),
    ),
    "fabricated-file": (
        "the Gemini bar: a locator naming a file that does not exist",
        lambda r: r["findings"][0].__setitem__("locator", "protocols/INVENTED.md:1"),
    ),
    "fabricated-line": (
        "a real file, a line number past its end",
        lambda r: r["findings"][0].__setitem__("locator", "protocols/EXAMPLE.md:900"),
    ),
    "locator-drift": (
        "locator-exactness is not claim-correctness: the quote is not at the line",
        lambda r: r["findings"][0].__setitem__("quote", "A branch is merged with `--no-ff`"),
    ),
    "planted-defect-missed": (
        "a shape-perfect answer that walked past a defect the corpus plants",
        lambda r: r["findings"].pop(1),
    ),
    "misclassified-defect": (
        "the right line under the wrong heading: a planted defect cited and mis-categorised",
        lambda r: r["findings"][0].__setitem__("category", "contradiction"),
    ),
}


#: The suite corpus's own GROUND TRUTH, matching what `admissible_record` returns. A defect
#: reachable from two files is not a miss because the candidate cited the other one, so the
#: sites are alternatives rather than a checklist.
SUITE_GROUND_TRUTH: tuple[PlantedDefect, ...] = (
    PlantedDefect("unenforced-rule", (PlantedSite(
        "protocols/EXAMPLE.md", 4, "Commit summaries are imperative"),)),
    PlantedDefect("duplicated-clause", (PlantedSite(
        "ecosystem/example.yaml", 4, "cli: claude-code"),)),
)

#: The seeds adjudicated WITH a coverage requirement. Deliberately not all of them: a seed
#: that mutates a locator would then refuse twice - once for its own reason, once for the
#: coverage it incidentally broke - and an unattributed refusal is precisely what this suite
#: exists to make impossible.
_SEEDS_WITH_COVERAGE: frozenset[str] = frozenset({
    "planted-defect-missed", "misclassified-defect"})


# ---------------------------------------------------------------------------------------
# the LIVE probe corpus — the same seeded-defect idea, pointed at a candidate CLI
# ---------------------------------------------------------------------------------------

#: A small governance corpus carrying THREE planted defects, one per category the `[#627]`
#: precedent scores. It lives here, in the tree, rather than as loose files under an audit
#: bundle, for one reason: a measurement whose instrument is not reproducible is an anecdote.
#: Anyone can rebuild it byte-for-byte with `--probe-corpus DIR` and re-run the probe.
#:
#: The planted defects, stated so a scorer is not grading on vibes:
#:   D1 CONTRADICTION   `RULES.md:5` requires `--no-ff`; `HANDBOOK.md:7` calls fast-forward
#:                      the default. Both are normative; they cannot both hold.
#:   D2 UNENFORCED      `RULES.md:8` states a commit-summary rule; `gates.yaml` lists every
#:                      armed hook and none of them reads a summary line.
#:   D3 DUPLICATION     `RULES.md:11` and `HANDBOOK.md:11` carry the same clause verbatim,
#:                      against `HANDBOOK.md:3`'s own claim that nothing is duplicated.
PROBE_CORPUS: dict[str, str] = {
    "RULES.md": (
        "# Rules\n"                                                       # 1
        "\n"                                                              # 2
        "The rules below bind every session in this repository.\n"        # 3
        "\n"                                                              # 4
        "A branch lands on main by `--no-ff` merge, never by fast-forward.\n"   # 5
        "\n"                                                              # 6
        "## Commits\n"                                                    # 7
        "A commit summary is imperative, specific and under 72 characters.\n"  # 8
        "\n"                                                              # 9
        "## Records\n"                                                    # 10
        "An append-only log is never edited in place; corrections append.\n"    # 11
    ),
    "HANDBOOK.md": (
        "# Handbook\n"                                                    # 1
        "\n"                                                              # 2
        "This handbook restates no rule that RULES.md already carries.\n"  # 3
        "\n"                                                              # 4
        "## Landing work\n"                                               # 5
        "Keep history linear.\n"                                          # 6
        "A fast-forward merge is the default way a branch lands on main.\n"     # 7
        "\n"                                                              # 8
        "## Records\n"                                                    # 9
        "Logs are the institutional memory of the project.\n"             # 10
        "An append-only log is never edited in place; corrections append.\n"    # 11
    ),
    "gates.yaml": (
        "# Every hook armed in this repository. Nothing outside this list runs.\n"  # 1
        "hooks:\n"                                                        # 2
        "  - id: block-commit-on-main\n"                                  # 3
        "    stage: pre-commit\n"                                         # 4
        "  - id: backlog-id-on-close\n"                                   # 5
        "    stage: commit-msg\n"                                         # 6
        "  - id: block-ff-push\n"                                         # 7
        "    stage: pre-push\n"                                           # 8
    ),
}

#: The three defects `PROBE_CORPUS` plants, and EVERY locator that legitimately names each.
#: Promoted out of `test_offload_admission.py` so the ground truth a LIVE run is scored
#: against has exactly one home: the sites were previously stated in this module's comments
#: and again in the test, and a drifted copy would move the bar silently -- turning a miss
#: into a hit, which is the failure the whole module exists to make impossible.
PROBE_PLANTED: dict[str, PlantedDefect] = {
    "D1-contradiction": PlantedDefect("contradiction", (
        PlantedSite("RULES.md", 5, "`--no-ff` merge, never by fast-forward"),
        PlantedSite("HANDBOOK.md", 7, "fast-forward merge is the default"))),
    "D2-unenforced": PlantedDefect("unenforced-rule", (
        PlantedSite("RULES.md", 8, "imperative, specific and under 72 characters"),)),
    "D3-duplication": PlantedDefect("duplicated-clause", (
        PlantedSite("RULES.md", 11, "append-only log is never edited in place"),
        PlantedSite("HANDBOOK.md", 11, "append-only log is never edited in place"))),
}

#: `PROBE_PLANTED` in the order `adjudicate(ground_truth=...)` takes it. Two of the three
#: defects are reachable from either file, so a ground truth of single locators would score
#: a correct answer as a miss on which of the pair the candidate happened to cite.
PROBE_GROUND_TRUTH: tuple[PlantedDefect, ...] = tuple(
    defect for _, defect in sorted(PROBE_PLANTED.items()))


#: What a candidate is asked. RETRIEVAL-ONLY and locator-bearing, because those are the two
#: halves of the role intake #75 defines — and because a question with no checkable answer in
#: the corpus is how a fan-out head came to return a fabricated count (`routing-table.yaml`,
#: the `fan_out` scar). The requested shape is the admission record this module adjudicates,
#: so the candidate's own output IS the evidence, with no transcription step in between.
PROBE_QUESTION = """\
You are a read-only retrieval seat. Read every file under the directory given to you and
answer ONE question about that corpus and nothing else.

QUESTION: which clauses in this corpus contradict each other, are stated as rules but armed
by no gate, or are duplicated across two files?

Return ONLY a JSON object, no prose around it, in exactly this shape:

{
  "role": "offload",
  "provider": "copilot-enterprise",
  "cli": "copilot",
  "requested_model": "<the model you were asked to run as>",
  "served_model": "<the model that actually answered>",
  "findings": [
    {
      "rank": 1,
      "category": "contradiction | unenforced-rule | duplicated-clause",
      "locator": "<file>:<line>",
      "quote": "<the text at that exact line, copied verbatim>"
    }
  ]
}

Rules for the answer, all of them checked mechanically afterwards:
- `locator` is a path relative to the corpus root plus a 1-based line number.
- `quote` must appear on that exact line. Every locator is re-opened on disk; one that does
  not hold is counted as a fabrication and the whole answer is refused.
- `rank` is 1..N, most significant first, no repeats.
- Return NO verdict, recommendation, or instruction of any kind. Candidates and locators only.
- The shape above is CLOSED. Any field outside it, at either level, refuses the whole answer.
"""


def _reservation_identity(root: Path) -> tuple[int, int] | None:
    """`(st_dev, st_ino)` for `root` ITSELF, following no symlink. `None` if it is gone.

    `lstat` and not `stat`: a symlink dropped in place of the reserved directory resolves
    through `stat` to whatever it points at, which is the one substitution that would let a
    swap read as unchanged.
    """
    try:
        info = os.lstat(root)
    except OSError:
        return None
    return (info.st_dev, info.st_ino)


def write_probe_corpus(root: Path) -> Path:
    """Materialise `PROBE_CORPUS` at `root`, which must NOT already exist. Returns `root`.

    `RULES.md`, `HANDBOOK.md` and `gates.yaml` are ordinary enough filenames that a real
    checkout holds all three, so `--probe-corpus .` would destroy tracked governance files
    without asking. There is no overwrite path, not even behind a flag: core invariant #3 is
    never overwrite without asking, and git making it recoverable is not a defence for a
    command that writes without looking.

    TWO GUARANTEES ARE ABSOLUTE, and the KERNEL enforces both rather than this module
    checking them -- a check is two operations wherever the guarantee needs one:

    - NOTHING IS EVER OVERWRITTEN. Every file is built in a private staging directory under
      `open(..., "x")` and published with `os.link`, which REFUSES an existing name.
    - NOTHING OUTSIDE STAGING IS EVER DELETED. The failure path removes staging -- ours
      alone, unpredictably named -- and then calls `rmdir` on the reservation, which the
      kernel refuses on a non-empty directory, and only while it is still ours.

    THE THIRD PROPERTY CANNOT BE GUARANTEED, SO IT IS MEASURED INSTEAD. POSIX has no atomic
    create-and-hold for a directory -- no `mkdiropenat` -- so between `root.mkdir()`
    reserving a name and this function using it there is always a gap, and a racer may take
    the name back and put their own directory, or a symlink, there. Seven review passes each
    closed one interleaving of that gap and each left a narrower one; the eighth answer is
    that PREVENTION IS NOT AVAILABLE AT THIS LAYER.

    Z-G4 is the rule for that case -- a gate that cannot compute its ground truth REPORTS
    the gap, it does not pass -- so the reservation's `(st_dev, st_ino)` is captured at
    creation and re-read at the end. If the name no longer resolves to the directory this
    call made, the run REFUSES and says so, naming what was written where. Because the two
    guarantees above already hold, a detected swap is a reportable event and never a
    data-loss one: the racer's files are neither replaced nor removed.

    What remains, stated rather than papered over: detection is not prevention. A swap that
    happens and is reported still wrote three files into a directory this call does not own.
    They are named in the error so the operator can remove them, and this function does not,
    because unlinking through a name whose identity it no longer holds is the exact defect
    the rest of this docstring exists to remove.
    """
    root = Path(root)
    try:
        root.mkdir(parents=True)
    except FileExistsError:
        raise FileExistsError(
            f"refusing to write the probe corpus to {root}: it already exists. Give a "
            f"destination that does not exist -- this command creates it.") from None
    reservation = _reservation_identity(root)

    staging = Path(tempfile.mkdtemp(prefix=".probe-corpus-", dir=root.parent))
    published: list[str] = []
    try:
        for rel, text in PROBE_CORPUS.items():
            target = staging / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            with open(target, "x", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
        for rel in PROBE_CORPUS:
            os.link(staging / rel, root / rel)   # refuses an existing name; never replaces
            published.append(rel)
        shutil.rmtree(staging, ignore_errors=True)
    except OSError as exc:
        shutil.rmtree(staging, ignore_errors=True)
        if _reservation_identity(root) == reservation:
            try:
                root.rmdir()                      # refused by the kernel if anything is there
            except OSError:
                pass
        left = (f"; {len(published)} file(s) already published at {root} were LEFT rather "
                f"than unlinked by a path this call can no longer prove it owns"
                if published else
                "; the empty destination this command created was removed if it was still "
                "empty and still ours, and nothing else was touched")
        raise OSError(
            f"could not write the probe corpus to {root} ({exc}){left}") from None

    if _reservation_identity(root) != reservation:
        raise OSError(
            f"the destination {root} was REPLACED while the probe corpus was being "
            f"published: the name no longer resolves to the directory this command "
            f"created. {len(published)} file(s) -- {', '.join(published)} -- were written "
            f"through that name and are NOT removed here, because this command can no "
            f"longer prove it owns the path they are under. Nothing was overwritten and "
            f"nothing was deleted; inspect {root} before re-running.")
    return root


@dataclass(frozen=True)
class SeededCase:
    """One seeded defect, ready to adjudicate, with the coverage bar it is scored under."""

    code: str
    rationale: str
    record: dict[str, Any]
    ground_truth: tuple[PlantedDefect, ...] = ()


def write_suite_corpus(root: Path) -> Path:
    """Write the suite's corpus and its registry under `root`; return the registry path."""
    root = Path(root)
    for rel, text in _SUITE_CORPUS.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")
    registry = root / "provider-registry.yaml"
    registry.write_text(_SUITE_REGISTRY, encoding="utf-8", newline="\n")
    return registry


def build_seeded_suite() -> list[SeededCase]:
    """The seeded cases, in `REFUSAL_CODES` order."""
    return [SeededCase(code, SEEDED_DEFECTS[code][0], _mutate(SEEDED_DEFECTS[code][1]),
                       SUITE_GROUND_TRUTH if code in _SEEDS_WITH_COVERAGE else ())
            for code in REFUSAL_CODES]


def run_seeded_suite(root: Path) -> list[tuple[SeededCase, Verdict]]:
    """Write the corpus under `root`, adjudicate every seeded case, return the verdicts.

    Re-MEASURED, never asserted. `N` is what this function counts on the day it runs, which is
    the difference between a gate that refuses twelve defects and a doc that says it does.
    """
    registry = write_suite_corpus(root)
    return [(case, adjudicate(case.record, root, registry, case.ground_truth))
            for case in build_seeded_suite()]


def control_verdict(root: Path) -> Verdict:
    """Adjudicate the POSITIVE CONTROL against the suite corpus."""
    registry = write_suite_corpus(root)
    return adjudicate(admissible_record(), root, registry, SUITE_GROUND_TRUTH)


# ---------------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------------

@dataclass(frozen=True)
class SeededReport:
    """The seeded-suite measurement, ATTRIBUTED rather than merely counted.

    The headline number is `len(attributed)` -- the cases refused FOR THEIR OWN CODE --
    deliberately not "how many refused". Under a bare refusal count, a shared upstream
    regression that made all sixteen cases refuse for one reason belonging to none of them
    would score identically to a healthy gate, and the run would exit 0. That is the
    instrument-layer failure class the architecture red-team named: the gate is right, the
    reader is wrong, repeatedly. This module's own headline is produced here, so a counter
    that cannot tell those two runs apart is not evidence about the gate at all.
    """

    total: int
    attributed: tuple[str, ...]
    unattributed: tuple[tuple[str, tuple[str, ...]], ...]
    accepted: tuple[str, ...]
    control: Verdict
    lines: tuple[str, ...]

    @property
    def sound(self) -> bool:
        """Every case refused for its own code, AND the positive control was ADMITTED.

        Both legs, because either alone is satisfiable by a broken gate: "refuses
        everything" clears the first half of a bare count, and sixteen correct refusals mean
        nothing once the control no longer clears the gate they are measured against.
        """
        return len(self.attributed) == self.total and self.control.admitted

    def refusal_lines(self) -> list[str]:
        """Why the run is unsound, one line per cause. Empty when it is sound."""
        out: list[str] = []
        for code in self.accepted:
            out.append(f"REFUSING THE RUN: seeded defect {code!r} was ACCEPTED")
        for code, got in self.unattributed:
            seen = ", ".join(got) or "no code"
            out.append(f"REFUSING THE RUN: seeded defect {code!r} refused for {seen} "
                       f"-- not its own reason, so the refusal is unattributed")
        if not self.control.admitted:
            out.append(f"REFUSING THE RUN: the POSITIVE CONTROL was refused "
                       f"-- {self.control.detail}")
        return out


def seeded_report(root: Path) -> SeededReport:
    """Adjudicate the seeded suite plus its positive control under `root`.

    Re-MEASURED on the day it runs. The three outcome buckets are kept apart rather than
    summed, because ACCEPTED, refused-for-the-wrong-reason and refused-for-its-own-reason
    are three different states of the gate and only the last one is a pass.
    """
    lines: list[str] = []
    attributed: list[str] = []
    unattributed: list[tuple[str, tuple[str, ...]]] = []
    accepted: list[str] = []

    for case, verdict in run_seeded_suite(root):
        if verdict.admitted:
            accepted.append(case.code)
            mark = "ACCEPTED"
        elif verdict.codes == (case.code,):
            attributed.append(case.code)
            mark = "refused"
        else:
            unattributed.append((case.code, verdict.codes))
            mark = f"refused (unattributed: {', '.join(verdict.codes) or 'no code'})"
        lines.append(f"  [{mark}] {case.code} — {case.rationale}")

    control = control_verdict(root)
    lines.append(f"  [control] admissible record -> "
                 f"{'ADMITTED' if control.admitted else 'REFUSED: ' + control.detail}")
    # The denominator is the SPEC's code count, not the number of cases that happened to
    # run: a suite that silently dropped a case would otherwise still print N/N.
    return SeededReport(
        total=len(REFUSAL_CODES),
        attributed=tuple(attributed),
        unattributed=tuple(unattributed),
        accepted=tuple(accepted),
        control=control,
        lines=tuple(lines),
    )


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--record", "record_path", type=click.Path(path_type=Path),
              help="the admission record to adjudicate (YAML or JSON).")
@click.option("--corpus", "corpus_root", type=click.Path(path_type=Path), default=".",
              show_default=True,
              help="the corpus root the record's locators are relative to.")
@click.option("--registry", "registry_path", type=click.Path(path_type=Path), default=None,
              help="provider registry to adjudicate against "
                   "(default: this repo's ecosystem/provider-registry.yaml).")
@click.option("--ground-truth", "ground_truth_name",
              type=click.Choice(["probe", "none"]), default=None,
              help="which corpus GROUND TRUTH to score coverage against. REQUIRED with "
                   "--record: `probe` scores the record against the defects PROBE_CORPUS "
                   "plants; `none` declares on the record that coverage was not scored.")
@click.option("--seeded-defects", "seeded", is_flag=True,
              help="re-measure the seeded-defect suite and print how many are REFUSED.")
@click.option("--probe-corpus", "probe_root", type=click.Path(path_type=Path), default=None,
              help="materialise the LIVE probe corpus in DIR and print the probe question.")
@click.option("--json", "as_json", is_flag=True, help="emit the verdict as JSON.")
def cli(record_path: Path | None, corpus_root: Path, registry_path: Path | None,
        ground_truth_name: str | None, seeded: bool, probe_root: Path | None,
        as_json: bool) -> None:
    """Adjudicate an `offload` admission record, or re-measure the seeded-defect suite.

    Exit code follows the VERDICT, not the transport: 0 only on ADMITTED (or on a seeded run
    in which every case was refused FOR ITS OWN CODE and the positive control was ADMITTED),
    1 on a refusal, 2 when there was nothing to adjudicate, no ground truth was declared, or
    the command refused to act.
    A gap that exited 0 would read as a pass to anything shelling out to this command.
    """
    if seeded:
        with tempfile.TemporaryDirectory() as tmp:
            report = seeded_report(Path(tmp))
        click.echo(f"seeded-defect cases REFUSED FOR THEIR OWN CODE by the {ROLE} "
                   f"admission gate: {len(report.attributed)}/{report.total}")
        for line in report.lines:
            click.echo(line)
        for line in report.refusal_lines():
            click.echo(line)
        raise SystemExit(0 if report.sound else 1)

    if probe_root is not None:
        try:
            written = write_probe_corpus(probe_root)
        except OSError as exc:          # FileExistsError included -- it is an OSError
            click.echo(f"NOT WRITTEN - {exc}")
            raise SystemExit(2) from None
        click.echo(f"probe corpus written to {written}")
        click.echo(PROBE_QUESTION)
        raise SystemExit(0)

    if record_path is None:
        click.echo(
            f"NOT ADMITTED — no admission record on file for role {ROLE!r}. "
            f"A gate that cannot compute its ground truth reports the gap; it does not "
            f"pass (Z-G4). Pass --record, or --seeded-defects to measure the gate itself.")
        raise SystemExit(2)

    if ground_truth_name is None:
        click.echo(
            "NOT ADMITTED — no ground truth declared. Coverage is the half of an answer a "
            "locator cannot prove, so this command will not admit a record without "
            "--ground-truth {probe|none}. Declaring `none` is allowed and is recorded in "
            "the verdict; inheriting it by default is not (Z-G4).")
        raise SystemExit(2)
    ground_truth = PROBE_GROUND_TRUTH if ground_truth_name == "probe" else ()

    try:
        record = load_record(record_path)
        verdict = adjudicate(record, corpus_root, registry_path, ground_truth)
    except AdmissionError as exc:
        click.echo(f"NOT ADMITTED — {exc}")
        raise SystemExit(2) from None

    if as_json:
        click.echo(json.dumps({
            "admitted": verdict.admitted,
            "findings_seen": verdict.findings_seen,
            "locators_verified": verdict.locators_verified,
            "refusals": [{"code": r.code, "detail": r.detail} for r in verdict.refusals],
        }, indent=2))
    else:
        click.echo(verdict.detail)
    raise SystemExit(0 if verdict.admitted else 1)


if __name__ == "__main__":
    cli()
