# ML Domain 6 — Decision Trees

## Domain cheat-sheet

- **Prediction flow (G1):** A single decision tree routes each observation down **one** root-to-leaf path determined by the split rules; the prediction comes from **that one leaf only**, never by averaging/combining all leaves (that is ensembles). Nodes off the observation's path are not evaluated for that observation. A **leaf is terminal** (a prediction), not another split; an **internal node** applies a feature-based rule.
  - **Regression leaf** → prediction = **mean training response** in that leaf. **Classification leaf** → majority class / class-probabilities. A leaf may hold one *or many* training observations.
  - A root-to-leaf path = a **conjunction of if-then conditions** → the source of tree interpretability.
- **Splitting criteria (G2, G6):** CART is **greedy, top-down, recursive binary splitting** — at each node it does a *local exhaustive search* over every feature and threshold and picks the split with the **largest immediate impurity/error reduction**. Greedy = no lookahead; **locally optimal ≠ globally optimal**. Finding the truly optimal tree is NP-complete.
  - **Classification impurity:** Gini `G(p)=2p(1−p)` and cross-entropy `H(p)=−p ln p−(1−p)ln(1−p)`. Both = **0 at pure nodes** (p=0 or 1), **maximum at p=0.5**. Classification error `E=1−max_k p̂` is **less sensitive** to class-proportion changes → used for pruning, less for growing.
  - Weighted child impurity **can never exceed** parent impurity (concavity) → impurity reduction ≥ 0 (may equal 0).
- **Complexity & overfitting (G3):** Depth / number of leaves = model capacity. Unrestricted growth → leaves down to 1 observation → **0 training error but high variance / poor generalization** (memorizes noise, especially in low signal-to-noise financial data). Shallow/over-constrained → **underfitting (high bias)**. Bias–variance is the governing tradeoff.
- **Hyperparameters as controls (G4):** `max_depth` (caps root-to-leaf path length, uniform), `min_samples_leaf` (hard lower bound on leaf size → variance reduction), `min_samples_split` (min samples to *attempt* a split — does **not** guarantee leaf size), `max_leaf_nodes` (best-first / impurity-priority growth → asymmetric tree). These are **structural pre-pruning constraints**, distinct from L1/L2 penalties (they restrict allowed structures but keep the same impurity criterion). Cost-complexity pruning (α) is the penalized-objective analog.
- **Stability & sensitivity (G5):** Individual trees are **high-variance / unstable** — small data changes (add/remove a few rows, a near-tie between candidate splits) can flip an early split and cascade through all downstream branches. Same hyperparameters do **not** guarantee same tree across different samples. Motivates **bagging / random forests** (average many trees to lower variance). Equal aggregate accuracy does not imply stable per-case predictions.
- **Strengths (G6):** Handle **nonlinearity & interactions** via hierarchical conditional splits (no manual polynomial/spline/interaction terms); **no feature scaling needed** — splits depend on *ordering*, so any **strictly monotonic transform** (log, z-score, min-max) preserves the candidate partitions and the fitted tree (unlike distance-based KNN/SVM); **interpretable** if-then paths; implicit feature selection; relatively robust to feature-space outliers.
- **Weaknesses / failure modes (G7):** **Axis-aligned splits only** → a diagonal/oblique boundary needs a many-split "staircase" approximation; **cannot extrapolate** beyond training-response range (leaf outputs are bounded constants); **piecewise-constant** → abrupt jumps at thresholds; **greedy** can miss good multi-level structure if the first split's immediate gain is weak; **high variance / instability**; **overfitting** without constraints. A learned threshold is predictive, **not causal or permanent** (regime shift breaks it).

## Common traps

- **Inverted-logic questions (12 of 42):** the Answer Key flips scoring — "**True = incorrect; False = accurate**." So a verdict of **False actually means the statement is correct**. Read the polarity line first. Inverted here: **G1Q1, G2Q5, G2Q6, G3Q3, G4Q1, G4Q2, G4Q4, G4Q6, G6Q2, G6Q4, G7Q3, G7Q5.** (Verdicts below are shown as `True (incorrect)` / `False (accurate)` for these.)
- **Double-negative "embedded claim" choices:** a choice asserts that an accurate statement is *false/incorrect*, so the whole choice is false.
  - **G1Q1 A** ("The following claim is false: the observation first follows momentum>2%…") — inner claim is accurate, so the choice is incorrect → **True (incorrect)** under inverted scoring.
  - **G4Q3 A** ("The following claim is false: max depth and min leaf size both influence complexity") — inner claim accurate → whole choice false → **False** (normal scoring).
  - **G7Q4 A** ("It is incorrect to conclude that trees struggle with smooth/diagonal boundaries…") — inner conclusion is accurate, so calling it incorrect is **False** (normal scoring).
  - In inverted questions **G4Q4E, G4Q6A, G6Q2, G6Q4** the key literally writes "The statement is accurate → marked False" — read the polarity, not the word.
