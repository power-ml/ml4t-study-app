# ML Domain 7 — Ensemble Methods

## Domain cheat-sheet

- **Why ensembles work**: combining multiple models by aggregation (averaging for regression, voting for classification) can produce more accurate *and* more stable predictions than any single model — but only under conditions, never as a guarantee.
  - **Error cancellation requires imperfectly correlated errors.** If members make *different* mistakes, errors partly cancel in the average. Perfectly correlated (identical) members give no diversity benefit.
  - **No observation-by-observation guarantee.** An ensemble improves *expected* performance; it is not guaranteed to beat its best member (or every member) on any given future point or regime.
  - **Shared systematic bias survives aggregation.** If every learner has the same directional error, averaging preserves it. "Wisdom of the crowd" still requires out-of-sample testing.
  - Combining weak/unstable learners can beat repeatedly picking one learner; the **aggregation rule matters** (mean, median, weighted vote all differ).
- **Bagging (bootstrap aggregating)** — G2:
  - A **bootstrap sample** draws N rows *with replacement* from the original N observations → some rows repeat, some are absent. Duplicated rows keep their original features and target (never relabeled/permuted).
  - On average a bootstrap sample contains ~**63%** unique rows; the ~**37% "out-of-bag" (OOB)** rows give a free, built-in validation estimate (evaluate each row only on trees that never saw it).
  - Bagging **reduces variance** of high-variance, low-bias learners → use **deep, unconstrained trees**. Averaging *shallow* high-bias trees reduces variance a little but leaves the systematic error intact (does not reduce bias).
  - Bootstrap resampling promotes variation but does **not** guarantee independent errors — shared data/features keep trees correlated (a dominant feature becomes the root split in nearly every tree), which limits variance reduction.
- **Random forests** — G3:
  - Add **feature randomness**: at each split only a random subset of candidate features is considered. This **decorrelates** trees beyond what bootstrap sampling alone achieves.
  - Trees do not use disjoint feature sets; subsets are re-drawn per split and features recur across trees. Predictions are still **aggregated** (averaging/voting).
  - **Tradeoff (candidates per split, "mtry")**: fewer candidates → weaker individual trees but more diversity; using *all* features → collapses back to ordinary bagged trees. Fewer candidates does **not** guarantee lower test error — tune and validate.
- **Diversity among learners** — G4:
  - What matters is **behavioral diversity** (errors on different observations), not model count, file count, or different algorithm *names*. A linear model + KNN + tree can still share blind spots (e.g., same crisis dates) and produce correlated errors.
  - Diversity helps **only if** the diverse learners retain predictive skill; injecting random/uninformative predictions degrades the aggregate.
  - Standalone quality ≠ ensemble contribution — a lower-Sharpe but complementary model can add more incremental value than a top model highly correlated with existing members. Assess with **out-of-sample residual/prediction correlation**, not in-sample fit alone.
- **Boosting intuition** — G5 (conceptual only):
  - **Sequential**: each new (typically shallow) learner is trained to address the errors the current ensemble has not captured (residuals) or reweights hard/misclassified examples. Final prediction is an **additive, weighted** combination scaled by a **learning rate (shrinkage)**.
  - Differs from bagging: bagged learners are trained **independently** (parallelizable); boosting stages **depend on** prior stages (sequential, not parallel).
  - Boosting can **reduce bias** by adding corrections that expand effective capacity; weak learners combine into an expressive nonlinear model. But a mislabeled/noisy example can look persistently "hard" and attract harmful excess focus.
- **Bias vs. variance in ensembles** — G6:
  - Bagging unstable deep trees → **variance reduction** (stability across retraining samples). Boosting shallow underfit learners → **bias reduction**.
  - Reduced variance does **not** imply unbiased: stability (consistency across samples) and accuracy (closeness to truth) are distinct properties. Averaging identical predictions changes nothing; averaging cannot create signal absent from every member.
