# ML Domain 1 — Learning Paradigms & Problem Framing

## Domain cheat-sheet

- **Supervised vs. unsupervised** is defined by the *task and the presence of paired target values (labels/Y)*, NOT by the input features, the output format, or how results are later interpreted.
  - **Supervised**: each training example is paired with a known target (numeric return, class label, approval flag). Learns a mapping X → Y.
  - **Unsupervised**: no targets supplied; the model discovers structure (clusters/regimes) from features (X) alone.
  - A common **pipeline pattern**: unsupervised clustering produces "signatures"/regimes that are then fed as features into a downstream supervised model. Attaching a return/score to a discovered cluster afterward makes *that later step* supervised; it does not make the clustering supervised.
- **Regression vs. classification** is defined by the *nature of the target*:
  - **Regression** → quantitative/continuous target (price, YTM, basis-point spread, probability 0.0–1.0). Estimates E(Y | X). Evaluated with distance-based metrics: MSE, MAE.
  - **Classification** → qualitative/discrete categories (up/down, approve/deny, multiclass). Estimates P(Y = j | X). Evaluated with error rate/accuracy (and cost-sensitive variants).
  - **Same underlying phenomenon can be framed either way**; thresholding a continuous prediction into a category is a *later decision step*, not a change in the learned task. Binning to categories **discards magnitude/variance information**.
- **Training vs. inference** ("fit-once, apply-many"):
  - **Training** = fitting/estimating parameters from historical labeled data (often expensive, offline, periodic).
  - **Inference** = applying the fitted model to new inputs (often the latency-critical, online step; exposed to live market risk).
  - Training cost ≠ inference cost — no 1:1 relationship. A model can train for hours and infer in microseconds.
  - **Eager (parametric) learners** (linear, trees) build a compact representation → cheap inference independent of N training rows (cost ~ number of features / tree depth). **Lazy learners** (KNN) do ~no training work but pay at inference, scaling with training-set size N; must retain the data in memory.
- **Hypothesis space & model families**: choosing a model class constrains which functions the learner can represent. More expressive families capture more patterns but risk overfitting; interpretability/governance can justify a more constrained family. Different families (linear, tree, instance-based) search *different* hypothesis spaces and generally do NOT converge to the same predictor.
- **Generalization vs. memorization / bias-variance**:
  - Goal is performance on *unseen* data, not reproduction of the training set. Near-zero training error + high test error = overfitting/memorization = **high variance**.
  - Underfitting = **high bias** (too simple to capture the true relationship). Adding data of the same type doesn't fix high bias — need more capacity/better features.
  - Expected test error = **bias2 + variance + irreducible error (ε)**. ε (unmeasured factors, inherent randomness) cannot be reduced by any model and sets the accuracy floor; the U-shaped test-error-vs-complexity curve persists above that floor.
  - Generalization is defined for a **stationary** distribution; a regime shift (change in the data-generating process) can break even a well-generalizing model.
  - **Regularization** trades training fit for a simpler, more stable hypothesis to favor generalization.
- **What makes a "good" model** is contextual — judged against the decision it supports, not a single metric:
  - Balances **accuracy, robustness (performance under distribution shift), and stability (consistent outputs/behavior under small perturbations)**.
  - Averages can hide tail behavior; accuracy is a "vanity metric" on imbalanced data (e.g., rare crashes). Net objective (turnover, transaction costs, latency, tail-risk) often matters more than raw predictive score.

## Common traps

- **Inverted-logic questions** (11 of 38 here) flip the meaning: the Answer Key notes "**True = incorrect; False = accurate**." So "False" means the statement is *correct*. Always read the Answer Key polarity line first. Inverted here: G1Q2, G2Q2, G2Q4, G2Q5, G2Q6, G2Q7, G3Q1, G3Q4, G4Q2, G5Q2, G6Q3.
- **Double-negative "embedded claim" choices**: even in *normal-polarity* questions, several choices start "It is incorrect to conclude that [an accurate statement]." The Answer Key marks these **False** ("the embedded claim is accurate, so saying it is incorrect is false"). Parse the inner claim, judge its truth, then negate. Appears in G3Q5A, G3Q6A, G4Q5A, G4Q6A, G5Q4A, G5Q5A, G5Q6A, G6Q2B, G6Q4A/B, G6Q5A, G6Q6A.
- **"Presence of labels defines supervised, not the output or features."** Same feature rows can serve supervised or unsupervised tasks; identical inputs do NOT force the same paradigm. A buy/sell *action* can come from a rule without any labels.
- **Post-hoc cluster naming ≠ supervision.** Naming clusters "bull/bear/sideways" or scoring them by average forward return *after* the fact does not provide labels *during* clustering — the clustering stays unsupervised. (But if you label *before* training so the model learns from labels, it becomes supervised.)
- **Numeric output ≠ regression by itself.** A class *probability* is still a classification output; a probability/rate target (0–1) is still regression. It's the target's nature that decides.
- **Thresholding/binning loses information** about within-category magnitude — and classification metrics (error rate) treat all misclassifications as equal regardless of distance from the boundary, unlike MSE.
- **Training speed says nothing about inference speed** (and vice versa). "Zero training time" (KNN) can mean *slow, N-dependent* inference. Aggregate/total compute can hide per-prediction latency misses.
- **In-sample fit does not prove generalization.** More runs on the development sample, or matching more historical detail, is not fresh evidence; an untouched, representative (ideally later/regime-matched) evaluation period is. More data helps *variance/overfitting*, not *bias*.

