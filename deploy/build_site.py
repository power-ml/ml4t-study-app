#!/usr/bin/env python3
"""Assemble the files to upload for hosted mode: app/index.html + app/data.js + the two sign-in pages,
each with the (non-secret) Cognito settings injected. Book PDFs and personal data are never included.
Usage: python3 deploy/build_site.py --out deploy/build --domain <cognito domain> --client <app client id>"""
import argparse, json, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); APP = os.path.join(os.path.dirname(HERE), 'app')
ap = argparse.ArgumentParser(); ap.add_argument('--out', required=True); ap.add_argument('--domain', required=True); ap.add_argument('--client', required=True)
a = ap.parse_args()
cfg = '<script>window.ML4T_HOSTED=' + json.dumps({'domain': a.domain, 'clientId': a.client}) + ';</script>'
os.makedirs(a.out, exist_ok=True)
idx = open(os.path.join(APP, 'index.html')).read()
assert '<script src="data.js"></script>' in idx
open(os.path.join(a.out, 'index.html'), 'w').write(idx.replace('<script src="data.js"></script>', cfg + '\n<script src="data.js"></script>', 1))
shutil.copy(os.path.join(APP, 'data.js'), os.path.join(a.out, 'data.js'))
for page in ('login.html', 'callback.html'):
    t = open(os.path.join(HERE, 'web', page)).read(); assert '<!--ML4T_CONFIG-->' in t
    open(os.path.join(a.out, page), 'w').write(t.replace('<!--ML4T_CONFIG-->', cfg))
print('built', sorted(os.listdir(a.out)), '→', a.out)
