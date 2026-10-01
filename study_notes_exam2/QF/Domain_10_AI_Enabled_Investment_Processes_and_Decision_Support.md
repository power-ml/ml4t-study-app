# QF Domain 10 — AI-Enabled Investment Processes & Decision Support

## Domain cheat-sheet

- **AI spans the whole investment workflow — evaluate each stage on its own terms.** A single platform may touch *research* (summarizing filings, extracting signals), *portfolio construction* (forecasting returns, suggesting weights), *execution* (routing/sizing orders), and *monitoring/communication* (client reports, risk dashboards). Each stage has different objectives, failure modes, and risks, so **skill at one stage does not establish readiness of the whole pipeline**. Research-stage success (e.g., good summaries) does **not** imply forecast skill, portfolio-risk control, execution quality, or communication accuracy — these require **separate tests**. When one stage's output becomes the next stage's input, **errors propagate**, so the *interfaces* between stages must be monitored, not just the endpoints.
- **Predictive skill is necessary but not sufficient.** A forecast with genuine skill can still produce poor **net** performance if portfolio construction concentrates in illiquid names or execution trades too urgently. Realized return = gross alpha − implementation cost (constraints, sizing, turnover, impact). *Example:* 6% gross alpha − 8% cost/impact ≈ **−2%** net. Accurate forecasts do **not** remove liquidity, capacity, or turnover constraints, and monitoring **only** forecast accuracy misses the construction/execution causes of bad realized results. Slower/smaller execution can cut impact but adds **timing (opportunity) risk** — a genuine tradeoff.
- **Decision support ≠ autonomous decision-making; autonomy is a dial, not a switch.** AI can add value by improving *analysis* while a human retains *final authority*. The appropriate level of autonomy should scale with the **consequences of error, reversibility, novelty, and decision scope** — routine, tightly bounded actions (small index-tracking rebalances within tracking-error limits) can be automated, while leverage, new asset classes, or unusually large trades route to **human approval/escalation**. "Autonomy must be all-or-nothing" is false — **partial autonomy** (automated routine + human-controlled exceptions) is coherent and common. Strong backtests do **not** justify full autonomy (live deployment adds model, data, implementation, operational risk) and automation does **not** eliminate model risk — it can **transmit or amplify** it. Even bounded automation needs monitoring, and **kill switches / safe fallbacks** (pause or shrink trading) are valuable even at the cost of continuity, especially under **out-of-distribution (OOD)** stress where high model confidence can be **confidently wrong** and conflicting data feeds are a reasonable trigger to pause/escalate.
- **Human + AI is complementary, and neither side is infallible.** Machines provide **scale/breadth** (screen thousands of securities); humans provide **context and exception judgment** (institutional knowledge, accounting nuance, regime awareness). A documented **override** — recording reason, evidence, decision-maker, and time — improves the decision *and* preserves accountability. Disagreement should trigger **structured challenge of both** the model and the human, not blind deference to either. Human involvement does **not** guarantee correctness (humans carry bias/error), and screening more names raises *opportunity count* but does **not** guarantee a higher information coefficient. Evaluate the **joint** system (interactions, selection rules, implementation), not either component alone. Beware **mechanical deference** (auto-approving any confidence score > threshold) — that disguises automation as oversight; review adds little if reviewers merely re-apply the model's own rule.
- **Knowledge graphs & symbolic representation organize relationships; they do not prove impact.** Representing **entities as nodes** and **relationships as edges** supports **multi-hop/multi-step queries** (link a supplier shutdown through supply edges to public holdings not named in the article; link a shared director to two firms). Graph structure supplies **candidate/structured context**, not guaranteed causal or predictive conclusions: a connection does **not** imply **equal materiality** — direction, substitutes, inventory, contract terms, each firm's circumstances differ. Conclusions depend on **relationship accuracy and currency** (stale/incorrect edges → misleading exposure maps). Richer rules can weight edges by **relationship type, recency, and materiality** rather than treating every edge equally, and combining graph context with **statistical evidence** is more informative than the relationship alone.
- **Symbolic rules vs. statistical/ML models — different roles, used together.** In a compliance-aware system a **statistical forecast** estimates *attractiveness* while **symbolic rules** encode *constraints and required actions* (no restricted issuers, sector-exposure limits, escalate ambiguous issuers). A governance restriction is **not** a weak return forecast, so a strong forecast must **not** auto-override a restricted-list rule. **Explicit rules are easier to inspect** than constraints learned implicitly from examples (even if the full system stays complex). Rules only cover the risks their designers **identified and encoded** — they do **not** guarantee all risks are represented. **Entity resolution** matters: ambiguous name/issuer/instrument linking can apply a rule to the wrong security or skip it entirely.
- **Integrating structured + unstructured data: alignment, vintage, and provenance are everything.** Combining prices/fundamentals (structured) with text (filings, calls, news) and alt-data (satellite, etc.) can add information **even when the numeric fields are already correct** — complementary sources are not redundant just because they share an issuer. But correct structured data do **not** neutralize errors in unstructured inputs: misaligned transcript dates create **false language→return relationships** and can **leak** future information, producing misleadingly good backtests. Required controls: **timestamp and entity-alignment checks** before training; **point-in-time / information-vintage** discipline (vendor revisions and restated histories cause **look-ahead bias**); awareness of **coverage/measurement bias** (e.g., suburban-skewed satellite coverage) and **non-random missingness** (weather is persistent/regional, not random w.r.t. activity). Novel sources **increase**, not remove, the need for provenance/quality controls (collection, transformations, rights, revisions). Conflicting sources should be **analyzed by provenance/purpose/timing**, not mechanically averaged; cross-source comparison can expose narrative-vs-financials tension; evasive management answers may be informative but remain **noisy/uncertain**.
- **Explainability, governance, and oversight.** A **plausible narrative is not a faithful explanation** — a coherent story (leverage rose, liquidity weakened) can be a **post-hoc** rationalization while the model actually keyed on an unidentified feature. Post-hoc explanations must be validated for **fidelity**, not just readability; misleading explanations cause reviewers to approve decisions for reasons the model **didn't use**, and hidden drivers can conceal **instability, leakage, bias**. Explainability **supports oversight but does not prove the recommendation is correct** (interpretability ≠ predictive validity). **Model-change governance:** a material update warrants **fresh review** even if one metric (e.g., validation Sharpe) improves — review data, assumptions, controls, intended use, and failure modes; a higher Sharpe does **not** guarantee lower operational/model risk. Keep **versioned records** (reconstruct which model made a decision) and **monitor continuously** — drift/limit breaches/data failures can appear **before** aggregate returns go negative. A **profitable override outcome does not prove a sound process**; outcome quality ≠ process quality, and accountability requires clear decision rights plus contemporaneous records.
- **Operational, model, and systemic risk.** *Operational:* a **stale feed** that is correctly *formatted* can still be economically wrong — **schema validation alone won't catch it**; need **freshness checks and cross-feed comparison**, plus a fallback that reduces/pauses trading. Correctly functioning code can still produce harmful decisions when **production inputs fail**, so this *is* operational/model risk; monitoring must cover **upstream data dependencies**, not just model output. *Model drift:* the input→return relationship can change **even with unchanged code** — disclosure-language shifts alter text-feature meaning/distribution, and wider adoption of similar signals **erodes alpha via crowding**; drift is about **changing data/relationships, not just software bugs**, detectable by monitoring predictive performance *and* input distributions. *Systemic:* when many funds share models, data vendors, and risk triggers, individually reasonable risk reductions can become **correlated/synchronized selling** that amplifies market stress — common dependencies create correlation **without explicit coordination**, independent legal ownership does **not** guarantee independent behavior, simultaneous exits invalidate **normal-condition cost assumptions**, and diversifying across many securities does **not** eliminate systemic risk from shared signals/vendors/controls.

