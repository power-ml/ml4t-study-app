# ML Domain 10 — Sequential, Generative & Responsible AI

## Domain cheat-sheet

- **Sequence data, temporal validity, and leakage (G1).** Financial observations are *ordered in time* and the pipeline must respect that order end-to-end:
  - **Order carries information.** A window of lagged returns is a *sequence*, not an unordered set — the position of each value records *when* it occurred, and temporal patterns depend on that ordering. Treating a fixed-length window as an i.i.d. feature vector does **not** remove temporal dependence, overlap, or distribution change.
  - **Overlapping windows create dependence.** Adjacent windows share many of the same underlying daily returns, so a **random** train/test split can place near-duplicate, highly correlated samples on both sides and mix future and past regimes. A random split does **not** enforce a realistic information boundary; a **chronological** split (train on the past, evaluate on a later period) does.
  - **Look-ahead bias.** A feature is only legitimate if its value was *available at the decision time*. A day-*t* close/volume or a trailing moving average computed through day *t* is fine; a **revised statistic released on day t+3** used as though known on day *t* leaks the future. Timestamps must reflect *when information became available*, not the date it refers to. Strong test performance does **not** prove the absence of leakage — leakage *inflates* apparent performance.
  - **Regime shift / distribution change.** A model trained in a low-volatility regime and evaluated in a crisis can show rising error because the **data-generating process changed**, not because of a bug. Temporal dependence *within* a sequence does **not** imply stationarity *across* regimes. Retraining on the test interval before reporting makes it in-sample and invalidates the evaluation. Valid timestamp handling is **necessary but not sufficient** for robustness.
