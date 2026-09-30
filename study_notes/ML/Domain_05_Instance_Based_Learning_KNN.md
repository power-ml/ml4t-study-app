# ML Domain 5 — Instance-Based Learning (KNN)

## Domain cheat-sheet

- **KNN core idea:** predict a query from the *k* stored training observations closest to it under a chosen distance metric. Classification = majority (or weighted) vote of neighbor labels; regression = (weighted) average of neighbor targets. It is **non-parametric** — no global equation is fit; predictions are local.
- **Distance & similarity (G1):**
  - Ordinary **Euclidean distance** `d(x,y)=√Σ(xᵢ−yᵢ)²` uses raw numerical differences and does **not** auto-correct for units. A feature with a much larger numerical range **dominates** the distance and drives neighbor selection.
  - **Manhattan** distance `Σ|xᵢ−yᵢ|` sums absolute differences (no squaring) but still uses raw magnitudes → switching metric does **not** fix scale imbalance.
  - **Feature scaling** (z-score `(x−μ)/σ`, min-max, rank/percentile) makes contributions comparable. Fit scaler on **training data only** (μ, σ, min/max, ranks) → apply to val/test/future to avoid **leakage**.
  - Different metrics can rank the *same* candidates differently; the metric is a **hyperparameter** chosen with train/validation, never the test set. Scaling improves comparability but does **not** make distinct metrics equivalent, nor make an irrelevant/identifier feature meaningful.
  - **Cosine similarity** is invariant to scaling the *whole vector* by a positive scalar, but **not** to rescaling individual features.
- **Choice of k / bias–variance (G2):**
  - **Small k (k=1):** low bias, **high variance**; jagged boundary / Voronoi cells; ~0 training error; overfits noise.
  - **Large k:** high bias, low variance; smoother boundary; can **oversmooth** real local structure (underfit). At **k=N** every query returns the global mean (regression) / majority class (classification) — feature-independent, max bias.
  - Capacity heuristic: **DoF ≈ N/k** (inverse to k). Training error alone never selects k; use **validation / cross-validation**. Test error is typically **U-shaped** in k.
  - Even k is **valid** for regression (averaging targets, no tie-breaking vote needed).
- **Noise & local structure (G3):** a single mislabeled/erroneous neighbor can dominate at k=1; larger k dilutes it (one of k votes) but not unconditionally (numerous/clustered/boundary outliers). Outlier influence is **strictly local** (unlike a high-leverage point in OLS). Neighbor selection uses **feature distance, not target extremeness**. Data cleaning helps a lazy learner, but not all outliers are errors (real crashes/shocks carry signal).
- **Curse of dimensionality (G4):** adding irrelevant dimensions injects noise into distances; data becomes **sparse** relative to volume (to cover fraction q in p dims, side length r=q^(1/p)→1); **distance concentration** shrinks (Dmax−Dmin)/Dmin→0 so "near" vs "far" loses contrast. Scaling does **not** cure this; feature selection / dimensionality reduction (PCA) can — but PCA fit on the test period still **leaks**, and reduction is not guaranteed to help.
- **Computational tradeoffs (G5):** KNN is a **lazy learner** — training ≈ O(1) (just store data); brute-force inference ≈ **O(N·p)** per query and memory ≈ **O(N·p)** (retains all instances). k-d / ball trees give ~O(log N) only in **low** dimensions; they degrade to O(N) once p ≳ 20–30. Eager models (linear/logistic) pay upfront but infer in ~O(p). k = neighbors used, **not** the count stored.
- **Trading suitability (G6):** wrong for ultra-low-latency/HFT (per-query search blows the microsecond budget); **ANN** methods (HNSW, LSH) trade recall for speed to make it viable. Fine for low-frequency/offline tasks (daily TAA, regime detection, illiquid pricing) and offers **interpretability** ("today resembles these historical dates"). Appending data is cheap but does **not** solve concept drift — stale windows must be pruned. Large neighbor distance is itself a **signal** the query is unlike history (supports abstention).

## Common traps

- **Inverted-logic questions (8 of 36):** the Answer Key reads "**True = incorrect; False = accurate**," so a "True" verdict means the statement is *wrong* and "False" means it is *correct*. Read the polarity line first. Inverted here: **G1Q2, G1Q3, G1Q4, G2Q1, G2Q2, G4Q6, G5Q1, G5Q5.**
- **Double-negative "embedded claim" choices:** a choice wraps an inner claim in "The following claim is false: …" or "It is incorrect to conclude that …". Parse the inner claim, judge *its* truth, then negate. In **normal**-polarity questions the key marks an accurate embedded claim **False** (G2Q3A, G5Q6A) and an inaccurate one **True** (G6Q4A). An embedded claim also appears inside the **inverted** question **G1Q2A** ("The following claim is false: …"), where the negation compounds with the inverted polarity — resolve the inner claim first, then apply "True = incorrect."
- **Scale ≠ meaning ≠ relevance:** standardizing puts features on comparable scales but does **not** make an arbitrary identifier meaningful, guarantee equal predictive value, or cure the curse of dimensionality. Frequent distractor: "scaling proves every feature now contributes meaningfully" → false.
- **Changing the metric is not a scaling fix:** Manhattan (or any raw-magnitude metric) still lets a billions-vs-units feature dominate. Distractor that "Manhattan treats all features equally regardless of units" is false.
- **k=N ≠ zero variance / "single best neighbor is most stable":** k=N gives max bias but still sample-dependent (not literally zero variance); k=1 *maximizes* variance (a common reversed distractor claims k=1 minimizes it).
- **Lazy ≠ fast in production:** "no training" does not imply cheap inference; trees do **not** rescue high-dimensional search; storing raw data is **more** memory than a parameter vector. Appending data does not defeat concept drift.