## Common traps

- **Inverted-polarity questions (10 of 21 here).** When the body says *"each item asserts that its quoted statement is incorrect,"* the Answer Key verdict is flipped relative to the statement's truth: **True = the quoted statement is wrong (incorrect); False = the quoted statement is accurate (correct).** Read the polarity line *first*. Inverted here: **G1Q1, G2Q1, G3Q3, G4Q2, G4Q3, G5Q1, G5Q2, G6Q1, G6Q2, G7Q2.** The remaining 11 are Normal (True = accurate).
- **"Stage success ⇒ pipeline ready."** False — good summaries don't imply forecast skill, forecast skill doesn't imply good construction/execution, and interfaces between stages must be monitored because errors propagate.
- **"Accurate forecast ⇒ profitable strategy / drop constraints."** False — net return subtracts implementation cost; liquidity/capacity/turnover constraints stay; monitoring only accuracy misses construction/execution failures. Gross 6% − cost 8% ≈ **−2%**.
- **"Backtest beat benchmark ⇒ full autonomy / no model risk."** False — live deployment adds model/data/implementation/operational risk; automation transmits and amplifies model error rather than eliminating it.
- **"Autonomy is all-or-nothing."** False — autonomy is calibrated to consequence, reversibility, novelty, and scope; routine automation + human exception handling is coherent (partial autonomy).
- **"High confidence ⇒ familiar/OOD-safe / humans shouldn't intervene in stress."** False — models can be confidently wrong out of distribution; conflicting feeds and stress are exactly when escalation/kill-switches matter.
- **"Human involvement guarantees correctness" / "override that made money ⇒ good process."** Both false — humans have bias/error; outcome quality ≠ process quality; document reason, evidence, owner, time.
- **"A graph edge establishes equal materiality / identical signals."** False — connections justify *investigation*, not equal economic impact; weight edges by type, recency, materiality, and combine with statistical evidence.
- **"A strong forecast should override a restricted-list rule."** False — governance restrictions aren't weak forecasts; symbolic constraints and statistical attractiveness play different roles; rules cover only encoded risks.
- **"Correct numeric data neutralizes bad text / more data can't help when prices are right."** False — misaligned/leaked text creates false relationships and inflated backtests; complementary sources add information and need alignment, vintage, and provenance checks.
- **"Alt-data is independent of filings ⇒ no provenance needed" / "weather missingness is random."** False — novel data *increases* provenance needs; coverage bias and weather-driven missingness are systematic; vendor revisions cause look-ahead bias; use point-in-time vintages.
- **"Plausible explanation ⇒ faithful explanation."** False — post-hoc narratives can misrepresent true drivers; validate fidelity, not just readability; explainability aids oversight but doesn't prove the recommendation is right.
- **"Prior approval + higher Sharpe ⇒ skip re-review / stop monitoring."** False — material changes warrant fresh governance across data/assumptions/controls/use/failure modes; keep versioned records; drift and failures surface before negative returns.
- **"Model drift = software bugs only / unchanged code ⇒ no drift."** False — relationships and data-generating processes evolve around a fixed model; disclosure shifts and crowding erode signals; monitor performance *and* input distributions.
- **"Correctly formatted feed ⇒ not operational risk."** False — stale-but-valid values are economically wrong; schema checks miss it; need freshness/cross-feed checks and controlled degradation.
- **"Independent ownership / broad diversification ⇒ no systemic risk."** False — shared models/vendors/triggers create correlated, synchronized action without coordination; simultaneous exits break normal-market cost assumptions; shared factors persist across broad books.