- **Convolutional models for sequences (G2).** A 1-D convolution slides a **shared filter** (parameter sharing) across consecutive segments of the series. A single learned filter can detect a *local motif wherever it occurs* (translation equivariance), using far fewer parameters than a separate detector per position. Each first-layer activation sees only its **local receptive field** (e.g., three positions), not the whole 250-day window; **stacking layers / larger kernels / dilation / pooling** expand the effective receptive field and let distant positions interact. Multi-channel filters span time *and* aligned feature channels (return, volume, volatility). **Global pooling** keeps detection strength but discards *where* a motif occurred. Convolution preserves local ordering (arbitrary permutations change activations) — but architecture guarantees **no** economic stability, generalization, or causality. (ISLP ch.10 §10.3, CNNs.)
- **Recurrent and memory-based models (G3).** An RNN reads one step at a time, combining the current input with the **previous hidden state** to form a new state — a mechanism for earlier observations to influence later computation, with **transition parameters shared across time**. Because updates are sequential, order matters (two orderings of the same values generally give different final states). The hidden state is an *internal representation*, not the target label. **Vanishing gradients:** repeated multiplication through a long recurrent chain shrinks gradients, so plain RNNs learn short lags but struggle at ~100 steps; **gated units (LSTM/GRU)** add memory/gating paths to preserve information and gradient flow. Longer input length does **not** guarantee learning a distant relation (it can worsen optimization/noise), and failure to learn does **not** prove the distant observation is uninformative. **Stateful inference:** carrying hidden state across independent sequences (Stock A → Stock B without reset) contaminates B's early predictions; reset/initialize at genuine sequence boundaries unless continuity is part of the intended problem. (ISLP ch.10 §10.5, RNNs/LSTM.)
- **Attention and transformers (G4).** Self-attention lets any position **directly aggregate** information from any other position (no step-by-step traversal), with weights that are **learned query–key compatibilities of the content**, not fixed by calendar distance — and the computation **parallelizes** across positions, unlike strictly sequential recurrence. Soft attention assigns *small nonzero* weights broadly, so it does **not** guarantee zero weight on irrelevant inputs, and a large weight is an *association*, not proof of causality. Content-only attention is **permutation-equivariant**: without **positional encoding** it cannot distinguish "loss then gain" from "gain then loss"; incidental feature–time correlations are not a reliable ordering mechanism, and removing positional info does **not** turn a transformer into an RNN. A **causal mask** restricts each position to past information; a mask that lets day *t* attend to the day *t+1* target is **look-ahead leakage** that makes training loss artificially low and a leaky test set a non-deployable simulation. (ISLP ch.10, sequence models; attention conceptually.)
- **Generative AI and LLMs (G5).** LLMs genuinely help *transform unstructured text* into summaries/drafts, but a grounded source does **not** guarantee complete or faithful output (models can omit, misread, or invent). **Fluent generation ≠ validated forecast:** text quality and out-of-sample, cost-aware trading performance are different objectives, and a language-model objective (next-token prediction) is not automatically aligned with risk-adjusted returns. Producing a well-formatted label ("BUY/HOLD/SELL") says nothing about predictive value — predictive claims require evaluation against *subsequent outcomes* with turnover and transaction costs included. **RAG** supplies current, task-specific evidence and citations aid traceability, but retrieval does **not** guarantee the cited source entails every sentence; retrieval quality bounds the grounded answer, and a citation must be *checked*, not trusted as proof.
- **Hallucination, verification, and human oversight (G6).** Fluent, confident prose can carry **unsupported or fabricated claims** — writing polish is not a reliability signal, and a *real* source citation does not excuse a *materially wrong* value (40% vs. actual 14%). Finite development-time sampling cannot guarantee correctness of every future numeric claim; a track record of acceptable summaries does not validate the current one. **Human review, source verification, risk-based checks on consequential figures, and clear accountability** remain essential in high-stakes finance. For an **autonomous order-sending agent**, a daily dollar limit constrains one exposure dimension but not misinformation, correlated actions, or operational failure — source-quality rules, anomaly alerts, escalation/intervention, and a named human owner are still required. Autonomy *raises* the importance of accountability.
- **Bias, explainability, and responsible deployment (G7).** Strong **aggregate** accuracy can hide materially different error rates across subgroups because the majority dominates the average; historical data encodes past selection practices and structural inequities, and **dropping protected attributes does not remove bias** (proxy/correlated features reproduce it). Disaggregated, subgroup evaluation is needed — predictive performance and fairness are **separate** questions. **Explainability:** feature-attribution can aid investigation of a prediction, but attribution is an *association* (not a causal-intervention effect), can be useful without making the model transparent, and an explanation that is **unstable** under tiny economically irrelevant perturbations is suspect — explanations must be judged for fidelity, stability, and audience. **Governance:** a single backtest does not establish permanent safety; data and behavior drift even when code is unchanged, so responsible deployment requires ongoing **monitoring, versioning/traceability, thresholds, and escalation** as design elements, not afterthoughts. (Isbell/Littman ML4T keynote on algorithmic bias; Handbook of AI & Big Data in Investments, responsible-AI / model-risk & governance.)

## Common traps