- **"Single tree averages all paths / combines all leaves"** is always wrong for one tree (that describes ensembles). One observation → one path → one leaf. (G1Q1C, G1Q4A.)
- **Scaling/standardization is NOT required for trees** — repeated distractor. Monotonic transforms only change reported threshold numbers, not the partitions/structure. Claiming scaling is *mandatory* is false; claiming a monotonic transform *stabilizes* the tree is also false (G5Q5B, G5Q6B). Trees are the contrast to distance-based KNN/SVM.
- **"Greedy = globally optimal / looks ahead"** is always wrong (G2Q3B, G2Q6B, G4Q6-related, G6Q5C, G6Q6E, G7Q5C). Greedy = best local split now, no lookahead.
- **`min_samples_split` ≠ guaranteed leaf size:** a node of 10 (or 100) can split into children of 1 and 9 (99), so only `min_samples_leaf` bounds leaf size (G4Q4C, G4Q6C).
- **Answer-key mismatch — G5Q5:** the key's letters are **shuffled relative to the choice text**. Verdicts below are mapped by **content** (the faithful reading) and flagged with a Note.

## Questions

### [ML-D6G1Q1] Prediction flow through one root-to-leaf path
**Scenario:** A tree predicts a positive next-day return: root tests 20-day momentum > 2%, then volatility < 1.5% → "positive" leaf. An observation has 3% momentum and 1.2% volatility. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Embedded double-negative: "the claim is false" that momentum>2% branch is taken — but 3% > 2% is satisfied, so the inner claim is accurate and calling it false is incorrect. |
| B | False (accurate) | Volatility 1.2% < 1.5% satisfies the second test, so the observation does follow that branch. |
| C | True (incorrect) | Wrong: a single tree predicts from the **one** leaf the observation reaches, not by combining outputs of every leaf (that is ensemble behavior). |
| D | False (accurate) | Correct: only tests along the observation's own root-to-leaf path affect its prediction; a split in an unvisited branch cannot change it. |
| E | False (accurate) | Correct: the scenario defines the reached leaf as carrying the "positive" prediction. |

**Reference:** Tree prediction flow / single-path routing — ISLR ch.8 (§8.1 tree basics); scikit-learn "Decision Trees" (prediction).

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

**Reference:** Regression-tree leaf mean prediction — ISLR §8.1 (regression trees); scikit-learn `DecisionTreeRegressor`.

### [ML-D6G1Q3] Interpreting a decision path as a rule
**Scenario:** A risk tree flags a trade for review via path leverage>2.0, liquidity≤40, holding period>10 days → "review" leaf. The tree has many other sector/market-cap nodes.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Those three tests were encountered in sequence before the prediction — they describe this trade's path. |
| B | False | Nodes off the selected path (sector, market cap) are not evaluated for this trade merely because they exist in the tree. |
| C | True | The root-to-leaf path translates into a conjunction (if-and-then) rule explaining the prediction. |
| D | True | Changing leverage so the opposite root branch is taken changes the subsequent path and possibly the leaf. |
| E | False | A leaf is terminal (gives a prediction); it is not another split sending the trade to children. |

**Reference:** Root-to-leaf paths as conjunctive rules / interpretability — ISLR §8.1; scikit-learn "Understanding the decision tree structure."

### [ML-D6G1Q4] Trees are not black boxes (junior-analyst claim)
**Scenario:** A CRO prefers trees for interpretable allocation logic; a junior analyst claims trees are black-box and hard to interpret. Evaluate that assumption.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Trees do **not** average all possible paths; each observation follows one path to one leaf. |
| B | False | No standardization required — threshold splits on individual variables, not distance calculations. |
| C | False | Individual splits are simple, but many combined splits capture nonlinearities and interactions. |
| D | False | Trees can be unstable: small data changes can alter selected splits → different structures. |
| E | True | Correct definition: prediction = routing through feature-based splits from root to a terminal leaf. |

**Reference:** Tree interpretability, nonlinearity, instability — ISLR §8.1; scikit-learn "Decision Trees" (advantages/disadvantages).

### [ML-D6G1Q5] CART regressor architecture (RSI + MA-crossover)
**Scenario:** A Decision Tree Regressor predicts next-month excess returns from RSI and an MA-crossover ratio, trained with squared-error impurity. Evaluate its axis-aligned, greedy, unstable, piecewise-constant behavior.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | CART evaluates one feature at a time; a split depends on which points fall each side of the threshold, not on relative feature scale → no standardization needed. |
| B | True | Splits X_j ≤ s are axis-aligned rectangles; a diagonal boundary X₁+X₂>C needs a many-split staircase approximation. |
| C | True | Greedy top-down recursive binary splitting selects the (feature, threshold) minimizing within-node squared error / maximizing impurity reduction. |
| D | True | Deep, minimally constrained trees have low training bias but high variance: a changed early split propagates through downstream branches. |
| E | False | A mean-predicting regression tree cannot extrapolate; out-of-range inputs still land in an existing leaf and get its bounded mean, so ŷ ∈ [y_min, y_max] of training. |

**Reference:** CART regression: axis-aligned splits, greedy SSE, variance, no extrapolation — ISLR §8.1; ESL ch.9 (CART).

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

**Reference:** Gini/entropy/classification-error impurity & concavity — ISLR §8.1; ESL §9.2.3.

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

**Reference:** Impurity-reduction split selection — ISLR §8.1; scikit-learn "Mathematical formulation" of tree splitting.

