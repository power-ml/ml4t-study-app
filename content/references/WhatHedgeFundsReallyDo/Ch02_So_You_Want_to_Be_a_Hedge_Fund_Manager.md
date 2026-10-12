# What Hedge Funds Really Do — Ch. 2: So You Want to Be a Hedge Fund Manager

*Source: Romero & Balch, What Hedge Funds Really Do, PDF pages 13–21 (no separate printed page
numbers; PDF page labels = PDF page numbers). Sections: The Economic Role of Investing; What Are Hedge
Funds?; How Hedge Funds Differ from Mutual Funds; Hedge Fund Strategies; Funds of Funds; Hedge Fund
Fees; Evaluated (I) Return; Evaluated (II) Return vs Benchmark; Evaluated (III) Risk; Sharpe Ratio.*

> ML4T exam relevance: returns, CAGR/compounding and the Rule of 72 → QF D1; volatility, drawdown,
> Sortino, Sharpe ratio → QF D2; benchmarks/alpha, fee drag, active vs passive → QF D7/D10; long/short,
> 130/30, leverage → QF D7/D10.

## The Economic Role of Investing (p.13)
- Economies grow by applying accumulated **capital** (from household savings) to produce goods/services.
  Savings are invested only if instruments offer an attractive return.
- The financial sector (hedge funds a major part) **redeploys capital from poor-return assets to
  superior-return assets** — makes finite savings be used most efficiently.
- Small investors buying individual stocks/bonds may lack capital to **diversify** to control risk.
- **Mutual funds** pool investors' capital and buy a diverse portfolio consistent with the fund's
  **charter** (e.g., large mature companies, small speculative companies, short-term corporate bonds).
  Called "unit investment trusts" in the UK. Heavily regulated (SEC, Investment Company Act of 1940).

## What Are Hedge Funds? (pp.13–14)
- Mutual funds are restricted to their charter, described in a **prospectus**; most aspire to be fully
  invested most of the time.
- First hedge fund: **Albert Winslow Jones, 1949** (ex-journalist), more flexible style.
  - **Pair trades**: two companies expected to move in opposite directions (e.g., duopoly competitors) →
    **go long** one, **go short** the other. The short **hedges** against the whole market moving against
    the position. Jones called it a "hedged fund."
- Growth: passed $100B AUM early 1990s; $500B ~2000; $1T ~2004; ~10,000 funds now manage > $2T.
  If uniform (they definitely are not), a typical fund would manage $200M.

## How Hedge Funds Differ from Mutual Funds (p.14)
- Both = pools of investor capital run by a manager. **Mutual funds are far more transparent**: accept
  SEC regulation as the price of access to millions of small investors; must specify strategies in a
  prospectus and report holdings and results regularly.
- **Hedge funds are very lightly regulated**. In the US, **investor qualification** replaces regulation:
  investors must be **"accredited"** (assets in the upper few percent of households). Hedge funds are
  **prohibited from advertising** (book notes this may soon change).
- Original investors were wealthy individuals/families; by the 1990s overtaken by **large institutions**
  (endowments, pension funds).
- **Secrecy** exists because legally protecting financial IP is virtually impossible → secrecy is the only
  way to delay copying. Holdings/strategies generally not disclosed publicly, and reported to investors
  only broadly, after the fact.

## Hedge Fund Strategies (pp.14–15)
- Four major types:
  1. **Equity** — emphasis on stock selection; many follow Jones's long/short model.
  2. **Arbitrage** — price relationships between assets fall outside normal variation; bet on return to
     normal. Started in fixed income; now any market where quant analysis finds discrepancies.
  3. **Momentum or direction** — manager has a macro view of probable price direction in a market.
  4. **Event-driven** — trades instigated by an event (war, supply disruption, merger). "Global macro"
     funds rose in the 1990s mainly with event-driven strategies; some famous for **merger arbitrage**.
- No taxonomy lasts long (young, fast-innovating industry).
- **Long-only** (profit only if price rises), **short-only** (profit only if price falls), or **(most
  commonly) hedged** — both long and short, **usually not equally**.
- Profits per transaction are small → many hedge funds **borrow extensively to leverage** ("gearing" in UK).
- **130/30** equity strategy: long 130% of capital (borrowing 30% beyond 100% equity) and short 30% as
  a hedge.
