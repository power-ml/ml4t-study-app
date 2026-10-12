# ML Domain 2 — Data & Sampling Discipline

## Domain cheat-sheet

- **Missing data mechanisms** decide what is safe to do:
  - **MCAR (Missing Completely at Random)** — missingness is unrelated to any value (e.g., a random API/feed glitch). Dropping MCAR rows shrinks the sample but does **not** systematically bias it.
  - **MAR (Missing at Random)** — missingness depends on *observed* variables, not the missing value itself.
  - **MNAR (Missing Not at Random)** — missingness depends on the *unobserved value itself* (e.g., a firm stops filing *because* it defaulted; volume missing *because* liquidity evaporated). Any imputation that ignores the cause injects systematic bias. MNAR missingness is often an informative **feature** (a proxy for stress/distress/untradeability).
- **Imputation is an estimate, not a measurement.** Treating an imputed value as an observed fact discards uncertainty and distorts relationships.
  - **Mean imputation** shrinks apparent variance, blunts signal, and can hide the "signal of failure/zero-liquidity."
  - **Median imputation** is more robust to extreme observed values than the mean, but repeatedly inserting one central value still creates an artificial spike in the distribution.
  - **Zero/neutral imputation** for sentiment forces a "neutral" assumption that dampens real trending signal.
  - **Forward-fill** carries the last observation forward — reasonable for short gaps, but long fills make **stale prices look current** and conflate distinct causes (feed outage vs. no-trade).
  - Best practice: **fit imputation parameters on training data only**, then apply to test; record missingness reason/duration as metadata; use different strategies for different *types* of missingness in the same column.
- **Noise vs. outliers:** extremeness alone does **not** prove an observation is erroneous. Decide by *context and data-quality evidence* (source records, corporate actions, decimal-placement checks) and by the **model's intended use**, distinguishing a **data-integrity error** (delete/correct) from a **valid extreme / "hard truth"** (keep or manage robustly).
  - **OLS / L2 (MSE) loss is the most outlier-sensitive**: squaring residuals gives extreme points disproportionate leverage over the fitted parameters. A single large-sigma outlier under MSE can dominate many small errors.
  - **Robust methods** (Huber loss, MAE, ε-insensitive SVR) cap the influence of large residuals (linear, not squared, penalty beyond a threshold).
  - **Trees** are relatively robust to an outlier's *magnitude*: once a value is past a split threshold, its exact size doesn't move the split; larger min-leaf size further prevents isolating single points. Trees are not fully immune — outliers can still affect split selection and leaf values.
  - **High-capacity models (deep NNs)** are *more* prone to fitting/memorizing outliers, not immune; **Batch Norm does not neutralize outliers** (an extreme value skews the batch mean/variance).
  - **Winsorizing/trimming** genuine tail events understates tail severity and can create a form of survivorship bias for risk models.
- **Sampling bias & representativeness:** a sample must be a "miniature version" of the deployment population. Sample **size/volume/duration does NOT fix systematic bias**, and adding **more features does not fix a biased set of rows**.
  - **Survivorship bias** — conditioning on entities that survived to the end (current index constituents; firms still listed today) omits failures, inflating apparent performance and hiding the negative/failure class.
  - **Selection bias** — inclusion criteria correlated with the target (dividend payers, published trials → **publication bias**) skew feature/outcome distributions.
  - **Point-in-time** membership/data better reconstructs what was investable/known at each past date. Evaluation data should resemble the intended deployment population/regime; a clean split only tests transfer *within the sampled source population*.
- **Temporal structure & ordering:** financial rows are time-ordered and serially dependent (not exchangeable), so treat time as first-class.
  - **Random shuffling** before splitting places later regimes in training and earlier ones in test, ignores information-arrival direction, and destroys autocorrelation signals (momentum, moving averages). Use **chronological / walk-forward** splits (train on earlier, test on later).
  - **Look-ahead / forward-looking bias:** never let information unavailable at the decision time enter training — e.g., normalizing on the *full* dataset (global μ/σ), aligning macro data (BLS unemployment) to its *period* rather than its *release date*, or including a label whose forward window hasn't matured. Distinguish **event date** from **availability/publication date**; index by point-in-time.
  - Walk-forward preserves the arrow of time, exposes regime drift, and simulates live deployment; expanding-window folds legitimately grow the training history (folds need not be equal size). Preserving order can lower but *make more meaningful* the score.
- **Train/test separation discipline:** the test set must stay genuinely unseen. Avoiding test *labels* is **not** sufficient — **any data-dependent choice fit on test features leaks**:
  - Preprocessing (scaling, median/KNN imputation), **feature selection (RFE)**, and hyperparameter/model selection are all part of the model-development pipeline and must be fit **on training data only** (or dynamically within each walk-forward fold).
  - Combined-data standardization, global-median imputation, and KNN imputation over the full matrix (a **transductive/manifold leak** — a past row borrows a future neighbor) all contaminate the evaluation even without touching labels.
  - Retraining the winning config on the training data does **not** erase test-based selection; upstream vendor feature lists built on full history carry the same leak (provenance matters).
- **Data snooping & reuse:** repeatedly evaluating on the same held-out period and reacting to results makes that period part of development.
  - **Multiple comparisons:** screening many candidates and reporting the max (best Sharpe of 5,000 indicators) favors positive noise; in-sample ranking is not independent confirmation. The *breadth of the search* determines how surprising the winner is.
  - Leakage can occur through **human iteration and organization-wide feedback** (shared holdout scores) without ever copying labels into features. Access-controlling raw rows does not preserve independence.
  - Mitigations: a genuinely untouched final set, limited evaluation frequency, and experiment tracking (which improves transparency but cannot restore spent independence).

## Common traps