### [ML-D6G2Q2] Regression split groups similar targets
**Scenario:** A regression tree compares momentum/volatility thresholds at a node, scoring each by how much it reduces squared prediction error in the children.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A good split groups similar-target observations together, reducing residual variance/squared error. |
| B | True | Candidate thresholds are evaluated using the target values of the node's observations. |
| C | False | Balanced child sizes are not required unless separately constrained. |
| D | True | Greedy growth selects the candidate with the best local error reduction. |
| E | False | A greedy local choice does not prove global optimality of the completed tree. |

**Reference:** Regression-tree variance-reduction splitting / greedy growth — ISLR §8.1.

### [ML-D6G2Q3] Greedy local optimum ≠ global optimum
**Scenario:** The root picks a volatility split (largest immediate error reduction); later an analyst finds a momentum split with smaller immediate gain would have enabled better lower-level splits.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Choosing the best available split now is exactly greedy construction. |
| B | False | Standard growth does not revisit earlier splits or exhaustively optimize all complete trees. |
| C | True | A locally best split can yield a suboptimal overall tree. |
| D | False | The volatility split may still have had the largest immediate reduction — just not the best long-run structure. |
| E | True | Out-of-sample validation assesses whether the greedily-built tree generalizes. |

**Reference:** Greedy recursive binary splitting & suboptimality — ISLR §8.1; ESL §9.2.

### [ML-D6G2Q4] How splits are chosen; limitations
**Scenario:** A PM asks whether a tree's error-reducing splits amount to a globally optimized strategy. Explain split selection and its limits.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Trees use a greedy algorithm selecting the best split at each stage without checking all future combinations. |
| B | False | A locally optimal split does not guarantee a globally optimal tree. |
| C | True | Splitting criteria aim to make children more homogeneous / lower error than the parent. |
| D | False | Trees do not enumerate all future split combinations (computationally infeasible) — they build recursively/greedily. |
| E | True | Split quality is judged by impurity/error reduction in the resulting groups. |

**Reference:** Greedy split selection — ISLR §8.1; scikit-learn tree "Mathematical formulation."

### [ML-D6G2Q5] "Cleanest split" — true drivers vs. greedy limits (INVERTED)
**Scenario:** A tree picked a credit-quality split for the "cleanest" profit/loss separation; the PM asks whether it found true return drivers or if split-selection has limits. Mark True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a split is chosen for immediate objective improvement at the node, not because the feature is the dataset's most important factor. |
| B | True (incorrect) | Wrong: trees do **not** examine every possible future split sequence; they use greedy recursion (exhaustive search is infeasible). |
| C | True (incorrect) | Wrong: a near-root feature is highly predictive for the model but not guaranteed the strongest economic driver (correlation/interactions/greedy placement). |
| D | False (accurate) | Correct: a strong immediate split can foreclose a better overall structure (greedy limitation). |
| E | True (incorrect) | Wrong: tree construction is greedy/local, not global optimization accounting for all future outcomes. |

**Reference:** Greedy vs. global optimization; feature importance caveats — ISLR §8.1; ESL §9.2.

### [ML-D6G2Q6] CART greedy split mechanics + Gini extremes (INVERTED)
**Scenario:** A supervisor explains CART's top-down greedy evaluation using Gini/MSE for an Up/Down predictor. Mark each statement True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a local exhaustive search scans every feature and threshold to pick the max immediate impurity/error reduction. |
| B | True (incorrect) | Wrong: "greedy" means best choice now with **no** lookahead — it does not look 3–4 steps ahead. |
| C | True (incorrect) | Wrong: splits are local to their branch; changing the left branch does not auto-recalculate the right branch. |
| D | True (incorrect) | Wrong: Gini's **minimum 0.0** occurs at a **pure** node; a 50/50 mix is maximum impurity (Gini=0.5), not "perfectly pure." |
| E | False (accurate) | Correct: a single-class (100%) node is pure → Gini = 0. |

**Reference:** Greedy local search & Gini extremes — ISLR §8.1; scikit-learn tree criteria.

### [ML-D6G3Q1] Fully-grown tree overfits
**Scenario:** A tree grows until each training point has its own leaf: 0 training error, much higher test error, jagged predictions across nearby feature values.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Very low training error with much worse test error is the classic overfitting signature. |
| B | False | Pure/singleton training leaves do not guarantee accurate unseen predictions. |
| C | True | Unrestricted growth can encode sample-specific noise rather than stable structure. |
| D | True | Restricting growth can improve generalization even if training error rises. |
| E | False | Zero training error often coexists with **high** variance, not low. |

**Reference:** Overfitting / capacity & bias–variance — ISLR §8.1 (tree pruning); ESL ch.7.

### [ML-D6G3Q2] Shallow tree underfits an interaction
**Scenario:** A shallow tree has poor training *and* validation accuracy and cannot represent "momentum matters only in low-volatility periods."
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Poor performance even on training data indicates possible underfitting (insufficient capacity). |
| B | True | More permitted depth can express the sequential volatility→momentum conditional interaction. |
| C | False | Poor training performance can reflect an over-constrained learner, not absence of predictive structure. |
| D | True | A shallow tree has lower capacity than a deeper tree on the same features. |
| E | False | Making it even shallower reduces capacity further and worsens this underfitting. |

**Reference:** Underfitting / capacity & interactions — ISLR §8.1; ESL ch.7 (bias–variance).

