# ML Domain 4 — Linear Models & Regression

## Domain cheat-sheet

- **Form of a linear model**: prediction = intercept + a weighted (additive) sum of feature values, `ŷ = β₀ + Σ βⱼXⱼ`. The model is defined as **linear in its coefficients (parameters)**, NOT necessarily linear in the raw features — this is the single most-tested idea in the domain.
- **Coefficient meaning & directionality**:
  - A coefficient βⱼ is the modeled change in the prediction per one-unit change in Xⱼ, **holding the other included features fixed** (a *conditional/partial/marginal* association, not a total or unconditional effect).
  - The **sign** gives the direction of the modeled association; a positive/negative sign does **not** establish causality.
  - **Magnitude is NOT importance** unless features are on a common scale. Raw coefficient size depends on the feature's units/scale; comparing coefficients across differing units (percentage points vs. basis points) or across models with different specifications is misleading.
  - **Standardizing** features (mean 0, variance 1) makes absolute coefficient magnitudes comparable as "effect per one-standard-deviation change."
  - **Rescaling** a feature forces its coefficient to rescale by the reciprocal factor; consistent rescaling of feature *and* coefficient leaves predictions unchanged (e.g., pp→bps: coefficient becomes 1/100).
- **Intercept** = the prediction when all features equal zero (for standardized features, when all features are at their sample means). It is a fitted value, not a guarantee about any future realized outcome; may lack practical meaning.
- **OLS assumptions / estimation**:
  - OLS does **not** require features to be independent/uncorrelated. A **unique** OLS solution fails only under **exact linear dependence** (perfect multicollinearity / rank-deficient design matrix).
  - **Multicollinearity** (high but imperfect correlation) inflates variance/standard errors of individual coefficients → estimates unstable, can swing or flip sign across samples — yet R², F-statistic, and *combined predictions* can stay stable. It does NOT bias coefficients and is distinct from serial correlation (which concerns residuals over time).
  - **Zero conditional mean** `E[ε|X] = 0` is what buys unbiasedness; **omitted-variable bias** arises when an omitted variable is correlated with an included predictor (the coefficient then absorbs confounded effects).
  - **Gauss–Markov / BLUE** requires linearity, exogeneity, homoscedasticity, no perfect collinearity — **normality of errors is NOT required** for BLUE (only for exact finite-sample t/F inference).
- **Capacity & polynomial expansion**:
  - Adding polynomial (X², X³…) or interaction (X₁X₂) terms increases capacity/flexibility to represent curvature and interactions while the model **stays linear in coefficients**.
  - A squared term lets the slope vary with the feature (a turning point); an interaction lets one feature's marginal effect depend on another (∂ŷ/∂X₂ = β₂ + β₃X₁).
  - **Bias–variance tradeoff**: higher degree lowers bias but raises variance; matching capacity to the true functional form (e.g., quadratic for a parabola) minimizes both. Degree 15 on noisy data overfits (wild oscillation), low OOS performance. Polynomial term count **grows fast** with the raw feature count. Raw powers of one feature are often **highly correlated** → multicollinearity; centering / orthogonal polynomials help.
- **Residuals & fit**: residual `eᵢ = yᵢ − ŷᵢ` (observed − predicted); positive residual ⇒ model underpredicted. With an intercept, OLS residuals **sum to zero** (mean ≈ 0) by construction — so a near-zero mean residual proves nothing about correct specification. **Systematic patterns** (curvature vs. fitted values ⇒ nonlinearity/omitted structure; fan shape ⇒ heteroscedasticity; sign runs over time ⇒ serial correlation; heavy tails on Q-Q ⇒ non-normal errors). **MSE** (squared) penalizes large errors far more than **MAE** (absolute), so a single outlier can dominate MSE and the two metrics can rank models differently. **R² = 0** means "explains none beyond the mean," NOT "all residuals zero" (that is R² = 1).
- **When linear models fail**: cannot represent U-shaped/non-monotone relationships with a single raw term, disconnected/clustered decision regions, or interaction effects without engineered features. Logistic regression on raw features gives a **linear decision boundary**; adding interactions/polynomials/splines can curve it. **More data does not fix high bias** from an inappropriate model class.
- **Regularization intuition**: add a coefficient penalty to the RSS objective to discourage large weights → accept higher training error for lower variance / better generalization (bias–variance tradeoff). **Ridge (L₂)** shrinks toward zero, keeps all features, shares weight among correlated ones; **Lasso (L₁)** can set coefficients exactly to zero (feature selection / sparsity) but its selection among correlated features is unstable. Larger λ ⇒ stronger penalty, less flexibility, more bias (too large ⇒ underfitting); choose λ by **cross-validation / validation set**, never by training error (which favors no penalty). A zero/near-zero coefficient does **not** prove no population relationship, and shrinkage does **not** confer causal meaning.

## Common traps

- **Inverted-logic questions (8 of 36):** the Answer Key reads "**True = incorrect; False = accurate**," so a **True** verdict means the statement is *wrong* and **False** means the statement is *correct*. Read the polarity line first. Inverted here: **G1Q3, G1Q4, G2Q2, G3Q3, G4Q1, G5Q1, G5Q2, G6Q1.**
- **Double-negative "embedded claim" choices** — the choice literally starts *"The following claim is false: [an accurate statement]."* The embedded statement is true, so asserting it is false is itself incorrect. In **normal** polarity these are keyed **False** (G5Q3A, G6Q2A, G6Q3A). In **inverted** polarity these are keyed **True (incorrect)** (G1Q3A, G3Q3A, G4Q1A). Parse the inner claim, judge its truth, then negate — and re-negate again for inverted polarity.
- **Magnitude ≠ importance; "always" is a red flag.** Choices claiming a bigger coefficient is "always more important," a term "always" reduces error/improves OOS, or added flexibility "guarantees" zero error are keyed false (or "incorrect" when inverted). Comparability requires standardized/same-scale features.
- **Multicollinearity myths.** It does NOT (a) bias coefficients, (b) violate a core OLS independence assumption, (c) force R²/F toward zero, (d) create serial correlation, or (e) get eliminated by standardizing or by adding an interaction term. It only inflates coefficient variance; a unique solution fails only under *exact* linear dependence.
- **"Still a linear model."** Adding X², X₁X₂, or other transforms keeps the model linear in coefficients — choices claiming it "is no longer a linear model" or "changes the OLS objective / creates local optima / non-convexity" are false. OLS RSS is convex.
- **In-sample fit ≠ truth.** Low training error, near-zero mean residual, or perfect training fit never proves correct specification or good generalization — always evaluate out-of-sample (time-aware for overlapping/serial data).

