# ML Domain 8 — Comparative Strategy Learning & Evaluation

## Domain cheat-sheet

- **Three families of trading-strategy learners.** Keep the paradigms distinct — the exam repeatedly tests whether you can tell them apart:
  - **Supervised (e.g., decision-tree) strategy learner** maps *features → supplied target labels* from a fixed labeled table (one row per date). The label (BUY/HOLD/SELL, a return class, or an "optimal position") *defines what it learns*; it does not interact, take actions, or receive rewards. Change the label construction and the fitted strategy changes even with the same features and algorithm.
  - **Reinforcement learner (e.g., Q-Learner)** steps through a simulator, *chooses actions*, and updates action-values from *reward-bearing transitions* (changes in portfolio value). It learns a policy, not a per-row label; its experience distribution changes as its policy changes.
  - **Manual / rule-based strategy** is a fixed, human-specified state→action rule. It is still a legitimate strategy and *can* be evaluated out-of-sample — provided it is frozen before the test period is seen.
- **Same indicators ≠ same objective, signal, or behavior.** Using identical input features does **not** make two learners equivalent. Labels encode one objective (and its horizon/thresholds/cost assumptions); portfolio rewards encode another (action- and holding-dependent net value). Two systems can reach the *same position* through entirely different objectives and mechanisms, and similar classification accuracy does **not** imply similar trades or returns.
- **Predict-then-trade vs. direct policy learning.**
  - **Predict-then-trade** separates a *forecast model* from an *execution rule* that converts forecasts into positions. You can change the rule (e.g., add a no-trade threshold) **without retraining** the forecaster. Costs can enter via labels, thresholds, objectives, or the execution rule — the architecture is *not* incapable of modeling costs.
  - **Direct policy learning** selects an action (long/short/cash) directly from rewards, with **no intermediate calibrated forecast required**. Transaction-cost consequences can be built into the reward, so inaction (cash) can be the *preferred* learned action when expected moves don't cover costs.
  - **Forecast accuracy ≠ trading utility.** A correctly-signed but economically small forecast can be unprofitable after costs; lower forecast error does **not** guarantee higher net return.
- **Labels, rewards, and credit assignment.** Supervised labels are *targets*; RL rewards are *action-dependent consequences*. A single immediate reward (a costly entry) does not establish an action's long-term value — with a positive discount factor, later rewards propagate back to earlier state-action values (and with discount = 0 **only** the immediate reward counts). Daily rewards do **not** automatically assign long-run consequences perfectly to the causing action — temporal **credit assignment** is an approximation that depends on states, subsequent actions, discounting, and the update rule.
- **Batch vs. interactive learning.** A supervised dataset is assembled *independently* of the model's fitted actions (batch). A Q-Learner's actions change its *simulated holdings/cash/costs* and therefore later rewards (interactive) — even though standard historical replay uses **immutable prices**: simulated orders do not rewrite recorded market data. Replaying one history for many episodes does **not** create independent market samples; the term "interactive" should be qualified by *which* environment variables respond to actions. A fixed price path does not prevent RL updates (they come from simulated state transitions and rewards).
- **In-sample vs. out-of-sample.** Strong *training-period* performance alone is **not** evidence of generalization; a large train-test gap is a warning sign of **overfitting** to the training environment. Always examine both in-sample and out-of-sample results under aligned assumptions. A single out-of-sample result (one period, one directional call) is too noisy to rank designs or declare any approach universally best/impossible.
- **Fair comparison (apples-to-apples).** A meaningful comparison holds the environment constant: **same dates, same costs (commission + market impact), same starting capital and leverage constraints, same information set / feature timing, and the same metric set computed under the same conventions.** Giving portfolio state (holdings) or extra features to only one system, or charging costs to only some strategies, confounds algorithm effects with information/condition effects. A shared **benchmark** (e.g., buy-and-hold) provides context for whether a strategy adds value.
- **Evaluation metrics.** Report a *common set* per strategy, not one cherry-picked dimension each:
  - **Cumulative return** — total growth; sensitive to starting capital and allowed leverage, so compare **percentage** return and match constraints.
  - **Sharpe ratio** — risk-adjusted (return per unit volatility); needed when volatility/leverage differ.
  - **Maximum drawdown** — worst peak-to-trough loss; captures tail/path risk that return alone hides.
  - Ranking Strategy A by return, B by Sharpe, and C by drawdown is **incoherent** — different dimensions are not one comparable scale, and no single metric establishes universal superiority. Strategy preference depends on return, risk, drawdown, costs, and investor objectives.
