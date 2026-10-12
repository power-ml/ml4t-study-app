# ML Domain 10 — Model Selection & Practical Tradeoffs

## Domain cheat-sheet

- **No free lunch.** No single learner is universally best; the "right" model is contextual — chosen against the *problem's* structure, data, and the decision it supports, not from theoretical flexibility alone. Compare candidates on representative (ideally time-aware, out-of-sample) validation, not on which family "can represent more functions."
- **Match model to problem structure:**
  - Approximately **linear / proportional** relationships → a linear model is a strong, retrainable baseline (fast, transparent, low variance).
  - **Threshold / interaction** effects → decision trees encode conditional splits without hand-specifying each interaction; linear models can still reach some nonlinearity via feature engineering (transforms, interaction terms).
  - Flexibility ≠ accuracy: a more expressive learner can fit **noise** and generalize *worse*, especially with limited/noisy samples where a simpler, lower-variance model often wins.
- **Accuracy vs. interpretability tradeoff.** A small accuracy gain from a black-box model may not justify the loss of explainability when governance, risk, or compliance requires justifying decisions (e.g., adverse-action explanations). Interpretability can be a *binding constraint* even when performance differs — and being "interpretable" does **not** certify inputs are leakage-free or the design is sound. Document the accepted tradeoff to make it reviewable. Interpretability and accuracy are **not** always perfectly opposed — a model can improve one without harming the other.
- **Training time vs. inference time — evaluate each against the workflow where its cost occurs.** They are decoupled: a model can train slowly and infer in microseconds (or the reverse). **Eager/parametric** learners (linear, trees) pay to fit once, then predict cheaply from a compact representation. **Lazy** learners (**KNN**) do almost no fitting (just store data) but push heavy computation to inference — neighbor search cost grows with the stored set N and consumes memory. A 40-min overnight train is fine in a 4-hr window; millisecond inference for a weekly model is irrelevant slack.
- **Sensitivity to noise / data quality.** Least-squares regression is highly sensitive to extreme target values (residuals are **squared**). KNN is sensitive to **feature scale** (large-magnitude features dominate distance) — fix with scaling; larger *k* damps isolated noisy neighbors but adds bias. Deep single trees are unstable — a few corrected rows can restructure early splits. Fix root-cause data defects at the source; **bagging** reduces *variance* but does **not** immunize against *systematic* errors/corruption shared across all learners.
- **Data size vs. model complexity.** More candidate features enlarge the hypothesis space and *increase* the data required; limited observations relative to flexibility → overfitting (perfect training fit is weak evidence of generalization). Restrict depth / min-leaf-size / feature count to cut effective capacity. More data helps distinguish signal from noise but does **not** eliminate the need to control complexity — and raw row count can **overstate** usable information if much of it comes from obsolete regimes (distribution shift). Effective sample *relevance* matters, not just count.
- **Real-time constraints.** A model that violates the latency budget is unusable regardless of offline accuracy — a timely, slightly-less-accurate model can produce better realized outcomes. Measure **end-to-end latency under peak load** (feature computation + system overhead + tail/high-percentile latency, not just one isolated prediction or the average). Latency requirements are strategy-specific: market-making (microseconds) ≠ daily rebalance (minutes) — "must be HFT-suitable" is not a universal requirement.
- **Robustness & stability in production.** Strong *average* backtest performance can hide failure in economically important regimes (e.g., high volatility) — evaluate segmented by regime. Historical success does not guarantee future stability (regimes shift). Prefer models whose outputs are stable under small perturbations and across time splits (bagging lowers prediction variance); a simpler, dependable fallback can be valuable even if not top performer in calm conditions. Stability analysis must consider both predictions *and* downstream decisions (turnover, exposures). Retraining more often does **not** necessarily increase stability — it can amplify sensitivity to short-term sample changes.
- **Comparative reasoning (linear / KNN / tree):** linear = fast, transparent, stable, but underfits without feature engineering; tree = captures thresholds and is inspectable (subject to depth/pruning), but deep trees are unstable; KNN = accurate offline but slow/memory-heavy at inference with the full dataset and provides no compact global equation. Practical selection *manages* these tradeoffs (feature engineering, depth limits/bagging, reference-set reduction) rather than declaring one algorithm inherently superior.

