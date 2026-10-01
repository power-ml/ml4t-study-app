#!/usr/bin/env python3
"""Parse the 20 slice files (+ md cheat-sheets) into app/data.js for the study app.

CORRECTNESS-FIRST pairing: the pool's answer-key rationale restates the choice it
grades, so we pair each verdict to the choice by CONTENT (text similarity), not by
letter position. This is faithful even when the source key's letters are mislabeled
(e.g. ML-D6 G5Q5). Any question where content-pairing disagrees with letter-order,
or where a match is weak, is flagged so it can be verified against the PDF.

Reads slices/ + study_notes/ only; writes app/data.js only. Never edits source files.
"""
import re, glob, json, os, difflib
from pdf_text_cleanup import clean, garbled_chars   # repair PDF math-font mojibake (X₁, ŷ, •, …)
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
DOMNAMES={
 ('ML','01'):'Learning Paradigms & Problem Framing',('ML','02'):'Data & Sampling Discipline',
 ('ML','03'):'Feature Engineering & Leakage',('ML','04'):'Linear Models & Regression',
 ('ML','05'):'Instance-Based Learning (KNN)',('ML','06'):'Decision Trees',
 ('ML','07'):'Ensemble Methods',('ML','08'):'Model Evaluation & Metrics',
 ('ML','09'):'Overfitting, Underfitting & Generalization',('ML','10'):'Model Selection & Practical Tradeoffs',
 ('QF','01'):'Investment Returns & Compounding',('QF','02'):'Risk & Risk-Adjusted Performance',
 ('QF','03'):'Diversification & Correlation',('QF','04'):'Portfolio Optimization',
 ('QF','05'):'Market Microstructure & Trade Execution',('QF','06'):'Valuation & Mispricing',
 ('QF','07'):'CAPM, Alpha, Beta & Hedging',('QF','08'):'Market Efficiency & Arbitrage',
 ('QF','09'):'Financial Data & Research Bias',('QF','10'):'Quantitative Strategy Design & Evaluation'}
# domain -> course week(s) it's taught (confirmed 2026-09-29 from course_schedule.md; Exam 1 = wks 1-7)
WEEKS={('ML','01'):[1,3],('ML','02'):[1,2],('ML','03'):[1,3],('ML','04'):[3],('ML','05'):[5],
 ('ML','06'):[4],('ML','07'):[4],('ML','08'):[3,4],('ML','09'):[4,5],('ML','10'):[4,5],
 ('QF','01'):[1,2],('QF','02'):[2],('QF','03'):[2,3],('QF','04'):[3],('QF','05'):[5],
 ('QF','06'):[6],('QF','07'):[6,7],('QF','08'):[8],('QF','09'):[8],('QF','10'):[7,8]}
def norm(s): return re.sub(r'[^a-z0-9 ]',' ',(s or '').lower())
def sim(a,b): return difflib.SequenceMatcher(None,norm(a),norm(b)).ratio()
def md_section(md, header):
    m=re.search(r'(?m)^##\s+'+re.escape(header)+r'\s*\n(.*?)(?=\n##\s|\Z)', md, re.S)
    return m.group(1).strip() if m else ''
def find_md(part,num):
    g=glob.glob(os.path.join(ROOT,'study_notes',part,f'Domain_{num}_*.md')); return open(g[0]).read() if g else ''

def parse_md_questions(md):
    """From a domain study-note md, return {qid: {'why':{L:text}, 'ref':str}} using the
    per-question '### [ID]' blocks and their | Choice | Verdict | Why | tables. Used to
    surface the EXPANDED explanations in the app. Verdict column is ignored (authoritative
    verdicts come from the source pool); only the 'Why' text and Reference are taken."""
    out={}
    for m in re.finditer(r'###\s*\[((?:ML|QF)-D\d+G\d+Q\d+)\](.*?)(?=\n###\s|\n##\s|\Z)', md, re.S):
        qid=m.group(1); body=m.group(2); why={}
        # first cell may be bare "A" or "A. <choice text>"; ignore verdict col; take Why col
        for row in re.finditer(r'(?m)^\|\s*([A-E])[.\)]?[^|]*\|[^|]*\|\s*(.*?)\s*\|\s*$', body):
            why[row.group(1)]=row.group(2).strip()
        refm=re.search(r'\*\*Reference:\*\*\s*(.+)', body)
        out[qid]={'why':why,'ref':refm.group(1).strip() if refm else ''}
    return out