- **Data snooping / leakage in comparisons.** Selecting manual thresholds (or normalization parameters) after viewing the test period contaminates the evaluation — the test interval must stay unseen until the design is fixed. A feature that includes information unavailable at the decision time (e.g., next-day close used to pick today's close trade) is **leakage**; using the same mathematical formula does not cure it. Using *future outcomes to build training labels* is legitimate **only** when train/test boundaries and timing are handled correctly.
- **Statistical vs. economic significance.** Winning in a majority of windows (11/20) does not by itself establish a reliable or deployable edge — significance depends on **effect size, variability, dependence across windows, and sample design**, and the advantage must survive **transaction costs**. A statistically precise effect can still be too small to matter economically; a positive gross average is **not** automatically significant.

## Common traps

- **Inverted-polarity questions (9 of 21 here).** When the body says "mark each statement True when the stated claim is **incorrect** and False when it is correct," the Answer Key verdict is flipped relative to the statement's truth: **True = the statement is wrong; False = the statement is accurate.** Read the polarity line *first*. Inverted here: **G1Q1, G1Q2, G2Q1, G3Q1, G4Q1, G4Q3, G5Q2, G6Q3, G7Q2.** The remaining 12 are Normal (True = accurate).
- **"Same indicators ⇒ same objective / same strategy."** False — labels and portfolio rewards can encode different objectives, horizons, and cost treatments; identical features do not equalize learning signals or guarantee similar trades.
- **"A direct policy must first produce a return forecast."** False — direct policy learning selects useful actions without an explicit, calibrated forecast; a policy "LONG" is an action, not a numerical return prediction.
- **"Predict-then-trade can't model costs."** False — costs enter via labels, thresholds, the optimization objective, or the execution rule; and changing the execution rule needs no retraining of the forecaster.
- **Forecast accuracy ⇒ profit.** False — correctly-signed but tiny moves lose money after costs; lower forecast error does not guarantee higher net portfolio return.
- **"Zero discount weights later rewards more."** Backwards — with discount = 0 only the *immediate* reward enters the target; later rewards influence earlier values only with a *positive* discount factor.
- **"Daily/immediate reward attributes long-run consequences perfectly."** False — temporal credit assignment is an approximation; an immediate negative reward does not prove negative long-term value.
- **"Historical replay is fully interactive / orders change recorded prices."** False — standard replay uses immutable prices; actions change only simulated holdings, cash, and costs. Sequential decision-making alone does not reproduce live market feedback, and simulator results carry external-validity caveats.
- **"Repeating one history = independent samples."** False — 100 passes over a fixed price path are not 100 independent market samples.
- **"Resetting the portfolio erases learned Q-values."** False — portfolio state and learned parameters are reset or retained independently; a retained Q-table carries knowledge across episodes.
- **Giving holdings/features/costs to only one system is fair if indicators match.** False — equal market indicators do not compensate for unequal access to portfolio state, extra features, or different cost assumptions; such comparisons are confounded.
- **Shared feature *name* ⇒ information-equivalent.** False — different windows or timestamps make nominally identical features materially different; future-dated inputs are leakage even with the same formula.
- **"Manual strategies can't be evaluated out-of-sample" / "normalization guarantees no leakage."** Both false — a frozen manual rule can be tested on unseen data; normalization can itself leak if its parameters use test/future data.
- **Ranking by raw dollar profit or one isolated metric each.** False — ending dollars depend on capital/leverage; and ranking A-by-return, B-by-Sharpe, C-by-drawdown is incoherent. Use a common metric set and a shared benchmark.
- **Statistical ⇒ economic significance (and win-rate ⇒ edge).** False — significance needs effect size and dependence structure; an edge must survive costs; a precise but tiny effect may be economically worthless.
- **"Disagreement ⇒ bugs" and "one correct call ⇒ best design."** Both false — correctly built strategies disagree because their objectives/horizons/signals/state differ; a single noisy outcome cannot rank designs.

## Questions

### [ML2-D8G1Q1] Decision tree vs. Q-Learner — labels vs. reward-bearing interaction
**Scenario:** Two systems use the same indicators. A decision tree is trained on rows labeled buy/hold/sell from future returns; a Q-Learner steps through a market simulator, chooses actions, and receives portfolio-value changes as rewards. Classify each claim.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Supervised tree training learns a mapping from features to supplied target labels — exactly how a labeled dataset is fit. The claim is correct, so the inverted verdict is False. |
| B | False (accurate) | Q-Learning updates action-values from experience tuples that include the action taken and the subsequent reward. The claim is correct, so the verdict is False. |
| C | True (incorrect) | Wrong: shared indicators do not force a shared objective — the tree's labels and the Q-Learner's portfolio rewards can encode different goals and cost treatments. |
| D | False (accurate) | Correct: an exploratory policy deliberately selects a non-greedy action to gather experience, so exploration can pick an action not currently estimated best. |
| E | True (incorrect) | Wrong: a conventional classifier fits fixed labeled rows directly; it does not explore a simulator to learn. |

**Reference:** Balch, *ML4T* — supervised learners vs. Q-Learning (lectures 03-02/03-05) and Project 8 (comparing a manual, supervised, and RL strategy); Sutton & Barto, 2nd ed., ch.1 §1.1 (RL vs. supervised learning; learning from reward/interaction, not labels).

### [ML2-D8G1Q2] Interpreting outputs — return class vs. policy action
**Scenario:** A tree predicts tomorrow's return is positive; a Q-Learner selects LONG for the same state. An analyst treats the two outputs as identical forecasts. Evaluate.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the supervised output's meaning depends on its training target — it may be a return class or a trading label. The verdict is False. |
| B | True (incorrect) | Wrong: LONG is an action / target-position choice, not necessarily a numerical prediction of tomorrow's return. |
| C | False (accurate) | Correct: direct policy learning can choose a useful action without producing an explicit return forecast. |
| D | False (accurate) | Correct: interpreting either output requires knowing how labels, actions, and trades were defined. |
| E | True (incorrect) | Wrong: holding the same position does not imply identical internal learning — different objectives and mechanisms can yield the same action. |

**Reference:** Balch, *ML4T* — Project 8 (what a strategy learner outputs; policy action vs. prediction); Sutton & Barto, 2nd ed., §3.5 (policy as a state→action rule) and ch.1 §1.1 (RL vs. supervised outputs).

### [ML2-D8G1Q3] Reproducibility — rebuilt tree vs. episodic Q-learning
**Scenario:** A decision tree is rebuilt once from a completed labeled dataset; a Q-Learner processes the same interval over many episodes, with later actions influenced by earlier Q-values.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Controlled, deterministic training on unchanged rows (fixed algorithm and seed) can reproduce the same fitted tree. |
| B | True | A changing behavior policy changes which state-action pairs are visited, so the Q-Learner's experience distribution shifts across episodes. |
| C | False | Repetition alone does not guarantee sufficient coverage, stationarity, or convergence to the globally optimal policy. |
| D | False | Conventional supervised splits are chosen from labeled training data, not from discounted TD rewards. |
| E | True | A fair comparison must document training passes, stopping rules, and random seeds, since these affect reproducibility. |

**Reference:** Balch, *ML4T* — reproducibility and seeds in strategy comparison (Project 8); Sutton & Barto, 2nd ed., §6.5 (Q-learning convergence conditions) and ch.2/ch.5 (on-policy experience distribution shifting with the policy).

### [ML2-D8G2Q1] Predict-then-trade vs. direct policy learning
**Scenario:** System P forecasts next-day return and goes long only when the forecast exceeds a configurable threshold. System D directly learns long/short/cash from portfolio rewards. Classify each claim.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: predict-then-trade separates the prediction model from the rule that converts predictions into positions. Verdict False. |
| B | False (accurate) | Correct: the execution threshold can be changed while leaving the fitted forecaster unchanged. |
| C | True (incorrect) | Wrong: a direct policy may select an action without an intermediate calibrated return forecast. |
| D | False (accurate) | Correct: direct policy learning can incorporate transaction-cost consequences through its reward design. |
| E | True (incorrect) | Wrong: lower forecast error does not guarantee higher net return — forecast accuracy and realized trading utility are not the same objective. |

**Reference:** Balch, *ML4T* — predict-then-trade pipelines vs. direct policy learning (Project 6/Project 8); Sutton & Barto, 2nd ed., ch.1 §1.1 and §3.2 (reward encodes action-dependent objective, including costs).

### [ML2-D8G2Q2] Turnover, costs, and the no-trade region
**Scenario:** A supervised model makes many small positive-return forecasts and its rule trades on every one, producing heavy turnover; a cost-aware direct-policy learner stays in cash for many of the same observations.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A statistically correct direction can still fail to find moves large enough to cover transaction costs. |
| B | True | A no-trade region can be added to predict-then-trade by requiring the forecast to exceed a threshold. |
| C | False | Remaining in cash does not prove the learner failed — cash can be the best action when expected opportunities don't justify costs or risk. |
| D | True | Cost-sensitive rewards can make inaction more valuable than marginal trades, explaining the behavioral difference. |
| E | False | Predict-then-trade can reflect costs in labels, thresholds, objectives, or execution rules — not costless by design. |

**Reference:** Balch, *ML4T* — commissions, market impact, and turnover in strategy design (Project 6/Project 8); Sutton & Barto, 2nd ed., §3.2 (cost-sensitive reward shaping action choice).

### [ML2-D8G2Q3] Fair inputs — portfolio state access
**Scenario:** A team compares direct policy learning with a predict-then-trade pipeline but gives current holdings only to the direct learner; the forecaster and its downstream rule are barred from seeing holdings.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | The comparison does not isolate only the learning paradigm — the systems also differ in access to portfolio-state information. |
| B | True | Current holdings affect whether a target exposure requires a costly position change. |
| C | False | Equal market indicators do not compensate for unequal access to decision-relevant portfolio state. |
| D | True | A fairer pipeline could let the execution rule consider current holdings, making the information sets comparable. |
| E | True | Holdings are agent state and often determine which position changes are feasible or costly, so they can influence trading decisions. |

**Reference:** Balch, *ML4T* — holdings as part of state and fair-input design (Project 8); Sutton & Barto, 2nd ed., §3.1 (state may combine observations with agent-specific internals such as holdings).

### [ML2-D8G3Q1] Labels vs. action-dependent rewards as learning signals
**Scenario:** A supervised strategy labels each day BUY/SELL/HOLD from the next five-day return against ±1% thresholds; an RL strategy instead receives daily net-portfolio-value changes. Classify each claim.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the labels explicitly embed a five-day horizon and chosen thresholds. Verdict False. |
| B | False (accurate) | Correct: the RL reward depends partly on the positions produced by the learner's actions (and on costs). |
| C | True (incorrect) | Wrong: identical market features do not ensure identical learning signals — one system sees target labels, the other action-dependent rewards. |
| D | False (accurate) | Correct: altering the labeling thresholds can change the fitted strategy without changing the features. |
| E | True (incorrect) | Wrong: daily rewards do not automatically assign all long-run consequences perfectly — delayed effects create a credit-assignment problem. |

**Reference:** Balch, *ML4T* — label construction (horizon/thresholds) vs. reward design (Project 8); Sutton & Barto, 2nd ed., §3.2–§3.3 (rewards, returns) and ch.1 (delayed reward / credit assignment).

### [ML2-D8G3Q2] Temporal credit assignment — costly entry before a rally
**Scenario:** A Q-Learner buys before a three-day rally; day one's net reward is slightly negative (market impact), later rewards positive. A researcher calls the buy a mistake using only its immediate reward.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A costly entry can still have positive long-term value, so the immediate negative reward alone does not condemn it. |
| B | True | A positive discount factor lets bootstrapped later value propagate back into the earlier state-action value. |
| C | False | With discount = 0 only the immediate reward enters the target; zero discounting weights later rewards *less*, not more. |
| D | True | The example illustrates why temporal credit assignment matters in sequential trading. |
| E | False | The later appreciation is not assigned automatically and exclusively to the original buy — attribution depends on states, subsequent actions, discounting, and the algorithm. |

**Reference:** Balch, *ML4T* — discounting and sequential value in Q-Learning (lectures 03-05); Sutton & Barto, 2nd ed., §3.3–§3.4 (returns and discounting) and ch.1 / ch.12 (temporal credit assignment).

### [ML2-D8G3Q3] Label definition is strategy design
**Scenario:** Two supervised learners share algorithm and features. Learner A is labeled by the sign of next-day return; Learner B by the position that would have maximized five-day net return after estimated costs.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Different target definitions can produce different strategies even with the same algorithm and features. |
| B | True | Learner B's labels embed horizon, cost estimates, and an optimization criterion — more trading assumptions than a sign label. |
| C | False | Similar classification accuracy is measured against different targets and does not establish similar trades or returns. |
| D | True | Label construction determines the behavior the learner reproduces, so it is part of strategy design, not neutral preprocessing. |
| E | False | Using future outcomes to build labels is legitimate when train/test boundaries and timing are handled correctly — not always leakage. |

**Reference:** Balch, *ML4T* — label engineering as strategy design and leakage avoidance (Project 8); standard backtest-evaluation references on train/test discipline (e.g., Prado, *Advances in Financial Machine Learning*, labeling chapter).

### [ML2-D8G4Q1] Batch dataset vs. interactive simulated trajectory
**Scenario:** A decision-tree learner receives a fixed one-row-per-date table; a Q-Learner replays the same prices, but each action changes its simulated holdings and later portfolio rewards. Classify each claim.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the supervised dataset is assembled independently of the model's fitted actions, so examples are fixed before fitting. Verdict False. |
| B | False (accurate) | Correct: the Q-Learner's trades alter inventory, cash, costs, and portfolio value without changing the historical prices. |
| C | True (incorrect) | Wrong: standard historical replay does not let simulated orders rewrite recorded market prices, so it is not "fully interactive." |
| D | False (accurate) | Correct: simulated agent state and rewards can respond to actions even when the price path is fixed. |
| E | True (incorrect) | Wrong: a fixed price history does not prevent RL updates — they are computed from simulated state transitions and rewards. |

**Reference:** Balch, *ML4T* — market simulator with fixed prices and action-dependent portfolio (Project 8 / `marketsim`); Sutton & Barto, 2nd ed., §3.1 (agent-environment interaction) and ch.8 (planning/replay from fixed experience).

### [ML2-D8G4Q2] Episodes, retained Q-table, and epsilon decay
**Scenario:** A Q-Learner trains 100 episodes on one period; each episode starts with the same cash and no holdings, but epsilon decays and the Q-table is retained.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Exploration and evolving Q-values can produce different action sequences across episodes despite the same price path. |
| B | True | Retaining the Q-table carries value estimates — and thus learning — across episode boundaries. |
| C | False | Portfolio state and learned parameters are reset or retained independently; resetting the portfolio does not erase the Q-values. |
| D | True | Decaying epsilon lowers the probability of random actions, shifting behavior from exploration toward exploitation. |
| E | False | One hundred passes through a fixed history are not 100 statistically independent market samples. |

**Reference:** Balch, *ML4T* — episodic Q-learning, epsilon decay, retained Q-table (lectures 03-05, Project 8); Sutton & Barto, 2nd ed., §2.x (epsilon-greedy exploration/exploitation) and §3.3 (episodes).

### [ML2-D8G4Q3] What "interactive" means — immutable prices and fixed impact
**Scenario:** One researcher calls a historical simulator "interactive" because trades are chosen sequentially; another objects that prices are immutable and the impact formula is fixed and unrelated to order flow. Classify each claim.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the strategy can interact with a simulated portfolio (cash/holdings) while having no causal effect on the historical market path. Verdict False. |
| B | False (accurate) | Correct: "interactive" should be qualified by describing which environment variables actually respond to actions. |
| C | True (incorrect) | Wrong: sequential decision-making alone does not prove the simulator reproduces live market feedback. |
| D | False (accurate) | Correct: a fixed impact model can approximate a trading cost without modeling a truly endogenous market response. |
| E | True (incorrect) | Wrong: limited market feedback and other simulation assumptions constrain external validity, so live-deployment caveats are needed. |

**Reference:** Balch, *ML4T* — market-impact modeling and simulator limitations (Project 8); standard backtest-evaluation references on backtest realism and external validity (e.g., Prado, backtesting pitfalls).

### [ML2-D8G5Q1] Confounded comparison — unequal feature sets
**Scenario:** A tree strategy using momentum and Bollinger-band position is compared with a Q-Learner using those plus volatility and current holdings; the team attributes all performance differences to the learning algorithms.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The conclusion is confounded because the learners receive different inputs, so differences may stem from information access, not algorithm. |
| B | True | Volatility can give the Q-Learner predictive information the tree lacks. |
| C | False | Identical feature names are not sufficient — different window lengths or timestamps make them materially different. |
| D | True | A controlled comparison would first give both systems the same market indicators and timing conventions. |
| E | False | Current holdings cannot be ignored — they affect valid and costly actions, so their availability must be controlled or accounted for. |

**Reference:** Balch, *ML4T* — fair-input design and feature parity (Project 8); Sutton & Barto, 2nd ed., §3.1 (holdings as state). Standard backtest-evaluation references on controlled comparison.

### [ML2-D8G5Q2] Feature timing and leakage despite a shared name
**Scenario:** Both learners get a "momentum" column. For the supervised model it uses data through today's close to trade next-day open; for the RL model it includes the next day's close while choosing today's closing trade. Classify each claim.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the columns are not information-equivalent despite the shared name — their windows and decision timing differ. Verdict False. |
| B | False (accurate) | Correct: the RL feature contains future information relative to its decision time (the next close is unavailable then). |
| C | True (incorrect) | Wrong: a higher RL test return is not sufficient evidence the algorithm is superior — the leaked feature can inflate performance independently of algorithm quality. |
| D | False (accurate) | Correct: fairness requires aligning feature timestamps with when each trade decision is made. |
| E | True (incorrect) | Wrong: using the same formula does not remove leakage introduced by unavailable (future) timestamps. |

**Reference:** Balch, *ML4T* — look-ahead bias and feature timing (Project 8); standard backtest-evaluation references on data leakage / look-ahead bias (e.g., Prado, backtesting pitfalls).

### [ML2-D8G5Q3] Data snooping — manual thresholds set after seeing the test chart
**Scenario:** A manual strategy, a tree learner, and a Q-Learner all use the same three normalized indicators. The manual thresholds are chosen after viewing the test-period chart; both learners are finalized before the test period is examined.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Shared indicators alone do not make this a fair out-of-sample comparison — the manual rule had indirect access to test outcomes. |
| B | True | Choosing thresholds after inspecting test outcomes contaminates the manual strategy's evaluation. |
| C | True | The manual strategy should be designed from training-period information or prespecified rules, with the test interval unseen until the design is fixed. |
| D | False | A frozen manual rule can be evaluated out of sample like any other strategy — manual strategies are not inherently un-testable. |
| E | False | Normalization does not guarantee no future information — its parameters can themselves leak if computed from future/test data. |

**Reference:** Balch, *ML4T* — out-of-sample discipline and overfitting to test data (Project 8); standard backtest-evaluation references on data snooping (e.g., White's reality check; Prado).

### [ML2-D8G6Q1] Fair comparison — unequal cost assumptions
**Scenario:** A manual strategy is tested with no transaction costs while two learned strategies include commissions and market impact; the team declares the manual strategy superior on raw return.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Different cost assumptions distort the comparison, so the conclusion is unfair. |
| B | True | All strategies should use the same evaluation period to hold the market environment constant. |
| C | True | All strategies should use the same starting portfolio value, since starting capital affects comparability. |
| D | False | A higher raw return is not sufficient when test conditions differ — unequal conditions undermine the conclusion. |
| E | True | Consistent benchmarks and metrics are necessary for a meaningful comparison. |

**Reference:** Balch, *ML4T* — common costs, period, and capital for fair comparison (Project 8); standard backtest-evaluation references on consistent assumptions and benchmarking.

### [ML2-D8G6Q2] Dollar profit, capital, and leverage
**Scenario:** Strategy A starts with $100,000 and may use 2:1 leverage; Strategy B starts with $50,000 and may not borrow. The report compares only ending dollar profits and calls the larger value better.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Ending dollar profit is affected by starting capital and permitted exposure. |
| B | True | Matching capital and leverage constraints would improve comparability. |
| C | False | Percentage return alone would not capture every relevant difference — equal returns can hide very different volatility, drawdown, or tail risk. |
| D | True | Risk-adjusted metrics such as Sharpe ratio and drawdown can supplement cumulative return when leverage or volatility differs. |
| E | False | A larger dollar profit does not prove greater learning quality when capital and leverage differ. |

**Reference:** Balch, *ML4T* — cumulative return vs. risk-adjusted metrics; Sharpe ratio and drawdown (lectures 01-07/Project 8); standard backtest-evaluation references on normalized and risk-adjusted performance.

### [ML2-D8G6Q3] Incoherent ranking — one isolated metric per strategy
**Scenario:** Three strategies are evaluated over the same dates, costs, and capital, but the report ranks them using A's cumulative return, B's Sharpe ratio, and C's maximum drawdown as if these formed one scale. Classify each claim.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the strategies are not ranked on a common criterion — different dimensions are treated as one comparable scale. Verdict False. |
| B | False (accurate) | Correct: a common metric set, computed under the same conventions, enables like-for-like comparison. |
| C | False (accurate) | Correct: a shared benchmark such as buy-and-hold helps interpret whether performance adds value. |
| D | True (incorrect) | Wrong: common dates and costs do not repair an incoherent ranking rule — fair inputs are necessary but not sufficient. |
| E | True (incorrect) | Wrong: one metric is not always enough — strategy preference depends on return, risk, drawdown, costs, and investor objectives. |

**Reference:** Balch, *ML4T* — reporting a common metric set and benchmark (Project 8; cumulative return, Sharpe, drawdown); standard backtest-evaluation references on multi-metric and benchmark-relative evaluation.

### [ML2-D8G7Q1] In-sample vs. out-of-sample — overfitting signal
**Scenario:** On training, the Q-Learner strongly beats a tree learner and a manual strategy; on the unseen test period it underperforms buy-and-hold while the tree and manual strategies earn smaller positive excess returns.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Training performance alone is insufficient evidence of generalization — it may reflect adaptation to conditions already seen. |
| B | True | The train-to-test reversal is consistent with overfitting to the training environment. |
| C | False | Remaining profitable out of sample does not make the manual strategy optimal or robust. |
| D | True | The comparison should examine both in-sample and out-of-sample results under aligned assumptions. |
| E | False | Underperforming on one test period does not prove RL can never work for trading — one result is not a universal impossibility. |

**Reference:** Balch, *ML4T* — in-sample vs. out-of-sample testing and overfitting (Project 8; lectures on overfitting); standard backtest-evaluation references on generalization and train/test gaps.

### [ML2-D8G7Q2] Statistical vs. economic significance across windows
**Scenario:** Across 20 independent test windows, a learned strategy beats a manual one in 11 windows, but the average difference is tiny and vanishes after transaction costs. The team advertises it as economically superior. Classify each claim.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: winning 11 of 20 windows alone gives limited evidence about magnitude and uncertainty. Verdict False. |
| B | False (accurate) | Correct: economic significance depends on the magnitude of net improvement, not only how often the learner wins. |
| C | False (accurate) | Correct: transaction costs are relevant to whether the observed advantage is deployable. |
| D | True (incorrect) | Wrong: a positive average gross difference is not automatically statistically significant — significance depends on variability, dependence, sample design, and effect size. |
| E | True (incorrect) | Wrong: statistical significance would not guarantee economic worth — a precise effect can still be too small to matter. |

**Reference:** Balch, *ML4T* — evaluating edge after costs and over multiple windows (Project 8); standard backtest-evaluation references on statistical vs. economic significance and multiple-testing (e.g., Prado; White's reality check).

### [ML2-D8G7Q3] One directional outcome cannot rank designs
**Scenario:** In one regime the manual strategy holds cash, the supervised strategy goes long, and the Q-Learner goes short. The next day's return is negative, so an analyst concludes the Q-Learner is categorically the best design.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Disagreement does not prove bugs — correctly implemented strategies can choose different actions because their designs differ. |
| B | True | The strategies may disagree because their objectives, horizons, learning signals, or state representations differ. |
| C | False | One correct directional decision is too limited and noisy to rank the designs reliably. |
| D | True | Examining repeated out-of-sample outcomes and portfolio-level metrics would provide stronger evidence. |
| E | False | A cash position need not mean a forecast of exactly zero — it can mean the evidence does not cross the strategy's threshold for taking exposure. |

**Reference:** Balch, *ML4T* — why strategies disagree and the need for repeated out-of-sample evaluation (Project 8); Sutton & Barto, 2nd ed., §3.1–§3.5 (objectives, state, policy differences). Standard backtest-evaluation references on sample size and noise.

## References (domain-level)

1. **Balch — *ML4T* (Georgia Tech), Project 8 "Strategy Evaluation":** the core comparison of a Manual Strategy, a tree-based supervised Strategy Learner, and a Q-Learning strategy over the same symbol, dates, costs, and starting capital — including in-sample vs. out-of-sample testing, impact/commission settings in the market simulator, and reporting cumulative return, Sharpe ratio, and drawdown. Also lectures 03-05/03-06 (Q-Learning and trading-as-RL), Project 6 (predict-then-trade indicators/rules), and 01-07 (performance metrics: cumulative return, Sharpe, volatility, drawdown).
2. **Sutton & Barto — *Reinforcement Learning: An Introduction*, 2nd ed.:** ch.1 §1.1 (RL vs. supervised learning; reward/interaction vs. labels; delayed reward); §3.1 (agent-environment interaction, state including holdings); §3.2 (reward defines the objective, costs/penalties); §3.3–§3.4 (returns, discounting, episodes; discount = 0 keeps only the immediate reward); §3.5 (policy distinct from value estimates); §2.x (epsilon-greedy exploration/exploitation); ch.6 (Q-learning convergence); ch.8 (planning/replay from fixed experience); ch.12 (temporal credit assignment).
3. **Standard backtest-evaluation references:** de Prado, *Advances in Financial Machine Learning* (labeling, backtesting pitfalls, look-ahead bias/data leakage, multiple-testing and the deflated/economic significance of a strategy); White (2000), "A Reality Check for Data Snooping" (data-snooping bias in strategy comparison); general treatments of risk-adjusted performance (Sharpe ratio, maximum drawdown) and benchmark-relative evaluation (buy-and-hold). Cited at section/topic level to characterize fair comparison, leakage, and significance — no specific page numbers invented.

---

*Note on source fidelity:* All verdicts above are transcribed verbatim from `slices/ML2_D08.txt` (never flipped). The source text contains "fi"/"fl" **ligature glyphs** (e.g., "classiﬁer", "ﬁt", "ﬁve", "proﬁtable", "inﬂuence", "deﬁned", "conﬁgurable", "signiﬁcance") and recurring **page-footer artifacts** (e.g., "538 Rev:081020261230"); these are OCR/typesetting garble and have been rendered as normal characters here without altering any answer-key verdict.
