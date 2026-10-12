# What Hedge Funds Really Do — Ch. 7: Framework for Investing: The Capital Asset Pricing Model (CAPM)

*Source: Romero & Balch, What Hedge Funds Really Do, PDF pages 39–45 (no separate printed page
numbers; PDF page labels = PDF page numbers). Sections: (intro: CAPM, EMH, indexing); An Overview of
CAPM; The ABCs of CAPM: Alphas, Betas, and Correlations; Implications of CAPM; Basic Hedge Fund
Strategies in the CAPM Framework.*

> ML4T exam relevance: return decomposition into beta (market) and alpha (stock-specific), beta as
> regression slope, alpha as intercept, correlation as scatter tightness, portfolio return as weighted
> average, dollar-balanced vs beta-balanced hedges, leverage → QF D7 CAPM/Alpha/Beta/Hedging (primary);
> correlation & diversification → QF D3; indexing/active management → QF D8; regression framing → ML D4.

## Introduction (p.39)
- Rigorous portfolio-appraisal frameworks only arose mid-20th century. The book states Merton Miller, Franco
  Modigliani, and William Sharpe shared the **1990 Nobel** for developing CAPM (as written in the book).
- **CAPM + EMH** implication: **very few investors can produce sustained returns superior to market
  averages** → adherents asserted buying "the market" (an index) beats most strategies.
  - Malkiel, *A Random Walk Down Wall Street* (1973) — first popular book on **indexing**; Bogle founded
    **Vanguard** (early 1970s) for retail **index investing**.
- **Hedge funds are premised on the belief that outperforming a long-only index strategy *is* possible.**
  CAPM still matters: hugely influential, and it **breaks investing performance into component parts**.

## An Overview of CAPM (pp.39–40)
- Figure 7.1: daily prices of **XOM** (ExxonMobil) and **SPX** (S&P 500), late 2011–late 2012. They
  **mostly** move in tandem, suggesting:
  - A strong **positive correlation** — most events affect both similarly.
  - XOM's changes are (mostly) **less pronounced** than SPX's.
- **Core of CAPM: distinguishing stock returns that derive from broad market movements from those that do not.**

## The ABCs of CAPM: Alphas, Betas, and Correlations (pp.40–43)
- Figure 7.2: daily % changes (returns) of XOM and SPX; often indistinguishable.
- Return = (Price_t / Price_{t−1}) − 1.
- **Correlation** — book's simple description: "measures the frequency with which prices of two assets move
  in the same direction." Range:
  - **−1.0** perfect negative (S&P rises → XOM falls, and vice versa); **0** no visible relationship;
    **+1.0** perfect positive.
- Combining assets with **low or negative correlations** (near zero or negative) **dampens portfolio
  volatility (lowers risk)**.
- Figure 7.3: **scatter plot** of XOM daily returns (y) vs SPX daily returns (x), one dot per day. Upward-
  sloping oval → positive correlation (0 to 1). If XOM benefited from events that hurt the market, the
  scatter would slope **downward** (correlation −1 to 0).
- Fit a **regression line**: Y = b × X + a →
  **Return(XOM) = beta × Return(SPX) + alpha**; **alpha = Y-intercept**, **beta = slope**.