## Questions

### [ML-D4G1Q1] Coefficient interpretation for an investment memo
**Scenario:** An equity analyst fits a linear model predicting next-month return from earnings growth and valuation. The PM wants to turn the fitted equation into an economic story; the analyst cautions the inputs are correlated and the model is predictive, not causal.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A linear coefficient is the modeled change in prediction as earnings growth rises with the other included feature held fixed — the standard conditional interpretation. |
| B | True | The intercept is algebraically the prediction when all features equal zero, even if that point is not economically meaningful. |
| C | False | Coefficient magnitude depends on the feature's units/scale, so a larger number does not prove greater importance when features differ in units. |
| D | False | A predictive (associational) sign does not by itself establish that changing the feature *causes* the predicted change. |
| E | True | Correlated inputs allow several nearly equivalent fits that allocate weight differently, making individual coefficients less stable. |

**Reference:** OLS coefficient interpretation & correlation of predictors — ISLR ch.3 (§3.1–3.2, multiple regression, interpreting coefficients); concept "association vs. causation."

### [ML-D4G1Q2] Feature units and coefficient scaling (pp vs. bps)
**Scenario:** A futures desk models daily returns using interest-rate changes in percentage points. A developer switches the input to basis points but retrains nothing and reports the old coefficient unchanged. The risk officer asks what must change to preserve the same economic relationship.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A coefficient expresses change in prediction per unit of its feature, so changing units changes the required numerical coefficient. |
| B | True | One pp = 100 bps, so the per-basis-point coefficient must be 1/100 of the per-percentage-point coefficient for equivalent predictions. |
| C | False | Multiplying by a positive conversion factor preserves direction; the sign does not reverse. |
| D | True | Consistent rescaling of feature and coefficient leaves the product (and thus predictions) identical. |
| E | False | Comparing raw coefficients across models without checking units/definitions can be misleading. |

**Reference:** Units, scaling, and coefficient equivalence — ISLR ch.3 (§3.1, interpreting coefficients); scikit-learn `preprocessing`/`StandardScaler` docs (feature scaling).

### [ML-D4G1Q3] Model structure vs. guaranteed profit — INVERTED logic
**Scenario:** A risk team predicts a fund's daily return from market and sector returns with an intercept. The CIO sees a positive market coefficient and small positive intercept and asks whether they guarantee future profits. Flag the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Embedded claim ("the market coefficient is the modeled sensitivity conditional on the sector input") is accurate, so labeling it "false" is itself incorrect. |
| B | True (incorrect) | Wrong: a positive intercept is a fitted prediction, not a guarantee of a positive realized return when market return is zero. |
| C | False (accurate) | Correct: adding the intercept to the weighted feature values is exactly the additive form of an ordinary linear model. |
| D | False (accurate) | Correct: when all features are zero, every feature contribution vanishes and the prediction equals the intercept. |
| E | False (accurate) | Correct: an estimated relationship need not remain stable under a distribution or regime shift. |

**Reference:** Linear model structure, intercept meaning, non-stationarity — ISLR ch.3 (§3.1); concept "regime shift / parameter instability."

### [ML-D4G1Q4] Coefficient interpretation for a client thesis — INVERTED logic
**Scenario:** A quant fund builds a linear model on valuation, momentum, and quality factors. The PM asks whether coefficient signs/magnitudes can explain the thesis to clients; the risk team warns misinterpretation causes unintended tilts. Flag the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a positive momentum coefficient means higher momentum is associated with higher predicted return, holding other factors fixed. |
| B | False (accurate) | Correct: a −0.8 valuation coefficient means a one-unit increase lowers the prediction by 0.8, other predictors held constant. |
| C | False (accurate) | Correct: the intercept is the predicted return when all predictors equal zero; economic meaning depends on scaling/context. |
| D | True (incorrect) | Wrong: magnitudes cannot generally be compared directly (different units/scales), so a coefficient of 2.0 is not "always" more economically important than 0.5. |
| E | False (accurate) | Correct: opposite signs indicate opposite directional associations after accounting for the other variables. |

**Reference:** Multiple-regression coefficient interpretation & scale — ISLR ch.3 (§3.1–3.2); concept "standardization for comparability."

### [ML-D4G1Q5] Standardized coefficients and "most important signal"
**Scenario:** A systematic fund ranks stocks with a cross-sectional regression on standardized momentum, value, and earnings-revision factors. The PM argues the largest coefficient must be the most important signal; the Head of Research urges nuance.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | With standardized predictors, a larger absolute coefficient corresponds to a larger prediction change per one-standard-deviation move, so magnitudes become comparable. |
| B | False | Coefficients commonly shift when a correlated predictor is added; that does not mean the original estimate was "incorrect" for its specification. |
| C | True | In multiple regression each coefficient measures the association with the response holding the other predictors fixed. |
| D | False | A near-zero coefficient does not prove no relationship — the effect may be nonlinear, captured by correlated predictors, or masked by noise. |
| E | True | An interpretable coefficient describes a statistical association, not necessarily a causal economic mechanism. |

