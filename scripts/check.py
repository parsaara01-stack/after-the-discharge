#!/usr/bin/env python3
"""Meaningful source, selection, missing-data and public-artifact invariants."""
import csv,hashlib,html.parser,json,pathlib,subprocess,sys
from analyze import number,reliable
ROOT=pathlib.Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(ROOT/'scripts/analyze.py')],check=True,stdout=subprocess.DEVNULL)
subprocess.run([sys.executable,str(ROOT/'scripts/prepare_site.py')],check=True)
s=json.loads((ROOT/'data/derived/summary.json').read_text()); rows=list(csv.DictReader((ROOT/'data/derived/wisconsin_audit.csv').open()))
assert number('Not Available') is None and number('') is None and number('Not Applicable') is None
assert number('0')==0 and number('nan') is None and number('inf') is None
base={'HCAHPS Answer Percent':'89','Number of Completed Surveys':'100','HCAHPS Answer Percent Footnote':''}
assert reliable(base)
assert not reliable(dict(base,**{'Number of Completed Surveys':'99'}))
assert not reliable(dict(base,**{'HCAHPS Answer Percent Footnote':'6'}))
assert len(rows)==140 and len({r['facility_id'] for r in rows})==140
assert all(len(r['facility_id'])==6 and r['facility_id'].startswith('52') for r in rows)
a=[r for r in rows if r['hospital_type']=='Acute Care Hospitals']
assert len(a)==64 and s['reliable_exposure_n']==63
assert s['eligible_pairs']==0 and s['association'] is None
assert all(r['readmission_raw']=='Not Available' and r['readmission_percent']=='' and r['readmission_footnote']=='4' for r in a)
assert all(r['readmission_denominator_raw']==r['readmission_lower_raw']==r['readmission_upper_raw']=='Not Available' for r in a)
assert all(r['exact_period_match']=='False' for r in a)
assert s['overlap_days']==273
assert s['all_acute_discharge']['median']==89 and s['all_acute_discharge']['min']==81 and s['all_acute_discharge']['max']==94
assert s['sensitivity']['100']['n']==63 and s['sensitivity']['300']['n']==52
assert sum(s['hospital_types'].values())==140
for before,after in zip(s['funnel'],s['funnel'][1:]):assert before['remaining']-after['excluded']==after['remaining']
assert s['funnel'][-1]['remaining']==0
n=json.loads((ROOT/'data/national_audit.json').read_text())
assert all(x['duplicate_keys']==0 for x in n.values())
assert 'READM_30_HOSP_WIDE' not in n['632h-zaca']['measures']
assert sum(n['632h-zaca']['selected_outcome_tokens'].values())==4790
assert set(n['632h-zaca']['selected_outcome_tokens'])=={'Not Available | footnote 4','Not Available | footnote 5','Not Available | footnote 19'}
for r in json.loads((ROOT/'data/source_manifest.json').read_text()):
 p=ROOT/r['path']
 if p.exists():assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],r['path']
class Links(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:assert d['id'] not in self.ids;self.ids.add(d['id'])
  for k in ['href','src']:
   if d.get(k):self.links.append(d[k])
l=Links();l.feed((ROOT/'site/index.html').read_text())
for link in l.links:
 if link.startswith('#'):assert link=='#' or link[1:] in l.ids,link
 elif '://' not in link:assert (ROOT/'site'/link).is_file(),link
assert json.loads((ROOT/'site/pilot-data.json').read_text())['summary']==s
print('PASS: source hashes, unique IDs, missing != zero, reliability boundaries, cohort/funnel, independent time mismatch, national availability, site downloads and anchors.')
