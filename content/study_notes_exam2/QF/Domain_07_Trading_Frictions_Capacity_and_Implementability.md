# QF Domain 7 — Trading Frictions, Capacity & Implementability

## Domain cheat-sheet

- **Explicit vs. implicit costs.** *Explicit* costs are directly billed/assessed line items you can read off a statement: broker **commissions**, exchange/venue **fees**, taxes, borrow fees. *Implicit* costs are not separately invoiced but are just as real: the **bid-ask spread**, **slippage**, **market impact**, **delay/timing cost**, and **opportunity cost** of missed fills. A frequent trap is calling a commission or exchange fee "implicit" because it feels like overhead — a separately charged amount is **explicit** by definition. Modeling only explicit fees in a backtest leaves spread, slippage, impact, and opportunity cost unaccounted for, so net return is overstated (Harris, *Trading & Exchanges*, transaction-cost chapters).
- **Bid-ask spread.** Quoted spread = ask − bid. The **midpoint** = (bid + ask) / 2 is the usual frictionless reference. A marketable buy pays the **ask** (half-spread above mid); a marketable sell hits the **bid** (half-spread below mid). Crossing from the midpoint to the ask/bid is a real **spread cost** even when the broker charges zero commission. Per-share half-spread × shares = the spread component of cost. Spread widens in stress and in thin names (Harris, *Trading & Exchanges*, bid-ask spread / dealer-cost chapters).
- **Slippage.** The difference between the price you *expected/referenced* and the price you actually got. It bundles (a) crossing the spread, (b) adverse price movement between the decision and the fill, and (c) walking the book when displayed depth is thin. "Fill came in worse than the displayed ask/decision price" is slippage, not an accounting error.
- **Implementation shortfall (IS).** The all-in gap between the **arrival (decision-time) price** and the realized execution outcome, including explicit fees, spread, impact, delay, and the **opportunity cost** of any unfilled quantity. IS is the honest scorecard: comparing fills only to an *ending* midpoint, or only to the displayed ask, omits the move that already happened relative to the decision reference (Perold's implementation shortfall; Harris, execution-cost measurement chapters).
- **Market impact — temporary vs. permanent.** Your own order moves the price. **Temporary impact** is transient liquidity-demand pressure that **dissipates** after the order completes (price reverts). **Permanent impact** is the lasting, information-related component that stays after pressure ends. A buy that runs price up during execution and then partially reverts shows both: the reversion is temporary impact, the residual above the arrival price is a candidate permanent component (which observation alone cannot prove — other market moves may explain it). The **peak** price move is *not* the permanent impact — it mixes temporary impact, permanent impact, and noise (Almgren & Chriss, *Optimal Execution of Portfolio Transactions*, 2000).
- **Impact models — linear & square-root.** In the Almgren–Chriss framework, **temporary impact** per share is commonly modeled as (roughly) **linear in the trade rate** (shares/time), while aggregate/permanent impact and empirical total cost often scale **sub-linearly** — the widely used **square-root law**: cost ∝ σ·√(Q/ADV). The practical consequence of *nonlinear/convex* impact: trading **10× the size can raise total impact cost by more than 10×** (cost per share rises with participation). Equal expected alpha per share does **not** survive scaling — larger size inflates impact per share and shrinks net alpha per share.
- **Participation rate & liquidity.** Participation = order size ÷ market (or average daily) volume. Larger participation strains available depth, reveals demand, and moves price more. **Average daily volume (ADV/ADDV) does not guarantee an execution price** — it is an aggregate, silent on *current depth*, intraday conditions, and replenishment. Equal quoted percentage spreads do **not** imply equal impact: impact also depends on depth, size relative to liquidity, urgency, and how fast the book refills (Harris, liquidity chapters).
- **Walking the book.** A market order larger than top-of-book depth consumes successive price levels; the **volume-weighted average fill** is worse than the best quote. A tight top-level spread does **not** prove a large order is liquid — tradability of size depends on depth *beyond* the best quote.
- **Turnover & cost drag.** Turnover = total dollar volume traded ÷ portfolio value. Cost drag ≈ turnover × round-trip cost rate. Two strategies with identical gross return can have very different **net** returns if their turnover differs. A positive **gross** edge can be a negative **net** edge once round-trip cost exceeds it (e.g., 8 bps gross edge vs. 10 bps round-trip cost ⇒ −2 bps). Raising a signal **threshold** or using a **no-trade band** reduces churn from small/weak signals, trading away some gross alpha for a larger cost saving — often improving net (Balch ML4T, Marketsim; 02-07 Dealing with Data).
- **Capacity & scaling.** Capacity = how much capital a strategy can deploy before performance degrades below an acceptable level. Adding capital does **not** create more opportunities or deeper liquidity; the same percentage turnover on a bigger base means proportionally more dollars traded, higher participation, and more impact. Gross alpha typically **dilutes** at scale (accepting weaker signals, trading more aggressively) while **costs rise** — net alpha can fall or go negative. Deeper markets / lower turnover / longer holding periods can raise capacity (at the cost of changing the economic strategy). Choose capital level by **net** return and risk, not gross dollar profit.
- **Shorting, borrowing & funding.** Short net edge = gross short return − borrow fee − other financing/trading costs (e.g., 12% − 9% − 2% = 1%). A high **borrow fee** can consume most of the gross edge; ignoring it overstates net profitability. **Availability is not guaranteed**: a locate today does not keep the short open — a **recall** can force an early cover regardless of signal horizon. A short's loss is **theoretically unlimited** (price can rise >100%). Gross exposure = |long| + |short|; net exposure = long − short; leverage = gross ÷ equity. Rising **margin requirements** can force deleveraging even when forecasts are unchanged.
- **Crowding & implementation risk.** Similar signals produce **correlated** portfolios across funds. Simultaneous deleveraging (sell the same longs, cover the same shorts) consumes shared liquidity and moves prices adversely before everyone finishes — a strategy liquid in calm conditions can become hard to exit when crowded investors act together. Faster competitors reacting to the same public data can **capture the gap** before a slower fund fills: a statistically valid forecast is only worth what you can trade on at viable prices. Publication/replication erodes alpha. Stress-testing synchronized entries/exits surfaces risk invisible in a frictionless backtest.
- **Paper vs. live gap.** Backtests that assume fills at the close/open/midpoint, unlimited size at the frictionless price, free shorting, and calm-period costs **overstate implementable performance**. The gap is spread + slippage + impact + opportunity cost + borrow/availability + crowding + stress-period liquidity.

## Common traps

- **Inverted-polarity questions (10 of 21 here).** When the body says *"each item asserts that its quoted statement is incorrect,"* the Answer Key verdict is flipped relative to the inner statement's truth: **True = the inner statement is wrong; False = the inner statement is accurate.** Read the polarity line *first*. Inverted here: **G1Q2, G1Q3, G2Q1, G3Q1, G3Q3, G4Q3, G5Q2, G6Q1, G6Q3, G7Q1.** The remaining 11 are Normal (True = accurate).
- **"Commissions/exchange fees are implicit."** False — anything separately billed or assessed is an **explicit** cost. Implicit = spread, slippage, impact, delay, opportunity cost.
- **"Modeling the explicit fee makes the backtest realistic."** False — spread, slippage, impact, and opportunity cost remain after fees.
- **Reference-price confusion.** Shortfall is measured from the **arrival/decision midpoint**, not the ending midpoint or the displayed ask. Comparing only to the ending price omits the move since the decision.
- **"A later low price proves you could have bought there earlier."** False — an observed later price does not establish that enough liquidity existed at that price at the earlier time.
- **Peak move = permanent impact.** False — peak movement mixes temporary impact, permanent impact, and noise. Reversion after completion signals the temporary component.
- **"Slower/split execution eliminates impact."** False — even gradual orders cross spreads, move prices, and interact with limited depth; splitting *reduces the rate* of liquidity consumption but trades impact for **timing/delay risk** and alpha decay.
- **"Lowest spread+impact schedule always has lowest shortfall."** False — total IS also includes delay, missed trades, and adverse moves.
- **ADV guarantees price / equal spread ⇒ equal impact.** False — volume is an aggregate; impact depends on depth, size vs. liquidity, urgency, replenishment.
- **Tight top-of-book spread ⇒ large order is liquid.** False — depth beyond the best quote governs the tradability of size.
- **Gross edge ⇒ net edge; same gross ⇒ same net.** False — turnover and cost drag separate them; positive gross can be negative net.
- **Threshold guarantees profitable trades.** False — a forecast above a threshold is still uncertain and can be wrong.
- **"More capital can't change a historically profitable rule."** False — scaling dilutes alpha, raises impact, and can erase net edge; capacity is finite.
- **"Historical % returns are guaranteed at larger size."** False — impact, allocation limits, and alpha dilution change performance with scale.
- **Borrow availability / recall.** A locate today does not guarantee the position stays open; recall can force an early cover. A short's loss potential is unlimited.
- **"Short-sale implementability can be read from price history."** False — price history does not establish borrow availability, fees, recalls, or locate requirements.
- **"Crowding only affects expected return."** False — crowding raises impact, liquidity risk, correlations, and unwind losses.
- **"Public data ⇒ equal implementation for all."** False — speed, order handling, capacity, and market access decide realized fills.

## Questions

### [QF2-D7G1Q1] Spread, slippage, and commission on a 1,000-share buy
**Scenario:** A strategy buys 1,000 shares. The quote just before the order is $49.95 bid / $50.05 ask (midpoint $50.00). The order fills immediately at $50.07, and the broker charges a $5 commission.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Quoted spread = ask − bid = $50.05 − $49.95 = **$0.10** per share. |
| B | True | The ask is half a spread above the midpoint: $50.05 − $50.00 = $0.05, and $0.05 × 1,000 = **$50** of spread-related cost before any further slippage. |
| C | True | The fill is $0.02 above the displayed ask ($50.07 − $50.05), i.e. $0.02 × 1,000 = **$20** of additional slippage relative to the displayed ask — the book moved/the order walked past the top level. |
| D | False | A separately billed commission is an **explicit** cost by definition, not implicit. Implicit costs are the spread, slippage, and impact. |
| E | True | Relative to the pre-trade midpoint, the fill is $0.07 above mid ($50.07 − $50.00) → $70, plus the $5 commission = **$75** total. |

**Reference:** Harris, *Trading & Exchanges*, chapters on the bid-ask spread and on transaction-cost measurement (explicit vs. implicit costs); Balch ML4T 02-07 "Dealing with Data" / Marketsim (modeling commission and spread).

### [QF2-D7G1Q2] Backtest at closing midpoint vs. live frictions
**Scenario:** A backtest assumes every trade fills at the daily closing midpoint and subtracts a known exchange fee. Live, market orders cross the spread, some fills occur after the price moves, and an unfilled limit order misses a profitable move. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: an exchange fee is a directly assessed charge, so subtracting it does account for an **explicit** trading cost. |
| B | False (accurate) | Correct: crossing from the midpoint to the ask incurs part of the bid-ask spread — an **implicit** cost that exists even with zero commission. |
| C | False (accurate) | Correct: slippage includes the adverse price deterioration between the reference/expected price and the actual fill, so a post-decision move contributes to it. |
| D | False (accurate) | Correct: the forgone profit from an unfilled limit order is an **opportunity cost** of the execution decision — a real implicit cost. |
| E | True (incorrect) | Wrong: modeling only the explicit exchange fee is **not** sufficient — spread, slippage, market impact, and opportunity cost remain, so net return is still overstated. |

**Reference:** Harris, *Trading & Exchanges*, transaction-cost chapters (explicit vs. implicit costs; spread; opportunity cost); Balch ML4T 02-07 / Marketsim (why idealized fills overstate backtest performance).

### [QF2-D7G1Q3] Implementation shortfall vs. temporary impact (arrival price)
**Scenario:** When a PM releases a buy order the midpoint is $100.00. The volume-weighted average fill is $100.18. At execution end the midpoint is $100.12; the price later falls back to $100.03 after order pressure dissipates. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: $100.18 − $100.00 = **$0.18** per share is an execution/implementation shortfall measured from the arrival midpoint, before explicit fees. |
| B | False (accurate) | Correct: the contemporaneous midpoint rising from $100.00 to $100.12 during execution is consistent with temporary/information-related pressure while the order was active (the scenario alone does not prove the cause). |
| C | False (accurate) | Correct: the post-completion decline toward $100.03 is consistent with transient (temporary) impact dissipating. |
| D | True (incorrect) | Wrong: a later observed price of $100.03 does **not** establish that the full desired quantity could have been bought at $100.03 at the original decision time — later prices do not prove earlier depth. |
| E | False (accurate) | Correct: comparing the fill only with the **ending** midpoint ($100.12) omits part of the cost relative to the $100.00 decision-time reference — shortfall is measured from arrival. |

**Reference:** Perold's implementation shortfall; Harris, *Trading & Exchanges*, execution-cost measurement chapters (arrival-price benchmark); Almgren & Chriss (2000) on temporary vs. permanent impact (reversion after order completion). Balch ML4T 02-07 / Marketsim.

### [QF2-D7G2Q1] Turnover and cost drag across two strategies
**Scenario:** Two dollar-neutral strategies each manage $10M. Strategy A turns over 20%/month, Strategy B 200%/month. Each dollar traded costs 10 bps one-way; turnover = total dollar volume ÷ portfolio value. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: 20% × $10M = **$2M** traded per month for Strategy A. |
| B | False (accurate) | Correct: 200% × $10M = **$20M** traded per month for Strategy B. |
| C | False (accurate) | Correct: 10 bps = 0.001, and 0.001 × $2M = **$2,000** monthly cost for A. |
| D | False (accurate) | Correct: 0.001 × $20M = **$20,000** monthly cost for B. |
| E | True (incorrect) | Wrong: equal gross return does **not** imply equal net return — Strategy B's 10× turnover creates far greater **cost drag**, so its net return is lower. |

**Reference:** Harris, *Trading & Exchanges*, transaction-cost chapters (cost scales with volume traded); Balch ML4T Marketsim and 02-07 (turnover, cost drag on net performance).

### [QF2-D7G2Q2] Signal threshold vs. round-trip cost
**Scenario:** A daily signal forecasts an average gross gain of 8 bps per trade; estimated round-trip cost is 10 bps. A researcher proposes trading only when the forecast exceeds 15 bps, cutting the number of trades substantially.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | 8 bps gross edge − 10 bps round-trip cost = **−2 bps** expected net edge before other costs: the gross edge does not cover the cost. |
| B | True | A positive gross expectancy can still be a negative **net** expectancy once costs are subtracted — trading every signal can lose money net. |
| C | True | A 15-bps threshold suppresses weaker signals, so fewer forecasts qualify and position changes (turnover) fall. |
| D | False | A forecast above the threshold is still **uncertain** — it can be wrong; a threshold cannot guarantee every executed trade is profitable. |
| E | True | Raising a threshold is a tradeoff: it avoids costly weak trades but also skips some genuinely profitable opportunities (selectivity vs. participation). |

**Reference:** Balch ML4T 02-07 / Marketsim (net edge after round-trip cost; turnover reduction via thresholds); Harris, *Trading & Exchanges*, transaction-cost chapters.

### [QF2-D7G2Q3] Rebalance frequency, net alpha, and no-trade bands
**Scenario:** A portfolio ranks stocks hourly but rankings change only slightly. Immediate full rebalancing yields 9% gross alpha and 11% estimated costs; daily rebalancing yields 7% gross alpha and 3% costs.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Hourly net alpha ≈ 9% − 11% = **−2%**. |
| B | True | Daily net alpha ≈ 7% − 3% = **4%**. |
| C | False | The hourly strategy is **not** preferable on gross alpha alone — its higher gross (9%) is more than offset by much larger costs (11%), giving negative net. |
| D | True | A **no-trade band** around current holdings avoids churn from small ranking changes whose expected benefit is too small to justify the cost. |
| E | True | Less frequent rebalancing can improve net performance even while sacrificing some gross alpha — here a 2-pt gross reduction buys an 8-pt cost reduction. |

**Reference:** Balch ML4T 02-07 / Marketsim (rebalance frequency, turnover, net vs. gross alpha, no-trade bands); Harris, *Trading & Exchanges*, transaction-cost chapters.

### [QF2-D7G3Q1] Participation rate and liquidity strain
**Scenario:** A strategy wants to buy $4M of a stock whose average daily dollar volume is $8M; a second candidate has $200M ADDV. Both show equal historical signal strength and equal quoted percentage spread. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: $4M ÷ $8M = **50%** of the first stock's ADDV. |
| B | False (accurate) | Correct: $4M ÷ $200M = **2%** of the second stock's ADDV. |
| C | True (incorrect) | Wrong: average daily volume does **not** guarantee the execution price — it is an aggregate, silent on current depth, price response, and intraday conditions. |
| D | False (accurate) | Correct: at 50% of ADDV the first trade is a much larger fraction of ordinary activity, so it is more likely to strain available liquidity. |
| E | True (incorrect) | Wrong: equal displayed percentage spreads do **not** imply equal market impact — impact also depends on depth, size relative to liquidity, urgency, and replenishment. |

**Reference:** Harris, *Trading & Exchanges*, liquidity and market-impact chapters (participation rate; volume vs. depth); Almgren & Chriss (2000) on impact scaling with size relative to liquidity.

### [QF2-D7G3Q2] Walking the book on a thin security
**Scenario:** A thinly traded security shows a best offer of 500 shares at $20.10, then 1,000 at $20.30, then 2,000 at $20.60. A trader submits a market buy for 3,000 shares; no new sell orders arrive during execution.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The scenario states only **500** shares sit at the best displayed offer ($20.10). |
| B | True | 3,000 > 500 + 1,000, so the order must consume liquidity at **more than one** price level (it reaches the $20.60 tier). |
| C | False | The VWAP fill is **not** $20.10 — only the first 500 shares fill at $20.10; the remaining shares execute at $20.30 and $20.60, raising the average well above $20.10. |
| D | True | Limited displayed depth forces the buyer to **walk up the book**, so the effective purchase cost exceeds what the best quote alone suggests. |
| E | False | A small top-of-book spread does **not** by itself prove a 3,000-share order is highly liquid — tradability of size depends on depth beyond the best quote. |

**Reference:** Harris, *Trading & Exchanges*, order-book / limit-order-book chapters (depth, walking the book, effective cost vs. quoted spread); Balch ML4T 02-07 / Marketsim.

### [QF2-D7G3Q3] Stressed liquidity vs. calm-period cost estimates
**Scenario:** A portfolio normally exits within one day. In a market shock, spreads widen, displayed depth falls, and many participants try to sell the same securities. The backtest estimated costs using calm-period averages. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: reduced liquidity forces a choice between slower execution and larger price concessions, so the portfolio may take **longer or cost more** to exit. |
| B | False (accurate) | Correct: wider spreads increase the cost of demanding immediate liquidity — an aggressive seller crosses a larger distance from midpoint to bid. |
| C | False (accurate) | Correct: falling displayed depth means a fixed-size sell order is more likely to **walk down the book** to lower bid levels. |
| D | True (incorrect) | Wrong: calm-period averages do **not** necessarily give a conservative estimate — costs typically **rise** in stress, so calm-period figures tend to understate stressed execution cost. |
| E | False (accurate) | Correct: liquidity risk can create implementation losses (spreads, impact, delayed fills, forced sales) **beyond** the securities' frictionless price changes. |

**Reference:** Harris, *Trading & Exchanges*, liquidity and market-stress chapters (spread widening, depth withdrawal, liquidity risk); Almgren & Chriss (2000) on cost rising with urgency/volatility. Balch ML4T 02-07 / Marketsim.

### [QF2-D7G4Q1] Participation rate and nonlinear impact
**Scenario:** A fund buys 10,000 shares on a day with 1,000,000 total market volume, then considers 100,000 shares on a day with the same expected volume and similar conditions.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Participation = 10,000 ÷ 1,000,000 = **1%**. |
| B | True | Participation = 100,000 ÷ 1,000,000 = **10%**. |
| C | True | The larger order is a bigger fraction of market volume, so it is more likely to reveal demand and move prices, all else equal. |
| D | True | With **nonlinear/convex** impact, a 10× size increase can raise total impact cost by **more than** 10× (cost per share grows with participation — the square-root/convex-cost intuition). |
| E | False | Equal expected alpha per share does **not** guarantee equal net alpha per share — larger execution size raises impact per share and reduces net alpha. |

**Reference:** Almgren & Chriss (2000), *Optimal Execution of Portfolio Transactions* (temporary impact ~linear in rate; aggregate impact sub-linear / square-root law; convex total cost); Harris, *Trading & Exchanges*, market-impact chapters. Balch ML4T 02-07.

### [QF2-D7G4Q2] Immediate vs. scheduled execution tradeoff
**Scenario:** A manager must buy 200,000 shares. Immediate execution is expected to cost 45 bps in spread+impact; splitting across the day cuts that to 20 bps, but waiting risks the price rising before completion.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Splitting the order distributes trades over time, giving the market time to replenish liquidity and reducing the **rate** of liquidity consumption. |
| B | False | Slower execution does **not** eliminate all market impact — even a gradual order crosses spreads, moves prices, and interacts with limited depth. |
| C | True | The manager faces the core tradeoff: urgency raises immediate impact cost but reduces exposure to adverse price movement (**timing/delay risk**). |
| D | True | If alpha decays quickly, a slow schedule may capture less of the forecast's value — a position obtained after the opportunity fades earns less. |
| E | False | The schedule with the lowest estimated spread+impact does **not** always have the lowest total implementation shortfall — IS also includes delay, missed trades, and adverse moves. |

**Reference:** Almgren & Chriss (2000) (impact vs. timing-risk tradeoff; the efficient frontier of execution); Harris, *Trading & Exchanges*, execution-strategy chapters; alpha decay in Balch ML4T 02-07.

### [QF2-D7G4Q3] Temporary vs. permanent impact and peak movement
**Scenario:** A buy order pushes a stock from $30.00 to $30.40 while executing. Ten minutes after completion it trades at $30.12, and days later remains near $30.15, absent important public news. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the reversal from $30.40 to $30.12 is consistent with a **temporary-impact** component dissipating after buying pressure stopped. |
| B | False (accurate) | Correct: the price staying above $30.00 is consistent with a smaller **persistent** component — though this observation alone does not establish causality (other moves could explain it). |
| C | False (accurate) | Correct: temporary impact is price pressure from transient liquidity demand that tends to dissipate after the order ends. |
| D | True (incorrect) | Wrong: permanent impact need **not** equal the order's peak price movement — the peak ($30.40) mixes temporary impact, permanent impact, and noise. |
| E | False (accurate) | Correct: a backtest assuming unlimited purchases at $30.00 could materially **overstate** implementable performance — the real order moved through prices above the frictionless level. |

**Reference:** Almgren & Chriss (2000), *Optimal Execution of Portfolio Transactions* (decomposition of temporary vs. permanent impact; peak ≠ permanent); Harris, *Trading & Exchanges*, market-impact chapters. Balch ML4T 02-07 / Marketsim (idealized-fill overstatement).

### [QF2-D7G5Q1] Capacity: scaling capital on the same opportunity set
**Scenario:** A strategy manages $2M, targeting short-lived opportunities supporting ~$200,000 of trades/day at modest impact. The sponsor proposes raising capital to $100M while keeping the same securities, horizon, and signal rules.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Adding capital does **not** by itself create more underlying trading opportunities or more liquidity in the targeted names. |
| B | True | The same turnover percentage on a $100M base requires proportionally far more daily dollar volume than at $2M. |
| C | True | Larger orders consume more market depth, raising participation and impact and reducing net return. |
| D | False | Historical percentage returns are **not** guaranteed to persist at $100M — market impact, allocation limits, and alpha dilution change performance with scale. |
| E | True | The strategy may have **limited capacity** even with a strong small-scale backtest — capacity is how much capital can be deployed before performance becomes unacceptable. |

**Reference:** Harris, *Trading & Exchanges*, liquidity and market-impact chapters (capacity, impact scaling); Almgren & Chriss (2000) (cost rising with size); Balch ML4T 02-07 / Marketsim (capacity constraints).

### [QF2-D7G5Q2] Capacity: net alpha across capital levels
**Scenario:** A fund's gross alpha is 6% at $10M, 5% at $50M, 3% at $200M (weaker signals, more aggressive trading). Estimated annual costs are 1%, 2%, and 4% respectively. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: net alpha at $10M = 6% − 1% = **5%**. |
| B | False (accurate) | Correct: net alpha at $50M = 5% − 2% = **3%**. |
| C | False (accurate) | Correct: net alpha at $200M = 3% − 4% = **−1%**. |
| D | False (accurate) | Correct: both gross-alpha **dilution** and rising **costs** reduce scalability here. |
| E | True (incorrect) | Wrong: the $200M deployment is **not** most attractive just because it produces the largest gross dollar profit — allocation must weigh **net** return, risk, alternatives, and whether value is destroyed after costs (net is −1%). |

**Reference:** Harris, *Trading & Exchanges*, transaction-cost and capacity chapters; Almgren & Chriss (2000) (cost grows with size); Balch ML4T 02-07 / Marketsim (net vs. gross alpha, capacity).

### [QF2-D7G5Q3] Raising capacity via deeper markets and lower turnover
**Scenario:** A small-cap strategy nears capacity. The team considers adding large-cap securities, lengthening the holding period, and lowering turnover. The new large-cap signals have lower gross expected returns but much deeper markets.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Expanding into **deeper** markets can accommodate larger trades with less impact, increasing deployable capacity. |
| B | True | Lower turnover reduces the dollars that must be traded per dollar of capital, easing the liquidity/impact burden. |
| C | True | A longer holding period can help capacity by cutting trading frequency — though it also changes signal effectiveness and risk (it alters the economic strategy). |
| D | False | Adding lower-alpha large-cap opportunities does **not** necessarily reduce total net profit — greater depth can permit more capital and lower costs, improving scalable net profit. |
| E | True | Capacity analysis concerns the joint relationship among capital, opportunity availability, liquidity, costs, and resulting performance — not alpha or capital alone. |

**Reference:** Harris, *Trading & Exchanges*, liquidity/market-impact chapters (depth and capacity); Almgren & Chriss (2000) (impact vs. liquidity); Balch ML4T 02-07 / Marketsim (turnover, holding period, capacity).

### [QF2-D7G6Q1] Shorting a hard-to-borrow name: borrow fee and recall
**Scenario:** A strategy shorts a hard-to-borrow stock with a 12% expected annual gross return from the short. The annualized borrow fee is 9%; other trading/financing costs are ~2%. Shares are available today but not guaranteed for the full holding period. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: estimated annual net return ≈ 12% − 9% − 2% = **1%** if the gross return and stated costs are realized. |
| B | False (accurate) | Correct: the 9% borrow fee consumes three-quarters of the 12% gross edge — most of the expected edge. |
| C | True (incorrect) | Wrong: present borrow availability does **not** guarantee the short can stay open until the manager chooses to close — borrow can become unavailable or be recalled. |
| D | False (accurate) | Correct: a lender **recall** can force an early cover regardless of the signal's intended horizon. |
| E | False (accurate) | Correct: ignoring the borrow fee would overstate the short's net profitability — the omitted fee is economically large relative to the edge. |

**Reference:** Harris, *Trading & Exchanges*, short-selling and securities-lending chapters (borrow fees, locates, recall risk); Balch ML4T 02-07 / Marketsim (financing costs, short constraints).

### [QF2-D7G6Q2] Leverage, exposure, and unlimited short loss
**Scenario:** A leveraged long-short fund holds $150M long and $100M short against $50M of equity. The broker raises margin requirements during a volatile period while several shorts rise sharply.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Gross exposure = \|long\| + \|short\| = $150M + $100M = **$250M**. |
| B | True | Net exposure = long − short = $150M − $100M = **$50M long**. |
| C | True | Leverage = gross ÷ equity = $250M ÷ $50M = **5×**. |
| D | True | Higher margin requirements can force position reductions (a funding constraint / forced deleveraging) even if long-run forecasts are unchanged. |
| E | False | A short's loss is **not** capped at initial market value — a stock can rise more than 100%, giving a short **theoretically unlimited** loss. |

**Reference:** Harris, *Trading & Exchanges*, chapters on short selling, margin, and leverage (gross/net exposure, funding constraints, unlimited short loss); Balch ML4T 02-07 / Marketsim.

### [QF2-D7G6Q3] Free-shorting backtest vs. real borrow constraints
**Scenario:** A backtest freely shorts every stock with a negative signal at the prior close. In practice, some stocks have no borrow, some carry variable borrow fees, and a crowded short rises rapidly when others cover. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: stocks with no available borrow may be **impossible to short** at the desired time — a negative forecast does not create lendable shares. |
| B | False (accurate) | Correct: variable borrow fees can make realized net performance differ from a backtest using a fixed cost (fees rise as a name gets hard to borrow). |
| C | False (accurate) | Correct: rapid covering by other short sellers adds buy demand and can intensify an upward price move — a **short squeeze**. |
| D | True (incorrect) | Wrong: short-sale implementability **cannot** be assumed from historical price data alone — price history does not establish borrow availability, fees, recalls, or locate requirements. |
| E | False (accurate) | Correct: a realistic backtest could restrict the eligible universe and model borrow costs, availability, and forced-close risk. |

**Reference:** Harris, *Trading & Exchanges*, short-selling and securities-lending chapters (locates, borrow availability, squeeze dynamics); Balch ML4T 02-07 / Marketsim (realistic short-side modeling).

### [QF2-D7G7Q1] Crowding and correlated deleveraging
**Scenario:** Many funds use similar momentum signals and hold overlapping long/short positions. A volatility spike causes several to reduce leverage at the same time. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: common inputs and rules can produce **correlated portfolios** across funds. |
| B | False (accurate) | Correct: simultaneous deleveraging commonly means many funds **sell the same longs and cover the same shorts**. |
| C | False (accurate) | Correct: correlated exits consume shared liquidity and can worsen prices before every fund completes its trades. |
| D | True (incorrect) | Wrong: crowding does **not** affect only expected return — it can increase market impact, liquidity risk, correlations, and losses during unwinds. |
| E | False (accurate) | Correct: a strategy liquid in normal conditions can become hard to exit when crowded investors act together — effective liquidity depends on competing exit demand. |

**Reference:** Harris, *Trading & Exchanges*, liquidity and market-stress chapters (crowding, correlated order flow, liquidity risk); Balch ML4T 02-07 / Marketsim (implementation risk beyond frictionless backtest).

### [QF2-D7G7Q2] Opening-fill assumption vs. faster competitors
**Scenario:** A backtest assumes trades fill at the next day's open. After launch, many competitors react to the same public data before the open; prices gap in the predicted direction, spreads widen, and the live fund fills after much of the move.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The assumed opening fill may be **unavailable** once many traders pursue the same signal — competitive order flow moves prices before/during execution. |
| B | True | The gap can represent alpha captured by **faster participants** rather than the live fund — a correct forecast can arrive too late to earn the predicted return. |
| C | True | Wider spreads raise execution cost, further reducing realized net return. |
| D | False | Public availability of the input does **not** guarantee equal implementation — speed, order handling, capacity, and market access shape realized fills. |
| E | True | Live implementation shortfall can reveal that a statistically valid forecast is **not fully monetizable** by this trading process — information is worth only what you can trade on at viable prices. |

**Reference:** Harris, *Trading & Exchanges*, chapters on information, latency, and execution quality; Perold's implementation shortfall; Balch ML4T 02-07 / Marketsim (paper vs. live gap).

### [QF2-D7G7Q3] Publication, replication, and alpha erosion
**Scenario:** A niche strategy did well with $5M when few knew it. After publication, multiple funds replicate the rule, deploy large capital collectively, and trade the same securities at the same times.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Replication increases **competition** for a limited set of opportunities — more capital chasing the same signals and liquidity. |
| B | True | Entry trades by multiple funds move prices sooner, eroding the alpha remaining for later traders. |
| C | True | Crowding reduces the capital each fund can deploy at acceptable cost — shared depth and higher impact lower capacity. |
| D | False | A historically profitable rule's future net profitability **can** change — competition, impact, and earlier price adjustment can reduce or eliminate future net alpha. |
| E | True | Stress-testing synchronized entries/exits can expose implementation risk and liquidity deterioration invisible in a frictionless backtest. |

**Reference:** Harris, *Trading & Exchanges*, liquidity and competition chapters (crowding, alpha decay); Almgren & Chriss (2000) (impact under aggregate size); Balch ML4T 02-07 / Marketsim (capacity and implementation risk).

## References (domain-level)

1. **Harris — *Trading & Exchanges: Market Microstructure for Practitioners*:** chapters on the bid-ask spread and dealer costs; transaction-cost measurement (explicit vs. implicit costs; commissions and fees as explicit; spread, slippage, impact, opportunity cost as implicit); the limit order book, depth, and walking the book; liquidity, market stress, and liquidity risk; short selling, securities lending, locates, borrow fees, and recall; margin, leverage, gross/net exposure, and unlimited short loss; crowding, competition, and alpha decay. Cited at section/chapter level only.
2. **Almgren & Chriss (2000), *Optimal Execution of Portfolio Transactions*:** market-impact decomposition into **temporary** (transient, dissipating) vs. **permanent** (lasting, information-related) components; temporary impact modeled ~linear in trade rate; aggregate/empirical cost often sub-linear (**square-root law**, cost ∝ σ·√(Q/ADV)); convex total cost (10× size can cost >10×); the impact-vs-timing-risk tradeoff and execution efficient frontier; peak price move ≠ permanent impact.
3. **Perold — implementation shortfall:** the arrival-price benchmark; all-in gap between decision price and realized outcome including fees, spread, impact, delay, and opportunity cost of unfilled quantity.
4. **Balch — ML4T (Georgia Tech), module 02-07 "Dealing with Data" and the Marketsim project:** modeling commissions and market impact in a simulator; turnover and cost drag; net vs. gross alpha; rebalance frequency and no-trade bands; capacity constraints; realistic short-side modeling; the paper-vs-live performance gap and why idealized fills (close/open/midpoint, unlimited size, free shorting, calm-period costs) overstate implementable performance.

---
*Glyph note: the source slice `QF2_D07.txt` renders the "fi" ligature as a single garbled glyph throughout (e.g., "ﬁll", "proﬁt", "ﬁrst", "deﬁnition", "beneﬁt", "insufficient"). These were normalized to plain "fi" in this note; no verdicts or numeric values were affected.*
