# ML Domain 8 — Model Evaluation & Metrics

## Domain cheat-sheet

- **Three-way data split (train / validation / test)** — each split has a distinct, non-interchangeable role:
  - **Training set**: estimate model parameters / learned structure from observed examples (fit).
  - **Validation set**: choose hyperparameters and select among candidate models *before* the final test. It provides feedback for development decisions without touching the final evaluation.
  - **Test set**: a *single, final* out-of-sample check. It is most informative only when earlier decisions have **not** been adapted to its results.
  - After selection, refitting the chosen configuration on **train + validation** combined is legitimate **as long as the test set stays untouched**.
  - **Why validation exists separately from test**: trying many candidates produces **selection optimism** — the best-of-many validation score is optimistically low. The test set stays clean precisely so it is not contaminated by that selection pressure.
- **Test-set reuse / leakage** is the cardinal sin:
  - Repeatedly inspecting the test score and revising features/settings turns the test set into part of the *development* process — even if test **rows are never passed to the fit method**. Human decisions based on test feedback are indirect adaptation.
  - The "best observed" result after many attempts exploits chance variation and is **optimistic**, not unbiased.
  - **Scarce data does not make reuse harmless** — small datasets make estimates *less* stable, not contamination-free.
  - Test **labels** are needed to *score* (compute error) but must stay out of *fitting and tuning*.
- **Error metrics — MAE, MSE, RMSE** (regression):
  - **MAE** (mean absolute error): linear penalty on |error|; treats all errors proportionally; robust to outliers. Same units as target.
  - **MSE** (mean squared error): squares errors → **disproportionate weight to large errors/outliers**; squaring also prevents +/− errors from canceling; units are **squared** (e.g., dollars2).
  - **RMSE** = √MSE: restores the **target's original units** (easier to compare to the target scale than MSE), while keeping MSE's emphasis on large errors. RMSE is **more** sensitive to outliers than MAE, not less.
  - **RMSE ≥ MAE always** for the same set of errors (equality only when all absolute errors are equal). A wider RMSE–MAE gap indicates **greater dispersion/variation in error sizes**.
- **Baselines & benchmarking**:
  - A metric value **in isolation is meaningless** — it needs the target scale plus a relevant comparator.
  - **Regression baseline**: predict the **training-set mean** (a naive constant) — the reference for squared-error evaluation. If the model's test RMSE is worse than this baseline, it added no value under that metric.
  - **Classification baseline**: predict the **majority class**. With 60% positive days, an always-up rule scores 60% accuracy; a 58% model is **below** that baseline.
  - **Trading baselines**: buy-and-hold, and a cash / no-trade benchmark, evaluated over the **same period**. Baselines are deliberately **simple** — they need not be more complex than the candidate.
  - Never compute a baseline (or scaling stats) from the **test targets** — that leaks the evaluation set.
- **Fair model comparison**:
  - Score all models on the **same held-out observations** (same period, same rows). Different test periods confound model quality with market-regime difficulty; a common metric does **not** fix unequal test conditions.
  - Use the **same metric and same units** across models; comparing a displayed MAE against a displayed RMSE (or % vs. decimal returns) mixes definitions and scales.
  - **Avoid leakage in preprocessing**: estimate scaling stats (mean/SD) from **training data only**, then apply unchanged to validation/test. Computing them on the full dataset leaks. Leakage is a flaw even for learners insensitive to scaling (e.g., trees), and KNN is especially scale-sensitive because it relies on distances.
- **Metric selection & business alignment**:
  - Low prediction RMSE does **not** guarantee profit — execution costs (spreads, commissions, market impact), decision rules, turnover, and risk sit between forecast and P&L. A statistical improvement that never changes a trade has ~no economic effect.
  - **Do not discard statistical metrics** entirely for trading — they remain diagnostically useful, just not sufficient.
  - **Symmetric metrics** (MAE/MSE/RMSE) ignore error **direction** — they don't distinguish a harmful underestimate from an equal overestimate. Tail-risk / asymmetric-cost settings may need **asymmetric or tail-focused** measures in addition.
  - **Directional accuracy** weights every day equally regardless of move size — a model right more often can still be less profitable than one that captures the few large moves (magnitude, position sizing, costs decide P&L).
  - An economically aligned metric still requires **disciplined out-of-sample evaluation**.
