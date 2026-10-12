# ML Domain 3 — Q-Learning Mechanics

## Domain cheat-sheet

- **The Q-table and what a Q-value *is*.** Tabular Q-learning stores one entry **Q(s,a)** per (state, action) pair — a table with `#states × #actions` cells (4 states × 3 actions = 12 entries). Each entry is an **estimate of the action value**: the expected *discounted cumulative return* from taking action `a` in state `s` and thereafter following the (greedy) target policy. A Q-value is therefore **not** a transition probability, **not** a guaranteed next state, and **not** the last immediate reward observed — it is a learned expectation that can fold in many past updates and bootstrapped future value. Reading one cell `Q[s,a]` in isolation does **not** tell you whether that action is greedy; greediness is a **relative** comparison *within the same row* (across the actions available in that state), so you need the whole row. Action rankings are **state-specific** — the best action in one row says nothing about another row.
- **Greedy action selection & ties.** A **greedy** policy picks `argmax_a Q(s,a)` — the largest value *in the current state's row*. A **negative** Q-value can still be greedy if every other action in that row is lower (comparison is relative, not about the sign). When values **tie** at the row maximum, every tied action is equally "greedy with respect to the table": a deterministic first-index rule returns the earliest tied column, while a valid random tie-break chooses among the maximizers — both remain greedy. **Equal estimates do not prove equal true values** (finite, noisy data can make distinct true values tie), and a tie supplies a *choice* but not learned *preference*.
- **The temporal-difference (TD) update — off-policy TD control.** Q-learning is a **model-free, off-policy TD control** algorithm. On each observed transition `s → a → r → s'`:
  - **One-step target:** `target = r + γ · max_a' Q(s', a')` — the observed reward plus the **discounted maximum** successor estimate. (For a **terminal** `s'`, continuation value is 0, so `target = r` — the reward is counted exactly **once**.)
  - **TD error:** `δ = target − Q(s,a)`.
  - **Update:** `Q(s,a) ← Q(s,a) + α · δ = Q(s,a) + α·[r + γ·max_a' Q(s',a') − Q(s,a)]`.
  - The target uses `max_a'` (the greedy/target policy) **regardless of which action the behavior policy actually takes next** — that `max` is exactly what makes Q-learning **off-policy**. Worked values from this domain: `r=1, γ=0.9, maxQ'=4.0, Q=2.0, α=0.5` → target `4.6`, new `3.3`; `r=−2, γ=0.5, maxQ'=3, Q=5, α=0.2` → target `−0.5`, δ `−5.5`, new `3.9`.
- **Learning rate α (step size).** α ∈ [0,1] sets how far the estimate moves toward the target: `new = old + α·(target − old)`.
  - **α = 1** fully **replaces** the old estimate with the target (it does *not* ignore the transition — that is the opposite error). **α = 0** multiplies the TD error by zero → **no update** (the estimate is **frozen**, not erased — old experience is retained, not forgotten).
  - A **larger** α weights the newest sample more heavily and adapts faster; a **smaller** α moves a smaller fraction per update and adapts more gradually. A **constant** α performs a *recency-weighted* (exponential) average — it does **not** weight all history equally; recent samples dominate, so with noisy targets estimates keep swinging. **Decaying α** over time dampens the influence of individual late/noisy samples and supports stability in a **stationary** task (the Robbins–Monro conditions `Σα=∞, Σα²<∞` underpin convergence).
  - A lower α does **not** *guarantee* a better final policy; outcome also depends on sampling, coverage, schedules, and (non)stationarity.
