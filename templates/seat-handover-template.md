carried-by: OPEN
kind: HANDOVER
summary: <one line: what this seat was doing and where it stopped>
by: <outgoing seat id>

# Handover <seat> cycle <n>

## Head row

| Model | Mode | Effort |
|---|---|---|
| <model from the role table> | execute | <effort from ecosystem/seat-cycle.yaml> |

## State

<Where the work stands now: what is merged, what is mid-flight, what is blocked.>

## Next steps

1. <First action the successor takes; a numbered item is required.>

## Open decisions

- <A decision still open, or `none`.>

## Live children

- <A lane or child still running that the successor inherits, or `none`.>

## Seat bookkeeping

<Cycle count, batch id, base branch, worktree: whatever the successor needs to keep the seat's books.>

## First act (successor)

FIRST read every section above. THEN, as the next action, run exactly:

```
uv run --locked python scripts/seat_cycle.py bound --handover <abs handover path> --name <successor slug> --seat <outgoing seat> --cycle <n>
```

The BOUND line it appends means the handover is consumed.

<!-- That command appends one BOUND line:
BOUND seat=<seat> cycle=<n> job=<successor job id> model=<served model>
Until that line exists the outgoing seat keeps running; it is stopped only after BOUND. -->