### [ML-D6G3Q3] Depth sweep 1–30; validation U-curve (INVERTED)
**Scenario:** Training error falls throughout depths 1–30; validation error falls to depth 7 then rises; depth-30 leaves hold 1–2 observations. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: falling training error alone doesn't identify the best-generalizing depth. |
| B | False (accurate) | Correct: rising validation error past depth 7 indicates increasing overfitting. |
| C | False (accurate) | Correct: tiny leaves make predictions depend heavily on a few observations. |
| D | True (incorrect) | Wrong: depth should be chosen on validation performance, not lowest training error. |
| E | False (accurate) | Correct: the final test set must stay separate from depth selection for an unbiased estimate. |

**Reference:** Validation-based complexity selection; small-leaf variance — ISLR §8.1 & ch.5 (CV); ESL ch.7.

### [ML-D6G3Q4] Unrestricted deep tree: variance, hyper-rectangles
**Scenario:** An unconstrained regime classifier grows to depth 28 with pure leaves, 0% training error, but sharply degraded live performance. Evaluate overfitting/complexity/variance.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Deep unrestricted trees fit training noise → severe overfitting and poor generalization; they do **not** guarantee low OOS error. |
| B | True | Without constraints, trees split until leaves are pure / below min_samples_split, memorizing noisy instances → fragmented boundaries. |
| C | False | Deep unrestricted trees have **low bias, high variance** — not high bias/low variance. |
| D | True | In low signal-to-noise financial data, deep leaves isolate tiny subsets and treat noise as signal. |
| E | True | A K-leaf tree partitions the space into K non-overlapping axis-aligned hyper-rectangles, each predicting from few samples. |

**Reference:** Unrestricted growth → high variance; hyper-rectangular partitions — ISLR §8.1; ESL §9.2.

### [ML-D6G3Q5] Zero training error ≠ deterministic process
**Scenario:** A Decision Tree Regressor on 500 daily observations grows until nearly one obs/leaf: MSE_train=0, R²=1, but test MSE worse than a mean baseline.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Deeper trees reduce training bias but raise variance (more sensitive to the particular sample/noise). |
| B | True | Axis-aligned splits shrink regions; single-observation leaves let the tree memorize exact responses. |
| C | False | Zero training error shows only interpolation capacity, not that returns are a deterministic noise-free function of the 15 features. |
| D | False | p features impose **no** log₂(p) depth cap — a tree can split repeatedly on the same feature; depth relates to N/arrangement (log₂N balanced up to N−1 unbalanced). |
| E | True | Deep splits act on small subsets → more likely to capture localized, sample-specific variation that fails to generalize. |

**Reference:** Interpolation vs. true process; depth not bounded by p; deep-split variance — ISLR §8.1; ESL ch.7.

### [ML-D6G3Q6] Deep vs. constrained tree (Model A vs. B)
**Scenario:** Model A (unconstrained, pure leaves) vs. Model B (max_depth=4, min_samples_leaf=50) for 3-class liquidity regimes. Explain depth/leaf-size/overfitting.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Model A's unconstrained depth isolates partitions around each training sample → 0 training error, memorizing noise. |
| B | True | min_samples_leaf=50 averages each leaf over ≥50 points → variance reduction, smoother boundaries. |
| C | False | Deep trees show **low bias, high variance** (prone to overfitting), not high bias/low variance/underfitting. |
| D | True | A slight change near a high-depth split can alter the whole subtree beneath it — high variance of deep trees. |
| E | False | Model B is **not** guaranteed lower training error (Model A hits 0); constraints reduce capacity, and CART stays greedy (no more "global" root splits). |

**Reference:** Depth/leaf-size vs. bias–variance; greedy still greedy — ISLR §8.1; scikit-learn tree hyperparameters.

### [ML-D6G4Q1] max_depth as regularization (INVERTED)
**Scenario:** A regression tree changed from unlimited depth to max_depth=4: fewer leaves, slightly higher training error, lower validation error. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: max_depth caps the length of root-to-leaf decision paths (split levels). |
| B | False (accurate) | Correct: higher training error is consistent with reduced capacity. |
| C | False (accurate) | Correct: lower validation error suggests the depth cap improved generalization here. |
| D | True (incorrect) | Wrong: no single depth is best for every dataset — appropriate complexity is data/task/validation dependent. |
| E | False (accurate) | Correct: limiting depth reduces flexibility and acts as regularization. |

**Reference:** max_depth as pre-pruning/regularization — ISLR §8.1; scikit-learn `max_depth`.

### [ML-D6G4Q2] Raising min_samples_leaf; tradeoffs (INVERTED)
**Scenario:** min leaf size raised from 1 to 50. Rare genuine regimes have only 20 examples; some isolated mislabeled records exist. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a larger minimum leaf size prevents singleton leaves from isolated records. |
| B | False (accurate) | Correct: aggregating more observations makes leaf estimates less sample-sensitive → lower variance. |
| C | False (accurate) | Correct: genuine 20-obs regimes may be merged away and become harder to detect. |
| D | True (incorrect) | Wrong: stronger constraints can **increase bias and cause underfitting**, not only reduce bias. |
| E | False (accurate) | Correct: the setting trades off robustness against preservation of local structure. |

**Reference:** min_samples_leaf variance/bias tradeoff — ISLR §8.1; scikit-learn `min_samples_leaf`.