## Questions

### [ML-D5G1Q1] Feature scaling & unit dominance in Euclidean distance
**Scenario:** A researcher predicts next-day return with KNN using unscaled daily return (≈ −0.03 to 0.03) and volume (1–500 million shares). Selected neighbors share near-identical volume but differ sharply in recent return.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Volume's numerical range dwarfs return's, so its squared differences dominate Euclidean distance and drive neighbor selection. |
| B | True | Changing volume's units (shares → millions) rescales its contribution to distance and can reorder which observations are nearest unless features are scaled consistently. |
| C | False | Ordinary Euclidean distance uses the supplied numbers as-is; it performs no automatic unit correction across features. |
| D | True | Z-score standardization from training statistics equalizes marginal scales so raw magnitude alone no longer decides similarity. |
| E | False | Scaling parameters (μ, σ) must come from training data only; including the test period leaks information and biases distances. |

**Reference:** Feature scaling for distance-based methods — ISLR ch.2 (KNN, §2.2.3); scikit-learn "Preprocessing data" (StandardScaler) + "Nearest Neighbors."

### [ML-D5G1Q2] Metrics can rank differently — INVERTED logic (embedded claim in A)
**Scenario:** A team represents each day with standardized momentum/volatility/liquidity and weighs Euclidean vs. Manhattan distance; one candidate differs moderately on all three features, another differs greatly on one but is close on the others. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Embedded claim "different metrics can rank the same neighbors differently" is *true*; the choice asserts that claim is false, so the choice is incorrect. Metrics encode similarity differently and can reorder neighbors. |
| B | False (accurate) | Correct: Euclidean squares coordinate differences, giving a large gap on one feature disproportionate influence. |
| C | False (accurate) | Correct: Manhattan distance is by definition the sum of absolute coordinate differences. |
| D | True (incorrect) | Wrong: standardization improves comparability but does not force distinct metrics to select identical neighbors. |
| E | False (accurate) | Correct: the metric is a hyperparameter, chosen with training/validation data, not final test performance. |

**Reference:** Distance-metric choice as hyperparameter — ISLR §2.2.3; scikit-learn "Nearest Neighbors" (metric parameter, Minkowski p=1 vs 2).

### [ML-D5G1Q3] Scale does not create meaning — INVERTED logic
**Scenario:** A KNN model uses standardized momentum, bid-ask spread, and an integer security identifier; validation is poor despite comparable scales. An analyst argues scaling proves every input now contributes meaningful similarity information. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: standardizing an arbitrary identifier does not make numerical closeness between IDs economically meaningful. |
| B | False (accurate) | Correct: useful distances need feature *meaning*, not just comparable *scale*. |
| C | False (accurate) | Correct: every included coordinate contributes to computed distances, so removing an irrelevant one can change neighbors. |
| D | True (incorrect) | Wrong: unit variance does not imply equal relevance or predictive value. |
| E | False (accurate) | Correct: an irrelevant coordinate can push genuinely similar observations apart and distort neighbor selection. |

**Reference:** Relevance vs. scale in distance models; feature selection — ESL ch.13 (prototype/nearest-neighbor methods); scikit-learn "Nearest Neighbors" + feature selection guide.

### [ML-D5G1Q4] KNN does not auto-weight features — INVERTED logic
**Scenario:** A quant builds KNN over daily returns, volume (millions), and market cap (billions); a junior analyst claims KNN will automatically decide which features matter. Evaluate whether the current representation yields meaningful similarity. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: two observations are "similar" if close under the chosen distance metric — the definition of KNN similarity. |
| B | False (accurate) | Correct: a feature with orders-of-magnitude larger values (market cap) can dominate distance unless scaled. |
| C | True (incorrect) | Wrong: Euclidean distance combines all features jointly, so scale differences *directly* change computed distances and neighbors. |
| D | False (accurate) | Correct: an inappropriate metric can yield neighbors that are numerically close but not meaningfully similar for the task. |
| E | False (accurate) | Correct: comparable scales let multiple relevant features contribute fairly to distance. |

**Reference:** KNN similarity & scaling — ISLR ch.2 (KNN); "Deep Learning: Foundations and Concepts" ch.1 (data preprocessing).

### [ML-D5G1Q5] Market-cap vs. debt-to-equity scale imbalance
**Scenario:** A KNN risk classifier uses raw market cap ($100M–$1T) and debt-to-equity (0–5) under Euclidean distance. In validation, changing D/E barely alters neighbors while small % changes in market cap reshuffle them. Which statements correctly explain or remedy this?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Euclidean distance uses absolute numerical differences, so market cap's hundreds-of-billions range dominates and drives neighbor ordering. |
| B | False | KNN is *highly* sensitive to scaling — distances are computed jointly, so rescaling one feature changes neighbors and predictions (not rank-invariant per feature). |
| C | True | D/E is not removed, but its numerical contribution becomes negligible; the 2-D neighborhood behaves almost 1-D (market cap only). |
| D | False | Manhattan distance still uses raw magnitudes, so a billions-scale gap keeps dominating; changing the metric does not address incompatible scales. |
| E | True | Z-score standardization (training μ, σ) makes contributions comparable, though it does not guarantee equal predictive/economic importance; fit on training data to avoid leakage. |

