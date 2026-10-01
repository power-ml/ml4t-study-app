# ML Domain 7 — Reinforcement Learning for Trading

## Domain cheat-sheet

- **Formulating trading as an RL problem.** Map the desk's decision loop onto the five RL primitives:
  - **State** = the information available *at decision time*. In a Q-Learning trader it typically combines **market indicators** (momentum, volatility, Bollinger-band position — usually **discretized** into bins) **with the agent's own holdings** (long/cash/short, or exact position size and remaining capacity). The state must contain **only contemporaneously available** information — anything computed from prices that would not exist when a live action is selected is leakage.
  - **Action** = a **controllable choice**, most naturally expressed as a **target position** (e.g., short/cash/long → −1,000 / 0 / +1,000 shares). The action names a *desired* holding; the **order size is derived** by subtracting current holdings from the target (`order = target − current`). The same action label can mean very different trades under different execution mappings (incremental "buy 100 each time" vs. "move to +100 target").
  - **Reward** = a scalar that *defines the objective*. The economically correct reward is the **change in net portfolio value including commissions and market impact**, not gross price change and not a proxy such as "+1 per order." Changing the reward changes the learned policy, so a mis-specified proxy (activity count, gross-only P&L) can be maximized while real profitability falls.
- **Discretization & the Markov representation.** Binning maps ranges of continuous values into a finite label set so a tabular Q-learner can index states. `k` indicators with `b` bins each give `b^k` states (3 indicators × 3 bins = 3³ = 27). Trade-offs: more bins → more distinct states but **sparser** experience per state and more poorly-supported (unvisited) states at deployment; observations sharing a bin are **indistinguishable** to the learner and are *asserted* to be equivalent (binning does not *prove* identical future-return distributions).
- **Holdings belong in the state.** Omitting current holdings **aliases** portfolio situations that call for different actions (in the same bullish indicator state the right move is buy-when-flat, hold-when-long, cover-when-short). Holdings are decision-relevant even though the *agent* controls them: they determine order size, cost, risk, and feasibility. Market indicators **alone** do not guarantee a Markov representation of the combined market-plus-portfolio process. Adding holdings improves the representation but does **not** by itself guarantee good out-of-sample performance.
- **Position persistence & mark-to-market reward.** With a target-position simulator, selecting the same target you already hold produces a **zero order** — the position carries forward with no new trade. "No trade" ≠ "zero reward": an open position is **marked to market**, so portfolio value (and thus the daily reward) moves with price even on days with no transaction. A realized-only reward delays feedback and worsens credit assignment.
- **Transaction costs, impact, and turnover.** Commissions (fixed per order) and market impact (scales with traded quantity) must be **inside the reward**. A reward on *gross* change rewards churn; realistic costs can turn a positive-gross-expected-value marginal trade into **negative net** value, so a cost-aware learner rationally trades less. Reversals are expensive: moving +1,000 → −1,000 trades **2,000** shares, not 1,000. Compare strategies on **net-of-cost** performance when turnover differs.
- **Train / test / out-of-sample discipline.** Freeze the Q-table and discretization thresholds learned on the training window, then evaluate once, forward-in-time, on a later untouched window. **Leakage sources beyond an explicit future-return feature:** full-sample normalization (uses test-period statistics in training features), and **tuning hyperparameters/features on the test period** (turns the "test" set into part of model selection — its role is set by *use*, not by its label). Repeatedly selecting the best of many configurations on one period invites **selection bias**; a fresh holdout gives the cleaner final estimate. Good in-sample ≠ good out-of-sample.
- **Market non-stationarity & policy stability.** Markets are non-stationary: state frequencies, the returns following each state-action pair, and costs all drift across regimes. A **frozen** Q-table can go **stale** — its values no longer represent current expected returns — even if chosen actions look unchanged. Monitor state visitation and net performance; stable *actions* do not prove stationary *rewards*. Responses: rolling retraining + validation (Plan A) vs. online learning with continuing exploration (Plan B, which incurs real-money exploratory trades and still needs risk controls). Q-Learning offers **no guarantee** that a historical policy stays optimal after a regime change.
- **Q-Learning trader vs. supervised predictor.** The Q-Learner learns a **policy** (state → action) from **reward-bearing transitions** and acts to maximize **cumulative net** reward; a supervised model predicts a **label** (e.g., next-day return) from a fixed dataset and needs a separate trading rule. A more accurate predictor is not guaranteed to yield the best net-of-cost policy.