### [ML-D6G4Q3] Jointly tuning depth and leaf size
**Scenario:** Candidate 1: depth 20, leaves ≥2 (fits training closely). Candidate 2: depth 6, leaves ≥100 (smoother). Compare.
**Answer polarity:** Normal (True = accurate). Note embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded double-negative: the inner claim (both max_depth and min leaf size influence effective complexity) is accurate, so "the following claim is false" is itself false. |
| B | True | Greater permitted depth and smaller leaves allow finer, more localized partitions. |
| C | False | The simpler candidate may generalize better *or* underfit — validation is required, not guaranteed lower test error. |
| D | True | Validation data estimates the generalization tradeoff among candidate settings. |
| E | True | Tuning on the final test set leaks test information into model selection, compromising its role. |

**Reference:** Depth & leaf-size as joint complexity controls; validation vs. test — ISLR §8.1 & ch.5; scikit-learn model selection.

### [ML-D6G4Q4] Structural controls vs. L1/L2 (INVERTED)
**Scenario:** Tuning max_depth, min_samples_split, min_samples_leaf, max_leaf_nodes on a 10k-bar momentum classifier. Mark each True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: increasing min_samples_leaf blocks splits producing children below the threshold → variance reduction. |
| B | False (accurate) | Correct: decreasing max_depth lowers capacity/variance and raises bias via coarser partitions. |
| C | True (incorrect) | Wrong: min_samples_split governs eligibility to split (e.g., 100→99/1 children); it does **not** guarantee every leaf has ≥100 obs — only min_samples_leaf does. |
| D | False (accurate) | Correct: max_leaf_nodes grows best-first by impurity reduction → asymmetric tree under a fixed leaf budget. |
| E | False (accurate) | Correct: max_depth/min_samples_leaf are structural pre-pruning constraints that keep the same impurity criterion, unlike L1/L2 penalty terms. |

**Reference:** Structural constraints vs. penalty regularization — ISLR §8.1 (pruning); scikit-learn tree hyperparameters.

### [ML-D6G4Q5] Complexity controls improve reliability
**Scenario:** A tree with hundreds of branches perfectly classifies training data but is inconsistent across new market periods. How can complexity controls help without discarding useful patterns?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Deeper trees add splits and capture more detailed patterns/interactions (but can fit noise). |
| B | True | Limiting depth prevents overly specific rules from small subsets → less overfitting. |
| C | False | Increasing minimum leaf size makes the tree **less** flexible and lowers variance, not more flexible. |
| D | False | Unlimited depth can memorize training data and generalize poorly — more complexity ≠ better generalization. |
| E | True | max_depth/min leaf size/pruning control the complexity–generalization tradeoff. |

**Reference:** Complexity controls & generalization — ISLR §8.1 (pruning); scikit-learn tree tuning.

### [ML-D6G4Q6] Four hyperparameter configs (INVERTED)
**Scenario:** Grid search over Config 1 (max_depth=3), Config 2 (min_samples_leaf=250), Config 3 (min_samples_split=10, leaf=1), Config 4 (max_leaf_nodes=16). Mark each True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: max_depth=3 caps paths at 3 splits → ≤2³=8 leaves; it is an upper bound, so branches may stop early / be asymmetric. |
| B | False (accurate) | Correct: min_samples_leaf=250 averages each leaf over ≥250 orders → stabilizes leaf variance. |
| C | True (incorrect) | Wrong: min_samples_split=10 governs split eligibility (can leave a child of 1); it does **not** force ≥10 per leaf — that needs min_samples_leaf. |
| D | False (accurate) | Correct: max_leaf_nodes uses best-first impurity-reduction growth → asymmetric, flexible capacity allocation. |
| E | False (accurate) | Correct: larger min_samples_leaf raises training error (bias) while lowering OOS variance. |

**Reference:** Hyperparameter semantics (depth, leaf, split, leaf_nodes) — ISLR §8.1; scikit-learn tree parameters.

### [ML-D6G5Q1] Instability from removing 5 observations
**Scenario:** Two trees, identical settings, datasets differing by 5 removed observations, choose different root features and give noticeably different predictions.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Large structural change from a small sample change is model instability. |
| B | True | An altered upper-level split changes the data reaching later splits (cascade). |
| C | False | Identical hyperparameters don't guarantee identical trees — structure depends on the particular sample. |
| D | True | Different structures can still coincide on predictions in some regions. |
| E | False | Low training error doesn't establish reliable predictions across samples / unseen data. |

**Reference:** Tree instability / high variance — ISLR §8.2 (bagging motivation); ESL §9.2.

### [ML-D6G5Q2] Near-tie between candidate splits
**Scenario:** Momentum and volatility give near-identical impurity reductions; one new day tips volatility ahead, replacing momentum at that node and changing lower branches.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Near-ties make structure sensitive: a small perturbation can reverse near-equal criterion values. |
| B | True | Replacing one split changes which observations reach descendant nodes. |
| C | False | The choice is sample/criterion dependent, especially in a near-tie — not proof volatility is universally more important. |
| D | True | Predictions far from affected regions can remain unchanged. |
| E | False | Determinism fixes output for a *given* dataset, not across different datasets. |

**Reference:** Near-tie sensitivity / instability — ISLR §8.2; ESL §9.2.

