# Study Guide — ISLP §8.1: The Basics of Decision Trees

*Built from the distilled ref `references/ISLP/Ch08-1_Decision_Trees.md` (source: ISLP PDF pages 340–349 / book pp. 333–342; 8.1.1 Regression Trees, 8.1.2 Classification Trees, 8.1.3 Trees vs Linear Models, 8.1.4 Advantages/Disadvantages) and the verified Q&A in `study_notes/ML/Domain_06_Decision_Trees.md`.*

> Mapping note: follows the authoritative chapter→domain map in `references/INDEX.md` (ML Domain 6). (The inline number inside the distilled ref uses an older scheme.)

---

## 1. Key concepts to know for the exam

**Terminology:** terminal nodes/leaves = final regions R_1,...,R_J; internal nodes = split points; branches connect nodes; trees drawn upside down.

**Regression trees (8.1.1):**
- **Two-step build:** (1) partition predictor space into J non-overlapping regions (boxes); (2) predict the **mean** of training responses in the region.
- **Goal:** minimize `RSS = Σ_j Σ_{i∈R_j} (y_i − ŷ_{R_j})2` (Eq. 8.1), ŷ_{R_j} = region mean.
- **Recursive binary splitting** (top-down, greedy): pick predictor X_j and cutpoint s splitting into `{X | X_j < s}` and `{X | X_j ≥ s}` giving the **greatest RSS reduction** (Eq. 8.2–8.3). Greedy = best split now, no look-ahead.

**Tree pruning:**
- A large tree overfits (low bias, high variance). Grow a large tree T_0, then **prune** to a subtree.
- **Cost complexity pruning** (weakest-link): minimize `Σ_{m=1}^{|T|} Σ_{i:x_i∈R_m} (y_i − ŷ_{R_m})2 + α|T|` (Eq. 8.4). |T| = # terminal nodes; α=0 → full tree; larger α → smaller subtree (penalty per leaf). Analogous to the **lasso** penalty. **Select α via cross-validation** (Algorithm 8.1).

**Classification trees (8.1.2):**
- Predicts the **most commonly occurring class** in a region. RSS can't be used for splits. Split-quality measures on p̂_mk (proportion of class k in region m):
  - **Classification error rate:** `E = 1 − max_k(p̂_mk)` (Eq. 8.5) — not sensitive enough for growing.
  - **Gini index:** `G = Σ_k p̂_mk(1 − p̂_mk)` (Eq. 8.6) — total variance across classes; small when a node is **pure**. A **node-purity** measure.
  - **Entropy:** `D = − Σ_k p̂_mk log p̂_mk` (Eq. 8.7) — also small for pure nodes; numerically similar to Gini.
  - **Growing:** use Gini or entropy (more purity-sensitive). **Pruning:** any of the three; classification error preferred if final accuracy is the goal.
- Handles **qualitative predictors** natively (no dummy variables). Two leaves with the same predicted class can still be worthwhile — they **increase node purity**.

**Trees vs. linear models (8.1.3):** linear `f(X) = β₀ + Σ_j X_j β_j` (Eq. 8.8) vs. tree `f(X) = Σ_m c_m · 1(X ∈ R_m)` (Eq. 8.9). Which is better depends on the true f (choose by estimating test error).

**Advantages/disadvantages (8.1.4):**
- **Pros:** very easy to explain; mirror human decision-making; graphical/interpretable; handle qualitative predictors with no dummies.
- **Cons:** generally lower predictive accuracy; **non-robust** — a small data change can drastically change the tree (**high variance**).
- **Fix:** aggregate many trees (bagging, random forests, boosting — §8.2).

## 2. Why it matters for Exam 1

- **Maps to ML Domain 6 (Decision Trees / CART).**
- **Question themes:** prediction flow (one root-to-leaf path, not an average of all leaves); regression leaf = mean of training targets; splitting criteria (Gini / entropy / classification error — behavior at pure nodes vs. p=0.5, which to use for growing vs. pruning); impurity-reduction split selection; axis-aligned greedy splits, no need for feature scaling, high variance / instability, no extrapolation.

## 3. Sample questions with correct answers (verbatim from `Domain_06`)

### [ML-D6G1Q2] Regression leaf = mean of training targets
**Scenario:** A regression tree's leaf holds training targets 1%, 2%, −1%, 2%; the implementation predicts the leaf mean. A new observation lands in that leaf.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Mean = (1+2−1+2)/4 = 1%, the leaf's constant prediction. |
| B | True | Every observation reaching a leaf gets that leaf's single aggregate prediction. |
| C | False | A tree follows split rules; it does not compute KNN-style distances to all training points at inference. |
| D | True | Internal nodes route observations by their feature-based split conditions. |
| E | False | A leaf may contain one or many training observations, not exactly one. |

### [ML-D6G1Q6] Node impurity: Gini vs. entropy vs. classification error
**Scenario:** A Decision Tree Classifier labels liquidity regimes with Gini impurity; the risk team compares Gini, cross-entropy, and classification error, and the effect of feature transforms.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Classification error E=1−max_k p̂ is piecewise-linear and less sensitive to class-proportion changes → less effective for growing trees (used more for pruning). |
| B | False | Gini and entropy are **0** at pure endpoints p=0/1 and **maximal at p=0.5** — they do not attain maxima at the pure endpoints. |
| C | True | At a pure node both Gini (2·1·0) and entropy (−1·ln1−0·ln0, with 0ln0=0) equal 0. |
| D | True | A strictly monotonic transform changes reported thresholds but preserves observation ordering → same candidate partitions → same fitted tree (barring ties/precision exceptions). |
| E | True | By concavity, weighted child impurity ≤ parent impurity, so impurity reduction ≥ 0 (can equal 0). |

### [ML-D6G2Q1] Impurity reduction rewards purer children
**Scenario:** Two candidate root splits: Split A yields children each dominated by one class; Split B yields two near-equal mixtures. The criterion rewards impurity reduction.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Separating classes produces purer children and a larger impurity decrease than a near-even split. |
| B | True | A pure child contains observations of only one class. |
| C | False | Splits are compared by criterion value, not by raw feature scale. |
| D | True | Supervised splitting uses the known target labels to measure separation quality. |
| E | False | A locally useful training split does not guarantee minimum test error / global optimality. |
