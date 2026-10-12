# ISLP Section 2.2 — Assessing Model Accuracy

*Source: ISLP, PDF pages 38–49 (book pp. 28–39). Covers 2.2.1 Measuring Quality of Fit,
2.2.2 Bias-Variance Trade-Off, 2.2.3 The Classification Setting.*

> ML4T exam relevance: core of model evaluation — MSE, train vs. test error, overfitting,
> bias-variance decomposition, Bayes error, KNN flexibility. → ML Domain 8 (Model Evaluation) and
> the bias-variance framing behind every learner in ML Domain 4–7.

## 2.2.1 Measuring the Quality of Fit (regression)
- **Mean Squared Error (MSE)**: `MSE = (1/n) Σ_i ( y_i − f̂(x_i) )²`  (Eq. 2.5).
  Small when predictions are close to truth.
- **Training MSE** uses the data the model was fit on. We *do not* care about it per se — we care
  about **test MSE** = `Ave( y_0 − f̂(x_0) )²` on previously unseen (x_0, y_0) (Eq. 2.6).
  - Example intuition: predicting *tomorrow's* stock price, not last week's; predicting diabetes
    for *future* patients, not the training patients.
- **Key pitfall**: minimizing training MSE does **not** guarantee low test MSE. Many methods fit
  coefficients specifically to minimize training MSE, driving it small while test MSE stays large.
- **Flexibility vs. error** (fundamental pattern, holds for any dataset/method):
  - Training MSE **decreases monotonically** as flexibility (degrees of freedom) increases.
  - Test MSE is **U-shaped**: falls, then rises.
- **Overfitting**: small training MSE but large test MSE — the method chases random patterns in
  training data that don't exist in test data. Defined specifically as: a *less flexible* model
  would have given a smaller test MSE. (Training MSE is almost always < test MSE regardless.)
- **Degrees of freedom** = a summary of a curve's flexibility (linear regression = 2 df, most
  restrictive). **Cross-validation** (Ch. 5) estimates test MSE using only training data.

## 2.2.2 The Bias-Variance Trade-Off
- The U-shape in test MSE comes from decomposing expected test MSE at a point x_0 into **three
  non-negative** parts (Eq. 2.7):
  `E( y_0 − f̂(x_0) )² = Var(f̂(x_0)) + [Bias(f̂(x_0))]² + Var(ε)`
  = **Variance + squared Bias + irreducible error**.
- Expected test MSE can **never** be below `Var(ε)` (the irreducible error).
- **Variance**: how much f̂ would change with a different training set. More flexible → higher
  variance (a wiggly curve shifts a lot if one point moves).
- **Bias**: error from approximating a complex reality with a simpler model. More flexible → lower
  bias. (Linear regression is badly biased when true f is non-linear.)
- **General rule**: as flexibility ↑, variance ↑ and bias ↓. Early on bias falls faster than
  variance rises (test MSE ↓); later variance dominates (test MSE ↑).
- **The trade-off**: good test performance needs *both* low variance and low squared bias. Easy to
  get one at the cost of the other (interpolating curve = zero bias/high variance; horizontal line
  = low variance/high bias). Finding both-low is the challenge — a recurring theme of the book.

## 2.2.3 The Classification Setting
- **Training error rate**: `(1/n) Σ_i I(y_i ≠ ŷ_i)` (Eq. 2.8) — fraction misclassified;
  `I(·)` is an indicator (1 if wrong, 0 if right).
- **Test error rate**: `Ave( I(y_0 ≠ ŷ_0) )` (Eq. 2.9). A good classifier minimizes this.
- **Bayes classifier**: assign x_0 to the **most likely class**, i.e. the class j maximizing the
  conditional probability `Pr(Y = j | X = x_0)` (Eq. 2.10). Two-class: predict class 1 if
  `Pr(Y=1|X=x_0) > 0.5`.
  - **Bayes decision boundary**: the set of points where the probability is exactly 50%.
  - **Bayes error rate** (lowest possible test error): `1 − E( max_j Pr(Y=j|X) )` (Eq. 2.11);
    at a point it is `1 − max_j Pr(Y=j|X=x_0)`. Analogous to irreducible error. > 0 when classes
    overlap (example dataset: ≈ 0.13). The Bayes classifier is an **unattainable gold standard**
    (needs the true conditional distribution, which is unknown for real data).
- **K-Nearest Neighbors (KNN) classifier**: estimates `Pr(Y=j|X=x_0) = (1/K) Σ_{i∈N_0} I(y_i=j)`
  over the K training points N_0 nearest to x_0 (Eq. 2.12); predicts the majority class among them.
  - Can get surprisingly close to the Bayes boundary (e.g., K=10 test error 0.1363 vs. Bayes 0.1304).
  - **K controls flexibility**: small K (K=1) = very flexible, low bias / high variance, jagged
    boundary, training error = 0 but high test error. Large K (K=100) = inflexible, high bias /
    low variance, near-linear boundary. **1/K** is the flexibility axis.
  - Same U-shaped test-error pattern as regression; no strong link between training and test error.

## One-line takeaways
- Choose the model that minimizes **test** error, not training error.
- The **right level of flexibility** is critical and dataset-dependent; the bias-variance trade-off
  produces the U-shaped test-error curve. Cross-validation (Ch. 5) is how you find it in practice.
