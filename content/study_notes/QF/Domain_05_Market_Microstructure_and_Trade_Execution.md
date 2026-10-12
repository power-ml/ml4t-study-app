# QF Domain 5 — Market Microstructure and Trade Execution

## Domain cheat-sheet

- **Best bid / best ask**: the highest price a buyer will pay (bid) and the lowest a seller will accept (ask). A market **buy** lifts the **ask**; a market **sell** hits the **bid**.
- **Quoted spread** = ask − bid (in dollars). **Midpoint** = (bid + ask) / 2. The spread is a cost paid for *immediacy* — crossing it is the price of demanding an instant fill.
- **Relative (percentage) spread** = dollar spread / midpoint. A larger *dollar* spread does not by itself mean less liquid; compare relative spread, depth, volume, resilience, and trade size.
- **Market order** = certainty of *execution*, uncertain *price* (can walk the book). **Limit order** = control of *price*, uncertain *execution* (fill risk; a resting limit may never trade even if the market touches its price, due to queue priority and available size).
- **Buy limit** sets the *maximum* acceptable price; **sell limit** sets the *minimum*. A buy limit priced at/above the ask becomes marketable; below the ask, it rests as bid-side liquidity.
- **Order book / market depth**: price levels and the quantity resting at each. Best price ≠ total available liquidity. A large order "walks the book," consuming successively worse levels. Identical spreads can hide very different depth. Displayed depth is not guaranteed — it can be canceled or hidden.
- **Order imbalance**: asymmetry in displayed depth. Can carry *probabilistic* short-horizon information, but never guarantees direction and can be spoofed or evaporate.
- **Slippage** = realized execution price − quoted/decision price. **Market impact** = the order's own effect on price. Impact splits into **temporary** (transient pressure that reverts) and **permanent** (lasting information effect). Isolating the two needs a benchmark methodology and more data than a quote.
- **Liquidity risk** scales with order size *relative to available liquidity/volume*, not dollars alone. A profitable paper strategy can be infeasible at scale (capacity constraint).
- **Short selling**: borrow shares → **sell-to-open**; later **buy-to-close** and return them. Profit when price *falls*. Costs: borrow fee + owed dividends to the lender. **Loss is theoretically unlimited** (price has no upper bound); gain is capped (price floor = 0). **Short squeeze / recall risk** can force covering against the trader's view; collateral does not remove economic/operational risk.
- **Implementation shortfall** = decision-price benchmark vs. actual outcome, including price move (delay + execution) and commissions. Decision value = shares × decision price. Later P&L does not erase implementation cost.
- **Transaction costs** = commissions + spread + market impact + delay cost. Gross return overstates realized (net) performance. High turnover amplifies per-trade cost sensitivity; zero commission still leaves spread and impact.
- **Execution strategy**: split large orders to lower instantaneous impact at the cost of *timing risk* (adverse moves, signal decay) and possible *information leakage* from predictable patterns. Optimal schedule balances expected alpha decay against transaction costs; no algorithm eliminates impact, timing, and non-completion risk simultaneously.

## Common traps

- **No fully inverted-polarity questions in this slice.** None carry the "Answer Key (True = incorrect; False = accurate)" header, so every question below is scored with **Normal** polarity (True verdict = statement accurate). Still read each Answer Key line literally.
- **Embedded-claim / double-negative choices** — the biggest trap here. Phrases like *"A reviewer would be wrong to accept the claim that X"* and *"It would be wrong to reject X"* flip the truth value: if X is actually correct, the choice is **False** ("the underlying claim is correct and should be accepted"). Affected: **[QF-D5G1Q3] A**, **[QF-D5G3Q1] C**, **[QF-D5G7Q3] C and E**.
- **Negation traps ("... is not ...")** — a choice that asserts a value is *not* the correct number is **False** when that number is in fact correct. Affected: **[QF-D5G1Q1] B**, **[QF-D5G1Q2] D**, **[QF-D5G3Q1] D**, **[QF-D5G5Q2] C**, **[QF-D5G6Q1] A**, **[QF-D5G6Q2] B**, **[QF-D5G6Q3] D**. The Answer Key tags these "The statement reverses the correct conclusion."
- **Round-trip / direction sign errors**: buying at the ask and selling at the bid *loses* the spread, not gains it ([QF-D5G1Q1] D). For a *seller*, a lower execution price is *worse* ([QF-D5G6Q3] E); a buyer prefers lower ([QF-D5G4Q1] C).
- **"Guarantee" and "eliminate" absolutes** are almost always False: limit orders don't guarantee fills ([QF-D5G2Q2] C), market orders don't eliminate price risk ([QF-D5G2Q3] E), splitting doesn't guarantee lower cost ([QF-D5G7Q1] D), displayed depth isn't guaranteed to persist ([QF-D5G3Q2] E), collateral doesn't eliminate short risk ([QF-D5G5Q3] E).
- **"Proves" overreach**: an observed price level or unchanged midpoint never *proves* unchanged liquidity or an exact permanent-value change ([QF-D5G1Q3] D, [QF-D5G4Q3] C).

