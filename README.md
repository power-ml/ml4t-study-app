# ML4T Exam Prep — Study App

A local study app for the Georgia Tech CS 7646 *Machine Learning for Trading* (ML4T) exam
question pools. It covers **Exam 1** (518 questions) and **Exam 2** (420 questions). Each question
includes the official answer key, an expanded explanation for every choice, the concepts it tests,
and where to read about them.

It runs entirely on your computer. There is no account and no internet connection needed, and
nothing you do is sent anywhere.

> The question pool was published by the course instructor, and is public on purpose. The pool's
> own introduction says: "The public nature of the pool is intentional." This app reorganizes it for study and adds explanations.
> The official answer key is never changed.

---

## 1. Start the app

You need **Python 3.8 or newer** and nothing else (no packages to install).

| Your computer | How to start |
|---|---|
| **macOS** | Double-click `start.command`. If macOS blocks it the first time, right-click it → **Open**. |
| **Windows** | Double-click `start.bat`. |
| **Linux / terminal** | `./start.sh` or `python3 app/serve.py --open` |

Your browser opens at `http://127.0.0.1:8765/`. Keep the small terminal window open while you
study, and close it (or press Ctrl-C) to stop the app.

**No Python?** Open `app/index.html` directly in your browser. Everything works except two things:
your progress is saved only inside that browser, and the book reader is off.

**Port already in use?** Start it on another port: `ML4T_PORT=8790 python3 app/serve.py --open`.

### Where your progress is saved
Notes, flags, reviewed questions and quiz results are saved automatically in `user-data/` as you work:
- `ml4t_state.json`: everything the app tracks.
- `ml4t_notes.md`: a readable copy of all your notes, grouped by exam, part and domain.
- `_backups/`: the last 60 versions, in case something goes wrong.

`user-data/` is private to you and is never included if you share the app. To start over, stop the
app and delete `user-data/ml4t_state.json`.

### Optional: textbook PDFs
Add your own copies of the course textbooks to `books/` and citations become clickable: the book
opens at the cited page. See [`books/README.md`](books/README.md) for the official free sources and
the filenames the app expects.

---

## 2. How the exam is scored (and why the app scores the same way)

- 40 questions. Each has 5 choices, and you mark each choice **True** or **False**.
- **1 point per correct choice**, so 5 per question and 200 in total. A blank choice scores 0, the
  same as a wrong one, so **always guess**.
- Marking **all 5 the same** (or leaving all 5 blank) may score **0 for the whole question**.
- **Inverted questions** say "mark True if the statement is *incorrect*." The app flags them with
  an amber **INVERTED** label.

Every quiz in the app uses these rules.

---

## 3. The header bar (always visible)

| Control | What it does |
|---|---|
| **🎓 Exam 1 / Exam 2** | Switches every tab between the two question pools. Your progress is kept separately for each. |
| **📅 Studied thru week** | The course week you've reached. Domains taught later are dimmed and marked "not yet covered". Quizzes can be limited to covered material. |
| **💡 Hints** | Shows or hides the trap-word hints on choices ("absolute → ~74% False", "negation → check the claim") in Study, Flashcards, Quiz and Review. Turn it off to practise under real exam conditions. The setting is remembered. |
| **Save status** | Shows "saving…", then "✓ saved". "notes→file ✅" means progress is going to `user-data/`. |

---

## 4. The tabs

### 📖 Study: browse and self-test every question
Questions are grouped by domain. Each domain header shows how many of its questions you've reviewed
and has a **📚 Deep dive** panel, described below.

**Filters (top bar):** part (ML / QF), domain, text search, **hide reviewed**, **🚩 flagged only**,
**❌ missed in quiz**, and **🚫 hide withdrawn** (on by default; withdrawn questions are no longer on
the exam).

**Two modes (toggle button):**
- **🙈 Self-test (tap to reveal):** answers are hidden. Each choice has **True / False** buttons.
  Click your call and the answer appears, marked ✓ or ✗. You can also tap a choice to reveal it
  without guessing. Once every choice is revealed, you see a **Self-check: x/5** score.