## Common traps

- **Inverted-polarity questions (9 of 21 here).** When the body says "mark each statement True when the stated claim is **incorrect** and False when it is correct," the Answer-Key verdict is flipped relative to the statement's truth: **True = the statement is wrong; False = the statement is accurate.** Read the polarity line *first*. Inverted here: **G1Q1, G2Q2, G3Q2, G3Q3, G4Q2, G4Q3, G5Q2, G6Q2, G7Q1.** The remaining 12 are Normal (True = accurate).
- **Look-ahead leakage hides in preprocessing/selection, not just features.** "No future-return feature ⇒ clean evaluation" is false. Full-sample normalization and tuning on the test window both leak; "any indicator from historical prices is automatically safe" is false whenever the calculation includes prices unavailable at decision time.
- **Action = order size.** False — the action is a **target position**; the order is `target − current`. Selecting "short" while already short the target quantity trades **zero**; short→long trades twice as much as cash→long.
- **Same action label ⇒ same portfolio dynamics.** False — execution semantics (incremental vs. target) determine accumulation, turnover, and cost; defining the action set alone does not fix the learned returns.
- **"Hold" ⇒ flat / zero position.** False — hold preserves the current position, which may be long or short.
- **Omitting holdings is harmless.** False — it aliases situations needing different actions; holdings are decision-relevant even though the agent controls them.
- **No trade ⇒ zero reward.** False — an open position is marked to market, so held inventory produces positive or negative reward without a transaction.
- **Target-position actions remove the need to model costs.** False — any nonzero order still incurs commissions/impact; a risk layer can still clip or reject the highest-Q action.
- **Reward proxy is cosmetic / "the desk's verbal goal overrides the number."** False — Q-updates use the *supplied numerical reward*. Rewarding order count maximizes activity, not profit; use **net** portfolio-value change.
- **Gross-only comparison is fine.** False when turnover differs — net-of-cost performance is required; impact changes effective transaction prices, not just the accounting presentation.
- **"Test set" label guarantees validity.** False — a dataset's role is determined by its use; repeated selection on it overfits that period. Favorable in-sample numbers are not a reason to discard genuinely out-of-sample evidence.
- **Frozen policy stays optimal / stable actions ⇒ stationary environment.** False — regime change makes stale Q-values; unchanged turnover does not prove unchanged costs, and deteriorating returns under a fixed policy signal non-stationarity.
- **Online learning needs no guardrails.** False — continuing exploration in production places deliberately non-greedy, real-money trades; validation and risk controls remain necessary. Neither rolling retraining nor online adaptation *guarantees* improvement (recent data can be noisy or insufficient).
- **One bad test period condemns RL.** False — a single strategy-period result does not establish a universal limitation of the method (and one good period does not prove durability either).

> **Garbled-symbol flag:** the source slice renders many words with `fi`/`fl` **ligature glyphs** (e.g., "ﬁnite," "ﬁxed," "ﬂawed," "proﬁtability," "beneﬁt," "inﬂuencing," "speciﬁc"). These are transcription artifacts of the PDF export, not content errors; they are reproduced here as ordinary `fi`/`fl`. Page-footer markers of the form `522 Rev:081020261230` in the slice are pagination noise, not part of any question.

## Questions

### [ML2-D7G1Q1] State must use only information available at decision time
**Scenario:** A fund builds a daily Q-Learning strategy on discretized momentum, volatility, and Bollinger-band position. A researcher wants to add *tomorrow's return* because it exists in the completed historical dataset; the production trader notes the value will not exist when a live action is selected.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a deployable decision rule must operate on contemporaneously available information, so a historical decision's state should contain only information available by that decision time. |
| B | False (accurate) | Correct: tomorrow's return reveals part of the outcome the learner is meant to act *before* observing — using it to choose today's action is look-ahead leakage. |
| C | False (accurate) | Correct: discretizing bins maps ranges of continuous values into a limited set of labels, letting many continuous observations share a finite state. |
| D | True (incorrect) | Wrong: an indicator computed from historical prices is **not** automatically safe — it still leaks if the calculation includes prices unavailable at the decision time. |
| E | True (incorrect) | Wrong: a useful state representation need not preserve every raw observation exactly; it may intentionally compress observations while retaining decision-relevant distinctions. |

