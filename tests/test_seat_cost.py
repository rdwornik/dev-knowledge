"""The ATTENDED SEAT's own cost line, RED-first (lane `aa-2`, the integrator model split).

Implements `[#751]` — *"cost in money: the transcripts' token figures become tokens and USD per
lane and per model"* — for the one population that row's reader could not reach. `[#751]` built a
LANE reader keyed on a session-store directory; an attended seat has no directory of its own, so
its cost was the part of every batch total that had to be computed by hand.


WHY A SECOND READER OVER THE SAME TRANSCRIPTS. `lane_cost.lane_cost` prices a LANE, and it finds
its transcripts by matching the lane slug against a session-store DIRECTORY name. That works for a
lane because a lane owns a worktree and a worktree is a directory. It does not work — at all — for
an attended seat, and the failure is not a near miss:

    Asking `lane_cost` for the batch-Z integrator seat by its directory returns
    **USD 8,714.37 over 52,822 calls across six models** — the primary checkout's LIFETIME
    total, every session ever run there. The night's real figure was USD 82.53.
    (`docs/audits/2026-09-15-technical-batch-z-close-packet.md` §2, "A correction the
    instrument forced": *"A per-directory tally reported as a per-lane cost would have
    overstated the night by 32x."*)

The integrator, the dispatcher, the filings seat and the handoff seat all run IN the primary
checkout, alongside that checkout's whole history. The store is keyed per DIRECTORY, not per
seat, so the only key that isolates one seat's sitting is its **session id** — and until this
module there was no verb that took one. The USD 82.53 in the close packet was therefore produced
by a method that lived nowhere in this repository, which is why this lane's contract says a
number you inherited is a claim.

WHAT THESE TESTS REFUSE, each with a test whose name says which:

  1. **A seat cost read by directory.** It answers a different question with a plausible number.
  2. **A window that is not recorded.** A session transcript GROWS: the same file priced an hour
     later is a different figure, and it is *supposed* to be. Measured on the batch-Z integrator
     session — USD 82.53 at 06:51:12Z, USD 89.88 at the end of the file. So a seat figure without
     its window is not reproducible, and a PAIRED comparison against one is worthless. The window
     rides the row.
  3. **A split seat reported as one number.** The whole point of routing PLAN and EXECUTE to
     different models is that the two halves become separately visible. A seat row that summed
     them would report the split as working exactly when it had not happened.
  4. **A missing seat row read as a cheap batch.** `lane_cost` already refuses this for a lane;
     an attended seat was the one population the refusal could not reach, because no verb could
     write its row.
"""
from __future__ import annotations

import json

import pytest

import lane_cost as lc


# --- fixtures ----------------------------------------------------------------------------

_REGISTRY = """\
rate_card:
  currency: USD
  unit: per_million_tokens
  as_of: "2026-09-15"
  basis: list-price
  source: test fixture
  cache_write_multiplier: 1.25
  cache_read_multiplier: 0.1

providers:
  anthropic:
    display_name: Anthropic
    cli: claude
    version_command: ["claude", "--version"]

models:
  plan-model:
    provider: anthropic
    rates:
      input: 5.0
      output: 25.0
  execute-model:
    provider: anthropic
    rates:
      input: 2.0
      output: 10.0
  unpriced-model:
    provider: anthropic
"""


@pytest.fixture()
def registry(tmp_path):
    path = tmp_path / "provider-registry.yaml"
    path.write_text(_REGISTRY, encoding="utf-8", newline="\n")
    return path


def _turn(model: str, *, uuid: str, at: str, output_tokens: int = 0, cache_read: int = 0,
          cache_write: int = 0, input_tokens: int = 0) -> str:
    """One assistant turn in the Claude Code transcript shape, with its timestamp.

    `timestamp` sits on the RECORD, not inside `message` — the spelling measured on this host's
    own transcripts, and the field the window is read from.
    """
    return json.dumps({
        "type": "assistant",
        "uuid": uuid,
        "timestamp": at,
        "message": {
            "id": f"msg_{uuid}",
            "model": model,
            "usage": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cache_creation_input_tokens": cache_write,
                "cache_read_input_tokens": cache_read,
            },
        },
    })


#: One seat's sitting: four PLAN turns, then four EXECUTE turns after the handoff. The shape this
#: lane's split produces, so a test can ask whether the reader can SEE the split.
_SESSION_ID = "9b8de937-0744-4851-af0d-be3e84cd8005"