**Reference:** Scale dominance & standardization — ISLR §2.2 (KNN); scikit-learn StandardScaler + "common pitfalls / data leakage."

### [ML-D5G1Q6] Distance metrics + multiple scaling methods (VIX/yield/return)
**Scenario:** A regime-matching KNN uses VIX (10–80), 10Y yield (decimal ≈0.04), and S&P return (decimal). The manager weighs Euclidean, cosine, and several scalers, all fit on training data then applied unchanged. Which statements correctly describe metric/scaling effects?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | On raw features, VIX (tens of points) dwarfs decimal yield/return differences, so neighbor selection depends mainly on VIX. |
| B | False | Cosine similarity is invariant to scaling the *whole vector*, not to rescaling *individual* features; changing one feature's units changes vector orientation and cosine. |
| C | True | After z-scoring, a one-SD difference in any feature contributes equally (same squared term) to Euclidean distance — comparable, not equally predictive. |
| D | False | Min-max is not "necessarily superior"; extreme crisis observations can compress normal data into a narrow range, and z-score is likewise outlier-sensitive — robust/rank methods may be better. |
| E | True | Rank/percentile scaling keeps ordering while curbing extreme magnitudes, so it is invariant to strictly increasing (rank-preserving) transforms, at the cost of discarding gap-size information. |

**Reference:** Scaling methods & metric invariances — scikit-learn "Preprocessing" (StandardScaler, MinMaxScaler, QuantileTransformer/rank); cosine vs. Euclidean geometry.

### [ML-D5G2Q1] k=1 vs k=75 variance/bias — INVERTED logic
**Scenario:** KNN regressors predict five-day returns: k=1 gives near-zero training error but predictions swing when a few training points change; k=75 is stable but misses recurring local patterns. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: heavy dependence on individual observations = high variance for k=1. |
| B | False (accurate) | Correct: averaging over more neighbors smooths the fitted function. |
| C | False (accurate) | Correct: excessive averaging (k=75) can suppress real local structure → more bias than k=1. |
| D | True (incorrect) | Wrong: the k minimizing *training* error (very small k) can generalize poorly; it is not necessarily best. |
| E | False (accurate) | Correct: k is a hyperparameter, selected on validation data before final test evaluation. |

**Reference:** Bias–variance tradeoff & k — ISLR §2.2 (KNN, bias-variance); §5 (cross-validation for hyperparameters).

### [ML-D5G2Q2] Decision-boundary complexity vs k — INVERTED logic
**Scenario:** A bullish/bearish KNN classifier: at k=3 the boundary has many small bends and isolated pockets; at k=51 it is smoother and a small but genuine bearish region vanishes. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: small k gives a complex boundary that tracks local observations closely. |
| B | False (accurate) | Correct: larger k pulls in more distant votes and can erase small regions. |
| C | True (incorrect) | Wrong: increasing k does not *always* improve unseen accuracy — it eventually adds excessive bias (underfit). |
| D | False (accurate) | Correct: smoothing away a real local regime is exactly underfitting. |
| E | False (accurate) | Correct: the best k depends on the data distribution and must be assessed empirically. |

**Reference:** k vs. boundary complexity — ISLR §2.2.3 (KNN classifier, Fig. of k effects); scikit-learn "Nearest Neighbors Classification."

### [ML-D5G2Q3] k=N behavior & even-k validity (embedded claim in A)
**Scenario:** KNN regression on 120 observations with k ∈ {1,5,25,120} predicts next-week portfolio return. The PM asks what happens at the largest k and whether an even k is invalid for regression.
**Answer polarity:** Normal (True = accurate) — note embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | The embedded claim (k=120 equal-weight → every prediction is the mean of all targets) is *accurate*, so asserting it is false is itself false; equal-weight regression averages all selected neighbors' targets. |
| B | True | With the identical full set for every query, feature values no longer differentiate predictions — all get the same equal-weight mean. |
| C | False | Regression averages numerical targets; it needs no majority vote, so an even k is not invalid. |
| D | True | Global averaging (k=N) is stable (low variance) but can miss substantial local structure (higher bias) vs. k=1. |
| E | True | Distance-weighted KNN gives closer neighbors more influence — a valid alternative to equal weighting. |

**Reference:** k=N limit & weighting schemes — ISLR §2.2.3; scikit-learn "Nearest Neighbors" (weights='uniform' vs 'distance').

### [ML-D5G2Q4] Capacity, DoF ≈ N/k, and the k=1 / k=N extremes
**Scenario:** A KNN classifier for Up/Down equity direction over normalized order-flow features is tested across k=1..250 on 1,000 instances; the team analyzes how k shapes boundary complexity, bias, variance, and capacity.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | k=1 gives each point its own Voronoi cell → 100% training accuracy (low bias) but a boundary that wraps every noise spike (high variance, overfit). |
| B | False | k=1 *maximizes* variance, not minimizes it; a single neighbor makes predictions unstable to small training changes. |
| C | True | As k→N the boundary smooths and simplifies, lowering variance while raising bias as local dynamics are averaged away. |
| D | True | At k=N every query evaluates all points → predicts the global majority class everywhere (flat boundary, max bias, zero flexibility). |
| E | False | Increasing k *reduces* effective DoF (heuristic DoF ≈ N/k) and flexibility; smaller k means higher capacity, not larger k. |

