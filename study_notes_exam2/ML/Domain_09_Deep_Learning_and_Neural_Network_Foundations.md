# ML Domain 9 — Deep Learning & Neural-Network Foundations

## Domain cheat-sheet

- **Perceptron → MLP → layers.** A single artificial neuron computes a **pre-activation** `z = w·x + b` (weighted sum of inputs plus a trainable **bias**) and then applies an **activation** `a = g(z)`. A **multilayer perceptron (MLP)** stacks layers: an **input layer** (just the feature values — momentum, volatility, volume, etc.), one or more **hidden layers**, and an **output layer**.
  - **Input layer** = the predictor features supplied to the network; it holds the data, not learned transformations.
  - Each hidden unit has its **own incoming weight vector and bias**, so different units in the *same* layer can learn **different weighted combinations** of the identical inputs.
  - The **output layer** form depends on the *task*, not on a universal rule: a **single scalar output** can be a continuous regression value (a return forecast) just as easily as a class score. "Scalar ⇒ class label" is false.
  - A hidden unit normally receives the **previous layer's outputs**, not necessarily the raw inputs — only the first hidden layer touches the inputs directly.
- **Depth vs. width (not interchangeable).** **Width** = number of units *within* a layer; **depth** = number of successive hidden layers. A network with 20 units in one layer and a network with four 5-unit layers both have "20 hidden units" but are **structurally different**: the second is **deeper**, and depth composes transformations stage-by-stage while width spreads them across one stage. **Equal unit totals do not imply equal parameter counts** — parameters depend on how adjacent layers connect and their dimensions. Depth and width are **not** made equivalent by a shared product.
- **Activation functions & nonlinearity.** Without a nonlinear activation, a layer computes only an **affine** map `Wx + b`; **composing affine maps yields a single affine map**, so stacking depth with *no* nonlinearity cannot escape the affine function class (and **biases alone do not** add nonlinearity). Nonlinear activations (ReLU, sigmoid, tanh) are what let stacked layers represent relationships a single affine map cannot. Adding parameters without expanding the representable function class is **redundant parameterization**.
- **Saturation & vanishing gradients.** Sigmoid/tanh are **flat (saturated)** at extreme pre-activations, where the local derivative ≈ 0. During backprop these small derivatives **multiply through layers**, attenuating gradients to earlier parameters (**vanishing gradients**) and slowing learning. Saturation is an *activation-regime* observation — it is **not** evidence of a global minimum, and it does **not** break the forward pass; the concern is **training signal**, not inference. Input scaling / weight initialization influence how often units start saturated (motivation for standardization and careful init).
- **Forward propagation (inference).** Information flows **inputs → hidden layers → output**; each layer consumes the previous layer's activations. The **target label is NOT an input** during ordinary inference — targets are used only to compute training loss. With **fixed parameters and deterministic ops**, identical inputs give identical outputs; changing one input can propagate through many downstream units. **Inference needs only a forward pass** — backprop is for *learning*, not for producing a forecast. Deployment inputs must be **preprocessed the same way** as training inputs (same standardization). The model's **score and the decision rule** that converts it into a trade (e.g., a threshold) are **separate components** — a threshold can change without retraining weights, and a 0.70 score is not a calibrated 70% frequency.
- **Loss functions & learning objectives.** The **loss defines what is optimized**. **Regression** targets (continuous next-day return) → squared-error / MSE; **classification** targets (direction up/down) → cross-entropy on predicted class probabilities. The target's *semantics* — not the shared input features — determine the appropriate objective. **Squaring magnifies large errors**, so a few high-volatility days can dominate unweighted MSE; **reweighting** changes which observations drive training. Crucially, a **lower statistical loss does not guarantee better economic outcomes** (Sharpe, drawdown) — MSE is not a Sharpe objective; evaluate both statistical and economic metrics.
- **Gradient descent & backpropagation.** The **gradient** points in the direction of **steepest local increase** of loss; gradient descent steps in the **negative-gradient** direction, scaled by the **learning rate**. **Backpropagation** applies the **chain rule** over the computational graph to compute gradients for **all** layers efficiently — early-layer gradients depend on how that layer influences later computations and the loss (**credit/blame flows backward**). Order: **forward pass first** (produces activations and loss), then backward pass, then the **optimizer** applies the update. Backprop does **not** pick labels (the dataset does) and does **not** act before the forward pass. A **zero gradient at one parameter** does not prove global optimality. **Learning-rate pathology:** too large → overshoot / oscillation / divergence; too small → stable but very slow. The best rate is problem-dependent, and training curves alone don't establish best *generalization* — need validation evidence.
- **Epochs, batches, training dynamics.** An **epoch** = one full pass over the training set. With 10,000 observations and batch size 100 ⇒ **100 mini-batches/epoch**, and the optimizer updates **after each mini-batch** (not once per epoch). Batch size concerns **observations per update**, not network width. **Mini-batch gradients are noisy estimates** of the full-data gradient and vary with sampling; **full-batch** uses all observations per update but **does not** eliminate nonconvex optimization difficulty or guarantee a global optimum. Batch size trades off **gradient noise, memory, and compute**. Completing an epoch does **not** equalize training and validation loss.
- **Overfitting, capacity & regularization.** A **high-capacity** model can **memorize** a small dataset (near-zero training error) yet **generalize poorly** out of sample; near-zero training error is **not** evidence of out-of-sample stability — **generalization must be measured on held-out data**. When validation loss rises while training loss keeps falling (classic **overfitting** signature), prefer the **validation-minimum checkpoint**, not the final one; training loss alone cannot pick the deployment epoch. Remedies: **dropout** (randomly omit activations so the network doesn't over-rely on specific units/paths), **L2 weight penalty** (add a weight-magnitude term to discourage large parameters), **early stopping** (halt near the validation minimum). Regularization aims to **control effective complexity / improve generalization** — it does **not** increase memorization, and it **cannot guarantee** positive trading returns. Model choice should weigh **data quantity/quality, compute cost, and simpler baselines**; there is **no universal minimum sample count**, and popularity/lower training loss alone never justifies a bigger model.
- **Universal approximation.** A sufficiently wide one-hidden-layer network with a nonlinear activation can approximate a broad class of continuous functions — but **representational capacity ≠ learnability or generalization**: it says nothing about how much data, which optimizer, or how to avoid overfitting. Depth often achieves comparable expressiveness **more parameter-efficiently** than extreme width.

## Common traps

- **Inverted-polarity questions (9 of 21 here).** When the body says "mark each statement **True** when the stated claim is **incorrect** and **False** when it is correct," the Answer Key verdict is flipped relative to the statement's plain truth: **True = the statement is wrong; False = the statement is accurate.** Read the polarity line *first*. Inverted here: **G1Q1, G1Q2, G2Q2, G3Q1, G4Q3, G5Q2, G6Q1, G6Q2, G7Q1.** The remaining 12 are Normal (True = accurate).
- **Scalar output ⇒ classification.** False — a single output can be a continuous regression value; the output's meaning is set by the task/output design, not by its dimensionality.
- **Width = depth / unit-count = structure.** Four units in a layer is **width**, not four layers. Equal total units across two architectures imply neither equal depth nor equal parameter count; depth and width are distinct and not interchangeable by equal product.
- **Depth without nonlinearity is powerful.** False — stacking affine layers (no activation) collapses to one affine map; biases don't add nonlinearity; more parameters needn't enlarge the function class.
- **Saturation = optimization success / breaks forward pass.** Both wrong — saturation is an activation-regime fact that weakens gradients (vanishing gradients); the forward pass still computes fine; it is not proof of a global minimum.
- **Hidden-unit interpretability.** Emergent activation patterns are *learned*, not hand-programmed; internal features need not map to named human indicators, and activation associations do **not** by themselves establish causal/economic meaning.
- **Targets as inference inputs / backprop needed for prediction.** False — labels enter only the training loss; inference is a pure forward pass; backprop is for gradient-based learning.
- **Score = decision = calibrated probability.** The network's score and the threshold rule that turns it into a trade are separate; changing the threshold doesn't retrain weights; a 0.70 score is not a guaranteed 70% real-world frequency across regimes.
- **Lower loss ⇒ better strategy.** False — statistical loss (MSE) is not a trading objective (Sharpe/drawdown); evaluate economic metrics too. Squaring overweights large-error days; reweighting changes what training emphasizes.
- **Objective is fixed by the inputs.** False — the *target definition* (continuous return vs. direction label) determines regression vs. classification loss, even with identical features.
- **Gradient points downhill / only output layer has gradients.** The gradient points toward steepest *increase*; descent subtracts it. Backprop (chain rule) gives gradients for **all** layers; hidden parameters influence the loss through downstream activations.
- **Backprop before forward / backprop picks labels / one zero gradient ⇒ global optimum.** All wrong — forward pass first; labels come from the dataset; a single zero component characterizes neither all parameters nor global optimality.
- **Bigger learning rate always better.** False — too large overshoots/diverges; too small is slow; the right rate is problem-specific and needs validation evidence.
- **Batch size = network width / one update per epoch / full-batch guarantees global optimum.** Batch size is observations-per-update; mini-batch allows many updates per epoch; full-batch removes gradient *noise* but not nonconvex difficulty.
- **More epochs ⇒ better generalization / training loss picks the epoch.** False — past the validation minimum, extra epochs overfit; choose the validation-minimum checkpoint.
- **Near-zero training error ⇒ generalizes / deep beats classical when training loss is lower / popularity decides.** All wrong — memorization isn't generalization; model choice needs validation/test evidence, data sufficiency, cost, and baseline comparison; there's no universal million-sample floor and regularization can't guarantee profits.

## Questions

### [ML2-D9G1Q1] Return-forecasting MLP — input layer, width, bias, output type
**Scenario:** A neural network forecasts next-day return from three inputs (momentum, volatility, volume change) with one hidden layer of four units and one scalar output; every hidden unit receives all three inputs.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the three market indicators are the **input layer** — the layer that supplies the predictor values. The claim is accurate, so the inverted verdict is False. |
| B | False (accurate) | Correct: each hidden unit has its **own incoming weights and bias**, so units can learn different weighted combinations of the same three features. |
| C | True (incorrect) | Wrong: a **scalar output can represent a continuous return** (regression). Output meaning follows the task/output design — it is not forced to be a buy/sell class. |
| D | False (accurate) | Correct: a **bias** is an additive trainable parameter that shifts a unit's pre-activation `z = w·x + b` independently of the current inputs. |
| E | True (incorrect) | Wrong: four units is **width** within one layer; this network still has exactly **one hidden layer**. Width is not depth. |

**Reference:** ISLP ch.10, §10.1–10.2 (single/multilayer neural networks: input/hidden/output layers, weights and bias); Bishop, *Deep Learning: Foundations & Concepts*, ch.1 (neurons, layers, regression vs. classification outputs); Goodfellow-Bengio-Courville, ch.6 (Deep Feedforward Networks — units, affine pre-activation, output units).

### [ML2-D9G1Q2] Two architectures, equal unit totals — depth vs. width vs. parameters
**Scenario:** Network A has one hidden layer with 20 units; Network B has four hidden layers of five units each. A student claims the two are identical because each has 20 hidden units total.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: Network B has **more successive hidden layers**, so it is **deeper**. |
| B | True (incorrect) | Wrong: **equal unit totals do not imply equal trainable parameters** — parameter counts depend on how adjacent layers connect and on their dimensions. |
| C | False (accurate) | Correct: a 20-unit layer is **wider** than each 5-unit layer in Network B. |
| D | False (accurate) | Correct: successive layers **compose transformations** stage-by-stage rather than placing every unit at one stage, so connectivity organizes computation differently. |
| E | True (incorrect) | Wrong: **depth and width are different structural properties** and are not made equivalent by a shared product. |

**Reference:** ISLP ch.10, §10.2 (multilayer networks; layer dimensions determine parameter counts); Goodfellow-Bengio-Courville, §6.4 (architecture design — depth vs. width, representational efficiency of depth); Bishop ch.1 (network architecture and parameterization).

### [ML2-D9G1Q3] Inactive added units — zero weights, zero bias, frozen
**Scenario:** A team adds hidden units but freezes every incoming connection and bias at zero; original parameters and activations are unchanged.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Merely adding structurally present but **inactive** units need not change the computed function — zero-contribution units leave predictions unchanged. |
| B | True | If the added path always emits zero and contributes nothing downstream, the **original network function is preserved**. |
| C | True | **Trainable connections** are precisely what let a unit adapt its influence during learning; frozen-at-zero weights cannot adapt. |
| D | True | A unit's output depends on its **pre-activation**, which combines a weighted input sum **and its bias** — both can shape the output. |
| E | False | Units in **deeper layers normally receive outputs of preceding layers**, not the raw input features directly; direct connection to inputs is not required. |

**Reference:** ISLP ch.10, §10.1–10.2 (feedforward composition; how weights/biases determine unit outputs); Goodfellow-Bengio-Courville, ch.6 (hidden units, parameterization, inactive paths); Bishop ch.1 (parameters and learning).

### [ML2-D9G2Q1] Stacked affine layers with no nonlinearity
**Scenario:** A network uses three fully connected hidden layers with **no** nonlinear activation (each layer is a weighted sum plus bias); the researcher expects depth alone to create nonlinear decision boundaries.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A **composition of affine transformations is itself affine** — three linear layers collapse to one `Wx + b`. |
| B | False | Depth **without a nonlinearity** does not escape the affine function class; more such layers add no nonlinear behavior. |
| C | True | **Nonlinear activations** are what prevent the composition from collapsing into a single affine map, enabling richer relationships. |
| D | False | **Biases shift** affine maps but do not make the composition nonlinear. |
| E | True | The network can have **many parameters yet remain affine** — redundant parameterization does not enlarge the representable function class. |

**Reference:** ISLP ch.10, §10.1 (role of nonlinear activation functions); Goodfellow-Bengio-Courville, §6.3 (hidden units — why nonlinearity is required for expressive power); Bishop ch.1 (activation functions and the limits of linear models).

### [ML2-D9G2Q2] Sigmoid saturation and gradient flow
**Scenario:** A hidden layer uses sigmoid activations; for many observations the pre-activations are extreme, placing units near the flat ends of the sigmoid.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: extreme pre-activations place sigmoid outputs near their limiting values — the units are **saturated**. |
| B | False (accurate) | Correct: flat regions have **small local derivatives**, which attenuate gradients propagated backward (vanishing-gradient mechanism). |
| C | True (incorrect) | Wrong: saturation describes **activation behavior**, not proof the loss has reached a global minimum. |
| D | False (accurate) | Correct: **input scaling and weight initialization** influence pre-activation magnitudes, hence how often units start saturated. |
| E | True (incorrect) | Wrong: the **forward computation still works**; saturation's primary cost is **reduced gradient flow during training**, not an impossible forward pass. |

**Reference:** ISLP ch.10, §10.7 (fitting networks; difficulties of optimization); Goodfellow-Bengio-Courville, §6.3 and §8.2 (saturating activations, vanishing gradients, effect of initialization/scaling); Bishop ch.1 (activation functions and gradient behavior).

### [ML2-D9G2Q3] Learned hidden representations — interpretation limits
**Scenario:** After training, one hidden unit activates on high-momentum/low-volatility observations and another on high-volatility observations regardless of momentum.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Learned weights and nonlinearities let hidden units **encode useful feature combinations**. |
| B | False | The patterns can **emerge from training** without any explicit human-assigned financial meaning — they were not manually programmed. |
| C | True | Different parameters let **different units develop distinct internal representations**. |
| D | False | Internal features **need not align** with named, human-designed indicators. |
| E | False | Observed activation associations **do not by themselves establish** a causal or economic interpretation. |

**Reference:** ISLP ch.10, §10.1–10.2 (hidden-unit representations as learned feature transformations); Goodfellow-Bengio-Courville, §6.4 and ch.15 (learned/distributed representations; interpretation caveats); Bishop ch.1 (feature learning).

### [ML2-D9G3Q1] Forward propagation and inference semantics
**Scenario:** A trained network takes a standardized indicator vector; the first hidden layer computes weighted sums and activations, the second processes those outputs, and the output layer produces a return forecast.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: **forward propagation** moves information inputs → successive layers → output — exactly the described sequence. |
| B | True (incorrect) | Wrong: the **target label is not an ordinary inference input**; targets are used to evaluate predictions during training, not fed into hidden layers at inference. |
| C | False (accurate) | Correct: with fixed weights, biases, and activations, the output is determined by the **learned parameters and the supplied inputs**. |
| D | True (incorrect) | Wrong: inference needs only a **forward pass**; **backpropagation** is for gradient-based *learning*, not for producing each forecast. |
| E | False (accurate) | Correct: **standardization applied in training must be applied consistently** to deployment inputs so features are represented the same way. |

**Reference:** ISLP ch.10, §10.1–10.2 (forward pass) and §10.7 (training uses targets/backprop; preprocessing consistency); Goodfellow-Bengio-Courville, §6.3–6.5 (forward propagation vs. back-propagation); Bishop ch.1 (inference vs. training).

### [ML2-D9G3Q2] Deterministic inference with fixed parameters
**Scenario:** A model is in evaluation mode with fixed parameters; the same input is submitted twice; all eval-time operations are deterministic and no parameters update between submissions.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Identical inputs under **deterministic, fixed computation** yield identical outputs. |
| B | False | Parameters are fixed, but the output **remains a function of the supplied input** — it is not input-independent. |
| C | True | Changing one input can **propagate through multiple connected downstream units**. |
| D | False | **Multilayer** networks can also perform deterministic inference — determinism is not limited to single-layer models. |
| E | True | With **dropout disabled** for evaluation, it will not randomly remove different units across the two passes (eval uses full-network behavior). |

**Reference:** ISLP ch.10, §10.7 (dropout active in training, disabled at inference); Goodfellow-Bengio-Courville, §7.12 (dropout — training vs. test-time behavior); Bishop ch.1 (deterministic forward computation).

### [ML2-D9G3Q3] Score vs. decision threshold
**Scenario:** A binary classifier outputs 0.70; the system trades only when the score exceeds a threshold; the team changes the threshold from 0.50 to 0.80 without retraining.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The **forward-pass score can stay 0.70** — the threshold is part of the decision rule, not the neural computation. |
| B | True | Under a strict exceeds-threshold rule, 0.70 is **above 0.50 but below 0.80**, so it triggers at 0.50 but not at 0.80. |
| C | False | A **post-model threshold** can change **without updating** the network's learned weights. |
| D | True | The **output score and the rule converting it to a trade** are conceptually distinct system components. |
| E | False | A 0.70 score **does not prove** a 70% realized frequency in every regime — that requires valid **calibration** and stability. |

**Reference:** ISLP ch.10, §10.1 (classification outputs/probabilities) and ch.4 (thresholds, calibration context); Goodfellow-Bengio-Courville, §5.7 (decision thresholds vs. model outputs); Bishop ch.1 (probabilistic outputs and decision rules).

### [ML2-D9G4Q1] MSE improves but trading metrics worsen
**Scenario:** A network minimizing MSE for next-day returns shows improved validation loss, yet the strategy has lower Sharpe and worse drawdown than a simpler benchmark; a scientist argues it is still better because prediction loss is lower.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | **Lower prediction loss does not guarantee better trading performance** — prediction quality and trading utility differ. |
| B | True | The **loss function may be misaligned** with the strategy objective (portfolio outcomes). |
| C | True | **Trading metrics can worsen** even as forecast error improves — small accuracy gains need not improve positions. |
| D | False | **MSE is not a Sharpe-ratio objective** — it does not directly optimize Sharpe. |
| E | True | Strategy evaluation should include **economic as well as statistical** metrics. |

**Reference:** ISLP ch.10, §10.3 (choosing loss functions / fitting objective); Goodfellow-Bengio-Courville, §5.1–5.2 (performance measure vs. training objective); Bishop ch.1 (loss selection and task alignment).

### [ML2-D9G4Q2] Regression vs. classification output and loss
**Scenario:** One team predicts a continuous next-day return; another classifies whether the return is positive; identical inputs but different output layers and losses.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A **continuous numerical return** is naturally a **regression** target. |
| B | True | A **probability-based classification output** can be trained against categorical **direction labels** (cross-entropy). |
| C | False | Identical inputs do **not** force the same objective — the **target definition** determines the appropriate loss. |
| D | False | **Ordinary direction labels discard exact magnitude**; a direction classifier is not penalized for magnitude unless the objective explicitly includes it. |
| E | True | Loss selection requires considering **what the target and output represent** (task semantics). |

**Reference:** ISLP ch.10, §10.1–10.3 (regression vs. classification outputs; squared-error vs. cross-entropy); Goodfellow-Bengio-Courville, §6.2 (output units and cost functions by task); Bishop ch.1 (regression vs. classification losses).

### [ML2-D9G4Q3] Unweighted MSE and large-error days
**Scenario:** A return forecaster minimizes **unweighted** MSE; a few high-volatility days have very large errors while most quiet days have small errors; the team wants to know what the objective emphasizes.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: **squaring magnifies** the contribution of large-absolute-error observations, so big misses count disproportionately. |
| B | True (incorrect) | Wrong: unweighted MSE does **not** automatically equalize regimes — regimes with more observations or larger errors exert greater aggregate influence. |
| C | False (accurate) | Correct: a **differently weighted loss** changes which observations/groups most affect training. |
| D | True (incorrect) | Wrong: a lower MSE **does not guarantee** lower maximum drawdown — forecast loss and portfolio drawdown are different quantities. |
| E | False (accurate) | Correct: the team should check whether the **statistical loss reflects the trading consequences** that matter (objective alignment). |

**Reference:** ISLP ch.10, §10.3 (squared-error loss properties); Goodfellow-Bengio-Courville, §5.1–5.2 and ch.8 (weighted objectives, loss emphasis); Bishop ch.1 (squared error sensitivity to large residuals).

### [ML2-D9G5Q1] Gradient-descent update mechanics
**Scenario:** During training a network computes a mini-batch loss and its gradient with respect to each trainable parameter; the optimizer applies a standard gradient-descent update.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The gradient points in the direction of **steepest local increase** of loss (usual Euclidean interpretation). |
| B | True | Standard gradient descent moves parameters in the **negative-gradient** direction to reduce loss locally. |
| C | False | **One zero gradient component** does not characterize all parameters or establish **global optimality**. |
| D | True | The **learning rate scales** the size of the parameter update (multiplies the gradient). |
| E | False | **Hidden-layer parameters affect downstream activations** and therefore the loss — gradients are computed for them too, not only the output layer. |

**Reference:** ISLP ch.10, §10.7 (gradient descent and backpropagation; learning rate); Goodfellow-Bengio-Courville, §4.3 and §6.5 (gradient-based optimization, learning rate, back-propagation to all layers); Bishop ch.1 (gradient descent).

### [ML2-D9G5Q2] Backpropagation via the chain rule
**Scenario:** A deep network makes a prediction, compares it with the target, then uses backpropagation to compute gradients for parameters in all layers.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: backpropagation applies the **chain rule** through the computational graph, combining local derivatives efficiently. |
| B | False (accurate) | Correct: an **early layer's gradient depends on how it influences later computations and the loss** — credit/blame is transmitted through downstream dependencies. |
| C | True (incorrect) | Wrong: a **forward pass must run first** to produce the activations and loss needed for the backward computation — weights are not changed before it. |
| D | True (incorrect) | Wrong: **targets come from the dataset/problem design**, not from backpropagation. |
| E | False (accurate) | Correct: once gradients are available, a **gradient-based optimizer updates parameters** with them. |

**Reference:** ISLP ch.10, §10.7 (backpropagation and the chain rule); Goodfellow-Bengio-Courville, §6.5 (back-propagation algorithm; forward then backward pass); Bishop ch.1 (automatic differentiation / error backpropagation).

### [ML2-D9G5Q3] Learning-rate extremes
**Scenario:** Two otherwise identical runs use learning rates 0.0001 and 10.0; the high-rate run's loss oscillates and sometimes grows, while the low-rate run improves very slowly.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | An **excessively large** learning rate can **overshoot** useful parameter regions (jumping across/away from lower-loss areas). |
| B | True | A **very small** learning rate can be stable but require **many updates** for substantial progress. |
| C | False | The behavior does **not** prove 0.0001 is globally optimal for every dataset — appropriate rates depend on model, data, and optimizer. |
| D | False | Increasing the learning rate does **not always** reduce final validation loss — larger steps can destabilize or converge worse. |
| E | False | Training curves **alone** do not establish best **validation/generalization** performance — validation evidence is still needed. |

**Reference:** ISLP ch.10, §10.7 (learning-rate selection and training stability); Goodfellow-Bengio-Courville, §8.3–8.5 (learning rate, oscillation/divergence, tuning); Bishop ch.1 (optimization step size).

### [ML2-D9G6Q1] Epochs and mini-batches
**Scenario:** A training set of 10,000 observations is trained with mini-batches of 100, processing every observation once per epoch.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: one **epoch** is one complete pass through all 10,000 training observations. |
| B | False (accurate) | Correct: 10,000 ÷ 100 = **100 mini-batches** per epoch. |
| C | False (accurate) | Correct: mini-batch training normally **updates parameters after each batch**, not once per epoch. |
| D | True (incorrect) | Wrong: **batch size** concerns observations processed per update, **not network width** (number of hidden units). |
| E | True (incorrect) | Wrong: completing one epoch **does not guarantee** training and validation losses are equal. |

**Reference:** ISLP ch.10, §10.7 (epochs, mini-batches, SGD updates); Goodfellow-Bengio-Courville, §8.1 (minibatch stochastic gradient descent; epochs); Bishop ch.1 (stochastic/minibatch training).

### [ML2-D9G6Q2] Full-batch vs. mini-batch gradients
**Scenario:** A researcher compares full-batch gradient descent (each update from the entire dataset) with mini-batch training (a subset per update).
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a **mini-batch gradient varies** with which observations are sampled (a noisy estimate of the full-data gradient). |
| B | False (accurate) | Correct: **full-batch updates use all training observations** per gradient — that is the defining characteristic. |
| C | True (incorrect) | Wrong: mini-batch training normally permits **several updates per epoch**, not just one per full pass. |
| D | True (incorrect) | Wrong: full-batch gradients remove sampling noise but **do not make a nonconvex problem globally solvable** or guarantee a global optimum. |
| E | False (accurate) | Correct: **batch size trades off** gradient noise, memory use, and computational efficiency. |

**Reference:** ISLP ch.10, §10.7 (batching and stochastic gradients); Goodfellow-Bengio-Courville, §8.1–8.2 (minibatch vs. batch methods; gradient noise; nonconvex optimization); Bishop ch.1 (batch vs. stochastic training tradeoffs).

### [ML2-D9G6Q3] Early stopping vs. deploying the final epoch
**Scenario:** A network trains for 200 epochs; training loss declines throughout, but validation loss bottoms near epoch 40 then rises; the team deploys epoch-200 parameters because they received the most updates.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Divergence after epoch 40 (training improving, validation worsening) is a classic **overfitting** signature. |
| B | False | **More epochs do not necessarily improve** unseen-data performance — continued optimization can harm generalization. |
| C | True | A **validation-based checkpoint near the validation minimum** may generalize better than the final checkpoint (early stopping). |
| D | False | **Training loss alone is insufficient** to choose the deployment epoch — it does not measure unseen-data performance. |
| E | True | Monitoring **both training and validation curves** reveals changing generalization during training. |

**Reference:** ISLP ch.10, §10.7 (early stopping; monitoring validation loss); Goodfellow-Bengio-Courville, §7.8 (early stopping as regularization); Bishop ch.1 (overfitting and validation-based model selection).

### [ML2-D9G7Q1] Overfitting and model capacity
**Scenario:** A very large network nearly memorizes a small dataset (≈0 training error) but performs poorly on a later test period; a smaller tree-based model does moderately well on both.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the result is consistent with **excessive capacity relative to the available data** — a high-capacity model can memorize limited observations. |
| B | True (incorrect) | Wrong: **near-zero training error does not prove** the relationship persists out of sample. |
| C | False (accurate) | Correct: the **test result matters** — generalization must be evaluated outside the fitting observations. |
| D | True (incorrect) | Wrong: a deep model is **not necessarily preferable** whenever its training loss is lower — choice must weigh validation/test performance, complexity, cost, and task. |
| E | False (accurate) | Correct: more expressive models can fit **genuine structure but also noise** — capacity alone does not separate signal from sample-specific noise. |

**Reference:** ISLP ch.10, §10.7 and ch.2 §2.2 (capacity, overfitting, bias–variance, test-error assessment); Goodfellow-Bengio-Courville, §5.2 (capacity, overfitting, generalization); Bishop ch.1 (model complexity and overfitting).

### [ML2-D9G7Q2] Dropout, L2, and early stopping
**Scenario:** A team considers dropout, an L2 weight penalty, and early stopping for a network whose validation performance degrades while training loss keeps improving.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | **Dropout** randomly omits activations during training, reducing reliance on specific units/paths. |
| B | True | An **L2 penalty** adds a weight-magnitude term to the objective, discouraging very large parameters. |
| C | True | **Early stopping** can select a checkpoint before validation performance deteriorates further. |
| D | False | These methods **cannot guarantee positive trading returns** in every out-of-sample period. |
| E | False | Regularization aims to **control effective complexity / improve generalization**, not to increase training-set memorization. |

**Reference:** ISLP ch.10, §10.7 (dropout, ridge/L2 regularization, early stopping); Goodfellow-Bengio-Courville, ch.7 (regularization — L2/weight decay §7.1, dropout §7.12, early stopping §7.8); Bishop ch.1 (regularization for generalization).

### [ML2-D9G7Q3] Choosing capacity under limited data and compute
**Scenario:** A firm with 2,000 labeled observations and limited compute proposes a massive deep network "because deep learning is popular," without baselines or data/training-cost estimates.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | **Popularity alone** does not establish that the massive network is the best model — suitability must be shown empirically. |
| B | True | **Data amount and quality constrain** the benefit of a high-capacity network (insufficient representative data raises overfitting risk). |
| C | True | Training and tuning a **large network commonly costs more computation** than fitting a small classical model. |
| D | True | Comparing against **simpler baselines** reveals whether added complexity provides meaningful out-of-sample value. |
| E | False | There is **no universal minimum sample count** (e.g., one million) — suitability depends on the problem, architecture, and evidence. |

**Reference:** ISLP ch.10, §10.6–10.7 and ch.2 (when to prefer complex vs. simple models; baselines; data requirements); Goodfellow-Bengio-Courville, §5.2–5.3 and ch.11 (capacity vs. data, practical methodology, baselines); Bishop ch.1 (model selection and data sufficiency).

## References (domain-level)

1. **ISLP — *An Introduction to Statistical Learning* (Python ed.), ch.10 "Deep Learning":** §10.1 (single-layer networks, activation functions, output types); §10.2 (multilayer networks, layers, width/depth, weights and bias); §10.3 (fitting a network — loss/objective, regression vs. classification); §10.6–10.7 (practical considerations, backpropagation and gradient descent, learning rate, epochs/mini-batches, dropout, L2/ridge regularization, early stopping, overfitting). Bias–variance/overfitting context in ch.2 §2.2; classification/calibration context in ch.4.
2. **Bishop — *Deep Learning: Foundations & Concepts*, ch.1:** neurons and the perceptron, network architecture, activation functions, regression vs. classification outputs and losses, gradient-based training and error backpropagation, overfitting and regularization — used for conceptual foundations.
3. **Goodfellow, Bengio & Courville — *Deep Learning*:** ch.6 (Deep Feedforward Networks — units, affine pre-activation, output units §6.2, hidden units/nonlinearity §6.3, architecture/depth §6.4, back-propagation §6.5); ch.7 (Regularization — L2/weight decay §7.1, early stopping §7.8, dropout §7.12); ch.8 (Optimization — minibatch SGD §8.1, nonconvex difficulties §8.2, learning rate §8.3–8.5); §5.1–5.3 (capacity, overfitting, generalization, performance measure vs. objective). Section-level citations only; no page numbers asserted.

---

**Source-fidelity note:** Verdicts above are transcribed **exactly** from `slices/ML2_D09.txt` and never flipped. For the 9 inverted-polarity questions, the slice's "False – The underlying claim is correct" is rendered **False (accurate)** and "True – The underlying claim is incorrect" is rendered **True (incorrect)**, preserving the slice's letter verdict verbatim.

**Garbled-symbol flag:** The source `.txt` is littered with **fi/fl ligature artifacts** from PDF extraction — e.g., "ﬁve/ﬁrst/ﬁxes/ﬁts/ﬁrm," "ﬂat," "beneﬁt," "classiﬁer/classiﬁcation," "speciﬁc," "inﬂuence," "deﬁned/deﬁning," "modiﬁes," "magniﬁes," "reﬂects," "overﬁtting," "proﬁtability," "veriﬁcation." These are rendering glitches (the "fi"/"fl" glyphs), not content errors; they have been silently normalized to plain ASCII in the scenarios/explanations above. The recurring `NNN Rev:081020261230` strings and bare page numbers in the slice are pagination footers, not question content.
