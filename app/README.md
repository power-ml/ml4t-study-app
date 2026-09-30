# ML4T Exam 1 — Study App

A local, dependency-free study app over the 518-question pool + the domain study notes.
**Additive & non-destructive:** it only reads `../slices/` and `../study_notes/`, and only writes inside `../notes/`.

## Run locally (recommended — notes persist to files)
```bash
cd projects/ml4t_prep/app
python3 serve.py            # prints http://127.0.0.1:8765/
```
Open the printed URL. Notes + quiz progress save to `../notes/ml4t_state.json` and a readable `../notes/ml4t_notes.md`.

(You can also just double-click `index.html` — it still works, but notes then live in the browser only.)


## Regenerate the data (after editing slices/study notes)
```bash
python3 build_data.py       # rewrites data.js from ../slices/*.txt + ../study_notes/**
```

## Features
- **Study**: browse by part/domain/group; per-question scenario, choices with the authoritative verdict + expanded "why", auto trap-flags (absolute/negation words), inverted-polarity banner, and a per-domain **Deep dive** (cheat-sheet + common traps + references).
- **Quiz / Mock**: Smart (unseen/missed first), Trap drill, Random, or Exam simulator (40 Q, 2/domain). Scored the real way — 1 pt/correct choice; all-5-same = 0.
- **My Notes**: all notes at a glance; inline note box on every question (saved to file).
- **Readiness**: per-domain accuracy heatmap (RAG), overall %, weakest-domain recommendations, export/import progress.
- **Heuristics**: the data-mined answer patterns (absolutes ~74% False, negation ~69% inaccurate, positional skew, 95 inverted).