- **Inverted-logic questions (12 of 33):** the Answer Key reads "**True = incorrect; False = accurate**," so a "True" verdict means the statement is *wrong* and "False" means it is *correct*. Read the polarity line before every table. Inverted here: **G1Q2, G1Q5, G1Q6, G2Q2, G3Q2, G3Q4, G3Q5, G4Q1, G4Q4, G4Q6, G5Q3, G6Q1.**
- **Double-negative "embedded claim" choices — "The following claim is false: <accurate statement>":** the inner claim is true, so the whole statement is false/inaccurate. In inverted questions that maps to a **True (incorrect)** verdict; in normal questions to a **False** verdict. Appears in **G1Q2A** (inverted → True), **G3Q2A** (inverted → True), **G4Q2A** (normal → False), **G6Q3A** (normal → False).
- **"It is incorrect to conclude that <false statement>":** in **G4Q4A** (inverted) the embedded claim (global μ/σ gives a sound "stable reference") is itself inaccurate, so rejecting it is correct → the statement is **accurate → False**. Parse the inner claim, judge it, then apply the double negative and the polarity.
- **Size/volume never cures bias.** Many choices bait you with "the dataset is large / spans a decade / two exchanges / thousands of responses, therefore representative." A large but systematically filtered sample is still biased (G3Q1C, G3Q2, G3Q4E, G3Q5A/E, G3Q6C). Likewise **adding features cannot fix biased rows** (G3Q5E).
- **"No test labels used" ≠ clean test.** Leakage hides in preprocessing, imputation, feature selection, and human/organizational iteration (G2, G5, G6 families). Fitting *any* parameter on data that includes the held-out portion contaminates the estimate.
- **Extreme ≠ erroneous, and cleaning that lowers average error can worsen the decision.** Validity needs context, not a distance-from-mean threshold (G2Q1B/E, G2Q3E, G2Q4E). OLS/MSE is the *most* outlier-sensitive learner (recurring distractor claims it "de-weights" outliers — false).
- **Calendar alignment vs. availability.** Aligning macro/label data to the period it *covers* rather than its *release* date is look-ahead bias; shuffling does not fix a causality violation, it just spreads the corrupted signal (G4Q6E, G4Q3, G6-style reasoning).

## Questions

### [ML-D2G1Q1] Complete-case deletion and systematic missingness
**Scenario:** A quant equity team gets fundamentals where young firms lack long histories and distressed firms stop reporting fields. The PM wants to delete every row with any missing value; the research lead asks how that affects a model meant to score the full universe.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | If missingness correlates with firm characteristics (age, distress), deleting incomplete rows changes the population the sample represents — i.e., it becomes MNAR-driven selection bias, not a random thinning. |
| B | False | A large *retained* sample can still be systematically unrepresentative: dropping all young/distressed firms removes a whole segment regardless of how many rows remain. |
| C | True | The fact that a value is missing can itself be predictive — a missingness flag can encode age/distress/reporting-failure signal that a plain deletion throws away. |
| D | False | Any imputed number is an estimate carrying uncertainty; treating it as an observed measurement understates variance and can distort feature–target relationships. |
| E | True | Comparing retained vs. removed firms is exactly the diagnostic that reveals whether the deletion rule disproportionately excludes certain firm types before you adopt it. |

**Reference:** Missing-data mechanisms (MCAR/MAR/MNAR) and complete-case bias — Little & Rubin, *Statistical Analysis with Missing Data*; scikit-learn "Imputation of missing values."

### [ML-D2G1Q2] Global median imputation before the split — INVERTED logic
**Scenario:** A risk team replaces missing leverage with the median computed over the entire ten-year dataset *before* splitting into train/test, arguing median imputation is "always safe" because it ignores the target. Identify the flawed (incorrect) claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Note the embedded double-negative: the statement asserts "*The following claim is false: median imputation can be more resistant to extreme values than mean imputation.*" The inner claim is actually true (the median *is* more robust to extremes), so calling it false is itself incorrect. |
| B | False (accurate) | Correct: computing the median over the *entire* dataset lets test-period observations shape the preprocessing parameter, leaking held-out information into training. |
| C | True (incorrect) | Wrong: not using the target does not guarantee an uncontaminated evaluation — test-*feature* information (via the global median) still influences development, so the test is no longer independent. |
| D | False (accurate) | Correct: fitting the imputation value on training data and applying it to test preserves the intended separation and mimics live deployment. |
| E | False (accurate) | Correct: replacing many missing values with one median creates an artificial concentration (spike) that reduces the feature's apparent variability. |

**Reference:** Preprocessing leakage and fit-on-train discipline — scikit-learn "Common pitfalls: data leakage" and `Pipeline`/`SimpleImputer`; median vs. mean robustness (basic robust statistics).

### [ML-D2G1Q3] Forward-fill for two different missingness causes
**Scenario:** A desk merges multi-vendor prices where a gap can mean a feed outage *or* an illiquid no-trade. The head trader wants every gap forward-filled to keep a complete matrix; the team must decide if one rule fits both causes.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Forward-filling substitutes the last observed value until a new observation arrives — that is precisely the assumption it encodes. |
| B | False | A feed outage (a data-system failure) and a no-trade interval (a liquidity condition) carry different economic meaning; treating them identically conflates them. |
| C | True | Long forward-filled stretches make a stale price look current, masking that no fresh price was actually observed. |
| D | True | Recording the duration/reason of missingness preserves information a single filled value would erase, letting the model distinguish stale from genuine data. |
| E | False | The missingness mechanism governs whether an imputation rule is defensible and how to interpret results, so it cannot be ignored once gaps are filled. |