**Reference:** Model capacity & DoF≈N/k — ISLR §2.2 (KNN flexibility, effective degrees of freedom); ESL ch.13.

### [ML-D5G2Q5] Choosing k as overfit/underfit balance
**Scenario:** For a KNN classifier of monthly market outperformance, a junior analyst wants k=1 for highest training accuracy; the Head of Research worries about live performance and asks for the k tradeoffs.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Very small k (k=1) closely tracks training data → low bias, high variance, overfit risk. |
| B | True | Larger k averages over more neighbors → smoother, less complex boundaries. |
| C | False | Increasing k makes predictions *less* sensitive to individual noisy points; extremely large k instead causes underfitting. |
| D | True | Selecting k balances overfitting (small k) against underfitting (large k) — the bias-variance tradeoff. |
| E | False | k strongly controls boundary complexity: small k → irregular, large k → smooth. |

**Reference:** k and the bias–variance tradeoff — ISLR §2.2 (KNN; bias-variance); scikit-learn "Nearest Neighbors Classification."

### [ML-D5G2Q6] KNN regression flexibility & U-shaped test error
**Scenario:** KNN regression forecasts next-week 10Y yield changes from two normalized features on N=500 weekly observations; the strategist sweeps k=1..500, comparing training error, validation error, and surface smoothness.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | At k=1 a training point is its own neighbor → fitted value equals its response (≈0 training error), a highly flexible surface with high noise sensitivity (ties/duplicates/LOO can prevent exactly zero). |
| B | False | Increasing k generally *raises* in-sample training error (broader averaging smooths away observation-specific fit); it does not have to decrease. |
| C | True | Larger k lowers variance but adds bias where the true relationship has sharp local variation across regimes. |
| D | True | At k=N every prediction is the training mean ȳ — a constant, feature-independent, high-bias surface. |
| E | False | Lower variance does not guarantee monotonically improving test error; bias rises with k, so test error is typically U-shaped — select k via validation/CV. |

**Reference:** KNN regression f̂(x₀)=(1/k)Σyᵢ, U-shaped test error — ISLR §2.2.3; §5 (cross-validation).

### [ML-D5G3Q1] Corrupted target & averaging over neighbors
**Scenario:** A KNN volatility regressor has one data-entry error giving an extreme target to a record whose features sit near a common market state; predictions there are extreme at k=1 and milder at k=15.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | At k=1 the single closest observation supplies the entire prediction, so the erroneous record alone can determine it. |
| B | True | Averaging over more neighbors makes the corrupted target just one component of the mean, reducing its influence. |
| C | False | Larger k does not *guarantee* zero influence — a noisy point can still be included and shift the aggregate. |
| D | True | Cleaning suspected errors improves a lazy learner because its stored examples *are* the model — no algorithm change needed. |
| E | False | Neighbor selection uses feature distance, not target extremeness; a far-away outlier is not selected just because its target is large. |

**Reference:** Noise sensitivity & data quality in instance-based learners — ISLR §2.2.3; ESL ch.13 (nearest-neighbor robustness).

### [ML-D5G3Q2] Local structure vs. a global linear model
**Scenario:** Returns follow two regimes (high- vs low-volatility). A global linear model and KNN are compared; KNN wins where enough historical observations sit near each query.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | KNN forms predictions from local neighborhoods, representing different local relationships without one global equation. |
| B | True | Prediction quality depends on whether relevant nearby examples exist for the query. |
| C | False | KNN is non-parametric and does not assume a single global linear relationship. |
| D | True | In sparse regions the nearest available cases can be poor analogues, yielding unreliable predictions. |
| E | False | Local averaging models nonlinear structure in regression too, not only classification. |

**Reference:** Non-parametric local modeling — ISLR §2.2.3 (KNN vs. linear); ch.7 (local/flexible methods).

### [ML-D5G3Q3] Mislabeled point, voting, and distance weighting
**Scenario:** A KNN classifier for trade profitability has a mislabeled point inside a dense "profitable" region; the team compares k=1, k=9, and distance-weighted voting.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | At k=1 queries nearest the mislabeled point inherit its wrong label, creating a small incorrect region. |
| B | True | With k=9 the surrounding correct labels can outvote a single mislabeled case. |
| C | False | Distance weighting does not *always* eliminate the effect — a close mislabeled neighbor can still get large weight. |
| D | True | If the mislabeled point is extremely close, common weighting rules (larger weight for smaller distance) can *increase* its influence. |
| E | False | KNN is not inherently robust to all label noise; stored bad labels directly affect later predictions, so label quality matters. |

**Reference:** Label noise & weighted voting — scikit-learn "Nearest Neighbors" (weights='distance'); ESL ch.13.

### [ML-D5G3Q4] Black-swan outliers, k, and local influence
**Scenario:** A KNN regime classifier (High vs Low Volatility) contains several black-swan days — short-lived, fat-tailed anomalies rather than persistent shifts. The analyst evaluates KNN's sensitivity to this noise and outliers.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | At k=1 a single anomalous point owns 100% of the vote, creating an isolated island ("lake") that misclassifies nearby test points. |
| B | False | Outlier influence in KNN is strictly *local* (bounded by the neighborhood), unlike a high-leverage point that pivots a global OLS line. |
| C | True | Larger k makes the anomaly one of k votes (more robust) but excessive k blurs genuine local regimes and adds bias — pick k via validation. |
| D | False | Reversed: a *small* k (k=1) is warped by an outlier deep in opposite-class points; a *large* k outvotes it. |
| E | True | Pre-filtering (Isolation Forest, distance-to-median) stabilizes KNN by keeping non-representative points out of stored neighborhoods. |