**Reference:** Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed., §3.1 (state as information available at decision time); Balch ML4T Q-Learning / trading-as-RL lectures (03-05) and Project 8 (strategy learner) on indicator features and avoiding look-ahead; Moody & Saffell (2001), "Learning to Trade via Direct Reinforcement" (state/feature construction for a trading agent).

### [ML2-D7G1Q2] Discretization, state count, and sparsity
**Scenario:** A learner assigns each day to one of 27 states formed from three indicators with three bins each. Review finds that two conditions with identical bins can have different raw indicator values and that some state combinations never occur in training.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | With all combinations possible, three indicators with three bins each define the Cartesian product 3³ = 27 states. |
| B | True | Observations in the same discrete state are indistinguishable to a tabular learner (the Q-table indexes the shared label, not the raw values) unless other state information is added. |
| C | True | An unvisited state may have poorly supported action values when first encountered at deployment — the learner has little or no direct experience there. |
| D | False | Sharing a state asserts a *modeling* equivalence; it does not prove the two observations have identical future-return distributions. |
| E | False | More bins generally spread a fixed history across more states and can *increase* sparsity — it does not reduce the experience needed per state. |

**Reference:** Sutton & Barto, 2nd ed., §3.1 (state representation) and ch.6 (tabular Q-learning, experience per state); Balch ML4T Project 7 (Q-Learning Robot) and Project 8 (strategy learner) on discretization and state-space sizing.

### [ML2-D7G1Q3] Full-sample normalization and test-period tuning leak
**Scenario:** A team normalizes each day's indicator using the mean/standard deviation of the entire 2015–2025 dataset, then reports an out-of-sample test on 2024–2025, and also uses the test period to choose the bin count that maximizes test return.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Full-sample normalization leaks test-period information into earlier feature values — the transformation parameters use observations that should have stayed unseen during training. |
| B | True | Selecting bin counts by test-period return makes the test period part of model selection, so it is no longer purely evaluative. |
| C | False | Leakage can enter through preprocessing and selection even without an explicit future-return feature, so the evaluation is **not** automatically clean. |
| D | False | Repeatedly tuning on the same test period adapts the system to that period and biases the reported performance — it is not an unbiased estimate of generalization. |
| E | False | Fitting preprocessing on the entire dataset before splitting uses test-period distribution information before evaluation, which breaks temporal separation rather than preserving it. |

**Reference:** Balch ML4T lectures on overfitting and in-sample vs. out-of-sample evaluation (03-06/03-07) and Project 8 (train/test discipline); Sutton & Barto, 2nd ed., ch.1 (generalization, evaluating a learned policy on unseen data).

### [ML2-D7G2Q1] Target positions vs. order size
**Scenario:** An agent's action space is short/cash/long, interpreted as target positions of −1,000 / 0 / +1,000 shares. The agent is currently short 1,000 shares when it selects *long*.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Reaching the long target requires buying 2,000 shares — moving inventory from −1,000 to +1,000. |
| B | True | The selected action describes a desired *position*; the order is derived by subtracting current holdings from the target, so it is not necessarily the order size itself. |
| C | False | Selecting *short* while already short 1,000 shares requires a zero order — current and desired inventories are already equal. |
| D | False | A short→long move trades 2,000 shares while a cash→long move trades only 1,000, so the traded quantities differ. |
| E | True | Transaction costs depend on the executed position change — commissions and impact arise from executed quantity, not the target label. |

**Reference:** Sutton & Barto, 2nd ed., §3.1 (actions as controllable choices); Balch ML4T Project 8 (strategy learner — target-position action space, order generation) and trading-as-RL lectures (03-05/03-06); Moody & Saffell (2001) (direct RL over target positions / trading signals).