- **👁 Answers shown:** every answer and explanation is visible, for fast reading.

**On every question card:**
- The answer and an **expanded explanation** for each choice. On inverted questions it also says
  whether the statement itself is accurate.
- **📖 Read:** the concept being tested and the book, chapter and page to read.
- **Trap hints** on choices that contain absolute words ("always", "never", "only"…) or negations.
  Turn them on or off with **💡 Hints** in the header.
- **✅ reviewed** checkbox. It ticks itself once you've revealed all 5 choices.
- **🚩 flag** to come back to the question later.
- **📝 Note** box. Notes save as you type.
- Badges: **#n** (stable question number), **📅 week**, **INVERTED**, **🚫 withdrawn**,
  **🔁 duplicate**, **⚠ check formula glyphs** (a symbol may be misread from the source PDF), and
  **✅/❌ last quiz** result.

**📚 Deep dive (per domain):**
- *Where to read*: a table of the domain's key concepts and the best book/chapter/page for each.
- A cheat-sheet and the common traps for that domain.
- References and distilled book notes.

The app remembers where you were and returns to that question next time.

### 🃏 Flashcards: one question at a time, then flip
1. **Front:** the question and its 5 choices, with True/False buttons on each.
2. Press **Flip ▸** (or Enter / Space). The card turns over.
3. **Back:**
   - Your score for that question (x/5).
   - Every choice with the correct answer, your answer (✓/✗), the full explanation and the answer
     key's own rationale.
   - **Concepts tested:** each concept explained, its lecture, and every book/chapter/section/page
     that covers it, with notes.
   - The question's reference, the domain cheat-sheet and the common traps.
   - Flag and note controls.
4. **Next ▸** moves on. **↺ Try again** flips back to the front. On a keyboard, use ← → to move
   between cards.

**Decks:** All, Not yet reviewed, 🚩 Flagged, ❌ Missed in a quiz, Inverted only, and ⚖ 1/4 or 4/1
split. You can also filter by part and domain. **🔀 Shuffle** randomizes the order. Answering all 5
choices and flipping marks the question reviewed. Your deck and position are remembered.

### 📝 Quiz / Mock: timed-style practice, scored like the real exam
**Modes:**
- **Smart:** fresh questions you've never reviewed or quizzed, split half ML / half QF, one per
  domain. If fresh questions run out, it fills in with remaining fresh questions, then flagged ones,
  then repeats. Each card says why it was picked.
- **Trap drill:** inverted questions, plus questions with absolute or negation wording.
- **🚩 Flagged:** re-quiz the questions you flagged.
- **Random:** a random sample.
- **Exam simulator:** 40 questions, 2 from each domain, just like the real exam.

**Count**, **Part** and **covered only** (questions up to your studied week) narrow the pool. Two more
filters apply to every mode:
- **Domains:** pick one or more, with quick **All / None / ML only / QF only** buttons. Each domain
  shows not-reviewed / total questions.
- **not-reviewed only:** skip questions you've already reviewed. Combined with Domains, this lets
  you work through the new questions in chosen domains.

The builder shows how many questions match, and remembers your choices. The Exam simulator draws 2
questions per selected domain.

**During the quiz** each card shows only its position ("Q 3 / 10"). The question ID, #number, domain
and INVERTED label stay hidden, as on the real exam, and so do book links. You can still flag and
note any question.

**After Submit & score:**
- Your percentage and the domains to focus on next.
- The correct answer and explanation on every choice.
- A **🚩 Flag all missed** button.
- Each question's details are revealed: #number, ID, domain, week and INVERTED label.
- A **✅ reviewed** checkbox appears next to flag and note. Questions with all 5 choices answered
  are ticked automatically, and you can change it.
- The page stays as it is, so you can write things down.

### 🚩 Review: your personal re-study list
Shows the questions you flagged, wrote a note on, or missed in a quiz. Filter by: All, 🚩 Flagged,
📝 Has note, ❌ Missed in a quiz, or 🕘 Last quiz. Each card has its choices and answers (expandable),
an editable note and a flag toggle. **Quiz flagged ▸** starts a quiz from your flagged questions.