## Questions

### [QF2-D10G1Q1] One AI platform across the workflow — stage-appropriate readiness
**Scenario:** An asset manager proposes one AI platform to summarize filings, forecast returns, suggest weights, route orders, and draft client reports; the CIO asks whether research-stage success proves the whole workflow is production-ready.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: each stage (research, forecasting, construction, execution, communication) should be evaluated against its own objectives and risks — the claim is correct, so the inverted verdict is False. |
| B | True (incorrect) | Wrong: accurate filing *summaries* do not guarantee accurate *return forecasts* — summarization performance does not establish predictive skill; these are distinct capabilities. |
| C | False (accurate) | Correct: a useful forecast can still produce poor net performance when construction or execution is flawed — constraints, sizing, turnover, and trading costs shape realized results. |
| D | False (accurate) | Correct: client-facing output can require different controls than internal research notes — external communication raises distinct accuracy, disclosure, and reputational concerns. |
| E | True (incorrect) | Wrong: one platform does not remove the need to monitor interfaces — errors propagate when one stage's output becomes another's input, so interfaces require monitoring. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.10 (AI across the investment process; stage-specific evaluation) and ch.11 (model governance and monitoring across the pipeline); Balch ML4T week-13/14 readings (deploying ML in the trading workflow; separating prediction skill from realized performance).

### [QF2-D10G1Q2] Predictive skill vs. net performance — construction and execution
**Scenario:** An AI forecast predicts relative returns well, but the optimizer concentrates in illiquid names and execution trades urgently; gross backtest alpha is 6%/yr while estimated costs/impact are 8%.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Predictive skill alone is not an investable strategy — portfolio construction and execution determine whether forecast value is actually captured. |
| B | True | Under the stated estimates, net ≈ 6% gross alpha − 8% implementation cost ≈ −2% before other effects. |
| C | False | Accurate forecasts do not remove liquidity or capacity constraints — dropping them to chase illiquid names worsens realized results. |
| D | True | Slower/smaller execution can lower market impact but adds timing (price-movement) risk before completion — a real tradeoff, not a free improvement. |
| E | False | Monitoring only forecast accuracy would miss concentration, liquidity, turnover, and execution-quality causes of poor realized performance. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.10 (portfolio construction and execution; implementation shortfall and capacity); Balch ML4T week-13/14 readings (transaction costs, market impact, and the gap between gross and net performance).