@pytest.fixture()
def store(tmp_path):
    """A session store holding one seat session plus unrelated history in the SAME directory.

    The second file is the whole point: it is the batch-Z defect in miniature. A reader keyed on
    the directory sums both and reports a number 8x too large; a reader keyed on the session id
    reports the sitting.
    """
    project = tmp_path / "sessions" / "C--Users-x-Documents-Dev--dev-knowledge"
    project.mkdir(parents=True)
    (project / f"{_SESSION_ID}.jsonl").write_text("\n".join([
        _turn("plan-model", uuid="p1", at="2026-09-15T23:10:00.000Z", output_tokens=100_000),
        _turn("plan-model", uuid="p2", at="2026-09-15T23:20:00.000Z", output_tokens=100_000),
        _turn("plan-model", uuid="p3", at="2026-09-16T00:00:00.000Z", output_tokens=100_000),
        _turn("plan-model", uuid="p4", at="2026-09-16T01:00:00.000Z", output_tokens=100_000),
        _turn("execute-model", uuid="e1", at="2026-09-16T02:00:00.000Z", output_tokens=100_000),
        _turn("execute-model", uuid="e2", at="2026-09-16T03:00:00.000Z", output_tokens=100_000),
        _turn("execute-model", uuid="e3", at="2026-09-16T04:00:00.000Z", output_tokens=100_000),
        # AFTER the declared window: the session ran on past the close, exactly as the real one
        # did. A reader that ignores the window prices this turn into the batch's figure.
        _turn("execute-model", uuid="e4", at="2026-09-16T09:00:00.000Z", output_tokens=100_000),
    ]) + "\n", encoding="utf-8", newline="\n")
    # Unrelated history in the same directory — the primary checkout's lifetime.
    (project / "aaaaaaaa-0000-0000-0000-000000000000.jsonl").write_text("\n".join([
        _turn("plan-model", uuid=f"h{n}", at="2026-01-01T00:00:00.000Z", output_tokens=1_000_000)
        for n in range(20)
    ]) + "\n", encoding="utf-8", newline="\n")
    return tmp_path / "sessions"


WINDOW = ("2026-09-15T23:00:00Z", "2026-09-16T06:51:12.577Z")


# --- REFUSAL 1: a seat is not a directory -------------------------------------------------

def test_a_seat_is_read_by_SESSION_ID_and_not_by_its_directory(store, registry):
    """The batch-Z defect, reproduced in miniature and then refused.

    The seat's own eight turns are 800,000 output tokens. The directory also holds 20,000,000
    tokens of unrelated history. A directory-keyed read sums both; the session-keyed read does
    not, and the ASSERTION IS THE RATIO rather than a bare figure, because the wrong answer here
    is not a small error — it is a different question answered confidently.
    """
    by_session = lc.seat_cost(_SESSION_ID, sessions_root=store, registry_path=registry)
    by_directory = lc.lane_cost("dev-knowledge", sessions_root=store, registry_path=registry)
    assert by_session.usage().total_tokens == 800_000
    assert by_directory.usage().total_tokens == 20_800_000
    assert by_directory.usd > 20 * by_session.usd


def test_a_session_id_that_names_no_transcript_is_UNKNOWN_and_never_zero(store, registry):
    """`lane_cost`'s own posture, carried to the seat: an unfound seat must not be the cheap one.

    The refusal names the id, because the remedy differs by cause — a typo, a seat that ran in
    another store, or a `--bg` child filed under its launcher — and a bare `False` sends a reader
    looking in the wrong place.
    """
    cost = lc.seat_cost("00000000-dead-beef-0000-000000000000", sessions_root=store,
                        registry_path=registry)
    assert cost.has_transcript() is False
    assert cost.usd == 0.0
    assert "NO TRANSCRIPT" in cost.render()
    assert "00000000-dead-beef" in cost.render()


# --- REFUSAL 2: a window that is not recorded ---------------------------------------------

def test_the_window_BOUNDS_the_figure_and_a_later_turn_is_excluded(store, registry):
    """A session transcript GROWS. Measured on the real batch-Z integrator session: USD 82.53 at
    06:51:12Z and USD 89.88 at end-of-file — the SAME file, 9% apart, and both honest.

    So a seat figure is a function of (session, window), and a reader that took only the session
    would silently re-price the baseline every time anyone reopened the seat's own session.
    """
    windowed = lc.seat_cost(_SESSION_ID, sessions_root=store, registry_path=registry,
                            since=WINDOW[0], until=WINDOW[1])
    whole = lc.seat_cost(_SESSION_ID, sessions_root=store, registry_path=registry)
    assert windowed.usage().calls == 7, "the 09:00Z turn is outside the declared window"
    assert whole.usage().calls == 8
    assert windowed.usd < whole.usd


