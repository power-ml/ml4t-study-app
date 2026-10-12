# Study Guide — ISLP Ch. 1: Introduction (An Overview of Statistical Learning)

*Built from the distilled ref `references/ISLP/Ch01_Introduction.md` (source: ISLP PDF pages 12–25 / book pp. 1–14) and the verified Q&A in `study_notes/ML/Domain_01_Learning_Paradigms_and_Problem_Framing.md`.*

> Mapping note: this guide follows the authoritative chapter→domain map in `references/INDEX.md`. (The inline "ML Domain" numbers printed inside the distilled ref use a different/older scheme; INDEX.md and the `Domain_XX` study-note filenames are the source of truth.)

---

## 1. Key concepts to know for the exam

- **Statistical learning** = a toolset for *understanding data*. Two broad families:
  - **Supervised learning**: build a model to predict/estimate an **output** from one or more **inputs** (a response variable Y is present).
  - **Unsupervised learning**: inputs but **no supervising output**; learn structure/relationships (e.g., grouping similar observations).
- **Regression vs. classification**: quantitative/continuous output → **regression**; qualitative/categorical output → **classification**.
- **Supervised vs. unsupervised**: defined by the *presence vs. absence of a response variable Y* — not by the output format or which rows are used.
- Three motivating datasets map to the problem types:
  - **Wage data** → regression (predict a continuous wage); relationship of wage to age is **non-linear**.
  - **Smarket (S&P 500) data** → classification (market **Up** vs **Down**); QDA reached ~60% directional accuracy on 2005.
  - **NCI60 gene expression** → clustering / **unsupervised**; PCA reduces 6,830 measurements to 2 dimensions (Z₁, Z₂).
- **Notation (used throughout the book):**
  - **n** = number of observations; **p** = number of variables/predictors (Wage: n = 3,000, p = 11).
  - **x_ij** = value of the *j*-th variable for the *i*-th observation; **X** is the n×p matrix.
  - **x_i** = row vector (length p) of one observation; **x_j** (bold) = column vector (length n) of one variable; vectors default to columns; `T` = transpose.
  - **y_i** = *i*-th response; observed data = {(x_1,y_1), ..., (x_n,y_n)}.
  - Convention: length-n vectors in lowercase bold; matrices in bold capitals; random variables in capital normal font; scalars lowercase normal.
- Brief history (context): least squares / linear regression (early 1800s); LDA (1936); logistic regression (1940s); GLMs (early 1970s); trees, GAMs, neural networks (1980s); SVMs (1990s).

## 2. Why it matters for Exam 1

- **Maps to ML Domain 1 (Learning Paradigms & Problem Framing).** This chapter supplies the framing/vocabulary that underpins every other domain.
- **Question themes:** supervised vs. unsupervised (labels define the paradigm); regression vs. classification (target definition, not features, decides the type); two-stage unsupervised→supervised pipelines; "the task/target defines the paradigm, not which rows are used."

## 3. Sample questions with correct answers (verbatim from `Domain_01`)

### [ML-D1G1Q1] Supervised vs. unsupervised — labels define the paradigm
**Scenario:** A hedge-fund PM wants a system that finds market patterns and signals buy/sell, while a client suggests clustering regimes without using returns. You must clarify how the approaches differ.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Predicting next-day returns from labeled history is supervised: the realized next-day return is a known target (Y) paired with each feature row, so the model learns a mapping X → Y. |
| B | False | Clustering days into regimes *without* labels is unsupervised — there is no target to predict; the model only groups by feature similarity. |
| C | True | Discovering structure with no supplied targets is the definition of unsupervised learning (e.g., clustering, dimensionality reduction). |
| D | False | A buy/sell output does not imply supervised learning — a hand-coded rule or an unsupervised signal can also emit actions. The *action format* doesn't reveal how (or whether) learning used labels. |
| E | True | It is exactly the availability of example-target pairs that makes a problem supervised; without paired targets you cannot do supervised learning. |

### [ML-D1G1Q3] Same rows, two paradigms
**Scenario:** A team has market features + realized one-week returns and wants both a return forecast and a regime map, and must explain which outputs depend on labels. The same rows feed two analyses.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Predicting realized one-week return uses that return as a supervised numeric target (each example paired with a known outcome → regression). |
| B | True | Drop the return column and group weeks by feature similarity → no target supplied → the task becomes unsupervised structure discovery. |
| C | False | Using the same feature rows does not force one paradigm; the paradigm is set by the task/target, not by which rows are used. |
| D | True | Naming clusters "bull/bear/sideways" after inspecting them is post-hoc interpretation — it supplies no labels *during* learning, so the clustering stays unsupervised. |
| E | False | Unsupervised structure is not guaranteed useful for prediction — discovered groups may be unrelated to the trading objective. |

### [ML-D1G2Q1] Exact return (regression) vs. above-threshold (classification)
**Scenario:** For tomorrow's S&P 500 move, one team forecasts the exact % return, another predicts whether return exceeds 0.50%; risk wants to know why evaluation differs. Both use the same features.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Exact percentage return is a continuous numeric target → regression. |
| B | True | "Exceeds 0.50%?" has two discrete classes defined by a threshold → binary classification. |
| C | False | Identical features do not force the same problem type — the *target definition* does. |
| D | True | Converting a continuous return to an above/below label discards magnitude: very different returns can share the same class. |
| E | False | Low regression error does not guarantee perfect classification — a tiny numeric error near the threshold flips the class. |