- **Discount factor γ.** γ ∈ [0,1] weights **future** reward: successor value enters the target as `γ·max_a' Q(s',a')`. **Higher γ → delayed payoffs matter more** (less penalty on the future); **lower γ → short-sighted** valuation that emphasizes near rewards over distant costs. γ scales *successor* value only — in the one-step target the **immediate reward r is not discounted**. Changing γ can change the **learned policy even when the reward function is unchanged**, because it changes the objective's time preference. γ does **not** control exploration (that is ε / random-action rate). `γ=0` makes the target just `r`; a finite **episodic** task can use `γ=1` without inevitable divergence.
- **The max operator & overestimation.** Bootstrapping from `max_a' Q(s',a')` means an **inflated successor estimate propagates backward** into predecessor targets. Because the `max` **selects one estimate** (it does not average and cannot cancel noise), it preferentially picks positive errors → **maximization/overestimation bias**, especially early with poorly sampled actions. More **representative experience** corrects the inflated entry and later targets. The `max` is taken over *current, possibly inaccurate* estimates — it does **not** prove an action is truly optimal.
- **Off-policy = behavior ≠ target.** The **behavior policy** (e.g., ε-greedy) generates experience, including exploratory and losing actions; the **target policy** is greedy via the `max`. Exploratory transitions are **fully usable** — they update the preceding (s,a) and are a key source of state-action **coverage**. Off-policy learning does **not** require the behavior to act greedily, and the exploratory action is **not relabeled** as greedy — the *current* action's entry is updated while the *successor* target stays greedy. On- vs. off-policy is determined by the **target–behavior relationship** (does the target bootstrap from `max`, or from the next action actually taken?), **not** by the mere use of a value table. (Contrast: SARSA, on-policy, bootstraps from the action actually chosen.)
- **Initialization, visitation, convergence.** Unvisited rows **still reflect their initialization**, not learned evidence — zeros (or any init) are not proof of true returns, and a tie-break there yields an arbitrary, uninformative choice. **Tabular updates touch only the experienced (s,a) entry** — visiting other states does **not** update an unvisited row. **Optimistic initialization** (e.g., all 100) can encourage early exploration (updated entries drop below still-optimistic unvisited ones), but does **not** guarantee every pair is visited, nor a superior final policy. Q-learning **converges** to optimal `Q*` under the classic conditions — **all relevant (s,a) pairs visited infinitely often**, a suitable (decaying) step-size schedule, and (greedy-in-the-limit) exploration — in a **finite, stationary** task. Values *changing less* is **not** by itself proof of global optimality (bias, poor representation, or thin coverage can masquerade as convergence); a single pass per pair is **not** sufficient. In **nonstationary** environments a permanent fixed point is **not** guaranteed, and a nonzero α is needed to keep adapting.

## Common traps

- **Inverted-polarity questions (9 of 21 here).** When the body says "mark each statement **True** when the stated claim is **incorrect** and **False** when it is correct," the Answer-Key verdict is flipped relative to the statement's truth: **True = the statement is wrong; False = the statement is accurate.** Read the polarity line *first*. Inverted here: **G1Q1, G2Q3, G3Q2, G3Q3, G4Q3, G5Q1, G6Q2, G7Q1, G7Q2.** The remaining 12 are Normal (True = accurate).
- **Q-value = probability / next state / last reward.** All wrong. A Q-value estimates **expected discounted return** for one (s,a) pair — not a transition probability, not a deterministic next state, not the most recent immediate reward.
- **"Highest value in this row ⇒ best in every state."** False — action rankings are **state-specific**; another row can favor a different action.
- **One cell decides greediness.** False — greedy is a **relative** comparison across the whole row; a single `Q[s,a]` (even a negative one) is insufficient on its own.
- **Ties.** Equal estimates do **not** prove equal true values; first-index and random tie-breaks are *both* greedy w.r.t. the table; a tie gives a choice, not a learned preference.
- **α = 1 "ignores" the transition.** Backwards — α=1 **fully adopts** the target. α=0 gives **no update** and **freezes** (does not erase) the estimate.
- **Constant α averages all history equally.** False — constant-step is **recency-weighted**; recent samples dominate, so noisy targets keep estimates swinging. Decaying α aids stability in stationary tasks.
- **Immediate reward gets discounted.** False — in the one-step target, γ scales only the **successor** value; `r` is undiscounted.
- **Lower γ raises weight on delayed reward.** Backwards — lower γ gives the future **less** weight (short-sighted). γ does **not** control exploration.
- **Changing γ can't change the policy if the reward is unchanged.** False — γ changes the time preference, hence the action-value comparison and the learned policy.
- **The target uses the action behavior takes next.** False for Q-learning — the target uses `max_a' Q(s',a')` (greedy), independent of the exploratory action taken. Using the next *behavior* action is **on-policy (SARSA)** reasoning.
- **The max cancels noise / only underestimates matter.** False — the `max` selects one estimate (no averaging) and preferentially picks **positive** errors → overestimation bias; the concern is **spuriously high** estimates.
- **Terminal reward counted twice / add a successor max after termination.** False — terminal continuation value is 0, so `target = r` once; a reset belongs to a **new** episode, not a continuation.
- **Exploratory transitions are useless.** False — experience from exploration updates the preceding (s,a) and supplies coverage; off-policy does **not** require greedy behavior, and the explored action is **not relabeled** as greedy.
- **A value table ⇒ on-policy.** False — on/off-policy is set by the **target–behavior relationship**, not by using a Q-table.
- **Unvisited rows are learned / updates touch every row.** False — an unvisited row reflects **initialization**; tabular updates modify only the **experienced** (s,a) entry.
- **Optimistic init guarantees full visitation / a better policy.** False on both — it can *encourage* early exploration but guarantees neither coverage nor superior final performance.
- **Values settling ⇒ optimal policy / one pass suffices / convergence guaranteed in a changing world.** All false — apparent stability can hide bias/poor coverage; stochastic, bootstrapped learning needs repeated updates; nonstationarity removes the fixed-point guarantee.