### [QF2-D10G1Q3] AI-drafted client explanations — faithful rationale vs. correct trade list
**Scenario:** A wealth manager uses AI to draft plain-language explanations of portfolio changes; the system gets approved trades and risk data but occasionally invents reasons not part of the committee's decision.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A factually correct list of trades does not guarantee a faithful explanation of *why* they occurred — transaction accuracy and rationale accuracy are separate requirements. |
| B | False | The system should not be free to infer any plausible rationale just because trades were approved — a plausible but unsupported reason can misrepresent the decision process. |
| C | True | Grounding explanations in approved decision records reduces unsupported claims — the records provide evidence to check generated text against. |
| D | True | Human review is especially appropriate before high-impact client communications — errors create client, compliance, and reputational consequences. |
| E | False | Communication quality is not unrelated to governance — client communications are part of the investment workflow and require accountability even though they don't place trades. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.11 (governance of AI-generated communications; grounding and human review) and ch.8 (faithfulness of generated text to source evidence); Balch ML4T week-13/14 readings (responsible deployment of ML outputs).

### [QF2-D10G2Q1] Full autonomy from a backtest — decision support vs. automation
**Scenario:** An AI recommends trades; the CIO proposes executing every recommendation automatically because the backtest beat the benchmark.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: strong backtest performance alone does not justify full autonomy — live deployment adds model, data, implementation, and operational risks one backtest does not resolve. |
| B | False (accurate) | Correct: human approval and escalation rules are appropriate controls — they limit the effect of questionable recommendations. |
| C | True (incorrect) | Wrong: autonomous execution does not eliminate model risk — automation can transmit or amplify model errors rather than remove them. |
| D | False (accurate) | Correct: acceptable autonomy should depend on the consequences of error — higher-impact or less reversible actions warrant stronger controls. |
| E | False (accurate) | Correct: decision-support systems can add value without making the final decision — AI improves analysis while a human retains decision authority. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.11 (decision support vs. automation; autonomy calibrated to consequence/reversibility; approval and escalation controls); Balch ML4T week-13/14 readings (backtest overfitting; risks of live automated trading).

### [QF2-D10G2Q2] Graduated autonomy — bounded automation with human escalation
**Scenario:** A pension fund lets AI rebalance small index-tracking positions within tight limits but requires committee approval for leverage, new asset classes, or unusually large trades; a risk officer argues autonomy must be all-or-nothing.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The fund can rationally use different autonomy levels for different decisions — autonomy is calibrated to risk, novelty, reversibility, and scope. |
| B | True | Predefined position and tracking-error limits can bound automated actions, restricting what the system may do without approval. |
| C | True | Requiring approval for novel or high-impact decisions is escalation — routing out-of-routine decisions to human governance. |
| D | False | Partial autonomy is not logically inconsistent — workflows routinely combine automated routine actions with human-controlled exceptions. |
| E | True | Even tightly bounded automation needs monitoring — boundaries do not prevent bad inputs, software faults, or execution problems. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.11 (tiered autonomy, limits, and escalation; monitoring bounded automation); Balch ML4T week-13/14 readings (operational guardrails in deployed strategies).

### [QF2-D10G2Q3] Out-of-distribution stress — confidence, conflicting feeds, kill switches
**Scenario:** During a market disruption an autonomous strategy sees prices far outside its training range; its confidence score stays high but several market-data feeds disagree, and the desk must decide whether to keep trading.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | High model confidence does not necessarily mean conditions are familiar — models can be confidently wrong, especially outside their training distribution. |
| B | True | Conflicting feeds are a reasonable trigger to pause or escalate — input disagreement undermines the reliability of downstream decisions. |
| C | True | Out-of-distribution conditions make historical validation less informative — evidence from familiar regimes may not transfer. |
| D | True | A kill switch or safe fallback can be valuable even if it reduces trading continuity — limiting loss from uncontrolled behavior can outweigh temporary inactivity. |
| E | False | Having authority in ordinary markets does not mean humans should never intervene in stress — stress is a central reason to define intervention/escalation mechanisms. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.11 (OOD risk, confidence calibration, fail-safes and escalation under stress); Balch ML4T week-13/14 readings (regime change and the limits of historical validation).

