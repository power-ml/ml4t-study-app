# ML Domain 1 — Reinforcement Learning Problem Framing

## Domain cheat-sheet

- **The five RL primitives (agent / environment / state / action / reward).** Fix the *boundary* before anything else:
  - **Agent** = the decision-maker/controller that *selects actions*. It is defined by what it controls, not by who designed it or how it was built. A hand-written rule, a programmed controller, or a learned Q-table can all be the agent; the human who specified the objective is **not** the agent.
  - **Environment** = everything the agent interacts with but does not directly choose. The boundary is drawn at the **limit of the agent's absolute control**, not at a physical surface. In trading, portfolio accounting, cost models, and market mechanics are typically *inside the environment* even though they live on the same computer as the agent.
  - **State** = the information available at decision time that is used to choose an action. It can combine external observations (indicators, obstacles, order book) with agent-specific internals (current holdings, battery, remaining inventory/time). Observed conditions the agent *reacts to* are **state**, not actions.
  - **Action** = a choice the agent can make at a decision point (target position, order size, move/wait/recharge, quote). It is *controllable*; outcomes that merely *follow* a decision (realized P&L, next-day return) are **not** actions.
  - **Reward** = a scalar feedback signal defining *what* to achieve (not *how*). Rewards may be **positive or negative** (penalties are rewards too). The **reward defines the objective the agent optimizes**, so changing the reward changes the learned policy. (Sutton & Barto "reward hypothesis": goals can be expressed as maximization of expected cumulative reward.)
- **Sequential decision-making.** RL optimizes **cumulative** (long-run) reward, not each step in isolation. An action's value depends on the *state it leads to* and the options it leaves open later. A sequence of locally optimal (greedy one-step) choices need **not** maximize cumulative return — early actions constrain later feasibility (transaction costs that depend on current holdings, battery that caps future routes, inventory that becomes risky). "Same observation ⇒ same best action" is false whenever a carried-forward internal state (inventory, position) changes downstream consequences.
- **Episodes vs. continuing tasks.** An **episode** is a bounded interaction ending in a *terminal* state (goal reached, collision, liquidation, or a truncation such as a step cap), after which the environment resets to a (possibly independent) start. "Terminal" means *end of this episode*, not end of all training. A **continuing** task runs indefinitely with no natural terminal success state (e.g., always-on market making). Episode/reset boundaries are a **modeling choice**: a calendar or reporting boundary does not by itself make a task episodic, and forced liquidation/truncation changes the formulated problem (terminal costs, next start state, which delayed consequences the learner experiences).
- **Policies & action selection.** A **policy (π)** maps states → actions (deterministic) or states → probability distributions over actions (stochastic). The policy is distinct from the **value estimates** (Q-table/value function): values *evaluate* actions; the policy is the *rule* converting those evaluations into choices. Consequences:
  - A **greedy** policy picks the max-value action — but with random tie-breaking it is still stochastic when values tie.
  - A **stochastic** policy can place nonzero probability on lower-valued actions (e.g., ε-greedy exploration); it is a deliberate distribution, not just tie-breaking.
  - You can **change the selection rule without retraining the values** (e.g., switch exploratory→greedy for deployment). Two deployments can share identical learned values yet behave differently.
  - **Policy randomness ≠ environment randomness** — a policy can be stochastic in a deterministic environment, and removing exploration does not make external outcomes deterministic.