### [ML2-D7G2Q2] Same action label, different execution mappings
**Scenario:** Two teams both expose actions named buy/sell/hold. Team A treats *buy* as purchasing 100 shares on every selection; Team B treats *buy* as moving to a fixed +100-share target. A bullish state persists four days.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: under Team A's incremental interpretation, selecting *buy* on all four days adds 100 shares each time and can accumulate 400 shares absent a constraint. |
| B | False (accurate) | Correct: under Team B's target interpretation the first *buy* may trade 100 shares, while later identical selections trade zero once the +100 target is reached. |
| C | False (accurate) | Correct: the same action label creates different portfolio dynamics under different execution mappings — semantics determine accumulation, turnover, constraints, and costs. |
| D | True (incorrect) | Wrong: a *hold* action ordinarily preserves the current position, which may be long or short — it does not necessarily mean a zero position in both implementations. |
| E | True (incorrect) | Wrong: defining actions alone is **not** sufficient — the order-generation rule determines holdings and costs and therefore changes the reward sequence the learner experiences. |

**Reference:** Sutton & Barto, 2nd ed., §3.1 (action semantics) and §3.2 (reward depends on executed outcomes); Balch ML4T Project 8 (strategy learner — action-to-order mapping) and lectures 03-05/03-06.

### [ML2-D7G2Q3] Risk-control layer can clip or reject the chosen action
**Scenario:** A fund permits positions of −500 / 0 / +500 shares. Its simulator receives a desired target, computes the order from current holdings, and then checks leverage and liquidity limits before execution.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Current holdings are needed to translate a target position into an order quantity — required trade = desired inventory − existing inventory. |
| B | True | A risk-control layer may reject or clip an order even when the learner assigns that action the highest Q-value — hard constraints can override a proposed action. |
| C | True | If an order is clipped, resulting holdings may differ from the learner's requested target — partial execution cannot always reach the requested exposure. |
| D | False | Target-position actions do not eliminate the need to model commissions and market impact — any nonzero order can still create implementation costs. |
| E | False | A feasible action in one portfolio state need not be feasible in every other — feasibility depends on current exposure, capital, liquidity, and other state-specific constraints. |

**Reference:** Sutton & Barto, 2nd ed., §3.1 (action feasibility; environment applies constraints); Balch ML4T Project 8 (order generation, leverage/position limits) and lectures 03-06/03-07; Moody & Saffell (2001) (position/risk constraints in a trading agent).

### [ML2-D7G3Q1] Holdings are decision-relevant state
**Scenario:** A strategy's state includes market indicators but **not** current holdings. In the same bullish indicator state the right decision is buy-when-in-cash, hold-when-long, cover-when-short — yet the Q-table has only one set of action values for that indicator state.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Omitting holdings aliases portfolio situations that may require different actions — distinct inventory conditions collapse into one table entry. |
| B | True | Including long/cash/short status permits separate action values for otherwise identical market indicators (the combined market-position state learns per-inventory preferences). |
| C | True | Holdings can be decision-relevant even though the agent controls them — existing inventory changes order size, costs, risk, and feasible decisions. |
| D | False | Market indicators alone do **not** guarantee a Markov representation of the combined market-and-portfolio process — an action's consequences can depend on omitted portfolio state. |
| E | False | Adding holdings does not guarantee optimal out-of-sample performance — a better representation does not ensure sufficient data, suitable rewards, stable markets, or generalization. |

**Reference:** Sutton & Barto, 2nd ed., §3.1 (state includes agent-internal variables) and §3.5 (Markov property); Balch ML4T Project 8 (holdings in the state) and lectures 03-05/03-06.

### [ML2-D7G3Q2] Position persistence and no-trade days
**Scenario:** A daily learner enters long on Monday and keeps selecting the long target on Tuesday and Wednesday while the bullish state persists; the simulator trades only the difference between current and desired holdings.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the position can persist across days with no new order — existing holdings carry forward unless a trade or forced liquidation changes them. |
| B | False (accurate) | Correct: selecting the same long target while already long represents maintaining exposure (target = current, so the required order is zero), not repeatedly buying. |
| C | False (accurate) | Correct: portfolio value may change on Tuesday even with no trade because mark-to-market gains/losses arise from price changes on the held inventory. |
| D | True (incorrect) | Wrong: no trade does **not** force a zero reward — a held position can generate a positive or negative portfolio-value reward without a transaction. |
| E | True (incorrect) | Wrong: position persistence does not make holdings irrelevant — holdings are precisely what determine whether a new target requires an order. |

