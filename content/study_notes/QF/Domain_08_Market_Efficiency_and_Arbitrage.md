# QF Domain 8 — Market Efficiency and Arbitrage

## Domain cheat-sheet

- **Efficient Market Hypothesis (EMH) — three nested forms** defined by *which information set* is already impounded in price:
  - **Weak form**: prices reflect all *past price and volume* data. Implication: purely technical/past-return rules cannot earn *consistent, exploitable* abnormal returns. Motivated by the **random-walk** intuition (price changes are unpredictable from history).
  - **Semi-strong form**: prices reflect all *publicly available* information (financial statements, announcements, filings). Implication: **fundamental analysis on already-public data** should not consistently earn abnormal returns; public news is incorporated *rapidly*.
  - **Strong form**: prices reflect *all* information, **public and private/insider**. Implication: even insiders cannot systematically earn abnormal returns. Rarely holds in practice; insider-trading regulation restricts behavior but does **not** prove the strong form.
  - Each higher form **contains** the lower one (strong ⊃ semi-strong ⊃ weak).
- **What efficiency does NOT claim**: it does not require prices to be *perfectly correct* in an absolute sense, nor instantaneous perfection with no price discovery, nor that prices "can never rise two days in a row." Runs of gains/losses, brief price-discovery windows, and partial reversals are all compatible with efficiency.
- **Testing an inefficiency = "does a reliable, tradeable edge survive beyond chance and costs?"** A profitable *in-sample* backtest can arise from **data snooping / overfitting**; a gross edge that is negative after **transaction costs** is not economically exploitable. Predictability (academically interesting) ≠ profitability (net-of-cost tradeability).
- **Arbitrage & the law of one price (LOOP)**: identical/equivalent state-contingent cash flows must command the *same* price in a frictionless market. A price gap between equivalents is a *theoretical* arbitrage — buy cheap, sell dear, pocket the difference; profit comes from the **contemporaneous discrepancy**, not a directional forecast. Simultaneous execution of both legs limits execution price risk. Repeated arbitrage pushes prices to **convergence**.
  - **Riskless vs. risky arbitrage**: truly identical payoffs ⇒ riskless; only *highly correlated* (not identical) payoffs ⇒ residual (basis) risk remains.
  - **ETF mechanism**: authorized creation/redemption keeps market price near NAV/basket value; but timing, execution, financing, and tracking risks can erase a small apparent spread.
- **Statistical arbitrage & mean reversion**: exploit *temporary* deviations from a historical relationship (pair trading). **z-score = (spread − mean) / std**; a large |z| flags historical unusualness, **not** guaranteed convergence. Short the relatively expensive leg, buy the cheap leg; the spread can narrow with either/both legs moving. Key risk: the **historical relationship breaks** (structural change). Not riskless — carries model, convergence, market, and execution risk.
- **Dollar-neutral ≠ risk-free**: equal long/short notionals limit *net directional dollar* exposure but do **not** eliminate *relative-price* risk; the short can rise more than the long and lose money even when both rise.
- **Event-driven & relative-value strategies**:
  - **Merger arbitrage**: post-announcement target trades below the offer (a *deal spread*) reflecting deal-failure/timing risk — the spread is **not** a guaranteed profit. Annualized return depends on time-to-close.
  - **Relative-value / pairs**: long one asset, short a related one — expresses a *relative* (not absolute/directional) view; equal notionals do **not** equalize differing sensitivities (betas, hedges, leverage); company-specific news and borrow costs still matter.
  - **Earnings events**: returns depend on the surprise *relative to what price already implied*, which can differ from published analyst consensus — beating consensus can still trigger a decline.
