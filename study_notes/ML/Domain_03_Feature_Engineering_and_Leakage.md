# ML Domain 3 — Feature Engineering & Leakage

## Domain cheat-sheet

- **Feature construction from raw inputs**: derived features (ratios, growth rates, margins) can expose relationships the raw level does not. A *growth* term encodes a temporal change; a *ratio/margin* (profit ÷ revenue) is scale-adjusted and comparable across firms. But a transformation only helps if it adds representable structure — restating existing information (a pure re-expression) can be redundant and add no new signal.
- **Feature interactions**: a purely additive linear model (β₁x₁ + β₂x₂) cannot represent a *conditional/multiplicative* effect (e.g., "high volume matters differently in rising vs. falling markets"). An explicit interaction term (sign × volume) encodes that joint dependence. Adding flexibility can help, do nothing, or overfit — it never *guarantees* better out-of-sample performance.
- **Nonlinear transforms for linear learners**: polynomial/other basis expansions let a linear combination express curved relationships. More terms = more capacity to fit noise, especially with limited data. Judge usefulness on **held-out** data, never training error alone.
- **Scaling & normalization** — *learner-dependent*:
  - **Distance/gradient-based learners (KNN, neural nets, SVM)** are scale-sensitive: an unscaled large-magnitude feature dominates Euclidean distance; unscaled inputs cause exploding/saturating gradients. Standardize (z-score) so features contribute on comparable scales. Scaling changes *numerical influence*, not information content, and does not equalize predictive value.
  - **Tree-based learners (CART, Random Forest, GBDT)** split on order/thresholds → invariant to any monotonic (incl. positive-linear, z-score, quantile) per-feature transform. Removing an unneeded scaling step simplifies the pipeline without changing tree predictions. Trees are still vulnerable to noise, leakage, and irrelevant inputs.
  - **Fit the scaler on training data only**, then apply to held-out/live data (a causal, backward-looking window). Refitting on the full/test window leaks future distribution info even though no *target* is touched.
- **Non-stationarity traps in scaling** (finance-specific):
  - **Rolling z-score in a volatility spike**: the denominator (rolling σ) balloons, *deflating* the z-score and masking a genuine tail event (Domain 3 G2Q4).
  - **Standardizing an exponential/trending series**: training mean/σ become unrepresentative; production values drift out-of-distribution (G2Q5).
  - **Cross-sectional quantile transform**: preserves rank but caps at [0,1]; a market-wide crash where *all* values spike leaves percentiles unchanged → an "information blackout" that strips the macro signal (G2Q6).
