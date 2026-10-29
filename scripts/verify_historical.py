"""Verify pinned inputs, cohort integrity and independent summary calculations."""
import csv, hashlib, json, pathlib, statistics, math, subprocess, sys
root=pathlib.Path(__file__).resolve().parents[1]
p=root/'data/historical'
for item in json.loads((p/'manifest.json').read_text()):
 if 'extract' in item:
  assert hashlib.sha256((p/item['extract']).read_bytes()).hexdigest()==item['sha256']
for name in ['general','survey','readmission']:
 rows=list(csv.DictReader((p/f'{name}.csv').open()))
 assert len(rows)==len({r['Facility ID'] for r in rows})
before=(p/'results.json').read_bytes()
subprocess.run([sys.executable,str(root/'scripts/historical_analysis.py')],check=True,stdout=subprocess.DEVNULL)
def equivalent(a,b):
 if isinstance(a,dict):return a.keys()==b.keys() and all(equivalent(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(equivalent(x,y) for x,y in zip(a,b))
 if isinstance(a,float):return math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12)
 return a==b
assert equivalent(json.loads(before),json.loads((p/'results.json').read_text())), 'Analysis changed beyond floating-point tolerance'
(p/'results.json').write_bytes(before)
r=json.loads(before);h=r['hospitals'];assert len(h)==61 and r['survey300']['n']==51
assert all(x['state']=='WI' and x['surveys']>=100 for x in h)
x=[a['discharge'] for a in h];y=[a['readmission'] for a in h]
assert math.isclose(statistics.correlation(x,y),r['primary']['pearson'],abs_tol=1e-12)
assert math.isclose(statistics.linear_regression(x,y).slope*5,r['primary']['slope_per_5pp'],abs_tol=1e-12)
assert json.loads((root/'site/historical-results.json').read_text())==r
assert (root/'site/historical-manifest.json').read_bytes()==(p/'manifest.json').read_bytes()
print('Historical source hashes, cohort, independent estimates and reproduction within 1e-12 tolerance passed')
