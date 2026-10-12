# What Hedge Funds Really Do — Ch. 12: Overcoming Data Quirks to Design Trading Strategies

*Source: Romero & Balch, What Hedge Funds Really Do, PDF pages 68–72 (no separate printed page
numbers; PDF page labels = PDF page numbers). Sections: (intro); Actual Versus Adjusted Stock Price
Data; Stock Splits; Dividends; Breaks in Series and Missing Data; Missing Ticker Symbols; Conclusion.*

> ML4T exam relevance: actual vs adjusted prices, split and dividend adjustment for backtests, fill
> forward / fill backward for missing data, symbol changes, survivor bias, sanity-checking data → QF D9
> Financial Data & Research Bias (primary); backtest design → QF D10; data hygiene → ML D2 Data &
> Sampling Discipline.

## Introduction (p.68)
- Stock price data are widely available → expect **many strategies have already been found** by competitors.
- Data used for **event studies and backtesting** "cannot be used without special care." The chapter lists
  main pitfalls and coping strategies — **hardly exhaustive**.

## Actual Versus Adjusted Stock Price Data (p.68)
- **Actual price data** (as reported by financial services) used naively **can be misleading** — prices
  often change for reasons **unrelated to supply and demand**: **splits** and **dividends**.
- Can be handled manually in backtests if the database has that info, but most researchers fold both into
  **adjusted price** — streamlines backtesting.

## Stock Splits (pp.68–70)
- Boards split when price seems too expensive for some investors (most trades are **round lots of ≥100
  shares**; options cover 100 shares). $100/share → $10,000 smallest economic position.
- Split: each old share → N new shares. **Company value does not change**; each share worth proportionately less.
  - **2-for-1**: 100 shares → 200 shares. Split should not in itself change holding value ("a medium pizza is
    still a medium pizza, whether sliced into 4, 6, or 8 pieces").
- Figure 12.1 (IBM actual vs split-adjusted, 1963–2012): IBM split several times 1962–2012.
  - **1979: actual price ~$300 → ~$75 = a 4-for-1 split**; holder's total value and ownership fraction unchanged.
  - IBM's actual **1962 price > $500** corresponds to ~**$2.50 adjusted** (over **200-fold** difference).
  - 2012 price ~$200 → appreciated ~**80-fold** ($2.50 → $200) over 50 years ≈ **9% annual return**.
- **Data services adjust for splits**: if a stock split 2-for-1 on Jan 1, 2012, **all prior prices are
  halved**. Actual prices would show a **50% one-day drop**; adjusted prices show the real long-term trend.
- **When you conduct event studies or backtest trading strategies, it is crucial to use split-adjusted prices.**
- Some boards avoid splits (believing high prices attract long-term investors): AAPL ~$500/share (100 shares ≈
  $50,000) at writing; **Berkshire Hathaway (BRKA) has never split** (> $100,000/share) despite 20%+ annual
  appreciation for ~50 years; mid-2000s created **Class B (BRKB) at 1/1500th** of A shares.
- **Reverse split** (e.g., **1-for-3**): price rises — a share controls 3× as much. **$30 → $90**.

## Dividends (p.70)
- **Dividend** = cash return to shareholders of a portion of annual earnings, declared by the board.
  **Payout ratio** = that proportion. Regular (usually **quarterly**) or special one-time dividends.
- Long-term value of owning a stock = actual price **plus** value shed over time as dividends.
- **Dividend yield = annual dividend per share / share price**. Average ~**2%** presently; some up to 10%;
  some pay none (BRK; AAPL until recently).
- Paying a dividend distributes cash → company assets fall → **share price typically drops by an equivalent
  amount**, but the holder still captures the value.
- IBM example: actual vs adjusted prices differed before **Feb 6, 2014**, due to a **$0.95 dividend** paid that day.
  - Adjust: dividend ≈ **0.55%** → **all previous historical prices adjusted downward by that same
    proportion** → in backtesting this reaps a **0.55% "reward" on the dividend date**.

## Breaks in Series and Missing Data (pp.70–71)
- Price data may be missing if a stock's trading (or all trading) is **suspended**. Example: **NASDAQ halted
  just over 3 hours on Aug 22, 2013** (faulty communications with NYSE computers) — Figure 12.2.
- **Solvers such as QSTK cannot handle missing data** (they return errors) → must fill with reasonable guesses.
- **Fill forward**: treat missing values as the **last known value**. NASDAQ example: treat all values
  **12:14 p.m.–3:10 p.m.** as the **12:13 p.m.** (last traded) value.
- If values are missing at the **beginning** of a series, fill forward isn't possible → **fill backward**:
  apply the first known value to prior missing periods.
- **Rule: "fill forward first, and fill backward where you can't fill forward."**

## Missing Ticker Symbols (pp.71–72)
- Stocks may be **listed mid-series** (e.g., IPO) or **delisted** (acquired, gone private, out of business)
  → missing data before/after.
- Companies change symbols: **Sun Microsystems** had **at least three symbols** in ~25 years (1980s listing to
  Oracle acquisition).
- Analysts must check whether sudden (dis)appearances are **real births/deaths or merely relabeling**.
- **Omitting stocks/companies (or funds) during a series introduces bias**: the omitted one has commonly run
  into trouble, often fatal. Hedge funds that shut down often far underperformed peers; per **eVestment, only
  30% of funds that existed 10 years ago are still in business**.
- Scrubbing the sample to include only companies operating **throughout the period** tends to omit **more
  failures than successes** → **survivor bias**.

## Conclusion (p.72)
- These data problems are **unavoidable**: capitalism's **"creative destruction"** kills poor performers and
  (sometimes) buys up good ones; market glitches happen (sometimes caused by hedge funds).
- Goal is **not** to choose a sample that **avoids** these problems — that would make the analysis
  **virtually irrelevant**. Instead: **don't accept data uncritically, and check data for sanity**.

## Exam traps (book-grounded)
- A split **does not change company value** or a holder's total value; unadjusted prices show a spurious drop
  (−50% for 2-for-1; ~$300 → $75 for IBM's 4-for-1).
- Split adjustment changes **historical (prior) prices**, not post-split prices (all prior prices halved for 2-for-1).
- Dividend adjustment lowers **prior** prices by the dividend **proportion** (≈0.55% for IBM), creating a
  "reward" on the dividend date in backtests.
- Reverse split **raises** the per-share price (1-for-3: $30 → $90).
- Missing-data order: **fill forward first, then fill backward** (backward only where forward is impossible,
  i.e., at the series start).
- Restricting the sample to firms alive the whole period **causes** survivor bias (omits more failures).
- The book's advice is to **keep** messy data and sanity-check it — **not** to choose a clean sample that
  avoids the problems.
- A ticker disappearing may be a **symbol change**, not a company death.

## ML4T exam relevance
- Actual vs adjusted price, split/dividend adjustments, reverse splits, dividend yield/payout ratio → **QF D9 Financial Data & Research Bias**.
- Fill forward / fill backward, suspensions and missing data, solver errors on NaNs → **QF D9**, **ML D2 Data & Sampling Discipline**.
- Missing tickers, symbol changes, delistings, survivor bias (eVestment 30% survival) → **QF D9**; universe construction → **ML D2**.
- Using adjusted prices in event studies/backtests; sanity-checking data; not cherry-picking clean samples → **QF D10 Quantitative Strategy Design & Evaluation**, **QF D9**.
