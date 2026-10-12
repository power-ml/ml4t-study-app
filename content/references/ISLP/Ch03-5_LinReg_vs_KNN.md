# ISLP Section 3.5 — Comparison of Linear Regression with K-Nearest Neighbors

*Source: ISLP, PDF pages 120–124 (book pp. 111–115).*

> ML4T exam relevance: parametric vs non-parametric trade-off, KNN regression, curse of
> dimensionality — recurring exam themes. → ML Domain 4 (Linear Models) and ML Domain 3
> (Instance-based / KNN), with bias-variance framing (Domain 8).

## Parametric vs. non-parametric
- **Linear regression = parametric**: assumes a functional form for f(X) (linear). Advantages:
  easy to fit (few coefficients), interpretable coefficients, significance tests/p-values available.
  Disadvantage: strong form assumption — if the true f is far from linear, prediction is poor.
- **KNN regression = non-parametric**: no assumed form for f(X); more flexible.

## KNN regression
- For a value K and a prediction point x_0: find the K training points **N_0** closest to x_0, then
  predict the **average** of their responses:
  `f̂(x_0) = (1/K) Σ_{x_i ∈ N_0} y_i`.
- Fit is a **step function**. K=1 interpolates training data exactly (rough steps); larger K averages
  more points → smoother, less variable fit.
- **K controls the bias-variance trade-off**: small K = flexible, **low bias / high variance**
  (a region's prediction rests on one point); large K = smooth, **high bias / low variance** (averaging
  can mask real structure). Choose optimal K via test-error estimation (cross-validation, Ch. 5).

## When does each win?
- **Linear regression wins when the true f is (close to) linear** — KNN pays a variance cost with no
  offsetting bias reduction, so it is slightly inferior (esp. small K).
- **KNN wins when f is substantially non-linear** — with p=1 it can massively beat linear regression;
  as non-linearity grows, KNN test MSE barely changes while linear regression's test MSE rises sharply.

## The catch: dimensionality and the curse of dimensionality
- The KNN advantage in non-linear settings **collapses as p grows**. Example: strongly non-linear in
  one variable plus added noise predictors — KNN beats linear regression at p=1,2; mixed at p=3;
  linear regression superior at p ≥ 4. Adding dimensions barely hurt linear regression but caused a
  >10× increase in KNN's MSE.
- **Curse of dimensionality**: in high dimensions the K "nearest" neighbors can be very far from x_0
  (spreading n observations across many dimensions ≈ a reduction in effective sample size), so KNN
  predicts poorly.
- **Rule of thumb**: parametric methods tend to beat non-parametric ones when there are **few
  observations per predictor**.

## Interpretability
- Even when KNN's test MSE is slightly lower, linear regression may be preferred for
  **interpretability** — a few coefficients, with p-values, vs. an opaque local-averaging model.