- **Delayed reward & credit assignment.** RL's defining difficulty: a reward realized late (implementation shortfall at order completion, +100 only at delivery, a tail loss weeks later) must be **attributed back** to the earlier actions that produced it. Temporal proximity ≠ causal responsibility — crediting only the *last* action is wrong; early actions shape remaining inventory, average price, exposure, and reachable states. **Sparse** reward (long runs of zeros, one terminal payoff) is hard precisely because informative, differentiating feedback is rare — frequent zeros do **not** make it "dense." **Reward shaping** (intermediate rewards for genuine progress) can help, but a poorly designed proxy invites shortcuts/reward hacking and can change the behavior being optimized.
- **When RL fits vs. supervised learning.**
  - **Supervised** learning maps inputs → *known labels/targets* from a fixed labeled dataset; it needs no agent, actions, rewards, or environment interaction. Relabeling targets "buy"/"sell" does **not** make it RL — RL requires reward-bearing *interaction or transition experience*.
  - **RL** fits genuine **sequential control** problems where current actions change future states and cumulative cost/benefit, and feedback is a reward rather than a per-example label. A highly accurate predictor is **not** guaranteed to yield the best cumulative-net-reward policy (accuracy can be misaligned with costs, sizing, risk, turnover).
  - **Hybrid** is common and legitimate: a supervised forecast (volatility, obstacle recognition) can be a **state feature / perception module** feeding an RL control policy. Logs of actions+transitions+outcomes *can* support policy learning; labeled images support supervised perception.
  - **Appropriateness ≠ feasibility.** Even when a problem is correctly sequential, **exploration cost, safety, data, validation, and governance** still matter. Prefer simulators, historical transition data, or constrained/offline exploration over unrestricted online learning on a production system.

## Common traps

- **Inverted-polarity questions (9 of 21 here).** When the body says "mark each statement True when the stated claim is **incorrect** and False when it is correct," the Answer Key verdict is flipped relative to the statement's truth: **True = the statement is wrong; False = the statement is accurate.** Read the polarity line *first*. Inverted here: **G1Q1, G1Q2, G2Q1, G3Q2, G4Q1, G5Q3, G6Q1, G6Q2, G7Q2.** The remaining 12 are Normal (True = accurate).
- **Agent-boundary confusion.** "Only the external market is the environment; portfolio accounting must be in the agent" and "the human who defined the objective must be the agent" are both wrong. The agent is the *action-selector*; everything it does not directly control (including on-box accounting/cost models) is environment.
- **Action vs. outcome vs. state.** Realized P&L / next-day return (an *outcome*) is not an action. Observed obstacles, indicators, battery, inventory (conditions) are *state*, not actions. The *controllable choice* (target position, order size, move/recharge, quote) is the action.
- **Greedy-one-step = optimal.** False in sequential settings — "best next-step gross return/distance/fill" need not maximize cumulative net reward; costs and future feasibility depend on carried-forward state.
- **"Same market observation ⇒ same optimal action."** False whenever current inventory/holdings change downstream risk and cost.
- **Reward sign.** Penalties (collisions, costs) *are* part of the reward signal — rewards can be negative.
- **Changing the reward is harmless / terminology doesn't matter.** False — the reward *defines* the objective, so which quantity is the reward changes the learned policy.
- **Convenient boundary ⇒ episodic.** A daily/calendar reporting boundary does not create a natural terminal state; markets continue. Forced liquidation/truncation is a modeling choice that *does* change the task.
- **"Terminal = end of training."** No — terminal = end of the *current episode*; a new one can start immediately.
- **Last-action credit / "later loss can't relate to earlier trades."** Both wrong — credit assignment must spread responsibility across the sequence that built the exposure; delayed losses trace to earlier positioning.
- **Sparse ≠ dense.** Many zeros do not make feedback dense; dense means frequent *informative* reward.
- **Reward shaping is a free lunch.** Rewarding every movement/day can induce wandering or hide accumulated risk — proxies can be gamed.
- **Relabeling ⇒ RL / "classifier must interact to learn."** Renaming labels "buy/sell" does not create RL; supervised training can use a fixed dataset with no environment interaction.
- **Accuracy ⇒ best policy.** A more accurate forecaster is not guaranteed to produce the highest cumulative-net-reward policy.
- **Policy = Q-table.** The value estimates are not the policy; the selection *rule* is. Switching stochastic→greedy need not retrain stored values.
- **"A policy must be learned."** A fixed/programmed state→action rule is still a policy; learned policies are not automatically better than fixed rules.
- **Sequential ⇒ RL mandatory / RL ⇒ ignore cost.** Temporal ordering alone (e.g., forecasting volatility) does not require RL; and identifying a problem as sequential does not waive exploration-cost, safety, and governance constraints.