**Reference:** Sutton & Barto, 2nd ed., §3.1–§3.2 (state carries forward; reward from value change); Balch ML4T Project 8 (holdings persistence, daily portfolio-value reward) and lectures 03-05/03-06.

### [ML2-D7G3Q3] Coarse vs. exact holdings encoding
**Scenario:** A risk manager compares two state encodings: one records only long/cash/short, the other records exact position size and remaining leverage capacity. Positions range 100–10,000 shares under a capital limit.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the three-category encoding may combine positions with materially different risk and remaining capacity — a small and a maximum-size long share one label. |
| B | False (accurate) | Correct: exact inventory can distinguish whether an additional purchase would breach the capital limit — current size helps judge whether more risk is feasible. |
| C | False (accurate) | Correct: a coarser holdings state may generalize more broadly but lose decision-relevant detail — compression trades specificity for broader sharing of experience. |
| D | True (incorrect) | Wrong: recording exact position size **can** increase state-space complexity — greater inventory granularity creates more distinct states. |
| E | True (incorrect) | Wrong: having holdings in the state does **not** make separate limit enforcement unnecessary — operational controls should still enforce hard constraints. |

**Reference:** Sutton & Barto, 2nd ed., §3.1 (state granularity trade-offs) and ch.6 (state-space size vs. data); Balch ML4T Project 8 (holdings encoding) and lectures 03-06/03-07 on risk controls.

### [ML2-D7G4Q1] Realized-only vs. mark-to-market reward
**Scenario:** A learner buys at Monday's close and holds through Thursday. Reward is recorded only when a position is closed, so Tuesday and Wednesday return zero despite a substantial mark-to-market loss; the position is sold Thursday.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A realized-only reward delays feedback about changes in the value of an open position — nothing is recognized until the closing transaction. |
| B | True | Daily change in total portfolio value could reflect unrealized gains and losses before Thursday, because current prices revalue open inventory each day. |
| C | False | Zero realized profit on Tuesday does not prove no economic loss — an open position can lose value without the loss being realized through a sale. |
| D | True | Reward timing affects how readily the learner associates actions with consequences — long delays make credit assignment harder. |
| E | False | Mark-to-market reward does **not** require future prices — reward for a completed interval can use the endpoint price observed at that time without looking beyond it. |

**Reference:** Sutton & Barto, 2nd ed., §3.2 (reward signal) and ch.1 / ch.12 (delayed reward and temporal credit assignment); Balch ML4T Project 8 (daily portfolio-value reward) and lectures 03-05/03-07; Moody & Saffell (2001) (per-period returns as the reward).

### [ML2-D7G4Q2] Net vs. gross reward arithmetic
**Scenario:** A fund starts a day at $100,000. After price moves and all trades, but before a $50 commission, value is $101,000; the commission is then charged.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the gross dollar change before commission is +$1,000 (the pre-cost value rose from $100,000 to $101,000). |
| B | False (accurate) | Correct: subtracting the $50 commission from $101,000 leaves a net ending value of $100,950. |
| C | False (accurate) | Correct: the net dollar reward based on portfolio-value change is +$950 (from the $100,000 start). |
| D | True (incorrect) | Wrong: gross and net are **not** equal — commission reduces portfolio value even though it does not move the quoted asset price. |
| E | True (incorrect) | Wrong: +$950 is 0.95% of $100,000, not 9.5%. |

**Reference:** Sutton & Barto, 2nd ed., §3.2 (reward defines the objective; costs enter the reward); Balch ML4T Project 8 (net portfolio-value reward with commissions) and lectures 03-06; Moody & Saffell (2001) (returns net of transaction costs).

### [ML2-D7G4Q3] Reward misspecification — rewarding order count
**Scenario:** A desk rewards its agent +1 every time it submits an order, regardless of profit. The agent learns to trade at nearly every step while portfolio value declines after costs.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the learner may maximize the encoded activity reward while harming the desk's profitability objective — the proxy values activity, not economic performance. |
| B | False (accurate) | Correct: rewarding order count creates an incentive for turnover, since each additional order earns another positive signal. |
| C | False (accurate) | Correct: a reward based on net portfolio-value change aligns learning more directly with the economic objective, because net value incorporates investment outcomes and implementation costs. |
| D | True (incorrect) | Wrong: falling portfolio value does **not** prove the agent failed to maximize its reward — frequent trading may successfully maximize the flawed order-count reward. |
| E | True (incorrect) | Wrong: the Q-update uses the supplied numerical reward, **not** the desk's unstated verbal intention — the verbal goal does not override the numbers. |