## Questions

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

**Reference:** Supervised vs. unsupervised learning — ISLR ch.2 (§2.1); scikit-learn "Choosing the right estimator" flowchart.

### [ML-D1G1Q2] Compliance clustering — INVERTED logic
**Scenario:** Compliance wants accounts grouped by trading pattern, but no account is labeled normal/suspicious; a junior analyst proposes training a suspicious-account classifier. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Grouping accounts by observed-behavior similarity with no labels is genuinely unsupervised. |
| B | True (incorrect) | Wrong: lacking suspicious labels does NOT prevent finding structure — unsupervised methods still surface groups, similarities, and outliers/anomalies. |
| C | False (accurate) | Correct: once investigators label accounts, those discrete labels can train a supervised classifier. |
| D | True (incorrect) | Wrong: a cluster reflects patterns in the chosen features, not a verified legal/compliance category — it carries no ground-truth "suspicious" meaning by itself. |
| E | False (accurate) | Correct: humans must interpret whether statistical structure maps to real-world (suspicious) meaning. |

**Reference:** Unsupervised anomaly/cluster discovery — ISLR ch.12 (unsupervised learning); scikit-learn "Clustering" and "Novelty and outlier detection."

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

**Reference:** Task-defines-paradigm distinction — ISLR §2.1; concept "clustering is not classification."

### [ML-D1G1Q4] Market-state classifier + liquidity-spike prediction
**Scenario:** An HFT firm groups 50 order-book metrics into 4 regimes with no labels, then a second system uses those regime IDs to predict probability of a liquidity spike in 100 ms. Identify the paradigms.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Grouping order-book metrics into regimes without target outcomes is unsupervised (clustering). |
| B | True | Predicting spike vs. no-spike (a discrete binary event) is supervised classification. |
| C | True | Regimes are discovered from patterns in the features X, not mapped to a known ground truth — the hallmark of clustering. |
| D | False | For exploring natural structure in a *new, unlabeled* dataset, unsupervised is the appropriate choice; supervised learning cannot run without labels. |
| E | False | Manually labeling regimes (High/Low Volatility) *before* the model learns turns the task into supervised classification — same inputs, but now learning from labels. |

**Reference:** Two-stage unsupervised→supervised pipelines — ISLR ch.12 + ch.4 (classification); scikit-learn clustering as feature engineering.

### [ML-D1G1Q5] "Black box" tool — hybrid learning clarified
**Scenario:** A tool groups Russell 3000 stocks hourly into 12 "neighborhoods" by price action (200 indicators), then scores each group by average 1-hour forward return. Marketing calls it "Hybrid Learning."
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Grouping without sector labels/target categories is unsupervised (clustering), not supervised. |
| B | True | Finding clusters of similar behavior in high-dimensional feature space is a core unsupervised application. |
| C | True | Using average forward return as a score attaches a target (Y) to groups → a supervised evaluation of the clusters' predictive utility. |
| D | False | Clustering does NOT need a pre-existing ground-truth neighborhood label per stock; it derives groupings from features X alone. |
| E | True | This is the standard pipeline: unsupervised for structure discovery (neighborhoods) + supervised prediction using the returns. |

**Reference:** Unsupervised feature construction feeding supervised targets — ISLR ch.12; "clustering + downstream prediction" concept.

### [ML-D1G1Q6] "Market signature" — clusters as features for a volatility model
**Scenario:** 200 indicators for 1,000 stocks → discover "natural" clusters of similar high-volatility behavior with no sector labels, then a separate model predicts each cluster's next-day volatility.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Discovering natural clusters by feature similarity without predefined labels is unsupervised learning. |
| B | False | Phase-1 clustering is driven by relationships among features X, not by external target labels indicating "profitable" clusters. |
| C | True | Predicting a continuous value (next-day volatility) is supervised regression. |
| D | False | Unsupervised clustering is commonly used as a preprocessing/feature-engineering step for supervised pipelines — not "incapable." |
| E | True | In supervised learning the "supervisor" is the ground-truth target (Y) — here the numerical volatility that trains the second model. |

**Reference:** "Supervisor = Y" terminology and unsupervised-as-preprocessing — ISLR §2.1, ch.12.

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

**Reference:** Regression vs. classification framing & thresholding — ISLR §2.1.5, ch.4.

### [ML-D1G2Q2] Margin-call alert — INVERTED logic
**Scenario:** A brokerage wants either a probability of a margin call within 5 days or the dollar size of the shortfall; ops can only investigate top cases. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: margin call vs. none is a two-class discrete outcome → classification. |
| B | False (accurate) | Correct: dollar shortfall is a continuous target → regression. |
| C | True (incorrect) | Wrong: producing a class *probability* does not turn classification into regression — a probability is a standard classification output. |
| D | False (accurate) | Correct: the framing should follow how operations will actually use the result. |
| E | True (incorrect) | Wrong: classification and regression targets require *different* metrics; the same metric can't be applied without changing its meaning. |