## Questions

### [ML2-D1G1Q1] Trading desk — mapping agent/environment/state/action/reward
**Scenario:** A trading desk builds an RL system choosing short/cash/long daily, wants rewards to reflect net performance (incl. commissions and market impact), and asks how each part maps to the RL framework.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The position-selecting algorithm *is* the agent — the agent is the decision-maker that emits actions. The claim is correct, so the inverted verdict is False. |
| B | True (incorrect) | Wrong: the environment can include portfolio accounting that applies costs and converts trades/market moves into outcomes. The agent–environment boundary is the limit of the agent's control, not "external market only." |
| C | True (incorrect) | Wrong: next-day realized net change is an *outcome* that may feed the reward; the chosen target position is the action. Something occurring after the decision is not thereby an action. |
| D | False (accurate) | Correct: a state can combine market observations with agent-specific holdings — both are legitimate state components used at decision time. |
| E | False (accurate) | Correct: a reward on net portfolio change encodes the desk's true objective (including costs) more directly than a reward based only on the sign of tomorrow's market return. |

**Reference:** Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed., §3.1 (agent–environment interface and boundary) and §3.2 (goals and rewards / reward hypothesis); Balch ML4T "Q-Learning" problem-framing lectures (03-05).

### [ML2-D1G1Q2] Warehouse robot — state vs. action vs. reward
**Scenario:** A warehouse delivery robot has state = location, battery, package status, nearby obstacles; actions = move/wait/recharge; objective penalizes collisions and late deliveries. Verify the mapping.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: battery level is a candidate *state* variable describing decision context, not an action. |
| B | False (accurate) | Correct: "recharge" is an action when it is a choice available to the agent at an eligible station. |
| C | False (accurate) | Correct: a collision penalty is part of the reward signal — rewards may be negative, and penalties communicate undesirable outcomes. |
| D | True (incorrect) | Wrong: the agent is the robot's decision-making controller, not the human lead who merely defined the objective. |
| E | True (incorrect) | Wrong: obstacle locations are *observed conditions* that enter the state; the robot's chosen response is the action. Reacting to something does not reclassify it as an action. |

**Reference:** Sutton & Barto, 2nd ed., §3.1 (states, actions, agent definition) and §3.2 (rewards, including negative rewards/penalties); Balch ML4T RL-framing lectures (03-05).

### [ML2-D1G1Q3] Order execution — reward/state/action terminology matters
**Scenario:** An execution agent splits a parent order over 10 minutes. A manager calls the bid-ask spread "the reward," shares-sent-now "the state," and says terminology is cosmetic. Evaluate.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | The spread is an observed market *condition*, not the natural reward; execution outcomes such as implementation shortfall are more appropriate reward components. |
| B | True | Order size submitted now is a controllable decision — a valid action in the execution problem. |
| C | True | A negative implementation shortfall (or equivalent execution-quality measure) aligns learning with the desk's objective, so it can contribute to reward. |
| D | False | Changing which quantity is the reward *does* change the learned policy — the reward defines what behavior is encouraged. Terminology is not cosmetic. |
| E | True | Remaining shares and remaining time constrain which later actions are feasible/desirable (deadline pressure), so they are useful state variables. |

**Reference:** Sutton & Barto, 2nd ed., §3.1–§3.2 (state vs. reward, reward defines the objective); Balch ML4T lectures on trading-as-an-RL-problem (03-05/06).

### [ML2-D1G2Q1] Daily position — one-step greedy vs. sequential control
**Scenario:** A PM proposes choosing each day the action with the highest predicted next-day gross return, independently, with transaction costs charged on position changes. Verify the framing.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: today's position affects tomorrow's transaction cost because tomorrow's trade size depends on holdings already carried. |
| B | True (incorrect) | Wrong: maximizing one-step gross return need not maximize cumulative net return — a chain of locally attractive returns can incur excessive costs or land in poor later states. |
| C | True (incorrect) | Wrong: current position cannot be omitted — the cost of a target-position action depends on the position already held, not just market indicators. |
| D | False (accurate) | Correct: action order matters because the same action has different consequences depending on the preceding holdings. |
| E | False (accurate) | Correct: a sequential-control formulation evaluates longer-run effects that independent one-step choices overlook. |