- **Failure modes** — G7:
  - **Correlated base learners**: near-identical trees fail together; large member count ≠ diversification; a regime shift can expose a weakness shared by all.
  - **Leakage-driven gains**: look-ahead / point-in-time leakage inflates validation; averaging many leaked models cannot repair invalid temporal availability and instead creates *false confidence* through correlated optimism. Reconstruct features as-of each prediction timestamp.
  - **Overfitting in boosting**: training error → 0 while validation peaks early then deteriorates (memorization of noise). Use time-aware validation / early stopping / learning-rate / depth controls; zero training error ≠ smallest future loss.
  - Averaging systematically low estimates stays systematically low; use **regime/segment stress testing** to reveal concentrated failures average metrics hide.

## Common traps

- **Inverted-logic questions (8 of 24):** the Answer Key reads "**True = incorrect; False = accurate**," so a verdict of **False means the statement is correct**. Read the polarity line first. Inverted here: **G1Q2, G1Q6, G2Q2, G3Q2, G4Q2, G5Q2, G6Q1, G7Q2.**
- **Double-negative "embedded claim" choices** that begin **"The following claim is false: ..."**: judge the inner claim's truth, then negate ("says X is false"), then apply the question's polarity. Appears in **G2Q2A, G3Q2A, G3Q3A, G7Q3A**. Example: G3Q3A embeds an *accurate* claim, so "the following claim is false" is itself inaccurate → verdict **False** (normal polarity). G2Q2A/G3Q2A embed accurate claims inside *inverted* questions, so the choice is incorrect → verdict **True (incorrect)**.
- **"Averaging fixes everything" fallacy:** aggregation cannot remove shared systematic bias, cannot repair look-ahead leakage, and cannot recover signal absent from every member. Recurs in G1Q1C, G4Q2C, G6Q1C, G7Q1B, G7Q3C.
- **Bag deep, not shallow:** bagging wants high-variance/low-bias base learners (deep trees). "Bag shallow max_depth=1–2 trees" is a distractor (G1Q6D) — that leaves high bias untouched.
- **OOB is ~37%, not one-third precisely, and it validates without a holdout** (G1Q6C) — the "one-third" phrasing is treated as incorrect wording in the inverted question.
- **Member count ≠ diversity ≠ independence:** more trees never guarantees zero variance (G2Q2D), never guarantees an unbiased estimate (G7Q3C), and identical/duplicate models add no information (G4Q1B, G1Q5C).

## Questions

### [ML-D7G1Q1] Motivation — averaging correlated regression trees
**Scenario:** A PM has five independently trained regression trees for next-day returns that are each moderately accurate but unstable across samples, and asks whether averaging their forecasts stabilizes position sizing without changing the universe.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Imperfectly correlated errors partially cancel in an average, so aggregation reduces prediction variance — the core variance-reduction argument for bagging/averaging. |
| B | False | An ensemble improves *expected* performance but carries no observation-by-observation guarantee to beat its best member on every future point. |
| C | True | A shared systematic directional bias does not disappear under averaging; only the uncorrelated (variance) component cancels. |
| D | True | Combining unstable learners can yield a more reliable aggregate than repeatedly selecting one learner, even when no single tree is consistently best. |
| E | False | Averaging uses all five outputs; it is not equivalent to selecting the single deepest tree's prediction. |

**Reference:** Bagging / averaging for variance reduction — ISLR ch.8 (§8.2 bagging); concept "error cancellation requires imperfect correlation."

### [ML-D7G1Q2] Majority-vote ensemble — INVERTED logic
**Scenario:** A desk combines three classifiers voting "buy," "buy," "do not buy" and wants a rule less dependent on any single model while keeping low latency. Mark each statement True if it is *incorrect*.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: two of three votes support "buy," so a majority-vote ensemble issues "buy." |
| B | True (incorrect) | Wrong: majority voting does NOT ensure correctness whenever one member is right — a correct minority can be overruled by two incorrect members. |
| C | False (accurate) | Correct: other members can outvote an isolated idiosyncratic error, reducing dependence on one learner. |
| D | False (accurate) | Correct: perfectly aligned (identical) predictions provide no diversity, so voting offers little error-cancellation benefit. |
| E | True (incorrect) | Wrong: an ensemble does not require more features than its members — multiple learners may share the same feature set. |