- **Limits to arbitrage (why mispricing persists despite informed investors)** — Shleifer/Vishny:
  - **Timing/horizon uncertainty**: a correct long-run valuation can still lose if the position can't be held to convergence.
  - **Funding/margin constraints & leverage**: adverse interim moves trigger margin calls and **forced liquidation** ("the market can stay irrational longer than you can stay solvent").
  - **Noise-trader risk**: other traders push price *further* from value before it corrects.
  - **Short-sale constraints**: high borrow fees, limited availability, and **recall** risk cap how fully negative views get expressed and let overpricing persist.
  - **Crowded trades**: common positioning creates endogenous liquidity/feedback loops — one fund's redemption-driven unwind moves prices against others and cascades.

## Common traps

- **No inverted-logic questions in this domain.** *Every* [QF-D8...] item uses a plain "Answer Key:" (True = accurate, False = inaccurate). There is no "True = incorrect; False = accurate" header here — do not invent one. (Flagged explicitly because sibling domains *do* contain inverted items; this one does not.)
- **Double-negative "embedded claim" / "reverses the correct conclusion" choices are the primary trap.** Many choices are phrased in the negative ("The net profit is *not* $0.30", "the two positions should *not* have the same price", "leverage *cannot* convert…") and are marked **False** because the embedded factual claim is true. Rule: strip the negation, judge the inner statement, then flip. These appear in **G2Q3E, G3Q2B, G4Q1B, G4Q1D, G4Q2A, G4Q3A, G4Q3B, G5Q2E, G6Q1A, G6Q1B, G6Q3C, G6Q3E, G7Q1E, G7Q2A, G7Q2C, G7Q3C.**
- **"Guaranteed / cannot lose / riskless" absolutes are almost always False** in stat-arb, merger-arb, and dollar-neutral contexts (G5Q1D, G5Q2D/E, G6Q1C, G4Q3C). A large z-score, an announced deal, or balanced notionals never *guarantee* convergence or eliminate risk.
- **In-sample profit ≠ inefficiency; net-of-cost loss ≠ exploitable edge.** Data snooping (G1Q1C, G5Q3A/B) can manufacture a winning historical rule; a 6% gross edge behind 7% costs is −1% net and not exploitable (G1Q3B/C).
- **Efficiency ≠ perfection.** Choices demanding instantaneous, single-transaction final prices, multi-day mandated drift, or "every investor must read/own the data" are False (G2Q1B, G2Q2B, G2Q3B, G3Q3B). Price discovery, disagreement, and informed-subset trading are all compatible with efficiency.
- **Form confusion**: semi-strong concerns *public* info only and does **not** require *private* (undisclosed) results to be in the price; strong form does (G3Q1C, G3Q2B, G3Q3E). Regulation existing ≠ strong form holding (G3Q1E).

## Questions

### [QF-D8G1Q1] Weak-form efficiency — an in-sample rule does not disprove it
**Scenario:** A researcher finds a rule using only the last five days of prices/volume earned positive returns in a historical sample and concludes weak-form efficiency is disproved.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Weak-form efficiency is precisely about whether *past* price/volume can be used to earn *consistent* abnormal returns; the choice states the hypothesis correctly. |
| B | False | A single profitable in-sample result can be sample-specific, overfit, or uneconomic after costs; it does not by itself establish an *exploitable* inefficiency. |
| C | True | Data snooping — searching many candidate rules — will surface a chance winner in historical data even when no durable predictability exists. |
| D | True | Transaction costs and out-of-sample performance *are* relevant when judging a claimed inefficiency; a usable abnormal return must survive independent testing and realistic implementation costs. |
| E | False | Weak-form efficiency says past data are already impounded; it does **not** imply prices can never rise on two consecutive days — random/weakly predictable returns still produce runs. |

**Reference:** Fama (1970) EMH — weak form; ISLR ch.5 (out-of-sample validation) and data-snooping concept.