## Questions

### [ML2-D3G1Q1] Trading Q-table — size, meaning of a Q-value, greedy choice
**Scenario:** A trading learner uses 4 discrete market states and 3 actions (short/cash/long), one Q-table row per state, one column per action. In State 2 the estimates are short = −0.4, cash = 0.7, long = 1.3. Verify claims about table size, the meaning of 1.3, the greedy choice, and generalization.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a tabular Q-function has `#states × #actions` entries = 4 × 3 = **12**. The claim is right, so the inverted verdict is False. |
| B | False (accurate) | Correct: 1.3 is the estimated **action value** of choosing `long` in State 2 and thereafter following the policy represented by the learned values — exactly what a Q-value is. |
| C | False (accurate) | Correct: greedy selection takes `argmax_a Q(s,a)` within the current row; 1.3 is the row max, so `long` is greedy in State 2. |
| D | True (incorrect) | Wrong: Q-values estimate **expected discounted returns**, not next-state **transition probabilities** — the row is not a probability distribution over successor states. |
| E | True (incorrect) | Wrong: action rankings are **state-specific**; `long` being best in State 2's row does not make it best in every state — another row can favor another action. |

**Reference:** Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed., §6.5 (Q-learning; the action-value table) with §3.5–§3.6 (action values vs. transition dynamics); Watkins & Dayan (1992), "Q-learning" (definition of Q(s,a) as an action-value estimate); Balch ML4T Q-Learning lectures (03-05/03-06).

### [ML2-D3G1Q2] Warehouse robot — greedy argmax with tied values
**Scenario:** A warehouse robot's State `loading_dock` has wait = 2.1, move_north = 2.1, move_east = 0.5. A greedy policy applies argmax to the row; the library returns the first index on ties.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Both `wait` and `move_north` attain the row maximum of 2.1, so both are greedy-maximizing actions under the learned estimates. |
| B | True | A first-index tie rule returns the earliest maximizing column, so `wait` is chosen if it is stored before `move_north`. |
| C | False | Equal **estimates** need not imply equal **true** expected returns — finite, noisy sampling can make distinct true values appear tied. |
| D | True | Randomly choosing among the maximizing actions is still greedy *with respect to the table* — any valid tie-break over the maximizers preserves greediness. |
| E | False | Action selection for the current state compares actions **within its own row**; values in other state rows are irrelevant to the choice in `loading_dock`. |

**Reference:** Sutton & Barto, 2nd ed., §6.5 (greedy action selection in Q-learning) and §2.3–§2.7 (argmax, tie-breaking, estimates vs. true values); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G1Q3] Reading one Q-cell — Q[7,1] = −3.0
**Scenario:** States 0–9, actions 0–2. A reviewer sees Q[7,1] = −3.0 and claims this single entry completely describes what happens after Action 1 in State 7.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The row/column index identifies exactly one (state, action) pair — State 7, Action 1. |
| B | True | A **negative** Q-value can still be the greedy choice if the other actions in State 7 have even lower values — greediness is relative within the row. |
| C | False | A Q-value estimates **return**, not a guaranteed next state; it does not encode the exact successor the environment will produce. |
| D | False | The estimate can combine **many updates** and bootstrapped discounted future value — it is not necessarily the immediate reward from the most recent visit. |
| E | False | Determining whether Action 1 is greedy requires the **other action values in the same row** for comparison; Q[7,1] alone is insufficient. |