- **Variability & stability of results**:
  - Wide spread of scores across reasonable splits/seeds means performance is **sensitive to the evaluation period / randomness** (often market-regime differences). Report **central tendency AND dispersion**, not the single best run.
  - Variation can arise from sampling and regime shifts **without any implementation defect**.
  - Two models with equal **mean** error can differ greatly in **stability**; when large swings are costly, the more consistent model may be preferable. Window-level inspection reveals regime-specific failure that an average hides.
  - **Record random seeds** (they affect resampling / model construction) for reproducibility. But seed-stability ≠ robustness to future **regime change**.

## Common traps

- **Inverted-logic questions** (7 of 18 here) flip the meaning: the Answer Key states "**True = incorrect; False = accurate**." So marking a statement **False means it is actually correct/accurate**, and **True means it is a flawed/incorrect claim**. Always read the polarity line first. Inverted here: **G1Q3, G2Q2, G3Q3, G4Q2, G5Q1, G5Q3, G6Q1.** In this file each inverted verdict is written as `False (accurate)` or `True (incorrect)` to keep the plain-English meaning visible.
- **No double-negative "embedded claim" choices in Domain 8.** Unlike Domain 1, none of these choices are phrased "It is incorrect to conclude that [accurate statement]." Watch for the pattern anyway — if a choice buries an accurate claim inside a negation, parse the inner claim, judge it, then negate. It does not appear here, so the only polarity twist is the inverted-question header.
- **The "harmless because small data" trap** (G1Q3-D): scarce data does NOT excuse test reuse — it makes contamination *worse*. Marked as a flawed (incorrect) claim.
- **The "RMSE < MAE always" trap** (G2Q2-D): reversed inequality. RMSE is always **≥** MAE for the same errors — flagged incorrect.
- **The "more accurate / more complex must be better" trap** (G3Q2-E, G3Q3-B, G5Q3-B): higher accuracy frequency, higher raw return, or greater model sophistication does **not** by itself establish superiority once baselines, costs, risk, and magnitude enter. These are the classic "sounds obviously true" distractors that are actually false/flawed.
- **The "leakage is OK for trees" trap** (G4Q2-C): a learner's insensitivity to a leak does not make the leak methodologically acceptable — flagged incorrect.
- **The "aligned metric removes need for out-of-sample testing" trap** (G5Q3-E) and **"variation proves the code is buggy" trap** (G6Q1-D): both are flagged incorrect — a good metric still needs OOS validation, and split-to-split variance can be pure sampling/regime effect.

## Questions

### [ML-D8G1Q1] Train / validation / test — the role of each split
**Scenario:** A research team splits ten years of market data into training, validation, and final test periods. It fits candidates on the training period, tunes hyperparameters on the validation period, and plans to report performance from the test period.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Training data are used to estimate model parameters / learned structure from observed examples — the definition of the fitting step. |
| B | True | The validation set supports model and hyperparameter selection *before* the final test, giving feedback for pre-test decisions without fitting the test observations. |
| C | False | Repeatedly inspecting test results while revising features turns the test set into part of the development loop — even though the rows aren't fed to the fit method, the decisions adapt to it, destroying its out-of-sample value. |
| D | True | The test set is most informative as a *final* evaluation precisely when earlier decisions were not adapted to its results — an untouched set is a genuine out-of-sample check. |
| E | False | A validation set cannot guarantee equal future performance in all markets — regime shifts and sampling uncertainty break any such guarantee. |

