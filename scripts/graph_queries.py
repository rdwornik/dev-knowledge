#!/usr/bin/env python
"""graph_queries.py -- the three commit-tier REFUSALS over the persisted FPG-1 store ([#664]).

WHAT THIS IS. `[#664]`'s acceptance clause, in code: *"three queries, each a REFUSAL at commit
tier"*. `orphan_census`, `task_coverage` and `process_list`, each wired to its own pre-commit
hook, each exiting non-zero on the property it refuses. A query that reports without refusing
discharges nothing -- the row says so and the frozen contract repeats it.

ORGANS ARE VIEWS (ADR-118 §2). Every predicate here is a SELECT over
`scripts/graph_store.py`. Nothing in this module walks the tree for an edge, parses a config,
or computes a relation of its own; where a relation was missing it was added to FPG-1
(`triggers`, `imports`, `implements`) rather than computed here. That is intake #86's
acceptance criterion 5 -- *"a test asserts the organ imports the graph rather than walking the
tree"* -- and it is the whole point of the landing: a private computation here would defeat
the thing it is meant to prove.

STDLIB ONLY ON THE READ PATH, and it is deliberate. This module imports `graph_store`, which
defers its `file_purpose_graph` import into `rebuild()`. So three hooks per commit pay for
sqlite and nothing else; `rustworkx` is loaded once, by the rebuild hook, and never by a
reader.

THE ONE THING THIS MODULE HOLDS THAT IS NOT A QUERY -- `ORPHAN_DISPOSITIONS`, and it is
declared as an exception rather than left to be noticed. It is a curated register with a
reason and an owner per row: the "kept-as-manifest with a reason" form, and the same shape
`ecosystem/disposition-register.yaml` already uses for known WARNs. It lives HERE rather than
there for exactly one reason, which is footprint: `[#664]`'s frozen contract gives this lane
`scripts/`, `tests/`, `.pre-commit-config.yaml` and one audit, and `ecosystem/` is not its to
write. **Relocating it to `ecosystem/disposition-register.yaml` is an owed follow-up**, named
in this lane's artifact rather than left as a surprise.

NO LLM ANYWHERE IN A QUERY. `[#664]`'s anti-patterns list it first, ADR-118 §4 rules it
("no gate calls an LLM on its hot path"), and every predicate below is mechanical and seeded
by a fixture.

Usage:
    python scripts/graph_queries.py orphan-census  [--repo-root .] [--db PATH]
    python scripts/graph_queries.py task-coverage  [--repo-root .] [--staged PATH ...]
    python scripts/graph_queries.py process-list   [--repo-root .] [--render]
"""

from __future__ import annotations

import argparse
import logging
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:  # importable both as a module and as a script
    sys.path.insert(0, str(_SCRIPTS))

import graph_store as gs  # noqa: E402

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("graph-queries")

#: Reachability over these two kinds is what "triggered" means: a wiring surface fires a
#: process directly (`triggers`), and a fired process reaches what it calls (`imports`).
TRIGGER_KINDS = ("triggers", "imports")
#: The one kind `task_coverage` reads. Both of its directions are `implements` edges -- the
#: row naming the file and the file naming the row -- so the query asks ONE question.
COVERAGE_KINDS = ("implements",)


@dataclass(frozen=True)
class Finding:
    """One refusal. `subject` is the path; `evidence` is why, in the operator's terms."""
    subject: str
    evidence: str


@dataclass(frozen=True)
class Disposition:
    """A recorded reason a process may have no trigger, and who owns the decision.

    A DISPOSITION IS NOT AN EXEMPTION. It records that the absence of a trigger has been
    LOOKED AT and ruled, and it names who can change that. ADR-75's decoration rule is what
    keeps it honest: a disposition naming a file that is gone is surfaced by
    `stale_dispositions()` and pinned by a test, so the register cannot rot into paper
    suppressions.
    """
    reason: str
    owner: str


@dataclass(frozen=True)
class ProcessRow:
    """One row of the traversal that answers "all processes"."""
    path: str
    process_class: str
    triggered: bool
    trigger: str
    disposition: Disposition | None = None


