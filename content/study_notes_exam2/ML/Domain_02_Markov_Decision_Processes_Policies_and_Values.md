# ML Domain 2 — Markov Decision Processes, Policies & Values

## Domain cheat-sheet

- **The Markov property.** A state is **Markov** when it summarizes everything from the history that is relevant to predicting future transitions and rewards — i.e., the future is conditionally independent of the past *given the present state*: `P[S_{t+1}, R_{t+1} | S_t, A_t] = P[S_{t+1}, R_{t+1} | S_0,A_0,…,S_t,A_t]`. The test is **sufficiency**, not completeness: a Markov state need not record every past event, only a *sufficient summary* of the decision-relevant history.
  - **State aliasing (perceptual aliasing)** happens when two genuinely different underlying situations map to the *same* represented state. The learner then blends their outcomes and can estimate one averaged value where distinct situations actually require distinct actions. Omitting a variable that changes transitions, rewards, or available actions (package status, portfolio position, an unresolved earlier application) breaks the Markov property and causes aliasing.
  - **The fix is sufficiency, not raw history.** Adding the relevant *current* summary variable (carried position, package flag) can restore the Markov property; retaining the entire raw history is neither required nor sufficient on its own.
- **The MDP tuple `(S, A, P, R, γ)`.** States `S`, actions `A`, transition dynamics `P(s'|s,a)`, reward function `R(s,a)` (or `R(s,a,s')`), and discount factor `γ ∈ [0,1]`. Everything in this domain is defined relative to this tuple.
- **Transition dynamics `P(s'|s,a)`.** The current state **and action together** induce a *probability distribution* over next states.
  - **Deterministic** transition: one next state has probability 1 (dry floor → exactly one square).
  - **Stochastic** transition: the same `(s,a)` can lead to several next states, with probabilities that **sum to 1** (wet floor: 0.8 forward / 0.1 stay / 0.1 slide). A stochastic transition does **not** mean the action has no influence — different actions induce *different* distributions.
  - A single realized transition does **not** identify the underlying distribution, and does not prove deterministic causation. A deterministic *policy* removes randomness in action *selection*, not randomness in *environment* dynamics.
- **Reward, return, and the objective.** The **reward** `R_t` is the one-step scalar signal; the **return** `G_t` is the (optionally discounted) sum of current and future rewards: `G_t = R_{t+1} + γR_{t+2} + γ²R_{t+3} + …`. The agent optimizes the **return (expected cumulative reward)**, not the single largest or single immediate reward. A step with a poor immediate reward can still have high return; penalties (negative rewards) are legitimate. Reward is a **designed proxy** for the real objective and can be misspecified — missing cost/risk/turnover/drawdown terms let a policy earn a high *encoded* return while performing poorly on the intended measure, and convergence does not cure a wrong objective.
- **Discount factor `γ` and time preference.** `γ` weights future rewards: contribution of a reward `k` steps ahead is multiplied by `γ^k`. The **immediate** reward from the current decision is weighted 1 (undiscounted). Larger `γ` (→1) makes delayed rewards relatively **more** important; smaller `γ` discounts distant rewards more sharply (short-sighted). With `γ=1`, all rewards carry equal temporal weight. Discounting is **not** mathematically required for a *finite-horizon* return — a finite sum of finite rewards already converges; `γ<1` is a modeling choice, and changing `γ` can re-rank policies whose rewards are timed differently.
- **State-value function `Vπ(s)`.** Expected return **starting from `s` and following policy `π` thereafter**: `Vπ(s) = E_π[G_t | S_t = s]`. Key properties:
  - It is an **expectation over possible returns**, not the most likely outcome (State A: `0.8·10 + 0.2·(−10) = 6`, not 10).
  - It is **policy-dependent**: the same physical state can have different values under different policies — the state did not change, the planned future behavior did. Write it as `Vπ` to keep that explicit.
  - It concerns returns *beginning from* the state (future), not rewards already received (sunk).