**Reference:** Time-series imputation pitfalls (stale-quote/forward-fill) and missingness metadata — de Prado, *Advances in Financial Machine Learning* (data structures); general data-cleaning practice.

### [ML-D2G1Q4] Missing volume during liquidity crunches (MNAR)
**Scenario:** A researcher finds small-cap "Daily Trading Volume" is missing mainly during extreme-volatility periods when liquidity evaporates, and must judge how to treat it.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | It is **not** MAR: the volume is missing *because* the (unobserved) volume was effectively zero/untradeable — the missingness depends on the value itself, which is MNAR. |
| B | True | Mean imputation of volume artificially reduces variance and erases the "zero-liquidity" signal, so the model underestimates risk. |
| C | False | Complete-case deletion drops exactly the volatile stress periods, creating survivorship-style bias — the model never learns crisis behavior it most needs. |
| D | True | Missingness that coincides with liquidity crunches is itself an informative feature: a null in a liquidity field flags untradeability, valuable to a risk model. |
| E | True | When data is MNAR, any imputation that does not model the *cause* of missingness introduces systematic bias into the backtest. |

**Reference:** MNAR / informative missingness and missing-indicator features — Little & Rubin; scikit-learn `MissingIndicator`.

### [ML-D2G1Q5] Two causes of missing Interest Coverage Ratio — INVERTED logic
**Scenario:** In 5,000 distressed-debt firms, 15% of Interest Coverage Ratios are missing: 10% from firms that defaulted and stopped filing, 5% from a data-provider API error. Mark each statement True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: an API glitch is unrelated to firm performance, so those 5% are MCAR; dropping them only reduces sample size without skewing results. |
| B | False (accurate) | Correct: the 10% from defaulted firms is MNAR — missingness is directly tied to the firms' poor financial health (a selection effect of bankruptcy). |
| C | True (incorrect) | Wrong: deleting the defaulted firms creates survivorship bias, so the model learns only "successful distressed debt" and massively overestimates expected returns. |
| D | False (accurate) | Correct: imputing a sector average for a firm with zero earnings and high debt hides the failure signal, blinding the model to the very risk it should manage. |
| E | False (accurate) | Correct: rigorous practice uses different strategies per missingness type — impute the API gaps, but treat defaulted-firm gaps as a distinct category or distressed "floor" value. |

**Reference:** Distinguishing MCAR/MNAR within one column; survivorship bias — Little & Rubin; de Prado (backtest pitfalls). Note: source labels B's mechanism a "Selection Effect" rather than naming MNAR, but the accurate/inaccurate verdict is preserved.

### [ML-D2G1Q6] Zero vs. mean imputation for intraday sentiment — INVERTED logic
**Scenario:** Intraday sentiment is missing for hours during the Asian session. The researcher weighs zero (neutral) imputation vs. mean imputation over the whole 5-year training set. Mark each statement True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: forcing a neutral 0 dampens the signal and makes the model less reactive to genuine overnight sentiment shifts — a conservative bias. |
| B | True (incorrect) | Wrong: mean imputation is *not* superior — it blunts the signal and ignores the temporal context, typically hurting live performance. |
| C | False (accurate) | Correct: a mean computed from the full dataset uses information from the future relative to early-year gaps, i.e., look-ahead bias. |
| D | False (accurate) | Correct: filling crash-period gaps with neutral/average scores means the model never learns the association between missing data and extreme losses, understating drawdown risk. |
| E | False (accurate) | Correct: deleting the missing hours destroys time-series continuity, producing a fragmented, unrealistic backtest. |

**Reference:** Look-ahead bias from global statistics; imputation and signal attenuation — de Prado (backtest overfitting); scikit-learn data-leakage guidance.

### [ML-D2G2Q1] Suspected fat-finger price of $9,800 near $98
**Scenario:** A pipeline records $9,800 between observations near $98. Ops wants the row removed immediately; the PM notes genuine jumps can also look extreme; the research team investigates before editing the training set.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Cross-checking source records and corporate-action data (splits/dividends) is how you separate a bad record from a legitimate event. |
| B | False | Not every statistically extreme point is an error; deleting all of them blindly discards valid rare events. |
| C | True | If it is a decimal-placement error, keeping it can distort learned relationships and statistics (especially under squared-error fitting). |
| D | True | If it reflects a real market event, removing it strips out behavior the deployed model must handle. |
| E | False | Distance from the mean alone does not establish invalidity — validity needs contextual and data-quality evidence. |

**Reference:** Outlier validation vs. blind removal; error vs. valid extreme — ISLR §3.3.3 (leverage/outliers); data-cleaning best practice.

### [ML-D2G2Q2] Do outliers hit regression and trees identically? — INVERTED logic
**Scenario:** A group compares linear regression vs. a tree for transaction-cost estimation; a few trades have huge costs. A junior analyst claims outliers must affect both learners identically since both see the same rows. Mark each statement True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: least-squares squares the residuals, so large residuals exert disproportionate influence on the fit. |
| B | True (incorrect) | Wrong: a tree is *not* immune to outliers — they can affect split selection, leaf predictions, and stability. |
| C | False (accurate) | Correct: different model families have different structures/fitting criteria and therefore different outlier sensitivities. |
| D | False (accurate) | Correct: increasing minimum leaf size prevents very small groups (single unusual points) from being modeled on their own, reducing isolation of an outlier. |
| E | True (incorrect) | Wrong: lower *training* error from removing high-cost trades is not automatic justification — you must first determine if they are errors or valid, and evaluate out of sample. |

**Reference:** Squared-error sensitivity vs. tree robustness; min-leaf regularization — ISLR §3 (OLS) and ch.8 (trees); ESL ch.9.

