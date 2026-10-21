carried-by: OPEN
kind: HANDOVER
summary: <one line: what this seat was doing and where it stopped>
by: <outgoing seat id>

# Handover <seat> cycle <n>

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

<!-- The successor's first act is to read this file, then append one BOUND line:
BOUND seat=<seat> cycle=<n> job=<successor job id> model=<served model>
Until that line exists the outgoing seat keeps running; it is stopped only after BOUND. -->
