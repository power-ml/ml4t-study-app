#!/usr/bin/env python3
"""CORRECTNESS TEST — proves app/data.js answers are faithful to the source pool.

Independently re-parses the raw slices with a simple POSITIONAL (letter) mapping and compares
every choice's verdict to what data.js serves. Any difference must be an explicitly documented
override (overrides.json). Exit code 0 = all faithful; non-zero = a discrepancy to investigate.

Run:  python3 app/tests/verify_answers.py
"""
import json, re, glob, os, sys
APP=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT=os.path.dirname(APP)
data=json.loads(open(os.path.join(APP,'data.js')).read().replace('window.ML4T=','',1).rstrip(';\n'))
overrides=set(json.load(open(os.path.join(APP,'overrides.json'))).get('content_paired',{}).keys())

# independent positional parse of the source slices
src={}
for f in glob.glob(os.path.join(ROOT,'slices','*.txt')):
    for b in re.split(r'(?=\[(?:ML|QF)-D\d+G\d+Q\d+\])', open(f).read()):
        m=re.search(r'\[((?:ML|QF)-D\d+G\d+Q\d+)\]',b)
        if not m or 'Answer Key' not in b: continue
        key=b[b.find('Answer Key'):]
        vv={km.group(1):km.group(2) for km in re.finditer(r'(?m)^\s*([A-E])\.\s*(True|False)\b',key)}
        src[m.group(1)]=vv

checked=faithful=override_ok=fail=0
for q in data['questions']:
    sv=src.get(q['id'],{})
    for c in q['choices']:
        if c['L'] not in sv: continue
        checked+=1
        if c['verdict']==sv[c['L']]:
            faithful+=1
        elif q['id'] in overrides:
            override_ok+=1
        else:
            fail+=1
            print(f"MISMATCH (not an override): {q['id']} choice {c['L']} — data.js={c['verdict']} source(positional)={sv[c['L']]}")

print(f"choices checked: {checked}")
print(f"faithful to source (positional): {faithful}")
print(f"differs but is a documented override: {override_ok}  (expected: {sorted(overrides)})")
print(f"UNEXPECTED mismatches: {fail}")
print("RESULT:", "PASS ✅ every answer is faithful to the source (or a documented override)" if fail==0 else "FAIL ❌")
sys.exit(0 if fail==0 else 1)