# --------------------------------------------------------------- the disposition register
#
# THE 32-vs-20 GAP, RULED RATHER THAN ROUNDED -- `[#664]`'s clause 4, and the frozen
# contract's warning that *"32 -> 0 against a 20-item predicate is unreachable by
# construction"*.
#
# THE RULING: widen the node class to EVERY IN-TREE PROCESS FILE, and name what a corpus
# graph of this repo cannot see. `docs/audits/2026-09-08-technical-process-trigger-census.md`
# counted 32 orphans across three populations -- 20 script-class, 3 L0 hooks, 9 commands and
# skills. Of those, 6 are on the OPERATOR'S DISK under `~/.claude/` (three
# `block-onedrive.SUPERSEDED*.ps1` copies, `~/.claude/commands/codex-review.md`, two
# `~/.claude/skills/gotchas/` files). They are not tracked by this repo, so they are not nodes
# in a graph of this repo's corpus -- unrepresentable, not overlooked. The census already
# rules their disposition operator-owned (*"a file deletion in an exclusion-adjacent
# directory and is the operator's call, not a lane's"*), and ADR-54 makes `~/.claude/` a home
# this repo authors nothing in.
#
# Widening was chosen over "give the other 12 their own queries" because that 12 splits 6/6
# across in-repo and out-of-tree: a second query would still not reach the out-of-tree half,
# so it would buy a surface without buying an answer.
#
# WHAT THE WIDENED CLASS MEASURES, live: 38 orphans, not the census's 26 in-repo. The
# difference is measured, not hand-waved, and every row of it is below:
#   * +11 commands and +2 skills. The census reports 9 command/skill orphans and rules the
#     other 8 ON-DEMAND-BY-OPERATOR against a closed list of seven acts. That list is a
#     RULING, not a computation -- nothing in the tree fires a command -- so the mechanism
#     finds every in-repo command and skill, and the eight the census ruled on-demand are
#     dispositioned here with the act each maps to. The classification is preserved; what
#     changes is that it is now written down where a gate can read it.
#   * +2 script-class arrivals since the census's 2026-09-08 cut: `gen_ledger.py` (landed by
#     lane V-000 on 2026-09-09) and the derived-copy pair below.
#   * -1: `scripts/file_purpose_graph.py` is NO LONGER AN ORPHAN. It is the row's own
#     headline landing -- FPG-1 acquired a trigger, the `graph-rebuild` pre-commit hook, and
#     drops off this list by being wired rather than by being dispositioned.
#
# Every entry carries a reason and an owner, both asserted by tests.

_LANE_BUILT = ("lane-built and never adopted -- the process-trigger census's DECLARE §5 "
               "finding in mechanism form: lanes build organs and nothing adopts them "
               "afterwards. Retirement-or-wiring is V+1's list, not this lane's act")