**Reference:** Sutton & Barto, 2nd ed., ch.3 intro (sequential decision-making) and §3.3 (returns = cumulative reward); Balch ML4T lectures 03-05 (why trading is a sequential/Q-Learning problem).

### [ML2-D1G2Q2] Delivery drone — immediate progress vs. future feasibility
**Scenario:** A drone can take a short route risking too little battery to reach a charger, or a longer route preserving margin. Why consider anything beyond immediate distance reduction?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | An action that maximizes immediate progress can still lower the probability of mission completion by leaving an unsafe future battery state. |
| B | False | Battery consumption is not merely an immediate cost — the route changes remaining battery, hence the next state and the options available later. |
| C | False | Greatest next-step distance reduction is not necessarily the optimal sequential decision; optimality depends on cumulative consequences. |
| D | True | A long-term objective can favor the longer route when it improves expected mission completion (future feasibility outweighs small immediate progress). |
| E | True | Treating each movement as an independent prediction misses how earlier actions constrain later choices — the core of sequential dependence. |

**Reference:** Sutton & Barto, 2nd ed., §3.3–§3.4 (returns, discounting, long-run objective); ch.3 (how actions change future states). Balch ML4T lecture 03-05.

### [ML2-D1G2Q3] Market maker — spread capture vs. future inventory risk
**Scenario:** A market-making team repeatedly sets bid/ask quotes; aggressive quotes earn spread now but accumulate inventory that is costly during fast price moves. Evaluate the tension.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Executed quotes change inventory carried into later decisions as well as immediate revenue — quotes have downstream consequences. |
| B | False | Given the same market observation, the best quote is *not* inventory-independent: current inventory changes the risk and downstream consequences of additional fills. |
| C | False | Maximizing reward from the next fill alone does not guarantee acceptable end-of-day inventory risk — repeated attractive fills can build an undesirable position. |
| D | True | A sequential objective can trade current spread capture against future inventory-management costs, valuing actions by immediate *and* downstream effects. |
| E | False | Timing is not irrelevant even with a fixed number of updates — early actions shape the states and choices encountered later. |

**Reference:** Sutton & Barto, 2nd ed., ch.3 (sequential decisions; state carries forward), §3.3 (cumulative return); Balch ML4T lecture 03-05/06.

### [ML2-D1G3Q1] Decision tree vs. Q-Learner — labels vs. rewards
**Scenario:** One team fits a decision tree to predict next-day returns from labeled history; another uses Q-Learning over long/cash/short by cumulative reward. Are they solving the same kind of problem?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The decision tree is a supervised learner trained from labeled examples (each row paired with a known next-day return). |
| B | True | The Q-Learner estimates action values directly from reward-bearing state-action transitions, then selects the best action. |
| C | False | Q-Learning does *not* require a target label per state-action pair — it learns from rewards and transitions, not explicit labels. |
| D | True | Both can use the same market indicators as inputs even though the learning paradigms differ. |
| E | True | Comparing them is appropriate when the goal is to understand how policy learning differs from supervised prediction (a core Exam-2 distinction). |

**Reference:** Sutton & Barto, 2nd ed., ch.1 §1.1 (RL vs. supervised vs. unsupervised; learning from reward/interaction, not labeled examples); Balch ML4T Q-Learning lectures (03-05).

### [ML2-D1G3Q2] Relabeling classifier outputs is not an RL formulation
**Scenario:** A quant team has a direction classifier but the CIO wants position choices accounting for turnover and drawdown. An analyst claims renaming labels "buy"/"sell" turns the classifier into an RL agent.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: relabeling supervised targets as actions does not by itself create RL — RL requires reward-bearing interaction or transition experience, not action-like label names. |
| B | True (incorrect) | Wrong: a supervised classifier need *not* interact with an environment during training; it can learn from a fixed dataset of already-supplied labels. |
| C | False (accurate) | Correct: an RL reward can incorporate action- and holding-dependent consequences such as transaction costs. |
| D | True (incorrect) | Wrong: a highly accurate direction classifier is not guaranteed to produce the highest-cumulative-net-reward policy — accuracy can be misaligned with sizing, costs, and risk. |
| E | False (accurate) | Correct: a prediction model can serve as a feature/component within a broader sequential decision policy. |

