s=open('JOURNAL.md',encoding='utf-8',newline='').read()
e=open('../integrate-e2-1-journal-entry-f.md',encoding='utf-8',newline='').read().replace('\r\n','\n')
nl='\r\n' if '\r\n' in s else '\n'
e=e.replace('\n',nl)
i=s.index('### 2026-10-23 (e)')
open('JOURNAL.md','w',encoding='utf-8',newline='').write(s[:i]+e+s[i:])
print('ok')
