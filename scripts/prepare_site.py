#!/usr/bin/env python3
import pathlib,shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
 d=ROOT/'site/downloads';d.mkdir(exist_ok=True)
 for source in ['docs/protocol.md','docs/methods.md','docs/data-dictionary.md','docs/evidence.csv','data/source_manifest.json','data/derived/wisconsin_audit.csv','data/derived/summary.json']:
  shutil.copyfile(ROOT/source,d/pathlib.Path(source).name)
if __name__=='__main__':main()