- **Inverted-polarity questions (9 of 21 here).** When the body says "mark each statement True when the stated claim is **incorrect** and False when it is correct," the Answer Key verdict is flipped relative to the statement's truth: **True = the statement is wrong; False = the statement is accurate.** Read the polarity line *first*. Inverted here: **G1Q1, G2Q3, G3Q1, G3Q3, G4Q3, G5Q1, G6Q2, G7Q2, G7Q3.** The remaining 12 are Normal (True = accurate).
- **"Fixed-length window ⇒ i.i.d."** False — a fixed vector size does not erase temporal dependence, window overlap, or distribution change; and overlapping windows leak across a *random* split.
- **"Random split prevents future→past leakage."** Backwards — random assignment *mixes* regimes and future/past; only a chronological boundary enforces a realistic information cut.
- **"Trailing aggregate = leakage."** False — a lagged moving average is valid if *every component* was available before the prediction deadline; leakage is about *availability timing*, not about containing many observations.
- **"Good test performance proves no leakage."** Backwards — leakage *inflates* test performance; it hides, rather than reveals, itself.
- **"Rising crisis error = a coding bug."** Not necessarily — it is consistent with regime change / non-stationarity even in a correct pipeline. And valid timestamps alone don't guarantee robustness to a new regime.
- **"Retrain on the test interval, then report."** Invalidates the out-of-sample claim — the crisis interval becomes in-sample.
- **CNN receptive field.** A width-3 filter sees 3 positions, *not* all 250 days; reach over distance comes from depth, kernel size, dilation, and pooling. Each position does **not** get its own filter — that would destroy the parameter sharing.
- **"No recurrence ⇒ can't handle order."** False — 1-D CNNs and attention both process ordered data without recurrent state.
- **"Global pooling keeps location."** No — pooling retains detection strength but discards *where* the motif occurred.
- **RNN myths.** Hidden state ≠ label; same values in different order ≠ same final state; longer sequences don't guarantee learning long-range deps; inability to learn ≠ absence of signal; recurrent inference is **not** stateless (forgetting to reset contaminates the next sequence).
- **Attention myths.** Self-attention is *not* strictly sequential (it parallelizes); weights aren't fixed by distance; soft attention rarely assigns exact zero to irrelevant inputs; big weight ≠ causality; **no positional encoding ⇒ permutation-equivariant** (can't tell order), and removing it does *not* create an RNN.
- **Leaky attention mask.** Letting day *t* attend to day *t+1* (the target) is target leakage; reusing the leaky mask at test time measures a non-deployable task.
- **"Fluent/cited ⇒ correct."** False — a confident tone is not a confidence measure; a real citation does not excuse a materially wrong figure; RAG does not guarantee the source entails the claim; citations must be opened and checked.
- **"Valid label format ⇒ predictive value."** False — syntactic BUY/HOLD/SELL compliance says nothing about returns; evaluate on subsequent outcomes with turnover and costs. Next-token objective ≠ risk-adjusted-return objective.
- **"Dollar limit / autonomy ⇒ no human owner needed."** Backwards — a position cap verifies no claims; autonomy *increases* the need for source checks, anomaly alerts, escalation, and a named accountable owner.
- **Fairness myths.** High aggregate accuracy can hide subgroup harm; removing protected attributes leaves proxy features; accuracy and fairness are separate evaluations.
- **Explainability myths.** Attribution is association, not a causal intervention effect; an *unstable* explanation is unreliable; "produced a chart" ≠ satisfied governance (fidelity/stability/audience matter).
- **"One backtest ⇒ permanently safe / code unchanged ⇒ no monitoring."** False — drift, external change, and degraded outcomes occur without any code change; monitoring, versioning, thresholds, and escalation are ongoing obligations.

## Questions

### [ML2-D10G1Q1] Overlapping windows and a random train/test split
**Scenario:** A researcher builds one sample per trading day from the preceding 20 days' returns to forecast the next day's return, then randomly splits the overlapping samples into training and test sets.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the sequence records *when* each return occurred, and temporal patterns can depend on that ordering, so the order would be lost by treating the window as an unordered set. |
| B | False (accurate) | Correct: adjacent windows share many of the same underlying daily returns, creating dependence that can place closely related observations in both training and test sets. |
| C | True (incorrect) | Wrong: a random split does **not** prevent future dates from influencing earlier selection — random assignment mixes future and past regimes and enforces no realistic information boundary. |
| D | False (accurate) | Correct: a chronological split better represents training on the past and evaluating on a later period, matching how a forecaster receives information. |
| E | True (incorrect) | Wrong: a fixed window length does **not** make observations i.i.d. — temporal dependence, overlap, and distribution change remain. |

**Reference:** ISLP ch.10 (sequence models — ordered inputs and sequence structure); Handbook of AI & Big Data in Investments (time-series validation, train/test design, and look-ahead avoidance in financial ML).

