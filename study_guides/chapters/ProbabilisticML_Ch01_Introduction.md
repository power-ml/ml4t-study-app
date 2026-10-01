# Study Guide — Probabilistic Machine Learning (Murphy, Book 1) Ch. 1: Introduction

**Source ref:** `references/ProbabilisticML/Ch01_Introduction.md`
**Book pages:** Kevin P. Murphy, *Probabilistic Machine Learning: An Introduction* (MIT Press), **pp. 1–29** (PDF pp. 31–59). Online version, April 18, 2025.
**Week:** 1 (recommended, Exam-1 scope).

---

## 1. Key concepts (must-know)

**What is ML (§1.1)**
- **Mitchell's definition:** a program learns from experience *E* w.r.t. tasks *T* and performance measure *P* if its performance at T (measured by P) improves with E. Three levers: **T, P, E**.
- **Probabilistic perspective:** treat all unknown quantities as random variables with probability distributions — optimal for decision-making under uncertainty + a unifying language.

**Supervised learning (§1.2)**
- Learn mapping *f*: inputs **x ∈ X** → outputs **y ∈ Y**.
- Terminology (exam loves synonyms): **inputs x** = features = covariates = predictors (exogenous); **output y** = label = target = response (endogenous); **D = {(xn,yn)}**, N = sample size; **design matrix** N×D (row = example, column = feature).
- **Classification (§1.2.1):** C unordered mutually-exclusive classes; binary = 2. EDA, decision boundary/tree, parameters θ. **Softmax:** $\text{softmax}(a)_c = e^{a_c}/\sum e^{a_{c'}}$ turns logits into a distribution.
- **ERM:** empirical risk L(θ) = (1/N) Σ l(yn, f(xn;θ)); zero-one loss l01 = I(y≠ŷ) → misclassification rate. True goal = minimize expected loss on **future** data.
- **MLE:** minimize **negative log-likelihood** l = −log p(y|f(x;θ)).
- **Regression (§1.2.2):** real-valued y; **l2 loss** (y−ŷ)2 → empirical risk = **MSE**; Gaussian output ⇒ NLL ∝ MSE. Linear/polynomial regression linear in w. **DNNs** learn φ(x;V) automatically (CNNs, RNNs).

**Overfitting & generalization (§1.2.3) ★ high-yield**
- Flexible model can drive **training loss to 0** by memorizing → **overfitting**.
- **Population risk** L(θ;p*) = expected loss under true p*; **generalization gap** = L(θ;p*) − L(θ;D_train).
- p* unknown → split train/test; **U-shaped test-error curve** (underfit left, overfit right).
- **Model selection:** never pick by training loss. Use **three sets: training (fit), validation (model selection), test (future-risk estimate only).**

**No Free Lunch (§1.2.4):** no single model is best for all problems; assumptions = **inductive bias**.

**Unsupervised learning (§1.3):** only D = {xn}; fit **unconditional p(x)** (vs. supervised **p(y|x)**). Clustering (no single correct k); latent factors (FA, PCA, VAE); self-supervised (proxy tasks); evaluation is hard (density estimation / NLL, downstream features, interpretability).

**Reinforcement learning (§1.4):** agent + environment + policy a=π(x); learns from occasional **reward** ("critic" not "teacher"); credit-assignment problem.

**Data (§1.5):** one-hot encoding; feature crosses (interaction vs. main effects); BoW, TF-IDF, word embeddings, BPE/UNK; missing data **MCAR / MAR / MNAR**, mean imputation.

**Uncertainty:** **epistemic** (reducible with data) vs. **aleatoric** (irreducible).

---

## 2. Why it matters for Exam 1

**Mapped domains (per `references/INDEX.md`):** **ML Domain 1 (Learning Paradigms) [PRIMARY]** plus **ML Domains 8/9 (Model Evaluation, Overfitting & Generalization).**

Question themes:
- D1: supervised vs. unsupervised vs. RL; classification vs. regression; T/P/E framing; p(y|x) vs. p(x); loss functions, ERM, MLE as the fitting objective — core week-1 vocabulary.
- D8/D9: overfitting vs. underfitting, U-shaped test-error curve, generalization gap, train/validation/test roles (validation = selection; test = future estimate only), No Free Lunch / inductive bias; backtest-overfitting analogy for ML4T.

---

## 3. Sample questions (verbatim from mapped-domain verdict tables)

### [ML-D1G1Q3] Same rows, two paradigms
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Predicting realized one-week return uses that return as a supervised numeric target (each example paired with a known outcome → regression). |
| B | True | Drop the return column and group weeks by feature similarity → no target supplied → the task becomes unsupervised structure discovery. |
| C | False | Using the same feature rows does not force one paradigm; the paradigm is set by the task/target, not by which rows are used. |

*(Source: `study_notes/ML/Domain_01_Learning_Paradigms_and_Problem_Framing.md`. Maps to Murphy p(y|x) vs. p(x).)*

### [ML-D8G1Q1] Train / validation / test — the role of each split
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Training data are used to estimate model parameters / learned structure from observed examples — the definition of the fitting step. |
| B | True | The validation set supports model and hyperparameter selection *before* the final test, giving feedback for pre-test decisions without fitting the test observations. |
| C | False | Repeatedly inspecting test results while revising features turns the test set into part of the development loop — even though the rows aren't fed to the fit method, the decisions adapt to it, destroying its out-of-sample value. |

*(Source: `study_notes/ML/Domain_08_Model_Evaluation_and_Metrics.md`. Maps to Murphy §1.2.3 three-set split.)*

### [ML-D9G1Q3] Three models — matching patterns to over/underfitting
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | High error even on training data means Model A is not capturing enough structure — underfitting / high bias. |
| B | True | Excellent training fit with poor validation performance is the standard overfitting (high-variance) symptom. |
| D | False | Lowest training error rewards memorization and does not establish performance on new data; it never "always" identifies the best model. |

*(Source: `study_notes/ML/Domain_09_Overfitting_Underfitting_and_Generalization.md`. Maps to Murphy's U-shaped test-error curve.)*