**Reference:** Sutton & Barto, 2nd ed., ch.1 §1.1 (what distinguishes RL from supervised learning); §3.2 (reward captures action-dependent outcomes). Balch ML4T lectures 03-05.

### [ML2-D1G3Q3] Image classifier vs. RL navigation — complementary roles
**Scenario:** A robotics lab has labeled "obstacle"/"clear" images plus logs of actions, collisions, delivery times, and must decide among a classifier, an RL policy, or both, while real-world exploration is costly.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The labeled images define a supervised dataset for obstacle recognition. |
| B | False | Action/transition/outcome logs *can* support policy learning — reward-bearing experience is not limited to labeled images. |
| C | False | An obstacle classifier identifies conditions but does not by itself resolve the control tradeoffs (turn/stop/continue) in every situation. |
| D | True | RL can optimize the sequence of navigation choices while a supervised model supplies perception — complementary roles. |
| E | True | Costly interaction is a real practical consideration that may make unrestricted online RL exploration inappropriate (collisions/delays carry real cost). |

**Reference:** Sutton & Barto, 2nd ed., ch.1 §1.1 (RL vs. supervised) and ch.3 (control vs. perception); on exploration cost/safety see ch.1 and §3.1. Balch ML4T lectures 03-05/07.

### [ML2-D1G4Q1] Robot navigation — episodes and termination
**Scenario:** A navigation team ends each run when the robot reaches a destination, collides, or exceeds 500 steps, then resets to a new start. Verify the episodic framing.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: each run is an episode — the start and stopping rules define a bounded interaction. |
| B | False (accurate) | Correct: reaching a destination is a terminal event even if a new episode starts immediately; "terminal" means end of the current episode, not of all training. |
| C | True (incorrect) | Wrong: a 500-step cap *can* end an episode by truncation even without a natural terminal state (goal or collision). |
| D | True (incorrect) | Wrong: a reset need not depend on late actions of the prior episode — the next episode can be initialized independently per the team's procedure. |
| E | False (accurate) | Correct: whether a collision terminates an episode is part of the problem formulation — a design choice. |

**Reference:** Sutton & Barto, 2nd ed., §3.3–§3.4 (episodes, terminal states, episodic vs. continuing, truncation/time limits); Balch ML4T RL lectures (03-05).

### [ML2-D1G4Q2] Market making — continuing task vs. episodic boundaries
**Scenario:** A market-making system runs whenever the exchange is open. The trading lead calls each quote update an episode; research treats it as continuing with daily training/reporting boundaries.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A continuing task may operate indefinitely with no natural terminal success state. |
| B | False | Dividing data by day does not *prove* the task is episodic — a convenient reporting boundary is not a natural terminal state. |
| C | False | A single quote decision is not necessarily its own episode; an episode normally contains a sequence of related transitions. |
| D | True | Forcibly closing positions at day's end changes the formulated task — it alters terminal consequences and the next start condition. |
| E | False | Boundaries should be chosen *with* attention to whether state/holdings/consequences carry across them; ignoring that distorts learning. |

**Reference:** Sutton & Barto, 2nd ed., §3.3–§3.4 (continuing vs. episodic tasks; boundaries as modeling choices; discounting for continuing tasks). Balch ML4T lectures 03-05.