ORPHAN_DISPOSITIONS: dict[str, Disposition] = {
    # ---- population A: scripts, lane-built and never wired (the census's own class) ----
    "scripts/cost_usage_telemetry.py": Disposition(
        reason=f"{_LANE_BUILT}; only call site is LANE-f-6-observability-otel.md:27",
        owner="V+1 retirement-or-wiring list"),
    "scripts/gen_north_star.py": Disposition(
        reason=f"{_LANE_BUILT}; only call site is batch-e CUT.md:40",
        owner="V+1 retirement-or-wiring list"),
    "scripts/gen_trend_dashboard.py": Disposition(
        reason=f"{_LANE_BUILT}; only call site is LANE-n-14-trends-burndown.md:27",
        owner="V+1 retirement-or-wiring list"),
    "scripts/logs_retention.py": Disposition(
        reason=f"{_LANE_BUILT}; the DECLARE §3 names run_retention() at 0 callers and the "
               f"census confirms it at module level too",
        owner="V+1 retirement-or-wiring list"),
    "scripts/nopack_sandbox.py": Disposition(
        reason=f"{_LANE_BUILT}; only call site is LANE-e-5-vision-relocation.md:46",
        owner="V+1 retirement-or-wiring list"),
    "scripts/trace_writer.py": Disposition(
        reason=f"{_LANE_BUILT}; only call site is LANE-t-000-trace-scorecard.md:47",
        owner="V+1 retirement-or-wiring list"),
    "scripts/window_metrics.py": Disposition(
        reason=f"{_LANE_BUILT}; only call site is LANE-r-000-zc-candidates.md:39",
        owner="V+1 retirement-or-wiring list"),
    "scripts/failed_set.py": Disposition(
        reason="reachable only from the untriggered window_metrics.py:359 -- an orphan by "
               "inheritance, so it is dispositioned WITH its caller and not before it",
        owner="V+1 retirement-or-wiring list"),
    "scripts/desired_state_report.py": Disposition(
        reason="named in ARCHITECTURE.md:504 prose only -- documented, never wired. Prose is "
               "not a trigger, which is the census's own method line",
        owner="V+1 retirement-or-wiring list"),
    "scripts/desired_state_loader.py": Disposition(
        reason="reachable only from the untriggered desired_state_report.py:50 -- an orphan "
               "by inheritance, dispositioned with its caller",
        owner="V+1 retirement-or-wiring list"),
    "scripts/boundary_headers.py": Disposition(
        reason="named in ARCHITECTURE.md:480 prose only -- documented, never wired",
        owner="V+1 retirement-or-wiring list"),
    "scripts/boundary_report.py": Disposition(
        reason="reachable only from the untriggered boundary_headers.py:58 -- an orphan by "
               "inheritance, dispositioned with its caller",
        owner="V+1 retirement-or-wiring list"),
    "scripts/gen_ledger.py": Disposition(
        reason="ARRIVED AFTER THE CENSUS -- landed 2026-09-09 by lane V-000 and therefore "
               "absent from its 32. Recorded as a NEW orphan rather than folded into the "
               "old count: the census is a dated measurement, not a live roster",
        owner="V+1 retirement-or-wiring list"),
    # ---- population A: tests are not triggers ----
    "scripts/archive_row_body.py": Disposition(
        reason="referenced only by tests/test_archive_row_body.py -- a test proves a module "
               "works and schedules nothing, so it is not a trigger. [#664]'s row names this "
               "module's trigger ride as an edge of this arc, not a separate row",
        owner="V+1 retirement-or-wiring list"),
    "scripts/cloud_provisioning.py": Disposition(
        reason="referenced only by tests/test_cloud_provisioning.py:24 -- a test is not a "
               "trigger",
        owner="V+1 retirement-or-wiring list"),
    "scripts/probe_child_backlogs.py": Disposition(
        reason="referenced only by tests/test_probe_child_backlogs.py -- a test is not a "
               "trigger",
        owner="V+1 retirement-or-wiring list"),
    "scripts/seed_runbook.py": Disposition(
        reason="referenced only by tests/test_seed_runbook.py -- a test is not a trigger",
        owner="V+1 retirement-or-wiring list"),
    "scripts/validate_onboarding_rulings.py": Disposition(
        reason="referenced only by tests/test_onboarding_rulings.py:19 -- a test is not a "
               "trigger",
        owner="V+1 retirement-or-wiring list"),
    # ---- population A: orphan BY DESIGN, and wiring it would RED a test ----
    "scripts/export_backlog_view.py": Disposition(
        reason="ORPHAN BY DESIGN: tests/test_export_backlog_view.py::test_no_gate_hook_or_"
               "script_reads_the_export ASSERTS that nothing reads it ([#563] one-way view "
               "layer). Wiring it would RED that test, so the disposition is a ruling rather "
               "than a defect and this row must never be 'fixed'",
        owner="[#563] -- settled; reopening needs a ruling, not a lane"),
    "scripts/setup-fleet-scheduler.ps1": Disposition(
        reason="one-shot INSTALLER. The task it registers is live (Get-ScheduledTask -> "
               "fleet-baseline, State=Ready), so the PROCESS is triggered; an installer is "
               "not a recurring process and never was",
        owner="operator -- machine setup, not repo wiring"),
    # ---- population A: derived-copy SOURCES, which fire as their copies ----
    "scripts/propose_closures.py": Disposition(
        reason="DERIVED-COPY SOURCE. The armed process is the plugin copy "
               "plugins/tier1-lifecycle/scripts/propose_closures.py, which the plugin Stop "
               "hook fires; this is the hub original it is generated from, registered in "
               "ecosystem/derived-copies.yaml. A source is not an orphan, it is upstream -- "
               "and the pair is exactly why the wiring loader resolves a plugin manifest's "
               "path against the PLUGIN root before the repo root",
        owner="ecosystem/derived-copies.yaml -- the registry that owns the pair"),
    "scripts/review_closures.py": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = ratification. Invoked by /review-closures "
               "(plugins/tier1-lifecycle/commands/review-closures.md:20). Also the "
               "derived-copy source of the plugin copy below",
        owner="operator -- one of the census's seven acts"),
    "plugins/tier1-lifecycle/scripts/review_closures.py": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = ratification. The plugin copy invoked by "
               "/review-closures; no event fires it and none should",
        owner="operator -- one of the census's seven acts"),
    # ---- population A: on-demand, mapped to one of the seven acts ----
    "scripts/worktree_seed.py": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = GO. Invoked by /lane-boot "
               "(.claude/commands/lane-boot.md:124)",
        owner="operator -- one of the census's seven acts"),
    "scripts/worktree_import_proof.py": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = GO. Invoked by /lane-boot "
               "(.claude/commands/lane-boot.md:174)",
        owner="operator -- one of the census's seven acts"),
    "scripts/single_flight.py": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = GO. Invoked by /lane-boot "
               "(.claude/commands/lane-boot.md:71) and /lane-integrate:132. A FINDING "
               "AGAINST THE CENSUS, recorded rather than quietly absorbed: it is absent "
               "from the census's 20 and this query finds it, which is exactly intake #86's "
               "acceptance criterion 2 -- 'every orphan the query finds that the sweep "
               "missed is recorded as a finding against the sweep', reported and never "
               "silently reconciled",
        owner="operator -- one of the census's seven acts"),
    # ---- population C: commands. NOTHING FIRES A COMMAND, and that is the finding ----
    ".claude/commands/boot-session.md": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = sitting. No event fires a command; the census "
               "rules the seven acts a closed list and this is one of them",
        owner="operator -- one of the census's seven acts"),
    ".claude/commands/handoff.md": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = seat release",
        owner="operator -- one of the census's seven acts"),
    ".claude/commands/handoff-verify.md": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = seat release",
        owner="operator -- one of the census's seven acts"),
    ".claude/commands/lane-boot.md": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = GO",
        owner="operator -- one of the census's seven acts"),
    ".claude/commands/lane-integrate.md": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = GO",
        owner="operator -- one of the census's seven acts"),
    "plugins/tier1-lifecycle/commands/review-closures.md": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = ratification",
        owner="operator -- one of the census's seven acts"),
    "plugins/tier1-lifecycle/commands/ship.md": Disposition(
        reason="ON-DEMAND-BY-OPERATOR, act = destructive acts",
        owner="operator -- one of the census's seven acts"),
    ".claude/commands/changelog-review.md": Disposition(
        reason="ORPHAN in the census's own terms: a PUSH trigger only. A SessionStart "
               "sentinel NUDGES it, and a nudge is not a trigger -- the distinction the "
               "census draws deliberately and this register preserves",
        owner="V+1 retirement-or-wiring list"),
    ".claude/commands/override.md": Disposition(
        reason="RETIRED by the ADR-85 amendment 2026-08-03 §A2 -- discharges no gate and "
               "arms only a local telemetry token. The file IS the retirement notice, which "
               "is why it is kept rather than deleted (2026-09-07 census-templates ruling)",
        owner="ADR-85 amendment -- settled"),
    ".claude/commands/preflight.md": Disposition(
        reason="its own frontmatter says 'wired into no gate' -- a self-declared orphan, and "
               "an adoption-first read-only helper is a legitimate shape for one",
        owner="V+1 retirement-or-wiring list"),
    ".claude/commands/save.md": Disposition(
        reason="convenience wrapper, not one of the seven acts. INVISIBLE TO THE CENSUS'S "
               "OWN MECHANISM until this lane made every process file a node -- nothing "
               "named it, so it had no vertex to be counted at",
        owner="V+1 retirement-or-wiring list"),
    # ---- population C: skills. A MANDATE IN PROSE IS NOT A TRIGGER ----
    ".claude/skills/verify/SKILL.md": Disposition(
        reason="no event fires a skill; a skill is read when a seat chooses to read it. The "
               "census's finding, not a filing error -- and [#664]'s anti-pattern list rules "
               "the repair: a skill's mandate becomes a HOOK, never a graph row",
        owner="V+1 retirement-or-wiring list"),
    ".claude/skills/check-against-spec/SKILL.md": Disposition(
        reason="no event fires a skill. Same class as `verify` above; the mandate lives in "
               "prose and prose is carried by seats' diligence, which is the missing spine "
               "the DECLARE §5 names",
        owner="V+1 retirement-or-wiring list"),
}