**Reference:** Sutton & Barto, 2nd ed., §6.5 (Q-learning update and bootstrapping) and §3.5 (action values as expected returns, not dynamics); Watkins & Dayan (1992); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G2Q1] TD update — target, step size, and the α = 1 case
**Scenario:** A Q-Learner observes a transition with current Q = 2.0, reward = 1.0, γ = 0.9, max next-state Q = 4.0, α = 0.5. The team reviews how the TD update changes the estimate.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The one-step Q-learning target is `r + γ·max_a' Q(s',a') = 1.0 + 0.9 × 4.0`. |
| B | True | `1.0 + (0.9 × 4.0) = 1.0 + 3.6 = 4.6`. |
| C | True | With α = 0.5 the update moves the estimate **halfway** from the old value toward the target. |
| D | True | `Q ← 2.0 + 0.5 × (4.6 − 2.0) = 2.0 + 1.3 = 3.3`. |
| E | False | α = 1.0 would **fully replace** the old estimate with the target (not ignore the transition) — full replacement, the opposite of ignoring it. |

**Reference:** Sutton & Barto, 2nd ed., §6.5 (Q-learning update rule `Q ← Q + α[r + γ max_a' Q(s',a') − Q]`) and §6.1 (TD target, step size); Watkins & Dayan (1992); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G2Q2] TD update with a negative reward — target, error, direction
**Scenario:** A learner observes `s → a → s'` with Q(s,a) = 5, reward = −2, max Q(s',·) = 3, γ = 0.5, α = 0.2.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Target = `r + γ·max Q(s',·) = −2 + 0.5 × 3 = −0.5` — observed reward plus discounted successor estimate. |
| B | True | TD error = `target − Q(s,a) = −0.5 − 5 = −5.5`. |
| C | True | `Q ← 5 + 0.2 × (−5.5) = 5 − 1.1 = 3.9`. |
| D | False | A positive successor max does **not** force an increase — the **complete** target (−0.5) is below the old estimate (5), so the update **decreases** it. |
| E | False | With bootstrapping and α < 1, neither the reward nor the full target automatically becomes the new Q-value; the estimate moves only part-way. |

**Reference:** Sutton & Barto, 2nd ed., §6.5 (Q-learning target and TD error) and §6.1 (sign/direction of the update); Watkins & Dayan (1992); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G2Q3] Resampling the same (s,a) — model-free TD vs. a stored first sample
**Scenario:** On two visits to the same (s,a) a trading agent sees different rewards and next states. An analyst claims the first observed transition should **permanently** fix the Q-value because it is an actual sample, while later estimates are "only predictions."
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: every observed transition supplies reward + successor info and can serve as a **sample target** for updating that Q-value. |
| B | False (accurate) | Correct: one **stochastic** realization need not equal the **expected** return the Q-value estimates — a single sample can differ from the expectation. |
| C | False (accurate) | Correct: repeated updates integrate multiple stochastic outcomes, moving the estimate toward the experience-weighted expected value. |
| D | True (incorrect) | Wrong: Q-learning is **model-free** — it updates directly from sampled experience and does **not** require the full transition-probability table before learning. |
| E | True (incorrect) | Wrong: continued visitation and updating are **central** to refining the estimate — later visits must not be ignored. |

**Reference:** Sutton & Barto, 2nd ed., §6.5 (Q-learning as model-free TD control) and §6.1–§6.2 (sampled targets, bootstrapping toward expectations); Watkins & Dayan (1992, convergence under repeated sampling); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G3Q1] Step size — two learners, same target
**Scenario:** Two learners receive the same transition target of 10 from a current Q = 2. Learner H uses α = 0.8; Learner L uses α = 0.1.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | `2 + 0.8 × (10 − 2) = 2 + 6.4 = 8.4`. |
| B | True | `2 + 0.1 × (10 − 2) = 2 + 0.8 = 2.8`. |
| C | True | A larger α moves a greater fraction toward the new target, so H weights this sample more than L does. |
| D | False | A lower α does **not** guarantee a better final policy — performance also depends on sampling, nonstationarity, and the step-size schedule. |
| E | False | Full replacement of the old estimate occurs only at **α = 1**, not at 0.8 or 0.1. |

**Reference:** Sutton & Barto, 2nd ed., §6.5 (step size in the Q-learning update) and §2.4–§2.6 (α as fraction toward target; constant vs. decaying step sizes); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G3Q2] Constant large α on noisy stationary rewards
**Scenario:** A stationary simulator gives noisy rewards. A Q-learner keeps a **constant** α = 0.9 over a very long run; estimates keep swinging after unusually good/bad samples.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a high constant α makes each recent sample strongly influential — each update moves 90% of the way to its target. |
| B | False (accurate) | Correct: with α large, noisy targets produce persistent variability — estimates cannot settle tightly. |
| C | False (accurate) | Correct: **reducing α over time** supports greater stability in a stationary setting (smaller later steps dampen individual noisy observations). |
| D | True (incorrect) | Wrong: constant-step updates are **recency-weighted** (exponential), weighting recent experience more heavily — they do **not** average all history with equal weight. |
| E | True (incorrect) | Wrong: estimate movement can come purely from **noisy revisits**; it is not proof the agent is discovering new states. |

**Reference:** Sutton & Barto, 2nd ed., §2.5 (constant-α as recency-weighted average), §2.7 (Robbins–Monro step-size conditions `Σα=∞, Σα²<∞` for stationary convergence), §6.5 (Q-learning); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G3Q3] Regime change — α = 0 vs. small positive α
**Scenario:** After training, a regime change makes a once-profitable action costly. One deployed learner keeps updating with α = 0; another uses a small positive constant α.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: multiplying the TD error by **α = 0** yields no change, so the affected Q-value stays fixed under new transitions. |
| B | False (accurate) | Correct: a **positive** α lets new targets influence the stored estimate, enabling adaptation to the new experience. |
| C | False (accurate) | Correct: a smaller positive α changes the estimate by a smaller fraction per comparable update, so it adapts more gradually than a larger α. |
| D | True (incorrect) | Wrong: α = 0 **freezes** the old estimate — it does **not** erase or immediately forget prior experience. |
| E | True (incorrect) | Wrong: in a **nonstationary** environment the target values keep changing, so convergence to one permanent Q-set is **not** guaranteed regardless of α design. |

**Reference:** Sutton & Barto, 2nd ed., §2.5 (constant α for tracking nonstationary problems), §6.5 (Q-learning update); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G4Q1] Discount factor — immediate vs. delayed reward in a two-step task
**Scenario:** Terminal two-step task. Action A gives reward 4 immediately then ends. Action B gives 0 now, then 10 one step later. Values are learned correctly; ignore exploration.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | With γ = 0.9 the delayed reward contributes `0.9 × 10 = 9`, which exceeds A's 4, so B is preferred. |
| B | True | With γ = 0.2 the delayed reward contributes `0.2 × 10 = 2 < 4`, so A is preferred. |
| C | True | A larger γ reduces the penalty applied to the delayed payoff, raising B's relative influence. |
| D | False | The discount factor does **not** scale Action A's **immediate** reward — in the one-step Q-learning target the current reward is undiscounted (γ multiplies the successor value only). |
| E | False | Episodes terminating does **not** equalize the actions — differently timed and sized returns remain unequal. |

**Reference:** Sutton & Barto, 2nd ed., §3.3–§3.4 (return, discounting) and §6.5 (γ in the Q-learning target); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G4Q2] Lowering γ — near rebate vs. later loss
**Scenario:** A trading agent earns a small rebate now by entering a position that may create a larger loss several steps later. A developer changes γ from 0.95 to 0.05, leaving state, reward function, and data unchanged.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Lower γ multiplies successor values by a much smaller factor, so distant estimated consequences contribute less to current updates. |
| B | True | Short-sighted valuation can emphasize the near rebate over the distant cost, making the immediate reward more attractive. |
| C | True | The learned policy can change because γ changes the objective's **time preference** — even with the reward function unchanged. |
| D | False | Lower γ gives future rewards **less**, not more, numerical weight. |
| E | False | γ does **not** govern exploration — that is controlled separately (e.g., ε / random-action rate). |

**Reference:** Sutton & Barto, 2nd ed., §3.3–§3.4 (discounting and time preference), §6.5 (Q-learning target), §2.x (ε-greedy exploration as a separate mechanism); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G4Q3] γ = 0 vs. γ = 1 on a nonterminal transition
**Scenario:** A learner updates from a nonterminal transition with reward 6 and max successor Q = 8; old Q = 3, α = 0.5. Compare γ = 0 with γ = 1.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: with γ = 0 the future estimate contributes zero, so `target = 6`. |
| B | False (accurate) | Correct: with γ = 1 the undiscounted `target = 6 + 8 = 14`. |
| C | False (accurate) | Correct: the updates are `3 + 0.5(6−3) = 4.5` and `3 + 0.5(14−3) = 8.5`, so γ = 1 yields the larger new Q-value here. |
| D | True (incorrect) | Wrong: with γ = 0, α still governs movement from the old estimate (3) toward the target (6) — the step size continues to matter. |
| E | True (incorrect) | Wrong: γ = 1 does **not** always diverge — a **finite episodic** task can use γ = 1 without inevitable divergence. |

**Reference:** Sutton & Barto, 2nd ed., §3.3–§3.4 (undiscounted episodic return, γ = 1 for finite episodes), §6.5 (Q-learning target and step size); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G5Q1] Max over successors — greedy target vs. exploratory next action
**Scenario:** After an action the learner reaches State s' with Q-values [−1, 2, 5]; observed reward 1, γ = 0.8. During exploration the action **actually selected next** is the one valued at −1.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: standard Q-learning bootstraps from `max_a' Q(s',a')`, i.e., it uses **5** as the successor estimate. |
| B | False (accurate) | Correct: `target = 1 + 0.8 × 5 = 5`. |
| C | False (accurate) | Correct: using the **max** makes the target greedy w.r.t. successor estimates even though behavior chose another action — this is the off-policy separation. |
| D | True (incorrect) | Wrong: using the value of the next **behavior** action (−1) would be **on-policy (SARSA-style)** reasoning, not the standard Q-learning target. |
| E | True (incorrect) | Wrong: the max is taken over **current estimates**, which can be inaccurate — it does not prove the action valued at 5 is truly optimal. |