- **Stationarity tests are limited**: the **ADF test** only rejects a unit root (stochastic trend in the *mean*); a series can pass ADF yet still suffer structural breaks or variance drift. Rolling OLS betas are unstable under regime shifts (non-stationarity); remedies are exponentially-weighted regression or state-space/Kalman filters (G1Q4–Q6).
- **Irrelevant & redundant features**: random/irrelevant columns give a flexible learner more chances to fit spurious patterns → higher selection/evaluation variance; training correlation can be accidental. Highly **collinear** features carry overlapping info: in **OLS** they destabilize coefficient estimates (near-singular X'X, inflated standard errors); in **tree ensembles** they *dilute* feature importance (credit is split across duplicates) but do not break the splitting math. Redundancy is task-dependent — a correlated feature can still add conditional information. Remedies: judge on validated (out-of-sample) performance, weigh cost/latency/reliability, or project to orthogonal components via **PCA**.
- **Feature selection intuition**: reducing the feature space lowers estimation variance and spurious-pattern opportunities — especially valuable when *features ≫ observations*. The tradeoff: pruning can discard weak-but-real signal (omitted-variable bias / underfitting) and typically *raises* in-sample error while lowering out-of-sample variance (bias–variance). Lowest training error ≠ best subset. **PCA** is *unsupervised* (maximizes X-variance, ignores y) so it may drop a low-variance but highly predictive direction, and its components lose interpretability. **Ridge (L2)** shrinks all coefficients toward (never exactly) zero, keeping every feature; **Lasso (L1)/Best-Subset** produce sparsity and win when the true model is sparse. Wrapper searches (SFS/Best-Subset) that optimize a backtest metric **overfit the selection step itself** (selection bias) even if the final model is small.
- **Target leakage**: a feature that encodes the outcome (post-resolution status codes, "days since eventual last transaction," post-alert review codes) yields unrealistic accuracy that vanishes in deployment. Leakage is about *timing/lineage*, not the column name — renaming does nothing. Leakage also travels through **preprocessing and feature-selection decisions** (fitting scalers, imputers, or target-guided selectors on pooled train+test data) and through **cross-sectional pooling** (computing a sector total/mean or cross-sectional σ over the full universe before splitting folds). Fix: reconstruct every feature point-in-time; fit all learned steps (scaling, imputation, selection) strictly within each training fold.
- **Look-ahead bias in time-series**: using information not yet available at the decision timestamp. A **centered moving average / z-score** (uses t−k…t+k) peeks forward — replace with a **trailing** window (…t−1, t). A **chronological split does NOT fix a feature whose own construction looks forward**. Backfilling revised/restated fundamentals into earlier dates, joining by fiscal year without publication lags, using today's *close* to trade today's *open*, or using an auction print to participate in that same auction are all look-ahead. Future returns are valid as **labels** (once realized) but never as contemporaneous features. Use a **point-in-time (PIT)** database that stores each value's publication/effective date.
- **"Too good to be true" features**: an abrupt, implausible jump in accuracy (53% → 99%), an opaque vendor feature, or a suspiciously high-importance field with unclear lineage/timing warrants a leakage/lineage audit. Correlation ≠ causation (e.g., ticker alphabetical order "predicts" returns); confidentiality, feature importance, and historical presence do not establish point-in-time availability. Diagnostics: verify feature timestamp precedes the decision, ablate/lag the feature, and replicate across untouched periods/universes.

## Common traps

- **Inverted-logic questions (12 of 39):** the Answer Key reads "**True = incorrect; False = accurate**," so a **True** verdict flags the statement as *wrong* and **False** confirms it is *correct*. Read the polarity line before every question. Inverted here: **G1Q2, G1Q4, G2Q3, G2Q6, G3Q3, G3Q5, G3Q6, G4Q2, G5Q2, G5Q6, G6Q1, G7Q2.**
- **Double-negative "embedded claim" choices:** a choice states "**The following claim is false: [X]**" or "**It is incorrect to conclude that [X]**." Parse inner claim X, judge *its* truth, then negate. When X is accurate, asserting it is false/incorrect is itself wrong. In **normal** polarity these resolve to verdict **False** (G5Q3A, G5Q4A, G6Q2A, G6Q3A) or **True** when X is inaccurate (G2Q5A). In **inverted** polarity they flip again: G2Q3A → True (incorrect), G3Q3A → True, G4Q2A → True, G5Q6A → False (accurate), G6Q1... (G6Q1 has plain choices). Always separate the *polarity* flip from the *embedded-negation* flip.
- **Scaling is learner-dependent — never "mandatory for every algorithm."** Trees are invariant to monotonic per-feature transforms; distance/gradient learners are not. Watch for choices claiming scaling is universally required (false) or that trees are "immune to all data problems" (false — noise/leakage/irrelevance still bite).
- **"Chronological split prevents all temporal leakage" is false.** A forward-looking feature (centered MA, t+k windows, execution using same-bar auction price) leaks regardless of how the train/test boundary is drawn.
- **Leakage hides in preprocessing/selection, not just raw columns.** Fitting a scaler, imputer, target-correlation ranker, Lasso selector, or cross-sectional statistic on pooled data (or the full universe before splitting) contaminates the evaluation even when no future-dated column enters the final model. Excluding the target column is *not* sufficient.
- **PCA and rank-based transforms are monotonic/rank-preserving — they do NOT alter within-window rank order.** Choices claiming z-score or quantile mapping "changes the rank-order of the data points" are wrong; the real failures are out-of-distribution drift, denominator inflation, or information blackout.
- **A ratio scaled by a firm's *own contemporaneous, point-in-time* figure is clean** (G5Q6C); a ratio scaled by a *cross-sectional universe aggregate computed before the split* leaks (G5Q6A).

## Questions

### [ML-D3G1Q1] Derived financial-statement features (growth, margin, PIT)
**Scenario:** An equity team predicting next-month returns debates using raw revenue vs. revenue growth and profit margin to compare firms of different sizes, without using information unavailable on the prediction date.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Revenue *growth* encodes a change over time; a single revenue *level* cannot express that temporal relationship directly. |
| B | True | Profit ÷ revenue is a margin — a scale-adjusted feature that normalizes for firm size and supports cross-firm comparison. |
| C | False | A transformation does *not* necessarily add information; it may merely restate existing inputs and be redundant. |
| D | True | Publication dates matter: using figures before they became public would make the historical feature unavailable in practice (look-ahead bias). |
| E | False | Appropriate transformations also improve distance measures and neighborhood structure — not only linear models benefit. |

**Reference:** Feature construction & scale-adjusted ratios — ISLR ch.3 (linear model features); point-in-time availability / look-ahead bias concept.

### [ML-D3G1Q2] Return-sign × volume interaction — INVERTED logic
**Scenario:** A futures desk's linear model includes price and volume separately; the head trader suspects volume's effect depends on whether price is rising or falling, and considers a return-sign × relative-volume interaction. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: an interaction feature represents a relationship depending on the joint values of two inputs — effects beyond additive contributions. |
| B | True (incorrect) | Wrong: separate additive linear terms do NOT automatically represent a multiplicative/conditional interaction between the variables. |
| C | False (accurate) | Correct: a price-direction × volume feature lets high volume mean different things in rising vs. falling markets. |
| D | True (incorrect) | Wrong: adding the interaction does not *guarantee* better out-of-sample performance — the added flexibility may help, do nothing, or overfit. |
| E | False (accurate) | Correct: a deployable interaction must be computed only from information known at the trade-decision time. |

**Reference:** Interaction terms & additive-model limits — ISLR §3.3.2 (interaction terms, hierarchy); bias-variance of added flexibility §2.2.2.

### [ML-D3G1Q3] Polynomial expansion vs. generalization
**Scenario:** A credit fund predicts bond price changes from days-to-maturity, coupon, and yield; a junior wants dozens of polynomial terms while the risk officer fears instability with limited default history. Balance representation vs. generalization.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A nonlinear (e.g., polynomial) transform lets a linear learner express curved relationships via a linear combination of basis terms. |
| B | True | Many polynomial features raise model complexity and overfitting risk — more terms = more chances to fit noise, especially with little data. |
| C | False | A transform computed only from existing features *can* change predictions — re-expressing inputs alters what the learner can fit. |
| D | True | Usefulness must be assessed on data not used to fit or select the terms — held-out evaluation estimates generalization. |
| E | False | Lower training error alone does not establish out-of-sample value; a complicated feature is not preferable just because it cuts training loss. |

**Reference:** Polynomial/basis expansion & overfitting — ISLR §7.1 (polynomial regression), §2.2.2 (bias-variance); cross-validation ch.5.

### [ML-D3G1Q4] Rolling-beta instability = non-stationarity — INVERTED logic
**Scenario:** A multi-factor model uses rolling 12-month OLS betas of tech stocks vs. the Nasdaq 100 as features; during a high-volatility pivot, predictive power collapses and coefficients are highly unstable. Mark each statement True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: beta instability is a classic symptom of non-stationarity — the stock-index relationship changes over regimes; a bull-market beta misrepresents risk in a shock. |
| B | True (incorrect) | Wrong: a fixed rolling window *mitigates* but does not *eliminate* non-stationarity — a structural break inside the window leaves OLS parameters as a polluted average of two regimes. |
| C | False (accurate) | Correct: standard OLS assumes an invariant data-generating process (its residual/independence assumptions break when parameters shift at regime changes). |
| D | False (accurate) | Correct: rapid degradation reflects a structural break — the historical 12-month window acts as an anchor that fails to capture the sudden step-change until old data rolls off. |
| E | False (accurate) | Correct: without changing feature definitions, exponentially weighting recent observations (EWMA regression / a Kalman-filter state-space model) lets parameters adapt to drift. |

**Note:** Only B is flagged incorrect. C's rationale reframes OLS's assumption as "homoscedastic, independent residuals" rather than full DGP stationarity — the key accepts the statement as accurate; keep verdict False.
**Reference:** Non-stationarity, structural breaks, adaptive estimation — Hamilton *Time Series Analysis* (structural change, state-space/Kalman); ESL §7 (model assessment under drift).

### [ML-D3G1Q5] ADF test blind spots (variance drift)
**Scenario:** A momentum classifier feeds a 50-day rolling variance of returns straight into a deep net after an ADF test rejects a unit root (p<0.01); accuracy later collapses under a regime shift with severe structural drift. Which statement correctly diagnoses why ADF failed and gives the right remedy?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Wrong: ADF is *designed* to detect stochastic trends (unit roots) and handles deterministic trends via a time-trend (βt) term — it is not limited to fixed linear trends. |
| B | False | Wrong: there is no 252-day minimum; ADF validity depends on sample size, lag structure, and the DGP, not a calendar constraint. |
| C | False | Wrong: rejecting the null does not guarantee all moments are invariant — it only rules out a random walk; breaks/heteroscedasticity/seasonality can remain. |
| D | False | Wrong: ADF does not mechanically invert its error rates just because a feature is bounded/non-negative; the DF distribution assumes i.i.d. errors, not Gaussian data. |
| E | True | Correct: ADF checks only a unit root / stochastic trend in the *mean*; a mean-reverting series can still have its variance/distribution warp under regime shifts — the test does not account for that. |

**Reference:** Augmented Dickey-Fuller test scope & limits — Hamilton *Time Series Analysis* (unit-root testing); stationarity vs. structural-break distinction.

### [ML-D3G1Q6] ADF test blind spots (duplicate of G1Q5)
**Scenario:** Identical to G1Q5 — a rolling-variance feature passes an ADF unit-root rejection, is fed raw into a deep net, and collapses under regime drift. (Verbatim repeat in the pool.)
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Wrong: ADF specifically targets stochastic trends and models deterministic trends with a βt term. |
| B | False | Wrong: no arbitrary 252-day structural minimum exists for ADF validity. |
| C | False | Wrong: an ADF rejection is not a blanket guarantee of stationarity; breaks/heteroscedasticity/seasonality persist. |
| D | False | Wrong: boundedness/non-negativity does not mechanically flip the test's error rates. |
| E | True | Correct: ADF only checks a mean unit root; variance/distribution drift under regime shift escapes it — a key feature-engineering limitation. |

**Reference:** Same as G1Q5 — ADF scope/limits (Hamilton); stationarity vs. structural break.

### [ML-D3G2Q1] KNN dominated by unscaled volume
**Scenario:** A wealth manager's KNN finds similar market days using daily return (~0.01) and volume (millions of shares); neighbors are determined almost entirely by volume.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Without scaling, a large-magnitude feature dominates a Euclidean distance calculation. |
| B | True | Standardizing puts return and volume on comparable numerical scales so both contribute to distance. |
| C | False | Scaling changes numerical influence, not underlying information content — it does not equalize predictive value. |
| D | True | Scaling parameters should be estimated from training data, not the held-out test data (else train/test separation weakens). |
| E | False | Rescaling can change which observations are nearest — KNN predictions are *not* always unchanged by rescaling. |

**Reference:** Feature scaling for distance-based learners — scikit-learn "Preprocessing data" (StandardScaler), "Nearest Neighbors"; ISLR §2.2.3.

### [ML-D3G2Q2] Tree vs. KNN under scaling; pipeline simplicity
**Scenario:** A group compares a decision tree and KNN on the same standardized financial ratios and asks whether scaling helps both equally, while keeping the production pipeline simple.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A conventional tree splits on value ordering, so a positive linear (monotonic) rescale leaves its partition structure unchanged. |
| B | True | KNN neighborhoods depend on distances, so it is sensitive to changing relative feature scales. |
| C | False | Standardization is not mandatory for every algorithm — the need depends on the learner and representation. |
| D | True | Removing an unnecessary scaling step can simplify the tree's pipeline without materially changing predictions. |
| E | False | Trees not needing scaling does not make them immune to noise, leakage, irrelevant inputs, or other data problems. |

**Reference:** Scale-invariance of trees vs. distance-based models — scikit-learn "Preprocessing" & "Decision Trees"; pipeline hygiene (`sklearn.pipeline`).

### [ML-D3G2Q3] Full-window normalization introduces hindsight — INVERTED logic
**Scenario:** A global macro desk uses a distance-based model over rolling windows; volatility spikes in the test period and an analyst proposes normalizing each observation using the mean/σ of its entire window (including later test dates). Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Embedded: "The following claim is *false*: using later test obs to set earlier scaling introduces future info." The inner claim is accurate, so declaring it false is itself incorrect — full-window scaling *does* leak future distribution info. |
| B | False (accurate) | Correct: applying *training-period* scaling parameters to later observations preserves the train/test boundary (the rule was learned without seeing them). |
| C | False (accurate) | Correct: a large standardized test value can legitimately signal a genuine distribution shift beyond the training range — not a preprocessing error. |
| D | True (incorrect) | Wrong: recomputing a scaler over the full test period is *not* safe — leakage occurs through future feature statistics even without using the target. |
| E | False (accurate) | Correct: a causal rolling scaler using only pre-decision observations (a consistently defined backward window) is reproducible at deployment. |

**Reference:** Leakage via preprocessing statistics — scikit-learn "Common pitfalls: data leakage" (fit scaler on train only, `Pipeline`); look-ahead bias in time-series.

### [ML-D3G2Q4] Rolling z-score deflates a shock (denominator inflation)
**Scenario:** A hedge fund standardizes macro/fundamental features with a rolling-36-month z-score before a GBDT; during a liquidity freeze the raw macro indicators spike but their z-scores stay in normal bounds and precision drops. Which statement diagnoses the flaw and remedy?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Wrong: the CLT concerns the distribution of sample *means*, not standardizing individual points; ~156 weekly obs is ample for parameter estimation. |
| B | False | Wrong: standard z-score does not automatically truncate/cap at ±3.0 — that would require an added clipping/winsorization step. |
| C | False | Wrong: z-scoring is monotonic and preserves within-window rank order; tree models are invariant to monotonic per-feature transforms anyway. |
| D | True | Correct: in a volatility spike the rolling σ (denominator) balloons, deflating the z-score and masking the anomaly's true severity — a classic non-stationary-standardization pitfall. |
| E | False | Wrong: a fixed calm-period scaler avoids denominator expansion but no scaling choice can *guarantee* reliable behavior under every future distribution shift. |

**Reference:** Standardization under non-stationarity / denominator inflation — scikit-learn "Preprocessing" (StandardScaler caveats); Marcos López de Prado *Advances in Financial ML* (stationarity/fractional differencing).

### [ML-D3G2Q5] Standardizing an exponentially trending series
**Scenario:** A macro fund standardizes exponentially growing indices (Industrial Production, Retail Sales) by subtracting the training mean and dividing by the training σ before a deep net. Which statement diagnoses the production failure and contrasts unscaled behavior?
**Answer polarity:** Normal (True = accurate) — embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Embedded: "It is incorrect to conclude that standardization fails *because of look-ahead bias*." The inner leakage claim is inaccurate — the failure is a distribution-shift issue, not an accidental data leak — so rejecting it is correct. |
| B | True | Correct: with an exponential trend the mean/σ drift upward, so standardized production values keep growing into regions never seen in training (distribution shift). |
| C | False | Wrong: deep nets are *not* invariant to unscaled trending inputs — on raw exponential data gradients explode/saturate, destabilizing training from the start. |
| D | False | Wrong: raw macro indices are not mean-reverting/bounded — they grow with inflation and expansion, which is exactly why engineers try to scale them. |
| E | False | Wrong: z-scoring is linear and preserves rank order; the breakdown is out-of-distribution values in production, not a distortion of past rankings. |

**Reference:** Distribution shift from non-stationary features; gradient stability of NN inputs — scikit-learn "Preprocessing"; López de Prado (stationarity), ISLR §2.2.

### [ML-D3G2Q6] Cross-sectional quantile transform masks a crash — INVERTED logic
**Scenario:** A cross-sectional alpha model maps right-skewed Book-to-Market ratios to a uniform [0,1] via a quantile transform before a neural net. Mark each statement True if incorrect (diagnosing side-effects during a regime shift vs. unscaled behavior).
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Wrong: quantile mapping is monotonic (percentile-based) and *preserves* the cross-sectional rank order — it does not change it. |
| B | False (accurate) | Correct: in a market-wide crash absolute values spike but relative percentiles stay identical, so the [0,1] output masks the macro destruction — a real blind spot of rank-based normalization. |
| C | True (incorrect) | Wrong: on unscaled right-skewed data, extreme outliers dominate MSE and make gradients explode — backprop does not "cancel out" their variance. |
| D | True (incorrect) | Wrong: an ECDF maps real inputs to [0,1] and cannot produce complex/imaginary numbers, however extreme the outlier. |
| E | False (accurate) | Correct: unlike Min-Max (which exceeds 1.0 on new maxima), the quantile transform caps extremes at the 1.0 bucket — removing the out-of-bounds issue but creating an information blackout that makes a severe outlier look like a mild one. |

**Reference:** QuantileTransformer vs. MinMaxScaler behavior on tails — scikit-learn "Preprocessing" (non-linear/quantile transforms); rank-based normalization limitations.

### [ML-D3G3Q1] Hundreds of random columns
**Scenario:** A fund adds hundreds of random columns believing a capable learner ignores useless inputs; validation varies widely across splits and the risk team questions the expanded set. The model must be stable on unseen markets.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Irrelevant features give a flexible learner more chances to fit accidental (spurious) patterns. |
| B | True | With finite data, adding random inputs increases variance in model selection and evaluation. |
| C | False | An irrelevant feature is *not* guaranteed zero influence — many algorithms assign it weight due to sampling variation. |
| D | True | Comparing held-out performance with vs. without the random features tests their effect on generalization. |
| E | False | Training-sample correlation with the target may be accidental, unstable, or leakage-driven — not sufficient justification. |

**Reference:** Curse of dimensionality / spurious features — ISLR §6.1 (why fewer features help), §2.2.2; ESL §7.

### [ML-D3G3Q2] Near-duplicate vendor field (collinearity)
**Scenario:** A bank predicts default using debt-to-equity plus a near-exact duplicate from another vendor; compliance wants all variables kept, the modeling lead worries redundancy complicates interpretation. Comparing linear and tree learners.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Highly correlated features carry overlapping rather than independent information. |
| B | True | In a linear model, strong collinearity makes individual coefficient estimates unstable. |
| C | False | Two redundant features do not double predictive information — duplication adds no independent signal. |
| D | True | A tree may pick one of several similar features, so feature-importance attributions vary across samples. |
| E | False | Removing a redundant variable does not *always* reduce out-of-sample accuracy — it may leave it unchanged or improve stability. |

**Reference:** Multicollinearity effects & tree importance splitting — ISLR §3.3.3 (collinearity, VIF); scikit-learn "Permutation importance with multicollinear features."

### [ML-D3G3Q3] Correlation ≠ interchangeability — INVERTED logic
**Scenario:** A commodity fund finds warehouse inventory and weeks-of-supply strongly correlated (the latter also embeds expected demand); the PM wants to drop one by correlation alone, the analyst says judge redundancy by the prediction task. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Embedded: "The following claim is *false*: strong correlation does not prove interchangeability." The inner claim is accurate (correlated features can differ in nonlinear/conditional behavior), so calling it false is incorrect. |
| B | False (accurate) | Correct: a feature can add conditional information even when strongly correlated with another — residual differences may still predict the target. |
| C | True (incorrect) | Wrong: predictor correlation alone does not establish that one feature is causally irrelevant. |
| D | False (accurate) | Correct: comparing validated models reveals whether removing one feature sacrifices useful (generalizable) information. |
| E | False (accurate) | Correct: with similar predictive value, operational cost, latency, and data reliability can decide between redundant features. |

**Reference:** Correlation vs. causation / conditional information — ISLR §3.3.3; feature-selection tradeoffs (cost/reliability) — production ML practice.

### [ML-D3G3Q4] 50 collinear technical indicators
**Scenario:** A team adds 50 near-duplicate momentum/MA-crossover indicators; training metrics improve marginally but live risk-adjusted returns drop and turnover/costs rise; an audit finds high collinearity. Which statement diagnoses the mathematical and operational impact?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Wrong: trees do not invert a covariance matrix to split — they evaluate features sequentially; collinearity degrades interpretability but does not make them "fail completely." |
| B | True | Correct: correlated indicators dilute Mean-Decrease-Impurity importance — the ensemble randomly uses one or another across nodes, splitting the credit and hiding dominant signals. |
| C | False | Wrong: collinearity typically *increases* out-of-sample prediction variance via unstable estimation, not artificially narrows prediction variance. |
| D | True | Correct: in linear regression, high collinearity makes individual coefficients unstable and data-sensitive even when overall predictions stay relatively stable. |
| E | True | Correct: PCA projects correlated features into orthogonal components, isolating core variance and stripping collinear redundancy. |

**Reference:** MDI dilution under correlation; OLS instability; PCA decorrelation — scikit-learn "Permutation importance with multicollinear features," "PCA"; ISLR §3.3.3, §6.3 (PCA/PCR).

### [ML-D3G3Q5] RF vs. unregularized OLS on redundant indices — INVERTED logic
**Scenario:** A quant desk keeps 15 macro sentiment indices (4 with pairwise r>0.92) and trains both a Random Forest and an unregularized OLS to compare how each handles redundancy. Mark each statement True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Wrong: sample size does not cure multicollinearity — OLS estimates stay extremely sensitive to minor data variation regardless of N. |
| B | False (accurate) | Correct: the RF splits node selections across the ~identical indices, lowering each one's importance and making a predictive group look trivial on an importance plot. |
| C | False (accurate) | Correct: severe multicollinearity inflates coefficient variance/standard errors, which can make OLS out-of-sample predictions unstable — especially if correlations shift between train and test. |
| D | True (incorrect) | Wrong: RFs split sequentially/greedily and do not invert a covariance matrix; collinearity degrades importance interpretability but does not break the splitting math or collapse accuracy to zero. |
| E | True (incorrect) | Wrong: RFs do not auto-isolate one of a correlated set — bootstrap samples *rows*, not features; a random feature subset is considered per split, so redundant features are used throughout and dilute importances. |

**Note:** C (accurate) and G3Q4-D (accurate, "predictions relatively stable") are subtly in tension. Reconcile via the key's caveat: correlated-feature OLS predictions stay stable *while the correlation structure holds* but become unstable *when that structure changes between train and test*. Keep both verdicts as the key gives them.
**Reference:** Bootstrap samples rows not features; multicollinearity persists with large N — scikit-learn "Random Forest," "Permutation importance with multicollinear features"; ISLR §3.3.3, ch.8.

### [ML-D3G3Q6] Sequential Forward Selection overfits the backtest — INVERTED logic
**Scenario:** A pipeline runs SFS to add features maximizing out-of-sample Sharpe over 150 factors; the final 12-feature subset backtests superbly but underperforms the all-150 baseline live. Mark each statement True if incorrect (diagnosing the statistical flaw).
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: SFS adds features one at a time and can miss interaction effects where two features help only together; a feature rejected early is not reconsidered with later additions. |
| B | False (accurate) | Correct: the collapse is selection bias / backtest overfitting — the wrapper treats backtest performance as the objective and "mines" historical noise for a lucky subset. |
| C | True (incorrect) | Wrong: selecting a column subset does not change the underlying joint distribution of those variables — it just discards others; the failure is over-optimizing on noise, not a distributional alteration. |
| D | True (incorrect) | Wrong: wrapper methods evaluate subsets using the *exact* downstream model (they are directly tuned to it) — the opposite of "optimizing independently of hyperparameters." |
| E | True (incorrect) | Wrong: greedy SFS does not favor low-variance features by default — it picks whatever maximizes the objective (Sharpe); failure is noise capitalization, not a low-variance bias. |

**Reference:** Wrapper-method selection bias / multiple-testing on backtests — ISLR §6.1 (subset selection, validation), ch.5; López de Prado (backtest overfitting, deflated Sharpe).

### [ML-D3G4Q1] Small data, hundreds of features
**Scenario:** A small-cap strategy has three years of weekly data but hundreds of accounting/sentiment candidates; the PM wants to keep all, the research lead fears searching too many accidental relationships. The model must perform reliably out of sample.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Reducing the feature space lowers the number of spurious patterns available to the learner. |
| B | True | Feature selection is especially valuable when candidate features are large relative to observations. |
| C | False | Selecting features using the full dataset (incl. the test period) contaminates the final test — it does not preserve an unbiased evaluation. |
| D | True | Removing features reduces overfitting but may also discard genuine signal (a tradeoff). |
| E | False | The lowest-training-error subset is not necessarily best — training fit does not measure generalization and favors complexity. |

**Reference:** Feature selection when p≫n; validation hygiene — ISLR §6.1, ch.5 (cross-validation); curse of dimensionality.

### [ML-D3G4Q2] Rank-then-report on same data — INVERTED logic
**Scenario:** A firm ranks 1,000 features by correlation with next-day returns, keeps the top 20, and reports performance on the same observations used for ranking; the head of research says using only 20 inputs removes overfitting concern. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Embedded: "The following claim is *false*: searching 1,000 candidates can overfit the selection step even if the final model uses 20." The inner claim is accurate, so declaring it false is incorrect — the search itself can pick chance-correlated predictors. |
| B | False (accurate) | Correct: evaluating the selected subset on the same observations used to rank features produces optimistic results. |
| C | True (incorrect) | Wrong: feature selection is a learned preprocessing decision and *must* be validated (contained within the CV loop), not treated as outside the model. |
| D | False (accurate) | Correct: selection should be repeated within each training fold so each validation fold stays uninvolved in choosing its features. |
| E | False (accurate) | Correct: a final untouched test period gives a more independent assessment once the selection procedure is frozen. |

**Reference:** Selection-inside-CV / leakage from feature ranking — scikit-learn "Common pitfalls: data leakage," "Nested cross-validation"; ISLR ch.5, §6.1.

### [ML-D3G4Q3] 12 vs. 150 features — cost & maintainability
**Scenario:** A pension manager wants a transparent, small-team-maintainable risk model; a 12-feature model nearly matches a 150-feature model in rolling validation, but several of the 150 need expensive alt-data feeds.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Similar validated performance can favor the smaller model when cost and maintainability matter. |
| B | True | Fewer features reduce exposure to feed failures and future changes in data availability. |
| C | False | The larger set is not automatically superior for containing the smaller one — extra inputs add noise, instability, cost, and overfitting risk. |
| D | True | Fewer inputs improve interpretability — fewer variables for stakeholders to understand. |
| E | False | A small accuracy difference should not override deployment constraints; the gain may not justify cost/fragility. |

**Reference:** Parsimony / operational-cost tradeoffs — ISLR §6.1 (model interpretability); production ML practice (data-dependency risk).

### [ML-D3G4Q4] Tree-importance pruning for a linear model
**Scenario:** An analyst prunes 80 features to the top 15 using a tree-based importance threshold before fitting a regularized linear model, to combat out-of-sample decay. Evaluate the statistical benefits and tradeoffs.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Correct: fewer parameters reduce estimation variance — the linear model focuses on robust relationships rather than high-dimensional noise. |
| B | False | Wrong: shrinking the feature space does not reduce bias — constraining inputs typically *increases* bias (less flexibility). |
| C | True | Correct: the classic risk is omitted-variable bias — dropping 65 features may discard weak-but-collectively-useful signals, causing underfit. |
| D | False | Wrong: tree-based selection does not alter the rank-order/values of the data and does not invalidate downstream OLS estimation. |
| E | True | Correct: restricting capacity limits overfitting but usually raises in-sample (training) error — the bias-variance tradeoff in action. |

**Reference:** Bias-variance of feature reduction; omitted-variable bias — ISLR §6.1, §2.2.2; feature selection via tree importance (scikit-learn `SelectFromModel`).

### [ML-D3G4Q5] PCA before a neural net
**Scenario:** A fund compresses 300 macro/sentiment/order-flow features into 10 PCA components and trains a neural net only on them, to control overfitting. Which statements correctly diagnose the tradeoffs and risks?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Wrong: PCA controls collinearity/dimensionality but does not eliminate overfitting — a deep net can still overfit 10 components if its capacity is unconstrained. |
| B | True | Correct: PCA is unsupervised (maximizes X-variance, ignores y), so it may discard a low-variance direction that is highly predictive of the target. |
| C | False | Wrong: orthogonal inputs *help* NN training — decorrelation reduces ill-conditioning of the loss surface and aids gradient-descent convergence. |
| D | True | Correct: reducing 300→10 dimensions lowers estimation variance, yielding a more parsimonious model less prone to overfit. |
| E | True | Correct: interpretability is lost — each component is a linear combination of all 300 raw features, so risk cannot be attributed to specific economic drivers. |

**Reference:** PCA as unsupervised dimensionality reduction (variance ≠ predictiveness); conditioning benefits — ISLR §6.3 (PCR), §12.2; scikit-learn "PCA," "Decomposition."

### [ML-D3G4Q6] Best-Subset Selection vs. Ridge
**Scenario:** With 250 order-flow variables for an intraday model, one faction wants a sparse 20-feature Best-Subset model, the other wants all 250 under heavy Ridge (L2). Evaluate the tradeoffs and structural differences.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Correct: Best-Subset reduces estimation variance but adds *selection variance* — the combinatorial search can overfit by picking noise-fitting features by chance. |
| B | True | Correct: Ridge shrinks all coefficients toward zero, cutting flexibility and estimation variance while retaining every variable. |
| C | False | Wrong: a 250-feature Ridge model (larger functional space) will almost always achieve lower/equal *training* error than a 20-feature subset — sparsity does not guarantee lower in-sample loss. |
| D | True | Correct: keeping 250 features under Ridge is an operational drag — production must ingest/transform 230 more variables than the sparse model. |
| E | False | Wrong: if the true model is sparse, Lasso/Best-Subset generally beat Ridge — Ridge shrinks but never sets coefficients exactly to zero, so it cannot drop the noise variables. |

**Reference:** Ridge vs. Lasso/Best-Subset (shrinkage vs. sparsity, selection variance) — ISLR §6.1–§6.2 (subset selection, ridge, lasso); ESL §3.4.

### [ML-D3G5Q1] Post-resolution status code (target leakage)
**Scenario:** A default model uses an account-status code recorded *after* collections closes the case and hits near-perfect accuracy; the credit officer wants to deploy but model-risk questions when the code becomes available.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A post-resolution status code may encode the outcome itself → target leakage. |
| B | False | Wrong: high accuracy says nothing about whether the feature is available at prediction time. |
| C | True | Each feature should be reconstructed using only information available at the prediction timestamp (point-in-time). |
| D | True | Removing the leaked field likely lowers measured performance but yields a more realistic, credible estimate. |
| E | False | Wrong: strong association *caused by outcome information* is precisely why leakage is misleading, not harmless. |

**Reference:** Target leakage / point-in-time reconstruction — scikit-learn "Common pitfalls: data leakage"; Kaufman et al. "Leakage in Data Mining."

### [ML-D3G5Q2] "Days since eventual last transaction" — INVERTED logic
**Scenario:** A brokerage predicts account closures monthly; a feature "days since final transaction" is computed after month-end using the customer's *eventual* last transaction date. A PM argues it is not the label so it cannot be leakage. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a feature can leak target information without being an exact copy of the label. |
| B | False (accurate) | Correct: using an *eventual* last-transaction date reveals future behavior unavailable at the monthly prediction date. |
| C | True (incorrect) | Wrong: renaming the field does not eliminate leakage — leakage depends on the underlying data and timing, not the column name. |
| D | False (accurate) | Correct: auditing feature lineage and timestamps exposes how the field was calculated and whether it postdates the decision. |
| E | False (accurate) | Correct: a valid replacement computes days since the most recent transaction *known as of* each prediction date (reproducible live). |

**Reference:** Derived-feature leakage & lineage auditing — scikit-learn "data leakage"; point-in-time feature engineering.

### [ML-D3G5Q3] Target-guided selection leaks even if target column excluded
**Scenario:** A quant standardizes, selects predictors, and tunes, but the selector used correlations with target returns from *both* train and test periods; the PM insists there is no leakage since no future-return column enters the final model.
**Answer polarity:** Normal (True = accurate) — embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded: "The following claim is *false*: target info used to choose features can leak into development." The inner claim is accurate (target-guided selection is part of fitting the pipeline), so calling it false is incorrect. |
| B | False | Wrong: excluding the target column is *not* sufficient — the target can influence development indirectly via selection. |
| C | True | Correct: test-period targets shaped which predictors survived, so the reported test result is no longer independent. |
| D | True | Correct: feature selection should be fitted on training data and applied unchanged to held-out data. |
| E | True | Correct: leakage can travel through preprocessing and selection decisions, not just raw feature columns. |

**Reference:** Leakage through selection/preprocessing; selection-inside-CV — scikit-learn "Common pitfalls," "Nested CV"; ISLR ch.5.

### [ML-D3G5Q4] Cross-sectional pooling (sector denominator before split)
**Scenario:** A cross-sectional model uses "Relative Profitability" = firm net income ÷ sector-wide total net income, but the sector total is computed globally across all 800 firms *before* splitting into CV folds. Which statement diagnoses the target leakage and contrasts an isolated pipeline?
**Answer polarity:** Normal (True = accurate) — embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded: "It is incorrect to conclude that target leakage occurs because the global denominator leaks validation info into training." The inner claim is accurate (this *is* cross-sectional leakage via pooling), so declaring it incorrect is false. |
| B | True | Correct: the global denominator embeds the scale/health/distribution of the whole peer universe — metadata that is uncalibrated/missing when a new firm is scored alone in production. |
| C | False | Wrong: leakage is not exclusively temporal — absorbing info from validation/test partitions across peers is also leakage. |
| D | True | Correct: comparing CV scores against a structurally isolated out-of-universe test set exposes the leak (a sharp drop reveals it). |
| E | True | Correct: remediation requires computing cross-sectional summary statistics strictly within each training fold, then applying that static mapping to validation. |

**Reference:** Cross-sectional / pooling leakage; fit-transform within folds — scikit-learn "Common pitfalls: data leakage," `Pipeline`+`cross_val_score`.

### [ML-D3G5Q5] Lasso feature selection on the full dataset before split
**Scenario:** A predictive-maintenance latency model fits a Lasso selector on the *entire* dataset to pick non-zero features, then trains a deep net on an 80/20 split and gets exceptional precision. Which statement diagnoses the target leakage and its consequences?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Wrong: Lasso's linearity does not make it "absorb future residual variance" — the leak is structural (pooling before the split), not a functional-form effect. |
| B | True | Correct: selecting features on the full dataset lets test-set target/joint-distribution info dictate which features reach the neural net. |
| C | True | Correct: the test metrics are an illusion — the 20% test set helped select the features, so the net sees a space pre-optimized to fit those exact records. |
| D | False | Wrong: regularization does not prevent leakage when run on pooled data — Lasso uses whole-dataset info to shrink coefficients, bridging the split. |
| E | True | Correct: remediation fits the Lasso selector on the training partition only; the test partition stays blind until final evaluation. |

**Reference:** Feature-selection pooling leakage — scikit-learn "Common pitfalls: data leakage," `SelectFromModel` inside a `Pipeline`; ISLR ch.5, §6.2.

### [ML-D3G5Q6] Five signals — which is leakage-free — INVERTED logic
**Scenario:** An auditor reviews five alpha signals for a cross-sectional momentum pipeline (K-fold CV); four contain structural target leakage and one is clean. Mark each statement True if incorrect (the clean one is the "accurate" statement).
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Embedded: "It is incorrect to conclude that Signal Alpha [cross-sectional σ over all 600 stocks before splitting] leaks." The inner claim is inaccurate — it *is* cross-sectional leakage — so rejecting it is correct. |
| B | True (incorrect) | Wrong: Signal Beta imputes NaNs with a median over the entire 10-year slice before splitting → temporal/partition leakage via preprocessing. |
| C | False (accurate) | Correct: Signal Gamma deflates R&D by the firm's own point-in-time quarterly revenue (definitive publication date) → no future info, no cross-partition contamination → clean. |
| D | True (incorrect) | Wrong: Signal Delta's rolling window for day t spans t−2…t+7 → classic look-ahead, absorbing the future the model is forecasting. |
| E | True (incorrect) | Wrong: Signal Epsilon selects keywords via a chi-square test against y across the whole database → feature-selection pooling leakage. |

**Reference:** Point-in-time cleanliness vs. pooling/look-ahead leakage across preprocessing, imputation, selection — scikit-learn "Common pitfalls"; López de Prado (PIT, CV in finance).

### [ML-D3G6Q1] Trade the open using today's close — INVERTED logic
**Scenario:** A strategy trades at each day's open using an indicator built from that day's official close; the backtest Sharpe is high, but the close does not exist when the opening trade is placed. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the indicator contains future information relative to the trade decision (the close occurs after the open). |
| B | False (accurate) | Correct: shifting the feature so an opening trade uses the *previous* day's close restores causal timing (prior close is known before the next open). |
| C | True (incorrect) | Wrong: applying the biased formula consistently does not remove the bias — consistent use of unavailable info remains biased. |
| D | False (accurate) | Correct: a strong backtest can arise from information impossible to obtain live (hindsight/artificial predictive power). |
| E | False (accurate) | Correct: feature timestamps must be aligned with actual decision/execution times — calendar labels alone don't prove availability. |

**Reference:** Look-ahead bias, causal feature timing — López de Prado *Advances in Financial ML* (labeling/timing); backtest realism principles.

### [ML-D3G6Q2] Backfilling revised fundamentals
**Scenario:** A global equity model joins annual fundamentals to daily prices by fiscal year and copies revised statements backward to every date in that year; the research director says it is fine since all refer to the same company-year. Does the dataset reflect what traders knew?
**Answer polarity:** Normal (True = accurate) — embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded: "The following claim is *false*: backfilling a later filing/revision into earlier dates can create look-ahead bias." The inner claim is accurate, so declaring it false is incorrect — earlier simulated decisions would receive later-published info. |
| B | True | Correct: a point-in-time database must retain each value's publication/effective date to reconstruct the live information set. |
| C | False | Wrong: describing past operations does not mean the values were *available* throughout the year — economic coverage ≠ public-availability date. |
| D | True | Correct: restatements should not silently replace originally available figures in a historical simulation. |
| E | True | Correct: joining by fiscal year alone ignores reporting delays between the measured period and public release. |

**Reference:** Point-in-time databases, restatement/reporting-lag bias — López de Prado (PIT data); survivorship/look-ahead bias literature.

### [ML-D3G6Q3] Centered moving average with a chronological split
**Scenario:** A pipeline labels each day with the next 5-day return and builds a *centered* 10-day MA (5 past + 5 future obs); the team uses a chronological train/test split and believes that alone prevents temporal leakage.
**Answer polarity:** Normal (True = accurate) — embedded-claim wording in A.

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded: "The following claim is *false*: a chronological split does not prevent leakage inside a feature computed with future obs." The inner claim is accurate, so calling it false is incorrect — splitting cannot repair a forward-looking feature. |
| B | True | Correct: the centered MA uses prices unavailable at the day being scored (half its window is in the future). |
| C | True | Correct: replacing it with a *trailing* MA (current + prior obs only) makes the feature causal. |
| D | True | Correct: future returns may serve as training *labels* (once realized) even though they cannot be contemporaneous prediction features. |
| E | False | Wrong: later dates *can* validly serve as labels once realized — the restriction concerns availability at prediction time and evaluation separation, not any use of later dates. |

**Reference:** Look-ahead in feature construction vs. valid future labels — López de Prado (labeling, triple-barrier); trailing vs. centered windows.

### [ML-D3G6Q4] Centered z-score for mean reversion
**Scenario:** A mean-reversion feature for day t uses price(t) minus the average of days t−5…t+5, divided by that same 11-day window's σ (a centered z-score).
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Wrong: a centered mean is not a tradeable "true mean" — it relies on the future to define the present. |
| B | True | Correct: the feature for day t incorporates the actual closes of t+1…t+5, unknown when the trade must be placed → look-ahead bias. |
| C | True | Correct: this smoothing contamination yields a "perfect" indicator that looks 90%+ accurate in backtest but is impossible to execute live. |
| D | False | Wrong: using future data to remove phase lag renders the backtest fiction — a backtest must be a sequence of decisions made in "blind" time. |
| E | True | Correct: switching to a trailing window (t−10…t) for the mean and σ enforces the causal constraint. |

**Reference:** Causal (trailing) vs. centered indicators, look-ahead bias — signal-processing phase lag vs. tradeability; López de Prado (causal features).

### [ML-D3G6Q5] Gap trade priced at the same opening auction
**Scenario:** A gap-trading strategy computes "Gap %" from the official 9:30 AM opening auction print and assumes execution at that *same* opening price.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Wrong: the price is real but the sequence is not — you cannot use an auction's *result* to participate in that same auction. |
| B | True | Correct: execution look-ahead — the Gap % cannot be confirmed until the open is published, by which time the auction has already concluded. |
| C | True | Correct: using the same information for both the signal and the execution price is simultaneity bias — impossible in a live latency environment. |
| D | False | Wrong: a "zero-slippage" baseline that ignores temporal sequence is a baseline for a crystal ball, not a trading bot. |
| E | True | Correct: compute the gap from the open but execute at, e.g., the 9:30–9:35 VWAP so the signal is fully formed and knowable before capital is committed. |

**Reference:** Execution/simultaneity look-ahead bias — realistic fill assumptions; López de Prado (execution realism).

### [ML-D3G6Q6] Intraday volume feature overlapping the execution window
**Scenario:** A VWAP-participation engine sets the participation rate for the 10:00–10:30 AM block using the variance of 1-minute mid-prices from 9:45–10:15 AM — a window overlapping the block it controls.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Wrong: a feature is not a "leading indicator" if its calculation window overlaps the period during which the model is actively executing. |
| B | True | Correct: structural look-ahead — the rate for 10:00–10:15 relies on 1-minute mid-prices that have not yet occurred. |
| C | True | Correct: this overlapping-horizon infraction masks real high-frequency feature latency, creating an unearned variance reduction in the backtest. |
| D | False | Wrong: intraday variance directly drives optimal execution sizing — knowing a future volatility spike lets the backtest artificially avoid/exploit impact, inflating execution alpha. |
| E | True | Correct: truncate/shift the window to end at or before t=10:00 AM (e.g., 9:30–10:00) so the boundary information is finalized before execution logic begins. |

**Reference:** Execution-level look-ahead / overlapping windows — causal feature boundaries; market-microstructure backtest realism.

### [ML-D3G7Q1] 53%→99% from an opaque vendor feature
**Scenario:** A new alt-data "sentiment score" jumps a stock-direction model's test accuracy from 53% to 99%; the vendor won't explain construction, the PM wants to trade, and model-risk wants proof the score is available before each prediction.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | An abrupt, implausibly large accuracy jump is a reason to investigate leakage and data lineage. |
| B | False | Wrong: confidentiality does not establish causal availability or clean construction — a proprietary feature is not presumed valid. |
| C | True | Testing whether the feature timestamp precedes the trading decision helps assess deployability. |
| D | True | Comparing performance after lagging or removing the feature reveals whether its power depends on timing (contemporaneous/future info). |
| E | False | Wrong: near-perfect historical accuracy does not guarantee live accuracy — leakage, overfitting, and regime change can destroy it. |

**Reference:** "Too good to be true" diagnostics; leakage/lineage audit — Kaufman et al. "Leakage in Data Mining"; ablation/lag testing.

### [ML-D3G7Q2] Ticker alphabetical order "predicts" returns — INVERTED logic
**Scenario:** A researcher finds a stock ticker's alphabetical position strongly predicts returns in one backtest; the sponsor says correlation suffices, the research lead suspects a dataset artifact. Independent periods/universes are available. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: strong historical correlation alone does not show a stable economic relationship with returns. |
| B | False (accurate) | Correct: the ticker result may arise from selection effects, data ordering, or pure chance. |
| C | False (accurate) | Correct: replication across untouched periods and alternative universes tests the relationship's stability. |
| D | True (incorrect) | Wrong: lack of an obvious causal mechanism does NOT *prove with certainty* the feature is useless — absence of a mechanism is suggestive, not definitive. |
| E | False (accurate) | Correct: if the correlation disappears outside the discovery sample, the original result is weak evidence for deployment. |

**Reference:** Correlation vs. causation, replication/robustness testing — spurious-correlation literature; out-of-sample replication practice.

### [ML-D3G7Q3] High-importance field with post-alert timing (fraud)
**Scenario:** A fraud model leans on `review_outcome_code`, which has unusually high importance and is populated for nearly every historical fraud case; ops says the field may be written during a manual investigation that occurs *after* the alert must fire.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | High importance + unclear lineage + suspicious timing together justify a focused audit. |
| B | False | Wrong: feature importance measures predictive use within the model, not causality — it does not establish the field causes fraud. |
| C | True | Examining when the field is created relative to the prediction timestamp reveals outcome-derived leakage. |
| D | True | Running the model without the field quantifies how dependent the reported performance is on it (ablation). |
| E | False | Wrong: historical presence in the database does not establish point-in-time availability before each fraud event. |

**Reference:** Target leakage from post-outcome fields; importance ≠ causality; ablation — Kaufman et al. "Leakage in Data Mining"; scikit-learn "Permutation importance."

## References (domain-level)

1. **ISLR — *An Introduction to Statistical Learning* (James, Witten, Hastie, Tibshirani):** §2.2.2 (bias-variance, overfitting), §3.3 (interactions §3.3.2, collinearity/VIF §3.3.3), §6.1 (subset selection & why fewer features help), §6.2 (ridge & lasso — shrinkage vs. sparsity), §6.3 / §12.2 (PCA / principal-components regression), §7.1 (polynomial/basis expansion), ch.5 (cross-validation and selection-inside-CV).
2. **ESL — *The Elements of Statistical Learning* (Hastie, Tibshirani, Friedman):** §3.4 (ridge/lasso), ch.7 (model assessment, generalization), ch.14/15 (PCA, random forests & feature importance).
3. **scikit-learn User Guide:** "Common pitfalls and recommended practices — Data leakage" (fit preprocessing/selection on train only; use `Pipeline`), "Preprocessing data" (StandardScaler, MinMaxScaler, QuantileTransformer — scale-sensitivity and monotonicity), "Nearest Neighbors" (distance dependence), "Decision Trees / Random Forest" (scale-invariance), "Permutation importance with multicollinear features," "Cross-validation" / "Nested cross-validation," "Feature selection" (`SelectFromModel`, SFS).
4. **Marcos López de Prado — *Advances in Financial Machine Learning*:** point-in-time data, look-ahead bias, causal feature construction, labeling (triple-barrier), stationarity & fractional differentiation, backtest overfitting / deflated Sharpe.
5. **Hamilton — *Time Series Analysis*:** unit-root / Augmented Dickey-Fuller testing scope and limits, structural breaks, non-stationarity, state-space/Kalman filtering.
6. **Kaufman, Rosset, Perlich — "Leakage in Data Mining: Formulation, Detection, and Avoidance":** taxonomy of target leakage and detection via timing/lineage and ablation.