# ---------------------------------------------------------------------- query 1: the census


def orphan_census(repo_root: Path | str, store: gs.GraphStore,
                  dispositions: dict[str, Disposition] | None = None) -> list[Finding]:
    """REFUSE on a process node no wiring surface reaches, transitively, and nothing rules.

    intake #86's organ, at commit tier. The predicate is a REACHABILITY query over the store
    -- in-degree alone would be wrong, because a module reached only through three imports is
    triggered just as truly as one a hook names directly, and the census closes its call
    graph for exactly that reason.
    """
    del repo_root  # the store answers; the tree is not read here, and that is the point
    register = ORPHAN_DISPOSITIONS if dispositions is None else dispositions
    reached = store.reachable(store.roots(), TRIGGER_KINDS)
    findings: list[Finding] = []
    for node in store.processes():
        if node.key in reached or node.path in register:
            continue
        findings.append(Finding(
            subject=node.path,
            evidence=(f"{node.process_class} reached by no wiring surface over "
                      f"{'/'.join(TRIGGER_KINDS)}. Wire it, retire it, or add a disposition "
                      f"with a reason and an owner to ORPHAN_DISPOSITIONS.")))
    return findings


def stale_dispositions(repo_root: Path | str,
                       dispositions: dict[str, Disposition] | None = None) -> list[str]:
    """Dispositioned paths that are no longer on disk -- ADR-75's decoration rule.

    Surfaced, never blocking: a register allowed to rot into paper suppressions is worse than
    no register, and a stale row is a fact about the register rather than about the commit.
    """
    root = Path(repo_root)
    register = ORPHAN_DISPOSITIONS if dispositions is None else dispositions
    return sorted(path for path in register if not (root / path).exists())