### [ML2-D10G1Q2] Feature availability and look-ahead bias
**Scenario:** A model forecasts the day *t+1* close-to-close return using the day-*t* close, day-*t* volume, a five-day moving average through day *t*, and a revised economic statistic not released until day *t+3*.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Day-*t* market variables are legitimate predictors when they are available at the moment the forecast is formed. |
| B | False | A trailing five-day moving average is *not* automatically leakage — a lagged aggregate is valid when every component was available before the prediction deadline. |
| C | True | Using the day-*t+3* revised statistic as though it were known on day *t* gives the model information a real trader could not yet observe — look-ahead bias. |
| D | True | Feature timestamps should reflect *when information became available*, not merely the date the information refers to. |
| E | False | Strong test performance does *not* prove the revised statistic was harmless — leakage inflates test performance rather than revealing itself through poor results. |

**Reference:** ISLP ch.10 (constructing supervised inputs from sequences); Handbook of AI & Big Data in Investments (point-in-time data, data revisions, and look-ahead bias in investment models).

### [ML2-D10G1Q3] Regime shift and distribution change
**Scenario:** A sequence model trained during a long low-volatility regime is evaluated during a later crisis; input construction is temporally valid but forecast error rises sharply.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The result may reflect a change in the data-generating process, not a coding error — financial relationships and volatility can shift across regimes even with a correct pipeline. |
| B | False | Temporal dependence within a sequence does *not* guarantee that learned relationships stay stable across regimes — dependence does not imply stationarity over time. |
| C | True | A chronological test holds the model out against the distribution encountered *after* training and can expose regime sensitivity a randomly mixed split would obscure. |
| D | False | Retraining on the combined training and crisis data before reporting makes that interval in-sample and *invalidates* the original out-of-sample evaluation. |
| E | False | Valid timestamp handling avoids leakage but does *not* by itself guarantee useful forecasts under distribution shift. |

**Reference:** ISLP ch.10 (sequence models and generalization); Handbook of AI & Big Data in Investments (non-stationarity, regime change, and out-of-sample evaluation / model risk).

### [ML2-D10G2Q1] 1-D convolution, parameter sharing, and receptive field
**Scenario:** A 1-D convolutional network applies the same width-three filter to every consecutive three-day segment of a return series before later layers.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A shared local filter can learn a three-day motif and respond to it wherever it occurs in the window (translation equivariance). |
| B | True | Reusing the same filter coefficients across positions *is* parameter sharing — the defining property of convolution. |
| C | False | Each position does *not* require separate parameters — position-specific coefficients would remove the sharing described. |
| D | True | Each first-layer activation is computed only from the values in its local receptive field. |
| E | False | A width-three filter's direct receptive field is three positions, *not* the entire 250-day sequence. |

**Reference:** ISLP ch.10 §10.3 (convolutional neural networks — filters, parameter sharing, local receptive fields).

### [ML2-D10G2Q2] Stacked convolutions and effective receptive field
**Scenario:** A team stacks several convolutional layers over minute-by-minute prices; deeper units combine earlier local activations with no recurrent state.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Stacking layers can expand the effective receptive field, so deeper units depend on a broader portion of the input. |
| B | True | Early filters can detect short motifs that later layers compose into longer patterns (hierarchical composition). |
| C | False | Absence of recurrence does *not* mean the architecture cannot process ordered data — 1-D convolution operates over ordered positions without recurrent state. |
| D | True | Whether distant events interact depends on kernel sizes, depth, dilation, and pooling choices. |
| E | False | Convolution's parameter sharing provides *no* guarantee that a learned relationship stays profitable when the regime changes. |

**Reference:** ISLP ch.10 §10.3 (CNN depth, pooling, and receptive-field growth).