## Questions

### [QF-D5G1Q1] Quoted spread, midpoint, and round-trip cost
**Scenario:** A stock is quoted best bid $49.90 / best ask $50.10. An investor considers an immediate round trip, ignoring commissions and price changes.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. The quoted spread is $0.20 per share. | True | Spread = ask − bid = $50.10 − $49.90 = $0.20. |
| B. The quoted midpoint is not $50.00. | False | Negation trap. Midpoint = ($49.90 + $50.10)/2 = $50.00, so "not $50.00" reverses the correct conclusion. |
| C. A market buy would not normally execute against the ask side of the book. | False | An aggressive buyer takes resting sell liquidity at the ask; a market buy lifts the ask. |
| D. An immediate market buy followed by an immediate market sell would gain $0.20 per share. | False | Buying at $50.10 and selling at $49.90 *loses* $0.20/share — the round trip pays the spread. |
| E. The spread represents one component of the cost of demanding immediate liquidity. | True | Crossing the spread is a cost of immediacy paid to liquidity providers. |

**Reference:** Investopedia — Bid-Ask Spread (cost of immediacy). Harris, *Trading and Exchanges* — ch. on bid/ask quotes and the cost of liquidity.

### [QF-D5G1Q2] Dollar spread vs. relative spread and liquidity
**Scenario:** Stock A is $20.00 × $20.04; Stock B is $200.00 × $200.20. A trader compares their spreads.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. Stock A's dollar spread is $0.04. | True | $20.04 − $20.00 = $0.04. |
| B. Stock B's dollar spread is larger than Stock A's. | True | $0.20 (B) > $0.04 (A) in dollar terms. |
| C. Relative to the midpoint, Stock A's spread is approximately 0.20%. | True | $0.04 / $20.02 ≈ 0.20%. |
| D. Relative to the midpoint, Stock B's spread is not approximately 0.10%. | False | Negation trap. $0.20 / $200.10 ≈ 0.10%, so the "not" reverses the correct conclusion. |
| E. The larger dollar spread proves that Stock B is less liquid by every meaningful measure. | False | Liquidity also depends on relative spread, depth, volume, resilience, and trade size — dollar spread alone doesn't prove it. |

**Reference:** CFA curriculum — market microstructure / liquidity measures (relative spread, depth). Investopedia — Bid-Ask Spread and liquidity.

### [QF-D5G1Q3] Quote change, midpoint, and fill risk (embedded-claim trap)
**Scenario:** In a quiet period a quote moves from $75.00 × $75.02 to $74.95 × $75.07 with similar displayed depth.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. A reviewer would be wrong to accept the claim that the midpoint remains $75.01 after the quote change. | False | Embedded-claim trap. Both quotes have midpoint $75.01 ((75.00+75.02)/2 and (74.95+75.07)/2), so the underlying claim is correct and should be accepted. |
| B. The spread widens from $0.02 to $0.12. | True | New spread = $75.07 − $74.95 = $0.12; old was $0.02. |
| C. The wider spread generally makes immediate trading more expensive. | True | A liquidity demander must cross a larger spread. |
| D. The unchanged midpoint proves that the stock's liquidity is unchanged. | False | Spread width is itself a liquidity dimension; an unchanged midpoint doesn't prove unchanged liquidity. |
| E. A passive buyer posting at the bid cannot avoid crossing the spread but assumes fill risk. | False | Reverses the conclusion: a bid-side limit order *avoids* crossing the spread (controls price) but may never execute (fill risk). |