# -------------------------------------------------------------------- query 2: task coverage

#: Surfaces that cannot carry an ownership claim, each with the reason it cannot. This is a
#: SHORT and REASONED list, not a convenience escape: every entry is either generated (its
#: content is not authored, so a row citation in it would be a generator's, not a claim) or
#: is a record of every row at once (a journal entry names every row a session touched, so
#: reading it as ownership would make everything covered).
COVERAGE_EXEMPT: dict[str, str] = {
    "JOURNAL.md": "names every row a session touched -- ownership read from it is vacuous",
    "BACKLOG.md": "generated VIEW of tasks/; never read for an edge (FPG-1 input 4's rule)",
    "tasks/manifest.json": "generated by gen_task_tree.py",
    "ecosystem/organ-index.md": "generated by generate_organ_index.py",
    "ecosystem/doc-counts.md": "generated by gen_doc_counts.py",
    "docs/audits/README.md": "generated by gen_audit_index.py",
    "docs/intake/README.md": "generated by gen_intake_tree.py",
    "docs/intake/manifest.json": "generated by gen_intake_tree.py",
    ".claude/methodology-roster.md": "generated by gen_methodology_roster.py",
    "uv.lock": "generated by uv; ADR-106 owns its lifecycle",
}
#: Directory prefixes under the same rule.
COVERAGE_EXEMPT_PREFIXES: tuple[str, ...] = (".claude/generated/",)


def staged_paths(repo_root: Path | str) -> list[str]:
    """The files this commit is about to write -- `git diff --cached`, ACMR.

    THE ONE PLACE THIS MODULE READS COMMIT STATE RATHER THAN THE GRAPH, and it is named
    rather than hidden. DECLARE-REVIEWS §A.1 correction 2 rules that a two-tree gate cannot
    be a view: the staged set is commit-time state and stays a gate; the `implements`
    relation is corpus structure and is a query. `task_coverage` is the JOIN of the two, and
    calling it a pure view would be the mis-filing that correction exists to prevent.
    """
    try:
        out = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
            cwd=repo_root, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):  # pragma: no cover -- no git on PATH
        return []
    if out.returncode != 0:
        return []
    return [line.strip() for line in out.stdout.splitlines() if line.strip()]


