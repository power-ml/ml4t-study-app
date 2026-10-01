# Ch. 1 — Introduction (Murphy, *Probabilistic Machine Learning: An Introduction*, Book 1)

**Source:** Kevin P. Murphy, *Probabilistic Machine Learning: An Introduction* (MIT Press). Online version, April 18, 2025.
**Chapter 1 span:** book pp. 1–29 = **PDF pp. 31–59** (Ch. 2 begins PDF p. 62).
**Week-1 recommended reading for GT ML4T Exam 1.**

> Study notes distilled faithfully from the text. Section numbers (e.g., §1.2.3) are the book's own.

---

## 1.1 What is machine learning? (PDF p. 31)

- **Mitchell's definition:** "A computer program learns from experience *E* w.r.t. tasks *T* and performance measure *P*, if its performance at *T*, measured by *P*, improves with *E*." The three levers of any ML setup are **T** (task), **P** (performance measure), **E** (training signal/experience).
- This book takes a **probabilistic perspective**: treat all unknown quantities (predictions, model parameters) as **random variables** endowed with **probability distributions**.
- Two reasons for the probabilistic approach: (1) it is the **optimal approach to decision-making under uncertainty**; (2) it is the shared language of science/engineering, giving a unifying framework.

---

## 1.2 Supervised learning (PDF p. 31)

**Goal:** learn a mapping *f* from inputs **x ∈ X** to outputs **y ∈ Y**.

Key terminology (memorize — exam loves synonyms):
- **Inputs x** = features = covariates = predictors. Often a fixed-dim vector, X = R^D (D = number of features / dimensionality). In statsmodels: *exogenous* variables.
- **Output y** = label = target = response. In statsmodels: *endogenous* variable.
- **Experience E** = training set **D = {(xn, yn)}**, n = 1..N. **N = sample size.**
- **Design matrix:** N × D matrix; each **row = an example**, each **column = a feature**.
  - Tall & skinny: N ≫ D. Short & fat: D ≫ N (e.g., genomics). "Big data" = large N; "wide data" = large D.
- **Tabular data** vs. variable-size inputs (sequences, graphs) → converted to fixed-size vectors via **featurization**.

### 1.2.1 Classification (PDF p. 32)
- Output space = **C unordered, mutually exclusive labels (classes)**, Y = {1,...,C}. Also called **pattern recognition**.
- **Binary classification** = 2 classes (y ∈ {0,1} or {−1,+1}).
- **Exploratory data analysis (EDA):** inspect data first (patterns, label noise, outliers). Tools: **pair plot** (scatter of feature pairs + marginal on diagonal), color-coded by class; for high-D data, do **dimensionality reduction** first.
- **Decision rule / classifier** partitions input space via a **decision boundary**; nested rules form a **decision tree** inducing a **decision surface**. Tree stores, per node, feature index + threshold; all these are **parameters θ**.

**Empirical Risk Minimization (ERM) (PDF p. 36):**
- **Misclassification rate** on training set: L(θ) = (1/N) Σ I(yn ≠ f(xn;θ)), where **I** = indicator function (1 if true, else 0).
- **Loss function l(y, ŷ)** generalizes this; errors can be asymmetric (costlier one way — poisonous-flower loss matrix example).
- **Empirical risk** = average loss on training set: L(θ) = (1/N) Σ l(yn, f(xn;θ)).
- **Zero-one loss** l01 = I(y ≠ ŷ) → makes empirical risk equal the misclassification rate.
- **Model fitting / training** = **ERM**: θ̂ = argmin_θ L(θ). **But the true goal is to minimize expected loss on FUTURE data (generalize), not just training loss** (see §1.2.3).