- Interpretations:
  - **Alpha** = the **systematic difference in return of a stock over and above the market**. Sources:
    superior management, production technology, product design, or a dominant position giving **pricing
    power**. Because all stocks together **are** the market, **alpha is assumed to be zero on average**
    (positive-alpha stocks offset by negative-alpha stocks).
  - **Beta** = the stock's **price volatility relative to the overall market**. Beta 1.5 → rises/falls on
    average 1.5× as much as the market (percentage terms).
    - **Small speculative companies: betas well above 1.0**; **large stable-earnings companies: well under 1.0**.
    - **XOM beta = 0.77** (moves almost as much as the market).
    - **The market's beta is 1.0 by definition.** Beta = slope of the Fig 7.3 regression line; published on
      sites like Google/Yahoo Finance.
  - **Correlation coefficient** = the **"tightness" of the scatter around the regression line**. Closer to
    1.0 → more of XOM's moves are **explained** by SPX moves (market events have similar effects on XOM).
  - [Trap: beta (slope) and correlation (tightness) are distinct quantities in the book's framing.]

## Implications of CAPM (p.43)
- Return from market rise = **"buying beta"**; return from investment skill = **"seeking alpha."**
- Extensive mutual-fund research finds **little evidence of persistent alpha** among managers.
- CAPM's basic disaggregation: **beta** (market return, achievable by buying an index) + **alpha**
  (company-specific factors).
- Index funds/ETFs give a beta of 1.0 extremely cheaply → to outperform, either buy **stocks more volatile
  than the index (buying beta)** or find stocks that systematically outperform (**buying alpha**).
- **Buying beta = buying increased risk** (high-beta stocks rise faster on up days **and fall farther on down
  days**). **Buying alpha is oft-sought but rarely achieved.**

## Basic Hedge Fund Strategies in the CAPM Framework (pp.43–45)
- A. W. Jones's 1949 fund sought **absolute positive returns through hedging** — contrary bets paying off if
  the main bet failed. Hedges at minimum reduce losses; at best give returns above zero even in a falling
  market; in exchange they **drag returns when the market rises**.
- **Portfolio return = weighted average of constituent returns.**
  - Worked example: 60% XOM (return 8%) + 40% SPY (return 10%) → 0.6×8% + 0.4×10% = 4.8% + 4% = **8.8%**
    (between the two, shaded toward the larger weight). SPY = ETF tracking SPX.
- In CAPM terms: return(portfolio) = w_XOM × return(XOM) + w_SPY × return(SPY), with
  return(XOM) = β_XOM × return(market) + α_XOM and return(SPY) = β_SPY × return(market) + α_SPY;
  **assume β_SPY = 1.0 and α_SPY = 0** (it is the market).
- **Hedge example**: believe XOM will outperform. Long-only investor loses if the market drops. Hedge fund:
  **long XOM, short SPY**. With **+50% XOM, −50% SPY**:
  - Return = 0.5 × [β_XOM × r_m + α_XOM] − 0.5 × [β_SPY × r_m + α_SPY] (negative weight = short).
  - If XOM falls because the market falls, the short **at least partly compensates**; if both rise, XOM
    gains are **at least partly offset** by the short.
- **Dollar balanced ≠ beta balanced**:
  - 50/−50 is **dollar balanced** (equal $ long and short) but **not beta balanced**, because XOM's beta
    (0.77) < SPY's (1.0); positions don't fully cancel. In an up market the portfolio is net long only if
    XOM's alpha is large enough to offset the **0.23** beta difference (1.0 − 0.77).
  - If betas were very close, the positive return would be **0.5 × the long position's alpha**.
- **Most hedge funds seek beta-balanced portfolios** to be precisely protected against market-wide moves:
  - **Σ(β_i × w_i) = 0** and **Σ|w_i| = 1.0**.
  - Lower-beta XOM needs a **larger** weight: beta-balanced = **56% XOM, −44% SPY** (algebra left as exercise
    in the book). [Check: 0.77 w = 1.0 (1 − w) → w ≈ 0.565.]
- Such excess returns are **quite small** → hedge funds trade huge volumes and use **leverage**; many
  institutions leverage **20 or 30 times** capital. **Leverage magnifies both gains and losses** → that's why
  high leverage is often combined with hedged long/short strategies.

## Exam traps (book-grounded)
- Alpha = **intercept**, beta = **slope**, correlation = **tightness** — don't swap them.
- Market beta = **1.0 by definition**; market alpha = **0 by definition**; alpha averages zero across all stocks.
- High beta ≠ skill: buying beta = buying more risk (bigger down-day losses too).
- **Dollar-neutral does not mean beta-neutral** (50/−50 XOM/SPY is still skewed by the 0.23 beta difference).
- A beta < 1 long needs a **larger** long weight than the short (56/−44), not equal weights.
- Hedges reduce losses in down markets but **drag** returns in up markets — not free.
- Low/negative correlation **reduces** portfolio volatility.
- Leverage magnifies **losses as well as** gains.

## ML4T exam relevance
- Return(stock) = β × Return(market) + α; alpha intercept / beta slope; buying beta vs seeking alpha; persistent alpha is rare → **QF D7 CAPM/Alpha/Beta/Hedging**.
- Portfolio return as weighted average; long/short hedge; dollar-balanced vs beta-balanced (Σβw = 0, Σ|w| = 1); 56/−44 example; leverage → **QF D7**, **QF D4 Portfolio Optimization** (weights/constraints), **QF D10**.
- Correlation range −1..+1, low/negative correlation dampens volatility → **QF D3 Diversification & Correlation**.
- CAPM + EMH ⇒ indexing; hedge funds premised on beating the index → **QF D8 Market Efficiency & Arbitrage**.
- Fitting a regression line to a return scatter (slope/intercept) → **ML D4 Linear Models**.