**Reference:** Train/validation/test roles & the validation set — ISLR §5.1 (the validation-set approach); scikit-learn "Cross-validation: evaluating estimator performance" (train/validation/test split rationale).

### [ML-D8G1Q2] Selecting tree depth on validation, then refitting
**Scenario:** A student trains five decision-tree variants, picks the depth with the lowest validation error, retrains that configuration on the combined training+validation periods, and evaluates it once on a later test period.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Using validation performance to choose tree depth is the standard, intended role of the validation set (hyperparameter selection). |
| B | True | After selection, refitting the chosen configuration on train+validation data is reasonable *provided the test set stays untouched* — it uses more pre-test data for the final fit. |
| C | False | Choosing a different depth whenever the test score disappoints contaminates the final evaluation by adapting the model to the test set. |
| D | True | Evaluating on a *later* period respects temporal order and avoids training on observations from the test period's future (a form of look-ahead leakage a random mix would introduce). |
| E | False | Selecting among many candidates on validation data introduces **selection optimism** — the winning validation score is optimistically low, not free of it. |

**Reference:** Validation for model selection, selection optimism, temporal splits — ISLR §5.1–5.2; concept "look-ahead bias / walk-forward evaluation."

### [ML-D8G1Q3] Skipping validation and tuning on the test score — INVERTED logic
**Scenario:** With only three years of data, an analyst skips validation, selects features/settings by repeatedly checking the test score, and presents the best observed test result as an unbiased estimate of future performance. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: human decisions driven by test feedback create *indirect* adaptation to the test set, even when the test rows are never passed to the fit method. |
| B | False (accurate) | Correct: selecting the best of many trials exploits chance variation in that particular set, so the reported best result is optimistic. |
| C | False (accurate) | Correct: a separate validation procedure can absorb model-selection pressure and reserve the test set for a clean final evaluation. |
| D | True (incorrect) | Wrong: scarce data does **not** make test reuse harmless — fewer observations make contamination worse and estimates less stable, not safer. |
| E | False (accurate) | Correct: test labels are required to compute prediction error (scoring) but should remain outside fitting and tuning. |

**Reference:** Data leakage / test-set hygiene, optimism of the best-of-many — ISLR §5.1; concept "multiple-comparisons / selection bias in evaluation."

### [ML-D8G2Q1] Why RMSE (not MAE) when large errors matter
**Scenario:** A client asks why RMSE is used instead of MAE; the risk team worries about large prediction errors during volatile periods.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | MSE's squared term amplifies large errors, so MSE penalizes big misses more than MAE's linear penalty does. |
| B | False | RMSE is **more** (not less) sensitive to outliers/large errors than MAE — it inherits MSE's squaring. |
| C | True | MAE applies a linear penalty to absolute error magnitude, treating all errors proportionally (equally per unit). |
| D | True | Taking the square root of MSE restores the target variable's original units, so RMSE shares the target's units. |
| E | True | Squaring before averaging places greater emphasis on large deviations, so RMSE highlights large errors more than MAE — matching the risk team's concern. |

**Reference:** MAE vs. MSE vs. RMSE definitions and outlier sensitivity — scikit-learn "Metrics and scoring" (mean_absolute_error, mean_squared_error, RMSE); ISLR §2.2.1 (MSE).

### [ML-D8G2Q2] One large shock error across MAE/MSE/RMSE — INVERTED logic
**Scenario:** Two return-forecasting models are evaluated on the same days; most errors are small but Model A makes one exceptionally large error during a shock. The team compares MAE, MSE, RMSE. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: quadratic loss gives the very large miss disproportionate weight, so it influences MSE more than MAE. |
| B | False (accurate) | Correct: RMSE and MAE weight error magnitudes differently, so a model with small typical errors but one big miss can look better under MAE and worse under RMSE — the rankings can flip. |
| C | False (accurate) | Correct: squaring makes errors nonnegative regardless of sign, so positive and negative errors cannot cancel. |
| D | True (incorrect) | Wrong: RMSE is generally **at least as large as** MAE for the same errors (RMSE ≥ MAE), so it need not — and generally will not — be numerically smaller. |
| E | False (accurate) | Correct: removing the shock day solely because it hurts Model A changes the evaluation question and biases the comparison. |