- **Action-value function `Qπ(s,a)`.** Expected return from taking action `a` in `s`, **then** following `π`: `Qπ(s,a) = E_π[G_t | S_t=s, A_t=a]`. Q-values are expected returns, **not** probabilities (they need not sum to 1); a negative Q is a negative *expectation* and does not mean every realized outcome is negative. The **greedy** rule picks `argmax_a Q(s,a)`; the greedy action can change when estimates change even if the state is unchanged.
- **Bellman equations (the recursive link).**
  - **Bellman expectation:** `Vπ(s) = Σ_a π(a|s) Qπ(s,a)` and `Qπ(s,a) = R(s,a) + γ Σ_{s'} P(s'|s,a) Vπ(s')`. So state value is the **policy-weighted average of its action values** (`V = 0.75·8 + 0.25·0 = 6`), and an action value is **immediate reward + discounted expected successor value** (`−1 + 0.5·10 = 4`).
  - **Bellman optimality:** `V*(s) = max_a [ R(s,a) + γ Σ_{s'} P(s'|s,a) V*(s') ]`; the optimal greedy action maximizes immediate reward **plus** discounted successor value — it never ignores either term.
- **Policy improvement & iteration.** Switching one state to the higher-valued action (while holding other states fixed) is a **local policy-improvement** step; alternating evaluation and greedy improvement moves toward an optimal policy under appropriate assumptions. Improving one state does **not** guarantee global optimality, and improvement favors *higher* estimated value (it is distinct from exploration). Greediness with respect to **incomplete, biased, or uncovered** estimates does not prove optimality — Bellman optimality only holds when the reward/transition quantities fed into it are correct and coverage is adequate.

## Common traps

- **Inverted-polarity questions (9 of 21 here).** When the body says "mark each statement True when the stated claim is **incorrect** and False when it is correct," the Answer-Key verdict is flipped relative to the statement's truth: **True = the statement is wrong; False = the statement is accurate.** Read the polarity line *first*. Inverted here: **G1Q2, G2Q2, G3Q3, G4Q1, G4Q2, G5Q2, G5Q3, G6Q2, G7Q2.** The other 12 are Normal (True = accurate).
- **"Location/indicators alone are Markov."** False whenever an omitted carried-forward variable (package status, portfolio position, an unresolved prior application) changes future transitions, rewards, or available actions. The Markov test is *sufficiency for the future*, not "contains the most important variable."
- **"Repair a non-Markov state only by adding all raw history."** False — adding the relevant *current* summary variable can suffice; exhaustive history is not inherently required.
- **Stochastic ⇒ action has no influence / one sample reveals the distribution.** Both false. Different actions induce different next-state distributions; one realized transition neither proves deterministic causation nor identifies/invalidates a probability.
- **Deterministic policy ⇒ deterministic environment.** False — a deterministic policy removes randomness in *action selection*, not in environment dynamics.
- **Return = immediate reward / objective = biggest single reward.** False — return aggregates current **and** future rewards; the objective is cumulative, so a poor immediate reward can precede a high return.
- **Rewards must be positive.** False — penalties (negative rewards) are valid and common. And a high *encoded* return does not guarantee a good outcome under a different (intended) objective; reward is a proxy that can be misspecified, and convergence does not fix a wrong objective.
- **Discounting is required for finiteness / `γ<1` makes later rewards count more / `γ` discounts the immediate reward.** All false. A finite-horizon sum of finite rewards is already finite; `γ<1` *reduces* the weight on later rewards; the current reward is weighted 1.
- **State value = most-likely outcome / is policy-independent / depends on reward received before entering.** All false. `Vπ` is an *expectation over returns from the state onward*, it is *policy-conditioned*, and it ignores sunk rewards.
- **State value from Q: take the max.** Only for a greedy policy. For a stochastic policy, `V = Σ_a π(a|s)Q(s,a)` (policy-weighted average), e.g., `0.75·8 + 0.25·0 = 6`, not 8.
- **Q-values are probabilities / a negative Q means every trade loses.** Both false — Q-values are expected returns (need not sum to 1); a negative expectation can contain positive realized outcomes.
- **Bellman "compares only successor values."** False — it is `reward + γ·(expected successor value)`; dropping either the immediate reward or the discounted future term gives the wrong comparison.
- **Greedy on biased/incomplete estimates ⇒ optimal; improving one state ⇒ globally optimal.** Both false — unevaluated or mis-estimated actions can outperform; optimality claims require model validity, coverage, and accurate estimates.

