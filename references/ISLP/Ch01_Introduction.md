# ISLP Ch. 1 — Introduction (An Overview of Statistical Learning)

*Source: ISLP (James, Witten, Hastie, Tibshirani, Taylor), PDF pages 12–25 (book pp. 1–14).*

> ML4T exam relevance: framing/vocabulary that underpins every domain — supervised vs.
> unsupervised, regression vs. classification, and notation. → ML Domain 1 (ML fundamentals).

## What statistical learning is
- **Statistical learning** = a vast toolset for *understanding data*. Two broad families:
  - **Supervised learning**: build a model to predict/estimate an **output** from one or more
    **inputs**. (Business, medicine, astrophysics, public policy, finance.)
  - **Unsupervised learning**: inputs but **no supervising output**; still learn structure/
    relationships (e.g., grouping similar observations).

## Three motivating datasets (map to problem types)
- **Wage data** — predict a continuous/quantitative output (wage) from age, education, year →
  a **regression** problem. Relationship of wage to age is **non-linear** (rises then falls ~age 60).
- **Smarket (S&P 500) data** — predict a categorical output (market **Up** vs **Down**) from prior
  days' % changes → a **classification** problem. Successive daily returns show little
  association (efficient-market intuition); QDA reached ~60% directional accuracy on 2005.
- **NCI60 gene expression data** — inputs only, no output → a **clustering / unsupervised**
  problem; PCA reduces 6,830 measurements per cell line to 2 dimensions (Z1, Z2) for visualization.

## Key distinctions to memorize
- **Regression vs. classification**: quantitative/continuous output → regression; qualitative/
  categorical output → classification.
- **Supervised vs. unsupervised**: presence vs. absence of a response variable Y.

## Brief history (context)
- Least squares / **linear regression** — early 19th century (astronomy).
- **Linear discriminant analysis** (1936); **logistic regression** (1940s); **generalized linear
  models** (early 1970s).
- Non-linear methods became practical in the 1980s: **classification & regression trees**,
  **generalized additive models**, **neural networks** (1980s), **support vector machines** (1990s).

## Notation (used throughout the book)
- **n** = number of observations (data points). **p** = number of variables/predictors.
  (Wage: n = 3,000, p = 11.)
- **x_ij** = value of the *j*-th variable for the *i*-th observation; **X** is the n×p matrix.
- **x_i** = row vector (length p) of one observation; **x_j** (bold) = column vector (length n)
  of one variable. Vectors default to columns; `T` = transpose.
- **y_i** = *i*-th response; observed data = {(x_1,y_1), ..., (x_n,y_n)}.
- Convention: vectors of length n in **lowercase bold**; matrices in **bold capitals**; random
  variables in **capital normal font**; scalars in lowercase normal.

## Book organization (what lives where — useful for exam topic mapping)
- Ch 2: terminology + concepts, KNN classifier. Ch 3: linear regression. Ch 4: classification
  (logistic regression, LDA). Ch 5: cross-validation & bootstrap. Ch 6: linear model selection/
  regularization (ridge, lasso, PCR). Ch 7: non-linear (splines, GAMs). Ch 8: tree-based
  (bagging, boosting, random forests). Ch 9: SVMs. Ch 10: deep learning. Ch 11: survival.
  Ch 12: unsupervised (PCA, K-means, hierarchical). Ch 13: multiple testing.