def _merge_in_progress(repo_root: Path | str) -> bool:
    """`MERGE_HEAD` present in the RESOLVED git dir -- a merge is being committed.

    Resolved, never `repo_root / ".git" / "MERGE_HEAD"`: in a worktree `.git` is a file and
    the naive spelling answers False for every merge a lane ever makes, which is the one
    place this carve-out has to work.
    """
    git_dir = gs._resolved_git_dir(Path(repo_root))
    return bool(git_dir and (git_dir / "MERGE_HEAD").exists())


def _worktree_skew(repo_root: Path | str) -> set[str]:
    """Files whose WORKING-TREE bytes are not what this commit will write.

    Unstaged modifications to tracked files, plus untracked files. Empty when git cannot
    answer, which is the same posture `staged_paths` takes: with no git there is no staged
    set either, so the gate has nothing to be lenient about.
    """
    skew: set[str] = set()
    for args in (["git", "diff", "--name-only", "--diff-filter=ACMR"],
                 ["git", "ls-files", "--others", "--exclude-standard"]):
        try:
            out = subprocess.run(args, cwd=repo_root, capture_output=True, text=True,
                                 timeout=60)
        except (OSError, subprocess.SubprocessError):  # pragma: no cover -- no git on PATH
            return set()
        if out.returncode != 0:
            return set()
        skew.update(line.strip() for line in out.stdout.splitlines() if line.strip())
    return skew


def _evidence_paths(store: gs.GraphStore, relpath: str, edges: list[dict]) -> set[str]:
    """Every file the coverage claim for `relpath` actually rests on.

    Both legs, because coverage holds in both directions: the file itself (it may name the
    row) and each row that names it. A claim is only as staged as the file carrying it.
    """
    paths = {relpath}
    for edge in edges:
        node = store.node(edge["src"])
        if node and node.path:
            paths.add(node.path)
    return paths


def _exempt(relpath: str) -> str | None:
    if relpath in COVERAGE_EXEMPT:
        return COVERAGE_EXEMPT[relpath]
    for prefix in COVERAGE_EXEMPT_PREFIXES:
        if relpath.startswith(prefix):
            return f"under {prefix} -- generated"
    return None


def task_coverage(repo_root: Path | str, store: gs.GraphStore,
                  staged: list[str] | None = None) -> list[Finding]:
    """REFUSE on a staged file with no inbound `implements` edge from an OPEN row.

    "nic bez taska" as a mechanism, AT OPEN and not only at CLOSE -- `[#664]`'s own framing.
    Coverage holds if the row names the file OR the file names the row; both are `implements`
    edges, so the query asks one question of the graph rather than two of the tree.

    TWO TREES, AND THE SKEW BETWEEN THEM IS THIS GATE'S ONE REAL HAZARD. The subject set is
    the INDEX (`git diff --cached`); the `implements` relation comes from a graph built off
    the WORKING TREE. Left alone, that gap is a bypass: stage an unclaimed change, leave the
    `[#id]` mention -- or a whole open row -- unstaged or untracked beside it, and the tree
    supplies an edge for a claim the commit does not carry. Terra pre-merge review found it.

    THE FIX REFUSES THE SKEW RATHER THAN REBUILDING THE GRAPH FROM THE INDEX, and the choice
    is a design one rather than a shortcut. The store is a TREE artifact -- one build per
    commit, shared by three queries and every other reader -- so an index-shaped graph would
    be a second graph with a second lifetime, which ADR-118's "one graph" rules out and no
    ruling licenses here. So coverage is accepted only when every file the claim rests on is
    what the commit will actually write. In the hook path this costs nothing: pre-commit
    stashes unstaged changes, so the tracked-unstaged set is empty by the time this runs, and
    the untracked leg is exactly the hole -- a new row that is going to be committed has been
    `git add`ed, so an UNTRACKED row is never legitimate evidence.
    """
    if staged is None and _merge_in_progress(repo_root):
        # A MERGE IS TRANSPORT, NOT AUTHORSHIP, and this carve-out has direct precedent in
        # this repo: `block_commit_on_main` carries exactly one, `MERGE_HEAD present =>
        # allow`, for the same reason. Without it the gate refuses a lane's SYNC MERGE
        # because main's own commits brought files this branch never wrote -- ten of them on
        # the first live merge, all filed on main by other lanes. Refusing them here would
        # ask this lane to claim, or to retire, work it has not assessed.
        return []
    paths = staged_paths(repo_root) if staged is None else staged
    skew = _worktree_skew(repo_root)
    findings: list[Finding] = []
    for relpath in paths:
        if _exempt(relpath):
            continue
        key = store.key_for_path(relpath)
        if key and key.startswith("task:"):
            # A ROW FILE IS ITS OWN CLAIM. `tasks/665-*.md` IS `[#665]`; asking it to be
            # named by an open row is asking it to name itself, and FPG-1 keys it on the
            # row's identity rather than its path precisely because the two are one thing.
            # Found by this gate firing on a real merge, which is where a predicate written
            # from the row's wording meets the tree's actual shape.
            continue
        edges = store.in_edges(key, COVERAGE_KINDS) if key else []
        if edges:
            unstaged = sorted(p for p in _evidence_paths(store, relpath, edges) if p in skew)
            if not unstaged:
                continue
            findings.append(Finding(
                subject=relpath,
                evidence=("the claim covering this file is in the WORKING TREE, not in the "
                          f"commit: {', '.join(unstaged)}. The graph is built from the tree "
                          "and the commit writes the index, so an unstaged or untracked "
                          "claim covers nothing. Stage it.")))
            continue
        findings.append(Finding(
            subject=relpath,
            evidence=("no `implements` edge from an OPEN row. Name this file in the row's "
                      "body, or name the row `[#id]` in this file -- either direction is "
                      "the claim, and one of them is owed before the change lands.")))
    return findings