## Common traps

- **Inverted-logic questions (11 of 24): mark True if the statement is *incorrect*, False if *accurate*.** The Answer Key line reads "True = incorrect; False = accurate." Read that polarity line FIRST. Inverted here: **G1Q2, G1Q3, G2Q2, G3Q2, G4Q3, G5Q1, G5Q2, G6Q1, G7Q1, G8Q1, G8Q2.** On these, a "False" verdict means the choice is a *correct* statement, and "True" flags the *flawed/wrong* claim you were asked to find.
- **The trap-within-a-trap.** On inverted questions the plausible-sounding, textbook-correct statements resolve to **False**, and the one overreaching/absolute claim (e.g., "guarantees," "always," "need not understand," "proves") is the **True** answer. Do not let "this statement is true in real life" push you to mark True — that is exactly backwards under inverted polarity.
- **Double-negative "embedded claim" choices:** none appear in Domain 10 — no choice uses the "It is incorrect to conclude that [accurate statement]" construction. (Watch for it in other domains, where the Answer Key marks such choices False because the inner claim is accurate.) The nearest analog here is the inverted-polarity resolution above.
- **Absolute-language distractors are the reliable "flawed" pick.** Words like *always, guarantees, automatically, must, eliminates, immune, universal, need not, dominates, irrelevant* signal the overreaching claim — the intended wrong statement in nearly every question (normal or inverted).
- **Flexibility ≠ better generalization; more data / more features ≠ automatically better.** Recurs across G1, G3, G5. More flexibility or more inputs can raise variance and data requirements, not lower error.
- **"Interpretable / good validation score / bagging / infrequent retraining" do NOT certify what they seem to.** Transparency doesn't validate data or rule out leakage (G2Q1E); a good aggregate score doesn't certify record-level integrity (G4Q1E); bagging doesn't fix systematic corruption (G4Q3C); rare retraining doesn't make inference cost irrelevant (G3Q3D). These "guarantee" claims are the planted errors.

## Questions

### [ML-D10G1Q1] Linear baseline vs. deep tree for near-linear factors
**Scenario:** A systematic equity team sees next-day returns move roughly in proportion to a few standardized factors and wants a dependable, frequently retrained baseline. The PM asks whether to start with a deep tree instead of a linear model just because the tree is more flexible.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | When the observed relationship is approximately linear, a linear model's structure matches it and gives a transparent, low-variance, easily retrained baseline — a sound starting point. |
| B | False | Greater flexibility does not guarantee lower out-of-sample error; the extra capacity can fit noise and generalize worse. Ability to represent more functions ≠ better generalization. |
| C | True | Under a limited or noisy sample, a simpler learner's lower variance can make it more reliable than a complex model that overfits the scarce data. |
| D | True | Comparing candidates on representative validation data tests how the accuracy–flexibility tradeoff actually behaves on unseen observations — better than choosing by theoretical flexibility. |
| E | False | Standardizing features rescales units; it does not change the underlying functional form, so it cannot make a nonlinear relationship linear. |

**Reference:** Flexibility–interpretability and bias–variance — ISLR §2.1.3, §2.2 (assessing model accuracy); concept "no-free-lunch / simpler-model-under-limited-data."

### [ML-D10G1Q2] Threshold interactions: tree vs. linear — INVERTED logic
**Scenario:** A commodity desk finds returns rise only when momentum and inventory jointly cross thresholds and asks whether a straight-line model or a tree fits this structure, with out-of-sample support required. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | A decision tree's successive splits can encode conditional threshold relationships without the analyst specifying each interaction explicitly — accurate, so not a flaw. |
| B | True (incorrect) | Flawed: a purely additive linear model with raw features does **not** automatically reproduce arbitrary threshold interactions; the word "every" overreaches. |
| C | False (accurate) | Feature engineering (transforms, interaction terms) can let a linear model represent some nonlinear/interaction effects — accurate. |
| D | True (incorrect) | Flawed: an apparent threshold structure does not prove the *deepest possible* tree is best; unrestricted depth overfits sample-specific thresholds. |
| E | False (accurate) | Time-aware validation on later periods tests whether the threshold behavior persists beyond training — accurate. |