**Reference:** Class probabilities vs. regression outputs, metric selection — ISLR ch.4; scikit-learn "Metrics and scoring."

### [ML-D1G2Q3] Underperform/track/outperform — multiclass vs. thresholded regression
**Scenario:** A desk wants to predict underperform/track/outperform vs. sector; one researcher predicts continuous excess return then thresholds, the desk head learns categories directly. The desk most fears large longs in underperformers.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Assigning one of three named outcomes is multiclass classification. |
| B | True | Predicting excess return is regression even if later binned — the learned target stays continuous; thresholding is a separate decision step. |
| C | False | A direct classifier and a thresholded regressor optimize different objectives and can learn different decision boundaries — not guaranteed identical. |
| D | True | The desk's asymmetric cost (underperformers hurt more) should shape how decisions are evaluated (cost-sensitive / asymmetric loss). |
| E | False | Any conversion to categories loses within-category magnitude information, regardless of how narrow the thresholds are. |

**Reference:** Multiclass classification & cost-sensitive evaluation — ISLR ch.4; scikit-learn "Multiclass and multioutput," confusion-matrix costs.

### [ML-D1G2Q4] NVDA price vs. bullish/bearish flag — INVERTED logic
**Scenario:** Head of Trading wants (1) NVDA's exact next-session close and (2) a bullish/bearish flag for hedging. Explain how the two tasks differ mathematically.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: exact price is a continuous response → regression. |
| B | False (accurate) | Correct: bullish/bearish is a discrete category → classification. |
| C | False (accurate) | Correct: a regression output can be thresholded/binned into a categorical decision (e.g., return > 0 ⇒ Bullish). |
| D | True (incorrect) | Wrong: MSE is a regression metric; a bullish/bearish classifier is judged by error rate/accuracy, not MSE. |
| E | False (accurate) | Correct: classifiers typically work by estimating P(class | X). |

**Reference:** Regression vs. classification metrics, probabilistic classifiers — ISLR §2.2, ch.4.

### [ML-D1G2Q5] Bond YTM vs. approve/deny — INVERTED logic
**Scenario:** One model estimates a bond's exact yield-to-maturity from credit spread/duration; a second flags approve/deny for the buy-list. Explain evaluation differences.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: exact YTM is continuous → regression. |
| B | False (accurate) | Correct: approve/denied is a discrete qualitative category → classification. |
| C | False (accurate) | Correct: minimizing MSE (distance between predicted and actual yields) is the standard regression goal. |
| D | True (incorrect) | Wrong: a classifier outputs class labels or class probabilities, not an unbounded (−∞, +∞) range whose magnitude encodes price. |
| E | False (accurate) | Correct: both are supervised — each needs labeled history (actual YTM / actual approval). |

**Reference:** Supervised regression vs. classification & loss functions — ISLR §2.1, ch.4; MSE definition.

### [ML-D1G2Q6] CPI value vs. regime ID — INVERTED logic
**Scenario:** A macro desk wants to predict CPI to flag "Hyper-inflationary" vs. "Stable"; a junior argues to train a classifier from the start since the trade is binary. Evaluate the choice vs. regression.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: outputting exact CPI = regression; outputting a regime ID (1/0) = classification. The output's nature defines the problem type. |
| B | False (accurate) | Correct: binarizing continuous CPI before training discards magnitude and variance information. |
| C | False (accurate) | Correct: a classification loss (error rate) penalizes a wrong "Stable" call for 2.1% CPI the same as for 10.5% CPI if both exceed the threshold — distance from boundary is ignored. |
| D | True (incorrect) | Wrong: accuracy is a *classification* metric; a regression model's sensitivity is assessed with distance metrics (MSE/MAE), not accuracy. |
| E | False (accurate) | Correct: classifying a continuous phenomenon is a model-selection tradeoff — decision simplicity vs. predictive granularity. |

**Reference:** Information loss from binning, metric mismatch — ISLR §2.1.5, §2.2.3.

### [ML-D1G2Q7] Yield-curve spread: predict bps vs. invert/normal flag — INVERTED logic
**Scenario:** A fixed-income PM goes defensive when the 10y–2y spread inverts. Model A predicts the numeric bps spread then checks sign; Model B outputs a binary inverted/normal indicator. Evaluate the math.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: continuous spread target (A) = regression; binary indicator target (B) = classification. |
| B | False (accurate) | Correct: MSE grows with the squared deviation, so predicting −40 (true −10) is penalized more than −15. |
| C | False (accurate) | Correct: if Model B predicts "Inverted" correctly, error rate is 0 whether the true spread was −5 or −500 bps — magnitude is ignored. |
| D | True (incorrect) | Wrong: Model A is *more* informative — it gives the sign (regime) plus the magnitude/severity of inversion; B discards magnitude. |
| E | False (accurate) | Correct: regression estimates E(Y \| X); classification estimates P(Y = j \| X). |

**Reference:** Conditional mean vs. class probability objectives — ISLR §2.1.1, §2.2.3, ch.4 (Bayes classifier).

