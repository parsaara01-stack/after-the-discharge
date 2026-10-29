#!/usr/bin/env python3
"""Reproduce feasibility audit from checked-in public hospital aggregates. No dependencies."""
import collections,csv,datetime,hashlib,json,math,pathlib,statistics
ROOT=pathlib.Path(__file__).resolve().parents[1]
def number(s):
 try:
  n=float(s);return n if math.isfinite(n) else None
 except (TypeError,ValueError):return None
def read(ds):
 with (ROOT/'data/snapshot'/f'{ds}.csv').open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def indexed(rows):
 d={}
 for r in rows:
  assert r['Facility ID'] not in d,'Duplicate join key';d[r['Facility ID']]=r
 return d
def period(r):return (r.get('Start Date'),r.get('End Date'))
def reliable(r,minimum=100):
 return number(r.get('HCAHPS Answer Percent')) is not None and number(r.get('Number of Completed Surveys')) is not None and number(r['Number of Completed Surveys'])>=minimum and not r.get('HCAHPS Answer Percent Footnote')
def summarize(vals):
 vals=sorted(vals)
 if not vals:return dict(n=0,median=None,min=None,max=None,mean=None)
 return dict(n=len(vals),median=statistics.median(vals),min=min(vals),max=max(vals),mean=round(statistics.mean(vals),4))
def main():
 for r in json.loads((ROOT/'data/snapshot_manifest.json').read_text()):
  assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256'],'Snapshot changed'
 g=read('xubh-q36u');h=indexed(read('dgck-syfz'));o=indexed(read('632h-zaca'));indexed(g)
 cross={r['Footnote']:r['Footnote Text'] for r in csv.DictReader((ROOT/'data/raw/y9us-9xdf.csv').open(encoding='utf-8-sig'))}
 stages=[];current=g
 def keep(label,predicate):
  nonlocal current
  before=len(current);current=[r for r in current if predicate(r)];stages.append(dict(stage=label,remaining=len(current),excluded=before-len(current)))
 stages.append(dict(stage='Wisconsin facilities in CMS general-information file',remaining=len(g),excluded=0))
 keep('Acute Care Hospitals',lambda r:r['Hospital Type']=='Acute Care Hospitals');acute=list(current)
 keep('Discharge-information measure row matched by facility ID',lambda r:r['Facility ID'] in h)
 keep('Numeric discharge-information score',lambda r:number(h[r['Facility ID']]['HCAHPS Answer Percent']) is not None)
 keep('At least 100 completed surveys; no discharge-score footnote',lambda r:reliable(h[r['Facility ID']]))
 reliable_n=len(current)
 keep('Hospital-wide hybrid readmission row matched by facility ID',lambda r:r['Facility ID'] in o)
 keep('Numeric hospital-wide readmission score',lambda r:number(o[r['Facility ID']]['Score']) is not None)
 keep('Exactly matching measurement start and end dates',lambda r:period(h[r['Facility ID']])==period(o[r['Facility ID']]))
 rows=[]
 for r in g:
  ident=r['Facility ID'];a=h.get(ident,{});b=o.get(ident,{})
  rows.append(dict(facility_id=ident,facility_name=r['Facility Name'],hospital_type=r['Hospital Type'],ownership=r['Hospital Ownership'],city=r['City/Town'],discharge_percent=number(a.get('HCAHPS Answer Percent')),completed_surveys=number(a.get('Number of Completed Surveys')),survey_response_percent=number(a.get('Survey Response Rate Percent')),exposure_footnote=a.get('HCAHPS Answer Percent Footnote','ROW ABSENT'),survey_count_footnote=a.get('Number of Completed Surveys Footnote','ROW ABSENT'),exposure_start=a.get('Start Date',''),exposure_end=a.get('End Date',''),readmission_raw=b.get('Score','ROW ABSENT'),readmission_percent=number(b.get('Score')),readmission_footnote=b.get('Footnote','ROW ABSENT'),readmission_footnote_text=cross.get(b.get('Footnote'),''),readmission_denominator_raw=b.get('Denominator','ROW ABSENT'),readmission_lower_raw=b.get('Lower Estimate','ROW ABSENT'),readmission_upper_raw=b.get('Higher Estimate','ROW ABSENT'),outcome_start=b.get('Start Date',''),outcome_end=b.get('End Date',''),primary_reliable_exposure=reliable(a),exact_period_match=period(a)==period(b) and bool(a) and bool(b),eligible=ident in {x['Facility ID'] for x in current}))
 ac=[r for r in rows if r['hospital_type']=='Acute Care Hospitals']; ex=next(r for r in ac if r['exposure_start']);out=next(r for r in ac if r['outcome_start'])
 date=lambda s:datetime.datetime.strptime(s,'%m/%d/%Y').date()
 overlap=max(0,(min(date(ex['exposure_end']),date(out['outcome_end']))-max(date(ex['exposure_start']),date(out['outcome_start']))).days+1)
 summary=dict(status='Feasibility pilot — association not estimable',as_of='2026-10-29',author='Parsa Ara',exposure_measure='H_COMP_6_Y_P',outcome_measure='Hybrid_HWR',funnel=stages,hospital_types=dict(collections.Counter(r['Hospital Type'] for r in g)),acute_hospitals=len(acute),reliable_exposure_n=reliable_n,eligible_pairs=len(current),acute_numeric_readmission_n=sum(r['readmission_percent'] is not None for r in ac),acute_outcome_tokens=dict(collections.Counter(r['readmission_raw'] for r in ac)),acute_outcome_flags=dict(collections.Counter(r['readmission_footnote'] for r in ac)),acute_exposure_flags=dict(collections.Counter(r['exposure_footnote'] or '(blank)' for r in ac)),exposure_period=[ex['exposure_start'],ex['exposure_end']],outcome_period=[out['outcome_start'],out['outcome_end']],overlap_days=overlap,exact_period_matches_in_acute=sum(r['exact_period_match'] for r in ac),all_acute_discharge=summarize([r['discharge_percent'] for r in ac if r['discharge_percent'] is not None]),reliable_discharge=summarize([r['discharge_percent'] for r in ac if r['primary_reliable_exposure']]),survey_completions=summarize([r['completed_surveys'] for r in ac if r['completed_surveys'] is not None]),survey_response=summarize([r['survey_response_percent'] for r in ac if r['survey_response_percent'] is not None]),ownership=dict(collections.Counter(r['ownership'] for r in ac)),expansion='Not triggered: dataset-level period mismatch and no numeric hospital-wide outcomes; adding states cannot fix either barrier.',association=None)
 for minimum in [0,100,300]:
  vals=[r['discharge_percent'] for r in ac if r['discharge_percent'] is not None and r['completed_surveys'] is not None and r['completed_surveys']>=minimum and (minimum==0 or not r['exposure_footnote'])]
  summary.setdefault('sensitivity',{})[str(minimum)]=summarize(vals)
 d=ROOT/'data/derived';d.mkdir(exist_ok=True)
 with (d/'wisconsin_audit.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 (d/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 (ROOT/'site/pilot-data.json').write_text(json.dumps(dict(summary=summary,hospitals=ac),indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