**Reference:** Investopedia — Bid-Ask Spread; Limit Order / fill risk. Harris, *Trading and Exchanges* — liquidity dimensions.

### [QF-D5G2Q1] Market vs. limit order for a large buy
**Scenario:** A desk must buy 200,000 shares of a moderately liquid stock before the close; the head trader wants guaranteed completion, the PM wants to avoid paying far above the ask.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. A market order provides more certainty of execution than a limit order. | True | Market orders prioritize execution over price. |
| B. A limit order guarantees execution at the specified price. | False | A limit order may never execute; it guarantees price bound, not a fill. |
| C. A large market order may walk through multiple levels of the order book. | True | It consumes liquidity at progressively worse prices when top-of-book size is insufficient. |
| D. Splitting the order can reduce immediate market impact but introduces timing risk. | True | Slower execution lowers instantaneous footprint but exposes the order to adverse price moves. |
| E. The quoted ask necessarily equals the average execution price for the full 200,000-share order. | False | Available depth at the best ask is limited; the fill VWAP typically exceeds the quoted ask. |

**Reference:** Investopedia — Market Order vs. Limit Order. Harris, *Trading and Exchanges* — order types and execution certainty.

### [QF-D5G2Q2] Marketability of a buy limit below the ask
**Scenario:** Stock quoted $30.00 bid / $30.05 ask. A trader submits a limit buy for 1,000 shares at $30.02.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. The order should immediately execute against the displayed $30.05 ask. | False | The $30.02 buy limit is below the $30.05 ask, so it is not marketable and won't execute immediately. |
| B. The order cannot become resting bid-side liquidity at $30.02. | False | Subject to venue rules it can rest as a bid at its limit price. |
| C. The trader is guaranteed to receive 1,000 shares if the market later trades at $30.02. | False | Queue priority and available quantity can prevent a fill even if trades print at that price. |
| D. If filled, the order cannot execute above its $30.02 limit price. | True | A buy limit sets the maximum acceptable execution price. |
| E. Raising the buy limit to $30.05 could make the order immediately marketable against displayed ask liquidity. | True | A buy priced at the ask can trade with resting sellers. |

**Reference:** Investopedia — Limit Order (marketable limit, price protection). Harris, *Trading and Exchanges* — limit order book mechanics and priority.

### [QF-D5G2Q3] Market vs. limit sell before earnings
**Scenario:** Minutes before an earnings announcement, a manager choosing between a market and a limit order to sell.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. A market sell emphasizes prompt execution but leaves the realized price uncertain. | True | Market orders prioritize execution, not a guaranteed price. |
| B. A sell limit establishes the minimum acceptable execution price. | True | A sell limit prevents execution below its limit. |
| C. A sell limit placed above the current bid cannot remain unfilled if prices fall. | False | Reverses the conclusion: the market can move away before anyone trades with the order, leaving it unfilled. |
| D. Greater urgency generally strengthens the case for accepting price uncertainty to obtain execution. | True | Urgent traders often accept more price risk to secure completion. |
| E. A market order eliminates both fill risk and the risk of an unfavorable execution price. | False | Market orders reduce non-execution risk but can still receive poor prices. |

**Reference:** Investopedia — Market vs. Limit Orders; slippage under urgency. Harris, *Trading and Exchanges* — execution vs. price risk trade-off.

### [QF-D5G3Q1] Walking the book and VWAP (embedded-claim + negation traps)
**Scenario:** Ask side shows 500 @ $10.01, 1,000 @ $10.03, 2,000 @ $10.05. A market buy for 2,000 shares fills with no new orders or cancels.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. The order buys 500 shares at $10.01. | True | The best ask level is consumed first. |
| B. The order buys 1,000 shares at $10.03. | True | The next 1,000 consume the second ask level. |
| C. A reviewer would be wrong to accept the claim that the remaining 500 shares execute at $10.05. | False | Embedded-claim trap. After 1,500 shares, 500 remain and fill at $10.05, so the underlying claim is correct and should be accepted. |
| D. The volume-weighted average execution price is not $10.03. | False | Negation trap. VWAP = (500×10.01 + 1,000×10.03 + 500×10.05)/2,000 = $10.03, so "not $10.03" reverses the conclusion. |
| E. The entire order executes at the original best ask because that was the displayed quote when it was submitted. | False | Only 500 shares were displayed at the original best ask; the rest fills deeper in the book. |