### [ML2-D10G2Q3] Multi-channel filters and global pooling
**Scenario:** A convolutional model receives three aligned daily channels (return, volume change, volatility); one filter spans five days and all three channels, followed by global pooling.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the filter combines values across both its five-day temporal width and the aligned feature channels, so it can respond to a joint multi-channel pattern. |
| B | False (accurate) | Correct: sharing one detector across time uses fewer parameters than learning a separate five-day detector for every position. |
| C | False (accurate) | Correct: global pooling can retain detection strength while discarding precise information about *where* the motif occurred. |
| D | True (incorrect) | Wrong: a convolutional output is *not* invariant to every reordering — convolution preserves and uses local ordering, so arbitrary permutations generally change its activations. |
| E | True (incorrect) | Wrong: adding channels changes available input information but guarantees *neither* generalization *nor* causality — more inputs can help or hurt. |

**Reference:** ISLP ch.10 §10.3 (multi-channel convolution and pooling); conceptual link to feature-channel design.

### [ML2-D10G3Q1] Recurrent hidden state as carried memory
**Scenario:** A recurrent model reads daily indicators one day at a time, combining the current inputs with the preceding hidden state to form a new hidden state.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: state recurrence carries a learned summary of prior processing forward, so earlier observations can influence later computation. |
| B | True (incorrect) | Wrong: two sequences with the same observations in *different orders* generally produce *different* final hidden states — sequential updates make the state order-sensitive. |
| C | False (accurate) | Correct: standard recurrent architectures reuse the same transition parameters at successive time steps (parameter sharing across time). |
| D | False (accurate) | Correct: the final prediction can depend on both recent inputs and information carried forward from earlier steps. |
| E | True (incorrect) | Wrong: the hidden state is an internal representation, *not* the target label the model is trained to predict. |

**Reference:** ISLP ch.10 §10.5 (recurrent neural networks — hidden state, weight sharing across time).

### [ML2-D10G3Q2] Vanishing gradients and gated units
**Scenario:** An ordinary RNN handles a signal one or two days before the target but fails at ~100 steps; gradients propagated across many steps become extremely small during training.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Gradients shrinking across many steps is the classic signature of *vanishing gradients* (repeated multiplication through the recurrent chain). |
| B | True | Weak long-range gradient flow gives earlier parameters little learning signal, making distant dependencies hard to learn. |
| C | True | Gated recurrent units such as LSTMs are designed in part to improve information and gradient flow across time via memory/gating paths. |
| D | False | Increasing sequence length does *not* guarantee the distant relationship is learned — longer inputs can intensify optimization and noise problems. |
| E | False | Training failure does *not* prove the observation 100 steps earlier is uninformative — it may reflect an optimization limitation, not absence of signal. |

**Reference:** ISLP ch.10 §10.5 (RNN training difficulties; LSTM/gated memory for long-range dependence).

### [ML2-D10G3Q3] Stateful inference and cross-sequence contamination
**Scenario:** A recurrent trading model keeps hidden state continuously across companies, finishing Stock A then starting Stock B without resetting, though the two sequences are unrelated.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: Stock B's starting state still encodes the preceding processing of Stock A, so B's early predictions can be unintentionally influenced. |
| B | False (accurate) | Correct: resetting or deliberately initializing state at independent sequence boundaries prevents this contamination. |
| C | False (accurate) | Correct: carrying state across a boundary is appropriate only when the continuity is a meaningful part of the intended problem, not an implementation accident. |
| D | True (incorrect) | Wrong: recurrent predictions explicitly depend on state — they are *not* stateless at inference unless the architecture or invocation resets it. |
| E | True (incorrect) | Wrong: a shared feature schema does *not* erase values carried in the hidden state, so identical features do not make contamination impossible. |

**Reference:** ISLP ch.10 §10.5 (recurrent state and sequence boundaries); conceptual stateful-inference handling.