**Reference:** Majority voting and diversity — ISLR ch.8; scikit-learn "Ensemble methods: Voting Classifier."

### [ML-D7G1Q3] "Weak → strong" claim and aggregation quality
**Scenario:** A risk committee compares one highly tuned tree with an ensemble of many modest trees for drawdown risk; the CRO questions whether "many weak models must always become one strong model" while valuing stability across retraining.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Members with useful signal and partly different errors yield a more stable aggregate — the legitimate version of the "wisdom of crowds" claim. |
| B | False | Adding worse-than-random members that make the *same* errors can damage the ensemble; correlated poor learners do not "must improve" it. |
| C | True | The aggregation rule (mean, median, weighted vote) affects the final prediction, so it is part of ensemble design. |
| D | True | A single model can beat an ensemble when added learners contribute noise or shared systematic error — more models ≠ better generalization. |
| E | False | "Wisdom of the crowd" does not remove the need for out-of-sample evaluation; ensemble performance must still be tested on unseen data. |

**Reference:** Limits of aggregation & aggregation rules — ISLR ch.8; ESL ch.16 (ensemble learning).

### [ML-D7G1Q4] Motivation for replacing a single tree with an ensemble
**Scenario:** As Head of Quant Research you must explain ensemble motivation to a PM (who sees extra trees as needless compute) and a CRO (who expects better reliability in volatile markets).
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The primary motivation is that combining models often yields more accurate and stable predictions than a single learner (robustness). |
| B | True | Ensembles help even when individual models err, provided the errors are not perfectly correlated so they can partly cancel. |
| C | False | A tree that is best on *training* data is not guaranteed to generalize best; ensembles often outperform it out-of-sample by reducing variance — no "guaranteed worse" result. |
| D | True | Different models (or differently trained versions) capture complementary patterns; combining these perspectives is a key motivation. |
| E | False | Ensembles aim to improve performance/robustness, not to reduce required training data — they typically add computation on the same dataset. |

**Reference:** Motivation for ensembles — ISLR ch.8 (§8.2); concept "accuracy + robustness vs. single learner."

### [ML-D7G1Q5] Statistical advantage vs. mere complexity
**Scenario:** Presenting to an Investment Committee, one team wants a single interpretable tree and another an ensemble of many trees; the committee asks whether combining models is only added complexity or a real statistical advantage.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | When individual models make different errors, aggregating predictions reduces overall error and improves generalization. |
| B | False | The motivation is improved performance/robustness, not interpretability — ensembles are usually *less* interpretable than a single model. |
| C | True | Identical models that make exactly the same errors provide little improvement; diversity is a key ingredient. |
| D | True | Averaging across models yields more stable predictions, less sensitive to a single training sample's peculiarities. |
| E | False | No guarantee an ensemble beats every individual model; it depends on base-learner quality, diversity, and method suitability. |

**Reference:** Statistical rationale for ensembles — ISLR ch.8; scikit-learn "Ensemble methods" overview.

### [ML-D7G1Q6] Bagging mechanics (bootstrap, correlation, OOB) — INVERTED logic
**Scenario:** A team moves from a single decision-tree classifier to a bagged ensemble of 300 unconstrained trees for futures direction; a junior analyst asks how bootstrap sampling, tree correlation, and OOB validation improve signal stability. Mark each statement True if it is *incorrect*.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: deep trees have low bias but high variance; averaging hundreds of them cancels sample-specific noise and lowers variance. |
| B | False (accurate) | Correct: each tree uses a bootstrap sample — N observations drawn with replacement from the original N. |
| C | False (accurate) | Correct: each bootstrap sample leaves ~37% out-of-bag, and those rows give a built-in cross-validation check without a separate holdout. |
| D | True (incorrect) | Wrong: bagging wants deep, low-bias trees; pruning to max_depth 1–2 keeps high bias that averaging cannot remove — shallow trees are *not* the right base learner. |
| E | False (accurate) | Correct: a dominant feature becomes the root split in nearly every tree, keeping trees correlated and limiting bagging's variance reduction. |