**Reference:** Standardized coefficients, omitted/added-variable effects — ISLR ch.3 (§3.2–3.3); ESL ch.3 (subset/coefficient behavior).

### [ML-D4G1Q6] Interpreting a fitted standardized OLS equation
**Scenario:** A team standardizes three fundamentals (earnings yield X₁, debt-to-equity X₂, 3-month volatility X₃) and fits OLS: ŷ = 0.02 + 0.045X₁ − 0.012X₂ − 0.038X₃. They evaluate interpretations of structure and coefficients.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Standardized features have mean zero, so at the sample means X₁=X₂=X₃=0 and the prediction equals the intercept, 0.02 (2%). |
| B | False | The −0.012 coefficient is a conditional association holding other features fixed, not an unconditional or causal effect of debt-to-equity. |
| C | True | Standardization puts features on a common scale, so \|0.045\| > \|0.038\| > \|0.012\| ranks estimated per-SD effects: X₁ then X₃ then X₂. |
| D | True | With no interaction terms the marginal effect of X₁ is constant, so a one-SD increase changes the prediction by +0.045 at every value of X₃. |
| E | False | High correlation inflates coefficient variance but does not necessarily break uniqueness; only *exact* linear dependence (perfect multicollinearity) prevents a unique OLS solution. |

**Reference:** Standardized OLS interpretation, additive marginal effects, multicollinearity vs. rank deficiency — ISLR ch.3 (§3.2, §3.3.3); concept "perfect multicollinearity."

### [ML-D4G2Q1] Linearity assumption and curvature (natural-gas demand)
**Scenario:** A commodities fund predicts natural-gas demand from temperature. Residuals suggest demand barely moves on mild days but rises rapidly in extreme cold; the PM wants to keep a straight line for explainability. The research lead assesses the cost of that simplification.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | An untransformed single-feature linear model has a constant slope — a fixed marginal change per unit of temperature. |
| B | True | Systematic curvature in residuals is evidence the linear form is misspecified (missing part of the relationship). |
| C | False | High in-sample correlation can coexist with important unmodeled nonlinear structure, so it does not guarantee a linear form is appropriate everywhere. |
| D | True | A nonlinear transformation (e.g., a polynomial term) can represent curvature while keeping the model linear in its coefficients. |
| E | False | Interpretability aids explanation but does not ensure adequate capacity; a simple model can still underfit. |

**Reference:** Linearity assumption, residual diagnostics, transformations — ISLR ch.3 (§3.3.3, non-linearity of the response-predictor relationships).

### [ML-D4G2Q2] Multicollinearity and dropping a small-coefficient feature — INVERTED logic
**Scenario:** A credit team predicts bond spreads from leverage and debt-to-equity, which are closely related; two retraining runs give similar predictions but different individual coefficients. The PM wants to drop whichever feature has the smaller coefficient as "unimportant." Flag the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: strongly related inputs make it hard to uniquely assign effects, so individual estimates can be unstable. |
| B | False (accurate) | Correct: compensating weight shifts across correlated features can leave the combined contribution (and predictions) similar. |
| C | True (incorrect) | Wrong: a small coefficient does not mean no predictive information — scale, redundancy, and other variables all affect coefficient size. |
| D | False (accurate) | Correct: out-of-sample comparison tests whether dropping a redundant feature preserves generalization. |
| E | True (incorrect) | Wrong: linear regression does not require every feature pair to have exactly zero correlation; correlation is allowed. |

**Reference:** Multicollinearity, coefficient instability, feature selection by validation — ISLR ch.3 (§3.3.3, collinearity); ch.6 (subset selection).

### [ML-D4G2Q3] Overlapping windows and independence of observations
**Scenario:** A stat-arb team fits a return model to overlapping five-day observations. A junior analyst treats each row as independent and reports very precise coefficients; the risk manager notes adjacent targets share trading days.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Overlapping windows reuse some of the same underlying returns, creating dependence between neighboring observations. |
| B | True | Treating dependent rows as independent overstates the effective (independent) information in the sample, inflating apparent precision. |
| C | False | Dependence affects inference and evaluation but does not make every fitted prediction numerically wrong. |
| D | True | A time-aware validation design respects how the data arise better than assuming randomly shuffled, exchangeable rows. |
| E | False | Redundant overlapping rows provide less new information than an equal number of independent periods. |

**Reference:** Independence assumption, autocorrelation, time-aware validation — ISLR ch.3 (§3.3.3, correlation of error terms); ch.5 (validation); concept "overlapping-sample bias."

### [ML-D4G2Q4] High feature correlation on the yield curve
**Scenario:** An analyst fits OLS predicting next-day index return from changes in the 10-year (X₁) and 2-year (X₂) Treasury yields, which move together with r = 0.92. Evaluate how the high correlation affects assumptions, stability, and prediction.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | OLS does not require independent/uncorrelated features; high-but-imperfect correlation does not bias estimates or invalidate OLS — only exact linear dependence breaks uniqueness. |
| B | True | Multicollinearity inflates the variance/standard errors of individual coefficients, so small sample changes can move them substantially or flip signs. |
| C | False | R² and the F-statistic can stay high when correlated features are collectively predictive, even though individual coefficients are imprecise. |
| D | False | Multicollinearity concerns relationships among features; serial correlation concerns residuals over time — the former does not automatically create the latter. |
| E | True | Individual coefficients can be unstable while combined predictions stay reliable for new data drawn from the same joint distribution/correlation structure. |

**Reference:** Multicollinearity effects, variance inflation, serial correlation distinction — ISLR ch.3 (§3.3.3, collinearity and VIF); concept "prediction vs. inference under collinearity."

