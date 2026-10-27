p='../integrate-e2-1-journal-entry.md'
s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    assert a in s, a[:70]
    s=s.replace(a,b)
rep('regenerate (BACKLOG.md 809 -> 806 tasks, tasks/manifest.json, ecosystem/doc-counts.md, docs/audits/README.md for the new Codex review record)','regenerate (BACKLOG.md 809 -> 806 tasks, tasks/manifest.json, ecosystem/doc-counts.md)')
rep("hard-fails 0 introduced by the diff; two new WARNs for the Codex review record (consumer_at_landing, funnel_coverage: no consumer, no disposition) and one generated-artifact WARN fixed here by regenerating the audits index; ","hard-fails 0 introduced by the diff; the lane's Codex review record (docs/audits/2026-10-23-codex-codespace-delivery-fix-review.md) carried two new WARNs (consumer_at_landing, funnel_coverage) and, in the first landing attempt (CI run 40003524303), two new red tests in tests/test_consumer_at_landing.py (the branch-context witnesses): its consumer is the lane's own merge receipt, which exists only after the landing. DECIDED-BY-INTEGRATOR: this merge lands WITHOUT that one file (left on the lane tip ebdc856a8, an ancestor of main) and the NEXT landing adds it together with this lane's receipt line, the integration shape the witness describes; ")
rep("`docs/audits/2026-10-23-codex-codespace-delivery-fix-review.md`, `docs/audits/README.md`, ","")
rep("**Next:** startup-tokens repair","**Next:** the next landing restores docs/audits/2026-10-23-codex-codespace-delivery-fix-review.md (git show ebdc856a8:docs/audits/2026-10-23-codex-codespace-delivery-fix-review.md) with this lane's ledger line in the same merge; startup-tokens repair")
open(p,'w',encoding='utf-8').write(s)
s=open('JOURNAL.md',encoding='utf-8',newline='').read()
e=open(p,encoding='utf-8',newline='').read().replace('\r\n','\n')
nl='\r\n' if '\r\n' in s else '\n'
e=e.replace('\n',nl)
i=s.index('### 2026-10-23 (d)')
open('JOURNAL.md','w',encoding='utf-8',newline='').write(s[:i]+e+s[i:])
print('ok')