**Reference:** Local outlier influence vs. OLS leverage; outlier filtering — ESL ch.13; scikit-learn "Novelty and Outlier Detection."

### [ML-D5G3Q5] Noise, outliers, and k→N (reversed distractors)
**Scenario:** An instance-based regime model (Expansion vs Contraction) contains transient flash crashes and liquidity freezes that do not reflect persistent regimes. The manager evaluates how these noisy points affect boundaries and stability across k.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | k=1 gives *maximum* sensitivity to outliers (100% weight to one neighbor), creating an artificial "island," not protection. |
| B | True | k=20 makes a lone noisy point one of 20 votes, smoothing the boundary — robust but not guaranteed if outliers are numerous/clustered/near a boundary; too-large k oversmooths (use validation). |
| C | False | A distant outlier's influence is local (bounded by its neighborhood), unlike a high-leverage OLS point that shifts the global slope everywhere. |
| D | False | As k→N, KNN becomes *less* sensitive to individual noise (predicts global majority), not more. |
| E | False | At k=1 KNN does no filtering; it blindly picks the closest point even if it is an isolated anomaly, warping the boundary around it. |

**Reference:** k→N smoothing & local outlier influence — ISLR §2.2.3; ESL ch.13.

### [ML-D5G3Q6] When KNN behaves well vs. poorly under noise
**Scenario:** A junior analyst proposes KNN because it "looks at similar historical situations"; the PM worries that unusual events and noise cause unstable decisions and asks how KNN behaves under distorted local patterns before deployment.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | KNN depends directly on the closest examples, so one noisy/mislabeled nearby point can strongly sway a prediction. |
| B | False | Increasing k generally *reduces* sensitivity to individual noise (averaging), though excessively large k adds bias. |
| C | True | As a flexible non-parametric method, KNN performs well when similar observations have similar outcomes, even with complex/nonlinear relationships. |
| D | False | Not all outliers are errors — crashes/shocks can be genuine signal; blind removal can discard important information. |
| E | True | Because it relies on local neighborhoods, KNN is typically more affected by noisy labels/unusual points than global parametric models. |

**Reference:** Local sensitivity vs. global models; data-cleaning judgment — ISLR §2.2.3; ESL ch.13.

### [ML-D5G4Q1] Irrelevant dimensions degrade distances
**Scenario:** A KNN model starts with 5 economically motivated features; a developer adds 200 weak/irrelevant indicators expecting improvement. Validation falls and the nearest-neighbor distance becomes similar to many others' distances.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Irrelevant coordinates inject noise into the similarity calculation, degrading the distance measure. |
| B | True | In high dimensions distances concentrate, so nearest vs. farther observations become less distinguishable. |
| C | False | More features do not guarantee improvement — extra dimensions can distort rankings and increase sparsity. |
| D | True | Feature selection / dimensionality reduction can restore more meaningful neighborhoods. |
| E | False | Scaling addresses feature *magnitude*, not high-dimensional sparsity or distance concentration. |

**Reference:** Curse of dimensionality & distance concentration — ISLR §2.2.3 (KNN in high dimensions); ESL ch.2/13.

### [ML-D5G4Q2] Sparsity: fixed sample, more dimensions
**Scenario:** A researcher expands a KNN feature space from 2 to 10 dimensions but keeps 5,000 daily observations fixed, assuming the same sample still gives comparably local neighbors.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A fixed sample grows sparser relative to the space as dimensionality (and volume) increases. |
| B | True | Maintaining similar local coverage can require dramatically more data as dimensions are added. |
| C | False | The nearest point can be far in absolute terms — it is "nearest" only because all points are far. |
| D | True | Sparse neighborhoods force KNN to use observations that are not truly similar to the query. |
| E | False | The curse of dimensionality is statistical/geometric, not merely a storage-size problem. |

**Reference:** Data sparsity in high dimensions (r=q^(1/p)) — ISLR §2.2.3; ESL §2.5.

### [ML-D5G4Q3] PCA before KNN and leakage
**Scenario:** A model uses 80 standardized, largely redundant technical indicators; the team proposes PCA before KNN but plans to fit PCA once using all dates, including the test period.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Reducing redundant dimensions can make distance comparisons more informative. |
| B | True | Ordinary PCA builds components from input-feature variation and does not use the target. |
| C | False | Even without labels, fitting PCA on all dates lets test-period feature information shape the transform. |
| D | True | Unsupervised preprocessing can still leak when fit on the test-period distribution — fit within training only. |
| E | False | Dimensionality reduction is not guaranteed to help; useful information can be discarded, so validate empirically. |

**Reference:** Leakage from preprocessing fit on test data; PCA + KNN — scikit-learn "common pitfalls / data leakage," "Decomposition (PCA)"; ISLR ch.12.

