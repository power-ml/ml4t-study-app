#!/usr/bin/env python3
"""Slice the Exam-2 (Part 2) question pool out of pool.txt into per-domain slice files.

The pool already tags each Part-2 question with a full bracket id ([ML2-D1G1Q1], [QF2-D3G2Q4], …)
and a per-question "Answer Key:" block — same structure build_data.py already parses for Exam 1.
So slicing = bucket each question block by the domain number in its id, prepend the domain header,
and write slices/ML2_D0N.txt / slices/QF2_D0N.txt. Idempotent; safe to re-run.

Usage:  python3 tools/slice_pool.py /path/to/pool.txt
"""
import sys, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(os.path.dirname(HERE), 'content')
# pool.txt = text extracted from the course's question-pool PDF (not shipped); pass its path as argv[1]
POOL = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'pool.txt')
SLICES = os.path.join(ROOT, 'slices')

TITLES = {
    'ML2': {1: 'Reinforcement Learning Problem Framing', 2: 'Markov Decision Processes, Policies, and Values',
            3: 'Q-Learning Mechanics', 4: 'Exploration, Exploitation, and Learning Dynamics',
            5: 'Dyna and Model-Based Reinforcement Learning', 6: 'State Representation, Discretization, and Reward Design',
            7: 'Reinforcement Learning for Trading', 8: 'Comparative Strategy Learning and Evaluation',
            9: 'Deep Learning and Neural-Network Foundations', 10: 'Sequential, Generative, and Responsible AI'},
    'QF2': {1: 'Financial Time Series and Market Data Behavior', 2: 'Technical Indicators and Signal Construction',
            3: 'Alpha Research and Formulaic Signals', 4: 'Fundamental Law of Active Portfolio Management',
            5: 'Advanced Portfolio Construction', 6: 'Strategy Evaluation and Performance Attribution',
            7: 'Trading Frictions, Capacity, and Implementability', 8: 'Execution Algorithms and Order Book Analytics',
            9: 'Options and Derivative Payoffs', 10: 'AI-Enabled Investment Processes and Decision Support'},
}


def main():
    text = open(POOL, encoding='utf-8').read()
    os.makedirs(SLICES, exist_ok=True)
    # Split the whole pool into question blocks on the Part-2 bracket ids; bucket by (prefix, domain).
    blocks = re.split(r'(?=\[(?:ML2|QF2)-D\d+G\d+Q\d+\])', text)
    buckets = {}  # (prefix, dnum) -> list of blocks
    for b in blocks:
        m = re.match(r'\[(ML2|QF2)-D(\d+)G\d+Q\d+\]', b)
        if not m or 'Answer Key' not in b:
            continue
        key = (m.group(1), int(m.group(2)))
        buckets.setdefault(key, []).append(b.rstrip() + '\n')

    written = []
    for prefix in ('ML2', 'QF2'):
        for d in range(1, 11):
            qs = buckets.get((prefix, d), [])
            if not qs:
                print(f"  !! no questions found for {prefix} Domain {d}")
                continue
            header = f"Domain {d}: {TITLES[prefix][d]}\n\n"
            path = os.path.join(SLICES, f"{prefix}_D{d:02d}.txt")
            open(path, 'w', encoding='utf-8').write(header + '\n'.join(qs))
            nq = sum(len(re.findall(r'\[(?:ML2|QF2)-D\d+G\d+Q\d+\]', q)) for q in qs)
            written.append((os.path.basename(path), nq))

    total = sum(n for _, n in written)
    for name, n in written:
        print(f"  {name}: {n} questions")
    print(f"wrote {len(written)} Exam-2 slice files, {total} questions total")


if __name__ == '__main__':
    main()