### [QF2-D10G3Q1] Analyst override of a model flag — missing context
**Scenario:** An AI flags a manufacturer as attractive on improving margins and positive report language; an analyst knows a temporary accounting change inflated reported margins and asks to override.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The analyst's domain knowledge may identify context omitted from the model's inputs — relevant institutional/accounting context may not be encoded in the data. |
| B | False | The model's quantitative consistency does not mean the accounting change can't matter — consistent processing cannot compensate for missing or misleading inputs. |
| C | True | A documented override can improve the decision while preserving accountability — recording evidence and authority supports learning and review. |
| D | True | The disagreement should prompt investigating both sides — either the model or the analyst may be mistaken, so structured challenge beats blind acceptance. |
| E | False | Human involvement does not guarantee a correct final decision — human judgment also contains biases and errors. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.11 (human-in-the-loop oversight; documented overrides and accountability); Balch ML4T week-13/14 readings (combining human judgment with model signals).

### [QF2-D10G3Q2] Unaided analysts vs. AI-screen-then-human-review — complementary strengths
**Scenario:** Team A has analysts forecast unaided; Team B uses AI to screen thousands of securities, then has analysts investigate the most promising and most anomalous cases before approval.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Team B uses AI scalability and human contextual judgment as complementary strengths — machines process breadth while people investigate context and exceptions. |
| B | False | Screening more securities does not guarantee a higher information coefficient — more coverage increases opportunity count but not forecast skill. |
| C | True | Reviewing anomalous cases can reveal data errors or regime changes — anomalies may reflect bad data, unusual events, or shifting relationships. |
| D | False | Analyst review is not valuable only when it agrees with the AI — well-supported disagreement is a key source of human value. |
| E | True | The combined process should be evaluated as a whole — interactions, selection rules, and implementation shape the joint system's output. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.10 (AI-augmented research; breadth-vs-depth division of labor) and ch.11 (evaluating human+AI systems jointly); Balch ML4T week-13/14 readings (information coefficient; breadth vs. skill).

### [QF2-D10G3Q3] Mechanical confidence-threshold approvals — miscalibration
**Scenario:** A committee auto-approves AI recommendations with confidence > 90% without examining assumptions; a 92%-score trade is later found to come from a model poorly calibrated in volatile markets.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a confidence score should be interpreted per how it was defined and calibrated — its meaning depends on the model target and empirical calibration. |
| B | True (incorrect) | Wrong: a 92% score does not necessarily mean a 92% probability of profit — the score may represent something else and may not be a calibrated probability. |
| C | False (accurate) | Correct: a fixed approval threshold can create blind reliance when market context is ignored — mechanical deference disguises automation as human oversight. |
| D | False (accurate) | Correct: human review adds little if reviewers merely repeat the model's decision rule — effective review needs independent scrutiny or additional information. |
| E | False (accurate) | Correct: calibration should be monitored across relevant regimes, not just the full-sample average — aggregate calibration can conceal regime-specific errors. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.11 (probability calibration, threshold governance, and meaningful human review); Balch ML4T week-13/14 readings (interpreting model confidence; regime-dependent performance).

### [QF2-D10G4Q1] Supply-chain knowledge graph — tracing indirect exposure
**Scenario:** A fund builds a knowledge graph linking companies to subsidiaries, executives, suppliers, commodities, and securities; a news model reports a factory shutdown at a private supplier and the team wants affected public holdings.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The supplier relationship can connect the news event to securities not named in the article — graph paths link an event entity through supply edges to public firms. |
| B | True | Representing entities separately from relationships supports multi-step queries — structured nodes and edges enable reasoning across relationship types. |
| C | False | Not every connected company must experience the same impact — direction, materiality, substitutes, inventory, and contract terms differ. |
| D | True | Stale or incorrect relationship data can produce misleading exposure maps — graph conclusions depend on relationship accuracy and currency. |
| E | True | The graph organizes candidate relationships but does not itself prove an event will affect returns — it supplies structured context, not guaranteed causal/predictive conclusions. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.8 (knowledge graphs; entities, edges, and multi-hop queries over relationships); Balch ML4T week-13/14 readings (alternative-data linkage and the limits of inferred exposure).