### [ML2-D1G4Q3] Annual vs. monthly resets — episode design affects learning
**Scenario:** A strategy learner trains one calendar year at a time, starting in cash and liquidating on the last day. Is a calendar year inherently an episode, and would monthly resets be equivalent?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Starting in cash and ending with liquidation creates an explicit episodic structure defined by the team's initialization/termination rules. |
| B | True | The calendar boundary is terminal only because of the modeling/training design — markets do not cease permanently. |
| C | False | Monthly resets are not guaranteed to produce the same incentives — they change horizon, available experience, and liquidation frequency. |
| D | False | More frequent forced liquidation exposes the learner to terminal trading costs *more* often, potentially increasing their influence — not making them less relevant. |
| E | True | Episode design affects which delayed consequences the learner experiences; consequences beyond a reset may be excluded or represented differently. |

**Reference:** Sutton & Barto, 2nd ed., §3.3–§3.4 (episode definition, horizon/return, effect of boundaries on experienced return). Balch ML4T lectures 03-05/06.

### [ML2-D1G5Q1] Execution shortfall — credit assignment across child orders
**Scenario:** An execution agent sends child orders over 30 minutes; implementation shortfall is computed only at parent completion. The manager wants to credit the entire result to the last child order.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Not only the last child order matters — the calculation time does not erase the effects of earlier prices, sizes, and timing. |
| B | True | Assigning all credit/blame to the most recent action can be misleading; temporal proximity is not exclusive causal responsibility. |
| C | True | The delay between actions and the final reward creates a credit-assignment challenge — the learner must connect a late outcome to the actions that produced it. |
| D | False | Earlier actions *do* keep influencing the final reward — they shape remaining inventory, average price, and later options. |
| E | True | Informative intermediate rewards can help, but poorly designed ones can change the behavior being optimized (reward-shaping risk). |

**Reference:** Sutton & Barto, 2nd ed., ch.1 (delayed reward as a defining RL feature) and ch.12 (eligibility traces / temporal credit assignment); Minsky's credit-assignment problem. Balch ML4T lectures 03-05/07.

### [ML2-D1G5Q2] Sparse terminal reward — delayed credit assignment
**Scenario:** A robot gets +100 only on completing a delivery and 0 at every prior step; most early runs fail, giving little information about which movements helped.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | This is a *sparse*, not dense, reward problem — frequent zeros are not dense feedback because the informative, differentiating reward occurs only rarely. |
| B | True | The successful terminal reward must propagate back to raise the estimated value of earlier actions that led to the goal. |
| C | False | Giving +1 for every movement is not a guaranteed fix — it can encourage wandering/longer routes and changes incentives. |
| D | True | Long delays make it harder to distinguish helpful early actions from irrelevant ones (many intervening steps separate decision and outcome). |
| E | True | Progress-based intermediate rewards can add feedback, but their design must be checked for unintended shortcuts (reward hacking). |

**Reference:** Sutton & Barto, 2nd ed., ch.1 (sparse/delayed reward) and §3.3 (return propagation); reward-shaping caveats (Ng, Harada & Russell, 1999, potential-based shaping). Balch ML4T lectures 03-05/07.

### [ML2-D1G5Q3] Tail-risk selling — delayed loss and credit assignment
**Scenario:** A strategy earns small daily premiums selling tail-risk protection but occasionally takes a large loss weeks later. The PM proposes judging each sell only by the day's premium.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: immediate premium can make the action look attractive before its delayed risk is realized — short-term reward conceals accumulated risk. |
| B | True (incorrect) | Wrong: a suitable long-horizon return should include *both* the premium and the delayed loss, not discard the premium. |
| C | False (accurate) | Correct: evaluating only same-day reward can systematically favor actions with harmful delayed consequences. |
| D | True (incorrect) | Wrong: the later large loss is not unrelated — earlier trades create or enlarge the exposure that generates it. |
| E | False (accurate) | Correct: credit assignment is exactly the problem of attributing the eventual outcome across the sequence of exposure-building decisions. |

**Reference:** Sutton & Barto, 2nd ed., ch.1 (delayed reward) and §3.3–§3.4 (return/discounting across a horizon); temporal credit assignment (ch.12). Balch ML4T lectures 03-05/07.