**Reference:** Investopedia — Order Book / market depth; slippage from walking the book. Harris, *Trading and Exchanges* — limit order book and VWAP of a marketable order.

### [QF-D5G3Q2] Equal spreads, unequal depth
**Scenario:** Two stocks each show a one-cent spread; Stock A displays 100 shares at each best quote, Stock B displays 20,000.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. The identical spreads imply identical displayed depth. | False | Spread and displayed quantity measure different aspects of liquidity. |
| B. A 10,000-share market order is more likely to walk the book in Stock A. | True | Only 100 shares sit at Stock A's best price, so the order exhausts it and moves to worse levels. |
| C. For a very small order, both stocks may initially offer the same quoted price concession. | True | An order within the displayed size crosses the same one-cent spread in either name. |
| D. Market depth is a relevant liquidity measure even when quoted spreads match. | True | Depth determines how much can trade near the best quote. |
| E. Displayed depth is guaranteed to remain available until every incoming order has traded against it. | False | Orders may be canceled or changed before execution; displayed depth is not guaranteed. |

**Reference:** Investopedia — Market Depth / Order Book; liquidity beyond the spread. Harris, *Trading and Exchanges* — depth and displayed vs. available liquidity.

### [QF-D5G3Q3] Order imbalance as a short-term signal
**Scenario:** The book shows much greater displayed buy quantity than sell quantity near the midpoint; an analyst treats the imbalance as a short-term bullish signal.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. The imbalance describes an asymmetry in displayed depth. | True | More displayed quantity appears on one side of the book. |
| B. It cannot contain information about near-term supply and demand. | False | Reverses the conclusion: depth imbalance can sometimes provide short-horizon information. |
| C. It guarantees that the next price movement will be upward. | False | Order-book signals are probabilistic and can fail or be manipulated. |
| D. Cancellations or hidden liquidity can weaken the signal. | True | The displayed book is incomplete and can change rapidly. |
| E. Using the signal without accounting for execution costs cannot overstate its trading value. | False | Reverses the conclusion: a predictive signal need not remain profitable after trading costs, so ignoring costs *can* overstate its value. |

**Reference:** Harris, *Trading and Exchanges* — order-book information and imbalance. Investopedia — Order Book / liquidity; net-of-cost signal value.

### [QF-D5G4Q1] Slippage vs. quoted ask
**Scenario:** At the buy decision the best ask is $40.00; the desk buys 10,000 shares at an average $40.12.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. Relative to the quoted ask, the execution slippage is $0.12 per share. | True | $40.12 − $40.00 = $0.12 per share. |
| B. The total price difference relative to buying all shares at $40.00 is $1,200. | True | $0.12 × 10,000 = $1,200. |
| C. The average execution was better for the buyer than the quoted ask. | False | A buyer prefers a *lower* price; $40.12 > $40.00 is worse. |
| D. Limited depth and market impact could both contribute to the difference. | True | Walking the book and the order's own price impact can both worsen the fill. |
| E. The quotation alone is sufficient to identify exactly how much of the difference was temporary market impact. | False | Separating temporary vs. permanent impact requires additional data and a benchmark methodology. |

**Reference:** Investopedia — Slippage; Market Impact. Harris, *Trading and Exchanges* — realized vs. quoted price and impact decomposition.

