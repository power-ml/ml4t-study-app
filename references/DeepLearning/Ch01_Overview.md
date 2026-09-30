# Ch. 1 — The Deep Learning Revolution (Overview)

**Source:** Bishop & Bishop, *Deep Learning: Foundations and Concepts* (Springer, 2024).
**Book pages 1–21** (PDF pages 21–41). Section 1.1 pp. 2–5; §1.2 Tutorial Example pp. 6–15; §1.3 Brief History pp. 16–21.

> **→ ML4T Exam-1 relevance: ML Domain 1 (Learning Paradigms), ML Domain 9 (Generalization / Overfitting), plus the core supervised-vs-unsupervised framing tested throughout.**

---

## 1. What deep learning is (§1.1)
- **Deep learning** = machine learning based on multilayer **neural networks** trained on large data sets; a single general framework replaces many hand-crafted, application-specific algorithms.
- **Learning / training** = the process of setting a model's adjustable **parameters (weights)** from data. Modern nets can have millions to ~1 trillion (10^12) parameters.
- Application examples span medical diagnosis, protein structure (AlphaFold), image synthesis, and large language models (LLMs) — all variants of the *same* framework.

### Learning paradigms (from the four examples) — **exam-critical**
- **Supervised learning:** each training example has a known target/label.
  - **Classification:** output assigned to a discrete set of classes (e.g., benign vs. malignant).
  - **Regression:** output is one or more *continuous* variables (e.g., predict chemical yield from temp/pressure).
- **Unsupervised learning:** data is *unlabelled* (e.g., generating new synthetic face images).
- **Generative AI / autoregressive models:** LLMs take a word sequence and predict the next word; the augmented sequence is fed back to generate more (used for text generation).

---

## 2. The polynomial curve-fitting tutorial (§1.2) — the backbone example

Setup: input `x`, target `t`; training set of N observations; goal is **generalization** = accurate prediction on previously unseen inputs. Data = underlying regularity (here sin(2πx)) + random (Gaussian) noise.

**Linear model (polynomial):**
$$y(x,\mathbf{w}) = w_0 + w_1 x + \dots + w_M x^M = \sum_{j=0}^{M} w_j x^j \tag{1.1}$$
- Nonlinear in `x` but **linear in the coefficients w** → called a **linear model**.

**Sum-of-squares error function:**
$$E(\mathbf{w}) = \tfrac{1}{2}\sum_{n=1}^{N}\{y(x_n,\mathbf{w}) - t_n\}^2 \tag{1.2}$$
- Non-negative; zero iff the curve passes through every point. Quadratic in w → **unique closed-form minimum** w*.

**Root-mean-square (RMS) error** (lets you compare across data-set sizes, same units as t):
$$E_{RMS} = \sqrt{\tfrac{1}{N}\sum_{n=1}^{N}\{y(x_n,\mathbf{w}^\*) - t_n\}^2} \tag{1.3}$$

### Model complexity & overfitting — **exam-critical**
- Order **M is a hyperparameter** controlling model complexity.
- Low M (0,1): underfits (too inflexible). M=3: good fit. **M=9: fits training data exactly (E=0) but oscillates wildly → over-fitting**, large test error.
- Overfitting symptom: coefficient magnitudes grow very large as M increases (finely tuned to noise).
- **More data reduces overfitting:** a given complex model over-fits less as N grows. Classical heuristic: N ≥ 5–10× the number of parameters (though deep learning routinely violates this).

### Regularization (§1.2.5) — **exam-critical**
Add a penalty on coefficient size to the error:
$$\tilde{E}(\mathbf{w}) = \tfrac{1}{2}\sum_{n=1}^{N}\{y(x_n,\mathbf{w}) - t_n\}^2 + \tfrac{\lambda}{2}\|\mathbf{w}\|^2 \tag{1.4}$$
where $\|\mathbf{w}\|^2 = w_0^2 + \dots + w_M^2$; λ controls regularization strength.
- Known as **shrinkage** (statistics) or **weight decay** (neural nets).
- λ controls *effective* model complexity: too small → overfit; too large → underfit. (w0 often excluded from the penalty.)

### Model selection (§1.2.6) — **exam-critical**
- Hyperparameters (λ, M) **cannot** be chosen by minimizing training error (would drive λ→0, M large → overfit).
- Partition data: **training set** (fit w) + **validation / hold-out / development set** (choose model) + optionally a **test set** for final unbiased evaluation.
- **S-fold cross-validation:** split into S groups; train on S−1, validate on the held-out group; rotate; average scores. Uses (S−1)/S of data for training. **S = N → leave-one-out.**
- Drawback: cost multiplies by S; combinatorial explosion with many hyperparameters. Modern large models rely more on heuristics/experience than exhaustive search.

---

## 3. Brief history of ML / neural networks (§1.3)

**Single artificial neuron:**
$$a = \sum_{i=1}^{M} w_i x_i \tag{1.5}, \qquad y = f(a) \tag{1.6}$$
- `a` = pre-activation; `f(·)` = activation function; `y` = activation; `w_i` = weights (synapse strengths). Polynomial (1.1) is a special case (f = identity, inputs = powers of x).

**Three phases:**
1. **Single-layer networks / perceptron** (Rosenblatt): step activation (fires if weighted input > threshold). Perceptron algorithm provably converges if data is linearly separable. Minsky & Papert (1969) proved single-layer limitations (and wrongly conjectured they'd extend to multilayer) → "AI winter." A modern net is still sometimes called a **multilayer perceptron (MLP)**.
2. **Backpropagation era (mid-1980s):** replace step function with **differentiable** activations + differentiable error functions → gradients computable. **Hidden units** = middle-layer nodes (values not in training data). **Feed-forward networks**; trained by **error backpropagation** (Rumelhart, Hinton, Williams 1986) + **stochastic gradient descent**. Recognized central role of probability/statistics and **inductive bias / prior knowledge**. Limitation: only last ~2 layers learned useful values; heavy reliance on hand-crafted **feature extraction**.
3. **Deep networks (2010s–now):** many-layer nets trainable effectively → **deep learning** (LeCun, Bengio, Hinton 2015). Driven by scale (parameters up to ~10^12), massive data, and **GPUs** (parallelism). Compute to train SOTA models: doubling ~2 yrs pre-2012 (Moore's law), then ~3.4 months after 2012.

---

## Quick exam anchors
- Supervised = labelled; classification (discrete) vs. regression (continuous). Unsupervised = unlabelled.
- Generalization is the goal; overfitting = fitting noise; controlled by complexity, data size, and regularization.
- Validation set / cross-validation choose hyperparameters; test set gives final estimate.
- Regularization = weight decay = shrinkage; λ penalizes large weights.
