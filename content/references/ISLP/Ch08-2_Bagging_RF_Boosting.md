# ISLP Section 8.2 — Bagging, Random Forests, Boosting (and BART)

*Source: ISLP, PDF pages 350–361 (book pp. 343–354). 8.2.1 Bagging, 8.2.2 Random Forests,
8.2.3 Boosting, 8.2.4 BART, 8.2.5 Summary.*

> ML4T exam relevance: tree ensembles — the variance-reduction vs sequential-bias-reduction
> distinction, key hyperparameters, and OOB error. → ML Domain 6 (Ensemble Learners: bagging,
> random forests, boosting).

## Ensemble idea
- **Ensemble method**: combine many simple **weak learners** (here, trees) into one strong model.

## 8.2.1 Bagging (Bootstrap AGGregatING)
- **Motivation**: single trees have **high variance** (a different data split gives a very different
  tree). Averaging n independent observations with variance σ² gives variance σ²/n → **averaging
  reduces variance**.
- **Procedure**: draw B **bootstrap** samples from the training data, fit a tree to each, average:
  `f̂_bag(x) = (1/B) Σ_b f̂*^b(x)`. Trees are grown **deep and unpruned** (high variance, low bias);
  averaging kills the variance.
- **Classification**: **majority vote** across the B trees.
- **B is not critical**: large B does **not** cause overfitting; pick B large enough for error to
  settle (e.g., B=100).
- **Out-of-Bag (OOB) error**: each bootstrap tree uses ~2/3 of observations; predict each obs. using
  only the ~B/3 trees where it was OOB (average / majority-vote), then compute OOB MSE / error. A
  valid test-error estimate — with large B ≈ leave-one-out CV — and cheap vs CV on big data.
- **Variable importance**: bagging loses the single-tree interpretability. Summarize importance by
  total **RSS decrease** (regression) or **Gini index decrease** (classification) from splits on
  each predictor, averaged over B trees. Large decrease = important predictor.

## 8.2.2 Random Forests
- Like bagging (bootstrap + deep trees), **but at each split only a random subset of m predictors**
  is considered as split candidates (fresh sample each split). Typically **m ≈ √p**.
- **Why**: with one strong predictor, all bagged trees split on it first → trees **highly
  correlated** → averaging correlated quantities barely reduces variance. Restricting to m predictors
  **decorrelates** the trees (on avg (p−m)/p of splits ignore the strong predictor), reducing
  variance more.
- **m = p is just bagging.** Small m helps most when predictors are **many and correlated**.
- Like bagging, **does not overfit** as B increases.

## 8.2.3 Boosting
- Trees grown **sequentially**, each using information from prior trees. **No bootstrap** — each tree
  fit on a modified version of the data. Idea: **learn slowly**, fitting each new tree to the
  **residuals** of the current model, then add a shrunken version in.
- **Algorithm 8.2 (regression)**: init f̂(x)=0, r_i=y_i; for b=1..B: fit tree f̂^b with d splits to
  (X, r); update `f̂(x) ← f̂(x) + λ f̂^b(x)`; update `r_i ← r_i − λ f̂^b(x_i)`. Output
  `f̂(x) = Σ_b λ f̂^b(x)`.
- **Three tuning parameters**:
  1. **B (number of trees)** — boosting **CAN overfit** if B too large (slowly); choose B via CV.
     (Contrast: bagging/RF don't overfit with large B.)
  2. **λ (shrinkage)** — small positive learning rate, typically 0.01 or 0.001. Smaller λ needs
     larger B.
  3. **d (splits per tree = interaction depth)** — controls complexity. **d=1 = stump** → an additive
     model (each term one variable). d = max interaction order.
- Because each tree accounts for prior trees, **small trees (even stumps) often suffice** and aid
  interpretability. In the gene-expression example, depth-1 stumps beat depth-2 and both beat a
  random forest.

## 8.2.4 Bayesian Additive Regression Trees (BART)  — brief
- Hybrid of bagging/RF (each tree built with randomness) and boosting (each tree captures signal not
  yet fit). Uses K trees over B iterations; **novelty**: each new tree is a random **perturbation**
  of the previous iteration's tree (change structure by adding/pruning branches, or change
  terminal-node predictions), favoring perturbations that improve fit to the **partial residual**
  (Algorithm 8.3).
- Perturbing (vs fitting fresh) plus small trees **guards against overfitting** — training and test
  error stay close (unlike boosting, which overfits as iterations grow). Uses a **burn-in** period L
  (discard early models); final prediction = average over post-burn-in iterations.
- Can be viewed as a **Bayesian / MCMC** method (each perturbation ≈ draw from a posterior). Typical
  settings K=200, B=1000, L=100; strong **out-of-box** performance with minimal tuning.

## 8.2.5 Summary of tree ensembles (memorize the contrast)
- **Bagging**: trees grown **independently** on bootstrap samples → similar trees; can get stuck in
  local optima.
- **Random forests**: independent bootstrap trees **+ random feature subset per split** →
  decorrelated trees, better model-space exploration.
- **Boosting**: **original data only**, trees grown **successively** on leftover signal, shrunken;
  slow learning.
- **BART**: original data only, trees grown successively but **perturbed** to avoid local minima /
  explore more.
- Trees make good weak learners: flexible, handle **mixed** (qualitative + quantitative) predictors.