- Original funds ran on experience/instinct (Jones, Robertson, Steinhardt, Soros). By the 1990s, quant
  finance + cheap computing enabled examining thousands of price relationships → "rocket scientists"/quants.

## Funds of Funds (p.15)
- Hedge funds can't advertise → hard for clients to choose; competition erodes strategies fast.
- **Funds of hedge funds** select, monitor, and reallocate among hedge funds — and **add their own fees
  on top** of the hedge funds' fees.

## Hedge Fund Fees (p.16)
- Mutual funds: **expense ratio** as % of AUM; median a bit more than **1%/yr**; some also charge a
  **load** (front-end or back-end). Expense ratio is **not performance-dependent** — paid even in
  negative-return years.
- Hedge funds: hybrid **"2 and 20"** — ~**2%** expense/management fee + **20%** of returns.
  - The book states the 20% performance fee is on **absolute performance, not performance above a
    benchmark** (trap: it is not a benchmark-relative fee).
  - Same structure as private equity. **Not universal**: Renaissance Medallion charged **5% and 44%**;
    incentive fees as high as **55%** heard of; after 2008 some dropped to **1% and 10%**.
- Fees have made many founders billionaires; critics say the industry overcharges and underdelivers.

## How Hedge Funds Are Evaluated (I): Return (pp.16–18)
- Core issues in evaluating any investment: **return and risk**.
- **Return = [Value(t) / Value(t−1)] − 1**. Example: $110/$100 − 1 = 0.1 = **10%**.
- Book mostly uses **daily returns**; annualized by compounding over **252 trading days**:
  `annual_return = cumprod(daily_returns + 1) − 1` (Python). 260 weekdays in a 52-week year, minus ~8
  market holidays.
- **CAGR (compound annual growth rate)** is the right multi-year annual return (compounding).
  - Worked example: $100 (2002) → $200 (2012) = **100% cumulative return** over 10 yrs. Annual return is
    **not** 100%/10 = 10% (that ignores compounding).
  - $200 = $100 × (1 + CAGR)^10 → 2 = (1 + CAGR)^10 → 2^(1/10) = 1.072 → **CAGR = 7.2%**.
  - 7.2% compound doubles in 10 years; "simple" (non-compounded) growth would need 10%/yr.
- **Rule of 72**: periods to double ≈ 72 / CAGR (CAGR in whole numbers).
  - 8% → ~9 years (8×9=72); 6% → 12 years; doubled in 15 years → CAGR ≈ **4.8%** (15×4.8=72).
  - Works for multiples of two: 4× = 2^2, 8× = 2^3; **100-fold is a bit less than 2^7**; **1000-fold ≈
    2^10** (1,024).
  - Wall Street interviewers routinely ask compounding mental-math questions.