def pair_by_content(stmts, keys):
    """Greedy best-similarity 1-1 assignment. Used ONLY for verified-mislabeled qids
    (overrides.content_paired), where the source rationale verbatim-restates the choice."""
    cand=[]
    for (kL,v,rat) in keys:
        for sL,st in stmts.items():
            cand.append((sim(rat,st), sL, kL, v, rat))
    cand.sort(reverse=True)
    assigned={}; usedK=set(); usedS=set()
    for score,sL,kL,v,rat in cand:
        if sL in usedS or kL in usedK: continue
        assigned[sL]=(v,rat,kL,round(score,2)); usedS.add(sL); usedK.add(kL)
    return assigned

def detect_mislabel(stmts, keys):
    """High-precision detector: flags a question only when some key's rationale clearly
    restates a DIFFERENT choice (sim>=0.80) far better than its own letter (own<0.55).
    Catches verbatim-restatement letter typos WITHOUT flagging normal paraphrase rationales."""
    for (kL,v,rat) in keys:
        own=sim(rat,stmts.get(kL,''))
        best=max(((sim(rat,st),sL) for sL,st in stmts.items()), default=(0,None))
        if best[1] and best[1]!=kL and best[0]>=0.80 and own<0.55:
            return True
    return False

OVR=json.load(open(os.path.join(HERE,'overrides.json'))).get('content_paired',{})
# Questions withdrawn from the official exam pool — kept for completeness but flagged so they can be skipped in study.
WITHDRAWN={'ML-D1G2Q8','ML-D2G4Q5','ML-D3G1Q4','ML-D3G3Q6','ML-D5G5Q4','ML-D6G4Q6','ML-D6G5Q5','ML-D6G5Q6','QF-D8G4Q1'}
questions=[]; domains=[]; suspects=[]; overridden=[]; seen_sig={}; expanded_full=0
for f in sorted(glob.glob(os.path.join(ROOT,'slices','*.txt'))):
    base=os.path.basename(f); part='ML' if base.startswith('ML_') else 'QF'
    num=re.search(r'_D(\d\d)',base).group(1); md=find_md(part,num); mdq=parse_md_questions(md)
    domains.append({'part':part,'num':num,'name':DOMNAMES[(part,num)],
        'weeks':WEEKS[(part,num)],'weekMax':max(WEEKS[(part,num)]),
        'cheatsheet':md_section(md,'Domain cheat-sheet'),'traps':md_section(md,'Common traps'),
        'references':md_section(md,'References (domain-level)')})
    for b in re.split(r'(?=\[(?:ML|QF)-D\d+G\d+Q\d+\])', open(f).read()):
        mm=re.search(r'\[((?:ML|QF)-D(\d+)G(\d+)Q(\d+))\]',b)
        if not mm or 'Answer Key' not in b: continue
        qid=mm.group(1); grp='G'+mm.group(3)
        inverted=('True = incorrect' in b or 'True=incorrect' in b)
        ks=b.find('Answer Key'); head=b[b.find(']')+1:ks]; key=b[ks:]
        scen=re.sub(r'\s+',' ',re.split(r'(?m)^\s*A\.\s',head)[0]).strip()
        stmts={}
        for cm in re.finditer(r'(?m)^\s*([A-E])\.\s*(.*?)(?=\n\s*[A-E]\.\s|\Z)',head,re.S):
            stmts[cm.group(1)]=re.sub(r'\s+',' ',cm.group(2)).strip()
        keys=[(km.group(1),km.group(2),re.sub(r'\s+',' ',km.group(3)).strip())
              for km in re.finditer(r'(?m)^\s*([A-E])\.\s*(True|False)\s*[–\-:]?\s*(.*?)(?=\n\s*[A-E]\.\s(?:True|False)|\Z)',key,re.S)]
        if len(stmts)<3 or len(keys)<3: continue
        keymap={kL:(v,rat) for kL,v,rat in keys}
        choices=[]
        if qid in OVR:                                   # verified mislabel → content pairing
            assigned=pair_by_content(stmts,keys); overridden.append(qid)
            for L in sorted(stmts):
                if L not in assigned: continue
                v,rat,kL,score=assigned[L]
                choices.append({'L':L,'text':stmts[L],'verdict':v,'accurate':(v=='True')^inverted,'why':rat})
        else:                                            # DEFAULT: positional (letter) pairing
            for L in sorted(stmts):
                if L not in keymap: continue
                v,rat=keymap[L]
                choices.append({'L':L,'text':stmts[L],'verdict':v,'accurate':(v=='True')^inverted,'why':rat})
        q={'id':qid,'part':part,'domain':num,'domainName':DOMNAMES[(part,num)],'group':grp,
           'weeks':WEEKS[(part,num)],'weekMax':max(WEEKS[(part,num)]),
           'polarity':'inverted' if inverted else 'normal','scenario':scen,'choices':choices}
        if qid in OVR:
            q['flag']='source-key letters were mislabeled — corrected & verified vs PDF'
        elif detect_mislabel(stmts,keys):
            q['flag']='possible source-key mislabel — VERIFY vs PDF'; suspects.append(qid)
        ex=mdq.get(qid,{})
        for c in q['choices']:
            c['whyPool']=c['why']
            if ex.get('why',{}).get(c['L']): c['why']=ex['why'][c['L']]
        if ex.get('ref'): q['reference']=ex['ref']
        if sum(1 for c in q['choices'] if ex.get('why',{}).get(c['L']))==len(q['choices']): expanded_full+=1
        sig=scen+'||'+'||'.join(c['text'] for c in choices)
        if sig in seen_sig: q['duplicateOf']=seen_sig[sig]
        else: seen_sig[sig]=qid
        if qid in WITHDRAWN: q['withdrawn']=True
        # --- repair PDF math-font mojibake in all displayed text; flag any residual we can't safely fix ---
        q['scenario']=clean(q['scenario'])
        for c in q['choices']:
            c['text']=clean(c['text']); c['why']=clean(c.get('why','')); c['whyPool']=clean(c.get('whyPool',''))
        if q.get('reference'): q['reference']=clean(q['reference'])
        blob=q['scenario']+' '+' '.join(c['text']+' '+c['why'] for c in q['choices'])
        g=garbled_chars(blob)
        if g: q['pdfArtifacts']=g
        questions.append(q)

