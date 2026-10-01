# ML Domain 9 — Overfitting, Underfitting & Generalization

## Domain cheat-sheet

- **Overfitting vs. underfitting** is read off the *pair* of training and out-of-sample errors, never one alone:
  - **Overfitting**: near-zero (very low) training error but much worse test/validation error → the model memorized sample-specific noise. Symptom of **high variance**. Fixes: reduce capacity, add representative data, regularize, early-stop.
  - **Underfitting**: high error on *both* training and test, roughly similar → the model is too simple to capture the true structure. Symptom of **high bias**. Fixes: add capacity / richer features; more data does NOT help.
  - A **small train–test gap alone does not prove generalization** — two similarly *poor* scores mean the model is consistently weak, not useful. You need low *and* similar errors.
- **Bias–variance tradeoff** (expected out-of-sample error = bias2 + variance + irreducible error):
  - Increasing model complexity/capacity typically **lowers bias but raises variance**; it does *not* reduce both at once. The best model minimizes *total* expected out-of-sample error, not either term in isolation.
  - Validation error is **U-shaped** in complexity: falls then rises. The depth/complexity with lowest *validation* error is generally a better choice than the one with lowest *training* error.
  - **High variance ≠ high training error** — a high-variance model often fits each training set extremely well (low training error) yet swings wildly across samples.
  - **Low variance ≠ accurate** — a stable model (e.g., a straight line on a curved relationship) can be consistently and systematically wrong (high bias).
- **Model capacity vs. data size**:
  - More *representative* data reduces variance/overfitting by making recurring patterns easier to distinguish from noise — but it **cannot cure bias**: it never expands the functions a fixed hypothesis class can express (a linear model stays linear no matter how many rows).
  - **Duplicated rows add no independent information**; only genuinely new observations help.
  - More data does **not guarantee** an arbitrarily complex model won't overfit (capacity, noise, leakage, bad sampling still bite), and quantity **cannot compensate** for data drawn from the wrong distribution/regime (representativeness ≥ raw count).