**Reference:** Bagging, OOB error, tree correlation — ISLR ch.8 (§8.2.1 bagging, OOB error); ESL §15 (random forests / OOB).

### [ML-D7G2Q1] Bootstrap sampling with replacement
**Scenario:** An asset manager builds 100 trees, each on 10,000 rows drawn with replacement from 10,000 trading days, then averages forecasts; a junior analyst asks why some days repeat and others are absent.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Sampling with replacement returns each drawn row to the pool, so the same row can appear multiple times in one sample. |
| B | False | A 10,000-draw bootstrap need not contain all 10,000 distinct rows — repeats imply omissions (~37% omitted on average). |
| C | True | Different sampled observations change chosen splits and structure, so a deterministic algorithm still yields different fitted trees. |
| D | True | Averaging is aimed primarily at reducing the variance of an unstable base learner such as a decision tree. |
| E | False | Bagging does not permute targets; features and their correct targets must stay paired. |

**Reference:** Bootstrap resampling — ISLR ch.8 (§8.2.1); ch.5 (§5.2 the bootstrap).

### [ML-D7G2Q2] Bootstrap does not guarantee independent errors — INVERTED logic
**Scenario:** A quant bags several deep regression trees but they still respond similarly in volatile markets; the PM claims different bootstrap samples make errors independent so they cancel completely. Mark each statement True if it is *incorrect*.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Embedded double negative: the choice asserts "the claim [different bootstrap samples do not guarantee independent errors] is false." That inner claim is actually accurate (resampling promotes variation but not statistical independence), so asserting it is false is incorrect. |
| B | False (accurate) | Correct: shared market features and overlapping observations keep predictions correlated. |
| C | False (accurate) | Correct: strongly positively correlated errors reinforce rather than cancel, giving less variance reduction than weakly correlated errors. |
| D | True (incorrect) | Wrong: adding more *highly correlated* trees does not drive ensemble variance to zero — a shared correlated component remains even in a large ensemble. |
| E | False (accurate) | Correct: measuring correlation among out-of-sample residuals directly assesses error diversity. |

**Reference:** Correlation limits on bagging variance reduction — ESL §15.2 (random forests, variance of an average of correlated variables); ISLR ch.8.

### [ML-D7G2Q3] Disjoint partitions vs. bootstrap; rare-class representation
**Scenario:** A compliance system bags classifiers to flag suspicious orders; the team proposes training each model on a disjoint one-tenth of the data to "make models independent," while compliance worries rare manipulation examples vanish from subsets.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Standard bagging draws with-replacement bootstrap samples from the *full* training set, not mutually exclusive partitions. |
| B | True | A one-tenth disjoint partition exposes each learner to far fewer observations than a full-size bootstrap sample. |
| C | False | Bootstrap sampling does not guarantee every rare positive appears in every learner's sample — any observation may be absent. |
| D | True | Stratified or otherwise controlled sampling can address rare-class representation when handled consistently and evaluated properly. |
| E | False | A duplicated row retains its original features and target; bagging never changes the observed label. |

**Reference:** Bagging vs. data partitioning; class imbalance — ISLR ch.8 (§8.2.1); scikit-learn "Ensemble methods: Bagging," "Imbalanced learning" (stratified sampling).