### [ML-D5G4Q4] More features ≠ better neighbors
**Scenario:** A regime-classification team adds hundreds of indicators/alt-data/macro variables and the model shines on training data; the Risk Officer questions whether KNN can still find meaningful "similar days" in a huge feature space.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | In high dimensions distances become similar across points, making truly close neighbors hard to distinguish. |
| B | False | Extra features can hurt — irrelevant/noisy variables distort distance-based similarity. |
| C | True | Higher dimensionality spreads observations out, requiring more data to keep enough nearby examples. |
| D | True | The curse of dimensionality is exactly the difficulty of learning as dimensions grow and data becomes sparse. |
| E | False | KNN does not auto-ignore useless features; irrelevant/redundant ones change distances and worsen neighbor selection. |

**Reference:** Curse of dimensionality — ISLR §2.2.3; ESL §2.5.

### [ML-D5G4Q5] Sparsity, distance concentration, and remedies (with formulas)
**Scenario:** A KNN co-movement model expands from 3 standardized macro features to 250 standardized inputs and performs much worse out of sample; nearest and farthest training distances from a typical test point converge. Which statements correctly describe the curse of dimensionality here?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | With fixed N, adding dimensions makes points sparse relative to volume — capturing fraction q needs side length r=q^(1/p)→1, so "local" neighbors span most of each range. |
| B | True | Distance concentration: (Dmax−Dmin)/Dmin→0 (equivalently Dmin/Dmax→1) as p→∞, weakening the near/far contrast (not literally identical distances). |
| C | False | Standardization fixes units/marginal scales but not sparsity, concentration, irrelevant dimensions, or coverage — the model still lives in 250-D. |
| D | True | Each standardized irrelevant feature adds a nonzero term to squared distance; many such terms can swamp the few informative dimensions. |
| E | False | Manhattan or fractional distances change severity but still aggregate all 250 dims; none eliminates high-dimensional sparsity or guarantees good neighborhoods — feature selection/reduction may still be needed. |

**Reference:** Sparsity (r=q^{1/p}) & distance concentration — ISLR §2.2.3; ESL §2.5; Beyer et al. "When is nearest neighbor meaningful?"

### [ML-D5G4Q6] Does adding dimensions always help? — INVERTED logic
**Scenario:** A KNN model matching current-to-historical market conditions works well with 5 selected indicators but deteriorates after expanding to hundreds. The Head of Trading asks whether more information always makes the model smarter. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: irrelevant features change distances and reduce prediction quality. |
| B | False (accurate) | Correct: in high-D, "close" under a metric need not mean meaningfully similar (distances become indistinguishable). |
| C | False (accurate) | Correct: KNN is especially vulnerable to the curse of dimensionality because it depends on meaningful proximity. |
| D | True (incorrect) | Wrong: more dimensions do not reliably improve nearest-neighbor relationships — they add noise, sparsity, and less reliable similarity. |
| E | False (accurate) | Correct: feature selection can improve KNN by dropping variables that add noise without improving similarity. |

**Reference:** Curse of dimensionality & feature selection — ISLR §2.2.3; scikit-learn feature selection guide.

### [ML-D5G5Q1] Lazy learning, fitting vs. inference cost — INVERTED logic
**Scenario:** A desk compares linear regression with a brute-force KNN regressor that stores training data and does little work until a prediction arrives; the production team worries about response time as the dataset grows. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: KNN is a lazy learner — it defers most work to inference. |
| B | False (accurate) | Correct: basic KNN fitting mainly records data and config (little model-fitting cost). |
| C | False (accurate) | Correct: brute-force prediction may compute distances to many/all stored observations. |
| D | True (incorrect) | Wrong: KNN is not always faster — a linear model evaluates a compact equation while KNN must search for neighbors. |
| E | False (accurate) | Correct: more stored candidates generally increase inference time for brute-force search. |

**Reference:** Lazy vs. eager; O(N·p) inference — scikit-learn "Nearest Neighbors" (algorithm/complexity); ISLR §2.2.3.

### [ML-D5G5Q2] Memory footprint & approximate search
**Scenario:** A KNN system retains ten million feature vectors and targets; a manager claims it needs almost no memory since KNN fits no coefficients. Engineers consider indexing and approximate-neighbor methods.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | KNN can need substantial memory because it retains the training instances as its representation. |
| B | False | Dataset size affects memory, search time, and operational complexity even without coefficient fitting. |
| C | True | A search index does preprocessing/storage work in advance to speed up neighbor queries. |
| D | True | Approximate nearest-neighbor search cuts latency by occasionally returning non-exact neighbors. |
| E | False | Deleting stored observations can change predictions — removed points may have been neighbors for some queries. |

**Reference:** Memory O(N·p); ANN tradeoffs — scikit-learn "Nearest Neighbors" (KDTree/BallTree, approximate methods); HNSW/LSH literature.

### [ML-D5G5Q3] Cheap updates but growing search cost
**Scenario:** A nightly pipeline appends new observations to a KNN model without re-solving an optimization, but the batch forecast now takes hours; the lead weighs algorithmic, data, and system remedies.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Appending a labeled instance can be simpler than refitting many eager models. |
| B | False | Cheap updates do not make inference constant-time — brute-force search grows with the dataset. |
| C | True | Reducing stored prototypes lowers search cost but can alter predictions by dropping useful local examples. |
| D | False | Efficient data structures are not equally effective in every dimension/metric — they degrade in high-D and vary by metric. |
| E | True | Suitability depends jointly on dataset size, dimensionality, latency needs, and implementation. |

**Reference:** Prototype reduction; index degradation in high-D — ESL ch.13 (prototype methods); scikit-learn "Nearest Neighbors" complexity notes.

