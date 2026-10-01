# ISLP Sections 3.1–3.3 — Linear Regression

*Source: ISLP, PDF pages 80–119 (book pp. 71–110). 3.1 Simple LR, 3.2 Multiple LR,
3.3 Other Considerations.*

> ML4T exam relevance: the canonical parametric supervised learner — coefficients, fit metrics,
> inference, and the assumption failures that break it. → ML Domain 4 (Linear Models) and
> ML Domain 8 (Model Evaluation: R2, RSE, F-test).

## 3.1 Simple Linear Regression  (one predictor)
- **Model**: `Y ≈ β0 + β1 X`. β0 = intercept (E[Y] at X=0), β1 = slope (avg. change in Y per
  1-unit rise in X). Prediction: `ŷ = β̂0 + β̂1 x`.
- **Residual**: `e_i = y_i − ŷ_i`. **RSS** = Σ e_i2 (Eq. 3.3).
- **Least squares estimates** (minimize RSS, Eq. 3.4):
  `β̂1 = Σ(x_i−x̄)(y_i−ȳ) / Σ(x_i−x̄)2`,  `β̂0 = ȳ − β̂1 x̄`.

### 3.1.2 Accuracy of the coefficient estimates
- **Population regression line** = true best linear approx (unobserved); **least squares line** =
  our estimate from one sample. Different samples → different lines, but least squares estimates
  are **unbiased** (average over many samples = truth).
- **Standard errors** (Eq. 3.8): `SE(β̂1)2 = σ2/Σ(x_i−x̄)2`,
  `SE(β̂0)2 = σ2[1/n + x̄2/Σ(x_i−x̄)2]`, where σ2 = Var(ε). SE(β̂1) is *smaller* when x's are more
  spread out (more leverage to estimate slope). Assumes errors uncorrelated with common variance.
- **Residual standard error** estimates σ: `RSE = √(RSS/(n−2))`.
- **95% confidence interval** ≈ `β̂1 ± 2·SE(β̂1)` (Eq. 3.9).
- **Hypothesis test**: H0: β1 = 0 (no relationship) vs Ha: β1 ≠ 0. **t-statistic**
  `t = β̂1 / SE(β̂1)` (Eq. 3.14); # of SDs β̂1 is from 0. Under H0, t ~ t-dist with n−2 df.
  **p-value** = prob. of seeing |t| this large by chance; small p → reject H0 (typical cutoffs 5%/1%).

### 3.1.3 Accuracy of the model (goodness of fit)
- **RSE** = `√(RSS/(n−2))` (Eq. 3.15) — absolute lack-of-fit, in units of Y (avg deviation from
  the regression line).
- **R2 statistic** (Eq. 3.17): `R2 = (TSS − RSS)/TSS = 1 − RSS/TSS`, where **TSS = Σ(y_i−ȳ)2**.
  Proportion of variance in Y explained by X; always in [0,1], scale-free. In *simple* regression,
  **R2 = r2** (squared correlation `Cor(X,Y)`, Eq. 3.18). What counts as "good" R2 is domain-dependent.

## 3.2 Multiple Linear Regression  (p predictors)
- **Model** (Eq. 3.19): `Y = β0 + β1X1 + β2X2 + ... + βpXp + ε`. Interpret βj = avg effect on Y of a
  1-unit rise in Xj **holding all other predictors fixed**. Fit by least squares (Eq. 3.22),
  minimizing RSS (matrix algebra; software).
- **Simple ≠ multiple coefficients**: correlated predictors change the story. Advertising example:
  `newspaper` is significant *alone* but ~0 with TV+radio in the model — it was a **surrogate** for
  radio (radio & newspaper correlated 0.35). ("Shark attacks vs. ice cream" — confounder = temperature.)

### 3.2.2 Four key questions
1. **Is at least one predictor useful?** Test H0: β1=...=βp=0 with the **F-statistic**
   `F = [(TSS−RSS)/p] / [RSS/(n−p−1)]` (Eq. 3.23). F ≈ 1 under H0; F ≫ 1 → reject.
   - F adjusts for p; individual t-p-values do **not** — with large p, ~5% of predictors look
     significant by chance, so rely on F for the global test. (For a subset of q coefficients use
     Eq. 3.24; each individual t-test equals the F-test dropping that one variable, i.e. its
     partial effect.) If **p > n**, least squares can't be fit — see Ch. 6 (forward selection).