**Reference:** RMSE ≥ MAE inequality, squared vs. absolute loss, evaluation integrity — scikit-learn "Metrics and scoring"; ISLR §2.2.1; Jensen's-inequality relationship between mean-absolute and root-mean-square.

### [ML-D8G2Q3] Interpreting MAE=$400, MSE=490,000, RMSE=$700
**Scenario:** A model predicts daily dollar profit. MAE is $400, MSE is 490,000 dollars-squared, RMSE is $700. A manager wants to interpret these and decide which loss reflects operational concerns.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | MAE averages the absolute dollar errors, so $400 is the average absolute prediction error. |
| B | False | MSE is in **squared** units (dollars2), not dollars — 490,000 dollars2 is not directly comparable to the target. |
| C | True | RMSE returns the error to the target's original units ($700 in dollars), so it is easier to compare to the target scale than MSE. |
| D | True | RMSE exceeding MAE ($700 > $400) reflects dispersion in error sizes — greater spread in absolute errors widens the RMSE–MAE gap. |
| E | False | Choosing MAE vs. RMSE is not purely mathematical — it should reflect whether large misses are disproportionately costly (linear vs. squared penalty). |

**Reference:** Units of MSE/RMSE and the RMSE–MAE gap as a dispersion signal — scikit-learn "Metrics and scoring"; ISLR §2.2.1.

### [ML-D8G3Q1] Mean-prediction baseline for regression RMSE
**Scenario:** A regression model predicts next-day returns with RMSE 0.012. The team celebrates the low number but has not compared it to a predictor that always outputs the training-set mean return.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | An RMSE value alone lacks context; it needs the target scale and a relevant comparator to show whether the model beats a simple baseline. |
| B | True | Predicting the training mean is the standard naive benchmark for squared-error regression — it reveals whether the model captures useful predictive structure. |
| C | True | If the model's test RMSE is worse than the baseline's on the same observations, the model added no value under that metric (higher RMSE = worse). |
| D | False | A baseline need not be more complex — baselines are deliberately simple; a trivial constant predictor is exactly the point. |
| E | False | Computing the baseline mean from the **test** targets leaks information from the evaluation set; the mean must come from training data. |

**Reference:** Naive/mean baseline for regression, leakage of test statistics — scikit-learn "DummyRegressor" (strategy='mean') and "Metrics and scoring"; concept "skill relative to a baseline."

### [ML-D8G3Q2] Majority-class baseline for imbalanced classification
**Scenario:** A classifier predicts whether tomorrow's return is positive. Because 60% of test days are positive, an always-up rule gets 60% accuracy while the new model gets 58%.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Always predicting the majority class is the standard naive accuracy baseline for an imbalanced outcome. |
| B | False | 58% is **below** the 60% baseline — using features does not make it a win on this metric. |
| C | True | The baseline comparison exposes that apparent accuracy may not exceed a trivial rule — information the raw 58% hides. |
| D | True | The model *might* be useful under a different objective (e.g., asymmetric payoffs), but that requires an appropriate metric and evidence, not assumption. |
| E | False | A sophisticated model is not automatically preferable when it underperforms on the stated objective — complexity alone does not establish value. |

**Reference:** Accuracy baselines & class imbalance — scikit-learn "DummyClassifier" (strategy='most_frequent'), "Metrics and scoring" (accuracy caveats on imbalanced data); ISLR ch.4 (confusion matrices).