### [ML-D4G2Q5] OLS assumptions and multicollinearity misconceptions
**Scenario:** A quant fund stress-tests a return model with correlated valuation, momentum, and liquidity predictors. A junior analyst says "if residuals look small the assumptions are fine"; the risk team notes correlated predictors and possible omitted macro variables.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The zero-conditional-mean condition E[ε\|X] = 0 is required for unbiased OLS estimates; violation (e.g., correlation with an omitted variable) biases coefficients. |
| B | False | A near-zero residual mean is a built-in property of OLS with an intercept and does not imply correct functional form or absence of misspecification. |
| C | True | Multicollinearity inflates coefficient variance, making estimates unstable and sensitive to small data changes even if prediction is unaffected. |
| D | False | Standardization rescales variables but leaves correlations unchanged, so it does not address multicollinearity. |
| E | False | Nonlinear/interaction terms can raise variance and overfitting risk, so OOS performance depends on the bias-variance tradeoff, not a guaranteed improvement. |

**Reference:** Zero conditional mean, omitted-variable bias, multicollinearity, standardization — ISLR ch.3 (§3.2–3.3); ESL ch.3 (regularization vs. scaling).

### [ML-D4G2Q6] Residual patterns, low training error, and omitted variables
**Scenario:** A systematic fund deploys a cross-sectional return model on momentum, value, and volatility factors. The PM insists low training error means the true structure is captured; a risk analyst flags predictors from overlapping financial statements with hidden dependencies.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Under correct specification residuals should look like noise with no systematic pattern against fitted values; visible patterns suggest misspecification. |
| B | False | Low training error can reflect overfitting/in-sample fit and does not imply the true data-generating process was captured. |
| C | True | With correlated predictors, individual coefficients can vary substantially across samples even when overall predictive performance is stable. |
| D | False | Linearity violations can degrade both interpretability and predictive performance, especially when the true relationship is strongly nonlinear. |
| E | True | Omitted variables correlated with included predictors cause coefficients to reflect confounded (direct + omitted) effects. |

**Reference:** Residual diagnostics, overfitting, omitted-variable confounding — ISLR ch.3 (§3.3.3); ch.2 (assessing model accuracy).

### [ML-D4G3Q1] Adding a squared feature (market-impact model)
**Scenario:** A market-impact model predicts execution cost from order size; a straight line misses the steepening cost of large orders, so the desk considers adding squared order size. The head trader wants better fit without a fragile production model.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A squared term makes the prediction quadratic, so its derivative (slope) varies with order size. |
| B | True | The expanded model is still linear in its coefficients — they enter as an additive weighted combination of features. |
| C | False | Extra capacity can fit training noise and does not guarantee lower error on every future sample. |
| D | True | Time-ordered held-out testing measures whether the added term generalizes under realistic deployment. |
| E | False | A degree-2 polynomial is flexible but still a restricted functional form; it cannot represent every possible relationship. |

**Reference:** Polynomial regression, linear-in-coefficients, generalization testing — ISLR ch.3 (§3.3.2, polynomial regression); ch.7 (§7.1).

### [ML-D4G3Q2] Choosing polynomial degree by validation
**Scenario:** A researcher fits polynomials of degrees 1–15 to a small volatility/returns history. Training error falls at every degree, but validation error improves only through degree 3 then rises sharply. The PM asks which pattern should drive selection.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A higher-degree polynomial nests the lower-degree ones and can fit extra variation, so training error falls as degree rises. |
| B | True | Better training fit paired with worse validation error after degree 3 is a classic overfitting signal. |
| C | False | Lowest training error rewards capacity even when it fits noise, so degree 15 should not be selected on that basis. |
| D | True | If both training and validation errors are materially worse at degree 1, the straight line is underfitting (lacking useful flexibility). |
| E | False | Repeatedly tuning on the final test set contaminates it and no longer gives an unbiased performance estimate. |

**Reference:** Model selection, validation curves, test-set hygiene — ISLR ch.5 (cross-validation); ch.2 (bias-variance / U-shaped test error).

### [ML-D4G3Q3] Polynomial expansion dimensionality and overfitting — INVERTED logic
**Scenario:** A 40-feature global equity model may add every pairwise product and several powers; the researcher argues expansion is cheaper than more data. Governance worries about limited history and instability. Flag the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Embedded claim ("polynomial expansion can increase candidate terms rapidly as feature count grows") is accurate, so labeling it "false" is itself incorrect. |
| B | False (accurate) | Correct: product terms let one feature's modeled effect depend on another, capturing interactions an additive model misses. |
| C | True (incorrect) | Wrong: more terms do not always reduce both bias and variance — greater capacity typically lowers bias but raises variance. |
| D | False (accurate) | Correct: many adjustable terms relative to limited data increase overfitting risk. |
| E | False (accurate) | Correct: regularization or disciplined feature construction can control the added capacity. |

**Reference:** Curse of dimensionality, interactions, regularization — ISLR ch.3 (§3.3.2, interactions), ch.6 (regularization); ESL ch.5 (basis expansions).

### [ML-D4G3Q4] Bias-variance across polynomial degrees (volatility smile)
**Scenario:** A researcher models a parabola-shaped implied-volatility smile from moneyness using Model A (degree 1), Model B (degree 2), and Model C (degree 15), each fit by OLS. Evaluate capacity, degree, and the bias-variance tradeoff.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A straight line cannot fit a parabola — it forces a constant slope, producing systematic underfitting (high bias) on both training and validation data. |
| B | False | Degree 15 drives training error down but inflates variance; OOS error rises as it overfits the sample's noise — no guaranteed reduction. |
| C | True | Degree 2 matches the true quadratic data-generating process, capturing signal without absorbing noise → low bias and low variance. |
| D | True | Degree 15's excess capacity lets unregularized OLS chase idiosyncratic noise, producing wild oscillation between points and poor generalization. |
| E | False | Raw powers of the same feature can be highly correlated (multicollinearity), especially uncentered; higher degree does not inherently reduce multicollinearity — centering/orthogonal polynomials do. |