### [ML-D6G5Q3] Fluctuating signals despite similar accuracy
**Scenario:** A team retrains one tree monthly; feature-importance rankings and signals fluctuate though aggregate validation accuracy stays similar. Assessing reliability.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Similar aggregate accuracy doesn't guarantee stable individual predictions. |
| B | True | Comparing outputs across resampled/rolling training sets reveals sensitivity. |
| C | False | Equal summary scores can come from substantially different structures/decisions. |
| D | True | Unstable signals create turnover, shifting exposures, unreliable behavior — operational risk. |
| E | False | Prediction consistency matters for risk, costs, trust, and deployment controls. |

**Reference:** Stability assessment / resampling — ISLR §8.2 (bagging); ESL ch.7–8.

### [ML-D6G5Q4] Instability motivates ensembles
**Scenario:** Two analysts retrain on nearly identical datasets (a few recent observations differ) and get noticeably different trees/predictions. Is this expected and what does it imply?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Small data changes can alter the optimal-looking split → different structure (trees are unstable). |
| B | False | Nearly identical datasets are **not** guaranteed to produce identical split sequences. |
| C | True | Instability of single trees is a primary motivation for bagging and random forests. |
| D | False | Structural change is a known property of greedy tree construction, not evidence the algorithm is wrong. |
| E | True | High sensitivity to small training changes = high variance; trees are the classic example. |

**Reference:** Instability → bagging/random forests — ISLR §8.2; ESL §8.7, §15.

### [ML-D6G5Q5] Structural instability mechanics (ANSWER-KEY LETTERS SCRAMBLED)
**Scenario:** Removing 5 of 2,000 trading days (0.25%) flips the root split from RSI to 10-day volatility, producing a substantially different tree and different predicted regimes for hundreds of dates.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Trees are high-variance: greedy hierarchical construction makes every downstream split conditional on those above, so an early change alters much of the tree. |
| B | False | A strictly monotonic transform preserves ordering/candidate partitions, so it does **not** stabilize the tree against added/removed observations (claim of "reduces instability by changing ordering" is wrong). |
| C | True | Structural instability produces changing feature-importance rankings and inconsistent signals on retrain → turnover, transaction costs, unintended exposures. |
| D | True | Variance/sample-sensitivity of single trees is a core motivation for bagging and random forests (aggregate many trees → more stable). |
| E | True | Increasing permitted depth generally increases instability: deeper trees form more localized partitions sensitive to small sample changes. |

**Note:** The source Answer Key mislabels this item — its verdict letters are shuffled relative to the choice text (key "B/C/D" restate choices C/D/B respectively, and key "D. False" is the monotonic-transform statement = choice B). Verdicts above are mapped by **content** to preserve the authoritative True/False on each actual statement: A True, B False, C True, D True, E True.

**Reference:** High variance / instability & monotonic-transform invariance — ISLR §8.1–8.2; ESL §9.2.

### [ML-D6G5Q6] Adding 5 new observations re-organizes the tree
**Scenario:** Appending 5 new days to a 3-year dataset flips the root split and reorganizes all downstream splits, drastically altering backtest allocations. Explain the mechanics.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Trees use **local greedy** splitting, not global optimization; a small change near the root can pick a different split and cascade — not just localized leaf tweaks. |
| B | False | A strictly monotonic transform (ln, z-score) preserves ordering/partitions, so it does **not** inherently stabilize the tree against sample changes. |
| C | False | Deeper trees increase capacity/variance and instability — they do **not** buffer the root against perturbations. |
| D | True | Single-tree structural sensitivity drives model variance → core motivation for bagging/random forests over bootstrapped trees. |
| E | False | Trees evaluate splits feature-by-feature; skewed/outlier ticks near thresholds can displace split points → trees are sensitive to noisy data. |

**Reference:** Local greedy sensitivity; monotonic invariance; ensemble motivation — ISLR §8.1–8.2; ESL §9.2, §15.

### [ML-D6G6Q1] Representing an interaction via sequential splits
**Scenario:** Positive momentum predicts gains only when volatility < 2% (reverses when higher). The tree splits on volatility first, then uses different momentum thresholds per branch.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Separate branches apply different momentum rules to low- vs. high-volatility regions. |
| B | True | Hierarchical splits model nonlinear interactions without an explicit momentum×volatility feature. |
| C | False | Trees are not limited to one global linear coefficient for momentum. |
| D | True | Each root-to-leaf path defines a conditional if-and-then rule. |
| E | False | Representational capacity does not eliminate estimation error / overfitting risk on small noisy samples. |

**Reference:** Interaction modeling via hierarchical splits — ISLR §8.1; ESL §9.2.

### [ML-D6G6Q2] Scaling not required for trees (INVERTED)
**Scenario:** Return (decimal), volume (shares), volatility (%). Analyst multiplies volume by 1,000 and asks whether an ordinary tree must standardize first. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: splits compare values within one feature, so mixed units don't distort a cross-feature distance. |
| B | False (accurate) | Correct: a positive rescaling changes thresholds but preserves volume ordering → equivalent partitions. |
| C | True (incorrect) | Wrong: standardization is **not** mandatory for a tree to function. |
| D | False (accurate) | Correct: distance-based methods (Euclidean) are sensitive to scale even when tree partitions are unchanged. |
| E | True (incorrect) | Wrong: not needing scaling doesn't mean irrelevant features are harmless — they can drive spurious splits/overfitting. |