### [QF2-D10G4Q2] Statistical forecast plus symbolic compliance rules — different roles
**Scenario:** A compliance-aware system combines a statistical return forecast with symbolic rules: don't buy restricted issuers, keep sector exposure within limits, escalate ambiguous-issuer securities.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: statistical forecasts and symbolic rules can serve different roles — the forecast estimates attractiveness while rules encode constraints and required actions. |
| B | True (incorrect) | Wrong: a strong forecast should not automatically override a restricted-list rule — a governance restriction is not merely a weaker return forecast. |
| C | False (accurate) | Correct: explicit rules can be easier to inspect than constraints learned implicitly from examples — rule logic can often be traced directly even if the full system stays complex. |
| D | False (accurate) | Correct: ambiguous entity resolution can cause a rule to hit the wrong security or not apply — correctly linking names, issuers, and instruments is necessary for reliable rules. |
| E | True (incorrect) | Wrong: symbolic rules do not guarantee all risks are represented — rules cover only the risks and relationships designers identify and encode. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.8 (symbolic vs. statistical/ML representation; rule inspectability and entity resolution) and ch.11 (encoding compliance constraints; coverage limits of rule sets); Balch ML4T week-13/14 readings (combining learned models with hard constraints).

### [QF2-D10G4Q3] Shared-director edge — connection vs. equal materiality
**Scenario:** A knowledge graph records that Director Lee sits on the boards of Company A and Company B; a model infers that news about Lee should always generate identical trading signals for both.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the shared-director relationship is represented as a connection among distinct entities — one person entity linked by board-membership edges to two company entities. |
| B | False (accurate) | Correct: the connection may justify further research into whether the event affects both companies — the link is a reason to investigate exposure. |
| C | True (incorrect) | Wrong: the graph relationship alone does not establish equal economic materiality — the person's role, the event, and each firm's circumstances determine relevance. |
| D | False (accurate) | Correct: rules can incorporate relationship type, recency, and materiality rather than treating every edge equally — richer symbolic logic distinguishes relationships. |
| E | False (accurate) | Correct: combining graph context with statistical evidence can be more informative than the relationship alone — statistics help estimate whether a structured link has predictive importance. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.8 (edge semantics; weighting relationships by type/recency/materiality; graph context combined with statistical evidence); Balch ML4T week-13/14 readings (avoiding naive inference from relationship data).

### [QF2-D10G5Q1] Misaligned transcript dates — unstructured-data integrity and leakage
**Scenario:** A model combines daily prices and fundamentals with earnings-call text; the text pipeline attaches several transcripts to the wrong fiscal quarter while the numerical data stay correct.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Wrong: integrating more data types *can* improve the model even when prices are accurate — complementary text may add information beyond correct numeric fields. |
| B | False (accurate) | Correct: misaligned transcript dates can create false relationships between language and later returns — incorrect timing associates text with outcomes it could not properly predict. |
| C | False (accurate) | Correct: correct structured data do not neutralize errors in unstructured inputs — faulty text features can still distort estimates and decisions. |
| D | False (accurate) | Correct: timestamp and entity-alignment checks are important before training — inputs must be linked to the correct company, event, and information-availability time. |
| E | False (accurate) | Correct: a model may exploit corrupted alignment and still look successful in an improperly designed backtest — leakage/misalignment creates misleading historical performance. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.8 (structured + unstructured integration; timestamp/entity alignment and leakage); Balch ML4T week-13/14 readings (look-ahead bias and backtest integrity).

### [QF2-D10G5Q2] Satellite parking-lot alt-data — coverage bias, missingness, revisions
**Scenario:** A fund evaluates satellite parking-lot counts as a retail-sales signal; coverage is strongest in suburbs, cloud cover creates missing observations, and the vendor revised its historical series.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: geographic coverage bias may make the signal represent some retailers better than others — uneven coverage creates systematic measurement differences across firms. |
| B | True (incorrect) | Wrong: weather-driven missingness is not guaranteed random w.r.t. economic conditions — weather patterns can be persistent, regional, and related to observed activity. |
| C | False (accurate) | Correct: vendor revisions can make today's data differ from what was available historically — restated history introduces look-ahead bias if treated as contemporaneously known. |
| D | False (accurate) | Correct: a valid backtest should preserve the information vintages observable at each decision time — point-in-time data are essential for an implementable test. |
| E | True (incorrect) | Wrong: alternative data do not remove the need for provenance and quality controls — novel sources increase the need to understand collection, transformations, rights, and revisions. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.8 (alternative data; coverage/measurement bias, missingness, provenance) and ch.11 (point-in-time discipline and data governance); Balch ML4T week-13/14 readings (survivorship/look-ahead bias; vendor data revisions).

