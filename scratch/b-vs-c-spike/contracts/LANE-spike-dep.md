# LANE spike-dep -- synthetic contract for the b-vs-c spike (never launched)

| Model | Mode | Effort |
|---|---|---|
| claude-sonnet-5-5 | execute | high |

## Dispatch

```
claude --bg -n spike-dep --model claude-sonnet-5-5 --effort high --permission-mode bypassPermissions --worktree spike-dep "Read and execute the frozen contract"
```

slug `spike-dep` -> branch `worktree-spike-dep` -> contract `LANE-spike-dep.md`

**Starts after `spike-clean` is merged.**  serialize-group: spike-g1
