# ML4T Exam 1 — Tactics & Trap Cheat-Sheet

## Scoring mechanics (from the prep guide)
- 40 questions; 2 drawn per domain across the 20 domains. Each question = 5 choices scored **independently** True/False. 1 raw point per correct T or F; 200 raw → %.
- **Do NOT mark all 5 the same** (all-True or all-False) — the guide warns it may zero the whole question. Every question has ≥1 True and ≥1 False, so a uniform answer is always wrong and flagged.
- Unmarked choices score 0 — move every choice into True or False.
- Partial credit is per-choice, so answer every sub-choice even when unsure.

## The #1 trap: read the answer polarity FIRST
Each question's answer key is one of two modes:
- **Normal:** "Answer Key:" → **True = the statement is accurate.**
- **Inverted:** "Answer Key (True = incorrect; False = accurate)" → the prompt asks you to flag the FLAWED statements, so **True = the statement is WRONG.** Read the instruction line before answering or you invert every mark.

### Where inverted questions live (ML only)
**Every inverted-logic question in Exam 1 is in the ML domains. Quant Finance has ZERO inverted questions** — all 210 QF questions are Normal polarity. Inverted counts (verified from the parsed pool): ML D1=11, D2=12, D3=12, D4=8, D5=8, D6=12, D7=8, D8=7, D9=6, D10=11 = **95 of 308 ML questions**.

## The #2 trap: choice-level negation / "embedded claim" (heavy in QF)
Even in Normal-polarity questions, individual choices flip meaning with wording like:
- **"It is incorrect to conclude that <X>"** / **"The following claim is false: <X>"** / **"A reviewer would be wrong to accept that <X>"** — if the inner claim X is actually accurate, the whole choice is **False**. Parse the inner claim, judge its truth, then negate.
- **"... is not <the correct value>"** — the pool marks these **False** with the recurring phrase *"the statement reverses the correct conclusion."*
QF domains lean on these instead of question-level inversion (e.g., QF D8 had 16 such choices, QF D4 ~20). Slow down and evaluate the literal claim.

## The #3 trap: absolute/overreaching claims are usually False
"always / guarantees / proves / riskless / cannot lose / eliminates / must" → almost always the flawed (False, or True-under-inversion) choice. In inverted ML questions the textbook-correct statements resolve to "False" and the absolute overreach is the "True (incorrect)" answer.

## Answer-key oddities to be aware of (verified against the pool, verdicts preserved)
These are flagged inline in the domain files with a **Note:** — know them so a quirky key doesn't throw you:
- **ML D1 · G3Q1 D** — the key's own rationale reads inconsistent with its verdict (marked True, but the rationale argues the statement is accurate). The one genuinely self-contradictory item.
- **ML D6 · G5Q5** — the source key's verdict LETTERS are scrambled vs the choice text; notes remap by content (A T, B F, C T, D T, E T).
- **ML D3 · G1Q5 and G1Q6** — verbatim duplicate questions (identical scenario/choices/key: only E True).
- **ML D2 · G1Q5B** — terminology only (pool calls it "Selection Effect", not MNAR); verdict fine.
- **ML D3 · G1Q4C / G3Q5C vs G3Q4D** — mild rationale tension (stationarity wording; correlated-feature stability "holds while correlation structure holds"); verdicts kept.

## Study flow
1. Read this sheet + each domain's **cheat-sheet** and **Common traps** first — that's most of the conceptual coverage.
2. Drill the domain question tables; for ML, rehearse spotting inverted polarity; for QF, rehearse parsing negation/embedded-claim choices and checking the arithmetic (Sharpe, CAGR, turnover, DCF — all verified in the notes).