## Questions

### [ML2-D2G1Q1] Robot navigation — omitted package status breaks Markov
**Scenario:** A robot-navigation team puts only the robot's current grid location in the state and omits whether it is carrying a package, even though movement depends on it. The lead claims the state is still Markov because location is the most important variable.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A Markov state must carry the information *sufficient* to predict relevant future transitions and rewards — "needed to predict relevant future outcomes" is the correct sufficiency criterion. |
| B | True | Omitting package status is exactly state aliasing: two materially different situations (carrying vs. not) collapse to the same displayed location-only state. |
| C | False | Containing location does **not** guarantee the Markov property — location alone can be insufficient when an omitted carried variable changes future dynamics. |
| D | True | Aliasing can prevent correct action selection, because the learner cannot distinguish situations that call for different actions. |
| E | True | Adding package status is a legitimate representation improvement — it supplies the omitted decision-relevant variable and reduces aliasing. |

**Reference:** Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed., §3.1 (the agent–environment interface and the Markov property / state as a sufficient statistic); Balch ML4T Q-Learning lectures (03-05).

### [ML2-D2G1Q2] Strategy learner — omitting portfolio position
**Scenario:** A strategy learner's state uses momentum and volatility indicators but omits the portfolio position; transaction costs depend on how far the target is from the position already held. The developer argues the market indicators alone are sufficient.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: with identical indicators but different holdings, buying from cash versus adding while long produces different trades and costs — holdings change the consequences. |
| B | False (accurate) | Correct: because costs depend on information absent from the state, the formulation violates the Markov assumption — the hidden holdings affect reward and the next portfolio condition. |
| C | True (incorrect) | Wrong: adding the relevant *current* position can suffice; retaining all raw price history is not inherently required to repair a non-Markov state. |
| D | False (accurate) | Correct: the Markov property is about whether the state is a *sufficient* summary for future dynamics and rewards, not whether it stores every historical observation. |
| E | True (incorrect) | Wrong: any omitted variable that changes relevant rewards or transitions can cause aliasing — portfolio-dependent costs included; aliasing is not limited to "physical" dynamics. |

**Reference:** Sutton & Barto, 2nd ed., §3.1 (Markov property as a sufficient statistic of history); Balch ML4T lectures on trading-as-an-RL-problem (03-05/06).

### [ML2-D2G1Q3] Credit-risk control — unresolved prior application
**Scenario:** A credit system approves/reviews/rejects applications. Its state has income and loan size but not whether an applicant has an unresolved earlier application that changes legal processing and the effect of the next action.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The same displayed state (income + loan size) can correspond to different underlying situations because the earlier-application condition is hidden. |
| B | True | With aliased situations sharing one representation, the learner can estimate a *blended* value even when different actions are appropriate in each. |
| C | False | Being "earlier in time" does not exempt information from the Markov requirement — past information must be represented when it still affects future transitions, rewards, or available actions. |
| D | True | Including the unresolved-application status is a current summary of decision-relevant history that improves how transitions and rewards are conditioned. |
| E | False | A Markov state need only retain a *sufficient summary* of relevant history, not an exhaustive record of every life event. |

**Reference:** Sutton & Barto, 2nd ed., §3.1 (Markov property; state as sufficient summary of history, not a full log); Balch ML4T lectures (03-05).

### [ML2-D2G2Q1] Order execution — stochastic fills from a state-action pair
**Scenario:** An execution agent chooses passive/midpoint/aggressive orders; from the same market state a passive order may be unfilled, partially fill, or fully fill, while an aggressive order fills more readily but with greater impact.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The transition dynamics map the current state **and** action to a distribution over next states — both jointly influence what can happen next. |
| B | True | Multiple possible fill outcomes from the same state-action pair are the definition of a stochastic transition. |
| C | False | A stochastic transition does **not** mean the agent has no influence — the action shifts outcome probabilities even without determining the result with certainty. |
| D | True | A probability distribution can represent the likelihoods of no fill, partial fill, and full fill. |
| E | False | Stochasticity does not force the realized next state to be independent of the order type — different order types induce different next-state distributions. |

