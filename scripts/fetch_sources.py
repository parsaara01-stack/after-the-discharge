#!/usr/bin/env python3
"""Fetch immutable CMS snapshot. Standard library only; --refresh explicitly replaces it."""
import argparse,datetime,hashlib,json,pathlib,urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--refresh',action='store_true');a=p.parse_args()
manifest_path=ROOT/'data/source_manifest.json'
if manifest_path.exists() and not a.refresh:
 print('Snapshot exists; use --refresh for a new release (then re-audit protocol).');raise SystemExit
records=[]
def fetch(url,path,**meta):
 req=urllib.request.Request(url,headers={'User-Agent':'AfterTheDischargeResearch/0.1 (public CMS aggregate pilot)'})
 with urllib.request.urlopen(req,timeout=90) as response: b=response.read();headers=dict(response.headers)
 (ROOT/path).write_bytes(b)
 row=dict(path=path,url=url,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),http_last_modified=headers.get('Last-Modified'),**meta)
 records.append(row);return b
for dataset in ['632h-zaca','dgck-syfz','xubh-q36u','y9us-9xdf','4j6d-yzce']:
 url='https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items/'+dataset
 d=json.loads(fetch(url,'data/raw/'+dataset+'.json',kind='catalog metadata'))
 fetch(d['distribution'][0]['downloadURL'],'data/raw/'+dataset+'.csv',kind='data',dataset_id=dataset,title=d['title'],cms_modified=d['modified'],cms_released=d['released'])
fetch(d['distribution'][0]['describedBy'],'data/raw/HOSPITAL_Data_Dictionary.pdf',kind='dictionary')
fetch('https://hcahpsonline.org/globalassets/hcahps/podcasts/hcahps-program-updates-changes-to-survey-content-and-survey-protocol-podcast-script.pdf','data/raw/hcahps-2025-changes.pdf',kind='official survey methods')
fetch('https://hcahpsonline.org/globalassets/hcahps/training-materials/2025_training-materials_slides.pdf','data/raw/hcahps-2025-training.pdf',kind='official training and reporting timeline')
manifest_path.write_text(json.dumps(records,indent=2)+'\n')
for r in records:print(r['path'],r['bytes'],r['sha256'])
