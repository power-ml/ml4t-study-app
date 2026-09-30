# Ch. 2.2 — Probability Densities

**Source:** Bishop & Bishop, *Deep Learning: Foundations and Concepts* (Springer, 2024).
**Book pages 32–35** (PDF pages 52–55). §2.2 Probability Densities; §2.2.1 Example distributions; §2.2.2 Expectations and covariances. (§2.3 Gaussian begins p. 36 — out of scope.)

> **→ ML4T Exam-1 relevance: ML Domain 2 (continuous distributions), expected value / variance / covariance — the statistical machinery behind returns, risk, and portfolio math.**

---

## 1. Probability density (§2.2) — **exam-critical**
- For a **continuous** variable the probability of any exact value is effectively zero, so we use a **probability density** p(x): probability of x in (x, x+δx) ≈ p(x)δx as δx→0.
- Probability over an interval:
$$p(x \in (a,b)) = \int_a^b p(x)\, dx \tag{2.23}$$
- **Validity conditions:**
$$p(x) \ge 0 \tag{2.24}, \qquad \int_{-\infty}^{\infty} p(x)\, dx = 1 \tag{2.25}$$
- **Cumulative distribution function (CDF):** $P(z) = \int_{-\infty}^{z} p(x)\, dx$ (2.26), with $P'(x) = p(x)$.
- **Multivariate:** joint density p(x) over vector x with p(x) ≥ 0 and ∫p(x)dx = 1 over all space.

**Sum/product rules and Bayes carry over to densities** (integrals replace sums):
$$\text{sum: } p(x) = \int p(x,y)\,dy \tag{2.29}, \quad \text{product: } p(x,y) = p(y \mid x)\,p(x) \tag{2.30}$$
$$\text{Bayes: } p(y \mid x) = \frac{p(x \mid y)\,p(y)}{p(x)} \tag{2.31}, \quad p(x) = \int p(x \mid y)\,p(y)\,dy \tag{2.32}$$

## 2. Example distributions (§2.2.1)
- A constant density can't be normalized over the real line → **improper distribution**.
- **Uniform** over (c,d): $p(x) = 1/(d-c)$ for x∈(c,d) (2.33).
- **Exponential:** $p(x \mid \lambda) = \lambda e^{-\lambda x}, \; x>0$ (2.34).
- **Laplace** (exponential with movable peak μ): $p(x \mid \mu,\gamma) = \tfrac{1}{2\gamma}\exp(-|x-\mu|/\gamma)$ (2.35).
- **Dirac delta** $\delta(x-\mu)$: zero everywhere except x=μ, integrates to 1 — an infinitely narrow, tall unit-area spike (2.36).
- **Empirical distribution:** sum of deltas on the data points, $p(x \mid \mathcal{D}) = \tfrac{1}{N}\sum_{n=1}^N \delta(x - x_n)$ (2.37).

## 3. Expectations and covariances (§2.2.2) — **exam-critical**
- **Expectation** (weighted average of f(x)):
$$\text{discrete: } \mathbb{E}[f] = \sum_x p(x) f(x) \tag{2.38}, \qquad \text{continuous: } \mathbb{E}[f] = \int p(x) f(x)\, dx \tag{2.39}$$
- **Monte Carlo / sample estimate** (exact as N→∞):
$$\mathbb{E}[f] \approx \tfrac{1}{N}\sum_{n=1}^{N} f(x_n) \tag{2.40}$$
- **Conditional expectation:** $\mathbb{E}_x[f \mid y] = \sum_x p(x \mid y) f(x)$ (2.42), integral form (2.43); it is a function of y. Subscript $\mathbb{E}_x$ marks the averaged variable.
- **Variance** (spread around the mean):
$$\text{var}[f] = \mathbb{E}[(f(x) - \mathbb{E}[f(x)])^2] = \mathbb{E}[f(x)^2] - \mathbb{E}[f(x)]^2 \tag{2.44, 2.45}$$
$$\text{var}[x] = \mathbb{E}[x^2] - \mathbb{E}[x]^2 \tag{2.46}$$
- **Covariance** (how two variables vary together):
$$\text{cov}[x,y] = \mathbb{E}_{x,y}[\{x - \mathbb{E}[x]\}\{y - \mathbb{E}[y]\}] = \mathbb{E}_{x,y}[xy] - \mathbb{E}[x]\mathbb{E}[y] \tag{2.47}$$
- **Independence ⟹ covariance = 0.** For vectors, covariance is a matrix (2.48); $\text{cov}[x] \equiv \text{cov}[x,x]$.

---

## Quick exam anchors
- Density: p(x) ≥ 0, integrates to 1; probabilities come from integrating over an interval; CDF is the integral, its derivative is the density.
- E[·] = probability-weighted average; sample mean approximates it (basis of Monte Carlo).
- var[x] = E[x²] − E[x]²; cov measures co-movement; independent ⇒ cov = 0 (directly relevant to portfolio variance and diversification).