### [ML-D1G2Q8] Recession probability — regression of a 0–1 target
**Scenario:** A CIO wants a risk-on/off system estimating probability of recession within 12 months (0.0–1.0) from a bond yield spread; a junior argues to evaluate with accuracy since the trade is binary.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Predicting a value on a continuous scale (a probability 0–1) is a regression task, since the response is quantitative/continuous. |
| B | False | Accuracy is a classification metric; a continuous probability output needs distance-based metrics (MSE). Note: the pool treats this as pure regression; in practice probabilistic classifiers are also scored with log-loss/AUC — see reference. |
| C | True | MSE here = mean squared difference between predicted probability and the 0/1 outcome — this is the Brier score. |
| D | True | Restricting output to "Recession"/"No Recession" (a discrete category) shifts the task from regression to classification. |
| E | False | Regression handles any quantitative response — interest rates, probabilities, economic indicators — not just price. |

**Reference:** Brier score / probability calibration — Brier (1950); scikit-learn "Probability calibration"; ISLR ch.4 for the regression-of-probabilities view.

### [ML-D1G3Q1] Overnight training vs. 10 ms live prediction — INVERTED logic
**Scenario:** A prop firm retrains a signal model overnight and applies it intraday, requiring each live prediction < 10 ms; a junior says total daily compute is all that matters. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: estimating parameters from historical examples is training. |
| B | False (accurate) | Correct: applying the fitted model to a new feature vector is inference. |
| C | True (incorrect) | Wrong: the 10 ms limit constrains *inference*, not overnight fitting; slow training doesn't violate it. |
| D | True (incorrect) | Wrong statement to flag as incorrect — actually a model IS practical if training is expensive but inference meets latency; different stages tolerate different costs. (Key marks it True = "incorrect" because the choice is phrased in the negative frame of "flawed claims"; per the rationale, different stages can tolerate different costs.) |
| E | True (incorrect) | Wrong: an aggregate daily-compute number can hide whether individual predictions blow the per-prediction deadline. |

**Note:** Choice D's rationale ("Different deployment stages can tolerate different computational costs") supports that D's statement is *accurate/reasonable*, yet the Key marks it True (=incorrect). This reads inconsistently with the other rows; go with the Key's verdict (True) for the exam but be aware the rationale actually argues the statement is sensible. Treat D cautiously if a near-identical item appears.
**Reference:** Training vs. inference cost, latency SLAs — ISLR §2.1 (fit vs. predict); scikit-learn "Computational performance" / prediction latency.

### [ML-D1G3Q2] Quarterly training vs. nightly scoring
**Scenario:** A wealth manager retrains quarterly but scores every portfolio nightly; the CTO wants to move scoring to a smaller server and asks if the quarterly training benchmark alone proves feasibility. Scoring must finish before overnight reports.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Frequent scoring makes inference cost operationally important even though training is rare — repeated application can dominate total cost. |
| B | False | A training benchmark does not establish scoring throughput/latency — they are different operations. |
| C | True | Inference-time memory (to store and apply the fitted model) is a real deployment constraint. |
| D | False | One fitted model is normally applied to many observations; you don't retrain per prediction. |
| E | True | The right test is a representative nightly-scoring (inference) benchmark against the reporting deadline. |

**Reference:** Inference-time resource planning — scikit-learn "Computational performance"; fit-once/apply-many concept.

### [ML-D1G3Q3] Daily retraining vs. instant scoring
**Scenario:** A market-making desk's model has degraded; risk wants daily retraining, engineering notes fitting takes 6 hours but scoring is near-instant. Distinguish updating from live use.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Generating a quote with the currently fitted model is inference (applying the model). |
| B | True | Refitting on the latest labeled observations is training. |
| C | False | Fast inference says nothing about the 6-hour fit fitting within the maintenance window. |
| D | True | A retraining schedule is an operational tradeoff (model freshness vs. fit time/logistics) even when inference is fast. |
| E | False | Changing market conditions (distribution shift) can degrade a trained model's future predictions. |

**Reference:** Model staleness / retraining cadence & distribution shift — ISLR §2.2 (irreducible error, changing f); concept "concept drift."

### [ML-D1G3Q4] Hours to train vs. 500 μs to execute — INVERTED logic
**Scenario:** An HFT firm's momentum model takes hours to optimize on limit-order-book history but must emit a signal in < 500 μs per packet. Explain resource allocation across the two phases.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: training is the fit-once/periodic phase that learns the feature→price-move relationship. |
| B | False (accurate) | Correct: inference is the apply-many phase using the pre-trained model on live data. |
| C | False (accurate) | Correct: in HFT, tick-to-trade inference latency is more critical to success than training duration (training can be offline). |
| D | True (incorrect) | Wrong: no 1:1 link between training and inference time — models can train for hours yet infer in microseconds. |
| E | False (accurate) | Correct: fit-once/apply-many means heavy training can coexist with cheap inference (simple arithmetic) → viable for low latency. |

**Reference:** Fit-once/apply-many, offline training — ISLR §2.1; HFT tick-to-trade latency concept.