### [QF2-D10G5Q3] Conflicting disclosures — weighting evidence by provenance
**Scenario:** An AI reads a company's press release, regulatory filing, and earnings-call transcript; the release is optimistic, the filing shows weakening cash flow, and management dodges a question about customer losses.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Conflicting sources should not necessarily be averaged into a neutral signal — mechanical averaging can erase meaningful distinctions that should be analyzed. |
| B | True | Source type and provenance affect weighting — documents differ in purpose, controls, timing, and reliability. |
| C | True | Avoiding a question may be informative, but its interpretation stays uncertain — evasion is a possible signal amid noisy language. |
| D | True | Combining text with structured cash-flow data can reveal inconsistency either source alone might miss — cross-source comparison exposes narrative-vs-financials tension. |
| E | False | The three sources are not redundant just because they concern one company — different sources can carry complementary information. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.8 (multi-source text analysis; weighting by provenance; cross-source consistency); Balch ML4T week-13/14 readings (sentiment/NLP signals and their reliability).

### [QF2-D10G6Q1] Post-hoc explanation vs. actual driver — faithfulness
**Scenario:** A credit model recommends selling a bond, citing rising leverage and weakening liquidity; the committee later learns the model mostly relied on an unidentified text feature and the explanation was generated after the recommendation.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a plausible narrative is not necessarily a faithful explanation — it can sound reasonable without reflecting the model's actual drivers. |
| B | False (accurate) | Correct: post-hoc explanations should be validated for fidelity as well as readability — useful explanations communicate real model behavior, not just a coherent story. |
| C | True (incorrect) | Wrong: a persuasive narrative does not make the actually-used feature irrelevant — hidden decision drivers may reveal instability, leakage, bias, or unintended behavior. |
| D | False (accurate) | Correct: misleading explanations can cause reviewers to approve decisions for reasons the model did not use — reviewers can't challenge reasoning that is misrepresented. |
| E | False (accurate) | Correct: explainability can support oversight without proving the recommendation is correct — interpretability assists evaluation but doesn't establish predictive validity. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.11 (explainability and model governance; faithfulness vs. plausibility of explanations); Balch ML4T week-13/14 readings (interpretability and its limits in deployed models).

### [QF2-D10G6Q2] Material model update — fresh governance review
**Scenario:** A firm is about to deploy a material model update; the developer argues approval is unnecessary because the prior model was approved and the new version has a higher validation Sharpe.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a material model change can warrant fresh review even when one metric improves — a new version may alter behavior, dependencies, and risks. |
| B | False (accurate) | Correct: approval should weigh data, assumptions, controls, intended use, and failure modes beyond historical performance — governance evaluates fitness and controls, not one metric. |
| C | True (incorrect) | Wrong: a higher validation Sharpe does not guarantee lower operational and model risk — risk can rise despite improved historical risk-adjusted returns. |
| D | False (accurate) | Correct: versioned records help reconstruct which model produced a decision — version traceability supports investigation, accountability, and reproducibility. |
| E | True (incorrect) | Wrong: approval does not make subsequent monitoring unnecessary until returns go negative — drift, data failures, limit breaches, and unusual behavior can appear first. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.11 (model-change governance, versioning, and ongoing monitoring); Balch ML4T week-13/14 readings (validation metrics do not guarantee live robustness).

### [QF2-D10G6Q3] Undocumented override that worked — process vs. outcome
**Scenario:** A PM overrides an AI recommendation during a liquidity crisis but records neither reason nor evidence; the trade performs well and management concludes the override process is effective.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A profitable outcome alone does not establish the override process was sound — outcome quality and decision-process quality are related but not identical. |
| B | True | Recording reason, evidence, decision maker, and time strengthens the audit trail — contemporaneous records make later evaluation more reliable. |
| C | False | Human overrides should not always be prohibited — overrides can be appropriate when governed, justified, and monitored. |
| D | True | Reviewing override patterns can reveal either model weaknesses or systematic human bias — repeated disagreements are evidence about both components. |
| E | True | Accountability requires clarity about who had authority for the final decision — decision rights must be identifiable for meaningful oversight. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.11 (override governance; audit trails and decision rights; outcome vs. process quality); Balch ML4T week-13/14 readings (process discipline vs. result-driven conclusions).

### [QF2-D10G7Q1] Stale price feed — operational risk despite valid formatting
**Scenario:** A live trading model receives a stale price feed after a vendor outage; the values are correctly formatted, so the system keeps trading on prices that are 20 minutes old.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Schema validation alone may miss the stale-feed problem — correctly formatted values can still be untimely and economically wrong. |
| B | True | Freshness checks and cross-feed comparisons could identify the failure — timestamp and independent-source controls expose stale or inconsistent data. |
| C | False | Functioning code does not mean there is no model/operational risk — reliable code can still produce harmful decisions when production inputs fail. |
| D | True | A fallback that reduces or pauses trading may be safer than continuing on unreliable inputs — controlled degradation limits damage until data recover. |
| E | True | Monitoring should cover upstream data dependencies as well as model output — end-to-end reliability depends on data, infrastructure, model, and execution. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.11 (operational risk; data-dependency monitoring, freshness controls, and fallbacks); Balch ML4T week-13/14 readings (data-feed integrity in live systems).