### [ML-D8G3Q3] Learned strategy vs. buy-and-hold with omitted costs — INVERTED logic
**Scenario:** A learned strategy beats buy-and-hold on cumulative test return but takes substantially more risk and incurs frequent transaction costs omitted from the simulation. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: buy-and-hold is a simple, investable alternative and a useful benchmark for a trading strategy. |
| B | True (incorrect) | Wrong: higher raw return does **not** prove superiority under every objective — risk, costs, drawdowns, and the investor's goal can reverse the conclusion. |
| C | False (accurate) | Correct: a cash / no-trade benchmark adds context beyond buy-and-hold, helping reveal what kind of value the strategy adds. |
| D | False (accurate) | Correct: omitting transaction costs overstates value added, and frequent (high-turnover) trading magnifies the effect of those unmodeled costs. |
| E | False (accurate) | Correct: benchmarks should span the same market period as the strategy so the comparison controls for market conditions. |

**Reference:** Trading benchmarks (buy-and-hold, cash), transaction-cost realism — Grinold & Kahn "Active Portfolio Management" (benchmark-relative evaluation); concept "backtest cost modeling / turnover."

### [ML-D8G4Q1] Comparing models on different test periods
**Scenario:** A linear model is tested on a calm recent year while a decision tree is tested on an earlier crisis year; both report RMSE and the lower value is declared the winner.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Different test periods confound model quality with market difficulty — one period may be intrinsically harder to predict. |
| B | True | Models should be scored on the same held-out observations so both face a consistent evaluation challenge. |
| C | False | A shared metric (RMSE for both) does not correct for unequal test conditions — same metric, different data is still unfair. |
| D | True | A paired comparison on identical observations enables case-by-case analysis of which model errs where. |
| E | False | A larger training set does not by itself establish better test performance — training size alone proves nothing. |

**Reference:** Common held-out data for fair comparison — scikit-learn "Cross-validation" (same folds across estimators); ISLR §5 (comparing models on identical resamples).

### [ML-D8G4Q2] Scaling from the full dataset before splitting (leakage) — INVERTED logic
**Scenario:** A team compares KNN with a regression tree, standardizing all features using means/SDs computed from the **full** dataset before splitting, then trains both and reports test error. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: computing scaling statistics from the full dataset uses the distribution of held-out observations, exposing the comparison to test information. |
| B | False (accurate) | Correct: scaling parameters should be estimated on training data and applied unchanged to validation/test, keeping test information out of the fitted transform. |
| C | True (incorrect) | Wrong: test leakage is a methodological flaw even if one learner (trees) is largely insensitive to monotonic scaling — it is not acceptable. |
| D | False (accurate) | Correct: a consistent, leakage-free preprocessing protocol appropriate to each learner supports a fairer comparison. |
| E | False (accurate) | Correct: KNN is affected more directly by feature scaling because it relies on distances, where scale changes each feature's relative contribution. |

**Reference:** Preprocessing inside the CV/train fold to prevent leakage — scikit-learn "Pipeline" and "Common pitfalls: data leakage"; ISLR §5 (fit transforms on training data only); KNN distance scaling (ISLR §2.2.3).

### [ML-D8G4Q3] Mixing MAE vs. RMSE and different units
**Scenario:** A researcher reports MAE for Model A and RMSE for Model B and picks whichever displayed number is smaller; Model A is in percentage points while Model B's output was converted to decimal returns.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | MAE and RMSE weight the error distribution differently, so comparing the two displayed numbers mixes different loss definitions. |
| B | True | Different output units make raw values incomparable without conversion — one percentage point equals 0.01 in decimal returns. |
| C | True | Both models should use the same chosen metric and units on the same observations, which isolates model performance from evaluation choices. |
| D | False | A smaller number does not always mean better predictions — metric definition and scale determine what the number means. |
| E | True | Reporting multiple metrics is fine *if* each is computed consistently for both models and interpreted separately — different measures illuminate different tradeoffs. |

**Reference:** Metric/units consistency for fair ranking — scikit-learn "Metrics and scoring" (choose one scorer per comparison); unit-conversion / scale-invariance considerations.

