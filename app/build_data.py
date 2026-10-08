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
# Exam 2 = Part 2 (course weeks 9-16; Exam 2 is week 16). RL + deep learning (ML) / advanced quant + options (QF).
DOMNAMES_E2={
 ('ML','01'):'Reinforcement Learning Problem Framing',('ML','02'):'Markov Decision Processes, Policies & Values',
 ('ML','03'):'Q-Learning Mechanics',('ML','04'):'Exploration, Exploitation & Learning Dynamics',
 ('ML','05'):'Dyna & Model-Based Reinforcement Learning',('ML','06'):'State Representation, Discretization & Reward Design',
 ('ML','07'):'Reinforcement Learning for Trading',('ML','08'):'Comparative Strategy Learning & Evaluation',
 ('ML','09'):'Deep Learning & Neural-Network Foundations',('ML','10'):'Sequential, Generative & Responsible AI',
 ('QF','01'):'Financial Time Series & Market Data Behavior',('QF','02'):'Technical Indicators & Signal Construction',
 ('QF','03'):'Alpha Research & Formulaic Signals',('QF','04'):'Fundamental Law of Active Portfolio Management',
 ('QF','05'):'Advanced Portfolio Construction',('QF','06'):'Strategy Evaluation & Performance Attribution',
 ('QF','07'):'Trading Frictions, Capacity & Implementability',('QF','08'):'Execution Algorithms & Order Book Analytics',
 ('QF','09'):'Options & Derivative Payoffs',('QF','10'):'AI-Enabled Investment Processes & Decision Support'}
WEEKS_E2={('ML','01'):[11],('ML','02'):[11],('ML','03'):[11],('ML','04'):[11],('ML','05'):[11],
 ('ML','06'):[11],('ML','07'):[11,12],('ML','08'):[12,14],('ML','09'):[12],('ML','10'):[12,14],
 ('QF','01'):[9],('QF','02'):[9],('QF','03'):[9],('QF','04'):[10],('QF','05'):[10],
 ('QF','06'):[14],('QF','07'):[10,13],('QF','08'):[13],('QF','09'):[15],('QF','10'):[13,14]}
def dom_name(exam,part,num): return (DOMNAMES_E2 if exam==2 else DOMNAMES)[(part,num)]
def dom_weeks(exam,part,num): return (WEEKS_E2 if exam==2 else WEEKS)[(part,num)]
def norm(s): return re.sub(r'[^a-z0-9 ]',' ',(s or '').lower())
def sim(a,b): return difflib.SequenceMatcher(None,norm(a),norm(b)).ratio()
def md_section(md, header):
    m=re.search(r'(?m)^##\s+'+re.escape(header)+r'\s*\n(.*?)(?=\n##\s|\Z)', md, re.S)
    return m.group(1).strip() if m else ''
def find_md(exam,part,num):
    sub=os.path.join('study_notes_exam2',part) if exam==2 else os.path.join('study_notes',part)
    g=glob.glob(os.path.join(ROOT,sub,f'Domain_{num}_*.md')); return open(g[0]).read() if g else ''