### [ML2-D1G6Q1] Q-table vs. policy; deterministic vs. stochastic selection
**Scenario:** A Q-Learner has estimated values for short/cash/long per state. The lead claims the policy *is* the Q-table and that two deployments with the same values must act identically.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a policy specifies how actions are selected in each state (a map from states to actions or action probabilities). |
| B | True (incorrect) | Wrong: picking the highest-valued action is not always deterministic — random tie-breaking makes selection stochastic when values are tied. |
| C | False (accurate) | Correct: a stochastic policy can assign nonzero probability to more than one action in a state (a distribution over actions). |
| D | True (incorrect) | Wrong: value estimates and the selection rule are *not* identical — values evaluate actions; the policy converts those evaluations into choices. |
| E | False (accurate) | Correct: two deployments can share learned values but use different selection policies (one greedy, one still exploring). |

**Reference:** Sutton & Barto, 2nd ed., §3.5 (policies and value functions; policy distinct from value function) and §2.x / ch.5 (ε-greedy, exploration). Balch ML4T Q-Learning lectures (03-05).

### [ML2-D1G6Q2] A fixed rule is a policy; learned is not necessarily better
**Scenario:** A risk committee compares a fixed "go to cash when volatility > threshold" rule with an RL-learned policy. The chair claims the fixed rule is not a policy because a human wrote it.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the fixed volatility rule *is* a policy — it maps observed states to actions. |
| B | True (incorrect) | Wrong: a policy need not be learned by RL; policies may be fixed, programmed, learned, deterministic, or stochastic. |
| C | True (incorrect) | Wrong: a learned policy is not guaranteed to beat a fixed rule — limited data, reward misalignment, or regime change can make it worse. |
| D | False (accurate) | Correct: policy quality is judged by relevant outcomes (performance, robustness, costs, risk), not by whether it was handwritten or learned. |
| E | False (accurate) | Correct: states on opposite sides of the threshold can trigger different actions — the state-dependent rule is a genuine policy. |

**Reference:** Sutton & Barto, 2nd ed., §3.5 (definition of a policy — any state→action rule, fixed or learned, deterministic or stochastic). Balch ML4T lectures 03-05/06.

### [ML2-D1G6Q3] Stochastic→greedy deployment; values vs. selection rule
**Scenario:** An autonomous vehicle uses a stochastic lane-selection policy in simulation to explore, but the safety manager wants consistent behavior in deployment. Does making it deterministic change the values or just the selection?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A deterministic policy returns the same chosen action for the same represented state under a fixed decision rule. |
| B | False | A stochastic policy need not put all probability on the top action — it may deliberately assign nonzero probability to lower-valued actions (e.g., for exploration). |
| C | False | Switching from stochastic to greedy selection does not necessarily retrain the stored action values — the selection rule can change independently. |
| D | True | Removing exploratory randomness makes choices more repeatable, but environmental uncertainty can still yield different outcomes. |
| E | True | Policy randomness and environment randomness are separate properties — a policy can be stochastic even in a deterministic environment. |

**Reference:** Sutton & Barto, 2nd ed., §3.5 (policies; deterministic vs. stochastic) and ch.5 (greedy vs. ε-greedy; separating selection from learned values). Balch ML4T lectures 03-05.

### [ML2-D1G7Q1] Labeled sentiment — supervised, not RL
**Scenario:** A group has a fixed dataset of earnings-call passages labeled positive/neutral/negative and only wants to reproduce those labels on new passages, but the director proposes RL because it "sounds advanced."
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The task — mapping inputs to known categorical labels — is naturally supervised classification. |
| B | False | The analyst labels are supervised *targets*, not RL rewards resulting from agent actions. |
| C | False | RL is not necessarily preferable just because a trading team will eventually use the output — the downstream domain does not fix the paradigm for a component task. |
| D | True | An RL formulation would require specifying actions, rewards, and interactions that a labeling task does not inherently need. |
| E | True | Adding an agent and reward artificially increases complexity without improving alignment to the stated prediction goal. |

**Reference:** Sutton & Barto, 2nd ed., ch.1 §1.1 (RL vs. supervised learning — RL needs actions/rewards/interaction); contrast with supervised classification (ISLR ch.4 for the supervised side). Balch ML4T lectures 03-05.