### [ML-D7G3Q1] Random-feature selection to decorrelate trees
**Scenario:** Bagged trees keep choosing recent momentum as the root split because it is strongest; the director suggests a random forest that considers only a random subset of features at each split so trees are not near-identical.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Restricting candidates at a split can force some trees to use alternative predictive features when momentum is unavailable. |
| B | True | Feature randomness is intended to increase diversity, decorrelating trees beyond bootstrap sampling alone. |
| C | False | Trees need not use disjoint feature sets; random subsets are re-drawn per split and features recur across trees. |
| D | True | Reducing correlation among useful trees improves the variance-reduction benefit of aggregation. |
| E | False | A random forest aggregates its trees' predictions by averaging or voting — it does not combine them without using predictions. |

**Reference:** Random forests / feature subsampling — ISLR ch.8 (§8.2.2); ESL §15.

### [ML-D7G3Q2] Forest vs. single tree — individual vs. collective strength — INVERTED logic
**Scenario:** A 300-tree random forest beats one deep tree on validation accuracy and stability; the PM asks whether this proves every tree is individually better than the original. Mark each statement True if it is *incorrect*.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Embedded double negative: the choice asserts "the claim [the forest can outperform even if many members are individually weaker] is false." That inner claim is accurate (collective error cancellation can outweigh weaker members), so asserting it false is incorrect. |
| B | False (accurate) | Correct: bootstrap and feature randomness both alter the data/splits seen, making member trees differ. |
| C | False (accurate) | Correct: aggregation reduces sensitivity to any one tree's unstable structure, so the aggregate can be more stable than any single deep tree. |
| D | True (incorrect) | Wrong: good validation accuracy does not prove outperformance in *every* future regime — validation is evidence, not a guarantee. |
| E | False (accurate) | Correct: a consistent, time-aware evaluation design for both models is needed for a meaningful comparison. |

**Reference:** Random forest generalization vs. single tree; time-aware validation — ISLR ch.8; ESL §15.3.

### [ML-D7G3Q3] Candidate-features-per-split tradeoff
**Scenario:** A low-latency desk tunes a random forest: considering fewer features per split slightly lowers individual-tree accuracy but reduces correlation; considering all features resembles ordinary bagging and barely changes training time.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded double negative: the choice asserts "the claim [lower individual-tree accuracy can be acceptable if diversity improves the aggregate] is false." The inner claim is accurate, so calling it false is inaccurate → False. Ensemble quality depends on both member strength and error correlation. |
| B | True | Considering all available features at every split removes the random-feature component, leaving only bootstrap variation (i.e., bagging). |
| C | True | The number of candidate features per split is a genuine tradeoff between tree strength and diversity. |
| D | False | Fewer candidate features does not guarantee lower test error — the best setting is data-dependent and must be validated. |
| E | True | Inference cost and latency grow with the number of trees (more split traversals and aggregation at prediction time). |

**Reference:** mtry tradeoff and inference cost — ISLR ch.8 (§8.2.2); ESL §15.3; scikit-learn "RandomForest max_features."

### [ML-D7G4Q1] Which ensemble benefits more from averaging
**Scenario:** A committee compares Ensemble A (five near-identical trees making the same mistakes) with Ensemble B (useful models erring on different observations) and asks which benefits more from averaging.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Ensemble B's different error patterns give more opportunity for errors to cancel. |
| B | False | Five nearly identical files do not confer five independent information sources; duplicates add little. |
| C | True | Diversity helps only when the diverse learners retain predictive skill; otherwise it just injects noise. |
| D | False | Deliberately adding random, uninformative predictions can degrade, not improve, Ensemble B. |
| E | True | Comparing out-of-sample prediction/residual correlations helps distinguish which ensemble has genuine diversity. |

**Reference:** Diversity and error correlation — ESL ch.16; concept "duplicate models add no information."

### [ML-D7G4Q2] Architecture labels vs. behavioral diversity — INVERTED logic
**Scenario:** A manager combines a linear model, KNN, and a tree; the CIO likes the architectural differences, but validation shows all three err badly on the same crisis dates none was trained on. Mark each statement True if it is *incorrect*.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: different algorithm names do not guarantee diverse errors — distinct methods may learn similar signals or fail on the same cases. |
| B | False (accurate) | Correct: shared blind spots (a common regime gap) create correlated errors and limit crisis protection. |
| C | True (incorrect) | Wrong: averaging does NOT eliminate an error all three make in the same direction — a shared directional error survives aggregation. |
| D | False (accurate) | Correct: diversity should be judged by out-of-sample behavior/errors, not architecture labels alone. |
| E | False (accurate) | Correct: a model that behaves differently on crisis dates *and* generalizes can improve robustness by addressing the common weakness. |

