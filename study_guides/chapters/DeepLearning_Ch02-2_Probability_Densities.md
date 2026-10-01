# Study Guide — Deep Learning (Bishop) §2.2: Probability Densities

**Source ref:** `references/DeepLearning/Ch02-2_Probability_Densities.md`
**Book pages:** Bishop & Bishop, *Deep Learning: Foundations and Concepts* (Springer, 2024), **pp. 32–35** (PDF pp. 52–55). §2.2 Densities; §2.2.1 Example distributions; §2.2.2 Expectations & covariances. (§2.3 Gaussian begins p. 36 — out of scope.)
**Week:** 2 (recommended, Exam-1 scope).

---

## 1. Key concepts (must-know)

**Probability density (§2.2) — exam-critical**
- For a **continuous** variable the probability of any exact value ≈ 0, so use a density p(x): P(x in (x, x+δx)) ≈ p(x)δx.
- Interval probability: $p(x \in (a,b)) = \int_a^b p(x)\, dx$ (2.23).
- **Validity:** $p(x) \ge 0$ (2.24) and $\int_{-\infty}^{\infty} p(x)\, dx = 1$ (2.25).
- **CDF:** $P(z) = \int_{-\infty}^{z} p(x)\, dx$ (2.26), with $P'(x) = p(x)$.
- Sum/product rules and Bayes carry over with integrals: $p(x) = \int p(x,y)\,dy$ (2.29); $p(x,y)=p(y\mid x)p(x)$ (2.30); Bayes (2.31)–(2.32).

**Example distributions (§2.2.1)**
- Constant density over R can't normalize → **improper**. **Uniform** $1/(d-c)$ (2.33); **Exponential** $\lambda e^{-\lambda x}$ (2.34); **Laplace** $\tfrac{1}{2\gamma}e^{-|x-\mu|/\gamma}$ (2.35); **Dirac delta** (2.36); **empirical** $\tfrac{1}{N}\sum_n \delta(x-x_n)$ (2.37).

**Expectations & covariances (§2.2.2) — exam-critical**
- **Expectation:** discrete $\mathbb{E}[f] = \sum_x p(x) f(x)$ (2.38); continuous $\int p(x) f(x)\,dx$ (2.39).
- **Monte Carlo / sample estimate:** $\mathbb{E}[f] \approx \tfrac{1}{N}\sum_n f(x_n)$ (2.40) — exact as N→∞.
- **Variance:** $\text{var}[f] = \mathbb{E}[f(x)^2] - \mathbb{E}[f(x)]^2$ (2.44–2.45); $\text{var}[x] = \mathbb{E}[x^2] - \mathbb{E}[x]^2$ (2.46).
- **Covariance:** $\text{cov}[x,y] = \mathbb{E}[xy] - \mathbb{E}[x]\mathbb{E}[y]$ (2.47).
- **Independence ⟹ covariance = 0.** For vectors, covariance is a matrix (2.48). (Directly relevant to portfolio variance / diversification.)

---

## 2. Why it matters for Exam 1

**Mapped domains (per `references/INDEX.md`):** **ML Domain 2** (continuous distributions) and **QF Domain 1 / Domain 2** — expectation, variance, covariance are the statistical machinery behind returns, risk, and portfolio math.

Question themes:
- QF D1: expected value, arithmetic vs. geometric mean, returns as probability-weighted averages.
- QF D2: variance/σ as dispersion ($\mathbb{E}[x^2]-\mathbb{E}[x]^2$), outlier sensitivity of squaring, covariance's role in co-movement/diversification.

---

## 3. Sample questions (verbatim from mapped-domain verdict tables)

### [QF-D2G1Q1] Same average return, different dispersion
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Every A observation equals its mean, so each deviation is 0 → variance = mean of squared deviations = 0. A perfectly constant series has zero historical variance. |
| C | False | Equal *arithmetic means* say nothing about spread; two series with the same mean can have any variance. Equal average ≠ equal σ. |
| D | True | Variance is in squared-return units; σ = √variance restores the original return units — the reason σ is the more interpretable risk figure. |

*(Source: `study_notes/QF/Domain_02_Risk_and_Risk_Adjusted_Performance.md`. Maps to Bishop Eq. 2.44–2.46 var[x] = E[x2] − E[x]2.)*

### [QF-D1G3Q1] Arithmetic vs geometric mean with a +30% / −20% pair
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|---|---|---|
| A. The arithmetic average return is 5%. | True | (30% + (−20%))/2 = **5%**. |
| C. The geometric average is **not** ≈1.98% per year. | False | Embedded double negative: geometric mean = √(1.04) − 1 ≈ **1.98%**. So it *is* ≈1.98%; negation reverses → False. |
| E. The arithmetic average overstates the annualized compound growth achieved. | True | 5% arithmetic > 1.98% geometric — the classic volatility-drag gap. |

*(Source: `study_notes/QF/Domain_01_Investment_Returns_and_Compounding.md`. Expectation as probability-weighted average, Bishop Eq. 2.38–2.39.)*

### [ML-D2G2Q4] Extreme P/E outliers pulling the OLS line
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Extreme P/E points far from the predictor mean are high-leverage outliers that disproportionately influence the OLS slope. |
| B | False | Keeping the outliers *and* using L2 (MSE) loss is the wrong fix — squaring errors increases the penalty for outliers, making the model even more sensitive to them. |
| C | True | Robust learners (Huber loss, SVR) are designed to limit outlier influence on the final parameters, so they are less sensitive than plain OLS. |

*(Source: `study_notes/ML/Domain_02_Data_and_Sampling_Discipline.md`. The squaring sensitivity mirrors variance's E[x2] weighting of extremes, Bishop §2.2.2.)*
