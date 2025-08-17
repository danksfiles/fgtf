# NOTES.md: Formula & Known Issues

This document outlines the initial formula for the Fear & Greed Index, its components, and the assumptions made during its design. It serves as a starting point for backtesting and validation as per `forward.md`.

---

## 1. Fear & Greed Formula (Version 1.0)

The index is calculated as a weighted average of several indicators, each normalized to a scale of 0 (Extreme Fear) to 100 (Extreme Greed).

### Pseudocode:
```
function calculate_fear_greed_index():
    # Indicator weights must sum to 1.0
    volatility_weight = 0.40
    momentum_weight = 0.30
    social_sentiment_weight = 0.30

    # Get normalized indicator values (0-100)
    volatility_score = get_volatility_score()
    momentum_score = get_momentum_score()
    social_score = get_social_sentiment_score()

    # Calculate final index
    fear_greed_index = (volatility_score * volatility_weight) + \
                       (momentum_score * momentum_weight) + \
                       (social_score * social_sentiment_weight)

    return fear_greed_index
```

---

## 2. Indicator Definitions

### a. Volatility (40% weight)
- **Measures**: Compares current asset volatility to its 30-day and 90-day average.
- **Logic**: Higher-than-average volatility is a sign of a fearful market.
- **Signal**:
    - `100` (Extreme Greed): Volatility is at the bottom 5% of its historical range.
    - `0` (Extreme Fear): Volatility is at the top 5% of its historical range.

### b. Market Momentum (30% weight)
- **Measures**: Compares the current asset price to its 125-day moving average.
- **Logic**: A sustained period of prices being above the average indicates greed, while below indicates fear.
- **Signal**:
    - `100` (Extreme Greed): Price is significantly and consistently above the 125-day MA.
    - `0` (Extreme Fear): Price is significantly and consistently below the 125-day MA.

### c. Social Sentiment (30% weight)
- **Measures**: Analyzes the volume and tone of social media posts (e.g., Twitter, Reddit) related to the asset.
- **Logic**: Unusually high volume of positive mentions suggests greed; high volume of negative mentions suggests fear.
- **Signal**:
    - `100` (Extreme Greed): High volume of positive sentiment, low negative.
    - `0` (Extreme Fear): High volume of negative sentiment, low positive.

---

## 3. Known Issues & Assumptions

1.  **Arbitrary Weights**: The initial weights (`0.40`, `0.30`, `0.30`) are subjective and not based on rigorous analysis. They are the first thing that should be tuned during backtesting.
2.  **Indicator Simplification**: The indicators are simplified for this initial version. For example, "social sentiment" is a complex field and requires a robust data source and NLP model, which is not yet implemented.
3.  **Data Source Dependency**: The quality of the index is entirely dependent on the quality and reliability of the underlying data feeds (VIX, price data, social media APIs). A failure or anomaly in any one source could significantly skew the index.
4.  **Overfitting Risk**: The formula and its parameters (e.g., moving average periods) must be carefully tested to avoid overfitting to the historical data used for backtesting. Walk-forward validation is necessary.
5.  **Lack of On-Chain Metrics**: This initial version omits on-chain data (e.g., transaction volume, whale activity), which is a critical component for a comprehensive crypto sentiment index. This is a planned future addition.

---

## 4. Next Steps

- **Backtest**: Use the `initial_spy_vix_backtest.ipynb` notebook to implement and test this formula against historical SPY and VIX data.
- **Parameter Tuning**: Experiment with different indicator weights and moving average periods to see how they affect signal quality.
- **Data Source Integration**: Begin implementing data ingestion modules for the required indicators.