**Reference:** Behavioral vs. nominal diversity; correlated errors — ESL ch.16; concept "shared blind spots survive averaging."

### [ML-D7G4Q3] Standalone quality vs. complementarity in weighting
**Scenario:** A team assigns ensemble weights: one model has the best standalone Sharpe but is highly correlated with two members; another has lower Sharpe but forecasts well when the others fail. Balance individual quality against complementarity.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Standalone performance alone is insufficient — marginal value depends on interaction with existing members. |
| B | True | The lower-Sharpe model can add more incremental value through complementary (uncorrelated) errors. |
| C | False | Concentrating all weight on the top model discards diversification and can overfit model selection — not an out-of-sample maximizer. |
| D | False | Choosing weights on in-sample fit alone is unsafe; in-sample correlations may be optimistic or unstable. |
| E | True | Validation should compare whether weighting schemes improve the *aggregate*, the object actually deployed. |

**Reference:** Ensemble weighting, diversification vs. concentration — Grinold & Kahn (combining signals / information ratio); ESL ch.16.

### [ML-D7G5Q1] Boosting on residuals with a learning rate
**Scenario:** A quant builds a sequence of shallow regression trees where each new tree addresses remaining errors, and the lead explains the final forecast adds tree contributions using a learning rate.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Boosting trains later trees on information about earlier trees' errors, focusing on what the current ensemble missed. |
| B | True | This sequential dependence differs from bagging, where base learners can be trained independently. |
| C | False | The first tree need not perfectly fit the targets — remaining error is exactly what later learners reduce. |
| D | True | A smaller learning rate (shrinkage) makes each new tree's correction more conservative. |
| E | False | Regression boosting forms an additive, weighted prediction, not an unweighted majority vote. |

**Reference:** Boosting / gradient boosting, shrinkage — ISLR ch.8 (§8.2.3 boosting); ESL ch.10.

### [ML-D7G5Q2] Reweighting hard cases vs. duplicating live data — INVERTED logic
**Scenario:** A fraud desk uses a boosted classifier; after early models miss rare manipulative orders, later learners emphasize hard/misclassified cases. Compliance asks whether that means those cases are duplicated at prediction time. Mark each statement True if it is *incorrect*.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: boosting can shift training attention toward examples the current ensemble handles poorly (some methods reweight, others fit residuals). |
| B | False (accurate) | Correct: emphasizing hard examples is a *training* mechanism; live predictions use the learned ensemble and need not alter incoming data. |
| C | True (incorrect) | Wrong: later learners are not exact independent copies of the first — they respond to the current ensemble's weaknesses. |
| D | False (accurate) | Correct: a mislabeled example can look persistently hard, attract increasing attention, and become harmful. |
| E | True (incorrect) | Wrong: boosting and bagging do not share the same logic — standard bagging trains learners independently on resampled data. |

**Reference:** Boosting reweighting vs. residual fitting; noise sensitivity — ESL ch.10 (AdaBoost / gradient boosting); ISLR ch.8.

### [ML-D7G5Q3] Bagging vs. boosting under a compute budget
**Scenario:** A PM compares a bagged-tree model (trains in parallel, stabilizes estimates) with a boosted-tree model (trains sequentially, progressively refines) under a fixed compute budget.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Bagging parallelizes naturally because base learners are fit separately; boosting stages depend on the current model. |
| B | True | Boosting reduces systematic error by building corrections to the current ensemble (bias reduction). |
| C | False | Fitting residuals of earlier trees characterizes boosting, not bagging — bagged trees do not depend on prior trees. |
| D | True | Boosting can use shallow weak learners whose combined additive output is expressive and nonlinear. |
| E | False | The methods differ in sampling, fitting, and aggregation, so equal tree counts do not force identical forecasts. |