def test_the_window_RIDES_THE_ROW_so_a_paired_comparison_can_check_it_is_the_same_one(
        tmp_path, store, registry):
    """THE paired-measurement guard, and the reason it is a stored field rather than a note.

    This lane's contract: *"Paired measurement must be adjacent in time and method. If you
    measure the new seat with a different reader, a different window, or a different definition
    of 'the integrator line', the comparison is worthless."* A window that lives only in the
    operator's memory cannot be checked; one that rides the row can be, by a reader months later
    who never met either seat.
    """
    cost = lc.seat_cost(_SESSION_ID, sessions_root=store, registry_path=registry,
                        since=WINDOW[0], until=WINDOW[1], batch="AA")
    lc.append_cost(tmp_path, cost)
    row = json.loads(lc.cost_ledger_path(tmp_path).read_text(encoding="utf-8").splitlines()[0])
    assert row["window"] == {"since": WINDOW[0], "until": WINDOW[1]}
    assert row["session_id"] == _SESSION_ID
    assert lc.read_cost_ledger(tmp_path)[0].window == WINDOW


def test_an_UNWINDOWED_seat_row_says_so_rather_than_implying_a_window(tmp_path, store, registry):
    """An absent window is reported as absent, never as an open interval someone might read as
    deliberate. The row is still valid — a seat whose session is finished has nothing to bound —
    but a reader must be able to tell "the whole session" from "a window I chose"."""
    cost = lc.seat_cost(_SESSION_ID, sessions_root=store, registry_path=registry)
    assert cost.window is None
    assert "WHOLE SESSION" in cost.render()


# --- REFUSAL 3: a split seat reported as one number ---------------------------------------

def test_a_SPLIT_seat_reports_its_two_halves_SEPARATELY(store, registry):
    """The measurement this lane exists to make possible.

    A split seat runs two models inside one sitting. If the reader summed them, the seat's line
    would look identical whether the split happened or not — and this lane's done-when is a
    MEASURED lower number, so an instrument that cannot see the split cannot close it.

    `ModelCost` per model already exists on `LaneCost`; what this asserts is that `seat_cost`
    preserves it rather than folding a seat into a single figure the way a receipt total does.
    """
    cost = lc.seat_cost(_SESSION_ID, sessions_root=store, registry_path=registry,
                        since=WINDOW[0], until=WINDOW[1])
    by_model = {m.model: m for m in cost.models}
    assert set(by_model) == {"plan-model", "execute-model"}
    # 400,000 output tokens at 25.0/MTok; 300,000 at 10.0/MTok — inside the window.
    assert by_model["plan-model"].usd == pytest.approx(10.0)
    assert by_model["execute-model"].usd == pytest.approx(3.0)
    assert cost.usd == pytest.approx(13.0)
    rendered = cost.render()
    assert "plan-model" in rendered and "execute-model" in rendered


def test_the_split_share_is_reported_so_a_DECORATIVE_split_is_visible(store, registry):
    """A split that is declared and did not happen is the failure mode this lane was warned about
    by name: *"a split that silently lets the cheap half make expensive decisions is worse than no
    split"*. Its cheap sibling is a split that simply never fired — every turn ran on the plan
    model and the config change bought nothing.

    So the seat row carries the SHARE of spend that ran on each model. A share of 100% on the plan
    model is a decorative split, and it is visible in the row rather than deducible from it.
    """
    cost = lc.seat_cost(_SESSION_ID, sessions_root=store, registry_path=registry,
                        since=WINDOW[0], until=WINDOW[1])
    shares = cost.model_shares()
    assert shares["plan-model"] == pytest.approx(10.0 / 13.0)
    assert shares["execute-model"] == pytest.approx(3.0 / 13.0)
    assert sum(shares.values()) == pytest.approx(1.0)


def test_model_shares_over_an_UNPRICED_model_does_not_manufacture_a_share(tmp_path, registry):
    """An unpriced model has tokens and no money. A share computed over the priced total would
    silently omit it while the percentages still summed to 1.0 — the precise plausible-value
    failure `lane_cost` refuses everywhere else. The share map carries the priced models and the
    row's own `unpriced()` still names the rest."""
    project = tmp_path / "sessions" / "proj"
    project.mkdir(parents=True)
    (project / "abcd.jsonl").write_text("\n".join([
        _turn("plan-model", uuid="p1", at="2026-09-15T23:10:00.000Z", output_tokens=100_000),
        _turn("unpriced-model", uuid="u1", at="2026-09-15T23:20:00.000Z", output_tokens=900_000),
    ]) + "\n", encoding="utf-8", newline="\n")
    cost = lc.seat_cost("abcd", sessions_root=tmp_path / "sessions", registry_path=registry)
    assert [m.model for m in cost.unpriced()] == ["unpriced-model"]
    assert cost.model_shares() == {"plan-model": pytest.approx(1.0)}
    assert "UNPRICED" in cost.render()


# --- REFUSAL 4: a missing seat row read as a cheap batch -----------------------------------