### [ML-D1G3Q5] Lazy (KNN) vs. eager learners at scale
**Scenario:** A macro desk considers KNN ("zero training time") to predict monthly bond yields, but must produce 50,000 predictions each morning within 10 minutes. Evaluate scalability.
**Answer polarity:** Normal (True = accurate) — note embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded claim ("lazy learning shifts burden from training to inference") is accurate, so calling it "incorrect" is false. KNN does ~no training work and computes distances at inference. |
| B | False | KNN inference speed is NOT independent of N — it must search all stored observations to find neighbors, so it scales with training-set size. |
| C | True | For a parametric model (linear regression), inference cost depends on the number of features (a dot product), not on how many rows fit the coefficients. |
| D | True | Eager learners build compact representations (equation/tree) that evaluate faster in batch than a search-based lazy learner → better for 50k simultaneous predictions. |
| E | True | Fit-once/apply-many lets expensive training run offline without hurting live execution latency — ideal for trading. |

**Reference:** Lazy vs. eager, KNN cost O(N) — ISLR §2.2.3 (KNN), §3.5; scikit-learn "Nearest Neighbors" (query complexity, KD/Ball trees).

### [ML-D1G3Q6] Weekly training vs. millions of daily inferences (cloud cost)
**Scenario:** A stat-arb fund migrates to cloud "Prediction-as-a-Service"; the model is retrained weekly on 5 years of tick data but queried millions of times/day. The CTO worries about variable cost.
**Answer polarity:** Normal (True = accurate) — note embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded claim (training = periodic fixed weekly cost; inference cost scales with opportunities) is accurate, so calling it "incorrect" is false. |
| B | False | Higher hypothesis-space complexity does not scale training and inference by the same percentage — e.g., a deep tree trains slowly but infers fast vs. KNN. |
| C | True | A parametric model stores only weights (small footprint); a lazy learner must retain the whole training set for similarity search (large footprint). |
| D | True | Long training latency is forward-looking: the model can't absorb "today's" regime shift until the training cycle completes. |
| E | True | Training is offline empirical-risk minimization on the past; inference is the online moment parameters face live market risk. |

**Reference:** Parametric vs. non-parametric memory footprint; empirical risk minimization — ISLR §2.1, §2.2.3; Vapnik, empirical vs. structural risk.

### [ML-D1G4Q1] Choosing a model family constrains the hypothesis space
**Scenario:** A quant team must model valuation indicators → returns; the director prefers a linear model for transparency, analysts suspect thresholds/interactions matter. They pick a family before fitting.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Choosing linear restricts the representable functions to linear combinations — the family constrains the candidate functions. |
| B | False | Trees and linear models search *different* hypothesis spaces (different functional structure); sharing training data doesn't equate them. |
| C | True | A more expressive family can represent relationships (nonlinearities, interactions) a linear family cannot. |
| D | False | More expressiveness does NOT guarantee better out-of-sample performance — extra flexibility can fit noise (overfit). |
| E | True | Interpretability/governance is a legitimate reason to prefer a more constrained family even at some accuracy cost. |

**Reference:** Hypothesis space, expressiveness vs. interpretability — ISLR §2.1.3 (flexibility-interpretability tradeoff), Fig. 2.7.

### [ML-D1G4Q2] Linear vs. tree vs. KNN — different inductive biases — INVERTED logic
**Scenario:** A risk committee compares linear regression, a decision tree, and KNN for stress losses; an analyst claims family choice is just a software preference since careful training makes them equal. Identify flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: each family imposes different assumptions/structure on possible predictions (its inductive bias). |
| B | False (accurate) | Correct: KNN is instance-based — it predicts from nearby stored points via local similarity, not one global line. |
| C | False (accurate) | Correct: a tree represents threshold/piecewise behavior without a globally linear function. |
| D | True (incorrect) | Wrong: careful training does NOT force all three to the same predictor — distinct hypothesis spaces and fitting procedures yield different functions. |
| E | False (accurate) | Correct: comparing families reveals which structural/inductive constraint best suits the task. |

**Reference:** Model families & inductive bias — ISLR §2.1.3, ch.3 (linear), ch.8 (trees), §2.2.3 (KNN).

### [ML-D1G4Q3] Flexibility vs. small data
**Scenario:** A small fund has 2 years of weekly data but hundreds of features; the PM wants the most flexible model (fits nearly anything), the risk manager wants constraints until more evidence exists. They want reliable forecasts, not historical fit.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A highly expressive space can fit accidental/spurious patterns in a small sample (overfitting). |
| B | True | Constraining the family adds bias but reduces the chance of fitting noise — a bias-variance tradeoff favoring stability. |
| C | False | The broadest hypothesis space does not guarantee the lowest future error; it can increase overfitting. |
| D | False | Excellent in-sample fit is not evidence of generalization — it doesn't test unseen data. |
| E | True | Appropriate capacity depends on dataset size and signal strength (little informative data ⇒ favor constraints). |

**Reference:** Bias-variance tradeoff, capacity vs. sample size — ISLR §2.2.2; curse of dimensionality (§6, KNN discussion).

### [ML-D1G4Q4] High-degree polynomial overfits — bias-variance
**Scenario:** A "Earnings Surprise" model uses a high-degree polynomial fitting 10 years of data with near-zero training MSE, but out-of-sample error exceeds a simple linear baseline.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Near-zero training error + high test error indicates high variance — it overfit noise and fails to generalize. |
| B | True | Bias is the error from approximating a complex reality with a too-simple model (e.g., a line for a curve); high bias → underfitting. |
| C | True | As complexity rises, training MSE falls monotonically but test MSE follows a U-shape (falls, then rises). |
| D | False | To reduce variance you *decrease* flexibility (fewer parameters/simpler form), not increase it. |
| E | False | Even with zero bias and variance, irreducible error ε remains (unmeasured factors), so "zero-zero regardless of noise" is impossible. |