**Reference:** Trees and interactions — ISLR ch.8 (tree-based methods); feature engineering for linear models — ESL ch.5 (basis expansions); time-series/out-of-sample validation.

### [ML-D10G1Q3] Many correlated features, tiny sample — INVERTED logic
**Scenario:** A cross-sectional strategy has thousands of highly correlated indicators but only two years of monthly data. A client demands the most complex ensemble ("more inputs need a more powerful model") while the risk officer fears unstable estimates. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | A large feature count alone does not justify the most complex learner; model choice depends on usable information and constraints — accurate. |
| B | False (accurate) | Few observations relative to model flexibility genuinely raises overfitting risk (a flexible learner finds accidental patterns) — accurate. |
| C | False (accurate) | A constrained model or reduced feature set is a defensible candidate; cutting effective complexity can improve stability and generalization — accurate. |
| D | True (incorrect) | Flawed: correlated indicators do **not** guarantee independent errors among ensemble members — shared correlated inputs tend to make members err similarly, defeating the diversification an ensemble relies on. |
| E | False (accurate) | Selection should weigh sample size, redundancy, stability, and the prediction task together — these jointly determine suitability, so this is accurate. |

**Reference:** Overfitting with p ≫ n and correlated predictors, ensemble error correlation — ISLR ch.6 (regularization/selection), ch.8 (bagging/random forests, decorrelation).

### [ML-D10G2Q1] Ensemble vs. linear model when decisions must be explained
**Scenario:** A bank approves client leverage limits with a model; an ensemble beats a linear model slightly on validation accuracy, but a compliance officer must explain adverse decisions. Does the accuracy gain settle the choice?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Higher validation accuracy is relevant but need not be the sole criterion; deployment decisions also weigh compliance and operational objectives. |
| B | True | A linear model may be preferred if its explanations satisfy a material governance requirement at an acceptable performance cost — a justified small accuracy sacrifice. |
| C | False | Interpretability is not relevant only when models tie on performance; it can be a binding constraint even when predictive performance differs. |
| D | True | Documenting the performance–interpretability tradeoff makes the rationale and the accepted compromise reviewable and defensible. |
| E | False | Calling a model interpretable does not guarantee its inputs are appropriate or leakage-free; transparency does not validate the data or experimental design. |

**Reference:** Interpretability vs. flexibility and governance constraints — ISLR §2.1.3; scikit-learn "Model interpretation"; concept "adverse-action explainability."

### [ML-D10G2Q2] Internal-only signal favors a black-box model — INVERTED logic
**Scenario:** A hedge fund's internal signal only ranks liquid stocks; no client decision depends on it directly. The PM prefers a less transparent bagged-tree model for a stable out-of-sample gain, but researchers must still monitor it. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Absence of a client-facing explanation need may *reduce but not eliminate* interpretability's value — research, debugging, risk, and oversight still benefit — accurate. |
| B | False (accurate) | A less interpretable model can be reasonable when its benefit is material and adequate controls exist; the acceptable balance depends on objectives and controls — accurate. |
| C | True (incorrect) | Flawed: internal use does **not** mean the team can skip understanding inputs, failure modes, or regime sensitivity — internal models still create financial and operational risk. |
| D | False (accurate) | Monitoring out-of-sample performance matters regardless of transparency; live reliability cannot be inferred from transparency alone — accurate. |
| E | True (incorrect) | Flawed: interpretability and accuracy are **not** always perfectly opposed — some models improve one dimension without necessarily harming the other. |

**Reference:** Interpretability tradeoffs and monitoring — ISLR §2.1.3; ESL ch.8/ch.15 (bagging/random forests); concept "model risk management for internal models."