# ---- attach distilled book-note references to domains (via 'ML/QF Domain N' tags in each note) ----
reffiles=[]
for p in sorted(glob.glob(os.path.join(ROOT,'references','*','*.md'))):
    txt=open(p).read(); book=os.path.basename(os.path.dirname(p))
    tm=re.search(r'^#\s*(.+)',txt,re.M); title=tm.group(1).strip() if tm else os.path.basename(p)
    doms={(a,int(b)) for a,b in re.findall(r'\b(ML|QF)\s*Domain\s*(\d+)',txt)}
    reffiles.append({'book':book,'title':title,'file':os.path.relpath(p,ROOT),'md':txt,'doms':doms})
for d in domains:
    key=(d['part'],int(d['num']))
    d['bookNotes']=[{'book':r['book'],'title':r['title'],'file':r['file'],'md':r['md']} for r in reffiles if key in r['doms']]
print('reference files:',len(reffiles),'| domains with book notes:',sum(1 for d in domains if d.get('bookNotes')))

heur={'absolute_false_pct':74,'negation_inacc_pct':69,'accurate_base_pct':58,
      'positional':{'A':75,'B':63,'C':47,'D':53,'E':50},
      'inverted_total':sum(1 for q in questions if q['polarity']=='inverted')}
for i,q in enumerate(questions,1): q['n']=i   # stable global question number (survives filters/reorder)
data={'generated':'2026-10-01','counts':{'questions':len(questions),
      'ML':sum(1 for q in questions if q['part']=='ML'),'QF':sum(1 for q in questions if q['part']=='QF'),
      'withdrawn':sum(1 for q in questions if q.get('withdrawn')),
      'pdfArtifacts':sum(1 for q in questions if q.get('pdfArtifacts'))},
      'heuristics':heur,'domains':domains,'questions':questions,
      'overridden':overridden,'suspects':suspects,'withdrawn':sorted(WITHDRAWN)}
open(os.path.join(HERE,'data.js'),'w').write('window.ML4T='+json.dumps(data,ensure_ascii=False)+';')
dups=[q['id'] for q in questions if q.get('duplicateOf')]
print('questions:',len(questions),'| inverted',heur['inverted_total'])
print('expanded-why coverage (all 5 choices):',expanded_full,'/',len(questions))
print('duplicates marked:',dups)
_wfound=sorted(q['id'] for q in questions if q.get('withdrawn')); _wmiss=sorted(WITHDRAWN-set(_wfound))
print('withdrawn marked:',len(_wfound),_wfound,('| MISSING(not in pool!): '+str(_wmiss)) if _wmiss else '')
_art=[q['id'] for q in questions if q.get('pdfArtifacts')]
print('pdf-mojibake repaired across all Qs; residual-garble flagged on',len(_art),'questions:',_art)
print('overridden (verified mislabels, content-paired):',overridden)
print('NEW suspects to verify vs PDF:',suspects if suspects else 'none 🎉')
q=[x for x in questions if x['id']=='ML-D6G5Q5'][0]
print('ML-D6G5Q5 verdicts:', {c['L']:c['verdict'] for c in q['choices']})