**Reference:** Bias-variance decomposition & U-shaped test error — ISLR §2.2.2 (Eqs. 2.7, 2.9), Figs. 2.9–2.12.

### [ML-D1G4Q5] Trees overfit vs. linear underfit — error profiles
**Scenario:** In a portfolio of 100 models, high-order trees show 0.02 train / 0.85 live MSE, while simple linear models show a steady 0.40 on both. Characterize the error profiles.
**Answer polarity:** Normal (True = accurate) — note embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded claim (trees have high variance because predictions swing with slightly altered training data) is accurate, so calling it "incorrect" is false. |
| B | True | The linear models show high bias — a too-simple form can't capture nonlinear market structure (consistent, moderate error). |
| C | True | A large train-vs-test gap (0.02 → 0.85) is the classic overfitting/memorized-noise symptom. |
| D | False | For a high-bias (underfitting) model, more data of the same type won't help — you need more capacity or better features. |
| E | True | Total expected error = bias2 + variance + variance of the irreducible error term (bias-variance decomposition). |

**Reference:** Bias-variance decomposition, overfitting gap — ISLR §2.2.2; ESL §7.3.

### [ML-D1G4Q6] Irreducible error is not an excuse — cross-sectional momentum
**Scenario:** A flexible non-parametric model on 200 factors → next-month returns shows low train MSE, high test MSE. A junior claims ε must be huge so the fund should accept the high test MSE.
**Answer polarity:** Normal (True = accurate) — note embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded claim (ε is the noise variance in Y = f(X)+ε, independent of model choice/sample size) is accurate, so calling it "incorrect" is false. |
| B | False | A large train-vs-test gap is the hallmark of variance (overfitting), not bias — it does not mean the model is too simple. |
| C | True | If ε is truly large, the test-MSE curve has a higher floor, but the bias-variance U-shape vs. flexibility still holds. |
| D | True | Overfitting occurs when added flexibility's variance increase outweighs the squared-bias reduction, raising expected test error. |
| E | True | Adding irrelevant features lets the model fit more training noise (lower train MSE) while raising test MSE via added variance. |

**Reference:** Irreducible error floor, variance from irrelevant features — ISLR §2.2.2, §6.1 (feature selection); ESL §7.3.

### [ML-D1G5Q1] Perfect training fit ≠ learning the market
**Scenario:** A model reproduces every historical return but fails the following year. The PM calls the perfect fit proof of learning; the research lead suspects memorization. No capital without an explanation.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Near-perfect training + poor later performance is evidence *against* reliable generalization. |
| B | True | Memorizing training idiosyncrasies (noise) hurts unseen performance because that noise won't recur. |
| C | False | Perfect training fit does not prove the true relationship was found — the model may have captured noise/coincidences. |
| D | True | Evaluating on unseen, temporally later data matches the desk's intended use (predicting after the training period). |
| E | False | A well-generalizing model need not reproduce every training point exactly; some training error can accompany better recovery of persistent patterns. |

**Reference:** Overfitting vs. generalization, out-of-time validation — ISLR §2.2.2; concept "walk-forward / out-of-sample testing."

### [ML-D1G5Q2] Backtest on development sample — INVERTED logic
**Scenario:** A vendor demos on the same 5-year set it developed/tuned on; the CIO asks whether it handles unseen data, the vendor says more runs on that sample will answer it. Identify flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: repeatedly reporting on the development sample does not establish performance on genuinely unseen data. |
| B | False (accurate) | Correct: generalization is about learned relationships holding beyond the fitting examples. |
| C | True (incorrect) | Wrong: matching more detail in the 5-year history can be fitting noise, not better generalization. |
| D | False (accurate) | Correct: an untouched evaluation period gives more relevant evidence than re-reporting on the dev sample. |
| E | True (incorrect) | Wrong: markets change, so strong historical generalization does NOT guarantee identical live performance. |

**Reference:** Data leakage / train-test hygiene, non-stationarity — ISLR §5.1 (validation); "look-ahead bias" concept.

### [ML-D1G5Q3] Calm-period training, crisis deployment
**Scenario:** A credit fund trains on a calm period and will deploy in a liquidity crisis; the PM thinks holding out random calm-period bonds proves crisis readiness. The risk officer questions representativeness.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Good performance on held-out calm-period bonds is evidence of *some* generalization within that environment. |
| B | False | It does not prove generalization to materially different crisis conditions — the distribution differs. |
| C | True | Generalization is easier to assess when evaluation data reflect the deployment conditions. |
| D | True | Memorizing bond identifiers could look useful in-sample without learning transferable risk patterns. |
| E | False | A clean train/test split doesn't remove concern about mismatch between evaluation and deployment (economic context still matters). |

**Reference:** Distribution shift / covariate shift, representative validation — ISLR §2.2; concept "regime-aware / stress backtesting."