**Reference:** Bias-variance tradeoff, polynomial capacity, multicollinearity of raw powers — ISLR ch.2 (§2.2), ch.3 (§3.3.2); ESL ch.5 (orthogonal polynomials).

### [ML-D4G3Q5] Fourth-degree expansion — statistical consequences (slippage)
**Scenario:** An analyst models slippage (bps) from order size (%ADV), believes it is roughly quadratic, but applies a fourth-degree expansion (X, X², X³, X⁴) fit by OLS on 10,000 trades. Evaluate the statistical consequences.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Raw powers of one feature can be highly correlated (especially uncentered/limited range), inflating coefficient variances/standard errors and making estimates unstable and hard to interpret. |
| B | False | Polynomial expansion changes the feature matrix, not the objective — OLS still minimizes the sum of squared residuals. |
| C | True | Cubic/quartic terms exceed the true quadratic form: they may slightly cut bias but raise estimation variance, increasing the risk of fitting noise/outliers. |
| D | False | Polynomial expansion creates powers of the feature, not a CDF transform; it neither removes sensitivity to extremes nor protects against regime change. |
| E | False | Added flexibility guarantees neither zero training error nor any particular OOS error; financial data are noisy and extra terms may fit non-generalizing idiosyncrasies. |

**Reference:** Multicollinearity of polynomial terms, OLS objective, overfitting — ISLR ch.3 (§3.3.2–3.3.3); scikit-learn `PolynomialFeatures` docs.

### [ML-D4G3Q6] Polynomial features, capacity, and "still a linear model"
**Scenario:** A quant fund adds polynomial transforms of momentum (M², M³) to a cross-sectional linear model to capture nonlinearity. The PM worries about overfitting/instability for portfolio construction; the risk team wants OOS justification.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Polynomial expansion increases capacity, letting linear regression represent nonlinear relationships via the transformed input space. |
| B | False | Lower training error does not guarantee better OOS performance, especially for high-capacity models prone to overfitting. |
| C | True | Increasing degree typically lowers bias but raises variance — the fundamental bias-variance tradeoff. |
| D | False | Polynomial regression is still linear *in the parameters*, so it remains a linear model in the statistical sense even though it is nonlinear in the raw features. |
| E | False | Strong in-sample fit does not imply the true data-generating process was captured; it may reflect overfitting to noise. |

**Reference:** Linear-in-parameters definition, capacity, bias-variance — ISLR ch.3 (§3.3.2), ch.2 (§2.2); ESL ch.5.

### [ML-D4G4Q1] Residual sign and pattern interpretation (currency desk) — INVERTED logic
**Scenario:** A currency desk defines each residual as actual minus predicted return. The PM sees large positive residuals around central-bank announcements and asks whether sign and pattern matter. Flag the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Embedded claim ("a positive residual means realized return exceeded the prediction") is accurate under actual−predicted, so labeling it "false" is itself incorrect. |
| B | False (accurate) | Correct: a zero residual means the observed and predicted values matched exactly for that observation. |
| C | False (accurate) | Correct: large residuals clustered around announcements suggest omitted event-related structure (non-random errors). |
| D | True (incorrect) | Wrong: useful models retain irreducible and estimation error; residuals need not all equal zero. |
| E | False (accurate) | Correct: averaging signed residuals can hide large positive and negative misses that cancel. |

**Reference:** Residual definition and diagnostics — ISLR ch.3 (§3.3.3); concept "signed vs. absolute error, error cancellation."

### [ML-D4G4Q2] Heteroscedasticity — fan-shaped residuals (risk model)
**Scenario:** A risk model predicts daily portfolio losses; its residual plot is narrow for small predicted losses but fans out as predicted loss grows. The CRO worries a single headline error number understates uncertainty when exposure is greatest.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A fan shape indicates residual variability changes with the prediction level — non-constant error variance (heteroscedasticity). |
| B | False | A near-zero mean residual is a different property from constant variance; it does not prove homoscedasticity. |
| C | True | Wider residuals in the high-loss region imply less reliable point predictions there. |
| D | True | Inspecting residuals by prediction range reveals behavior hidden by one aggregate error metric. |
| E | False | Changing error variance does not determine coefficient signs. |

**Reference:** Heteroscedasticity, residual-vs-fitted diagnostics — ISLR ch.3 (§3.3.3, non-constant variance of error terms).

### [ML-D4G4Q3] MAE vs. squared error and outlier sensitivity (fund flows)
**Scenario:** Two models forecast monthly fund flows: Model A has many small errors and one extreme miss; Model B has larger typical errors but no catastrophic miss. The client is especially sensitive to large failures and asks the team to compare MAE and squared-error measures.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Squaring residuals gives unusually large errors more relative weight than absolute error does. |
| B | False | Because MSE and MAE weight large errors differently, they can rank the two models differently. |
| C | True | Model A's single extreme miss contributes its squared magnitude and can dominate its MSE. |
| D | True | The chosen metric should reflect the client's relative cost of ordinary vs. extreme misses. |
| E | False | Lower training error under a metric does not guarantee lower future error under that metric (generalization is not assured). |

**Reference:** MAE vs. MSE, outlier sensitivity, loss selection — ISLR ch.2 (§2.2, MSE); scikit-learn "Metrics and scoring" (regression metrics).

### [ML-D4G4Q4] Residuals and fit fundamentals
**Scenario:** A systematic fund reviews a return model for portfolio construction. The PM focuses on explained return variation; the Head of Quant reviews diagnostic plots; the risk team warns regime changes may make historical fit statistics misleading.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A residual is the observed return minus the model-predicted return for each observation (eᵢ = yᵢ − ŷᵢ). |
| B | False | Low training error does not guarantee structureless residuals; systematic patterns can persist under misspecification even with small in-sample error. |
| C | True | Systematic patterns (e.g., curvature vs. fitted values) can indicate misspecification such as nonlinearity or omitted variables. |
| D | True | With an intercept, OLS residuals sum to exactly zero in-sample by the first-order optimality conditions. |
| E | False | Smaller in-sample residuals may reflect overfitting and do not always translate to better OOS trading performance. |