### [ML-D2G2Q3] Winsorizing shock days for a risk model
**Scenario:** A volatility model does well on normal days but poorly during shocks. The PM calls shock days "noise" and wants every extreme return winsorized; the risk officer says those days matter most. Intended use is risk control in normal *and* stressed markets.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Whether to retain shock observations depends partly on intended use — a risk-control model must handle exactly those conditions. |
| B | False | Rarity alone does not make an observation noise; rare events can be valid and economically important. |
| C | True | Winsorization caps extreme values, so it can understate the true severity of genuine tail events. |
| D | True | Evaluating separately in ordinary vs. stressed regimes exposes the tradeoff that a single average metric would hide. |
| E | False | Lower *average* error does not necessarily mean more usefulness for risk control — it may come at the cost of worse behavior in the most consequential periods. |

**Reference:** Winsorization/tail treatment and segment-wise evaluation — de Prado (fat tails, backtest evaluation); robust-statistics tradeoffs.

### [ML-D2G2Q4] Extreme P/E outliers pulling the OLS line
**Scenario:** Training linear regression to predict tech-stock P/E, a few penny stocks with near-zero earnings produce P/E > 5,000 (sector average 30), dragging the regression line and hurting fit for the rest.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Extreme P/E points far from the predictor mean are high-leverage outliers that disproportionately influence the OLS slope. |
| B | False | Keeping the outliers *and* using L2 (MSE) loss is the wrong fix — squaring errors increases the penalty for outliers, making the model even more sensitive to them. |
| C | True | Robust learners (Huber loss, SVR) are designed to limit outlier influence on the final parameters, so they are less sensitive than plain OLS. |
| D | False | Even accurate outliers that don't represent the broader population can harm generalization (high variance); "accurate" does not mandate keeping them. |
| E | True | The decision hinges on whether the outlier represents the "true process" you want to model or "noise" that obscures the typical relationship — a use-dependent judgment. |

**Reference:** Leverage/influence in OLS, robust regression (Huber, SVR) — ISLR §3.3.3; ESL §6.9 / robust loss functions.

### [ML-D2G2Q5] Aggressively "cleaning" spikes in a trend-following pipeline
**Scenario:** A research lead reviews a pipeline where the analyst wants to treat rare S&P E-mini price spikes as systematic errors and handle them aggressively to keep coefficients stable.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | OLS does not "de-weight" outliers by squaring — squaring *amplifies* them, making OLS the most outlier-sensitive of these choices. |
| B | False | Trimming a *valid* market event creates survivorship bias and a model unprepared for real risk — effectively snooping for a cleaner history. |
| C | False | SVR with ε-insensitive loss is actually *robust*: it ignores errors below ε and penalizes larger ones linearly (like Huber/MAE), not by squaring. |
| D | False | Trees are relatively robust to magnitude — once a value is past a split threshold, whether it is 100 or 1,000,000 doesn't change the tree structure; trees do not use the whole column's variance to place every split. |
| E | True | Genuine extreme realizations should generally be retained or managed with robust loss (Huber), not deleted, because they carry critical fat-tail risk information. |

**Reference:** OLS vs. robust losses; ε-insensitive SVR; tree robustness to magnitude — ISLR §3, ch.8/9; ESL §12 (SVM/SVR).

### [ML-D2G2Q6] "Big NN will just learn to ignore flash crashes"
**Scenario:** A consultant audits a risk-parity fund whose researcher argues a high-capacity neural net trained on decades of data needs no manual outlier handling because it will learn to treat crashes as anomalies.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | High-capacity models are *more* prone to fitting outliers — enough flexibility to memorize an anomaly as a complex rule rather than ignore it. |
| B | True | A broken ticker ($0.01) creates a leverage effect: the network distorts its internal representation to minimize the huge loss from the error, degrading the feature space for all stocks. |
| C | False | Batch Normalization does not eliminate outlier influence — a single extreme value skews the batch mean/variance, polluting normalization for the whole batch. |
| D | True | Correct data discipline: remove/correct proven data-integrity errors, but manage genuine extreme realizations via robust optimization or clipping. |
| E | False | Because MSE squares errors, one 20-sigma outlier contributes ~400 while 1,000 separate 0.1-sigma errors contribute ~10 combined — the single extreme has far greater impact. |

**Reference:** Outlier fragility of high-capacity models; BatchNorm sensitivity; MSE quadratic weighting — ESL ch.11; Ioffe & Szegedy (Batch Normalization); loss-function robustness concept.

### [ML-D2G3Q1] Survivorship bias from current index constituents
**Scenario:** A researcher builds a stock-selection model using only firms still in the S&P 500 at the study's end, and wants the backtest to prove the strategy worked over the prior decade. A risk analyst asks about firms that left the index.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Restricting to firms that survived in the index to the end conditions the sample on survival — the textbook definition of survivorship bias. |
| B | True | Excluding firms that failed/merged/were removed drops poor outcomes, making historical performance look better than it truly was. |
| C | False | A large count of *current* constituents does not correct a systematic inclusion rule — size cannot fix a biased selection. |
| D | True | A point-in-time constituent history reconstructs the securities actually investable at each past date, avoiding the bias. |
| E | False | Survivorship bias is not limited to descriptive statistics — biased training examples change learned relationships and evaluated performance. |

**Reference:** Survivorship bias and point-in-time data — de Prado (backtesting); Grinold & Kahn (data quality); standard quant-finance practice.

