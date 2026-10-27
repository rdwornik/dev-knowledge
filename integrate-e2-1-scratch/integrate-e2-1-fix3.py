p='../integrate-e2-1-journal-entry-f.md'
s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    assert a in s, a[:70]
    s=s.replace(a,b)
rep("`88421fe17` (the lane tip: the one dated fates line, common rule 2a)","`88421fe17` (the one dated fates line, common rule 2a), `21a9a369b` (the lane tip, repair 2: the probe reads its default model from `provider_registry.anthropic_role_model(\"seat-orchestrator\")`, not a literal, R1536)")
rep("(7 code commits plus the fates commit on merge-base af8bdad5b;","(9 lane commits on merge-base af8bdad5b;")
rep("substitution gate clean after repair 1 (`([], [])` with the primary's receipts dir)","substitution gate clean (`([], [])` with the primary's receipts dir); the first merge (94189ab301ed, CI run 40013380443) was REFUSED REGRESSED on `tests/test_model_id_single_source.py` x2 (the probe hard-coded a model id) and sent back as repair 2 of 2, nothing reached main")
rep("`--close-row 1705 --evidence 5f0a26eda`","`--close-row 1705 --evidence 21a9a369b`")
rep("merged-tree tests, then the ship-gate diff.","merged-tree tests (368 passed, 1 skipped, -n0, 710 s; now including test_model_id_single_source, test_consumer_at_landing and test_provider_registry), ship-gate head leg of the first merged tree (hard-fails 0 introduced; not re-run for the 23-line repair-2 delta).")
rep("**Next:** landing-class (L8) @ 0cead9524, then connector-land (rebase on this main, re-bind process-binding.yaml), then ci-one-verdict repair 1.","**Next:** ci-one-verdict (repair 1 handback c80044042), then landing-class (repair 1 owed), then connector-land (rebase on this main, re-bind process-binding.yaml).")
open(p,'w',encoding='utf-8').write(s)
j=open('JOURNAL.md',encoding='utf-8',newline='').read()
e=open(p,encoding='utf-8',newline='').read().replace('\r\n','\n')
nl='\r\n' if '\r\n' in j else '\n'
e=e.replace('\n',nl)
i=j.index('### 2026-10-23 (e)')
open('JOURNAL.md','w',encoding='utf-8',newline='').write(j[:i]+e+j[i:])
print('ok')
