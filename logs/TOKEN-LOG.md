# Token Usage Log

Append /stats snapshot weekly. Never edit previous entries.

## 2026-07-01 (delta: 2026-06-24 to 2026-07-01, via ccusage --json)
Delta: 7 active days, sessions N/A (not in ccusage --json), $491.60
Tokens in+out: 5.42M (in: 956K, out: 4464K) — cache not counted here for comparability
Opus 4.8: 94.4% (in: 786K, out: 4332K)
Haiku 4.5: 4.7% (in: 165K, out: 90K)
Sonnet 4.6: 0.8% (in: 5K, out: 41K)
Peak day: 2026-06-26 ($123.38)
Rate limits hit: N/A (not available via ccusage --json)

## 2026-06-23 (delta: 2026-06-16 to 2026-06-23, via ccusage --json)
Delta: 8 active days, sessions N/A (not in ccusage --json), $685.28
Tokens in+out: 9.62M (in: 1801K, out: 7814K) — cache not counted here for comparability
Opus 4.8: 87.8% (in: 1253K, out: 7186K)
Haiku 4.5: 11.7% (in: 545K, out: 585K)
Sonnet 4.6: 0.5% (in: 4K, out: 43K)
Peak day: 2026-06-20 ($119.24)
Rate limits hit: N/A (not available via ccusage --json)

## 2026-06-15 (delta: 2026-06-08 to 2026-06-15, via ccusage --json)
Delta: 8 active days, sessions N/A (not in ccusage --json), $416.40
Tokens in+out: 5.23M (in: 1021K, out: 4208K) — cache not counted here for comparability
Opus 4.8: 86.5% (in: 680K, out: 3844K)
Haiku 4.5: 11.9% (in: 339K, out: 280K)
Sonnet 4.6: 1.7% (in: 3K, out: 84K)
Peak day: 2026-06-11 ($93.97)
Rate limits hit: N/A (not available via ccusage --json)

## 2026-06-07 (delta: 2026-05-28 to 2026-06-07, via ccusage 18.0.11)
Delta: 11 active days, sessions N/A (not in ccusage --json), $883.77
Tokens in+out: 9.29M (in: 1301K, out: 7993K) — cache not counted here for comparability
Opus 4.8: 82.4% (in: 1060K, out: 6601K)
Sonnet 4.6: 10.3% (in: 59K, out: 900K)
Opus 4.7: 4.0% (in: 75K, out: 301K)
Haiku 4.5: 3.2% (in: 108K, out: 191K)
Peak day: 2026-06-02 ($178.40)
Rate limits hit: N/A (not available via ccusage --json)
Note: Opus 4.8 marathon band (first full window on 4.8); ccusage figure is model-priced — Max-subscription actual billing differs. Resumes the weekly comparability series after the 2026-05-31 session-scoped marker (kept out of the series); window picks up from the 2026-05-27 weekly delta.

## 2026-05-31 (session-scoped marker — methodology+backlog audit; NOT a ccusage weekly delta)
Single Claude Code session (Opus, xhigh). Scope: 3-track methodology/canonical/backlog audit, analysis-only, 7 commits, no structural edits.
Reads: CLAUDE/VISION/ARCHITECTURE/BACKLOG(871L full)/ESSENTIALS/AI_COUNCIL_PROCESS/PLAYBOOK(TOC+§7+§10)/ADR-39/41/47/48 + 2026-05-31 classification audit + targeted greps/globs.
Sub-agent (reference study, Customization track only): 32,810 output tokens, 27 tool-uses, 125.8s (measured).
Main-session exact in/out tokens not instrumented here — append the canonical weekly ccusage delta at the normal cadence; this per-session marker is kept out of the weekly comparability series.

## 2026-05-27 (delta: 2026-05-20 to 2026-05-27, via ccusage)
Delta: 8 active days, sessions N/A (not in ccusage --json), $207.10
Tokens in+out: 1.90M (in: 174K, out: 1729K) — cache not counted here for comparability
Opus 4.7: 85.2%
Sonnet 4.6: 13.0%
Haiku 4.5: 1.8%
Peak day: 2026-05-27 ($46.24)
Rate limits hit: N/A (not available via ccusage --json)

## 2026-05-19 (delta: 2026-05-10 to 2026-05-19, via ccusage)
Delta: 10 active days, sessions N/A (not in ccusage --json), $223.86
Tokens in+out: 2.46M (in: 215K, out: 2244K) — cache not counted here for comparability
Sonnet 4.6: 65.1%
Opus 4.7: 32.2%
Haiku 4.5: 2.7%
Peak day: 2026-05-18 ($75.08)
Rate limits hit: N/A (not available via ccusage --json)

## 2026-05-09 (delta: 2026-04-24 to 2026-05-09, via ccusage 18.0.11)
Delta: 8 active days, sessions N/A (not in ccusage --json), $113.44
Tokens in+out: 1.7M (in: 75K, out: 1.6M) — cache not counted here for comparability
Sonnet 4.6: 82.2% (in: 48K, out: 1.3M)
Opus 4.7: 16.0% (in: 15K, out: 255K)
Haiku 4.5: 1.8% (in: 13K, out: 17K)
Peak day: 2026-04-27 ($26.59)
Rate limits hit: N/A (not available via ccusage --json)

## 2026-04-24 (delta: 2026-03-29 to 2026-04-24, via ccusage 18.0.11)
Delta: 11 active days, 31 sessions, $190.53
Tokens in+out: 1.8M (in: 284K, out: 1.5M) — cache not counted here for comparability
Sonnet 4.6: 49.5% (in: 102K, out: 779K)
Haiku 4.5: 23.8% (in: 126K, out: 298K)
Opus 4.7: 16.1% (in: 23K, out: 264K)  [first use: Apr 17]
Opus 4.6: 10.5% (in: 33K, out: 154K)
Peak day: Mar 30 ($59.99)
Rate limits hit: N/A (not available via ccusage --json)
Note: ccusage counts in+out only for comparability; cache tokens excluded (cache-create 14M, cache-read 323M tracked separately in JSON). /stats baseline method differs — lifetime totals not directly comparable.

## 2026-03-28 (baseline, end of Spring Break 2x promotion)
Total: 5.2M tokens, 89 days, 34 active, 129 sessions
Opus 4.6: 70.1% (in: 427K, out: 3.2M)
Sonnet 4.6: 23.1% (in: 74K, out: 1.1M)
Sonnet 4.5: 5.8% (in: 28K, out: 272K)
Opus 4.5: 1.0% (in: 25K, out: 29K)
Peak day: Mar 25
Rate limits hit this week: unknown (start tracking from next week)