def test_a_batch_with_lane_rows_and_NO_seat_row_is_reported_as_a_GAP(tmp_path, store, registry):
    """The batch-Z finding, turned into something that fires on its own.

    The close packet: *"The cost ledger `logs/LANE-COSTS.jsonl` carries ZERO batch-Z rows … every
    figure above was recomputed at close from transcripts rather than read from the ledger …
    A figure that must be recomputed at close is not a ledger."* The integrator seat was 30.5% of
    that batch, so a batch total built from lane rows alone understates it by a third while
    looking complete.
    """
    lane = lc.lane_cost("lane-aa-1", batch="AA", sessions_root=store, registry_path=registry,
                        slug_dirs=["C--Users-x-Documents-Dev--dev-knowledge"])
    lc.append_cost(tmp_path, lane)
    gap = lc.seat_cost_gap(tmp_path)
    assert gap is not None
    assert "AA" in gap
    assert "seat" in gap.lower()


def test_the_GAP_CLOSES_when_the_seat_row_lands(tmp_path, store, registry):
    lane = lc.lane_cost("lane-aa-1", batch="AA", sessions_root=store, registry_path=registry,
                        slug_dirs=["C--Users-x-Documents-Dev--dev-knowledge"])
    lc.append_cost(tmp_path, lane)
    seat = lc.seat_cost(_SESSION_ID, sessions_root=store, registry_path=registry, batch="AA",
                        since=WINDOW[0], until=WINDOW[1])
    lc.append_cost(tmp_path, seat)
    assert lc.seat_cost_gap(tmp_path) is None


def test_the_gap_reaches_the_SessionStart_digest_without_anyone_remembering_to_look(
        tmp_path, store, registry):
    """DONE-WHEN 4, and the leg that makes it automatic rather than a habit.

    `cost_health_line` is printed by `fleet_health` at every SessionStart. Folding the seat gap
    into it means the next batch's integrator line appears in the boot banner — and so does its
    ABSENCE. Nobody has to remember to run anything; the seat that forgot is named at the next
    seat's first screen.
    """
    lane = lc.lane_cost("lane-aa-1", batch="AA", sessions_root=store, registry_path=registry,
                        slug_dirs=["C--Users-x-Documents-Dev--dev-knowledge"])
    lc.append_cost(tmp_path, lane)
    line = lc.cost_health_line(tmp_path)
    assert line is not None
    assert "seat" in line.lower()


def test_only_the_LATEST_batch_is_named_and_older_gaps_are_COUNTED(tmp_path, store, registry):
    """An older batch's gap is usually unclosable — the seat's session ages out of the store and
    a closed batch's record does not carry the window. A permanent item nobody can clear is how a
    reader learns to scroll past this line, which is the failure the check exists to avoid,
    arriving by a different door. So the actionable one is NAMED and the rest are COUNTED.

    Ledger order is chronological (append-only), and batch letters ran past `Z` into `AA` — so
    "latest" is read from the file, never sorted. A lexical sort would name `AA` as the oldest.
    """
    for batch in ("Z", "AA"):
        row = lc.lane_cost(f"lane-{batch}-1", batch=batch, sessions_root=store,
                           registry_path=registry,
                           slug_dirs=["C--Users-x-Documents-Dev--dev-knowledge"])
        lc.append_cost(tmp_path, row)
    gap = lc.seat_cost_gap(tmp_path)
    assert gap is not None
    assert "batch AA carries" in gap
    assert "1 older batch(es) likewise" in gap


def test_an_EMPTY_ledger_reports_no_seat_gap_rather_than_a_false_one(tmp_path):
    """A batch with no rows at all has not forgotten its seat — it has not started. Reporting a
    gap there would train a reader to ignore the line, which is how a real gap gets through."""
    assert lc.seat_cost_gap(tmp_path) is None


# --- the definition itself ----------------------------------------------------------------

def test_cache_reads_are_IN_the_seat_definition_and_the_test_says_why(tmp_path, registry):
    """MEASURED on the batch-Z integrator session: cache reads are **80.8%** of that seat's bill
    (145,314,211 of 146,653,877 tokens; USD 72.66 of USD 89.88). A definition that excluded them
    — as `logs/TOKEN-LOG.md` does "for comparability" — would misstate the integrator line by
    more than the integrator line.

    This is the frozen half of the paired comparison: the next batch's seat MUST be priced under
    the same definition or the comparison is worthless.
    """
    project = tmp_path / "sessions" / "proj"
    project.mkdir(parents=True)
    (project / "cafe.jsonl").write_text(
        _turn("plan-model", uuid="c1", at="2026-09-15T23:10:00.000Z",
              cache_read=1_000_000, output_tokens=0) + "\n",
        encoding="utf-8", newline="\n")
    cost = lc.seat_cost("cafe", sessions_root=tmp_path / "sessions", registry_path=registry)
    # 1 MTok of cache read at the plan model's 5.0 input rate x the 0.1 cache-read multiplier.
    assert cost.usd == pytest.approx(0.5)
    assert cost.usage().cache_read_tokens == 1_000_000