**🖨 Print notes** prints every note for the selected exam. Notes are grouped by part (ML, then QF) and
by domain (e.g. "QF-D6 · Valuation & Mispricing"), in question order, without group or question
labels. Tick **include question** to print each question's scenario above its note. Your browser's
print dialog also lets you **Save as PDF**.

### ⚖ T/F Split: study by answer pattern
For each question, the app counts how many choices you mark True (after the inverted flip).
- **The table** shows how often each split (1T/4F, 2T/3F, 3T/2F, 4T/1F) occurs, by part and polarity.
  No question is ever all-True or all-False.
- **Filter:** lopsided (1/4 or 4/1), balanced (3/2 or 2/3), or an exact split. You can combine it
  with part, polarity and domain.
- Cards work like Study self-test. **Quiz these ▸** runs a quiz on the current filter.

The pattern is useful for settling the last uncertain choice. For example, Exam 1 QF questions are
always 3/2 or 2/3.

### 📈 Readiness: where you stand
- **Overall quiz accuracy**, with a readiness call and your weakest domains.
- **Review coverage by part:** ML, QF and total reviewed/total, with progress bars.
- **Review coverage by domain:** least-reviewed first, so start from the top.
- **Domain heatmap:** 🟢 ≥85% · 🟡 70–84% · 🔴 <70% · ⚪ not attempted (quiz accuracy).
- **Daily review log** for the last 14 days.
- **Export / Import progress:** save your progress to a file, or load it on another computer.

### 💡 Heuristics: answer patterns mined from the whole pool
Absolute words lean False, negations are often inaccurate, choice A leans True, and so on. Use these
**only as tiebreakers** after judging each choice on its merits.

---

## 5. Using it on a phone or tablet

The layout adapts to small screens. To study on your phone while the app runs on your computer
(same home Wi-Fi):

1. Start the app in **LAN mode**: `python3 app/serve.py --lan` (or `./start.sh --lan`).
2. The terminal prints a link like `http://192.168.1.20:8765/?k=abcd2345ef`. Open it once on your
   phone, then bookmark the page or use Share → **Add to Home Screen**. The key is saved as a
   cookie for 30 days, so you don't need the link again.
3. Study on either device. Progress saves to the same `user-data/` folder. If both devices are open,
   saves are **merged**, and a device picks up the other's progress when you switch back to it.
   (One limit: an un-flag or deleted note made on a device that was out of date can come back.
   Just redo it.)

**How LAN mode is protected:**
- It's **off by default**. Normally the app only accepts connections from the same computer.
- Phones and other devices need the **random access key** in that link. Everything else gets "not
  authorized". The key is in `user-data/lan_key.txt`; delete that file and restart to issue a new
  key, which locks out any device that had the old one.
- Only **local-network addresses** are accepted. Your router doesn't pass connections from the
  internet through to your computer unless you set up port forwarding, so **don't add a
  port-forwarding rule for this app.**
- Optional: limit it to your phone's IP address, with
  `ML4T_LAN_ALLOW=192.168.1.23 python3 app/serve.py --lan`. The key is still required. Set a
  fixed/reserved IP for the phone in your router, or this can lock you out when the address
  changes.
- **What other devices can do, even with the key:** read only the app page, its data, your saved
  progress, the book list and the book PDFs. Nothing else on the computer is reachable (no other
  files or folders, no app source, no directory listings, no `../` tricks). The only thing they can
  write is **saving study progress**, and those saves only **add or update** entries (notes, flags,
  reviewed, quiz results). They can never remove anything, and they never delete or overwrite any
  file. Every save also keeps a new backup copy. Delete, edit and other request types are refused.
  Removing a flag or clearing a note therefore only sticks when done on the computer itself.
- LAN mode won't start if the progress, book or data folder is outside the app's folder (or the
  folder set by `ML4T_ROOT`).
- Use it only on a network you trust, like home Wi-Fi, not public or shared Wi-Fi. It's plain HTTP
  inside your network.