# --------------------------------------------------------------------- query 3: the process list


#: A process path named in prose. Bounded to the trees that hold executables, for the reason
#: `_SCRIPT_PATH_RE` is bounded in `file_purpose_graph`: a doc path in a sentence is not a
#: process reference and must not be read as a dangling one.
_PROSE_PROCESS_RE = re.compile(r"(?:scripts|plugins)/[A-Za-z0-9_./-]+\.(?:py|ps1)")
#: The surface `ARCHITECTURE.md` Ch2 is rendered from. Rendering it is a DIFFERENT lane --
#: `[#664]`'s frozen contract pins ARCHITECTURE.md prose out of this one -- so this module
#: arms the refusal and PRODUCES the body, and does not rewrite the file.
PROSE_SURFACE = "ARCHITECTURE.md"


def process_list(repo_root: Path | str, store: gs.GraphStore) -> list[ProcessRow]:
    """The traversal that answers "all processes", with WHY each one runs.

    This is the query `[#664]` says the repo did not have: *"so 'list all processes' is
    answered by re-reading the repo."* It is answered here by reading the store.
    """
    del repo_root
    reached = store.reachable(store.roots(), TRIGGER_KINDS)
    rows: list[ProcessRow] = []
    for node in store.processes():
        triggered = node.key in reached
        rows.append(ProcessRow(
            path=node.path,
            process_class=node.process_class,
            triggered=triggered,
            trigger=store.trigger_of(node.key) if triggered else "",
            disposition=ORPHAN_DISPOSITIONS.get(node.path)))
    return rows


def dangling_references(repo_root: Path | str, store: gs.GraphStore) -> list[Finding]:
    """REFUSE on prose naming a process the graph does not hold -- a `dangling_reference`.

    `[#664]`: *"prose naming a process the graph lacks becomes a `dangling_reference`."* The
    graph holds every in-tree process file, so a prose path the graph lacks is a path that
    does not exist -- a stale locator in the document that is supposed to be the structural
    model, which is the worst place in this repo for one.
    """
    root = Path(repo_root)
    surface = root / PROSE_SURFACE
    if not surface.is_file():
        return []
    try:
        text = surface.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):  # pragma: no cover -- unreadable canonical doc
        return []
    findings: list[Finding] = []
    for token in sorted(set(_PROSE_PROCESS_RE.findall(text))):
        if store.key_for_path(token) is None:
            findings.append(Finding(
                subject=token,
                evidence=(f"{PROSE_SURFACE} names this process and the graph does not hold "
                          f"it. Either the path is stale, or the file was removed and the "
                          f"prose was not.")))
    return findings


