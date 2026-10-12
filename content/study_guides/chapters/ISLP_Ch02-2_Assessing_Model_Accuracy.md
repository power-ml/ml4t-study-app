# Study Guide — ISLP §2.2: Assessing Model Accuracy

*Built from the distilled ref `references/ISLP/Ch02-2_Assessing_Model_Accuracy.md` (source: ISLP PDF pages 38–49 / book pp. 28–39; covers 2.2.1 Measuring Quality of Fit, 2.2.2 Bias-Variance Trade-Off, 2.2.3 The Classification Setting) and the verified Q&A in `study_notes/ML/Domain_08_Model_Evaluation_and_Metrics.md` and `study_notes/ML/Domain_09_Overfitting_Underfitting_and_Generalization.md`.*

> Mapping note: follows the authoritative chapter→domain map in `references/INDEX.md`.

---

## 1. Key concepts to know for the exam

**Measuring quality of fit (regression):**
- **Mean Squared Error (MSE):** `MSE = (1/n) Σ_i ( y_i − f̂(x_i) )2` (Eq. 2.5). Small when predictions are close to truth.
- **Training MSE** uses the data the model was fit on; we care about **test MSE** = `Ave( y_0 − f̂(x_0) )2` on unseen (x_0, y_0) (Eq. 2.6).
- **Key pitfall:** minimizing training MSE does **not** guarantee low test MSE.
- **Flexibility vs. error:** training MSE **decreases monotonically** as flexibility rises; test MSE is **U-shaped** (falls, then rises).
- **Overfitting:** small training MSE but large test MSE — specifically, a *less flexible* model would have given smaller test MSE.
- **Degrees of freedom** summarize a curve's flexibility (linear regression = 2 df). Cross-validation (Ch. 5) estimates test MSE from training data.

**Bias-variance trade-off:**
- Expected test MSE at x_0 decomposes into **three non-negative** parts (Eq. 2.7):
  `E( y_0 − f̂(x_0) )2 = Var(f̂(x_0)) + [Bias(f̂(x_0))]² + Var(ε)` = **Variance + squared Bias + irreducible error**.
- Expected test MSE can **never** be below `Var(ε)` (irreducible error).
- **Variance** = how much f̂ changes with a different training set (↑ with flexibility). **Bias** = error from approximating complex reality with a simpler model (↓ with flexibility).
- **General rule:** as flexibility ↑, variance ↑ and bias ↓; good test performance needs *both* low.

**Classification setting:**
- **Training error rate:** `(1/n) Σ_i I(y_i ≠ ŷ_i)` (Eq. 2.8). **Test error rate:** `Ave( I(y_0 ≠ ŷ_0) )` (Eq. 2.9).
- **Bayes classifier:** assign x_0 to the class j maximizing `Pr(Y = j | X = x_0)` (Eq. 2.10); two-class: predict class 1 if `Pr(Y=1|X=x_0) > 0.5`.
- **Bayes error rate** (lowest possible test error): `1 − E( max_j Pr(Y=j|X) )` (Eq. 2.11); analogous to irreducible error, > 0 when classes overlap. An **unattainable gold standard**.
- **KNN classifier:** `Pr(Y=j|X=x_0) = (1/K) Σ_{i∈N_0} I(y_i=j)` (Eq. 2.12); predicts the majority class among the K nearest points. **1/K** is the flexibility axis — small K = flexible (low bias/high variance); large K = inflexible (high bias/low variance).

## 2. Why it matters for Exam 1

- **Maps to ML Domain 8 (Model Evaluation & Metrics)** — MSE, train vs. test error, metric definitions — **and ML Domain 9 (Overfitting, Underfitting & Generalization)** — the bias-variance decomposition and U-shaped test-error curve behind every learner.
- **Question themes:** MSE/RMSE/MAE definitions and outlier sensitivity; recognizing overfitting (near-zero training error, poor test error) vs. underfitting (both errors high and similar); bias-variance trade-off as flexibility/depth/K changes; "more capacity reduces bias while *increasing* variance (not both)."

## 3. Sample questions with correct answers (verbatim from `Domain_08` / `Domain_09`)

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

### [ML-D9G2Q1] Increasing tree depth — bias-variance (INVERTED logic)
**Scenario:** As max tree depth increases, training error falls at every step while validation error first falls then rises once the tree is deep. The team asks which claims are flawed.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Very shallow trees systematically miss useful structure — relatively high bias. The statement is correct. |
| B | False (accurate) | Very deep trees become sensitive to noise and small training-set changes — relatively high variance. Correct. |
| C | False (accurate) | Validation error better reflects the goal of performing on unseen data, so the lowest-validation depth is a better choice than lowest-training depth. Correct. |
| D | True (incorrect) | Flawed: greater capacity typically *reduces bias while increasing variance* — it does not reduce both simultaneously. |
| E | False (accurate) | Worsening validation despite improving training fit is evidence of overfitting. Correct. |