### [QF-D5G4Q2] Order size relative to liquidity (deep vs. thin)
**Scenario:** A fund trades the same dollar amount in a deep large-cap and a thin small-cap; the small-cap order is large relative to normal volume.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. The small-cap trade will generally face greater liquidity risk. | True | Thin markets absorb large relative orders less easily. |
| B. Equal dollar orders necessarily produce equal percentage market impact. | False | Impact depends on depth, volume, volatility, and size relative to liquidity — not dollars alone. |
| C. An order's size relative to available liquidity matters for execution quality. | True | Capacity is not determined by dollars alone. |
| D. A profitable paper strategy cannot become infeasible if its required trades exceed market capacity. | False | Reverses the conclusion: liquidity can constrain whether theoretical signals are implementable at scale. |
| E. Reducing the order's participation rate cannot lower immediate impact while increasing exposure to price movement during execution. | False | Reverses the conclusion: slower trading exchanges impact risk for timing risk (it *does* lower immediate impact). |

**Reference:** Investopedia — Market Impact / Liquidity; strategy capacity. Harris, *Trading and Exchanges* — order size vs. available liquidity.

### [QF-D5G4Q3] Temporary vs. permanent impact
**Scenario:** After a large buy, the stock rises from $25.00 to $25.30; ten minutes after the order ends it falls to $25.08 and stays there.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. The initial increase could not include temporary and permanent impact. | False | Reverses the conclusion: the immediate response can contain both transient pressure and lasting information effects. |
| B. The reversal from $25.30 to $25.08 is consistent with some temporary impact decaying. | True | Price reversion after completion is consistent with transient pressure dissipating. |
| C. The remaining $0.08 increase proves that the order permanently changed fundamental value by exactly $0.08. | False | Other trades, information, and benchmark choices prevent that exact causal conclusion. |
| D. Market-wide news during the interval could confound the impact estimate. | True | Concurrent market moves can affect the observed price path. |
| E. Temporary impact matters to execution cost even if the price later reverses. | True | The trader may have paid the temporarily elevated prices during execution. |

**Reference:** Harris, *Trading and Exchanges* — temporary vs. permanent price impact. Investopedia — Market Impact; slippage attribution.

### [QF-D5G5Q1] Short sale mechanics and profit direction
**Scenario:** A trader borrows and sells short 1,000 shares at $50, later buys them back at $42, ignoring fees and dividends.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. The opening transaction is not a sell-to-open. | False | Reverses the conclusion: selling borrowed shares *is* a sell-to-open that establishes the short. |
| B. The closing transaction is a buy-to-close. | True | Repurchasing shares closes the short position. |
| C. The gross trading profit is $8,000. | True | ($50 − $42) × 1,000 = $8,000. |
| D. The short position profits because the stock price increased. | False | A short profits when the price *declines*. |
| E. The shares purchased to close cannot be returned to the lender. | False | Reverses the conclusion: the repurchased shares satisfy the obligation to return the borrowed shares. |

**Reference:** Investopedia — Short Selling (sell-to-open / buy-to-close). CFA curriculum — short-position mechanics.

### [QF-D5G5Q2] Short-sale carrying costs (dividend + borrow fee)
**Scenario:** An investor shorts 500 shares at $20; during the hold the company pays a $0.40 dividend, the borrow fee is $150, and the investor covers at $18.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. The gross price profit before carrying costs is $1,000. | True | ($20 − $18) × 500 = $1,000. |
| B. The short seller generally owes a payment equivalent to the $200 dividend on the borrowed shares. | True | The lender is economically entitled to the dividend; $0.40 × 500 = $200 owed by the short. |
| C. After the dividend payment and borrow fee, the net profit is not $650, ignoring other costs. | False | Negation trap. $1,000 − $200 − $150 = $650, so "not $650" reverses the conclusion. |
| D. Borrow fees increase the net return of a short position. | False | Borrow fees are a *cost* that reduces net return. |
| E. A high-conviction price forecast can still be unprofitable after short-position carrying costs. | True | Dividends, borrow charges, and other costs can consume a forecasted gain. |

**Reference:** Investopedia — Short Selling costs (borrow fee, dividend obligation). CFA curriculum — carrying costs of short positions.

