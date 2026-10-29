#!/usr/bin/env python3
"""Restore the exact pinned national files and dictionaries, validating every hash."""
import hashlib,json,pathlib,urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
for row in json.loads((ROOT/'data/source_manifest.json').read_text()):
 p=ROOT/row['path'];p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']:continue
 b=urllib.request.urlopen(row['url'],timeout=120).read()
 assert hashlib.sha256(b).hexdigest()==row['sha256'],'Source changed at '+row['url']
 p.write_bytes(b);print('Restored',row['path'])