### [ML2-D10G4Q1] Self-attention over distant positions
**Scenario:** A transformer processes 60 daily observations; for the final-position prediction, self-attention assigns different weights to earlier positions, including one near the window's start.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Attention can create a *direct* interaction between the final position and a distant earlier position (no step-by-step traversal needed). |
| B | True | Attention weights are learned functions of the current representations (query–key compatibility), not fixed solely by calendar distance. |
| C | False | Self-attention does *not* require strictly one-at-a-time processing like a basic RNN — computations across positions can be parallelized. |
| D | True | A large attention weight identifies an association the model uses, but does not by itself prove economic causality. |
| E | False | Attention does *not* guarantee irrelevant observations receive exactly zero weight — soft attention commonly assigns small nonzero weights. |

**Reference:** ISLP ch.10 (sequence models; attention over positions, conceptual); contrast with recurrent processing in §10.5.

### [ML2-D10G4Q2] Positional encoding and order
**Scenario:** A team strips every positional encoding from a transformer and feeds only daily feature embeddings, expecting it to tell "loss followed by gain" from "gain followed by loss."
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Self-attention without positional information is permutation-equivariant and has no intrinsic sense of which embedding came first. |
| B | True | Positional encodings (or related mechanisms) associate content with sequence location, helping represent temporal order. |
| C | True | Feature values might incidentally correlate with time, but that is not a reliable, explicit ordering mechanism for arbitrary observations. |
| D | False | Removing positional information does *not* turn the transformer into a recurrent network — it stays attention-based with no recurrent state transitions. |
| E | False | Attention weights alone do *not* guarantee a unique chronological position for otherwise-identical embeddings — identical content needs a position source. |

**Reference:** ISLP ch.10 (sequence representation and the need for order information in attention-based models, conceptual).

### [ML2-D10G4Q3] Attention mask and target leakage
**Scenario:** A transformer forecasts next-day return, but its attention mask accidentally lets day *t* attend to the known day *t+1* return, which is also the target.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the mask permits target leakage from the future — the model is allowed to use the answer it is supposed to forecast. |
| B | False (accurate) | Correct: low training loss under this mask may exaggerate genuine forecasting ability because access to future targets makes the task artificially easy. |
| C | False (accurate) | Correct: a causal mask can restrict each position from attending to prohibited future information, enforcing the intended direction of information flow. |
| D | True (incorrect) | Wrong: transformer attention does *not* remove the need to define what information was available at prediction time — availability timing remains essential. |
| E | True (incorrect) | Wrong: reusing the leaky mask on a historical test set does *not* make it a valid live-forecasting simulation — it measures a non-deployable task. |

**Reference:** ISLP ch.10 (sequence modeling and masking, conceptual); Handbook of AI & Big Data in Investments (look-ahead / leakage in model validation).

### [ML2-D10G5Q1] LLM summary as the sole trade input
**Scenario:** An analyst has an LLM summarize a 100-page annual report, identify risks, and draft a research memo, then considers using the memo as the sole input to an automated trade.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: summarization and drafting are natural language generation tasks for which an LLM can provide genuine assistance. |
| B | False (accurate) | Correct: grounding in the report reduces some risk but does not guarantee complete or faithful output — the memo may omit qualifications or misstate details. |
| C | False (accurate) | Correct: producing a fluent summary is distinct from demonstrating positive expected return after costs — different evaluation objectives. |
| D | True (incorrect) | Wrong: supplying the source does *not* guarantee every generated claim is supported — a model can still misread, omit, or invent details. |
| E | True (incorrect) | Wrong: an LLM's text-generation ability does *not* make quantitative validation unnecessary — a strategy still needs realistic evaluation, cost modeling, and risk controls. |

**Reference:** Handbook of AI & Big Data in Investments (NLP / generative AI for research workflows; separation of text generation from validated investment decisions; responsible-AI controls).