### [QF-D5G5Q3] Short squeeze, recall risk, and unlimited loss
**Scenario:** A crowded short rises sharply after unexpected good news; lenders begin recalling shares and borrow availability falls.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. A short seller's maximum gain is bounded because a stock price cannot fall below zero. | True | The greatest price decline is from the sale price to zero, capping the gain. |
| B. A short seller's theoretical loss is not unlimited because the stock price has no fixed upper bound. | False | Reverses the conclusion: because price has no upper bound, repurchase cost can keep rising — loss *is* theoretically unlimited. |
| C. Forced buying by short sellers cannot intensify a short squeeze. | False | Reverses the conclusion: buy-to-close demand adds upward pressure and can intensify a squeeze. |
| D. Recall risk can force a trader to close even when the trader still believes the stock is overvalued. | True | Continued borrowing is not always under the short seller's control. |
| E. Posting collateral eliminates price risk and borrow risk for the short seller. | False | Collateral supports the position but does not remove its economic or operational risks. |

**Reference:** Investopedia — Short Squeeze; unlimited loss; recall risk. CFA curriculum — short-selling risks.

### [QF-D5G6Q1] Implementation shortfall with delay and commission
**Scenario:** A manager decides to buy 5,000 shares at $100.00; delayed approval means execution at an average $100.40 plus a $100 commission.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. The decision-value benchmark is not $500,000. | False | Negation trap. 5,000 × $100.00 = $500,000, so "not $500,000" reverses the conclusion. |
| B. The execution-price difference costs $2,000 relative to the decision price. | True | 5,000 × ($100.40 − $100.00) = $2,000. |
| C. Including the commission, the implementation shortfall is $2,100 under this simplified benchmark. | True | $2,000 price cost + $100 commission = $2,100. |
| D. The $0.40 adverse move may be described as a delay or execution-related cost, depending on the timing decomposition used. | True | Attribution depends on benchmark timestamps and the execution process. |
| E. Because the position may later be profitable, the implementation shortfall at execution must be zero. | False | Later investment performance does not erase the cost of implementing the decision. |

**Reference:** CFA curriculum — Implementation Shortfall (decision price benchmark, delay/execution decomposition). Investopedia — Implementation Shortfall.

### [QF-D5G6Q2] Gross vs. net return and turnover sensitivity
**Scenario:** A strategy earns 12% gross annually; commissions 0.5%, spread costs 1.0%, estimated market impact 1.5%, no other costs.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. The stated trading costs total 3.0% of capital. | True | 0.5% + 1.0% + 1.5% = 3.0%. |
| B. The simplified net return is not 9.0%. | False | Negation trap. 12.0% − 3.0% = 9.0% under the additive treatment, so "not 9.0%" reverses the conclusion. |
| C. Reporting only the 12% gross return overstates the investor's realized performance under these assumptions. | True | Investors keep returns *after* implementation costs, not before them. |
| D. Eliminating commissions would also eliminate spread and market-impact costs. | False | Spread and impact can remain even with zero explicit commission. |
| E. A high-turnover strategy cannot be more sensitive to per-trade costs than a low-turnover strategy. | False | Reverses the conclusion: more frequent trading creates more opportunities to incur costs. |

**Reference:** Investopedia — Transaction Costs; gross vs. net return. CFA curriculum — cost drag and turnover.

### [QF-D5G6Q3] Sell-side implementation shortfall
**Scenario:** A PM orders the sale of 10,000 shares at a $50.00 decision price; the desk sells 6,000 @ $49.80 and 4,000 @ $49.60, paying $200 in commissions.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. The average execution price is $49.72. | True | (6,000×49.80 + 4,000×49.60)/10,000 = $49.72. |
| B. The price shortfall relative to the decision price is $0.28 per share. | True | For a seller, $50.00 − $49.72 = $0.28 per share is adverse. |
| C. The price component of implementation shortfall is $2,800. | True | $0.28 × 10,000 = $2,800. |
| D. Including commissions, total simplified implementation shortfall is not $3,000. | False | Negation trap. $2,800 + $200 = $3,000, so "not $3,000" reverses the conclusion. |
| E. Because this is a sale, receiving less than the decision price improves execution quality. | False | A seller benefits from a *higher* execution price; less than decision price is worse. |

**Reference:** CFA curriculum — Implementation Shortfall (sell-side sign convention). Investopedia — VWAP; Implementation Shortfall.