2. **Which predictors matter? (variable selection)** 2^p possible subsets → infeasible for large p.
   Classical automated searches: **forward selection** (start null, add best-RSS variable each step;
   greedy, always usable), **backward selection** (start full, drop largest p-value; needs p<n),
   **mixed selection** (add forward, drop if p-value rises). Model-quality criteria: Mallow's Cp,
   AIC, BIC, adjusted R2 (Ch. 6).
3. **Model fit**: RSE and R2 (here **R2 = Cor(Y,Ŷ)2**). **R2 always rises when adding any
   predictor** (RSS falls on training data) → don't use raw R2 to compare models of different size;
   a tiny bump (e.g., adding newspaper) signals the variable is useless and may overfit.
   `RSE = √(RSS/(n−p−1))` (Eq. 3.25) — can *increase* with more predictors if RSS barely drops.
4. **Predictions** carry 3 uncertainties: (a) coefficient estimation error → **reducible**,
   (b) **model bias** (linearity is an approximation), (c) irreducible error ε.
   - **Confidence interval**: uncertainty about the *average* response f(X).
   - **Prediction interval**: uncertainty about an *individual* Y; **always wider** (adds
     irreducible error ε).

## 3.3 Other Considerations

### 3.3.1 Qualitative predictors
- Two levels → one **dummy/indicator variable** (0/1; a.k.a. one-hot encoding). Coding is arbitrary
  and doesn't change predictions, only coefficient interpretation.
- >2 levels → **(#levels − 1) dummies**; the omitted level is the **baseline**. Test overall effect
  with an F-test on the dummies (coding-independent).

### 3.3.2 Extensions (relaxing key assumptions)
- Standard model assumes **additive** and **linear** relationships.
- **Interaction terms** (remove additivity): add `β3·X1·X2` (Eq. 3.31). Then effect of X1 depends on
  X2. Advertising TV×radio interaction: R2 96.8% vs 89.7% → strong synergy. **Hierarchical
  principle**: if you keep an interaction, keep its main effects even if their p-values are large.
- **Polynomial regression** (remove linearity): include `X, X2, ...` as predictors (Eq. 3.36); still a
  *linear model* in the coefficients. Higher degree → risk of over-wiggly fit.

### 3.3.3 Potential problems (six)
1. **Non-linearity** — detect via **residual plots** (residuals vs fitted); a pattern (U-shape) =
   non-linear. Fix: transform predictors (log X, √X, X2).
2. **Correlated error terms** — common in **time series** (adjacent errors track). Understated SEs →
   too-narrow CIs, too-small p-values, false confidence.
3. **Non-constant error variance (heteroscedasticity)** — funnel shape in residual plot. Fix:
   transform Y (log Y, √Y) or use **weighted least squares** (weights ∝ 1/variance).
4. **Outliers** — unusual **y** given x. Use **studentized residuals**; |value| > 3 flags an outlier.
   Inflates RSE and lowers R2 even if the line barely moves.
5. **High-leverage points** — unusual **x**. Have large impact on the fit. **Leverage statistic**
   h_i (Eq. 3.37), between 1/n and 1, average = (p+1)/n; a value ≫ (p+1)/n is high leverage. Worst
   case = high leverage + outlier.
6. **Collinearity** — two+ predictors closely related. Inflates SE(β̂j), shrinks t-statistics,
   reduces power → may fail to reject H0. Detect: correlation matrix, or **VIF** (variance inflation
   factor) = `1/(1 − R2_{Xj|X−j})`; VIF ≥ 5–10 is problematic (min = 1). Fix: drop one collinear
   variable, or combine them into one.

## 3.4 Marketing plan (worked answers, Advertising data)
Relationship exists (F-test p≈0); ~90% variance explained (R2=0.897, RSE=1.69 ≈12% error); only
TV & radio matter (newspaper CI includes 0, no collinearity — VIFs ≈1); use prediction interval for
an individual, CI for the average; residual plot reveals non-linearity; TV×radio interaction shows
synergy.