**Reference:** Sutton & Barto, 2nd ed., §6.5 (Q-learning `max` target — off-policy) vs. §6.4 (SARSA — on-policy); Watkins & Dayan (1992); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G5Q2] Maximization bias — inflated successor estimates
**Scenario:** Early in training, random estimation error makes a poorly sampled successor action look much better than its true value; the `max` operation repeatedly selects that inflated entry when predecessors are updated.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Bootstrapping can **propagate the inflated successor estimate backward** into predecessor Q-values (their targets incorporate the selected successor value). |
| B | True | Taking the **max over noisy estimates** preferentially selects positive errors, contributing to **overestimation bias**. |
| C | True | Additional representative experience can **correct** the inflated value and the later targets that rely on it. |
| D | False | The `max` **selects one** estimate; it does **not** average all successor actions, so it cannot automatically cancel estimation noise. |
| E | False | Overestimation arises precisely when **some** estimates are spuriously **high** — not only when every estimate is below its true value. |

**Reference:** Sutton & Barto, 2nd ed., §6.7 (maximization bias and Double Q-learning), §6.5 (the max target); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G5Q3] Terminal transition — zero continuation value
**Scenario:** A robot enters a terminal goal state with reward 20; the terminal state's future value is 0. Just before the transition Q(s,a) = 8, with α = 0.25 and γ = 0.9.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | With zero continuation value, `target = r + γ·0 = 20` — the terminal reward itself. |
| B | True | A terminal state has no future action return, so no successor action value is added. |
| C | True | `Q ← 8 + 0.25 × (20 − 8) = 8 + 3 = 11` — one quarter of the 12-point TD error. |
| D | False | The reward is included **once** in the target; there is no basis for counting it twice (38 is wrong). |
| E | False | A reset starts a **new episode** and is not a continuation — the next episode's initial state does not feed this terminal transition's target. |