### [QF-D5G7Q1] Order size vs. daily volume and splitting
**Scenario:** A fund must buy 1 million shares where normal daily volume is 2 million; it weighs immediate execution vs. splitting across the day.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. The order equals 50% of normal daily volume and is not therefore large relative to typical activity. | False | Reverses the conclusion: 1M / 2M = 50% *is* large relative to typical activity. |
| B. Immediate execution cannot reduce timing risk but increase market impact. | False | Reverses the conclusion: speed reduces exposure time but demands liquidity aggressively (raising impact). |
| C. Slower execution may reduce participation at any moment but leaves more time for the price to move adversely. | True | Lower urgency reduces footprint while increasing timing exposure. |
| D. Splitting the order guarantees a lower total execution cost. | False | Adverse price moves or information leakage can make slower execution more expensive. |
| E. Strategy capacity should be evaluated because the desired trade is large relative to available market volume. | True | The ability to trade the required size is an implementation constraint. |

**Reference:** Harris, *Trading and Exchanges* — order splitting, timing risk, information leakage. Investopedia — Market Impact / strategy capacity.

### [QF-D5G7Q2] Fixed-schedule vs. volume-sensitive algorithms
**Scenario:** One algorithm releases equal-sized child orders every five minutes regardless of volume; a second varies participation with observed volume.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. Both approaches split a parent order into smaller child orders. | True | Each stages execution rather than submitting the full order at once. |
| B. The fixed schedule necessarily completes at the market's volume-weighted average price. | False | A schedule does not guarantee any particular benchmark price. |
| C. A volume-sensitive schedule may trade more when market activity is greater. | True | Participation-based execution scales trading with market activity. |
| D. Predictable child orders cannot create information-leakage risk if other traders infer the parent order. | False | Reverses the conclusion: detectable patterns *can* reveal sustained buying or selling interest. |
| E. No execution algorithm can simultaneously eliminate market impact, timing risk, and non-completion risk. | True | Execution involves trade-offs among competing risks. |

**Reference:** Harris, *Trading and Exchanges* — execution algorithms (TWAP/VWAP/POV) and information leakage. Investopedia — VWAP; algorithmic execution.

### [QF-D5G7Q3] Urgency, alpha decay, and execution speed (embedded-claim traps)
**Scenario:** A desk planning to buy gradually over six hours learns its signal will decay within one hour after unexpected news, so it increases execution speed.
**Answer polarity:** Normal

| Choice | Verdict | Why |
|--------|---------|-----|
| A. Faster execution can be rational when the opportunity is short-lived. | True | Delayed completion may miss a transient opportunity. |
| B. Increasing speed generally reduces exposure to signal-decay and adverse-movement risk. | True | More of the order is completed before the signal or price can change. |
| C. A reviewer would be wrong to accept the claim that increasing speed can require crossing the spread or consuming deeper liquidity more aggressively. | False | Embedded-claim trap. Urgency *can* increase spread costs and market impact, so the underlying claim is correct and should be accepted. |
| D. The change in urgency has no relevance to the appropriate execution strategy. | False | Urgency is central to balancing completion, timing, and price risks. |
| E. A reviewer would be wrong to accept the claim that the best schedule depends on expected alpha decay as well as transaction costs. | False | Embedded-claim trap. Optimal execution balances the value of acting quickly against implementation costs, so the underlying claim is correct and should be accepted. |

**Reference:** Harris, *Trading and Exchanges* — urgency, alpha decay, and the impact–timing trade-off. CFA curriculum — implementation shortfall and optimal execution scheduling.

## References (domain-level)

- Larry Harris, *Trading and Exchanges: Market Microstructure for Practitioners* — bid/ask quotes, limit order book, depth, market impact (temporary vs. permanent), execution algorithms, and information leakage.
- CFA Program curriculum — Trading, Execution, and Costs: order types, implementation shortfall (decision-price benchmark and cost decomposition), transaction-cost analysis.
- Investopedia — *Bid-Ask Spread* (cost of immediacy, relative spread).
- Investopedia — *Market Order vs. Limit Order* (execution vs. price certainty, fill risk).
- Investopedia — *Slippage* and *Market Impact* / *Order Book & Market Depth* (walking the book, liquidity).
- Investopedia — *Short Selling* (sell-to-open/buy-to-close, borrow fees, dividend obligation, unlimited loss, short squeeze/recall risk).
