p='logs/MERGE-RECEIPTS.jsonl'
c=open('../integrate-e2-1-land-carry.jsonl','rb').read().replace(b'\r\n',b'\n').rstrip(b'\n')+b'\n'
b=open(p,'rb').read(); assert b.endswith(b'\n') and c not in b
open(p,'wb').write(b+c); print(len(open(p,'rb').read().splitlines()), b'\r' in open(p,'rb').read())
import json; print(json.loads(c)['slug'])