**Reference:** Sutton & Barto, 2nd ed., §3.4 (terminal states, zero continuation value), §6.5 (Q-learning target at termination); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G6Q1] ε-greedy behavior — exploration still trains the greedy target
**Scenario:** A Q-learner follows an ε-greedy behavior policy. In s' the greedy action has Q = 7 but exploration picks an action with Q = 1. A colleague says the transition is useless because the agent acted randomly.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The observed reward and next state still update the **preceding** (s,a) — exploratory experience remains usable for TD learning. |
| B | True | The Q-learning target uses the **successor maximum (7)**, not the value of the action taken next. |
| C | True | The behavior policy can differ from the greedy target policy — the defining off-policy intuition. |
| D | False | Off-policy learning does **not** require the behavior to always act greedily — it may explore while the target stays greedy. |
| E | False | An exploratory action does **not** block updates — such transitions are an important source of state-action coverage. |

**Reference:** Sutton & Barto, 2nd ed., §6.5 (Q-learning as off-policy; ε-greedy behavior with a greedy target), §5.4–§5.6 (off-policy behavior vs. target policies); Watkins & Dayan (1992); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G6Q2] Q-learning vs. SARSA target — same transition, different rule
**Scenario:** Two agents observe the same transition into a next state with Q(left) = 4, Q(right) = 9; behavior next chooses `left`. Agent Q uses the successor **max**; Agent S uses the value of the **behavior** action chosen.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: Agent Q bootstraps from the max successor estimate, **9**. |
| B | False (accurate) | Correct: Agent S's on-policy-style rule evaluates the **next action actually selected** (`left` = 4). |
| C | False (accurate) | Correct: Agent Q's target favors the maximizing next action **independently of behavior** — it is greedy even though behavior chose `left`. |
| D | True (incorrect) | Wrong: different target rules can produce **different** updates from the same transition — the two targets need not be identical. |
| E | True (incorrect) | Wrong: using a value table does **not** make an agent on-policy — on/off-policy is set by the **target–behavior relationship**, not table use. |

