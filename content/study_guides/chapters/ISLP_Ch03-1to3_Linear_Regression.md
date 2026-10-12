# Study Guide — ISLP §3.1–3.3: Linear Regression

*Built from the distilled ref `references/ISLP/Ch03-1to3_Linear_Regression.md` (source: ISLP PDF pages 80–119 / book pp. 71–110; 3.1 Simple LR, 3.2 Multiple LR, 3.3 Other Considerations) and the verified Q&A in `study_notes/ML/Domain_04_Linear_Models_and_Regression.md`.*

> Mapping note: follows the authoritative chapter→domain map in `references/INDEX.md`.

---

## 1. Key concepts to know for the exam

**Simple linear regression (one predictor):**
- **Model:** `Y ≈ β₀ + β₁ X`; prediction `ŷ = β̂₀ + β̂₁ x`. β₀ = intercept, β₁ = slope.
- **Residual:** `e_i = y_i − ŷ_i`; **RSS = Σ e_i2** (Eq. 3.3).
- **Least squares estimates** (minimize RSS, Eq. 3.4): `β̂₁ = Σ(x_i−x̄)(y_i−ȳ) / Σ(x_i−x̄)²`, `β̂₀ = ȳ − β̂₁ x̄`.
- **Standard errors** (Eq. 3.8): `SE(β̂₁)² = σ²/Σ(x_i−x̄)²`, `SE(β̂₀)² = σ²[1/n + x̄²/Σ(x_i−x̄)²]`, σ² = Var(ε). Least squares estimates are **unbiased**.
- **Residual standard error:** `RSE = √(RSS/(n−2))` estimates σ.
- **95% CI** ≈ `β̂₁ ± 2·SE(β̂₁)` (Eq. 3.9). **t-statistic** `t = β̂₁ / SE(β̂₁)` (Eq. 3.14); small **p-value** → reject H0: β₁ = 0.
- **R² statistic** (Eq. 3.17): `R² = (TSS − RSS)/TSS = 1 − RSS/TSS`, **TSS = Σ(y_i−ȳ)²**; proportion of variance explained, in [0,1]. In simple regression **R² = r²** (Eq. 3.18).

**Multiple linear regression (p predictors):**
- **Model** (Eq. 3.19): `Y = β₀ + β₁X₁ + ... + βpXp + ε`. βj = avg effect of a 1-unit rise in Xj **holding all other predictors fixed**.
- Simple ≠ multiple coefficients when predictors are correlated (surrogate/confounding effects).
- **F-statistic** (Eq. 3.23): `F = [(TSS−RSS)/p] / [RSS/(n−p−1)]`; F ≈ 1 under H0, F ≫ 1 → at least one predictor useful. F adjusts for p where individual t-tests do not.
- Variable selection: forward / backward / mixed selection; criteria Cp, AIC, BIC, adjusted R².
- **R² always rises when adding any predictor** → don't compare different-size models by raw R². `RSE = √(RSS/(n−p−1))` (Eq. 3.25) can increase with more predictors.
- **Confidence interval** (average response) vs. **prediction interval** (individual Y) — the prediction interval is **always wider** (adds irreducible error).

**Other considerations (3.3):**
- **Qualitative predictors:** two levels → one dummy (0/1); >2 levels → (#levels−1) dummies, one baseline.
- **Interaction terms** `β₃·X₁·X₂` remove additivity; **hierarchical principle** — keep main effects if you keep the interaction. **Polynomial regression** (X, X², ...) removes linearity but is still linear in coefficients.
- **Six potential problems:** (1) non-linearity (residual plots); (2) **correlated error terms** (common in time series → understated SEs); (3) heteroscedasticity (funnel shape → transform Y / weighted LS); (4) outliers (studentized residual |·|>3); (5) high-leverage points (leverage h_i, Eq. 3.37); (6) **collinearity** (inflates SE(β̂j); detect via correlation matrix or **VIF = 1/(1 − R2_{Xj|X−j})**, VIF ≥ 5–10 problematic).

## 2. Why it matters for Exam 1

- **Maps to ML Domain 4 (Linear Models & Regression)** — the canonical parametric supervised learner — with model-evaluation framing (R², RSE, F-test).
- **Question themes:** coefficient interpretation ("holding others fixed"; magnitude depends on units/scale; association ≠ causation); units/scaling of coefficients; the linearity assumption and residual curvature; correlated/overlapping observations violating the independence assumption; multicollinearity and coefficient instability.

## 3. Sample questions with correct answers (verbatim from `Domain_04`)

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