**Reference:** Sutton & Barto, 2nd ed., §3.1 (dynamics `p(s',r|s,a)`; stochastic transitions); Balch ML4T lectures (03-05/06).

### [ML2-D2G2Q2] Delivery robot — deterministic dry vs. stochastic wet floor
**Scenario:** On dry flooring each command moves the robot exactly one square; on a wet section a forward command moves forward with prob 0.8, stays with 0.1, slides sideways with 0.1.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: dry-section movement is deterministic — each command has exactly one specified next state. |
| B | False (accurate) | Correct: wet-section movement is stochastic — one state-action pair samples from several possible next states. |
| C | False (accurate) | Correct: the wet-section outcome probabilities (0.8 + 0.1 + 0.1) should sum to one, accounting for all modeled outcomes. |
| D | True (incorrect) | Wrong: a deterministic policy removes randomness in *action selection*, not in *environment dynamics* — wet-floor transitions stay stochastic. |
| E | True (incorrect) | Wrong: one observed forward movement does not prove the forward probability is one — a single realization does not identify the underlying distribution. |

**Reference:** Sutton & Barto, 2nd ed., §3.1 (environment dynamics; deterministic vs. stochastic transitions) and §3.5 (policy randomness distinct from environment randomness); Balch ML4T lectures (03-05).

### [ML2-D2G2Q3] Volatility regime — distribution vs. single-trial guarantee
**Scenario:** After a "reduce exposure" action in a high-volatility state, estimates give 0.6 to staying high and 0.4 to switching to low. A manager says the action must *cause* the regime change whenever low volatility is observed next.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A low-volatility next state is an allowed outcome with probability 0.4, so observing it is consistent with the stated model. |
| B | False | A realized low-volatility outcome does not prove deterministic causation — the regime is modeled as stochastic, so one draw is just one sample. |
| C | False | One observation is insufficient to discard the estimated 0.6 — a single sample does not invalidate a transition distribution. |
| D | True | Transition probabilities describe relative likelihoods over *repeated* comparable transitions, not a guarantee for a single trial. |
| E | True | Different components of the next state can have different dynamics — a deterministically controlled exposure need not share the regime's randomness. |

**Reference:** Sutton & Barto, 2nd ed., §3.1 (transition probabilities as distributions over repeated transitions); Balch ML4T lectures (03-05/06).