**Reference:** Residual definition, residual sum-to-zero, diagnostics — ISLR ch.3 (§3.1, §3.3.3).

### [ML-D4G4Q5] Residual definition, R², and serial correlation
**Scenario:** A data scientist fits OLS to predict a trend-following portfolio's Sharpe ratio from microstructure features, computes residuals eᵢ = yᵢ − ŷᵢ, and examines diagnostic plots. Evaluate interpretations of residuals and patterns.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A residual is the signed vertical distance between the observed target and the fitted value — the part of that observation the model did not explain. |
| B | False | A U-shaped/parabolic residual pattern signals *unmodeled* nonlinear structure, not a well-captured relationship; it suggests adding a transformation. |
| C | False | OLS minimizes the sum of *squared* residuals, not absolute residuals; the intercept's first-order condition is what forces the residual mean to zero. |
| D | True | Long runs of same-sign residuals plotted chronologically indicate serial correlation (autocorrelation) in the errors. |
| E | False | R² = 0 means the model explains none of the variation beyond the sample mean, not that every residual is zero (that would be R² = 1). |

**Reference:** Residuals, OLS objective, serial correlation, R² interpretation — ISLR ch.3 (§3.1, §3.3.3).

### [ML-D4G4Q6] Heavy-tailed residuals, Q-Q plots, and BLUE
**Scenario:** A macro researcher's EUR/USD volatility model has E[ε\|X] = 0 and constant variance, but the residual histogram and Normal Q-Q plot show symmetric, heavy-tailed (leptokurtic) errors deviating from the 45° line at both extremes. Diagnose implications for the linear framework.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Points curving away from the 45° reference line at both ends show the residuals have heavier tails than a normal distribution — a violation of the normality assumption. |
| B | True | Unbiasedness rests on E[ε\|X] = 0, not normality, so heavy tails alone do not bias the coefficients (though they raise sensitivity to extremes). |
| C | False | Gauss-Markov requires linearity, exogeneity, homoscedasticity, and no perfect collinearity — not normality; OLS remains BLUE without normal errors (normality is only for exact finite-sample testing). |
| D | True | Heavy-tailed errors invalidate the finite-sample formulas behind t-statistics and confidence intervals, so inference (significance) becomes unreliable. |
| E | False | Adding an interaction term changes functional form, not the noise distribution; fat tails call for robust regression (e.g., Huber) or a Student-t error model. |

**Reference:** Error-distribution diagnostics, Gauss-Markov / BLUE, robust regression — ISLR ch.3 (§3.3.3); ESL ch.3; concept "Q-Q plot / leptokurtosis."

### [ML-D4G5Q1] U-shaped relationship and a single feature — INVERTED logic
**Scenario:** A volatility desk finds both unusually low and unusually high volatility precede positive returns, while moderate volatility does not; a single raw volatility term predicts a monotonic relationship and keeps missing both extremes. Flag the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: one straight-line slope cannot turn direction across the range, so a single raw feature cannot represent a U-shape. |
| B | False (accurate) | Correct: a squared volatility term permits curvature and a turning point. |
| C | True (incorrect) | Wrong: the intercept only shifts the line vertically; changing it cannot make a line curve upward at both extremes. |
| D | False (accurate) | Correct: a model can have low overall error yet fail systematically in economically important regions. |
| E | False (accurate) | Correct: a repeated structured residual pattern is a reason to reconsider feature representation or model family. |

**Reference:** Non-monotone relationships, polynomial terms, localized failure — ISLR ch.3 (§3.3.2–3.3.3); ch.7 (basis functions).

### [ML-D4G5Q2] Interaction terms for a size-dependent effect — INVERTED logic
**Scenario:** A merger-arb team believes deal size matters differently when regulatory risk is high, but its additive model includes deal size and regulatory risk separately with no interaction. The head of trading asks whether that equation can express a size effect whose direction changes with regulatory risk. Flag the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: without an interaction, the additive slope on deal size is constant at every regulatory-risk value. |
| B | False (accurate) | Correct: a deal-size × regulatory-risk product lets the modeled size effect depend on regulatory risk. |
| C | True (incorrect) | Wrong: including both raw variables separately is not equivalent to including their product; additive effects cannot reproduce a multiplicative term. |
| D | False (accurate) | Correct: an added interaction may capture signal or noise, so generalization must be tested out-of-sample. |
| E | True (incorrect) | Wrong: the product can be treated as another feature with its own coefficient, so the model stays linear in coefficients. |

**Reference:** Interaction terms, linear-in-coefficients, additivity assumption — ISLR ch.3 (§3.3.2, removing the additive assumption).

### [ML-D4G5Q3] Linear decision boundary vs. clustered profitable regions
**Scenario:** A lending desk reframes a return forecast as approve/reject; profitable observations form two separated clusters around an unprofitable center in feature space. A manager proposes one linear scoring boundary for speed and transparency.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded claim ("a single linear boundary divides the feature space into two half-spaces") is accurate — a linear rule separates with a hyperplane — so calling it "false" is itself false. |
| B | True | Two disconnected profitable regions can require a nonlinear representation that one linear boundary cannot capture. |
| C | False | More data cannot remove a structural limitation of the chosen hypothesis space (a misspecified linear boundary). |
| D | True | Engineered nonlinear features or a more flexible model family can produce a boundary better matched to the geometry. |
| E | True | Operational simplicity can still justify a linear model if the performance tradeoff (latency, stability, governance) is understood and acceptable. |

**Reference:** Linear separability, hyperplane boundaries, feature engineering — ISLR ch.4 (§4.3, logistic regression boundary), ch.9 (§9.1, hyperplanes).

