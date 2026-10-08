# ML4T Exam-1 Reference Library — Source-of-Truth Index

Distilled study notes from the **recommended** book chapters in `course_schedule.md` for **Exam 1 (weeks 1–7)**.
Each note cites the source PDF page range at its top and ends sections with an "ML4T exam relevance" mapping.
Faithful distillations of the books in `../books/` — use these to verify/deep-dive concepts behind exam questions.

_Built 2026-09-29 via isolated sub-agents (text extracted with `pypdf`; poppler not installed)._

## What's covered (recommended, in scope)
| Book (file in `books/`) | Chapter(s) | Week | Distilled file | Primary exam domains |
|---|---|---|---|---|
| Probabilistic Machine Learning (Murphy, Bk 1) `Probabilistic Machine Learning.pdf` | Ch. 1 Introduction | 1 | `ProbabilisticML/Ch01_Introduction.md` | ML D1 (paradigms), D8/D9 (eval, generalization) |
| Handbook of AI & Big Data in Investments `ai-and-big-data-in-investments.pdf` | Ch. 1 ML Applications | 1 | `Handbook_AI_BigData/Ch01_ML_Applications_in_Investments.md` | ML D1/D3; QF D9/D10 |
| Handbook of AI & Big Data in Investments | Ch. 2 Alternative Data & AI | 2, 6 | `Handbook_AI_BigData/Ch02_Alternative_Data_and_AI.md` | ML D2/D3; QF D9 |
| Deep Learning: Foundations & Concepts (Bishop) `Deep Learning_ Foundations and Concepts-Springer (2024).pdf` | Ch. 1 Overview | 5 | `DeepLearning/Ch01_Overview.md` | ML D1, D9 |
| Deep Learning: Foundations & Concepts | §2.1 Rules of Probability | 2 | `DeepLearning/Ch02-1_Probability.md` | ML D1/D2 (Bayes) |
| Deep Learning: Foundations & Concepts | §2.2 Probability Densities | 2 | `DeepLearning/Ch02-2_Probability_Densities.md` | ML D2; QF D1/D2 (expectation/variance/covariance) |
| Intro to Statistical Learning, Python (ISLP) `ISLP_website.pdf` | Ch. 1 Introduction | 3 | `ISLP/Ch01_Introduction.md` | ML D1 |
| ISLP | §2.2 Assessing Model Accuracy | 3 | `ISLP/Ch02-2_Assessing_Model_Accuracy.md` | ML D8, D9 (bias-variance, MSE, Bayes error) |
| ISLP | §3.1–3.3 Linear Regression | 3 | `ISLP/Ch03-1to3_Linear_Regression.md` | ML D4 |
| ISLP | §3.5 Linear Regression vs KNN | 5 | `ISLP/Ch03-5_LinReg_vs_KNN.md` | ML D4, D5 |
| ISLP | §8.1 Decision Trees | 4 | `ISLP/Ch08-1_Decision_Trees.md` | ML D6 |
| ISLP | §8.2 Bagging, Random Forests, Boosting | 4 | `ISLP/Ch08-2_Bagging_RF_Boosting.md` | ML D7 |
| What Hedge Funds Really Do (Romero & Balch) `What Hedge Funds Really Do - An Introduction to Portfolio Management.pdf` | Ch. 2 So You Want to Be a Hedge Fund Manager | 5 | `WhatHedgeFundsReallyDo/Ch02_So_You_Want_to_Be_a_Hedge_Fund_Manager.md` | QF D1 (returns, CAGR, Rule of 72), D2 (volatility, Sharpe, drawdown), D7/D10 (benchmarks, fees) |
| What Hedge Funds Really Do | Ch. 4 Market-Making Mechanics | 5 | `WhatHedgeFundsReallyDo/Ch04_Market_Making_Mechanics.md` | QF D5 (spreads, orders, order book, shorting, HFT); D8 |
| What Hedge Funds Really Do | Ch. 5 Introduction to Company Valuation | 6 | `WhatHedgeFundsReallyDo/Ch05_Company_Valuation.md` | QF D6 (book value, PV, DDM, perpetuity); D1 |
| What Hedge Funds Really Do | Ch. 7 Framework for Investing: CAPM | 6 | `WhatHedgeFundsReallyDo/Ch07_CAPM.md` | QF D7 (alpha, beta, beta-balanced hedge); D3; D8 |
| What Hedge Funds Really Do | Ch. 8 The Efficient Market Hypothesis — Three Versions | 7 | `WhatHedgeFundsReallyDo/Ch08_Efficient_Market_Hypothesis.md` | QF D8 (EMH forms); D6, D10 |
| What Hedge Funds Really Do | Ch. 12 Overcoming Data Quirks to Design Trading Strategies | 7 | `WhatHedgeFundsReallyDo/Ch12_Overcoming_Data_Quirks.md` | QF D9 (adjusted prices, fill forward/backward, survivor bias); D10; ML D2 |


## Not covered (and why)
- **What Hedge Funds Really Do** — now distilled (2026-10-07) for the Exam-1 chapters (Ch. 2, 4, 5, 7, 8, 12) in `WhatHedgeFundsReallyDo/`. **Ch. 9/10 (Exam-2, week 10) still pending.** Book has no separate printed page numbers (PDF page labels = PDF page numbers, offset 0).
- **Optional** readings (e.g., Machine Learning Ch.1/3/8, Python for Finance, papers) — excluded per scope, unless the exam prep guide references a concept from them.
- **Exam-2 material** (weeks 8+: RL, deep nets, options, etc.) — out of scope for now.

## Notes
- Page offsets differ per book (recorded in each file's header): ISLP PDF offset varies (book+11 in Ch.1, +9 in Ch.3, +7 by Ch.8 — the website PDF drops/inserts pages); concept-map links use PDF pages from the bookmarks, so they're unaffected; Deep Learning PDF = book + 20; verify against the book if a page cite matters.
