# LANE e30-fixture -- a Sonnet-implements test contract

| Model | Mode | Effort |
|---|---|---|
| claude-sonnet-5-5 | execute | medium |

## Dispatch

```
claude --bg -n e30-fixture --model claude-sonnet-5-5 --effort medium --permission-mode bypassPermissions --worktree e30-fixture "Read and execute the frozen contract"
```

## Roles

| Phase | Model | Where |
|---|---|---|
| lane head | claude-sonnet-5-5 | local |
| implement | claude-sonnet-5-5 | local |
