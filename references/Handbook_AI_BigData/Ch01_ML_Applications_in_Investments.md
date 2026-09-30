# Ch. 1 — On Machine Learning Applications in Investments

**Source:** Chen, M. (Robeco) & Zhou, W. — *Handbook of AI and Big Data Applications in Investments*, CFA Institute Research Foundation (2023).
**Book pages:** 2–19 (PDF pages 23–40).
**ML4T exam relevance:** ML Domain 1 (supervised learning, regression/classification, ensembles, decision trees, overfitting), ML Domain 2 (evaluation, bias/variance, data splitting), QF Domain 9–10 (return prediction, Sharpe ratio, factor models, backtesting). Faithful to source; nothing invented.

---

## 1. Why apply ML to investing (motivations)

- **Primary attraction:** promise of higher **risk-adjusted return**. ML is built for **prediction on high-dimensional data with no functional-form specification**, so it should be good at predicting future equity returns.
- Practitioners have used ML to predict: **cross-sectional equity returns**, **corporate earnings** (more accurate than traditional models), and **crash / severe price-drop probability** (superior to linear models using leverage ratio or distance-to-default).
- **Key driver of outperformance vs. linear models:** ML does **not prespecify the functional relationship** between predictors (financial-statement metrics, past returns) and target (return, earnings). It can capture **interaction effects** and **nonlinear effects**.
  - **Interaction effect:** output is not a linear combination of inputs because one input's effect depends on another's value (e.g., reported earnings matter only when an accounting "red flag" = 0; if red flag = 1, price drops 50% regardless of earnings).
  - **Nonlinear effect:** e.g., relationship between a firm's CDS spread and its equity return (equity as embedded call option on firm assets). Neural networks introduce nonlinearity via **activation functions** (without them a deep net collapses to a linear model).
  - Empirically (Gu, Kelly, Xiu 2020): **interaction effects drive most of the outperformance**; the jury is still out on nonlinear-only contribution (a generalized linear model with splines but no interactions barely beat purely linear).
- **"Data mining" / "knowledge discovery":** ML can find relationships not prespecified by researchers. Attractive with the growing "data deluge," but must guard against **spurious, nonreplicable correlations**.

## 2. Why finance is HARD for ML (unique challenges)

- **Low signal-to-noise ratio:** any single metric weakly determines a security's performance; returns compress company-specific, macro, behavioral, and positioning drivers into one dimension (up/down). Contrast with high-signal domains (e.g., video recommendations).
- **Small data vs. big data:** financial data is small (US = ~100 yrs, at most ~1,200 monthly points per security) vs. billions/trillions in other domains. Small data limits true cross-validation, out-of-sample testing, hyperparameter tuning, robustness checks. **A simpler model on more data often beats a sophisticated model on little data.** (Alternative data is more abundant but overall finance data is still small.)
- **Nonstationarity / adaptive markets / irrationality:** markets are **man-made and adaptive** — they "learn" as participants learn, and published research (e.g., Fama–French 1993) changes behavior (McLean & Pontiff 2016). The **data-generating process changes over time**; humans act irrationally (greed/fear). Contrast static domains (e.g., protein folding).

## 3. Common pitfalls and how to avoid them (exam-critical)

- **Overfitting:** biggest concern given short history + high degrees of freedom in ML. Symptom = great backtest, poor out-of-sample.
  - Mitigations (cross-domain): **cross-validation, feature selection/removal, regularization, early stopping, ensembling, holdout data.**
  - Finance advantage: **human intuition + economic domain knowledge** ("smell tests"). Use **SHAP values** (Shapley additive explanation — average marginal contribution of a feature) to check whether learned relationships make economic sense.
  - **Feature engineering:** curate inputs using domain knowledge up front (e.g., profit margin, debt coverage are sensible crash predictors; CEO's last-name initial is not).
- **Replicability:** even harder for ML than traditional stats — more tunable variables, and open-source algorithms vary by version/random seed/implementation. Mitigate with **robust data + code infrastructure**: version control, fixed parameters (algorithm version, universe, hyperparameters, feature sets), and documentation of all iterations including failures ("research graveyards").
- **Lookahead bias / data leakage:**
  - **Lookahead bias:** using data before it was actually available (use **point-in-time** data — e.g., quarterly results available 40 days after quarter-end must not be used at quarter-end).
  - **Leakage in data:** information that belongs in one split (train/validation/test) leaks into another → overly optimistic results. Mitigate with a **gap period** (months–quarters) between train/validation/test splits.
  - **Leakage in features:** an informative feature that would be unavailable at production time (e.g., undisclosed executive health issue).
- **Implementation gap:** backtest trades that are impossible/infeasible live — e.g., alpha coming from small/micro-cap stocks (too costly, insufficient shares), or shorting stocks that can't be borrowed / cost too much. ML worsens this via **high turnover**.
- **Explainability / performance attribution:** models are complex "black boxes" (though inspectable). Asset owners demand explanations. Technique = **partial dependence response**: fix a feature at value x, average predictions, sweep x over its range → decompose output into **linear, interaction, nonlinear** components; then form portfolios from each to attribute returns.

## 4. Sample applications (examples + results)

- **Predicting cross-sectional stock returns** (relative, not absolute; stock selection, not timing/allocation — an easier problem with more data).
  - Setup: (1) investment universe, (2) ML algorithms (boosted trees/random forests, neural nets, ensembles), (3) feature set (value price-ratios, quality/profitability, momentum/past returns). Limiting the feature set = imposing domain-knowledge structure to fight small data.
  - **Five consistent results:**
    1. ML significantly and economically outperforms linear approaches. Gu et al. (2020): 4-layer NN long–short decile spread → out-of-sample **Sharpe 1.35 (value-weighted), 2.45 (equal-weighted)** vs. OLS **0.61 / 0.83**.
    2. Outperformance comes from **higher-order effects (nonlinearity + interactions)**; interactions matter more than nonlinearity.
    3. The **most important features are consistent across ML algorithms**: short-term reversal, stock & sector momentum, return volatility, firm size.
    4. **Simple ML models beat complex ones** (less overfitting on small data).
    5. **More data → better ML performance** ("unreasonable effectiveness of data").
- **Predicting stock crashes:** crash = large idiosyncratic price drop vs. peers. Algorithms: logistic regression, random forest, gradient-boosted tree, ensemble. Features: distance-to-default, volatility, market beta + fundamentals. Used in **conservative/low-vol equity** ("win by not losing"). ML beats traditional in developed and emerging markets; returns come from stock selection, not sector allocation.
- **Predicting fundamentals (earnings):** easier + more stable target than returns. Cao & You (2021), US ex-financials/utilities, 1975–2019, 28 line items + first differences (56 features). Linear ML beats traditional (~6%); nonlinear ML beats linear ML (~1–3%); **ensembles beat individuals** ("ensembling is the closest thing to a free lunch, like diversification").
- **NLP in multiple languages:** embedding-based NLP to decode Chinese A-share retail-investor slang; word embeddings preserve vector arithmetic (King − Man + Woman ≈ Queen). Shows ML helps non-numerical tasks too.

## 5. Conclusion takeaways

- ML beats traditional methods **if applied to the right problem**; source of edge = nonlinear + interaction effects; **ensembling** adds value.
- Finance is distinctive: less data, nonstationary, irrational participants — so know the technique's limits.
- Other ML uses: sentiment analysis, foreign-language understanding, data cleaning, fraud detection, credit scoring, trading optimization.