### [ML-D5G5Q4] Time/space complexity of KNN vs. eager models
**Scenario:** A mid-frequency team evaluates KNN (N=100,000 snapshots, p=40 features, K=25) that must return a signal within 500 ms, comparing training/storage/inference against logistic regression and neural nets.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Lazy learning: training just stores data, so construction cost is effectively O(1). |
| B | True | Brute-force inference computes distance to every stored instance across all features → O(N·p) per query. |
| C | False | k-d/ball trees give ~O(log N) only in low dimensions; at p=40 the curse of dimensionality collapses them back toward O(N). |
| D | False | KNN must retain the full data → O(N·p) memory, far more than logistic regression's O(p) coefficient vector. |
| E | True | Eager models pay upfront training for ~O(p) inference; KNN flips this — ~0 training but expensive, N-scaling inference and memory. |

**Reference:** Time/space complexity, tree degradation — scikit-learn "Nearest Neighbors" (algorithm complexity); ESL ch.13.

### [ML-D5G5Q5] Lazy learning tradeoffs for deployment — INVERTED logic
**Scenario:** A quant developer weighs KNN's development simplicity against live-prediction cost for intraday signals; the Tech Lead worries it won't scale to millions of stored observations. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: KNN is lazy — it stores data and defers computation to prediction time. |
| B | False (accurate) | Correct: retaining the training set makes KNN memory-heavy vs. parameter-summarizing models. |
| C | True (incorrect) | Wrong: KNN inference is often *slow* (distances to many points), even though training is cheap. |
| D | False (accurate) | Correct: more stored observations increase distance calculations and inference latency at scale. |
| E | False (accurate) | Correct: KNN can be practical when latency is relaxed and dataset size is manageable — selection depends on constraints, not accuracy alone. |

**Reference:** Lazy learning inference cost — scikit-learn "Nearest Neighbors" (computational performance); ISLR §2.2.3.

### [ML-D5G5Q6] Training vs. inference cost (embedded claim in A)
**Scenario:** A market-making firm must process thousands of predictions per second under strict latency; the team assesses whether KNN's minimal training actually yields operational efficiency.
**Answer polarity:** Normal (True = accurate) — note embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | The embedded claim (KNN training is cheap because it mostly stores data) is accurate, so calling it incorrect is false — KNN is lazy and does little at training time. |
| B | True | Inference can be costly: each prediction may compute distances to many stored observations. |
| C | True | More historical data improves neighbor availability but increases search/latency during inference. |
| D | False | Avoiding a training phase does not make the whole system faster — KNN trades low training cost for high prediction cost, unlike fast-inference linear models. |
| E | True | Deployment must weigh both training and inference costs; in latency-sensitive trading, prediction speed can dominate. |

**Reference:** Train-vs-infer cost tradeoff — scikit-learn "Nearest Neighbors" (performance); ISLR §2.2.3.

### [ML-D5G6Q1] KNN in a microsecond HFT latency budget
**Scenario:** An HFT system must decide within microseconds per quote update, but the proposed KNN brute-force searches several million stored states before every prediction.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Millions of per-query distance calculations can exceed a microsecond deadline. |
| B | False | Cheap fitting does not imply cheap prediction — inference is the constraint here. |
| C | True | For this deployment, prediction-time cost dominates over offline training convenience. |
| D | True | Reducing the reference set or using an optimized search can cut latency, subject to validation of predictive impact. |
| E | False | Offline accuracy alone is not enough — deployment also needs acceptable latency, reliability, and resource use. |

**Reference:** Latency constraints, ANN methods — scikit-learn "Nearest Neighbors"; HNSW/LSH for low-latency retrieval.

### [ML-D5G6Q2] Once-nightly batch KNN — modest latency is fine
**Scenario:** An asset manager runs KNN once each evening to estimate next-week returns for 500 securities over several years of daily data; features are scaled and the batch finishes in two minutes inside a one-hour window.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The modest latency requirement makes KNN operationally reasonable here. |
| B | False | Being instance-based does not make KNN inappropriate for *every* application — suitability depends on frequency/scale/latency. |
| C | True | Feature scaling still affects neighbor identity regardless of how often inference runs. |
| D | True | Acceptable runtime does not establish predictive validity — still evaluate out-of-sample performance and stability. |
| E | False | A two-minute batch today does not prove feasibility after arbitrary growth in data/query volume. |

**Reference:** Operational suitability & scaling — ISLR §2.2.3; scikit-learn preprocessing + performance notes.

### [ML-D5G6Q3] Nearest ≠ economically similar; distance as a warning
**Scenario:** A risk team uses KNN to find historical days like the current market and estimate a loss distribution; during an unprecedented shock it still returns the mathematically nearest days even though all are far from the query.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A ranking always exists given enough stored data, even when the best matches are poor. |
| B | True | A large nearest-neighbor distance warns the query is unlike the historical reference set. |
| C | False | Mathematical proximity under chosen features does not guarantee the days are valid economic analogues. |
| D | True | Monitoring neighbor distances supports an abstention/fallback policy for unfamiliar states. |
| E | False | Standard KNN combines stored neighbor targets; it does not fit an extrapolative trend beyond observed patterns. |

**Reference:** Distance thresholds / abstention; extrapolation limits — ESL ch.13; concept "out-of-distribution detection via neighbor distance."