**Reference:** Sutton & Barto, 2nd ed., §3.2 (reward hypothesis; the reward defines what is optimized — reward hacking from proxies); Balch ML4T lectures 03-05/03-06 (choosing the trading reward) and Project 8; Moody & Saffell (2001) (profit/risk-adjusted return as the correct objective).

### [ML2-D7G5Q1] Costs belong in the training reward
**Scenario:** A Q-Learning strategy performs well with zero costs; with realistic commissions and impact it still trades frequently and net performance turns negative. The PM argues the original (gross) reward should be kept because costs are an "execution issue, not a learning issue."
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A reward based only on gross portfolio change can encourage excessive turnover — frequent small trades look attractive. |
| B | True | Transaction costs can be incorporated into the reward signal (net change after implementation costs). |
| C | True | If costs are excluded during training, the learned policy may be misaligned with net profitability — the learner optimizes the wrong objective. |
| D | False | Execution costs **can** influence the optimal trading policy — costs can make previously attractive trades unprofitable. |
| E | True | Adding trading penalties may change which actions the learner prefers, because net reward changes the relative value of actions. |

**Reference:** Sutton & Barto, 2nd ed., §3.2 (reward defines the objective); Balch ML4T Project 8 (impact/commission parameters in the reward) and lectures 03-06; Moody & Saffell (2001) (transaction costs inside the direct-RL objective).

### [ML2-D7G5Q2] Turnover, reversals, and market impact
**Scenario:** A strategy alternates daily between +1,000 and −1,000 shares; the broker charges $10 per order and each reversal incurs impact proportional to the 2,000-share change. A second strategy usually holds for several days.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: each direct reversal trades 2,000 shares — moving from +1,000 to −1,000 requires selling 2,000. |
| B | False (accurate) | Correct: with similar gross returns the higher-turnover strategy can have lower net returns, since greater implementation costs consume more of its gross performance. |
| C | False (accurate) | Correct: both fixed commissions and quantity-dependent impact penalize frequent reversals (more orders and more traded volume). |
| D | True (incorrect) | Wrong: market impact is **not** mere accounting — it changes effective transaction prices and therefore realized portfolio value. |
| E | True (incorrect) | Wrong: comparing strategies on gross returns alone is **not** sufficient when turnover differs — net performance is needed to judge implementable results. |

**Reference:** Sutton & Barto, 2nd ed., §3.2 (reward reflects true costs); Balch ML4T Project 8 (impact scaling with traded quantity; commissions) and lectures 03-06; Moody & Saffell (2001) (turnover and transaction-cost effects on realized return).

### [ML2-D7G5Q3] Retraining with costs changes the policy
**Scenario:** A learner trained with zero costs takes a small expected-gain trade whenever an indicator crosses a threshold. Retrained with realistic costs, many marginal trades disappear from the learned policy.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Introducing costs can change action-value rankings — costs reduce the expected return of actions that require trading. |
| B | True | A trade with positive expected *gross* value can have negative expected *net* value when implementation cost exceeds the gross gain. |
| C | True | Reduced turnover after cost-aware training can be a rational policy response — avoiding uneconomic marginal trades aligns behavior with net reward — not evidence of failed learning. |
| D | False | A cost-aware learner need **not** always choose cash — opportunities whose expected benefit exceeds costs can still justify positions. |
| E | False | The zero-cost and cost-aware environments do **not** necessarily share the same optimal policy — altering rewards and transition consequences can change which actions are optimal. |

**Reference:** Sutton & Barto, 2nd ed., §3.2 (changing the reward changes the optimal policy); Balch ML4T Project 8 (cost-sensitivity of the strategy learner) and lectures 03-06/03-07; Moody & Saffell (2001) (cost-aware trading behavior).