### [ML-D1G5Q4] Empirical vs. structural risk; capacity enables memorization — embedded claims
**Scenario:** A stat-arb non-parametric learner has near-zero empirical risk (training loss) but much higher structural risk (expected loss on new data); the lead argues millions of ticks make any pattern a general truth.
**Answer polarity:** Normal (True = accurate) — most choices use embedded-claim wording.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded claim (memorization can occur even on big data if capacity/VC-dimension is high enough to fit noise) is accurate, so calling it "incorrect" is false. |
| B | True | Generalization gap = training vs. test error; as N→∞ a well-specified model's train and test performance should converge (a necessary condition). |
| C | True | A model that memorized can no longer separate signal f(X) from the stochastic realization of ε. |
| D | True | Adding a complexity-penalizing regularization term enforces generalization over memorization, even at higher training error. |
| E | False | Generalization is defined for a stationary distribution; a regime shift can break even a perfectly generalizing model. |

**Reference:** VC dimension, empirical vs. structural risk minimization, regularization — Vapnik (SLT); ISLR §6.2 (shrinkage); ESL §7.9.

### [ML-D1G5Q5] Bitcoin volatility model — memorization vs. generalization
**Scenario:** A high-capacity learner hits near-perfect accuracy on 12 months of BTC but fails the next quarter (misses reversals a simple MA catches). Investigate signal extraction vs. "identity mapping."
**Answer polarity:** Normal (True = accurate) — note embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded claim (near-perfect train + failure on the next quarter = memorizing noise, not generalizing) is accurate, so calling it "incorrect" is false. |
| B | True | A generalizing model captures structural f(X) while staying invariant to the specific ε realization in the training sample. |
| C | False | Increasing training-data volume typically forces focus on persistent signal and makes memorizing unique noise harder, not easier. |
| D | True | Memorization in high-capacity models comes from too-large a hypothesis space relative to data, letting it fit every point (identity map). |
| E | True | A generalizing model performs consistently across out-of-sample periods *provided the data-generating process is stationary*. |

**Reference:** Capacity vs. data volume, stationarity — ISLR §2.2.2; ESL §7 (model assessment).

### [ML-D1G5Q6] Kernel learner as a lookup table — post-mortem
**Scenario:** A complex kernel HFT-arb model showed a near-perfect 5-year backtest equity curve but performed like a coin flip live; you find it built a high-dimensional lookup table of specific historical price paths.
**Answer polarity:** Normal (True = accurate) — note embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded claim (the live failure is memorization — encoding historical noise as deterministic signal) is accurate, so calling it "incorrect" is false. |
| B | True | To move from memorization to generalization, constrain the model to capture only patterns invariant across historical samples. |
| C | True | With high irreducible error ε, a high-capacity model may map noise as an identity mapping to be replicated → perfect train fit, no live edge. |
| D | False | More training iterations/epochs on the same data typically *reinforce* memorization and worsen generalization, not fix it. |
| E | True | A stable, small generalization gap across data volumes indicates the model learned the underlying data-generating process. |

**Reference:** Overfitting/memorization, early stopping, generalization gap — ESL §7; ISLR §2.2.2; regularization concept.

### [ML-D1G6Q1] Average error vs. tail risk
**Scenario:** Model A has lower average error but occasional extreme mistakes in volatile markets; Model B has slightly higher average error but is stable. The CRO prioritizes limiting severe surprises; the team ranks by average error.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Lower average error is not sufficient for every objective — a single average can omit the tail outcomes the CRO values. |
| B | True | The cost of extreme errors is relevant; tail mistakes can have disproportionate financial impact. |
| C | True | Model B may be preferable if its stability better aligns with the risk objective (a modest accuracy sacrifice can be worth it). |
| D | True | A good model is judged against the decision it supports — quality is contextual. |
| E | False | Considering robustness is an *additional* criterion; it does not make accuracy irrelevant. |

**Reference:** Loss-function/metric choice, tail risk — ISLR §2.2.1; concept "expected shortfall / cost-sensitive evaluation."

### [ML-D1G6Q2] Transparency & stability vs. one best score
**Scenario:** A pension fund weighs a transparent model against a marginally more accurate but unstable one; the committee needs explanations and consistent recommendations under small input changes. A data scientist says the best single test score wins.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The explanation requirement legitimately affects which model counts as "good" (interpretability is a stated objective). |
| B | True | Sensitivity to small, economically insignificant input changes is a valid measure of (in)stability. |
| C | False | A marginally higher score on one test sample doesn't guarantee superior future decisions — a single estimate is uncertain. |
| D | True | The committee may rationally trade a little measured accuracy for interpretability and stability. |
| E | False | Model quality can't be determined without considering how predictions enter the allocation process (use context matters). |

**Reference:** Interpretability & stability as objectives — ISLR §2.1.3; concept "model risk / governance."

### [ML-D1G6Q3] Accuracy vs. net performance under turnover — INVERTED logic
**Scenario:** A long-only fund's accurate next-day model causes frequent turnover; transaction costs erase the gain. The PM asks if it's successful; the modeling lead cites only the prediction score. Objective: net performance under a turnover limit.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: predictive accuracy alone may be insufficient — the model is part of a decision system judged on net outcomes/constraints. |
| B | False (accurate) | Correct: turnover and transaction costs connect model outputs to the fund's true objective. |
| C | True (incorrect) | Wrong: high forecast accuracy does not establish alignment with the portfolio objective (net-of-costs performance). |
| D | False (accurate) | Correct: a less accurate but more stable model can yield better net results after costs. |
| E | False (accurate) | Correct: changing the forecast→trade decision rule can alter trades/costs without retraining the predictor. |

