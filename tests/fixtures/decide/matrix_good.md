# synthetic fixture -- matrix_good

Weights: fidelity=25 portability=20 throughput=20 cost=10 modifiability=10 observability=15

| Area A | fidelity | portability | throughput | cost | modifiability | observability | Σ |
|---|---|---|---|---|---|---|---|
| A1 today | 3 | 1 | 1 | 2 | 3 | 1 | 1.80 |
| A7 armed | 4[^1] | 4[^2] | 4[^3] | 4[^4] | 3 | 4[^5] | 3.90 |

[^1]: measured -- run 36234959090, jobs/70677588/tmp/vtop-suite.log:561
[^2]: measured -- docs.github.com/actions/reference/runners, read 2026-09-26
[^3]: measured -- run 36234959090 vs the local suite's 4,935 s
[^4]: measured -- public-repo runners are $0 (docs.github.com/actions, read 2026-09-26)
[^5]: measured -- the required-status-check URL, read 2026-09-26