**Reference:** Scale invariance of trees vs. distance methods — ISLR §8.1; scikit-learn "Tips on practical use."

### [ML-D6G6Q3] Interpretability as a model-selection factor
**Scenario:** A small tree rejects a trade via 4 nodes (traceable); a deeper alternative has slightly better validation accuracy.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The small tree gives a human-readable path explaining this individual rejection. |
| B | True | Root-to-leaf paths can be presented as explicit conditional rules to stakeholders. |
| C | False | Large/deep trees can become hard to understand — interpretability is not constant across size. |
| D | True | Deployment can balance accuracy against transparency/governance. |
| E | False | A readable path permits inspection but does not prove economic validity, fairness, or causality. |

**Reference:** Interpretability tradeoffs — ISLR §8.1; scikit-learn tree advantages/limits.

### [ML-D6G6Q4] Tree strengths vs. logistic regression (INVERTED)
**Scenario:** Replacing an engineered logistic model with a Decision Tree Classifier for credit-default risk; evaluate strengths/limits on scaling, nonlinearity, data prep, computation, interpretability. Mark True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a strictly monotonic transform changes thresholds but preserves candidate partitions. |
| B | False (accurate) | Correct: hierarchical conditional splits represent nonlinearity/interactions without manual polynomial/spline/interaction terms. |
| C | True (incorrect) | Wrong: native categorical handling and surrogate splits for missing values are **implementation-dependent**, not universal CART requirements. |
| D | False (accurate) | Correct: axis-aligned partitions give traceable root-to-leaf if-then explanations for a prediction. |
| E | True (incorrect) | Wrong: greedy best-split does **not** yield a globally optimal tree, and CV/pruning/complexity controls are still needed. |

**Reference:** Tree strengths & implementation caveats — ISLR §8.1; scikit-learn "Decision Trees" (advantages/disadvantages).

### [ML-D6G6Q5] Trees vs. neural network for auditability
**Scenario:** A PM explains choosing a Decision Tree Regressor over an MLP for a compliance auditor requiring auditability, scale-invariance, and raw-feature handling.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Trees need little scaling: splits depend on ordering, and monotonic transforms (log, min-max) preserve candidate partitions (barring ties/precision exceptions). |
| B | False | Unconstrained trees are prone to overfitting; they do **not** auto-cap depth when variance exceeds bias. |
| C | False | CART is greedy/local; the globally optimal tree is NP-complete — no linear-time global guarantee. |
| D | False | Trees build non-linear axis-aligned step partitions, not smooth linear hyperplanes; not equivalent to linear regression. |
| E | True | Trees do implicit feature selection, capture conditional nonlinear interactions, and give transparent if-then paths. |

**Reference:** Tree strengths (scale invariance, interpretability) & greedy limits — ISLR §8.1; ESL §9.2.

### [ML-D6G6Q6] Tree strengths vs. logistic regression (credit scoring)
**Scenario:** A Decision Tree Classifier vs. logistic regression for corporate-bond default; the analyst lists practical tree advantages.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Splits depend on rank ordering, so trees are relatively robust to feature-space outliers (not fully immune, but less magnitude-driven). |
| B | False | Trees give piecewise-constant predictions, not continuous slope coefficients like linear/logistic regression. |
| C | True | Hierarchical splitting models nonlinear boundaries and interactions without manual interaction/polynomial terms. |
| D | True | Unlike distance-based KNN/SVM, trees don't require standardization/scaling. |
| E | False | Unconstrained trees do **not** guarantee the globally optimal partition — CART is greedy; global optimum is NP-complete. |

**Reference:** Tree strengths vs. distance/linear methods; greedy limits — ISLR §8.1; ESL §9.2.

### [ML-D6G7Q1] Singleton leaves memorize noise
**Scenario:** An unconstrained tree on 40 indicators has several single-day leaves, ~0 training error, poor OOS results.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | High capacity can capture accidental sample patterns rather than durable relationships. |
| B | True | Singleton leaves estimate output from one possibly unrepresentative observation. |
| C | False | Near-zero training error does not rule out overfitting — it often accompanies it. |
| D | True | Complexity constraints/pruning are reasonable remedies to evaluate. |
| E | False | Interpretability does not compensate for failure to generalize. |

**Reference:** Overfitting via tiny leaves; pruning — ISLR §8.1; ESL ch.7.

### [ML-D6G7Q2] Axis-aligned splits vs. a diagonal boundary
**Scenario:** A tree with only axis-aligned splits approximates an approximately diagonal true boundary using many small rectangles.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A single axis-aligned split tests one feature against a threshold. |
| B | True | Approximating a diagonal boundary needs multiple splits (a staircase). |
| C | True | More splits raise complexity and overfitting risk. |
| D | False | Collections of splits form nonlinear piecewise-constant regions — trees are not limited to linear boundaries. |
| E | False | Sufficient data are still needed to estimate the more detailed structure reliably. |

**Reference:** Axis-aligned staircase approximation — ISLR §8.1; ESL §9.2.