### [ML-D10G2Q3] Shallow vs. deep tree for a committee-reviewed allocation
**Scenario:** A pension fund compares a shallow tree against a much deeper one for tactical allocation. The deep tree has a tiny validation edge but decides through many narrow rules the investment committee cannot reliably review.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The shallow tree's fewer splits produce a more compact decision path that the committee can inspect more easily. |
| B | False | A validation improvement does not automatically dominate governance concerns; a negligible gain may not justify the added complexity and oversight cost. |
| C | True | The small performance difference should be checked for statistical and practical significance — sampling variation can make a tiny observed edge meaningless. |
| D | True | Stability across multiple time splits helps judge whether the deep tree's advantage is durable rather than a lucky single split. |
| E | False | Choosing the shallow tree does not abandon all nonlinearity; even a shallow tree represents thresholds and limited interactions. |

**Reference:** Tree depth, pruning, and interpretability; significance of small performance gaps — ISLR ch.8; ESL ch.7 (model assessment/selection).

### [ML-D10G3Q1] Real-time system: speed vs. complex ensemble
**Scenario:** You are picking a model for a real-time trading system. The Head of Trading prioritizes speed; a data scientist advocates a complex ensemble.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | For a real-time system, fast inference is the operative constraint, so inference time outweighs training time here. |
| B | True | KNN is often unsuitable for real-time use because it defers heavy neighbor-search computation to inference (high latency). |
| C | True | Linear models are computationally efficient at inference (a dot product with the coefficient vector), so they are often preferred for speed. |
| D | False | More complex models are not always better; tradeoffs among accuracy, latency, and robustness exist. |
| E | True | The appropriate choice depends on system constraints (latency budget, throughput, memory) — context determines the decision. |

**Reference:** Train vs. inference cost, lazy vs. eager learners — ISLR §2.2.3 (KNN); scikit-learn "Computational performance"; concept "latency-constrained deployment."