### [ML2-D10G5Q2] Retrieval-augmented generation and citations
**Scenario:** A research system retrieves filings and earnings-call transcripts before an LLM answers a question, displaying citations beside the generated answer.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Retrieval can provide current, task-specific evidence not reliably encoded in the model's parameters. |
| B | True | Citations help a reviewer trace claims back to candidate source passages (traceability). |
| C | False | RAG does *not* guarantee the cited source entails every sentence — the model may misinterpret evidence or attach an irrelevant citation. |
| D | True | Retrieval quality affects the evidence available to the generator — poor or missing material constrains the grounded answer. |
| E | False | A citation should *not* be treated as proof of correctness without opening and checking the cited passage. |

**Reference:** Handbook of AI & Big Data in Investments (retrieval-augmented generation, grounding, and the need for human verification of sources).

### [ML2-D10G5Q3] Valid labels are not predictive value
**Scenario:** A team prompts an LLM with market commentary to output "BUY," "HOLD," or "SELL," then calls it a profitable forecaster because it consistently produces one of the three labels.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Generating a valid label format does *not* demonstrate predictive value — syntactic compliance says nothing about whether labels predict returns. |
| B | True | The system must be evaluated against subsequent outcomes (on data not used to build or tune it) to assess forecasting value. |
| C | True | A next-token prediction objective is not automatically aligned with risk-adjusted trading returns — the training and financial objectives differ. |
| D | False | Consistent formatting does *not* remove the need to measure turnover and transaction costs — economic evaluation must include implementation effects. |
| E | False | Calling an output "BUY" does *not* convert a generative response into evidence of causal market insight or economic usefulness. |

**Reference:** Handbook of AI & Big Data in Investments (evaluating AI-generated signals; objective misalignment of language-model training vs. investment performance).

### [ML2-D10G6Q1] Fluency is not reliability
**Scenario:** A team uses an LLM to summarize earnings calls and draft trade rationales; the CIO suggests removing analyst review because the summaries sound fluent and convincing.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Fluent output can still contain unsupported claims — hallucinations may be presented persuasively. |
| B | True | Human review remains important in high-stakes financial use because decisions require accountability and validation. |
| C | False | Model confidence *cannot* be reliably inferred from how polished the prose sounds — writing quality is not a confidence measure. |
| D | True | Source verification can reduce the risk of acting on hallucinated information by checking claims against source material. |
| E | True | Generative models should not be assumed to distinguish fact from plausible completion without verification — output may be plausible yet false. |

**Reference:** Handbook of AI & Big Data in Investments (hallucination risk, human oversight, and verification controls for generative AI in finance).

### [ML2-D10G6Q2] Materially wrong figure with a real citation
**Scenario:** An LLM report states a company reduced debt by 40% and cites its latest filing; the filing actually reports 14%. Users approve reports quickly because most prior summaries were acceptable.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the numerical discrepancy is a material verification failure — a real source reference does not excuse a materially incorrect value. |
| B | True (incorrect) | Wrong: sampling a few outputs during development is *not* sufficient to guarantee all future numerical claims — finite testing cannot cover every new input/output. |
| C | False (accurate) | Correct: automated extraction checks can assist reviewers but do not remove accountability for the final decision. |
| D | False (accurate) | Correct: a workflow can require reviewers to compare consequential figures with the cited source before release (risk-based review). |
| E | True (incorrect) | Wrong: a history of acceptable summaries does *not* make the current 40% claim reliable without inspection — past performance does not validate this specific assertion. |

**Reference:** Handbook of AI & Big Data in Investments (verification of consequential outputs, model risk, and reviewer accountability).

