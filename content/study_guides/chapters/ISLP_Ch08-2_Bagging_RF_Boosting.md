# Study Guide — ISLP §8.2: Bagging, Random Forests, Boosting (and BART)

*Built from the distilled ref `references/ISLP/Ch08-2_Bagging_RF_Boosting.md` (source: ISLP PDF pages 350–361 / book pp. 343–354; 8.2.1 Bagging, 8.2.2 Random Forests, 8.2.3 Boosting, 8.2.4 BART, 8.2.5 Summary) and the verified Q&A in `study_notes/ML/Domain_07_Ensemble_Methods.md`.*

> Mapping note: follows the authoritative chapter→domain map in `references/INDEX.md` (ML Domain 7). (The inline number inside the distilled ref uses an older scheme.)

---

## 1. Key concepts to know for the exam

**Ensemble idea:** combine many simple **weak learners** (trees) into one strong model.

**Bagging (Bootstrap AGGregatING, 8.2.1):**
- **Motivation:** single trees have **high variance**; averaging n independent observations with variance σ² gives variance σ²/n → **averaging reduces variance**.
- **Procedure:** draw B **bootstrap** samples, fit a tree to each, average: `f̂_bag(x) = (1/B) Σ_b f̂*^b(x)`. Trees grown **deep and unpruned** (high variance, low bias); averaging kills the variance. **Classification:** majority vote.
- **B is not critical:** large B does **not** overfit; pick B large enough for error to settle (e.g., B=100).
- **Out-of-Bag (OOB) error:** each bootstrap tree uses ~2/3 of observations; predict each obs. from the ~B/3 trees where it was OOB → valid test-error estimate (≈ LOO-CV for large B), cheap vs. CV.
- **Variable importance:** total **RSS decrease** (regression) or **Gini decrease** (classification) from splits on each predictor, averaged over B trees.

**Random forests (8.2.2):**
- Like bagging, **but at each split only a random subset of m predictors** is considered (fresh sample each split). Typically **m ≈ √p**.
- **Why:** with one strong predictor, bagged trees all split on it first → **highly correlated** → averaging barely helps. Restricting to m predictors **decorrelates** the trees, reducing variance more.
- **m = p is just bagging.** Small m helps most when predictors are **many and correlated**. Does not overfit as B increases.

**Boosting (8.2.3):**
- Trees grown **sequentially**, each using info from prior trees. **No bootstrap** — fit on a modified version of the data. Idea: **learn slowly**, fitting each new tree to the **residuals**, then add a shrunken version.
- **Algorithm 8.2 (regression):** init f̂(x)=0, r_i=y_i; for b=1..B: fit tree f̂^b with d splits to (X, r); `f̂(x) ← f̂(x) + λ f̂^b(x)`; `r_i ← r_i − λ f̂^b(x_i)`. Output `f̂(x) = Σ_b λ f̂^b(x)`.
- **Three tuning parameters:** (1) **B** — boosting **CAN overfit** if B too large; choose via CV. (2) **λ (shrinkage)** — small learning rate, typically 0.01 or 0.001; smaller λ needs larger B. (3) **d (splits/tree = interaction depth)** — d=1 = stump → additive model.
- Small trees (even stumps) often suffice.

**BART (8.2.4):** hybrid of RF (randomness) and boosting (captures unfit signal); each new tree is a random **perturbation** of the previous iteration's tree; uses a **burn-in** L; guards against overfitting; viewable as Bayesian/MCMC. Typical K=200, B=1000, L=100.

**Summary contrast (8.2.5):** Bagging = independent bootstrap trees. Random forests = bootstrap trees + random feature subset per split (decorrelated). Boosting = original data only, trees grown successively on leftover signal, shrunken. BART = original data, successive but perturbed trees.

## 2. Why it matters for Exam 1

- **Maps to ML Domain 7 (Ensemble Methods: bagging, random forests, boosting).**
- **Question themes:** averaging for variance reduction (and its limits — shared bias doesn't cancel); bootstrap sampling with replacement and OOB (~37% out-of-bag); bag **deep** (not shallow) trees; random-feature subsetting to **decorrelate** trees (m ≈ √p); boosting as sequential residual-fitting with a learning rate (additive, not majority vote); boosting can overfit with large B (unlike bagging/RF).

## 3. Sample questions with correct answers (verbatim from `Domain_07`)

### [ML-D7G1Q1] Motivation — averaging correlated regression trees
**Scenario:** A PM has five independently trained regression trees for next-day returns that are each moderately accurate but unstable across samples, and asks whether averaging their forecasts stabilizes position sizing without changing the universe.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Imperfectly correlated errors partially cancel in an average, so aggregation reduces prediction variance — the core variance-reduction argument for bagging/averaging. |
| B | False | An ensemble improves *expected* performance but carries no observation-by-observation guarantee to beat its best member on every future point. |
| C | True | A shared systematic directional bias does not disappear under averaging; only the uncorrelated (variance) component cancels. |
| D | True | Combining unstable learners can yield a more reliable aggregate than repeatedly selecting one learner, even when no single tree is consistently best. |
| E | False | Averaging uses all five outputs; it is not equivalent to selecting the single deepest tree's prediction. |

### [ML-D7G3Q1] Random-feature selection to decorrelate trees
**Scenario:** Bagged trees keep choosing recent momentum as the root split because it is strongest; the director suggests a random forest that considers only a random subset of features at each split so trees are not near-identical.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Restricting candidates at a split can force some trees to use alternative predictive features when momentum is unavailable. |
| B | True | Feature randomness is intended to increase diversity, decorrelating trees beyond bootstrap sampling alone. |
| C | False | Trees need not use disjoint feature sets; random subsets are re-drawn per split and features recur across trees. |
| D | True | Reducing correlation among useful trees improves the variance-reduction benefit of aggregation. |
| E | False | A random forest aggregates its trees' predictions by averaging or voting — it does not combine them without using predictions. |

### [ML-D7G5Q1] Boosting on residuals with a learning rate
**Scenario:** A quant builds a sequence of shallow regression trees where each new tree addresses remaining errors, and the lead explains the final forecast adds tree contributions using a learning rate.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Boosting trains later trees on information about earlier trees' errors, focusing on what the current ensemble missed. |
| B | True | This sequential dependence differs from bagging, where base learners can be trained independently. |
| C | False | The first tree need not perfectly fit the targets — remaining error is exactly what later learners reduce. |
| D | True | A smaller learning rate (shrinkage) makes each new tree's correction more conservative. |
| E | False | Regression boosting forms an additive, weighted prediction, not an unweighted majority vote. |