**Without the computer running:** copy the folder to the device and open `app/index.html`. Progress
is then saved only in that browser; use **Export / Import** on the Readiness tab to move it.

The book side panel is a desktop feature. On a phone, a book link opens in a new tab when the PDF is
available.

---

## 6. Optional: host it privately on your own AWS account

Use this to study from any device (phone, laptop, tablet) without keeping a computer running.
Everything sits behind your own login, and progress syncs across devices.

```
Browser ─HTTPS─► CloudFront ─► login check (Lambda@Edge): no valid sign-in → sign-in page
                  ├─ /*         → private S3 bucket (Block Public Access on; readable only by CloudFront via OAC)
                  └─ /api/state → API Gateway (Cognito JWT check) → Lambda → DynamoDB (your progress)
Cognito: you're the only user (self sign-up off), optional MFA, 30-day sessions
```

**Deploy (from your own computer, with your personal AWS CLI profile):**
```bash
AWS_PROFILE=personal ./deploy/deploy.sh you@example.com
```
- It creates the `ml4t-study` stack in **us-east-1**, uploads the app, and creates your login.
  Cognito emails you a temporary password; set your own the first time you sign in.
- Re-run the same command after any update to push the new version.
- The first deploy takes about 5–15 minutes (CloudFront).
- Optional extra security: turn on MFA (an authenticator app) for your user in the Cognito console.

**Move your existing progress in:** in the local app, open **Readiness → Export progress**. Then in the
hosted app, open **Readiness → Import** and pick that file.

**What's protected and how:**
- **Pages and question data:** the bucket is private, encrypted and versioned. CloudFront can read
  it only through OAC, and every request needs a valid sign-in, checked at the edge (RS256
  signature, issuer, expiry).
- **Your progress:** the API needs your Cognito token and only reads or writes your own record.
  Saves are validated and size-limited, and a save from an out-of-date device is merged rather than
  overwriting. DynamoDB point-in-time recovery keeps 35 days of history.
- **HTTPS only,** with standard security headers. The API is throttled (5 requests/second).
- **Book PDFs are never uploaded.** Citations still show as text.
- **Cost:** for one person, typically well under $1/month.

**Remove it:** delete the `ml4t-study` stack in CloudFormation (us-east-1). Deletion protection is on
for the user pool and the progress table, so turn it off for those first: this deletes your synced
progress, so export it first if you want to keep it. Empty the bucket too, including old versions.
CloudFront's edge function can take a few hours to finish deleting.

## 7. For maintainers

```
study-app/
├─ start.command / start.bat / start.sh   one-click launchers
├─ app/        index.html (the whole UI), data.js (generated), serve.py (local server)
├─ content/    slices/ (question pool, by domain), study_notes*/ (expanded explanations),
│              references/ (distilled book notes + concept_map/), study_guides/, overrides.json
├─ tools/      build_data.py (content → app/data.js), slice_pool.py, pdf_text_cleanup.py
├─ tests/      verify_answers.py, headless_smoke.mjs, TESTS.md
├─ deploy/     ml4t-hosting.yaml (CloudFormation), deploy.sh, build_site.py, web/ (sign-in pages)
├─ books/      your PDFs (git-ignored)
└─ user-data/  your progress (git-ignored)
```

- **Rebuild after editing content:** `python3 tools/build_data.py`
- **Prove answers match the source key:** `python3 tests/verify_answers.py`. Expect `PASS`, with 0
  unexpected mismatches.
- **UI smoke test:** see `tests/TESTS.md`.
- **Formula repairs:** the pool PDF's math font extracts as garbage glyphs. `content/math_fixes.json`
  records 137 exact-text repairs transcribed from the rendered PDF pages, applied to `content/slices/`
  by `python3 tools/apply_math_fixes.py` (idempotent; `--check` to verify). `verify_answers.py` also
  fails if any garbled glyph reaches the app.
- **Answer fidelity:** answers are copied verbatim from the official pool's answer key. The only
  deliberate correction is the one in `content/overrides.json` (a verified letter mislabel in the
  source).