**Reference:** Sutton & Barto, 2nd ed., §6.5 (Q-learning, off-policy max target) vs. §6.4 (SARSA, on-policy target); Watkins & Dayan (1992); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G6Q3] Random early actions — off-policy learning from exploration
**Scenario:** A trading learner deliberately takes random actions early, some producing losses. A manager concludes off-policy Q-learning cannot find an optimal greedy policy unless every training action comes from that greedy policy.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Exploratory losses are informative samples that can **lower** estimates for poor (s,a) pairs. |
| B | True | Visiting alternatives can reveal that an action initially believed inferior is actually valuable (correcting rankings). |
| C | True | Q-learning uses exploratory **behavior** to generate experience while updating toward a **greedy successor** target. |
| D | False | The experienced current action is updated as taken; the **successor target** is greedy — the random action is **not relabeled** as a greedy choice. |
| E | False | Off-policy learning does **not** remove the need for adequate **visitation** — rarely visited pairs can stay poorly estimated. |

**Reference:** Sutton & Barto, 2nd ed., §6.5 (off-policy Q-learning), §5.5–§5.6 (coverage/exploration requirements for off-policy methods); Watkins & Dayan (1992, visit-infinitely-often condition); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G7Q1] Initialization vs. learned evidence — an unvisited state
**Scenario:** A learner initializes every Q-value to zero and never visits State 12. At evaluation State 12 appears and the system picks the first action because the row is still tied at zero.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: with no update, State 12's row still reflects **initialization**, not learned evidence about that state. |
| B | True (incorrect) | Wrong: unchanged **zeros are not evidence** that every action truly has zero expected return. |
| C | False (accurate) | Correct: a deterministic first-index tie rule supplies a choice but **not** a learned preference — the row remains uninformative. |
| D | True (incorrect) | Wrong: **tabular** updates modify only the **experienced** (s,a) entry; visiting other states does **not** automatically update State 12's row. |
| E | False (accurate) | Correct: training **coverage** affects confidence in the extracted policy — poorly covered states yield arbitrary/unreliable choices. |