### [ML2-D2G3Q1] Trading agent — immediate reward vs. multi-day return
**Scenario:** Daily net-change rewards are −2 (Mon), +1 (Tue), +5 (Wed). The team evaluates the three-day undiscounted return from Monday and asks whether Monday's reward alone measures the full result.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Monday's immediate reward is the one-step signal observed on Monday: −2. |
| B | True | With no discounting the three-day return is the sum: −2 + 1 + 5 = 4. |
| C | False | Return and immediate reward are **not** always identical in a multi-step task — the return aggregates a sequence while immediate reward is a single term. |
| D | True | A state or action can have a poor immediate reward yet lead to a favorable cumulative return — later rewards can outweigh an early loss. |
| E | False | The objective is cumulative net performance, not necessarily the single largest reward (Wednesday's +5). |

**Reference:** Sutton & Barto, 2nd ed., §3.3 (returns and episodes — return = cumulative reward); Balch ML4T lectures (03-05).

### [ML2-D2G3Q2] Warehouse agent — reward design shapes behavior
**Scenario:** A warehouse agent earns +20 per order, −1 per minute, −50 per collision, and rushes crowded aisles because the completion bonus dominates the expected penalty. An engineer argues the behavior cannot relate to reward design because reward is "only a reporting metric."
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The numerical reward operationalizes what the agent optimizes — it is the signal the learner evaluates behavior against, not a passive report. |
| B | True | Completing orders quickly can yield a high *encoded* return even when the behavior is undesirable to the engineers — the incentives favor risky speed. |
| C | False | Reward design and the real organizational objective are **not** guaranteed to align — a reward is a designed proxy that can be misspecified or incomplete. |
| D | True | Raising the collision penalty (or otherwise revising the reward) changes which behavior has the greatest expected return. |
| E | False | The collision penalty **is** a reward — negative rewards are valid and commonly represent costs or penalties. |

**Reference:** Sutton & Barto, 2nd ed., §3.2 (goals and rewards; the reward hypothesis; penalties as negative rewards; reward defines the objective); Balch ML4T lectures (03-05/06).

### [ML2-D2G3Q3] Portfolio policy — reward omits risk and cost terms
**Scenario:** A policy earns +1 when the market rises on a long day and 0 otherwise, with no penalty for losses, leverage, turnover, or drawdown. It takes extreme long positions, and the designer claims maximizing this reward equals maximizing risk-adjusted net return.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the reward omits losses, leverage, turnover, and drawdown — consequences present in the claimed investment objective but absent from the signal. |
| B | False (accurate) | Correct: a policy can achieve a high *encoded* return while performing poorly under a different (risk-adjusted) evaluation measure. |
| C | True (incorrect) | Wrong: the absence of negative rewards does not guarantee conservative behavior — removing penalties can *encourage* aggressive positioning. |
| D | False (accurate) | Correct: adding cost and risk-sensitive terms can better align the reward with the stated objective. |
| E | True (incorrect) | Wrong: convergence does not cure misspecification — the algorithm can converge to a stable optimum for the *wrong* objective. |

**Reference:** Sutton & Barto, 2nd ed., §3.2 (reward as a designed proxy for the objective; reward misspecification); Balch ML4T lectures (03-05/06).

### [ML2-D2G4Q1] Immediate vs. delayed reward under different discount factors
**Scenario:** Action X gives reward 6 now and nothing later; Action Y gives 0 now then 10 one step later. The team compares the two under different discount factors.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: with γ = 0.5 the one-step-delayed reward contributes 0.5 × 10 = 5, so Action Y's return is 5. |
| B | True (incorrect) | Wrong: at γ = 0.5, Action Y returns 5 while Action X returns 6, so Action X has the greater return — Y does not. |
| C | False (accurate) | Correct: with γ = 0.9 the delayed reward contributes 0.9 × 10 = 9. |
| D | False (accurate) | Correct: a larger discount factor reduces the penalty on future rewards, making delayed rewards relatively more important. |
| E | True (incorrect) | Wrong: the discount factor does not change Action X's immediate reward of 6 — the current reward in the return is undiscounted (weight 1). |

**Reference:** Sutton & Barto, 2nd ed., §3.3–§3.4 (returns and discounting; `G_t = R_{t+1} + γR_{t+2} + …`, immediate reward weighted 1); Balch ML4T lectures (03-05).

### [ML2-D2G4Q2] Low vs. high discount factor — time preference
**Scenario:** Agent L uses a low discount factor, Agent H one close to one. Changing positions has an immediate cost but may improve returns over several later periods.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: Agent L places less relative weight on distant rewards — repeated multiplication by a smaller factor shrinks distant contributions faster. |
| B | False (accurate) | Correct: Agent H, weighting later outcomes more, may accept an immediate cost for sufficiently valuable future rewards. |
| C | True (incorrect) | Wrong: a discount factor near one does not *guarantee* higher realized profits — performance also depends on estimates, data, dynamics, reward design, and policy quality. |
| D | False (accurate) | Correct: the appropriate discount factor depends on the task horizon and how future uncertainty/time preference should be represented. |
| E | True (incorrect) | Wrong: a low discount factor does not eliminate immediate rewards — the current reward ordinarily receives weight one; discounting grows for later rewards. |

**Reference:** Sutton & Barto, 2nd ed., §3.3–§3.4 (discounting, horizon, and time preference); Balch ML4T lectures (03-05).

### [ML2-D2G4Q3] Finite horizon — discounting is not required for finiteness
**Scenario:** A trading simulation always ends after five decisions. An analyst claims discounting is mathematically required to make the five-step return finite, and that γ = 1 makes the fifth reward more important than the first.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A five-step undiscounted return stays finite when the individual rewards are finite — a finite sum of finite terms converges without discounting. |
| B | True | With γ = 1, timing alone reduces no reward's contribution, so the stated rewards carry equal temporal weight. |
| C | False | A discount factor below one makes later rewards count **less**, not more, than earlier rewards. |
| D | False | Finite-horizon tasks need **not** use γ < 1 — undiscounted finite-horizon returns are valid when appropriate to the objective. |
| E | False | Changing the discount factor **can** change policy ranking — policies with differently timed rewards can swap rank as γ changes. |

**Reference:** Sutton & Barto, 2nd ed., §3.3–§3.4 (episodic/finite-horizon returns; discounting as a modeling choice, not a convergence requirement); Balch ML4T lectures (03-05).

### [ML2-D2G5Q1] State value as expected return over outcomes
**Scenario:** From State A a policy reaches a charger (return 10) with prob 0.8 or is stranded (return −10) with prob 0.2; from State B it always gets 5. The team uses expected undiscounted return as state value.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The expected return of State A is 0.8 × 10 + 0.2 × (−10) = 6. |
| B | True | A certain return of 5 has expected value 5, so V(B) = 5. |
| C | True | State A's value (6) exceeds State B's (5) even though one possible A outcome (−10) is worse than B — expected value accounts for both A outcomes. |
| D | False | Value is an **expectation** over possible returns, not merely the most likely outcome, so V(A) is 6, not 10. |
| E | False | State value is defined **relative to the policy** followed from the state (unless an optimal value is explicitly used) — it does not ignore that behavior. |

**Reference:** Sutton & Barto, 2nd ed., §3.5 (state-value function `Vπ(s) = E_π[G_t | S_t=s]` as an expectation under the policy); Balch ML4T lectures (03-05).

### [ML2-D2G5Q2] State value is policy-dependent
**Scenario:** Two managers evaluate the same market state: Policy P stays in cash, Policy Q goes long, assigning different expected returns. A reviewer claims a state can have only one value regardless of policy.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the value of a state can differ under Policy P and Policy Q — expected future return depends on what the agent will do from the state. |
| B | False (accurate) | Correct: a state-value function averages over the actions the policy selects and their subsequent outcomes. |
| C | True (incorrect) | Wrong: different state values do **not** imply the physical market state changed — the same state can have different values because the planned future behavior differs. |
| D | False (accurate) | Correct: writing the policy into the value notation (`Vπ`) clarifies which behavior is being evaluated and prevents treating policy values as interchangeable. |
| E | True (incorrect) | Wrong: state value concerns returns *beginning from* the state, not the reward received before entering it — sunk rewards do not determine it. |

**Reference:** Sutton & Barto, 2nd ed., §3.5 (policy-conditioned value functions; `Vπ` notation); Balch ML4T lectures (03-05).

### [ML2-D2G5Q3] State value vs. immediate reward on screen
**Scenario:** State C has immediate reward 0 then reliable rewards of 4 on each of the next three steps; State D has immediate reward 5 then nothing. A supervisor compares states only by the reward currently displayed.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: immediate reward alone can rank the states differently from their expected cumulative values — D looks better now, C offers a later stream. |
| B | False (accurate) | Correct: State C can be more valuable than D when future rewards are weighted sufficiently (with little/no discounting, 4+4+4 > 5). |
| C | True (incorrect) | Wrong: a state with zero immediate reward need not have zero value — future rewards can give it positive state value. |
| D | False (accurate) | Correct: state value summarizes expected return from the state, incorporating the relevant future reward sequence under the policy, not just the displayed reward. |
| E | True (incorrect) | Wrong: comparing state values does not require identical immediate rewards — expected return can compare states with any reward profiles. |

**Reference:** Sutton & Barto, 2nd ed., §3.5 (state value as expected return, not immediate reward); Balch ML4T lectures (03-05).

### [ML2-D2G6Q1] Action values and the greedy rule
**Scenario:** In a market state Q(s,long)=2.4, Q(s,cash)=1.1, Q(s,short)=−0.3, and deployment is greedy with respect to these estimates.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The greedy rule selects long because it has the largest estimated action value (2.4). |
| B | True | Q(s,long) is the expected return from choosing long in the state and then following the specified continuation behavior. |
| C | False | A negative Q for short does **not** mean every individual short trade loses — a negative *expectation* can still contain positive realized outcomes. |
| D | True | If the action-value estimates change, the greedy action can change without the represented state changing — greedy choice depends on the relative estimates. |
| E | False | Q-values are expected returns, **not** transition probabilities, so they need not sum to one. |

**Reference:** Sutton & Barto, 2nd ed., §3.5 (action-value function `Qπ(s,a)`) and §3.6 (greedy action selection w.r.t. value estimates); Balch ML4T Q-Learning lectures (03-05).

### [ML2-D2G6Q2] State value from a stochastic policy's action values
**Scenario:** At State s the policy picks Action A with prob 0.75 (Q=8) and Action B with prob 0.25 (Q=0). The team wants the corresponding state value.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: V(s) = 0.75 × 8 + 0.25 × 0 = 6 under this policy. |
| B | False (accurate) | Correct: the calculation weights each action value by the policy's probability of selecting that action (the Bellman expectation `V = Σ_a π(a|s)Q(s,a)`). |
| C | True (incorrect) | Wrong: V need not equal 8 — using the maximum describes a *greedy* choice, not the stated stochastic policy's value. |
| D | False (accurate) | Correct: if the policy always chose A (with the same Q-values), all probability lands on 8, so V(s) would become 8. |
| E | True (incorrect) | Wrong: stochastic action selection does not force the actions' expected returns to zero — the Q-values are unchanged by the selection probabilities. |

**Reference:** Sutton & Barto, 2nd ed., §3.5 (Bellman expectation linking `Vπ` and `Qπ`: `Vπ(s)=Σ_a π(a|s)Qπ(s,a)`); Balch ML4T lectures (03-05).

### [ML2-D2G6Q3] One-step action value = reward + discounted successor value
**Scenario:** From one state, "Wait" gives reward −1 then a successor worth 10; "Dispatch" gives reward 3 then a successor worth 4. γ = 0.5, and the successor values suit the continuation policy.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The one-step action value for Wait is −1 + 0.5 × 10 = 4 (immediate reward plus discounted successor value). |
| B | True | The same decomposition gives Dispatch 3 + 0.5 × 4 = 3 + 2 = 5. |
| C | True | Dispatch's 5 exceeds Wait's 4 under the supplied model and discount factor, so Dispatch has the greater action value. |
| D | False | Wait is **not** automatically preferred for having the greater successor value — the immediate reward and discounting must also enter the comparison. |
| E | False | Comparing actions does not ignore immediate reward — action value combines immediate and discounted future consequences. |

**Reference:** Sutton & Barto, 2nd ed., §3.5 (Bellman expectation for `Qπ`: `Qπ(s,a)=R + γ Σ_{s'} p(s'|s,a)Vπ(s')`); Balch ML4T lectures (03-05/06).

### [ML2-D2G7Q1] Bellman one-step comparison — Safe vs. Risky
**Scenario:** From State s, Safe gives reward 2 and deterministically reaches a state with optimal value 5; Risky gives reward 0 and reaches a state worth 10 (prob 0.5) or −2 (prob 0.5). γ = 0.9.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The Bellman one-step value for Safe is 2 + 0.9 × 5 = 6.5 (immediate reward plus discounted successor value). |
| B | True | Risky's expected successor value is 0.5 × 10 + 0.5 × (−2) = 4. |
| C | True | Risky's one-step value is 0 + 0.9 × 4 = 3.6. |
| D | False | The optimal greedy choice is **Safe**, not Risky — Safe's 6.5 exceeds Risky's 3.6. |
| E | False | Bellman reasoning does **not** exclude the immediate reward — the recursive decomposition is current reward plus discounted future value. |

**Reference:** Sutton & Barto, 2nd ed., §3.6 (Bellman optimality equation; `V*(s)=max_a[R + γ Σ p(s'|s,a)V*(s')]`); Balch ML4T lectures (03-05/06).

### [ML2-D2G7Q2] Local policy improvement from action values
**Scenario:** A policy currently chooses cash (Q=1.2) in a state; updated estimates give long=2.0 and short=0.4 there. The analyst considers switching that state to long while leaving other states unchanged.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: switching to long is a local policy-improvement step — long has greater estimated return than the currently chosen action. |
| B | False (accurate) | Correct: the change compares action values *within the same state*, holding the state fixed and considering alternative actions. |
| C | True (incorrect) | Wrong: policy improvement favors *higher*-valued actions, not the lowest-valued action — exploration and greedy improvement are distinct concepts. |
| D | False (accurate) | Correct: repeated evaluation plus greedy improvement can move a policy toward optimality under appropriate estimates — the intuition behind policy iteration. |
| E | True (incorrect) | Wrong: improving one state does not guarantee global optimality — other states may still use inferior actions, and values may need re-evaluation after the change. |

**Reference:** Sutton & Barto, 2nd ed., §4.2 (policy improvement theorem) and §4.3 (policy iteration — alternating evaluation and greedy improvement); Balch ML4T lectures (03-05/06).

### [ML2-D2G7Q3] Greedy on biased/incomplete estimates ≠ optimal
**Scenario:** A manager finds a policy chooses the highest estimated Q-value in every observed state and declares it globally optimal — even though some state-action pairs were never evaluated and the transition estimates are known to be biased.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Greediness with respect to incomplete or biased estimates does not by itself prove optimality — a policy can be greedy on inaccurate values and still be suboptimal. |
| B | True | Missing state-action estimates can conceal actions with greater true expected return. |
| C | False | A policy is **not** optimal merely because it is deterministic — determinism describes action *selection*, not the quality of the selected actions. |
| D | False | Bellman optimality is **not** satisfied regardless of input correctness — incorrect transition/reward quantities produce estimates that do not represent the true environment's optimal values. |
| E | False | Demonstrating optimality **does** require assumptions about the model, coverage, and accuracy of the value estimates. |

**Reference:** Sutton & Barto, 2nd ed., §3.6–§3.7 (Bellman optimality equations and the role of accurate models/coverage; optimality and approximation); Balch ML4T lectures (03-05/06).

## References (domain-level)

1. **Sutton & Barto — *Reinforcement Learning: An Introduction*, 2nd ed. (ch.3 "Finite Markov Decision Processes"):** §3.1 (agent–environment interface, dynamics `p(s',r|s,a)`, and the Markov property — the state as a sufficient statistic of history); §3.2 (goals and rewards, the reward hypothesis, negative rewards/penalties, reward as a designed proxy that defines the objective); §3.3 (returns and episodes — return = cumulative reward); §3.4 (unified notation and discounting; the role of `γ` and finite-horizon returns); §3.5 (policies and value functions — `Vπ`, `Qπ`, policy-conditioned expectations, and the Bellman expectation equations linking them); §3.6 (optimal value functions and the Bellman optimality equation); §3.7 (optimality and approximation — dependence on accurate models and coverage).
2. **Sutton & Barto, 2nd ed. (ch.4 "Dynamic Programming"):** §4.2 (policy improvement theorem) and §4.3 (policy iteration — the evaluation/greedy-improvement loop underlying G7Q2's local-improvement reasoning).
3. **Balch — ML4T lectures (Georgia Tech):** RL/Q-Learning problem-framing and MDP lectures (03-05), the trading-as-RL formulation and value/action-value estimation (03-06), used for the trading-contextualized scenarios (state representation, transitions, rewards, discounting, state/action values, Bellman reasoning).
