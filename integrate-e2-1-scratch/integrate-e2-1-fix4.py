p='../integrate-e2-1-journal-entry-g.md'
j=open('JOURNAL.md',encoding='utf-8',newline='').read()
e=open(p,encoding='utf-8',newline='').read().replace('\r\n','\n')
nl='\r\n' if '\r\n' in j else '\n'
e=e.replace('\n',nl)
i=j.index('### 2026-10-23 (f)')
open('JOURNAL.md','w',encoding='utf-8',newline='').write(j[:i]+e+j[i:])
print('ok')