### [ML2-D1G7Q2] Data-center allocation — sequential, RL fits with caveats
**Scenario:** A data-center operator repeatedly allocates jobs across servers while queues, energy prices, and temperatures respond to earlier allocations; it wants to minimize long-run delay/energy cost but cannot risk production exploration.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Wrong: direct observability does not remove sequential dependence — allocations change future queues, temperatures, and options, so decisions are not independent. |
| B | False (accurate) | Correct: RL may fit because the objective concerns a sequence of decisions and their long-run consequences. |
| C | True (incorrect) | Wrong: exploration cost is not irrelevant once a problem is sequential — exploration can degrade service or breach operational limits. |
| D | False (accurate) | Correct: simulators, historical transition data, or constrained exploration should be considered before unrestricted online learning. |
| E | False (accurate) | Correct: suitability for RL does not waive deployment complexity and safety constraints — feasibility is part of choosing/governing an RL solution. |

**Reference:** Sutton & Barto, 2nd ed., ch.1 (characteristics of RL problems; exploration–exploitation) and ch.3 (sequential formulation); on safe/offline exploration see ch.5 (off-policy) and SB discussion of simulation. Balch ML4T lectures 03-05/07.

### [ML2-D1G7Q3] Rebalancing (RL) vs. volatility forecast (supervised)
**Scenario:** An asset manager must choose between RL to rebalance over time and a supervised model to estimate next-month volatility; the CRO wants the approach chosen by the decision problem, not a single favored technique.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Next-month volatility need not be RL — temporal ordering alone does not require it; realized volatility can serve as a supervised regression target. |
| B | True | Rebalancing is sequential: today's trades change holdings, costs, and later choices (state carries forward). |
| C | False | RL is not appropriate for every forecasting problem — producing a forecast is not itself an interactive control problem. |
| D | True | A supervised forecast can be a *state feature* used by an RL rebalancing policy — the two combine naturally. |
| E | True | The expected benefit of sequential optimization must be weighed against RL's data, exploration, validation, and governance costs. |

**Reference:** Sutton & Barto, 2nd ed., ch.1 §1.1 (RL vs. supervised) and ch.3 (when a problem is a sequential control task); hybrid prediction-feeds-control framing. Balch ML4T lectures 03-05/07.

## References (domain-level)

1. **Sutton & Barto — *Reinforcement Learning: An Introduction*, 2nd ed.:** ch.1 §1.1 (what RL is; RL vs. supervised vs. unsupervised; delayed reward and exploration as defining features); §3.1 (agent–environment interface and the control-based boundary); §3.2 (goals and rewards, the reward hypothesis, negative rewards/penalties, reward defines the objective); §3.3 (returns = cumulative reward, episodes, terminal states); §3.4 (unified notation for episodic vs. continuing tasks, discounting); §3.5 (policies and value functions — policy distinct from value estimates, deterministic vs. stochastic); ch.2 and ch.5 (exploration vs. exploitation, ε-greedy, greedy action selection, off-policy learning); ch.12 (eligibility traces / temporal credit assignment).
2. **Reward shaping:** Ng, Harada & Russell (1999), "Policy invariance under reward transformations" — potential-based shaping and the risk of changing the optimized behavior (G5 questions).
3. **Credit assignment:** Minsky (1961), "Steps toward artificial intelligence" — origin of the temporal credit-assignment problem (G5 questions).
4. **Balch — ML4T lectures (Georgia Tech):** RL/Q-Learning problem-framing lectures (03-05), the trading-as-RL formulation and Q-Learning (03-06), and the Dyna / practical-RL considerations (03-07) for episodes, policies, and when RL is appropriate.
5. **Supervised-learning contrast (for G3/G7):** ISLR — *An Introduction to Statistical Learning* (James, Witten, Hastie, Tibshirani), ch.4 (classification) and §2.1 (supervised learning from labeled data) — used only to characterize the supervised alternative, not the RL side.
