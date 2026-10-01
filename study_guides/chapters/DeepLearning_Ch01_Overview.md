# Study Guide — Deep Learning (Bishop) Ch. 1: The Deep Learning Revolution (Overview)

**Source ref:** `references/DeepLearning/Ch01_Overview.md`
**Book pages:** Bishop & Bishop, *Deep Learning: Foundations and Concepts* (Springer, 2024), **pp. 1–21** (PDF pp. 21–41). §1.1 pp. 2–5; §1.2 Tutorial Example pp. 6–15; §1.3 Brief History pp. 16–21.
**Week:** 5 (recommended, Exam-1 scope).

---

## 1. Key concepts (must-know)

**What deep learning is (§1.1)**
- **Deep learning** = ML based on multilayer **neural networks** trained on large data sets — one general framework replacing many hand-crafted, application-specific algorithms.
- **Learning / training** = setting a model's adjustable **parameters (weights)** from data (modern nets: millions to ~1012 params). "Deep learning adds" automatic feature learning + scale.

**Learning paradigms (exam-critical)**
- **Supervised:** every training example has a known target/label.
  - **Classification** → output assigned to a discrete set of classes (benign vs. malignant).
  - **Regression** → output is one or more *continuous* variables.
- **Unsupervised:** data is *unlabelled* (e.g., generating synthetic faces).
- **Generative / autoregressive (LLMs):** predict the next word from a sequence; feed the augmented sequence back to generate more.

**Polynomial curve-fitting tutorial (§1.2) — the backbone example**
- Linear model: $y(x,\mathbf{w}) = \sum_{j=0}^{M} w_j x^j$ (1.1) — nonlinear in x but **linear in w** → "linear model."
- Sum-of-squares error: $E(\mathbf{w}) = \tfrac{1}{2}\sum_{n=1}^{N}\{y(x_n,\mathbf{w}) - t_n\}^2$ (1.2) — quadratic in w → unique closed-form minimum.
- RMS error: $E_{RMS} = \sqrt{\tfrac{1}{N}\sum\{y(x_n,\mathbf{w}^*) - t_n\}^2}$ (1.3) — comparable across data-set sizes; same units as t.
- **Order M is a hyperparameter** for complexity. Low M underfits; **M=9 fits training exactly (E=0) but over-fits** (wild oscillation, large test error). Over-fitting symptom: coefficient magnitudes blow up. **More data reduces over-fitting** (heuristic N ≥ 5–10× #params).

**Regularization (§1.2.5) — exam-critical**
- $\tilde{E}(\mathbf{w}) = \tfrac{1}{2}\sum\{y(x_n,\mathbf{w}) - t_n\}^2 + \tfrac{\lambda}{2}\|\mathbf{w}\|^2$ (1.4).
- = **shrinkage** (stats) = **weight decay** (nets). λ controls *effective* complexity: too small → overfit; too large → underfit.

**Model selection (§1.2.6)**
- Hyperparameters (λ, M) **cannot** be chosen by minimizing training error. Partition: **training** (fit w) + **validation / hold-out** (choose model) + **test** (final unbiased estimate).
- **S-fold cross-validation:** rotate held-out groups, average; **S = N → leave-one-out**. Drawback: cost ×S.

**Brief history (§1.3)**
- Single neuron: $a = \sum_i w_i x_i$ (1.5), $y = f(a)$ (1.6). Three phases: (1) perceptron (step activation, linearly-separable limit; Minsky–Papert → AI winter; MLP name); (2) backprop era (differentiable activations, hidden units, SGD, inductive bias, hand-crafted features); (3) deep nets 2010s (scale, big data, GPUs).

---

## 2. Why it matters for Exam 1

**Mapped domains (per `references/INDEX.md`):** **ML Domain 1 (Learning Paradigms & Problem Framing)** and **ML Domain 9 (Overfitting / Generalization).**

Question themes:
- D1: supervised (labelled) vs. unsupervised (unlabelled); classification (discrete) vs. regression (continuous); "presence of labels defines the paradigm, not the output/features."
- D9: overfitting = near-zero training error + poor test error (high variance); regularization/weight decay as a capacity knob; validation/CV for hyperparameter choice, test set reserved for final estimate; U-shaped test error vs. complexity.

---

## 3. Sample questions (verbatim from mapped-domain verdict tables)

### [ML-D1G1Q1] Supervised vs. unsupervised — labels define the paradigm
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Predicting next-day returns from labeled history is supervised: the realized next-day return is a known target (Y) paired with each feature row, so the model learns a mapping X → Y. |
| C | True | Discovering structure with no supplied targets is the definition of unsupervised learning (e.g., clustering, dimensionality reduction). |
| D | False | A buy/sell output does not imply supervised learning — a hand-coded rule or an unsupervised signal can also emit actions. The *action format* doesn't reveal how (or whether) learning used labels. |

*(Source: `study_notes/ML/Domain_01_Learning_Paradigms_and_Problem_Framing.md`.)*

### [ML-D9G1Q1] Near-zero training error, poor on new data — classic overfitting
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Near-zero training error with poor performance on unseen data is the textbook overfitting signature — the model fit sample-specific noise rather than the underlying signal. |
| D | True | Reducing model capacity/complexity limits the model's ability to memorize noise, directly attacking overfitting. |
| E | False | Underfitting produces poor performance even on the *training* data; here training error is near zero, so this is not underfitting. |

*(Source: `study_notes/ML/Domain_09_Overfitting_Underfitting_and_Generalization.md`.)*

### [ML-D9G6Q2] Regularized linear regression — penalty strength
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The penalty makes large coefficient magnitudes costly, discouraging reliance on them (shrinkage). |
| C | True | Moderate regularization trades a little bias for lower variance, improving generalization when the unregularized model overfits. |
| D | True | An excessively strong penalty over-shrinks and suppresses useful relationships, causing underfitting. |

*(Source: `study_notes/ML/Domain_09_...md` — ties directly to Bishop Eq. 1.4 weight decay.)*