### [ML-D2G3Q2] Voluntary-survey churn model — INVERTED logic
**Scenario:** A brokerage trains a churn model on a voluntary satisfaction survey where highly engaged and very dissatisfied clients respond most, but applies it to all clients. The director assumes thousands of responses make the sample representative. Mark each statement True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Embedded double-negative: the statement says "*The following claim is false: voluntary response patterns can create selection bias.*" The inner claim is true (they *can* create bias), so denying it is incorrect. |
| B | False (accurate) | Correct: more observations reduce random uncertainty but do not remove systematic sampling bias. |
| C | True (incorrect) | Wrong: high accuracy within respondents does not prove equal accuracy for nonrespondents — performance can change in underrepresented groups. |
| D | False (accurate) | Correct: comparing respondent vs. nonrespondent characteristics can reveal systematic coverage differences. |
| E | False (accurate) | Correct: reweighting only helps if you have variables that describe the relevant selection differences between sampled and target populations. |

**Reference:** Selection/self-selection (voluntary response) bias; reweighting/covariate shift — survey-sampling theory; scikit-learn "sample weighting" / dataset-shift concepts.

### [ML-D2G3Q3] Train on large-cap low-rate era, deploy on small private firms in tightening
**Scenario:** A credit fund trains a default model on large U.S. public firms from a low-rate period, then plans to score small private firms during tightening. The committee asks if a clean random holdout with strong results justifies deployment.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A clean random split estimates performance on rows drawn from the *same source population* — valid within that sampled setting. |
| B | False | It does not guarantee representative evaluation for small private firms in a different rate regime — the deployment population and environment differ. |
| C | True | Differences in size, disclosure, and macro conditions can shift both feature distributions and outcome relationships, limiting generalization. |
| D | True | Evaluation data resembling the intended deployment population provides more relevant, decision-supporting evidence. |
| E | False | A clean train/test split and population representativeness are distinct concerns; no test-row use during training does not rule out sampling bias. |

**Reference:** Dataset shift / covariate shift vs. train-test hygiene — Quiñonero-Candela et al., *Dataset Shift in Machine Learning*; ISLR ch.5 (resampling limits).

### [ML-D2G3Q4] Dividend-payer high-yield backtest — INVERTED logic
**Scenario:** A strategist backtests a high-yield dividend strategy on all US-listed dividend payers 2010–2020, and notices many top performers were small caps later acquired at a premium. Mark each statement True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Wrong: filtering to dividend payers excludes growth and non-payers, so the sample is *not* representative of the total equity market. |
| B | False (accurate) | Correct: this is selection bias — the inclusion criterion (paying a dividend) skews the distribution of features and outcomes toward value/low-volatility. |
| C | False (accurate) | Correct: if acquired winners are dropped because they no longer trade under their ticker, the backtest ignores a primary source of the strategy's historical return (survivorship bias). |
| D | True (incorrect) | Wrong: a model trained during falling rates will likely *fail* when rates rise — dividend "bond proxies" underperform, so it does not automatically generalize. |
| E | True (incorrect) | Wrong: volume and duration do not eliminate systematic bias; a sample restricted to one market slice/regime stays a prisoner of that slice. |

**Reference:** Selection vs. survivorship bias; regime dependence of dividend "bond proxies" — de Prado; Grinold & Kahn; standard factor-investing critique.

### [ML-D2G3Q5] Bankruptcy model from firms listed as of 2025 — INVERTED logic
**Scenario:** A bankruptcy model is trained on 10,000 NYSE/NASDAQ firms listed as of Dec 2025, labeled by whether they filed Chapter 11 during 2015–2025. Mark each statement True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Wrong: a snapshot of currently existing firms is a "winner's history," not a representative decade — it omits the failures needed for a balanced classification task. |
| B | False (accurate) | Correct: this is classic survivorship bias — looking backward from the present, you only see firms that survived the interval. |
| C | True (incorrect) | Wrong: NYSE/NASDAQ firms have fundamentally different risk profiles and data-generating processes than small private startups; results don't generalize without adjustment. |
| D | False (accurate) | Correct: it is selection bias where the survival filter is correlated with the target, so the training set is systematically missing the critical "bankrupt" outcomes. |
| E | True (incorrect) | Wrong: adding more features cannot fix a biased row set — if failed firms are absent, extra columns only help the model overfit the survivor bias. |

**Reference:** Survivorship + selection bias; "features can't fix biased rows" — de Prado; general sampling-bias theory.

### [ML-D2G3Q6] Clinical-trial success model from published trials
**Scenario:** A model predicts clinical-trial success trained only on trials successfully completed and published in major journals 2010–2025, to advise a VC firm on early-stage drug candidates.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Published journals are a heavy filter; the universe of *all* trials is far larger and more diverse than published successes, so the sample is not representative. |
| B | True | This is selection bias — specifically publication bias: failed/negative trials are less likely to be published, producing an overly optimistic training set. |
| C | False | Fifteen years of *published* trials cannot fix a sample skewed toward one outcome type; volume does not cure the bias. |
| D | True | The model will underestimate the true failure rate because discontinued/unpublished negative outcomes are entirely absent from the training distribution. |
| E | True | Trained on a sanitized history, the model gives false confidence — it never learned the signals preceding failure/abandonment, so it fails in production. |

**Reference:** Publication/selection bias and base-rate distortion — Ioannidis, "Why Most Published Research Findings Are False"; general survivorship/selection-bias concept.

### [ML-D2G4Q1] Random shuffle before splitting next-day returns — INVERTED logic
**Scenario:** To balance class proportions, an analyst randomly shuffles ten years of daily observations before the train/test split. The PM asks whether the resulting score reflects how the model would truly have been developed and deployed over time. Mark each statement True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a chronological split preserves the past→future sequence — it trains on earlier data and evaluates on later data, matching deployment. |
| B | False (accurate) | Correct: random shuffling can place later regimes in training and earlier ones in test, ignoring the direction in which information actually arrives. |
| C | True (incorrect) | Wrong: distinct dates per row do not make shuffling valid — dated rows still have temporal dependence and a real forecasting order. |
| D | False (accurate) | Correct: nearby-in-time financial observations can be serially dependent (overlapping signals, persistent conditions), so they are not exchangeable. |
| E | False (accurate) | Correct: preserving order can make evaluation harder yet more realistic — a genuine future period may differ from the training period and yield a lower but more meaningful estimate. |