### [ML-D4G5Q4] Logistic regression's linear boundary and interactions (downgrade risk)
**Scenario:** A team fits logistic regression to predict bond-rating downgrades from interest coverage (X₁) and leverage (X₂). Risk rises sharply only when coverage is very low *and* leverage very high, but the two-feature model fits poorly. Diagnose the limits and fixes.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The sigmoid makes probability nonlinear in the linear predictor, but at any fixed threshold the boundary β₀+β₁X₁+β₂X₂ = const is a straight line in (X₁,X₂) — so raw-feature logistic regression cannot draw a curved boundary. |
| B | True | Without an interaction the log-odds are additive: the effect of X₁ is always β₁ regardless of X₂, so the model cannot express the compounding "low coverage dangerous only when leverage is high" effect. |
| C | False | The logistic negative log-likelihood is convex, so there are no multiple local optima to trap optimization; the poor fit is inadequate feature specification, not a local-optimum problem. |
| D | True | Adding X₁X₂ keeps the model linear in coefficients while letting each ratio's effect on log-odds depend on the other, producing a nonlinear boundary in the original space. |
| E | False | Logistic regression is linear in the *expanded* features, so suitable polynomial/interaction/spline/RBF transforms can separate complex patterns — though richer expansions raise cost, variance, and overfitting risk. |

**Reference:** Logistic regression boundary, interactions, convex likelihood, feature maps — ISLR ch.4 (§4.3), ch.3 (§3.3.2); ESL ch.4.

### [ML-D4G5Q5] Size-dependent momentum and the interaction term
**Scenario:** A PM predicts cross-sectional returns from log market cap (X₁) and momentum (X₂) with an additive OLS model, hypothesizing momentum helps small caps but hurts large caps. OOS testing shows the additive model misses this size-dependent effect.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | In the additive model ∂ŷ/∂X₂ = β₂ is constant across all X₁, so it can estimate only one common momentum slope and cannot flip sign with company size. |
| B | False | OLS minimizes a convex quadratic RSS, so a missing interaction produces a poorly specified model, not local minima; the solution is still the global minimum (unique if the design has full column rank). |
| C | True | Adding X₁X₂ gives ∂ŷ/∂X₂ = β₂ + β₃X₁, letting the momentum slope vary with size and cross zero within the observed range. |
| D | False | The expanded model is still linear regression (linear in β₀…β₃); the interaction makes it nonadditive/nonlinear in the original space but OLS still fits a linear combination of feature columns. |
| E | False | Adding an interaction does not eliminate multicollinearity — the product can itself be correlated with its components; centering may reduce it but neither guarantees stable estimates. |

**Reference:** Interaction terms, marginal effects, convex OLS objective, multicollinearity — ISLR ch.3 (§3.3.2–3.3.3).

### [ML-D4G5Q6] Nonlinearity, and why more data won't fix bias
**Scenario:** A researcher's linear model predicts next-day returns well in calm markets but consistently misses sharp reversals in volatile periods. The PM asks whether collecting more data will solve it or whether the approach itself is limited.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | If the true relationship is highly nonlinear, a linear model shows systematic (bias) errors regardless of dataset size. |
| B | False | Standard linear regression models only additive effects; interactions must be explicitly engineered (e.g., X₁X₂) before they can be learned. |
| C | True | A clearly curved residual pattern indicates unmodeled nonlinear structure. |
| D | False | More data reduces estimation variance but cannot overcome high bias from an inappropriate model class — an underpowered linear model stays systematically biased. |
| E | True | Polynomial and interaction features increase expressive power while keeping the model linear in its coefficients. |

**Reference:** Bias from misspecification, additivity, capacity via feature engineering — ISLR ch.2 (§2.2, bias-variance), ch.3 (§3.3.2–3.3.3).

### [ML-D4G6Q1] Regularization for stability (correlated signals, little data) — INVERTED logic
**Scenario:** A factor model has hundreds of correlated signals but only a few years of data; it fits with very low training error using large offsetting coefficients, yet small sample changes produce very different positions. The risk committee asks whether regularization could stabilize it. Flag the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a coefficient penalty makes extreme weights costlier, discouraging reliance on very large coefficients. |
| B | False (accurate) | Correct: constraining coefficients can raise training error while improving OOS performance (accept bias, cut variance). |
| C | True (incorrect) | Wrong: shrinkage does not turn predictive associations into causal effects, so it guarantees no causal interpretation. |
| D | False (accurate) | Correct: large offsetting coefficients on correlated features are a sign of an unstable fit. |
| E | False (accurate) | Correct: regularization strength should be chosen by out-of-sample validation, not training error (which favors weaker constraints). |

**Reference:** Regularization (Ridge/Lasso), bias-variance, validation for λ — ISLR ch.6 (§6.2, shrinkage methods).

### [ML-D4G6Q2] Regularization path and choosing penalty strength
**Scenario:** A team compares an unregularized regression with increasingly constrained versions: as the penalty strengthens, coefficients shrink and training error rises while validation error first falls then rises. The PM concludes the strongest penalty must be safest.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded claim ("the initial validation improvement is consistent with reducing overfitting") is accurate — moderate shrinkage cuts sensitivity to noise — so calling it "false" is itself false. |
| B | True | The later validation deterioration can indicate underfitting from excessive shrinkage suppressing genuine structure. |
| C | False | The strongest penalty is not always optimal; an over-constrained model can be stable but uninformative. |
| D | True | Regularization trades data fit against coefficient size/complexity — that tradeoff is the whole point. |
| E | True | The penalty with the lowest validation error is more defensible than the one with the smallest training error, which favors overfitting. |

**Reference:** Regularization tuning, validation curves, bias-variance — ISLR ch.6 (§6.2); ch.5 (cross-validation).