### [ML-D8G5Q1] Low RMSE but the strategy loses money after costs — INVERTED logic
**Scenario:** A model has excellent next-day price RMSE, but a strategy trading its forecasts loses money after spreads, commissions, and market impact. The research lead argues prediction accuracy is all that matters. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: execution costs and decision rules sit between predictions and profit, so low RMSE does not guarantee profitable trading. |
| B | False (accurate) | Correct: a trading-oriented evaluation may need returns, risk, turnover, and transaction costs to connect to the deployed objective. |
| C | False (accurate) | Correct: improving RMSE on small forecasts that never flip a trade has little effect — a statistical gain need not alter any economically relevant decision. |
| D | True (incorrect) | Wrong: statistical prediction metrics should **not** be discarded entirely for trading — they remain diagnostically useful even when insufficient. |
| E | False (accurate) | Correct: the evaluation criterion should reflect how model outputs convert into positions and outcomes (the full decision pipeline). |

**Reference:** Statistical metric vs. economic objective, net-of-cost evaluation — Grinold & Kahn "Active Portfolio Management"; concept "signal vs. execution / implementation shortfall."

### [ML-D8G5Q2] Asymmetric / tail-cost loss for a risk system
**Scenario:** A risk system predicts daily portfolio losses. The firm views a $100 error on an ordinary day as manageable but a $10,000 underestimate on a stressed day as especially dangerous.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A measure that places extra weight on large misses (e.g., squared error) better reflects the firm's disproportionate concern for severe misses than MAE alone. |
| B | True | MSE/RMSE emphasize large absolute errors through squaring, magnifying the contribution of the big misses. |
| C | True | A symmetric metric treats equal-magnitude over- and under-estimates the same, even though the firm considers underestimation more harmful — MAE/MSE/RMSE ignore error direction. |
| D | False | The lowest average error does not automatically identify the safest model under tail-risk objectives — averages can conceal dangerous behavior in critical cases. |
| E | True | The team may need an asymmetric or tail-focused evaluation in addition to standard aggregate metrics to capture unequal, tail-specific costs. |

**Reference:** Asymmetric loss & tail-risk metrics — concept "expected shortfall / quantile (pinball) loss / cost-sensitive evaluation"; scikit-learn "Metrics and scoring" (custom/asymmetric scorers).

### [ML-D8G5Q3] Directional accuracy vs. profit-weighted evaluation — INVERTED logic
**Scenario:** A model calls direction correctly 55% of days but is mostly right on tiny moves and often wrong on large moves; another model has 52% directional accuracy but captures several large profitable moves. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: directional accuracy counts a correct tiny move and a correct large move each as one correct classification, weighting days equally regardless of move size. |
| B | True (incorrect) | Wrong: being correct more often does **not** guarantee greater trading profit — frequency of correct direction does not determine payoff magnitude. |
| C | False (accurate) | Correct: return magnitude, position sizing, and trading costs can make the 52% model more economically valuable. |
| D | False (accurate) | Correct: evaluating only directional accuracy may be misaligned with a profit objective because it ignores the consequences of being right or wrong. |
| E | True (incorrect) | Wrong: choosing an economically aligned metric does **not** remove the need for disciplined out-of-sample evaluation — any metric still requires OOS testing. |

**Reference:** Directional accuracy vs. profit-weighted / magnitude-aware evaluation, and the necessity of OOS testing — concept "hit-rate vs. P&L"; ISLR §5 (out-of-sample validation).

### [ML-D8G6Q1] Reporting only the best of five split RMSEs — INVERTED logic
**Scenario:** A decision tree gets test RMSE of 0.010, 0.011, 0.029, 0.013, 0.026 across five reasonable time-based splits; the analyst wants to report only the lowest value. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the substantial spread across plausible windows shows performance is sensitive to the evaluation period. |
| B | False (accurate) | Correct: reporting only 0.010 conceals variability — that single value is not representative of all trials. |
| C | False (accurate) | Correct: summarizing both central performance and dispersion gives a fuller, more honest picture than the best run alone. |
| D | True (incorrect) | Wrong: variation across splits does **not** prove every implementation is incorrect — it can arise from sampling and regime differences without any defect. |
| E | False (accurate) | Correct: differing market regimes (changing relationships/volatility over time) can contribute to the observed instability. |