**Reference:** Time-series cross-validation and non-exchangeability — scikit-learn `TimeSeriesSplit`; de Prado (walk-forward, purging/embargo).

### [ML-D2G4Q2] Walk-forward vs. random folds with overlapping windows
**Scenario:** A monthly model is cross-validated. An engineer proposes ordinary random folds; the director proposes walk-forward (train earlier months, test later). Several features/labels use overlapping return windows.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | The statement is "*The following claim is false: walk-forward respects the past-to-future direction.*" The inner claim is true (walk-forward predicts each period from only preceding periods), so denying it is false. |
| B | True | Random folds can put observations from both sides of a test month into its training set, breaking chronological availability. |
| C | True | Overlapping windows share underlying days, so nominally separate examples share information and appear more independent than they are (motivating purging/embargo). |
| D | False | Walk-forward folds need not be equal size — expanding-window designs legitimately use a growing training history. |
| E | True | Temporal validation should mirror when inputs and labels would actually have been available in practice. |

**Reference:** Walk-forward/purged CV, overlapping-label leakage — de Prado, *Advances in Financial ML* (ch. on cross-validation); scikit-learn `TimeSeriesSplit`.

### [ML-D2G4Q3] Including an unresolved forward label at retraining time
**Scenario:** A fund retrains each Friday to trade the next week, labeling each Friday with the return through the *next* Friday — but the training set includes the most recent Friday whose label isn't yet known. The developer says the row is "historical now," so it's fine.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The right question is whether the label was available at the simulated Friday decision time — a valid backtest reproduces historical information availability. |
| B | True | Including the unresolved forward return feeds the simulated model information it could not have had then (the return is known only later). |
| C | False | A value's presence in today's completed database does not prove it existed at every earlier training date — databases often contain later-known values. |
| D | True | The training cutoff may need to exclude observations whose label windows haven't finished; only realized labels can support that run. |
| E | False | Respecting row *dates* alone is insufficient when labels mature *after* those dates — label availability can lag the timestamp and must also be checked. |

**Reference:** Look-ahead bias from unmatured labels; point-in-time labeling — de Prado (labeling, backtest hygiene); "event date vs. availability date" concept.