### [ML2-D7G6Q1] A clean forward out-of-sample test
**Scenario:** A team trains a Q-Learner on 2015–2021, freezes its Q-table and discretization thresholds, and evaluates once on 2022–2023. No test-period observations are used to choose features or hyperparameters.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The chronological separation is consistent with an out-of-sample evaluation — the test uses a later period excluded from model construction. |
| B | True | Freezing the learned policy prevents test-period rewards from updating the Q-table, so test outcomes assess rather than train the stored values. |
| C | True | Applying training-derived thresholds unchanged avoids fitting the preprocessing to the test distribution. |
| D | False | Good 2022–2023 results do **not** prove the policy will stay profitable in every future regime — one historical test cannot guarantee all future conditions. |
| E | False | The test is **not** invalid merely because its observations occur later in calendar time — forward chronological testing is appropriate for a strategy meant to act on future data. |

**Reference:** Balch ML4T lectures on in-sample vs. out-of-sample evaluation and overfitting (03-06/03-07) and Project 8 (frozen-policy forward test); Sutton & Barto, 2nd ed., ch.1 (evaluating a learned policy on held-out experience).

### [ML2-D7G6Q2] Tuning on the test period is selection, not evaluation
**Scenario:** A researcher evaluates 50 combinations of state variables, epsilon decay, and cost penalties on the same 2022–2023 period, picks the highest-return combination there, and reports that return as final out-of-sample performance.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the 2022–2023 period has influenced model selection — test outcomes determine which design is retained. |
| B | False (accurate) | Correct: the maximum reported return is vulnerable to selection bias — some configuration may look best partly because of noise specific to that period. |
| C | False (accurate) | Correct: a later untouched holdout period would give a cleaner final evaluation of the selected configuration. |
| D | True (incorrect) | Wrong: calling the period a "test set" does **not** prevent leakage — a dataset's role is determined by its use, not its label. |
| E | True (incorrect) | Wrong: training each configuration only on earlier data does **not** prevent overfitting the test — repeated selection adapts model-level choices to idiosyncrasies in the test data. |

**Reference:** Balch ML4T lectures on overfitting and model selection / data snooping (03-06/03-07) and Project 8; Sutton & Barto, 2nd ed., ch.1 (generalization; the danger of tuning on the evaluation data).

### [ML2-D7G6Q3] In-sample strength ≠ out-of-sample strength
**Scenario:** A fund compares a learner against a benchmark. In training the learner returns 40% vs. 12%; in a later frozen-policy test it returns 3% vs. 10% and trades much more frequently.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Strong in-sample performance does not establish strong out-of-sample performance — training results reflect data used to build the policy. |
| B | True | The reversal may indicate overfitting, regime sensitivity, or both — the policy may have fit historical patterns or met changed dynamics. |
| C | True | Turnover and net-of-cost performance are relevant to interpreting the comparison — frequent trading can materially reduce implementable results. |
| D | False | The 40% training return should **not** replace the weaker test result — favorability is not a valid reason to discard genuinely out-of-sample evidence. |
| E | False | Underperformance in one test period does **not** prove RL can never be useful for trading — one strategy-period result is not a universal limitation. |

**Reference:** Balch ML4T lectures on backtest overfitting and benchmark comparison (03-06/03-07) and Project 8; Sutton & Barto, 2nd ed., ch.1 (generalization and evaluation); Moody & Saffell (2001) (out-of-sample evaluation of a trading agent).

### [ML2-D7G7Q1] Non-stationarity and stale Q-values
**Scenario:** A policy learned during a long low-volatility bull market is deployed in a high-volatility bear market. State frequencies, the returns following each state-action pair, and trading costs all differ from training.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the environment may be non-stationary relative to the learner's historical experience — market dynamics and costs differ across the regimes. |
| B | False (accurate) | Correct: previously learned Q-values can become stale when transition or reward behavior changes — old estimates need not represent current expected returns. |
| C | False (accurate) | Correct: monitoring state visitation and performance can help detect policy degradation — shifts in inputs and outcomes signal that historical assumptions no longer hold. |
| D | True (incorrect) | Wrong: Q-Learning does **not** guarantee a frozen historical policy stays optimal after a regime change — a frozen policy does not adapt. |
| E | True (incorrect) | Wrong: historical profitability does **not** prove the market's data-generating process is fixed — past success is compatible with a changing process. |