### [QF-D8G1Q2] Random-walk model — zero-mean innovation
**Scenario:** A stock closes at $100. Under a simplified random walk, tomorrow's price = today's price plus an unpredictable innovation with expected value zero.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the correct conclusion: with a zero-mean innovation, the *conditional expected* next price equals the current price ($100), so "expected price is not $100" is wrong. |
| B | False | The innovation is uncertain, so the *realized* price need not equal its expectation; the model guarantees nothing about the realized value. |
| C | True | Unexpected news is represented by a large positive or negative innovation, which can move the realized price substantially away from $100. |
| D | False | The random-walk claim is about *unpredictability from currently available information*, not independence from all future information; tomorrow's news can affect tomorrow's price. |
| E | True | A chart can describe the past without conferring profitable predictive power — descriptive patterns ≠ forecastable abnormal returns. |

**Reference:** Random-walk model of prices (Fama 1965); EMH weak form and conditional-expectation intuition.

### [QF-D8G1Q3] Momentum signal — net-of-cost economics
**Scenario:** A momentum signal from past returns earns +6%/yr gross over the benchmark; realistic turnover costs are ~7%/yr.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The pre-cost result is associated with a signal built from past returns, i.e., apparent predictability from historical price data. |
| B | True | Net abnormal return ≈ 6% − 7% = −1%/yr under the stated cost estimate — simple arithmetic. |
| C | False | A strategy that loses money after realistic costs is **not** an economically exploitable violation of weak-form efficiency. |
| D | True | Predictability and net profitability are related but distinct research questions; a signal can be academically interesting yet untradeable. |
| E | False | Reverses the conclusion: reducing turnover/implementation costs *could* let some of the gross edge survive, changing net economics. |

**Reference:** EMH weak form and net-of-cost tradeability; transaction-cost/turnover analysis (Grinold & Kahn, implementation shortfall).

### [QF-D8G2Q1] Semi-strong — rapid incorporation, no mandated drift
**Scenario:** A firm releases unexpectedly strong earnings at 8:30 a.m.; the stock jumps pre-open. A junior analyst claims semi-strong efficiency requires days of continued rising because the news is public.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Semi-strong efficiency is about *rapid* incorporation of public information into price. |
| B | False | A persistent, predictable multi-day drift is **not** required — it would in fact *challenge* the hypothesis. |
| C | False | Reverses the conclusion: under semi-strong efficiency, fundamental analysis on already-public info should **not** consistently earn abnormal returns. |
| D | False | Reverses the conclusion: an immediate pre-market jump is *consistent* with rapid adjustment, not inconsistent with it. |
| E | True | Efficiency concerns information incorporation, not perfect (absolutely correct) valuation. |

**Reference:** Fama EMH — semi-strong form; event-study "speed of adjustment" literature.

### [QF-D8G2Q2] Annual report — competition incorporates public info
**Scenario:** A firm publishes an annual report at noon; at 2 p.m. an analyst values it on the disclosed figures and plans to buy "before others notice."
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A published annual report is publicly available information once released. |
| B | False | Semi-strong efficiency does **not** require every investor to read the report first — prices can adjust via the trades of *informed* participants. |
| C | True | Competing analysts and algorithms can analyze and trade on the disclosure before this one analyst finishes. |
| D | True | Repeatedly earning abnormal *risk-adjusted, net-of-cost* returns from newly public disclosures would be evidence *against* semi-strong efficiency. |
| E | False | The hypothesis targets abnormal returns from *public information*, not compensation for bearing *systematic risk* (which is expected). |

**Reference:** Fama EMH — semi-strong form; competitive price discovery / informed-trading concept.

### [QF-D8G2Q3] Rate announcement — price discovery vs. efficiency
**Scenario:** After an unexpected central-bank rate announcement an index falls 2% in one minute, rebounds 0.4% over ten minutes, then trades in a narrow range.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The large immediate move is consistent with rapid processing of a public surprise. |
| B | False | Efficiency does **not** require the first post-announcement trade to fix the exact final price with no further trading — it doesn't demand instantaneous perfection or eliminate price discovery. |
| C | True | A brief window of price discovery/disagreement can occur even in a relatively efficient market as participants interpret news and liquidity adjusts. |
| D | False | A 0.4% partial rebound does not *prove* the news was initially ignored — it can reflect price discovery, liquidity, or mild overreaction; one observation isn't proof. |
| E | False | Reverses the conclusion: testing efficiency **does** require systematic analysis of whether predictable abnormal returns persist after the announcement and after costs. |