def render_ch2(rows: list[ProcessRow]) -> str:
    """The Ch2 body, generated from the traversal rather than maintained by hand.

    PRODUCED, NOT LANDED. `[#664]`'s contract pins `ARCHITECTURE.md` prose out of this lane
    ("Ch2 is RENDERED by this lane's mechanism; the hand rewrite is step D of the recovery
    plan and a different lane"), so this returns the text and writes nothing. Flat bullets,
    no column padding -- CLAUDE.md output-formatting.
    """
    lines = ["## Processes -- generated from FPG-1 (`graph_queries.py process-list --render`)",
             ""]
    for klass in ("script", "command", "skill"):
        members = [row for row in rows if row.process_class == klass]
        armed = [row for row in members if row.triggered]
        lines.append(f"### {klass} ({len(armed)} triggered of {len(members)})")
        lines.append("")
        for row in members:
            if row.triggered:
                lines.append(f"- `{row.path}` -- triggered by `{row.trigger}`")
            else:
                reason = row.disposition.reason if row.disposition else "UNDISPOSITIONED"
                owner = row.disposition.owner if row.disposition else "-"
                lines.append(f"- `{row.path}` -- no trigger; {reason} [owner: {owner}]")
        lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------------------------- CLI


def _open(args) -> gs.GraphStore:
    """The store these queries answer from -- ALWAYS through the freshness check.

    EXISTS IS NOT FRESH, and the earlier shape here confused the two: it opened any store
    that was on disk and only built one that was absent. Terra pre-merge review named what
    that costs -- every invocation after a source file changes outside the hook chain
    answers `orphan-census`, `task-coverage` and `process-list` from yesterday's graph, and
    a stale graph does not fail, it just answers wrongly. `ensure` is the whole contract in
    one call: fresh store, rebuild if stale, one rebuilder at a time.

    THE HOOK CHAIN PAYS AN mtime SWEEP PER QUERY FOR THIS, and that is the right trade to
    make: `graph-rebuild` runs first and leaves the store fresh, so the three query hooks
    each pay `is_stale` and none of them rebuilds. Buying that back with an
    `--assume-fresh` flag would reintroduce the hole with a switch on it.
    """
    root = Path(args.repo_root).resolve()
    path = Path(args.db) if args.db else gs.store_path(root)
    return gs.ensure(root, path)


def _report(name: str, findings: list[Finding]) -> int:
    if not findings:
        print(f"{name}: OK")
        return 0
    print(f"{name}: REFUSED -- {len(findings)} finding(s)")
    for finding in findings:
        print(f"  - {finding.subject}")
        print(f"    {finding.evidence}")
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="The three commit-tier refusals over the persisted FPG-1 store.")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo-root", default=".", help="repo to read (default: cwd)")
    common.add_argument("--db", default=None, help="store path (default: under the git dir)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("orphan-census", parents=[common],
                   help="refuse on a process nothing triggers")
    coverage = sub.add_parser("task-coverage", parents=[common],
                              help="refuse on a staged file no OPEN row claims")
    coverage.add_argument("--staged", nargs="*", default=None,
                          help="paths to check (default: git diff --cached)")
    listing = sub.add_parser("process-list", parents=[common],
                             help="every process with its trigger; refuse on a dangling ref")
    listing.add_argument("--render", action="store_true",
                         help="emit the ARCHITECTURE.md Ch2 body (writes nothing)")

    args = parser.parse_args(argv)
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):  # pragma: no cover -- a non-TextIO stream
            pass

    root = Path(args.repo_root).resolve()
    try:
        store = _open(args)
    except gs.StoreUnreadable as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1

    if args.command == "orphan-census":
        stale = stale_dispositions(root)
        if stale:
            # Surfaced, never blocking -- ADR-75's decoration rule. A stale disposition is a
            # fact about the register, and refusing a commit for it would punish the wrong act.
            print("orphan-census: NOTE -- dispositions naming files that are gone: "
                  + ", ".join(stale))
        return _report("orphan-census", orphan_census(root, store))

    if args.command == "task-coverage":
        return _report("task-coverage", task_coverage(root, store, args.staged))

    rows = process_list(root, store)
    if args.render:
        print(render_ch2(rows))
    else:
        armed = sum(1 for row in rows if row.triggered)
        print(f"process-list: {len(rows)} processes, {armed} triggered, "
              f"{len(rows) - armed} not")
    return _report("process-list", dangling_references(root, store))


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
