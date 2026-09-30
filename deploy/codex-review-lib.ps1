# deploy/codex-review-lib.ps1 -- consumer-line composition for the Codex-review organ ([#1329]).
#
# Function-only: no top-level param() block, so dot-sourcing this file is safe (no mandatory
# prompt, no side effect) -- the deliberate split that makes Get-ConsumerLine independently
# testable without running codex-review.ps1's precondition/diff/codex-invocation chain.
#
# THE FOUR CITATION FORMS AND THE REASON FLOOR ARE DUPLICATED FROM
# scripts/consumer_at_landing.py's _CITATION_RES / NO_CONSUMER_REASON_FLOOR, NOT IMPORTED --
# this script is deployed standalone to an arbitrary operator repo (~/.claude/bin/), which has
# no scripts/consumer_at_landing.py and no `uv`/hub Python environment to reach back into. A
# second copy is the honest cost of a user-machine-scoped organ; tests/test_codex_review_consumer.py
# pins both copies' literal patterns so a change to one side is caught rather than silently
# drifting.

function Get-ConsumerLine {
    param(
        [string]$Consumer = "",
        [string]$NoConsumerReason = ""
    )

    # Mirrors consumer_at_landing._CITATION_RES: a backlog row, an ADR, the standing-rulings
    # register, or an intake -- the four forms an artifact's own text can declare a consumer by.
    $citationPatterns = @(
        '\[#\d+\]',
        '\bADR-\d+(?!\d)',
        'STANDING_RULINGS',
        '\bintake\s+#\d+'
    )
    # Mirrors consumer_at_landing.NO_CONSUMER_REASON_FLOOR.
    $reasonFloor = 24

    $consumer = $Consumer.Trim()
    $reason = $NoConsumerReason.Trim()

    if ($consumer -and $reason) {
        throw "Get-ConsumerLine: pass -Consumer or -NoConsumerReason, not both"
    }

    if ($consumer) {
        $matched = $false
        foreach ($pattern in $citationPatterns) {
            if ($consumer -match $pattern) { $matched = $true; break }
        }
        if (-not $matched) {
            throw ("Get-ConsumerLine: '$consumer' matches no governance-citation form " +
                   "(a [#id] row, ADR-<n>, STANDING_RULINGS, or intake #<n>)")
        }
        return "**Consumer:** $consumer"
    }

    if ($reason.Length -ge $reasonFloor) {
        return "no-consumer: $reason"
    }

    throw ("Get-ConsumerLine: pass -Consumer <citation> (a [#id] row, ADR-<n>, " +
           "STANDING_RULINGS, or intake #<n>), or -NoConsumerReason of at least " +
           "$reasonFloor characters")
}
