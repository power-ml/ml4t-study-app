# Study Guide — Deep Learning (Bishop) §2.1: The Rules of Probability

**Source ref:** `references/DeepLearning/Ch02-1_Probability.md`
**Book pages:** Bishop & Bishop, *Deep Learning: Foundations and Concepts* (Springer, 2024), **pp. 23–31** (PDF pp. 43–51). Ch. 2 intro pp. 23–24; §2.1 pp. 25–31.
**Week:** 2 (recommended, Exam-1 scope).

---

## 1. Key concepts (must-know)

**Two kinds of uncertainty (Ch. 2 intro)**
- **Epistemic (systematic):** from a *finite* data set; reduced by observing more data.
- **Aleatoric (intrinsic / noise):** persists with infinite data; reduced by gathering *different kinds* of data.
- Both handled by probability theory via two rules: **sum** and **product**.

**Two views of probability**
- **Frequentist:** probability = frequency of a repeatable event in the infinite-trial limit.
- **Bayesian:** probability = quantification of uncertainty; more general (includes frequentist as a special case).

**Sum and product rules (§2.1.2) — exam-critical**
- Joint: $p(X=x_i, Y=y_j) = n_{ij}/N$. Marginal: $p(X=x_i) = c_i/N$. Conditional: $p(Y=y_j \mid X=x_i) = n_{ij}/c_i$.
- **Sum rule:** $p(X) = \sum_{Y} p(X, Y)$ (2.8) — *marginalization* = summing out other variables.
- **Product rule:** $p(X, Y) = p(Y \mid X)\, p(X)$ (2.9).

**Bayes' theorem (§2.1.3) — exam-critical**
- $p(Y \mid X) = \dfrac{p(X \mid Y)\, p(Y)}{p(X)}$ (2.10), with $p(X) = \sum_Y p(X \mid Y)\, p(Y)$ (2.11) — the denominator is the **normalization constant**.

**Prior vs. posterior (§2.1.5)**
- **Prior p(C):** belief *before* evidence. **Posterior p(C | T):** belief *after* evidence T, via Bayes.

**Independence (§2.1.6):** X ⊥ Y ⟺ $p(X, Y) = p(X)\,p(Y)$ ⟺ $p(Y \mid X) = p(Y)$.

**Worked base-rate example (exam-critical):** prevalence p(C=1)=0.01; sensitivity p(T=1|C=1)=0.90; false-positive p(T=1|C=0)=0.03.
- Positive rate: $p(T{=}1) = 0.03(0.99) + 0.90(0.01) = 0.0387$ (~4%).
- Posterior: $p(C{=}1 \mid T{=}1) = \dfrac{0.90 \times 0.01}{0.0387} \approx 0.23$ (23%).
- **Lesson:** even an "accurate" test gives only 23% posterior because the **prior (base rate) is low** — the base-rate fallacy behind precision/recall intuition.

---

## 2. Why it matters for Exam 1

**Mapped domains (per `references/INDEX.md`):** **ML Domain 1 / Domain 2** — probabilistic foundations, Bayes' theorem, conditional probability, and the base-rate reasoning behind classifier evaluation.

Question themes:
- Class *probability* outputs are still classification; a probability/rate target (0–1) is still regression (the target's nature decides) — Bayes gives $p(Y=j\mid X)$.
- Base-rate / prior reasoning underpins why accuracy misleads on imbalanced (low-prevalence) outcomes.

---

## 3. Sample questions (verbatim from mapped-domain verdict tables)

### [ML-D1G2Q2] Margin-call alert — INVERTED logic
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: margin call vs. none is a two-class discrete outcome → classification. |
| C | True (incorrect) | Wrong: producing a class *probability* does not turn classification into regression — a probability is a standard classification output. |
| E | True (incorrect) | Wrong: classification and regression targets require *different* metrics; the same metric can't be applied without changing its meaning. |

*(Source: `study_notes/ML/Domain_01_Learning_Paradigms_and_Problem_Framing.md`.)*

### [ML-D1G2Q8] Recession probability — regression of a 0–1 target
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Predicting a value on a continuous scale (a probability 0–1) is a regression task, since the response is quantitative/continuous. |
| C | True | MSE here = mean squared difference between predicted probability and the 0/1 outcome — this is the Brier score. |
| D | True | Restricting output to "Recession"/"No Recession" (a discrete category) shifts the task from regression to classification. |

*(Source: `study_notes/ML/Domain_01_...md`. Connects to Bishop's p(C=1|T=1) posterior as a probability output.)*

### [ML-D2G1Q4] Missing volume during liquidity crunches (MNAR)
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | It is **not** MAR: the volume is missing *because* the (unobserved) volume was effectively zero/untradeable — the missingness depends on the value itself, which is MNAR. |
| D | True | Missingness that coincides with liquidity crunches is itself an informative feature: a null in a liquidity field flags untradeability, valuable to a risk model. |
| E | True | When data is MNAR, any imputation that does not model the *cause* of missingness introduces systematic bias into the backtest. |

*(Source: `study_notes/ML/Domain_02_Data_and_Sampling_Discipline.md` — conditional-probability reasoning P(missing | value).)*
