# ML Domain 6 — State Representation, Discretization & Reward Design

## Domain cheat-sheet

- **What a state must do.** The **state** is the information available *at decision time* that the agent uses to choose an action. A good feature earns its place only if it carries information **relevant to future rewards or to the action choice** — it should help distinguish situations that warrant different decisions. Legitimate state components include external observations (indicators, obstacles, order book) **and** agent-specific internals (current holdings, remaining capacity, time-to-deadline). A variable is not disqualified just because it is "not a market indicator," and it is not qualified just because it correlates with something in-sample.
- **Decision-time availability (no look-ahead).** A deployable state can use **only** information observable when the action is selected. A value known only in the future (e.g., *tomorrow's* closing return) creates **look-ahead leakage** and cannot be supplied live, even though it sits in the historical training file. The same rule bans recomputing discretization thresholds from future deployment data during a historical evaluation.
- **Feature value ≠ in-sample correlation.** A univariate historical correlation does **not** guarantee incremental, policy-relevant value out of sample. **Redundant** encodings of the same information multiply states without adding a useful distinction. A **random unique identifier** makes every historical state unique but destroys generalization and inflates the state space — uniqueness without decision-relevant information is harmful.
- **Discretization / binning tradeoffs.** Binning maps a range of continuous values to one finite label; within a bin, values become **indistinguishable** (e.g., momentum −0.9 and 0.9 can share a middle bin, and distances are not preserved). Membership depends on **boundary locations**, so moving a threshold can relabel an unchanged observation. **Fixed thresholds** learned in one regime can produce badly **imbalanced** bin frequencies after a distribution shift; **rank/percentile (quantile) bins** spread a reference sample more evenly, but the raw value a percentile represents **changes** as the reference distribution changes, so economic meaning is not permanent. Balanced bin counts alone do **not** prove the representation preserves decision-relevant information.
- **Boundary noise & hysteresis.** Hard thresholds make nearly identical observations map to different states, so **sensor/measurement noise near a boundary** causes frequent state switching and action chatter. **Wider bins or hysteresis** can stabilize assignment (at the cost of responsiveness). Binning changes the representation but does **not** remove measurement noise, and two observations in different bins need **not** have different optimal actions.
- **Granularity & the curse of dimensionality.** The tabular state count is the **Cartesian product** of per-feature bins: 5 bins on each of 4 indicators = 5⁴ = 625 states; 10 bins = 10⁴ = 10,000. Doubling bins on every one of 4 dimensions multiplies states by 2⁴ = **16**, not 2. Finer representations distinguish more conditions but **divide a fixed experience history among more states**, leaving fewer visits per state and less reliable Q-estimates. Allocating more table entries does **not** generate additional experience. **Selective refinement** of the one decision-relevant dimension can resolve ambiguity with far less state-space growth than refining all inputs. With 50,000 states but only 2,000 visited, most states got **no direct experience**; unvisited state-action Q-values are just **initialization assumptions** (not true optima), and more exploration or a **generalizing (function-approximation) representation** can improve coverage. Many combinatorial states may be unreachable or irrelevant.
- **Markov sufficiency & state aliasing.** A state is **Markov (sufficient)** when it captures everything about history relevant to future dynamics and rewards; a compact sufficient statistic can be Markov **without** retaining the complete raw history. **State aliasing** occurs when one encoded state hides contexts with different action consequences (robot at aisle 7 arriving from north vs. south; identical price with/without a scheduled earnings event; a long label covering 10% vs. 100% exposure). A memoryless **tabular** policy must assign the *same* action values to the same label, so it cannot act differently on aliased contexts. Fixes: **add the missing observable** (direction, event flag, position magnitude) or **add a history summary** (rolling window) to approximate a Markov state. Accurate measurement of the *included* features does not compensate for a relevant **omitted** variable; a larger Q-table built from the same incomplete inputs cannot distinguish contexts those inputs do not encode; and tuning a hyperparameter (learning rate) cannot supply an omitted variable. A lossy summary can still alias.
- **Holdings/position as state.** The same market signal can require different actions depending on **current inventory** (buy from cash vs. hold when already long vs. reverse from short, which may cross through cash at higher cost). Omitting position causes aliasing and can produce repeated/invalid trades (e.g., buying when already at max long). Position is a valid state variable even though it is agent-controlled, not market-observed. Position-awareness **helps** but does not by itself prevent overtrading, and hard constraints (exposure limits) must still be **enforced in implementation**, not assumed away once holdings are in the state.
- **Reward design — the objective is literally the reward.** The agent optimizes the **reward it is given**, not an unstated business goal. **Realized-only** reward delays feedback while a position stays open (zero realized reward ≠ no economic change); **mark-to-market / daily change in portfolio value** gives denser, more timely feedback that reflects unrealized P&L — provided it uses no future information. **Gross vs. net:** optimizing gross profit when **transaction costs/market impact** are material is misaligned; a net-value reward that deducts costs when trades occur aligns learning with real economics, and higher-turnover policies can reverse their ranking once costs are charged — so costs belong in **training**, not only evaluation. A one-step dollar-profit reward may fail to penalize drawdowns/volatility and its scale depends on portfolio size; summed immediate rewards approximate a long-run objective **only** to the extent the reward definition and discounting are aligned — cumulative optimization cannot recover omitted risk preferences automatically.
- **Reward shaping & reward hacking.** A **shaping term** (per-trade penalty, progress bonus, terminal flat-position bonus) changes action rankings and can change the optimal policy, so it must be **calibrated** to the economic cost/objective it represents — an oversized term can make inactivity (all-cash) or a loophole the reward-maximizing policy. **Reward hacking / unintended incentives:** the learner exploits a loophole in the proxy (drive forward-and-back to re-collect +1/meter; liquidate at the close for the flat bonus then reopen next morning) — this is *successful* reward maximization under a *flawed specification*, not an algorithm failure, and the stakeholder's intent does **not** override the encoded reward. Rewarding **net progress or completion** (rather than repeatable incremental credit) reduces these loops. Validation must examine **total return, costs, risk, and unintended behaviors** — never just the shaped metric. **Potential-based shaping** (Ng, Harada & Russell 1999) is the one shaping form that provably preserves the optimal policy; arbitrary shaping does not.

## Common traps

- **Inverted-polarity questions (9 of 21 here).** When the body says "mark each statement True when the stated claim is **incorrect** and False when it is correct," the Answer Key verdict is flipped relative to the statement's truth: **True = the statement is wrong; False = the statement is accurate.** Read the polarity line *first*. Inverted here: **G1Q1, G2Q3, G3Q1, G3Q3, G4Q1, G4Q3, G5Q3, G6Q2, G7Q2.** The remaining 12 are Normal (True = accurate).
- **Look-ahead leakage.** "Tomorrow's return is a valid feature because it's in the training file" is wrong — a value known only in the future cannot be supplied at live decision time. Same for recomputing bin thresholds from future/deployment data in a historical test.
- **In-sample correlation ⇒ useful feature.** False — univariate marginal association does not guarantee incremental, out-of-sample, policy-relevant value. Redundant features and random unique IDs *expand* the state space while adding little or nothing.
- **"More features / more inputs is always better."** False — irrelevant or overly specific features increase sparsity and hinder learning; representation balances decision-relevant information against complexity and available evidence.
- **Binning preserves information / distances.** False — within-bin values become indistinguishable, distances are not preserved, and three bins do not guarantee that every economically distinct condition gets its own state.
- **Fixed thresholds survive regime change / rank bins fix meaning.** Fixed thresholds imbalance after a distribution shift; rank bins rebalance frequency but their raw-value meaning drifts with the reference window. Balanced counts don't prove an adequate representation.
- **Discretization removes noise / different bins ⇒ different optimal actions.** False — binning doesn't denoise, and different labels don't prove the correct action differs.
- **State-count arithmetic.** Doubling bins on 4 dimensions multiplies states by 2⁴ = 16, not 2. 5⁴ = 625; 10⁴ = 10,000.
- **"A bigger table supplies the data to fill it."** False — more entries ≠ more experience; finer states spread fixed experience thinner. Unvisited Q-values are initialization assumptions, not true optima.
- **State aliasing / Markov.** The same label hiding different-consequence contexts (arrival direction, earnings event, exposure magnitude) breaks the Markov property; a memoryless table can't act differently on the same label. Removing *any* feature doesn't break Markov — only removing information needed for decision-relevant dynamics does. A sufficient compact statistic can be Markov without the full raw history; a lossy summary can still alias. Raising the learning rate / enlarging the table can't supply an omitted variable.
- **Holdings aren't "market" so exclude them.** False — agent-specific variables (position, remaining capacity) are valid state when they change feasible actions, costs, or outcomes. Position-awareness alone doesn't stop overtrading; still enforce hard constraints.
- **Reward = the objective.** The agent optimizes the specified reward, not the intended goal. Realized-only reward delays feedback; zero realized reward ≠ no value change. Gross-profit reward is misaligned when costs are material; costs belong in training. One-step profit need not encode long-run risk-adjusted goals; cumulative optimization can't recover omitted risk preferences.
- **Reward shaping is free / the metric validates itself.** False — shaping can change the optimum, be gamed (reward hacking), and must be calibrated and validated against total economics. Reward hacking is effective maximization of a flawed proxy, not an algorithm bug. Only potential-based shaping (Ng–Harada–Russell 1999) is policy-invariant.
- **Garbled-symbol note.** The source slice contains OCR ligature artifacts — "identiﬁer," "ﬁnite," "deﬁning," "proﬁt," "speciﬁc," "ﬂag," "conﬂicts," etc. (fi/fl rendered as single glyphs) — plus page-footer noise ("506 Rev:081020261230"). Content is unaffected; verdicts are transcribed verbatim.

## Questions

### [ML2-D6G1Q1] Intraday Q-Learner — which proposed features belong in the state
**Scenario:** A quant team designs the state for an intraday long/cash/short Q-Learner. The PM wants to include momentum, volatility, current position, a random per-observation identifier, and *tomorrow's* closing return — but the production system must decide before tomorrow's return is known.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: momentum and volatility are legitimate features when they carry information relevant to future rewards or action choices — they help distinguish situations warranting different decisions. |
| B | False (accurate) | Correct: current position matters because the effect and cost of an action depend on existing holdings (feasible trades, transaction costs, meaning of the action). |
| C | True (incorrect) | Wrong: tomorrow's closing return is known only in the future, so using it is **look-ahead leakage** — it cannot be supplied at live decision time merely because it exists in the historical file. |
| D | True (incorrect) | Wrong: a random unique identifier adds no decision-relevant information; it only prevents generalization and expands the state space. |
| E | False (accurate) | Correct: feature availability at decision time is a necessary design consideration — a deployable state uses only information observable when the action is selected. |

**Reference:** Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed., §3.1 (state signal; the Markov property — what belongs in the state) and ch.9 §9.5 (feature construction and generalization); on avoiding future information, Balch ML4T Q-Learning / "Dyna" trading-state construction lectures.

### [ML2-D6G1Q2] Daily agent — adding volatility and time-to-liquidation features
**Scenario:** A risk committee reviews a daily agent whose state holds only a short-term price oscillator. Identical oscillator readings have produced different preferred trades depending on volatility and time remaining before a mandatory end-of-day liquidation; should those be added?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Volatility is relevant if it changes the distribution of outcomes associated with an action — action values can differ even when the oscillator is unchanged. |
| B | True | Time remaining is relevant under a deadline-dependent liquidation constraint; the consequences of entering/holding depend on the remaining horizon. |
| C | False | A feature need not be a technical indicator to be valid — state variables may describe the environment, constraints, or agent status. |
| D | True | Adding a relevant feature can separate observations that previously shared one aliased state (distinguishing decision-relevant contexts). |
| E | False | Adding *every* available feature is not guaranteed to help — irrelevant or overly specific features increase sparsity and can hinder learning. |

**Reference:** Sutton & Barto, 2nd ed., §3.1 (state sufficiency / Markov property) and §17.3 (observations and state — when added information resolves aliasing); ch.9 §9.5 (feature relevance vs. complexity). Balch ML4T trading-state lectures.

### [ML2-D6G1Q3] Forty univariate-correlation features — curse of dimensionality
**Scenario:** A PM proposes adding 40 features to a tabular Q-Learner because each improved a univariate correlation statistic in-sample. The quant lead warns history is limited, several features are redundant, and every selected feature gets discretized.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | In-sample univariate marginal association does not guarantee incremental or policy-relevant value out of sample. |
| B | True | Redundant features multiply the encoded state space without adding a useful distinction (multiple encodings of similar information). |
| C | True | With fixed data, adding many discretized features increases **sparse visitation** — more feature combinations divide the same experience among more states. |
| D | False | State selection should not maximize inputs regardless of sample size; it balances decision-relevant information against complexity and available evidence. |
| E | False | Removing an irrelevant feature does not break the Markov property — Markov is lost only if the omitted information is needed to characterize decision-relevant dynamics. |

**Reference:** Sutton & Barto, 2nd ed., ch.9 (on-policy prediction with approximation; curse of dimensionality, generalization, and sparse coverage) and §3.1 (Markov property). Balch ML4T Q-Learning state-design lectures.

### [ML2-D6G2Q1] Three-bin momentum — binning loses within-bin distinction
**Scenario:** A desk maps continuous momentum into three states (below −1 = low; −1 through 1 = middle; above 1 = high). The head trader asks how −0.9 and 0.9 can receive the same state despite different raw values.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Discretization intentionally maps multiple continuous observations to one finite state label (binning groups ranges). |
| B | True | Under the stated inclusive mapping, both −0.9 and 0.9 fall within the −1-through-1 middle bin. |
| C | False | The mapping does not preserve exact distances — values within a bin become indistinguishable in the discrete representation. |
| D | True | Moving a threshold can change the discrete state assigned to an unchanged observation — membership depends on boundary locations. |
| E | False | Three bins do not guarantee a distinct state for every economically distinct condition — important differences may be combined within a bin. |

**Reference:** Sutton & Barto, 2nd ed., ch.9 §9.5 (coarse coding / tile coding; how bin width and boundaries control resolution and generalization). Balch ML4T discretization lectures.

### [ML2-D6G2Q2] Fixed vs. percentile-rank bins under distribution shift
**Scenario:** A manager uses fixed volatility thresholds learned in a calm period; in a high-volatility deployment nearly every observation lands in the top bin, so the research director considers percentile-rank bins recomputed from an appropriate reference window.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Fixed thresholds can produce highly imbalanced state frequencies after a distribution shift (observations concentrate on one side of regime-specific boundaries). |
| B | True | Rank-based (quantile) bins are designed to distribute reference observations more evenly across ranked groups. |
| C | False | Rank-based discretization does not make a bin's economic meaning permanently identical — the raw value a percentile represents changes as the reference distribution changes. |
| D | True | Recomputing thresholds using future deployment data would create **look-ahead bias** in a historical evaluation. |
| E | False | Balanced bin counts alone do not prove the representation preserves all decision-relevant information or supports an optimal policy. |

**Reference:** Sutton & Barto, 2nd ed., ch.9 §9.5 (feature construction; resolution choices) and §3.1 (state sufficiency); on look-ahead / out-of-sample integrity, Balch ML4T evaluation lectures.

### [ML2-D6G2Q3] Obstacle-distance bins — boundary noise and hysteresis
**Scenario:** A robotics team discretizes distance to an obstacle into near/medium/far. Readings just below and just above the "near" boundary make the controller alternate actions, though sensor noise — not a real environmental change — explains the difference.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: hard thresholds can make nearly identical continuous observations map to different states (a small change crosses a categorical boundary). |
| B | False (accurate) | Correct: sensor noise near a boundary can cause frequent state switching as repeated noisy crossings alternate the encoded state. |
| C | False (accurate) | Correct: wider bins or hysteresis can stabilize state assignment against small boundary-crossing noise (though they may reduce responsiveness). |
| D | True (incorrect) | Wrong: discretization changes the representation but does **not** eliminate measurement noise or guarantee noisy values are assigned appropriately. |
| E | True (incorrect) | Wrong: two observations in different bins need not have materially different optimal actions — different labels don't prove the decision should differ. |

**Reference:** Sutton & Barto, 2nd ed., ch.9 §9.5 (coarse/tile coding; bin width vs. responsiveness and stability); on partial observability/noise and the state signal, §17.3. Balch ML4T discretization lectures.

### [ML2-D6G3Q1] Five vs. ten bins across four indicators — Cartesian growth
**Scenario:** A tabular learner uses four continuous indicators. The researcher proposes raising each from 5 to 10 bins with the same training history; the PM asks about the effect on the state table.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: with all combinations represented, 5 bins per indicator yield 5⁴ = 625 states (the Cartesian product). |
| B | False (accurate) | Correct: 10 bins per indicator give 10⁴ = 10,000 states (ten choices for each of four dimensions). |
| C | True (incorrect) | Wrong: doubling bins on all four indicators multiplies the state count by 2⁴ = 16, not by two. |
| D | False (accurate) | Correct: the finer representation distinguishes more conditions but divides a fixed experience history among more states (fewer visits per state). |
| E | True (incorrect) | Wrong: a larger state table does not automatically supply the extra observations needed to estimate its Q-values — allocating entries doesn't generate experience. |

**Reference:** Sutton & Barto, 2nd ed., ch.9 (curse of dimensionality; why finer tabular resolution spreads fixed experience thinner) and §3.1. Balch ML4T state-space / Q-table lectures.

### [ML2-D6G3Q2] Coarse navigation bins — selective refinement
**Scenario:** A navigation learner with very coarse bins reaches the goal but takes inefficient routes because it cannot distinguish two corridor positions needing opposite turns. The manager considers refining only the location dimension causing the ambiguity.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The coarse representation generalizes across observations that should require different actions (it stores one action value for both positions). |
| B | True | Selectively refining the decision-relevant dimension can resolve the ambiguity with far less state-space growth than refining every dimension. |
| C | False | Finer bins are not guaranteed to improve deployment performance — insufficient visits can make the finer estimates unreliable. |
| D | True | More granular states can require additional experience before their action values stabilize (experience spreads over more state-action entries). |
| E | False | Coarse discretization does not use more memory than fine — coarser representations generally contain fewer states and need less table memory. |

**Reference:** Sutton & Barto, 2nd ed., ch.9 §9.5 (adaptive/variable resolution; refining only where needed) and §3.1 (state sufficiency vs. aliasing). Balch ML4T discretization lectures.

### [ML2-D6G3Q3] Fifty-thousand states, two-thousand visited — sparse coverage
**Scenario:** A trading agent has 50,000 discrete states and three actions, but the training run visits only 2,000 states. The head of validation asks what can be concluded about the unvisited portion of the Q-table.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: most possible states received no direct experience — only 2,000 of 50,000 encoded states were observed. |
| B | False (accurate) | Correct: Q-values for unvisited state-action pairs cannot have been empirically updated, since a direct update requires encountering the state and choosing the action. |
| C | True (incorrect) | Wrong: initial Q-values for unvisited pairs need not equal true optimal values — initialization is an assumption. |
| D | False (accurate) | Correct: more exploration or a representation that generalizes across observations (function approximation) can improve coverage of a sparse table. |
| E | True (incorrect) | Wrong: many unvisited states do not prove all 50,000 combinations are reachable — some combinatorial states may be impossible or irrelevant. |

**Reference:** Sutton & Barto, 2nd ed., ch.9 (generalization/function approximation to cover sparsely visited state spaces), ch.2 & ch.5 (exploration; optimistic initialization as an assumption). Balch ML4T Q-Learning coverage/exploration lectures.

### [ML2-D6G4Q1] Warehouse robot — aisle-only state aliases arrival direction
**Scenario:** A warehouse robot observes only its current aisle. At aisle 7, turning left is safe if it arrived from the north but collides if from the south; the operations manager asks why the learner keeps assigning one value to the action.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the representation aliases two decision-relevant situations into the same observed state (hiding contexts with different action consequences). |
| B | False (accurate) | Correct: if direction of arrival predicts the transition, adding it to the state can resolve the ambiguity (it supplies the needed history). |
| C | True (incorrect) | Wrong: a memoryless tabular policy cannot choose different actions for the two cases while they share the same state label and no other memory. |
| D | False (accurate) | Correct: the current aisle alone may fail to be a Markov state — relevant transition information depends on history the state doesn't capture. |
| E | True (incorrect) | Wrong: increasing the learning rate cannot make missing directional information observable — a parameter change can't supply an omitted variable. |

**Reference:** Sutton & Barto, 2nd ed., §17.3 (observations and state; partial observability / state aliasing) and §3.1 (the Markov property). Balch ML4T state-construction lectures.

### [ML2-D6G4Q2] Omitted earnings-announcement flag — event aliasing
**Scenario:** A trading agent's state has current price and momentum but omits whether an earnings announcement is scheduled before the next decision. The same encoded state has ordinary risk most days and event-driven risk on announcement days.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The omitted event status can cause state aliasing if it changes action outcomes (event and non-event conditions share one state). |
| B | True | Adding an observable announcement flag can make represented transition and reward behavior more consistent within each state (separating risk/reward regimes). |
| C | False | Identical current prices do not imply identical future reward distributions — other conditions can alter the distribution of future outcomes. |
| D | True | The state can be inadequate even if every included feature is measured accurately — accuracy doesn't compensate for a relevant omitted variable. |
| E | False | A larger Q-table built from the same incomplete state variables cannot fix the missing-information problem — more entries from unchanged inputs can't encode an un-included context. |

**Reference:** Sutton & Barto, 2nd ed., §17.3 (observations and state; aliasing from omitted relevant variables) and §3.1 (Markov sufficiency). Balch ML4T state-design lectures.

### [ML2-D6G4Q3] Partially observable wear — rolling history summary
**Scenario:** A maintenance system cannot directly measure machine wear. The lead proposes adding a rolling summary of recent vibration readings because the current reading alone produces inconsistent failure probabilities.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a history summary can provide information about a hidden condition the current observation misses (recent patterns reveal accumulated wear). |
| B | False (accurate) | Correct: adding recent history can help approximate a Markov state when dynamics otherwise depend on the past (an appropriate summary encodes relevant past information). |
| C | True (incorrect) | Wrong: no rolling summary is *guaranteed* to capture all hidden information — a lossy or poorly chosen summary may omit important distinctions. |
| D | False (accurate) | Correct: if two different histories produce the same summary, relevant aliasing can still remain (compression can combine different-consequence histories). |
| E | True (incorrect) | Wrong: the Markov property does not require the complete raw history — a sufficient compact statistic can be Markov without retaining every raw observation. |

**Reference:** Sutton & Barto, 2nd ed., §17.3 (observations and state; constructing an approximate state / state-update from history under partial observability) and §3.1 (Markov property; sufficient statistics). Balch ML4T state-construction lectures.

### [ML2-D6G5Q1] Omitting position causes repeated buys at max long
**Scenario:** A learner defines market states from technical indicators but omits the current portfolio position. It sometimes issues repeated buy actions even when already at maximum long.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The same market indicators can require different actions depending on current holdings — action desirability depends partly on inventory. |
| B | True | Omitting holdings can create state aliasing (distinct portfolio conditions mapped to the same state). |
| C | False | Repeated buy actions are not always harmless — they may create invalid, redundant, or costly trades. |
| D | True | Including position status helps the learner distinguish entering a position from maintaining one (position-aware states support better action selection). |
| E | True | Position information can be part of the state even though it is not a market indicator — state variables may include agent-specific information. |

**Reference:** Sutton & Barto, 2nd ed., §3.1 (state can combine external observations with agent internals; Markov sufficiency). Balch ML4T trading-state / holdings lectures.

### [ML2-D6G5Q2] Short/cash/long targets — position-dependent trades
**Scenario:** A learner chooses target positions short/cash/long. With the same bullish signal, buying is right from cash, holding may be right when already long, and buying from short may require a larger trade crossing through cash; the execution manager wants these cases represented explicitly.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Market indicators alone may be insufficient to distinguish the three decision contexts — the action needed to reach/maintain exposure depends on starting inventory. |
| B | True | Encoding current target position lets the same signal-position combinations carry their own Q-values. |
| C | True | Moving from short to long can incur different transaction costs than remaining long (reversing exposure generally trades more units). |
| D | False | Holdings should not be excluded for being agent-controlled — agent-specific variables are valid state when they affect consequences or choices. |
| E | False | Adding position to the state does not guarantee no overtrading — policy, reward, exploration, and implementation can still generate excess trades. |

**Reference:** Sutton & Barto, 2nd ed., §3.1 (state components including agent internals). Balch ML4T lectures on actions vs. orders, target positions, and holdings.

### [ML2-D6G5Q3] Leveraged 10% vs. 100% long — magnitude aliasing
**Scenario:** A leveraged agent uses the same directional label "long" for both 10% and 100% allocations. An additional buy is feasible at 10% but violates the exposure limit at 100%.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a three-valued long/cash/short encoding can alias materially different inventory levels (the coarse label hides exposure differences). |
| B | False (accurate) | Correct: including position magnitude or remaining capacity helps distinguish feasible actions (revealing whether risk capacity remains). |
| C | True (incorrect) | Wrong: the same "long" label does not prove additional buying has the same risk — 100% is at the exposure limit while 10% is not. |
| D | False (accurate) | Correct: a state should include constraint-relevant information when it changes available actions or outcomes (a useful state distinguishes conditions that alter the decision problem). |
| E | True (incorrect) | Wrong: action validation is still necessary even with holdings in the state — implementation must enforce hard constraints regardless. |

**Reference:** Sutton & Barto, 2nd ed., §3.1 (state sufficiency; constraint-relevant internals) and §17.3 (aliasing). Balch ML4T holdings/position and risk-constraint lectures.

### [ML2-D6G6Q1] Realized-only vs. mark-to-market daily value change
**Scenario:** A daily learner is rewarded only when it closes a position and realizes a gain/loss. A position can carry a large unrealized loss for days at zero reward; the PM asks whether daily change in total portfolio value is a better signal.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A realized-only reward delays feedback while a position stays open — no gain/loss is recognized until a closing transaction. |
| B | True | Daily change in portfolio value reflects both realized and unrealized gains/losses (marking current holdings to market). |
| C | False | A zero *realized* reward does not prove the portfolio's economic value was unchanged — open positions can gain or lose value without realization. |
| D | True | A denser value-change reward can improve temporal feedback — provided it is computed without future information. |
| E | False | Mark-to-market reward does not automatically eliminate risk-taking incentives — the learner can still prefer risky actions if expected reward favors them and risk isn't otherwise represented. |

**Reference:** Sutton & Barto, 2nd ed., §3.2 (goals and rewards) and §17.4 (designing reward signals — timing/density of feedback). Balch ML4T reward-timing / daily-return lectures.

### [ML2-D6G6Q2] Gross-profit reward vs. net-value objective (costs)
**Scenario:** A brokerage trains an agent to maximize gross trading profit but deploys it in an account paying commissions and market impact. The learned strategy makes many small gross-profit trades that lose money after costs.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: gross profit is misaligned with the net-value objective when costs are economically material (it omits an important component of actual performance). |
| B | False (accurate) | Correct: a reward based on net portfolio-value change can incorporate transaction costs, aligning the signal with realized economics. |
| C | False (accurate) | Correct: the policy can rationally exploit trades profitable under the specified reward even if they lose under the true objective — the learner optimizes the reward it is given. |
| D | True (incorrect) | Wrong: transaction costs do not matter only at evaluation — including realistic costs during *training* can be essential to selecting a viable policy. |
| E | True (incorrect) | Wrong: maximizing gross reward does not guarantee maximizing net reward — higher-turnover policies can incur enough cost to reverse their ranking. |

**Reference:** Sutton & Barto, 2nd ed., §3.2 (the reward defines the objective) and §17.4 (designing reward signals; reward–objective alignment). Balch ML4T gross-vs-net reward and transaction-cost lectures.

### [ML2-D6G6Q3] One-step dollar profit vs. long-run risk-adjusted objective
**Scenario:** A fund's stated objective is long-run risk-adjusted growth, but its RL agent is rewarded only by the next day's raw dollar profit. The committee asks whether this one-step signal fully specifies the objective.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Immediate dollar profit may fail to penalize paths with unacceptable drawdowns or volatility — equal profits can come from very different risk paths. |
| B | True | The scale of dollar rewards depends on portfolio size, complicating comparisons across episodes with different capital. |
| C | True | Summing immediate rewards represents a longer-run objective only to the extent the reward definition and discounting align with it. |
| D | False | Because Q-Learning uses cumulative reward does not mean any arbitrary immediate reward yields the desired risk-adjusted policy — cumulative optimization can't recover omitted risk preferences. |
| E | False | Reward design is not unrelated to optimized behavior — reward is the numerical objective that directs policy learning. |

**Reference:** Sutton & Barto, 2nd ed., §3.2–§3.4 (reward hypothesis; returns and discounting) and §17.4 (designing reward signals for the intended objective). Balch ML4T reward-definition / risk-adjusted-objective lectures.

### [ML2-D6G7Q1] Per-trade penalty calibration
**Scenario:** A team adds a fixed penalty per transaction to discourage turnover. The PM wants lower costs but worries a very large penalty will keep the learner in cash even when attractive opportunities arise.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A per-trade penalty makes otherwise equal high-turnover behavior less attractive (each transaction reduces shaped return). |
| B | True | If the penalty greatly exceeds plausible trading gains, inactivity can become the reward-maximizing policy (avoiding all trades avoids the oversized penalty). |
| C | True | The penalty should be calibrated to the economic cost or objective it represents, so the shaping term doesn't overwhelm the true objective. |
| D | False | Adding any nonzero turnover penalty does not guarantee higher net returns out of sample — lower turnover doesn't guarantee better decisions. |
| E | False | Reward shaping *can* change the optimal policy — an arbitrary shaping term can alter action rankings and the learned optimum. |

**Reference:** Sutton & Barto, 2nd ed., §17.4 (designing reward signals); Ng, Harada & Russell (1999), "Policy invariance under reward transformations" — only potential-based shaping is policy-invariant; arbitrary shaping changes the optimum. Balch ML4T turnover-penalty / reward-shaping lectures.

### [ML2-D6G7Q2] Delivery robot +1/meter — reward hacking loop
**Scenario:** A delivery robot gets +1 per meter moved toward its destination and −100 only if it collides. It repeatedly moves forward and backward near the goal, collecting fresh +1 on each forward move without completing the delivery.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the robot is exploiting the specified reward rather than accomplishing the intended task (the cycle earns shaped reward while avoiding the unstated completion objective). |
| B | False (accurate) | Correct: this is an unintended incentive / conceptual reward hacking — the learner found a loophole in the proxy reward. |
| C | False (accurate) | Correct: rewarding net progress or successful completion removes/reduces repeated credit for the same progress, shrinking the back-and-forth loop. |
| D | True (incorrect) | Wrong: the behavior does not prove the algorithm failed to maximize reward — it is effective maximization under a flawed specification. |
| E | True (incorrect) | Wrong: a stakeholder's intended objective does not automatically override the numerical reward — the learner responds to encoded feedback, not intention. |

**Reference:** Sutton & Barto, 2nd ed., §3.2 (reward defines the objective) and §17.4 (designing reward signals; pitfalls of proxy rewards / reward hacking); Ng, Harada & Russell (1999), potential-based shaping (rewarding progress safely). Balch ML4T reward-hacking lectures.

### [ML2-D6G7Q3] Terminal flat-position bonus — liquidate-and-reopen gaming
**Scenario:** A risk manager adds a large bonus when a trading agent ends the day with no open position, hoping to cut overnight exposure. Backtests show it liquidates profitable positions just before the close and reopens them next morning, raising costs and sometimes worsening risk-adjusted returns.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The liquidation pattern can be a rational response to the terminal flat-position bonus — the agent collects the encoded bonus even when it conflicts with broader economics. |
| B | False | The bonus does not necessarily improve the fund's true risk-adjusted objective — costs, lost opportunities, and other risks can offset the reduced overnight exposure. |
| C | True | Reopening costs show a locally appealing shaping term can create undesirable system-level behavior (optimizing the proxy harms the broader objective). |
| D | False | Increasing the bonus is not guaranteed to eliminate the morning re-entry — a larger bonus further favors liquidation but doesn't remove the incentive to reopen. |
| E | False | Checking only whether the agent ends flat is insufficient validation — it must examine total returns, costs, risk, and unintended behaviors, not just the shaped metric. |

**Reference:** Sutton & Barto, 2nd ed., §17.4 (designing reward signals; unintended consequences of shaped terminal rewards); Ng, Harada & Russell (1999), potential-based shaping and policy invariance. Balch ML4T reward-shaping / validation lectures.

## References (domain-level)

1. **Sutton & Barto — *Reinforcement Learning: An Introduction*, 2nd ed.:** §3.1 (agent–environment interface; the **state signal and the Markov property**; what information belongs in the state; sufficient statistics); §3.2 (goals and rewards; the reward hypothesis; the reward *defines* the optimized objective); §3.3–§3.4 (returns = cumulative reward; discounting; how summed immediate rewards induce the long-run objective); ch.9 (**On-policy Prediction with Approximation** — generalization and function approximation; §9.5 **feature construction**, coarse coding and tile coding; resolution/granularity vs. the **curse of dimensionality** and sparse coverage); §17.3 (**Observations and State** — partial observability, state aliasing, constructing an approximate/Markov state from history); §17.4 (**Designing Reward Signals** — reward density/timing, reward–objective alignment, proxy rewards and reward hacking).
2. **Reward shaping / policy invariance:** Ng, Harada & Russell (1999), "Policy invariance under reward transformations: Theory and application to reward shaping" — **potential-based shaping** is the shaping form that provably preserves the optimal policy; arbitrary shaping terms can change the learned optimum (G7 questions; also G6).
3. **Balch — ML4T (Georgia Tech):** Q-Learning / "The Dyna Architecture" and trading-as-RL lectures — mapping market data into discretized states, avoiding future information, holdings/position as state, actions vs. orders, reward timing (daily return / change in portfolio value), gross vs. net reward and transaction costs, and reward-shaping/turnover-penalty cautions (section level).