**Reference:** Semi-strong efficiency & price discovery; microstructure of announcement responses.

### [QF-D8G3Q1] Strong-form — private information already reflected?
**Scenario:** A pharma executive privately learns a clinical trial failed pre-announcement and believes strong-form efficiency means it's already in the price.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Strong-form efficiency claims prices reflect *both public and private* information. |
| B | True | If the executive can profit from genuinely private information, that contradicts the strong-form claim (which denies such abnormal profits). |
| C | False | Semi-strong efficiency concerns *public* info only, so it does **not** require an undisclosed trial result to be in the price. |
| D | True | Information can be economically valuable *before* it is legally permissible to trade on it — trading restrictions don't erase informational value. |
| E | False | Insider-trading laws restrict *behavior*; they do not demonstrate that prices already contain all private information (i.e., they don't prove the strong form). |

**Reference:** Fama EMH — strong form; insider-information and regulation distinction.

### [QF-D8G3Q2] Insider purchases — abnormal returns
**Scenario:** A study finds insiders' legally reported purchases are, on average, followed by positive abnormal returns; the purchases become public only after the trades are filed.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The finding may indicate insiders held information not fully reflected in price when they traded (private knowledge / superior context). |
| B | False | Reverses the conclusion: the finding *is* easier to reconcile with semi-strong efficiency (which doesn't require private info in price) than with strong-form efficiency (which does) — so calling them equivalent is wrong. |
| C | True | Once the required filing is released, it becomes public information within the semi-strong information set. |
| D | False | Strong-form efficiency *denies* consistent abnormal profits even to those with private information; it does not predict insiders profit for being "better trained." |
| E | False | An average relationship does not imply *every* individual insider purchase is profitable. |

**Reference:** Fama EMH — strong vs. semi-strong; insider-trading event studies (e.g., Seyhun).

### [QF-D8G3Q3] Alternative data — the public/private gray area
**Scenario:** A hedge fund buys legal satellite imagery of retailer parking lots; it's commercially available to any paying customer, but most investors don't subscribe.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Alternative data can sit in a practical gray area between broadly disseminated and costly-to-access information; classification depends on availability, access, and the chosen information-set definition. |
| B | False | Semi-strong efficiency does **not** require every investor to own the same subscriptions — prices can aggregate information without universal ownership. |
| C | True | Prices can incorporate information through the trades of a *subset* of informed investors, transmitting it to the wider market. |
| D | True | If data are legal but costly to acquire/process, information-acquisition costs reduce incentives and slow complete incorporation. |
| E | False | Strong and semi-strong forms are **not** identical: the strong form includes private information; semi-strong is limited to public information. |

**Reference:** Grossman–Stiglitz (costly information / limits to efficiency); Fama EMH form distinctions.

### [QF-D8G4Q1] Cross-market arbitrage — law of one price
**Scenario:** The same freely transferable stock trades $50.00 in Market A and $50.40 in Market B; total transaction/transfer cost is $0.10/share, no quantity limits, simultaneous execution.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Gross spread = $50.40 − $50.00 = $0.40/share. |
| B | False | Reverses the conclusion: after $0.10 total costs the net spread *is* $0.30/share, so "net profit is not $0.30" is wrong (double-negative trap). |
| C | False | The profit comes from the *contemporaneous* price discrepancy, not a directional forecast of fundamental value. |
| D | False | Reverses the conclusion: simultaneous execution *does* reduce the risk of one price moving before both legs complete (the choice's negated wording makes it false). |
| E | True | Repeated arbitrage — buying in A, selling in B — pushes A's price up and B's down toward convergence. |

**Reference:** Law of one price / cross-market arbitrage; Investopedia "Arbitrage."

### [QF-D8G4Q2] Convertible vs. replicating portfolio — theoretical arbitrage
**Scenario:** A convertible and a replicating portfolio have identical future cash flows in all states; the convertible costs $102, the replicating portfolio $100; frictionless, no financing/default risk.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the conclusion: identical state-contingent cash flows *should* command the same price under the stated assumptions (LOOP), so "should not have the same price" is wrong. |
| B | True | The arbitrage buys the cheaper equivalent ($100 portfolio) and shorts the dearer one ($102 convertible). |
| C | True | Initial cash flow = $102 short proceeds − $100 purchase = $2 inflow. |
| D | True | Offsetting future obligations in every state leave the $2 initial difference as profit — a theoretical arbitrage under the assumptions. |
| E | False | If cash flows were only *highly correlated* rather than identical, residual (basis) risk remains — the trade would not be riskless. |

**Reference:** Law of one price / replication; riskless vs. risky arbitrage (CFA curriculum, no-arbitrage pricing).

### [QF-D8G4Q3] ETF discount — creation/redemption arbitrage
**Scenario:** An ETF's basket is worth $100.00/share but the ETF trades at $99.60; creation/redemption costs $0.25/share, and the basket value can move during execution.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the conclusion: the ETF trades $100.00 − $99.60 = $0.40 below the basket, so "the discount is not $0.40" is wrong. |
| B | False | Reverses the conclusion: subtracting the $0.25 cost leaves $0.15/share before other frictions, so "the spread is not $0.15" is wrong. |
| C | False | The trade is **not** necessarily riskless — timing, execution, financing, and tracking risks can prevent locking in the spread. |
| D | True | A small gross opportunity can vanish before all legs complete due to execution delay and basket-value movement. |
| E | True | Authorized creation/redemption lets equivalent ETF shares and baskets be exchanged, supporting price–NAV convergence. |

**Reference:** ETF creation/redemption arbitrage mechanism; law of one price with frictions (Investopedia "ETF arbitrage").

### [QF-D8G5Q1] Pair trade — z-score and mean reversion
**Scenario:** Two related stocks have a fitted spread with mean $0, std $2; the current spread is +$5. The model reads positive spreads as Stock A expensive vs. Stock B.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | z = ($5 − $0) / $2 = +2.5. |
| B | True | Mean-reversion trade shorts the relatively expensive Stock A and buys Stock B, profiting if the spread declines. |
| C | False | The *relative* spread can narrow with both stocks rising, both falling, or diverging — it doesn't require both to fall in absolute terms. |
| D | False | A large positive z-score measures historical unusualness; it does **not** guarantee future convergence. |
| E | True | Structural changes (mergers, business-model shifts, leverage changes) can break the historical spread relationship. |

**Reference:** Statistical arbitrage / pairs trading, z-score entry; mean reversion (Investopedia "Statistical arbitrage").

### [QF-D8G5Q2] Dollar-neutral pair trade — P&L
**Scenario:** A pair trade buys $100,000 of Stock B and shorts $100,000 of Stock A. Over the period A rises 8%, B rises 5%, excluding costs.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Long B gain = $100,000 × 5% = $5,000. |
| B | True | Short A loss = $100,000 × 8% = $8,000 (the shorted stock rose). |
| C | False | Net P&L = $5,000 − $8,000 = **−$3,000** before costs, so "earns $3,000" is wrong (it *loses* $3,000). |
| D | False | Dollar neutrality limits net dollar exposure but does **not** eliminate relative-price risk. |
| E | False | Reverses the conclusion: a dollar-neutral trade **can** lose money when both rise — here the short rose more than the long, producing a loss despite balanced initial dollars. |

**Reference:** Dollar-neutral / long-short P&L mechanics; relative-value risk (CFA long-short strategies).

### [QF-D8G5Q3] Threshold optimization — overfitting / selection bias
**Scenario:** A quant team tests z-score thresholds 0.5–4.0 on the same 15-year data; the 2.3 threshold performs best and they report its Sharpe without independent validation.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Choosing the best threshold on the *same* evaluation sample overfits historical noise. |
| B | True | Selection bias makes the winning in-sample Sharpe unusually favorable, likely overstating future performance. |
| C | True | An independent out-of-sample period is a stronger test of whether the chosen rule generalizes. |
| D | False | Calling a strategy "statistical arbitrage" does **not** make it riskless — it typically carries model, convergence, market, and execution risk. |
| E | False | Frequent re-estimation of mean/variance may adapt to change but cannot *guarantee* a valid economic relationship persists. |

**Reference:** Data snooping / selection bias; out-of-sample validation (ISLR ch.5 cross-validation); statistical-arbitrage risk.

### [QF-D8G6Q1] Merger arbitrage — deal spread and risk
**Scenario:** A buyer offers $50/share cash for a target; the target trades at $47 post-announcement because investors think the deal might fail or be delayed.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the conclusion: the deal spread *is* $50 − $47 = $3/share, so "not $3" is wrong (double-negative trap). |
| B | False | Reverses the conclusion: buying at $47 and receiving $50 at close *does* produce a $3 gain before costs, so the negated wording is false. |
| C | False | Completion is uncertain, so the $3 is **not** a guaranteed profit — merger arbitrage is risky event-driven investing. |
| D | True | Regulatory rejection or financing failure can remove the offer-price support and cause a loss. |
| E | True | Annualized return depends on time-to-close: the same $3 earned sooner yields a higher annualized return. |

**Reference:** Merger (risk) arbitrage — deal spread & completion risk; event-driven strategies (CFA / Investopedia "Merger arbitrage").

### [QF-D8G6Q2] Relative-value airline trade
**Scenario:** An investor thinks Airline A is undervalued vs. similar Airline B; she buys $1M of A and shorts $1M of B before an industry-wide fuel-price announcement.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The trade expresses a *relative-value* view (A outperforms B), not a purely directional bet on airlines. |
| B | False | Equal dollar sizing does **not** remove differences in fuel-price sensitivity — the airlines may differ in hedges, routes, costs, leverage, and betas. |
| C | True | If both fall but B falls more, the short gain can exceed the long loss → positive gross return. |
| D | True | Company-specific news affecting only A still influences the outcome — residual idiosyncratic risk remains in a relative-value position. |
| E | False | Borrow fees and short availability for B are **not** irrelevant — they directly affect feasibility and net performance despite equal notionals. |

**Reference:** Relative-value / pairs trading, residual idiosyncratic risk; short-sale cost considerations.

### [QF-D8G6Q3] Earnings surprise vs. priced-in expectations
**Scenario:** A model predicts a retailer beats consensus; the trader buys pre-announcement. Earnings come in above published consensus but below the higher figure already implied by the price, and the stock falls.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Beating published consensus does not guarantee a positive reaction — returns depend on the surprise vs. what was already priced. |
| B | True | Market prices can embed expectations that differ from stated analyst consensus (positioning, informal forecasts, whisper numbers). |
| C | False | Reverses the conclusion: an event-driven strategy *must* forecast **both** the outcome and how it compares to priced-in expectations — a correct number forecast can still lose if the market expected more. |
| D | False | The decline does not prove earnings were objectively poor — a report can be strong absolutely yet disappoint the market's implicit expectation. |
| E | False | Reverses the conclusion: volatility, spreads, and gaps around announcements *do* increase implementation risk (rapid repricing, reduced execution certainty). |

**Reference:** Post-earnings-announcement drift & "beat vs. whisper" expectations; event-driven execution risk.

### [QF-D8G7Q1] Timing / noise-trader risk — the short squeeze
**Scenario:** A manager shorts an overpriced stock at $120 expecting a fall to $80, but it first rises to $170, triggering margin calls and forcing the position closed.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A correct long-run valuation thesis can still lose money because of the price *path* and financing constraints. |
| B | True | Timing/horizon uncertainty (capital and margin limits) can prevent holding until convergence — a core limit to arbitrage. |
| C | True | The interim rise driven by other traders is noise-trader risk for the short seller. |
| D | False | Brokers set collateral/margin on *current exposure*, not the manager's $80 valuation estimate — they need not grant unlimited time. |
| E | False | Reverses the conclusion: forced liquidation *can* let mispricing persist — constrained informed capital cannot necessarily eliminate it immediately. |

**Reference:** Shleifer & Vishny "Limits of Arbitrage" (noise-trader & horizon risk); Shleifer *Inefficient Markets*.

### [QF-D8G7Q2] Crowded-trade / leverage feedback loop
**Scenario:** Several funds hold the same leveraged convergence trade; one gets redemptions and unwinds, moving prices against the rest and triggering further margin calls.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the conclusion: this *is* crowded-trade risk — many investors are exposed to the same position and may exit together. |
| B | True | Price impact from the first liquidation transmits losses and constraints to other funds in the same trade. |
| C | False | Reverses the conclusion: leverage *can* convert a temporary adverse move into forced selling — leveraged portfolios absorb less adverse mark-to-market. |
| D | False | Crowding does **not** guarantee faster convergence — crowded exits can amplify divergence and *delay* convergence. |
| E | True | A strategy's risk depends on other investors' positioning (endogenous liquidity / feedback loops), not only the underlying securities. |

**Reference:** Shleifer & Vishny "Limits of Arbitrage"; crowded trades / LTCM-style deleveraging spirals.

### [QF-D8G7Q3] Short-sale constraints — borrow fee and recall
**Scenario:** An investor spots an apparently overpriced stock but shares are hard to borrow: 18% annual borrow fee, possible lender recall, and unknown correction timing.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A high borrow fee is a direct carrying cost that reduces expected net profit on the short. |
| B | True | A lender recall can force the investor to close before the expected correction — horizon/forced-closeout risk. |
| C | False | Reverses the conclusion: short-sale constraints *can* let overpricing persist longer than under frictionless arbitrage — pessimistic views aren't fully expressed when shorting is costly/infeasible. |
| D | False | An 18% annual borrow fee is **not** irrelevant against a 10% estimated overvaluation — carrying costs can exceed the expected convergence profit, especially with uncertain timing. |
| E | True | Difficulty exploiting a suspected inefficiency can coexist with relatively efficient prices — efficiency is shaped by trading cost/risk, not "every discrepancy is free to remove." |

**Reference:** Shleifer *Inefficient Markets* (short-sale constraints); Miller (1977) overpricing under short constraints; limits to arbitrage.

## References (domain-level)

1. **Fama, E. (1970) "Efficient Capital Markets: A Review of Theory and Empirical Work"** — the canonical weak / semi-strong / strong-form taxonomy and the information-set definitions; also Fama (1965) on the random-walk model of prices.
2. **Shleifer, A. — *Inefficient Markets: An Introduction to Behavioral Finance*** and **Shleifer & Vishny (1997) "The Limits of Arbitrage"** — noise-trader risk, funding/horizon constraints, short-sale constraints, and why mispricing persists despite informed investors.
3. **CFA Institute curriculum** — Market Efficiency (forms of EMH, implications for technical/fundamental analysis), no-arbitrage pricing and the law of one price, and event-driven / relative-value (merger arbitrage, pairs) strategies.
4. **Investopedia** — "Efficient Market Hypothesis," "Arbitrage," "Statistical Arbitrage," "Merger Arbitrage," "ETF Arbitrage," and "No Free Lunch" — accessible definitions matching the question phrasing.
5. **Grossman & Stiglitz (1980) "On the Impossibility of Informationally Efficient Markets"** — costly information acquisition as a structural limit to full incorporation (alternative-data / acquisition-cost questions).
6. **James, Witten, Hastie & Tibshirani — *An Introduction to Statistical Learning*, ch.5 (cross-validation / out-of-sample testing)** — data-snooping, selection bias, and validation for the backtest-overfitting questions.
