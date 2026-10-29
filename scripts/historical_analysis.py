"""Matched-year analysis. Requires numpy. Inputs: pinned public CMS extracts."""
import csv,json,pathlib,collections
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
def read(n):return list(csv.DictReader((ROOT/'data/historical'/f'{n}.csv').open()))
def num(v):
 try:return float(v)
 except:return None
g=read('general');h={r['Facility ID']:r for r in read('survey')};o={r['Facility ID']:r for r in read('readmission')}
def cohort(states):
 rows=[];funnel=collections.Counter()
 for r in g:
  if r['State'] not in states:continue
  funnel['Listed']+=1
  if r['Hospital Type']!='Acute Care Hospitals':continue
  funnel['Acute Care']+=1
  a=h.get(r['Facility ID']);b=o.get(r['Facility ID'])
  if not a or not b:continue
  funnel['Both Measures']+=1
  if num(a['HCAHPS Answer Percent']) is None or num(b['Score']) is None:continue
  funnel['Numeric Pair']+=1
  if num(a['Number of Completed Surveys']) is None or num(a['Number of Completed Surveys'])<100 or a['HCAHPS Answer Percent Footnote'] or b['Footnote']:continue
  funnel['Reliable Unflagged Pair']+=1
  if (a['Start Date'],a['End Date'])!=(b['Start Date'],b['End Date']):continue
  assert a['Start Date']=='07/01/2022' and a['End Date']=='06/30/2023'
  funnel['Matched Year']+=1
  rows.append(dict(id=r['Facility ID'],state=r['State'],name=r['Facility Name'],ownership=r['Hospital Ownership'],discharge=float(a['HCAHPS Answer Percent']),readmission=float(b['Score']),surveys=int(a['Number of Completed Surveys']),response=num(a['Survey Response Rate Percent']),denominator=num(b['Denominator']),lower=num(b['Lower Estimate']),upper=num(b['Higher Estimate'])))
 return rows,dict(funnel)
def ranks(x):return np.array([sum(x<v)+(sum(x==v)+1)/2 for v in x])
def stats(rows):
 x=np.array([r['discharge'] for r in rows]);y=np.array([r['readmission'] for r in rows]);rng=np.random.default_rng(20261029)
 def calc(a,b):return np.corrcoef(a,b)[0,1],5*np.sum((a-a.mean())*(b-b.mean()))/np.sum((a-a.mean())**2)
 boots=np.array([calc(x[ix],y[ix]) for ix in rng.integers(0,len(x),(10000,len(x)))])
 r,slope=calc(x,y)
 return dict(n=len(rows),pearson=float(r),slope_per_5pp=float(slope),pearson_ci=np.quantile(boots[:,0],[.025,.975]).tolist(),slope_ci=np.quantile(boots[:,1],[.025,.975]).tolist(),spearman=float(np.corrcoef(ranks(x),ranks(y))[0,1]),discharge_range=[min(x),max(x)],readmission_range=[min(y),max(y)])
wi,wf=cohort(['WI']);rows,funnel=(wi,wf) if len(wi)>=60 else cohort(['WI','IL','IA','MI','MN'])
assert len(rows)>=60
result=dict(period=['2022-07-01','2023-06-30'],wisconsin_funnel=wf,analysis_funnel=funnel,states=dict(collections.Counter(r['state'] for r in rows)),primary=stats(rows),survey300=stats([r for r in rows if r['surveys']>=300]),ownership=dict(collections.Counter(r['ownership'] for r in rows)),hospitals=rows)
(ROOT/'data/historical/results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='hospitals'},indent=2))
