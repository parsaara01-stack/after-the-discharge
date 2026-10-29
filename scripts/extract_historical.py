"""Rebuild extracts from official archives; verify every archive, member and output hash."""
import csv,io,zipfile,json,pathlib,hashlib,urllib.request,argparse
root=pathlib.Path(__file__).resolve().parents[1];dest=root/'data/historical'
parser=argparse.ArgumentParser();parser.add_argument('--cache',type=pathlib.Path,default=root/'work/archive-cache');args=parser.parse_args();args.cache.mkdir(parents=True,exist_ok=True)
manifest=json.loads((dest/'manifest.json').read_text())
for name,item in zip(['general','survey','readmission'],manifest[:3]):
 path=args.cache/item['archive_url'].split('/')[-1]
 if not path.exists(): urllib.request.urlretrieve(item['archive_url'],path)
 blob=path.read_bytes();assert hashlib.sha256(blob).hexdigest()==item['archive_sha256']
 raw=zipfile.ZipFile(io.BytesIO(blob)).read(item['member']);assert hashlib.sha256(raw).hexdigest()==item['member_sha256']
 rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
 if name=='survey':rows=[r for r in rows if r['HCAHPS Measure ID']=='H_COMP_6_Y_P']
 if name=='readmission':rows=[r for r in rows if r['Measure ID']=='READM_30_HOSP_WIDE']
 assert len(rows)==len({r['Facility ID'] for r in rows})
 rows=[r for r in rows if r['State'] in ['WI','IL','IA','MI','MN']]
 output=io.StringIO(newline='');writer=csv.DictWriter(output,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)
 data=output.getvalue().encode();expected=next(m['sha256'] for m in manifest if m.get('extract')==name+'.csv');assert hashlib.sha256(data).hexdigest()==expected
 (dest/(name+'.csv')).write_bytes(data)
print('Official archives and all extracts verified')
