#!/usr/bin/env python3
"""Apply the recorded math-formula fixes (content/math_fixes.json) to the content files.

The pool PDF's math font has a broken text map, so formulas with sub/superscripts, sums, hats or
fractions were extracted as garbage glyphs. Each fix in math_fixes.json was transcribed from the
rendered PDF page image and replaces one exact span of text:
    {"qid", "file" (relative to content/), "original", "corrected", "page", "note"}

Idempotent and strict: a fix is applied only when `original` occurs exactly once; if `corrected`
is already present it is skipped; anything else is reported and the script exits non-zero.
Verdict words (True/False) are checked to be unchanged by every fix.

Usage: python3 tools/apply_math_fixes.py [--check]
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(os.path.dirname(HERE), 'content')
VERDICT = re.compile(r'\b(True|False)\b')


def main(check_only=False):
    fixes = json.load(open(os.path.join(CONTENT, 'math_fixes.json')))
    texts, applied, skipped, bad = {}, 0, 0, []
    for i, f in enumerate(fixes):
        path = os.path.join(CONTENT, f['file'])
        s = texts.setdefault(path, open(path).read())
        if VERDICT.findall(f['original']) != VERDICT.findall(f['corrected']):
            bad.append((i, f['qid'], 'verdict words differ')); continue
        n = s.count(f['original'])
        if n == 1:
            texts[path] = s.replace(f['original'], f['corrected']); applied += 1
        elif n == 0 and f['corrected'] in s:
            skipped += 1
        else:
            bad.append((i, f['qid'], f'original found {n}x'))
    print(f'fixes: {len(fixes)} | applied {applied} | already applied {skipped} | problems {len(bad)}')
    for b in bad:
        print('  PROBLEM', b)
    if bad:
        sys.exit(1)
    if not check_only:
        for path, s in texts.items():
            open(path, 'w').write(s)


if __name__ == '__main__':
    main('--check' in sys.argv)