**Reference:** Sutton & Barto, 2nd ed., §2.5 (non-stationary problems; tracking vs. averaging) and ch.1 (environment dynamics); Balch ML4T lectures 03-07 (practical RL / Dyna, regime change); Moody & Saffell (2001) (adaptive / online updating for non-stationary markets).

### [ML2-D7G7Q2] Rolling retraining vs. online adaptation
**Scenario:** A desk weighs two responses to changing markets. Plan A retrains quarterly on a rolling window and deploys only after validation; Plan B keeps learning online from live rewards with continuing exploration, using each updated Q-table immediately.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Rolling retraining can discard older observations while emphasizing recent regimes — it changes the evidence used to estimate the policy. |
| B | True | Online adaptation may respond sooner but can change live behavior as new, noisy rewards arrive — responsiveness can bring instability. |
| C | True | Continuing exploration in production can cause deliberately non-greedy trades with real financial consequences (losses, costs, constraint concerns). |
| D | False | Neither plan **guarantees** improvement — recent data can be noisy, temporary, or insufficient for reliable learning. |
| E | False | Validation and risk controls are **not** unnecessary for Plan B — online adaptation creates additional reasons to monitor and constrain behavior. |

**Reference:** Sutton & Barto, 2nd ed., §2.5–§2.7 (non-stationary tracking; exploration cost) and ch.1 (exploration–exploitation; online vs. batch); Balch ML4T lectures 03-07 (practical/online RL considerations); Moody & Saffell (2001) (online adaptive trading).

### [ML2-D7G7Q3] Stable actions do not prove a stable environment
**Scenario:** A policy's monthly turnover and selected actions stay nearly unchanged for a year, but net returns deteriorate steadily. The manager concludes the policy is "stable" and therefore the environment cannot have changed.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Stable action choices do not prove the rewards resulting from those actions are stationary — the same behavior can produce different results when market relationships change. |
| B | True | Return deterioration can occur even if the policy itself is unchanged — a fixed policy can lose effectiveness under new dynamics. |
| C | False | Unchanged turnover does **not** prove transaction costs and market impact are unchanged — liquidity, spreads, and impact can shift at the same trade frequency. |
| D | False | Policy stability alone does **not** establish that retraining would improve performance — retraining may help or harm and must be assessed, not assumed. |
| E | False | Comparing recent and historical state-action outcomes is **not** unnecessary just because action choices are stable — such comparisons can reveal reward/transition shifts. |

**Reference:** Sutton & Barto, 2nd ed., §2.5 (non-stationarity; why fixed estimates degrade) and ch.1 (monitoring performance); Balch ML4T lectures 03-07 (detecting regime change / when to retrain); Moody & Saffell (2001) (performance monitoring of a trading agent).

## References (domain-level)

1. **Sutton & Barto — *Reinforcement Learning: An Introduction*, 2nd ed.:** §3.1 (agent–environment interface; state as information available at decision time, including agent-internal holdings; actions as controllable choices; feasibility); §3.2 (goals and rewards, the reward hypothesis, reward defines the optimized objective, negative rewards/costs); §3.5 (Markov property; policies vs. value estimates); ch.6 (tabular Q-learning; experience per state and sparsity); §2.5–§2.7 (non-stationary problems, tracking, exploration–exploitation); ch.1 (RL vs. supervised learning; delayed reward; generalization/evaluation); ch.12 (temporal credit assignment).
2. **Balch — ML4T (Georgia Tech):** trading-as-RL / Q-Learning problem-framing lectures (03-05), the Q-Learning-for-trading formulation (03-06), and Dyna / practical-RL and overfitting considerations (03-07); **Project 7** (Q-Learning Robot — discretization, state design, Q-table) and **Project 8** (strategy learner — target-position actions, order generation from holdings, net portfolio-value reward with commissions and market impact, in-sample vs. out-of-sample testing).
3. **Moody & Saffell (2001), "Learning to Trade via Direct Reinforcement" (*IEEE Transactions on Neural Networks*):** direct reinforcement over trading positions, reward defined on returns net of transaction costs, turnover/cost effects, and online/adaptive updating for non-stationary markets (used for G2 action/position design, G4–G5 reward/cost framing, and G7 non-stationarity).