**Reference:** Bagging vs. boosting (parallel vs. sequential, variance vs. bias) — ISLR ch.8 (§8.2); ESL ch.10 & §15.

### [ML-D7G6Q1] Variance reduction vs. residual bias — INVERTED logic
**Scenario:** A deep tree retrained on slightly different samples shows large forecast swings; a bagged ensemble is much more consistent, yet both keep underestimating returns after major policy announcements. Mark each statement True if it is *incorrect*.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: large prediction changes from small sample changes indicate high variance. |
| B | False (accurate) | Correct: bagging reduces the aggregate's sample sensitivity by smoothing learner-specific fluctuations. |
| C | False (accurate) | Correct: the persistent underestimation is a systematic bias that averaging similar trees may not remove. |
| D | True (incorrect) | Wrong: reduced variance does NOT guarantee an unbiased ensemble — bias and variance are distinct; improving one need not zero the other. |
| E | False (accurate) | Correct: stability across retraining and accuracy vs. true targets are different properties (a consistently wrong model can be stable). |

**Reference:** Bias-variance decomposition in ensembles — ISLR §2.2 & ch.8; ESL ch.7.

### [ML-D7G6Q2] Underfit shallow trees cannot recover missing structure
**Scenario:** A desk averages 200 heavily constrained shallow trees that each predict nearly the same value everywhere, expecting the large ensemble to recover nonlinear structure no member learned.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Averaging reduces variance but cannot create signal absent from every underfit member. |
| B | True | Strongly underfit base learners give the ensemble high bias. |
| C | False | Merely adding more identical shallow trees preserves, not eliminates, the shared bias. |
| D | True | Boosting weak learners can reduce bias via sequential corrections (subject to tuning and data quality), expanding effective capacity. |
| E | False | Out-of-sample evaluation is still required; ensemble size does not replace generalization testing. |

**Reference:** High-bias ensembles; boosting for bias reduction — ISLR ch.8; ESL ch.10 & §7.

### [ML-D7G6Q3] Matching interventions to bias vs. variance
**Scenario:** A governance team compares bagging unstable deep trees, boosting underfit shallow trees, and averaging many copies of one deterministic linear model on identical data, asking which addresses variance, which bias, and where benefits are limited.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Bagging unstable deep trees is plausibly aimed at variance reduction (resampling + aggregation stabilizes them). |
| B | True | Boosting shallow learners can reduce bias by building a more expressive combined model. |
| C | False | Averaging identical predictions from a deterministic model does not change the prediction — the average of identical values is that value. |
| D | True | If every member shares the same omitted-variable error, aggregation may leave that common systematic error intact. |
| E | False | Bias/variance behavior cannot be inferred from training error alone; generalization needs out-of-sample evidence. |

**Reference:** Ensemble interventions vs. bias-variance — ISLR §2.2 & ch.8; ESL ch.7, ch.10.

### [ML-D7G7Q1] Look-ahead leakage cannot be averaged away
**Scenario:** An ensemble shows spectacular validation using a "revised earnings" feature; an audit finds the feature used values released *after* each predicted date, and the CIO argues averaging many models should protect the result.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Future-released values give models information unavailable at trade time, so reported performance may be leakage-driven. |
| B | False | Averaging many leaked models cannot make future-released information valid at the historical prediction time. |
| C | True | If all members exploit the same leaked feature, their agreement is correlated optimism — false confidence, not independent confirmation. |
| D | True | The feature must be reconstructed using only point-in-time values available as of each prediction timestamp. |
| E | False | Unexpectedly strong results make data-provenance/leakage auditing *more* important, not unnecessary. |

**Reference:** Look-ahead / point-in-time leakage in backtests — López de Prado, *Advances in Financial ML* (leakage, purged CV); concept "aggregation cannot repair invalid data."