**Uncertainty (PDF p. 37):**
- **Epistemic (model) uncertainty:** lack of knowledge of the mapping — *reducible* with more data.
- **Aleatoric (data) uncertainty:** intrinsic/irreducible stochasticity.
- Model the conditional distribution p(y=c|x;θ) = f_c(x;θ), with 0 ≤ f_c ≤ 1 and Σ f_c = 1.
- **Softmax function** converts unnormalized **logits** a = f(x;θ) into a valid probability distribution: softmax(a)_c = e^{a_c} / Σ e^{a_c'}.

**Logistic regression & MLE (PDF p. 38):**
- Affine model f(x;θ) = b + wTx → passed through softmax = **logistic regression**.
- Terminology: **w** = weights (stats: regression coefficients β); **b** = bias (stats: intercept). Bias here ≠ statistical bias.
- Absorbing bias into weights turns an **affine** function into a **linear** one: f(x;w) = wTx.
- **Maximum Likelihood Estimation (MLE):** use **negative log-likelihood (NLL)** as loss: l = −log p(y|f(x;θ)); θ̂_mle = argmin NLL(θ). A good model assigns high probability to the true output.

### 1.2.2 Regression (PDF p. 38)
- Predict a **real-valued** output y ∈ R (vs. discrete class).
- **Quadratic / l2 loss:** l2(y,ŷ) = (y − ŷ)2. Penalizes large **residuals** (y − ŷ). Empirical risk = **Mean Squared Error (MSE)**.
- Model output uncertainty with a **Gaussian/normal**: p(y|x;θ) = N(y | f(x;θ), σ2). With fixed σ2, **NLL ∝ MSE** → MLE = minimizing squared error.
- **Linear regression:** f(x;θ) = b + wx (w = slope, b = offset/intercept); **least squares** = argmin MSE. **Multiple linear regression** = many input features.
- **Polynomial regression:** f(x;w) = wTφ(x) with φ(x) = [1, x, x2,...,x^D] — an example of **feature preprocessing / feature engineering**. Still **linear in the parameters w** (nonlinear in x) → MSE has a unique global optimum.
- **Deep Neural Networks (DNNs) (PDF p. 42):** learn the feature extractor φ(x;V) automatically; stack of L nested functions f(x;θ) = f_L(f_{L−1}(...f1(x)...)). Variants: **CNNs** (images), **RNNs** (sequences).

### 1.2.3 Overfitting and generalization (PDF p. 42) ★ high-yield
- A flexible model can drive **training loss to 0** by memorizing → **overfitting** (fits training data but too complex).
- **Population risk** L(θ; p*) = expected loss under the true data distribution p*(x,y) — what we actually care about.
- **Generalization gap** = L(θ; p*) − L(θ; D_train). Large gap (low train risk, high population risk) ⇒ overfitting.
- p* is unknown → split data into **training set** and **test set**; approximate population risk with **test risk** L(θ; D_test).
- **U-shaped test-error curve** vs. model complexity: too simple = **underfitting** (left); too complex = **overfitting** (right); middle = "just right." Training error monotonically decreases with complexity.
- **Model selection:** never pick by training loss (always chooses the most complex / most **degrees of freedom**). Use **three sets: training (fit), validation (model selection), test (estimate future/population risk only — never used for fitting or selection).**

### 1.2.4 No Free Lunch (NFL) theorem (PDF p. 43)
- "All models are wrong, but some are useful." **No single model is best for all problems.**
- Reason: a set of assumptions = **inductive bias** that helps in one domain may hurt in another.
- Choose models via **domain knowledge** and/or trial-and-error (cross-validation, Bayesian methods). Keep many models/techniques in your toolbox.

---

## 1.3 Unsupervised learning (PDF p. 44)

- Only inputs **D = {xn}**, no outputs. Goal: "make sense of" data, not learn a mapping.
- Probabilistic view: fit an **unconditional model p(x)** (vs. supervised **conditional model p(y|x)**).
- Advantages: no need for expensive labels; avoids arbitrary category definitions; forces the model to "explain" high-dimensional inputs → richer world models. (Supervised learning is "glorified curve fitting.")

- **§1.3.1 Clustering:** partition inputs into regions of similar points. **No single correct number of clusters** — trade off model complexity vs. fit.
- **§1.3.2 Latent factors of variation:** assume high-D xn generated from low-D **latent factors zn ∈ R^K**. Linear version = **Factor Analysis (FA)**; special case (Σ = σ2I) = **(probabilistic) PCA**. Nonlinear extension via DNN → **variational autoencoder (VAE)**.
- **§1.3.3 Self-supervised learning:** create **proxy supervised tasks from unlabeled data** (e.g., predict masked words, colorize grayscale). Learns useful features for downstream supervised tasks.
- **§1.3.4 Evaluating unsupervised learning:** hard — no ground truth. Approaches: (1) **density estimation** — measure NLL/probability assigned to unseen test data (good model isn't "surprised"); relates to **data compression**; (2) use learned representation as features for a downstream task → improves **sample efficiency**; (3) **gain understanding / interpretability** ("carve nature at its joints").

---

## 1.4 Reinforcement learning (RL) (PDF p. 47)

- An **agent** learns to **interact with an environment** via a **policy a = π(x)** mapping states → actions.
- Difference from supervised learning: agent is **not told the correct action**; it only gets an occasional **reward** (or punishment) signal. "Learning with a critic" (occasional thumbs up/down) vs. "learning with a teacher."
- Hard because reward is sparse/delayed → **credit-assignment problem** (which action earned the reward?).
- LeCun's cake analogy: unsupervised = sponge (bulk), supervised = icing, RL = cherry.

---

## 1.5 Data (PDF p. 49)

- Data nature/quality is as vital as the model.
- **Image datasets:** MNIST (60k train / 10k test, 28×28 grayscale digits — the "drosophila of ML"), EMNIST, Fashion-MNIST, CIFAR-10/100, **ImageNet** (~14M images; ILSVRC benchmark; CNNs surpassed a human in 2015).
- **Text / NLP datasets & tasks:** text classification / **sentiment analysis** (IMDB reviews), **machine translation** (WMT), **seq2seq** (summarization, question answering — SQuAD), **language modeling** (unconditional generative model of text p(x1...x_T) — a form of unsupervised learning).

### 1.5.3 Preprocessing discrete input data (PDF p. 53)
- **One-hot encoding (dummy encoding):** categorical variable with K values → indicator vector, e.g., red = [1,0,0].
- **Feature crosses:** linear model on one-hot features captures only **main effects**, not **interaction effects**. Explicit feature crosses (composite features) capture interactions → data becomes **wide format**.

### 1.5.4 Preprocessing text data (PDF p. 53)
- Challenges: variable length, high-cardinality categorical words, **out-of-vocabulary (OOV)** words.
- **Bag of words (BoW):** ignore word order; map words → tokens; represent doc as count vector (**vector space model**). Preprocessing: drop punctuation, lowercase, **stop word removal**, **word stemming**.
- **TF-IDF:** down-weight globally frequent words. IDF_i = log(N / (1+DF_i)); TFIDF_ij = log(TF_ij + 1) × IDF_i.
- **Word embeddings:** map sparse one-hot vectors to dense low-D vectors so semantically similar words are close (fixes that one-hot/count vectors put "man" no closer to "woman" than to "banana"). Often use a **pre-trained embedding** → model stays linear in W.
- **OOV / novel words:** replace with **UNK**, or use **subword units / wordpieces** via **byte-pair encoding (BPE)**.

### 1.5.5 Handling missing data (PDF p. 56)
- Missingness matrix M (M_nd = 1 if feature missing).
- **MCAR** (missing completely at random): missingness independent of all features. **MAR** (missing at random): depends only on *observed* features. **NMAR** (not missing at random): depends on the hidden values themselves — must model the missingness mechanism.
- Common fixes: **mean value imputation**, or fit a generative model to fill in missing values. (This book assumes MAR.)

---

## 1.6 Discussion (PDF p. 57)

- **ML vs. related fields:** predictive analytics (business-focused supervised learning), data mining (structured/commercial DBs), data science (ML + stats + integration/visualization), **statistics** (very close), **AI** (ML now used so an AI system acquires its own knowledge; "ML" and "AI" sometimes used interchangeably).
- **Structure of the book:** probability theory is the unifying lens. Part I = foundations; Parts II–IV = supervised; Part V = unsupervised. RL is covered in the sequel [Mur23].
- **Caveats:** loss functions are hard to specify → **reward hacking**, part of the broader **alignment problem** (AI ethics/safety). **Inverse RL (IRL)** infers reward from human behavior. **AGI** (autonomous decisions) vs. **IA / augmented intelligence** (human in the loop).

---

## Key formulas cheat-sheet
| Concept | Formula |
|---|---|
| Empirical risk | L(θ) = (1/N) Σ l(yn, f(xn;θ)) |
| Misclassification rate | zero-one loss l01 = I(y ≠ ŷ) |
| Softmax | softmax(a)_c = e^{a_c} / Σ_{c'} e^{a_{c'}} |
| Regression (l2) loss / MSE | (y − ŷ)2 ; MSE = (1/N) Σ (yn − f(xn;θ))2 |
| NLL (fitting probabilistic models) | −(1/N) Σ log p(yn | f(xn;θ)); MLE = argmin NLL |
| Generalization gap | L(θ; p*) − L(θ; D_train) |

---

## ML4T Exam 1 relevance
- **→ ML Domain 1 (Learning Paradigms & Problem Framing) [PRIMARY]:** supervised vs. unsupervised vs. reinforcement learning distinctions; classification vs. regression; the T/P/E framing; conditional p(y|x) vs. unconditional p(x) models; loss functions, empirical risk minimization, and MLE as the fitting objective. This is the core week-1 vocabulary the exam tests.
- **→ ML Domain 8/9 (Model Evaluation, Overfitting & Generalization):** overfitting vs. underfitting, U-shaped test-error curve, generalization gap, train/validation/test split (validation = model selection; test = future-performance estimate only), degrees of freedom, No Free Lunch / inductive bias, and (for ML4T) why a model that memorizes in-sample data fails out-of-sample — directly analogous to backtest overfitting on historical price data.
- **Supporting:** feature engineering/preprocessing (polynomial features, one-hot, feature crosses), linear vs. polynomial regression and least squares (ties to the course's regression-learner and decision-tree material), and epistemic vs. aleatoric uncertainty.
