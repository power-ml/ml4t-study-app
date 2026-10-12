# ISLP Section 8.1 — The Basics of Decision Trees

*Source: ISLP, PDF pages 340–349 (book pp. 333–342). 8.1.1 Regression Trees, 8.1.2 Classification
Trees, 8.1.3 Trees vs Linear Models, 8.1.4 Advantages/Disadvantages.*

> ML4T exam relevance: CART fundamentals — splitting criteria, pruning, and the high-variance
> weakness that motivates ensembles. → ML Domain 5 (Decision Trees / CART).

## Terminology
- **Terminal nodes / leaves**: the final regions R_1,…,R_J. **Internal nodes**: split points.
  **Branches**: segments connecting nodes. Trees are drawn upside down (leaves at bottom).

## 8.1.1 Regression Trees
- **Two-step build**:
  1. Partition predictor space into J distinct, non-overlapping regions R_1,…,R_J (boxes).
  2. Predict the **mean** of the training responses in the region an observation falls into.
- **Goal**: choose boxes minimizing `RSS = Σ_j Σ_{i∈R_j} (y_i − ŷ_{R_j})²` (Eq. 8.1), where ŷ_{R_j}
  is the region mean. Considering all partitions is infeasible.
- **Recursive binary splitting** (top-down, greedy): at each step pick predictor X_j and cutpoint s
  splitting into `{X | X_j < s}` and `{X | X_j ≥ s}` giving the **greatest RSS reduction** (Eq. 8.2–8.3).
  - *Top-down*: starts with all data in one region. *Greedy*: best split at the current step only,
    no look-ahead. Continue until a stopping rule (e.g., no node > 5 observations).

### Tree Pruning
- A large tree overfits (low bias, high variance, poor test performance). Stopping early on an RSS
  threshold is too short-sighted (a weak split may enable a great later split).
- **Better**: grow a large tree T_0, then **prune** back to a subtree.
- **Cost complexity pruning** (a.k.a. weakest-link pruning): index subtrees by tuning parameter
  **α ≥ 0**, minimizing `Σ_{m=1}^{|T|} Σ_{i:x_i∈R_m} (y_i − ŷ_{R_m})² + α|T|` (Eq. 8.4).
  - |T| = number of terminal nodes. α trades complexity vs training fit. α=0 → full tree T_0; larger
    α → smaller subtree (penalty per leaf). Analogous to the **lasso** penalty.
  - Branches prune in a nested, predictable way as α increases. **Select α via cross-validation**
    (Algorithm 8.1: grow → prune to subtree sequence → K-fold CV to pick α → refit on full data).

## 8.1.2 Classification Trees
- Predicts the **most commonly occurring class** in a region (also report class proportions).
- RSS can't be used for splits. Split-quality measures on p̂_mk (proportion of class k in region m):
  - **Classification error rate**: `E = 1 − max_k(p̂_mk)` (Eq. 8.5). Not sensitive enough for growing.
  - **Gini index**: `G = Σ_k p̂_mk(1 − p̂_mk)` (Eq. 8.6) — total variance across classes; small when a
    node is **pure** (p̂'s near 0 or 1). A **node-purity** measure.
  - **Entropy**: `D = − Σ_k p̂_mk log p̂_mk` (Eq. 8.7) — also small for pure nodes; numerically similar
    to Gini.
  - **Growing**: use Gini or entropy (more purity-sensitive). **Pruning**: any of the three, but
    classification error rate preferred if final prediction accuracy is the goal.
- Handles **qualitative predictors** natively (split assigns some categories to each branch).
- Splits can yield two leaves with the **same predicted class** — still worthwhile because they
  **increase node purity** (improves Gini/entropy even if classification error is unchanged),
  raising prediction confidence.

## 8.1.3 Trees vs. Linear Models
- Linear model: `f(X) = β0 + Σ_j X_j β_j` (Eq. 8.8). Tree: `f(X) = Σ_m c_m · 1(X ∈ R_m)` (Eq. 8.9).
- **Which is better depends on the true f**: linear structure → linear regression wins; highly
  non-linear/complex → trees win. Choose by estimating test error (CV / validation set). Trees may
  also be preferred for interpretability/visualization.

## 8.1.4 Advantages & Disadvantages
- **Pros**: very easy to explain (easier than linear regression); mirror human decision-making;
  graphical, interpretable by non-experts (if small); handle qualitative predictors with **no dummy
  variables**.
- **Cons**: generally **lower predictive accuracy** than other methods; **non-robust** — a small
  data change can drastically change the tree (**high variance**).
- **Fix**: aggregate many trees via **bagging, random forests, boosting** (Section 8.2) → large
  accuracy gains.