### [ML-D5G6Q4] "KNN is simplest so fastest to deploy" — embedded claims
**Scenario:** A CIO believes KNN's simplicity/low training makes it automatically the fastest, easiest model to deploy at scale for daily stock selection over a large universe and years of data; the Engineering Lead asks for a review.
**Answer polarity:** Normal (True = accurate) — note embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The embedded claim (KNN is always faster than linear models because it avoids training) is inaccurate, so rejecting it is correct — KNN's inference search can be expensive. |
| B | False | KNN is memory-intensive: it stores training observations rather than compact prediction rules. |
| C | False | KNN predictions require distance calculations, which is why it struggles in latency-sensitive settings. |
| D | False | KNN inference cost grows with the number of stored examples — it is not constant regardless of dataset size. |
| E | True | KNN has low training cost but potentially high prediction cost because computation shifts to inference (lazy learning). |

**Reference:** Lazy-learning deployment tradeoffs — scikit-learn "Nearest Neighbors" (performance); ISLR §2.2.3.

### [ML-D5G6Q5] HFT unsuitability & ANN alternatives
**Scenario:** An HFT firm needs sub-100-µs inference to classify order-book liquidity regimes; a researcher proposes KNN over N=500,000 snapshots (p=50). The lead rejects pure KNN but asks where instance-based ideas remain viable.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Brute-force O(N·p) ≈ 25M float ops per tick takes milliseconds — far beyond a 100-µs budget, so exact KNN is unsuitable for sub-ms HFT. |
| B | False | Exact spatial trees degrade to O(N) once p ≳ 20–30 (curse of dimensionality), so at p=50 they give almost no speedup. |
| C | True | ANN methods (HNSW, LSH) trade a little recall for orders-of-magnitude faster, sub-ms lookups on high-D data, making instance-based retrieval viable. |
| D | False | No formal retraining does not fix the inference bottleneck; eager models evaluate in ~O(p) (nanoseconds), so KNN is not "ideally suited" to real-time execution. |
| E | True | KNN fits offline/low-frequency tasks (daily macro regime classification, stress-testing, illiquid bond pricing) where latency budgets are seconds/minutes. |

**Reference:** HFT latency, tree degradation, ANN — scikit-learn "Nearest Neighbors"; HNSW (Malkov & Yashunin), LSH literature.

### [ML-D5G6Q6] KNN vs. eager FNN across two trading regimes
**Scenario:** A team compares KNN vs. an eager feedforward neural net for Strategy 1 (ultra-low-latency market making, <500 µs) and Strategy 2 (end-of-day tactical asset allocation on macro/valuation/volatility data).
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | For Strategy 1, exact KNN inference scales O(N·p) with stored data, while an FNN (hours to train) evaluates fixed matrix multiplies in ~O(p) per layer — microsecond-feasible. |
| B | False | Streaming the dataset to disk cannot meet microsecond limits: disk I/O is millisecond-scale, thousands of times slower than RAM. |
| C | True | For Strategy 2, KNN's non-parametric nature is interpretable — predictions trace to specific historical analog dates (e.g., 1998 LTCM, 2020 COVID), aiding risk committees. |
| D | False | Appending data (O(1)) does not defeat concept drift; stale non-stationary instances keep being selected unless windows are pruned/re-weighted. |
| E | True | For daily TAA, N≈7,500 and p=15 (~112,500 ops) is trivial within a minutes/hours budget, so KNN's O(N·p) inference overhead is negligible. |

**Reference:** Lazy vs. eager inference; concept drift; interpretability — ISLR §2.2.3; scikit-learn "Nearest Neighbors"; concept "instance-based interpretability."

## References (domain-level)

1. **ISLR — *An Introduction to Statistical Learning* (James, Witten, Hastie, Tibshirani):** §2.2.3 (K-Nearest Neighbors — classifier & regression, k and the bias-variance tradeoff, decision-boundary flexibility, KNN in high dimensions), §2.2 (assessing model accuracy, U-shaped test error), §5 (cross-validation for selecting k), ch.12 (unsupervised preprocessing/PCA).
2. **ESL — *The Elements of Statistical Learning* (Hastie, Tibshirani, Friedman):** ch.13 (prototype methods & nearest-neighbor classifiers, edited/condensed NN, robustness), §2.5 (local methods in high dimensions, curse of dimensionality).
3. **scikit-learn User Guide — "Nearest Neighbors":** distance metrics (Minkowski p=1/2, Euclidean/Manhattan), `weights='uniform'` vs `'distance'`, KDTree/BallTree vs brute force and algorithmic complexity (train O(1), query cost, high-dimension degradation); "Preprocessing data" (StandardScaler, MinMaxScaler, QuantileTransformer); "Common pitfalls / data leakage" (fit scalers/PCA on training only).
4. **Concept references (no page numbers):** choice of k / bias–variance tradeoff and DoF≈N/k capacity heuristic; feature scaling for distance; curse of dimensionality — sparsity (r=q^{1/p}) and distance concentration ((Dmax−Dmin)/Dmin→0; Beyer et al., "When Is 'Nearest Neighbor' Meaningful?"); lazy vs. eager learning and train-vs-inference cost.
5. **Approximate nearest neighbor for low-latency retrieval:** HNSW (Malkov & Yashunin) and Locality-Sensitive Hashing — trading recall for sub-millisecond search when exact KNN is infeasible.
6. **"Deep Learning: Foundations and Concepts" (Bishop & Bishop), ch.1:** data preprocessing / feature scaling context cited in the source answer key for G1Q4.