### [ML2-D10G6Q3] Autonomous order agent with only a dollar limit
**Scenario:** A firm deploys an autonomous agent that reads news, proposes trades, and sends orders without approval; it has a daily dollar limit but no source-quality rules, anomaly alerts, or human stop mechanism.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A dollar limit constrains one exposure dimension but does not address all failure modes (misinformation, correlated actions, operational failures). |
| B | True | Source-quality checks could reduce the chance that unreliable content triggers an order. |
| C | True | Escalation and intervention mechanisms are appropriate when inputs or proposed actions are anomalous (outside expected operation). |
| D | False | Autonomy does *not* make assigning a human owner for monitoring and outcomes unnecessary — it increases the importance of clear accountability. |
| E | False | A daily limit does *not* guarantee each executed trade has a sound factual basis — position constraints do not verify claims or reasoning. |

**Reference:** Handbook of AI & Big Data in Investments (governance of autonomous/agentic systems; layered controls, escalation, and accountability).

### [ML2-D10G7Q1] Aggregate accuracy versus subgroup fairness
**Scenario:** A credit-risk model was trained mostly on applicants from a period and region with limited demographic representation; aggregate validation accuracy is strong, but subgroup performance was not examined.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Strong aggregate accuracy can coexist with materially different error rates across subgroups — majority performance can dominate the average. |
| B | True | Historical data can encode past selection practices and structural inequities (it reflects the systems through which it was collected). |
| C | True | Subgroup (disaggregated) evaluation can reveal harms that a single aggregate metric hides. |
| D | False | Removing explicitly protected attributes does *not* guarantee no correlated feature reproduces unequal outcomes — proxy variables retain the information. |
| E | False | High overall accuracy alone does *not* prove the model is fair for every group — performance and fairness need separate, context-sensitive examination. |

**Reference:** Isbell/Littman ML4T keynote on algorithmic bias (how historical data and proxies encode bias); Handbook of AI & Big Data in Investments (subgroup/fairness evaluation, responsible AI).

### [ML2-D10G7Q2] Unstable feature-attribution explanations
**Scenario:** A PM asks why a complex model rejected a trade; the system returns a feature-attribution chart (volatility and sentiment dominant) that varies noticeably under small, economically irrelevant input perturbations.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: feature attribution can help a reviewer investigate a particular prediction by identifying inputs the method associates with the output. |
| B | False (accurate) | Correct: instability under small perturbations is relevant when assessing explanation reliability — an explanation that changes arbitrarily may not support dependable review. |
| C | False (accurate) | Correct: an explanation method can be useful without making the underlying model causal or fully transparent (post-hoc aid with limitations). |
| D | True (incorrect) | Wrong: the chart does *not* prove that changing sentiment will *cause* the outcome to change by the attributed amount — predictive attribution is not a causal intervention effect. |
| E | True (incorrect) | Wrong: providing any chart does *not* satisfy all explainability and governance obligations — explanations must be evaluated for suitability, faithfulness, stability, and audience. |

**Reference:** Isbell/Littman ML4T keynote on algorithmic bias (interpretability caveats); Handbook of AI & Big Data in Investments (explainability, attribution limits, and governance obligations).

### [ML2-D10G7Q3] Deploy-and-forget without monitoring
**Scenario:** A firm approves an AI investment tool after one backtest and leaves it unchanged in production, with no one assigned to monitor input drift, performance, incidents, model versions, or overrides.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: responsible deployment includes ongoing monitoring because data and behavior can change after approval, even without a code change. |
| B | False (accurate) | Correct: version records help investigators reconstruct which model and configuration produced a decision (traceability for audits and rollback). |
| C | False (accurate) | Correct: defined thresholds and escalation procedures convert monitoring results into accountable action (who responds and what happens). |
| D | True (incorrect) | Wrong: a successful historical backtest does *not* permanently establish safety and suitability — a backtest is limited evidence and cannot cover all future regimes. |
| E | True (incorrect) | Wrong: monitoring is *not* unnecessary just because source code is unchanged — input drift, external change, and degraded outcomes arise while code stays fixed. |

**Reference:** Handbook of AI & Big Data in Investments (model risk management, monitoring, versioning, and governance as design elements); Isbell/Littman ML4T keynote (ongoing responsibility for deployed models).