### [ML-D7G7Q2] Boosting overfitting and early stopping — INVERTED logic
**Scenario:** A boosted model adds trees until training error is near zero; validation peaks at ~80 trees then deteriorates (especially around noisy news), yet the PM wants the 600-tree endpoint because it fits history best. Mark each statement True if it is *incorrect*.
**Answer polarity:** Inverted (True = incorrect; False = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: falling training error alongside worsening validation is classic overfitting — added fit is not transferring to unseen data. |
| B | False (accurate) | Correct: later boosting stages may focus excessively on persistent noisy/outlier cases. |
| C | False (accurate) | Correct: choosing the number of stages via time-aware validation improves generalization without relying on final training fit. |
| D | True (incorrect) | Wrong: zero training error does NOT guarantee the smallest future loss — perfect historical fit can reflect memorization. |
| E | False (accurate) | Correct: learning rate, tree depth, and early stopping regularize the size/aggressiveness of sequential corrections. |

**Reference:** Boosting overfitting, early stopping, regularization — ESL ch.10 (§10.12 regularization, shrinkage); ISLR ch.8 (boosting tuning).

### [ML-D7G7Q3] Member count ≠ diversification; regime failure
**Scenario:** A risk ensemble of 50 trees trained on nearly identical samples with the same dominant features all underestimate transaction costs during a sudden liquidity regime change, though the risk officer assumed the large count guaranteed diversification.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Embedded double negative: the choice asserts "the claim [a large number of members does not guarantee meaningful diversity] is false." The inner claim is accurate (effective diversity is about behavior/errors, not count), so calling it false is inaccurate → False. |
| B | True | Highly correlated errors survive aggregation, so the full ensemble can fail together. |
| C | False | Averaging 50 systematically low estimates stays systematically low — it does not produce an unbiased cost estimate. |
| D | True | A regime shift exposes a weakness shared by every learner because their training experience (data and features) was similar. |
| E | True | Regime/segment stress testing reveals concentrated failures that average validation metrics can hide. |

**Reference:** Correlated-learner failure modes; regime stress testing — ESL §15.2 (correlation limits); concept "member count ≠ diversification," López de Prado (backtest stress by regime).

## References (domain-level)

1. **ISLR — *An Introduction to Statistical Learning* (James, Witten, Hastie, Tibshirani):** ch.8 (§8.2 tree-based ensembles: §8.2.1 bagging & out-of-bag error, §8.2.2 random forests / feature subsampling, §8.2.3 boosting & shrinkage), §2.2 (bias-variance tradeoff), ch.5 (§5.2 the bootstrap).
2. **ESL — *The Elements of Statistical Learning* (Hastie, Tibshirani, Friedman):** ch.10 (boosting, AdaBoost, gradient boosting, regularization/shrinkage), §15 (random forests; variance of an average of correlated variables, OOB), ch.16 (ensemble learning, diversity), ch.7 (model assessment, bias-variance).
3. **scikit-learn User Guide — "Ensemble methods":** Bagging, Random Forests / Extra-Trees (`max_features`), Voting Classifier/Regressor, Gradient Boosting / HistGradientBoosting (learning rate, early stopping), plus "Imbalanced learning" (stratified sampling) and OOB scoring.
4. **Breiman:** "Bagging Predictors" (1996) and "Random Forests" (2001) — original bootstrap-aggregation and feature-randomness results; bias-variance framing of variance reduction.
5. **López de Prado — *Advances in Financial Machine Learning*:** data leakage / point-in-time features, purged & embargoed cross-validation, and regime-aware backtest evaluation — for the failure-mode questions (leakage, overfitting, correlated-learner regime failure).
6. **Concept references:** bagging vs. boosting (parallel/variance vs. sequential/bias), bootstrap sampling (~63% unique / ~37% OOB), error decorrelation and the correlation limit on ensemble variance reduction, and diversity-with-skill as prerequisites for aggregation gains.