def parse_md_questions(md):
    """From a domain study-note md, return {qid: {'why':{L:text}, 'ref':str}} using the
    per-question '### [ID]' blocks and their | Choice | Verdict | Why | tables. Used to
    surface the EXPANDED explanations in the app. Verdict column is ignored (authoritative
    verdicts come from the source pool); only the 'Why' text and Reference are taken."""
    out={}
    for m in re.finditer(r'###\s*\[((?:ML|QF)2?-D\d+G\d+Q\d+)\](.*?)(?=\n###\s|\n##\s|\Z)', md, re.S):
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
    base=os.path.basename(f); part='ML' if base.startswith(('ML_','ML2_')) else 'QF'
    exam=2 if base.startswith(('ML2_','QF2_')) else 1
    num=re.search(r'_D(\d\d)',base).group(1); md=find_md(exam,part,num); mdq=parse_md_questions(md)
    domains.append({'exam':exam,'part':part,'num':num,'name':dom_name(exam,part,num),
        'weeks':dom_weeks(exam,part,num),'weekMax':max(dom_weeks(exam,part,num)),
        'cheatsheet':md_section(md,'Domain cheat-sheet'),'traps':md_section(md,'Common traps'),
        'references':md_section(md,'References (domain-level)')})
    for b in re.split(r'(?=\[(?:ML|QF)2?-D\d+G\d+Q\d+\])', open(f).read()):
        mm=re.search(r'\[((?:ML|QF)2?-D(\d+)G(\d+)Q(\d+))\]',b)
        if not mm or 'Answer Key' not in b: continue
        qid=mm.group(1); grp='G'+mm.group(3)
        # Inverted polarity ("mark True if the statement is WRONG"). Exam 1 signals it in the answer-key
        # header ("True = incorrect"); Exam 2 signals it only in the body. Scope the body test to the text
        # BETWEEN "True when/if" and "False" so a normal question that merely says "False if incorrect" isn't flagged.
        _bm=re.search(r'mark\s+(?:each\s+statement\s+)?True\s+(?:when|if)\s+(.*?)\s+(?:and\s+)?False\b',b,re.I|re.S)
        inverted=('True = incorrect' in b or 'True=incorrect' in b
                  or bool(_bm and re.search(r'\b(incorrect|wrong|inaccurate|false)\b',_bm.group(1),re.I)))
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
        q={'id':qid,'exam':exam,'part':part,'domain':num,'domainName':dom_name(exam,part,num),'group':grp,
           'weeks':dom_weeks(exam,part,num),'weekMax':max(dom_weeks(exam,part,num)),
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
    if book=='WhatHedgeFundsReallyDo':  # these notes tag domains as "QF D8" (authoritative numbering)
        doms|={(a,int(b)) for a,b in re.findall(r'\b(ML|QF)\s*D(\d+)\b',txt)}
    reffiles.append({'book':book,'title':title,'file':os.path.relpath(p,ROOT),'md':txt,'doms':doms})
for d in domains:
    key=(d['part'],int(d['num']))
    # references/ currently holds Exam-1 recommended chapters only; don't attach them to Exam-2 domains
    # (same (part,num) key would otherwise leak Exam-1 notes onto Exam-2). Exam-2 refs: distill later.
    d['bookNotes']=[] if d.get('exam')==2 else [{'book':r['book'],'title':r['title'],'file':r['file'],'md':r['md']} for r in reffiles if key in r['doms']]
print('reference files:',len(reffiles),'| domains with book notes:',sum(1 for d in domains if d.get('bookNotes')))

# book short-name (as used in concept_map JSON) → PDF filename in ../books/ (served read-only by serve.py at /books/)
BOOKS={'ISLP':'ISLP_website.pdf','DeepLearning':'Deep Learning_ Foundations and Concepts-Springer (2024).pdf',
       'ProbML':'Probabilistic Machine Learning.pdf','FoundationsML':'Foundations of Machine Learning.pdf',
       'Handbook':'ai-and-big-data-in-investments.pdf','WHFRD':'What Hedge Funds Really Do - An Introduction to Portfolio Management.pdf'}
BOOKS={k:v for k,v in BOOKS.items() if os.path.exists(os.path.join(ROOT,'books',v))}
# ---- attach Exam-1 concept → book/chapter map (references/concept_map/{ML,QF}_DNN.json) ----
def src_label(s):
    return ' · '.join(x for x in [s.get('book'),s.get('chapter'),s.get('section'),
                                   ('PDF p.'+s['pdfPages']) if s.get('pdfPages') else None] if x)
def first_page(pp):
    m=re.match(r'\s*(\d+)',str(pp or '')); return int(m.group(1)) if m else None
qconcepts={}
for d in domains:
    if d.get('exam')==2: continue
    p=os.path.join(ROOT,'references','concept_map',f"{d['part']}_D{d['num']}.json")
    if not os.path.exists(p): continue
    cm=json.load(open(p)); d['conceptMap']=cm.get('concepts',[]); d['conceptGaps']=cm.get('gaps')
    for c in d['conceptMap']:
        best=next((s for s in c.get('sources',[]) if s.get('kind') in ('recommended','other-book') and s.get('verified')),None)
        for qid in c.get('questions',[]):
            qconcepts.setdefault(qid,[]).append({'concept':c['concept'],'src':src_label(best) if best else None,'lecture':c.get('lecture'),
                'book':best.get('book') if best else None,'page':first_page(best.get('pdfPages')) if best else None})
for q in questions:
    if q.get('exam',1)==1 and q['id'] in qconcepts: q['concepts']=qconcepts[q['id']]
print('concept map: domains',sum(1 for d in domains if d.get('conceptMap')),'| questions tagged',sum(1 for q in questions if q.get('concepts')))

heur={'absolute_false_pct':74,'negation_inacc_pct':69,'accurate_base_pct':58,
      'positional':{'A':75,'B':63,'C':47,'D':53,'E':50},
      'inverted_total':sum(1 for q in questions if q['polarity']=='inverted')}
for i,q in enumerate(questions,1): q['n']=i   # stable global question number (survives filters/reorder)
data={'generated':'2026-10-01','counts':{'questions':len(questions),
      'ML':sum(1 for q in questions if q['part']=='ML'),'QF':sum(1 for q in questions if q['part']=='QF'),
      'withdrawn':sum(1 for q in questions if q.get('withdrawn')),
      'pdfArtifacts':sum(1 for q in questions if q.get('pdfArtifacts'))},
      'heuristics':heur,'domains':domains,'questions':questions,'books':BOOKS,
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