### [ML-D4G6Q3] Ridge vs. Lasso sparsity and the meaning of a zero coefficient
**Scenario:** A fund adds many weak, redundant predictors; one proposal uses a penalty that smoothly shrinks coefficients, another favors a sparse solution driving some to zero. The governance lead wants a smaller model but won't assume any penalty identifies the true economic signals.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded claim ("different penalties can produce different coefficient and feature-retention behavior") is accurate — penalty shape governs how weight is distributed/removed — so calling it "false" is itself false. |
| B | True | A penalty that can produce exactly-zero coefficients (Lasso) supports a sparser deployed model. |
| C | False | A zero regularized coefficient does not prove no population relationship — it depends on sample, penalty strength, scaling, and competing predictors. |
| D | True | With strongly correlated predictors, which feature is retained can be sensitive to the sample (redundant variables substitute for one another). |
| E | True | Sparsity, predictive performance, and stability are distinct criteria to evaluate separately, not treat as identical. |

**Reference:** Lasso sparsity vs. Ridge shrinkage, selection instability — ISLR ch.6 (§6.2, the lasso, comparison with ridge).

### [ML-D4G6Q4] Ridge/Lasso mechanics and tradeoffs
**Scenario:** A team predicts weekly returns from 150 correlated indicators with few samples; unregularized OLS gives large, unstable coefficients. They consider Ridge and Lasso with standardized predictors. Evaluate the mechanics and tradeoffs.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Ridge and Lasso add a coefficient penalty to the RSS, accepting worse training fit for lower estimation variance and potentially better OOS performance. |
| B | False | Ridge uses the L₂ penalty (Σβⱼ²) and shrinks toward zero without zeroing coefficients; it is Lasso's L₁ penalty that performs feature selection. |
| C | True | With similar-information predictors, Ridge distributes weight across the correlated group while Lasso may keep some and zero others. |
| D | True | Larger λ strengthens the penalty, reducing flexibility/variance and raising bias, so λ should be chosen by validation/cross-validation, not training error. |
| E | True | Lasso can produce a sparse model when the true signal is sparse, but its selected variables can be unstable across samples when predictors are highly correlated. |

**Reference:** Ridge (L₂) vs. Lasso (L₁), penalty form, λ selection — ISLR ch.6 (§6.2); scikit-learn `linear_model` (`Ridge`, `Lasso`) docs.

### [ML-D4G6Q5] Regularization to reduce overfitting
**Scenario:** A quant fund's model with hundreds of indicators fits training data exceptionally well but is inconsistent on unseen market data. The CRO asks whether constraining the model could improve reliability even if it slightly reduces training accuracy.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Regularization adds a penalty that discourages large coefficients, reducing complexity and helping prevent overfitting. |
| B | False | Regularization typically *increases* training error relative to unregularized OLS (though it may lower test error). |
| C | True | Accepting a small rise in training error can cut variance and improve OOS performance — the bias-variance tradeoff. |
| D | False | Regularization reduces effective complexity by constraining coefficients; it does not increase flexibility. |
| E | True | With many noisy or weakly predictive features, regularization reduces their influence and improves generalization. |

**Reference:** Regularization purpose, bias-variance, generalization — ISLR ch.6 (§6.2); ch.2 (§2.2).

### [ML-D4G6Q6] Regularization, underfitting, and the bias-variance balance
**Scenario:** A model forecasting weekly growth-stock returns nearly memorizes the training set after dozens of added indicators but is highly unstable on new data. The PM asks whether intentionally limiting flexibility yields more reliable decisions.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Regularization penalizes large coefficients during training, encouraging simpler models less prone to overfitting. |
| B | False | If a model is already underfitting, stronger regularization increases bias and worsens both training and test performance. |
| C | True | Limiting coefficient magnitudes makes the model less sensitive to small training-data changes, improving stability/generalization. |
| D | False | The lowest training error often signals overfitting; the goal is generalization, not perfect in-sample fit. |
| E | True | Choosing the regularization amount balances bias and variance — too little overfits, too much underfits. |

**Reference:** Regularization strength, bias-variance tradeoff, generalization — ISLR ch.6 (§6.2); ch.2 (§2.2).

## References (domain-level)

1. **ISLR — *An Introduction to Statistical Learning* (James, Witten, Hastie, Tibshirani):** ch.3 (Linear Regression) — §3.1 simple regression, intercept, residual sum-to-zero; §3.2 multiple regression and coefficient interpretation; §3.3.2 extensions (polynomial regression, interaction terms, removing the additive assumption); §3.3.3 potential problems (non-linearity, correlation of errors, non-constant variance, outliers, collinearity/VIF). ch.4 (§4.3, logistic regression and its linear decision boundary). ch.6 (§6.2, Ridge and Lasso shrinkage). ch.2 (§2.2, bias-variance tradeoff, MSE). ch.5 (cross-validation for tuning).
2. **ESL — *The Elements of Statistical Learning* (Hastie, Tibshirani, Friedman):** ch.3 (linear methods, subset selection, ridge/lasso, Gauss-Markov / BLUE), ch.5 (basis expansions and orthogonal polynomials), ch.7 (model assessment, bias-variance).
3. **scikit-learn User Guide — `linear_model`:** `LinearRegression` (OLS), `Ridge` (L₂), `Lasso` (L₁), `ElasticNet`; `preprocessing.StandardScaler` and `PolynomialFeatures` (standardization and polynomial expansion); "Metrics and scoring" (MSE vs. MAE, regression metrics).
4. **OLS assumptions & concepts:** linearity, zero conditional mean E[ε\|X]=0 (unbiasedness), homoscedasticity, no perfect multicollinearity, independence of errors; Gauss-Markov theorem / BLUE (normality not required); omitted-variable bias; multicollinearity vs. serial correlation; Q-Q plots and residual diagnostics.
5. **Regularization & robustness:** Ridge/Lasso bias-variance mechanics, sparsity and selection instability under correlated features; robust regression (Huber loss) and Student-t error models for heavy-tailed residuals.
