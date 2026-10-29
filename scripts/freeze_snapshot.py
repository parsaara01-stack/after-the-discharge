#!/usr/bin/env python3
"""Check national keys and preserve a bounded, exact-column Wisconsin extract."""
import collections,csv,hashlib,json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
raw=ROOT/'data/raw'; bounded=ROOT/'data/snapshot'; bounded.mkdir(exist_ok=True)
audit={};manifest=[]
for ds,key,measure in [('xubh-q36u',None,None),('dgck-syfz','HCAHPS Measure ID','H_COMP_6_Y_P'),('632h-zaca','Measure ID','Hybrid_HWR')]:
 path=raw/(ds+'.csv'); seen=set(); selected=[]; counts=collections.Counter();tokens=collections.Counter();n=0; ids=set(); dates=collections.Counter()
 with path.open(encoding='utf-8-sig',newline='') as f:
  reader=csv.DictReader(f); fields=reader.fieldnames
  for r in reader:
   n+=1; ident=r['Facility ID']; assert re.fullmatch(r'[A-Za-z0-9]{6}',ident),repr(ident)
   k=(ident,r[key]) if key else ident
   assert k not in seen,('duplicate',ds,k)
   seen.add(k);ids.add(ident)
   if key: counts[r[key]]+=1
   if key and r[key]==measure:
    dates[(r['Start Date'],r['End Date'])]+=1
    if ds=='632h-zaca':tokens[r['Score']+' | footnote '+r['Footnote']]+=1
   if r['State']=='WI' and (not key or r[key]==measure):selected.append(r)
 with (bounded/(ds+'.csv')).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(selected)
 b=(bounded/(ds+'.csv')).read_bytes()
 manifest.append(dict(path='data/snapshot/'+ds+'.csv',sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),rows=len(selected),parent_path='data/raw/'+ds+'.csv',parent_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),filter='State == WI'+(' AND '+key+' == '+measure if key else '')))
 audit[ds]=dict(national_rows=n,national_facilities=len(ids),duplicate_keys=0,selected_wisconsin_rows=len(selected),measures=dict(sorted(counts.items())),selected_measure_dates=[dict(start=s,end=e,rows=c) for (s,e),c in dates.items()],selected_outcome_tokens=dict(tokens))
(ROOT/'data/snapshot_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(ROOT/'data/national_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
print(json.dumps({k:{a:b for a,b in v.items() if a not in ['measures']} for k,v in audit.items()},indent=2))