### [ML-D10G3Q2] Overnight retrain fits the window — INVERTED logic
**Scenario:** An asset manager retrains a weekly allocation model overnight (one set of weights before Monday's open). The research director rejects a candidate that trains in 40 minutes even though prediction takes milliseconds and the overnight window is four hours. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Forty minutes of training fits well inside the four-hour retraining window — accurate. |
| B | False (accurate) | Millisecond inference is more than sufficient for a model that predicts only once per week — accurate. |
| C | False (accurate) | Training and inference costs should each be judged against the workflow where they occur; different schedules value them differently — accurate. |
| D | True (incorrect) | Flawed: a slower-training model does **not** necessarily predict more slowly — training and inference have different computational patterns across learners (e.g., KNN trains fast, infers slowly). |
| E | False (accurate) | Rejecting the model solely because another trains in one minute ignores whether the difference affects the deployment objective — accurate. |

**Reference:** Decoupling of train vs. inference cost — ISLR §2.2.3; scikit-learn "Computational performance"; concept "cost matters only against the binding constraint."

### [ML-D10G3Q3] KNN for high-volume what-if serving
**Scenario:** A research platform serves thousands of interactive what-if requests daily against a fixed model but retrains only at month-end. An analyst proposes KNN (fitting just stores data); the platform owner worries about response time and memory growth.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | KNN's near-trivial fitting shifts substantial computation to prediction time (distance/neighbor search happens per query). |
| B | True | KNN inference cost grows with the stored training set — more observations mean more distance computations absent special indexing. |
| C | True | A fitted linear model answers each request from its learned coefficient vector, without scanning all training rows. |
| D | False | Infrequent retraining does not make inference cost irrelevant; with thousands of daily requests, inference can be the dominant operational cost. |
| E | True | Expected request volume and memory constraints belong in the comparison — a deployable choice must meet throughput and resource requirements. |

**Reference:** Lazy-learner inference scaling and memory — ISLR §2.2.3; scikit-learn "Nearest Neighbors" (query complexity), "Computational performance."

### [ML-D10G4Q1] Extreme target values and least-squares sensitivity
**Scenario:** A return dataset has a few extreme target values from bad price adjustments. The PM notes the linear regression fit shifts sharply when those rows are included and asks whether the model should be trusted.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Extreme target errors strongly influence a least-squares fit because squared loss gives large residuals disproportionate weight. |
| B | True | Investigating and correcting confirmed data errors at the source is preferable to picking a model just to accommodate corrupted rows. |
| C | False | Removing every economically extreme observation is not automatically valid — genuine market extremes may be informative and should not be discarded reflexively. |
| D | True | Comparing fits with and without suspect rows is a sensitivity analysis that reveals whether a few rows drive the conclusion. |
| E | False | A good validation score cannot certify record-level data integrity; aggregate performance does not confirm the records are correctly adjusted. |

**Reference:** Sensitivity of squared-error loss to outliers, robust regression, data quality — ISLR ch.3 (linear regression, outliers/leverage); ESL ch.10 (robust loss).

### [ML-D10G4Q2] KNN, feature scaling, and noise
**Scenario:** A KNN strategy uses volatility, volume, and momentum on very different scales. The head quant finds small measurement noise in the high-magnitude volume feature changes which neighbors are selected.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Distance-based KNN is sensitive to feature scale — distance calculations reflect numerical magnitude unless features are treated appropriately. |
| B | True | Appropriate scaling puts features on comparable scales so no feature dominates distance merely because of its units. |
| C | False | Scaling changes magnitude, not information content; it does not guarantee a noisy feature becomes a useful predictor. |
| D | True | Increasing k averages more neighbors and can dampen a single mislabeled/noisy neighbor, though excessive smoothing adds bias (erases local structure). |
| E | False | Feature quality is not irrelevant to KNN; neighbor selection depends directly on the quality of the feature representation, even without learned coefficients. |

**Reference:** KNN scale sensitivity, choice of k, bias–variance — ISLR §2.2.3, §3.5; scikit-learn "Preprocessing" (StandardScaler) and "Nearest Neighbors."

### [ML-D10G4Q3] Deep-tree instability, bagging, and data controls — INVERTED logic
**Scenario:** A single deep tree yields very different trading rules after a few observations are corrected. The risk officer proposes a bagged ensemble plus better data controls, but a researcher claims bagging makes clean data unnecessary. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Deep trees can be unstable: small data changes may alter early splits and cascade through downstream branches — accurate. |
| B | False (accurate) | Bagging reduces variance by averaging predictions from multiple resampled trees — accurate. |
| C | True (incorrect) | Flawed: bagging does **not** guarantee immunity to systematic errors present throughout the data — shared bias or corrupted inputs affect every member. |
| D | False (accurate) | Correcting upstream data defects improves both single models and ensembles — accurate. |
| E | False (accurate) | Robustness should be assessed with plausible perturbation/stress tests, not assumed from the algorithm's name — accurate. |

**Reference:** Tree instability, bagging variance reduction and its limits vs. systematic error — ISLR ch.8 (bagging, random forests); ESL ch.8/ch.15; concept "empirical robustness testing."

### [ML-D10G5Q1] Fully grown tree on 180 obs, 60 features — INVERTED logic
**Scenario:** A crypto strategy has only 180 daily observations and 60 candidate indicators. The PM wants a fully grown tree because it fits the training period perfectly; the analyst warns the sample cannot support so many adaptive choices. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Perfect training fit is weak evidence of generalization in a small sample — a flexible model can memorize it — accurate. |
| B | False (accurate) | A fully grown tree can partition the limited data into highly specific leaves that describe individual rows, not recurring structure — accurate. |
| C | False (accurate) | Restricting depth or minimum leaf size limits effective capacity and can reduce overfitting risk — accurate. |
| D | True (incorrect) | Flawed: adding more candidate indicators does **not** reduce data needs — more features enlarge the search space and *increase* the data required. |
| E | False (accurate) | Later out-of-sample observations are needed to test whether the learned rules persist beyond the construction sample — accurate. |

**Reference:** Overfitting, tree complexity control, curse of dimensionality — ISLR ch.8 (pruning, min-leaf), §2.2 (overfitting); ESL ch.7.

### [ML-D10G5Q2] 5K → 5M examples; reconsidering high-variance models — INVERTED logic
**Scenario:** An equity desk grows from 5,000 to 5 million clean training examples and wants to revisit models previously rejected for high variance. The engineering lead notes KNN would have to retain the enlarged dataset for prediction. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | More representative observations can make fitting a flexible model more reliable by separating stable patterns from sampling noise — accurate. |
| B | True (incorrect) | Flawed: a larger dataset does **not** eliminate the need to control complexity — flexible models can still overfit, and data can carry noise or mismatch. |
| C | False (accurate) | KNN storage and naive inference costs grow with the training set (it stores observations and compares queries against them) — accurate. |
| D | False (accurate) | Scaling constraints (memory, training, serving) may change which model is practical even when predictive accuracy improves — accurate. |
| E | False (accurate) | The value of extra rows depends on their relevance to the deployment distribution; stale/irrelevant data may not help — accurate. |

**Reference:** Sample size vs. variance, KNN scaling, distribution relevance — ISLR §2.2.3, ch.8; scikit-learn "Computational performance"; concept "data relevance vs. raw count."

### [ML-D10G5Q3] Decades of data spanning obsolete regimes
**Scenario:** A global macro team pools decades of daily data to train a complex ensemble. The CIO argues the raw row count is large enough, but many observations come from market structures that no longer exist and only a small fraction represents the current regime.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Raw dataset size can overstate the information relevant to current deployment — effective sample relevance matters beyond total count. |
| B | False | More historical rows do not guarantee lower out-of-sample error now; distribution shift can make additional history misleading. |
| C | True | A complex model may learn obsolete relationships if regime differences are not addressed — its flexibility lets it exploit patterns that no longer operate. |
| D | True | Time-based evaluation on recent periods better approximates the intended use and reveals whether performance transfers. |
| E | True | A simpler model relying on fewer, more stable relationships may be competitive and more robust under regime change. |

**Reference:** Distribution shift/non-stationarity, effective sample size, time-aware evaluation — ISLR §2.2; concept "regime shift and stationarity."

### [ML-D10G6Q1] 200-microsecond market-making latency budget — INVERTED logic
**Scenario:** A market-making system must update quotes within 200 microseconds. A candidate ensemble improves offline error by 0.2% but exceeds the end-to-end latency budget at peak load. Does the gain justify deployment? Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | A model that violates the latency budget may be unusable despite better offline error — predictions arriving too late cannot support the decision — accurate. |
| B | False (accurate) | End-to-end testing under peak load is more relevant than timing one prediction in isolation (production latency includes contention and tails) — accurate. |
| C | True (incorrect) | Flawed: predictive accuracy does **not** always dominate execution speed — late decisions can erase or reverse the value of a small accuracy gain. |
| D | False (accurate) | A faster model with slightly worse error could produce better realized trading outcomes because timely execution can matter more — accurate. |
| E | False (accurate) | Feature computation and system overhead must be included in the latency assessment — inference is only one component — accurate. |

**Reference:** Latency-constrained deployment, tail latency, end-to-end measurement — scikit-learn "Computational performance"; concept "deployment constraints / realized vs. offline performance."

### [ML-D10G6Q2] Daily rebalance vs. "everything must be HFT"
**Scenario:** A daily rebalancing strategy generates orders once after the close within a 30-minute window. A junior engineer insists only HFT-suitable models should be considered because "all trading systems are real time."
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The daily strategy has a materially different latency requirement from a market-making system — its decisions occur on a much slower schedule. |
| B | True | A slower model is acceptable if it completes reliably within the decision window; meeting the actual deadline matters more than minimizing latency for its own sake. |
| C | False | High-frequency suitability is not a universal requirement; model constraints depend on the strategy's holding period and operating design. |
| D | True | With a generous time budget, the team may reasonably prioritize robustness or interpretability over microsecond inference. |
| E | True | Operational deadlines still matter even for non-HFT strategies — missing the rebalance window could disrupt execution. |

**Reference:** Strategy-specific latency requirements, batch vs. real-time — concept "match latency budget to holding period"; scikit-learn "Computational performance."

### [ML-D10G6Q3] Linear → KNN under bursty low-latency load
**Scenario:** A low-latency desk considers moving from a linear model to KNN as its historical dataset grows daily. The system must handle bursts of simultaneous predictions, and the engineering manager asks the team to account for tail latency, not just average.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Naive KNN prediction slows as the stored dataset grows — each query may require distances to an increasing number of observations. |
| B | True | Burst traffic makes high-percentile (tail) latency more important than a low average, which can hide rare deadline-violating delays. |
| C | False | The absence of a costly fitting phase does not make KNN automatically suitable for low-latency serving — it defers much of its computation to inference. |
| D | True | Limiting the reference set could improve speed but may exclude relevant neighbors and change predictive behavior. |
| E | True | The comparison should include throughput, memory, and latency under representative load — these determine whether the model fits the system constraints. |

**Reference:** KNN inference scaling, tail latency under load — ISLR §2.2.3; scikit-learn "Nearest Neighbors," "Computational performance."

### [ML-D10G7Q1] Model good in calm markets, worse in volatility — INVERTED logic
**Scenario:** A live forecasting model performed well in calm markets but its errors rise sharply when volatility increases. The risk committee asks whether strong average backtest performance is enough to keep it active unchanged. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Average performance can conceal failure in economically important regimes — many calm observations hide poor stressed-period behavior — accurate. |
| B | False (accurate) | Evaluating by volatility regime reveals conditional weaknesses (whether performance depends on market state) — accurate. |
| C | True (incorrect) | Flawed: historical success does **not** guarantee the relationship stays stable in production — markets and data-generating relationships change. |
| D | False (accurate) | Monitoring can support thresholds for review, fallback, or retraining when behavior deteriorates, making degradation actionable — accurate. |
| E | False (accurate) | A simpler fallback model can be valuable during failures even if it is not the top performer in normal conditions — accurate. |

**Reference:** Regime-segmented evaluation, robustness vs. average performance, monitoring/fallback — ISLR §2.2; concept "non-stationarity, production monitoring, graceful degradation."

### [ML-D10G7Q2] Deep tree vs. bagged ensemble — stability at equal average error
**Scenario:** A deep tree and a bagged-tree ensemble have similar average validation error, but across nearby time windows and small input perturbations the single tree varies much more while the ensemble stays consistent; the production owner values predictable exposures.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The ensemble's lower sensitivity is relevant even at similar average error — prediction variability affects turnover, exposure, and operational confidence. |
| B | True | Bagging reduces variance by averaging unstable component predictions, dampening sample-specific tree behavior. |
| C | False | Similar average error does not prove identical trading risk; models with equal mean error can differ in tails, turnover, and sensitivity. |
| D | True | Small-perturbation tests provide evidence about local stability — whether modest input changes cause disproportionate output changes. |
| E | True | Stability considerations can justify choosing the ensemble; production suitability includes reliability beyond mean accuracy. |

**Reference:** Bagging variance reduction, stability vs. average accuracy — ISLR ch.8; ESL ch.15; concept "prediction stability / turnover in production."

### [ML-D10G7Q3] Unstable monthly-retrained factor model
**Scenario:** A factor model is retrained monthly and its selected features and coefficients change dramatically each time even though headline validation scores stay similar. The model-risk lead asks whether this instability should be investigated before clients rely on the allocations.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Similar validation scores do not rule out unstable behavior — different models can score alike while producing materially different outputs. |
| B | True | Large month-to-month changes may indicate correlated features, limited data, or regime sensitivity — each can shift fitted relationships across samples. |
| C | True | Comparing portfolio turnover and exposure changes reveals the practical consequences of instability (costs and risk). |
| D | False | Retraining more often does not necessarily increase stability; more frequent fitting can amplify sensitivity to short-term sample changes. |
| E | True | Stability analysis should consider both predictions and the downstream decisions the system makes with them. |

**Reference:** Coefficient instability under collinearity/limited data, decision-level impact — ISLR ch.6 (collinearity, selection stability); concept "model-risk stability analysis."

### [ML-D10G8Q1] Choosing among linear, KNN, tree (thresholds + speed + inspectable) — INVERTED logic
**Scenario:** A PM must pick among linear regression, KNN, and a decision tree for a medium-sized return dataset where the relationship may contain thresholds, inference must be fast, and the committee wants an inspectable model. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Linear regression offers fast inference and transparent coefficients but may miss unengineered threshold effects — an accurate match to its strengths/limits. |
| B | False (accurate) | A decision tree represents thresholds and gives inspectable rules, subject to complexity limits (pruning/depth) — accurate. |
| C | True (incorrect) | Flawed: KNN does **not** provide a compact global equation — its predictions depend on local stored examples, not one fitted equation. |
| D | False (accurate) | No learner is universally best across the stated objectives; each offers a different balance of structure, speed, and interpretability — accurate (no free lunch). |
| E | False (accurate) | Representative validation plus operational tests should inform the final choice — both predictive and deployment evidence are needed — accurate. |

**Reference:** Comparative model properties (linear/tree/KNN), no-free-lunch — ISLR §2.1.3, §2.2.3, ch.8; scikit-learn "Choosing the right estimator."

### [ML-D10G8Q2] KNN best on a small validation set vs. stable linear model — INVERTED logic
**Scenario:** On a nonlinear signal, KNN performs best on a small validation set, a tree is close behind, and a linear model is slightly worse but far more stable across time splits. The CIO wants the winner named immediately. Identify the flawed claims.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | A single validation ranking may be uncertain because a small evaluation set is subject to sampling variation — accurate. |
| B | False (accurate) | Stability across time splits is relevant evidence for a trading model, since market relationships and samples vary through time — accurate. |
| C | True (incorrect) | Flawed: KNN need **not** be selected — the lowest observed error does not always identify the true best model; the lead may be noise and ignores other constraints. |
| D | False (accurate) | The linear model's stability may justify selection if the small accuracy difference is unreliable or operationally unimportant — accurate. |
| E | False (accurate) | Models should be compared using consistent splits and metrics; consistency is necessary for a fair comparison — accurate. |

**Reference:** Validation-set variance, model comparison under small samples, stability — ISLR ch.5 (cross-validation, resampling); ESL ch.7.

### [ML-D10G8Q3] Recommend a system improvement, not a "best" algorithm
**Scenario:** A desk summarizes its options: linear is fast/stable but underfits; a deep tree fits nonlinearities but is unstable; KNN is accurate offline but too slow with the full dataset. The research director wants a recommendation that improves the system rather than crowning one algorithm.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Feature engineering can improve the linear model (capturing more structure) while retaining its fast serving pattern. |
| B | True | Restricting tree depth or using a bagged-tree ensemble can address variance/instability concerns, though each introduces its own tradeoffs. |
| C | True | Reducing or restructuring KNN's reference data can improve latency but alters neighbor quality, so accuracy must be re-validated. |
| D | False | Each model having a weakness does not mean none can be deployed; practical selection manages tradeoffs rather than requiring perfection. |
| E | True | The best choice achieves an acceptable balance under the desk's measured predictive, operational, and governance constraints. |

**Reference:** Practical tradeoff management, feature engineering, complexity control, no-free-lunch — ISLR §2.1.3, ch.6, ch.8; concept "constraint-driven model selection."

## References (domain-level)

1. **ISLR — *An Introduction to Statistical Learning* (James, Witten, Hastie, Tibshirani):** §2.1.3 (flexibility–interpretability tradeoff), §2.2 (assessing accuracy, bias–variance, overfitting, non-stationarity), §2.2.3 (KNN and inference cost), ch.3 (linear regression, outliers/leverage, collinearity), ch.5 (cross-validation/resampling), ch.6 (subset selection, regularization), ch.8 (trees, pruning, bagging, random forests).
2. **ESL — *The Elements of Statistical Learning* (Hastie, Tibshirani, Friedman):** ch.7 (model assessment & selection), ch.8/ch.15 (bagging, ensembles, variance reduction), ch.10 (robust loss functions).
3. **scikit-learn User Guide:** "Choosing the right estimator" (task→model), "Nearest Neighbors" (query complexity/memory), "Preprocessing" (feature scaling for distance-based models), "Computational performance" (train vs. inference latency, throughput), "Model interpretation."
4. **Concept — No-Free-Lunch theorem & Occam's razor:** no learner is best across all problems; prefer the simplest model adequate to the data and constraints.
5. **Concept — Deployment constraints (latency, throughput, memory, tail latency) and model risk management:** realized vs. offline performance, regime-segmented evaluation, stability/robustness monitoring, graceful-degradation fallbacks.
6. **Grinold & Kahn — *Active Portfolio Management*:** linking predictive signal to net-of-cost portfolio outcomes (turnover, exposure stability, transaction costs) for the production-suitability questions.
