# Ch. 2.1 — The Rules of Probability

**Source:** Bishop & Bishop, *Deep Learning: Foundations and Concepts* (Springer, 2024).
**Book pages 23–31** (PDF pages 43–51). Ch. 2 intro pp. 23–24; §2.1 The Rules of Probability pp. 25–31.

> **→ ML4T Exam-1 relevance: ML Domain 1/2 (probabilistic foundations), Bayes' theorem, conditional probability, and the base-rate reasoning behind classifier evaluation.**

---

## 1. Two kinds of uncertainty (Ch. 2 intro)
- **Epistemic (systematic) uncertainty:** from having only a *finite* data set. Reduced by observing more data.
- **Aleatoric (intrinsic / stochastic) uncertainty = noise:** persists even with infinite data; arises from observing only partial information. Reduced by gathering *different kinds* of data (e.g., biopsy vs. image alone).
- Both handled by **probability theory**, governed by two rules: the **sum rule** and the **product rule**.

## 2. Two views of probability
- **Frequentist:** probability = frequency of a repeatable event in the limit of infinite trials (e.g., a bent coin landing concave-up 60% of the time).
- **Bayesian:** probability = quantification of uncertainty; more general — includes frequentist as a special case (e.g., which unseen side is "heads" is unknown, not repeatable).

---

## 3. Sum and product rules (§2.1.2) — **exam-critical**

For random variables X (values x_i) and Y (values y_j), from counting cells n_ij out of N trials:
- **Joint probability:** $p(X=x_i, Y=y_j) = n_{ij}/N$
- **Marginal probability:** $p(X=x_i) = c_i/N$; probabilities sum to 1.
- **Conditional probability:** $p(Y=y_j \mid X=x_i) = n_{ij}/c_i$

**Compact form of the two fundamental rules:**
$$\textbf{Sum rule:}\quad p(X) = \sum_{Y} p(X, Y) \tag{2.8}$$
$$\textbf{Product rule:}\quad p(X, Y) = p(Y \mid X)\, p(X) \tag{2.9}$$
- **Marginalization** = summing out the other variable(s) to get p(X).

## 4. Bayes' theorem (§2.1.3) — **exam-critical**
From the product rule + symmetry p(X,Y) = p(Y,X):
$$p(Y \mid X) = \frac{p(X \mid Y)\, p(Y)}{p(X)} \tag{2.10}, \qquad p(X) = \sum_Y p(X \mid Y)\, p(Y) \tag{2.11}$$
- The denominator p(X) is the **normalization constant** ensuring the posterior sums to 1.
- Relates a conditional to its "reversed" conditional.

## 5. Prior vs. posterior (§2.1.5) — **exam-critical**
- **Prior probability p(C):** belief *before* observing evidence.
- **Posterior probability p(C | T):** belief *after* observing evidence T, computed via Bayes' theorem.

## 6. Independence (§2.1.6)
- X and Y independent ⟺ joint factorizes: $p(X, Y) = p(X)\,p(Y)$, equivalently $p(Y \mid X) = p(Y)$.

---

## Worked example — medical screening (base rates) — **exam-critical**
Given: prevalence p(C=1)=0.01; test sensitivity p(T=1|C=1)=0.90; false-positive p(T=1|C=0)=0.03.
- **Overall positive rate (sum + product rules):**
  $p(T{=}1) = 0.03 \times 0.99 + 0.90 \times 0.01 = 0.0387$ (~4%).
- **Posterior via Bayes:**
  $p(C{=}1 \mid T{=}1) = \dfrac{0.90 \times 0.01}{0.0387} = \dfrac{90}{387} \approx 0.23$ (23%).
- **Lesson:** even an "accurate" test yields only 23% posterior because the **prior (base rate) is low** — strong evidence must be combined with the prior. This is the base-rate fallacy that underlies precision/recall intuition.