- **Fee worked examples** (20% of return over and above a 2% management fee):
  - Fund returns **4%** → manager gets 2% + 0.2 × (4% − 2%) = 0.4% → **2.4% of AUM** = **60%** of the
    portfolio's return (2.4/4).
  - Fund returns **10%** → 2% + 0.2 × (10% − 2%) = 1.6% → **3.6%** = **36%** of the return.
  - All of the first 2% goes to the manager, then 20% of returns above 2%.
  - **Negative returns** → no incentive fee, but the 2% management fee is still charged (far more than
    the client's negative return).

## Evaluated (II): Return Versus Benchmark (Relative Return) (pp.18–19)
- Paying on absolute return implicitly assumes the only alternative is "the mattress"; realistically,
  investors have alternatives (T-bills, commercial paper, equities).
- **Benchmark**: a **nonmanaged** investment that is a relevant comparator. For equity funds most commonly
  a stock **index** such as the **S&P 500** (500 largest US-listed companies by market cap). Narrower
  strategies → narrower indexes or a weighted combination of indexes. HFRX (Hedge Fund Research) hedge
  fund index exists but has significant drawbacks.
- **Alpha** = exceeding a benchmark; a measure of investing skill (defined later in the book).
- Decades of research (mostly mutual funds): **very few active managers consistently beat their
  benchmark**. Active management **at best matches, and more typically underperforms, benchmark indexes
  *before* management costs**; frequent trading and fees are further drag.
- Hedge-fund studies: managers **frequently generate positive alpha**, but compensation absorbs **at
  least half** of annual excess return over the benchmark. One analysis (1998–2010): managers absorbed
  **84–98%** of total profits (clients kept 1/50 to 1/6). In one-fourth of those years total profits were
  negative, yet managers were still paid 2% of AUM.
- Bogle (Vanguard, originated indexed investing): mutual fund investors "get what they **don't** pay for."
  Hedge-fund analog: "no gain without at least equal pain."

## Evaluated (III): Risk (pp.19–20)
- Hedge funds aim not solely to maximize return but to **control risk** ("hedge").
- **Risk is operationalized as volatility** of a portfolio's returns.
- Figure 2.1 (Mar 2009–Jul 2012): **Dow** cumulative 43% (11.6%/yr) vs **a fund** 33% (9.2%/yr); fund had
  significantly less volatility. "Reduced volatility" is what investors pay hedge funds for.
- Most common volatility measure: **standard deviation of per-period returns**. The book's wording:
  "the square root of the sum of the squared deviations ... versus the mean for all periods in the
  sample" (it does not spell out dividing by N). Book's example: mean daily return 0.1%, June 1 return 0.3% →
  deviation 0.2%, squared deviation written as ".04% = 0.2%^2" (book calls this the day's "variance"; the
  squaring corrects for negative deviations). [Note: the book's text says "per period prices" at one point
  but means returns.]
  - Dow SD **1.23%** vs fund **0.58%** → fund less than half as volatile.
- Critique: SD treats upside and downside deviations alike ("a measure only an academic could love").
  - **Drawdown**: maximum drop from **peak to trough**, as % of the peak.
  - **Sortino ratio** focuses on the **downside**; the more common **Sharpe ratio is indifferent** between
    upward and downward deviations.

## Sharpe Ratio: Combining Return and Risk (pp.20–21)
- CAPM observation: across asset classes it's virtually impossible to increase return without increasing
  risk → use a combined measure (analogous to cost–benefit analysis).
- Developed by Nobel laureate **William Sharpe**. Numerator = **excess return over the risk-free rate**
  (usually short-term T-bills — that return is available with no risk); denominator = **standard deviation
  of portfolio return**:
  - **Sharpe Ratio = (r_portfolio − r_risk-free) / σ_portfolio**
- Worked example: S&P 500 since 1926 ≈ 10% nominal return, risk-free ≈ 2.5%, SD ≈ 15% →
  (10% − 2.5%)/15% = 7.5%/15% = **0.5**.
- Interpretation: higher = better. 1.0 can be loosely viewed as "fairly compensated for risk," but the
  stricter reading is just "higher is better." **Sharpe ratios at or above 1.0 are *very* uncommon.**
- Figure 2.1 portfolios: Dow **0.63**, fund **0.94** → fund superior by about half again, risk-adjusted
  (despite lower raw return).
- Drawdown and Sortino ratios are especially relevant to hedge funds, whose raison d'être is minimizing
  falls in down markets at the cost of reduced upside in rising markets.

## Exam traps (book-grounded)
- Cumulative return ÷ years ≠ annual return (CAGR must compound): 100% over 10 yrs = 7.2%/yr, not 10%.
- "2 and 20": the 20% is on absolute performance, **not** above a benchmark; the 2% is charged even
  in losing years.
- Hedge funds are "most commonly" hedged — long and short, but **usually not equally**.
- Sharpe uses **excess** return (minus risk-free) and **total SD** — it does not distinguish upside from
  downside volatility (Sortino does).
- A fund with **lower** raw return can have the **higher** Sharpe (fund 9.2% vs Dow 11.6%; Sharpe 0.94 vs 0.63).
- Active management typically underperforms benchmarks even **before** costs (per the research the book cites).

## ML4T exam relevance
- Daily return, cumulative return, CAGR, 252-day annualization, Rule of 72 → **QF D1 Investment Returns & Compounding**.
- Volatility as SD, drawdown, Sortino, Sharpe ratio formula and examples → **QF D2 Risk & Risk-Adjusted Performance**.
- Benchmarks, alpha as skill, fee drag on excess return, active vs passive → **QF D7 CAPM/Alpha/Beta/Hedging**, **QF D10 Strategy Design & Evaluation**.
- Long/short pair trades, 130/30, leverage, strategy taxonomy (equity, arbitrage, momentum, event-driven) → **QF D7**, **QF D8 Market Efficiency & Arbitrage**, **QF D10**.
- Diversification as the reason for pooled funds → **QF D3 Diversification & Correlation** (light).
