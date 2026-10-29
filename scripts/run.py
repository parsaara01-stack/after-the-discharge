#!/usr/bin/env python3
import functools,http.server,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(ROOT/'scripts/check.py')],check=True)
print('After the Discharge: http://127.0.0.1:8027',flush=True)
http.server.ThreadingHTTPServer(('127.0.0.1',8027),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT/'site'))).serve_forever()