### [ML-D6G7Q3] Threshold discontinuity & regime dependence (INVERTED)
**Scenario:** A bull-market tree: momentum > 1.00% → large positive forecast, ≤ 1.00% → negative. Two observations have momentum 0.99% and 1.01%. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: nearly identical momenta on opposite sides of the threshold can reach different leaves → very different predictions. |
| B | False (accurate) | Correct: piecewise-constant leaves create abrupt jumps at split boundaries. |
| C | True (incorrect) | Wrong: a predictive threshold from historical data does not establish a permanent causal law. |
| D | False (accurate) | Correct: regime/distribution change can make the historical partition unreliable. |
| E | False (accurate) | Correct: time-ordered out-of-sample testing can reveal this generalization failure. |

**Reference:** Piecewise-constant discontinuity; regime shift ≠ causality — ISLR §8.1; ESL §9.2.

### [ML-D6G7Q4] Weaknesses post-mortem (momentum strategy)
**Scenario:** An unconstrained Decision Tree Classifier on 25 HFT indicators has severe drawdown and turnover in paper trading. Evaluate weaknesses/failure modes.
**Answer polarity:** Normal (True = accurate). Note embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded double-negative: the inner conclusion (trees struggle with smooth/diagonal boundaries, needing a staircase of axis-aligned splits) is accurate, so calling it "incorrect" is false. |
| B | True | Recursive splitting isolates small subsets, so deep leaves fit random fluctuations rather than true signals. |
| C | False | Trees **cannot** extrapolate; leaves give constant step values, not continuous linear regressions on unseen ranges. |
| D | True | Greedy top-down search can miss good multi-level combinations if the initial split's immediate impurity reduction is weak. |
| E | True | A tiny perturbation can flip the root split and cascade a full topology change (high variance). |

**Reference:** Diagonal-boundary inefficiency, no extrapolation, greedy limits, instability — ISLR §8.1; ESL §9.2.

### [ML-D6G7Q5] Weaknesses of a single regressor (INVERTED)
**Scenario:** A single Decision Tree Regressor for volatility (15 inputs) fails under regime shifts with high turnover on minor updates. Mark each True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: axis-aligned splits force a high-depth staircase to model a diagonal boundary. |
| B | True (incorrect) | Wrong: trees **cannot** extrapolate beyond training ranges; leaves give bounded constants, not continuous regression lines. |
| C | True (incorrect) | Wrong: CART is greedy/local and does **not** perform a global combinatorial search; global optimum is NP-complete. |
| D | True (incorrect) | Wrong: single trees are **not** robust — a small perturbation near the root can restructure the whole tree (high variance). |
| E | False (accurate) | Correct: unconstrained deep trees isolate tiny samples in noisy data → high variance, fitting noise as signal. |

**Reference:** No extrapolation, greedy NP-completeness, instability, high variance — ISLR §8.1; ESL §9.2.

### [ML-D6G7Q6] Single-tree limitations vs. simpler models
**Scenario:** A junior analyst argues trees (nonlinear + interactions) should always beat linear regression. Evaluate limitations of relying on a single tree before production.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Single trees are high-variance: small data changes alter selected splits → different structures/predictions. |
| B | False | No model is guaranteed to outperform others on unseen data (no free lunch); it depends on data/sample size/bias–variance. |
| C | True | Deep unconstrained trees can memorize noise, hurting generalization. |
| D | False | More complexity generally improves training but can worsen test performance (overfitting). |
| E | True | Controlling complexity (hyperparameters/pruning) often improves out-of-sample performance even if training accuracy drops. |

**Reference:** Single-tree variance, no-free-lunch, complexity control — ISLR §8.1–8.2; ESL ch.7.

## References (domain-level)

1. **ISLR — *An Introduction to Statistical Learning* (James, Witten, Hastie, Tibshirani), ch.8 (Tree-Based Methods):** §8.1 (regression & classification trees, recursive binary splitting, Gini/entropy/classification-error impurity, tree pruning / cost-complexity α, interpretability, axis-aligned splits and their limits); §8.2 (bagging, random forests — the variance-reduction motivation for tree instability).
2. **ESL — *The Elements of Statistical Learning* (Hastie, Tibshirani, Friedman):** §9.2 (CART — greedy recursive splitting, impurity measures, cost-complexity pruning); ch.7 (bias–variance, model assessment); §8.7 & ch.15 (bagging, random forests).
3. **scikit-learn User Guide — "Decision Trees":** mathematical formulation of splitting, `DecisionTreeClassifier`/`DecisionTreeRegressor`, hyperparameters (`max_depth`, `min_samples_split`, `min_samples_leaf`, `max_leaf_nodes`), advantages/disadvantages (no scaling needed, overfitting, instability), and "Understanding the decision tree structure."
4. **J. R. Quinlan — ID3/C4.5 (induction of decision trees):** information-gain / entropy-based splitting and greedy top-down tree induction; historical complement to CART's Gini/variance-reduction criteria.
5. **ML4T course material (Georgia Tech):** random-tree construction and the "correlation-of-feature" split-selection detail (choosing a feature by correlation with the target and taking the mean of two random A-cut instances as the split value); axis-aligned partitioning and leaf-mean prediction.
6. **Breiman, Friedman, Olshen & Stone — *Classification and Regression Trees* (CART, 1984):** the foundational reference for greedy binary splitting, impurity reduction, surrogate splits for missing values, and cost-complexity pruning.