### [ML-D2G4Q4] Normalizing on the full 20-year dataset — INVERTED logic
**Scenario:** A mean-reversion researcher normalizes features (RSI, Bollinger) by subtracting the mean and dividing by the std computed over the *entire* 20-year dataset before splitting. Mark each statement True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | "*It is incorrect to conclude that this preprocessing is sound because the global μ/σ give a stable reference across all regimes.*" The embedded claim (it's sound / a legitimate stable point) is itself inaccurate — a 2010 trader cannot know 2024's mean — so rejecting it is correct → the statement is accurate. |
| B | True (incorrect) | Wrong: scaling does not address temporal autocorrelation — it only changes units while leaking future information into the past. |
| C | True (incorrect) | Wrong: global-parameter normalization *ruins* generalization — the model expects a global scale it can never compute live, where the future mean is unknown. |
| D | True (incorrect) | Wrong: this *is* look-ahead bias — the global mean/variance encode future distribution info even if specific future dates weren't "seen." |
| E | False (accurate) | Correct: to avoid leakage, normalization parameters must be fit only on the training set (or a rolling window) and then applied to test. |

**Reference:** Data leakage from full-sample scaling; fit-transform on train only — scikit-learn "Common pitfalls: data leakage," `StandardScaler` in a `Pipeline`; de Prado (look-ahead bias).

### [ML-D2G4Q5] Walk-forward validation properties and limits
**Scenario:** A trend-following algo uses sliding-window walk-forward: train on 3 years, test on the 4th, shift forward 1 year, repeat.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Walk-forward preserves temporal order, ensuring the model is never tested on data chronologically preceding its training set — the finance "gold standard." |
| B | False | Shuffling days *within* the training window is harmful: features like momentum/moving averages depend on sequence, and shuffling destroys the autocorrelation the model should capture. |
| C | True | Because the model is retrained and retested moving through time, walk-forward reveals regime drift — when/why a strategy starts failing as conditions change. |
| D | False | Re-seeing historical patterns as the window slides is *not* leakage: as long as each fold's test set follows its training set chronologically, the future stays unknown at each step. |
| E | True | A practical drawback: early folds train on smaller samples (especially in expanding-window variants), so initial results are less reliable and it is data-hungry. |

**Reference:** Walk-forward validation and within-window shuffling harm — de Prado (backtesting through time); scikit-learn `TimeSeriesSplit`.

### [ML-D2G4Q6] Aligning BLS unemployment to the month it covers — INVERTED logic
**Scenario:** A regime-switching model aligns BLS monthly unemployment (e.g., January's figure) to the market close of that same month (Jan 31), even though the figure is only released in early February. Mark each statement True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Wrong: aligning by calendar month rather than release date lets the model trade on information invisible to participants at that time. |
| B | False (accurate) | Correct: this is fatal look-ahead bias — January's figure isn't known until the early-February BLS release, so using it on Jan 31 is cheating. |
| C | True (incorrect) | Wrong: even a short reporting lag is catastrophic in systematic trading — unlagged data lets the backtest "avoid" downturns perfectly, then fail live. |
| D | False (accurate) | Correct: valid time-series validation needs point-in-time data indexed by publication timestamp, not the period covered — this is a timestamp-mismatch (event vs. availability date) error. |
| E | True (incorrect) | Wrong: shuffling does not fix a causality violation — it just spreads the corrupted look-ahead signal across the dataset, guaranteeing an overfit model. |

**Reference:** Point-in-time data, publication-lag / look-ahead bias — de Prado (backtest hygiene); "event date vs. availability date"; economic-data vintages (e.g., ALFRED/real-time datasets) concept.

### [ML-D2G5Q1] Standardizing on combined train+test data
**Scenario:** A team splits into train/test, then standardizes every feature using the mean/std of the *combined* data. The analyst says the test labels were never used, so the test score is fully independent. The PM asks if preprocessing design matters.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Combined-data standardization lets the test-feature distribution influence the training pipeline — the fitted mean/std summarize held-out observations. |
| B | False | Avoiding test *labels* is not the only requirement; test *features* can also affect learned preprocessing and development choices. |
| C | True | Scaling parameters should be estimated from training data and applied unchanged to test, simulating how new post-deployment observations would be transformed. |
| D | True | Preprocessing is part of the model-development pipeline for train/test separation — data-dependent choices must be learned without the final test set. |
| E | False | Applying the same formula to every row does not undo the fact that test information was used to *estimate* the parameters. |

**Reference:** Preprocessing leakage; scale on train only — scikit-learn "Common pitfalls: data leakage," `Pipeline`; ISLR ch.5.

### [ML-D2G5Q2] Selecting among 40 configs directly on the test set
**Scenario:** A desk compares 40 model/hyperparameter combos directly on the designated test set, picks the best, and reports that score as the final estimate. The validation set went unused. Research calls it efficient since no candidate was trained on test rows.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Selecting among models by test performance makes the test set part of model development — its results drove the choice. |
| B | True | The reported maximum is optimistically biased: with many comparisons, the winner partly reflects chance variation specific to that test sample. |
| C | True | A validation set could handle model selection while the test set is reserved for a single final generalization estimate. |
| D | False | The test set is not "unseen" just because its rows didn't fit candidate parameters — viewing and acting on test scores is itself exposure. |
| E | False | Retraining the chosen config on training data does not erase test-based selection; the choice still encodes what was learned from the test set. |

**Reference:** Validation vs. test set separation; multiple-comparison optimism — ISLR ch.5–6; scikit-learn "Cross-validation" / nested CV.

### [ML-D2G5Q3] Vendor feature list built on full history — INVERTED logic
**Scenario:** A vendor supplies a preselected feature list after evaluating hundreds of candidates on the *full* dataset. Your team then makes a fresh split and fits only those features, claiming a clean test since your code never inspected the rows before splitting. Mark each statement True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: feature selection on the full dataset transmits information from future test rows into the pipeline — the list reflects relationships seen across the entire history. |
| B | True (incorrect) | Wrong: a later split does *not* remove contamination from earlier data-dependent decisions; the prior selection remains informed by the future test observations. |
| C | False (accurate) | Correct: to preserve separation, feature selection (a data-dependent step) must be redone using only the training portion. |
| D | False (accurate) | Correct: documentation of how the vendor built the list (provenance) is exactly what determines whether held-out information shaped the features. |
| E | False (accurate) | Correct: contamination can occur through development choices even when test rows never reach the final fitting function — indirect influence still compromises evaluation. |

**Reference:** Feature-selection leakage / provenance — ISLR §6 and the classic "selecting features on all data" error (ESL §7.10.2, "the wrong way to do CV"); scikit-learn data-leakage guidance.

### [ML-D2G5Q4] Global-median imputation before the split (cross-sectional equity)
**Scenario:** An analyst predicts next-day returns of 500 tech stocks; before a 70/30 split they fill missing accounting features with a *global* median over the entire 10-year dataset "to maximize sample integrity."
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Preserving the global distribution by leaking test data into training destroys out-of-sample validity — "structurally sound" is wrong. |
| B | True | This is a classic preprocessing leak: the median filling training gaps is partly computed from future test values, so the test is no longer unseen. |
| C | False | Even a non-directional summary statistic leaks variance/scale information about the future space, letting the model adapt to the test distribution prematurely. |
| D | True | It is a common splitting violation — out-of-sample information is mixed into the in-sample phase, inflating generalization metrics. |
| E | True | Correct discipline: compute the median on training data only, then apply it to impute test-set gaps. |

**Reference:** Imputation leakage; fit imputer on train — scikit-learn `SimpleImputer` in a `Pipeline`, "data leakage" pitfalls.

### [ML-D2G5Q5] KNN imputation over the full matrix, then chronological split
**Scenario:** For heavy missingness in "Annual Revenue," a researcher runs KNN imputation on the *entire* 10-year feature matrix so neighbors are most accurate, then does a chronological 80/20 split.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | The improved accuracy is "illegal" — the training phase is contaminated with data that in reality would sit in the unknown future. |
| B | True | This violates separation: a training row's imputed value can be derived from a nearest neighbor located in the future test set (a transductive leak). |
| C | False | Leakage is not limited to labels — if training features are influenced by test features, the model gains a hidden familiarity with the test distribution. |
| D | True | Using the whole dataset to define neighborhoods lets the geometry of the future warp the representation of the past — a manifold/structure leak. |
| E | True | Correct discipline: fit the KNN imputer on training data only, then use that fitted imputer to fill gaps in both train and test. |

**Reference:** Transductive/neighbor-based imputation leakage — scikit-learn `KNNImputer` fit-on-train guidance; ESL §7.10.2 (leakage through preprocessing).

### [ML-D2G5Q6] Feature selection (RFE) on the full dataset before walk-forward
**Scenario:** A developer runs Recursive Feature Elimination on the entire 5-year dataset to pick the top 10 features, then applies walk-forward validation using only those 10.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reducing dimensionality by peeking at the test set yields a "survivor" feature set tailored to a future it shouldn't know — not statistically sound. |
| B | True | This is a global information leak: the choice of which features to include was informed by the entire out-of-sample period. |
| C | False | Feature selection is part of model-building; if the selection "sees" the future, the subsequent walk-forward training is already biased toward future-relevant features. |
| D | True | It is selection bias / data snooping — the chosen features may have performed well over that specific window by chance, overstating live performance. |
| E | True | Correct discipline: perform feature selection *inside* each training fold of the walk-forward, using only data available up to that point. |

**Reference:** Feature-selection-inside-CV rule; snooping via selection — ESL §7.10.2; de Prado (backtest overfitting); scikit-learn `RFE` within a CV pipeline.

### [ML-D2G6Q1] Re-tuning weekly on the same 2018–2025 test period — INVERTED logic
**Scenario:** A team evaluates a strategy on the same 2018–2025 test period every week, changing features/holding periods/learners after each poor result until the backtest looks strong. Because test labels are never copied into training, the PM believes the final result is unbiased. Mark each statement True if incorrect.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: repeatedly modifying the strategy in response to the same test results makes that period part of development (feedback guides the design). |
| B | False (accurate) | Correct: enough iterations adapt the strategy to sample-specific noise, so the final estimate can capture chance patterns peculiar to the reused period. |
| C | True (incorrect) | Wrong: leakage is *not* impossible without label-copying — information leaks through human selection and iteration. |
| D | False (accurate) | Correct: a genuinely untouched evaluation period tests the selected design on observations that did not shape it, giving stronger evidence. |
| E | False (accurate) | Correct: experiment tracking improves transparency but cannot make previously used data unseen again. |

**Reference:** Backtest overfitting from repeated reuse; human-in-the-loop leakage — de Prado & Bailey, "The Deflated Sharpe Ratio" / "Pseudo-mathematics and financial charlatanism"; multiple-testing concept.

### [ML-D2G6Q2] Publishing the best 10 of 5,000 indicators (multiple comparisons)
**Scenario:** A fund screens 5,000 technical indicators on one historical period and publishes the ten with the best Sharpe ratios as evidence they are economically meaningful. The CIO asks whether multiple comparisons change the interpretation.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Searching many weak/useless indicators can still produce apparently strong winners by pure chance. |
| B | True | Selecting the maximum observed Sharpe favors estimates that benefited from unusually favorable sample noise (selection/winner's-curse effect). |
| C | False | Outperforming the other 4,990 on the *search* data is not independent confirmation — in-sample ranking proves nothing about persistence. |
| D | True | Testing the chosen indicators on untouched data helps separate persistent signal from selection luck. |
| E | False | The number of alternatives examined is highly relevant — the breadth of the search determines how surprising the winning values really are. |

**Reference:** Multiple-testing / data snooping and the Sharpe-ratio winner's curse — Bailey & de Prado, "Deflated Sharpe Ratio"; White's "Reality Check"; ESL §7 (multiple comparisons).

### [ML-D2G6Q3] Shared "golden" holdout across three teams
**Scenario:** Three teams use the same corporate "golden" holdout for final evaluation, share scores monthly, abandon weak ideas, and build replacements based on what worked for others. Governance still calls the period "untouched" because no one retrains on its rows.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | The statement is "*The following claim is false: org-wide feedback can cause the holdout to influence later designs.*" The inner claim is true (shared results shape which approaches the org pursues), so denying it is false. |
| B | False | A holdout does not stay independent indefinitely just because raw rows are access-controlled — repeated outcome feedback compromises independence without exposing rows. |
| C | True | Aggregate scores can reveal enough information to guide adaptation: teams learn which choices worked on that specific period and respond accordingly. |
| D | True | Limiting evaluation frequency and reserving a newer final set reduces institutional overfitting and preserves a more credible evaluation boundary. |
| E | True | Models selected through this process can have over-optimistic estimates because the selection favors approaches tailored to the repeatedly observed holdout. |

**Reference:** Institutional/adaptive overfitting of a shared holdout — Dwork et al., "The reusable holdout" (adaptive data analysis); de Prado (backtest overfitting).

## References (domain-level)

1. **de Prado — *Advances in Financial Machine Learning*:** the core reference for this domain — labeling and point-in-time data, look-ahead/forward-looking bias, purged & embargoed / walk-forward cross-validation, backtest overfitting, and fat-tail/outlier treatment in finance.
2. **ISLR — *An Introduction to Statistical Learning* (James, Witten, Hastie, Tibshirani):** ch.3 (OLS, leverage/outliers, high-influence points), ch.5 (resampling, validation vs. test set), ch.6 (feature/subset selection), ch.8–9 (trees, SVM/SVR robustness).
3. **ESL — *The Elements of Statistical Learning* (Hastie, Tibshirani, Friedman):** ch.7, esp. §7.10.2 "The Wrong and Right Way to Do Cross-Validation" (feature-selection and preprocessing leakage) and multiple-comparison bias.
4. **Little & Rubin — *Statistical Analysis with Missing Data*:** MCAR/MAR/MNAR taxonomy, bias from complete-case deletion, and principled imputation/uncertainty.
5. **scikit-learn User Guide:** "Common pitfalls and recommended practices — Data leakage," `Pipeline`, `StandardScaler`, `SimpleImputer`/`KNNImputer`/`MissingIndicator`, `TimeSeriesSplit`, and cross-validation — fit all preprocessing on training data only.
6. **Bailey, Borwein, López de Prado & Zhu / Dwork et al.:** "The Deflated Sharpe Ratio" and "The reusable holdout" — multiple-testing, selection under many comparisons, and adaptive (institutional) overfitting of held-out data.
