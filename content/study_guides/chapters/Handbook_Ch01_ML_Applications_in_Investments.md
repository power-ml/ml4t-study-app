# Study Guide — Handbook Ch. 1: ML Applications in Investments

**Built from:** `references/Handbook_AI_BigData/Ch01_ML_Applications_in_Investments.md`
(Chen, M. (Robeco) & Zhou, W. — *Handbook of AI and Big Data Applications in Investments*, CFA Institute Research Foundation, 2023).
**Source page range (from ref header):** Book pages **2–19** (PDF pages 23–40).
**Mapped exam domains (per `references/INDEX.md`):** ML **D1** (learning paradigms, framing) & ML **D3** (feature engineering, leakage); QF **D9** (financial-data & research bias) & QF **D10** (quantitative strategy design & evaluation).

---

## 1. Key concepts

- **Why apply ML to investing:** the attraction is higher **risk-adjusted return**. ML predicts on **high-dimensional data with no prespecified functional form**, so it can model future returns, earnings, and crash probability better than linear models.
- **Where the edge comes from:** ML does *not* prespecify the predictor→target relationship, so it captures **interaction effects** (one input's effect depends on another) and **nonlinear effects** (e.g., NN activation functions). Empirically (Gu, Kelly, Xiu 2020) **interaction effects drive most of the outperformance**; nonlinear-only contribution is less clear.
- **Why finance is hard for ML:**
  - **Low signal-to-noise ratio** — any one metric only weakly determines returns.
  - **Small data** — US ≈ 100 yrs, ~1,200 monthly points/security; limits CV, OOS testing, tuning. *A simpler model on more data often beats a sophisticated model on little data.*
  - **Nonstationarity / adaptive markets** — markets "learn," published research changes behavior (McLean & Pontiff 2016); the data-generating process shifts over time.
- **Pitfalls (exam-critical):**
  - **Overfitting** — great backtest, poor OOS. Mitigate with cross-validation, feature selection, regularization, early stopping, **ensembling**, holdout; plus economic "smell tests" and **SHAP values**; and **feature engineering** from domain knowledge.
  - **Replicability** — harder for ML (version/seed/implementation variance); fix with version control, fixed parameters, documentation of failures ("research graveyards").
  - **Lookahead bias / data leakage** — use **point-in-time** data; insert a **gap period** between train/validation/test; beware features unavailable at production time.
  - **Implementation gap** — backtest trades that are infeasible live (micro-caps, hard-to-borrow shorts); ML worsens this via **high turnover**.
  - **Explainability** — use **partial dependence response** to decompose output into linear/interaction/nonlinear components.
- **Representative results:** Gu et al. (2020) 4-layer NN long–short decile spread → OOS **Sharpe 1.35 (value-weighted), 2.45 (equal-weighted)** vs. OLS **0.61 / 0.83**. Most important features are consistent across algorithms (short-term reversal, momentum, volatility, size); **simple ML beats complex**; **more data → better ML**; **ensembling ≈ "the closest thing to a free lunch."**

## 2. Why it matters for Exam 1

This chapter is the conceptual bridge between the ML and QF sides of Exam 1 (Week 1 reading). It directly reinforces:

- **ML D1 (Learning Paradigms & Problem Framing):** supervised return/earnings/crash prediction, regression vs. classification framing, and the overfitting/generalization and bias-variance language the exam tests.
- **ML D3 (Feature Engineering & Leakage):** feature engineering from domain knowledge, point-in-time data, and leakage in features — the chapter's "lookahead bias / leakage" section maps almost one-to-one.
- **QF D9 (Financial Data & Research Bias):** lookahead bias, data leakage, point-in-time data, replicability, and data-snooping guardrails.
- **QF D10 (Quantitative Strategy Design & Evaluation):** the implementation gap (turnover, transaction costs, feasibility) and net-vs-gross thinking that separate a good backtest from a deployable strategy.

## 3. Sample questions (verbatim from mapped-domain verdict tables — not invented)

### Q1 — ML D1, item [ML-D1G1Q1] "Supervised vs. unsupervised — labels define the paradigm"
**Scenario:** A hedge-fund PM wants a system that finds market patterns and signals buy/sell, while a client suggests clustering regimes without using returns. You must clarify how the approaches differ. **Answer polarity: Normal (True = accurate).**

> | A | True | Predicting next-day returns from labeled history is supervised: the realized next-day return is a known target (Y) paired with each feature row, so the model learns a mapping X → Y. |
> | D | False | A buy/sell output does not imply supervised learning — a hand-coded rule or an unsupervised signal can also emit actions. The *action format* doesn't reveal how (or whether) learning used labels. |

*(Source: `study_notes/ML/Domain_01_Learning_Paradigms_and_Problem_Framing.md`.)*

### Q2 — ML D3, item [ML-D3G5Q1] "Post-resolution status code (target leakage)"
**Scenario:** A default model uses an account-status code recorded *after* collections closes the case and hits near-perfect accuracy; the credit officer wants to deploy but model-risk questions when the code becomes available. **Answer polarity: Normal (True = accurate).**

> | A | True | A post-resolution status code may encode the outcome itself → target leakage. |
> | B | False | Wrong: high accuracy says nothing about whether the feature is available at prediction time. |
> | C | True | Each feature should be reconstructed using only information available at the prediction timestamp (point-in-time). |

*(Source: `study_notes/ML/Domain_03_Feature_Engineering_and_Leakage.md`.)*

### Q3 — QF D10, item [QF-D10G4Q1] "Small edge at high turnover — gross vs. net"
**Scenario:** A model with a small, statistically significant edge trades every few minutes, earning 8% annually before costs; estimated spreads, commissions, and impact total ~10% annually at that turnover. **Answer polarity: Normal (True = accurate).**

> | B | False | It is not profitable on a net basis: estimated 10% costs exceed the 8% gross return. |
> | D | True | Deployment decisions must be based on net, not gross, performance. |
> | E | True | Reducing turnover can improve net economics even if gross predictive accuracy falls slightly. |

*(Source: `study_notes/QF/Domain_10_Quantitative_Strategy_Design_and_Evaluation.md`.)*