### [QF2-D10G7Q2] Weakening sentiment signal — model drift without code change
**Scenario:** A sentiment model performed well at training but weakens as companies change disclosure language and investors adopt similar text tools; the research lead argues unchanged software means no drift.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the input-return relationship can change even when code is unchanged — market behavior and data-generating processes evolve around a fixed model. |
| B | False (accurate) | Correct: changes in disclosure practices can alter the meaning or distribution of text features — new conventions break relationships learned from older text. |
| C | False (accurate) | Correct: wider adoption of similar signals can reduce realizable alpha through crowding — competition and shared positioning change a signal's economics. |
| D | True (incorrect) | Wrong: model drift is not only post-deployment programming bugs — drift concerns changing data or relationships, not just software defects. |
| E | False (accurate) | Correct: monitoring predictive performance and input distributions provides evidence of drift — both feature behavior and outcome relationships are relevant diagnostics. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.11 (model drift, crowding, and drift monitoring) and ch.8 (text-feature distribution shift); Balch ML4T week-13/14 readings (alpha decay and signal crowding).

### [QF2-D10G7Q3] Correlated AI strategies — systemic risk from shared models
**Scenario:** Several large funds use similar AI models, data vendors, and risk triggers; after a shock the models recommend selling the same securities and automated execution starts simultaneously across firms.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Individually reasonable risk reductions can collectively intensify market pressure — feedback between common signals, selling, and price declines amplifies stress. |
| B | False | Independent legal ownership does not guarantee independent behavior — similar inputs, objectives, and constraints can generate similar actions. |
| C | True | Common data and model designs can create correlated decisions without explicit coordination — correlation emerges from shared dependencies, not communication. |
| D | True | Simultaneous selling may invalidate normal-condition cost assumptions — liquidity and impact deteriorate when many participants demand the same exit. |
| E | False | Diversifying across many securities does not necessarily eliminate systemic risk — broad portfolios can still share factors, signals, vendors, or synchronized controls. |

**Reference:** *Handbook of AI & Big Data in Investments*, ch.11 (systemic risk from shared models/data/triggers; crowding and synchronized execution); Balch ML4T week-13/14 readings (market-impact feedback and liquidity under stress).

## References (domain-level)

1. **Handbook of AI & Big Data in Investments — ch.8 (data, knowledge representation, and NLP):** knowledge graphs (entities as nodes, relationships as edges, multi-hop queries), symbolic vs. statistical/ML representation and rule inspectability, entity resolution, structured + unstructured integration, text-feature alignment/vintage, alternative-data coverage bias, missingness, and provenance (G4, G5, and text-drift aspects of G7Q2).
2. **Handbook of AI & Big Data in Investments — ch.10 (AI across the investment process):** research, portfolio construction, execution, and monitoring as distinct stages; stage-appropriate evaluation; gross alpha vs. net performance (implementation shortfall, liquidity/capacity/turnover); AI-augmented research and the breadth-vs-skill distinction (G1, G3Q2).
3. **Handbook of AI & Big Data in Investments — ch.11 (governance, oversight, and risk):** decision support vs. automation; autonomy calibrated to consequence/reversibility/novelty; approval and escalation; OOD confidence and fail-safes; human-in-the-loop overrides and audit trails; explainability and faithfulness; model-change governance, versioning, and continuous monitoring; operational, model, and systemic risk including drift, crowding, and correlated execution (G1 interfaces, G2, G3Q1, G3Q3, G6, G7).
4. **Balch — ML4T, Georgia Tech, week-13/14 readings:** deploying ML in the trading workflow; backtest overfitting, data-snooping, look-ahead/survivorship bias and point-in-time data; transaction costs and market impact (gross vs. net); regime change and the limits of historical validation; alpha decay/signal crowding; data-feed integrity in live systems — used to ground the practical trading-ML side of each group.

> **Note on source symbols:** the authoritative slice `slices/QF2_D10.txt` contains "fi"/"fl" ligature glyphs throughout (e.g., "ﬁlings", "forecast"→"ﬂawed", "conﬁdence", "proﬁtable", "speciﬁc", "identiﬁed", "beneﬁt"), plus page/footer artifacts ("Rev:081020261230" and page numbers 740–753). These are OCR/export artifacts, not content; text above is de-ligatured and verdicts are copied verbatim from the Answer Keys.