**Reference:** Sutton & Barto, 2nd ed., §6.5 (tabular Q-learning updates the visited entry), §5.5 (coverage/visitation and policy reliability); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G7Q2] Convergence intuition — visitation, decaying α, coverage
**Scenario:** In a finite stationary task, a Q-learner keeps visiting all relevant (s,a) pairs, uses an exploration schedule that doesn't cut coverage too early, and gradually reduces α. Its Q-values change less over time.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: repeated visitation supplies multiple samples so estimates can incorporate the range of outcomes. |
| B | False (accurate) | Correct: smaller later updates (decaying α) reduce sensitivity to individual noisy transitions. |
| C | False (accurate) | Correct: broad coverage supports stronger convergence claims than observing only a narrow path — alternatives need adequate experience to be compared. |
| D | True (incorrect) | Wrong: values changing less is **not** conclusive proof of global optimality — apparent stability can coexist with bias, poor representation, or thin coverage. |
| E | True (incorrect) | Wrong: a single pass per pair is **not** always sufficient — stochastic outcomes and bootstrapped dependencies generally require repeated updates. |

**Reference:** Sutton & Barto, 2nd ed., §6.5 (Q-learning convergence intuition), §2.7 (step-size conditions `Σα=∞, Σα²<∞`), §5.5 (coverage); Watkins & Dayan (1992, convergence proof: visit infinitely often + decaying α); Balch ML4T lectures (03-05/03-06).

### [ML2-D3G7Q3] Initialization bias — zero vs. optimistic, stopped early
**Scenario:** Two identical tabular learners differ only in initial values: Z sets all entries to 0, O sets all to 100. Both use greedy selection with deterministic tie-breaking and stop after a few episodes.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Early behavior can differ: as O's updated entries fall, **still-optimistic unvisited** entries stay attractive, encouraging O to try them. |
| B | True | With sufficient representative experience under suitable conditions, accumulated evidence can **overcome** starting values, so initialization need not determine eventual estimates. |
| C | False | Optimistic initialization does **not** guarantee every (s,a) is visited in every environment — reachability, dynamics, tie-breaking, and exploration can still prevent visits. |
| D | False | Equal initial entries with **deterministic** greedy tie-breaking can repeatedly pick the same action rather than exploring the ties — no guaranteed exploration. |
| E | False | Larger initial numbers (optimism) affect learning **dynamics** but do **not** guarantee a superior final greedy policy. |

**Reference:** Sutton & Barto, 2nd ed., §2.6 (optimistic initial values as exploration), §6.5 (tabular Q-learning), §5.5 (coverage/visitation); Balch ML4T lectures (03-05/03-06).

## References (domain-level)

1. **Sutton & Barto — *Reinforcement Learning: An Introduction*, 2nd ed.:** §6.5 (Q-learning — the off-policy TD control update `Q(s,a) ← Q(s,a) + α[r + γ·max_a' Q(s',a') − Q(s,a)]`, the greedy `max` target, convergence intuition); §6.1–§6.2 (TD prediction, bootstrapped sampled targets, TD error); §6.4 (SARSA — the on-policy contrast whose target uses the action actually taken); §6.7 (maximization/overestimation bias and Double Q-learning); §3.3–§3.4 (returns, discounting γ, episodic vs. continuing tasks, terminal states with zero continuation value, γ = 1 for finite episodes); §3.5 (action values vs. transition dynamics; policy vs. value); §2.4–§2.7 (step size α as fraction toward target, constant-α recency weighting, optimistic initial values, Robbins–Monro conditions `Σα=∞, Σα²<∞`); §5.4–§5.6 (off-policy behavior vs. target policies, coverage/visitation requirements).
2. **Watkins & Dayan (1992), "Q-learning," *Machine Learning* 8:279–292:** the original Q-learning algorithm and convergence proof (every state-action pair visited infinitely often + a suitably decaying learning rate ⇒ convergence to Q*).
3. **Balch — ML4T lectures (Georgia Tech):** reinforcement-learning problem framing (03-05) and the Q-Learning algorithm and trading application (03-06) — Q-table structure, the update rule, α and γ roles, off-policy exploration, and training-vs-deployment behavior.

_Source-symbol note: the slice renders some ligatures (e.g., "ﬁrst", "ﬁnite") and spacing artifacts such as `Q(s' ,·)` / `max Q(s' ,·)`; these are typographic, not semantic — the centered dot denotes "over all actions." No symbols were garbled in a way that affects any verdict, so none required a "(symbol unclear in source — verify)" flag._
