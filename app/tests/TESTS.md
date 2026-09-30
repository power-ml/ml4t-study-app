# ML4T Study App — Tests & Validation

Two automated tests + a manual checklist. The most important is **verify_answers.py** — it proves the
answers the app shows are faithful to the source pool.

## 1. Answer-fidelity test (run this — it's the correctness guarantee)
```bash
cd projects/ml4t_prep
python3 app/tests/verify_answers.py
```
**Expected:** `RESULT: PASS ✅`, with `UNEXPECTED mismatches: 0` and exactly 2 documented-override
differences (the two swapped choices in `ML-D6G5Q5`). It independently re-parses the raw `slices/` with a
positional letter→verdict mapping and compares every one of the 2,590 choices to what `data.js` serves.
Any answer that drifted from the source (other than a documented override) fails the test.

## 2. Headless UI smoke test (verifies the client JS runs error-free)
Needs the server running + Playwright/Chromium.
```bash
# terminal 1
cd projects/ml4t_prep/app && python3 serve.py
# terminal 2 (from a dir with playwright installed, or: npm i playwright && npx playwright install chromium)
node projects/ml4t_prep/app/tests/headless_smoke.mjs
```
**Expected:** `RESULT: PASS ✅`, `errors: []`, `studyCards > 0`, `quizCards = 10`.

## 3. Manual checklist (5 minutes in the browser)
Open http://127.0.0.1:8765/ (after `serve.py`) and confirm:
- [ ] **Answer-key spot-check:** Study → search `ML-D6G5Q5`. It shows a ⚠ "corrected & verified" banner; verdicts read **A True, B False, C True, D True, E True**. (Optionally open the PDF pool and confirm.)
- [ ] **Pick 3 random questions**, reveal answers, and confirm the True/False matches the PDF pool exactly.
- [ ] **Inverted polarity:** open any ML question with the amber "INVERTED" banner — the "why" should read as "True = the statement is WRONG."
- [ ] **Quiz scoring:** Quiz → Random, 10 → answer some → Submit. Confirm a score appears. Mark ALL 5 of one question the same (all True) → that question is called out as scored **0** (the real-exam all-5 rule).
- [ ] **Notes persist to file:** add a note on any question → check `projects/ml4t_prep/notes/ml4t_state.json` and `notes/ml4t_notes.md` updated. Reload the page → the note is still there.
- [ ] **Tables render** in a Deep-dive panel (no raw `|` pipes).
- [ ] **Readiness heatmap** shows 🟢/🟡/🔴/⚪ glyphs (not color-only) after a quiz.
- [ ] **Duplicate:** `ML-D3G1Q6` shows a "🔁 duplicate of ML-D3G1Q5" badge.

## Re-generate data after any edit to slices/study_notes
```bash
python3 app/build_data.py     # rewrites data.js; prints coverage + any NEW mislabel suspects
python3 app/tests/verify_answers.py   # re-confirm fidelity
```