**Reference:** Net-of-cost / implementation shortfall, decision rules — Grinold & Kahn "Active Portfolio Management"; concept "signal vs. execution."

### [ML-D1G6Q4] 99% accuracy but misses flash crashes — accuracy as a vanity metric
**Scenario:** A tail-risk protection strategy hit 99% backtest accuracy by predicting normal days but missed both flash crashes (30% drawdown). The board debates whether high accuracy makes it "good."
**Answer polarity:** Normal (True = accurate) — note embedded-claim wording in B.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Accuracy is NOT sufficient here — on imbalanced data it's a "vanity metric" that ignores utility in the rare, high-impact cases. |
| B | False | Embedded claim (a model is robust if it stays reliable under inputs differing from training) is accurate, so calling it "incorrect" is false; robustness = handling distributional shift/noise. |
| C | True | Alignment with objectives makes it a poor model — the cost of missing a rare tail event (false negative) far outweighs correctly calling normal days. |
| D | True | A stable model gives consistent outputs and holds predictive power over time rather than reacting sharply to small input changes. |
| E | True | The accuracy-vs-robustness tradeoff means a good model may accept lower overall accuracy to perform better on critical rare events. |

**Reference:** Class imbalance & metric choice (precision/recall, cost of false negatives), robustness — scikit-learn "Metrics" (imbalanced); ISLR §4 (confusion matrices).

### [ML-D1G6Q5] HFT: accuracy vs. latency vs. stability tradeoffs
**Scenario:** An HFT market-making model must balance latency, accuracy, and computational stability; a deeper DL model adds 2% accuracy but doubles latency and increases response-time variance under stress.
**Answer polarity:** Normal (True = accurate) — note embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded claim (the 2% accuracy gain is only valuable if latency stays below the arbitrage-vanishing threshold) is accurate, so calling it "incorrect" is false. |
| B | True | Choosing the simpler, faster model prioritizes stability/robustness over pure accuracy. |
| C | False | A good HFT model must balance multiple criteria (efficiency, business constraints); training MSE alone doesn't define it. |
| D | True | Stability here means predictable latency in a tight range even when incoming data volume spikes. |
| E | True | Rejecting the more accurate but brittle model is an evaluation of robustness (integrity under stressful/outlying data). |

**Reference:** Multi-criteria model selection, latency/robustness — concept "production ML tradeoffs"; ISLR §2.1.3 (flexibility-interpretability).

### [ML-D1G6Q6] Low-liquidity failure — robustness vs. stability post-mortem
**Scenario:** An order-flow-imbalance model trained on high-volume data spikes in error and its risk parameters swing wildly during a low-liquidity holiday session. Post-mortem on why it failed as a production system.
**Answer polarity:** Normal (True = accurate) — note embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded claim (erratic holiday behavior despite high training accuracy is a robustness failure) is accurate, so calling it "incorrect" is false; robustness = staying effective when the input distribution shifts (high→low liquidity). |
| B | True | If predictions/parameters stayed consistent despite the volume change, the model would be characterized as having high stability. |
| C | False | A good model is not defined *solely* by backtest MSE — operational behavior in live trading is part of model quality, not just an engineering afterthought. |
| D | True | High parameter sensitivity to minor jitter suggests an overly flexible hypothesis space → instability (over-reaction to small variations). |
| E | True | Preferring consistent execution/risk thresholds over 1% higher but unpredictable accuracy is prioritizing reliability in model selection. |

**Reference:** Robustness (distribution shift) vs. stability (perturbation sensitivity); flexibility-driven instability — ISLR §2.2.2; concept "production model reliability."

## References (domain-level)

1. **ISLR — *An Introduction to Statistical Learning* (James, Witten, Hastie, Tibshirani):** §2.1 (supervised vs. unsupervised, regression vs. classification, inference vs. prediction), §2.2 (assessing model accuracy, bias-variance tradeoff, irreducible error, U-shaped test error), §2.1.3 (flexibility–interpretability), ch.4 (classification, Bayes classifier, P(Y|X)), §2.2.3 (KNN), ch.8 (trees), ch.12 (unsupervised learning), ch.5 (cross-validation).
2. **ESL — *The Elements of Statistical Learning* (Hastie, Tibshirani, Friedman):** ch.7 (model assessment & selection, bias-variance decomposition, generalization gap), §7.9 (VC dimension).
3. **scikit-learn User Guide:** "Choosing the right estimator" (map task→paradigm), "Clustering," "Nearest Neighbors" (query cost), "Metrics and scoring," "Probability calibration" (Brier score), "Computational performance" (train vs. predict latency).
4. **Vapnik — Statistical Learning Theory:** empirical vs. structural risk minimization, capacity/VC dimension, regularization — for the generalization/memorization questions.
5. **Grinold & Kahn — *Active Portfolio Management*:** connecting predictive signal to net-of-cost portfolio outcomes (turnover, transaction costs, implementation shortfall) for the "good model" questions.