- **Cross-validation & generalization estimation**:
  - k-fold: each fold is held out for evaluation exactly once; a *separate* model is fit per round (the held-out fold is excluded from that round's training). Averaging fold scores gives a less split-specific estimate than one arbitrary holdout.
  - **Selection bias / optimism**: picking the best of many tuned alternatives makes the winning CV score optimistic. A separate **untouched test set** is needed for an honest final estimate — don't reuse the same evidence for selection and final assessment.
  - **Leakage discipline**: any preprocessing that *learns from data* (normalization, scaling) must be fit **within each training fold**, never once on the full dataset — global fitting leaks held-out info.
  - **Time order matters**: for time series, random folds can train on the future and test on the past (unrealistic). Use forward/rolling (time-aware) splits. More folds do NOT repair a wrong splitting design; CV is not "invalid for all time series," just needs adaptation.
- **Detecting overfitting in practice**:
  - Large train–test gap; **instability** (splits/structure/returns change dramatically across resamples); **"too good to be true"** results.
  - Implausibly strong scores → check for **leakage** (e.g., a feature built from the *next day's* close) and evaluation errors before believing a "market inefficiency."
  - **Selection/search overfitting**: trying hundreds of configs on one validation period will surface a chance winner; its edge collapses out of sample. Record the full search and re-evaluate the pick on fresh data.
  - Reporting only the best of several runs hides variance and creates false optimism.
- **Controlling model complexity** (hyperparameters as capacity knobs):
  - Trees: **lower max depth** and **larger min leaf size** reduce effective complexity. **KNN**: larger *k* smooths / lowers capacity (more bias, less variance); *k*=1 is highest capacity (low bias, high variance, ~0 training error).
  - **Regularization**: penalizing large coefficients constrains (does not free) the fit; moderate strength trades a little bias for lower variance and better generalization; too strong → underfitting. A positive penalty alone does not "eliminate" the need for validation.
  - **Early stopping**: halt near best validation iteration — a form of complexity control. Stop too early → underfit. Lowest *training* error does not imply best out-of-sample model.
  - Complexity knobs should be tuned on **validation** evidence, keeping the final **test set independent** of tuning. No setting is guaranteed to help on every dataset.

## Common traps

- **Inverted-logic questions** (6 of 18 here): the Answer Key reads "**True = incorrect; False = accurate**," so a **False** verdict means the statement is *actually correct*, and **True** means it is *flawed*. Read the polarity line first every time. Inverted here: **G2Q1, G2Q2, G3Q2, G4Q2, G5Q1, G6Q1.**
- **Double-negative / trap "must / always / necessarily / guarantees" choices**: absolute claims are the planted wrong answers. Watch "must reduce both bias and variance" (G2Q1D), "necessarily correct the problem" (G1Q2C), "always identifies the best model" (G1Q3D), "guarantees ... cannot overfit" (G3Q1D), "every model class can represent every target" (G3Q2D), "guarantees ... all future periods" (G4Q2D), "always increases capacity" (G2Q3E), "automatically correct any violation" (G4Q3E), "guaranteed to improve ... every dataset" (G6Q1D), "eliminates the need for validation" (G6Q2E), "must produce the best out-of-sample model" (G6Q3D).
- **Small train–test gap ≠ good model.** Two similarly poor scores (underfitting) show consistency, not predictive value (G1Q2E, G1Q3, G6). Judge on *level* and *gap* together.
- **"Too good to be true" = suspect leakage first.** A next-day-close feature or full-dataset normalization inflates scores; a high score does not prove a durable edge (G5Q1, G5Q3). In inverted G5Q1, choice D ("high score proves durable inefficiency") is the one flawed claim marked **True**.
- **More data fixes variance, not bias.** Adding rows (even a million) to a linear model on a curved target does not remove approximation error (G3Q2); duplicated rows add nothing (G3Q1C); wrong-regime data doesn't generalize (G3Q3).
- **Instability is a variance symptom.** Splits/returns swinging across resamples = high variance/overfitting even with ~0 training error; never report only the best run (G5Q2).

## Questions

### [ML-D9G1Q1] Near-zero training error, poor on new data — classic overfitting
**Scenario:** A team's model shows near-zero training error but much worse performance on new data, and the PM asks whether that is acceptable.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Near-zero training error with poor performance on unseen data is the textbook overfitting signature — the model fit sample-specific noise rather than the underlying signal. |
| B | True | Strong sensitivity to the particular training sample is the defining trait of high variance, which is what overfitting expresses. |
| C | True | More representative training data makes sample-specific noise harder to fit and typically shrinks the generalization gap (variance-reduction). |
| D | True | Reducing model capacity/complexity limits the model's ability to memorize noise, directly attacking overfitting. |
| E | False | Underfitting produces poor performance even on the *training* data; here training error is near zero, so this is not underfitting. |

**Reference:** Overfitting & the bias-variance tradeoff — ISLR §2.2 (assessing model accuracy, U-shaped test error); ESL ch.7 (model assessment).

### [ML-D9G1Q2] Shallow tree, high similar errors — underfitting
**Scenario:** A shallow decision tree is fit to a nonlinear indicator→return relationship; both training and test errors are high and similar, and adding data without changing the tree barely helps.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Similarly high training and test errors are the hallmark of underfitting — the model is too simple to fit even the data it has seen. |
| B | True | A shallow tree has limited capacity and may be unable to express the relevant nonlinear pattern (high bias). |
| C | False | Making the tree *shallower* reduces capacity further and would generally worsen underfitting, not correct it. |
| D | True | Adding modest capacity (more depth / richer features) can capture missed structure and reduce bias. |
| E | False | A small train–test gap alone only shows consistency; two similarly poor scores do not demonstrate useful generalization. |

**Reference:** Underfitting / high bias, capacity of trees — ISLR §2.2 (bias-variance); ISLR ch.8 (tree depth as complexity).

### [ML-D9G1Q3] Three models — matching patterns to over/underfitting
**Scenario:** Model A has high training and high validation error; Model B has very low training but high validation error; Model C has moderate, similar training/validation error and the best validation score.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | High error even on training data means Model A is not capturing enough structure — underfitting / high bias. |
| B | True | Excellent training fit with poor validation performance is the standard overfitting (high-variance) symptom. |
| C | True | Model C has the best validation performance with no large train–validation gap, giving the strongest evidence of generalization. |
| D | False | Lowest training error rewards memorization and does not establish performance on new data; it never "always" identifies the best model. |
| E | False | The train–validation gap is informative for both regression and classification, not classification only. |

**Reference:** Diagnosing over/underfitting from train vs. validation curves — ESL ch.7 (generalization gap); scikit-learn "Underfitting vs. overfitting."

### [ML-D9G2Q1] Increasing tree depth — bias-variance (INVERTED)
**Scenario:** As max tree depth increases, training error falls at every step while validation error first falls then rises once the tree is deep. The team asks which claims are flawed.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Very shallow trees systematically miss useful structure — relatively high bias. The statement is correct. |
| B | False (accurate) | Very deep trees become sensitive to noise and small training-set changes — relatively high variance. Correct. |
| C | False (accurate) | Validation error better reflects the goal of performing on unseen data, so the lowest-validation depth is a better choice than lowest-training depth. Correct. |
| D | True (incorrect) | Flawed: greater capacity typically *reduces bias while increasing variance* — it does not reduce both simultaneously. |
| E | False (accurate) | Worsening validation despite improving training fit is evidence of overfitting. Correct. |

**Reference:** Bias-variance tradeoff, U-shaped validation curve — ISLR §2.2.2; scikit-learn "Validation curves."

### [ML-D9G2Q2] Linear vs. flexible learner across samples — bias vs. variance (INVERTED)
**Scenario:** Across many resampled training sets, a straight-line model predicts consistently but keeps missing a curve, while a flexible nonlinear learner fits the curve on average but changes a lot across samples. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The linear model's repeated, systematic miss of the same structure is high bias. Correct. |
| B | False (accurate) | The nonlinear learner's large swings across plausible samples are high variance. Correct. |
| C | False (accurate) | A low-variance model can still be consistently inaccurate when too restrictive (stable but biased). Correct. |
| D | True (incorrect) | Flawed: high variance does NOT require high training error — a high-variance model can fit each training set extremely well yet generalize poorly. |
| E | False (accurate) | Selection should balance both error sources via expected out-of-sample error, not minimize bias or variance alone. Correct. |

**Reference:** Bias-variance decomposition — ISLR §2.2.2; ESL ch.7 (bias, variance, and their tradeoff).

### [ML-D9G2Q3] KNN and k — smoothing, bias, variance
**Scenario:** A KNN regressor is tested across values of k; at k=1 predictions track individual training points, while at very large k predictions are nearly constant.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | With k=1 a point can be its own nearest neighbor, giving extremely low (often near-zero) training error versus a heavily smoothed large-k model. |
| B | True | Larger k averages over a broader neighborhood, smoothing the prediction function. |
| C | True | Very large k over-smooths and averages away local structure, increasing bias. |
| D | True | Very small k makes predictions hinge on a few neighbors, so they change sharply across samples — high variance. |
| E | False | Larger k *reduces* effective flexibility/capacity of KNN; it does not always increase capacity. |

**Reference:** KNN flexibility vs. k, bias-variance — ISLR §2.2.3 (KNN) and §3.5; scikit-learn "Nearest Neighbors."

### [ML-D9G3Q1] Deep tree on 300 days — value of more data
**Scenario:** A deep tree overfits a 300-day training set; the team can collect several years of comparable data from the same data-generating process.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A larger representative sample reduces sensitivity to accidental patterns in the small dataset (variance reduction). |
| B | True | More observations make estimates of recurring patterns more reliable by separating signal from noise. |
| C | False | Duplicated copies of the same 300 rows add no independent information, so they do not give the benefit of genuinely new data. |
| D | False | More data does not *guarantee* an arbitrarily complex model won't overfit — excess capacity, noise, leakage, or poor sampling can still cause it. |
| E | True | The usefulness of extra data depends on whether it represents the deployment setting; unrepresentative data may not help. |

**Reference:** Data size vs. variance, representativeness — ISLR §2.2 (more data reduces variance); ESL ch.7; concept "learning curves."

### [ML-D9G3Q2] Linear model on a curve + a million rows — capacity, not size (INVERTED)
**Scenario:** A linear model underfits a strongly curved relationship; the analyst adds a million more observations but keeps the same linear feature representation and model form. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | More data alone cannot remove error caused by inability to represent the curve — it doesn't change the model's expressible functions. Correct. |
| B | False (accurate) | The limitation is capacity (hypothesis-class expressiveness), not sample size. Correct. |
| C | False (accurate) | A richer feature representation or more expressive model may be needed to reduce this systematic error. Correct. |
| D | True (incorrect) | Flawed: data quantity does not let *every* model class represent *every* target function — the hypothesis class still restricts what can be expressed. |
| E | False (accurate) | More data can still estimate the best linear approximation's parameters more precisely even though approximation bias remains. Correct. |

**Reference:** Hypothesis-class / approximation error (bias) vs. estimation error — ESL ch.7 (bias-variance, model capacity); ISLR §2.2.

### [ML-D9G3Q3] Small clean data vs. large stale-regime data — representativeness
**Scenario:** Team A trains on 500 clean, relevant observations; Team B on 50,000 mostly from an old market regime with different relationships from the deployment period.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A larger row count does not automatically generalize to the new regime — quantity cannot fix wrong-distribution data. |
| B | True | Relevant sampling can matter as much as raw size; training data should reflect the relationships the model will face. |
| C | True | Regime mismatch (non-stationarity) can cause poor deployment performance even with low training error. |
| D | False | Smaller datasets do not "always" contain less bias; there is no rule guaranteeing Team A's superiority. |
| E | True | Evaluating both on representative out-of-sample data reveals which dataset supports the intended use. |

**Reference:** Distribution shift / non-stationarity, representativeness — ESL ch.7; concept "regime shift / covariate shift."

### [ML-D9G4Q1] Five-fold cross-validation mechanics
**Scenario:** A researcher runs five-fold CV: each round trains on four folds and evaluates on the remaining one, each fold serving as the evaluation fold once.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Every fold takes exactly one turn as the held-out evaluation subset, so each observation is evaluated once. |
| B | False | The evaluation fold is excluded from training in its round — a model is not trained on its own evaluation fold. |
| C | True | Averaging over multiple partitions gives a less split-specific estimate than a single arbitrary holdout. |
| D | False | A separate model is fit for each training-fold combination; CV is not five evaluations of one fixed model. |
| E | True | Data-learning preprocessing must be fit within each training portion; fitting it globally leaks evaluation-fold information. |

**Reference:** k-fold cross-validation — ISLR §5.1 (cross-validation); scikit-learn "Cross-validation" + "data leakage in preprocessing."

### [ML-D9G4Q2] CV for depth selection reported as final estimate (INVERTED)
**Scenario:** A student selects tree depth from 20 alternatives by CV, then reports the best mean CV score as the final unbiased performance estimate with no separate test set. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Comparing validation performance across depths is a valid use of CV. Correct. |
| B | False (accurate) | Choosing the best of many alternatives makes the selected CV score optimistic (selection bias). Correct. |
| C | False (accurate) | A separate untouched test set gives a stronger final check by not reusing evidence for selection and assessment. Correct. |
| D | True (incorrect) | Flawed: CV cannot *guarantee* the selected depth generalizes equally well to all future periods — sampling uncertainty and market change forbid such a guarantee. |
| E | False (accurate) | Folds should respect the data's structure (e.g., time order); ordinary random folds may be inappropriate. Correct. |

**Reference:** Selection bias / optimism of the tuned score, held-out test set — ISLR §5.1 & §6 (model selection); ESL ch.7 (the "training-set reuse" fallacy).

### [ML-D9G4Q3] Random folds on time series — temporal leakage
**Scenario:** A team randomly assigns daily observations from ten years to CV folds, so models are sometimes trained on later dates and evaluated on earlier ones, though deployment predicts the future from the past.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Random folds let future information influence models evaluated on the past — mismatching deployment's temporal direction. |
| B | True | Time-aware (forward/rolling) folds that train on earlier and validate on later data better mirror forecasting use. |
| C | True | Using future observations for training can mislead when relationships change over time (non-stationarity). |
| D | False | CV is not invalid for every time-series problem — it can be adapted (blocked/rolling) to preserve time order. |
| E | False | Increasing the fold count does not repair an inappropriate splitting design; the leakage is structural. |

**Reference:** Time-series cross-validation / look-ahead leakage — scikit-learn "TimeSeriesSplit"; concept "walk-forward validation."

### [ML-D9G5Q1] 99.9% accuracy from leakage (INVERTED)
**Scenario:** A model reports 99.9% directional accuracy on unseen data; the analyst finds features were normalized using full-dataset statistics and one feature used the next day's closing price. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | An implausibly strong result should prompt checks for leakage and evaluation errors. Correct. |
| B | False (accurate) | Using the next day's close to predict next-day direction feeds the model information unavailable at decision time (target leakage). Correct. |
| C | False (accurate) | Full-dataset normalization contaminates evaluation because test-period info influences preprocessing. Correct. |
| D | True (incorrect) | Flawed: a very high score does NOT prove a durable market inefficiency — leakage is the more immediate explanation and the result needs validation. |
| E | False (accurate) | Rebuilding the pipeline to use only information available at each point is necessary for a credible assessment. Correct. |

**Reference:** Data leakage (target and preprocessing) — scikit-learn "Common pitfalls: data leakage"; concept "look-ahead bias."

### [ML-D9G5Q2] Tree retrained on five samples — instability
**Scenario:** A single decision tree is retrained on five slightly different samples; training error stays near zero but chosen splits and out-of-sample returns change dramatically run to run.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Small data changes producing large changes in the learned model and its results is model instability. |
| B | False | Near-zero training error does not rule out overfitting — extremely low training error often accompanies it. |
| C | True | Sensitivity to small sample changes is a defining symptom of high variance. |
| D | True | Examining results across repeated samples exposes variability that a single run would hide. |
| E | False | Reporting only the most profitable run conceals variability and creates a misleadingly optimistic impression. |

**Reference:** Model stability / variance under resampling — ESL ch.7 & ch.8 (tree instability, motivation for bagging); concept "bootstrap stability."

### [ML-D9G5Q3] 500 configs, one validation period — selection overfitting
**Scenario:** An analyst tries 500 combinations on one validation period; one earns an exceptional Sharpe ratio but has an ordinary training score and collapses on a later test period.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Trying many alternatives raises the chance of finding a config that benefits from random validation noise (multiple-comparisons effect). |
| B | True | The later test failure is consistent with selection overfitting — the config adapted to validation-period peculiarities. |
| C | False | The best of 500 trials is not an unbiased estimate; taking the maximum observed score introduces selection optimism. |
| D | True | Recording the full search and evaluating the pick on untouched data improves credibility by testing for a durable edge. |
| E | False | An ordinary training score does not guarantee the validation success was genuine; search-driven results still need fresh validation. |

**Reference:** Multiple-comparisons / backtest overfitting — concept "data snooping, deflated Sharpe ratio"; ISLR §5–6 (selection with a held-out set).

### [ML-D9G6Q1] Deep overfitting tree — depth & leaf-size controls (INVERTED)
**Scenario:** A deep tree fits nearly every fluctuation in training data but does poorly on validation; the team considers reducing max depth and increasing minimum leaf size. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Reducing max depth limits the number of successive splits — fewer levels to partition the data. Correct. |
| B | False (accurate) | A larger minimum leaf size prevents leaves for very small groups, discouraging over-specific partitions. Correct. |
| C | False (accurate) | Both changes reduce the tree's effective complexity. Correct. |
| D | True (incorrect) | Flawed: these changes are NOT guaranteed to improve test performance on every dataset — excessive restriction can cause underfitting, and results are data-dependent. |
| E | False (accurate) | Complexity controls should be chosen using validation evidence, keeping the final test set independent. Correct. |

**Reference:** Tree pruning / complexity control hyperparameters — ISLR ch.8 (pruning, min node size); scikit-learn "Decision Trees: controlling complexity."

### [ML-D9G6Q2] Regularized linear regression — penalty strength
**Scenario:** A team uses regularized linear regression with a penalty on large coefficients and gradually increases the penalty strength while watching training and validation error.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The penalty makes large coefficient magnitudes costly, discouraging reliance on them (shrinkage). |
| B | False | A stronger penalty *constrains* the fitted solution rather than increasing its freedom to fit training data. |
| C | True | Moderate regularization trades a little bias for lower variance, improving generalization when the unregularized model overfits. |
| D | True | An excessively strong penalty over-shrinks and suppresses useful relationships, causing underfitting. |
| E | False | A positive penalty does not eliminate the need for validation — the right strength is data-dependent and must be tuned. |

**Reference:** Regularization / shrinkage (ridge, lasso) — ISLR §6.2 (shrinkage methods); ESL ch.3 (ridge regression) & ch.7.

### [ML-D9G6Q3] Divergence at iteration 40 — early stopping
**Scenario:** During iterative training, training error keeps falling; validation error falls through iteration 40 then rises steadily while training keeps improving. The team considers early stopping.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Divergence after iteration 40 (validation up, training down) indicates later iterations are fitting non-generalizing detail — overfitting. |
| B | True | Stopping near the best validation iteration limits how fully the learner adapts to the sample — a form of complexity control. |
| C | False | The stopping point should be chosen on a validation set, not by repeatedly examining the final test set (which would contaminate it). |
| D | False | Minimizing training error need not give the best out-of-sample model; the lowest training error can occur after generalization worsens. |
| E | True | Stopping too early leaves useful structure unlearned, causing underfitting. |

**Reference:** Early stopping as regularization — ESL ch.7 (model selection); scikit-learn "Early stopping" / validation-curve docs.

## References (domain-level)

1. **ISLR — *An Introduction to Statistical Learning* (James, Witten, Hastie, Tibshirani):** §2.2 (assessing model accuracy, bias-variance tradeoff, irreducible error, U-shaped test-error curve), §2.2.3 (KNN flexibility vs. k), ch.5 (cross-validation, the validation set and k-fold CV), §6.2 (shrinkage / regularization: ridge and lasso), ch.8 (trees, depth and pruning as complexity controls).
2. **ESL — *The Elements of Statistical Learning* (Hastie, Tibshirani, Friedman):** ch.7 (model assessment & selection, bias-variance decomposition, generalization gap, optimism of the training error rate), ch.3 (ridge regression), ch.8 (bagging / tree instability under resampling).
3. **scikit-learn User Guide:** "Underfitting vs. overfitting" example, "Validation curves" and "Learning curves," "Cross-validation" (k-fold, TimeSeriesSplit), and "Common pitfalls and recommended practices: data leakage" (preprocessing fit inside CV folds).
4. **Concept references:** bias-variance decomposition (expected error = bias2 + variance + irreducible error); regularization / shrinkage and early stopping as capacity control; learning curves (data size vs. error); generalization gap.
5. **Non-stationarity / backtest overfitting:** regime shift and covariate/distribution shift; look-ahead and target leakage; multiple-comparisons / data-snooping bias in strategy search (e.g., deflated Sharpe ratio) for the detection-in-practice questions.