**Reference:** Cross-validation variability, report mean ± spread not the best fold — ISLR §5.1 (variance of the validation estimate); scikit-learn "Cross-validation" (cv score mean and std).

### [ML-D8G6Q2] Bagged learner vs. single deep tree — seed stability
**Scenario:** A bagged learner retrained ten times under different seeds has nearly identical validation scores, while a single deep tree's scores vary widely; their average validation errors are similar.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The bagged learner is more stable with respect to the tested randomness — its scores barely change when the seed changes. |
| B | False | Similar average error does not mean identical reliability — models with the same mean can have very different dispersion. |
| C | True | Random seeds that affect resampling or model construction should be recorded to improve reproducibility and clarify experimental conditions. |
| D | True | Repeated runs distinguish a typical result from a lucky initialization or sample — a single outcome cannot reveal that sensitivity. |
| E | False | Low variation across seeds does not guarantee stability under future regime change — seed stability tests randomness, not distributional shift. |

**Reference:** Bagging variance reduction, seed/reproducibility, repeated evaluation — ISLR §8.2 (bagging reduces variance); scikit-learn "Ensemble methods" and reproducibility (random_state).

### [ML-D8G6Q3] Equal mean MAE, different window-level stability
**Scenario:** Two models have the same mean out-of-sample MAE across six sequential windows; Model A is consistent every window while Model B is excellent in four and very poor in two volatile windows. Large performance swings are costly.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Equal mean MAE does not imply equal stability — the same average can arise from very different distributions of performance. |
| B | True | Model A may be preferable because its lower variability aligns with the stated cost of large swings. |
| C | True | Examining window-level results exposes failure patterns (Model B's two bad windows) that the overall average conceals. |
| D | False | Strong performance in four windows does **not** make the two poor windows irrelevant — poor behavior in volatile periods can be operationally critical. |
| E | True | The choice may reasonably depend on both average error and variability, reflecting typical accuracy and stability requirements. |

**Reference:** Mean vs. dispersion of performance, regime-specific weakness — ISLR §5.1 (variance of estimates); concept "consistency / drawdown-aware model selection."

## References (domain-level)

1. **ISLR — *An Introduction to Statistical Learning* (James, Witten, Hastie, Tibshirani):** §2.2.1 (measuring quality of fit, MSE, training vs. test error, out-of-sample generalization); §5.1–5.2 (the validation-set approach, cross-validation, variance of the estimate, temporal/leakage considerations); ch.4 (classification, accuracy, confusion matrices); §8.2 (bagging / variance reduction).
2. **ESL — *The Elements of Statistical Learning* (Hastie, Tibshirani, Friedman):** ch.7 (model assessment and selection, optimism of the training error, cross-validation, the "one-standard-error" rule for choosing simpler models).
3. **scikit-learn User Guide:** "Metrics and scoring" (MAE, MSE, RMSE units and outlier sensitivity, precision/recall/F1, ROC-AUC); "Cross-validation: evaluating estimator performance" (shared folds, mean ± std reporting); "Common pitfalls and recommended practices: data leakage" (fit preprocessing on the training fold only); "Dummy estimators" (mean / majority-class baselines).
4. **Concept references (metric definitions):** RMSE ≥ MAE relationship for a fixed error set; symmetric vs. asymmetric loss and direction-insensitivity of MAE/MSE/RMSE; quantile (pinball) loss and expected shortfall for tail-cost objectives; Brier score for probabilistic outputs.
5. **Grinold & Kahn — *Active Portfolio Management*:** connecting predictive signal to net-of-cost outcomes (turnover, transaction costs, risk, benchmark-relative evaluation) for the metric-selection / business-alignment questions.
