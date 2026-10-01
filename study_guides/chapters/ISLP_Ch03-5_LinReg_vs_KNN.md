# Study Guide — ISLP §3.5: Linear Regression vs. K-Nearest Neighbors

*Built from the distilled ref `references/ISLP/Ch03-5_LinReg_vs_KNN.md` (source: ISLP PDF pages 120–124 / book pp. 111–115) and the verified Q&A in `study_notes/ML/Domain_05_Instance_Based_Learning_KNN.md` (with linear-model framing from `Domain_04`).*

> Mapping note: follows the authoritative chapter→domain map in `references/INDEX.md` (ML Domains 4 and 5).

---

## 1. Key concepts to know for the exam

**Parametric vs. non-parametric:**
- **Linear regression = parametric:** assumes a functional form (linear). Pros: easy to fit (few coefficients), interpretable, significance tests/p-values available. Con: strong form assumption — poor if true f is far from linear.
- **KNN regression = non-parametric:** no assumed form for f(X); more flexible.

**KNN regression:**
- For K and prediction point x_0: find the K nearest training points **N_0**, predict the **average** of their responses: `f̂(x_0) = (1/K) Σ_{x_i ∈ N_0} y_i`.
- Fit is a **step function**. K=1 interpolates training data exactly (rough); larger K averages more → smoother, less variable.
- **K controls the bias-variance trade-off:** small K = flexible, **low bias / high variance**; large K = smooth, **high bias / low variance**. Pick optimal K via cross-validation (Ch. 5).

**When each wins:**
- **Linear regression wins when true f is (close to) linear** — KNN pays a variance cost with no offsetting bias reduction.
- **KNN wins when f is substantially non-linear** — with p=1 it can massively beat linear regression.

**Curse of dimensionality:**
- KNN's advantage **collapses as p grows**: with noise predictors, KNN beats LR at p=1,2; mixed at p=3; LR superior at p ≥ 4 (a >10× increase in KNN MSE as dimensions were added).
- In high dimensions the K "nearest" neighbors can be very far from x_0 (spreading n points across many dimensions ≈ reduced effective sample size) → KNN predicts poorly.
- **Rule of thumb:** parametric methods tend to beat non-parametric ones when there are **few observations per predictor**.
- **Interpretability:** even when KNN's test MSE is slightly lower, LR may be preferred for its few, significance-tested coefficients vs. an opaque local-averaging model.

> Distance-metric practicality (reinforced in Domain_05): KNN relies on distances, so **feature scaling** (e.g., z-score from *training* statistics) is critical — an unscaled large-range feature dominates Euclidean distance.

## 2. Why it matters for Exam 1

- **Maps to ML Domain 4 (Linear Models & Regression) and ML Domain 5 (Instance-Based Learning / KNN)**, with bias-variance framing (Domain 9).
- **Question themes:** parametric vs. non-parametric trade-off; KNN feature scaling and distance dominance; K as the flexibility/bias-variance knob (k=1 high variance vs. large k high bias); curse of dimensionality / few-observations-per-predictor rule.

## 3. Sample questions with correct answers (verbatim from `Domain_05`)

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

### [ML-D5G2Q1] k=1 vs k=75 variance/bias (INVERTED logic)
**Scenario:** KNN regressors predict five-day returns: k=1 gives near-zero training error but predictions swing when a few training points change; k=75 is stable but misses recurring local patterns. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: heavy dependence on individual observations = high variance for k=1. |
| B | False (accurate) | Correct: averaging over more neighbors smooths the fitted function. |
| C | False (accurate) | Correct: excessive averaging (k=75) can suppress real local structure → more bias than k=1. |
| D | True (incorrect) | Wrong: the k minimizing *training* error (very small k) can generalize poorly; it is not necessarily best. |
| E | False (accurate) | Correct: k is a hyperparameter, selected on validation data before final test evaluation. |
